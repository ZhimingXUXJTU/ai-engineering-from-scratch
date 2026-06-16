# Vision Transformers and the Patch-Token Primitive | 视觉 Transformer 与 Patch-Token 原语

> Before anything multimodal, an image has to become a sequence of tokens a transformer can eat. The 2020 ViT paper answered this with 16x16 pixel patches, a linear projection, and a position embedding. Five years later every 2026 frontier model (Claude Opus 4.7 at 2576px native, Gemini 3.1 Pro, Qwen3.5-Omni) still begins this way — the encoder changed from ViT to DINOv2 to SigLIP 2, register tokens were added, the positional scheme became 2D-RoPE, but the primitive held. This lesson reads the patch-token pipeline end to end and builds it in stdlib Python so the rest of Phase 12 has a concrete mental model for "visual tokens."

> **【中文解读】** 在进入多模态之前，图像必须先变成 Transformer 能处理的 token 序列。ViT 用16x16像素块+线性投影+位置编码实现了这一转换，至今仍是所有前沿模型的基础。

> **【拓展：ViT Patch→多模态基础】** Patch-Token 是所有视觉语言模型的基础——无论是 CLIP 的视觉编码器、LLaVA 的图像输入还是文档理解模型，都从 Patch 切分开始。

> 🔗 **【前置】** 学本节前请先掌握：(1) Phase 7·01-05（Transformer 基础）——理解 Self-Attention、Position Embedding；(2) Phase 4·03（CNNs）——理解卷积特征提取，对比 ViT 的 patch 方法；(3) Phase 10·01（Tokenizers）——理解文本 token，本节是其视觉对应；(4) numpy 矩阵运算。本节是 Phase 12 全部 25 节的基础，跳过会看不懂后续。

**Type:** Learn | **类型:** 学习
**Languages:** Python (stdlib, patch tokenizer + geometry calculator) | **语言:** Python（标准库，patch tokenizer + 几何计算器）
**Prerequisites:** Phase 7 (Transformers), Phase 4 (Computer Vision) | **前置知识:** Phase 7（Transformer），Phase 4（计算机视觉）
**Time:** ~120 minutes | **时间:** ~120 分钟

## Learning Objectives | 学习目标

- Convert an HxWx3 image into a sequence of patch tokens with correct positional encoding.
  中文翻译：将 HxWx3 图像转换为带有正确位置编码的 patch token 序列。
- Compute sequence length, parameter count, and FLOPs for a ViT of a given (patch size, resolution, hidden dim, depth).
  中文翻译：计算给定（patch 大小、分辨率、隐藏维度、深度）的 ViT 的序列长度、参数量和 FLOPs。
- Name the three upgrades that took ViT from 2020 research to 2026 production: self-supervised pretraining (DINO / MAE), register tokens, and native-resolution packing.
  中文翻译：列举将 ViT 从 2020 年研究推向 2026 年生产环境的三大升级：自监督预训练（DINO / MAE）、register token 和原生分辨率打包。
- Pick between CLS pooling, mean pooling, and register tokens for a downstream task.
  中文翻译：为下游任务选择 CLS 池化、均值池化或 register token。

## The Problem | 问题引入

Transformers operate on sequences of vectors. Text is already a sequence (bytes or tokens). An image is a 2D grid of pixels with three color channels — not a sequence. If you flatten every pixel, a 224x224 RGB image becomes 150,528 tokens, and self-attention at that length is a non-starter (quadratic in sequence length).

> Transformer 操作的是向量序列。文本本身就是序列（字节或 token），但图像是具有三个颜色通道的像素 2D 网格——不是序列。如果你展平每个像素，一张 224x224 的 RGB 图像变成 150,528 个 token，而在这个长度上做自注意力是不可行的（复杂度与序列长度呈二次关系）。

Pre-2020 approaches bolted a CNN feature extractor onto the front: ResNet produces a 7x7 feature map of 2048-dim vectors, feed those 49 tokens to a transformer. This works but inherits the CNN's biases (translation equivariance, local receptive fields) and loses the transformer's appetite for scale.

> 2020 年之前的方法是在前端接一个 CNN 特征提取器：ResNet 生成 7x7 的 2048 维向量特征图，将这 49 个 token 喂给 Transformer。这可行，但继承了 CNN 的归纳偏置（平移等变性、局部感受野），并丧失了 Transformer 对规模扩展的胃口。

