# Capstone 02 — RAG over Codebase (Cross-Repo Semantic Search) | 结业 代码库 搜索 仓库 RAG

> Every serious engineering org in 2026 runs an internal code search that understands meaning, not just strings. Sourcegraph Amp, Cursor's codebase answers, Augment's enterprise graph, Aider's repomap, Pinterest's internal MCP — same shape. Ingest many repos, parse with tree-sitter, embed function- and class-level chunks, hybrid-search, re-rank, answer with citations. This capstone asks you to build one that handles 2M lines of code across 10 repos and survives incremental re-indexing on every git push.

> **【中文解读】** 本节是综合项目——构建代码库 RAG 系统，实现代码语义搜索和检索增强生成。


**Type:** Capstone
**Languages:** Python (ingestion), TypeScript (API + UI)
**Prerequisites:** Phase 5 (NLP foundations), Phase 7 (transformers), Phase 11 (LLM engineering), Phase 13 (tools), Phase 17 (infrastructure)
**Phases exercised:** P5 · P7 · P11 · P13 · P17
**Time:** 30 hours

## Problem

> **【中文解读】** 本节阐述代码检索增强生成（RAG）的核心痛点。即使 Claude 拥有 100 万 token 的上下文窗口，也无法解决跨仓库语义搜索问题——需要的是排序检索。朴素余弦搜索在生成代码、monorepo 重复和长尾符号上效果极差。生产级方案是混合搜索（稠密向量 + BM25），基于 AST 感知的分块和重排序，并依赖符号引用图。

> **【拓展：代码搜索的产业实践】** Sourcegraph Amp、Cursor Codebase Answers、Augment Enterprise Graph 等产品在 2026 年都采用相似架构。Pinterest 内部构建了 MCP 搜索服务，Aider 使用 repomap 做 tree-sitter 排序视图。关键指标包括 MRR@10（前 10 结果的倒数排名均值）、引用忠实度（答案中可验证声明的比例）和增量索引延迟（从 git push 到可搜索的时间）。对于 200 万行代码的仓库舰队，增量重索引需在 60 秒内完成。

By 2026 every frontier coding agent ships with a codebase retrieval layer because context windows alone do not solve cross-repo questions. Claude's 1M-token context helps; it does not eliminate the need for ranked retrieval. Naive cosine search over raw chunks poisons results on generated code, on monorepo duplication, and on the long tail of rarely-imported symbols. The production answer is a hybrid (dense + BM25) search over AST-aware chunks with a re-ranker, backed by a graph of symbol references.

You learn this by indexing a real fleet — not one tutorial repo — and measuring MRR@10, citation faithfulness, and incremental freshness. The failure modes are infrastructural: a 100k-file monorepo, a push that retouches half the files, a query that needs to cross four repos to answer correctly.

## Concept

> **【中文解读】** 核心概念是 AST 感知的摄取管道：用 tree-sitter 解析代码，在函数/类边界分块（而非固定 token 窗口）。每个分块生成三种表示：稠密嵌入（Voyage-code-3）、BM25 稀疏索引、自然语言摘要。检索采用混合搜索 + 交叉编码器重排序，最终由长上下文模型生成带引用的答案。增量索引只重嵌入变更分块，保持索引用于大仓库的实时性。

> **【拓展：向量数据库选型】** 2026 年主流选择：Qdrant 1.12 支持原生混合搜索，适合中等规模（< 5000 万向量）；pgvector + pgvectorscale 适合已有 PostgreSQL 基础设施的团队；Vespa 支持多向量字段和 MaxSim，适合文档级检索。嵌入模型方面，Voyage-code-3 在代码检索上领先，nomic-embed-code-v1.5 是自托管首选。重排序模型 Cohere rerank-3 或 bge-reranker-v2-gemma-2b 可将 MRR@10 提升 10-20%。

An AST-aware ingestion pipeline parses each file with tree-sitter, extracts function and class nodes, and chunks at node boundaries rather than fixed token windows. Each chunk gets three representations: a dense embedding (Voyage-code-3 or nomic-embed-code), sparse BM25 terms, and a short natural-language summary. The summary adds a third retrievable modality — users ask "how is X authorized" and the summary mentions "authz", even if the code only has `check_permission`.

