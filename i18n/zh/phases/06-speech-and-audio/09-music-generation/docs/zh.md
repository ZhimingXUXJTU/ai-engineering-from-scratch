# 音乐生成 音乐生成,稳定音频,苏诺,以及许可证地震.

> 2026年音乐代:Suno v5和Udio v4占据商业主导地位; MusicGen,Stable Audio Open和 ACE-Step引领开源.技术问题大多得到解决.法律问题 (Warner Music 500M美元和解,UMG和解) 在2025-2026年重新塑造了该领域.

> **【中文解读】**2026年的音乐产量:Suno v5 和 Udio v4 主导商业产品;MusicGen、Stable Audio Open 和 ACE-Step 领先开源――技术问题基本解决,但法律问题(Warner Music 5 亿美元和解案) 在2025-2026年重塑这个领域――

> **【拓展：AI 音乐的法律风暴】**音乐产品版权问题引发了音乐行业的地震.

**Type:** Build | **类型:** 构建
**Languages:** Python | **语言:** Python
**Prerequisites:** Phase 6 · 02 (Spectrograms), Phase 4 · 10 (Diffusion Models) | **前置知识:** 阶段 6 · 02（频谱图），阶段 4 · 10（扩散模型）
**Time:** ~75 minutes | **预计用时:** ~75 分钟

## 问题 问题引入

文字 → 30 秒到 4 分钟的音乐片段,歌词,歌声和结构.

> 文本 → 30秒到 4分钟的音乐片段,带歌词、人声和结构──三子问题:

> **【中文解读】**本节提出的问题是:如何在实际工程中正确理解和应用这一技术――理解问题背景有助于把握技术选择的关键决策点――在实际人工智能系统中,错误的技术选择往往比实现细节的错误成本更高――

1. **Instrumental generation.**文字如"热键的洛菲哈普鼓" →音频.
   **器乐生成。**像"热键的低音哈鼓"这样的文本 → 音频──音乐Gen、稳定音频、音频LDM──
2. **Song generation (with vocals + lyrics).**关于雨天的德克萨斯州夜晚的乡村歌曲.
   **歌曲生成（带人声+歌词）。**关于雨天的德克萨斯州夜晚的乡村歌曲
3. **Conditional / controllable.**扩展现有剪辑,再生桥梁,交换类型,干部分离或涂料.Udio的涂料+干部分离是2026年配合的功能.
   **条件/可控生成。**扩展现有片段"",重新生成桥段"",切换风格"",分轨或内画"",Udio的内画+分轨是2026年要追赶的功能──

## 概念的核心概念

> **【中文解读】**本节介绍核心概念和理论基础.掌握这些概念是后续动手实现的前提,同时也是面试和工程实践中高频考察的知识点.


![Music generation: token-LM vs diffusion, the 2026 model map](../assets/music-generation.svg)

### 标志 LM 与神经编码标志相比

> ### 基于神经编解码代币的代币LM

标签**MusicGen**根据"中文代码"的定义,它可以使用"中文代码" (MIT) 和许多衍生品:文字/旋律嵌入式的条件,可自行预测EnCodec代码 (32 kHz, 4 代码书),可用EnCodec解码. 300M - 3.3B参数.强基线;超过 30 秒的斗争.

> 标签:**MusicGen**(2023,MIT) 和许多衍生品:以文本/旋律嵌入为条件,自归预测EnCodec代币(32 kHz,4个码本),使用EnCodec解码──3亿到33亿参数──强基线;超过30秒效果下降──

**ACE-Step**开源,4B XL发布于2026年4月. 这将扩展到全歌曲歌词的生成.

> **ACE-Step**开源社区最接近苏诺的产品.

### 化或隐藏物间的化

> ### 基于或潜变量的扩散

**Stable Audio (2023)**其他**Stable Audio Open (2024)**音,音响设计,环境纹理,结构性完整歌曲不太好.

> **Stable Audio（2023）**和 **Stable Audio Open（2024）**压缩音频上的潜变量扩散――擅长循环、声音设计、氛围质感――不太擅长结构化完整歌曲――

**AudioLDM / AudioLDM2**通过T2I式的隐藏传播,将其通用到音乐,音效,语音.

> **AudioLDM / AudioLDM2**通过T2I风格的潜变量扩散进行文本到音频生成,泛化到音乐、音效、语音──

### 混合动力 (制作) 苏诺,乌迪奥,丽亚

> ### 混合(生产)  苏诺、音声、歌曲

密闭重量.可能是AR编码器LM+基于扩散的声码器,具有专业的声音/鼓/旋律头.Suno v5 (2026) 是ELO 1293质量领导者.Udio v4增加了涂料+干部分离 (低音,鼓,声声单独下载).

