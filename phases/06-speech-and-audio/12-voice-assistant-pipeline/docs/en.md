# Build a Voice Assistant Pipeline — The Phase 6 Capstone | 构建语音助手流水线 — 阶段 6 毕业项目

> Everything from lessons 01-11, stitched together. Build a voice assistant that listens, reasons, and talks back. In 2026 that is a solved engineering problem, not a research problem — but the integration details decide whether it ships.

> **【中文解读】** 把 01-11 课的所有内容串起来，构建一个能听、能想、能说的语音助手。2026 年这是一个已解决的工程问题（而非研究问题）——但集成细节决定产品能否上线。

**Type:** Build | **类型:** 构建
**Languages:** Python | **语言:** Python
**Prerequisites:** Phase 6 · 04, 05, 06, 07, 11; Phase 11 · 09 (Function Calling); Phase 14 · 01 (Agent Loop) | **前置知识:** 阶段 6 · 04、05、06、07、11；阶段 11 · 09（函数调用）；阶段 14 · 01（智能体循环）
**Time:** ~120 minutes | **预计用时:** ~120 分钟

## The Problem | 问题引入

Build an end-to-end assistant:

> 构建一个端到端助手：

> **【中文解读】** 本节提出的问题是：如何在实际工程中正确理解和应用这一技术。理解问题背景有助于把握技术选型的关键决策点。在实际 AI 系统中，错误的技术选型往往比实现细节的 bug 代价更高。

1. Captures mic input (16 kHz mono).
   捕获麦克风输入（16 kHz 单声道）。
2. Detects start/end of user speech.
   检测用户语音的开始/结束。
3. Transcribes streaming.
   流式转录。
4. Passes transcript to an LLM that can call tools (timer, weather, calendar).
   将转录传递给可调用工具（定时器、天气、日历）的 LLM。
5. Streams LLM text to a TTS.
   将 LLM 文本流式传输给 TTS。
6. Plays audio back to the user.
   向用户播放音频。
7. Stops if the user interrupts mid-response.
   如果用户在回应中打断则停止。

Latency target: first TTS audio byte within 800 ms of the user finishing their utterance on a laptop CPU. Quality target: no missed words, no hallucinated subtitles on silence, no voice cloning leakage, no prompt injection success.

> 延迟目标：在笔记本 CPU 上用户说完话后 800 ms 内发出第一个 TTS 音频字节。质量目标：不漏词、静音不产生幻觉字幕、无声音克隆泄漏、提示注入不成功。

## The Concept | 核心概念

> **【中文解读】** 本节介绍核心概念和理论基础。掌握这些概念是后续动手实现的前提，同时也是面试和工程实践中高频考察的知识点。


![Voice assistant pipeline: mic → VAD → STT → LLM+tools → TTS → speaker](../assets/voice-assistant.svg)

### The seven components

1. **Audio capture.** Mic → 16 kHz mono → 20 ms chunks. Usually `sounddevice` in Python or native AudioUnit/ALSA/WASAPI in production.
   **音频捕获。** 麦克风 → 16 kHz 单声道 → 20 ms 块。Python 中通常用 `sounddevice`，生产环境用原生 AudioUnit/ALSA/WASAPI。
2. **VAD (Lesson 11).** Silero VAD @ threshold 0.5, min speech 250 ms, silence hang-over 500 ms. Signals "start" and "end."
   **VAD（第 11 课）。** Silero VAD @ 阈值 0.5，最小语音 250 ms，静音持续 500 ms。信号"开始"和"结束"。
3. **Streaming STT (Lesson 4-5).** Whisper-streaming, Parakeet-TDT, or Deepgram Nova-3 (API). Partial + final transcripts.
   **流式 STT（第 4-5 课）。** Whisper-streaming、Parakeet-TDT 或 Deepgram Nova-3（API）。部分 + 最终转录。
4. **LLM with tool calling.** GPT-4o / Claude 3.5 / Gemini 2.5 Flash. JSON schema for tools. Stream tokens.
   **带工具调用的 LLM。** GPT-4o / Claude 3.5 / Gemini 2.5 Flash。工具的 JSON schema。流式 token。
5. **Streaming TTS (Lesson 7).** Kokoro-82M (fastest open) or Cartesia Sonic (commercial). Start TTS after 20 LLM tokens.
   **流式 TTS（第 7 课）。** Kokoro-82M（最快的开源）或 Cartesia Sonic（商业）。在 20 个 LLM token 后启动 TTS。
