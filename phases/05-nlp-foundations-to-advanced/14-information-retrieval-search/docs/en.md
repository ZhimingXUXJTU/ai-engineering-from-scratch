# Information Retrieval and Search | 信息检索与搜索

> BM25 is precise but brittle. Dense casts a wide net but misses keywords. Hybrid is the 2026 default. Everything else is tuning.

> **【中文解读】** 从关键词匹配到向量检索。RAG 的检索器就是信息检索的应用。

**Type:** Build | **类型:** 动手
**Languages:** Python | **语言:** Python
**Prerequisites:** Phase 5 · 02 (BoW + TF-IDF), Phase 5 · 04 (GloVe, FastText, Subword) | **前置知识:** Phase 5 · 02 (BoW + TF-IDF), Phase 5 · 04 (GloVe, FastText, Subword)
**Time:** ~75 minutes | **时间:** ~75 minutes


## The Problem | 问题引入

The user types "what happens if someone lies to get money" and expects to find the statute that actually covers that: "Section 420 IPC." A keyword search misses it entirely (no shared vocabulary). A semantic search misses it if the embeddings were not trained on legal text. Real search has to handle both.
> 用户输入 "what happens if someone lies to get money" 并期望找到实际覆盖该内容的法规："Section 420 IPC"。关键词搜索完全找不到它（没有共享词汇）。如果嵌入没有在法律文本上训练过，语义搜索也会错过它。真正的搜索必须同时处理两者。

> **【中文解读】** 本节提出的问题是：如何在实际工程中正确理解和应用这一技术。理解问题背景有助于把握技术选型的关键决策点。在实际 AI 系统中，错误的技术选型往往比实现细节的 bug 代价更高。


IR is the pipeline under every RAG system, every search bar, every docs site's fuzzy lookup. The 2026 architecture that works in production is not a single method. It is a chain of complementary methods, each catching the failures of the one before.
> IR 是每个 RAG 系统、每个搜索栏、每个文档站点模糊查找底下的流水线。2026 年在生产中有效的架构不是单一方法。它是一串互补方法的链条，每个捕获前一个的失败。

This lesson builds each piece and names which failures each catches.
> 本课构建每个部分并指出各自捕获了哪些失败。

> **【中文解读】** 本节介绍核心概念和理论基础。掌握这些概念是后续动手实现的前提，同时也是面试和工程实践中高频考察的知识点。


## The Concept | 核心概念

![Hybrid retrieval: BM25 + dense + RRF + cross-encoder rerank](../assets/retrieval.svg)
> ![混合检索：BM25 + 稠密 + RRF + 交叉编码器重排序](../assets/retrieval.svg)

Four layers. Pick the ones you need.
> 四层。选择你需要的。

1. **Sparse retrieval (BM25).** Fast, precise on exact matches, terrible on semantics. Run over an inverted index. Sub-10ms per query on millions of documents. Gets you statute references, product codes, error messages, named entities right.
2. **Dense retrieval.** Encode query and documents into vectors. Nearest neighbor search. Captures paraphrases and semantic similarity. Misses exact keyword matches that differ by one character. 50-200ms per query with FAISS or a vector DB.
3. **Fusion.** Merge the ranked lists from sparse and dense. Reciprocal Rank Fusion (RRF) is the easy default because it ignores raw scores (which live in different scales) and only uses rank positions. Weighted fusion is an option when you know one signal dominates for your domain.
4. **Cross-encoder rerank.** Take the top-30 from fusion. Run a cross-encoder (query + document together, scoring each pair). Keep the top-5. Cross-encoders are slower per pair than bi-encoders but far more accurate. You amortize by only running them on the top-30.
> 1. **稀疏检索（BM25）。** 快速、精确匹配准确、语义上糟糕。在倒排索引上运行。百万文档上每查询亚 10 毫秒。正确处理法规引用、产品代码、错误消息、命名实体。
2. **稠密检索。** 将查询和文档编码为向量。最近邻搜索。捕获释义和语义相似性。遗漏差一个字符的精确关键词匹配。使用 FAISS 或向量数据库每查询 50-200 毫秒。
3. **融合。** 合并稀疏和稠密的排序列表。倒数排名融合（Reciprocal Rank Fusion, RRF）是简单的默认选择，因为它忽略原始分数（存在于不同尺度）只使用排名位置。当你知道某个信号在你的领域占主导时，加权融合是一个选项。
4. **交叉编码器重排序。** 从融合中取 top-30。运行交叉编码器（查询 + 文档一起，对每对打分）。保留 top-5。交叉编码器每对比双编码器慢但准确得多。你只在 top-30 上运行来摊销成本。

