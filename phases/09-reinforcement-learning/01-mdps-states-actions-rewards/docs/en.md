# MDPs, States, Actions & Rewards | MDP — 状态、动作与奖励

> A Markov Decision Process is five things: states, actions, transitions, rewards, a discount. Everything in RL — Q-learning, PPO, DPO, GRPO — optimizes over this shape. Learn it once, read the rest of reinforcement learning for free.

> **【中文解读】** 马尔可夫决策过程（MDP）包含五个要素：状态、动作、转移概率、奖励函数、折扣因子。RL 中的一切——Q-learning、PPO、DPO、GRPO——都在这个框架上优化。学一次，免费读懂整个强化学习。

> **【拓展：MDP 是 AI 对齐的基础】** ChatGPT 的 RLHF 训练本质上也是一个 MDP：状态=对话上下文，动作=生成的 token，奖励=人类偏好评分。理解 MDP 是理解大模型对齐技术的起点。

**Type:** Learn
**Languages:** Python
**Prerequisites:** Phase 1 · 06 (Probability & Distributions), Phase 2 · 01 (ML Taxonomy)
**Time:** ~45 minutes

## The Problem | 问题引入

You are writing a chess bot. Or an inventory planner. Or a trading agent. Or the PPO loop that trains a reasoning model. Four different domains, one surprising fact: all four collapse to the same mathematical object.

> 你在写一个国际象棋机器人。或者库存规划器。或者交易代理。或者训练推理模型的 PPO 循环。四个不同的领域，一个令人惊讶的事实：它们都可以归结为同一个数学对象。

Supervised learning gives you `(x, y)` pairs and asks you to fit a function. Reinforcement learning gives you no labels — only a stream of states, the actions you took, and a scalar reward. Did the move win the game? Did the restock decision save money? Did the trade make a profit? Did the token the LLM just produced lead to a higher reward from the judge?

> 监督学习给你 `(x, y)` 对，让你拟合一个函数。强化学习不给你标签——只有状态流、你采取的动作和一个标量奖励。那步棋赢了吗？补货决策省钱了吗？交易赚钱了吗？LLM 刚刚生成的 token 是否从评判者那里得到了更高的奖励？

You cannot learn from this stream until you formalize it. "What I saw," "what I did," "what happened next," "how good that was" — each has to become an object you can reason about. That formalization is a Markov Decision Process. Every RL algorithm in this phase, including the RLHF and GRPO loops at the end, optimizes over this shape.

> 你无法从这个数据流中学习，直到你将其形式化。"我看到了什么"、"我做了什么"、"接下来发生了什么"、"这有多好"——每一个都必须成为你可以推理的对象。这个形式化就是马尔可夫决策过程。本阶段中的每一个 RL 算法，包括最后的 RLHF 和 GRPO 循环，都在这个结构上进行优化。

## The Concept | 核心概念

![Markov decision process: states, actions, transitions, rewards, discount](../assets/mdp.svg)

**The five objects.** / **五个核心要素。**

- **States** `S`. Everything the agent needs to decide. In GridWorld, the cell. In chess, the board. In an LLM, the context window plus any memory.
  **状态** `S`。智能体决策所需的所有信息。在 GridWorld 中是格子，在国际象棋中是棋盘，在 LLM 中是上下文窗口加记忆。
- **Actions** `A`. The choices. Move up/down/left/right. Play a move. Emit a token.
  **动作** `A`。可选的操作。上/下/左/右移动。下一步棋。生成一个 token。
- **Transitions** `P(s' | s, a)`. Given state `s` and action `a`, the distribution over next state. Deterministic in chess, stochastic in inventory, almost-deterministic in LLM decoding.
  **转移概率** `P(s' | s, a)`。给定状态 `s` 和动作 `a`，下一个状态的分布。国际象棋中是确定性的，库存管理中是随机的，LLM 解码中近似确定性。
