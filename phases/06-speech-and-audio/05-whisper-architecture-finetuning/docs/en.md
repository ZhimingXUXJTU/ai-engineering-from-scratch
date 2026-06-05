# Whisper — Architecture & Fine-Tuning | Whisper — 架构与微调

> Whisper is a 30-second-window transformer encoder-decoder, trained on 680k hours of multilingual weakly-supervised audio-text pairs. One architecture, multiple tasks, robust across 99 languages. The 2026 reference ASR.

> **【中文解读】** Whisper 是 30 秒窗口的 Transformer 编码器-解码器，在 68 万小时多语言弱监督音频-文本对上训练。一个架构，多种任务（识别、翻译、检测语言），覆盖 99 种语言。是 2026 年语音识别的标杆模型。

> **【拓展：Whisper 的生态】** Whisper 衍生了 whisper.cpp（本地部署）、Faster-Whisper（CTranslate2 加速）、WhisperX（词级时间戳）、Bloomsbury（实时流式）等工具链，是语音识别工业部署的事实标准。

**Type:** Build | **类型:** 构建
**Languages:** Python | **语言:** Python
**Prerequisites:** Phase 6 · 04 (ASR), Phase 5 · 10 (Attention), Phase 7 · 05 (Full Transformer) | **前置知识:** 阶段 6 · 04（ASR），阶段 5 · 10（注意力机制），阶段 7 · 05（完整 Transformer）
**Time:** ~75 minutes | **预计用时:** ~75 分钟

## The Problem | 问题引入

Whisper, released by OpenAI in September 2022, was the first ASR model to ship as a commodity: paste audio, get text, 99 languages, robust to noise, runs on a laptop. By 2024 OpenAI had shipped Large-v3 and Turbo variants; by 2026, Whisper is the default baseline for everything from podcast transcription to voice assistants to YouTube subtitles.

> Whisper 由 OpenAI 于 2022 年 9 月发布，是第一个作为通用商品发布的 ASR 模型：粘贴音频，获取文本，99 种语言，抗噪声，可在笔记本上运行。到 2024 年，OpenAI 发布了 Large-v3 和 Turbo 变体；到 2026 年，Whisper 是从播客转录到语音助手到 YouTube 字幕等所有场景的默认基线。

> **【中文解读】** 本节提出的问题是：如何在实际工程中正确理解和应用这一技术。理解问题背景有助于把握技术选型的关键决策点。在实际 AI 系统中，错误的技术选型往往比实现细节的 bug 代价更高。

But Whisper is not a pipeline you can treat as a black box forever. Domain shift kills it — technical jargon, speaker accents, proper nouns, short clips, silence. You need to know:

> 但 Whisper 不是可以永远当黑盒使用的流水线。领域偏移会毁掉它——技术术语、说话人口音、专有名词、短片段、静音。你需要知道：

1. What it actually is inside.
   它内部到底是什么结构。
2. How to give it chunked, streaming, or long-form audio correctly.
   如何正确地给它分块、流式或长音频输入。
3. When to fine-tune and how.
   何时微调以及如何微调。

> **【中文解读】** 本节介绍核心概念和理论基础。掌握这些概念是后续动手实现的前提，同时也是面试和工程实践中高频考察的知识点。


## The Concept | 核心概念

![Whisper encoder-decoder, tasks, chunked inference, fine-tune](../assets/whisper.svg)

**Architecture.** Standard transformer encoder-decoder.

> **架构。** 标准 Transformer 编码器-解码器。

- Input: 30-second log-mel spectrogram, 80 mels, 10 ms hop → 3000 frames. Clips shorter are zero-padded, clips longer are chunked.
  输入：30 秒 log-mel 频谱图，80 mels，10 ms 步长 → 3000 帧。短片段零填充，长片段分块。
- Encoder: conv-downsample (stride 2) + `N` transformer blocks. For Large-v3: 32 layers, 1280-dim, 20 heads.
  编码器：卷积下采样（步幅 2）+ `N` 个 Transformer 块。Large-v3：32 层，1280 维，20 头。
- Decoder: `N` transformer blocks with causal self-attn + cross-attn to encoder output. Same size as encoder.
  解码器：`N` 个带因果自注意力 + 对编码器输出的交叉注意力的 Transformer 块。与编码器同大小。