Three-way retrieval (BM25 + dense + learned-sparse like SPLADE) outperforms two-way in 2026 benchmarks but needs infrastructure for learned-sparse indexes. For most teams, two-way plus cross-encoder rerank is the sweet spot.
> 三路检索（BM25 + 稠密 + 学习稀疏如 SPLADE）在 2026 年基准上优于两路，但需要学习稀疏索引的基础设施。对大多数团队来说，两路加交叉编码器重排序是最佳平衡点。

> **【拓展：大语言模型的工程实践】** 从 GPT 到 ChatGPT，NLP 领域经历了从 "每个任务训练一个模型" 到 "一个模型解决所有任务" 的范式转变。在实际工程中，LLM 的部署需要考虑 Token 限制、延迟、成本、安全审查等问题。LangChain、LlamaIndex 等框架简化了 LLM 应用的开发。

> **【拓展：RAG 与企业知识库】** 检索增强生成（RAG）是当前企业 AI 应用最流行的架构：将用户查询先检索相关文档片段，再将检索结果作为上下文喂给 LLM 生成答案。这种方式解决了 LLM 知识过时和幻觉问题。向量数据库（如 Milvus、Pinecone、Weaviate）是 RAG 系统的核心组件。

> **【拓展：NLP 的多语言挑战】** 全球有 7000+ 种语言，但 NLP 研究主要集中在英语等少数语言。跨语言迁移学习、多语言预训练模型（如 mBERT、XLM-R）是解决低资源语言 NLP 的主要方法。字节级模型（如 ByT5）甚至可以在无分词器的情况下处理任何语言。


## Build It | 动手实现

> **【中文解读】** 本节通过代码从零实现核心算法。这种 "from scratch" 的方式能帮助理解框架背后的原理，遇到问题时不会被黑盒困住。


### Step 1: BM25 from scratch
> 两个参数值得了解。`k1=1.5` 控制词频饱和；更高意味着词重复的权重更大。`b=0.75` 控制长度归一化；0 忽略文档长度，1 完全归一化。默认值是 Robertson 原始论文中的推荐值，很少需要调整。

```python
import math
import re
from collections import Counter

TOKEN_RE = re.compile(r"[a-z0-9]+")


def tokenize(text):
    return TOKEN_RE.findall(text.lower())


class BM25:
    def __init__(self, corpus, k1=1.5, b=0.75):
        if not corpus:
            raise ValueError("corpus must not be empty")
        self.corpus = [tokenize(d) for d in corpus]
        self.k1 = k1
        self.b = b
        self.n_docs = len(self.corpus)
        self.avg_dl = sum(len(d) for d in self.corpus) / self.n_docs
        self.df = Counter()
        for doc in self.corpus:
            for term in set(doc):
                self.df[term] += 1

    def idf(self, term):
        n = self.df.get(term, 0)
        return math.log(1 + (self.n_docs - n + 0.5) / (n + 0.5))

    def score(self, query, doc_idx):
        q_tokens = tokenize(query)
        doc = self.corpus[doc_idx]
        dl = len(doc)
        freq = Counter(doc)
        score = 0.0
        for term in q_tokens:
            f = freq.get(term, 0)
            if f == 0:
                continue
            numerator = f * (self.k1 + 1)
            denominator = f + self.k1 * (1 - self.b + self.b * dl / self.avg_dl)
            score += self.idf(term) * numerator / denominator
        return score

    def rank(self, query, top_k=10):
        scored = [(self.score(query, i), i) for i in range(self.n_docs)]
        scored.sort(reverse=True)
        return scored[:top_k]
```

