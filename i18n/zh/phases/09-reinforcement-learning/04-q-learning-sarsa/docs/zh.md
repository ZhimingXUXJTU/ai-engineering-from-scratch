# 时间差距  Q学习与SARSA

> 蒙特卡洛等到集结束.TD每一步都会通过启动下一个值估计进行更新.Q-学习是非政策和乐观的;SARSA是政策和谨慎的.这两条都是一个代码线.这两条都支持了这个阶段的每种深度RL方法.

> **【中文解读】**必须等到回合结束才能更新,TD(时间差分) 每一步都能更新用`r + γ V(s')`作为引导当前估计的目标. -学习是离策略的,SARSA是在线策略的,学习当前行为策略.`max`它们是所有深度RL的基础.

**Type:** Build | **类型:** 动手
**Languages:** Python | **语言:** Python
**Prerequisites:** Phase 9 · 01 (MDPs), Phase 9 · 02 (Dynamic Programming), Phase 9 · 03 (Monte Carlo) | **前置知识:** Phase 9 · 01 (MDP), Phase 9 · 02 (动态规划), Phase 9 · 03 (蒙特卡洛)
**Time:** ~75 minutes | **时间:** ~75 分钟

## 问题 问题引入

蒙特卡洛工作,但它有两个昂贵的要求.它需要结束的集,并且只有在最后的回报后更新.如果你的集是1000步,MC等待1000步更新任何东西.它是高变异,低偏见,并缓慢的实践.

> 卡洛是有效的,但有两个昂贵的要求. 它需要终止循环,而且只有在最终回报出炉后才更新. 如果回合有1000步,MC必须等1000步才能更新任何东西.

动态编程具有相反的配置文件,但需要已知的模型.

> 动态规划有相反的特点零方差的自举备份但需要已知模型

时间差异 (TD) 学习将差异分开.`(s, a, r, s')`形成一个步骤的目标`r + γ V(s')`着着`V(s)`没有模型,没有完整的集,使用近似的偏见.`V`在RHS上,但与MC和在线更新相比,

> 时序差分(TD) 学习折中了两者――从单次转移 `(s, a, r, s')`构建单步目标`r + γ V(s')`将`V(s)`向其靠近──不需要模型──不需要完整回合──因为右侧使用近似`V`差距远低于MC,从第一步就能在线更新.

现在,我们在第9阶段的基础上将使用一个步骤的TD更新,然后再进行一个步骤的TD更新.

> 这是所有现代RLDQN、A2C、PPO、SAC的枢纽. 第9阶段的剩余部分是你将在本课程中编写的单步TD更新的构建函数近似和技巧层.

> **【中文解读】**通过单步转移,`(s,a,r,s')`构建目标`r + γV(s')`由于使用近似V,而差距远低于MC,而且可以在线更新.

> **【拓展：游戏AI→LLM对齐】**基于TD差异的思想,理解Q-学习和SARSA是理解大模型对齐训练的基础.

## 概念的核心概念

![Q-learning vs SARSA: off-policy max vs on-policy Q(s', a')](../assets/td.svg)

**The TD(0) update for V:**

`V(s) ← V(s) + α [r + γ V(s') - V(s)]`

