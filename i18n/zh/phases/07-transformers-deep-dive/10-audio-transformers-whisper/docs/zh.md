# 音频变压器   架构

> 音频是时间频率的图像. 语是一种吃掉光谱的 ViT,

> **【中文解读】**语音识别和翻译. 了解音频如何变成标志.

**Type:** Study | **类型:** 学习
**Language:**子**语言:**字符串
**Prerequisites:** Phase 7 · 05 (Full Transformer), Phase 7 · 08 (Encoder-Decoder), Phase 7 · 09 (ViT) | **前置知识:** Phase 7 · 05 (Full Transformer), Phase 7 · 08 (Encoder-Decoder), Phase 7 · 09 (ViT)
**Time:** ~45 minutes | **时间:** ~45 分钟

## 问题 问题引入

在Whisper之前 (OpenAI,Radford等2022年) 最先进的自动语音识别 (ASR) 意味着 wav2vec 2.0和HuBERT 自主监督的特征提取器以及一个精细调的头.高质量,昂贵的数据管道,域名脆性.多语言语音识别需要每个语言家庭的单独模型.

> 在Whisper,Radford等2022年之前,最先进的自动语音识别 (ASR) 使用了WAV2vec 2.0 和HuBERT自监督特征提取器加微调头.质量高,但数据管道昂贵,对领域敏感.多语言语音识别需要每个语言族的单独模型.

声打了三张注:

> 语做了三个注:

1. **Train on everything.**没有清洁的学术资料,没有音符标签.
   翻译: 中文**用一切数据训练。**没有干净的学术语料库,没有素标签.
2. **Multi-task single model.**一个解码器通过任务代币共同训练成文 transcription,翻译,语音活动检测,语言识别和时刻标记.
   翻译: 中文**单模型多任务。**一个解码器通过任务代币 联合训练转录、翻译、语音活动检测、语言识别和时间──
3. **Standard encoder-decoder transformer.**编码器使用日志邮件谱谱. 解码器自动降低生成文本代码. 没有声码器,没有CTC,没有HMM.
   翻译: 中文**标准编码器-解码器 Transformer。**编码器消费日志 频谱图――解码器自归生成文本代币――没有声码器,没有CTC,没有HMM――

结果:Whisper large-v3在零清洁标记数据的口音,噪音和语言中具有强度.它是2026年每个开源语音助理和大多数商业语言的默认语音前端.

> 结果:对口音,噪音和零标签数据的语言都有性.

> **【中文解读】**微笑的三大创新:(1) 用68万小时弱标注音频训练,覆盖 97种语言;(2) 单模型多任务(转录、翻译、语种识别、时间);(3) 标准编码器-解码器 变码器 架构──音频被转换为日志 频谱图(类似图像),编码器处理频谱特征,解码器生成文本──

## 概念的核心概念

![Whisper pipeline: audio → mel → encoder → decoder → text](../assets/whisper.svg)

### 步骤 1 重复样本+窗口

音频 16 kHz. 剪辑/pad 30 秒. 计算日志-邮件谱: 80 个音符, 10 毫米步骤 → ~ 3,000 个框架 × 80 个功能.这是Whisper 看到的"输入图像".

> 音频采样率 16 kHz──剪切/填充到30秒──计算日志-邮件频谱图:80个梅尔频率bin,10 ms 步长 → 约3000  × 80 特征──这是"输入图像"的"语看"──

### 步骤 2 卷积干

两个Conv1D层,内核3和步骤2将3000个框架缩小到1,500个.

> 两层 Conv1D(核大小 3,步长 2) 将3,000 减少到1,500 ──将序列长度减半而不增加太多参数──

> **【拓展：Whisper 的多语言能力来源】**语在 97种语言,680万小时音频上训练,多语言能力来自两个因素: 1) 超大规模的弱标签数据覆盖绝大多数语言; 2) 统一的BPE词表是GPT-2词表的超集,天然支持多语言――解码器提示 中的语言代币如`<|zh|>`)控制输出语言,使同一模型能够执行转录或翻译任务.

### 步骤 3 编码器

转变器编码器24层 (大型) 超过1500个时间步骤. 静脉定位编码,自觉注意力,GELU FFN. 产生1500 × 1,280个隐藏状态.

> 一个24层的变压器编码器处理1,500个时间步骤――正弦位置编码、自注意力、GELU FFN――产生1,500 × 1,280 的隐藏状态――

### 步骤 4 解码器

它自动降低地从BPE词汇中生成代币,这是GPT-2的超集,有几个特定音频的特殊代币.

