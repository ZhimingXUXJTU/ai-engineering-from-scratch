# 语音活动检测与轮次切换 — Silero、Cobra 与刷新技巧

> 每个语音助手的成败取决于两个判断：用户现在在说话吗？用户说完了吗？VAD（语音活动检测）回答第一个，轮次检测（VAD+静音持续+语义终点模型）回答第二个。任何一个搞错，助手要么打断用户，要么永远不开口。

> **【中文解读】** 每个语音助手的成败取决于两个判断：用户现在在说话吗？用户说完了吗？VAD（语音活动检测）回答第一个，轮次检测（VAD+静音持续+语义终点模型）回答第二个。任何一个搞错，助手要么打断用户，要么永远不开口。

**类型：** 构建
**语言：** Python
**前置条件：** 阶段 6 · 11（实时音频），阶段 6 · 12（语音助手）
**时长：** 约 45 分钟

## 问题引入

语音代理在每个 20 ms 块上做三个不同的判断：

> **【中文解读】** 本节提出的问题是：如何在实际工程中正确理解和应用这一技术。理解问题背景有助于把握技术选型的关键决策点。在实际 AI 系统中，错误的技术选型往往比实现细节的 bug 代价更高。

1. **这一帧是语音吗？**——VAD。二元的，逐帧。
2. **用户开始了一个新的话语吗？**——起始检测。
3. **用户说完了吗？**——端点检测（轮次结束）。

朴素答案（能量阈值）在任何噪声下都会失败——交通、键盘、人群嘈杂。2026 年的答案：Silero VAD（开源，深度学习）+ 轮次检测模型（语义端点检测）+ VAD 校准的静音悬挂。

## 核心概念

> **【中文解读】** 本节介绍核心概念和理论基础。掌握这些概念是后续动手实现的前提，同时也是面试和工程实践中高频考察的知识点。

![VAD 级联：能量 -> Silero -> 轮次检测器 -> 刷新技巧](../assets/vad-turn-taking.svg)

### 三层 VAD 级联

**第 1 层：能量门。** 最便宜。-40 dBFS 阈值 RMS。过滤明显静音但任何超过阈值的噪声都会触发。

**第 2 层：Silero VAD**（2020-2026，MIT）。100 万参数。在 6000+ 种语言上训练。在单个 CPU 线程上每 30 ms 块约 1 ms 运行。5% FPR 下 87.7% TPR。开源默认。

**第 3 层：语义轮次检测器。** LiveKit 的轮次检测模型（2024-2026）或你自己的小型分类器。区分"句中停顿"和"说完"。使用语言上下文（语调 + 最近词语），不仅仅是静音。

### 关键参数及默认值

- **阈值。** Silero 输出概率；> 0.5 分类为语音（默认）或 > 0.3（敏感）。较低阈值 = 更少首词截断，更多误报。
- **最小语音时长。** 拒绝短于 250 ms 的语音——通常是咳嗽或椅子噪声。
- **静音悬挂（端点检测）。** VAD 返回 0 后，等待 500-800 ms 再声明轮次结束。太短 -> 打断用户。太长 -> 感觉迟钝。
- **预滚动缓冲。** 保留 VAD 触发前 300-500 ms 的音频。防止"嘿"被截断。

### 刷新技巧（Kyutai 2025）

流式 STT 模型有前瞻延迟（Kyutai STT-1B 为 500 ms，STT-2.6B 为 2.5 s）。通常你需要在语音结束后等那么久才能得到转录。刷新技巧：当 VAD 触发语音结束时，**向 STT 发送一个刷新信号**强制立即输出。STT 以约 4 倍实时速度处理，所以 500 ms 缓冲在约 125 ms 内完成。

端到端：125 ms VAD + 刷新 STT = 对话级延迟。

### 2026 VAD 比较

| VAD | 5% FPR 下 TPR | 延迟 | 许可 |
|-----|---------------|------|------|
| WebRTC VAD（Google，2013） | 50.0% | 30 ms | BSD |
| Silero VAD（2020-2026） | 87.7% | 约 1 ms | MIT |
| Cobra VAD（Picovoice） | 98.9% | 约 1 ms | 商业 |
| pyannote 分割 | 95% | 约 10 ms | MIT-ish |

Silero 是正确的默认选择。Cobra 是合规/精度升级。仅能量 VAD 在 2026 年生产中没有位置。

> **【中文解读】** 本节通过代码从零实现核心算法。这种 "from scratch" 的方式能帮助理解框架背后的原理，遇到问题时不会被黑盒困住。

> **【拓展：语音 AI 的产品化】** 语音技术在产品化中面临独特挑战：不同口音、背景噪声、远场拾音、多人说话等。Siri、Alexa、小爱同学等产品都投入了大量工程优化来解决这些 "长尾问题"。实时性要求（<300ms 延迟）也是语音产品的核心指标。

> **【拓展：多语言语音技术】** 全球语言的语音特性差异巨大：声调语言（如中文）的音高携带语义，低资源语言缺乏训练数据。Meta 的 MMS 模型支持 1000+ 种语言的语音识别，Whisper 在多语言场景表现出色，但仍需针对特定语言微调。

> **【拓展：语音隐私与安全】** 语音数据包含大量个人隐私信息（声纹、对话内容）。深度伪造（Deepfake）语音技术可以被滥用于诈骗。音频水印（Audio Watermarking）和声纹反欺诈（Anti-spoofing）是当前的研究热点。

## 动手实现

