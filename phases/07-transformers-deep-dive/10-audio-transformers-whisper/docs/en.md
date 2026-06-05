# Audio Transformers — Whisper Architecture | 音频 Transformer — Whisper 架构

> Audio is an image of frequency over time. Whisper is a ViT that eats mel spectrograms and speaks back.

> **【中文解读】** Whisper 用 Transformer 做语音识别和翻译。理解音频如何变成 token 序列送入 Transformer。

**Type:** Study | **类型:** 学习
**Language:** Python | **语言:** Python
**Prerequisites:** Phase 7 · 05 (Full Transformer), Phase 7 · 08 (Encoder-Decoder), Phase 7 · 09 (ViT) | **前置知识:** Phase 7 · 05 (Full Transformer), Phase 7 · 08 (Encoder-Decoder), Phase 7 · 09 (ViT)
**Time:** ~45 minutes | **时间:** ~45 分钟

## The Problem | 问题引入

Before Whisper (OpenAI, Radford et al. 2022), state-of-the-art automatic speech recognition (ASR) meant wav2vec 2.0 and HuBERT — self-supervised feature extractors plus a fine-tuned head. High quality, expensive data pipelines, domain-brittle. Multilingual speech recognition needed separate models per language family.

> 在 Whisper（OpenAI，Radford 等人，2022）之前，最先进的自动语音识别（ASR）使用 wav2vec 2.0 和 HuBERT——自监督特征提取器加微调头。质量高，但数据管道昂贵，对领域敏感。多语言语音识别需要每种语言族单独的模型。

Whisper made three bets:

> Whisper 做了三个赌注：

1. **Train on everything.** 680,000 hours of weakly-labeled audio scraped from the internet across 97 languages. No clean academic corpus. No phoneme labels.
   中文翻译：**用一切数据训练。** 68 万小时从互联网抓取的弱标注音频，覆盖 97 种语言。没有干净的学术语料库。没有音素标签。
2. **Multi-task single model.** One decoder trained jointly on transcription, translation, voice activity detection, language ID, and timestamping via task tokens.
   中文翻译：**单模型多任务。** 一个解码器通过任务 token 联合训练转录、翻译、语音活动检测、语言识别和时间戳。
3. **Standard encoder-decoder transformer.** Encoder consumes log-mel spectrograms. Decoder produces text tokens autoregressively. No vocoder, no CTC, no HMM.
   中文翻译：**标准编码器-解码器 Transformer。** 编码器消费 log-mel 频谱图。解码器自回归生成文本 token。没有声码器，没有 CTC，没有 HMM。

The result: Whisper large-v3 is robust across accents, noise, and languages that have zero clean labeled data. It is the default speech front-end for every open-source voice assistant and most commercial ones in 2026.

> 结果：Whisper large-v3 对口音、噪声和零标注数据的语言都具有鲁棒性。它是 2026 年每个开源语音助手和大多数商业语音助手的默认语音前端。

> **【中文解读】** Whisper 的三大创新：(1) 用 68 万小时弱标注音频训练，覆盖 97 种语言；(2) 单模型多任务（转录、翻译、语种识别、时间戳）；(3) 标准编码器-解码器 Transformer 架构。音频被转换为 log-mel 频谱图（类似图像），编码器处理频谱特征，解码器生成文本。

## The Concept | 核心概念

![Whisper pipeline: audio → mel → encoder → decoder → text](../assets/whisper.svg)

### Step 1 — resample + window

Audio at 16 kHz. Clip/pad to 30 seconds. Compute log-mel spectrogram: 80 mel bins, 10 ms stride → ~3,000 frames × 80 features. This is the "input image" that Whisper sees.

> 音频采样率 16 kHz。裁剪/填充到 30 秒。计算 log-mel 频谱图：80 个梅尔频率 bin，10 ms 步长 → 约 3,000 帧 × 80 特征。这就是 Whisper 看到的"输入图像"。

### Step 2 — convolutional stem

Two Conv1D layers with kernel 3 and stride 2 reduce the 3,000 frames to 1,500. Halves sequence length without adding a lot of parameters.

