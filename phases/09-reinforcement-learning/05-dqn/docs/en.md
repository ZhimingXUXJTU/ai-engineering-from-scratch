# Deep Q-Networks (DQN) | 深度Q网络

> 2013: Mnih trained one Q-learning network on raw pixels, beat every classical RL agent on seven Atari games. 2015: extended to 49 games, published in Nature, sparked the deep-RL era. DQN is Q-learning plus three tricks that make function approximation stable.

> **【中文解读】** DQN = Q-learning + 神经网络 + 三个稳定化技巧（经验回放、目标网络、奖励裁剪）。2013-2015 年在 Atari 游戏上击败所有经典 RL 方法，开启了深度 RL 时代。这三个技巧至今仍被所有深度 RL 方法使用。

**Type:** Build
**Languages:** Python
**Prerequisites:** Phase 3 · 03 (Backpropagation), Phase 9 · 04 (Q-learning, SARSA)
**Time:** ~75 minutes

## The Problem | 问题引入

Tabular Q-learning needs a separate Q-value for every (state, action) pair. A chess board has ~10⁴³ states. An Atari frame is 210×160×3 = 100,800 features. Tabular RL dies at thousands of states, let alone billions.

> 表格 Q-learning 需要为每个（状态，动作）对单独存储一个 Q 值。一个国际象棋棋盘有约 10⁴³ 个状态。一个 Atari 帧有 210×160×3 = 100,800 个特征。表格 RL 在数千个状态时就已经失效，更不用说数十亿了。

The fix is obvious in hindsight: replace the Q-table with a neural network, `Q(s, a; θ)`. But obvious-in-hindsight took decades. Naive function approximation with Q-learning diverges under the "deadly triad" — function approximation + bootstrapping + off-policy learning. Mnih et al. (2013, 2015) identified three engineering tricks that stabilize learning:

> 事后看解决方案很简单：用神经网络 `Q(s, a; θ)` 替换 Q 表。但这个"简单"花了数十年。朴素的函数近似与 Q-learning 在"致命三要素"下会发散——函数近似 + 自举 + 离策略学习。Mnih 等人（2013、2015）确定了三个稳定学习的工程技巧：

1. **Experience replay** decorrelates transitions.
   **经验回放** 打破转移的时间相关性。
2. **Target network** freezes the bootstrap target.
   **目标网络** 冻结自举目标。
3. **Reward clipping** normalizes gradient magnities.
   **奖励裁剪** 归一化梯度量级。

DQN on Atari was the first time a single architecture with a single hyperparameter set solved dozens of control problems from raw pixels. Everything "deep-RL" built since — DDQN, Rainbow, Dueling, Distributional, R2D2, Agent57 — is stacked on top of this three-trick base.

> Atari 上的 DQN 是第一次用单一架构和单一超参数集从原始像素解决数十个控制问题。此后构建的所有"深度 RL"——DDQN、Rainbow、Dueling、Distributional、R2D2、Agent57——都建立在这三个技巧之上。

> **【中文解读】** "致命三要素"：函数近似 + 自举 + 离策略 → 训练不稳定甚至发散。DQN 的三个技巧解决了这个问题：(1) 经验回放打破时间相关性；(2) 目标网络冻结自举目标；(3) 奖励裁剪归一化梯度。所有后续深度 RL 算法都建立在这三个技巧之上。

> **【拓展：经验回放→RLHF】** 经验回放 (Experience Replay) 的思想在 LLM 训练中无处不在：PPO 训练时的 buffer、RLHF 中的偏好数据集、DPO 的离线数据——本质上都是"打破数据相关性、反复利用经验"。

## The Concept | 核心概念

![DQN training loop: env, replay buffer, online net, target net, Bellman TD loss](../assets/dqn.svg)

**The objective.** DQN minimizes the one-step TD loss on a neural Q-function:

`L(θ) = E_{(s,a,r,s')~D} [ (r + γ max_{a'} Q(s', a'; θ^-) - Q(s, a; θ))² ]`

`θ` = online network, updated every step by gradient descent. `θ^-` = target network, periodically copied from `θ` (every ~10,000 steps). `D` = replay buffer of past transitions.

> **目标。** DQN 最小化神经 Q 函数上的单步 TD 损失。`θ` = 在线网络，每步通过梯度下降更新。`θ^-` = 目标网络，定期从 `θ` 复制（约每 10,000 步）。`D` = 过去转移的回放缓冲区。

**The three tricks, in order of importance:**

> **三个技巧，按重要性排序：**

**Experience replay.** A ring buffer of `~10⁶` transitions. Each training step samples a minibatch uniformly at random. This breaks temporal correlation (successive frames are nearly identical), lets the network learn from rare rewarding transitions many times, and decorrelates consecutive gradient updates. Without it, on-policy TD with a neural net diverges on Atari.

> **经验回放。** 一个约 10⁶ 次转移的环形缓冲区。每次训练步骤随机均匀采样一个小批次。这打破了时间相关性（连续帧几乎相同），让网络多次学习稀有奖励转移，并去相关连续的梯度更新。

**Target network.** Using the same network `Q(·; θ)` on both sides of the Bellman equation makes the target move every update — "chasing your own tail." The fix: keep a second network `Q(·; θ^-)` with frozen weights. Every `C` steps, copy `θ → θ^-`. This stabilizes the regression target for thousands of gradient steps at a time. Soft updates `θ^- ← τ θ + (1-τ) θ^-` (used in DDPG, SAC) are a smoother variant.

> **目标网络。** 在 Bellman 方程两侧使用同一网络会使目标每次更新都在移动——"追逐自己的尾巴"。修复方法：保留一个权重冻结的第二网络。每 `C` 步复制 `θ → θ^-`。软更新（DDPG、SAC 中使用）是更平滑的变体。

**Reward clipping.** Atari reward magnitudes vary from 1 to 1000+. Clipping to `{-1, 0, +1}` stops any single game from dominating the gradient. Wrong when reward magnitude matters; fine for Atari where only sign matters.

> **奖励裁剪。** Atari 奖励量级从 1 到 1000+不等。裁剪到 `{-1, 0, +1}` 防止任何单个游戏主导梯度。

**Double DQN.** Hasselt (2016) fixes maximization bias: use the online net to *select* the action, the target net to *evaluate* it.

`target = r + γ Q(s', argmax_{a'} Q(s', a'; θ); θ^-)`

Drop-in replacement, consistently better. Use it by default.

> **双重 DQN。** Hasselt (2016) 修复最大化偏差：用在线网络*选择*动作，用目标网络*评估*它。直接替换，始终更好。默认使用。

**Other improvements (Rainbow, 2017):** prioritized replay (sample high-TD-error transitions more), dueling architecture (separate `V(s)` and advantage heads), noisy networks (learned exploration), n-step returns, distributional Q (C51/QR-DQN), multi-step bootstrapping. Each adds a few percent; the gains are roughly additive.

> **其他改进（Rainbow, 2017）：** 优先回放、决斗架构、噪声网络、n 步回报、分布式 Q、多步自举。每种改进贡献几个百分点；收益大致可叠加。

> **【拓展：Rainbow DQN 与集成改进】** Rainbow DQN（2017）将 6 种 DQN 改进集成在一起：优先经验回放、Dueling 架构、噪声网络探索、n 步回报、分布式 Q 学习、多步自举。每种改进贡献几个百分点的性能提升，组合起来效果显著。这种"增量集成"思路在 LLM 训练中也有体现——数据质量、训练策略、架构改进的效果通常是叠加的。

## Build It | 动手实现

The code here is stdlib-only numpy-free — we use a hand-rolled single-hidden-layer MLP on a tiny continuous GridWorld, so every training step runs in microseconds. The algorithm is identical to Atari DQN at scale.

