# Capstone 07 — End-to-End Fine-Tuning Pipeline (Data to SFT to DPO to Serve) | 微调 结业 流水线 SFT DPO

> An 8B model trained on your own data, DPO-aligned on your own preferences, quantized, speculative-decoded, and served at measurable $/1M tokens. The 2026 open stack is Axolotl v0.8, TRL 0.15, Unsloth for iteration, GPTQ/AWQ/GGUF for quantization, vLLM 0.7 with EAGLE-3 for serving. The capstone is to run the whole pipeline reproducibly — YAML in, served endpoint out — and publish a model card under the 2026 Model Openness Framework.

> **【中文解读】** 本节是综合项目——构建端到端微调流水线，从数据准备到模型评估。


**Type:** Capstone | **类型:** 综合项目
**Languages:** Python (pipeline), YAML (configs), Bash (scripts) | **语言:** Python（管道）, YAML（配置）, Bash（脚本）
**Prerequisites:** Phase 2 (ML), Phase 3 (DL), Phase 7 (transformers), Phase 10 (LLMs from scratch), Phase 11 (LLM engineering), Phase 17 (infrastructure), Phase 18 (safety)

> 🔗 **【前置】** 顶点项目 07 = 综合几乎全部 Phase。端到端微调流水线：data→SFT→DPO→serve。
> 💡 **【类比】** 微调流水线 = "AI 训练厨房"。2026 开源栈：Axolotl v0.8（配置）+ TRL 0.15（训练）+ Unsloth（迭代加速）+ GPTQ/AWQ/GGUF（量化）+ vLLM 0.7+EAGLE-3（服务）。目标：8B 模型在自有数据上 SFT+DPO+量化+投机解码+可测 $/1M tokens，YAML 输入→服务端点输出，附 2026 Model Openness Framework 模型卡。| **前置知识:** Phase 2（ML）, Phase 3（DL）, Phase 7（Transformer）, Phase 10（从头构建 LLM）, Phase 11（LLM 工程）, Phase 17（基础设施）, Phase 18（安全）
**Phases exercised:** P2 · P3 · P7 · P10 · P11 · P17 · P18 | **涉及阶段:** P2 · P3 · P7 · P10 · P11 · P17 · P18
**Time:** 35 hours | **时间:** 35 小时

## Problem | 问题引入

> **【中文解读】** 本节描述端到端微调流水线的核心挑战。2026 年每个认真的 AI 团队都维护着一条微调流水线，不是为了训练前沿模型，而是为了下游适配——领域 SFT、DPO 偏好对齐、蒸馏草稿模型用于投机解码、EAGLE-3 推理加速。工具链已成熟（Axolotl v0.8 + TRL 0.15 + Unsloth + vLLM 0.7），真正的工艺在 YAML 配置、数据卫生和评估纪律。

> **【拓展：微调工具链生态】** 2026 年微调工具栈：Axolotl v0.8（多 GPU SFT 配置驱动）、TRL 0.15（DPO/GRPO/RLHF）、Unsloth（单 GPU 快速迭代，2-5x 加速）。量化选择：GPTQ（Marlin 后端，推理最快）、AWQ（精度保持好）、GGUF（llama.cpp 兼容，CPU 推理友好）。服务端 vLLM 0.7 配合 EAGLE-3 投机解码可达 2-3x 吞吐提升，acceptance rate 通常在 0.65-0.80。8B 模型在 8xH100 上 SFT 约 6 小时，DPO 约 1.5 小时。

Every serious AI team in 2026 keeps a fine-tuning pipeline on tap. Not because they ship a frontier base model, but because downstream adaptation — domain SFT, DPO against labeled preferences, distilled drafts for speculative decoding, serving with EAGLE-3 — is where the measurable wins live. Axolotl v0.8 handles multi-GPU SFT configs. TRL 0.15 handles DPO and GRPO. Unsloth gets you fast single-GPU iteration. vLLM 0.7 with EAGLE-3 pushes decode throughput 2-3x without quality loss. The tooling works; the craft is in the YAMLs, the data hygiene, and the eval discipline.

> 2026 年每个认真的 AI 团队都保持一条随时可用的微调管道。不是因为它们发布前沿基础模型，而是因为下游适配——领域 SFT、针对标注偏好的 DPO、用于投机解码的蒸馏草稿、用 EAGLE-3 服务——是可衡量收益所在。Axolotl v0.8 处理多 GPU SFT 配置。TRL 0.15 处理 DPO 和 GRPO。Unsloth 让你快速进行单 GPU 迭代。vLLM 0.7 配合 EAGLE-3 在不损失质量的情况下将解码吞吐量推高 2-3 倍。工具链有效；工艺在于 YAML 配置、数据卫生和评估纪律。

