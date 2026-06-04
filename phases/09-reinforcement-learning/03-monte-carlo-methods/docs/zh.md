# 蒙特卡洛方法 — 从完整回合中学习

> 动态规划需要模型。蒙特卡洛只需要回合。运行策略，观察回报，取平均。RL 中最简单的思想——也是解锁所有后续方法的关键。

> **【中文解读】** 动态规划需要已知环境模型，蒙特卡洛只需要完整的回合数据：执行策略、观测回报、取平均。这是 RL 中最简单的思想，也是所有后续算法（TD、Q-learning、PPO、RLHF）的基石。

**类型：** 构建
**语言：** Python
**前置知识：** Phase 9 · 01（MDP），Phase 9 · 02（动态规划）
**用时：** 约 75 分钟

## 问题引入

动态规划很优雅，但它假设你可以对每个状态和动作查询 `P(s' | s, a)`。现实世界中几乎没有什么能这样工作。机器人无法解析计算关节力矩后相机像素的分布。定价算法无法对所有可能的客户反应进行积分。LLM 无法枚举 token 后所有可能的续写。

你需要一种只需要从环境中*采样*能力的方法。运行策略。获得轨迹 `s_0, a_0, r_1, s_1, a_1, r_2, …, s_T`。用它来估计值。这就是蒙特卡洛。

从 DP 到 MC 的转变在哲学上很重要：我们从*已知模型 + 精确备份*转向*采样展开 + 平均回报*。方差增大了，但适用范围爆炸式扩展。本课之后的每个 RL 算法——TD、Q-learning、REINFORCE、PPO、GRPO——本质上都是蒙特卡洛估计器，有时在上面叠加了自举。

> **【中文解读】** 从 DP 到 MC 的核心转变：从"已知模型+精确计算"到"采样轨迹+平均回报"。方差增大了，但适用范围爆炸式扩展。PPO、RLHF 本质上都是 MC 估计器的变体。

> **【拓展：LLM中的MC】** ChatGPT 的 RLHF 训练中，对每个 prompt 采样多个回答、计算平均奖励——这就是 MC 思想在大模型训练中的直接应用。DeepSeek-R1 的 GRPO 也是基于组内采样的 MC 估计。

## 核心概念

![蒙特卡洛：展开、计算回报、取平均；首次访问 vs 每次访问](../assets/monte-carlo.svg)

**核心理念，一行概括：** `V^π(s) = E_π[G_t | s_t = s] ≈ (1/N) Σ_i G^{(i)}(s)`，其中 `G^{(i)}(s)` 是在策略 `π` 下访问 `s` 时观测到的回报。

> **【中文解读】** MC 评估的核心：状态值 = 多次经过该状态时观测到的回报的平均值。首次访问 MC 只统计每个回合中第一次访问的回报，每次访问 MC 统计所有访问。增量式均值更新 `V_new = V_old + α(target - V_old)` 是从 MC 到 TD 到所有现代 RL 算法的桥梁。

**首次访问 vs 每次访问 MC。** 给定一个多次访问状态 `s` 的回合，首次访问 MC 只计算第一次访问的回报；每次访问 MC 计算所有访问的回报。两者在极限情况下都是无偏的。首次访问更易分析（iid 样本）。每次访问每个回合利用更多数据，实践中通常收敛更快。

**增量均值。** 不存储所有回报，而是更新运行平均：

`V_n(s) = V_{n-1}(s) + (1/n) [G_n - V_{n-1}(s)]`

重新整理：`V_new = V_old + α · (target - V_old)`，其中 `α = 1/n`。将 `1/n` 替换为常数步长 `α ∈ (0, 1)` 就得到一个非平稳 MC 估计器，可以跟踪 `π` 的变化。这一步就是从 MC 到 TD 再到所有现代 RL 算法的全部跨越。

**探索现在成了问题。** DP 通过枚举触及每个状态。MC 只能看到策略访问的状态。如果 `π` 是确定性的，状态空间的整个区域永远不会被采样，其值估计永远为零。三种修复方案，按历史顺序：

> **【中文解读】** 探索问题：DP 能遍历所有状态，MC 只能看到策略访问过的状态。如果策略是确定性的，大量状态永远不会被访问。三种解决方案：探索起点（不实际）、ε-贪心（最常用）、离策略 MC（通过重要性采样从行为策略学习目标策略）。

