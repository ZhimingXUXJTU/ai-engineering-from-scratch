# TensorRT-LLM on Blackwell with FP8 and NVFP4 | Blackwell TensorRT LLM

> TensorRT-LLM is NVIDIA-only but it wins on Blackwell. On GB200 NVL72 with Dynamo orchestration, SemiAnalysis InferenceX measured $0.012 per million tokens on a 120B model in Q1-Q2 2026, against $0.09/M on H100 + vLLM — a 7x economic gap. The stack is three floating-point regimes compounded: FP8 stays critical for KV cache and attention kernels because it has the dynamic range they need; NVFP4 (4-bit microscaling) handles weights and activations; multi-token prediction (MTP) and disaggregated prefill/decode add another 2-3x on top. Day-0 model support loads FP4 weights directly without post-training conversion. The catch for 2026 engineering teams: TRT-LLM is a closed NVIDIA stack, so adopting it trades portability for throughput. Run the math on your mix of models and hardware before committing.

> **【中文解读】** 本节介绍了 TensorRT-LLM 和 Blackwell——NVIDIA 的 LLM 推理优化框架和最新 GPU 架构。


**Type:** Learn | **类型:** 学习
**Languages:** Python (stdlib, toy FP8/NVFP4 memory and cost calculator) | **语言:** Python（标准库，FP8/NVFP4 内存和成本计算器）
**Prerequisites:** Phase 17 · 04 (vLLM Serving Internals), Phase 10 · 13 (Quantization) | **前置知识:** Phase 17 · 04（vLLM 服务内部）, Phase 10 · 13（量化）
**Time:** ~75 minutes | **时间:** ~75 分钟

## Learning Objectives | 学习目标

- Explain why FP8 stays critical for KV cache and attention even when weights are in NVFP4.
  中文翻译：解释为什么即使权重在 NVFP4 中，FP8 对 KV 缓存和注意力仍然关键。
- Compute the HBM footprint of a frontier model under BF16, FP8, and NVFP4 and reason about where the savings come from.
  中文翻译：计算前沿模型在 BF16、FP8 和 NVFP4 下的 HBM 占用，分析节省来自哪里。
- Name the Blackwell-specific features TRT-LLM exploits (day-0 FP4, MTP, disaggregated serving, all-to-all primitives).
  中文翻译：说出 TRT-LLM 利用的 Blackwell 特有功能（day-0 FP4、MTP、分离式服务、all-to-all 原语）。
- Decide when TRT-LLM's NVIDIA-lock is worth the 7x cost gap vs vLLM on Hopper.
  中文翻译：决定 TRT-LLM 的 NVIDIA 锁定何时值得相比 Hopper 上 vLLM 的 7x 成本差距。

## The Problem | 问题引入

> **【中文解读】** 2026 年推理经济学的前沿问题是"每美元多少 token"。答案取决于四层叠加选择：硬件代际（Hopper H100/H200 vs Blackwell B200/GB200）、精度（BF16 → FP8 → NVFP4）、推理引擎（vLLM vs SGLang vs TRT-LLM）和编排（朴素 vs 分离式 vs Dynamo）。在 Hopper + vLLM 上运行 120B MoE 约 $0.09/M tokens；在 Blackwell + TRT-LLM + Dynamo 上仅 $0.012/M——7x 差距。这个差距的代价是 NVIDIA 锁定——你无法在其他厂商的硬件上复现。

> **【拓展：NVIDIA Blackwell 架构】** Blackwell（B200/GB200）是 NVIDIA 2024-2025 年推出的 GPU 架构，相比 Hopper (H100) 在 LLM 推理上有 11-15x 的每 GPU 吞吐提升。关键特性包括：NVFP4 精度（4-bit 微缩放浮点，硬件加速）、NVLink 5（MoE 专家通信延迟降低 3x）、第二代 Transformer Engine、以及 GB200 NVL72 的 72-GPU 一致内存域。MLPerf Inference v6.0（2026 年 4 月）显示 Blackwell 在所有提交任务中全面领先。

The frontier of inference economics in 2026 is "how many tokens per dollar". The answer depends on four stacked choices: hardware generation (Hopper H100/H200 vs Blackwell B200/GB200), precision (BF16 → FP8 → NVFP4), serving engine (vLLM vs SGLang vs TRT-LLM), and orchestration (plain vs disaggregated vs Dynamo).

