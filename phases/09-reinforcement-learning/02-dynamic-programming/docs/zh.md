# 动态规划 — 策略迭代与值迭代

> 动态规划是强化学习的"作弊版"——你已经知道转移概率和奖励函数，只需反复迭代 Bellman 方程直到 `V` 或 `π` 不再变化。它是所有基于采样的方法试图逼近的"金标准"。

> **【中文解读】** 动态规划是强化学习的"作弊版"——你已知环境的转移概率和奖励函数，只需反复迭代 Bellman 方程直到收敛。它是所有采样方法（Q-learning、PPO 等）的"金标准"参照。

**类型：** 构建
**语言：** Python
**前置知识：** Phase 9 · 01（MDP）
**用时：** 约 75 分钟

## 问题引入

你有一个已知模型的 MDP：可以对任意状态-动作对查询 `P(s' | s, a)` 和 `R(s, a, s')`。库存管理者知道需求分布。棋盘游戏有确定性转移。网格世界只需四行 Python。你有一个*模型*。

无模型 RL（Q-learning、PPO、REINFORCE）是为没有模型的情况发明的——你只能从环境中采样。但当你确实有模型时，有更快、更好的方法：动态规划。Bellman 在 1957 年设计了它们。它们至今定义着正确性：当人们说"这个 MDP 的最优策略"时，他们指的是 DP 会返回的策略。

> **【中文解读】** 当你已知环境模型（转移概率和奖励函数）时，动态规划可以精确求解最优策略。它是无模型 RL 的"参照答案"——用 DP 算出的 V* 来验证 Q-learning 是否正确。AlphaZero 的 MCTS 搜索本质上也是在做 Bellman 备份。

> **【拓展：AlphaZero/MCTS】** AlphaZero 的蒙特卡洛树搜索 (MCTS) 本质上是异步版本的 Bellman 备份——在搜索树中迭代值函数。DP 的思想贯穿了从游戏 AI 到大模型推理的全链条。

在 2026 年你需要动态规划有三个原因。第一，RL 研究中的每个表格式环境（GridWorld、FrozenLake、CliffWalking）都用 DP 求解以产生金标准策略。第二，精确值让你能*调试*采样方法：如果 Q-learning 对 `V*(s_0)` 的估计与 DP 答案相差 30%，你的 Q-learning 就有 bug。第三，现代离线 RL 和规划方法（MCTS、AlphaZero 的搜索、Phase 9 · 10 中基于模型的 RL）都在学习或给定的模型上迭代 Bellman 备份。

## 核心概念

![策略迭代和值迭代，并排对比](../assets/dp.svg)

**两种算法，都是对 Bellman 方程做不动点迭代。**

> **【中文解读】** 两种算法都是对 Bellman 方程做不动点迭代。策略迭代：交替执行"策略评估"和"策略改进"直到策略不变；值迭代：将两者合并为一步，直接取 max。两者最终收敛到同一个最优值函数 V*。

**策略迭代 (Policy Iteration)。** 交替执行两个步骤直到策略不再变化。

1. *评估：* 给定策略 `π`，通过反复应用 `V(s) ← Σ_a π(a|s) Σ_{s',r} P(s',r|s,a) [r + γ V(s')]` 直到收敛来计算 `V^π`。
2. *改进：* 给定 `V^π`，使 `π` 对 `V^π` 贪心：`π(s) ← argmax_a Σ_{s',r} P(s',r|s,a) [r + γ V(s')]`。

收敛性有保证，因为 (a) 每次改进步要么保持 `π` 不变，要么严格增加某个状态的 `V^π`，(b) 确定性策略空间是有限的。即使对大状态空间，通常也只需约 5-20 次外迭代即可收敛。

**值迭代 (Value Iteration)。** 将评估和改进合并为一次扫描。应用 Bellman *最优性*方程：

`V(s) ← max_a Σ_{s',r} P(s',r|s,a) [r + γ V(s')]`

重复直到 `max_s |V_{new}(s) - V(s)| < ε`。最后通过取贪心动作提取策略。每次迭代更快——没有内部评估循环——但通常需要更多迭代才能收敛。

**广义策略迭代 (Generalized Policy Iteration, GPI)。** 统一框架。值函数和策略锁定在双向改进循环中；任何驱动两者趋向一致的方法（异步值迭代、修正策略迭代、Q-learning、Actor-Critic、PPO）都是 GPI 的实例。

> **【拓展：GPI→PPO/RLHF】** 广义策略迭代 (GPI) 是统一框架：Q-learning、Actor-Critic、PPO 本质上都是 GPI 的实例。理解了 DP 的 GPI，你就理解了 ChatGPT 背后 RLHF 训练循环的设计哲学。

