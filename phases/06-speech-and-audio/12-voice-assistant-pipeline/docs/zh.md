# 构建语音助手流水线 — 阶段 6 毕业项目

> 把 01-11 课的所有内容串起来，构建一个能听、能想、能说的语音助手。2026 年这是一个已解决的工程问题（而非研究问题）——但集成细节决定产品能否上线。

> **【中文解读】** 把 01-11 课的所有内容串起来，构建一个能听、能想、能说的语音助手。2026 年这是一个已解决的工程问题（而非研究问题）——但集成细节决定产品能否上线。

**类型：** 构建
**语言：** Python
**前置条件：** 阶段 6 · 04、05、06、07、11；阶段 11 · 09（函数调用）；阶段 14 · 01（代理循环）
**时长：** 约 120 分钟

## 问题引入

构建一个端到端助手：

> **【中文解读】** 本节提出的问题是：如何在实际工程中正确理解和应用这一技术。理解问题背景有助于把握技术选型的关键决策点。在实际 AI 系统中，错误的技术选型往往比实现细节的 bug 代价更高。

1. 捕获麦克风输入（16 kHz 单声道）。
2. 检测用户语音的开始/结束。
3. 流式转录。
4. 将转录传给能调用工具（计时器、天气、日历）的 LLM。
5. 将 LLM 文本流式传给 TTS。
6. 将音频回放给用户。
7. 如果用户在回复中途打断则停止。

延迟目标：笔记本 CPU 上用户说完话后 800 ms 内出首个 TTS 音频字节。质量目标：不错过单词、静音上没有幻觉字幕、没有语音克隆泄漏、提示注入不成功。

## 核心概念

> **【中文解读】** 本节介绍核心概念和理论基础。掌握这些概念是后续动手实现的前提，同时也是面试和工程实践中高频考察的知识点。

![语音助手流水线：麦克风 -> VAD -> STT -> LLM+工具 -> TTS -> 扬声器](../assets/voice-assistant.svg)

### 七个组件

1. **音频捕获。** 麦克风 -> 16 kHz 单声道 -> 20 ms 块。通常 Python 用 `sounddevice`，生产环境用原生 AudioUnit/ALSA/WASAPI。
2. **VAD（第 11 课）。** Silero VAD @ 阈值 0.5，最小语音 250 ms，静音悬挂 500 ms。发出"开始"和"结束"信号。
3. **流式 STT（第 4-5 课）。** Whisper-streaming、Parakeet-TDT 或 Deepgram Nova-3（API）。部分 + 最终转录。
4. **带工具调用的 LLM。** GPT-4o / Claude 3.5 / Gemini 2.5 Flash。工具的 JSON schema。流式 token。
5. **流式 TTS（第 7 课）。** Kokoro-82M（最快开源）或 Cartesia Sonic（商业）。收到 20 个 LLM token 后开始 TTS。
6. **播放。** 扬声器输出；低带宽网络用 Opus 编码。
7. **中断处理器。** 如果 TTS 播放期间 VAD 触发，停止播放、取消 LLM、重启 STT。

### 你会遇到的三种失败模式

1. **首词截断。** VAD 晚了一拍启动。用户的"嘿"丢失。阈值从 0.3 开始，不是 0.5。
2. **中途回复中断混乱。** 用户打断后 LLM 继续生成；助手盖过用户。连接 VAD -> 取消 LLM。
3. **静音幻觉。** Whisper 在静默预热帧上输出"Thanks for watching"。始终 VAD 门控。

### 2026 生产参考栈

| 栈 | 延迟 | 许可 | 备注 |
|----|------|------|------|
| LiveKit + Deepgram + GPT-4o + Cartesia | 350-500 ms | 商业 API | 2026 行业默认 |
| Pipecat + Whisper-streaming + GPT-4o + Kokoro | 500-800 ms | 多数开源 | DIY 友好 |
| Moshi（全双工） | 200-300 ms | CC-BY 4.0 | 单一模型；不同架构，第 15 课 |
| Vapi / Retell（托管） | 300-500 ms | 商业 | 最快上线；有限定制 |
| Whisper.cpp + llama.cpp + Kokoro-ONNX | 离线 | 开源 | 隐私 / 边缘 |

> **【中文解读】** 本节通过代码从零实现核心算法。这种 "from scratch" 的方式能帮助理解框架背后的原理，遇到问题时不会被黑盒困住。

> **【拓展：语音 AI 的产品化】** 语音技术在产品化中面临独特挑战：不同口音、背景噪声、远场拾音、多人说话等。Siri、Alexa、小爱同学等产品都投入了大量工程优化来解决这些 "长尾问题"。实时性要求（<300ms 延迟）也是语音产品的核心指标。

> **【拓展：多语言语音技术】** 全球语言的语音特性差异巨大：声调语言（如中文）的音高携带语义，低资源语言缺乏训练数据。Meta 的 MMS 模型支持 1000+ 种语言的语音识别，Whisper 在多语言场景表现出色，但仍需针对特定语言微调。