Dosovitskiy et al. (2020) asked the blunt question: what if we skip the CNN? Split the image into fixed-size patches (say 16x16 pixels), linearly project each patch into a vector, add a positional embedding, and feed the sequence to a vanilla transformer. At the time this was heresy — vision without convolutions. With enough data (JFT-300M, then LAION) it beat ResNet on ImageNet and kept improving.

> Dosovitskiy 等人（2020）提出了一个直接的问题：如果我们跳过 CNN 呢？将图像分割为固定大小的 patch（比如 16x16 像素），线性投影每个 patch 为一个向量，加上位置编码，然后将序列喂给标准 Transformer。当时这被视为异端——没有卷积的视觉。但有了足够的数据（JFT-300M，后来是 LAION），它在 ImageNet 上超越了 ResNet 并持续改进。

By 2026 the ViT primitive is the unquestioned foundation. Every open-weights VLM's vision tower is some descendant (DINOv2, SigLIP 2, CLIP, EVA, InternViT). The question is no longer "should we use patches?" but "what patch size, what resolution schedule, what pretraining objective, what positional encoding."

> 到 2026 年，ViT 原语已成为无可争议的基础。每个开放权重的 VLM 的视觉塔都是其后代（DINOv2、SigLIP 2、CLIP、EVA、InternViT）。问题不再是"该不该用 patch？"而是"什么 patch 大小、什么分辨率调度、什么预训练目标、什么位置编码"。

## The Concept | 核心概念

> **【中文解读】** Vision Transformer (ViT) 将图像分割为固定大小的 patch（如 16x16 像素），每个 patch 展平后通过线性投影变成一个 token，然后像 NLP 中的 Transformer 一样处理。这是将 Transformer 架构引入计算机视觉的奠基性工作，取代了 CNN 成为视觉 backbone。

> **【拓展：ViT 的影响】** Dosovitskiy 等人 2020 年提出的 ViT 证明 Transformer 在图像分类上可以超越 CNN。ViT-L/14 在 ImageNet 上达到 88.5% top-1 准确率。ViT 是 CLIP、GPT-4V、Gemini 等多模态模型的视觉编码器基础。Swin Transformer 通过层级化窗口注意力解决了 ViT 对高分辨率图像的计算瓶颈。


> **【拓展：ViT 对 CNN 的优势】** ViT 的全局自注意力在数据量足够大时（如 JFT-300M 或 LAION-5B）显著优于 CNN 的局部感受野。ViT-H/14 在 ImageNet-21k 上预训练后，在多个下游任务上超越 EfficientNet 和 ResNet。ViT 也是 DINOv2（自监督视觉基础模型）的 backbone。


### Patches as tokens

Given an image `x` of shape `(H, W, 3)` and a patch size `P`, you carve the image into a grid of `(H/P) x (W/P)` non-overlapping patches. Each patch is a `P x P x 3` cube of pixels. Flatten each cube to a `3 P^2` vector. Apply a shared linear projection `W_E` of shape `(3 P^2, D)` to map each patch into the model's hidden dimension `D`.

> 给定形状为 `(H, W, 3)` 的图像 `x` 和 patch 大小 `P`，将图像切割为 `(H/P) x (W/P)` 个不重叠的 patch 网格。每个 patch 是一个 `P x P x 3` 的像素立方体。将每个立方体展平为 `3 P^2` 维向量。应用形状为 `(3 P^2, D)` 的共享线性投影 `W_E`，将每个 patch 映射到模型的隐藏维度 `D`。

For the ViT-B/16 canonical config:
- Resolution 224, patch size 16 → grid 14x14 → 196 patch tokens.
  中文翻译：分辨率 224，patch 大小 16 → 网格 14x14 → 196 个 patch token。
- Each patch is `16 x 16 x 3 = 768` pixel values, projected to `D = 768`.
  中文翻译：每个 patch 包含 `16 x 16 x 3 = 768` 个像素值，投影到 `D = 768`。
- Add a learnable `[CLS]` token → sequence length 197.
  中文翻译：添加一个可学习的 `[CLS]` token → 序列长度 197。

