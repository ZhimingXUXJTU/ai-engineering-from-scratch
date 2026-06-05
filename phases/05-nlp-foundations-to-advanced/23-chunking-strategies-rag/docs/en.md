# Chunking Strategies for RAG | RAG 分块策略

> Chunking configuration influences retrieval quality as much as the choice of embedding model (Vectara NAACL 2025). Get chunking wrong and no amount of reranking saves you.

> **【中文解读】** 如何把长文档切成适合检索的块。分块策略直接影响 RAG 效果。

**Type:** Build | **类型:** 动手
**Languages:** Python | **语言:** Python
**Prerequisites:** Phase 5 · 14 (Information Retrieval), Phase 5 · 22 (Embedding Models) | **前置知识:** Phase 5 · 14 (Information Retrieval), Phase 5 · 22 (Embedding Models)
**Time:** ~60 minutes | **时间:** ~60 minutes
> RAG 分块策略


## The Problem | 问题引入

You put a 50-page contract into a RAG system. User asks: "What is the termination clause?" The retriever returns the cover page. Why? Because the model was trained on 512-token chunks and the termination clause sits 20 pages in, split across a page break, with no local keywords tying it to the query.
> You put a 50-page contract into a RAG system. User asks: "What is the termination clause?" The retriever returns the cover page. Why? Because the model was trained on 512-token chunks and the termination clause sits 20 pages in, split across a page break, with no local keywords tying it to the query.

> **【中文解读】** 本节提出的问题是：如何在实际工程中正确理解和应用这一技术。理解问题背景有助于把握技术选型的关键决策点。在实际 AI 系统中，错误的技术选型往往比实现细节的 bug 代价更高。


The fix is not "buy a better embedding model." The fix is chunking. How big? Overlap? Where to split? With surrounding context?
> The fix is not "buy a better embedding model." The fix is chunking. How big? Overlap? Where to split? With surrounding context?

Feb 2026 benchmarks show surprising results:
> Feb 2026 benchmarks show surprising results:

- Vectara's 2026 study: recursive 512-token chunking beat semantic chunking 69% → 54% accuracy.
- SPLADE + Mistral-8B on Natural Questions: overlap provided zero measurable benefit.
- Context cliff: response quality drops sharply around 2,500 tokens of context.
> - Vectara's 2026 study: recursive 512-token chunking beat semantic chunking 69% → 54% accuracy.
- SPLADE + Mistral-8B on Natural Questions: overlap provided zero measurable benefit.
- Context cliff: response quality drops sharply around 2,500 tokens of context.

The "obvious" answer (semantic chunking, 20% overlap, 1000 tokens) is often wrong. This lesson builds intuition for six strategies and tells you when to reach for which.
> The "obvious" answer (semantic chunking, 20% overlap, 1000 tokens) is often wrong. This lesson builds intuition for six strategies and tells you when to reach for which.

## The Concept | 核心概念

> **【中文解读】** 本节介绍核心概念和理论基础。掌握这些概念是后续动手实现的前提，同时也是面试和工程实践中高频考察的知识点。


![Six chunking strategies visualized on one passage](../assets/chunking.svg)
> ![Six chunking strategies visualized on one passage](../assets/chunking.svg)

**Fixed chunking.** Split every N characters or tokens. Simplest baseline. Breaks mid-sentence. Good compression, bad coherence.
> **Fixed chunking.** Split every N characters or tokens. Simplest baseline. Breaks mid-sentence. Good compression, bad coherence.

**Recursive.** LangChain's `RecursiveCharacterTextSplitter`. Try splitting on `\n\n` first, then `\n`, then `.`, then space. Falls back cleanly. The 2026 default.
> **Recursive.** LangChain's `RecursiveCharacterTextSplitter`. Try splitting on `\n\n` first, then `\n`, then `.`, then space. Falls back cleanly. The 2026 default.

**Semantic.** Embed each sentence. Compute cosine similarity between adjacent sentences. Split where similarity drops below a threshold. Preserves topic coherence. Slower; sometimes produces tiny 40-token fragments that hurt retrieval.
> **Semantic.** Embed each sentence. Compute cosine similarity between adjacent sentences. Split where similarity drops below a threshold. Preserves topic coherence. Slower; sometimes produces tiny 40-token fragments that hurt retrieval.

