# Voice Activity Detection & Turn-Taking — Silero, Cobra, and the Flush Trick | 语音活动检测与轮次切换

> Every voice agent lives or dies on two decisions: is the user speaking now, and are they done? VAD answers the first. Turn-detection (VAD + silence-hangover + semantic endpoint model) answers the second. Get either wrong and your assistant either cuts users off or never shuts up.

> **【中文解读】** 每个语音助手的成败取决于两个判断：用户现在在说话吗？用户说完了吗？VAD（语音活动检测）回答第一个，轮次检测（VAD+静音持续+语义终点模型）回答第二个。任何一个搞错，助手要么打断用户，要么永远不开口。

**Type:** Build | **类型:** 构建
**Languages:** Python | **语言:** Python
**Prerequisites:** Phase 6 · 11 (Real-Time Audio), Phase 6 · 12 (Voice Assistant) | **前置知识:** 阶段 6 · 11（实时音频），阶段 6 · 12（语音助手）
**Time:** ~45 minutes | **预计用时:** ~45 分钟

## The Problem | 问题引入

Three distinct decisions a voice agent makes on every 20 ms chunk:

> 语音助手在每 20 ms 的音频块上需要做出三个不同的判断：

> **【中文解读】** 本节提出的问题是：如何在实际工程中正确理解和应用这一技术。理解问题背景有助于把握技术选型的关键决策点。在实际 AI 系统中，错误的技术选型往往比实现细节的 bug 代价更高。


1. **Is this frame speech?** — VAD. Binary, per-frame.
   中文翻译：这一帧是语音吗？——VAD。二分类，逐帧判断。
2. **Has the user started a new utterance?** — onset detection.
   中文翻译：用户开始了一个新的发言吗？——起始检测。
3. **Has the user finished?** — end-pointing (turn-end).
   中文翻译：用户说完了吗？——端点检测（轮次结束）。

The naive answer (energy threshold) fails on any noise — traffic, keyboards, crowd babble. The 2026 answer: Silero VAD (open, deep-learned) + a turn-detection model (semantic endpointing) + a VAD-calibrated silence hangover.

> 朴素的答案（能量阈值）在任何噪声环境下都会失败——交通声、键盘声、人群嘈杂声。2026 年的答案是：Silero VAD（开源、深度学习）+ 轮次检测模型（语义端点检测）+ VAD 校准的静音持续等待。

## The Concept | 核心概念

> **【中文解读】** 本节介绍核心概念和理论基础。掌握这些概念是后续动手实现的前提，同时也是面试和工程实践中高频考察的知识点。


![VAD cascade: energy → Silero → turn-detector → flush trick](../assets/vad-turn-taking.svg)

### The three-tier VAD cascade

> 三级 VAD 级联架构

**Tier 1: energy gate.** Cheapest. Threshold RMS at -40 dBFS. Filters obvious silence but fires on any noise above the threshold.

> **第一层：能量门控。** 最廉价的方法。将 RMS 阈值设为 -40 dBFS。能过滤明显的静音，但任何超过阈值的噪声都会触发。

**Tier 2: Silero VAD** (2020-2026, MIT). 1M parameters. Trained on 6000+ languages. Runs in ~1 ms per 30 ms chunk on a single CPU thread. 87.7% TPR at 5% FPR. The open-source default.

> **第二层：Silero VAD**（2020-2026，MIT 许可）。100 万参数。在 6000+ 种语言上训练。在单 CPU 线程上每 30 ms 块约 1 ms 推理时间。5% FPR 下 TPR 达 87.7%。开源方案的默认选择。

**Tier 3: semantic turn detector.** LiveKit's turn-detection model (2024-2026) or your own small classifier. Distinguishes "pause mid-sentence" from "done talking." Uses linguistic context (intonation + recent words), not just silence.

> **第三层：语义轮次检测器。** LiveKit 的轮次检测模型（2024-2026）或自定义小分类器。区分"句子中间的停顿"和"说完了"。使用语言上下文（语调 + 近期词汇），而不仅是静音。

### Key parameters and their defaults

> 关键参数及其默认值

- **Threshold.** Silero outputs a probability; classify speech at &gt; 0.5 (default) or &gt; 0.3 (sensitive). Lower threshold = fewer first-word clips, more false positives.
  中文翻译：**阈值。** Silero 输出概率值；以 > 0.5（默认）或 > 0.3（敏感模式）分类语音。阈值越低 = 首词截断越少，但误报越多。
