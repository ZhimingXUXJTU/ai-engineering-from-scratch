# 词嵌入 — Word2Vec 从零实现

> 一个词取决于它所保持的公司。在这个想法上训练一个浅层网络，几何就自然涌现了。

> **【中文解读】** Word2Vec 把词映射到稠密向量空间，相似词在向量空间中接近。这是现代 NLP 的基石。

**类型：** 构建
**编程语言：** Python
**前置课程：** Phase 5 · 02（BoW + TF-IDF），Phase 3 · 03（反向传播从零实现）
**预计时长：** ~75 分钟

## 问题引入

TF-IDF 知道 `dog` 和 `puppy` 是不同的词。它不知道它们的意思几乎相同。在 `dog` 上训练的分类器无法泛化到关于 `puppy` 的评论。你可以通过列出同义词来弥补，但这在罕见术语、领域行话和你没有预料到的每种语言上都会失败。

> **【中文解读】** 本节提出的问题是：如何在实际工程中正确理解和应用这一技术。理解问题背景有助于把握技术选型的关键决策点。在实际 AI 系统中，错误的技术选型往往比实现细节的 bug 代价更高。


你想要一种表示，让 `dog` 和 `puppy` 在空间中靠近。让 `king - man + woman` 落在 `queen` 附近。让在 `dog` 上训练的模型免费向 `puppy` 传递一些信号。

Word2Vec 给了我们这样的空间。两层神经网络，万亿 token 的训练运行，2013 年发表。架构简单到令人尴尬。结果重塑了 NLP 十年。

## 核心概念

> **【中文解读】** 本节介绍核心概念和理论基础。掌握这些概念是后续动手实现的前提，同时也是面试和工程实践中高频考察的知识点。


**分布假设（Distributional Hypothesis）**（Firth, 1957）："你将通过一个词所保持的公司来认识它。" 如果两个词出现在相似的上下文中，它们可能意味着相似的事物。

Word2Vec 有两种变体，都利用了这个想法。

- **Skip-gram（跳字模型）。** 给定中心词，预测周围的词。`cat -> (the, sat, on)`，窗口大小为 2。
- **CBOW（连续词袋模型）。** 给定周围的词，预测中心词。`(the, sat, on) -> cat`。

Skip-gram 训练较慢但更好地处理罕见词。它成为了默认选择。

网络有一个不带非线性激活函数的隐藏层。输入是词表上的 one-hot 向量。输出是词表上的 softmax。训练后，你丢弃输出层。隐藏层的权重就是嵌入。

```
one-hot(center) ── W ──▶ hidden (d-dim) ── W' ──▶ softmax(vocab)
                          ^
                          this is the embedding
```

诀窍：对 10 万个词做 softmax 代价太高。Word2Vec 使用**负采样（Negative Sampling）** 将其转化为二分类任务。预测 "这个上下文词是否出现在这个中心词附近，是或否"。每个训练对采样少量负例（非共现词），而不是对整个词表计算 softmax。

> **【拓展：大语言模型的工程实践】** 从 GPT 到 ChatGPT，NLP 领域经历了从 "每个任务训练一个模型" 到 "一个模型解决所有任务" 的范式转变。在实际工程中，LLM 的部署需要考虑 Token 限制、延迟、成本、安全审查等问题。LangChain、LlamaIndex 等框架简化了 LLM 应用的开发。

> **【拓展：RAG 与企业知识库】** 检索增强生成（RAG）是当前企业 AI 应用最流行的架构：将用户查询先检索相关文档片段，再将检索结果作为上下文喂给 LLM 生成答案。这种方式解决了 LLM 知识过时和幻觉问题。向量数据库（如 Milvus、Pinecone、Weaviate）是 RAG 系统的核心组件。

> **【拓展：NLP 的多语言挑战】** 全球有 7000+ 种语言，但 NLP 研究主要集中在英语等少数语言。跨语言迁移学习、多语言预训练模型（如 mBERT、XLM-R）是解决低资源语言 NLP 的主要方法。字节级模型（如 ByT5）甚至可以在无分词器的情况下处理任何语言。





