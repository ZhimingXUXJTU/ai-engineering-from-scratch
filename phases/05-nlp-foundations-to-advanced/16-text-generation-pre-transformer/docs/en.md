# Text Generation Before Transformers — N-gram Language Models | Transformer 之前的文本生成 — N-gram 语言模型

> If a word is surprising, the model is bad. Perplexity makes surprise a number. Smoothing keeps it finite.
> 如果一个词令人惊讶，模型就不好。困惑度把惊讶变成数字。平滑让它保持有限。

> **【中文解读】** N-gram 统计词频预测下一个词。GPT 就是更强大的语言模型。

**Type:** Build | **类型:** 动手
**Languages:** Python | **语言:** Python
**Prerequisites:** Phase 5 · 01 (Text Processing), Phase 2 · 14 (Naive Bayes) | **前置知识:** Phase 5 · 01（文本处理），Phase 2 · 14（朴素贝叶斯）
**Time:** ~45 minutes | **时间:** ~45 分钟

## The Problem | 问题引入

Before transformers, before RNNs, before word embeddings, a language model predicted the next word by counting how often it followed the previous `n-1` words. Count "the cat" → "sat" 47 times, "the cat" → "jumped" 12 times, "the cat" → "refrigerator" 0 times. Normalize to get a probability distribution.

> 在 Transformer 之前，在 RNN 之前，在词嵌入之前，语言模型通过统计前 `n-1` 个词后面跟着当前词的频率来预测下一个词。统计 "the cat" → "sat" 出现 47 次，"the cat" → "jumped" 出现 12 次，"the cat" → "refrigerator" 出现 0 次。归一化得到概率分布。

> **【中文解读】** 本节提出的问题是：如何在实际工程中正确理解和应用这一技术。理解问题背景有助于把握技术选型的关键决策点。在实际 AI 系统中，错误的技术选型往往比实现细节的 bug 代价更高。

That is an n-gram language model. It ran every speech recognizer, every spell checker, and every phrase-based machine translation system from 1980 through 2015. It still runs when you need cheap on-device language modeling.

> 这就是 n-gram 语言模型。从 1980 年到 2015 年，它运行在每个语音识别器、每个拼写检查器和每个基于短语的机器翻译系统中。当你需要廉价的设备端语言建模时，它仍在运行。

The interesting problem is what to do about unseen n-grams. A raw count-based model assigns zero probability to anything it has not seen, which is catastrophic because sentences are long and almost every long sentence contains at least one unseen sequence. Fifty years of smoothing research fixed that. Kneser-Ney smoothing is the result, and modern deep learning inherited its empirical tradition.

> 有趣的问题是：如何处理未见的 n-gram。原始的基于计数的模型对任何未见过的东西分配零概率，这是灾难性的，因为句子很长，几乎每个长句子都包含至少一个未见序列。五十年的平滑研究解决了这个问题。Kneser-Ney 平滑是结果，现代深度学习继承了它的实证传统。

## The Concept | 核心概念

> **【中文解读】** 本节介绍核心概念和理论基础。掌握这些概念是后续动手实现的前提，同时也是面试和工程实践中高频考察的知识点。

![N-gram model: count, smooth, generate](../assets/ngram.svg)

**N-gram probability:** `P(w_i | w_{i-n+1}, ..., w_{i-1})`. Fix `n` (typically 3 for trigrams, 4 for 4-grams). Compute from counts:

> **N-gram 概率：** `P(w_i | w_{i-n+1}, ..., w_{i-1})`。固定 `n`（三元组通常为 3，四元组为 4）。从计数计算：

```text
P(w | context) = count(context, w) / count(context)
```

**The zero-count problem.** Any n-gram not seen in training gets probability zero. A 2007 study on the Brown corpus found that even a 4-gram model had 30% of held-out 4-grams unseen in training. You cannot evaluate on any real text without smoothing.

> **零计数问题。** 任何训练中未见过的 n-gram 都获得零概率。2007 年对 Brown 语料库的研究发现，即使是四元组模型也有 30% 的留出四元组在训练中未见过。没有平滑就无法在任何真实文本上评估。

