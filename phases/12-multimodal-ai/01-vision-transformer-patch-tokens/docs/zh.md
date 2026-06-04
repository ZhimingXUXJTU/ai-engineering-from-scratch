# Vision Transformer 与 Patch-Token 原语

> 在进入多模态之前，图像必须先变成 Transformer 能处理的 token 序列。2020 年的 ViT 论文用 16x16 像素块、线性投影和位置嵌入给出了答案。五年后，2026 年的每一个前沿模型（2576px 原生分辨率的 Claude Opus 4.7、Gemini 3.1 Pro、Qwen3.5-Omni）仍然从此开始——编码器从 ViT 演变为 DINOv2 再到 SigLIP 2，增加了 register token，位置编码方案变成了 2D-RoPE，但原语没有变。本课从头到尾阅读 patch-token 流水线，用标准库 Python 构建它，为 Phase 12 其余课程建立"视觉 token"的具体心智模型。

> **【中文解读】** 在进入多模态之前，图像必须先变成 Transformer 能处理的 token 序列。ViT 用16x16像素块+线性投影+位置编码实现了这一转换，至今仍是所有前沿模型的基础。

> **【拓展：ViT Patch→多模态基础】** Patch-Token 是所有视觉语言模型的基础——无论是 CLIP 的视觉编码器、LLaVA 的图像输入还是文档理解模型，都从 Patch 切分开始。

**类型：** 学习
**语言：** Python（标准库，patch tokenizer + 几何计算器）
**前置知识：** Phase 7（Transformer），Phase 4（计算机视觉）
**时长：** 约 120 分钟

## 学习目标

- 将 HxWx3 的图像转换为带有正确位置编码的 patch token 序列。
- 计算给定（patch 大小、分辨率、隐藏维度、深度）的 ViT 的序列长度、参数量和 FLOPs。
- 说出将 ViT 从 2020 年研究带到 2026 年生产的三项升级：自监督预训练（DINO / MAE）、register token 和原生分辨率打包。
- 为下游任务在 CLS 池化、均值池化和 register token 之间做出选择。

## 问题引入

Transformer 处理向量序列。文本本身已经是序列（字节或 token）。图像是具有三个颜色通道的 2D 像素网格——不是序列。如果将每个像素展平，一张 224x224 的 RGB 图像变成 150,528 个 token，而如此长度的自注意力是行不通的（复杂度为序列长度的二次方）。

2020 年之前的方法将 CNN 特征提取器嫁接到前面：ResNet 产生 7x7 的 2048 维向量特征图，将这 49 个 token 送入 Transformer。这可行，但继承了 CNN 的偏差（平移等变性、局部感受野），并失去了 Transformer 对规模的需求。

Dosovitskiy 等人（2020）提出了一个直接的问题：如果我们跳过 CNN 会怎样？将图像分割为固定大小的 patch（比如 16x16 像素），对每个 patch 进行线性投影到向量，添加位置嵌入，然后将序列送入标准 Transformer。当时这是异端——没有卷积的视觉。在足够的数据（JFT-300M，后来是 LAION）下，它在 ImageNet 上击败了 ResNet 并持续改进。

到 2026 年，ViT 原语是无可争议的基础。每个开源 VLM 的视觉塔都是某个后裔（DINOv2、SigLIP 2、CLIP、EVA、InternViT）。问题不再是"应该用 patch 吗？"而是"什么 patch 大小、什么分辨率调度、什么预训练目标、什么位置编码"。

## 核心概念

> **【中文解读】** Vision Transformer (ViT) 将图像分割为固定大小的 patch（如 16x16 像素），每个 patch 展平后通过线性投影变成一个 token，然后像 NLP 中的 Transformer 一样处理。这是将 Transformer 架构引入计算机视觉的奠基性工作，取代了 CNN 成为视觉 backbone。

> **【拓展：ViT 的影响】** Dosovitskiy 等人 2020 年提出的 ViT 证明 Transformer 在图像分类上可以超越 CNN。ViT-L/14 在 ImageNet 上达到 88.5% top-1 准确率。ViT 是 CLIP、GPT-4V、Gemini 等多模态模型的视觉编码器基础。Swin Transformer 通过层级化窗口注意力解决了 ViT 对高分辨率图像的计算瓶颈。


> **【拓展：ViT 对 CNN 的优势】** ViT 的全局自注意力在数据量足够大时（如 JFT-300M 或 LAION-5B）显著优于 CNN 的局部感受野。ViT-H/14 在 ImageNet-21k 上预训练后，在多个下游任务上超越 EfficientNet 和 ResNet。ViT 也是 DINOv2（自监督视觉基础模型）的 backbone。


### Patch 即 Token

给定形状为 `(H, W, 3)` 的图像 `x` 和 patch 大小 `P`，将图像切割为 `(H/P) x (W/P)` 个不重叠的 patch 网格。每个 patch 是一个 `P x P x 3` 的像素立方体。将每个立方体展平为 `3 P^2` 的向量。应用共享的线性投影 `W_E`（形状为 `(3 P^2, D)`），将每个 patch 映射到模型的隐藏维度 `D`。