- **Minimum speech duration.** Reject speech shorter than 250 ms — usually coughs or chair noise.
  中文翻译：**最小语音时长。** 拒绝短于 250 ms 的语音——通常是咳嗽或椅子噪声。
- **Silence hangover (end-pointing).** After VAD returns to 0, wait 500-800 ms before declaring end-of-turn. Too short → interrupt user. Too long → feels sluggish.
  中文翻译：**静音持续等待（端点检测）。** VAD 回到 0 后，等待 500-800 ms 再宣布轮次结束。太短 → 打断用户。太长 → 感觉迟钝。
- **Pre-roll buffer.** Keep 300-500 ms of audio before VAD fires. Prevents "hey" being clipped.
  中文翻译：**预滚缓冲。** 在 VAD 触发前保留 300-500 ms 音频。防止"嘿"字被截断。

### The flush trick (Kyutai 2025)

Streaming STT models have a look-ahead delay (500 ms for Kyutai STT-1B, 2.5 s for STT-2.6B). Normally you'd wait that long after end-of-speech for the transcript. Flush trick: when VAD fires end-of-speech, **send a flush signal to the STT** that forces immediate output. STT processes at ~4× realtime, so the 500 ms buffer finishes in ~125 ms.

> 流式 STT 模型有前视延迟（Kyutai STT-1B 为 500 ms，STT-2.6B 为 2.5 s）。通常你需要在语音结束后等待这么长时间才能获得转录结果。刷新技巧：当 VAD 触发语音结束时，**向 STT 发送刷新信号**，强制立即输出。STT 以约 4 倍实时速度处理，所以 500 ms 缓冲区在约 125 ms 内完成。

End-to-end: 125 ms VAD + flush STT = conversational latency.

> 端到端：125 ms VAD + 刷新 STT = 对话级延迟。

### 2026 VAD comparison

> 2026 年 VAD 对比

| VAD | TPR @ 5% FPR | Latency | License |
|-----|--------------|---------|---------|
| WebRTC VAD (Google, 2013) | 50.0% | 30 ms | BSD |
| Silero VAD (2020-2026) | 87.7% | ~1 ms | MIT |
| Cobra VAD (Picovoice) | 98.9% | ~1 ms | commercial |
| pyannote segmentation | 95% | ~10 ms | MIT-ish |

Silero is the right default. Cobra is the compliance / accuracy upgrade. Energy-only VAD has no place in 2026 production.

> Silero 是正确的默认选择。Cobra 是合规性/准确性的升级选项。仅基于能量的 VAD 在 2026 年的生产环境中已没有立足之地。

> **【中文解读】** 本节通过代码从零实现核心算法。这种 "from scratch" 的方式能帮助理解框架背后的原理，遇到问题时不会被黑盒困住。

> **【拓展：语音 AI 的产品化】** 语音技术在产品化中面临独特挑战：不同口音、背景噪声、远场拾音、多人说话等。Siri、Alexa、小爱同学等产品都投入了大量工程优化来解决这些 "长尾问题"。实时性要求（<300ms 延迟）也是语音产品的核心指标。

> **【拓展：多语言语音技术】** 全球语言的语音特性差异巨大：声调语言（如中文）的音高携带语义，低资源语言缺乏训练数据。Meta 的 MMS 模型支持 1000+ 种语言的语音识别，Whisper 在多语言场景表现出色，但仍需针对特定语言微调。

> **【拓展：语音隐私与安全】** 语音数据包含大量个人隐私信息（声纹、对话内容）。深度伪造（Deepfake）语音技术可以被滥用于诈骗。音频水印（Audio Watermarking）和声纹反欺诈（Anti-spoofing）是当前的研究热点。





## Build It | 动手实现

### Step 1: the energy gate

> 步骤 1：能量门控

```python
def energy_vad(chunk, threshold_dbfs=-40.0):
    rms = (sum(x * x for x in chunk) / len(chunk)) ** 0.5
    dbfs = 20.0 * math.log10(max(rms, 1e-10))
    return dbfs > threshold_dbfs
```

### Step 2: Silero VAD in Python

> 步骤 2：在 Python 中使用 Silero VAD

