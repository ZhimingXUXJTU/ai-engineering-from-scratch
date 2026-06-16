# Janus-Pro: Decoupled Encoders for Unified Multimodal Models | Janus-Pro：解耦编码器的统一多模态模型

> Unified multimodal models have an unavoidable tension. Understanding wants semantic features — SigLIP or DINOv2 output vectors rich with concept-level information. Generation wants reconstruction-friendly codes — VQ tokens that compose back into crisp pixels. The two goals are not compatible in a single encoder. Janus (DeepSeek, October 2024) and Janus-Pro (DeepSeek, January 2025) argue the fix is to stop trying: decouple the two encoders. Share the transformer body between tasks, but route understanding through SigLIP and generation through a VQ tokenizer. At 7B, Janus-Pro beats DALL-E 3 on GenEval while matching LLaVA on MMMU. This lesson reads why two encoders work where one fails.

> **【中文解读】** Janus-Pro（DeepSeek，2025年1月）解决了一个根本矛盾：理解任务需要语义特征（SigLIP），生成任务需要重建友好的编码（VQ token）。两者无法兼容于单一编码器。Janus-Pro 的答案是解耦：理解走 SigLIP 路径，生成走 VQ 路径，共享 Transformer 主体。7B 参数就在 GenEval 上击败了 DALL-E 3。

> **【拓展：解耦编码器的产业影响】** 解耦编码器思想已成为 2026 年统一模型的默认架构。InternVL-U 将其整合到了原生多模态预训练框架中。对于需要同时理解和生成的产品（如创意工具、内容生成平台），Janus-Pro 是参考架构。

**Type:** Build  | **类型:** 构建
**Languages:** Python (stdlib, dual-encoder routing + shared-body signal) | **语言:** Python（标准库，双编码器路由 + 共享体信号）
**Prerequisites:** Phase 12 · 13 (Transfusion), Phase 12 · 14 (Show-o) | **前置知识:** Phase 12 · 13（Transfusion），Phase 12 · 14（Show-o）
**Time:** ~120 minutes | **时间:** ~120 分钟

> 🔗 **【前置】** 学本节前请先掌握：Phase 12·02（SigLIP 语义编码器）、Phase 12·13-14（Transfusion/Show-o 统一模型）、Phase 8（VQ-VAE 重建编码器）。Janus-Pro = "理解 vs 生成的编码器分离"——是 Phase 12 多模态生成模型的最终答案之一。
> 💡 **【类比】** Janus-Pro = "左右脑分工"。左脑 = SigLIP（语义理解，认识"猫"的概念）；右脑 = VQ-VAE（像素重建，能画出猫的细节）。其他统一模型 = 强迫一个脑区同时干两件事，两边都不极致；Janus-Pro = 接受左右脑分工，共享脑干（Transformer 主体）做高层推理。这就像人类视觉皮层（理解）和运动皮层（绘画）本来就在不同脑区。

## Learning Objectives  | 学习目标

- Explain why a single shared encoder compromises either understanding or generation quality.
  > 解释为什么单一共享编码器会损害理解或生成质量。
- Describe Janus-Pro's routing: SigLIP features on the input side for understanding, VQ tokens on both input and output for generation.
  > 描述 Janus-Pro 的路由：理解路径输入侧用 SigLIP 特征，生成路径输入和输出侧都用 VQ token。
- Trace the data-mix scaling that makes Janus-Pro succeed where Janus did not.
  > 追溯让 Janus-Pro 成功而 Janus 失败的数据混合扩展。
- Compare decoupled (Janus-Pro), coupled-continuous (Transfusion), and coupled-discrete (Show-o) architectures.
  > 比较解耦（Janus-Pro）、耦合连续（Transfusion）、耦合离散（Show-o）三种架构。

## The Problem  | 问题背景

Unified models share a transformer body across understanding and generation. Previous attempts (Chameleon, Show-o, Transfusion) all use one visual tokenizer for both directions. The tokenizer is a compromise:

> 统一模型在理解和生成之间共享 Transformer 主体。之前的尝试（Chameleon、Show-o、Transfusion）都使用一个视觉分词器处理两个方向。分词器是妥协：

- Optimized for reconstruction (generation): VQ-VAE captures fine-grained pixel detail but produces tokens with weak semantic coherence.
  中文翻译：为重建优化（生成）：VQ-VAE 捕获细粒度像素细节，但产生的 token 语义一致性弱。
