# 深度Q网络 (DQN)

> 2013 年：Mnih 在原始像素上训练了一个 Q-learning 网络，在七款 Atari 游戏上击败了所有经典 RL 智能体。2015 年：扩展到 49 款游戏，发表在 Nature 上，开启了深度 RL 时代。DQN 就是 Q-learning 加上三个使函数近似稳定的技巧。

> **【中文解读】** DQN = Q-learning + 神经网络 + 三个稳定化技巧（经验回放、目标网络、奖励裁剪）。2013-2015 年在 Atari 游戏上击败所有经典 RL 方法，开启了深度 RL 时代。这三个技巧至今仍被所有深度 RL 方法使用。

**类型：** 构建
**语言：** Python
**前置知识：** Phase 3 · 03（反向传播），Phase 9 · 04（Q-learning、SARSA）
**用时：** 约 75 分钟

## 问题引入

表格式 Q-learning 需要为每个（状态，动作）对存储一个单独的 Q 值。国际象棋棋盘有约 10⁴³ 个状态。一帧 Atari 画面是 210×160×3 = 100,800 个特征。表格式 RL 在几千个状态时就力不从心了，更别说数十亿。

修复方法事后看很显然：用神经网络替换 Q 表，`Q(s, a; θ)`。但这"事后看显然"花了几十年。朴素的函数近似配合 Q-learning 在"致命三要素"下会发散——函数近似 + 自举 + 离策略学习。Mnih 等人（2013、2015）确定了三个工程技巧来稳定学习：

1. **经验回放 (Experience Replay)** 消除转移之间的相关性。
2. **目标网络 (Target Network)** 冻结自举目标。
3. **奖励裁剪 (Reward Clipping)** 归一化梯度幅度。

Atari 上的 DQN 是第一次用单一架构和单一超参数集从原始像素解决数十个控制问题。此后构建的所有"深度 RL"——DDQN、Rainbow、Dueling、Distributional、R2D2、Agent57——都建立在这三个技巧的基础之上。

> **【中文解读】** "致命三要素"：函数近似 + 自举 + 离策略 → 训练不稳定甚至发散。DQN 的三个技巧解决了这个问题：(1) 经验回放打破时间相关性；(2) 目标网络冻结自举目标；(3) 奖励裁剪归一化梯度。所有后续深度 RL 算法都建立在这三个技巧之上。

> **【拓展：经验回放→RLHF】** 经验回放 (Experience Replay) 的思想在 LLM 训练中无处不在：PPO 训练时的 buffer、RLHF 中的偏好数据集、DPO 的离线数据——本质上都是"打破数据相关性、反复利用经验"。

## 核心概念

![DQN 训练循环：环境、回放缓冲、在线网络、目标网络、Bellman TD 损失](../assets/dqn.svg)

**目标函数。** DQN 在神经 Q 函数上最小化单步 TD 损失：

`L(θ) = E_{(s,a,r,s')~D} [ (r + γ max_{a'} Q(s', a'; θ^-) - Q(s, a; θ))² ]`

`θ` = 在线网络，每步通过梯度下降更新。`θ^-` = 目标网络，定期从 `θ` 复制（约每 10,000 步）。`D` = 存储过去转移的回放缓冲。

**三个技巧，按重要性排序：**

**经验回放。** 一个约 `~10⁶` 个转移的环形缓冲。每个训练步骤随机均匀采样一个小批次。这打破了时间相关性（连续帧几乎相同），让网络可以多次从罕见的奖励转移中学习，并去相关连续的梯度更新。没有它，带神经网络的在线策略 TD 在 Atari 上会发散。

**目标网络。** 在 Bellman 方程两边使用同一网络 `Q(·; θ)` 会使目标每次更新都在移动——"追自己的尾巴"。修复方法：保持第二个网络 `Q(·; θ^-)` 权重冻结。每 `C` 步，复制 `θ → θ^-`。这稳定了回归目标，使其在数千个梯度步内保持不变。软更新 `θ^- ← τ θ + (1-τ) θ^-`（DDPG、SAC 使用）是更平滑的变体。

**奖励裁剪。** Atari 奖励幅度从 1 到 1000+ 不等。裁剪到 `{-1, 0, +1}` 阻止任何单个游戏主导梯度。当奖励幅度有含义时这是错误的；对于只关心符号的 Atari 来说没问题。

