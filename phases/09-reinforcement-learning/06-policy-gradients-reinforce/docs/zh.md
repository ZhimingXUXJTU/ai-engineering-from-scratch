# 策略梯度 — 从零实现REINFORCE

> 不再估计值函数。直接参数化策略，计算期望回报的梯度，往上走。Williams（1992）用一个定理就写完了。这就是 PPO、GRPO 和每个 LLM RL 循环存在的原因。

> **【中文解读】** 不再估计值函数，直接参数化策略 π_θ(a|s)，计算期望回报的梯度并梯度上升。REINFORCE 定理告诉我们：`∇J(θ) = E[G · ∇log π_θ(a|s)]`。这是 PPO、GRPO、以及所有大模型 RL 训练循环存在的理由。

**类型：** 构建
**语言：** Python
**前置知识：** Phase 3 · 03（反向传播），Phase 9 · 03（蒙特卡洛），Phase 9 · 04（TD 学习）
**用时：** 约 75 分钟

## 问题引入

Q-learning 和 DQN 参数化*值函数*。你通过 `argmax Q` 选择动作。这对离散动作和离散状态没问题。但当动作是连续的（在 10 维力矩上取 `argmax`？）或你需要随机策略时（`argmax` 天然是确定性的），就失效了。

策略梯度改为参数化*策略*。`π_θ(a | s)` 是一个输出动作分布的神经网络。从中采样来行动。计算期望回报关于 `θ` 的梯度。往上走。没有 `argmax`。没有 Bellman 递归。就是在 `J(θ) = E_{π_θ}[G]` 上做梯度上升。

REINFORCE 定理（Williams 1992）告诉你这个梯度是可计算的：`∇J(θ) = E_π[ G · ∇_θ log π_θ(a | s) ]`。运行一个回合。计算回报。在每步乘以 `∇ log π_θ(a | s)`。取平均。梯度上升。完成。

2026 年的每个 LLM-RL 算法——PPO、DPO、GRPO——都是 REINFORCE 的改进。将其烂熟于心是本阶段其余课程、Phase 10 · 07（RLHF 实现）和 Phase 10 · 08（DPO）的前提。

> **【中文解读】** 策略梯度的核心思想：直接优化策略参数 θ，让高回报的动作概率增大、低回报的动作概率减小。`∇log π` 就是"策略的方向导数"，乘以回报 G 就是"沿着好的方向走"。

> **【拓展：PPO→ChatGPT对齐】** ChatGPT 的 RLHF 训练使用的 PPO 算法，本质上就是 REINFORCE + critic 基线 + 信赖域裁剪。`loss = -advantage * log_prob` 这一行代码，出现在几乎所有 2026 年的大模型 RL 训练脚本中。DeepSeek-R1 的 GRPO 则是用组均值替代 critic 基线的 REINFORCE。

## 核心概念

![策略梯度：softmax 策略、log-π 梯度、回报加权更新](../assets/policy-gradient.svg)

**策略梯度定理。** 对于任何由 `θ` 参数化的策略 `π_θ`：

`∇J(θ) = E_{τ ~ π_θ}[ Σ_{t=0}^{T} G_t · ∇_θ log π_θ(a_t | s_t) ]`

其中 `G_t = Σ_{k=t}^{T} γ^{k-t} r_{k+1}` 是从步骤 `t` 开始的折扣回报。期望是对从 `π_θ` 采样的完整轨迹 `τ` 取的。

**证明很短。** 对 `J(θ) = Σ_τ P(τ; θ) G(τ)` 在期望下求导。利用 `∇P(τ; θ) = P(τ; θ) ∇ log P(τ; θ)`（对数导数技巧）。分解 `log P(τ; θ) = Σ log π_θ(a_t | s_t) + 不依赖于 θ 的环境项`。环境项消失。两行代数给出定理。

**方差缩减技巧。** 朴素 REINFORCE 有可怕的方差——回报有噪声，`∇ log π` 有噪声，它们的乘积噪声非常大。两种标准修复：

