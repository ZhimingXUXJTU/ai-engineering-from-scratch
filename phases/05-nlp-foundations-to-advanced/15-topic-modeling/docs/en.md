# Topic Modeling — LDA and BERTopic | 主题建模 — LDA 与 BERTopic

> LDA: documents are mixtures of topics, topics are distributions over words. BERTopic: documents cluster in embedding space, clusters are topics. Same goal, different decompositions.

> **【中文解读】** LDA 用概率模型发现主题，BERTopic 用 BERT 嵌入。

**Type:** Learn
**Languages:** Python | **语言:** Python
**Prerequisites:** Phase 5 · 02 (BoW + TF-IDF), Phase 5 · 03 (Word2Vec) | **前置知识:** Phase 5 · 02 (BoW + TF-IDF), Phase 5 · 03 (Word2Vec)
**Time:** ~45 minutes | **时间:** ~45 minutes


## The Problem | 问题引入

You have 10,000 customer support tickets, 50,000 news articles, or 200,000 tweets. You need to know what the collection is about without reading it. You do not have labeled categories. You do not even know how many categories exist.
> 你有 10,000 张客户支持工单、50,000 篇新闻文章或 200,000 条推文。你需要在不阅读的情况下了解这个集合的主题。你没有标注的类别。你甚至不知道有多少类别存在。

> **【中文解读】** 本节提出的问题是：如何在实际工程中正确理解和应用这一技术。理解问题背景有助于把握技术选型的关键决策点。在实际 AI 系统中，错误的技术选型往往比实现细节的 bug 代价更高。


Topic modeling answers that without supervision. Give it a corpus, get back a small set of coherent topics and, for each document, a distribution over those topics.
> 主题建模在无监督的情况下回答这个问题。给它一个语料库，返回一小组连贯的主题，以及每篇文档在这些主题上的分布。

Two algorithmic families dominate. LDA (2003) treats each document as a mixture of latent topics and each topic as a distribution over words. Inference is Bayesian. It still ships in production where you need mixed-membership topic assignments and explainable word-level probability distributions.
> 两个算法族占主导地位。LDA（2003）将每篇文档视为潜在主题的混合，每个主题视为词的分布。推断是贝叶斯的。它仍然在你需要混合成员主题分配和可解释的词级概率分布的生产中发布。

BERTopic (2020) encodes documents with BERT, reduces dimensionality with UMAP, clusters with HDBSCAN, and extracts topic words via class-based TF-IDF. It wins on short text, social media, and anything where semantic similarity matters more than word overlap. One document gets one topic, which is a limitation for long-form content.
> BERTopic（2020）用 BERT 编码文档，用 UMAP 降维，用 HDBSCAN 聚类，通过基于类的 TF-IDF 提取主题词。它在短文本、社交媒体和语义相似性比词重叠更重要的内容上胜出。一篇文档获得一个主题，这对长篇内容是一个限制。

This lesson builds intuition for both and names which one to pick for a given corpus.
> 本课为两者建立直觉并指出给定语料该选哪个。

> **【中文解读】** 本节介绍核心概念和理论基础。掌握这些概念是后续动手实现的前提，同时也是面试和工程实践中高频考察的知识点。


## The Concept | 核心概念

![LDA mixture model vs BERTopic clustering](../assets/topic-modeling.svg)
> ![LDA 混合模型 vs BERTopic 聚类](../assets/topic-modeling.svg)

**LDA generative story.** Each topic is a distribution over words. Each document is a mixture of topics. To generate a word in a document, sample a topic from the document's mixture, then sample a word from that topic's distribution. Inference reverses this: given observed words, infer the topic distribution per document and the word distribution per topic. Collapsed Gibbs sampling or variational Bayes does the math.
> **LDA 生成故事。** 每个主题是词的分布。每篇文档是主题的混合。要在文档中生成一个词，从文档的混合中采样一个主题，然后从该主题的分布中采样一个词。推断逆转这个过程：给定观察到的词，推断每篇文档的主题分布和每个主题的词分布。坍缩 Gibbs 采样或变分贝叶斯做数学运算。

Key LDA output:
> 关键 LDA 输出：

