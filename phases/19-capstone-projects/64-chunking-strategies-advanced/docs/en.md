# Chunking Strategies, Compared | 分块策略对比

> Chunking decides what your retriever can ever surface. Get the boundaries wrong and no embedding model, no reranker, no LLM can repair the damage downstream.

> **【中文解读】** 分块决定了检索器"能捞到什么"。边界切错了，下游再强的嵌入模型、重排序器、LLM 都救不回来。本课并排实现五种分块策略——固定窗口、句子、递归切分、语义聚类、结构化 Markdown 标题——在带金标答案区间的固定语料上跑 recall@k 对比，让你亲眼看到不同语料形态下谁赢谁输，以及每条策略各自注入的失败模式。

> **【拓展：分块在 RAG 产业链中的位置】** 分块是 RAG 流水线的第一站，也是被低估最深的一站：LongRAG（2024）实测仅分块策略一项就能造成 35 个百分点的检索召回绝对摆动；Anthropic 的上下文检索（Contextual Retrieval，2025）给每个块补上下文头也只是收窄而未消除差距。本课是 RAG 深入路线（64-69 课）的地基：65 课的混合检索、66 课的重排序、68 课的评测线束全都消费这里切出来的块。

> 🔗 **【前置】** 学本课前请先掌握：Phase 11 · 04（嵌入）、06（RAG 基础）、07（进阶 RAG）——嵌入与检索的上下游关系；Phase 19 Track B 基础（20-29 课）——DenseIndex 的形状来自那里。术语约定：chunking=分块、recall@k=前 k 命中率、gold span=金标答案区间。

**Type:** Build | **类型:** 构建
**Languages:** Python | **语言:** Python
**Prerequisites:** Phase 11 lessons 04 (embeddings), 06 (RAG), 07 (advanced RAG); Phase 19 Track B foundations (lessons 20-29) | **前置知识:** Phase 11 · 04（嵌入）、06（RAG）、07（进阶 RAG）；Phase 19 Track B 基础（20-29 课）
**Time:** ~90 minutes | **时间:** 约 90 分钟

## Learning Objectives | 学习目标
- Implement five chunking strategies from scratch: fixed-window, sentence, recursive-split, semantic clustering, and structural markdown headers.
  中文翻译：从零实现五种分块策略：固定窗口、句子、递归切分、语义聚类和结构化 Markdown 标题切分。
- Measure recall@k on a fixture corpus with gold-labeled answer spans and explain why one strategy wins on prose and a different strategy wins on technical documents.
  中文翻译：在带金标答案区间的固定语料上度量 recall@k，并解释为什么一种策略在散文体上赢、另一种在技术文档上赢。
- Read a chunk-length distribution and recognize the failure modes each strategy injects: orphan sentences, mid-symbol cuts, header-only chunks, semantic drift.
  中文翻译：读懂块长度分布，识别每条策略注入的失败模式：孤儿句、符号中途截断、纯标题块、语义漂移。
- Pick a default for a new corpus without running the benchmark by inspecting three properties: document type, average paragraph length, and whether the format carries explicit structure.
  中文翻译：不跑基准，只靠检查三个属性——文档类型、平均段落长度、格式是否自带显式结构——为新语料选定默认策略。

## The Problem | 问题引入

> **【中文解读】** 本节立论：切在哪里不是超参数，而是检索器召回的上限。一个问"预算中止阈值是多少"的查询，只有当包含阈值的块完整可达才能成功——固定窗口把数值从上下文里切开的那一刻，嵌入漂移、BM25 降分、重排序器看到噪声，LLM 的答案随之出错。LongRAG 的 35 个百分点摆动就是这句话的量化版。

Every RAG pipeline starts by cutting source documents into pieces small enough that an embedding model fits them and large enough that each piece carries a self-contained idea. The choice of where to cut is not a hyperparameter. It is the upper bound on what the retriever can ever return.

> 每条 RAG 流水线都从把源文档切块开始：块要小到嵌入模型装得下，又要大到每块承载一个自足的观点。在哪里切不是超参数，而是检索器所能返回内容的上限。

