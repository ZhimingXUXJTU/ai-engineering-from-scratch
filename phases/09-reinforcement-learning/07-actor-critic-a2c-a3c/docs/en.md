# Actor-Critic — A2C and A3C | 演员-评论家 — A2C 与 A3C

> REINFORCE is noisy. Add a critic that learns `V̂(s)`, subtract it from the return, and you get an advantage that has the same expectation but far lower variance. That is actor-critic. A2C runs it synchronously; A3C runs it across threads. Both are the mental model for every modern deep-RL method.

> **【中文解读】** REINFORCE 方差太大。加入一个"评论家"(Critic)学习 V̂(s)，用它作为基线构造优势函数 A = G - V̂(s)，期望不变但方差大幅降低。这就是 Actor-Critic——PPO、SAC 等所有现代深度 RL 方法的架构原型。

**Type:** Build
**Languages:** Python
**Prerequisites:** Phase 9 · 04 (TD Learning), Phase 9 · 06 (REINFORCE)
**Time:** ~75 minutes

## The Problem | 问题引入

Vanilla REINFORCE works, but its variance is terrible. Monte Carlo returns `G_t` can swing over a factor of 10 between episodes. Multiplying that noise by `∇ log π` and averaging produces a gradient estimator that takes thousands of episodes to move the policy the same distance you could move it with far fewer DQN updates.

> 原始 REINFORCE 有效，但方差很糟糕。蒙特卡洛回报 `G_t` 在回合间可能波动 10 倍。将噪声乘以 `∇ log π` 再取平均，产生的梯度估计器需要数千回合才能移动策略——用少得多的 DQN 更新就能达到相同效果。

The variance comes from using raw returns. If you subtract a baseline `b(s_t)` — any function of state, including a learned value — the expectation is unchanged and the variance drops. The best tractable baseline is `V̂(s_t)`. Now the quantity multiplying `∇ log π` is the *advantage*:

`A(s, a) = G - V̂(s)`

> 方差来自使用原始回报。如果减去基线 `b(s_t)`——任何状态函数，包括学习的值——期望不变但方差降低。最佳可用基线是 `V̂(s_t)`。现在乘以 `∇ log π` 的量就是*优势*。

An action is good if it produced above-average return; bad if below. REINFORCE with a learned critic is *actor-critic*. The critic gives the actor a low-variance teacher. This is every deep-policy method after 2015 (A2C, A3C, PPO, SAC, IMPALA).

> 动作好如果产生了高于平均的回报；差如果低于。带学习 critic 的 REINFORCE 就是 *Actor-Critic*。Critic 给 Actor 一个低方差的教师。这是 2015 年后每个深度策略方法（A2C、A3C、PPO、SAC、IMPALA）。

## The Concept | 核心概念

![Actor-critic: policy net plus value net, TD residual as advantage](../assets/actor-critic.svg)

**Two networks, one shared loss:**

> **两个网络，一个共享损失：**

- **Actor** `π_θ(a | s)`: the policy. Sampled to act. Trained with policy gradient.
  **Actor** `π_θ(a | s)`：策略。采样以行动。用策略梯度训练。
- **Critic** `V_φ(s)`: estimates expected return from state. Trained to minimize `(V_φ(s) - target)²`.
  **Critic** `V_φ(s)`：估计从状态出发的期望回报。训练以最小化 `(V_φ(s) - target)²`。

**The advantage.** Two standard forms:

> **优势函数。** 两种标准形式：

- *MC advantage:* `A_t = G_t - V_φ(s_t)`. Unbiased, higher variance.
  *MC 优势：* 无偏，方差较高。
- *TD advantage:* `A_t = r_{t+1} + γ V_φ(s_{t+1}) - V_φ(s_t)`. Biased (uses `V_φ`), far lower variance. Also called the *TD residual* `δ_t`.
  *TD 优势：* 有偏差（使用 `V_φ`），方差远低。也称为 *TD 残差* `δ_t`。

**n-step advantage.** Interpolate between the two:

`A_t^{(n)} = r_{t+1} + γ r_{t+2} + … + γ^{n-1} r_{t+n} + γ^n V_φ(s_{t+n}) - V_φ(s_t)`

`n = 1` is pure TD. `n = ∞` is MC. Most implementations use `n = 5` for Atari, `n = 2048` for PPO on MuJoCo.

