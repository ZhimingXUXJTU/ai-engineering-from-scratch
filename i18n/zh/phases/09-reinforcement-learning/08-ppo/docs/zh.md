# 通过"近端策略优化"

> 根据APP的数据,PPO将政策梯度缩小到一个重要的比例,以便在不爆发的政策的情况下,您可以在同一数据上进行10+个时代.

> **【中文解读】**通过PPO使用切割的重要性比率包裹策略梯度,使同一批数据能够进行10+轮更新而策略不会爆炸.

> **【拓展：PPO 与 ChatGPT】**博是ChatGPT RLHF 训练的核心算法. 博是GPT-3对人类偏好进行PPO的核心算法.

**Type:** Build | **类型:** 动手
**Languages:** Python | **语言:** Python
**Prerequisites:** Phase 9 · 06 (REINFORCE), Phase 9 · 07 (Actor-Critic) | **前置知识:** Phase 9 · 06 (REINFORCE), Phase 9 · 07 (Actor-Critic)
**Time:** ~75 minutes | **时间:** ~75 分钟

## 问题 问题引入

向 (课07),是政策的`E_{π_θ}[A · ∇ log π_θ]`需要从*流量*中采集的数据`π_θ`接下来,我们要做一个更新,`π_θ`您使用的数据现在是非政策的. 再利用它,你的偏差偏差.

> ,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,`E_{π_θ}[A · ∇ log π_θ]`要求从*当前* `π_θ`采样数据.`π_θ`改变;你使用的数据就变成了战略.

在Atari上,一个8个Envs × 128 步骤的推出 = 1024 个转型和十几秒钟的环境时间.在一个梯度步骤后抛弃它是浪费的.

> 在亚太里上,8个环境 × 128 步 = 1024 次转移和几秒钟的环境时间.

首先,我们必须限制每次更新,`δ`理论上是清洁的,但每次更新需要一个结合分数解决.

> 据悉,这项新战略的发展将在2015年开始.`δ`理论上优雅,但每次更新都需要共度求解.

根据PPO (Schulman et al. 2017) 的规定,硬信任区域的限制被简单的剪切目标所取代.一个额外的代码线.每次推出的十个时代.没有结合梯度.足够的理论保障.九年后,它仍然是从MuJoCo到RLHF的默认政策梯度算法.

> 根据PPO的简单剪辑目标,它仍然是从MuJoCo到RLHF的所有任务的默认策略梯度算法――

> **【中文解读】**核心创新:用剪切目标替代TRPO的硬约束――重要性比率r_t(theta) = pi_theta / pi_old 被剪切到 [1-epsilon, 1+epsilon] 范围内――当优势A_t>0时,不将好动作的概率推得太高;当A_t<0时,不将坏动作的概率降低太低――需要一行代码,就能安全地多次复制相同的数据批量――

> **【拓展：PPO 之外的选择——DPO 与 GRPO】**虽然PPO仍然是2026年的默认选择,但替代方案正在兴起.DPO (直接偏好优化) 跳过奖励模型,直接从偏好对训练策略,更简单但灵活性较低.GRPO (Group Relative Policy Optimization,DeepSeek-R1 使用) 消除了价值头脑的需求.

## 概念的核心概念

![PPO clipped surrogate objective: ratio clipping at 1 ± ε](../assets/ppo.svg)

**The importance ratio.**

`r_t(θ) = π_θ(a_t | s_t) / π_{θ_old}(a_t | s_t)`

这就是新政策与收集数据的政策的概率比率. `r_t = 1`没有变化.`r_t = 2`这意味着新政策的可能性是两倍`a_t`像以前一样.

> **重要性比率。**新策略与数据收集策略的相似性.`r_t = 1`表示没有变化.`r_t = 2`表明采取新策略`a_t`可能性是旧策略的两倍.

**The clipped surrogate.**

`L^{CLIP}(θ) = E_t [ min( r_t(θ) A_t, clip(r_t(θ), 1-ε, 1+ε) A_t ) ]`

两条条条款:

- 如果优势`A_t > 0`现在,这个比例试图扩大.`1 + ε`不推出一个好的行动更远`+ε`超过了旧的可能性.
- 如果优势`A_t < 0`现在,这个比例试图扩大.`1 - ε`片罩梯度 不推下一个坏动作 `-ε`现在,我们要去.

其他`min`处理另一方向:如果比率移动到*有益*方向,你仍然得到梯度 (没有侧面剪辑会伤害你).

典型的`ε = 0.2`绘制目标作为函数`r_t`部分直线功能,"好面"有一个平面的屋顶,"坏面"一个平面的地板.

> **裁剪代理。**两项:如果优势为正确且比率超过`1 + ε`切割,使梯度变平,不要把好动作推高于旧概率.`+ε`更多──如果优势为负率低于`1 - ε`切割限制梯度,不要把坏动作降低.`-ε`更多──典型`ε = 0.2`,我知道.

> **【中文解读】**剪切机制直觉:epsilon=0.2 意思是策略每次更新最多变化20%──如果某一动作很好 ((A>0),最多将增加20%;如果某一动作很差 ((A<0),最多将降低20%──这防止"灾难性遗忘"策略不会变得太大.

**The full PPO loss.**

`L(θ, φ) = L^{CLIP}(θ) - c_v · (V_φ(s_t) - V_t^{target})² + c_e · H(π_θ(·|s_t))`

平均水平为3个系数,通常是`c_v = 0.5`现在`c_e = 0.01`现在`ε = 0.2`现在,我们要去.

> **完整的 PPO 损失。**与A2C相似的演员评论结构──三系数,通常`c_v = 0.5`,我知道.`c_e = 0.01`,我知道.`ε = 0.2`,我知道.

**The training loop.**

1. 收集`N × T`跨境的过渡`N`对于平行环境`T`每一步都在做.
2. 计算优势 (GAE),将它们作为常数结结.
3. 结`π_{θ_old}`作为目前的快照`π_θ`现在,我们要去.
4. 为了`K`对于每一批小批量,`(s, a, A, V_target, log π_old(a|s))`其他:
   - 计算`r_t(θ) = exp(log π_θ(a|s) - log π_old(a|s))`现在,我们要去.
   - 申请`L^{CLIP}`它们的价值损失
   - 渐进步骤.
5. 放弃部署,回到第一步.

`K = 10`率强度:确切数量很少在 ± 50% 范围内.

> **训练循环。**收集 → 计算 GAE 优势 → 结旧策略 → K轮更新 → 丢弃数据──`K = 10`和 64 的小批次是标准超参数──PPO 非常棒:具体数值在 ±50% 内通常无关紧要──

**KL-penalty variant.**原稿提出了使用适应性KL罚款的替代方案: `L = L^{PG} - β · KL(π_θ || π_old)`随着`β`根据观察到的KL调整.剪辑版本成为主导性;KL变体在RLHF中存活 (KL对参考政策是你总是想要的单独的限制).

> **KL 惩罚变体。**原始论文提出了使用自适应KL的替代方案. 剪辑版本成为主流.

## 建立它,实现它.
```figure
ppo-clip
```

## 建立它

### 步骤1: 捕获`log π_old(a | s)`在推出时

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

快照一次拍摄,在推出时,它不会在更新时代发生变化.

> 快照在推出时拍摄一次.

### 步骤2:计算GAE的优势 (07课)

像A2C一样,在整个批量中正常化.

> 与A2C相同.

### 步骤3:切断替代更新

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
            # backprop -surrogate, add value loss, subtract entropy
            grad_logpi = onehot(rec["a"]) - probs
            if (adv > 0 and ratio >= 1 + EPS) or (adv < 0 and ratio <= 1 - EPS):
                pg_grad = 0.0  # clipped
            else:
                pg_grad = ratio * adv
            for i in range(N_ACTIONS):
                for j in range(N_FEAT):
                    theta[i][j] += LR * pg_grad * grad_logpi[i] * x[j]
```

如果新政策已经过于偏向有利方向,更新就会停止.

> 裁剪 →零梯度模式是PPO的核心. 如果新策略在有利方向上偏向太远,更新就停止.

### 步骤4:价值和缩

加入标准的MSE到批评目标和对演员的透奖励,与A2C相同.

> 对于演员来说, 增加奖励, 与 A2C 相似.

### 步骤5:诊断

每次更新都需要看三个东西:

> 每次更新都需要监控的三个事情:

- **Mean KL** `E[log π_old - log π_θ]`应该留在里面.`[0, 0.02]`如果它过去`0.1`减少`K_EPOCHS`或`LR`现在,我们要去.
  **平均 KL。**应保持在`[0, 0.02]`如果超过`0.1`减少`K_EPOCHS`或`LR`,我知道.
- **Clip fraction** 占外面比例的样本比例`[1-ε, 1+ε]`应该是`~0.1-0.3`如果`~0`片从来没有触发的升`LR`或`K_EPOCHS`如果`~0.5+`现在,你把它们放下.
  **裁剪比例。**比率超出`[1-ε, 1+ε]`样本比例.`~0.1-0.3`,我知道.
- **Explained variance** `1 - Var(V_target - V_pred) / Var(V_target)`评论家学习时,应该朝1.
  **解释方差。**批判性质量指标――应随着批判性学习趋向1――

## 陷

- **Clip coefficient mistuned.** `ε = 0.2`实际上,我们将会使用`0.1`让更新变得太尬;`0.3+`造成不稳定.
  **裁剪系数调错。** `ε = 0.2`是事实标准.`0.1`太保守;`0.3+`导致不稳定.
- **Too many epochs.** `K > 20`由于政策偏离了`π_old`限制时代,尤其是对于大型网络.
  **太多 epoch。** `K > 20`常常不稳定,因为策略偏离`π_old`太远――限制时代,特别是大网络――
- **No reward normalization.**运行的奖励 (STD) 在计算优势之前,将奖励正常化.
  **没有奖励归一化。**大奖励尺度侵蚀剪切范围――计算优势前归归化奖励――
- **Forgetting advantage normalization.**平均零/单位STD正常化是标准的. 跳过它,在大多数基准上会破坏PPO.
  **忘记优势归一化。**每批零平均值/单位标准差归纳是标准的.
- **Learning rate not decayed.**由于线性LR衰退到零,PPO受益.
  **学习率未衰减。**常数 LR 通常更差──
- **Importance ratio math errors.**总是`exp(log_new - log_old)`对于数值稳定性而言,不`new / old`现在,我们要去.
  **重要性比率数学错误。**始终使用`exp(log_new - log_old)`保证数值稳定性而不是`new / old`,我知道.
- **Wrong gradient sign.**增加代孕的可能性.`-L^{CLIP}`翻转标志是最常见的PPO虫.
  **梯度符号错误。**最大化代理 = * 最小化* `-L^{CLIP}`符号反转为 PPO 最常见的错误

## 用它实现框架

据了解,

> 预测是2026年众多领域的默认RL算法:

| Use case | PPO variant |
|----------|-------------|
| Use case / 用例 | PPO variant / PPO 变体 |
| MuJoCo / robotics control / MuJoCo/机器人控制 | PPO with Gaussian policy, GAE(0.95) / 高斯策略的 PPO，GAE(0.95) |
| Atari / discrete games / Atari/离散游戏 | PPO with categorical policy, rolling 128-step rollouts / 分类策略的 PPO |
| RLHF for LLMs / LLM 的 RLHF | PPO with KL penalty to reference model, reward from RM at end of response / 带 KL 惩罚的 PPO |
| Large-scale game agents / 大规模游戏 Agent | IMPALA + PPO (AlphaStar, OpenAI Five) |
| Reasoning LLMs / 推理 LLM | GRPO (Lesson 12) — PPO variant without critic / 无 Critic 的 PPO 变体 |
| Preference-only data / 仅偏好数据 | DPO — closed-form collapsing of PPO+KL, no online sampling / 闭式 PPO+KL 折叠 |

切割替代+值+入力是DPO,GRPO和几乎每个RLHF管道的架构.

> 剪代理 + 值 + 是DPO、GRPO 和几乎所有RLHF流水线的脚手架──

## 运送它.

保存如`outputs/skill-ppo-trainer.md`其他:

```markdown
---
name: ppo-trainer
description: Produce a PPO training config and a diagnostic plan for a given environment.
version: 1.0.0
phase: 9
lesson: 8
tags: [rl, ppo, policy-gradient]
---

Given an environment and training budget, output:

1. Rollout size. `N` envs × `T` steps.
2. Update schedule. `K` epochs, minibatch size, LR schedule.
3. Surrogate params. `ε` (clip), `c_v`, `c_e`, advantage normalization on.
4. Advantage. GAE(`λ`) with explicit `γ` and `λ`.
5. Diagnostics plan. KL, clip fraction, explained variance thresholds with alerts.

Refuse `K > 30` or `ε > 0.3` (unsafe trust region). Refuse any PPO run without advantage normalization or KL/clip monitoring. Flag clip fraction sustained above 0.4 as drift.
```

## 练习题

1. **Easy.**在4×4格里德世界上运行PPO`ε=0.2, K=4`通过相对环境步骤,比较样品效率与A2C (每次推出一次)
2. **Medium.**扫描`K ∈ {1, 4, 10, 30}`节点返回与环境步骤,跟踪平均KL每次更新.`K`这项任务是否会爆炸?
3. **Hard.**取代切割的替代母体用适应性 KL罚款 (`β`如果`KL > 2·target`半个如果`KL < target/2`) 比较最终回报,稳定性和无剪辑性.

## 关键词 快速查找表

| Term | What people say | What it actually means |
|------|-----------------|-----------------------|
| Importance ratio | "r_t(θ)" | `π_θ(a\|s) / π_old(a\|s)`; deviation from the policy that collected the data. |
| Clipped surrogate | "PPO's main trick" | `min(r·A, clip(r, 1-ε, 1+ε)·A)`; flat gradient past the clip on beneficial side. |
| Trust region | "TRPO / PPO intent" | Limit each update's KL to guarantee monotone improvement. |
| KL penalty | "Soft trust region" | Alternative PPO: `L - β · KL(π_θ \|\| π_old)`. Adaptive `β`. |
| Clip fraction | "How often clipping triggers" | Diagnostic — should be 0.1-0.3; outside means mistuned. |
| Multi-epoch training | "Data reuse" | K epochs on each rollout; variance cost traded for sample efficiency. |
| On-policy-ish | "Mostly on-policy" | PPO is nominally on-policy but K>1 epochs uses slightly-off-policy data safely. |
| PPO-KL | "The other PPO" | KL-penalty variant; used in RLHF where KL-to-reference is already a constraint. |

## 继续阅读 继续阅读

- [Schulman et al. (2017). Proximal Policy Optimization Algorithms](https://arxiv.org/abs/1707.06347)报纸.
- [Schulman et al. (2015). Trust Region Policy Optimization](https://arxiv.org/abs/1502.05477)TRPO,是PPO的前任.
- [Andrychowicz et al. (2021). What Matters In On-Policy RL? A Large-Scale Empirical Study](https://arxiv.org/abs/2006.05990)每一个PPO超参数都被取消.
- [Ouyang et al. (2022). Training language models to follow instructions with human feedback](https://arxiv.org/abs/2203.02155) 导读GPT;PPO-in-RLHF配方.
- [OpenAI Spinning Up — PPO](https://spinningup.openai.com/en/latest/algorithms/ppo.html)使用 PyTorch 清洁现代化展览.
- [CleanRL PPO implementation](https://github.com/vwxyzjn/cleanrl)许多论文所使用的单档PPO参考.
- [Hugging Face TRL — PPOTrainer](https://huggingface.co/docs/trl/main/en/ppo_trainer)语言模型的PPO生产配方;阅读与第09课 (RLHF) 一起.
- [Engstrom et al. (2020). Implementation Matters in Deep Policy Gradients](https://arxiv.org/abs/2005.12729)"37代码级优化"论文;哪些PPO技巧承载负载,哪些是民间故事.
