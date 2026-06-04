# 游戏中的强化学习 — AlphaZero、MuZero 与 LLM 推理时代

> 1992 年：TD-Gammon 用纯 TD 在双陆棋上击败人类冠军。2016 年：AlphaGo 击败李世乭。2017 年：AlphaZero 从零开始称霸国际象棋、将棋和围棋。2024 年：DeepSeek-R1 证明了相同配方，用 GRPO 替换 PPO，也适用于推理。游戏是驱动本阶段每个突破的基准。

> **【中文解读】** 游戏是 RL 突破的试验场：TD-Gammon (1992) → AlphaGo (2016) → AlphaZero (2017) → DeepSeek-R1 (2025)。DeepSeek-R1 证明了 AlphaZero 的"自我博弈+搜索+策略改进"循环可以直接用于大模型的数学推理——token 就是动作，验证器就是"赢/输"信号。

**类型：** 构建
**语言：** Python
**前置知识：** Phase 9 · 05（DQN），Phase 9 · 08（PPO），Phase 9 · 09（RLHF），Phase 9 · 10（MARL）
**用时：** 约 120 分钟

## 问题引入

游戏拥有 RL 想要的一切。干净的奖励（赢/输）。无限的回合（自我博弈可重置）。完美的仿真（游戏*就是*仿真器）。离散或小的连续动作空间。迫使对抗鲁棒性的多智能体结构。

游戏是每个重大 RL 突破的测试场。TD-Gammon（双陆棋，1992）。Atari-DQN（2013）。AlphaGo（2016）。AlphaZero（2017）。OpenAI Five（Dota 2，2019）。AlphaStar（星际争霸 II，2019）。MuZero（学习模型，2019）。AlphaTensor（矩阵乘法，2022）。AlphaDev（排序算法，2023）。DeepSeek-R1（数学推理，2025）——最新的展示，证明游戏 RL 技术也适用于文本。

这个总结课程通过统一视角——**自我博弈 + 搜索 + 策略改进**——纵览三个里程碑架构：AlphaZero、MuZero 和 GRPO。每个都是前一个的推广；特别是 GRPO 就是 AlphaZero 的配方应用于 LLM 推理，以 token 为动作，以数学验证为胜负信号。

## 核心概念

![AlphaZero ↔ MuZero ↔ GRPO：相同循环，不同环境](../assets/rl-games.svg)

**统一循环。**

```
while True:
    trajectory = self_play(current_policy, search)     # 与自己对战
    policy_target = search.improved_policy(trajectory) # 搜索改进原始策略
    policy_net.update(policy_target, value_target)     # 在搜索输出上监督学习
```

**AlphaZero (2017)。** Silver 等人。给定一个已知规则的游戏（国际象棋、将棋、围棋）：

- 策略-值网络：一个塔 `f_θ(s) → (p, v)`。`p` 是合法走法的先验分布。`v` 是期望游戏结果。
- 蒙特卡洛树搜索 (MCTS)：每步走棋时，展开可能后续的树。使用 `(p, v)` 作为先验 + 自举。通过 UCB (PUCT) 选择节点：`a* = argmax Q(s, a) + c · p(a|s) · √N(s) / (1 + N(s, a))`。
- 自我博弈：智能体 vs 智能体对弈。在第 `t` 步，MCTS 访问分布 `π_t` 成为策略训练目标。
- 损失：`L = (v - z)² - π · log p + c · ||θ||²`。`z` 是游戏结果（+1 / 0 / -1）。

零人类知识。零手工启发式。单个配方在数千万自我博弈后分别掌握了国际象棋、将棋和围棋。

**MuZero (2019)。** Schrittwieser 等人。去除了规则已知的假设。

- 不使用固定环境，而是学习*隐空间动力学模型* `(h, g, f)`：
  - `h(s)`：将观测编码到隐状态。
  - `g(s_latent, a)`：预测下一隐状态 + 奖励。
  - `f(s_latent)`：预测策略先验 + 值。
