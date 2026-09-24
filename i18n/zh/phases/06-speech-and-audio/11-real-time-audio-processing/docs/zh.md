# 实时音频处理

> 批量管道处理一个文件. 实时管道处理下20毫秒前,下20毫秒到来. 每个对话人工智能,广播工作室和电话机器人都以这个延迟预算生活和死亡.

> **【中文解读】**批量处理流水线处理文件,实时流水线在下20毫秒到达之前处理完整的20毫秒. 每个对话式AI、广播系统和电话机器人都在这个延迟预算中存活着.

**Type:** Build | **类型:** 构建
**Languages:** Python | **语言:** Python
**Prerequisites:** Phase 6 · 02 (Spectrograms), Phase 6 · 04 (ASR), Phase 6 · 07 (TTS) | **前置知识:** 阶段 6 · 02（频谱图），阶段 6 · 04（ASR），阶段 6 · 07（TTS）
**Time:** ~75 minutes | **预计用时:** ~75 分钟

## 问题 问题引入

您想要一个感觉活跃的语音助理. 人类对话转换延迟约230ms (沉默回应).500ms以上的任何东西都感觉机器人;1500ms以上的东西感觉破碎.**hear → understand → respond → speak**2026年循环是:

> 你想要一个"活的"语音助手――人类对话轮次延迟约230 ms(静音到回应)――超过500 ms 感觉像机器人;超过1500 ms 感觉坏了――2026年完整**听 → 理解 → 回应 → 说**循环预算是:

> **【中文解读】**本节提出的问题是:如何在实际工程中正确理解和应用这一技术――理解问题背景有助于把握技术选择的关键决策点――在实际人工智能系统中,错误的技术选择往往比实现细节的错误成本更高――

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

莫希 (九台,2024) 完成了200 ms的全双重时钟.GPT-4o实时 (2024) 钟~320 ms. 2022 年的管道以 2500 ms 运输. 10 倍的改进来自三个技术: (1) 流通到处, (2) 有部分结果的异步管道, (3) 可断断的生成.

> 莫希·九台,2024实现了200 ms 全双工――GPT-4o实时――2024) 约320 ms──2022年级联流水线延迟 2500 ms──10倍提升来自三个技术:

## 概念的核心概念

> **【中文解读】**本节介绍核心概念和理论基础.掌握这些概念是后续动手实现的前提,同时也是面试和工程实践中高频考察的知识点.


![Streaming audio pipeline with ring buffer, VAD gate, interruption](../assets/real-time.svg)

**Frame / chunk / window.**现实时间音频流动是固定尺寸的块. 常见选择:20 ms (320 个样本在 16 kHz). 下游的所有东西都必须跟上这个节奏.

> **帧/块/窗口。**实时音频以固定大小的块流动──常见选择:20 ms(16 kHz 下 320 采样点)──下游一切都必须跟上这个节奏──

**Ring buffer.**固体尺寸圆形缓冲器.生产线写出新的框架,消费线阅读.防止在热路中的分配. 尺寸≈最大延迟 ×样品速率; 2 秒 16 kHz 环 = 32,000 样品.

> **环形缓冲区。**固定大小的循环缓冲区──生产者线程写入新,消费者线程读取──防止热路内存分配──大小约等于最大延迟 × 采样率;2秒16kHz 环形缓冲 = 32,000采样点──

**VAD (Voice Activity Detection).**通过"Silero VAD 4.0 (2024) "在CPU上运行每30ms的框架. `webrtcvad`现在,我们需要一个更好的选择.

> **VAD（语音活动检测）。**无人说话时阻止下游工作──Silero VAD 4.0(2024) 在CPU上每30ms运行 <1ms──`webrtcvad`是一个更老的替代方案.

**Streaming ASR.**通过传输方式 (NeMo, 2024) 发射部分转录的模型. 子-CTC-0.6B 在流媒体模式下 (NeMo, 2024) 在 320 ms 延迟时实现25% WER. 声流 (Macháček等, 2023) 块 Whisper 在 ~ 2 秒的延迟时进行近流.

> **流式 ASR。**随频到达而输出部分转录的模型――鱼-CTC-0.6B流式模式(NeMo,2024) 在 320 ms 延迟下实现 2-5% WER――声流程(Macháček等,2023) 将声分块实现接近流式的约2秒延迟――

