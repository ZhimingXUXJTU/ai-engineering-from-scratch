# Spectrograms, Mel Scale & Audio Features | 频谱图、Mel 尺度与音频特征

> Neural nets do not consume raw waveforms well. They consume spectrograms. They consume mel spectrograms even better. Every ASR, TTS, and audio classifier in 2026 lives or dies by this single preprocessing choice.

> **【中文解读】** 神经网络处理原始波形效果不好，但处理频谱图效果好，处理 Mel 频谱图效果更好。2026 年所有 ASR、TTS 和音频分类器的成败取决于这一个预处理选择。Mel 尺度模拟人耳对频率的感知（低频精细、高频粗略）。

> **【拓展：Mel 频谱图是音频 AI 的 "图像"】** Mel 频谱图将音频转换为 2D 图像（时间×频率），可以用 CNN/ViT 处理。Whisper、MusicGen、Stable Audio 都使用 Mel 频谱图作为中间表示。

**Type:** Build | **类型:** 构建
**Languages:** Python | **语言:** Python
**Prerequisites:** Phase 6 · 01 (Audio Fundamentals) | **前置知识:** 阶段 6 · 01（音频基础）
**Time:** ~45 minutes | **预计用时:** ~45 分钟

## The Problem | 问题引入

Take a 10-second 16 kHz clip. That is 160,000 floats, all in `[-1, 1]`, almost perfectly uncorrelated with the label "dog barking" or "the word cat". The raw waveform has the information but in a form the model cannot easily extract. Two identical phonemes spoken 100 ms apart have completely different raw samples.

> 拿一段 10 秒的 16 kHz 音频。那是 160,000 个浮点数，全在 `[-1, 1]` 范围内，几乎与标签"狗叫"或"单词 cat"完全不相关。原始波形包含信息，但形式是模型难以提取的。间隔 100 ms 的两个相同音素的原始采样完全不同。

> **【中文解读】** 本节提出的问题是：如何在实际工程中正确理解和应用这一技术。理解问题背景有助于把握技术选型的关键决策点。在实际 AI 系统中，错误的技术选型往往比实现细节的 bug 代价更高。

A spectrogram fixes this. It collapses the temporal detail where human perception ignores it (microsecond jitter) and preserves the structure where perception attends (which frequencies are energetic, over time windows of ~10–25 ms).

> 频谱图解决了这个问题。它压缩了人类感知忽略的时间细节（微秒级抖动），保留了感知关注的结构（在约 10–25 ms 的时间窗口内，哪些频率有能量）。

Mel spectrograms push further. Humans perceive pitch logarithmically: 100 Hz vs 200 Hz sounds "the same distance apart" as 1000 Hz vs 2000 Hz. The mel scale warps the frequency axis to match. A mel-scaled spectrogram is the single most important feature in speech ML from 2010 through 2026.

> Mel 频谱图更进一步。人类对音高的感知是对数的：100 Hz 与 200 Hz 听起来和 1000 Hz 与 2000 Hz "距离一样远"。Mel 尺度将频率轴扭曲以匹配这种感知。Mel 频谱图是 2010 到 2026 年语音机器学习中最重要的单一特征。

## The Concept | 核心概念

> **【中文解读】** 本节介绍核心概念和理论基础。掌握这些概念是后续动手实现的前提，同时也是面试和工程实践中高频考察的知识点。


![Waveform to STFT to mel spectrogram to MFCC ladder](../assets/mel-features.svg)

**STFT (Short-Time Fourier Transform).** Slice the waveform into overlapping frames (typical: 25 ms window, 10 ms hop = 400 samples / 160 samples at 16 kHz). Multiply each frame by a window function (Hann is the default; Hamming slightly different tradeoff). FFT each frame. Stack the magnitude spectra into a matrix of shape `(n_frames, n_freq_bins)`. That is your spectrogram.

> **STFT（短时傅里叶变换）。** 将波形切成重叠的帧（典型：25 ms 窗口，10 ms 步长 = 16 kHz 下 400 采样点 / 160 采样点）。每帧乘以窗函数（默认 Hann；Hamming 略有不同）。对每帧做 FFT。将幅度谱堆叠成 `(n_frames, n_freq_bins)` 形状的矩阵。这就是你的频谱图。

