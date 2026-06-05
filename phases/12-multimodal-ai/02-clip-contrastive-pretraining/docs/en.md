# CLIP and Contrastive Vision-Language Pretraining | CLIP 图文对比预训练

> OpenAI's CLIP (2021) proved a single idea big enough to power the next five years: align an image encoder and a text encoder in the same vector space using only noisy web image-caption pairs and a contrastive loss. Zero supervised labels. 400M pairs. The resulting embedding space does zero-shot classification, image-text retrieval, and plugs into every 2026 VLM as its vision tower. SigLIP 2 (2025) replaced softmax with sigmoid and scaled past CLIP at lower cost. This lesson walks the math from InfoNCE to sigmoid pairwise loss and builds the training step in stdlib Python.

> **【中文解读】** CLIP 用4亿网络图文对，通过对比损失将图像和文本编码到同一向量空间。零标注实现零样本分类和图文检索，是所有2026年视觉语言模型的视觉塔基础。

> **【拓展：CLIP→多模态大模型】** CLIP 的图文对比学习是 LLaVA、BLIP-2 等多模态大模型的基础。理解 CLIP 是理解整个多模态 AI 生态的起点。

**Type:** Build | **类型:** 构建
**Languages:** Python (stdlib, InfoNCE + sigmoid loss implementations) | **语言:** Python（标准库，InfoNCE + sigmoid 损失实现）
**Prerequisites:** Phase 12 · 01 (ViT patches), Phase 7 (Transformers) | **前置知识:** Phase 12 · 01（ViT patch），Phase 7（Transformer）
**Time:** ~180 minutes | **时间:** ~180 分钟

## Learning Objectives | 学习目标

- Derive InfoNCE loss from mutual information and implement a numerically-stable vectorized version.
  中文翻译：从互信息推导 InfoNCE 损失，并实现数值稳定的向量化版本。
- Explain why sigmoid pairwise loss (SigLIP) scales to batch 32768+ without the all-gather overhead softmax demands.
  中文翻译：解释为什么 sigmoid 成对损失（SigLIP）可以扩展到 32768+ 批次大小，而无需 softmax 所需的 all-gather 开销。
- Run zero-shot ImageNet classification by constructing text templates (`a photo of a {class}`) and taking argmax over cosine similarity.
  中文翻译：通过构建文本模板（`a photo of a {class}`）并对余弦相似度取 argmax 来运行零样本 ImageNet 分类。
- Name the four levers CLIP / SigLIP pretraining gives you: batch size, temperature, prompt template, data quality.
  中文翻译：列举 CLIP / SigLIP 预训练给你的四个杠杆：批次大小、温度、提示模板、数据质量。

## The Problem | 问题引入

Pre-CLIP vision was supervised. Collect labeled datasets (ImageNet: 1.2M images, 1000 classes), train a CNN, ship it. Labels are expensive, labels bias to what labelers can agree on, and labels do not transfer to new tasks without finetuning.

> CLIP 之前的视觉是监督式的。收集标注数据集（ImageNet：120 万张图像，1000 个类别），训练 CNN，部署。标注昂贵，标注偏向标注者能达成共识的内容，而且标注不通过微调就无法迁移到新任务。

The image-caption web has one billion-plus loosely-labeled pairs for free. A picture of a golden retriever with alt text "my dog Max in the park" carries a supervisory signal — the text describes the image. The question: can you turn this into useful training?

> 网络上有超过十亿的松散标注图文对可供免费使用。一张金毛猎犬的照片配有 alt 文本"我的狗 Max 在公园里"携带了监督信号——文本描述了图像。问题是：你能把这变成有用的训练吗？

CLIP's answer: treat image-caption pairs as a matching task. Given a batch of N images and N captions, learn to match each image to its own caption against N-1 distractors. The supervision is "these two things belong together; these N-1 do not." No class labels. No human annotation. Just a contrastive loss.

> CLIP 的答案：将图文对视为匹配任务。给定一批 N 张图像和 N 条描述，学习在 N-1 个干扰项中将每张图像匹配到自己的描述。监督信号是"这两样东西属于一起；这 N-1 个不属于"。没有类别标签，没有人工标注，只有对比损失。

The resulting embedding space does more than CLIP was trained for. ImageNet zero-shot works because "a photo of a cat" embeds near pictures of cats that were never explicitly labeled cats. This is the bet that spawned every 2026 VLM.

