# T5, BART — Encoder-Decoder Models | T5、BART — 编码器-解码器模型

> 编码器理解。解码器生成。把它们放回去，你就得到一个为输入→输出任务构建的模型：翻译、摘要、改写、转录。

> **【中文解读】** T5 把所有 NLP 任务统一为 text-to-text 格式。BART 用去噪自编码训练。适用于翻译、摘要等序列转换任务。

**类型：** 学习
**语言：** Python
**前置条件：** 阶段 7 · 05（完整 Transformer），阶段 7 · 06（BERT），阶段 7 · 07（GPT）
**时长：** 约 45 分钟

## 问题引入

纯解码器 GPT 和纯编码器 BERT 各自为不同目标精简了 2017 年架构。但许多任务天然是输入-输出形式：

- 翻译：英语 → 法语。
- 摘要：5,000-token 文章 → 200-token 摘要。
- 语音识别：音频 token → 文本 token。
- 结构化提取：散文 → JSON。

对于这些，编码器-解码器是最干净的适配。编码器产生源的密集表示。解码器生成输出，在每一步交叉关注该表示。训练是输出端的偏移一位。与 GPT 相同的损失，只是以编码器输出为条件。

两篇论文定义了现代方法：

1. **T5**（Raffel 等人 2019）。"Text-to-Text Transfer Transformer。"每个 NLP 任务重新定义为文本输入、文本输出。单一架构、单一词汇表、单一损失。在掩码片段预测上预训练（破坏输入中的片段，在输出中解码它们）。
2. **BART**（Lewis 等人 2019）。"Bidirectional and Auto-Regressive Transformer。"去噪自编码器：以多种方式破坏输入（打乱、掩码、删除、旋转），要求解码器重建原始内容。

2026 年，编码器-解码器格式在输入结构重要的地方延续：

- Whisper（语音 → 文本）。
- Google 的翻译栈。
- 一些具有独特上下文-编辑结构的代码补全/修复模型。
- Flan-T5 及其用于结构化推理任务的变体。

纯解码器赢得了聚光灯，但编码器-解码器从未消失。

> **【中文解读】** 编码器-解码器架构在"输入→输出"结构化任务中仍有优势。T5 将所有 NLP 任务统一为 text-to-text 格式，BART 用去噪自编码训练。虽然在纯文本生成领域被 Decoder-only 取代，但在语音识别（Whisper）、翻译、摘要等任务中仍是最佳选择。

## 核心概念

![带交叉注意力的编码器-解码器](../assets/encoder-decoder.svg)

### 前向循环

```
源 token ─▶ 编码器 ─▶ (N_src, d_model)  ──┐
                                            │
目标 token ─▶ 解码器块                      │
                ├─▶ 掩码自注意力            │
                ├─▶ 交叉注意力 ◀───────────┘
                └─▶ FFN
               ↓
             下一个 token 的 logits
```

关键是，编码器对每个输入只运行一次。解码器自回归运行但在每一步交叉关注*相同*的编码器输出。缓存编码器输出对长输入是免费的加速。

> **【中文解读】** 交叉注意力是编码器-解码器架构的信息桥梁：Q 来自解码器，K/V 来自编码器输出。编码器只运行一次（高效），解码器每步都通过交叉注意力访问编码器的完整输出。

> **【拓展：Whisper 的编码器-解码器设计】** OpenAI 的 Whisper 语音识别模型使用编码器-解码器架构，因为音频（梅尔频谱图）和文本是完全不同的模态。编码器处理音频特征，解码器生成文本。这种设计让 Whisper 能处理多语言语音识别和翻译任务，是 2026 年语音领域的事实标准。

### T5 预训练——片段破坏

选择输入中的随机片段（平均长度 3 个 token，共 15%）。用唯一哨兵替换每个片段：`<extra_id_0>`、`<extra_id_1>` 等。解码器只输出被破坏的片段及其哨兵前缀：

```
源：The quick <extra_id_0> fox jumps <extra_id_1> dog
目标：<extra_id_0> brown <extra_id_1> over the lazy
```

