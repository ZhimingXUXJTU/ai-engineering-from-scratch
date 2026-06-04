实体链接与消歧

> NER found "Paris." Entity linking decides: Paris, France? Paris Hilton? Paris, Texas? Paris (the Trojan prince)? Without linking, your knowledge graph stays ambiguous.

> **【中文解读】** 把实体链接到知识库中的对应条目。

**类型：** 构建
**编程语言：** Python
**前置课程：** Phase 5 · 06 (NER), Phase 5 · 24 (Coreference Resolution)
**预计时长：** ~60 minutes

## 问题引入

A sentence reads: "Jordan beat the press." Your NER tags "Jordan" as PERSON. Good. But *which* Jordan?

> **【中文解读】** 本节提出的问题是：如何在实际工程中正确理解和应用这一技术。理解问题背景有助于把握技术选型的关键决策点。在实际 AI 系统中，错误的技术选型往往比实现细节的 bug 代价更高。


- Michael Jordan (basketball)?
- Michael B. Jordan (actor)?
- Michael I. Jordan (Berkeley ML professor — yes, this confusion is real in ML papers)?
- Jordan (the country)?
- Jordan (Hebrew first name)?

Entity linking (EL) resolves each mention to a unique entry in a knowledge base: Wikidata, Wikipedia, DBpedia, or your domain KB. Two subtasks:

1. **Candidate generation.** Given "Jordan," which KB entries are plausible?
2. **Disambiguation.** Given the context, which candidate is the right one?

Both steps are learnable. Both are benchmarked. The combined pipeline has been stable for a decade — what changes is the quality of the disambiguator.

## 核心概念

> **【中文解读】** 本节介绍核心概念和理论基础。掌握这些概念是后续动手实现的前提，同时也是面试和工程实践中高频考察的知识点。


![Entity linking pipeline: mention → candidates → disambiguated entity](../assets/entity-linking.svg)

**Candidate generation.** Given the mention surface form ("Jordan"), look up candidates in an alias index. Wikipedia alias dictionaries cover most named entities: "JFK" → John F. Kennedy, Jacqueline Kennedy, JFK airport, JFK (movie). Typical index returns 10-30 candidates per mention.

**Disambiguation: three approaches.**

1. **Prior + context (Milne & Witten, 2008).** `P(entity | mention) × context-similarity(entity, text)`. Works well, fast, no training.
2. **Embedding-based (ESS / REL / Blink).** Encode mention + context. Encode each candidate's description. Pick max cosine. The 2020-2024 default.
3. **Generative (GENRE, 2021; LLM-based, 2023+).** Decode the entity's canonical name token-by-token. Constrained to a trie of valid entity names so output is guaranteed to be a valid KB id.

**End-to-end vs pipeline.** Modern models (ELQ, BLINK, ExtEnD, GENRE) run NER + candidate generation + disambiguation in one pass. Pipeline systems still dominate in production because you can swap components.

### The two measurements

- **Mention recall (candidate gen).** Fraction of gold mentions where the correct KB entry appears in the candidate list. Floor for the whole pipeline.
- **Disambiguation accuracy / F1.** Given correct candidates, how often the top-1 is right.

Always report both. A system with 99% disambiguation on 80% candidate recall is an 80% pipeline.

> **【中文解读】** 本节通过代码从零实现核心算法。这种 "from scratch" 的方式能帮助理解框架背后的原理，遇到问题时不会被黑盒困住。

> **【拓展：大语言模型的工程实践】** 从 GPT 到 ChatGPT，NLP 领域经历了从 "每个任务训练一个模型" 到 "一个模型解决所有任务" 的范式转变。在实际工程中，LLM 的部署需要考虑 Token 限制、延迟、成本、安全审查等问题。LangChain、LlamaIndex 等框架简化了 LLM 应用的开发。

> **【拓展：RAG 与企业知识库】** 检索增强生成（RAG）是当前企业 AI 应用最流行的架构：将用户查询先检索相关文档片段，再将检索结果作为上下文喂给 LLM 生成答案。这种方式解决了 LLM 知识过时和幻觉问题。向量数据库（如 Milvus、Pinecone、Weaviate）是 RAG 系统的核心组件。

> **【拓展：NLP 的多语言挑战】** 全球有 7000+ 种语言，但 NLP 研究主要集中在英语等少数语言。跨语言迁移学习、多语言预训练模型（如 mBERT、XLM-R）是解决低资源语言 NLP 的主要方法。字节级模型（如 ByT5）甚至可以在无分词器的情况下处理任何语言。