> 闭源权重──可能是AR 编解码 LM + 基于扩散的声码器,配有专门的语音/鼓/旋律头──Suno v5(2026) 是ELO 1293质量领先者──Udio v4 增加内画 + 分轨(贝斯、鼓、人声分别下载) ⋅

### 评估

> ### 评估

- **FAD (Fréchet Audio Distance).**嵌入级距离在使用VGGish或PANN功能生成与真实的音频分发之间.较低更好.音乐Gen小: MusicCaps上的4.5 FAD;SOTA ~3.0.
  **FAD（Fréchet 音频距离）。**使用VGGish或PANNs特征的生成与真实音频分布的嵌入级距离──越低越好──音乐Gen小:音乐Caps 上 4.5 FAD;SOTA 约 3.0──
- **Musicality (subjective).**人类偏好.苏诺V5ELO1293导向.
  **音乐性（主观）。**人类偏好──苏诺 v5 ELO 1293 领先──
- **Text-audio alignment.**快速和输出之间的CLAP分数.
  **文本-音频对齐。**提示与输出之间的CLAP 分数――
- **Musicality artifacts.**音频转变,声语漂移,30秒后结构损失.
  **音乐性伪影。**跑拍过渡、人声短语漂移、超过30秒后结构丢失──

> **【拓展：语音 AI 的产品化】**语音技术在产品化中面临着独特的挑战:不同口音,背景噪音,远场拾音,多人说话等.

> **【拓展：多语言语音技术】**全球语言的语音特性差异巨大:声调语言的音高携带语义,低资源语言缺乏训练数据――Meta的MMS模型支持1000多种语言的语音识别,语在多语言场景表现出色,但仍然需要针对特定语言微调――



## 2026年模型地图

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

## 法律环境 (2025-2026)

> ## 法律环境(2025-2026)

- **Warner Music vs Suno settlement.**现在WMG已经监督了Suno的AI相似性,音乐权利和用户生成的曲目.
  **Warner Music 诉 Suno 和解。**现在,WMG对Suno上 AI的相似性,音乐版权和用户生成内容有监督权.
- **EU AI Act**其他**California SB 942**必须披露人工智能生成的音乐.
  **EU AI 法案**其他**加利福尼亚 SB 942**音乐必须被披露.
- **Riffusion / MusicGen**没有合规包装,也没有商业声.
  **Riffusion / MusicGen**没有合规负担,但也没有商业人士的声音.

安全到船的模式:

> 安全发布模式:

1. 仅生成仪器 (MusicGen,稳定音频开放,MIT/CC0输出).
   仅生成器乐(音乐Gen、稳定音频开、MIT/CC0 输出) 。
2. 使用商业API (Suno,Udio,ElevenLabs Music) 按一代许可.
   通过使用每次生成许可的商业API (Suno、Udio、ElevenLabs Music)
3. 列车在拥有或授权的目录上 (大多数企业都在此结束).
   在自有或授权目录上训练 (大多数企业最终走到这个阶段)
4. 标签生成器用水标+元数据.
   用水印+元数据标记生成内容──

> **【中文解读】**本节通过代码实现从零到核心算法――这种"从零开始"的方式可以帮助理解框架背后的原理,遇到问题时不会被黑盒困住――


## 建立它,实现它.
```figure
sp-codec-tokens
```

## 建立它

### 步骤1:使用 MusicGen生成

```python
from audiocraft.models import MusicGen
import torchaudio

model = MusicGen.get_pretrained("facebook/musicgen-small")
model.set_generation_params(duration=10)
wav = model.generate(["upbeat synthwave with driving drums, 128 BPM"])
torchaudio.save("out.wav", wav[0].cpu(), 32000)
```

三个尺寸:`small`快速的`medium`其他国家`large`3.3B. 对于"想法能实现"而言,小就足够了.

> 两个小说:`small`快速的增长率`medium`美国`large`美国`small`足以验证"想法是否可行"――

### 步骤2:调节旋律

```python
melody, sr = torchaudio.load("humming.wav")
wav = model.generate_with_chroma(
    ["jazz piano cover"],
    melody.squeeze(),
    sr,
)
```

音乐Gen-melody在调音调换时会采用染色符号,保存调音.

> 音乐Gen-melody 接受色度图并交换音色时保留旋律──适用于"把这个旋律转换为弦乐四重奏"──

### 步骤3:FAD评估

```python
from frechet_audio_distance import FrechetAudioDistance
fad = FrechetAudioDistance()

fad.get_fad_score("generated_folder/", "reference_folder/")
```

对于类型水平回归测试有用,而不是替代人类听者.

> 计算 VGGish 嵌入距离――适用于流派级回归测试;不能替代人类听众――

### 步骤4:加入LLM音乐工作流程

结合了从第七到八课的想法:

> **【中文解读】**本节展示了如何使用成熟框架 (如PyTorch、HuggingFace等) 快速应用该技术.