> 2026 年推理经济学的前沿是"每美元多少 token"。答案取决于四个叠加选择：硬件代际（Hopper vs Blackwell）、精度（BF16 → FP8 → NVFP4）、推理引擎（vLLM vs SGLang vs TRT-LLM）和编排（朴素 vs 分离式 vs Dynamo）。

On Hopper with vLLM, a 120B MoE runs at ~$0.09 per million tokens. On Blackwell with TRT-LLM + Dynamo, the same model runs at ~$0.012 — 7x cheaper. Some of that gap is hardware (Blackwell is 11-15x per-GPU LLM throughput vs Hopper). Some is the stack: FP4 weights, MTP draft, disaggregated prefill/decode, and NVLink 5 all-to-all for MoE expert communication.

> 在 Hopper + vLLM 上，120B MoE 运行约 $0.09/M tokens。在 Blackwell + TRT-LLM + Dynamo 上，同一模型运行约 $0.012——便宜 7 倍。部分差距来自硬件（Blackwell vs Hopper 每 GPU LLM 吞吐 11-15 倍）。部分来自栈：FP4 权重、MTP draft、分离式预填充/解码和 NVLink 5 all-to-all 用于 MoE 专家通信。

You cannot replicate this outside NVIDIA's stack. That is the tradeoff — portability for economics. Understanding which stack choices give which share of the gap is the point of this lesson.

> 你无法在 NVIDIA 栈之外复现。这就是权衡——可移植性换经济性。理解哪个栈选择贡献差距的哪部分是本课的重点。

## The Concept | 核心概念

### Why FP8 is still the floor for KV cache

> **【中文解读】** FP8 是 KV Cache 的最低精度要求。KV Cache 存储的注意力键值跨越很宽的动态范围——将 KV 量化到 FP4 会导致灾难性精度损失。NVFP4 只适用于权重和激活——微缩放让每个权重块有独立的缩放因子。典型的 Blackwell 配置是：权重 NVFP4（4-bit 微缩放）、激活 NVFP4、KV Cache FP8、注意力累加器 FP32。

A common mistake in 2026: assuming NVFP4 applies everywhere. It does not. KV cache needs FP8 (8-bit floating point) because it stores attention keys and values that span a wide dynamic range. Quantizing KV to FP4 causes catastrophic accuracy loss — the tail of the distribution drops off and attention scores collapse. FP8's exponent bits give KV cache the range it needs.

> 2026 年的一个常见错误：假设 NVFP4 适用于所有地方。不是的。KV 缓存需要 FP8（8 位浮点），因为它存储跨越很宽动态范围的注意力键值。将 KV 量化到 FP4 会导致灾难性精度损失——分布尾部衰减，注意力分数崩塌。FP8 的指数位给 KV 缓存所需的范围。

NVFP4 (2025-2026) applies to weights and activations. Microscaling: each block of weights has its own scale factor so small blocks can span different dynamic ranges without per-tensor scale loss. For activations, FP4 holds up because activations are small-range within a layer.

> NVFP4（2025-2026）适用于权重和激活。微缩放：每个权重块有自己的缩放因子，小块可以跨越不同动态范围而不损失每张量缩放。对于激活，FP4 可以保持，因为激活在层内范围较小。

The typical Blackwell config:

- Weights: NVFP4 (4-bit microscaling).
  中文翻译：权重：NVFP4（4-bit 微缩放）。
- Activations: NVFP4.
  中文翻译：激活：NVFP4。
- KV cache: FP8.
  中文翻译：KV 缓存：FP8。
- Attention accumulator: FP32 (softmax stability).
  中文翻译：注意力累加器：FP32（softmax 稳定性）。

### The Blackwell-specific primitives TRT-LLM uses

- **Day-0 FP4 weights**: model providers ship FP4 weights directly; TRT-LLM loads without post-training conversion. No AWQ / GPTQ step for FP4.
  中文翻译：**Day-0 FP4 权重**：模型提供商直接发布 FP4 权重；TRT-LLM 无需训练后转换即可加载。FP4 不需要 AWQ/GPTQ 步骤。
- **Multi-token prediction (MTP)**: same idea as EAGLE (Phase 17 · 05) but integrated into the TRT-LLM build.
  中文翻译：**多 token 预测 (MTP)**：与 EAGLE 相同的想法（Phase 17 · 05），但集成到 TRT-LLM 构建中。
