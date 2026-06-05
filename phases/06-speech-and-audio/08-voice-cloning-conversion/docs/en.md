# Voice Cloning & Voice Conversion | 语音克隆与语音转换

> Voice cloning reads your text in someone else's voice. Voice conversion rewrites your voice into someone else's while preserving what you said. Both hang on the same decomposition: separate speaker identity from content.

> **【中文解读】** 语音克隆用别人的声音朗读你的文字；语音转换把你的声音变成别人的但保留内容。两者的核心都是同一个分解：将说话人身份与内容分离。

> **【拓展：语音克隆的伦理与法律】** 语音克隆技术引发严重的伦理和法律问题——深度伪造语音诈骗、名人声音未经授权使用。2025-2026 年多起诉讼（如 Warner Music 5 亿美元和解案）推动了音频水印和防伪造技术的发展。

**Type:** Build | **类型:** 构建
**Languages:** Python | **语言:** Python
**Prerequisites:** Phase 6 · 06 (Speaker Recognition), Phase 6 · 07 (TTS) | **前置知识:** 阶段 6 · 06（说话人识别），阶段 6 · 07（TTS）
**Time:** ~75 minutes | **预计用时:** ~75 分钟

## The Problem | 问题引入

In 2026, a 5-second audio clip is enough to produce a high-quality clone of anyone's voice with a consumer GPU. ElevenLabs, F5-TTS, OpenVoice v2, VoiceBox all ship zero-shot or few-shot cloning. The technology is a blessing (accessibility TTS, dubbing, assistive voices) and a weapon (scam calls, political deepfakes, IP theft).

> 2026 年，一段 5 秒音频就足以用消费级 GPU 高质量克隆任何人的声音。ElevenLabs、F5-TTS、OpenVoice v2、VoiceBox 都提供零样本或少样本克隆。这项技术既是福音（无障碍 TTS、配音、辅助声音），也是武器（诈骗电话、政治深度伪造、知识产权盗窃）。

> **【中文解读】** 本节提出的问题是：如何在实际工程中正确理解和应用这一技术。理解问题背景有助于把握技术选型的关键决策点。在实际 AI 系统中，错误的技术选型往往比实现细节的 bug 代价更高。

Two closely-related tasks:

> 两个密切相关的任务：

- **Voice cloning (TTS-side):** text + 5-second reference voice → audio in that voice.
  **声音克隆（TTS 侧）：** 文本 + 5 秒参考声音 → 该声音的音频。
- **Voice conversion (speech-side):** source audio (person A saying X) + reference voice of person B → audio of B saying X.
  **语音转换（语音侧）：** 源音频（说话人 A 说 X）+ 说话人 B 的参考声音 → B 说 X 的音频。

Both factor a waveform into (content, speaker, prosody) and recombine content from one source with speaker from another.

> 两者都将波形分解为（内容、说话人、韵律）并从一个来源取内容与另一个来源的说话人重新组合。

Key constraint you now ship under in 2026: **watermarking and consent gates are legally required in the EU (AI Act, enforceable August 2026) and in California (AB 2905, effective 2025)**. Your pipeline must emit an inaudible watermark and refuse non-consensual clones.

> 2026 年你面临的关键约束：**水印和同意门在 EU（AI 法案，2026 年 8 月生效）和加利福尼亚州（AB 2905，2025 年生效）是法律要求的**。你的流水线必须发出不可听的水印并拒绝未经同意的克隆。

## The Concept | 核心概念

> **【中文解读】** 本节介绍核心概念和理论基础。掌握这些概念是后续动手实现的前提，同时也是面试和工程实践中高频考察的知识点。


![Voice cloning vs conversion: factorize, swap speaker, recombine](../assets/voice-cloning.svg)

**Zero-shot cloning.** Pass a 5-second clip to a model that has been trained on thousands of speakers. The speaker encoder maps the clip to a speaker embedding; the TTS decoder conditions on that embedding plus text.

> **零样本克隆。** 将 5 秒音频传给在数千说话人上训练过的模型。说话人编码器将音频映射为说话人嵌入；TTS 解码器基于该嵌入加文本生成音频。

