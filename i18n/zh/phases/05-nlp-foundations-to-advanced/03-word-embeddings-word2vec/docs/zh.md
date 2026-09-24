# 词嵌入  Word2Vec从零开始

> 对于这个想法,就会有微小的网络,而几何则会掉下来.
> 一个词取决于它所持有的公司.

> **【中文解读】**Word2Vec 把词映射到密向量空间,相似词在向量空间中接近――这是现代NLP的基石――

**Type:** Build | **类型:** 动手
**Languages:** Python | **语言:** Python
**Prerequisites:** Phase 5 · 02 (BoW + TF-IDF), Phase 3 · 03 (Backpropagation from Scratch) | **前置知识:** Phase 5 · 02（BoW + TF-IDF），Phase 3 · 03（反向传播从零实现）
**Time:** ~75 minutes | **时间:** ~75 分钟

## 问题 问题引入

国际特种基金会知道`dog`其他`puppy`它们几乎意味着同一个东西.`dog`无法将其总体化为关于`puppy`您可以通过列出同义词来记录下这一点, 但这在罕见的术语,域名语和你不预料的每一种语言上都失败了.

>  TF-IDF 知道`dog`和 `puppy`是不同的词. 它不知道它们的意思几乎相同.`dog`训练中的分类器不能泛化到关于`puppy`评论. 你可以通过列出同义词来弥补,但这在罕见的术语,领域的行言和你没有预料的每种语言都会失败.

你想要一个代表,`dog`其他`puppy`太空中的陆地.`king - man + woman`附近的土地`queen`模型在哪里训练`dog`传输一些信号到`puppy`免费的.

> 你想要一种表示,让`dog`和 `puppy`在空间中靠近.`king - man + woman`落在`queen`附近的.`dog`上训练的模型免费向`puppy`传递一些信号.

Word2Vec给了我们这个空间. 两个层神经网络,数万亿代币的训练运行,发表于2013年. 架构几乎是令人尬的简单.

> 据悉,Word2Vec 给了我们这样的空间.

## 概念的核心概念

> **【中文解读】**本节介绍核心概念和理论基础.掌握这些概念是后续动手实现的前提,同时也是面试和工程实践中高频考察的知识点.

**Distributional hypothesis**"你会从一个词的朋友中知道" (第一个,1957年).

> **分布假设（Distributional Hypothesis）**"如果你两个词出现相似的上下文,它们可能意味着相似的事物.

两种风味,两种利用这个想法.

> 两种变化,都利用了这个想法.

- **Skip-gram.**给一个中心词,预测周围的词.`cat -> (the, sat, on)`窗口尺寸2
  **Skip-gram（跳字模型）。**给定中心词,预测周围的词――`cat -> (the, sat, on)`窗户大小为2个.
- **CBOW (continuous bag of words).**根据周围的词汇,预测中心.`(the, sat, on) -> cat`现在,我们要去.
  **CBOW（连续词袋模型）。**给定周围的词,预测中心词――`(the, sat, on) -> cat`,我知道.

跳转语法训练速度较慢,但处理稀有词语更好.

> 跳转语法训练较慢,但更好处理罕见词.

网络有一个隐藏的层,没有线性.输入是词汇上的一个热向量.输出是词汇上的软最大.训练后,你扔掉输出层.隐藏的层重量是嵌入.

> 网络有一个不带线性激活函数的隐藏层――输入是单词表上的热向量――输出是单词表上的软max――训练后,你丢弃输出层――隐藏层的权重就是嵌入――

```
one-hot(center) ── W ──▶ hidden (d-dim) ── W' ──▶ softmax(vocab)
                          ^
                          this is the embedding
```

软max超过100万字是非常昂贵的.**negative sampling**预测"这个文本词是否出现在这个中文字附近,是的或是的". 通过每一个训练对的少数负面 (非同发生) 字样,而不是计算整个词汇中的软max.

> :对10万个词做软最大价格太高――Word2Vec 使用**负采样（Negative Sampling）**预测"这个上下文词是否出现在这个中心词附近,是或否"......每个训练对采样少量负例 (非共现词),而不是对整个词表计算软max。

> **【拓展：大语言模型的工程实践】**从GPT到ChatGPT,NLP领域经历了从"每个任务训练一个模型"到"一个模型解决所有任务"的范式转变. 在实际工程中,LLM的部署需要考虑代币限制,延迟,成本,安全审查等问题.

> **【拓展：RAG 与企业知识库】**检索增强生成 (RAG) 是当前企业人工智能应用中最流行的架构:将用户查询先检索相关文档片段,再将检索结果作为上下文给LLM 生成答案――这种方式解决了LLM 知识过时和幻觉问题――向量数据库――如Milvus、Pinecone、Weaviate) 是RAG系统的核心组件――

> **【拓展：NLP 的多语言挑战】**全球有7000多种语言,但NLP研究主要集中在英语等少数语言.跨语言迁移学习,多语言预训模型 (如 mBERT,XLM-R) 是解决低资源语言NLP的主要方法.

