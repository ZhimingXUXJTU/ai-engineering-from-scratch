# 时序差分 — Q学习与SARSA

> 蒙特卡洛要等到回合结束。TD 在每一步后通过自举下一个值估计来更新。Q-learning 是离策略且乐观的；SARSA 是在线策略且谨慎的。两者都是一行代码。两者都是本阶段每个深度 RL 方法的基础。

> **【中文解读】** MC 要等到回合结束才能更新，TD（时序差分）每一步都能更新——用 `r + γ V(s')` 作为目标来引导当前估计。Q-learning 是离策略的（学习最优策略），SARSA 是在线策略的（学习当前行为策略）。两者仅差一个 `max`，却是所有深度 RL 的基础。

**类型：** 构建
**语言：** Python
**前置知识：** Phase 9 · 01（MDP），Phase 9 · 02（动态规划），Phase 9 · 03（蒙特卡洛）
**用时：** 约 75 分钟

## 问题引入

蒙特卡洛有效，但有两个昂贵的要求。它需要终止的回合，而且只在最终回报确定后才更新。如果你的回合是 1,000 步，MC 要等 1,000 步才更新任何东西。它高方差、低偏差，实践中也慢。

动态规划有相反的特性——零方差的自举备份——但需要已知模型。

时序差分 (Temporal Difference, TD) 学习取两者折中。从单个转移 `(s, a, r, s')` 构造单步目标 `r + γ V(s')`，将 `V(s)` 向它微调。无需模型。无需完整回合。由于在右侧使用近似 `V` 而产生偏差，但方差远低于 MC，并且从第一步就可以在线更新。

这是所有现代 RL——DQN、A2C、PPO、SAC——的转折点。Phase 9 的其余部分是在你本课将写的单步 TD 更新之上构建的函数近似和技巧的层层叠加。

> **【中文解读】** TD 学习是 DP 和 MC 的折中：用单步转移 `(s,a,r,s')` 构造目标 `r + γV(s')`，不需要模型，也不需要完整回合。有偏差（因为用了近似 V），但方差远低于 MC，而且可以在线更新。DQN、PPO、RLHF 都是基于 TD 思想的变体。

> **【拓展：游戏AI→LLM对齐】** Q-learning 是 2013 年 Atari DQN 的核心，开启了深度 RL 时代。PPO 则是 ChatGPT RLHF 训练的核心算法——两者都基于 TD 误差的思想。理解 Q-learning 和 SARSA 是理解大模型对齐训练的基础。

## 核心概念

![Q-learning vs SARSA：离策略 max vs 在线策略 Q(s', a')](../assets/td.svg)

**V 的 TD(0) 更新：**

`V(s) ← V(s) + α [r + γ V(s') - V(s)]`

括号中的量是 TD 误差 `δ = r + γ V(s') - V(s)`。它是 MC 中 `G_t - V(s_t)` 的在线对应。收敛要求 `α` 满足 Robbins-Monro 条件（`Σ α = ∞`，`Σ α² < ∞`）且所有状态被无限频繁访问。

**Q-learning。** 一种离策略的 TD 控制方法：

`Q(s, a) ← Q(s, a) + α [r + γ max_{a'} Q(s', a') - Q(s, a)]`

`max` 假设从 `s'` 起将遵循*贪心*策略，无论智能体实际采取什么动作。这种解耦使得 Q-learning 在智能体通过 ε-贪心探索的同时学习 `Q*`。Mnih 等人（2015）将此转化为 Atari 上的深度 Q-learning（第 05 课）。

**SARSA。** 一种在线策略的 TD 方法：

`Q(s, a) ← Q(s, a) + α [r + γ Q(s', a') - Q(s, a)]`

名字来自元组 `(s, a, r, s', a')`。SARSA 使用智能体*实际*采取的下一个动作 `a'`，而非贪心的 `argmax`。收敛到正在运行的任何 ε-贪心 `π` 的 `Q^π`，在 `ε → 0` 极限下变为 `Q*`。

**悬崖行走的差异。** 在经典悬崖行走任务上（掉下悬崖 = 奖励 -100），Q-learning 学到沿悬崖边缘的最优路径，但探索时偶尔会受惩罚。SARSA 学到离悬崖一步的安全路径，因为它将探索噪声计入 Q 值。训练后，当 `ε → 0` 时两者都达到最优。实践中这很重要：当部署时探索确实在发生时，SARSA 的行为更保守。

> **【中文解读】** 经典悬崖行走实验揭示了 Q-learning 和 SARSA 的关键区别：Q-learning 学到贴着悬崖的最优路径（但探索时会掉下去），SARSA 学到远离悬崖的安全路径（因为它考虑了探索噪声）。部署中有探索时，SARSA 更安全保守。

**期望 SARSA (Expected SARSA)。** 将 `Q(s', a')` 替换为 `π` 下的期望值：

`Q(s, a) ← Q(s, a) + α [r + γ Σ_{a'} π(a'|s') Q(s', a') - Q(s, a)]`

