# 语音合成 — 从 Tacotron 到 F5 和 Kokoro

> ASR 把语音变文字，TTS（Text-to-Speech）把文字变语音。2026 年的 TTS 技术栈分三步：文本 -> token -> Mel 频谱 -> 波形。每一步都有可在笔记本上运行的默认模型。

> **【中文解读】** ASR 把语音变文字，TTS 把文字变语音。2026 年的 TTS 技术栈分三步：文本→token→Mel 频谱→波形。每一步都有可在笔记本上运行的默认模型。

> **【拓展：TTS 的应用】** TTS 是有声书、导航语音、虚拟助手（Siri/小爱同学）、无障碍辅助（为视障人士朗读）的核心技术。零样本 TTS（只需几秒参考音频即可克隆声音）是最新突破。

**类型：** 构建
**语言：** Python
**前置条件：** 阶段 6 · 02（频谱图与 Mel），阶段 5 · 09（序列到序列），阶段 7 · 05（完整 Transformer）
**时长：** 约 75 分钟

## 问题引入

你有一个字符串："请在下午 6 点提醒我浇花。"你需要一段 3 秒的音频，听起来自然，有正确的韵律（停顿、重音），"花"的元音发音正确，并且在 CPU 上运行不超过 300 ms 以支持实时语音助手。你还需要切换声音、处理混合语言输入（"remind me at 6 pm, 大丈夫？"），以及在名字上不出丑。

> **【中文解读】** 本节提出的问题是：如何在实际工程中正确理解和应用这一技术。理解问题背景有助于把握技术选型的关键决策点。在实际 AI 系统中，错误的技术选型往往比实现细节的 bug 代价更高。

现代 TTS 流水线如下：

1. **文本前端。** 归一化文本（日期、数字、电子邮件），转换为音素或子词 token，预测韵律特征。
2. **声学模型。** 文本 -> Mel 频谱图。Tacotron 2（2017）、FastSpeech 2（2020）、VITS（2021）、F5-TTS（2024）、Kokoro（2024）。
3. **声码器（Vocoder）。** Mel -> 波形。WaveNet（2016）、WaveRNN、HiFi-GAN（2020）、BigVGAN（2022），2024+ 年为神经编解码器声码器。

2026 年，随着端到端扩散和流匹配模型的出现，声学模型 + 声码器的界限变得模糊。但三部分的心智模型对于调试仍然有用。

## 核心概念

> **【中文解读】** 本节介绍核心概念和理论基础。掌握这些概念是后续动手实现的前提，同时也是面试和工程实践中高频考察的知识点。

![Tacotron、FastSpeech、VITS、F5/Kokoro 并排比较](../assets/tts.svg)

**Tacotron 2（2017）。** 序列到序列：字符嵌入 -> BiLSTM 编码器 -> 位置敏感注意力 -> 自回归 LSTM 解码器发射 Mel 帧。慢（自回归），长文本不稳定。仍被引用为基线。

**FastSpeech 2（2020）。** 非自回归。时长预测器输出每个音素对应多少个 Mel 帧。单次前向，比 Tacotron 快 10 倍。损失一些自然度（单调对齐）但在各处部署。

**VITS（2021）。** 端到端联合训练编码器 + 基流的时长预测 + HiFi-GAN 声码器，使用变分推断。高质量，单一模型。2022-2024 年主导开源 TTS。变体：YourTTS（多说话人零样本）、XTTS v2（2024，Coqui）。

**F5-TTS（2024）。** 基于流匹配的扩散 Transformer。自然韵律，5 秒参考音频即可零样本语音克隆。2026 年开源 TTS 排行榜榜首。3.35 亿参数。

**Kokoro（2024）。** 小型（82M），可在 CPU 上运行，英语实时 TTS 中质量最佳。封闭词汇表仅支持英语，Apache-2.0 许可。

**OpenAI TTS-1-HD、ElevenLabs v2.5、Google Chirp-3。** 商业 SOTA。ElevenLabs v2.5 的情感标签（"[whispered]"、"[laughing]"）和角色声音在 2026 年有声书制作中占主导。

### 声码器演进

| 时代 | 声码器 | 延迟 | 质量 |
|------|--------|------|------|
| 2016 | WaveNet | 仅离线 | 发布时 SOTA |
| 2018 | WaveRNN | 约实时 | 好 |
| 2020 | HiFi-GAN | 100x 实时 | 接近人类 |
| 2022 | BigVGAN | 50x 实时 | 跨说话人/语言泛化 |
| 2024 | SNAC、DAC（神经编解码器） | 与 AR 模型集成 | 离散 token，比特高效 |

