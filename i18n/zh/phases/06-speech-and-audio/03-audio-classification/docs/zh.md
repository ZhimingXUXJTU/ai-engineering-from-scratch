# 音频分类  从MFCC+KNN到AST和BEAT

> 无论是"狗吠声与声"还是"这是什么语言",都在进行音频分类. 功能都是化. 架构每十年都在移动. 评估仍然是AUC,F1和每类回忆.

> **【中文解读】**从"狗叫还是警笛"到"这是什么语言",都是音频分类.

**Type:** Build | **类型:** 构建
**Languages:** Python | **语言:** Python
**Prerequisites:** Phase 6 · 02 (Spectrograms & Mel), Phase 3 · 06 (CNNs), Phase 5 · 08 (CNNs & RNNs for Text) | **前置知识:** 阶段 6 · 02（频谱图与 Mel），阶段 3 · 06（CNN），阶段 5 · 08（文本的 CNN 与 RNN）
**Time:** ~75 minutes | **预计用时:** ~75 分钟

## 问题 问题引入

你得到一个10秒钟的剪辑.你想知道:"这是什么?"城市声音 (声,钻机,狗),语音命令 (是的/不/停止),语言识别 (en/es/ar),扬声器情绪 (愤怒/中性),或环境声音 (室内/室外,声).所有这些都是 *音频分类*,并在2026年基础架构成熟:log-mel → CNN或变压器 →软max.

> 你得到一段10秒音频. 你想知道:"这是什么?"城市声音:警笛,钻机,狗叫) 语音命令:

> **【中文解读】**本节提出的问题是:如何在实际工程中正确理解和应用这一技术――理解问题背景有助于把握技术选择的关键决策点――在实际人工智能系统中,错误的技术选择往往比实现细节的错误成本更高――

音频数据集具有残酷的类失衡,强大的域名转移 (清洁与噪音),以及标签噪音 (谁决定"城市语"与"餐厅噪音"?).80%的问题是策展,增强和评估,而不是将CNN换为变压器.

> 核心难点不在网络,而在数据中──音频数据集有严重的类别不平衡,强领域偏移──干净与杂杂) 和标签噪音──谁定义了"城市杂杂"与餐厅噪音?

## 概念的核心概念

> **【中文解读】**本节介绍核心概念和理论基础.掌握这些概念是后续动手实现的前提,同时也是面试和工程实践中高频考察的知识点.


![Audio classification ladder: k-NN on MFCCs to AST to BEATs](../assets/audio-classification.svg)

**k-NN on MFCCs (the 1990s baseline).**按片段平坦的MFCC,计算与标记的银行相似的共数,返回顶部K的多数投票.在清洁的小数据集 (语音命令,ESC-50) 上,令人惊的强度.

> **MFCC 上的 k-NN（1990 年代基线）。**计算与标记库的余弦相似度,返回前K个的多数投票.

**2D CNN on log-mels (2015-2019).**治疗`(T, n_mels)`通过RESNET-18或VGG方式,全球平均时间轴积分,课程上的软度,仍然是2026年大多数高格赛的基线.

> **log-mel 上的 2D CNN（2015-2019）。**将`(T, n_mels)`通过ResNet-18或VGG风格进行全局平均值池化. 在时间轴上进行全局平均值池化. 对类别进行软最大的处理. 在2026年大多数卡格尔比赛中仍然是基线.

**Audio Spectrogram Transformer, AST (2021-2024).**贴合日志邮件 (例如16×16补丁),添加位置嵌入,输入VIT. 视频组的最新状态 (mAP 0.485) 进行监督学习.

> **音频频谱图 Transformer，AST（2021-2024）。**将 log-mail 分块(如16×16块),添加位置嵌入,送入 ViT──AudioSet 上监督学习的SOTA(mAP 0.485)──

**BEATs and WavLM-base (2024-2026).**通过使用1-10%的监督数据,你需要完成任务.在2026年,这是非语音音的默认起点. BEATs-iter3在AudioSet上击败AST1-2mAP,同时使用1/4的计算.

> **BEATs 和 WavLM-base（2024-2026）。**在数百万小时的数据上自监督预训练. 您本来需要的监督数据的1-10%就能微调. 2026年这是非语音频的默认起点.

