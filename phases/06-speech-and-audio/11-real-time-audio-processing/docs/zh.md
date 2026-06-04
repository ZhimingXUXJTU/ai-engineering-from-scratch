# 实时音频处理

> 批处理流水线处理文件，实时流水线在下 20 毫秒到达之前处理完这 20 毫秒。每个对话式 AI、广播系统和电话机器人都在这个延迟预算上生死存亡。实时音频处理是语音 AI 落地的关键工程挑战。

> **【中文解读】** 批处理流水线处理文件，实时流水线在下 20 毫秒到达之前处理完这 20 毫秒。每个对话式 AI、广播系统和电话机器人都在这个延迟预算上生死存亡。实时音频处理是语音 AI 落地的关键工程挑战。

**类型：** 构建
**语言：** Python
**前置条件：** 阶段 6 · 02（频谱图），阶段 6 · 04（ASR），阶段 6 · 07（TTS）
**时长：** 约 75 分钟

## 问题引入

你想要一个有生命感的语音助手。人类对话轮次切换延迟约 230 ms（从静音到响应）。超过 500 ms 感觉机械；超过 1500 ms 感觉坏了。2026 年完整的**听 -> 理解 -> 回应 -> 说**循环的预算是：

> **【中文解读】** 本节提出的问题是：如何在实际工程中正确理解和应用这一技术。理解问题背景有助于把握技术选型的关键决策点。在实际 AI 系统中，错误的技术选型往往比实现细节的 bug 代价更高。

| 阶段 | 预算 |
|------|------|
| 麦克风 -> 缓冲 | 20 ms |
| VAD | 10 ms |
| ASR（流式） | 150 ms |
| LLM（首个 token） | 100 ms |
| TTS（首个块） | 100 ms |
| 渲染 -> 扬声器 | 20 ms |
| **总计** | **约 400 ms** |

Moshi（Kyutai，2024）实现了 200 ms 全双工。GPT-4o-realtime（2024）约 320 ms。2022 年的级联流水线交付 2500 ms。10 倍改进来自三种技术：(1) 全面流式化，(2) 带部分结果的异步流水线，(3) 可中断的生成。

## 核心概念

> **【中文解读】** 本节介绍核心概念和理论基础。掌握这些概念是后续动手实现的前提，同时也是面试和工程实践中高频考察的知识点。

![流式音频流水线：环形缓冲区、VAD 门控、中断](../assets/real-time.svg)

**帧 / 块 / 窗口。** 实时音频以固定大小的块流动。常见选择：20 ms（16 kHz 下 320 个采样点）。所有下游必须跟上这个节奏。

**环形缓冲区（Ring buffer）。** 固定大小的循环缓冲区。生产者线程写入新帧，消费者线程读取。防止热路径上的内存分配。大小约等于最大延迟 × 采样率；2 秒的 16 kHz 环形 = 32,000 个采样点。

**VAD（语音活动检测）。** 当没有人说话时门控下游工作。Silero VAD 4.0（2024）在 CPU 上每 30 ms 帧运行不到 1 ms。`webrtcvad` 是较老的替代品。

**流式 ASR。** 随音频到达发射部分转录的模型。Parakeet-CTC-0.6B 流式模式（NeMo，2024）在 320 ms 延迟下达到 2-5% WER。Whisper-Streaming（Machacek 等，2023）将近流式的 Whisper 分块，约 2 秒延迟。

**中断（Interruption）。** 当用户在助手说话时开口，你必须 (a) 检测到打断，(b) 停止 TTS，(c) 丢弃剩余的 LLM 输出。全部在 100 ms 内，否则用户感觉助手是聋子。

**WebRTC Opus 传输。** 20 ms 帧，48 kHz，自适应比特率 8-128 kbps。浏览器和移动端标准。LiveKit、Daily.co、Pion 是 2026 年构建语音应用的栈。

**抖动缓冲区（Jitter buffer）。** 网络包乱序 / 迟到到达。抖动缓冲区重新排序和平滑；太小 -> 可听间隙，太大 -> 延迟。典型值 60-80 ms。

