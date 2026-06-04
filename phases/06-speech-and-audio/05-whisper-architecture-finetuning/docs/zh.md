# Whisper — 架构与微调

> Whisper 是 30 秒窗口的 Transformer 编码器-解码器，在 68 万小时多语言弱监督音频-文本对上训练。一个架构，多种任务（识别、翻译、语言检测），覆盖 99 种语言。是 2026 年语音识别的标杆模型。

> **【中文解读】** Whisper 是 30 秒窗口的 Transformer 编码器-解码器，在 68 万小时多语言弱监督音频-文本对上训练。一个架构，多种任务（识别、翻译、检测语言），覆盖 99 种语言。是 2026 年语音识别的标杆模型。

> **【拓展：Whisper 的生态】** Whisper 衍生了 whisper.cpp（本地部署）、Faster-Whisper（CTranslate2 加速）、WhisperX（词级时间戳）、Bloomsbury（实时流式）等工具链，是语音识别工业部署的事实标准。

**类型：** 构建
**语言：** Python
**前置条件：** 阶段 6 · 04（ASR），阶段 5 · 10（注意力机制），阶段 7 · 05（完整 Transformer）
**时长：** 约 75 分钟

## 问题引入

Whisper 由 OpenAI 于 2022 年 9 月发布，是第一个作为通用商品发布的 ASR 模型：粘贴音频，获取文本，99 种语言，对噪声鲁棒，可在笔记本上运行。到 2024 年，OpenAI 发布了 Large-v3 和 Turbo 变体；到 2026 年，Whisper 是从播客转录到语音助手到 YouTube 字幕等一切应用的默认基线。

> **【中文解读】** 本节提出的问题是：如何在实际工程中正确理解和应用这一技术。理解问题背景有助于把握技术选型的关键决策点。在实际 AI 系统中，错误的技术选型往往比实现细节的 bug 代价更高。

但 Whisper 不是你可以永远当作黑盒使用的流水线。领域偏移会摧毁它——专业术语、说话人口音、专有名词、短片段、静音。你需要知道：

1. 它内部到底是什么。
2. 如何正确地给它分块、流式或长音频。
3. 何时微调以及如何微调。

> **【中文解读】** 本节介绍核心概念和理论基础。掌握这些概念是后续动手实现的前提，同时也是面试和工程实践中高频考察的知识点。

## 核心概念

![Whisper 编码器-解码器、任务、分块推理、微调](../assets/whisper.svg)

**架构。** 标准 Transformer 编码器-解码器。

- 输入：30 秒对数 Mel 频谱图，80 Mel，10 ms 步移 -> 3000 帧。短片段零填充，长片段分块。
- 编码器：卷积下采样（步移 2）+ `N` 个 Transformer 块。Large-v3：32 层，1280 维，20 个注意力头。
- 解码器：`N` 个 Transformer 块，带因果自注意力 + 对编码器输出的交叉注意力。与编码器相同大小。
- 输出：51,865 个 token 词汇表上的 BPE token。

Large-v3 有 15.5 亿参数。Turbo 使用 4 层解码器（从 32 层减少），延迟降低 8 倍，WER 损失不到 1%。

**提示格式。** Whisper 是一个多任务模型，通过解码器提示中的特殊 token 来控制：

```
<|startoftranscript|><|en|><|transcribe|><|notimestamps|> Hello world.
```

- `<|en|>` —— 语言标签；强制翻译 vs 转录行为。
- `<|transcribe|>` 或 `<|translate|>` —— 将任何语言输入翻译成英文输出，或逐字转录。
- `<|notimestamps|>` —— 跳过词级时间戳（更快）。

提示让一个模型做多种任务。将 `<|en|>` 改为 `<|fr|>` 就转录法语。

**30 秒窗口。** 一切都锚定在 30 秒。更长的片段需要分块；更短的片段被填充。窗口本身不支持流式——这就是 WhisperX、Whisper-Streaming 和 faster-whisper 存在的原因。

**对数 Mel 归一化。** `(log_mel - mean) / std`，其中统计量来自 Whisper 自己的训练语料。你*必须*使用 Whisper 的预处理（`whisper.audio.log_mel_spectrogram`），而不是 `librosa.feature.melspectrogram`。

### 2026 年的变体

| 变体 | 参数 | 延迟（A100） | WER（LibriSpeech-clean） |
|------|------|--------------|--------------------------|
| Tiny | 39M | 1x 实时 | 5.4% |
| Base | 74M | 1x | 4.1% |
| Small | 244M | 1x | 3.0% |
| Medium | 769M | 1x | 2.7% |
| Large-v3 | 15.5 亿 | 2x | 1.8% |
| Large-v3-turbo | 809M | 8x | 1.58% |
| Whisper-Streaming（2024） | 15.5 亿 | 流式 | 2.0% |