**Sentence.** Split on sentence boundaries. One sentence per chunk or a window of N sentences. Matches semantic chunking up to ~5k tokens at a fraction of the cost.
> **Sentence.** Split on sentence boundaries. One sentence per chunk or a window of N sentences. Matches semantic chunking up to ~5k tokens at a fraction of the cost.

**Parent-document.** Store small child chunks for retrieval *and* the larger parent chunk for context. Retrieve by child; return parent. Degrades gracefully: bad child chunks still return reasonable parents.
> **Parent-document.** Store small child chunks for retrieval *and* the larger parent chunk for context. Retrieve by child; return parent. Degrades gracefully: bad child chunks still return reasonable parents.

**Late chunking (2024).** Embed the whole document at the token level first, then pool token embeddings into chunk embeddings. Preserves cross-chunk context. Works with long-context embedders (BGE-M3, Jina v3). Higher compute.
> **Late chunking (2024).** Embed the whole document at the token level first, then pool token embeddings into chunk embeddings. Preserves cross-chunk context. Works with long-context embedders (BGE-M3, Jina v3). Higher compute.

**Contextual retrieval (Anthropic, 2024).** Prepend each chunk with an LLM-generated summary of its position in the document ("This chunk is section 3.2 of the termination clauses..."). 35-50% retrieval improvement in Anthropic's own benchmark. Expensive to index.
> **Contextual retrieval (Anthropic, 2024).** Prepend each chunk with an LLM-generated summary of its position in the document ("This chunk is section 3.2 of the termination clauses..."). 35-50% retrieval improvement in Anthropic's own benchmark. Expensive to index.

### The rule that beats every default
> Match the chunk size to the query type:

Match the chunk size to the query type:
> | Query type | Chunk size |
|------------|-----------|
| Factoid ("what is the CEO's name?") | 256-512 tokens |
| Analytical / multi-hop | 512-1024 tokens |
| Whole-section comprehension | 1024-2048 tokens |

| Query type | Chunk size |
|------------|-----------|
| Factoid ("what is the CEO's name?") | 256-512 tokens |
| Analytical / multi-hop | 512-1024 tokens |
| Whole-section comprehension | 1024-2048 tokens |
> NVIDIA's 2026 benchmark. The chunk should be big enough to contain the answer plus local context, small enough that the retriever's top-K returns focus on the answer rather than context noise.

NVIDIA's 2026 benchmark. The chunk should be big enough to contain the answer plus local context, small enough that the retriever's top-K returns focus on the answer rather than context noise.

> **【拓展：大语言模型的工程实践】** 从 GPT 到 ChatGPT，NLP 领域经历了从 "每个任务训练一个模型" 到 "一个模型解决所有任务" 的范式转变。在实际工程中，LLM 的部署需要考虑 Token 限制、延迟、成本、安全审查等问题。LangChain、LlamaIndex 等框架简化了 LLM 应用的开发。

> **【拓展：RAG 与企业知识库】** 检索增强生成（RAG）是当前企业 AI 应用最流行的架构：将用户查询先检索相关文档片段，再将检索结果作为上下文喂给 LLM 生成答案。这种方式解决了 LLM 知识过时和幻觉问题。向量数据库（如 Milvus、Pinecone、Weaviate）是 RAG 系统的核心组件。

> **【拓展：NLP 的多语言挑战】** 全球有 7000+ 种语言，但 NLP 研究主要集中在英语等少数语言。跨语言迁移学习、多语言预训练模型（如 mBERT、XLM-R）是解决低资源语言 NLP 的主要方法。字节级模型（如 ByT5）甚至可以在无分词器的情况下处理任何语言。


## Build It | 动手实现

> **【中文解读】** 本节通过代码从零实现核心算法。这种 "from scratch" 的方式能帮助理解框架背后的原理，遇到问题时不会被黑盒困住。


### Step 1: fixed and recursive chunking
> Tune `threshold` on your domain. Too high → fragments. Too low → one giant chunk.

