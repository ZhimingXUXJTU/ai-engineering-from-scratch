# 简单的贝尔斯
# 朴素贝叶斯


> 简单的假设是错误的,它无论如何都能发挥作用.

> 简单的假设是错误的,但它仍然可以使用.

**Type:** Build | **类型：** 构建
**Language:**子**语言：**字符串
**Prerequisites:** Phase 2, Lessons 01-07 (classification, Bayes' theorem) | **前置知识：** Phase 2 第 1-7 课（分类、贝叶斯定理）
**Time:** ~75 minutes | **时间：** 约 75 分钟

## 学习目标

- 实现多项字母天真贝伊从零开始,使用拉普莱斯平滑的文本分类
  从零实现带拉普拉斯平滑的多项式简单贝叶斯用于文本分类
- 解释为什么天真的独立假设是数学上错误的,但实际上产生了正确的类排名
  解释为什么简单的独立性假设在数学上是错误的,但在实践中产生正确的类别排名
- 比较多项式,伯诺利和高斯天真贝叶斯变体,选择给定的特征类型的正确变体
  比较多项式,伯努利和高斯朴素贝叶斯变体,为特征选择正确的变体
- 评估高维度稀疏数据的逻辑回归和解释工作中偏差差异的交易
  在高维稀疏数据上评估简单的贝叶斯与逻辑回归,解释偏差-方差权衡


> **【中文解读】**
> 简单贝叶斯基于贝叶斯定理 + 特性独立性假设──虽然假设很强大,但在文本分类中出奇地好──在学习中多边NB/高斯NB──

> **【拓展：朴素贝叶斯在垃圾邮件过滤和情感分析中的应用】**
> 早期垃圾邮件过器 (如SpamAssassin) 大量使用朴素贝叶斯,因为它在特征维度高的表达可达数十万),但训练样本少的场景表现出色.

## 问题 问题引入

你需要将文本分类.电子邮件分为垃圾邮件或非垃圾邮件.客户评论分为积极或负面.支持门票分为类别.你有数千个功能 (每字一个) 和有限的培训数据.

> 你需要将文本分为垃圾邮件或非垃圾邮件. 客户评论分为正面或负面. 文本单独分为不同类别.

现在,我们需要一个单词,一个单词,一个单词,一个单词,一个单词,一个单词,一个单词,一个单词,一个单词,一个单词,一个单词,一个单词,一个单词,一个单词,一个单词,一个单词,一个单词,一个单词,一个单词,一个单词,一个单词,一个单词,一个单词,一个单词,一个单词,一个单词,一个单词,一个单词,一个单词,一个单词,一个单词,一个单词,一个单词,一个单词,一个单词,一个单词,一个单词,一个单词,一个单词,一个单词,一个单词,一个单词,一个单词,一个单词,一个单词,一个单词,一个单词,一个单词,一个单词,一个单词,一个单词,一个单词,一个单词,一个单词,一个单词,一个单词,一个单词,一个单词,一个单词,一个单词,一个单词,一个单词,一个单词,一个单词,一个单词,一个单词,一个单词,一个单词,一个单词,一个单词,一个单词,一个单词,一个单词,一个单词,一个单词,一个,一个单词,一个,一个单词,一个,一个,一个,一个,一个,一个,一个,一个,一个,一个,一个,一个,一个,一个,一个,一个,一个,一个,一个,一个,一个,一个,一个,一个,一个,一个,一个,一个,一个,一个,一个,一个,一个,一个,一个,一个,一个,一个,一个,一个,一个,一个,一个,一个,一个,一个,一个,一个,一个,一个,一个,一个,一个,一个,一个,一个,一个,一个,一个,一个,一个,一个,一个,一个,一个,一个,一个,一个,一个,一个,一个,一个,一个,一个,一个,一个,一个,一个,一个,一个,一个,一个,一个,一个,一个,一个,一个,一个,一个,一个,一个,一个,一个,一个,一个,一个,一个

> 大多数分类器在这里会卡住.逻辑归归需要足够的样式可靠估计数千个权力.决策树每次在一个词上分开并过度合适.

