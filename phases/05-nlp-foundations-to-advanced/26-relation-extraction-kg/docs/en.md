# Relation Extraction & Knowledge Graph Construction | 关系抽取与知识图谱构建

> NER found the entities. Entity linking anchored them. Relation extraction finds the edges between them. A knowledge graph is the sum of nodes, edges, and their provenance.

> **【中文解读】** 从文本中抽取关系，构建知识图谱。

**Type:** Build | **类型:** 动手
**Languages:** Python | **语言:** Python
**Prerequisites:** Phase 5 · 06 (NER), Phase 5 · 25 (Entity Linking) | **前置知识:** Phase 5 · 06 (NER), Phase 5 · 25 (Entity Linking)
**Time:** ~60 minutes | **时间:** ~60 minutes
> 关系抽取与知识图谱构建


## The Problem | 问题引入

An analyst reads: "Tim Cook became CEO of Apple in 2011." Four facts:
> An analyst reads: "Tim Cook became CEO of Apple in 2011." Four facts:

> **【中文解读】** 本节提出的问题是：如何在实际工程中正确理解和应用这一技术。理解问题背景有助于把握技术选型的关键决策点。在实际 AI 系统中，错误的技术选型往往比实现细节的 bug 代价更高。


- `(Tim Cook, role, CEO)`
- `(Tim Cook, employer, Apple)`
- `(Tim Cook, start_date, 2011)`
- `(Apple, type, Organization)`
> - `(Tim Cook, role, CEO)`
- `(Tim Cook, employer, Apple)`
- `(Tim Cook, start_date, 2011)`
- `(Apple, type, Organization)`

Relation Extraction (RE) turns free text into structured triples `(subject, relation, object)`. Aggregate across a corpus and you have a knowledge graph. Aggregate and query and you have a reasoning substrate for RAG, analytics, or compliance audits.
> Relation Extraction (RE) turns free text into structured triples `(subject, relation, object)`. Aggregate across a corpus and you have a knowledge graph. Aggregate and query and you have a reasoning substrate for RAG, analytics, or compliance audits.

The 2026 problem: LLMs extract relations enthusiastically. Too enthusiastically. They hallucinate triples that the source text does not support. Without provenance, you cannot tell real triples from plausible fiction. The 2026 answer is AEVS-style anchor-and-verify pipelines.
> The 2026 problem: LLMs extract relations enthusiastically. Too enthusiastically. They hallucinate triples that the source text does not support. Without provenance, you cannot tell real triples from plausible fiction. The 2026 answer is AEVS-style anchor-and-verify pipelines.

## The Concept | 核心概念

> **【中文解读】** 本节介绍核心概念和理论基础。掌握这些概念是后续动手实现的前提，同时也是面试和工程实践中高频考察的知识点。


![Text → triples → knowledge graph](../assets/relation-extraction.svg)
> ![Text → triples → knowledge graph](../assets/relation-extraction.svg)

**Triple form.** `(subject_entity, relation_type, object_entity)`. Relations come from a closed ontology (Wikidata properties, FIBO, UMLS) or an open set (OpenIE-style, anything goes).
> **Triple form.** `(subject_entity, relation_type, object_entity)`. Relations come from a closed ontology (Wikidata properties, FIBO, UMLS) or an open set (OpenIE-style, anything goes).

**Three extraction approaches.**
> **Three extraction approaches.**

1. **Rule / pattern-based.** Hearst patterns: "X such as Y" → `(Y, isA, X)`. Plus hand-crafted regex. Brittle, precise, explainable.
2. **Supervised classifier.** Given two entity mentions in a sentence, predict the relation from a fixed set. Trained on TACRED, ACE, KBP. Standard 2015–2022.
3. **Generative LLM.** Prompt the model to emit triples. Works out of the box. Needs provenance, or hallucinates plausible-looking junk.
> 1. **Rule / pattern-based.** Hearst patterns: "X such as Y" → `(Y, isA, X)`. Plus hand-crafted regex. Brittle, precise, explainable.
2. **Supervised classifier.** Given two entity mentions in a sentence, predict the relation from a fixed set. Trained on TACRED, ACE, KBP. Standard 2015–2022.
3. **Generative LLM.** Prompt the model to emit triples. Works out of the box. Needs provenance, or hallucinates plausible-looking junk.