```python
def chunk_fixed(text, size=512, overlap=0):
    step = size - overlap
    return [text[i:i + size] for i in range(0, len(text), step)]


def chunk_recursive(text, size=512, seps=("\n\n", "\n", ". ", " ")):
    if len(text) <= size:
        return [text]
    for sep in seps:
        if sep not in text:
            continue
        parts = text.split(sep)
        chunks = []
        buf = ""
        for p in parts:
            if len(p) > size:
                if buf:
                    chunks.append(buf)
                    buf = ""
                chunks.extend(chunk_recursive(p, size=size, seps=seps[1:] or (" ",)))
                continue
            candidate = buf + sep + p if buf else p
            if len(candidate) <= size:
                buf = candidate
            else:
                if buf:
                    chunks.append(buf)
                buf = p
        if buf:
            chunks.append(buf)
        return [c for c in chunks if c.strip()]
    return chunk_fixed(text, size)
```

### Step 2: semantic chunking
> Key insight: dedupe parents. Multiple children can map to the same parent; returning all would waste context.

```python
def chunk_semantic(text, encoder, threshold=0.6, min_chars=200, max_chars=2048):
    sentences = split_sentences(text)
    if not sentences:
        return []
    embs = encoder.encode(sentences, normalize_embeddings=True)
    chunks = [[sentences[0]]]
    for i in range(1, len(sentences)):
        sim = float(embs[i] @ embs[i - 1])
        current_len = sum(len(s) for s in chunks[-1])
        if sim < threshold and current_len >= min_chars:
            chunks.append([sentences[i]])
        else:
            chunks[-1].append(sentences[i])

    result = []
    for group in chunks:
        text_group = " ".join(group)
        if len(text_group) > max_chars:
            result.extend(chunk_recursive(text_group, size=max_chars))
        else:
            result.append(text_group)
    return result
```

Tune `threshold` on your domain. Too high → fragments. Too low → one giant chunk.
> Index the contextualized chunks. At query time, retrieval benefits from the extra surrounding signal.

### Step 3: parent-document
> Always benchmark. The "best" strategy for your corpus may not match any blog post.

```python
def chunk_parent_child(text, parent_size=2048, child_size=256):
    parents = chunk_recursive(text, size=parent_size)
    mapping = []
    for p_idx, parent in enumerate(parents):
        children = chunk_recursive(parent, size=child_size)
        for child in children:
            mapping.append({"child": child, "parent_idx": p_idx, "parent": parent})
    return mapping


def retrieve_parent(child_query, mapping, encoder, top_k=3):
    child_embs = encoder.encode([m["child"] for m in mapping], normalize_embeddings=True)
    q_emb = encoder.encode([child_query], normalize_embeddings=True)[0]
    scores = child_embs @ q_emb
    top = np.argsort(-scores)[:top_k]
    seen, parents = set(), []
    for i in top:
        if mapping[i]["parent_idx"] not in seen:
            parents.append(mapping[i]["parent"])
            seen.add(mapping[i]["parent_idx"])
    return parents
```

Key insight: dedupe parents. Multiple children can map to the same parent; returning all would waste context.

### Step 4: contextual retrieval (Anthropic pattern)

```python
def contextualize_chunks(document, chunks, llm):
    context_prompts = [
        f"""<document>{document}</document>
Here is the chunk to situate: <chunk>{c}</chunk>
Write 50-100 words placing this chunk in the document's context."""
        for c in chunks
    ]
    contexts = llm.batch(context_prompts)
    return [f"{ctx}\n\n{c}" for ctx, c in zip(contexts, chunks)]
```

Index the contextualized chunks. At query time, retrieval benefits from the extra surrounding signal.

### Step 5: evaluate

```python
def recall_at_k(queries, corpus_chunks, encoder, k=5):
    chunk_embs = encoder.encode(corpus_chunks, normalize_embeddings=True)
    hits = 0
    for q_text, gold_idxs in queries:
        q_emb = encoder.encode([q_text], normalize_embeddings=True)[0]
        top = np.argsort(-(chunk_embs @ q_emb))[:k]
        if any(i in gold_idxs for i in top):
            hits += 1
    return hits / len(queries)
```

Always benchmark. The "best" strategy for your corpus may not match any blog post.


> **【拓展：Prompt Engineering 与 LLM 应用】** Prompt Engineering 已成为 NLP 工程师的核心技能。从 Zero-shot 到 Few-shot，从 Chain-of-Thought 到 ReAct，不同的提示策略适用于不同场景。在实际项目中，系统提示（System Prompt）的设计直接影响 LLM 应用的稳定性和输出质量。

## Pitfalls

