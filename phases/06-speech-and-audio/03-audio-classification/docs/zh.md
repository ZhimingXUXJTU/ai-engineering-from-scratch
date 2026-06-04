# 音频分类 — 从 MFCCs+KNN 到 AST 和 BEATs

> 从"狗叫还是警笛"到"这是什么语言"，都是音频分类。特征用 Mel，架构每个时代都在变（MFCC+kNN -> CNN -> Transformer），评估指标始终是 AUC、F1 和每类召回率。AST（Audio Spectrogram Transformer，音频频谱图 Transformer）和 BEATs 是当前 SOTA。

> **【中文解读】** 从"狗叫还是警笛"到"这是什么语言"，都是音频分类。特征用 Mel，架构每个时代都在变（MFCC+kNN → CNN → Transformer），评估指标始终是 AUC、F1 和每类召回率。AST（Audio Spectrogram Transformer）和 BEATs 是当前 SOTA。

**类型：** 构建
**语言：** Python
**前置条件：** 阶段 6 · 02（频谱图与 Mel），阶段 3 · 06（CNN），阶段 5 · 08（文本的 CNN 与 RNN）
**时长：** 约 75 分钟

## 问题引入

你拿到一段 10 秒的音频片段。你想知道："它是什么？"城市声音（警笛、电钻、狗叫）、语音指令（是/否/停止）、语言识别（英语/西班牙语/阿拉伯语）、说话人情感（愤怒/中性）或环境声音（室内/室外、嘈杂人声）。这些都是*音频分类*，2026 年的基线架构已经成熟：对数 Mel -> CNN 或 Transformer -> softmax。

> **【中文解读】** 本节提出的问题是：如何在实际工程中正确理解和应用这一技术。理解问题背景有助于把握技术选型的关键决策点。在实际 AI 系统中，错误的技术选型往往比实现细节的 bug 代价更高。

核心难点不在网络。而在数据。音频数据集有严重的类别不平衡、强烈的领域偏移（干净 vs 嘈杂）和标签噪声（谁定义了"城市嘈杂人声" vs "餐厅噪音"？）。问题的 80% 是数据整理、数据增强和评估，而不是把 CNN 换成 Transformer。

## 核心概念

> **【中文解读】** 本节介绍核心概念和理论基础。掌握这些概念是后续动手实现的前提，同时也是面试和工程实践中高频考察的知识点。

![音频分类阶梯：MFCCs 上的 k-NN 到 AST 到 BEATs](../assets/audio-classification.svg)

**MFCC 上的 k-NN（1990 年代的基线）。** 将每个片段的 MFCC 展平，计算与标记库的余弦相似度，返回前 K 个的多数投票。在干净的小数据集上（Speech Commands、ESC-50）出奇地强。不需要 GPU。

**对数 Mel 上的 2D CNN（2015-2019）。** 将 `(T, n_mels)` 对数 Mel 当作图像。应用 ResNet-18 或 VGG 风格网络。沿时间轴全局均值池化。各类别 softmax。在 2026 年大多数 Kaggle 比赛中仍是基线。

**音频频谱图 Transformer，AST（2021-2024）。** 将对数 Mel 切成 patch（例如 16x16），添加位置嵌入，送入 ViT。AudioSet 上监督学习的 SOTA（mAP 0.485）。

**BEATs 和 WavLM-base（2024-2026）。** 在数百万小时数据上自监督预训练。用监督学习所需数据的 1-10% 微调你的任务。2026 年这是非语音音频的默认起点。BEATs-iter3 在 AudioSet 上比 AST 高 1-2 mAP，同时只用 1/4 的计算量。

**Whisper 编码器作为冻结骨干（2024）。** 取 Whisper 的编码器，丢弃解码器，接一个线性分类器。在语言识别和简单事件分类上接近 SOTA，无需任何音频增强。这是"免费午餐"基线。

### 类别不平衡才是真正的挑战

ESC-50：50 个类别，每类 40 个片段——均衡，简单。UrbanSound8K：10 个类别，10:1 不平衡。AudioSet：632 个类别，100,000:1 的长尾分布。有效的技术：

- 训练时均衡采样（评估时不使用）。
- Mixup：线性插值两个片段（及其标签）作为增强。
- SpecAugment：遮蔽随机时间和频带。简单但关键。

### 评估

- 多类别互斥（Speech Commands）：top-1 准确率，top-5 准确率。
- 多类别多标签（AudioSet、UrbanSound 风格）：平均精度均值（mAP, mean Average Precision）。
- 严重不平衡：每类召回率 + 宏观 F1。

2026 年你应该知道的数字：