## 动手实现

> **【中文解读】** 本节通过代码从零实现核心算法。这种 "from scratch" 的方式能帮助理解框架背后的原理，遇到问题时不会被黑盒困住。


### 步骤 1：从语料库生成训练对

```python
def skipgram_pairs(docs, window=2):
    pairs = []
    for doc in docs:
        for i, center in enumerate(doc):
            for j in range(max(0, i - window), min(len(doc), i + window + 1)):
                if i == j:
                    continue
                pairs.append((center, doc[j]))
    return pairs
```

```python
>>> skipgram_pairs([["the", "cat", "sat", "on", "mat"]], window=2)
[('the', 'cat'), ('the', 'sat'),
 ('cat', 'the'), ('cat', 'sat'), ('cat', 'on'),
 ('sat', 'the'), ('sat', 'cat'), ('sat', 'on'), ('sat', 'mat'),
 ...]
```

窗口中的每个（中心词，上下文词）对都是一个正训练样本。

### 步骤 2：嵌入表

两个矩阵。`W` 是中心词嵌入表（你保留的那个）。`W'` 是上下文词表（通常丢弃，有时与 `W` 取平均）。

```python
import numpy as np


def init_embeddings(vocab_size, dim, seed=0):
    rng = np.random.default_rng(seed)
    W = rng.normal(0, 0.1, size=(vocab_size, dim))
    W_prime = rng.normal(0, 0.1, size=(vocab_size, dim))
    return W, W_prime
```

小随机初始化。词表大小 1 万、维度 100 是现实的；教学用 50 词表 x 16 维就足以看到几何效果。

### 步骤 3：负采样目标函数

对每个正样本对 `(center, context)`，从词表中采样 `k` 个随机词作为负例。训练模型使正例的点积 `W[center] · W'[context]` 高，负例的低。

```python
def sigmoid(x):
    return 1.0 / (1.0 + np.exp(-np.clip(x, -20, 20)))


def train_pair(W, W_prime, center_idx, context_idx, negative_indices, lr):
    v_c = W[center_idx]
    u_pos = W_prime[context_idx]
    u_negs = W_prime[negative_indices]

    pos_score = sigmoid(v_c @ u_pos)
    neg_scores = sigmoid(u_negs @ v_c)

    grad_center = (pos_score - 1) * u_pos
    for i, u in enumerate(u_negs):
        grad_center += neg_scores[i] * u

    W[context_idx] = W[context_idx]
    W_prime[context_idx] -= lr * (pos_score - 1) * v_c
    for i, neg_idx in enumerate(negative_indices):
        W_prime[neg_idx] -= lr * neg_scores[i] * v_c
    W[center_idx] -= lr * grad_center
```

神奇的公式：正例对上的逻辑损失（希望 sigmoid 接近 1）加上负例对上的逻辑损失（希望 sigmoid 接近 0）。梯度流向两个表。完整推导见原始论文；如果你想让它深入理解，用纸笔走一遍。

### 步骤 4：在玩具语料上训练

```python
def train(docs, dim=16, window=2, k_neg=5, epochs=100, lr=0.05, seed=0):
    vocab = build_vocab(docs)
    vocab_size = len(vocab)
    rng = np.random.default_rng(seed)
    W, W_prime = init_embeddings(vocab_size, dim, seed=seed)
    pairs = skipgram_pairs(docs, window=window)

    for epoch in range(epochs):
        rng.shuffle(pairs)
        for center, context in pairs:
            c_idx = vocab[center]
            ctx_idx = vocab[context]
            negs = rng.integers(0, vocab_size, size=k_neg)
            negs = [n for n in negs if n != ctx_idx and n != c_idx]
            train_pair(W, W_prime, c_idx, ctx_idx, negs, lr)
    return vocab, W
```

在大语料上经过足够多的轮次后，共享上下文的词具有相似的中心词嵌入。在玩具语料上，效果微弱。在数十亿 token 上，效果惊人。

### 步骤 5：类比技巧

