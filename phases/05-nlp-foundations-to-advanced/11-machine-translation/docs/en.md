# Machine Translation | 机器翻译

> Translation is the task that paid for NLP research for thirty years and keeps paying now.
> 翻译是为 NLP 研究买单三十年的任务，现在仍在继续。

> **【中文解读】** 从统计机器翻译到神经机器翻译。现代用 Transformer。

**Type:** Build | **类型:** 动手
**Languages:** Python | **语言:** Python
**Prerequisites:** Phase 5 · 10 (Attention Mechanism), Phase 5 · 04 (GloVe, FastText, Subword) | **前置知识:** Phase 5 · 10 (Attention Mechanism), Phase 5 · 04 (GloVe, FastText, Subword)
**Time:** ~75 minutes | **时间:** ~75 minutes


## The Problem | 问题引入

A model reads a sentence in one language and produces a sentence in another. Length varies. Word order varies. Some source words map to multiple target words and vice versa. Idioms refuse one-to-one mapping. "I miss you" in French is "tu me manques" — literally "you are lacking to me." No word-level alignment survives that.
> 模型读取一种语言的句子并产生另一种语言的句子。长度不同。词序不同。一些源词映射到多个目标词，反之亦然。习语拒绝一对一映射。"I miss you" 的法语是 "tu me manques" —— 字面意思是 "你对我来说是缺失的"。没有词级对齐能经受住这个。

> **【中文解读】** 本节提出的问题是：如何在实际工程中正确理解和应用这一技术。理解问题背景有助于把握技术选型的关键决策点。在实际 AI 系统中，错误的技术选型往往比实现细节的 bug 代价更高。


Machine translation is the task that forced NLP to invent encoder-decoders, attention, transformers, and eventually the whole LLM paradigm. Every step forward arrived because translation quality was measurable and the gap between human and machine was stubborn.
> 机器翻译是迫使 NLP 发明编码器-解码器、注意力、Transformer 以及最终整个 LLM 范式的任务。每一步前进都是因为翻译质量可测量且人与机器之间的差距顽固。

This lesson skips the history lesson and teaches the working pipeline of 2026: pretrained multilingual encoder-decoder (NLLB-200 or mBART), subword tokenization, beam search, BLEU and chrF evaluation, and the handful of failure modes that still ship to production uncaught.
> 本课跳过历史课，教授 2026 年的工作流水线：预训练多语言编码器-解码器（NLLB-200 或 mBART）、子词分词、束搜索、BLEU 和 chrF 评估，以及少数仍会逃过检查进入生产的失败模式。

## The Concept | 核心概念

> **【中文解读】** 本节介绍核心概念和理论基础。掌握这些概念是后续动手实现的前提，同时也是面试和工程实践中高频考察的知识点。


![MT pipeline: tokenize → encode → decode with attention → detokenize](../assets/mt-pipeline.svg)
> ![MT 流水线：分词 → 编码 → 带注意力的解码 → 去分词](../assets/mt-pipeline.svg)

Modern MT is a transformer encoder-decoder trained on parallel text. The encoder reads the source in its language's tokenization. The decoder generates the target, one subword at a time, using the encoder's output via cross-attention (lesson 10). Decoding uses beam search to avoid the greedy-decoding trap. The output is detokenized, detruecased, and scored against a reference.
> 现代 MT 是在平行文本上训练的 Transformer 编码器-解码器。编码器以其语言的分词读取源语言。解码器通过交叉注意力（第 10 课）使用编码器的输出，每次生成一个子词的目标语言。解码使用束搜索避免贪心解码陷阱。输出经过去分词、去真实大小写处理，并与参考评分。

Three operational choices drive real-world MT quality.
> 三个运营选择驱动真实世界的 MT 质量。

- **Tokenizer.** SentencePiece BPE trained on a mixed-language corpus. Shared vocabulary across languages is what enables zero-shot pairs in NLLB.
- **Model size.** NLLB-200 distilled 600M fits on a laptop. NLLB-200 3.3B is the published production default. 54.5B is the research ceiling.
- **Decoding.** Beam width 4-5 for general content. Length penalty to avoid too-short output. Constrained decoding when you need terminology consistency.
> - **分词器。** 在混合语言语料上训练的 SentencePiece BPE。跨语言共享词表是 NLLB 支持零样本语言对的关键。
- **模型大小。** NLLB-200 蒸馏 600M 适合笔记本。NLLB-200 3.3B 是已发表的生产默认。54.5B 是研究天花板。
- **解码。** 通用内容束宽度 4-5。长度惩罚避免输出过短。需要术语一致性时使用约束解码。

