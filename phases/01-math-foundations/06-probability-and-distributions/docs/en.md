# Probability and Distributions | 概率与分布

> Probability is the language AI uses to express uncertainty.
> 概率是 AI 表达不确定性的语言。

**Type:** Learn | **类型:** 学习
**Language:** Python | **语言:** Python
**Prerequisites:** Phase 1, Lessons 01-04 | **前置知识:** Phase 1, Lessons 01-04
**Time:** ~75 minutes | **时间:** ~75 分钟

## Learning Objectives | 学习目标

- Implement PMFs and PDFs from scratch for Bernoulli, categorical, Poisson, uniform, and normal distributions
- Compute expected value, variance, and use the Central Limit Theorem to explain why Gaussians dominate
- Build softmax and log-softmax functions with the numerical stability trick (subtract max logit)
- Calculate cross-entropy loss from logits and connect it to negative log-likelihood

> **【中文解读】**
> 概率是 AI 表达不确定性的语言。分类器输出概率分布，语言模型从 5 万个候选词中按概率采样，扩散模型从学习到的分布中生成图像。本章从零实现常见的概率分布、Softmax 函数和交叉熵损失。

> **【拓展：概率在 AI 中的位置】**
> - **Softmax**: 将神经网络输出转换为概率分布，是所有分类模型的最后一步。
> - **交叉熵损失**: 分类任务的标准损失函数，等于负对数似然。
> - **高斯分布**: 中心极限定理解释了为什么高斯分布在自然界和 AI 中如此常见。

## The Problem | 问题引入

> **【中文解读】** 分类器输出 `[0.03, 0.91, 0.06]`（91% 概率是猫），语言模型从 5 万候选词中选下一个，扩散模型从学到的分布中采样生成图片——这些都是概率论在起作用。不理解概率，就无法理解 Softmax、贝叶斯推理、VAE 和扩散模型。

## The Concept | 核心概念

> **【拓展：概率分布是 AI 生成模型的基础】** 生成模型（VAE、GAN、扩散模型）的核心都是概率分布：学到一个数据分布 p(x)，然后从中采样生成新数据。高斯分布（正态分布）是其中的核心——VAE 假设隐变量服从高斯分布，扩散模型的前向过程是逐步添加高斯噪声，反向过程是逐步去噪。中心极限定理解释了为什么高斯分布无处不在。

Every prediction a model makes is a probability distribution. Every loss function measures how far the predicted distribution is from the true one. Every training step adjusts parameters to make one distribution look more like another. Without probability, you cannot read a single ML paper, debug a single model, or understand why your training loss is NaN.

> 模型的每个预测都是一个概率分布。每个损失函数衡量预测分布与真实分布的差距。每步训练都在调整参数使一个分布更接近另一个。不理解概率，你就无法读论文、调试模型或理解为什么训练损失是 NaN。

## The Concept | 核心概念

### Events, Sample Spaces, and Probability

The sample space S is the set of all possible outcomes. An event is a subset of the sample space. Probability maps events to numbers between 0 and 1.

> 样本空间 S 是所有可能结果的集合。事件是样本空间的子集。概率将事件映射到 0 到 1 之间的数字。

```
Coin flip:
  S = {H, T}
  P(H) = 0.5,  P(T) = 0.5

Single die roll:
  S = {1, 2, 3, 4, 5, 6}
  P(even) = P({2, 4, 6}) = 3/6 = 0.5
```

Three axioms define all of probability:
1. P(A) >= 0 for any event A
2. P(S) = 1 (something always happens)
3. P(A or B) = P(A) + P(B) when A and B cannot both occur

> 概率论由三条公理定义：
> 1. 对于任意事件 A，P(A) >= 0
> 2. P(S) = 1（必然有某种结果发生）
> 3. 当 A 和 B 不能同时发生时，P(A 或 B) = P(A) + P(B)

