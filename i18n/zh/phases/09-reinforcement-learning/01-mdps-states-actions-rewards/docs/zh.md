# 美国人民政府,国家,行动和奖励

> 马科夫决策过程是五件事:状态,行动,转型,奖励,折扣.RL  Q-学习,PPO,DPO,GRPO 中的一切都优化了这个形式.一遍学习,免费阅读其他强化学习.

> **【中文解读】**马尔科夫决策过程 (MDP) 包含五个要素:状态,动作,转移概率,奖励函数,折扣因子,

> **【拓展：MDP 是 AI 对齐的基础】**聊天GPT的RLHF训练本质上也是一个MDP:状态=对话上下文,动作=生成代币,奖励=人类偏好评分;;理解MDP是理解大模型对齐技术的起点;;

**Type:** Learn | **类型:** 学习
**Languages:** Python | **语言:** Python
**Prerequisites:** Phase 1 · 06 (Probability & Distributions), Phase 2 · 01 (ML Taxonomy) | **前置知识:** Phase 1 · 06 (概率与分布), Phase 2 · 01 (ML 分类)
**Time:** ~45 minutes | **时间:** ~45 分钟

## 问题 问题引入

你写着一个棋牌机器人,或者一个库存规划师,或者一个交易代理,或者一个训练推理模型的PPO循环.四个不同的领域,一个令人惊的事实:四个都崩到同一个数学对象.

> 你在写一个国际象棋机器人――或库存规划器――或交易代理――或训练推理模型的PPO循环――四个不同的领域,一个令人惊的事实:它们都归结为同一个数学对象――

监督学习给你`(x, y)`强化学习给你没有标签,只有一个流量的状态,你采取的行动,和一个 skalar 奖励. 这一举动赢得了比赛吗? 补充决定节省了钱吗? 贸易带来了利吗? 士刚刚生产的代币导致了更高的奖励吗?

> 监督学习给你`(x, y)`强化学习不给你标签,只有状态流,你采取的行动和标量奖励.

您不能从这个流中学习,直到您正式化. "我看到的", "我做了什么", "接下来发生了什么", "这么好" 每个都必须成为一个可以推理的对象.这种形式化是马科夫决策过程.这个阶段的每个RL算法,包括RLHF和GRPO循环在最后,优化了这个形状.

> 你无法从这个数据流中学习,直到你将其形式化. "我看到了什么", "我做了什么", "接下来发生了什么", "这是好事" 每个都必须成为可以推理的对象.

## 概念的核心概念

![Markov decision process: states, actions, transitions, rewards, discount](../assets/mdp.svg)

**The five objects.**现在,**五个核心要素。**

- **States** `S`在格里德世界,细胞,象棋,板块,在法学,文本窗口和任何记忆.
  **状态** `S`在网球世界中是格子,在国际象棋中是棋盘,在LLM中是上下文窗口加记忆.
- **Actions** `A`选择,向上/下/左/右,玩动,发行令牌.
  **动作** `A`△可选的操作──上/下/左/右移动──下一步棋──生成一个代币──
- **Transitions** `P(s' | s, a)`根据国家`s`行动`a`在棋牌中确定性,在库存中稳定性,在LLM解码中几乎确定性.
  **转移概率** `P(s' | s, a)`给定状态`s`和动作 `a`在国际象棋中是确定性,库存管理中是随机,LLM解码中是近似的确定性.
- **Rewards** `R(s, a, s')`收益减成本,日志概率比率在GRPO中.
  **奖励** `R(s, a, s')`△标量信号──赢=+1,输=−──收入减成本──GRPO 中的对数似然比项──
- **Discount** `γ ∈ [0, 1)`未来的奖励与现在的奖励有多少?`γ = 0.99`购买一个水平的 ~ 100 步; `γ = 0.9`买了10个.
  **折扣因子** `γ ∈ [0, 1)`△未来奖励与当前奖励权重相比.`γ = 0.99`应对100步的有效视野;`γ = 0.9`应对10步.

**The Markov property** `P(s_{t+1} | s_t, a_t) = P(s_{t+1} | s_0, a_0, …, s_t, a_t)`如果没有,国家代表性是不完整的,不是方法的失败,是国家的失败.

> **马尔可夫性质**未来只取决于当前状态. 如果不存在,说明状态表示不完整,不是方法的失败,而是状态的失败.

**Policies and returns.**一个政策`π(a | s)`图表状态到行动分布. 返回`G_t = r_t + γ r_{t+1} + γ² r_{t+2} + …`价值: 未来奖励的折扣金额.`V^π(s) = E[G_t | s_t = s]`是从 开始的预期回报`s`政策`π`值`Q^π(s, a) = E[G_t | s_t = s, a_t = a]`每个RL算法估计其中一个,然后改进`π`根据此.

