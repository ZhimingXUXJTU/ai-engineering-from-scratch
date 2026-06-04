# 视觉自回归建模 (VAR)：下一尺度预测

> 扩散模型在时间维度上迭代采样（去噪步骤）。VAR 在尺度维度上迭代——先预测 1x1 token，再 2x2，再 4x4，直到最终分辨率，每个尺度以前一个为条件。2024 年论文证明 VAR 展现了 GPT 风格的 Scaling Law，在相同计算预算下超越 DiT。本课构建核心机制。

> **【中文解读】** 扩散模型在时间维度上迭代采样（去噪步骤），VAR 在尺度维度上迭代——先预测 1x1 token，再 2x2，再 4x4，直到目标分辨率。2024 年论文证明 VAR 展现了 GPT 风格的 Scaling Law，在相同计算预算下超越 DiT。

> **【拓展：VAR 是生成模型的新范式】** VAR 将自回归思想从"下一个 token"扩展到"下一个尺度"，为图像生成开辟了新方向。它可能成为继扩散模型之后的下一代生成范式。

**类型：** 构建
**语言：** Python（使用 PyTorch）
**前置要求：** 阶段 7 第 03 课（多头注意力）、阶段 8 第 06 课（DDPM）
**预计时间：** ~90 分钟

## 问题引入

自回归生成在语言建模中占主导地位，因为它可以预测地扩展：更多计算、更多参数、更低困惑度、更好输出。2024 年之前图像生成有两种主要的自回归尝试：PixelRNN/PixelCNN（逐像素）和 DALL-E 1 / Parti / MuseGAN（VQ-VAE 编码上的逐 token）。

两者都受到生成顺序问题的困扰。像素和 token 排列在 2D 网格上，但 AR 模型必须以 1D 光栅顺序访问它们。早期角落的像素不知道图像最终会变成什么样。生成质量的扩展不如文本上的 GPT，在相同计算量下从未达到扩散模型的质量。

VAR 通过改变被生成的内容来修复生成顺序问题。VAR 不再在空间上逐个预测图像 token，而是以递增分辨率预测整张图像。步骤 1：预测 1x1 token（整体图像"摘要"）。步骤 2：预测 2x2 的 token 网格（粗特征）。步骤 3：预测 4x4 的 token 网格。步骤 K：预测最终的 (H/8)x(W/8) 网格。

每个尺度关注所有之前的尺度（按"尺度顺序"因果），并在自身尺度内并行。顺序问题消失了：尺度 k 的整个图像在一次 Transformer 传播中生成。

> **【中文解读】** VAR（Visual Autoregressive）的核心创新：将图像生成的自回归顺序从"逐像素/逐 token"改为"逐尺度"。先预测 1x1 的全局摘要，再 2x2 的粗特征，再 4x4 的细节，直到目标分辨率。每个尺度内并行生成，消除了传统图像 AR 的"生成顺序问题"。2024 年论文证明 VAR 展现了类似 GPT 的 Scaling Law。

> **【拓展：VAR 与扩散模型的对比】** VAR 是继扩散模型之后最有潜力的图像生成新范式。优势：(1) 清晰的 Scaling Law——像 GPT 一样可预测扩展；(2) 生成过程结构化——先全局后局部，更符合人类感知；(3) 在相同计算预算下超越 DiT。挑战：需要多尺度 VQ-VAE tokenizer，训练更复杂。如果 Scaling Law 验证成功，VAR 可能成为下一代图像生成的基础架构。

## 核心概念

### VQ-VAE 多尺度分词器

VAR 需要一个**多尺度离散分词器**。对于图像 x，它产生一系列递增分辨率的 token 网格：

```
x -> encoder -> latent f
f -> tokenize at 1x1: token grid z_1 of shape (1, 1)
f -> tokenize at 2x2: token grid z_2 of shape (2, 2)
...
f -> tokenize at (H/p)x(W/p): token grid z_K of shape (H/p, W/p)
```