Used by: F5-TTS (2024), YourTTS (2022), XTTS v2 (2024), OpenVoice v2 (2024).

> 使用者：F5-TTS（2024）、YourTTS（2022）、XTTS v2（2024）、OpenVoice v2（2024）。

**Few-shot fine-tuning.** Record 5-30 minutes of the target voice. LoRA-fine-tune a base model for an hour. Quality leaps from "okay" to "indistinguishable". Coqui and ElevenLabs both support this pattern; community uses it with F5-TTS.

> **少样本微调。** 录制目标声音 5-30 分钟。LoRA 微调基础模型一小时。质量从"还行"跳到"无法区分"。Coqui 和 ElevenLabs 都支持这种模式；社区用 F5-TTS 实现。

**Voice conversion (VC).** Two families:

> **语音转换（VC）。** 两个家族：

- **Recognition-synthesis.** Run ASR-like model to extract content representation (e.g., soft phoneme posteriors, PPGs), then resynthesize with target speaker embedding. Robust to language and accent. Used by KNN-VC (2023), Diff-HierVC (2023).
  **识别-合成。** 运行类 ASR 模型提取内容表示（如软音素后验、PPG），然后用目标说话人嵌入重新合成。对语言和口音鲁棒。KNN-VC（2023）、Diff-HierVC（2023）使用。
- **Disentanglement.** Train an autoencoder that separates content, speaker, and prosody in latent space at the bottleneck. Swap speaker embedding at inference. Lower quality but faster. Used by AutoVC (2019), VITS-VC variants.
  **解耦。** 训练自编码器在瓶颈处的潜在空间中分离内容、说话人和韵律。推理时交换说话人嵌入。质量较低但更快。AutoVC（2019）、VITS-VC 变体使用。

**Neural codec-based cloning (2024+).** VALL-E, VALL-E 2, NaturalSpeech 3, VoiceBox — treat audio as discrete tokens from SoundStream / EnCodec, train a large autoregressive or flow-matching model over codec tokens. Quality comparable to ElevenLabs on short prompts.

> **基于神经编解码器的克隆（2024+）。** VALL-E、VALL-E 2、NaturalSpeech 3、VoiceBox——将音频视为 SoundStream/EnCodec 的离散 token，在编解码 token 上训练大型自回归或流匹配模型。短提示上质量可与 ElevenLabs 相当。

### The ethics bit, not a bolt-on

> ### 伦理问题，不是可选项

**Watermarking.** PerTh (Perth) and SilentCipher (2024) embed a ~16-32 bit ID imperceptibly in the audio. Survives re-encoding, streaming, and common edits. Production-ready open source.

> **水印。** PerTh 和 SilentCipher（2024）在音频中不可感知地嵌入约 16-32 位 ID。能经受重新编码、流传输和常见编辑。生产可用的开源方案。

**Consent gates.** Must pair every cloned output with a verifiable consent record. "I, Rohit, on 2026-04-22, authorize this voice for X purpose." Store in a tamper-evident log.

> **同意门。** 每个克隆输出必须配对一个可验证的同意记录。"我，Rohit，于 2026-04-22，授权将此声音用于 X 目的。"存储在防篡改日志中。

**Detection.** AASIST, RawNet2, and Wav2Vec2-AASIST ship as detectors. ASVspoof 2025 challenge published EERs of 0.8–2.3% for state-of-the-art detectors against ElevenLabs, VALL-E 2, and Bark outputs.

> **检测。** AASIST、RawNet2 和 Wav2Vec2-AASIST 作为检测器发布。ASVspoof 2025 挑战赛发布了 SOTA 检测器对 ElevenLabs、VALL-E 2 和 Bark 输出的 EER 为 0.8-2.3%。

### Numbers (2026)

> 2026 年的数字

