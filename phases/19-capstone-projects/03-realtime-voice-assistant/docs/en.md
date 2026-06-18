# Capstone 03 — Real-Time Voice Assistant (ASR to LLM to TTS) | 助手 结业 语音 LLM

> A voice agent that feels right has end-to-end latency under 800ms, knows when you have stopped talking, handles barge-in, and can call a tool without stalling. Retell, Vapi, LiveKit Agents, and Pipecat all hit this bar in 2026. They do it with the same shape: a streaming ASR, a turn-detector, a streaming LLM, and a streaming TTS, all wired through WebRTC with aggressive latency budgets at every hop. Build one, measure WER and MOS and false-cutoff rate, and run it under packet loss.

> **【中文解读】** 本节是综合项目——构建实时语音助手，整合语音识别、LLM 推理和语音合成。


**Type:** Capstone | **类型:** 综合项目
**Languages:** Python (agent + pipeline), TypeScript (web client) | **语言:** Python（Agent + 管道）, TypeScript（Web 客户端）
**Prerequisites:** Phase 6 (speech and audio), Phase 7 (transformers), Phase 11 (LLM engineering), Phase 13 (tools), Phase 14 (agents), Phase 17 (infrastructure)

> 🔗 **【前置】** 顶点项目 03 = 综合 Phase 6/7/11/13/14/17。实时语音助手（ASR→LLM→TTS）。
> 💡 **【类比】** 实时语音助手 = "开源版 GPT-4o"。2026 商业参考：Retell/Vapi/LiveKit/Pipecat。难点：端到端延迟 <800ms、知道用户何时说完、barge-in（打断）、工具调用不卡。架构：流式 ASR+turn-detector+流式 LLM+流式 TTS+WebRTC。参考 Phase 12·20 Thinker-Talker。指标：WER/MOS/误切断率。| **前置知识:** Phase 6（语音与音频）, Phase 7（Transformer）, Phase 11（LLM 工程）, Phase 13（工具）, Phase 14（Agent）, Phase 17（基础设施）
**Phases exercised:** P6 · P7 · P11 · P13 · P14 · P17 | **涉及阶段:** P6 · P7 · P11 · P13 · P14 · P17
**Time:** 30 hours | **时间:** 30 小时

## Problem | 问题引入

> **【中文解读】** 本节描述实时语音助手面临的技术挑战。2025-2026 年语音成为 AI UX 发展最快的品类，关键指标是端到端延迟 < 800ms。难点不仅在延迟，还在于交互体验：不能打断用户、不能被用户打断时出错、中断恢复、工具调用不阻塞音频、在移动网络抖动下生存。这不是三个 REST 调用的拼接，而是端到端流式管道。

> **【拓展：语音 AI 产品生态】** 2026 年主要语音 Agent 平台包括 Retell AI、Vapi.ai、LiveKit Agents 1.0、Pipecat 0.0.70。OpenAI Realtime API 和 Gemini 2.5 Live 提供集成式语音模型。ASR 领域 Deepgram Nova-3 以亚 300ms 首片延迟领先，开源方案 faster-whisper 可自托管。TTS 方面 Cartesia Sonic-2 首字节延迟最低（~200ms），ElevenLabs Flash v3 质量最优。单台 g5.xlarge GPU 服务器可支撑 50 路并发通话。

Voice has been the fastest-moving AI UX category of 2025-2026. The technical ceiling dropped each quarter. OpenAI Realtime API, Gemini 2.5 Live, Cartesia Sonic-2, ElevenLabs Flash v3, LiveKit Agents 1.0, and Pipecat 0.0.70 all put sub-800ms first-audio-out within reach. The bar is not latency alone. It is the interaction feel: not cutting the user off, not getting cut off, recovering from a mid-sentence interruption, calling a tool mid-conversation without stalling the audio, surviving jittery mobile networks.

> 语音是 2025-2026 年发展最快的 AI UX 品类。技术天花板每个季度都在降低。OpenAI Realtime API、Gemini 2.5 Live、Cartesia Sonic-2、ElevenLabs Flash v3、LiveKit Agents 1.0 和 Pipecat 0.0.70 都使亚 800ms 首音频输出成为可能。标准不仅是延迟，还有交互体验：不打断用户、不被打断、从句子中间的中断中恢复、在对话中调用工具而不阻塞音频、在抖动的移动网络中生存。