A query that asks "what does the budget abort threshold look like" can only succeed if the chunk that holds the abort threshold is reachable. If the fixed-window splitter cut the threshold value from the surrounding context, the embedding moves to a different cluster, the BM25 score drops, the rerankers see noise, and the answer the LLM generates is wrong. The 2024 paper "LongRAG: Enhancing Retrieval-Augmented Generation with Long-context LLMs" measured a 35 percent absolute swing in retrieval recall purely from the chunking choice. The follow-up work in 2025 on contextual chunk headers narrowed the gap but did not close it.

> 询问"预算中止阈值长什么样"的查询，只有在持有中止阈值的那块内容可达时才可能成功。如果固定窗口切分器把阈值数值从上下文中切开，嵌入就漂移到另一个聚类，BM25 得分下降，重排序器看到的是噪声，LLM 生成的答案随之出错。2024 年论文 "LongRAG: Enhancing Retrieval-Augmented Generation with Long-context LLMs" 实测：仅分块策略的选择就带来 35 个百分点的检索召回绝对摆动。2025 年关于上下文块头的后续工作收窄了差距，但没有消除。

This lesson builds five strategies side by side, runs them against a fixture corpus with gold-labeled answer spans, and lets you read the recall numbers yourself.

> 本课并排构建五种策略，在带金标答案区间的固定语料上运行，让你亲自读召回数字。

## The Concept | 核心概念

> **【中文解读】** 五种策略是一条"从盲目到聪明"的光谱：固定窗口按字符硬切（对照组）；句子切分按句界打包；递归切分按分隔符层级逐级降级；语义聚类按句子嵌入的质心漂移切；结构化 Markdown 按标题层级切。越往右越尊重语义，但对语料形态的要求也越苛刻。评测口径是 recall@k：金标答案区间与任一前 k 块有重叠记 1，否则记 0。

```mermaid
flowchart LR
  Doc[Source Document] --> S1[Fixed Window]
  Doc --> S2[Sentence]
  Doc --> S3[Recursive Split]
  Doc --> S4[Semantic Cluster]
  Doc --> S5[Structural Markdown]
  S1 --> Chunks1[Chunks]
  S2 --> Chunks2[Chunks]
  S3 --> Chunks3[Chunks]
  S4 --> Chunks4[Chunks]
  S5 --> Chunks5[Chunks]
  Chunks1 --> Index[Embedding Index]
  Chunks2 --> Index
  Chunks3 --> Index
  Chunks4 --> Index
  Chunks5 --> Index
  Index --> Eval[Recall@k vs Gold Spans]
```

### Fixed-window

The brute-force baseline. Cut every N characters. Optionally overlap so a sentence cut at position N appears whole inside the chunk that starts at position N - overlap. Fast, deterministic, terrible at boundaries. Use it as a control, not a default.

> 暴力基线。每 N 个字符切一刀。可选重叠：在位置 N 处被切断的句子会完整出现在从位置 N - overlap 开始的那块里。快、确定性、边界质量糟糕。把它当对照组用，别当默认值。

### Sentence

Split on sentence boundaries with a regex or a simple state machine. Pack one or more sentences into a chunk up to a target character budget. Stops cutting mid-word. Still cuts mid-paragraph and mid-section. The default in many early RAG pipelines and a reasonable choice for prose with no other structure.

> 用正则或简单状态机按句子边界切分。把一个或多个句子打包进块，直到目标字符预算。不会把词切成两半，但仍会在段落中间、小节中间切断。这是许多早期 RAG 流水线的默认选择，对没有其他结构的散文体是合理方案。

### Recursive split

The hierarchy strategy popularized by 2023-era libraries. Try to split on the strongest separator first (double newline, paragraph), fall back to the next (single newline), then to sentences, then to characters. The recursion terminates when the chunk fits the budget. Strong on documents that have inconsistent structure because it adapts per region.

> 由 2023 年代的库带火的层级策略。先尝试按最强分隔符（双换行、段落）切，退而求其次（单换行），再到句子，最后到字符。递归在块装进预算时终止。对结构不一致的文档很强，因为它按区域自适应。

