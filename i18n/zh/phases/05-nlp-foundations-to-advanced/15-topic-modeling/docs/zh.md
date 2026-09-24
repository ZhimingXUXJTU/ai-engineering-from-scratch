# 标题模拟  LDA 和 BERTopic 标题建模

> 文件是主题的混合物,主题是词汇上的分布.BERTopic:文件集群在嵌入空间中,集群是主题.相同的目标,不同的分解.
> 文档是主题的混合,主题是词的分布.

> **【中文解读】**们的们都在们的们中.

**Type:** Learn | **类型:** 学习
**Languages:** Python | **语言:** Python
**Prerequisites:** Phase 5 · 02 (BoW + TF-IDF), Phase 5 · 03 (Word2Vec) | **前置知识:** Phase 5 · 02 (BoW + TF-IDF), Phase 5 · 03 (Word2Vec)
**Time:** ~45 minutes | **时间:** ~45 分钟


## 问题 问题引入

你有1万张客户支持门票,5万条新闻文章或200万条推文.你需要知道收集内容是什么,而不需要阅读它.你没有标签类别.你甚至不知道有多少类别.
> 你有1万张客户支持单单,5万篇新闻文章或200万条推文――你需要在没有阅读的情况下了解这个集合的主题――你没有标签类别――你甚至不知道有多少类别――

> **【中文解读】**本节提出的问题是:如何在实际工程中正确理解和应用这一技术――理解问题背景有助于把握技术选择的关键决策点――在实际人工智能系统中,错误的技术选择往往比实现细节的错误成本更高――


给它一个体积,回来一组连贯的主题,
> 给它一个语料库,返回一小组连贯的主题,以及每个文档在这些主题上的分布.

两个算法家族主导.LDA (2003) 将每个文档视为隐藏的主题的混合,每个主题视为词汇分布.推理是贝耶斯.它仍然在生产中运输,需要混合成员主题分配和可解释的词汇水平概率分布.
> 两个算法族占主导地位――LDA,2003) 将每篇文档视为潜在主题的混合,每个主题视为词的分布――推断是贝叶斯的――它仍然在你需要的混合成员主题的分配和可解释的词级概率分布的生产中发布――

BERTopic (2020) 用BERT编码文件,用UMAP减少维度,用HDBSCAN集群,并通过基于类的TF-IDF提取主题词.它在短文本,社交媒体和任何语义相似性比词汇重叠更重要的地方都赢得了胜利. 一份文件得到了一个主题,这是一种长形式内容的限制.
> 通过基于类型的TF-IDF提取主题词. 它在短文本,社交媒体和语义相似性比词重叠更重要的内容中胜出.

这一课就建立了对两个人的直觉,
> 课程中,我们要建立直觉并指出要选择哪个语料.

> **【中文解读】**本节介绍核心概念和理论基础.掌握这些概念是后续动手实现的前提,同时也是面试和工程实践中高频考察的知识点.


## 概念的核心概念

![LDA mixture model vs BERTopic clustering](../assets/topic-modeling.svg)
> ![LDA 混合模型 vs BERTopic 聚类](../assets/topic-modeling.svg)

**LDA generative story.**每个主题都是单词的分布.每份文件都是单词的混合物.为了生成一个词,在文档中取样一个主题,然后取样一个词从该主题的分布中.推理逆转这一点:给出观察到的单词,推断每份文件的主题分布和每份话题的词分布.崩的吉布斯样本或变化贝斯做了数学.
> **LDA 生成故事。**每个主题是词的分布. 每个文档是主题的混合. 必须在文档中生成一个词,从文档的混合中采用一个词,然后从该主题的分布中采用一个词. 推断逆转这个过程:给定观察到的词,推断每一个文档的主题的分布和每个主题的词分布.

关键 LDA输出:
> 关键 LDA 输出:

- `doc_topic`列表`(n_docs, n_topics)`,每行总数为1 (文档的主题混合).
- `topic_word`列表`(n_topics, vocab_size)`,每行总数为1 (主题的词分布).
> - `doc_topic`矩阵`(n_docs, n_topics)`文档主题混合)
- `topic_word`矩阵`(n_topics, vocab_size)`总和为 1 个题的词分布.

**BERTopic pipeline.**
> **BERTopic 流水线。**