每个 z_k 使用相同的码本（典型大小 4096-16384）。每个尺度的 token 化不是独立的——训练使得每个尺度的残差求和可以重建 f：

```
f ≈ upsample(embed(z_1), target_size) + ... + upsample(embed(z_K), target_size)
```

这是一种**残差 VQ** 变体。尺度 k 捕获尺度 1..k-1 遗漏的内容。解码器取所有尺度嵌入的和并产生图像。

多尺度 VQ 分词器只训练一次（类似 VQGAN）然后冻结。所有生成工作由之上的自回归模型完成。

### 下一尺度预测

生成模型是一个 Transformer，它看到所有之前尺度的 token 并预测下一个尺度的 token。

输入序列结构：
```
[START, z_1 tokens, z_2 tokens, z_3 tokens, ..., z_K tokens]
```

位置嵌入编码尺度索引和尺度内的空间位置。注意力在尺度顺序上是因果的：尺度 k 位置 (i, j) 的 token 可以关注尺度 1..k 的所有 token 以及尺度 k 本身中在所用任意尺度内顺序中较早的 token（VAR 使用固定位置注意力，无尺度内因果性——尺度内的所有位置并行预测）。

训练损失：在每个尺度 k，给定所有先前尺度的 token 预测 token z_k。离散 VQ 编码上的交叉熵损失。与 GPT 结构相同，只是"序列"现在是尺度结构化的。

### 生成

推理时：
```
generate z_1 = sample from p(z_1)                    # 1 个 token
generate z_2 = sample from p(z_2 | z_1)              # 4 个 token 并行
generate z_3 = sample from p(z_3 | z_1, z_2)         # 16 个 token 并行
...
decode: f = sum of embed-and-upsample scales 1..K
image = VAE_decoder(f)
```

对于 K = 10 个尺度，生成是 10 次 Transformer 前向传播。每次传播并行生成其整个尺度——尺度内没有逐 token 自回归。对于 256x256 图像，这大约是 10 次传播 vs DiT 的 28-50 次。

### 为什么下一尺度胜过下一 token

三个结构性优势：
1. **从粗到细与自然图像统计一致。** 人类视觉感知和图像数据集都展现出尺度依赖的规律性：低频结构稳定且可预测；高频细节依赖于低频内容。下一尺度预测利用了这一点。
2. **尺度内并行生成。** 与 GPT 风格的 token AR 不同，VAR 在一步中产生一个尺度的所有 token。有效生成长度是对数级别的而非线性的。
3. **无生成顺序偏差。** 尺度 k 的 token 看到尺度 k-1 的全部；没有"左侧"或"上方"偏差迫使早期 token 在后期上下文可用之前就做出承诺。

### 缩放定律

Tian et al. 证明 VAR 在 ImageNet 上遵循 FID 的幂律缩放曲线——就像 GPT 对困惑度一样。参数或计算量翻倍，误差减半。这是第一个像语言模型一样清晰展现这种缩放行为的图像生成模型。结果是 VAR 尺度的预测可以从计算量做出，而非每个架构的经验猜测。

### 与扩散模型的关系

VAR 和扩散模型共享相同的数据压缩故事：两者都将生成问题分解为一系列更简单的子问题。

- 扩散：逐步添加噪声，学习撤销一步。
- VAR：逐步添加分辨率，学习预测下一个尺度。

它们是问题的不同切面。两者都产生可处理的条件分布。实验上 VAR 推理更快（更少传播，尺度内全部并行），在类别条件 ImageNet 上匹敌或超越 DiT。文本条件 VAR（VARclip, HART）是活跃的研究方向。

## 动手实现

在 `code/main.py` 中你将：
1. 在合成"图像"数据（2D 高斯环）上构建一个微型**多尺度 VQ 分词器**。
2. 训练一个 **VAR 风格 Transformer** 进行下一尺度预测。
3. 通过调用 Transformer 4 次（4 个尺度）并解码来采样。
4. 验证尺度有序训练使尺度内生成可以并行。