**Whisper-encoder as a frozen backbone (2024).**接下来,我们将Whisper的编码器放下,将解码器放下,将线性分类器附加到.

> **Whisper 编码器作为冻结骨干（2024）。**取 Whisper 的编码器,丢弃解码器,接一个线性分类器.

### 阶级失衡是真正的挑战

> ### 类别不平衡才是真正的挑战

标签: 标签: 标签: 标签: 标签: 标签: 标签: 标签: 标签: 标签: 标签: 标签: 标签: 标签: 标签: 标签: 标签: 标签: 标签: 标签: 标签: 标签: 标签: 标签: 标签: 标签: 标签: 标签: 标签: 标签: 标签: 标签: 标签: 标签: 标签: 标签: 标签: 标签: 标签: 标签: 标签: 标签: 标签: 标签: 标签: 标签: 标签: 标签: 标签: 标签: 标签: 标签: 标签: 标签: 标签: 标签: 标签: 标签: 标签: 标签: 标签: 标签: 标签: 标签: 标签: 标签: 标签: 标签: 标签: 标签: 标签: 标签: 标签: 标签: 标签: 标签: 标签: 标签: 标签: 标签: 标签: 标签: 标签

> 标签: 标签: 标签: 标签: 标签: 标签: 标签: 标签: 标签: 标签: 标签: 标签: 标签: 标签: 标签: 标签: 标签: 标签: 标签: 标签: 标签: 标签: 标签: 标签: 标签: 标签: 标签: 标签: 标签: 标签: 标签: 标签: 标签: 标签: 标签: 标签: 标签: 标签: 标签: 标签: 标签: 标签: 标签: 标签: 标签: 标签: 标签: 标签: 标签: 标签: 标签: 标签: 标签: 标签: 标签: 标签: 标签: 标签: 标签: 标签: 标签: 标签: 标签: 标签: 标签: 标签: 标签: 标签: 标签: 标签: 标签: 标签: 标签: 标签: 标签: 标签: 标签: 标签: 标签: 标签: 标签: 标签

- 在培训期间 (不在评估中) 进行均衡的采样.
  训练时平衡采样(评估时不用)
- 混合:将两个剪辑 (及其标签) 线性插入为增强.
  混合:线性插值两段音频 (和标签) 作为增强.
- 简单,关键. 现在,我们需要一个新的技术.
  频率带带.简单但关键.

### 评估

> ### 评估

- 多级独家 (语音命令):最高1-准确,最高5-准确.
  语音命令:上-1 准确率、上-5 准确率──
- 多级多级标签 (AudioSet, UrbanSound-style):平均精度 (mAP).
  类型: 平均精度平均值: 平均精度平均精度
- 严重失衡:每类召回+宏F1.
  严重不平衡:每类召回率 + 宏观F1──

2026号码你应该知道:

> 2026年你应该知道的数字:

| Benchmark | Baseline | SOTA 2026 | Source |
|-----------|----------|-----------|--------|
| ESC-50 | 82% (AST) | 97.0% (BEATs-iter3) | BEATs paper (2024) |
| AudioSet mAP | 0.485 (AST) | 0.548 (BEATs-iter3) | HEAR leaderboard 2026 |
| Speech Commands v2 | 98% (CNN) | 99.0% (Audio-MAE) | HEAR v2 results |

| 基准测试 | 基线 | 2026 SOTA | 来源 |
|----------|------|-----------|------|
| ESC-50 | 82%（AST） | 97.0%（BEATs-iter3） | BEATs 论文（2024） |
| AudioSet mAP | 0.485（AST） | 0.548（BEATs-iter3） | HEAR 排行榜 2026 |
| Speech Commands v2 | 98%（CNN） | 99.0%（Audio-MAE） | HEAR v2 结果 |

> **【中文解读】**本节通过代码实现从零到核心算法――这种"从零开始"的方式可以帮助理解框架背后的原理,遇到问题时不会被黑盒困住――

> **【拓展：语音 AI 的产品化】**语音技术在产品化中面临着独特的挑战:不同口音,背景噪音,远场拾音,多人说话等.

> **【拓展：多语言语音技术】**全球语言的语音特性差异巨大:声调语言的音高携带语义,低资源语言缺乏训练数据――Meta的MMS模型支持1000多种语言的语音识别,语在多语言场景表现出色,但仍然需要针对特定语言微调――