| Model | Zero-shot? | SECS (target sim) | WER (intel.) | Params |
|-------|-----------|--------------------|--------------|--------|
| F5-TTS | Yes | 0.72 | 2.1% | 335M |
| XTTS v2 | Yes | 0.65 | 3.5% | 470M |
| OpenVoice v2 | Yes | 0.70 | 2.8% | 220M |
| VALL-E 2 | Yes | 0.77 | 2.4% | 370M |
| VoiceBox | Yes | 0.78 | 2.1% | 330M |

| 模型 | 零样本？ | SECS（目标相似度） | WER（可懂度） | 参数量 |
|------|---------|-------------------|--------------|--------|
| F5-TTS | 是 | 0.72 | 2.1% | 3.35 亿 |
| XTTS v2 | 是 | 0.65 | 3.5% | 4.7 亿 |
| OpenVoice v2 | 是 | 0.70 | 2.8% | 2.2 亿 |
| VALL-E 2 | 是 | 0.77 | 2.4% | 3.7 亿 |
| VoiceBox | 是 | 0.78 | 2.1% | 3.3 亿 |

> **【中文解读】** 本节通过代码从零实现核心算法。这种 "from scratch" 的方式能帮助理解框架背后的原理，遇到问题时不会被黑盒困住。


SECS > 0.70 is generally indistinguishable from the target for most listeners.

> SECS > 0.70 对大多数听众来说通常与目标无法区分。

> **【拓展：语音 AI 的产品化】** 语音技术在产品化中面临独特挑战：不同口音、背景噪声、远场拾音、多人说话等。Siri、Alexa、小爱同学等产品都投入了大量工程优化来解决这些 "长尾问题"。实时性要求（<300ms 延迟）也是语音产品的核心指标。

> **【拓展：多语言语音技术】** 全球语言的语音特性差异巨大：声调语言（如中文）的音高携带语义，低资源语言缺乏训练数据。Meta 的 MMS 模型支持 1000+ 种语言的语音识别，Whisper 在多语言场景表现出色，但仍需针对特定语言微调。



## Build It | 动手实现

### Step 1: decompose with recognition-synthesis (code-only demo in main.py)

```python
def clone_pipeline(ref_audio, text, target_embedder, tts_model):
    speaker_emb = target_embedder.encode(ref_audio)
    mel = tts_model(text, speaker=speaker_emb)
    return vocoder(mel)
```

Conceptually simple; implementation mass is in `tts_model` and speaker encoder.

> 概念上简单；实现量在 `tts_model` 和说话人编码器中。

### Step 2: zero-shot clone with F5-TTS

```python
from f5_tts.api import F5TTS
tts = F5TTS()
wav = tts.infer(
    ref_file="rohit_5s.wav",
    ref_text="The quick brown fox jumps over the lazy dog.",
    gen_text="Please add milk and bread to my list.",
)
```

Reference transcript must exactly match the audio; mismatch breaks alignment.

> 参考转录必须与音频完全匹配；不匹配会破坏对齐。

### Step 3: voice conversion with KNN-VC

```python
import torch
from knnvc import KNNVC  # 2023 model, https://github.com/bshall/knn-vc
vc = KNNVC.load("wavlm-base-plus")
out_wav = vc.convert(source="my_voice.wav", target_pool=["alice_1.wav", "alice_2.wav"])
```

KNN-VC runs WavLM to extract per-frame embeddings for source and target pool, then replaces each source frame with its nearest neighbor in the pool. Non-parametric, works with a minute of target speech.

> KNN-VC 运行 WavLM 提取源和目标池的逐帧嵌入，然后用池中最近邻替换每个源帧。非参数化，一分钟目标语音即可工作。

### Step 4: embed a watermark

```python
from silentcipher import SilentCipher
sc = SilentCipher(model="2024-06-01")
payload = b"consent_id:abc123;ts:1745353200"
watermarked = sc.embed(wav, sr=24000, message=payload)
detected = sc.detect(watermarked, sr=24000)   # returns payload bytes
```

~32 bits of payload, detectable after MP3 re-encode and light noise.

> 约 32 位载荷，MP3 重编码和轻度噪声后仍可检测。

### Step 5: consent gate