- MCTS 在*学习的隐空间*中运行。相同的搜索，相同的训练循环。
- 适用于围棋、国际象棋、将棋*以及* Atari——一个算法，无需规则知识。

> **【中文解读】** AlphaZero 和 MuZero 的核心循环：自我博弈 → MCTS 搜索改进策略 → 监督学习更新网络。AlphaZero 需要已知游戏规则，MuZero 通过学习隐空间动力学模型消除了这个限制。这个"自我博弈+搜索+策略改进"循环直接启发了 DeepSeek-R1 的推理训练——用可验证奖励替代游戏胜负信号。

> **【拓展：DeepSeek-R1 与 AlphaZero 范式】** DeepSeek-R1（2025）将 AlphaZero 的范式应用于 LLM 推理：token 就是动作，推理过程就是"游戏"，验证器（数学题对错、代码是否通过测试）就是"胜负信号"。GRPO 替代 PPO，组内采样替代自我博弈。这验证了游戏 AI 的方法论可以迁移到大模型推理训练。

**随机 MuZero (Stochastic MuZero, 2022)。** 添加随机动力学和机会节点；扩展到双陆棋类游戏。

**Muesli、Gumbel MuZero (2022-2024)。** 在样本效率和确定性搜索方面的改进。

**GRPO (2024-2025)。** DeepSeek-R1 配方。相同 AlphaZero 形状的循环，应用于语言模型推理：

- "游戏"：回答数学 / 编程 / 推理问题。"赢" = 验证器（测试用例通过、数值答案匹配）返回 1。
- 策略：LLM。动作：token。状态：提示 + 目前回复。
- 无评论家（PPO 风格的 V_φ）。替代方案：对每个提示，从策略采样 `G` 个补全。计算每个的奖励。使用**组相对优势** `A_i = (r_i - mean_r) / std_r` 作为 REINFORCE 风格更新的信号。
- 到参考策略的 KL 惩罚以防止漂移（类似 RLHF）。
- 完整损失：

  `L_GRPO(θ) = -E_{q, {o_i}} [ (1/G) Σ_i A_i · log π_θ(o_i | q) ] + β · KL(π_θ || π_ref)`

无奖励模型，无评论家，无 MCTS。组相对基线替代了这三个。在推理基准上以几分之一的计算匹配或超越 PPO-RLHF 质量。

> **【中文解读】** GRPO 是 DeepSeek-R1 的核心创新：不需要 critic 网络（省一半内存），用组内均值和标准差构造优势。对每个问题采样 G 个回答，正确回答的优势为正（增强概率），错误的为负（降低概率）。这是"没有 critic 的 PPO"，是 2025 年大模型推理训练最重要的算法突破。

> **【拓展：GRPO→DeepSeek-R1→开源推理革命】** DeepSeek-R1 的四阶段训练流程：冷启动 SFT → 推理导向 GRPO → 拒绝采样+SFT → 全谱 GRPO。R1-Zero（纯 GRPO 无 SFT）证明了 LLM 可以从零学会推理，但输出可读性差。蒸馏实验表明：用强 RL 教师的推理轨迹做 SFT，比小模型从头做 RL 效果更好。

**R1 完整配方。** DeepSeek-R1（DeepSeek 2025）是一篇论文中的两个模型：

