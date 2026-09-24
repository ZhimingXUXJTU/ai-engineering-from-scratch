# Vision Encoder Patches | 视觉编码器分块

> A vision model that reads pixels needs a tokenizer for pixels. Patch embedding is that tokenizer. Cut the image into a grid of squares, flatten each square, project it through one linear layer, then add a 2D position signal so the transformer knows where each square sat in the original image.

> **【中文解读】** 本课是"Build It / Use It"中 Build 侧的第一块砖：视觉编码器的分块（patch embedding）前端。视觉模型读的是像素，而 Transformer 吃的是向量序列——分块嵌入就是像素世界的"分词器"。流程是：把图像切成方块网格、每块展平、过一个线性层投影、再加二维位置信号，让模型知道每块原来在图中的位置。

> **【拓展：多模态视觉路线→整个 VLM 栈的地基】** CLIP、SigLIP、DINOv2、Qwen-VL、InternVL——2025-2026 年所有主流开源视觉-语言模型的视觉侧都从这个"Conv2d 分块投影 + 位置信号"前端起步。本课（58）搭建前端，59 课在其上叠 12 层 Transformer，60 课做模态对齐投影，61 课做交叉注意力融合，62 课做视觉-语言预训练——五课合成一条完整的多模态视觉路线。

> 🔗 **【前置】** 学本课前请先掌握：Phase 19 · 30-37（Track B 基础：BPE 分词器、位置嵌入、注意力机制从零实现）——本课把"序列 + 嵌入 + 位置"的同一套语言搬到图像域。

**Type:** Build | **类型:** 构建
**Languages:** Python | **语言:** Python
**Prerequisites:** Phase 19 lessons 30-37 (Track B foundations) | **前置知识:** Phase 19 · 30-37（Track B 基础）
**Time:** ~90 minutes | **时间:** 约 90 分钟

## Learning Objectives | 学习目标

- Tokenize an image into a fixed-length sequence of patch embeddings.
  中文翻译：把一张图像分块成固定长度的图像块嵌入序列。
- Implement a `Conv2d`-based patch projection that matches the math of unfold-then-linear.
  中文翻译：实现基于 `Conv2d` 的图像块投影，其数学结果与"展开后再线性"完全一致。
- Build a deterministic 2D sinusoidal position embedding so token order encodes spatial position.
  中文翻译：构建确定性的二维正弦位置嵌入，让词元顺序携带空间位置信息。
- Verify patch count, embedding shape, and `Conv2d`/unfold equivalence on a synthetic fixture.
  中文翻译：在合成测试图上验证图像块数量、嵌入形状以及 `Conv2d` 与 unfold 的等价性。

## The Problem | 问题引入

> **【中文解读】** 本节算清"为什么必须分块"这笔账。逐像素当词元会让 224x224 的图产生 150,528 个 token，注意力开销平方级爆炸；整图压成一个向量又丢掉局部性。图像块嵌入用一次线性投影折中：224x224 切成 16x16 的块得到 14x14=196 块，每块展平成 768 维向量再投影到隐藏维度——Transformer 看到的是 196+1 个词元，这是后续网络嚼得动的序列。

A transformer eats a sequence of vectors. An image is a 3-channel grid. Reading every pixel as a token explodes the sequence length: a 224x224 RGB image is 150,528 tokens, which a 12-layer transformer cannot afford in attention. Reading the image as one giant flat vector throws away locality, which the attention layer cannot recover from. The job of the encoder front end is to compress the pixel grid into a few hundred tokens that each summarize a square region.

> Transformer 吃的是向量序列，而图像是三通道网格。把每个像素当一个词元会让序列长度爆炸：一张 224x224 的 RGB 图是 150,528 个词元，12 层 Transformer 的注意力根本养不起。把整张图读成一个巨大的扁平向量又丢掉了局部性，注意力层也无法把它找回来。编码器前端的任务就是把像素网格压缩成几百个词元，每个词元概括一块方形区域。

Patch embedding solves this with one linear projection. A 224x224 image cut into 16x16 patches produces a 14x14 grid of 196 patches. Each patch is flattened from `(3, 16, 16) = 768` pixel values into one vector, then a linear layer maps it to the model's hidden dimension. The transformer sees 196 tokens of dimension `hidden` (commonly 768) plus a CLS token. That is a sequence the rest of the network can chew on.