**Log-magnitude.** Raw magnitudes span 5-6 orders of magnitude. Take `log(|X| + 1e-6)` or `20 * log10(|X|)` to compress dynamic range. Every production pipeline uses log-magnitude, not raw magnitude.

> **对数幅度。** 原始幅度跨 5-6 个数量级。取 `log(|X| + 1e-6)` 或 `20 * log10(|X|)` 来压缩动态范围。每个生产流水线都使用对数幅度而非原始幅度。

**Mel scale.** Frequency `f` in Hz maps to mel `m` by `m = 2595 * log10(1 + f / 700)`. The mapping is roughly linear below 1 kHz and roughly logarithmic above. 80 mel bins covering 0–8 kHz is the standard ASR input.

> **Mel 尺度。** 频率 `f`（Hz）映射到 mel `m` 的公式为 `m = 2595 * log10(1 + f / 700)`。该映射在 1 kHz 以下大致线性，以上大致对数。覆盖 0–8 kHz 的 80 个 mel bin 是标准 ASR 输入。

**Mel filterbank.** A set of triangular filters spaced equally on the mel scale. Each filter is a weighted sum of adjacent FFT bins. Multiplying the STFT magnitude by the filterbank matrix gives the mel spectrogram in one matmul.

> **Mel 滤波器组。** 一组在 mel 尺度上等间距排列的三角滤波器。每个滤波器是相邻 FFT bin 的加权和。将 STFT 幅度乘以滤波器组矩阵即可通过一次矩阵乘法得到 mel 频谱图。

**Log-mel spectrogram.** `log(mel_spec + 1e-10)`. Whisper's input. Parakeet's input. SeamlessM4T's input. The universal 2026 audio frontend.

> **对数 Mel 频谱图。** `log(mel_spec + 1e-10)`。Whisper 的输入。Parakeet 的输入。SeamlessM4T 的输入。2026 年通用的音频前端。

**MFCCs.** Take the log-mel spectrogram, apply a DCT (type II), keep the first 13 coefficients. Decorrelates the features and compresses further. Dominant feature until about 2015 when CNNs/Transformers on raw log-mels caught up. Still used in speaker recognition (x-vectors, ECAPA).

> **MFCC。** 取对数 Mel 频谱图，应用 DCT（类型 II），保留前 13 个系数。去除特征间相关性并进一步压缩。2015 年之前的主流特征，之后 CNN/Transformer 在原始 log-mel 上追上。仍用于说话人识别（x-vectors、ECAPA）。

**Resolution trade.** Larger FFT = better frequency resolution but worse time resolution. 25 ms / 10 ms is the audio-ML default; 50 ms / 12.5 ms for music; 5 ms / 2 ms for transient detection (drum hits, plosives).

> **分辨率权衡。** 更大的 FFT = 更好的频率分辨率但更差的时间分辨率。25 ms / 10 ms 是音频 ML 的默认值；50 ms / 12.5 ms 用于音乐；5 ms / 2 ms 用于瞬态检测（鼓击、爆破音）。

> **【拓展：语音 AI 的产品化】** 语音技术在产品化中面临独特挑战：不同口音、背景噪声、远场拾音、多人说话等。Siri、Alexa、小爱同学等产品都投入了大量工程优化来解决这些 "长尾问题"。实时性要求（<300ms 延迟）也是语音产品的核心指标。

> **【拓展：多语言语音技术】** 全球语言的语音特性差异巨大：声调语言（如中文）的音高携带语义，低资源语言缺乏训练数据。Meta 的 MMS 模型支持 1000+ 种语言的语音识别，Whisper 在多语言场景表现出色，但仍需针对特定语言微调。



## Build It | 动手实现

> **【中文解读】** 本节通过代码从零实现核心算法。这种 "from scratch" 的方式能帮助理解框架背后的原理，遇到问题时不会被黑盒困住。


### Step 1: frame the waveform

```python
def frame(signal, frame_len, hop):
    n = 1 + (len(signal) - frame_len) // hop
    return [signal[i * hop : i * hop + frame_len] for i in range(n)]
```

