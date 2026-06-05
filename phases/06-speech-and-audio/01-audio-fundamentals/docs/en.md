# Audio Fundamentals — Waveforms, Sampling, Fourier Transform | 音频基础 — 波形、采样与傅里叶变换

> Waveforms are the raw signal. Spectrograms are the representation. Mel features are the ML-friendly form. Every modern ASR and TTS pipeline walks this ladder, and the first rung is understanding sampling and Fourier.

> **【中文解读】** 波形是原始信号，频谱图是表示形式，Mel 特征是机器学习友好的形式。每个现代语音识别（ASR）和语音合成（TTS）系统都沿这个阶梯向上：波形 → 频谱图 → Mel 特征。第一阶就是理解采样和傅里叶变换。

> **【拓展：音频 AI 的基础】** 采样率（如 16kHz）决定了可表示的最高频率（奈奎斯特定理）。傅里叶变换将时域信号分解为频域成分。这些概念是 Whisper、TTS、语音克隆等所有音频 AI 的基础。

**Type:** Learn | **类型:** 学习
**Languages:** Python | **语言:** Python
**Prerequisites:** Phase 1 · 06 (Vectors & Matrices), Phase 1 · 14 (Probability Distributions) | **前置知识:** 阶段 1 · 06（向量与矩阵），阶段 1 · 14（概率分布）
**Time:** ~45 minutes | **预计用时:** ~45 分钟

## The Problem | 问题引入

A microphone produces a pressure-vs-time signal. Your neural net consumes tensors. Between them sits a stack of conventions that, when violated, produce silent bugs: the model trains fine but the WER doubles, or TTS ships a hiss, or a voice cloning system memorizes the microphone instead of the speaker.

> 麦克风产生一个压力-时间信号。你的神经网络消费的是张量。两者之间是一堆约定——违反这些约定会产生隐性 bug：模型训练正常但 WER 翻倍，或者 TTS 输出嘶嘶声，或者语音克隆系统记住了麦克风而不是说话人。

> **【中文解读】** 本节提出的问题是：如何在实际工程中正确理解和应用这一技术。理解问题背景有助于把握技术选型的关键决策点。在实际 AI 系统中，错误的技术选型往往比实现细节的 bug 代价更高。

Every bug in speech systems traces back to one of three questions:

> 语音系统中的每个 bug 都可以追溯到以下三个问题之一：

1. What sample rate was the data recorded at, and what does the model expect?
   数据的录制采样率是多少，模型期望的采样率是多少？
2. Is the signal aliased?
   信号是否存在混叠？
3. Are you operating on raw samples or on a frequency representation?
   你在处理原始采样点还是频率表示？

Get these right and the rest of Phase 6 is tractable. Get them wrong and even Whisper-Large-v4 produces garbage.

> 搞对这三个问题，阶段 6 的其余内容就容易理解了。搞错了，即使是 Whisper-Large-v4 也会输出垃圾。

## The Concept | 核心概念

> **【中文解读】** 本节介绍核心概念和理论基础。掌握这些概念是后续动手实现的前提，同时也是面试和工程实践中高频考察的知识点。


![Waveform, sampling, DFT, and frequency bins visualized](../assets/audio-fundamentals.svg)

**Waveform.** A one-dimensional array of floats in `[-1.0, 1.0]`. Indexed by sample number. To convert to seconds, divide by the sample rate: `t = n / sr`. A 10-second clip at 16 kHz is an array of 160,000 floats.

> **波形（Waveform）。** 一个取值在 `[-1.0, 1.0]` 之间的一维浮点数组。以采样编号为索引。要转换为秒数，除以采样率：`t = n / sr`。一段 10 秒的 16 kHz 音频是 160,000 个浮点数的数组。

**Sampling rate (sr).** How many samples per second. Common rates in 2026:

> **采样率（sr）。** 每秒的采样点数。2026 年常用采样率：