> 得到的嵌入空间超越了 CLIP 的训练目标。ImageNet 零样本分类有效，因为"a photo of a cat"嵌入到从未被显式标注为猫的猫图片附近。这就是催生所有 2026 年 VLM 的赌注。

## The Concept | 核心概念

> **【中文解读】** CLIP（Contrastive Language-Image Pre-training）通过对比学习将图像和文本映射到同一向量空间：匹配的图文对距离拉近，不匹配的推远。CLIP 在 4 亿图文对上训练后，无需微调即可实现 zero-shot 图像分类，是 OpenAI 多模态能力的基石。

> **【拓展：CLIP 的应用生态】** CLIP 的对比学习范式催生了大量应用：DALL-E 2/3 用 CLIP 引导图像生成，Stable Diffusion 用 OpenCLIP 作为安全过滤器，LLaVA 用 CLIP 视觉编码器连接 LLM 和图像理解。CLIP 的 zero-shot 能力在 ImageNet 上达到 76.2% top-1 准确率，无需任何 ImageNet 训练数据。


> **【拓展：CLIP 的 zero-shot 能力】** CLIP 最惊人的能力是 zero-shot 分类——不需要任何下游任务的训练数据，只需给出类别名称就能分类图像。在 ImageNet 上，CLIP ViT-L/14 的 zero-shot 准确率（76.2%）接近 ResNet-50 的全监督准确率（76.7%）。这种能力来自 4 亿图文对的对比学习。


### The dual encoder

CLIP has two towers:

> CLIP 有两个塔：

- Image encoder `f`: ViT or ResNet, outputs a D-dim vector per image.
  中文翻译：图像编码器 `f`：ViT 或 ResNet，每张图像输出一个 D 维向量。
- Text encoder `g`: small transformer, outputs a D-dim vector per caption.
  中文翻译：文本编码器 `g`：小型 Transformer，每条描述输出一个 D 维向量。

Both towers normalize their outputs to unit length. Similarity is `cos(f(x), g(y)) = f(x)^T g(y)` since both are unit-norm.

> 两个塔都将输出归一化为单位长度。相似度为 `cos(f(x), g(y)) = f(x)^T g(y)`，因为两者都是单位向量。

For a batch of N (image, caption) pairs, build the similarity矩阵 `S` of shape `(N, N)`:

> 对于一批 N 个（图像，描述）对，构建形状为 `(N, N)` 的相似度矩阵 `S`：

```
S[i, j] = cos(f(x_i), g(y_j)) / tau
```

where `tau` is a learned temperature (CLIP initializes to 0.07; learned in log-space).

> 其中 `tau` 是一个可学习的温度参数（CLIP 初始化为 0.07；在对数空间中学习）。

### InfoNCE loss

CLIP uses a symmetric cross-entropy over rows and columns:

> CLIP 对行和列使用对称交叉熵：

```
loss_i2t = CE(S, labels=identity)     # each image's positive is its own caption
loss_t2i = CE(S^T, labels=identity)   # each caption's positive is its own image
loss = (loss_i2t + loss_t2i) / 2
```

This is InfoNCE. The softmax in CE forces each image to match its caption more than every other caption in the batch. The "negatives" are all other batch items. Bigger batches = more negatives = stronger signal. CLIP trained at batch 32k; scale matters.

> 这就是 InfoNCE。CE 中的 softmax 强制每张图像与自己的描述的匹配度高于批次中所有其他描述。"负样本"是批次中所有其他项。批次越大 = 负样本越多 = 信号越强。CLIP 在 32k 批次下训练；规模很重要。

### Temperature

`tau` controls the sharpness of the softmax. Low tau → sharp distribution, hard negative mining effect. High tau → soft, all samples contribute. CLIP learns log(1/tau), clipped to prevent collapse. SigLIP 2 fixes the initial tau and uses a learned bias instead.

> `tau` 控制 softmax 的锐度。低 tau → 尖锐分布，具有难负例挖掘效果。高 tau → 平滑，所有样本都有贡献。CLIP 学习 log(1/tau)，并裁剪以防止崩溃。SigLIP 2 固定初始 tau 并使用可学习的偏置代替。

### Why sigmoid scales better (SigLIP)

Softmax needs the whole similarity matrix in sync. In distributed training you must all-gather every embedding to every replica, then do the softmax. This is quadratic in world size for communication.

