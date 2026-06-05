# Text-to-Speech (TTS) — From Tacotron to F5 and Kokoro | 语音合成 — 从 Tacotron 到 F5 和 Kokoro

> ASR inverts speech to text; TTS inverts text to speech. The 2026 stack is three parts: text → tokens, tokens → mel, mel → waveform. Each part has a default model that fits in a laptop.

> **【中文解读】** ASR 把语音变文字，TTS 把文字变语音。2026 年的 TTS 技术栈分三步：文本→token→Mel 频谱→波形。每一步都有可在笔记本上运行的默认模型。

> **【拓展：TTS 的应用】** TTS 是有声书、导航语音、虚拟助手（Siri/小爱同学）、无障碍辅助（为视障人士朗读）的核心技术。零样本 TTS（只需几秒参考音频即可克隆声音）是最新突破。

**Type:** Build | **类型:** 构建
**Languages:** Python | **语言:** Python
**Prerequisites:** Phase 6 · 02 (Spectrograms & Mel), Phase 5 · 09 (Seq2Seq), Phase 7 · 05 (Full Transformer) | **前置知识:** 阶段 6 · 02（频谱图与 Mel），阶段 5 · 09（Seq2Seq），阶段 7 · 05（完整 Transformer）
**Time:** ~75 minutes | **预计用时:** ~75 分钟

## The Problem | 问题引入

You have a string: "Please remind me to water the plants at 6 pm." You need a 3-second audio clip that sounds natural, has correct prosody (pauses, stress), pronounces "plants" with the right vowel, and runs in under 300 ms on a CPU for a live voice assistant. You also need to swap voices, handle code-switched input ("remind me at 6 pm, daijoubu?"), and not embarrass yourself on names.

> 你有一个字符串："Please remind me to water the plants at 6 pm." 你需要一段 3 秒的音频，听起来自然，韵律正确（停顿、重音），"plants"的元音发音正确，并且在 CPU 上不到 300 ms 就能运行以用于实时语音助手。你还需要切换声音、处理混合语言输入（"remind me at 6 pm, daijoubu?"），且不能在人名上出错。

> **【中文解读】** 本节提出的问题是：如何在实际工程中正确理解和应用这一技术。理解问题背景有助于把握技术选型的关键决策点。在实际 AI 系统中，错误的技术选型往往比实现细节的 bug 代价更高。

Modern TTS pipelines look like this:

> 现代 TTS 流水线如下：

1. **Text frontend.** Normalize text (dates, numbers, emails), convert to phonemes or subword tokens, predict prosody features.
   **文本前端。** 归一化文本（日期、数字、邮箱），转换为音素或子词 token，预测韵律特征。
2. **Acoustic model.** Text → mel spectrogram. Tacotron 2 (2017), FastSpeech 2 (2020), VITS (2021), F5-TTS (2024), Kokoro (2024).
   **声学模型。** 文本 → Mel 频谱图。Tacotron 2（2017）、FastSpeech 2（2020）、VITS（2021）、F5-TTS（2024）、Kokoro（2024）。
3. **Vocoder.** Mel → waveform. WaveNet (2016), WaveRNN, HiFi-GAN (2020), BigVGAN (2022), neural codec vocoders in 2024+.
   **声码器。** Mel → 波形。WaveNet（2016）、WaveRNN、HiFi-GAN（2020）、BigVGAN（2022）、2024+ 的神经编解码声码器。

In 2026 the acoustic + vocoder split blurs with end-to-end diffusion and flow-matching models. But the mental model of three parts still holds for debugging.

> 2026 年，随着端到端扩散和流匹配模型的出现，声学模型 + 声码器的界限变得模糊。但三部分的心理模型对调试仍然有效。

## The Concept | 核心概念

> **【中文解读】** 本节介绍核心概念和理论基础。掌握这些概念是后续动手实现的前提，同时也是面试和工程实践中高频考察的知识点。


![Tacotron, FastSpeech, VITS, F5/Kokoro side-by-side](../assets/tts.svg)

**Tacotron 2 (2017).** Seq2seq: char-embedding → BiLSTM encoder → location-sensitive attention → autoregressive LSTM decoder emits mel frames. Slow (AR), wobbly on long text. Still cited as a baseline.