```python
from silero_vad import load_silero_vad, get_speech_timestamps

vad = load_silero_vad()
audio = torch.tensor(waveform_16k, dtype=torch.float32)
segments = get_speech_timestamps(
    audio, vad, sampling_rate=16000,
    threshold=0.5,
    min_speech_duration_ms=250,
    min_silence_duration_ms=500,
    speech_pad_ms=300,
)
for s in segments:
    print(f"{s['start']/16000:.2f}s - {s['end']/16000:.2f}s")
```

### Step 3: turn-end state machine

> 步骤 3：轮次结束状态机

```python
class TurnDetector:
    def __init__(self, silence_hangover_ms=500, min_speech_ms=250):
        self.state = "idle"
        self.speech_ms = 0
        self.silence_ms = 0
        self.silence_hangover_ms = silence_hangover_ms
        self.min_speech_ms = min_speech_ms

    def update(self, is_speech, chunk_ms=20):
        if is_speech:
            self.speech_ms += chunk_ms
            self.silence_ms = 0
            if self.state == "idle" and self.speech_ms >= self.min_speech_ms:
                self.state = "speaking"
                return "START"
        else:
            self.silence_ms += chunk_ms
            if self.state == "speaking" and self.silence_ms >= self.silence_hangover_ms:
                self.state = "idle"
                self.speech_ms = 0
                return "END"
        return None
```

### Step 4: the flush trick skeleton

> 步骤 4：刷新技巧框架代码

```python
def flush_on_end(stt_client, audio_buffer):
    stt_client.send_audio(audio_buffer)
    stt_client.send_flush()
    return stt_client.recv_transcript(timeout_ms=150)
```

> **【中文解读】** 本节展示如何用成熟框架（如 PyTorch、HuggingFace 等）快速应用该技术。在实际项目中，优先使用经过验证的框架实现，可以减少 bug 并提高开发效率。


STT (Kyutai, Deepgram, AssemblyAI) must support flush for this to work. Whisper streaming does not — it's block-based and always waits for chunks.

> STT（Kyutai、Deepgram、AssemblyAI）必须支持 flush 才能使此技巧生效。Whisper 流式不支持——它是基于块的，总是等待完整块。




> **【拓展：语音与情感计算】** 语音不仅传递文字信息，还携带丰富的情感信号（语调、语速、音高变化）。情感语音识别（Speech Emotion Recognition, SER）在客服质检、心理健康监测、智能教育等领域有广泛应用。当前 SOTA 模型通常基于 wav2vec 2.0 或 HuBERT 等预训练模型微调。

## Use It | 用框架实现

| Situation | VAD choice |
|-----------|-----------|
| Open, fast, general / 开源、快速、通用 | Silero VAD |
| Commercial call center / 商业呼叫中心 | Cobra VAD |
| On-device (phone) / 端侧（手机） | Silero VAD ONNX |
| Research / diarization / 研究/说话人日志 | pyannote segmentation |
| Zero-dependency fallback / 零依赖后备方案 | WebRTC VAD（传统） |
| Need turn-ending quality / 需要轮次结束质量 | Silero + LiveKit 轮次检测器分层 |

Rule of thumb: never ship energy-only VAD unless you really have no other option.

> 经验法则：除非真的没有其他选择，否则永远不要上线仅基于能量的 VAD。



## Pitfalls

> 常见陷阱

- **Fixed threshold.** Works in quiet, fails in noisy. Either calibrate on-device or switch to Silero.
  中文翻译：**固定阈值。** 在安静环境下有效，嘈杂环境下失败。要么在设备上校准，要么切换到 Silero。
- **Too-short silence hangover.** Agent interrupts mid-sentence. 500-800 ms is the sweet spot for conversational speech.
  中文翻译：**静音持续等待过短。** 助手在句子中间打断用户。500-800 ms 是对话语音的最佳范围。
- **Too-long hangover.** Feels sluggish. A/B test with target users.
  中文翻译：**静音持续等待过长。** 感觉迟钝。与目标用户进行 A/B 测试。
- **No pre-roll buffer.** First 200-300 ms of user audio lost. Always keep a rolling pre-roll.
  中文翻译：**没有预滚缓冲。** 用户音频的前 200-300 ms 丢失。始终保持滚动预滚缓冲。
- **Ignoring semantic endpointing.** "Hmm, let me think..." contains long pauses. Users hate being cut off mid-thought. Use LiveKit's turn-detector or similar.
  中文翻译：**忽略语义端点检测。** "嗯，让我想想……"包含长停顿。用户讨厌在思考过程中被打断。使用 LiveKit 的轮次检测器或类似方案。