### 步骤 1：能量门

```python
def energy_vad(chunk, threshold_dbfs=-40.0):
    rms = (sum(x * x for x in chunk) / len(chunk)) ** 0.5
    dbfs = 20.0 * math.log10(max(rms, 1e-10))
    return dbfs > threshold_dbfs
```

### 步骤 2：Python 中的 Silero VAD

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

### 步骤 3：轮次结束状态机

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

### 步骤 4：刷新技巧骨架

```python
def flush_on_end(stt_client, audio_buffer):
    stt_client.send_audio(audio_buffer)
    stt_client.send_flush()
    return stt_client.recv_transcript(timeout_ms=150)
```

> **【中文解读】** 本节展示如何用成熟框架（如 PyTorch、HuggingFace 等）快速应用该技术。在实际项目中，优先使用经过验证的框架实现，可以减少 bug 并提高开发效率。

STT（Kyutai、Deepgram、AssemblyAI）必须支持刷新才能使用这个技巧。Whisper streaming 不支持——它是基于块的，总是等待完整块。

> **【拓展：语音与情感计算】** 语音不仅传递文字信息，还携带丰富的情感信号（语调、语速、音高变化）。情感语音识别（Speech Emotion Recognition, SER）在客服质检、心理健康监测、智能教育等领域有广泛应用。当前 SOTA 模型通常基于 wav2vec 2.0 或 HuBERT 等预训练模型微调。

## 用框架实现

| 场景 | VAD 选择 |
|------|----------|
| 开源，快速，通用 | Silero VAD |
| 商业呼叫中心 | Cobra VAD |
| 端上（手机） | Silero VAD ONNX |
| 研究 / 说话人日志 | pyannote 分割 |
| 零依赖回退 | WebRTC VAD（遗留） |
| 需要轮次结束质量 | Silero + LiveKit 轮次检测器分层 |

经验法则：除非真的没有其他选择，否则永远不要发布仅能量 VAD。

## 陷阱

- **固定阈值。** 安静时有效，嘈杂时失败。要么在设备上校准，要么切换到 Silero。
- **静音悬挂太短。** 代理在句中打断用户。500-800 ms 是对话语音的最佳点。
- **悬挂太长。** 感觉迟钝。与目标用户做 A/B 测试。
- **没有预滚动缓冲。** 用户音频前 200-300 ms 丢失。始终保持滚动的预滚动。
- **忽略语义端点检测。** "嗯，让我想想..."包含长停顿。用户讨厌在思考中途被打断。使用 LiveKit 的轮次检测器或类似方案。

> **【中文解读】** 本节关注如何将模型部署为可用的产品。从原型到生产级系统需要考虑性能优化、错误处理、监控等多个维度。

## 产出物

保存为 `outputs/skill-vad-tuner.md`。为工作负载选择 VAD 模型、阈值、悬挂、预滚动和轮次检测策略。

## 练习题

1. **简单。** 运行 `code/main.py`。它模拟一个语音 + 静音 + 语音 + 咳嗽序列，测试三层 VAD。
2. **中等。** 安装 `silero-vad`，处理一段 5 分钟录音，调优阈值以最小化首词截断和误触发。报告精确率/召回率。
3. **困难。** 构建迷你轮次检测器：Silero VAD + 最近 10 个词嵌入上的 3 层 MLP（使用 sentence-transformers）。在手标注的轮次结束数据集上训练。在 F1 上超过仅 Silero 10%。

> **【中文解读】** 术语表中的 "What people say" vs "What it actually means" 区分了日常口语和精确技术含义。在团队协作中，统一术语定义可以避免大量沟通误解。

## 术语速查表

| 术语 | 通俗说法 | 实际含义 |
|------|----------|----------|
| VAD | 语音检测器 | 逐帧二元判断：这是语音吗？ |
| 轮次检测 | 端点检测 | VAD + 静音悬挂 + 语义端点。 |
| 静音悬挂 | 语音后等待 | 声明轮次结束前等待的时间；500-800 ms。 |
| 预滚动 | 语音前缓冲 | VAD 触发前保留 300-500 ms 音频。 |
| 刷新技巧 | Kyutai 技巧 | VAD -> 刷新 STT -> 125 ms 而不是 500 ms 延迟。 |
| 语义端点 | "他们想停吗？" | 看词语的 ML 分类器，不仅仅是静音。 |
| 5% FPR 下 TPR | ROC 点 | 标准 VAD 基准；Silero 87.7%，WebRTC 50%。 |

> **【中文解读】** 延伸阅读提供了深入学习的高质量资源。这些论文和教程是该领域的经典参考文献，适合需要深入理解的读者。

## 延伸阅读

- [Silero VAD](https://github.com/snakers4/silero-vad) —— 参考开源 VAD。
- [Picovoice Cobra VAD](https://picovoice.ai/products/cobra/) —— 商业精度领军者。
- [Kyutai — Unmute + 刷新技巧](https://kyutai.org/stt) —— 亚 200 ms 工程技巧。
- [LiveKit — 轮次检测](https://docs.livekit.io/agents/logic/turns/) —— 生产中的语义端点检测。
- [WebRTC VAD](https://webrtc.googlesource.com/src/) —— 遗留基线。
- [pyannote 分割](https://github.com/pyannote/pyannote-audio) —— 日志级分割。

> **【中文解读】** 延伸阅读提供了深入学习的高质量资源，包括论文、教程和工具。建议按需选读，优先阅读标注为 "the critical read" 的核心论文。
