# 音乐生成 — MusicGen、Stable Audio、Suno 与版权地震

> 2026 年的音乐生成：Suno v5 和 Udio v4 主导商业产品；MusicGen、Stable Audio Open 和 ACE-Step 领先开源。技术问题基本解决，但法律问题（Warner Music 5 亿美元和解案）在 2025-2026 年重塑了这个领域。

> **【中文解读】** 2026 年的音乐生成：Suno v5 和 Udio v4 主导商业产品；MusicGen、Stable Audio Open 和 ACE-Step 领先开源。技术问题基本解决，但法律问题（Warner Music 5 亿美元和解案）在 2025-2026 年重塑了这个领域。

> **【拓展：AI 音乐的法律风暴】** AI 生成音乐的版权问题引发了音乐行业的地震。训练数据中的版权音乐是否构成侵权？AI 生成的音乐版权归谁？这些问题正在全球法庭上激烈辩论。

**类型：** 构建
**语言：** Python
**前置条件：** 阶段 6 · 02（频谱图），阶段 4 · 10（扩散模型）
**时长：** 约 75 分钟

## 问题引入

文本 -> 30 秒到 4 分钟的音乐片段，带歌词、人声和结构。三个子问题：

> **【中文解读】** 本节提出的问题是：如何在实际工程中正确理解和应用这一技术。理解问题背景有助于把握技术选型的关键决策点。在实际 AI 系统中，错误的技术选型往往比实现细节的 bug 代价更高。

1. **器乐生成。** 文本如"lo-fi hip-hop 鼓点配温暖键盘" -> 音频。MusicGen、Stable Audio、AudioLDM。
2. **歌曲生成（带人声 + 歌词）。** "关于德克萨斯雨夜的乡村歌曲" -> 完整歌曲。Suno、Udio、YuE、ACE-Step。
3. **条件化 / 可控。** 扩展现有片段、重新生成桥段、切换风格、分离音轨或修复。Udio 的修复 + 音轨分离是 2026 年需要追赶的功能。

## 核心概念

> **【中文解读】** 本节介绍核心概念和理论基础。掌握这些概念是后续动手实现的前提，同时也是面试和工程实践中高频考察的知识点。

![音乐生成：token-LM vs 扩散，2026 模型地图](../assets/music-generation.svg)

### 神经编解码器 token 上的 Token LM

Meta 的 **MusicGen**（2023，MIT）和许多衍生品：以文本/旋律嵌入为条件，自回归预测 EnCodec token（32 kHz，4 个码本），用 EnCodec 解码。3 亿 - 33 亿参数。强基线；超过 30 秒后挣扎。

**ACE-Step**（开源，40 亿 XL 于 2026 年 4 月发布）为此扩展了完整歌曲的歌词条件生成。开源社区最接近 Suno 的产品。

### Mel 或潜空间上的扩散

**Stable Audio（2023）** 和 **Stable Audio Open（2024）**：压缩音频上的潜扩散。擅长循环、声音设计、氛围质感。不擅长结构化完整歌曲。

**AudioLDM / AudioLDM2**：通过 T2I 风格的潜扩散实现文本到音频，泛化到音乐、音效、语音。

### 混合（生产） — Suno、Udio、Lyria

闭源。可能是 AR 编解码器 LM + 基于扩散的声码器配合专门的语音/鼓/旋律头。Suno v5（2026）是 ELO 1293 质量领军者。Udio v4 添加了修复 + 音轨分离（贝斯、鼓、人声分别下载）。

### 评估

- **FAD（Frechet 音频距离）。** 使用 VGGish 或 PANNs 特征的生成 vs 真实音频分布之间的嵌入级距离。越低越好。MusicGen small：MusicCaps 上 FAD 4.5；SOTA 约 3.0。
- **音乐性（主观）。** 人类偏好。Suno v5 ELO 1293 领先。
- **文本-音频对齐。** 提示和输出之间的 CLAP 分数。
- **音乐性伪影。** 节拍外过渡、人声短语漂移、30 秒后结构丢失。

> **【拓展：语音 AI 的产品化】** 语音技术在产品化中面临独特挑战：不同口音、背景噪声、远场拾音、多人说话等。Siri、Alexa、小爱同学等产品都投入了大量工程优化来解决这些 "长尾问题"。实时性要求（<300ms 延迟）也是语音产品的核心指标。

