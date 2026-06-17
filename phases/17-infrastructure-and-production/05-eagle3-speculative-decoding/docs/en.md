# EAGLE-3 Speculative Decoding in Production | 推测解码 生产 EAGLE

> Speculative decoding pairs a fast draft model with the target model. The draft proposes K tokens; the target verifies in a single forward; accepted tokens are free. In 2026, EAGLE-3 is the production-grade variant — it trains a draft head on the target model's hidden states rather than on raw tokens, pushing acceptance rate alpha into the 0.6-0.8 band on general chat. The right question is not "how fast is the draft" but "what is alpha on my traffic?" If alpha drops below ~0.55, speculative decoding is net negative at high concurrency because every rejected draft costs a second target forward pass. This lesson teaches you to measure alpha first and flip the flag second.

> **【中文解读】** 本节介绍了推测解码——用小模型预测大模型输出来加速推理的技术。


**Type:** Learn | **类型:** 学习
**Languages:** Python (stdlib, toy acceptance-rate simulator) | **语言:** Python（标准库，接受率模拟器）
**Prerequisites:** Phase 17 · 04 (vLLM Serving Internals), Phase 10 · 18 (Multi-Token Prediction) | **前置知识:** Phase 17 · 04（vLLM 服务内部）, Phase 10 · 18（多 Token 预测）

> 🔗 **【前置】** 学本节前请先掌握：Phase 17·04（vLLM）、Phase 10·18（MTP 多 token 预测）、Phase 10·25（投机解码原理）。本节是生产版 EAGLE-3。
> 💡 **【类比】** EAGLE-3 = "翻译员打草稿"。草稿模型（draft）快速猜 K 个 token，目标模型一次验证。猜对=免费，猜错=多一次验证开销。EAGLE-3 创新：用目标模型隐藏状态训练 draft（而非原始 token），接受率 α 提到 0.6-0.8。生产关键问题：α 在你的流量上多少？<0.55 时反而拖慢（拒绝的 draft 浪费算力）——必须先测 α 再开 flag。
**Time:** ~60 minutes | **时间:** ~60 分钟

## Learning Objectives | 学习目标

- Name the three generations of speculative decoding and explain what EAGLE-3 changes from EAGLE-2 and from a classic draft model.
  中文翻译：说出推测解码的三代，并解释 EAGLE-3 相比 EAGLE-2 和经典 draft 模型改变了什么。
- Define acceptance rate alpha, compute expected speedup from alpha and K (draft length), and identify the break-even alpha for your target concurrency.
  中文翻译：定义接受率 alpha，从 alpha 和 K（draft 长度）计算预期加速比，并确定目标并发下的盈亏平衡 alpha。
- Explain why speculative decoding is opt-in (not default) in vLLM 2026 and why turning it on without measuring alpha is a production anti-pattern.
  中文翻译：解释为什么推测解码在 2026 年 vLLM 中是 opt-in（非默认），以及为什么不测量 alpha 就开启它是生产反模式。
- Write a measurement plan: which benchmark, which prompt distribution, which concurrency point, which metric to gate on.
  中文翻译：写出测量计划：哪个基准测试、哪个 prompt 分布、哪个并发点、哪个指标作为门控。

## The Problem | 问题引入

> **【中文解读】** 推理的解码阶段是内存带宽受限的——每解码一个 token 需要读取约 140 GB/s 的权重，GPU 计算几乎空闲。推测解码利用这个空闲：用廉价的小模型生成 K 个候选 token，然后让目标模型在一次前向传播中验证所有 K 个。接受率 alpha 是唯一重要的指标——低于 0.55 时推测解码在高并发下反而有害。

> **【拓展：推测解码的产业应用】** Google 在 2025 年将推测解码部署到 AI Overviews（搜索引擎摘要生成），在不损失质量的情况下显著加快了响应速度。vLLM V1 提供了 `speculative_config` 作为官方接口。生产中，推测解码特别适合实时对话（TTFT 敏感）和代码补全（延迟敏感）场景。但需注意：高并发（256+）时，decode batch 已经足够大，内存带宽的差距缩小，推测解码的收益降低。