- Output: BPE tokens over a 51,865-token vocab.
  输出：51,865 token 词表上的 BPE token。

Large-v3 has 1.55B params. Turbo uses a 4-layer decoder (from 32), cutting latency 8× with a <1% WER hit.

> Large-v3 有 15.5 亿参数。Turbo 使用 4 层解码器（从 32 层减少），延迟降低 8 倍，WER 损失不到 1%。

**The prompt format.** Whisper is a multitask model steered by special tokens in the decoder prompt:

> **提示格式。** Whisper 是一个多任务模型，通过解码器提示中的特殊 token 来控制：

```
<|startoftranscript|><|en|><|transcribe|><|notimestamps|> Hello world.<|endoftext|>
```

- `<|en|>` — language tag; forces translation-vs-transcription behavior.
  `<|en|>` —— 语言标签；强制翻译或转录行为。
- `<|transcribe|>` or `<|translate|>` — translate English output from any-language input, or verbatim.
  `<|transcribe|>` 或 `<|translate|>` —— 从任何语言输入翻译为英文输出，或逐字转录。
- `<|notimestamps|>` — skip word-level timestamps (faster).
  `<|notimestamps|>` —— 跳过词级时间戳（更快）。

The prompt is what lets one model do many tasks. Change `<|en|>` to `<|fr|>` and it transcribes French.

> 提示就是让一个模型完成多种任务的关键。把 `<|en|>` 改为 `<|fr|>` 就转录法语。

**30-second window.** Everything is pinned to 30 seconds. Longer clips need chunking; shorter clips are padded. Windows are not streamed natively — this is why WhisperX, Whisper-Streaming, and faster-whisper exist.

> **30 秒窗口。** 一切都以 30 秒为基准。更长的音频需要分块；更短的音频需要填充。窗口本身不支持原生流式处理——这就是 WhisperX、Whisper-Streaming 和 faster-whisper 存在的原因。

**Log-mel normalization.** `(log_mel - mean) / std` where the stats come from Whisper's own training corpus. You *must* use Whisper's preprocessing (`whisper.audio.log_mel_spectrogram`), not `librosa.feature.melspectrogram`.

> **Log-mel 归一化。** `(log_mel - mean) / std`，其中统计量来自 Whisper 自己的训练语料。你*必须*使用 Whisper 的预处理（`whisper.audio.log_mel_spectrogram`），而不是 `librosa.feature.melspectrogram`。

### Variants in 2026

> ### 2026 年的变体

| Variant | Params | Latency (A100) | WER (LibriSpeech-clean) |
|---------|--------|----------------|------------------------|
| Tiny | 39M | 1× realtime | 5.4% |
| Base | 74M | 1× | 4.1% |
| Small | 244M | 1× | 3.0% |
| Medium | 769M | 1× | 2.7% |
| Large-v3 | 1.55B | 2× | 1.8% |
| Large-v3-turbo | 809M | 8× | 1.58% |
| Whisper-Streaming (2024) | 1.55B | streaming | 2.0% |

| 变体 | 参数量 | 延迟（A100） | WER（LibriSpeech-clean） |
|------|--------|--------------|-------------------------|
| Tiny | 3900 万 | 1× 实时 | 5.4% |
| Base | 7400 万 | 1× | 4.1% |
| Small | 2.44 亿 | 1× | 3.0% |
| Medium | 7.69 亿 | 1× | 2.7% |
| Large-v3 | 15.5 亿 | 2× | 1.8% |
| Large-v3-turbo | 8.09 亿 | 8× | 1.58% |
| Whisper-Streaming（2024） | 15.5 亿 | 流式 | 2.0% |

### Fine-tuning

> ### 微调

Canonical workflow in 2026:

> 2026 年的标准流程：

1. Collect 10–100 hours of target-domain audio with aligned transcripts.
   收集 10-100 小时目标领域的音频及对应转录文本。
2. Run `transformers.Seq2SeqTrainer` with `generate_with_loss` callback.
   使用 `transformers.Seq2SeqTrainer` 和 `generate_with_loss` 回调运行训练。
3. Parameter-efficient: LoRA on `q_proj`, `k_proj`, `v_proj` of attention layers reduces GPU memory 4× with <0.3 WER cost.
   参数高效：在注意力层的 `q_proj`、`k_proj`、`v_proj` 上使用 LoRA，GPU 内存降低 4 倍，WER 损失 <0.3。