> **策略与回报。**策略`π(a|s)`将状态映射到动作分布.`G_t`是未来奖励的折扣和――值函数`V^π(s)`是从状态`s`出发的期望回报──Q 值 `Q^π(s,a)`根据这些两个量,每个RL算法都在估计其中一个,然后根据此改进策略.

**The Bellman equations.**在这个阶段使用的固定点方程:

`V^π(s) = Σ_a π(a|s) Σ_{s', r} P(s', r | s, a) [r + γ V^π(s')]`

> **【中文解读】**贝尔曼方程是RL的核心推进关系:当前状态的价值 = 即时奖励 + 折扣后的下一状态价值――它是动态规划的共同基础――Q-学习、TD学习――在LLM的RLHF训练中,这应对"当前代币的贡献 = 人类偏好分数 + 未来代币的预期贡献"――

> **【拓展：从 MDP 到 POMDP】**现实中很多问题不满足马尔可夫性 (现状不能完全决定未来),需要使用POMDP (部分可观察MDP) 建模――对话系统就是POMDP模型只能看到上下文窗口内的内容,而不是完整的用户意图――LLM的长上下文能力本质上是缓解POMDP的信息不完整问题――
`Q^π(s, a) = Σ_{s', r} P(s', r | s, a) [r + γ Σ_{a'} π(a'|s') Q^π(s', a')]`

这些预期的分化返回为"这个步骤的奖励"加上"你降落的地方的折扣值".反复性. 9 阶段的每个算法要么重复这个方程到融合 (动态编程),从它 (蒙特卡洛) 样本,或者将它启动一步 (时间差异).

> 这些方程将希望回报被分解为"当前步骤的奖励"加上"到达状态折扣值"――递归的――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――

## 建立它,实现它.
```figure
discount-horizon
```

## 建立它

### 步骤1:一个小的确定性MDP

代理从左上开始,终端在右下,每步的奖励为 -1 个,行动`{up, down, left, right}`看到`code/main.py`现在,我们要去.

> 一个4×4的网格世界――智能体从左上角出发,终止状态在右下角,每步奖励 -1,动作 `{上, 下, 左, 右}`,我知道.

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

五条线,就是整个环境,确定性过渡,恒定的步骤惩罚,吸收终端状态.

> 五行代码――这就是整个环境――确定性转移――恒定步惩罚――吸收终止状态――

### 步骤2:制定政策

政策是从状态到行动分布的函数.

> 策略是从状态到动作分布的函数.

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

运行随机策略1000次.这个4×4板的平均回报率为 -60至 -80左右.最佳回报率是 -6 (直线路向右).关闭这一差距是9阶段的一切.

> 运行随机策略 1000 次――这个4×4棋盘的平均回报约为 -60~ -80――最优回报是 -6――直线路径向右下) ─缩小这个差距就是9期的全部目标――

### 步骤3:计算`V^π`通过贝尔曼方程

对于小 MDP 来说,贝尔曼方程是一个线性系统. 列出状态,应用预期,再重复直到值停止变化.

> 对于小型MDP,贝尔曼方程是一个线性系统.

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

这是一个反复的政策评估.这是萨顿和巴托的第一个算法,也是每种RL方法的理论基础.

> 这是Sutton & Barto教科书中的第一个算法,也是所有后续RL方法的理论基础.

### 步骤4:`γ`是一个具有物理意义的超参数

实际水平大概是`1 / (1 - γ)`现在,我们要去.`γ = 0.9`十个步骤.`γ = 0.99`百步.`γ = 0.999`千个步骤.

> 有效的视野约为`1 / (1 - γ)`,我知道.`γ = 0.9`应对10步.`γ = 0.99`应对100步.`γ = 0.999`应对1000步.

由于许多早期步骤都承担了远期奖励的责任,因此信用分配变得很杂.`γ = 1`控制任务使用`0.95–0.99`长视野战略游戏使用`0.999`现在,我们要去.

> 折扣因子太低,智能体会目光短浅――太高,信用分配会变得杂,因为许多早期步骤共同承担长期奖励责任――LLM RLHF通常使用`γ = 1`由于回合短且有界限.`0.95-0.99`长视野策略游戏使用 `0.999`,我知道.

## 陷

- **Non-Markovian state.**如果您需要最后三个观察来决定,"状态"不仅仅是当前的观察. 修复:堆框架 (DQN在Atari堆 4) 或使用复制状态 (LSTM/GRU在观测上).
  **非马尔可夫状态。**如果您需要最近三个观测才能做出决策,"状态"就不仅仅是当前观测――修复方法:堆叠(Atari 上的DQN 堆叠 4 ) 或使用循环状态(LSTM/GRU) ⋅
- **Sparse rewards.**只有获奖奖使在大型状态空间中学习几乎不可能.
  **稀疏奖励。**仅获胜的奖励使在大状态空间中学习几乎不可能.