A 10-second 16 kHz clip with `frame_len=400, hop=160` yields 998 frames.

> 一段 10 秒 16 kHz 的音频，使用 `frame_len=400, hop=160`，得到 998 帧。

### Step 2: Hann window

```python
import math

def hann(N):
    return [0.5 * (1 - math.cos(2 * math.pi * n / (N - 1))) for n in range(N)]
```

Multiply element-wise before the FFT. Removes spectral leakage caused by truncating at non-zero endpoints.

> 在 FFT 之前逐元素相乘。消除因在非零端点处截断导致的频谱泄漏。

### Step 3: STFT magnitude

```python
def stft_magnitude(signal, frame_len=400, hop=160):
    win = hann(frame_len)
    frames = frame(signal, frame_len, hop)
    return [magnitudes(dft([w * s for w, s in zip(win, f)])) for f in frames]
```

Production uses `torch.stft` or `librosa.stft` (FFT-backed, vectorized). The loop here is pedagogical; it runs on short clips in `code/main.py`.

> 生产环境使用 `torch.stft` 或 `librosa.stft`（基于 FFT、向量化）。这里的循环是教学目的；它在 `code/main.py` 中处理短音频片段。

### Step 4: mel filterbank

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

80 mels covering 0–8 kHz with `n_fft=400` gives an `(80, 201)` matrix. Multiply the `(n_frames, 201)` STFT magnitude by the transpose to get `(n_frames, 80)` mel spectrogram.

> 覆盖 0–8 kHz 的 80 个 mel 滤波器，`n_fft=400`，得到 `(80, 201)` 矩阵。将 `(n_frames, 201)` 的 STFT 幅度乘以转置得到 `(n_frames, 80)` 的 mel 频谱图。

### Step 5: log-mel

```python
def log_mel(mel_spec, eps=1e-10):
    return [[math.log(max(v, eps)) for v in frame] for frame in mel_spec]
```

