# 蒙特卡洛方法 从完整的集中学习

> 动态编程需要一个模型.蒙特卡罗只需要一段时间. 运行政策,观察收益,平均它们. 在RL 中最简单的想法,并解锁下游的想法.

> **【中文解读】**动态规划需要已知环境模型,蒙特卡洛只需要完整的回合数据:执行策略,观测回报,取平均.

**Type:** Build | **类型:** 动手
**Languages:** Python | **语言:** Python
**Prerequisites:** Phase 9 · 01 (MDPs), Phase 9 · 02 (Dynamic Programming) | **前置知识:** Phase 9 · 01 (MDP), Phase 9 · 02 (动态规划)
**Time:** ~75 minutes | **时间:** ~75 分钟

## 问题 问题引入

动态编程是优雅的,但它假设你可以查询`P(s' | s, a)`实际上,几乎没有什么都能这样做. 机器人不能分析地计算相机像素的分布,在合并扭矩之后. 定价算法不能整合每一个可能的客户反应.

> 动态规划很优秀,但假设你可以查询每个状态和动作.`P(s' | s, a)`△现实中几乎没有什么是这样的工作.机器无法计算关节力矩后机像素的分布. 定价算法无法对待所有可能的客户反应积分.

需要一种方法,只需要从环境中*样本*的能力.`s_0, a_0, r_1, s_1, a_1, r_2, …, s_T`运用它来估计价值.这是蒙特卡罗.

> 你需要一种从环境中采用的方法.`s_0, a_0, r_1, s_1, a_1, r_2, …, s_T`,用它来估计价值.

从DP到MC的转变是哲学上重要的:我们从*已知模型+精确备份*转移到*样本推出+平均回报*.差异跳跃,但可用性爆炸.此课后的每一个RL算法T,Q-学习,REINFORCE,PPO,GRPO都是蒙特卡罗估计器,有时在上面有层次的启动.

> 从DP到MC的转变在哲学上很重要:我们从*已知模型+精确备份*转向*采样推广+平均回报*──差增加,但适用范围爆炸式增长──本课后的每个RL算法TD、Q-学习、REINFORCE、PPO、GRPO本质上都是蒙特卡洛估计器,有时都叠加了自己──

> **【中文解读】**从DP到MC的核心转变:从"已知模型+精确计算"到"采样轨迹+平均回报"――差距增加了,但适用范围爆炸式扩大了──PPO、RLHF本质上都是MC估计器的变化──

> **【拓展：LLM中的MC】**在ChatGPT的RLHF训练中,对每个提示采集多个答案,计算平均奖励. 这就是MC思想在大模型训练中直接应用.

## 概念的核心概念

![Monte Carlo: rollout, compute returns, average; first-visit vs every-visit](../assets/monte-carlo.svg)

**The core idea, in one line:** `V^π(s) = E_π[G_t | s_t = s] ≈ (1/N) Σ_i G^{(i)}(s)`在哪里`G^{(i)}(s)`访问后的回报`s`政策`π`现在,我们要去.

> **核心思想，一行概括：** `V^π(s) = E_π[G_t | s_t = s] ≈ (1/N) Σ_i G^{(i)}(s)`在其中`G^{(i)}(s)`是在策略中`π`下访问 `s`时观测到的回报.

> **【中文解读】**评价核心:状态值 = 经过该状态的多次观测到的回报的平均值.`V_new = V_old + α(target - V_old)`是从MC到TD到所有现代RL算法的桥梁.

**First-visit vs every-visit MC.**考虑到一个访问国家事件`s`首先,每次访问的MC只会计算出第一次访问的回报;每次访问的MC只会计算所有访问.这两次访问在限制中都是无偏见的.第一次访问更容易分析 (iid样本).每次访问每集使用更多数据,通常在实践中更快地融合.

> **首次访问 vs 每次访问 MC。**给定一个多次访问状态`s`回合,第一次访问 MC 仅计算第一次访问的回报;每次访问 MC 计算所有访问――两者在极限下都是无偏见的――第一次访问更容易分析――独立和分布样本)――每次访问每回合使用更多数据,实践中通常收获更快――

**Incremental mean.**更新运行平均值:

`V_n(s) = V_{n-1}(s) + (1/n) [G_n - V_{n-1}(s)]`

重新组织:`V_new = V_old + α · (target - V_old)`随着`α = 1/n`换个`1/n`对于一个恒定的步骤尺寸`α ∈ (0, 1)`并且你得到一个非静止的MC估计器,`π`这一举动是从MC到TD到每一个现代的RL算法的全部跳跃.

