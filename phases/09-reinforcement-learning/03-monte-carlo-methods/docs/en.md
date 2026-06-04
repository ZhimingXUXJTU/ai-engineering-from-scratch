# Monte Carlo Methods — Learning from Complete Episodes | 蒙特卡洛方法 — 从完整回合中学习

> Dynamic programming needs a model. Monte Carlo needs nothing but episodes. Run the policy, watch the returns, average them. The simplest idea in RL — and the one that unlocks everything downstream.

> **【中文解读】** 动态规划需要已知环境模型，蒙特卡洛只需要完整的回合数据：执行策略、观测回报、取平均。这是 RL 中最简单的思想，也是所有后续算法（TD、Q-learning、PPO、RLHF）的基石。

**Type:** Build
**Languages:** Python
**Prerequisites:** Phase 9 · 01 (MDPs), Phase 9 · 02 (Dynamic Programming)
**Time:** ~75 minutes

## The Problem | 问题引入

Dynamic programming is elegant, but it assumes you can query `P(s' | s, a)` for every state and action. Almost nothing in the real world works that way. A robot cannot analytically compute the distribution over camera pixels after a joint torque. A pricing algorithm cannot integrate over every possible customer reaction. An LLM cannot enumerate all possible continuations after a token.

You need a method that only needs the ability to *sample* from the environment. Run the policy. Get a trajectory `s_0, a_0, r_1, s_1, a_1, r_2, …, s_T`. Use it to estimate values. That is Monte Carlo.

The shift from DP to MC is philosophically important: we move from *known model + exact backup* to *sampled rollouts + averaged return*. The variance jumps, but the applicability explodes. Every RL algorithm after this lesson — TD, Q-learning, REINFORCE, PPO, GRPO — is a Monte Carlo estimator at heart, sometimes with bootstrapping layered on top.

> **【中文解读】** 从 DP 到 MC 的核心转变：从"已知模型+精确计算"到"采样轨迹+平均回报"。方差增大了，但适用范围爆炸式扩展。PPO、RLHF 本质上都是 MC 估计器的变体。

> **【拓展：LLM中的MC】** ChatGPT 的 RLHF 训练中，对每个 prompt 采样多个回答、计算平均奖励——这就是 MC 思想在大模型训练中的直接应用。DeepSeek-R1 的 GRPO 也是基于组内采样的 MC 估计。

## The Concept | 核心概念

![Monte Carlo: rollout, compute returns, average; first-visit vs every-visit](../assets/monte-carlo.svg)

**The core idea, in one line:** `V^π(s) = E_π[G_t | s_t = s] ≈ (1/N) Σ_i G^{(i)}(s)` where `G^{(i)}(s)` are observed returns following visits to `s` under policy `π`.

> **【中文解读】** MC 评估的核心：状态值 = 多次经过该状态时观测到的回报的平均值。首次访问 MC 只统计每个回合中第一次访问的回报，每次访问 MC 统计所有访问。增量式均值更新 `V_new = V_old + α(target - V_old)` 是从 MC 到 TD 到所有现代 RL 算法的桥梁。

**First-visit vs every-visit MC.** Given an episode that visits state `s` multiple times, first-visit MC only counts the return from the first visit; every-visit MC counts all visits. Both are unbiased in the limit. First-visit is simpler to analyze (iid samples). Every-visit uses more data per episode and typically converges faster in practice.

**Incremental mean.** Instead of storing all returns, update the running average:

`V_n(s) = V_{n-1}(s) + (1/n) [G_n - V_{n-1}(s)]`

Reorganize: `V_new = V_old + α · (target - V_old)` with `α = 1/n`. Swap `1/n` for a constant step-size `α ∈ (0, 1)` and you get a non-stationary MC estimator that tracks changes in `π`. That move is the entire jump from MC to TD to every modern RL algorithm.

**Exploration is now a problem.** DP touched every state by enumeration. MC only sees states the policy visits. If `π` is deterministic, whole regions of the state space never get sampled, and their value estimates stay at zero forever. Three fixes, in historical order:

> **【中文解读】** 探索问题：DP 能遍历所有状态，MC 只能看到策略访问过的状态。如果策略是确定性的，大量状态永远不会被访问。三种解决方案：探索起点（不实际）、ε-贪心（最常用）、离策略 MC（通过重要性采样从行为策略学习目标策略）。

1. **Exploring starts.** Start each episode from a random (s, a) pair. Guarantees coverage; unrealistic in practice (you cannot "reset" a robot into an arbitrary state).
2. **ε-greedy.** Act greedy w.r.t. current Q, but with probability `ε` pick a random action. All state-action pairs get sampled asymptotically.
3. **Off-policy MC.** Collect data under a behavior policy `μ`, learn about target policy `π` via importance sampling. High variance, but it's the bridge to replay-buffer methods like DQN.

