# 近端策略优化 (PPO)

> A2C 每次更新后丢弃展开数据。PPO 用裁剪的重要性比率包裹策略梯度，使同一批数据可以做 10+ 轮更新而策略不会爆炸。Schulman 等人（2017）。仍是 2026 年默认的策略梯度算法。

> **【中文解读】** PPO 用裁剪的重要性比率包裹策略梯度，使同一批数据可以做 10+ 轮更新而策略不会爆炸。2017 年提出，至今仍是 2026 年默认的策略梯度算法。

> **【拓展：PPO 与 ChatGPT】** PPO 是 ChatGPT RLHF 训练的核心算法。InstructGPT（2022）使用 PPO 对 GPT-3 进行人类偏好对齐，这就是 ChatGPT 背后的技术。PPO 的稳定性和简单性使其成为工业界首选。

**类型：** 构建
**语言：** Python
**前置知识：** Phase 9 · 06（REINFORCE），Phase 9 · 07（Actor-Critic）
**用时：** 约 75 分钟

## 问题引入

A2C（第 07 课）是在线策略的：梯度 `E_{π_θ}[A · ∇ log π_θ]` 要求从*当前* `π_θ` 采样的数据。做一次更新，`π_θ` 变化；你使用的数据现在变成了离策略。重复使用它会让梯度有偏差。

展开数据是昂贵的。在 Atari 上，8 个环境 × 128 步 = 1,024 个转移和十几秒的环境时间。一次梯度步后就丢弃太浪费了。

信赖域策略优化 (Trust Region Policy Optimization, TRPO, Schulman 2015) 是第一个修复：约束每次更新使新旧策略之间的 KL 散度保持在 `δ` 以下。理论上干净，但每次更新需要共轭梯度求解。2026 年没有人运行 TRPO。

PPO（Schulman 等人 2017）用简单的裁剪目标替换了硬信赖域约束。多一行代码。每次展开十个轮次。无需共轭梯度。足够好的理论保证。九年后，它仍然是从 MuJoCo 到 RLHF 所有场景的默认策略梯度算法。

> **【中文解读】** PPO 的核心创新：用裁剪目标替代 TRPO 的硬约束。重要性比率 r_t(theta) = pi_theta / pi_old 被裁剪到 [1-epsilon, 1+epsilon] 范围内。当优势 A_t>0 时，不将好动作的概率推得太高；当 A_t<0 时，不将坏动作的概率降得太低。只需一行代码，就能安全地多次复用同一批数据。

> **【拓展：PPO 之外的选择——DPO 与 GRPO】** 虽然 PPO 仍是 2026 年的默认选择，但替代方案正在兴起。DPO（Direct Preference Optimization）跳过奖励模型，直接从偏好对训练策略，更简单但灵活性较低。GRPO（Group Relative Policy Optimization，DeepSeek-R1 使用）用组内采样均值替代 critic 基线，消除了 value head 的需求。

## 核心概念

![PPO 裁剪代理目标：比率在 1 ± ε 处裁剪](../assets/ppo.svg)

**重要性比率。**

`r_t(θ) = π_θ(a_t | s_t) / π_{θ_old}(a_t | s_t)`

这是新策略与收集数据策略的似然比。`r_t = 1` 表示无变化。`r_t = 2` 表示新策略采取 `a_t` 的可能性是旧策略的两倍。

**裁剪代理。**

`L^{CLIP}(θ) = E_t [ min( r_t(θ) A_t, clip(r_t(θ), 1-ε, 1+ε) A_t ) ]`

两项：

- 如果优势 `A_t > 0` 且比率试图增长超过 `1 + ε`，裁剪使梯度变平——不要将好动作推到旧概率之上 `+ε` 以外。
- 如果优势 `A_t < 0` 且比率试图增长超过 `1 - ε`（意味着我们可能使坏动作比其被裁剪的减少更有可能），裁剪限制梯度——不要将坏动作推到 `-ε` 以下。

`min` 处理另一个方向：如果比率已经在*有利*方向移动，你仍然得到梯度（不会在对你不利的一侧裁剪）。

典型的 `ε = 0.2`。将目标绘制为 `r_t` 的函数：一个分段线性函数，在"好侧"有平顶，在"坏侧"有平底。

> **【中文解读】** PPO 裁剪机制的直觉：epsilon=0.2 意味着策略每次更新最多改变 20%。如果某个动作很好（A>0），最多将概率提升 20%；如果某个动作很差（A<0），最多降低 20%。这防止了"灾难性遗忘"——策略不会一步变化太大。

**完整 PPO 损失。**

`L(θ, φ) = L^{CLIP}(θ) - c_v · (V_φ(s_t) - V_t^{target})² + c_e · H(π_θ(·|s_t))`

与 A2C 相同的 Actor-Critic 结构。三个系数，通常 `c_v = 0.5`、`c_e = 0.01`、`ε = 0.2`。

