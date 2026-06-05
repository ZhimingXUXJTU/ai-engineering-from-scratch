# Neural Audio Codecs — EnCodec, SNAC, Mimi, DAC and the Semantic-Acoustic Split | 神经音频编解码器

> 2026 audio generation is almost all tokens. EnCodec, SNAC, Mimi, and DAC turn continuous waveforms into discrete sequences that a transformer can predict. The semantic-vs-acoustic token split — first-codebook as semantic, rest as acoustic — is the most important architectural shift since the Transformer for audio.

> **【中文解读】** 2026 年的音频生成几乎都基于 token。EnCodec、SNAC、Mimi、DAC 将连续波形转换为离散序列，让 Transformer 可以预测。语义-声学 token 分离（第一个码本=语义，其余=声学）是自 Transformer 以来音频领域最重要的架构变革。

> **【拓展：音频 token 化】** 就像文本有 BPE tokenizer 将文字变成 token，音频有 EnCodec 等编解码器将声波变成 token。这使得音频可以像文本一样被大语言模型处理。Moshi、AudioLM 等模型都依赖这种 token 化。

**Type:** Learn | **类型:** 学习
**Languages:** Python | **语言:** Python
**Prerequisites:** Phase 6 · 02 (Spectrograms), Phase 10 · 11 (Quantization), Phase 5 · 19 (Subword Tokenization) | **前置知识:** 阶段 6 · 02（频谱图），阶段 10 · 11（量化），阶段 5 · 19（子词分词）
**Time:** ~60 minutes | **预计用时:** ~60 分钟

## The Problem | 问题引入

Language models work on discrete tokens. Audio is continuous. If you want an LLM-style model for speech / music — MusicGen, Moshi, Sesame CSM, VibeVoice, Orpheus — you first need a **neural audio codec**: a learned encoder that discretizes audio into a small vocabulary of tokens, and a matching decoder that reconstructs the waveform.

> 语言模型处理离散 token。音频是连续的。如果你想为语音/音乐构建 LLM 风格的模型——MusicGen、Moshi、Sesame CSM、VibeVoice、Orpheus——你首先需要一个**神经音频编解码器**：一个学习编码器将音频离散化为小词表 token，加上匹配的解码器重建波形。

> **【中文解读】** 本节提出的问题是：如何在实际工程中正确理解和应用这一技术。理解问题背景有助于把握技术选型的关键决策点。在实际 AI 系统中，错误的技术选型往往比实现细节的 bug 代价更高。

Two families have emerged:

> 两个家族已经出现：

1. **Reconstruction-first codecs** — EnCodec, DAC. Optimize perceptual audio quality. Tokens are "acoustic" — they capture everything including speaker identity, timbre, background noise.
   **重建优先编解码器**——EnCodec、DAC。优化感知音频质量。Token 是"声学的"——它们捕获一切，包括说话人身份、音色、背景噪声。
2. **Semantic-first codecs** — Mimi (Kyutai), SpeechTokenizer. Force the first codebook to encode linguistic / phonetic content (often by distilling from WavLM). Subsequent codebooks are acoustic detail.
   **语义优先编解码器**——Mimi（Kyutai）、SpeechTokenizer。强制第一个码本编码语言/语音内容（通常通过从 WavLM 蒸馏）。后续码本是声学细节。

The 2024-2026 insight: **a pure reconstruction codec gives you blurry speech when you try to generate from text.** The LLM over codec tokens has to learn both language structure AND acoustic structure in the same codebook, which doesn't scale. Separating them — semantic codebook 0, acoustic codebooks 1-N — is what makes Moshi and Sesame CSM work.

> 2024-2026 年的洞察：**纯重建编解码器在从文本生成时给你模糊的语音。** 编解码 token 上的 LLM 必须在同一个码本中同时学习语言结构和声学结构，这无法扩展。将它们分离——语义码本 0，声学码本 1-N——正是 Moshi 和 Sesame CSM 成功的关键。

## The Concept | 核心概念

> **【中文解读】** 本节介绍核心概念和理论基础。掌握这些概念是后续动手实现的前提，同时也是面试和工程实践中高频考察的知识点。


![Four codec landscape: EnCodec, DAC, SNAC (multi-scale), Mimi (semantic+acoustic)](../assets/codec-comparison.svg)

### The core trick: Residual Vector Quantization (RVQ)

Rather than one big codebook (which would need millions of codes for good quality), all modern audio codecs use **RVQ**: a cascade of small codebooks. The first codebook quantizes the encoder output; the second quantizes the residual; etc. Each codebook is 1024 codes. 8 codebooks = effective vocabulary of 1024^8 = 10^24.

