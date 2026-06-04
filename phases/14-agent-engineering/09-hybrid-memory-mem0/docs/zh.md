# 混合记忆：向量 + 图 + KV (Mem0)

> Mem0 (Chhikara 等人, 2025) 将记忆视为三个并行存储——向量用于语义相似性、KV 用于快速事实查找、图用于实体关系推理。评分层在检索时融合三者。这是 2026 年外部记忆的生产标准。

**类型：** 构建
**语言：** Python (标准库)
**前置条件：** Phase 14 · 07 (MemGPT), Phase 14 · 08 (Letta 记忆块)
**预计时间：** ~75 分钟

## 学习目标

- 解释为什么单一存储（仅向量、仅图、仅 KV）不足以应对 Agent 记忆。
- 说出 Mem0 的三个并行存储及各自优化的目标。
- 描述 Mem0 的融合评分——相关性 (relevance)、重要性 (importance)、时效性 (recency)——以及为什么它是加权和而非层级。
- 用标准库实现玩具三层存储记忆，带写入所有三层的 `add()` 和融合结果的 `search()`。

## 问题引入

单一存储对三类查询中的一种是错误的：

- **语义相似性**——"我们上周讨论了什么关于 Agent 漂移的内容？"向量胜出；KV 和图都缺失。
- **事实查找**——"用户的电话号码是什么？"KV 胜出；向量浪费、图过度。
- **关系推理**——"哪些客户共享同一个计费实体？"图胜出；向量和 KV 无法回答。

生产 Agent 在一次会话中发出所有三种查询。单一存储记忆对其中两种总是错误的。Mem0 的贡献是在单个 `add`/`search` 面后连接所有三种，带融合评分函数。

> **【中文解读】** 混合记忆系统（Mem0）结合了短期工作记忆和长期持久化记忆。短期记忆存储在上下文窗口中，长期记忆使用向量数据库和图数据库。Mem0 的核心创新是自动记忆提取——从对话中自动识别需要持久化的信息并存储。

> **【拓展：Mem0 (2024-2025) 是目前最流行的 Agent 记忆解决方案之一，GitHub 25k+ stars。它的三层架构：短期记忆（上下文窗口）、长期记忆（向量 + 图数据库）、episodic 记忆（事件序列）。Mem0 的自动记忆提取能力意味着开发者不需要手动管理记忆——Agent 自动决定什么值得记住。**

## 核心概念

### 三个并行存储

Mem0 (arXiv:2504.19413, 2025 年 4 月) 在 `add(text, user_id, metadata)` 时：

1. 从文本中提取候选事实（LLM 驱动的步骤）。
2. 将每个事实写入向量存储（嵌入）用于语义搜索。
3. 将每个事实写入 KV 存储，键为 (user_id, fact_type, entity) 用于 O(1) 查找。
4. 将每个事实写入图存储 (Mem0g) 作为类型化边用于关系查询。

在 `search(query, user_id)` 时：

1. 向量存储返回按嵌入余弦的 top-k。
2. KV 存储返回按查询派生的 (user_id, type, entity) 键的直接命中。
3. 图存储返回从查询实体可达的子图。
4. 评分层融合三者。

### 融合评分

```
score = w_relevance * relevance(q, record)
      + w_importance * importance(record)
      + w_recency * recency(record)
```

权重按产品调整。聊天 Agent 的 `w_recency` 更高；合规 Agent 的 `w_importance` 更高；检索 Agent 的 `w_relevance` 更高。

### Mem0g 和时态推理

Mem0g 添加了冲突检测器。当新事实与现有边矛盾时，现有边被标记为失效但不删除。时态查询（"用户三月的城市是什么？"）遍历时点有效子图。

### 基准数据

Mem0 论文报告 (2025)：

- **LoCoMo**（长篇对话记忆）：91.6
- **LongMemEval**（长程情景记忆）：93.4
- **BEAM 1M**（1M token 记忆基准）：64.1