## 建立它,实现它.

> **【中文解读】**本节通过代码实现从零到核心算法――这种"从零开始"的方式可以帮助理解框架背后的原理,遇到问题时不会被黑盒困住――
```figure
word-vector-arithmetic
```

## 建立它

### 步骤1:从一个体内训练对

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

每个窗口中的 (中心,背景) 双是积极的训练例子.

> 窗户中的每个中心词,上下文词) 对都是正确的训练样本.

### 步骤 2:嵌入表

两个矩阵.`W`是一个中文字嵌入表 (你保留的表).`W'`文本词表 (通常被丢弃,有时平均为`W`)

> 两个矩阵.`W`是中心词嵌入表(你保留的那个)`W'`是上下文词表(通常丢弃,有时与`W`取平均) 〔

```python
import numpy as np


def init_embeddings(vocab_size, dim, seed=0):
    rng = np.random.default_rng(seed)
    W = rng.normal(0, 0.1, size=(vocab_size, dim))
    W_prime = rng.normal(0, 0.1, size=(vocab_size, dim))
    return W, W_prime
```

字母大小10k和色100是现实的;用于教学,50字母×16色足以看到几何.

> 小随机初始化──词表大小1万、度100是现实的;教学用50个词表 x16个维就足以看到几何效果──

### 步骤3:负样本目标

对于每一个正数对`(center, context)`样本`k`训练模型,所以点产量`W[center] · W'[context]`对于积极的情况来说,高,对于负面的情况来说,低.

> 对每一个正确的样本`(center, context)`从词表中采样`k`个随机词作为负例――训练模型使正例的点积`W[center] · W'[context]`高,负例的低.

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

魔术公式:正对的物流损失 (想要sigmoid接近1) 加上负对的物流损失 (想要sigmoid接近0). 渐变体向两个表流动.完整的衍生是在原始纸上;如果你想它粘着,用笔和纸一次穿过它.

> 神奇的公式:正例对逻辑损失 希望 sigmoid 接近 1)加上负例对逻辑损失 希望 sigmoid 接近 0) △梯度流向两个表.

### 步骤4:在玩具体上训练

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

在一个大型的体积上,经过足够的时代,分享背景的词语具有类似的中心嵌入.在一个玩具体积上,你看到了效果微弱.在数十亿的代币上,你看到了戏剧性.

> 在大语料上经历了足够多轮次后,分享下文上的词具有类似的中心词嵌入.在玩具语料上,效果微弱.在数十亿代币上,效果惊人.

### 步骤5:比喻技巧

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

在预训练的300d谷歌新闻载体上:

```python
>>> analogy(vocab, W, "man", "king", "woman")
[('queen', 0.71), ('monarch', 0.62), ('princess', 0.59), ...]
```

`king - man + woman = queen`不是因为模型知道皇室是什么,而是因为向量`(king - man)`像"皇家"这样的东西,`woman`靠近皇室妇女地区的土地.

> `king - man + woman = queen`不是因为模型知道王室是什么,而是因为向量.`(king - man)`抓住类似王室的东西,将它添加到`woman`上落在王室女性区域附近.

> **【中文解读】**本节展示了如何使用成熟框架 (如PyTorch、HuggingFace等) 快速应用该技术.

> **【拓展：Prompt Engineering 与 LLM 应用】**快速工程已成为NLP工程师的核心技能. 从零射到少射,从思想链到反应,不同的提示策略适用于不同场景. 在实际项目中,系统提示 (系统提示) 的设计直接影响了LLM应用的稳定性和输出质量.

## 用它实现框架

编写Word2Vec从零开始就是教学.`gensim`现在,我们要去.

> 从零编写 Word2Vec 是为了教学.`gensim`,我知道.

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

对于真正的工作,你几乎从来没有训练Word2Vec.

> 实际工作中,你几乎没有自学训练 Word2Vec──你下载预训练向量──

- **GloVe**斯坦福的共发生矩阵因数化方法. 50d, 100d, 200d, 300d检查站.
  **GloVe**斯坦福的共现矩阵分解方法──50维,100维,200维300维的检查点──通用覆盖良好──第04课专讲全球化──
- **fastText**Facebook的 Word2Vec扩展,嵌入了字符n图.通过编写子词来处理词汇库之外的单词. 第04课.
  **fastText**Facebook的 Word2Vec 扩展,嵌入字符n-gram──通过组合子词处理词表外词──第04课──
- **Pretrained Word2Vec on Google News** 300d,3M字词库,发表于 2013. 仍然每天下载.
  **Google News 预训练 Word2Vec** 300 维,300万词表,2013年发布.至今每天都有人下载.

### 在2026年Word2Vec仍然赢得胜利时

- 通过笔记本电脑,在一个小时内训练医学摘要,获得专业的向量,没有一般模型捕获.
  轻量级领域的特定检查. 在笔记本上,在一小时的医学摘要上训练,获得通用模型无法捕获的专用向量.