Two parameters worth knowing. `k1=1.5` controls term-frequency saturation; higher means more weight on term repetition. `b=0.75` controls length normalization; 0 ignores document length, 1 fully normalizes. The defaults are Robertson's recommendations from the original paper and rarely need tuning.
> L2 归一化嵌入使点积等于余弦。`all-MiniLM-L6-v2` 是 384 维，快速，对大多数英语检索足够强。多语言工作使用 `paraphrase-multilingual-MiniLM-L12-v2`。最高准确率使用 `bge-large-en-v1.5` 或 `e5-large-v2`。

### Step 2: dense retrieval with a bi-encoder
> `k=60` 常数来自原始 RRF 论文。更高的 `k` 使排名差异的贡献变平；更低的 `k` 使顶部排名主导。60 是已发布的默认值，很少需要调整。

```python
from sentence_transformers import SentenceTransformer
import numpy as np


def build_dense_index(corpus, model_id="sentence-transformers/all-MiniLM-L6-v2"):
    encoder = SentenceTransformer(model_id)
    embeddings = encoder.encode(corpus, normalize_embeddings=True)
    return encoder, embeddings


def dense_search(encoder, embeddings, query, top_k=10):
    q_emb = encoder.encode([query], normalize_embeddings=True)
    sims = (embeddings @ q_emb.T).flatten()
    order = np.argsort(-sims)[:top_k]
    return [(float(sims[i]), int(i)) for i in order]
```

L2-normalize embeddings so dot product equals cosine. `all-MiniLM-L6-v2` is 384-dim, fast, and strong enough for most English retrieval. For multilingual work, use `paraphrase-multilingual-MiniLM-L12-v2`. For top accuracy, `bge-large-en-v1.5` or `e5-large-v2`.
> 三阶段组合。BM25 找到词汇匹配。稠密找到语义匹配。RRF 合并两个排名而不需要分数校准。交叉编码器使用查询-文档对重新对 top-30 打分，捕获双编码器遗漏的细粒度相关性。保留 top-5。

### Step 3: Reciprocal Rank Fusion
> | 指标 | 含义 |
|------|------|
| Recall@k | 存在正确文档的查询中，正确文档在 top-k 中的比例 |
| MRR（平均倒数排名） | 第一个相关文档的 1/rank 的平均值 |
| nDCG@k | 考虑相关性分级，而非仅仅是二元的 相关/不相关 |

```python
def reciprocal_rank_fusion(rankings, k=60):
    scores = {}
    for ranking in rankings:
        for rank, (_, doc_idx) in enumerate(ranking):
            scores[doc_idx] = scores.get(doc_idx, 0.0) + 1.0 / (k + rank + 1)
    fused = sorted(scores.items(), key=lambda x: x[1], reverse=True)
    return [(score, doc_idx) for doc_idx, score in fused]
```

The `k=60` constant comes from the original RRF paper. Higher `k` flattens the contribution of rank differences; lower `k` makes top ranks dominate. 60 is the published default and rarely needs tuning.
> 特别是对 RAG，检索器的 **Recall@k** 是最重要的数字。如果正确的段落不在检索集中，阅读器无法回答。

### Step 4: hybrid search + rerank
> 调试技巧：对于失败的查询，对比稀疏和稠密排名。如果一个找到正确文档而另一个没有，你有词汇不匹配（修复：添加缺失的一半）或语义歧义（修复：更好的嵌入或重排序器）。

```python
from sentence_transformers import CrossEncoder

reranker = CrossEncoder("cross-encoder/ms-marco-MiniLM-L-6-v2")


def hybrid_search(query, bm25, encoder, dense_embeddings, corpus, top_k=5, pool_size=30, reranker=reranker):
    sparse_ranking = bm25.rank(query, top_k=pool_size)
    dense_ranking = dense_search(encoder, dense_embeddings, query, top_k=pool_size)
    fused = reciprocal_rank_fusion([sparse_ranking, dense_ranking])[:pool_size]

    pairs = [(query, corpus[doc_idx]) for _, doc_idx in fused]
    scores = reranker.predict(pairs)
    reranked = sorted(zip(scores, [doc_idx for _, doc_idx in fused]), reverse=True)
    return reranked[:top_k]
```

Three stages composed. BM25 finds lexical matches. Dense finds semantic matches. RRF merges the two rankings without needing score calibration. Cross-encoder rescores the top-30 using query-document pairs together, which captures fine-grained relevance the bi-encoder missed. Keep top-5.

