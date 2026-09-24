# 机器学习统计学

> 统计是如何知道你的模型是否真的有效,或者只是幸运.
> 统计学告诉你模型是真的有效还是只是运气好.

**Type:** Build | **类型:** 动手
**Language:**子**语言:**字符串
**Prerequisites:** Phase 1, Lessons 06 (Probability and Distributions), 07 (Bayes' Theorem) | **前置知识:** Phase 1, 第 06 课（概率与分布）、第 07 课（贝叶斯定理）
**Time:** ~120 minutes | **时间:** ~120 分钟

## 学习目标

- 计算描述性统计,皮尔森/斯皮尔曼相关性和零的共变矩阵
  从零计算描述性统计量、皮尔森/斯皮尔曼 相关系数和协方差矩阵

- 执行假设测试 (t测试,chi-平方) 并正确解释p值和信任间隔
  执行假设检验(t 检验、卡方检验),正确解释 p 值和置信区间

- 使用bootstrap重样构建任何测量值的信任间隔,而没有分布假设
  使用Bootstrap重采样为任意标标构建置信区间,无需分布假设

- 使用效果尺寸测量来区分统计意义与实用意义
  效果量区别统计显著性与实际显著性

> **【中文解读】**
> 统计学告诉你模型是真的有效还是运气好――A/B 测试评估新模型、Bootstrap 构建置信区间、假设检查判断差异显著性 这些是ML 实验评估的基础――

## 问题 问题引入

> **【中文解读】**模型 A 准确率 0.87,模型 B 准确率 0.89,你部署了 B ∙ 三周后线效果反而变化因为 0.02 的差异是噪音不是真实升级 统计学回答:差异是显著吗?置信区间多宽?样本量不够?没有统计学 ML 实验 = 盲人摸象──

## 概念的核心概念

> **【拓展：AI 工程中的统计学实战】**(1) 其他**A/B 测试**推/搜索模型上线前必须做,统计显著(p<0.05) 才发布;(2) **Bootstrap 置信区间**没有假设数据分布,重采样构建任意指标的置信区间;**效应量**结果量告诉你差异有多大 统计显著 ≠实际有用;**多重比较校正**调整了20个超参数取最好的,必须校正否则是"多碰运气"

随时发生这种情况. 曲排名表的调整. 文件无法复制. A/B 测试,根据几百个样本宣布获胜者. 根本原因总是相同的:有人跳过了统计数据.

> 这种情况经常发生. 乱 排名大洗牌. 不复制论文. 基于几百个样本的宣布获胜者 A/B 测试.

统计数据给你提供了区分信号和噪音的工具. 它告诉你什么时候差异是真实的,你应该有多自信,以及你需要多少数据才能相信结果. 每个ML管道,每一个模型比较,每一个实验都需要统计.没有它,你猜测.

> 统计学为你提供了区分信号和噪音的工具――它告诉你什么时候差异是真实的,你应该有多大的信心,以及你需要多少数据才能相信一个结果――每个 ML 管道,每个模型比较,每个实验都需要统计学――没有它,你只是在猜测――

## 概念的核心概念

### 描述统计:汇总你的数据

在你做任何模型之前,你需要知道你的数据是什么样子.描述性统计数据集将数据集压缩成几个数字,

> 在建立任何模型之前,你需要了解数据的样式.

**Measures of central tendency**答案是"中间在哪里?"

> **集中趋势度量**回答"中间在哪里?"

```
Mean:   sum of all values / count
        mu = (1/n) * sum(x_i)

Median: middle value when sorted
        Robust to outliers. If you have [1, 2, 3, 4, 1000], the mean is 202
        but the median is 3.

Mode:   most frequent value
        Useful for categorical data. For continuous data, rarely informative.
```

平均值是平衡点.中位数是半途线.当它们分离时,你的分布是偏差的.收入分布有平均值 >>中位数 (从亿万富翁中右偏差).训练期间的损失分布通常有平均值 <<中位数 (从轻松样本中左偏差).

> 平均值是平衡点――中位数是中位标志――当它们偏离时,你的分布是偏斜的――收入分布的平均值远大于中位数――亿万富翁造成的右偏)――训练期间的损失分布通常平均值远小于中位数――简单样本造成的左偏)――

**Measures of spread**答案是"数据分布多大?"

> **离散程度度量**回答"数据可能散发吗?"

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

**Percentiles**分类数据成100个等部分.25个百分点 (Q1) 表示25%的值落在这个点以下.50个百分点是中位数.75个百分点是Q3.

> **百分位数**将排序后的数据分成100等位数. 第25百分位数. Q1意味着25%的值低于此点. 第50百分位数是中位数. 第75百分位数是 Q3──

