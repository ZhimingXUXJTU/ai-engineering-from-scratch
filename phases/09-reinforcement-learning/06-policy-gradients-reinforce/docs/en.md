# Policy Gradient — REINFORCE from Scratch | 策略梯度 — 从零实现REINFORCE

> Stop estimating value. Parameterize the policy directly, compute the gradient of expected return, step uphill. Williams (1992) wrote it in one theorem. It is why PPO, GRPO, and every LLM RL loop exist.

> **【中文解读】** 不再估计值函数，直接参数化策略 π_θ(a|s)，计算期望回报的梯度并梯度上升。REINFORCE 定理告诉我们：`∇J(θ) = E[G · ∇log π_θ(a|s)]`。这是 PPO、GRPO、以及所有大模型 RL 训练循环存在的理由。

**Type:** Build | **类型:** 动手
**Languages:** Python | **语言:** Python
**Prerequisites:** Phase 3 · 03 (Backpropagation), Phase 9 · 03 (Monte Carlo), Phase 9 · 04 (TD Learning) | **前置知识:** Phase 3 · 03 (反向传播), Phase 9 · 03 (蒙特卡洛), Phase 9 · 04 (TD 学习)
**Time:** ~75 minutes | **时间:** ~75 分钟

## The Problem | 问题引入

Q-learning and DQN parameterize the *value* function. You pick actions by `argmax Q`. That is fine for discrete actions and discrete states. It breaks when actions are continuous (which `argmax` over a 10-dimensional torque?) or when you want a stochastic policy (`argmax` is deterministic by construction).

> Q-learning 和 DQN 参数化*值*函数。通过 `argmax Q` 选择动作。这对离散动作和离散状态没问题。但当动作连续时（10 维力矩上取哪个 `argmax`？）或需要随机策略时（`argmax` 天然是确定性的），就崩溃了。

Policy gradients parameterize the *policy* instead. `π_θ(a | s)` is a neural net that outputs a distribution over actions. Sample from it to act. Compute the gradient of expected return with respect to `θ`. Step uphill. No `argmax`. No Bellman recursion. Just gradient ascent on `J(θ) = E_{π_θ}[G]`.

> 策略梯度改为参数化*策略*。`π_θ(a | s)` 是一个输出动作分布的神经网络。从中采样来行动。计算期望回报关于 `θ` 的梯度。往上走。不需要 `argmax`。不需要 Bellman 递推。就是在 `J(θ) = E_{π_θ}[G]` 上做梯度上升。

The REINFORCE theorem (Williams 1992) tells you this gradient is computable: `∇J(θ) = E_π[ G · ∇_θ log π_θ(a | s) ]`. Run an episode. Compute the return. Multiply by `∇ log π_θ(a | s)` at every step. Average. Gradient-ascent. Done.

> REINFORCE 定理（Williams 1992）告诉我们这个梯度是可计算的：`∇J(θ) = E_π[ G · ∇_θ log π_θ(a | s) ]`。运行一个回合。计算回报。每步乘以 `∇ log π_θ(a | s)`。取平均。梯度上升。完成。

Every LLM-RL algorithm in 2026 — PPO, DPO, GRPO — is a refinement of REINFORCE. Understanding it in your fingers is the prerequisite for the rest of this phase, and for Phase 10 · 07 (RLHF implementation) and Phase 10 · 08 (DPO).

> 2026 年每个 LLM-RL 算法——PPO、DPO、GRPO——都是 REINFORCE 的精化。将其掌握到肌肉记忆是本阶段剩余部分以及 Phase 10 · 07（RLHF 实现）和 Phase 10 · 08（DPO）的前提。

> **【中文解读】** 策略梯度的核心思想：直接优化策略参数 θ，让高回报的动作概率增大、低回报的动作概率减小。`∇log π` 就是"策略的方向导数"，乘以回报 G 就是"沿着好的方向走"。

> **【拓展：PPO→ChatGPT对齐】** ChatGPT 的 RLHF 训练使用的 PPO 算法，本质上就是 REINFORCE + critic 基线 + 信赖域裁剪。`loss = -advantage * log_prob` 这一行代码，出现在几乎所有 2026 年的大模型 RL 训练脚本中。DeepSeek-R1 的 GRPO 则是用组均值替代 critic 基线的 REINFORCE。

## The Concept | 核心概念

![Policy gradient: softmax policy, log-π gradient, return-weighted update](../assets/policy-gradient.svg)

**The policy gradient theorem.** For any policy `π_θ` parameterized by `θ`:

`∇J(θ) = E_{τ ~ π_θ}[ Σ_{t=0}^{T} G_t · ∇_θ log π_θ(a_t | s_t) ]`

