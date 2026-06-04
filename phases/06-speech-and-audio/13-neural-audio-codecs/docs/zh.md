# 神经音频编解码器 — EnCodec、SNAC、Mimi、DAC 与语义-声学分离

> 2026 年的音频生成几乎都基于 token。EnCodec、SNAC、Mimi、DAC 将连续波形转换为离散序列，让 Transformer 可以预测。语义-声学 token 分离（第一个码本=语义，其余=声学）是自 Transformer 以来音频领域最重要的架构变革。

> **【中文解读】** 2026 年的音频生成几乎都基于 token。EnCodec、SNAC、Mimi、DAC 将连续波形转换为离散序列，让 Transformer 可以预测。语义-声学 token 分离（第一个码本=语义，其余=声学）是自 Transformer 以来音频领域最重要的架构变革。

> **【拓展：音频 token 化】** 就像文本有 BPE tokenizer 将文字变成 token，音频有 EnCodec 等编解码器将声波变成 token。这使得音频可以像文本一样被大语言模型处理。Moshi、AudioLM 等模型都依赖这种 token 化。

**类型：** 学习
**语言：** Python
**前置条件：** 阶段 6 · 02（频谱图），阶段 10 · 11（量化），阶段 5 · 19（子词分词）
**时长：** 约 60 分钟

## 问题引入

语言模型处理离散 token。音频是连续的。如果你想为语音/音乐构建 LLM 风格的模型——MusicGen、Moshi、Sesame CSM、VibeVoice、Orpheus——你首先需要一个**神经音频编解码器**：一个学习到的编码器将音频离散化为小词汇表的 token，以及一个匹配的解码器重建波形。

> **【中文解读】** 本节提出的问题是：如何在实际工程中正确理解和应用这一技术。理解问题背景有助于把握技术选型的关键决策点。在实际 AI 系统中，错误的技术选型往往比实现细节的 bug 代价更高。

两个家族已经出现：

1. **重建优先编解码器** — EnCodec、DAC。优化感知音频质量。Token 是"声学的"——它们捕获一切，包括说话人身份、音色、背景噪声。
2. **语义优先编解码器** — Mimi（Kyutai）、SpeechTokenizer。强制第一个码本编码语言/语音内容（通常从 WavLM 蒸馏）。后续码本是声学细节。

2024-2026 年的洞察：**纯重建编解码器在尝试从文本生成时给出模糊的语音。** 编解码器 token 上的 LLM 必须在同一个码本中同时学习语言结构和声学结构，这不可扩展。将它们分离——语义码本 0，声学码本 1-N——正是让 Moshi 和 Sesame CSM 成功的关键。

## 核心概念

> **【中文解读】** 本节介绍核心概念和理论基础。掌握这些概念是后续动手实现的前提，同时也是面试和工程实践中高频考察的知识点。

![四种编解码器对比：EnCodec、DAC、SNAC（多尺度）、Mimi（语义+声学）](../assets/codec-comparison.svg)

### 核心技巧：残差向量量化（RVQ）

不是一个大型码本（需要数百万个码才能获得好质量），所有现代音频编解码器都使用 **RVQ**：一组小码本的级联。第一个码本量化编码器输出；第二个量化残差；以此类推。每个码本 1024 个码。8 个码本 = 1024^8 = 10^24 的有效词汇量。

推理时，解码器将每帧所有选定的码求和来重建。

### 2026 年四种重要编解码器

**EnCodec（Meta，2022）。** 基线。波形上的编码器-解码器，RVQ 瓶颈。24 kHz，最多 32 个码本，默认 4 个码本 @ 1.5 kbps。使用 `1D 卷积 + Transformer + 1D 卷积`架构。MusicGen 使用。

**DAC（Descript，2023）。** 带 L2 归一化码本的 RVQ，周期性激活函数，改进的损失函数。任何开源编解码器中最高的重建保真度——12 个码本时有时与原始语音难以区分。44.1 kHz 全频带。

**SNAC（Hubert Siuzdak，2024）。** 多尺度 RVQ——粗糙码本以比精细码本更低的帧率运行。有效地分层建模音频：约 12 Hz 的粗"草图"加 50 Hz 的细节。被 Orpheus-3B 使用，因为层次结构很好地映射到基于 LM 的生成。

**Mimi（Kyutai，2024）。** 2026 年的游戏规则改变者。12.5 Hz 帧率（极低），8 个码本 @ 4.4 kbps。码本 0 从 **WavLM 蒸馏**——训练来预测 WavLM 的语音内容特征。码本 1-7 是声学残差。这种分离驱动了 Moshi（第 15 课）和 Sesame CSM。

### 帧率对语言建模很重要

