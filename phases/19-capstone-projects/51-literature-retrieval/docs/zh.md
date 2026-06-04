# Literature Retrieval | 文献 检索

> A hypothesis is cheap. Knowing whether someone already proved it is the expensive part. Build the retrieval layer that answers that question before the runner spins up a sandbox.

> **【中文解读】** 本节是综合项目——实现文献检索。


**类型：** 构建
**语言：** Python
**前置知识：** Phase 19 Track A lessons 20-29
**预计时间：** ~90 minutes

## Learning Objectives | 学习目标
- Model a small paper record with the fields the loop will read downstream.
- Build a BM25 index over abstracts with stdlib data structures only.
- Walk a citation graph to surface papers the lexical search missed.
- Deduplicate hits across the lexical and graph passes by stable paper id.
- Wrap two mock external APIs behind a single client so the upstream call site stays the same when real endpoints land.

## Why two retrieval passes

> **【中文解读】** 关键词搜索覆盖大多数词汇匹配，但遗漏两种情况：基础论文使用不同词汇（如搜索"sparse attention"错过了标题为"block selection in transformer routing"的论文），以及相关论文是已知锚点的后续引用。本课构建两阶段检索：BM25 词汇搜索 + 引用图谱遍历（1-2 跳），合并去重后按综合分数排序。

> **【拓展：学术检索在 AI 科研自动化中的应用】** Semantic Scholar 的推荐系统使用类似的混合检索策略：词汇匹配 + 引用图谱 + 知识图谱。Sakana AI 的 "The AI Scientist" 使用 Semantic Scholar API 进行文献检索。Google Scholar 的 PageRank 变体（称为 ScholarRank）也结合了引用网络拓扑和文本相似度。本课从零构建的 BM25 + 引用图谱组合是这些工业系统的核心简化版本。

A keyword search over abstracts returns papers that share vocabulary with the query. That covers most of the surface. It misses two cases. The first is when the foundational paper uses different vocabulary; for example a query for "sparse attention" misses a paper titled "block selection in transformer routing." The second is when the relevant paper is a follow up that cites a known anchor; it is more efficient to find the anchor and walk forward than to brute force the abstract pool.

The lesson builds both passes. BM25 over abstracts catches the lexical hits. A citation graph traversal expands a seed set forward and backward by one or two hops. The union is deduplicated by paper id and ranked by a small combined score.

## The Paper shape

> **【拓展：学术知识图谱在 AI 科研中的价值】** Semantic Scholar 的知识图谱包含 2 亿+ 论文、20 亿+ 引用关系。它不仅支持关键词检索，还支持：1）TLDR 自动摘要；2）影响力预测；3）研究趋势检测。本课的 Paper 结构是 Semantic Scholar 论文记录的教育性简化——同样的字段（id、title、abstract、references、citations），更小的规模。

```text
Paper
  id          : str           (stable identifier, "p001" for the mock corpus)
  title       : str
  abstract    : str
  year        : int
  authors     : list[str]
  references  : list[str]     (paper ids this paper cites)
  citations   : list[str]     (paper ids that cite this paper)
  source      : str           (which mock api supplied it, "arxiv" or "s2")
```

The references and citations fields form the directed citation graph. The two mock APIs return overlapping but not identical fields, so the corpus loader unions them on `id`.

## 架构 | 架构

```mermaid
flowchart TD
    Q[query string] --> A[arxiv mock client]
    Q --> S[semantic scholar mock client]
    A --> L[load corpus]
    S --> L
    L --> B[bm25 index]
    L --> G[citation graph]
    Q --> B
    B --> R1[lexical hits]
    R1 --> H[expand hops 1 to 2]
    G --> H
    H --> R2[graph hits]
    R1 --> M[merge and dedup]
    R2 --> M
    M --> O[ranked paper list]
```

The retrieval client owns both passes and the merge. The caller hands it a query and gets back a ranked list where each entry carries per paper score fields (`bm25_score`, `graph_distance`, `recency_score`, `final_score`) that explain the ranking.

## BM25 from scratch

> **【中文解读】** BM25 的实现使用标准 Okapi 公式，默认参数 k1=1.5, b=0.75。索引由两个字典构成：`term -> doc_frequency` 和 `term -> list of (doc_id, term_count)`。评分公式对查询词求和 `idf * tf_norm`，其中 tf_norm 包含文档长度归一化。分词器只做小写化和非字母数字分割，不做词干提取。

The implementation is the standard Okapi BM25 with default parameters `k1=1.5`, `b=0.75`. The index is two dictionaries: `term -> doc_frequency` and `term -> list of (doc_id, term_count)`. The document length is the token count of the abstract. The average document length is computed once at index build time. Scoring a query is a sum over query terms of `idf * tf_norm` where `tf_norm` is the standard BM25 length normalised term frequency.