**Smoothing approaches, in order of sophistication:**

> **平滑方法，按复杂度排序：**

1. **Laplace (add-one).** Add 1 to every count. Simple, terrible on rare events.
   **拉普拉斯（加一）。** 给每个计数加 1。简单，但在罕见事件上效果很差。
2. **Good-Turing.** Reallocate probability mass from higher-frequency events to unseen ones based on frequency-of-frequencies.
   **Good-Turing。** 基于频率的频率，将概率质量从高频事件重新分配到未见事件。
3. **Interpolation.** Combine n-gram, (n-1)-gram, etc., estimates with tunable weights.
   **插值。** 用可调权重组合 n-gram、(n-1)-gram 等估计。
4. **Backoff.** If n-gram has count zero, fall back to (n-1)-gram. Katz backoff normalizes this.
   **回退。** 如果 n-gram 计数为零，回退到 (n-1)-gram。Katz 回退将其归一化。
5. **Absolute discounting.** Subtract a fixed discount `D` from all counts, redistribute to unseen.
   **绝对折扣。** 从所有计数中减去固定折扣 `D`，重新分配给未见事件。
6. **Kneser-Ney.** Absolute discounting plus a clever choice for the lower-order model: use *continuation probability* (how many contexts a word appears in) instead of raw frequency.
   **Kneser-Ney。** 绝对折扣加上低阶模型的巧妙选择：使用*续接概率*（一个词出现在多少上下文中）而不是原始频率。

The Kneser-Ney insight is deep. "San Francisco" is a common bigram. Unigram "Francisco" appears mostly after "San." Naive absolute discounting gives "Francisco" high unigram probability (because the count is high). Kneser-Ney notices that "Francisco" appears in only one context and lowers its continuation probability accordingly. Result: a novel bigram ending in "Francisco" gets the appropriate low probability.

> Kneser-Ney 的洞察很深刻。"San Francisco" 是一个常见的二元组。一元组 "Francisco" 主要出现在 "San" 之后。朴素绝对折扣给 "Francisco" 高一元组概率（因为计数高）。Kneser-Ney 注意到 "Francisco" 只出现在一个上下文中，相应地降低其续接概率。结果：以 "Francisco" 结尾的新二元组获得适当的低概率。

**Evaluation: perplexity.** The exponent of the average negative log-likelihood per word on a held-out test set. Lower is better. A perplexity of 100 means the model is as confused as it would be choosing uniformly among 100 words.

> **评估：困惑度。** 留出测试集上每词平均负对数似然的指数。越低越好。困惑度 100 意味着模型的困惑程度相当于在 100 个词中均匀选择。

```text
perplexity = exp(- (1/N) * Σ log P(w_i | context_i))
```

> **【中文解读】** 本节通过代码从零实现核心算法。这种 "from scratch" 的方式能帮助理解框架背后的原理，遇到问题时不会被黑盒困住。

> **【拓展：大语言模型的工程实践】** 从 GPT 到 ChatGPT，NLP 领域经历了从 "每个任务训练一个模型" 到 "一个模型解决所有任务" 的范式转变。在实际工程中，LLM 的部署需要考虑 Token 限制、延迟、成本、安全审查等问题。LangChain、LlamaIndex 等框架简化了 LLM 应用的开发。

> **【拓展：RAG 与企业知识库】** 检索增强生成（RAG）是当前企业 AI 应用最流行的架构：将用户查询先检索相关文档片段，再将检索结果作为上下文喂给 LLM 生成答案。这种方式解决了 LLM 知识过时和幻觉问题。向量数据库（如 Milvus、Pinecone、Weaviate）是 RAG 系统的核心组件。

> **【拓展：NLP 的多语言挑战】** 全球有 7000+ 种语言，但 NLP 研究主要集中在英语等少数语言。跨语言迁移学习、多语言预训练模型（如 mBERT、XLM-R）是解决低资源语言 NLP 的主要方法。字节级模型（如 ByT5）甚至可以在无分词器的情况下处理任何语言。

