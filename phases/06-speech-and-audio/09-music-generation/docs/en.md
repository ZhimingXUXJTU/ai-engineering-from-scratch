# Music Generation — MusicGen, Stable Audio, Suno, and the Licensing Earthquake | 音乐生成 — MusicGen、Stable Audio、Suno 与版权地震

> 2026 music generation: Suno v5 and Udio v4 dominate commercial; MusicGen, Stable Audio Open, and ACE-Step lead open-source. The technical problem is mostly solved. The legal problem (Warner Music $500M settlement, UMG settlement) reshaped the field in 2025-2026.

> **【中文解读】** 2026 年的音乐生成：Suno v5 和 Udio v4 主导商业产品；MusicGen、Stable Audio Open 和 ACE-Step 领先开源。技术问题基本解决，但法律问题（Warner Music 5 亿美元和解案）在 2025-2026 年重塑了这个领域。

> **【拓展：AI 音乐的法律风暴】** AI 生成音乐的版权问题引发了音乐行业的地震。训练数据中的版权音乐是否构成侵权？AI 生成的音乐版权归谁？这些问题正在全球法庭上激烈辩论。

**Type:** Build | **类型:** 构建
**Languages:** Python | **语言:** Python
**Prerequisites:** Phase 6 · 02 (Spectrograms), Phase 4 · 10 (Diffusion Models) | **前置知识:** 阶段 6 · 02（频谱图），阶段 4 · 10（扩散模型）
**Time:** ~75 minutes | **预计用时:** ~75 分钟

## The Problem | 问题引入

Text → a 30-second to 4-minute music clip, with lyrics, vocals, and structure. Three sub-problems:

> 文本 → 30 秒到 4 分钟的音乐片段，带歌词、人声和结构。三个子问题：

> **【中文解读】** 本节提出的问题是：如何在实际工程中正确理解和应用这一技术。理解问题背景有助于把握技术选型的关键决策点。在实际 AI 系统中，错误的技术选型往往比实现细节的 bug 代价更高。

1. **Instrumental generation.** Text like "lo-fi hip-hop drums with warm keys" → audio. MusicGen, Stable Audio, AudioLDM.
   **器乐生成。** 像"lo-fi hip-hop drums with warm keys"这样的文本 → 音频。MusicGen、Stable Audio、AudioLDM。
2. **Song generation (with vocals + lyrics).** "Country song about rainy Texas nights" → full song. Suno, Udio, YuE, ACE-Step.
   **歌曲生成（带人声+歌词）。** "Country song about rainy Texas nights" → 完整歌曲。Suno、Udio、YuE、ACE-Step。
3. **Conditional / controllable.** Extend an existing clip, regenerate a bridge, swap genre, stem-separate, or inpaint. Udio's inpainting + stem separation is the 2026 feature to match.
   **条件/可控生成。** 扩展现有片段、重新生成桥段、切换风格、分轨或内画。Udio 的内画 + 分轨是 2026 年要追赶的功能。

## The Concept | 核心概念

> **【中文解读】** 本节介绍核心概念和理论基础。掌握这些概念是后续动手实现的前提，同时也是面试和工程实践中高频考察的知识点。


![Music generation: token-LM vs diffusion, the 2026 model map](../assets/music-generation.svg)

### Token LM over neural-codec tokens

> ### 基于神经编解码 token 的 Token LM

Meta's **MusicGen** (2023, MIT) and many derivatives: condition on text/melody embeddings, autoregressively predict EnCodec tokens (32 kHz, 4 codebooks), decode with EnCodec. 300M - 3.3B params. Strong baseline; struggles past 30 seconds.

> Meta 的 **MusicGen**（2023，MIT）和许多衍生品：以文本/旋律嵌入为条件，自回归预测 EnCodec token（32 kHz，4 个码本），用 EnCodec 解码。3 亿到 33 亿参数。强基线；超过 30 秒效果下降。

**ACE-Step** (open-source, 4B XL released April 2026) extends this for full-song lyric-conditioned generation. The open community's closest thing to Suno.