**Monte Carlo Control.** Evaluate → improve → evaluate, just like policy iteration, but evaluation is sampling-based:

1. Run `π`, get an episode.
2. Update `Q(s, a)` from observed returns.
3. Make `π` ε-greedy w.r.t. `Q`.
4. Repeat.

Converges to `Q*` and `π*` with probability 1 under mild conditions (every pair visited infinitely often, `α` satisfies Robbins-Monro).

## Build It | 动手实现

### Step 1: rollout → list of (s, a, r)

```python
def rollout(env, policy, max_steps=200):
    trajectory = []
    s = env.reset()
    for _ in range(max_steps):
        a = policy(s)
        s_next, r, done = env.step(s, a)
        trajectory.append((s, a, r))
        s = s_next
        if done:
            break
    return trajectory
```

No model, only `env.reset()` and `env.step(s, a)`. Same interface as a gym environment but stripped down.

### Step 2: compute returns (reverse sweep)

```python
def returns_from(trajectory, gamma):
    returns = []
    G = 0.0
    for _, _, r in reversed(trajectory):
        G = r + gamma * G
        returns.append(G)
    return list(reversed(returns))
```

One pass, `O(T)`. The backward recurrence `G_t = r_{t+1} + γ G_{t+1}` avoids re-summing.

### Step 3: first-visit MC evaluation

```python
def mc_policy_evaluation(env, policy, episodes, gamma=0.99):
    V = defaultdict(float)
    counts = defaultdict(int)
    for _ in range(episodes):
        trajectory = rollout(env, policy)
        returns = returns_from(trajectory, gamma)
        seen = set()
        for t, ((s, _, _), G) in enumerate(zip(trajectory, returns)):
            if s in seen:
                continue
            seen.add(s)
            counts[s] += 1
            V[s] += (G - V[s]) / counts[s]
    return V
```

Three lines do the work: mark state as seen on first visit, increment count, update running mean.

### Step 4: ε-greedy MC control (on-policy)

```python
def mc_control(env, episodes, gamma=0.99, epsilon=0.1):
    Q = defaultdict(lambda: {a: 0.0 for a in ACTIONS})
    counts = defaultdict(lambda: {a: 0 for a in ACTIONS})

    def policy(s):
        if random() < epsilon:
            return choice(ACTIONS)
        return max(Q[s], key=Q[s].get)

    for _ in range(episodes):
        trajectory = rollout(env, policy)
        returns = returns_from(trajectory, gamma)
        seen = set()
        for (s, a, _), G in zip(trajectory, returns):
            if (s, a) in seen:
                continue
            seen.add((s, a))
            counts[s][a] += 1
            Q[s][a] += (G - Q[s][a]) / counts[s][a]
    return Q, policy
```

### Step 5: compare to DP gold standard

Your MC estimate of `V^π` should agree with the DP result from Lesson 02 as episodes → ∞. In practice: 50,000 episodes on 4×4 GridWorld gets you within `~0.1` of the DP answer.

## Pitfalls

- **Infinite episodes.** MC requires episodes to *terminate*. If your policy can loop forever, cap `max_steps` and treat the cap as implicit failure. GridWorld with a random policy routinely times out — that is normal, just make sure you count it correctly.
- **Variance.** MC uses full returns. On long episodes, variance is huge — one unlucky reward at the end shifts `V(s_0)` by the same amount. TD methods (Lesson 04) cut this by bootstrapping.
- **State coverage.** Greedy MC on a fresh Q with ties will only ever try one action. You *must* explore (ε-greedy, exploring starts, UCB).
- **Non-stationary policies.** If `π` changes (as in MC control), old returns are from a different policy. Constant-α MC handles this; sample-average MC does not.
- **Off-policy importance sampling.** The weights `π(a|s)/μ(a|s)` multiply across a trajectory. Variance explodes with horizon. Cap with per-decision weighted IS or switch to TD.

## Use It | 用框架实现

The 2026 role of Monte Carlo methods:

| Use case | Why MC |
|----------|--------|
| Short-horizon games (blackjack, poker) | Episodes terminate naturally; returns are clean. |
| Offline evaluation of a logged policy | Average discounted returns over stored trajectories. |
| Monte Carlo Tree Search (AlphaZero) | MC rollouts from tree leaves guide selection. |
| LLM RL evaluation | Compute average reward over sampled completions for a given policy. |
| Baseline estimation in PPO | The advantage target `A_t = G_t - V(s_t)` uses an MC `G_t`. |
| Teaching RL | Simplest algorithm that actually works — strip bootstrapping to see the core. |