4. Freeze the encoder if you have <10 hours. Only tune the decoder.
   如果数据不足 10 小时则冻结编码器，只微调解码器。
5. Use Whisper's own tokenizer and prompt format; never swap tokenizers.
   使用 Whisper 自己的 tokenizer 和提示格式；永远不要替换 tokenizer。

Community results: fine-tuning Medium on 20 hours of medical dictation drops WER from 12% to 4.5% on medical vocabulary. Fine-tuning Turbo on 4 hours of Icelandic drops WER from 18% to 6%.

> 社区结果：在 20 小时医疗口述上微调 Medium，医疗词汇 WER 从 12% 降到 4.5%。在 4 小时冰岛语上微调 Turbo，WER 从 18% 降到 6%。

> **【拓展：语音 AI 的产品化】** 语音技术在产品化中面临独特挑战：不同口音、背景噪声、远场拾音、多人说话等。Siri、Alexa、小爱同学等产品都投入了大量工程优化来解决这些 "长尾问题"。实时性要求（<300ms 延迟）也是语音产品的核心指标。

> **【拓展：多语言语音技术】** 全球语言的语音特性差异巨大：声调语言（如中文）的音高携带语义，低资源语言缺乏训练数据。Meta 的 MMS 模型支持 1000+ 种语言的语音识别，Whisper 在多语言场景表现出色，但仍需针对特定语言微调。



## Build It | 动手实现

> **【中文解读】** 本节通过代码从零实现核心算法。这种 "from scratch" 的方式能帮助理解框架背后的原理，遇到问题时不会被黑盒困住。


### Step 1: run Whisper out of the box

```python
import whisper
model = whisper.load_model("large-v3-turbo")
result = model.transcribe(
    "clip.wav",
    language="en",
    task="transcribe",
    temperature=0.0,
    condition_on_previous_text=False,  # prevents runaway repetition
)
print(result["text"])
for seg in result["segments"]:
    print(f"[{seg['start']:.2f}–{seg['end']:.2f}] {seg['text']}")
```

Key defaults you should always override: `temperature=0.0` (sampling defaults to 0.0 → 0.2 → 0.4 … fallback chain), `condition_on_previous_text=False` (prevents the cascading hallucination problem), and `no_speech_threshold=0.6` (silence detection).

> 你应该始终覆盖的关键默认值：`temperature=0.0`（采样默认为 0.0 → 0.2 → 0.4 ... 回退链）、`condition_on_previous_text=False`（防止级联幻觉问题）和 `no_speech_threshold=0.6`（静音检测）。

### Step 2: chunked long-form

```python
# whisperx is the 2026 reference for long-form with word-level timestamps
import whisperx
model = whisperx.load_model("large-v3-turbo", device="cuda", compute_type="float16")
segments = model.transcribe("1hour.mp3", batch_size=16, chunk_size=30)
```

WhisperX adds (1) Silero VAD gating, (2) word-level alignment via wav2vec 2.0, (3) diarization via `pyannote.audio`. The 2026 workhorse for production transcription.

> WhisperX 添加了 (1) Silero VAD 门控，(2) 通过 wav2vec 2.0 实现词级对齐，(3) 通过 `pyannote.audio` 实现说话人分离。2026 年生产转录的主力工具。

### Step 3: fine-tune with LoRA

```python
from transformers import WhisperForConditionalGeneration, WhisperProcessor
from peft import LoraConfig, get_peft_model

model = WhisperForConditionalGeneration.from_pretrained("openai/whisper-large-v3-turbo")
lora = LoraConfig(
    r=16, lora_alpha=32, target_modules=["q_proj", "v_proj"],
    lora_dropout=0.1, bias="none", task_type="SEQ_2_SEQ_LM",
)
model = get_peft_model(model, lora)
# model.print_trainable_parameters()  -> ~3M trainable / 809M total
```

Then standard Trainer loop. Checkpoint every 1000 steps. Evaluate with WER on held-out.

> 然后标准的 Trainer 训练循环。每 1000 步保存检查点。在留出集上用 WER 评估。

### Step 4: inspect what each layer learns

```python
# Grab cross-attention weights during decode to see what the decoder attends to.
with torch.inference_mode():
    out = model.generate(
        input_features=features,
        return_dict_in_generate=True,
        output_attentions=True,
    )
# out.cross_attentions: layer × head × step × src_len
```

