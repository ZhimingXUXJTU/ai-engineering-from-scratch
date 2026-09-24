# 嵌入模型  2026年深度潜水

> Word2Vec给你一个单词的向量.现代嵌入式模型给你一个单词的向量,跨语言,稀疏,密集和多向量视图,以适合你的索引.选择错误,你的RAG检索错误的东西.
> Word2Vec 给你每一个词一个向量――现代嵌入式模型给你每一个段落一个向量,跨语言,有稀疏,密和多向量视图,大小适合你的索引――选择错误你的RAG会检查错误的东西――

> **【中文解读】**嵌入模型是RAG和语义搜索的核心.

**Type:** Learn | **类型:** 学习
**Languages:** Python | **语言:** Python
**Prerequisites:** Phase 5 · 03 (Word Embeddings), Phase 5 · 14 (IR & Search) | **前置知识:** Phase 5 · 03（词嵌入），Phase 5 · 14（信息检索）
**Time:** ~60 minutes | **时间:** ~60 分钟

## 问题 问题引入

选择2026年嵌入式意味着选择五个轴:密集对稀少对多向量,单语言对多语言,模型大小,培训目标,以及是否符合向量数据库的维度限制.

> 2026年选择嵌入意味着在五个轴上选择:密 VS 稀疏 VS 多向量、单语 VS 多语言、模型大小、训练目标、以及是否适合你的向量数据库尺寸约束――

> **【中文解读】**本节提出的问题是:如何正确理解和应用这一技术在实际工程中.

## 概念的核心概念

> **【中文解读】**本节介绍核心概念和理论基础.掌握这些概念是后续动手实现的前提.

**Dense embeddings.**单个固定尺寸向量每文本 (例如,从MiniLM的768-dim).快速进行比较,压缩良好,在向量数据库中标准.最适合一般用途检索.

> **稠密嵌入。**每文本都有一个固定的大小向量,比较快,压缩好,向量数据库标准,最适合通用检索.

**Sparse embeddings.**按词汇术语的重量 (如学到的TF-IDF).

> **稀疏嵌入。**每个词表项一个权重(如学习的TF-IDF) ――SPLADE、BM25──适合关键词密集的查询──

**Multi-vector / ColBERT.**对于每个代币,一个向量,迟到的交互评分. 更准确但更大的指数.

> **多向量 / ColBERT。**每个标志一个向量,延迟交互评分.

> **【拓展：大语言模型的工程实践】**从GPT到ChatGPT,NLP领域经历了从"每个任务训练一个模型"到"一个模型解决所有任务"的范式转变.

> **【拓展：RAG 与企业知识库】**检索增强生成 (RAG) 是当前企业人工智能应用中最流行的架构.

> **【拓展：NLP 的多语言挑战】**全球有7000多种语言,但NLP研究主要集中在英语等少数语言.

## 建立它,实现它.

> **【中文解读】**本节通过代码从零实现核心算法.
```figure
gx-matryoshka
```

## 建立它

### 步骤1:比较嵌入式模型

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

> **【中文解读】**本节展示了如何使用成熟框架快速应用该技术.

> **【拓展：Prompt Engineering 与 LLM 应用】**快速工程已成为NLP工程师的核心技能.

## 用它实现框架

> **【中文解读】**本节关注如何将模型部署为可用产品.

| Model / 模型 | Dim / 维度 | Best for / 最适合 |
|------|------|---------|
| all-MiniLM-L6-v2 | 384 | English, speed / 英语，速度 |
| paraphrase-multilingual-MiniLM-L12-v2 | 384 | Multilingual / 多语言 |
| BGE-large-en-v1.5 | 1024 | English accuracy / 英语准确率 |

## 运送它.

保存如`outputs/skill-embedding-picker.md`其他:

> 保存为`outputs/skill-embedding-picker.md`其他:

```markdown
Given requirements (language, accuracy, latency, index size), pick the right embedding model.
1. Dense vs sparse vs multi-vector.
2. Model checkpoint.
3. Dimension and index budget.
```

## 练习题

1. **Easy.**在100个查询任务中,比较MiniLM与BGE. / **简单。**在100个查询检查任务上比较MiniLM与BGE.
2. **Medium.**建立混合密集+稀疏检索. / **中等。**构建混合密+稀疏检索
3. **Hard.**调整一个嵌入模型在特定域的对. / **困难。**在特定领域对上微调嵌入模型.

## 关键词 快速查找表

| Term / 术语 | What it means / 含义 |
|------|-----------------------|
| Dense embedding（稠密嵌入） | Fixed-size vector per text. / 固定大小向量。 |
| Sparse embedding（稀疏嵌入） | One weight per vocab term. / 每个词表项一个权重。 |
| ColBERT / multi-vector | One vector per token, late interaction. / 每个 token 一个向量。 |
| Hybrid search（混合搜索） | Combine dense + sparse retrieval scores. / 结合稠密+稀疏检索。 |

## 继续阅读 继续阅读

- [MTEB Leaderboard](https://huggingface.co/spaces/mteb/leaderboard)嵌入基准. / 嵌入模型基准.
- [SPLADE](https://arxiv.org/abs/2109.10086)稀疏学习嵌入.
- [ColBERT](https://arxiv.org/abs/2004.12832) 延迟交互检索.