比预测整个序列更便宜的信号。在 T5 论文的消融实验中与 MLM（BERT）和前缀 LM（UniLM）有竞争力。

### BART 预训练——多噪声去噪

BART 尝试五种噪声函数：

1. Token 掩码。
2. Token 删除。
3. 文本填充（掩码一个片段，解码器插入正确长度）。
4. 句子排列。
5. 文档旋转。

结合文本填充 + 句子排列产生了最好的下游结果。解码器总是重建原始内容。BART 的输出是完整序列，而不仅是被破坏的片段——所以预训练计算比 T5 更高。

> **【中文解读】** T5 和 BART 的预训练策略不同：T5 的 span corruption 只预测被破坏的片段（高效），BART 的去噪自编码重建整个序列（更彻底但更贵）。选择取决于任务——T5 更适合 extractive 任务，BART 更适合 abstractive 任务。

### 推理

与 GPT 相同的自回归生成。贪心/束/top-p 采样都适用。束搜索（宽度 4-5）是翻译和摘要的标准，因为输出分布比聊天更窄。

> **【拓展：Beam Search 在翻译中的重要性】** 编码器-解码器模型在翻译和摘要任务中常用 beam search（宽度 4-5），因为输出分布较窄。Beam search 维护多个候选序列，每步保留得分最高的几个继续扩展。相比贪心搜索，beam search 能找到更优的全局序列；相比随机采样，它更稳定。在对话生成中通常不需要 beam search，因为输出分布更广。

### 2026 年何时选择每种变体

| 任务 | 编码器-解码器？ | 原因 |
|------|---------------|------|
| 翻译 | 是，通常 | 清晰的源序列；固定的输出分布；束搜索有效 |
| 语音转文本 | 是（Whisper） | 输入模态与输出不同；编码器塑造音频特征 |
| 聊天/推理 | 否，纯解码器 | 没有持久的"输入"——对话就是序列 |
| 代码补全 | 通常否 | 带长上下文的纯解码器胜出；Qwen 2.5 Coder 等代码模型是纯解码器 |
| 摘要 | 两者皆可 | BART、PEGASUS 击败了早期的纯解码器基线；现代纯解码器 LLM 匹配它们 |
| 结构化提取 | 两者皆可 | T5 很干净，因为"文本→文本"吸收了任何输出格式 |

约 2022 年以来的趋势：纯解码器接管了编码器-解码器曾经拥有的任务，因为 (a) 指令微调的纯解码器 LLM 通过提示泛化到任何任务，(b) 一种架构比两种更容易扩展，(c) RLHF 假设有一个解码器。编码器-解码器在输入模态不同（语音、图像）或束搜索质量重要的地方坚持下来。

> **【拓展：T5 的 text-to-text 统一范式】** T5 的核心理念是将所有 NLP 任务统一为"文本输入→文本输出"格式。翻译："translate English to French: Hello → Bonjour"；分类："sentiment: This movie is great → positive"。这种统一简化了架构和训练流程，也是后来 instruction tuning 和 prompt engineering 的思想源头。Flan-T5 更是通过指令微调大幅提升了零样本能力。

## 动手实现

参见 `code/main.py`。我们为玩具语料库实现了 T5 风格的片段破坏——这是本课最有用的单一部分，因为它出现在此后每个编码器-解码器预训练方案中。

### 步骤 1：片段破坏

```python
def corrupt_spans(tokens, mask_rate=0.15, mean_span=3.0, rng=None):
    """选择总和约为 mask_rate 的片段。返回（被破坏的输入，目标）。"""
    n = len(tokens)
    n_mask = max(1, int(n * mask_rate))
    n_spans = max(1, int(round(n_mask / mean_span)))
    ...
```

目标格式是 T5 约定：`<sent0> span0 <sent1> span1 ...`。被破坏的输入将未改变的 token 与片段位置的哨兵 token 交错。

### 步骤 2：验证往返