| Rate | Use |
|------|-----|
| 8 kHz | Telephony, legacy VOIP. Nyquist at 4 kHz kills consonants. Avoid for ASR. |
| 16 kHz | ASR standard. Whisper, Parakeet, SeamlessM4T v2 all consume 16 kHz. |
| 22.05 kHz | TTS vocoder training for older models. |
| 24 kHz | Modern TTS (Kokoro, F5-TTS, xTTS v2). |
| 44.1 kHz | CD audio, music. |
| 48 kHz | Film, pro audio, high-fidelity TTS (VALL-E 2, NaturalSpeech 3). |

| 采样率 | 用途 |
|--------|------|
| 8 kHz | 电话、传统 VOIP。奈奎斯特频率 4 kHz 会丢失辅音。ASR 应避免使用。 |
| 16 kHz | ASR 标准。Whisper、Parakeet、SeamlessM4T v2 均使用 16 kHz。 |
| 22.05 kHz | 旧模型 TTS 声码器训练。 |
| 24 kHz | 现代 TTS（Kokoro、F5-TTS、xTTS v2）。 |
| 44.1 kHz | CD 音质、音乐。 |
| 48 kHz | 电影、专业音频、高保真 TTS（VALL-E 2、NaturalSpeech 3）。 |

**Nyquist-Shannon.** A sample rate of `sr` can unambiguously represent frequencies up to `sr/2`. The `sr/2` boundary is the *Nyquist frequency*. Energy above Nyquist gets *aliased* — folded down into lower frequencies — and corrupts the signal. Always low-pass filter before downsampling.

> **奈奎斯特-香农定理。** 采样率 `sr` 可以无歧义地表示最高到 `sr/2` 的频率。`sr/2` 边界就是*奈奎斯特频率*。超过奈奎斯特的能量会被*混叠*——折叠到更低的频率——从而破坏信号。降采样前务必先进行低通滤波。

**Bit depth.** 16-bit PCM (signed int16, range ±32,767) is the universal exchange format. 24-bit for music, 32-bit float for internal DSP. Libraries like `soundfile` read int16 but expose float32 arrays in `[-1, 1]`.

> **位深度。** 16 位 PCM（有符号 int16，范围 ±32,767）是通用交换格式。音乐用 24 位，内部 DSP 用 32 位浮点。`soundfile` 等库读取 int16 但返回 `[-1, 1]` 范围的 float32 数组。

**Fourier Transform.** Any finite signal is a sum of sinusoids at different frequencies. The Discrete Fourier Transform (DFT) computes, for `N` samples, `N` complex coefficients — one per frequency bin. `bin k` maps to frequency `k · sr / N` Hz. Magnitude is amplitude at that frequency, angle is phase.

> **傅里叶变换。** 任何有限信号都可以分解为不同频率的正弦波之和。离散傅里叶变换（DFT）对 `N` 个采样点计算 `N` 个复数系数——每个频率 bin 一个。`bin k` 对应频率 `k · sr / N` Hz。幅度是该频率的振幅，角度是相位。

**FFT.** Fast Fourier Transform: an `O(N log N)` algorithm for the DFT when `N` is a power of 2. Every audio library uses FFT under the hood. A 1024-sample FFT at 16 kHz gives 512 usable frequency bins spanning 0–8 kHz at 15.6 Hz resolution.

> **FFT。** 快速傅里叶变换：当 `N` 为 2 的幂时，DFT 的 `O(N log N)` 算法。每个音频库底层都使用 FFT。16 kHz 下 1024 采样点的 FFT 产生 512 个可用频率 bin，覆盖 0–8 kHz，分辨率为 15.6 Hz。

**Framing + window.** We do not FFT an entire clip. We chop it into overlapping *frames* (typically 25 ms with 10 ms hop), multiply each frame by a window function (Hann, Hamming) to kill edge discontinuities, then FFT each frame. This is the Short-Time Fourier Transform (STFT). Lesson 02 picks up from here.