> **ACE-Step**（开源，2026 年 4 月发布的 40 亿 XL 版本）将此扩展为全曲歌词条件生成。开源社区最接近 Suno 的产品。

### Diffusion over mels or latents

> ### 基于 Mel 或潜变量的扩散

**Stable Audio (2023)** and **Stable Audio Open (2024)**: latent diffusion on compressed audio. Excels at loops, sound design, ambient textures. Not great at structured full songs.

> **Stable Audio（2023）** 和 **Stable Audio Open（2024）**：压缩音频上的潜变量扩散。擅长循环、声音设计、氛围质感。不太擅长结构化完整歌曲。

**AudioLDM / AudioLDM2**: text-to-audio via T2I-style latent diffusion, generalized to music, sound effects, speech.

> **AudioLDM / AudioLDM2**：通过 T2I 风格的潜变量扩散进行文本到音频生成，泛化到音乐、音效、语音。

### Hybrid (production) — Suno, Udio, Lyria

> ### 混合（生产）—— Suno、Udio、Lyria

Closed weights. Likely AR codec LM + diffusion-based vocoder with specialized voice / drum / melody heads. Suno v5 (2026) is the ELO 1293 quality leader. Udio v4 adds inpainting + stem separation (bass, drums, vocals separate downloads).

> 闭源权重。可能是 AR 编解码 LM + 基于扩散的声码器，配有专门的语音/鼓/旋律头。Suno v5（2026）是 ELO 1293 质量领先者。Udio v4 增加了内画 + 分轨（贝斯、鼓、人声分别下载）。

### Evaluation

> ### 评估

- **FAD (Fréchet Audio Distance).** Embedding-level distance between generated vs real audio distribution using VGGish or PANNs features. Lower is better. MusicGen small: 4.5 FAD on MusicCaps; SOTA ~3.0.
  **FAD（Fréchet 音频距离）。** 使用 VGGish 或 PANNs 特征的生成 vs 真实音频分布的嵌入级距离。越低越好。MusicGen small：MusicCaps 上 4.5 FAD；SOTA 约 3.0。
- **Musicality (subjective).** Human preference. Suno v5 ELO 1293 leads.
  **音乐性（主观）。** 人类偏好。Suno v5 ELO 1293 领先。
- **Text-audio alignment.** CLAP score between prompt and output.
  **文本-音频对齐。** 提示与输出之间的 CLAP 分数。
- **Musicality artifacts.** Off-beat transitions, vocal-phrase drift, loss of structure past 30 s.
  **音乐性伪影。** 跑拍过渡、人声短语漂移、超过 30 秒后结构丢失。

> **【拓展：语音 AI 的产品化】** 语音技术在产品化中面临独特挑战：不同口音、背景噪声、远场拾音、多人说话等。Siri、Alexa、小爱同学等产品都投入了大量工程优化来解决这些 "长尾问题"。实时性要求（<300ms 延迟）也是语音产品的核心指标。

> **【拓展：多语言语音技术】** 全球语言的语音特性差异巨大：声调语言（如中文）的音高携带语义，低资源语言缺乏训练数据。Meta 的 MMS 模型支持 1000+ 种语言的语音识别，Whisper 在多语言场景表现出色，但仍需针对特定语言微调。



## 2026 model map

> 2026 年模型地图

| Model | Params | Length | Vocals | License |
|-------|--------|--------|--------|---------|
| MusicGen-large | 3.3B | 30 s | no | MIT |
| Stable Audio Open | 1.2B | 47 s | no | Stability non-commercial |
| ACE-Step XL (Apr 2026) | 4B | > 2 min | yes | Apache-2.0 |
| YuE | 7B | > 2 min | yes, multilingual | Apache-2.0 |
| Suno v5 (closed) | ? | 4 min | yes, ELO 1293 | commercial |
| Udio v4 (closed) | ? | 4 min | yes + stems | commercial |
| Google Lyria 3 (closed) | ? | real-time | yes | commercial |
| MiniMax Music 2.5 | ? | 4 min | yes | commercial API |

