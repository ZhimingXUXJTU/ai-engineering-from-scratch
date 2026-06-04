# 多智能体强化学习

> 单智能体 RL 假设环境是平稳的。放入两个同时学习的智能体后，每个智能体都成了对方环境的一部分——环境不再平稳，马尔可夫假设被打破。多智能体 RL 就是处理"大家都在变"时的收敛问题。

> **【中文解读】** 单智能体 RL 假设环境是平稳的。但放入两个同时学习的智能体后，每个智能体都成了对方环境的一部分——环境不再平稳，马尔可夫假设被打破。多智能体 RL 就是处理"大家都在变"时的收敛问题。

**类型：** 构建
**语言：** Python
**前置知识：** Phase 9 · 04（Q-learning），Phase 9 · 06（REINFORCE），Phase 9 · 07（Actor-Critic）
**用时：** 约 45 分钟

## 问题引入

机器人学习导航房间是单智能体 RL 问题。足球队不是。AlphaStar 对战星际争霸对手不是。竞标智能体的市场不是。两辆车在四向停车让路口协商不是。许多对许多的现实世界问题都不是。

在每个多智能体设置中，从任何一个智能体的视角来看，其他智能体*就是*环境的一部分。当它们学习和改变行为时，环境变得非平稳。马尔可夫性质——"下一状态只取决于当前状态和我的动作"——被违反了，因为下一状态还取决于*其他*智能体选择了什么，而它们的策略是移动目标。

这打破了表格式收敛证明（Q-learning 的保证假设平稳环境）。也打破了朴素的深度 RL：智能体在循环中互相追逐，永远不收敛到稳定策略。你需要多智能体专用技术：集中训练/分布执行、反事实基线、联盟训练、自我博弈。

2026 年应用：机器人群体、交通路由、自动驾驶车队、市场模拟器、多智能体 LLM 系统（Phase 16），以及任何有多个智能玩家的游戏。

> **【中文解读】** 多智能体 RL 的核心挑战：非平稳性（其他智能体也在学习）、信用分配（谁该得到奖励？）、联合动作空间爆炸、部分可观察性。四种主要范式：独立学习（简单但不保证收敛）、CTDE（训练时集中、执行时分布）、自我博弈（AlphaZero）、联盟训练（AlphaStar）。

> **【拓展：多智能体→LLM Agent系统】** 2026 年最热门的 MARL 应用是多智能体 LLM 系统：多个大模型 Agent 协作完成复杂任务。Claude Code 的 multi-agent 模式、AutoGen、CrewAI 等框架本质上都是 MARL 思想在语言 Agent 领域的延伸。

## 核心概念

![四种 MARL 范式：独立、集中评论家、自我博弈、联盟](../assets/marl.svg)

**形式化：马尔可夫博弈 (Markov Game)。** MDP 的推广：状态 `S`，联合动作 `a = (a_1, …, a_n)`，转移 `P(s' | s, a)`，和每个智能体的奖励 `R_i(s, a, s')`。每个智能体 `i` 在自己的策略 `π_i` 下最大化自己的回报。如果奖励相同，是**完全合作型**。如果是零和的，是**对抗型**。如果混合，是**一般和型**。

**核心挑战：**

- **非平稳性。** 从智能体 `i` 视角的 `P(s' | s, a_i)` 依赖于 `π_{-i}`，后者在变化。
- **信用分配。** 在共享奖励下，哪个智能体导致的？
- **探索协调。** 智能体必须探索互补策略，而非冗余探索相同状态。
- **可扩展性。** 联合动作空间随 `n` 指数增长。
- **部分可观察性。** 每个智能体只看到自己的观测；全局状态是隐藏的。

**四种主导范式：**

**1. 独立 Q-learning / 独立 PPO (IQL, IPPO)。** 每个智能体学习自己的 Q 或策略，将其他智能体视为环境的一部分。简单，有时有效（特别是当经验回放充当平滑的智能体建模技巧时）。理论收敛性：无。实践中：对松耦合任务可行，紧耦合任务不行。

**2. 集中训练、分布执行 (CTDE)。** 最常见的现代范式。每个智能体有自己的*策略* `π_i`，基于局部观测 `o_i` 做决策——部署时标准分布式执行。在*训练*时，集中评论家 `Q(s, a_1, …, a_n)` 基于完整全局状态和联合动作做决策。示例：
- **MADDPG**（Lowe 等人 2017）：每个智能体带集中评论家的 DDPG。
- **COMA**（Foerster 等人 2017）：反事实基线——问"如果我采取动作 `a'` 而非实际动作，奖励会是多少？"——隔离我的贡献。
- **MAPPO** / **IPPO** 带共享评论家（Yu 等人 2022）：带集中值函数的 PPO。2026 年合作 MARL 的主导方法。
- **QMIX**（Rashid 等人 2018）：值分解——`Q_tot(s, a) = f(Q_1(s, a_1), …, Q_n(s, a_n))` 具有单调混合。

