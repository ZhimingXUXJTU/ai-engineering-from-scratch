# Hybrid Memory: Vector + Graph + KV (Mem0) | 混合记忆：向量+图+KV（Mem0）

> Mem0 (Chhikara et al., 2025) treats memory as three stores in parallel — vector for semantic similarity, KV for fast fact lookup, graph for entity-relationship reasoning. A scoring layer fuses the three on retrieval. This is the 2026 production standard for external memory.

> **【中文解读】** Mem0 将记忆视为三个并行存储——向量用于语义相似性、KV 用于快速事实查找、图用于实体关系推理。一个评分层在检索时融合三者。这是 2026 年外部记忆的生产标准。

**Type:** Build | **类型:** 构建
**Languages:** Python (stdlib) | **语言:** Python (标准库)
**Prerequisites:** Phase 14 · 07 (MemGPT), Phase 14 · 08 (Letta Blocks) | **前置知识:** Phase 14 · 07 (MemGPT), Phase 14 · 08 (Letta 块)
**Time:** ~75 minutes | **时间:** ~75 分钟

## Learning Objectives | 学习目标

- Explain why a single store (vector only, graph only, KV only) is insufficient for agent memory.
  中文翻译：解释为什么单一存储（仅向量、仅图、仅 KV）不足以支撑 Agent 记忆。
- Name Mem0's three parallel stores and what each one optimizes for.
  中文翻译：说出 Mem0 的三个并行存储及各自优化的目标。
- Describe Mem0's fusion scoring — relevance, importance, recency — and why it is a weighted sum, not a hierarchy.
  中文翻译：描述 Mem0 的融合评分——相关性、重要性、时效性——以及为什么是加权和而非层级。
- Implement a toy three-store memory in stdlib with an `add()` that writes to all three and a `search()` that fuses results.
  中文翻译：用标准库实现玩具三存储记忆，`add()` 写入所有三个存储，`search()` 融合结果。

## The Problem | 问题引入

One store is wrong for one of three query classes:

> 单一存储对三类查询之一是错误的：

- **Semantic similarity** — "what did we discuss about agent drift last week?" Vector wins; KV and graph miss.
  中文翻译：**语义相似性**——"我们上周讨论了什么关于 Agent 漂移的？" 向量胜出；KV 和图遗漏。
- **Fact lookup** — "what is the user's phone number?" KV wins; vector is wasteful, graph is overkill.
  中文翻译：**事实查找**——"用户的电话号码是什么？" KV 胜出；向量浪费，图过度。
- **Relationship reasoning** — "which customers share the same billing entity?" Graph wins; vector and KV cannot answer.
  中文翻译：**关系推理**——"哪些客户共享同一计费实体？" 图胜出；向量和 KV 无法回答。

Production agents issue all three in one session. A single-store memory is always wrong for two of them. Mem0's contribution is wiring all three behind a single `add`/`search` surface with a scoring function that fuses them.

> 生产 Agent 在一次会话中发出所有三种查询。单一存储记忆对其中两种总是错误的。Mem0 的贡献是将三者连接在统一的 `add`/`search` 接口后面，并用评分函数融合它们。

> **【中文解读】** 混合记忆系统（Mem0）结合了短期工作记忆和长期持久化记忆。短期记忆存储在上下文窗口中，长期记忆使用向量数据库和图数据库。Mem0 的核心创新是自动记忆提取——从对话中自动识别需要持久化的信息并存储。

> **【拓展：Mem0 是目前最流行的 Agent 记忆解决方案之一】** Mem0 (2024-2025) 是目前最流行的 Agent 记忆解决方案之一，GitHub 25k+ stars。它的三层架构：短期记忆（上下文窗口）、长期记忆（向量 + 图数据库）、episodic 记忆（事件序列）。Mem0 的自动记忆提取能力意味着开发者不需要手动管理记忆——Agent 自动决定什么值得记住。

## The Concept | 核心概念

