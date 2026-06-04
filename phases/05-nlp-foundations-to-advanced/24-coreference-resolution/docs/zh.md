共指消解

> "She called him. He did not answer. The doctor was at lunch." Three references to two people and nobody is named. Coreference resolution figures out who is who.

> **【中文解读】** 识别文本中指代同一实体的不同表达。

**类型：** 学习
**编程语言：** Python
**前置课程：** Phase 5 · 06 (NER), Phase 5 · 07 (POS & Parsing)
**预计时长：** ~60 minutes

## 问题引入

Extract every mention of Apple Inc. from a 300-word article. Easy when the article says "Apple." Hard when it says "the company," "they," "Cupertino's technology giant," or "Jobs's firm." Without resolving these mentions to the same entity, your NER pipeline misses 60-80% of the mentions.

> **【中文解读】** 本节提出的问题是：如何在实际工程中正确理解和应用这一技术。理解问题背景有助于把握技术选型的关键决策点。在实际 AI 系统中，错误的技术选型往往比实现细节的 bug 代价更高。


Coreference resolution links every expression that refers to the same real-world entity into one cluster. It is the glue between surface-level NLP (NER, parsing) and downstream semantics (IE, QA, summarization, KG).

Why it matters in 2026:

- Summarization: "The CEO announced..." vs "Tim Cook announced..." — the summary should name the CEO.
- Question answering: "Who did she call?" requires resolving "she."
- Information extraction: a knowledge graph with "PER1 founded Apple" and "Jobs founded Apple" as separate entries is wrong.
- Multi-document IE: merging mentions across articles about the same event is cross-document coreference.

## 核心概念

> **【中文解读】** 本节介绍核心概念和理论基础。掌握这些概念是后续动手实现的前提，同时也是面试和工程实践中高频考察的知识点。


![Coreference clustering: mentions → entities](../assets/coref.svg)

**The task.** Input: a document. Output: a clustering of mentions (spans) where each cluster refers to one entity.

**Mention types.**

- **Named entity.** "Tim Cook"
- **Nominal.** "the CEO", "the company"
- **Pronominal.** "he", "she", "they", "it"
- **Appositive.** "Tim Cook, Apple's CEO,"

**Architectures.**

1. **Rule-based (Hobbs, 1978).** Syntactic-tree-based pronoun resolution using grammar rules. Good baseline. Surprisingly hard to beat on pronouns.
2. **Mention-pair classifier.** For every pair of mentions (m_i, m_j), predict whether they corefer. Cluster by transitive closure. Standard pre-2016.
3. **Mention-ranking.** For each mention, rank candidate antecedents (including "no antecedent"). Pick the top.
4. **Span-based end-to-end (Lee et al., 2017).** Transformer encoder. Enumerate all candidate spans up to a length cap. Predict mention scores. Predict antecedent-probability for each span. Cluster greedily. The modern default.
5. **Generative (2024+).** Prompt an LLM: "List every pronoun in this text and its antecedent." Works well on easy cases, struggles on long documents and rare referents.

**The evaluation metrics.** Five standard metrics (MUC, B³, CEAF, BLANC, LEA) because no single metric captures clustering quality. Report the average of the first three as CoNLL F1. State-of-the-art in 2026 on CoNLL-2012: ~83 F1.

**Known hard cases.**

- Definite descriptions referring to entities introduced pages earlier.
- Bridging anaphora ("the wheels" → a previously mentioned car).
- Zero anaphora in languages like Chinese and Japanese.
- Cataphora (pronoun before referent): "When **she** walked in, Mary smiled."

> **【中文解读】** 本节通过代码从零实现核心算法。这种 "from scratch" 的方式能帮助理解框架背后的原理，遇到问题时不会被黑盒困住。

> **【拓展：大语言模型的工程实践】** 从 GPT 到 ChatGPT，NLP 领域经历了从 "每个任务训练一个模型" 到 "一个模型解决所有任务" 的范式转变。在实际工程中，LLM 的部署需要考虑 Token 限制、延迟、成本、安全审查等问题。LangChain、LlamaIndex 等框架简化了 LLM 应用的开发。