The patch projection is mathematically identical to a 2D convolution with kernel size `P`, stride `P`, and `D` output channels. That is how production code actually implements it — `nn.Conv2d(3, D, kernel_size=P, stride=P)`. The "linear projection" framing is conceptual; the kernel framing is efficient.

> Patch 投影在数学上等同于核大小为 `P`、步长为 `P`、输出通道为 `D` 的 2D 卷积。生产代码就是这样实现的——`nn.Conv2d(3, D, kernel_size=P, stride=P)`。"线性投影"是概念性的；卷积核的实现是高效的。

### Positional embeddings

Patches have no inherent order — the transformer sees them as a bag. Early ViTs added a learnable 1D positional embedding (one 768-dim vector per position, 197 of them). Works, but ties the model to the training resolution: at inference you have to interpolate the position table if you change the grid.

> Patch 没有固有顺序——Transformer 将它们视为一个无序集合。早期 ViT 添加了可学习的 1D 位置编码（每个位置一个 768 维向量，共 197 个）。有效，但将模型绑定到训练分辨率：推理时如果改变网格大小，必须对位置表进行插值。

Modern vision backbones use 2D-RoPE (Qwen2-VL's M-RoPE, SigLIP 2's default) or factorized 2D positions. 2D-RoPE rotates the query and key vectors based on the patch's (row, column) index, so the model infers relative 2D position from the rotation angle. No position table. The model handles arbitrary grid sizes at inference.

> 现代视觉主干网络使用 2D-RoPE（Qwen2-VL 的 M-RoPE、SigLIP 2 的默认方案）或分解式 2D 位置编码。2D-RoPE 根据 patch 的（行、列）索引旋转 query 和 key 向量，因此模型从旋转角度推断相对 2D 位置。无需位置表。模型在推理时可以处理任意网格大小。

### CLS token, pooled output, and register tokens

What is the image-level representation? Three choices coexist:

> 什么是图像级表示？三种选择并存：

1. `[CLS]` token. Prepend a learnable vector to the patch sequence. After all transformer blocks, the CLS token's hidden state is the image representation. Inherited from BERT. Used by original ViT, CLIP.
   中文翻译：`[CLS]` token。在 patch 序列前拼接一个可学习向量。所有 Transformer 块之后，CLS token 的隐藏状态就是图像表示。继承自 BERT。原始 ViT 和 CLIP 使用。
2. Mean pool. Average the patch tokens' output hidden states. Used by SigLIP, DINOv2, most modern VLMs.
   中文翻译：均值池化。对所有 patch token 的输出隐藏状态取平均。SigLIP、DINOv2 和大多数现代 VLM 使用。
3. Register tokens. Darcet et al. (2023) observed that ViTs trained without an explicit sink token develop high-norm "artifact" patches that hijack self-attention. Adding 4–16 learnable register tokens absorbs this load and improves dense-prediction quality (segmentation, depth). DINOv2 and SigLIP 2 both ship with registers.
   中文翻译：Register token。Darcet 等人（2023）观察到，没有显式汇聚 token 的 ViT 会产生高范数"伪影"patch，劫持自注意力。添加 4-16 个可学习的 register token 可以吸收这种负载，提高密集预测质量（分割、深度）。DINOv2 和 SigLIP 2 都带有 register。

The choice matters for downstream tasks. CLS is fine for classification. For VLMs that feed patch tokens into an LLM, you skip pooling entirely — every patch becomes an LLM input token. Registers get discarded before handoff (they are scaffolding, not content).

> 选择对下游任务很重要。CLS 适合分类。对于将 patch token 喂入 LLM 的 VLM，完全跳过池化——每个 patch 都成为 LLM 的输入 token。Register 在交接前被丢弃（它们是脚手架，不是内容）。

### Pretraining: supervised, contrastive, masked, self-distilled

The 2020 ViT was pretrained with supervised classification on JFT-300M. Quickly supplanted by:

> 2020 年的 ViT 在 JFT-300M 上用监督分类进行预训练。很快被以下方法取代：

- CLIP (2021): contrastive image-text on 400M pairs. Lesson 12.02.
  中文翻译：CLIP（2021）：4 亿对图像-文本的对比学习。第 12.02 课。
