# 字包,TF-IDF,和文字表示

> 根据F-IDF的数据,在2026年,
> 在定义明确任务上,TF-IDF到2026年仍然赢得了嵌入.

> **【中文解读】**词袋模型忽略词序只统计词频,TF-IDF 通过惩罚常见词突出关键词――这是最基础的文本表示方法――

**Type:** Build | **类型:** 动手
**Languages:** Python | **语言:** Python
**Prerequisites:** Phase 5 · 01 (Text Processing), Phase 2 · 02 (Linear Regression from Scratch) | **前置知识:** Phase 5 · 01（文本处理），Phase 2 · 02（线性回归从零实现）
**Time:** ~75 minutes | **时间:** ~75 分钟

## 学习目标

- 从零开始构建字体和TF-IDF表示
  从零构建词袋模型和TF-IDF表示
- 了解稀疏向量,术语频率和反向文档频率
  了解稀疏向量、词频和逆文档频率
- 在生产中使用scikit-learn的 CountVectorizer和TfidfVectorizer
  在生产中使用小学学习的 CountVectorizer 和 TfidfVectorizer
- 知道TF-IDF在什么时候胜过嵌入式,以及什么时候失败
  知道TF-IDF何时胜过嵌入,何时失败

## 问题 问题引入

模型需要数字,你有字符串.

> 模型需要数字. 你手上的字符串.

每个NLP管道都必须回答同一个问题.我们如何将变长的代币流转化为一个固定尺寸的向量,一个分类器可以消耗. 首先答案是最愚蠢的答案. 计算字母. 制作向量.

> 每个NLP流水线都必须回答同样的问题:如何将变长的代币流转换为固定大量的向量,使分类器能消费.

输出量比任何嵌入式模型都多. 垃圾邮件过器,主题分类器,日志异常检测,搜索排名 (BM25之前),情感分析的第一波, 2026年,从业者仍然在狭窄的分类任务上先达到它. 它是快速的,可解释的,而且往往无法区分于400M参数嵌入模型,

> 这种载量生产的NLP应用比任何嵌入式模型都多了.垃圾邮件过器,主题分类器,日志异常检测,搜索排序 (BM25出现在之前) 首波情感分析,学术NLP基准测试的第一十年.2026年,在狭分类任务上,从业者仍然会首先使用它.它很快,可以解释,并且在词的存在或不存在是关键因素的任务上,通常很难区分400亿参数的嵌入式模型.

课程将从零开始构建一个词包,然后是TF-IDF,然后将Skit-Learn在三个行中做同样的事情,然后将导致你接触嵌入的失败模式命名.

> 首先,我们需要从零构建词袋模型,然后构建TF-IDF――然后展示使用三行代码做同样的事情――最后指出让你不得不选择嵌入失败模式――

## 概念的核心概念

> **【中文解读】**本节介绍核心概念和理论基础.掌握这些概念是后续动手实现的前提,同时也是面试和工程实践中高频考察的知识点.

**Bag of Words (BoW)**对于每个文件,计算每个词汇词汇出现的次数. 矢量长度是词汇大小. 位置 `i`是字数`i`现在,我们要去.

> **词袋模型（Bag of Words, BoW）**抛弃顺序――对每文档,统计每词表词出现的次数――向量长度是词表大小――位置`i`是词`i`计数量

**TF-IDF**任何文件中出现的单词都是非信息性的,所以缩小.一个词在整个文件中很少出现,但在单一文件中频繁的,是信号,所以缩小.

> **TF-IDF**对Bow重新加权. 现在每个文档中的词没有信息量,所以减轻其权重. 在整个语料库中罕见,但在单个文档中频繁出现的词是信号,所以提高其权重.

```
TF-IDF(w, d) = TF(w, d) * IDF(w)
             = count(w in d) / |d| * log(N / df(w))
```

在哪里?`TF`是文件中的术语频率,`df`是文件频率 (包含这个词的文件数量),`N`文件是全部的文件.`log`限制了人们使用无处不在的词语的重量.

