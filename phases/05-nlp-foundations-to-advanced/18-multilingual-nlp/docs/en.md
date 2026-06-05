# Multilingual NLP | 多语言 NLP

> One model, 100+ languages, zero training data for most of them. Cross-lingual transfer is the practical miracle of the 2020s.
> 一个模型，100+ 种语言，大多数语言零训练数据。跨语言迁移是 2020 年代的实用奇迹。

> **【中文解读】** 多语言 BERT、XLM-R 等模型处理多种语言。

**Type:** Learn | **类型:** 学习
**Languages:** Python | **语言:** Python
**Prerequisites:** Phase 5 · 04 (GloVe, FastText, Subword), Phase 5 · 11 (Machine Translation) | **前置知识:** Phase 5 · 04（GloVe、FastText、子词），Phase 5 · 11（机器翻译）
**Time:** ~45 minutes | **时间:** ~45 分钟

## The Problem | 问题引入

English has billions of labeled examples. Urdu has thousands. Maithili has almost none. Any practical NLP system that serves a global audience has to work on the long tail of languages where task-specific training data does not exist.

> 英语有数十亿标注样本。乌尔都语有数千。迈蒂利语几乎没有。任何服务全球用户的实用 NLP 系统都必须在特定任务训练数据不存在的长尾语言上工作。

> **【中文解读】** 本节提出的问题是：如何在实际工程中正确理解和应用这一技术。理解问题背景有助于把握技术选型的关键决策点。在实际 AI 系统中，错误的技术选型往往比实现细节的 bug 代价更高。

Multilingual models solve this by training one model on many languages simultaneously. The shared representation lets the model transfer skills learned in high-resource languages to low-resource ones. Fine-tune the model on English sentiment analysis, and it produces surprisingly good sentiment predictions on Urdu out of the box. That is zero-shot cross-lingual transfer, and it has reshaped how NLP ships to the world.

> 多语言模型通过同时在许多语言上训练一个模型来解决这个问题。共享表示让模型将高资源语言学到的技能迁移到低资源语言。在英语情感分析上微调模型，它开箱即可对乌尔都语产生令人惊讶的良好情感预测。这就是零样本跨语言迁移，它重塑了 NLP 面向世界的方式。

This lesson names the tradeoffs, the canonical models, and the one decision that trips up teams new to multilingual work: picking a source language for transfer.

> 本课命名了权衡、经典模型，以及困扰多语言工作新手团队的决策：选择迁移的源语言。

## The Concept | 核心概念

> **【中文解读】** 本节介绍核心概念和理论基础。掌握这些概念是后续动手实现的前提，同时也是面试和工程实践中高频考察的知识点。

![Cross-lingual transfer via shared multilingual embedding space](../assets/multilingual.svg)

**Shared vocabulary.** Multilingual models use a SentencePiece or WordPiece tokenizer trained on text from all target languages. The vocabulary is shared: the same subword unit represents the same morpheme across related languages. `anti-` in English and Italian gets the same token.

> **共享词表。** 多语言模型使用在所有目标语言文本上训练的 SentencePiece 或 WordPiece 分词器。词表是共享的：相同的子词单元在相关语言中表示相同的语素。英语和意大利语的 `anti-` 获得相同的 token。

**Shared representation.** A transformer pretrained on masked language modeling across many languages learns that semantically similar sentences in different languages produce similar hidden states. mBERT, XLM-R, and NLLB all exhibit this. Embeddings for "cat" in English cluster near "chat" in French and "gato" in Spanish, and so do full-sentence embeddings.

> **共享表示。** 在多种语言的掩码语言建模上预训练的 Transformer 学到不同语言中语义相似的句子产生相似的隐藏状态。mBERT、XLM-R 和 NLLB 都展示了这一点。英语 "cat" 的嵌入与法语的 "chat" 和西班牙语的 "gato" 聚集在一起，完整句子嵌入也是如此。

**Zero-shot transfer.** Fine-tune the model on labeled data in one language (usually English). At inference, run it on any other language the model supports. No target-language labels needed. Results are strong for typologically related languages and weaker for distant ones.

> **零样本迁移。** 在一种语言（通常是英语）的标注数据上微调模型。推理时，在模型支持的任何其他语言上运行。不需要目标语言标签。对类型学相关的语言结果强，对远距离语言较弱。

**Few-shot fine-tuning.** Add 100-500 labeled examples in the target language. Accuracy jumps to 95-98% of the English baseline on classification tasks. This is the single most cost-effective lever in multilingual NLP.

