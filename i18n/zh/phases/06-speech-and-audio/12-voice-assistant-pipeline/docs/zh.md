# 建设语音助手流水线 阶段 6 毕业项目

> 根据"一"课程,编织在一起. 建立一个听取,推理和回复的语音助理. 2026年,这是一个解决的工程问题,而不是一个研究问题.

> **【中文解读】**把01-11课程的所有内容串联起来,构建一个能听,能想,能说的语音助手.

**Type:** Build | **类型:** 构建
**Languages:** Python | **语言:** Python
**Prerequisites:** Phase 6 · 04, 05, 06, 07, 11; Phase 11 · 09 (Function Calling); Phase 14 · 01 (Agent Loop) | **前置知识:** 阶段 6 · 04、05、06、07、11；阶段 11 · 09（函数调用）；阶段 14 · 01（智能体循环）
**Time:** ~120 minutes | **预计用时:** ~120 分钟

## 问题 问题引入

建立一个端到端助理:

> 构建一个端到端助手:

> **【中文解读】**本节提出的问题是:如何在实际工程中正确理解和应用这一技术――理解问题背景有助于把握技术选择的关键决策点――在实际人工智能系统中,错误的技术选择往往比实现细节的错误成本更高――

1. 捕捉麦克风输入 (16 kHz单频).
   捕获麦克风输入(16kHz 单声道)
2. 检测用户语音的开始/结束.
   检测用户语音的开始/结束.
3. 转载了流媒体.
   流式转录.
4. 通过转录到可以调用工具的LLM (计时器,天气,日历).
   将转录传递给可调用工具 (定时器,天气,日历) 的LLM.
5. 传递法学士文本给一个TTS.
   将LLM 文本流式传输给TTS.
6. 播放音频回给用户.
   向用户播放音频──
7. 如果用户中途响应中断,则停止.
   如果用户在回应中打断则停止.

延迟目标:用户在笔记本电脑CPU上完成语音后800ms内首个TTS音频字节.质量目标:没有错过的字符,没有沉默的幻觉字幕,没有语音克隆泄漏,没有快速注射成功.

> 延迟目标:在笔记本CPU上用户说完话后800ms内发出第一个TTS 音频字节──质量目标:不漏词、静音不产生幻觉字幕、无声音克隆泄漏、提示注入不成功──

## 概念的核心概念

> **【中文解读】**本节介绍核心概念和理论基础.掌握这些概念是后续动手实现的前提,同时也是面试和工程实践中高频考察的知识点.


![Voice assistant pipeline: mic → VAD → STT → LLM+tools → TTS → speaker](../assets/voice-assistant.svg)

### 七个组成部分

1. **Audio capture.**微 → 16 kHz 单 → 20 ms 块. 通常`sounddevice`在Python或本土AudioUnit/ALSA/WASAPI中制作.
   **音频捕获。**麦克风 → 16 kHz 单声道 → 20 ms 块──Python 中通常使用 `sounddevice`产业环境用原生音频单位/ALSA/WASAPI。
2. **VAD (Lesson 11).**声,声,声,声,声,声,声,声,声,声,声,声,声,声,声,声,声,声,声,声,声,声,声,声,声,声,声,声,声,声,声,声,声,声,声.
   **VAD（第 11 课）。**静音持续500 ms──信号"开始"和"结束"──
3. **Streaming STT (Lesson 4-5).**微声流,Parakeet-TDT,或深度图 Nova-3 (API).部分+最终转录.
   **流式 STT（第 4-5 课）。**声流,子-TDT或深度图片Nova-3 (API) 部分+ 最终转录
4. **LLM with tool calling.**简单的方法是:
   **带工具调用的 LLM。**据悉,在此次的发布中,
5. **Streaming TTS (Lesson 7).**开启的时间是20个LLM代币后开始TTS.
   **流式 TTS（第 7 课）。**卡特西亚索尼克 (Kokoro-82M) 后启动了TTS.
6. **Playback.**低带宽网络的编码.
   **回放。**扬声器输出;低带宽网络用 opus编码.
7. **Interruption handler.**如果在TTS播放期间发生VAD火灾,停止播放,取消LLM,重新启动STT.
   **打断处理器。**如果在播放期间,VAD 触发,停止播放,取消LLM,重新启动STT.

### 你将击中的三个失败模式

> ### 你会遇到三种失败模式

1. **First-word clip.**升速度太晚了,用户的""没有,开始门为0.3,而不是0.5.
   **首词截断。**开始使用0.3而不是0.5的用户""丢失.
2. **Mid-response interrupt confusion.**接下来,在用户中断后,LLM继续生成;助理在用户之间谈话.
   **回应中打断混乱。**用户打断后LLM 继续生成;助手压过用户说话──连接 VAD → 取消LLM──
3. **Silence hallucination.**声在安静的加热上发出"谢谢你看的"
   **静音幻觉。**微笑 在静音预热上输出"谢谢你观看"――务必用 VAD 过──

### 2026生产参考堆

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

> **【中文解读】**本节通过代码实现从零到核心算法――这种"从零开始"的方式可以帮助理解框架背后的原理,遇到问题时不会被黑盒困住――

> **【拓展：语音 AI 的产品化】**语音技术在产品化中面临着独特的挑战:不同口音,背景噪音,远场拾音,多人说话等.

> **【拓展：多语言语音技术】**全球语言的语音特性差异巨大:声调语言的音高携带语义,低资源语言缺乏训练数据――Meta的MMS模型支持1000多种语言的语音识别,语在多语言场景表现出色,但仍然需要针对特定语言微调――