- **Rewards** `R(s, a, s')`. The scalar signal. Win = +1, loss = -1. Revenue minus cost. The log-likelihood ratio term in GRPO.
  **奖励** `R(s, a, s')`。标量信号。赢=+1，输=-1。收入减成本。GRPO 中的对数似然比项。
- **Discount** `γ ∈ [0, 1)`. How much future reward counts vs present. `γ = 0.99` buys a horizon of ~100 steps; `γ = 0.9` buys ~10.
  **折扣因子** `γ ∈ [0, 1)`。未来奖励相对于当前奖励的权重。`γ = 0.99` 对应约 100 步的有效视野；`γ = 0.9` 对应约 10 步。

**The Markov property** `P(s_{t+1} | s_t, a_t) = P(s_{t+1} | s_0, a_0, …, s_t, a_t)`. The future depends only on the present state. If it does not, the state representation is incomplete — not a failure of the method, a failure of the state.

> **马尔可夫性质**：未来只取决于当前状态。如果不成立，说明状态表示不完整——不是方法的失败，而是状态的失败。

**Policies and returns.** A policy `π(a | s)` maps states to action distributions. The return `G_t = r_t + γ r_{t+1} + γ² r_{t+2} + …` is the discounted sum of future rewards. The value `V^π(s) = E[G_t | s_t = s]` is the expected return starting from `s` under policy `π`. The Q-value `Q^π(s, a) = E[G_t | s_t = s, a_t = a]` is the expected return starting with a specific action. Every RL algorithm estimates one of these two, then improves `π` accordingly.

> **策略与回报。** 策略 `π(a|s)` 将状态映射到动作分布。回报 `G_t` 是未来奖励的折扣和。值函数 `V^π(s)` 是从状态 `s` 出发的期望回报。Q 值 `Q^π(s,a)` 是从特定动作出发的期望回报。每个 RL 算法都在估计这两个量之一，然后据此改进策略。

**The Bellman equations.** The fixed-point equations that everything in this phase uses:

`V^π(s) = Σ_a π(a|s) Σ_{s', r} P(s', r | s, a) [r + γ V^π(s')]`

> **【中文解读】** Bellman 方程是 RL 的核心递推关系：当前状态的价值 = 即时奖励 + 折扣后的下一状态价值。它是动态规划、Q-learning、TD 学习的共同基础。在 LLM 的 RLHF 训练中，这对应于"当前 token 的贡献 = 人类偏好分数 + 未来 token 的期望贡献"。

> **【拓展：从 MDP 到 POMDP】** 现实中很多问题不满足马尔可夫性（当前状态不能完全决定未来），需要用 POMDP（部分可观察 MDP）建模。对话系统就是 POMDP——模型只能看到上下文窗口内的内容，而非完整的用户意图。LLM 的长上下文能力本质上是在缓解 POMDP 的信息不完整问题。
`Q^π(s, a) = Σ_{s', r} P(s', r | s, a) [r + γ Σ_{a'} π(a'|s') Q^π(s', a')]`

These split expected return into "this step's reward" plus "discounted value of where you land." Recursive. Every algorithm in Phase 9 either iterates this equation to convergence (dynamic programming), samples from it (Monte Carlo), or bootstraps it one step (temporal difference).

> 这些方程将期望回报分解为"当前步的奖励"加上"到达状态的折扣值"。递归的。Phase 9 中的每个算法要么迭代这个方程到收敛（动态规划），要么从中采样（蒙特卡洛），要么自举一步（时序差分）。

## Build It | 动手实现

### Step 1: a tiny deterministic MDP

A 4×4 GridWorld. Agent starts top-left, terminal at bottom-right, reward of -1 per step, actions `{up, down, left, right}`. See `code/main.py`.

> 一个 4×4 的网格世界。智能体从左上角出发，终止状态在右下角，每步奖励 -1，动作为 `{上, 下, 左, 右}`。