Decode is memory-bound. On an H100 running Llama 3.3 70B FP8, each decoded token reads ~140 GB/s of weights and emits one token. The GPU compute is almost idle during decode — the bottleneck is HBM bandwidth, not matmul throughput.

> 解码是内存受限的。在 H100 上运行 Llama 3.3 70B FP8 时，每个解码的 token 读取约 140 GB/s 的权重并输出一个 token。GPU 计算在解码期间几乎空闲——瓶颈是 HBM 带宽，而非矩阵乘法吞吐量。

Speculative decoding exploits the gap. Generate K candidate tokens with a cheap draft model, then ask the target model to verify all K in a single forward pass. Each verified token is effectively free (amortized into a batch-of-K forward the target would have had to do anyway).

> 推测解码利用这个差距。用廉价的 draft 模型生成 K 个候选 token，然后让目标模型在一次前向传播中验证所有 K 个。每个验证通过的 token 实际上是免费的（分摊到目标模型本来就要做的 K 批前向中）。

The classic draft-model approach uses a smaller model of the same family (Llama 3.2 1B drafting for Llama 3.3 70B). It works but acceptance rate is mediocre — the smaller model distribution diverges from the target. EAGLE, then EAGLE-2, then EAGLE-3 train a light draft head directly on the target model's internal states, so the draft's distribution tracks the target much more closely. That is why alpha goes from 0.4 with draft-model to 0.6-0.8 with EAGLE-3.

> 经典的 draft 模型方法使用同系列的更小模型（Llama 3.2 1B 为 Llama 3.3 70B 做 draft）。它可行但接受率平庸——更小模型的分布偏离目标。EAGLE、EAGLE-2、EAGLE-3 直接在目标模型的内部状态上训练轻量 draft head，所以 draft 的分布更接近目标。这就是为什么 alpha 从 draft 模型的 0.4 提升到 EAGLE-3 的 0.6-0.8。

The catch: EAGLE-3 is opt-in in vLLM 2026. `speculative_config` must be set explicitly. No flag, no acceleration. Teams that flip it on without measuring alpha on their real traffic often see tail latency get worse, not better.

> 关键点：EAGLE-3 在 2026 年 vLLM 中是 opt-in 的。`speculative_config` 必须显式设置。没有标志，就没有加速。不测量真实流量 alpha 就开启的团队经常看到尾部延迟变差而非改善。

## The Concept | 核心概念

### What speculative decoding actually buys

> **【中文解读】** 推测解码的加速比公式为 `S = (1 + K*alpha) / (1 + verify_overhead)`。对于 K=5, alpha=0.7，理论加速 4.1x。但实际生产中通常只达到 2-3x，因为 alpha 在真实流量上很少达到 0.7 以上，且验证开销在高 batch size 时增大。

Without spec decode, per-token cost is one target forward. With spec decode at draft length K and acceptance alpha, expected tokens per target forward is `1 + K * alpha`. The speedup is `(1 + K * alpha) / (1 + epsilon)` where epsilon is draft-plus-verify overhead. For K=5, alpha=0.7: `(1 + 5*0.7) / (1 + 0.1) = 4.5 / 1.1 = 4.1x`. Real-world numbers cluster around 2-3x because alpha is rarely that high on production traffic and epsilon grows at high batch size.

> 没有推测解码时，每 token 成本是一次目标前向传播。有推测解码时，draft 长度 K 和接受率 alpha 下，每次目标前向的预期 token 数为 `1 + K * alpha`。加速比为 `(1 + K * alpha) / (1 + epsilon)`，其中 epsilon 是 draft + 验证开销。对于 K=5, alpha=0.7：`(1 + 5*0.7) / (1 + 0.1) = 4.5 / 1.1 = 4.1x`。实际数据集中在 2-3x，因为 alpha 在生产流量上很少那么高，且 epsilon 在高 batch size 时增大。

