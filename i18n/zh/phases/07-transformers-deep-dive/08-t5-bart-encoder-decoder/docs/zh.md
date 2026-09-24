# 编码器解码器模型

> 编码器理解.编码器生成.把它们重新组合起来,你就能为输入 →输出任务构建模型:翻译,总结,重写,转录.

> **【中文解读】**把所有NLP任务统一为文本到文本格式.

**Type:** Study | **类型:** 学习
**Language:**子**语言:**字符串
**Prerequisites:** Phase 7 · 05 (Full Transformer), Phase 7 · 06 (BERT), Phase 7 · 07 (GPT) | **前置知识:** Phase 7 · 05 (Full Transformer), Phase 7 · 06 (BERT), Phase 7 · 07 (GPT)
**Time:** ~45 minutes | **时间:** ~45 分钟

## 问题 问题引入

只有解码器的GPT和只有编码器的BERT每个都为不同的目标而沿着2017年的架构.

> 解码器专用GPT 和编码器专用BERT各为不同目标精简了2017年的架构――但许多任务是天然的输入输出形式:

- 翻译:英语 → 法语.
  中文翻译:翻译:英语 → 法语。
- 总结:5000个标记文章 →200个标记总结.
  中文翻译:摘要:5000个代币 文章 →200个代币 摘要.
- 语音识别:音频代码 →文字代码.
  中文翻译:语音识别:音频代币 → 文本代币。
- 结构化提取:散文 → JSON.
  中文翻译:结构化提取:散文 → JSON。

编码器生成出口,在每一步都会交叉地关注该表示.训练在输出侧进行一个接一个.与GPT相同的损失,只是根据编码器输出条件.

> 对于这些任务,编码器-解码器是最合适的选择.编码器生成源的密集表示.解码器生成输出,在每一步通过交叉注意力访问该表示.

现代游戏书的定义是两篇论文:

> 两篇论文定义了现代范式:

1. **T5**"文本转移变换器".每一个NLP任务都被重构为文本输入,文本输出.单个架构,单个词汇库,单个损失.预训练在面具跨度预测 (输入中的腐败跨度,输出中解码它们).
   翻译: 中文**T5**(Raffel 等人,2019) ――"文本到文本迁移变压器"――每个NLP任务都被重新定义为文本输入文本输出――单一架构、单一词表、单一损失――用掩码片段预测进行预训练(破坏输入中的片段,在输出中解码它们) ――
2. **BART**"双向和自动回归变压器". 否认自动编码器:通过多种方式 (混动,掩盖,删除,旋转) 破坏输入,请解码器重建原始.
   翻译: 中文**BART**转换器:用多种方式破坏输入,要求解码器重建原始文本.

在2026年,编码器-解码器格式将继续存在输入结构的重要位置:

> 在2026年,编码器解码器格式在输入结构中继续存在:

- 语 (语音 →文字).
  中文翻译:语音 → 文本) 』
- 谷歌的翻译堆.
  中文翻译:谷歌的翻译系统.
- 一些代码完成/修复模型具有不同的文本和编辑结构.
  中文翻译:一些有明确的下文编辑结构的代码补全/修复模型──
- 结构性推理任务的Flan-T5和变体.
  中文翻译:Flan-T5 及其变体,用于结构化推理任务.

只有解码器赢得了关注点,但解码器从来没有消失.

> 解码器专用模型赢得聚光灯,但编码器-解码器从来没有消失.

> **【中文解读】**编码器-解码器架构在"输入→输出"结构化任务中仍然有优势――T5将所有NLP任务统一为文本到文本格式,BART使用去噪音自编码训练――虽然在纯文本生成领域仅被除了编码器,但在语音识别(语) 、翻译、摘要等任务中仍然是最佳选择――

## 概念的核心概念

![Encoder-decoder with cross-attention](../assets/encoder-decoder.svg)

### 进而循环

```
source tokens ─▶ encoder ─▶ (N_src, d_model)  ──┐
                                                 │
target tokens ─▶ decoder block                   │
                 ├─▶ masked self-attention       │
                 ├─▶ cross-attention ◀───────────┘
                 └─▶ FFN
                ↓
              next-token logits
```

重要的是,编码器每输入一次运行.解码器运行自动降低式,但在每一步都会交叉处理 *相同*编码器输出.缓存编码器输出是长输入的免费加快.