At inference time, the decoder sums all chosen codes per frame to reconstruct.

### The four codecs that matter in 2026

**EnCodec (Meta, 2022).** The baseline. Encoder-decoder over waveform, RVQ bottleneck. 24 kHz, 32 codebooks possible, default 4 codebooks @ 1.5 kbps. Uses `1D conv + transformer + 1D conv` architecture. Used by MusicGen.

**DAC (Descript, 2023).** RVQ with L2-normalized codebooks, periodic activation functions, improved losses. Highest reconstruction fidelity of any open codec — sometimes indistinguishable from original speech with 12 codebooks. 44.1 kHz full-band.

**SNAC (Hubert Siuzdak, 2024).** Multi-scale RVQ — the coarse codebooks operate at a lower frame rate than fine ones. Effectively models audio hierarchically: a coarse "sketch" at ~12 Hz plus detail at 50 Hz. Used by Orpheus-3B because the hierarchical structure maps well onto LM-based generation.

**Mimi (Kyutai, 2024).** The 2026 game-changer. 12.5 Hz frame rate (extremely low), 8 codebooks @ 4.4 kbps. Codebook 0 is **distilled from WavLM** — trained to predict WavLM's speech-content features. Codebooks 1-7 are acoustic residuals. This split powers Moshi (Lesson 15) and Sesame CSM.

### Frame rates matter for language modeling

Lower frame rate = shorter sequence = faster LM.

| Codec | Frame rate | 1 s = N frames | Good for |
|-------|-----------|----------------|---------|
| EnCodec-24k | 75 Hz | 75 | music, general audio |
| DAC-44.1k | 86 Hz | 86 | high-fidelity music |
| SNAC-24k (coarse) | ~12 Hz | 12 | AR-LM efficient |
| Mimi | 12.5 Hz | 12.5 | streaming speech |

| 编解码器 | 帧率 | 1 秒 = N 帧 | 适用场景 |
|---------|------|------------|---------|
| EnCodec-24k | 75 Hz | 75 | 音乐、通用音频 |
| DAC-44.1k | 86 Hz | 86 | 高保真音乐 |
| SNAC-24k（粗） | ~12 Hz | 12 | AR-LM 高效 |
| Mimi | 12.5 Hz | 12.5 | 流式语音 |

At 12.5 Hz, a 10-second utterance is only 125 codec frames — a transformer can easily predict them.

### Semantic vs acoustic tokens

```
frame_t → [semantic_token_t, acoustic_token_0_t, acoustic_token_1_t, ..., acoustic_token_6_t]
```

- **Semantic token (codebook 0 in Mimi).** Encodes what was said — phonemes, words, content. Distilled from WavLM via an auxiliary prediction loss.
- **Acoustic tokens (codebooks 1-7).** Encode timbre, speaker identity, prosody, background noise, fine detail.

An AR LM predicts the semantic token first (conditioned on text), then predicts acoustic tokens (conditioned on semantic + speaker reference). This factorization is why modern TTS can zero-shot-clone voices: the semantic model handles content; the acoustic model handles timbre.

### 2026 reconstruction quality (bits per sec, lower bitrate is better)

| Codec | Bitrate | PESQ | ViSQOL |
|-------|---------|------|--------|
| Opus-20kbps | 20 kbps | 4.0 | 4.3 |
| EnCodec-6kbps | 6 kbps | 3.2 | 3.8 |
| DAC-6kbps | 6 kbps | 3.5 | 4.0 |
| SNAC-3kbps | 3 kbps | 3.3 | 3.8 |
| Mimi-4.4kbps | 4.4 kbps | 3.1 | 3.7 |

| 编解码器 | 比特率 | PESQ | ViSQOL |
|---------|--------|------|--------|
| Opus-20kbps | 20 kbps | 4.0 | 4.3 |
| EnCodec-6kbps | 6 kbps | 3.2 | 3.8 |
| DAC-6kbps | 6 kbps | 3.5 | 4.0 |
| SNAC-3kbps | 3 kbps | 3.3 | 3.8 |
| Mimi-4.4kbps | 4.4 kbps | 3.1 | 3.7 |

Traditional codecs like Opus still win per bit on perceptual quality. Neural codecs win on **discrete tokens** (which Opus does not produce) and **generative-model quality** (what the LM can do with those tokens).

> **【拓展：语音 AI 的产品化】** 语音技术在产品化中面临独特挑战：不同口音、背景噪声、远场拾音、多人说话等。Siri、Alexa、小爱同学等产品都投入了大量工程优化来解决这些 "长尾问题"。实时性要求（<300ms 延迟）也是语音产品的核心指标。

