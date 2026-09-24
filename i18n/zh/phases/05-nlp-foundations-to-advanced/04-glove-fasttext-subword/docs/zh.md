# 快文和字体嵌入

> 词2Vec训练每字一个嵌入. GloVe因数化了共发生矩阵. 快文本嵌入了零件. BPE 与变压器桥梁.
> 词2Vec 为每一个词训练一个嵌入.

> **【中文解读】**全球利用全局共现统计,FastText 处理子词解决OOV 问题.

**Type:** Build | **类型:** 动手
**Languages:** Python | **语言:** Python
**Prerequisites:** Phase 5 · 03 (Word2Vec from Scratch) | **前置知识:** Phase 5 · 03（Word2Vec 从零实现）
**Time:** ~45 minutes | **时间:** ~45 分钟

## 问题 问题引入

Word2Vec留下了两个问题.

> 两个问题已经解开了.

首先,有一个平行的研究线,直接因子化了共发生矩阵 (LSA,HAL) 而不是在线跳转图更新. Word2Vec的反复方法基本上更好,还是两种方法处理的方式的差异是构成的?**GloVe**答案是:对矩阵因数分解,以精心选择的损失匹配或超过Word2Vec,

> 首先,存在一条并行的研究路线,直接分解共现矩阵 (LSA、HAL),而不是做在线跳转图.**GloVe**回答:配合精心选择的损失函数的矩阵分解匹配或超过Word2Vec,且训练成本更低.

第二,这两种方法都没有一个故事,`Zoomer-approved`现在`dogecoin`任何本质的名词,上周发明,每一个曲的罕见根.**FastText**字符是其部分的总和,包括形态,所以即使是词汇之外的字符也得到了合理的向量.

> 第二,两种方法对从未见过的词都没有解决方案.`Zoomer-approved`,我知道.`dogecoin`、上周刚造的任何专名词、稀有词根的每一个变形形式──**FastText**通过嵌入字符n-gram 修复这个问题:一个词是其各部分之和,包括语素,因此即使是词表外的词也可以获得合理的向量.

第三,当变革者到达时,问题又发生了变化.**Byte-pair encoding (BPE)**现在,我们在研究中发现,每一个现代的代码符号都是一种代码符号.

> 第三,当变革者到来后,问题再次转变.**字节对编码（Byte-Pair Encoding, BPE）**通过学习覆盖一切的高频子词单元词表解决了这个问题.

这一课将包括三个,然后解释哪个是什么时候.

> 现在我们要讲一个一个,然后解释什么时候使用哪个.

## 概念的核心概念

> **【中文解读】**本节介绍核心概念和理论基础.掌握这些概念是后续动手实现的前提,同时也是面试和工程实践中高频考察的知识点.

**GloVe (Global Vectors).**构建一个词-词共发生矩阵`X`在哪里`X[i][j]`是多么经常的词`j`在"字"中出现`i`列车向量,这样`v_i · v_j + b_i + b_j ≈ log(X[i][j])`减肥,所以频繁的对子不占主导地位.

> **GloVe（全局向量）。**构建词-词共现矩阵 `X`在其中`X[i][j]`是词`j`出现在词语`i`上下文中的频率──训练向量使`v_i · v_j + b_i + b_j ≈ log(X[i][j])`对损失加权以使频繁对不主导.

**FastText.**一个词是其字符n-grams的总和加上单词本身.`where`成为`<wh, whe, her, ere, re>, <where>`作为 Word2Vec,训练:不可见的单词 (`whereupon`) 由已知n-gram组成.

> **FastText。**一词是其字符 n-gram 之和加上词本身.`where`变成`<wh, whe, her, ere, re>, <where>`△词向量是这些组件的向量和──像 Word2Vec 一样训练──好处:未见过的词(`whereupon`) 从已知n-gram组合而成

