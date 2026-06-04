# 频谱图、Mel 尺度与音频特征

> 神经网络处理原始波形效果不好，处理频谱图效果好，处理 Mel 频谱图效果更好。2026 年所有 ASR（语音识别）、TTS（语音合成）和音频分类器的成败取决于这一个预处理选择。Mel 尺度模拟人耳对频率的感知（低频精细、高频粗略）。

> **【中文解读】** 神经网络处理原始波形效果不好，但处理频谱图效果好，处理 Mel 频谱图效果更好。2026 年所有 ASR、TTS 和音频分类器的成败取决于这一个预处理选择。Mel 尺度模拟人耳对频率的感知（低频精细、高频粗略）。

> **【拓展：Mel 频谱图是音频 AI 的 "图像"】** Mel 频谱图将音频转换为 2D 图像（时间×频率），可以用 CNN/ViT 处理。Whisper、MusicGen、Stable Audio 都使用 Mel 频谱图作为中间表示。

**类型：** 构建
**语言：** Python
**前置条件：** 阶段 6 · 01（音频基础）
**时长：** 约 45 分钟

## 问题引入

取一段 10 秒的 16 kHz 音频片段。那是 160,000 个浮点数，全部在 `[-1, 1]` 范围内，与标签"狗叫"或"单词 cat"几乎完全不相关。原始波形包含信息，但形式是模型难以提取的。100 毫秒间隔发出的两个相同音素（phoneme）在原始采样点中完全不同。

> **【中文解读】** 本节提出的问题是：如何在实际工程中正确理解和应用这一技术。理解问题背景有助于把握技术选型的关键决策点。在实际 AI 系统中，错误的技术选型往往比实现细节的 bug 代价更高。

频谱图解决了这个问题。它压缩了人类感知忽略的时间细节（微秒级抖动），保留了感知关注的结构（哪些频率有能量，以约 10-25 ms 的时间窗为单位）。

Mel 频谱图走得更远。人类对音高的感知是对数的：100 Hz vs 200 Hz 听起来"距离相同"，就像 1000 Hz vs 2000 Hz 一样。Mel 尺度（Mel scale）将频率轴扭曲以匹配这种感知。Mel 尺度的频谱图是 2010 年到 2026 年语音机器学习中最重要的单一特征。

## 核心概念

> **【中文解读】** 本节介绍核心概念和理论基础。掌握这些概念是后续动手实现的前提，同时也是面试和工程实践中高频考察的知识点。

![从波形到 STFT 到 Mel 频谱图到 MFCC 的阶梯](../assets/mel-features.svg)

**STFT（短时傅里叶变换）。** 将波形切成重叠的帧（典型：25 ms 窗口，10 ms 步移 = 16 kHz 下 400 采样点 / 160 采样点）。每帧乘以窗函数（Hann 是默认选择；Hamming 略有不同）。对每帧做 FFT。将幅度谱堆叠成 `(n_frames, n_freq_bins)` 形状的矩阵。这就是频谱图。

**对数幅度（Log-magnitude）。** 原始幅度跨越 5-6 个数量级。取 `log(|X| + 1e-6)` 或 `20 * log10(|X|)` 来压缩动态范围。每个生产流水线都使用对数幅度，而非原始幅度。

**Mel 尺度。** 频率 `f`（Hz）映射到 Mel 值 `m`：`m = 2595 * log10(1 + f / 700)`。该映射在 1 kHz 以下大致线性，在 1 kHz 以上大致对数。80 个 Mel bin 覆盖 0-8 kHz 是标准 ASR 输入。

**Mel 滤波器组（Mel filterbank）。** 一组在 Mel 尺度上等距排列的三角形滤波器。每个滤波器是相邻 FFT bin 的加权和。将 STFT 幅度乘以滤波器组矩阵，一次矩阵乘法即可得到 Mel 频谱图。

**对数 Mel 频谱图（Log-mel spectrogram）。** `log(mel_spec + 1e-10)`。Whisper 的输入。Parakeet 的输入。SeamlessM4T 的输入。2026 年的通用音频前端。

**MFCC（梅尔频率倒谱系数）。** 对对数 Mel 频谱图做 DCT（类型 II），保留前 13 个系数。去除特征间相关性并进一步压缩。在大约 2015 年 CNN/Transformer 直接处理对数 Mel 之前是主流特征。仍在说话人识别（x-vector、ECAPA）中使用。

**分辨率权衡。** FFT 越大 = 频率分辨率越好但时间分辨率越差。25 ms / 10 ms 是音频 ML 的默认值；音乐用 50 ms / 12.5 ms；瞬态检测（鼓点、爆破音）用 5 ms / 2 ms。

> **【拓展：语音 AI 的产品化】** 语音技术在产品化中面临独特挑战：不同口音、背景噪声、远场拾音、多人说话等。Siri、Alexa、小爱同学等产品都投入了大量工程优化来解决这些 "长尾问题"。实时性要求（<300ms 延迟）也是语音产品的核心指标。