### 常见坑

- **线程竞争。** Python 的 GIL + 重模型会饿死音频线程。使用 C 回调音频库（sounddevice、PortAudio）并让 Python 远离热路径。
- **采样率转换延迟。** 流水线内重采样增加 5-20 ms。要么预先重采样，要么使用零延迟重采样器（PolyPhase、`soxr_hq`）。
- **TTS 预热。** 即使是快速 TTS 如 Kokoro 首次请求也有 100-200 ms 预热。缓存模型 + 在首次真正轮次前用空运行预热。
- **回声消除。** 没有 AEC，TTS 输出重新进入麦克风并触发 ASR 对机器人自己声音的识别。WebRTC AEC3 是开源默认。

> **【中文解读】** 本节通过代码从零实现核心算法。这种 "from scratch" 的方式能帮助理解框架背后的原理，遇到问题时不会被黑盒困住。

> **【拓展：语音 AI 的产品化】** 语音技术在产品化中面临独特挑战：不同口音、背景噪声、远场拾音、多人说话等。Siri、Alexa、小爱同学等产品都投入了大量工程优化来解决这些 "长尾问题"。实时性要求（<300ms 延迟）也是语音产品的核心指标。

> **【拓展：多语言语音技术】** 全球语言的语音特性差异巨大：声调语言（如中文）的音高携带语义，低资源语言缺乏训练数据。Meta 的 MMS 模型支持 1000+ 种语言的语音识别，Whisper 在多语言场景表现出色，但仍需针对特定语言微调。

> **【拓展：语音隐私与安全】** 语音数据包含大量个人隐私信息（声纹、对话内容）。深度伪造（Deepfake）语音技术可以被滥用于诈骗。音频水印（Audio Watermarking）和声纹反欺诈（Anti-spoofing）是当前的研究热点。

## 动手实现

### 步骤 1：环形缓冲区

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

容量决定最大缓冲延迟。16 kHz 下 32,000 个采样点 = 2 秒。

### 步骤 2：VAD 门控

```python
def simple_energy_vad(frame, threshold=0.01):
    return sum(x * x for x in frame) / len(frame) > threshold ** 2
```

生产环境用 Silero VAD：

```python
import torch
vad, _ = torch.hub.load("snakers4/silero-vad", "silero_vad")
is_speech = vad(torch.tensor(frame), 16000).item() > 0.5
```

### 步骤 3：流式 ASR

```python
# 通过 NeMo 的 Parakeet-CTC-0.6B 流式
from nemo.collections.asr.models import EncDecCTCModelBPE
asr = EncDecCTCModelBPE.from_pretrained("nvidia/parakeet-ctc-0.6b")
# chunk_ms=320 ms, look_ahead_ms=80 ms
for chunk in audio_stream():
    partial_text = asr.transcribe_streaming(chunk)
    print(partial_text, end="\r")
```

### 步骤 4：中断处理

```python
class Dialog:
    def __init__(self):
        self.tts_task = None

    def on_user_speech(self, frame):
        if self.tts_task and not self.tts_task.done():
            self.tts_task.cancel()   # 打断
        # 然后喂给流式 ASR

    def on_final_user_utterance(self, text):
        self.tts_task = asyncio.create_task(self.reply(text))

    async def reply(self, text):
        async for tts_chunk in llm_then_tts(text):
            speaker.write(tts_chunk)
```

> **【中文解读】** 本节展示如何用成熟框架（如 PyTorch、HuggingFace 等）快速应用该技术。在实际项目中，优先使用经过验证的框架实现，可以减少 bug 并提高开发效率。

核心依赖异步 I/O 和可取消的 TTS 流式。WebRTC peerconnection.stop() 在音频轨道上是标准方式。

> **【拓展：语音与情感计算】** 语音不仅传递文字信息，还携带丰富的情感信号（语调、语速、音高变化）。情感语音识别（Speech Emotion Recognition, SER）在客服质检、心理健康监测、智能教育等领域有广泛应用。当前 SOTA 模型通常基于 wav2vec 2.0 或 HuBERT 等预训练模型微调。