| 基准 | 基线 | 2026 SOTA | 来源 |
|------|------|-----------|------|
| ESC-50 | 82%（AST） | 97.0%（BEATs-iter3） | BEATs 论文（2024） |
| AudioSet mAP | 0.485（AST） | 0.548（BEATs-iter3） | HEAR 排行榜 2026 |
| Speech Commands v2 | 98%（CNN） | 99.0%（Audio-MAE） | HEAR v2 结果 |

> **【中文解读】** 本节通过代码从零实现核心算法。这种 "from scratch" 的方式能帮助理解框架背后的原理，遇到问题时不会被黑盒困住。

> **【拓展：语音 AI 的产品化】** 语音技术在产品化中面临独特挑战：不同口音、背景噪声、远场拾音、多人说话等。Siri、Alexa、小爱同学等产品都投入了大量工程优化来解决这些 "长尾问题"。实时性要求（<300ms 延迟）也是语音产品的核心指标。

> **【拓展：多语言语音技术】** 全球语言的语音特性差异巨大：声调语言（如中文）的音高携带语义，低资源语言缺乏训练数据。Meta 的 MMS 模型支持 1000+ 种语言的语音识别，Whisper 在多语言场景表现出色，但仍需针对特定语言微调。

> **【拓展：语音隐私与安全】** 语音数据包含大量个人隐私信息（声纹、对话内容）。深度伪造（Deepfake）语音技术可以被滥用于诈骗。音频水印（Audio Watermarking）和声纹反欺诈（Anti-spoofing）是当前的研究热点。

## 动手实现

### 步骤 1：特征化

```python
def featurize_mfcc(signal, sr, n_mfcc=13, n_mels=40, frame_len=400, hop=160):
    mag = stft_magnitude(signal, frame_len, hop)
    fb = mel_filterbank(n_mels, frame_len, sr)
    mels = apply_filterbank(mag, fb)
    log = log_transform(mels)
    return [dct_ii(frame, n_mfcc) for frame in log]
```

### 步骤 2：固定长度摘要

```python
def summarize(mfcc_frames):
    n = len(mfcc_frames[0])
    mean = [sum(f[i] for f in mfcc_frames) / len(mfcc_frames) for i in range(n)]
    var = [
        sum((f[i] - mean[i]) ** 2 for f in mfcc_frames) / len(mfcc_frames) for i in range(n)
    ]
    return mean + var
```

简单但有效：沿时间的均值 + 方差给出 13 系数 MFCC 的 26 维固定嵌入。即刻运行。直到 2017 年仍在 ESC-50 上击败最先进的神经网络基线。

### 步骤 3：k-NN

```python
def cosine(a, b):
    dot = sum(x * y for x, y in zip(a, b))
    na = math.sqrt(sum(x * x for x in a)) or 1e-12
    nb = math.sqrt(sum(x * x for x in b)) or 1e-12
    return dot / (na * nb)

def knn_classify(q, bank, labels, k=5):
    sims = sorted(range(len(bank)), key=lambda i: -cosine(q, bank[i]))[:k]
    votes = Counter(labels[i] for i in sims)
    return votes.most_common(1)[0][0]
```

### 步骤 4：升级到对数 Mel 上的 CNN

用 PyTorch：

```python
import torch.nn as nn

class AudioCNN(nn.Module):
    def __init__(self, n_mels=80, n_classes=50):
        super().__init__()
        self.body = nn.Sequential(
            nn.Conv2d(1, 32, 3, padding=1), nn.ReLU(), nn.MaxPool2d(2),
            nn.Conv2d(32, 64, 3, padding=1), nn.ReLU(), nn.MaxPool2d(2),
            nn.Conv2d(64, 128, 3, padding=1), nn.ReLU(),
            nn.AdaptiveAvgPool2d(1),
        )
        self.head = nn.Linear(128, n_classes)

    def forward(self, x):  # x: (B, 1, T, n_mels)
        return self.head(self.body(x).flatten(1))
```

3M 参数。在 ESC-50 上单张 RTX 4090 约 10 分钟训练完成。80%+ 准确率。

### 步骤 5：2026 年的默认选择 — 微调 BEATs

```python
from transformers import ASTFeatureExtractor, ASTForAudioClassification

ext = ASTFeatureExtractor.from_pretrained("MIT/ast-finetuned-audioset-10-10-0.4593")
model = ASTForAudioClassification.from_pretrained(
    "MIT/ast-finetuned-audioset-10-10-0.4593",
    num_labels=50,
    ignore_mismatched_sizes=True,
)

> **【中文解读】** 本节展示如何用成熟框架（如 PyTorch、HuggingFace 等）快速应用该技术。在实际项目中，优先使用经过验证的框架实现，可以减少 bug 并提高开发效率。


inputs = ext(audio, sampling_rate=16000, return_tensors="pt")
logits = model(**inputs).logits
```