You will run an 8B base (Llama 3.3, Qwen3, or Gemma 3) through SFT then DPO on task-specific data, quantize for serving, and measure gains against lm-evaluation-harness, RewardBench-2, MT-Bench-v2, and MMLU-Pro. You will produce a model card under the 2026 Model Openness Framework. The point is reproducibility — one command reruns the whole pipeline end to end.

> 你将在任务特定数据上对 8B 基础模型（Llama 3.3、Qwen3 或 Gemma 3）运行 SFT 然后 DPO，量化用于服务，并对照 lm-evaluation-harness、RewardBench-2、MT-Bench-v2 和 MMLU-Pro 测量收益。你将在 2026 Model Openness Framework 下生成模型卡。重点是可复现性——一条命令端到端重跑整个管道。

## Concept | 核心概念

> **【中文解读】** 流水线分五个阶段：数据（去重/质量过滤/PII 脱敏/污染检查）→ SFT（Axolotl YAML, ZeRO-3, 8xH100, 余弦调度, 2-3 轮）→ DPO/GRPO（TRL, 偏好对, beta 调参）→ 量化（GPTQ+AWQ+GGUF 三种格式）→ 服务（vLLM 0.7 + EAGLE-3, K8s 部署）。交付物是消融实验对比表：SFT-only vs SFT+DPO vs SFT+GRPO，以及服务指标和安全性评估。

> **【拓展：GRPO 与 DPO 对比】** DPO（Direct Preference Optimization）直接在偏好对上训练，简单高效，但需要人工标注。GRPO（Group Relative Policy Optimization）来自 DeepSeek R1，使用可验证奖励（数学/代码的正确性）做 RL 训练，不需要人工偏好标注。实测中，DPO 在对话质量上略优，GRPO 在数学/代码推理上更强。beta 参数（KL 散度权重）是关键超参，通常 0.05-0.15 之间。

The pipeline has five stages. **Data**: dedup (MinHash / Datatrove), quality filter (Nemotron-CC style classifier), PII scrub, split-hygiene check against public benchmark contamination. **SFT**: Axolotl YAML, ZeRO-3 on 8xH100, cosine schedule, packed sequences, 2-3 epochs. **DPO or GRPO**: TRL config, 1 epoch, preference pairs either human-labeled or model-judged, beta tuning. **Quantize**: GPTQ + AWQ + GGUF for deployment flexibility. **Serve**: vLLM 0.7 with EAGLE-3 speculative heads (or SGLang with SpecForge), K8s deployment, HPA on queue-wait.

> 管道有五个阶段。**数据**：去重（MinHash/Datatrove）、质量过滤（Nemotron-CC 风格分类器）、PII 清洗、针对公共基准污染的分割卫生检查。**SFT**：Axolotl YAML，8xH100 上的 ZeRO-3，余弦调度，打包序列，2-3 轮。**DPO 或 GRPO**：TRL 配置，1 轮，偏好对由人工标注或模型评判，beta 调参。**量化**：GPTQ + AWQ + GGUF 用于部署灵活性。**服务**：带 EAGLE-3 投机头的 vLLM 0.7（或带 SpecForge 的 SGLang），K8s 部署，基于 queue-wait 的 HPA。

Ablations are the deliverable: SFT-only vs SFT+DPO vs SFT+GRPO on three task-specific benchmarks. Serving metrics: tokens/s at batch 1 / 8 / 32, EAGLE-3 acceptance rate, $/1M tokens. Safety eval: Llama Guard 4 pass rate. Model card: bias evaluations, reproducibility seeds, data licensing.

> 消融实验是交付物：三个任务特定基准上的 SFT-only vs SFT+DPO vs SFT+GRPO。服务指标：批量 1/8/32 时的 tokens/s、EAGLE-3 接受率、$/1M tokens。安全评估：Llama Guard 4 通过率。模型卡：偏见评估、可复现性种子、数据许可。

## Architecture | 架构

```
raw data (HF datasets + internal)
    |
    v
Datatrove dedup + Nemotron-CC quality filter + PII scrub
    |
    v
split hygiene (MMLU-Pro contamination check)
    |
    v
Axolotl SFT config (YAML)  ---> 8xH100, ZeRO-3
    |
    v
TRL DPO / GRPO config       ---> 4xH100, 1 epoch
    |
    v
GPTQ + AWQ + GGUF quantize
    |
    v
vLLM 0.7 + EAGLE-3 speculative decoding
    |
    v
K8s deployment, HPA on queue-wait
    |
    v
lm-eval-harness + RewardBench-2 + MT-Bench-v2 + MMLU-Pro
    |
    v
model card (2026 MOF) + safety eval (Llama Guard 4)
```

