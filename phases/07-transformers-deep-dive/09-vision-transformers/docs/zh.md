# Vision Transformers (ViT) | 视觉 Transformer (ViT)

> 图像是一个 patch 的网格。句子是一个 token 的网格。同一个 Transformer 两者都能处理。

> **【中文解读】** ViT 把图像切成 patch 当作 token 序列处理。理解 ViT = 理解 Transformer 不限于 NLP。CLIP、DALL-E、Sora 都基于 Transformer。

**类型：** 构建
**语言：** Python
**前置条件：** 阶段 7 · 05（完整 Transformer），阶段 4 · 03（CNN），阶段 4 · 14（视觉 Transformer 入门）
**时长：** 约 45 分钟

## 问题引入

2020 年之前，计算机视觉就是卷积。ImageNet、COCO 和检测基准上的每个 SOTA 都使用 CNN 骨干。Transformer 是用于语言的。

Dosovitskiy 等人（2020）——"An Image is Worth 16x16 Words"——展示了你可以完全放弃卷积。将图像切成固定大小的 patch，将每个 patch 线性投影为嵌入，将序列送入普通 Transformer 编码器。在足够大的规模（ImageNet-21k 预训练或更大）下，ViT 匹配或超越基于 ResNet 的模型。

ViT 是 2026 年更广泛模式的起点：一种架构，多种模态。Whisper 将音频 token 化。ViT 将图像 token 化。机器人的动作 token。视频的像素 token。Transformer 不在乎——给它一个序列，它就会学习。

到 2026 年，ViT 及其后代（DeiT、Swin、DINOv2、ViT-22B、SAM 3）占据了视觉的大部分。CNN 在边缘设备和延迟敏感任务上仍然胜出。其他所有地方都有 ViT 存在于堆栈中。

> **【中文解读】** ViT 的核心洞察：图像可以像文本一样被切成"token"序列。将 224x224 图像切成 14x14 个 16x16 patch，每个 patch 展平后线性投影为嵌入向量，然后送入标准 Transformer 编码器。这证明了 Transformer 的通用性——不限于 NLP，任何可以"分块序列化"的数据都适用。

## 核心概念

![图像 → patch → token → Transformer](../assets/vit.svg)

### 步骤 1——分块化 (Patchify)

将 `H × W × C` 图像拆分为 `N × (P·P·C)` 的扁平 patch 序列。典型设置：`224 × 224` 图像，`16 × 16` patch → 196 个 patch，每个 768 个值。

```
图像 (224, 224, 3) → 14 × 14 的 16x16x3 patch 网格 → 196 个长度为 768 的向量
```

Patch 大小是调节杆。更小的 patch = 更多 token，更好的分辨率，二次注意力成本。更大的 patch = 更粗糙，更便宜。

### 步骤 2——线性嵌入

一个学习矩阵将每个扁平 patch 投影到 `d_model`。等效于核大小为 `P` 且步幅为 `P` 的卷积。在 PyTorch 中这字面上就是 `nn.Conv2d(C, d_model, kernel_size=P, stride=P)` —— 2 行实现。

> **【拓展：Swin Transformer 的层级设计】** 标准 ViT 使用固定 patch 大小和全局注意力，计算量 O(N^2)。Swin Transformer 引入层级结构：在小 patch 上做局部窗口注意力，逐层合并 patch 扩大感受野。这使得计算复杂度变为 O(N)，同时保留了层级特征提取的能力。Swin 在检测和分割任务上仍优于标准 ViT。

### 步骤 3——预置 `[CLS]` token，添加位置嵌入

- 预置一个可学习的 `[CLS]` token。其最终隐藏状态是用于分类的图像表示。
- 添加可学习的位置嵌入（ViT 原版）或正弦 2D（后续变体）。
- 2024+ RoPE 扩展到 2D 用于位置，有时不使用显式嵌入。

### 步骤 4——标准 Transformer 编码器

堆叠 L 个 `LayerNorm → Self-Attention → + → LayerNorm → MLP → +` 块。与 BERT 相同。没有视觉特定的层。这是论文的教学核心。

### 步骤 5——头部

用于分类：取 `[CLS]` 隐藏状态 → 线性 → softmax。用于 DINOv2 或 SAM，丢弃 `[CLS]`，直接使用 patch 嵌入。

### 重要的变体

| 模型 | 年份 | 变化 |
|------|------|------|
| ViT | 2020 | 原始版本。固定 patch 大小，全全局注意力。 |
| DeiT | 2021 | 蒸馏；仅在 ImageNet-1k 上可训练。 |
| Swin | 2021 | 层级式带移位窗口。固定的次二次成本。 |
| DINOv2 | 2023 | 自监督（无标签）。最佳通用视觉特征。 |
| ViT-22B | 2023 | 22B 参数；缩放定律适用。 |
| SigLIP | 2023 | ViT + 语言配对，sigmoid 对比损失。 |
| SAM 3 | 2025 | Segment Anything；ViT-Large + 可提示的掩码解码器。 |

### 为什么花了一段时间

ViT 需要*大量*数据才能匹配 CNN，因为它没有 CNN 的任何归纳偏好（平移不变性、局部性）。没有 >1 亿标注图像或强自监督预训练，CNN 在匹配计算量下仍然胜出。DeiT 在 2021 年通过蒸馏技巧修复了这个问题；DINOv2 在 2023 年通过自监督永久修复了它。

