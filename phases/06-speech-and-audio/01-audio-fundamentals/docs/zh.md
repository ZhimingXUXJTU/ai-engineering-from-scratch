# 音频基础 — 波形、采样与傅里叶变换

> 波形是原始信号，频谱图是表示形式，Mel 特征是机器学习友好的形式。每个现代语音识别（ASR, Automatic Speech Recognition）和语音合成（TTS, Text-to-Speech）系统都沿这个阶梯向上：波形 -> 频谱图 -> Mel 特征。第一阶就是理解采样和傅里叶变换。

> **【中文解读】** 波形是原始信号，频谱图是表示形式，Mel 特征是机器学习友好的形式。每个现代语音识别（ASR）和语音合成（TTS）系统都沿这个阶梯向上：波形 → 频谱图 → Mel 特征。第一阶就是理解采样和傅里叶变换。

> **【拓展：音频 AI 的基础】** 采样率（如 16kHz）决定了可表示的最高频率（奈奎斯特定理）。傅里叶变换将时域信号分解为频域成分。这些概念是 Whisper、TTS、语音克隆等所有音频 AI 的基础。

**类型：** 学习
**语言：** Python
**前置条件：** 阶段 1 · 06（向量与矩阵），阶段 1 · 14（概率分布）
**时长：** 约 45 分钟

## 问题引入

麦克风产生的是压力-时间信号。你的神经网络消费的是张量（tensor）。它们之间是一套约定栈——一旦违反，就会产生隐蔽的 bug：模型训练得很好但词错率（WER）翻倍，TTS 带有嘶嘶声，或者语音克隆系统记住了麦克风而不是说话人。

> **【中文解读】** 本节提出的问题是：如何在实际工程中正确理解和应用这一技术。理解问题背景有助于把握技术选型的关键决策点。在实际 AI 系统中，错误的技术选型往往比实现细节的 bug 代价更高。

语音系统中的每一个 bug 都可以追溯到以下三个问题之一：

1. 数据是以什么采样率录制的，模型期望什么采样率？
2. 信号是否存在混叠（aliasing）？
3. 你操作的是原始采样点还是频率表示？

这三个问题搞对了，第六阶段的其余内容就迎刃而解。搞错了，即使是 Whisper-Large-v4 也会产生垃圾输出。

## 核心概念

> **【中文解读】** 本节介绍核心概念和理论基础。掌握这些概念是后续动手实现的前提，同时也是面试和工程实践中高频考察的知识点。

![波形、采样、DFT 和频率 bin 的可视化](../assets/audio-fundamentals.svg)

**波形（Waveform）。** 一个一维浮点数组，值域 `[-1.0, 1.0]`。以采样点编号索引。要转换为秒数，除以采样率：`t = n / sr`。一段 10 秒的 16 kHz 音频片段是一个包含 160,000 个浮点数的数组。

**采样率（sr）。** 每秒多少个采样点。2026 年常用的采样率：

| 采样率 | 用途 |
|--------|------|
| 8 kHz | 电话通信、旧版 VOIP。奈奎斯特频率为 4 kHz，辅音信息丢失。ASR 应避免使用。 |
| 16 kHz | ASR 标准。Whisper、Parakeet、SeamlessM4T v2 均使用 16 kHz。 |
| 22.05 kHz | 旧版 TTS 声码器（vocoder）训练。 |
| 24 kHz | 现代 TTS（Kokoro、F5-TTS、xTTS v2）。 |
| 44.1 kHz | CD 音质，音乐。 |
| 48 kHz | 电影、专业音频、高保真 TTS（VALL-E 2、NaturalSpeech 3）。 |

**奈奎斯特-香农定理（Nyquist-Shannon）。** 采样率为 `sr` 时，可以无歧义表示的最高频率为 `sr/2`。`sr/2` 这个边界就是*奈奎斯特频率*。超过奈奎斯特频率的能量会被*混叠*——折叠到更低的频率中——从而破坏信号。降采样前务必进行低通滤波。

**位深度（Bit depth）。** 16 位 PCM（有符号 int16，范围 +/-32,767）是通用交换格式。音乐用 24 位，内部数字信号处理（DSP）用 32 位浮点。`soundfile` 等库读取 int16 但输出 `[-1, 1]` 范围的 float32 数组。

**傅里叶变换（Fourier Transform）。** 任何有限信号都可以表示为不同频率正弦波的叠加。离散傅里叶变换（DFT, Discrete Fourier Transform）对 `N` 个采样点计算 `N` 个复数系数——每个频率 bin 对应一个。`bin k` 对应频率 `k * sr / N` Hz。幅度（magnitude）是该频率的振幅，角度（angle）是相位。