- **Chunking evaluated only on factoid queries.** Multi-hop queries reveal very different winners. Use a query-type-stratified eval set.
- **Semantic chunking without a minimum size.** Produces 40-token fragments that hurt retrieval. Always enforce `min_tokens`.
- **Overlap as cargo cult.** 2026 studies find overlap often provides zero benefit and doubles index cost. Measure, do not assume.
- **No min/max enforcement.** Chunks of 5 tokens or 5000 tokens both break retrieval. Clamp.
- **Cross-doc chunking.** Never let a chunk span two documents. Always chunk per-doc, then merge.
> - **Chunking evaluated only on factoid queries.** Multi-hop queries reveal very different winners. Use a query-type-stratified eval set.
- **Semantic chunking without a minimum size.** Produces 40-token fragments that hurt retrieval. Always enforce `min_tokens`.
- **Overlap as cargo cult.** 2026 studies find overlap often provides zero benefit and doubles index cost. Measure, do not assume.
- **No min/max enforcement.** Chunks of 5 tokens or 5000 tokens both break retrieval. Clamp.
- **Cross-doc chunking.** Never let a chunk span two documents. Always chunk per-doc, then merge.

> **【中文解读】** 本节展示如何用成熟框架（如 PyTorch、HuggingFace 等）快速应用该技术。在实际项目中，优先使用经过验证的框架实现，可以减少 bug 并提高开发效率。


## Use It | 用框架实现

The 2026 stack:
> The 2026 stack:

| Situation | Strategy |
|-----------|----------|
| First build, unknown corpus | Recursive, 512 tokens, no overlap |
| Factoid QA | Recursive, 256-512 tokens |
| Analytical / multi-hop | Recursive, 512-1024 tokens + parent-document |
| Heavy cross-reference (contracts, papers) | Late chunking or contextual retrieval |
| Conversational / dialog corpus | Turn-level chunks + speaker metadata |
| Short utterances (tweets, reviews) | One document = one chunk |
> | Situation | Strategy |
|-----------|----------|
| First build, unknown corpus | Recursive, 512 tokens, no overlap |
| Factoid QA | Recursive, 256-512 tokens |
| Analytical / multi-hop | Recursive, 512-1024 tokens + parent-document |
| Heavy cross-reference (contracts, papers) | Late chunking or contextual retrieval |
| Conversational / dialog corpus | Turn-level chunks + speaker metadata |
| Short utterances (tweets, reviews) | One document = one chunk |

> **【中文解读】** 本节关注如何将模型部署为可用的产品。从原型到生产级系统需要考虑性能优化、错误处理、监控等多个维度。


Start with recursive 512. Measure recall@5 on a 50-query eval set. Tune from there.
> Start with recursive 512. Measure recall@5 on a 50-query eval set. Tune from there.


## Ship It | 产出物

Save as `outputs/skill-chunker.md`:
> 保存为 `outputs/skill-chunker.md`:

```markdown
---
name: chunker
description: Pick a chunking strategy, size, and overlap for a given corpus and query distribution.
version: 1.0.0
phase: 5
lesson: 23
tags: [nlp, rag, chunking]
---

Given a corpus (document types, avg length, domain) and query distribution (factoid / analytical / multi-hop), output:

1. Strategy. Recursive / sentence / semantic / parent-document / late / contextual. Reason.
2. Chunk size. Token count. Reason tied to query type.
3. Overlap. Default 0; justify if >0.
4. Min/max enforcement. `min_tokens`, `max_tokens` guards.
5. Evaluation plan. Recall@5 on 50-query stratified eval set (factoid, analytical, multi-hop).

> **【中文解读】** 练习题按照 Easy/Medium/Hard 三个难度递进。建议至少完成 Medium 级别的题目，Hard 级别适合深入研究或面试准备。


Refuse any chunking strategy without min/max chunk size enforcement. Refuse overlap above 20% without an ablation showing it helps. Flag semantic chunking recommendations without a min-token floor.
```

## Exercises | 练习题

> **【中文解读】** 术语表中的 "What people say" vs "What it actually means" 区分了日常口语和精确技术含义。在团队协作中，统一术语定义可以避免大量沟通误解。


