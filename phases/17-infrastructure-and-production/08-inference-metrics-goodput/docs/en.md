# Inference Metrics — TTFT, TPOT, ITL, Goodput, P99 | 推理 指标 Goodput

> Four metrics decide whether an inference deployment is working. TTFT is prefill plus queue plus network. TPOT (equivalently ITL) is the memory-bound decode cost per token. End-to-end latency is TTFT plus TPOT times output length. Throughput is tokens per second aggregated across the fleet. But the one that matters for product is goodput — the fraction of requests that met every SLO simultaneously. High throughput at low goodput means you are processing tokens that never reach users on time. Reference numbers for Llama-3.1-8B-Instruct on TRT-LLM in 2026: mean TTFT 162 ms, mean TPOT 7.33 ms, mean E2E 1,093 ms. Always report P50, P90, P99 — never just mean. And watch the measurement trap: GenAI-Perf excludes TTFT from ITL calculation, LLMPerf includes it; two tools disagree on TPOT for the same run.

> **【中文解读】** 本节介绍了推理指标和 Goodput——衡量 LLM 推理服务质量的关键指标体系。


**Type:** Learn | **类型:** 学习
**Languages:** Python (stdlib, toy percentile calculator and goodput reporter) | **语言:** Python（标准库，百分位计算器和 Goodput 报告器）
**Prerequisites:** Phase 17 · 04 (vLLM Serving Internals) | **前置知识:** Phase 17 · 04（vLLM 服务内部）
**Time:** ~60 minutes | **时间:** ~60 分钟

## Learning Objectives | 学习目标

- Define TTFT, TPOT, ITL, E2E, throughput, and goodput precisely and name the component each one measures.
  中文翻译：精确定义 TTFT、TPOT、ITL、E2E、吞吐量和 Goodput，并说出每个指标测量的组件。
- Explain why mean is the wrong statistic for LLM serving and how to read P50/P90/P99.
  中文翻译：解释为什么均值是 LLM 服务的错误统计量，以及如何阅读 P50/P90/P99。
- Construct an SLO multi-constraint (e.g. TTFT<500 ms AND TPOT<15 ms AND E2E<2 s) and compute goodput against it.
  中文翻译：构造 SLO 多约束（如 TTFT<500ms 且 TPOT<15ms 且 E2E<2s）并据此计算 Goodput。
- Name two benchmark tools that disagree on TPOT for the same run and explain why.
  中文翻译：说出两个在同一运行中对 TPOT 产生不同结果的基准测试工具并解释原因。

## The Problem | 问题引入

> **【中文解读】** 推理服务有多个延迟轴，每个轴以不同方式失败。Prefill 是计算受限的，随提示长度增长；Decode 是内存受限的，随 batch size 增长；排队延迟是运维问题；网络是物理距离问题。需要不同的指标来衡量每个维度，需要百分位数，还需要一个综合指标说"用户是否得到了期望的体验"——这就是 Goodput。

> **【拓展：LLM 推理指标体系】** 2026 年 LLM 推理的完整指标体系包括：(1) TTFT（首 token 延迟）——用户感知到的首次响应时间；(2) TPOT/ITL（每 token 延迟/inter-token 延迟）——流式输出的平滑度；(3) E2E（端到端延迟）——从请求到完成的总时间；(4) Throughput（吞吐量）——集群效率指标；(5) Goodput（有效吞吐）——同时满足所有 SLA 的请求比例。MLPerf Inference v6.0 已将 Goodput 作为官方提交指标。

"Our throughput is 15,000 tokens per second." So what? If 40% of requests blew past 2 seconds end-to-end, users abandoned the session. Throughput alone does not tell you whether the product works.

> "我们的吞吐量是每秒 15,000 个 token。"那又怎样？如果 40% 的请求端到端超过 2 秒，用户会放弃会话。仅吞吐量不能告诉你产品是否正常工作。

Inference has multiple axes of latency and each one fails differently. Prefill is compute-bound and scales with prompt length. Decode is memory-bound and scales with batch size. Queuing delay is an operational problem. Network is a physical-distance problem. You need distinct metrics for each, and you need percentiles, and you need a single composite that says "did the user get what they expected" — that is goodput.