> **增量均值。**没有存储所有回报,而是更新运行平均值.`1/n`替换为常数步长`α ∈ (0, 1)`得到一个追踪.`π`变化不平稳的MC估计器. 这一步就是从MC到TD到所有现代RL算法的整个跳跃.

**Exploration is now a problem.**根据统计,DP 通过统计查询接触到每个州.`π`总是说,在一个特定的位置上,整个区域的状态空间从来没有得到样本,

> **探索现在成了问题。**通过枚举触及每个状态.`π`总体而言,整个状态空间区域永远不会被采样,其值估计永远为零.

> **【中文解读】**探索问题:DP 能遍历所有状态,MC 只能看到策略访问过的状态――如果策略是确定性的,大量状态永远不会被访问――三种解决方案:探索起点 (不实用) ̇ε-贪心 (最常用的) ̇离策略MC通过重要性采样从行为策略学习目标策略) ̇

1. **Exploring starts.**开始每一集从一个随机对 (s, a). 保障覆盖; 实际上不现实 (你不能"重置"机器人到任意状态).
   **探索起点。**每回合从随机 (s,a) 对开始――保证覆盖;实际中不现实――你不能把机器人"重置"到任意状态)
2. **ε-greedy.**现在,我会做什么?`ε`随机行动,所有状态行动对均被抽样.
   **ε-贪心。**对于当前的Q 贪心行动,但概率`ε`随机选动作. 所有状态动作都被逐渐采用.
3. **Off-policy MC.**根据行为政策收集数据`μ`了解目标政策`π`通过重点样本采集. 差异很高,但它是重播缓冲方法的桥梁,比如DQN.
   **离策略 MC。**在行为策略中`μ`下收集数据,通过学习目标策略的重要性`π`△高方差,但它是通往DQN等回放缓冲方法的桥梁.

**Monte Carlo Control.**评估 →改善 →评估,就像政策代一样,但评估是基于样本:

1. 跑步`π`让我们看一段话.
2. 更新`Q(s, a)`根据观察到的回报.
3. 造`π`贪的子.`Q`现在,我们要去.
4. 复制.

向`Q*`其他`π*`在温和条件下,每对都会无限频繁访问,`α`为了满足罗宾斯-蒙罗的需求.

> **蒙特卡洛控制。**评估 → 改进 → 评估,就像策略代,但评估基于采样.`α`满足罗宾斯-蒙罗),以概率1 收到`Q*`和 `π*`,我知道.

## 建立它,实现它.
```figure
epsilon-greedy
```

## 建立它

### 步骤1:推出 →列表 (s, a, r)

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

没有模型,只有`env.reset()`其他`env.step(s, a)`接口与健身房环境相同,但被剥离.

> 不需要模型,只需要`env.reset()`和 `env.step(s, a)`与健身房的环境接口相同,但更简单.

### 步骤2:计算返回 (反扫)

```python
def returns_from(trajectory, gamma):
    returns = []
    G = 0.0
    for _, _, r in reversed(trajectory):
        G = r + gamma * G
        returns.append(G)
    return list(reversed(returns))
```

一个通行,`O(T)`逆转复发`G_t = r_{t+1} + γ G_{t+1}`避免再总结.

> 一次经历,`O(T)`△反向递送`G_t = r_{t+1} + γ G_{t+1}`避免了重复求和――

### 步骤3:第一次访问的MC评估

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

工作的三个行:标记状态,如第一次访问,增量数量,更新运行平均.

> 三行代码完成工作:标记第一次访问状态,增加计数,更新运行平均值.

### 步骤4: ε贪的MC控制 (政策)

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

### 步骤5:与DP黄金标准进行比较

你的 MC估计`V^π`实际上:4×4格里德世界上5万集让你进入了`~0.1`答案的答案.

> 你对`V^π`经验中:4×4 GridWorld 上5万回合可将错误控制在`~0.1`在内

## 陷

- **Infinite episodes.**如果你的政策可以永远循环,`max_steps`格里德世界随机政策经常出,这是正常的,只是确保你正确计算它.
  **无限回合。**要求回合*终止*──如果策略可能永远循环,设置`max_steps`上限并将视为隐式失败.
- **Variance.**在长期的节目中,差异很大.`V(s_0)`通过启动,TD方法 (课4) 减少了这一点.
  **方差。**长回合上方差异很大,最后一步的不幸奖励会同样影响.`V(s_0)`◎TD 方法 (课4) 通过自举来降低方差.