1. **基线减法。** 用 `G_t - b(s_t)` 替换 `G_t`，其中 `b(s_t)` 是不依赖于 `a_t` 的任何基线函数。无偏，因为 `E[b(s_t) · ∇ log π(a_t | s_t)] = 0`。典型选择：`b(s_t) = V̂(s_t)` 由评论家学习 → Actor-Critic（第 07 课）。
2. **未来回报 (Reward-to-go)。** 将 `Σ_t G_t · ∇ log π_θ(a_t | s_t)` 替换为 `Σ_t G_t^{from t} · ∇ log π_θ(a_t | s_t)`。只有未来回报对给定动作有影响——过去奖励贡献零均值噪声。

组合起来得到：

`∇J ≈ (1/N) Σ_{i=1}^{N} Σ_{t=0}^{T_i} [ G_t^{(i)} - V̂(s_t^{(i)}) ] · ∇_θ log π_θ(a_t^{(i)} | s_t^{(i)})`

这就是带基线的 REINFORCE——A2C（第 07 课）和 PPO（第 08 课）的直接祖先。

**Softmax 策略参数化。** 对于离散动作，标准选择：

`π_θ(a | s) = exp(f_θ(s, a)) / Σ_{a'} exp(f_θ(s, a'))`

其中 `f_θ` 是任何输出每个动作分数的神经网络。梯度有简洁形式：

`∇_θ log π_θ(a | s) = ∇_θ f_θ(s, a) - Σ_{a'} π_θ(a' | s) ∇_θ f_θ(s, a')`

即所取动作的分数减去策略下其期望值。

**高斯策略用于连续动作。** `π_θ(a | s) = N(μ_θ(s), σ_θ(s))`。`∇ log N(a; μ, σ)` 有闭式解。这就是 Phase 9 · 07 的 SAC 所需的全部。

## 动手实现

### 第 1 步：softmax 策略网络

```python
def policy_logits(theta, state_features):
    return [dot(theta[a], state_features) for a in range(N_ACTIONS)]

def softmax(logits):
    m = max(logits)
    exps = [exp(l - m) for l in logits]
    Z = sum(exps)
    return [e / Z for e in exps]
```

对表格式环境使用线性策略（每个动作一个权重向量）。对 Atari，替换为 CNN 并保留 softmax 头。

### 第 2 步：采样和对数概率

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

### 第 3 步：带对数概率的展开

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

### 第 4 步：REINFORCE 更新

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

梯度 `∇ log π(a|s) = e_a - π(·|s)`（`a` 的 one-hot 减去概率）是 softmax 策略梯度的核心。将其刻入肌肉记忆。

### 第 5 步：基线

近期回合中 `G` 的运行均值就足以让 4×4 GridWorld 运行；大约 500 个回合收敛。将基线升级为学习的 `V̂(s)` 就得到 Actor-Critic。

## 常见陷阱

- **梯度爆炸。** 回报可能非常大。始终在乘以 `∇ log π` 之前将 `G` 归一化到 `~N(0, 1)`。
- **熵坍缩。** 策略过早收敛到近确定性动作，停止探索，陷入困境。修复：添加熵奖励 `β · H(π(·|s))` 到目标函数。
- **高方差。** 朴素 REINFORCE 需要数千个回合。评论家基线（第 07 课）或 TRPO/PPO 的信赖域（第 08 课）是标准修复。
- **样本效率低。** 在线策略意味着每次更新后丢弃每个转移。通过重要性采样的离策略修正可以复用数据，代价是方差（PPO 的比率就是裁剪的 IS 权重）。
- **非平稳梯度。** 100 个回合前的梯度使用的是旧的 `π`。在线策略方法因此每隔几次展开就更新。
- **信用分配。** 没有未来回报的话，过去奖励贡献噪声。始终使用未来回报。

## 用框架实现

2026 年，REINFORCE 很少直接运行，但它的梯度公式无处不在：

| 用例 | 衍生方法 |
|------|----------|
| 连续控制 | 带高斯策略的 PPO / SAC |
| LLM RLHF | 带 KL 惩罚的 PPO，在 token 级策略上运行 |
| LLM 推理（DeepSeek） | GRPO — 带组相对基线的 REINFORCE，无评论家 |
| 多智能体 | 集中评论家 REINFORCE（MADDPG、COMA） |
| 离散动作机器人 | A2C、A3C、PPO |
| 仅偏好设置 | DPO — REINFORCE 重写为偏好似然损失，无需采样 |

