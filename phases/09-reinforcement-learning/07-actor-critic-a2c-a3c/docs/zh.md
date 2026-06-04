# 演员-评论家 — A2C 与 A3C

> REINFORCE 噪声太大。加一个学习 `V̂(s)` 的评论家，从回报中减去它，得到一个期望相同但方差低得多的优势。这就是 Actor-Critic。A2C 同步运行；A3C 跨线程运行。两者都是每个现代深度 RL 方法的思维模型。

> **【中文解读】** REINFORCE 方差太大。加入一个"评论家"(Critic)学习 V̂(s)，用它作为基线构造优势函数 A = G - V̂(s)，期望不变但方差大幅降低。这就是 Actor-Critic——PPO、SAC 等所有现代深度 RL 方法的架构原型。

**类型：** 构建
**语言：** Python
**前置知识：** Phase 9 · 04（TD 学习），Phase 9 · 06（REINFORCE）
**用时：** 约 75 分钟

## 问题引入

朴素 REINFORCE 有效，但方差很糟糕。蒙特卡洛回报 `G_t` 在回合之间可以波动 10 倍。将噪声乘以 `∇ log π` 再取平均产生的梯度估计器需要数千个回合才能将策略移动与少量 DQN 更新就能达到的相同距离。

方差来自使用原始回报。如果你减去基线 `b(s_t)`——任何状态函数，包括学习的值函数——期望不变且方差下降。最佳可行基线是 `V̂(s_t)`。现在乘以 `∇ log π` 的量是*优势*：

`A(s, a) = G - V̂(s)`

一个动作如果产生了高于平均的回报就是好的；低于平均就是差的。带学习评论家的 REINFORCE 就是 *Actor-Critic*。评论家给演员一个低方差的教师。这就是 2015 年之后的每个深度策略方法（A2C、A3C、PPO、SAC、IMPALA）。

## 核心概念

![Actor-Critic：策略网络加值网络，TD 残差作为优势](../assets/actor-critic.svg)

**两个网络，一个共享损失：**

- **演员 (Actor)** `π_θ(a | s)`：策略。用于采样行动。用策略梯度训练。
- **评论家 (Critic)** `V_φ(s)`：估计从状态出发的期望回报。训练以最小化 `(V_φ(s) - target)²`。

**优势。** 两种标准形式：

- *MC 优势：* `A_t = G_t - V_φ(s_t)`。无偏，方差较高。
- *TD 优势：* `A_t = r_{t+1} + γ V_φ(s_{t+1}) - V_φ(s_t)`。有偏差（使用 `V_φ`），方差远低。也叫 *TD 残差* `δ_t`。

**n 步优势。** 在两者之间插值：

`A_t^{(n)} = r_{t+1} + γ r_{t+2} + … + γ^{n-1} r_{t+n} + γ^n V_φ(s_{t+n}) - V_φ(s_t)`

`n = 1` 是纯 TD。`n = ∞` 是 MC。大多数实现对 Atari 使用 `n = 5`，对 MuJoCo 上的 PPO 使用 `n = 2048`。

**广义优势估计 (Generalized Advantage Estimation, GAE)。** Schulman 等人（2016）提出对所有 n 步优势的指数加权平均：

`A_t^{GAE} = Σ_{l=0}^{∞} (γλ)^l δ_{t+l}`

其中 `λ ∈ [0, 1]`。`λ = 0` 是 TD（低方差，高偏差）。`λ = 1` 是 MC（高方差，无偏差）。`λ = 0.95` 是 2026 年的默认值——调节直到偏差/方差旋钮到你想要的位置。

> **【中文解读】** GAE（广义优势估计）是 Actor-Critic 的关键改进：通过指数加权平均所有 n 步优势，在偏差和方差之间找到最优平衡。lambda=0 是纯 TD（低方差高偏差），lambda=1 是纯 MC（高方差无偏差），lambda=0.95 是 2026 年默认值。GAE 是 PPO 的核心组件。

> **【拓展：GAE 在 RLHF 中的应用】** ChatGPT 的 PPO 训练使用 GAE 计算优势函数。在 LLM 场景中，"状态"是已生成的 token 序列，"动作"是下一个 token，"奖励"来自奖励模型。GAE 让 PPO 能在长文本生成（数百 token）中稳定训练，平衡即时奖励和长期回报。