```python
def nearest(vocab, W, target_vec, topk=5, exclude=None):
    exclude = exclude or set()
    inv_vocab = {i: w for w, i in vocab.items()}
    norms = np.linalg.norm(W, axis=1, keepdims=True) + 1e-9
    W_norm = W / norms
    target = target_vec / (np.linalg.norm(target_vec) + 1e-9)
    sims = W_norm @ target
    order = np.argsort(-sims)
    out = []
    for i in order:
        if i in exclude:
            continue
        out.append((inv_vocab[i], float(sims[i])))
        if len(out) == topk:
            break
    return out


def analogy(vocab, W, a, b, c, topk=5):
    v = W[vocab[b]] - W[vocab[a]] + W[vocab[c]]
    return nearest(vocab, W, v, topk=topk, exclude={vocab[a], vocab[b], vocab[c]})
```

在预训练的 300 维 Google News 向量上：

```python
>>> analogy(vocab, W, "man", "king", "woman")
[('queen', 0.71), ('monarch', 0.62), ('princess', 0.59), ...]
```

`king - man + woman = queen`。不是因为模型知道什么是王室。而是因为向量 `(king - man)` 捕获了类似 "王室" 的东西，将它加到 `woman` 上落在王室女性区域附近。

> **【中文解读】** 本节展示如何用成熟框架（如 PyTorch、HuggingFace 等）快速应用该技术。在实际项目中，优先使用经过验证的框架实现，可以减少 bug 并提高开发效率。




> **【拓展：Prompt Engineering 与 LLM 应用】** Prompt Engineering 已成为 NLP 工程师的核心技能。从 Zero-shot 到 Few-shot，从 Chain-of-Thought 到 ReAct，不同的提示策略适用于不同场景。在实际项目中，系统提示（System Prompt）的设计直接影响 LLM 应用的稳定性和输出质量。

## 用框架实现

从零编写 Word2Vec 是为了教学。生产 NLP 使用 `gensim`。

```python
from gensim.models import Word2Vec

sentences = [
    ["the", "cat", "sat", "on", "the", "mat"],
    ["the", "dog", "ran", "across", "the", "room"],
]

model = Word2Vec(
    sentences,
    vector_size=100,
    window=5,
    min_count=1,
    sg=1,
    negative=5,
    workers=4,
    epochs=30,
)

print(model.wv["cat"])
print(model.wv.most_similar("cat", topn=3))
```

实际工作中，你几乎从不自己训练 Word2Vec。你下载预训练向量。

- **GloVe** — 斯坦福的共现矩阵分解方法。50 维、100 维、200 维、300 维的检查点。通用覆盖良好。第 04 课专门讲解 GloVe。
- **fastText** — Facebook 的 Word2Vec 扩展，嵌入字符 n-gram。通过组合子词处理词表外词。第 04 课。
- **Google News 预训练 Word2Vec** — 300 维，300 万词表，2013 年发布。至今每天都有人下载。

### Word2Vec 在 2026 年仍然胜出的场景

- 轻量级领域特定检索。在笔记本上用一小时在医学摘要上训练，获得通用模型无法捕获的专用向量。
- 类比式特征工程。`gender_vector = mean(man - woman pairs)`。从其他词中减去它以获得性别中性轴。仍在公平性研究中使用。
- 可解释性。100 维足够小，可以通过 PCA 或 t-SNE 绘图并实际看到聚类形成。
- 任何需要在没有 GPU 的设备上运行推理的场景。Word2Vec 查找就是单行获取。

### Word2Vec 失败的场景

多义词壁垒。`bank` 只有一个向量。`river bank` 和 `financial bank` 共享它。`table`（电子表格 vs. 家具）共享它。下游分类器无法从向量中区分不同含义。

上下文嵌入（ELMo、BERT 以及之后的所有 Transformer）通过根据周围上下文为每个词的出现产生不同的向量解决了这个问题。这就是从 Word2Vec 到 BERT 的跳跃：从静态到上下文。Phase 7 涵盖 Transformer 部分。