> **【拓展：多语言语音技术】** 全球语言的语音特性差异巨大：声调语言（如中文）的音高携带语义，低资源语言缺乏训练数据。Meta 的 MMS 模型支持 1000+ 种语言的语音识别，Whisper 在多语言场景表现出色，但仍需针对特定语言微调。



## Build It | 动手实现

> **【中文解读】** 本节通过代码从零实现核心算法。这种 "from scratch" 的方式能帮助理解框架背后的原理，遇到问题时不会被黑盒困住。


### Step 1: encode with EnCodec

```python
from encodec import EncodecModel
import torch

model = EncodecModel.encodec_model_24khz()
model.set_target_bandwidth(6.0)  # kbps

wav = torch.randn(1, 1, 24000)
with torch.no_grad():
    encoded = model.encode(wav)
codes, scale = encoded[0]
# codes: (1, n_codebooks, n_frames), dtype=int64
```

`n_codebooks=8` at 6 kbps. Each code is 0-1023 (10-bit).

### Step 2: decode and measure reconstruction

```python
with torch.no_grad():
    wav_recon = model.decode([(codes, scale)])

from torchaudio.functional import compute_deltas
import torch.nn.functional as F

mse = F.mse_loss(wav_recon[:, :, :wav.shape[-1]], wav).item()
```

### Step 3: the semantic-acoustic split (Mimi-style)

```python
from moshi.models import loaders
mimi = loaders.get_mimi()

with torch.no_grad():
    codes = mimi.encode(wav)  # shape (1, 8, frames@12.5Hz)

semantic = codes[:, 0]
acoustic = codes[:, 1:]
```

Semantic codebook 0 is WavLM-aligned. You can train a text-to-semantic transformer — much smaller vocabulary than going direct-to-audio. Then a separate acoustic-to-waveform decoder conditions on a speaker reference.

### Step 4: why AR LM over codec tokens works

For a 10 s speech clip at Mimi's 12.5 Hz × 8 codebooks:

```
N_tokens = 10 * 12.5 * 8 = 1000 tokens
```

> **【中文解读】** 本节展示如何用成熟框架（如 PyTorch、HuggingFace 等）快速应用该技术。在实际项目中，优先使用经过验证的框架实现，可以减少 bug 并提高开发效率。


1000 tokens is a trivial context for a transformer. A 256M-parameter transformer can generate 10 seconds of speech in milliseconds on a modern GPU.




> **【拓展：语音与情感计算】** 语音不仅传递文字信息，还携带丰富的情感信号（语调、语速、音高变化）。情感语音识别（Speech Emotion Recognition, SER）在客服质检、心理健康监测、智能教育等领域有广泛应用。当前 SOTA 模型通常基于 wav2vec 2.0 或 HuBERT 等预训练模型微调。

## Use It | 用框架实现

Map problem → codec:

| Task | Codec |
|------|-------|
| General music generation | EnCodec-24k |
| Highest-fidelity reconstruction | DAC-44.1k |
| AR LM over speech (TTS) | SNAC or Mimi |
| Streaming full-duplex speech | Mimi (12.5 Hz) |
| Sound-effect library with text | EnCodec + T5 condition |
| Fine-grained audio editing | DAC + inpainting |

| 任务 | 编解码器 |
|------|---------|
| 通用音乐生成 | EnCodec-24k |
| 最高保真重建 | DAC-44.1k |
| 语音上的 AR LM（TTS） | SNAC 或 Mimi |
| 流式全双工语音 | Mimi（12.5 Hz） |
| 文本驱动的音效库 | EnCodec + T5 条件 |
| 细粒度音频编辑 | DAC + 内画 |

Rule of thumb: **if you're building a generative model, start with Mimi or SNAC. If you're building a compression pipeline, use Opus.**



## Pitfalls

- **Too many codebooks.** Adding codebooks increases fidelity linearly but LM sequence length linearly too. Stop at 8-12.
- **Frame-rate mismatch.** Training LM on 12.5 Hz Mimi then fine-tuning on 50 Hz EnCodec fails silently.
- **Assuming all codebooks equal.** In Mimi, codebook 0 carries content; losing it destroys intelligibility. Losing codebook 7 is barely noticeable.
- **Using reconstruction quality as the only metric.** A codec can have great reconstruction but be useless for LM-based generation if the semantic structure is bad.

> **【中文解读】** 本节关注如何将模型部署为可用的产品。从原型到生产级系统需要考虑性能优化、错误处理、监控等多个维度。


## Ship It | 产出物

Save as `outputs/skill-codec-picker.md`. Pick a codec for a given generative or compression task.

