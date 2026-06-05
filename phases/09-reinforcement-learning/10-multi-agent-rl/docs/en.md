# Multi-Agent RL | 多智能体强化学习

> Single-agent RL assumes the environment is stationary. Put two learning agents in the same world and that assumption breaks: each agent is part of the other's environment, and both are changing. Multi-agent RL is the set of tricks to make learning converge when the Markov assumption no longer holds.

> **【中文解读】** 单智能体 RL 假设环境是平稳的。但放入两个同时学习的智能体后，每个智能体都成了对方环境的一部分——环境不再平稳，马尔可夫假设被打破。多智能体 RL 就是处理"大家都在变"时的收敛问题。

**Type:** Build
**Languages:** Python
**Prerequisites:** Phase 9 · 04 (Q-learning), Phase 9 · 06 (REINFORCE), Phase 9 · 07 (Actor-Critic)
**Time:** ~45 minutes

## The Problem | 问题引入

A robot learning to navigate a room is a single-agent RL problem. A soccer team is not. AlphaStar vs StarCraft opponents is not. A marketplace of bidding agents is not. Two cars negotiating a four-way stop is not. Many-on-many real-world problems are not.

> 机器人学习在房间中导航是单智能体 RL 问题。足球队不是。AlphaStar 对 StarCraft 对手不是。竞价代理的市场不是。两辆车协商四路停车不是。多对多的现实世界问题都不是。

In every multi-agent setting, from the perspective of any one agent, the other agents *are* part of the environment. As they learn and change their behavior, the environment becomes non-stationary. The Markov property — "next state depends only on current state and my action" — gets violated because the next state also depends on what the *other* agents chose, and their policies are moving targets.

> 在每个多智能体环境中，从任一智能体的视角看，其他智能体*是*环境的一部分。当它们学习和改变行为时，环境变得非平稳。马尔可夫性被违反，因为下一状态还取决于*其他*智能体的选择，而它们的策略是移动目标。