- **R1-Zero。** 从 DeepSeek-V3 基础模型开始。无 SFT。直接应用 GRPO，使用两个奖励组件：*准确度奖励*（基于规则——最终答案是否解析为正确数字 / 代码是否通过单元测试）和*格式奖励*（补全是否用 `思考…输出` 标签包裹了思维链）。数千步后，平均回复长度从约 100 增长到约 10,000 个 token，数学基准分数攀升到接近 o1-preview 水平。模型从零学会了推理。缺点：其思维链通常不可读，混合语言，缺乏文体润色。
- **R1。** 通过四阶段管线修复 R1-Zero 的可读性问题：
  1. **冷启动 SFT。** 收集几千条格式整洁的长 CoT 示范。在其上对基础模型做监督微调。这给出了可读的起点。
  2. **推理导向 GRPO。** 应用 GRPO，使用准确度+格式奖励加*语言一致性*奖励防止语码切换。
  3. **拒绝采样 + SFT 第 2 轮。** 从 RL 检查点采样约 60 万条推理轨迹，只保留最终答案正确且 CoT 可读的，与约 20 万条非推理 SFT 示例（写作、问答、自我认知）组合。再次微调基础模型。
  4. **全谱 GRPO。** 再做一轮 RL，同时覆盖推理（基于规则的奖励）和通用对齐（有用性/无害性基于偏好的奖励）。

结果在 AIME 和 MATH-500 上匹配 o1，且以开放权重发布，足够小以至于可以蒸馏。同一论文还发布了六个蒸馏密集模型（Qwen-1.5B 到 Llama-70B），通过在 R1 的推理轨迹上做 SFT——学生在学生规模上不做 RL。强 RL 教师的蒸馏始终优于学生规模从零做 RL。

**为什么 GRPO 而非 PPO 用于推理。** DeepSeekMath 论文（2024 年 2 月）给出三个理由：(1) 无需训练值网络，内存减半；(2) 组基线天然处理推理任务产生的稀疏回合末奖励；(3) 逐提示归一化使不同难度的题目间优势可比，而 PPO 的单一评论家做不到。

**无搜索 vs 基于搜索。** 游戏已分化：

- *长视野完全信息博弈*（围棋、国际象棋）：仍然基于搜索。AlphaZero / MuZero 占主导。
- *LLM 推理*：生产中还没有 MCTS；GRPO 在完整展开上做，Best-of-N 用于推理计算。过程奖励模型 (PRM) 暗示步骤级搜索可能被加回来。

## 动手实现

`code/main.py` 中的代码实现了**微型 GRPO**——一个带多组样本的多臂赌博机。算法与 LLM 上的相同；只是策略和环境更简单。它教授*损失*和*组相对优势*，这是 2025 年的创新。

### 第 1 步：微型验证器环境

```python
QUESTIONS = [
    {"prompt": "q1", "correct": 3},
    {"prompt": "q2", "correct": 1},
]

def verify(prompt_idx, answer_token):
    return 1.0 if answer_token == QUESTIONS[prompt_idx]["correct"] else 0.0
```

在真实 GRPO 中，验证器运行单元测试或检查数学等式。

### 第 2 步：策略：每个提示的 K 个答案 token 上的 softmax

```python
def policy_probs(theta, p_idx):
    return softmax(theta[p_idx])
```

等价于以提示为条件的 LLM 最终层输出。

### 第 3 步：组采样和组相对优势

```python
def grpo_step(theta, p_idx, G=8, beta=0.01, lr=0.1, rng=None):
    probs = policy_probs(theta, p_idx)
    samples = [sample(probs, rng) for _ in range(G)]
    rewards = [verify(p_idx, s) for s in samples]
    mean_r = sum(rewards) / G
    std_r = stddev(rewards) + 1e-8
    advs = [(r - mean_r) / std_r for r in rewards]

    for a, A in zip(samples, advs):
        grad = onehot(a) - probs
        for i in range(len(probs)):
            theta[p_idx][i] += lr * A * grad[i]
    # KL 惩罚：将 theta 拉向参考
    for i in range(len(probs)):
        theta[p_idx][i] -= beta * (theta[p_idx][i] - reference[p_idx][i])
```

组相对优势是 2024 年 DeepSeek 的技巧。不需要评论家。"基线"是组均值，归一化使用组标准差。

### 第 4 步：与 REINFORCE 基线（无值函数）对比

相同设置，相同计算，朴素 REINFORCE。GRPO 收敛更快更稳定。

### 第 5 步：观察熵和 KL

