# 频谱图,Mel尺度和音频特征

> 网络不用好使用原始波形.它们用光谱.它们用光谱更好. 2026年每一个ASR,TTS和音频分类器都会因这个单一的预处理选择而活着或死亡.

> **【中文解读】**神经网络处理原始波形效果不好,但处理频谱图效果好,处理 Mel 频谱图效果更好――2026年所有ASR、TTS 和音频分类器的成功取决于这个预处理选择――Mel 尺度模拟人耳对频率的感知(低频精细、高频粗略) ――

> **【拓展：Mel 频谱图是音频 AI 的 "图像"】**频谱图将音频转换为2D图像(时间×频率),可用CNN/ViT处理──语、音乐Gen、稳定音频都使用 Mel 频谱图作为中间表示──

**Type:** Build | **类型:** 构建
**Languages:** Python | **语言:** Python
**Prerequisites:** Phase 6 · 01 (Audio Fundamentals) | **前置知识:** 阶段 6 · 01（音频基础）
**Time:** ~45 minutes | **预计用时:** ~45 分钟

## 问题 问题引入

拍摄10秒16千克Hz的剪辑,这相当于16万次,全部在`[-1, 1]`几乎完全不与标签"狗吠叫"或"猫"相关.原始波形有信息,但模型无法轻松提取. 100 ms 的距离之间讲述的两个相同音符完全不同原始样本.

> 拿一段10秒的16千克音频.`[-1, 1]`范围,几乎与标签"狗叫"或"单词猫"完全不相关.

> **【中文解读】**本节提出的问题是:如何在实际工程中正确理解和应用这一技术――理解问题背景有助于把握技术选择的关键决策点――在实际人工智能系统中,错误的技术选择往往比实现细节的错误成本更高――

频谱图解决了这一问题.它将人类感知忽视的时间细节 (微秒的) 崩,并保留了感知参与的结构 (这些频率是能量,在时间窗口中是1025ms).

> 频谱图解决了这个问题. 它缩小了人类感知忽略的时间细节 (微秒级动),保留了感知关注的结构 (在约1025ms的时间窗口内,哪些频率有能量)

梅尔谱程进一步推进.人类以逻辑方式感知音速:100Hz与200Hz的声音与1000Hz与2000Hz的距离相同.梅尔谱程扭曲频率轴以匹配.梅尔谱程是2010年至2026年语音ML中最重要的单一特征.

> 频谱图进一步.人类对高音频的感知是对数:100 Hz 与 200 Hz 听起来和1000 Hz 与 2000 Hz "距离一样远"的感知.

## 概念的核心概念

> **【中文解读】**本节介绍核心概念和理论基础.掌握这些概念是后续动手实现的前提,同时也是面试和工程实践中高频考察的知识点.


![Waveform to STFT to mel spectrogram to MFCC ladder](../assets/mel-features.svg)

**STFT (Short-Time Fourier Transform).**切割波形成重叠的框架 (典型:25 ms窗口,10 ms跳 = 400 样本 / 16 样本在 16 kHz).乘以窗口函数 (汉是默认的; Hamming 略有不同的交易).FFT 每个框架.堆积大小谱到一个形状矩阵`(n_frames, n_freq_bins)`这是你的光谱.

> **STFT（短时傅里叶变换）。**将波形切成重叠的(典型:25 ms 窗口,10 ms 步长=16 kHz 下400 采样点 / 160 采样点) ⋅每乘以窗口函数(默认 Hann;Hamming 略有不同) ⋅对每做 FFT。将幅度谱堆叠成`(n_frames, n_freq_bins)`这就是你的频谱图.

**Log-magnitude.**度范围为5至6个级别.`log(|X| + 1e-6)`或`20 * log10(|X|)`每个生产管道都使用日志大小,而不是原始大小.

> **对数幅度。**原始幅度跨5-6个数量级.`log(|X| + 1e-6)`或`20 * log10(|X|)`压缩动态范围――每一个生产流线都使用数量幅度而不是原始幅度――

**Mel scale.**频率`f`在Hz地图中到MEL`m`通过`m = 2595 * log10(1 + f / 700)`图表大致是线性低于1kHz,大致是高于高数. 80 melbin覆盖08kHz是标准ASR输入.

> **Mel 尺度。**频率`f`映射到我`m`的公式为`m = 2595 * log10(1 + f / 700)`◎该映射在1kHz以下大致线性,以上大致对数量──覆盖08kHz的80个 melbin是标准ASR输入──

**Mel filterbank.**单个选器是单个选器,一个选器是单个选器,一个选器是单个选器.一个选器的选器是单个选器.一个选器的选器是单个选器.一个选器的选器是单个选器.一个选器是单个选器.一个选器是单个选器.一个选器是单个选器.一个选器是单个选器.一个选器是单个选器.一个选器是单个选器.一个选器是单个选器.一个选器是单个选器.

> **Mel 滤波器组。**一组在旋尺度上等间距排列的三角波器──每波器是相邻的FTbin的加权和──将STFT幅乘以波器组矩阵即可通过一次矩阵乘法得到旋频谱图──