> 关键是,编码器对每个输入只运行一次.解码器自归运行,但在每一步都交叉关注*相同*编码器输出.缓存编码器输出对长输入是免费的加速.

> **【中文解读】**交叉注意力是编码器-解码器架构的信息桥梁:Q 来自解码器,K/V 来自编码器输出――编码器只运行一次 (高效),解码器每步都通过交叉注意力访问编码器的完整输出――

> **【拓展：Whisper 的编码器-解码器设计】**开放AI的语音识别模型使用编码器-解码器架构,因为音频 (音频) 和文本是完全不同的模态――编码器处理音频特征,解码器生成文本――这种设计让Whisper能处理多语言语音识别和翻译任务,是2026年语音领域的现实标准――

###        

选择输入的随机跨度 (平均长度3个代币,总数为15%). 替换每个跨度一个独特的哨兵:`<extra_id_0>`现在`<extra_id_1>`解码器只输出了被破坏的跨度,

> 随机选择输入中的片段(平均长度3个标志,总计15%) ⋅用唯一的哨兵标记替换每个片段:`<extra_id_0>`,我知道.`<extra_id_1>`等──解码器只输出被破坏的片段及其哨兵前:

```
source: The quick <extra_id_0> fox jumps <extra_id_1> dog
target: <extra_id_0> brown <extra_id_1> over the lazy
```

具有竞争力,与MLM (BERT) 和前LM (UniLM) 在T5纸的缩.

> 在T5论文的消融实验中,与LM (BERT) 和前LM (UniLM) 的竞争力相当.

### 多噪音排斥

音系统试验了五种噪音功能:

> 试试五种噪音函数:

1. 标志掩盖.
   中文翻译:托肯 掩码――
2. 删除代码.
   中文翻译:Token 删除──
3. 填写文字 (掩盖一个跨度,解码器插入了正确的长度).
   中文翻译:文本填充(掩码一个片段,解码器插入正确长度) 』
4. 换句话变化.
   中文翻译:句子排列──
5. 文件转换.
   中文翻译:文档旋转.

结合文本填写+句子变换产生了最佳下游数字.解码器总是重建原始.BART的输出是完整的序列,而不仅仅是损坏的跨度,因此预训计算高于T5.

> 组合文本填充 + 句子排列产生了最佳下游效果――解码器总是重建原始文本――BART的输出是完整序列,而不仅仅是被破坏的段片因此预训计算量高于T5――

> **【中文解读】**预训策略不同:T5的跨度腐败只预测被破坏的片段(高效),BART的去噪音自编码重建整个序列(更彻底但更贵) ――选择取决于任务T5更适合抽象任务,BART更适合抽象任务――

### 推理

采用GPT的相同的自动降低性生成. 贪/束/顶部采样应用.束搜索 (45) 是翻译和总结的标准,因为输出分布比聊天更窄.

> 推理与GPT的自归生成相同──贪心/束搜索/top-p采样都适用──束搜索(宽度 4-5) 是翻译和摘要的标准策略,因为输出分布比对话更窄──

> **【拓展：Beam Search 在翻译中的重要性】**编码器-解码器模型在翻译和摘要任务中常用光束搜索 (宽度 4-5),因为输出分布较窄.

### 2026年,每种变体何时选择

| Task | Encoder-decoder? | Why |
|------|------------------|-----|
| 任务 | 是否用编码器-解码器？ | 原因 |
| Translation | Yes, usually | Clear source sequence; fixed output distribution; beam search works |
| 翻译 | 通常是 | 明确的源序列；固定的输出分布；束搜索有效 |
| Speech-to-text | Yes (Whisper) | Input modality differs from output; encoder shapes audio features |
| 语音转文本 | 是（Whisper） | 输入模态与输出不同；编码器处理音频特征 |
| Chat / reasoning | No, decoder-only | No persistent "input" — the conversation is the sequence |
| 对话/推理 | 否，解码器专用 | 没有持久的"输入"——对话本身就是序列 |
| Code completion | Usually no | Decoder-only with long context wins; code models like Qwen 2.5 Coder are decoder-only |
| 代码补全 | 通常否 | 带长上下文的解码器专用胜出；Qwen 2.5 Coder 等代码模型是解码器专用 |
| Summarization | Either works | BART, PEGASUS beat earlier decoder-only baselines; modern decoder-only LLMs match them |
| 摘要 | 都可以 | BART、PEGASUS 超越早期解码器专用基线；现代解码器专用 LLM 能匹配它们 |
| Structured extraction | Either | T5 is clean because "text → text" absorbs any output format |
| 结构化提取 | 都可以 | T5 很干净，因为"文本 → 文本"可以吸收任何输出格式 |