> **【拓展：RAG 与企业知识库】** 检索增强生成（RAG）是当前企业 AI 应用最流行的架构：将用户查询先检索相关文档片段，再将检索结果作为上下文喂给 LLM 生成答案。这种方式解决了 LLM 知识过时和幻觉问题。向量数据库（如 Milvus、Pinecone、Weaviate）是 RAG 系统的核心组件。

> **【拓展：NLP 的多语言挑战】** 全球有 7000+ 种语言，但 NLP 研究主要集中在英语等少数语言。跨语言迁移学习、多语言预训练模型（如 mBERT、XLM-R）是解决低资源语言 NLP 的主要方法。字节级模型（如 ByT5）甚至可以在无分词器的情况下处理任何语言。





## 动手实现

### 步骤 1： pretrained neural coreference (AllenNLP / spaCy-experimental)

```python
import spacy
nlp = spacy.load("en_coreference_web_trf")   # experimental model
doc = nlp("Apple announced new products. The company said they would ship soon.")
for cluster in doc._.coref_clusters:
    print(cluster, "->", [m.text for m in cluster])
```

On a longer document, you get something like:
- Cluster 1: [Apple, The company, they]
- Cluster 2: [new products]

### 步骤 2： rule-based pronoun resolver (teaching)

See `code/main.py` for a stdlib-only implementation:

1. Extract mentions: named entities (capitalized spans), pronouns (dict lookup), definite descriptions ("the X").
2. For each pronoun, look at the previous K mentions and score them by:
   - gender/number agreement (heuristic)
   - recency (closer wins)
   - syntactic role (subjects preferred)
3. Link the highest-scoring antecedent.

Not competitive with neural models. But it shows the search space and the decisions an end-to-end model must make.

### 步骤 3： using LLMs for coreference

```python
prompt = f"""Text: {text}

List every pronoun and noun phrase that refers to a person or company.
Cluster them by what they refer to. Output JSON:
[{{"entity": "Apple", "mentions": ["Apple", "the company", "it"]}}, ...]
"""
```

Two failure modes to watch. First, LLMs over-merge ("him" and "her" referring to two distinct people). Second, LLMs silently drop mentions in long documents. Always verify with span-offset checks.

### 步骤 4： evaluation

The standard conll-2012 script computes MUC, B³, CEAF-φ4 and reports the average. For an in-house eval, start with span-level precision and recall on your annotated test set, then add mention-linking F1.




> **【拓展：Prompt Engineering 与 LLM 应用】** Prompt Engineering 已成为 NLP 工程师的核心技能。从 Zero-shot 到 Few-shot，从 Chain-of-Thought 到 ReAct，不同的提示策略适用于不同场景。在实际项目中，系统提示（System Prompt）的设计直接影响 LLM 应用的稳定性和输出质量。

## Pitfalls

- **Singleton explosion.** Some systems report every mention as its own cluster. B³ is lenient. MUC punishes this. Always check all three metrics.
- **Pronouns in long context.** Performance drops ~15 F1 on documents over 2,000 tokens. Chunk carefully.
- **Gender assumptions.** Hard-coded gender rules break on non-binary referents, organizations, animals. Use learned models or neutral scoring.
- **LLM drift on long docs.** A single API call cannot reliably cluster mentions across 50+ paragraphs. Use sliding-window + merge.

> **【中文解读】** 本节展示如何用成熟框架（如 PyTorch、HuggingFace 等）快速应用该技术。在实际项目中，优先使用经过验证的框架实现，可以减少 bug 并提高开发效率。


## 用框架实现

The 2026 stack:

| 场景 | 选择 |
|------|------|
| English, single document | `en_coreference_web_trf` (spaCy-experimental) or AllenNLP neural coref |
| Multilingual | SpanBERT / XLM-R trained on OntoNotes or Multilingual CoNLL |
| Cross-document event coref | Specialized end-to-end models (2025–26 SOTA) |
| Quick LLM baseline | GPT-4o / Claude with structured-output coref prompt |
| Production dialog systems | Rule-based fallback + neural primary + manual review for critical slots |

