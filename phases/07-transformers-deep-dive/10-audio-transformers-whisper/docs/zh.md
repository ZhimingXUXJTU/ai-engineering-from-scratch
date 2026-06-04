# Audio Transformers — Whisper Architecture | 音频 Transformer — Whisper 架构

> 音频是频率随时间的图像。Whisper 是一个吃梅尔频谱图并说话的 ViT。

> **【中文解读】** Whisper 用 Transformer 做语音识别和翻译。理解音频如何变成 token 序列送入 Transformer。

**类型：** 学习
**语言：** Python
**前置条件：** 阶段 7 · 05（完整 Transformer），阶段 7 · 08（编码器-解码器），阶段 7 · 09（ViT）
**时长：** 约 45 分钟

## 问题引入

Whisper（OpenAI，Radford 等人 2022）之前，最先进的自动语音识别（ASR）是 wav2vec 2.0 和 HuBERT——自监督特征提取器加微调头。高质量、昂贵的数据管道、领域脆弱。多语言语音识别需要按语系分别建模。

Whisper 押了三个赌注：

1. **在所有数据上训练。** 680,000 小时的弱标注音频，从互联网上抓取，覆盖 97 种语言。不是干净的学术语料库。没有音素标签。
2. **多任务单一模型。** 一个解码器联合训练转录、翻译、语音活动检测、语言识别和时间戳预测，通过任务 token 实现。
3. **标准编码器-解码器 Transformer。** 编码器消费 log-mel 频谱图。解码器自回归产生文本 token。没有声码器，没有 CTC，没有 HMM。

结果：Whisper large-v3 在口音、噪声和没有干净标注数据的语言上都很鲁棒。它是 2026 年每个开源语音助手和大多数商业语音助手默认的语音前端。

> **【中文解读】** Whisper 的三大创新：(1) 用 68 万小时弱标注音频训练，覆盖 97 种语言；(2) 单模型多任务（转录、翻译、语种识别、时间戳）；(3) 标准编码器-解码器 Transformer 架构。音频被转换为 log-mel 频谱图（类似图像），编码器处理频谱特征，解码器生成文本。

## 核心概念

![Whisper 流水线：音频 → mel → 编码器 → 解码器 → 文本](../assets/whisper.svg)

### 步骤 1——重采样 + 加窗

音频采样率 16 kHz。裁剪/填充到 30 秒。计算 log-mel 频谱图：80 个梅尔频率 bin，10 ms 步幅 → 约 3,000 帧 × 80 个特征。这就是 Whisper 看到的"输入图像"。

### 步骤 2——卷积主干

两个 Conv1D 层，核大小 3，步幅 2，将 3,000 帧减少到 1,500。减半序列长度而不增加太多参数。

> **【拓展：Whisper 的多语言能力来源】** Whisper 在 97 种语言、68 万小时音频上训练，多语言能力来自两个因素：(1) 超大规模的弱标注数据覆盖了绝大多数语言；(2) 统一的 BPE 词表是 GPT-2 词表的超集，天然支持多语言。decoder prompt 中的语言 token（如 `<|zh|>`）控制输出语言，使同一模型可以执行转录或翻译任务。

### 步骤 3——编码器

一个 24 层（large 版本）的 Transformer 编码器，处理 1,500 个时间步。正弦位置编码，自注意力，GELU FFN。产生 1,500 × 1,280 的隐藏状态。

### 步骤 4——解码器

一个 24 层的 Transformer 解码器。它自回归地从 BPE 词汇表中产生 token，该词汇表是 GPT-2 的超集，带有一些音频特定的特殊 token。

### 步骤 5——任务 token

解码器提示以控制 token 开头，告诉模型要做什么：

```
<|startoftranscript|>  <|en|>  <|transcribe|>  <|0.00|>
```

或

```
<|startoftranscript|>  <|fr|>  <|translate|>   <|0.00|>
```

模型在这种约定上训练。你通过前缀控制任务。这是 2026 年版的指令微调，但应用于语音。

> **【中文解读】** Whisper 的任务控制机制非常优雅：通过在解码器前缀中添加特殊 token（如 `<|transcribe|>` 或 `<|translate|>`）来指定任务类型。这是"指令微调"在语音领域的应用——同一模型通过不同的前缀 token 执行不同任务。