对于 ViT-B/16 的规范配置：
- 分辨率 224，patch 大小 16 → 网格 14x14 → 196 个 patch token。
- 每个 patch 是 `16 x 16 x 3 = 768` 个像素值，投影到 `D = 768`。
- 添加可学习的 `[CLS]` token → 序列长度 197。

patch 投影在数学上等同于核大小为 `P`、步幅为 `P`、`D` 个输出通道的 2D 卷积。这就是生产代码的实际实现方式——`nn.Conv2d(3, D, kernel_size=P, stride=P)`。"线性投影"的表述是概念性的；卷积核的表述是高效的。

### 位置嵌入

Patch 没有内在的顺序——Transformer 将它们视为一个集合。早期的 ViT 添加了可学习的一维位置嵌入（每个位置一个 768 维向量，共 197 个）。可行，但将模型绑定到训练分辨率：推理时如果改变网格，需要插值位置表。

现代视觉骨干使用 2D-RoPE（Qwen2-VL 的 M-RoPE、SigLIP 2 的默认）或分解的 2D 位置。2D-RoPE 根据每个 patch 的（行、列）索引旋转 query 和 key 向量，因此模型从旋转角度推断相对的 2D 位置。没有位置表。模型在推理时处理任意网格大小。

### CLS Token、池化输出和 Register Token

图像级别的表示是什么？三种选择共存：

1. `[CLS]` token。在 patch 序列前面添加一个可学习向量。经过所有 Transformer 块后，CLS token 的隐藏状态就是图像表示。继承自 BERT。由原始 ViT、CLIP 使用。
2. 均值池化。对 patch token 的输出隐藏状态取平均。由 SigLIP、DINOv2、大多数现代 VLM 使用。
3. Register token。Darcet 等人（2023）观察到，没有显式汇聚 token 的 ViT 训练会产生高范数的"伪影" patch，劫持了自注意力。添加 4-16 个可学习的 register token 可以吸收这种负载并提高密集预测质量（分割、深度）。DINOv2 和 SigLIP 2 都附带 register。

这个选择对下游任务很重要。CLS 适合分类。对于将 patch token 送入 LLM 的 VLM，你完全跳过池化——每个 patch 都成为 LLM 输入 token。Register 在交接前被丢弃（它们是脚手架，不是内容）。

### 预训练：监督、对比、掩码、自蒸馏

2020 年的 ViT 使用监督分类在 JFT-300M 上预训练。很快被取代：

- CLIP（2021）：在 4 亿对上进行对比图文预训练。第 12.02 课。
- MAE（2021，He 等人）：掩码 75% 的 patch，重建像素。自监督，在纯图像上工作。
- DINO（2021）/ DINOv2（2023）：师生自蒸馏，无需标签，无需描述。2023 年的 DINOv2 ViT-g/14 是最强的纯视觉骨干，也是"密集特征"用例的默认选择。
- SigLIP / SigLIP 2（2023，2025）：使用 sigmoid 损失和 NaFlex 实现原生宽高比的 CLIP。2026 年开源 VLM 中的主导视觉塔（Qwen、Idefics2、LLaVA-OneVision）。

你选择的预训练决定了骨干擅长什么：CLIP/SigLIP 适用于与文本的语义匹配，DINOv2 用于密集视觉特征，MAE 作为下游微调的起点。

### 缩放定律

ViT 缩放（Zhai 等人，2022）确立了 ViT 的质量遵循模型大小、数据量和计算量的可预测规律。在固定计算量下：
- 更大的模型 + 更多数据 → 更好的质量。
- Patch 大小是序列长度与保真度的调节杆。Patch 14（DINOv2/SigLIP SO400m 的典型值）每张图产生比 patch 16 更多的 token；有利于 OCR 和密集任务，不利于速度。
- 分辨率是另一个大调节杆。从 224 到 384 到 512 几乎总是有帮助，但 FLOPs 成本为二次方增长。

ViT-g/14（1B 参数，patch 14，分辨率 224 → 256 token）和 SigLIP SO400m/14（400M 参数，patch 14）是 2026 年开源 VLM 的两个主力编码器。

### ViT 的参数量

完整计算在 `code/main.py` 中。对于 ViT-B/16 在 224：

```
patch_embed = 3 * 16 * 16 * 768 + 768  =  591k
cls + pos    = 768 + 197 * 768          =  152k
block        = 4 * 768^2 (QKVO) + 2 * 4 * 768^2 (MLP) + 2 * 2*768 (LN)
             = 12 * 768^2 + 3k          =  7.1M
12 blocks    = 85M
final LN    = 1.5k
total       ≈ 86M
```

在加载检查点之前用这种方式估算每个 ViT。骨干大小设定了任何下游 VLM 的显存下限。

### 2026 年生产配置