where `G_t = Σ_{k=t}^{T} γ^{k-t} r_{k+1}` is the discounted return from step `t`. The expectation is over full trajectories `τ` sampled from `π_θ`.

> **策略梯度定理。** 对任何由 `θ` 参数化的策略 `π_θ`，期望回报的梯度等于：返回的折扣和乘以对数策略梯度的期望。期望在从 `π_θ` 采样的完整轨迹上取。

**The proof is short.** Differentiate `J(θ) = Σ_τ P(τ; θ) G(τ)` under the expectation. Use `∇P(τ; θ) = P(τ; θ) ∇ log P(τ; θ)` (the log-derivative trick). Factor `log P(τ; θ) = Σ log π_θ(a_t | s_t) + environment terms that do not depend on θ`. The environment terms vanish. Two lines of algebra give you the theorem.

> **证明很短。** 在期望下对 `J(θ)` 求导。使用对数导数技巧。将 `log P(τ; θ)` 分解为策略项和环境项。环境项消失。两行代数就得到定理。

**Variance reduction tricks.** Vanilla REINFORCE has murderous variance — returns are noisy, `∇ log π` is noisy, their product is very noisy. Two standard fixes:

> **方差降低技巧。** 原始 REINFORCE 有极大的方差——回报有噪声，`∇ log π` 有噪声，它们的乘积噪声更大。两种标准修复：

1. **Baseline subtraction.** Replace `G_t` with `G_t - b(s_t)` for any baseline `b(s_t)` that does not depend on `a_t`. Unbiased because `E[b(s_t) · ∇ log π(a_t | s_t)] = 0`. Typical choice: `b(s_t) = V̂(s_t)` learned by a critic → actor-critic (Lesson 07).
   **基线减法。** 用 `G_t - b(s_t)` 替换 `G_t`。典型选择：`b(s_t) = V̂(s_t)` 由 critic 学习 → Actor-Critic（Lesson 07）。
2. **Reward-to-go.** Replace `Σ_t G_t · ∇ log π_θ(a_t | s_t)` with `Σ_t G_t^{from t} · ∇ log π_θ(a_t | s_t)`. Only future returns matter for a given action — past rewards contribute zero-mean noise.
   **未来回报。** 只有未来的回报对给定动作有意义——过去的奖励贡献零均值噪声。

Combined, you get:

`∇J ≈ (1/N) Σ_{i=1}^{N} Σ_{t=0}^{T_i} [ G_t^{(i)} - V̂(s_t^{(i)}) ] · ∇_θ log π_θ(a_t^{(i)} | s_t^{(i)})`

which is REINFORCE with a baseline — the direct ancestor of A2C (Lesson 07) and PPO (Lesson 08).

**Softmax policy parameterization.** For discrete actions, the standard choice:

`π_θ(a | s) = exp(f_θ(s, a)) / Σ_{a'} exp(f_θ(s, a'))`

where `f_θ` is any neural net that outputs a score per action. The gradient has a clean form:

`∇_θ log π_θ(a | s) = ∇_θ f_θ(s, a) - Σ_{a'} π_θ(a' | s) ∇_θ f_θ(s, a')`

i.e., score of the taken action minus its expected value under the policy.

> **Softmax 策略参数化。** 对离散动作，梯度形式简洁：所取动作的分数减去策略下的期望值。

**Gaussian policy for continuous actions.** `π_θ(a | s) = N(μ_θ(s), σ_θ(s))`. `∇ log N(a; μ, σ)` has a closed form. That is all Phase 9 · 07's SAC needs.

> **连续动作的高斯策略。** `∇ log N(a; μ, σ)` 有闭式解。这就是 Phase 9 · 07 的 SAC 所需的全部。

## Build It | 动手实现

### Step 1: softmax policy network

```python
def policy_logits(theta, state_features):
    return [dot(theta[a], state_features) for a in range(N_ACTIONS)]

def softmax(logits):
    m = max(logits)
    exps = [exp(l - m) for l in logits]
    Z = sum(exps)
    return [e / Z for e in exps]
```

Use a linear policy (one weight vector per action) for a tabular env. For Atari, swap in a CNN and keep the softmax head.

> 表格环境使用线性策略（每个动作一个权重向量）。对 Atari，换入 CNN 并保留 softmax 头。

### Step 2: sampling and log-probability

```python
def sample_action(probs, rng):
    x = rng.random()
    cum = 0
    for a, p in enumerate(probs):
        cum += p
        if x <= cum:
            return a
    return len(probs) - 1

def log_prob(probs, a):
    return log(probs[a] + 1e-12)
```