### Three stores in parallel

Mem0 (arXiv:2504.19413, April 2025) on `add(text, user_id, metadata)`:

> Mem0（arXiv:2504.19413，2025 年 4 月）在 `add(text, user_id, metadata)` 上：

1. Extract candidate facts from the text (an LLM-driven step).
   中文翻译：从文本中提取候选事实（LLM 驱动的步骤）。
2. Write each fact to the vector store (embedding) for semantic search.
   中文翻译：将每个事实写入向量存储（嵌入）用于语义搜索。
3. Write each fact to the KV store keyed on (user_id, fact_type, entity) for O(1) lookup.
   中文翻译：将每个事实写入 KV 存储，以 (user_id, fact_type, entity) 为键，实现 O(1) 查找。
4. Write each fact to the graph store (Mem0g) as typed edges for relationship queries.
   中文翻译：将每个事实写入图存储（Mem0g）作为类型化边，用于关系查询。

On `search(query, user_id)`:

> 在 `search(query, user_id)` 上：

1. Vector store returns top-k by embedding cosine.
   中文翻译：向量存储按嵌入余弦相似度返回 top-k。
2. KV store returns direct hits keyed on query-derived (user_id, type, entity).
   中文翻译：KV 存储返回基于查询推导的 (user_id, type, entity) 键的直接命中。
3. Graph store returns subgraph reachable from query entities.
   中文翻译：图存储返回从查询实体可达的子图。
4. A scoring layer fuses the three.
   中文翻译：评分层融合三者。

### Fusion scoring

```
score = w_relevance * relevance(q, record)
      + w_importance * importance(record)
      + w_recency * recency(record)
```

- **Relevance** — vector cosine, KV exact match, graph path weight.
  中文翻译：**相关性**——向量余弦、KV 精确匹配、图路径权重。
- **Importance** — tagged at write time or learned (some facts matter more: names, IDs, policies).
  中文翻译：**重要性**——写入时标记或学习得到（某些事实更重要：姓名、ID、策略）。
- **Recency** — exponential decay over time since last write or read.
  中文翻译：**时效性**——自上次写入或读取以来的时间指数衰减。

Weights are tuned per product. Higher `w_recency` for chat agents; higher `w_importance` for compliance agents; higher `w_relevance` for retrieval agents.

> 权重按产品调优。聊天 Agent 使用更高的 `w_recency`；合规 Agent 使用更高的 `w_importance`；检索 Agent 使用更高的 `w_relevance`。

### Mem0g and temporal reasoning

Mem0g adds a conflict detector. When a new fact contradicts an existing edge, the existing edge is marked invalid but not deleted. Temporal queries ("what was the user's city in March?") traverse the valid-at-time subgraph.

> Mem0g 添加了冲突检测器。当新事实与现有边矛盾时，现有边被标记为无效但不删除。时序查询（"用户三月份的城市是什么？"）遍历时间有效子图。

This is the compliance-grade behavior Letta's invalidation pattern generalizes.

> 这是 Letta 失效模式泛化的合规级行为。

### Benchmark numbers

The Mem0 paper reports (2025):

> Mem0 论文报告（2025）：

- **LoCoMo** (long-form conversation memory): 91.6
- **LongMemEval** (long-horizon episodic memory): 93.4
- **BEAM 1M** (1M-token memory benchmark): 64.1

Comparison baselines (full-context 128k LLM, flat vector store, flat KV) all lose by 10+ points. Benchmarks alone don't justify choice — operational shape does — but the numbers show the fusion design is not a rounding error.

> 比较基线（全上下文 128k LLM、扁平向量存储、扁平 KV）都落后 10+ 分。仅凭基准测试不能证明选择——运营形态才行——但数字表明融合设计不是四舍五入的误差。

### Scope taxonomy

Mem0 splits memory by scope:

> Mem0 按范围拆分记忆：