比较基线（全上下文 128k LLM、扁平向量存储、扁平 KV）都低 10+ 个百分点。

### 范围分类法

Mem0 按范围分割记忆：

- **用户记忆**——跨会话持久化，键为 `user_id`。
- **会话记忆**——在一个线程内持久化。
- **Agent 记忆**——每个 Agent 实例的状态。

### 这个模式哪里会出错

- **嵌入漂移。** 前几百次查询看起来正确的向量结果随着语料库增长而退化。定期重新嵌入使用频率最高的 N 条记录。
- **KV schema 蔓延。** `(user_id, type, entity)` 看起来简单，直到每个团队添加自己的 `type`。每季度审计类型集合。
- **图爆炸。** 一个嘈杂的提取器每条消息添加 50 条边。限制每次 `add` 调用的图写入；丢弃低置信度边。

## 动手实现

`code/main.py` 用标准库实现三层存储模式：

- `VectorStore`——作为嵌入替代的朴素 token 重叠相似度。
- `KVStore`——以 (user_id, fact_type, entity) 为键的字典。
- `GraphStore`——类型化边 (subject, relation, object, valid)。
- `Mem0`——顶层门面，带 `add()`、`search()`、融合评分和范围感知检索。

运行：

```
python3 code/main.py
```

## 用框架实现

- **Mem0 (Apache 2.0)**——生产就绪。使用 Postgres + Qdrant + Neo4j 自托管，或使用托管云。
- **Letta**——三层 core/recall/archival；自带向量和图后端。
- **Zep**——带时态知识图谱和事实提取的商业替代。
- **自定义构建**——需要精确控制提取器（合规）或融合权重（语音 Agent 其中时效性占主导）时。

## 产出物

`outputs/skill-hybrid-memory.md` 生成带融合评分器、范围分类法和时态失效连线的三层记忆脚手架。

## 练习题

1. 将玩具向量相似度替换为真实嵌入模型（sentence-transformers、Ollama、OpenAI embeddings）。在合成长对话上测量 recall@10。排名在 1000 次写入后会漂移吗？
2. 添加时态查询：`search(query, as_of=timestamp)`。只返回该时间点或之前有效的记录。哪个存储需要最多工作？
3. 实现冲突检测器：如果传入事实与图边矛盾，使旧边失效并记录两者。在"user lives in Berlin" → "user lives in Lisbon"上测试。
4. 将融合评分器移植为包含 `user_feedback` 维度（对检索到的记录点赞）。如何防止作弊（Agent 只返回它已经喜欢的记录）？
5. 阅读 Mem0 文档 (`docs.mem0.ai`)。将玩具移植为 `mem0` 客户端调用。在相同的 20 个测试查询上比较检索质量。

## 术语速查表

| 术语 | 实际含义 |
|------|---------|
| Hybrid memory（混合记忆） | 三个并行存储写入，检索时融合 |
| Fact extraction（事实提取） | 将文本拆分为 (entity, relation, fact) 元组的 LLM 步骤 |
| Fusion scoring（融合评分） | 相关性、重要性、时效性的加权和 |
| Scope（范围） | user / session / agent——决定谁看到什么 |
| Mem0g | 带时态有效性的类型化边，用于关系查询 |
| Temporal invalidation（时态失效） | 标记矛盾边为失效；永不删除 |
| Embedding drift（嵌入漂移） | 向量质量随语料库增长退化；定期重新嵌入 |

## 延伸阅读

- [Chhikara et al., Mem0 (arXiv:2504.19413)](https://arxiv.org/abs/2504.19413)
- [Mem0 docs](https://docs.mem0.ai/platform/overview)
- [Packer et al., MemGPT (arXiv:2310.08560)](https://arxiv.org/abs/2310.08560)
- [Letta, Memory Blocks blog](https://www.letta.com/blog/memory-blocks)