简单的贝耶斯处理这个. 它对数学错误的假设 (每个特征都是独立于给定的类别的其他特征),而且仍然超过了文本分类的"更聪明"模型,特别是小型培训集. 它通过数据进行一次训练. 它可以达到数百万个特征. 它产生了概率估计 (尽管由于独立假设,通常是未准确的).

> 简单的贝叶斯能处理这种情况――它做了一个数学错误的假设――但在文本分类上仍然优于"更聪明"的模型,特别是在小训练集中――它只需要一次遍历数据就能训练――它扩展到数百万个特征――它产生概率估计 (尽管独立假设通常校准不佳)

了解为什么错误的假设导致了好预测,就教你机器学习的基本知识:最好的模型不是最正确的,

> 了解错误假设能产生良好的预测会教会你机器学习中的一些基本东西:最好的模型不是最正确的模型,而是对你的数据的差距衡量最好的模型.

> **【中文解读】**
> 朴素贝叶斯的"朴素"在于假设所有特征在给定的类别下相互独立. 这在现实中几乎不存在.如"免费"和"优惠"在垃圾邮件中高度相关.但为什么还可以使用?因为分类只需要各类概率的排名正确,不需要概率值精确.

## 概念的核心概念

### 贝叶斯定理 (快速复习)

贝叶斯定理反转了条件概率:

> 贝叶斯定理翻转条件概率:

```
P(class | features) = P(features | class) * P(class) / P(features)
```

我们想要`P(class | features)`根据文件中的字符,一个文件属于一个类的概率.
- `P(features | class)`-- 看到这些词在本类文件中的可能性
  `P(features | class)`在这个类档案中看到这些词的相似
- `P(class)`-- 类别的先前概率 (一般情况下垃圾邮件是多么普遍?)
  `P(class)`垃圾邮件通常有多常见?
- `P(features)`证据,同样适用于所有类别,所以我们可以忽略它,
  `P(features)`-- 证据,对所有类别都相同,比较时可以忽略

那些有最高的类型`P(class | features)`赢了.

> `P(class | features)`最好的类别是胜利.

### 无明自主假设

计算`P(features | class)`总体而言,如果我们使用1万个词汇,我们需要估计2^10,000个可能的组合.

> 精确计算`P(features | class)`需要估计所有特征的联合概率.对于10,000个词表,你需要估计2^10,000种可能组合分布.

简单的假设:每一个特征都在给定类别的条件下独立.

> 简单假设:给定类别下每个特征条件独立.

```
P(w1, w2, ..., wn | class) = P(w1 | class) * P(w2 | class) * ... * P(wn | class)
```

它们只需要一个数值,一个数值,一个数值,一个数值,一个数值.

> 你不需要估计一个不可能的联合分布,而是估计一个简单的特征分布.

这种假设显然是错误的. "机器"和"学习"的单词在任何文档中都不独立.但分类器不需要正确的概率估计.它需要正确的排名 - - 哪个类具有最高的概率.独立假设引入系统错误,但这些错误对所有类别都同样影响,所以排名保持正确.

> 这种假设显然是错误的. "机器"和"学习"在任何文档中都不是独立的.但分类器件不需要正确的概率估计.

### 为什么它仍然有效

原因有三个:

> 三个原因:

1. **Ranking over calibration.**排名只需要排名最好的类别才是正确的.即使P(spam) =0.99999 当真实概率为0.7,排名器仍然选择了正确的垃圾邮件.我们不需要正确的概率.我们需要正确的赢家.
   **排名优于校准。**虽然P(spam) =0.99999 而真实概率是0.7,分类器仍然正确选择垃圾邮件――我们不需要正确的概率――我们需要正确的赢家――

2. **High bias, low variance.**独立假设是一个强大的先驱.它严重限制了模型,这防止过度匹配. 有限训练数据,一个略错误但稳定的模型比一个理论上正确但非常不稳定的模型更好.这是偏差变异的交易.
   **高偏差、低方差。**独立性假设是一个强先验――它严重约束模型,防止过拟合――在有限的训练数据下,一个稍微错误但稳定的模型胜过理论上正确但极不稳定的模型――这是偏差-差差权衡的实际运作――