Common alternatives: `librosa.power_to_db` (reference-normalized dB), `10 * log10(power + eps)`. Whisper uses a more involved clip + normalize routine (see Whisper's `log_mel_spectrogram`).

> 常见替代方案：`librosa.power_to_db`（参考归一化 dB）、`10 * log10(power + eps)`。Whisper 使用更复杂的裁剪 + 归一化流程（参见 Whisper 的 `log_mel_spectrogram`）。

### Step 6: MFCCs

```python
def dct_ii(x, n_coeffs):
    N = len(x)
    return [
        sum(x[n] * math.cos(math.pi * k * (2 * n + 1) / (2 * N)) for n in range(N))
        for k in range(n_coeffs)
    ]
```

> **【中文解读】** 本节展示如何用成熟框架（如 PyTorch、HuggingFace 等）快速应用该技术。在实际项目中，优先使用经过验证的框架实现，可以减少 bug 并提高开发效率。


Apply DCT to each log-mel frame, keep the first 13 coefficients. That is your MFCC matrix. The first coefficient is usually dropped (it encodes overall energy).

> 对每个 log-mel 帧应用 DCT，保留前 13 个系数。这就是你的 MFCC 矩阵。第一个系数通常被丢弃（它编码的是整体能量）。




> **【拓展：语音与情感计算】** 语音不仅传递文字信息，还携带丰富的情感信号（语调、语速、音高变化）。情感语音识别（Speech Emotion Recognition, SER）在客服质检、心理健康监测、智能教育等领域有广泛应用。当前 SOTA 模型通常基于 wav2vec 2.0 或 HuBERT 等预训练模型微调。

## Use It | 用框架实现

The 2026 stack:

> 2026 年的技术栈：

| Task | Features |
|------|----------|
| ASR (Whisper, Parakeet, SeamlessM4T) | 80 log-mels, 10 ms hop, 25 ms window |
| TTS acoustic model (VITS, F5-TTS, Kokoro) | 80 mels, 5–12 ms hop for fine temporal control |
| Audio classification (AST, PANNs, BEATs) | 128 log-mels, 10 ms hop |
| Speaker embedding (ECAPA-TDNN, WavLM) | 80 log-mels or raw-waveform SSL |
| Music (MusicGen, Stable Audio 2) | EnCodec discrete tokens (not mels) |
| Keyword spotting | 40 MFCCs for tiny devices |

| 任务 | 特征配置 |
|------|----------|
| ASR（Whisper、Parakeet、SeamlessM4T） | 80 log-mels，10 ms 步长，25 ms 窗口 |
| TTS 声学模型（VITS、F5-TTS、Kokoro） | 80 mels，5–12 ms 步长，精细时间控制 |
| 音频分类（AST、PANNs、BEATs） | 128 log-mels，10 ms 步长 |
| 说话人嵌入（ECAPA-TDNN、WavLM） | 80 log-mels 或原始波形 SSL |
| 音乐（MusicGen、Stable Audio 2） | EnCodec 离散 token（非 mels） |
| 关键词检测 | 40 MFCCs，用于小型设备 |

Rule of thumb: **if you are not working on music, start with 80 log-mels.** The burden of proof is on any deviation.

> 经验法则：**如果你不是在做音乐，就从 80 log-mels 开始。** 任何偏离都需要证明其合理性。



## Pitfalls that still ship in 2026

> 2026 年仍然在犯的陷阱

- **Mel count mismatch.** Training with 80 mels, inference with 128 mels. Silent failure. Log the feature shape at both ends.
  **Mel 数量不匹配。** 训练用 80 mels，推理用 128 mels。静默失败。在两端记录特征形状。
- **Sample-rate mismatch upstream.** Mels computed at 22.05 kHz look different from 16 kHz. Fix SR *before* featurization.
  **上游采样率不匹配。** 22.05 kHz 计算的 mels 与 16 kHz 的不同。在特征化*之前*修正采样率。
- **dB vs log.** Whisper expects log-mel, not dB-mel. Some HF pipelines autodetect; your custom code will not.
  **dB 与 log。** Whisper 期望 log-mel 而非 dB-mel。某些 HF 流水线会自动检测；你的自定义代码不会。
- **Normalization drift.** Per-utterance normalization during training, global normalization during inference. Production bug that doubles WER.
  **归一化漂移。** 训练时逐句归一化，推理时全局归一化。这种生产 bug 会使 WER 翻倍。
- **Leakage from padding.** Zero-padding the end of a clip produces a flat spectrum in the trailing frames. Pad symmetrically or replicate.
  **填充泄漏。** 对音频片段末尾零填充会在尾部帧产生平坦频谱。使用对称填充或复制填充。

> **【中文解读】** 本节关注如何将模型部署为可用的产品。从原型到生产级系统需要考虑性能优化、错误处理、监控等多个维度。


## Ship It | 产出物

Save as `outputs/skill-feature-extractor.md`. The skill picks feature type, mel count, frame/hop, and normalization for a given model target.

> 保存为 `outputs/skill-feature-extractor.md`。该技能为给定模型目标选择特征类型、mel 数量、帧/步长和归一化方式。

## Exercises | 练习题

1. **Easy.** Run `code/main.py`. It synthesizes a chirp (frequency swept 200 → 4000 Hz) and prints the argmax mel bin per frame. Plot (optional) and confirm it matches the sweep.
   **简单。** 运行 `code/main.py`。它合成一个啁啾信号（频率从 200 扫到 4000 Hz）并打印每帧的 argmax mel bin。绘图（可选）并确认与扫频匹配。
2. **Medium.** Re-run with `n_mels` in `{40, 80, 128}` and `frame_len` in `{200, 400, 800}`. Measure sharp-peak bandwidth across the time axis. Which combo resolves the chirp the best?
   **中等。** 用 `n_mels` 为 `{40, 80, 128}` 和 `frame_len` 为 `{200, 400, 800}` 重新运行。沿时间轴测量锐峰带宽。哪个组合分辨啁啾信号最好？
3. **Hard.** Implement `power_to_db` and compare ASR accuracy of a tiny CNN classifier on AudioMNIST using (a) raw log-mel, (b) dB-mel with `ref=max`, (c) MFCC-13 + delta + delta-delta. Report top-1 accuracy.
   **困难。** 实现 `power_to_db`，在 AudioMNIST 上用微型 CNN 分类器比较 (a) 原始 log-mel、(b) `ref=max` 的 dB-mel、(c) MFCC-13 + delta + delta-delta 的 ASR 准确率。报告 top-1 准确率。

> **【中文解读】** 术语表中的 "What people say" vs "What it actually means" 区分了日常口语和精确技术含义。在团队协作中，统一术语定义可以避免大量沟通误解。


## Key Terms | 术语速查表

| Term | What people say | What it actually means |
|------|-----------------|-----------------------|
| Frame | A slice | 25 ms chunk of waveform fed to one FFT. |
| Hop | Stride | Samples between consecutive frames; 10 ms is ASR default. |
| Window | Hann/Hamming thing | Point-wise multiplier that tapers the frame edges to zero. |
| STFT | Spectrogram generator | Framed + windowed FFT; yields time × frequency matrix. |
| Mel | Warped frequency | Log-perception scale; `m = 2595·log10(1 + f/700)`. |
| Filterbank | The matrix | Triangular filters that project STFT onto mel bins. |
| Log-mel | Whisper's input | `log(mel_spec + eps)`; standardized in 2026. |
| MFCC | Old-school feature | DCT of log-mel; 13 coeffs, decorrelated. |

| 术语 | 人们常说的 | 实际含义 |
|------|-----------|---------|
| 帧 | 一段切片 | 送入一次 FFT 的 25 ms 波形片段。 |
| 步长 | 步幅 | 连续帧之间的采样点数；10 ms 是 ASR 默认值。 |
| 窗函数 | Hann/Hamming 那个东西 | 将帧边缘逐渐缩减为零的逐点乘数。 |
| STFT | 频谱图生成器 | 分帧 + 加窗的 FFT；产生时间 × 频率矩阵。 |
| Mel | 扭曲的频率 | 对数感知尺度；`m = 2595·log10(1 + f/700)`。 |
| 滤波器组 | 那个矩阵 | 将 STFT 投影到 mel bin 的三角滤波器。 |
| Log-mel | Whisper 的输入 | `log(mel_spec + eps)`；2026 年标准化。 |
| MFCC | 老派特征 | log-mel 的 DCT；13 个系数，去相关。 |

> **【中文解读】** 延伸阅读提供了深入学习的高质量资源。这些论文和教程是该领域的经典参考文献，适合需要深入理解的读者。


## Further Reading | 延伸阅读

- [Davis, Mermelstein (1980). Comparison of parametric representations for monosyllabic word recognition](https://ieeexplore.ieee.org/document/1163420) — the MFCC paper.
  Davis、Mermelstein (1980)——单音节词识别的参数化表示比较——MFCC 论文。
- [Stevens, Volkmann, Newman (1937). A Scale for the Measurement of the Psychological Magnitude Pitch](https://pubs.aip.org/asa/jasa/article-abstract/8/3/185/735757/) — the original mel scale.
  Stevens、Volkmann、Newman (1937)——心理音高量级的测量尺度——原始 mel 尺度。
- [OpenAI — Whisper source, log_mel_spectrogram](https://github.com/openai/whisper/blob/main/whisper/audio.py) — read the reference implementation.
  OpenAI——Whisper 源码，log_mel_spectrogram——阅读参考实现。
- [librosa feature extraction docs](https://librosa.org/doc/main/feature.html) — reference for `mfcc`, `melspectrogram`, and hop/window.
  librosa 特征提取文档——`mfcc`、`melspectrogram` 和 hop/window 的参考。
- [NVIDIA NeMo — audio preprocessing](https://docs.nvidia.com/deeplearning/nemo/user-guide/docs/en/main/asr/asr_all.html#featurizers) — production-scale pipeline for Parakeet + Canary models.
  NVIDIA NeMo——音频预处理——Parakeet + Canary 模型的生产级流水线。

> **【中文解读】** 延伸阅读提供了深入学习的高质量资源，包括论文、教程和工具。建议按需选读，优先阅读标注为 "the critical read" 的核心论文。