> Softmax 需要整个相似度矩阵同步。在分布式训练中，你必须将每个嵌入 all-gather 到每个副本，然后做 softmax。通信开销与世界大小呈二次关系。

SigLIP replaces softmax with element-wise sigmoid: for each pair `(i, j)`, the loss is a binary classification of "are these the matching pair?" positive class labels are the diagonal, everything else is negative. The loss is:

> SigLIP 用逐元素 sigmoid 替换 softmax：对于每对 `(i, j)`，损失是对"它们是否是匹配对？"的二分类。正类标签是对角线，其他都是负类。损失为：

```
L = -1/N sum over (i, j) [ y_ij log sigmoid(S[i,j]) + (1-y_ij) log sigmoid(-S[i,j]) ]
```

`y_ij = 1` if `i == j`, else 0. Each pair's loss is independent. No all-gather needed. Each GPU computes its local block and sums. SigLIP 2 scales to batch 32k-512k cheaply where CLIP would need proportionally more communication.

> `y_ij = 1` 如果 `i == j`，否则为 0。每对的损失是独立的。不需要 all-gather。每个 GPU 计算其本地块并求和。SigLIP 2 可以低成本扩展到 32k-512k 批次，而 CLIP 需要相应更多的通信。

### Zero-shot classification

Given N class names, for each class build a text template:

> 给定 N 个类别名称，为每个类别构建文本模板：

```
"a photo of a {class}"
```

Embed each template with the text encoder. Embed your image with the image encoder. Argmax cosine similarity = predicted class. No training on the target classes.

> 用文本编码器嵌入每个模板。用图像编码器嵌入图像。Argmax 余弦相似度 = 预测类别。无需在目标类别上训练。

Prompt templates matter. CLIP's original paper used 80 templates per class (plain, artistic, photo, painting, etc.) and averaged the embeddings. +3 ImageNet points. Modern usage typically picks one or two templates.

> 提示模板很重要。CLIP 原始论文每类使用 80 个模板（普通、艺术、照片、绘画等）并对嵌入取平均。ImageNet 上提升 3 个百分点。现代用法通常选择一两个模板。

### Linear probes and finetuning

Zero-shot is a baseline. A linear probe (train one linear layer on top of frozen CLIP features for your target classes) beats zero-shot on in-domain tasks. Full finetuning beats linear probe on in-domain but can hurt zero-shot transfer. Three regimes with three trade-offs.

> 零样本是基线。线性探测（在冻结的 CLIP 特征之上为目标类别训练一个线性层）在域内任务上超越零样本。全量微调在域内超越线性探测，但可能损害零样本迁移。三种模式，三种权衡。

### SigLIP 2: NaFlex and dense features

SigLIP 2 (2025) adds:

> SigLIP 2（2025）添加了：

- NaFlex: single model handles variable aspect ratios and resolutions.
  中文翻译：NaFlex：单一模型处理可变宽高比和分辨率。
- Better dense features for segmentation and depth estimation, targeting use as a frozen backbone in VLMs.
  中文翻译：更好的密集特征用于分割和深度估计，目标是在 VLM 中作为冻结主干网络。
- Multilingual: trained on 100+ languages where CLIP was English-only.
  中文翻译：多语言：在 100+ 种语言上训练，而 CLIP 仅限英文。
- 1B param scale where CLIP topped out at 400M.
  中文翻译：10 亿参数规模，而 CLIP 最高为 4 亿。

In 2026 open VLMs, SigLIP 2 SO400m/14 is the default vision tower. CLIP remains the default for pure image-text retrieval where the specific LAION-2B training distribution matches your query pattern.

> 在 2026 年的开放 VLM 中，SigLIP 2 SO400m/14 是默认视觉塔。CLIP 在纯图文检索中仍是默认选择，特别是当特定 LAION-2B 训练分布匹配你的查询模式时。

### ALIGN, BASIC, OpenCLIP, EVA-CLIP

ALIGN (Google, 2021): same idea as CLIP, 1.8B pair scale, 90% noisy. Proved noisy data scales. OpenCLIP (LAION): open reproduction of CLIP on LAION-400M / 2B, multiple scales, the go-to open checkpoint. EVA-CLIP: initializes from masked image modeling; strong backbone for VLMs. BASIC: Google's CLIP+ALIGN hybrid. All the same family, different data and tuning.