> **n 步优势。** 在两者之间插值。`n = 1` 是纯 TD。`n = ∞` 是 MC。大多数实现 Atari 用 `n = 5`，MuJoCo 上的 PPO 用 `n = 2048`。

**Generalized Advantage Estimation (GAE).** Schulman et al. (2016) proposed an exponentially weighted average over all n-step advantages:

`A_t^{GAE} = Σ_{l=0}^{∞} (γλ)^l δ_{t+l}`

with `λ ∈ [0, 1]`. `λ = 0` is TD (low variance, high bias). `λ = 1` is MC (high variance, unbiased). `λ = 0.95` is the 2026 default — tune until the bias/variance dial is where you want it.

> **【中文解读】** GAE（广义优势估计）是 Actor-Critic 的关键改进：通过指数加权平均所有 n 步优势，在偏差和方差之间找到最优平衡。lambda=0 是纯 TD（低方差高偏差），lambda=1 是纯 MC（高方差无偏差），lambda=0.95 是 2026 年默认值。GAE 是 PPO 的核心组件。

> **【拓展：GAE 在 RLHF 中的应用】** ChatGPT 的 PPO 训练使用 GAE 计算优势函数。在 LLM 场景中，"状态"是已生成的 token 序列，"动作"是下一个 token，"奖励"来自奖励模型。GAE 让 PPO 能在长文本生成（数百 token）中稳定训练，平衡即时奖励和长期回报。

**A2C: synchronous advantage actor-critic.** Collect `T` steps across `N` parallel environments. Compute advantages for each step. Update actor and critic on the combined batch. Repeat. The simpler, more-scalable sibling of A3C.

> **A2C：同步优势 Actor-Critic。** 在 `N` 个并行环境中收集 `T` 步。计算每步优势。在合并批次上更新 Actor 和 Critic。重复。A3C 的更简单、更可扩展的兄弟。

**A3C: asynchronous advantage actor-critic.** Mnih et al. (2016). Spawn `N` worker threads, each running an env. Each worker computes gradients locally on its own rollout, then asynchronously applies them to a shared parameter server. No replay buffer needed — workers decorrelate by running different trajectories. A3C proved you could train on CPUs at scale. In 2026, GPU-based A2C (batched parallel envs) dominates because GPUs want large batches.

> **A3C：异步优势 Actor-Critic。** Mnih 等人 (2016)。启动 `N` 个工作线程，每个运行一个环境。每个工作线程在本地计算梯度，然后异步应用到共享参数服务器。不需要回放缓冲区——工作线程通过运行不同轨迹来去相关。2026 年，基于 GPU 的 A2C 占主导，因为 GPU 需要大批量。

**The combined loss.**

`L(θ, φ) = -E[ A_t · log π_θ(a_t | s_t) ]  +  c_v · E[(V_φ(s_t) - G_t)²]  -  c_e · E[H(π_θ(·|s_t))]`

Three terms: policy-gradient loss, value regression, entropy bonus. `c_v ~ 0.5`, `c_e ~ 0.01` are canonical starting points.

> **组合损失。** 三项：策略梯度损失、值回归、熵奖励。`c_v ~ 0.5`、`c_e ~ 0.01` 是典型起始值。

> **【中文解读】** Actor-Critic 的组合损失 = 策略梯度损失 + 值函数回归 + 熵正则化。这三项分别对应：让好的动作概率更大、让 Critic 更准确、防止策略过早坍缩为确定性策略。

> **【拓展：GAE→PPO→RLHF】** GAE (广义优势估计) 是 PPO 的核心组件，而 PPO 是 ChatGPT RLHF 训练的标准算法。λ=0.95 是 2026 年的默认值，在偏差和方差之间取得平衡。理解 GAE 就理解了大模型对齐训练中最关键的优势估计方法。

## Build It | 动手实现

### Step 1: a critic

Linear critic `V_φ(s) = w · features(s)` updated with MSE:

```python
def critic_update(w, x, target, lr):
    v_hat = dot(w, x)
    err = target - v_hat
    for j in range(len(w)):
        w[j] += lr * err * x[j]
    return v_hat
```

On a tabular env the critic converges in a few hundred episodes. On Atari, replace the linear critic with a shared CNN trunk + value head.

> 线性 critic `V_φ(s) = w · features(s)` 用 MSE 更新。在表格环境中几百回合就收敛。在 Atari 上，替换为共享 CNN 主干 + 值头。

### Step 2: n-step advantage