> 两层 Conv1D（核大小 3，步长 2）将 3,000 帧减少到 1,500。将序列长度减半而不增加太多参数。

> **【拓展：Whisper 的多语言能力来源】** Whisper 在 97 种语言、68 万小时音频上训练，多语言能力来自两个因素：(1) 超大规模的弱标注数据覆盖了绝大多数语言；(2) 统一的 BPE 词表是 GPT-2 词表的超集，天然支持多语言。decoder prompt 中的语言 token（如 `<|zh|>`）控制输出语言，使同一模型可以执行转录或翻译任务。

### Step 3 — encoder

A 24-layer (for large) transformer encoder over 1,500 timesteps. Sinusoidal positional encoding, self-attention, GELU FFN. Produces 1,500 × 1,280 hidden states.

> 一个 24 层（large 版本）Transformer 编码器处理 1,500 个时间步。正弦位置编码、自注意力、GELU FFN。产生 1,500 × 1,280 的隐藏状态。

### Step 4 — decoder

A 24-layer transformer decoder. It autoregressively produces tokens from a BPE vocabulary that is a superset of GPT-2's with a few audio-specific special tokens.

> 一个 24 层 Transformer 解码器。自回归地从 BPE 词表生成 token，该词表是 GPT-2 词表的超集，外加几个音频专用特殊 token。

### Step 5 — task tokens

The decoder prompt starts with control tokens that tell the model what to do:

> 解码器提示以控制 token 开头，告诉模型要做什么：

```
<|startoftranscript|>  <|en|>  <|transcribe|>  <|0.00|>
```

or

```
<|startoftranscript|>  <|fr|>  <|translate|>   <|0.00|>
```

The model was trained on this convention. You control task by prefix. The 2026 equivalent of instruction-tuning, but applied to speech.

> 模型按这种约定训练。你通过前缀控制任务。这是指令微调在语音领域的等价物。

> **【中文解读】** Whisper 的任务控制机制非常优雅：通过在解码器前缀中添加特殊 token（如 `<|transcribe|>` 或 `<|translate|>`）来指定任务类型。这是"指令微调"在语音领域的应用——同一模型通过不同的前缀 token 执行不同任务。

> **【拓展：Whisper 在语音助手中的应用】** Whisper 是 2026 年语音 AI 的基础组件。从实时语音助手到视频字幕生成，再到多语言会议翻译，Whisper 提供了统一的语音前端。Whisper-turbo（4 层解码器）将延迟降低 8 倍，使实时对话成为可能。结合 LLM 的后端，形成了"Whisper + LLM + TTS"的现代语音助手架构。

### Step 6 — output

Beam search (width 5) with a log-prob threshold. Timestamps are predicted every 0.02 seconds of audio when the `<|notimestamps|>` token is absent.

> 束搜索（宽度 5）加对数概率阈值。当没有 `<|notimestamps|>` token 时，每 0.02 秒预测一次时间戳。

### Whisper sizes

| Model | Params | Layers | d_model | Heads | VRAM (fp16) |
|-------|--------|--------|---------|-------|-------------|
| 模型 | 参数量 | 层数 | d_model | 头数 | 显存 (fp16) |
| Tiny | 39M | 4 | 384 | 6 | ~1 GB |
| Base | 74M | 6 | 512 | 8 | ~1 GB |
| Small | 244M | 12 | 768 | 12 | ~2 GB |
| Medium | 769M | 24 | 1024 | 16 | ~5 GB |
| Large | 1550M | 32 | 1280 | 20 | ~10 GB |
| Large-v3 | 1550M | 32 | 1280 | 20 | ~10 GB |
| Large-v3-turbo | 809M | 32 | 1280 | 20 | ~6 GB (4-layer decoder) |

Large-v3-turbo (2024) cut the decoder from 32 layers to 4. 8× faster decoding with <1 WER point regression. That decode speed unlock is why Whisper-turbo is the default for real-time voice agents in 2026.

> Large-v3-turbo（2024）将解码器从 32 层减少到 4 层。解码速度提高 8 倍，WER 退化不到 1 个百分点。这种解码速度的突破是 Whisper-turbo 成为 2026 年实时语音代理默认选择的原因。