You cannot get there by stitching three REST calls. The architecture is pipelined streaming end to end. Build it and the failure modes become visible: a VAD tuned for phone audio firing on background TV, a turn-detector waiting for punctuation that never comes, a TTS that buffers 400ms before emitting. The capstone is to fix these one at a time under load and publish a latency-and-quality report.

> 你无法通过拼接三个 REST 调用来实现。架构是端到端的管道式流式传输。构建它后，失败模式变得可见：为电话音频调优的 VAD 在背景电视上触发、等待永远不来的标点符号的轮次检测器、在输出前缓冲 400ms 的 TTS。本结业项目是在负载下逐一修复这些问题并发布延迟和质量报告。

## Concept | 核心概念

> **【中文解读】** 语音助手管道包含五个流式阶段：音频输入（WebRTC）、ASR（Deepgram Nova-3 流式转写）、轮次检测（VAD + 转完判断模型）、LLM（流式 token 输出）、TTS（首 token 后 200ms 内流式音频输出）。三个横切关注点：Barge-in（用户打断时取消 TTS）、工具调用（侧通道执行不阻塞音频）、反压（丢包时提高 VAD 阈值）。

> **【拓展：VAD 与轮次检测】** Silero VAD v5 是 2026 年语音活动检测的默认选择，以 20ms 粒度判断语音/静音。但单纯 VAD 无法判断用户是否说完——LiveKit 的轮次检测器是小型 Transformer，读部分转写文本判断语义完整度。实测显示，500ms 静音 + 完整度评分 > 0.6 的组合策略可将误切断率控制在 3% 以下。WER（词错率）目标 < 8%（15dB SNR），MOS（语音质量评分）目标 > 4.2。

The pipeline has five streaming stages: **audio in** (WebRTC from browser or PSTN), **ASR** (streaming partial transcripts from Deepgram Nova-3 or faster-whisper), **turn detection** (VAD plus a small turn-detector model that reads partial transcripts for completion cues), **LLM** (streaming tokens as soon as the turn is judged complete), **TTS** (streaming audio out within ~200ms of the first LLM token).

> 管道有五个流式阶段：**音频输入**（来自浏览器或 PSTN 的 WebRTC）、**ASR**（来自 Deepgram Nova-3 或 faster-whisper 的流式部分转写）、**轮次检测**（VAD 加上读取部分转写以获取完成提示的小型轮次检测模型）、**LLM**（一旦轮次被判断为完成即流式输出 token）、**TTS**（在第一个 LLM token 后约 200ms 内流式输出音频）。

Three cross-cutting concerns. **Barge-in**: when the user starts speaking while the agent is speaking, the TTS cancels and the ASR picks up immediately. **Tool use**: mid-conversation function calls (weather, calendar) must run on a side channel without stalling the audio; the agent pre-fills an acknowledgement token ("one second...") if latency exceeds 300ms. **Backpressure**: under packet loss, partial transcripts are held, VAD raises the speech-gate threshold, and the agent avoids speaking over an unacknowledged message.

> 三个横切关注点。**Barge-in**：当用户在 Agent 说话时开始说话，TTS 取消并立即恢复 ASR。**工具使用**：对话中的函数调用（天气、日历）必须在侧通道上运行而不阻塞音频；如果延迟超过 300ms，Agent 预填一个确认 token（"稍等..."）。**反压**：在丢包情况下，部分转写被保留，VAD 提高语音门阈值，Agent 避免在未确认的消息上说话。

The measurement bar is quantitative. WER under 8% on the Hamming VAD benchmark at 15 dB SNR. First-audio-out p50 under 800ms on 100 measured calls. False-cutoff rate under 3%. MOS above 4.2 on TTS. 50 concurrent calls on a single g5.xlarge. These numbers are the deliverable.