> **【中文解读】** ViT 的弱归纳偏好是双刃剑：需要更多数据才能匹配 CNN 的性能，因为 CNN 天生具有平移不变性和局部性的归纳偏好。但当数据量足够大时，ViT 的扩展性远超 CNN。DINOv2 通过自监督学习解决了数据需求问题。

> **【拓展：ViT 在多模态系统中的角色】** CLIP 使用 ViT 编码图像、Transformer 编码文本，通过对比学习对齐两个模态。DALL-E 和 Sora 使用 ViT 理解图像/视频，再生成新内容。SAM（Segment Anything）使用 ViT 作为主干网络实现通用图像分割。ViT 已成为多模态 AI 的视觉基础模块。

## 动手实现

参见 `code/main.py`。纯标准库的分块化 + 线性嵌入 + 健全性检查。不训练——任何实际规模的 ViT 都需要 PyTorch 和数小时的 GPU 时间。

### 步骤 1：伪图像

一个 24 × 24 RGB 图像，作为 `(R, G, B)` 元组的行列表。我们使用 6×6 patch → 16 个 patch，每个 108 维嵌入向量。

### 步骤 2：分块化

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

光栅顺序：网格上的行优先。每个 ViT 都使用这种顺序。

### 步骤 3：线性嵌入

将每个扁平 patch 乘以随机 `(patch_flat_size, d_model)` 矩阵。验证预置 `[CLS]` 后的输出形状是 `(N_patches + 1, d_model)`。

### 步骤 4：计算真实 ViT 的参数量

打印 ViT-Base 的参数量：12 层，12 头，d=768，patch=16。与 ResNet-50（约 25M）比较。ViT-Base 约 86M。ViT-Large 约 307M。ViT-Huge 约 632M。

## 用框架实现

```python
from transformers import ViTImageProcessor, ViTModel
import torch
from PIL import Image

processor = ViTImageProcessor.from_pretrained("google/vit-base-patch16-224-in21k")
model = ViTModel.from_pretrained("google/vit-base-patch16-224-in21k")

img = Image.open("cat.jpg")
inputs = processor(img, return_tensors="pt")
out = model(**inputs).last_hidden_state   # (1, 197, 768): [CLS] + 196 个 patch
cls_emb = out[:, 0]                       # 图像表示
```

**DINOv2 嵌入是 2026 年图像特征的默认选择。** 冻结骨干，训练一个微型头。适用于分类、检索、检测、标题生成。Meta 的 DINOv2 检查点在每个非文本视觉任务上都优于 CLIP。

**Patch 大小选择。** 小模型使用 16×16（ViT-B/16）。密集预测（分割）使用 8×8 或 14×14（SAM、DINOv2）。非常大的模型使用 14×14。

## 产出物

参见 `outputs/skill-vit-configurator.md`。该技能为新的视觉任务选择 ViT 变体和 patch 大小，给定数据集大小、分辨率和计算预算。

## 练习题

1. **简单。** 运行 `code/main.py`。验证 patch 数量等于 `(H/P) * (W/P)`，扁平 patch 维度等于 `P*P*C`。
2. **中等。** 实现 2D 正弦位置嵌入——每个 patch 的 `row` 和 `col` 各自独立的正弦编码，拼接。将它们送入微型 PyTorch ViT，在 CIFAR-10 上与可学习位置嵌入比较准确率。
3. **困难。** 构建一个 3 层 ViT（PyTorch），用 4×4 patch 在 1,000 张 MNIST 图像上训练。测量测试准确率。现在在相同的 1,000 张图像上添加 DINOv2 预训练（简化版：只训练编码器从掩码 patch 预测 patch 嵌入）。准确率是否提高？

## 术语速查表

| 术语 | 人们的说法 | 实际含义 |
|------|-----------|---------|
| Patch | "视觉 Transformer 的 token" | 图像 `P × P × C` 区域的像素值扁平向量。 |
| 分块化 (Patchify) | "切 + 展平" | 将图像切成不重叠的 patch，将每个展平为向量。 |
| `[CLS]` token | "图像摘要" | 预置的可学习 token；其最终嵌入是图像表示。 |
| 归纳偏好 | "模型假设什么" | ViT 比 CNN 的先验更少；需要更多数据来弥补差距。 |
| DINOv2 | "自监督 ViT" | 使用图像增强 + 动量教师无标签训练。2026 年最佳通用图像特征。 |
| SigLIP | "CLIP 的继任者" | ViT + 文本编码器使用 sigmoid 对比损失训练；在匹配计算量下优于 CLIP。 |
| Swin | "窗口化 ViT" | 带局部注意力 + 移位窗口的层级 ViT；次二次复杂度。 |
| 寄存器 token | "2023 年的技巧" | 少量额外可学习 token 吸收注意力汇聚；改善 DINOv2 特征。 |

## 延伸阅读

- [Dosovitskiy 等人（2020）。An Image is Worth 16x16 Words: Transformers for Image Recognition at Scale](https://arxiv.org/abs/2010.11929) —— ViT 论文。
- [Touvron 等人（2021）。Training data-efficient image transformers & distillation through attention](https://arxiv.org/abs/2012.12877) —— DeiT。
- [Liu 等人（2021）。Swin Transformer: Hierarchical Vision Transformer using Shifted Windows](https://arxiv.org/abs/2103.14030) —— Swin。
- [Oquab 等人（2023）。DINOv2: Learning Robust Visual Features without Supervision](https://arxiv.org/abs/2304.07193) —— DINOv2。
- [Darcet 等人（2023）。Vision Transformers Need Registers](https://arxiv.org/abs/2309.16588) —— DINOv2 的寄存器 token 修复。