比 SARSA 方差更低（不需要采样 `a'`），相同的在线策略目标。通常作为现代教科书中的默认方法。

**n 步 TD 和 TD(λ)。** 通过在自举前等待 `n` 步，在 TD(0) 和 MC 之间插值。`n=1` 是 TD，`n=∞` 是 MC。TD(λ) 用几何权重 `(1-λ)λ^{n-1}` 对所有 `n` 取平均。大多数深度 RL 使用 3 到 20 之间的 `n`。

> **【拓展：TD 误差在 LLM RLHF 中的对应】** TD 误差 δ = r + γV(s') - V(s) 在 LLM 的 RLHF 训练中有直接对应：PPO 的优势函数 A = r + γV(s') - V(s) 就是 TD 误差的变体。每生成一个 token，计算当前 token 的奖励（来自 RM）加上 critic 对未来价值的估计减去当前估计。理解 TD 误差是理解 PPO 优势函数的关键。

## 动手实现

### 第 1 步：ε-贪心策略上的 SARSA

```python
def sarsa(env, episodes, alpha=0.1, gamma=0.99, epsilon=0.1):
    Q = defaultdict(lambda: {a: 0.0 for a in ACTIONS})

    def choose(s):
        if random() < epsilon:
            return choice(ACTIONS)
        return max(Q[s], key=Q[s].get)

    for _ in range(episodes):
        s = env.reset()
        a = choose(s)
        while True:
            s_next, r, done = env.step(s, a)
            a_next = choose(s_next) if not done else None
            target = r + (gamma * Q[s_next][a_next] if not done else 0.0)
            Q[s][a] += alpha * (target - Q[s][a])
            if done:
                break
            s, a = s_next, a_next
    return Q
```

八行代码。与 Q-learning *唯一*的区别是目标行。

### 第 2 步：Q-learning

```python
def q_learning(env, episodes, alpha=0.1, gamma=0.99, epsilon=0.1):
    Q = defaultdict(lambda: {a: 0.0 for a in ACTIONS})
    for _ in range(episodes):
        s = env.reset()
        while True:
            a = choose(s, Q, epsilon)
            s_next, r, done = env.step(s, a)
            target = r + (gamma * max(Q[s_next].values()) if not done else 0.0)
            Q[s][a] += alpha * (target - Q[s][a])
            if done:
                break
            s = s_next
    return Q
```

`max` 将目标与行为解耦。这一个符号就是在线策略和离策略之间的区别。

### 第 3 步：学习曲线

追踪每 100 个回合的平均回报。Q-learning 在简单确定性 GridWorld 上收敛更快；SARSA 在悬崖行走上更保守。在 `code/main.py` 的 4×4 GridWorld 上，`α=0.1, ε=0.1` 时两者都在约 2,000 个回合后接近最优。

### 第 4 步：与 DP 真值对比

运行值迭代（第 02 课）得到 `Q*`。检查 `max_{s,a} |Q_learned(s,a) - Q*(s,a)|`。健康的表格式 TD 智能体在 10,000 个回合后在 4×4 GridWorld 上的偏差在 `~0.5` 以内。

## 常见陷阱

- **Q 初始值很重要。** 乐观初始化（负奖励任务中 `Q = 0`）鼓励探索。悲观初始化可能让贪心策略永远困住。
- **α 调度。** 常数 `α` 对非平稳问题可行。理论上衰减 `α_n = 1/n` 可以收敛但实践中太慢——将 `α` 固定在 `[0.05, 0.3]` 并监控学习曲线。
- **ε 调度。** 高起点（`ε=1.0`），衰减到 `ε=0.05`。"GLIE"（极限贪心且无限探索）是收敛条件。
- **Q-learning 的最大值偏差。** `max` 算子在 `Q` 有噪声时向上偏差。导致过估计——Hasselt 的双重 Q-learning（第 05 课的 DDQN 使用）用两个 Q 表修复此问题。
- **非终止回合。** TD 可以在没有终止状态的情况下学习，但你需要设置步数上限或在上限处正确处理自举。标准做法：将上限视为非终止状态，继续自举。
- **状态哈希。** 如果状态是元组/张量，使用可哈希的键（元组而非列表；浮点数四舍五入后的元组，非原始值）。

## 用框架实现

2026 年的 TD 格局：

| 任务 | 方法 | 原因 |
|------|------|------|
| 小型表格式环境 | Q-learning | 直接学习最优策略。 |
| 在线策略安全关键 | SARSA / 期望 SARSA | 探索时更保守。 |
| 高维状态 | DQN（Phase 9 · 05） | 神经网络 Q 函数 + 回放和目标网络。 |
| 连续动作 | SAC / TD3（Phase 9 · 07） | Q 网络上的 TD 更新；策略网输出动作。 |
| LLM RL（基于奖励模型） | PPO / GRPO（Phase 9 · 08, 12） | Actor-Critic 通过 GAE 使用 TD 风格优势。 |
| 离线 RL | CQL / IQL（Phase 9 · 08） | 带保守正则化的 Q-learning。 |