> **【拓展：多语言语音技术】** 全球语言的语音特性差异巨大：声调语言（如中文）的音高携带语义，低资源语言缺乏训练数据。Meta 的 MMS 模型支持 1000+ 种语言的语音识别，Whisper 在多语言场景表现出色，但仍需针对特定语言微调。

## 2026 模型地图

| 模型 | 参数 | 长度 | 人声 | 许可 |
|------|------|------|------|------|
| MusicGen-large | 33 亿 | 30 秒 | 否 | MIT |
| Stable Audio Open | 12 亿 | 47 秒 | 否 | Stability 非商业 |
| ACE-Step XL（2026 年 4 月） | 40 亿 | > 2 分钟 | 是 | Apache-2.0 |
| YuE | 70 亿 | > 2 分钟 | 是，多语言 | Apache-2.0 |
| Suno v5（闭源） | ? | 4 分钟 | 是，ELO 1293 | 商业 |
| Udio v4（闭源） | ? | 4 分钟 | 是 + 音轨分离 | 商业 |
| Google Lyria 3（闭源） | ? | 实时 | 是 | 商业 |
| MiniMax Music 2.5 | ? | 4 分钟 | 是 | 商业 API |

## 法律格局（2025-2026）

- **Warner Music vs Suno 和解。** 5 亿美元。WMG 现在对 Suno 上的 AI 形象、音乐权利和用户生成内容有监督权。UMG 对 Udio 有类似和解。
- **欧盟 AI 法案** + **加利福尼亚州 SB 942**：AI 生成的音乐必须披露。
- **Riffusion / MusicGen** 在 MIT 下没有合规包袱，但也没有商业人声。

安全交付模式：

1. 仅生成器乐（MusicGen、Stable Audio Open，MIT/CC0 输出）。
2. 使用商业 API（Suno、Udio、ElevenLabs Music）带逐次生成的许可。
3. 在自有或授权目录上训练（大多数企业最终走到这里）。
4. 为生成内容打上水印 + 元数据标签。

> **【中文解读】** 本节通过代码从零实现核心算法。这种 "from scratch" 的方式能帮助理解框架背后的原理，遇到问题时不会被黑盒困住。

## 动手实现

### 步骤 1：用 MusicGen 生成

```python
from audiocraft.models import MusicGen
import torchaudio

model = MusicGen.get_pretrained("facebook/musicgen-small")
model.set_generation_params(duration=10)
wav = model.generate(["upbeat synthwave with driving drums, 128 BPM"])
torchaudio.save("out.wav", wav[0].cpu(), 32000)
```

三个大小：`small`（3 亿，快）、`medium`（15 亿）、`large`（33 亿）。Small 足以验证"想法是否成立"。

### 步骤 2：旋律条件化

```python
melody, sr = torchaudio.load("humming.wav")
wav = model.generate_with_chroma(
    ["jazz piano cover"],
    melody.squeeze(),
    sr,
)
```

MusicGen-melody 接受色度图并保留旋律同时替换音色。适用于"把这段旋律变成弦乐四重奏"。

### 步骤 3：FAD 评估

```python
from frechet_audio_distance import FrechetAudioDistance
fad = FrechetAudioDistance()

fad.get_fad_score("generated_folder/", "reference_folder/")
```

计算 VGGish 嵌入距离。适用于类型级回归测试；不能替代人类听众。

### 步骤 4：添加到 LLM-音乐工作流

结合第 7-8 课的想法：

> **【中文解读】** 本节展示如何用成熟框架（如 PyTorch、HuggingFace 等）快速应用该技术。在实际项目中，优先使用经过验证的框架实现，可以减少 bug 并提高开发效率。

```python
prompt = "Write a 30-second jazz loop. Describe the drums, bass, and piano voicing."
description = llm.complete(prompt)
music = musicgen.generate([description], duration=30)
```

> **【拓展：语音与情感计算】** 语音不仅传递文字信息，还携带丰富的情感信号（语调、语速、音高变化）。情感语音识别（Speech Emotion Recognition, SER）在客服质检、心理健康监测、智能教育等领域有广泛应用。当前 SOTA 模型通常基于 wav2vec 2.0 或 HuBERT 等预训练模型微调。

## 用框架实现