**AEVS (Anchor-Extraction-Verification-Supplement, 2026).** The current hallucination-mitigation framework:
> **AEVS (Anchor-Extraction-Verification-Supplement, 2026).** The current hallucination-mitigation framework:

- **Anchor.** Identify every entity span and relation-phrase span with exact positions.
- **Extract.** Generate triples linked to anchor spans.
- **Verify.** Match each triple element back to the source text; reject anything unsupported.
- **Supplement.** A coverage pass ensures no anchored span is dropped.
> - **Anchor.** Identify every entity span and relation-phrase span with exact positions.
- **Extract.** Generate triples linked to anchor spans.
- **Verify.** Match each triple element back to the source text; reject anything unsupported.
- **Supplement.** A coverage pass ensures no anchored span is dropped.

Hallucinations drop sharply. Requires more compute but is auditable.
> Hallucinations drop sharply. Requires more compute but is auditable.

**The open-vs-closed tradeoff.**
> **The open-vs-closed tradeoff.**

- **Closed ontology.** Fixed property list (e.g., Wikidata's 11,000+ properties). Predictable. Queryable. Hard to invent.
- **Open IE.** Any verbal phrase becomes a relation. High recall. Low precision. Messy to query.
> - **Closed ontology.** Fixed property list (e.g., Wikidata's 11,000+ properties). Predictable. Queryable. Hard to invent.
- **Open IE.** Any verbal phrase becomes a relation. High recall. Low precision. Messy to query.

Production KGs usually mix: open IE for discovery, then canonicalize relations onto a closed ontology before merging into the main graph.
> Production KGs usually mix: open IE for discovery, then canonicalize relations onto a closed ontology before merging into the main graph.

> **【中文解读】** 本节通过代码从零实现核心算法。这种 "from scratch" 的方式能帮助理解框架背后的原理，遇到问题时不会被黑盒困住。

> **【拓展：大语言模型的工程实践】** 从 GPT 到 ChatGPT，NLP 领域经历了从 "每个任务训练一个模型" 到 "一个模型解决所有任务" 的范式转变。在实际工程中，LLM 的部署需要考虑 Token 限制、延迟、成本、安全审查等问题。LangChain、LlamaIndex 等框架简化了 LLM 应用的开发。

> **【拓展：RAG 与企业知识库】** 检索增强生成（RAG）是当前企业 AI 应用最流行的架构：将用户查询先检索相关文档片段，再将检索结果作为上下文喂给 LLM 生成答案。这种方式解决了 LLM 知识过时和幻觉问题。向量数据库（如 Milvus、Pinecone、Weaviate）是 RAG 系统的核心组件。

> **【拓展：NLP 的多语言挑战】** 全球有 7000+ 种语言，但 NLP 研究主要集中在英语等少数语言。跨语言迁移学习、多语言预训练模型（如 mBERT、XLM-R）是解决低资源语言 NLP 的主要方法。字节级模型（如 ByT5）甚至可以在无分词器的情况下处理任何语言。


## Build It | 动手实现

### Step 1: pattern-based extraction
> See `code/main.py` for the full toy extractor. Hearst patterns still ship in domain-specific pipelines because they are debuggable.

```python
PATTERNS = [
    (r"(?P<s>[A-Z]\w+) (?:is|was) (?:a|an|the) (?P<o>[A-Z]?\w+)", "isA"),
    (r"(?P<s>[A-Z]\w+) (?:is|was) born in (?P<o>\w+)", "bornIn"),
    (r"(?P<s>[A-Z]\w+) works? (?:at|for) (?P<o>[A-Z]\w+)", "worksAt"),
    (r"(?P<s>[A-Z]\w+) founded (?P<o>[A-Z]\w+)", "founded"),
]
```

See `code/main.py` for the full toy extractor. Hearst patterns still ship in domain-specific pipelines because they are debuggable.
> REBEL is a seq2seq relation extractor: text in, triples out, already in Wikidata property ids. Fine-tuned on distant-supervision data. Standard open-weights baseline.

### Step 2: supervised relation classification
> Verify every returned span against the source. Reject anything where `text[start:end] != triple_entity`. This is the AEVS "verify" step in its minimal form.

```python
from transformers import AutoTokenizer, AutoModelForSequenceClassification

tok = AutoTokenizer.from_pretrained("Babelscape/rebel-large")
model = AutoModelForSequenceClassification.from_pretrained("Babelscape/rebel-large")

text = "Tim Cook was born in Alabama. He later became CEO of Apple."
encoded = tok(text, return_tensors="pt", truncation=True)
output = model.generate(**encoded, max_length=200)
triples = tok.batch_decode(output, skip_special_tokens=False)
```

REBEL is a seq2seq relation extractor: text in, triples out, already in Wikidata property ids. Fine-tuned on distant-supervision data. Standard open-weights baseline.
> Canonicalization is often 60-80% of the engineering work. Budget for it.

### Step 3: LLM-prompted extraction with anchoring
> This is the atom of every RAG-over-KG system. Scale it with RDF triple stores (Blazegraph, Virtuoso), property graphs (Neo4j), or vector-augmented graph stores.

```python
prompt = f"""Extract (subject, relation, object) triples from the text.
For each triple, include the exact character span in the source text.

Text: {text}

Output JSON:
[{{"subject": {{"text": "...", "span": [start, end]}},
   "relation": "...",
   "object": {{"text": "...", "span": [start, end]}}}}, ...]

Only include triples fully supported by the text. No inference beyond what is stated.
"""
```

Verify every returned span against the source. Reject anything where `text[start:end] != triple_entity`. This is the AEVS "verify" step in its minimal form.

### Step 4: canonicalize onto a closed ontology

```python
RELATION_MAP = {
    "is the CEO of": "P169",       # "chief executive officer"
    "was born in":   "P19",         # "place of birth"
    "founded":        "P112",       # "founded by" (inverted subject/object)
    "works at":       "P108",       # "employer"
}


def canonicalize(relation):
    rel_low = relation.lower().strip()
    if rel_low in RELATION_MAP:
        return RELATION_MAP[rel_low]
    return None   # drop unmapped open relations or route to manual review
```

Canonicalization is often 60-80% of the engineering work. Budget for it.

### Step 5: build a small graph and query

```python
triples = extract(text)
graph = {}
for s, r, o in triples:
    graph.setdefault(s, []).append((r, o))


def neighbors(node, relation=None):
    return [(r, o) for r, o in graph.get(node, []) if relation is None or r == relation]


print(neighbors("Tim Cook", relation="P108"))    # -> [(P108, Apple)]
```

This is the atom of every RAG-over-KG system. Scale it with RDF triple stores (Blazegraph, Virtuoso), property graphs (Neo4j), or vector-augmented graph stores.


> **【拓展：Prompt Engineering 与 LLM 应用】** Prompt Engineering 已成为 NLP 工程师的核心技能。从 Zero-shot 到 Few-shot，从 Chain-of-Thought 到 ReAct，不同的提示策略适用于不同场景。在实际项目中，系统提示（System Prompt）的设计直接影响 LLM 应用的稳定性和输出质量。

## Pitfalls

- **Coreference before RE.** "He founded Apple" — RE needs to know who "he" is. Run coref first (lesson 24).
- **Entity canonicalization.** "Apple Inc" and "Apple" must resolve to the same node. Entity linking first (lesson 25).
- **Hallucinated triples.** LLMs emit triples the text does not support. Enforce span verification.
- **Relation canonicalization drift.** Open IE relations are inconsistent ("was born in," "came from," "is a native of"). Collapse to canonical ids or the graph is unqueryable.
- **Temporal errors.** "Tim Cook is CEO of Apple" — true now, false in 2005. Many relations are time-bounded. Use qualifiers (`P580` start time, `P582` end time in Wikidata).
- **Domain mismatch.** REBEL trained on Wikipedia. Legal, medical, and scientific text often need domain-fine-tuned RE models.
> - **Coreference before RE.** "He founded Apple" — RE needs to know who "he" is. Run coref first (lesson 24).
- **Entity canonicalization.** "Apple Inc" and "Apple" must resolve to the same node. Entity linking first (lesson 25).
- **Hallucinated triples.** LLMs emit triples the text does not support. Enforce span verification.
- **Relation canonicalization drift.** Open IE relations are inconsistent ("was born in," "came from," "is a native of"). Collapse to canonical ids or the graph is unqueryable.
- **Temporal errors.** "Tim Cook is CEO of Apple" — true now, false in 2005. Many relations are time-bounded. Use qualifiers (`P580` start time, `P582` end time in Wikidata).
- **Domain mismatch.** REBEL trained on Wikipedia. Legal, medical, and scientific text often need domain-fine-tuned RE models.

> **【中文解读】** 本节展示如何用成熟框架（如 PyTorch、HuggingFace 等）快速应用该技术。在实际项目中，优先使用经过验证的框架实现，可以减少 bug 并提高开发效率。


## Use It | 用框架实现

The 2026 stack:
> The 2026 stack:

| Situation | Pick |
|-----------|------|
| Fast production, general domain | REBEL or LlamaPred with Wikidata canonicalization |
| Domain-specific (biomed, legal) | SciREX-style domain fine-tune + custom ontology |
| LLM-prompted, audited output | AEVS pipeline: anchor → extract → verify → supplement |
| High-volume news IE | Pattern-based + supervised hybrid |
| Building a KG from scratch | Open IE + manual canonicalization pass |
| Temporal KG | Extract with qualifiers (start/end time, point in time) |
> | 场景 | 选择 |
|------|------|
| Fast production, general domain | REBEL or LlamaPred with Wikidata canonicalization |
| Domain-specific (biomed, legal) | SciREX-style domain fine-tune + custom ontology |
| LLM-prompted, audited output | AEVS pipeline: anchor → extract → verify → supplement |
| High-volume news IE | Pattern-based + supervised hybrid |
| Building a KG from scratch | Open IE + manual canonicalization pass |
| Temporal KG | Extract with qualifiers (start/end time, point in time) |

> **【中文解读】** 本节关注如何将模型部署为可用的产品。从原型到生产级系统需要考虑性能优化、错误处理、监控等多个维度。


The integration pattern: NER → coref → entity linking → relation extraction → ontology mapping → graph load. Every stage is a potential quality gate.
> The integration pattern: NER → coref → entity linking → relation extraction → ontology mapping → graph load. Every stage is a potential quality gate.


## Ship It | 产出物

Save as `outputs/skill-re-designer.md`:
> 保存为 `outputs/skill-re-designer.md`:

```markdown
---
name: re-designer
description: Design a relation extraction pipeline with provenance and canonicalization.
version: 1.0.0
phase: 5
lesson: 26
tags: [nlp, relation-extraction, knowledge-graph]
---

Given a corpus (domain, language, volume) and downstream use (KG-RAG, analytics, compliance), output:

1. Extractor. Pattern-based / supervised / LLM / AEVS hybrid. Reason tied to precision vs recall target.
2. Ontology. Closed property list (Wikidata / domain) or open IE with canonicalization pass.
3. Provenance. Every triple carries source char-span + doc id. Non-negotiable for audit.
4. Merge strategy. Canonical entity id + relation id + temporal qualifiers; dedup policy.
5. Evaluation. Precision / recall on 200 hand-labelled triples + hallucination-rate on LLM-extracted sample.

> **【中文解读】** 练习题按照 Easy/Medium/Hard 三个难度递进。建议至少完成 Medium 级别的题目，Hard 级别适合深入研究或面试准备。


Refuse any LLM-based RE pipeline without span verification (source provenance). Refuse open-IE output flowing into a production graph without canonicalization. Flag pipelines with no temporal qualifier on time-bounded relations (employer, spouse, position).
```

## Exercises | 练习题

> **【中文解读】** 术语表中的 "What people say" vs "What it actually means" 区分了日常口语和精确技术含义。在团队协作中，统一术语定义可以避免大量沟通误解。


1. **Easy.** Run the pattern extractor in `code/main.py` on 5 news-article sentences. Hand-check precision.
2. **Medium.** Use REBEL (or a small LLM) on the same sentences. Compare triples. Which extractor has higher precision? Higher recall?
3. **Hard.** Build the AEVS pipeline: extract with LLM + verify spans against source. Measure hallucination rate before vs after the verify step on 50 Wikipedia-style sentences.
> 1. **Easy.** Run the pattern extractor in `code/main.py` on 5 news-article sentences. Hand-check precision.
2. **Medium.** Use REBEL (or a small LLM) on the same sentences. Compare triples. Which extractor has higher precision? Higher recall?
3. **Hard.** Build the AEVS pipeline: extract with LLM + verify spans against source. Measure hallucination rate before vs after the verify step on 50 Wikipedia-style sentences.

## Key Terms | 术语速查表

| Term | What people say | What it actually means |
|------|-----------------|-----------------------|
| Triple | Subject-relation-object | `(s, r, o)` tuple that is the atomic unit of a KG. |
| Open IE | Extract anything | Open-vocabulary relation phrases; high recall, low precision. |
| Closed ontology | Fixed schema | Bounded set of relation types (Wikidata, UMLS, FIBO). |
| Canonicalization | Normalize everything | Map surface names / relations to canonical ids. |
| AEVS | Grounded extraction | Anchor-Extraction-Verification-Supplement pipeline (2026). |
| Provenance | Source-of-truth link | Every triple carries a doc id + char-span to its source. |
| Distant supervision | Cheap labels | Align text with an existing KG to create training data. |
> | 术语 | 人们常说的 | 实际含义 |
|------|-----------|---------|
| Triple | Subject-relation-object | `(s, r, o)` tuple that is the atomic unit of a KG. |
| Open IE | Extract anything | Open-vocabulary relation phrases; high recall, low precision. |
| Closed ontology | Fixed schema | Bounded set of relation types (Wikidata, UMLS, FIBO). |
| Canonicalization | Normalize everything | Map surface names / relations to canonical ids. |
| AEVS | Grounded extraction | Anchor-Extraction-Verification-Supplement pipeline (2026). |
| Provenance | Source-of-truth link | Every triple carries a doc id + char-span to its source. |
| Distant supervision | Cheap labels | Align text with an existing KG to create training data. |

> **【中文解读】** 延伸阅读提供了深入学习的高质量资源。这些论文和教程是该领域的经典参考文献，适合需要深入理解的读者。


## Further Reading | 延伸阅读

- [Mintz et al. (2009). Distant supervision for relation extraction without labeled data](https://www.aclweb.org/anthology/P09-1113.pdf) — the distant-supervision paper.
- [Huguet Cabot, Navigli (2021). REBEL: Relation Extraction By End-to-end Language generation](https://aclanthology.org/2021.findings-emnlp.204.pdf) — seq2seq RE workhorse.
- [Wadden et al. (2019). Entity, Relation, and Event Extraction with Contextualized Span Representations (DyGIE++)](https://arxiv.org/abs/1909.03546) — joint IE.
- [AEVS — Anchor-Extraction-Verification-Supplement framework](https://www.mdpi.com/2073-431X/15/3/178) — 2026 hallucination-mitigation design.
- [Wikidata SPARQL tutorial](https://www.wikidata.org/wiki/Wikidata:SPARQL_tutorial) — canonical graph queries.
> - [Mintz et al. (2009). Distant supervision for relation extraction without labeled data](https://www.aclweb.org/anthology/P09-1113.pdf) — the distant-supervision paper.
- [Huguet Cabot, Navigli (2021). REBEL: Relation Extraction By End-to-end Language generation](https://aclanthology.org/2021.findings-emnlp.204.pdf) — seq2seq RE workhorse.
- [Wadden et al. (2019). Entity, Relation, and Event Extraction with Contextualized Span Representations (DyGIE++)](https://arxiv.org/abs/1909.03546) — joint IE.
- [AEVS — Anchor-Extraction-Verification-Supplement framework](https://www.mdpi.com/2073-431X/15/3/178) — 2026 hallucination-mitigation design.
- [Wikidata SPARQL tutorial](https://www.wikidata.org/wiki/Wikidata:SPARQL_tutorial) — canonical graph queries.