> **【中文解读】** 本节通过代码从零实现核心算法。这种 "from scratch" 的方式能帮助理解框架背后的原理，遇到问题时不会被黑盒困住。

> **【拓展：大语言模型的工程实践】** 从 GPT 到 ChatGPT，NLP 领域经历了从 "每个任务训练一个模型" 到 "一个模型解决所有任务" 的范式转变。在实际工程中，LLM 的部署需要考虑 Token 限制、延迟、成本、安全审查等问题。LangChain、LlamaIndex 等框架简化了 LLM 应用的开发。

> **【拓展：RAG 与企业知识库】** 检索增强生成（RAG）是当前企业 AI 应用最流行的架构：将用户查询先检索相关文档片段，再将检索结果作为上下文喂给 LLM 生成答案。这种方式解决了 LLM 知识过时和幻觉问题。向量数据库（如 Milvus、Pinecone、Weaviate）是 RAG 系统的核心组件。

> **【拓展：NLP 的多语言挑战】** 全球有 7000+ 种语言，但 NLP 研究主要集中在英语等少数语言。跨语言迁移学习、多语言预训练模型（如 mBERT、XLM-R）是解决低资源语言 NLP 的主要方法。字节级模型（如 ByT5）甚至可以在无分词器的情况下处理任何语言。


## Build It | 动手实现

### Step 1: a pretrained MT call
> 三件事很重要。`src_lang` 告诉分词器使用哪种文字和分割。`forced_bos_token_id` 告诉解码器生成哪种语言。两者都是 NLLB 特有的技巧；mBART 和 M2M-100 使用各自的约定，不可互换。

```python
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

model_id = "facebook/nllb-200-distilled-600M"
tok = AutoTokenizer.from_pretrained(model_id, src_lang="eng_Latn")
model = AutoModelForSeq2SeqLM.from_pretrained(model_id)

src = "The cats are running."
inputs = tok(src, return_tensors="pt")

out = model.generate(
    **inputs,
    forced_bos_token_id=tok.convert_tokens_to_ids("fra_Latn"),
    num_beams=5,
    length_penalty=1.0,
    max_new_tokens=64,
)
print(tok.batch_decode(out, skip_special_tokens=True)[0])
```

```text
Les chats courent.
```

Three things matter here. `src_lang` tells the tokenizer which script and segmentation to apply. `forced_bos_token_id` tells the decoder which language to generate. Both are NLLB-specific tricks; mBART and M2M-100 use their own conventions and they are not interchangeable.
> BLEU 测量输出与参考之间的 n-gram 重叠。四种参考 n-gram 大小（1-4），精确率的几何平均，对过短输出的简洁惩罚。分数在 [0, 100]。常用但难以解读：30 BLEU 是 "可用"；40 是 "好"；50 是 "出色"；1 BLEU 以内的差异是噪声。

### Step 2: BLEU and chrF
> chrF 测量字符级 F 分数。对 BLEU 低估匹配的形态丰富语言更敏感。通常与 BLEU 一起报告。

BLEU measures n-gram overlap between output and reference. Four reference n-gram sizes (1-4), geometric mean of precisions, brevity penalty for too-short output. The score is in [0, 100]. Commonly used. Frustrating to interpret: 30 BLEU is "usable"; 40 is "good"; 50 is "exceptional"; differences under 1 BLEU are noise.
> 始终使用 `sacrebleu`。它归一化分词使分数跨论文可比。自己实现 BLEU 是产生误导基准的方式。

chrF measures character-level F-score. More sensitive to morphologically rich languages where BLEU undercounts matches. Often reported alongside BLEU.
> 现代 MT 评估使用三个互补的指标族。至少用两个发布。

```python
import sacrebleu

hypotheses = ["Les chats courent."]
references = [["Les chats courent."]]

bleu = sacrebleu.corpus_bleu(hypotheses, references)
chrf = sacrebleu.corpus_chrf(hypotheses, references)
print(f"BLEU: {bleu.score:.1f}  chrF: {chrf.score:.1f}")
```

Always use `sacrebleu`. It normalizes tokenization so scores are comparable across papers. Rolling your own BLEU computation is how misleading benchmarks happen.
> - **启发式**（BLEU、chrF）。快速、基于参考、可解释、对释义不敏感。用于遗留比较和回归检测。
- **学习型**（COMET、BLEURT、BERTScore）。在人类判断上训练的神经模型；比较翻译与源和参考的语义相似性。COMET 自 2023 年以来与 MT 研究关联最高，是 2026 年质量重要的生产默认选择。
- **LLM 评委**（无参考）。提示大模型在流畅性、充分性、语调和文化适当性上为翻译打分。GPT-4 评委在评分标准设计良好时与人类一致性约 80%。用于不存在参考的开放内容。