括数量是TD错误`δ = r + γ V(s') - V(s)`它是网上模拟的`G_t - V(s_t)`在MC. 融合需要`α`满足罗宾斯-蒙罗的需求 (`Σ α = ∞`现在`Σ α² < ∞`许多国家都经常访问.

> **V 的 TD(0) 更新：**括号中的量是 TD 误差`δ = r + γ V(s') - V(s)`,这是一个MC中.`G_t - V(s_t)`收要求 收要求`α`满足罗宾斯-蒙罗条件和所有状态被无限次访问.

**Q-learning.**控制的非政策TD方法:

`Q(s, a) ← Q(s, a) + α [r + γ max_{a'} Q(s', a') - Q(s, a)]`

其他`max`假设从`s'`无论代理人做什么,这种脱而出,使Q学习学习.`Q*`在Atari (课程05) 上,Mnih et al. (2015) 将这转化为深度Q学习.

> **Q-learning。**一种离策略 TD 控制方法`max`假设从`s'`开始将遵循*贪心*策略,无论智能体实际采取什么动作.`Q*`〔Mnih 等人 (2015) 将将此转化为Atari 上的深度Q学习(05课程〕

**SARSA.**政策上的TD方法:

`Q(s, a) ← Q(s, a) + α [r + γ Q(s', a') - Q(s, a)]`

现在,这个叫""`(s, a, r, s', a')` SARSA使用该行动`a'`现在,那个代理人是接下来的,而不是贪的人.`argmax`合到`Q^π`为了什么是贪的`π`现在,它正在运行,`ε → 0`成为`Q*`现在,我们要去.

> **SARSA。**一种在线策略 TD 方法──名称是元组`(s, a, r, s', a')`◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎`a'`而不是贪的.`argmax`〔收到当前〕`π`的`Q^π`在`ε → 0`极限下变为`Q*`,我知道.

**The cliff-walking difference.**在经典的悬崖行走任务 (落下悬崖 = 奖励 -100),Q-学习学习沿悬崖边缘的最佳路径,但偶尔在探索过程中承担罚款.SARSA学习一个更安全的路径,因为它将探索噪音纳入其Q值.`ε → 0`在实践中,这很重要:当探索实际发生在部署时,SARSA的行为更保守.

> **【中文解读】**经典悬崖走行实验揭示了Q学习与SARSA的关键区别:Q学习学习悬崖上最好的路径,但探索时会掉下来,SARSA学习远离悬崖的安全路径,因为它考虑了探索噪音.

**Expected SARSA.**取代`Q(s', a')`预期值低于`π`其他:

`Q(s, a) ← Q(s, a) + α [r + γ Σ_{a'} π(a'|s') Q(s', a') - Q(s, a)]`

较 SARSA较低的变异性 (没有样本`a'`常常是现代教科书中的默认.

> **期望 SARSA。**用`π`下的期望值替换`Q(s', a')`△比 SARSA 方差更低`a'`),相同的在线策略目标──常作为现代教科书的默认选择──

**n-step TD and TD(λ).**通过等待来间隔TD(0) 和MC`n`起步前的步骤.`n=1`是TD,`n=∞`是 MC. TD(λ) 平均值`n`具有几何权重`(1-λ)λ^{n-1}`大多数深度RL使用`n`在3到20之间.

> **n 步 TD 和 TD(λ)。**在 TD(0) 和 MC 之间插值,等待`n`步再自举.`n=1`是TD,`n=∞`是 MC──TD(λ) 用几何权重对所有`n`取平均──大多数深度 RL 使用 `n`在3到20之间.

> **【拓展：TD 误差在 LLM RLHF 中的对应】**率差差 δ = r + γV(s') - V(s) 在LLM的 RLHF 训练中有直接对应:PPO的优势函数 A = r + γV(s') - V(s) 就是 TD 差差的变体――每生成一个代币,计算当前代币的奖励――来自RM) 加上对未来价值的估计减小的评论者――理解 TD 差是理解 PPO 优势函数的关键――

## 建立它,实现它.
```figure
qlearning-gridworld
```

## 建立它

### 步骤1:关于利政策的SARS

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

只有一个区别与Q学习是目标线.

> 八行代码──与Q学习的唯一区别是目标行──

### 步骤2:Q学习

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

其他`max`目标与行为分离. 这一符号是政策和非政策之间的区别.

> `max`实现目标与行为解. 这一符号是网络策略与离策略的区别.

### 步骤3:学习曲线

追踪平均回报每100集.Q学习在简单的确定性格里德世界上更快地融合;SARSA在悬崖行走上更保守.在4×4格里德世界上`code/main.py`两部都在2000集后接近最佳`α=0.1, ε=0.1`现在,我们要去.

> 随着每100回合的平均回报. 简单确定性,`code/main.py`,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,`α=0.1, ε=0.1`约有2000回合后接近最优.

### 步骤4:与DP真相相比较

运行值回复 (课程02) 得到`Q*`查看`max_{s,a} |Q_learned(s,a) - Q*(s,a)|`一个健康的表表表TD代理落地在`~0.5`在4×4格林世界上,经过1万集.

> 运行值代(课02)获得 `Q*`查查`max_{s,a} |Q_learned(s,a) - Q*(s,a)|`△一个健康的表格 TD 智能体在10,000回合后在4×4格格世界上误差在`~0.5`在内

## 陷

- **Initial Q values matter.**乐观的初步 (`Q = 0`悲观的初步可以永远陷入贪的政治陷.
  **初始 Q 值很重要。**乐观初始化 负奖励任务中`Q = 0`为了鼓励探索,悲观初始化可能永远困住贪心策略.
- **α schedule.**持续`α`对于非静态问题来说,很好.`α_n = 1/n`在理论上,它能实现相近性,但在实践中却太慢了.`α`在`[0.05, 0.3]`监视学习曲线.
  **α 调度。**常数`α`适用于不平稳问题――衰退的`α_n = 1/n`理论上收取,但实践中太慢了.`α`固定在`[0.05, 0.3]`并监控学习曲线.
- **ε schedule.**开始高 (`ε=1.0`), 衰退到`ε=0.05`利 (贪在极限的探索) 是化条件.
  **ε 调度。**从高值开始`ε=1.0`),衰减到`ε=0.05`极限贪心且无限探索) 是收条件.