1. **探索起点 (Exploring Starts)。** 每个回合从随机 (s, a) 对开始。保证覆盖；实践中不现实（你不能把机器人"重置"到任意状态）。
2. **ε-贪心 (ε-greedy)。** 以贪心方式对当前 Q 行动，但以概率 `ε` 选择随机动作。所有状态-动作对渐近地都会被采样。
3. **离策略 MC (Off-policy MC)。** 在行为策略 `μ` 下收集数据，通过重要性采样学习目标策略 `π`。方差高，但它是通往 DQN 等回放缓冲方法的桥梁。

**蒙特卡洛控制。** 评估 → 改进 → 评估，就像策略迭代一样，但评估是基于采样的：

1. 运行 `π`，获得一个回合。
2. 从观测回报更新 `Q(s, a)`。
3. 使 `π` 对 `Q` ε-贪心。
4. 重复。

在温和条件下（每对被无限频繁访问，`α` 满足 Robbins-Monro 条件），以概率 1 收敛到 `Q*` 和 `π*`。

## 动手实现

### 第 1 步：展开 → (s, a, r) 列表

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

无需模型，只有 `env.reset()` 和 `env.step(s, a)`。与 gym 环境接口相同，只是精简版。

### 第 2 步：计算回报（反向扫描）

```python
def returns_from(trajectory, gamma):
    returns = []
    G = 0.0
    for _, _, r in reversed(trajectory):
        G = r + gamma * G
        returns.append(G)
    return list(reversed(returns))
```

一遍扫描，`O(T)`。反向递推 `G_t = r_{t+1} + γ G_{t+1}` 避免了重复求和。

### 第 3 步：首次访问 MC 评估

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

三行代码完成工作：标记首次访问的状态，增加计数，更新运行均值。

### 第 4 步：ε-贪心 MC 控制（在线策略）

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

### 第 5 步：与 DP 金标准对比

当回合数 → ∞ 时，你的 MC 估计 `V^π` 应该与第 02 课的 DP 结果一致。实践中：4×4 网格世界上 50,000 个回合可以让你在 DP 答案的 `~0.1` 范围内。

## 常见陷阱

- **无限回合。** MC 要求回合*终止*。如果你的策略可能永远循环，设置 `max_steps` 上限并将上限视为隐式失败。随机策略的 GridWorld 经常超时——这是正常的，只要确保正确计数即可。
- **方差。** MC 使用完整回报。在长回合上，方差很大——末尾一个不幸的奖励对 `V(s_0)` 的影响同样大。TD 方法（第 04 课）通过自举来削减方差。
- **状态覆盖。** 新 Q 上平局的贪心 MC 永远只会尝试一个动作。你*必须*探索（ε-贪心、探索起点、UCB）。
- **非平稳策略。** 如果 `π` 在变化（如 MC 控制中），旧回报来自不同的策略。常数-α MC 处理这种情况；样本平均 MC 则不行。
- **离策略重要性采样。** 权重 `π(a|s)/μ(a|s)` 在轨迹上相乘。方差随视野爆炸式增长。用逐决策加权 IS 限制或切换到 TD。

## 用框架实现

2026 年蒙特卡洛方法的应用：

| 用例 | 为什么用 MC |
|------|-------------|
| 短视野游戏（二十一点、扑克） | 回合自然终止；回报干净。 |
| 已记录策略的离线评估 | 对存储轨迹求折扣回报平均。 |
| 蒙特卡洛树搜索（AlphaZero） | 树叶节点的 MC 展开指导选择。 |
| LLM RL 评估 | 对给定策略的采样补全计算平均奖励。 |
| PPO 中的基线估计 | 优势目标 `A_t = G_t - V(s_t)` 使用 MC 的 `G_t`。 |
| RL 教学 | 实际有效最简单的算法——去掉自举看核心。 |

现代深度 RL 算法（PPO、SAC）通过 `n`-步回报或 GAE 在纯 MC（完整回报）和纯 TD（单步自举）之间插值。两个端点都是同一个估计器的实例。

## 产出物

保存为 `outputs/skill-mc-evaluator.md`：