### The three-tier evaluation hierarchy (2026)
> 2026 年实用技术栈：`sacrebleu` 用于 BLEU 和 chrF，`unbabel-comet` 用于 COMET，提示 LLM 用于最终面向人类的信号。在信任生产数据之前，针对 50-100 个人类标注样本校准每个指标。

Modern MT evaluation uses three complementary metric families. Ship with at least two.
> 无参考指标（COMET-QE、BLEURT-QE、LLM 评委）让你在没有参考的情况下评估翻译，这对不存在参考翻译的长尾语言对很重要。

- **Heuristic** (BLEU, chrF). Fast, reference-based, interpretable, insensitive to paraphrase. Use for legacy comparison and regression detection.
- **Learned** (COMET, BLEURT, BERTScore). Neural models trained on human judgment; compare semantic similarity of translation to source and reference. COMET has the highest association with MT research since 2023 and is the 2026 production default where quality matters.
- **LLM-as-judge** (reference-free). Prompt a large model to score translations on fluency, adequacy, tone, cultural appropriateness. GPT-4-as-judge matches human agreement ~80% of the time when the rubric is well designed. Use for open-ended content where no reference exists.
> 上面的工作流水线 80% 的时间能流畅翻译，剩下 20% 会静默失败。已命名的失败模式：

Practical 2026 stack: `sacrebleu` for BLEU and chrF, `unbabel-comet` for COMET, and a prompted LLM for the final human-facing signal. Calibrate every metric against 50-100 human-labeled examples before trusting it on production data.
> - **幻觉。** 模型发明源中没有的内容。在不熟悉的领域词汇中常见。症状：输出流畅但声称源没有陈述的事实。缓解：对领域术语的约束解码，对受监管内容的人工审查，监控输出比输入长得多的异常。
- **偏离目标语言生成。** 模型翻译成错误的语言。NLLB 在罕见语言对上出奇地容易出错。缓解：验证 `forced_bos_token_id` 并始终用语言识别模型检查输出。
- **术语漂移。** "Sign up" 在文档 1 中变成 "s'inscrire"，在文档 2 中变成 "créer un compte"。对于 UI 文本和面向用户的字符串，一致性比原始质量更重要。缓解：词汇表约束解码或后编辑字典。
- **语体不匹配。** 法语 "tu" vs "vous"，日语敬语级别。模型选择训练中更常见的形式。对于面向客户的内容，这通常是错误的。缓解：如果模型支持，用语体 token 作为提示前缀，或在仅正式语料上微调小模型。
- **短输入长度爆炸。** 非常短的输入句子经常产生过长的翻译，因为长度惩罚在约 5 个源 token 以下急剧下降。缓解：与源长度成比例的硬最大长度上限。

Reference-free metrics (COMET-QE, BLEURT-QE, LLM-as-judge) let you evaluate translations without a reference, which matters for long-tail language pairs where reference translations do not exist.
> 预训练模型是通才。法律、医疗或游戏对话翻译从领域平行数据的微调中可测量地受益。方案并不复杂：

### Step 3: what breaks in production
> 几千个高质量平行样本胜过几十万个噪声网络抓取样本。训练数据的质量是最大的生产杠杆。

The working pipeline above will translate fluently 80% of the time and silently fail the remaining 20%. Named failure modes:

- **Hallucination.** Model invents content that was not in the source. Common in unfamiliar domain vocabulary. Symptom: output is fluent but claims facts the source did not state. Mitigation: constrained decoding on domain terms, human review on regulated content, monitoring for output much longer than input.
- **Off-target generation.** Model translates into the wrong language. NLLB is surprisingly prone to this on rare language pairs. Mitigation: verify `forced_bos_token_id` and always decode with a language-ID model check on output.
- **Terminology drift.** "Sign up" becomes "s'inscrire" in doc 1 and "créer un compte" in doc 2. For UI text and user-facing strings, consistency matters more than raw quality. Mitigation: glossary-constrained decoding or post-edit dictionary.
- **Formality mismatch.** French "tu" vs "vous", Japanese politeness levels. The model picks whichever form was more common in training. For customer-facing content this is usually wrong. Mitigation: prompt prefix with a formality token if the model supports it, or fine-tune a small model on formal-only corpora.
- **Length explosion on short input.** Very short input sentences often produce overlong translations because the length penalty falls off a cliff below ~5 source tokens. Mitigation: hard max-length cap proportional to source length.

