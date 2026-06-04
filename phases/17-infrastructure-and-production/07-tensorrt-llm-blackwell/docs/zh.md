# TensorRT-LLM on Blackwell with FP8 and NVFP4 | Blackwell TensorRT LLM

> TensorRT-LLM is NVIDIA-only but it wins on Blackwell. On GB200 NVL72 with Dynamo orchestration, SemiAnalysis InferenceX measured $0.012 per million tokens on a 120B model in Q1-Q2 2026, against $0.09/M on H100 + vLLM — a 7x economic gap. The stack is three floating-point regimes compounded: FP8 stays critical for KV cache and attention kernels because it has the dynamic range they need; NVFP4 (4-bit microscaling) handles weights and activations; multi-token prediction (MTP) and disaggregated prefill/decode add another 2-3x on top. Day-0 model support loads FP4 weights directly without post-training conversion. The catch for 2026 engineering teams: TRT-LLM is a closed NVIDIA stack, so adopting it trades portability for throughput. Run the math on your mix of models and hardware before committing.

> **【中文解读】** 本节介绍了 TensorRT-LLM 和 Blackwell——NVIDIA 的 LLM 推理优化框架和最新 GPU 架构。


**类型：** 学习
**语言：** Python (stdlib, toy FP8/NVFP4 memory and cost calculator)
**前置条件：** Phase 17 · 04 (vLLM Serving Internals), Phase 10 · 13 (Quantization)
**时间：** ~75 minutes

## 学习目标 | 学习目标

- Explain why FP8 stays critical for KV cache and attention even when weights are in NVFP4.
- Compute the HBM footprint of a frontier model under BF16, FP8, and NVFP4 and reason about where the savings come from.
- Name the Blackwell-specific features TRT-LLM exploits (day-0 FP4, MTP, disaggregated serving, all-to-all primitives).
- Decide when TRT-LLM's NVIDIA-lock is worth the 7x cost gap vs vLLM on Hopper.

## 问题引入 | 问题

> **【中文解读】** 2026 年推理经济学的前沿问题是"每美元多少 token"。答案取决于四层叠加选择：硬件代际（Hopper H100/H200 vs Blackwell B200/GB200）、精度（BF16 → FP8 → NVFP4）、推理引擎（vLLM vs SGLang vs TRT-LLM）和编排（朴素 vs 分离式 vs Dynamo）。在 Hopper + vLLM 上运行 120B MoE 约 $0.09/M tokens；在 Blackwell + TRT-LLM + Dynamo 上仅 $0.012/M——7x 差距。这个差距的代价是 NVIDIA 锁定——你无法在其他厂商的硬件上复现。

> **【拓展：NVIDIA Blackwell 架构】** Blackwell（B200/GB200）是 NVIDIA 2024-2025 年推出的 GPU 架构，相比 Hopper (H100) 在 LLM 推理上有 11-15x 的每 GPU 吞吐提升。关键特性包括：NVFP4 精度（4-bit 微缩放浮点，硬件加速）、NVLink 5（MoE 专家通信延迟降低 3x）、第二代 Transformer Engine、以及 GB200 NVL72 的 72-GPU 一致内存域。MLPerf Inference v6.0（2026 年 4 月）显示 Blackwell 在所有提交任务中全面领先。

The frontier of inference economics in 2026 is "how many tokens per dollar". The answer depends on four stacked choices: hardware generation (Hopper H100/H200 vs Blackwell B200/GB200), precision (BF16 → FP8 → NVFP4), serving engine (vLLM vs SGLang vs TRT-LLM), and orchestration (plain vs disaggregated vs Dynamo).

On Hopper with vLLM, a 120B MoE runs at ~$0.09 per million tokens. On Blackwell with TRT-LLM + Dynamo, the same model runs at ~$0.012 — 7x cheaper. Some of that gap is hardware (Blackwell is 11-15x per-GPU LLM throughput vs Hopper). Some is the stack: FP4 weights, MTP draft, disaggregated prefill/decode, and NVLink 5 all-to-all for MoE expert communication.

You cannot replicate this outside NVIDIA's stack. That is the tradeoff — portability for economics. Understanding which stack choices give which share of the gap is the point of this lesson.

## 核心概念 | 概念

### Why FP8 is still the floor for KV cache

> **【中文解读】** FP8 是 KV Cache 的最低精度要求。KV Cache 存储的注意力键值跨越很宽的动态范围——将 KV 量化到 FP4 会导致灾难性精度损失。NVFP4 只适用于权重和激活——微缩放让每个权重块有独立的缩放因子。典型的 Blackwell 配置是：权重 NVFP4（4-bit 微缩放）、激活 NVFP4、KV Cache FP8、注意力累加器 FP32。

