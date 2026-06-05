# Sentiment Analysis | 情感分析

> The canonical NLP task. Most of what you need to know about classical text classification shows up here.
> 最经典的 NLP 任务。经典文本分类中你需要知道的大部分内容都在这里了。

> **【中文解读】** 判断文本的情感倾向。是 NLP 最经典的分类任务之一。

**Type:** Build | **类型:** 动手
**Languages:** Python | **语言:** Python
**Prerequisites:** Phase 5 · 02 (BoW + TF-IDF), Phase 2 · 14 (Naive Bayes) | **前置知识:** Phase 5 · 02（BoW + TF-IDF），Phase 2 · 14（朴素贝叶斯）
**Time:** ~75 minutes | **时间:** ~75 分钟

## The Problem | 问题引入

"The food was not great." Positive or negative?

> "The food was not great." 正面还是负面？

Sentiment sounds simple. A reviewer said they liked or did not like something. Label the sentence. The reason it became the canonical NLP task is that every easy-looking case hides a hard one. Negation flips meaning. Sarcasm inverts it. "Not bad at all" is positive despite two negative-coded words. Emojis carry more signal than surrounding text. Domain vocabulary matters (`tight` in music review versus `tight` in fashion review).

> 情感分析听起来简单。评论者说了喜欢或不喜欢什么。标记句子。它之所以成为经典 NLP 任务，是因为每个看似简单的案例背后都隐藏着一个困难的案例。否定翻转含义。讽刺反转含义。"Not bad at all" 尽管有两个负面编码词，却是正面的。表情符号比周围文本携带更多信号。领域词汇很重要（音乐评论中的 `tight` 与时尚评论中的 `tight`）。

Sentiment is a working lab for classical NLP. If you understand why every naive baseline has a specific failure mode, you understand why every richer model was invented. This lesson builds a Naive Bayes baseline from scratch, adds logistic regression, and names the traps that make production sentiment a compliance-grade problem.

> 情感分析是经典 NLP 的工作实验室。如果你理解为什么每个朴素基线都有特定的失败模式，你就理解为什么每种更丰富的模型被发明出来。本课从零构建朴素贝叶斯基线，添加逻辑回归，并指出使生产情感分析成为合规级问题的陷阱。

## The Concept | 核心概念

> **【中文解读】** 本节介绍核心概念和理论基础。掌握这些概念是后续动手实现的前提，同时也是面试和工程实践中高频考察的知识点。

Classical sentiment is a two-step recipe.

> 经典情感分析是一个两步方案。

1. **Represent.** Turn the text into a feature vector. BoW, TF-IDF, or n-grams.
   **表示。** 将文本转换为特征向量。BoW、TF-IDF 或 n-gram。
2. **Classify.** Fit a linear model (Naive Bayes, logistic regression, SVM) on labeled examples.
   **分类。** 在标注样本上拟合线性模型（朴素贝叶斯、逻辑回归、SVM）。

Naive Bayes is the dumbest model that works. Assume every feature is independent given the label. Estimate `P(word | positive)` and `P(word | negative)` from counts. At inference, multiply the probabilities. The "naive" independence assumption is laughably wrong and yet the results are shockingly strong. The reason: with sparse text features and moderate data, the classifier cares about which side each word leans toward more than how much.

> 朴素贝叶斯是最笨但管用的模型。假设给定标签后每个特征相互独立。从计数估计 `P(word | positive)` 和 `P(word | negative)`。推理时将概率相乘。"朴素"的独立性假设错得可笑，但结果惊人地强。原因：在稀疏文本特征和中等数据下，分类器关心的是每个词倾向于哪一边，而不是倾向于多少。

Logistic regression fixes the independence assumption. It learns a weight per feature, including negative weights. `not good` as a bigram feature gets a negative weight. Naive Bayes cannot do that for bigrams it has never labeled.

> 逻辑回归修复了独立性假设。它为每个特征学习一个权重，包括负权重。`not good` 作为二元组特征获得负权重。朴素贝叶斯对从未标注过的二元组做不到这一点。

> **【拓展：大语言模型的工程实践】** 从 GPT 到 ChatGPT，NLP 领域经历了从 "每个任务训练一个模型" 到 "一个模型解决所有任务" 的范式转变。在实际工程中，LLM 的部署需要考虑 Token 限制、延迟、成本、安全审查等问题。LangChain、LlamaIndex 等框架简化了 LLM 应用的开发。