### Step 5: evaluation

| Metric | Meaning |
|--------|---------|
| Recall@k | Of queries where the correct document exists, how often is it in the top-k? |
| MRR (Mean Reciprocal Rank) | Average of 1/rank of first relevant document. |
| nDCG@k | Accounts for relevance gradations, not just binary relevant/not. |

For RAG specifically, **Recall@k** of the retriever is the most important number. Your reader cannot answer if the right passage is not in the retrieved set.

Debugging tip: for failing queries, diff the sparse and dense rankings. If one finds the right document and the other does not, you have a vocabulary mismatch (fix: add the missing half) or a semantic ambiguity (fix: better embeddings or a reranker).


> **【拓展：Prompt Engineering 与 LLM 应用】** Prompt Engineering 已成为 NLP 工程师的核心技能。从 Zero-shot 到 Few-shot，从 Chain-of-Thought 到 ReAct，不同的提示策略适用于不同场景。在实际项目中，系统提示（System Prompt）的设计直接影响 LLM 应用的稳定性和输出质量。

## Use It | 用框架实现

> **【中文解读】** 本节展示如何用成熟框架（如 PyTorch、HuggingFace 等）快速应用该技术。在实际项目中，优先使用经过验证的框架实现，可以减少 bug 并提高开发效率。


The 2026 stack:
> 2026 年技术栈：

| Scale | Stack |
|-------|-------|
| 1k-100k docs | In-memory BM25 + `all-MiniLM-L6-v2` embeddings + RRF. No separate DB. |
| 100k-10M docs | FAISS or pgvector for dense + Elasticsearch / OpenSearch for BM25. Run in parallel. |
| 10M+ docs | Qdrant / Weaviate / Vespa / Milvus with hybrid support. Cross-encoder rerank on top-30. |
| Best-quality frontier | Three-way (BM25 + dense + SPLADE) + ColBERT late-interaction reranking |
> | 规模 | 技术栈 |
|------|--------|
| 1k-100k 文档 | 内存中 BM25 + `all-MiniLM-L6-v2` 嵌入 + RRF。无需独立数据库。 |
| 100k-10M 文档 | FAISS 或 pgvector 做稠密 + Elasticsearch / OpenSearch 做 BM25。并行运行。 |
| 10M+ 文档 | Qdrant / Weaviate / Vespa / Milvus 配混合支持。交叉编码器重排序 top-30。 |
| 最高质量前沿 | 三路（BM25 + 稠密 + SPLADE）+ ColBERT 后期交互重排序 |

Whatever you pick, budget for evaluation. Benchmark retrieval recall before benchmarking end-to-end RAG accuracy. A reader cannot fix what the retriever missed.
> 无论选择什么，都要为评估做预算。在基准端到端 RAG 准确率之前先基准检索召回率。阅读器无法修复检索器遗漏的内容。

### The hard-won lessons from 2026 production RAG
> - **80% 的 RAG 失败追溯到摄取和分块，而不是模型。** 团队花几周交换 LLM 和调优提示，而检索每三次查询就安静地返回错误的上下文。先修复分块。
- **分块策略比分块大小更重要。** 固定大小分割会破坏表格、代码和嵌套标题。句子感知是默认选择；语义或基于 LLM 的分块在技术文档和产品手册上有回报。
- **父文档模式。** 检索小的 "子" 块以获得精确度。当同一父节的多个子块出现时，换入父块以保留上下文。这持续提升答案质量而无需重新训练。
- **k_rerank=3 通常最优。** 每增加一个块超过这个数都会增加 token 成本和生成延迟而不提升答案质量。如果 k=8 仍然比 k=3 好，说明重排序器表现不足。
- **HyDE / 查询扩展。** 从查询生成假设答案，嵌入它，检索。弥合短问题和长文档之间的表述差距。无需训练即可免费提升精确率。
- **上下文预算控制在 8K token 以下。** 在该限制下持续命中意味着重排序器阈值太松。
- **版本化一切。** 提示、分块规则、嵌入模型、重排序器。任何漂移都会静默破坏答案质量。忠实度、上下文精确率和未回答问题率上的 CI 门控在用户看到之前阻止回归。
- **三路检索（BM25 + 稠密 + 学习稀疏如 SPLADE）在 2026 年基准上优于两路**，特别是混合专有名词和语义的查询。当基础设施支持 SPLADE 索引时发布它。