> **【拓展：Whisper 在语音助手中的应用】** Whisper 是 2026 年语音 AI 的基础组件。从实时语音助手到视频字幕生成，再到多语言会议翻译，Whisper 提供了统一的语音前端。Whisper-turbo（4 层解码器）将延迟降低 8 倍，使实时对话成为可能。结合 LLM 的后端，形成了"Whisper + LLM + TTS"的现代语音助手架构。

### 步骤 6——输出

束搜索（宽度 5）带 log-prob 阈值。当 `<|notimestamps|>` token 不存在时，每 0.02 秒音频预测一次时间戳。

### Whisper 模型规模

| 模型 | 参数量 | 层数 | d_model | 头数 | 显存 (fp16) |
|------|--------|------|---------|------|-------------|
| Tiny | 39M | 4 | 384 | 6 | 约 1 GB |
| Base | 74M | 6 | 512 | 8 | 约 1 GB |
| Small | 244M | 12 | 768 | 12 | 约 2 GB |
| Medium | 769M | 24 | 1024 | 16 | 约 5 GB |
| Large | 1550M | 32 | 1280 | 20 | 约 10 GB |
| Large-v3 | 1550M | 32 | 1280 | 20 | 约 10 GB |
| Large-v3-turbo | 809M | 32 | 1280 | 20 | 约 6 GB（4 层解码器） |

Large-v3-turbo（2024）将解码器从 32 层削减到 4 层。解码速度 8 倍提升，WER 退化不到 1 个点。这种解码速度解锁就是为什么 Whisper-turbo 是 2026 年实时语音代理的默认选择。

> **【拓展：音频 Transformer 的统一趋势】** 语音识别（Whisper）、语音合成（VALL-E, Kokoro）、音乐生成（MusicGen）都在转向 Transformer 架构。核心思路相同：将音频转换为频谱图或离散 token 序列，然后用标准 Transformer 处理。这验证了 Transformer 作为通用序列建模器的地位。

### Whisper 做不到的事

- 没有说话人分离（谁在说话）。需要搭配 pyannote。
- 没有原生实时流式处理——30 秒窗口是固定的。现代封装（`faster-whisper`、`WhisperX`）通过 VAD + 重叠来添加流式。
- 没有外部分块就无法处理超过 30 秒的长格式上下文。实际效果良好，因为人类语音很少需要长程上下文进行转录。

### 2026 年格局

| 任务 | 模型 | 备注 |
|------|------|------|
| 英语 ASR | Whisper-turbo, Moonshine | Moonshine 在边缘设备上快 4 倍 |
| 多语言 ASR | Whisper-large-v3 | 97 种语言 |
| 流式 ASR | faster-whisper + VAD | 可达到 150 ms 延迟目标 |
| TTS | Piper, XTTS-v2, Kokoro | 编码器-解码器模式，但 Whisper 形状 |
| 音频 + 语言 | AudioLM, SeamlessM4T | 一个 Transformer 中的文本 token + 音频 token |

## 动手实现

参见 `code/main.py`。我们不训练 Whisper——我们构建 log-mel 频谱图管道 + 任务 token 提示格式化器。这些是你在生产中实际接触的部分。

### 步骤 1：合成音频

生成一个 16 kHz 采样的 1 秒 440 Hz 正弦波。16,000 个采样点。

### 步骤 2：log-mel 频谱图（简化版）

完整的梅尔频谱图需要 FFT。我们做一个简化的分帧 + 每帧能量版本，展示管道而不需要 `librosa`：

```python
def frame_signal(x, frame_size=400, hop=160):
    frames = []
    for start in range(0, len(x) - frame_size + 1, hop):
        frames.append(x[start:start + frame_size])
    return frames
```

帧 = 25 ms，步幅 = 10 ms。匹配 Whisper 的加窗。每帧能量代替梅尔频率 bin 用于教学。

### 步骤 3：填充到 30 秒

Whisper 总是处理 30 秒的块。将频谱图填充（或裁剪）到 3,000 帧。

### 步骤 4：构建提示 token

```python
def whisper_prompt(lang="en", task="transcribe", timestamps=True):
    tokens = ["<|startoftranscript|>", f"<|{lang}|>", f"<|{task}|>"]
    if not timestamps:
        tokens.append("<|notimestamps|>")
    return tokens
```

这就是完整的任务控制面。一个 4-token 前缀。

## 用框架实现

```python
import whisper
model = whisper.load_model("large-v3-turbo")
result = model.transcribe("meeting.wav", language="en", task="transcribe")
print(result["text"])
print(result["segments"][0]["start"], result["segments"][0]["end"])
```

更快，兼容 OpenAI：

