# 语音活动检测与轮次切换

> 每个语音代理都根据两个决定生活或死亡:用户现在在说话,他们已经完成了吗?VAD回答第一个.转发检测 (VAD +沉默-置 +语义终点模型) 回答第二个.要么错误,你的助理要么关闭用户,要么永远不关闭嘴.

> **【中文解读】**每个语音助手的成功取决于两个判断:用户现在在说话吗?用户说完了吗?VAD(语音活动检测) 回答第一个,轮次检测(VAD+静音持续+语义终点模型) 回答第二个――任何一个搞错,助手要么打断用户,要么永远不开口――

**Type:** Build | **类型:** 构建
**Languages:** Python | **语言:** Python
**Prerequisites:** Phase 6 · 11 (Real-Time Audio), Phase 6 · 12 (Voice Assistant) | **前置知识:** 阶段 6 · 11（实时音频），阶段 6 · 12（语音助手）
**Time:** ~45 minutes | **预计用时:** ~45 分钟

## 问题 问题引入

语音代理每20毫米分钟就会做出三个不同的决定:

> 语音助手需要在每20ms的音频块上做出三个不同的判断:

> **【中文解读】**本节提出的问题是:如何在实际工程中正确理解和应用这一技术――理解问题背景有助于把握技术选择的关键决策点――在实际人工智能系统中,错误的技术选择往往比实现细节的错误成本更高――


1. **Is this frame speech?**VAD,双式,每一个框架.
   中文翻译:这个是语音吗?
2. **Has the user started a new utterance?** 发病的检测.
   中文翻译:用户开始一个新的发言吗?
3. **Has the user finished?**终点指向 (转向).
   中文翻译:用户说完了吗?

简单的答案 (能量门) 在任何噪音,键盘,人群语上都失败了. 2026 答案:Silero VAD (开放,深入学习) + 转向检测模型 (语义终点指标) + VAD校准的沉默.

> 简单的答案:                                                                                                                                                                                                                                                            

## 概念的核心概念

> **【中文解读】**本节介绍核心概念和理论基础.掌握这些概念是后续动手实现的前提,同时也是面试和工程实践中高频考察的知识点.


![VAD cascade: energy → Silero → turn-detector → flush trick](../assets/vad-turn-taking.svg)

### 排列三的VAD

> 三级VAD级联架构

**Tier 1: energy gate.**最便宜的,门RMS在 -40 dBFS. 过明显的沉默,但在门以上的任何噪音上,

> **第一层：能量门控。**最便宜的方法:将RMS 值设为 -40 dBFS.

**Tier 2: Silero VAD**运行在一个CPU线程上每30ms块的1ms. 87.7%的TPR在5%的FPR.开源默认.

> **第二层：Silero VAD**通过网络技术,我们可以通过网络技术来实现网络技术的发展.

**Tier 3: semantic turn detector.**动Kit的轮回检测模型 (2024-2026) 或您自己的小分类器. 区分"语句中暂停"和"做完谈话". 使用语言背景 (语法 + 最近的词),而不仅仅是沉默.

> **第三层：语义轮次检测器。**语调 + 近期词汇),而不仅仅是静音──

### 关键参数及其默认设置

> 关键参数及其默认值

- **Threshold.**希勒罗输出一个概率;将语音分为&gt;0.5 (默认) 或&gt;0.3 (敏感).较低的门 = 减少第一词剪辑,更多的虚假积极.
  翻译: 中文**阈值。**字母输出概率值;以 > 0.5(默认) 或 > 0.3(敏感模式) 分类语音──值越低 = 首词截断越少,但误报越多──
- **Minimum speech duration.**拒绝超过250 ms的语音 通常咳或椅子噪音.
  翻译: 中文**最小语音时长。**拒绝短于250ms的语音通常是咳或椅子噪音.
- **Silence hangover (end-pointing).**在VAD返回0后,等待500-800ms,然后宣布转换结束.太短 →打断用户.太长 →感觉缓慢.
  翻译: 中文**静音持续等待（端点检测）。**转到0后,等待500-800ms再宣布轮次结束――太短 → 打断用户――太长 → 感觉迟――
- **Pre-roll buffer.**在VAD发射之前保持300-500ms的音频,防止""被剪切.
  翻译: 中文**预滚缓冲。**在VAD 触发前保留300-500 ms 音频──防止""字被截断──

### 鱼的技巧 (九台2025年)

流媒体STT模型的前进延迟 (Kyutai STT-1B的500ms,STT-2.6B的2.5s). 通常你会等待这么长时间后的演讲结束.**send a flush signal to the STT**通过4×实时处理,所以500ms缓冲器在125ms内完成.