**为什么 `γ < 1` 很重要。** Bellman 算子是无穷范数中的 `γ`-压缩映射：`||T V - T V'||_∞ ≤ γ ||V - V'||_∞`。压缩映射意味着唯一不动点和几何收敛。去掉 `γ < 1` 就失去保证——你需要有限视野或吸收终止状态。

## 动手实现

### 第 1 步：构建 GridWorld MDP 模型

使用第 01 课中相同的 4×4 网格世界。我们添加一个随机变体：以概率 `0.1` 智能体会滑向随机垂直方向。

```python
SLIP = 0.1

def transitions(state, action):
    if state == TERMINAL:
        return [(state, 0.0, 1.0)]
    outcomes = []
    for direction, prob in action_probs(action):
        outcomes.append((apply_move(state, direction), -1.0, prob))
    return outcomes
```

`transitions(s, a)` 返回 `(s', r, p)` 的列表。这就是整个模型。

### 第 2 步：策略评估

给定策略 `π(s) = {动作: 概率}`，迭代 Bellman 方程直到 `V` 不再变化：

```python
def policy_evaluation(policy, gamma=0.99, tol=1e-6):
    V = {s: 0.0 for s in states()}
    while True:
        delta = 0.0
        for s in states():
            v = sum(pi_a * sum(p * (r + gamma * V[s_prime])
                              for s_prime, r, p in transitions(s, a))
                   for a, pi_a in policy(s).items())
            delta = max(delta, abs(v - V[s]))
            V[s] = v
        if delta < tol:
            return V
```

### 第 3 步：策略改进

用对 `V` 贪心的策略替换 `π`。如果 `π` 没有变化，返回——我们已达到最优。

```python
def policy_improvement(V, gamma=0.99):
    new_policy = {}
    for s in states():
        best_a = max(
            ACTIONS,
            key=lambda a: sum(p * (r + gamma * V[s_prime])
                              for s_prime, r, p in transitions(s, a)),
        )
        new_policy[s] = best_a
    return new_policy
```

### 第 4 步：组装

```python
def policy_iteration(gamma=0.99):
    policy = {s: "up" for s in states()}   # 任意初始策略
    for _ in range(100):
        V = policy_evaluation(lambda s: {policy[s]: 1.0}, gamma)
        new_policy = policy_improvement(V, gamma)
        if new_policy == policy:
            return V, policy
        policy = new_policy
```

在 4×4 网格上典型收敛：4-6 次外迭代。输出 `V*(0,0) ≈ -6` 和一个严格减少步数的策略。

### 第 5 步：值迭代（单循环版本）

```python
def value_iteration(gamma=0.99, tol=1e-6):
    V = {s: 0.0 for s in states()}
    while True:
        delta = 0.0
        for s in states():
            v = max(sum(p * (r + gamma * V[s_prime])
                       for s_prime, r, p in transitions(s, a))
                   for a in ACTIONS)
            delta = max(delta, abs(v - V[s]))
            V[s] = v
        if delta < tol:
            break
    policy = policy_improvement(V, gamma)
    return V, policy
```

相同的不动点，更少的代码行。

## 常见陷阱

- **忘记处理终止状态。** 如果对吸收状态应用 Bellman 方程，它仍会选出一个不改变任何事的"最佳动作"。用 `if s == terminal: V[s] = 0` 防护。
- **无穷范数 vs L2 收敛。** 使用 `max |V_new - V|`，而非平均值。理论保证是基于无穷范数的。
- **原地 vs 同步更新。** 原地更新 `V[s]`（Gauss-Seidel）比单独的 `V_new` 字典（Jacobi）收敛更快。生产代码使用原地更新。
- **策略平局。** 如果两个动作有相同的 Q 值，`argmax` 可能每次迭代的平局打破方式不同，导致"策略稳定"检查振荡。使用稳定的平局打破方式（固定顺序中的第一个动作）。
- **状态空间爆炸。** DP 每次扫描的复杂度是 `O(|S| · |A|)`。适用于约 10⁷ 个状态。超过这个范围，需要函数近似（Phase 9 · 05 起的章节）。

## 用框架实现

2026 年，DP 是正确性基准和规划器的内循环：

| 用例 | 方法 |
|------|------|
| 精确求解小型表格式 MDP | 值迭代（更简单）或策略迭代（更少外迭代） |
| 验证 Q-learning / PPO 实现 | 在玩具环境上与 DP 最优 V* 对比 |
| 基于模型的 RL（Phase 9 · 10） | 在学习的转移模型上做 Bellman 备份 |
| AlphaZero / MuZero 中的规划 | 蒙特卡洛树搜索 = 异步 Bellman 备份 |
| 离线 RL（CQL, IQL） | 保守 Q 迭代——带 OOD 动作惩罚的 DP |