> 一个24层变压器 解码器──自归地从BPE词表生成代币,该词表是GPT-2词表的超集,外加几个音频专用特殊代币──

### 步骤 5 任务代币

解码提示开始使用控制代币告诉模型该怎么做:

> 解码器提示 控制代币 开头,告诉模型要做什么:

```
<|startoftranscript|>  <|en|>  <|transcribe|>  <|0.00|>
```

或

```
<|startoftranscript|>  <|fr|>  <|translate|>   <|0.00|>
```

模型是根据这个公约训练的.你用前控制任务. 2026 相当于指令调整,但适用于语音.

> 模型按这种约定训练――你通过前控制任务――这是语音领域的指令微调等价物――

> **【中文解读】**通过在解码器前中添加特殊的标记(如`<|transcribe|>`或`<|translate|>`) 指定任务类型.这是语音领域的应用中"指示微调" 通过不同的前代币执行不同的任务.

> **【拓展：Whisper 在语音助手中的应用】**语是2026年语音人工智能的基础组件. 从实时语音助手到视频字幕生成,再到多语言会议翻译,语提供统一语音前端.

### 步骤 6 输出

随着测试记录的值,随着测试记录的值,每0.02秒钟的音频时,`<|notimestamps|>`标志是缺失的.

> 束搜索(宽度 5)加对数概率值──当没有`<|notimestamps|>`时,每0.02秒预测一次时间──

### 语尺寸

| Model | Params | Layers | d_model | Heads | VRAM (fp16) |
|-------|--------|--------|---------|-------|-------------|
| 模型 | 参数量 | 层数 | d_model | 头数 | 显存 (fp16) |
| Tiny | 39M | 4 | 384 | 6 | ~1 GB |
| Base | 74M | 6 | 512 | 8 | ~1 GB |
| Small | 244M | 12 | 768 | 12 | ~2 GB |
| Medium | 769M | 24 | 1024 | 16 | ~5 GB |
| Large | 1550M | 32 | 1280 | 20 | ~10 GB |
| Large-v3 | 1550M | 32 | 1280 | 20 | ~10 GB |
| Large-v3-turbo | 809M | 32 | 1280 | 20 | ~6 GB (4-layer decoder) |

大v3turbo (2024) 将解码器从32层缩小到4.8x更快的解码器,以 <1 WER 点回归.这解码速度解锁是为什么Whisper-turbo是2026年实时语音代理的默认.

> 由于这种解码速度的突破,WER 退化不到1个百分点.

> **【拓展：音频 Transformer 的统一趋势】**语音识别(语)、语音合成(VALL-E, Kokoro)、音乐生成(MusicGen) 都在转向变频架构.

### 语不做什么

- 没有日记,与笔记相对.
  中文翻译:没有说话人分离(谁在说话) ◊需要搭配笔使用.
- 没有实时流媒体本地 30秒窗口是固定的.`faster-whisper`现在`WhisperX`) 通过VAD+重叠的流通.
  中文翻译:没有原生实时流式处理30秒窗口是固定的──现代封装器(`faster-whisper`,我知道.`WhisperX`) 通过VAD+重叠实现流式处理――
- 没有长文本超过30秒,没有外部的碎片. 在实践中,它很好,因为人类的语言很少需要长文本来转录.
  中文翻译:没有外部块则不支持30秒以上长格式上下文──实际效果很好,因为人类语音转录很少需要长距离上下文──

### 2026年景观

| Task | Model | Notes |
|------|-------|-------|
| 任务 | 模型 | 备注 |
| English ASR | Whisper-turbo, Moonshine | Moonshine is 4× faster on edge |
| 英语 ASR | Whisper-turbo, Moonshine | Moonshine 在边缘设备上快 4 倍 |
| Multilingual ASR | Whisper-large-v3 | 97 languages |
| 多语言 ASR | Whisper-large-v3 | 97 种语言 |
| Streaming ASR | faster-whisper + VAD | 150 ms latency targets achievable |
| 流式 ASR | faster-whisper + VAD | 可实现 150ms 延迟目标 |
| TTS | Piper, XTTS-v2, Kokoro | Encoder-decoder pattern, but Whisper-shaped |
| TTS | Piper, XTTS-v2, Kokoro | 编码器-解码器模式，但类似 Whisper |
| Audio + language | AudioLM, SeamlessM4T | Text tokens + audio tokens in one transformer |
| 音频 + 语言 | AudioLM, SeamlessM4T | 文本 token + 音频 token 在一个 Transformer 中 |

