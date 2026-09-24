# 音频基础 波形采样与里叶变化

> 波形是原始信号.谱谱是表示.MEL特征是ML友好的形式.每一个现代ASR和TTS管道都走在这个梯子上,第一步是理解采样和Fourier.

> **【中文解读】**波形是原始信号,频谱图是表示形式,Mel特征是机器学习的友好的形式――每个现代语音识别(ASR) 和语音合成(TTS) 系统都沿着这个阶段上升:波形 → 频谱图 → Mel特征――第一阶段就是理解采样和里叶变化――

> **【拓展：音频 AI 的基础】**采样率 (如16kHz) 决定了可表示的最高频率 (如16kHz) 里叶变化将时域信号分解为频域成分.

**Type:** Learn | **类型:** 学习
**Languages:** Python | **语言:** Python
**Prerequisites:** Phase 1 · 06 (Vectors & Matrices), Phase 1 · 14 (Probability Distributions) | **前置知识:** 阶段 1 · 06（向量与矩阵），阶段 1 · 14（概率分布）
**Time:** ~45 minutes | **预计用时:** ~45 分钟

## 问题 问题引入

电话产生压力与时间信号.你的神经网络消耗了器.它们之间有堆积的规则,如果被违反,会产生沉默的错误:模型运行得很好,但WER翻倍,或者TTS发出声,或者语音克隆系统记忆起电话而不是扬声器.

> 麦克风产生压力时间信号――你的神经网络消费是张量――两者之间有一堆约定违反这些约定会产生隐性错误:模型训练正常但 WER 翻倍,或者 TTS 输出声,或者语音克隆系统记住麦克风而不是说话人――

> **【中文解读】**本节提出的问题是:如何在实际工程中正确理解和应用这一技术――理解问题背景有助于把握技术选择的关键决策点――在实际人工智能系统中,错误的技术选择往往比实现细节的错误成本更高――

语音系统中的每一个错误都追溯到三个问题之一:

> 语音系统中的每个 bug 都可以追溯到以下三个问题之一:

1. 数据记录的样本率是多少,模型预期什么?
   数据的录制采样率是多少,模型预期的采样率是多少?
2. 信号是个别名吗?
   信号是否存在混?
3. 你是用原始样本或频率表示操作?
   你处理原始采样点还是频率表示?

错误的,甚至是声大型v4也会产生垃圾.

> 搞错了,即使是Whisper-Large-v4也会输出垃圾.

## 概念的核心概念

> **【中文解读】**本节介绍核心概念和理论基础.掌握这些概念是后续动手实现的前提,同时也是面试和工程实践中高频考察的知识点.


![Waveform, sampling, DFT, and frequency bins visualized](../assets/audio-fundamentals.svg)

**Waveform.**的一个维度的浮动阵列`[-1.0, 1.0]`为了将其转换为秒,按样本速率划分:`t = n / sr`十秒钟的 16 kHz 剪辑是 160,000 个浮动的阵列.

> **波形（Waveform）。**一个取值在`[-1.0, 1.0]`之间的一个维浮点数组.以采样编号为索引.`t = n / sr`一段10秒的16kHz音频是16万个浮点数组.

**Sampling rate (sr).**2026年常见率:

> **采样率（sr）。**每秒采样点数量,2026年常用采样率:

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

**Nyquist-Shannon.**样本率`sr`能明确表示高达 `sr/2`现在,我们要去.`sr/2`边界是尼奎斯特频率. 尼奎斯特上方的能量被*aliased* 折叠到较低频率,并破坏信号.

> **奈奎斯特-香农定理。**采样率`sr`可以无歧义地表示最高到`sr/2`频率:`sr/2`边界就是奈奎斯特频率的超过奈奎斯特的能量会被叠加到更低的频率从而破坏信号――降采前必先进行低通波――

**Bit depth.**16位PCM (签名int16,范围±32,767) 是通用交换格式. 24位为音乐, 32位为内部DSP.`soundfile`读 int16,但在 显示 float32 阵列中`[-1, 1]`现在,我们要去.

> **位深度。**16位PCM(有符号 int16,范围±32,767) 是通用交换格式──音乐用24位,内部DSP用32位浮点──`soundfile`等库读取16但回来`[-1, 1]`范围的浮动32 数组――

**Fourier Transform.**任何有限的信号是不同频率的突体的总和.`N`样本`N`复杂系数 每频段一个. `bin k`频率地图`k · sr / N`度是频率的宽度,角度是相.