> 保存为 `outputs/skill-codec-picker.md`。为给定的生成或压缩任务选择编解码器。

## Exercises | 练习题

1. **Easy.** Run `code/main.py`. It implements a toy scalar + residual quantizer and measures reconstruction error as you add codebooks.
   **简单。** 运行 `code/main.py`。它实现了一个玩具标量 + 残差量化器，测量随着码本增加的重建误差。
2. **Medium.** Install `encodec` and compare 1, 4, 8, 32 codebooks on a held-out speech clip. Plot PESQ or MSE vs bitrate.
   **中等。** 安装 `encodec`，在留出语音片段上比较 1、4、8、32 个码本。绘制 PESQ 或 MSE vs 比特率。
3. **Hard.** Load Mimi. Encode a clip. Replace codebook 0 with random integers; decode. Then replace codebook 7 similarly. Compare the two corruptions — codebook 0 corruption should destroy intelligibility; codebook 7 corruption should barely change anything.
   **困难。** 加载 Mimi。编码一段音频。用随机整数替换码本 0；解码。然后类似地替换码本 7。比较两种损坏——码本 0 损坏应破坏可懂度；码本 7 损坏几乎无变化。

> **【中文解读】** 术语表中的 "What people say" vs "What it actually means" 区分了日常口语和精确技术含义。在团队协作中，统一术语定义可以避免大量沟通误解。


## Key Terms | 术语速查表

| Term | What people say | What it actually means |
|------|-----------------|-----------------------|
| RVQ | Residual quantization | Cascade of small codebooks; each quantizes the previous residual. |
| Frame rate | Codec speed | How many token-frames per second. Lower = faster LM. |
| Semantic codebook | Codebook 0 (Mimi) | Codebook distilled from SSL features; encodes content. |
| Acoustic codebooks | Everything else | Timbre, prosody, noise, fine detail. |
| PESQ / ViSQOL | Perceptual quality | Objective metrics correlating with MOS. |
| EnCodec | Meta codec | The RVQ baseline; used by MusicGen. |
| Mimi | Kyutai codec | 12.5 Hz frame rate; semantic-acoustic split; powers Moshi. |

| 术语 | 人们常说的 | 实际含义 |
|------|-----------|---------|
| RVQ | 残差量化 | 小码本级联；每个量化前一个残差。 |
| 帧率 | 编解码器速度 | 每秒多少 token 帧。越低 = LM 越快。 |
| 语义码本 | 码本 0（Mimi） | 从 SSL 特征蒸馏的码本；编码内容。 |
| 声学码本 | 其余所有 | 音色、韵律、噪声、精细细节。 |
| PESQ / ViSQOL | 感知质量 | 与 MOS 相关的客观指标。 |
| EnCodec | Meta 编解码器 | RVQ 基线；MusicGen 使用。 |
| Mimi | Kyutai 编解码器 | 12.5 Hz 帧率；语义-声学分离；驱动 Moshi。 |

> **【中文解读】** 延伸阅读提供了深入学习的高质量资源。这些论文和教程是该领域的经典参考文献，适合需要深入理解的读者。


## Further Reading | 延伸阅读

- [Défossez et al. (2023). EnCodec](https://arxiv.org/abs/2210.13438) — the RVQ baseline.
  Défossez 等 (2023). EnCodec——RVQ 基线。
- [Kumar et al. (2023). Descript Audio Codec (DAC)](https://arxiv.org/abs/2306.06546) — highest-fidelity open.
  Kumar 等 (2023). DAC——最高保真开源编解码器。
- [Siuzdak (2024). SNAC](https://arxiv.org/abs/2410.14411) — multi-scale RVQ.
  Siuzdak (2024). SNAC——多尺度 RVQ。
- [Kyutai (2024). Mimi codec](https://kyutai.org/codec-explainer) — semantic-acoustic split, WavLM distillation.
  Kyutai (2024). Mimi 编解码器——语义-声学分离，WavLM 蒸馏。
- [Borsos et al. (2023). AudioLM](https://arxiv.org/abs/2209.03143) — the two-stage semantic/acoustic paradigm.
  Borsos 等 (2023). AudioLM——两阶段语义/声学范式。
- [Zeghidour et al. (2021). SoundStream](https://arxiv.org/abs/2107.03312) — the original streamable RVQ codec.
  Zeghidour 等 (2021). SoundStream——原始可流式 RVQ 编解码器。

> **【中文解读】** 延伸阅读提供了深入学习的高质量资源，包括论文、教程和工具。建议按需选读，优先阅读标注为 "the critical read" 的核心论文。

