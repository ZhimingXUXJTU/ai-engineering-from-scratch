# Vision Transformers (ViT) | 视觉 Transformer (ViT)

> An image is a grid of patches. A sentence is a grid of tokens. The same transformer eats both.

> **【中文解读】** ViT 把图像切成 patch 当作 token 序列处理。理解 ViT = 理解 Transformer 不限于 NLP。CLIP、DALL-E、Sora 都基于 Transformer。

**Type:** Hands-on | **类型:** 动手
**Language:** Python | **语言:** Python
**Prerequisites:** Phase 7 · 05 (Full Transformer), Phase 4 · 03 (CNNs), Phase 4 · 14 (Vision Transformers intro) | **前置知识:** Phase 7 · 05 (Full Transformer), Phase 4 · 03 (CNNs), Phase 4 · 14 (Vision Transformers intro)
**Time:** ~45 minutes | **时间:** ~45 分钟

## The Problem | 问题引入

Before 2020, computer vision meant convolutions. Every SOTA on ImageNet, COCO, and detection benchmarks used a CNN backbone. Transformers were for language.

> 2020 年之前，计算机视觉意味着卷积。ImageNet、COCO 和检测基准上的每个 SOTA 都使用 CNN 骨干网络。Transformer 是用于语言处理的。

Dosovitskiy et al. (2020) — "An Image is Worth 16x16 Words" — showed you can drop the convolutions entirely. Slice an image into fixed-size patches, linearly project each patch into an embedding, feed the sequence to a vanilla transformer encoder. At sufficient scale (ImageNet-21k pretraining or bigger), ViT matches or beats ResNet-based models.

> Dosovitskiy 等人（2020）——"一张图像值 16x16 个词"——证明可以完全放弃卷积。将图像切成固定大小的 patch，线性投影每个 patch 为嵌入，将序列送入标准 Transformer 编码器。在足够大的规模下（ImageNet-21k 预训练或更大），ViT 可以匹配或超越基于 ResNet 的模型。

ViT was the start of a broader pattern in 2026: one architecture, many modalities. Whisper tokenizes audio. ViT tokenizes images. Action tokens for robotics. Pixel tokens for video. The transformer doesn't care — feed it a sequence and it learns.

> ViT 是 2026 年更广泛趋势的起点：一种架构，多种模态。Whisper 将音频 token 化。ViT 将图像 token 化。机器人的动作 token。视频的像素 token。Transformer 不在乎——给它一个序列，它就能学习。

By 2026, ViT and its descendants (DeiT, Swin, DINOv2, ViT-22B, SAM 3) own most of vision. CNNs still win on edge devices and latency-sensitive tasks. Everything else has a ViT somewhere in the stack.

> 到 2026 年，ViT 及其后继者（DeiT、Swin、DINOv2、ViT-22B、SAM 3）占据了视觉领域的大部分。CNN 在边缘设备和延迟敏感任务上仍然胜出。其他场景的某处都有 ViT。

> **【中文解读】** ViT 的核心洞察：图像可以像文本一样被切成"token"序列。将 224x224 图像切成 14x14 个 16x16 patch，每个 patch 展平后线性投影为嵌入向量，然后送入标准 Transformer 编码器。这证明了 Transformer 的通用性——不限于 NLP，任何可以"分块序列化"的数据都适用。

## The Concept | 核心概念

![Image → patches → tokens → transformer](../assets/vit.svg)

### Step 1 — patchify

Split a `H × W × C` image into an `N × (P·P·C)` sequence of flat patches. Typical setup: `224 × 224` image, `16 × 16` patches → 196 patches of 768 values each.

> 将 `H × W × C` 图像分割为 `N × (P·P·C)` 的扁平 patch 序列。典型设置：`224 × 224` 图像，`16 × 16` patch → 196 个 768 值的 patch。

```
image (224, 224, 3) → 14 × 14 grid of 16x16x3 patches → 196 vectors of length 768
```

Patch size is the lever. Smaller patches = more tokens, better resolution, quadratic attention cost. Larger patches = coarser, cheaper.

> Patch 大小是控制参数。更小的 patch = 更多 token、更好的分辨率、二次注意力成本。更大的 patch = 更粗糙、更廉价。

### Step 2 — linear embedding

A single learned matrix projects each flat patch to `d_model`. Equivalent to a convolution of kernel size `P` and stride `P`. In PyTorch this is literally `nn.Conv2d(C, d_model, kernel_size=P, stride=P)` — a 2-line implementation.