> **少样本微调。** 在目标语言中添加 100-500 个标注样本。在分类任务上准确率跳升到英语基线的 95-98%。这是多语言 NLP 中最具成本效益的杠杆。

> **【拓展：大语言模型的工程实践】** 从 GPT 到 ChatGPT，NLP 领域经历了从 "每个任务训练一个模型" 到 "一个模型解决所有任务" 的范式转变。在实际工程中，LLM 的部署需要考虑 Token 限制、延迟、成本、安全审查等问题。LangChain、LlamaIndex 等框架简化了 LLM 应用的开发。

> **【拓展：RAG 与企业知识库】** 检索增强生成（RAG）是当前企业 AI 应用最流行的架构：将用户查询先检索相关文档片段，再将检索结果作为上下文喂给 LLM 生成答案。这种方式解决了 LLM 知识过时和幻觉问题。向量数据库（如 Milvus、Pinecone、Weaviate）是 RAG 系统的核心组件。

> **【拓展：NLP 的多语言挑战】** 全球有 7000+ 种语言，但 NLP 研究主要集中在英语等少数语言。跨语言迁移学习、多语言预训练模型（如 mBERT、XLM-R）是解决低资源语言 NLP 的主要方法。字节级模型（如 ByT5）甚至可以在无分词器的情况下处理任何语言。

## The models | 模型

| Model / 模型 | Year / 年份 | Coverage / 覆盖 | Notes / 说明 |
|-------|------|----------|-------|
| mBERT | 2018 | 104 languages / 104 种语言 | Trained on Wikipedia. First practical multilingual LM. Weak on low-resource. / 在 Wikipedia 上训练。首个实用多语言 LM。低资源语言较弱。 |
| XLM-R | 2019 | 100 languages / 100 种语言 | Trained on CommonCrawl. Sets the cross-lingual baseline. / 在 CommonCrawl 上训练。设定跨语言基线。 |
| XLM-V | 2023 | 100 languages / 100 种语言 | XLM-R with 1M-token vocabulary. Better on low-resource. / XLM-R 配 1M token 词表。低资源更好。 |
| mT5 | 2020 | 101 languages / 101 种语言 | T5 architecture for multilingual generation. / T5 架构用于多语言生成。 |
| NLLB-200 | 2022 | 200 languages / 200 种语言 | Meta's translation model; includes 55 low-resource languages. / Meta 翻译模型；含 55 种低资源语言。 |
| BLOOM | 2022 | 46 languages + 13 programming / 46 种语言 + 13 种编程语言 | Open 176B LLM trained multilingually. / 开源 176B 多语言 LLM。 |
| Aya-23 | 2024 | 23 languages / 23 种语言 | Cohere's multilingual LLM. Strong on Arabic, Hindi, Swahili. / Cohere 多语言 LLM。阿拉伯语、印地语、斯瓦希里语强。 |

Pick by use case. Classification works well with XLM-R-base as the sane default. Generation tasks call for mT5 or NLLB depending on translation vs open generation. LLM-style work pairs with Aya-23 or Claude using explicit multilingual prompting.

> 按用例选择。分类任务以 XLM-R-base 作为合理默认。生成任务根据翻译 vs 开放生成选择 mT5 或 NLLB。LLM 风格工作配合 Aya-23 或 Claude 使用显式多语言提示。

## The source-language decision (2026 research) | 源语言决策（2026 研究）

Most teams default to English as the fine-tuning source. Recent research (2026) shows this is often wrong.

> 大多数团队默认以英语作为微调源。最新研究（2026）表明这通常是错的。

Language similarity predicts transfer quality better than raw corpus size. For Slavic targets, German or Russian often beat English. For Indic targets, Hindi often beats English. The **qWALS** similarity metric (2026, based on World Atlas of Language Structures features) quantifies this. **LANGRANK** (Lin et al., ACL 2019) is a separate, earlier method that ranks candidate source languages from a combination of linguistic similarity, corpus size, and genetic relatedness.

> 语言相似性比原始语料大小更好地预测迁移质量。对于斯拉夫语目标，德语或俄语通常胜过英语。对于印度语目标，印地语通常胜过英语。**qWALS** 相似性度量（2026）量化了这一点。**LANGRANK**（Lin 等，ACL 2019）从语言相似性、语料大小和遗传关系的组合中排名候选源语言。