> 图像块嵌入用一次线性投影解决这个问题。224x224 的图切成 16x16 的块得到 14x14 网格共 196 块。每块从 `(3, 16, 16) = 768` 个像素值展平成一个向量，再由线性层映射到模型的隐藏维度。Transformer 看到 196 个维度为 `hidden`（通常是 768）的词元外加一个 CLS 词元。这才是后续网络嚼得动的序列。

## The Concept | 核心概念

```mermaid
flowchart LR
  Image[224x224x3 image] --> Cut[cut into 16x16 patches]
  Cut --> Grid[14x14 grid of patches]
  Grid --> Flatten[flatten each patch]
  Flatten --> Proj[linear projection]
  Proj --> Tokens[196 tokens of dim hidden]
  Tokens --> Pos[add 2D sinusoidal position]
  Pos --> Out[final token sequence]
```

### Why patches, not pixels | 为什么用图像块而不是像素

> 💡 **【类比】** 分块像把一幅大拼图按 16x16 的格子"预组装"成 196 块中等碎片再交给整理师（Transformer）。逐像素等于把一万多粒散沙倒上台面，整理师连两两配对都做不完（注意力平方爆炸）；整图压一块等于把拼图直接绞碎成粉末，局部图案信息彻底没了。16x16 的碎片刚好保留"这一格里有猫耳朵边缘"级别的信号，又把整理量压到 196 件。

Attention is quadratic in sequence length. A 196-token sequence costs `196 * 196 = 38,416` attention scores per head per layer; a 150,528-token sequence costs `150,528 * 150,528 = 22.6 billion`. Patches buy a 590,000x reduction in attention compute, and a single 16x16 region carries enough signal for high-level vision tasks. The cost is a loss of fine-grained spatial detail inside one patch, which is why downstream multimodal stacks often run a second high-resolution branch when fine localization matters.

> 注意力开销与序列长度成平方关系。196 个词元的序列每头每层只需 `196 * 196 = 38,416` 个注意力分数；150,528 个词元的序列需要 `150,528 * 150,528 = 226 亿`。分块换来约 59 万倍的注意力算力缩减，而单个 16x16 区域携带的信号足以支撑高层视觉任务。代价是块内细粒度空间细节的丢失——这正是下游多模态栈在需要精细定位时另跑一条高分辨率分支的原因。

### Why a linear projection is enough | 为什么一层线性投影就够了

Each patch is treated as an independent vector. The projection learns a basis: edge detectors, color filters, simple textures. A single linear layer is small (`768 * 768 = 589,824` parameters for ViT-Base) and trains fast. Deeper convolutional stems exist (the "hybrid" ViT), but a flat linear projection is the standard, and most modern open-weight encoders ship with this exact shape.

> 每个图像块被当作独立向量处理。投影层学出的是一组基：边缘检测器、颜色滤波器、简单纹理。单层线性层很小（ViT-Base 为 `768 * 768 = 589,824` 个参数）且训练快。更深的卷积前端也存在（"混合式"ViT），但扁平的线性投影才是标准做法，大多数现代开源权重编码器出厂就是这个形状。

### The `Conv2d` trick | `Conv2d` 技巧

> **【中文解读】** `Conv2d(in_channels=3, out_channels=hidden, kernel_size=patch_size, stride=patch_size)` 不加 padding 时，数值上与"展开 + 线性层"完全等价——每个输出位置就是该块像素与一个滤波器的点积。生产代码库几乎都用卷积写法：GPU 上更快，还少一次 reshape。本课的测试正是验证这两种拼法逐位一致。

A `Conv2d(in_channels=3, out_channels=hidden, kernel_size=patch_size, stride=patch_size)` with no padding gives the same numerical result as unfold-then-linear, because each output position dot-products the patch pixels against one filter. The convolution is the patch projection, and most production codebases ship it that way because it is faster on GPU and uses one fewer reshape.

> `Conv2d(in_channels=3, out_channels=hidden, kernel_size=patch_size, stride=patch_size)` 不加 padding 时与"展开 + 线性"给出相同的数值结果，因为每个输出位置就是把图像块像素与一个滤波器做点积。这个卷积就是图像块投影，大多数生产代码库都这么写，因为 GPU 上更快、还省一次 reshape。

### Position embeddings | 位置嵌入