- MAE (2021, He et al.): mask 75% of patches, reconstruct pixels. Self-supervised, works on pure images.
  中文翻译：MAE（2021，He 等人）：遮蔽 75% 的 patch，重建像素。自监督，适用于纯图像。
- DINO (2021) / DINOv2 (2023): self-distillation with student-teacher, no labels, no captions. The 2023 DINOv2 ViT-g/14 is the strongest purely-visual backbone and the default for "dense features" use cases.
  中文翻译：DINO（2021）/ DINOv2（2023）：师生自蒸馏，无需标签、无需描述。2023 年的 DINOv2 ViT-g/14 是最强的纯视觉主干网络，也是"密集特征"用例的默认选择。
- SigLIP / SigLIP 2 (2023, 2025): CLIP with a sigmoid loss and NaFlex for native aspect ratio. The dominant vision tower in 2026 open VLMs (Qwen, Idefics2, LLaVA-OneVision).
  中文翻译：SigLIP / SigLIP 2（2023，2025）：使用 sigmoid 损失和 NaFlex 原生宽高比的 CLIP。2026 年开放 VLM（Qwen、Idefics2、LLaVA-OneVision）的主导视觉塔。

Your choice of pretraining determines what the backbone is good for: CLIP/SigLIP for semantic matching with text, DINOv2 for dense visual features, MAE as a starting point for downstream finetuning.

> 预训练方式决定主干网络擅长什么：CLIP/SigLIP 用于与文本的语义匹配，DINOv2 用于密集视觉特征，MAE 作为下游微调的起点。

### Scaling laws

ViT scaling (Zhai et al. 2022) established that a ViT's quality obeys predictable laws in model size, data size, and compute. At fixed compute:

> ViT 缩放定律（Zhai 等人，2022）确立了 ViT 的质量遵循关于模型大小、数据大小和计算量的可预测规律。在固定计算量下：

- Bigger model + more data → better quality.
  中文翻译：更大的模型 + 更多数据 → 更好的质量。
- Patch size is a lever on sequence length vs fidelity. Patch 14 (typical for DINOv2/SigLIP SO400m) gives more tokens per image than patch 16; better for OCR and dense tasks, worse for speed.
  中文翻译：Patch 大小是序列长度与保真度之间的杠杆。Patch 14（DINOv2/SigLIP SO400m 的典型配置）比 patch 16 每张图像产生更多 token；更适合 OCR 和密集任务，但速度更慢。
- Resolution is the other big lever. Going from 224 to 384 to 512 almost always helps, at quadratic cost in FLOPs.
  中文翻译：分辨率是另一个重要杠杆。从 224 提升到 384 再到 512 几乎总是有帮助，但 FLOPs 成本呈二次增长。

ViT-g/14 (1B params, patch 14, resolution 224 → 256 tokens) and SigLIP SO400m/14 (400M params, patch 14) are the two workhorse encoders for 2026 open VLMs.

> ViT-g/14（10 亿参数，patch 14，分辨率 224 → 256 个 token）和 SigLIP SO400m/14（4 亿参数，patch 14）是 2026 年开放 VLM 的两大主力编码器。

### Parameter count for a ViT

The full calculation lives in `code/main.py`. For ViT-B/16 at 224:

> 完整计算见 `code/main.py`。对于 ViT-B/16 在 224 分辨率下：

```
patch_embed = 3 * 16 * 16 * 768 + 768  =  591k
cls + pos    = 768 + 197 * 768          =  152k
block        = 4 * 768^2 (QKVO) + 2 * 4 * 768^2 (MLP) + 2 * 2*768 (LN)
             = 12 * 768^2 + 3k          =  7.1M
12 blocks    = 85M
final LN    = 1.5k
total       ≈ 86M
```

Ball-park every ViT this way before you load the checkpoint. The backbone size sets your VRAM floor in any downstream VLM.

> 在加载检查点之前，用这种方法估算每个 ViT。主干网络的大小决定了下游 VLM 的显存下限。

### 2026 production config

The encoder most open VLMs ship with in 2026 is SigLIP 2 SO400m/14 at native resolution (NaFlex). It has:

> 2026 年大多数开放 VLM 搭载的编码器是原生分辨率（NaFlex）的 SigLIP 2 SO400m/14。它具有：

- 400M parameters.
  中文翻译：4 亿参数。
