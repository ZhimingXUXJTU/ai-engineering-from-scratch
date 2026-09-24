# 搜索信息搜索信息搜索

> 虽然BM25是精确的,但很脆弱.密集的网投宽,但错过关键字.混合型是2026年默认的.其他一切都在调整.
> 混检索是2026年默认选择. 其余都是调参.

> **【中文解读】**从关键词匹配到向量检索.RAG的检索器就是信息检索的应用.

**Type:** Build | **类型:** 动手
**Languages:** Python | **语言:** Python
**Prerequisites:** Phase 5 · 02 (BoW + TF-IDF), Phase 5 · 04 (GloVe, FastText, Subword) | **前置知识:** Phase 5 · 02 (BoW + TF-IDF), Phase 5 · 04 (GloVe, FastText, Subword)
**Time:** ~75 minutes | **时间:** ~75 minutes


## 问题 问题引入

用户输入"如果有人说谎来获得钱会发生什么?"并希望找到实际覆盖该条例:"IPC第420条".一个关键词搜索完全错过了它 (没有共享的词汇库).一个语义搜索错过了它如果嵌入式没有训练在法律文本.真正的搜索必须处理两者.
> 用户输入"如果有人说谎,会怎么办?"并期望找到实际覆盖该内容的法规:"第420条"――关键词搜索完全找不到它(没有共享词汇)――如果嵌入没有在法律文本上训练过,语义搜索也会错过它――真正的搜索必须同时处理两者――

> **【中文解读】**本节提出的问题是:如何在实际工程中正确理解和应用这一技术――理解问题背景有助于把握技术选择的关键决策点――在实际人工智能系统中,错误的技术选择往往比实现细节的错误成本更高――


根据"图库"的定义,每一个图库都会被查到一个位置,每一个图库都会被查到一个位置.
> 它们是每个RAG系统,每个搜索站点模糊查找下面流水线.

这一课构建了每一个小块,每一个捕获都失败了.
> 本课程的各部分都指出了他们所取得的失败.

> **【中文解读】**本节介绍核心概念和理论基础.掌握这些概念是后续动手实现的前提,同时也是面试和工程实践中高频考察的知识点.


## 概念的核心概念

![Hybrid retrieval: BM25 + dense + RRF + cross-encoder rerank](../assets/retrieval.svg)
> ![混合检索：BM25 + 稠密 + RRF + 交叉编码器重排序](../assets/retrieval.svg)

选择你需要的四层.
> 选择你需要的.

1. **Sparse retrieval (BM25).**快速,准确的匹配,可怕的语义. 翻转索引. 每次查询在数百万文件中. 获得法规引用,产品代码,错误信息,命名实体正确.
2. **Dense retrieval.**编码查询和文件成向量. 最近邻居搜索.捕捉句子和语义相似性. 错过一个字符不同的关键字匹配. 50-200ms 每个查询与FAISS或向量DB.
3. **Fusion.**合并排名列表从稀疏和密集. 相互排名融合 (RRF) 是简单的默认,因为它忽略原始分数 (生活在不同的尺度中) 并仅使用排名位置.当你知道一个信号为你的域占主导地位时,重量融合是一个选择.
4. **Cross-encoder rerank.**通过合,运行一个跨编码器 (查询+文档一起,分分分每对).保持前五个.跨编码器比双编码器较慢,但更准确.
> 1. **稀疏检索（BM25）。**快速、精确匹配准确、语义上糟糕──在倒排索引上运行──百万档案上每查询亚 10 毫秒──正确处理法规引用、产品代码、错误消息、命名实体──
2. **稠密检索。**将查询和文档编码为向量――近邻搜索――捕获释义和语义相似性――遗漏差于一个字符的精确关键词匹配――使用FAISS或向量数据库每查询50-200毫秒――
3. **融合。**合并稀疏和密的排列列表――倒数排列融合 (RRF) 是简单的默认选择,因为它忽略原始分数 (存在于不同尺度) 只使用排列位置――当你知道某个信号在你的领域占主导地位时,加权融合是一个选项――
4. **交叉编码器重排序。**从融合中取前-30――运行交叉编码器(查询+档案一起,对每对打分) ・保留前-5――交叉编码器对每对双编码器慢但准确得多――你只在前-30 上运行来摊销成本――

两向检索 (BM25 +密集 +学习空间,如SPLADE) 在2026年比较高于两向检索,但需要学习空间指数的基础设施.对于大多数团队来说,双向加加密交叉编码重排是最好的点.
> 三路检索 (BM25 + 密 + 学习稀疏如 SPLADE) 在2026年基准上优于两路,但需要学习稀疏索引的基础设施――对于大多数团队来说,两路加交叉编码器重排是最佳平衡点――