A common mistake in 2026: assuming NVFP4 applies everywhere. It does not. KV cache needs FP8 (8-bit floating point) because it stores attention keys and values that span a wide dynamic range. Quantizing KV to FP4 causes catastrophic accuracy loss — the tail of the distribution drops off and attention scores collapse. FP8's exponent bits give KV cache the range it needs.

NVFP4 (2025-2026) applies to weights and activations. Microscaling: each block of weights has its own scale factor so small blocks can span different dynamic ranges without per-tensor scale loss. For activations, FP4 holds up because activations are small-range within a layer.

The typical Blackwell config:

- Weights: NVFP4 (4-bit microscaling).
- Activations: NVFP4.
- KV cache: FP8.
- Attention accumulator: FP32 (softmax stability).

### The Blackwell-specific primitives TRT-LLM uses

- **Day-0 FP4 weights**: model providers ship FP4 weights directly; TRT-LLM loads without post-training conversion. No AWQ / GPTQ step for FP4.
- **Multi-token prediction (MTP)**: same idea as EAGLE (Phase 17 · 05) but integrated into the TRT-LLM build.
- **Disaggregated serving**: prefill and decode on separate GPU pools, KV cache transferred over NVLink or InfiniBand. Same idea as Dynamo (Phase 17 · 20).
- **All-to-all communication primitives**: NVLink 5 cut MoE expert communication latency by 3x vs Hopper. TRT-LLM's MoE kernels are tuned for this.
- **NVFP4 + MXFP8 microscaling**: hardware-accelerated scale-factor handling on Blackwell Tensor Cores.

### The numbers you should memorize

- HGX B200 at $0.02/M tokens on GPT-OSS-120B via TRT-LLM.
- GB200 NVL72 at $0.012/M tokens via Dynamo (orchestrating TRT-LLM).
- H100 + vLLM ≈ $0.09/M tokens on comparable workload.
- 2.8x throughput gain in three months of TRT-LLM updates (2026).
- 11-15x per-GPU LLM throughput, Blackwell vs Hopper.
- MLPerf Inference v6.0 (April 2026): Blackwell dominates every submitted task.

### What FP4 actually costs in quality

> **【中文解读】** NVFP4 在推理密集型工作负载（思维链、数学、长上下文代码生成）上会导致可见的质量退化。每块校准可以缓解但不能消除。2026 年的实践指南是：推理模型使用 FP8 权重 + FP4 激活作为折中，或继续使用 H200 全 FP8。规则是：在提交 NVFP4 权重之前，必须在自己的评估集上验证任务质量。

> **【拓展：量化精度 vs 推理成本权衡】** 量化精度的选择是质量和成本的权衡：(1) BF16——无质量损失，但内存需求大（70B 模型需 140GB）；(2) FP8——近乎无损，Hopper/Blackwell 硬件加速，推荐用于推理密集型任务；(3) INT4（AWQ/GPTQ）——4-bit 权重，MATH 分数下降 3-5 点，适合通用聊天；(4) NVFP4——最激进，Blackwell 专用，必须在目标评估集上验证。生产中通常混合使用：权重低精度、KV Cache FP8。

NVFP4 is aggressive. On reasoning-heavy workloads (chain-of-thought, math, code-gen with long context), FP4 weights degrade visibly. Per-block calibration mitigates but does not eliminate. Teams shipping reasoning models often use FP8 weights + FP4 activations as a compromise, or stick to H200 with FP8 throughout.

The rule: always validate task quality on your eval set before committing to NVFP4 weights.

### Why this is an NVIDIA-lock decision

> **【中文解读】** TRT-LLM 是 C++ + CUDA + 闭源内核的组合。模型需要为特定 GPU SKU 编译。不支持 AMD、Intel 或 ARM。如果你的基础设施策略是多供应商，TRT-LLM 对于这个层是不可选项——你仍然可以在混合硬件上使用 vLLM。但如果你是 NVIDIA-only，7x 的经济差距值得这个锁定。

> **【拓展：NVIDIA vs AMD 推理生态】** 2026 年 AI 推理芯片市场的格局：NVIDIA 凭借 CUDA 生态和 TRT-LLM 占据约 80% 的数据中心推理份额。AMD MI300X 在原始算力上有竞争力，但软件栈（ROCm + vLLM）仍在追赶。Intel Gaudi 3 是另一个选项但采用率较低。对于年推理支出 $100M+ 的企业，迁移到 Blackwell + TRT-LLM + Dynamo 的 7x 成本差距可以节省数千万美元。

TRT-LLM is C++ + CUDA + closed-source kernels. Models need to be compiled for a specific GPU SKU. No AMD, no Intel, no ARM. If your infra strategy is multi-vendor, TRT-LLM is a non-starter for the TRT-LLM-served tier — you can still serve from vLLM on mixed hardware. If you are NVIDIA-only, the 7x gap pays for the lock.

### 2026 practical recipe