> **Tacotron 2（2017）。** Seq2seq：字符嵌入 → BiLSTM 编码器 → 位置敏感注意力 → 自回归 LSTM 解码器输出 mel 帧。慢（AR），长文本不稳定。仍被引用为基线。

**FastSpeech 2 (2020).** Non-autoregressive. Duration predictor outputs how many mel frames each phoneme gets. 1-pass, 10× faster than Tacotron. Loses some naturalness (monotonic alignment) but ships everywhere.

> **FastSpeech 2（2020）。** 非自回归。时长预测器输出每个音素获得多少 mel 帧。单次前向，比 Tacotron 快 10 倍。损失一些自然度（单调对齐）但到处都在用。

**VITS (2021).** Jointly trains encoder + flow-based duration + HiFi-GAN vocoder end-to-end with variational inference. High quality, single model. Dominant open-source TTS 2022–2024. Variants: YourTTS (multi-speaker zero-shot), XTTS v2 (2024, Coqui).

> **VITS（2021）。** 联合训练编码器 + 基流的时长预测 + HiFi-GAN 声码器端到端，使用变分推断。高质量，单模型。2022-2024 年主导开源 TTS。变体：YourTTS（多说话人零样本）、XTTS v2（2024，Coqui）。

**F5-TTS (2024).** Diffusion transformer over flow matching. Natural prosody, zero-shot voice cloning with 5 seconds of reference audio. Top of the 2026 open-source TTS leaderboards. 335M params.

> **F5-TTS（2024）。** 基于流匹配的扩散 Transformer。自然韵律，5 秒参考音频零样本声音克隆。2026 年开源 TTS 排行榜榜首。3.35 亿参数。

**Kokoro (2024).** Small (82M), CPU-runnable, best-in-class English TTS for real-time use. Closed-vocabulary English-only, apache-2.0.

> **Kokoro（2024）。** 小型（8200 万参数），可在 CPU 上运行，同类最佳的实时英文 TTS。封闭词表仅限英文，Apache-2.0 许可。

**OpenAI TTS-1-HD, ElevenLabs v2.5, Google Chirp-3.** Commercial state of the art. ElevenLabs v2.5 emotion tags ("[whispered]", "[laughing]") and character voices dominate audiobook production in 2026.

> **OpenAI TTS-1-HD、ElevenLabs v2.5、Google Chirp-3。** 商业 SOTA。ElevenLabs v2.5 的情感标签（"[whispered]"、"[laughing]"）和角色声音主导 2026 年有声书制作。

### Vocoder evolution

> ### 声码器演进

| Era | Vocoder | Latency | Quality |
|-----|---------|---------|---------|
| 2016 | WaveNet | offline only | SOTA at release |
| 2018 | WaveRNN | ~realtime | good |
| 2020 | HiFi-GAN | 100× realtime | near-human |
| 2022 | BigVGAN | 50× realtime | generalizes across speakers/langs |
| 2024 | SNAC, DAC (neural codecs) | integrated with AR models | discrete tokens, bit-efficient |

| 时代 | 声码器 | 延迟 | 质量 |
|------|--------|------|------|
| 2016 | WaveNet | 仅离线 | 发布时 SOTA |
| 2018 | WaveRNN | 约实时 | 良好 |
| 2020 | HiFi-GAN | 100× 实时 | 接近人类 |
| 2022 | BigVGAN | 50× 实时 | 跨说话人/语言泛化 |
| 2024 | SNAC, DAC（神经编解码器） | 与 AR 模型集成 | 离散 token，比特高效 |

By 2026 most "TTS" models are end-to-end from text to waveform; the mel spectrogram is an internal representation.

> 到 2026 年，大多数"TTS"模型是从文本到波形的端到端模型；Mel 频谱图是内部表示。

### Evaluation

> ### 评估

- **MOS (Mean Opinion Score).** 1–5 scale, crowd-sourced. Still the gold standard; painfully slow.
  **MOS（平均意见分）。** 1-5 分量表，众包。仍是黄金标准；速度痛苦地慢。
- **CMOS (Comparative MOS).** A-vs-B preference. Tighter confidence intervals per annotation.
  **CMOS（比较 MOS）。** A-vs-B 偏好。每个标注的置信区间更窄。
- **UTMOS, DNSMOS.** Reference-free neural MOS predictors. Used for leaderboards.
  **UTMOS、DNSMOS。** 无参考神经 MOS 预测器。用于排行榜。