与 RLHF 相同的诊断：到参考的平均 KL、策略熵、奖励随时间变化。一旦这些稳定，训练就完成了。

## 常见陷阱

- **通过验证器博弈的奖励黑客行为。** GRPO 继承了 RLHF 的风险：如果验证器有错或可利用，LLM 会找到利用方式。健壮的验证器（多个测试用例、形式化证明）很重要。
- **组大小太小。** 组基线的方差与 `1/√G` 成正比。低于 `G = 4` 时，优势信号噪声大；标准选择是 `G = 8` 到 `64`。
- **长度偏差。** 不同长度的 LLM 补全有不同的对数概率。按 token 数归一化，或使用序列级对数概率，或截断到最大长度。
- **纯自我博弈循环。** AlphaZero 风格训练在一般和博弈上可能陷入支配循环。通过多样对手池缓解（联盟训练，第 10 课）。
- **搜索-策略不匹配。** AlphaZero 训练策略以模仿搜索输出。如果策略网络太小无法表示搜索的分布，训练停滞。
- **计算下限。** MuZero / AlphaZero 需要大量计算。单次消融通常是数百 GPU 小时。存在微型演示（如 AlphaZero on Connect Four）供学习用。
- **验证器覆盖。** 对有 bug 的解决方案通过的单元测试会强化 bug。设计能捕获边缘情况的验证器。

## 用框架实现

2026 年游戏 RL 格局，按领域：

| 领域 | 主导方法 |
|------|----------|
| 双人零和棋盘游戏（围棋、国际象棋、将棋） | AlphaZero / MuZero / KataGo |
| 不完全信息纸牌游戏（扑克） | CFR + 深度学习（DeepStack、Libratus、Pluribus） |
| Atari / 像素游戏 | Muesli / MuZero / IMPALA-PPO |
| 大型多人策略（Dota、星际争霸） | PPO + 自我博弈 + 联盟（OpenAI Five、AlphaStar） |
| LLM 数学/代码推理 | GRPO（DeepSeek-R1、Qwen-RL、开源复现） |
| LLM 对齐 | DPO / RLHF-PPO（非 GRPO；验证器是偏好而非可验证的） |
| 机器人 | PPO + DR（非游戏 RL，但使用相同策略梯度工具） |
| 组合问题 | AlphaZero 变体（AlphaTensor、AlphaDev） |

*配方*——自我博弈、搜索增强的改进、策略蒸馏——横跨文本、像素和物理控制。GRPO 是最新的实例；更多即将到来。

## 产出物

保存为 `outputs/skill-game-rl-designer.md`：

```markdown
---
name: game-rl-designer
description: 为给定领域设计游戏 RL 或推理 RL 训练管线（AlphaZero / MuZero / GRPO）。
version: 1.0.0
phase: 9
lesson: 12
tags: [rl, alphazero, muzero, grpo, self-play]
---

给定目标（完全信息博弈 / 不完全信息 / Atari / LLM 推理 / 组合问题），输出：

1. 环境适配。规则已知？马尔可夫？随机？多智能体？决定 AlphaZero vs MuZero vs GRPO。
2. 搜索策略。MCTS（带学习先验的 PUCT）、Gumbel 采样、Best-of-N、或无。
3. 自我博弈计划。对称自我博弈 / 联盟 / 离线数据 / 验证器生成。
4. 目标信号。游戏结果 / 验证器奖励 / 偏好 / 学习模型。包含鲁棒性计划。
5. 诊断。相对基线的胜率、ELO 曲线、验证器通过率、到参考的 KL。

拒绝在不完全信息博弈上使用 AlphaZero（引导到 CFR）。拒绝没有可信验证器的 GRPO。拒绝任何没有固定基线对手集的游戏 RL 管线（否则自我博弈 ELO 未校准）。
```

## 练习题