Tokens carry no order out of the projection. The 2D sinusoidal embedding gives each token a fixed signal that encodes its `(row, col)` position. Half the embedding dimension encodes row position with sin/cos at multiple frequencies; the other half encodes column position. The encoding is deterministic so you can swap resolutions without retraining, and it interpolates cleanly to grids the model never saw at training time.

> 词元走出投影层时并不携带顺序信息。二维正弦位置嵌入给每个词元一个固定信号，编码其 `(行, 列)` 位置：嵌入维度的一半用多频率 sin/cos 编码行位置，另一半编码列位置。该编码是确定性的，因此不重训也能换分辨率，还能干净地插值到训练时从未见过的网格。

| Component | Shape | Parameters |
|-----------|-------|------------|
| Patch projection (`Conv2d`) | `(hidden, 3, patch, patch)` | `3 * P * P * hidden + hidden` |
| Position embedding (fixed) | `(num_patches, hidden)` | 0 (computed, not learned) |
| CLS token (learned) | `(1, hidden)` | `hidden` |

For ViT-Base/16 at 224 resolution: 590,592 parameters in the projection, 768 in the CLS token, and zero for sinusoidal position. The next lesson (59) stacks a 12-layer transformer on top of this front end.

> 对 224 分辨率的 ViT-Base/16：投影层 590,592 个参数，CLS 词元 768 个，正弦位置编码零个。下一课（59）在这个前端之上叠一个 12 层 Transformer。

### Equivalence as a sanity check | 用等价性做健全性检查

The patch step has two spellings: a `Conv2d` projection and an explicit unfold-then-linear. They must produce the same output for the same weights. If they do not, the unfold math is wrong, and the rest of the encoder is built on sand. The tests in this lesson exercise that equivalence.

> 图像块这一步有两种拼法：`Conv2d` 投影和显式的"展开 + 线性"。同样的权重必须产生同样的输出。如果不一样，说明展开的数学写错了，编码器其余部分就是建在沙子上。本课的测试专门验证这个等价性。

```figure
ch-patch-tokenizer
```

## Build It | 动手实现

> **【中文解读】** `code/main.py` 用 PyTorch 实现了四个部件：`PatchEmbed`（包着 `Conv2d` 的图像块投影模块）、`sinusoidal_2d`（无状态的二维位置表构造函数）、`VisionFrontEnd`（分块嵌入 + CLS 前置 + 位置相加的一次前向组合）、`synthesize_image(seed)`（用 `numpy.random` 造确定性 224x224x3 测试图）。demo 跑一张测试图并打印输出形状、CLS 词元范数和位置嵌入的一行——范数在同一行内均匀，正是正弦编码的签名。

`code/main.py` implements:

- `PatchEmbed`, an `nn.Module` wrapping `Conv2d` for patch projection.
- `sinusoidal_2d(grid_h, grid_w, dim)`, a stateless function that builds the 2D position table.
- `VisionFrontEnd`, which composes patch embedding, CLS prepend, and position addition into one forward pass.
- A `synthesize_image(seed)` helper that builds a deterministic 224x224x3 fixture from `numpy.random`.
- A demo that runs one fixture image through the front end and prints the output shape, the CLS token norm, and one row of the position embedding.

Run it:

```bash
python3 code/main.py
```

Output: the 224x224 fixture is tokenized to a sequence of shape `(1, 197, 768)`. The first token is the CLS; the next 196 are patch tokens. The position embedding norms are uniform within a row, which is the sinusoidal signature.

> 输出：224x224 测试图被分块为形状 `(1, 197, 768)` 的序列。第一个词元是 CLS，后面 196 个是图像块词元。位置嵌入的范数在同一行内均匀一致，这正是正弦编码的签名。

## Use It | 用框架实现

> **【中文解读】** 同一个分块前端出现在每一个现代视觉-语言模型里：CLIP ViT-L/14、SigLIP、DINOv2、Qwen-VL 家族、InternVL 栈全都从"`Conv2d` 分块投影 + 位置信号"起步。各家族的差异都在下游（CLS 池化 vs 无 CLS 池化、register 词元、14 vs 16 的块大小、靠位置插值做动态分辨率）。本课的前端是所有这些模型共同站立的地基。

The same patch front end shows up in every modern vision-language model: CLIP ViT-L/14, SigLIP, DINOv2, the Qwen-VL family, and the InternVL stack all start from a `Conv2d` patch projection plus a position signal. Differences across families live downstream (CLS vs no-CLS pooling, register tokens, varying patch sizes 14 vs 16, dynamic resolution via interpolated positions). The frontend in this lesson is the substrate every one of those models stands on.