> 推理有多个延迟轴，每个轴以不同方式失败。预填充是计算受限的，随提示长度增长。解码是内存受限的，随批次大小增长。排队延迟是运维问题。网络是物理距离问题。你需要为每个维度不同的指标，需要百分位数，还需要一个综合指标说"用户是否得到了期望的体验"——这就是 Goodput。

## The Concept | 核心概念

### TTFT — time to first token

> **【中文解读】** TTFT = queue_time + network_request + prefill_time。Prefill 在长提示时占主导——32K prompt 在 Llama 3.3 70B FP8 H100 上需要约 800ms 的纯 prefill。排队时间是负载下的调度器行为，网络请求包括 TLS 的线缆时间。TTFT 是用户在流式返回任何内容之前感知到的延迟。

`TTFT = queue_time + network_request + prefill_time`

Prefill dominates when prompts are long. On Llama-3.3-70B FP8 on H100, a 32k prompt takes ~800 ms of pure prefill. Queue time is scheduler behavior under load. Network request is wire time including TLS. TTFT is the latency the user sees before anything streams back.

> 预填充在长提示时占主导。Llama-3.3-70B FP8 在 H100 上，32K 提示需要约 800ms 的纯预填充。排队时间是负载下的调度器行为。网络请求是包括 TLS 的线缆时间。TTFT 是用户在任何内容流式返回前感知到的延迟。

### TPOT / ITL — inter-token latency

> **【中文解读】** TPOT（time per output token）= ITL（inter-token latency）= decode latency per token。公式：TPOT = (decode_forward_time + scheduler_overhead) / tokens_produced。在 Llama 3.3 70B H100 + 分块预填充下，TPOT 均值约 7ms；无分块预填充时，在长 prefill 邻居序列期间 TPOT 可飙升至 50ms。永远监控 P99 而非均值。

Many names for one quantity. `TPOT` (time per output token), `ITL` (inter-token latency), `decode latency per token` — all the same. It is the time between consecutive streamed tokens after the first.

> 一个量的多个名称。`TPOT`（每输出 token 时间）、`ITL`（inter-token 延迟）、`每 token 解码延迟`——都是同一个。它是第一个 token 之后连续流式 token 之间的时间。

`TPOT = (decode_forward_time + scheduler_overhead) / tokens_produced`

On the same Llama-3.3-70B H100 stack with chunked prefill, TPOT mean ~7 ms. Without chunked prefill, during a long prefill on a neighboring sequence, TPOT can spike to 50 ms. Watch P99, not mean.

> 在相同的 Llama-3.3-70B H100 栈上加 分块预填充，TPOT 均值约 7ms。无分块预填充时，在邻居序列的长预填充期间，TPOT 可能飙升至 50ms。关注 P99，不是均值。

### E2E latency

`E2E = TTFT + TPOT * output_tokens + network_response`

For long outputs (>500 tokens), E2E is TPOT-dominated. For short outputs with long prompts, E2E is TTFT-dominated. Report output-length-conditioned E2E.

> 对于长输出（>500 token），E2E 由 TPOT 主导。对于长提示的短输出，E2E 由 TTFT 主导。报告按输出长度分条件的 E2E。

### Throughput

`throughput = total_output_tokens / elapsed_time`

Aggregate metric. Tells you fleet efficiency. Does not tell you individual-request health.

> 聚合指标。告诉你集群效率。不告诉你单个请求的健康状况。

### Goodput — the metric you actually care about

> **【中文解读】** Goodput 是唯一真正重要的综合指标。SLO 是多约束的——一个请求只有同时满足 TTFT <= a、TPOT <= b、E2E <= c 才算"好"。高吞吐量在 60% Goodput 时是失败；低吞吐量在 99% Goodput 时才是目标。2026 年 MLPerf Inference v6.0 和 AI 平台提供商的内部 SLA 追踪都以 Goodput 为核心指标。

`goodput = fraction of requests meeting (TTFT <= a) AND (TPOT <= b) AND (E2E <= c)`

The SLO is a multi-constraint. A request is "good" only if every constraint held. Goodput is the share. High throughput at 60% goodput is failure. Lower throughput at 99% goodput is the target.