- **CER (Character Error Rate) via ASR.** Run TTS output through Whisper, compute CER against the input text. Proxy for intelligibility.
  **CER（字符错误率）通过 ASR。** 将 TTS 输出通过 Whisper，对输入文本计算 CER。可懂度的代理指标。
- **SECS (Speaker Embedding Cosine Similarity).** Voice-cloning quality.
  **SECS（说话人嵌入余弦相似度）。** 声音克隆质量。

2026 numbers on LibriTTS test-clean:

> 2026 年 LibriTTS test-clean 上的数字：

| Model | UTMOS | CER (via Whisper) | Size |
|-------|-------|-------------------|------|
| Ground truth | 4.08 | 1.2% | — |
| F5-TTS | 3.95 | 2.1% | 335M |
| XTTS v2 | 3.81 | 3.5% | 470M |
| VITS | 3.62 | 3.1% | 25M |
| Kokoro v0.19 | 3.87 | 1.8% | 82M |
| Parler-TTS Large | 3.76 | 2.8% | 2.3B |

| 模型 | UTMOS | CER（通过 Whisper） | 大小 |
|------|-------|---------------------|------|
| 真实音频 | 4.08 | 1.2% | — |
| F5-TTS | 3.95 | 2.1% | 3.35 亿 |
| XTTS v2 | 3.81 | 3.5% | 4.7 亿 |
| VITS | 3.62 | 3.1% | 2500 万 |
| Kokoro v0.19 | 3.87 | 1.8% | 8200 万 |
| Parler-TTS Large | 3.76 | 2.8% | 23 亿 |

> **【中文解读】** 本节通过代码从零实现核心算法。这种 "from scratch" 的方式能帮助理解框架背后的原理，遇到问题时不会被黑盒困住。

> **【拓展：语音 AI 的产品化】** 语音技术在产品化中面临独特挑战：不同口音、背景噪声、远场拾音、多人说话等。Siri、Alexa、小爱同学等产品都投入了大量工程优化来解决这些 "长尾问题"。实时性要求（<300ms 延迟）也是语音产品的核心指标。

> **【拓展：多语言语音技术】** 全球语言的语音特性差异巨大：声调语言（如中文）的音高携带语义，低资源语言缺乏训练数据。Meta 的 MMS 模型支持 1000+ 种语言的语音识别，Whisper 在多语言场景表现出色，但仍需针对特定语言微调。




## Build It | 动手实现

### Step 1: phonemize input

```python
from phonemizer import phonemize
ph = phonemize("Hello world", language="en-us", backend="espeak")
# 'həloʊ wɜːld'
```

Phonemes are the universal bridge. Avoid feeding raw text to anything below VITS-level quality.

> 音素是通用桥梁。避免将原始文本输入到 VITS 级别以下的任何模型。

### Step 2: run Kokoro (2026 CPU default)

```python
from kokoro import KPipeline
tts = KPipeline(lang_code="a")  # "a" = American English
audio, sr = tts("Please remind me to water the plants at 6 pm.", voice="af_bella")
# audio: float32 tensor, sr=24000
```

Runs offline, single file, 82M params.

> 离线运行，单文件，8200 万参数。

### Step 3: run F5-TTS with voice cloning

```python
from f5_tts.api import F5TTS
tts = F5TTS()
wav = tts.infer(
    ref_file="my_voice_5s.wav",
    ref_text="The quick brown fox jumps over the lazy dog.",
    gen_text="Please remind me to water the plants.",
)
```

Pass a 5-second reference clip + its transcript; F5 clones prosody and timbre.

> 传入 5 秒参考音频 + 其转录文本；F5 克隆韵律和音色。

### Step 4: HiFi-GAN vocoder from scratch

Too big to fit in a tutorial script, but the shape is:

```python
class HiFiGAN(nn.Module):
    def __init__(self, mel_channels=80, upsample_rates=[8, 8, 2, 2]):
        super().__init__()
        # 4 upsample blocks, total 256x to go from mel-rate to audio-rate
        ...
    def forward(self, mel):
        return self.blocks(mel)  # -> waveform
```

Training: adversarial (discriminator on short windows) + mel-spectrogram reconstruction loss + feature-matching loss. Commoditized — use pretrained checkpoints from `hifi-gan` repo or nvidia-NeMo.