> **【中文解读】** 本节展示如何用成熟框架（如 PyTorch、HuggingFace 等）快速应用该技术。在实际项目中，优先使用经过验证的框架实现，可以减少 bug 并提高开发效率。


Visualize with a heatmap — you will see diagonal alignment as decoder steps scan through encoder frames. That diagonal is Whisper's notion of word timestamps.

> 用热力图可视化——你会看到解码器步进扫描编码器帧时的对角线对齐。那条对角线就是 Whisper 的词时间戳概念。




> **【拓展：语音与情感计算】** 语音不仅传递文字信息，还携带丰富的情感信号（语调、语速、音高变化）。情感语音识别（Speech Emotion Recognition, SER）在客服质检、心理健康监测、智能教育等领域有广泛应用。当前 SOTA 模型通常基于 wav2vec 2.0 或 HuBERT 等预训练模型微调。

## Use It | 用框架实现

The 2026 stack:

> 2026 年的技术栈：

| Situation | Pick |
|-----------|------|
| General English, offline | Large-v3-turbo via `whisperx` |
| Mobile / edge | Whisper-Tiny quantized (int8) or Moonshine |
| Multilingual long-form | Large-v3 via `whisperx` + diarization |
| Low-resource language | Fine-tune Medium or Turbo with LoRA |
| Streaming (2 s latency) | Whisper-Streaming or Parakeet-TDT |
| Word-level timestamps | WhisperX (forced alignment via wav2vec 2.0) |

| 场景 | 选择 |
|------|------|
| 通用英文、离线 | 通过 `whisperx` 使用 Large-v3-turbo |
| 移动端/边缘设备 | 量化 Whisper-Tiny（int8）或 Moonshine |
| 多语言长音频 | 通过 `whisperx` 使用 Large-v3 + 说话人分离 |
| 低资源语言 | 用 LoRA 微调 Medium 或 Turbo |
| 流式（2 秒延迟） | Whisper-Streaming 或 Parakeet-TDT |
| 词级时间戳 | WhisperX（通过 wav2vec 2.0 强制对齐） |

`faster-whisper` (CTranslate2 backend) is the fastest CPU+GPU inference runtime in 2026 — 4× faster than vanilla with identical output.

> `faster-whisper`（CTranslate2 后端）是 2026 年最快的 CPU+GPU 推理运行时——比原始版本快 4 倍，输出完全相同。



## Pitfalls that still ship in 2026

> 2026 年仍然在犯的陷阱

- **Hallucinated text on silence.** Whisper trained on captions includes "Thanks for watching!", "Subscribe!", song lyrics. Always VAD-gate before calling.
  **静音上的幻觉文本。** Whisper 在字幕数据上训练，会包含"Thanks for watching!"、"Subscribe!"、歌词。调用前务必用 VAD 过滤。
- **`condition_on_previous_text` cascade.** One hallucination pollutes subsequent windows. Set `False` unless you need fluency across chunks.
  **`condition_on_previous_text` 级联。** 一次幻觉会污染后续窗口。除非需要跨块流畅性，否则设为 `False`。
- **Short-clip padding.** A 2-second clip padded to 30 seconds can hallucinate in the trailing silence. Use `pad=False` or VAD-gate.
  **短片段填充。** 2 秒片段填充到 30 秒可能在尾部静音处产生幻觉。使用 `pad=False` 或 VAD 过滤。
- **Wrong mel stats.** Using librosa's mels instead of Whisper's produces near-random output. Use `whisper.audio.log_mel_spectrogram`.
  **错误的 mel 统计量。** 使用 librosa 的 mels 而非 Whisper 的会产生近乎随机的输出。使用 `whisper.audio.log_mel_spectrogram`。

> **【中文解读】** 本节关注如何将模型部署为可用的产品。从原型到生产级系统需要考虑性能优化、错误处理、监控等多个维度。


## Ship It | 产出物

Save as `outputs/skill-whisper-tuner.md`. Design a Whisper fine-tune or inference pipeline for a given domain.

> 保存为 `outputs/skill-whisper-tuner.md`。为给定领域设计 Whisper 微调或推理流水线。

## Exercises | 练习题