> 一个学习到的矩阵将每个扁平 patch 投影到 `d_model`。等价于核大小为 `P`、步长为 `P` 的卷积。在 PyTorch 中就是 `nn.Conv2d(C, d_model, kernel_size=P, stride=P)`——两行实现。

> **【拓展：Swin Transformer 的层级设计】** 标准 ViT 使用固定 patch 大小和全局注意力，计算量 O(N^2)。Swin Transformer 引入层级结构：在小 patch 上做局部窗口注意力，逐层合并 patch 扩大感受野。这使得计算复杂度变为 O(N)，同时保留了层级特征提取的能力。Swin 在检测和分割任务上仍优于标准 ViT。

### Step 3 — prepend `[CLS]` token, add positional embeddings

- Prepend a learnable `[CLS]` token. Its final hidden state is the image representation used for classification.
  中文翻译：在开头添加一个可学习的 `[CLS]` token。其最终隐藏状态用于分类的图像表示。
- Add learnable positional embeddings (ViT-original) or sinusoidal 2D (later variants).
  中文翻译：添加可学习的位置嵌入（ViT 原始版）或正弦 2D 嵌入（后续变体）。
- In 2024+ RoPE extended to 2D for position, sometimes without explicit embeddings.
  中文翻译：2024 年之后，RoPE 扩展到 2D 位置编码，有时不需要显式嵌入。

### Step 4 — standard transformer encoder

Stack L blocks of `LayerNorm → Self-Attention → + → LayerNorm → MLP → +`. Identical to BERT. No vision-specific layers. This is the pedagogical punchline of the paper.

> 堆叠 L 个 `LayerNorm → Self-Attention → + → LayerNorm → MLP → +` 块。与 BERT 完全相同。没有视觉特有的层。这是这篇论文的教学要点。

### Step 5 — head

For classification: take `[CLS]` hidden state → linear → softmax. For DINOv2 or SAM, discard `[CLS]`, use the patch embeddings directly.

> 分类：取 `[CLS]` 隐藏状态 → 线性层 → softmax。对于 DINOv2 或 SAM，丢弃 `[CLS]`，直接使用 patch 嵌入。

### Variants that mattered

| Model | Year | Change |
|-------|------|--------|
| 模型 | 年份 | 变化 |
| ViT | 2020 | The original. Fixed patch size, full global attention. |
| ViT | 2020 | 原始版本。固定 patch 大小，全局注意力。 |
| DeiT | 2021 | Distillation; trainable on ImageNet-1k only. |
| DeiT | 2021 | 蒸馏；仅在 ImageNet-1k 上可训练。 |
| Swin | 2021 | Hierarchical with shifted windows. Fixed sub-quadratic cost. |
| Swin | 2021 | 层级结构，移位窗口。固定的亚二次成本。 |
| DINOv2 | 2023 | Self-supervised (no labels). Best general vision features. |
| DINOv2 | 2023 | 自监督（无标签）。最佳通用视觉特征。 |
| ViT-22B | 2023 | 22B params; scaling laws apply. |
| ViT-22B | 2023 | 22B 参数；缩放定律适用。 |
| SigLIP | 2023 | ViT + language pair, sigmoid contrastive loss. |
| SigLIP | 2023 | ViT + 语言配对，sigmoid 对比损失。 |
| SAM 3 | 2025 | Segment anything; ViT-Large + promptable mask decoder. |
| SAM 3 | 2025 | 分割一切；ViT-Large + 可提示的掩码解码器。 |

### Why it took a while

ViT needs *a lot* of data to match CNNs because it has none of the CNN inductive biases (translation invariance, locality). Without >100M labeled images or strong self-supervised pretraining, CNNs still win at matched compute. DeiT fixed this in 2021 with distillation tricks; DINOv2 fixed it permanently in 2023 with self-supervision.

> ViT 需要大量数据才能匹配 CNN 的性能，因为它没有 CNN 的归纳偏好（平移不变性、局部性）。没有 1 亿张以上的标注图像或强自监督预训练，CNN 在相同计算量下仍然胜出。DeiT 在 2021 年通过蒸馏技巧解决了这个问题；DINOv2 在 2023 年通过自监督永久解决了它。

> **【中文解读】** ViT 的弱归纳偏好是双刃剑：需要更多数据才能匹配 CNN 的性能，因为 CNN 天生具有平移不变性和局部性的归纳偏好。但当数据量足够大时，ViT 的扩展性远超 CNN。DINOv2 通过自监督学习解决了数据需求问题。