> **分帧 + 加窗。** 我们不对整段音频做 FFT。而是将其切成重叠的*帧*（通常 25 ms，步长 10 ms），每帧乘以窗函数（Hann、Hamming）以消除边缘不连续性，然后对每帧做 FFT。这就是短时傅里叶变换（STFT）。第 02 课将从此处继续。

> **【拓展：语音 AI 的产品化】** 语音技术在产品化中面临独特挑战：不同口音、背景噪声、远场拾音、多人说话等。Siri、Alexa、小爱同学等产品都投入了大量工程优化来解决这些 "长尾问题"。实时性要求（<300ms 延迟）也是语音产品的核心指标。

> **【拓展：多语言语音技术】** 全球语言的语音特性差异巨大：声调语言（如中文）的音高携带语义，低资源语言缺乏训练数据。Meta 的 MMS 模型支持 1000+ 种语言的语音识别，Whisper 在多语言场景表现出色，但仍需针对特定语言微调。



## Build It | 动手实现

> **【中文解读】** 本节通过代码从零实现核心算法。这种 "from scratch" 的方式能帮助理解框架背后的原理，遇到问题时不会被黑盒困住。


### Step 1: read a clip and plot the waveform

`code/main.py` uses only the stdlib `wave` module to keep the demo dependency-free. For production you will use `soundfile` or `torchaudio.load` (both return `(waveform, sr)` tuples):

> `code/main.py` 仅使用标准库的 `wave` 模块以保持演示无依赖。生产环境你会使用 `soundfile` 或 `torchaudio.load`（两者都返回 `(waveform, sr)` 元组）：

```python
import soundfile as sf
waveform, sr = sf.read("clip.wav", dtype="float32")  # shape (T,), sr=int
```

### Step 2: synthesize a sine wave from first principles

```python
import math

def sine(freq_hz, sr, seconds, amp=0.5):
    n = int(sr * seconds)
    return [amp * math.sin(2 * math.pi * freq_hz * i / sr) for i in range(n)]
```

A 440 Hz sine (concert A) at 16 kHz for 1 second is 16,000 floats. Write with `wave.open(..., "wb")` using 16-bit PCM encoding.

> 16 kHz 采样率下 440 Hz 正弦波（标准音 A）持续 1 秒是 16,000 个浮点数。使用 `wave.open(..., "wb")` 以 16 位 PCM 编码写入。

### Step 3: compute the DFT by hand

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

`O(N²)` — fine for `N=256` to confirm correctness, useless for real audio. Real code calls `numpy.fft.rfft` or `torch.fft.rfft`.

> `O(N²)` 复杂度——对 `N=256` 验证正确性还行，对真实音频没用。实际代码调用 `numpy.fft.rfft` 或 `torch.fft.rfft`。

### Step 4: find the dominant frequency

Magnitude peak index `k_star` maps to frequency `k_star * sr / N`. Running this on the 440 Hz sine should return a peak at bin `440 * N / sr`.

> 幅度峰值索引 `k_star` 对应频率 `k_star * sr / N`。对 440 Hz 正弦波运行此函数应在 bin `440 * N / sr` 处返回峰值。

### Step 5: demonstrate aliasing

Sample a 7 kHz sine at 10 kHz (Nyquist = 5 kHz). The 7 kHz tone is above Nyquist and folds to `10 − 7 = 3 kHz`. The FFT peak appears at 3 kHz. This is the classic aliasing demo and the reason every DAC/ADC ships with a brick-wall low-pass filter.

> 以 10 kHz 采样 7 kHz 正弦波（奈奎斯特频率 = 5 kHz）。7 kHz 音调高于奈奎斯特频率，会折叠到 `10 − 7 = 3 kHz`。FFT 峰值出现在 3 kHz 处。这是经典的混叠演示，也是每个 DAC/ADC 都配备砖墙式低通滤波器的原因。

> **【中文解读】** 本节展示如何用成熟框架（如 PyTorch、HuggingFace 等）快速应用该技术。在实际项目中，优先使用经过验证的框架实现，可以减少 bug 并提高开发效率。