**BPE (Byte-Pair Encoding).**开始使用单个字节 (或字符) 的词汇库. 计算体内每个相邻的对. 将最频繁的对合并成一个新的代币. 重复为 `k`结果:一个词汇库`k + 256`标记,其中频繁的序列 (`ing`现在`tion`现在`the`单个代币,稀有词被分解成熟悉的部分.

> **BPE（字节对编码）。**从单个字节 (或字符) 的词表开始――统计语料中每个相邻的出现频率――将最频繁的对合并为新代币――重复`k`结果:一个`k + 256`个标志的词表,其中高频序列(`ing`,我知道.`tion`,我知道.`the`) 是单个标志,罕见词被分解为熟悉的段落.

> **【拓展：大语言模型的工程实践】**从GPT到ChatGPT,NLP领域经历了从"每个任务训练一个模型"到"一个模型解决所有任务"的范式转变. 在实际工程中,LLM的部署需要考虑代币限制,延迟,成本,安全审查等问题.

> **【拓展：RAG 与企业知识库】**检索增强生成 (RAG) 是当前企业人工智能应用中最流行的架构:将用户查询先检索相关文档片段,再将检索结果作为上下文给LLM 生成答案――这种方式解决了LLM 知识过时和幻觉问题――向量数据库――如Milvus、Pinecone、Weaviate) 是RAG系统的核心组件――

> **【拓展：NLP 的多语言挑战】**全球有7000多种语言,但NLP研究主要集中在英语等少数语言.跨语言迁移学习,多语言预训模型 (如 mBERT,XLM-R) 是解决低资源语言NLP的主要方法.

## 建立它,实现它.

> **【中文解读】**本节通过代码实现从零到核心算法――这种"从零开始"的方式可以帮助理解框架背后的原理,遇到问题时不会被黑盒困住――
```figure
n5-subword-merge
```

## 建立它

### 聚合物:对合发生矩阵进行因素化

```python
import numpy as np
from collections import Counter


def build_cooccurrence(docs, window=5):
    pair_counts = Counter()
    vocab = {}
    for doc in docs:
        for token in doc:
            if token not in vocab:
                vocab[token] = len(vocab)
    for doc in docs:
        indexed = [vocab[t] for t in doc]
        for i, center in enumerate(indexed):
            for j in range(max(0, i - window), min(len(indexed), i + window + 1)):
                if i != j:
                    distance = abs(i - j)
                    pair_counts[(center, indexed[j])] += 1.0 / distance
    return vocab, pair_counts


def glove_train(vocab, pair_counts, dim=16, epochs=100, lr=0.05, x_max=100, alpha=0.75, seed=0):
    n = len(vocab)
    rng = np.random.default_rng(seed)
    W = rng.normal(0, 0.1, size=(n, dim))
    W_tilde = rng.normal(0, 0.1, size=(n, dim))
    b = np.zeros(n)
    b_tilde = np.zeros(n)

    for epoch in range(epochs):
        for (i, j), x_ij in pair_counts.items():
            weight = (x_ij / x_max) ** alpha if x_ij < x_max else 1.0
            diff = W[i] @ W_tilde[j] + b[i] + b_tilde[j] - np.log(x_ij)
            coef = weight * diff

            grad_W_i = coef * W_tilde[j]
            grad_W_tilde_j = coef * W[i]
            W[i] -= lr * grad_W_i
            W_tilde[j] -= lr * grad_W_tilde_j
            b[i] -= lr * coef
            b_tilde[j] -= lr * coef

    return W + W_tilde
```