1. **Easy.** Run `code/main.py`. It tokenizes a Whisper-style prompt, computes decoded shape budgets, and prints the chunk schedule for a 10-minute clip.
   **简单。** 运行 `code/main.py`。它对 Whisper 风格的提示进行 token 化，计算解码形状预算，并打印 10 分钟音频的分块计划。
2. **Medium.** Install `faster-whisper`, transcribe a 10-minute podcast, compare WER against a human transcript. Try `language="auto"` vs forced `language="en"`.
   **中等。** 安装 `faster-whisper`，转录 10 分钟播客，与人工转录比较 WER。尝试 `language="auto"` 与强制 `language="en"`。
3. **Hard.** Using HF `datasets`, pick a language Whisper struggles with (e.g., Urdu), fine-tune Medium with LoRA for 2 epochs on 2 hours, and report WER delta.
   **困难。** 使用 HF `datasets`，选一个 Whisper 困难的语言（如乌尔都语），在 2 小时数据上用 LoRA 微调 Medium 2 个 epoch，报告 WER 差值。

> **【中文解读】** 术语表中的 "What people say" vs "What it actually means" 区分了日常口语和精确技术含义。在团队协作中，统一术语定义可以避免大量沟通误解。


## Key Terms | 术语速查表

| Term | What people say | What it actually means |
|------|-----------------|-----------------------|
| 30-sec window | Whisper's limit | Hard input cap; chunk longer audio. |
| SOT | Start-of-transcript | `<\|startoftranscript\|>` kicks off the decoder prompt. |
| Timestamps token | Temporal alignment | Every 0.02 s offset is a special token in the 51k vocab. |
| Turbo | The fast variant | 4-decoder layers, 8× faster, <1% WER regression. |
| WhisperX | The long-form wrapper | VAD + Whisper + wav2vec alignment + diarization. |
| LoRA fine-tune | Efficient tuning | Add low-rank adapters to attention; train ~0.3% of params. |
| Hallucination | The silent failure | Whisper produces fluent English from noise/silence. |

| 术语 | 人们常说的 | 实际含义 |
|------|-----------|---------|
| 30 秒窗口 | Whisper 的限制 | 硬性输入上限；更长音频需分块。 |
| SOT | 转录开始 | `<\|startoftranscript\|>` 启动解码器提示。 |
| 时间戳 token | 时间对齐 | 每 0.02 秒偏移是 51k 词表中的特殊 token。 |
| Turbo | 快速变体 | 4 层解码器，快 8 倍，WER 回退 <1%。 |
| WhisperX | 长音频封装 | VAD + Whisper + wav2vec 对齐 + 说话人分离。 |
| LoRA 微调 | 高效调优 | 在注意力层添加低秩适配器；仅训练约 0.3% 参数。 |
| 幻觉 | 静默失败 | Whisper 从噪声/静音中产生流畅的英文。 |

> **【中文解读】** 延伸阅读提供了深入学习的高质量资源。这些论文和教程是该领域的经典参考文献，适合需要深入理解的读者。


## Further Reading | 延伸阅读

- [Radford et al. (2022). Whisper paper](https://arxiv.org/abs/2212.04356) — the original architecture and training recipe.
  Radford 等 (2022). Whisper 论文——原始架构和训练方案。
- [OpenAI (2024). Whisper Large-v3-turbo release](https://github.com/openai/whisper/discussions/2363) — 4-layer decoder, 8× speedup.
  OpenAI (2024). Whisper Large-v3-turbo 发布——4 层解码器，8 倍加速。
- [Bain et al. (2023). WhisperX](https://arxiv.org/abs/2303.00747) — long-form, word-aligned, diarized.
  Bain 等 (2023). WhisperX——长音频、词级对齐、说话人分离。
- [Systran — faster-whisper repo](https://github.com/SYSTRAN/faster-whisper) — CTranslate2-backed, 4× faster.
  Systran——faster-whisper 仓库——CTranslate2 后端，快 4 倍。
- [HuggingFace — Whisper fine-tune tutorial](https://huggingface.co/blog/fine-tune-whisper) — canonical LoRA / full-FT walkthrough.
  HuggingFace——Whisper 微调教程——标准 LoRA/全参数微调指南。

> **【中文解读】** 延伸阅读提供了深入学习的高质量资源，包括论文、教程和工具。建议按需选读，优先阅读标注为 "the critical read" 的核心论文。