3. **Feature redundancy cancels out.**相关的特性提供了冗余的证据.分类器对这些证据进行双重计算,但对正确类型也进行双重计算.如果"机器"和"学习"总是出现在一起,则这两者都为"技术"类提供证据.NB会两次计算,但对正确类型计算两次.
   **特征冗余相互抵消。**相关特征提供冗余证据. 分类重复计数这些证据,但正确类别的证据也被重复计数. 如果"机器"和"学习"总是出现,它们都为"技术"类提供证据.

第四个,实际原因是:天真贝耶斯非常快.训练是通过数据计算频率的单次通过.预测是矩阵乘法.你可以在几秒钟内训练100万份文件.这种速度意味着你可以更快地反复,尝试更多的功能集,并且比较慢的模型运行更多实验.

> 第四个实际原因:简单贝叶斯极快――训练是单次遍历数据计数频率――预测是矩阵乘法――你可以在几秒钟内训练一百万个文档――这种速度意味着你可以比使用更慢的模型更快代――尝试更多特征――运行更多实验――

### 数学一步一步

让我们通过一个具体的例子来追踪.假设我们有两个类别:垃圾邮件和非垃圾邮件.我们的词汇有三个词汇:"免费","钱","会议".

培训数据:
- 垃圾邮件中提到"免费"80次,"钱"60次,"会议"10次 (150个词汇总)
- 没有垃圾邮件中提到"免费" 5 次,"钱" 10 次,"会议" 100 次 (115 个词汇总)
- 40%的电子邮件是垃圾邮件,60%是非垃圾邮件

平 (alpha=1):

```
P(free | spam)    = (80 + 1) / (150 + 3) = 81/153 = 0.529
P(money | spam)   = (60 + 1) / (150 + 3) = 61/153 = 0.399
P(meeting | spam) = (10 + 1) / (150 + 3) = 11/153 = 0.072

P(free | not-spam)    = (5 + 1) / (115 + 3) = 6/118 = 0.051
P(money | not-spam)   = (10 + 1) / (115 + 3) = 11/118 = 0.093
P(meeting | not-spam) = (100 + 1) / (115 + 3) = 101/118 = 0.856
```

新电子邮件包含"免费" (2次),"钱" (1次),"会议" (0次).

```
log P(spam | email) = log(0.4) + 2*log(0.529) + 1*log(0.399) + 0*log(0.072)
                    = -0.916 + 2*(-0.637) + (-0.919) + 0
                    = -3.109

log P(not-spam | email) = log(0.6) + 2*log(0.051) + 1*log(0.093) + 0*log(0.856)
                        = -0.511 + 2*(-2.976) + (-2.375) + 0
                        = -8.838
```

垃圾邮件以大差距获胜.出现两次的"免费"字是垃圾邮件的强烈证据.注意,不出现的"会议"对两个日志数量 (0 * log(P)) 贡献了零 - 在多项名词NB中,缺失的单词没有影响.是伯诺利NB明确模拟词缺失.

### 三种方式

简单的贝耶斯有三个口味.`P(feature | class)`没有什么不同.

> 简单的贝叶斯有三个变体.`P(feature | class)`建模方式不同.

#### 多数字 无明的贝斯

模型将每个特征作为一个数值.最适合文字数据,其中特征是单词频率或TF-IDF值.

> 给每个特征构建为数量. 最适合的特征是词频或TF-IDF值的文本数据.

```
P(word_i | class) = (count of word_i in class + alpha) / (total words in class + alpha * vocab_size)
```

其他`alpha`拉普莱斯平滑 (下面解释). 这种变体是文本分类的工作马.

> `alpha`是拉普拉斯平滑(下面解释) .

#### 盖斯人天真的贝斯

模型将每个功能作为正常分布.

> 给每一个特征构建模型为正态分布.

```
P(x_i | class) = (1 / sqrt(2 * pi * var)) * exp(-(x_i - mean)^2 / (2 * var))
```