```python
def cloned_inference(text, ref_audio, consent_record):
    assert verify_signature(consent_record), "Signed consent required"
    assert consent_record["speaker_id"] == hash_speaker(ref_audio)
    wav = tts.infer(ref_file=ref_audio, gen_text=text)
    wav = watermark(wav, payload=consent_record["id"])
    return wav
```

> **【中文解读】** 本节展示如何用成熟框架（如 PyTorch、HuggingFace 等）快速应用该技术。在实际项目中，优先使用经过验证的框架实现，可以减少 bug 并提高开发效率。





> **【拓展：语音与情感计算】** 语音不仅传递文字信息，还携带丰富的情感信号（语调、语速、音高变化）。情感语音识别（Speech Emotion Recognition, SER）在客服质检、心理健康监测、智能教育等领域有广泛应用。当前 SOTA 模型通常基于 wav2vec 2.0 或 HuBERT 等预训练模型微调。

## Use It | 用框架实现

The 2026 stack:

> 2026 年的技术栈：

| Situation | Pick |
|-----------|------|
| 5-sec zero-shot clone, open-source | F5-TTS or OpenVoice v2 |
| Commercial production cloning | ElevenLabs Instant Voice Clone v2.5 |
| Voice conversion (rewriting) | KNN-VC or Diff-HierVC |
| Many-speaker fine-tune | StyleTTS 2 + speaker adapter |
| Cross-lingual cloning | XTTS v2 or VALL-E X |
| Deepfake detection | Wav2Vec2-AASIST |

| 场景 | 选择 |
|------|------|
| 5 秒零样本克隆，开源 | F5-TTS 或 OpenVoice v2 |
| 商业生产级克隆 | ElevenLabs Instant Voice Clone v2.5 |
| 语音转换（重写） | KNN-VC 或 Diff-HierVC |
| 多说话人微调 | StyleTTS 2 + 说话人适配器 |
| 跨语言克隆 | XTTS v2 或 VALL-E X |
| 深度伪造检测 | Wav2Vec2-AASIST |



## Pitfalls

> 常见陷阱

- **Misaligned reference transcript.** F5-TTS and similar require the reference text to match the reference audio exactly, punctuation included.
  **参考转录不对齐。** F5-TTS 等要求参考文本与参考音频完全匹配，包括标点。
- **Reverberant reference.** Echo kills the clone. Record dry, close-mic.
  **混响参考。** 回声会毁掉克隆。干声录制，近距离麦克。
- **Emotional mismatch.** Training reference "cheerful" produces cheerful clones of everything. Match reference emotion to target use.
  **情感不匹配。** 训练参考"欢快"会对所有内容产生欢快克隆。匹配参考情感与目标用途。
- **Language leakage.** Cloning an English speaker then asking the model to speak French often carries the accent anyway; use cross-lingual models (XTTS, VALL-E X).
  **语言泄漏。** 克隆英文说话人然后让模型说法语仍会带有口音；使用跨语言模型（XTTS、VALL-E X）。
- **No watermark.** Legally unshippable in EU from Aug 2026.
  **没有水印。** 从 2026 年 8 月起在 EU 法律上不可发布。

> **【中文解读】** 本节关注如何将模型部署为可用的产品。从原型到生产级系统需要考虑性能优化、错误处理、监控等多个维度。


## Ship It | 产出物

Save as `outputs/skill-voice-cloner.md`. Design a cloning or conversion pipeline with consent gate + watermark + quality target.

> 保存为 `outputs/skill-voice-cloner.md`。设计带同意门 + 水印 + 质量目标的克隆或转换流水线。

## Exercises | 练习题

1. **Easy.** Run `code/main.py`. Demonstrates the speaker-embedding swap by computing the cosine between two "speakers" pre and post swap.
   **简单。** 运行 `code/main.py`。通过计算交换前后两个"说话人"的余弦相似度来演示说话人嵌入交换。
2. **Medium.** Use OpenVoice v2 to clone your own voice. Measure SECS between reference and clone. Measure CER via Whisper.
   **中等。** 用 OpenVoice v2 克隆你自己的声音。测量参考与克隆之间的 SECS。通过 Whisper 测量 CER。