## 动手实现

### 步骤 1： build an alias index from Wikipedia redirects

```python
alias_to_entities = {
    "jordan": ["Q41421 (Michael Jordan)", "Q810 (Jordan, country)", "Q254110 (Michael B. Jordan)"],
    "paris":  ["Q90 (Paris, France)", "Q663094 (Paris, Texas)", "Q55411 (Paris Hilton)"],
    "apple":  ["Q312 (Apple Inc.)", "Q89 (apple, fruit)"],
}
```

Wikipedia alias data: ~18M (alias, entity) pairs. Download from Wikidata dumps. Store as inverted index.

### 步骤 2： context-based disambiguation

```python
def disambiguate(mention, context, alias_index, entity_desc):
    candidates = alias_index.get(mention.lower(), [])
    if not candidates:
        return None, 0.0
    context_words = set(tokenize(context))
    best, best_score = None, -1
    for entity_id in candidates:
        desc_words = set(tokenize(entity_desc[entity_id]))
        union = len(context_words | desc_words)
        score = len(context_words & desc_words) / union if union else 0.0
        if score > best_score:
            best, best_score = entity_id, score
    return best, best_score
```

The Jaccard overlap is a toy. Replace with cosine similarity on embeddings (see `code/main.py` step-2 for the transformer version).

### 步骤 3： embedding-based (BLINK-style)

```python
from sentence_transformers import SentenceTransformer
encoder = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")

def embed_mention(text, mention_span):
    start, end = mention_span
    marked = f"{text[:start]} [MENTION] {text[start:end]} [/MENTION] {text[end:]}"
    return encoder.encode([marked], normalize_embeddings=True)[0]

def embed_entity(entity_id, description):
    return encoder.encode([f"{entity_id}: {description}"], normalize_embeddings=True)[0]
```

At index time, embed every KB entity once. At query time, embed the mention + context once, dot-product against the candidate pool, pick max.

### 步骤 4： generative entity linking (concept)

GENRE decodes the entity's Wikipedia title character-by-character. Constrained decoding (see lesson 20) ensures only valid titles can be output. Tight integration with a KB-backed trie. The modern descendant is REL-GEN and LLM-prompted EL with structured output.

```python
prompt = f"""Text: {text}
Mention: {mention}
List the best Wikipedia title for this mention.
Respond with JSON: {{"title": "..."}}"""
```

Combined with a whitelist (Outlines `choice`), this is the simplest EL pipeline to ship in 2026.

### 步骤 5： evaluate on AIDA-CoNLL

AIDA-CoNLL is the standard EL benchmark: 1,393 Reuters articles, 34k mentions, Wikipedia entities. Report in-KB accuracy (`P@1`) and out-of-KB NIL-detection rate.




> **【拓展：Prompt Engineering 与 LLM 应用】** Prompt Engineering 已成为 NLP 工程师的核心技能。从 Zero-shot 到 Few-shot，从 Chain-of-Thought 到 ReAct，不同的提示策略适用于不同场景。在实际项目中，系统提示（System Prompt）的设计直接影响 LLM 应用的稳定性和输出质量。

## Pitfalls

- **NIL handling.** Some mentions are not in the KB (emerging entities, obscure people). Systems must predict NIL instead of guessing the wrong entity. Measured separately.
- **Mention boundary errors.** Upstream NER misses partial spans ("Bank of America" tagged as just "Bank"). EL recall drops.
- **Popularity bias.** Trained systems over-predict frequent entities. A mention of "Michael I. Jordan" on an ML paper often links to basketball Jordan.
- **Cross-lingual EL.** Mapping mentions in Chinese text to English Wikipedia entities. Requires a multilingual encoder or a translation step.
- **KB staleness.** New companies, events, people are not in last year's Wikipedia dump. Production pipelines need a refresh loop.

> **【中文解读】** 本节展示如何用成熟框架（如 PyTorch、HuggingFace 等）快速应用该技术。在实际项目中，优先使用经过验证的框架实现，可以减少 bug 并提高开发效率。


## 用框架实现

The 2026 stack:

| 场景 | 选择 |
|------|------|
| General-purpose English + Wikipedia | BLINK or REL |
| Cross-lingual, KB = Wikipedia | mGENRE |
| LLM-friendly, few mentions/day | Prompt Claude/GPT-4 with candidate list + constrained JSON |
| Domain-specific KB (medical, legal) | Custom BERT with KB-aware retrieval + fine-tune on domain AIDA-style set |
| Extremely low-latency | Exact-match prior only (Milne-Witten baseline) |
| Research SOTA | GENRE / ExtEnD / generative LLM-EL |