Given a rollout of length `T` and a bootstrapped final `V(s_T)`:

```python
def compute_advantages(rewards, values, gamma=0.99, lam=0.95, last_value=0.0):
    advantages = [0.0] * len(rewards)
    gae = 0.0
    for t in reversed(range(len(rewards))):
        next_v = values[t + 1] if t + 1 < len(values) else last_value
        delta = rewards[t] + gamma * next_v - values[t]
        gae = delta + gamma * lam * gae
        advantages[t] = gae
    returns = [a + v for a, v in zip(advantages, values)]
    return advantages, returns
```

`returns` is the critic target. `advantages` is what multiplies `∇ log π`.

> `returns` 是 critic 目标。`advantages` 是乘以 `∇ log π` 的量。

### Step 3: combined update

```python
for step_i, (x, a, _r, probs) in enumerate(traj):
    adv = advantages[step_i]
    target_v = returns[step_i]

    # critic
    critic_update(w, x, target_v, lr_v)

    # actor
    for i in range(N_ACTIONS):
        grad_logpi = (1.0 if i == a else 0.0) - probs[i]
        for j in range(N_FEAT):
            theta[i][j] += lr_a * adv * grad_logpi * x[j]
```

On-policy, one rollout per update, separate learning rates for actor and critic.

> 在线策略，每次更新一个 rollout，Actor 和 Critic 使用不同学习率。

### Step 4: parallelization (A3C vs A2C)

- **A3C:** spin up `N` threads. Each runs its own env and its own forward pass. Periodically push gradient updates to a shared master. No locks on the master — races are ok, they just add noise.
- **A2C:** run `N` env instances in a single process, stack observations into a `[N, obs_dim]` batch, batched forward pass, batched backward pass. Higher GPU utilization, deterministic, easier to reason about. The default in 2026.

Our toy code is single-threaded for clarity; rewriting to batched A2C is three lines of numpy.

> 我们的玩具代码是单线程的以保持清晰；重写为批量 A2C 只需三行 numpy。

## Pitfalls

- **Critic bias before actor gradient.** If the critic is random, its baseline is uninformative and you are training on pure noise. Warm up the critic for a few hundred steps before turning on the policy gradient, or use a slow actor learning rate.
  **Actor 梯度之前的 Critic 偏差。** 如果 Critic 是随机的，其基线没有信息量，你在纯噪声上训练。在开启策略梯度前先预热 Critic 几百步。
- **Advantage normalization.** Normalize advantages to zero-mean/unit-std per batch. Stabilizes training massively at near-zero cost.
  **优势归一化。** 每批次将优势归一化为零均值/单位标准差。几乎零成本地大幅稳定训练。
- **Shared trunk.** Use a shared feature extractor for actor and critic on image inputs. Separate heads. The shared features free-ride on both losses.
  **共享主干。** 图像输入时使用共享特征提取器。分开的头。共享特征同时从两个损失中获益。
- **On-policy contract.** A2C reuses data for exactly one update. More and your gradient is biased (importance-sampling correction is what PPO adds).
  **在线策略约束。** A2C 恰好用数据做一次更新。更多则梯度有偏差（PPO 添加了重要性采样修正）。
- **Entropy collapse.** Without `c_e > 0`, policy becomes near-deterministic in a few hundred updates and stops exploring.
  **熵坍缩。** 没有 `c_e > 0`，策略在几百次更新后变为近确定性并停止探索。
- **Reward scale.** Advantage magnitudes depend on reward scale. Normalize rewards (e.g., running-std dividing) for consistent gradient magnitudes across tasks.
  **奖励尺度。** 优势量级取决于奖励尺度。归一化奖励以获得跨任务一致的梯度量级。

## Use It | 用框架实现

A2C/A3C are rarely the final choice in 2026 but they are the architecture everything later refines:

> A2C/A3C 在 2026 年很少是最终选择，但它们是后来所有方法精化的架构：

| Method | Relation to A2C |
|--------|----------------|
| Method / 方法 | Relation to A2C / 与 A2C 的关系 |
| PPO | A2C + clipped importance ratio for multi-epoch updates / A2C + 裁剪重要性比率用于多轮更新 |
| IMPALA | A3C + V-trace off-policy correction / A3C + V-trace 离策略修正 |
| SAC (Phase 9 · 07) | Off-policy A2C with a soft-value critic (next lesson) / 离策略 A2C + 软值 Critic |
| GRPO (Phase 9 · 12) | A2C without the critic — group-relative advantage / 无 Critic 的 A2C——组相对优势 |
| DPO | A2C collapsed into a preference-ranking loss, no sampling / 折叠为偏好排名损失的 A2C |
| AlphaStar / OpenAI Five | A2C with league training + imitation pre-training / A2C + 联盟训练 + 模仿预训练 |