The tokeniser is `lower` then split on non alphanumeric. It is not stemmed. A production system would swap in a small stemmer. The interface stays the same.

```text
idf(t)      = log((N - df + 0.5) / (df + 0.5) + 1.0)
tf_norm(t)  = (f * (k1 + 1)) / (f + k1 * (1 - b + b * dl / avgdl))
score(d, q) = sum over t in q of idf(t) * tf_norm(t)
```

## Citation graph traversal

> **【中文解读】** 引用图谱从语料库一次性构建。前向边从论文指向其参考文献，后向边从论文指向引用它的论文。遍历是从 BM25 命中种子出发的广度优先搜索，限制 2 跳。一跳太浅，三跳在连通图上爆炸且容易偏离主题。跳数限制是可配置的。

The graph is built once from the corpus. Forward edges go from a paper to its references. Backward edges go from a paper to its citations. The traversal is a breadth first search seeded by the top BM25 hits, capped at two hops.

Two hops is a deliberate ceiling. One hop is too shallow; the agent often wants the immediate ancestor or descendant. Three hops blows up the result size on a connected graph and tends to drift off topic. The lesson exposes the hop limit as a config knob so a downstream loop can tighten it.

## Dedup and ranking

> **【中文解读】** 两阶段检索返回重叠集合，合并以论文 id 为键去重。最终分数是三个加权和：归一化 BM25 分数（权重 0.5）、图谱分数（直接命中 1.0，一跳 0.6，两跳 0.3，权重 0.3）、时效分数（年份线性插值，权重 0.2）。权重可配置，过时话题可降低时效权重，快速发展的领域可提高。

> **【拓展：混合检索在 RAG 系统中的应用】** 本课的 BM25 + 图谱混合检索策略与 RAG（Retrieval-Augmented Generation）系统中的混合检索异曲同工。Pinecone 和 Weaviate 等向量数据库都支持"关键词 + 语义向量"混合搜索。在学术 RAG 系统中，论文引用图谱作为结构化知识源，比纯向量搜索更擅长发现间接相关的文献。

The two passes return overlapping sets. The merge keys on paper id. For each paper the final score is a weighted blend.

```text
final_score = w_bm25 * bm25_score_norm
            + w_graph * graph_score
            + w_recency * recency_score
```

`bm25_score_norm` is the BM25 score divided by the maximum BM25 score in the merged set (so the field lives in zero to one). `graph_score` is one for direct lexical hits, then `0.6` for one hop, `0.3` for two hops, zero otherwise. `recency_score` is a linear ramp from zero at the corpus minimum year to one at the maximum.

Default weights are `0.5`, `0.3`, `0.2`. The weights are config; a stale topic might tune recency down while a fast moving topic raises it.

## Mock corpus

The corpus is one hundred papers, generated by `build_corpus()`. Each paper has a hand written title and abstract on one of five topics: attention sparsity, retrieval augmentation, low rank adapters, dataset distillation, and evaluation harnesses. References and citations are wired so each topic forms a connected sub graph with a few cross topic edges.

The two mock API clients (`ArxivMockClient`, `SemanticScholarMockClient`) read from the same corpus but expose different fields. Arxiv returns title, abstract, year, authors. Semantic Scholar adds references and citations. The retrieval client unions on id; cross client field disagreement handling is deferred to a follow up lesson.

## What lessons 52 and 53 read

The runner in lesson fifty-two reads `paper.id`, `paper.title`, and the top three sentences of the abstract as context for the experiment. The evaluator in lesson fifty-three reads `paper.year` and `paper.references` to attribute a baseline to a specific paper.

The retrieval client returns a `RetrievalResult` with both the ranked list and the per query metrics: hit count, average score, top score, total wall time. The runner logs these so a downstream observability pass can plot quality over time.

## 如何阅读代码

`code/main.py` defines `Paper`, `ArxivMockClient`, `SemanticScholarMockClient`, `BM25Index`, `CitationGraph`, `RetrievalClient`, and a deterministic demo. The mock clients and the corpus are in the same file so the lesson stays portable. The BM25 implementation is one class, sixty lines. The graph traversal is one method.

`code/tests/test_retrieval.py` covers the lexical path, the graph path, the merge, the dedup, and the empty query.

## Where this slots in

Lesson fifty produces a hypothesis. Lesson fifty-one searches the literature to see whether that hypothesis is already settled. Lesson fifty-two runs the experiment if it is not. Lesson fifty-three reads both the retrieval result and the experiment metrics to write the verdict. The retrieval client is the cheapest of the four stages and runs first in the orchestrator.