> **【中文解读】** 本节关注如何将模型部署为可用的产品。从原型到生产级系统需要考虑性能优化、错误处理、监控等多个维度。


The integration pattern that ships in 2026: run NER first, run coref, merge coref clusters into NER entities. Downstream tasks see one entity per cluster, not one entity per mention.



## 产出物

保存为 `outputs/skill-coref-picker.md`:

```markdown
---
name: coref-picker
description: Pick a coreference approach, evaluation plan, and integration strategy.
version: 1.0.0
phase: 5
lesson: 24
tags: [nlp, coref, information-extraction]
---

Given a use case (single-doc / multi-doc, domain, language), output:

1. Approach. Rule-based / neural span-based / LLM-prompted / hybrid. One-sentence reason.
2. Model. Named checkpoint if neural.
3. Integration. Order of operations: tokenize → NER → coref → downstream task.
4. Evaluation. CoNLL F1 (MUC + B³ + CEAF-φ4 average) on held-out set + manual cluster review on 20 documents.

> **【中文解读】** 练习题按照 Easy/Medium/Hard 三个难度递进。建议至少完成 Medium 级别的题目，Hard 级别适合深入研究或面试准备。


Refuse LLM-only coref for documents over 2,000 tokens without sliding-window merge. Refuse any pipeline that runs coref without a mention-level precision-recall report. Flag gender-heuristic systems deployed in demographically diverse text.
```

## 练习题

> **【中文解读】** 术语表中的 "What people say" vs "What it actually means" 区分了日常口语和精确技术含义。在团队协作中，统一术语定义可以避免大量沟通误解。


1. **Easy.** Run the rule-based resolver in `code/main.py` on 5 hand-crafted paragraphs. Measure mention-link accuracy against ground truth.
2. **Medium.** Use a pretrained neural coref model on a news article. Compare clusters against your own manual annotation. Where did it fail?
3. **Hard.** Build a coref-enhanced NER pipeline: NER first, then merge via coref clusters. Measure entity-coverage improvement vs NER-only on 100 articles.

## 术语速查表

| 术语 | 人们常说的 | 实际含义 |
|------|-----------|---------|
| Mention | A reference | A span of text that refers to an entity (name, pronoun, noun phrase). |
| Antecedent | What "it" refers to | The earlier mention a later one corefers with. |
| Cluster | The entity's mentions | Set of mentions that all refer to the same real-world entity. |
| Anaphora | Backward reference | Later mention refers to earlier ("he" → "John"). |
| Cataphora | Forward reference | Earlier mention refers to later ("When he arrived, John..."). |
| Bridging | Implicit reference | "I bought a car. The wheels were bad." (wheels of THAT car.) |
| CoNLL F1 | The number on leaderboards | Average of MUC, B³, CEAF-φ4 F1 scores. |

> **【中文解读】** 延伸阅读提供了深入学习的高质量资源。这些论文和教程是该领域的经典参考文献，适合需要深入理解的读者。


## 延伸阅读

- [Jurafsky & Martin, SLP3 Ch. 26 — Coreference Resolution and Entity Linking](https://web.stanford.edu/~jurafsky/slp3/26.pdf) — canonical textbook chapter.
- [Lee et al. (2017). End-to-end Neural Coreference Resolution](https://arxiv.org/abs/1707.07045) — span-based end-to-end.
- [Joshi et al. (2020). SpanBERT](https://arxiv.org/abs/1907.10529) — pretraining that improves coref.
- [Pradhan et al. (2012). CoNLL-2012 Shared Task](https://aclanthology.org/W12-4501/) — the benchmark.
- [Hobbs (1978). Resolving Pronoun References](https://www.sciencedirect.com/science/article/pii/0024384178900064) — the rule-based classic.