- **User memory** — persists across sessions, keyed on `user_id`.
  中文翻译：**用户记忆**——跨会话持久化，以 `user_id` 为键。
- **Session memory** — persists within one thread.
  中文翻译：**会话记忆**——在一个线程内持久化。
- **Agent memory** — per-agent instance state.
  中文翻译：**Agent 记忆**——每个 Agent 实例状态。

Every write picks one scope. Retrieval can query across scopes with per-scope weights. Mixing scopes without thought is how you get "the assistant told Alice about Bob's project" incidents.

> 每次写入选择一个范围。检索可以跨范围查询，带每个范围的权重。不经思考地混合范围会导致"助手告诉 Alice 关于 Bob 项目"的事件。

### Where this pattern goes wrong

- **Embedding drift.** Vector results that look right on the first hundred queries degrade as the corpus grows. Add periodic re-embedding of the top-N-used records.
  中文翻译：**嵌入漂移。** 前一百次查询看起来正确的向量结果随语料增长而退化。添加周期性重新嵌入 top-N 使用记录。
- **KV schema creep.** `(user_id, type, entity)` looks simple until every team adds their own `type`. Audit the type set quarterly.
  中文翻译：**KV 模式蔓延。** `(user_id, type, entity)` 看起来简单，直到每个团队添加自己的 `type`。每季度审计类型集。
- **Graph explosion.** One noisy extractor adds 50 edges per message. Cap graph writes per `add` call; drop low-confidence edges.
  中文翻译：**图爆炸。** 一个嘈杂的提取器每条消息添加 50 条边。限制每次 `add` 调用的图写入数；丢弃低置信度边。

## Build It | 动手构建

`code/main.py` implements the three-store pattern in stdlib:

> `code/main.py` 用标准库实现了三存储模式：

- `VectorStore` — naive token-overlap similarity as an embedding stand-in.
  中文翻译：`VectorStore`——用朴素 token 重叠相似性替代嵌入。
- `KVStore` — dict keyed on `(user_id, fact_type, entity)`.
  中文翻译：`KVStore`——以 `(user_id, fact_type, entity)` 为键的字典。
- `GraphStore` — typed edges (subject, relation, object, valid).
  中文翻译：`GraphStore`——类型化边（主语、关系、宾语、有效）。
- `Mem0` — top-level facade with `add()`, `search()`, fusion scoring, and scope-aware retrieval.
  中文翻译：`Mem0`——顶层门面，带 `add()`、`search()`、融合评分和范围感知检索。
- A worked trace on a multi-user, multi-session conversation.
  中文翻译：多用户、多会话对话的演练轨迹。

Run it:

> 运行：

```
python3 code/main.py
```

The output shows three separate recall paths plus the fused top-k. Flip the scoring weights at the top of `main()` and watch the ranking change.

> 输出显示三条独立的召回路径加上融合的 top-k。在 `main()` 顶部翻转评分权重观察排名变化。

## Use It | 用框架实现

- **Mem0 (Apache 2.0)** — production-ready. Self-host with Postgres + Qdrant + Neo4j, or use the managed cloud.
  中文翻译：**Mem0 (Apache 2.0)**——生产就绪。用 Postgres + Qdrant + Neo4j 自托管，或使用托管云。
- **Letta** — three-tier core/recall/archival; bring your own vector and graph backends.
  中文翻译：**Letta**——三层 core/recall/archival；自带向量和图后端。
- **Zep** — commercial alternative with temporal KG and fact extraction.
  中文翻译：**Zep**——带时序知识图谱和事实提取的商业替代方案。
- **Custom builds** — when you need exact control over the extractor (compliance) or fusion weights (voice agents where recency dominates).
  中文翻译：**自定义构建**——当你需要精确控制提取器（合规）或融合权重（时效性主导的语音 Agent）时。

## Ship It | 产出物

`outputs/skill-hybrid-memory.md` generates a three-store memory scaffold with a fusion scorer, scope taxonomy, and temporal invalidation wired in.