- Patch size 14, default resolution 384 → 729 patch tokens per image.
  中文翻译：Patch 大小 14，默认分辨率 384 → 每张图像 729 个 patch token。
- Mean pool for image-level tasks; all 729 patches flow into the LLM for VQA.
  中文翻译：图像级任务使用均值池化；所有 729 个 patch 流入 LLM 进行视觉问答。
- 4 register tokens, discarded before LLM handoff.
  中文翻译：4 个 register token，在交给 LLM 前丢弃。
- 2D-RoPE with image-level scaling for native aspect ratio.
  中文翻译：2D-RoPE，带图像级缩放以支持原生宽高比。

Every decision in that config traces back to a paper you can read.

> 该配置中的每个决策都可以追溯到你可以阅读的论文。

## Use It | 用框架实现

`code/main.py` is a patch tokenizer and geometry calculator. It takes (image H, W, patch P, hidden D, depth L) and reports:

> `code/main.py` 是一个 patch tokenizer 和几何计算器。它接收（图像 H, W, patch P, 隐藏维度 D, 深度 L）并报告：

- Grid shape and sequence length after patching.
  中文翻译：Patch 切分后的网格形状和序列长度。
- Token sequence for a synthetic 8x8 pixel toy image (walk through the flatten + project path).
  中文翻译：合成 8x8 像素玩具图像的 token 序列（遍历展平 + 投影路径）。
- Parameter count broken down by patch embed, position embed, transformer blocks, and head.
  中文翻译：按 patch 嵌入、位置编码、Transformer 块和头分解的参数量。
- FLOPs per forward pass at the target resolution.
  中文翻译：目标分辨率下每次前向传播的 FLOPs。
- A comparison table across ViT-B/16 @ 224, ViT-L/14 @ 336, DINOv2 ViT-g/14 @ 224, SigLIP SO400m/14 @ 384.
  中文翻译：ViT-B/16 @ 224、ViT-L/14 @ 336、DINOv2 ViT-g/14 @ 224、SigLIP SO400m/14 @ 384 的对比表。

Run it. Match the parameter counts to the published numbers. Play with patch size and resolution to feel the token-count cost.

> 运行它。将参数量与发布的数据对比。调整 patch 大小和分辨率来感受 token 数量的成本。

## Ship It | 产出物

This lesson produces `outputs/skill-patch-geometry-reader.md`. Given a ViT config (patch size, resolution, hidden dim, depth), it produces a token-count, parameter-count, and VRAM estimate with justifications. Use this skill whenever you pick a vision backbone for a VLM — it prevents "the tokens exploded and my LLM context filled up" surprises.

> 本课产出 `outputs/skill-patch-geometry-reader.md`。给定 ViT 配置（patch 大小、分辨率、隐藏维度、深度），它生成 token 数量、参数量和显存估算及其依据。每当为 VLM 选择视觉主干网络时使用此 skill——它可以防止"token 数爆炸，LLM 上下文被填满"的意外。

## Exercises | 练习题

1. Compute the patch-token sequence length for Qwen2.5-VL at native 1280x720 input with patch size 14. How does that compare to a CLS-only representation?
   中文翻译：计算 Qwen2.5-VL 在原生 1280x720 输入、patch 大小 14 下的 patch-token 序列长度。与仅使用 CLS 的表示相比如何？

2. A 1080p frame (1920x1080) at patch 14 produces how many tokens? At 30 FPS over a 5-minute video, how many total visual tokens? Which cost saves you most: pooling, frame sampling, or token merging?
   中文翻译：一帧 1080p 图像（1920x1080）在 patch 14 下产生多少 token？以 30 FPS 播放 5 分钟视频，总共多少视觉 token？哪种方法最节省成本：池化、帧采样还是 token 合并？

3. Implement mean pooling over patch tokens in pure Python. Verify that mean-pool over 196 tokens of a DINOv2 output matches what the model's `forward` returns when you ask for a pooled embedding.
   中文翻译：用纯 Python 实现 patch token 的均值池化。验证对 DINOv2 输出的 196 个 token 做均值池化是否与模型 `forward` 返回的池化嵌入一致。

4. Read Section 3 of "Vision Transformers Need Registers" (arXiv:2309.16588). Describe in two sentences what artifact the registers absorb and why it matters for downstream dense prediction.
   中文翻译：阅读"Vision Transformers Need Registers"（arXiv:2309.16588）第 3 节。用两句话描述 register 吸收了什么伪影，以及为什么这对下游密集预测很重要。

