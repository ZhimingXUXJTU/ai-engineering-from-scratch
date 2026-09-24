# 情感分析

> 关于经典文本分类的大部分知识都在这里.
> 最经典的NLP任务. 你需要知道的大部分内容都在这里.

> **【中文解读】**判断文本的情感倾向.

**Type:** Build | **类型:** 动手
**Languages:** Python | **语言:** Python
**Prerequisites:** Phase 5 · 02 (BoW + TF-IDF), Phase 2 · 14 (Naive Bayes) | **前置知识:** Phase 5 · 02（BoW + TF-IDF），Phase 2 · 14（朴素贝叶斯）
**Time:** ~75 minutes | **时间:** ~75 分钟

## 问题 问题引入

"食物不好". 积极还是消极?

> "食物不好". 正面还是负面?

感觉听起来很简单.一个评论员说他们喜欢或不喜欢某种东西.标签句子.它成为了神圣的NLP任务的原因是每个容易看起来的案例都隐藏着一个难以理解的.否定翻转意义.刺反转意义. "不坏的"是积极的,尽管有两个负面编码的词.爱莫吉带有比周围文本更多的信号.域名词汇问题 (`tight`在音乐评论中`tight`在时尚审查中).

> 情感分析听起来很简单――评论员说喜欢或不喜欢什么――标记句子――它成为经典的NLP任务,因为每个看起来很简单的案例背后都隐藏着一个困难的案例――否定翻转含义――刺反转含义――"不坏的"虽然有两个负面编码词,但是正面的――表情符号比周围文本带来更多信号――领域词汇很重要(音乐评论中`tight`时尚评论中`tight`

感觉是经典NLP的工作实验室.如果你明白为什么每一个天真的基线都有特定的失败模式,你就会明白为什么每一个更丰富的模型都被发明了.这个课程从零开始构建了一个天真的贝叶斯基线,添加了物流回归,并命名了使生产感觉成为合规程度问题的陷.

> 情感分析是经典的NLP工作实验室.如果你明白为什么每个简单的基础线都有特定的失败模式,你就明白为什么每种更丰富的模型都被发明了. 本课从零构建简单的基础线,添加逻辑回归,并指出使生产情感分析成为合规级问题的陷.

## 概念的核心概念

> **【中文解读】**本节介绍核心概念和理论基础.掌握这些概念是后续动手实现的前提,同时也是面试和工程实践中高频考察的知识点.

经典情感是一个两步的食谱.

> 经典情感分析是一个两步方案.

1. **Represent.**转换文本为特征向量.
   **表示。**将文本转换为特征向量──BoW、TF-IDF 或n-gram──
2. **Classify.**根据标记的例子,适应线性模型 (Naive Bayes,物流回归,SVM).
   **分类。**在标标示样本上拟合线性模型 (简单贝叶斯,逻辑归归,SVM) 

简单的贝耶斯是最愚蠢的模型,假设每个特征都独立,`P(word | positive)`其他`P(word | negative)`根据"无常"独立假设,这是一个可笑的错误,但结果却令人震惊.原因是:由于文本的特征稀少,并且数据中等,分类器关心每个词的倾向是哪个方面,而不是多少.

> 简单的贝叶斯是最但可用的模型.`P(word | positive)`和 `P(word | negative)`△推理时将概率相乘――"简单"的独立性假设是可笑的,但结果惊人地强――原因:在稀疏文本特征和中等数据下,分类器关心的是每个词倾向于哪边,而不是倾向于多少――

逻辑回归修复了独立假设. 它学习每个特征的权重,包括负权重. `not good`简单的贝耶斯不能为它从未标记过的比格拉姆做.

> 逻辑归归修复了独立性假设――它为每个特征学习一个权重,包括负权重――`not good`作为二元组特征获得负权力.

> **【拓展：大语言模型的工程实践】**从GPT到ChatGPT,NLP领域经历了从"每个任务训练一个模型"到"一个模型解决所有任务"的范式转变. 在实际工程中,LLM的部署需要考虑代币限制,延迟,成本,安全审查等问题.

> **【拓展：RAG 与企业知识库】**检索增强生成 (RAG) 是当前企业人工智能应用中最流行的架构:将用户查询先检索相关文档片段,再将检索结果作为上下文给LLM 生成答案――这种方式解决了LLM 知识过时和幻觉问题――向量数据库――如Milvus、Pinecone、Weaviate) 是RAG系统的核心组件――

> **【拓展：NLP 的多语言挑战】**全球有7000多种语言,但NLP研究主要集中在英语等少数语言.跨语言迁移学习,多语言预训模型 (如 mBERT,XLM-R) 是解决低资源语言NLP的主要方法.

## 建立它,实现它.

> **【中文解读】**本节通过代码实现从零到核心算法――这种"从零开始"的方式可以帮助理解框架背后的原理,遇到问题时不会被黑盒困住――
```figure
sentiment-logits
```

## 建立它

### 步骤1:一个真正的微型数据集

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

实际工作使用了数万个例子 (IMDb,SST-2,Yelp极度).数学是相同的.