### Why alpha is the only metric that matters

Rejected tokens do not disappear — they force a second target forward for the first rejected token. On a workload where alpha drops to 0.4, you pay draft overhead plus verification plus re-roll. At high concurrency (say 256 concurrent), the decode batch is already large enough that the memory-bandwidth gap between "target alone" and "target with verify" shrinks. Below alpha 0.55 on most 2026 hardware, spec decode is net negative.

> 被拒绝的 token 不会消失——它们强制对第一个被拒绝的 token 进行第二次目标前向传播。在 alpha 降到 0.4 的工作负载上，你付出 draft 开销 + 验证 + 重新生成。在高并发（如 256 并发）下，解码批次已经足够大，"单独目标"和"带验证目标"之间的内存带宽差距缩小。在 2026 年大多数硬件上，alpha 低于 0.55 时推测解码是净负面的。

Alpha varies by workload. On ShareGPT-style general chat, EAGLE-3 trained on ShareGPT hits 0.6-0.8. On domain-specific traffic (code, medical, legal) the draft head trained on general data drops to 0.4-0.6. Training a domain-specific draft head recovers alpha — it is a light, quick training job compared to target finetuning.

> Alpha 因工作负载而异。在 ShareGPT 风格的通用聊天上，用 ShareGPT 训练的 EAGLE-3 达到 0.6-0.8。在领域特定流量（代码、医疗、法律）上，用通用数据训练的 draft head 降到 0.4-0.6。训练领域特定的 draft head 可以恢复 alpha——与目标微调相比，这是一个轻量、快速的训练任务。

### EAGLE generations at a glance

> **【中文解读】** 推测解码经历了三代演进：(1) Classic draft model（同一系列的小模型，alpha 0.3-0.5）——简单但接受率低；(2) EAGLE-1/2（在目标模型隐状态上训练 draft head，alpha 0.5-0.7）——更高接受率；(3) EAGLE-3（在多层隐状态上训练，alpha 0.6-0.8）——2025-2026 年的生产级方案。关键区别是 EAGLE 直接在目标模型的内部表示上训练 draft，而非在原始 token 上，因此分布更接近目标。

> **【拓展：推测解码 vs 其他加速技术】** LLM 推理加速技术对比：(1) 推测解码（EAGLE-3）——2-3x 加速，需要额外 draft head；(2) 量化（INT8/FP8）——推理加速 1.5-2x，有轻微质量损失；(3) 分块预填充——降低 ITL tail 但不直接提升吞吐；(4) 分离式 prefill/decode——消除资源浪费，30-40% 成本节省；(5) 自研芯片（Groq/Cerebras）——5-10x 解码速度但单价更高。这些技术可以叠加使用：EAGLE-3 + FP8 + 分离式部署的综合效果可达 10x+。

- **Classic draft model**: small model of same family. Alpha 0.3-0.5. Infrastructure simple — two models loaded, draft runs K forwards per target forward.
  中文翻译：**经典 draft 模型**：同系列的小模型。Alpha 0.3-0.5。基础设施简单——加载两个模型，draft 每次目标前向运行 K 次前向。
- **EAGLE-1 (2024)**: single draft head trained on target hidden states (last layer). Alpha ~0.5-0.6. Small param overhead on top of target.
  中文翻译：**EAGLE-1 (2024)**：在目标隐状态（最后一层）上训练的单 draft head。Alpha 约 0.5-0.6。目标之上的小参数开销。
- **EAGLE-2 (2025)**: adaptive draft length and tree-based drafts (verify multiple branches in one target pass). Alpha ~0.6-0.7. More complex draft scheduler.
  中文翻译：**EAGLE-2 (2025)**：自适应 draft 长度和基于树的 draft（一次目标前向验证多个分支）。Alpha 约 0.6-0.7。更复杂的 draft 调度器。