> **【拓展：多语言语音技术】** 全球语言的语音特性差异巨大：声调语言（如中文）的音高携带语义，低资源语言缺乏训练数据。Meta 的 MMS 模型支持 1000+ 种语言的语音识别，Whisper 在多语言场景表现出色，但仍需针对特定语言微调。

## 动手实现

> **【中文解读】** 本节通过代码从零实现核心算法。这种 "from scratch" 的方式能帮助理解框架背后的原理，遇到问题时不会被黑盒困住。

### 步骤 1：对波形分帧

```python
def frame(signal, frame_len, hop):
    n = 1 + (len(signal) - frame_len) // hop
    return [signal[i * hop : i * hop + frame_len] for i in range(n)]
```

一段 10 秒的 16 kHz 音频，`frame_len=400, hop=160`，产生 998 帧。

### 步骤 2：Hann 窗

```python
import math

def hann(N):
    return [0.5 * (1 - math.cos(2 * math.pi * n / (N - 1))) for n in range(N)]
```

FFT 前逐元素相乘。消除因非零端点截断导致的频谱泄漏。

### 步骤 3：STFT 幅度

```python
def stft_magnitude(signal, frame_len=400, hop=160):
    win = hann(frame_len)
    frames = frame(signal, frame_len, hop)
    return [magnitudes(dft([w * s for w, s in zip(win, f)])) for f in frames]
```

生产环境使用 `torch.stft` 或 `librosa.stft`（基于 FFT，向量化）。这里的循环是教学用途；在 `code/main.py` 中处理短音频片段。

### 步骤 4：Mel 滤波器组

```python
def hz_to_mel(f):
    return 2595.0 * math.log10(1.0 + f / 700.0)

def mel_to_hz(m):
    return 700.0 * (10 ** (m / 2595.0) - 1)

def mel_filterbank(n_mels, n_fft, sr, fmin=0, fmax=None):
    fmax = fmax or sr / 2
    mels = [hz_to_mel(fmin) + (hz_to_mel(fmax) - hz_to_mel(fmin)) * i / (n_mels + 1)
            for i in range(n_mels + 2)]
    hzs = [mel_to_hz(m) for m in mels]
    bins = [int(h * n_fft / sr) for h in hzs]
    fb = [[0.0] * (n_fft // 2 + 1) for _ in range(n_mels)]
    for m in range(n_mels):
        for k in range(bins[m], bins[m + 1]):
            fb[m][k] = (k - bins[m]) / max(1, bins[m + 1] - bins[m])
        for k in range(bins[m + 1], bins[m + 2]):
            fb[m][k] = (bins[m + 2] - k) / max(1, bins[m + 2] - bins[m + 1])
    return fb
```

80 个 Mel bin 覆盖 0-8 kHz，`n_fft=400`，得到 `(80, 201)` 矩阵。将 `(n_frames, 201)` STFT 幅度乘以其转置得到 `(n_frames, 80)` Mel 频谱图。

### 步骤 5：对数 Mel

```python
def log_mel(mel_spec, eps=1e-10):
    return [[math.log(max(v, eps)) for v in frame] for frame in mel_spec]
```

常见替代方案：`librosa.power_to_db`（参考归一化 dB），`10 * log10(power + eps)`。Whisper 使用更复杂的裁剪 + 归一化流程（参见 Whisper 的 `log_mel_spectrogram`）。

### 步骤 6：MFCC

```python
def dct_ii(x, n_coeffs):
    N = len(x)
    return [
        sum(x[n] * math.cos(math.pi * k * (2 * n + 1) / (2 * N)) for n in range(N))
        for k in range(n_coeffs)
    ]
```

> **【中文解读】** 本节展示如何用成熟框架（如 PyTorch、HuggingFace 等）快速应用该技术。在实际项目中，优先使用经过验证的框架实现，可以减少 bug 并提高开发效率。

对每帧对数 Mel 应用 DCT，保留前 13 个系数。这就是 MFCC 矩阵。第一个系数通常被丢弃（它编码整体能量）。

> **【拓展：语音与情感计算】** 语音不仅传递文字信息，还携带丰富的情感信号（语调、语速、音高变化）。情感语音识别（Speech Emotion Recognition, SER）在客服质检、心理健康监测、智能教育等领域有广泛应用。当前 SOTA 模型通常基于 wav2vec 2.0 或 HuBERT 等预训练模型微调。

## 用框架实现

2026 年的技术栈：