### Step 4: fine-tuning for a domain

Pretrained models are generalists. Legal, medical, or game-dialog translation benefits measurably from fine-tuning on domain parallel data. The recipe is not exotic:

```python
from transformers import Trainer, TrainingArguments
from datasets import Dataset

pairs = [
    {"src": "The defendant pleaded guilty.", "tgt": "L'accusé a plaidé coupable."},
]

ds = Dataset.from_list(pairs)


def preprocess(ex):
    return tok(
        ex["src"],
        text_target=ex["tgt"],
        truncation=True,
        max_length=128,
        padding="max_length",
    )


ds = ds.map(preprocess, remove_columns=["src", "tgt"])

args = TrainingArguments(output_dir="out", per_device_train_batch_size=4, num_train_epochs=3, learning_rate=3e-5)
Trainer(model=model, args=args, train_dataset=ds).train()
```

> **【中文解读】** 本节展示如何用成熟框架（如 PyTorch、HuggingFace 等）快速应用该技术。在实际项目中，优先使用经过验证的框架实现，可以减少 bug 并提高开发效率。


A few thousand high-quality parallel examples beats a few hundred thousand noisy web-scraped ones. Quality of training data is the single largest production lever.


> **【拓展：Prompt Engineering 与 LLM 应用】** Prompt Engineering 已成为 NLP 工程师的核心技能。从 Zero-shot 到 Few-shot，从 Chain-of-Thought 到 ReAct，不同的提示策略适用于不同场景。在实际项目中，系统提示（System Prompt）的设计直接影响 LLM 应用的稳定性和输出质量。

## Use It | 用框架实现

The 2026 production stack for MT:
> 2026 年的 MT 生产技术栈：

| Use case | Recommended starting point |
|---------|---------------------------|
| Any-to-any, 200 languages | `facebook/nllb-200-distilled-600M` (laptop) or `nllb-200-3.3B` (production) |
| English-centric, high quality, 50 languages | `facebook/mbart-large-50-many-to-many-mmt` |
| Short runs, cheap inference, English-French/German/Spanish | Helsinki-NLP / Marian models |
| Latency-critical browser-side | ONNX-quantized Marian (~50 MB) |
| Maximum quality, willing to pay | GPT-4 / Claude / Gemini with translation prompts |
> | 使用场景 | 推荐起点 |
|---------|---------|
| 任意到任意，200 种语言 | `facebook/nllb-200-distilled-600M`（笔记本）或 `nllb-200-3.3B`（生产） |
| 以英语为中心，高质量，50 种语言 | `facebook/mbart-large-50-many-to-many-mmt` |
| 短任务，廉价推理，英语-法语/德语/西班牙语 | Helsinki-NLP / Marian 模型 |
| 延迟敏感的浏览器端 | ONNX 量化的 Marian（约 50 MB） |
| 最高质量，愿意付费 | GPT-4 / Claude / Gemini 配合翻译提示 |

LLMs now outperform specialized MT models on several language pairs as of 2026, particularly on idiomatic content and long context. The tradeoff is per-token cost and latency. Pick an LLM when context length, stylistic consistency, or domain adaptation via prompting matters more than throughput.
> 截至 2026 年，LLM 在多种语言对上已超越专门的 MT 模型，特别是在习语内容和长上下文上。代价是每 token 成本和延迟。当上下文长度、风格一致性或通过提示进行领域适配比吞吐量更重要时，选择 LLM。

> **【中文解读】** 本节关注如何将模型部署为可用的产品。从原型到生产级系统需要考虑性能优化、错误处理、监控等多个维度。


## Ship It | 产出物

Save as `outputs/skill-mt-evaluator.md`:
> 保存为 `outputs/skill-mt-evaluator.md`：

```markdown
---
name: mt-evaluator
description: Evaluate a machine translation output for shipping.
version: 1.0.0
phase: 5
lesson: 11
tags: [nlp, translation, evaluation]
---

Given a source text and a candidate translation, output:

1. Automatic score estimate. BLEU and chrF ranges you would expect. State whether a reference is available.
2. Five-point human-verifiable check list: (a) content preservation (no hallucinations), (b) correct language, (c) register / formality match, (d) terminology consistency with glossary if provided, (e) no truncation or length explosion.
3. One domain-specific issue to probe. E.g., for legal: named entities and statute citations. For medical: drug names and dosages. For UI: placeholder variables `{name}`.
4. Confidence flag. "Ship" / "Ship with review" / "Do not ship". Tie to the severity of issues found in step 2.

> **【中文解读】** 练习题按照 Easy/Medium/Hard 三个难度递进。建议至少完成 Medium 级别的题目，Hard 级别适合深入研究或面试准备。


Refuse to ship a translation without a language-ID check on output. Refuse to evaluate without a reference unless the user explicitly opts in to reference-free scoring (COMET-QE, BLEURT-QE). Flag any content over 1000 tokens as likely needing chunked translation.
```