- **EAGLE-3 (2025-2026)**: draft head trained on multiple target layers (not just last), better alignment. Alpha ~0.6-0.8 on general chat.
  中文翻译：**EAGLE-3 (2025-2026)**：在多个目标层（不仅最后一层）上训练的 draft head，更好对齐。通用聊天上 Alpha 约 0.6-0.8。

### The 2026 production recipe

> **【中文解读】** 生产环境 EAGLE-3 部署的五步流程：(1) 先以基础模型上线，建立 TTFT/ITL/吞吐量基线；(2) 启用 EAGLE-3 draft 配置；(3) 监控接受率 alpha——vLLM V1 通过 `spec_decode_metrics.accepted_tokens_per_request` 暴露此指标；(4) 如果 alpha < 0.55，禁用推测解码或训练领域特定的 draft head；(5) 在生产并发水平重新测试，确认 P99 ITL 没有恶化。

1. Ship target model plain. Measure baseline TTFT, ITL, throughput at target concurrency.
   中文翻译：先以基础模型上线。在目标并发下测量基线 TTFT、ITL、吞吐量。
2. Enable EAGLE-3 draft via vLLM `speculative_config`. Re-run the benchmark.
   中文翻译：通过 vLLM `speculative_config` 启用 EAGLE-3 draft。重新运行基准测试。
3. Log acceptance rate alpha. vLLM V1 reports this as `spec_decode_metrics.accepted_tokens_per_request`. Divide by requested draft length to get alpha.
   中文翻译：记录接受率 alpha。vLLM V1 通过 `spec_decode_metrics.accepted_tokens_per_request` 报告。除以请求的 draft 长度得到 alpha。
4. If alpha < 0.55 on production traffic distribution, disable spec decode or train a domain-specific EAGLE-3 draft.
   中文翻译：如果生产流量分布上 alpha < 0.55，禁用推测解码或训练领域特定的 EAGLE-3 draft。
5. At production concurrency, re-run. Confirm P99 ITL did not get worse.
   中文翻译：在生产并发下重新测试。确认 P99 ITL 没有恶化。

### The production pitfall: P99 tail

Mean ITL drops with spec decode. P99 can get worse if you do not tune. Rejected drafts trigger a two-pass sequence (draft + verify-fail + reroll). Under full batch, those two passes serialize. Watch P99 ITL, not P50.

> 平均 ITL 随推测解码下降。如果不调优，P99 可能恶化。被拒绝的 draft 触发两次传递序列（draft + 验证失败 + 重新生成）。在满批次下，这两次传递串行化。关注 P99 ITL，而非 P50。

### Where EAGLE-3 is already deployed

Google deployed speculative decoding in AI Overviews in 2025 (same quality, faster response). vLLM V1 ships `speculative_config` as the documented interface; N-gram GPU speculative decoding in V1 is the variant compatible with chunked prefill. SGLang supports EAGLE-3 as the recommended draft path for prefix-heavy workloads.

> Google 在 2025 年将推测解码部署到 AI Overviews（相同质量，更快响应）。vLLM V1 将 `speculative_config` 作为文档化接口；V1 中的 N-gram GPU 推测解码是与分块预填充兼容的变体。SGLang 支持 EAGLE-3 作为前缀密集工作负载的推荐 draft 路径。

### Break-even math in one line

Expected speedup: `S(alpha, K) = (1 + K*alpha) / (1 + verify_overhead)`. Setting `S = 1` solves for alpha: `alpha_breakeven = verify_overhead / K`. For typical verify_overhead ~0.15 and K=5: `alpha_breakeven = 0.03`. But that is the raw decode math. At high concurrency the verify overhead rises and the decode batch already amortizes memory reads across sequences, so effective alpha_breakeven climbs to ~0.45-0.55 in practice.

> 预期加速比：`S(alpha, K) = (1 + K*alpha) / (1 + verify_overhead)`。设 `S = 1` 求解 alpha：`alpha_breakeven = verify_overhead / K`。典型 verify_overhead 约 0.15，K=5：`alpha_breakeven = 0.03`。但那是原始解码数学。在高并发下，验证开销增大，解码批次已经在序列间分摊内存读取，所以实际有效 alpha_breakeven 上升到约 0.45-0.55。