```python
GRID = 4
TERMINAL = (3, 3)
ACTIONS = {"up": (-1, 0), "down": (1, 0), "left": (0, -1), "right": (0, 1)}

def step(state, action):
    if state == TERMINAL:
        return state, 0.0, True
    dr, dc = ACTIONS[action]
    r, c = state
    nr = min(max(r + dr, 0), GRID - 1)
    nc = min(max(c + dc, 0), GRID - 1)
    return (nr, nc), -1.0, (nr, nc) == TERMINAL
```

Five lines. That is the entire environment. Deterministic transitions, constant step penalty, absorbing terminal state.

> 五行代码。这就是整个环境。确定性转移、恒定步惩罚、吸收终止状态。

### Step 2: roll out a policy

A policy is a function from state to action distribution. The simplest: uniform random.

> 策略是从状态到动作分布的函数。最简单的：均匀随机。

```python
def uniform_policy(state):
    return {a: 0.25 for a in ACTIONS}

def rollout(policy, max_steps=200):
    s, total, steps = (0, 0), 0.0, 0
    for _ in range(max_steps):
        a = sample(policy(s))
        s, r, done = step(s, a)
        total += r
        steps += 1
        if done:
            break
    return total, steps
```

Run the random policy 1000 times. Average return is around -60 to -80 for this 4×4 board. The optimal return is -6 (straight-line path down-right). Closing that gap is everything in Phase 9.

> 运行随机策略 1000 次。这个 4×4 棋盘的平均回报约为 -60 到 -80。最优回报是 -6（直线路径向右下方）。缩小这个差距就是 Phase 9 的全部目标。

### Step 3: compute `V^π` exactly via the Bellman equation

For small MDPs the Bellman equation is a linear system. Enumerate states, apply the expectation, iterate until the values stop changing.

> 对于小型 MDP，Bellman 方程是一个线性系统。枚举状态，应用期望，迭代直到值不再变化。

```python
def policy_evaluation(policy, gamma=0.99, tol=1e-6):
    V = {s: 0.0 for s in all_states()}
    while True:
        delta = 0.0
        for s in all_states():
            if s == TERMINAL:
                continue
            v = 0.0
            for a, pi_a in policy(s).items():
                s_next, r, _ = step(s, a)
                v += pi_a * (r + gamma * V[s_next])
            delta = max(delta, abs(v - V[s]))
            V[s] = v
        if delta < tol:
            return V
```

This is iterative policy evaluation. It is the first algorithm in Sutton & Barto and the theoretical foundation of every RL method that follows.

> 这是迭代策略评估。它是 Sutton & Barto 教科书中的第一个算法，也是后续所有 RL 方法的理论基础。

### Step 4: `γ` is a hyperparameter with physical meaning

Effective horizon is roughly `1 / (1 - γ)`. `γ = 0.9` → 10 steps. `γ = 0.99` → 100 steps. `γ = 0.999` → 1000 steps.

> 有效视野约为 `1 / (1 - γ)`。`γ = 0.9` 对应 10 步。`γ = 0.99` 对应 100 步。`γ = 0.999` 对应 1000 步。

Too low and the agent acts myopically. Too high and credit assignment becomes noisy, because many early steps share responsibility for far-future reward. LLM RLHF typically uses `γ = 1` because episodes are short and bounded. Control tasks use `0.95–0.99`. Long-horizon strategy games use `0.999`.

> 折扣因子太低，智能体会目光短浅。太高，信用分配会变得嘈杂，因为许多早期步骤共同承担远期奖励的责任。LLM RLHF 通常使用 `γ = 1`，因为回合短且有界。控制任务使用 `0.95-0.99`。长视野策略游戏使用 `0.999`。

## Pitfalls

- **Non-Markovian state.** If you need the last three observations to decide, the "state" is not just the current observation. Fix: stack frames (DQN on Atari stacks 4) or use a recurrent state (LSTM/GRU over observations).
  **非马尔可夫状态。** 如果你需要最近三个观测才能决策，"状态"就不仅仅是当前观测。修复方法：堆叠帧（Atari 上的 DQN 堆叠 4 帧）或使用循环状态（LSTM/GRU）。