1. **Easy.** Chunk one 20-page document with fixed(512, 0), recursive(512, 0), and recursive(512, 100). Compare chunk counts and boundary quality.
2. **Medium.** Build a 30-query eval set over 5 documents. Measure recall@5 for recursive, semantic, and parent-document. Which wins? Does it match the blog posts?
3. **Hard.** Implement contextual retrieval. Measure MRR improvement over baseline recursive. Report index cost (LLM calls) vs accuracy gain.
> 1. **Easy.** Chunk one 20-page document with fixed(512, 0), recursive(512, 0), and recursive(512, 100). Compare chunk counts and boundary quality.
2. **Medium.** Build a 30-query eval set over 5 documents. Measure recall@5 for recursive, semantic, and parent-document. Which wins? Does it match the blog posts?
3. **Hard.** Implement contextual retrieval. Measure MRR improvement over baseline recursive. Report index cost (LLM calls) vs accuracy gain.

## Key Terms | 术语速查表

| Term | What people say | What it actually means |
|------|-----------------|-----------------------|
| Chunk | A piece of a doc | Sub-document unit that gets embedded, indexed, and retrieved. |
| Overlap | Safety margin | N tokens shared between adjacent chunks; often useless in 2026 benchmarks. |
| Semantic chunking | Smart chunking | Split where adjacent-sentence embedding similarity drops. |
| Parent-document | Two-level retrieval | Retrieve small children, return larger parents. |
| Late chunking | Chunk after embedding | Embed full doc at token level, pool into chunk vectors. |
| Contextual retrieval | Anthropic's trick | LLM-generated summary prepended to each chunk before indexing. |
| Context cliff | 2500-token wall | Quality drop observed around 2.5k context tokens in RAG (Jan 2026). |
> | 术语 | 人们常说的 | 实际含义 |
|------|-----------|---------|
| Chunk | A piece of a doc | Sub-document unit that gets embedded, indexed, and retrieved. |
| Overlap | Safety margin | N tokens shared between adjacent chunks; often useless in 2026 benchmarks. |
| Semantic chunking | Smart chunking | Split where adjacent-sentence embedding similarity drops. |
| Parent-document | Two-level retrieval | Retrieve small children, return larger parents. |
| Late chunking | Chunk after embedding | Embed full doc at token level, pool into chunk vectors. |
| Contextual retrieval | Anthropic's trick | LLM-generated summary prepended to each chunk before indexing. |
| Context cliff | 2500-token wall | Quality drop observed around 2.5k context tokens in RAG (Jan 2026). |

> **【中文解读】** 延伸阅读提供了深入学习的高质量资源。这些论文和教程是该领域的经典参考文献，适合需要深入理解的读者。


## Further Reading | 延伸阅读

- [Yepes et al. / LangChain — Recursive Character Splitting docs](https://python.langchain.com/docs/how_to/recursive_text_splitter/) — the default in production.
- [Vectara (2024, NAACL 2025). Chunking configurations analysis](https://arxiv.org/abs/2410.13070) — chunking matters as much as embedding choice.
- [Jina AI — Late Chunking in Long-Context Embedding Models (2024)](https://jina.ai/news/late-chunking-in-long-context-embedding-models/) — the late chunking paper.
- [Anthropic — Contextual Retrieval](https://www.anthropic.com/news/contextual-retrieval) — 35-50% retrieval improvement with LLM-generated context prefixes.
- [NVIDIA 2026 chunk-size benchmark — Premai summary](https://blog.premai.io/rag-chunking-strategies-the-2026-benchmark-guide/) — chunk size by query type.
> - [Yepes et al. / LangChain — Recursive Character Splitting docs](https://python.langchain.com/docs/how_to/recursive_text_splitter/) — the default in production.
- [Vectara (2024, NAACL 2025). Chunking configurations analysis](https://arxiv.org/abs/2410.13070) — chunking matters as much as embedding choice.
- [Jina AI — Late Chunking in Long-Context Embedding Models (2024)](https://jina.ai/news/late-chunking-in-long-context-embedding-models/) — the late chunking paper.
- [Anthropic — Contextual Retrieval](https://www.anthropic.com/news/contextual-retrieval) — 35-50% retrieval improvement with LLM-generated context prefixes.
- [NVIDIA 2026 chunk-size benchmark — Premai summary](https://blog.premai.io/rag-chunking-strategies-the-2026-benchmark-guide/) — chunk size by query type.