> `outputs/skill-hybrid-memory.md` 生成三存储记忆脚手架，内置融合评分器、范围分类和时序失效。

## Exercises | 练习题

1. Replace the toy vector similarity with a real embedding model (sentence-transformers, Ollama, OpenAI embeddings). Measure recall@10 on a synthetic long conversation. Does the ranking drift over 1000 writes?
   中文翻译：将玩具向量相似性替换为真实嵌入模型。在合成长对话上测量 recall@10。1000 次写入后排名会漂移吗？
2. Add a temporal query: `search(query, as_of=timestamp)`. Return only records valid at or before that time. Which store needs the most work?
   中文翻译：添加时序查询：`search(query, as_of=timestamp)`。仅返回该时间或之前有效的记录。哪个存储需要最多工作？
3. Implement a conflict detector: if an incoming fact contradicts a graph edge, invalidate the old edge and log both. Test on "user lives in Berlin" -> "user lives in Lisbon."
   中文翻译：实现冲突检测器：如果传入事实与图边矛盾，使旧边失效并记录两者。用"user lives in Berlin" -> "user lives in Lisbon"测试。
4. Port the fusion scorer to include a `user_feedback` dimension (thumbs-up on retrieved records). How do you prevent gaming (the agent only returns records it already liked)?
   中文翻译：将融合评分器移植为包含 `user_feedback` 维度。如何防止操纵（Agent 只返回它已经喜欢的记录）？
5. Read the Mem0 docs (`docs.mem0.ai`). Port the toy to `mem0` client calls. Compare retrieval quality on the same 20 test queries.
   中文翻译：阅读 Mem0 文档。将玩具移植为 `mem0` 客户端调用。比较相同 20 个测试查询的检索质量。

## Key Terms | 术语速查表

| Term | What people say | What it actually means |
|------|-----------------|-----------------------|
| 术语 | 通俗说法 | 实际含义 |
| Hybrid memory | "Vector plus graph plus KV" / "向量加图加 KV" | Three stores written in parallel, fused on retrieval / 三个存储并行写入，检索时融合 |
| Fact extraction | "Memory ingestion" / "记忆摄取" | LLM step that breaks text into (entity, relation, fact) tuples / 将文本拆分为（实体、关系、事实）元组的 LLM 步骤 |
| Fusion scoring | "Relevance ranking" / "相关性排序" | Weighted sum of relevance, importance, recency / 相关性、重要性、时效性的加权和 |
| Scope | "Memory namespace" / "记忆命名空间" | user / session / agent — determines who sees what / 用户/会话/Agent——决定谁看到什么 |
| Mem0g | "Memory graph" / "记忆图" | Typed edges with temporal validity for relationship queries / 带时序有效性的类型化边，用于关系查询 |
| Temporal invalidation | "Soft delete" / "软删除" | Mark contradicted edges invalid; never delete / 标记矛盾边为无效；永不删除 |
| Embedding drift | "Retrieval rot" / "检索腐化" | Vector quality degrades as corpus grows; re-embed periodically / 向量质量随语料增长退化；定期重新嵌入 |

## Further Reading | 延伸阅读

- [Chhikara et al., Mem0 (arXiv:2504.19413)](https://arxiv.org/abs/2504.19413) — the original paper
  中文翻译：Mem0 原始论文。
- [Mem0 docs](https://docs.mem0.ai/platform/overview) — production API, SDKs, managed cloud
  中文翻译：Mem0 文档——生产 API、SDK、托管云。
- [Packer et al., MemGPT (arXiv:2310.08560)](https://arxiv.org/abs/2310.08560) — the virtual-context predecessor
  中文翻译：MemGPT 论文——虚拟上下文的前身。
- [Letta, Memory Blocks blog](https://www.letta.com/blog/memory-blocks) — the three-tier sibling design
  中文翻译：Letta 记忆块博客——三层兄弟设计。