Retrieval is hybrid. A query fires both dense and BM25 searches, merges top-k, and hands the union to a cross-encoder re-ranker (Cohere rerank-3 or bge-reranker-v2-gemma-2b). The re-ranked list goes to a long-context synthesizer (Claude Sonnet 4.7 with prompt caching, or Llama 3.3 70B self-hosted) with instructions to cite every claim by file and line range. Answers without citations are rejected by a post-filter.

Incremental freshness is the infrastructure problem. Git push triggers a diff: which files changed, which symbols changed. Only affected chunks re-embed. Affected cross-file symbol edges (imports, method calls) get recomputed. The index stays consistent without reprocessing 2M lines each commit.

## Architecture | 架构

```
git push --> webhook --> ingest worker (LlamaIndex Workflow)
                           |
                           v
             tree-sitter parse + AST chunk
                           |
            +--------------+----------------+
            v              v                v
          dense        BM25 index       summary (LLM)
        (Voyage / bge)  (Tantivy)        (Haiku 4.5)
            |              |                |
            +------> Qdrant / pgvector <----+
                            |
                            v
                      symbol graph (Neo4j / kuzu)
                            |
  query --> LangGraph agent (retrieve -> rerank -> synth)
                            |
                            v
                 Claude Sonnet 4.7 1M context
                            |
                            v
                 answer + file:line citations
```

## Stack

- Parsing: tree-sitter with 17 language grammars (Python, TS, Rust, Go, Java, C++, etc.)
- Dense embeddings: Voyage-code-3 (hosted) or nomic-embed-code-v1.5 (self-host), bge-code-v1 fallback
- Sparse index: Tantivy (Rust) with BM25F, field-weighted on symbol name vs body
- Vector DB: Qdrant 1.12 with hybrid search, or pgvector + pgvectorscale for teams under 50M vectors
- Chunk summary model: Claude Haiku 4.5 or Gemini 2.5 Flash, prompt-cached
- Re-ranker: Cohere rerank-3 or bge-reranker-v2-gemma-2b self-hosted
- Orchestration: LlamaIndex Workflows for ingestion, LangGraph for query agent
- Synthesizer: Claude Sonnet 4.7 (1M context) with prompt caching
- Symbol graph: Neo4j (managed) or kuzu (embedded) for import and call edges
- Observability: Langfuse spans per retrieval + synthesis step

## Build It | 动手构建

> **【中文解读】** 构建分为 9 个阶段：摄取遍历器（git push 触发 diff）、分块摘要器（Haiku 4.5 批处理）、嵌入池（Voyage-code-3 批量 128）、BM25 索引（字段加权）、符号图（Neo4j/kuzu 存储导入/调用/继承关系）、查询 Agent（LangGraph 三节点：检索-重排-合成）、引用强制（无锚点声明被过滤）、增量重索引（50 文件推送 < 60 秒）、评估（100 个标注问题测 MRR@10）。

1. **Ingestion walker.** Iterate git history on every push hook. Collect changed files. For each file, parse with tree-sitter, extract function and class nodes with their full source span. Emit chunk records `{repo, path, start_line, end_line, symbol, body}`.

2. **Chunk summarizer.** Batch chunks into Haiku 4.5 calls with prompt caching on the system preamble. Prompt: "Summarize this function in one sentence, naming its public contract and side effects." Store summary alongside the chunk.

3. **Embedding pool.** Two parallel queues: dense (Voyage-code-3 batch 128) and summary (same model, but on the summary string). Write vectors to Qdrant with payload `{repo, path, start_line, end_line, symbol, kind}`.

4. **BM25 index.** Field-weighted Tantivy index: symbol name weight 4, symbol body weight 1, summary weight 2. Enables "find the function named X" queries alongside "find the function that does X".

5. **Symbol graph.** For each chunk, record edges: imports (this file uses symbol Y from repo Z), calls (this function calls method M on class C), inheritance. Store in kuzu. Used at query time to expand retrieval across repo boundaries.

6. **Query agent.** LangGraph with three nodes. `retrieve` fires dense + BM25 in parallel, deduplicates by (repo, path, symbol). `rerank` runs the cross-encoder on top-50 and keeps top-10. `synth` calls Claude Sonnet 4.7 with the reranked chunks in context, caches the system prompt, requires file:line citations.

7. **Citation enforcement.** Parse the model output; any claim without a `(repo/path:start-end)` anchor gets flagged for re-ask or dropped. Return cited-only answer to the user.