### Step 3: rollout with log-probs captured

```python
def rollout(theta, env, rng, gamma):
    trajectory = []
    s = env.reset()
    while not done:
        logits = policy_logits(theta, s)
        probs = softmax(logits)
        a = sample_action(probs, rng)
        s_next, r, done = env.step(s, a)
        trajectory.append((s, a, r, probs))
        s = s_next
    return trajectory
```

### Step 4: REINFORCE update

```python
def reinforce_step(theta, trajectory, gamma, lr, baseline=0.0):
    returns = compute_returns(trajectory, gamma)
    for (s, a, _, probs), G in zip(trajectory, returns):
        advantage = G - baseline
        grad_log_pi_a = [-p for p in probs]
        grad_log_pi_a[a] += 1.0
        for i in range(N_ACTIONS):
            for j in range(len(s)):
                theta[i][j] += lr * advantage * grad_log_pi_a[i] * s[j]
```

The gradient `∇ log π(a|s) = e_a - π(·|s)` (onehot of `a` minus probabilities) is the heart of softmax policy gradients. Burn it into muscle memory.

> 梯度 `∇ log π(a|s) = e_a - π(·|s)`（`a` 的 one-hot 减去概率）是 softmax 策略梯度的核心。将其刻入肌肉记忆。

### Step 5: baselines

A running mean of `G` over recent episodes is enough variance reduction to get a 4×4 GridWorld running; it takes ~500 episodes to converge. Upgrade the baseline to a learned `V̂(s)` and you get actor-critic.

> 最近回合中 `G` 的运行均值足以让 4×4 GridWorld 工作；约 500 回合收敛。将基线升级为学习的 `V̂(s)` 就得到 Actor-Critic。

## Pitfalls

- **Exploding gradients.** Returns can be huge. Always normalize `G` to `~N(0, 1)` across the batch before multiplying by `∇ log π`.
  **梯度爆炸。** 回报可能很大。在乘以 `∇ log π` 之前始终将 `G` 归一化到 `~N(0, 1)`。
- **Entropy collapse.** The policy converges to a near-deterministic action too early, stops exploring, gets stuck. Fix: add entropy bonus `β · H(π(·|s))` to the objective.
  **熵坍缩。** 策略过早收敛到近确定性动作，停止探索，陷入困境。修复：向目标添加熵奖励 `β · H(π(·|s))`。
- **High variance.** Vanilla REINFORCE needs thousands of episodes. A critic baseline (Lesson 07) or TRPO/PPO's trust region (Lesson 08) is the standard fix.
  **高方差。** 原始 REINFORCE 需要数千回合。Critic 基线（Lesson 07）或 TRPO/PPO 的信赖域（Lesson 08）是标准修复。
