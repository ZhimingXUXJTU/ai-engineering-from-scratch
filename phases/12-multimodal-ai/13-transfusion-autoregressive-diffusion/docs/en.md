# Transfusion: Autoregressive Text + Diffusion Image in One Transformer | Transfusion：一个 Transformer 兼做自回归文本和扩散图像

> Chameleon and Emu3 bet everything on discrete tokens. They work, but the quantization bottleneck is visible — the image quality plateaus below continuous-space diffusion models. Transfusion (Meta, Zhou et al., August 2024) takes the opposite bet: keep images continuous, drop the VQ-VAE entirely, and train one transformer with two losses. Text tokens get next-token-prediction. Image patches get a flow-matching / diffusion loss. Both objectives optimize the same weights. The architecture underlying Stable Diffusion 3 (MMDiT) is a close cousin. This lesson reads the Transfusion thesis, builds a toy two-loss trainer, and traces the attention mask that lets one transformer do both jobs.

> **【中文解读】** Transfusion（Meta，2024年8月）选择了与 Chameleon/Emu3 相反的路径：保持图像为连续表示，不用 VQ-VAE，用一个 Transformer 同时跑两个损失——文本 token 用下一 token 预测，图像补丁用流匹配/扩散损失。Stable Diffusion 3 的 MMDiT 架构就是近亲。

> **【拓展：双损失训练的工程挑战】** Transfusion 的核心难点在于平衡两个数值尺度不同的损失函数。NTP 损失和扩散 MSE 损失的量级差异可能导致一个损失主导训练。实际部署中需要仔细调整损失权重。MMDiT 通过模态特定权重缓解了这个问题。

**Type:** Build  | **类型:** 构建
**Languages:** Python (stdlib, two-loss trainer on MNIST-scale toy) | **语言:** Python（标准库，MNIST 规模玩具的双损失训练器）
**Prerequisites:** Phase 12 · 11 (Chameleon), Phase 8 (Generative AI) | **前置知识:** Phase 12 · 11（Chameleon），Phase 8（生成式 AI）
**Time:** ~180 minutes | **时间:** ~180 分钟

> 🔗 **【前置】** 学本节前请先掌握：Phase 12·11（Chameleon 离散 token）、Phase 12·12（Emu3 next-token 生成）、Phase 8·01-03（扩散模型 / Flow Matching）。Transfusion = 两套思路的融合：文本离散 + 图像连续，一个 Transformer 两个损失。
> 💡 **【类比】** Transfusion = "双拼户型"。Chameleon = 一居室（所有内容用同一种 token）；LLaVA = 联排别墅（视觉和文本完全分开，靠桥接连接）；Transfusion = 双拼（一边文本 next-token loss，一边图像扩散 loss，共享承重墙 = 同一个 Transformer 骨干）。两个损失共同优化一套参数，保留各自模态的优势。
> ⚠️ **【易错点】** 两个损失直接相加而不调权重 → 一个损失主导训练（通常扩散 MSE 数值大，文本 NTP 被淹没）。修复：用 loss weighting（如 λ_text=1.0, λ_image=0.1）或 GradNorm 自适应平衡。

## Learning Objectives  | 学习目标

- Wire a transformer that runs two losses (NTP on text tokens, diffusion MSE on image patches) on one backbone.
  > 构建一个能在同一骨干上跑两个损失（文本 token NTP + 图像 patch 扩散 MSE）的 Transformer。
- Explain why bidirectional attention across image patches plus causal attention over text tokens is the right mask choice.
  > 解释为什么"图像 patch 双向 + 文本 token 因果"是正确的掩码选择。
- Compare Transfusion-style (continuous images, diffusion loss) to Chameleon-style (discrete images, NTP) on compute, quality, and code complexity.
  > 比较 Transfusion 风格（连续图像、扩散损失）与 Chameleon 风格（离散图像、NTP）在算力、质量和代码复杂度上的差异。
- Name MMDiT's contribution: modality-specific weights at each block, joint attention at the residual stream.
  > 列举 MMDiT 的贡献：每个块的模态特定权重、残差流的联合注意力。

## The Problem  | 问题背景

The discrete vs continuous image tokens debate is older than LLMs. Continuous representations (raw pixels, VAE latents) preserve detail. Discrete tokens (VQ indices) fit the transformer's native vocabulary but lose detail at the quantization step.

> 离散与连续图像 token 的争论比 LLM 更早。连续表示（原始像素、VAE 潜变量）保留细节。离散 token（VQ 索引）适合 Transformer 的原生词汇表，但在量化步骤中损失细节。

Chameleon / Emu3 went discrete: one loss, one architecture, but image fidelity capped by tokenizer quality.

> Chameleon / Emu3 选择离散：一个损失，一个架构，但图像保真度受限于分词器质量。