### 微调

2026 年的标准工作流：

1. 收集 10-100 小时的目标领域音频及对齐转录。
2. 使用 `transformers.Seq2SeqTrainer` 配合 `generate_with_loss` 回调运行。
3. 参数高效：在注意力层的 `q_proj`、`k_proj`、`v_proj` 上使用 LoRA，GPU 内存减少 4 倍，WER 代价不到 0.3。
4. 如果不到 10 小时数据，冻结编码器。只调解码器。
5. 使用 Whisper 自己的分词器和提示格式；永远不要更换分词器。

社区结果：在 20 小时医疗口述数据上微调 Medium，WER 从 12% 降至 4.5%。在 4 小时冰岛语上微调 Turbo，WER 从 18% 降至 6%。

> **【拓展：语音 AI 的产品化】** 语音技术在产品化中面临独特挑战：不同口音、背景噪声、远场拾音、多人说话等。Siri、Alexa、小爱同学等产品都投入了大量工程优化来解决这些 "长尾问题"。实时性要求（<300ms 延迟）也是语音产品的核心指标。

> **【拓展：多语言语音技术】** 全球语言的语音特性差异巨大：声调语言（如中文）的音高携带语义，低资源语言缺乏训练数据。Meta 的 MMS 模型支持 1000+ 种语言的语音识别，Whisper 在多语言场景表现出色，但仍需针对特定语言微调。

## 动手实现

> **【中文解读】** 本节通过代码从零实现核心算法。这种 "from scratch" 的方式能帮助理解框架背后的原理，遇到问题时不会被黑盒困住。

### 步骤 1：开箱即用运行 Whisper

```python
import whisper
model = whisper.load_model("large-v3-turbo")
result = model.transcribe(
    "clip.wav",
    language="en",
    task="transcribe",
    temperature=0.0,
    condition_on_previous_text=False,  # 防止失控重复
)
print(result["text"])
for seg in result["segments"]:
    print(f"[{seg['start']:.2f}–{seg['end']:.2f}] {seg['text']}")
```

你应始终覆盖的关键默认值：`temperature=0.0`（采样默认走 0.0 -> 0.2 -> 0.4 ... 回退链），`condition_on_previous_text=False`（防止级联幻觉问题），和 `no_speech_threshold=0.6`（静音检测）。

### 步骤 2：分块长音频

```python
# whisperx 是 2026 年带词级时间戳的长音频处理参考
import whisperx
model = whisperx.load_model("large-v3-turbo", device="cuda", compute_type="float16")
segments = model.transcribe("1hour.mp3", batch_size=16, chunk_size=30)
```

WhisperX 添加了 (1) Silero VAD 门控，(2) 通过 wav2vec 2.0 的词级对齐，(3) 通过 `pyannote.audio` 的说话人分离。2026 年生产转录的主力工具。

### 步骤 3：用 LoRA 微调

```python
from transformers import WhisperForConditionalGeneration, WhisperProcessor
from peft import LoraConfig, get_peft_model

model = WhisperForConditionalGeneration.from_pretrained("openai/whisper-large-v3-turbo")
lora = LoraConfig(
    r=16, lora_alpha=32, target_modules=["q_proj", "v_proj"],
    lora_dropout=0.1, bias="none", task_type="SEQ_2_SEQ_LM",
)
model = get_peft_model(model, lora)
# model.print_trainable_parameters()  -> 约 3M 可训练 / 809M 总计
```

然后标准 Trainer 循环。每 1000 步保存检查点。在留出集上用 WER 评估。

### 步骤 4：检查每层学到了什么

```python
# 在解码期间获取交叉注意力权重，查看解码器关注什么
with torch.inference_mode():
    out = model.generate(
        input_features=features,
        return_dict_in_generate=True,
        output_attentions=True,
    )
# out.cross_attentions: layer x head x step x src_len
```

> **【中文解读】** 本节展示如何用成熟框架（如 PyTorch、HuggingFace 等）快速应用该技术。在实际项目中，优先使用经过验证的框架实现，可以减少 bug 并提高开发效率。

用热力图可视化——你会看到解码步扫描编码器帧时的对角线对齐。那条对角线就是 Whisper 的词时间戳概念。

> **【拓展：语音与情感计算】** 语音不仅传递文字信息，还携带丰富的情感信号（语调、语速、音高变化）。情感语音识别（Speech Emotion Recognition, SER）在客服质检、心理健康监测、智能教育等领域有广泛应用。当前 SOTA 模型通常基于 wav2vec 2.0 或 HuBERT 等预训练模型微调。

