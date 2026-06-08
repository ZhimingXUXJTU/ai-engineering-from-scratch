# Voice Agents: Pipecat and LiveKit | PipeCat LiveKit Agent 语音

> Voice agents are a first-class production category in 2026. Pipecat gives you a Python frame-based pipeline (VAD → STT → LLM → TTS → transport). LiveKit Agents bridges AI models to users over WebRTC. Production latency targets land at 450–600ms end-to-end for premium stacks.

**Type:** Learn | **类型:** 学习
**Languages:** Python (stdlib) | **语言:** Python (标准库)
**Prerequisites:** Phase 14 · 01 (Agent Loop), Phase 14 · 12 (Workflow Patterns) | **前置知识:** 见原文
**Time:** ~60 minutes | **时间:** 见原文

## Learning Objectives | 学习目标

- Describe Pipecat's frame-based pipeline: DOWNSTREAM (source→sink) and UPSTREAM (control).
- Name the canonical voice pipeline stages and which transports Pipecat supports.
- Explain LiveKit Agents' two voice agent classes (MultimodalAgent, VoicePipelineAgent) and when each fits.
- Summarize 2026 production latency expectations and how they drive architecture choices.

## The Problem | 问题引入

Voice agents are not a text loop with TTS bolted on. Latency budgets are brutal (~600ms), partial audio is the default, turn detection is a model, and transports range from telephony SIP to WebRTC. Either you build a frame-based pipeline (Pipecat) or you lean on a platform (LiveKit).

> 语音 Agent 不是文本循环加上 TTS。延迟预算极其严苛（约 600ms），部分音频是默认状态，轮次检测是一个模型，传输方式从电话 SIP 到 WebRTC 不等。你要么构建一个基于帧的管道（Pipecat），要么依赖一个平台（LiveKit）。


> **【中文解读】** 语音 Agent 需要实时处理音频流——语音识别（ASR）、LLM 推理、语音合成（TTS）的延迟必须在 300ms 以内才能维持自然对话。Pipecat 和 LiveKit 提供了构建低延迟语音 Agent 的框架和基础设施。

> **{【拓展：Pipecat（开源框架）和 LiveKit（实时音频基础设施）是 2026 年语音 Agent 生...】}** Pipecat（开源框架）和 LiveKit（实时音频基础设施）是 2026 年语音 Agent 生态的核心。Pipecat 提供模块化的音频处理管道，支持多种 ASR/TTS/LLM 后端。LiveKit 提供 WebRTC 基础设施，确保低延迟音频传输。代表产品包括 Pi AI、ChatGPT Voice 和 Claude Voice。
## The Concept | 核心概念

### Pipecat (pipecat-ai/pipecat)

- Python frame-based pipeline framework.
- `Frame` → `FrameProcessor` chain.
- Two flow directions:
  - **DOWNSTREAM** — source → sink (audio in, TTS out).
  - **UPSTREAM** — feedback and control (cancellation, metrics, barge-in).
- `PipelineTask` manages lifecycle with events (`on_pipeline_started`, `on_pipeline_finished`, `on_idle_timeout`) and observers for metrics/tracing/RTVI.

Typical pipeline:

```
VAD (Silero) → STT → LLM (context alternates user/assistant) → TTS → transport
```

Transports: Daily, LiveKit, SmallWebRTCTransport, FastAPI WebSocket, WhatsApp.

> 语音 Agent 结合 LLM 和实时语音处理。Pipecat 和 LiveKit 是两种主要的语音 Agent 框架，分别处理音频管道和实时通信。

Pipecat Flows adds structured conversations (state machines). Pipecat Cloud is the managed runtime.

> 语音 Agent 结合 LLM 和实时语音处理。Pipecat 和 LiveKit 是两种主要的语音 Agent 框架，分别处理音频管道和实时通信。

### LiveKit Agents (livekit/agents)

- Bridges AI models to users over WebRTC.
- Key concepts: `Agent`, `AgentSession`, `entrypoint`, `AgentServer`.
- Two voice agent classes:
  - **MultimodalAgent** — direct audio via OpenAI Realtime or equivalent.
  - **VoicePipelineAgent** — STT → LLM → TTS cascade; gives text-level control.
- Semantic turn detection via a transformer model.
- Native MCP integration.
- Telephony via SIP.
- 50+ models with no API keys via LiveKit Inference; 200+ more via plugins.

### Commercial platforms

Vapi (~450–600ms on an optimized premium stack) and Retell (~600ms end-to-end across 180 test calls) build on top of these. Pick a platform when you want a managed voice stack without a WebRTC team.

> Vapi（优化后的高级堆栈约 450-600ms）和 Retell（180 次测试通话端到端约 600ms）构建在这些之上。当你想要一个托管语音堆栈而不需要 WebRTC 团队时，选择平台。

> 语音 Agent 结合 LLM 和实时语音处理。Pipecat 和 LiveKit 是两种主要的语音 Agent 框架，分别处理音频管道和实时通信。

### Where this pattern goes wrong