给定被破坏的输入和目标，重建原始句子。如果你的破坏是可逆的，前向传播就是良定义的。这是一个健全性检查——真实训练从不这样做，但测试很便宜，能发现片段簿记中的差一错误。

### 步骤 3：BART 噪声

五个函数：`token_mask`、`token_delete`、`text_infill`、`sentence_permute`、`document_rotate`。组合其中两个并展示结果。

## 用框架实现

HuggingFace 参考：

```python
from transformers import T5ForConditionalGeneration, T5Tokenizer
tok = T5Tokenizer.from_pretrained("google/flan-t5-base")
model = T5ForConditionalGeneration.from_pretrained("google/flan-t5-base")

inputs = tok("translate English to French: Attention is all you need.", return_tensors="pt")
out = model.generate(**inputs, max_new_tokens=32)
print(tok.decode(out[0], skip_special_tokens=True))
```

T5 技巧：任务名称进入输入文本。同一个模型处理数十个任务，因为每个任务都是文本输入、文本输出。2026 年，这种模式已被指令微调的纯解码器模型泛化，但 T5 最先将它规范化。

## 产出物

参见 `outputs/skill-seq2seq-picker.md`。该技能在编码器-解码器和纯解码器之间为新任务做选择，给定输入-输出结构、延迟和质量目标。

## 练习题

1. **简单。** 运行 `code/main.py`，对一个 30-token 的句子应用片段破坏，验证将非哨兵源 token 与解码目标片段拼接能重现原始内容。
2. **中等。** 实现 BART 的 `text_infill` 噪声：用单个 `<mask>` token 替换随机片段，解码器必须推断正确的片段长度加内容。展示一个示例。
3. **困难。** 在一个微型英语→pig-Latin 语料库（200 对）上微调 `flan-t5-small`。在留出的 50 对上测量 BLEU。与在相同数据和相同计算量上微调 `Llama-3.2-1B` 比较。

## 术语速查表

| 术语 | 人们的说法 | 实际含义 |
|------|-----------|---------|
| 编码器-解码器 | "Seq2seq Transformer" | 两个堆叠：用于输入的双向编码器，带交叉注意力的因果解码器用于输出。 |
| 交叉注意力 | "源与目标对话的地方" | 解码器的 Q × 编码器的 K/V。编码器信息进入解码器的唯一地方。 |
| 片段破坏 | "T5 的预训练技巧" | 用哨兵 token 替换随机片段；解码器输出这些片段。 |
| 去噪目标 | "BART 的游戏" | 对输入应用噪声函数，训练解码器重建干净序列。 |
| 哨兵 token | "`<extra_id_N>` 占位符" | 在源中标记被破坏片段并在目标中重新标记的特殊 token。 |
| Flan | "指令微调的 T5" | 在 1,800+ 任务上微调的 T5；使编码器-解码器在指令遵循上具有竞争力。 |
| 束搜索 | "解码策略" | 每步保留 top-k 部分序列；翻译/摘要的标准。 |
| Teacher forcing | "训练时输入" | 训练时，将真实的前一个输出 token 输入给解码器，而非采样的。 |

## 延伸阅读

- [Raffel 等人（2019）。Exploring the Limits of Transfer Learning with a Unified Text-to-Text Transformer](https://arxiv.org/abs/1910.10683) —— T5。
- [Lewis 等人（2019）。BART: Denoising Sequence-to-Sequence Pre-training for Natural Language Generation, Translation, and Comprehension](https://arxiv.org/abs/1910.13461) —— BART。
- [Chung 等人（2022）。Scaling Instruction-Finetuned Language Models](https://arxiv.org/abs/2210.11416) —— Flan-T5。
- [Radford 等人（2022）。Robust Speech Recognition via Large-Scale Weak Supervision](https://arxiv.org/abs/2212.04356) —— Whisper，2026 年规范的编码器-解码器。
- [HuggingFace `modeling_t5.py`](https://github.com/huggingface/transformers/blob/main/src/transformers/models/t5/modeling_t5.py) —— 参考实现。