Everything else (Bayes' theorem, expectations, distributions) follows from these three rules.

> 其他一切（贝叶斯定理、期望、分布）都由这三条规则推导出来。

### Conditional Probability and Independence

P(A|B) is the probability of A given that B happened.

> P(A|B) 是在 B 已经发生的条件下 A 发生的概率。

```
P(A|B) = P(A and B) / P(B)

Example: deck of cards
  P(King | Face card) = P(King and Face card) / P(Face card)
                      = (4/52) / (12/52)
                      = 4/12 = 1/3
```

Two events are independent when knowing one tells you nothing about the other:

> 两个事件独立是指知道其中一个不会告诉你关于另一个的任何信息：

```
Independent:   P(A|B) = P(A)
Equivalent to: P(A and B) = P(A) * P(B)
```

Coin flips are independent. Drawing cards without replacement is not.

> 抛硬币是独立的。不放回抽牌不是独立的。

### Probability Mass Functions vs Probability Density Functions

Discrete random variables have a probability mass function (PMF). Each outcome has a specific probability that you can read off directly.

> 离散随机变量有概率质量函数（PMF）。每个结果都有一个可以直接读出的具体概率。

```
PMF: P(X = k)

Fair die:
  P(X = 1) = 1/6
  P(X = 2) = 1/6
  ...
  P(X = 6) = 1/6

  Sum of all probabilities = 1
```

Continuous random variables have a probability density function (PDF). The density at a single point is not a probability. Probability comes from integrating the density over an interval.

> 连续随机变量有概率密度函数（PDF）。单个点上的密度值不是概率，概率来自对密度函数在某个区间上求积分。

```
PDF: f(x)

P(a <= X <= b) = integral of f(x) from a to b

f(x) can be greater than 1 (density, not probability)
integral from -inf to +inf of f(x) dx = 1
```

This distinction matters in ML. Classification outputs are PMFs (discrete choices). VAE latent spaces use PDFs (continuous).

> 这个区别在 ML 中很重要。分类输出是 PMF（离散选择），VAE 隐空间使用 PDF（连续）。

### Common Distributions

**Bernoulli:** one trial, two outcomes. Models binary classification.

> **伯努利分布：** 一次试验，两种结果。用于建模二分类问题。

```
P(X = 1) = p
P(X = 0) = 1 - p
Mean = p,  Variance = p(1-p)
```

**Categorical:** one trial, k outcomes. Models multi-class classification (softmax output).

> **分类分布：** 一次试验，k 种结果。用于建模多分类问题（softmax 输出）。

```
P(X = i) = p_i,  where sum of p_i = 1
Example: P(cat) = 0.7,  P(dog) = 0.2,  P(bird) = 0.1
```

**Uniform:** all outcomes equally likely. Used for random initialization.

> **均匀分布：** 所有结果等概率出现。用于随机初始化。

```
Discrete: P(X = k) = 1/n for k in {1, ..., n}
Continuous: f(x) = 1/(b-a) for x in [a, b]
```

**Normal (Gaussian):** the bell curve. Parameterized by mean (mu) and variance (sigma^2).

> **正态（高斯）分布：** 钟形曲线。由均值 (mu) 和方差 (sigma^2) 参数化。

```
f(x) = (1 / sqrt(2*pi*sigma^2)) * exp(-(x - mu)^2 / (2*sigma^2))

Standard normal: mu = 0, sigma = 1
  68% of data within 1 sigma
  95% within 2 sigma
  99.7% within 3 sigma
```

**Poisson:** counts of rare events in a fixed interval. Models event rates.

> **泊松分布：** 固定区间内稀有事件的计数。用于建模事件发生率。

```
P(X = k) = (lambda^k * e^(-lambda)) / k!
Mean = lambda,  Variance = lambda
```

### Expected Value and Variance

Expected value is the weighted average outcome.

> 期望值是加权平均结果。

```
Discrete:   E[X] = sum of x_i * P(X = x_i)
Continuous: E[X] = integral of x * f(x) dx
```

Variance measures spread around the mean.

> 方差衡量围绕均值的离散程度。

```
Var(X) = E[(X - E[X])^2] = E[X^2] - (E[X])^2
Standard deviation = sqrt(Var(X))
```

In ML, expected value appears as the loss function (average loss over the data distribution). Variance tells you about model stability. High variance in gradients means noisy training.

> 在 ML 中，期望值表现为损失函数（数据分布上的平均损失），方差告诉你模型稳定性。梯度方差大意味着训练噪声大。

### Joint and Marginal Distributions

A joint distribution P(X, Y) describes two random variables together.

> 联合分布 P(X, Y) 描述两个随机变量同时出现的情况。

Joint PMF example (X = weather, Y = umbrella):
联合 PMF 示例（X = 天气，Y = 是否带伞）：

| | Y=0 (no umbrella / 不带伞) | Y=1 (umbrella / 带伞) | Marginal P(X) / 边缘 P(X) |
|---|---|---|---|
| X=0 (sun / 晴天) | 0.40 | 0.10 | P(X=0) = 0.50 |
| X=1 (rain / 下雨) | 0.05 | 0.45 | P(X=1) = 0.50 |
| **Marginal P(Y) / 边缘 P(Y)** | P(Y=0) = 0.45 | P(Y=1) = 0.55 | 1.00 |

The marginal distribution sums out the other variable:

> 边缘分布通过对另一个变量求和得到：

```
P(X = x) = sum over all y of P(X = x, Y = y)
```

The row and column totals in the table above are the marginals.

> 上表中的行合计和列合计就是边缘分布。

### Why the Normal Distribution Shows Up Everywhere

The Central Limit Theorem: the sum (or average) of many independent random variables converges to a normal distribution, regardless of the original distribution.

> 中心极限定理：许多独立随机变量的和（或平均）收敛到正态分布，无论原始分布是什么。

```
Roll 1 die:  uniform distribution (flat)
Average of 2 dice:  triangular (peaked)
Average of 30 dice: nearly perfect bell curve

This works for ANY starting distribution.
```

This is why:
- Measurement errors are approximately normal (many small independent sources)
  中文翻译：测量误差近似正态（由许多小的独立来源叠加）
- Weight initializations in neural networks use normal distributions
  中文翻译：神经网络的权重初始化使用正态分布
- Gradient noise in SGD is approximately normal (sum of many sample gradients)
  中文翻译：SGD 中的梯度噪声近似正态（许多样本梯度的总和）
- The normal distribution is the maximum entropy distribution for a given mean and variance
  中文翻译：正态分布是给定均值和方差下熵最大的分布

### Log Probabilities

Raw probabilities cause numerical problems. Multiplying many small probabilities together quickly underflows to zero.

> 原始概率会导致数值问题。许多小概率相乘很快就会下溢为零。

```
P(sentence) = P(word1) * P(word2) * ... * P(word_n)
            = 0.01 * 0.003 * 0.02 * ...
            -> 0.0 (underflow after ~30 terms)
```

Log probabilities fix this. Multiplications become additions.

> 对数概率解决了这个问题。乘法变成了加法。

```
log P(sentence) = log P(word1) + log P(word2) + ... + log P(word_n)
                = -4.6 + -5.8 + -3.9 + ...
                -> finite number (no underflow)
```

Rules:
- log(a * b) = log(a) + log(b)
- log probabilities are always <= 0 (since 0 < P <= 1)
- More negative = less likely
- Cross-entropy loss is the negative log probability of the correct class

> 规则：
> - log(a * b) = log(a) + log(b)
> - 对数概率总是 <= 0（因为 0 < P <= 1）
> - 越负 = 越不可能
> - 交叉熵损失就是正确类别的负对数概率

### Softmax as a Probability Distribution

Neural networks output raw scores (logits). Softmax converts them into a valid probability distribution.

> 神经网络输出原始分数（logits）。Softmax 将它们转换为有效的概率分布。

```
softmax(z_i) = exp(z_i) / sum(exp(z_j) for all j)

Properties:
  - All outputs are in (0, 1)
  - All outputs sum to 1
  - Preserves relative ordering of inputs
  - exp() amplifies differences between logits
```

The softmax trick: subtract the max logit before exponentiating to prevent overflow.

> Softmax 技巧：在取指数之前减去最大 logit，防止溢出。

```
z = [100, 101, 102]
exp(102) = overflow

z_shifted = z - max(z) = [-2, -1, 0]
exp(0) = 1  (safe)

Same result, no overflow.
```

Log-softmax combines softmax and log for numerical stability. PyTorch uses this internally for cross-entropy loss.

> Log-softmax 将 softmax 和 log 合并为一步以保持数值稳定性。PyTorch 内部的交叉熵损失就使用了这种方式。

### Sampling

Sampling means drawing random values from a distribution. In ML:
- Dropout randomly samples which neurons to zero out
  中文翻译：Dropout 随机采样决定哪些神经元置零
- Data augmentation samples random transformations
  中文翻译：数据增强采样随机变换
- Language models sample the next token from the predicted distribution
  中文翻译：语言模型从预测分布中采样下一个词
- Diffusion models sample noise and progressively denoise
  中文翻译：扩散模型采样噪声并逐步去噪

Sampling from arbitrary distributions requires techniques like inverse transform sampling, rejection sampling, or the reparameterization trick (used in VAEs).

> 从任意分布中采样需要逆变换采样、拒绝采样或重参数化技巧（VAE 中使用）等技术。

## Build It | 动手实现

### Step 1: Probability basics

```python
import math
import random

def factorial(n):
    result = 1
    for i in range(2, n + 1):
        result *= i
    return result

def combinations(n, k):
    return factorial(n) // (factorial(k) * factorial(n - k))

def conditional_probability(p_a_and_b, p_b):
    return p_a_and_b / p_b

p_king_given_face = conditional_probability(4/52, 12/52)
print(f"P(King | Face card) = {p_king_given_face:.4f}")
```

### Step 2: PMF and PDF from scratch

```python
def bernoulli_pmf(k, p):
    return p if k == 1 else (1 - p)

def categorical_pmf(k, probs):
    return probs[k]

def poisson_pmf(k, lam):
    return (lam ** k) * math.exp(-lam) / factorial(k)

def uniform_pdf(x, a, b):
    if a <= x <= b:
        return 1.0 / (b - a)
    return 0.0

def normal_pdf(x, mu, sigma):
    coeff = 1.0 / (sigma * math.sqrt(2 * math.pi))
    exponent = -0.5 * ((x - mu) / sigma) ** 2
    return coeff * math.exp(exponent)
```

### Step 3: Expected value and variance

```python
def expected_value(values, probabilities):
    return sum(v * p for v, p in zip(values, probabilities))

def variance(values, probabilities):
    mu = expected_value(values, probabilities)
    return sum(p * (v - mu) ** 2 for v, p in zip(values, probabilities))

die_values = [1, 2, 3, 4, 5, 6]
die_probs = [1/6] * 6
mu = expected_value(die_values, die_probs)
var = variance(die_values, die_probs)
print(f"Die: E[X] = {mu:.4f}, Var(X) = {var:.4f}, SD = {var**0.5:.4f}")
```

### Step 4: Sampling from distributions

```python
def sample_bernoulli(p, n=1):
    return [1 if random.random() < p else 0 for _ in range(n)]

def sample_categorical(probs, n=1):
    cumulative = []
    total = 0
    for p in probs:
        total += p
        cumulative.append(total)
    samples = []
    for _ in range(n):
        r = random.random()
        for i, c in enumerate(cumulative):
            if r <= c:
                samples.append(i)
                break
    return samples

def sample_normal_box_muller(mu, sigma, n=1):
    samples = []
    for _ in range(n):
        u1 = random.random()
        u2 = random.random()
        z = math.sqrt(-2 * math.log(u1)) * math.cos(2 * math.pi * u2)
        samples.append(mu + sigma * z)
    return samples
```

### Step 5: Softmax and log probabilities

```python
def softmax(logits):
    max_logit = max(logits)
    shifted = [z - max_logit for z in logits]
    exps = [math.exp(z) for z in shifted]
    total = sum(exps)
    return [e / total for e in exps]

def log_softmax(logits):
    max_logit = max(logits)
    shifted = [z - max_logit for z in logits]
    log_sum_exp = max_logit + math.log(sum(math.exp(z) for z in shifted))
    return [z - log_sum_exp for z in logits]

def cross_entropy_loss(logits, target_index):
    log_probs = log_softmax(logits)
    return -log_probs[target_index]
```

### Step 6: Central Limit Theorem demonstration

```python
def demonstrate_clt(dist_fn, n_samples, n_averages):
    averages = []
    for _ in range(n_averages):
        samples = [dist_fn() for _ in range(n_samples)]
        averages.append(sum(samples) / len(samples))
    return averages
```

### Step 7: Visualization

```python
import matplotlib.pyplot as plt

xs = [mu + sigma * (i - 500) / 100 for i in range(1001)]
ys = [normal_pdf(x, mu, sigma) for x, mu, sigma in ...]
plt.plot(xs, ys)
```

Full implementations with all visualizations are in `code/probability.py`.

> 包含所有可视化的完整实现见 `code/probability.py`。

## Use It | 用框架实现

With NumPy and SciPy, everything above is one-liners:

> 使用 NumPy 和 SciPy，上面的所有功能只需一行代码：

```python
import numpy as np
from scipy import stats

normal = stats.norm(loc=0, scale=1)
samples = normal.rvs(size=10000)
print(f"Mean: {np.mean(samples):.4f}, Std: {np.std(samples):.4f}")
print(f"P(X < 1.96) = {normal.cdf(1.96):.4f}")

logits = np.array([2.0, 1.0, 0.1])
from scipy.special import softmax, log_softmax
probs = softmax(logits)
log_probs = log_softmax(logits)
print(f"Softmax: {probs}")
print(f"Log-softmax: {log_probs}")
```

You built these from scratch. Now you know what the library calls are doing.

> 你从零构建了这些。现在你知道库函数在做什么了。

## Exercises | 练习题

1. Implement inverse transform sampling for the exponential distribution. Verify by sampling 10,000 values and comparing the histogram to the true PDF.

2. Build a joint distribution table for two loaded dice. Compute the marginal distributions and check whether the dice are independent.

3. Compute the cross-entropy loss for a 5-class classifier that outputs logits `[2.0, 0.5, -1.0, 3.0, 0.1]` when the correct class is index 3. Then verify your answer with PyTorch's `nn.CrossEntropyLoss`.

4. Write a function that takes a list of log probabilities and returns the most likely sequence, the total log probability, and the equivalent raw probability. Test it with a sentence of 50 words where each word has probability 0.01.

## Key Terms | 术语速查表

| Term | What people say | What it actually means |
|------|----------------|----------------------|
| Sample space | "All the possibilities" / "所有可能性" | The set S of every possible outcome of an experiment / 实验所有可能结果的集合 S |
| PMF | "The probability function" / "概率函数" | A function that gives the exact probability of each discrete outcome, summing to 1 / 给出每个离散结果精确概率的函数，总和为 1 |
| PDF | "The probability curve" / "概率曲线" | A density function for continuous variables. Integrate it over an interval to get probability / 连续变量的密度函数，在区间上积分得到概率 |
| Conditional probability | "Probability given something" / "条件概率" | P(A\|B) = P(A and B) / P(B). The foundation of Bayesian thinking and Bayes' theorem / 贝叶斯思维和贝叶斯定理的基础 |
| Independence | "They don't affect each other" / "互不影响" | P(A and B) = P(A) * P(B). Knowing one event tells you nothing about the other / 知道一个事件不影响另一个 |
| Expected value | "The average" / "平均值" | The probability-weighted sum of all outcomes. The loss function is an expected value / 所有结果的概率加权求和，损失函数就是一种期望值 |
| Variance | "How spread out" / "离散程度" | The expected squared deviation from the mean. High variance = noisy, unstable estimates / 偏离均值的平方的期望，方差大 = 噪声大、不稳定 |
| Normal distribution | "The bell curve" / "钟形曲线" | f(x) = (1/sqrt(2*pi*sigma^2)) * exp(-(x-mu)^2/(2*sigma^2)). Appears everywhere due to the CLT / 因中心极限定理而无处不在 |
| Central Limit Theorem | "Averages become normal" / "平均趋于正态" | The mean of many independent samples converges to a normal distribution regardless of the source / 许多独立样本的均值收敛到正态分布 |
| Joint distribution | "Two variables together" / "两个变量一起" | P(X, Y) describes the probability of every combination of X and Y outcomes / 描述 X 和 Y 每种组合的概率 |
| Marginal distribution | "Sum out the other variable" / "消去另一个变量" | P(X) = sum_y P(X, Y). Recovers one variable's distribution from the joint / 从联合分布中恢复单个变量的分布 |
| Log probability | "Log of the probability" / "概率的对数" | log P(x). Turns products into sums, preventing numerical underflow in long sequences / 将乘法变加法，防止长序列数值下溢 |
| Softmax | "Turn scores into probabilities" / "分数转概率" | softmax(z_i) = exp(z_i) / sum(exp(z_j)). Maps real-valued logits to a valid probability distribution / 将实数值 logits 映射为有效概率分布 |
| Cross-entropy | "The loss function" / "损失函数" | -sum(p_true * log(p_predicted)). Measures how different two distributions are. Lower is better / 衡量两个分布的差异，越小越好 |
| Logits | "Raw model outputs" / "模型原始输出" | Unnormalized scores before softmax. Named after the logistic function / softmax 之前的未归一化分数 |
| Sampling | "Drawing random values" / "随机取值" | Generating values according to a probability distribution. How models generate output / 按概率分布生成值，模型用它生成输出 |

## Further Reading | 延伸阅读

- [3Blue1Brown: But what is the Central Limit Theorem?](https://www.youtube.com/watch?v=zeJD6dqJ5lo) - visual proof of why averages become normal
- [Stanford CS229 Probability Review](https://cs229.stanford.edu/section/cs229-prob.pdf) - concise reference covering everything here and more
- [The Log-Sum-Exp Trick](https://gregorygundersen.com/blog/2020/02/09/log-sum-exp/) - why numerical stability matters and how to achieve it