词表外（Out-of-Vocabulary）问题是另一个失败。如果 `Zoomer-approved` 不在训练数据中，Word2Vec 就从未见过它。没有后备方案。fastText 通过子词组合修复了这个问题（第 04 课）。

> **【中文解读】** 本节关注如何将模型部署为可用的产品。从原型到生产级系统需要考虑性能优化、错误处理、监控等多个维度。



## 产出物

保存为 `outputs/skill-embedding-probe.md`：

```markdown
---
name: embedding-probe
description: Inspect a word2vec model. Run analogies, find neighbors, diagnose quality.
version: 1.0.0
phase: 5
lesson: 03
tags: [nlp, embeddings, debugging]
---

You probe trained word embeddings to verify they are working. Given a `gensim.models.KeyedVectors` object and a vocabulary, you run:

1. Three canonical analogy tests. `king : man :: queen : woman`. `paris : france :: tokyo : japan`. `walking : walked :: swimming : ?`. Report the top-1 result and its cosine.
2. Five nearest-neighbor tests on domain-specific words the user supplies. Print top-5 neighbors with cosines.
3. One symmetry check. `similarity(a, b) == similarity(b, a)` to within float precision.
4. One degenerate check. If any embedding has a norm below 0.01 or above 100, the model has a training bug. Flag it.

> **【中文解读】** 练习题按照 Easy/Medium/Hard 三个难度递进。建议至少完成 Medium 级别的题目，Hard 级别适合深入研究或面试准备。


Refuse to declare a model good on analogy accuracy alone. Analogy benchmarks are gameable and do not transfer to downstream tasks. Recommend intrinsic + downstream evaluation together.
```

## 练习题

1. **简单。** 在一个小语料上运行训练循环（20 句关于猫和狗的句子）。200 轮后，验证 `nearest(vocab, W, W[vocab["cat"]])` 返回的 top 3 中包含 `dog`。如果没有，增加轮次或词表。
2. **中等。** 添加高频词子采样。频率高于 `10^-5` 的词按与其频率成正比的概率从训练对中丢弃。测量对罕见词相似度的影响。
3. **困难。** 在 20 Newsgroups 语料上训练模型。计算两个偏见轴：`he - she` 和 `doctor - nurse`。将职业词投影到两个轴上。报告哪些职业有最大的偏见差距。这是公平性研究人员使用的那种探测。

> **【中文解读】** 术语表中的 "What people say" vs "What it actually means" 区分了日常口语和精确技术含义。在团队协作中，统一术语定义可以避免大量沟通误解。


## 术语速查表

| 术语 | 人们常说的 | 实际含义 |
|------|-----------|---------|
| 词嵌入 | 词向量 | 从上下文学习的稠密、低维（通常 100-300）表示。 |
| Skip-gram | Word2Vec 技巧 | 从中心词预测上下文词。比 CBOW 慢，对罕见词更好。 |
| 负采样 | 训练捷径 | 用对 `k` 个随机词的二分类替换对整个词表的 softmax。 |
| 静态嵌入 | 每个词一个向量 | 无论上下文如何都是同一个向量。在多义词上失败。 |
| 上下文嵌入 | 上下文敏感向量 | 根据周围词，每次出现都是不同的向量。Transformer 产生的。 |
| OOV（词表外） | 词表外 | 训练中未见过的词。Word2Vec 无法为这些词产生向量。 |

> **【中文解读】** 延伸阅读提供了深入学习的高质量资源。这些论文和教程是该领域的经典参考文献，适合需要深入理解的读者。


## 延伸阅读

- [Mikolov et al. (2013). Distributed Representations of Words and Phrases and their Compositionality](https://arxiv.org/abs/1310.4546) — 负采样论文。短小易读。
- [Rong, X. (2014). word2vec Parameter Learning Explained](https://arxiv.org/abs/1411.2738) — 最清晰的梯度推导，如果你觉得原始论文的数学太密集。
- [gensim Word2Vec tutorial](https://radimrehurek.com/gensim/models/word2vec.html) — 真正有效的生产训练设置。
