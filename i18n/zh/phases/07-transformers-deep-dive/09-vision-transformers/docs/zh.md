# 视觉变换器 (ViT)

> 一个图像是一个补丁格,一个句子是一个代币格,一个变压器吃了两者.

> **【中文解读】**维特 把图像切成补丁 当作代币序列处理――理解维特 =理解变压器 不限于NLP――CLIP、DALL-E、Sora 都基于变压器――

**Type:** Hands-on | **类型:** 动手
**Language:**子**语言:**字符串
**Prerequisites:** Phase 7 · 05 (Full Transformer), Phase 4 · 03 (CNNs), Phase 4 · 14 (Vision Transformers intro) | **前置知识:** Phase 7 · 05 (Full Transformer), Phase 4 · 03 (CNNs), Phase 4 · 14 (Vision Transformers intro)
**Time:** ~45 minutes | **时间:** ~45 分钟

## 问题 问题引入

在2020年前,计算机视觉意味着曲.每一个图像网上的SOTA,COCO和检测基准都使用了CNN的脊柱.变体是语言.

> 在2020年之前,计算机视觉意味着卷积. 图像网,COCO和检测基准上的每个SOTA都使用了CNN骨干网络.

东索维茨基及其他 (2020) "一个图像值16x16字" 显示你可以完全放下曲.切片图像成固定尺寸的补丁,线性投影每个补丁成嵌入,将序列输送到尼拉变压器编码器.在足够的规模 (ImageNet-21k预训或更大),ViT匹配或超过ResNet基于的模型.

> 东苏维茨基等(2020) "一张图像值16x16个词"证明可以完全放弃卷积──将图像切成固定大小的补丁,线性投影每个补丁为嵌入,将序列送入标准变压器编码器──在足够大的规模下(ImageNet-21k 预训练或更大),ViT可以匹配或超越基于ResNet的模型──

维特是2026年开始的更广泛模式:一个架构,许多模式. 语标记音频.维特标记图像. 机器人的行动代币. 视频的像素代币. 变压器不关心给它一个序列,它学习.

> 视频是2026年更广泛的趋势的起点:一种架构,多种模态――语将音频代币化―― 视频将图像代币化――机器人的动作代币―― 视频的像素代币―― 变压器不关乎给它一个序列,它就能学习――

到2026年,ViT及其后代 (DeiT,Swin,DINOv2,ViT-22B,SAM3) 拥有大部分视觉.CNN仍然在边缘设备和延迟敏感任务上获胜.其他所有东西都在堆中有ViT.

> 到2026年,越南电视台及其后代 (DeiT、Swin、DINOv2、ViT-22B、SAM 3) 占据了视觉领域的大部分.

> **【中文解读】**图像可以像文本一样被切成"标记"序列.将224x224图像切成14x14个16x16补丁,每个补丁都展现平线后线性投影为嵌入量,然后送入标准变压器编码器. 这证明了变压器的通用性不仅限于NLP,任何可以"分块序列化"的数据都适用.

## 概念的核心概念

![Image → patches → tokens → transformer](../assets/vit.svg)

### 步骤 1  补丁

分开一个`H × W × C`图像成一个`N × (P·P·C)`片的序列. 典型的设置: `224 × 224`图像`16 × 16`补丁 → 196个补丁,每个值为 768 个.

> 将`H × W × C`图像分为`N × (P·P·C)`的平补丁序列──典型设置:`224 × 224`图像,`16 × 16`补丁 → 196 个 768 值的补丁

```
image (224, 224, 3) → 14 × 14 grid of 16x16x3 patches → 196 vectors of length 768
```

补丁尺寸是杆. 较小的补丁 = 更多的代币,更好的分辨率,方形注意力成本.较大的补丁 = 粗,更便宜.

> 补丁大小是控制参数――更小的补丁 = 更多的代币、更好的分辨率、第二次注意力成本――更大的补丁 = 更粗、更便宜――

### 步骤 2 线性嵌入

一个学习的矩阵将每个平面补丁投射到`d_model`相当于一个核子大小的卷积`P`走进步`P`在PyTorch中,这字面上是`nn.Conv2d(C, d_model, kernel_size=P, stride=P)`两行实施.