| 任务 | 特征配置 |
|------|----------|
| ASR（Whisper、Parakeet、SeamlessM4T） | 80 对数 Mel，10 ms 步移，25 ms 窗口 |
| TTS 声学模型（VITS、F5-TTS、Kokoro） | 80 Mel，5-12 ms 步移以实现精细时间控制 |
| 音频分类（AST、PANNs、BEATs） | 128 对数 Mel，10 ms 步移 |
| 说话人嵌入（ECAPA-TDNN、WavLM） | 80 对数 Mel 或原始波形 SSL |
| 音乐（MusicGen、Stable Audio 2） | EnCodec 离散 token（非 Mel） |
| 关键词检测（Keyword Spotting） | 40 MFCC 用于小型设备 |

经验法则：**如果你不在做音乐，从 80 对数 Mel 开始。** 任何偏离都需要充分理由。

## 2026 年仍在出现的陷阱

- **Mel 数量不匹配。** 训练用 80 Mel，推理用 128 Mel。静默失败。在两端都记录特征形状。
- **上游采样率不匹配。** 22.05 kHz 计算的 Mel 与 16 kHz 看起来不同。在特征化*之前*修复采样率。
- **dB vs 对数。** Whisper 期望对数 Mel，不是 dB-Mel。一些 HF 流水线会自动检测；你的自定义代码不会。
- **归一化漂移。** 训练时逐话语归一化，推理时全局归一化。这种生产 bug 会使 WER 翻倍。
- **填充泄漏。** 音频末尾零填充会在尾部帧产生平坦频谱。对称填充或复制填充。

> **【中文解读】** 本节关注如何将模型部署为可用的产品。从原型到生产级系统需要考虑性能优化、错误处理、监控等多个维度。

## 产出物

保存为 `outputs/skill-feature-extractor.md`。该技能为给定模型目标选择特征类型、Mel 数量、帧长/步移和归一化方式。

## 练习题

1. **简单。** 运行 `code/main.py`。它合成一个扫频信号（chirp，频率从 200 扫到 4000 Hz）并打印每帧的 argmax Mel bin。绘制（可选）并确认与扫频匹配。
2. **中等。** 用 `n_mels` 在 `{40, 80, 128}` 和 `frame_len` 在 `{200, 400, 800}` 中重新运行。测量时间轴上的锐峰带宽。哪种组合对扫频的分辨最好？
3. **困难。** 实现 `power_to_db`，在 AudioMNIST 上用 (a) 原始对数 Mel、(b) `ref=max` 的 dB-Mel、(c) MFCC-13 + delta + delta-delta 比较一个小型 CNN 分类器的 ASR 准确率。报告 top-1 准确率。

> **【中文解读】** 术语表中的 "What people say" vs "What it actually means" 区分了日常口语和精确技术含义。在团队协作中，统一术语定义可以避免大量沟通误解。

## 术语速查表

| 术语 | 通俗说法 | 实际含义 |
|------|----------|----------|
| 帧（Frame） | 一个切片 | 25 ms 的波形块，送入一次 FFT。 |
| 步移（Hop） | 步幅 | 连续帧之间的采样点数；10 ms 是 ASR 默认值。 |
| 窗函数（Window） | Hann/Hamming 那个东西 | 逐点乘法器，将帧边缘渐变到零。 |
| STFT | 频谱图生成器 | 分帧 + 加窗的 FFT；产生时间 × 频率矩阵。 |
| Mel | 扭曲的频率 | 对数感知尺度；`m = 2595*log10(1 + f/700)`。 |
| 滤波器组（Filterbank） | 那个矩阵 | 将 STFT 投影到 Mel bin 的三角形滤波器。 |
| 对数 Mel（Log-mel） | Whisper 的输入 | `log(mel_spec + eps)`；2026 年的标准化表示。 |
| MFCC | 老派特征 | 对数 Mel 的 DCT；13 个系数，去相关。 |

> **【中文解读】** 延伸阅读提供了深入学习的高质量资源。这些论文和教程是该领域的经典参考文献，适合需要深入理解的读者。

## 延伸阅读

- [Davis, Mermelstein (1980). Comparison of parametric representations for monosyllabic word recognition](https://ieeexplore.ieee.org/document/1163420) —— MFCC 论文。
- [Stevens, Volkmann, Newman (1937). A Scale for the Measurement of the Psychological Magnitude Pitch](https://pubs.aip.org/asa/jasa/article-abstract/8/3/185/735757/) —— 原始 Mel 尺度论文。
- [OpenAI — Whisper 源码, log_mel_spectrogram](https://github.com/openai/whisper/blob/main/whisper/audio.py) —— 阅读参考实现。
- [librosa 特征提取文档](https://librosa.org/doc/main/feature.html) —— `mfcc`、`melspectrogram` 和 hop/window 的参考。
- [NVIDIA NeMo — 音频预处理](https://docs.nvidia.com/deeplearning/nemo/user-guide/docs/en/main/asr/asr_all.html#featurizers) —— Parakeet + Canary 模型的生产级流水线。

> **【中文解读】** 延伸阅读提供了深入学习的高质量资源，包括论文、教程和工具。建议按需选读，优先阅读标注为 "the critical read" 的核心论文。