**双重 DQN (Double DQN)。** Hasselt (2016) 修复了最大化偏差：用在线网络*选择*动作，用目标网络*评估*它。

`target = r + γ Q(s', argmax_{a'} Q(s', a'; θ); θ^-)`

直接替换，一致更好。默认使用它。

**其他改进（Rainbow, 2017）：** 优先回放（更多采样高 TD 误差的转移）、决斗架构（分离 `V(s)` 和优势头）、噪声网络（学习探索）、n 步回报、分布式 Q（C51/QR-DQN）、多步自举。每项增加几个百分点；收益大致可叠加。

> **【拓展：Rainbow DQN 与集成改进】** Rainbow DQN（2017）将 6 种 DQN 改进集成在一起：优先经验回放、Dueling 架构、噪声网络探索、n 步回报、分布式 Q 学习、多步自举。每种改进贡献几个百分点的性能提升，组合起来效果显著。这种"增量集成"思路在 LLM 训练中也有体现——数据质量、训练策略、架构改进的效果通常是叠加的。

## 动手实现

这里的代码只用标准库，不依赖 numpy——我们使用手写的单隐藏层 MLP 在一个微型连续 GridWorld 上，所以每个训练步骤在微秒级运行。算法与大规模 Atari DQN 完全相同。

### 第 1 步：回放缓冲

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

Atari 上约 50,000 容量；我们的玩具环境 5,000 就够了。

### 第 2 步：微型 Q 网络（手动 MLP）

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

前向传播：线性 → ReLU → 线性。这就是整个网络。

### 第 3 步：DQN 更新

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

形状与第 04 课的 Q-learning 相同，只有两个区别：(a) 我们通过可微的 `Q(·; θ)` 反向传播而非查表，(b) 目标使用 `Q(·; θ^-)`。

### 第 4 步：外循环

每个回合，在 `Q(·; θ)` 上 ε-贪心行动，将转移推入缓冲，采样小批次，进行梯度步，定期同步 `θ^- ← θ`。模式如下：

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

在我们的微型 GridWorld 上使用 16 维独热编码状态，智能体在约 500 个回合内学到接近最优的策略。在 Atari 上，扩展到 2 亿帧并添加 CNN 特征提取器。

## 常见陷阱

- **致命三要素。** 函数近似 + 离策略 + 自举可能发散。DQN 用目标网络 + 回放缓解；不要去掉任何一个。
- **探索。** ε 必须衰减，通常从 1.0 到 0.01 在前约 10% 的训练期间。没有足够的早期探索，Q 网络会收敛到局部盆地。
- **过估计。** 对噪声 Q 取 `max` 向上偏差。生产中始终使用双重 DQN。
- **奖励尺度。** 裁剪或归一化奖励；梯度幅度与奖励幅度成正比。
- **回放缓冲冷启动。** 缓冲有几千个转移前不要训练。在约 20 个样本上的早期梯度会过拟合。
- **目标同步频率。** 太频繁 ≈ 没有目标网络；太不频繁 ≈ 过时目标。Atari DQN 用 10,000 环境步。经验法则：约训练视野的 1/100 同步一次。
- **观测预处理。** Atari DQN 堆叠 4 帧使状态满足马尔可夫性。任何有速度信息的环境需要帧堆叠或循环状态。

## 用框架实现

2026 年，DQN 很少是最先进的，但仍是参考的离策略算法：

| 任务 | 首选方法 | 为什么不用 DQN？ |
|------|----------|-------------------|
| 离散动作 Atari 类 | Rainbow DQN 或 Muesli | 相同框架，更多技巧。 |
| 连续控制 | SAC / TD3（Phase 9 · 07） | DQN 没有策略网络。 |
| 在线策略 / 高吞吐 | PPO（Phase 9 · 08） | 无回放缓冲；更易扩展。 |
| 离线 RL | CQL / IQL / Decision Transformer | 保守 Q 目标，无自举爆炸。 |
| 大离散动作空间（推荐） | 带 action embedding 的 DQN 或 IMPALA | 可行；表示方式重要。 |
| LLM RL | PPO / GRPO | 序列级，非步骤级；不同损失。 |

教训依然传承。回放和目标网络出现在 SAC、TD3、DDPG、SAC-X、AlphaZero 的自博弈缓冲以及每个离线 RL 方法中。奖励裁剪在 PPO 中以优势归一化的形式延续。架构就是蓝图。