> **【拓展：音频 Transformer 的统一趋势】** 语音识别（Whisper）、语音合成（VALL-E, Kokoro）、音乐生成（MusicGen）都在转向 Transformer 架构。核心思路相同：将音频转换为频谱图或离散 token 序列，然后用标准 Transformer 处理。这验证了 Transformer 作为通用序列建模器的地位。

### What Whisper does not do

- No diarization (who is speaking). Pair with pyannote for that.
  中文翻译：没有说话人分离（谁在说话）。需要搭配 pyannote 使用。
- No real-time streaming natively — the 30-second window is fixed. Modern wrappers (`faster-whisper`, `WhisperX`) bolt on streaming via VAD + overlap.
  中文翻译：没有原生实时流式处理——30 秒窗口是固定的。现代封装器（`faster-whisper`、`WhisperX`）通过 VAD + 重叠实现流式处理。
- No long-form context beyond 30 s without external chunking. Works well in practice because human speech rarely needs long-range context for transcription.
  中文翻译：没有外部分块则不支持 30 秒以上的长格式上下文。实际效果良好，因为人类语音转录很少需要长距离上下文。

### 2026 landscape

| Task | Model | Notes |
|------|-------|-------|
| 任务 | 模型 | 备注 |
| English ASR | Whisper-turbo, Moonshine | Moonshine is 4× faster on edge |
| 英语 ASR | Whisper-turbo, Moonshine | Moonshine 在边缘设备上快 4 倍 |
| Multilingual ASR | Whisper-large-v3 | 97 languages |
| 多语言 ASR | Whisper-large-v3 | 97 种语言 |
| Streaming ASR | faster-whisper + VAD | 150 ms latency targets achievable |
| 流式 ASR | faster-whisper + VAD | 可实现 150ms 延迟目标 |
| TTS | Piper, XTTS-v2, Kokoro | Encoder-decoder pattern, but Whisper-shaped |
| TTS | Piper, XTTS-v2, Kokoro | 编码器-解码器模式，但类似 Whisper |
| Audio + language | AudioLM, SeamlessM4T | Text tokens + audio tokens in one transformer |
| 音频 + 语言 | AudioLM, SeamlessM4T | 文本 token + 音频 token 在一个 Transformer 中 |

## Build It | 动手实现

See `code/main.py`. We don't train Whisper — we build the log-mel spectrogram pipeline + task-token prompt formatter. Those are the parts you actually touch in production.

> 参见 `code/main.py`。我们不训练 Whisper——我们构建 log-mel 频谱图管道 + 任务 token 提示格式化器。这些是你在生产中实际接触的部分。

### Step 1: synthesize audio

Generate a 1-second sine wave at 440 Hz sampled at 16 kHz. 16,000 samples.

> 生成一个 1 秒的 440 Hz 正弦波，采样率 16 kHz。16,000 个采样点。

### Step 2: log-mel spectrogram (simplified)

Full mel spectrogram needs FFT. We do a simplified framing + per-frame energy version that shows the pipeline without requiring `librosa`:

> 完整的梅尔频谱图需要 FFT。我们做一个简化的分帧 + 逐帧能量版本，无需 `librosa` 即可展示管道：

```python
def frame_signal(x, frame_size=400, hop=160):
    frames = []
    for start in range(0, len(x) - frame_size + 1, hop):
        frames.append(x[start:start + frame_size])
    return frames
```

Frame = 25 ms, hop = 10 ms. Matches Whisper's windowing. Per-frame energy stands in for mel bins for pedagogy.

> 帧 = 25 ms，步长 = 10 ms。与 Whisper 的窗口匹配。逐帧能量用于教学演示，替代梅尔频率 bin。

### Step 3: pad to 30 s

Whisper always processes 30-second chunks. Pad (or clip) the spectrogram to 3,000 frames.

> Whisper 总是处理 30 秒的分块。将频谱图填充（或裁剪）到 3,000 帧。

### Step 4: build the prompt tokens