### When not to use speculative decoding

> **【拓展：推测解码的适用场景】** 推测解码在以下场景有效：(1) 实时对话（TTFT < 200ms 要求）——2-3x 加速显著改善用户体验；(2) 代码补全（实时性要求高）；(3) 低并发场景（< 50 concurrent）——内存带宽差距大，收益明显。在以下场景应避免：(1) 批量离线生成——延迟不重要，使用 plain target；(2) 短输出（< 50 tokens）——draft 开销和验证成本主导；(3) 专业领域（无领域训练的 draft head）——alpha 太低；(4) vLLM v0.18.0 + draft-model + chunked-prefill 的组合——不兼容。

> **【拓展：vLLM 推测解码配置】** vLLM V1 支持三种推测解码模式：(1) Draft model——传统小模型作为 draft，与 chunked-prefill 不兼容；(2) EAGLE——在隐状态上训练的 draft head，推荐用于通用场景；(3) N-gram GPU——基于 prompt 中 N-gram 查找的 GPU 端 draft，是唯一与 chunked-prefill 兼容的模式。`speculative_config` 必须显式设置，vLLM 默认不开启任何推测解码。

- Batch-1 offline generation where latency does not matter. Use plain target.
  中文翻译：延迟无关紧要的批量为 1 的离线生成。使用普通目标模型。
- Very short outputs (under 50 tokens). Draft overhead and verify cost dominate.
  中文翻译：非常短的输出（50 token 以下）。draft 开销和验证成本占主导。
- Specialized domains without a domain-trained draft head. Alpha too low.
  中文翻译：没有领域训练 draft head 的专业领域。Alpha 太低。
- vLLM v0.18.0 plus draft-model spec decode plus `--enable-chunked-prefill`. This combination does not compile. The documented exception is N-gram GPU spec decode in V1.
  中文翻译：vLLM v0.18.0 + draft-model 推测解码 + `--enable-chunked-prefill`。此组合无法编译。文档例外是 V1 中的 N-gram GPU 推测解码。

## Use It | 用框架实现

`code/main.py` simulates a decode loop with and without speculative decoding across a range of alpha values and draft lengths K. It prints the break-even alpha, measured speedup, and tail behavior. Run it on several (alpha, K) combinations to see exactly where speculative decoding stops paying.

> `code/main.py` 模拟有/无推测解码的解码循环，覆盖一系列 alpha 值和 draft 长度 K。它打印盈亏平衡 alpha、测量加速比和尾部行为。在多个 (alpha, K) 组合上运行，精确看到推测解码在哪里停止收益。

## Ship It | 产出物

This lesson produces `outputs/skill-eagle3-rollout.md`. Given a target model, traffic distribution description, and concurrency target, it produces a staged EAGLE-3 rollout plan — benchmark baseline, enable config, measure alpha, gate on alpha >= 0.55, watch P99 ITL.

> 本课产出 `outputs/skill-eagle3-rollout.md`。给定目标模型、流量分布描述和并发目标，它生成分阶段 EAGLE-3 推出计划——基准基线、启用配置、测量 alpha、以 alpha >= 0.55 作为门控、关注 P99 ITL。

## Exercises | 练习题

1. Run `code/main.py`. At K=5, what alpha do you need for a 2x speedup? For a 3x speedup? How sensitive is that to verify_overhead?
   中文翻译：运行 `code/main.py`。K=5 时，2x 加速需要多少 alpha？3x 加速呢？这对 verify_overhead 有多敏感？
2. Imagine production traffic splits 70% general chat, 30% code. General chat hits alpha 0.7 with EAGLE-3 trained on ShareGPT; code hits alpha 0.4. What is blended alpha and is spec decode net-positive?
   中文翻译：假设生产流量 70% 通用聊天，30% 代码。通用聊天 alpha 0.7，代码 alpha 0.4。混合 alpha 是多少，推测解码是否净正向？
