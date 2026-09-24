# 动态规划 策略 代代与价值 代代

> 动态编程是与欺骗的RL. 你已经知道过渡和奖励函数; 你只是重复贝尔曼方程直到`V`或`π`采样方法都试图接近的基准.

> **【中文解读】**动态规划是强化学习的"作弊版"你已知环境的转移概率和奖励函数,只需反复代 Bellman 方程直到收.

**Type:** Build | **类型:** 动手
**Languages:** Python | **语言:** Python
**Prerequisites:** Phase 9 · 01 (MDPs) | **前置知识:** Phase 9 · 01 (MDP)
**Time:** ~75 minutes | **时间:** ~75 分钟

## 问题 问题引入

您有已知模型的MDP:您可以查询`P(s' | s, a)`其他`R(s, a, s')`对于任何状态动作对.库存管理员知道需求分布.一个板游戏有确定性过渡.一个网格世界是四行Python.你有一个 *模型*.

> 你有一个已知模型的MDP:你可以查询任意状态动作对的`P(s' | s, a)`和 `R(s, a, s')`│ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │

无模型RL (Q-learning,PPO,REINFORCE) 是为没有模型的情况下发明的.但当你有一个时,有更快,更好的方法:动态编程.贝尔曼在1957年设计它们.他们仍然定义了正确性:当人们说"最佳政策为这个MDP",他们意味着政策DP将返回.

> 无模型RL(Q-学习、PPO、REINFORCE) 是为没有模型的情况发明的你只能从环境中采样.但是当你有模型时,有更快更好的方法:动态规划.贝尔曼在1957年设计它们.

> **【中文解读】**当你知道环境模型 (转移概率和奖励函数) 时,动态规划可以精确查找最优的策略――它是没有模型的RL"参照答案"使用DP计算的V*来验证Q学习是否正确――阿尔法零的MCTS搜索本质上也是在做贝尔曼备份――

> **【拓展：AlphaZero/MCTS】**根据AlphaZero的Monte Carlo树搜索 (MCTS) 基本上是Bellman备份的异步版本.

首先,在RL研究中每个表格环境 (GridWorld,FrozenLake,CliffWalking) 都被DP解决以制造金标准政策.`V*(s_0)`第三,现代的离线RL和规划方法 (MCTS,AlphaZero的搜索,9 · 10阶段的模型基于RL) 都会反复对学习或给定的模型进行贝尔曼备份.

> 你在2026年需要它们,原因有三.第一,RL研究中的每个表格环境 (GridWorld、FrozenLake、CliffWalking) 都用DP 求解以产生金标准策略.`V*(s_0)`根据"新课程"的研究,你在学习或学习中发现了一些问题.

## 概念的核心概念

![Policy iteration and value iteration, side by side](../assets/dp.svg)

**Two algorithms, both fixed-point iteration on Bellman.**

> **两种算法，都是对 Bellman 方程做不动点迭代。**

> **【中文解读】**两种算法都是对贝尔曼方程做不动点代的. 策略代:交替执行"策略评估"和"策略改进"直到策略不变; 值代:将两者合并为一步,直接取最大.

**Policy iteration.**交替两步,直到政策停止变化.

> **策略迭代。**交替执行两个步骤,直到策略不再改变.

1. *评估:* 给定政策`π`计算`V^π`通过多次应用`V(s) ← Σ_a π(a|s) Σ_{s',r} P(s',r|s,a) [r + γ V(s')]`直到它融合.
   给定策略`π`让我们一起去.`V^π`收──
2. *改善:* 提供`V^π`制造`π`贪的子`V^π`其他`π(s) ← argmax_a Σ_{s',r} P(s',r|s,a) [r + γ V(s')]`现在,我们要去.
   给定`V^π`让我们`π`对于`V^π`贪心.

由于 (a) 每个改进步骤都保持了`π`相同或严格增加`V^π`对于某些状态, (b) 确定性政策的空间是有限的. 通常,即使是大型状态空间,也会在520外表代中融合.

> 收性是有保证的,因为 (a) 每次改进要保持`π`不变,要么严格增加某种状态.`V^π`确定性策略空间有限.即使是大型状态空间,通常只需要5-20次外层代.

