# Sampling Methods | 采样方法

> Sampling is how AI explores the space of possibilities.

**Type:** Build
**Language:** Python
**Prerequisites:** Phase 1, Lessons 06-07 (Probability, Bayes' Theorem)
**Time:** ~120 minutes

## Learning Objectives | 学习目标

- Implement inverse CDF, rejection, and importance sampling from scratch using only uniform random numbers
- Build temperature, top-k, and top-p (nucleus) sampling for language model token generation
- Explain the reparameterization trick and why it enables backpropagation through sampling in VAEs
- Run Metropolis-Hastings MCMC to sample from an unnormalized target distribution


> **【中文解读】** 采样是 AI 探索可能性的方式。LLM 用 temperature/top-k/top-p 控制文本生成多样性。VAE 用重参数化技巧让采样可微。扩散模型的前向过程是采样（加噪），反向过程是去噪（生成）。本节从均匀分布出发，逐步构建所有主流采样方法，直到支撑现代 LLM 和生成模型的核心技术。

## The Problem

A language model finishes processing your prompt and produces a vector of 50,000 logits. One for every token in its vocabulary. Now it has to pick one. How?

If it always picks the highest-probability token, every response is identical. Deterministic. Boring. If it picks uniformly at random, the output is gibberish. The answer lives somewhere between these extremes, and that somewhere is controlled by sampling.

Sampling is not limited to text generation. Reinforcement learning estimates policy gradients by sampling trajectories. VAEs learn latent representations by sampling from learned distributions and backpropagating through the randomness. Diffusion models generate images by sampling noise and iteratively denoising. Monte Carlo methods estimate integrals that have no closed-form solution. MCMC algorithms explore high-dimensional posterior distributions that are impossible to enumerate.

Every generative AI system is a sampling system. The sampling strategy determines the quality, diversity, and controllability of the output. This lesson builds every major sampling method from scratch, starting from uniform random numbers and ending with the techniques that power modern LLMs and generative models.

> **【中文解读】** 核心矛盾：语言模型输出 5 万个 token 的概率分布，但不能总选最高的（无聊）也不能随机选（胡说）。采样策略决定了"创造力"和"准确性"之间的平衡。同样的问题出现在 RL 策略梯度、VAE 潜变量、扩散模型去噪等所有生成场景中——本质上都是在问：如何从概率分布中"聪明地"取样本？

## The Concept

### Why Sampling Matters

Sampling appears in four fundamental roles across AI and machine learning:

**Generation.** Language models, diffusion models, and GANs all produce output by sampling. The sampling algorithm directly controls creativity, coherence, and diversity. Temperature, top-k, and nucleus sampling are the knobs that engineers turn daily.

**Training.** Stochastic gradient descent samples mini-batches. Dropout samples neurons to deactivate. Data augmentation samples random transformations. Importance sampling reweights samples to reduce gradient variance in reinforcement learning (PPO, TRPO).

**Estimation.** Many quantities in ML have no closed-form solution. The expected loss over a data distribution, the partition function of an energy-based model, the evidence in Bayesian inference. Monte Carlo estimation approximates all of these by averaging over samples.

**Exploration.** MCMC algorithms explore posterior distributions in Bayesian inference. Evolutionary strategies sample parameter perturbations. Thompson sampling balances exploration and exploitation in bandits.

The core challenge: you can only sample directly from simple distributions (uniform, normal). For everything else, you need a method to convert simple samples into samples from your target distribution.

> **【中文解读】** 采样在 AI 中扮演四个角色：**生成**（LLM、扩散模型用采样产生输出）、**训练**（SGD 采小批量、Dropout 随机丢弃神经元）、**估计**（用蒙特卡洛逼近无法解析求解的积分和期望）、**探索**（MCMC 在贝叶斯后验中探索高维空间）。所有方法的共同起点：计算机只能直接生成均匀分布或正态分布的样本，其他分布必须通过变换间接获得。

### Uniform Random Sampling

Every sampling method starts here. A uniform random number generator produces values in [0, 1) where every sub-interval of equal length has equal probability.

```
U ~ Uniform(0, 1)

P(a <= U <= b) = b - a    for 0 <= a <= b <= 1

Properties:
  E[U] = 0.5
  Var(U) = 1/12
```

To sample uniformly from a discrete set of n items, generate U and return floor(n * U). To sample from a continuous range [a, b], compute a + (b - a) * U.

The key insight: a single uniform random number contains exactly the right amount of randomness to produce one sample from any distribution. The trick is finding the right transformation.

> **【中文解读】** 均匀分布是一切采样的基石。期望 0.5、方差 1/12。一个 U(0,1) 的随机数恰好包含"恰好够"的随机性来生成任何分布的一个样本——关键在于找到正确的变换函数。从连续区间 [a,b] 采样只需 `a + (b-a)*U`；从离散集合采样用 `floor(n*U)`。

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

**Discrete version:** For discrete distributions, build the CDF as a cumulative sum, generate U, and find the first index where the cumulative sum exceeds U. This is how `sample_categorical` works in Lesson 06.

> **【中文解读】** 逆 CDF 方法的原理：CDF 函数 F(x) 把值映射到 [0,1]，逆函数 F^{-1} 把 [0,1] 映射回值。所以 F^{-1}(U) 就服从目标分布。以指数分布为例，CDF 为 F(x) = 1 - e^{-lambda*x}，反解得 x = -ln(U)/lambda。该方法精确且高效，但前提是必须能写出 F^{-1} 的解析形式——正态分布就不行，需要用 Box-Muller 等其他方法。

### Rejection Sampling

When you cannot invert the CDF but can evaluate the target PDF up to a constant, rejection sampling works.

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

**Example: sampling from a truncated normal.** Use a uniform proposal over the truncated range. The envelope M is the maximum of the normal PDF in that range.

**Example: sampling from a semicircle.** Propose uniformly in the bounding rectangle. Accept if the point falls inside the semicircle. This is how Monte Carlo computes pi: the acceptance rate equals the area ratio pi/4.

> **【中文解读】** 拒绝采样适用于无法求逆 CDF 但能计算目标概率密度的场景。核心思想是"投飞镖再筛选"：从简单的提议分布 q(x) 中采样，以 p(x)/(M*q(x)) 的概率接受。M 越紧贴目标分布，接受率越高（1/M）。致命缺点：高维空间中接受率随维度指数衰减——这就是拒绝采样的"维度灾难"。

> **【拓展：拒绝采样与蒙特卡洛估计 pi】** 在 [-1,1]x[-1,1] 的正方形中均匀投点，落在单位圆内的比例约等于 pi/4（因为圆面积/正方形面积 = pi/4）。这就是经典的蒙特卡洛估计 pi 的方法——本质上是拒绝采样的一种特例。

### Importance Sampling

Sometimes you do not need samples from the target distribution p(x). You need to estimate an expectation under p(x), and you have samples from a different distribution q(x).

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

The variance of the importance sampling estimator depends on how similar q is to p. If q is very different from p, a few samples get enormous weights and dominate the estimate. Self-normalized importance sampling divides by the sum of weights to reduce this problem:

```
E_p[f(x)] ~ sum(w_i * f(x_i)) / sum(w_i)
```

> **【中文解读】** 重要性采样不需要从目标分布 p(x) 中采样——它用另一个分布 q(x) 的样本来估计 p(x) 下的期望，方法是给每个样本加权 w(x) = p(x)/q(x)。在强化学习 PPO 算法中，旧策略采集的轨迹通过重要性加权 `pi_new/pi_old` 来更新新策略，并裁剪权重防止偏离太远。方差取决于 p 和 q 的相似度——差异大时少数样本获得巨大权重，主导估计结果。

### Monte Carlo Estimation

Monte Carlo estimation approximates integrals by averaging random samples. The law of large numbers guarantees convergence.

```
Goal: estimate I = integral of g(x) dx over domain D

Method:
  1. Sample x_1, ..., x_N uniformly from D
  2. I ~ (Volume of D / N) * sum(g(x_i))

Error: O(1 / sqrt(N))   regardless of dimension
```

The error rate is dimension-independent. This is why Monte Carlo methods dominate in high dimensions where grid-based integration is impossible.

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

> **【中文解读】** 蒙特卡洛估计的核心思想：用样本均值逼近积分/期望。大数定律保证收敛，误差为 O(1/sqrt(N))，且与维度无关——这正是蒙特卡洛在高维问题上碾压网格积分的原因。估计 pi 是最经典的例子：在正方形中随机投点，统计落在内切圆中的比例。

### Markov Chain Monte Carlo (MCMC): Metropolis-Hastings

MCMC constructs a Markov chain whose stationary distribution is the target distribution p(x). After enough steps, samples from the chain are (approximately) samples from p(x).

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

**Why it works.** The acceptance rule ensures detailed balance: the probability of being at x and moving to x' equals the probability of being at x' and moving to x. Detailed balance implies that p(x) is the stationary distribution of the chain.

**Practical considerations:**
- Burn-in: discard early samples before the chain reaches equilibrium
- Thinning: keep every k-th sample to reduce autocorrelation
- Proposal scale: too small and the chain moves slowly (high acceptance, slow exploration); too large and most proposals are rejected (low acceptance, stuck in place)
- The optimal acceptance rate for a Gaussian proposal in high dimensions is approximately 0.234

> **【中文解读】** MCMC 构造一条马尔可夫链，使其平稳分布恰好是目标分布 p(x)。Metropolis-Hastings 的流程：从当前位置提议一个新位置 x'，以概率 alpha = p(x')*q(x|x') / [p(x)*q(x'|x)] 接受转移。对称提议（如高斯随机游走）下简化为 p(x')/p(x)——"向上走必接受，向下走有概率接受"。细致平衡条件保证了收敛。实践中需要丢弃预热期（burn-in）的样本，并注意提议步长太大太小都不好。

> **【拓展：为什么 MCMC 如此重要】** 贝叶斯推断中，后验分布通常没有解析解，直接采样也不可能。MCMC 通过构建一条随机游走链来间接探索后验分布，是贝叶斯方法的核心工具。PyMC、Stan 等概率编程库的本质就是在帮你跑 MCMC。

### Gibbs Sampling

Gibbs sampling is a special case of MCMC for multivariate distributions. Instead of proposing a move in all dimensions at once, it updates one variable at a time from its conditional distribution.

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
- Gaussian mixtures: conditionals are Gaussian
- Ising models: each spin's conditional depends only on its neighbors

The acceptance rate is always 1 (every proposal is accepted) because sampling from the exact conditional automatically satisfies detailed balance.

**Limitation.** When variables are highly correlated, Gibbs sampling mixes slowly because updating one variable at a time cannot make large diagonal moves through the distribution.

> **【中文解读】** Gibbs 采样是 MCMC 的特殊情况：每次只更新一个变量（从其条件分布中采样），其余变量固定。由于每次从精确的条件分布采样，接受率永远是 100%。适用于条件分布容易采样的模型（如贝叶斯网络、高斯混合模型）。但变量高度相关时，每次只能沿坐标轴方向小步移动，导致收敛极慢。

### Temperature Sampling (Used in LLMs)

Language models output logits z_1, ..., z_V for each token in the vocabulary. Softmax converts these to probabilities. Temperature rescales the logits before softmax:

```
p_i = exp(z_i / T) / sum(exp(z_j / T))

T = 1.0: standard softmax (original distribution)
T -> 0:  argmax (deterministic, always picks highest logit)
T -> inf: uniform (all tokens equally likely)
T < 1.0: sharpens the distribution (more confident, less diverse)
T > 1.0: flattens the distribution (less confident, more diverse)
```

**Why it works.** Dividing logits by T < 1 amplifies differences between logits. If z_1 = 2 and z_2 = 1, dividing by T = 0.5 gives z_1/T = 4 and z_2/T = 2, making the gap larger. After softmax, the highest-logit token gets a much larger share.

**In practice:**
- T = 0.0: greedy decoding, best for factual Q&A
- T = 0.3-0.7: slightly creative, good for code generation
- T = 0.7-1.0: balanced, good for general conversation
- T = 1.0-1.5: creative writing, brainstorming
- T > 1.5: increasingly random, rarely useful

Temperature does not change which tokens are possible. It changes the probability mass allocated to each token.

> **【中文解读】** Temperature 是 LLM 中最常用的采样控制参数。softmax 前把 logits 除以 T：T<1 放大概率差距（更确定、更保守），T>1 缩小差距（更随机、更多样），T->0 等价于贪心解码（始终选概率最高的）。实践经验：代码生成用 T=0.3-0.7，对话用 T=0.7-1.0，创意写作用 T=1.0-1.5。Temperature 不改变哪些 token 可选，只改变概率分配。

### Top-k Sampling

Top-k sampling restricts the candidate set to the k tokens with the highest probabilities, then renormalizes and samples from that restricted set.

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

> **【中文解读】** Top-k 固定保留概率最高的 k 个 token，重新归一化后采样。k=1 就是贪心，k=词表大小等于不过滤。典型值 k=40 可以过滤掉长尾的低质量 token。缺点：k 是固定的，不适应模型的置信度——模型很确定时仍保留了太多候选，模型不确定时又可能截掉了合理选项。

### Top-p (Nucleus) Sampling

Top-p sampling dynamically adjusts the candidate set size. Instead of keeping a fixed number of tokens, it keeps the smallest set of tokens whose cumulative probability exceeds p.

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

**Common combinations:**
- Temperature 0.7 + top-p 0.9: good general-purpose setting
- Temperature 0.0 (greedy): best for deterministic tasks
- Temperature 1.0 + top-k 50: Fan et al. (2018) original paper setting

Top-k and top-p can be combined. Apply top-k first, then top-p on the remaining set.

> **【中文解读】** Top-p（核采样/Nucleus Sampling）是 Top-k 的升级版：不固定候选数量，而是保留累积概率刚好超过 p 的最小 token 集合。模型自信时只保留 2-3 个 token，不确定时保留上百个——这种自适应性使 top-p 通常比 top-k 效果更好。实际中常用组合：Temperature 0.7 + top-p 0.9。

### Reparameterization Trick (Used in VAEs)

Variational autoencoders (VAEs) learn by encoding inputs into a distribution in latent space, sampling from that distribution, and decoding the sample back. The problem: you cannot backpropagate through a sampling operation.

```
Standard sampling (not differentiable):
  z ~ N(mu, sigma^2)

  The randomness blocks gradient flow.
  d/d_mu [sample from N(mu, sigma^2)] = ???
```

The reparameterization trick separates the randomness from the parameters:

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

**In the VAE training loop:**
1. Encoder outputs mu and log(sigma^2) for each input
2. Sample epsilon ~ N(0, 1)
3. Compute z = mu + sigma * epsilon
4. Decode z to reconstruct the input
5. Backpropagate through steps 4, 3, 2, 1 (possible because step 3 is differentiable)

Without the reparameterization trick, VAEs cannot be trained with standard backpropagation. This single insight made VAEs practical.

> **【中文解读】** VAE 的训练瓶颈：编码器输出分布参数 (mu, sigma)，需要从中采样再送入解码器，但采样操作不可微。重参数化技巧的优雅解法：把随机性"搬"到外部——先从标准正态采样 epsilon，再用 z = mu + sigma * epsilon 构造样本。这样 z 对 mu 的梯度是 1，对 sigma 的梯度是 epsilon，反向传播畅通无阻。这个看似简单的技巧是 VAE 能够端到端训练的关键。

> **【拓展：为什么采样操作不可微】** 采样涉及随机数生成，输出与输入的关系是概率性的而非确定性的。例如 z ~ N(mu, sigma^2) 中，相同的 mu 和 sigma 可以产生不同的 z，所以 dz/dmu 没有定义。重参数化把随机性隔离到 epsilon 中，使 z 成为 mu 和 sigma 的确定性函数。

### Gumbel-Softmax (Differentiable Categorical Sampling)

The reparameterization trick works for continuous distributions (Gaussian). For discrete categorical distributions, we need a different approach. Gumbel-Softmax provides a differentiable approximation to categorical sampling.

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

**Applications:**
- Discrete latent variables in VAEs
- Neural architecture search (choosing discrete operations)
- Hard attention mechanisms
- Reinforcement learning with discrete actions

> **【中文解读】** Gumbel-Softmax 是重参数化技巧在离散分布上的扩展。先用 Gumbel-Max 技巧精确采样（加 Gumbel 噪声后取 argmax），再用 softmax 替代不可微的 argmax 实现可微近似。温度参数 tau 控制连续性：tau->0 趋近 one-hot（硬采样），tau->inf 趋近均匀分布。应用于离散潜变量 VAE、神经架构搜索和硬注意力机制。

### Stratified Sampling

Standard Monte Carlo sampling can leave gaps in the sample space by chance. Stratified sampling forces even coverage by dividing the space into strata and sampling from each.

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

```
Var(stratified) <= Var(standard Monte Carlo)

The improvement is largest when f(x) varies smoothly.
For piecewise-constant functions, stratified sampling is exact.
```

**Applications:**
- Numerical integration (quasi-Monte Carlo)
- Training data splits (ensuring class balance in each fold)
- Importance sampling with stratification (combining both techniques)
- NeRF (Neural Radiance Fields) uses stratified sampling along camera rays

> **【中文解读】** 分层采样强制样本均匀覆盖空间：将采样域划分为 N 个等分层，每层内采一个点。由于保证了每个区域都有代表，方差永远不高于朴素蒙特卡洛。NeRF 中沿相机光线使用分层采样来保证射线方向上的覆盖均匀性。

### Connection to Diffusion Models

Diffusion models generate images through a sampling process. The forward process adds Gaussian noise to an image over T steps until it becomes pure noise. The reverse process learns to denoise, recovering the original image step by step.

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
- The noise schedule {alpha_t} controls a form of temperature annealing
- Training uses Monte Carlo estimation to approximate the ELBO (evidence lower bound)
- Ancestral sampling in diffusion models is a Markov chain (each step depends only on the current state)

The entire image generation process is iterative sampling: start from noise, and at each step, sample a slightly less noisy version conditioned on the learned denoising model.

> **【中文解读】** 扩散模型把图像生成完全变成了采样过程：前向过程逐步加噪直到变成纯噪声，反向过程逐步去噪恢复图像。每一步去噪都使用了重参数化技巧（采样噪声再施加确定性变换），噪声调度表 {alpha_t} 控制着类似温度退火的效果，训练用蒙特卡洛估计 ELBO，整个生成过程本身是一条马尔可夫链。

## Build It

### Step 1: Uniform and inverse CDF sampling

```python
import math
import random

def sample_uniform(a, b):
    return a + (b - a) * random.random()

def sample_exponential_inverse_cdf(lam):
    u = random.random()
    return -math.log(u) / lam
```

Generate 10,000 exponential samples and verify the mean is 1/lambda.

### Step 2: Rejection sampling

```python
def rejection_sample(target_pdf, proposal_sample, proposal_pdf, M):
    while True:
        x = proposal_sample()
        u = random.random()
        if u < target_pdf(x) / (M * proposal_pdf(x)):
            return x
```

Use rejection sampling to draw from a truncated normal distribution. Verify the shape by histogramming the samples.

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
    x = x0
    for i in range(n_samples + burn_in):
        x_new = proposal_sample(x)
        log_alpha = (target_log_pdf(x_new) + proposal_log_pdf(x, x_new)
                     - target_log_pdf(x) - proposal_log_pdf(x_new, x))
        if math.log(random.random()) < log_alpha:
            x = x_new
        if i >= burn_in:
            samples.append(x)
    return samples
```

Sample from a bimodal distribution (mixture of two Gaussians). Visualize the chain's trajectory.

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
    scaled = [z / temperature for z in logits]
    probs = softmax(scaled)
    return sample_from_probs(probs)
```

Show how temperature changes the output distribution for a set of token logits.

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
    epsilon = random.gauss(0, 1)
    return mu + sigma * epsilon

def reparam_gradient(mu, sigma, epsilon):
    dz_dmu = 1.0
    dz_dsigma = epsilon
    return dz_dmu, dz_dsigma
```

Demonstrate that gradients flow through the reparameterized sample but not through direct sampling.

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

Full implementations with all visualizations are in `code/sampling.py`.

> **【中文解读】** 代码实现按难度递进：从均匀分布和逆 CDF 采样（最基础）开始，到拒绝采样和重要性采样（间接采样），再到 MCMC（Metropolis-Hastings 和 Gibbs），最后是 LLM 相关的 temperature/top-k/top-p 和 VAE 相关的重参数化/Gumbel-Softmax。每一步都用纯 Python 从零实现，让你理解库函数背后真正在做什么。

## Use It

With NumPy and SciPy, the production versions:

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
- emcee: ensemble MCMC sampler
- NumPyro/JAX: GPU-accelerated MCMC

You built these from scratch. Now you know what the library calls are doing.

> **【中文解读】** 生产环境中用 NumPy/SciPy 一行就能完成我们手写的采样。`rng.exponential()`、`stats.norm.cdf()`、`stats.norm.ppf()` 分别对应指数分布采样、CDF 计算和逆 CDF 计算。LLM 的 temperature 采样只需对 logits 除以 T 再做 softmax。大规模 MCMC 推荐使用 PyMC（贝叶斯建模）、emcee（集成采样）或 NumPyro/JAX（GPU 加速）。

## Exercises

1. Implement inverse CDF sampling for the Cauchy distribution. The CDF is F(x) = 0.5 + arctan(x)/pi. Generate 10,000 samples and plot the histogram against the true PDF. Notice the heavy tails (extreme values far from center).
   > **中文：** 实现柯西分布的逆 CDF 采样。CDF 为 F(x) = 0.5 + arctan(x)/pi。生成 10,000 个样本，绘制直方图并与真实 PDF 对比。注意其重尾特性（远离中心的极端值频繁出现）。

2. Use rejection sampling to generate samples from a Beta(2, 5) distribution using a Uniform(0, 1) proposal. Plot the accepted samples against the true Beta PDF. What is the theoretical acceptance rate?
   > **中文：** 用拒绝采样从 Beta(2,5) 分布生成样本，提议分布用 Uniform(0,1)。绘制接受样本与真实 Beta PDF 的对比图。理论接受率是多少？

3. Estimate the integral of sin(x) from 0 to pi using Monte Carlo with 1,000, 10,000, and 100,000 samples. Compare the error at each level. Verify that the error scales as O(1/sqrt(N)).
   > **中文：** 用蒙特卡洛方法估计 sin(x) 在 [0, pi] 上的积分，分别用 1000、10000、100000 个样本。比较各层级的误差，验证误差按 O(1/sqrt(N)) 缩放。

4. Implement Metropolis-Hastings to sample from a 2D distribution p(x, y) proportional to exp(-(x^2 * y^2 + x^2 + y^2 - 8*x - 8*y) / 2). Plot the samples and the chain trajectory. Experiment with different proposal standard deviations.
   > **中文：** 实现 Metropolis-Hastings 从二维分布 p(x,y) 正比于 exp(-(x^2*y^2 + x^2 + y^2 - 8x - 8y)/2) 中采样。绘制样本和链的轨迹。尝试不同的提议标准差。

5. Build a complete text generation demo: given a vocabulary of 10 words with logits, generate sequences of 20 tokens using (a) greedy, (b) temperature=0.7, (c) top-k=3, (d) top-p=0.9. Compare the diversity of outputs across 5 runs.
   > **中文：** 构建完整的文本生成演示：给定 10 个词的词表和 logits，用 (a) 贪心、(b) temperature=0.7、(c) top-k=3、(d) top-p=0.9 分别生成 20 个 token 的序列。比较 5 次运行的输出多样性。

## Key Terms

| Term | What people say | What it actually means | 中文释义 |
|------|----------------|----------------------|---------|
| Sampling | "Drawing random values" | Generating values according to a probability distribution. The mechanism behind all generative AI | 采样：按概率分布生成随机值，所有生成式 AI 的底层机制 |
| Uniform distribution | "All equally likely" | Every value in [a, b] has equal probability density 1/(b-a). The starting point for all sampling methods | 均匀分布：所有值等概率出现，一切采样方法的起点 |
| Inverse CDF | "Probability transform" | F_inverse(U) converts a uniform sample into a sample from any distribution with known CDF. Exact and efficient | 逆 CDF 法：用均匀样本通过逆累积分布函数变换为目标分布样本 |
| Rejection sampling | "Propose and accept/reject" | Generate from a simple proposal, accept with probability proportional to target/proposal ratio. Exact but wastes samples | 拒绝采样：从简单分布提议，按概率比例接受，精确但浪费样本 |
| Importance sampling | "Reweight samples" | Estimate expectations under p(x) using samples from q(x) by weighting each sample by p(x)/q(x). Core to PPO in RL | 重要性采样：用 q(x) 的样本加权估计 p(x) 下的期望，PPO 的核心 |
| Monte Carlo | "Average random samples" | Approximate integrals as sample averages. Error O(1/sqrt(N)) regardless of dimension | 蒙特卡洛：用样本均值逼近积分，误差与维度无关 |
| MCMC | "Random walk that converges" | Construct a Markov chain whose stationary distribution is the target. Metropolis-Hastings is the foundational algorithm | 马尔可夫链蒙特卡洛：构造收敛到目标分布的随机游走 |
| Metropolis-Hastings | "Accept uphill, sometimes downhill" | Propose moves, accept based on density ratio. Detailed balance ensures convergence to target distribution | MH 算法：提议移动，按密度比决定接受，细致平衡保证收敛 |
| Gibbs sampling | "One variable at a time" | Update each variable from its conditional distribution holding others fixed. 100% acceptance rate | Gibbs 采样：每次从条件分布更新一个变量，100% 接受率 |
| Temperature | "Confidence knob" | Divides logits by T before softmax. T<1 sharpens (more confident), T>1 flattens (more diverse) | 温度：softmax 前缩放 logits，控制输出的确定性程度 |
| Top-k sampling | "Keep the k best" | Zero out all but the k highest-probability tokens, renormalize, sample. Fixed candidate set size | Top-k 采样：只保留概率最高的 k 个 token |
| Nucleus sampling (top-p) | "Keep the probable ones" | Keep the smallest set of tokens whose cumulative probability exceeds p. Adaptive candidate set size | 核采样(top-p)：保留累积概率超过 p 的最小 token 集合 |
| Reparameterization trick | "Move randomness outside" | Write z = mu + sigma * epsilon where epsilon ~ N(0,1). Makes sampling differentiable. Essential for VAE training | 重参数化技巧：把随机性移到外部，使采样可微分 |
| Gumbel-Softmax | "Soft categorical sampling" | Differentiable approximation to categorical sampling using Gumbel noise + softmax with temperature | Gumbel-Softmax：离散分布的可微采样近似 |
| Stratified sampling | "Forced coverage" | Divide sample space into strata, sample from each. Always lower variance than naive Monte Carlo | 分层采样：强制覆盖每个区域，方差永远不高于朴素蒙特卡洛 |
| Burn-in | "Warm-up period" | Initial MCMC samples discarded before the chain reaches its stationary distribution | 预热期：丢弃链达到平稳分布前的初始样本 |
| Detailed balance | "Reversibility condition" | p(x) * T(x->y) = p(y) * T(y->x). Sufficient condition for p to be the stationary distribution of a Markov chain | 细致平衡：保证平稳分布的充分条件 |
| Diffusion sampling | "Iterative denoising" | Generate data by starting from noise and applying learned denoising steps. Each step is a conditional sampling operation | 扩散采样：从噪声出发迭代去噪生成数据 |

## Further Reading

- [Holbrook (2023): The Metropolis-Hastings Algorithm](https://arxiv.org/abs/2304.07010) - detailed tutorial on MCMC foundations
- [Jang, Gu, Poole (2017): Categorical Reparameterization with Gumbel-Softmax](https://arxiv.org/abs/1611.01144) - original Gumbel-Softmax paper
- [Holtzman et al. (2020): The Curious Case of Neural Text Degeneration](https://arxiv.org/abs/1904.09751) - nucleus (top-p) sampling paper
- [Kingma & Welling (2014): Auto-Encoding Variational Bayes](https://arxiv.org/abs/1312.6114) - VAE paper introducing the reparameterization trick
- [Ho, Jain, Abbeel (2020): Denoising Diffusion Probabilistic Models](https://arxiv.org/abs/2006.11239) - DDPM connects sampling to image generation
