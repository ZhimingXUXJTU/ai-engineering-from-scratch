# Embedding Models — The 2026 Deep Dive | 嵌入模型 — 深度解析

> Word2Vec gave you a vector per word. Modern embedding models give you a vector per passage, cross-lingual, with sparse, dense, and multi-vector views, sized to fit your index. Pick wrong and your RAG retrieves the wrong thing.
> Word2Vec 给你每个词一个向量。现代嵌入模型给你每个段落一个向量，跨语言，有稀疏、稠密和多向量视图，大小适合你的索引。选错你的 RAG 会检索到错误的东西。

> **【中文解读】** 嵌入模型是 RAG 和语义搜索的核心。

**Type:** Learn | **类型:** 学习
**Languages:** Python | **语言:** Python
**Prerequisites:** Phase 5 · 03 (Word Embeddings), Phase 5 · 14 (IR & Search) | **前置知识:** Phase 5 · 03（词嵌入），Phase 5 · 14（信息检索）
**Time:** ~60 minutes | **时间:** ~60 分钟

## The Problem | 问题引入

Choosing an embedding in 2026 means picking across five axes: dense vs sparse vs multi-vector, monolingual vs multilingual, model size, training objective, and whether it fits your vector database's dimension constraints.

> 2026 年选择嵌入意味着在五个轴上选择：稠密 vs 稀疏 vs 多向量、单语 vs 多语言、模型大小、训练目标、以及是否适合你的向量数据库维度约束。

> **【中文解读】** 本节提出的问题是：如何在实际工程中正确理解和应用这一技术。理解问题背景有助于把握技术选型的关键决策点。

## The Concept | 核心概念

> **【中文解读】** 本节介绍核心概念和理论基础。掌握这些概念是后续动手实现的前提。

**Dense embeddings.** Single fixed-size vector per text (e.g., 768-dim from MiniLM). Fast to compare, compress well, standard in vector databases. Best for general-purpose retrieval.

> **稠密嵌入。** 每个文本一个固定大小向量（如 MiniLM 的 768 维）。比较快，压缩好，向量数据库标准。最适合通用检索。

**Sparse embeddings.** One weight per vocabulary term (like a learned TF-IDF). SPLADE, BM25. Good for keyword-heavy queries.

> **稀疏嵌入。** 每个词表项一个权重（如学习的 TF-IDF）。SPLADE、BM25。适合关键词密集的查询。

**Multi-vector / ColBERT.** One vector per token, late interaction scoring. More accurate but larger index.

> **多向量 / ColBERT。** 每个 token 一个向量，延迟交互评分。更准确但索引更大。

> **【拓展：大语言模型的工程实践】** 从 GPT 到 ChatGPT，NLP 领域经历了从 "每个任务训练一个模型" 到 "一个模型解决所有任务" 的范式转变。

> **【拓展：RAG 与企业知识库】** 检索增强生成（RAG）是当前企业 AI 应用最流行的架构。

> **【拓展：NLP 的多语言挑战】** 全球有 7000+ 种语言，但 NLP 研究主要集中在英语等少数语言。

## Build It | 动手实现

> **【中文解读】** 本节通过代码从零实现核心算法。

### Step 1: comparing embedding models

```python
from sentence_transformers import SentenceTransformer
import numpy as np

models = {
    "MiniLM": "sentence-transformers/all-MiniLM-L6-v2",
    "multilingual": "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2",
}

query = "What is attention in transformers?"
docs = ["Self-attention computes weighted sums of values.", "The cat sat on the mat."]

for name, model_id in models.items():
    model = SentenceTransformer(model_id)
    q_emb = model.encode([query], normalize_embeddings=True)
    d_embs = model.encode(docs, normalize_embeddings=True)
    sims = (d_embs @ q_emb.T).flatten()
    print(f"{name}: {list(zip(docs, sims.round(3)))}")
```

> **【中文解读】** 本节展示如何用成熟框架快速应用该技术。

> **【拓展：Prompt Engineering 与 LLM 应用】** Prompt Engineering 已成为 NLP 工程师的核心技能。

## Use It | 用框架实现

> **【中文解读】** 本节关注如何将模型部署为可用的产品。

| Model / 模型 | Dim / 维度 | Best for / 最适合 |
|------|------|---------|
| all-MiniLM-L6-v2 | 384 | English, speed / 英语，速度 |
| paraphrase-multilingual-MiniLM-L12-v2 | 384 | Multilingual / 多语言 |
| BGE-large-en-v1.5 | 1024 | English accuracy / 英语准确率 |

## Ship It | 产出物

Save as `outputs/skill-embedding-picker.md`:

> 保存为 `outputs/skill-embedding-picker.md`：

```markdown
Given requirements (language, accuracy, latency, index size), pick the right embedding model.
1. Dense vs sparse vs multi-vector.
2. Model checkpoint.
3. Dimension and index budget.
```

## Exercises | 练习题

1. **Easy.** Compare MiniLM vs BGE on a 100-query retrieval task. / **简单。** 在 100 查询检索任务上比较 MiniLM vs BGE。
2. **Medium.** Build hybrid dense+sparse retrieval. / **中等。** 构建混合稠密+稀疏检索。
3. **Hard.** Fine-tune an embedding model on domain-specific pairs. / **困难。** 在领域特定对上微调嵌入模型。

## Key Terms | 术语速查表

| Term / 术语 | What it means / 含义 |
|------|-----------------------|
| Dense embedding（稠密嵌入） | Fixed-size vector per text. / 固定大小向量。 |
| Sparse embedding（稀疏嵌入） | One weight per vocab term. / 每个词表项一个权重。 |
| ColBERT / multi-vector | One vector per token, late interaction. / 每个 token 一个向量。 |
| Hybrid search（混合搜索） | Combine dense + sparse retrieval scores. / 结合稠密+稀疏检索。 |

## Further Reading | 延伸阅读

- [MTEB Leaderboard](https://huggingface.co/spaces/mteb/leaderboard) — embedding benchmarks. / 嵌入模型基准。
- [SPLADE](https://arxiv.org/abs/2109.10086) — sparse learned embeddings. / 稀疏学习嵌入。
- [ColBERT](https://arxiv.org/abs/2004.12832) — late interaction retrieval. / 延迟交互检索。