**FFT（快速傅里叶变换）。** 当 `N` 是 2 的幂次时，FFT 是 DFT 的 `O(N log N)` 算法。每个音频库底层都使用 FFT。对 1024 个采样点做 FFT，采样率 16 kHz，得到 512 个可用频率 bin，覆盖 0-8 kHz，分辨率 15.6 Hz。

**分帧 + 加窗（Framing + window）。** 我们不会对整段音频做 FFT。而是将其切成重叠的*帧*（通常 25 ms 窗口，10 ms 步移），每帧乘以窗函数（Hann、Hamming）以消除边缘不连续性，然后对每帧做 FFT。这就是短时傅里叶变换（STFT, Short-Time Fourier Transform）。第 02 课从这里继续。

> **【拓展：语音 AI 的产品化】** 语音技术在产品化中面临独特挑战：不同口音、背景噪声、远场拾音、多人说话等。Siri、Alexa、小爱同学等产品都投入了大量工程优化来解决这些 "长尾问题"。实时性要求（<300ms 延迟）也是语音产品的核心指标。

> **【拓展：多语言语音技术】** 全球语言的语音特性差异巨大：声调语言（如中文）的音高携带语义，低资源语言缺乏训练数据。Meta 的 MMS 模型支持 1000+ 种语言的语音识别，Whisper 在多语言场景表现出色，但仍需针对特定语言微调。

## 动手实现

> **【中文解读】** 本节通过代码从零实现核心算法。这种 "from scratch" 的方式能帮助理解框架背后的原理，遇到问题时不会被黑盒困住。

### 步骤 1：读取音频片段并绘制波形

`code/main.py` 仅使用标准库的 `wave` 模块以保持演示无依赖。生产环境中你会使用 `soundfile` 或 `torchaudio.load`（两者都返回 `(waveform, sr)` 元组）：

```python
import soundfile as sf
waveform, sr = sf.read("clip.wav", dtype="float32")  # shape (T,), sr=int
```

### 步骤 2：从第一性原理合成正弦波

```python
import math

def sine(freq_hz, sr, seconds, amp=0.5):
    n = int(sr * seconds)
    return [amp * math.sin(2 * math.pi * freq_hz * i / sr) for i in range(n)]
```

一个 440 Hz 正弦波（标准 A 音）在 16 kHz 下 1 秒钟是 16,000 个浮点数。使用 `wave.open(..., "wb")` 以 16 位 PCM 编码写入。

### 步骤 3：手动计算 DFT

```python
def dft(x):
    N = len(x)
    out = []
    for k in range(N):
        re = sum(x[n] * math.cos(-2 * math.pi * k * n / N) for n in range(N))
        im = sum(x[n] * math.sin(-2 * math.pi * k * n / N) for n in range(N))
        out.append((re, im))
    return out
```

`O(N^2)` ——对于 `N=256` 来验证正确性可以，实际音频无用。实际代码调用 `numpy.fft.rfft` 或 `torch.fft.rfft`。

### 步骤 4：找到主频率

幅度峰值索引 `k_star` 对应频率 `k_star * sr / N`。对 440 Hz 正弦波运行此代码，峰值应出现在 bin `440 * N / sr`。

### 步骤 5：演示混叠

以 10 kHz 采样一个 7 kHz 正弦波（奈奎斯特 = 5 kHz）。7 kHz 音调超过奈奎斯特频率，折叠到 `10 - 7 = 3 kHz`。FFT 峰值出现在 3 kHz。这是经典的混叠演示，也是每个 DAC/ADC 都内置砖墙式低通滤波器的原因。

> **【中文解读】** 本节展示如何用成熟框架（如 PyTorch、HuggingFace 等）快速应用该技术。在实际项目中，优先使用经过验证的框架实现，可以减少 bug 并提高开发效率。

> **【拓展：语音与情感计算】** 语音不仅传递文字信息，还携带丰富的情感信号（语调、语速、音高变化）。情感语音识别（Speech Emotion Recognition, SER）在客服质检、心理健康监测、智能教育等领域有广泛应用。当前 SOTA 模型通常基于 wav2vec 2.0 或 HuBERT 等预训练模型微调。

## 用框架实现

2026 年你实际会使用的技术栈：