每个类别都有其各自的平均值和变异.

> 每个类别对每个特征都有其平均值和方差.

#### 伯诺利天真的贝耶斯

模型每个特征都作为二进制 (现或缺).最适合短文本或二进制特征向量.

> 把每个特征建模为二值 (或不) .

```
P(word_i | class) = (docs in class containing word_i + alpha) / (total docs in class + 2 * alpha)
```

与多个字母不同,伯诺利明确地惩罚了一个词的缺失.如果"免费"通常在垃圾邮件中出现,但不在这个电子邮件中,伯诺利将其视为反对垃圾邮件的证据.

> 由于不多项式,伯努利明确惩罚词的出现不存在. 如果"免费"通常出现在垃圾邮件中,但没有,伯努利将其视为反对垃圾邮件的证据.

### 每种变体何时使用

| Variant | Feature Type | Best For | Example |
|---------|-------------|----------|---------|
| Multinomial | Counts or frequencies | Text classification, bag-of-words | Email spam, topic classification |
| Gaussian | Continuous values | Tabular data with normal-ish features | Iris classification, sensor data |
| Bernoulli | Binary (0/1) | Short text, binary feature vectors | SMS spam, presence/absence features |

| 变体 | 特征类型 | 最适合 | 示例 |
|------|---------|--------|------|
| Multinomial | 计数或频率 | 文本分类、词袋 | 邮件垃圾过滤、主题分类 |
| Gaussian | 连续值 | 近正态的表格数据 | 鸢尾花分类、传感器数据 |
| Bernoulli | 二值（0/1） | 短文本、二值特征向量 | 短信垃圾过滤、出现/缺失特征 |

### 拉普拉斯滑滑

如果一个词出现在测试数据中,但从来没有出现在特定类的培训数据中,会发生什么?

> 如果一个词在测试数据中出现,但从未出现在某种类别的训练数据中,会发生什么?

没有滑滑:`P(word | class) = 0/N = 0`一个零乘以整个产品,`P(class | features) = 0`无论其他证据如何,一个单独的未见字都会摧毁整个预测,

> 没有平滑:`P(word | class) = 0/N = 0`零乘到整个乘积中会使`P(class | features) = 0`无论其他证据如何. 一个未见的词都破坏了整个预测.

平的平增加了少量`alpha`(通常是1) 对每一个特征数量:

> 给每个特征加一个小数.`alpha`(通常为1):

```
P(word_i | class) = (count(word_i, class) + alpha) / (total_words_in_class + alpha * vocab_size)
```

随着alpha=1,每个字至少得到一个微小的概率.在测试电子邮件中出现的"discombobulate"字不再杀死垃圾邮件概率.滑滑有贝耶斯解释:它相当于在词分布前放置统一的Dirichlet.

> 简单有贝叶斯解释:等于在词分布上放一个均的直径先验.

较高的阿尔法意味着更强的平滑 (更均的分布).较低的阿尔法意味着模型更信任数据.阿尔法是一个调节的超参数.

> 更高的阿尔法意味着更强的平滑(更接近均分布) ――更低的阿尔法意味着模型更相信数据――――阿尔法是你调用的超参数――

艾尔法的作用:

> 影响:

| Alpha | Effect | When to use |
|-------|--------|-------------|
| 0.001 | Almost no smoothing, trust the data | Very large training set, no unseen features expected |
| 0.1 | Light smoothing | Large training set |
| 1.0 | Standard Laplace smoothing | Default starting point |
| 10.0 | Heavy smoothing, flattens distributions | Very small training set, many unseen features expected |

| Alpha | 效果 | 使用场景 |
|-------|------|---------|
| 0.001 | 几乎不平滑，相信数据 | 非常大的训练集，预期不会有未见特征 |
| 0.1 | 轻度平滑 | 大训练集 |
| 1.0 | 标准 Laplace 平滑 | 默认起点 |
| 10.0 | 重度平滑，拉平分布 | 非常小的训练集，预期有很多未见特征 |

### 记录空间计算