**A2C：同步优势 Actor-Critic。** 在 `N` 个并行环境中收集 `T` 步。计算每步的优势。在合并批次上更新演员和评论家。重复。A3C 的更简单、更可扩展的兄弟。

**A3C：异步优势 Actor-Critic。** Mnih 等人（2016）。创建 `N` 个工作线程，每个运行一个环境。每个工作线程在自己的展开上本地计算梯度，然后异步应用到共享参数服务器。无需回放缓冲——工作线程通过运行不同轨迹来去相关。A3C 证明了可以在 CPU 上大规模训练。2026 年，基于 GPU 的 A2C（批量并行环境）占主导，因为 GPU 需要大批次。

**组合损失。**

`L(θ, φ) = -E[ A_t · log π_θ(a_t | s_t) ]  +  c_v · E[(V_φ(s_t) - G_t)²]  -  c_e · E[H(π_θ(·|s_t))]`

三项：策略梯度损失、值回归、熵奖励。`c_v ~ 0.5`、`c_e ~ 0.01` 是经典的起始点。

> **【中文解读】** Actor-Critic 的组合损失 = 策略梯度损失 + 值函数回归 + 熵正则化。这三项分别对应：让好的动作概率更大、让 Critic 更准确、防止策略过早坍缩为确定性策略。

> **【拓展：GAE→PPO→RLHF】** GAE (广义优势估计) 是 PPO 的核心组件，而 PPO 是 ChatGPT RLHF 训练的标准算法。λ=0.95 是 2026 年的默认值，在偏差和方差之间取得平衡。理解 GAE 就理解了大模型对齐训练中最关键的优势估计方法。

## 动手实现

### 第 1 步：评论家

线性评论家 `V_φ(s) = w · features(s)` 用 MSE 更新：

```python
def critic_update(w, x, target, lr):
    v_hat = dot(w, x)
    err = target - v_hat
    for j in range(len(w)):
        w[j] += lr * err * x[j]
    return v_hat
```

在表格式环境上，评论家在几百个回合内收敛。在 Atari 上，将线性评论家替换为共享 CNN 主干 + 值头。

### 第 2 步：n 步优势

给定长度 `T` 的展开和自举的最终 `V(s_T)`：

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

`returns` 是评论家目标。`advantages` 是乘以 `∇ log π` 的量。

### 第 3 步：组合更新

```python
for step_i, (x, a, _r, probs) in enumerate(traj):
    adv = advantages[step_i]
    target_v = returns[step_i]

    # 评论家
    critic_update(w, x, target_v, lr_v)

    # 演员
    for i in range(N_ACTIONS):
        grad_logpi = (1.0 if i == a else 0.0) - probs[i]
        for j in range(N_FEAT):
            theta[i][j] += lr_a * adv * grad_logpi * x[j]
```

在线策略，每次更新一个展开，演员和评论家使用不同的学习率。

### 第 4 步：并行化（A3C vs A2C）

- **A3C：** 启动 `N` 个线程。每个运行自己的环境和前向传播。定期将梯度更新推送到共享主服务器。主服务器无锁——竞争没关系，只是增加噪声。
- **A2C：** 在单个进程中运行 `N` 个环境实例，将观测堆叠为 `[N, obs_dim]` 批次，批量前向传播，批量反向传播。更高的 GPU 利用率，确定性，更易推理。2026 年的默认选择。

我们的玩具代码为清晰起见是单线程的；改写为批量 A2C 只需三行 numpy。

## 常见陷阱

- **评论家偏差在演员梯度之前。** 如果评论家是随机的，其基线没有信息量，你在纯噪声上训练。在打开策略梯度之前预热评论家几百步，或使用较慢的演员学习率。
- **优势归一化。** 将优势归一化为每批次零均值/单位标准差。几乎零成本就大幅稳定训练。
- **共享主干。** 对图像输入使用共享特征提取器给演员和评论家。分离的头。共享特征从两个损失中搭便车。
- **在线策略约束。** A2C 恰好使用数据一次更新。更多次使用会让梯度有偏差（重要性采样修正是 PPO 添加的）。
- **熵坍缩。** 没有 `c_e > 0`，策略在几百次更新内变为近确定性并停止探索。
- **奖励尺度。** 优势幅度取决于奖励尺度。归一化奖励（例如，除以运行标准差）以在不同任务间保持一致的梯度幅度。

## 用框架实现

A2C/A3C 在 2026 年很少是最终选择，但它们是后来所有方法改进的架构基础：