> **【中文解读】** 本节关注如何将模型部署为可用的产品。从原型到生产级系统需要考虑性能优化、错误处理、监控等多个维度。


Production pattern that ships in 2026: NER → coref → EL on each mention → collapse clusters to one canonical entity per cluster. Output: one KB id per entity in the document, not one per mention.



## 产出物

保存为 `outputs/skill-entity-linker.md`:

```markdown
---
name: entity-linker
description: Design an entity linking pipeline — KB, candidate generator, disambiguator, evaluation.
version: 1.0.0
phase: 5
lesson: 25
tags: [nlp, entity-linking, knowledge-graph]
---

Given a use case (domain KB, language, volume, latency budget), output:

1. Knowledge base. Wikidata / Wikipedia / custom KB. Version date. Refresh cadence.
2. Candidate generator. Alias-index, embedding, or hybrid. Target mention recall @ K.
3. Disambiguator. Prior + context, embedding-based, generative, or LLM-prompted.
4. NIL strategy. Threshold on top score, classifier, or explicit NIL candidate.
5. Evaluation. Mention recall @ 30, top-1 accuracy, NIL-detection F1 on held-out set.

Refuse any EL pipeline without a mention-recall baseline (you cannot evaluate a disambiguator without knowing candidate gen surfaced the right entity). Refuse any pipeline using LLM-prompted EL without constrained output to valid KB ids. Flag systems where popularity bias affects minority entities (e.g. name-clashes) without domain fine-tuning.
```

> **【中文解读】** 练习题按照 Easy/Medium/Hard 三个难度递进。建议至少完成 Medium 级别的题目，Hard 级别适合深入研究或面试准备。


## 练习题

1. **Easy.** Implement the prior+context disambiguator in `code/main.py` on 10 ambiguous mentions (Paris, Jordan, Apple). Hand-label the correct entity. Measure accuracy.
2. **Medium.** Encode 50 ambiguous mentions with a sentence transformer. Embed each candidate's description. Compare embedding-based disambiguation to Jaccard context overlap.
3. **Hard.** Build a 1k-entity domain KB (e.g. employees + products in your company). Implement NER + EL end-to-end. Measure precision and recall on 100 held-out sentences.

> **【中文解读】** 术语表中的 "What people say" vs "What it actually means" 区分了日常口语和精确技术含义。在团队协作中，统一术语定义可以避免大量沟通误解。


## 术语速查表

| 术语 | 人们常说的 | 实际含义 |
|------|-----------|---------|
| Entity linking (EL) | Link to Wikipedia | Map a mention to a unique KB entry. |
| Candidate generation | Who could it be? | Return a shortlist of plausible KB entries for a mention. |
| Disambiguation | Pick the right one | Score candidates using context, pick the winner. |
| Alias index | The lookup table | Map from surface form → candidate entities. |
| NIL | Not in KB | Explicit prediction that no KB entry matches. |
| KB | Knowledge base | Wikidata, Wikipedia, DBpedia, or your domain KB. |
| AIDA-CoNLL | The benchmark | 1,393 Reuters articles with gold entity links. |

> **【中文解读】** 延伸阅读提供了深入学习的高质量资源。这些论文和教程是该领域的经典参考文献，适合需要深入理解的读者。


## 延伸阅读

- [Milne, Witten (2008). Learning to Link with Wikipedia](https://www.cs.waikato.ac.nz/~ihw/papers/08-DM-IHW-LearningToLinkWithWikipedia.pdf) — the foundational prior+context approach.
- [Wu et al. (2020). Zero-shot Entity Linking with Dense Entity Retrieval (BLINK)](https://arxiv.org/abs/1911.03814) — the embedding-based workhorse.
- [De Cao et al. (2021). Autoregressive Entity Retrieval (GENRE)](https://arxiv.org/abs/2010.00904) — generative EL with constrained decoding.
- [Hoffart et al. (2011). Robust Disambiguation of Named Entities in Text (AIDA)](https://www.aclweb.org/anthology/D11-1072.pdf) — the benchmark paper.
- [REL: An Entity Linker Standing on the Shoulders of Giants (2020)](https://arxiv.org/abs/2006.01969) — the open production stack.
