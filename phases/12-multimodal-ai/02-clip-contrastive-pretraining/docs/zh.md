# CLIP 图文对比预训练

> OpenAI 的 CLIP（2021）证明了一个足够大的单一想法可以驱动未来五年：仅使用嘈杂的网络图像-描述对和对比损失，将图像编码器和文本编码器对齐到同一向量空间。零监督标签。4 亿对。生成的嵌入空间可以做到零样本分类、图文检索，并作为每个 2026 年 VLM 的视觉塔接入。SigLIP 2（2025）用 sigmoid 替换了 softmax，以更低成本扩展超越了 CLIP。本课从 InfoNCE 到 sigmoid 逐对损失讲解数学，并用标准库 Python 构建训练步骤。

> **【中文解读】** CLIP 用4亿网络图文对，通过对比损失将图像和文本编码到同一向量空间。零标注实现零样本分类和图文检索，是所有2026年视觉语言模型的视觉塔基础。

> **【拓展：CLIP→多模态大模型】** CLIP 的图文对比学习是 LLaVA、BLIP-2 等多模态大模型的基础。理解 CLIP 是理解整个多模态 AI 生态的起点。

**类型：** 构建
**语言：** Python（标准库，InfoNCE + sigmoid 损失实现）
**前置知识：** Phase 12 · 01（ViT Patch），Phase 7（Transformer）
**时长：** 约 180 分钟

## 学习目标

- 从互信息推导 InfoNCE 损失并实现数值稳定的向量化版本。
- 解释为什么 sigmoid 逐对损失（SigLIP）可以扩展到批量 32768+ 而没有 softmax 要求的全归约开销。
- 通过构建文本模板（`a photo of a {class}`）并取余弦相似度的 argmax 来运行零样本 ImageNet 分类。
- 说出 CLIP / SigLIP 预训练给你的四个调节杆：批量大小、温度、提示模板、数据质量。

## 问题引入

CLIP 之前的视觉是监督式的。收集标注数据集（ImageNet：120 万图像，1000 类），训练 CNN，部署。标签昂贵，标签偏向标注者能达成共识的内容，标签不能在没有微调的情况下迁移到新任务。

图像-描述的网络有超过 10 亿松散标注的免费对。一张金毛猎犬的照片配以 alt 文本"我的狗 Max 在公园里"携带了监督信号——文本描述了图像。问题是：你能把这个变成有用的训练吗？

CLIP 的答案：将图像-描述对视为匹配任务。给定一批 N 张图像和 N 条描述，学习将每张图像与自己的描述在 N-1 个干扰项中匹配。监督是"这两个东西属于一起；这 N-1 个不属于"。没有类别标签。没有人工标注。只有一个对比损失。

生成的嵌入空间能做到的比 CLIP 训练的更多。ImageNet 零样本有效是因为"a photo of a cat"嵌入到从未被显式标记为猫的猫图片附近。这就是催生每个 2026 年 VLM 的赌注。

## 核心概念

> **【中文解读】** CLIP（Contrastive Language-Image Pre-training）通过对比学习将图像和文本映射到同一向量空间：匹配的图文对距离拉近，不匹配的推远。CLIP 在 4 亿图文对上训练后，无需微调即可实现 zero-shot 图像分类，是 OpenAI 多模态能力的基石。

> **【拓展：CLIP 的应用生态】** CLIP 的对比学习范式催生了大量应用：DALL-E 2/3 用 CLIP 引导图像生成，Stable Diffusion 用 OpenCLIP 作为安全过滤器，LLaVA 用 CLIP 视觉编码器连接 LLM 和图像理解。CLIP 的 zero-shot 能力在 ImageNet 上达到 76.2% top-1 准确率，无需任何 ImageNet 训练数据。


> **【拓展：CLIP 的 zero-shot 能力】** CLIP 最惊人的能力是 zero-shot 分类——不需要任何下游任务的训练数据，只需给出类别名称就能分类图像。在 ImageNet 上，CLIP ViT-L/14 的 zero-shot 准确率（76.2%）接近 ResNet-50 的全监督准确率（76.7%）。这种能力来自 4 亿图文对的对比学习。


### 双编码器

CLIP 有两个塔：

- 图像编码器 `f`：ViT 或 ResNet，每张图像输出一个 D 维向量。
- 文本编码器 `g`：小型 Transformer，每条描述输出一个 D 维向量。