> 流式 STT 模型有前视延迟(Kyutai STT-1B 为 500 ms,STT-2.6B 为 2.5 s) ⋅通常你需要在语音结束后等这么长时间才能获得转录结果──刷新技巧:当VAD 触发语音结束时,**向 STT 发送刷新信号**强制即时输出.STT以实际处理速度约4倍,所以500 ms 缓冲区在约125 ms 内完成.

终端到终端:125 ms VAD + 流动STT = 对话延迟.

> 端到端:125 ms VAD + 刷新STT = 对话级延迟――

### 2026 年的VAD比较

> 2026 年的VAD对比

| VAD | TPR @ 5% FPR | Latency | License |
|-----|--------------|---------|---------|
| WebRTC VAD (Google, 2013) | 50.0% | 30 ms | BSD |
| Silero VAD (2020-2026) | 87.7% | ~1 ms | MIT |
| Cobra VAD (Picovoice) | 98.9% | ~1 ms | commercial |
| pyannote segmentation | 95% | ~10 ms | MIT-ish |

果是正确的默认. 科布拉是合规性/精度升级. 仅能VAD在2026年生产没有地方.

> 科布拉是合规性/准确性升级选项. 仅基于能量的VAD在2026年的生产环境中已经没有足够的位置.

> **【中文解读】**本节通过代码实现从零到核心算法――这种"从零开始"的方式可以帮助理解框架背后的原理,遇到问题时不会被黑盒困住――

> **【拓展：语音 AI 的产品化】**语音技术在产品化中面临着独特的挑战:不同口音,背景噪音,远场拾音,多人说话等.

> **【拓展：多语言语音技术】**全球语言的语音特性差异巨大:声调语言的音高携带语义,低资源语言缺乏训练数据――Meta的MMS模型支持1000多种语言的语音识别,语在多语言场景表现出色,但仍然需要针对特定语言微调――

> **【拓展：语音隐私与安全】**语音数据包含大量个人隐私信息 (声纹、对话内容) ◦深度伪造 (Deepfake) 语音技术可被滥用作弊 (欺诈) 音频水印 (音频水印) ◎音纹反欺诈 (反欺诈) ◎反欺诈 (反欺诈) ◎是当前的研究热点.





## 建立它,实现它.
```figure
sp-vad-cascade
```

## 建立它

### 步骤1:能源门

> 步骤1:能量门控

```python
def energy_vad(chunk, threshold_dbfs=-40.0):
    rms = (sum(x * x for x in chunk) / len(chunk)) ** 0.5
    dbfs = 20.0 * math.log10(max(rms, 1e-10))
    return dbfs > threshold_dbfs
```

### 步骤 2: 在 Python 中使用 Silero VAD

> 步骤 2: 在Python中使用Silero VAD

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

### 步骤3:转端状态机

> 步骤3:轮次结束状态机

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

### 步骤4: 鱼技巧骨架

> 步骤4:刷新技巧框架代码

```python
def flush_on_end(stt_client, audio_buffer):
    stt_client.send_audio(audio_buffer)
    stt_client.send_flush()
    return stt_client.recv_transcript(timeout_ms=150)
```

> **【中文解读】**本节展示了如何使用成熟框架 (如PyTorch、HuggingFace等) 快速应用该技术.


为了实现这一目标,STT (Kyutai,Deepgram,AssemblyAI) 必须支持flush.

> 语流式不支持它是基于块的,总是等待完整块的语.




> **【拓展：语音与情感计算】**语音不仅传递文字信息,还携带丰富的情感信号 (语调、语速、音高变化) 情感语音识别 (语音识别,语音情感识别,SER) 在客服质检,心理健康监测,智能教育等领域广泛应用.

## 用它实现框架

| Situation | VAD choice |
|-----------|-----------|
| Open, fast, general / 开源、快速、通用 | Silero VAD |
| Commercial call center / 商业呼叫中心 | Cobra VAD |
| On-device (phone) / 端侧（手机） | Silero VAD ONNX |
| Research / diarization / 研究/说话人日志 | pyannote segmentation |
| Zero-dependency fallback / 零依赖后备方案 | WebRTC VAD（传统） |
| Need turn-ending quality / 需要轮次结束质量 | Silero + LiveKit 轮次检测器分层 |

指规则:除非你真的没有其他选择,否则,永远不要运送纯能动的VAD.

> 经验法则:除非真的没有其他选择,否则永远不要上线仅基于能量的VAD.



## 陷

> 常见陷

- **Fixed threshold.**机器在安静状态下工作,噪音时失败.
  翻译: 中文**固定阈值。**在安静环境下有效,杂环境下失败.
- **Too-short silence hangover.**代理打断句子中. 500-800ms是谈话的最好地方.
  翻译: 中文**静音持续等待过短。**助手在句子中打断用户──500-800 ms 是对话语音的最佳范围──
- **Too-long hangover.**对于目标用户来说,A/B测试.
  翻译: 中文**静音持续等待过长。**感觉迟──与目标用户进行A/B测试──