这是一个玩具实现。重点是看到尺度结构化的注意力掩码和尺度内并行生成真正工作。

## 产出物

本课产出 `outputs/skill-var-tokenizer-designer.md`——一个用于设计多尺度分词器的技能：尺度数、尺度比率、码本大小、残差共享、解码器架构。

## 练习题

1. **尺度数量消融。** 用 4、6、8、10 个尺度训练 VAR。测量重建质量 vs 自回归传播次数。更多尺度 = 更细的残差 = 更好的质量但更多传播。

2. **码本大小。** 用码本大小 512、4096、16384 训练分词器。更大的码本给出更好的重建但更难的预测。找到拐点。

3. **尺度内并行检查。** 对于训练好的 VAR，显式测量注意力模式。在尺度 k 内，模型是否关注跨尺度位置但不关注尺度内位置？验证掩码实现。

4. **VAR vs DiT 缩放。** 对于相同的 ImageNet 类别条件任务，在匹配的参数预算（如 33M、130M、458M）下训练 VAR 和 DiT。绘制 FID vs 计算量。VAR 应该在每个大小上领先——在小规模上复现论文结果。

5. **文本条件化。** 扩展 VAR 以通过 adaLN 接受文本嵌入（CLIP 池化）作为额外条件输入。这是 HART 的配方。FID 在文本对齐采样上改善多少？

## 术语速查表

| 术语 | 人们怎么说 | 实际含义 |
|------|-----------------|----------------------|
| VAR | "Visual AutoRegressive" | 通过 VQ token 金字塔上的下一尺度预测进行图像生成 |
| 下一尺度预测 | "先预测粗的，再预测细的" | 模型在递增分辨率尺度上预测 token，以所有先前尺度为条件 |
| 多尺度 VQ 分词器 | "残差 VQ" | 产生 K 个递增分辨率 token 网格的 VQ-VAE，解码器对所有尺度求和 |
| 尺度 k | "金字塔层级 k" | K 个分辨率级别之一，从 k=1 的 1x1 到 k=K 的 (H/p)x(W/p) |
| 尺度内并行 | "每个尺度一次前向" | 尺度 k 的所有 token 在一次 Transformer 传播中预测，非自回归 |
| 跨尺度因果 | "尺度有序注意力" | 尺度 k 的 token 可以关注尺度 1..k 的全部但不能关注尺度 k+1..K |
| 残差 VQ | "加性 token 化" | 每个尺度的 token 编码更低尺度的残差；解码器对所有尺度嵌入求和 |
| VAR 缩放定律 | "图像 GPT 缩放" | FID 在计算量上遵循可预测的幂律，类似语言模型的困惑度 |
| HART | "混合 VAR + 文本" | 结合 MaskGIT 风格迭代解码与 VAR 尺度结构的文本条件 VAR 变体 |
| 尺度位置嵌入 | "(scale, row, col) 三元组" | 位置编码同时携带尺度索引和尺度内的空间坐标 |

## 延伸阅读

- [Tian et al., 2024 — "Visual Autoregressive Modeling: Scalable Image Generation via Next-Scale Prediction"](https://arxiv.org/abs/2404.02905) — VAR 论文，权威参考
- [Peebles and Xie, 2022 — "Scalable Diffusion Models with Transformers"](https://arxiv.org/abs/2212.09748) — DiT，扩散对比基线
- [Esser et al., 2021 — "Taming Transformers for High-Resolution Image Synthesis"](https://arxiv.org/abs/2012.09841) — VQGAN，VAR 多尺度分词器扩展的分词器家族
- [van den Oord et al., 2017 — "Neural Discrete Representation Learning"](https://arxiv.org/abs/1711.00937) — VQ-VAE，离散图像 token 化的基础
- [Tang et al., 2024 — "HART: Efficient Visual Generation with Hybrid Autoregressive Transformer"](https://arxiv.org/abs/2410.10812) — 文本条件 VAR