## Build It | 动手实现

> **【中文解读】** 本节通过代码从零实现核心算法。这种 "from scratch" 的方式能帮助理解框架背后的原理，遇到问题时不会被黑盒困住。

### Step 1: trigram counts

```python
from collections import Counter, defaultdict


def train_ngram(corpus_tokens, n=3):
    ngrams = Counter()
    contexts = Counter()
    for sentence in corpus_tokens:
        padded = ["<s>"] * (n - 1) + sentence + ["</s>"]
        for i in range(len(padded) - n + 1):
            ctx = tuple(padded[i:i + n - 1])
            word = padded[i + n - 1]
            ngrams[ctx + (word,)] += 1
            contexts[ctx] += 1
    return ngrams, contexts


def raw_probability(ngrams, contexts, context, word):
    ctx = tuple(context)
    if contexts.get(ctx, 0) == 0:
        return 0.0
    return ngrams.get(ctx + (word,), 0) / contexts[ctx]
```

Input is a list of tokenized sentences. Output is n-gram counts and context counts. `<s>` and `</s>` are sentence boundaries.

> 输入是分词后的句子列表。输出是 n-gram 计数和上下文计数。`<s>` 和 `</s>` 是句子边界。

### Step 2: Laplace smoothing

```python
def laplace_probability(ngrams, contexts, vocab_size, context, word):
    ctx = tuple(context)
    numerator = ngrams.get(ctx + (word,), 0) + 1
    denominator = contexts.get(ctx, 0) + vocab_size
    return numerator / denominator
```

Add 1 to every count. Smooths but over-allocates mass to unseen events, hurting rare-known events too.

> 给每个计数加 1。平滑但过度分配质量给未见事件，也伤害已知罕见事件。

### Step 3: Kneser-Ney (bigram, interpolated)

```python
def kneser_ney_bigram_model(corpus_tokens, discount=0.75):
    unigrams = Counter()
    bigrams = Counter()
    unigram_contexts = defaultdict(set)

    for sentence in corpus_tokens:
        padded = ["<s>"] + sentence + ["</s>"]
        for i, w in enumerate(padded):
            unigrams[w] += 1
            if i > 0:
                prev = padded[i - 1]
                bigrams[(prev, w)] += 1
                unigram_contexts[w].add(prev)

    total_unique_bigrams = sum(len(ctx_set) for ctx_set in unigram_contexts.values())
    continuation_prob = {
        w: len(ctx_set) / total_unique_bigrams for w, ctx_set in unigram_contexts.items()
    }

    context_totals = Counter()
    for (prev, w), count in bigrams.items():
        context_totals[prev] += count

    unique_follow = defaultdict(set)
    for (prev, w) in bigrams:
        unique_follow[prev].add(w)

    def prob(prev, w):
        count = bigrams.get((prev, w), 0)
        denom = context_totals.get(prev, 0)
        if denom == 0:
            return continuation_prob.get(w, 1e-9)
        first_term = max(count - discount, 0) / denom
        lambda_prev = discount * len(unique_follow[prev]) / denom
        return first_term + lambda_prev * continuation_prob.get(w, 1e-9)

    return prob
```

Three moving parts. `continuation_prob` captures "how many different contexts does this word appear in?" (the Kneser-Ney innovation). `lambda_prev` is the mass freed by the discount, used to weight the backoff. The final probability is the discounted main term plus the weighted continuation term.

> 三个动态部分。`continuation_prob` 捕获 "这个词出现在多少不同上下文中？"（Kneser-Ney 的创新）。`lambda_prev` 是折扣释放的质量，用于加权回退。最终概率是折扣主项加加权续接项。

### Step 4: generating text with sampling

```python
import random


def generate(prob_fn, vocab, prefix, max_len=30, seed=0):
    rng = random.Random(seed)
    tokens = list(prefix)
    for _ in range(max_len):
        candidates = [(w, prob_fn(tokens[-1], w)) for w in vocab]
        total = sum(p for _, p in candidates)
        r = rng.random() * total
        acc = 0.0
        for w, p in candidates:
            acc += p
            if r <= acc:
                tokens.append(w)
                break
        if tokens[-1] == "</s>":
            break
    return tokens
```