> 测量标准是量化的。在 Hamming VAD 基准测试上 15 dB SNR 时 WER 低于 8%。100 次测量通话中首音频输出 p50 低于 800ms。误切断率低于 3%。TTS MOS 高于 4.2。单台 g5.xlarge 上 50 路并发通话。这些数字就是交付物。

## Architecture | 架构

```
browser / Twilio PSTN
        |
        v
   WebRTC / SIP edge
        |
        v
  LiveKit Agents 1.0  (or Pipecat 0.0.70)
        |
   +----+--------------+--------------+-----------------+
   |                   |              |                 |
   v                   v              v                 v
  ASR              VAD v5         turn-detector     side-channel
(Deepgram         (Silero)          (LiveKit)        tools
 Nova-3 /         speech-gate    completion score    (weather,
 Whisper-v3)      per 20ms        on partials        calendar)
   |                   |              |
   +--------+----------+--------------+
            v
        LLM (streaming)
     GPT-4o-realtime / Gemini 2.5 Flash /
     cascaded Claude Haiku 4.5
            |
            v
        TTS streaming
     Cartesia Sonic-2 / ElevenLabs Flash v3
            |
            v
     audio back to caller
            |
            v
   OpenTelemetry voice traces -> Langfuse
```

## Stack | 技术栈

- Transport: LiveKit Agents 1.0 (WebRTC) plus Twilio PSTN gateway; Pipecat 0.0.70 as the alternate framework
  中文翻译：Transport: LiveKit Agents 1.0 (WebRTC) plus Twilio PSTN gateway; Pipecat 0.0.70 as the alternate framework

> 中文翻译：Transport: LiveKit Agents 1.0 (WebRTC) plus Twilio PSTN gateway; Pipecat 0.0.70 as the alternate framework（翻译）

- ASR: Deepgram Nova-3 (streaming, sub-300ms first partial) or faster-whisper Whisper-v3-turbo self-hosted
  中文翻译：ASR: Deepgram Nova-3 (streaming, sub-300ms first partial) or faster-whisper Whisper-v3-turbo self-hosted

> 中文翻译：ASR: Deepgram Nova-3 (streaming, sub-300ms first partial) or faster-whisper Whisper-v3-turbo self-hosted（翻译）

- VAD: Silero VAD v5 plus the LiveKit turn-detector (small transformer that reads partial transcripts)
  中文翻译：VAD: Silero VAD v5 plus the LiveKit turn-detector (small transformer that reads partial transcripts)

> 中文翻译：VAD: Silero VAD v5 plus the LiveKit turn-detector (small transformer that reads partial transcripts)（翻译）

- LLM: OpenAI GPT-4o-realtime for tight integration, Gemini 2.5 Flash Live, or cascaded Claude Haiku 4.5 (streaming completions, separate audio path)
  中文翻译：LLM: OpenAI GPT-4o-realtime for tight integration, Gemini 2.5 Flash Live, or cascaded Claude Haiku 4.5 (streaming completions, separate audio path)
- TTS: Cartesia Sonic-2 (lowest first-byte), ElevenLabs Flash v3, or open-source Orpheus for self-host
  中文翻译：TTS: Cartesia Sonic-2 (lowest first-byte), ElevenLabs Flash v3, or open-source Orpheus for self-host

> 中文翻译：TTS: Cartesia Sonic-2 (lowest first-byte), ElevenLabs Flash v3, or open-source Orpheus for self-host（翻译）

- Tools: FastMCP side-channel for weather/calendar/booking; agent pre-emits filler if tool takes >300ms
  中文翻译：Tools: FastMCP side-channel for weather/calendar/booking; agent pre-emits filler if tool takes >300ms
- Observability: OpenTelemetry voice spans, Langfuse voice traces with audio replay
  中文翻译：Observability: OpenTelemetry voice spans, Langfuse voice traces with audio replay
- Deployment: single g5.xlarge (24GB VRAM) for self-hosted Whisper + Orpheus; hosted APIs for lowest latency
  中文翻译：Deployment: single g5.xlarge (24GB VRAM) for self-hosted Whisper + Orpheus; hosted APIs for lowest latency

