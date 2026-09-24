# 的Q网络

> 2013年:Mnih在原始像素上训练了一种Q学习网络,在七款Atari游戏中击败了每一个经典RL代理. 2015年:扩展到49个游戏,发表在Nature上,引发了深度RL时代.DQN是Q学习加上三个技巧,使函数近似稳定.

> **【中文解读】**语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语

**Type:** Build | **类型:** 动手
**Languages:** Python | **语言:** Python
**Prerequisites:** Phase 3 · 03 (Backpropagation), Phase 9 · 04 (Q-learning, SARSA) | **前置知识:** Phase 3 · 03 (反向传播), Phase 9 · 04 (Q-learning, SARSA)
**Time:** ~75 minutes | **时间:** ~75 分钟

## 问题 问题引入

图表 Q-学习需要每个 (状态,行动) 双的单独Q-值.棋牌板上有1043个状态.阿塔利框架为210×160×3 =100800个特征.图表 RL在数千个状态中死亡,更不用说数十亿.

> 表格Q学习 需要为每一个状态,动作) 对单独存储一个Q值.一个国际象棋盘有约1043个状态.一个Atari 有210×160×3=100,800.

后面看来,解决方案很明显:用神经网络取代Q表,`Q(s, a; θ)`,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,

> 后面的解决方案很简单:使用神经网络`Q(s, a; θ)`换成Q表.但这个"简单"花了几十年. 简单的函数近似与Q学习. 在"致命三要素"下会发散函数近似+自举+离策略学习.

1. **Experience replay**调整过渡.
   **经验回放**打破转移的时间相关性.
2. **Target network**结了启动线的目标.
   **目标网络**结自举目标.
3. **Reward clipping**降梯度的强度正常化.
   **奖励裁剪**归化梯度量级.

亚塔利的DQN是唯一一个架构的首次,一个单一的超参数组解决了数十个控制问题.从 DDQN,彩虹,双斗,分销,R2D2,Agent57 以来构建的所有"深度RL"都堆叠在这个三招基础上.

> 亚太里上 DQN 是第一次使用单一架构和单一超参数集从原始像素来解决数十个控制问题.

> **【中文解读】**"致命三要素":函数近似 + 自举 + 离策略 → 训练不稳定甚至发散――DQN的三个技巧解决了这个问题:

> **【拓展：经验回放→RLHF】**经验回放 (经验重播) 的思想在LLM训练中无处不在:PPO训练时的缓冲,RLHF中偏好数据集,DPO的离线数据本质上是"打破数据相关性"",反复利用经验".

## 概念的核心概念

![DQN training loop: env, replay buffer, online net, target net, Bellman TD loss](../assets/dqn.svg)

**The objective.**通过 DQN 降低神经 Q 函数的单步 TD 损失:

`L(θ) = E_{(s,a,r,s')~D} [ (r + γ max_{a'} Q(s', a'; θ^-) - Q(s, a; θ))² ]`

`θ`网络,每一步都会随着梯度下降更新.`θ^-`网址: 网址: 网址: 网址: 网址:`θ`它们的位置是很小的.`D`= 过去的过渡的重播缓冲器.

> **目标。**子 损失 子 损失 子 损失 子 损失 子 损失 子 损失 子 损失 子 损失 子 损失 子 损失 子 损失 子 损失 子 损失 子 损失 子 损失 子 损失 子 损失 子 损失 子 损失 子 损失 子 损失 子 子 子 子 子 子 子 子 子 子 子 子 子 子 子 子 子 子 子 子 子 子 子 子 子 子 子 子 子 子 子 子 子 子 子 子 子 子 子 子 子 子 子`θ`通过梯度下降更新.`θ^-`目标网络,定期从`θ`复制 约每1万步)`D`过去转移的回放缓冲区──

**The three tricks, in order of importance:**

> **三个技巧，按重要性排序：**

**Experience replay.**的环保器`~10⁶`通过此,网络可以从罕见的有益转型中学习,并将连续的梯度更新进行调整.没有它,在政策上,TD与神经网络分离在Atari上.

> **经验回放。**一个转移环形缓冲区约106次. 每次训练步骤随机均采用小批次. 这打破了时间相关性.

**Target network.**通过同一个网络`Q(·; θ)`通过Bellman方程的两侧,目标每次更新都会移动 "追逐自己的尾巴".`Q(·; θ^-)`结的重量.`C`步骤,复制`θ → θ^-`这使得反归目标稳定,`θ^- ← τ θ + (1-τ) θ^-`(用于DDPG,SAC) 是一个更平滑的变体.

> **目标网络。**在贝尔曼方程的两侧使用相同的网络会使目标每次更新都在移动"追逐自己的尾巴"──修复方法:保留一个权重结的第二网络──每次更新都在移动"追逐自己的尾巴".`C`步复制`θ → θ^-`〔软更新〕DDPG、SAC 中使用) 更平滑的变体──