- **Max bias in Q-learning.**其他`max`操作员偏向上升时`Q`导致过度估值 哈塞尔特的双重Q学习 (DDQN在05课中使用) 用两个Q表来解决这一问题.
  **Q-learning 的最大化偏差。** `max`算子在`Q`哈塞尔的双重Q学习 (DDQN中文课5)
- **Non-terminating episodes.**标准:把作为非终端,继续启动.
  **非终止回合。**标准做法:将上限视为不终止,继续自行举动.
- **State hashing.**如果状态是体/体,请使用可的键 (体,而不是列表;体圆,而不是原始).
  **状态哈希。**如果状态是元组/张量,使用可哈希的键 (元组而非列表;舍入的浮点数元组而非原始值) 

## 用它实现框架

2026年特工技术景观:

> 美国国家经济发展部的2026年学年版图:

| Task | Method | Reason |
|------|--------|--------|
| Task / 任务 | Method / 方法 | Reason / 原因 |
| Small tabular environments / 小型表格环境 | Q-learning | Learns optimal policy directly. / 直接学习最优策略。 |
| On-policy safety-critical / 在线策略安全关键 | SARSA / Expected SARSA | Conservative during exploration. / 探索期间保守。 |
| High-dimensional state / 高维状态 | DQN (Phase 9 · 05) | Neural-net Q-function with replay and target net. / 神经网络 Q 函数+回放+目标网络。 |
| Continuous actions / 连续动作 | SAC / TD3 (Phase 9 · 07) | TD update on a Q-network; policy net emits actions. / Q 网络上的 TD 更新；策略网络输出动作。 |
| LLM RL (reward-model-based) / LLM RL（基于奖励模型） | PPO / GRPO (Phase 9 · 08, 12) | Actor-critic with TD-style advantage via GAE. / Actor-Critic + GAE 的 TD 式优势。 |
| Offline RL / 离线 RL | CQL / IQL (Phase 9 · 08) | Q-learning with conservative regularization. / 带保守正则化的 Q-learning。 |

在2026年报纸中,你读到的"RL"中90%是Q学习或SARSA的精细化.

> 在2026年论文中你读到的"RL",90%是Q学习或SARSA的某种变化.

## 运送它.

保存如`outputs/skill-td-agent.md`其他:

```markdown
---
name: td-agent
description: Pick between Q-learning, SARSA, Expected SARSA for a tabular or small-feature RL task.
version: 1.0.0
phase: 9
lesson: 4
tags: [rl, td-learning, q-learning, sarsa]
---

Given a tabular or small-feature environment, output:

1. Algorithm. Q-learning / SARSA / Expected SARSA / n-step variant. One-sentence reason tied to on-policy vs off-policy and variance.
2. Hyperparameters. α, γ, ε, decay schedule.
3. Initialization. Q_0 value (optimistic vs zero) and justification.
4. Convergence diagnostic. Target learning curve, `|Q - Q*|` check if DP is possible.
5. Deployment caveat. How will exploration behave at inference? Is SARSA's conservatism needed?

Refuse to apply tabular TD to state spaces > 10⁶. Refuse to ship a Q-learning agent without a max-bias caveat. Flag any agent trained with ε held at 1.0 throughout (no exploitation phase).
```

## 练习题

1. **Easy.**实现Q学习和SARSA在4×4格林世界. 绘制学习曲线 (每100集的平均回报) 进行2000集.谁更快地融合?
   > **练习1：**在GridWorld上对比Q学习和SARSA的学习曲线.
