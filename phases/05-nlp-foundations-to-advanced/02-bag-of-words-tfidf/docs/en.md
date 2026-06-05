# Bag of Words, TF-IDF, and Text Representation | 词袋模型、TF-IDF 与文本表示

> Count first, think later. TF-IDF still beats embeddings on well-defined tasks in 2026.
> 先计数，后思考。在定义明确的任务上，TF-IDF 到 2026 年仍然胜过嵌入。

> **【中文解读】** 词袋模型忽略词序只统计词频，TF-IDF 通过惩罚常见词突出关键词。这是最基础的文本表示方法。

**Type:** Build | **类型:** 动手
**Languages:** Python | **语言:** Python
**Prerequisites:** Phase 5 · 01 (Text Processing), Phase 2 · 02 (Linear Regression from Scratch) | **前置知识:** Phase 5 · 01（文本处理），Phase 2 · 02（线性回归从零实现）
**Time:** ~75 minutes | **时间:** ~75 分钟

## Learning Objectives | 学习目标

- Build bag-of-words and TF-IDF representations from scratch
  从零构建词袋模型和 TF-IDF 表示
- Understand sparse vectors, term frequency, and inverse document frequency
  理解稀疏向量、词频和逆文档频率
- Use scikit-learn's CountVectorizer and TfidfVectorizer in production
  在生产中使用 scikit-learn 的 CountVectorizer 和 TfidfVectorizer
- Know when TF-IDF wins over embeddings and when it fails
  知道 TF-IDF 何时胜过嵌入，何时失败

## The Problem | 问题引入

The model needs numbers. You have strings.

> 模型需要数字。你手上的是字符串。

Every NLP pipeline has to answer the same question. How do we turn a variable-length stream of tokens into a fixed-size vector that a classifier can consume. The first answer the field landed on was the dumbest one that works. Count the words. Make a vector.

> 每个 NLP 流水线都必须回答同样的问题：如何将变长的 token 流转换为固定大小的向量，使分类器可以消费。该领域给出的第一个答案是最笨但管用的方法。数词频。做向量。

That vector has carried more production NLP than any embedding model. Spam filters, topic classifiers, log anomaly detection, search ranking (before BM25), the first wave of sentiment analysis, the first decade of academic NLP benchmarks. 2026 practitioners still reach for it first on narrow classification tasks. It is fast, interpretable, and often indistinguishable from a 400M-parameter embedding model on tasks where word presence is what matters.

> 这个向量承载的生产 NLP 应用比任何嵌入模型都多。垃圾邮件过滤器、主题分类器、日志异常检测、搜索排序（BM25 出现之前）、第一波情感分析、学术 NLP 基准测试的第一个十年。2026 年的从业者在窄分类任务上仍然会首先使用它。它快速、可解释，并且在词的存在与否是关键因素的任务上，通常与 4 亿参数的嵌入模型难以区分。

This lesson builds bag of words, then TF-IDF, from scratch. Then shows scikit-learn doing the same in three lines. Then names the failure mode that makes you reach for embeddings.

> 本课从零构建词袋模型，然后构建 TF-IDF。然后展示 scikit-learn 用三行代码做同样的事。最后指出让你不得不选择嵌入的失败模式。

## The Concept | 核心概念

> **【中文解读】** 本节介绍核心概念和理论基础。掌握这些概念是后续动手实现的前提，同时也是面试和工程实践中高频考察的知识点。

**Bag of Words (BoW)** throws away order. For each document, count how many times each vocabulary word appears. Vector length is the vocabulary size. Position `i` is the count of word `i`.

> **词袋模型（Bag of Words, BoW）** 抛弃顺序。对每个文档，统计每个词表词出现的次数。向量长度是词表大小。位置 `i` 是词 `i` 的计数。

**TF-IDF** reweights BoW. A word that appears in every document is uninformative, so scale it down. A word rare across the corpus but frequent in a single document is signal, so scale it up.

> **TF-IDF** 对 BoW 重新加权。出现在每个文档中的词没有信息量，所以降低其权重。在整个语料库中罕见但在单个文档中频繁出现的词是信号，所以提高其权重。

```
TF-IDF(w, d) = TF(w, d) * IDF(w)
             = count(w in d) / |d| * log(N / df(w))
```

Where `TF` is term frequency in the document, `df` is document frequency (how many docs contain the word), `N` is total documents. The `log` keeps the weight bounded for ubiquitous words.

> 其中 `TF` 是文档中的词频，`df` 是文档频率（有多少文档包含该词），`N` 是文档总数。`log` 使无处不在的词的权重保持有界。

Key property: both produce sparse vectors with interpretable axes. You can look at a trained classifier's weights and read which words push a document toward each class. You cannot do this with a 768-dimensional BERT embedding.