自2022年以来的趋势:仅解码器接管了以前拥有的任务,因为 (a) 通过提示将指示调节的仅解码器LLM将其通用到任何东西, (b) 一个架构比两种更容易, (c) RLHF假设一个解码器. 编码器-解码器在输入方式不同的地方 (演讲,图像) 或光束搜索质量在哪里有意义.

> 自2022年以来,解码器专用接管了编码器-解码器曾经拥有的任务,因为 (a) 指令微调的解码器专用 LLM 通过提示可以泛化为任何任务, (b) 单一架构比两个更容易扩展, (c) RLHF 假设使用解码器.

> **【拓展：T5 的 text-to-text 统一范式】**翻译:"翻译英语为法语:Hello → Bonjour";分类:"感觉:这部电影很棒 →积极"――这种统一简化了架构和训练流程,也后来指示调整和快速工程的思想源头――Flan-T5 更是通过指示微调大幅提升了零样本能力――

## 建立它,实现它.
```figure
encoder-decoder
```

## 建立它

看到`code/main.py`我们将T5式的跨度腐败用于玩具体,这是这个课程中最有用的单一部分,因为它显示在每一个编码器-解码器预训练配方.

> 参见`code/main.py`                                                                                                                                                                                                                                                              

### 步骤1:跨度腐败

```python
def corrupt_spans(tokens, mask_rate=0.15, mean_span=3.0, rng=None):
    """Pick spans summing to ~mask_rate of tokens. Return (corrupted_input, target)."""
    n = len(tokens)
    n_mask = max(1, int(n * mask_rate))
    n_spans = max(1, int(round(n_mask / mean_span)))
    ...
```

目标格式是T5公约: `<sent0> span0 <sent1> span1 ...`损坏的输入将未变的代币与守望器代币交换到跨度位置.

> 目标格式遵循T5 约定:`<sent0> span0 <sent1> span1 ...`△被破坏的输入将未改变的标志与片段位置的哨兵标志交换排列──

### 步骤2:检查回路

鉴于被破坏的输入和目标,重建原始句子.如果你的腐败是可逆的,前进通过是很清楚的.这是一个智力检查真正的训练从来没有这样做,但测试是便宜的,并捕获你的跨度账本中的一个-一个错误.

> 给定被破坏的输入和目标,重建原始句子. 如果破坏是可逆的,前向传播就是很好的定义.

### 步骤3:BART噪音

五个功能:`token_mask`现在`token_delete`现在`text_infill`现在`sentence_permute`现在`document_rotate`两种组合,然后显示结果.

> 五个函数:`token_mask`,我知道.`token_delete`,我知道.`text_infill`,我知道.`sentence_permute`,我知道.`document_rotate`组合其中两个并显示结果.

## 用它实现框架

抱脸的参考:

> 抱脸 参考:

```python
from transformers import T5ForConditionalGeneration, T5Tokenizer
tok = T5Tokenizer.from_pretrained("google/flan-t5-base")
model = T5ForConditionalGeneration.from_pretrained("google/flan-t5-base")

inputs = tok("translate English to French: Attention is all you need.", return_tensors="pt")
out = model.generate(**inputs, max_new_tokens=32)
print(tok.decode(out[0], skip_special_tokens=True))
```

任务名称进入输入文本.同样的模型处理数十项任务,因为每个任务都是输入和输出. 2026年,该模式已被指令调节的单独解码器模型普遍化,但T5先编码了它.

> 技术:任务名称写在输入文本中. 一个模型可以处理数十种任务,因为每个任务都是文本输入文本输出. 在2026年,这种模式已经被指令微调的解码器专用模型泛化,但T5是最早规范化的.

## 运送它.

看到`outputs/skill-seq2seq-picker.md`技能选择编码器-解码器和解码器-仅用于新任务,因为输入输出结构,延迟和质量目标.

> 参见`outputs/skill-seq2seq-picker.md`△根据输出输出结构、延迟和质量目标,为新任务选择编码器-解码器或解码器专用架构──

## 练习题