Modern deep-RL algorithms (PPO, SAC) interpolate between pure MC (full returns) and pure TD (one-step bootstrap) via `n`-step returns or GAE. Both endpoints are instances of the same estimator.

## Ship It | 产出物

Save as `outputs/skill-mc-evaluator.md`:

```markdown
---
name: mc-evaluator
description: Evaluate a policy via Monte Carlo rollouts and produce a convergence report with DP-comparison if available.
version: 1.0.0
phase: 9
lesson: 3
tags: [rl, monte-carlo, evaluation]
---

Given an environment (episodic, with reset+step API) and a policy, output:

1. Method. First-visit vs every-visit MC. Reason.
2. Episode budget. Target number, variance diagnostic, expected standard error.
3. Exploration plan. ε schedule (if needed) or exploring starts.
4. Gold-standard comparison. DP-optimal V* if tabular; otherwise a bound from a Q-learning / PPO baseline.
5. Termination check. Max-step cap, timeouts, handling of non-terminating trajectories.

Refuse to run MC on non-episodic tasks without a finite horizon cap. Refuse to report V^π estimates from fewer than 100 episodes per state for tabular tasks. Flag any policy with zero-variance actions as an exploration risk.
```

## Exercises | 练习题

1. **Easy.** Implement first-visit MC evaluation of the uniform-random policy on 4×4 GridWorld. Run 10,000 episodes. Plot `V(0,0)` as a function of episode count against the DP answer.
   > **练习1：** 实现 MC 评估，将 V(0,0) 随回合数的收敛曲线与 DP 基准对比。
2. **Medium.** Implement ε-greedy MC control with `ε ∈ {0.01, 0.1, 0.3}`. Compare mean return after 20,000 episodes. What does the curve look like? Where does the bias-variance tradeoff live?
   > **练习2：** 用不同 ε 值做 MC 控制，观察探索-利用权衡。
3. **Hard.** Implement *off-policy* MC with importance sampling: collect data under uniform-random policy `μ`, estimate `V^π` for the deterministic optimal policy `π`. Compare plain IS vs per-decision IS vs weighted IS. Which has lowest variance?
   > **练习3：** 实现离策略 MC（重要性采样），比较不同 IS 方差的差异。

## Key Terms | 术语速查表

| Term | What people say | What it actually means |
|------|-----------------|-----------------------|
| Monte Carlo | "Random sampling" / 蒙特卡洛 | Estimate expectations by averaging over iid samples from the distribution. |
| Return `G_t` | "Future reward" / 回报 | Sum of discounted rewards from step `t` to episode end: `Σ_{k≥0} γ^k r_{t+k+1}`. |
| First-visit MC | "Count each state once" / 首次访问 MC | Only the first visit in an episode contributes to the value estimate. |
| Every-visit MC | "Use all visits" / 每次访问 MC | Every visit contributes; slightly biased but more sample-efficient. |
| ε-greedy | "Exploration noise" / ε-贪心 | Pick greedy action with prob `1-ε`; random action with prob `ε`. |
| Importance sampling | "Correcting for sampling from the wrong distribution" / 重要性采样 | Reweight returns by `π(a\|s)/μ(a\|s)` products to estimate `V^π` from `μ` data. |
| On-policy | "Learn from my own data" / 在线策略 | Target policy = behavior policy. Vanilla MC, PPO, SARSA. |
| Off-policy | "Learn from someone else's data" / 离线策略 | Target policy ≠ behavior policy. Importance-sampled MC, Q-learning, DQN. |

## Further Reading | 延伸阅读

- [Sutton & Barto (2018). Ch. 5 — Monte Carlo Methods](http://incompleteideas.net/book/RLbook2020.pdf) — the canonical treatment.
- [Singh & Sutton (1996). Reinforcement Learning with Replacing Eligibility Traces](https://link.springer.com/article/10.1007/BF00114726) — first-visit vs every-visit analysis.
- [Precup, Sutton, Singh (2000). Eligibility Traces for Off-Policy Policy Evaluation](http://incompleteideas.net/papers/PSS-00.pdf) — off-policy MC and variance control.
- [Mahmood et al. (2014). Weighted Importance Sampling for Off-Policy Learning](https://arxiv.org/abs/1404.6362) — modern low-variance IS estimators.
- [Tesauro (1995). TD-Gammon, A Self-Teaching Backgammon Program](https://dl.acm.org/doi/10.1145/203330.203343) — the first large-scale empirical demonstration of MC/TD self-play converging to superhuman play; conceptual precursor to every lesson in the second half of this phase.