- **No pre-roll buffer.**首先,用户的音频输出200-300ms,总是保持滚动前滚动.
  翻译: 中文**没有预滚缓冲。**用户音频的前200-300ms 丢失──始终保持滚动预滚缓冲──
- **Ignoring semantic endpointing.**"让我思考"...包含长时间的暂停.用户讨厌被停留在思考中.使用LiveKit的转换探测器或类似.
  翻译: 中文**忽略语义端点检测。**让我想想......"包含长停顿.用户不喜欢在思考过程中被断断.

> **【中文解读】**本节关注如何将模型部署为可用的产品. 从原型到生产级系统需要考虑性能优化,错误处理,监控等多个维度.


## 运送它.

保存如`outputs/skill-vad-tuner.md`选择VAD模型,门,,预滚和转变检测策略.

> 保存为`outputs/skill-vad-tuner.md`△为工作负载选择VAD 模型、值、静音持续等待、预滚缓冲和轮次检测策略──

## 练习题

1. **Easy.**跑步`code/main.py`它模拟了语音+沉默+语音+咳序列,并测试了三个VAD级别.
   翻译: 中文**简单。**运行`code/main.py`〔它模拟一段语音 + 静音 + 语音 + 咳的序列,并测试三层VAD〕
2. **Medium.**安装`silero-vad`通过5分钟的录音,调整门以尽量减少第一字剪辑和错误触发.
   翻译: 中文**中等。**装备`silero-vad`处理一段 5 分钟录音,调整值以最小化首词截断和误触发――报告精确率/召回率――
3. **Hard.**建立一个小型转换检测器:Silero VAD + 在最后10个字的嵌入式上进行3层MLP (使用句子转换器).使用手动标记的转换端数据集训练.仅打败Silero-F110%
   翻译: 中文**困难。**构建一个小型轮次检测器:Silero VAD + 基于10个近词嵌入的3层MLP(使用句子转换器) ⋅在手工标签的轮次结束数据集上训练――比纯Silero方案 F1 高10%──

> **【中文解读】**在团队协作中,统一术语定义可以避免大量沟通误解.


## 关键词 快速查找表

| Term | What people say | What it actually means |
|------|-----------------|-----------------------|
| VAD | Voice detector | Binary per-frame: is this speech? / 逐帧二分类：这是语音吗？ |
| Turn detection | End-pointing | VAD + silence-hangover + semantic endpoint. / VAD + 静音持续 + 语义端点 |
| Silence hangover | Wait-after-speech | Time to wait before declaring turn end; 500-800 ms. / 宣布轮次结束前的等待时间；500-800 ms |
| Pre-roll | Pre-speech buffer | Keep 300-500 ms audio before VAD fires. / 在 VAD 触发前保留 300-500 ms 音频 |
| Flush trick | Kyutai hack | VAD → flush-STT → 125 ms instead of 500 ms delay. / VAD → 刷新 STT → 125 ms 而非 500 ms 延迟 |
| Semantic endpoint | "Did they mean to stop?" | ML classifier that looks at words, not just silence. / 看词汇而非仅看静音的 ML 分类器 |
| TPR @ FPR 5% | ROC point | Standard VAD benchmark; 87.7% for Silero, 50% WebRTC. / 标准 VAD 基准；Silero 87.7%，WebRTC 50% |

> **【中文解读】**延伸阅读提供了深入学习的高质量资源. 这些论文和教程是该领域的经典参考文献,适合需要深入了解的读者.


## 继续阅读 继续阅读

- [Silero VAD](https://github.com/snakers4/silero-vad) 参考开放的VAD.
                    
- [Picovoice Cobra VAD](https://picovoice.ai/products/cobra/)商业精度领先者.
  商业精度领先者
- [Kyutai — Unmute + flush trick](https://kyutai.org/stt)200ms下级工程技巧.
  九台Unmute + 刷新技巧亚 200 ms 的工程技巧。
- [LiveKit — turn detection](https://docs.livekit.io/agents/logic/turns/)生产中的语义终点.
  轮检测生产中的语义端点检测
- [WebRTC VAD](https://webrtc.googlesource.com/src/)遗产基线.
  网络广告技术有限公司
- [pyannote segmentation](https://github.com/pyannote/pyannote-audio)日记级分类.
  标签: 标签: 标签: 标签: 标签: 标签: 标签: 标签: 标签: 标签: 标签: 标签: 标签: 标签: 标签: 标签: 标签: 标签: 标签: 标签: 标签: 标签: 标签: 标签: 标签: 标签: 标签: 标签: 标签: 标签: 标签: 标签: 标签: 标签: 标签: 标签: 标签: 标签: 标签: 标签: 标签: 标签: 标签: 标签: 标签: 标签

> **【中文解读】**延伸阅读提供了深入学习的高质量资源,包括论文,教程和工具.