1. 编码每个文档用句子变换器 (例如, `all-MiniLM-L6-v2`它们是384维向量.
2. 通过UMAP将维度降低到5维度.BERT嵌入式太低于结.
3. 基于密度,产生变量尺寸的集群和"异常"标签.
4. 对于每个集群,计算基于类的TF-IDF在集群文件中以提取顶级词.
> 1. 用句子变压器`all-MiniLM-L6-v2`编码每篇文档.
2. 用UMAP降维到大约5维度.
3. 用HDBSCAN 聚类.基于密度,产生变大小聚类和"离群值"标签.
4. 根据各类的文件计算,以提取顶级词语.

输出是每份文件的一个主题 (加上 -1 异常标签). 选择性是通过HDBSCAN的概率向量进行软会员.
> 输出是每篇文档一个主题,通过HDBSCAN的概率向量获得软件成员资格.

> **【中文解读】**本节通过代码实现从零到核心算法――这种"从零开始"的方式可以帮助理解框架背后的原理,遇到问题时不会被黑盒困住――

> **【拓展：大语言模型的工程实践】**从GPT到ChatGPT,NLP领域经历了从"每个任务训练一个模型"到"一个模型解决所有任务"的范式转变. 在实际工程中,LLM的部署需要考虑代币限制,延迟,成本,安全审查等问题.

> **【拓展：RAG 与企业知识库】**检索增强生成 (RAG) 是当前企业人工智能应用中最流行的架构:将用户查询先检索相关文档片段,再将检索结果作为上下文给LLM 生成答案――这种方式解决了LLM 知识过时和幻觉问题――向量数据库――如Milvus、Pinecone、Weaviate) 是RAG系统的核心组件――

> **【拓展：NLP 的多语言挑战】**全球有7000多种语言,但NLP研究主要集中在英语等少数语言.跨语言迁移学习,多语言预训模型 (如 mBERT,XLM-R) 是解决低资源语言NLP的主要方法.


## 建立它,实现它.
```figure
topic-drift
```

## 建立它

### 步骤1:通过 scikit-learn进行LDA
> 注意:移除停用词,min_df 和 max_df 过罕见和无处不在的词,使用 CountVectorizer(不是 TfidfVectorizer),因为 LDA 期望原始计数。

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

注意:删除停止字,min_df和max_df过稀有和无处不在的术语, CountVectorizer (不是TfidfVectorizer) 因为LDA预计原始计数.
> `Topic != -1`已丢弃BERTopic的离群值桶 (HDBSCAN无法聚类的文档)`min_topic_size`控制HDBSCAN的最小聚类大小;BERTopic 默认为10──本例为课程的规模显然设定为15──对于超过10,000文档语料,增加到50或100──

### 步骤2:BERTopic (生产)
> 两种方法都输出主题词――问题是这些词是否连贯――

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

镜开了`Topic != -1`降低BERTopic的外向桶 (HDBSCAN无法集结文件). `min_topic_size`控制HDBSCAN的最小集群大小;BERTopic的库默认是10.本例明确设置为15为课程规模.对于超过10,000份文件,增加到50或100.
> - **主题连贯度（c_v）。**结合滑动窗口上下文中顶级词对的NPMI(归结一化点对信息),将分数聚合为主题向量,通过余弦相似度比较这些向量──越高越好──使用 `gensim.models.CoherenceModel`配`coherence="c_v"`,我知道.
- **主题多样性。**所有主题顶级词中唯一词的比例──越高越好──主题不重叠──
- **定性检查。**阅读每个主题的顶级词.它们是否命名为一个真实的东西?人类的判断仍然是最后的防线.

### 步骤3:评估

问题是,这些词是否一致.

- **Topic coherence (c_v).**结合了在滑动窗口背景下顶级词对的NPMI (标准化的点向互通信息),将分数集成成主题向量,并通过共数相似性进行比较.更高更好.使用 `gensim.models.CoherenceModel`随着`coherence="c_v"`现在,我们要去.
- **Topic diversity.**专题中所有主题的顶级词中独特词的比例.
- **Qualitative inspection.**读一读每一个话题的头条词.它们是否命名一个真实的东西?


> **【拓展：Prompt Engineering 与 LLM 应用】**快速工程已成为NLP工程师的核心技能. 从零射到少射,从思想链到反应,不同的提示策略适用于不同场景. 在实际项目中,系统提示 (系统提示) 的设计直接影响了LLM应用的稳定性和输出质量.

## 什么时候选择哪个

| Situation | Pick |
|-----------|------|
| Short text (tweets, reviews, headlines) | BERTopic |
| Long documents with topic mixtures | LDA |
| No GPU / limited compute | LDA or NMF |
| Need document-level multi-topic distributions | LDA |
| LLM integration for topic labeling | BERTopic (direct support) |
| Resource-constrained edge deployment | LDA |
| Max semantic coherence | BERTopic |

文件长度是最大的实际考虑因素.BERT嵌入式缩短;LDA计算工作在任何长度.对于文件长于嵌入式模型的文本,要么使用chunk + agregate或使用LDA.

> **【中文解读】**本节展示了如何使用成熟框架 (如PyTorch、HuggingFace等) 快速应用该技术.


## 用它实现框架

现在,我们要做什么?
> 2026 年技术:

- **BERTopic.**默认的短文本和任何语义的东西.
- **`gensim.models.LdaModel`.**经典的LDA生产,成熟,战斗测试.
- **`sklearn.decomposition.LatentDirichletAllocation`.**实验的LDA很容易.
- **NMF.**快速替代LDA,短文本的质量相似.
- **Top2Vec.**类似于BERTopic的设计. 社区较小,但在一些基准上很好.
- **FASTopic.**在非常大的体体上,比BERTopic更快.
- **LLM-based labeling.**运行任何集群,然后要求一个模型命名每个集群.
> - **BERTopic。**短文本和语义重要场景的默认选择──
- **`gensim.models.LdaModel`。**生产级经典LDA,成熟,久经验.
- **`sklearn.decomposition.LatentDirichletAllocation`。**实验用简单的LDA.
- **NMF。**非负矩阵分解──LDA的快速替代,短文上质量相当──
- **Top2Vec。**类似于BERTopic的设计.社区较小,但在某些基准上表现良好.
- **FASTopic。**更新,在超大语料上比BERTopic快
- **基于 LLM 的标注。**运行任何聚类,然后提示模型命名每个聚类.

> **【中文解读】**本节关注如何将模型部署为可用的产品. 从原型到生产级系统需要考虑性能优化,错误处理,监控等多个维度.


## 运送它.

保存如`outputs/skill-topic-picker.md`其他:
> 保存为`outputs/skill-topic-picker.md`其他:

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

> **【中文解读】**练习题按照易/中/难 三个难度递进;;建议至少完成中级题,Hard级适合深入研究或面试准备;;


## 练习题

1. **Easy.**按LDA适应20个新闻群数据集中的5个主题.按主题打印前10个词.手动标记每个主题.算法是否找到真正的类别?
2. **Medium.**根据LDA的数据,比较发现的主题数量,顶尖词汇和质量一致性.哪个更清洁地表现出实际类别?
3. **Hard.**在您的作品中计算LDA和BERTopic的c_v一致性.运行每个 5, 10, 20, 50个主题.图集一致性与主题数量.报告哪种方法在主题数量中更稳定.
> 1. **简单。**在20个新闻小组 数据集上使用5个主题拟合LDA――打印每个主题的前10个词――手工标签每个主题――算法找到了真实的类别吗?
2. **中等。**在同样的20个新闻小组中, 集编编辑与BERTopic相比较.
3. **困难。**在你的语料上计算LDA和BERTopic的c_v连贯度――分别使用5、10、20、50个主题运行――绘制连贯度与主题数量――报告哪种方法在主题数量变化下更稳定――

> **【中文解读】**在团队协作中,统一术语定义可以避免大量沟通误解.


## 关键词 快速查找表

| Term | What people say | What it actually means |
|------|-----------------|-----------------------|
| Topic | A thing the corpus is about | A probability distribution over words (LDA) or a cluster of similar documents (BERTopic). |
| Mixed membership | Doc is multiple topics | LDA assigns each document a distribution over all topics. |
| UMAP | Dimensionality reduction | Manifold learning that preserves local structure; used in BERTopic. |
| HDBSCAN | Density clustering | Finds variable-size clusters; produces "noise" label (-1) for outliers. |
| c_v coherence | Topic quality metric | Average pointwise mutual information of top topic words within sliding windows. |
> 现在,我们在这个世界里,
|------|-----------|---------|
| 主题 | 语料关于的东西 | 词的概率分布（LDA）或相似文档的聚类（BERTopic）。 |
| 混合成员资格 | 文档是多个主题 | LDA 为每篇文档分配所有主题上的分布。 |
| UMAP | 降维 | 保留局部结构的流形学习；BERTopic 中使用。 |
| HDBSCAN | 密度聚类 | 找到变大小聚类；为离群值产生 "噪声" 标签（-1）。 |
| c_v 连贯度 | 主题质量指标 | 滑动窗口内顶级主题词的平均逐点互信息。 |

> **【中文解读】**延伸阅读提供了深入学习的高质量资源. 这些论文和教程是该领域的经典参考文献,适合需要深入了解的读者.


## 继续阅读 继续阅读

- [Blei, Ng, Jordan (2003). Latent Dirichlet Allocation](https://www.jmlr.org/papers/volume3/blei03a/blei03a.pdf)LDA的报纸.
- [Grootendorst (2022). BERTopic: Neural topic modeling with a class-based TF-IDF procedure](https://arxiv.org/abs/2203.05794)BERTopic论文
- [Röder, Both, Hinneburg (2015). Exploring the Space of Topic Coherence Measures](https://svn.aksw.org/papers/2015/WSDM_Topic_Evaluation/public.pdf)报纸介绍了C_V和朋友.
- [BERTopic documentation](https://maartengr.github.io/BERTopic/)生产参考. 优秀的例子.
> - [Blei, Ng, Jordan (2003). Latent Dirichlet Allocation](https://www.jmlr.org/papers/volume3/blei03a/blei03a.pdf) LDA 论文──
- [Grootendorst (2022). BERTopic: Neural topic modeling with a class-based TF-IDF procedure](https://arxiv.org/abs/2203.05794) BERTopic 论文──
- [Röder, Both, Hinneburg (2015). Exploring the Space of Topic Coherence Measures](https://svn.aksw.org/papers/2015/WSDM_Topic_Evaluation/public.pdf) 引入相关指标的论文.
- [BERTopic documentation](https://maartengr.github.io/BERTopic/) 生产参考――优秀示例――