> **【拓展：RAG 与企业知识库】** 检索增强生成（RAG）是当前企业 AI 应用最流行的架构：将用户查询先检索相关文档片段，再将检索结果作为上下文喂给 LLM 生成答案。这种方式解决了 LLM 知识过时和幻觉问题。向量数据库（如 Milvus、Pinecone、Weaviate）是 RAG 系统的核心组件。

> **【拓展：NLP 的多语言挑战】** 全球有 7000+ 种语言，但 NLP 研究主要集中在英语等少数语言。跨语言迁移学习、多语言预训练模型（如 mBERT、XLM-R）是解决低资源语言 NLP 的主要方法。字节级模型（如 ByT5）甚至可以在无分词器的情况下处理任何语言。

## Build It | 动手实现

> **【中文解读】** 本节通过代码从零实现核心算法。这种 "from scratch" 的方式能帮助理解框架背后的原理，遇到问题时不会被黑盒困住。

### Step 1: a real mini-dataset

```python
POSITIVE = [
    "absolutely loved this movie",
    "beautiful cinematography and a great story",
    "one of the best films of the year",
    "brilliant acting from the lead",
    "heartwarming and funny",
]

NEGATIVE = [
    "boring and far too long",
    "not worth your time",
    "the plot made no sense",
    "terrible acting, awful script",
    "i want my two hours back",
]
```

Small on purpose. Real work uses tens of thousands of examples (IMDb, SST-2, Yelp polarity). The math is identical.

> 故意做得很小。实际工作使用数万个样本（IMDb、SST-2、Yelp Polarity）。数学是相同的。

### Step 2: multinomial Naive Bayes from scratch

```python
import math
from collections import Counter


def train_nb(docs_by_class, vocab, alpha=1.0):
    class_priors = {}
    class_word_probs = {}
    total_docs = sum(len(d) for d in docs_by_class.values())

    for cls, docs in docs_by_class.items():
        class_priors[cls] = len(docs) / total_docs
        counts = Counter()
        for doc in docs:
            for token in doc:
                counts[token] += 1
        total = sum(counts.values()) + alpha * len(vocab)
        class_word_probs[cls] = {
            w: (counts[w] + alpha) / total for w in vocab
        }
    return class_priors, class_word_probs


def predict_nb(doc, class_priors, class_word_probs):
    scores = {}
    for cls in class_priors:
        s = math.log(class_priors[cls])
        for token in doc:
            if token in class_word_probs[cls]:
                s += math.log(class_word_probs[cls][token])
        scores[cls] = s
    return max(scores, key=scores.get)
```

Additive smoothing (alpha=1.0) is Laplace smoothing. Without it, a word unseen in a class has probability zero and the log explodes. `alpha=0.01` is common in practice. `alpha=1.0` is the teaching default.

> 加法平滑（alpha=1.0）是拉普拉斯平滑。没有它，一个类别中未见过的词概率为零，log 会爆炸。实践中 `alpha=0.01` 很常见。`alpha=1.0` 是教学默认值。

### Step 3: logistic regression from scratch

```python
import numpy as np


def sigmoid(x):
    return 1.0 / (1.0 + np.exp(-np.clip(x, -20, 20)))


def train_lr(X, y, epochs=500, lr=0.05, l2=0.01):
    n_features = X.shape[1]
    w = np.zeros(n_features)
    b = 0.0
    for _ in range(epochs):
        logits = X @ w + b
        preds = sigmoid(logits)
        err = preds - y
        grad_w = X.T @ err / len(y) + l2 * w
        grad_b = err.mean()
        w -= lr * grad_w
        b -= lr * grad_b
    return w, b


def predict_lr(X, w, b):
    return (sigmoid(X @ w + b) >= 0.5).astype(int)
```

L2 regularization matters here. Text features are sparse; without L2 the model memorizes training examples. Start at `0.01` and tune.

> L2 正则化在这里很重要。文本特征是稀疏的；没有 L2 模型会记住训练样本。从 `0.01` 开始调参。

### Step 4: handling negation (the failure mode)

Consider "not good" and "not bad". A BoW classifier sees `{not, good}` and `{not, bad}` and learns from whichever showed up more in training. A bigram classifier sees `not_good` and `not_bad` and learns them as distinct features. That is usually enough.

> 考虑 "not good" 和 "not bad"。BoW 分类器看到 `{not, good}` 和 `{not, bad}`，根据训练中哪个出现更多来学习。二元组分类器看到 `not_good` 和 `not_bad` 作为不同特征学习。这通常就够了。