**训练循环。**

1. 在 `N` 个并行环境中各收集 `T` 步，共 `N × T` 个转移。
2. 计算优势（GAE），冻结为常数。
3. 冻结 `π_{θ_old}` 作为当前 `π_θ` 的快照。
4. 对 `K` 个轮次，对每个 `(s, a, A, V_target, log π_old(a|s))` 的小批次：
   - 计算 `r_t(θ) = exp(log π_θ(a|s) - log π_old(a|s))`。
   - 应用 `L^{CLIP}` + 值损失 + 熵。
   - 梯度步。
5. 丢弃展开数据。回到第 1 步。

`K = 10` 和 64 的小批次是标准超参数集。PPO 鲁棒：在 ±50% 范围内精确数字很少重要。

**KL 惩罚变体。** 原始论文提出了使用自适应 KL 惩罚的替代方案：`L = L^{PG} - β · KL(π_θ || π_old)`，`β` 根据观测 KL 调整。裁剪版本成为主导；KL 变体在 RLHF 中延续（其中到参考策略的 KL 是你始终需要的独立约束）。

## 动手实现

### 第 1 步：在展开时捕获 `log π_old(a | s)`

```python
for step in range(T):
    probs = softmax(logits(theta, state_features(s)))
    a = sample(probs, rng)
    s_next, r, done = env.step(s, a)
    buffer.append({
        "s": s, "a": a, "r": r, "done": done,
        "v_old": value(w, state_features(s)),
        "log_pi_old": log(probs[a] + 1e-12),
    })
    s = s_next
```

快照在展开时拍摄一次。在更新轮次期间不会改变。

### 第 2 步：计算 GAE 优势（第 07 课）

与 A2C 相同。跨批次归一化。

### 第 3 步：裁剪代理更新

```python
for _ in range(K_EPOCHS):
    for mb in minibatches(buffer, size=64):
        for rec in mb:
            x = state_features(rec["s"])
            probs = softmax(logits(theta, x))
            logp = log(probs[rec["a"]] + 1e-12)
            ratio = exp(logp - rec["log_pi_old"])
            adv = rec["advantage"]
            surrogate = min(
                ratio * adv,
                clamp(ratio, 1 - EPS, 1 + EPS) * adv,
            )
            # 反向传播 -surrogate，加值损失，减熵
            grad_logpi = onehot(rec["a"]) - probs
            if (adv > 0 and ratio >= 1 + EPS) or (adv < 0 and ratio <= 1 - EPS):
                pg_grad = 0.0  # 被裁剪
            else:
                pg_grad = ratio * adv
            for i in range(N_ACTIONS):
                for j in range(N_FEAT):
                    theta[i][j] += LR * pg_grad * grad_logpi[i] * x[j]
```

"裁剪 → 零梯度"模式是 PPO 的核心。如果新策略已经在有利方向漂移太远，更新停止。

### 第 4 步：值和熵

对评论家目标添加标准 MSE，对演员添加熵奖励，与 A2C 相同。

### 第 5 步：诊断

每次更新需要监控三件事：

- **平均 KL** `E[log π_old - log π_θ]`。应保持在 `[0, 0.02]`。如果冲过 `0.1`，减小 `K_EPOCHS` 或 `LR`。
- **裁剪比例** — 比率落在 `[1-ε, 1+ε]` 之外的样本比例。应为 `~0.1-0.3`。如果 `~0`，裁剪从未触发 → 提高 `LR` 或 `K_EPOCHS`。如果 `~0.5+`，你过拟合展开 → 降低它们。
- **解释方差** `1 - Var(V_target - V_pred) / Var(V_target)`。评论家质量指标。应随着评论家学习趋近 1。

## 常见陷阱

- **裁剪系数调错。** `ε = 0.2` 是事实标准。改为 `0.1` 使更新太保守；`0.3+` 引入不稳定。
- **太多轮次。** `K > 20` 经常导致不稳定，因为策略漂移远离 `π_old`。限制轮次，特别是对大型网络。
- **没有奖励归一化。** 大奖励尺度侵蚀裁剪范围。在计算优势之前归一化奖励（运行标准差）。
- **忘记优势归一化。** 每批次零均值/单位标准差归一化是标准做法。跳过它会在大多数基准上破坏 PPO。
- **学习率未衰减。** PPO 受益于线性 LR 衰减到零。常数 LR 通常更差。
- **重要性比率数学错误。** 始终用 `exp(log_new - log_old)` 保证数值稳定性，而非 `new / old`。
- **梯度符号错误。** 最大化代理 = *最小化* `-L^{CLIP}`。符号翻转是最常见的 PPO bug。

## 用框架实现

PPO 是 2026 年跨多个领域的默认 RL 算法：