> **【拓展：ViT 在多模态系统中的角色】** CLIP 使用 ViT 编码图像、Transformer 编码文本，通过对比学习对齐两个模态。DALL-E 和 Sora 使用 ViT 理解图像/视频，再生成新内容。SAM（Segment Anything）使用 ViT 作为主干网络实现通用图像分割。ViT 已成为多模态 AI 的视觉基础模块。

## Build It | 动手实现

See `code/main.py`. Pure-stdlib patchify + linear embedding + sanity checks. No training — ViT at any realistic scale needs PyTorch and hours of GPU time.

> 参见 `code/main.py`。纯标准库的 patchify + 线性嵌入 + 合理性检查。无训练——任何实际规模的 ViT 都需要 PyTorch 和数小时的 GPU 时间。

### Step 1: fake image

A 24 × 24 RGB image as a list of rows of `(R, G, B)` tuples. We use 6×6 patches → 16 patches, 108-d embedding vector each.

> 一个 24 × 24 RGB 图像，以 `(R, G, B)` 元组的行列表形式表示。使用 6×6 patch → 16 个 patch，每个 108 维嵌入向量。

### Step 2: patchify

```python
def patchify(image, P):
    H = len(image)
    W = len(image[0])
    patches = []
    for i in range(0, H, P):
        for j in range(0, W, P):
            patch = []
            for di in range(P):
                for dj in range(P):
                    patch.extend(image[i + di][j + dj])
            patches.append(patch)
    return patches
```

Raster order: row-major across the grid. Every ViT uses this ordering.

> 光栅顺序：网格上按行优先遍历。每个 ViT 都使用这种排序。

### Step 3: linear embed

Multiply each flat patch by a random `(patch_flat_size, d_model)` matrix. Verify output shape is `(N_patches + 1, d_model)` after prepending `[CLS]`.

> 将每个扁平 patch 乘以一个随机 `(patch_flat_size, d_model)` 矩阵。验证在添加 `[CLS]` 后输出形状为 `(N_patches + 1, d_model)`。

### Step 4: count parameters for a realistic ViT

Print the param count for ViT-Base: 12 layers, 12 heads, d=768, patch=16. Compare to ResNet-50 (~25M). ViT-Base lands at ~86M. ViT-Large ~307M. ViT-Huge ~632M.

> 打印 ViT-Base 的参数量：12 层、12 头、d=768、patch=16。与 ResNet-50（约 25M）对比。ViT-Base 约 86M。ViT-Large 约 307M。ViT-Huge 约 632M。

## Use It | 用框架实现

```python
from transformers import ViTImageProcessor, ViTModel
import torch
from PIL import Image

processor = ViTImageProcessor.from_pretrained("google/vit-base-patch16-224-in21k")
model = ViTModel.from_pretrained("google/vit-base-patch16-224-in21k")

img = Image.open("cat.jpg")
inputs = processor(img, return_tensors="pt")
out = model(**inputs).last_hidden_state   # (1, 197, 768): [CLS] + 196 patches
cls_emb = out[:, 0]                       # image representation
```

**DINOv2 embeddings are the 2026 default for image features.** Freeze the backbone, train a tiny head. Works for classification, retrieval, detection, captioning. Meta's DINOv2 checkpoints outperform CLIP on every non-text vision task.

> **DINOv2 嵌入是 2026 年图像特征的默认选择。** 冻结骨干网络，训练一个小头。适用于分类、检索、检测、图像描述。Meta 的 DINOv2 检查点在每个非文本视觉任务上都优于 CLIP。

**Patch-size picking.** Small models use 16×16 (ViT-B/16). Dense prediction (segmentation) uses 8×8 or 14×14 (SAM, DINOv2). Very large models use 14×14.

> **Patch 大小选择。** 小模型使用 16×16（ViT-B/16）。密集预测（分割）使用 8×8 或 14×14（SAM、DINOv2）。非常大的模型使用 14×14。

## Ship It | 产出物

See `outputs/skill-vit-configurator.md`. The skill picks a ViT variant and patch size for a new vision task given dataset size, resolution, and compute budget.

> 参见 `outputs/skill-vit-configurator.md`。该 skill 根据数据集大小、分辨率和计算预算，为新视觉任务选择 ViT 变体和 patch 大小。

## Exercises | 练习题