```
For latency monitoring:
  P50 = median latency        (typical user experience)
  P95 = 95th percentile       (bad but not worst case)
  P99 = 99th percentile       (tail latency, often 10x the median)
```

在ML中,你关心推断延迟,预测信心分布和理解错误分布的百分比.一个平均错误低但可怕的P99错误的模型可能对安全关键应用来说是无用的.

> 在ML中,你关注推理延迟,预测和误差分布的百分比.

**Sample vs population statistics.**计算一个样本的差异时,除以 (n-1) 而不是 (n-1).这是贝塞尔的纠正.它弥补了样本的平均值不是真正的人口平均值的事实.在命名器中,你系统地低估了真正的差异.在 (n-1) 时,估计是无偏见的.

> **样本统计 vs 总体统计。**从样本计算方差时,除以 (n-1) 而不是n──这是贝塞尔校正 (Bessel的修正)──它补偿了样本平均值不是真实总体平均值这一事实──分母用n 会系统性低估真实方差──用 (n-1),估计是无偏的──

```
Population variance: sigma^2 = (1/N) * sum((x_i - mu)^2)
Sample variance:     s^2     = (1/(n-1)) * sum((x_i - x_bar)^2)
```

实际上:如果n是大 (成千上万个样本),差异是微不足道的.如果n是小 (成千上万个样本),它很重要.

> 实践中:如果n 很大 ((数千个样本),差异可以忽略.

### 相关性:变量如何一起变化

相关性衡量两个变量之间的线性关系的强度和方向.

> 相关性衡量两种变量之间的线性关系强度和方向.

**Pearson correlation coefficient**措施是线性协同:

> **Pearson 相关系数**衡量线性关联:

```
r = sum((x_i - x_bar)(y_i - y_bar)) / (n * s_x * s_y)

r = +1:  perfect positive linear relationship
r = -1:  perfect negative linear relationship
r =  0:  no linear relationship (but there might be a nonlinear one!)

Range: [-1, 1]
```

皮尔森假设这种关系是线性,两个变量都大致正常分布.它对异常值敏感.一个极端点可以从0.1拖到0.9拉 r.

> 皮尔森假设关系是线性的,且两个变量大致服从正态分布.

**Spearman rank correlation**措施单调的联系:

> **Spearman 秩相关**衡量单调关联:

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

**The golden rule:**相关性并不意味着因果关系.冰淋销售和溺水死亡都相关,因为夏季都会增加. 模型的准确性和参数数数量都相关,但添加参数不会自动提高准确性 (见:过度配件).

> **黄金法则：**相关不意味着因果.冰销量和溺水死亡都相关,因为它们都在夏季增加.

### 变量矩阵

两个变量之间的共变量衡量它们如何与 nhau变化:

> 两个变量之间的协同差距衡量它们如何变化:

```
Cov(X, Y) = (1/n) * sum((x_i - x_bar)(y_i - y_bar))

Cov(X, Y) > 0:  X and Y tend to increase together
Cov(X, Y) < 0:  when X increases, Y tends to decrease
Cov(X, Y) = 0:  no linear co-movement
```

对于d特征,共变矩阵C是一个d x d矩阵,其中C[i][j] =Cov(feature_i, feature_j).对角值输入C[i][i]是每个特征的变化.

> 对于d 个特征,协方差矩阵C 是一个d x d矩阵,其中C[i][j] =Cov(特征_i,特征_j) ――对角线元素C[i][i] 是每个特征的方差──

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

**Connection to PCA.**实际上,在一个对比数组中,一个对比数组的位置是个对比数组. PCA 自身构成了共变矩阵.自向量是主要的组件 (最大变异的方向).自值值告诉你每个组件捕获多少变异.这正是10课程所涵盖的,但现在你看到了为什么共变矩阵是分解的正确东西:它编码了你数据中的所有对对线关系.

> **与 PCA 的联系。**PCA对方差矩阵做了特征分解――特征向量就是主成分――最大方差方向――特征值告诉你每个成分捕获了多少方差――这正是第十课中所讲的内容,但现在你明白了为什么方差矩阵是正确的分解对象:它编码了数据中的所有对方线性关系――

**Connection to correlation.**相关性矩阵是标准化变量 (每个变量以其标准偏差分为) 的共变矩阵.相对性正常化共变,因此所有值都在 [-1, 1] 中下降.

> **与相关性的联系。**相关矩阵是标准化变量 (),每个除其标准差) 的协方差矩阵.

### 假设测试

假设测试是在不确定性下做出决定的框架.

> 假设检查是在不确定性下做出决策的框架.

**The setup:**

