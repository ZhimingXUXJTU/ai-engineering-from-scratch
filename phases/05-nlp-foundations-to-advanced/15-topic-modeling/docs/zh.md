# 主题建模 — LDA 与 BERTopic

> LDA：文档是主题的混合，主题是词的分布。BERTopic：文档在嵌入空间中聚类，聚类就是主题。同样的目标，不同的分解方式。

> **【中文解读】** LDA 用概率模型发现主题，BERTopic 用 BERT 嵌入。

**类型：** 学习
**编程语言：** Python
**前置课程：** Phase 5 · 02（BoW + TF-IDF），Phase 5 · 03（Word2Vec）
**预计时长：** ~45 分钟

## 问题引入

你有 10,000 张客户支持工单、50,000 篇新闻文章或 200,000 条推文。你需要在不阅读的情况下了解这个集合的主题。你没有标注的类别。你甚至不知道有多少类别存在。

> **【中文解读】** 本节提出的问题是：如何在实际工程中正确理解和应用这一技术。理解问题背景有助于把握技术选型的关键决策点。在实际 AI 系统中，错误的技术选型往往比实现细节的 bug 代价更高。


主题建模在无监督的情况下回答这个问题。给它一个语料库，返回一小组连贯的主题，以及每篇文档在这些主题上的分布。

两个算法族占主导地位。LDA（2003）将每篇文档视为潜在主题的混合，每个主题视为词的分布。推断是贝叶斯的。它仍然在你需要混合成员主题分配和可解释的词级概率分布的生产中发布。

BERTopic（2020）用 BERT 编码文档，用 UMAP 降维，用 HDBSCAN 聚类，通过基于类的 TF-IDF 提取主题词。它在短文本、社交媒体和语义相似性比词重叠更重要的内容上胜出。一篇文档获得一个主题，这对长篇内容是一个限制。

本课为两者建立直觉并指出给定语料该选哪个。

> **【中文解读】** 本节介绍核心概念和理论基础。掌握这些概念是后续动手实现的前提，同时也是面试和工程实践中高频考察的知识点。


## 核心概念

![LDA 混合模型 vs BERTopic 聚类](../assets/topic-modeling.svg)

**LDA 生成故事。** 每个主题是词的分布。每篇文档是主题的混合。要在文档中生成一个词，从文档的混合中采样一个主题，然后从该主题的分布中采样一个词。推断逆转这个过程：给定观察到的词，推断每篇文档的主题分布和每个主题的词分布。坍缩 Gibbs 采样或变分贝叶斯做数学运算。

关键 LDA 输出：

- `doc_topic`：矩阵 `(n_docs, n_topics)`，每行总和为 1（文档的主题混合）。
- `topic_word`：矩阵 `(n_topics, vocab_size)`，每行总和为 1（主题的词分布）。

**BERTopic 流水线。**

1. 用句子 Transformer（如 `all-MiniLM-L6-v2`）编码每篇文档。384 维向量。
2. 用 UMAP 降维到约 5 维。BERT 嵌入对聚类来说维度太高。
3. 用 HDBSCAN 聚类。基于密度，产生变大小聚类和 "离群值" 标签。
4. 对每个聚类，在聚类的文档上计算基于类的 TF-IDF 以提取顶级词。

输出是每篇文档一个主题（加上 -1 离群值标签）。可选地，通过 HDBSCAN 的概率向量获得软成员资格。

> **【中文解读】** 本节通过代码从零实现核心算法。这种 "from scratch" 的方式能帮助理解框架背后的原理，遇到问题时不会被黑盒困住。

> **【拓展：大语言模型的工程实践】** 从 GPT 到 ChatGPT，NLP 领域经历了从 "每个任务训练一个模型" 到 "一个模型解决所有任务" 的范式转变。在实际工程中，LLM 的部署需要考虑 Token 限制、延迟、成本、安全审查等问题。LangChain、LlamaIndex 等框架简化了 LLM 应用的开发。

> **【拓展：RAG 与企业知识库】** 检索增强生成（RAG）是当前企业 AI 应用最流行的架构：将用户查询先检索相关文档片段，再将检索结果作为上下文喂给 LLM 生成答案。这种方式解决了 LLM 知识过时和幻觉问题。向量数据库（如 Milvus、Pinecone、Weaviate）是 RAG 系统的核心组件。

> **【拓展：NLP 的多语言挑战】** 全球有 7000+ 种语言，但 NLP 研究主要集中在英语等少数语言。跨语言迁移学习、多语言预训练模型（如 mBERT、XLM-R）是解决低资源语言 NLP 的主要方法。字节级模型（如 ByT5）甚至可以在无分词器的情况下处理任何语言。





## 动手实现

### 步骤 1：通过 scikit-learn 实现 LDA

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

注意：移除了停用词，min_df 和 max_df 过滤罕见和无处不在的词，使用 CountVectorizer（不是 TfidfVectorizer），因为 LDA 期望原始计数。

### 步骤 2：BERTopic（生产）

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

`Topic != -1` 的过滤丢弃了 BERTopic 的离群值桶（HDBSCAN 无法聚类的文档）。`min_topic_size` 控制 HDBSCAN 的最小聚类大小；BERTopic 库默认为 10。本例为课程的规模显式设为 15。对于超过 10,000 文档的语料，增加到 50 或 100。