- **Reward hacking.**优化代理奖励通常会产生病态行为.OpenAI的船只比赛代理在圈子里旋转,以收集力量而不是永远完成比赛.总是根据目标结果定义奖励,而不是代理.
  **奖励黑客。**优化代理奖励常产生病态行为――OpenAI的赛船代理原地转圈收集道具,永远不完成比赛――始终从目标结果定义奖励,而不是代理――
- **Discount mis-spec.** `γ = 1`在一个无限视野任务上,每个值都是无限的.`γ < 1`现在,我们要去.
  **折扣因子设定错误。**无限视野任务上`γ = 1`会使所有价值为无穷――始终用有限视野或`γ < 1`现在我们要去.
- **Reward scale.**奖励 {+100, -100} vs {+1, -1} 给出相同的最佳政策,但截然不同的梯度大小.`[-1, 1]`- 在连接到PPO/DQN之前.
  **奖励尺度。**奖励与 {+1, -1} 给予相同的优势策略,但梯度量级差异巨大.`[-1, 1]`左右的.

## 用它实现框架

2026堆将每一个RL管道降低到MDP,然后触摸代码:

> 在2026年技术在写代码之前,将每个RL流水线归结为一个MDP:

| Situation | State | Action | Reward | γ |
|-----------|-------|--------|--------|---|
| Situation / 场景 | State / 状态 | Action / 动作 | Reward / 奖励 | γ |
| Control (locomotion, manipulation) / 控制（运动、操作） | Joint angles + velocities / 关节角度+速度 | Continuous torques / 连续力矩 | Task-specific shaped / 任务特定塑形 | 0.99 |
| Games (chess, Go, poker) / 游戏（象棋、围棋、扑克） | Board + history / 棋盘+历史 | Legal move / 合法走法 | Win=+1 / loss=-1 / 胜=+1/负=-1 | 1.0 (finite) |
| Inventory / pricing / 库存/定价 | Stock + demand / 库存+需求 | Order qty / 订购量 | Revenue - cost / 收入-成本 | 0.95 |
| RLHF for LLMs / LLM 的 RLHF | Context tokens / 上下文 token | Next token / 下一个 token | Reward-model score at end / 末尾奖励模型分数 | 1.0 (episode ~200 tokens) |
| GRPO for reasoning / 推理的 GRPO | Prompt + partial response / 提示+部分回复 | Next token / 下一个 token | Verifier 0/1 at end / 末尾验证器 0/1 | 1.0 |

在写任何训练循环之前,写出五个.大多数"RL不工作"错误报告追溯到纸上被打破的MDP公式.

> 在写任何训练循环之前先写好五元组. 大多数"RL不工作"的错误报告都可以追溯到纸面上的MDP定义就有问题.

## 运送它.

保存如`outputs/skill-mdp-modeler.md`其他:

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

## 练习题

1. **Easy.**实现4×4格式世界和随机政策推广`code/main.py`运行1万集,报告回报的平均值和STD.
   > **练习1（简单）：**实现4×4 GridWorld 和随机策略推广――运行 10,000 回合――报告回报的平均值和标准差,与最优回报 (-6) 比较――
2. **Medium.**跑步`policy_evaluation`随着`γ ∈ {0.5, 0.9, 0.99}`对于统一随机政策.`V`解释为什么终端附近的状态值越来越快`γ`现在,我们要去.
   > **练习2（中等）：**用`γ ∈ {0.5, 0.9, 0.99}`运行策略评估――打印每 γ 的 4×4 值网格――解释为什么接近终止状态的状态值在更大的 γ 下增长更快――
3. **Hard.**转换格里德世界到静止状态:每个动作都会与概率相邻方向滑动`p = 0.1`重新评估制服政策.`V[start]`变得更好还是更糟?
   > **练习3（困难）：**将GridWorld 变为随机的:每动作以概率`p = 0.1`滑向相邻方向――重新评估均策略――`V[start]`变好还是变差?为什么?

## 关键词 快速查找表

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

## 继续阅读 继续阅读

- [Sutton & Barto (2018). Reinforcement Learning: An Introduction, 2nd ed.](http://incompleteideas.net/book/RLbook2020.pdf)课本.第3章涵盖MDP和贝尔曼方程;第1章激励了每次课程的奖励假设.
- [Bellman (1957). Dynamic Programming](https://press.princeton.edu/books/paperback/9780691146683/dynamic-programming)贝尔曼方程的起源.
- [OpenAI Spinning Up — Part 1: Key Concepts](https://spinningup.openai.com/en/latest/spinningup/rl_intro.html)从深度RL角度来看简洁的MDP.
- [Puterman (2005). Markov Decision Processes](https://onlinelibrary.wiley.com/doi/book/10.1002/9780470316887)关于MDP和精确解决方法的操作研究参考.
- [Littman (1996). Algorithms for Sequential Decision Making (PhD thesis)](https://www.cs.rutgers.edu/~mlittman/papers/thesis-main.pdf)作为动态编程专业化的MDP最清洁的衍生.