## Stack | 技术栈

- Data: Datatrove for dedup, Nemotron-CC classifier for quality, Presidio for PII
  中文翻译：Data: Datatrove for dedup, Nemotron-CC classifier for quality, Presidio for PII
- Base: Llama 3.3 8B, Qwen3 14B, or Gemma 3 12B
  中文翻译：Base: Llama 3.3 8B, Qwen3 14B, or Gemma 3 12B
- SFT: Axolotl v0.8 with ZeRO-3, Flash Attention 3, packed sequences
  中文翻译：SFT: Axolotl v0.8 with ZeRO-3, Flash Attention 3, packed sequences
- Preference tuning: TRL 0.15 for DPO or GRPO; Unsloth for single-GPU iteration
  中文翻译：Preference tuning: TRL 0.15 for DPO or GRPO; Unsloth for single-GPU iteration
- Quantization: GPTQ (Marlin), AWQ, GGUF via llama.cpp
  中文翻译：Quantization: GPTQ (Marlin), AWQ, GGUF via llama.cpp
- Serving: vLLM 0.7 with EAGLE-3 speculative decoding (or SGLang 0.4 + SpecForge)
  中文翻译：Serving: vLLM 0.7 with EAGLE-3 speculative decoding (or SGLang 0.4 + SpecForge)
- Eval: lm-evaluation-harness, RewardBench-2, MT-Bench-v2, MMLU-Pro
  中文翻译：Eval: lm-evaluation-harness, RewardBench-2, MT-Bench-v2, MMLU-Pro

> 中文翻译：Eval: lm-evaluation-harness, RewardBench-2, MT-Bench-v2, MMLU-Pro（翻译）

- Safety eval: Llama Guard 4, ShieldGemma-2
  中文翻译：Safety eval: Llama Guard 4, ShieldGemma-2
- Infrastructure: Kubernetes + NVIDIA device plugin, HPA on queue-wait metric
  中文翻译：Infrastructure: Kubernetes + NVIDIA device plugin, HPA on queue-wait metric
- Observability: W&B for training, Langfuse for inference
  中文翻译：Observability: W&B for training, Langfuse for inference

## Build It | 动手构建

> **【中文解读】** 构建 8 个阶段：数据管道（Datatrove 去重 + 质量分类 + PII 清洗）、污染检查（MinHash 对比基准测试集）、Axolotl SFT（ZeRO-3 + FA3 + 序列打包）、TRL DPO/GRPO 偏好对齐、GPTQ/AWQ/GGUF 三种量化、vLLM 投机解码推理、完整评估（SWE-bench/HumanEval+/GPQA）和成本分析。

> **【拓展：端到端微调在 LLM 公司中的标准化流程】** Meta 的 LLaMA 微调流程、Mistral 的模型工厂、Cohere 的 Command 系列都遵循相同的阶段：预训练 -> SFT -> DPO/RLHF -> 量化 -> 部署。2026 年的标准化工具链：Axolotl 或 LLaMA-Factory（训练配置）、TRL（对齐）、AutoGPTQ/AutoAWQ（量化）、vLLM 或 TensorRT-LLM（推理）。关键指标：$/1M tokens vs 商业 API 价格。

1. **Data pipeline.** Run Datatrove dedup on raw corpus. Apply Nemotron-CC-style quality classifier. Presidio scrubs PII. Write train/val splits with explicit seed.
   中文翻译：1. **Data pipeline.** Run Datatrove dedup on raw corpus. Apply Nemotron-CC-style quality classifier. Presidio scrubs PII. Write train/val splits with explicit seed.

2. **Contamination check.** For every validation split, compute MinHash against MMLU-Pro, MT-Bench-v2, RewardBench-2 test sets. Reject any overlap.
   中文翻译：2. **Contamination check.** For every validation split, compute MinHash against MMLU-Pro, MT-Bench-v2, RewardBench-2 test sets. Reject any overlap.

3. **Axolotl SFT.** YAML with ZeRO-3, FA3, sequence packing. 2-3 epochs on 8xH100. Log to W&B.
   中文翻译：3. **Axolotl SFT.** YAML with ZeRO-3, FA3, sequence packing. 2-3 epochs on 8xH100. Log to W&B.

> 中文翻译：3. **Axolotl SFT.** YAML with ZeRO-3, FA3, sequence packing. 2-3 epochs on 8xH100. Log to W&B.（翻译）