### Semantic clustering

Embed every sentence. Cluster contiguous sentences that share a topic centroid. Cut whenever the running similarity to the centroid drops below a threshold. The boundaries reflect meaning, not characters. Slower to build and dependent on the embedding model, but resilient against documents that switch topics inside a paragraph.

> 给每个句子做嵌入。把共享主题质心的连续句子聚成一簇。一旦与质心的运行相似度跌破阈值就切一刀。边界反映的是意义而不是字符。构建更慢、依赖嵌入模型，但对段内切换主题的文档有韧性。

### Structural markdown headers

For documents that carry explicit structure (markdown, reStructuredText, RFC-style numbered sections), cut at heading boundaries. Each chunk becomes the heading plus everything underneath it down to the next heading at the same or higher level. Smallest chunks per topic, but only available when the corpus is well-formed.

> 对自带显式结构的文档（Markdown、reStructuredText、RFC 式编号小节），按标题边界切。每块 = 标题 + 其下直到同级或更高级标题之前的全部内容。每主题块最小，但只在语料格式规整时可用。

### How recall@k measures the boundary choice

A gold-labeled query carries the exact character offsets of the answer span inside the source document. After chunking, you ask: does any of the top-k chunks the retriever returned overlap the gold span? If yes, recall@k for that query is 1. If no, it is 0. Average across the query set. Run the same evaluation for each strategy and the spread shows you which boundary policy survives the corpus you have.

> 金标查询携带答案区间在源文档中的精确字符偏移。分块之后你问：检索器返回的前 k 块中是否有任何一块与金标区间重叠？有则该查询 recall@k 记 1，无则记 0，在查询集上取平均。对每条策略跑同样的评测，差距分布会告诉你哪种边界策略能在你手头的语料上活下来。

```figure
ci-chunk-boundaries
```

## Build It | 动手实现

> **【中文解读】** `code/main.py` 把五种策略实现成同签名的切分函数，配一个哈希式确定性 mock 嵌入让整条回路离线运行，`DenseIndex` 沿用 Track B 混合检索课的形状，`eval_recall` 是对比循环。跑完打印一张"策略 × k"的召回表：句子策略在结构化语料上输、结构化 Markdown 在 Markdown 语料上赢、递归切分靠自适应在混合语料上守住、语义聚类在无结构线索的散文语料上胜出。

`code/main.py` implements:

- `fixed_window(text, size, overlap)` - the baseline.
  中文翻译：`fixed_window(text, size, overlap)`——基线。
- `sentence_chunks(text, target)` - simple sentence packer.
  中文翻译：`sentence_chunks(text, target)`——简单的句子打包器。
- `recursive_split(text, separators, target)` - hierarchical recursion.
  中文翻译：`recursive_split(text, separators, target)`——层级递归。
- `semantic_chunks(text, similarity_threshold)` - centroid-based clustering on top of a deterministic mock embedding.
  中文翻译：`semantic_chunks(text, similarity_threshold)`——在确定性 mock 嵌入之上做质心聚类。
- `structural_markdown(text)` - header-aware splitter.
  中文翻译：`structural_markdown(text)`——标题感知切分器。
- `mock_embed(text, dim)` - a hash-based embedding so the loop runs offline.
  中文翻译：`mock_embed(text, dim)`——哈希式嵌入，让整条回路离线运行。
- `DenseIndex` - the same shape used in Phase 19 Track B's hybrid retrieval lesson.
  中文翻译：`DenseIndex`——与 Phase 19 Track B 混合检索课相同的形状。
- `eval_recall(strategy, corpus, queries, k)` - the comparison loop.
  中文翻译：`eval_recall(strategy, corpus, queries, k)`——对比循环。
- A `main()` that runs every strategy on the fixture corpus and prints a recall@k table.
  中文翻译：一个 `main()`：在固定语料上运行每种策略并打印 recall@k 表。

Run it:

> 运行：

```bash
python3 code/main.py
```