A cruder fix that works when you do not have bigrams: **negation scoping**. Prefix tokens following a negation word with `NOT_` up to the next punctuation.

> 一个更粗糙但在没有二元组时有效的修复：**否定范围标记**。在否定词后给 token 加 `NOT_` 前缀，直到下一个标点符号。

```python
NEGATION_WORDS = {"not", "no", "never", "nor", "none", "nothing", "neither"}
NEGATION_TERMINATORS = {".", "!", "?", ",", ";"}


def apply_negation(tokens):
    out = []
    negate = False
    for token in tokens:
        if token in NEGATION_TERMINATORS:
            negate = False
            out.append(token)
            continue
        if token in NEGATION_WORDS:
            negate = True
            out.append(token)
            continue
        out.append(f"NOT_{token}" if negate else token)
    return out
```

```python
>>> apply_negation(["not", "good", "at", "all", ".", "but", "funny"])
['not', 'NOT_good', 'NOT_at', 'NOT_all', '.', 'but', 'funny']
```

Now `good` and `NOT_good` are different features. The classifier can weight them opposite. Three lines of preprocessing, measurable accuracy jump on sentiment benchmarks.

> 现在 `good` 和 `NOT_good` 是不同的特征。分类器可以给它们相反的权重。三行预处理，在情感分析基准上有可测量的准确率提升。

### Step 5: evaluation metrics that matter

Accuracy alone is misleading if classes are imbalanced. Real sentiment corpora are usually 70-80% positive or 70-80% negative; a constant-majority classifier gets 80% accuracy and is worthless. Report every one of the following:

> 如果类别不平衡，仅看准确率会产生误导。真实情感语料通常 70-80% 是正面或 70-80% 是负面的；一个常量多数类分类器就能获得 80% 的准确率，但毫无价值。请报告以下每一项：

- **Per-class precision and recall.** One pair per class. Macro-average them to get a single number that respects class balance.
  **每类精确率和召回率。** 每个类别一对。宏平均它们得到一个尊重类别平衡的单一数字。
- **Macro-F1 (primary metric for imbalanced data).** Mean of per-class F1 scores, equally weighted. Use this instead of accuracy when classes are imbalanced.
  **Macro-F1（不平衡数据的主要指标）。** 各类 F1 分数的均值，等权重。当类别不平衡时用这个代替准确率。
- **Weighted-F1 (alternative).** Same as macro but weighted by class frequency. Report alongside macro-F1 when the imbalance itself has business meaning.
  **Weighted-F1（替代方案）。** 与宏平均相同但按类频率加权。当不平衡本身有业务含义时，与 Macro-F1 一起报告。
- **Confusion matrix.** Raw counts. Always inspect before trusting any scalar metric; it reveals which pair of classes the model confuses.
  **混淆矩阵。** 原始计数。在信任任何标量指标之前始终检查；它揭示模型混淆了哪些类别对。
- **Per-class error samples.** Pull 5 wrong predictions per class. Read them. Nothing replaces reading the actual errors.
  **每类错误样本。** 每个类别抽取 5 个错误预测。阅读它们。没有什么能替代阅读实际错误。

For severely imbalanced data (> 95-5 ratio), report **AUROC** and **AUPRC** instead of accuracy. AUPRC is more sensitive to the minority class, which is what you usually care about (spam, fraud, rare sentiment).

> 对于严重不平衡的数据（> 95-5 比例），报告 **AUROC** 和 **AUPRC** 代替准确率。AUPRC 对少数类更敏感，这通常是你关心的（垃圾邮件、欺诈、罕见情感）。

**Common bug to avoid.** Reporting micro-F1 instead of macro-F1 on imbalanced data gives a number that looks high because it is dominated by the majority class. Macro-F1 forces you to see the minority-class performance.

> **常见错误。** 在不平衡数据上报告 micro-F1 而不是 macro-F1 会给出一个看起来很高的数字，因为它被多数类主导。Macro-F1 迫使你看到少数类的表现。

```python
def evaluate(y_true, y_pred):
    tp = sum(1 for t, p in zip(y_true, y_pred) if t == 1 and p == 1)
    fp = sum(1 for t, p in zip(y_true, y_pred) if t == 0 and p == 1)
    fn = sum(1 for t, p in zip(y_true, y_pred) if t == 1 and p == 0)
    tn = sum(1 for t, p in zip(y_true, y_pred) if t == 0 and p == 0)
    precision = tp / (tp + fp) if tp + fp else 0
    recall = tp / (tp + fn) if tp + fn else 0
    f1 = 2 * precision * recall / (precision + recall) if precision + recall else 0
    return {"tp": tp, "fp": fp, "tn": tn, "fn": fn, "precision": precision, "recall": recall, "f1": f1}
```