到 2026 年，大多数"TTS"模型是端到端从文本到波形；Mel 频谱图是内部表示。

### 评估

- **MOS（平均意见分，Mean Opinion Score）。** 1-5 分，众包。仍是黄金标准；速度令人痛苦。
- **CMOS（比较 MOS）。** A-vs-B 偏好。每个标注的置信区间更窄。
- **UTMOS、DNSMOS。** 无参考神经 MOS 预测器。用于排行榜。
- **CER（字符错误率）通过 ASR。** 将 TTS 输出通过 Whisper，计算与输入文本的 CER。可懂度的代理指标。
- **SECS（说话人嵌入余弦相似度）。** 语音克隆质量指标。

2026 年 LibriTTS test-clean 上的数字：

| 模型 | UTMOS | CER（通过 Whisper） | 大小 |
|------|-------|---------------------|------|
| 真实语音 | 4.08 | 1.2% | — |
| F5-TTS | 3.95 | 2.1% | 3.35 亿 |
| XTTS v2 | 3.81 | 3.5% | 4.7 亿 |
| VITS | 3.62 | 3.1% | 25M |
| Kokoro v0.19 | 3.87 | 1.8% | 82M |
| Parler-TTS Large | 3.76 | 2.8% | 23 亿 |

> **【中文解读】** 本节通过代码从零实现核心算法。这种 "from scratch" 的方式能帮助理解框架背后的原理，遇到问题时不会被黑盒困住。

> **【拓展：语音 AI 的产品化】** 语音技术在产品化中面临独特挑战：不同口音、背景噪声、远场拾音、多人说话等。Siri、Alexa、小爱同学等产品都投入了大量工程优化来解决这些 "长尾问题"。实时性要求（<300ms 延迟）也是语音产品的核心指标。

> **【拓展：多语言语音技术】** 全球语言的语音特性差异巨大：声调语言（如中文）的音高携带语义，低资源语言缺乏训练数据。Meta 的 MMS 模型支持 1000+ 种语言的语音识别，Whisper 在多语言场景表现出色，但仍需针对特定语言微调。

## 动手实现

### 步骤 1：音素化输入

```python
from phonemizer import phonemize
ph = phonemize("Hello world", language="en-us", backend="espeak")
# 'həloʊ wɜːld'
```

音素是通用桥梁。避免将原始文本喂给 VITS 质量以下的任何模型。

### 步骤 2：运行 Kokoro（2026 年 CPU 默认）

```python
from kokoro import KPipeline
tts = KPipeline(lang_code="a")  # "a" = 美式英语
audio, sr = tts("Please remind me to water the plants at 6 pm.", voice="af_bella")
# audio: float32 tensor, sr=24000
```

离线运行，单文件，82M 参数。

### 步骤 3：用 F5-TTS 做语音克隆

```python
from f5_tts.api import F5TTS
tts = F5TTS()
wav = tts.infer(
    ref_file="my_voice_5s.wav",
    ref_text="The quick brown fox jumps over the lazy dog.",
    gen_text="Please remind me to water the plants.",
)
```

传入 5 秒参考片段 + 其转录；F5 克隆韵律和音色。

### 步骤 4：从零构建 HiFi-GAN 声码器

太大无法放入教程脚本，但形状是：

```python
class HiFiGAN(nn.Module):
    def __init__(self, mel_channels=80, upsample_rates=[8, 8, 2, 2]):
        super().__init__()
        # 4 个上采样块，总共 256 倍从 Mel 速率到音频速率
        ...
    def forward(self, mel):
        return self.blocks(mel)  # -> 波形
```

训练：对抗性（短窗口上的判别器）+ Mel 频谱图重建损失 + 特征匹配损失。已商品化——使用 `hifi-gan` 仓库或 nvidia-NeMo 的预训练检查点。

### 步骤 5：完整流水线（伪代码）

```python
text = "Please remind me at 6 pm."
phones = phonemize(text)
mel = acoustic_model(phones, speaker=alice)      # [T, 80]
wav = vocoder(mel)                                # [T * 256]
soundfile.write("out.wav", wav, 24000)
```

> **【中文解读】** 本节展示如何用成熟框架（如 PyTorch、HuggingFace 等）快速应用该技术。在实际项目中，优先使用经过验证的框架实现，可以减少 bug 并提高开发效率。