> **基本设置：**

```
Null hypothesis (H0):        the default assumption, usually "no effect"
Alternative hypothesis (H1): what you are trying to show

Example:
  H0: Model A and Model B have the same accuracy
  H1: Model B has higher accuracy than Model A
```

**The p-value**假设H0是真的,这是一个最常见的误解.

> **p 值**在H0为真假设下,观察到与观测数据相同的极端或更极端数据的概率.

```
p-value = P(data this extreme | H0 is true)

If p-value < alpha (typically 0.05):
    Reject H0. The result is "statistically significant."
If p-value >= alpha:
    Fail to reject H0. You do not have enough evidence.
    This does NOT mean H0 is true.
```

**Confidence intervals**给一个参数一个可行的值范围:

> **置信区间**给出参数的一个合理值范围:

```
95% confidence interval for the mean:
    x_bar +/- z * (s / sqrt(n))

where z = 1.96 for 95% confidence

Interpretation: if you repeated this experiment many times, 95% of the
computed intervals would contain the true mean. It does NOT mean there
is a 95% probability the true mean is in this specific interval.
```

宽度的保证间隔告诉你准确性.宽度的间隔意味着高的不确定性.狭的间隔意味着你的估计是准确的 (但不一定是准确的,如果你的数据偏见).

> 置信区间的宽度告诉你精度.宽区间意味着高不确定性.狭区间意味着你的估计是精确的.

### 测试的时间

测试比较了各种味道.

> 检查比较平均值──有几种变化──

**One-sample t-test:**人口平均值与假设值不同吗?

> **单样本 t 检验：**总体平均值与假设值是否不同?

```
t = (x_bar - mu_0) / (s / sqrt(n))

degrees of freedom = n - 1
```

**Two-sample t-test (independent):**两个群体的意思是不同的吗?

> **两样本 t 检验（独立）：**两个组的平均值是否不同?

```
t = (x_bar_1 - x_bar_2) / sqrt(s1^2/n1 + s2^2/n2)

This is Welch's t-test, which does not assume equal variances.
Always use Welch's unless you have a specific reason for equal variances.
```

**Paired t-test:**测量对 (相同模型在相同的数据分区上进行评估):

> **配对 t 检验：**当测量是对的 (同样的模型在同样的数据分类上评估):

```
Compute d_i = x_i - y_i for each pair
Then run a one-sample t-test on the d_i values against mu_0 = 0
```

在ML中,对 t 测试是常见的:你运行两个模型在相同的10个验证折叠上,并对比它们的分数.

> 在ML中,配对t检验很常见:你在同一的10个交叉验证折上运行两个模型,然后对比它们的分数.

### 二面测试

检查观察频率是否与预期频率相匹配.

> 卡方检查检查观测频率是否匹配期望频率――适用于分类数据――

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

### 对于ML模型进行A/B测试

在ML中A/B测试与网络A/B测试不同.模型比较具有具体的挑战:

> 模型比较有特定的挑战:

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

### 统计显著性与实际显著性

结果可能是统计上显著的,但实际上是无意义的.

> 一个结果可能在统计上显著,但实际上是无意义的.

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

**Effect size**量化了不同程度,不论样本大小如何:

> **效应量**量化差异有多,与样本量无关:

```
Cohen's d = (mean_1 - mean_2) / pooled_std

d = 0.2:  small effect
d = 0.5:  medium effect
d = 0.8:  large effect
```

总是报告p值和效果大小.p值告诉你是否有真正的差异.效果大小告诉你是否重要.

> 始终同时报告p值和效应量──p值告诉你差异是否真实──效应量告诉你差异是否有意义──

### 许多比较问题

如果在alpha=0.05时测试20个东西,你会预期1个假阳性,即使没有什么是真实的.

> 如果你在alpha=0.05下检查20个东西,即使没有真实效果,你也预期有一个假阳性.

```
P(at least one false positive) = 1 - (1 - alpha)^m

m = 20 tests, alpha = 0.05:
P(false positive) = 1 - 0.95^20 = 0.64

You have a 64% chance of at least one false positive.
```

**Bonferroni correction:**分别对试验数量的阿尔法.

> **Bonferroni 校正：**检查次数除了将阿尔法.

```
Adjusted alpha = alpha / m = 0.05 / 20 = 0.0025

Only reject H0 if p-value < 0.0025.
Conservative but simple. Works when tests are independent.
```

在ML中,当你比较一个模型在多个指标中,测试许多超参数配置,或在多个数据集上评估时,这很重要.

> 在 ML 中,当你在多个指标上比较模型,测试多个超参数配置或在多个数据集上评估时,这是很重要的.