> 实际工作使用数万个样本 (IMDb、SST-2、Yelp Polarity) ).数学是相同的.

### 步骤2:从零开始,多个个字母的天真贝耶斯

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

没有它,一个词在类中看不到的概率为零,并且日志爆炸. `alpha=0.01`实际上,这种情况是常见的.`alpha=1.0`现在,我们在教学中,

> 加法平滑(alpha=1.0) 是拉普拉斯平滑──没有它,一个类别中未见的词概率为零,log会爆炸──实践中`alpha=0.01`很常见.`alpha=1.0`是教学默认值.

### 步骤3:从零开始的物流回归

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

文本特征很少,没有L2模型记住训练示例.`0.01`听,听听.

> 文本特征很稀疏;没有L2模型会记住训练样本.`0.01`开始调参.

### 操作否定 (故障模式)

考虑"不好"和"不坏".`{not, good}`其他`{not, bad}`们的们都会看到一个大类别.`not_good`其他`not_bad`对于这些问题,我们需要了解更多的信息.

> 考虑"不好" 和"不坏"──BoW 分类器看看`{not, good}`和 `{not, bad}`根据训练中出现的更多来学习.`not_good`和 `not_bad`作为不同特征学习.

没有大子的时候可以做得更好.**negation scoping**后面的代码是否定字符.`NOT_`接下来的分字.

> 一个更粗的,但在没有二元组时有效的修复:**否定范围标记**在否定词后给标志加`NOT_`之前,直到下一个标点符号.

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

现在`good`其他`NOT_good`它们的分类器可以对比重重. 三行预处理,可测量的准确性跳跃于情感基准.

> 现在`good`和 `NOT_good`它们的特征是不同的. 分类器可以给它们反面的权力.

### 步骤5:重要的评估指标

只有在类别不平衡的情况下,准确性就会误导.实际的情感体通常是70-80%正确的或70-80%负面的;一个常数多数的分类器获得80%的准确性,并且是无价值的.报告以下每一个:

> 如果类别不平衡,仅看准确率会产生误导. 真正情感语料通常是70-80%,是正面或是70-80%,是负面.

- **Per-class precision and recall.**给每班一个对,对它们进行宏观平均,以得到一个尊重班级平衡的单个数字.
  **每类精确率和召回率。**每个类别的对应.宏平均它们得到一个单个数字的尊重类别平衡.
- **Macro-F1 (primary metric for imbalanced data).**平均每类F1分数,均重.当类不平衡时,使用这个比较.
  **Macro-F1（不平衡数据的主要指标）。**类别不平衡时使用这个替代准确率.
- **Weighted-F1 (alternative).**报告与宏F1同时,当不平衡本身具有商业意义时.
  **Weighted-F1（替代方案）。**与宏平均相同,但按类频率加权──当不平衡本身具有业务意义时,与宏F1 一起报告──
- **Confusion matrix.**总是检查之前信任任何规模度量; 它揭示模型混的类对.
  **混淆矩阵。**始计数――在信任中任何标志标志之前始终检查;它揭示了模型混了哪些类型对――
- **Per-class error samples.**每班就有五个错误预测,阅读它们. 没有什么可以取代读到实际错误.
  **每类错误样本。**每个类别抽取5个错误预测――阅读它们――没有什么可以替代阅读实际错误――

对于严重失衡的数据 (> 95-5 比例),报告**AUROC**其他**AUPRC**非洲人民共和国人民共和国 (AUPRC) 对少数民族群体更敏感,这就是你通常关心的 (垃圾邮件,欺诈,罕见情绪).

> 对于严重不平衡的数据 (例如: 95-5),报告**AUROC**和 **AUPRC**代替准确率──AUPRC对少数群体更敏感,这通常是你关心的垃圾邮件,欺诈,罕见情感.

**Common bug to avoid.**报告微F1而不是宏F1在不平衡数据上给出一个看起来很高的数字,因为它由多数类占主导地位.

> **常见错误。**在不平衡数据上报告微型F1而不是宏型F1将给出一个看起来很高的数字,因为它被大多数类主导.

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

> **【中文解读】**本节展示了如何使用成熟框架 (如PyTorch、HuggingFace等) 快速应用该技术.

> **【拓展：Prompt Engineering 与 LLM 应用】**快速工程已成为NLP工程师的核心技能. 从零射到少射,从思想链到反应,不同的提示策略适用于不同场景. 在实际项目中,系统提示 (系统提示) 的设计直接影响了LLM应用的稳定性和输出质量.

## 用它实现框架

子学习用六行,正确.

> 简单学习,而且正确.

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

需要注意的三个东西.`stop_words=None`没有任何证据.`ngram_range=(1, 2)`增加了大图.`not_good`成为一个特征.`sublinear_tf=True`它们是SST-2的75%准确基线和85%准确基线之间的区别.

> 值得注意的三个地方.`stop_words=None`留下否定词.`ngram_range=(1, 2)`添加二元组使 `not_good`成为特征.`sublinear_tf=True`抑制重复词――这些三个标志是SST-2上 75% 准确率基线和 85% 准确率基线之间的区别――