## 用框架实现

2026 年的技术栈：

| 场景 | 选择 |
|------|------|
| 通用英语，离线 | Large-v3-turbo 通过 `whisperx` |
| 移动 / 边缘 | Whisper-Tiny 量化（int8）或 Moonshine |
| 多语言长音频 | Large-v3 通过 `whisperx` + 说话人分离 |
| 低资源语言 | 用 LoRA 微调 Medium 或 Turbo |
| 流式（2 秒延迟） | Whisper-Streaming 或 Parakeet-TDT |
| 词级时间戳 | WhisperX（通过 wav2vec 2.0 强制对齐） |

`faster-whisper`（CTranslate2 后端）是 2026 年最快的 CPU+GPU 推理运行时——比原始版本快 4 倍，输出完全相同。

## 2026 年仍在出现的陷阱

- **静音上的幻觉文本。** Whisper 在字幕数据上训练，包含 "Thanks for watching!"、"Subscribe!"、歌词。调用前务必 VAD 门控。
- **`condition_on_previous_text` 级联。** 一个幻觉污染后续窗口。除非需要跨块连贯性，否则设为 `False`。
- **短片段填充。** 2 秒片段填充到 30 秒可能在尾部静音上产生幻觉。使用 `pad=False` 或 VAD 门控。
- **错误的 Mel 统计量。** 使用 librosa 的 Mel 而不是 Whisper 的会产生近乎随机的输出。使用 `whisper.audio.log_mel_spectrogram`。

> **【中文解读】** 本节关注如何将模型部署为可用的产品。从原型到生产级系统需要考虑性能优化、错误处理、监控等多个维度。

## 产出物

保存为 `outputs/skill-whisper-tuner.md`。为给定领域设计 Whisper 微调或推理流水线。

## 练习题

1. **简单。** 运行 `code/main.py`。它将 Whisper 风格提示分词，计算解码形状预算，并打印 10 分钟片段的分块计划。
2. **中等。** 安装 `faster-whisper`，转录一个 10 分钟播客，与人工转录比较 WER。尝试 `language="auto"` vs 强制 `language="en"`。
3. **困难。** 使用 HF `datasets`，选一个 Whisper 挣扎的语言（如乌尔都语），用 LoRA 在 2 小时数据上微调 Medium 2 个 epoch，报告 WER 变化。

> **【中文解读】** 术语表中的 "What people say" vs "What it actually means" 区分了日常口语和精确技术含义。在团队协作中，统一术语定义可以避免大量沟通误解。

## 术语速查表

| 术语 | 通俗说法 | 实际含义 |
|------|----------|----------|
| 30 秒窗口 | Whisper 的限制 | 硬性输入上限；更长的音频需要分块。 |
| SOT | 转录开始 | `<|startoftranscript|>` 启动解码器提示。 |
| 时间戳 token | 时间对齐 | 每 0.02 秒偏移量是 51k 词汇表中的特殊 token。 |
| Turbo | 快速变体 | 4 层解码器，8 倍加速，<1% WER 回退。 |
| WhisperX | 长音频封装 | VAD + Whisper + wav2vec 对齐 + 说话人分离。 |
| LoRA 微调 | 高效调优 | 在注意力上添加低秩适配器；训练约 0.3% 参数。 |
| 幻觉 | 静默失败 | Whisper 从噪声/静音生成流畅的英文。 |

> **【中文解读】** 延伸阅读提供了深入学习的高质量资源。这些论文和教程是该领域的经典参考文献，适合需要深入理解的读者。

## 延伸阅读

- [Radford et al. (2022). Whisper 论文](https://arxiv.org/abs/2212.04356) —— 原始架构和训练方法。
- [OpenAI (2024). Whisper Large-v3-turbo 发布](https://github.com/openai/whisper/discussions/2363) —— 4 层解码器，8 倍加速。
- [Bain et al. (2023). WhisperX](https://arxiv.org/abs/2303.00747) —— 长音频、词对齐、说话人分离。
- [Systran — faster-whisper 仓库](https://github.com/SYSTRAN/faster-whisper) —— 基于 CTranslate2，4 倍加速。
- [HuggingFace — Whisper 微调教程](https://huggingface.co/blog/fine-tune-whisper) —— 标准的 LoRA / 全量微调指南。

> **【中文解读】** 延伸阅读提供了深入学习的高质量资源，包括论文、教程和工具。建议按需选读，优先阅读标注为 "the critical read" 的核心论文。