- **80% of RAG failures trace to ingestion and chunking, not the model.** Teams spend weeks swapping LLMs and tuning prompts while the retrieval quietly returns the wrong context every third query. Fix chunking first.
- **Chunking strategy matters more than chunk size.** Fixed-size splits break tables, code, and nested headers. Sentence-aware is the default; semantic or LLM-based chunking pays off for technical docs and product manuals.
- **Parent-doc pattern.** Retrieve small "child" chunks for precision. When multiple children from the same parent section appear, swap in the parent block to preserve context. This consistently lifts answer quality without retraining.
- **k_rerank=3 is usually optimal.** Every extra chunk past that adds token cost and generation latency without lifting answer quality. If k=8 is still better than k=3 for you, the reranker is underperforming.
- **HyDE / query expansion.** Generate a hypothetical answer from the query, embed that, retrieve. Bridges the phrasing gap between short questions and long documents. Free precision lift with no training.
- **Context budget under 8K tokens.** Consistent hits at that limit mean the reranker threshold is too loose.
- **Version everything.** Prompts, chunking rules, embedding model, reranker. Any drift silently breaks answer quality. CI gates on faithfulness, context precision, and unanswered-question rate block regressions before users see them.
- **Three-way retrieval (BM25 + dense + learned-sparse like SPLADE) outperforms two-way** on 2026 benchmarks, especially for queries mixing proper nouns with semantics. Ship it when infrastructure supports SPLADE indexes.
> 根据 2026 年行业测量，正确的检索设计减少 70-90% 的幻觉。大多数 RAG 性能提升来自更好的检索，而非模型微调。

Proper retrieval design reduces hallucinations by 70-90% according to 2026 industry measurements. Most RAG performance gains come from better retrieval, not model fine-tuning.

> **【中文解读】** 本节关注如何将模型部署为可用的产品。从原型到生产级系统需要考虑性能优化、错误处理、监控等多个维度。


## Ship It | 产出物

Save as `outputs/skill-retrieval-picker.md`:
> 保存为 `outputs/skill-retrieval-picker.md`：

```markdown
---
name: retrieval-picker
description: Pick a retrieval stack for a given corpus and query pattern.
version: 1.0.0
phase: 5
lesson: 14
tags: [nlp, retrieval, rag, search]
---

Given requirements (corpus size, query pattern, latency budget, quality bar, infra constraints), output:

1. Stack. BM25 only, dense only, hybrid (BM25 + dense + RRF), hybrid + cross-encoder rerank, or three-way (BM25 + dense + learned-sparse).
2. Dense encoder. Name the specific model. Match to language(s), domain, and context length.
3. Reranker. Name the specific cross-encoder model if used. Flag that rerank adds 30-100ms latency on top-30.
4. Evaluation plan. Recall@10 is the primary retriever metric. MRR for multi-answer. Baseline first, incremental improvements measured against it.

Refuse to recommend dense-only for corpora with named entities, error codes, or product SKUs unless the user has evidence dense handles exact matches. Refuse to skip reranking for high-stakes retrieval (legal, medical) where the final top-5 decides the user's answer.
```

> **【中文解读】** 练习题按照 Easy/Medium/Hard 三个难度递进。建议至少完成 Medium 级别的题目，Hard 级别适合深入研究或面试准备。


## Exercises | 练习题

1. **Easy.** Implement `hybrid_search` above on a 500-document corpus. Test 20 queries. Compare recall at 5 between BM25-only, dense-only, and hybrid.
2. **Medium.** Add MRR calculation. For each test query with a known correct document, find the rank of the correct doc in BM25, dense, and hybrid rankings. Report the MRR for each.
3. **Hard.** Fine-tune a dense encoder on your domain using MultipleNegativesRankingLoss (Sentence Transformers). Build a training set from 500 query-document pairs. Compare pre- and post-fine-tune recall.
> 1. **简单。** 在 500 文档语料上实现上面的 `hybrid_search`。测试 20 个查询。比较 BM25-only、dense-only 和混合的 recall@5。
2. **中等。** 添加 MRR 计算。对于每个有已知正确文档的测试查询，找到正确文档在 BM25、稠密和混合排名中的位置。报告各自的 MRR。
3. **困难。** 使用 MultipleNegativesRankingLoss（Sentence Transformers）在你的领域上微调稠密编码器。从 500 个查询-文档对构建训练集。比较微调前后的召回率。