**Value iteration.**运用贝尔曼 *优化*方程:

`V(s) ← max_a Σ_{s',r} P(s',r|s,a) [r + γ V(s')]`

重复到`max_s |V_{new}(s) - V(s)| < ε`通过采取贪的行动,将政策提取到最后. 严格速度每次代 没有内部评估循环,但通常需要更多的代来融合.

> **值迭代。**通过Bellman的 *最优性* 方法,每代人都会严格更快,但通常需要更多的代人才能获得.

**Generalized policy iteration (GPI).**统一框架. 价值函数和政策锁定在双向改进循环中;任何驱动两者对相互一致性 (异步值代,修改政策代,Q-学习,演员批评,PPO) 的方法都是GPI的一个实例.

> **【拓展：GPI→PPO/RLHF】**广义策略代 (GPI) 是统一框架:Q-学习、演员批判、PPO 本质上都是GPI的实例――理解DP的GPI,你就理解了ChatGPT背后的RLHF训练循环的设计哲学――

**Why `γ < 1` matters.**贝尔曼操作员是`γ`- 标准中的缩减:`||T V - T V'||_∞ ≤ γ ||V - V'||_∞`缩小意味着独特的固定点和几何融合.`γ < 1`您需要一个有限的视界或吸收终端状态.

> **为什么 `γ < 1` 很重要。**贝尔曼的算子在下`γ`压缩意味着唯一的不动点和几何收收.`γ < 1`没有保证你需要有限的视野或吸收终止状态.

## 建立它,实现它.
```figure
value-iteration-gamma
```

## 建立它

### 步骤1:构建GridWorldMDP模型

我们将一个性变体添加到:与概率`0.1`机器人滑向一个随机垂直方向.

> 通过使用第01课中相同的4×4格式世界.`0.1`智能体会滑向随机垂直方向.

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

`transitions(s, a)`返回列表`(s', r, p)`这就是整个模型.

> `transitions(s, a)`返回`(s', r, p)`列表――这是整个模型――

### 步骤2:政策评估

考虑到政策`π(s) = {action: prob}`求求求求求求求求求求求求求求求求求求求求求求求求求求求求求求求求求求求求求求求求求求求求求求求求求求求求求求求求求求求求求求求求求求求求求求求求求求求求求求求求求求求求求求求求求求求求求求求求求求求求求求求求求求求求求求求求求求求求求求求求求求求求求求求求求求求求求求求求求求求求求求求求求求求求求求求求求求求求求求求求求求求求求求求求求求求求求求求求求求求求求求求求求求求求求求求求求求求求求求求求求求求求求求求求求求求求求求求求求求求求求求求求求求求求求求求求求求求求求求求求求求求求求求求求求求求求求求求求求求求求求求求求求求求求求求求求求求求求求求求求求求求求求求求求求求求求求求求求求求求求求求求求求求求求求求求求求求求求求求求求求求求求求求求求求求求求求求求求求求求求求求求求求求求求求求求求求求求求求求求求求求求求求求求求求求求求求求求求求求求求求求求求求求求求求`V`停止移动:

> 给定策略`π(s) = {action: prob}`代贝尔曼的路程直到`V`变化:

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

### 第三步:政策改进

取代`π`随着贪的政策,`V`如果`π`没有改变,返回我们处于最佳状态.

> 将`π`替换为对`V`贪心的策略――如果`π`没有变化,回来我们已经达到最优.

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

### 步骤 4: 它们在一起

```python
def policy_iteration(gamma=0.99):
    policy = {s: "up" for s in states()}   # arbitrary start
    for _ in range(100):
        V = policy_evaluation(lambda s: {policy[s]: 1.0}, gamma)
        new_policy = policy_improvement(V, gamma)
        if new_policy == policy:
            return V, policy
        policy = new_policy
```

典型的4×4:46外表代.输出`V*(0,0) ≈ -6`政策将严格减少步骤数量.

> ,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,`V*(0,0) ≈ -6`和一个严格减少步数的策略.

### 步骤5:值回复 (单循环版本)

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