4. **TRL DPO / GRPO.** Take the SFT checkpoint, run one epoch of DPO on preference pairs (or GRPO with a verifiable reward on math/code). Sweep beta.
   中文翻译：4. **TRL DPO / GRPO.** Take the SFT checkpoint, run one epoch of DPO on preference pairs (or GRPO with a verifiable reward on math/code). Sweep beta.

5. **Quantize.** Produce three quants: GPTQ-INT4-Marlin, AWQ-INT4, GGUF-Q4_K_M for llama.cpp. Record size and nominal throughput.
   中文翻译：5. **Quantize.** Produce three quants: GPTQ-INT4-Marlin, AWQ-INT4, GGUF-Q4_K_M for llama.cpp. Record size and nominal throughput.

6. **Serve with speculative decoding.** vLLM 0.7 config with EAGLE-3 draft heads trained via Red Hat Speculators. Measure acceptance rate and tail latency at batch 1 / 8 / 32. Report $/1M tokens vs Anthropic / OpenAI on the same eval.
   中文翻译：6. **Serve with speculative decoding.** vLLM 0.7 config with EAGLE-3 draft heads trained via Red Hat Speculators. Measure acceptance rate and tail latency at batch 1 / 8 / 32. Report $/1M tokens vs Anthropic / OpenAI on the same eval.

7. **Eval matrix.** Run lm-eval-harness, RewardBench-2, MT-Bench-v2, MMLU-Pro on base, SFT-only, SFT+DPO, SFT+GRPO. Produce a table.
   中文翻译：7. **Eval matrix.** Run lm-eval-harness, RewardBench-2, MT-Bench-v2, MMLU-Pro on base, SFT-only, SFT+DPO, SFT+GRPO. Produce a table.

8. **Safety eval.** Llama Guard 4 pass rate on the dev set. ShieldGemma-2 output filter.
   中文翻译：8. **Safety eval.** Llama Guard 4 pass rate on the dev set. ShieldGemma-2 output filter.

9. **Model card.** MOF 2026 template: data, training, eval, safety, license, reproducibility section with YAMLs and commit SHAs.
   中文翻译：9. **Model card.** MOF 2026 template: data, training, eval, safety, license, reproducibility section with YAMLs and commit SHAs.

## Use It | 使用方法

```
$ ./pipeline.sh config/llama3.3-8b-domainX.yaml
[data]    300k deduped, 12k filtered, 280k accepted (seed=7)
[SFT]     3 epochs, 8xH100, 6h12m, val loss 1.42 -> 1.03
[DPO]     1 epoch, beta=0.08, 4xH100, 1h40m
[quant]   GPTQ-INT4 4.6 GB, AWQ-INT4 4.8 GB, GGUF-Q4_K_M 5.1 GB
[serve]   vLLM 0.7, EAGLE-3 acceptance 0.74, p99 126ms @ bs=8
[eval]    MMLU-Pro +3.2, MT-Bench-v2 +0.41, RewardBench-2 +0.08
[card]    model-card.md generated under 2026 MOF
```

## Ship It | 部署上线

`outputs/skill-finetuning-pipeline.md` describes the deliverable. A single command runs data through SFT through DPO through quant through serve through eval, and emits a model card + the served endpoint.

> `outputs/skill-finetuning-pipeline.md` 描述了交付物。一条命令从数据到 SFT 到 DPO 到量化到服务到评估，并输出模型卡 + 服务端点。

| Weight | Criterion | How it is measured |
| 权重 | 标准 | 如何衡量 |
|:-:|---|---|
| 25 | Eval delta vs base | Measured gain on target tasks (MMLU-Pro, MT-Bench-v2, task-specific) |
| 25 | 评估增量 vs 基础 | 目标任务上的测量增益（MMLU-Pro、MT-Bench-v2、任务特定） |
| 20 | Pipeline reproducibility | One command reruns end to end with identical seeds |
| 20 | 管道可复现性 | 一条命令用相同种子端到端重跑 |
| 20 | Data hygiene | Dedup rate, PII scrub coverage, contamination check green |
| 20 | 数据卫生 | 去重率、PII 清洗覆盖率、污染检查通过 |
| 20 | Serving efficiency | tokens/s at bs=1/8/32, EAGLE-3 acceptance rate, $/1M tokens |
| 20 | 服务效率 | 批量 1/8/32 时的 tokens/s、EAGLE-3 接受率、$/1M tokens |
| 15 | Model card + safety eval | 2026 MOF completeness + Llama Guard 4 pass rate |
| 15 | 模型卡 + 安全评估 | 2026 MOF 完整性 + Llama Guard 4 通过率 |
| **100** | | |