**Interruption.**当用户在助理在说话时,你必须 (a) 检测到入, (b) 停止TTS, (c) 丢弃剩余的LLM输出.所有这些都在100ms内,否则用户会感知助理是聋的.

> **打断。**当助手在说话时用户开口,你必须 (a) 检测到抢话, (b) 停止TTS, (c) 丢弃剩余的LLM输出.

**WebRTC Opus transport.**浏览器和移动设备的标准. 莱夫基特,日报.co,皮昂是2026年建立语音应用程序的堆.

> **WebRTC Opus 传输。**20 ms ,48 kHz,自适应比特率 8-128 kbps──浏览器和移动端标准──LiveKit、Daily.co、Pion 是2026年构建语音应用技术──

**Jitter buffer.**网络包裹到达时间已过时. 节缓冲器重新排序和平滑; 太小 → 听力间隙,太大 → 延迟. 典型的6080 ms.

> **抖动缓冲区。**网络包乱序/迟到到达──动缓冲区重排和平滑;太小 → 可听间隙,太大 → 延迟──典型值 60-80 ms──

### 常见的

> ### 常见陷

- **Thread contention.**通过使用C-callback音频库 (音频设备,PortAudio) 让Python远离热线.
  **线程竞争。**字符串的GIL + 重模型会使音频线程饥饿──使用C 回调音频库(音响设备、PortAudio),让字符串远离热路径──
- **Sample-rate conversion latency.**输入管道内重新样本增加520ms.`soxr_hq`)
  **采样率转换延迟。**流水线内部重采采集增加5-20 ms──要么提前重采采集,要么使用零延迟重采采集器──
- **TTS priming.**即使像Kokoro这样的快速TTS也可以在第一次请求时加热100200ms.缓存模型+在第一次真正转之前用模拟运行加热.
  **TTS 预热。**即使像Kokoro这样的快速TTS在第一次请求时也有100-200 ms预热――缓存模型+在第一个真实轮次前使用假运行预热――
- **Echo cancellation.**没有AEC,TTS输出重新进入麦克风,并触发机器人自己的声音上的ASR.WebRTC AEC3是开源默认的.
  **回声消除。**没有AEC,TTS 输出重新进入麦克风并触发ASR 识别机器人自己的声音――WebRTC AEC3是开源默认方案――

> **【中文解读】**本节通过代码实现从零到核心算法――这种"从零开始"的方式可以帮助理解框架背后的原理,遇到问题时不会被黑盒困住――

> **【拓展：语音 AI 的产品化】**语音技术在产品化中面临着独特的挑战:不同口音,背景噪音,远场拾音,多人说话等.

> **【拓展：多语言语音技术】**全球语言的语音特性差异巨大:声调语言的音高携带语义,低资源语言缺乏训练数据――Meta的MMS模型支持1000多种语言的语音识别,语在多语言场景表现出色,但仍然需要针对特定语言微调――

> **【拓展：语音隐私与安全】**语音数据包含大量个人隐私信息 (声纹、对话内容) ◦深度伪造 (Deepfake) 语音技术可被滥用作弊 (欺诈) 音频水印 (音频水印) ◎音纹反欺诈 (反欺诈) ◎反欺诈 (反欺诈) ◎是当前的研究热点.





## 建立它,实现它.
```figure
nyquist-aliasing
```

## 建立它

### 步骤1:环保器

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

容量决定了最大缓冲延迟.

### 步骤2:VAD门

```python
def simple_energy_vad(frame, threshold=0.01):
    return sum(x * x for x in frame) / len(frame) > threshold ** 2
```

在生产中用Silero VAD取代:

```python
import torch
vad, _ = torch.hub.load("snakers4/silero-vad", "silero_vad")
is_speech = vad(torch.tensor(frame), 16000).item() > 0.5
```

### 步骤3: 流媒体ASR

```python
# Parakeet-CTC-0.6B streaming via NeMo
from nemo.collections.asr.models import EncDecCTCModelBPE
asr = EncDecCTCModelBPE.from_pretrained("nvidia/parakeet-ctc-0.6b")
# chunk_ms=320 ms, look_ahead_ms=80 ms
for chunk in audio_stream():
    partial_text = asr.transcribe_streaming(chunk)
    print(partial_text, end="\r")
```