> **【拓展：大语言模型的工程实践】**从GPT到ChatGPT,NLP领域经历了从"每个任务训练一个模型"到"一个模型解决所有任务"的范式转变. 在实际工程中,LLM的部署需要考虑代币限制,延迟,成本,安全审查等问题.

> **【拓展：RAG 与企业知识库】**检索增强生成 (RAG) 是当前企业人工智能应用中最流行的架构:将用户查询先检索相关文档片段,再将检索结果作为上下文给LLM 生成答案――这种方式解决了LLM 知识过时和幻觉问题――向量数据库――如Milvus、Pinecone、Weaviate) 是RAG系统的核心组件――

> **【拓展：NLP 的多语言挑战】**全球有7000多种语言,但NLP研究主要集中在英语等少数语言.跨语言迁移学习,多语言预训模型 (如 mBERT,XLM-R) 是解决低资源语言NLP的主要方法.


## 建立它,实现它.

> **【中文解读】**本节通过代码实现从零到核心算法――这种"从零开始"的方式可以帮助理解框架背后的原理,遇到问题时不会被黑盒困住――

```figure
gx-hybrid-retrieval
```

## 建立它

### 步骤1:从零开始BM25
> 两个参数值得了解.`k1=1.5`控制词频和;更高意味着重复词的权重更大.`b=0.75`控制长度归纳;0 忽略文档长度,1 完全归纳.默认值是罗伯逊原始论文中的推值,很少需要调整.

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

值得知道的两个参数.`k1=1.5`控制术语频率和;更高意味着更重的术语重复. `b=0.75`根据罗伯逊的建议,通常需要调整. 根据罗伯逊的建议, 罗伯逊的建议, 罗伯逊的建议是完全正常化的.
> 归结嵌入使点积等于余弦.`all-MiniLM-L6-v2`是384维,快速,对大多数英语检索足够强.多语言工作使用.`paraphrase-multilingual-MiniLM-L12-v2`△最高准确率使用`bge-large-en-v1.5`或`e5-large-v2`,我知道.

### 步骤2:使用双编码器进行密集检索
> `k=60`常数来自原始的RRF论文.`k`使排名差异的贡献变平;更低`k`已发布的默认值,很少需要调整.

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

点产量等于kosine.`all-MiniLM-L6-v2`对于多语言工作,使用 `paraphrase-multilingual-MiniLM-L12-v2`为了最准确的,`bge-large-en-v1.5`或`e5-large-v2`现在,我们要去.
> 三阶段组合――BM25 找到词汇匹配――密找到语义匹配――RRF 合并两个排名不需要分数校准――交叉编码器使用查询文档对重新对前-30 打分,捕获双编码器遗漏的细粒度相关性――保留前-5――

### 步骤3:相互级别的融合
> 标志意味着什么
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

其他`k=60`常数来自原始的RRF纸.`k`降低了排名差异的贡献;`k`现在,我们在这个问题上,我们需要一个问题.
> 特别是对RAG,检索器的**Recall@k**如果正确的段落没有检查集中,读者无法回答.

### 步骤4:混合搜索+重排
> 调试技巧:对于失败的查询,对稀疏和密排名. 如果一个找到正确的文档而另一个没有,你有词汇不匹配.

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

组建三个阶段.BM25发现词汇匹配.密集发现语义匹配.RRF不需要分数校准的情况下合并两个排名.跨编码器使用查询文档对进行重新评分,从而捕获了双编码器错过的细粒度相关性.保持前-5.

### 五步:评估

| Metric | Meaning |
|--------|---------|
| Recall@k | Of queries where the correct document exists, how often is it in the top-k? |
| MRR (Mean Reciprocal Rank) | Average of 1/rank of first relevant document. |
| nDCG@k | Accounts for relevance gradations, not just binary relevant/not. |

对于RAG而言,**Recall@k**如果没有正确的段落,读者不能回答.

调试提示:对于失败的查询,分别稀疏和密集的排名.如果一个找到正确的文档,而另一个没有,你会出现词汇不匹配 (修正:添加缺失的一半) 或语义模糊 (修正:更好的嵌入或重新排名).


> **【拓展：Prompt Engineering 与 LLM 应用】**快速工程已成为NLP工程师的核心技能. 从零射到少射,从思想链到反应,不同的提示策略适用于不同场景. 在实际项目中,系统提示 (系统提示) 的设计直接影响了LLM应用的稳定性和输出质量.

## 用它实现框架

> **【中文解读】**本节展示了如何使用成熟框架 (如PyTorch、HuggingFace等) 快速应用该技术.