- Optimized for semantics (understanding): SigLIP embeddings group "cat" images near "cat" tokens but do not permit good reconstruction.
  中文翻译：为语义优化（理解）：SigLIP 嵌入将"猫"的图像归到"猫"的 token 附近，但不允许好的重建。

Show-o and Transfusion pay for this with a visible quality tax on one direction. Janus-Pro asks: why require one tokenizer when the tasks have different needs?

> Show-o 和 Transfusion 为此付出了可见的质量税。Janus-Pro 问：当任务有不同需求时，为什么要用一个分词器？

## The Concept  | 核心概念

> **【中文解读】** Janus-Pro（DeepSeek）使用解耦的视觉编码器：一个用于理解任务（CLIP 编码器），一个用于生成任务（VQ 编码器）。两个编码器共享同一个 LLM backbone，各自专注优化不同的视觉表示。

> **【拓展：解耦编码器的动机】** 理解任务需要高层语义特征，生成任务需要底层细节特征。单个编码器难以同时做好两者。Janus-Pro 的解耦设计在理解和生成任务上都超过了统一编码器方案。


### Decoupled visual encoding

Janus-Pro's architecture separates the two encoders:

> Janus-Pro 的架构将两个编码器分离：

- Understanding path. Input image → SigLIP-SO400m → 2-layer MLP → transformer body.
  中文翻译：理解路径。输入图像 → SigLIP-SO400m → 2 层 MLP → Transformer 主体。
- Generation path. Input image (if conditioning on an existing image) → VQ tokenizer → token IDs → transformer body.
  中文翻译：生成路径。输入图像（如果以现有图像为条件）→ VQ 分词器 → token ID → Transformer 主体。
- Output generation. Image tokens predicted by the transformer → VQ decoder → pixels.
  中文翻译：输出生成。Transformer 预测的图像 token → VQ 解码器 → 像素。

The transformer body is shared. Everything upstream and downstream of the body is task-specific.

> Transformer 主体是共享的。主体上下游的所有内容都是任务特定的。

Inputs are disambiguated by prompt format: a `<understand>` tag routes through SigLIP; `<generate>` routes through VQ. Or the routing is implicit from task.

> 输入通过提示格式消歧：`<understand>` 标签路由到 SigLIP；`<generate>` 路由到 VQ。或者路由从任务隐式确定。

### Why this works

Understanding loss gets SigLIP features, which CLIP-style pretraining has tuned for semantic similarity. The model's perception benchmarks improve over Show-o / Transfusion because the input features are better for the task.

> 理解损失获得 SigLIP 特征，CLIP 风格的预训练已为语义相似性调优了这些特征。模型的感知基准测试超过 Show-o / Transfusion，因为输入特征更适合任务。

Generation loss gets VQ tokens, which a tokenizer has tuned for reconstruction. Image quality improves over Show-o because VQ codes compose back to pixels cleanly.

> 生成损失获得 VQ token，分词器已为重建调优了这些 token。图像质量超过 Show-o，因为 VQ 码能干净地组合回像素。

The shared transformer body sees two input distributions (SigLIP and VQ) and learns to work with both. The claim: enough data + enough parameters, the body absorbs the switching.

> 共享的 Transformer 主体看到两种输入分布（SigLIP 和 VQ），学会与两者一起工作。声称：足够的数据 + 足够的参数，主体能吸收切换。

### Data scaling — Janus vs Janus-Pro

Janus (original, arXiv 2410.13848) introduced the decoupling but at small scale (1.3B params, limited data). Janus-Pro (arXiv 2501.17811) scaled:

> Janus（原始版，arXiv 2410.13848）引入了解耦但规模较小（13 亿参数，有限数据）。Janus-Pro（arXiv 2501.17811）进行了扩展：

- 7B params (vs 1.3B).
  中文翻译：70 亿参数（对比 13 亿）。
- 90M image-text pairs for stage 1 (alignment) up from 72M.
  中文翻译：9000 万图文对用于第一阶段（对齐），从 7200 万提升。
- 72M for stage 2 (unified) up from 26M.
  中文翻译：7200 万用于第二阶段（统一），从 2600 万提升。
- Added 200k image-gen instruction samples for stage 3.
  中文翻译：为第三阶段增加了 20 万图像生成指令样本。

The upshot: Janus-Pro-7B matches LLaVA on MMMU (60.3 vs ~58) and beats DALL-E 3 on GenEval (0.80 vs 0.67). One open model, competitive on both sides of the unified spectrum.

> 结果：Janus-Pro-7B 在 MMMU 上匹配 LLaVA（60.3 vs ~58），在 GenEval 上击败 DALL-E 3（0.80 vs 0.67）。一个开放模型，在统一谱系的两端都有竞争力。