乘以数百个概率 (每一个小于1) 导致浮点下流. 产品在浮点变为零,尽管真实值是一个非常小的正数.

> 把数百个概率 (每一个小于1) 乘以导致浮点下溢.即使真实值是一个极小的正数,乘积在浮点下也会变成零.

解决方案:在日志空间中工作.

> 解决方案:在对数空间计算中,把概率相乘以对数相加:

```
log P(class | x1, x2, ..., xn) = log P(class) + sum_i log P(xi | class)
```

这将预测变成一个点数:

> 这种预测变成了点积:

```
log_scores = X @ log_feature_probs.T + log_class_priors
prediction = argmax(log_scores)
```

这就是为什么天真贝叶斯的预测如此快速-- 它与单层线性模型相同的操作.

> 矩阵乘法――这就是简单的贝叶斯预测如此快速的原因它和单层线性模型是同一个操作――

### 简单的贝尔斯与物流回归

它们的分类是线性,它们的模特是不同的.

> 它们都是文本的线性分类器.

| Aspect | Naive Bayes | Logistic Regression |
|--------|------------|-------------------|
| Type | Generative (models P(X\|Y)) | Discriminative (models P(Y\|X)) |
| Training | Count frequencies | Optimize loss function |
| Small data | Better (strong prior helps) | Worse (not enough to estimate weights) |
| Large data | Worse (wrong assumption hurts) | Better (flexible boundary) |
| Features | Assumes independence | Handles correlations |
| Speed | Single pass, very fast | Iterative optimization |
| Calibration | Poor probabilities | Better probabilities |

| 方面 | 朴素贝叶斯 | 逻辑回归 |
|------|----------|---------|
| 类型 | 生成式（建模 P(X\|Y)） | 判别式（建模 P(Y\|X)） |
| 训练 | 统计频率 | 优化损失函数 |
| 小数据 | 更好（强先验有帮助） | 更差（数据不足以估计权重） |
| 大数据 | 更差（错误假设有害） | 更好（灵活边界） |
| 特征 | 假设独立 | 能处理相关性 |
| 速度 | 单次遍历，极快 | 迭代优化 |
| 校准 | 概率校准差 | 概率校准更好 |

基本规则:从天真的贝伊斯开始.如果你有足够的数据和NB高原,

> 经验法则:先用简单的贝叶斯. 如果数据足够且NB 性能停滞,换逻辑回归.

### 类别管道

```mermaid
flowchart LR
    A[Raw Text] --> B[Tokenize]
    B --> C[Build Vocabulary]
    C --> D[Count Word Frequencies]
    D --> E[Apply Smoothing]
    E --> F[Compute Log Probabilities]
    F --> G[Predict: argmax P class given words]

    style A fill:#f9f,stroke:#333
    style G fill:#9f9,stroke:#333
```

实际上,我们在日志空间中工作,以避免浮点的下流.

```
log P(class | features) = log P(class) + sum_i log P(feature_i | class)
```

## 建立它,实现它.

> **【中文解读】**
> 从零实现多项式简单贝叶斯 (多项式NB,用于文本分类) 和高斯朴素贝叶斯 (高斯朴素贝叶斯) 开始,用于连续特征.

> **【拓展：朴素贝叶斯在现代 NLP 中的角色演变】**
> 虽然变压器模型 (BERT、GPT) 在NLP任务上远远超过了朴素贝叶斯,但朴素贝叶斯仍然有其用处:实时垃圾邮件过(毫秒级延迟) 、大规模文本预分类(成本极低) 、作为基线快速验证特征工程效果――在医疗诊断中,高斯朴素贝叶斯因输出概率可解释而广泛使用医生需要知道"有多大把握",而不是黑箱输出.
```figure
naive-bayes
```

## 建立它

编码在`code/naive_bayes.py`实现了多项NB和高斯NB的基础.

### 多号号NB

从零开始实施:

1. **fit(X, y)**对于每个类,计算每个特征的频率. 添加拉普莱斯平滑. 计算日志概率. 存储类先例 (类频率日志).