| 方法 | 与 A2C 的关系 |
|------|---------------|
| PPO | A2C + 裁剪重要性比率用于多轮更新 |
| IMPALA | A3C + V-trace 离策略修正 |
| SAC（Phase 9 · 07） | 离策略 A2C 带软值评论家（下一课） |
| GRPO（Phase 9 · 12） | 无评论家的 A2C——组相对优势 |
| DPO | A2C 坍缩为偏好排序损失，无需采样 |
| AlphaStar / OpenAI Five | A2C + 联盟训练 + 模仿预训练 |

如果你在 2026 年论文中看到"优势"，想 Actor-Critic。

## 产出物

保存为 `outputs/skill-actor-critic-trainer.md`：

```markdown
---
name: actor-critic-trainer
description: 为给定环境生成 A2C / A3C / GAE 配置，指定优势估计和损失权重。
version: 1.0.0
phase: 9
lesson: 7
tags: [rl, actor-critic, gae]
---

给定环境和计算预算，输出：

1. 并行度。A2C（GPU 批量）vs A3C（CPU 异步）及工作线程数。
2. 展开长度 T。每个环境每次更新的步数。
3. 优势估计器。n 步或 GAE(λ)；指定 λ。
4. 损失权重。`c_v`（值）、`c_e`（熵）、梯度裁剪。
5. 学习率。演员和评论家（如使用则分开）。

拒绝在视野 > 1000 的环境上使用单工作线程 A2C（太在线策略，太慢）。拒绝发布没有优势归一化的方案。标记任何 c_e=0 且观测熵 < 0.1 的运行为熵坍缩。
```

## 练习题

1. **简单。** 在 4×4 GridWorld 上用 MC 优势（`G_t - V(s_t)`）训练 Actor-Critic。与第 06 课的 REINFORCE-运行均值-基线比较样本效率。
2. **中等。** 切换到 TD 残差优势（`r + γ V(s') - V(s)`）。测量优势批次的方差。降低了多少？
3. **困难。** 实现 GAE(λ)。扫描 `λ ∈ {0, 0.5, 0.9, 0.95, 1.0}`。绘制最终回报 vs 样本效率。这个任务的偏差/方差最佳点在哪里？

## 术语速查表

| 术语 | 通俗说法 | 实际含义 |
|------|----------|----------|
| 演员 (Actor) | "策略网络" | `π_θ(a\|s)`，由策略梯度更新。 |
| 评论家 (Critic) | "值网络" | `V_φ(s)`，由对回报 / TD 目标的 MSE 回归更新。 |
| 优势 (Advantage) | "比平均好多少" | `A(s, a) = Q(s, a) - V(s)` 或其估计器。`∇ log π` 的乘数。 |
| TD 残差 | "δ" | `δ_t = r + γ V(s') - V(s)`；单步优势估计。 |
| GAE | "插值旋钮" | n 步优势的指数加权和，由 `λ` 参数化。 |
| A2C | "同步 Actor-Critic" | 跨环境批量；每次展开一个梯度步。 |
| A3C | "异步 Actor-Critic" | 工作线程将梯度推送到共享参数服务器。原始论文；2026 年较少见。 |
| 自举截断 (Bootstrap) | "在视野处用 V" | 截断展开，加上 `γ^n V(s_{t+n})` 来闭合求和。 |

## 延伸阅读

- [Mnih et al. (2016). Asynchronous Methods for Deep Reinforcement Learning](https://arxiv.org/abs/1602.01783) — A3C，原始异步 Actor-Critic 论文。
- [Schulman et al. (2016). High-Dimensional Continuous Control Using Generalized Advantage Estimation](https://arxiv.org/abs/1506.02438) — GAE。
- [Sutton & Barto (2018). Ch. 13 — Actor-Critic Methods](http://incompleteideas.net/book/RLbook2020.pdf) — 基础；当评论家是神经网络时配合第 9 章函数近似一起阅读。
- [Espeholt et al. (2018). IMPALA](https://arxiv.org/abs/1802.01561) — 可扩展分布式 Actor-Critic 带 V-trace 离策略修正。
- [OpenAI Baselines / Stable-Baselines3](https://stable-baselines3.readthedocs.io/) — 值得阅读的生产 A2C/PPO 实现。
- [Konda & Tsitsiklis (2000). Actor-Critic Algorithms](https://papers.nips.cc/paper/1786-actor-critic-algorithms) — 双时间尺度 Actor-Critic 分解的基础收敛结果。