> 中文翻译：Deployment: single g5.xlarge (24GB VRAM) for self-hosted Whisper + Orpheus; hosted APIs for lowest latency（翻译）


## Build It | 动手构建

> **【中文解读】** 构建分为 9 个阶段：WebRTC 会话建立、ASR 流式处理（20ms PCM 帧）、VAD 与轮次检测（500ms 静音 + 完整度 > 0.6）、LLM 流式输出、TTS 流式输出（首 chunk 200ms 内）、Barge-in 处理（取消 TTS + 丢弃 LLM 输出 + 重新启动 ASR）、工具侧通道（> 300ms 时发送填充语）、评估套件（100 路通话测 WER/误切断/延迟/MOS）、负载测试（单台 50 路并发）。

> **【拓展：SWE-bench 评估体系】** SWE-bench 是目前编码 Agent 最权威的评测基准，包含真实 GitHub issue 和对应 patch。SWE-bench Verified 子集经过人工验证，确保 issue 描述足够明确。2026 年排行榜上，排名靠前的系统 pass@1 在 60-80% 区间。衡量维度不仅看通过率，还包括每任务轮次、token 消耗和美元成本。mini-swe-agent 作为最简基线实现，通常作为对比起点。

1. **WebRTC session.** Stand up a LiveKit room and a web client that streams microphone audio. On the server, attach an agent worker that joins the room.
   中文翻译：1. **WebRTC session.** Stand up a LiveKit room and a web client that streams microphone audio. On the server, attach an agent worker that joins the room.

2. **ASR streaming.** Feed 20ms PCM frames to Deepgram Nova-3 (or faster-whisper on GPU). Subscribe to partial and final transcripts. Log per-partial latency.
   中文翻译：2. **ASR streaming.** Feed 20ms PCM frames to Deepgram Nova-3 (or faster-whisper on GPU). Subscribe to partial and final transcripts. Log per-partial latency.

3. **VAD and turn detector.** Run Silero VAD v5 on the frame stream. On speech-end event, fire the LiveKit turn-detector against the latest partial transcript. Only commit to "turn complete" when VAD says silence for 500ms and the turn-detector scores completion > 0.6.
   中文翻译：3. **VAD and turn detector.** Run Silero VAD v5 on the frame stream. On speech-end event, fire the LiveKit turn-detector against the latest partial transcript. Only commit to "turn complete" when VAD says silence for 500ms and the turn-detector scores completion > 0.6.

4. **LLM stream.** On turn complete, start the LLM call with the running conversation plus the final transcript. Stream tokens out. At the first token, hand off to TTS.
   中文翻译：4. **LLM stream.** On turn complete, start the LLM call with the running conversation plus the final transcript. Stream tokens out. At the first token, hand off to TTS.

5. **TTS stream.** Cartesia Sonic-2 streams audio chunks back. The first chunk must leave the server within 200ms of the first LLM token. Emit chunks to LiveKit room; client plays through WebRTC jitter buffer.
   中文翻译：5. **TTS stream.** Cartesia Sonic-2 streams audio chunks back. The first chunk must leave the server within 200ms of the first LLM token. Emit chunks to LiveKit room; client plays through WebRTC jitter buffer.

6. **Barge-in.** When VAD detects new user speech while TTS is playing, cancel the TTS stream immediately, drop the remaining LLM output, and re-arm the ASR. Publish a `tts_canceled` span.
   中文翻译：6. **Barge-in.** When VAD detects new user speech while TTS is playing, cancel the TTS stream immediately, drop the remaining LLM output, and re-arm the ASR. Publish a `tts_canceled` span.

7. **Tool side channel.** Register weather and calendar as function-calling tools. When invoked, fire the call concurrently; if it does not resolve within 300ms, have the LLM emit "one second, let me check" as a filler; resume once the tool returns.
   中文翻译：7. **Tool side channel.** Register weather and calendar as function-calling tools. When invoked, fire the call concurrently; if it does not resolve within 300ms, have the LLM emit "one second, let me check" as a filler; resume once the tool returns.