## 建立它,实现它.
```figure
n5-mel-decode
```

## 建立它

看到`code/main.py`我们不训练Whisper,我们构建了"日志邮件谱"管道,

> 参见`code/main.py`我们不训练 微笑 构建日志 频谱图管道 任务代码 提示格式化器 这些是你在生产中实际接触的部分.

### 步骤1:合成音频

产生1秒的光阴波,在440Hz,采用16kHz的样本.

> 成一个1秒的440Hz正弦波,采样率16kHz──16,000个采样点──

### 步骤2:日志通讯谱 (简化)

我们做了一个简单的框架+每框架的能量版本,`librosa`其他:

> 我们做了一个简化的分+每次能量版本,无需`librosa`展示管道:

```python
def frame_signal(x, frame_size=400, hop=160):
    frames = []
    for start in range(0, len(x) - frame_size + 1, hop):
        frames.append(x[start:start + frame_size])
    return frames
```

片的能量是教育的片.

>  = 25 ms,步长 = 10 ms──与语的窗口匹配──逐个能量用于教学演示,替代梅尔频率──

### 步骤3: 到30秒

语总是处理30秒的块. 片或剪辑光谱到3000个图片.

> 总是处理30秒的分块.

### 步骤 4: 建立提示令牌

```python
def whisper_prompt(lang="en", task="transcribe", timestamps=True):
    tokens = ["<|startoftranscript|>", f"<|{lang}|>", f"<|{task}|>"]
    if not timestamps:
        tokens.append("<|notimestamps|>")
    return tokens
```

这就是整个任务控制表面.

> 这就是所有任务控制接口的前.

## 用它实现框架

```python
import whisper
model = whisper.load_model("large-v3-turbo")
result = model.transcribe("meeting.wav", language="en", task="transcribe")
print(result["text"])
print(result["segments"][0]["start"], result["segments"][0]["end"])
```

快速,与OpenAI兼容:

> 更快的与OpenAI兼容方案:

```python
from faster_whisper import WhisperModel
model = WhisperModel("large-v3-turbo", compute_type="int8_float16")
segments, info = model.transcribe("meeting.wav", vad_filter=True)
for s in segments:
    print(f"{s.start:.2f} - {s.end:.2f}: {s.text}")
```

**When to pick Whisper in 2026:**

> **2026 年何时选择 Whisper：**

- 具有多语言的ASR,一个模型.
  中文翻译:用一个模型做多语言ASR。
- 强大的音频转录.
  中文翻译:对噪音大,多样化的音频进行鲁棒转录.
- 研究/原型ASR 最快的起点.
  中文翻译:研究/原型ASR最快的起点──

**When to pick something else:**

> **何时选择其他方案：**

- 极低延迟在边缘流 月光比语在匹配的质量.
  中文翻译:边缘设备上的超低延迟流式处理月光在相同质量下比语更快――
- 需要200 ms 专用流媒体ASR的实时对话AI.
  中文翻译:需要 <200ms 的实时对话 AI专用流式 ASR。
-  语不这样做; 在平笔上.
  中文翻译:说话人分离 低声 不做这个;需要加装笔记.

## 运送它.

看到`outputs/skill-asr-configurator.md`技能选择一个ASR模型,解码参数,以及为新的语音应用程序进行预处理.

> 参见`outputs/skill-asr-configurator.md`△这个技能为新语音应用选择ASR模型、解码参数和预处理管道.

## 练习题

1. **Easy.**跑步`code/main.py`确认一个秒钟信号的16kHz,10ms跳跃是~100个.30秒钟:~3,000个.
   中文翻译:运行 `code/main.py`▽确认1秒信号在16kHz,10ms步长下约100──30秒:约3,000──
2. **Medium.**使用 构建完整的日志邮件谱`numpy.fft`检查80个桶的匹配`librosa.feature.melspectrogram(n_mels=80)`在数值错误中.
   中文翻译:用`numpy.fft`构建完整的日志频谱图――验证 80 个日志频率`librosa.feature.melspectrogram(n_mels=80)`在数值差距范围内一致.
3. **Hard.**实现流传推断:将部分音频分为10秒的窗户,并进行2秒的重叠,在每个部分运行Whisper,并并并转录.在5分钟播客样本上测量文字错误率与单次传输率.
   中文翻译:实现流式推理:将音频分成10秒窗口(2秒重叠),在每个窗口上运行 语,合并转录――在5分钟播客样本上测量词语错误率与单次处理的对比――

## 关键词 快速查找表