### 步骤4: 断路处理器

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

> **【中文解读】**本节展示了如何使用成熟框架 (如PyTorch、HuggingFace等) 快速应用该技术.


网络网络同行连接.停止() 在音频轨道是正规的方式.

> 根据不同步骤的 I/O 和可取消的 TTS 流式传输――WebRTC 的同行连接.停止() 停止音频轨道是标准方式――




> **【拓展：语音与情感计算】**语音不仅传递文字信息,还携带丰富的情感信号 (语调、语速、音高变化) 情感语音识别 (语音识别,语音情感识别,SER) 在客服质检,心理健康监测,智能教育等领域广泛应用.

## 用它实现框架

现在,我们要做什么?

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



## 陷

> 常见陷

- **Buffering 500 ms to be safe.**缓冲器是你的延迟地板.
  **缓冲 500 ms 求安全。**缓冲区就是你的延迟下限.
- **Not pinning threads.**在优先级低于UI线程上的音频回调 = 负载下出现故障.
  **没有绑定线程。**音频调调在低于UI 优先线程上 = 负载下出现故障.
- **TTS chunks too small.**微分数为200ms,使声码器的文物听起来.
  **TTS 块太小。**低于200ms的块使声码器伪影可听.320ms的块是最佳平衡点.
- **No jitter buffer.**实际的网络是紧张的,没有平滑的你得到了爆发.
  **没有抖动缓冲。**没有平滑会出现爆音.
- **Single-shot error handling.**音频管道必须是防撞的.
  **单次错误处理。**频频流水线必须抗击崩.

> **【中文解读】**本节关注如何将模型部署为可用的产品. 从原型到生产级系统需要考虑性能优化,错误处理,监控等多个维度.


## 运送它.

保存如`outputs/skill-realtime-designer.md`设计一个实时音频管道,每个阶段的具体延迟预算.

> 保存为`outputs/skill-realtime-designer.md`◎每个阶段的设计有具体的延迟预算的实时频流水线.

## 练习题

1. **Easy.**跑步`code/main.py`模拟环保器+能量VAD; 打印假的10秒流的阶段延迟.
   **简单。**运行`code/main.py`模拟环形缓冲区 + 能量 VAD;印假 10 秒流各阶段延迟──
2. **Medium.**使用`sounddevice`通过一个循环,将你的麦克风处理在20毫米的框架中,
   **中等。**使用 `sounddevice`构建直通循环,以20 ms 处理风,每次打印VAD状态.
3. **Hard.**通过 构建一个完整的双重回声测试`aiortc`通过1kHz脉冲测量玻璃到玻璃延迟.
   **困难。**用`aiortc`构建全双工回声测试:浏览器 → WebRTC → Python → WebRTC → 浏览器──用 1 kHz 脉冲测量端到端延迟──

> **【中文解读】**在团队协作中,统一术语定义可以避免大量沟通误解.


## 关键词 快速查找表

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

> **【中文解读】**延伸阅读提供了深入学习的高质量资源. 这些论文和教程是该领域的经典参考文献,适合需要深入了解的读者.


## 继续阅读 继续阅读

- [Macháček et al. (2023). Whisper-Streaming](https://arxiv.org/abs/2307.14743)           
  语流分块近流式语──
- [Kyutai (2024). Moshi](https://kyutai.org/Moshi.pdf) 完全双重200 ms延迟
  九台 (2024). 莫西全双工 200 ms 延迟──
- [LiveKit Agents framework (2024)](https://docs.livekit.io/agents/)制作音频代理管弦乐.
  现场直播机器人 框架(2024) 生产级音频智能体编排──
- [Silero VAD repo](https://github.com/snakers4/silero-vad)下-1 ms VAD,Apache 2.0.
  果版的数据库
- [WebRTC AEC3 paper](https://webrtc.googlesource.com/src/+/main/modules/audio_processing/aec3/)在开源下回声取消.
  网络广告技术有限公司

> **【中文解读】**延伸阅读提供了深入学习的高质量资源,包括论文,教程和工具.