> 这里的代码仅使用标准库——在一个微型连续 GridWorld 上使用手写的单隐藏层 MLP。算法与大规模 Atari DQN 完全相同。

### Step 1: replay buffer

```python
class ReplayBuffer:
    def __init__(self, capacity):
        self.buf = []
        self.capacity = capacity
    def push(self, s, a, r, s_next, done):
        if len(self.buf) == self.capacity:
            self.buf.pop(0)
        self.buf.append((s, a, r, s_next, done))
    def sample(self, batch, rng):
        return rng.sample(self.buf, batch)
```

~50,000 capacity for Atari; 5,000 suffices for our toy env.

> Atari 约需 50,000 容量；我们的玩具环境 5,000 就够了。

### Step 2: a tiny Q-network (manual MLP)

```python
class QNet:
    def __init__(self, n_in, n_hidden, n_actions, rng):
        self.W1 = [[rng.gauss(0, 0.3) for _ in range(n_in)] for _ in range(n_hidden)]
        self.b1 = [0.0] * n_hidden
        self.W2 = [[rng.gauss(0, 0.3) for _ in range(n_hidden)] for _ in range(n_actions)]
        self.b2 = [0.0] * n_actions
    def forward(self, x):
        h = [max(0.0, sum(w * xi for w, xi in zip(row, x)) + b) for row, b in zip(self.W1, self.b1)]
        q = [sum(w * hi for w, hi in zip(row, h)) + b for row, b in zip(self.W2, self.b2)]
        return q, h
```

Forward pass: linear → ReLU → linear. That is the entire net.

> 前向传播：线性 → ReLU → 线性。这就是整个网络。

### Step 3: the DQN update

```python
def train_step(online, target, batch, gamma, lr):
    grads = zeros_like(online)
    for s, a, r, s_next, done in batch:
        q, h = online.forward(s)
        if done:
            y = r
        else:
            q_next, _ = target.forward(s_next)
            y = r + gamma * max(q_next)
        td_error = q[a] - y
        accumulate_grads(grads, online, s, h, a, td_error)
    apply_sgd(online, grads, lr / len(batch))
```

The shape is Q-learning from Lesson 04 with two differences: (a) we backprop through a differentiable `Q(·; θ)` instead of indexing a table, (b) the target uses `Q(·; θ^-)`.

> 形式与 Lesson 04 的 Q-learning 相同，但有两个区别：(a) 通过可微的 `Q(·; θ)` 反向传播而非索引表格，(b) 目标使用 `Q(·; θ^-)`。

### Step 4: the outer loop

For each episode, act ε-greedy on `Q(·; θ)`, push transitions into the buffer, sample a minibatch, take a gradient step, periodically sync `θ^- ← θ`. The pattern:

```python
for episode in range(N):
    s = env.reset()
    while not done:
        a = epsilon_greedy(online, s, epsilon)
        s_next, r, done = env.step(s, a)
        buffer.push(s, a, r, s_next, done)
        if len(buffer) >= batch:
            train_step(online, target, buffer.sample(batch), gamma, lr)
        if steps % sync_every == 0:
            target = copy(online)
        s = s_next
```

On our tiny GridWorld with a 16-dim one-hot state, the agent learns a near-optimal policy in ~500 episodes. On Atari, scale this to 200M frames and add a CNN feature extractor.

> 在我们使用 16 维 one-hot 状态的微型 GridWorld 上，智能体在约 500 回合内学到接近最优的策略。在 Atari 上，扩展到 2 亿帧并添加 CNN 特征提取器。

## Pitfalls

- **Deadly triad.** Function approximation + off-policy + bootstrapping can diverge. DQN mitigates with target net + replay; do not remove either.
  **致命三要素。** 函数近似+离策略+自举可能发散。DQN 通过目标网络+回放缓解；不要移除任何一个。