> 关键特性：两者都产生具有可解释轴的稀疏向量。你可以查看训练好的分类器的权重，读出哪些词将文档推向每个类别。你无法用 768 维的 BERT 嵌入做到这一点。

> **【拓展：大语言模型的工程实践】** 从 GPT 到 ChatGPT，NLP 领域经历了从 "每个任务训练一个模型" 到 "一个模型解决所有任务" 的范式转变。在实际工程中，LLM 的部署需要考虑 Token 限制、延迟、成本、安全审查等问题。LangChain、LlamaIndex 等框架简化了 LLM 应用的开发。

> **【拓展：RAG 与企业知识库】** 检索增强生成（RAG）是当前企业 AI 应用最流行的架构：将用户查询先检索相关文档片段，再将检索结果作为上下文喂给 LLM 生成答案。这种方式解决了 LLM 知识过时和幻觉问题。向量数据库（如 Milvus、Pinecone、Weaviate）是 RAG 系统的核心组件。

> **【拓展：NLP 的多语言挑战】** 全球有 7000+ 种语言，但 NLP 研究主要集中在英语等少数语言。跨语言迁移学习、多语言预训练模型（如 mBERT、XLM-R）是解决低资源语言 NLP 的主要方法。字节级模型（如 ByT5）甚至可以在无分词器的情况下处理任何语言。

## Build It | 动手实现

> **【中文解读】** 本节通过代码从零实现核心算法。这种 "from scratch" 的方式能帮助理解框架背后的原理，遇到问题时不会被黑盒困住。

### Step 1: build the vocabulary

```python
def build_vocab(docs):
    vocab = {}
    for doc in docs:
        for token in doc:
            if token not in vocab:
                vocab[token] = len(vocab)
    return vocab
```

Input: list of tokenized documents (any word-level tokenizer will do; the `code/main.py` in this lesson uses a simplified lowercase variant). Output: `{word: index}` dict. Stable insertion order means word index 0 is the first word seen in the first document. Convention varies; scikit-learn sorts alphabetically.

> 输入：token 化的文档列表（任何词级分词器都可以；本课的 `code/main.py` 使用简化的忽略大小写变体）。输出：`{word: index}` 字典。稳定的插入顺序意味着词索引 0 是第一个文档中看到的第一个词。惯例各不相同；scikit-learn 按字母排序。

### Step 2: bag of words

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

Rows are documents. Columns are vocabulary indices. Entry `[i][j]` is "how many times word `j` appears in document `i`." Doc 1 has `cat` twice because it did. Doc 0 has `ran` zero times because it did not.

> 行是文档。列是词表索引。条目 `[i][j]` 是 "词 `j` 在文档 `i` 中出现了多少次"。文档 1 有两次 `cat`，因为它确实出现了两次。文档 0 有零次 `ran`，因为它没有出现。

### Step 3: term frequency and document frequency

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

Two smoothing tricks worth naming. The `(n+1)/(d+1)` avoids `log(x/0)`. The trailing `+1` ensures a word in every document still has IDF 1 (not 0), matching scikit-learn's default. Other implementations use raw `log(N/df)`. Both work; the smoothed version is friendlier.

> 两个平滑技巧值得注意。`(n+1)/(d+1)` 避免 `log(x/0)`。尾部的 `+1` 确保出现在每个文档中的词的 IDF 仍然为 1（而不是 0），与 scikit-learn 的默认值一致。其他实现使用原始的 `log(N/df)`。两种都有效；平滑版本更友好。

### Step 4: TF-IDF

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

Three documents, five vocab words (`the`, `cat`, `sat`, `dog`, `ran`). `the` appears in all three, so its IDF is low. `dog` appears in one, so its IDF is high. The vectors are sparse (most entries are small) and the discriminative words pop.

> 三个文档，五个词表词（`the`、`cat`、`sat`、`dog`、`ran`）。`the` 在所有三个文档中都出现，所以其 IDF 很低。`dog` 只在一个文档中出现，所以其 IDF 很高。向量是稀疏的（大多数条目很小），区分性强的词突出。

### Step 5: L2-normalize rows

```python
def l2_normalize(matrix):
    out = []
    for row in matrix:
        norm = math.sqrt(sum(x * x for x in row))
        out.append([x / norm if norm else 0 for x in row])
    return out
```

> **【中文解读】** 本节展示如何用成熟框架（如 PyTorch、HuggingFace 等）快速应用该技术。在实际项目中，优先使用经过验证的框架实现，可以减少 bug 并提高开发效率。

Without normalization, a longer document gets a larger vector and dominates similarity scores. L2 normalization puts every document on the unit hypersphere. Cosine similarity between rows is now just a dot product.

> 没有归一化，更长的文档会得到更大的向量并主导相似度得分。L2 归一化将每个文档放在单位超球面上。行之间的余弦相似度现在只是点积。