- **Sparse rewards.** Win-only rewards make learning nearly impossible in large state spaces. Shape rewards (intermediate signal) or bootstrap with imitation (Phase 9 · 09).
  **稀疏奖励。** 仅获胜的奖励使大状态空间中的学习几乎不可能。塑形奖励（中间信号）或用模仿学习引导。
- **Reward hacking.** Optimizing a proxy reward often produces pathological behavior. OpenAI's boat-racing agent spun in circles collecting powerups forever instead of finishing the race. Always define reward from the target outcome, not the proxy.
  **奖励黑客。** 优化代理奖励常产生病态行为。OpenAI 的赛船代理原地转圈收集道具，永远不完成比赛。始终从目标结果定义奖励，而非代理。
- **Discount mis-spec.** `γ = 1` on an infinite-horizon task makes every value infinite. Always cap with either a finite horizon or `γ < 1`.
  **折扣因子设定错误。** 无限视野任务上 `γ = 1` 会使所有值为无穷。始终用有限视野或 `γ < 1` 来约束。
- **Reward scale.** Rewards of {+100, -100} vs {+1, -1} give identical optimal policies but vastly different gradient magnitudes. Normalize to `[-1, 1]`-ish before plugging into PPO/DQN.
  **奖励尺度。** {+100, -100} 与 {+1, -1} 的奖励给出相同的最优策略，但梯度量级差异巨大。在输入 PPO/DQN 前归一化到 `[-1, 1]` 左右。

## Use It | 用框架实现

The 2026 stack reduces every RL pipeline to an MDP before touching code:

> 2026 年的技术栈在写代码之前，会将每个 RL 流水线归结为一个 MDP：

| Situation | State | Action | Reward | γ |
|-----------|-------|--------|--------|---|
| Situation / 场景 | State / 状态 | Action / 动作 | Reward / 奖励 | γ |
| Control (locomotion, manipulation) / 控制（运动、操作） | Joint angles + velocities / 关节角度+速度 | Continuous torques / 连续力矩 | Task-specific shaped / 任务特定塑形 | 0.99 |
| Games (chess, Go, poker) / 游戏（象棋、围棋、扑克） | Board + history / 棋盘+历史 | Legal move / 合法走法 | Win=+1 / loss=-1 / 胜=+1/负=-1 | 1.0 (finite) |
| Inventory / pricing / 库存/定价 | Stock + demand / 库存+需求 | Order qty / 订购量 | Revenue - cost / 收入-成本 | 0.95 |
| RLHF for LLMs / LLM 的 RLHF | Context tokens / 上下文 token | Next token / 下一个 token | Reward-model score at end / 末尾奖励模型分数 | 1.0 (episode ~200 tokens) |
| GRPO for reasoning / 推理的 GRPO | Prompt + partial response / 提示+部分回复 | Next token / 下一个 token | Verifier 0/1 at end / 末尾验证器 0/1 | 1.0 |

Write the five tuples before writing any training loop. Most "RL does not work" bug reports trace back to an MDP formulation that was broken on paper.

> 在写任何训练循环之前先写好五元组。大多数"RL 不工作"的 bug 报告都能追溯到纸面上 MDP 定义就有问题。

## Ship It | 产出物

Save as `outputs/skill-mdp-modeler.md`:

```markdown
---
name: mdp-modeler
description: Given a task description, produce a Markov Decision Process spec and flag formulation risks before training.
version: 1.0.0
phase: 9
lesson: 1
tags: [rl, mdp, modeling]
---

Given a task (control / game / recommendation / LLM fine-tuning), output:

1. State. Exact feature vector or tensor spec. Justify Markov property.
2. Action. Discrete set or continuous range. Dimensionality.
3. Transition. Deterministic, stochastic-with-known-model, or sample-only.
4. Reward. Function and source. Sparse vs shaped. Terminal vs per-step.
5. Discount. Value and horizon justification.

Refuse to ship any MDP where the state is non-Markovian without explicit mention of frame-stacking or recurrent state. Refuse any reward that was not defined in terms of the target outcome. Flag any `γ ≥ 1.0` on an infinite-horizon task. Flag any reward range >100x the typical step reward as a likely gradient-explosion source.
```