- **Disaggregated serving**: prefill and decode on separate GPU pools, KV cache transferred over NVLink or InfiniBand. Same idea as Dynamo (Phase 17 · 20).
  中文翻译：**分离式服务**：预填充和解码在独立 GPU 池上，KV 缓存通过 NVLink 或 InfiniBand 传输。
- **All-to-all communication primitives**: NVLink 5 cut MoE expert communication latency by 3x vs Hopper. TRT-LLM's MoE kernels are tuned for this.
  中文翻译：**All-to-all 通信原语**：NVLink 5 将 MoE 专家通信延迟降低 3 倍。
- **NVFP4 + MXFP8 microscaling**: hardware-accelerated scale-factor handling on Blackwell Tensor Cores.
  中文翻译：**NVFP4 + MXFP8 微缩放**：Blackwell Tensor Core 上的硬件加速缩放因子处理。

### The numbers you should memorize

- HGX B200 at $0.02/M tokens on GPT-OSS-120B via TRT-LLM.
  中文翻译：HGX B200 在 GPT-OSS-120B 上通过 TRT-LLM 为 $0.02/M tokens。
- GB200 NVL72 at $0.012/M tokens via Dynamo (orchestrating TRT-LLM).
  中文翻译：GB200 NVL72 通过 Dynamo（编排 TRT-LLM）为 $0.012/M tokens。
- H100 + vLLM ≈ $0.09/M tokens on comparable workload.
  中文翻译：H100 + vLLM 在可比工作负载上约 $0.09/M tokens。
- 2.8x throughput gain in three months of TRT-LLM updates (2026).
  中文翻译：TRT-LLM 2026 年三个月更新的 2.8 倍吞吐量提升。
- 11-15x per-GPU LLM throughput, Blackwell vs Hopper.
  中文翻译：Blackwell vs Hopper 每 GPU LLM 吞吐量 11-15 倍。
- MLPerf Inference v6.0 (April 2026): Blackwell dominates every submitted task.
  中文翻译：MLPerf Inference v6.0（2026 年 4 月）：Blackwell 在所有提交任务中领先。

### What FP4 actually costs in quality

> **【中文解读】** NVFP4 在推理密集型工作负载（思维链、数学、长上下文代码生成）上会导致可见的质量退化。每块校准可以缓解但不能消除。2026 年的实践指南是：推理模型使用 FP8 权重 + FP4 激活作为折中，或继续使用 H200 全 FP8。规则是：在提交 NVFP4 权重之前，必须在自己的评估集上验证任务质量。

> **【拓展：量化精度 vs 推理成本权衡】** 量化精度的选择是质量和成本的权衡：(1) BF16——无质量损失，但内存需求大（70B 模型需 140GB）；(2) FP8——近乎无损，Hopper/Blackwell 硬件加速，推荐用于推理密集型任务；(3) INT4（AWQ/GPTQ）——4-bit 权重，MATH 分数下降 3-5 点，适合通用聊天；(4) NVFP4——最激进，Blackwell 专用，必须在目标评估集上验证。生产中通常混合使用：权重低精度、KV Cache FP8。

NVFP4 is aggressive. On reasoning-heavy workloads (chain-of-thought, math, code-gen with long context), FP4 weights degrade visibly. Per-block calibration mitigates but does not eliminate. Teams shipping reasoning models often use FP8 weights + FP4 activations as a compromise, or stick to H200 with FP8 throughout.

> NVFP4 是激进的。在推理密集型工作负载（思维链、数学、长上下文代码生成）上，FP4 权重明显退化。每块校准缓解但不能消除。发布推理模型的团队通常使用 FP8 权重 + FP4 激活作为折中，或在 H200 上坚持全 FP8。

The rule: always validate task quality on your eval set before committing to NVFP4 weights.

> 规则：在提交 NVFP4 权重之前，始终在你的评估集上验证任务质量。

### Why this is an NVIDIA-lock decision

> **【中文解读】** TRT-LLM 是 C++ + CUDA + 闭源内核的组合。模型需要为特定 GPU SKU 编译。不支持 AMD、Intel 或 ARM。如果你的基础设施策略是多供应商，TRT-LLM 对于这个层是不可选项——你仍然可以在混合硬件上使用 vLLM。但如果你是 NVIDIA-only，7x 的经济差距值得这个锁定。