> **【中文解读】** 本节展示如何用成熟框架（如 PyTorch、HuggingFace 等）快速应用该技术。在实际项目中，优先使用经过验证的框架实现，可以减少 bug 并提高开发效率。

> **【拓展：Prompt Engineering 与 LLM 应用】** Prompt Engineering 已成为 NLP 工程师的核心技能。从 Zero-shot 到 Few-shot，从 Chain-of-Thought 到 ReAct，不同的提示策略适用于不同场景。在实际项目中，系统提示（System Prompt）的设计直接影响 LLM 应用的稳定性和输出质量。

## Use It | 用框架实现

scikit-learn does it in six lines, correctly.

> scikit-learn 六行代码搞定，而且正确。

```python
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline

pipe = Pipeline([
    ("tfidf", TfidfVectorizer(ngram_range=(1, 2), min_df=2, sublinear_tf=True, stop_words=None)),
    ("clf", LogisticRegression(C=1.0, max_iter=1000)),
])
pipe.fit(X_train, y_train)
print(pipe.score(X_test, y_test))
```

Three things to notice. `stop_words=None` keeps negations. `ngram_range=(1, 2)` adds bigrams so `not_good` becomes a feature. `sublinear_tf=True` dampens repeated words. These three flags are the difference between a 75%-accurate baseline and an 85%-accurate baseline on SST-2.

> 三个值得注意的地方。`stop_words=None` 保留否定词。`ngram_range=(1, 2)` 添加二元组使 `not_good` 成为特征。`sublinear_tf=True` 抑制重复词。这三个标志是在 SST-2 上 75% 准确率基线和 85% 准确率基线之间的区别。

### When to reach for a transformer

- Sarcasm detection. Classical models fail here. Period.
  讽刺检测。经典模型在这里会失败。毫无例外。
- Long reviews where sentiment shifts mid-document.
  情感在文档中间转变的长评论。
- Aspect-based sentiment. "Camera was great but battery was terrible." You need to attribute sentiment to aspects. Transformers or structured output models only.
  基于方面的情感分析。"Camera was great but battery was terrible." 你需要将情感归因到方面。只有 Transformer 或结构化输出模型能做到。
- Non-English, low-resource languages. Multilingual BERT gives you a zero-shot baseline for free.
  非英语、低资源语言。多语言 BERT 为你免费提供零样本基线。

If you need any of the above, skip ahead to phase 7 (transformers deep dive). Otherwise, Naive Bayes or logistic regression on TF-IDF plus bigrams plus negation handling is your 2026 production baseline.

> 如果你需要以上任何一项，跳到 Phase 7（Transformer 深入）。否则，在 TF-IDF 加二元组加否定处理上的朴素贝叶斯或逻辑回归就是你 2026 年的生产基线。

### The reproducibility trap (again)

Retraining sentiment models is routine. Re-evaluating them is not. Accuracy numbers reported in papers use specific splits, specific preprocessing, specific tokenizers. If you compare your new model to a baseline without using the identical pipeline, you will get misleading deltas. Always regenerate the baseline on your pipeline, not the paper's number.

> 重新训练情感模型是常规操作。重新评估却不是。论文中报告的准确率数字使用特定的数据划分、特定的预处理、特定的分词器。如果你不使用完全相同的流水线来比较新模型与基线，你会得到误导性的差值。始终在你的流水线上重新生成基线，而不是用论文中的数字。

> **【中文解读】** 本节关注如何将模型部署为可用的产品。从原型到生产级系统需要考虑性能优化、错误处理、监控等多个维度。

## Ship It | 产出物

Save as `outputs/prompt-sentiment-baseline.md`:

```markdown
---
name: sentiment-baseline
description: Design a sentiment analysis baseline for a new dataset.
phase: 5
lesson: 05
---

Given a dataset description (domain, language, size, label granularity, latency budget), you output:

1. Feature extraction recipe. Specify tokenizer, n-gram range, stopword policy (usually keep), negation handling (scoped prefix or bigrams).
2. Classifier. Naive Bayes for baseline, logistic regression for production, transformer only if the domain needs sarcasm / aspects / cross-lingual.
3. Evaluation plan. Report precision, recall, F1, confusion matrix, and per-class error samples (not just scalars).
4. One failure mode to monitor post-deployment. Domain drift and sarcasm are the top two.

> **【中文解读】** 练习题按照 Easy/Medium/Hard 三个难度递进。建议至少完成 Medium 级别的题目，Hard 级别适合深入研究或面试准备。

Refuse to recommend dropping stopwords for sentiment tasks. Refuse to report accuracy as the sole metric when classes are imbalanced (e.g., 90% positive). Flag subword-rich languages as needing FastText or transformer embeddings over word-level TF-IDF.
```

## Exercises | 练习题

1. **Easy.** Add `apply_negation` as a preprocessing step in the scikit-learn pipeline and measure the F1 delta on a small sentiment dataset.
   **简单。** 将 `apply_negation` 作为预处理步骤添加到 scikit-learn 流水线中，在一个小型情感数据集上测量 F1 变化。
2. **Medium.** Implement class-weighted logistic regression (pass `class_weight="balanced"` to scikit-learn, or derive the gradient yourself). Measure the effect on a synthetic 90-10 class imbalance.
   **中等。** 实现类别加权逻辑回归（传递 `class_weight="balanced"` 给 scikit-learn，或自己推导梯度）。在合成的 90-10 类别不平衡上测量效果。
3. **Hard.** Build a sarcasm detector by training a second classifier on the residuals of the sentiment model. Document your experimental setup. Warn the reader when your accuracy is below chance (chance-level on 2-class sarcasm is ~50%, and most first attempts land there).
   **困难。** 在情感模型的残差上训练第二个分类器来构建讽刺检测器。记录你的实验设置。当你的准确率低于随机水平时警告读者（2 类讽刺分类的随机水平约 50%，大多数首次尝试都停留在那里）。

> **【中文解读】** 练习题按照 Easy/Medium/Hard 三个难度递进。建议至少完成 Medium 级别的题目，Hard 级别适合深入研究或面试准备。

## Key Terms | 术语速查表

| Term | What people say | What it actually means | 术语 | 人们常说的 | 实际含义 |
|------|-----------------|-----------------------|------|-----------|---------|
| Polarity | Positive or negative | Binary label; sometimes extended to neutral or fine-grained (5-star). | 极性（Polarity） | 正面或负面 | 二分类标签；有时扩展到中性或细粒度（5 星）。 |
| Aspect-based sentiment | Per-aspect polarity | Attribute sentiment to specific entities or attributes mentioned in text. | 基于方面的情感分析 | 每个方面的极性 | 将情感归因到文本中提到的特定实体或属性。 |
| Negation scoping | Reversing nearby tokens | Prefix tokens after "not" with `NOT_` until punctuation. | 否定范围标记 | 反转附近的 token | 在 "not" 后给 token 加 `NOT_` 前缀直到标点符号。 |
| Laplace smoothing | Adding 1 to counts | Prevents zero-probability features in Naive Bayes. | 拉普拉斯平滑 | 给计数加 1 | 防止朴素贝叶斯中出现零概率特征。 |
| L2 regularization | Shrinking weights | Adds `lambda * sum(w^2)` to loss. Essential for sparse text features. | L2 正则化 | 缩小权重 | 在损失中添加 `lambda * sum(w^2)`。对稀疏文本特征必不可少。 |

> **【中文解读】** 术语表中的 "What people say" vs "What it actually means" 区分了日常口语和精确技术含义。在团队协作中，统一术语定义可以避免大量沟通误解。

## Further Reading | 延伸阅读

- [Pang and Lee (2008). Opinion Mining and Sentiment Analysis](https://www.cs.cornell.edu/home/llee/opinion-mining-sentiment-analysis-survey.html) — the foundational survey. Long, but the first four sections cover everything classical. / 基础综述。较长，但前四节涵盖了经典内容的全部。
- [Wang and Manning (2012). Baselines and Bigrams: Simple, Good Sentiment and Topic Classification](https://aclanthology.org/P12-2018/) — the paper that showed bigrams + Naive Bayes is hard to beat on short text. / 证明二元组 + 朴素贝叶斯在短文本上难以被超越的论文。
- [scikit-learn text feature extraction docs](https://scikit-learn.org/stable/modules/feature_extraction.html#text-feature-extraction) — reference for `CountVectorizer`, `TfidfVectorizer`, and every knob you'll tune. / `CountVectorizer`、`TfidfVectorizer` 及你将调参的每个参数的参考。