> **【拓展：语音隐私与安全】**语音数据包含大量个人隐私信息 (声纹、对话内容) ◦深度伪造 (Deepfake) 语音技术可被滥用作弊 (欺诈) 音频水印 (音频水印) ◎音纹反欺诈 (反欺诈) ◎反欺诈 (反欺诈) ◎是当前的研究热点.





## 建立它,实现它.
```figure
mfcc-pipeline
```

## 建立它

### 步骤1: 化

```python
def featurize_mfcc(signal, sr, n_mfcc=13, n_mels=40, frame_len=400, hop=160):
    mag = stft_magnitude(signal, frame_len, hop)
    fb = mel_filterbank(n_mels, frame_len, sr)
    mels = apply_filterbank(mag, fb)
    log = log_transform(mels)
    return [dct_ii(frame, n_mfcc) for frame in log]
```

### 步骤2:固定长度的总结

```python
def summarize(mfcc_frames):
    n = len(mfcc_frames[0])
    mean = [sum(f[i] for f in mfcc_frames) / len(mfcc_frames) for i in range(n)]
    var = [
        sum((f[i] - mean[i]) ** 2 for f in mfcc_frames) / len(mfcc_frames) for i in range(n)
    ]
    return mean + var
```

简单但强大:平均+时间变异为13个 MFCC提供26维固定嵌入.即时运行.在ESC-50上击败了最新的NN基线.

> 简单但有效:时间轴上的平均值 + 方差为13系数MFCC 给出26维固定嵌入式――运行瞬间――在ESC-50上直到2017年仍能击败当时的SOTA神经网络基线――

### 步骤3: k-NN

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

### 步骤4:升级到CNN在日志

在PyTorch:

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

列车在ESC-50上用单个RTX 4090的10分钟. 80%+精度.

> 通过单张RTX 4090 训练约10分钟,准确率80%+.

### 步骤5:2026年默认的 细调 BEAT

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

对于 BEAT 则使用`microsoft/BEATs-base`通过`beats`转换器API的形状相同.

> 对于BAT,通过`beats`库使用 `microsoft/BEATs-base`变压器API的形式相同.




> **【拓展：语音与情感计算】**语音不仅传递文字信息,还携带丰富的情感信号 (语调、语速、音高变化) 情感语音识别 (语音识别,语音情感识别,SER) 在客服质检,心理健康监测,智能教育等领域广泛应用.

## 用它实现框架

现在,我们要做什么?

> 2026 年技术:

| Situation | Start with |
|-----------|-----------|
| Tiny dataset (<1000 clips) | k-NN on MFCC means (your baseline) + audio augmentation |
| Medium dataset (1K–100K) | BEATs or AST fine-tune |
| Large dataset (>100K) | Train from scratch or fine-tune Whisper-encoder |
| Real-time, edge | 40-MFCC CNN, quantized to int8 (KWS-style) |
| Multi-label (AudioSet) | BEATs-iter3 with BCE loss + mixup + SpecAugment |
| Language ID | MMS-LID, SpeechBrain VoxLingua107 baseline |

| 场景 | 起始方案 |
|------|----------|
| 小数据集（<1000 段） | MFCC 均值上的 k-NN（基线）+ 音频增强 |
| 中等数据集（1K–100K） | BEATs 或 AST 微调 |
| 大数据集（>100K） | 从零训练或微调 Whisper 编码器 |
| 实时、边缘设备 | 40-MFCC CNN，量化为 int8（关键词检测风格） |
| 多标签（AudioSet） | BEATs-iter3 + BCE 损失 + mixup + SpecAugment |
| 语言识别 | MMS-LID，SpeechBrain VoxLingua107 基线 |

> **【中文解读】**本节关注如何将模型部署为可用的产品. 从原型到生产级系统需要考虑性能优化,错误处理,监控等多个维度.


决策规则:**start with a frozen backbone, not a fresh model**精细调节BET头脑,会让你在几个小时内获得95%的SOTA,而不是几周.

> 决策规则:**从冻结骨干开始，而不是从头训练模型**微调 BEATs 分类头可以在几小时内达到 SOTA 的95%,而不是几周.



## 运送它.

保存如`outputs/skill-classifier-designer.md`选择一个特定的音频分类任务的架构,增强,类平衡策略和评估指标.