两个塔都将输出归一化为单位长度。相似度为 `cos(f(x), g(y)) = f(x)^T g(y)`，因为两者都是单位范数。

对于一批 N 对（图像，描述），构建形状为 `(N, N)` 的相似度矩阵 `S`：

```
S[i, j] = cos(f(x_i), g(y_j)) / tau
```

其中 `tau` 是可学习的温度（CLIP 初始化为 0.07；在对数空间中学习）。

### InfoNCE 损失

CLIP 使用行和列上的对称交叉熵：

```
loss_i2t = CE(S, labels=identity)     # 每张图像的正样本是它自己的描述
loss_t2i = CE(S^T, labels=identity)   # 每条描述的正样本是它自己的图像
loss = (loss_i2t + loss_t2i) / 2
```

这就是 InfoNCE。CE 中的 softmax 迫使每张图像比批次中每条其他描述更匹配自己的描述。"负样本"是批次中所有其他项。更大的批量 = 更多负样本 = 更强信号。CLIP 在批量 32k 下训练；规模很重要。

### 温度

`tau` 控制 softmax 的锐度。低 tau → 尖锐分布，硬负样本挖掘效果。高 tau → 柔和，所有样本都有贡献。CLIP 学习 `log(1/tau)`，裁剪以防止崩溃。SigLIP 2 固定初始 tau 并使用可学习的偏置。

### 为什么 Sigmoid 扩展性更好（SigLIP）

Softmax 需要整个相似度矩阵同步。在分布式训练中，你必须将每个嵌入全归约到每个副本，然后做 softmax。这在通信上是世界大小的二次方。

SigLIP 用逐元素 sigmoid 替换 softmax：对于每对 `(i, j)`，损失是"它们是匹配对吗？"的二元分类。正类标签是对角线，其他一切都是负样本。损失为：

```
L = -1/N sum over (i, j) [ y_ij log sigmoid(S[i,j]) + (1-y_ij) log sigmoid(-S[i,j]) ]
```

`y_ij = 1` 如果 `i == j`，否则 0。每对的损失是独立的。不需要全归约。每个 GPU 计算其本地块并求和。SigLIP 2 可以廉价地扩展到批量 32k-512k，而 CLIP 需要按比例更多的通信。

### 零样本分类

给定 N 个类别名称，为每个类别构建文本模板：

```
"a photo of a {class}"
```

用文本编码器嵌入每个模板。用图像编码器嵌入你的图像。余弦相似度的 Argmax = 预测类别。无需在目标类别上训练。

提示模板很重要。CLIP 原始论文每个类别使用 80 个模板（朴素的、艺术的、照片的、绘画的等）并平均嵌入。ImageNet 上 +3 分。现代使用通常选择一两个模板。

### 线性探测和微调

零样本是基线。线性探测（在冻结的 CLIP 特征上为你的目标类别训练一个线性层）在域内任务上超越零样本。全量微调在域内超越线性探测，但可能损害零样本迁移。三种机制，三种权衡。

### SigLIP 2：NaFlex 和密集特征

SigLIP 2（2025）增加了：
- NaFlex：单一模型处理可变宽高比和分辨率。
- 更好的密集特征用于分割和深度估计，目标是作为 VLM 中冻结骨干使用。
- 多语言：在 100+ 语言上训练，而 CLIP 仅限英语。
- 1B 参数规模，CLIP 最高到 400M。

2026 年开源 VLM 中，SigLIP 2 SO400m/14 是默认视觉塔。CLIP 仍然是纯图文检索的默认选择，前提是特定的 LAION-2B 训练分布与你的查询模式匹配。

### ALIGN、BASIC、OpenCLIP、EVA-CLIP

ALIGN（Google，2021）：与 CLIP 相同的想法，18 亿对规模，90% 噪声。证明了噪声数据可以扩展。OpenCLIP（LAION）：CLIP 在 LAION-400M / 2B 上的开源复现，多种规模，首选开源检查点。EVA-CLIP：从掩码图像建模初始化；VLM 的强骨干。BASIC：Google 的 CLIP+ALIGN 混合。都是同一家族，不同的数据和调优。

### 零样本天花板

CLIP 类模型在 ImageNet 零样本上约 76% 封顶（CLIP-G、OpenCLIP-G）。超越需要要么更大的数据（SigLIP 2 达到 80%+），要么架构改变（监督头、更多参数）。基准正在饱和；真正的价值是下游 VLM 消费的嵌入空间。

## 用框架实现

`code/main.py` 实现了：