> SLO 是多约束的。只有当所有约束都满足时，请求才是"好"的。Goodput 是这个份额。60% Goodput 的高吞吐量是失败。99% Goodput 的较低吞吐量才是目标。

In 2026, goodput is the metric used in MLPerf Inference v6.0 submissions and in internal SLA tracking at AI platform providers.

> 2026 年，Goodput 是 MLPerf Inference v6.0 提交和 AI 平台提供商内部 SLA 追踪使用的指标。

### Why mean is the wrong statistic

> **【中文解读】** LLM 延迟分布是右偏的。一个包含长 prefill 邻居的 decode batch 可能发出 500 个 TPOT ~7ms 的 token 和 20 个 TPOT ~60ms 的 token。均值 TPOT 是 9ms，但 P99 TPOT 是 65ms。用户经常遇到 P99——这就是他们离开的原因。永远报告三元组（P50, P90, P99），对于用户体验，P99 是需要优化的目标。

LLM latency distributions are right-skewed. A decode batch with one long-prefill neighbor can ship 500 tokens with TPOT ~7 ms and 20 tokens with TPOT ~60 ms. Mean TPOT is 9 ms. P99 TPOT is 65 ms. Users hit the P99 regularly — that is why they leave.

> LLM 延迟分布是右偏的。一个包含长预填充邻居的解码批次可以发出 500 个 TPOT 约 7ms 的 token 和 20 个 TPOT 约 60ms 的 token。均值 TPOT 是 9ms。P99 TPOT 是 65ms。用户经常遇到 P99——这就是他们离开的原因。

Always report the triple (P50, P90, P99). For user experience, P99 is the one you optimize.

> 始终报告三元组（P50、P90、P99）。对于用户体验，P99 是你需要优化的。

### Reference numbers — Llama-3.1-8B-Instruct on TRT-LLM, 2026

- mean TTFT: 162 ms
  中文翻译：均值 TTFT：162ms
- mean TPOT: 7.33 ms
  中文翻译：均值 TPOT：7.33ms
- mean E2E: 1,093 ms
  中文翻译：均值 E2E：1,093ms
- P99 TPOT: varies 10-25 ms depending on chunked-prefill configuration.
  中文翻译：P99 TPOT：10-25ms，取决于分块预填充配置。

These are the published NVIDIA reference points. They change with model size (70B would show 3-5x), hardware (H100 vs B200 ~3x), and load.

> 这些是 NVIDIA 发布的参考数据。它们随模型大小（70B 会显示 3-5 倍）、硬件（H100 vs B200 约 3 倍）和负载变化。

### The measurement trap

> **【中文解读】** 2026 年最常用的两个基准测试工具在 TPOT 上产生不同结果：NVIDIA GenAI-Perf 将 TTFT 从 ITL 计算中排除（从 token 2 开始），LLMPerf 包含 TTFT（从 token 1 开始）。同一个请求（TTFT 500ms、100 输出 token、700ms decode），GenAI-Perf 报告 ITL=7.07ms，LLMPerf 报告 ITL=12.00ms。永远说明使用哪个工具，永远发布定义。

> **【拓展：LLM 基准测试工具生态】** 2026 年 LLM 推理基准测试工具包括：(1) NVIDIA GenAI-Perf——Triton 客户端，全面指标覆盖，ITL 不含 TTFT；(2) LLMPerf（Anyscale）——Rust-backed 分词，流式感知，含 TTFT 的 ITL；(3) LLM-Locust（TrueFoundry）——Locust 扩展，修复了 GIL 问题；(4) guidellm——大规模合成基准测试；(5) k6 v2026.1.0——流式感知，Kubernetes-native。选择工具时要了解其 ITL 定义差异。

Two of the most-used 2026 benchmark tools disagree on TPOT for the same run:

- **NVIDIA GenAI-Perf**: excludes TTFT from the ITL calculation. ITL starts from token 2.
  中文翻译：**NVIDIA GenAI-Perf**：从 ITL 计算中排除 TTFT。ITL 从第 2 个 token 开始。
- **LLMPerf**: includes TTFT. ITL starts from token 1.
  中文翻译：**LLMPerf**：包含 TTFT。ITL 从第 1 个 token 开始。