Practical rule: if your target language has a typologically close high-resource relative, try fine-tuning on that one first, then compare to English fine-tune.

> 实用规则：如果你的目标语言有类型学上接近的高资源亲属，先尝试在那个语言上微调，然后与英语微调比较。

## Build It | 动手实现

> **【中文解读】** 本节通过代码从零实现核心算法。这种 "from scratch" 的方式能帮助理解框架背后的原理，遇到问题时不会被黑盒困住。

### Step 1: zero-shot cross-lingual classification

```python
from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch

tok = AutoTokenizer.from_pretrained("joeddav/xlm-roberta-large-xnli")
model = AutoModelForSequenceClassification.from_pretrained("joeddav/xlm-roberta-large-xnli")


def classify(text, candidate_labels, hypothesis_template="This text is about {}."):
    scores = {}
    for label in candidate_labels:
        hypothesis = hypothesis_template.format(label)
        inputs = tok(text, hypothesis, return_tensors="pt", truncation=True)
        with torch.no_grad():
            logits = model(**inputs).logits[0]
        entail_score = torch.softmax(logits, dim=-1)[2].item()
        scores[label] = entail_score
    return dict(sorted(scores.items(), key=lambda x: -x[1]))


print(classify("I love this product!", ["positive", "negative", "neutral"]))
print(classify("मुझे यह उत्पाद पसंद है!", ["positive", "negative", "neutral"]))
print(classify("J'adore ce produit !", ["positive", "negative", "neutral"]))
```

One model, three languages, same API. XLM-R trained on NLI data transfers well to classification via the entailment trick.

> 一个模型，三种语言，相同 API。在 NLI 数据上训练的 XLM-R 通过蕴含技巧很好地迁移到分类。

### Step 2: multilingual embedding space

```python
from sentence_transformers import SentenceTransformer
import numpy as np

model = SentenceTransformer("sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2")

pairs = [
    ("The cat is sleeping.", "Le chat dort."),
    ("The cat is sleeping.", "El gato está durmiendo."),
    ("The cat is sleeping.", "Die Katze schläft."),
    ("The cat is sleeping.", "The dog is barking."),
]

for eng, other in pairs:
    emb_eng = model.encode([eng], normalize_embeddings=True)[0]
    emb_other = model.encode([other], normalize_embeddings=True)[0]
    sim = float(np.dot(emb_eng, emb_other))
    print(f"  {eng!r} <-> {other!r}: cos={sim:.3f}")
```

Translations land close in embedding space. A different English sentence lands further. This is what makes cross-lingual retrieval, clustering, and similarity work.

> 翻译在嵌入空间中距离很近。不同的英语句子距离更远。这就是跨语言检索、聚类和相似度工作的基础。

### Step 3: few-shot fine-tuning strategy

```python
from transformers import TrainingArguments, Trainer
from datasets import Dataset


def few_shot_finetune(base_model, base_tokenizer, examples):
    ds = Dataset.from_list(examples)

    def tokenize_fn(ex):
        out = base_tokenizer(ex["text"], truncation=True, max_length=128)
        out["labels"] = ex["label"]
        return out

    ds = ds.map(tokenize_fn)
    args = TrainingArguments(
        output_dir="out",
        per_device_train_batch_size=8,
        num_train_epochs=5,
        learning_rate=2e-5,
        save_strategy="no",
    )
    trainer = Trainer(model=base_model, args=args, train_dataset=ds)
    trainer.train()
    return base_model
```

For 100-500 target-language examples, `num_train_epochs=5` and `learning_rate=2e-5` are the safe defaults. Higher learning rates cause the multilingual alignment to collapse and you get an English-only model.

> 对于 100-500 个目标语言样本，`num_train_epochs=5` 和 `learning_rate=2e-5` 是安全默认值。更高的学习率会导致多语言对齐崩塌，你得到一个仅限英语的模型。

> **【拓展：Prompt Engineering 与 LLM 应用】** Prompt Engineering 已成为 NLP 工程师的核心技能。从 Zero-shot 到 Few-shot，从 Chain-of-Thought 到 ReAct，不同的提示策略适用于不同场景。在实际项目中，系统提示（System Prompt）的设计直接影响 LLM 应用的稳定性和输出质量。

## Evaluation that actually works | 真正有效的评估

- **Per-language accuracy on held-out sets.** Not aggregated. The aggregate hides the long tail.
  **每种语言在留出集上的准确率。** 不要聚合。聚合会隐藏长尾。