**Log-mel spectrogram.** `log(mel_spec + 1e-10)`声输入,子输入,无M4T输入,通用2026音频前端.

> **对数 Mel 频谱图。** `log(mel_spec + 1e-10)`〔语的输入〕子的输入──无M4T的输入──2026年通用音频前端──

**MFCCs.**采用日志谱,应用DCT (II类),保留第13个系数. 调节特征并进一步压缩. 在2015年左右,CNN/变压器在原始日志中被捕获.仍然用于扬声器识别 (x向量,ECAPA).

> **MFCC。**取对数 Mel 频谱图,应用 DCT(类 II),保留前 13 个系数――除特征间相关性并进一步缩小――2015年之前的主流特征,之后CNN/Transformer 在原始日志上追上――仍然用于说话人识别(x-向量、ECAPA) ――

**Resolution trade.**较大的FFT =更好的频率分辨率,但更糟糕的时间分辨率. 25 ms / 10 ms是音频-ML默认; 50 ms / 12.5 ms为音乐; 5 ms / 2 ms为过渡检测 (鼓击,音).

> **分辨率权衡。**更大的FFT = 更好的频率分辨率但更差的时间分辨率──25 ms / 10 ms 是音频ML的默认值;50 ms / 12.5 ms 用于音乐;5 ms / 2 ms 用于瞬态检测(鼓击、爆音)──

> **【拓展：语音 AI 的产品化】**语音技术在产品化中面临着独特的挑战:不同口音,背景噪音,远场拾音,多人说话等.

> **【拓展：多语言语音技术】**全球语言的语音特性差异巨大:声调语言的音高携带语义,低资源语言缺乏训练数据――Meta的MMS模型支持1000多种语言的语音识别,语在多语言场景表现出色,但仍然需要针对特定语言微调――



## 建立它,实现它.

> **【中文解读】**本节通过代码实现从零到核心算法――这种"从零开始"的方式可以帮助理解框架背后的原理,遇到问题时不会被黑盒困住――

```figure
spectrogram-window
```

## 建立它

### 步骤1:成波形

```python
def frame(signal, frame_len, hop):
    n = 1 + (len(signal) - frame_len) // hop
    return [signal[i * hop : i * hop + frame_len] for i in range(n)]
```

通过10秒16kHz的剪辑`frame_len=400, hop=160`结果是998个.

> 一段 10 秒 16 kHz 的音频,使用 `frame_len=400, hop=160`得到了998个.

### 步骤2:汉窗

```python
import math

def hann(N):
    return [0.5 * (1 - math.cos(2 * math.pi * n / (N - 1))) for n in range(N)]
```

在FFT之前乘以元素智能. 消除在非零的终点中切断造成的光谱泄漏.

> 在FFT之前,逐元素相乘.消除导致非零端点处截断的频谱泄漏.

### 步骤3:STFT大小

```python
def stft_magnitude(signal, frame_len=400, hop=160):
    win = hann(frame_len)
    frames = frame(signal, frame_len, hop)
    return [magnitudes(dft([w * s for w, s in zip(win, f)])) for f in frames]
```

生产用途`torch.stft`或`librosa.stft`循环是教学性的,它在短片中运行.`code/main.py`现在,我们要去.

> 生产环境使用`torch.stft`或`librosa.stft`循环是教学目的,它在`code/main.py`中处理短音频片段──

### 步骤4:mel过银行

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

频率为 80 mels 覆盖08 kHz`n_fft=400`给了一个`(80, 201)`乘以一个矩阵.`(n_frames, 201)`转移值的STFT大小`(n_frames, 80)`光谱.

> 覆盖08kHz的80个旋律波器,`n_fft=400`得到了`(80, 201)`矩阵――将`(n_frames, 201)`转换的 STFT 幅度乘以转换得到`(n_frames, 80)`们的故事.

### 步骤5: 记录

```python
def log_mel(mel_spec, eps=1e-10):
    return [[math.log(max(v, eps)) for v in frame] for frame in mel_spec]
```

共同的替代方案:`librosa.power_to_db`(参考标准化 dB),`10 * log10(power + eps)`语使用更有参与的剪辑 +正常化例程 (见语的图)`log_mel_spectrogram`)

> 常见替代方案:`librosa.power_to_db`(引用归化 dB)`10 * log10(power + eps)`◎ 语 使用更复杂的剪裁 + 归一化流程`log_mel_spectrogram`

### 步骤 6: 金融金融机构

```python
def dct_ii(x, n_coeffs):
    N = len(x)
    return [
        sum(x[n] * math.cos(math.pi * k * (2 * n + 1) / (2 * N)) for n in range(N))
        for k in range(n_coeffs)
    ]
```

> **【中文解读】**本节展示了如何使用成熟框架 (如PyTorch、HuggingFace等) 快速应用该技术.


按DCT对每一个日志格,保持第13个系数.这是你的MFCC矩阵.第一个系数通常会下降 (它编码总能量).