## 产出物

保存为 `outputs/skill-dqn-trainer.md`：

```markdown
---
name: dqn-trainer
description: 为离散动作 RL 任务生成 DQN 训练配置（缓冲、目标同步、ε 调度、奖励裁剪）。
version: 1.0.0
phase: 9
lesson: 5
tags: [rl, dqn, deep-rl]
---

给定一个离散动作环境（观测形状、动作数、视野、奖励尺度），输出：

1. 网络。架构（MLP / CNN / Transformer），特征维度，深度。
2. 回放缓冲。容量，小批次大小，预热大小。
3. 目标网络。同步策略（每 C 步硬同步或 τ 软更新）。
4. 探索。ε 起始 / 终止 / 调度长度。
5. 损失。Huber vs MSE，梯度裁剪值，奖励裁剪规则。
6. 双重 DQN。默认开启除非有明确理由禁用。

拒绝发布没有目标网络、没有回放缓冲、或 ε 保持 1 的 DQN。拒绝连续动作任务（引导到 SAC / TD3）。标记任何奖励范围 > 每步均值 10 倍的情况需要裁剪或尺度归一化。
```

## 练习题

1. **简单。** 运行 `code/main.py`。绘制每回合回报曲线。多少回合后运行均值超过 -10？
2. **中等。** 禁用目标网络（Bellman 目标两边都用在线网络）。测量训练不稳定性——回报是否振荡或发散？
3. **困难。** 添加双重 DQN：用在线网络选 `argmax a'`，目标网络评估。在带噪声奖励的 GridWorld 上 1,000 个回合后，比较有和没有双重 DQN 时 `Q(s_0, best_a)` 相对于真实 `V*(s_0)` 的偏差。

## 术语速查表

| 术语 | 通俗说法 | 实际含义 |
|------|----------|----------|
| DQN | "深度 Q-learning" | 带神经网络 Q 函数、回放缓冲和目标网络的 Q-learning。 |
| 经验回放 (Experience Replay) | "打乱的转移" | 每次梯度步均匀采样的环形缓冲；去相关数据。 |
| 目标网络 (Target Network) | "冻结的自举" | Bellman 目标中使用的 Q 的定期副本；稳定训练。 |
| 致命三要素 (Deadly Triad) | "为什么 RL 发散" | 函数近似 + 自举 + 离策略 = 无收敛保证。 |
| 双重 DQN (Double DQN) | "修复最大化偏差" | 在线网络选择动作，目标网络评估它。 |
| 决斗 DQN (Dueling DQN) | "V 和 A 头" | 分解 Q = V + A - mean(A)；相同输出，更好的梯度流。 |
| Rainbow | "所有技巧" | DDQN + PER + 决斗 + n 步 + 噪声 + 分布式合一。 |
| 优先经验回放 (PER) | "优先回放" | 按 TD 误差幅度成比例采样转移。 |

## 延伸阅读

- [Mnih et al. (2013). Playing Atari with Deep Reinforcement Learning](https://arxiv.org/abs/1312.5602) — 2013 年 NeurIPS 工坊论文，开启深度 RL。
- [Mnih et al. (2015). Human-level control through deep reinforcement learning](https://www.nature.com/articles/nature14236) — Nature 论文，49 游戏 DQN。
- [Hasselt, Guez, Silver (2016). Deep Reinforcement Learning with Double Q-learning](https://arxiv.org/abs/1509.06461) — DDQN。
- [Wang et al. (2016). Dueling Network Architectures](https://arxiv.org/abs/1511.06581) — 决斗 DQN。
- [Hessel et al. (2018). Rainbow: Combining Improvements in Deep RL](https://arxiv.org/abs/1710.02298) — 叠加技巧论文。
- [OpenAI Spinning Up — DQN](https://spinningup.openai.com/en/latest/algorithms/dqn.html) — 清晰的现代讲解。
- [Sutton & Barto (2018). Ch. 9 — On-policy Prediction with Approximation](http://incompleteideas.net/book/RLbook2020.pdf) — 教科书对"致命三要素"（函数近似 + 自举 + 离策略）的处理，DQN 的目标网络和回放缓冲正是为了驯服它。
- [CleanRL DQN implementation](https://docs.cleanrl.dev/rl-algorithms/dqn/) — 消融研究中使用的参考单文件 DQN；适合与本课从头实现的版本对照阅读。