帧率越低 = 序列越短 = LM 越快。

| 编解码器 | 帧率 | 1 秒 = N 帧 | 适合 |
|----------|------|-------------|------|
| EnCodec-24k | 75 Hz | 75 | 音乐，通用音频 |
| DAC-44.1k | 86 Hz | 86 | 高保真音乐 |
| SNAC-24k（粗糙） | 约 12 Hz | 12 | AR-LM 高效 |
| Mimi | 12.5 Hz | 12.5 | 流式语音 |

在 12.5 Hz，一段 10 秒的话语只有 125 个编解码器帧——Transformer 可以轻松预测。

### 语义 vs 声学 token

```
frame_t -> [semantic_token_t, acoustic_token_0_t, acoustic_token_1_t, ..., acoustic_token_6_t]
```

- **语义 token（Mimi 中的码本 0）。** 编码说了什么——音素、单词、内容。从 WavLM 通过辅助预测损失蒸馏。
- **声学 token（码本 1-7）。** 编码音色、说话人身份、韵律、背景噪声、精细细节。

AR LM 首先预测语义 token（以文本为条件），然后预测声学 token（以语义 + 说话人参考为条件）。这种分解就是为什么现代 TTS 可以零样本克隆声音：语义模型处理内容；声学模型处理音色。

### 2026 年重建质量（比特每秒，比特率越低越好）

| 编解码器 | 比特率 | PESQ | ViSQOL |
|----------|--------|------|--------|
| Opus-20kbps | 20 kbps | 4.0 | 4.3 |
| EnCodec-6kbps | 6 kbps | 3.2 | 3.8 |
| DAC-6kbps | 6 kbps | 3.5 | 4.0 |
| SNAC-3kbps | 3 kbps | 3.3 | 3.8 |
| Mimi-4.4kbps | 4.4 kbps | 3.1 | 3.7 |

传统编解码器如 Opus 在每比特感知质量上仍然获胜。神经编解码器在**离散 token**（Opus 不产生）和**生成模型质量**（LM 能用这些 token 做什么）上获胜。

> **【拓展：语音 AI 的产品化】** 语音技术在产品化中面临独特挑战：不同口音、背景噪声、远场拾音、多人说话等。Siri、Alexa、小爱同学等产品都投入了大量工程优化来解决这些 "长尾问题"。实时性要求（<300ms 延迟）也是语音产品的核心指标。

> **【拓展：多语言语音技术】** 全球语言的语音特性差异巨大：声调语言（如中文）的音高携带语义，低资源语言缺乏训练数据。Meta 的 MMS 模型支持 1000+ 种语言的语音识别，Whisper 在多语言场景表现出色，但仍需针对特定语言微调。

## 动手实现

> **【中文解读】** 本节通过代码从零实现核心算法。这种 "from scratch" 的方式能帮助理解框架背后的原理，遇到问题时不会被黑盒困住。

### 步骤 1：用 EnCodec 编码

```python
from encodec import EncodecModel
import torch

model = EncodecModel.encodec_model_24khz()
model.set_target_bandwidth(6.0)  # kbps

wav = torch.randn(1, 1, 24000)
with torch.no_grad():
    encoded = model.encode(wav)
codes, scale = encoded[0]
# codes: (1, n_codebooks, n_frames), dtype=int64
```

6 kbps 时 `n_codebooks=8`。每个码是 0-1023（10 位）。

### 步骤 2：解码并测量重建

```python
with torch.no_grad():
    wav_recon = model.decode([(codes, scale)])

from torchaudio.functional import compute_deltas
import torch.nn.functional as F

mse = F.mse_loss(wav_recon[:, :, :wav.shape[-1]], wav).item()
```

### 步骤 3：语义-声学分离（Mimi 风格）

```python
from moshi.models import loaders
mimi = loaders.get_mimi()

with torch.no_grad():
    codes = mimi.encode(wav)  # shape (1, 8, frames@12.5Hz)

semantic = codes[:, 0]
acoustic = codes[:, 1:]
```

语义码本 0 是 WavLM 对齐的。你可以训练一个文本到语义的 Transformer——比直接到音频的词汇量小得多。然后一个单独的声学到波形解码器以说话人参考为条件。

### 步骤 4：为什么编解码器 token 上的 AR LM 有效

对于 Mimi 的 12.5 Hz × 8 码本下 10 秒语音片段：

```
N_tokens = 10 * 12.5 * 8 = 1000 tokens
```

> **【中文解读】** 本节展示如何用成熟框架（如 PyTorch、HuggingFace 等）快速应用该技术。在实际项目中，优先使用经过验证的框架实现，可以减少 bug 并提高开发效率。