**3. 自我博弈 (Self-play)。** 同一智能体的两个副本互相对战。对手的策略*就是*我过去快照的策略。AlphaGo / AlphaZero / MuZero。OpenAI Five。对零和博弈效果最好；训练信号是对称的。

**4. 联盟训练 (League Play)。** 将自我博弈扩展到一般和 / 对抗环境：保持过去和当前策略的种群，从联盟中采样对手进行训练。添加剥削者（专门击败当前最强）和主剥削者（专门击败剥削者）。AlphaStar（星际争霸 II）。当博弈存在"石头剪刀布"策略循环时需要。

**通信。** 允许智能体相互发送学习到的消息 `m_i`。在合作设置中有效。Foerster 等人（2016）展示了可微的智能体间通信可以端到端训练。今天的基于 LLM 的多智能体系统（Phase 16）本质上用自然语言通信。

## 动手实现

本课使用 6×6 网格世界，有两个合作智能体。它们从对角出发，必须到达共享目标。共享奖励：任一智能体仍在移动时每步 `-1`，两个都到达时 `+10`。参见 `code/main.py`。

### 第 1 步：多智能体环境

```python
class CoopGridWorld:
    def __init__(self):
        self.size = 6
        self.goal = (5, 5)

    def reset(self):
        return ((0, 0), (5, 0))  # 两个智能体

    def step(self, state, actions):
        a1, a2 = state
        new1 = move(a1, actions[0])
        new2 = move(a2, actions[1])
        done = (new1 == self.goal) and (new2 == self.goal)
        reward = 10.0 if done else -1.0
        return (new1, new2), reward, done
```

*联合*动作空间是 `|A|² = 16`。全局状态是两个位置。

### 第 2 步：独立 Q-learning

每个智能体运行自己的 Q 表，以联合状态为键。每步：两个都选 ε-贪心动作，收集联合转移，各自用共享奖励更新自己的 Q。

```python
def independent_q(env, episodes, alpha, gamma, epsilon):
    Q1, Q2 = defaultdict(default_q), defaultdict(default_q)
    for _ in range(episodes):
        s = env.reset()
        while not done:
            a1 = epsilon_greedy(Q1, s, epsilon)
            a2 = epsilon_greedy(Q2, s, epsilon)
            s_next, r, done = env.step(s, (a1, a2))
            target1 = r + gamma * max(Q1[s_next].values())
            target2 = r + gamma * max(Q2[s_next].values())
            Q1[s][a1] += alpha * (target1 - Q1[s][a1])
            Q2[s][a2] += alpha * (target2 - Q2[s][a2])
            s = s_next
```

在这个任务上有效，因为奖励密集且一致。在紧耦合任务上失败（例如，一个智能体必须*等待*另一个）。

### 第 3 步：带分解值更新的集中 Q

在联合动作上使用一个 Q：`Q(s, a_1, a_2)`。从共享奖励更新。执行时通过边缘化分布：`π_i(s) = argmax_{a_i} max_{a_{-i}} Q(s, a_1, a_2)`。以指数联合动作空间换取*正确*的全局视角。

### 第 4 步：简单自我博弈（对抗型 2 智能体）

同一智能体，两个角色。训练智能体 A 对抗智能体 B；`K` 个回合后，将 A 的权重复制到 B。对称训练，一致进步。AlphaZero 配方的缩影。

## 常见陷阱

- **非平稳回放。** 独立智能体的经验回放比单智能体更差，因为旧转移是由现已过时的对手生成的。修复：重新标记或按新近度加权。
- **信用分配歧义。** 长回合后的共享奖励；无法明确说哪个智能体贡献了什么。修复：反事实基线（COMA），或每个智能体的奖励塑形。
- **策略漂移 / 追逐。** 每个智能体的最佳回应随其他智能体更新而变化。修复：集中评论家，慢学习率，或轮流冻结。
- **通过协调的奖励黑客行为。** 智能体找到设计者未预期的协调利用。拍卖智能体收敛到出价零。修复：仔细的奖励设计，行为约束。
- **探索冗余。** 两个智能体探索相同的状态-动作对。修复：每个智能体的熵奖励，或角色条件化。
- **联盟循环。** 纯自我博弈可能陷入支配循环。修复：带多样对手的联盟训练。
- **样本爆炸。** `n` 个智能体 × 状态空间 × 联合动作。用函数近似缓解；分解动作空间（每个智能体一个策略输出头）。

## 用框架实现

2026 年 MARL 应用版图：

| 领域 | 方法 | 备注 |
|------|------|------|
| 合作导航 / 操作 | MAPPO / QMIX | CTDE；共享评论家 + 分布式演员。 |
| 双人游戏（国际象棋、围棋、扑克） | 带 MCTS 的自我博弈（AlphaZero） | 零和；对称训练。 |
| 复杂多人游戏（Dota、星际争霸） | 联盟训练 + 模仿预训练 | OpenAI Five，AlphaStar。 |
| 自动驾驶车队 | CTDE MAPPO / 带注意力的 PPO | 部分观察；可变团队规模。 |
| 拍卖市场 | 博弈论均衡 + RL | 当 `n` → ∞ 时用平均场 RL。 |
| LLM 多智能体系统（Phase 16） | 自然语言通信 + 角色条件化 | 在智能体规划层的 RL 循环。 |