> **【中文解读】** 本节关注如何将模型部署为可用的产品。从原型到生产级系统需要考虑性能优化、错误处理、监控等多个维度。


## Ship It | 产出物

Save as `outputs/skill-vad-tuner.md`. Pick VAD model, threshold, hangover, pre-roll, and turn-detection strategy for a workload.

> 保存为 `outputs/skill-vad-tuner.md`。为一个工作负载选择 VAD 模型、阈值、静音持续等待、预滚缓冲和轮次检测策略。

## Exercises | 练习题

1. **Easy.** Run `code/main.py`. It simulates a speech + silence + speech + coughs sequence and tests three VAD tiers.
   中文翻译：**简单。** 运行 `code/main.py`。它模拟一段语音 + 静音 + 语音 + 咳嗽的序列，并测试三层 VAD。
2. **Medium.** Install `silero-vad`, process a 5-min recording, tune threshold to minimize both first-word clips and false triggers. Report precision/recall.
   中文翻译：**中等。** 安装 `silero-vad`，处理一段 5 分钟录音，调整阈值以最小化首词截断和误触发。报告精确率/召回率。
3. **Hard.** Build a mini turn-detector: Silero VAD + a 3-layer MLP on the last 10 words' embeddings (use sentence-transformers). Train on a hand-labeled turn-end dataset. Beat Silero-only by 10% F1.
   中文翻译：**困难。** 构建一个小型轮次检测器：Silero VAD + 基于 10 个近词嵌入的 3 层 MLP（使用 sentence-transformers）。在手工标注的轮次结束数据集上训练。比纯 Silero 方案 F1 高 10%。

> **【中文解读】** 术语表中的 "What people say" vs "What it actually means" 区分了日常口语和精确技术含义。在团队协作中，统一术语定义可以避免大量沟通误解。


## Key Terms | 术语速查表

| Term | What people say | What it actually means |
|------|-----------------|-----------------------|
| VAD | Voice detector | Binary per-frame: is this speech? / 逐帧二分类：这是语音吗？ |
| Turn detection | End-pointing | VAD + silence-hangover + semantic endpoint. / VAD + 静音持续 + 语义端点 |
| Silence hangover | Wait-after-speech | Time to wait before declaring turn end; 500-800 ms. / 宣布轮次结束前的等待时间；500-800 ms |
| Pre-roll | Pre-speech buffer | Keep 300-500 ms audio before VAD fires. / 在 VAD 触发前保留 300-500 ms 音频 |
| Flush trick | Kyutai hack | VAD → flush-STT → 125 ms instead of 500 ms delay. / VAD → 刷新 STT → 125 ms 而非 500 ms 延迟 |
| Semantic endpoint | "Did they mean to stop?" | ML classifier that looks at words, not just silence. / 看词汇而非仅看静音的 ML 分类器 |
| TPR @ FPR 5% | ROC point | Standard VAD benchmark; 87.7% for Silero, 50% WebRTC. / 标准 VAD 基准；Silero 87.7%，WebRTC 50% |

> **【中文解读】** 延伸阅读提供了深入学习的高质量资源。这些论文和教程是该领域的经典参考文献，适合需要深入理解的读者。


## Further Reading | 延伸阅读

- [Silero VAD](https://github.com/snakers4/silero-vad) — the reference open VAD.
  Silero VAD——开源参考 VAD。
- [Picovoice Cobra VAD](https://picovoice.ai/products/cobra/) — commercial accuracy leader.
  Picovoice Cobra VAD——商业精度领先者。
- [Kyutai — Unmute + flush trick](https://kyutai.org/stt) — the sub-200 ms engineering trick.
  Kyutai——Unmute + 刷新技巧——亚 200 ms 的工程技巧。
- [LiveKit — turn detection](https://docs.livekit.io/agents/logic/turns/) — semantic endpointing in production.
  LiveKit——轮次检测——生产中的语义端点检测。
- [WebRTC VAD](https://webrtc.googlesource.com/src/) — the legacy baseline.
  WebRTC VAD——传统基线。
- [pyannote segmentation](https://github.com/pyannote/pyannote-audio) — diarization-grade segmentation.
  pyannote segmentation——说话人日志级别的分割。

> **【中文解读】** 延伸阅读提供了深入学习的高质量资源，包括论文、教程和工具。建议按需选读，优先阅读标注为 "the critical read" 的核心论文。

