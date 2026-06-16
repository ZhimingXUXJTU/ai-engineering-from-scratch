# Audio-Language Models: the Whisper to Audio Flamingo 3 Arc | 音频语言模型：从 Whisper 到 Audio Flamingo 3

> Whisper (Radford et al., December 2022) settled speech recognition — 680k hours of weakly-supervised multilingual speech, a simple encoder-decoder transformer, a benchmark that made every subsequent ASR release cite it. But recognition is not reasoning. Asking "what instruments are in this recording" or "what emotion is the speaker expressing" or "what happened at minute 3" requires audio understanding, not transcription. Qwen-Audio, SALMONN, LTU, and NVIDIA's Audio Flamingo 3 (AF3, July 2025) progressively built that stack: keep Whisper-class encoders, bolt on Q-formers, train on audio-text instruction data, add chain-of-thought reasoning. This lesson walks the arc.

> **【中文解读】** Whisper 解决了语音识别，但识别不是推理。"这段录音用了什么乐器"、"说话者表达了什么情绪"等问题需要音频理解能力，不是简单转录。从 SALMONN 到 Audio Flamingo 3（AF3），音频 LLM 的发展路径是：保留 Whisper 级编码器 + 加 Q-Former 桥接 + 用音频-文本指令数据训练 + 加链式思考推理。

**Type:** Build
**Languages:** Python (stdlib, log-Mel spectrogram + audio Q-former skeleton)
**Prerequisites:** Phase 6 (Speech and Audio), Phase 12 · 03 (Q-Former)
**Time:** ~180 minutes

> 🔗 **【前置】** 学本节前请先掌握：Phase 6·01-02（语音信号处理：FFT/Mel 频谱图/Whisper）；Phase 12·03（Q-Former 桥接，本节复用为音频 Q-Former）；Phase 7（Transformer 编码器-解码器）。音频 LLM = 视觉 LLM 的"听觉版"，只是输入从图像 patch 变成 Mel 频谱图 patch。
> 💡 **【类比】** 音频 LLM = "为 LLM 装耳朵"。Whisper = 助听器（只能转录不能思考）；SALMONN = 聋哑学校的翻译员（Whisper 转录→LLM 思考）；AF3 = 直接给 LLM 装耳蜗（端到端听+想+答）。端到端的好处：能捕捉转录丢失的信息（语调、情绪、停顿），这些是推理的关键。

## Learning Objectives

- Compute a log-Mel spectrogram from a waveform: windowing, FFT, filter banks, log transform.
  中文翻译：从波形计算 log-Mel 频谱图：窗口化、FFT、滤波器组、对数变换。
- Compare encoder options: Whisper encoder, BEATs, AF-Whisper hybrid. When each wins.
  中文翻译：比较编码器选项：Whisper 编码器、BEATs、AF-Whisper 混合。各自何时胜出。
- Build an audio Q-former: N learnable queries cross-attending to spectrogram patches.
  中文翻译：构建音频 Q-former：N 个可学习查询对频谱图 patch 做交叉注意力。
- Explain cascaded (Whisper-then-LLM) vs end-to-end audio-LLM training: why end-to-end scales better for reasoning.
  中文翻译：解释级联（Whisper 后接 LLM）vs 端到端音频 LLM 训练：为什么端到端在推理上扩展更好。

## The Problem | 问题引入

Speech recognition was solved by Whisper. OCR-of-audio is a commodity. But "commodity" stops at transcription. If the model cannot reason over what it heard — timing, speakers, emotion, music structure, environmental sounds — transcription alone cannot drive product features.

> 语音识别已被 Whisper 解决。音频 OCR 已成为基础能力。但"基础能力"止步于转录。如果模型无法对所听内容进行推理——时间、说话人、情绪、音乐结构、环境声——仅靠转录无法驱动产品功能。

Three obvious routes:

> 三条明显路径：