8. **Eval harness.** Record 100 calls. Compute WER (against a held-out transcript), false-cutoff rate (TTS cancelled while user was mid-sentence), first-audio-out p50, TTS MOS (human or NISQA), and a jitter-loss test (drop 3% of packets).
   中文翻译：8. **Eval harness.** Record 100 calls. Compute WER (against a held-out transcript), false-cutoff rate (TTS cancelled while user was mid-sentence), first-audio-out p50, TTS MOS (human or NISQA), and a jitter-loss test (drop 3% of packets).

9. **Load test.** Drive 50 concurrent calls on a single g5.xlarge with a synthetic caller. Measure sustained first-audio-out p95.
   中文翻译：9. **Load test.** Drive 50 concurrent calls on a single g5.xlarge with a synthetic caller. Measure sustained first-audio-out p95.

## Use It | 使用方法

```
caller: "what is the weather in tokyo tomorrow"
[asr  ] partial @280ms: "what is the"
[asr  ] partial @540ms: "what is the weather"
[turn ] completion score 0.82 at @820ms; commit
[llm  ] first token @960ms
[tool ] weather.tokyo tomorrow -> 68/52 partly cloudy @1140ms
[tts  ] first audio-out @1040ms: "Tokyo tomorrow will be partly cloudy..."
turn latency: 1040ms user-stop -> audio-out
```

## Ship It | 部署上线

`outputs/skill-voice-agent.md` is the deliverable. Given a domain (customer support, scheduling, or kiosk), it stands up a LiveKit agent with the ASR/VAD/LLM/TTS pipeline tuned to the measurement bar. Rubric:

> `outputs/skill-voice-agent.md` 是交付物。给定一个领域（客户支持、调度或自助终端），它搭建一个根据测量标准调优的带 ASR/VAD/LLM/TTS 管道的 LiveKit Agent。评分标准：

| Weight | Criterion | How it is measured |
| 权重 | 标准 | 如何衡量 |
|:-:|---|---|
| 25 | End-to-end latency | p50 first-audio-out under 800ms across 100 recorded calls |
| 25 | 端到端延迟 | 100 路记录通话中 p50 首音频输出低于 800ms |
| 20 | Turn-taking quality | False-cutoff rate under 3% on the Hamming VAD benchmark |
| 20 | 轮次交互质量 | Hamming VAD 基准测试上误切断率低于 3% |
| 20 | Tool-use correctness | Mid-conversation tool calls that return the right data without stalling audio |
| 20 | 工具使用正确性 | 对话中返回正确数据而不阻塞音频的工具调用 |
| 20 | Reliability under packet loss | WER and turn-taking stability with 3% packet drop injected |
| 20 | 丢包下的可靠性 | 注入 3% 丢包时的 WER 和轮次交互稳定性 |
| 15 | Eval harness completeness | Reproducible measurements with public config |
| 15 | 评估框架完整性 | 公开配置的可复现测量 |
| **100** | | |

## Exercises | 练习题

1. Swap Deepgram Nova-3 for faster-whisper v3 turbo on a g5.xlarge. Measure the latency and WER gap. Identify where CPU-vs-GPU decisions matter.
   中文翻译：将 Deepgram Nova-3 换为 g5.xlarge 上的 faster-whisper v3 turbo。测量延迟和 WER 差距。确定 CPU vs GPU 决策在何处重要。

> 中文翻译：将 Deepgram Nova-3 换为 g5.xlarge 上的 faster-whisper v3 turbo。测量延迟和 WER 差距。确定 CPU vs GPU 决策在何处重要。（翻译）


2. Add an interruption-arbitration policy: what does the agent do when the user barges in during a tool call? Compare three policies (hard cancel, finish-tool-then-stop, queue next turn).
   中文翻译：添加中断仲裁策略：当用户在工具调用期间打断时 Agent 怎么做？比较三种策略（硬取消、完成工具后停止、排队下一轮）。

> 中文翻译：添加中断仲裁策略：当用户在工具调用期间打断时 Agent 怎么做？比较三种策略（硬取消、完成工具后停止、排队下一轮）。（翻译）