- **Sample inefficiency.** On-policy means you throw away every transition after one update. Off-policy corrections via importance sampling bring back data, at the cost of variance (PPO's ratio is a clipped IS weight).
  **样本效率低。** 在线策略意味着每次更新后丢弃所有转移。通过重要性采样的离策略修正可以恢复数据，代价是方差。
- **Non-stationary gradients.** The same gradient from 100 episodes ago uses old `π`. On-policy methods update every few rollouts for this reason.
  **非平稳梯度。** 100 回合前的梯度使用旧的 `π`。在线策略方法因此每隔几个 rollout 更新一次。
- **Credit assignment.** Without reward-to-go, past rewards contribute noise. Always use reward-to-go.
  **信用分配。** 没有未来回报，过去的奖励贡献噪声。始终使用未来回报。

## Use It | 用框架实现

In 2026, REINFORCE is rarely run directly but its gradient formula is everywhere:

> 2026 年，REINFORCE 很少直接运行，但其梯度公式无处不在：

| Use case | Derived method |
|----------|---------------|
| Use case / 用例 | Derived method / 派生方法 |
| Continuous control / 连续控制 | PPO / SAC with Gaussian policy / 高斯策略的 PPO/SAC |
| LLM RLHF / LLM RLHF | PPO with KL penalty, running on token-level policy / 带 KL 惩罚的 PPO，token 级策略 |
| LLM reasoning (DeepSeek) / LLM 推理 | GRPO — REINFORCE with group-relative baseline, no critic / 组相对基线的 REINFORCE，无 critic |
| Multi-agent / 多智能体 | Centralized-critic REINFORCE (MADDPG, COMA) / 集中 critic 的 REINFORCE |
| Discrete action robotics / 离散动作机器人 | A2C, A3C, PPO |
| Preference-only settings / 仅偏好设置 | DPO — REINFORCE rewritten as a preference-likelihood loss, no sampling / 重写为偏好似然损失的 REINFORCE |

When you read `loss = -advantage * log_prob` in a 2026 training script, that is REINFORCE with a baseline. Entire papers (DPO, GRPO, RLOO) are variance-reduction tricks on top of this one line.

> 当你在 2026 年的训练脚本中读到 `loss = -advantage * log_prob`，那就是带基线的 REINFORCE。整篇论文（DPO、GRPO、RLOO）都是在这行代码之上的方差降低技巧。

## Ship It | 产出物

Save as `outputs/skill-policy-gradient-trainer.md`:

```markdown
---
name: policy-gradient-trainer
description: Produce a REINFORCE / actor-critic / PPO training config for a given task and diagnose variance issues.
version: 1.0.0
phase: 9
lesson: 6
tags: [rl, policy-gradient, reinforce]
---

Given an environment (discrete / continuous actions, horizon, reward stats), output:

1. Policy head. Softmax (discrete) or Gaussian (continuous) with parameter counts.
2. Baseline. None (vanilla), running mean, learned `V̂(s)`, or A2C critic.
3. Variance controls. Reward-to-go on by default, return normalization, gradient clip value.
4. Entropy bonus. Coefficient β and decay schedule.
5. Batch size. Episodes per update; on-policy data freshness contract.

Refuse REINFORCE-no-baseline on horizons > 500 steps. Refuse continuous-action control with a softmax head. Flag any run with `β = 0` and observed policy entropy < 0.1 as entropy-collapsed.
```

## Exercises | 练习题

1. **Easy.** Implement REINFORCE on 4×4 GridWorld with a linear softmax policy. Train for 1,000 episodes without a baseline. Plot the learning curve; measure variance (std of returns).
2. **Medium.** Add a running-mean baseline. Train again. Compare sample efficiency and variance to the vanilla run. By how much does the baseline reduce steps to convergence?
3. **Hard.** Add an entropy bonus `β · H(π)`. Sweep `β ∈ {0, 0.01, 0.1, 1.0}`. Plot final return and policy entropy. Where is the sweet spot on this task?

## Key Terms | 术语速查表

| Term | What people say | What it actually means |
|------|-----------------|-----------------------|
| Policy gradient | "Train the policy directly" / 策略梯度 | `∇J(θ) = E[G · ∇ log π_θ(a\|s)]`; derived from the log-derivative trick. |
| REINFORCE | "The original PG algorithm" / REINFORCE算法 | Williams (1992); Monte Carlo returns multiplied by log-policy gradient. |
| Log-derivative trick | "Score function estimator" / 对数导数技巧 | `∇P(τ;θ) = P(τ;θ) · ∇ log P(τ;θ)`; makes gradients of expectations tractable. |
| Baseline | "Variance reduction" / 基线 | Any `b(s)` subtracted from `G`; unbiased because `E[b · ∇ log π] = 0`. |
| Reward-to-go | "Only future returns count" / 未来回报 | `G_t^{from t}` instead of the full `G_0`; correct and lower-variance. |
| Entropy bonus | "Encourage exploration" / 熵正则化 | `+β · H(π(·\|s))` term keeps the policy from collapsing. |
| On-policy | "Train on what you just saw" / 在线策略 | Gradient expectation is w.r.t. the current policy — cannot reuse old data directly. |
| Advantage | "How much better than average" / 优势函数 | `A(s, a) = G(s, a) - V(s)`; the signed quantity REINFORCE-with-baseline multiplies. |

## Further Reading | 延伸阅读

- [Williams (1992). Simple Statistical Gradient-Following Algorithms for Connectionist Reinforcement Learning](https://link.springer.com/article/10.1007/BF00992696) — the original REINFORCE paper.
- [Sutton et al. (2000). Policy Gradient Methods for Reinforcement Learning with Function Approximation](https://papers.nips.cc/paper_files/paper/1999/hash/464d828b85b0bed98e80ade0a5c43b0f-Abstract.html) — the modern policy-gradient theorem with function approximation.
- [Sutton & Barto (2018). Ch. 13 — Policy Gradient Methods](http://incompleteideas.net/book/RLbook2020.pdf) — textbook presentation.
- [OpenAI Spinning Up — VPG / REINFORCE](https://spinningup.openai.com/en/latest/algorithms/vpg.html) — clear pedagogical exposition with PyTorch code.
- [Peters & Schaal (2008). Reinforcement Learning of Motor Skills with Policy Gradients](https://homes.cs.washington.edu/~todorov/courses/amath579/reading/PolicyGradient.pdf) — variance-reduction and the natural-gradient view that connects REINFORCE to the trust-region family (TRPO, PPO).