5. Modify `code/main.py` to support patch-n'-pack: given a list of images of different resolutions, produce a single packed sequence and the block-diagonal attention mask. Verify against Lesson 12.06 when you reach it.
   中文翻译：修改 `code/main.py` 以支持 patch-n'-pack：给定一组不同分辨率的图像，生成一个打包序列和块对角注意力掩码。在学习第 12.06 课时验证。

## Key Terms | 术语速查表

| Term | What people say | What it actually means | 中文释义 |
|------|----------------|------------------------|---------|
| 术语 | 通俗说法 | 实际含义 | |
| Patch | "16x16 pixel square" | A fixed-size non-overlapping region of the input image; becomes one token | 固定大小的非重叠图像区域；成为一个 token |
| Patch embedding | "Linear projection" | A shared learned matrix (or Conv2d with stride=P) mapping flattened patch pixels to D-dim vectors | 共享的学习矩阵（或步长为 P 的 Conv2d），将展平的 patch 像素映射为 D 维向量 |
| CLS token | "Class token" | Prepended learnable vector whose final hidden state represents the whole image; optional in 2026 | 前置可学习向量，其最终隐藏状态代表整张图像；2026 年可选 |
| Register token | "Sink token" | Extra learnable tokens that absorb the high-norm attention artifacts ViTs develop during pretraining | 额外可学习 token，吸收 ViT 预训练中产生的高范数注意力伪影 |
| Position embedding | "Positional info" | Per-position vector or rotation making the sequence-order-aware; 2D-RoPE is the modern default | 每个位置的向量或旋转，使序列具有顺序感知；2D-RoPE 是现代默认方案 |
| Grid | "Patch grid" | The (H/P) x (W/P) 2D array of patches for a given resolution and patch size | 给定分辨率和 patch 大小下的 (H/P) x (W/P) 2D patch 数组 |
| NaFlex | "Native flexible resolution" | SigLIP 2 feature: single model serves multiple aspect ratios and resolutions without retraining | SigLIP 2 特性：单一模型服务多种宽高比和分辨率，无需重新训练 |
| Backbone | "Vision tower" | The pretrained image encoder whose patch-token outputs feed the LLM in a VLM | 预训练的图像编码器，其 patch-token 输出喂入 VLM 中的 LLM |
| Pooling | "Image-level summary" | Strategy to turn patch tokens into one vector: CLS, mean, attention pool, or register-based | 将 patch token 转为一个向量的策略：CLS、均值、注意力池化或基于 register |
| Patch 14 vs 16 | "Finer vs coarser grid" | Patch 14 produces more tokens per image, better fidelity for OCR, slower; patch 16 is the classic default | Patch 14 每张图产生更多 token，OCR 保真度更高但更慢；patch 16 是经典默认值 |

## Further Reading | 延伸阅读

- [Dosovitskiy et al. — An Image is Worth 16x16 Words (arXiv:2010.11929)](https://arxiv.org/abs/2010.11929) — original ViT.
  中文翻译：原始 ViT 论文。
- [He et al. — Masked Autoencoders Are Scalable Vision Learners (arXiv:2111.06377)](https://arxiv.org/abs/2111.06377) — MAE, self-supervised pretraining.
  中文翻译：MAE，自监督预训练。
- [Oquab et al. — DINOv2 (arXiv:2304.07193)](https://arxiv.org/abs/2304.07193) — self-distillation at scale, no labels.
  中文翻译：大规模自蒸馏，无需标签。
- [Darcet et al. — Vision Transformers Need Registers (arXiv:2309.16588)](https://arxiv.org/abs/2309.16588) — register tokens and artifact analysis.
  中文翻译：Register token 和伪影分析。
- [Tschannen et al. — SigLIP 2 (arXiv:2502.14786)](https://arxiv.org/abs/2502.14786) — the 2026 default vision tower.
  中文翻译：2026 年默认的视觉塔。
- [Zhai et al. — Scaling Vision Transformers (arXiv:2106.04560)](https://arxiv.org/abs/2106.04560) — empirical scaling laws.
  中文翻译：经验缩放定律。
