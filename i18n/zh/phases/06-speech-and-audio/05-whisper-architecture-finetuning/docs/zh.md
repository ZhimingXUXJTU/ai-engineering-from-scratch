# 语 建筑和调整

> 语是30秒钟的窗口变压器编码解码器,训练在多语言弱监督的音频文本对数的68万小时.一个架构,多任务,强大的99种语言.2026年参考ASR.

> **【中文解读】**微笑是30秒窗口的变压器编码器解码器,在68万小时多语言弱监督音频文本对上训练.

> **【拓展：Whisper 的生态】**语 衍生了语.cpp(本地部署)、Faster-Whisper(CTtranslate2 加速)、语X(词级时间)、布鲁姆斯伯里(实时流式) 等工具链,是语音识别工业部署的事实标准──

**Type:** Build | **类型:** 构建
**Languages:** Python | **语言:** Python
**Prerequisites:** Phase 6 · 04 (ASR), Phase 5 · 10 (Attention), Phase 7 · 05 (Full Transformer) | **前置知识:** 阶段 6 · 04（ASR），阶段 5 · 10（注意力机制），阶段 7 · 05（完整 Transformer）
**Time:** ~75 minutes | **预计用时:** ~75 分钟

## 问题 问题引入

微声,由OpenAI于2022年9月发布,是首个作为商品的ASR模型:粘贴音频,获取文字,99种语言,强于噪音,运行在笔记本电脑上.到2024年,OpenAI已经发送了Large-v3和Turbo变体;到2026年,微声是自定义的基线,从播客转录到语音助手到YouTube字幕.

> 微笑由OpenAI于2022年9月发布,是第一个作为通用商品发布的ASR模型:粘贴音频,获取文本,99种语言,抗噪声,可在笔记本上运行.到2024年,OpenAI发布了Large-v3 和Turbo变体;到2026年,微笑是从播客转录到语音助手到YouTube字幕等所有场景的默认基线.

> **【中文解读】**本节提出的问题是:如何在实际工程中正确理解和应用这一技术――理解问题背景有助于把握技术选择的关键决策点――在实际人工智能系统中,错误的技术选择往往比实现细节的错误成本更高――

语不是一个管道,你可以永远把它当作一个黑盒子.域名转移杀了它.

> 但语不是可以永远当黑盒使用流水线――领域偏移会破坏它技术术语、说话人口音、专名词、短片段、静音――你需要知道:

1. 实际上是什么?
   它内部是什么结构.
2. 如何正确地播放碎片,流媒体或长音频.
   如何正确地给它分块,流式或长音频输入.
3. 什么时候和如何调整.
   如何调微调以及如何调微调.

> **【中文解读】**本节介绍核心概念和理论基础.掌握这些概念是后续动手实现的前提,同时也是面试和工程实践中高频考察的知识点.


## 概念的核心概念

![Whisper encoder-decoder, tasks, chunked inference, fine-tune](../assets/whisper.svg)

**Architecture.**标准变压器编码器-解码器.

> **架构。**标准变压器编码器解码器

- 输入:30秒钟的日志-邮件谱,80mels,10ms跳 →3000个框架.更短的剪辑是零,更长的剪辑是碎片.
  输入30秒 频谱图,80mels,10 ms 步长 → 3000 ──短片段零填充,长片段分块──
- 编码器: conv-downsample (步骤2) + `N`对于大型V3: 32层, 1280层, 20头.
  编码器:卷积下采样(步幅2) + `N`个变压器块──大v3:32层,1280维,20头──
- 解码器:`N`变压器块具有因果自动接入 + 交叉接入到编码输出. 与编码器相同的尺寸.
  解码器:`N`个带因果自注意力 + 对编码器输出交叉注意力变压器块──与编码器同大小──
- 输出:BPE代币超过51,865代币的词汇.
  输出:51,865代币 词表上的BPE代币.

大型v3具有1.55B参数.Turbo使用4层解码器 (从32),切割延迟8x,WER击中<1% .