> **傅里叶变换。**任何有限信号都可以分为不同频率的正弦波之和──离散里叶变换 (DFT) 对`N`个样点计算`N`个复数系数每频率的一个.`bin k`对应频率`k · sr / N`幅度是该频率的振幅,角是相位.

**FFT.**快速福利尔转换:一个`O(N log N)`对于DFT的算法`N`每个音频库都使用FFT在罩杯下. 1024样本FFT在16kHz时提供512个可用频段,范围为08kHz在15.6Hz分辨率.

> **FFT。**快速里叶变换:当`N`为了2个时间,DFT的`O(N log N)`算法──每一个音频库底层都使用FFT──16kHz 下1024 采样点的FFT 产生512个可用频率bin,覆盖08kHz,分辨率为15.6Hz──

**Framing + window.**我们不把整个剪辑 FFT. 我们将它切成重叠的 * 框架* (通常是25 ms和10 ms跳),乘以窗口函数 (汉,汉明) 来消除边缘不连续性,然后将每个框 FFT.这是短时间福利尔转换 (STFT).课程02从这里开始.

> **分帧 + 加窗。**我们不对整段音频做FFT──而是将其切成重叠的**(通常25 ms,步长10 ms),每乘以窗函数(Hann、Hamming) 消除边缘不连续性,然后对每做FFT──这就是短时间里叶变化(STFT)──第02课将从这里继续──

> **【拓展：语音 AI 的产品化】**语音技术在产品化中面临着独特的挑战:不同口音,背景噪音,远场拾音,多人说话等.

> **【拓展：多语言语音技术】**全球语言的语音特性差异巨大:声调语言的音高携带语义,低资源语言缺乏训练数据――Meta的MMS模型支持1000多种语言的语音识别,语在多语言场景表现出色,但仍然需要针对特定语言微调――



## 建立它,实现它.

> **【中文解读】**本节通过代码实现从零到核心算法――这种"从零开始"的方式可以帮助理解框架背后的原理,遇到问题时不会被黑盒困住――

```figure
mel-scale
```

## 建立它

### 步骤1:阅读一个剪辑,绘制波形

`code/main.py`仅使用SDLIB`wave`为了保持演示的无依赖性.`soundfile`或`torchaudio.load`(两者都回来了)`(waveform, sr)`双:

> `code/main.py`仅使用标准库的`wave`模块以保持演示无依赖.`soundfile`或`torchaudio.load`(两者都回来了)`(waveform, sr)`元组:

```python
import soundfile as sf
waveform, sr = sf.read("clip.wav", dtype="float32")  # shape (T,), sr=int
```

### 步骤2:从第一原则合成一个鼻波

```python
import math

def sine(freq_hz, sr, seconds, amp=0.5):
    n = int(sr * seconds)
    return [amp * math.sin(2 * math.pi * freq_hz * i / sr) for i in range(n)]
```

按16kHz的440Hz音节 (音乐会A) 速度,在1秒钟内,是16000个浮动.`wave.open(..., "wb")`使用16位PCM编码.

> 采样率下16 kHz 440 Hz 正弦波(标准音 A)持续1秒是16000个浮点数――使用`wave.open(..., "wb")`以16位PCM编码写入.

### 步骤3:手动计算DFT

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

`O(N²)`罚款`N=256`为了确认正确性,对真正的音频无用.`numpy.fft.rfft`或`torch.fft.rfft`现在,我们要去.

> `O(N²)`复杂性`N=256`验证正确性还行,对真实音频没有用──实际代码调用 `numpy.fft.rfft`或`torch.fft.rfft`,我知道.

### 步骤4:找到主导频率

极度峰值指数`k_star`频率地图`k_star * sr / N`运行这个440Hz的阴影应该返回一个峰值`440 * N / sr`现在,我们要去.

> 幅度峰值索引`k_star`对应频率`k_star * sr / N`△对 440 Hz 正弦波运行此函数应在bin `440 * N / sr`处返回峰值.

### 步骤5:证明名

采样一个7kHz的弦在10kHz (Nyquist = 5kHz). 7kHz的音调是在 Nyquist 上,并折叠到`10 − 7 = 3 kHz`子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子

> 以10kHz 采样7kHz 正弦波(奈奎斯特频率 =5kHz) ・7kHz 音调高于奈奎斯特频率,会折叠到`10 − 7 = 3 kHz`△FFT峰值现在3kHz处.这是经典的混叠演示,也是每个DAC/ADC都配备壁式低通波器的原因.

