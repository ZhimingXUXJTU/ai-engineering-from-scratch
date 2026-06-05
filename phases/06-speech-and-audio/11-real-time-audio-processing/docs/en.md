# Real-Time Audio Processing | 实时音频处理

> Batch pipelines process a file. Real-time pipelines process the next 20 milliseconds before the next 20 arrive. Every conversational AI, broadcast studio, and telephony bot lives and dies by this latency budget.

> **【中文解读】** 批处理流水线处理文件，实时流水线在下 20 毫秒到达之前处理完这 20 毫秒。每个对话式 AI、广播系统和电话机器人都在这个延迟预算上生死存亡。实时音频处理是语音 AI 落地的关键工程挑战。

**Type:** Build | **类型:** 构建
**Languages:** Python | **语言:** Python
**Prerequisites:** Phase 6 · 02 (Spectrograms), Phase 6 · 04 (ASR), Phase 6 · 07 (TTS) | **前置知识:** 阶段 6 · 02（频谱图），阶段 6 · 04（ASR），阶段 6 · 07（TTS）
**Time:** ~75 minutes | **预计用时:** ~75 分钟

## The Problem | 问题引入

You want a voice assistant that feels alive. Human conversational turn-taking latency is ~230 ms (silence-to-response). Anything above 500 ms feels robotic; above 1500 ms feels broken. The budget for a full **hear → understand → respond → speak** loop in 2026 is:

> 你想要一个"活的"语音助手。人类对话轮次延迟约 230 ms（静音到回应）。超过 500 ms 感觉像机器人；超过 1500 ms 感觉坏掉了。2026 年完整的**听 → 理解 → 回应 → 说**循环预算是：

> **【中文解读】** 本节提出的问题是：如何在实际工程中正确理解和应用这一技术。理解问题背景有助于把握技术选型的关键决策点。在实际 AI 系统中，错误的技术选型往往比实现细节的 bug 代价更高。

| Stage | Budget |
|-------|--------|
| Mic → buffer | 20 ms |
| VAD | 10 ms |
| ASR (streaming) | 150 ms |
| LLM (first token) | 100 ms |
| TTS (first chunk) | 100 ms |
| Render → speaker | 20 ms |
| **Total** | **~400 ms** |

| 阶段 | 预算 |
|------|------|
| 麦克风 → 缓冲 | 20 ms |
| VAD | 10 ms |
| ASR（流式） | 150 ms |
| LLM（首 token） | 100 ms |
| TTS（首块） | 100 ms |
| 渲染 → 扬声器 | 20 ms |
| **总计** | **约 400 ms** |

Moshi (Kyutai, 2024) clocked 200 ms full-duplex. GPT-4o-realtime (2024) clocks ~320 ms. Cascaded pipelines in 2022 shipped at 2500 ms. The 10× improvement came from three techniques: (1) streaming everywhere, (2) asynchronous pipelining with partial results, (3) interruptible generation.

> Moshi（Kyutai，2024）实现了 200 ms 全双工。GPT-4o-realtime（2024）约 320 ms。2022 年的级联流水线延迟 2500 ms。10 倍提升来自三个技术：(1) 全面流式化，(2) 带部分结果的异步流水线，(3) 可中断生成。

## The Concept | 核心概念

> **【中文解读】** 本节介绍核心概念和理论基础。掌握这些概念是后续动手实现的前提，同时也是面试和工程实践中高频考察的知识点。


![Streaming audio pipeline with ring buffer, VAD gate, interruption](../assets/real-time.svg)

**Frame / chunk / window.** Real-time audio flows as fixed-size blocks. Common choice: 20 ms (320 samples at 16 kHz). Everything downstream must keep up with this cadence.

> **帧/块/窗口。** 实时音频以固定大小的块流动。常见选择：20 ms（16 kHz 下 320 采样点）。下游一切都必须跟上这个节奏。

**Ring buffer.** Fixed-size circular buffer. Producer thread writes new frames, consumer thread reads. Prevents allocations in the hot path. Size ≈ maximum-latency × sample-rate; a 2-second 16 kHz ring = 32,000 samples.

> **环形缓冲区。** 固定大小的循环缓冲区。生产者线程写入新帧，消费者线程读取。防止热路径中的内存分配。大小约等于最大延迟 × 采样率；2 秒 16 kHz 环形缓冲 = 32,000 采样点。

**VAD (Voice Activity Detection).** Gates downstream work when nobody is speaking. Silero VAD 4.0 (2024) runs <1 ms per 30 ms frame on CPU. `webrtcvad` is the older alternative.