值得命名的两个移动件.`f(x) = (x/x_max)^alpha`低权重非常频繁的对 (如`(the, and)`总数是总数,总数是总数,总数是总数,总数是总数.`W`其他`W_tilde`总结两者都是一个公布的技巧,

> 两个值得注意的关键点.`f(x) = (x/x_max)^alpha`降低非常频繁的对应`(the, and)`它们的权重,使其不主导损失.`W`语和`W_tilde`对于两者求和是一个已发表的技巧,通常更好只使用其中一个.

### 快文:有潜词的嵌入

```python
def char_ngrams(word, n_min=3, n_max=6):
    wrapped = f"<{word}>"
    grams = {wrapped}
    for n in range(n_min, n_max + 1):
        for i in range(len(wrapped) - n + 1):
            grams.add(wrapped[i:i + n])
    return grams
```

```python
>>> char_ngrams("where")
{'<where>', '<wh', 'whe', 'her', 'ere', 're>', '<whe', 'wher', 'here', 'ere>', '<wher', 'where', 'here>'}
```

每个词由其 n-gram 集合 (通常是3至6个字符) 表示.词嵌入是其 n-gram 嵌入的总和.对于跳转-gram 训练,在 Word2Vec 使用单个向量时,插入此.

> 每个词由其n-gram 集合 (通常是3到6个字符) 表示──词嵌入是其n-gram 嵌入之和──对于跳转gram 训练,将其插入Word2Vec使用单个向量位置──

```python
def fasttext_vector(word, ngram_table):
    grams = char_ngrams(word)
    vecs = [ngram_table[g] for g in grams if g in ngram_table]
    if not vecs:
        return None
    return np.sum(vecs, axis=0)
```

对于一个未见的词,只要知道它的n-gram,你仍然得到一个向量.`whereupon`股票`<wh`现在`her`现在`ere`其他`<where`随着`where`两者彼此靠近.

> 对于未见的词,只要其部分n-gram是已知的,你仍然可以得到一个向量.`whereupon`与`where`共享`<wh`,我知道.`her`,我知道.`ere`和 `<where`所以两者都处于相近的位置.

### 语:学习子词汇

```python
def learn_bpe(corpus, k_merges):
    vocab = Counter()
    for word, freq in corpus.items():
        tokens = tuple(word) + ("</w>",)
        vocab[tokens] = freq

    merges = []
    for _ in range(k_merges):
        pair_freq = Counter()
        for tokens, freq in vocab.items():
            for a, b in zip(tokens, tokens[1:]):
                pair_freq[(a, b)] += freq
        if not pair_freq:
            break
        best = pair_freq.most_common(1)[0][0]
        merges.append(best)

        new_vocab = Counter()
        for tokens, freq in vocab.items():
            new_tokens = []
            i = 0
            while i < len(tokens):
                if i + 1 < len(tokens) and (tokens[i], tokens[i + 1]) == best:
                    new_tokens.append(tokens[i] + tokens[i + 1])
                    i += 2
                else:
                    new_tokens.append(tokens[i])
                    i += 1
            new_vocab[tuple(new_tokens)] = freq
        vocab = new_vocab
    return merges


def apply_bpe(word, merges):
    tokens = list(word) + ["</w>"]
    for a, b in merges:
        new_tokens = []
        i = 0
        while i < len(tokens):
            if i + 1 < len(tokens) and tokens[i] == a and tokens[i + 1] == b:
                new_tokens.append(a + b)
                i += 2
            else:
                new_tokens.append(tokens[i])
                i += 1
        tokens = new_tokens
    return tokens
```

```python
>>> corpus = Counter({"low": 5, "lower": 2, "newest": 6, "widest": 3})
>>> merges = learn_bpe(corpus, k_merges=10)
>>> apply_bpe("lowest", merges)
['low', 'est</w>']
```

首先,重复的重复将最常见的邻居对合并.`low`现在`est`现在`tion`) 成为单个代币,稀有词语也会破碎.

> 第一次代合并最常见的邻居对应.`low`,我知道.`est`,我知道.`tion`) 变成单个标志,罕见词干净地分解――

实际的GPT/BERT/T5代币化器学习了30k-100k的合并.结果:任何文本都将代币化为已知ID的有限长度序列,没有OOV.