2. **predict_log_proba(X)**对于每个样本,计算 log P(class) + log P(feature_i 类) 对所有类.这是一个矩阵乘法: X @ log_probs.T + log_priors.

3. **predict(X)**返回具有最高日志概率的类.

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

基本的见解是,在合适后,预测只是矩阵乘法加上偏见.

### 盖斯尼NB

对于连续特征,我们估计每个特征的平均和变异:

```python
class GaussianNB:
    def __init__(self):
        pass

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

预测使用每个特征的高斯式PDF,乘以各个特征 (在日志空间中添加).

### 演示:文本分类

代码生成合成的单词数据,模拟两个类 (技术文章与体育文章).每个类别都有不同的单词频率分布.多项NB使用单词数来分类它们.

合成数据的运作是这样的:我们创建了200个"字" (特征列). 0-39字在技术文章中频率高,体育中频率低. 80-119字在体育中频率高,技术中频率低. 40-79字在两种中都是中频.这创造了一个现实化的场景,其中一些字是强大的类别指标,而其他是噪音.

### 演示:连续功能

该代码生成类似于Iris的数据 (3类, 4个特征,高斯群).高斯NB使用每个类的平均和变异进行分类.每个类都有不同的中心 (平均向量) 和不同的扩散 (变异),模仿现实世界的数据,其中测量在类别之间有系统的差异.

代码还表明:
- **Smoothing comparison:**训练多号NB以不同的阿尔法值来显示滑动强度对精度的影响.
- **Training size experiment:**随着训练数据的增长,NB的精度如何提高,从20个样本增长到1600个样本.
- **Confusion matrix:**按班级精度,召回,F1分数显示NB犯错误的地方.

### 预测速度

简单的贝叶斯预测是矩阵乘法.
- 多数NB:一个矩阵乘以 (n x d) @ (d x k) = O(n * d * k)
- 盖斯NB:n * k 盖斯PDF评估,每个都包含d特征 = O(n * d * k)

两者在每一个维度都是线性的.比较KNN (需要计算距离到所有训练点) 或SVM与RBF内核 (需要对所有支持向量的内核评估).NB在预测时间上以大小顺序更快.

## 用它实现框架

两种变体均为单线:

```python
from sklearn.naive_bayes import GaussianNB, MultinomialNB

gnb = GaussianNB()
gnb.fit(X_train, y_train)
print(f"GaussianNB accuracy: {gnb.score(X_test, y_test):.3f}")

mnb = MultinomialNB(alpha=1.0)
mnb.fit(X_train_counts, y_train)
print(f"MultinomialNB accuracy: {mnb.score(X_test_counts, y_test):.3f}")
```

对于与 sklearn 的文本分类:

```python
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline

text_clf = Pipeline([
    ("vectorizer", CountVectorizer()),
    ("classifier", MultinomialNB(alpha=1.0)),
])

text_clf.fit(train_texts, train_labels)
accuracy = text_clf.score(test_texts, test_labels)
```

编码在`naive_bayes.py`根据相同数据进行零部实施与Skularn的比较,以验证正确性.

### 们在们的家里,

字数量为每一个字的重量等于每一个事件. 但"the"和"is"等常见字在每个类中经常出现 - - 它们没有信息.TF-IDF (Term Frequency - Inverse Document Frequency) 低于常见字,高于罕见的歧视性字.

```python
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline

text_clf = Pipeline([
    ("tfidf", TfidfVectorizer()),
    ("classifier", MultinomialNB(alpha=0.1)),
])
```

TF-IDF值是非负的,因此它们与MultinomialNB一起工作.TF-IDF + MultinomialNB的组合是文本分类的最强的基线之一.它经常击败了不到10,000个训练样本的数据集上的更复杂的模型.

### 简短文本的BernoulliNB

对于短文本 (推文,短信,聊天消息),BernoulliNB可以超过MultinomialNB.短文本的单词数量较低,因此MultinomialNB依赖于的频率信息很杂.BernoulliNB只关心存在或缺席,这更可靠于短文本.

```python
from sklearn.naive_bayes import BernoulliNB
from sklearn.feature_extraction.text import CountVectorizer