| 模型 | 参数量 | 时长 | 人声 | 许可 |
|------|--------|------|------|------|
| MusicGen-large | 33 亿 | 30 秒 | 无 | MIT |
| Stable Audio Open | 12 亿 | 47 秒 | 无 | Stability 非商业 |
| ACE-Step XL（2026.04） | 40 亿 | > 2 分钟 | 有 | Apache-2.0 |
| YuE | 70 亿 | > 2 分钟 | 有，多语言 | Apache-2.0 |
| Suno v5（闭源） | ? | 4 分钟 | 有，ELO 1293 | 商业 |
| Udio v4（闭源） | ? | 4 分钟 | 有 + 分轨 | 商业 |
| Google Lyria 3（闭源） | ? | 实时 | 有 | 商业 |
| MiniMax Music 2.5 | ? | 4 分钟 | 有 | 商业 API |

## The legal landscape (2025-2026)

> ## 法律环境（2025-2026）

- **Warner Music vs Suno settlement.** $500M. WMG now has oversight of AI-likeness, music rights, and user-generated tracks on Suno. Similar UMG settlement on Udio.
  **Warner Music 诉 Suno 和解。** 5 亿美元。WMG 现在对 Suno 上的 AI 相似性、音乐版权和用户生成内容有监督权。UMG 对 Udio 有类似和解。
- **EU AI Act** + **California SB 942**: AI-generated music must be disclosed.
  **EU AI 法案** + **加利福尼亚 SB 942**：AI 生成的音乐必须披露。
- **Riffusion / MusicGen** under MIT have no compliance baggage but also no commercial vocals.
  **Riffusion / MusicGen** 在 MIT 许可下没有合规负担，但也没有商业人声。

Safe-to-ship patterns:

> 安全发布模式：

1. Generate instrumental only (MusicGen, Stable Audio Open, MIT/CC0 outputs).
   仅生成器乐（MusicGen、Stable Audio Open、MIT/CC0 输出）。
2. Use commercial APIs (Suno, Udio, ElevenLabs Music) with per-generation license.
   使用带每次生成许可的商业 API（Suno、Udio、ElevenLabs Music）。
3. Train on owned or licensed catalog (most enterprises end up here).
   在自有或授权目录上训练（大多数企业最终走到这一步）。
4. Tag generations with watermarks + metadata.
   用水印 + 元数据标记生成内容。

> **【中文解读】** 本节通过代码从零实现核心算法。这种 "from scratch" 的方式能帮助理解框架背后的原理，遇到问题时不会被黑盒困住。


## Build It | 动手实现

### Step 1: generate with MusicGen

```python
from audiocraft.models import MusicGen
import torchaudio

model = MusicGen.get_pretrained("facebook/musicgen-small")
model.set_generation_params(duration=10)
wav = model.generate(["upbeat synthwave with driving drums, 128 BPM"])
torchaudio.save("out.wav", wav[0].cpu(), 32000)
```

Three sizes: `small` (300M, fast), `medium` (1.5B), `large` (3.3B). Small is enough for "does the idea land."

> 三个大小：`small`（3 亿，快速）、`medium`（15 亿）、`large`（33 亿）。`small` 足以验证"想法是否可行"。

### Step 2: melody conditioning

```python
melody, sr = torchaudio.load("humming.wav")
wav = model.generate_with_chroma(
    ["jazz piano cover"],
    melody.squeeze(),
    sr,
)
```

MusicGen-melody takes a chromagram and preserves the tune while swapping timbre. Useful for "give me this melody as a string quartet."

> MusicGen-melody 接受色度图并在交换音色时保留旋律。适用于"把这个旋律改成弦乐四重奏"。

### Step 3: FAD evaluation

```python
from frechet_audio_distance import FrechetAudioDistance
fad = FrechetAudioDistance()

fad.get_fad_score("generated_folder/", "reference_folder/")
```

Computes VGGish-embedding distance. Useful for genre-level regression tests; not a substitute for human listeners.

