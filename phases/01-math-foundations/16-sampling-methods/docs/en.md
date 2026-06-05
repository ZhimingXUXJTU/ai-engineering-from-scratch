# Sampling Methods | 采样方法

> Sampling is how AI explores the space of possibilities.
> 采样是 AI 探索可能性空间的方式。

**Type:** Build | **类型:** 动手
**Language:** Python | **语言:** Python
**Prerequisites:** Phase 1, Lessons 06-07 (Probability, Bayes' Theorem) | **前置知识:** Phase 1, 第 06-07 课（概率、贝叶斯定理）
**Time:** ~120 minutes | **时间:** ~120 分钟

## Learning Objectives | 学习目标

- Implement inverse CDF, rejection, and importance sampling from scratch using only uniform random numbers
  使用均匀随机数从零实现逆 CDF（Inverse CDF）、拒绝采样（Rejection Sampling）和重要性采样（Importance Sampling）
- Build temperature, top-k, and top-p (nucleus) sampling for language model token generation
  构建用于语言模型 token 生成的 temperature、top-k 和 top-p（nucleus）采样
- Explain the reparameterization trick and why it enables backpropagation through sampling in VAEs
  解释重参数化技巧（Reparameterization Trick）以及为什么它能使 VAE 中的采样操作支持反向传播
- Run Metropolis-Hastings MCMC to sample from an unnormalized target distribution
  运行 Metropolis-Hastings MCMC 从未归一化的目标分布中采样


> **【中文解读】**
> 采样是 AI 探索可能性的方式。LLM 用 temperature/top-k/top-p 控制文本生成多样性。VAE 用重参数化技巧让采样可微。扩散模型的前向过程是采样（加噪），反向过程是去噪（生成）。

## The Problem | 问题引入

A language model finishes processing your prompt and produces a vector of 50,000 logits. One for every token in its vocabulary. Now it has to pick one. How?

> 语言模型处理完你的提示后，会生成一个包含 50,000 个 logit 的向量，对应词汇表中的每个 token。现在它需要从中选一个。怎么选？

If it always picks the highest-probability token, every response is identical. Deterministic. Boring. If it picks uniformly at random, the output is gibberish. The answer lives somewhere between these extremes, and that somewhere is controlled by sampling.

> 如果每次都选概率最高的 token，每次回答都一样——确定性的、无聊的。如果均匀随机选取，输出就是胡言乱语。答案介于两个极端之间，而这个中间地带由采样（Sampling）策略控制。

Sampling is not limited to text generation. Reinforcement learning estimates policy gradients by sampling trajectories. VAEs learn latent representations by sampling from learned distributions and backpropagating through the randomness. Diffusion models generate images by sampling noise and iteratively denoising. Monte Carlo methods estimate integrals that have no closed-form solution. MCMC algorithms explore high-dimensional posterior distributions that are impossible to enumerate.

> 采样不仅限于文本生成。强化学习通过采样轨迹（Trajectory）来估计策略梯度。VAE 通过从学习到的分布中采样并反向传播来学习隐表示。扩散模型通过采样噪声并迭代去噪来生成图像。蒙特卡洛方法估计没有解析解的积分。MCMC 算法探索无法枚举的高维后验分布。

Every generative AI system is a sampling system. The sampling strategy determines the quality, diversity, and controllability of the output. This lesson builds every major sampling method from scratch, starting from uniform random numbers and ending with the techniques that power modern LLMs and generative models.

> 每个生成式 AI 系统本质上都是一个采样系统。采样策略决定了输出的质量、多样性和可控性。本课从零构建所有主要采样方法，从均匀随机数开始，一直到驱动现代 LLM 和生成模型的技术。

## The Concept | 核心概念

> **【中文解读】**
> 采样问题无处不在：语言模型要从 5 万个 token 中选一个，VAE 要从隐空间采样，扩散模型要从噪声逐步去噪。核心挑战是你只能直接从简单分布（均匀分布、正态分布）采样，必须通过巧妙变换才能得到复杂目标分布的样本。

### Why Sampling Matters

Sampling appears in four fundamental roles across AI and machine learning:

> 采样在 AI 和机器学习中扮演四个基本角色：

**Generation.** Language models, diffusion models, and GANs all produce output by sampling. The sampling algorithm directly controls creativity, coherence, and diversity. Temperature, top-k, and nucleus sampling are the knobs that engineers turn daily.

> **生成。** 语言模型、扩散模型和 GAN 都通过采样产生输出。采样算法直接控制创造力、连贯性和多样性。Temperature、top-k 和 nucleus 采样是工程师每天调节的"旋钮"。

**Training.** Stochastic gradient descent samples mini-batches. Dropout samples neurons to deactivate. Data augmentation samples random transformations. Importance sampling reweights samples to reduce gradient variance in reinforcement learning (PPO, TRPO).

> **训练。** 随机梯度下降（SGD）采样 mini-batch。Dropout 采样要禁用的神经元。数据增强采样随机变换。重要性采样重新加权样本以降低强化学习（PPO、TRPO）中的梯度方差。

**Estimation.** Many quantities in ML have no closed-form solution. The expected loss over a data distribution, the partition function of an energy-based model, the evidence in Bayesian inference. Monte Carlo estimation approximates all of these by averaging over samples.

> **估计。** ML 中的许多量没有解析解。数据分布上的期望损失、基于能量模型的配分函数、贝叶斯推断中的证据（Evidence）。蒙特卡洛估计通过对样本求平均来近似所有这些量。

**Exploration.** MCMC algorithms explore posterior distributions in Bayesian inference. Evolutionary strategies sample parameter perturbations. Thompson sampling balances exploration and exploitation in bandits.

> **探索。** MCMC 算法在贝叶斯推断中探索后验分布。进化策略（Evolutionary Strategies）采样参数扰动。Thompson 采样在多臂老虎机问题中平衡探索与利用。

The core challenge: you can only sample directly from simple distributions (uniform, normal). For everything else, you need a method to convert simple samples into samples from your target distribution.

> 核心挑战：你只能直接从简单分布（均匀分布、正态分布）中采样。对于其他一切分布，你需要一种方法将简单样本转换为目标分布的样本。

> **【拓展：LLM 采样策略的工程实践】**
> GPT-4 等模型推理时，temperature 通常设为 0.0-1.0，top-p 设为 0.9-1.0。OpenAI API 默认 temperature=1.0、top_p=1.0。研究表明 top-p (nucleus) 采样在大多数任务上优于 top-k，因为它能根据模型置信度自适应调整候选集大小。对于代码生成，temperature=0.2 + top_p=0.95 是常见配置。

### Uniform Random Sampling

Every sampling method starts here. A uniform random number generator produces values in [0, 1) where every sub-interval of equal length has equal probability.

> 所有采样方法都从这里开始。均匀随机数生成器产生 [0, 1) 中的值，其中等长的子区间具有相等的概率。

```
U ~ Uniform(0, 1)

P(a <= U <= b) = b - a    for 0 <= a <= b <= 1

Properties:
  E[U] = 0.5
  Var(U) = 1/12
```

To sample uniformly from a discrete set of n items, generate U and return floor(n * U). To sample from a continuous range [a, b], compute a + (b - a) * U.

> 要从 n 个元素的离散集合中均匀采样，生成 U 并返回 floor(n * U)。要从连续区间 [a, b] 中采样，计算 a + (b - a) * U。

The key insight: a single uniform random number contains exactly the right amount of randomness to produce one sample from any distribution. The trick is finding the right transformation.

> 关键洞察：单个均匀随机数包含了恰好足够的随机性，可以从任何分布中产生一个样本。诀窍在于找到正确的变换。

> **【中文解读】**
> 均匀分布是所有采样的基石。计算机中的伪随机数生成器（如 Mersenne Twister）产生的就是 [0,1) 上的均匀分布。采样方法本质上是把均匀随机数"变换"成目标分布的样本，就像用一把万能钥匙打开不同锁。

### Inverse CDF Method (Inverse Transform Sampling)

The cumulative distribution function (CDF) maps values to probabilities:

```
F(x) = P(X <= x)

Properties:
  F is non-decreasing
  F(-inf) = 0
  F(+inf) = 1
  F maps the real line to [0, 1]
```

The inverse CDF maps probabilities back to values. If U ~ Uniform(0, 1), then X = F_inverse(U) follows the target distribution.

> 逆 CDF 将概率映射回值。如果 U ~ Uniform(0, 1)，那么 X = F_inverse(U) 服从目标分布。

```
Algorithm:
  1. Generate u ~ Uniform(0, 1)
  2. Return F_inverse(u)

Why it works:
  P(X <= x) = P(F_inverse(U) <= x) = P(U <= F(x)) = F(x)
```

**Exponential distribution example:**

```
PDF: f(x) = lambda * exp(-lambda * x),   x >= 0
CDF: F(x) = 1 - exp(-lambda * x)

Solve F(x) = u for x:
  u = 1 - exp(-lambda * x)
  exp(-lambda * x) = 1 - u
  x = -ln(1 - u) / lambda

Since (1 - U) and U have the same distribution:
  x = -ln(u) / lambda
```

This works perfectly when you can write down F_inverse in closed form. For the normal distribution, there is no closed-form inverse CDF, so we use other methods (Box-Muller, or numerical approximation).

> 当你能写出 F_inverse 的解析表达式时，这个方法完美运作。对于正态分布，没有解析形式的逆 CDF，所以我们使用其他方法（Box-Muller 或数值近似）。

**Discrete version:** For discrete distributions, build the CDF as a cumulative sum, generate U, and find the first index where the cumulative sum exceeds U. This is how `sample_categorical` works in Lesson 06.

> **离散版本：** 对于离散分布，将 CDF 构建为累积和，生成 U，找到累积和首次超过 U 的索引。这就是第 06 课中 `sample_categorical` 的工作方式。

> **【中文解读】**
> 逆 CDF 方法的核心思想：CDF 函数 F(x) 把随机变量的值映射到 [0,1] 上的概率，而它的逆函数 F_inverse 正好反过来——把 [0,1] 上的均匀随机数映射回目标分布的值。这个方法精确、高效，但前提是你能写出逆函数的解析表达式。

### Rejection Sampling

When you cannot invert the CDF but can evaluate the target PDF up to a constant, rejection sampling works.

> 当你无法求逆 CDF，但可以计算目标 PDF（至多差一个常数因子）时，拒绝采样（Rejection Sampling）就可以派上用场。

```
Target distribution: p(x)  (can evaluate, possibly unnormalized)
Proposal distribution: q(x)  (can sample from)
Bound: M such that p(x) <= M * q(x) for all x

Algorithm:
  1. Sample x ~ q(x)
  2. Sample u ~ Uniform(0, 1)
  3. If u < p(x) / (M * q(x)), accept x
  4. Otherwise, reject and go to step 1

Acceptance rate = 1/M
```

The tighter the bound M, the higher the acceptance rate. In low dimensions (1-3), rejection sampling works well. In high dimensions, the acceptance rate drops exponentially because most of the proposal volume gets rejected. This is the curse of dimensionality for rejection sampling.

> 包络 M 越紧，接受率越高。在低维空间（1-3 维），拒绝采样效果很好。在高维空间中，接受率呈指数下降，因为大部分提议体积都被拒绝了。这就是拒绝采样的维数灾难。

**Example: sampling from a truncated normal.** Use a uniform proposal over the truncated range. The envelope M is the maximum of the normal PDF in that range.

> **示例：从截断正态分布采样。** 在截断范围内使用均匀提议分布。包络 M 是正态 PDF 在该范围内的最大值。

**Example: sampling from a semicircle.** Propose uniformly in the bounding rectangle. Accept if the point falls inside the semicircle. This is how Monte Carlo computes pi: the acceptance rate equals the area ratio pi/4.

> **示例：从半圆采样。** 在外接矩形中均匀提议。如果点落在半圆内就接受。这就是蒙特卡洛计算 pi 的方法：接受率等于面积比 pi/4。

> **【拓展：拒绝采样在粒子滤波中的应用】**
> 粒子滤波（Particle Filter）是目标跟踪和机器人定位的核心算法。它本质上就是一种拒绝采样——用一组"粒子"近似后验分布，根据观测结果对粒子加权重采样。自动驾驶公司如 Waymo 在实时定位中使用了数万个粒子的粒子滤波器，每秒更新数十次。

### Importance Sampling

Sometimes you do not need samples from the target distribution p(x). You need to estimate an expectation under p(x), and you have samples from a different distribution q(x).

> 有时你不需要从目标分布 p(x) 中采样，而是需要在 p(x) 下估计一个期望，而你手上有来自另一个分布 q(x) 的样本。

```
Goal: estimate E_p[f(x)] = integral of f(x) * p(x) dx

Rewrite:
  E_p[f(x)] = integral of f(x) * (p(x)/q(x)) * q(x) dx
            = E_q[f(x) * w(x)]

where w(x) = p(x) / q(x)  are the importance weights.

Estimator:
  E_p[f(x)] ~ (1/N) * sum(f(x_i) * w(x_i))    where x_i ~ q(x)
```

This is critical in reinforcement learning. In PPO (Proximal Policy Optimization), you collect trajectories under an old policy pi_old but want to optimize a new policy pi_new. The importance weight is pi_new(a|s) / pi_old(a|s). PPO clips these weights to prevent the new policy from diverging too far from the old one.

> 这在强化学习中至关重要。在 PPO（Proximal Policy Optimization）中，你在旧策略 pi_old 下收集轨迹，但想优化新策略 pi_new。重要性权重就是 pi_new(a|s) / pi_old(a|s)。PPO 裁剪这些权重以防止新策略偏离旧策略太远。

> **【拓展：PPO 中的重要性采样】**
> PPO 是 ChatGPT RLHF 训练的核心算法。它用重要性采样修正新旧策略之间的分布差异。PPO 的关键创新是裁剪（clipping）：当重要性权重 ratio = pi_new/pi_old 超出 [1-epsilon, 1+epsilon] 范围时（epsilon 通常为 0.2），截断梯度防止策略更新过大。这使得训练比 TRPO 更稳定高效。

The variance of the importance sampling estimator depends on how similar q is to p. If q is very different from p, a few samples get enormous weights and dominate the estimate. Self-normalized importance sampling divides by the sum of weights to reduce this problem:

> 重要性采样估计器的方差取决于 q 与 p 的相似程度。如果 q 与 p 差异很大，少数样本会获得巨大的权重并主导估计。自归一化重要性采样通过除以权重之和来缓解这个问题：

```
E_p[f(x)] ~ sum(w_i * f(x_i)) / sum(w_i)
```

### Monte Carlo Estimation

Monte Carlo estimation approximates integrals by averaging random samples. The law of large numbers guarantees convergence.

> 蒙特卡洛估计通过对随机样本取平均来近似积分。大数定律保证了收敛性。

```
Goal: estimate I = integral of g(x) dx over domain D

Method:
  1. Sample x_1, ..., x_N uniformly from D
  2. I ~ (Volume of D / N) * sum(g(x_i))

Error: O(1 / sqrt(N))   regardless of dimension
```

The error rate is dimension-independent. This is why Monte Carlo methods dominate in high dimensions where grid-based integration is impossible.

> 误差率与维度无关。这就是为什么蒙特卡洛方法在高维空间中占据主导地位——在高维空间中，基于网格的积分是不可行的。

> **【中文解读】**
> 蒙特卡洛方法的精髓：用随机样本的平均值来近似期望。大数定律保证了收敛，而且误差率 O(1/sqrt(N)) 与维度无关。这在高维问题中极为重要——100 维的积分用网格法需要 2^100 个点，而蒙特卡洛只需几万个样本就能得到不错的估计。

**Estimating pi:**

```
Sample (x, y) uniformly from [-1, 1] x [-1, 1]
Count how many fall inside the unit circle: x^2 + y^2 <= 1
pi ~ 4 * (count inside) / (total count)
```

**Estimating expectations:**

```
E[f(X)] ~ (1/N) * sum(f(x_i))    where x_i ~ p(x)

The sample mean converges to the true expectation.
Variance of the estimator = Var(f(X)) / N
```

### Markov Chain Monte Carlo (MCMC): Metropolis-Hastings

MCMC constructs a Markov chain whose stationary distribution is the target distribution p(x). After enough steps, samples from the chain are (approximately) samples from p(x).

> MCMC 构造一个马尔可夫链（Markov Chain），其平稳分布（Stationary Distribution）就是目标分布 p(x)。经过足够多的步数后，链上的样本（近似地）就是 p(x) 的样本。

```
Target: p(x)  (known up to a normalizing constant)
Proposal: q(x'|x)  (how to propose the next state given the current state)

Metropolis-Hastings algorithm:
  1. Start at some x_0
  2. For t = 1, 2, ..., T:
     a. Propose x' ~ q(x'|x_t)
     b. Compute acceptance ratio:
        alpha = [p(x') * q(x_t|x')] / [p(x_t) * q(x'|x_t)]
     c. Accept with probability min(1, alpha):
        - If u < alpha (u ~ Uniform(0,1)): x_{t+1} = x'
        - Otherwise: x_{t+1} = x_t
  3. Discard first B samples (burn-in)
  4. Return remaining samples
```

For symmetric proposals (q(x'|x) = q(x|x')), the ratio simplifies to p(x')/p(x). This is the original Metropolis algorithm.

> 对于对称提议（q(x'|x) = q(x|x')），比率简化为 p(x')/p(x)。这就是原始的 Metropolis 算法。

**Why it works.** The acceptance rule ensures detailed balance: the probability of being at x and moving to x' equals the probability of being at x' and moving to x. Detailed balance implies that p(x) is the stationary distribution of the chain.

> **为什么有效。** 接受规则确保了细致平衡条件（Detailed Balance）：处于 x 并转移到 x' 的概率等于处于 x' 并转移到 x 的概率。细致平衡意味着 p(x) 是链的平稳分布。

> **【拓展：MCMC 在贝叶斯深度学习中的应用】**
> PyMC、NumPyro 等 Bayesian 推理框架的核心就是 MCMC。NUTS (No-U-Turn Sampler) 是最先进的 MCMC 变体，它自动调节步长和方向。在药物发现中，研究人员用 MCMC 采样分子构型的后验分布，处理数千维参数空间。Stan 语言（以统计学家 Stanislaw Ulam 命名）让研究人员无需手写 MCMC 就能进行贝叶斯推理。

**Practical considerations:**
- Burn-in: discard early samples before the chain reaches equilibrium
  预热期（Burn-in）：丢弃链达到平衡前的早期样本
- Thinning: keep every k-th sample to reduce autocorrelation
  稀释（Thinning）：每隔 k 个样本保留一个以减少自相关
- Proposal scale: too small and the chain moves slowly (high acceptance, slow exploration); too large and most proposals are rejected (low acceptance, stuck in place)
  提议尺度（Proposal Scale）：太小则链移动缓慢（接受率高但探索慢）；太大则大多数提议被拒绝（接受率低，原地不动）
- The optimal acceptance rate for a Gaussian proposal in high dimensions is approximately 0.234
  高维空间中高斯提议的最优接受率约为 0.234

### Gibbs Sampling

Gibbs sampling is a special case of MCMC for multivariate distributions. Instead of proposing a move in all dimensions at once, it updates one variable at a time from its conditional distribution.

> Gibbs 采样是 MCMC 在多变量分布中的特例。它不是同时在所有维度上提议移动，而是每次从条件分布中更新一个变量。

```
Target: p(x_1, x_2, ..., x_d)

Algorithm:
  For each iteration t:
    Sample x_1^{t+1} ~ p(x_1 | x_2^t, x_3^t, ..., x_d^t)
    Sample x_2^{t+1} ~ p(x_2 | x_1^{t+1}, x_3^t, ..., x_d^t)
    ...
    Sample x_d^{t+1} ~ p(x_d | x_1^{t+1}, x_2^{t+1}, ..., x_{d-1}^{t+1})
```

Gibbs sampling requires that you can sample from each conditional distribution p(x_i | x_{-i}). This is straightforward for many models:
- Bayesian networks: conditionals follow from the graph structure
  贝叶斯网络：条件分布由图结构决定
- Gaussian mixtures: conditionals are Gaussian
  高斯混合模型：条件分布是高斯的
- Ising models: each spin's conditional depends only on its neighbors
  Ising 模型：每个自旋的条件分布只依赖其邻居

The acceptance rate is always 1 (every proposal is accepted) because sampling from the exact conditional automatically satisfies detailed balance.

> 接受率永远是 1（每个提议都被接受），因为从精确的条件分布中采样自动满足细致平衡条件。

**Limitation.** When variables are highly correlated, Gibbs sampling mixes slowly because updating one variable at a time cannot make large diagonal moves through the distribution.

> **局限性。** 当变量之间高度相关时，Gibbs 采样混合得很慢，因为每次只更新一个变量无法在分布中做出大的对角移动。

> **【中文解读】**
> Gibbs 采样是 MCMC 的特例：每次只更新一个变量，从条件分布中采样。因为每次采样都来自精确的条件分布，所以接受率永远是 100%。但缺点也很明显——当变量之间高度相关时，每次只能"小步挪"，收敛非常慢。

### Temperature Sampling (Used in LLMs)

Language models output logits z_1, ..., z_V for each token in the vocabulary. Softmax converts these to probabilities. Temperature rescales the logits before softmax:

> 语言模型为词汇表中的每个 token 输出 logits z_1, ..., z_V。Softmax 将它们转换为概率。Temperature（温度）在 softmax 之前对 logits 进行缩放：

```
p_i = exp(z_i / T) / sum(exp(z_j / T))

T = 1.0: standard softmax (original distribution)
T -> 0:  argmax (deterministic, always picks highest logit)
T -> inf: uniform (all tokens equally likely)
T < 1.0: sharpens the distribution (more confident, less diverse)
T > 1.0: flattens the distribution (less confident, more diverse)
```

**Why it works.** Dividing logits by T < 1 amplifies differences between logits. If z_1 = 2 and z_2 = 1, dividing by T = 0.5 gives z_1/T = 4 and z_2/T = 2, making the gap larger. After softmax, the highest-logit token gets a much larger share.

> **为什么有效。** 将 logits 除以 T < 1 会放大 logits 之间的差异。如果 z_1 = 2、z_2 = 1，除以 T = 0.5 得到 z_1/T = 4、z_2/T = 2，差距更大了。经过 softmax 后，最高 logit 的 token 获得更大的份额。

**In practice:**
- T = 0.0: greedy decoding, best for factual Q&A
  贪心解码，最适合事实性问答
- T = 0.3-0.7: slightly creative, good for code generation
  略有创意，适合代码生成
- T = 0.7-1.0: balanced, good for general conversation
  均衡，适合一般对话
- T = 1.0-1.5: creative writing, brainstorming
  创意写作、头脑风暴
- T > 1.5: increasingly random, rarely useful
  越来越随机，很少有用

Temperature does not change which tokens are possible. It changes the probability mass allocated to each token.

> 温度不会改变哪些 token 可能被选中。它改变的是分配给每个 token 的概率质量。

> **【中文解读】**
> Temperature 是 LLM 输出多样性的"旋钮"。T < 1 让分布更尖锐（更像贪心），T > 1 让分布更平坦（更随机）。T → 0 退化为 argmax，T → ∞ 退化为均匀分布。实际中 T=0.7 是最常用的平衡点。注意：温度不改变哪些 token 有可能被选中，只改变概率分配。

### Top-k Sampling

Top-k sampling restricts the candidate set to the k tokens with the highest probabilities, then renormalizes and samples from that restricted set.

> Top-k 采样将候选集限制为概率最高的 k 个 token，然后重新归一化并从该受限集合中采样。

```
Algorithm:
  1. Compute softmax probabilities for all V tokens
  2. Sort tokens by probability (descending)
  3. Keep only the top k tokens
  4. Renormalize: p_i' = p_i / sum(p_j for j in top-k)
  5. Sample from the renormalized distribution

k = 1:  greedy decoding
k = V:  no filtering (standard sampling)
k = 40: typical setting, removes long tail of unlikely tokens
```

Top-k prevents the model from selecting extremely unlikely tokens (typos, nonsense) that exist in the long tail of the vocabulary distribution. The problem: k is fixed regardless of context. When the model is confident (one token has 95% probability), k = 40 still allows 39 alternatives. When the model is uncertain (probability is spread across 1000 tokens), k = 40 cuts off plausible options.

> Top-k 防止模型选择词汇分布长尾中极不可能的 token（错别字、无意义的词）。问题在于：k 是固定的，不随上下文变化。当模型很有信心时（一个 token 占 95% 概率），k = 40 仍允许 39 个替代选项。当模型不确定时（概率分散在 1000 个 token 上），k = 40 会截断合理的选项。

### Top-p (Nucleus) Sampling

Top-p sampling dynamically adjusts the candidate set size. Instead of keeping a fixed number of tokens, it keeps the smallest set of tokens whose cumulative probability exceeds p.

> Top-p 采样动态调整候选集大小。它不保留固定数量的 token，而是保留累积概率超过 p 的最小 token 集合。

```
Algorithm:
  1. Compute softmax probabilities for all V tokens
  2. Sort tokens by probability (descending)
  3. Find smallest k such that sum of top-k probabilities >= p
  4. Keep only those k tokens
  5. Renormalize and sample

p = 0.9:  keeps tokens covering 90% of probability mass
p = 1.0:  no filtering
p = 0.1:  very restrictive, nearly greedy
```

When the model is confident, nucleus sampling keeps few tokens (maybe 2-3). When the model is uncertain, it keeps many (maybe 200). This adaptive behavior is why nucleus sampling generally produces better text than top-k.

> 当模型有信心时，nucleus 采样只保留少量 token（可能 2-3 个）。当模型不确定时，它保留很多（可能 200 个）。这种自适应行为是 nucleus 采样通常比 top-k 产生更好文本的原因。

**Common combinations:**
- Temperature 0.7 + top-p 0.9: good general-purpose setting
  好的通用设置
- Temperature 0.0 (greedy): best for deterministic tasks
  最适合确定性任务
- Temperature 1.0 + top-k 50: Fan et al. (2018) original paper setting
  Fan 等人 (2018) 原论文设置

Top-k and top-p can be combined. Apply top-k first, then top-p on the remaining set.

> Top-k 和 top-p 可以组合使用。先应用 top-k，再在剩余集合上应用 top-p。

### Reparameterization Trick (Used in VAEs)

Variational autoencoders (VAEs) learn by encoding inputs into a distribution in latent space, sampling from that distribution, and decoding the sample back. The problem: you cannot backpropagate through a sampling operation.

> 变分自编码器（VAE）通过将输入编码为隐空间中的分布、从该分布采样、然后将样本解码回来来学习。问题是：你无法通过采样操作进行反向传播。

```
Standard sampling (not differentiable):
  z ~ N(mu, sigma^2)

  The randomness blocks gradient flow.
  d/d_mu [sample from N(mu, sigma^2)] = ???
```

The reparameterization trick separates the randomness from the parameters:

> 重参数化技巧将随机性与参数分离开来：

```
Reparameterized sampling:
  epsilon ~ N(0, 1)          (fixed random noise, no parameters)
  z = mu + sigma * epsilon   (deterministic function of parameters)

  Now z is a deterministic, differentiable function of mu and sigma.
  d(z)/d(mu) = 1
  d(z)/d(sigma) = epsilon

  Gradients flow through mu and sigma.
```

This works because N(mu, sigma^2) has the same distribution as mu + sigma * N(0, 1). The key insight: move the randomness to a parameter-free source (epsilon), then express the sample as a differentiable transformation of the parameters.

> 这之所以有效，是因为 N(mu, sigma^2) 与 mu + sigma * N(0, 1) 具有相同的分布。关键洞察：将随机性移到一个无参数的源（epsilon），然后将样本表示为参数的可微变换。

**In the VAE training loop:**
1. Encoder outputs mu and log(sigma^2) for each input
2. Sample epsilon ~ N(0, 1)
3. Compute z = mu + sigma * epsilon
4. Decode z to reconstruct the input
5. Backpropagate through steps 4, 3, 2, 1 (possible because step 3 is differentiable)

Without the reparameterization trick, VAEs cannot be trained with standard backpropagation. This single insight made VAEs practical.

> 没有重参数化技巧，VAE 就无法用标准反向传播训练。这一个洞察使 VAE 变得可行。

> **【拓展：重参数化技巧的广泛应用】**
> 重参数化技巧不限于 VAE。扩散模型（Stable Diffusion、DALL-E）的每一步去噪都用了重参数化：z = mu + sigma * epsilon。强化学习中，SAC (Soft Actor-Critic) 用重参数化计算策略梯度。可以说，只要涉及"从可学习分布中采样+反向传播"，就离不开这个技巧。

### Gumbel-Softmax (Differentiable Categorical Sampling)

The reparameterization trick works for continuous distributions (Gaussian). For discrete categorical distributions, we need a different approach. Gumbel-Softmax provides a differentiable approximation to categorical sampling.

> 重参数化技巧适用于连续分布（高斯分布）。对于离散的分类分布，我们需要不同的方法。Gumbel-Softmax 提供了分类采样的可微近似。

**The Gumbel-Max trick (non-differentiable):**

```
To sample from a categorical distribution with log-probabilities log(p_1), ..., log(p_k):
  1. Sample g_i ~ Gumbel(0, 1) for each category
     (g = -log(-log(u)), where u ~ Uniform(0, 1))
  2. Return argmax(log(p_i) + g_i)

This produces exact categorical samples.
```

**Gumbel-Softmax (differentiable approximation):**

```
Replace the hard argmax with a soft softmax:
  y_i = exp((log(p_i) + g_i) / tau) / sum(exp((log(p_j) + g_j) / tau))

tau (temperature) controls the approximation:
  tau -> 0:  approaches a one-hot vector (hard categorical)
  tau -> inf: approaches uniform (1/k, 1/k, ..., 1/k)
  tau = 1.0: soft approximation
```

Gumbel-Softmax produces a continuous relaxation of a discrete sample. The output is a probability vector (soft one-hot) instead of a hard one-hot. Gradients flow through the softmax. During the forward pass in training, you can use the "straight-through" estimator: use the hard argmax for the forward pass but the soft Gumbel-Softmax gradients for the backward pass.

> Gumbel-Softmax 产生离散样本的连续松弛（Continuous Relaxation）。输出是一个概率向量（软 one-hot）而不是硬 one-hot。梯度可以流过 softmax。在训练的前向传播中，你可以使用"直通估计器"（Straight-Through Estimator）：前向传播使用硬 argmax，反向传播使用软 Gumbel-Softmax 梯度。

**Applications:**
- Discrete latent variables in VAEs
  VAE 中的离散隐变量
- Neural architecture search (choosing discrete operations)
  神经架构搜索（选择离散操作）
- Hard attention mechanisms
  硬注意力机制
- Reinforcement learning with discrete actions
  离散动作的强化学习

### Stratified Sampling

Standard Monte Carlo sampling can leave gaps in the sample space by chance. Stratified sampling forces even coverage by dividing the space into strata and sampling from each.

> 标准蒙特卡洛采样可能会偶然在样本空间中留下空隙。分层采样（Stratified Sampling）通过将空间划分为层（Strata）并从每层中采样来强制均匀覆盖。

```
Standard Monte Carlo:
  Sample N points uniformly from [0, 1]
  Some regions may have clusters, others gaps

Stratified sampling:
  Divide [0, 1] into N equal strata: [0, 1/N), [1/N, 2/N), ..., [(N-1)/N, 1)
  Sample one point uniformly within each stratum
  x_i = (i + u_i) / N   where u_i ~ Uniform(0, 1),  i = 0, ..., N-1
```

Stratified sampling always has lower or equal variance compared to standard Monte Carlo:

> 分层采样的方差总是低于或等于标准蒙特卡洛：

```
Var(stratified) <= Var(standard Monte Carlo)

The improvement is largest when f(x) varies smoothly.
For piecewise-constant functions, stratified sampling is exact.
```

**Applications:**
- Numerical integration (quasi-Monte Carlo)
  数值积分（准蒙特卡洛）
- Training data splits (ensuring class balance in each fold)
  训练数据划分（确保每折的类别平衡）
- Importance sampling with stratification (combining both techniques)
  结合分层的重要性采样
- NeRF (Neural Radiance Fields) uses stratified sampling along camera rays
  NeRF（神经辐射场）沿相机光线使用分层采样

### Connection to Diffusion Models

Diffusion models generate images through a sampling process. The forward process adds Gaussian noise to an image over T steps until it becomes pure noise. The reverse process learns to denoise, recovering the original image step by step.

> 扩散模型通过采样过程生成图像。前向过程在 T 步内逐渐向图像添加高斯噪声，直到变成纯噪声。反向过程学习去噪，逐步恢复原始图像。

```
Forward process (known):
  x_t = sqrt(alpha_t) * x_{t-1} + sqrt(1 - alpha_t) * epsilon
  where epsilon ~ N(0, I)

  After T steps: x_T ~ N(0, I)  (pure noise)

Reverse process (learned):
  x_{t-1} = (1/sqrt(alpha_t)) * (x_t - (1 - alpha_t)/sqrt(1 - alpha_bar_t) * epsilon_theta(x_t, t)) + sigma_t * z
  where z ~ N(0, I)

  Each denoising step is a sampling step.
```

The connection to the methods in this lesson:
- Each denoising step uses the reparameterization trick (sample noise, apply deterministic transform)
  每个去噪步骤都使用重参数化技巧（采样噪声，应用确定性变换）
- The noise schedule {alpha_t} controls a form of temperature annealing
  噪声调度 {alpha_t} 控制一种形式的温度退火（Temperature Annealing）
- Training uses Monte Carlo estimation to approximate the ELBO (evidence lower bound)
  训练使用蒙特卡洛估计来近似 ELBO（Evidence Lower Bound，证据下界）
- Ancestral sampling in diffusion models is a Markov chain (each step depends only on the current state)
  扩散模型中的祖先采样（Ancestral Sampling）是一个马尔可夫链（每一步只依赖当前状态）

The entire image generation process is iterative sampling: start from noise, and at each step, sample a slightly less noisy version conditioned on the learned denoising model.

> 整个图像生成过程就是迭代采样：从噪声开始，在每一步中，基于学习到的去噪模型采样一个稍微不那么嘈杂的版本。

## Build It | 动手实现

### Step 1: Uniform and inverse CDF sampling

```python
import math
import random

def sample_uniform(a, b):
    return a + (b - a) * random.random()  # 线性变换：把 [0,1) 映射到 [a,b)

def sample_exponential_inverse_cdf(lam):
    u = random.random()                   # 生成均匀随机数
    return -math.log(u) / lam             # 逆 CDF：x = -ln(u) / lambda
```

Generate 10,000 exponential samples and verify the mean is 1/lambda.

> 生成 10,000 个指数分布样本，验证均值是否为 1/lambda。

### Step 2: Rejection sampling

```python
def rejection_sample(target_pdf, proposal_sample, proposal_pdf, M):
    while True:                           # 持续采样直到被接受
        x = proposal_sample()             # 从提议分布采样
        u = random.random()               # 均匀随机数用于决定接受/拒绝
        if u < target_pdf(x) / (M * proposal_pdf(x)):  # 接受条件
            return x
```

Use rejection sampling to draw from a truncated normal distribution. Verify the shape by histogramming the samples.

> 使用拒绝采样从截断正态分布中抽样。通过绘制直方图验证形状。

### Step 3: Importance sampling

```python
def importance_sampling_estimate(f, target_pdf, proposal_pdf, proposal_sample, n):
    total = 0
    for _ in range(n):
        x = proposal_sample()
        w = target_pdf(x) / proposal_pdf(x)
        total += f(x) * w
    return total / n
```

Estimate E[X^2] under a normal distribution using a uniform proposal. Compare to the known answer (mu^2 + sigma^2).

> 使用均匀提议分布估计正态分布下的 E[X^2]。与已知答案 (mu^2 + sigma^2) 比较。

### Step 4: Monte Carlo estimation of pi

```python
def monte_carlo_pi(n):
    inside = 0
    for _ in range(n):
        x = random.uniform(-1, 1)
        y = random.uniform(-1, 1)
        if x*x + y*y <= 1:
            inside += 1
    return 4 * inside / n
```

### Step 5: Metropolis-Hastings MCMC

```python
def metropolis_hastings(target_log_pdf, proposal_sample, proposal_log_pdf, x0, n_samples, burn_in):
    samples = []
    x = x0                                # 初始状态
    for i in range(n_samples + burn_in):
        x_new = proposal_sample(x)        # 从提议分布生成新候选
        log_alpha = (target_log_pdf(x_new) + proposal_log_pdf(x, x_new)  # 计算接受比的对数
                     - target_log_pdf(x) - proposal_log_pdf(x_new, x))
        if math.log(random.random()) < log_alpha:  # 以 min(1, alpha) 的概率接受
            x = x_new
        if i >= burn_in:                  # 丢弃 burn-in 阶段的样本
            samples.append(x)
    return samples
```

Sample from a bimodal distribution (mixture of two Gaussians). Visualize the chain's trajectory.

> 从双峰分布（两个高斯的混合）中采样。可视化链的轨迹。

### Step 6: Gibbs sampling

```python
def gibbs_sampling_2d(conditional_x_given_y, conditional_y_given_x, x0, y0, n_samples, burn_in):
    x, y = x0, y0
    samples = []
    for i in range(n_samples + burn_in):
        x = conditional_x_given_y(y)
        y = conditional_y_given_x(x)
        if i >= burn_in:
            samples.append((x, y))
    return samples
```

### Step 7: Temperature sampling

```python
def softmax(logits):
    max_l = max(logits)
    exps = [math.exp(z - max_l) for z in logits]
    total = sum(exps)
    return [e / total for e in exps]

def temperature_sample(logits, temperature):
    scaled = [z / temperature for z in logits]  # 温度缩放：除以 T
    probs = softmax(scaled)                      # 计算缩放后的概率分布
    return sample_from_probs(probs)
```

Show how temperature changes the output distribution for a set of token logits.

> 展示温度如何改变一组 token logits 的输出分布。

### Step 8: Top-k and top-p sampling

```python
def top_k_sample(logits, k):
    indexed = sorted(enumerate(logits), key=lambda x: -x[1])
    top = indexed[:k]
    top_logits = [l for _, l in top]
    probs = softmax(top_logits)
    idx = sample_from_probs(probs)
    return top[idx][0]

def top_p_sample(logits, p):
    probs = softmax(logits)
    indexed = sorted(enumerate(probs), key=lambda x: -x[1])
    cumsum = 0
    selected = []
    for token_idx, prob in indexed:
        cumsum += prob
        selected.append((token_idx, prob))
        if cumsum >= p:
            break
    sel_probs = [pr for _, pr in selected]
    total = sum(sel_probs)
    sel_probs = [pr / total for pr in sel_probs]
    idx = sample_from_probs(sel_probs)
    return selected[idx][0]
```

### Step 9: Reparameterization trick

```python
def reparam_sample(mu, sigma):
    epsilon = random.gauss(0, 1)          # 标准正态噪声，不含可学习参数
    return mu + sigma * epsilon            # 确定性变换，梯度可流过

def reparam_gradient(mu, sigma, epsilon):
    dz_dmu = 1.0                          # z 对 mu 的梯度恒为 1
    dz_dsigma = epsilon                   # z 对 sigma 的梯度是 epsilon
    return dz_dmu, dz_dsigma
```

Demonstrate that gradients flow through the reparameterized sample but not through direct sampling.

> 演示梯度可以流过重参数化样本，但不能流过直接采样。

### Step 10: Gumbel-Softmax

```python
def gumbel_sample():
    u = random.random()
    return -math.log(-math.log(u))

def gumbel_softmax(logits, temperature):
    gumbels = [math.log(p) + gumbel_sample() for p in logits]
    return softmax([g / temperature for g in gumbels])
```

Show how decreasing temperature makes the output approach a one-hot vector.

> 展示降低温度如何使输出趋近 one-hot 向量。

Full implementations with all visualizations are in `code/sampling.py`.

> 所有可视化的完整实现在 `code/sampling.py` 中。

## Use It | 用框架实现

> **【拓展：扩散模型中的采样工程】**
> Stable Diffusion 从 2022 年发布以来，采样方法从 DDPM 的 1000 步迭代进化到 DDIM、DPM-Solver++ 等只需 20-50 步的方法。核心思想是把扩散 ODE 离散化，用高阶数值方法（如 Runge-Kutta）加速采样。LCM (Latent Consistency Models) 更是将采样压缩到 4-8 步，单张图片生成仅需 0.1 秒。

With NumPy and SciPy, the production versions:

> 使用 NumPy 和 SciPy 的生产版本：

```python
import numpy as np

rng = np.random.default_rng(42)

exponential_samples = rng.exponential(scale=2.0, size=10000)
print(f"Exponential mean: {exponential_samples.mean():.4f} (expected 2.0)")

from scipy import stats
normal = stats.norm(loc=0, scale=1)
print(f"CDF at 1.96: {normal.cdf(1.96):.4f}")
print(f"Inverse CDF at 0.975: {normal.ppf(0.975):.4f}")

logits = np.array([2.0, 1.0, 0.5, 0.1, -1.0])
temperature = 0.7
scaled = logits / temperature
probs = np.exp(scaled - scaled.max()) / np.exp(scaled - scaled.max()).sum()
token = rng.choice(len(logits), p=probs)
print(f"Sampled token index: {token}")
```

For MCMC at scale, use dedicated libraries:
- PyMC: full Bayesian modeling with NUTS (adaptive HMC)
  完整的贝叶斯建模，使用 NUTS（自适应 HMC）
- emcee: ensemble MCMC sampler
  集成 MCMC 采样器
- NumPyro/JAX: GPU-accelerated MCMC
  GPU 加速的 MCMC

You built these from scratch. Now you know what the library calls are doing.

> 你从零构建了这些方法。现在你知道库函数在做什么了。

## Exercises | 练习题

1. Implement inverse CDF sampling for the Cauchy distribution. The CDF is F(x) = 0.5 + arctan(x)/pi. Generate 10,000 samples and plot the histogram against the true PDF. Notice the heavy tails (extreme values far from center).
   实现柯西分布（Cauchy Distribution）的逆 CDF 采样。CDF 为 F(x) = 0.5 + arctan(x)/pi。生成 10,000 个样本并绘制直方图与真实 PDF 对比。注意重尾（远离中心的极端值）。

2. Use rejection sampling to generate samples from a Beta(2, 5) distribution using a Uniform(0, 1) proposal. Plot the accepted samples against the true Beta PDF. What is the theoretical acceptance rate?
   使用拒绝采样从 Beta(2, 5) 分布中生成样本，提议分布使用 Uniform(0, 1)。绘制接受样本与真实 Beta PDF 的对比图。理论接受率是多少？

3. Estimate the integral of sin(x) from 0 to pi using Monte Carlo with 1,000, 10,000, and 100,000 samples. Compare the error at each level. Verify that the error scales as O(1/sqrt(N)).
   使用蒙特卡洛方法估计 sin(x) 在 0 到 pi 上的积分，分别使用 1,000、10,000 和 100,000 个样本。比较各层级的误差。验证误差按 O(1/sqrt(N)) 缩放。

4. Implement Metropolis-Hastings to sample from a 2D distribution p(x, y) proportional to exp(-(x^2 * y^2 + x^2 + y^2 - 8*x - 8*y) / 2). Plot the samples and the chain trajectory. Experiment with different proposal standard deviations.
   实现 Metropolis-Hastings 从 2D 分布 p(x, y) ~ exp(-(x^2*y^2 + x^2 + y^2 - 8x - 8y)/2) 中采样。绘制样本和链的轨迹。尝试不同的提议标准差。

5. Build a complete text generation demo: given a vocabulary of 10 words with logits, generate sequences of 20 tokens using (a) greedy, (b) temperature=0.7, (c) top-k=3, (d) top-p=0.9. Compare the diversity of outputs across 5 runs.
   构建一个完整的文本生成演示：给定 10 个词的词汇表和 logits，使用 (a) 贪心、(b) temperature=0.7、(c) top-k=3、(d) top-p=0.9 生成 20 个 token 的序列。比较 5 次运行的输出多样性。

## Key Terms | 术语速查表

| Term | What people say | What it actually means |
|------|----------------|----------------------|
| Sampling | "Drawing random values" | Generating values according to a probability distribution. The mechanism behind all generative AI |
| Uniform distribution | "All equally likely" | Every value in [a, b] has equal probability density 1/(b-a). The starting point for all sampling methods |
| Inverse CDF | "Probability transform" | F_inverse(U) converts a uniform sample into a sample from any distribution with known CDF. Exact and efficient |
| Rejection sampling | "Propose and accept/reject" | Generate from a simple proposal, accept with probability proportional to target/proposal ratio. Exact but wastes samples |
| Importance sampling | "Reweight samples" | Estimate expectations under p(x) using samples from q(x) by weighting each sample by p(x)/q(x). Core to PPO in RL |
| Monte Carlo | "Average random samples" | Approximate integrals as sample averages. Error O(1/sqrt(N)) regardless of dimension |
| MCMC | "Random walk that converges" | Construct a Markov chain whose stationary distribution is the target. Metropolis-Hastings is the foundational algorithm |
| Metropolis-Hastings | "Accept uphill, sometimes downhill" | Propose moves, accept based on density ratio. Detailed balance ensures convergence to target distribution |
| Gibbs sampling | "One variable at a time" | Update each variable from its conditional distribution holding others fixed. 100% acceptance rate |
| Temperature | "Confidence knob" | Divides logits by T before softmax. T<1 sharpens (more confident), T>1 flattens (more diverse) |
| Top-k sampling | "Keep the k best" | Zero out all but the k highest-probability tokens, renormalize, sample. Fixed candidate set size |
| Nucleus sampling (top-p) | "Keep the probable ones" | Keep the smallest set of tokens whose cumulative probability exceeds p. Adaptive candidate set size |
| Reparameterization trick | "Move randomness outside" | Write z = mu + sigma * epsilon where epsilon ~ N(0,1). Makes sampling differentiable. Essential for VAE training |
| Gumbel-Softmax | "Soft categorical sampling" | Differentiable approximation to categorical sampling using Gumbel noise + softmax with temperature |
| Stratified sampling | "Forced coverage" | Divide sample space into strata, sample from each. Always lower variance than naive Monte Carlo |
| Burn-in | "Warm-up period" | Initial MCMC samples discarded before the chain reaches its stationary distribution |
| Detailed balance | "Reversibility condition" | p(x) * T(x->y) = p(y) * T(y->x). Sufficient condition for p to be the stationary distribution of a Markov chain |
| Diffusion sampling | "Iterative denoising" | Generate data by starting from noise and applying learned denoising steps. Each step is a conditional sampling operation |

## Further Reading | 延伸阅读

- [Holbrook (2023): The Metropolis-Hastings Algorithm](https://arxiv.org/abs/2304.07010) - detailed tutorial on MCMC foundations
- [Jang, Gu, Poole (2017): Categorical Reparameterization with Gumbel-Softmax](https://arxiv.org/abs/1611.01144) - original Gumbel-Softmax paper
- [Holtzman et al. (2020): The Curious Case of Neural Text Degeneration](https://arxiv.org/abs/1904.09751) - nucleus (top-p) sampling paper
- [Kingma & Welling (2014): Auto-Encoding Variational Bayes](https://arxiv.org/abs/1312.6114) - VAE paper introducing the reparameterization trick
- [Ho, Jain, Abbeel (2020): Denoising Diffusion Probabilistic Models](https://arxiv.org/abs/2006.11239) - DDPM connects sampling to image generation