8. **Incremental re-index.** On each webhook, compute the symbol-level diff. Only re-embed chunks whose text changed. Recompute symbol edges for chunks whose imports changed. Measure: a 50-file push re-indexed in under 60 seconds for a 2M-LOC fleet.

9. **Eval.** Label 100 cross-repo questions with gold file:line answers. Measure MRR@10, nDCG@10, citation faithfulness (fraction of claims with verifiable anchors), and p50/p99 latency.

## Use It | 使用方法

```
$ code-rag ask "how is S3 multipart abort wired into our retry budget?"
[retrieve]  12 chunks dense + 7 chunks bm25, 16 unique after dedup
[rerank]    top-5 kept (cohere rerank-3)
[synth]     claude-sonnet-4.7, cache hit rate 68%, 2.1s
answer:
  Multipart aborts are triggered by `AbortMultipartOnFail` in
  services/uploader/retry.go:122-148, which decrements the per-bucket
  retry budget defined in config/budgets.yaml:34-51 ...
  citations: [services/uploader/retry.go:122-148, config/budgets.yaml:34-51,
              libs/s3client/multipart.ts:44-61]
```

## Ship It | 部署上线

Deliverable skill `outputs/skill-codebase-rag.md`. Given a corpus of repos, it stands up the ingestion pipeline, the hybrid index, and the query agent, and returns a cited answer for any cross-repo question. Rubric:

| Weight | Criterion | How it is measured |
|:-:|---|---|
| 25 | Retrieval quality | MRR@10 and nDCG@10 on a 100-question held-out set |
| 20 | Citation faithfulness | Fraction of answer claims with verifiable file:line anchors |
| 20 | Latency and scale | p95 query latency at 10k QPS on the indexed corpus size |
| 20 | Incremental indexing correctness | Time from git push to searchable on a 50-file commit |
| 15 | UX and answer formatting | Citation clickability, snippet previews, follow-up affordance |
| **100** | | |

## Exercises | 练习题

1. Swap Voyage-code-3 for nomic-embed-code self-hosted. Measure the MRR@10 delta. Report whether the gap closes with re-ranking enabled.

2. Inject 20% generated code (LLM-produced boilerplate) into the corpus and re-evaluate. Observe retrieval poisoning. Add a "generated" flag to the payload and down-weight those hits.

3. Benchmark Qdrant hybrid search vs pgvector + pgvectorscale at your corpus size. Report p99 at batch size 1.

4. Add a sampling-based drift check: weekly, rerun the 100-question eval. Alert on MRR@10 drop > 5%.

5. Extend to cross-language symbol resolution: a Python function that calls a Go service over gRPC. Use the symbol graph to link them.

## Key Terms | 关键术语

| Term | What people say | What it actually means |
|------|-----------------|------------------------|
| AST-aware chunking | "Function-level splits" | Cutting code at tree-sitter node boundaries instead of fixed token windows |
| Hybrid search | "Dense + sparse" | Run BM25 and vector search in parallel, merge top-k, rerank |
| Cross-encoder rerank | "Second-stage rank" | Model that scores each (query, candidate) pair together, more accurate than cosine |
| Prompt caching | "Cached system prompt" | 2026 Claude / OpenAI feature that discounts repeat prefix tokens up to 90% |
| Symbol graph | "Code graph" | Edges for imports, calls, inheritance across files and repos |
| Citation faithfulness | "Grounded answer rate" | Fraction of claims a user can verify by clicking the anchor and reading the referenced span |
| Incremental re-index | "Push-to-search time" | Wall-clock from git push to the changed symbols being queryable |

## Further Reading | 延伸阅读

- [Sourcegraph Amp](https://ampcode.com) — production cross-repo code intelligence
- [Sourcegraph Cody RAG architecture](https://sourcegraph.com/blog/how-cody-understands-your-codebase) — the reference deep-dive for this capstone
- [Aider repo-map](https://aider.chat/docs/repomap.html) — tree-sitter ranked repo view
- [Augment Code enterprise graph](https://www.augmentcode.com) — commercial symbol-graph RAG
- [Qdrant hybrid search docs](https://qdrant.tech/documentation/concepts/hybrid-queries/) — reference implementation
- [Voyage AI code embeddings](https://docs.voyageai.com/docs/embeddings) — Voyage-code-3 details
- [Cohere rerank-3](https://docs.cohere.com/reference/rerank) — cross-encoder reference
- [Pinterest MCP internal search](https://medium.com/pinterest-engineering) — internal-platform reference