```python
def whisper_prompt(lang="en", task="transcribe", timestamps=True):
    tokens = ["<|startoftranscript|>", f"<|{lang}|>", f"<|{task}|>"]
    if not timestamps:
        tokens.append("<|notimestamps|>")
    return tokens
```

That is the whole task-control surface. A 4-token prefix.

> 这就是全部的任务控制接口。一个 4 token 的前缀。

## Use It | 用框架实现

```python
import whisper
model = whisper.load_model("large-v3-turbo")
result = model.transcribe("meeting.wav", language="en", task="transcribe")
print(result["text"])
print(result["segments"][0]["start"], result["segments"][0]["end"])
```

Faster, OpenAI-compatible:

> 更快的、与 OpenAI 兼容的方案：

```python
from faster_whisper import WhisperModel
model = WhisperModel("large-v3-turbo", compute_type="int8_float16")
segments, info = model.transcribe("meeting.wav", vad_filter=True)
for s in segments:
    print(f"{s.start:.2f} - {s.end:.2f}: {s.text}")
```

**When to pick Whisper in 2026:**

> **2026 年何时选择 Whisper：**

- Multilingual ASR with one model.
  中文翻译：用一个模型做多语言 ASR。
- Robust transcription of noisy, diverse audio.
  中文翻译：对噪声大、多样化的音频进行鲁棒转录。
- Research / prototype ASR — fastest starting point.
  中文翻译：研究/原型 ASR——最快的起点。

**When to pick something else:**

> **何时选择其他方案：**

- Ultra-low latency streaming on edge — Moonshine beats Whisper at matched quality.
  中文翻译：边缘设备上的超低延迟流式处理——Moonshine 在相同质量下比 Whisper 更快。
- Real-time conversational AI needing <200 ms — dedicated streaming ASR.
  中文翻译：需要 <200ms 的实时对话 AI——专用流式 ASR。
- Speaker diarization — Whisper does not do this; bolt on pyannote.
  中文翻译：说话人分离——Whisper 不做这个；需要加装 pyannote。

## Ship It | 产出物

See `outputs/skill-asr-configurator.md`. The skill picks an ASR model, decoding parameters, and preprocessing pipeline for a new speech application.

> 参见 `outputs/skill-asr-configurator.md`。该 skill 为新的语音应用选择 ASR 模型、解码参数和预处理管道。

## Exercises | 练习题

1. **Easy.** Run `code/main.py`. Confirm the frame count for a 1-second signal at 16 kHz with 10 ms hop is ~100 frames. For 30 seconds: ~3,000 frames.
   中文翻译：运行 `code/main.py`。确认 1 秒信号在 16 kHz、10 ms 步长下约 100 帧。30 秒：约 3,000 帧。
2. **Medium.** Build the full log-mel spectrogram using `numpy.fft`. Verify 80 mel bins match `librosa.feature.melspectrogram(n_mels=80)` within numerical error.
   中文翻译：用 `numpy.fft` 构建完整的 log-mel 频谱图。验证 80 个梅尔频率 bin 与 `librosa.feature.melspectrogram(n_mels=80)` 在数值误差范围内一致。
3. **Hard.** Implement streaming inference: chunk audio into 10 s windows with 2 s overlap, run Whisper on each chunk, merge transcripts. Measure word-error rate vs single-pass on a 5-minute podcast sample.
   中文翻译：实现流式推理：将音频分成 10 秒窗口（2 秒重叠），在每个窗口上运行 Whisper，合并转录。在 5 分钟播客样本上测量词错误率与单次处理的对比。

## Key Terms | 术语速查表