> **VAD（语音活动检测）。** 无人说话时阻止下游工作。Silero VAD 4.0（2024）在 CPU 上每 30 ms 帧运行 <1 ms。`webrtcvad` 是较旧的替代方案。

**Streaming ASR.** Models that emit partial transcripts as audio arrives. Parakeet-CTC-0.6B in streaming mode (NeMo, 2024) does 2–5% WER at 320 ms latency. Whisper-Streaming (Macháček et al., 2023) chunks Whisper for near-streaming at ~2 s latency.

> **流式 ASR。** 随音频到达而输出部分转录的模型。Parakeet-CTC-0.6B 流式模式（NeMo，2024）在 320 ms 延迟下做到 2-5% WER。Whisper-Streaming（Macháček 等，2023）将 Whisper 分块以实现接近流式的约 2 秒延迟。

**Interruption.** When the user speaks while the assistant is talking, you must (a) detect the barge-in, (b) stop the TTS, (c) discard the remaining LLM output. All within 100 ms, or the user perceives deaf assistant.

> **打断。** 当助手在说话时用户开口，你必须 (a) 检测到抢话，(b) 停止 TTS，(c) 丢弃剩余 LLM 输出。全部在 100 ms 内完成，否则用户感觉助手是聋子。

**WebRTC Opus transport.** 20 ms frames, 48 kHz, adaptive bitrate 8–128 kbps. Standard for browser and mobile. LiveKit, Daily.co, Pion are the 2026 stacks for building voice apps.

> **WebRTC Opus 传输。** 20 ms 帧，48 kHz，自适应比特率 8-128 kbps。浏览器和移动端标准。LiveKit、Daily.co、Pion 是 2026 年构建语音应用的技术栈。

**Jitter buffer.** Network packets arrive out of order / late. The jitter buffer reorders and smooths; too small → audible gaps, too large → latency. 60–80 ms typical.

> **抖动缓冲区。** 网络包乱序/迟到到达。抖动缓冲区重排和平滑；太小 → 可听间隙，太大 → 延迟。典型值 60-80 ms。

### Common gotchas

> ### 常见陷阱

- **Thread contention.** Python's GIL + heavy models can starve the audio thread. Use a C-callback audio library (sounddevice, PortAudio) and keep Python off the hot path.
  **线程竞争。** Python 的 GIL + 重模型会使音频线程饥饿。使用 C 回调音频库（sounddevice、PortAudio），让 Python 远离热路径。
- **Sample-rate conversion latency.** Resampling inside the pipeline adds 5–20 ms. Either resample upfront or use a zero-latency resampler (PolyPhase, `soxr_hq`).
  **采样率转换延迟。** 流水线内部重采样增加 5-20 ms。要么提前重采样，要么使用零延迟重采样器。
- **TTS priming.** Even fast TTS like Kokoro has a 100–200 ms warm-up on first request. Cache model + warm it with a dummy run before the first real turn.
  **TTS 预热。** 即使像 Kokoro 这样的快速 TTS 在首次请求时也有 100-200 ms 预热。缓存模型 + 在第一个真实轮次前用假运行预热。
- **Echo cancellation.** Without AEC, TTS output re-enters the mic and triggers ASR on the bot's own voice. WebRTC AEC3 is the open-source default.
  **回声消除。** 没有 AEC，TTS 输出重新进入麦克风并触发 ASR 识别机器人自己的声音。WebRTC AEC3 是开源默认方案。

> **【中文解读】** 本节通过代码从零实现核心算法。这种 "from scratch" 的方式能帮助理解框架背后的原理，遇到问题时不会被黑盒困住。

> **【拓展：语音 AI 的产品化】** 语音技术在产品化中面临独特挑战：不同口音、背景噪声、远场拾音、多人说话等。Siri、Alexa、小爱同学等产品都投入了大量工程优化来解决这些 "长尾问题"。实时性要求（<300ms 延迟）也是语音产品的核心指标。

> **【拓展：多语言语音技术】** 全球语言的语音特性差异巨大：声调语言（如中文）的音高携带语义，低资源语言缺乏训练数据。Meta 的 MMS 模型支持 1000+ 种语言的语音识别，Whisper 在多语言场景表现出色，但仍需针对特定语言微调。

> **【拓展：语音隐私与安全】** 语音数据包含大量个人隐私信息（声纹、对话内容）。深度伪造（Deepfake）语音技术可以被滥用于诈骗。音频水印（Audio Watermarking）和声纹反欺诈（Anti-spoofing）是当前的研究热点。





## Build It | 动手实现

### Step 1: ring buffer