> ALIGN（Google，2021）：与 CLIP 相同的想法，18 亿对规模，90% 噪声数据。证明了噪声数据可以扩展。OpenCLIP（LAION）：在 LAION-400M / 2B 上的 CLIP 开放复现，多种规模，首选的开放检查点。EVA-CLIP：从掩码图像建模初始化；VLM 的强主干网络。BASIC：Google 的 CLIP+ALIGN 混合。都属于同一家族，不同的数据和调优。

### The zero-shot ceiling

CLIP-class models cap around 76% ImageNet zero-shot (CLIP-G, OpenCLIP-G). Beyond requires either much larger data (SigLIP 2 gets 80%+) or architecture changes (supervised heads, more parameters). The benchmark is saturating; the real value is the embedding space that downstream VLMs consume.

> CLIP 类模型在 ImageNet 零样本分类上的上限约为 76%（CLIP-G、OpenCLIP-G）。超越这一水平需要更大的数据（SigLIP 2 达到 80%+）或架构变更（监督头、更多参数）。基准测试正在饱和；真正的价值在于下游 VLM 消费的嵌入空间。

## Use It | 用框架实现

`code/main.py` implements:

> `code/main.py` 实现了：

1. A toy dual encoder (hash-based image features, text char features) so you can see the InfoNCE shape without numpy.
   中文翻译：一个玩具双编码器（基于哈希的图像特征、文本字符特征），无需 numpy 即可看到 InfoNCE 的形态。
2. InfoNCE loss in pure Python (numerical stability via log-sum-exp).
   中文翻译：纯 Python 实现的 InfoNCE 损失（通过 log-sum-exp 实现数值稳定性）。
3. Sigmoid pairwise loss for comparison.
   中文翻译：Sigmoid 成对损失用于对比。
4. A zero-shot classification routine: compute cosine similarity against a set of text prompts, argmax for prediction.
   中文翻译：零样本分类例程：计算与一组文本提示的余弦相似度，argmax 得出预测。

Run it and watch the loss curve. The absolute numbers are toy; the shape matches what a real CLIP trainer emits.

> 运行它并观察损失曲线。绝对数值是玩具级的；但形状与真实 CLIP 训练器的输出匹配。

## Ship It | 产出物

This lesson produces `outputs/skill-clip-zero-shot.md`. Given a set of images (via path) and a list of target classes, it builds text prompts with the CLIP template, embeds both sides with a stated checkpoint (e.g., `openai/clip-vit-large-patch14`), and returns top-1 / top-5 predictions with similarity scores. The skill refuses to make claims about classes not in the prompt list.

> 本课产出 `outputs/skill-clip-zero-shot.md`。给定一组图像（通过路径）和一组目标类别，它用 CLIP 模板构建文本提示，用指定的检查点（如 `openai/clip-vit-large-patch14`）嵌入两侧，并返回带有相似度分数的 top-1 / top-5 预测。该 skill 拒绝对不在提示列表中的类别做出判断。

## Exercises | 练习题

1. Implement InfoNCE for a batch of 4 pairs by hand. Construct the 4x4 similarity matrix, run softmax, pick out the diagonal, compute cross-entropy. Verify your Python implementation against this hand calculation.
   中文翻译：手动实现 4 对样本的 InfoNCE。构建 4x4 相似度矩阵，运行 softmax，提取对角线，计算交叉熵。验证你的 Python 实现与手算一致。

2. SigLIP uses a bias parameter `b` in addition to temperature: `S'[i,j] = S[i,j]/tau + b`. What role does `b` play when the batch has a large class imbalance (many more negatives than positives per row)? Read SigLIP Section 3 (arXiv:2303.15343).
   中文翻译：SigLIP 除了温度还使用偏置参数 `b`：`S'[i,j] = S[i,j]/tau + b`。当批次存在大的类别不平衡（每行负样本远多于正样本）时，`b` 起什么作用？阅读 SigLIP 第 3 节（arXiv:2303.15343）。

3. Build a zero-shot classifier for cats vs dogs. Try two prompt templates: `a photo of a {class}` and `a picture of a {class}`. Measure accuracy on 100 test images. Does the ensemble of templates beat single?
   中文翻译：构建猫狗零样本分类器。尝试两种提示模板：`a photo of a {class}` 和 `a picture of a {class}`。在 100 张测试图像上测量准确率。模板集成是否优于单一模板？