- **Benchmark against monolingual baseline.** For languages with enough data, a monolingual model trained from scratch sometimes beats the multilingual one. Test.
  **与单语基线比较。** 对于有足够数据的语言，从头训练的单语模型有时胜过多语言模型。测试。
- **Entity-level tests.** Named entities in the target language. Multilingual models often have weak tokenization for scripts far from Latin.
  **实体级测试。** 目标语言中的命名实体。多语言模型对远离拉丁文的书写的分词通常较弱。
- **Cross-lingual consistency.** Same meaning in two languages should produce the same prediction. Measure the gap.
  **跨语言一致性。** 两种语言中相同含义应产生相同预测。测量差距。

> **【中文解读】** 本节展示如何用成熟框架（如 PyTorch、HuggingFace 等）快速应用该技术。在实际项目中，优先使用经过验证的框架实现，可以减少 bug 并提高开发效率。

## Use It | 用框架实现

The 2026 stack:

> 2026 年的技术栈：

| Task / 任务 | Recommended / 推荐 |
|-----|-------------|
| Classification, 100 languages / 分类，100 种语言 | XLM-R-base (~270M) fine-tuned / 微调 |
| Zero-shot text classification / 零样本文本分类 | `joeddav/xlm-roberta-large-xnli` |
| Multilingual sentence embeddings / 多语言句子嵌入 | `sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2` |
| Translation, 200 languages / 翻译，200 种语言 | `facebook/nllb-200-distilled-600M` |
| Generative multilingual / 生成式多语言 | Claude, GPT-4, Aya-23, mT5-XXL |
| Low-resource language NLP / 低资源语言 NLP | XLM-V or domain-specific fine-tune / XLM-V 或领域微调 |

Always budget for fine-tuning in the target language if performance matters. Zero-shot is a starting point, not a final answer.

> 如果性能重要，始终为目标语言的微调预留预算。零样本是起点，不是最终答案。

### The tokenization tax | 分词税

Multilingual models share one tokenizer across all their languages. That vocabulary is trained on a corpus dominated by English, French, Spanish, Chinese, German. For any language outside the dominant set, three taxes compound silently:

> 多语言模型在所有语言间共享一个分词器。该词表在以英语、法语、西班牙语、中文、德语为主导的语料上训练。对于主导集之外的任何语言，三种税在暗中复合：

- **Fertility tax.** Low-resource language text tokenizes into far more tokens per word than English. A Hindi sentence can need 3-5x the tokens of an equivalent English sentence.
  **繁殖税。** 低资源语言文本每个词分词成比英语多很多的 token。一个印地语句子可能需要等价英语句子 3-5 倍的 token。
- **Variant recovery tax.** Every typo, diacritic variant, Unicode normalization mismatch, or case variation becomes a cold-start unrelated sequence in embedding space.
  **变体恢复税。** 每个拼写错误、变音符号变体、Unicode 归一化不匹配或大小写变化都变成嵌入空间中的冷启动无关序列。
- **Capacity spillover tax.** Taxes 1 and 2 consume context positions, layer depth, and embedding dimensions. What remains for actual reasoning is systematically smaller.
  **容量溢出税。** 税 1 和 2 消耗上下文位置、层深度和嵌入维度。留给实际推理的系统性地更小。

The practical symptom: your model trains normally on Hindi, the loss curve looks right, eval perplexity looks reasonable, and production outputs are subtly wrong. **You cannot data-scale your way out of a broken tokenizer.**

> 实际症状：模型在印地语上训练正常，损失曲线正确，评估困惑度合理，但生产输出微妙地出错。**你无法通过数据扩展来修复损坏的分词器。**

Mitigations: pick a tokenizer with good coverage for your target language; verify tokenization fertility on held-out target text; use byte-level fallback for truly long-tail scripts.

> 缓解措施：选择对目标语言覆盖良好的分词器；在留出的目标文本上验证分词繁殖率；对真正的长尾书写使用字节级回退。

> **【中文解读】** 本节关注如何将模型部署为可用的产品。从原型到生产级系统需要考虑性能优化、错误处理、监控等多个维度。

## Ship It | 产出物

Save as `outputs/skill-multilingual-picker.md`:

> 保存为 `outputs/skill-multilingual-picker.md`：