Diffusion models went continuous: exceptional image quality, but a separate model from the LLM, complex noise-schedule engineering, and no clean integration with text generation.

> 扩散模型选择连续：卓越的图像质量，但与 LLM 是独立模型，需要复杂的噪声调度工程，无法与文本生成干净集成。

Transfusion asks: can we have both? Keep images continuous, still train one model, use two losses stitched into one gradient step.

> Transfusion 问：能否兼得两者？保持图像连续，仍然训练一个模型，用两个损失拼接到一个梯度步骤中。

## The Concept  | 核心概念

> **【中文解读】** TransFusion（Meta）将自回归文本生成和扩散模型图像生成融合在同一个 Transformer 中：文本 token 使用 next-token prediction loss，图像 token 使用扩散 loss。两种模态共享同一模型参数但使用不同训练目标。

> **【拓展：多模态训练目标的融合】** TransFusion 证明自回归和扩散可以在同一模型中和谐共存。推理时文本部分自回归生成，遇到图像 token 时切换到扩散去噪过程。


### The two-loss architecture

A single decoder-only transformer processes a sequence that contains:

> 单一解码器 Transformer 处理包含以下内容的序列：

- Text tokens (discrete, from BPE vocab).
  中文翻译：文本 token（离散，来自 BPE 词汇表）。