3. Run an adversarial turn-detector test: give the user long pauses mid-sentence. Tune the VAD silence threshold and the turn-detector score threshold for lowest false-cutoff without blowing past 900ms.
   中文翻译：运行对抗性轮次检测器测试：给用户句子中间的长停顿。调优 VAD 静音阈值和轮次检测器分数阈值以获得最低误切断率，同时不超过 900ms。

4. Deploy the same agent on PSTN via Twilio. Compare PSTN first-audio-out to WebRTC. Explain the jitter-buffer and codec differences.
   中文翻译：通过 Twilio 在 PSTN 上部署同一 Agent。比较 PSTN 首音频输出与 WebRTC。解释 jitter buffer 和编解码器差异。

> 中文翻译：通过 Twilio 在 PSTN 上部署同一 Agent。比较 PSTN 首音频输出与 WebRTC。解释 jitter buffer 和编解码器差异。（翻译）


5. Add voice activity detection for non-English languages (Japanese, Spanish). Measure the Silero VAD v5 false-trigger rate versus language-specific fine-tunes.
   中文翻译：为非英语语言（日语、西班牙语）添加语音活动检测。测量 Silero VAD v5 误触发率与语言特定微调的对比。

> 中文翻译：为非英语语言（日语、西班牙语）添加语音活动检测。测量 Silero VAD v5 误触发率与语言特定微调的对比。（翻译）


## Key Terms | 术语速查表

| Term | What people say | What it actually means |
| 术语 | 通俗说法 | 实际含义 |
|------|-----------------|------------------------|
| Turn detection | "End of utterance" | Classifier that, given VAD silence and a partial transcript, decides the user is done speaking |
| 轮次检测 | "话语结束" | 给定 VAD 静音和部分转写，判断用户说完话的分类器 |
| Barge-in | "Interruption handling" | Canceling TTS mid-playback when VAD detects new user speech |
| 打断处理 | "中断处理" | VAD 检测到新用户语音时取消正在播放的 TTS |
| First-audio-out | "Latency" | Time from user stops speaking to the first audio packet leaving the server |
| 首音频输出 | "延迟" | 从用户停止说话到第一个音频包离开服务器的时间 |
| VAD | "Speech gate" | Model classifying audio frames as speech vs silence; Silero VAD v5 is the 2026 default |
| VAD | "语音门" | 将音频帧分类为语音或静音的模型；Silero VAD v5 是 2026 年默认选择 |
| Jitter buffer | "Audio smoothing" | Client-side buffer that holds packets briefly to absorb network variance |
| Jitter buffer | "音频平滑" | 客户端缓冲区，短暂保存数据包以吸收网络波动 |
| Filler | "Acknowledgment token" | Short phrase the agent emits to avoid silence when a tool is slow |
| 填充语 | "确认 token" | 工具响应慢时 Agent 发出的短句以避免沉默 |
| MOS | "Mean opinion score" | Perceptual speech quality rating; NISQA is the automated proxy |
| MOS | "平均意见评分" | 感知语音质量评分；NISQA 是自动化代理 |

## Further Reading | 延伸阅读

- [LiveKit Agents 1.0](https://github.com/livekit/agents) — reference WebRTC agent framework
  中文翻译：参考 WebRTC Agent 框架
- [Pipecat](https://github.com/pipecat-ai/pipecat) — alternate Python-first streaming agent framework
  中文翻译：备选的 Python 优先流式 Agent 框架
- [OpenAI Realtime API](https://platform.openai.com/docs/guides/realtime) — reference for integrated speech models
  中文翻译：集成语音模型的参考
- [Deepgram Nova-3 documentation](https://developers.deepgram.com/docs) — streaming ASR reference
  中文翻译：流式 ASR 参考
- [Silero VAD v5](https://github.com/snakers4/silero-vad) — VAD reference model
  中文翻译：VAD 参考模型
- [Cartesia Sonic-2](https://docs.cartesia.ai) — low-latency TTS reference
  中文翻译：低延迟 TTS 参考
- [Retell AI architecture](https://docs.retellai.com) — production voice agent architecture
  中文翻译：生产级语音 Agent 架构
- [Vapi.ai production stack](https://docs.vapi.ai) — alternate production reference
  中文翻译：备选的生产级参考