> **【中文解读】** 术语表中的 "What people say" vs "What it actually means" 区分了日常口语和精确技术含义。在团队协作中，统一术语定义可以避免大量沟通误解。


## Key Terms | 术语速查表

| Term | What people say | What it actually means |
|------|-----------------|-----------------------|
| BM25 | Keyword search | Okapi BM25. Scores documents by term frequency, IDF, and length. |
| Dense retrieval | Vector search | Encode query + doc into vectors, find nearest neighbors. |
| Bi-encoder | Embedding model | Encodes query and doc independently. Fast at query time. |
| Cross-encoder | Reranker model | Encodes query + doc together. Slow but accurate. |
| RRF | Rank fusion | Combine two rankings by summing `1/(k + rank)`. |
| Recall@k | Retrieval metric | Fraction of queries where a relevant doc is in the top-k. |
> | 术语 | 人们常说的 | 实际含义 |
|------|-----------|---------|
| BM25 | 关键词搜索 | Okapi BM25。按词频、IDF 和长度为文档打分。 |
| 稠密检索 | 向量搜索 | 将查询 + 文档编码为向量，找最近邻。 |
| 双编码器 | 嵌入模型 | 独立编码查询和文档。查询时快速。 |
| 交叉编码器 | 重排序模型 | 一起编码查询 + 文档。慢但准确。 |
| RRF | 排名融合 | 通过对 `1/(k + rank)` 求和合并两个排名。 |
| Recall@k | 检索指标 | 相关文档在 top-k 中的查询比例。 |

> **【中文解读】** 延伸阅读提供了深入学习的高质量资源。这些论文和教程是该领域的经典参考文献，适合需要深入理解的读者。


## Further Reading | 延伸阅读

- [Robertson and Zaragoza (2009). The Probabilistic Relevance Framework: BM25 and Beyond](https://www.staff.city.ac.uk/~sbrp622/papers/foundations_bm25_review.pdf) — the definitive BM25 treatment.
- [Karpukhin et al. (2020). Dense Passage Retrieval for Open-Domain QA](https://arxiv.org/abs/2004.04906) — DPR, the canonical bi-encoder.
- [Formal et al. (2021). SPLADE: Sparse Lexical and Expansion Model](https://arxiv.org/abs/2107.05720) — the learned-sparse retriever that closes the gap with dense.
- [Cormack, Clarke, Büttcher (2009). Reciprocal Rank Fusion outperforms Condorcet and individual Rank Learning Methods](https://plg.uwaterloo.ca/~gvcormac/cormacksigir09-rrf.pdf) — RRF paper.
- [Khattab and Zaharia (2020). ColBERT: Efficient and Effective Passage Search](https://arxiv.org/abs/2004.12832) — late-interaction retrieval.
> - [Robertson and Zaragoza (2009). The Probabilistic Relevance Framework: BM25 and Beyond](https://www.staff.city.ac.uk/~sbrp622/papers/foundations_bm25_review.pdf) — 权威的 BM25 处理。
- [Karpukhin et al. (2020). Dense Passage Retrieval for Open-Domain QA](https://arxiv.org/abs/2004.04906) — DPR，经典双编码器。
- [Formal et al. (2021). SPLADE: Sparse Lexical and Expansion Model](https://arxiv.org/abs/2107.05720) — 缩小与稠密差距的学习稀疏检索器。
- [Cormack, Clarke, Büttcher (2009). Reciprocal Rank Fusion outperforms Condorcet and individual Rank Learning Methods](https://plg.uwaterloo.ca/~gvcormac/cormacksigir09-rrf.pdf) — RRF 论文。
- [Khattab and Zaharia (2020). ColBERT: Efficient and Effective Passage Search](https://arxiv.org/abs/2004.12832) — 后期交互检索。