> **【中文解读】**本节展示了如何使用成熟框架 (如PyTorch、HuggingFace等) 快速应用该技术.





> **【拓展：语音与情感计算】**语音不仅传递文字信息,还携带丰富的情感信号 (语调、语速、音高变化) 情感语音识别 (语音识别,语音情感识别,SER) 在客服质检,心理健康监测,智能教育等领域广泛应用.

## 用它实现框架

实际上你将在2026年发送的堆:

> 2026年你实际会使用的技术:

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

> **【中文解读】**本节关注如何将模型部署为可用的产品. 从原型到生产级系统需要考虑性能优化,错误处理,监控等多个维度.


决策规则:**match sample rate before you match anything else**通过44.1千克Hz的立体音频,你会得到像模型 bug 的垃圾.

> 决策规则:**在匹配其他任何东西之前先匹配采样率**语 期望16kHz 单声道浮动32──传入44.1kHz 立体声,你会看起来像模型虫的垃圾输出──

> **【中文解读】**练习题按照易/中/难 三个难度递进;;建议至少完成中级题,Hard级适合深入研究或面试准备;;




## 运送它.

保存如`outputs/skill-audio-loader.md`技术帮助您检查音频输入是否符合下游模型的预期,并且在不符合时,可以正确复制.

> 保存为`outputs/skill-audio-loader.md`△ 应对下游模型的预期,并在不匹配时正确重采样.

## 练习题

1. **Easy.**在16kHz时合成220Hz+440Hz+880Hz的1秒混合.运行DFT.确认预期的垃圾桶的三个峰值.
   **简单。**合成一个220Hz+440Hz+880Hz的1秒混合信号,采样率16kHz──运行 DFT──确认在预期位置有三个峰值──
2. **Medium.**记录你的声音的3秒 WAV48kHz. 下样子到16kHz使用`torchaudio.transforms.Resample`通过每三样子进行简单的十度测量, FFT 两者.
   **中等。**录制一段 3 秒 48 kHz 的语音 WAV──使用 `torchaudio.transforms.Resample`降采采到16kHz,然后用简单抽取(每隔三个样本取一个)降采到16kHz――对两者做FFT――混叠现在出现在哪里?
3. **Hard.**仅使用 创建STFT从零开始`math`图像大小与 图像大小与 图像大小与 图像大小与 图像大小与 图像大小`matplotlib.pyplot.imshow`这是第二课的光谱.
   **困难。**仅用`math`和步骤 3 的 DFT 从零构建 STFT──大小400,步长160,汉窗──用 `matplotlib.pyplot.imshow`绘制幅图. 这就是第02课的频谱图.

> **【中文解读】**在团队协作中,统一术语定义可以避免大量沟通误解.


## 关键词 快速查找表

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

> **【中文解读】**延伸阅读提供了深入学习的高质量资源. 这些论文和教程是该领域的经典参考文献,适合需要深入了解的读者.


## 继续阅读 继续阅读

- [Shannon (1949). Communication in the Presence of Noise](https://people.math.harvard.edu/~ctm/home/text/others/shannon/entropy/entropy.pdf)样本定理背后的论文.
  农 (1949) 带噪音条件下的通信采样定理背后论文
- [Smith — The Scientist and Engineer's Guide to Digital Signal Processing](https://www.dspguide.com/ch8.htm)免费的法典DSP教科书.
  史密斯科学家和工程师数字信号处理指南 免费的经典DSP教材
- [librosa docs — audio primer](https://librosa.org/doc/latest/tutorial.html)实用程序.
  文档音频入门带代码的实践教程.
- [Heinrich Kuttruff — Room Acoustics (6th ed.)](https://www.routledge.com/Room-Acoustics/Kuttruff/p/book/9781482260434)为什么现实世界音频不是一个清洁的阴影.
  哈因里希·库特鲁夫 (Heinrich Kuttruff) 房间声学 (第6版) 解释为什么真世界音频不是干净正弦波的参考书.
- [Steve Eddins — FFT Interpretation notebook](https://blogs.mathworks.com/steve/2020/03/30/fft-spectrum-and-spectral-densities/)频率桶直觉在10分钟内清除了.
  史蒂夫·埃丁斯FFT 解读笔记10分钟搞清频率 的直觉.

> **【中文解读】**延伸阅读提供了深入学习的高质量资源,包括论文,教程和工具.