For a request with TTFT 500 ms and 100 output tokens in 700 ms total decode, GenAI-Perf reports `ITL = 700/99 = 7.07 ms`, LLMPerf reports `ITL = 1200/100 = 12.00 ms`. Tool choice changes the number.

> 对于一个 TTFT 500ms、100 输出 token、700ms 总解码的请求，GenAI-Perf 报告 `ITL = 700/99 = 7.07ms`，LLMPerf 报告 `ITL = 1200/100 = 12.00ms`。工具选择改变数字。

Always state which tool. Always publish the definition.

> 始终说明使用哪个工具。始终发布定义。

### Constructing an SLO

> **【拓展：LLM SLO 设定参考】** 2026 年推荐的消费级 70B 对话模型 SLO：TTFT P99 <= 800ms、TPOT P99 <= 25ms、E2E P99 <= 3s（<300 token 输出）、Goodput >= 99%。企业级 SLO 收紧 TTFT（200-400ms）但放宽 E2E。测量方法：使用真实流量或 LLMPerf 合成流量（`--mean-input-tokens 800 --stddev-input-tokens 300 --mean-output-tokens 150`），目标 2x 峰值并发，运行 30-50 次迭代取百分位数。

A reasonable consumer-facing SLO for a 70B chat model in 2026:

- TTFT P99 <= 800 ms.
  中文翻译：TTFT P99 <= 800ms。
- TPOT P99 <= 25 ms.
  中文翻译：TPOT P99 <= 25ms。
- E2E P99 <= 3 s for <300-token outputs.
  中文翻译：E2E P99 <= 3s（<300 token 输出）。
- Goodput target >= 99%.
  中文翻译：Goodput 目标 >= 99%。

Enterprise SLOs tighten TTFT (200-400 ms) and loosen E2E. The point is to write them down, measure all three, and track goodput as a single composite.

> 企业级 SLO 收紧 TTFT（200-400ms）并放宽 E2E。关键是要写下来、测量全部三个、并将 Goodput 作为单一综合指标追踪。

### How to measure

- Run real traffic or realistic synthetic (LLMPerf with `--mean-input-tokens 800 --stddev-input-tokens 300 --mean-output-tokens 150`).
  中文翻译：运行真实流量或逼真合成流量（LLMPerf 使用 `--mean-input-tokens 800 --stddev-input-tokens 300 --mean-output-tokens 150`）。
- Target 2x peak concurrency for the benchmark run.
  中文翻译：基准测试运行目标为 2 倍峰值并发。
- Run 30-50 iterations, take percentiles of the combined sample.
  中文翻译：运行 30-50 次迭代，取合并样本的百分位数。
- Publish with tool name, tool version, model, hardware, concurrency, prompt distribution.
  中文翻译：发布时标注工具名、版本、模型、硬件、并发数、提示分布。

## Use It | 用框架实现

`code/main.py` is a toy goodput calculator. Generate a synthetic latency distribution, apply an SLO, and compute goodput. Also shows the GenAI-Perf vs LLMPerf TPOT difference on the same trace.

> `code/main.py` 是一个模拟 Goodput 计算器。生成合成延迟分布，应用 SLO，计算 Goodput。还展示相同 trace 上 GenAI-Perf vs LLMPerf 的 TPOT 差异。

## Ship It | 产出物

> **【拓展：SLO 设定与 Goodput 门控】** 2026 年推荐的 70B 对话模型 SLO：TTFT P99 <= 800ms、TPOT P99 <= 25ms、E2E P99 <= 3s（<300 token 输出）、Goodput 目标 >= 99%。企业级 SLO 收紧 TTFT（200-400ms）但放宽 E2E。关键实践：(1) 在 CI/CD 中 gate 部署决策于 Goodput 而非吞吐量；(2) 用 2x 峰值并发运行基准测试；(3) 运行 30-50 次迭代取百分位数；(4) 发布时标注工具名、版本、模型、硬件、并发数、提示分布。

This lesson produces `outputs/skill-slo-goodput-gate.md`. Given a workload and SLO, it produces a CI/CD-ready benchmark recipe that gates deploys on goodput rather than throughput.