### 启动方法

引导测试通过替换数据来估计统计数据的样本分布.

> 通过有放回重采采集数据来估计统计量抽样分布.

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

这比对 t 测试更强大,因为它没有分布假设.

> 这比配对t检查更稳定,因为它不做分布假设.

### 参数检查与非参数检查

**Parametric tests**假设一个特定的分布 (通常是正常的):

> **参数检验**假设特定分布通常是正态分布):

```
t-test:         assumes normally distributed data (or large n by CLT)
ANOVA:          assumes normality and equal variances
Pearson r:      assumes bivariate normality
```

**Non-parametric tests**没有进行分布假设:

> **非参数检验**不做分布假设:

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

在ML实验中,通常有小的 n (5或10个跨验证折叠),因此像威尔科森签名等级的非参数测试通常比t测试更合适.

> 在ML实验中,你通常有小的n(5或10个交叉验证折),所以像威尔科森符号一样,这种非参数检查通常比t检查更合适.

### 实际意义: 实际意义: 实际意义:

根据CLT的说法,样品的分布平均接近正常分布,随着n的增长,

> 随着n 增长,样本平均值分布趋于正态分布,无论底层总体分布如何.

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

### 在ML论文中常见的统计错误

1. **Testing on the training set.**确保过度适应. 保持模型在训练中不会看到的数据.

> 1. **在训练集上测试。**确保过拟合――永远保留模型训练时从未见过的数据――

2. **No confidence intervals.**报告单个准确数号,而无可确定性,使得结果无法复制和无法验证.

> 2. **没有置信区间。**报告单个精度数字,而没有不确定性度量,使得结果不可复制和不可验证.

3. **Ignoring multiple comparisons.**测试50个配置,报告最好的配置,

> 3. **忽略多重比较。**测试50个配置并报告最好的一个不做校正,会膨胀假阳性率.

4. **Confusing statistical and practical significance.**对于0.01%的精度提高,一个0.001的p值是没有意义的.

> 4. **混淆统计显著性和实际显著性。**精度提升的p值 0.001 没有意义.

5. **Using accuracy on imbalanced data.**模型没有学到任何东西.使用精度,回忆,F1,或AUC.

> 5. **在不平衡数据上使用精度。**在99%负类数据集中,99%的精度意味着模型没有学到任何东西.

6. **Cherry-picking metrics.**诚实评估报告所有相关的指标.

> 6. **挑选指标。**仅报告你的模型的获胜指标.

7. **Leaking information across train/test splits.**在分开之前,将其正常化,或者使用未来数据来预测过去.

> 7. **在训练/测试划分之间泄露信息。**在分分前做归结,或用未来数据预测过去.

8. **Small test sets with no variance estimates.**通过100个样本进行评估,并声称2%的改善是噪音,而不是信号.

> 8. **小测试集没有方差估计。**在100个样本上评估并声称2%的提升是噪音,而不是信号.

9. **Assuming independence when data is not independent.**医疗图像来自同一患者,同一文件的多句话.

> 9. **数据不独立时假设独立。**医疗图像来自同一档案的多句话.

10. **P-hacking.**在试验中,我们可以尝试不同的测试,子集或排除标准,直到我们得到p <0.05.

> 10. **P 值操纵（P-hacking）。**尝试不同的检查,集或排除标准,直到得到p <0.05──结果是搜索过程的伪影──

## 建立它,实现

你将实施:

> 你将实现:

1. **Descriptive statistics from scratch**(平均,中位数,模式,标准偏差,百分点,IQR)
   **从零实现描述性统计**平均值,中位数,众数,标准差,百分位数,IQR)
2. **Correlation functions**(皮尔森和斯皮尔曼,与共变矩阵)
   **相关函数**(皮尔森和斯皮尔曼以及协方差矩阵)
3. **Hypothesis tests**(一个样本的t测试,两个样本的t测试,四方的chi测试)
   **假设检验**(单样本 t检测、两样本 t检测、卡方检测)
4. **Bootstrap confidence intervals**(对于任何统计数据,不需要假设)
   **Bootstrap 置信区间**(任意统计量,无需假设)
5. **A/B test simulator**(生成数据,测试,检查I类和II类错误)
   **A/B 测试模拟器**(生成数据,测试,检查第一类和第二类错误)
6. **Statistical vs practical significance demo**(显示大 n 让一切变得"重要")
   **统计 vs 实际显著性演示**(展示大 n 使一切都"显著")

只有使用`math`其他`random`没有,没有.

> 完全从零实现,仅使用`math`和 `random`不使用,.

## 关键词 快速查找表
```figure
f3-bootstrap-resample
```

## 关键词

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