### 步骤 3：评估

两种方法都输出主题词。问题是这些词是否连贯。

- **主题连贯度（c_v）。** 结合滑动窗口上下文中顶级词对的 NPMI（归一化逐点互信息），将分数聚合为主题向量，通过余弦相似度比较这些向量。越高越好。使用 `gensim.models.CoherenceModel` 配 `coherence="c_v"`。
- **主题多样性。** 所有主题顶级词中唯一词的比例。越高越好（主题不重叠）。
- **定性检查。** 阅读每个主题的顶级词。它们是否命名了一个真实的东西？人类判断仍然是最后一道防线。



> **【拓展：Prompt Engineering 与 LLM 应用】** Prompt Engineering 已成为 NLP 工程师的核心技能。从 Zero-shot 到 Few-shot，从 Chain-of-Thought 到 ReAct，不同的提示策略适用于不同场景。在实际项目中，系统提示（System Prompt）的设计直接影响 LLM 应用的稳定性和输出质量。

## 如何选择

| 场景 | 选择 |
|------|------|
| 短文本（推文、评论、标题） | BERTopic |
| 长文档且包含主题混合 | LDA |
| 无 GPU / 计算受限 | LDA 或 NMF |
| 需要文档级多主题分布 | LDA |
| LLM 集成进行主题标注 | BERTopic（直接支持） |
| 资源受限的边缘部署 | LDA |
| 最大语义连贯性 | BERTopic |

最大的实际考虑是文档长度。BERT 嵌入会截断；LDA 计数适用于任何长度。对于超过嵌入模型上下文的文档，要么分块 + 聚合，要么使用 LDA。

> **【中文解读】** 本节展示如何用成熟框架（如 PyTorch、HuggingFace 等）快速应用该技术。在实际项目中，优先使用经过验证的框架实现，可以减少 bug 并提高开发效率。


## 用框架实现

2026 年技术栈：

- **BERTopic。** 短文本和语义重要的场景的默认选择。
- **`gensim.models.LdaModel`。** 生产级经典 LDA，成熟，久经考验。
- **`sklearn.decomposition.LatentDirichletAllocation`。** 实验用简单 LDA。
- **NMF。** 非负矩阵分解。LDA 的快速替代，短文上质量相当。
- **Top2Vec。** 类似 BERTopic 的设计。社区较小但在某些基准上表现良好。
- **FASTopic。** 更新，在超大语料上比 BERTopic 快。
- **基于 LLM 的标注。** 运行任何聚类，然后提示模型命名每个聚类。

> **【中文解读】** 本节关注如何将模型部署为可用的产品。从原型到生产级系统需要考虑性能优化、错误处理、监控等多个维度。



## 产出物

保存为 `outputs/skill-topic-picker.md`：

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


## 练习题

1. **简单。** 在 20 Newsgroups 数据集上用 5 个主题拟合 LDA。打印每个主题的 top 10 词。手工标注每个主题。算法找到了真实的类别吗？
2. **中等。** 在同样的 20 Newsgroups 子集上拟合 BERTopic。比较找到的主题数量、顶级词和定性连贯度与 LDA 的对比。哪个更清晰地呈现了真实类别？
3. **困难。** 在你的语料上计算 LDA 和 BERTopic 的 c_v 连贯度。分别用 5、10、20、50 个主题运行。绘制连贯度 vs 主题数。报告哪种方法在主题数变化下更稳定。

> **【中文解读】** 术语表中的 "What people say" vs "What it actually means" 区分了日常口语和精确技术含义。在团队协作中，统一术语定义可以避免大量沟通误解。


## 术语速查表

| 术语 | 人们常说的 | 实际含义 |
|------|-----------|---------|
| 主题 | 语料关于的东西 | 词的概率分布（LDA）或相似文档的聚类（BERTopic）。 |
| 混合成员资格 | 文档是多个主题 | LDA 为每篇文档分配所有主题上的分布。 |
| UMAP | 降维 | 保留局部结构的流形学习；BERTopic 中使用。 |
| HDBSCAN | 密度聚类 | 找到变大小聚类；为离群值产生 "噪声" 标签（-1）。 |
| c_v 连贯度 | 主题质量指标 | 滑动窗口内顶级主题词的平均逐点互信息。 |

> **【中文解读】** 延伸阅读提供了深入学习的高质量资源。这些论文和教程是该领域的经典参考文献，适合需要深入理解的读者。


## 延伸阅读

- [Blei, Ng, Jordan (2003). Latent Dirichlet Allocation](https://www.jmlr.org/papers/volume3/blei03a/blei03a.pdf) — LDA 论文。
- [Grootendorst (2022). BERTopic: Neural topic modeling with a class-based TF-IDF procedure](https://arxiv.org/abs/2203.05794) — BERTopic 论文。
- [Röder, Both, Hinneburg (2015). Exploring the Space of Topic Coherence Measures](https://svn.aksw.org/papers/2015/WSDM_Topic_Evaluation/public.pdf) — 引入 c_v 及相关指标的论文。
- [BERTopic documentation](https://maartengr.github.io/BERTopic/) — 生产参考。优秀示例。