```python
from faster_whisper import WhisperModel
model = WhisperModel("large-v3-turbo", compute_type="int8_float16")
segments, info = model.transcribe("meeting.wav", vad_filter=True)
for s in segments:
    print(f"{s.start:.2f} - {s.end:.2f}: {s.text}")
```

**2026 年何时选择 Whisper：**

- 用一个模型做多语言 ASR。
- 噪声、多样音频的鲁棒转录。
- 研究/原型 ASR——最快的起点。

**何时选择其他：**

- 边缘设备上的超低延迟流式——Moonshine 在匹配质量下击败 Whisper。
- 需要 <200 ms 的实时对话 AI——专用流式 ASR。
- 说话人分离——Whisper 不做这个；需要搭配 pyannote。

## 产出物

参见 `outputs/skill-asr-configurator.md`。该技能为新的语音应用选择 ASR 模型、解码参数和预处理管道。

## 练习题

1. **简单。** 运行 `code/main.py`。确认 16 kHz、10 ms 步幅的 1 秒信号的帧数约为 100 帧。对于 30 秒：约 3,000 帧。
2. **中等。** 使用 `numpy.fft` 构建完整的 log-mel 频谱图。验证 80 个梅尔频率 bin 在数值误差内与 `librosa.feature.melspectrogram(n_mels=80)` 匹配。
3. **困难。** 实现流式推理：将音频分成 10 秒窗口，2 秒重叠，在每个块上运行 Whisper，合并转录。在一个 5 分钟的播客样本上测量词错误率与单次完整处理相比。

## 术语速查表

| 术语 | 人们的说法 | 实际含义 |
|------|-----------|---------|
| 梅尔频谱图 | "音频图像" | 2D 表示：一轴为频率 bin，另一轴为时间帧；每个单元格为对数缩放的能量。 |
| Log-mel | "Whisper 看到的" | 经对数变换的梅尔频谱图；近似人耳对响度的感知。 |
| 帧 | "一个时间切片" | 25 ms 的采样窗口；以 10 ms 步幅重叠。 |
| 任务 token | "语音的提示前缀" | 解码器提示中的特殊 token，如 `<\|transcribe\|>` / `<\|translate\|>`。 |
| 语音活动检测 (VAD) | "找到语音" | 在 ASR 前消除静音的门控；大幅降低成本。 |
| CTC | "Connectionist Temporal Classification" | 经典的无对齐训练 ASR 损失；Whisper 不使用它。 |
| Whisper-turbo | "小编码器，完整编码器" | large-v3 编码器 + 4 层解码器；解码速度 8 倍提升。 |
| Faster-whisper | "生产封装" | CTranslate2 重新实现；int8 量化；比 OpenAI 参考快 4 倍。 |

## 延伸阅读

- [Radford 等人（2022）。Robust Speech Recognition via Large-Scale Weak Supervision](https://arxiv.org/abs/2212.04356) —— Whisper 论文。
- [OpenAI Whisper 仓库](https://github.com/openai/whisper) —— 参考代码 + 模型权重。阅读 `whisper/model.py` 可以在大约 400 行中从头到尾看到 Conv1D 主干 + 编码器 + 解码器。
- [OpenAI Whisper — `whisper/decoding.py`](https://github.com/openai/whisper/blob/main/whisper/decoding.py) —— 步骤 5-6 中描述的束搜索 + 任务 token 逻辑在这里；500 行，完全可读。
- [Baevski 等人（2020）。wav2vec 2.0: A Framework for Self-Supervised Learning of Speech Representations](https://arxiv.org/abs/2006.11477) —— 前身；在某些设置中仍然是 SOTA 特征。
- [SYSTRAN/faster-whisper](https://github.com/SYSTRAN/faster-whisper) —— 生产封装，比参考快 4 倍。
- [Jia 等人（2024）。Moonshine: Speech Recognition for Live Transcription and Voice Commands](https://arxiv.org/abs/2410.15608) —— 2024 年边缘友好 ASR，Whisper 形状但更小。
- [HuggingFace 博客 — "Fine-Tune Whisper For Multilingual ASR with 🤗 Transformers"](https://huggingface.co/blog/fine-tune-whisper) —— 规范的微调方案，包括梅尔频谱图预处理器和 token-时间戳处理。
- [HuggingFace `modeling_whisper.py`](https://github.com/huggingface/transformers/blob/main/src/transformers/models/whisper/modeling_whisper.py) —— 完整实现（编码器、解码器、交叉注意力、生成），与本课的架构图对应。