- **State coverage.**贪的MC在新鲜的Q带领只会尝试一个行动.你必须*探索 (ε-贪,探索开始,UCB).
  **状态覆盖。**新Q上的贪心MC只会尝试一个动作――你*必须*探索(ε-贪心、探索起点、UCB) 』
- **Non-stationary policies.**如果`π`常数α MC处理这个问题;样本平均MC不.
  **非平稳策略。**如果`π`变化 (如 MC 控制中),旧回报来自不同策略──常数α MC 处理此问题;样本平均 MC 不能──
- **Off-policy importance sampling.**体重`π(a|s)/μ(a|s)`变量随着视界爆炸. 顶随着每决策权重的IS或转换为TD.
  **离策略重要性采样。**权重`π(a|s)/μ(a|s)`在轨迹上积累相乘――方差随视野爆炸――使用逐决权加加权 IS 限制或转换为 TD――

## 用它实现框架

蒙特卡罗方法的2026年作用:

> 蒙特卡洛方法的角色:

| Use case | Why MC |
|----------|--------|
| Use case / 用例 | Why MC / 为什么用 MC |
| Short-horizon games (blackjack, poker) / 短视野游戏（二十一点、扑克） | Episodes terminate naturally; returns are clean. / 回合自然终止；回报干净。 |
| Offline evaluation of a logged policy / 离线评估已记录的策略 | Average discounted returns over stored trajectories. / 对存储轨迹取折扣回报平均。 |
| Monte Carlo Tree Search (AlphaZero) / 蒙特卡洛树搜索 | MC rollouts from tree leaves guide selection. / 树叶的 MC rollout 指导选择。 |
| LLM RL evaluation / LLM RL 评估 | Compute average reward over sampled completions for a given policy. / 对给定策略的采样完成计算平均奖励。 |
| Baseline estimation in PPO / PPO 中的基线估计 | The advantage target `A_t = G_t - V(s_t)` uses an MC `G_t`. / 优势目标使用 MC 的 `G_t`。 |
| Teaching RL / 教学 RL | Simplest algorithm that actually works — strip bootstrapping to see the core. / 最简单且有效的算法——去掉自举看核心。 |

现代深度RL算法 (PPO,SAC) 通过纯 MC (完全返回) 和纯 TD (单步启动) 间进行间接`n`两种终点都是同一估计器的实例.

> 现代深度 RL 算法(PPO、SAC) 通过 `n`步回报或GAE 在纯 MC (完整回报) 和纯 TD (单步自举) 之间插值.

## 运送它.

保存如`outputs/skill-mc-evaluator.md`其他:

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

## 练习题

1. **Easy.**执行第一次访问 MC 评估4×4格林世界的统一随机政策. 运行10,000集.`V(0,0)`根据事件数与DP答案的函数.
   > **练习1：**实现 MC 评估,将 V(0,0) 随回合数量的收曲线与 DP 基准对比.
2. **Medium.**执行 ε-贪的 MC控制`ε ∈ {0.01, 0.1, 0.3}`现在,我们在20000集后的平均回报.
   > **练习2：**用不同 ε 值做 MC 控制,观察探索-利用权衡──
3. **Hard.**实施*非政策* MC与重要样本采集:根据统一随机政策收集数据`μ`估计`V^π`对于确定性最佳政策`π`根据决定与权重 IS. 哪个有最低差异?
   > **练习3：**实现离策略 MC 重点采样),比较不同 IS 方差的差异

## 关键词 快速查找表

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

## 继续阅读 继续阅读

- [Sutton & Barto (2018). Ch. 5 — Monte Carlo Methods](http://incompleteideas.net/book/RLbook2020.pdf)法典治疗.
- [Singh & Sutton (1996). Reinforcement Learning with Replacing Eligibility Traces](https://link.springer.com/article/10.1007/BF00114726)第一次访问与每次访问分析.
- [Precup, Sutton, Singh (2000). Eligibility Traces for Off-Policy Policy Evaluation](http://incompleteideas.net/papers/PSS-00.pdf)非政策 MC和变化控制.
- [Mahmood et al. (2014). Weighted Importance Sampling for Off-Policy Learning](https://arxiv.org/abs/1404.6362)现代低变量IS估计器.
- [Tesauro (1995). TD-Gammon, A Self-Teaching Backgammon Program](https://dl.acm.org/doi/10.1145/203330.203343)第一次大规模实验性演示 MC/TD自动游戏融合到超人游戏;在这个阶段下半段的每个课程的概念前.