## Exercises | 练习题

1. **Easy.** Translate a 5-sentence English paragraph to French and back to English using `nllb-200-distilled-600M`. Measure how close the round-trip is to the original. You should see semantic preservation with word-choice drift.
2. **Medium.** Implement a language-ID check on translation outputs using `fasttext lid.176` or `langdetect`. Integrate into the MT call so off-target generations are caught before returning.
3. **Hard.** Fine-tune `nllb-200-distilled-600M` on a 5,000-pair domain corpus of your choice. Measure BLEU on a held-out set before and after fine-tuning. Report which kinds of sentences improved and which regressed.
> 1. **简单。** 使用 `nllb-200-distilled-600M` 将 5 句英语段落翻译成法语再翻回英语。测量往返与原文的接近程度。你应该看到语义保留但用词漂移。
2. **中等。** 使用 `fasttext lid.176` 或 `langdetect` 实现翻译输出的语言识别检查。集成到 MT 调用中，在返回前捕获偏离目标语言的生成。
3. **困难。** 在你选择的 5000 对领域语料上微调 `nllb-200-distilled-600M`。测量微调前后在留出集上的 BLEU。报告哪些类型的句子改进了，哪些退步了。

> **【中文解读】** 术语表中的 "What people say" vs "What it actually means" 区分了日常口语和精确技术含义。在团队协作中，统一术语定义可以避免大量沟通误解。


## Key Terms | 术语速查表

| Term | What people say | What it actually means |
|------|-----------------|-----------------------|
| BLEU | Translation score | N-gram precision with brevity penalty. [0, 100]. |
| chrF | Character F-score | Character-level F-score. More sensitive for morphologically rich languages. |
| NMT | Neural MT | Transformer encoder-decoder trained on parallel text. The 2017+ default. |
| NLLB | No Language Left Behind | Meta's 200-language MT model family. |
| Constrained decoding | Controlled output | Force specific tokens or n-grams to appear / not appear in the output. |
| Hallucination | Invented content | Model output that is not supported by the source. |
> | 术语 | 人们常说的 | 实际含义 |
|------|-----------|---------|
| BLEU | 翻译分数 | 带简洁惩罚的 n-gram 精确率。[0, 100]。 |
| chrF | 字符 F 分数 | 字符级 F 分数。对形态丰富语言更敏感。 |
| NMT | 神经机器翻译 | 在平行文本上训练的 Transformer 编码器-解码器。2017+ 的默认。 |
| NLLB | No Language Left Behind | Meta 的 200 语言 MT 模型系列。 |
| 约束解码 | 控制输出 | 强制特定 token 或 n-gram 出现/不出现在输出中。 |
| 幻觉 | 发明内容 | 模型输出中不被源支持的内容。 |

> **【中文解读】** 延伸阅读提供了深入学习的高质量资源。这些论文和教程是该领域的经典参考文献，适合需要深入理解的读者。


## Further Reading | 延伸阅读

- [Costa-jussà et al. (2022). No Language Left Behind: Scaling Human-Centered Machine Translation](https://arxiv.org/abs/2207.04672) — the NLLB paper.
- [Post (2018). A Call for Clarity in Reporting BLEU Scores](https://aclanthology.org/W18-6319/) — why `sacrebleu` is the only correct way to report BLEU.
- [Popović (2015). chrF: character n-gram F-score for automatic MT evaluation](https://aclanthology.org/W15-3049/) — the chrF paper.
- [Hugging Face MT guide](https://huggingface.co/docs/transformers/tasks/translation) — practical fine-tuning walkthrough.
> - [Costa-jussà et al. (2022). No Language Left Behind: Scaling Human-Centered Machine Translation](https://arxiv.org/abs/2207.04672) — NLLB 论文。
- [Post (2018). A Call for Clarity in Reporting BLEU Scores](https://aclanthology.org/W18-6319/) — 为什么 `sacrebleu` 是报告 BLEU 的唯一正确方式。
- [Popović (2015). chrF: character n-gram F-score for automatic MT evaluation](https://aclanthology.org/W15-3049/) — chrF 论文。
- [Hugging Face MT guide](https://huggingface.co/docs/transformers/tasks/translation) — 实用微调演练。