> 一个学习到的矩阵将每个平面补丁投影到`d_model`△等价于核大小为`P`步长为`P`在 PyTorch 中就是`nn.Conv2d(C, d_model, kernel_size=P, stride=P)`两行实现.

> **【拓展：Swin Transformer 的层级设计】**标准ViT 使用固定补丁 大小和全局注意力,计算量 O(N^2)。Swin变压器 引入层次结构:在小补丁上做局部窗口注意力,逐层合并补丁 扩大感受野──这使得计算复杂性变为O(N),同时保留层次特征提取的能力──Swin 在检测和分类任务中仍然优于标准ViT──

### 步骤 3 预备`[CLS]`代码,添加位置嵌入

- 准备一个可学习的东西`[CLS]`它们的最后隐藏状态是用于分类的图像表示.
  中文翻译:在开头添加一个可学习的`[CLS]`标志──其最终隐藏状态用于分类图像表示──
- 添加可学习的位置嵌入式 (ViT原始) 或双向二维 (后代变体).
  中文翻译:添加可学习的位置嵌入 (ViT 原始版) 或正弦 2D嵌入 (后续变体) 。
- 在2024+ RoPE 扩展到2D位置,有时没有明确的嵌入.
  中文翻译:2024年后,RoPE 扩展到2D位置编码,有时不需要显式嵌入.

### 步骤 4 标准变压器编码器

堆积 L 块`LayerNorm → Self-Attention → + → LayerNorm → MLP → +`没有视觉特定层次.这是论文的教学性突破.

> 堆叠的`LayerNorm → Self-Attention → + → LayerNorm → MLP → +`块──与BERT完全相同──没有视觉特有的层──这是这篇论文的教学要点──

### 步骤 5 头

为了分类: 取`[CLS]`隐藏状态 →线性 →软max.对于DINOv2或SAM,丢弃`[CLS]`直接使用嵌件.

> 分类:取`[CLS]`隐藏状态 → 线性层 →软max──对于DINOv2或 SAM,丢弃`[CLS]`直接使用补丁嵌入.

### 重要的是哪些变体

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

### 为什么这需要一段时间

由于没有任何 CNN 诱导偏见 (翻译不变,本地).没有100万以上标记图像或强大的自我监督预训练,CNN 仍然在匹配计算中获胜. DeiT 在2021年通过蒸技巧解决了这一问题; DINOv2在2023年通过自我监督永久解决了这一问题.

> 由于没有CNN的归纳偏好 (平移不变性,局部性) 并且没有超过10亿张标记图像或强自监督预训练,CNN在相同的计算下仍然取得了成功.

> **【中文解读】**由于CNN天生具有平移不变性和局部性归纳偏好,因此需要更多的数据来匹配CNN的性能.

> **【拓展：ViT 在多模态系统中的角色】**通过对比学习对齐两模态――DALL-E 和 Sora 使用 ViT理解图像/视频,再生成新内容――SAM(部分任何) 使用 ViT 作为主干网络实现通用图像分区――ViT 已成为多模态 AI 的视觉基础模块――

## 建立它,实现它.
```figure
n5-patch-stream
```

## 建立它

看到`code/main.py`没有实在规模的 ViT 需要 PyTorch 和数小时的 GPU 时间.

> 参见`code/main.py`△纯标准库的补丁+线性嵌入+合理性检查――无训练任何实际规模的VIT都需要PyTorch和数小时的GPU时间――

### 步骤1:假图像

作为列列的24 × 24 RGB图像`(R, G, B)`我们使用6×6补丁 →16补丁,每一个108D嵌入向量.

> 一个24×24RGB图像,以`(R, G, B)`元组的行列表形式表示──使用6×6补丁 →16个补丁,每个108维嵌入向量──

### 步骤 2: 补丁

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

拉斯特序列:在网格上排列大.每个VIT都使用这种序列.

> 光顺序:网格上按行优先遍历.每个VT都使用这种排序.

### 步骤3:线性嵌入

乘以随机的每一个平面块`(patch_flat_size, d_model)`检查输出形状是`(N_patches + 1, d_model)`在预定后`[CLS]`现在,我们要去.