> 其中`TF`是文档中的词频,`df`是文档频率 ((有多少文档包含这个词),`N`是档案总数.`log`使无处不在的词权重保持有界限.

两个产生的稀疏向量具有可解释轴.你可以看看训练有素的分类器的重量,并读出哪些单词将文档推向每个类.你不能用768维的BERT嵌入来做到这一点.

> 关键特性:两者都产生了可解释轴的稀疏向量.你可以查看训练好的分类器的权重,读出哪些字将文件推向每个类别.

> **【拓展：大语言模型的工程实践】**从GPT到ChatGPT,NLP领域经历了从"每个任务训练一个模型"到"一个模型解决所有任务"的范式转变. 在实际工程中,LLM的部署需要考虑代币限制,延迟,成本,安全审查等问题.

> **【拓展：RAG 与企业知识库】**检索增强生成 (RAG) 是当前企业人工智能应用中最流行的架构:将用户查询先检索相关文档片段,再将检索结果作为上下文给LLM 生成答案――这种方式解决了LLM 知识过时和幻觉问题――向量数据库――如Milvus、Pinecone、Weaviate) 是RAG系统的核心组件――

> **【拓展：NLP 的多语言挑战】**全球有7000多种语言,但NLP研究主要集中在英语等少数语言.跨语言迁移学习,多语言预训模型 (如 mBERT,XLM-R) 是解决低资源语言NLP的主要方法.

## 建立它,实现它.

> **【中文解读】**本节通过代码实现从零到核心算法――这种"从零开始"的方式可以帮助理解框架背后的原理,遇到问题时不会被黑盒困住――
```figure
bow-tfidf
```

## 建立它

### 步骤1:建立词汇库

```python
def build_vocab(docs):
    vocab = {}
    for doc in docs:
        for token in doc:
            if token not in vocab:
                vocab[token] = len(vocab)
    return vocab
```

输入:标记文件列表 (任何字面级标记器都会做; `code/main.py`在本课程中使用简体小写的变体.`{word: index}`标签: 稳定插入顺序 意思是字符指数0是第一个文档中看到的第一字. 公约有所不同; scikit-learn类型以字母顺序.

> 输入:代码的文档列表`code/main.py`使用简化忽略大小写变体) ・输出:`{word: index}`字典──稳定的插入顺序意味着词索引 0 是第一个文档中看到的第一个词──惯例不同;小学学习按字母排序──

### 步骤2:字包

```python
def bag_of_words(docs, vocab):
    matrix = [[0] * len(vocab) for _ in docs]
    for i, doc in enumerate(docs):
        for token in doc:
            if token in vocab:
                matrix[i][vocab[token]] += 1
    return matrix
```

```python
>>> docs = [["cat", "sat", "on", "mat"], ["cat", "cat", "ran"]]
>>> vocab = build_vocab(docs)
>>> bag_of_words(docs, vocab)
[[1, 1, 1, 1, 0], [2, 0, 0, 0, 1]]
```

列是文件,列是词汇指数.`[i][j]`是"多次说话"`j`在文件中显示`i`"第一医生有`cat`医生0已经做了.`ran`没有,因为没有.

> 行是文档──列是词表索引──条目 `[i][j]`是"词`j`在文档中`i`文件1 有两次`cat`因为它确实出现了两次.`ran`因为它没有出现.

### 步骤3:术语频率和文件频率

```python
import math


def term_frequency(doc_bow, doc_length):
    return [c / doc_length if doc_length else 0 for c in doc_bow]


def document_frequency(bow_matrix):
    df = [0] * len(bow_matrix[0])
    for row in bow_matrix:
        for j, count in enumerate(row):
            if count > 0:
                df[j] += 1
    return df


def inverse_document_frequency(df, n_docs):
    return [math.log((n_docs + 1) / (d + 1)) + 1 for d in df]
```

两种滑滑技巧值得命名.`(n+1)/(d+1)`避免`log(x/0)`后面的东西`+1`确保每个文件中的单词仍然具有 IDF 1 (而不是 0),与 scikit-learn的默认匹配.`log(N/df)`两者都能工作,但更友好的版本.

> 两个平滑技巧值得注意.`(n+1)/(d+1)`避免`log(x/0)`尾部的`+1`确保每个文档中的词的IDF 仍然为1(而不是0),与小学学习的默认值一致.`log(N/df)`两种都有效;平滑版本更友好.

### 步骤4:TF-IDF