2. **Medium.**建立一个悬崖走路环境 (4×12,最后一行是悬崖,奖励 -100,重新设置开始).比较Q学习和SARSA最终政策.截图每个路径.哪个离悬崖更近?
   > **练习2：**实现悬崖行走环境,观察Q学习的策略差异
3. **Hard.**在一个噪音奖励格里德世界 (加加加加加加加加加加加加加加加加加加加加加加加加加加加加加加加加加加加加加加加加加加加加加加加加加加加加加加加加加加加加加加加加加加加加加加加加加加加加加加加加加加加加加加加加加加加加加加加加加加加加加加加加加加加加加加加加加加加加加加加加加加加加加加加加加加加加加加加加加加加加加加加加加加加加加加加加加加加加加加加加加加加加加加加加加加加加加加加加加加加加加加加加加加加加加加加加加加加加加加加加加加加加加加加加加加加加加加加加加加加加加加加加加加加加加加加加加加加加加加加加加加加加加加加加加加加加加加加加加加加加加加加加加加加加加加加加加加加加加加加加加加加加加加加加加加加加加加加加加加加加加加加加加加加加加加加加加加加加加加加加加加加加加加加加加加加加加加加加加加加加加加加加加加加加加加加加加加加加加加加加加加加加加加加加加加加加加加加加加加加加加加加加加加加加加加加加加加加加加加加加加加加加加加加加加加加加加加加加加加加加加加加加加加加加加加加加加加加加加加加加加加加加加加加加加加加加加加加加加加加加加加加加加加加加加加加加加加加加加加加加加加加加加加加加加加加加加加加加加加加`V*(0,0)`双重Q学习没有.
   > **练习3：**实现双重Q学习,验证它能够消除Q学习最大化偏差.

## 关键词 快速查找表

| Term | What people say | What it actually means |
|------|-----------------|-----------------------|
| TD error | "The update signal" / TD 误差 | `δ = r + γ V(s') - V(s)`, the bootstrapped residual. |
| TD(0) | "One-step TD" / 单步 TD | Update after every transition using only the next state's estimate. |
| Q-learning | "Off-policy RL 101" / Q 学习 | TD update with `max` over next-state actions; learns `Q*` regardless of behavior policy. |
| SARSA | "On-policy Q-learning" / SARSA | TD update using the actual next action; learns `Q^π` for current ε-greedy π. |
| Expected SARSA | "The low-variance SARSA" / 期望 SARSA | Replace sampled `a'` with its expectation under π. |
| GLIE | "Correct exploration schedule" / 无限探索极限贪心 | Greedy in the Limit with Infinite Exploration; needed for Q-learning convergence. |
| Bootstrapping | "Using current estimate in the target" / 自举 | What distinguishes TD from MC. Source of bias but massive variance reduction. |
| Maximization bias | "Q-learning overestimates" / 最大化偏差 | `max` over noisy estimates is upward-biased; fixed by Double Q-learning. |

## 继续阅读 继续阅读

- [Watkins & Dayan (1992). Q-learning](https://link.springer.com/article/10.1007/BF00992698)原始文件和相近性证明.
- [Sutton & Barto (2018). Ch. 6 — Temporal-Difference Learning](http://incompleteideas.net/book/RLbook2020.pdf) TD(0),SARSA,Q学习,预期SARSA.
- [Hasselt (2010). Double Q-learning](https://papers.nips.cc/paper_files/paper/2010/hash/091d584fced301b442654dd8c23b3fc9-Abstract.html)对最大化偏见的修正.
- [Seijen, Hasselt, Whiteson, Wiering (2009). A Theoretical and Empirical Analysis of Expected SARSA](https://ieeexplore.ieee.org/document/4927542)预期 SARSA动机.
- [Rummery & Niranjan (1994). On-line Q-learning using connectionist systems](https://www.researchgate.net/publication/2500611_On-Line_Q-Learning_Using_Connectionist_Systems)创建了SARSA的论文 (当时被称为"修改的连接性Q学习").
- [Sutton & Barto (2018). Ch. 7 — n-step Bootstrapping](http://incompleteideas.net/book/RLbook2020.pdf)将TD(0) 概括为TD(n),从Q学习到资格追踪的路径,后来,在PPO中GAE.