> **【拓展：语音隐私与安全】** 语音数据包含大量个人隐私信息（声纹、对话内容）。深度伪造（Deepfake）语音技术可以被滥用于诈骗。音频水印（Audio Watermarking）和声纹反欺诈（Anti-spoofing）是当前的研究热点。

## 动手实现

### 步骤 1：带分块的麦克风捕获（伪代码）

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

### 步骤 2：VAD 门控的轮次捕获

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

### 步骤 3：流式 STT -> LLM -> TTS

```python
async def turn(audio_bytes):
    transcript = await stt.transcribe(audio_bytes)
    async for token in llm.stream(transcript):
        async for audio in tts.stream(token):
            await speaker.play(audio)
```

### 步骤 4：LLM 循环中的工具调用

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

### 步骤 5：中断处理

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

## 用框架实现

参见 `code/main.py`，其中包含一个可运行的模拟，将所有七个组件与桩模型连接起来，这样即使没有硬件你也可以看到流水线形状。对于真实实现，用以下替换桩：

- `silero-vad`（`pip install silero-vad`）
- `deepgram-sdk` 或 `openai-whisper`
- `openai`（`gpt-4o`）或 `anthropic`
- `kokoro` 或 `cartesia`
- `sounddevice` 用于 I/O

## 陷阱

- **永久记录 PII。** 完整轮次音频在大多数司法管辖区是 PII。30 天保留期，静态加密。
- **没有打断。** 用户会打断。你的助手必须能停嘴。
- **阻塞的 TTS。** 同步 TTS 阻塞事件循环。使用异步或单独线程。
- **没有工具调用错误处理。** 工具会失败。LLM 必须获得错误 + 重试一次，然后优雅降级。
- **过度激进的幻觉过滤。** 过度过滤导致助手重复"我无法帮助那个"。过滤不足让它什么都说。在留出集上校准。
- **没有唤醒词选项。** 始终监听是隐私责任。添加唤醒词门控（Porcupine 或 openWakeWord）。

> **【中文解读】** 本节关注如何将模型部署为可用的产品。从原型到生产级系统需要考虑性能优化、错误处理、监控等多个维度。

## 产出物

保存为 `outputs/skill-voice-assistant-architect.md`。给定预算 + 规模 + 语言 + 合规约束，产出完整栈规格。

## 练习题

1. **简单。** 运行 `code/main.py`。它用桩模块模拟一个完整的轮次并打印各阶段延迟。
2. **中等。** 用预录 `.wav` 上的真实 Whisper 替换 STT 桩。测量 WER 和端到端延迟。
3. **困难。** 添加工具调用：实现 `get_weather`（任意 API）和 `set_timer`。将 LLM 路由通过工具，验证当用户说"设置 5 分钟计时器"时正确的函数触发且语音回复确认。

> **【中文解读】** 术语表中的 "What people say" vs "What it actually means" 区分了日常口语和精确技术含义。在团队协作中，统一术语定义可以避免大量沟通误解。

## 术语速查表

| 术语 | 通俗说法 | 实际含义 |
|------|----------|----------|
| 轮次（Turn） | 用户+助手一个来回 | 一个 VAD 界定的用户语音 + 一个 LLM-TTS 回复。 |
| 打断（Barge-in） | 中断 | 助手说话时用户开口；助手停止。 |
| 唤醒词（Wake word） | "嘿助手" | 短关键词检测器；Porcupine、Snowboy、openWakeWord。 |
| 端点检测（End-pointing） | 轮次结束 | VAD + 最小静音决策，判断用户说完。 |
| 预滚动（Pre-roll） | 语音前缓冲 | 在 VAD 触发前保留 200-400 ms 音频以避免首词截断。 |
| 工具调用（Tool call） | 函数调用 | LLM 发出 JSON；运行时分发；结果在循环中回传。 |

> **【中文解读】** 延伸阅读提供了深入学习的高质量资源。这些论文和教程是该领域的经典参考文献，适合需要深入理解的读者。

## 延伸阅读

- [LiveKit — 语音代理快速入门](https://docs.livekit.io/agents/) —— 生产级参考。
- [Pipecat — 语音代理示例](https://github.com/pipecat-ai/pipecat) —— DIY 友好的框架。
- [OpenAI Realtime API](https://platform.openai.com/docs/guides/realtime) —— 托管的语音原生路径。
- [Kyutai Moshi](https://github.com/kyutai-labs/moshi) —— 全双工参考（第 15 课）。
- [Porcupine 唤醒词](https://picovoice.ai/products/porcupine/) —— 唤醒词门控。
- [Anthropic — 工具使用指南](https://docs.anthropic.com/en/docs/build-with-claude/tool-use) —— LLM 函数调用。

> **【中文解读】** 延伸阅读提供了深入学习的高质量资源，包括论文、教程和工具。建议按需选读，优先阅读标注为 "the critical read" 的核心论文。
