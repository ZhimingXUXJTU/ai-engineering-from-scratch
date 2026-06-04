# 音频生成

> 音频是 16-48kHz 的 1D 信号。一段 5 秒的片段有 8-24 万个采样点。没有 Transformer 能直接处理这么长的序列。2026 年所有生产音频模型的解决方案相同：神经编解码器（EnCodec 等）将音频压缩为 50-75Hz 的离散 token，然后用 Transformer 或扩散模型生成 token。

> **【中文解读】** 音频是 16-48kHz 的 1D 信号，5 秒就是 8-24 万个采样点。没有 Transformer 能直接处理这么长的序列。2026 年所有音频生成模型的解决方案相同：神经编解码器（EnCodec 等）压缩为 50-75Hz 的离散 token，然后用 Transformer 生成。

> **【拓展：MusicGen 与 AudioCraft】** Meta 的 MusicGen 和 AudioCraft 使用 EnCodec + Transformer 架构生成音乐和音效。音频 token 化是音频生成领域的关键创新。

**类型：** 构建
**语言：** Python
**前置要求：** 阶段 6 · 02（音频特征）、阶段 6 · 04（ASR）、阶段 8 · 06（DDPM）
**预计时间：** ~45 分钟

## 问题引入

三个音频生成任务：

1. **文本转语音 (TTS)。** 给定文本，生成语音。干净语音是窄带的，有很强的音素结构——Transformer-over-token 方案解决得很好。VALL-E (Microsoft)、NaturalSpeech 3、ElevenLabs、OpenAI TTS。
2. **音乐生成。** 给定提示（文本、旋律、和弦进行、流派），生成音乐。分布宽得多。MusicGen (Meta)、Stable Audio 2.5、Suno v4、Udio、Riffusion。
3. **音效 / 声音设计。** 给定提示，生成环境声或拟音。AudioGen、AudioLDM 2、Stable Audio Open。

三者运行在相同的基础架构上：神经音频编解码器 + token 自回归或扩散生成器。

> **【中文解读】** 音频生成的三大任务——语音合成（TTS）、音乐生成、音效生成——都基于相同的基础架构：神经音频编解码器（如 EnCodec）将音频压缩为离散 token，然后 Transformer 或扩散模型在 token 序列上生成。这与语言模型的"tokenizer + Transformer"模式完全一致。

> **【拓展：ElevenLabs 与语音克隆技术】** ElevenLabs 是 2026 年最流行的 AI 语音平台。它只需几秒钟的参考音频就能克隆说话人的声音，然后用克隆的声音合成任意文本。底层技术结合了神经编解码器和条件语言模型。语音克隆在有声书、配音、虚拟人等领域有广泛应用，但也引发了深度伪造（deepfake）的伦理担忧。

## 核心概念

![音频生成：编解码器 token + Transformer 或扩散](../assets/audio-generation.svg)

### 神经音频编解码器

EnCodec (Meta, 2022)、SoundStream (Google, 2021)、Descript Audio Codec (DAC, 2023)。卷积编码器将波形压缩为逐时间步向量；残差向量量化 (RVQ) 将每个向量转换为 K 个码本索引的级联。解码器反转这个过程。24 kHz 音频以 2 kbps 使用 8 个 RVQ 码本，75 Hz = 600 token/秒。

```
waveform (16000 samples/sec)
    └─ encoder conv ─┐
                     ├─ RVQ layer 1 → indices at 75 Hz
                     ├─ RVQ layer 2 → indices at 75 Hz
                     ├─ ...
                     └─ RVQ layer 8
```

### 之上的两种生成范式

**Token 自回归。** 将 RVQ token 展平为序列，运行仅解码器 Transformer。MusicGen 使用"延迟并行"以每流偏移并行发射 K 个码本流。VALL-E 从文本提示 + 3 秒语音样本生成语音 token。

**潜在扩散。** 将编解码器 token 打包为连续潜在表示或用分类扩散建模。Stable Audio 2.5 使用连续音频潜在表示上的流匹配。AudioLDM 2 使用文本到梅尔频谱到音频的扩散。