**Reward clipping.**亚塔利奖励大小从1到1000+之间.`{-1, 0, +1}`错误的是奖励大小重要,但Atari只需要签字.

> **奖励裁剪。**亚太里奖励量级从1到1000+不等.`{-1, 0, +1}`防止任何单个游戏主导层次.

**Double DQN.**哈塞尔特 (2016) 修复了最大化偏见:使用在线网络来*选择*行动,目标网络来*评估*它.

`target = r + γ Q(s', argmax_{a'} Q(s', a'; θ); θ^-)`

随时更好,默认使用.

> **双重 DQN。**哈塞尔特 (2016) 修复最大化偏差:用在线网络*选择*动作,用目标网络*评估*它──直接替换,始终更好──默认使用──

**Other improvements (Rainbow, 2017):**优先重播 (样本高TD错误过渡更多),对决架构 (分开 `V(s)`它们的数量和优势是多少? 它们的数量和优势是多少?

> **其他改进（Rainbow, 2017）：**优先回放、决斗架构、噪声网络、n 步回报、分布式Q、多步自举──每种改进贡献几百分点;收益大致可叠加──

> **【拓展：Rainbow DQN 与集成改进】**彩虹DQN(2017) 将将6种DQN改进集成在一起:优先经验回放、双重架构、噪声网络探索、n 步回报、分布式Q学习、多步自举举──每种改进贡献几百分点的性能提升,组合效果显著――这种"增量集成"思路在LLM训练中也存在数据质量、训练策略、结构改进的效果通常是叠加的──

## 建立它,实现它.
```figure
f3-dqn-stability
```

## 建立它

我们使用一个手动滚动的单层隐藏MLP在一个微小的连续 GridWorld,所以每个训练步骤运行在微秒.算法是相同的阿塔利DQN规模.

> 这里的代码仅使用标准库在一个微型连续 GridWorld 上使用手写的单隐藏层MLP──算法与大规模的Atari DQN完全相同──

### 步骤1:重播缓冲器

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

对于阿塔利的容量大约为5万,

> 亚太里需要5万个容量,我们的玩具环境5000个就够了.

### 步骤2:一个小的Q网络 (手动MLP)

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

线性 → 线性 → 线性.

> 前向传播:线性 → ReLU → 线性――这就是整个网络――

### 步骤3:DQN更新

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

形状是从04课程中学习Q,有两个区别:`Q(·; θ)`目标使用的方法`Q(·; θ^-)`现在,我们要去.

> 形式与第04课程的Q学习相似,但有两个区别:`Q(·; θ)`反向传播而非索引表格,`Q(·; θ^-)`,我知道.

### 步骤4:外环

对于每一集,都做一个贪的行为.`Q(·; θ)`按,按,按,按,按,按,按,按.`θ^- ← θ`模式:

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

在我们的小小的GridWorld中,有16维的单热状态,代理在500集中学习了近乎最佳的政策.在Atari上,将这扩大到200万个框架,并添加一个CNN特色提取器.

> 在我们使用16维一热状态的微型网格世界上,智能体在约500回合内学到接近最优的策略. 在亚太里上,扩展到200亿并添加CNN特征提取器.

## 陷

- **Deadly triad.**函数近似+非政策+启动可能会分歧.DQN通过目标网+重播减轻;不要删除任何一个.
  **致命三要素。**函数近似+离策略+自举可能发散――DQN 通过目标网络+回放缓解;不要移除任何一个――
- **Exploration.**由于网的度较高,而网的度较高,所以网的度较高.
  **探索。**必须减弱,通常从1.0到0.01,覆盖前10%的训练.没有足够的早期探索,Q 网络会收到局部盆.
- **Overestimation.** `max`总是使用双DQN在生产中.
  **过估计。**对于有噪音的Q 取`max`两重DQN的生产总决使用.
- **Reward scale.**剪辑或正常化奖励;梯度大小与奖励大小相对.
  **奖励尺度。**裁剪或归纳奖励;梯度级与奖励级的正比.
- **Replay buffer coldstart.**在缓冲器有几千次过渡之前不要训练.
  **回放缓冲区冷启动。**缓冲区有几千次转移后再训练.
- **Target sync frequency.**太频繁 ≈ 没有目标网;太少 ≈ 过时目标. 雅塔利 DQN 使用10,000个env步骤. 指规则:每1/100个训练视野同步.
  **目标同步频率。**太频繁≈没有目标网络;太不频繁≈过时目标――经验法则:每约1/100 训练视野同步一次――
- **Observation preprocessing.**任何具有速度信息的环境都需要框架堆或复发状态.
  **观测预处理。**利DQN 堆叠4 使状态满足可行性利任何有速度信息的环境都需要叠或循环状态利

## 用它实现框架

在2026年,DQN很少是最先进的,但仍然是参考的非政策算法:

> 2026年,DQN 很少是最先进的,但仍然是离策略算法的参考:

| Task | Method of choice | Why not DQN? |
|------|------------------|--------------|
| Task / 任务 | Method of choice / 首选方法 | Why not DQN? / 为什么不用 DQN？ |
| Discrete-action Atari-like / 离散动作类 Atari | Rainbow DQN or Muesli | Same framework, more tricks. / 相同框架，更多技巧。 |
| Continuous control / 连续控制 | SAC / TD3 (Phase 9 · 07) | DQN has no policy network. / DQN 没有策略网络。 |
| On-policy / high-throughput / 在线策略/高吞吐 | PPO (Phase 9 · 08) | No replay buffer; easier to scale. / 无回放缓冲区；更易扩展。 |
| Offline RL / 离线 RL | CQL / IQL / Decision Transformer | Conservative Q targets, no bootstrapping blowups. / 保守 Q 目标，无自举爆炸。 |
| Large discrete action spaces (recommender) / 大离散动作空间（推荐） | DQN with action embedding, or IMPALA | Fine; decoration matters. / 可行；细节很重要。 |
| LLM RL / LLM RL | PPO / GRPO | Sequence-level, not step-level; different loss. / 序列级而非步级；不同损失。 |

课程仍然在进行.重播和目标网络出现在SAC,TD3,DDPG,SAC-X,AlphaZero的自动播放缓冲器和每个离线RL方法中.奖励剪辑作为PPO中的优势正常化继续存在.架构是蓝图.

> 这些经验仍然有效. 回放和目标网络现在出现在SAC、TD3、DDPG、SAC-X、AlphaZero的自发缓冲区和每个离线RL方法中.

## 运送它.

保存如`outputs/skill-dqn-trainer.md`其他:

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

## 练习题

1. **Easy.**跑步`code/main.py`运行平均值超过 -10之前,多少集?
2. **Medium.**禁用目标网络 (使用网络网络对贝尔曼目标的两侧). 测量训练不稳定性?
3. **Hard.**添加双DQN:使用网上网来选择`argmax a'`分析,分析,分析,分析,分析,分析,分析,分析,分析,分析,分析,分析,分析,分析,分析,分析,分析,分析,分析,分析,分析,分析,分析,分析,分析,分析,分析,分析,分析,分析,分析,分析,分析,分析,分析,分析,分析,分析,分析,分析,分析,分析,分析,分析,分析,分析,分析,分析,分析,分析,分析,分析,分析,分析,分析,分析,分析,分析,分析,分析,分析,分析,分析,分析,分析,分析,分析,分析,分析,分析,分析,分析,分析,分析,分析,分析,分析,分析,分析,分析,分析,分析,分析,分析,分析,分析,分析,分析,分析,分析,分析,分析,分析,分析,分析,分析,分析,分析,分析,分析,分析,分析,分析,分析,分析,分析,分析,分析,分析,分析,分析,分析,分析,分析,分析,分析,分析,分析,分析,分析,分析,分析,分析,分析,分析,分析,分析,分析,分析,分析,分析,分析,分析,分析,分析,分析,分析,分析,分析,分析,分析,分析,分析,分析,分析,分析,分析,分析,分析,分析,分析,分析,`Q(s_0, best_a)`实际情况`V*(s_0)`在一个杂的奖励格里德世界上,

## 关键词 快速查找表

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

## 继续阅读 继续阅读

- [Mnih et al. (2013). Playing Atari with Deep Reinforcement Learning](https://arxiv.org/abs/1312.5602)2013年"NeurIPS"研讨会论文,
- [Mnih et al. (2015). Human-level control through deep reinforcement learning](https://www.nature.com/articles/nature14236)"自然"论文,49场DQN.
- [Hasselt, Guez, Silver (2016). Deep Reinforcement Learning with Double Q-learning](https://arxiv.org/abs/1509.06461) DDQN
- [Wang et al. (2016). Dueling Network Architectures](https://arxiv.org/abs/1511.06581)     
- [Hessel et al. (2018). Rainbow: Combining Improvements in Deep RL](https://arxiv.org/abs/1710.02298)堆的刺纸.
- [OpenAI Spinning Up — DQN](https://spinningup.openai.com/en/latest/algorithms/dqn.html)清晰的现代化展示.
- [Sutton & Barto (2018). Ch. 9 — On-policy Prediction with Approximation](http://incompleteideas.net/book/RLbook2020.pdf)教科书处理"致命三位一体" (函数接近+启动+非政策) 目标网络和DQN的重播缓冲器旨在制.
- [CleanRL DQN implementation](https://docs.cleanrl.dev/rl-algorithms/dqn/)用于除研究的参考单档DQN;好在此课程的从头开始版本旁边阅读.