> 轮使用4层解码器 ((从32层减少),延迟降低8倍,WER 损失不到1%──

**The prompt format.**语是一个多任务模型,由解码器提示中的特殊代币控制:

> **提示格式。**语是一个多任务模型,通过解码器提示中的特殊代号来控制:

```
<|startoftranscript|><|en|><|transcribe|><|notimestamps|> Hello world.<|endoftext|>
```

- `<|en|>`语言标签;强迫翻译对转录行为.
  `<|en|>` 语言标签;强制翻译或转录行为──
- `<|transcribe|>`或`<|translate|>`从任何语言输入中翻译英语输出,或字面上翻译.
  `<|transcribe|>`或`<|translate|>` 从任何语言输入翻译为英文输出,或逐字转录.
- `<|notimestamps|>` 跳过字面级时间标签 (更快).
  `<|notimestamps|>` 跳过词级时间(更快) 

提示是让一个模型完成多项任务的.`<|en|>`为了`<|fr|>`它们写成法语.

> 提示就是让一个模型完成多种任务的关键.`<|en|>`改为`<|fr|>`在法语转录中.

**30-second window.**长片需要分片,短片需要.窗户不会本地流,这就是为什么存在的WhisperX,Whisper-Streaming和快速的.

> **30 秒窗口。**一切都以30秒为基准.更长的音频需要分块;更短的音频需要填充.窗户本身不支持原生流式处理.

**Log-mel normalization.** `(log_mel - mean) / std`您必须使用Whisper的预处理 (`whisper.audio.log_mel_spectrogram`),没有`librosa.feature.melspectrogram`现在,我们要去.

> **Log-mel 归一化。** `(log_mel - mean) / std`据说,这些数据来自Whisper自己的训练语料――你*必须*使用Whisper的预处理(`whisper.audio.log_mel_spectrogram`),而不是`librosa.feature.melspectrogram`,我知道.

### 2026年变种

> ### 2026 年变体

| Variant | Params | Latency (A100) | WER (LibriSpeech-clean) |
|---------|--------|----------------|------------------------|
| Tiny | 39M | 1× realtime | 5.4% |
| Base | 74M | 1× | 4.1% |
| Small | 244M | 1× | 3.0% |
| Medium | 769M | 1× | 2.7% |
| Large-v3 | 1.55B | 2× | 1.8% |
| Large-v3-turbo | 809M | 8× | 1.58% |
| Whisper-Streaming (2024) | 1.55B | streaming | 2.0% |

| 变体 | 参数量 | 延迟（A100） | WER（LibriSpeech-clean） |
|------|--------|--------------|-------------------------|
| Tiny | 3900 万 | 1× 实时 | 5.4% |
| Base | 7400 万 | 1× | 4.1% |
| Small | 2.44 亿 | 1× | 3.0% |
| Medium | 7.69 亿 | 1× | 2.7% |
| Large-v3 | 15.5 亿 | 2× | 1.8% |
| Large-v3-turbo | 8.09 亿 | 8× | 1.58% |
| Whisper-Streaming（2024） | 15.5 亿 | 流式 | 2.0% |

### 调整

> ### 微调

2026年可尼加工作流程:

> 2026 年标准流程:

1. 收集10100小时的目标域音频,并进行排列的转录.
   收集 10-100 小时目标领域的音频及对应转录文本.
2. 跑步`transformers.Seq2SeqTrainer`随着`generate_with_loss`呼叫回来.
   使用 `transformers.Seq2SeqTrainer`和 `generate_with_loss`回调运行训练――
3. 参数效率: 洛拉`q_proj`现在`k_proj`现在`v_proj`显著的GPU存储量4x,WER成本为<0.3
   参数高效:在注意力层面的`q_proj`,我知道.`k_proj`,我知道.`v_proj`上使用Lora,GPU内存降低4倍,WER损失 <0.3──
4. 如果有<10小时,请结编码器.
   如果数据不足10小时则结结编码器,只调解微调码器.
5. 使用Whisper自己的代币标记器和提示格式;永远不要交换代币标记器.
   使用Whisper 自己的代币和提示格式;永远不要替换代代币.

社区结果:调整:医疗指示20小时的中度调整降低了医疗词汇的WER12%至4.5%.

> 社区结果:在20小时医疗口述上调中,医疗词汇 WER从12% 降至4.5%──在4小时冰岛语上微调Turbo,WER从18% 降至6%──

> **【拓展：语音 AI 的产品化】**语音技术在产品化中面临着独特的挑战:不同口音,背景噪音,远场拾音,多人说话等.

> **【拓展：多语言语音技术】**全球语言的语音特性差异巨大:声调语言的音高携带语义,低资源语言缺乏训练数据――Meta的MMS模型支持1000多种语言的语音识别,语在多语言场景表现出色,但仍然需要针对特定语言微调――



## 建立它,实现它.

> **【中文解读】**本节通过代码实现从零到核心算法――这种"从零开始"的方式可以帮助理解框架背后的原理,遇到问题时不会被黑盒困住――

```figure
sp-asr-attention
```

## 建立它

### 步骤1: 运行Whisper

```python
import whisper
model = whisper.load_model("large-v3-turbo")
result = model.transcribe(
    "clip.wav",
    language="en",
    task="transcribe",
    temperature=0.0,
    condition_on_previous_text=False,  # prevents runaway repetition
)
print(result["text"])
for seg in result["segments"]:
    print(f"[{seg['start']:.2f}–{seg['end']:.2f}] {seg['text']}")
```

您应该总是取消关键默认问题: `temperature=0.0`(取样默认到0.0 → 0.2 → 0.4 ...反弹链), `condition_on_previous_text=False`(防止结幻觉问题),`no_speech_threshold=0.6`它们是的.

> 你应该永远覆盖关键默认值:`temperature=0.0`(采样默认为0.0 → 0.2 → 0.4 ... 回退链)`condition_on_previous_text=False`防止级联幻觉问题`no_speech_threshold=0.6`现在,我知道.

### 步骤2:长形碎片

```python
# whisperx is the 2026 reference for long-form with word-level timestamps
import whisperx
model = whisperx.load_model("large-v3-turbo", device="cuda", compute_type="float16")
segments = model.transcribe("1hour.mp3", batch_size=16, chunk_size=30)
```

微声X增加了 (1) Silero VAD 盖特, (2) 通过 wav2vec 2.0 进行文字水平排列, (3) 通过 日记化`pyannote.audio`作为2026年生产转录的工作马.

> 微笑X 添加了 (1) Silero VAD 门控,(2) 通过 wav2vec 2.0 实现词级对齐,(3) 通过 `pyannote.audio`实现说话人分离──2026年生产转录的主力工具──

### 步骤3:使用LoRA进行细调

```python
from transformers import WhisperForConditionalGeneration, WhisperProcessor
from peft import LoraConfig, get_peft_model

model = WhisperForConditionalGeneration.from_pretrained("openai/whisper-large-v3-turbo")
lora = LoraConfig(
    r=16, lora_alpha=32, target_modules=["q_proj", "v_proj"],
    lora_dropout=0.1, bias="none", task_type="SEQ_2_SEQ_LM",
)
model = get_peft_model(model, lora)
# model.print_trainable_parameters()  -> ~3M trainable / 809M total
```

然后是标准训练者循环,每1000步就有一个检查点,然后用WER来评估.

> 然后标准的训练循环. 每1000步保存检查点.

### 步骤4:检查每个层学到什么

```python
# Grab cross-attention weights during decode to see what the decoder attends to.
with torch.inference_mode():
    out = model.generate(
        input_features=features,
        return_dict_in_generate=True,
        output_attentions=True,
    )
# out.cross_attentions: layer × head × step × src_len
```

> **【中文解读】**本节展示了如何使用成熟框架 (如PyTorch、HuggingFace等) 快速应用该技术.


通过热图可视化,您将看到对角的对齐,因为解码器步骤通过编码器框架扫描.

> 用热力图可视化你会看到解码器步进扫描编码器时对角线对齐.那条对角线就是语的词时间概念.




> **【拓展：语音与情感计算】**语音不仅传递文字信息,还携带丰富的情感信号 (语调、语速、音高变化) 情感语音识别 (语音识别,语音情感识别,SER) 在客服质检,心理健康监测,智能教育等领域广泛应用.

## 用它实现框架

现在,我们要做什么?

> 2026 年技术:

| Situation | Pick |
|-----------|------|
| General English, offline | Large-v3-turbo via `whisperx` |
| Mobile / edge | Whisper-Tiny quantized (int8) or Moonshine |
| Multilingual long-form | Large-v3 via `whisperx` + diarization |
| Low-resource language | Fine-tune Medium or Turbo with LoRA |
| Streaming (2 s latency) | Whisper-Streaming or Parakeet-TDT |
| Word-level timestamps | WhisperX (forced alignment via wav2vec 2.0) |

| 场景 | 选择 |
|------|------|
| 通用英文、离线 | 通过 `whisperx` 使用 Large-v3-turbo |
| 移动端/边缘设备 | 量化 Whisper-Tiny（int8）或 Moonshine |
| 多语言长音频 | 通过 `whisperx` 使用 Large-v3 + 说话人分离 |
| 低资源语言 | 用 LoRA 微调 Medium 或 Turbo |
| 流式（2 秒延迟） | Whisper-Streaming 或 Parakeet-TDT |
| 词级时间戳 | WhisperX（通过 wav2vec 2.0 强制对齐） |

`faster-whisper`(CTranslate2后端) 是2026年最快的CPU+GPU推断运行时间,比尼拉快4x,具有相同输出.

> `faster-whisper`(CTranslate2后端) 是2026年最快的CPU+GPU 推理运行时比原版快4倍,输出完全相同.



## 陷在2026年仍存在

> 2026年仍在犯案陷中

- **Hallucinated text on silence.**语训练在标题包括"谢谢你观看!","订阅!",歌词.
  **静音上的幻觉文本。**在字幕数据上训练中,会包含"谢谢观看!""",订阅!"、歌词――调用前务必用 VAD 过──
- **`condition_on_previous_text` cascade.**一个幻觉会污染后续的窗户.`False`除非你需要流动的分块.
  **`condition_on_previous_text` 级联。**经过一次幻觉会污染后续窗口,除非需要跨块流性,否则设为`False`,我知道.
- **Short-clip padding.**两秒钟的剪辑,被成30秒钟,可以在后续的沉默中产生幻觉.`pad=False`或是VAD-gate.
  **短片段填充。**两个秒段充满到30秒可能在尾部静音处产生幻觉.`pad=False`或是过.
- **Wrong mel stats.**通过使用Librosa的而不是Whisper的,产生了近乎随机的输出.`whisper.audio.log_mel_spectrogram`现在,我们要去.
  **错误的 mel 统计量。**使用图书馆的而不是语的会产生近乎随机的输出.`whisper.audio.log_mel_spectrogram`,我知道.

> **【中文解读】**本节关注如何将模型部署为可用的产品. 从原型到生产级系统需要考虑性能优化,错误处理,监控等多个维度.


## 运送它.

保存如`outputs/skill-whisper-tuner.md`设计一个特定域的微声细调或推断管道.

> 保存为`outputs/skill-whisper-tuner.md`◎为特定领域设计 微调或推理流水线──

## 练习题

1. **Easy.**跑步`code/main.py`它标记了一个像"声"这样的提示,计算解码的形状预算,
   **简单。**运行`code/main.py`△它对"语风格"的提示进行代币化,计算解码形状预算,并打印10分钟音频的分块计划──
2. **Medium.**安装`faster-whisper`试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试`language="auto"`强迫的`language="en"`现在,我们要去.
   **中等。**装备`faster-whisper`转录10分钟播客,与人工转录比较 WER.`language="auto"`与强制`language="en"`,我知道.
3. **Hard.**使用HF`datasets`选择一个语言,Whisper与它所斗争的语言 (例如乌尔都),在两个小时内调整中度与洛拉两个时代,并报告WER的三角形.
   **困难。**使用HF `datasets`选择一个 微调 微调 平均 2 个时代,报告 WER 差值.

> **【中文解读】**在团队协作中,统一术语定义可以避免大量沟通误解.


## 关键词 快速查找表

| Term | What people say | What it actually means |
|------|-----------------|-----------------------|
| 30-sec window | Whisper's limit | Hard input cap; chunk longer audio. |
| SOT | Start-of-transcript | `<\|startoftranscript\|>` kicks off the decoder prompt. |
| Timestamps token | Temporal alignment | Every 0.02 s offset is a special token in the 51k vocab. |
| Turbo | The fast variant | 4-decoder layers, 8× faster, <1% WER regression. |
| WhisperX | The long-form wrapper | VAD + Whisper + wav2vec alignment + diarization. |
| LoRA fine-tune | Efficient tuning | Add low-rank adapters to attention; train ~0.3% of params. |
| Hallucination | The silent failure | Whisper produces fluent English from noise/silence. |

| 术语 | 人们常说的 | 实际含义 |
|------|-----------|---------|
| 30 秒窗口 | Whisper 的限制 | 硬性输入上限；更长音频需分块。 |
| SOT | 转录开始 | `<\|startoftranscript\|>` 启动解码器提示。 |
| 时间戳 token | 时间对齐 | 每 0.02 秒偏移是 51k 词表中的特殊 token。 |
| Turbo | 快速变体 | 4 层解码器，快 8 倍，WER 回退 <1%。 |
| WhisperX | 长音频封装 | VAD + Whisper + wav2vec 对齐 + 说话人分离。 |
| LoRA 微调 | 高效调优 | 在注意力层添加低秩适配器；仅训练约 0.3% 参数。 |
| 幻觉 | 静默失败 | Whisper 从噪声/静音中产生流畅的英文。 |

> **【中文解读】**延伸阅读提供了深入学习的高质量资源. 这些论文和教程是该领域的经典参考文献,适合需要深入了解的读者.


## 继续阅读 继续阅读

- [Radford et al. (2022). Whisper paper](https://arxiv.org/abs/2212.04356)原始的建筑和培训配方.
  拉德福德等 (2022). 语论文原始架构和训练方案
- [OpenAI (2024). Whisper Large-v3-turbo release](https://github.com/openai/whisper/discussions/2363)四层解码器,8倍加快.
  微笑大v3turbo 发布4层解码器,8倍加速──
- [Bain et al. (2023). WhisperX](https://arxiv.org/abs/2303.00747)长长的形式,词汇一致,日记化.
  语长音频,词级对齐,说话人分离.
- [Systran — faster-whisper repo](https://github.com/SYSTRAN/faster-whisper) CTranslate2支持,速度快4倍.
  系统快速语 仓库CTranslate2 后端,快4倍
- [HuggingFace — Whisper fine-tune tutorial](https://huggingface.co/blog/fine-tune-whisper)法规LoRA/全FT通行.
  抱擁面低声 微调教程标准 LoRA/全参数微调指南。

> **【中文解读】**延伸阅读提供了深入学习的高质量资源,包括论文,教程和工具.