| Term | What people say | What it actually means |
|------|-----------------|-----------------------|
| 术语 | 通俗说法 | 实际含义 |
| Mel spectrogram | "Audio image" | 2D representation: frequency bins on one axis, time frames on the other; log-scaled energy per cell. |
| 梅尔频谱图 | "音频图像" | 2D 表示：一个轴是频率 bin，另一个是时间帧；每个单元是对数缩放的能量。 |
| Log-mel | "What Whisper sees" | Mel spectrogram passed through log; approximates human perception of loudness. |
| Log-mel | "Whisper 看到的" | 梅尔频谱图取对数；近似人类对响度的感知。 |
| Frame | "One time slice" | A 25 ms window of samples; overlapping at 10 ms stride. |
| 帧 | "一个时间切片" | 25 ms 的采样窗口；10 ms 步长重叠。 |
| Task token | "Prompt prefix for speech" | Special tokens like `<\|transcribe\|>` / `<\|translate\|>` in the decoder prompt. |
| 任务 token | "语音的提示前缀" | 解码器提示中的特殊 token，如 `<\|transcribe\|>` / `<\|translate\|>`。 |
| Voice activity detection (VAD) | "Find the speech" | Gate that removes silence before ASR; cuts cost massively. |
| 语音活动检测 (VAD) | "找到语音" | 在 ASR 之前去除静音的门控；大幅降低成本。 |
| CTC | "Connectionist Temporal Classification" | Classic ASR loss for alignment-free training; Whisper does NOT use it. |
| CTC | "连接主义时间分类" | 经典的 ASR 对齐无关训练损失；Whisper 不使用它。 |
| Whisper-turbo | "Small decoder, full encoder" | large-v3 encoder + 4-layer decoder; 8× faster decoding. |
| Whisper-turbo | "小解码器，全编码器" | large-v3 编码器 + 4 层解码器；解码速度提高 8 倍。 |
| Faster-whisper | "The production wrapper" | CTranslate2 reimplementation; int8 quantization; 4× faster than OpenAI's reference. |
| Faster-whisper | "生产封装器" | CTranslate2 重新实现；int8 量化；比 OpenAI 参考实现快 4 倍。 |

## 继续阅读 继续阅读

- [Radford et al. (2022). Robust Speech Recognition via Large-Scale Weak Supervision](https://arxiv.org/abs/2212.04356) 语纸.
  中文翻译:语论文──
- [OpenAI Whisper repo](https://github.com/openai/whisper)参考码+模型重量.`whisper/model.py`查看Conv1D干 +编码器 +解码器从上到下,在400行左右.
  中文翻译:OpenAI 微笑代码仓库,约400 行代码展示Conv1D干 + 编码器 + 解码器──
- [OpenAI Whisper — `whisper/decoding.py`](https://github.com/openai/whisper/blob/main/whisper/decoding.py)步骤56中描述的光束搜索+任务标志逻辑在这里;500行,可以完全阅读.
  中文翻译:束搜索 + 任务代币 逻辑的实现,500 行代码,完全可读──
- [Baevski et al. (2020). wav2vec 2.0: A Framework for Self-Supervised Learning of Speech Representations](https://arxiv.org/abs/2006.11477)前;在某些设置中仍然具有SOTA功能.
  中文翻译:wav2vec 2.0 论文;Whisper 的前身,在某些场景下仍然是SOTA特征──
- [SYSTRAN/faster-whisper](https://github.com/SYSTRAN/faster-whisper)生产包装,比参考快4倍.
  中文翻译:快速语 生产封装器,比参考实现快4倍.
- [Jia et al. (2024). Moonshine: Speech Recognition for Live Transcription and Voice Commands](https://arxiv.org/abs/2410.15608) 2024 边缘友好的ASR,有声形状但较小.
  中文翻译:月亮论文,2024年面向边缘的ASR,类 低声但更小──
- [HuggingFace blog — "Fine-Tune Whisper For Multilingual ASR with 🤗 Transformers"](https://huggingface.co/blog/fine-tune-whisper)加нони化精细调节配方,包括MEL光谱预处理器和代币时刻标签处理.
  中文翻译:HuggingFace 微调教程,包括梅尔频谱图预处理器和代币 时间处理
- [HuggingFace `modeling_whisper.py`](https://github.com/huggingface/transformers/blob/main/src/transformers/models/whisper/modeling_whisper.py)完全实现 (编码器,解码器,交叉注意力,生成) 反映了课程的架构图图.
  中文翻译:HuggingFace 完整实现 (编码器,解码器,交叉注意力,生成),与课程架构对应.