6. **Playback.** Speaker out; opus-encode for low-bandwidth networks.
   **回放。** 扬声器输出；低带宽网络用 opus 编码。
7. **Interruption handler.** If VAD fires during TTS playback, stop playback, cancel LLM, restart STT.
   **打断处理器。** 如果 TTS 播放期间 VAD 触发，停止播放、取消 LLM、重启 STT。

### The three failure modes you will hit

> ### 你会遇到的三种失败模式

1. **First-word clip.** VAD starts a beat too late. User's "hey" is missing. Start threshold at 0.3, not 0.5.
   **首词截断。** VAD 启动晚了一拍。用户的"嘿"丢失。起始阈值用 0.3 而非 0.5。
2. **Mid-response interrupt confusion.** LLM keeps generating after user interrupts; assistant talks over user. Wire VAD → cancel-LLM.
   **回应中打断混乱。** 用户打断后 LLM 继续生成；助手压过用户说话。连接 VAD → 取消 LLM。
3. **Silence hallucination.** Whisper outputs "Thanks for watching" on the silent warm-up frames. Always VAD-gate.
   **静音幻觉。** Whisper 在静音预热帧上输出"Thanks for watching"。务必用 VAD 过滤。

### 2026 production reference stacks

| Stack | Latency | License | Notes |
|-------|---------|---------|-------|
| LiveKit + Deepgram + GPT-4o + Cartesia | 350-500 ms | commercial API | Industry default 2026 |
| Pipecat + Whisper-streaming + GPT-4o + Kokoro | 500-800 ms | mostly open | DIY-friendly |
| Moshi (full-duplex) | 200-300 ms | CC-BY 4.0 | Single-model; different architecture, lesson 15 |
| Vapi / Retell (managed) | 300-500 ms | commercial | Fastest to launch; limited customization |
| Whisper.cpp + llama.cpp + Kokoro-ONNX | offline | open | Privacy / edge |

| 技术栈 | 延迟 | 许可 | 备注 |
|--------|------|------|------|
| LiveKit + Deepgram + GPT-4o + Cartesia | 350-500 ms | 商业 API | 2026 行业默认 |
| Pipecat + Whisper-streaming + GPT-4o + Kokoro | 500-800 ms | 多数开源 | DIY 友好 |
| Moshi（全双工） | 200-300 ms | CC-BY 4.0 | 单模型；不同架构，第 15 课 |
| Vapi / Retell（托管） | 300-500 ms | 商业 | 最快上线；定制有限 |
| Whisper.cpp + llama.cpp + Kokoro-ONNX | 离线 | 开源 | 隐私/边缘 |

> **【中文解读】** 本节通过代码从零实现核心算法。这种 "from scratch" 的方式能帮助理解框架背后的原理，遇到问题时不会被黑盒困住。

> **【拓展：语音 AI 的产品化】** 语音技术在产品化中面临独特挑战：不同口音、背景噪声、远场拾音、多人说话等。Siri、Alexa、小爱同学等产品都投入了大量工程优化来解决这些 "长尾问题"。实时性要求（<300ms 延迟）也是语音产品的核心指标。

> **【拓展：多语言语音技术】** 全球语言的语音特性差异巨大：声调语言（如中文）的音高携带语义，低资源语言缺乏训练数据。Meta 的 MMS 模型支持 1000+ 种语言的语音识别，Whisper 在多语言场景表现出色，但仍需针对特定语言微调。

> **【拓展：语音隐私与安全】** 语音数据包含大量个人隐私信息（声纹、对话内容）。深度伪造（Deepfake）语音技术可以被滥用于诈骗。音频水印（Audio Watermarking）和声纹反欺诈（Anti-spoofing）是当前的研究热点。





## Build It | 动手实现

### Step 1: mic capture with chunking (pseudocode)

```python
import sounddevice as sd

def mic_stream(chunk_ms=20, sr=16000):
    q = queue.Queue()
    def cb(indata, frames, time, status):
        q.put(indata.copy().flatten())
    with sd.InputStream(channels=1, samplerate=sr, blocksize=int(sr * chunk_ms/1000), callback=cb):
        while True:
            yield q.get()
```