```python
def tfidf(bow_matrix):
    n_docs = len(bow_matrix)
    df = document_frequency(bow_matrix)
    idf = inverse_document_frequency(df, n_docs)
    out = []
    for row in bow_matrix:
        length = sum(row)
        tf = term_frequency(row, length)
        out.append([tf_j * idf_j for tf_j, idf_j in zip(tf, idf)])
    return out
```

```python
>>> docs = [
...     ["the", "cat", "sat"],
...     ["the", "dog", "sat"],
...     ["the", "cat", "ran"],
... ]
>>> vocab = build_vocab(docs)
>>> bow = bag_of_words(docs, vocab)
>>> tfidf(bow)
```

文件,字母词 (`the`现在`cat`现在`sat`现在`dog`现在`ran`它们是`the`现在,它在三部都出现了,所以 IDF 很低.`dog`它们的向量很稀少 (大多数输入都是小的) 而歧视性的词则出现.

> 三文档,五个词表词(`the`,我知道.`cat`,我知道.`sat`,我知道.`dog`,我知道.`ran``the`由于所有三份文件都出现,`dog`由于它在一个文档中出现,因此 IDF 很高.

### 步骤 5: L2 规范行

```python
def l2_normalize(matrix):
    out = []
    for row in matrix:
        norm = math.sqrt(sum(x * x for x in row))
        out.append([x / norm if norm else 0 for x in row])
    return out
```

> **【中文解读】**本节展示了如何使用成熟框架 (如PyTorch、HuggingFace等) 快速应用该技术.

没有正常化,一个更长的文档得到了更大的向量,并且占据了相似度分数.L2正常化将每个文档放在单元超层上.

> 没有归结,更长的文档会得到更大的向量并主导相似度分分.

> **【拓展：Prompt Engineering 与 LLM 应用】**快速工程已成为NLP工程师的核心技能. 从零射到少射,从思想链到反应,不同的提示策略适用于不同场景. 在实际项目中,系统提示 (系统提示) 的设计直接影响了LLM应用的稳定性和输出质量.

## 用它实现框架

子学习将生产版本发送.

> 简单学习提供了生产级版本.

```python
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer

docs = ["the cat sat on the mat", "the dog sat on the mat", "the cat ran"]

bow_vectorizer = CountVectorizer()
bow = bow_vectorizer.fit_transform(docs)
print(bow_vectorizer.get_feature_names_out())
print(bow.toarray())

tfidf_vectorizer = TfidfVectorizer()
tfidf = tfidf_vectorizer.fit_transform(docs)
print(tfidf.toarray().round(3))
```

`CountVectorizer`能在一个电话中实现代码化,词汇和BoW. `TfidfVectorizer`增加 IDF 重量和 L2 正规化. 两者都返回稀疏矩阵. 在100k 文件中,密集版本不适合内存;保持稀疏直到分类器要求密集.

> `CountVectorizer`在一次调用中完成分词、构建词表和BoW──`TfidfVectorizer`增加了IDF加权和L2归结――两者都回归稀疏矩阵――对10万篇文档,密集版本放不进内存;在分类器要求密集之前保持稀疏――

改变一切的节点:

> 改变一切的关键参数:

| Arg | Effect | 参数 | 效果 |
|-----|--------|------|------|
| `ngram_range=(1, 2)` | Include bigrams. Usually boosts classification. | `ngram_range=(1, 2)` | 包含二元组。通常提升分类效果。 |
| `min_df=2` | Drop words in fewer than 2 docs. Trims vocabulary on noisy data. | `min_df=2` | 丢弃出现在少于 2 个文档中的词。在噪声数据上修剪词表。 |
| `max_df=0.95` | Drop words in more than 95% of docs. Approximates stopword removal without a hardcoded list. | `max_df=0.95` | 丢弃出现在超过 95% 文档中的词。近似停用词去除，无需硬编码列表。 |
| `stop_words="english"` | scikit-learn's builtin stopword list. Task-dependent — sentiment analysis should *not* drop negations. | `stop_words="english"` | scikit-learn 内置停用词列表。因任务而异——情感分析不应去除否定词。 |
| `sublinear_tf=True` | Use `1 + log(tf)` instead of raw `tf`. Helps when a term repeats many times in one doc. | `sublinear_tf=True` | 使用 `1 + log(tf)` 代替原始 `tf`。当一个词在一个文档中重复多次时有帮助。 |

### 尽管TF-IDF仍然在胜利 (2026年)

- 标签,记录异常标记,词存在是重要的,语义细微的不同.
  垃圾邮件检测、主题标签、日志异常标签──词的存在或不存在是关键的;语义细微差异不重要──
- 低数据模式 (数百个标记的例子).TF-IDF加上物流回归没有预训费用.
  低数据场景 (数百个标注样本) ◎TF-IDF 加逻辑回归没有预训成本──
- 任何地方延迟都重要.TF-IDF加上线性模型在微秒内回答.通过变压器嵌入文件需要10-100ms.
  任何延迟敏感场景──TF-IDF 加线性模型的响应时间是微秒级──通过变压器 嵌入一个文档需要10-100毫秒──
- 系统必须解释他们的预测,检查分类器的系数. 最好的正面词是原因.
  需要解释预测结果的系统――检查分类器的系数――排名最高的正权重词就是原因――

### 当TF-IDF失败时

根据这两个文件:

> 语义盲点──考虑以下两个文档:

- "这部电影根本不好.
- "这部电影很棒.

一是负面评价,一个是积极的,他们的TF-IDF重叠是完全的`{the, movie, was}`一个词包分类器必须记住这个词`not`附近`good`它可以从足够的数据中学习,但从来没有像理解语法模型那样优雅.

> 一是否定评价,一个是肯定评价.`{the, movie, was}`词袋分类器必须记住`good`附近的`not`在足够的数据上,它可以学会这一点,但永远不会像理解语法模型那样优雅.

另一种失败:在推断时,不存在词汇库中的单词.`Zoomer-approved`如果该代币从未出现在训练中. 字母嵌入式 (课4) 处理这一点. TF-IDF不能.

> 另一个失败:推理时的词表外(Out-of-vocabulary, OOV)词――在IMDb评论上训练的BoW模型不知道如何处理`Zoomer-approved`如果这个符号从未出现了训练中.

### 混合型:TF-IDF权重嵌入式

2026年中型数据分类的实际默认:使用TF-IDF权重作为关注词嵌入.

> 2026年中等数据分类的实用默认方案:使用TF-IDF权重作为词嵌入的重点

```python
def tfidf_weighted_embedding(doc, tfidf_scores, embedding_table, dim):
    vec = [0.0] * dim
    total_weight = 0.0
    for token in doc:
        if token not in embedding_table or token not in tfidf_scores:
            continue
        weight = tfidf_scores[token]
        emb = embedding_table[token]
        for i in range(dim):
            vec[i] += weight * emb[i]
        total_weight += weight
    if total_weight == 0:
        return vec
    return [v / total_weight for v in vec]
```

> **【中文解读】**本节关注如何将模型部署为可用的产品. 从原型到生产级系统需要考虑性能优化,错误处理,监控等多个维度.

您从嵌入式中获得语义能力,并从TF-IDF中强调稀有词. 类别列在聚合向量上. 这在约50k标记的例子下,在情感,主题和意图分类方面本身都比较好.

> 您从嵌入获得语义能力,从TF-IDF获得稀有词强调. 分类器在池化后进行量化训练. 在大约5万标签样本下面的情感,主题和意图分类任务上,这比单独使用任何方法更好.

## 运送它.

保存如`outputs/prompt-vectorization-picker.md`其他:

```markdown
---
name: vectorization-picker
description: Given a text-classification task, recommend BoW, TF-IDF, embeddings, or a hybrid.
phase: 5
lesson: 02
---

You recommend a text-vectorization strategy. Given a task description, output:

1. Representation (BoW, TF-IDF, transformer embeddings, or a hybrid). Explain why in one sentence.
2. Specific vectorizer configuration. Name the library. Quote the arguments (`ngram_range`, `min_df`, `max_df`, `sublinear_tf`, `stop_words`).
3. One failure mode to test before shipping.

Refuse to recommend embeddings when the user has under 500 labeled examples unless they show evidence of semantic failure in a TF-IDF baseline. Refuse to remove stopwords for sentiment analysis (negations carry signal). Flag class imbalance as needing more than a vectorizer change.

Example input: "Classifying 30k customer support tickets into 12 categories. Most tickets are 2-3 sentences. English only. Need explainability for audit logs."

Example output:

- Representation: TF-IDF. 30k examples is not small; explainability requirement rules out dense embeddings.
- Config: `TfidfVectorizer(ngram_range=(1, 2), min_df=3, max_df=0.95, sublinear_tf=True, stop_words=None)`. Keep stopwords because category keywords sometimes are stopwords ("not working" vs "working").
- Failure to test: verify `min_df=3` does not drop rare category keywords. Run `get_feature_names_out` filtered by class and eyeball.
```

## 练习题

1. **Easy.**实施`cosine_similarity(doc_vec_a, doc_vec_b)`检查相同文件的分数为1.0和分离词汇文件的分数为0.0.
   **简单。**在 L2 归结的TF-IDF 输出上实现`cosine_similarity(doc_vec_a, doc_vec_b)`证实相同文档分分为1.0,词表完全不相交的文档分为0.0──
2. **Medium.**加入`n-gram`支持`bag_of_words`参数`n`产量超过了`n`- 试试吧`n=2`现在`["the", "cat", "sat"]`产生了大数的数量.`["the cat", "cat sat"]`现在,我们要去.
   **中等。**为`bag_of_words`添加`n-gram`支持──参数`n`产生`n`子的数量.`n=2`时 时间`["the", "cat", "sat"]`产生二元组`["the cat", "cat sat"]`计数量
3. **Hard.**通过 GloVe 100d 矢量 (下载一次,缓存) 构建上述TF-IDF 重量嵌入式混合式. 根据20新闻组数据集中的简单TF-IDF和简单中共嵌入式进行分类精度比较. 报告哪个获胜.
   **困难。**使用 GloVe 100 维向量 (下载一次并缓存) 构建上述TF-IDF加权嵌入混合方案――在20个新闻集中的数据集中比较分类准确率,对比纯TF-IDF和纯平均值池化嵌入.

> **【中文解读】**练习题按照易/中/难 三个难度递进;;建议至少完成中级题,Hard级适合深入研究或面试准备;;

## 关键词 快速查找表

| Term | What people say | What it actually means | 术语 | 人们常说的 | 实际含义 |
|------|-----------------|-----------------------|------|-----------|---------|
| BoW | Word frequency vector | Counts of vocabulary words in one document. Throws away order. | BoW（词袋模型） | 词频向量 | 一个文档中词表词的计数。抛弃顺序。 |
| TF | Term frequency | Count of a word in a document, optionally normalized by document length. | TF（词频） | 词频 | 一个词在文档中的计数，可选按文档长度归一化。 |
| DF | Document frequency | Count of documents containing the word at least once. | DF（文档频率） | 文档频率 | 至少包含该词一次的文档计数。 |
| IDF | Inverse document frequency | `log(N / df)` smoothed. Downweights words that appear everywhere. | IDF（逆文档频率） | 逆文档频率 | 经平滑的 `log(N / df)`。降低到处出现的词的权重。 |
| Sparse vector | Mostly zeros | Vocabulary is typically 10k-100k words; most are absent from any given document. | 稀疏向量 | 大部分为零 | 词表通常有 1 万到 10 万个词；大多数在任何给定文档中都不出现。 |
| Cosine similarity | Vector angle | Dot product of L2-normalized vectors. 1 is identical, 0 is orthogonal. | 余弦相似度 | 向量夹角 | L2 归一化向量的点积。1 表示相同，0 表示正交。 |

> **【中文解读】**在团队协作中,统一术语定义可以避免大量沟通误解.

## 继续阅读 继续阅读

- [scikit-learn — feature extraction from text](https://scikit-learn.org/stable/modules/feature_extraction.html#text-feature-extraction)法典API参考,加上每个按上的注释.
- [Salton, G., & Buckley, C. (1988). Term-weighting approaches in automatic text retrieval](https://www.sciencedirect.com/science/article/pii/0306457388900210)使TF-IDF成为十年默认方案的论文.
- ["Why TF-IDF Still Beats Embeddings" — Ashfaque Thonikkadavan (Medium)](https://medium.com/@cmtwskb/why-tf-idf-still-beats-embeddings-ad85c123e1b2) 2026年,当旧方法胜利时,以及为什么. / 2026年对旧方法何时胜出以及为什么的观点.