> 计算 VGGish 嵌入距离。适用于流派级回归测试；不能替代人类听众。

### Step 4: adding to the LLM-music workflow

Combine with the ideas from Lessons 7-8:

> **【中文解读】** 本节展示如何用成熟框架（如 PyTorch、HuggingFace 等）快速应用该技术。在实际项目中，优先使用经过验证的框架实现，可以减少 bug 并提高开发效率。


```python
prompt = "Write a 30-second jazz loop. Describe the drums, bass, and piano voicing."
description = llm.complete(prompt)
music = musicgen.generate([description], duration=30)
```




> **【拓展：语音与情感计算】** 语音不仅传递文字信息，还携带丰富的情感信号（语调、语速、音高变化）。情感语音识别（Speech Emotion Recognition, SER）在客服质检、心理健康监测、智能教育等领域有广泛应用。当前 SOTA 模型通常基于 wav2vec 2.0 或 HuBERT 等预训练模型微调。

## Use It | 用框架实现

| Goal | Stack |
|------|-------|
| Instrumental sound design | Stable Audio Open |
| Game / adaptive music | Google Lyria RealTime (closed) |
| Full songs with vocals (commercial) | Suno v5 or Udio v4 with explicit license |
| Full songs with vocals (open) | ACE-Step XL or YuE |
| Short ad jingle | MusicGen melody-conditioned on a hummed reference |
| Music-video background | MusicGen + Stable Video Diffusion |

| 目标 | 技术栈 |
|------|--------|
| 器乐声音设计 | Stable Audio Open |
| 游戏/自适应音乐 | Google Lyria RealTime（闭源） |
| 带人声的完整歌曲（商业） | Suno v5 或 Udio v4 带明确许可 |
| 带人声的完整歌曲（开源） | ACE-Step XL 或 YuE |
| 短广告曲 | MusicGen 在哼唱参考上的旋律条件 |
| 音乐视频背景 | MusicGen + Stable Video Diffusion |



## Pitfalls that still ship in 2026

> 2026 年仍然在犯的陷阱

- **Copyright-laundering prompts.** "Song in the style of Taylor Swift" — commercial Suno/Udio filter these now, open models do not. Add your own filter list.
  **版权洗钱提示。** "Song in the style of Taylor Swift"——商业 Suno/Udio 现在会过滤这些，开源模型不会。添加你自己的过滤列表。
- **Repetition / drift past 30 s.** AR models loop. Crossfade multiple generations, or use ACE-Step for structural coherence.
  **超过 30 秒的重复/漂移。** AR 模型会循环。交叉淡入多个生成，或使用 ACE-Step 保持结构一致性。
- **Tempo drift.** Models wander off the BPM. Use BPM tags in the prompt and post-filter with librosa's `beat_track`.
  **节奏漂移。** 模型偏离 BPM。在提示中使用 BPM 标签并用 librosa 的 `beat_track` 后过滤。
- **Vocal intelligibility.** Suno is excellent; open models are often mushy on words. If lyrics matter, use a commercial API or fine-tune.
  **人声清晰度。** Suno 表现出色；开源模型的歌词经常模糊。如果歌词重要，使用商业 API 或微调。