对于 BEATs，通过 `beats` 库使用 `microsoft/BEATs-base`；transformers API 的形式相同。

> **【拓展：语音与情感计算】** 语音不仅传递文字信息，还携带丰富的情感信号（语调、语速、音高变化）。情感语音识别（Speech Emotion Recognition, SER）在客服质检、心理健康监测、智能教育等领域有广泛应用。当前 SOTA 模型通常基于 wav2vec 2.0 或 HuBERT 等预训练模型微调。

## 用框架实现

2026 年的技术栈：

| 场景 | 起步选择 |
|------|----------|
| 微型数据集（<1000 片段） | MFCC 均值上的 k-NN（你的基线）+ 音频增强 |
| 中等数据集（1K-100K） | BEATs 或 AST 微调 |
| 大型数据集（>100K） | 从头训练或微调 Whisper 编码器 |
| 实时、边缘 | 40-MFCC CNN，量化到 int8（关键词检测风格） |
| 多标签（AudioSet） | BEATs-iter3 + BCE 损失 + mixup + SpecAugment |
| 语言识别 | MMS-LID，SpeechBrain VoxLingua107 基线 |

> **【中文解读】** 本节关注如何将模型部署为可用的产品。从原型到生产级系统需要考虑性能优化、错误处理、监控等多个维度。

决策规则：**从冻结骨干开始，不要从新模型开始。** 微调 BEATs 的分类头可以在几小时内达到 SOTA 的 95%，而不是几周。

## 产出物

保存为 `outputs/skill-classifier-designer.md`。为给定的音频分类任务选择架构、增强策略、类别平衡策略和评估指标。

## 练习题

1. **简单。** 运行 `code/main.py`。它在 4 类合成数据集（不同音高的纯音）上训练 k-NN MFCC 基线。报告混淆矩阵。
2. **中等。** 将 `summarize` 替换为 [均值, 方差, 偏度, 峰度]。4 阶矩池化是否在相同合成数据集上优于均值+方差？
3. **困难。** 使用 `torchaudio` 在 ESC-50 fold 1 上训练 2D CNN。报告 5 折交叉验证准确率。添加 SpecAugment（时间遮蔽 = 20，频率遮蔽 = 10）并报告差值。

> **【中文解读】** 术语表中的 "What people say" vs "What it actually means" 区分了日常口语和精确技术含义。在团队协作中，统一术语定义可以避免大量沟通误解。

## 术语速查表

| 术语 | 通俗说法 | 实际含义 |
|------|----------|----------|
| AudioSet | 音频界的 ImageNet | Google 的 200 万片段、632 类弱标记 YouTube 数据集。 |
| ESC-50 | 小型分类基准 | 50 类 × 40 片段的环境声音。 |
| AST | 音频频谱图 Transformer | 在对数 Mel patch 上的 ViT；2021 SOTA。 |
| BEATs | 自监督音频 | 微软模型，iter3 截至 2026 年领先 AudioSet。 |
| Mixup | 配对增强 | `x = lambda*x1 + (1-lambda)*x2; y = lambda*y1 + (1-lambda)*y2`。 |
| SpecAugment | 遮蔽增强 | 将频谱图的随机时间和频带置零。 |
| mAP | 主要多标签指标 | 跨类别和阈值的平均精度均值。 |

> **【中文解读】** 延伸阅读提供了深入学习的高质量资源。这些论文和教程是该领域的经典参考文献，适合需要深入理解的读者。

## 延伸阅读

- [Gong, Chung, Glass (2021). AST: Audio Spectrogram Transformer](https://arxiv.org/abs/2104.01778) —— 2021-2024 年的记录架构。
- [Chen et al. (2022, rev. 2024). BEATs: Audio Pre-Training with Acoustic Tokenizers](https://arxiv.org/abs/2212.09058) —— 2024+ 的默认选择。
- [Park et al. (2019). SpecAugment](https://arxiv.org/abs/1904.08779) —— 主导的音频增强方法。
- [Piczak (2015). ESC-50 数据集](https://github.com/karolpiczak/ESC-50) —— 经久不衰的 50 类基准。
- [Gemmeke et al. (2017). AudioSet](https://research.google.com/audioset/) —— 632 类 YouTube 分类体系；仍是黄金标准。

> **【中文解读】** 延伸阅读提供了深入学习的高质量资源，包括论文、教程和工具。建议按需选读，优先阅读标注为 "the critical read" 的核心论文。
