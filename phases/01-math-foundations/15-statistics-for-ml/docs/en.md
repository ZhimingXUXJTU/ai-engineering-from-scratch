# Statistics for Machine Learning | 机器学习统计学

> Statistics is how you know if your model actually works or just got lucky.
> 统计学告诉你模型是真的有效还是只是运气好。

**Type:** Build | **类型:** 动手
**Language:** Python | **语言:** Python
**Prerequisites:** Phase 1, Lessons 06 (Probability and Distributions), 07 (Bayes' Theorem) | **前置知识:** Phase 1, 第 06 课（概率与分布）、第 07 课（贝叶斯定理）
**Time:** ~120 minutes | **时间:** ~120 分钟

## Learning Objectives | 学习目标

- Compute descriptive statistics, Pearson/Spearman correlation, and covariance matrices from scratch
  从零计算描述性统计量、Pearson/Spearman 相关系数和协方差矩阵

- Perform hypothesis tests (t-test, chi-squared) and interpret p-values and confidence intervals correctly
  执行假设检验（t 检验、卡方检验），正确解释 p 值和置信区间

- Use bootstrap resampling to construct confidence intervals for any metric without distributional assumptions
  使用 Bootstrap 重采样为任意指标构建置信区间，无需分布假设

- Distinguish statistical significance from practical significance using effect size measures
  使用效应量区分统计显著性与实际显著性

> **【中文解读】**
> 统计学告诉你模型是真的有效还是运气好。A/B 测试评估新模型、Bootstrap 构建置信区间、假设检验判断差异显著性——这些是 ML 实验评估的基础。

## The Problem | 问题引入

> **【中文解读】** 模型 A 准确率 0.87，模型 B 准确率 0.89，你部署了 B。三周后线上效果反而变差了——因为 0.02 的差异是噪声不是真实提升。统计学回答：差异是否显著？置信区间多宽？样本量够不够？没有统计学的 ML 实验 = 瞎子摸象。

## The Concept | 核心概念

> **【拓展：AI 工程中的统计学实战】** (1) **A/B 测试**：推荐/搜索模型上线前必须做，统计显著（p<0.05）才发布；(2) **Bootstrap 置信区间**：不用假设数据分布，用重采样构建任意指标的置信区间；(3) **效应量**：p 值只告诉你"有没有差异"，效应量告诉你"差异有多大"——统计显著 ≠ 实际有用；(4) **多重比较校正**：调了 20 个超参数取最好的，必须校正否则是"多碰运气"。

This happens constantly. Kaggle leaderboard shakeups. Papers that fail to reproduce. A/B tests that declare winners based on a few hundred samples. The root cause is always the same: someone skipped the statistics.

> 这种事经常发生。Kaggle 排行榜的大洗牌。无法复现的论文。基于几百个样本就宣布赢家的 A/B 测试。根本原因总是相同的：有人跳过了统计学。

Statistics gives you the tools to distinguish signal from noise. It tells you when a difference is real, how confident you should be, and how much data you need before you can trust a result. Every ML pipeline, every model comparison, every experiment needs statistics. Without it, you are guessing.

> 统计学为你提供了区分信号和噪声的工具。它告诉你差异何时是真实的，你应该有多大信心，以及你需要多少数据才能信任一个结果。每个 ML 管道、每个模型比较、每个实验都需要统计学。没有它，你就是在猜测。

## The Concept | 核心概念

### Descriptive Statistics: Summarizing Your Data | 描述性统计：汇总你的数据

Before you model anything, you need to know what your data looks like. Descriptive statistics compress a dataset into a few numbers that capture its shape.

> 在建立任何模型之前，你需要了解数据的样子。描述性统计将数据集压缩成几个能捕捉其形状的数字。

**Measures of central tendency** answer "where is the middle?"

> **集中趋势度量** 回答"中间在哪里？"

```
Mean:   sum of all values / count
        mu = (1/n) * sum(x_i)

Median: middle value when sorted
        Robust to outliers. If you have [1, 2, 3, 4, 1000], the mean is 202
        but the median is 3.

Mode:   most frequent value
        Useful for categorical data. For continuous data, rarely informative.
```

The mean is the balance point. The median is the halfway mark. When they diverge, your distribution is skewed. Income distributions have mean >> median (right skew from billionaires). Loss distributions during training often have mean << median (left skew from easy samples).

> 均值是平衡点。中位数是中间标记。当它们偏离时，你的分布就是偏斜的。收入分布的均值远大于中位数（亿万富翁造成的右偏）。训练期间的损失分布通常均值远小于中位数（简单样本造成的左偏）。

**Measures of spread** answer "how dispersed is the data?"

> **离散程度度量** 回答"数据有多分散？"

```
Variance:   average squared deviation from the mean
            sigma^2 = (1/n) * sum((x_i - mu)^2)

Standard deviation:  square root of variance
                     sigma = sqrt(sigma^2)
                     Same units as the data, so more interpretable.

Range:      max - min
            Sensitive to outliers. Almost never useful alone.

IQR:        Q3 - Q1 (interquartile range)
            The range of the middle 50% of the data.
            Robust to outliers. Used for box plots and outlier detection.
```

**Percentiles** divide sorted data into 100 equal parts. The 25th percentile (Q1) means 25% of values fall below this point. The 50th percentile is the median. The 75th percentile is Q3.

> **百分位数** 将排序后的数据分成 100 等份。第 25 百分位数（Q1）意味着 25% 的值低于此点。第 50 百分位数就是中位数。第 75 百分位数是 Q3。

```
For latency monitoring:
  P50 = median latency        (typical user experience)
  P95 = 95th percentile       (bad but not worst case)
  P99 = 99th percentile       (tail latency, often 10x the median)
```

In ML, you care about percentiles for inference latency, prediction confidence distributions, and understanding error distributions. A model with low average error but terrible P99 error might be useless for safety-critical applications.

> 在 ML 中，你关注推理延迟、预测置信度分布和误差分布的百分位数。一个平均误差低但 P99 误差很差的模型，对于安全关键应用可能是无用的。

**Sample vs population statistics.** When computing variance from a sample, divide by (n-1) instead of n. This is Bessel's correction. It compensates for the fact that your sample mean is not the true population mean. With n in the denominator, you systematically underestimate the true variance. With (n-1), the estimate is unbiased.

> **样本统计 vs 总体统计。** 从样本计算方差时，除以 (n-1) 而不是 n。这是贝塞尔校正（Bessel's correction）。它补偿了样本均值不是真实总体均值这一事实。分母用 n 会系统性地低估真实方差。用 (n-1)，估计是无偏的。

```
Population variance: sigma^2 = (1/N) * sum((x_i - mu)^2)
Sample variance:     s^2     = (1/(n-1)) * sum((x_i - x_bar)^2)
```

In practice: if n is large (thousands of samples), the difference is negligible. If n is small (dozens of samples), it matters.

> 实践中：如果 n 很大（数千个样本），差异可以忽略。如果 n 很小（几十个样本），差异很重要。

### Correlation: How Variables Move Together | 相关性：变量如何一起变动

Correlation measures the strength and direction of a linear relationship between two variables.

> 相关性衡量两个变量之间线性关系的强度和方向。

**Pearson correlation coefficient** measures linear association:

> **Pearson 相关系数** 衡量线性关联：

```
r = sum((x_i - x_bar)(y_i - y_bar)) / (n * s_x * s_y)

r = +1:  perfect positive linear relationship
r = -1:  perfect negative linear relationship
r =  0:  no linear relationship (but there might be a nonlinear one!)

Range: [-1, 1]
```

Pearson assumes the relationship is linear and both variables are roughly normally distributed. It is sensitive to outliers. A single extreme point can drag r from 0.1 to 0.9.

> Pearson 假设关系是线性的，且两个变量大致服从正态分布。它对异常值敏感。一个极端点就可以将 r 从 0.1 拖到 0.9。

**Spearman rank correlation** measures monotonic association:

> **Spearman 秩相关** 衡量单调关联：

```
1. Replace each value with its rank (1, 2, 3, ...)
2. Compute Pearson correlation on the ranks

Spearman catches any monotonic relationship, not just linear.
If y = x^3, Pearson gives r < 1 but Spearman gives rho = 1.
```

**When to use each:**

> **何时使用哪个：**

```
Pearson:    Both variables are continuous and roughly normal.
            You care about the linear relationship specifically.
            No extreme outliers.

Spearman:   Ordinal data (rankings, ratings).
            Data is not normally distributed.
            You suspect a monotonic but not linear relationship.
            Outliers are present.
```

**The golden rule:** correlation does not imply causation. Ice cream sales and drowning deaths are correlated because both increase in summer. Your model's accuracy and the number of parameters are correlated, but adding parameters does not automatically improve accuracy (see: overfitting).

> **黄金法则：** 相关不意味着因果。冰淇淋销量和溺水死亡是相关的，因为两者都在夏天增加。你的模型精度和参数数量是相关的，但增加参数并不自动提高精度（参见：过拟合）。

### Covariance Matrix | 协方差矩阵

The covariance between two variables measures how they vary together:

> 两个变量之间的协方差衡量它们如何一起变化：

```
Cov(X, Y) = (1/n) * sum((x_i - x_bar)(y_i - y_bar))

Cov(X, Y) > 0:  X and Y tend to increase together
Cov(X, Y) < 0:  when X increases, Y tends to decrease
Cov(X, Y) = 0:  no linear co-movement
```

For d features, the covariance matrix C is a d x d matrix where C[i][j] = Cov(feature_i, feature_j). The diagonal entries C[i][i] are the variances of each feature.

> 对于 d 个特征，协方差矩阵 C 是一个 d x d 矩阵，其中 C[i][j] = Cov(feature_i, feature_j)。对角线元素 C[i][i] 是每个特征的方差。

```
C = | Var(x1)      Cov(x1,x2)  Cov(x1,x3) |
    | Cov(x2,x1)  Var(x2)      Cov(x2,x3) |
    | Cov(x3,x1)  Cov(x3,x2)  Var(x3)     |

Properties:
  - Symmetric: C[i][j] = C[j][i]
  - Positive semi-definite: all eigenvalues >= 0
  - Diagonal = variances
  - Off-diagonal = covariances
```

**Connection to PCA.** PCA eigendecomposes the covariance matrix. The eigenvectors are the principal components (directions of maximum variance). The eigenvalues tell you how much variance each component captures. This is exactly what Lesson 10 covered, but now you see why the covariance matrix is the right thing to decompose: it encodes all pairwise linear relationships in your data.

> **与 PCA 的联系。** PCA 对协方差矩阵做特征分解。特征向量就是主成分（最大方差方向）。特征值告诉你每个成分捕获了多少方差。这正是第 10 课讲过的内容，但现在你明白了为什么协方差矩阵是正确的分解对象：它编码了数据中所有成对的线性关系。

**Connection to correlation.** The correlation matrix is the covariance matrix of standardized variables (each divided by its standard deviation). Correlation normalizes covariance so all values fall in [-1, 1].

> **与相关性的联系。** 相关矩阵是标准化变量（每个除以其标准差）的协方差矩阵。相关性将协方差归一化，使所有值落在 [-1, 1]。

### Hypothesis Testing | 假设检验

Hypothesis testing is a framework for making decisions under uncertainty. You start with a claim, collect data, and determine if the data is consistent with the claim.

> 假设检验是在不确定性下做决策的框架。你从一个主张开始，收集数据，然后判断数据是否与主张一致。

**The setup:**

> **基本设置：**

```
Null hypothesis (H0):        the default assumption, usually "no effect"
Alternative hypothesis (H1): what you are trying to show

Example:
  H0: Model A and Model B have the same accuracy
  H1: Model B has higher accuracy than Model A
```

**The p-value** is the probability of seeing data as extreme as what you observed, assuming H0 is true. It is NOT the probability that H0 is true. This is the single most common misunderstanding in statistics.

> **p 值** 是在 H0 为真的假设下，观察到与所观测数据同样极端或更极端数据的概率。它不是 H0 为真的概率。这是统计学中最常见的误解。

```
p-value = P(data this extreme | H0 is true)

If p-value < alpha (typically 0.05):
    Reject H0. The result is "statistically significant."
If p-value >= alpha:
    Fail to reject H0. You do not have enough evidence.
    This does NOT mean H0 is true.
```

**Confidence intervals** give a range of plausible values for a parameter:

> **置信区间** 给出参数的一个合理值范围：

```
95% confidence interval for the mean:
    x_bar +/- z * (s / sqrt(n))

where z = 1.96 for 95% confidence

Interpretation: if you repeated this experiment many times, 95% of the
computed intervals would contain the true mean. It does NOT mean there
is a 95% probability the true mean is in this specific interval.
```

The width of the confidence interval tells you about precision. Wide intervals mean high uncertainty. Narrow intervals mean your estimate is precise (but not necessarily accurate, if your data is biased).

> 置信区间的宽度告诉你精度。宽区间意味着高不确定性。窄区间意味着你的估计是精确的（但如果数据有偏，不一定准确）。

### The t-test | t 检验

The t-test compares means. There are several flavors.

> t 检验比较均值。有几种变体。

**One-sample t-test:** is the population mean different from a hypothesized value?

> **单样本 t 检验：** 总体均值是否与假设值不同？

```
t = (x_bar - mu_0) / (s / sqrt(n))

degrees of freedom = n - 1
```

**Two-sample t-test (independent):** are two group means different?

> **两样本 t 检验（独立）：** 两个组的均值是否不同？

```
t = (x_bar_1 - x_bar_2) / sqrt(s1^2/n1 + s2^2/n2)

This is Welch's t-test, which does not assume equal variances.
Always use Welch's unless you have a specific reason for equal variances.
```

**Paired t-test:** when measurements come in pairs (same model evaluated on same data splits):

> **配对 t 检验：** 当测量是成对的（同一模型在同一数据划分上评估）：

```
Compute d_i = x_i - y_i for each pair
Then run a one-sample t-test on the d_i values against mu_0 = 0
```

In ML, the paired t-test is common: you run both models on the same 10 cross-validation folds and compare their scores pairwise.

> 在 ML 中，配对 t 检验很常见：你在相同的 10 个交叉验证折上运行两个模型，然后成对比较它们的分数。

### Chi-squared Test | 卡方检验

The chi-squared test checks if observed frequencies match expected frequencies. Useful for categorical data.

> 卡方检验检查观测频率是否匹配期望频率。适用于分类数据。

```
chi^2 = sum((observed - expected)^2 / expected)

Example: does a language model's output distribution match the
training distribution across categories?

Category    Observed   Expected
Positive       120        100
Negative        80        100
chi^2 = (120-100)^2/100 + (80-100)^2/100 = 4 + 4 = 8

With 1 degree of freedom, chi^2 = 8 gives p < 0.005.
The difference is significant.
```

### A/B Testing for ML Models | ML 模型的 A/B 测试

A/B testing in ML is not the same as web A/B testing. Model comparison has specific challenges:

> ML 中的 A/B 测试与网页 A/B 测试不同。模型比较有特定的挑战：

```
1. Same test set:    Both models must be evaluated on identical data.
                     Different test sets make comparison meaningless.

2. Multiple metrics: Accuracy alone is not enough. You need precision,
                     recall, F1, latency, and fairness metrics.

3. Variance:         Use cross-validation or bootstrap to estimate
                     the variance of each metric, not just point estimates.

4. Data leakage:     If the test set was used during model selection,
                     your comparison is biased. Hold out a final test set.
```

**The procedure:**

> **操作步骤：**

```
1. Define your metric and significance level (alpha = 0.05)
2. Run both models on the same k-fold cross-validation splits
3. Collect paired scores: [(a1, b1), (a2, b2), ..., (ak, bk)]
4. Compute differences: d_i = b_i - a_i
5. Run a paired t-test on the differences
6. Check: is the mean difference significantly different from 0?
7. Compute a confidence interval for the mean difference
8. Compute effect size (Cohen's d) to judge practical significance
```

### Statistical Significance vs Practical Significance | 统计显著性 vs 实际显著性

A result can be statistically significant but practically meaningless. With enough data, even a trivial difference becomes statistically significant.

> 一个结果可能在统计上显著但在实际中毫无意义。数据足够多时，即使是微不足道的差异也会变得统计显著。

```
Example:
  Model A accuracy: 0.9234
  Model B accuracy: 0.9237
  n = 1,000,000 test samples
  p-value = 0.001

Statistically significant? Yes.
Practically significant? A 0.03% improvement is not worth the
engineering cost of deploying a new model.
```

**Effect size** quantifies how big the difference is, independent of sample size:

> **效应量** 量化差异有多大，与样本量无关：

```
Cohen's d = (mean_1 - mean_2) / pooled_std

d = 0.2:  small effect
d = 0.5:  medium effect
d = 0.8:  large effect
```

Always report both the p-value and the effect size. The p-value tells you if the difference is real. The effect size tells you if it matters.

> 始终同时报告 p 值和效应量。p 值告诉你差异是否真实。效应量告诉你差异是否有意义。

### Multiple Comparison Problem | 多重比较问题

When you test many hypotheses, some will be "significant" by chance. If you test 20 things at alpha = 0.05, you expect 1 false positive even when nothing is real.

> 当你检验许多假设时，有些会偶然"显著"。如果你在 alpha = 0.05 下检验 20 个东西，即使没有真实效应，你也预期有 1 个假阳性。

```
P(at least one false positive) = 1 - (1 - alpha)^m

m = 20 tests, alpha = 0.05:
P(false positive) = 1 - 0.95^20 = 0.64

You have a 64% chance of at least one false positive.
```

**Bonferroni correction:** divide alpha by the number of tests.

> **Bonferroni 校正：** 将 alpha 除以检验次数。

```
Adjusted alpha = alpha / m = 0.05 / 20 = 0.0025

Only reject H0 if p-value < 0.0025.
Conservative but simple. Works when tests are independent.
```

In ML, this matters when you compare a model across multiple metrics, test many hyperparameter configurations, or evaluate on multiple datasets.

> 在 ML 中，当你在多个指标上比较模型、测试多个超参数配置或在多个数据集上评估时，这很重要。

### Bootstrap Methods | Bootstrap 方法

Bootstrapping estimates the sampling distribution of a statistic by resampling your data with replacement. No assumptions about the underlying distribution required.

> Bootstrap 通过有放回地重采样数据来估计统计量的抽样分布。不需要对底层分布做任何假设。

**The algorithm:**

> **算法：**

```
1. You have n data points
2. Draw n samples WITH replacement (some points appear multiple times,
   some not at all)
3. Compute your statistic on this bootstrap sample
4. Repeat B times (typically B = 1000 to 10000)
5. The distribution of bootstrap statistics approximates the
   sampling distribution
```

**Bootstrap confidence interval (percentile method):**

> **Bootstrap 置信区间（百分位数法）：**

```
Sort the B bootstrap statistics
95% CI = [2.5th percentile, 97.5th percentile]
```

**Why bootstrap matters for ML:**

> **Bootstrap 对 ML 为什么重要：**

```
- Test set accuracy is a point estimate. Bootstrap gives you
  confidence intervals.
- You cannot assume metric distributions are normal (especially
  for AUC, F1, precision at k).
- Bootstrap works for ANY statistic: median, ratio of two means,
  difference in AUC between two models.
- No closed-form formula needed.
```

**Bootstrap for model comparison:**

> **Bootstrap 用于模型比较：**

```
1. You have predictions from Model A and Model B on the same test set
2. For each bootstrap iteration:
   a. Resample test indices with replacement
   b. Compute metric_A and metric_B on the resampled set
   c. Store diff = metric_B - metric_A
3. 95% CI for the difference:
   [2.5th percentile of diffs, 97.5th percentile of diffs]
4. If the CI does not contain 0, the difference is significant
```

This is more robust than the paired t-test because it makes no distributional assumptions.

> 这比配对 t 检验更稳健，因为它不做分布假设。

### Parametric vs Non-parametric Tests | 参数检验 vs 非参数检验

**Parametric tests** assume a specific distribution (usually normal):

> **参数检验** 假设特定的分布（通常是正态分布）：

```
t-test:         assumes normally distributed data (or large n by CLT)
ANOVA:          assumes normality and equal variances
Pearson r:      assumes bivariate normality
```

**Non-parametric tests** make no distributional assumptions:

> **非参数检验** 不做分布假设：

```
Mann-Whitney U:     compares two groups (replaces independent t-test)
Wilcoxon signed-rank: compares paired data (replaces paired t-test)
Spearman rho:       correlation on ranks (replaces Pearson)
Kruskal-Wallis:     compares multiple groups (replaces ANOVA)
```

**When to use non-parametric:**

> **何时使用非参数检验：**

```
- Small sample size (n < 30) and data is clearly non-normal
- Ordinal data (ratings, rankings)
- Heavy outliers you cannot remove
- Skewed distributions
```

**When to use parametric:**

> **何时使用参数检验：**

```
- Large sample size (CLT makes the test statistic approximately normal)
- Data is roughly symmetric without extreme outliers
- More statistical power (better at detecting real differences)
```

In ML experiments, you typically have small n (5 or 10 cross-validation folds), so non-parametric tests like Wilcoxon signed-rank are often more appropriate than t-tests.

> 在 ML 实验中，你通常有小的 n（5 或 10 个交叉验证折），所以像 Wilcoxon 符号秩这样的非参数检验通常比 t 检验更合适。

### Central Limit Theorem: Practical Implications | 中心极限定理：实际意义

The CLT says the distribution of sample means approaches a normal distribution as n grows, regardless of the underlying population distribution.

> CLT 说的是，随着 n 增长，样本均值的分布趋近于正态分布，无论底层总体分布如何。

```
If X_1, X_2, ..., X_n are iid with mean mu and variance sigma^2:

    X_bar ~ Normal(mu, sigma^2 / n)    as n -> infinity

Works for n >= 30 in most cases.
For highly skewed distributions, you might need n >= 100.
```

**Why this matters for ML:**

> **这对 ML 为什么重要：**

```
1. Justifies confidence intervals and t-tests on aggregated metrics
2. Explains why averaging over cross-validation folds gives stable
   estimates even when individual folds vary wildly
3. Mini-batch gradient descent works because the average gradient
   over a batch approximates the true gradient (CLT in action)
4. Ensemble methods: averaging predictions from many models gives
   more stable output than any single model
```

**What CLT does NOT do:**

> **CLT 不能做什么：**

```
- Does NOT make your data normal. It makes the MEAN of samples normal.
- Does NOT work for heavy-tailed distributions with infinite variance
  (Cauchy distribution).
- Does NOT apply to dependent data (time series without correction).
```

### Common Statistical Mistakes in ML Papers | ML 论文中常见的统计错误

1. **Testing on the training set.** Guarantees overfitting. Always hold out data the model never sees during training.

> 1. **在训练集上测试。** 保证过拟合。始终保留模型训练时从未见过的数据。

2. **No confidence intervals.** Reporting a single accuracy number without uncertainty makes results unreproducible and unverifiable.

> 2. **没有置信区间。** 报告单个精度数字而没有不确定性度量，使结果不可复现且不可验证。

3. **Ignoring multiple comparisons.** Testing 50 configurations and reporting the best one without correction inflates false positive rates.

> 3. **忽略多重比较。** 测试 50 个配置并报告最好的一个而不做校正，会膨胀假阳性率。

4. **Confusing statistical and practical significance.** A p-value of 0.001 on a 0.01% accuracy improvement is not meaningful.

> 4. **混淆统计显著性和实际显著性。** 0.01% 精度提升上的 p 值 0.001 没有意义。

5. **Using accuracy on imbalanced data.** 99% accuracy on a dataset with 99% negative class means the model learned nothing. Use precision, recall, F1, or AUC.

> 5. **在不平衡数据上使用精度。** 在 99% 负类的数据集上 99% 的精度意味着模型什么都没学到。使用精确率、召回率、F1 或 AUC。

6. **Cherry-picking metrics.** Reporting only the metric where your model wins. Honest evaluation reports all relevant metrics.

> 6. **挑选指标。** 只报告你的模型赢的指标。诚实的评估报告所有相关指标。

7. **Leaking information across train/test splits.** Normalizing before splitting, or using future data to predict the past.

> 7. **在训练/测试划分之间泄露信息。** 在划分前做归一化，或用未来数据预测过去。

8. **Small test sets with no variance estimates.** Evaluating on 100 samples and claiming 2% improvement is noise, not signal.

> 8. **小测试集没有方差估计。** 在 100 个样本上评估并声称 2% 的提升是噪声，不是信号。

9. **Assuming independence when data is not independent.** Medical images from the same patient, multiple sentences from the same document. Observations within a group are correlated.

> 9. **数据不独立时假设独立。** 来自同一患者的医学图像、来自同一文档的多个句子。组内观测是相关的。

10. **P-hacking.** Trying different tests, subsets, or exclusion criteria until you get p < 0.05. The result is an artifact of the search.

> 10. **P 值操纵（P-hacking）。** 尝试不同的检验、子集或排除标准，直到得到 p < 0.05。结果是搜索过程的伪影。

## Building It | 动手实现

You will implement:

> 你将实现：

1. **Descriptive statistics from scratch** (mean, median, mode, standard deviation, percentiles, IQR)
   **从零实现描述性统计**（均值、中位数、众数、标准差、百分位数、IQR）
2. **Correlation functions** (Pearson and Spearman, with the covariance matrix)
   **相关函数**（Pearson 和 Spearman，以及协方差矩阵）
3. **Hypothesis tests** (one-sample t-test, two-sample t-test, chi-squared test)
   **假设检验**（单样本 t 检验、两样本 t 检验、卡方检验）
4. **Bootstrap confidence intervals** (for any statistic, no assumptions needed)
   **Bootstrap 置信区间**（任意统计量，无需假设）
5. **A/B test simulator** (generate data, test, check for Type I and Type II errors)
   **A/B 测试模拟器**（生成数据、测试、检查第一类和第二类错误）
6. **Statistical vs practical significance demo** (showing that large n makes everything "significant")
   **统计 vs 实际显著性演示**（展示大 n 使一切都"显著"）

All from scratch, using only `math` and `random`. No numpy, no scipy.

> 全部从零实现，仅使用 `math` 和 `random`。不使用 numpy、scipy。

## Key Terms | 术语速查表

| Term / 术语 | Definition / 定义 |
|---|---|
| Mean / 均值 | Sum of values divided by count. Sensitive to outliers. / 值的总和除以个数。对异常值敏感。 |
| Median / 中位数 | Middle value of sorted data. Robust to outliers. / 排序后数据的中间值。对异常值稳健。 |
| Standard deviation / 标准差 | Square root of variance. Measures spread in original units. / 方差的平方根。用原始单位衡量离散程度。 |
| Percentile / 百分位数 | Value below which a given percentage of data falls. / 给定百分比的数据低于此值。 |
| IQR / 四分位距 | Interquartile range. Q3 minus Q1. The spread of the middle 50%. / 四分位距。Q3 减 Q1。中间 50% 的展幅。 |
| Pearson correlation / Pearson 相关系数 | Measures linear association between two variables. Range [-1, 1]. / 衡量两个变量间的线性关联。范围 [-1, 1]。 |
| Spearman correlation / Spearman 相关系数 | Measures monotonic association using ranks. / 用排名衡量单调关联。 |
| Covariance matrix / 协方差矩阵 | Matrix of pairwise covariances between all features. / 所有特征间成对协方差的矩阵。 |
| Null hypothesis / 零假设 | Default assumption of no effect or no difference. / 无效应或无差异的默认假设。 |
| p-value / p 值 | Probability of data this extreme given the null hypothesis is true. / 在零假设为真的条件下观察到如此极端数据的概率。 |
| Confidence interval / 置信区间 | Range of plausible values for a parameter at a given confidence level. / 给定置信水平下参数的合理值范围。 |
| t-test / t 检验 | Tests whether means differ significantly. Uses the t-distribution. / 检验均值是否有显著差异。使用 t 分布。 |
| Chi-squared test / 卡方检验 | Tests whether observed frequencies differ from expected frequencies. / 检验观测频率是否与期望频率不同。 |
| Effect size / 效应量 | Magnitude of a difference, independent of sample size. Cohen's d is common. / 差异的大小，与样本量无关。常用 Cohen's d。 |
| Bonferroni correction / Bonferroni 校正 | Divides significance threshold by number of tests to control false positives. / 将显著性阈值除以检验次数以控制假阳性。 |
| Bootstrap / Bootstrap | Resampling with replacement to estimate sampling distributions. / 有放回重采样以估计抽样分布。 |
| Type I error / 第一类错误 | False positive. Rejecting H0 when it is true. / 假阳性。H0 为真时拒绝 H0。 |
| Type II error / 第二类错误 | False negative. Failing to reject H0 when it is false. / 假阴性。H0 为假时未能拒绝 H0。 |
| Statistical power / 统计功效 | Probability of correctly rejecting a false H0. Power = 1 minus Type II error rate. / 正确拒绝假 H0 的概率。功效 = 1 减第二类错误率。 |
| Central limit theorem / 中心极限定理 | Sample means converge to a normal distribution as sample size grows. / 样本均值随样本量增大趋近于正态分布。 |
| Parametric test / 参数检验 | Assumes a specific distribution for the data (usually normal). / 假设数据服从特定分布（通常是正态分布）。 |
| Non-parametric test / 非参数检验 | Makes no distributional assumptions. Works on ranks or signs. / 不做分布假设。基于排名或符号工作。 |