1. **Easy.**跑步`code/main.py`检查是否将非传密源代币与解码目标代码连接,复制原始.
   中文翻译:运行 `code/main.py`对于一个30个代币的句子应用片段破坏,验证将非哨兵源代币与解码的目标片段拼写可以恢复原始文本.
2. **Medium.**实施BART的方案`text_infill`噪音:用单个取代随机度`<mask>`解码器必须推断正确的跨度长度加上内容.
   中文翻译:实现BART 的`text_infill`噪音:用单个`<mask>`代码器必须推断正确的片段长度和内容.
3. **Hard.**精细调节`flan-t5-small`在一个微小的英语 →猪拉丁体 (200对). 测量蓝色在一个持久的50对的集. 进行比较与细调`Llama-3.2-1B`根据相同的数据,使用相同的计算.
   中文翻译:在小型英语 →猪拉丁语料库(200对) 上微调 `flan-t5-small`△在留下的50对测试集中的测量 BLEU 分数――与在相同数据,相同的计算量微调`Llama-3.2-1B`对于比较.

## 关键词 快速查找表

| Term | What people say | What it actually means |
|------|-----------------|-----------------------|
| 术语 | 通俗说法 | 实际含义 |
| Encoder-decoder | "Seq2seq transformer" | Two stacks: bidirectional encoder for input, causal decoder with cross-attention for output. |
| 编码器-解码器 | "Seq2seq Transformer" | 两个堆栈：双向编码器处理输入，带交叉注意力的因果解码器生成输出。 |
| Cross-attention | "Where source talks to target" | Decoder's Q × encoder's K/V. The only place encoder information enters the decoder. |
| 交叉注意力 | "源与目标对话的地方" | 解码器的 Q × 编码器的 K/V。编码器信息进入解码器的唯一通道。 |
| Span corruption | "T5's pretraining trick" | Replace random spans with sentinel tokens; decoder outputs the spans. |
| 片段破坏 | "T5 的预训练技巧" | 用哨兵 token 替换随机片段；解码器输出这些片段。 |
| Denoising objective | "BART's game" | Apply a noise function to the input, train the decoder to reconstruct the clean sequence. |
| 去噪目标 | "BART 的游戏" | 对输入应用噪声函数，训练解码器重建干净序列。 |
| Sentinel token | "The `<extra_id_N>` placeholder" | Special tokens that tag corrupted spans in the source and re-tag them in the target. |
| 哨兵 token | "`<extra_id_N>` 占位符" | 在源端标记被破坏片段、在目标端重新标记的特殊 token。 |
| Flan | "Instruction-tuned T5" | T5 fine-tuned on >1,800 tasks; made encoder-decoder competitive at instruction-following. |
| Flan | "指令微调的 T5" | 在 1,800+ 任务上微调的 T5；使编码器-解码器在指令遵循方面具有竞争力。 |
| Beam search | "Decoding strategy" | Keep top-k partial sequences at each step; standard for translation/summarization. |
| 束搜索 | "解码策略" | 每步保留得分最高的 k 个部分序列；翻译/摘要的标准策略。 |
| Teacher forcing | "Training-time input" | During training, feed the true previous output token to the decoder, not the sampled one. |
| Teacher forcing | "训练时输入" | 训练时向解码器输入真实的上一个输出 token，而非采样的 token。 |

## 继续阅读 继续阅读

- [Raffel et al. (2019). Exploring the Limits of Transfer Learning with a Unified Text-to-Text Transformer](https://arxiv.org/abs/1910.10683)T5
  中文翻译:T5 论文。
- [Lewis et al. (2019). BART: Denoising Sequence-to-Sequence Pre-training for Natural Language Generation, Translation, and Comprehension](https://arxiv.org/abs/1910.13461)  
  中文翻译:BART论文。
- [Chung et al. (2022). Scaling Instruction-Finetuned Language Models](https://arxiv.org/abs/2210.11416) 飞行器T5.
  中文翻译:Flan-T5 论文。
- [Radford et al. (2022). Robust Speech Recognition via Large-Scale Weak Supervision](https://arxiv.org/abs/2212.04356) 语,可谓的2026代码器-解码器.
  中文翻译:语论文,2026年典型编码器-解码器模型──
- [HuggingFace `modeling_t5.py`](https://github.com/huggingface/transformers/blob/main/src/transformers/models/t5/modeling_t5.py)参考实施.
  中文翻译:HuggingFace T5 参考实现──