> 训练：对抗式（短窗口判别器）+ Mel 频谱图重建损失 + 特征匹配损失。已商品化——使用 `hifi-gan` 仓库或 nvidia-NeMo 的预训练检查点。

### Step 5: the full pipeline (pseudocode)

```python
text = "Please remind me at 6 pm."
phones = phonemize(text)
mel = acoustic_model(phones, speaker=alice)      # [T, 80]
wav = vocoder(mel)                                # [T * 256]
soundfile.write("out.wav", wav, 24000)
```

> **【中文解读】** 本节展示如何用成熟框架（如 PyTorch、HuggingFace 等）快速应用该技术。在实际项目中，优先使用经过验证的框架实现，可以减少 bug 并提高开发效率。





> **【拓展：语音与情感计算】** 语音不仅传递文字信息，还携带丰富的情感信号（语调、语速、音高变化）。情感语音识别（Speech Emotion Recognition, SER）在客服质检、心理健康监测、智能教育等领域有广泛应用。当前 SOTA 模型通常基于 wav2vec 2.0 或 HuBERT 等预训练模型微调。

## Use It | 用框架实现

The 2026 stack:

> 2026 年的技术栈：

| Situation | Pick |
|-----------|------|
| Real-time English voice assistant | Kokoro (CPU) or XTTS v2 (GPU) |
| Voice cloning from 5 s reference | F5-TTS |
| Commercial character voices | ElevenLabs v2.5 |
| Audiobook narration | ElevenLabs v2.5 or XTTS v2 + fine-tune |
| Low-resource language | Train VITS on 5–20 h target-lang data |
| Expressive / emotion tags | ElevenLabs v2.5 or StyleTTS 2 fine-tune |

| 场景 | 选择 |
|------|------|
| 实时英文语音助手 | Kokoro（CPU）或 XTTS v2（GPU） |
| 5 秒参考音频声音克隆 | F5-TTS |
| 商业角色声音 | ElevenLabs v2.5 |
| 有声书朗读 | ElevenLabs v2.5 或 XTTS v2 + 微调 |
| 低资源语言 | 在 5-20 小时目标语言数据上训练 VITS |
| 表达性 / 情感标签 | ElevenLabs v2.5 或 StyleTTS 2 微调 |

Open-source leader as of 2026: **F5-TTS for quality, Kokoro for efficiency**. Don't reach for Tacotron unless you are a historian.

> 2026 年开源领导者：**F5-TTS 追求质量，Kokoro 追求效率**。除非你是历史学家，否则别用 Tacotron。



## Pitfalls

> 常见陷阱

- **No text normalizer.** "Dr. Smith" reads as "Doctor" or "Drive"? "2026" as "twenty twenty six" or "two zero two six"? Normalize BEFORE phonemizer.
  **没有文本归一化器。** "Dr. Smith" 读成"Doctor"还是"Drive"？"2026"读成"twenty twenty six"还是"two zero two six"？在音素化之前归一化。
- **OOV proper nouns.** "Ghumare" → "ghyu-mair"? Ship a fallback grapheme-to-phoneme model for unknown tokens.
  **OOV 专有名词。** "Ghumare" → "ghyu-mair"？为未知 token 提供备用的字素到音素模型。
- **Clipping.** Vocoder output rarely clips, but mel scaling mismatch at inference can overshoot ±1.0. Always `np.clip(wav, -1, 1)`.
  **削波。** 声码器输出很少削波，但推理时 Mel 缩放不匹配可能超出 ±1.0。始终使用 `np.clip(wav, -1, 1)`。
- **Sample-rate mismatch.** Kokoro outputs 24 kHz; your downstream pipeline expects 16 kHz → resample or get aliasing.
  **采样率不匹配。** Kokoro 输出 24 kHz；你的下游流水线期望 16 kHz → 重采样否则产生混叠。

> **【中文解读】** 本节关注如何将模型部署为可用的产品。从原型到生产级系统需要考虑性能优化、错误处理、监控等多个维度。


## Ship It | 产出物

Save as `outputs/skill-tts-designer.md`. Design a TTS pipeline for a given voice, latency, and language target.

> 保存为 `outputs/skill-tts-designer.md`。为给定的声音、延迟和语言目标设计 TTS 流水线。