Sampling proportional to probability. Always gives different output per seed. For beam-search-like output, pick the argmax at each step (greedy) and add a small randomness knob (temperature).

> 按概率比例采样。每个种子总是给出不同输出。对于类似束搜索的输出，每步取 argmax（贪心）并加一个小随机性旋钮（温度）。

### Step 5: perplexity

```python
import math


def perplexity(prob_fn, sentences):
    total_log_prob = 0.0
    total_tokens = 0
    for sentence in sentences:
        padded = ["<s>"] + sentence + ["</s>"]
        for i in range(1, len(padded)):
            p = prob_fn(padded[i - 1], padded[i])
            total_log_prob += math.log(max(p, 1e-12))
            total_tokens += 1
    return math.exp(-total_log_prob / total_tokens)
```

Lower is better. For Brown corpus, a well-tuned 4-gram KN model hits perplexity around 140. A transformer LM hits 15-30 on the same test set. The gap is about 10x. That gap is why the field moved on.

> 越低越好。对于 Brown 语料库，一个精心调参的四元组 KN 模型困惑度约 140。Transformer 语言模型在相同测试集上达到 15-30。差距约 10 倍。这个差距就是这个领域转向的原因。

> **【中文解读】** 本节展示如何用成熟框架（如 PyTorch、HuggingFace 等）快速应用该技术。在实际项目中，优先使用经过验证的框架实现，可以减少 bug 并提高开发效率。

> **【拓展：Prompt Engineering 与 LLM 应用】** Prompt Engineering 已成为 NLP 工程师的核心技能。从 Zero-shot 到 Few-shot，从 Chain-of-Thought 到 ReAct，不同的提示策略适用于不同场景。在实际项目中，系统提示（System Prompt）的设计直接影响 LLM 应用的稳定性和输出质量。

## Use It | 用框架实现

- **Classical NLP teaching.** The clearest exposure to smoothing, MLE, and perplexity you can get.
  **经典 NLP 教学。** 你能得到的最清晰的平滑、MLE 和困惑度体验。
- **KenLM.** Production n-gram library. Used as a rescorer in speech and MT systems where low latency matters.
  **KenLM。** 生产级 n-gram 库。用作低延迟语音和 MT 系统的重评分器。
- **On-device autocomplete.** Trigram models in keyboards. Still.
  **设备端自动补全。** 键盘中的三元组模型。仍然在使用。
- **Baselines.** Always compute an n-gram LM perplexity before declaring your neural LM good. If your transformer does not beat KN by a wide margin, something is wrong.
  **基线。** 在宣布你的神经语言模型好之前，始终计算 n-gram LM 困惑度。如果你的 Transformer 没有大幅击败 KN，那就有问题。

> **【中文解读】** 本节关注如何将模型部署为可用的产品。从原型到生产级系统需要考虑性能优化、错误处理、监控等多个维度。

## Ship It | 产出物

Save as `outputs/prompt-lm-baseline.md`:

> 保存为 `outputs/prompt-lm-baseline.md`：

```markdown
---
name: lm-baseline
description: Build a reproducible n-gram language model baseline before training a neural LM.
phase: 5
lesson: 16
---

Given a corpus and target use (next-word prediction, rescoring, perplexity baseline), output:

1. N-gram order. Trigram for general English, 4-gram if corpus is large, 5-gram for speech rescoring.
2. Smoothing. Modified Kneser-Ney is the default; Laplace only for teaching.
3. Library. `kenlm` for production, `nltk.lm` for teaching, roll your own only to learn.
4. Evaluation. Held-out perplexity with consistent tokenization between train and test sets.

Refuse to report perplexity computed with different tokenization between systems being compared — perplexity numbers are comparable only under identical tokenization. Flag OOV rate in test set; KN handles OOV poorly unless you reserve a special <UNK> token during training.
```