If you see "advantage" in a 2026 paper, think actor-critic.

> 如果你在 2026 年的论文中看到"优势"，就想到 Actor-Critic。

## Ship It | 产出物

Save as `outputs/skill-actor-critic-trainer.md`:

```markdown
---
name: actor-critic-trainer
description: Produce an A2C / A3C / GAE configuration for a given environment, with advantage estimation and loss weights specified.
version: 1.0.0
phase: 9
lesson: 7
tags: [rl, actor-critic, gae]
---

Given an environment and compute budget, output:

1. Parallelism. A2C (GPU batched) vs A3C (CPU async) and the number of workers.
2. Rollout length T. Steps per env per update.
3. Advantage estimator. n-step or GAE(λ); specify λ.
4. Loss weights. `c_v` (value), `c_e` (entropy), gradient clip.
5. Learning rates. Actor and critic (separate if using).

Refuse single-worker A2C on environments with horizon > 1000 (too on-policy, too slow). Refuse to ship without advantage normalization. Flag any run with `c_e = 0` and observed entropy < 0.1 as entropy-collapsed.
```

## Exercises | 练习题

1. **Easy.** Train actor-critic with MC advantage (`G_t - V(s_t)`) on 4×4 GridWorld. Compare sample efficiency to REINFORCE-with-running-mean-baseline from Lesson 06.
2. **Medium.** Switch to TD-residual advantage (`r + γ V(s') - V(s)`). Measure variance of the advantage batches. By how much does it drop?
3. **Hard.** Implement GAE(λ). Sweep `λ ∈ {0, 0.5, 0.9, 0.95, 1.0}`. Plot final return vs sample efficiency. Where is the bias/variance sweet spot for this task?

## Key Terms | 术语速查表

| Term | What people say | What it actually means |
|------|-----------------|-----------------------|
| Actor | "The policy net" / 演员（策略网络） | `π_θ(a\|s)`, updated by policy gradient. |
| Critic | "The value net" / 评论家（值网络） | `V_φ(s)`, updated by MSE regression to returns / TD targets. |
| Advantage | "How much better than average" / 优势函数 | `A(s, a) = Q(s, a) - V(s)` or its estimators. Multiplier for `∇ log π`. |
| TD residual | "δ" / TD 残差 | `δ_t = r + γ V(s') - V(s)`; one-step advantage estimate. |
| GAE | "The interpolation knob" / 广义优势估计 | Exponentially weighted sum of n-step advantages, parameterized by `λ`. |
| A2C | "Synchronous actor-critic" / 同步演员-评论家 | Batched across envs; one gradient step per rollout. |
| A3C | "Async actor-critic" / 异步演员-评论家 | Worker threads push gradients to a shared param server. Original paper; less common in 2026. |
| Bootstrap | "Use V at the horizon" / 自举截断 | Truncate the rollout, add `γ^n V(s_{t+n})` to close the sum. |

## Further Reading | 延伸阅读

- [Mnih et al. (2016). Asynchronous Methods for Deep Reinforcement Learning](https://arxiv.org/abs/1602.01783) — A3C, the original async actor-critic paper.
- [Schulman et al. (2016). High-Dimensional Continuous Control Using Generalized Advantage Estimation](https://arxiv.org/abs/1506.02438) — GAE.
- [Sutton & Barto (2018). Ch. 13 — Actor-Critic Methods](http://incompleteideas.net/book/RLbook2020.pdf) — foundations; pair this with Ch. 9 on function approximation when the critic is a neural net.
- [Espeholt et al. (2018). IMPALA](https://arxiv.org/abs/1802.01561) — scalable distributed actor-critic with V-trace off-policy correction.
- [OpenAI Baselines / Stable-Baselines3](https://stable-baselines3.readthedocs.io/) — production A2C/PPO implementations worth reading.
- [Konda & Tsitsiklis (2000). Actor-Critic Algorithms](https://papers.nips.cc/paper/1786-actor-critic-algorithms) — the foundational convergence result for the two-timescale actor-critic decomposition.
