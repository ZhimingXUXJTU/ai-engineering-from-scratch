# 音频生成

> 音频是16-48kHz的1D信号.五秒的剪辑是80-240k样本.没有变压器直接处理该序列.2026年每个生产音频模型的解决方案是一样的:一个神经编码器 (Encodec,SoundStream,DAC) 将音频压缩到50-75Hz的分离代币,而一个变压器或扩散模型生成代币.

> **【中文解读】**音频是16-48kHz的1D信号,5秒就是8-24万采样点――没有变压器能直接处理这么长的序列――2026年所有音频生成模型的解决方案相同:神经编码器(EnCodec等) 压缩为50-75Hz的离散代币,然后使用变压器生成――

> **【拓展：MusicGen 与 AudioCraft】**基因的音乐Gen 和 音频制作领域的关键创新.

**Type:** Build / 构建型
**Languages:** Python
**Prerequisites:** Phase 6 · 02 (Audio Features / 音频特征), Phase 6 · 04 (ASR), Phase 8 · 06 (DDPM)
**Time:** ~45 minutes

## 问题 问题引入

音频生成的三个任务:

> 三种音频生成任务:

1. **Text-to-speech.**给出文本,产生语音.清洁语音是窄带的,具有强大的音响结构.
   **语音合成。**给定文本生成语音──已有良好的解决方案──
2. **Music generation.**由于提示 (文字,旋律,和弦进步,类型),制作音乐.更广泛的分发.
   **音乐生成。**给定提示 (文本,旋律,弦,流派) 产生音乐,分布更广.
3. **Audio effects / sound design.**根据提示,生成环境声音或Foley.
   **音效/声音设计。**给定提示生成环境音或拟音.

它们都运行在同一基层上:神经音频编码器+代币-AR或扩散发电机.

> 三者都运行在相同的基础设施上:神经音频编码器 + 代币自归或扩散生成器──

> **【中文解读】**音频生成的三大任务语音合成(TTS)、音乐生成、音效生成都基于相同的基础架构:神经音频编解码器(如EnCodec) 将音频压缩为离散代币,然后变压器或扩散模型在代币序列上生成──这与语言模型的"代币化器+变压器"模式完全一致──

> **【拓展：ElevenLabs 与语音克隆技术】**11Labs是2026年最流行的人工智能语音平台.它只需要几秒钟的参考频道才能克隆说话者的声音,然后使用克隆的声音合成任意文本.

## 概念的核心概念

![Audio generation: codec tokens + transformer or diffusion](../assets/audio-generation.svg)

### 神经音频编程器

编码器 (Meta, 2022),声音流 (Google, 2021),描述音频编码器 (DAC, 2023).一个卷积编码器将波形压缩到每步向量;残余向量量化 (RVQ) 将每个向量转换为K代码书指数.解码器逆转它.使用8个RVQ代码书以75Hz =600代码本/秒的24kHz音频以2 kbps.

```
waveform (16000 samples/sec)
    └─ encoder conv ─┐
                     ├─ RVQ layer 1 → indices at 75 Hz
                     ├─ RVQ layer 2 → indices at 75 Hz
                     ├─ ...
                     └─ RVQ layer 8
```

### 两种产生型范式在顶部

**Token-autoregressive.**调整RVQ代币成一个序列,运行一个只使用解码器的变压器.音乐Gen使用"延迟平行"来与每流的偏移并发K代码书流.VALL-E从文本提示+3秒语音样本生成语音代币.

**Latent diffusion.**编码符号将其作为连续隐藏符号或用类型传播来模拟.稳定音频2.5使用连续音频隐藏符号的流量匹配.AudioLDM2使用文本到邮件到音频传播.

2024-2026年趋势:流量匹配是音乐中获胜的 (更快的推断,更清洁的样本),而代币-AR仍然占据了语音的主导地位,因为它是自然的因果性和流量良好.

## 制作风景

| System | Task | Backbone | Latency |
|--------|------|----------|---------|
| ElevenLabs V3 | TTS | Token-AR + neural vocoder | ~300ms first token |
| OpenAI GPT-4o audio | Full-duplex speech | End-to-end multimodal AR | ~200ms |
| NaturalSpeech 3 | TTS | Latent flow matching | Non-streaming |
| Stable Audio 2.5 | Music / SFX | DiT + flow matching on audio latents | ~10s for 1-minute clip |
| Suno v4 | Full songs | Undisclosed; token-AR suspected | ~30s per song |
| Udio v1.5 | Full songs | Undisclosed | ~30s per song |
| MusicGen 3.3B | Music | Token-AR on Encodec 32kHz | Real-time |
| AudioCraft 2 | Music + SFX | Flow matching | ~5s for 5s clip |
| Riffusion v2 | Music | Spectrogram diffusion | ~10s |

## 建立它,实现它.
```figure
score-matching
```

## 建立它

`code/main.py`模拟核心想法:将一个小的下一个代币变压器训练用合成的"音频代币"序列,由两个不同的"风格"生成 (A风格的低和高代币交替,B风格的单调坡).

### 步骤1:合成音频代币

```python
def make_tokens(style, length, vocab_size, rng):
    if style == 0:  # "speech-like": alternating
        return [i % vocab_size for i in range(length)]
    # "music-like": ramp
    return [(i * 3) % vocab_size for i in range(length)]
```

### 步骤2:训练一个小的代币预测器

标志是:编码符号 → 跨进体训练 → 逆向样本取.

### 步骤3:条件性样本

根据风格代币和起始代币,从预测分布中取下一个代币.继续为20-40代币.

## 陷常见的陷