```python
import collections

class RingBuffer:
    def __init__(self, capacity):
        self.buf = collections.deque(maxlen=capacity)
    def write(self, frame):
        self.buf.extend(frame)
    def read(self, n):
        return [self.buf.popleft() for _ in range(min(n, len(self.buf)))]
    def level(self):
        return len(self.buf)
```

Capacity determines max buffering latency. 32,000 samples at 16 kHz = 2 s.

### Step 2: VAD gate

```python
def simple_energy_vad(frame, threshold=0.01):
    return sum(x * x for x in frame) / len(frame) > threshold ** 2
```

Replace with Silero VAD in production:

```python
import torch
vad, _ = torch.hub.load("snakers4/silero-vad", "silero_vad")
is_speech = vad(torch.tensor(frame), 16000).item() > 0.5
```

### Step 3: streaming ASR

```python
# Parakeet-CTC-0.6B streaming via NeMo
from nemo.collections.asr.models import EncDecCTCModelBPE
asr = EncDecCTCModelBPE.from_pretrained("nvidia/parakeet-ctc-0.6b")
# chunk_ms=320 ms, look_ahead_ms=80 ms
for chunk in audio_stream():
    partial_text = asr.transcribe_streaming(chunk)
    print(partial_text, end="\r")
```

### Step 4: interruption handler

```python
class Dialog:
    def __init__(self):
        self.tts_task = None

    def on_user_speech(self, frame):
        if self.tts_task and not self.tts_task.done():
            self.tts_task.cancel()   # barge-in
        # then feed to streaming ASR

    def on_final_user_utterance(self, text):
        self.tts_task = asyncio.create_task(self.reply(text))

    async def reply(self, text):
        async for tts_chunk in llm_then_tts(text):
            speaker.write(tts_chunk)
```

> **【中文解读】** 本节展示如何用成熟框架（如 PyTorch、HuggingFace 等）快速应用该技术。在实际项目中，优先使用经过验证的框架实现，可以减少 bug 并提高开发效率。


Hinges on async I/O and cancellable TTS streaming. WebRTC peerconnection.stop() on the audio track is the canonical way.

> 依赖于异步 I/O 和可取消的 TTS 流式传输。WebRTC 的 peerconnection.stop() 停止音频轨道是标准方式。




> **【拓展：语音与情感计算】** 语音不仅传递文字信息，还携带丰富的情感信号（语调、语速、音高变化）。情感语音识别（Speech Emotion Recognition, SER）在客服质检、心理健康监测、智能教育等领域有广泛应用。当前 SOTA 模型通常基于 wav2vec 2.0 或 HuBERT 等预训练模型微调。

## Use It | 用框架实现

The 2026 stack:

| Layer | Pick |
|-------|------|
| Transport | LiveKit (WebRTC) or Pion (Go) |
| VAD | Silero VAD 4.0 |
| Streaming ASR | Parakeet-CTC-0.6B or Whisper-Streaming |
| LLM first-token | Groq, Cerebras, vLLM-streaming |
| Streaming TTS | Kokoro or ElevenLabs Turbo v2.5 |
| Echo cancel | WebRTC AEC3 |
| End-to-end native | OpenAI Realtime API or Moshi |

| 层 | 选择 |
|----|------|
| 传输 | LiveKit（WebRTC）或 Pion（Go） |
| VAD | Silero VAD 4.0 |
| 流式 ASR | Parakeet-CTC-0.6B 或 Whisper-Streaming |
| LLM 首 token | Groq、Cerebras、vLLM-streaming |
| 流式 TTS | Kokoro 或 ElevenLabs Turbo v2.5 |
| 回声消除 | WebRTC AEC3 |
| 端到端原生 | OpenAI Realtime API 或 Moshi |



## Pitfalls

> 常见陷阱

- **Buffering 500 ms to be safe.** The buffer *is* your latency floor. Shrink it.
  **缓冲 500 ms 求安全。** 缓冲区*就是*你的延迟下限。缩小它。
- **Not pinning threads.** Audio callback on a priority-lower-than-UI thread = glitches under load.
  **没有绑定线程。** 音频回调在低于 UI 优先级的线程上 = 负载下出现故障。
- **TTS chunks too small.** Sub-200 ms chunks make vocoder artifacts audible. 320 ms chunks are the sweet spot.
  **TTS 块太小。** 低于 200 ms 的块使声码器伪影可听。320 ms 块是最佳平衡点。
- **No jitter buffer.** Real networks are jittery; without smoothing you get pops.
  **没有抖动缓冲。** 真实网络有抖动；没有平滑会出现爆音。
- **Single-shot error handling.** Audio pipelines must be crash-proof. One exception kills the session.
  **单次错误处理。** 音频流水线必须抗崩溃。一个异常就杀死会话。

