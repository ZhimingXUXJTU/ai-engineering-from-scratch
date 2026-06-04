# 朴素贝叶斯

> "朴素"的假设是错的，但它还是能用。这就是它的美妙之处。

**类型：** 构建
**语言：** Python
**前置知识：** Phase 2 第 1-7 课（分类、贝叶斯定理）
**时长：** 约 75 分钟

## 学习目标

- 从零实现带 Laplace 平滑的多项式朴素贝叶斯用于文本分类
- 解释为什么朴素独立性假设在数学上错误但在实践中产生正确的类别排名
- 比较多项式、伯努利和高斯朴素贝叶斯变体，为给定特征类型选择正确的变体
- 在高维稀疏数据上评估朴素贝叶斯与逻辑回归，解释偏差-方差权衡

## 问题引入

你需要分类文本。邮件分为垃圾邮件或正常邮件。客户评论分为正面或负面。支持工单按类别分类。你有数千个特征（每个词一个）和有限的训练数据。

大多数分类器在这里会卡住。逻辑回归需要足够样本来可靠估计数千个权重。决策树一次在一个词上分裂，疯狂过拟合。KNN 在 10,000 维中毫无意义，因为每个点离其他每个点一样远。

朴素贝叶斯能处理这个。它做了一个数学上错误的假设（给定类别后每个特征与其他所有特征独立），但它仍然在文本分类上超越"更聪明"的模型，尤其是小训练集。它在单次遍历数据中训练。它扩展到数百万特征。它产生概率估计（虽然由于独立性假设通常校准不好）。

理解为什么一个错误假设能产生好的预测，教会你机器学习中基本的东西：最好的模型不是最正确的那个，而是对你的数据偏差-方差权衡最好的那个。

## 核心概念

### 贝叶斯定理（快速回顾）

贝叶斯定理翻转条件概率：

```
P(class | features) = P(features | class) * P(class) / P(features)
```

我们想要 `P(class | features)`——给定文档中的词，文档属于某类的概率。朴素假设：给定类别后每个特征条件独立。

```
P(w1, w2, ..., wn | class) = P(w1 | class) * P(w2 | class) * ... * P(wn | class)
```

不是一个不可能的联合分布，你估计 n 个简单的逐特征分布。每个只需要计数。

### 为什么它仍然有效

三个原因：

1. **排名优于校准。** 分类只需要排名最高的类别正确。即使 P(spam) = 0.99999 而真实概率是 0.7，分类器仍然正确选择 spam。

2. **高偏差，低方差。** 独立性假设是强先验。它严重约束模型，防止过拟合。训练数据有限时，一个略错但稳定的模型胜过理论正确但不稳定的模型。

3. **特征冗余抵消。** 相关特征提供冗余证据。分类器重复计数这个证据，但它也为正确类别重复计数。

第四个实用原因：朴素贝叶斯极其快速。训练是单次遍历数据计数频率。预测是矩阵乘法。你可以在几秒内训练百万文档。

### 三种变体

**多项式朴素贝叶斯 (Multinomial NB)：** 将每个特征建模为计数。适合词频或 TF-IDF 值的文本数据。

**高斯朴素贝叶斯 (Gaussian NB)：** 将每个特征建模为正态分布。适合连续特征。

**伯努利朴素贝叶斯 (Bernoulli NB)：** 将每个特征建模为二值（存在或不存在）。适合短文本或二值特征向量。与多项式不同，伯努利明确惩罚词的缺失。

| 变体 | 特征类型 | 适合 | 示例 |
|------|---------|------|------|
| 多项式 | 计数或频率 | 文本分类、词袋模型 | 邮件垃圾过滤、主题分类 |
| 高斯 | 连续值 | 正态分布特征的表格数据 | 鸢尾花分类、传感器数据 |
| 伯努利 | 二值（0/1） | 短文本、二值特征向量 | 短信垃圾过滤 |

### Laplace 平滑

当一个词出现在测试数据中但从未出现在某类的训练数据中时怎么办？

没有平滑：`P(word | class) = 0/N = 0`。一个零乘以整个乘积使 `P(class | features) = 0`，无论所有其他证据。一个未见过的词摧毁整个预测。

Laplace 平滑给每个特征计数加一个小计数 `alpha`（通常为 1）：

```
P(word_i | class) = (count(word_i, class) + alpha) / (total_words_in_class + alpha * vocab_size)
```

有了 alpha=1，每个词至少有微小概率。更高的 alpha 意味着更强的平滑（更均匀的分布）。Alpha 是你调优的超参数。

### 对数空间计算

乘以数百个概率（每个小于 1）会导致浮点下溢。解决方案：在对数空间工作。不乘概率，而是加它们的对数：

```
log P(class | x1, x2, ..., xn) = log P(class) + sum_i log P(xi | class)
```

这将预测变成点积。这就是为什么朴素贝叶斯预测如此快——它与单层线性模型的操作相同。

### 朴素贝叶斯 vs 逻辑回归

两者都是文本的线性分类器。区别在于它们建模什么。

| 方面 | 朴素贝叶斯 | 逻辑回归 |
|------|----------|---------|
| 类型 | 生成式（建模 P(X\|Y)） | 判别式（建模 P(Y\|X)） |
| 训练 | 计数频率 | 优化损失函数 |
| 小数据 | 更好（强先验有帮助） | 更差（不够估计权重） |
| 大数据 | 更差（错误假设有害） | 更好（灵活边界） |
| 速度 | 单次遍历，非常快 | 迭代优化 |

经验法则：从朴素贝叶斯开始。如果数据够多且 NB 平台期，切换到逻辑回归。

## 动手实现

### 多项式朴素贝叶斯