```markdown
---
name: mc-evaluator
description: 通过蒙特卡洛展开评估策略，并生成带 DP 对比（如可用）的收敛报告。
version: 1.0.0
phase: 9
lesson: 3
tags: [rl, monte-carlo, evaluation]
---

给定一个环境（回合制的，有 reset+step API）和一个策略，输出：

1. 方法。首次访问 vs 每次访问 MC。理由。
2. 回合预算。目标数量，方差诊断，预期标准误差。
3. 探索计划。ε 调度（如需要）或探索起点。
4. 金标准对比。如果是表格式的则使用 DP 最优 V*；否则使用 Q-learning / PPO 基准的界限。
5. 终止检查。最大步数上限，超时处理，非终止轨迹的处理。

拒绝在没有有限视野上限的非回合制任务上运行 MC。拒绝在表格式任务中每状态少于 100 个回合报告 V^π 估计。标记任何零方差动作的策略为探索风险。
```

## 练习题

1. **简单。** 在 4×4 网格世界上实现均匀随机策略的首次访问 MC 评估。运行 10,000 个回合。绘制 `V(0,0)` 随回合数的变化曲线，与 DP 答案对比。
   > **练习1：** 实现 MC 评估，将 V(0,0) 随回合数的收敛曲线与 DP 基准对比。
2. **中等。** 用 `ε ∈ {0.01, 0.1, 0.3}` 实现 ε-贪心 MC 控制。比较 20,000 个回合后的平均回报。曲线看起来什么样？偏差-方差权衡在哪里？
   > **练习2：** 用不同 ε 值做 MC 控制，观察探索-利用权衡。
3. **困难。** 实现带重要性采样的*离策略* MC：在均匀随机策略 `μ` 下收集数据，估计确定性最优策略 `π` 的 `V^π`。比较普通 IS vs 逐决策 IS vs 加权 IS。哪个方差最低？
   > **练习3：** 实现离策略 MC（重要性采样），比较不同 IS 方差的差异。

## 术语速查表

| 术语 | 通俗说法 | 实际含义 |
|------|----------|----------|
| 蒙特卡洛 (Monte Carlo) | "随机采样" | 通过对分布中的 iid 样本取平均来估计期望。 |
| 回报 `G_t` | "未来奖励" | 从步骤 `t` 到回合结束的折扣奖励和：`Σ_{k≥0} γ^k r_{t+k+1}`。 |
| 首次访问 MC | "每个状态只计一次" | 只有回合中首次访问才对值估计有贡献。 |
| 每次访问 MC | "使用所有访问" | 每次访问都有贡献；略有偏差但样本效率更高。 |
| ε-贪心 (ε-greedy) | "探索噪声" | 以概率 `1-ε` 选贪心动作；以概率 `ε` 选随机动作。 |
| 重要性采样 (Importance Sampling) | "修正从错误分布采样" | 用 `π(a\|s)/μ(a\|s)` 的乘积重新加权回报，从 `μ` 数据估计 `V^π`。 |
| 在线策略 (On-policy) | "从自己的数据学习" | 目标策略 = 行为策略。普通 MC、PPO、SARSA。 |
| 离策略 (Off-policy) | "从别人的数据学习" | 目标策略 ≠ 行为策略。重要性采样 MC、Q-learning、DQN。 |

## 延伸阅读

- [Sutton & Barto (2018). Ch. 5 — Monte Carlo Methods](http://incompleteideas.net/book/RLbook2020.pdf) — 经典论述。
- [Singh & Sutton (1996). Reinforcement Learning with Replacing Eligibility Traces](https://link.springer.com/article/10.1007/BF00114726) — 首次访问 vs 每次访问分析。
- [Precup, Sutton, Singh (2000). Eligibility Traces for Off-Policy Policy Evaluation](http://incompleteideas.net/papers/PSS-00.pdf) — 离策略 MC 和方差控制。
- [Mahmood et al. (2014). Weighted Importance Sampling for Off-Policy Learning](https://arxiv.org/abs/1404.6362) — 现代低方差 IS 估计器。
- [Tesauro (1995). TD-Gammon, A Self-Teaching Backgammon Program](https://dl.acm.org/doi/10.1145/203330.203343) — MC/TD 自博弈收敛到超人水平的首次大规模实证展示；本阶段后半部分每节课的概念先驱。