现在,我们要做什么?
> 2026 年技术:

| Scale | Stack |
|-------|-------|
| 1k-100k docs | In-memory BM25 + `all-MiniLM-L6-v2` embeddings + RRF. No separate DB. |
| 100k-10M docs | FAISS or pgvector for dense + Elasticsearch / OpenSearch for BM25. Run in parallel. |
| 10M+ docs | Qdrant / Weaviate / Vespa / Milvus with hybrid support. Cross-encoder rerank on top-30. |
| Best-quality frontier | Three-way (BM25 + dense + SPLADE) + ColBERT late-interaction reranking |
> 规模技术
|------|--------|
| 1k-100k 文档 | 内存中 BM25 + `all-MiniLM-L6-v2` 嵌入 + RRF。无需独立数据库。 |
| 100k-10M 文档 | FAISS 或 pgvector 做稠密 + Elasticsearch / OpenSearch 做 BM25。并行运行。 |
| 10M+ 文档 | Qdrant / Weaviate / Vespa / Milvus 配混合支持。交叉编码器重排序 top-30。 |
| 最高质量前沿 | 三路（BM25 + 稠密 + SPLADE）+ ColBERT 后期交互重排序 |

根据您选择的预算进行评估. 预测检索提醒,然后再进行预测,以检测到RAG的精度.
> 无论选择什么,都必须为评估做预算. 在基准端到端 RAG 准确率之前先基准检索召回率.

### 2026年生产RAG的难以获取教训
> - **80% 的 RAG 失败追溯到摄取和分块，而不是模型。**团队花了几周交换LLM和调优提示,检索每三次查询就安静地回复错误的上下文――先修复分块――
- **分块策略比分块大小更重要。**固定大小分类会破坏表格,代码和嵌套标题――句子感知是默认选择;语义或基于LLM的分块在技术文档和产品手册上有回报――
- **父文档模式。**检索小的"子"块以获得精确性. 当同一节的多个子块出现时,换入的块以保留下文.
- **k_rerank=3 通常最优。**每增加一个块超过这个数量都会增加代币 成本和生成延迟而不提升答案质量――如果 k=8 仍然比 k=3 好,说明重排序器表现不足――
- **HyDE / 查询扩展。**从查询生成假设答案,嵌入其中,检索――弥合短问题和长文档之间的表述差距――无需培训即可免费提升精确率――
- **上下文预算控制在 8K token 以下。**在这个限制下持续命中意味着重排器值太容易.
- **版本化一切。**提示、分块规则、嵌入模型、重排序器──任何漂移都会静默破坏答案质量──忠诚度、上下文精确率和未回答问题的率
- **三路检索（BM25 + 稠密 + 学习稀疏如 SPLADE）在 2026 年基准上优于两路**特别是混合专名词和语义的查询.

- **80% of RAG failures trace to ingestion and chunking, not the model.**团队花了几周时间交换LLM和调整提示,而检索每第三次查询都会地返回错误的文本.
- **Chunking strategy matters more than chunk size.**固定尺寸分开分开表,代码和嵌入式标题.句子意识是默认的;语义或LLM基于的分断为技术文件和产品手册付出代价.
- **Parent-doc pattern.**检索小小的"孩子"块以获得精确性.当来自同一父母部分的多个孩子出现时,在父母块中交换以保持文本.这在不需要重新训练的情况下不断提高答案质量.
- **k_rerank=3 is usually optimal.**如果 k=8 对你来说仍然比 k=3 更好,那么重新排名器的性能低.
- **HyDE / query expansion.**通过查询生成一个假设答案,嵌入,检索. 弥合短问题和长文档之间的措辞差距. 免费的精确升降,没有训练.
- **Context budget under 8K tokens.**连续击中这个极限意味着重排门太松散了.
- **Version everything.**提示,分量规则,嵌入模型,重新排序器.任何漂移都会默默破坏答案质量. CI 关闭信任,文本精确性和未回答问题的率,用户在看到之前阻止回归.
- **Three-way retrieval (BM25 + dense + learned-sparse like SPLADE) outperforms two-way**根据2026年基准,特别是对混合正确名词和语义的查询.
> 根据2026年行业测量,正确检索设计减少了70-90%的幻觉.

根据2026年行业测量,正确的检索设计可以减少70-90%.大多数RAG性能增长来自更好的检索,而不是模型细节调整.

> **【中文解读】**本节关注如何将模型部署为可用的产品. 从原型到生产级系统需要考虑性能优化,错误处理,监控等多个维度.


## 运送它.

保存如`outputs/skill-retrieval-picker.md`其他:
> 保存为`outputs/skill-retrieval-picker.md`其他:

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