> 保存为`outputs/skill-classifier-designer.md`△为给定的频率分类任务选择结构,增强策略,类别平衡策略和评估标志.

## 练习题

1. **Easy.**跑步`code/main.py`根据4类合成数据集 (不同音调的纯色调) 训练k-NN MFCC基线. 报告混矩阵.
   **简单。**运行`code/main.py`△它在4类合成数据集中炼 k-NN MFCC 基线――报告混矩阵――
2. **Medium.**取代`summarize`它们的数据集中的4分钟聚合率比同一个合成数据集的 mean+var 值更高吗?
   **中等。**将`summarize`替换为 [平均值,var, skew,kurtosis]──四矩池化是否在同一合成数据集上优于平均值+方差?
3. **Hard.**使用`torchaudio`报告交叉验证准确度为5倍. 添加规格增量 (时间面具=20,频率面具=10) 并报告三角形.
   **困难。**使用 `torchaudio`报告 5 折交叉验证准确率──添加规格 时间掩码 = 20,频率掩码 = 10)并报告差值──

> **【中文解读】**在团队协作中,统一术语定义可以避免大量沟通误解.


## 关键词 快速查找表

| Term | What people say | What it actually means |
|------|-----------------|-----------------------|
| AudioSet | The ImageNet of audio | Google's 2M-clip, 632-class weakly-labeled YouTube dataset. |
| ESC-50 | Small classification benchmark | 50 classes × 40 clips of environmental sounds. |
| AST | Audio Spectrogram Transformer | ViT on log-mel patches; 2021 SOTA. |
| BEATs | Self-supervised audio | Microsoft model, iter3 leads AudioSet as of 2026. |
| Mixup | Pair augmentation | `x = λ·x1 + (1-λ)·x2; y = λ·y1 + (1-λ)·y2`. |
| SpecAugment | Mask-based augmentation | Zero-out random time and frequency bands of the spectrogram. |
| mAP | Main multi-label metric | Mean average precision across classes and thresholds. |

| 术语 | 人们常说的 | 实际含义 |
|------|-----------|---------|
| AudioSet | 音频界的 ImageNet | Google 的 200 万片段、632 类弱标注 YouTube 数据集。 |
| ESC-50 | 小型分类基准 | 50 类 × 40 个环境声音片段。 |
| AST | 音频频谱图 Transformer | log-mel 块上的 ViT；2021 SOTA。 |
| BEATs | 自监督音频 | 微软模型，iter3 截至 2026 年领先 AudioSet。 |
| Mixup | 配对增强 | `x = λ·x1 + (1-λ)·x2; y = λ·y1 + (1-λ)·y2`。 |
| SpecAugment | 掩码增强 | 将频谱图的随机时间和频率带置零。 |
| mAP | 主要多标签指标 | 各类别和阈值的平均精度均值。 |

> **【中文解读】**延伸阅读提供了深入学习的高质量资源. 这些论文和教程是该领域的经典参考文献,适合需要深入了解的读者.


## 继续阅读 继续阅读

- [Gong, Chung, Glass (2021). AST: Audio Spectrogram Transformer](https://arxiv.org/abs/2104.01778)从2021年到2024年记录的建筑.
  东,,玻璃 (2021). 东:音频频谱图 变压器2021-2024年记录架构──
- [Chen et al. (2022, rev. 2024). BEATs: Audio Pre-Training with Acoustic Tokenizers](https://arxiv.org/abs/2212.09058)2024+默认
  陈等 (2022,修订 2024). BEATs:声学代币器的音频预训2024+ 的默认选择──
- [Park et al. (2019). SpecAugment](https://arxiv.org/abs/1904.08779)主导的音频增强.
   Park 等 (2019). 标签 增强方式
- [Piczak (2015). ESC-50 dataset](https://github.com/karolpiczak/ESC-50)50级的基准,活着.
  皮卡克 (2015). 欧洲央行50数据集持续使用的50类基准.
- [Gemmeke et al. (2017). AudioSet](https://research.google.com/audioset/) 632 级YouTube类别;仍然是黄金标准.
  据悉,在中国,米克等 (2017).

> **【中文解读】**延伸阅读提供了深入学习的高质量资源,包括论文,教程和工具.