每当有人说"最优值函数"，他们指的是"DP 不动点"。当你在论文中看到 `V*` 或 `Q*`，想象的就是这个循环。

## 产出物

保存为 `outputs/skill-dp-solver.md`：

```markdown
---
name: dp-solver
description: 通过策略迭代或值迭代精确求解小型表格式 MDP。报告收敛行为。
version: 1.0.0
phase: 9
lesson: 2
tags: [rl, dynamic-programming, bellman]
---

给定一个已知模型的 MDP，输出：

1. 选择。策略迭代 vs 值迭代。根据 |S|、|A|、γ 论证。
2. 初始化。V_0，起始策略。收敛敏感性。
3. 停止条件。无穷范数容差 ε。预期扫描次数。
4. 验证。精确计算的 V*(s_0)。提取贪心策略。
5. 用途。此基准将如何用于调试/评估基于采样的方法。

拒绝在状态空间 > 10⁷ 上运行 DP。拒绝在没有无穷范数检查的情况下声称收敛。对无限视野任务标记任何 γ ≥ 1 为保证违反。
```

## 练习题

1. **简单。** 用 `γ ∈ {0.9, 0.99}` 在 4×4 网格世界上运行值迭代。多少次扫描后 `max |ΔV| < 1e-6`？将 `V*` 打印为 4×4 网格。
   > **练习1：** 用不同的折扣因子 γ 运行值迭代，观察收敛速度如何随 γ 变化。
2. **中等。** 在*随机*网格世界（滑移概率 `0.1`）上比较策略迭代 vs 值迭代。统计：扫描次数、运行时间、最终 `V*(0,0)`。哪个在迭代次数上收敛更快？在运行时间上呢？
   > **练习2：** 比较策略迭代和值迭代在随机网格世界中的收敛速度（迭代次数和运行时间）。
3. **困难。** 构建修正策略迭代：在评估步中只运行 `k` 次扫描而非到收敛。绘制 `V*(0,0)` 误差 vs `k` 的图，`k ∈ {1, 2, 5, 10, 50}`。曲线告诉你评估/改进之间的什么权衡？
   > **练习3：** 实现修正策略迭代（评估步只迭代 k 次），探究评估精度与改进效率的权衡。

## 术语速查表

| 术语 | 通俗说法 | 实际含义 |
|------|----------|----------|
| 策略迭代 (Policy Iteration) | "DP 算法" | 交替执行评估（`V^π`）和改进（对 `V^π` 贪心的 `π`）直到策略不变。 |
| 值迭代 (Value Iteration) | "更快的 DP" | 单次扫描中应用 Bellman 最优性备份；几何收敛到 `V*`。 |
| Bellman 算子 | "递推式" | `(T V)(s) = max_a Σ P (r + γ V(s'))`；无穷范数中的 `γ`-压缩映射。 |
| 压缩映射 (Contraction) | "为什么 DP 收敛" | 任何满足 `\|\|T x - T y\|\| ≤ γ \|\|x - y\|\|` 的算子 `T` 都有唯一不动点。 |
| GPI | "一切都是 DP" | 广义策略迭代：任何驱动 `V` 和 `π` 趋向一致的方法。 |
| 同步更新 (Synchronous Update) | "Jacobi 式" | 在整个扫描中使用旧的 `V`；清晰可分析但更慢。 |
| 原地更新 (In-place Update) | "Gauss-Seidel 式" | 使用正在更新的 `V`；实践中收敛更快。 |

## 延伸阅读

- [Sutton & Barto (2018). Ch. 4 — Dynamic Programming](http://incompleteideas.net/book/RLbook2020.pdf) — 策略迭代和值迭代的经典呈现。
- [Bertsekas (2019). Reinforcement Learning and Optimal Control](http://www.athenasc.com/rlbook.html) — 压缩映射论证的严谨处理。
- [Puterman (2005). Markov Decision Processes](https://onlinelibrary.wiley.com/doi/book/10.1002/9780470316887) — 修正策略迭代及其收敛分析。
- [Howard (1960). Dynamic Programming and Markov Processes](https://mitpress.mit.edu/9780262582300/dynamic-programming-and-markov-processes/) — 原始策略迭代论文。
- [Bertsekas & Tsitsiklis (1996). Neuro-Dynamic Programming](http://www.athenasc.com/ndpbook.html) — 从 DP 到近似 DP / 深度 RL 的桥梁，后续每节课都在使用。