> 对于每个日志应用DCT,保留前13个系数――这就是你的MFCC矩阵――第一个系数通常被丢弃.




> **【拓展：语音与情感计算】**语音不仅传递文字信息,还携带丰富的情感信号 (语调、语速、音高变化) 情感语音识别 (语音识别,语音情感识别,SER) 在客服质检,心理健康监测,智能教育等领域广泛应用.

## 用它实现框架

现在,我们要做什么?

> 2026 年技术:

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

指规则:**if you are not working on music, start with 80 log-mels.**证明的责任是任何偏差.

> 经验法则:**如果你不是在做音乐，就从 80 log-mels 开始。**任何偏离都需要证明其合理性.



## 陷在2026年仍存在

> 2026年仍在犯案陷中

- **Mel count mismatch.**训练80米,推断128米,沉默失败,记录两端的特征形状.
  **Mel 数量不匹配。**训练用80米,推理用128米――静默失败――在两端记录特征形状――
- **Sample-rate mismatch upstream.**在22.05kHz计算的Mels看起来与16kHz不同.
  **上游采样率不匹配。**计算的速度与16kHz的不同.
- **dB vs log.**微信预计记录,而不是 dB-mel. 有些HF管道会自动检测,但你的定制代码不会.
  **dB 与 log。**微笑 期望日志- 标签而不是 dB- 标签――某些 HF 流水线会自动检测;你的自定义代码不会――
- **Normalization drift.**训练期间的每次发出正常化,推断期间的全球正常化.
  **归一化漂移。**训练时逐句归结,推理时全局归结.
- **Leakage from padding.**片的末端以零制,在后面的框架中产生平面光谱.
  **填充泄漏。**对于音频片段末尾零填充会在尾部产生平坦频谱──使用对称填充或复制填充──

> **【中文解读】**本节关注如何将模型部署为可用的产品. 从原型到生产级系统需要考虑性能优化,错误处理,监控等多个维度.


## 运送它.

保存如`outputs/skill-feature-extractor.md`技能选择特征类型,数量,框架/跳,和规范化给定的模型目标.

> 保存为`outputs/skill-feature-extractor.md`△该技能为给定模型目标选择特征类型,数量,步长和归结方式.

## 练习题

1. **Easy.**跑步`code/main.py`通过选,将每一个图片的 argmax melbin 打印出来.
   **简单。**运行`code/main.py`△它合成一个信号 (频率从200 扫到4000 Hz) 并打印每的 argmax mel bin──图图.
2. **Medium.**再运行`n_mels`在`{40, 80, 128}`其他`frame_len`在`{200, 400, 800}`时间轴上,测量尖峰带宽. 什么组合能解决声最好?
   **中等。**用`n_mels`为`{40, 80, 128}`和 `frame_len`为`{200, 400, 800}`重新运行. 沿时间轴测量峰带宽.
3. **Hard.**实施`power_to_db`通过使用 (a) 原始日志-mail, (b) dB-mel 进行对比,`ref=max`报告前一级准确性.
   **困难。**实现`power_to_db`通过微型CNN 分类器比较 (a) 原始日志-邮件、(b)`ref=max`报告前一准确率──

> **【中文解读】**在团队协作中,统一术语定义可以避免大量沟通误解.


## 关键词 快速查找表

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

> **【中文解读】**延伸阅读提供了深入学习的高质量资源. 这些论文和教程是该领域的经典参考文献,适合需要深入了解的读者.


## 继续阅读 继续阅读

- [Davis, Mermelstein (1980). Comparison of parametric representations for monosyllabic word recognition](https://ieeexplore.ieee.org/document/1163420) 国际金融委员会论文.
  戴维斯·默默尔斯坦 (1980) 单音节词识别的参数化表示比较MFCC论文──
- [Stevens, Volkmann, Newman (1937). A Scale for the Measurement of the Psychological Magnitude Pitch](https://pubs.aip.org/asa/jasa/article-abstract/8/3/185/735757/)原始的MEL尺度.
  史蒂文斯·沃克曼·纽曼 (1937) 心理音高量级的测量尺度
- [OpenAI — Whisper source, log_mel_spectrogram](https://github.com/openai/whisper/blob/main/whisper/audio.py)阅读参考实施.
  开启AI 语源码,log_mel_spectrogram阅读参考实现──
- [librosa feature extraction docs](https://librosa.org/doc/main/feature.html)参考`mfcc`现在`melspectrogram`跳/窗户.
  图书馆 特征提取文档`mfcc`,我知道.`melspectrogram`和跳/窗口的参考
- [NVIDIA NeMo — audio preprocessing](https://docs.nvidia.com/deeplearning/nemo/user-guide/docs/en/main/asr/asr_all.html#featurizers)生产规模的管道,用于Parakeet+加拿大车型.
  百度影音预处理 鱼 + 卡纳里 模型的生产级流水线。

> **【中文解读】**延伸阅读提供了深入学习的高质量资源,包括论文,教程和工具.