## Exercises | 练习题

1. **Easy.** Implement the 4×4 GridWorld and random-policy rollout in `code/main.py`. Run 10,000 episodes. Report mean and std of return. Compare to the optimal return (-6).
   > **练习1（简单）：** 实现 4×4 GridWorld 和随机策略 rollout。运行 10,000 回合。报告回报的均值和标准差，与最优回报 (-6) 比较。
2. **Medium.** Run `policy_evaluation` with `γ ∈ {0.5, 0.9, 0.99}` for the uniform-random policy. Print `V` as a 4×4 grid for each. Explain why the state values near the terminal grow faster with larger `γ`.
   > **练习2（中等）：** 用 `γ ∈ {0.5, 0.9, 0.99}` 运行策略评估。打印每个 γ 的 4×4 值网格。解释为什么靠近终止状态的状态值在更大的 γ 下增长更快。
3. **Hard.** Turn the GridWorld stochastic: each action slips to an adjacent direction with probability `p = 0.1`. Re-evaluate the uniform policy. Does `V[start]` get better or worse? Why?
   > **练习3（困难）：** 将 GridWorld 改为随机的：每个动作以概率 `p = 0.1` 滑向相邻方向。重新评估均匀策略。`V[start]` 变好还是变差？为什么？

## Key Terms | 术语速查表

| Term | What people say | What it actually means |
|------|-----------------|-----------------------|
| Term / 术语 | What people say / 通俗说法 | What it actually means / 实际含义 |
| MDP | "Reinforcement learning setup" | Tuple `(S, A, P, R, γ)` satisfying the Markov property. |
| State / 状态 | "What the agent sees" / "智能体看到什么" | Sufficient statistic for future dynamics under the chosen policy class. |
| Policy / 策略 | "Agent's behavior" / "智能体的行为" | Conditional distribution `π(a \| s)` or deterministic map `s → a`. |
| Return / 回报 | "Total reward" / "总奖励" | Discounted sum `Σ γ^t r_t` from the current step. |
| Value / 值函数 | "How good a state is" / "状态有多好" | Expected return under `π` starting from `s`. |
| Q-value / Q值 | "How good an action is" / "动作有多好" | Expected return under `π` starting from `s` with first action `a`. |
| Bellman equation / Bellman方程 | "Dynamic programming recursion" / "动态规划递推" | Fixed-point decomposition of value / Q into one-step reward plus discounted successor value. |
| Discount `γ` / 折扣因子 | "Future vs present" / "未来vs当前" | Geometric weight on far-future reward; effective horizon `~1/(1-γ)`. |

## Further Reading | 延伸阅读

- [Sutton & Barto (2018). Reinforcement Learning: An Introduction, 2nd ed.](http://incompleteideas.net/book/RLbook2020.pdf) — the textbook. Ch. 3 covers MDPs and Bellman equations; Ch. 1 motivates the reward hypothesis that underlies every subsequent lesson.
- [Bellman (1957). Dynamic Programming](https://press.princeton.edu/books/paperback/9780691146683/dynamic-programming) — the origin of the Bellman equation.
- [OpenAI Spinning Up — Part 1: Key Concepts](https://spinningup.openai.com/en/latest/spinningup/rl_intro.html) — concise MDP primer from a deep-RL angle.
- [Puterman (2005). Markov Decision Processes](https://onlinelibrary.wiley.com/doi/book/10.1002/9780470316887) — the operations-research reference on MDPs and exact solution methods.
- [Littman (1996). Algorithms for Sequential Decision Making (PhD thesis)](https://www.cs.rutgers.edu/~mlittman/papers/thesis-main.pdf) — the cleanest derivation of MDPs as a dynamic-programming specialization.