- **Codec quality caps output quality.**如果代码不能忠实地表示声音, 没有多少发电机质量有帮助.
- **RVQ error accumulation.**每个RVQ层都模拟了前一个层的残留.在层1上的错误扩散.在较高层上采样温度为0.
- **Musical structure.**30秒的代币是75Hz的20k+代币.对于变压器来说很难.音乐Gen使用滑窗+快速延续;稳定音频使用更短的剪辑+交叉.
- **Artifacts at boundaries.**产生的剪辑之间的交叉需要仔细的重叠.
- **Clean-data appetite.**音乐发电机需要数万小时的许可音乐.苏诺/乌迪奥RIAA诉讼 (2024) 揭露了这一点.
- **Voice cloning ethics.**对于VALL-E/XTTS/ElevenLabs来说,一个3秒钟的样本加上一个文本提示足够的,可以克隆声音.每个生产模型都需要发现滥用+选择退出列表.

## 用它实现框架

| Task / 任务 | 2026 stack / 2026 技术栈 |
|------|------------|
| Commercial TTS / 商业语音合成 | ElevenLabs, OpenAI TTS, or Azure Neural |
| Voice cloning (consent-verified) / 语音克隆 | XTTS v2 (open) or ElevenLabs Pro |
| Background music, fast / 快速背景音乐 | Stable Audio 2.5 API, Suno, or Udio |
| Music with lyrics / 带歌词音乐 | Suno v4 or Udio v1.5 |
| Sound effects / Foley / 音效/拟音 | AudioCraft 2, ElevenLabs SFX, or Stable Audio Open |
| Real-time voice agent / 实时语音代理 | GPT-4o realtime or Gemini Live |
| Open-weights music research / 开源音乐研究 | MusicGen 3.3B, Stable Audio Open 1.0, AudioLDM 2 |
| Dubbing / translation / 配音/翻译 | HeyGen, ElevenLabs Dubbing |

## 运送它.

保存`outputs/skill-audio-brief.md`技能采用音频简介 (任务,持续时间,风格,声音,许可证) 和输出:模型+托管,提示格式 (类型标签,风格描述符,结构标记),编码+生成器+声码链,种子协议和评估计划 (MOS/CLAP分数/TTS/用户A/B的 CER).

## 练习题

1. **Easy.**跑步`code/main.py`检查生成的序列与风格的模式一致.
2. **Medium.**添加延迟并行解码:模拟2个代币流,必须保持1步的抵消. 训练一个联合预测器.
3. **Hard.**使用 HuggingFace 变压器在本地运行 MusicGen-small. 生成一个10秒的剪辑,使用三个不同的提示;A/B以实现风格的依赖.

## 关键词 快速查找表

| Term | What people say | What it actually means |
|------|-----------------|-----------------------|
| Codec | "Neural compression" | Encoder / decoder for audio; typical output is 50-75 Hz tokens. |
| RVQ | "Residual VQ" | Cascade of K quantizers; each models the residual of the previous. |
| Token | "One codec symbol" | Discrete index into a codebook; 1024 or 2048 typical. |
| Delayed parallel | "Offset codebooks" | Emit K token streams with staggered offsets to reduce sequence length. |
| Flow matching | "The 2024 win for audio" | Straighter-path alternative to diffusion; faster sampling. |
| Voice prompt | "3-second sample" | Speaker embedding or token prefix that steers the cloned voice. |
| Mel spectrogram | "The visual" | Log-magnitude perceptual spectrogram; used by many TTS systems. |
| Vocoder | "Mel to wave" | Neural component that converts mel spectrograms back to audio. |

## 音频是流式问题

音频是用户预计将到达的输出模式,而不是一次性.在生产术语中,这意味着TPOT (Time Per Output Token) 重要,因为用户的听力速度是目标吞吐量,而不是他们的读取速度.对于16kHz的音频以75代币/秒 (Encodec) 代币,服务器必须每用户产生 ≥75代币/秒以保持播放流.

建筑的两个后果:

- **Flow-matching audio models cannot stream trivially.**稳定音频2.5和音频Craft2在一个传输中呈现固定剪辑长度. 为了流媒体,您将剪辑和重叠边界分片, 想象滑动窗口扩散, 增加100-300ms的延迟上线与编程 AR模型.

如果产品是"直播语音聊天"或"实时音乐延续",选择编程器AR路径.如果是"提交时发送30秒的剪辑",流量匹配在质量和总延迟上获胜.

## 继续阅读 继续阅读

- [Défossez et al. (2022). Encodec: High Fidelity Neural Audio Compression](https://arxiv.org/abs/2210.13438)编码标准.
- [Zeghidour et al. (2021). SoundStream](https://arxiv.org/abs/2107.03312)是第一个广泛使用的神经音频编程器.
- [Kumar et al. (2023). High-Fidelity Audio Compression with Improved RVQGAN (DAC)](https://arxiv.org/abs/2306.06546)  
- [Wang et al. (2023). Neural Codec Language Models are Zero-Shot Text to Speech Synthesizers (VALL-E)](https://arxiv.org/abs/2301.02111)  
- [Copet et al. (2023). Simple and Controllable Music Generation (MusicGen)](https://arxiv.org/abs/2306.05284)音乐Gen.
- [Liu et al. (2023). AudioLDM 2: Learning Holistic Audio Generation with Self-supervised Pretraining](https://arxiv.org/abs/2308.05734) 音频LDM 2.
- [Stability AI (2024). Stable Audio 2.5](https://stability.ai/news/introducing-stable-audio-2-5) 2025 文字与音乐的流量匹配.