### JanusFlow — the rectified flow variant

JanusFlow (arXiv 2411.07975) swaps the VQ generation path for a rectified-flow generation path (continuous). The split becomes SigLIP-for-understanding + rectified-flow-for-generation. Quality ceilings lift further. The architecture remains decoupled-encoders-shared-body.

> JanusFlow（arXiv 2411.07975）将 VQ 生成路径替换为整流流生成路径（连续）。分离变成 SigLIP 用于理解 + 整流流用于生成。质量上限进一步提升。架构仍然是解耦编码器-共享主体。

### The shared body's job

The transformer body processes a unified sequence but with two input distributions. Its job is to:

> Transformer 主体处理统一序列但有两种输入分布。它的任务是：

- For understanding: consume SigLIP features + text tokens → emit text autoregressively.
  中文翻译：理解：消费 SigLIP 特征 + 文本 token → 自回归输出文本。
- For generation: consume text tokens + (optional image VQ tokens) → emit image VQ tokens autoregressively.
  中文翻译：生成：消费文本 token +（可选图像 VQ token）→ 自回归输出图像 VQ token。

The body has no modality-specific weights per block. It is the text-style transformer you'd expect to find inside Qwen or Llama, plus the two input adapters.

> 主体没有模态特定的权重。它就是你在 Qwen 或 Llama 中期望找到的文本风格 Transformer，加上两个输入适配器。

Interestingly, this means Janus-Pro's body could be initialized from a pretrained LLM. Janus-Pro does initialize from DeepSeek-MoE-7B. That choice matters: the LLM contributes reasoning ability that pure-from-scratch unified models struggle to reach.

> 有趣的是，这意味着 Janus-Pro 的主体可以从预训练的 LLM 初始化。Janus-Pro 确实从 DeepSeek-MoE-7B 初始化。这个选择很重要：LLM 贡献了从头训练的统一模型难以达到的推理能力。

### Compared to InternVL-U

InternVL-U (Lesson 12.10) is the 2026 follow-up. It combines:

> InternVL-U（第 12.10 课）是 2026 年的后续。它结合了：

- Native multimodal pretraining (InternVL3 backbone).
  中文翻译：原生多模态预训练（InternVL3 主干）。
- Decoupled-encoder routing (SigLIP in, VQ + diffusion heads out).
  中文翻译：解耦编码器路由（SigLIP 输入，VQ + 扩散头输出）。
- Unified understanding + generation + editing.
  中文翻译：统一理解 + 生成 + 编辑。

InternVL-U subsumes Janus-Pro's architectural choice into a larger framework. The decoupled-encoder idea is now the default for unified models at scale.

> InternVL-U 将 Janus-Pro 的架构选择纳入更大的框架。解耦编码器思想现在是大规模统一模型的默认选择。

### Limitations

Decoupled encoders add architectural complexity. Two tokenizers to train, two input paths to maintain, two sets of fail modes. For products that do not need generation, Janus-Pro is over-engineered — pick a LLaVA-family understanding model.

> 解耦编码器增加了架构复杂性。两个分词器要训练，两条输入路径要维护，两组失败模式。对于不需要生成的产品，Janus-Pro 过度工程化——选择 LLaVA 家族的理解模型。

For products that do not need understanding, Janus-Pro is overqualified — pick a Stable Diffusion 3 / Flux model.

> 对于不需要理解的产品，Janus-Pro 大材小用——选择 Stable Diffusion 3 / Flux 模型。

For products that need both, Janus-Pro is now the reference open architecture.

> 对于两者都需要的产品，Janus-Pro 现在是参考的开放架构。


> **【拓展：Janus-Pro 在基准上的表现】** Janus-Pro 在多模态理解基准上超越统一编码器的方案约 3-5%，在图像生成基准上超越约 10-15%。DeepSeek 的研究表明解耦编码器是同时做好理解和生成的最优解。


## Use It  | 动手实践

`code/main.py` simulates Janus-Pro routing:

> `code/main.py` 模拟 Janus-Pro 路由：

- Two mock encoders: SigLIP-like (produces 256-dim semantic vectors) and VQ-like (produces integer codes).
  中文翻译：两个模拟编码器：类 SigLIP（产生 256 维语义向量）和类 VQ（产生整数码）。
- A prompt router that picks the encoder based on a task tag.
  中文翻译：基于任务标签选择编码器的提示路由器。