```markdown
---
name: multilingual-picker
description: Pick source language, target model, and evaluation plan for a multilingual NLP task.
version: 1.0.0
phase: 5
lesson: 18
tags: [nlp, multilingual, cross-lingual]
---

Given requirements (target languages, task type, available labeled data per language), output:

1. Source language for fine-tuning. Default English; check LANGRANK or qWALS if target language has a typologically close high-resource language.
2. Base model. XLM-R (classification), mT5 (generation), NLLB (translation), Aya-23 (generative LLM).
3. Few-shot budget. Start with 100-500 target-language examples if available.
4. Evaluation plan. Per-language accuracy, cross-lingual consistency, entity-level F1 on non-Latin scripts.

Refuse to ship a multilingual model without per-language evaluation. Flag scripts with low tokenization coverage as needing byte-fallback.
```

> **【中文解读】** 练习题按照 Easy/Medium/Hard 三个难度递进。建议至少完成 Medium 级别的题目，Hard 级别适合深入研究或面试准备。

## Exercises | 练习题

1. **Easy.** Run the zero-shot classification pipeline on 10 sentences per language across English, French, Hindi, and Arabic. Report accuracy on each.
   **简单。** 在英语、法语、印地语和阿拉伯语上运行零样本分类流水线，每种语言 10 句。报告准确率。
2. **Medium.** Use `paraphrase-multilingual-MiniLM-L12-v2` to build a cross-lingual retriever over a small mixed-language corpus. Query in English, retrieve documents in any language. Measure recall@5.
   **中等。** 构建跨语言检索器。用英语查询，检索任何语言的文档。测量 recall@5。
3. **Hard.** Compare English-source and Hindi-source fine-tuning for a Hindi classification task. Report which source produces better Hindi accuracy. This is the LANGRANK thesis in miniature.
   **困难。** 比较英语源和印地语源微调对印地语分类任务的效果。报告哪个源产生更好的准确率。这是 LANGRANK 论文的缩影。

> **【中文解读】** 术语表中的 "What people say" vs "What it actually means" 区分了日常口语和精确技术含义。在团队协作中，统一术语定义可以避免大量沟通误解。

## Key Terms | 术语速查表

| Term / 术语 | What people say / 人们常说的 | What it actually means / 实际含义 |
|------|-----------------|-----------------------|
| Multilingual model（多语言模型） | One model, many languages / 一个模型多种语言 | Shared vocabulary and parameters across languages. / 跨语言共享词表和参数。 |
| Cross-lingual transfer（跨语言迁移） | Train on one, run on another / 训练一种，运行另一种 | Fine-tune on source, evaluate on target without target labels. / 在源语言微调，在目标语言评估。 |
| Zero-shot（零样本） | No target labels / 无目标标签 | Transfer without target-language fine-tuning. / 无目标语言微调的迁移。 |
| Few-shot（少样本） | Small target labels / 少量目标标签 | 100-500 target-language examples for fine-tuning. / 100-500 个目标语言样本。 |
| mBERT | First multilingual LM / 首个多语言 LM | 104-language BERT on Wikipedia. / 104 语言 BERT。 |
| XLM-R | Cross-lingual baseline / 跨语言基线 | 100-language RoBERTa on CommonCrawl. / 100 语言 RoBERTa。 |
| NLLB | 200-language MT / 200 语言 MT | No Language Left Behind. 55 low-resource languages. / 不让任何语言掉队。55 种低资源语言。 |

> **【中文解读】** 延伸阅读提供了深入学习的高质量资源。这些论文和教程是该领域的经典参考文献，适合需要深入理解的读者。

## Further Reading | 延伸阅读

- [Conneau et al. (2019). XLM-R](https://arxiv.org/abs/1911.02116) — the XLM-R paper. / XLM-R 论文。
- [Pires et al. (2019). How Multilingual is Multilingual BERT?](https://arxiv.org/abs/1906.01502) — the cross-lingual transfer analysis. / 跨语言迁移分析。
- [Costa-jussà et al. (2022). No Language Left Behind](https://arxiv.org/abs/2207.04672) — NLLB-200. / NLLB-200 论文。
- [Üstün et al. (2024). Aya Model](https://arxiv.org/abs/2402.07827) — Cohere's multilingual LLM. / Cohere 多语言 LLM。
- [Language Similarity Predicts Cross-Lingual Transfer (2026)](https://www.mdpi.com/2504-4990/8/3/65) — qWALS / LANGRANK. / qWALS / LANGRANK 源语言论文。