### 什么时候要找变压器

- 刺的检测,古典模型失败了.
  刺检测. 经典模型在这里会失败.
- 长期的评论,情绪在文件中转移.
  情感在文档中转变的长评论.
- 基于面积的感觉. "相机很棒,但电池很糟糕".你需要把感觉归因于面积.
  基于情感分析. "相机很棒,但电池很糟糕". 你需要将情感归因到方面.
- 无英语,资源低.多语言BERT免费提供零截图的基础线.
  不英语,低资源语言.多语言BERT为您提供零样本基线.

如果您需要上述任何一个,请跳转到第7阶段 (变压器深入潜水).否则,TF-IDF+大图+否定处理的无知贝斯或物流回归将是2026年生产基线.

> 如果需要以上任何一项,跳到第7阶段.

### 复制性陷 (再次)

重新训练情感模型是常规的.重新评估它们不是.报纸中报告的准确数量使用特定的分区,特定的预处理,特定的代币化.如果你比较你的新模型与一个基线,而不使用相同的管道,你会得到误导性地分数.总是重建你的基线,而不是纸质的数字.

> 重新训练情感模型是常规操作.重新评估却不是――论文中报告的准确率数字使用特定的数据分分分,特定的预处理,特定的分词器――如果你不使用完全相同的流线来比较新模型和基线,你会得到误导差值――总是在你的流线上重新生成基线,而不是用论文中的数字――

> **【中文解读】**本节关注如何将模型部署为可用的产品. 从原型到生产级系统需要考虑性能优化,错误处理,监控等多个维度.

## 运送它.

保存如`outputs/prompt-sentiment-baseline.md`其他:

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

## 练习题

1. **Easy.**加入`apply_negation`作为一个预处理步骤,在 scikit-学习管道中测量F1三角形在一个小的情感数据集.
   **简单。**将`apply_negation`作为预处理步骤,在小情感数据集中测量F1变化.
2. **Medium.**实施按类权重的物流回归 (通过 `class_weight="balanced"`测量对合成90-10类失衡的影响.
   **中等。**实现类别加权逻辑回归(传递 `class_weight="balanced"`给小学生学习,或自导梯度)                                                                                                                                                                                                                                                         
3. **Hard.**通过训练第二个分类器对情感模型的残余进行刺探测器. 记录你的实验设置. 当你的准确性低于机会时,警告读者 (二级刺的机会水平是50%左右,大多数第一次尝试都会降落在那里).
   **困难。**在情感模型的残差上训练第二类器构建刺检测器――记录你的实验设置――当你的准确率低于随机水平时警告读者――2类刺分类随机水平约为50%的,大多数第一次尝试都停留在那里)

> **【中文解读】**练习题按照易/中/难 三个难度递进;;建议至少完成中级题,Hard级适合深入研究或面试准备;;

## 关键词 快速查找表

| Term | What people say | What it actually means | 术语 | 人们常说的 | 实际含义 |
|------|-----------------|-----------------------|------|-----------|---------|
| Polarity | Positive or negative | Binary label; sometimes extended to neutral or fine-grained (5-star). | 极性（Polarity） | 正面或负面 | 二分类标签；有时扩展到中性或细粒度（5 星）。 |
| Aspect-based sentiment | Per-aspect polarity | Attribute sentiment to specific entities or attributes mentioned in text. | 基于方面的情感分析 | 每个方面的极性 | 将情感归因到文本中提到的特定实体或属性。 |
| Negation scoping | Reversing nearby tokens | Prefix tokens after "not" with `NOT_` until punctuation. | 否定范围标记 | 反转附近的 token | 在 "not" 后给 token 加 `NOT_` 前缀直到标点符号。 |
| Laplace smoothing | Adding 1 to counts | Prevents zero-probability features in Naive Bayes. | 拉普拉斯平滑 | 给计数加 1 | 防止朴素贝叶斯中出现零概率特征。 |
| L2 regularization | Shrinking weights | Adds `lambda * sum(w^2)` to loss. Essential for sparse text features. | L2 正则化 | 缩小权重 | 在损失中添加 `lambda * sum(w^2)`。对稀疏文本特征必不可少。 |

> **【中文解读】**在团队协作中,统一术语定义可以避免大量沟通误解.

## 继续阅读 继续阅读

- [Pang and Lee (2008). Opinion Mining and Sentiment Analysis](https://www.cs.cornell.edu/home/llee/opinion-mining-sentiment-analysis-survey.html)基础调查. 长,但第一四节涵盖了经典的全部内容.
- [Wang and Manning (2012). Baselines and Bigrams: Simple, Good Sentiment and Topic Classification](https://aclanthology.org/P12-2018/)论文显示大图 + 简单的贝叶斯很难以以打败短文.
- [scikit-learn text feature extraction docs](https://scikit-learn.org/stable/modules/feature_extraction.html#text-feature-extraction)参考`CountVectorizer`现在`TfidfVectorizer`着你的每一个.`CountVectorizer`,我知道.`TfidfVectorizer`及你将调参的每个参数的参考.