### Step 2: VAD-gated turn capture

```python
def capture_turn(stream, vad, pre_roll_ms=300, silence_ms=500):
    buf, pre, triggered = [], collections.deque(maxlen=pre_roll_ms // 20), False
    silent = 0
    for chunk in stream:
        pre.append(chunk)
        if vad(chunk):
            if not triggered:
                buf = list(pre)
                triggered = True
            buf.append(chunk)
            silent = 0
        elif triggered:
            silent += 20
            buf.append(chunk)
            if silent >= silence_ms:
                return b"".join(buf)
```

### Step 3: streaming STT → LLM → TTS

```python
async def turn(audio_bytes):
    transcript = await stt.transcribe(audio_bytes)
    async for token in llm.stream(transcript):
        async for audio in tts.stream(token):
            await speaker.play(audio)
```

### Step 4: tool calling inside the LLM loop

```python
tools = [
    {"name": "get_weather", "parameters": {"location": "string"}},
    {"name": "set_timer", "parameters": {"seconds": "int"}},
]

async for chunk in llm.stream(user_text, tools=tools):
    if chunk.type == "tool_call":
        result = dispatch(chunk.name, chunk.args)
        continue_streaming(result)
    if chunk.type == "text":
        await tts.stream(chunk.text)
```

### Step 5: interruption handling

> **【中文解读】** 本节展示如何用成熟框架（如 PyTorch、HuggingFace 等）快速应用该技术。在实际项目中，优先使用经过验证的框架实现，可以减少 bug 并提高开发效率。


```python
tts_task = asyncio.create_task(tts_loop())
while True:
    chunk = await mic.get()
    if vad(chunk):
        tts_task.cancel()
        await speaker.stop()
        await new_turn()
        break
```




> **【拓展：语音与情感计算】** 语音不仅传递文字信息，还携带丰富的情感信号（语调、语速、音高变化）。情感语音识别（Speech Emotion Recognition, SER）在客服质检、心理健康监测、智能教育等领域有广泛应用。当前 SOTA 模型通常基于 wav2vec 2.0 或 HuBERT 等预训练模型微调。

## Use It | 用框架实现

See `code/main.py` for a runnable simulation that wires all seven components with stub models, so you can see the pipeline shape even without hardware. For a real implementation, swap stubs with:

> 参见 `code/main.py` 获取可运行的模拟，将七个组件用桩模块连接，无需硬件即可看到流水线形状。实际实现时，将桩模块替换为：

- `silero-vad` (`pip install silero-vad`) / VAD 模块
- `deepgram-sdk` or `openai-whisper` / 流式 STT
- `openai` (`gpt-4o`) or `anthropic` / LLM + 工具调用
- `kokoro` or `cartesia` / 流式 TTS
- `sounddevice` for I/O / 音频输入输出



## Pitfalls

> 常见陷阱

- **Logging PII forever.** Full-turn audio is PII in most jurisdictions. 30-day retention, encrypted at rest.
  **永久记录 PII。** 完整轮次音频在多数司法管辖区属于 PII。30 天保留，静态加密。
- **No barge-in.** Users will interrupt. Your assistant must stop talking.
  **没有抢话。** 用户会打断。你的助手必须停止说话。
- **TTS that blocks.** Synchronous TTS blocks the event loop. Use async or a separate thread.
  **阻塞式 TTS。** 同步 TTS 阻塞事件循环。使用异步或独立线程。
- **No tool-call error handling.** Tools fail. LLM must get back the error + retry once, then gracefully degrade.
  **没有工具调用错误处理。** 工具会失败。LLM 必须收到错误 + 重试一次，然后优雅降级。
- **Overzealous hallucination filters.** Over-filter and the assistant repeats "I can't help with that." Under-filter and it says anything. Calibrate on a held-out set.
  **过度激进的幻觉过滤。** 过度过滤助手会重复"我帮不了"。过滤不足则什么都说。在留出集上校准。
- **No wake-word option.** Always-listening is a privacy liability. Add a wake-word gate (Porcupine or openWakeWord).
  **没有唤醒词选项。** 持续监听是隐私负担。添加唤醒词门控（Porcupine 或 openWakeWord）。

> **【中文解读】** 本节关注如何将模型部署为可用的产品。从原型到生产级系统需要考虑性能优化、错误处理、监控等多个维度。