## Exercises | 练习题

1. **Easy.** Run `code/main.py`. Builds a phoneme dictionary from a toy vocab, estimates duration per phoneme, and prints a fake "mel" schedule.
   **简单。** 运行 `code/main.py`。从玩具词表构建音素字典，估算每个音素的时长，并打印假的"mel"计划。
2. **Medium.** Install Kokoro, synthesize the same sentence at voice `af_bella` and `am_adam`. Compare audio durations and subjective quality.
   **中等。** 安装 Kokoro，用 `af_bella` 和 `am_adam` 声音合成同一句话。比较音频时长和主观质量。
3. **Hard.** Record a 5-second reference clip of yourself. Use F5-TTS to clone it. Report SECS between reference and cloned output.
   **困难。** 录制一段 5 秒的自已的参考音频。用 F5-TTS 克隆。报告参考与克隆输出之间的 SECS。

> **【中文解读】** 术语表中的 "What people say" vs "What it actually means" 区分了日常口语和精确技术含义。在团队协作中，统一术语定义可以避免大量沟通误解。


## Key Terms | 术语速查表

| Term | What people say | What it actually means |
|------|-----------------|-----------------------|
| Phoneme | Sound unit | Abstract sound class; 39 in English (ARPABet). |
| Duration predictor | How long each phoneme lasts | Non-AR model output; integer frames per phoneme. |
| Vocoder | Mel → waveform | Neural net mapping mel-spec to raw samples. |
| HiFi-GAN | Standard vocoder | GAN-based; dominant 2020–2024. |
| MOS | Subjective quality | 1–5 mean opinion score from human raters. |
| SECS | Voice-clone metric | Cosine similarity between target and output speaker embedding. |
| F5-TTS | 2024 open-source SOTA | Flow-matching diffusion; zero-shot cloning. |
| Kokoro | CPU English leader | 82M-param model, Apache 2.0. |

| 术语 | 人们常说的 | 实际含义 |
|------|-----------|---------|
| 音素 | 声音单位 | 抽象声音类别；英文有 39 个（ARPABet）。 |
| 时长预测器 | 每个音素持续多久 | 非自回归模型输出；每个音素的整数帧数。 |
| 声码器 | Mel → 波形 | 将 mel 频谱映射为原始采样的神经网络。 |
| HiFi-GAN | 标准声码器 | 基于 GAN；2020-2024 年主导。 |
| MOS | 主观质量 | 人工评分员的 1-5 平均意见分。 |
| SECS | 声音克隆指标 | 目标与输出说话人嵌入之间的余弦相似度。 |
| F5-TTS | 2024 开源 SOTA | 流匹配扩散；零样本克隆。 |
| Kokoro | CPU 英文领导者 | 8200 万参数模型，Apache 2.0。 |

> **【中文解读】** 延伸阅读提供了深入学习的高质量资源。这些论文和教程是该领域的经典参考文献，适合需要深入理解的读者。


## Further Reading | 延伸阅读

- [Shen et al. (2017). Tacotron 2](https://arxiv.org/abs/1712.05884) — the seq2seq baseline.
  Shen 等 (2017). Tacotron 2——seq2seq 基线。
- [Kim, Kong, Son (2021). VITS](https://arxiv.org/abs/2106.06103) — end-to-end flow-based.
  Kim, Kong, Son (2021). VITS——端到端基于流的模型。
- [Chen et al. (2024). F5-TTS](https://arxiv.org/abs/2410.06885) — current open-source SOTA.
  Chen 等 (2024). F5-TTS——当前开源 SOTA。
- [Kong, Kim, Bae (2020). HiFi-GAN](https://arxiv.org/abs/2010.05646) — the vocoder that still ships in 2026.
  Kong, Kim, Bae (2020). HiFi-GAN——2026 年仍在用的声码器。
- [Kokoro-82M on HuggingFace](https://huggingface.co/hexgrad/Kokoro-82M) — 2024 CPU-friendly English TTS.
  Kokoro-82M 在 HuggingFace 上——2024 年 CPU 友好的英文 TTS。

> **【中文解读】** 延伸阅读提供了深入学习的高质量资源，包括论文、教程和工具。建议按需选读，优先阅读标注为 "the critical read" 的核心论文。