2026 年，MARL 最大的增长领域是基于 LLM 的：语言模型智能体群体进行协商、辩论、构建软件。RL 出现在*轨迹级*输出的偏好优化上，而非 token 级（Phase 16 · 03）。

## 产出物

保存为 `outputs/skill-marl-architect.md`：

```markdown
---
name: marl-architect
description: 为给定任务选择正确的多智能体 RL 范式（IPPO、CTDE、自我博弈、联盟）。
version: 1.0.0
phase: 9
lesson: 10
tags: [rl, multi-agent, marl, self-play]
---

给定一个有 `n` 个智能体的任务，输出：

1. 范式分类。合作 / 对抗 / 一般和。附理由。
2. 算法。IPPO / MAPPO / QMIX / 自我博弈 / 联盟。理由关联耦合紧密度和奖励结构。
3. 信息访问。集中训练（什么全局信息给评论家）？分布式执行？
4. 信用分配。反事实基线、值分解、或奖励塑形。
5. 探索计划。每个智能体熵、基于种群的训练、或联盟。

拒绝在紧耦合合作任务上使用独立 Q-learning。拒绝在有循环风险的一般和博弈上推荐自我博弈。标记任何没有固定对手评估的 MARL 管线（挑拣的自我博弈数据很常见）。
```

## 练习题

1. **简单。** 在 2 智能体合作 GridWorld 上训练独立 Q-learning。多少回合后平均回报 > 0？绘制联合学习曲线。
2. **中等。** 添加"协调"任务：只有当两个智能体在同一轮踏上目标时才算到达。独立 Q 还能收敛吗？什么出了问题？
3. **困难。** 为 MAPPO 风格训练实现集中评论家，在协调任务上与独立 PPO 比较收敛速度。

## 术语速查表

| 术语 | 通俗说法 | 实际含义 |
|------|----------|----------|
| 马尔可夫博弈 | "多智能体 MDP" | `(S, A_1, …, A_n, P, R_1, …, R_n)`；每个智能体有自己的奖励。 |
| CTDE | "集中训练分布执行" | 训练时联合评论家；每个智能体的策略只用局部观测。 |
| IPPO | "独立 PPO" | 每个智能体独立运行 PPO。简单基线；经常被低估。 |
| MAPPO | "多智能体 PPO" | 带基于全局状态的集中值函数的 PPO。 |
| QMIX | "单调值分解" | `Q_tot = f_monotone(Q_1, …, Q_n)` 允许分布式 argmax。 |
| COMA | "反事实多智能体" | 优势 = 我的 Q 减去对我的动作边缘化后的期望 Q。 |
| 自我博弈 | "智能体 vs 过去的自己" | 单智能体，两个角色；零和博弈的标准。 |
| 联盟训练 | "种群训练" | 缓存过去策略，从池中采样对手；处理策略循环。 |

## 延伸阅读

- [Lowe et al. (2017). Multi-Agent Actor-Critic for Mixed Cooperative-Competitive Environments (MADDPG)](https://arxiv.org/abs/1706.02275) — 带集中评论家的 CTDE。
- [Foerster et al. (2017). Counterfactual Multi-Agent Policy Gradients (COMA)](https://arxiv.org/abs/1705.08926) — 用于信用分配的反事实基线。
- [Rashid et al. (2018). QMIX: Monotonic Value Function Factorisation](https://arxiv.org/abs/1803.11485) — 带单调性的值分解。
- [Yu et al. (2022). The Surprising Effectiveness of PPO in Cooperative Multi-Agent Games (MAPPO)](https://arxiv.org/abs/2103.01955) — PPO 在 MARL 中惊人地强。
- [Vinyals et al. (2019). Grandmaster level in StarCraft II using multi-agent reinforcement learning (AlphaStar)](https://www.nature.com/articles/s41586-019-1724-z) — 大规模联盟训练。
- [Silver et al. (2017). Mastering the game of Go without human knowledge (AlphaGo Zero)](https://www.nature.com/articles/nature24270) — 零和博弈中的纯自我博弈。
- [Sutton & Barto (2018). Ch. 15 — Neuroscience & Ch. 17 — Frontiers](http://incompleteideas.net/book/RLbook2020.pdf) — 包括教科书对多智能体设置的简要处理，以及 CTDE 旨在解决的非平稳性问题。
- [Zhang, Yang & Başar (2021). Multi-Agent Reinforcement Learning: A Selective Overview](https://arxiv.org/abs/1911.10635) — 涵盖合作、竞争和混合 MARL 的调查，附收敛结果。