只有一个定点,更少的代码.

> 同样的不动点,更少的代码行数.

## 陷

- **Forgetting to handle terminals.**如果把贝尔曼应用到吸收状态,它仍然会采取"最佳行动",`if s == terminal: V[s] = 0`现在,我们要去.
  **忘记处理终止状态。**如果对吸收状态应用贝尔曼,它仍然会选择一个"最佳动作",但没有什么改变.`if s == terminal: V[s] = 0`保护
- **Sup-norm vs L2 convergence.**使用`max |V_new - V|`理论上,保证是根据标准.
  **Sup 范数 vs L2 收敛。**使用 `max |V_new - V|`理论保证在超级范数上.
- **In-place vs synchronous updates.**更新`V[s]`现场 (高斯-西德尔) 趋于比单独的相近速度更快.`V_new`产品代码使用现场.
  **原地更新 vs 同步更新。**原地更新`V[s]`比较单独的`V_new`字典(Jacob)收更快──生产代码使用原地更新──
- **Policy ties.**如果两个动作的Q值等,`argmax`每次代可能会不同地打破联系,导致"政策稳定"检查振荡. 使用稳定打破 (按固定顺序的第一步).
  **策略平局。**如果两个动作的Q值相等,`argmax`每次可能以不同的方式打破平局,导致"策略稳定"检查振荡.
- **State-space explosion.**士是`O(|S| · |A|)`通过扫描,可达到107个状态.除此之外,需要函数近似 (9 · 05 阶段及以上).
  **状态空间爆炸。**每次扫描都是`O(|S| · |A|)`△适用于约107个状态.

## 用它实现框架

在2026年,DP是规划者的正确性基线和内部循环:

> 2026年,DP 是正确性基线和规划器的内循环:

| Use case | Method |
|----------|--------|
| Use case / 用例 | Method / 方法 |
| Solve a small tabular MDP exactly / 精确求解小型表格 MDP | Value iteration (simpler) or policy iteration (fewer outer steps) / 值迭代（更简单）或策略迭代（更少外层步数） |
| Verify a Q-learning / PPO implementation / 验证 Q-learning/PPO 实现 | Compare to DP-optimal V* on a toy environment / 在玩具环境上与 DP 最优 V* 比较 |
| Model-based RL (Phase 9 · 10) / 基于模型的 RL | Bellman backup on a learned transition model / 在学习的转移模型上做 Bellman 备份 |
| Planning in AlphaZero / MuZero / AlphaZero/MuZero 中的规划 | Monte Carlo Tree Search = async Bellman backup / MCTS = 异步 Bellman 备份 |
| Offline RL (CQL, IQL) / 离线 RL | Conservative Q-iteration — DP with a penalty on OOD actions / 保守 Q 迭代——对 OOD 动作加惩罚的 DP |

每当有人说"最佳值函数",他们都指"DP固定点".`V*`或`Q*`在一张纸上,想象一下这个循环.

> 每次有人说"最优值函数",他们指的是"DP 不动点"――当你在论文中看到`V*`或`Q*`时,想象这个循环.

## 运送它.

保存如`outputs/skill-dp-solver.md`其他:

```markdown
---
name: dp-solver
description: Solve a small tabular MDP exactly via policy iteration or value iteration. Report convergence behavior.
version: 1.0.0
phase: 9
lesson: 2
tags: [rl, dynamic-programming, bellman]
---

Given an MDP with a known model, output:

1. Choice. Policy iteration vs value iteration. Reason tied to |S|, |A|, γ.
2. Initialization. V_0, starting policy. Convergence sensitivity.
3. Stopping. Sup-norm tolerance ε. Expected number of sweeps.
4. Verification. V*(s_0) computed exactly. Greedy policy extracted.
5. Use. How this baseline will be used to debug/evaluate sampling-based methods.

Refuse to run DP on state spaces > 10⁷. Refuse to claim convergence without a sup-norm check. Flag any γ ≥ 1 on an infinite-horizon task as a guarantee violation.
```

## 练习题