1. Cascade: Whisper transcribes, LLM reasons over the transcript. Works for pure-speech scenarios. Fails for music, environmental audio, multi-speaker overlap, emotion.
   中文翻译：级联：Whisper 转录，LLM 对转录文本推理。适用于纯语音场景。对音乐、环境音频、多人重叠、情绪不适用。

2. End-to-end audio-LLM: an audio encoder feeds audio tokens directly into an LLM, skipping transcription. Preserves acoustic information (emotion, speaker, environment). Needs new training data.
   中文翻译：端到端音频 LLM：音频编码器将音频 token 直接输入 LLM，跳过转录。保留声学信息（情绪、说话人、环境）。需要新训练数据。

3. Hybrid: audio encoder + text decoder that can both transcribe and reason. Qwen-Audio and Audio Flamingo pick this route.
   中文翻译：混合：音频编码器 + 文本解码器，既能转录又能推理。Qwen-Audio 和 Audio Flamingo 选择此路径。

## The Concept | 核心概念

> **【中文解读】** 语音语言模型从 Whisper（OpenAI 的语音识别模型）到 AudioFlamingo 的演进。Whisper 在 68 万小时多语言音频上训练，是语音识别的基础模型。AudioFlamingo 等新一代模型不仅能转录，还能理解音频内容（音乐描述、环境声识别等）。

> **【拓展：语音 AI 的前沿** Whisper-large-v3 支持约 100 种语言的语音识别。2024-2025 年的趋势是语音大模型：GPT-4o 原生语音输入输出（延迟约 320ms），Gemini 的实时语音对话，ElevenLabs 的语音克隆。AudioFlamingo 在音频理解任务上达到 SOTA，能回答关于音乐和声音的复杂问题。


### Log-Mel spectrogram: the input feature

Every audio encoder starts with the same feature: a log-Mel spectrogram.

> 每个音频编码器都从相同的特征开始：log-Mel 频谱图。

1. Resample to 16 kHz.
   中文翻译：重采样至 16 kHz。
2. Short-time Fourier transform with 25ms windows, 10ms hop.
   中文翻译：短时傅里叶变换，25ms 窗口，10ms 步长。
3. Take magnitude of the FFT result.
   中文翻译：取 FFT 结果的幅度。
4. Apply Mel filter banks (typically 80 filters log-spaced 0-8000 Hz) to warp to perceptual frequency.
   中文翻译：应用 Mel 滤波器组（通常 80 个滤波器，对数间隔 0-8000 Hz）映射到感知频率。
5. Log compress (log(1 + x)) for dynamic range.
   中文翻译：对数压缩（log(1 + x)）以处理动态范围。

Result: a 2D array of shape (T, 80) where T is the number of time frames. For a 30-second clip at 100 Hz frame rate: (3000, 80).

> 结果：形状为 (T, 80) 的 2D 数组，其中 T 是时间帧数。30 秒片段在 100 Hz 帧率下：(3000, 80)。

### Whisper's encoder

Whisper's encoder is a 12-layer ViT-style transformer processing the log-Mel spectrogram as a sequence of time frames. Output: one hidden-state vector per time frame.

> Whisper 的编码器是一个 12 层 ViT 风格的 Transformer，将 log-Mel 频谱图作为时间帧序列处理。输出：每个时间帧一个隐藏状态向量。

For ASR, Whisper's decoder is a cross-attention transformer that generates text tokens conditioned on the encoder output. Standard encoder-decoder.

> 对于 ASR，Whisper 的解码器是一个交叉注意力 Transformer，根据编码器输出生成文本 token。标准编码器-解码器。

For ALMs (audio-LLMs), you want the encoder output as input to a different LLM. The pattern: Whisper encoder frozen, Q-former trainable, LLM frozen or tuned.

> 对于 ALM（音频 LLM），需要将编码器输出作为另一个 LLM 的输入。模式：Whisper 编码器冻结，Q-former 可训练，LLM 冻结或微调。

### BEATs and audio-specific encoders

Whisper was trained on speech-dominant data. It is weaker for music and environmental audio.