> **【拓展：NVIDIA vs AMD 推理生态】** 2026 年 AI 推理芯片市场的格局：NVIDIA 凭借 CUDA 生态和 TRT-LLM 占据约 80% 的数据中心推理份额。AMD MI300X 在原始算力上有竞争力，但软件栈（ROCm + vLLM）仍在追赶。Intel Gaudi 3 是另一个选项但采用率较低。对于年推理支出 $100M+ 的企业，迁移到 Blackwell + TRT-LLM + Dynamo 的 7x 成本差距可以节省数千万美元。

TRT-LLM is C++ + CUDA + closed-source kernels. Models need to be compiled for a specific GPU SKU. No AMD, no Intel, no ARM. If your infra strategy is multi-vendor, TRT-LLM is a non-starter for the TRT-LLM-served tier — you can still serve from vLLM on mixed hardware. If you are NVIDIA-only, the 7x gap pays for the lock.

> TRT-LLM 是 C++ + CUDA + 闭源内核的组合。模型需要为特定 GPU SKU 编译。不支持 AMD、Intel 或 ARM。如果你的基础设施策略是多供应商，TRT-LLM 不可行——你仍可以在混合硬件上使用 vLLM。如果你是 NVIDIA-only，7x 差距值得这个锁定。

### 2026 practical recipe

For a $100M+ annual inference bill, running on Hopper + vLLM leaves 7-10x on the table. Migrate cost-dominant workloads to Blackwell + TRT-LLM + Dynamo. Keep experimentation tier on H100 + vLLM for model iteration speed. Validate quality on each NVFP4-converted model before production.

> 对于 $100M+ 的年度推理支出，在 Hopper + vLLM 上运行意味着留下 7-10 倍的节省空间。将成本主导的工作负载迁移到 Blackwell + TRT-LLM + Dynamo。在 H100 + vLLM 上保持实验层用于模型迭代速度。在每个 NVFP4 转换模型上线前验证质量。

### The disaggregation bonus

TRT-LLM's disaggregated serving (separate prefill and decode pools) is covered in depth in Phase 17 · 20. On Blackwell, the multiplier stacks: FP4 weights × MTP speedup × disaggregated placement × cache-aware routing. The 7x number assumes this full stack.

> TRT-LLM 的分离式服务（独立预填充和解码池）在 Phase 17 · 20 中深入讨论。在 Blackwell 上，乘数叠加：FP4 权重 × MTP 加速 × 分离式部署 × 缓存感知路由。7x 数字假设使用完整栈。

## Use It | 用框架实现

> **【拓展：Blackwell 迁移决策】** 从 Hopper 迁移到 Blackwell + TRT-LLM 的决策框架：(1) 年推理支出是否超过 $5M？是→值得评估迁移；(2) 是否可以接受 NVIDIA 锁定？否→继续使用 vLLM + Hopper；(3) 工作负载是否包含 MoE 模型？是→Blackwell 的 NVLink 5 all-to-all 提供额外 3x 加速；(4) 推理密集型任务占比是否超过 30%？是→需要验证 NVFP4 质量。迁移 ROI 通常在 6-12 个月内回本。

`code/main.py` computes HBM footprint, decode throughput (memory-bound regime), and $/M-tokens for a model across three stacks: H100 + BF16 + vLLM, H100 + FP8 + vLLM, B200 + NVFP4/FP8 + TRT-LLM. Run it to see the compounding effect and the share of the gap each change contributes.

> `code/main.py` 计算模型在三个栈上的 HBM 占用、解码吞吐量（内存受限）和 $/M-tokens：H100 + BF16 + vLLM、H100 + FP8 + vLLM、B200 + NVFP4/FP8 + TRT-LLM。运行它查看复合效应和每个变化贡献的差距份额。

## Ship It | 产出物

This lesson produces `outputs/skill-trtllm-blackwell-advisor.md`. Given a workload, model size, and annual token volume, it decides whether the Blackwell + TRT-LLM stack is worth the NVIDIA-lock.

> 本课产出 `outputs/skill-trtllm-blackwell-advisor.md`。给定工作负载、模型大小和年度 token 量，它决定 Blackwell + TRT-LLM 栈是否值得 NVIDIA 锁定。

## Exercises | 练习题

1. Run `code/main.py`. On a 120B MoE with 30% active parameters, compute the memory-bandwidth-limited decode throughput on H100 BF16, H100 FP8, and B200 NVFP4/FP8. Where does the biggest jump come from?
   中文翻译：运行 `code/main.py`。在 30% 活跃参数的 120B MoE 上，计算 H100 BF16、H100 FP8 和 B200 NVFP4/FP8 的内存带宽受限解码吞吐量。最大跳跃来自哪里？