4. Compute the communication cost of softmax InfoNCE vs sigmoid pairwise for a 512-GPU run at batch 32k. Which scales as O(N), which as O(N^2)? Cite SigLIP Section 4.
   中文翻译：计算 512 GPU、批次 32k 下 softmax InfoNCE 与 sigmoid 成对损失的通信成本。哪个是 O(N)，哪个是 O(N^2)？引用 SigLIP 第 4 节。

5. Read the OpenCLIP scaling-laws paper (arXiv:2212.07143, Cherti et al.). Reproduce their conclusion for data scaling from the figures: at fixed model size, what is the log-linear relationship between ImageNet zero-shot accuracy and training data size?
   中文翻译：阅读 OpenCLIP 缩放定律论文（arXiv:2212.07143，Cherti 等人）。从图表中复现他们关于数据扩展的结论：在固定模型大小下，ImageNet 零样本准确率与训练数据大小之间的对数线性关系是什么？

## Key Terms | 术语速查表

| Term | What people say | What it actually means | 中文释义 |
|------|----------------|------------------------|---------|
| 术语 | 通俗说法 | 实际含义 | |
| InfoNCE | "Contrastive loss" | Cross-entropy over a batch's similarity matrix; each item's positive is its paired item, negatives are everything else | 批次相似度矩阵上的交叉熵；每项的正样本是其配对项，负样本是所有其他项 |
| Sigmoid loss | "SigLIP loss" | Per-pair binary cross-entropy; no softmax, no all-gather, scales cheaply in distributed training | 逐对二分类交叉熵；无 softmax，无 all-gather，分布式训练中扩展成本低 |
| Temperature | "tau" | Scalar that scales logits before softmax/sigmoid; controls sharpness of the distribution | softmax/sigmoid 前缩放 logits 的标量；控制分布的锐度 |
| Zero-shot | "no-finetune classification" | Use text prompts to construct class embeddings and classify by cosine similarity; no training on target classes | 用文本提示构建类别嵌入，通过余弦相似度分类；无需在目标类别上训练 |
| Prompt template | "a photo of a ..." | Text scaffold around a class name; affects zero-shot accuracy by 1-5 points | 类别名周围的文本支架；影响零样本准确率 1-5 个百分点 |
| Dual encoder | "Two-tower" | One image encoder + one text encoder, outputs in shared D-dim space | 一个图像编码器 + 一个文本编码器，输出在共享的 D 维空间 |
| Hard negative | "Tough distractor" | A negative similar enough to the positive that the model has to work to separate them | 与正样本足够相似的负样本，模型需要努力区分它们 |
| Linear probe | "Frozen + one layer" | Train only a linear classifier on top of frozen features; measures feature quality | 仅在冻结特征之上训练线性分类器；衡量特征质量 |
| NaFlex | "Native flexible resolution" | SigLIP 2 capability to ingest images at any aspect ratio and resolution without resizing | SigLIP 2 以任意宽高比和分辨率输入图像的能力，无需调整大小 |
| Temperature scaling | "log-parametrized tau" | CLIP parametrizes `log(1/tau)` so gradients behave; clips to prevent collapse to near-zero tau | CLIP 参数化 `log(1/tau)` 使梯度行为正常；裁剪防止 tau 崩溃到接近零 |

## Further Reading | 延伸阅读

- [Radford et al. — Learning Transferable Visual Models From Natural Language Supervision (arXiv:2103.00020)](https://arxiv.org/abs/2103.00020) — the CLIP paper.
  中文翻译：CLIP 论文。
- [Zhai et al. — Sigmoid Loss for Language Image Pre-Training (arXiv:2303.15343)](https://arxiv.org/abs/2303.15343) — SigLIP.
  中文翻译：SigLIP 论文。
- [Tschannen et al. — SigLIP 2 (arXiv:2502.14786)](https://arxiv.org/abs/2502.14786) — multilingual + NaFlex.
  中文翻译：多语言 + NaFlex。
- [Jia et al. — ALIGN (arXiv:2102.05918)](https://arxiv.org/abs/2102.05918) — scale with noisy web data.
  中文翻译：用噪声网络数据扩展。
- [Cherti et al. — Reproducible scaling laws for contrastive language-image learning (arXiv:2212.07143)](https://arxiv.org/abs/2212.07143) — OpenCLIP scaling laws.
  中文翻译：OpenCLIP 缩放定律。