> Whisper 在语音主导的数据上训练。在音乐和环境音频上较弱。

BEATs (Chen et al., 2022) is a self-supervised transformer trained on AudioSet. Captures music and environmental sounds better than Whisper at the same parameter count.

> BEATs（Chen 等人，2022）是在 AudioSet 上训练的自监督 Transformer。在相同参数量下比 Whisper 更好地捕捉音乐和环境声。

AF-Whisper (Audio Flamingo 3's hybrid): concat Whisper + BEATs features as the audio input. Whisper carries linguistic signal, BEATs carries acoustic signal.

> AF-Whisper（Audio Flamingo 3 的混合方案）：拼接 Whisper + BEATs 特征作为音频输入。Whisper 携带语言信号，BEATs 携带声学信号。

### Audio Q-former

Same pattern as BLIP-2's visual Q-former. A fixed number of learnable queries (often 32 or 64) cross-attend over the audio encoder's output frames. The queries become audio tokens consumed by the LLM.

> 与 BLIP-2 的视觉 Q-former 相同的模式。固定数量的可学习查询（通常 32 或 64 个）对音频编码器的输出帧做交叉注意力。查询成为 LLM 消费的音频 token。

Training alignment stage: Q-former alone, contrastive + captioning losses on audio-text pairs (AudioCaps, Clotho). Instruction stage: end-to-end, unfreeze LLM, train on instruction data.

> 训练对齐阶段：仅 Q-former，音频-文本对上的对比+描述损失（AudioCaps、Clotho）。指令阶段：端到端，解冻 LLM，在指令数据上训练。

### The arc — SALMONN, Qwen-Audio, AF3

SALMONN (Tang et al., 2023): Whisper + BEATs + Q-former + LLaMA. The first open audio-LLM with serious reasoning ability. Benchmarks on MMAU show ~0.55 composite.

> SALMONN（Tang 等人，2023）：Whisper + BEATs + Q-former + LLaMA。第一个具有严肃推理能力的开放音频 LLM。MMAU 基准综合约 0.55。

Qwen-Audio (Chu et al., 2023): similar architecture, trained on a richer dataset, tuned for multi-turn dialogue. MMAU ~0.60.

> Qwen-Audio（Chu 等人，2023）：类似架构，在更丰富的数据集上训练，为多轮对话优化。MMAU 约 0.60。

LTU — Listen, Think, Understand (Gong et al., 2023): explicit reasoning data, focus on chain-of-thought over audio clips. Smaller but more focused.

> LTU——听、想、理解（Gong 等人，2023）：显式推理数据，专注于音频片段上的链式思考。更小但更专注。

Audio Flamingo 3 (Goel et al., July 2025): the current open SOTA. 8B LLM backbone (Qwen2 7B), Whisper-large encoder concat BEATs, 64-query Q-former, training on 1M+ audio-text instruction pairs. MMAU 0.72, matches proprietary frontier on some sub-tasks.

> Audio Flamingo 3（Goel 等人，2025 年 7 月）：当前开放 SOTA。8B LLM 主干（Qwen2 7B），Whisper-large 编码器拼接 BEATs，64 查询 Q-former，在 100 万+音频-文本指令对上训练。MMAU 0.72，在某些子任务上匹配闭源前沿。

AF3 also introduces on-demand chain-of-thought for audio: the model can optionally emit thinking tokens ("let me identify the instruments first: ...") before the final answer. Accuracy on complex reasoning tasks lifts 3-5 points when thinking is enabled.

> AF3 还引入了按需音频思维链：模型可以在最终回答前选择性地输出思考 token（"让我先识别乐器：..."）。启用思考时，复杂推理任务的准确率提升 3-5 个百分点。

### Cascaded vs end-to-end

Cascaded pipeline:

> 级联管道：

1. Whisper transcribes audio → text.
   中文翻译：Whisper 将音频转录为文本。
2. LLM reasons over text.
   中文翻译：LLM 对文本进行推理。

Works perfectly for "summarize this podcast." Fails for:
- "What's the mood of this song?" — mood is in the sound, not words.
- "Who is speaking, Alice or Bob?" — requires speaker identification.
- "At what second does the explosion happen?" — temporal grounding lost in text.
- "Is this real or generated audio?" — deepfake detection needs acoustic features.

> 对"总结这个播客"完美适用。但在以下场景失败：
> - "这首歌的情绪是什么？"——情绪在声音里，不在文字里。
> - "谁在说话，Alice 还是 Bob？"——需要说话人识别。
> - "爆炸在第几秒？"——文本中丢失了时间定位。
> - "这是真实音频还是生成的？"——深度伪造检测需要声学特征。

End-to-end preserves acoustic signal. Qwen-Audio and AF3 handle music, environment, and emotion natively.

> 端到端保留了声学信号。Qwen-Audio 和 AF3 原生处理音乐、环境和情绪。

> **【中文解读】** 级联管道（Whisper 转录→LLM 推理）适合纯语音场景如播客摘要，但无法处理音乐情绪、说话人识别、时间定位、深度伪造检测等需要声学特征的任务。端到端音频 LLM（AF3、Qwen-Audio）直接将音频 token 输入 LLM，保留了完整的声学信号。

> **【拓展：金融场景的音频理解】** 在金融领域，音频理解可用于：财报电话会的情绪分析（不仅是转录文字，还有语气和语调）、交易员的语音指令识别、客服质量监控的情绪检测、会议纪要的说话人分离。级联管道无法捕捉这些声学层面的信号。

### 2026 production recipe

For a new audio-understanding product:

> 对于新的音频理解产品：

- Cascaded if: transcription is the goal, no music, no emotion inference.
  中文翻译：级联方案：如果目标是转录，没有音乐，不需要情绪推断。
- AF3 / Qwen-Audio-family if: music, emotion, multi-speaker, or complex audio reasoning.
  中文翻译：AF3 / Qwen-Audio 系列：如果有音乐、情绪、多人说话或复杂音频推理。

Cascaded is cheaper and simpler. End-to-end is more capable.

> 级联更便宜更简单。端到端更强大。

### MMAU — the audio reasoning benchmark

MMAU (Massive Multimodal Audio Understanding) is the 2024-2025 audio reasoning benchmark:

> MMAU（大规模多模态音频理解）是 2024-2025 年的音频推理基准：

- 10,000 audio-text QA pairs across speech, music, environmental sounds.
  中文翻译：10,000 个跨语音、音乐、环境声的音频-文本 QA 对。
- Covers classification, temporal reasoning, causal reasoning, open-ended QA.
  中文翻译：覆盖分类、时间推理、因果推理、开放式 QA。
- Tests what cascaded pipelines systematically miss.
  中文翻译：测试级联管道系统性遗漏的内容。

Open SOTA (AF3) at 0.72; proprietary frontier ~0.78 (Gemini 2.5 Pro, Claude Opus 4.7). The gap is smaller than VideoMME's open-vs-closed delta, indicating audio-LLMs are maturing.

> 开放 SOTA（AF3）0.72；闭源前沿约 0.78（Gemini 2.5 Pro、Claude Opus 4.7）。差距小于 VideoMME 的开源-闭源差距，说明音频 LLM 正在成熟。

## Use It | 用框架实现

`code/main.py`:

- Implements log-Mel spectrogram computation in stdlib: windowing, naive DFT, Mel filter-bank.
  中文翻译：用标准库实现 log-Mel 频谱图计算：窗口化、朴素 DFT、Mel 滤波器组。
- Audio Q-former skeleton: given encoder output frames, compute Q, K, V, attention, and emit N tokens.
  中文翻译：音频 Q-former 骨架：给定编码器输出帧，计算 Q、K、V、注意力并输出 N 个 token。
- Cascaded-vs-end-to-end comparison on a toy task.
  中文翻译：在玩具任务上对比级联与端到端方案。

## Ship It | 产出物

This lesson produces `outputs/skill-audio-llm-pipeline-picker.md`. Given an audio task (transcription, music tagging, emotion inference, multi-speaker diarization, environment classification), it picks cascaded, end-to-end AF3, or a hybrid.

> 本课产出 `outputs/skill-audio-llm-pipeline-picker.md`。给定音频任务（转录、音乐标注、情绪推断、多人说话分离、环境分类），它选择级联、端到端 AF3 或混合方案。

## Exercises | 练习题

1. Compute the log-Mel spectrogram dimension for a 30-second clip at 16kHz, 25ms window, 10ms hop, 80 Mel bins. How does this change at 48kHz? 计算 30 秒音频在 16kHz、25ms 窗口、10ms 步长、80 Mel 频段下的 log-Mel 频谱图维度。48kHz 时如何变化？

2. Why does Whisper underperform on music? What audio features does BEATs capture that Whisper does not? 为什么 Whisper 在音乐上表现不佳？BEATs 捕获了哪些 Whisper 没有的音频特征？

3. Audio Q-former with 64 queries vs 32: at what task complexity does 64 pay off? 32 save compute for what? 64 查询 vs 32 查询的 Audio Q-former：在什么任务复杂度下 64 更值得？32 节省了什么计算？

4. Read AF3 Section 4 on on-demand thinking. Propose three audio tasks where chain-of-thought helps the most. 阅读 AF3 第 4 节关于按需思考的内容。提出三个链式思考最有帮助的音频任务。

5. Implement a minimal diarization pipeline using AF3's output. How do you signal speaker changes? 用 AF3 输出实现一个最小的说话人分离管道。如何标记说话人切换？

## Key Terms | 术语速查表

| Term | What people say | What it actually means | 中文释义 |
|------|-----------------|------------------------|---------|
| Log-Mel spectrogram | "Mel features" Mel 频谱 | 2D (time, frequency) array of log-magnitude values after Mel filter banks 经 Mel 滤波器组后的对数幅度二维数组 | |
| Audio Q-former | "Audio Perceiver" 音频感知器 | Cross-attention bottleneck from audio encoder output to fixed-length queries feeding the LLM 音频编码器输出到固定长度查询的交叉注意力瓶颈 | |
| Cascaded | "ASR-then-LLM" 级联管道 | Pipeline where Whisper transcribes and a text LLM reasons; loses acoustic information Whisper 转录后文本 LLM 推理的管道；丢失声学信息 | |
| End-to-end | "Audio-LLM" 端到端音频 LLM | Audio features enter the LLM directly via Q-former; preserves acoustic signal 音频特征通过 Q-former 直接进入 LLM；保留声学信号 | |
| BEATs | "Audio AudioSet encoder" 音频自监督编码器 | SSL transformer trained on AudioSet; strong on music + environmental sounds 在 AudioSet 上训练的自监督 Transformer；擅长音乐和环境声 | |
| MMAU | "Audio reasoning bench" 音频推理基准 | 10k QA pairs across speech, music, environment; 2024 eval standard 跨语音、音乐、环境的 1 万条 QA；2024 年评估标准 | |
| On-demand thinking | "Audio CoT" 按需音频思考 | Model can optionally emit reasoning tokens before final answer, lifts accuracy 3-5 pts 模型可在最终回答前输出推理 token，提升准确率 3-5 个百分点 | |

## Further Reading | 延伸阅读

- [Radford et al. — Whisper (arXiv:2212.04356)](https://arxiv.org/abs/2212.04356)
- [Chu et al. — Qwen-Audio (arXiv:2311.07919)](https://arxiv.org/abs/2311.07919)
- [Goel et al. — Audio Flamingo 3 (arXiv:2507.08128)](https://arxiv.org/abs/2507.08128)
- [Tang et al. — SALMONN (arXiv:2310.13289)](https://arxiv.org/abs/2310.13289)
- [Gong et al. — LTU (arXiv:2305.10790)](https://arxiv.org/abs/2305.10790)