## Ship It | 产出物

Save as `outputs/skill-voice-assistant-architect.md`. Given budget + scale + language + compliance constraints, produce a full stack spec.

> 保存为 `outputs/skill-voice-assistant-architect.md`。给定预算 + 规模 + 语言 + 合规约束，产出完整技术栈规格。

## Exercises | 练习题

1. **Easy.** Run `code/main.py`. It simulates one full turn end-to-end with stub modules and prints per-stage latency.
   **简单。** 运行 `code/main.py`。用桩模块模拟一个完整轮次端到端并打印各阶段延迟。
2. **Medium.** Replace the STT stub with a real Whisper model on a pre-recorded `.wav`. Measure WER and end-to-end latency.
   **中等。** 在预录 `.wav` 上用真实 Whisper 模型替换 STT 桩模块。测量 WER 和端到端延迟。
3. **Hard.** Add tool calling: implement `get_weather` (any API) and `set_timer`. Route the LLM through the tools and verify that when the user says "set a 5 minute timer" the right function fires and the spoken reply confirms it.
   **困难。** 添加工具调用：实现 `get_weather`（任何 API）和 `set_timer`。通过工具路由 LLM，验证当用户说"设一个 5 分钟定时器"时正确的函数被调用。

> **【中文解读】** 术语表中的 "What people say" vs "What it actually means" 区分了日常口语和精确技术含义。在团队协作中，统一术语定义可以避免大量沟通误解。


## Key Terms | 术语速查表

| Term | What people say | What it actually means |
|------|-----------------|-----------------------|
| Turn | A user + assistant round-trip | One VAD-bounded user speech + one LLM-TTS response. |
| Barge-in | Interruption | User speaks while assistant talks; assistant stops. |
| Wake word | "Hey assistant" | Short keyword detector; Porcupine, Snowboy, openWakeWord. |
| End-pointing | Turn ending | VAD + min-silence decision that user has finished. |
| Pre-roll | Pre-speech buffer | Keep 200-400 ms of audio before VAD fires to avoid first-word clip. |
| Tool call | Function invocation | LLM emits JSON; runtime dispatches; result feeds back in-loop. |

| 术语 | 人们常说的 | 实际含义 |
|------|-----------|---------|
| 轮次 | 用户+助手一个来回 | 一次 VAD 界定的用户语音 + 一次 LLM-TTS 回应。 |
| 抢话 | 打断 | 助手说话时用户开口；助手停止。 |
| 唤醒词 | "嘿助手" | 短关键词检测器；Porcupine、Snowboy、openWakeWord。 |
| 端点检测 | 轮次结束 | VAD + 最小静音决策用户已说完。 |
| 预滚 | 语音前缓冲 | 在 VAD 触发前保留 200-400 ms 音频以避免首词截断。 |
| 工具调用 | 函数调用 | LLM 输出 JSON；运行时分发；结果在循环中反馈。 |

> **【中文解读】** 延伸阅读提供了深入学习的高质量资源。这些论文和教程是该领域的经典参考文献，适合需要深入理解的读者。


## Further Reading | 延伸阅读

- [LiveKit — voice agent quickstart](https://docs.livekit.io/agents/) — production-grade reference.
  LiveKit——语音智能体快速入门——生产级参考。
- [Pipecat — voice agent examples](https://github.com/pipecat-ai/pipecat) — DIY-friendly framework.
  Pipecat——语音智能体示例——DIY 友好框架。
- [OpenAI Realtime API](https://platform.openai.com/docs/guides/realtime) — the managed voice-native path.
  OpenAI Realtime API——托管的语音原生路径。
- [Kyutai Moshi](https://github.com/kyutai-labs/moshi) — full-duplex reference (Lesson 15).
  Kyutai Moshi——全双工参考（第 15 课）。
- [Porcupine wake-word](https://picovoice.ai/products/porcupine/) — wake-word gating.
  Porcupine 唤醒词——唤醒词门控。
- [Anthropic — tool use guide](https://docs.anthropic.com/en/docs/build-with-claude/tool-use) — LLM function calling.
  Anthropic——工具使用指南——LLM 函数调用。

> **【中文解读】** 延伸阅读提供了深入学习的高质量资源，包括论文、教程和工具。建议按需选读，优先阅读标注为 "the critical read" 的核心论文。