The output is a small table with one row per strategy and one column per k. Sentence loses on the structured fixture. Structural-markdown wins on the markdown fixture. Recursive holds its own on the mixed fixture because the recursion adapts. Semantic clustering wins on the prose fixture where there are no useful structural cues.

> 输出是一张小表：每条策略一行、每个 k 一列。句子策略在结构化语料上输；结构化 Markdown 在 Markdown 语料上赢；递归切分靠递归的自适应性在混合语料上守得住；语义聚类在没有可用结构线索的散文语料上胜出。

## Failure modes the table will not hide | 表格藏不住的失败模式

> **【中文解读】** 召回表只给数字，这五种失败模式解释数字背后的机理：孤儿句让嵌入指向错误聚类；符号中途截断让两个半截标识符各自嵌入成噪声；纯标题块是零信息块；语义漂移让一个 5000 字符的块装进太多答案、嵌入变得弥散；过期嵌入提醒你——换了嵌入模型却不重建索引，块和检索就不再配套。

**Orphan sentences.** Sentence packing produces chunks that miss the topic sentence. The embedding then points at the wrong cluster.

> **孤儿句。** 句子打包产生的块会漏掉主题句。嵌入随之指向错误的聚类。

**Mid-symbol cuts.** Fixed-window inside code or YAML will split an identifier in half. The two halves embed to noise.

> **符号中途截断。** 固定窗口在代码或 YAML 里会把标识符切成两半。两半各自嵌入成噪声。

**Header-only chunks.** Structural markdown emits a chunk containing nothing but `## Title`. Filter those out or attach the next chunk's first paragraph.

> **纯标题块。** 结构化 Markdown 会吐出只含 `## Title` 的块。把它们过滤掉，或把下一块的第一段挂上来。

**Semantic drift.** Semantic clustering under-cuts when the corpus is uniformly on topic. A 5000-character chunk packs many specific answers into one diffuse embedding. Combine semantic with a hard character cap.

> **语义漂移。** 语料通篇同一主题时语义聚类会少切。一个 5000 字符的块把许多具体答案塞进一个弥散的嵌入。把语义切分与硬字符上限组合使用。

**Stale embeddings.** Semantic clustering uses an embedding model. If you change the model, you also change the chunks. Pin the chunk model separately from the retrieval model or rebuild the index together.

> **过期嵌入。** 语义聚类依赖嵌入模型。换了模型，块也跟着变。把分块用的模型与检索用的模型分开锁定版本，或一起重建索引。

## Choosing a default without running the benchmark | 不跑基准如何选默认策略

> **【中文解读】** 三个属性定默认：文档类型、段落长度、格式是否自带显式结构。无结构散文选递归切分（目标 800 字符）；Markdown/RFC/API 文档选结构化切分；代码走 AST 感知（超纲）；长而单一主题的段落选句子切分（目标 500）；短而混杂主题的段落选语义切分（阈值 0.6）。拿不准就选递归切分——它是最强的单策略基线。

Three properties decide the default chunker for a new corpus.

> 三个属性决定新语料的默认分块器。

| Property | Value | Default |
|----------|-------|---------|
| Document type | Prose with no structure | Recursive split, target 800 |
| Document type | Markdown / RFC / API docs | Structural markdown |
| Document type | Code | AST-aware (out of scope; see Phase 19 lesson 02) |
| Paragraph length | Long, single topic | Sentence, target 500 |
| Paragraph length | Short, mixed topics | Semantic, threshold 0.6 |

When in doubt, pick recursive split. It is the strongest single-strategy baseline.

> 拿不准时选递归切分。它是最强的单策略基线。

## Use It | 用框架实现

> **【中文解读】** 三条生产纪律：上新流水线前先跑评测，别盲信库的默认策略；每次换嵌入模型或语料配比后重跑评测，赢家是随语料而变的；把策略名持久化进每个块的元数据，将来回归才能归因。

Production patterns:

- Run the eval before you ship a new pipeline; do not trust the strategy your library defaults to.
  中文翻译：上新流水线前先跑评测；不要盲信你的库默认的策略。