For a $100M+ annual inference bill, running on Hopper + vLLM leaves 7-10x on the table. Migrate cost-dominant workloads to Blackwell + TRT-LLM + Dynamo. Keep experimentation tier on H100 + vLLM for model iteration speed. Validate quality on each NVFP4-converted model before production.

### The disaggregation bonus

TRT-LLM's disaggregated serving (separate prefill and decode pools) is covered in depth in Phase 17 · 20. On Blackwell, the multiplier stacks: FP4 weights × MTP speedup × disaggregated placement × cache-aware routing. The 7x number assumes this full stack.

## 用框架实现 | 使用方法

> **【拓展：Blackwell 迁移决策】** 从 Hopper 迁移到 Blackwell + TRT-LLM 的决策框架：(1) 年推理支出是否超过 $5M？是→值得评估迁移；(2) 是否可以接受 NVIDIA 锁定？否→继续使用 vLLM + Hopper；(3) 工作负载是否包含 MoE 模型？是→Blackwell 的 NVLink 5 all-to-all 提供额外 3x 加速；(4) 推理密集型任务占比是否超过 30%？是→需要验证 NVFP4 质量。迁移 ROI 通常在 6-12 个月内回本。

`code/main.py` computes HBM footprint, decode throughput (memory-bound regime), and $/M-tokens for a model across three stacks: H100 + BF16 + vLLM, H100 + FP8 + vLLM, B200 + NVFP4/FP8 + TRT-LLM. Run it to see the compounding effect and the share of the gap each change contributes.

## 产出物 | 部署上线

This lesson produces `outputs/skill-trtllm-blackwell-advisor.md`. Given a workload, model size, and annual token volume, it decides whether the Blackwell + TRT-LLM stack is worth the NVIDIA-lock.

## 练习题 | 练习题

1. Run `code/main.py`. On a 120B MoE with 30% active parameters, compute the memory-bandwidth-limited decode throughput on H100 BF16, H100 FP8, and B200 NVFP4/FP8. Where does the biggest jump come from?
2. A customer spends $2M/year on H100 + vLLM. What is the break-even number of Blackwell GPUs they need to buy to amortize a migration to TRT-LLM in 12 months, given the 7x economic gap?
3. You see accuracy drop 3 points on MATH after NVFP4 weight conversion. Name two recovery paths: one quality-first (keep FP8 weights), one cost-first (calibrate with in-domain data).
4. Read the MLPerf v6.0 inference results. Which task has the smallest Blackwell-over-Hopper gap, and why?
5. Compute the HBM needed for a 405B model at NVFP4 weights + FP8 KV cache at 128k context. Does it fit on a single GB200 NVL72 node?

## 术语速查表 | 关键术语

| Term | What people say | What it actually means |
|------|----------------|------------------------|
| FP8 | "eight-bit float" | 8-bit floating point; used for KV cache and attention due to dynamic range |
| NVFP4 | "four-bit micro" | NVIDIA's 4-bit microscaling FP format; weights and activations on Blackwell |
| MXFP8 | "MX eight" | Microscaling FP8 variant; hardware-accelerated on Blackwell Tensor Cores |
| Day-0 FP4 | "ship FP4 weights" | Model providers release weights already in FP4; no post-train conversion step |
| MTP | "multi-token prediction" | TRT-LLM's integrated speculative-decoding draft (Phase 17 · 05) |
| Disaggregated serving | "split prefill/decode" | Prefill and decode on separate GPU pools; KV transferred over NVLink/IB |
| All-to-all | "MoE expert comm" | Communication pattern routing tokens to expert GPUs; NVLink 5 cuts 3x |
| InferenceX | "SemiAnalysis inference bench" | The 2026 industry-accepted cost-per-token benchmark |

## 延伸阅读 | 延伸阅读

- [NVIDIA — Blackwell Ultra MLPerf Inference v6.0](https://developer.nvidia.com/blog/nvidia-blackwell-ultra-sets-new-inference-records-in-mlperf-debut/) — April 2026 MLPerf results.
- [NVIDIA — MoE Inference on Blackwell](https://developer.nvidia.com/blog/delivering-massive-performance-leaps-for-mixture-of-experts-inference-on-nvidia-blackwell/) — NVLink 5 all-to-all and MoE kernels.
- [TensorRT-LLM Overview](https://nvidia.github.io/TensorRT-LLM/overview.html) — official engine documentation.
- [NVIDIA — Introducing Dynamo](https://developer.nvidia.com/blog/introducing-nvidia-dynamo-a-low-latency-distributed-inference-framework-for-scaling-reasoning-ai-models/) — disaggregated orchestration above TRT-LLM.
- [MLPerf Inference](https://mlcommons.org/benchmarks/inference-datacenter/) — the benchmark suite that publishes Blackwell numbers.