1. 一个玩具双编码器（基于哈希的图像特征、文本字符特征），这样你可以在不用 numpy 的情况下看到 InfoNCE 的形状。
2. 纯 Python 的 InfoNCE 损失（通过 log-sum-exp 实现数值稳定性）。
3. 用于比较的 Sigmoid 逐对损失。
4. 一个零样本分类例程：计算与一组文本提示的余弦相似度，argmax 作为预测。

运行它并观察损失曲线。绝对数字是玩具级别的；形状与真正的 CLIP 训练器输出的匹配。

## 产出物

本课产出 `outputs/skill-clip-zero-shot.md`。给定一组图像（通过路径）和目标类别列表，它用 CLIP 模板构建文本提示，用指定检查点（如 `openai/clip-vit-large-patch14`）嵌入两侧，返回 top-1 / top-5 预测和相似度分数。该技能拒绝就提示列表中不存在的类别做出声明。

## 练习题

1. 手动为 4 对批量实现 InfoNCE。构建 4x4 相似度矩阵，运行 softmax，提取对角线，计算交叉熵。用你的 Python 实现验证这个手动计算。

2. SigLIP 在温度之外还使用了偏置参数 `b`：`S'[i,j] = S[i,j]/tau + b`。当批量有大的类别不平衡（每行负样本远多于正样本）时，`b` 起什么作用？阅读 SigLIP 第 3 节（arXiv:2303.15343）。

3. 为猫 vs 狗构建零样本分类器。尝试两种提示模板：`a photo of a {class}` 和 `a picture of a {class}`。在 100 张测试图像上测量准确率。模板集成是否超越单一模板？

4. 计算 512 GPU 批量 32k 的 softmax InfoNCE vs sigmoid 逐对的通信成本。哪个是 O(N)，哪个是 O(N^2)？引用 SigLIP 第 4 节。

5. 阅读 OpenCLIP 缩放定律论文（arXiv:2212.07143，Cherti 等人）。从图表复现他们关于数据缩放的结论：在固定模型大小下，ImageNet 零样本准确率与训练数据量之间的对数线性关系是什么？

## 术语速查表

| 术语 | 常见说法 | 实际含义 |
|------|---------|---------|
| InfoNCE | "对比损失" | 批量相似度矩阵上的交叉熵；每项的正样本是其配对项，负样本是其他一切 |
| Sigmoid 损失 | "SigLIP 损失" | 逐对二元交叉熵；无 softmax，无全归约，分布式训练中扩展成本低 |
| 温度 | "tau" | softmax/sigmoid 前缩放 logits 的标量；控制分布的锐度 |
| 零样本 | "无需微调分类" | 使用文本提示构建类别嵌入并通过余弦相似度分类；无需在目标类别上训练 |
| 提示模板 | "a photo of a ..." | 围绕类别名称的文本脚手架；影响零样本准确率 1-5 分 |
| 双编码器 | "双塔" | 一个图像编码器 + 一个文本编码器，在共享 D 维空间中输出 |
| 硬负样本 | "困难干扰项" | 与正样本足够相似的负样本，模型需要努力分离它们 |
| 线性探测 | "冻结 + 一层" | 仅在冻结特征之上训练线性分类器；衡量特征质量 |
| NaFlex | "原生灵活分辨率" | SigLIP 2 无需调整大小即可接收任意宽高比和分辨率图像的能力 |
| 温度缩放 | "对数参数化 tau" | CLIP 参数化 `log(1/tau)` 使梯度行为良好；裁剪以防止崩溃到接近零的 tau |

## 延伸阅读

- [Radford 等人 — Learning Transferable Visual Models From Natural Language Supervision (arXiv:2103.00020)](https://arxiv.org/abs/2103.00020) — CLIP 论文。
- [Zhai 等人 — Sigmoid Loss for Language Image Pre-Training (arXiv:2303.15343)](https://arxiv.org/abs/2303.15343) — SigLIP。
- [Tschannen 等人 — SigLIP 2 (arXiv:2502.14786)](https://arxiv.org/abs/2502.14786) — 多语言 + NaFlex。
- [Jia 等人 — ALIGN (arXiv:2102.05918)](https://arxiv.org/abs/2102.05918) — 用噪声网络数据扩展。
- [Cherti 等人 — Reproducible scaling laws for contrastive language-image learning (arXiv:2212.07143)](https://arxiv.org/abs/2212.07143) — OpenCLIP 缩放定律。
