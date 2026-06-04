# PipeCat LiveKit Agent 语音

> Voice agents are a first-class production category in 2026. Pipecat gives you a Python frame-based pipeline (VAD → STT → LLM → TTS → transport). LiveKit Agents bridges AI models to users over WebRTC. Production latency targets land at 450–600ms end-to-end for premium stacks.


**类型：** 学习
**语言：** Python (stdlib)
**前置条件：** Phase 14 · 01 (Agent Loop), Phase 14 · 12 (Workflow Patterns)
**预计时间：** ~60 minutes

## 学习目标

- Describe Pipecat's frame-based pipeline: DOWNSTREAM (source→sink) and UPSTREAM (control).
- Name the canonical voice pipeline stages and which transports Pipecat supports.
- Explain LiveKit Agents' two voice agent classes (MultimodalAgent, VoicePipelineAgent) and when each fits.
- Summarize 2026 production latency expectations and how they drive architecture choices.

## 问题引入

> **【中文解读】** 语音 Agent 需要实时处理音频流——语音识别（ASR）、LLM 推理、语音合成（TTS）的延迟必须在 300ms 以内才能维持自然对话。Pipecat 和 LiveKit 提供了构建低延迟语音 Agent 的框架和基础设施。
> **【拓展：Pipecat（开源框架）和 LiveKit（实时音频基础设施）是 2026 年语音 Agent 生...】** Pipecat（开源框架）和 LiveKit（实时音频基础设施）是 2026 年语音 Agent 生态的核心。Pipecat 提供模块化的音频处理管道，支持多种 ASR/TTS/LLM 后端。LiveKit 提供 WebRTC 基础设施，确保低延迟音频传输。代表产品包括 Pi AI、ChatGPT Voice 和 Claude Voice。

## 核心概念

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
Pipecat Flows adds structured conversations (state machines). Pipecat Cloud is the managed runtime.
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
### Where this pattern goes wrong
- **No barge-in handling.** User interrupts; agent keeps talking. Requires UPSTREAM cancel frames in Pipecat, equivalent in LiveKit.
- **STT confidence ignored.** Low-confidence transcripts fed to the LLM as if gospel. Gate on confidence or request confirmation.
- **TTS mid-sentence cutoff.** When the pipeline cancels mid-utterance, TTS needs to know or cut audio.
- **Latency budget ignored.** Every component adds 50–200ms. Sum your chain before shipping.
### Typical 2026 latencies
- VAD: 20–60ms
- STT partial: 100–250ms
- LLM first token: 150–400ms
- TTS first audio: 100–200ms
- Transport RTT: 30–80ms
End-to-end 450–600ms is premium. 800–1200ms is common. Anything > 1500ms feels broken.

## 动手实现

`code/main.py` is a frame-based toy pipeline with:
- `Frame` types (audio, transcript, text, tts_audio, control).
- `Processor` interface with `process(frame)`.
- A five-stage pipeline (VAD → STT → LLM → TTS → transport) as scripted processors.
- An UPSTREAM cancel frame to demonstrate barge-in.
Run it:
```
python3 code/main.py
```
The trace shows normal flow and a barge-in cancel that stops TTS mid-utterance.

## 用框架实现

- **Pipecat** for full control — custom processors, Python-first, pluggable providers.
- **LiveKit Agents** for WebRTC-first deployments and telephony.
- **Vapi / Retell** for hosted voice agents without a WebRTC team.
- **OpenAI Realtime / Gemini Live** for direct audio-in/audio-out (MultimodalAgent).

## 产出物

`outputs/skill-voice-pipeline.md` scaffolds a Pipecat-shaped voice pipeline with VAD + STT + LLM + TTS + transport plus barge-in handling.

## 练习题

1. Add a metrics observer to your toy pipeline: count frames per stage per second. Where does latency accumulate?
   *思考并实践此练习*
2. Implement confidence-gated STT: below threshold, request "could you repeat that?"
   *思考并实践此练习*
3. Add semantic turn detection: simple rule — if transcript ends with "?", end of turn.
   *思考并实践此练习*
4. Read Pipecat's transport docs. Swap the stdlib transport for the SmallWebRTCTransport config (stub).
   *思考并实践此练习*
5. Measure an OpenAI Realtime vs STT+LLM+TTS cascade on the same query. What latency cost does text-level control carry?
   *思考并实践此练习*

## 术语速查表

| 术语 | 实际含义 |
|------|---------|
| Frame | "Event" |
| Processor | "Pipeline stage" |
| DOWNSTREAM | "Forward flow" |
| UPSTREAM | "Feedback flow" |
| VAD | "Voice activity detection" |
| Semantic turn detection | "Smart end-of-turn" |
| MultimodalAgent | "Direct audio agent" |
| VoicePipelineAgent | "Cascade agent" |

## 延伸阅读