This breaks tabular convergence proofs (Q-learning's guarantee assumes a stationary environment). It breaks naive deep RL too: agents chase each other in loops, never converge to a stable policy. You need multi-agent-specific techniques: centralized training / decentralized execution, counterfactual baselines, league play, self-play.

> 这破坏了表格收敛证明（Q-learning 的保证假设平稳环境）。它也破坏了朴素深度 RL：智能体相互追逐循环，永远不收敛到稳定策略。你需要多智能体专用技术：集中训练/分布执行、反事实基线、联盟训练、自我博弈。

2026 applications: robot swarms, traffic routing, autonomous vehicle fleets, market simulators, multi-agent LLM systems (Phase 16), and any game with more than one intelligent player.

> 2026 年应用：机器人集群、交通路由、自动驾驶车队、市场模拟器、多智能体 LLM 系统（Phase 16），以及任何有多个智能玩家的游戏。

> **【中文解读】** 多智能体 RL 的核心挑战：非平稳性（其他智能体也在学习）、信用分配（谁该得到奖励？）、联合动作空间爆炸、部分可观察性。四种主要范式：独立学习（简单但不保证收敛）、CTDE（训练时集中、执行时分布）、自我博弈（AlphaZero）、联盟训练（AlphaStar）。

> **【拓展：多智能体→LLM Agent系统】** 2026 年最热门的 MARL 应用是多智能体 LLM 系统：多个大模型 Agent 协作完成复杂任务。Claude Code 的 multi-agent 模式、AutoGen、CrewAI 等框架本质上都是 MARL 思想在语言 Agent 领域的延伸。

## The Concept | 核心概念

![Four MARL regimes: indep, centralized critic, self-play, league](../assets/marl.svg)

**Formalism: Markov Game.** A generalization of MDP: states `S`, a joint action `a = (a_1, …, a_n)`, transition `P(s' | s, a)`, and per-agent rewards `R_i(s, a, s')`. Each agent `i` maximizes its own return under its own policy `π_i`. If rewards are identical, it is **fully cooperative**. If zero-sum, it is **adversarial**. If mixed, it is **general-sum**.

> **形式化：马尔可夫博弈。** MDP 的推广：状态 `S`、联合动作 `a = (a_1, …, a_n)`、转移 `P(s'|s,a)`、每个智能体的奖励 `R_i`。如果奖励相同，是**全合作**。如果是零和，是**对抗**。如果混合，是**一般和**。

**Core challenges:**

- **Non-stationarity.** `P(s' | s, a_i)` from agent `i`'s view depends on `π_{-i}`, which is changing.
  **非平稳性。** 从智能体 `i` 的视角看，转移取决于其他智能体正在变化的策略。
- **Credit assignment.** With a shared reward, which agent caused it?
  **信用分配。** 共享奖励时，哪个智能体导致的？
- **Exploration coordination.** Agents must explore complementary strategies, not redundantly explore the same state.
  **探索协调。** 智能体必须探索互补策略，而非冗余探索同一状态。
- **Scalability.** The joint action space grows exponentially in `n`.
  **可扩展性。** 联合动作空间随 `n` 指数增长。
- **Partial observability.** Each agent sees only its own observation; the global state is hidden.
  **部分可观察性。** 每个智能体只看到自己的观测；全局状态隐藏。

**Four dominant regimes:**

> **四种主导范式：**

**1. Independent Q-learning / independent PPO (IQL, IPPO).** Each agent learns its own Q or policy, treating others as part of the environment. Simple, sometimes it works (especially with experience replay acting as a smoothing agent-modeling trick). Theoretical convergence: none. In practice: fine for loosely-coupled tasks, bad for tightly-coupled ones.

> **1. 独立 Q-learning / 独立 PPO。** 每个智能体学习自己的 Q 或策略，将其他智能体视为环境的一部分。简单，有时有效。理论收敛性：无。实践：松耦合任务好用，紧耦合任务不好用。

**2. Centralized training, decentralized execution (CTDE).** Most common modern paradigm. Each agent has its own *policy* `π_i` that conditions on local observation `o_i` — standard decentralized execution at deployment. During *training*, a centralized critic `Q(s, a_1, …, a_n)` conditions on the full global state and joint action. Examples:
- **MADDPG** (Lowe et al. 2017): DDPG with a centralized critic per agent.
- **COMA** (Foerster et al. 2017): counterfactual baseline — ask "what would my reward have been if I'd taken action `a'` instead?" — isolates my contribution.
- **MAPPO** / **IPPO** with shared critic (Yu et al. 2022): PPO with a centralized value function. Dominant in 2026 for cooperative MARL.
- **QMIX** (Rashid et al. 2018): value decomposition — `Q_tot(s, a) = f(Q_1(s, a_1), …, Q_n(s, a_n))` with monotonic mixing.

> **2. 集中训练，分布执行（CTDE）。** 最常见的现代范式。每个智能体有自己的策略，只依赖局部观测。训练时使用集中 Critic，条件为全局状态和联合动作。

**3. Self-play.** Two copies of the same agent play each other. The opponent's policy *is* my policy from a past snapshot. AlphaGo / AlphaZero / MuZero. OpenAI Five. Works best for zero-sum games; the training signal is symmetric.

> **3. 自我博弈。** 同一智能体的两个副本对弈。对手的策略*是*我过去快照的策略。最适合零和博弈；训练信号是对称的。

**4. League play.** An extension of self-play to general-sum / adversarial environments: keep a population of past and current policies, sample an opponent from the league, train against them. Adds exploiters (specialize in beating the current best) and main exploiters (specialize in beating exploiters). AlphaStar (StarCraft II). Needed when the game admits "rock-paper-scissors" strategy cycles.

> **4. 联盟训练。** 自我博弈的扩展：保持过去和当前策略的种群，从联盟中采样对手。添加剥削者（专门击败当前最强）。AlphaStar（星际争霸 II）。在游戏允许"石头剪刀布"策略循环时需要。

**Communication.** Allow agents to send learned messages `m_i` to each other. Works in cooperative settings. Foerster et al. (2016) showed that differentiable inter-agent communication can be trained end-to-end. Today's LLM-based multi-agent systems (Phase 16) essentially communicate in natural language.

> **通信。** 允许智能体相互发送学习的消息。在合作环境中有效。今天的 LLM 多智能体系统本质上用自然语言通信。

## Build It | 动手实现

This lesson uses a 6×6 GridWorld with two cooperative agents. They start in opposite corners and must reach a shared goal. Shared reward: `-1` per step while either agent is still moving, `+10` when both arrive. See `code/main.py`.

> 本课使用一个 6×6 GridWorld 和两个合作智能体。它们从对角出发，必须到达共享目标。共享奖励：任一智能体仍在移动时每步 -1，两者都到达时 +10。

### Step 1: the multi-agent env

```python
class CoopGridWorld:
    def __init__(self):
        self.size = 6
        self.goal = (5, 5)

    def reset(self):
        return ((0, 0), (5, 0))  # two agents

    def step(self, state, actions):
        a1, a2 = state
        new1 = move(a1, actions[0])
        new2 = move(a2, actions[1])
        done = (new1 == self.goal) and (new2 == self.goal)
        reward = 10.0 if done else -1.0
        return (new1, new2), reward, done
```

The *joint* action space is `|A|² = 16`. The global state is two positions.

> *联合*动作空间是 `|A|² = 16`。全局状态是两个位置。

### Step 2: independent Q-learning

Each agent runs its own Q-table keyed on joint state. At each step: both pick ε-greedy actions, collect joint transition, each updates its own Q with the shared reward.

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

Works on this task because rewards are dense and aligned. Fails on tightly-coupled tasks (e.g., where one agent has to *wait* for the other).

> 在此任务上有效，因为奖励密集且对齐。在紧耦合任务上失败（例如，一个智能体必须*等待*另一个）。

### Step 3: centralized Q with decomposed-value update

Use one Q over joint actions `Q(s, a_1, a_2)`. Update from shared reward. Decentralize at execution by marginalizing: `π_i(s) = argmax_{a_i} max_{a_{-i}} Q(s, a_1, a_2)`. Trades exponential joint action space for a *correct* global view.

> 使用联合动作上的一个 Q。从共享奖励更新。执行时通过边缘化分布：用指数联合动作空间换取*正确的*全局视角。

### Step 4: simple self-play (adversarial 2-agent)

Same agent, two roles. Train agent A against agent B; after `K` episodes, copy A's weights into B. Symmetric training, consistent progress. The AlphaZero recipe in miniature.

> 同一智能体，两个角色。训练 A 对 B；`K` 回合后将 A 的权重复制到 B。对称训练，持续进步。AlphaZero 配方的缩影。

## Pitfalls

- **Non-stationary replay.** Experience replay with independent agents is worse than single-agent because old transitions were generated by now-obsolete opponents. Fix: relabel or weight by recency.
  **非平稳回放。** 独立智能体的经验回放比单智能体更差，因为旧转移是由已过时的对手生成的。
- **Credit assignment ambiguity.** Shared reward after a long episode; no clear way to say which agent contributed. Fix: counterfactual baselines (COMA), or reward shaping per agent.
  **信用分配模糊。** 长回合后的共享奖励；无法确定哪个智能体贡献了什么。修复：反事实基线或每智能体奖励塑形。
- **Policy drift / chasing.** Each agent's best response changes with each other's update. Fix: centralized critic, slow learning rates, or freeze-one-at-a-time.
  **策略漂移/追逐。** 每个智能体的最佳响应随其他智能体的更新而变化。修复：集中 Critic、慢学习率或逐个冻结。
- **Reward hacking via coordination.** Agents find coordinated exploits the designer did not anticipate. Auction agents converge to bid zero. Fix: careful reward design, behavioral constraints.
  **协调奖励黑客。** 智能体发现设计者未预料的协调漏洞。修复：仔细的奖励设计、行为约束。
- **Exploration redundancy.** Both agents explore the same state-action pairs. Fix: entropy bonuses per-agent, or role-conditioning.
  **探索冗余。** 两个智能体探索相同的状态-动作对。修复：每智能体熵奖励或角色条件化。
- **League cycles.** Pure self-play can get stuck in a dominance cycle. Fix: league play with diverse opponents.
  **联盟循环。** 纯自我博弈可能陷入支配循环。修复：多样化对手的联盟训练。
- **Sample explosion.** `n` agents × state space × joint actions. Approximate with function approximation; factored action spaces (one policy output head per agent).
  **样本爆炸。** n 个智能体 × 状态空间 × 联合动作。用函数近似解决；因子化动作空间。

## Use It | 用框架实现

The 2026 MARL application map:

> 2026 年 MARL 应用地图：

| Domain | Method | Notes |
|--------|--------|-------|
| Domain / 领域 | Method / 方法 | Notes / 备注 |
| Cooperative navigation / manipulation / 合作导航/操作 | MAPPO / QMIX | CTDE; shared critic + decentralized actors. / CTDE；共享 Critic + 分布式 Actor。 |
| Two-player games (chess, Go, poker) / 双人游戏 | Self-play with MCTS (AlphaZero) | Zero-sum; symmetric training. / 零和；对称训练。 |
| Complex multiplayer (Dota, StarCraft) / 复杂多人游戏 | League play + imitation pretraining | OpenAI Five, AlphaStar. |
| Autonomous-vehicle fleets / 自动驾驶车队 | CTDE MAPPO / PPO with attention | Partial obs; variable team sizes. / 部分可观察；可变团队大小。 |
| Auction markets / 拍卖市场 | Game-theoretic equilibrium + RL | Mean-field RL when `n` → ∞. / n→∞ 时用平均场 RL。 |
| LLM multi-agent systems (Phase 16) / LLM 多智能体系统 | Natural-language comm + role conditioning | RL loop at the agent-planning layer. / Agent 规划层的 RL 循环。 |

In 2026, MARL's biggest growth area is LLM-based: swarms of language-model agents negotiating, debating, building software. The RL shows up as preference optimization on *trajectory-level* outputs, not token-level (Phase 16 · 03).

> 2026 年 MARL 最大增长领域是基于 LLM 的：语言模型智能体群体协商、辩论、构建软件。RL 出现在*轨迹级*输出的偏好优化上，而非 token 级。

## Ship It | 产出物

Save as `outputs/skill-marl-architect.md`:

```markdown
---
name: marl-architect
description: Pick the right multi-agent RL regime (IPPO, CTDE, self-play, league) for a given task.
version: 1.0.0
phase: 9
lesson: 10
tags: [rl, multi-agent, marl, self-play]
---

Given a task with `n` agents, output:

1. Regime classification. Cooperative / adversarial / general-sum. Justify.
2. Algorithm. IPPO / MAPPO / QMIX / self-play / league. Reason tied to coupling tightness and reward structure.
3. Information access. Centralized training (what global info goes to the critic)? Decentralized execution?
4. Credit assignment. Counterfactual baseline, value decomposition, or reward shaping.
5. Exploration plan. Per-agent entropy, population-based training, or league.

Refuse independent Q-learning on tightly-coupled cooperative tasks. Refuse to recommend self-play for general-sum with cycle risks. Flag any MARL pipeline without a fixed-opponent eval (cherry-picked self-play numbers are common).
```

## Exercises | 练习题

1. **Easy.** Train independent Q-learning on the 2-agent cooperative GridWorld. How many episodes until mean return > 0? Plot the joint learning curve.
2. **Medium.** Add a "coordination" task: the goal is reached only when both agents step onto it on the same turn. Does independent Q still converge? What breaks?
3. **Hard.** Implement a centralized critic for MAPPO-style training and compare convergence speed to independent PPO on the coordination task.

## Key Terms | 术语速查表

| Term | What people say | What it actually means |
|------|-----------------|-----------------------|
| Markov game | "Multi-agent MDP" / 马尔可夫博弈 | `(S, A_1, …, A_n, P, R_1, …, R_n)`; each agent has its own reward. |
| CTDE | "Centralized training, decentralized execution" / 集中训练分布执行 | Joint critic at training time; each agent's policy uses only local obs. |
| IPPO | "Independent PPO" / 独立 PPO | Each agent runs PPO separately. Simple baseline; often underrated. |
| MAPPO | "Multi-agent PPO" / 多智能体 PPO | PPO with a centralized value function conditioned on global state. |
| QMIX | "Monotonic value decomposition" / 单调值分解 | `Q_tot = f_monotone(Q_1, …, Q_n)` allows decentralized argmax. |
| COMA | "Counterfactual multi-agent" / 反事实多智能体 | Advantage = my Q minus expected Q marginalizing over my action. |
| Self-play | "Agent vs past self" / 自我博弈 | Single agent, two roles; standard for zero-sum games. |
| League play | "Population training" / 联盟训练 | Cache past policies, sample opponents from the pool; handles strategy cycles. |

## Further Reading | 延伸阅读

- [Lowe et al. (2017). Multi-Agent Actor-Critic for Mixed Cooperative-Competitive Environments (MADDPG)](https://arxiv.org/abs/1706.02275) — CTDE with a centralized critic.
- [Foerster et al. (2017). Counterfactual Multi-Agent Policy Gradients (COMA)](https://arxiv.org/abs/1705.08926) — counterfactual baselines for credit assignment.
- [Rashid et al. (2018). QMIX: Monotonic Value Function Factorisation](https://arxiv.org/abs/1803.11485) — value decomposition with monotonicity.
- [Yu et al. (2022). The Surprising Effectiveness of PPO in Cooperative Multi-Agent Games (MAPPO)](https://arxiv.org/abs/2103.01955) — PPO is surprisingly strong for MARL.
- [Vinyals et al. (2019). Grandmaster level in StarCraft II using multi-agent reinforcement learning (AlphaStar)](https://www.nature.com/articles/s41586-019-1724-z) — league play at scale.
- [Silver et al. (2017). Mastering the game of Go without human knowledge (AlphaGo Zero)](https://www.nature.com/articles/nature24270) — pure self-play in zero-sum games.
- [Sutton & Barto (2018). Ch. 15 — Neuroscience & Ch. 17 — Frontiers](http://incompleteideas.net/book/RLbook2020.pdf) — includes the textbook's short treatment of multi-agent settings and the non-stationarity problem that CTDE is designed to solve.
- [Zhang, Yang & Başar (2021). Multi-Agent Reinforcement Learning: A Selective Overview](https://arxiv.org/abs/1911.10635) — survey covering cooperative, competitive, and mixed MARL with convergence results.