- **Mono output.** Open models generate mono or fake-stereo. Upgrade with a proper stereo reconstruction (ezst, Cartesia's stereo diffusion).
  **单声道输出。** 开源模型生成单声道或假立体声。用合适的立体声重建升级。

> **【中文解读】** 本节关注如何将模型部署为可用的产品。从原型到生产级系统需要考虑性能优化、错误处理、监控等多个维度。


## Ship It | 产出物

Save as `outputs/skill-music-designer.md`. Pick model, license strategy, length / structure plan, and disclosure metadata for a music-gen deployment.

> 保存为 `outputs/skill-music-designer.md`。为音乐生成部署选择模型、许可策略、长度/结构计划和披露元数据。

## Exercises | 练习题

1. **Easy.** Run `code/main.py`. It produces a "generative" chord progression + drum pattern as ASCII symbols — a music-gen cartoon. Play it back via any MIDI renderer if you want.
   **简单。** 运行 `code/main.py`。它以 ASCII 符号生成"生成式"和弦进行 + 鼓点——一个音乐生成的卡通。可以用 MIDI 渲染器播放。
2. **Medium.** Install `audiocraft`, generate 10-second clips across 4 genre prompts with MusicGen-small, measure FAD against a reference genre set.
   **中等。** 安装 `audiocraft`，用 MusicGen-small 在 4 个流派提示上生成 10 秒片段，对照参考流派集测量 FAD。
3. **Hard.** Using ACE-Step (or MusicGen-melody), generate three variations of the same tune with different timbre prompts. Compute CLAP similarity to the prompt to verify alignment.
   **困难。** 使用 ACE-Step（或 MusicGen-melody），用不同音色提示生成同一旋律的三个变体。计算 CLAP 相似度验证对齐。

> **【中文解读】** 术语表中的 "What people say" vs "What it actually means" 区分了日常口语和精确技术含义。在团队协作中，统一术语定义可以避免大量沟通误解。


## Key Terms | 术语速查表

| Term | What people say | What it actually means |
|------|-----------------|-----------------------|
| FAD | Audio FID | Fréchet distance between embedding distributions of real vs generated. |
| Chromagram | Melody as pitches | 12-dim per-frame vector; input to melody conditioning. |
| Stems | Instrument tracks | Separated bass / drums / vocals / melody as WAV. |
| Inpainting | Regen a section | Mask a time window; model regenerates just that. |
| CLAP | Text-audio CLIP | Contrastive audio-text embedding; eval text-audio alignment. |
| EnCodec | Music codec | Meta's neural codec used by MusicGen; 32 kHz, 4 codebooks. |

| 术语 | 人们常说的 | 实际含义 |
|------|-----------|---------|
| FAD | 音频 FID | 真实 vs 生成嵌入分布之间的 Fréchet 距离。 |
| 色度图 | 旋律即音高 | 12 维逐帧向量；旋律条件的输入。 |
| 分轨 | 乐器轨道 | 分离的贝斯/鼓/人声/旋律 WAV。 |
| 内画 | 重生成一段 | 遮蔽时间窗口；模型只重生成那部分。 |
| CLAP | 文本-音频 CLIP | 对比音频-文本嵌入；评估文本-音频对齐。 |
| EnCodec | 音乐编解码器 | Meta 的神经编解码器，MusicGen 使用；32 kHz，4 个码本。 |

> **【中文解读】** 延伸阅读提供了深入学习的高质量资源。这些论文和教程是该领域的经典参考文献，适合需要深入理解的读者。


## Further Reading | 延伸阅读

- [Copet et al. (2023). MusicGen](https://arxiv.org/abs/2306.05284) — the open autoregressive benchmark.
  Copet 等 (2023). MusicGen——开源自回归基准。
- [Evans et al. (2024). Stable Audio Open](https://arxiv.org/abs/2407.14358) — the sound-design default.
  Evans 等 (2024). Stable Audio Open——声音设计默认选择。
- [ACE-Step](https://github.com/ace-step/ACE-Step) — open 4B full-song generator, April 2026.
  ACE-Step——开源 40 亿参数全曲生成器，2026 年 4 月。
- [Suno v5 platform docs](https://suno.com) — the commercial quality leader.
  Suno v5 平台文档——商业质量领先者。
- [AudioLDM2](https://arxiv.org/abs/2308.05734) — latent diffusion for music + sound effects.
  AudioLDM2——音乐 + 音效的潜变量扩散。
- [WMG-Suno settlement coverage](https://www.musicbusinessworldwide.com/suno-warner-music-settlement/) — Nov 2025 precedent.
  WMG-Suno 和解报道——2025 年 11 月判例。

> **【中文解读】** 延伸阅读提供了深入学习的高质量资源，包括论文、教程和工具。建议按需选读，优先阅读标注为 "the critical read" 的核心论文。