- **Exploration.** ε must decay, typically from 1.0 to 0.01 over the first ~10% of training. Without enough early exploration the Q-net converges to a local basin.
  **探索。** ε 必须衰减，通常从 1.0 到 0.01，覆盖前约 10% 的训练。没有足够的早期探索，Q 网络会收敛到局部盆。
- **Overestimation.** `max` over noisy Q is upward-biased. Always use Double DQN in production.
  **过估计。** 对有噪声的 Q 取 `max` 会向上偏倚。生产中始终使用双重 DQN。
- **Reward scale.** Clip or normalize rewards; the gradient magnitude is proportional to reward magnitude.
  **奖励尺度。** 裁剪或归一化奖励；梯度量级与奖励量级成正比。
- **Replay buffer coldstart.** Don't train until the buffer has a few thousand transitions. Early gradients on ~20 samples overfit.
  **回放缓冲区冷启动。** 缓冲区有几千次转移后再训练。早期约 20 个样本上的梯度会过拟合。
- **Target sync frequency.** Too frequent ≈ no target net; too infrequent ≈ stale targets. Atari DQN uses 10,000 env steps. Rule of thumb: sync every ~1/100 of training horizon.
  **目标同步频率。** 太频繁≈没有目标网络；太不频繁≈过时目标。经验法则：每约 1/100 训练视野同步一次。
- **Observation preprocessing.** Atari DQN stacks 4 frames to make state Markov. Any env with velocity info needs frame-stacking or recurrent state.
  **观测预处理。** Atari DQN 堆叠 4 帧使状态满足马尔可夫性。任何有速度信息的环境都需要帧堆叠或循环状态。

## Use It | 用框架实现

In 2026, DQN is rarely state-of-the-art but remains the reference off-policy algorithm:

> 2026 年，DQN 很少是最先进的，但仍是离策略算法的参照：

| Task | Method of choice | Why not DQN? |
|------|------------------|--------------|
| Task / 任务 | Method of choice / 首选方法 | Why not DQN? / 为什么不用 DQN？ |
| Discrete-action Atari-like / 离散动作类 Atari | Rainbow DQN or Muesli | Same framework, more tricks. / 相同框架，更多技巧。 |
| Continuous control / 连续控制 | SAC / TD3 (Phase 9 · 07) | DQN has no policy network. / DQN 没有策略网络。 |
| On-policy / high-throughput / 在线策略/高吞吐 | PPO (Phase 9 · 08) | No replay buffer; easier to scale. / 无回放缓冲区；更易扩展。 |
| Offline RL / 离线 RL | CQL / IQL / Decision Transformer | Conservative Q targets, no bootstrapping blowups. / 保守 Q 目标，无自举爆炸。 |
| Large discrete action spaces (recommender) / 大离散动作空间（推荐） | DQN with action embedding, or IMPALA | Fine; decoration matters. / 可行；细节很重要。 |
| LLM RL / LLM RL | PPO / GRPO | Sequence-level, not step-level; different loss. / 序列级而非步级；不同损失。 |

The lessons still travel. Replay and target networks appear in SAC, TD3, DDPG, SAC-X, AlphaZero's self-play buffer, and every offline RL method. Reward clipping lives on as advantage normalization in PPO. The architecture is the blueprint.

> 这些经验仍然有效。回放和目标网络出现在 SAC、TD3、DDPG、SAC-X、AlphaZero 的自博弈缓冲区和每个离线 RL 方法中。奖励裁剪以 PPO 中的优势归一化形式延续。架构就是蓝图。

## Ship It | 产出物

Save as `outputs/skill-dqn-trainer.md`:

```markdown
---
name: dqn-trainer
description: Produce a DQN training config (buffer, target sync, ε schedule, reward clipping) for a discrete-action RL task.
version: 1.0.0
phase: 9
lesson: 5
tags: [rl, dqn, deep-rl]
---

Given a discrete-action environment (observation shape, action count, horizon, reward scale), output:

1. Network. Architecture (MLP / CNN / Transformer), feature dim, depth.
2. Replay buffer. Capacity, minibatch size, warmup size.
3. Target network. Sync strategy (hard every C steps or soft τ).
4. Exploration. ε start / end / schedule length.
5. Loss. Huber vs MSE, gradient clip value, reward clipping rule.
6. Double DQN. On by default unless explicit reason to disable.

Refuse to ship a DQN with no target network, no replay buffer, or ε held at 1. Refuse continuous-action tasks (route to SAC / TD3). Flag any reward range > 10× per-step mean as needing clipping or scale normalization.
```

## Exercises | 练习题

1. **Easy.** Run `code/main.py`. Plot the per-episode return curve. How many episodes until the running mean exceeds -10?
2. **Medium.** Disable the target network (use the online net for both sides of the Bellman target). Measure training instability — does return oscillate or diverge?
3. **Hard.** Add Double DQN: use the online net to pick `argmax a'`, target net to evaluate. Compare bias of `Q(s_0, best_a)` vs true `V*(s_0)` after 1,000 episodes with vs without Double DQN on a noisy-reward GridWorld.

## Key Terms | 术语速查表

| Term | What people say | What it actually means |
|------|-----------------|-----------------------|
| DQN | "Deep Q-learning" / 深度Q网络 | Q-learning with a neural Q-function, replay buffer, and target network. |
| Experience replay | "Shuffled transitions" / 经验回放 | Ring buffer sampled uniformly each gradient step; decorrelates data. |
| Target network | "Frozen bootstrap" / 目标网络 | Periodic copy of Q used in the Bellman target; stabilizes training. |
| Deadly triad | "Why RL diverges" / 致命三要素 | Function approximation + bootstrapping + off-policy = no convergence guarantee. |
| Double DQN | "Fix for maximization bias" / 双重DQN | Online net selects action, target net evaluates it. |
| Dueling DQN | "V and A heads" / 决斗DQN | Decompose Q = V + A - mean(A); same output, better gradient flow. |
| Rainbow | "All the tricks" / Rainbow | DDQN + PER + dueling + n-step + noisy + distributional in one. |
| PER | "Prioritized Replay" / 优先经验回放 | Sample transitions proportional to TD-error magnitude. |

## Further Reading | 延伸阅读

- [Mnih et al. (2013). Playing Atari with Deep Reinforcement Learning](https://arxiv.org/abs/1312.5602) — the 2013 NeurIPS workshop paper that kicked off deep RL.
- [Mnih et al. (2015). Human-level control through deep reinforcement learning](https://www.nature.com/articles/nature14236) — the Nature paper, 49-game DQN.
- [Hasselt, Guez, Silver (2016). Deep Reinforcement Learning with Double Q-learning](https://arxiv.org/abs/1509.06461) — DDQN.
- [Wang et al. (2016). Dueling Network Architectures](https://arxiv.org/abs/1511.06581) — dueling DQN.
- [Hessel et al. (2018). Rainbow: Combining Improvements in Deep RL](https://arxiv.org/abs/1710.02298) — the stacked-tricks paper.
- [OpenAI Spinning Up — DQN](https://spinningup.openai.com/en/latest/algorithms/dqn.html) — clear modern exposition.
- [Sutton & Barto (2018). Ch. 9 — On-policy Prediction with Approximation](http://incompleteideas.net/book/RLbook2020.pdf) — the textbook treatment of the "deadly triad" (function approximation + bootstrapping + off-policy) that DQN's target network and replay buffer are designed to tame.
- [CleanRL DQN implementation](https://docs.cleanrl.dev/rl-algorithms/dqn/) — reference single-file DQN used in ablation studies; good to read alongside this lesson's from-scratch version.