2026 年论文中你读到的"RL"有 90% 是 Q-learning 或 SARSA 的某种扩展。在深入阅读之前，先让表格式更新烂熟于胸。

## 产出物

保存为 `outputs/skill-td-agent.md`：

```markdown
---
name: td-agent
description: 为表格式或小特征 RL 任务选择 Q-learning、SARSA 或期望 SARSA。
version: 1.0.0
phase: 9
lesson: 4
tags: [rl, td-learning, q-learning, sarsa]
---

给定一个表格式或小特征环境，输出：

1. 算法。Q-learning / SARSA / 期望 SARSA / n 步变体。一句理由，关联在线策略 vs 离策略和方差。
2. 超参数。α、γ、ε、衰减调度。
3. 初始化。Q_0 值（乐观 vs 零）及理由。
4. 收敛诊断。目标学习曲线，如果可能做 DP 则检查 `|Q - Q*|`。
5. 部署注意事项。推理时探索如何表现？是否需要 SARSA 的保守性？

拒绝将表格式 TD 应用于状态空间 > 10⁶。拒绝发布没有最大值偏差警告的 Q-learning 智能体。标记任何 ε 在全程保持 1.0 的智能体（没有利用阶段）。
```

## 练习题

1. **简单。** 在 4×4 GridWorld 上实现 Q-learning 和 SARSA。绘制 2,000 个回合的学习曲线（每 100 个回合的平均回报）。谁收敛更快？
   > **练习1：** 在 GridWorld 上对比 Q-learning 和 SARSA 的学习曲线。
2. **中等。** 构建悬崖行走环境（4×12，最后一行是奖励 -100 的悬崖并重置到起点）。比较 Q-learning 和 SARSA 的最终策略。截图各自走的路径。哪个更接近悬崖？
   > **练习2：** 实现悬崖行走环境，观察 Q-learning（贴崖边）vs SARSA（远离崖边）的策略差异。
3. **困难。** 实现双重 Q-learning。在带噪声奖励的 GridWorld（每步奖励加入高斯噪声 σ=5）上，展示 Q-learning 有意义地过估计 `V*(0,0)`，而双重 Q-learning 没有。
   > **练习3：** 实现双重 Q-learning，验证它能消除 Q-learning 的最大化偏差。

## 术语速查表

| 术语 | 通俗说法 | 实际含义 |
|------|----------|----------|
| TD 误差 | "更新信号" | `δ = r + γ V(s') - V(s)`，自举残差。 |
| TD(0) | "单步 TD" | 每次转移后使用下一状态估计更新。 |
| Q-learning | "离策略 RL 入门" | 用下一状态动作 max 的 TD 更新；不管行为策略如何都学习 `Q*`。 |
| SARSA | "在线策略的 Q-learning" | 使用实际下一动作的 TD 更新；学习当前 ε-贪心 π 的 `Q^π`。 |
| 期望 SARSA | "低方差 SARSA" | 用 π 下的期望替换采样的 `a'`。 |
| GLIE | "正确的探索调度" | 极限贪心且无限探索 (Greedy in the Limit with Infinite Exploration)；Q-learning 收敛所需。 |
| 自举 (Bootstrapping) | "在目标中使用当前估计" | 区分 TD 和 MC 的特征。偏差来源但大幅降低方差。 |
| 最大化偏差 | "Q-learning 过估计" | 对噪声估计取 max 向上偏差；由双重 Q-learning 修复。 |

## 延伸阅读

- [Watkins & Dayan (1992). Q-learning](https://link.springer.com/article/10.1007/BF00992698) — 原始论文和收敛证明。
- [Sutton & Barto (2018). Ch. 6 — Temporal-Difference Learning](http://incompleteideas.net/book/RLbook2020.pdf) — TD(0)、SARSA、Q-learning、期望 SARSA。
- [Hasselt (2010). Double Q-learning](https://papers.nips.cc/paper_files/paper/2010/hash/091d584fced301b442654dd8c23b3fc9-Abstract.html) — 修复最大化偏差。
- [Seijen, Hasselt, Whiteson, Wiering (2009). A Theoretical and Empirical Analysis of Expected SARSA](https://ieeexplore.ieee.org/document/4927542) — 期望 SARSA 的动机。
- [Rummery & Niranjan (1994). On-line Q-learning using connectionist systems](https://www.researchgate.net/publication/2500611_On-Line_Q-Learning_Using_Connectionist_Systems) — 创造 SARSA 名字的论文（当时称为"修正连接主义 Q-learning"）。
- [Sutton & Barto (2018). Ch. 7 — n-step Bootstrapping](http://incompleteideas.net/book/RLbook2020.pdf) — 将 TD(0) 推广到 TD(n)，从 Q-learning 到资格迹以及后来 PPO 中 GAE 的路径。