- `doc_topic`: matrix `(n_docs, n_topics)`, each row sums to 1 (document's topic mixture).
- `topic_word`: matrix `(n_topics, vocab_size)`, each row sums to 1 (topic's word distribution).
> - `doc_topic`：矩阵 `(n_docs, n_topics)`，每行总和为 1（文档的主题混合）。
- `topic_word`：矩阵 `(n_topics, vocab_size)`，每行总和为 1（主题的词分布）。

**BERTopic pipeline.**
> **BERTopic 流水线。**

1. Encode each document with a sentence transformer (e.g., `all-MiniLM-L6-v2`). 384-dim vectors.
2. Reduce dimensionality with UMAP to ~5 dimensions. BERT embeddings are too high-dim for clustering.
3. Cluster with HDBSCAN. Density-based, produces variable-size clusters and an "outlier" label.
4. For each cluster, compute class-based TF-IDF over the cluster's documents to extract top words.
> 1. 用句子 Transformer（如 `all-MiniLM-L6-v2`）编码每篇文档。384 维向量。
2. 用 UMAP 降维到约 5 维。BERT 嵌入对聚类来说维度太高。
3. 用 HDBSCAN 聚类。基于密度，产生变大小聚类和 "离群值" 标签。
4. 对每个聚类，在聚类的文档上计算基于类的 TF-IDF 以提取顶级词。

Output is one topic per document (plus a -1 outlier label). Optionally, a soft membership via HDBSCAN's probability vector.
> 输出是每篇文档一个主题（加上 -1 离群值标签）。可选地，通过 HDBSCAN 的概率向量获得软成员资格。

> **【中文解读】** 本节通过代码从零实现核心算法。这种 "from scratch" 的方式能帮助理解框架背后的原理，遇到问题时不会被黑盒困住。

> **【拓展：大语言模型的工程实践】** 从 GPT 到 ChatGPT，NLP 领域经历了从 "每个任务训练一个模型" 到 "一个模型解决所有任务" 的范式转变。在实际工程中，LLM 的部署需要考虑 Token 限制、延迟、成本、安全审查等问题。LangChain、LlamaIndex 等框架简化了 LLM 应用的开发。

> **【拓展：RAG 与企业知识库】** 检索增强生成（RAG）是当前企业 AI 应用最流行的架构：将用户查询先检索相关文档片段，再将检索结果作为上下文喂给 LLM 生成答案。这种方式解决了 LLM 知识过时和幻觉问题。向量数据库（如 Milvus、Pinecone、Weaviate）是 RAG 系统的核心组件。

> **【拓展：NLP 的多语言挑战】** 全球有 7000+ 种语言，但 NLP 研究主要集中在英语等少数语言。跨语言迁移学习、多语言预训练模型（如 mBERT、XLM-R）是解决低资源语言 NLP 的主要方法。字节级模型（如 ByT5）甚至可以在无分词器的情况下处理任何语言。


## Build It | 动手实现

### Step 1: LDA via scikit-learn
> 注意：移除了停用词，min_df 和 max_df 过滤罕见和无处不在的词，使用 CountVectorizer（不是 TfidfVectorizer），因为 LDA 期望原始计数。

```python
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.decomposition import LatentDirichletAllocation
import numpy as np


def fit_lda(documents, n_topics=5, max_features=1000):
    cv = CountVectorizer(
        max_features=max_features,
        stop_words="english",
        min_df=2,
        max_df=0.9,
    )
    X = cv.fit_transform(documents)
    lda = LatentDirichletAllocation(
        n_components=n_topics,
        random_state=42,
        max_iter=50,
        learning_method="online",
    )
    doc_topic = lda.fit_transform(X)
    feature_names = cv.get_feature_names_out()
    return lda, cv, doc_topic, feature_names


def print_top_words(lda, feature_names, n_top=10):
    for idx, topic in enumerate(lda.components_):
        top_idx = np.argsort(-topic)[:n_top]
        words = [feature_names[i] for i in top_idx]
        print(f"topic {idx}: {' '.join(words)}")
```

Notice: stopwords removed, min_df and max_df filter rare and ubiquitous terms, CountVectorizer (not TfidfVectorizer) because LDA expects raw counts.
> `Topic != -1` 的过滤丢弃了 BERTopic 的离群值桶（HDBSCAN 无法聚类的文档）。`min_topic_size` 控制 HDBSCAN 的最小聚类大小；BERTopic 库默认为 10。本例为课程的规模显式设为 15。对于超过 10,000 文档的语料，增加到 50 或 100。

### Step 2: BERTopic (production)
> 两种方法都输出主题词。问题是这些词是否连贯。

```python
from bertopic import BERTopic

topic_model = BERTopic(
    embedding_model="sentence-transformers/all-MiniLM-L6-v2",
    min_topic_size=15,
    verbose=True,
)

topics, probs = topic_model.fit_transform(documents)
info = topic_model.get_topic_info()
print(info.head(20))
valid_topics = info[info["Topic"] != -1]["Topic"].tolist()
for topic_id in valid_topics[:5]:
    print(f"topic {topic_id}: {topic_model.get_topic(topic_id)[:10]}")
```

The filter on `Topic != -1` drops BERTopic's outlier bucket (documents HDBSCAN could not cluster). `min_topic_size` controls HDBSCAN's minimum cluster size; BERTopic's library default is 10. This example sets it to 15 explicitly for the lesson's scale. For corpora over 10,000 documents, increase to 50 or 100.
> - **主题连贯度（c_v）。** 结合滑动窗口上下文中顶级词对的 NPMI（归一化逐点互信息），将分数聚合为主题向量，通过余弦相似度比较这些向量。越高越好。使用 `gensim.models.CoherenceModel` 配 `coherence="c_v"`。
- **主题多样性。** 所有主题顶级词中唯一词的比例。越高越好（主题不重叠）。
- **定性检查。** 阅读每个主题的顶级词。它们是否命名了一个真实的东西？人类判断仍然是最后一道防线。

### Step 3: evaluation

Both methods output topic words. The question is whether those words cohere.

- **Topic coherence (c_v).** Combines NPMI (normalized pointwise mutual information) of top-word pairs over sliding-window contexts, aggregates the scores into topic vectors, and compares those vectors via cosine similarity. Higher is better. Use `gensim.models.CoherenceModel` with `coherence="c_v"`.
- **Topic diversity.** Fraction of unique words across all topics' top words. Higher is better (topics do not overlap).
- **Qualitative inspection.** Read the top words of each topic. Do they name a real thing? Human judgment is still the last line of defense.


> **【拓展：Prompt Engineering 与 LLM 应用】** Prompt Engineering 已成为 NLP 工程师的核心技能。从 Zero-shot 到 Few-shot，从 Chain-of-Thought 到 ReAct，不同的提示策略适用于不同场景。在实际项目中，系统提示（System Prompt）的设计直接影响 LLM 应用的稳定性和输出质量。

## When to pick which

| Situation | Pick |
|-----------|------|
| Short text (tweets, reviews, headlines) | BERTopic |
| Long documents with topic mixtures | LDA |
| No GPU / limited compute | LDA or NMF |
| Need document-level multi-topic distributions | LDA |
| LLM integration for topic labeling | BERTopic (direct support) |
| Resource-constrained edge deployment | LDA |
| Max semantic coherence | BERTopic |

The biggest practical consideration is document length. BERT embeddings truncate; LDA counts work on whatever length. For documents longer than the embedding model's context, either chunk + aggregate or use LDA.

> **【中文解读】** 本节展示如何用成熟框架（如 PyTorch、HuggingFace 等）快速应用该技术。在实际项目中，优先使用经过验证的框架实现，可以减少 bug 并提高开发效率。


## Use It | 用框架实现

The 2026 stack:
> 2026 年技术栈：

- **BERTopic.** Default for short text and anything where semantics matter.
- **`gensim.models.LdaModel`.** Classic LDA for production, mature, battle-tested.
- **`sklearn.decomposition.LatentDirichletAllocation`.** Easy LDA for experiments.
- **NMF.** Non-negative matrix factorization. Fast alternative to LDA, comparable quality on short text.
- **Top2Vec.** Similar design to BERTopic. Smaller community but good on some benchmarks.
- **FASTopic.** Newer, faster than BERTopic on very large corpora.
- **LLM-based labeling.** Run any clustering, then prompt a model to name each cluster.
> - **BERTopic。** 短文本和语义重要的场景的默认选择。
- **`gensim.models.LdaModel`。** 生产级经典 LDA，成熟，久经考验。
- **`sklearn.decomposition.LatentDirichletAllocation`。** 实验用简单 LDA。
- **NMF。** 非负矩阵分解。LDA 的快速替代，短文上质量相当。
- **Top2Vec。** 类似 BERTopic 的设计。社区较小但在某些基准上表现良好。
- **FASTopic。** 更新，在超大语料上比 BERTopic 快。
- **基于 LLM 的标注。** 运行任何聚类，然后提示模型命名每个聚类。

> **【中文解读】** 本节关注如何将模型部署为可用的产品。从原型到生产级系统需要考虑性能优化、错误处理、监控等多个维度。


## Ship It | 产出物

Save as `outputs/skill-topic-picker.md`:
> 保存为 `outputs/skill-topic-picker.md`：

```markdown
---
name: topic-picker
description: Pick LDA or BERTopic for a corpus. Specify library, knobs, evaluation.
version: 1.0.0
phase: 5
lesson: 15
tags: [nlp, topic-modeling]
---

Given a corpus description (document count, avg length, domain, language, compute budget), output:

1. Algorithm. LDA / NMF / BERTopic / Top2Vec / FASTopic. One-sentence reason.
2. Configuration. Number of topics: `recommended = max(5, round(sqrt(n_docs)))`, clamped to 200 for corpora under 40,000 docs; permit >200 only when the corpus is genuinely large (>40k) and note the increased compute cost. `min_df` / `max_df` filters and embedding model for neural approaches also belong here.
3. Evaluation. Topic coherence (c_v) via `gensim.models.CoherenceModel`, topic diversity, and a 20-sample human read.
4. Failure mode to probe. For LDA, "junk topics" absorbing stopwords and frequent terms. For BERTopic, the -1 outlier cluster swallowing ambiguous documents.

Refuse BERTopic on documents longer than the embedding model's context window without a chunking strategy. Refuse LDA on very short text (tweets, reviews under 10 tokens) as coherence collapses. Flag any n_topics choice below 5 as likely wrong; flag >200 on corpora under 40k docs as likely over-splitting.
```

> **【中文解读】** 练习题按照 Easy/Medium/Hard 三个难度递进。建议至少完成 Medium 级别的题目，Hard 级别适合深入研究或面试准备。


## Exercises | 练习题

1. **Easy.** Fit LDA with 5 topics on the 20 Newsgroups dataset. Print top 10 words per topic. Label each topic by hand. Did the algorithm find the real categories?
2. **Medium.** Fit BERTopic on the same 20 Newsgroups subset. Compare the number of topics found, top words, and qualitative coherence against LDA. Which surfaces the real categories more cleanly?
3. **Hard.** Compute c_v coherence for both LDA and BERTopic on your corpus. Run each with 5, 10, 20, 50 topics. Plot coherence vs topic count. Report which method is more stable across topic counts.
> 1. **简单。** 在 20 Newsgroups 数据集上用 5 个主题拟合 LDA。打印每个主题的 top 10 词。手工标注每个主题。算法找到了真实的类别吗？
2. **中等。** 在同样的 20 Newsgroups 子集上拟合 BERTopic。比较找到的主题数量、顶级词和定性连贯度与 LDA 的对比。哪个更清晰地呈现了真实类别？
3. **困难。** 在你的语料上计算 LDA 和 BERTopic 的 c_v 连贯度。分别用 5、10、20、50 个主题运行。绘制连贯度 vs 主题数。报告哪种方法在主题数变化下更稳定。

> **【中文解读】** 术语表中的 "What people say" vs "What it actually means" 区分了日常口语和精确技术含义。在团队协作中，统一术语定义可以避免大量沟通误解。


## Key Terms | 术语速查表

| Term | What people say | What it actually means |
|------|-----------------|-----------------------|
| Topic | A thing the corpus is about | A probability distribution over words (LDA) or a cluster of similar documents (BERTopic). |
| Mixed membership | Doc is multiple topics | LDA assigns each document a distribution over all topics. |
| UMAP | Dimensionality reduction | Manifold learning that preserves local structure; used in BERTopic. |
| HDBSCAN | Density clustering | Finds variable-size clusters; produces "noise" label (-1) for outliers. |
| c_v coherence | Topic quality metric | Average pointwise mutual information of top topic words within sliding windows. |
> | 术语 | 人们常说的 | 实际含义 |
|------|-----------|---------|
| 主题 | 语料关于的东西 | 词的概率分布（LDA）或相似文档的聚类（BERTopic）。 |
| 混合成员资格 | 文档是多个主题 | LDA 为每篇文档分配所有主题上的分布。 |
| UMAP | 降维 | 保留局部结构的流形学习；BERTopic 中使用。 |
| HDBSCAN | 密度聚类 | 找到变大小聚类；为离群值产生 "噪声" 标签（-1）。 |
| c_v 连贯度 | 主题质量指标 | 滑动窗口内顶级主题词的平均逐点互信息。 |

> **【中文解读】** 延伸阅读提供了深入学习的高质量资源。这些论文和教程是该领域的经典参考文献，适合需要深入理解的读者。


## Further Reading | 延伸阅读

- [Blei, Ng, Jordan (2003). Latent Dirichlet Allocation](https://www.jmlr.org/papers/volume3/blei03a/blei03a.pdf) — the LDA paper.
- [Grootendorst (2022). BERTopic: Neural topic modeling with a class-based TF-IDF procedure](https://arxiv.org/abs/2203.05794) — the BERTopic paper.
- [Röder, Both, Hinneburg (2015). Exploring the Space of Topic Coherence Measures](https://svn.aksw.org/papers/2015/WSDM_Topic_Evaluation/public.pdf) — the paper that introduced c_v and friends.
- [BERTopic documentation](https://maartengr.github.io/BERTopic/) — the production reference. Excellent examples.
> - [Blei, Ng, Jordan (2003). Latent Dirichlet Allocation](https://www.jmlr.org/papers/volume3/blei03a/blei03a.pdf) — LDA 论文。
- [Grootendorst (2022). BERTopic: Neural topic modeling with a class-based TF-IDF procedure](https://arxiv.org/abs/2203.05794) — BERTopic 论文。
- [Röder, Both, Hinneburg (2015). Exploring the Space of Topic Coherence Measures](https://svn.aksw.org/papers/2015/WSDM_Topic_Evaluation/public.pdf) — 引入 c_v 及相关指标的论文。
- [BERTopic documentation](https://maartengr.github.io/BERTopic/) — 生产参考。优秀示例。