> **【拓展：语音与情感计算】** 语音不仅传递文字信息，还携带丰富的情感信号（语调、语速、音高变化）。情感语音识别（Speech Emotion Recognition, SER）在客服质检、心理健康监测、智能教育等领域有广泛应用。当前 SOTA 模型通常基于 wav2vec 2.0 或 HuBERT 等预训练模型微调。

## Use It | 用框架实现

The stack you will actually ship in 2026:

> 2026 年你实际会使用的技术栈：

| Task | Library | Why |
|------|---------|-----|
| Read/write WAV/FLAC/OGG | `soundfile` (libsndfile wrapper) | Fastest, stable, returns float32. |
| Resample | `torchaudio.transforms.Resample` or `librosa.resample` | Correct anti-aliasing built in. |
| STFT / Mel | `torchaudio` or `librosa` | GPU-friendly; PyTorch ecosystem. |
| Real-time streaming | `sounddevice` or `pyaudio` | Cross-platform PortAudio bindings. |
| Inspect a file | `ffprobe` or `soxi` | CLI, fast, reports sr/channels/codec. |

| 任务 | 库 | 原因 |
|------|----|------|
| 读写 WAV/FLAC/OGG | `soundfile`（libsndfile 封装） | 最快、最稳定，返回 float32。 |
| 重采样 | `torchaudio.transforms.Resample` 或 `librosa.resample` | 内置正确的抗混叠滤波。 |
| STFT / Mel | `torchaudio` 或 `librosa` | GPU 友好；PyTorch 生态。 |
| 实时流 | `sounddevice` 或 `pyaudio` | 跨平台 PortAudio 绑定。 |
| 检查文件 | `ffprobe` 或 `soxi` | 命令行工具，快速报告采样率/声道/编码。 |

> **【中文解读】** 本节关注如何将模型部署为可用的产品。从原型到生产级系统需要考虑性能优化、错误处理、监控等多个维度。


Decision rule: **match sample rate before you match anything else**. Whisper expects 16 kHz mono float32. Pass it 44.1 kHz stereo and you will get garbage that looks like a model bug.

> 决策规则：**在匹配其他任何东西之前先匹配采样率**。Whisper 期望 16 kHz 单声道 float32。传入 44.1 kHz 立体声，你会得到看起来像模型 bug 的垃圾输出。

> **【中文解读】** 练习题按照 Easy/Medium/Hard 三个难度递进。建议至少完成 Medium 级别的题目，Hard 级别适合深入研究或面试准备。




## Ship It | 产出物

Save as `outputs/skill-audio-loader.md`. The skill helps you check that audio input matches the expectations of the downstream model and resamples correctly when it does not.

> 保存为 `outputs/skill-audio-loader.md`。该技能帮助你检查音频输入是否匹配下游模型的期望，并在不匹配时正确重采样。

## Exercises | 练习题

1. **Easy.** Synthesize a 1-second mix of 220 Hz + 440 Hz + 880 Hz at 16 kHz. Run DFT. Confirm three peaks at the expected bins.
   **简单。** 合成一个 220 Hz + 440 Hz + 880 Hz 的 1 秒混合信号，采样率 16 kHz。运行 DFT。确认在预期 bin 位置有三个峰值。
2. **Medium.** Record a 3-second WAV of your voice at 48 kHz. Downsample to 16 kHz using `torchaudio.transforms.Resample` (with anti-aliasing), then to 16 kHz using naive decimation (every third sample). FFT both. Where does the aliasing appear?
   **中等。** 录制一段 3 秒 48 kHz 的语音 WAV。使用 `torchaudio.transforms.Resample`（带抗混叠）降采样到 16 kHz，然后用朴素抽取（每隔三个样本取一个）降采样到 16 kHz。对两者做 FFT。混叠出现在哪里？
3. **Hard.** Build the STFT from scratch using only `math` and the DFT from Step 3. Frame size 400, hop 160, Hann window. Plot magnitudes with `matplotlib.pyplot.imshow`. This is the spectrogram of Lesson 02.
   **困难。** 仅用 `math` 和步骤 3 的 DFT 从零构建 STFT。帧大小 400，步长 160，Hann 窗。用 `matplotlib.pyplot.imshow` 绘制幅度图。这就是第 02 课的频谱图。