1. **Easy.** Run `code/main.py`. Verify the number of patches equals `(H/P) * (W/P)` and the flat patch dimension equals `P*P*C`.
   中文翻译：运行 `code/main.py`。验证 patch 数量等于 `(H/P) * (W/P)`，扁平 patch 维度等于 `P*P*C`。
2. **Medium.** Implement 2D sinusoidal positional embeddings — two independent sinusoidal codes for `row` and `col` of each patch, concatenated. Feed them into a tiny PyTorch ViT and compare accuracy vs learnable positional embeddings on CIFAR-10.
   中文翻译：实现 2D 正弦位置嵌入——每个 patch 的 `row` 和 `col` 独立编码后拼接。在小型 PyTorch ViT 上使用，与可学习位置嵌入在 CIFAR-10 上对比准确率。
3. **Hard.** Build a 3-layer ViT (PyTorch), train on 1,000 MNIST images with 4×4 patches. Measure test accuracy. Now add DINOv2 pretraining on the same 1,000 images (simplified: just train the encoder to predict patch embeddings from masked patches). Does accuracy improve?
   中文翻译：构建 3 层 ViT（PyTorch），用 4×4 patch 在 1,000 张 MNIST 图像上训练。测量测试准确率。然后添加 DINOv2 预训练（简化版：训练编码器从掩码 patch 预测 patch 嵌入）。准确率是否提升？

## Key Terms | 术语速查表

| Term | What people say | What it actually means |
|------|-----------------|-----------------------|
| 术语 | 通俗说法 | 实际含义 |
| Patch | "The vision-transformer token" | Flat vector of pixel values for a `P × P × C` region of the image. |
| Patch | "视觉 Transformer 的 token" | 图像中 `P × P × C` 区域的像素值扁平向量。 |
| Patchify | "Chop + flatten" | Slice image into non-overlapping patches, flatten each to a vector. |
| Patchify | "切分 + 展平" | 将图像切成不重叠的 patch，每个展平为向量。 |
| `[CLS]` token | "The image summary" | Prepended learnable token; its final embedding is the image representation. |
| `[CLS]` token | "图像摘要" | 预置的可学习 token；其最终嵌入是图像表示。 |
| Inductive bias | "What the model assumes" | ViT has fewer priors than CNNs; needs more data to make up the gap. |
| 归纳偏好 | "模型假设了什么" | ViT 的先验比 CNN 少；需要更多数据来弥补差距。 |
| DINOv2 | "Self-supervised ViT" | Trained without labels using image augmentation + momentum teacher. Best general image features in 2026. |
| DINOv2 | "自监督 ViT" | 使用图像增强 + 动量教师无标签训练。2026 年最佳通用图像特征。 |
| SigLIP | "CLIP's successor" | ViT + text encoder trained with sigmoid contrastive loss; better than CLIP on matched compute. |
| SigLIP | "CLIP 的继承者" | 用 sigmoid 对比损失训练的 ViT + 文本编码器；相同计算量下优于 CLIP。 |
| Swin | "Windowed ViT" | Hierarchical ViT with local attention + shifted windows; sub-quadratic. |
| Swin | "窗口 ViT" | 带局部注意力 + 移位窗口的层级 ViT；亚二次复杂度。 |
| Register tokens | "2023 trick" | A few extra learnable tokens that soak up attention sinks; improves DINOv2 features. |
| Register tokens | "2023 技巧" | 几个额外的可学习 token，吸收注意力汇聚；改善 DINOv2 特征。 |

## Further Reading | 延伸阅读

- [Dosovitskiy et al. (2020). An Image is Worth 16x16 Words: Transformers for Image Recognition at Scale](https://arxiv.org/abs/2010.11929) — the ViT paper.
  中文翻译：ViT 原始论文。
- [Touvron et al. (2021). Training data-efficient image transformers & distillation through attention](https://arxiv.org/abs/2012.12877) — DeiT.
  中文翻译：DeiT 论文。
- [Liu et al. (2021). Swin Transformer: Hierarchical Vision Transformer using Shifted Windows](https://arxiv.org/abs/2103.14030) — Swin.
  中文翻译：Swin Transformer 论文。
- [Oquab et al. (2023). DINOv2: Learning Robust Visual Features without Supervision](https://arxiv.org/abs/2304.07193) — DINOv2.
  中文翻译：DINOv2 论文。
- [Darcet et al. (2023). Vision Transformers Need Registers](https://arxiv.org/abs/2309.16588) — the register-token fix for DINOv2.
  中文翻译：DINOv2 的 register-token 修复论文。