> **【拓展：Prompt Engineering 与 LLM 应用】** Prompt Engineering 已成为 NLP 工程师的核心技能。从 Zero-shot 到 Few-shot，从 Chain-of-Thought 到 ReAct，不同的提示策略适用于不同场景。在实际项目中，系统提示（System Prompt）的设计直接影响 LLM 应用的稳定性和输出质量。

## Use It | 用框架实现

scikit-learn ships the production version.

> scikit-learn 提供了生产级版本。

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

`CountVectorizer` does tokenization, vocabulary, and BoW in one call. `TfidfVectorizer` adds IDF weighting and L2 normalization. Both return sparse matrices. For 100k documents, the dense version does not fit in memory; stay sparse until the classifier demands dense.

> `CountVectorizer` 在一次调用中完成分词、构建词表和 BoW。`TfidfVectorizer` 增加了 IDF 加权和 L2 归一化。两者都返回稀疏矩阵。对于 10 万篇文档，密集版本放不进内存；在分类器要求密集之前保持稀疏。

Knobs that change everything:

> 改变一切的关键参数：

| Arg | Effect | 参数 | 效果 |
|-----|--------|------|------|
| `ngram_range=(1, 2)` | Include bigrams. Usually boosts classification. | `ngram_range=(1, 2)` | 包含二元组。通常提升分类效果。 |
| `min_df=2` | Drop words in fewer than 2 docs. Trims vocabulary on noisy data. | `min_df=2` | 丢弃出现在少于 2 个文档中的词。在噪声数据上修剪词表。 |
| `max_df=0.95` | Drop words in more than 95% of docs. Approximates stopword removal without a hardcoded list. | `max_df=0.95` | 丢弃出现在超过 95% 文档中的词。近似停用词去除，无需硬编码列表。 |
| `stop_words="english"` | scikit-learn's builtin stopword list. Task-dependent — sentiment analysis should *not* drop negations. | `stop_words="english"` | scikit-learn 内置停用词列表。因任务而异——情感分析不应去除否定词。 |
| `sublinear_tf=True` | Use `1 + log(tf)` instead of raw `tf`. Helps when a term repeats many times in one doc. | `sublinear_tf=True` | 使用 `1 + log(tf)` 代替原始 `tf`。当一个词在一个文档中重复多次时有帮助。 |

### When TF-IDF still wins (as of 2026)

- Spam detection, topic labeling, log anomaly flagging. Word presence is what matters; semantic nuance does not.
  垃圾邮件检测、主题标注、日志异常标记。词的存在与否是关键；语义细微差别不重要。
- Low-data regimes (hundreds of labeled examples). TF-IDF plus logistic regression has no pretraining cost.
  低数据场景（数百个标注样本）。TF-IDF 加逻辑回归没有预训练成本。
- Anywhere latency matters. TF-IDF plus a linear model answers in microseconds. Embedding a document through a transformer takes 10-100ms.
  任何延迟敏感的场景。TF-IDF 加线性模型的响应时间是微秒级。通过 Transformer 嵌入一篇文档需要 10-100 毫秒。
- Systems that must explain their predictions. Inspect the classifier's coefficients. Top positive words are the reason.
  需要解释预测结果的系统。检查分类器的系数。排名最高的正权重词就是原因。

### When TF-IDF fails

The semantic blindness failure. Consider these two documents:

> 语义盲点。考虑以下两个文档：

- "The movie was not good at all."
- "The movie was excellent."

One is a negative review. One is positive. Their TF-IDF overlap is exactly `{the, movie, was}`. A bag-of-words classifier has to memorize that the word `not` near `good` flips the label. It can learn this on enough data, but never as gracefully as a model that understands syntax.

> 一个是否定评价，一个是肯定评价。它们的 TF-IDF 重叠部分恰好是 `{the, movie, was}`。词袋分类器必须记住 `good` 附近的 `not` 会翻转标签。在足够多的数据上它可以学会这一点，但永远不会像一个理解语法的模型那样优雅。

The other failure: out-of-vocabulary words at inference. A BoW model trained on IMDb reviews has no idea what to do with `Zoomer-approved` if that token never appeared in training. Subword embeddings (lesson 04) handle this. TF-IDF cannot.

> 另一个失败：推理时的词表外（Out-of-Vocabulary, OOV）词。在 IMDb 评论上训练的 BoW 模型不知道如何处理 `Zoomer-approved`，如果这个 token 从未出现在训练中。子词嵌入（第 04 课）处理这个问题。TF-IDF 不行。

### Hybrid: TF-IDF weighted embeddings

The 2026 pragmatic default for medium-data classification: use TF-IDF weights as attention over word embeddings.

> 2026 年中等数据分类的实用默认方案：使用 TF-IDF 权重作为词嵌入上的注意力。

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