> **【中文解读】** 术语表中的 "What people say" vs "What it actually means" 区分了日常口语和精确技术含义。在团队协作中，统一术语定义可以避免大量沟通误解。


## Key Terms | 术语速查表

| Term | What people say | What it actually means |
|------|-----------------|-----------------------|
| Sample rate | How many samples per second | Frequency in Hz at which the ADC measures the signal. |
| Nyquist | The max frequency you can represent | `sr/2`; energy above it aliases back down. |
| Bit depth | Resolution of each sample | `int16` = 65,536 levels; `float32` = 24-bit precision in `[-1, 1]`. |
| DFT | The Fourier transform for sequences | `N` samples → `N` complex frequency coefficients. |
| FFT | The fast DFT | `O(N log N)` algorithm requiring `N` = power of 2. |
| Bin | Frequency column | `k · sr / N` Hz; resolution = `sr / N`. |
| STFT | Spectrogram under the hood | Framed + windowed FFT over time. |
| Aliasing | Weird frequency ghosts | Energy above Nyquist mirroring down to lower bins. |

| 术语 | 人们常说的 | 实际含义 |
|------|-----------|---------|
| 采样率 | 每秒多少个采样点 | ADC 测量信号的频率（Hz）。 |
| 奈奎斯特 | 能表示的最大频率 | `sr/2`；超过它的能量会混叠回来。 |
| 位深度 | 每个采样点的精度 | `int16` = 65,536 级；`float32` = `[-1, 1]` 中 24 位精度。 |
| DFT | 序列的傅里叶变换 | `N` 个采样 → `N` 个复数频率系数。 |
| FFT | 快速 DFT | `O(N log N)` 算法，要求 `N` 为 2 的幂。 |
| Bin | 频率列 | `k · sr / N` Hz；分辨率 = `sr / N`。 |
| STFT | 频谱图的底层实现 | 分帧 + 加窗的 FFT 随时间推移。 |
| 混叠 | 奇怪的频率鬼影 | 超过奈奎斯特的能量镜像到更低的 bin。 |

> **【中文解读】** 延伸阅读提供了深入学习的高质量资源。这些论文和教程是该领域的经典参考文献，适合需要深入理解的读者。


## Further Reading | 延伸阅读

- [Shannon (1949). Communication in the Presence of Noise](https://people.math.harvard.edu/~ctm/home/text/others/shannon/entropy/entropy.pdf) — the paper behind the sampling theorem.
  Shannon (1949)——带噪声条件下的通信——采样定理背后的论文。
- [Smith — The Scientist and Engineer's Guide to Digital Signal Processing](https://www.dspguide.com/ch8.htm) — free, canonical DSP textbook.
  Smith——科学家与工程师的数字信号处理指南——免费的经典 DSP 教材。
- [librosa docs — audio primer](https://librosa.org/doc/latest/tutorial.html) — practical walkthrough with code.
  librosa 文档——音频入门——带代码的实践教程。
- [Heinrich Kuttruff — Room Acoustics (6th ed.)](https://www.routledge.com/Room-Acoustics/Kuttruff/p/book/9781482260434) — reference for why real-world audio is not a clean sinusoid.
  Heinrich Kuttruff——房间声学（第 6 版）——解释为什么真实世界音频不是干净正弦波的参考书。
- [Steve Eddins — FFT Interpretation notebook](https://blogs.mathworks.com/steve/2020/03/30/fft-spectrum-and-spectral-densities/) — frequency bin intuition cleared up in 10 minutes.
  Steve Eddins——FFT 解读笔记——10 分钟搞清频率 bin 的直觉。

> **【中文解读】** 延伸阅读提供了深入学习的高质量资源，包括论文、教程和工具。建议按需选读，优先阅读标注为 "the critical read" 的核心论文。