```python
prompt = "Write a 30-second jazz loop. Describe the drums, bass, and piano voicing."
description = llm.complete(prompt)
music = musicgen.generate([description], duration=30)
```




> **【拓展：语音与情感计算】**语音不仅传递文字信息,还携带丰富的情感信号 (语调、语速、音高变化) 情感语音识别 (语音识别,语音情感识别,SER) 在客服质检,心理健康监测,智能教育等领域广泛应用.

## 用它实现框架

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



## 陷在2026年仍存在

> 2026年仍在犯案陷中

- **Copyright-laundering prompts.**现在,开放型号不了. 添加自己的过列表.
  **版权洗钱提示。**现在会过这些,开源模型不会――添加你自己的过列表――
- **Repetition / drift past 30 s.**交叉多代,或使用ACE-Step来实现结构一致性.
  **超过 30 秒的重复/漂移。**交叉淡进多个生成,或使用ACE-Step 保持结构一致性.
- **Tempo drift.**通过图书馆的提示和后过器使用BPM标签.`beat_track`现在,我们要去.
  **节奏漂移。**模型偏离BPM──在提示中使用BPM标签并使用图书馆的 `beat_track`后过.
- **Vocal intelligibility.**苏诺很好,开放式模型通常是不熟悉的.如果歌词很重要,请使用商业API或细节调节.
  **人声清晰度。**子表现出色;开源模型的歌词经常模糊──如果歌词重要,使用商业API或微调──
- **Mono output.**开放型号生成单声或假声. 通过适当的声波重建升级 (例如,卡特西亚的声波扩散).
  **单声道输出。**开源模型生成单声道或假立体声.

> **【中文解读】**本节关注如何将模型部署为可用的产品. 从原型到生产级系统需要考虑性能优化,错误处理,监控等多个维度.


## 运送它.

保存如`outputs/skill-music-designer.md`选择模式,许可战略,长度/结构计划,以及披露音乐代部署的元数据.

> 保存为`outputs/skill-music-designer.md`◎为音乐生成部署选择模型、许可策略、长度/结构计划和披露元数据──

## 练习题

1. **Easy.**跑步`code/main.py`它产生"生成"和弦进步 + 鼓模式作为ASCII符号音乐代动画.
   **简单。**运行`code/main.py`△它使用ASCII符号生成"生成式"和弦进行 + 鼓点一个音乐生成的卡通可用MIDI染色器播放
2. **Medium.**安装`audiocraft`通过 MusicGen-small生成10秒的视频,
   **中等。**装备`audiocraft`通过音乐Gen-small 在 4 流派提示上生成 10 秒片段,对照参考流派集测量 FAD──
3. **Hard.**使用ACE-Step (或 MusicGen-melody) 来生成相同旋律的三个变化,使用不同的调音提示.计算CLAP与提示的相似性来验证对齐.
   **困难。**使用ACE-Step (或音乐Gen-旋律),使用不同音色提示生成同一旋律的三个变体.

> **【中文解读】**在团队协作中,统一术语定义可以避免大量沟通误解.


## 关键词 快速查找表

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

> **【中文解读】**延伸阅读提供了深入学习的高质量资源. 这些论文和教程是该领域的经典参考文献,适合需要深入了解的读者.


## 继续阅读 继续阅读

- [Copet et al. (2023). MusicGen](https://arxiv.org/abs/2306.05284)开放的反向性基准指数.
  音乐Gen开源自归基准――
- [Evans et al. (2024). Stable Audio Open](https://arxiv.org/abs/2407.14358)默认的音响设计.
  埃文斯等 (2024). 稳定音频开放声音设计默认选择.
- [ACE-Step](https://github.com/ace-step/ACE-Step)开放4B全歌发电机,2026年4月.
                                                                                                                                                                                                                                                                
- [Suno v5 platform docs](https://suno.com)商业质量领导者.
  诺V5 平台文档商业质量领先者
- [AudioLDM2](https://arxiv.org/abs/2308.05734) 音乐+音效的隐藏传播.
  音效的潜变量扩散.
- [WMG-Suno settlement coverage](https://www.musicbusinessworldwide.com/suno-warner-music-settlement/)2025年11月前例.
  周三,周二,周二,周二,周二,周二,周二,周二,周二,周二,周二,周二,周二,周二,周二,周二,周二,周二,周二,周二,周二,周二,周二,周二,周二,周二,周二,周二,周二,周二,周二,周二,周二,周二,周二,周二,周二,周二,周二,周二,周二,周二,周二,周二,周二,周二,周二,周二,周二,周二,周二,周二,周二,周二,周二,周二,周二,周二,周二,周二,周二,周二,周二,周二,周二,周二,周二,周二,周二,周二,周二,周二,周二,周二,周二,周二,周二,

> **【中文解读】**延伸阅读提供了深入学习的高质量资源,包括论文,教程和工具.