- 类似的特征工程.`gender_vector = mean(man - woman pairs)`现在还在公平研究中使用.
  类比式特征工程――`gender_vector = mean(man - woman pairs)`△从其他词中减去它以获得性别中性轴──仍在公平性研究中使用──
- 它们可以通过PCA或t-SNE绘制图,并实际上看到集群的形成.
  可解释性──100维足够小,可以通过PCA或t-SNE绘图并实际看到聚类形成──
- 任何地方的推断都必须在设备上运行,没有GPU.
  任何需要在没有GPU的设备上运行的情况.

### Word2Vec 失败的地方

聚墙.`bank`只有一个向量.`river bank`其他`financial bank`让我们分享.`table`后游分类器不能区分感官和向量.

> 多义词壁垒――`bank`只有一个向量.`river bank`和 `financial bank`分享它.`table`电表格与家具共享它.

基于周围的环境,语境嵌入式 (ELMo,BERT,自此以来的每个变压器) 通过根据周围的环境生成一个不同的向量来解决这一问题.这就是从Word2Vec到BERT的跳跃:从静态到语境.第7阶段涵盖变压器的一半.

> 上下文嵌入 (ELMo、BERT 以及之后的所有变压器) 通过周围的下文以每个词的出现产生不同的向量解决了这个问题.

其他失败是词汇缺失问题.`Zoomer-approved`如果没有在训练数据中.没有倒退. fastText通过子词组合来解决这一问题 (课04).

> 词表外(出口词库) 问题是另一个失败――如果`Zoomer-approved`在训练数据中,Word2Vec 就从来没有见过它.

> **【中文解读】**本节关注如何将模型部署为可用的产品. 从原型到生产级系统需要考虑性能优化,错误处理,监控等多个维度.

## 运送它.

保存如`outputs/skill-embedding-probe.md`其他:

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

1. **Easy.**经过200个时代,检查 子的子.`nearest(vocab, W, W[vocab["cat"]])`收益`dog`如果没有,则增加时代或词汇库.
   **简单。**在一个小语料上运行训练循环 (关于猫和狗的句子)`nearest(vocab, W, W[vocab["cat"]])`返回的前三中包含`dog`如果没有,增加轮次或词表.
2. **Medium.**增加频率字的子样本.`10^-5`测量对稀有词的相似性的影响.
   **中等。**添加高频词子采样──频率高于 `10^-5`根据其频率成正比的概率从训练中丢弃.
3. **Hard.**根据20个新闻群体的模型进行训练.`he - she`其他`doctor - nurse`报告哪些职业有最大的偏差差. 这种类型的探测器公平性研究人员使用.
   **困难。**在20个新闻群中语料上训练模型――计算两个偏见轴:`he - she`和 `doctor - nurse`将职业词投影到两个轴上. 报告哪些职业有最大偏见差距.

> **【中文解读】**练习题按照易/中/难 三个难度递进;;建议至少完成中级题,Hard级适合深入研究或面试准备;;

## 关键词 快速查找表

| Term | What people say | What it actually means | 术语 | 人们常说的 | 实际含义 |
|------|-----------------|-----------------------|------|-----------|---------|
| Word embedding | Word as a vector | A dense, low-dim (typically 100-300) representation learned from context. | 词嵌入 | 词向量 | 从上下文学习的稠密、低维（通常 100-300）表示。 |
| Skip-gram | Word2Vec trick | Predict context words from center word. Slower than CBOW, better for rare words. | Skip-gram | Word2Vec 技巧 | 从中心词预测上下文词。比 CBOW 慢，对罕见词更好。 |
| Negative sampling | Training shortcut | Replace softmax over full vocab with binary classification against `k` random words. | 负采样 | 训练捷径 | 用对 `k` 个随机词的二分类替换对整个词表的 softmax。 |
| Static embedding | One vector per word | Same vector regardless of context. Fails on polysemy. | 静态嵌入 | 每个词一个向量 | 无论上下文如何都是同一个向量。在多义词上失败。 |
| Contextual embedding | Context-sensitive vector | Different vector for each occurrence based on surrounding words. What transformers produce. | 上下文嵌入 | 上下文敏感向量 | 根据周围词，每次出现都是不同的向量。Transformer 产生的。 |
| OOV | Out of vocabulary | Word not seen in training. Word2Vec cannot produce a vector for these. | OOV（词表外） | 词表外 | 训练中未见过的词。Word2Vec 无法为这些词产生向量。 |

> **【中文解读】**在团队协作中,统一术语定义可以避免大量沟通误解.

## 继续阅读 继续阅读

- [Mikolov et al. (2013). Distributed Representations of Words and Phrases and their Compositionality](https://arxiv.org/abs/1310.4546)负采样论文──短小易读──短短可读.
- [Rong, X. (2014). word2vec Parameter Learning Explained](https://arxiv.org/abs/1411.2738)最清晰的梯度推导,如果原始论文的数学太密集──
- [gensim Word2Vec tutorial](https://radimrehurek.com/gensim/models/word2vec.html)实际上工作的生产训练设置.