## 用框架实现

2026 年的技术栈：

| 层 | 选择 |
|----|------|
| 传输 | LiveKit（WebRTC）或 Pion（Go） |
| VAD | Silero VAD 4.0 |
| 流式 ASR | Parakeet-CTC-0.6B 或 Whisper-Streaming |
| LLM 首 token | Groq、Cerebras、vLLM-streaming |
| 流式 TTS | Kokoro 或 ElevenLabs Turbo v2.5 |
| 回声消除 | WebRTC AEC3 |
| 端到端原生 | OpenAI Realtime API 或 Moshi |

## 陷阱

- **缓冲 500 ms"以防万一"。** 缓冲区就是你的延迟下限。缩小它。
- **没有固定线程。** 音频回调在优先级低于 UI 的线程上 = 负载下出现故障。
- **TTS 块太小。** 小于 200 ms 的块使声码器伪影可听。320 ms 块是最佳点。
- **没有抖动缓冲区。** 真实网络有抖动；不平滑会出爆音。
- **单次错误处理。** 音频流水线必须抗崩溃。一个异常就杀死会话。

> **【中文解读】** 本节关注如何将模型部署为可用的产品。从原型到生产级系统需要考虑性能优化、错误处理、监控等多个维度。

## 产出物

保存为 `outputs/skill-realtime-designer.md`。设计一个实时音频流水线，每个阶段有具体的延迟预算。

## 练习题

1. **简单。** 运行 `code/main.py`。模拟环形缓冲区 + 能量 VAD；打印假 10 秒流的各阶段延迟。
2. **中等。** 使用 `sounddevice`，构建一个直通循环，以 20 ms 帧处理你的麦克风并在每帧打印 VAD 状态。
3. **困难。** 用 `aiortc` 构建全双工回声测试：浏览器 -> WebRTC -> Python -> WebRTC -> 浏览器。用 1 kHz 脉冲测量端到端延迟。

> **【中文解读】** 术语表中的 "What people say" vs "What it actually means" 区分了日常口语和精确技术含义。在团队协作中，统一术语定义可以避免大量沟通误解。

## 术语速查表

| 术语 | 通俗说法 | 实际含义 |
|------|----------|----------|
| 环形缓冲区 | 循环队列 | 固定大小、无锁（或 SPSC 锁）的音频帧 FIFO。 |
| VAD | 静音门 | 标记语音 vs 非语音的模型或启发式。 |
| 流式 ASR | 实时 STT | 随音频到达发射部分文本；有界前瞻。 |
| 抖动缓冲区 | 网络平滑器 | 重排乱序包的队列；典型值 60-80 ms。 |
| AEC | 回声消除 | 减去扬声器到麦克风的反馈路径。 |
| 打断（Barge-in） | 用户中断 | 系统在 TTS 中途检测到用户说话；必须取消播放。 |
| 全双工（Full duplex） | 双向同时 | 用户和机器人可以同时说话；Moshi 是全双工。 |

> **【中文解读】** 延伸阅读提供了深入学习的高质量资源。这些论文和教程是该领域的经典参考文献，适合需要深入理解的读者。

## 延伸阅读

- [Machacek et al. (2023). Whisper-Streaming](https://arxiv.org/abs/2307.14743) —— 分块近流式 Whisper。
- [Kyutai (2024). Moshi](https://kyutai.org/Moshi.pdf) —— 全双工 200 ms 延迟。
- [LiveKit Agents 框架（2024）](https://docs.livekit.io/agents/) —— 生产级音频代理编排。
- [Silero VAD 仓库](https://github.com/snakers4/silero-vad) —— 亚毫秒 VAD，Apache 2.0。
- [WebRTC AEC3 论文](https://webrtc.googlesource.com/src/+/main/modules/audio_processing/aec3/) —— 开源回声消除。

> **【中文解读】** 延伸阅读提供了深入学习的高质量资源，包括论文、教程和工具。建议按需选读，优先阅读标注为 "the critical read" 的核心论文。