text_clf = Pipeline([
    ("vectorizer", CountVectorizer(binary=True)),
    ("classifier", BernoulliNB(alpha=1.0)),
])
```

其他`binary=True`没有它,BernoulliNB仍然运行,但看到它不是设计的数量.

### 校准NB概率

如果您需要可靠的概率估计 (例如,设定门值或与其他模型结合),请使用 sklearn 的校准分类CV:

```python
from sklearn.calibration import CalibratedClassifierCV

calibrated_nb = CalibratedClassifierCV(MultinomialNB(), cv=5, method="sigmoid")
calibrated_nb.fit(X_train, y_train)
proba = calibrated_nb.predict_proba(X_test)
```

这符合NB的原始分数上的一次物流回归,使用交叉验证.结果的概率远接近真正的类频率.

### 常见的古特哈

1. **Negative feature values.**多数式NB需要非负值的特性.如果你有负值 (如TF-IDF,某些设置或标准化功能),请使用GaussianNB代替,或者将功能转换为正值.

2. **Zero variance features.**盖斯NB按变异分为:如果一个特征为一个类别 (所有值均为相同) 具有零变异,概率计算会断裂.代码将一个小的平滑术语 (1e-9) 添加到所有变异中以防止这一点.

3. **Class imbalance.**如果99%的电子邮件是非垃圾邮件,前 P(非垃圾邮件) = 0.99 非常强大,以至于它压倒了概率证据.你可以手动设置类优先级或在 sklearn 中使用class_prior参数.

4. **Feature scaling.**多数项NB不需要扩展 (它运作在计算上).高斯式NB也不需要扩展 (它估计每个特征的统计).这是对物流回归和SVM的优势,这些特征规模很敏感.

## 运送它.

这一课产生了:
- `outputs/skill-naive-bayes-chooser.md`-- 选择合适的NB变体的决策技能
- `code/naive_bayes.py`--从零开始的多项NB和高斯NB,

### 当天真的贝耶斯失败时

独立假设导致错误排名 (不仅仅是错误的概率) 时,NB失败.

1. **Strong feature interactions.**如果类别取决于两个特征的组合,但不是单独的组合 (XOR类似的模式),NB将完全错过它.单独的每个特征都没有证据,NB不能将它们结合非线性.

2. **Highly correlated features with opposing evidence.**如果特征A表示"垃圾邮件",B表示"非垃圾邮件",但A和B完全相关 (在现实中总是一致),NB将看到没有的矛盾证据.

3. **Very large training sets.**具有足够的数据,物流回归等歧视性模型学习了真正的决策界限,并超过了NB.

在实践中,这些失败模式对于文本分类很少见.文本特征是众多的,个别弱,独立假设的错误往往会被取消.对于少数强烈相关特征的表格数据,首先考虑物流回归或基于树的模型.

## 练习题

1. **Smoothing experiment.**训练 MultinomialNB 在文字数据上,以0.01,0.1,1.0,10.0,和100.0的阿尔法值. 图谱精度与阿尔法. 性能最高点在哪里?
   1. **平滑实验。**用alpha 值0.01、0.1、1.0、10.0、100.0 在文本数据上训练多边数NB──绘制准确率与alpha──性能峰值在哪里?为什么很高的alpha 有害?

2. **Feature independence test.**拿一个真实的文本数据集. 选择两个明显相关的词语 ("机器"和"学习").计算P 字1类) *P 字2类) 和P 字1和字2类. 独立假设是多么错误的? 它是否影响了分类准确性?
   2. **特征独立性测试。**取一个真实文本数据集. 选两个明显相关词语 (如"机器"和"学习") 计算 P(字1 类) * P(字2 类) 并与 P(字1 和字2 类) 比较. 独立性假设错误多少?它影响分类准确率吗?

3. **Bernoulli implementation.**扩展代码使用BernoulliNB类.将字符包转换为二进制 (现/缺) 并对文本数据的MultinomialNB进行准确比较.Bernoulli什么时候获胜?
   3. **伯努利实现。**扩展代码添加BernoulliNB类型――将词袋转为二值(存在/不存在)并与多元NB在文本数据上比较准确率――伯努利何时赢?

4. **NB vs Logistic Regression.**训练两个在文本数据.从100个训练样本开始,增加到10,000. 剧情精度与训练集尺寸对两个. 在什么时候物流回归超过天真的贝斯?
   4. **NB vs 逻辑回归。**在文本数据上训练两者――从100个训练样本开始增加到10,000――绘制两者的准确率与训练集大小――逻辑回归在什么点上超越简单的贝叶斯?

5. **Spam filter.**建立一个完整的垃圾邮件分类器:标记原始电子邮件文本,建立词汇,创建字包功能,训练多维数NB,精确评估和回忆 (不仅仅是精确性 - 为什么?).
   5. **垃圾邮件过滤器。**构建完整的垃圾邮件分类器:分词原始邮件文本、构建词汇表、创建词袋特征、训练 多数字母NB、使用精确率和召回率评估──

> **【中文解读】**
> 朴素贝叶斯的三种变体:(1) 多项式朴素贝叶斯(多数NB) 适用于词频/TF-IDF特征文本分类;(2) 伯努利朴素贝叶斯(BernoulliNB) 适用于二值特征(词是否出现);(3) 高斯朴素贝叶斯(GaussianNB) 适用于连续特征,假设每类内特征从正态分布中征服――平滑加上

## 关键词 快速查找表

| Term | What people say | What it actually means |
|------|----------------|----------------------|
| Naive Bayes | "Simple probabilistic classifier" | A classifier that applies Bayes' theorem with the assumption that features are conditionally independent given the class |
| Conditional independence | "Features don't affect each other" | P(A, B \| C) = P(A \| C) * P(B \| C) -- knowing B tells you nothing new about A once you know C |
| Laplace smoothing | "Add-one smoothing" | Adding a small count to every feature to prevent zero probabilities from dominating the prediction |
| Prior | "What you believed before seeing data" | P(class) -- the probability of each class before observing any features |
| Likelihood | "How well the data fits" | P(features \| class) -- the probability of observing these features if the class is known |
| Posterior | "What you believe after seeing data" | P(class \| features) -- the updated probability of the class after observing the features |
| Generative model | "Models how data is generated" | A model that learns P(X \| Y) and P(Y), then uses Bayes' theorem to get P(Y \| X) |
| Discriminative model | "Models the decision boundary" | A model that directly learns P(Y \| X) without modeling how X is generated |
| Log probability | "Avoid underflow" | Working with log P instead of P to prevent the product of many small numbers from becoming zero in floating point |

## 继续阅读 继续阅读

- [scikit-learn Naive Bayes docs](https://scikit-learn.org/stable/modules/naive_bayes.html)-- 所有三个变体都具有数学细节
  [scikit-learn 朴素贝叶斯文档](https://scikit-learn.org/stable/modules/naive_bayes.html)- 三种变体及数学细节
- [McCallum and Nigam, A Comparison of Event Models for Naive Bayes Text Classification (1998)](https://www.cs.cmu.edu/~knigam/papers/multinomial-aaaiws98.pdf)-- 对于文本来说,多项和伯诺利的经典比较
  [McCallum and Nigam (1998)](https://www.cs.cmu.edu/~knigam/papers/multinomial-aaaiws98.pdf)- 多项式与伯努利文本分类的经典比较
- [Rennie et al., Tackling the Poor Assumptions of Naive Bayes Text Classifiers (2003)](https://people.csail.mit.edu/jrennie/papers/icml03-nb.pdf)-- 改进文本的NB
  [Ng and Jordan (2001)](https://ai.stanford.edu/~ang/papers/nips01-discriminativegenerative.pdf)- 证明NB 在少数据时收获快于 LR
- [Ng and Jordan, On Discriminative vs. Generative Classifiers (2001)](https://ai.stanford.edu/~ang/papers/nips01-discriminativegenerative.pdf)--证明NB比LR更快地相近,数据少