> **【中文解读】** 本节关注如何将模型部署为可用的产品。从原型到生产级系统需要考虑性能优化、错误处理、监控等多个维度。


## Ship It | 产出物

Save as `outputs/skill-realtime-designer.md`. Design a real-time audio pipeline with concrete latency budgets per stage.

> 保存为 `outputs/skill-realtime-designer.md`。设计每阶段有具体延迟预算的实时音频流水线。

## Exercises | 练习题

1. **Easy.** Run `code/main.py`. Simulates a ring buffer + energy VAD; prints stage latencies for a fake 10-second stream.
   **简单。** 运行 `code/main.py`。模拟环形缓冲区 + 能量 VAD；打印假 10 秒流的各阶段延迟。
2. **Medium.** Using `sounddevice`, build a passthrough loop that processes your mic in 20 ms frames and prints VAD state at each frame.
   **中等。** 使用 `sounddevice` 构建直通循环，以 20 ms 帧处理麦克风并在每帧打印 VAD 状态。
3. **Hard.** Build a full duplex echo test with `aiortc`: browser → WebRTC → Python → WebRTC → browser. Measure glass-to-glass latency with a 1 kHz pulse.
   **困难。** 用 `aiortc` 构建全双工回声测试：浏览器 → WebRTC → Python → WebRTC → 浏览器。用 1 kHz 脉冲测量端到端延迟。

> **【中文解读】** 术语表中的 "What people say" vs "What it actually means" 区分了日常口语和精确技术含义。在团队协作中，统一术语定义可以避免大量沟通误解。


## Key Terms | 术语速查表

| Term | What people say | What it actually means |
|------|-----------------|-----------------------|
| Ring buffer | The circular queue | Fixed-size, lock-free (or SPSC-locked) FIFO for audio frames. |
| VAD | Silence gate | Model or heuristic marking speech vs non-speech. |
| Streaming ASR | Real-time STT | Emits partial text as audio arrives; bounded lookahead. |
| Jitter buffer | Network smoother | Queue reordering out-of-order packets; 60–80 ms typical. |
| AEC | Echo cancellation | Subtracts speaker-to-mic feedback path. |
| Barge-in | User interrupt | System detects user speech mid-TTS; must cancel playback. |
| Full duplex | Simultaneous both ways | User and bot can talk at the same time; Moshi is full duplex. |

| 术语 | 人们常说的 | 实际含义 |
|------|-----------|---------|
| 环形缓冲 | 那个循环队列 | 固定大小、无锁（或 SPSC 锁）的音频帧 FIFO。 |
| VAD | 静音门 | 标记语音 vs 非语音的模型或启发式。 |
| 流式 ASR | 实时 STT | 随音频到达输出部分文本；有限前瞻。 |
| 抖动缓冲 | 网络平滑器 | 重排乱序包的队列；典型 60-80 ms。 |
| AEC | 回声消除 | 减去扬声器到麦克风的反馈路径。 |
| 抢话 | 用户打断 | 系统在 TTS 播放中检测用户语音；必须取消播放。 |
| 全双工 | 双向同时 | 用户和机器人可以同时说话；Moshi 是全双工。 |

> **【中文解读】** 延伸阅读提供了深入学习的高质量资源。这些论文和教程是该领域的经典参考文献，适合需要深入理解的读者。


## Further Reading | 延伸阅读

- [Macháček et al. (2023). Whisper-Streaming](https://arxiv.org/abs/2307.14743) — chunked near-streaming Whisper.
  Macháček 等 (2023). Whisper-Streaming——分块近流式 Whisper。
- [Kyutai (2024). Moshi](https://kyutai.org/Moshi.pdf) — full-duplex 200 ms latency.
  Kyutai (2024). Moshi——全双工 200 ms 延迟。
- [LiveKit Agents framework (2024)](https://docs.livekit.io/agents/) — production audio agent orchestration.
  LiveKit Agents 框架（2024）——生产级音频智能体编排。
- [Silero VAD repo](https://github.com/snakers4/silero-vad) — sub-1 ms VAD, Apache 2.0.
  Silero VAD 仓库——亚毫秒 VAD，Apache 2.0。
- [WebRTC AEC3 paper](https://webrtc.googlesource.com/src/+/main/modules/audio_processing/aec3/) — echo cancellation under open source.
  WebRTC AEC3 论文——开源回声消除。

> **【中文解读】** 延伸阅读提供了深入学习的高质量资源，包括论文、教程和工具。建议按需选读，优先阅读标注为 "the critical read" 的核心论文。