当你在 2026 年训练脚本中读到 `loss = -advantage * log_prob` 时，那就是带基线的 REINFORCE。整篇论文（DPO、GRPO、RLOO）都是在这行之上的方差缩减技巧。

## 产出物

保存为 `outputs/skill-policy-gradient-trainer.md`：

```markdown
---
name: policy-gradient-trainer
description: 为给定任务生成 REINFORCE / Actor-Critic / PPO 训练配置并诊断方差问题。
version: 1.0.0
phase: 9
lesson: 6
tags: [rl, policy-gradient, reinforce]
---

给定一个环境（离散 / 连续动作，视野，奖励统计），输出：

1. 策略头。Softmax（离散）或高斯（连续）及参数量。
2. 基线。无（朴素）、运行均值、学习的 `V̂(s)`、或 A2C 评论家。
3. 方差控制。默认开启未来回报，回报归一化，梯度裁剪值。
4. 熵奖励。系数 β 及衰减调度。
5. 批大小。每次更新的回合数；在线策略数据新鲜度约束。

拒绝在视野 > 500 步的任务上使用无基线 REINFORCE。拒绝在连续动作控制上使用 softmax 头。标记任何 β=0 且观测策略熵 < 0.1 的运行为熵坍缩。
```

## 练习题

1. **简单。** 用线性 softmax 策略在 4×4 GridWorld 上实现 REINFORCE。无基线训练 1,000 个回合。绘制学习曲线；测量方差（回报标准差）。
2. **中等。** 添加运行均值基线。再次训练。比较样本效率和方差与朴素运行。基线减少多少步才能收敛？
3. **困难。** 添加熵奖励 `β · H(π)`。扫描 `β ∈ {0, 0.01, 0.1, 1.0}`。绘制最终回报和策略熵。这个任务的最佳点在哪里？

## 术语速查表

| 术语 | 通俗说法 | 实际含义 |
|------|----------|----------|
| 策略梯度 (Policy Gradient) | "直接训练策略" | `∇J(θ) = E[G · ∇ log π_θ(a\|s)]`；从对数导数技巧推导。 |
| REINFORCE | "原始 PG 算法" | Williams（1992）；蒙特卡洛回报乘以 log 策略梯度。 |
| 对数导数技巧 (Log-derivative Trick) | "得分函数估计器" | `∇P(τ;θ) = P(τ;θ) · ∇ log P(τ;θ)`；使期望的梯度变得可计算。 |
| 基线 (Baseline) | "方差缩减" | 从 `G` 中减去的任何 `b(s)`；无偏因为 `E[b · ∇ log π] = 0`。 |
| 未来回报 (Reward-to-go) | "只有未来回报算数" | `G_t^{from t}` 而非完整的 `G_0`；正确且方差更低。 |
| 熵奖励 (Entropy Bonus) | "鼓励探索" | `+β · H(π(·\|s))` 项防止策略坍缩。 |
| 在线策略 (On-policy) | "用刚看到的训练" | 梯度期望是关于当前策略的——不能直接复用旧数据。 |
| 优势 (Advantage) | "比平均好多少" | `A(s, a) = G(s, a) - V(s)`；带基线 REINFORCE 乘以的有符号量。 |

## 延伸阅读

- [Williams (1992). Simple Statistical Gradient-Following Algorithms for Connectionist Reinforcement Learning](https://link.springer.com/article/10.1007/BF00992696) — 原始 REINFORCE 论文。
- [Sutton et al. (2000). Policy Gradient Methods for Reinforcement Learning with Function Approximation](https://papers.nips.cc/paper_files/paper/1999/hash/464d828b85b0bed98e80ade0a5c43b0f-Abstract.html) — 带函数近似的现代策略梯度定理。
- [Sutton & Barto (2018). Ch. 13 — Policy Gradient Methods](http://incompleteideas.net/book/RLbook2020.pdf) — 教科书呈现。
- [OpenAI Spinning Up — VPG / REINFORCE](https://spinningup.openai.com/en/latest/algorithms/vpg.html) — 带 PyTorch 代码的清晰教学讲解。
- [Peters & Schaal (2008). Reinforcement Learning of Motor Skills with Policy Gradients](https://homes.cs.washington.edu/~todorov/courses/amath579/reading/PolicyGradient.pdf) — 方差缩减和自然梯度视角，将 REINFORCE 连接到信赖域家族（TRPO、PPO）。