- Image patches (continuous, 16x16 pixel blocks projected into hidden dim via linear embedding — same as a ViT encoder's input).
  中文翻译：图像 patch（连续，16x16 像素块通过线性嵌入投影到隐藏维度——与 ViT 编码器输入相同）。
- `<image>` and `</image>` tags marking where continuous patches live.
  中文翻译：`<image>` 和 `</image>` 标签标记连续 patch 的位置。

Forward pass runs once. The loss picks one of two heads per token:

> 前向传播运行一次。损失为每个 token 选择两个头之一：

- For text tokens: standard cross-entropy on the vocab-logits head.
  中文翻译：文本 token：词汇表 logits 头上的标准交叉熵。
- For image patches: diffusion loss on continuous patches — predict the noise that was added to each patch.
  中文翻译：图像 patch：连续 patch 上的扩散损失——预测每个 patch 添加的噪声。

The gradient flows through the shared transformer body. Both losses improve the shared weights simultaneously.

> 梯度通过共享的 Transformer 体回流。两个损失同时改进共享权重。

### Attention mask: causal text + bidirectional image

Text tokens must be causal — you cannot let a text token attend to future text, or teacher forcing breaks. Image patches, however, represent one snapshot; they should attend to each other bidirectionally within the same image block.

> 文本 token 必须是因果的——不能让文本 token 关注未来文本，否则教师强制会失败。但图像 patch 代表一个快照；它们应该在同一个图像块内双向关注彼此。

The mask:

> 掩码：

```
M[i, j] = 1 if:
  (i is text and j is text and j <= i)   # causal for text
  OR (i is image and j is image and same_image_block(i, j))   # bidirectional within image
  OR (i is text and j is image and j < i_image_end)   # text attends to previous images
  OR (i is image and j is text and j < i_image_start)   # image attends to preceding text
```

Implemented as a block-triangular mask at training and inference.

> 在训练和推理时实现为块三角掩码。

### Diffusion loss inside the transformer

The diffusion loss is standard: add noise to an image patch, ask the model to predict the noise (or the clean patch, equivalently). Transfusion's version uses flow matching — predict the velocity field from noisy to clean.

> 扩散损失是标准的：给图像 patch 添加噪声，让模型预测噪声（或等价地预测干净 patch）。Transfusion 版本使用流匹配——预测从噪声到干净的速度场。

During training:
1. For each image patch x0, sample a random timestep t.
   中文翻译：对每个图像 patch x0，采样随机时间步 t。
2. Sample noise ε, compute xt = (1-t) * x0 + t * ε (linear interpolation for flow matching).
   中文翻译：采样噪声 ε，计算 xt = (1-t) * x0 + t * ε（流匹配的线性插值）。
3. The transformer predicts v_theta(xt, t); loss = MSE(v_theta(xt, t), ε - x0).
   中文翻译：Transformer 预测 v_theta(xt, t)；损失 = MSE(v_theta(xt, t), ε - x0)。
4. Backprop alongside text NTP losses from the same sequence.
   中文翻译：与同序列的文本 NTP 损失一起反向传播。

At inference, generation is:
- Text tokens: standard autoregressive sampling.
  中文翻译：文本 token：标准自回归采样。
- Image patches: diffusion sampling loop (10-30 steps typical) conditioned on the prior text tokens.
  中文翻译：图像 patch：以先前文本 token 为条件的扩散采样循环（通常 10-30 步）。

### MMDiT: Stable Diffusion 3's variant

Stable Diffusion 3 (Esser et al., March 2024) shipped MMDiT (Multimodal Diffusion Transformer) around the same time as Transfusion. The architectures are siblings.

> Stable Diffusion 3（Esser 等人，2024 年 3 月）发布了 MMDiT（多模态扩散 Transformer），与 Transfusion 差不多同时。两者架构是兄弟。

MMDiT's key differences:

> MMDiT 的关键区别：

- Modality-specific weights per block. Each transformer block has separate Q, K, V, and MLP weights for text tokens vs image patches. Attention is joint (cross-modality); everything else is modality-specific.
  中文翻译：每个块的模态特定权重。每个 Transformer 块有独立的文本 token vs 图像 patch 的 Q、K、V 和 MLP 权重。注意力是联合的（跨模态）；其余都是模态特定的。
- Rectified flow training. A specific flow-matching variant with known sampling and simpler math than DDPM.
  中文翻译：整流流训练。一种特定的流匹配变体，采样已知，数学比 DDPM 更简单。
- Scale. MMDiT is the backbone for SD3 (2B and 8B param variants). Transfusion's paper scales to 7B.
  中文翻译：规模。MMDiT 是 SD3 的主干（20 亿和 80 亿参数变体）。Transfusion 论文扩展到 70 亿。

Both converge on the same core idea: one transformer runs NTP on text and diffusion on continuous image representations.

> 两者收敛到同一核心理念：一个 Transformer 在文本上运行 NTP，在连续图像表示上运行扩散。

### Why this beats Chameleon-style

The quality gap between continuous-diffusion and discrete-NTP on image generation is measurable. Transfusion paper reports:

> 连续扩散和离散 NTP 在图像生成上的质量差距是可量化的。Transfusion 论文报告：

- At 7B params, beats a same-size Chameleon-style model on FID by 3-5 points.
  中文翻译：70 亿参数下，FID 上击败同规模的 Chameleon 风格模型 3-5 分。
- No tokenizer training required — the image encoder is simpler (Linear projection to hidden, same as a ViT's input layer).
  中文翻译：不需要分词器训练——图像编码器更简单（线性投影到隐藏层，与 ViT 输入层相同）。
- Inference can parallelize image patch denoising, unlike autoregressive image tokens.
  中文翻译：推理可以并行化图像 patch 去噪，不同于自回归图像 token。

Downside: Transfusion is a dual-loss model, making training dynamics trickier. Loss weights need tuning. Schedule mismatch between NTP and diffusion can cause one head to dominate.

> 缺点：Transfusion 是双损失模型，训练动态更复杂。损失权重需要调优。NTP 和扩散之间的调度不匹配可能导致一个头主导。

### What sits downstream

Janus-Pro (Lesson 12.15) refines Transfusion's idea by decoupling the vision encoder for understanding and generation — SigLIP for one, VQ for the other — while sharing the transformer body. Show-o (Lesson 12.14) swaps diffusion for discrete-diffusion (masked prediction). The unified-generation family branches rapidly after Transfusion.

> Janus-Pro（第 12.15 课）通过解耦视觉编码器改进了 Transfusion 的思想——SigLIP 用于理解，VQ 用于生成——同时共享 Transformer 主体。Show-o（第 12.14 课）将扩散替换为离散扩散（掩码预测）。统一生成家族在 Transfusion 之后迅速分化。

2026 production VLMs that emit images — Gemini 3 Pro, GPT-5, Claude Opus 4.7's image generation path — almost certainly use some descendant of this family. Details are proprietary.

> 2026 年生成图像的生产 VLM——Gemini 3 Pro、GPT-5、Claude Opus 4.7 的图像生成路径——几乎可以确定使用了这个家族的某种后代。细节是专有的。


> **【拓展：TransFusion 的推理过程】** TransFusion 推理时的关键步骤：文本 token 自回归生成，遇到图像开始标记时切换到扩散模式。扩散过程在 token 空间而非像素空间进行，与文本生成共享同一个模型参数。


## Use It  | 动手实践

`code/main.py` builds a toy Transfusion on a tiny MNIST-like problem:

> `code/main.py` 在微型 MNIST 问题上构建玩具 Transfusion：

- Text captions are short integer sequences describing a digit (0-9).
  中文翻译：文本描述是描述数字（0-9）的短整数序列。
- Images are 4x4 grids of bytes.
  中文翻译：图像是 4x4 字节网格。
- A pair of shared-weight linear projections acts as the transformer stand-in; NTP loss on text, MSE loss on noisy patches.
  中文翻译：一对共享权重的线性投影作为 Transformer 替代；文本用 NTP 损失，噪声 patch 用 MSE 损失。
- Training loop alternates the two losses, attention mask is explicit.
  中文翻译：训练循环交替两个损失，注意力掩码是显式的。
- Generation produces a text caption and a 4x4 image in one forward pass.
  中文翻译：生成在一次前向传播中产生文本描述和 4x4 图像。

The transformer is a toy. The two-loss plumbing, attention mask construction, and inference loop are the real artifacts.

> Transformer 是玩具级的。双损失管线、注意力掩码构建和推理循环才是真正的产物。

## Ship It  | 部署上线

This lesson produces `outputs/skill-two-loss-trainer-designer.md`. Given a new multimodal training task (text + image, text + audio, text + video), it designs the two-loss schedule (loss weights, mask shape, shared vs modality-specific blocks) and flags implementation risks.

> 本课产出 `outputs/skill-two-loss-trainer-designer.md`。给定新的多模态训练任务（文本+图像、文本+音频、文本+视频），它设计双损失调度（损失权重、掩码形状、共享 vs 模态特定块）并标记实现风险。

## Exercises  | 练习题

1. A Transfusion-style model trains 70% text tokens and 30% image patches. The image diffusion loss is ~10x the text NTP loss in magnitude. What loss weights balance them?
   中文翻译：Transfusion 风格模型训练 70% 文本 token 和 30% 图像 patch。图像扩散损失在量级上约为文本 NTP 损失的 10 倍。什么损失权重能平衡它们？

2. Implement the block-triangular mask for a sequence: `[T, T, <image>, P, P, P, P, </image>, T]`. Mark each entry 0 or 1.
   中文翻译：为序列 `[T, T, <image>, P, P, P, P, </image>, T]` 实现块三角掩码。标记每个条目为 0 或 1。

3. MMDiT has modality-specific QKV weights. What parameter count overhead does this add vs Transfusion's fully-shared transformer? At 7B params, is it worth it?
   中文翻译：MMDiT 有模态特定的 QKV 权重。相比 Transfusion 的全共享 Transformer 增加了多少参数？70 亿参数下值得吗？

4. Generation: given a text prompt, the model runs NTP for 50 tokens, then hits `<image>`, then runs diffusion on 256 patches over 20 denoise steps. How many forward passes total?
   中文翻译：生成：给定文本提示，模型运行 NTP 50 个 token，然后遇到 `<image>`，然后在 256 个 patch 上运行 20 步去噪扩散。总共多少次前向传播？

5. Read SD3 paper Section 3. Describe rectified flow and why it converges in fewer inference steps than DDPM.
   中文翻译：阅读 SD3 论文第 3 节。描述整流流以及为什么它比 DDPM 在更少推理步骤中收敛。

## Key Terms  | 关键术语

| Term | What people say | What it actually means | 中文含义 | 中文释义 |
|------|-----------------|------------------------|---------|
| Two-loss training | "NTP + diffusion" | A single transformer optimizes both cross-entropy on text tokens and MSE on continuous image patches in the same gradient step | 单一 Transformer 在同一梯度步中优化文本 token 交叉熵和连续图像 patch MSE |
| Flow matching | "Rectified flow" | Diffusion variant that predicts a velocity field from noise to clean data; simpler math than DDPM | 预测从噪声到干净数据速度场的扩散变体；数学比 DDPM 更简单 |
| MMDiT | "Multimodal DiT" | Stable Diffusion 3's architecture: joint attention, modality-specific MLPs and norms | SD3 架构：联合注意力、模态特定 MLP 和归一化 |
| Block-triangular mask | "Causal text + bidirectional image" | Attention mask that is causal across text but bidirectional within image regions | 文本因果、图像区域内双向的注意力掩码 |
| Continuous image representation | "No VQ" | Image patches as real-valued vectors, not integer codebook indices | 图像 patch 为实值向量，非整数码本索引 |
| Velocity prediction | "v-parameterization" | Network output is the velocity field between noise and data, not the noise itself | 网络输出为噪声和数据之间的速度场，非噪声本身 |

## Further Reading  | 延伸阅读

- [Zhou et al. — Transfusion (arXiv:2408.11039)](https://arxiv.org/abs/2408.11039)
  中文翻译：Transfusion 论文。
- [Esser et al. — Stable Diffusion 3 / MMDiT (arXiv:2403.03206)](https://arxiv.org/abs/2403.03206)
  中文翻译：Stable Diffusion 3 / MMDiT 论文。
- [Peebles & Xie — DiT (arXiv:2212.09748)](https://arxiv.org/abs/2212.09748)
  中文翻译：DiT 扩散 Transformer 论文。
- [Zhao et al. — MonoFormer (arXiv:2409.16280)](https://arxiv.org/abs/2409.16280)
  中文翻译：MonoFormer 论文。
- [Xie et al. — Show-o (arXiv:2408.12528)](https://arxiv.org/abs/2408.12528)
  中文翻译：Show-o 论文。