> **【拓展：语音隐私与安全】**语音数据包含大量个人隐私信息 (声纹、对话内容) ◦深度伪造 (Deepfake) 语音技术可被滥用作弊 (欺诈) 音频水印 (音频水印) ◎音纹反欺诈 (反欺诈) ◎反欺诈 (反欺诈) ◎是当前的研究热点.





## 建立它,实现它.
```figure
v4-voice-latency
```

## 建立它

### 步骤1:通过分块 (伪代码) 捕获微信

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

### 步骤2:VAD门转录

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

### 步骤3:播放STT →LLM →TTS

```python
async def turn(audio_bytes):
    transcript = await stt.transcribe(audio_bytes)
    async for token in llm.stream(transcript):
        async for audio in tts.stream(token):
            await speaker.play(audio)
```

### 步骤4:在LLM循环中调用工具

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

### 步骤5: 打断处理

> **【中文解读】**本节展示了如何使用成熟框架 (如PyTorch、HuggingFace等) 快速应用该技术.


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




> **【拓展：语音与情感计算】**语音不仅传递文字信息,还携带丰富的情感信号 (语调、语速、音高变化) 情感语音识别 (语音识别,语音情感识别,SER) 在客服质检,心理健康监测,智能教育等领域广泛应用.

## 用它实现框架

看到`code/main.py`对于一个可运行模拟,将所有七个组件都与模进行连接,以便即使没有硬件,也可以看到管道形状.

> 参见`code/main.py`获取可运行的模拟,将7个组件用模块连接,无需硬件即可看到流水线形状――实际实现时,将模块替换为:

- `silero-vad`(`pip install silero-vad`) / 模块
- `deepgram-sdk`或`openai-whisper`流式 STT
- `openai`(`gpt-4o`) 或`anthropic`/ LLM + 工具调用
- `kokoro`或`cartesia`流式 TTS
- `sounddevice`对于I/O/音频输入输出



## 陷

> 常见陷

- **Logging PII forever.**在大多数司法管辖区,全转音频是个人信息.
  **永久记录 PII。**完整轮次音频在大多数司法管辖区属于PII──30 天保留,静态加密──
- **No barge-in.**用户会打断,你的助理必须停止说话.
  **没有抢话。**用户会打断. 你的助手必须停止说话.
- **TTS that blocks.**通过同步的TTS,可以阻止事件循环.
  **阻塞式 TTS。**同步TTS 阻塞事件循环――使用异步或独立线程――
- **No tool-call error handling.**工具失败. 法律法师必须恢复错误,再尝试一次,然后优雅地降低.
  **没有工具调用错误处理。**工具会失败――LLM 必须收到错误 + 重试一次,然后优雅降级――
- **Overzealous hallucination filters.**过度过,助理说"我不能帮你",过下,它说任何东西.
  **过度激进的幻觉过滤。**过度过助手会重复"我帮不了"――过不足则什么都说――在留出集上校准――
- **No wake-word option.**总是倾听是隐私责任. 添加一个警觉门 (Porcupine或 openWakeWord).
  **没有唤醒词选项。**持续监听是隐私负担.

> **【中文解读】**本节关注如何将模型部署为可用的产品. 从原型到生产级系统需要考虑性能优化,错误处理,监控等多个维度.


## 运送它.

保存如`outputs/skill-voice-assistant-architect.md`鉴于预算+规模+语言+合规性限制, 制作完整的堆规格.

> 保存为`outputs/skill-voice-assistant-architect.md`△给定预算+规模+语言+合规约束,产出完整技术规格――

## 练习题

1. **Easy.**跑步`code/main.py`它模拟一个完整的转向端到端,
   **简单。**运行`code/main.py`△使用模块模拟一个完整的轮次端到端并打印各阶段延迟──
2. **Medium.**取代STT的片用一个现实的Whisper模型在预录音的`.wav`测量WER和端到端延迟.
   **中等。**在预录中`.wav`上用真实语 模型替换STT 模块――测量WER 和端到端延迟――
3. **Hard.**添加工具调用:实现 `get_weather`(任何API) 和`set_timer`通过工具引导LLM,并检查用户说"设置5分钟计时器"时,正确的函数会启动,口头回复会确认这一点.
   **困难。**添加工具调用:实现 `get_weather`任何一个 API`set_timer`通过工具路由 LLM,验证当用户说"设一个5分钟定时器"时正确的函数被调用.

> **【中文解读】**在团队协作中,统一术语定义可以避免大量沟通误解.


## 关键词 快速查找表

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

> **【中文解读】**延伸阅读提供了深入学习的高质量资源. 这些论文和教程是该领域的经典参考文献,适合需要深入了解的读者.


## 继续阅读 继续阅读

- [LiveKit — voice agent quickstart](https://docs.livekit.io/agents/)生产级参考.
  现场开户 语音智能体快速进入 生产级参考
- [Pipecat — voice agent examples](https://github.com/pipecat-ai/pipecat) 适合自动制作的框架.
  语音智能体示例DIY 友好框架。
- [OpenAI Realtime API](https://platform.openai.com/docs/guides/realtime)管理的语音母语路径.
  开放AI实时API托管的语音原生路径──
- [Kyutai Moshi](https://github.com/kyutai-labs/moshi) 完全双重参考 (课 15).
  九泰莫希全双工参考第15课)
- [Porcupine wake-word](https://picovoice.ai/products/porcupine/)警报关门.
  猪唤醒词唤醒词门控――
- [Anthropic — tool use guide](https://docs.anthropic.com/en/docs/build-with-claude/tool-use) 法学士职能调用.
  动态工具使用指南 LLM 函数调用。

> **【中文解读】**延伸阅读提供了深入学习的高质量资源,包括论文,教程和工具.