1000 个 token 对 Transformer 来说是微不足道的上下文。一个 2.56 亿参数的 Transformer 可以在现代 GPU 上在毫秒内生成 10 秒语音。

> **【拓展：语音与情感计算】** 语音不仅传递文字信息，还携带丰富的情感信号（语调、语速、音高变化）。情感语音识别（Speech Emotion Recognition, SER）在客服质检、心理健康监测、智能教育等领域有广泛应用。当前 SOTA 模型通常基于 wav2vec 2.0 或 HuBERT 等预训练模型微调。

## 用框架实现

问题 -> 编解码器映射：

| 任务 | 编解码器 |
|------|----------|
| 通用音乐生成 | EnCodec-24k |
| 最高保真重建 | DAC-44.1k |
| 语音上的 AR LM（TTS） | SNAC 或 Mimi |
| 流式全双工语音 | Mimi（12.5 Hz） |
| 带文本的音效库 | EnCodec + T5 条件 |
| 精细音频编辑 | DAC + 修复 |

经验法则：**如果你在构建生成模型，从 Mimi 或 SNAC 开始。如果你在构建压缩流水线，使用 Opus。**

## 陷阱

- **码本太多。** 添加码本线性增加保真度但 LM 序列长度也线性增加。停在 8-12。
- **帧率不匹配。** 在 12.5 Hz Mimi 上训练 LM 然后在 50 Hz EnCodec 上微调会静默失败。
- **假设所有码本平等。** 在 Mimi 中，码本 0 携带内容；丢失它会摧毁可懂度。丢失码本 7 几乎不可察觉。
- **仅用重建质量作为唯一指标。** 编解码器可以有出色的重建但如果语义结构差就对基于 LM 的生成无用。

> **【中文解读】** 本节关注如何将模型部署为可用的产品。从原型到生产级系统需要考虑性能优化、错误处理、监控等多个维度。

## 产出物

保存为 `outputs/skill-codec-picker.md`。为给定的生成或压缩任务选择编解码器。

## 练习题

1. **简单。** 运行 `code/main.py`。它实现一个玩具标量 + 残差量化器，测量随着码本增加的重建误差。
2. **中等。** 安装 `encodec`，在一段留出语音片段上比较 1、4、8、32 个码本。绘制 PESQ 或 MSE vs 比特率。
3. **困难。** 加载 Mimi。编码一段片段。将码本 0 替换为随机整数；解码。然后同样替换码本 7。比较两种破坏——码本 0 的破坏应摧毁可懂度；码本 7 的破坏应几乎不变。

> **【中文解读】** 术语表中的 "What people say" vs "What it actually means" 区分了日常口语和精确技术含义。在团队协作中，统一术语定义可以避免大量沟通误解。

## 术语速查表

| 术语 | 通俗说法 | 实际含义 |
|------|----------|----------|
| RVQ | 残差量化 | 小码本级联；每个量化前一个残差。 |
| 帧率 | 编解码器速度 | 每秒多少 token 帧。越低 = LM 越快。 |
| 语义码本 | 码本 0（Mimi） | 从 SSL 特征蒸馏的码本；编码内容。 |
| 声学码本 | 其他所有 | 音色、韵律、噪声、精细细节。 |
| PESQ / ViSQOL | 感知质量 | 与 MOS 相关的客观指标。 |
| EnCodec | Meta 编解码器 | RVQ 基线；MusicGen 使用。 |
| Mimi | Kyutai 编解码器 | 12.5 Hz 帧率；语义-声学分离；驱动 Moshi。 |

> **【中文解读】** 延伸阅读提供了深入学习的高质量资源。这些论文和教程是该领域的经典参考文献，适合需要深入理解的读者。

## 延伸阅读

- [Defossez et al. (2023). EnCodec](https://arxiv.org/abs/2210.13438) —— RVQ 基线。
- [Kumar et al. (2023). Descript Audio Codec (DAC)](https://arxiv.org/abs/2306.06546) —— 最高保真开源。
- [Siuzdak (2024). SNAC](https://arxiv.org/abs/2410.14411) —— 多尺度 RVQ。
- [Kyutai (2024). Mimi 编解码器](https://kyutai.org/codec-explainer) —— 语义-声学分离，WavLM 蒸馏。
- [Borsos et al. (2023). AudioLM](https://arxiv.org/abs/2209.03143) —— 两阶段语义/声学范式。
- [Zeghidour et al. (2021). SoundStream](https://arxiv.org/abs/2107.03312) —— 原始可流式 RVQ 编解码器。

> **【中文解读】** 延伸阅读提供了深入学习的高质量资源，包括论文、教程和工具。建议按需选读，优先阅读标注为 "the critical read" 的核心论文。