> **【拓展：语音与情感计算】** 语音不仅传递文字信息，还携带丰富的情感信号（语调、语速、音高变化）。情感语音识别（Speech Emotion Recognition, SER）在客服质检、心理健康监测、智能教育等领域有广泛应用。当前 SOTA 模型通常基于 wav2vec 2.0 或 HuBERT 等预训练模型微调。

## 用框架实现

2026 年的技术栈：

| 场景 | 选择 |
|------|------|
| 实时英语语音助手 | Kokoro（CPU）或 XTTS v2（GPU） |
| 5 秒参考音频的语音克隆 | F5-TTS |
| 商业角色声音 | ElevenLabs v2.5 |
| 有声书旁白 | ElevenLabs v2.5 或 XTTS v2 + 微调 |
| 低资源语言 | 在 5-20 小时目标语言数据上训练 VITS |
| 表现力 / 情感标签 | ElevenLabs v2.5 或 StyleTTS 2 微调 |

2026 年开源领军者：**F5-TTS 追求质量，Kokoro 追求效率**。除非你是历史学家，否则不要碰 Tacotron。

## 陷阱

- **没有文本归一化器。** "Dr. Smith" 读作"Doctor"还是"Drive"？"2026" 读作"twenty twenty six"还是"two zero two six"？在音素化器之前归一化。
- **OOV 专有名词。** "Ghumare" -> "ghyu-mair"？为未知 token 部署一个备用的字素到音素模型。
- **削波。** 声码器输出很少削波，但推理时 Mel 缩放不匹配可能超过 +/-1.0。始终 `np.clip(wav, -1, 1)`。
- **采样率不匹配。** Kokoro 输出 24 kHz；你的下游流水线期望 16 kHz -> 重采样否则会有混叠。

> **【中文解读】** 本节关注如何将模型部署为可用的产品。从原型到生产级系统需要考虑性能优化、错误处理、监控等多个维度。

## 产出物

保存为 `outputs/skill-tts-designer.md`。为给定的声音、延迟和语言目标设计 TTS 流水线。

## 练习题

1. **简单。** 运行 `code/main.py`。从玩具词汇构建音素字典，估算每个音素的时长，并打印一个假的"Mel"计划。
2. **中等。** 安装 Kokoro，用 `af_bella` 和 `am_adam` 两个声音合成同一句话。比较音频时长和主观质量。
3. **困难。** 录制一段 5 秒的自己声音的参考片段。使用 F5-TTS 克隆。报告参考和克隆输出之间的 SECS。

> **【中文解读】** 术语表中的 "What people say" vs "What it actually means" 区分了日常口语和精确技术含义。在团队协作中，统一术语定义可以避免大量沟通误解。

## 术语速查表

| 术语 | 通俗说法 | 实际含义 |
|------|----------|----------|
| 音素（Phoneme） | 声音单元 | 抽象声音类别；英语有 39 个（ARPABet）。 |
| 时长预测器 | 每个音素持续多久 | 非自回归模型输出；每个音素的整数帧数。 |
| 声码器（Vocoder） | Mel -> 波形 | 将 Mel 频谱映射为原始采样点的神经网络。 |
| HiFi-GAN | 标准声码器 | 基于 GAN；2020-2024 年主导。 |
| MOS | 主观质量 | 人类评分者的 1-5 分平均意见分。 |
| SECS | 语音克隆指标 | 目标和克隆输出说话人嵌入之间的余弦相似度。 |
| F5-TTS | 2024 开源 SOTA | 流匹配扩散；零样本克隆。 |
| Kokoro | CPU 英语领军者 | 82M 参数模型，Apache 2.0。 |

> **【中文解读】** 延伸阅读提供了深入学习的高质量资源。这些论文和教程是该领域的经典参考文献，适合需要深入理解的读者。

## 延伸阅读

- [Shen et al. (2017). Tacotron 2](https://arxiv.org/abs/1712.05884) —— seq2seq 基线。
- [Kim, Kong, Son (2021). VITS](https://arxiv.org/abs/2106.06103) —— 端到端基于流的。
- [Chen et al. (2024). F5-TTS](https://arxiv.org/abs/2410.06885) —— 当前开源 SOTA。
- [Kong, Kim, Bae (2020). HiFi-GAN](https://arxiv.org/abs/2010.05646) —— 2026 年仍在部署的声码器。
- [Kokoro-82M on HuggingFace](https://huggingface.co/hexgrad/Kokoro-82M) —— 2024 年 CPU 友好的英语 TTS。

> **【中文解读】** 延伸阅读提供了深入学习的高质量资源，包括论文、教程和工具。建议按需选读，优先阅读标注为 "the critical read" 的核心论文。