> 本课产出 `outputs/skill-slo-goodput-gate.md`。给定工作负载和 SLO，它生成一个 CI/CD 就绪的基准测试方案，以 Goodput 而非吞吐量作为部署门控。

## Exercises | 练习题

1. Run `code/main.py`. Generate a distribution with 1% tail spike. How does goodput change when you tighten P99 TPOT from 30 ms to 15 ms?
   中文翻译：运行 `code/main.py`。生成带有 1% 尾部尖刺的分布。当 P99 TPOT 从 30ms 收紧到 15ms 时 Goodput 如何变化？
2. A vendor quotes "15,000 tok/s on Llama 3.3 70B H100". Name three questions to ask before trusting it.
   中文翻译：供应商报价"Llama 3.3 70B H100 上 15,000 tok/s"。在信任之前说出三个要问的问题。
3. Why does chunked prefill protect P99 TPOT but not mean TPOT?
   中文翻译：为什么分块预填充保护 P99 TPOT 但不保护均值 TPOT？
4. Construct a consumer SLO for a voice assistant (first token is heard, not read). Which metric is most user-visible?
   中文翻译：为语音助手构建消费级 SLO（首 token 是听到而非读到）。哪个指标对用户最可见？
5. Read the LLMPerf README and the GenAI-Perf docs. Identify three other metrics where the tools disagree.
   中文翻译：阅读 LLMPerf README 和 GenAI-Perf 文档。找出工具在另外三个指标上的分歧。

## Key Terms | 术语速查表

| Term / 术语 | What people say / 通俗说法 | What it actually means / 实际含义 |
|------|----------------|------------------------|
| TTFT | "time to first token" / "首 token 时间" | Queue + network + prefill; dominated by prefill at long prompts / 队列+网络+预填充；长提示时由预填充主导 |
| TPOT | "time per output token" / "每输出 token 时间" | Memory-bound decode cost per token after first / 首个 token 后每 token 的内存受限解码成本 |
| ITL | "inter-token latency" / "inter-token 延迟" | Same as TPOT in most tools (not all — see GenAI-Perf) / 大多数工具中同 TPOT（非所有——见 GenAI-Perf） |
| E2E | "end to end" / "端到端" | TTFT + TPOT * output_len; response-side network on top / TTFT + TPOT * 输出长度；加上响应端网络 |
| Throughput | "tok/s" / "token 每秒" | Fleet efficiency; useless without latency percentiles / 集群效率；无延迟百分位数则无意义 |
| Goodput | "SLO-met rate" / "SLO 达标率" | Fraction of requests meeting every SLO constraint simultaneously / 同时满足所有 SLO 约束的请求比例 |
| P99 | "tail" / "尾部" | 1-in-100 worst-case latency; the user experience metric / 百分之一最差延迟；用户体验指标 |
| SLO multi-constraint | "the joint" / "联合约束" | AND of all three latency bounds; a request fails if any one is violated / 三个延迟界限的 AND；任一违反即失败 |
| GenAI-Perf vs LLMPerf | "the tool trap" / "工具陷阱" | Tools disagree on whether ITL includes TTFT / 工具在 ITL 是否包含 TTFT 上不一致 |

## Further Reading | 延伸阅读

- [NVIDIA NIM — LLM Benchmarking Metrics](https://docs.nvidia.com/nim/benchmarking/llm/latest/metrics.html) — canonical definition of TTFT, ITL, TPOT.
- [Anyscale — LLM Serving Benchmarking Metrics](https://docs.anyscale.com/llm/serving/benchmarking/metrics) — alternative definitions and measurement recipe.
- [BentoML — LLM Inference Metrics](https://bentoml.com/llm/inference-optimization/llm-inference-metrics) — applied measurement on real deployments.
- [LLMPerf](https://github.com/ray-project/llmperf) — Ray-based open-source benchmark.
- [GenAI-Perf](https://docs.nvidia.com/deeplearning/triton-inference-server/user-guide/docs/client/src/c++/perf_analyzer/genai-perf/README.html) — NVIDIA's benchmark tool.
- [MLPerf Inference](https://mlcommons.org/benchmarks/inference-datacenter/) — the industry-accepted goodput-based benchmark.