3. Read the vLLM `speculative_config` documentation. Name the three modes (draft model, EAGLE, N-gram) and which one is compatible with chunked prefill.
   中文翻译：阅读 vLLM `speculative_config` 文档。说出三种模式（draft model、EAGLE、N-gram）及哪个与分块预填充兼容。
4. You see mean ITL drop 25% after enabling EAGLE-3 but P99 ITL went up 15%. Diagnose and propose a mitigation.
   中文翻译：启用 EAGLE-3 后平均 ITL 下降 25% 但 P99 ITL 上升 15%。诊断并提出缓解方案。
5. Compute the memory cost of the EAGLE-3 draft head for Llama 3.3 70B. How does it compare to running Llama 3.2 1B as a classic draft?
   中文翻译：计算 Llama 3.3 70B 的 EAGLE-3 draft head 内存成本。与运行 Llama 3.2 1B 作为经典 draft 相比如何？

## Key Terms | 术语速查表

| Term / 术语 | What people say / 通俗说法 | What it actually means / 实际含义 |
|------|----------------|------------------------|
| Speculative decoding | "draft plus verify" / "draft 加验证" | Propose K tokens with a cheap model, verify all K in one target forward / 用廉价模型提议 K 个 token，一次目标前向验证所有 K 个 |
| Acceptance rate alpha | "spec accept rate" / "推测接受率" | Fraction of draft tokens accepted by the target; the only metric that matters / 被 target 接受的 draft token 比例；唯一重要的指标 |
| Draft length K | "spec k" / "推测 K" | How many tokens the draft proposes per target forward; typical 4-8 / 每次 target 前向 draft 提议多少 token；通常 4-8 |
| Verify overhead epsilon | "spec overhead" / "推测开销" | Extra cost to verify-and-reroll vs a plain target forward; grows with batch / 验证+重新生成 vs 普通 target 前向的额外成本；随 batch 增长 |
| EAGLE-3 | "latest EAGLE" / "最新 EAGLE" | 2025-2026 variant; trains draft head on multiple target layers; alpha 0.6-0.8 / 2025-2026 变体；在多个 target 层上训练 draft head |
| `speculative_config` | "vLLM spec config" / "vLLM 推测配置" | The explicit opt-in in vLLM V1; no default means no acceleration / vLLM V1 中的显式 opt-in；无默认即无加速 |
| N-gram spec decode | "N-gram draft" / "N-gram draft" | GPU-side draft using N-gram lookups in the prompt; chunked-prefill-compatible / GPU 端使用 prompt 中 N-gram 查找的 draft；与分块预填充兼容 |
| Break-even alpha | "no-op alpha" / "无效果 alpha" | Alpha at which spec decode gives zero speedup; watch this at production concurrency / 推测解码零加速的 alpha；在生产并发下关注 |
| Rejected-draft two-pass | "reroll cost" / "重新生成成本" | Two target forwards when drafts reject; drives P99 tail / draft 被拒绝时的两次 target 前向；驱动 P99 尾部 |

## Further Reading | 延伸阅读

- [vLLM — Speculative Decoding docs](https://docs.vllm.ai/en/latest/features/spec_decode/) — authoritative source on `speculative_config` and chunked-prefill compatibility in V1.
- [vLLM Speculative Config API](https://docs.vllm.ai/en/latest/api/vllm/config/speculative/) — the exact field set.
- [EAGLE paper (arXiv:2401.15077)](https://arxiv.org/abs/2401.15077) — original EAGLE draft-head formulation.
- [EAGLE-2 paper (arXiv:2406.16858)](https://arxiv.org/abs/2406.16858) — adaptive drafts and trees.
- [UC Berkeley EECS-2025-224](https://www2.eecs.berkeley.edu/Pubs/TechRpts/2025/EECS-2025-224.html) — efficient LLM system with speculative decoding.
- [BentoML — Speculative Decoding](https://bentoml.com/llm/inference-optimization/speculative-decoding) — production rollout checklist.