2024-2026 年趋势：流匹配在音乐方面胜出（推理更快，样本更干净），而 token 自回归仍在语音中占主导，因为它天然是因果的且支持流式输出。

## 生产级音频生成格局

| 系统 | 任务 | 主干 | 延迟 |
|--------|------|----------|---------|
| ElevenLabs V3 | TTS | Token-AR + 神经声码器 | ~300ms 首 token |
| OpenAI GPT-4o audio | 全双工语音 | 端到端多模态 AR | ~200ms |
| NaturalSpeech 3 | TTS | 潜在流匹配 | 非流式 |
| Stable Audio 2.5 | 音乐 / SFX | DiT + 音频潜在表示上的流匹配 | ~10s 生成 1 分钟片段 |
| Suno v4 | 完整歌曲 | 未公开；疑似 token-AR | ~30s 每首歌 |
| Udio v1.5 | 完整歌曲 | 未公开 | ~30s 每首歌 |
| MusicGen 3.3B | 音乐 | EnCodec 32kHz 上的 token-AR | 实时 |
| AudioCraft 2 | 音乐 + SFX | 流匹配 | ~5s 生成 5s 片段 |
| Riffusion v2 | 音乐 | 频谱图扩散 | ~10s |

## 动手实现

`code/main.py` 模拟了核心思想：在从两种不同"风格"生成的合成"音频 token"序列上训练一个微型下一 token Transformer（风格 A 为交替的高低 token，风格 B 为单调递增）。以风格为条件并采样。

### 步骤 1：合成音频 token

```python
def make_tokens(style, length, vocab_size, rng):
    if style == 0:  # "类语音"：交替
        return [i % vocab_size for i in range(length)]
    # "类音乐"：递增
    return [(i * 3) % vocab_size for i in range(length)]
```

### 步骤 2：训练微型 token 预测器

以风格为条件的大 gram 风格预测器。重点是模式：编解码器 token → 交叉熵训练 → 自回归采样。

### 步骤 3：条件采样

给定风格 token 和起始 token，从预测分布中采样下一个 token。继续 20-40 个 token。

## 常见陷阱

- **编解码器质量限制输出质量。** 如果编解码器无法忠真表示声音，生成器质量再高也没用。DAC 是当前开源最佳。
- **RVQ 误差累积。** 每个 RVQ 层建模前一层的残差。第 1 层的误差会传播。在更高层使用温度 0 采样有帮助。
- **音乐结构。** 30 秒的 token 在 75 Hz 下是 20k+ token。对 Transformer 来说很难。MusicGen 使用滑动窗口 + 提示延续；Stable Audio 使用更短片段 + 交叉淡入。
- **边界伪影。** 生成片段之间的交叉淡入需要仔细的重叠相加。
- **干净数据的胃口。** 音乐生成器需要数万小时的授权音乐。Suno / Udio 的 RIAA 诉讼（2024）将此推到了台面。
- **语音克隆伦理。** 3 秒样本加文本提示足以让 VALL-E / XTTS / ElevenLabs 克隆声音。每个生产模型都需要滥用检测 + 退出名单。

## 用框架实现

| 任务 | 2026 年技术栈 |
|------|------------|
| 商业 TTS | ElevenLabs、OpenAI TTS 或 Azure Neural |
| 语音克隆（经授权验证） | XTTS v2（开源）或 ElevenLabs Pro |
| 背景音乐，快速 | Stable Audio 2.5 API、Suno 或 Udio |
| 带歌词的音乐 | Suno v4 或 Udio v1.5 |
| 音效 / 拟音 | AudioCraft 2、ElevenLabs SFX 或 Stable Audio Open |
| 实时语音代理 | GPT-4o realtime 或 Gemini Live |
| 开源权重音乐研究 | MusicGen 3.3B、Stable Audio Open 1.0、AudioLDM 2 |
| 配音 / 翻译 | HeyGen、ElevenLabs Dubbing |