> 真正的GPT / BERT / T5 分词器学习3万至10万次合并并.结果:任何文本都被分词为已知ID的有界长序列,永远不会有OOV──

> **【中文解读】**本节展示了如何使用成熟框架 (如PyTorch、HuggingFace等) 快速应用该技术.

> **【拓展：Prompt Engineering 与 LLM 应用】**快速工程已成为NLP工程师的核心技能. 从零射到少射,从思想链到反应,不同的提示策略适用于不同场景. 在实际项目中,系统提示 (系统提示) 的设计直接影响了LLM应用的稳定性和输出质量.

## 用它实现框架

实际上,你很少自己训练这些.

> 在实践中,你几乎从不训练自己这些.

```python
import fasttext.util
fasttext.util.download_model("en", if_exists="ignore")
ft = fasttext.load_model("cc.en.300.bin")
print(ft.get_word_vector("whereupon").shape)
print(ft.get_word_vector("zoomerapproved").shape)
```

对于变压器时代的BPE式子词代码化:

> 对于变压器 时代的BPE 风格子词分词:

```python
from transformers import AutoTokenizer

tok = AutoTokenizer.from_pretrained("gpt2")
print(tok.tokenize("unbelievably tokenized"))
```

```
['un', 'bel', 'iev', 'ably', 'Ġtoken', 'ized']
```

其他`Ġ`预सर्ग标志着词界限 (GPT-2 公约).每个现代代币是BPE变体,WordPiece (BERT),或SentencePiece (T5,LLaMA).

> `Ġ`前标记词边界(GPT-2 的约定) ・・・每个现代分词器都是BPE 变体、WordPiece(BERT) 或句子Piece(T5、LLaMA) ・・・

### 什么时候选择哪个

| Situation | Pick | 场景 | 选择 |
|-----------|------|------|------|
| Pretrained general-purpose word vectors, no OOV tolerance needed | GloVe 300d | 预训练通用词向量，不需要处理 OOV | GloVe 300 维 |
| Pretrained general-purpose word vectors, must handle misspellings / neologisms / morphologically rich languages | FastText | 预训练通用词向量，必须处理拼写错误 / 新词 / 形态丰富的语言 | FastText |
| Anything going into a transformer (training or inference) | Whatever tokenizer the model shipped with. Never swap. | 输入 Transformer 的任何场景（训练或推理） | 模型自带的分词器。永远不要替换。 |
| Training your own language model from scratch | Train a BPE or SentencePiece tokenizer on your corpus first | 从零训练自己的语言模型 | 先在你的语料上训练 BPE 或 SentencePiece 分词器 |
| Production text classification with a linear model | Still TF-IDF. Lesson 02. | 使用线性模型的生产文本分类 | 仍然用 TF-IDF。第 02 课。 |

> **【中文解读】**本节关注如何将模型部署为可用的产品. 从原型到生产级系统需要考虑性能优化,错误处理,监控等多个维度.

## 运送它.

保存如`outputs/skill-embeddings-picker.md`其他:

```markdown
---
name: tokenizer-picker
description: Pick a tokenization approach for a new language model or text pipeline.
version: 1.0.0
phase: 5
lesson: 04
tags: [nlp, tokenization, embeddings]
---

Given a task and dataset description, you output:

1. Tokenization strategy (word-level, BPE, WordPiece, SentencePiece, byte-level). One-sentence reason.
2. Vocabulary size target (e.g., 32k for an English-only LM, 64k-100k for multilingual).
3. Library call with the exact training command. Name the library. Quote the arguments.
4. One reproducibility pitfall. Tokenizer-model mismatch is the single most common silent production bug; call out which pair must be used together.

> **【中文解读】** 练习题按照 Easy/Medium/Hard 三个难度递进。建议至少完成 Medium 级别的题目，Hard 级别适合深入研究或面试准备。

Refuse to recommend training a custom tokenizer when the user is fine-tuning a pretrained LLM. Refuse to recommend word-level tokenization for any model targeting production inference. Flag non-English / multi-script corpora as needing SentencePiece with byte fallback.
```