- Re-run the eval whenever you change the embedding model or the corpus mix; the winner is corpus-dependent.
  中文翻译：每次更换嵌入模型或语料配比都重跑评测；赢家随语料而变。
- Persist the strategy name in each chunk's metadata so you can attribute regressions later.
  中文翻译：把策略名持久化进每个块的元数据，便于日后给回归归因。

## Ship It | 产出物

The Track F end-to-end RAG system in lesson 69 uses the chunker selected here as its first stage. The eval harness in lesson 68 reads recall@k from the same shape that `eval_recall` returns in this lesson. Pick the strategy that wins on your corpus and feed it forward.

> RAG 深入路线第 69 课的端到端系统把这里选出的分块器用作第一级。第 68 课的评测线束从与 `eval_recall` 相同的返回形状读取 recall@k。选出在你语料上赢的策略，把它向后传递。

## Exercises | 练习题

1. Add a sixth strategy: token-window using `tiktoken` instead of character counts. Compare against fixed-window on the same fixture.
   中文翻译：加第六种策略：用 `tiktoken` 按 token 数而非字符数切的 token 窗口。在同一固定语料上与固定窗口对比。
2. Inject a 30 percent fraction of code blocks into the prose fixture. Re-run the table. Explain why every strategy except structural markdown loses recall.
   中文翻译：向散文语料注入 30% 的代码块。重跑表格。解释为什么除结构化 Markdown 外每条策略都掉召回。
3. Replace the deterministic embedding with the one from your project's real provider. Measure the semantic-clustering recall delta. Report whether the spread between strategies widens or narrows.
   中文翻译：把确定性嵌入换成你项目真实供应商的嵌入。度量语义聚类召回的变化。报告策略间差距是变宽还是变窄。
4. Add a `summary` field per chunk: a one-sentence centroid description. Re-run the eval with the summary appended to the chunk body. Measure the recall lift.
   中文翻译：给每块加一个 `summary` 字段：一句话质心描述。把摘要附加到块正文后重跑评测。度量召回提升。

## Key Terms | 术语速查表

| Term | What people say | What it actually means |
|------|-----------------|------------------------|
| Recall@k | "Did we get the right chunk?" | Fraction of queries where any of the top-k chunks overlaps the gold answer span |
| Chunk overlap | "Sliding window" | Re-include the last N characters of the previous chunk in the next chunk |
| Structural splitter | "Header-aware chunks" | Cut at H1/H2/H3 boundaries; the heading text is part of the chunk |
| Semantic chunker | "Topic-aware chunks" | Embed sentences, cluster by centroid similarity, cut on drift |
| Centroid drift | "Topic shift" | Cosine similarity between the running mean and the next sentence drops past a threshold |

## Further Reading | 延伸阅读

- [LongRAG: Enhancing Retrieval-Augmented Generation with Long-context LLMs (arXiv 2406.15319)](https://arxiv.org/abs/2406.15319)
  中文翻译：LongRAG 论文——分块策略造成 35 个百分点召回摆动的实测来源。
- [Anthropic, Contextual Retrieval](https://www.anthropic.com/news/contextual-retrieval)
  中文翻译：Anthropic 上下文检索——用上下文块头收窄分块差距的后续工作。
- [LlamaIndex, Chunking strategies for production RAG](https://docs.llamaindex.ai/en/stable/optimizing/production_rag/)
  中文翻译：LlamaIndex 生产 RAG 分块策略文档。
- Phase 11 lesson 06 - RAG fundamentals
  中文翻译：Phase 11 · 06——RAG 基础。
- Phase 11 lesson 07 - advanced RAG
  中文翻译：Phase 11 · 07——进阶 RAG。
- Phase 19 lesson 65 - hybrid retrieval that ranks the chunks produced here
  中文翻译：Phase 19 · 65——对本课产出的块做排序的混合检索。
- Phase 19 lesson 68 - the eval harness that scores the strategy choice in production
  中文翻译：Phase 19 · 68——在生产中给策略选择打分的评测线束。