## 产出物

保存 `outputs/skill-audio-brief.md`。技能接收音频需求（任务、时长、风格、声音、许可证），输出：模型 + 托管方案、提示格式（流派标签、风格描述词、结构标记）、编解码器 + 生成器 + 声码器链、种子协议和评估计划（MOS / CLAP score / TTS 的 CER / 用户 A/B 测试）。

## 练习题

1. **简单。** 运行 `code/main.py` 并显式设置风格。验证生成的序列匹配该风格的模式。
2. **中等。** 添加延迟并行解码：模拟 2 个必须偏移 1 步的 token 流。训练一个联合预测器。
3. **困难。** 使用 HuggingFace transformers 在本地运行 MusicGen-small。用三个不同提示生成 10 秒片段；A/B 测试风格遵循度。

## 术语速查表

| 术语 | 人们怎么说 | 实际含义 |
|------|-----------------|-----------------------|
| 编解码器 | "神经压缩" | 音频的编码器/解码器；典型输出为 50-75 Hz token。 |
| RVQ | "残差 VQ" | K 个量化器的级联；每个建模前一个的残差。 |
| Token | "一个编解码器符号" | 码本中的离散索引；典型值 1024 或 2048。 |
| 延迟并行 | "偏移码本" | 以交错偏移发射 K 个 token 流以减少序列长度。 |
| 流匹配 | "2024 年音频的赢家" | 扩散的更直路径替代方案；采样更快。 |
| 语音提示 | "3 秒样本" | 引导克隆声音的说话人嵌入或 token 前缀。 |
| 梅尔频谱图 | "可视化版本" | 对数幅度感知频谱图；许多 TTS 系统使用。 |
| 声码器 | "梅尔到波形" | 将梅尔频谱图转换回音频的神经组件。 |

## 生产笔记：音频是流式问题

音频是用户期望在*生成过程中*接收的输出模态，而非一次性全部到达。用生产术语来说，这意味着 TPOT（每个输出 token 的时间）很重要，因为用户的收听速度是目标吞吐量——而非阅读速度。对于 16kHz 音频以 ~75 token/秒 tokenize（EnCodec），服务器必须为每个用户生成 ≥75 token/秒才能保持播放流畅。

两个架构后果：

- **流匹配音频模型不能轻易流式输出。** Stable Audio 2.5 和 AudioCraft 2 在一次传播中渲染固定片段长度。要流式输出，你需要将片段分块并在边界处重叠——类似于滑动窗口扩散——相比编解码器 AR 模型增加 100-300ms 延迟开销。

如果产品是"实时语音聊天"或"实时音乐续写"，选择编解码器 AR 路径。如果是"提交时渲染 30 秒片段"，流匹配在质量和总延迟上胜出。

## 延伸阅读

- [Défossez et al. (2022). Encodec: High Fidelity Neural Audio Compression](https://arxiv.org/abs/2210.13438) — 编解码器标准。
- [Zeghidour et al. (2021). SoundStream](https://arxiv.org/abs/2107.03312) — 第一个广泛使用的神经音频编解码器。
- [Kumar et al. (2023). High-Fidelity Audio Compression with Improved RVQGAN (DAC)](https://arxiv.org/abs/2306.06546) — DAC。
- [Wang et al. (2023). Neural Codec Language Models are Zero-Shot Text to Speech Synthesizers (VALL-E)](https://arxiv.org/abs/2301.02111) — VALL-E。
- [Copet et al. (2023). Simple and Controllable Music Generation (MusicGen)](https://arxiv.org/abs/2306.05284) — MusicGen。
- [Liu et al. (2023). AudioLDM 2: Learning Holistic Audio Generation with Self-supervised Pretraining](https://arxiv.org/abs/2308.05734) — AudioLDM 2。
- [Stability AI (2024). Stable Audio 2.5](https://stability.ai/news/introducing-stable-audio-2-5) — 2025 年带流匹配的文本转音乐。