| Term | What people say | What it actually means |
|------|-----------------|-----------------------|
| 术语 | 通俗说法 | 实际含义 |
| Mel spectrogram | "Audio image" | 2D representation: frequency bins on one axis, time frames on the other; log-scaled energy per cell. |
| 梅尔频谱图 | "音频图像" | 2D 表示：一个轴是频率 bin，另一个是时间帧；每个单元是对数缩放的能量。 |
| Log-mel | "What Whisper sees" | Mel spectrogram passed through log; approximates human perception of loudness. |
| Log-mel | "Whisper 看到的" | 梅尔频谱图取对数；近似人类对响度的感知。 |
| Frame | "One time slice" | A 25 ms window of samples; overlapping at 10 ms stride. |
| 帧 | "一个时间切片" | 25 ms 的采样窗口；10 ms 步长重叠。 |
| Task token | "Prompt prefix for speech" | Special tokens like `<\|transcribe\|>` / `<\|translate\|>` in the decoder prompt. |
| 任务 token | "语音的提示前缀" | 解码器提示中的特殊 token，如 `<\|transcribe\|>` / `<\|translate\|>`。 |
| Voice activity detection (VAD) | "Find the speech" | Gate that removes silence before ASR; cuts cost massively. |
| 语音活动检测 (VAD) | "找到语音" | 在 ASR 之前去除静音的门控；大幅降低成本。 |
| CTC | "Connectionist Temporal Classification" | Classic ASR loss for alignment-free training; Whisper does NOT use it. |
| CTC | "连接主义时间分类" | 经典的 ASR 对齐无关训练损失；Whisper 不使用它。 |
| Whisper-turbo | "Small decoder, full encoder" | large-v3 encoder + 4-layer decoder; 8× faster decoding. |
| Whisper-turbo | "小解码器，全编码器" | large-v3 编码器 + 4 层解码器；解码速度提高 8 倍。 |
| Faster-whisper | "The production wrapper" | CTranslate2 reimplementation; int8 quantization; 4× faster than OpenAI's reference. |
| Faster-whisper | "生产封装器" | CTranslate2 重新实现；int8 量化；比 OpenAI 参考实现快 4 倍。 |

## Further Reading | 延伸阅读

- [Radford et al. (2022). Robust Speech Recognition via Large-Scale Weak Supervision](https://arxiv.org/abs/2212.04356) — Whisper paper.
  中文翻译：Whisper 论文。
- [OpenAI Whisper repo](https://github.com/openai/whisper) — reference code + model weights. Read `whisper/model.py` to see the Conv1D stem + encoder + decoder top-to-bottom in ~400 lines.
  中文翻译：OpenAI Whisper 代码仓库，约 400 行代码展示 Conv1D stem + 编码器 + 解码器。
- [OpenAI Whisper — `whisper/decoding.py`](https://github.com/openai/whisper/blob/main/whisper/decoding.py) — the beam-search + task-token logic described in Steps 5–6 is here; 500 lines, fully readable.
  中文翻译：束搜索 + 任务 token 逻辑的实现，500 行代码，完全可读。
- [Baevski et al. (2020). wav2vec 2.0: A Framework for Self-Supervised Learning of Speech Representations](https://arxiv.org/abs/2006.11477) — precursor; still SOTA features in some settings.
  中文翻译：wav2vec 2.0 论文；Whisper 的前身，在某些场景下仍是 SOTA 特征。
- [SYSTRAN/faster-whisper](https://github.com/SYSTRAN/faster-whisper) — production wrapper, 4× faster than reference.
  中文翻译：faster-whisper 生产封装器，比参考实现快 4 倍。
- [Jia et al. (2024). Moonshine: Speech Recognition for Live Transcription and Voice Commands](https://arxiv.org/abs/2410.15608) — 2024 edge-friendly ASR, Whisper-shaped but smaller.
  中文翻译：Moonshine 论文，2024 年面向边缘的 ASR，类 Whisper 但更小。
- [HuggingFace blog — "Fine-Tune Whisper For Multilingual ASR with 🤗 Transformers"](https://huggingface.co/blog/fine-tune-whisper) — canonical fine-tuning recipe including mel spectrogram preprocessor and token-timestamp handling.
  中文翻译：HuggingFace Whisper 微调教程，包括梅尔频谱图预处理器和 token 时间戳处理。
- [HuggingFace `modeling_whisper.py`](https://github.com/huggingface/transformers/blob/main/src/transformers/models/whisper/modeling_whisper.py) — full implementation (encoder, decoder, cross-attention, generation) that mirrors the lesson's architecture diagram.
  中文翻译：HuggingFace Whisper 完整实现（编码器、解码器、交叉注意力、生成），与课程架构图对应。