> **【中文解读】** 练习题按照 Easy/Medium/Hard 三个难度递进。建议至少完成 Medium 级别的题目，Hard 级别适合深入研究或面试准备。

## Exercises | 练习题

1. **Easy.** Train a trigram LM on a 1,000-sentence Shakespeare corpus. Generate 20 sentences. They will be locally plausible but globally incoherent. This is the canonical demo.
   **简单。** 在 1000 句莎士比亚语料上训练三元组语言模型。生成 20 个句子。它们在局部合理但全局不连贯。这是经典演示。
2. **Medium.** Implement perplexity for your KN model on a held-out Shakespeare split. Compare against Laplace. You should see KN lower perplexity by 30-50%.
   **中等。** 在留出的莎士比亚划分上为你的 KN 模型实现困惑度。与拉普拉斯比较。你应该看到 KN 降低困惑度 30-50%。
3. **Hard.** Build a trigram spell corrector: given a misspelled word and its context, generate corrections and rank by context probability under the LM. Evaluate on the Birkbeck spelling corpus (public).
   **困难。** 构建三元组拼写纠错器：给定一个拼写错误的词及其上下文，生成纠正并按 LM 下的上下文概率排序。在 Birkbeck 拼写语料库（公开）上评估。

> **【中文解读】** 术语表中的 "What people say" vs "What it actually means" 区分了日常口语和精确技术含义。在团队协作中，统一术语定义可以避免大量沟通误解。

## Key Terms | 术语速查表

| Term / 术语 | What people say / 人们常说的 | What it actually means / 实际含义 |
|------|-----------------|-----------------------|
| N-gram | Word sequence / 词序列 | Sequence of `n` consecutive tokens. / `n` 个连续 token 的序列。 |
| Smoothing（平滑） | Avoiding zeros / 避免零 | Reallocating probability mass so unseen events get non-zero probability. / 重新分配概率质量使未见事件获得非零概率。 |
| Perplexity（困惑度） | LM quality metric / LM 质量指标 | `exp(-average log-prob)` on held-out data. Lower is better. / 留出数据上的 `exp(-平均对数概率)`。越低越好。 |
| Backoff（回退） | Fallback to shorter context / 回退到更短上下文 | If trigram count is zero, use bigram. Katz backoff formalizes this. / 如果三元组计数为零，使用二元组。Katz 回退将其形式化。 |
| Kneser-Ney | Best smoothing for n-grams / 最佳 n-gram 平滑 | Absolute discounting + continuation probability for the lower-order model. / 绝对折扣 + 低阶模型的续接概率。 |
| Continuation probability（续接概率） | KN-specific / KN 特有 | `P(w)` weighted by number of contexts `w` appears in, not by raw count. / `P(w)` 按 `w` 出现的上下文数量加权，而非原始计数。 |

> **【中文解读】** 延伸阅读提供了深入学习的高质量资源。这些论文和教程是该领域的经典参考文献，适合需要深入理解的读者。

## Further Reading | 延伸阅读

- [Jurafsky and Martin — Speech and Language Processing, Chapter 3 (2026 draft)](https://web.stanford.edu/~jurafsky/slp3/3.pdf) — the canonical treatment of n-gram LMs and smoothing. / n-gram 语言模型和平滑的经典教材。
- [Chen and Goodman (1998). An Empirical Study of Smoothing Techniques for Language Modeling](https://dash.harvard.edu/handle/1/25104739) — the paper that settled Kneser-Ney as the best n-gram smoother. / 确定 Kneser-Ney 为最佳 n-gram 平滑器的论文。
- [Kneser and Ney (1995). Improved Backing-off for M-gram Language Modeling](https://ieeexplore.ieee.org/document/479394) — the original KN paper. / 原始 KN 论文。
- [KenLM](https://kheafield.com/code/kenlm/) — fast production n-gram LM, still used in 2026 for latency-sensitive applications. / 快速生产级 n-gram 语言模型，2026 年仍用于延迟敏感应用。