> 同一个分块前端出现在每一个现代视觉-语言模型中：CLIP ViT-L/14、SigLIP、DINOv2、Qwen-VL 家族和 InternVL 栈都从 `Conv2d` 分块投影加位置信号开始。各家族之间的差异都在下游（CLS 池化 vs 无 CLS 池化、register 词元、14 vs 16 的块大小差异、通过位置插值实现动态分辨率）。本课的前端是所有这些模型共同站立的地基。

## Tests | 测试

`code/test_main.py` covers:

- patch count matches `(image_size / patch_size) ** 2`
  中文翻译：图像块数量等于 `(image_size / patch_size) ** 2`。
- output shape matches `(batch, num_patches + 1, hidden)`
  中文翻译：输出形状为 `(batch, num_patches + 1, hidden)`。
- the `Conv2d` projection equals manual unfold-then-linear on a small fixture
  中文翻译：在小测试图上，`Conv2d` 投影与手工"展开 + 线性"逐位一致。
- sinusoidal position table is deterministic across calls
  中文翻译：正弦位置表跨调用保持确定性。
- CLS token broadcasts across batch dim without leakage
  中文翻译：CLS 词元在 batch 维度上广播且不发生串扰。

Run them:

```bash
python3 -m unittest code/test_main.py
```

## Exercises | 练习题

1. Replace the sinusoidal position with a learned `nn.Parameter` and compare the first-epoch loss on a tiny synthetic classification task. Learned positions win at fixed resolution; sinusoidal wins when you change resolution after training.
   中文翻译：把正弦位置换成可学习的 `nn.Parameter`，在微型合成分类任务上比较第一个 epoch 的损失。固定分辨率下可学习位置更优；训练后换分辨率则正弦编码胜出。

2. Swap the `Conv2d` for an explicit `nn.Unfold` plus `nn.Linear` and assert the outputs match to within float tolerance. Same math, two ways to spell it.
   中文翻译：把 `Conv2d` 换成显式的 `nn.Unfold` 加 `nn.Linear`，断言输出在浮点容差内一致。同一套数学，两种拼法。

3. Add support for non-square patch sizes (e.g. 32x16 for wide-aspect inputs) and verify the position table handles non-square grids.
   中文翻译：增加对非方形图像块的支持（如宽高比输入用 32x16），并验证位置表能处理非方形网格。

4. Profile the patch step at batch sizes 1, 8, 64. The patch projection is rarely the bottleneck; the attention layers downstream dominate.
   中文翻译：在 batch 为 1、8、64 下给分块步骤做性能剖析。图像块投影很少是瓶颈；下游的注意力层才占大头。

5. Train the front end as a frozen feature extractor on a 4-class synthetic shape dataset (circles, squares, triangles, stars). The CLS token output should linearly separate.
   中文翻译：把前端当冻结特征提取器，在四类合成形状数据集（圆、方、三角、星）上训练。CLS 词元输出应能被线性分开。

## Key Terms | 术语速查表

> **【中文解读】** 五个词锁定本课词汇：Patch（图像块）、Patch embedding（块嵌入）、Sequence length（分块后的序列长度，通常再加 CLS）、Sinusoidal position（正弦位置编码）、CLS token（可学习的池化头词元）。后续四课都在这套词汇上展开。

| Term | What it means |
|------|---------------|
| Patch | A square sub-region of the image, typically 14x14 or 16x16 |
| Patch embedding | Linear projection of one flattened patch to the hidden dim |
| Sequence length | Number of tokens after patch tokenization, usually plus CLS |
| Sinusoidal position | Fixed sin/cos signal that encodes 2D grid coordinates |
| CLS token | Learned vector prepended to the sequence as the pooling head |

## Further Reading | 延伸阅读

- An Image is Worth 16x16 Words (ViT, 2021) for the original patch-embed framing.
  中文翻译：《An Image is Worth 16x16 Words》（ViT，2021）——图像块嵌入的开山之作。
- Attention Is All You Need (2017) for the sinusoidal position formula adapted here to 2D.
  中文翻译：《Attention Is All You Need》（2017）——本课改编为二维的正弦位置公式出处。
- DINOv2 paper for register tokens, an extension you can add as exercise 6.
  中文翻译：DINOv2 论文——register 词元的出处，可作为附加练习自行扩展。