| 目标 | 技术栈 |
|------|--------|
| 器乐声音设计 | Stable Audio Open |
| 游戏 / 自适应音乐 | Google Lyria RealTime（闭源） |
| 带人声的完整歌曲（商业） | Suno v5 或 Udio v4 附带明确许可 |
| 带人声的完整歌曲（开源） | ACE-Step XL 或 YuE |
| 短广告 jingle | MusicGen 对哼唱参考的旋律条件化 |
| 音乐视频背景 | MusicGen + Stable Video Diffusion |

## 2026 年仍在出现的陷阱

- **版权清洗提示。** "Taylor Swift 风格的歌曲"——商业 Suno/Udio 现在会过滤这些，开源模型不会。添加你自己的过滤列表。
- **30 秒后重复 / 漂移。** AR 模型会循环。交叉淡化多个生成，或使用 ACE-Step 实现结构一致性。
- **节拍漂移。** 模型偏离 BPM。在提示中使用 BPM 标签并用 librosa 的 `beat_track` 做后过滤。
- **人声可懂度。** Suno 优秀；开源模型的歌词往往含糊。如果歌词重要，使用商业 API 或微调。
- **单声道输出。** 开源模型生成单声道或假立体声。用适当的立体声重建升级（ezst、Cartesia 的立体声扩散）。

> **【中文解读】** 本节关注如何将模型部署为可用的产品。从原型到生产级系统需要考虑性能优化、错误处理、监控等多个维度。

## 产出物

保存为 `outputs/skill-music-designer.md`。为音乐生成部署选择模型、许可策略、长度/结构计划和披露元数据。

## 练习题

1. **简单。** 运行 `code/main.py`。它生成一个"生成式"和弦进行 + 鼓点模式作为 ASCII 符号——音乐生成的卡通图。如果愿意可以通过任何 MIDI 渲染器回放。
2. **中等。** 安装 `audiocraft`，用 MusicGen-small 在 4 个风格提示上生成 10 秒片段，测量与参考风格集的 FAD。
3. **困难。** 使用 ACE-Step（或 MusicGen-melody），用不同音色提示生成同一旋律的三个变体。计算 CLAP 与提示的相似度以验证对齐。

> **【中文解读】** 术语表中的 "What people say" vs "What it actually means" 区分了日常口语和精确技术含义。在团队协作中，统一术语定义可以避免大量沟通误解。

## 术语速查表

| 术语 | 通俗说法 | 实际含义 |
|------|----------|----------|
| FAD | 音频 FID | 真实 vs 生成音频嵌入分布之间的 Frechet 距离。 |
| 色度图（Chromagram） | 旋律的音高 | 12 维逐帧向量；旋律条件化的输入。 |
| 音轨（Stems） | 乐器轨道 | 分离的贝斯/鼓/人声/旋律作为 WAV。 |
| 修复（Inpainting） | 重生成一段 | 遮蔽一个时间窗口；模型只重生成那部分。 |
| CLAP | 文本-音频 CLIP | 对比音频-文本嵌入；评估文本-音频对齐。 |
| EnCodec | 音乐编解码器 | Meta 的神经编解码器，MusicGen 使用；32 kHz，4 个码本。 |

> **【中文解读】** 延伸阅读提供了深入学习的高质量资源。这些论文和教程是该领域的经典参考文献，适合需要深入理解的读者。

## 延伸阅读

- [Copet et al. (2023). MusicGen](https://arxiv.org/abs/2306.05284) —— 开源自回归基准。
- [Evans et al. (2024). Stable Audio Open](https://arxiv.org/abs/2407.14358) —— 声音设计默认选择。
- [ACE-Step](https://github.com/ace-step/ACE-Step) —— 开源 40 亿参数完整歌曲生成器，2026 年 4 月。
- [Suno v5 平台文档](https://suno.com) —— 商业质量领军者。
- [AudioLDM2](https://arxiv.org/abs/2308.05734) —— 音乐 + 音效的潜扩散。
- [WMG-Suno 和解报道](https://www.musicbusinessworldwide.com/suno-warner-music-settlement/) —— 2025 年 11 月先例。

> **【中文解读】** 延伸阅读提供了深入学习的高质量资源，包括论文、教程和工具。建议按需选读，优先阅读标注为 "the critical read" 的核心论文。