1. **Easy.**在 4×4 GridWorld 上运行值代`γ ∈ {0.9, 0.99}`几次扫描到`max |ΔV| < 1e-6`打印`V*`作为一个4×4格.
   > **练习1：**用不同的折扣因素,观察收费速度随着变化.
2. **Medium.**根据 * 静态* 格里德世界 (滑动概率) 的政策反复反复反复值`0.1`计数:扫描,墙钟时间,最后`V*(0,0)`它们在反复中更快地融合?
   > **练习2：**交换策略 代价 代价 代价 代价 代价 代价 代价 代价 代价 代价 代价 代价 代价 代价 代价 代价 代价 代价 代价 代价 代价 代价 代价 代价 代价 代价 代价 代价 代价 代价 代价 代价 代价 代价 代价 代价 代价 代价 代价 代价 代价 代价 代价 代价 代价 代价 代价 代价 代价 代价 代价 代价 代价 代价 代价 代价 代价 代价 代价 代价 代价 代价 代价 代价 代价 代价 代价 代价 代价 代价 代价 代价 代价 代价 代价 代价 代价 代价 代价 代价 代价 代价 代价 代价 代价 代价 代价 代价 代价 代价 代价 代价 代价 代价 代价 代价 代价 代价 代价 代价 代价 代价 代价 代价 代价 代价 代价 代价 代价 代价 代价 代价 代价 代价 代价 代价 代价 代价 代价 代价 代价 代价 代价 代价 代价 代价 代价 代价 代价 代价 代价 代价 代价 代价 代价 代价 代价 代价 代价 代价 代价 代价 代价 代价 代价 代价 代价 代价 代价 代价 代价 代价 代价 代价 代价 代价 代价 代价 代价 代价 代价 代价 代价 代价 代价 代价 代价 代价 
3. **Hard.**构建修改的政策代:在评估阶段,仅运行`k`它们的位置是的,而不是的.`V*(0,0)`错误与`k`为了`k ∈ {1, 2, 5, 10, 50}`评估/改进的交易比较是什么?
   > **练习3：**实现修改策略代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代

## 关键词 快速查找表

| Term | What people say | What it actually means |
|------|-----------------|-----------------------|
| Policy iteration | "DP algorithm" / 策略迭代 | Alternating evaluation (`V^π`) and improvement (greedy `π` w.r.t. `V^π`) until the policy stops changing. |
| Value iteration | "Faster DP" / 值迭代 | Bellman optimality backup applied in one sweep; converges to `V*` geometrically. |
| Bellman operator | "The recursion" / Bellman 算子 | `(T V)(s) = max_a Σ P (r + γ V(s'))`; a `γ`-contraction in sup-norm. |
| Contraction | "Why DP converges" / 压缩映射 | Any operator `T` with `\|\|T x - T y\|\| ≤ γ \|\|x - y\|\|` has a unique fixed point. |
| GPI | "Everything is DP" / 广义策略迭代 | Generalized Policy Iteration: any method driving `V` and `π` to mutual consistency. |
| Synchronous update | "Jacobi-style" / 同步更新 | Use old `V` throughout a sweep; cleanly analyzable but slower. |
| In-place update | "Gauss-Seidel-style" / 原地更新 | Use `V` as it's being updated; converges faster in practice. |

## 继续阅读 继续阅读

- [Sutton & Barto (2018). Ch. 4 — Dynamic Programming](http://incompleteideas.net/book/RLbook2020.pdf)政策代和价值代的常规表述.
- [Bertsekas (2019). Reinforcement Learning and Optimal Control](http://www.athenasc.com/rlbook.html)严格处理缩减绘图论点.
- [Puterman (2005). Markov Decision Processes](https://onlinelibrary.wiley.com/doi/book/10.1002/9780470316887)修改政策反复和其化分析.
- [Howard (1960). Dynamic Programming and Markov Processes](https://mitpress.mit.edu/9780262582300/dynamic-programming-and-markov-processes/)原始政策反复论文.
- [Bertsekas & Tsitsiklis (1996). Neuro-Dynamic Programming](http://www.athenasc.com/ndpbook.html)从DP到大约DP/深度RL的桥梁,每次课程都使用.