## Exercises | 练习题

1. Run SFT-only vs SFT+DPO vs SFT+GRPO on the same task-specific benchmark. Report which preference method wins and by how much.
   中文翻译：在同一任务特定基准上运行 SFT-only vs SFT+DPO vs SFT+GRPO。报告哪种偏好方法获胜以及领先多少。

2. Swap Llama 3.3 8B for Qwen3 14B. Measure the $/1M tokens at matched quality.
   中文翻译：将 Llama 3.3 8B 换为 Qwen3 14B。测量匹配质量下的 $/1M tokens。

3. Measure EAGLE-3 acceptance rate on domain data vs generic ShareGPT. Report the delta and what it means for latency budgets.
   中文翻译：测量领域数据 vs 通用 ShareGPT 上的 EAGLE-3 接受率。报告差异及其对延迟预算的意义。

4. Inject 1% of contamination (leak MMLU-Pro answers into training data) and rerun eval. Watch MMLU-Pro accuracy jump unrealistically. Build a contamination-check CI gate that catches this.
   中文翻译：注入 1% 污染（将 MMLU-Pro 答案泄漏到训练数据中）并重跑评估。观察 MMLU-Pro 准确率不切实际地跳升。构建能捕获此问题的污染检查 CI 门。

5. Add LoRA SFT as an alternative to full fine-tune. Measure the quality gap at 10x lower memory.
   中文翻译：添加 LoRA SFT 作为全量微调的替代。测量 10 倍低内存下的质量差距。

## Key Terms | 术语速查表

| Term | What people say | What it actually means |
| 术语 | 通俗说法 | 实际含义 |
|------|-----------------|------------------------|
| Axolotl | "SFT trainer" | Unified YAML-driven trainer for SFT, DPO, and distillation |
| Axolotl | "SFT 训练器" | 统一的 YAML 驱动训练器，用于 SFT、DPO 和蒸馏 |
| TRL | "Preference tuner" | Hugging Face library for DPO, GRPO, PPO on LLMs |
| TRL | "偏好调优器" | Hugging Face 库，用于 LLM 上的 DPO、GRPO、PPO |
| GRPO | "Group-relative policy optimization" | DeepSeek R1's RL recipe with verifiable rewards |
| GRPO | "组相对策略优化" | DeepSeek R1 的 RL 方法，使用可验证奖励 |
| EAGLE-3 | "Speculative decoding draft" | Draft heads that predict N tokens ahead; vLLM verifies with target model |
| EAGLE-3 | "投机解码草稿" | 预测 N 个 token 的草稿头；vLLM 用目标模型验证 |
| MOF | "Model Openness Framework" | 2026 standard for grading model releases on data, code, license |
| MOF | "模型开放框架" | 2026 年按数据、代码、许可对模型发布评分的标准 |
| Contamination check | "Split hygiene" | MinHash-based detection of test-set leakage into training |
| 污染检查 | "分割卫生" | 基于 MinHash 的测试集泄漏到训练中的检测 |
| Acceptance rate | "EAGLE / MTP metric" | Fraction of drafted tokens the target model accepts |
| 接受率 | "EAGLE / MTP 指标" | 目标模型接受的草稿 token 比例 |

## Further Reading | 延伸阅读

- [Axolotl documentation](https://axolotl-ai-cloud.github.io/axolotl/) — the reference SFT / DPO trainer
  中文翻译：参考 SFT / DPO 训练器
- [TRL documentation](https://huggingface.co/docs/trl) — DPO and GRPO reference implementations
  中文翻译：DPO 和 GRPO 参考实现
- [Unsloth](https://github.com/unslothai/unsloth) — single-GPU iteration reference
  中文翻译：单 GPU 迭代参考
- [DeepSeek R1 paper (arXiv:2501.12948)](https://arxiv.org/abs/2501.12948) — GRPO methodology
  中文翻译：GRPO 方法论
- [vLLM + EAGLE-3 documentation](https://docs.vllm.ai) — reference serving stack
  中文翻译：参考服务栈
- [SGLang SpecForge](https://github.com/sgl-project/SpecForge) — alternate speculative-decoding trainer
  中文翻译：备选投机解码训练器
- [Model Openness Framework 2026](https://isocpp.org/) — the open-release grading standard
  中文翻译：开放发布评分标准
- [lm-evaluation-harness](https://github.com/EleutherAI/lm-evaluation-harness) — canonical eval runner
  中文翻译：规范评估运行器