| 任务 | 库 | 原因 |
|------|----|------|
| 读写 WAV/FLAC/OGG | `soundfile`（libsndfile 封装） | 最快、最稳定，返回 float32。 |
| 重采样 | `torchaudio.transforms.Resample` 或 `librosa.resample` | 内置正确的抗混叠。 |
| STFT / Mel | `torchaudio` 或 `librosa` | GPU 友好；PyTorch 生态。 |
| 实时流 | `sounddevice` 或 `pyaudio` | 跨平台 PortAudio 绑定。 |
| 检查文件 | `ffprobe` 或 `soxi` | 命令行工具，快速，报告采样率/声道/编解码器。 |

> **【中文解读】** 本节关注如何将模型部署为可用的产品。从原型到生产级系统需要考虑性能优化、错误处理、监控等多个维度。

决策规则：**先匹配采样率，再匹配其他一切。** Whisper 期望 16 kHz 单声道 float32。给它 44.1 kHz 立体声，你会得到看起来像模型 bug 的垃圾输出。

> **【中文解读】** 练习题按照 Easy/Medium/Hard 三个难度递进。建议至少完成 Medium 级别的题目，Hard 级别适合深入研究或面试准备。

## 产出物

保存为 `outputs/skill-audio-loader.md`。该技能帮助你检查音频输入是否匹配下游模型的期望，并在不匹配时正确重采样。

## 练习题

1. **简单。** 合成一个 1 秒的 220 Hz + 440 Hz + 880 Hz 混合信号，采样率 16 kHz。运行 DFT。确认三个峰值出现在预期的 bin 位置。
2. **中等。** 以 48 kHz 录制一段 3 秒的语音 WAV 文件。使用 `torchaudio.transforms.Resample`（带抗混叠）降采样到 16 kHz，再用朴素抽取法（每三个采样点取一个）降采样到 16 kHz。对两者做 FFT。混叠出现在哪里？
3. **困难。** 仅使用 `math` 和步骤 3 的 DFT，从头构建 STFT。帧长 400，步移 160，Hann 窗。用 `matplotlib.pyplot.imshow` 绘制幅度图。这就是第 02 课的频谱图。

> **【中文解读】** 术语表中的 "What people say" vs "What it actually means" 区分了日常口语和精确技术含义。在团队协作中，统一术语定义可以避免大量沟通误解。

## 术语速查表

| 术语 | 通俗说法 | 实际含义 |
|------|----------|----------|
| 采样率（Sample rate） | 每秒多少采样点 | ADC 测量信号的频率，单位 Hz。 |
| 奈奎斯特（Nyquist） | 能表示的最高频率 | `sr/2`；超过它的能量会混叠回低频。 |
| 位深度（Bit depth） | 每个采样点的精度 | `int16` = 65,536 个级别；`float32` = `[-1, 1]` 内 24 位精度。 |
| DFT | 序列的傅里叶变换 | `N` 个采样点 -> `N` 个复数频率系数。 |
| FFT | 快速 DFT | `O(N log N)` 算法，要求 `N` = 2 的幂次。 |
| Bin | 频率列 | `k * sr / N` Hz；分辨率 = `sr / N`。 |
| STFT | 频谱图的底层实现 | 分帧 + 加窗的 FFT 随时间排列。 |
| 混叠（Aliasing） | 奇怪的频率幽灵 | 超过奈奎斯特的能量镜像到更低的 bin。 |

> **【中文解读】** 延伸阅读提供了深入学习的高质量资源。这些论文和教程是该领域的经典参考文献，适合需要深入理解的读者。

## 延伸阅读

- [Shannon (1949). Communication in the Presence of Noise](https://people.math.harvard.edu/~ctm/home/text/others/shannon/entropy/entropy.pdf) —— 采样定理背后的论文。
- [Smith — The Scientist and Engineer's Guide to Digital Signal Processing](https://www.dspguide.com/ch8.htm) —— 免费的权威 DSP 教材。
- [librosa 文档 — audio primer](https://librosa.org/doc/latest/tutorial.html) —— 带代码的实用教程。
- [Heinrich Kuttruff — Room Acoustics (6th ed.)](https://www.routledge.com/Room-Acoustics/Kuttruff/p/book/9781482260434) —— 解释为什么真实世界的音频不是干净的正弦波。
- [Steve Eddins — FFT Interpretation notebook](https://blogs.mathworks.com/steve/2020/03/30/fft-spectrum-and-spectral-densities/) —— 10 分钟理清频率 bin 直觉。

> **【中文解读】** 延伸阅读提供了深入学习的高质量资源，包括论文、教程和工具。建议按需选读，优先阅读标注为 "the critical read" 的核心论文。