> **【中文解读】**练习题按照易/中/难 三个难度递进;;建议至少完成中级题,Hard级适合深入研究或面试准备;;


## 练习题

1. **Easy.**实施`hybrid_search`测试20个查询. 仅BM25,仅密集和混合物之间的5个回忆.
2. **Medium.**添加MRR计算.对于每个已知正确文档的测试查询,在BM25,密集和混合排名中找到正确文档的排名. 报告每个文档的MRR.
3. **Hard.**通过多个负面排名输失 (Sentence Transformers) 调整域名上的密集编码器.从500个查询文档对构建训练集.比较调整前和调整后的回忆.
> 1. **简单。**在500个文档语料上实现了上面的`hybrid_search`测试 20 个查询.比较 BM25-只,只有密度和混合的回忆.
2. **中等。**添加MRR计算――对于每个已知正确文档的测试查询,找到正确文档在BM25密和混合排名中的位置――报告各自的MRR――
3. **困难。**使用多个负面排名损失 (Sentence Transformers) 在你的领域微调密编码器――从500个查询文档对构建训练集――比较微调前后的召回率――

> **【中文解读】**在团队协作中,统一术语定义可以避免大量沟通误解.


## 关键词 快速查找表

| Term | What people say | What it actually means |
|------|-----------------|-----------------------|
| BM25 | Keyword search | Okapi BM25. Scores documents by term frequency, IDF, and length. |
| Dense retrieval | Vector search | Encode query + doc into vectors, find nearest neighbors. |
| Bi-encoder | Embedding model | Encodes query and doc independently. Fast at query time. |
| Cross-encoder | Reranker model | Encodes query + doc together. Slow but accurate. |
| RRF | Rank fusion | Combine two rankings by summing `1/(k + rank)`. |
| Recall@k | Retrieval metric | Fraction of queries where a relevant doc is in the top-k. |
> 现在,我们在这个世界里,
|------|-----------|---------|
| BM25 | 关键词搜索 | Okapi BM25。按词频、IDF 和长度为文档打分。 |
| 稠密检索 | 向量搜索 | 将查询 + 文档编码为向量，找最近邻。 |
| 双编码器 | 嵌入模型 | 独立编码查询和文档。查询时快速。 |
| 交叉编码器 | 重排序模型 | 一起编码查询 + 文档。慢但准确。 |
| RRF | 排名融合 | 通过对 `1/(k + rank)` 求和合并两个排名。 |
| Recall@k | 检索指标 | 相关文档在 top-k 中的查询比例。 |

> **【中文解读】**延伸阅读提供了深入学习的高质量资源. 这些论文和教程是该领域的经典参考文献,适合需要深入了解的读者.


## 继续阅读 继续阅读

- [Robertson and Zaragoza (2009). The Probabilistic Relevance Framework: BM25 and Beyond](https://www.staff.city.ac.uk/~sbrp622/papers/foundations_bm25_review.pdf)最终的BM25治疗.
- [Karpukhin et al. (2020). Dense Passage Retrieval for Open-Domain QA](https://arxiv.org/abs/2004.04906)DPR,是法典双码码器.
- [Formal et al. (2021). SPLADE: Sparse Lexical and Expansion Model](https://arxiv.org/abs/2107.05720)                              
- [Cormack, Clarke, Büttcher (2009). Reciprocal Rank Fusion outperforms Condorcet and individual Rank Learning Methods](https://plg.uwaterloo.ca/~gvcormac/cormacksigir09-rrf.pdf)  纸质
- [Khattab and Zaharia (2020). ColBERT: Efficient and Effective Passage Search](https://arxiv.org/abs/2004.12832) 晚间互动检索.
> - [Robertson and Zaragoza (2009). The Probabilistic Relevance Framework: BM25 and Beyond](https://www.staff.city.ac.uk/~sbrp622/papers/foundations_bm25_review.pdf) 权威的BM25 处理.
- [Karpukhin et al. (2020). Dense Passage Retrieval for Open-Domain QA](https://arxiv.org/abs/2004.04906)                     
- [Formal et al. (2021). SPLADE: Sparse Lexical and Expansion Model](https://arxiv.org/abs/2107.05720) 缩小与密差的学习稀疏检查器
- [Cormack, Clarke, Büttcher (2009). Reciprocal Rank Fusion outperforms Condorcet and individual Rank Learning Methods](https://plg.uwaterloo.ca/~gvcormac/cormacksigir09-rrf.pdf) 论文:
- [Khattab and Zaharia (2020). ColBERT: Efficient and Effective Passage Search](https://arxiv.org/abs/2004.12832) 后期交互检索──