| 用例 | PPO 变体 |
|------|----------|
| MuJoCo / 机器人控制 | 带高斯策略的 PPO，GAE(0.95) |
| Atari / 离散游戏 | 带分类策略的 PPO，滚动 128 步展开 |
| LLM 的 RLHF | 带 KL 惩罚到参考模型的 PPO，回复结束时来自 RM 的奖励 |
| 大规模游戏智能体 | IMPALA + PPO（AlphaStar、OpenAI Five） |
| 推理 LLM | GRPO（第 12 课）— 无评论家的 PPO 变体 |
| 仅偏好数据 | DPO — PPO+KL 的闭式坍缩，无在线采样 |

PPO 的*损失形状*——裁剪代理 + 值 + 熵——是 DPO、GRPO 和几乎所有 RLHF 管线的脚手架。

## 产出物

保存为 `outputs/skill-ppo-trainer.md`：

```markdown
---
name: ppo-trainer
description: 为给定环境生成 PPO 训练配置和诊断计划。
version: 1.0.0
phase: 9
lesson: 8
tags: [rl, ppo, policy-gradient]
---

给定环境和训练预算，输出：

1. 展开大小。`N` 个环境 × `T` 步。
2. 更新调度。`K` 轮次，小批次大小，LR 调度。
3. 代理参数。`ε`（裁剪）、`c_v`、`c_e`，开启优势归一化。
4. 优势。GAE(`λ`)，显式 `γ` 和 `λ`。
5. 诊断计划。KL、裁剪比例、解释方差阈值及警报。

拒绝 K > 30 或 ε > 0.3（不安全的信赖域）。拒绝没有优势归一化或 KL/裁剪监控的 PPO 运行。标记裁剪比例持续高于 0.4 为漂移。
```

## 练习题

1. **简单。** 在 4×4 GridWorld 上用 `ε=0.2, K=4` 运行 PPO。与 A2C（每次展开一个轮次）在匹配环境步数下比较样本效率。
2. **中等。** 扫描 `K ∈ {1, 4, 10, 30}`。绘制回报 vs 环境步数并追踪每次更新的平均 KL。在什么 `K` 时 KL 在这个任务上爆炸？
3. **困难。** 用自适应 KL 惩罚替换裁剪代理（`KL > 2·target` 时 `β` 翻倍，`KL < target/2` 时减半）。比较最终回报、稳定性和无裁剪程度。

## 术语速查表

| 术语 | 通俗说法 | 实际含义 |
|------|----------|----------|
| 重要性比率 | "r_t(θ)" | `π_θ(a\|s) / π_old(a\|s)`；偏离收集数据的策略的程度。 |
| 裁剪代理 | "PPO 的主要技巧" | `min(r·A, clip(r, 1-ε, 1+ε)·A)`；有利侧超过裁剪值后梯度为零。 |
| 信赖域 | "TRPO / PPO 的意图" | 限制每次更新的 KL 以保证单调改进。 |
| KL 惩罚 | "软信赖域" | 替代 PPO：`L - β · KL(π_θ \|\| π_old)`。自适应 `β`。 |
| 裁剪比例 | "裁剪触发频率" | 诊断——应为 0.1-0.3；超出表示参数不当。 |
| 多轮训练 | "数据复用" | 每次展开 K 轮；以方差代价换取样本效率。 |
| 准在线策略 | "大部分在线策略" | PPO 名义上是在线策略的，但 K>1 轮次安全地使用了略偏策略的数据。 |
| PPO-KL | "另一个 PPO" | KL 惩罚变体；用于 KL-到-参考已是约束的 RLHF。 |

## 延伸阅读

- [Schulman et al. (2017). Proximal Policy Optimization Algorithms](https://arxiv.org/abs/1707.06347) — 论文。
- [Schulman et al. (2015). Trust Region Policy Optimization](https://arxiv.org/abs/1502.05477) — TRPO，PPO 的前身。
- [Andrychowicz et al. (2021). What Matters In On-Policy RL? A Large-Scale Empirical Study](https://arxiv.org/abs/2006.05990) — 每个 PPO 超参数的消融。
- [Ouyang et al. (2022). Training language models to follow instructions with human feedback](https://arxiv.org/abs/2203.02155) — InstructGPT；RLHF 中的 PPO 配方。
- [OpenAI Spinning Up — PPO](https://spinningup.openai.com/en/latest/algorithms/ppo.html) — 带 PyTorch 的清晰现代讲解。
- [CleanRL PPO implementation](https://github.com/vwxyzjn/cleanrl) — 多篇论文使用的参考单文件 PPO。
- [Hugging Face TRL — PPOTrainer](https://huggingface.co/docs/trl/main/en/ppo_trainer) — 语言模型上 PPO 的生产配方；配合第 09 课（RLHF）阅读。
- [Engstrom et al. (2020). Implementation Matters in Deep Policy Gradients](https://arxiv.org/abs/2005.12729) — "37 个代码级优化"论文；哪些 PPO 技巧是承重的，哪些是传说。