2026 年大多数开源 VLM 搭载的编码器是原生分辨率（NaFlex）下的 SigLIP 2 SO400m/14。它有：
- 400M 参数。
- Patch 大小 14，默认分辨率 384 → 每张图 729 个 patch token。
- 图像级任务使用均值池化；所有 729 个 patch 流入 LLM 用于 VQA。
- 4 个 register token，在 LLM 交接前丢弃。
- 2D-RoPE 带图像级缩放以支持原生宽高比。

该配置中的每个决策都可以追溯到你可以阅读的论文。

## 用框架实现

`code/main.py` 是一个 patch tokenizer 和几何计算器。它接收（图像 H、W、patch P、隐藏维度 D、深度 L）并报告：

- Patch 后的网格形状和序列长度。
- 合成 8x8 像素玩具图像的 token 序列（遍历展平+投影路径）。
- 按 patch 嵌入、位置嵌入、Transformer 块和头部分解的参数量。
- 目标分辨率下每次前向传播的 FLOPs。
- ViT-B/16 @ 224、ViT-L/14 @ 336、DINOv2 ViT-g/14 @ 224、SigLIP SO400m/14 @ 384 的比较表。

运行它。将参数量与已发表数字匹配。调整 patch 大小和分辨率，感受 token 数量的开销。

## 产出物

本课产出 `outputs/skill-patch-geometry-reader.md`。给定 ViT 配置（patch 大小、分辨率、隐藏维度、深度），它生成 token 数量、参数量和显存估算并附带论证。每当你为 VLM 选择视觉骨干时都使用这个技能——它可以防止"token 爆炸填满了 LLM 上下文"的意外。

## 练习题

1. 计算 Qwen2.5-VL 在原生 1280x720 输入、patch 大小 14 下的 patch-token 序列长度。与仅 CLS 表示相比如何？

2. 1080p 帧（1920x1080）在 patch 14 下产生多少 token？以 30 FPS 超过 5 分钟的视频，总共多少视觉 token？哪种成本节省最多：池化、帧采样还是 token 合并？

3. 用纯 Python 实现对 patch token 的均值池化。验证 DINOv2 输出 196 个 token 的均值池化与模型的 `forward` 在你请求池化嵌入时返回的结果一致。

4. 阅读"Vision Transformers Need Registers"（arXiv:2309.16588）第 3 节。用两句话描述 register 吸收的伪影是什么，以及为什么它对下游密集预测很重要。

5. 修改 `code/main.py` 以支持 patch-n'-pack：给定不同分辨率的图像列表，生成单个打包序列和块对角注意力掩码。在学习第 12.06 课时进行验证。

## 术语速查表

| 术语 | 常见说法 | 实际含义 |
|------|---------|---------|
| Patch | "16x16 像素方块" | 输入图像的固定大小不重叠区域；变成一个 token |
| Patch 嵌入 | "线性投影" | 共享的学习矩阵（或步幅为 P 的 Conv2d），将展平的 patch 像素映射到 D 维向量 |
| CLS Token | "类 token" | 前置的可学习向量，其最终隐藏状态代表整个图像；2026 年可选 |
| Register Token | "汇聚 token" | 额外的可学习 token，吸收 ViT 预训练中产生的高范数注意力伪影 |
| 位置嵌入 | "位置信息" | 使序列具有顺序感知的逐位置向量或旋转；2D-RoPE 是现代默认选择 |
| 网格 | "Patch 网格" | 给定分辨率和 patch 大小下的 (H/P) x (W/P) 2D patch 数组 |
| NaFlex | "原生灵活分辨率" | SigLIP 2 功能：单一模型服务多种宽高比和分辨率，无需重训练 |
| 骨干 | "视觉塔" | 预训练的图像编码器，其 patch-token 输出馈入 VLM 中的 LLM |
| 池化 | "图像级摘要" | 将 patch token 变为一个向量的策略：CLS、均值、注意力池化或基于 register |
| Patch 14 vs 16 | "更细 vs 更粗网格" | Patch 14 每张图产生更多 token，OCR 保真度更好，速度更慢；Patch 16 是经典默认值 |

## 延伸阅读

- [Dosovitskiy 等人 — An Image is Worth 16x16 Words (arXiv:2010.11929)](https://arxiv.org/abs/2010.11929) — 原始 ViT。
- [He 等人 — Masked Autoencoders Are Scalable Vision Learners (arXiv:2111.06377)](https://arxiv.org/abs/2111.06377) — MAE，自监督预训练。
- [Oquab 等人 — DINOv2 (arXiv:2304.07193)](https://arxiv.org/abs/2304.07193) — 大规模自蒸馏，无需标签。
- [Darcet 等人 — Vision Transformers Need Registers (arXiv:2309.16588)](https://arxiv.org/abs/2309.16588) — register token 和伪影分析。
- [Tschannen 等人 — SigLIP 2 (arXiv:2502.14786)](https://arxiv.org/abs/2502.14786) — 2026 年默认视觉塔。
- [Zhai 等人 — Scaling Vision Transformers (arXiv:2106.04560)](https://arxiv.org/abs/2106.04560) — 经验缩放定律。