2. A customer spends $2M/year on H100 + vLLM. What is the break-even number of Blackwell GPUs they need to buy to amortize a migration to TRT-LLM in 12 months, given the 7x economic gap?
   中文翻译：客户在 H100 + vLLM 上每年花费 $2M。给定 7x 经济差距，他们需要购买多少 Blackwell GPU 才能在 12 个月内摊销迁移到 TRT-LLM 的成本？
3. You see accuracy drop 3 points on MATH after NVFP4 weight conversion. Name two recovery paths: one quality-first (keep FP8 weights), one cost-first (calibrate with in-domain data).
   中文翻译：NVFP4 权重转换后 MATH 精度下降 3 点。说出两条恢复路径：一条质量优先（保持 FP8 权重），一条成本优先（用领域内数据校准）。
4. Read the MLPerf v6.0 inference results. Which task has the smallest Blackwell-over-Hopper gap, and why?
   中文翻译：阅读 MLPerf v6.0 推理结果。哪个任务的 Blackwell-over-Hopper 差距最小，为什么？
5. Compute the HBM needed for a 405B model at NVFP4 weights + FP8 KV cache at 128k context. Does it fit on a single GB200 NVL72 node?
   中文翻译：计算 405B 模型在 NVFP4 权重 + FP8 KV 缓存 + 128k 上下文下的 HBM 需求。它是否适合单个 GB200 NVL72 节点？

## Key Terms | 术语速查表

| Term / 术语 | What people say / 通俗说法 | What it actually means / 实际含义 |
|------|----------------|------------------------|
| FP8 | "eight-bit float" / "8-bit 浮点" | 8-bit floating point; used for KV cache and attention due to dynamic range / 8-bit 浮点；因动态范围用于 KV 缓存和注意力 |
| NVFP4 | "four-bit micro" / "4-bit 微缩放" | NVIDIA's 4-bit microscaling FP format; weights and activations on Blackwell / NVIDIA 4-bit 微缩放浮点格式；Blackwell 上的权重和激活 |
| MXFP8 | "MX eight" / "MX 8-bit" | Microscaling FP8 variant; hardware-accelerated on Blackwell Tensor Cores / 微缩放 FP8 变体；Blackwell Tensor Core 硬件加速 |
| Day-0 FP4 | "ship FP4 weights" / "直接发布 FP4 权重" | Model providers release weights already in FP4; no post-train conversion step / 模型提供商直接发布 FP4 权重；无训练后转换步骤 |
| MTP | "multi-token prediction" / "多 token 预测" | TRT-LLM's integrated speculative-decoding draft (Phase 17 · 05) / TRT-LLM 集成的推测解码 draft |
| Disaggregated serving | "split prefill/decode" / "分离预填充/解码" | Prefill and decode on separate GPU pools; KV transferred over NVLink/IB / 独立 GPU 池的预填充和解码 |
| All-to-all | "MoE expert comm" / "MoE 专家通信" | Communication pattern routing tokens to expert GPUs; NVLink 5 cuts 3x / 将 token 路由到专家 GPU 的通信模式 |
| InferenceX | "SemiAnalysis inference bench" / "推理基准" | The 2026 industry-accepted cost-per-token benchmark / 2026 年行业接受的每 token 成本基准 |

## Further Reading | 延伸阅读

- [NVIDIA — Blackwell Ultra MLPerf Inference v6.0](https://developer.nvidia.com/blog/nvidia-blackwell-ultra-sets-new-inference-records-in-mlperf-debut/) — April 2026 MLPerf results.
- [NVIDIA — MoE Inference on Blackwell](https://developer.nvidia.com/blog/delivering-massive-performance-leaps-for-mixture-of-experts-inference-on-nvidia-blackwell/) — NVLink 5 all-to-all and MoE kernels.
- [TensorRT-LLM Overview](https://nvidia.github.io/TensorRT-LLM/overview.html) — official engine documentation.
- [NVIDIA — Introducing Dynamo](https://developer.nvidia.com/blog/introducing-nvidia-dynamo-a-low-latency-distributed-inference-framework-for-scaling-reasoning-ai-models/) — disaggregated orchestration above TRT-LLM.
- [MLPerf Inference](https://mlcommons.org/benchmarks/inference-datacenter/) — the benchmark suite that publishes Blackwell numbers.