- A shared body (stand-in) that processes token sequences regardless of which encoder produced them.
  中文翻译：共享主体（替代），处理 token 序列，无论来自哪个编码器。
- A switch from stage 1 (alignment) to stage 3 (instruction tune) weighted-sample schedule.
  中文翻译：从第一阶段（对齐）到第三阶段（指令微调）的加权采样调度切换。

Print the routed paths for 3 examples: image QA, T2I, image editing.

> 打印 3 个示例的路由路径：图像问答、T2I、图像编辑。

## Ship It  | 部署上线

This lesson produces `outputs/skill-decoupled-encoder-picker.md`. Given a product that wants unified generation + understanding at frontier-ish quality, it picks Janus-Pro, JanusFlow, or InternVL-U with a concrete data-scale recommendation.

> 本课产出 `outputs/skill-decoupled-encoder-picker.md`。给定需要前沿质量统一生成+理解的产品，它在 Janus-Pro、JanusFlow 或 InternVL-U 之间选择，附具体的数据规模建议。

## Exercises  | 练习题

1. Janus-Pro-7B beats DALL-E 3 on GenEval. Explain why a 7B open model can match a frontier proprietary model on generation but not on understanding.
   中文翻译：Janus-Pro-7B 在 GenEval 上击败 DALL-E 3。解释为什么 7B 开放模型能在生成上匹敌前沿专有模型，但在理解上不能。

2. Implement a router function: given prompt text, classify as `understand` or `generate`. How do you handle ambiguous prompts like "describe and then sketch"?
   中文翻译：实现路由函数：给定提示文本，分类为 `understand` 或 `generate`。如何处理模糊提示如"描述然后画出来"？

3. JanusFlow replaces the VQ path with rectified flow. What does the transformer body now output, and what changes in the loss?
   中文翻译：JanusFlow 用整流流替换 VQ 路径。Transformer 主体现在输出什么？损失有什么变化？

4. Propose a fourth task the Janus-Pro architecture could handle with one more decoupled encoder. Examples: image segmentation (DINO-style), depth (MiDaS-style).
   中文翻译：提出 Janus-Pro 架构通过增加一个解耦编码器可以处理的第四种任务。如：图像分割（DINO 风格）、深度（MiDaS 风格）。

5. Read Janus-Pro Section 4.2 on data scaling. Which data stage contributes most to the T2I quality gain vs Janus?
   中文翻译：阅读 Janus-Pro 第 4.2 节关于数据扩展。哪个数据阶段对 T2I 质量提升贡献最大？

## Key Terms  | 关键术语

| Term | What people say | What it actually means | 中文含义 | 中文释义 |
|------|-----------------|------------------------|---------|
| Decoupled encoding | "Two visual encoders" | Separate tokenizer or encoder per direction: semantic for understanding, reconstruction for generation | 每个方向使用独立的分词器或编码器：理解用语义，生成用重建 |
| Shared body | "One transformer" | Single transformer processes either encoder's output; no modality-specific weights | 单一 Transformer 处理任一编码器的输出；无模态特定权重 |
| SigLIP for understanding | "Semantic features" | CLIP-family vision tower providing rich conceptual features but poor reconstruction | CLIP 家族视觉塔，提供丰富的概念特征但重建能力差 |
| VQ for generation | "Reconstruction codes" | Vector-quantized tokens that decode cleanly back to pixels | 可干净解码回像素的向量量化 token |
| JanusFlow | "Rectified-flow variant" | Janus-Pro with a continuous flow-matching generation head instead of VQ | 使用连续流匹配生成头替代 VQ 的 Janus-Pro |
| Routing tag | "Task tag" | Prompt marker (`<understand>` / `<generate>`) that picks the input encoder | 选择输入编码器的提示标记 |

## Further Reading  | 延伸阅读

- [Wu et al. — Janus (arXiv:2410.13848)](https://arxiv.org/abs/2410.13848)
  中文翻译：Janus 论文。
- [Chen et al. — Janus-Pro (arXiv:2501.17811)](https://arxiv.org/abs/2501.17811)
  中文翻译：Janus-Pro 论文。
- [Ma et al. — JanusFlow (arXiv:2411.07975)](https://arxiv.org/abs/2411.07975)
  中文翻译：JanusFlow 论文。
- [InternVL-U (arXiv:2603.09877)](https://arxiv.org/abs/2603.09877)
  中文翻译：InternVL-U 论文。
- [Dong et al. — DreamLLM (arXiv:2309.11499)](https://arxiv.org/abs/2309.11499)
  中文翻译：DreamLLM 论文。