- **No barge-in handling.** User interrupts; agent keeps talking. Requires UPSTREAM cancel frames in Pipecat, equivalent in LiveKit.
- **STT confidence ignored.** Low-confidence transcripts fed to the LLM as if gospel. Gate on confidence or request confirmation.
- **TTS mid-sentence cutoff.** When the pipeline cancels mid-utterance, TTS needs to know or cut audio.
- **Latency budget ignored.** Every component adds 50–200ms. Sum your chain before shipping.

> **没有打断处理。** 用户打断；Agent 继续说话。需要 Pipecat 中的 UPSTREAM 取消帧，或 LiveKit 中的等效机制。
> **忽略 STT 置信度。** 低置信度转录被当作真理传给 LLM。根据置信度门控或请求确认。
> **TTS 句中截断。** 当管道在话语中间取消时，TTS 需要知道或截断音频。
> **忽略延迟预算。** 每个组件增加 50-200ms。在发布前计算你的链路总延迟。

### Typical 2026 latencies

- VAD: 20–60ms
- STT partial: 100–250ms
- LLM first token: 150–400ms
- TTS first audio: 100–200ms
- Transport RTT: 30–80ms

End-to-end 450–600ms is premium. 800–1200ms is common. Anything > 1500ms feels broken.

> 端到端 450-600ms 是高端水平。800-1200ms 是常见水平。超过 1500ms 感觉就会出问题。

> 语音 Agent 结合 LLM 和实时语音处理。Pipecat 和 LiveKit 是两种主要的语音 Agent 框架，分别处理音频管道和实时通信。

## Build It | 动手实现

`code/main.py` is a frame-based toy pipeline with:

> 语音 Agent 结合 LLM 和实时语音处理。Pipecat 和 LiveKit 是两种主要的语音 Agent 框架，分别处理音频管道和实时通信。

- `Frame` types (audio, transcript, text, tts_audio, control).
- `Processor` interface with `process(frame)`.
- A five-stage pipeline (VAD → STT → LLM → TTS → transport) as scripted processors.
- An UPSTREAM cancel frame to demonstrate barge-in.

Run it:

```
python3 code/main.py
```

The trace shows normal flow and a barge-in cancel that stops TTS mid-utterance.

> 追踪显示正常流程和一个在话语中间停止 TTS 的打断取消。

> 语音 Agent 结合 LLM 和实时语音处理。Pipecat 和 LiveKit 是两种主要的语音 Agent 框架，分别处理音频管道和实时通信。

## Use It | 用框架实现

- **Pipecat** for full control — custom processors, Python-first, pluggable providers.
- **LiveKit Agents** for WebRTC-first deployments and telephony.
- **Vapi / Retell** for hosted voice agents without a WebRTC team.
- **OpenAI Realtime / Gemini Live** for direct audio-in/audio-out (MultimodalAgent).

## Ship It | 产出物

`outputs/skill-voice-pipeline.md` scaffolds a Pipecat-shaped voice pipeline with VAD + STT + LLM + TTS + transport plus barge-in handling.

> `outputs/skill-voice-pipeline.md` 搭建一个 Pipecat 形态的语音管道，包含 VAD + STT + LLM + TTS + 传输以及打断处理。

> 语音 Agent 结合 LLM 和实时语音处理。Pipecat 和 LiveKit 是两种主要的语音 Agent 框架，分别处理音频管道和实时通信。

## Exercises | 练习题

1. Add a metrics observer to your toy pipeline: count frames per stage per second. Where does latency accumulate?
  中文翻译：思考并实践此练习。
2. Implement confidence-gated STT: below threshold, request "could you repeat that?"
  中文翻译：思考并实践此练习。
3. Add semantic turn detection: simple rule — if transcript ends with "?", end of turn.
  中文翻译：思考并实践此练习。
4. Read Pipecat's transport docs. Swap the stdlib transport for the SmallWebRTCTransport config (stub).
  中文翻译：思考并实践此练习。
5. Measure an OpenAI Realtime vs STT+LLM+TTS cascade on the same query. What latency cost does text-level control carry?
  中文翻译：思考并实践此练习。

## Key Terms | 术语速查表

| Term | What people say | What it actually means |
|------|----------------|------------------------|---|
| Frame | "Event" | Typed unit of data in the pipeline (audio, transcript, text, control) |  |
| Processor | "Pipeline stage" | Handler with process(frame) |  |
| DOWNSTREAM | "Forward flow" | Source to sink: audio in, speech out |  |
| UPSTREAM | "Feedback flow" | Control: cancel, metrics, barge-in |  |
| VAD | "Voice activity detection" | Detects when user is speaking |  |
| Semantic turn detection | "Smart end-of-turn" | Model-based decision that the user is done |  |
| MultimodalAgent | "Direct audio agent" | Audio in, audio out; no text in the middle |  |
| VoicePipelineAgent | "Cascade agent" | STT + LLM + TTS; text-level control |  |

## Further Reading | 延伸阅读

- [Pipecat docs](https://docs.pipecat.ai/getting-started/introduction) — frame-based pipeline, processors, transports
  中文翻译：见原文。
- [LiveKit Agents docs](https://docs.livekit.io/agents/) — WebRTC + voice primitives
  中文翻译：见原文。
- [Vapi](https://vapi.ai/) — managed voice platform
  中文翻译：见原文。
- [Retell AI](https://www.retellai.com/) — managed voice, latency-benchmarked
  中文翻译：见原文。