> **【中文解读】** 本节关注如何将模型部署为可用的产品。从原型到生产级系统需要考虑性能优化、错误处理、监控等多个维度。

You get semantic capacity from embeddings, and rare-word emphasis from TF-IDF. Classifier trains on the pooled vector. This outperforms either on its own for sentiment, topic, and intent classification below about 50k labeled examples.

> 你从嵌入获得语义能力，从 TF-IDF 获得稀有词强调。分类器在池化后的向量上训练。在大约 5 万标注样本以下的情感、主题和意图分类任务上，这比单独使用任何一种方法效果都好。

## Ship It | 产出物

Save as `outputs/prompt-vectorization-picker.md`:

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

## Exercises | 练习题

1. **Easy.** Implement `cosine_similarity(doc_vec_a, doc_vec_b)` on the L2-normalized TF-IDF output. Verify that identical documents score 1.0 and disjoint-vocabulary documents score 0.0.
   **简单。** 在 L2 归一化的 TF-IDF 输出上实现 `cosine_similarity(doc_vec_a, doc_vec_b)`。验证相同文档得分为 1.0，词表完全不相交的文档得分为 0.0。
2. **Medium.** Add `n-gram` support to `bag_of_words`. Parameter `n` produces counts over `n`-grams. Test that `n=2` on `["the", "cat", "sat"]` produces bigram counts for `["the cat", "cat sat"]`.
   **中等。** 为 `bag_of_words` 添加 `n-gram` 支持。参数 `n` 产生 `n`-gram 的计数。测试 `n=2` 时 `["the", "cat", "sat"]` 产生二元组 `["the cat", "cat sat"]` 的计数。
3. **Hard.** Build the TF-IDF-weighted-embedding hybrid above using GloVe 100d vectors (download once, cache). Compare classification accuracy against plain TF-IDF and plain mean-pooled embeddings on the 20 Newsgroups dataset. Report which wins where.
   **困难。** 使用 GloVe 100 维向量（下载一次并缓存）构建上述 TF-IDF 加权嵌入混合方案。在 20 Newsgroups 数据集上比较分类准确率，对比纯 TF-IDF 和纯均值池化嵌入。报告哪个在何处胜出。

> **【中文解读】** 练习题按照 Easy/Medium/Hard 三个难度递进。建议至少完成 Medium 级别的题目，Hard 级别适合深入研究或面试准备。

## Key Terms | 术语速查表

| Term | What people say | What it actually means | 术语 | 人们常说的 | 实际含义 |
|------|-----------------|-----------------------|------|-----------|---------|
| BoW | Word frequency vector | Counts of vocabulary words in one document. Throws away order. | BoW（词袋模型） | 词频向量 | 一个文档中词表词的计数。抛弃顺序。 |
| TF | Term frequency | Count of a word in a document, optionally normalized by document length. | TF（词频） | 词频 | 一个词在文档中的计数，可选按文档长度归一化。 |
| DF | Document frequency | Count of documents containing the word at least once. | DF（文档频率） | 文档频率 | 至少包含该词一次的文档计数。 |
| IDF | Inverse document frequency | `log(N / df)` smoothed. Downweights words that appear everywhere. | IDF（逆文档频率） | 逆文档频率 | 经平滑的 `log(N / df)`。降低到处出现的词的权重。 |
| Sparse vector | Mostly zeros | Vocabulary is typically 10k-100k words; most are absent from any given document. | 稀疏向量 | 大部分为零 | 词表通常有 1 万到 10 万个词；大多数在任何给定文档中都不出现。 |
| Cosine similarity | Vector angle | Dot product of L2-normalized vectors. 1 is identical, 0 is orthogonal. | 余弦相似度 | 向量夹角 | L2 归一化向量的点积。1 表示相同，0 表示正交。 |

> **【中文解读】** 术语表中的 "What people say" vs "What it actually means" 区分了日常口语和精确技术含义。在团队协作中，统一术语定义可以避免大量沟通误解。

## Further Reading | 延伸阅读

- [scikit-learn — feature extraction from text](https://scikit-learn.org/stable/modules/feature_extraction.html#text-feature-extraction) — the canonical API reference, plus notes on every knob. / 权威 API 参考，以及每个参数的说明。
- [Salton, G., & Buckley, C. (1988). Term-weighting approaches in automatic text retrieval](https://www.sciencedirect.com/science/article/pii/0306457388900210) — the paper that made TF-IDF the default for a decade. / 使 TF-IDF 成为十年默认方案的论文。
- ["Why TF-IDF Still Beats Embeddings" — Ashfaque Thonikkadavan (Medium)](https://medium.com/@cmtwskb/why-tf-idf-still-beats-embeddings-ad85c123e1b2) — 2026 take on when the old method wins and why. / 2026 年对旧方法何时胜出以及为什么的观点。