```python
class MultinomialNB:
    def __init__(self, alpha=1.0):
        self.alpha = alpha

    def fit(self, X, y):
        classes = np.unique(y)
        n_classes = len(classes)
        n_features = X.shape[1]

        self.classes_ = classes
        self.class_log_prior_ = np.zeros(n_classes)
        self.feature_log_prob_ = np.zeros((n_classes, n_features))

        for i, c in enumerate(classes):
            X_c = X[y == c]
            self.class_log_prior_[i] = np.log(X_c.shape[0] / X.shape[0])
            counts = X_c.sum(axis=0) + self.alpha
            self.feature_log_prob_[i] = np.log(counts / counts.sum())

        return self
```

关键洞察：拟合后，预测就是矩阵乘法加偏置。这就是为什么朴素贝叶斯这么快。

### 高斯朴素贝叶斯

对于连续特征，我们估计每个类别每个特征的均值和方差：

```python
class GaussianNB:
    def fit(self, X, y):
        classes = np.unique(y)
        self.classes_ = classes
        self.means_ = np.zeros((len(classes), X.shape[1]))
        self.vars_ = np.zeros((len(classes), X.shape[1]))
        self.priors_ = np.zeros(len(classes))

        for i, c in enumerate(classes):
            X_c = X[y == c]
            self.means_[i] = X_c.mean(axis=0)
            self.vars_[i] = X_c.var(axis=0) + 1e-9
            self.priors_[i] = X_c.shape[0] / X.shape[0]

        return self
```

完整实现和比较见 `code/naive_bayes.py`。

## 用框架实现

使用 sklearn，两种变体都是一行代码：

```python
from sklearn.naive_bayes import GaussianNB, MultinomialNB

gnb = GaussianNB()
gnb.fit(X_train, y_train)
print(f"GaussianNB 准确率: {gnb.score(X_test, y_test):.3f}")

mnb = MultinomialNB(alpha=1.0)
mnb.fit(X_train_counts, y_train)
print(f"MultinomialNB 准确率: {mnb.score(X_test_counts, y_test):.3f}")
```

文本分类用 TF-IDF + 朴素贝叶斯：

```python
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline

text_clf = Pipeline([
    ("tfidf", TfidfVectorizer()),
    ("classifier", MultinomialNB(alpha=0.1)),
])
```

### 朴素贝叶斯何时失败

1. **强特征交互。** 如果类别依赖两个特征的组合但单独不看每个，NB 会完全错过。
2. **高度相关特征有相反证据。** 特征 A 说"垃圾"而 B 说"非垃圾"，但 A 和 B 实际上完全一致。
3. **非常大的训练集。** 数据够多时，判别式模型学习真实决策边界并超越 NB。

## 产出物

本课产出：
- `outputs/skill-naive-bayes-chooser.md` -- 选择正确 NB 变体的决策技能
- `code/naive_bayes.py` -- 从零实现 MultinomialNB 和 GaussianNB，附 sklearn 比较

## 练习题

1. **平滑实验。** 用 alpha 值 0.01、0.1、1.0、10.0、100.0 在文本数据上训练 MultinomialNB。绘制准确率 vs alpha。性能峰值在哪？为什么非常高的 alpha 有害？

2. **特征独立性测试。** 取一个真实文本数据集。选两个明显相关的词（如"机器"和"学习"）。计算 P(word1 | class) * P(word2 | class) 并与 P(word1 AND word2 | class) 比较。独立性假设错多少？它影响分类准确率吗？

3. **伯努利实现。** 扩展代码添加 BernoulliNB 类。将词袋转为二值（存在/不存在）并与 MultinomialNB 在文本数据上比较准确率。伯努利何时赢？

4. **NB vs 逻辑回归。** 在文本数据上训练两者。从 100 个训练样本开始增加到 10,000。绘制两者的准确率 vs 训练集大小。逻辑回归在什么点超越朴素贝叶斯？

5. **垃圾邮件过滤器。** 构建完整的垃圾邮件分类器：分词原始邮件文本、构建词汇表、创建词袋特征、训练 MultinomialNB、用精确率和召回率评估。

## 术语速查表

| 术语 | 实际含义 |
|------|---------|
| 朴素贝叶斯 (Naive Bayes) | 应用贝叶斯定理并假设特征条件独立的分类器 |
| 条件独立 | P(A, B \| C) = P(A \| C) * P(B \| C) -- 知道 C 后 B 不提供 A 的新信息 |
| Laplace 平滑 | 给每个特征加小计数防止零概率主导预测 |
| 先验 (Prior) | P(class) -- 观察任何特征之前每个类别的概率 |
| 似然 (Likelihood) | P(features \| class) -- 如果类别已知，观察这些特征的概率 |
| 后验 (Posterior) | P(class \| features) -- 观察特征后更新的类别概率 |
| 生成式模型 | 学习 P(X \| Y) 和 P(Y)，然后用贝叶斯定理得到 P(Y \| X) 的模型 |
| 判别式模型 | 直接学习 P(Y \| X) 而不建模 X 如何生成的模型 |
| 对数概率 | 使用 log P 代替 P 防止许多小数的乘积在浮点中变为零 |

## 延伸阅读

- [scikit-learn 朴素贝叶斯文档](https://scikit-learn.org/stable/modules/naive_bayes.html) - 三种变体及数学细节
- [McCallum and Nigam (1998)](https://www.cs.cmu.edu/~knigam/papers/multinomial-aaaiws98.pdf) - 多项式 vs 伯努利文本分类的经典比较
- [Ng and Jordan (2001)](https://ai.stanford.edu/~ang/papers/nips01-discriminativegenerative.pdf) - 证明 NB 在少数据时收敛快于 LR
