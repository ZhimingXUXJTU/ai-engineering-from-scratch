# 语音合成 从塔科特朗到F5和Kokoro

> 亚斯尔将语音转换为文字;TTS将文字转换为语音.2026堆由三个部分组成:文字 →代币,代币 → mel,mel →波形.每个部分都有一个默认模型,可以适合笔记本电脑.

> **【中文解读】**语音变文字,TTS 把文字变语音──2026年的TTS 技术分三步:文本→token→Mel 频谱→波形──每一步都有可在笔记本上运行的默认模型──

> **【拓展：TTS 的应用】**作为一个"无障碍辅助"的核心技术,TTS的核心技术是:

**Type:** Build | **类型:** 构建
**Languages:** Python | **语言:** Python
**Prerequisites:** Phase 6 · 02 (Spectrograms & Mel), Phase 5 · 09 (Seq2Seq), Phase 7 · 05 (Full Transformer) | **前置知识:** 阶段 6 · 02（频谱图与 Mel），阶段 5 · 09（Seq2Seq），阶段 7 · 05（完整 Transformer）
**Time:** ~75 minutes | **预计用时:** ~75 分钟

## 问题 问题引入

你有一个字符串:"请提醒我在晚上6点点点灌植物".你需要一个自然听起来的3秒钟音频剪辑,有正确的音声 (暂停,压力),用正确的音符发音"植物",并在CPU上运行在300ms以下,即即可使用直播语音助理.你还需要交换声音,处理代码交换输入 ("提醒我在晚上6点,大约布?"),而不要在名字上尬.

> 你有一个字符串:"请提醒我在下午6点点点灌水植物. " 你需要一段3秒的音频,听起来自然,律正确(停顿、重音),"植物"的元音发音正确,并且在CPU上不到300 ms 就能运行以实时语音助手.

> **【中文解读】**本节提出的问题是:如何在实际工程中正确理解和应用这一技术――理解问题背景有助于把握技术选择的关键决策点――在实际人工智能系统中,错误的技术选择往往比实现细节的错误成本更高――

现代的TTS管道看起来像这样:

> 现代 TTS 流水线如下:

1. **Text frontend.**规范文本 (日期,数字,电子邮件),转换为音符或字幕标记,预测 prosody 功能.
   **文本前端。**归一化文本 ((日期、数字、邮箱),转换为音素或子词代币,预测律特征。
2. **Acoustic model.**文字 → 梅尔谱图.塔科特龙2 (2017),快速讲话2 (2020),VITS (2021),F5-TTS (2024),科科罗 (2024).
   **声学模型。**文本 → 梅尔 频谱图──塔科特龙 2(2017)、快速讲话 2(2020)、VITS(2021)、F5-TTS(2024)、科科罗(2024)。
3. **Vocoder.**波形:波网 (2016),波RNN,高清高清高清高清高清高清高清高清高清高清高清高清高清高清高清高清高清高清高清高清高清高清高清高清高清高清高清高清高清高清高清高清高清高清高清高清高清高清高清高清高清高清高清高清高清高清高清高清高清高清高清高清高清高清高清高清高清高清高清高清高清高清高清高清高清高清高清高清高清高清高清高清高清高清高清高清高清高清高清高清高清高清高清高清高清高清高清高清高清高清高清高清高清高清高清高清高清高清高清高清高清高清高清高清高清高清高清高清高清高清高清高清高清高清高清高清高清高清中高清高清高清中高清高清中高清高清中高清中高清中高清中高清中高清中高清中高清中高清中高清中高清中高清中高清中
   **声码器。**波形. 波网. 波网. 波网. 波网. 波网. 波网. 波网. 波网. 波网. 波网. 波网. 波网. 波网. 波网. 波网. 波网. 波网. 波网. 波网. 波网. 波网. 波网. 波网. 波网. 波网. 波网. 波网. 波网. 波网. 波网. 波网. 波网. 波网. 波网. 波网. 波网. 波网. 波网. 波网. 波网. 波网. 波网. 波网. 波网. 波网. 波网. 波网. 波网. 波网. 波网. 波网. 波网. 波网. 波网.

2026年,音声+声码器的分离模糊,并与端到端的扩散和流量匹配模型相匹配.

> 2026年,随着流匹配模型的出现,声学模型+声码器的界限变得模糊.

## 概念的核心概念

> **【中文解读】**本节介绍核心概念和理论基础.掌握这些概念是后续动手实现的前提,同时也是面试和工程实践中高频考察的知识点.


![Tacotron, FastSpeech, VITS, F5/Kokoro side-by-side](../assets/tts.svg)

**Tacotron 2 (2017).**序列2次:嵌入式 → BiLSTM编码器 →位置敏感注意 → 自动降低式LSTM解码器发射 mel 框架.慢 (AR),在长文中摇摆.仍然被引用为基线.

> **Tacotron 2（2017）。**字符嵌入 → BiLSTM 编码器 → 位置敏感注意力 → 自归 LSTM 解码器输出 mel ──慢(AR),长文本不稳定──仍被引用为基线──

**FastSpeech 2 (2020).**无自行降低. 时间预测器输出每个音符的 mel 框架. 1 通过,比塔科特龙快10倍. 失去一些自然性 (单调的排列),但在任何地方都出发.

> **FastSpeech 2（2020）。**不自归──时长预测器输出每音素获得多少米──单次前向,比塔科特龙快10倍──损失一些自然度(单调对齐) 但到处都在使用──

**VITS (2021).**联合训练编码器+基于流程的持续时间+高清高清高清高清单机型.主导的开源TTS 20222024.变体:YourTTS (多音箱零射击),XTTS v2 (2024,Coqui).

> **VITS（2021）。**联合训练编码器 + 基流的时长预测 + HiFi-GAN 声码器端到端,使用变分推断。高质量,单模型。2022-2024年主导开源 TTS。变体:YourTTS(多说话人零样本)、XTTS v2(2024,Coqui)。

**F5-TTS (2024).**传输变压器与流量匹配.自然的声,零射击语音克隆, 5 秒的参考音频. 2026 年开源TTS 排名榜首. 335 亿参数.

> **F5-TTS（2024）。**基于流匹配的扩散变压器──自然律,5秒参考音频零样本声音克隆──2026年开源TTS排行榜榜首──3.35亿参数──

**Kokoro (2024).**简单的英语语,只能使用闭口语库,Apache-2.0.

> **Kokoro（2024）。**小型(8200万参数),可在CPU上运行,同类最佳实时英文TTS──封闭词表仅限英文,Apache-2.0 许可──

**OpenAI TTS-1-HD, ElevenLabs v2.5, Google Chirp-3.**商业技术状态.ElevenLabs v2.5情感标签 ("[低声]", "[笑]") 和角色声音在2026年占据了音频书制作的主导地位.

> **OpenAI TTS-1-HD、ElevenLabs v2.5、Google Chirp-3。**商业SOTA──ElevenLabs v2.5 的情感标签("[低声]"、"[笑]") 和角色声音主导 2026 年有声书制作──

### 声码器的进化

> ### 声码器演进

| Era | Vocoder | Latency | Quality |
|-----|---------|---------|---------|
| 2016 | WaveNet | offline only | SOTA at release |
| 2018 | WaveRNN | ~realtime | good |
| 2020 | HiFi-GAN | 100× realtime | near-human |
| 2022 | BigVGAN | 50× realtime | generalizes across speakers/langs |
| 2024 | SNAC, DAC (neural codecs) | integrated with AR models | discrete tokens, bit-efficient |

| 时代 | 声码器 | 延迟 | 质量 |
|------|--------|------|------|
| 2016 | WaveNet | 仅离线 | 发布时 SOTA |
| 2018 | WaveRNN | 约实时 | 良好 |
| 2020 | HiFi-GAN | 100× 实时 | 接近人类 |
| 2022 | BigVGAN | 50× 实时 | 跨说话人/语言泛化 |
| 2024 | SNAC, DAC（神经编解码器） | 与 AR 模型集成 | 离散 token，比特高效 |

到2026年,大多数"TTS"模型将从文本到波形的端到端;MEL谱系是一个内部表示.

> 到2026年,大多数"TTS"模型是从文本到波形的端到端模型;Mel频谱图是内部表示.

### 评估

> ### 评估

- **MOS (Mean Opinion Score).**现在,我在上,我在上,我在上.
  **MOS（平均意见分）。**速度痛苦地慢.
- **CMOS (Comparative MOS).**对于每一个注释,更紧密的信任间隔.
  **CMOS（比较 MOS）。**对于每一个标志的置信区间更窄.
- **UTMOS, DNSMOS.**没有参考的神经MOS预测器,用于排名表.
  **UTMOS、DNSMOS。**无参考神经MOS预测器──用于排行榜──
- **CER (Character Error Rate) via ASR.**通过Whisper运行TTS输出,计算CER与输入文本.
  **CER（字符错误率）通过 ASR。**通过语输出,对输入文本计算 CER──可理解度的代理标志──
- **SECS (Speaker Embedding Cosine Similarity).**语音克隆质量.
  **SECS（说话人嵌入余弦相似度）。**声音克隆质量.

2026年 LibriTTS试验清洁号码:

> 2026年 LibriTTS测试清洁 上的数字:

| Model | UTMOS | CER (via Whisper) | Size |
|-------|-------|-------------------|------|
| Ground truth | 4.08 | 1.2% | — |
| F5-TTS | 3.95 | 2.1% | 335M |
| XTTS v2 | 3.81 | 3.5% | 470M |
| VITS | 3.62 | 3.1% | 25M |
| Kokoro v0.19 | 3.87 | 1.8% | 82M |
| Parler-TTS Large | 3.76 | 2.8% | 2.3B |

| 模型 | UTMOS | CER（通过 Whisper） | 大小 |
|------|-------|---------------------|------|
| 真实音频 | 4.08 | 1.2% | — |
| F5-TTS | 3.95 | 2.1% | 3.35 亿 |
| XTTS v2 | 3.81 | 3.5% | 4.7 亿 |
| VITS | 3.62 | 3.1% | 2500 万 |
| Kokoro v0.19 | 3.87 | 1.8% | 8200 万 |
| Parler-TTS Large | 3.76 | 2.8% | 23 亿 |

> **【中文解读】**本节通过代码实现从零到核心算法――这种"从零开始"的方式可以帮助理解框架背后的原理,遇到问题时不会被黑盒困住――

> **【拓展：语音 AI 的产品化】**语音技术在产品化中面临着独特的挑战:不同口音,背景噪音,远场拾音,多人说话等.

> **【拓展：多语言语音技术】**全球语言的语音特性差异巨大:声调语言的音高携带语义,低资源语言缺乏训练数据――Meta的MMS模型支持1000多种语言的语音识别,语在多语言场景表现出色,但仍然需要针对特定语言微调――




## 建立它,实现它.
```figure
sp-tts-stack
```

## 建立它

### 步骤1:调音输入

```python
from phonemizer import phonemize
ph = phonemize("Hello world", language="en-us", backend="espeak")
# 'həloʊ wɜːld'
```

避免给任何低于VITS水平的质量的原始文本.

> 音素是通用桥梁──避免将原始文本输入到以下级别的任何模型──

### 步骤2:运行Kokoro (2026 CPU默认)

```python
from kokoro import KPipeline
tts = KPipeline(lang_code="a")  # "a" = American English
audio, sr = tts("Please remind me to water the plants at 6 pm.", voice="af_bella")
# audio: float32 tensor, sr=24000
```

运行离线,单个文件,82M参数.

> 单文件,8200万参数

### 步骤3:使用语音克隆运行F5-TTS

```python
from f5_tts.api import F5TTS
tts = F5TTS()
wav = tts.infer(
    ref_file="my_voice_5s.wav",
    ref_text="The quick brown fox jumps over the lazy dog.",
    gen_text="Please remind me to water the plants.",
)
```

通过5秒的参考片段+其转录;F5克隆了 prosody 和 timbre.

> 传入 5秒参考音频 + 其转录文本;F5 克隆律和音色.

### 步骤4:从零开始的 HiFi-GAN 声码器

太大了,不能适合教程脚本,但形状是:

```python
class HiFiGAN(nn.Module):
    def __init__(self, mel_channels=80, upsample_rates=[8, 8, 2, 2]):
        super().__init__()
        # 4 upsample blocks, total 256x to go from mel-rate to audio-rate
        ...
    def forward(self, mel):
        return self.blocks(mel)  # -> waveform
```

培训:对抗性 (短窗上的歧视) + 黑色谱重建损失 + 功能匹配损失.`hifi-gan`投资者或NVIDIA-NeMo.

> 训练:对抗式(短窗口判别器) + Mel 频谱图重建损失 + 特征匹配损失──已商品化使用 `hifi-gan`仓库或nvidia-NeMo的预训检查点

### 步骤5:全管道 (伪代码)

```python
text = "Please remind me at 6 pm."
phones = phonemize(text)
mel = acoustic_model(phones, speaker=alice)      # [T, 80]
wav = vocoder(mel)                                # [T * 256]
soundfile.write("out.wav", wav, 24000)
```

> **【中文解读】**本节展示了如何使用成熟框架 (如PyTorch、HuggingFace等) 快速应用该技术.





> **【拓展：语音与情感计算】**语音不仅传递文字信息,还携带丰富的情感信号 (语调、语速、音高变化) 情感语音识别 (语音识别,语音情感识别,SER) 在客服质检,心理健康监测,智能教育等领域广泛应用.

## 用它实现框架

现在,我们要做什么?

> 2026 年技术:

| Situation | Pick |
|-----------|------|
| Real-time English voice assistant | Kokoro (CPU) or XTTS v2 (GPU) |
| Voice cloning from 5 s reference | F5-TTS |
| Commercial character voices | ElevenLabs v2.5 |
| Audiobook narration | ElevenLabs v2.5 or XTTS v2 + fine-tune |
| Low-resource language | Train VITS on 5–20 h target-lang data |
| Expressive / emotion tags | ElevenLabs v2.5 or StyleTTS 2 fine-tune |

| 场景 | 选择 |
|------|------|
| 实时英文语音助手 | Kokoro（CPU）或 XTTS v2（GPU） |
| 5 秒参考音频声音克隆 | F5-TTS |
| 商业角色声音 | ElevenLabs v2.5 |
| 有声书朗读 | ElevenLabs v2.5 或 XTTS v2 + 微调 |
| 低资源语言 | 在 5-20 小时目标语言数据上训练 VITS |
| 表达性 / 情感标签 | ElevenLabs v2.5 或 StyleTTS 2 微调 |

开源领导者到2026年: **F5-TTS for quality, Kokoro for efficiency**除非你是历史学家,就不要寻找塔科特朗.

> 2026年开源领导者:**F5-TTS 追求质量，Kokoro 追求效率**否则别使用塔科特伦.



## 陷

> 常见陷

- **No text normalizer.**"史密斯博士"是"医生"或"驱动"? "2026"是"二十六"或"两零两六"?
  **没有文本归一化器。**"医生史密斯" 读成"医生"还是"驱动"?"2026"读成"二十六"还是"两零两六"?在音素化之前归归一化.
- **OOV proper nouns.**运送一个反弹图形到音形模型,用于未知的代币.
  **OOV 专有名词。**为了未知标志提供备用字素到音素模型──
- **Clipping.**声器输出很少剪辑,但在推断时的MEL尺度不匹配可以超越 ±1.0.`np.clip(wav, -1, 1)`现在,我们要去.
  **削波。**音码器输出很少削波,但推理时 Mel 缩放不匹配可能超过 ±1.0──始终使用`np.clip(wav, -1, 1)`,我知道.
- **Sample-rate mismatch.**科科罗输出24kHz;下游管道预计16kHz →重新样本或获得号.
  **采样率不匹配。**东方 输出24kHz;你的下游流水线期望16kHz → 重采样否则产生混──

> **【中文解读】**本节关注如何将模型部署为可用的产品. 从原型到生产级系统需要考虑性能优化,错误处理,监控等多个维度.


## 运送它.

保存如`outputs/skill-tts-designer.md`设计一个针对特定语音,延迟和语言目标的TTS管道.

> 保存为`outputs/skill-tts-designer.md`◎为给定的声音、延迟和语言目标设计 TTS 流水线──

## 练习题

1. **Easy.**跑步`code/main.py`根据玩具词汇,构建一个音符词典,估计每音符的持续时间,
   **简单。**运行`code/main.py`从玩具词表构建音素字典,估计每个音素的时长,并打印假的"mel"计划
2. **Medium.**安装Kokoro,在语音上合成同一个句子`af_bella`其他`am_adam`进行对比.
   **中等。**装备科科罗,用`af_bella`和 `am_adam`声音合成同句话──比较音频时长和主观质量──
3. **Hard.**记录一个5秒的参考片,使用F5-TTS克隆它,报告SECS在参考和克隆输出之间.
   **困难。**录制一段5秒的自已的参考音频――使用F5-TTS 克隆――报告参考与克隆输出之间的SECS――

> **【中文解读】**在团队协作中,统一术语定义可以避免大量沟通误解.


## 关键词 快速查找表

| Term | What people say | What it actually means |
|------|-----------------|-----------------------|
| Phoneme | Sound unit | Abstract sound class; 39 in English (ARPABet). |
| Duration predictor | How long each phoneme lasts | Non-AR model output; integer frames per phoneme. |
| Vocoder | Mel → waveform | Neural net mapping mel-spec to raw samples. |
| HiFi-GAN | Standard vocoder | GAN-based; dominant 2020–2024. |
| MOS | Subjective quality | 1–5 mean opinion score from human raters. |
| SECS | Voice-clone metric | Cosine similarity between target and output speaker embedding. |
| F5-TTS | 2024 open-source SOTA | Flow-matching diffusion; zero-shot cloning. |
| Kokoro | CPU English leader | 82M-param model, Apache 2.0. |

| 术语 | 人们常说的 | 实际含义 |
|------|-----------|---------|
| 音素 | 声音单位 | 抽象声音类别；英文有 39 个（ARPABet）。 |
| 时长预测器 | 每个音素持续多久 | 非自回归模型输出；每个音素的整数帧数。 |
| 声码器 | Mel → 波形 | 将 mel 频谱映射为原始采样的神经网络。 |
| HiFi-GAN | 标准声码器 | 基于 GAN；2020-2024 年主导。 |
| MOS | 主观质量 | 人工评分员的 1-5 平均意见分。 |
| SECS | 声音克隆指标 | 目标与输出说话人嵌入之间的余弦相似度。 |
| F5-TTS | 2024 开源 SOTA | 流匹配扩散；零样本克隆。 |
| Kokoro | CPU 英文领导者 | 8200 万参数模型，Apache 2.0。 |

> **【中文解读】**延伸阅读提供了深入学习的高质量资源. 这些论文和教程是该领域的经典参考文献,适合需要深入了解的读者.


## 继续阅读 继续阅读

- [Shen et al. (2017). Tacotron 2](https://arxiv.org/abs/1712.05884) 后续后续的基线.
  沈等 (2017). 塔科特龙 2seq2seq 基线。
- [Kim, Kong, Son (2021). VITS](https://arxiv.org/abs/2106.06103)基于端到端流动.
  根据流的模型,VITS端到端.
- [Chen et al. (2024). F5-TTS](https://arxiv.org/abs/2410.06885)目前的开源SOTA.
  陈等 (2024).F5-TTS当前开源SOTA──
- [Kong, Kim, Bae (2020). HiFi-GAN](https://arxiv.org/abs/2010.05646) Vocoder,仍然在2026年发射.
  香港,金,贝 (2020). 音器2026年仍在使用中.
- [Kokoro-82M on HuggingFace](https://huggingface.co/hexgrad/Kokoro-82M) 2024 年的英语TTS,适用于 CPU.
  科科罗-82M 在抱擁面上2024年CPU友好的英文TTS──

> **【中文解读】**延伸阅读提供了深入学习的高质量资源,包括论文,教程和工具.