> 将每一个平补丁乘以一个随机`(patch_flat_size, d_model)`矩阵――验证在添加`[CLS]`后输出形状为`(N_patches + 1, d_model)`,我知道.

### 步骤4:对现实 ViT 计算参数

打印VIT-Base的参数数量:12层,12头,d=768,补丁=16.比较ResNet-50 (~25M).VIT-Base降落在~86M.VIT-Large~307M.VIT-Huge~632M.

> 打印ViT-Base的参数:12层、12头、d=768、补丁=16──与ResNet-50(约25M)对比──ViT-Base约86M──ViT-Large约307M──ViT-Huge约632M──

## 用它实现框架

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

**DINOv2 embeddings are the 2026 default for image features.**结脊椎,训练一个小头. 工作于分类,检索,检测,字幕. 测试点DINOv2超越Clip在任何非文字视觉任务.

> **DINOv2 嵌入是 2026 年图像特征的默认选择。**结骨干网络,训练一个小头――适用于分类,检查,检测,图像描述――Meta 的 DINOv2 检查点在每个非文本视觉任务上都优于 CLIP――

**Patch-size picking.**小型模型使用16×16 (ViT-B/16).密集预测 (细分) 使用8×8或14×14 (SAM,DINOv2).非常大的模型使用14×14.

> **Patch 大小选择。**小模型使用16×16(ViT-B/16)。密集预测(分割) 使用8×8或14×14(SAM、DINOv2)。非常大的模型使用14×14。

## 运送它.

看到`outputs/skill-vit-configurator.md`技能选择了 ViT 变体和补丁大小,以应对新的视觉任务,因为数据集的尺寸,分辨率和计算预算.

> 参见`outputs/skill-vit-configurator.md`△该技能根据数据集大小、分辨率和计算预算,为新视觉任务选择VIT 变体和补丁大小──

## 练习题

1. **Easy.**跑步`code/main.py`检查补丁数量是相同的`(H/P) * (W/P)`并且平面补丁的尺寸等于`P*P*C`现在,我们要去.
   中文翻译:运行 `code/main.py`△验证补丁 数量等于`(H/P) * (W/P)`平补丁维度等于`P*P*C`,我知道.
2. **Medium.**实现2D突形位置嵌入 两个独立的突形代码`row`其他`col`它们被入一个小的 PyTorch ViT 中,并将CIFAR-10的位置嵌入式与可学习的位置嵌入式进行比较.
   中文翻译:实现2D正弦位置嵌入每个补丁的`row`和 `col`独立编码后拼音──在小型 PyTorch ViT 上使用,与可学习位置嵌入 CIFAR-10 上对比准确率──
3. **Hard.**建立一个3层的ViT (PyTorch),训练1000个MNIST图像,使用4×4补丁.测试精度.现在添加DINOv2预训练在相同的1000个图像上 (简单化:只需训练编码器预测从掩盖补丁的补丁).是否提高精度?
   中文翻译:构建3层ViT(PyTorch),使用4×4补丁 在1000张MNIST图像上训练――测量测试准确率――然后添加DINOv2 预训练(简化版:训练编码器从掩码补丁 预测补丁 嵌入) ――准确率是否提升?

## 关键词 快速查找表

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

## 继续阅读 继续阅读

- [Dosovitskiy et al. (2020). An Image is Worth 16x16 Words: Transformers for Image Recognition at Scale](https://arxiv.org/abs/2010.11929)VIT的论文.
  中文翻译:ViT 原始论文。
- [Touvron et al. (2021). Training data-efficient image transformers & distillation through attention](https://arxiv.org/abs/2012.12877)  
  中文翻译:DeiT论文。
- [Liu et al. (2021). Swin Transformer: Hierarchical Vision Transformer using Shifted Windows](https://arxiv.org/abs/2103.14030) 
  中文翻译:Swin变压器论文.
- [Oquab et al. (2023). DINOv2: Learning Robust Visual Features without Supervision](https://arxiv.org/abs/2304.07193)   
  中文翻译:DINOv2论文──
- [Darcet et al. (2023). Vision Transformers Need Registers](https://arxiv.org/abs/2309.16588) DINOv2 的注册代码固定.
  中文翻译:DINOv2 的注册代码