1. **简单。** 在 `code/main.py` 中实现 GRPO 赌博机。在 2 个提示 × 4 个答案 token 上训练。`G=8` 时在 < 1,000 次更新内收敛。
2. **中等。** 接入 PPO（裁剪）和朴素 REINFORCE。在相同赌博机上与 GRPO 比较样本效率和奖励方差。
3. **困难。** 扩展到长度为 2 的"推理链"：智能体发射两个 token，验证器对 pair 给奖励。测量 GRPO 如何处理两步序列的信用分配。（提示：按*完整序列*计算组优势，传播到两个 token 位置。）

## 术语速查表

| 术语 | 通俗说法 | 实际含义 |
|------|----------|----------|
| MCTS | "带学习网络的树搜索" | 蒙特卡洛树搜索；UCB1/PUCT 选择带学习的 `(p, v)` 先验。 |
| AlphaZero | "自我博弈 + MCTS" | 策略-值网络训练以匹配 MCTS 访问和游戏结果。 |
| MuZero | "学习模型的 AlphaZero" | 相同循环但在隐空间中通过学习的动力学。 |
| GRPO | "无评论家的 PPO" | 组相对策略优化；带组均值基线 + KL 的 REINFORCE。 |
| PUCT | "AlphaZero 的 UCB" | `Q + c · p · √N / (1 + N_a)` — 平衡值估计与先验。 |
| 自我博弈 | "智能体 vs 过去的自己" | 零和博弈的标准；对称训练信号。 |
| 联盟训练 | "基于种群的自我博弈" | 过去 + 当前 + 剥削者被采样为对手。 |
| 验证器奖励 | "可验证 RL" | 奖励来自确定性检查器（测试通过、答案匹配）。 |
| 过程奖励 | "PRM" | 对每个推理步骤评分，而非仅最终答案。 |

## 延伸阅读

- [Silver et al. (2017). Mastering the game of Go without human knowledge (AlphaGo Zero)](https://www.nature.com/articles/nature24270)。
- [Silver et al. (2018). A general reinforcement learning algorithm that masters chess, shogi, and Go through self-play (AlphaZero)](https://www.science.org/doi/10.1126/science.aar6404)。
- [Schrittwieser et al. (2020). Mastering Atari, Go, chess and shogi by planning with a learned model (MuZero)](https://www.nature.com/articles/s41586-020-03051-4)。
- [Vinyals et al. (2019). Grandmaster level in StarCraft II (AlphaStar)](https://www.nature.com/articles/s41586-019-1724-z)。
- [DeepSeek-AI (2024). DeepSeekMath: Pushing the Limits of Mathematical Reasoning in Open Language Models (GRPO)](https://arxiv.org/abs/2402.03300) — 引入 GRPO 和组相对基线的论文。
- [DeepSeek-AI (2025). DeepSeek-R1: Incentivizing Reasoning Capability in LLMs via Reinforcement Learning](https://arxiv.org/abs/2501.12948) — 完整的四阶段 R1 配方加上 R1-Zero 消融实验。
- [Brown et al. (2019). Superhuman AI for multiplayer poker (Pluribus)](https://www.science.org/doi/10.1126/science.aay2400) — 大规模 CFR + 深度学习。
- [Tesauro (1995). Temporal Difference Learning and TD-Gammon](https://dl.acm.org/doi/10.1145/203330.203343) — 开创一切的论文。
- [Hugging Face TRL — GRPOTrainer](https://huggingface.co/docs/trl/main/en/grpo_trainer) — 应用带自定义奖励函数 GRPO 的生产参考。
- [Qwen Team (2024). Qwen2.5-Math — GRPO replication](https://github.com/QwenLM/Qwen2.5-Math) — 多规模 R1 配方的开源复现。
- [Sutton & Barto (2018). Ch. 17 — Frontiers of Reinforcement Learning](http://incompleteideas.net/book/RLbook2020.pdf) — 教科书对自我博弈、搜索和"设计奖励"的框架，R1 在 LLM 规模上实现了它。