## 练习题

1. **Easy.**跑步`char_ngrams("playing")`其他`char_ngrams("played")`计算两个n-gram集合的Jaccard重叠.`pla`现在`lay`现在`play`),这就是为什么FastText很好地转移到其他形式变体中.
   **简单。**运行`char_ngrams("playing")`和 `char_ngrams("played")`△计算两个n-gram 集合的Jaccard 重叠度──你应该看到大量的共享片段(`pla`,我知道.`lay`,我知道.`play`),这就是FastText在形态变体间的良好迁移的原因.
2. **Medium.**延长时间`learn_bpe`根据数组合数,绘制每个字符的代码.你应该看到快速的压缩,每代码的压缩量接近2-3个字符.
   **中等。**扩展`learn_bpe`以跟踪词表增长――绘制每个语料字符的符号 数作为合并次数的函数――你应该看到开始时快速缩小,在约2-3 字符/符号附近渐近――
3. **Hard.**训练一个K合并BPE在莎士比亚的完整作品.比较普通词的标记与罕见的正名词. 测量每字的平均标记前后.写出你惊的东西.
   **困难。**在莎士比亚全集上练习1000次合并的BPE──比较常见词与罕见专名词的分词结果──测量前后的平均每词符号数──写下让你惊的地方──

> **【中文解读】**练习题按照易/中/难 三个难度递进;;建议至少完成中级题,Hard级适合深入研究或面试准备;;

## 关键词 快速查找表

| Term | What people say | What it actually means | 术语 | 人们常说的 | 实际含义 |
|------|-----------------|-----------------------|------|-----------|---------|
| Co-occurrence matrix | Word-word frequency table | `X[i][j]` = how often word `j` appears in a window around word `i`. | 共现矩阵 | 词-词频率表 | `X[i][j]` = 词 `j` 在词 `i` 周围窗口中出现的频率。 |
| Subword | Piece of a word | A character n-gram (FastText) or learned token (BPE/WordPiece/SentencePiece). | 子词 | 词的片段 | 字符 n-gram（FastText）或学习到的 token（BPE/WordPiece/SentencePiece）。 |
| BPE | Byte-pair encoding | Iterative merging of most-frequent adjacent pairs until vocabulary hits target size. | BPE（字节对编码） | 字节对编码 | 迭代合并最频繁的相邻对，直到词表达到目标大小。 |
| OOV | Out of vocabulary | Word the model has never seen. Word2Vec/GloVe fail. FastText and BPE handle it. | OOV（词表外） | 词表外 | 模型从未见过的词。Word2Vec/GloVe 会失败。FastText 和 BPE 能处理。 |
| Byte-level BPE | BPE on raw bytes | GPT-2's scheme. Vocabulary starts with 256 bytes, so nothing is ever OOV. | 字节级 BPE | 对原始字节的 BPE | GPT-2 的方案。词表从 256 个字节开始，所以永远不会有 OOV。 |

> **【中文解读】**在团队协作中,统一术语定义可以避免大量沟通误解.

## 继续阅读 继续阅读

- [Pennington, Socher, Manning (2014). GloVe: Global Vectors for Word Representation](https://nlp.stanford.edu/pubs/glove.pdf) GloVe论文,七页,仍然是损失的最佳衍生.
- [Bojanowski et al. (2017). Enriching Word Vectors with Subword Information](https://arxiv.org/abs/1607.04606)快文文. /快文文论文。
- [Sennrich, Haddow, Birch (2016). Neural Machine Translation of Rare Words with Subword Units](https://arxiv.org/abs/1508.07909)将BPE引入现代NLP的论文.
- [Hugging Face tokenizer summary](https://huggingface.co/docs/transformers/tokenizer_summary)BPE,WordPiece和SentencePiece实际上在实践中是如何不同的.