3. **Hard.** Apply SilentCipher watermark to 20 clones, run them through 128 kbps MP3 encode+decode, detect the payload. Report bit-accuracy.
   **困难。** 对 20 个克隆应用 SilentCipher 水印，经过 128 kbps MP3 编码+解码，检测载荷。报告比特准确率。

> **【中文解读】** 术语表中的 "What people say" vs "What it actually means" 区分了日常口语和精确技术含义。在团队协作中，统一术语定义可以避免大量沟通误解。


## Key Terms | 术语速查表

| Term | What people say | What it actually means |
|------|-----------------|-----------------------|
| Zero-shot clone | 5 seconds is enough | Pretrained model + speaker embedding; no training. |
| PPG | Phonetic posteriorgram | Per-frame ASR posteriors used as language-agnostic content rep. |
| KNN-VC | Nearest-neighbor conversion | Replace each source frame with nearest target-pool frame. |
| Neural codec TTS | VALL-E style | AR model over EnCodec/SoundStream tokens. |
| Watermark | Inaudible signature | Bits embedded in audio, survive re-encode. |
| SECS | Cloning fidelity | Cosine between target and clone speaker embeddings. |
| AASIST | Deepfake detector | Anti-spoof model; detects synthesized speech. |

| 术语 | 人们常说的 | 实际含义 |
|------|-----------|---------|
| 零样本克隆 | 5 秒就够了 | 预训练模型 + 说话人嵌入；无需训练。 |
| PPG | 音素后验图 | 逐帧 ASR 后验，用作语言无关的内容表示。 |
| KNN-VC | 最近邻转换 | 用目标池中最近邻替换每个源帧。 |
| 神经编解码 TTS | VALL-E 风格 | 在 EnCodec/SoundStream token 上的 AR 模型。 |
| 水印 | 不可听签名 | 嵌入音频中的比特，经受重编码。 |
| SECS | 克隆保真度 | 目标与克隆说话人嵌入之间的余弦相似度。 |
| AASIST | 深度伪造检测器 | 反欺诈模型；检测合成语音。 |

> **【中文解读】** 延伸阅读提供了深入学习的高质量资源。这些论文和教程是该领域的经典参考文献，适合需要深入理解的读者。


## Further Reading | 延伸阅读

- [Chen et al. (2024). F5-TTS](https://arxiv.org/abs/2410.06885) — open-source SOTA zero-shot cloning.
  Chen 等 (2024). F5-TTS——开源 SOTA 零样本克隆。
- [Baevski et al. / Microsoft (2023). VALL-E](https://arxiv.org/abs/2301.02111) and [VALL-E 2 (2024)](https://arxiv.org/abs/2406.05370) — neural-codec TTS.
  Baevski 等 / 微软 (2023). VALL-E 和 VALL-E 2（2024）——神经编解码 TTS。
- [Qian et al. (2019). AutoVC](https://arxiv.org/abs/1905.05879) — disentanglement-based voice conversion.
  Qian 等 (2019). AutoVC——基于解耦的语音转换。
- [Baas, Waubert de Puiseau, Kamper (2023). KNN-VC](https://arxiv.org/abs/2305.18975) — retrieval-based VC.
  Baas, Waubert de Puiseau, Kamper (2023). KNN-VC——基于检索的语音转换。
- [SilentCipher (2024) — Audio Watermarking](https://github.com/sony/silentcipher) — production-ready 32-bit audio watermark.
  SilentCipher（2024）——音频水印——生产可用的 32 位音频水印。
- [ASVspoof 2025 results](https://www.asvspoof.org/) — detector vs synthesizer arms race, updated 2026.
  ASVspoof 2025 结果——检测器 vs 合成器军备竞赛，2026 年更新。

> **【中文解读】** 延伸阅读提供了深入学习的高质量资源，包括论文、教程和工具。建议按需选读，优先阅读标注为 "the critical read" 的核心论文。

