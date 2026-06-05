# Proximal Policy Optimization (PPO) | 近端策略优化

> A2C throws away each rollout after one update. PPO wraps the policy gradient in a clipped importance ratio so you can do 10+ epochs on the same data without the policy exploding. Schulman et al. (2017). Still the default policy-gradient algorithm in 2026.

> **【中文解读】** PPO 用裁剪的重要性比率包裹策略梯度，使同一批数据可以做 10+ 轮更新而策略不会爆炸。2017 年提出，至今仍是 2026 年默认的策略梯度算法。

> **【拓展：PPO 与 ChatGPT】** PPO 是 ChatGPT RLHF 训练的核心算法。InstructGPT（2022）使用 PPO 对 GPT-3 进行人类偏好对齐，这就是 ChatGPT 背后的技术。PPO 的稳定性和简单性使其成为工业界首选。

**Type:** Build
**Languages:** Python
**Prerequisites:** Phase 9 · 06 (REINFORCE), Phase 9 · 07 (Actor-Critic)
**Time:** ~75 minutes

## The Problem | 问题引入

A2C (Lesson 07) is on-policy: the gradient `E_{π_θ}[A · ∇ log π_θ]` requires data sampled from the *current* `π_θ`. Take one update, and `π_θ` changes; the data you used is now off-policy. Re-use it and your gradient is biased.

> A2C（Lesson 07）是在线策略的：梯度 `E_{π_θ}[A · ∇ log π_θ]` 要求从*当前* `π_θ` 采样的数据。一次更新后 `π_θ` 改变；你用过的数据就变成了离策略。复用它梯度就有偏差。

Rollouts are expensive. On Atari, one rollout across 8 envs × 128 steps = 1024 transitions and a dozen seconds of environment time. Throwing that away after one gradient step is wasteful.

> Rollout 很昂贵。在 Atari 上，8 个环境 × 128 步 = 1024 次转移和十几秒的环境时间。一次梯度步后就丢弃太浪费了。

Trust Region Policy Optimization (TRPO, Schulman 2015) was the first fix: constrain each update so the KL divergence between old and new policy stays below `δ`. Theoretically clean, but requires a conjugate-gradient solve per update. Nobody runs TRPO in 2026.

> 信赖域策略优化（TRPO，Schulman 2015）是第一个修复：约束每次更新使新旧策略的 KL 散度保持在 `δ` 以下。理论上优雅，但每次更新需要共轭梯度求解。2026 年没人运行 TRPO。

PPO (Schulman et al. 2017) replaces the hard trust-region constraint with a simple clipped objective. One extra line of code. Ten epochs per rollout. No conjugate gradients. Good-enough theoretical guarantees. Nine years later it is still the default policy-gradient algorithm for everything from MuJoCo to RLHF.

> PPO（Schulman 等人 2017）用简单的裁剪目标替代硬信赖域约束。多一行代码。每个 rollout 十个 epoch。不需要共轭梯度。足够好的理论保证。九年后它仍然是从 MuJoCo 到 RLHF 所有任务的默认策略梯度算法。

> **【中文解读】** PPO 的核心创新：用裁剪目标替代 TRPO 的硬约束。重要性比率 r_t(theta) = pi_theta / pi_old 被裁剪到 [1-epsilon, 1+epsilon] 范围内。当优势 A_t>0 时，不将好动作的概率推得太高；当 A_t<0 时，不将坏动作的概率降得太低。只需一行代码，就能安全地多次复用同一批数据。

> **【拓展：PPO 之外的选择——DPO 与 GRPO】** 虽然 PPO 仍是 2026 年的默认选择，但替代方案正在兴起。DPO（Direct Preference Optimization）跳过奖励模型，直接从偏好对训练策略，更简单但灵活性较低。GRPO（Group Relative Policy Optimization，DeepSeek-R1 使用）用组内采样均值替代 critic 基线，消除了 value head 的需求。

## The Concept | 核心概念

![PPO clipped surrogate objective: ratio clipping at 1 ± ε](../assets/ppo.svg)

**The importance ratio.**

`r_t(θ) = π_θ(a_t | s_t) / π_{θ_old}(a_t | s_t)`

This is the likelihood ratio of the new policy vs the policy that collected the data. `r_t = 1` means no change. `r_t = 2` means the new policy is twice as likely to take `a_t` as the old.

> **重要性比率。** 新策略与收集数据策略的似然比。`r_t = 1` 表示没有变化。`r_t = 2` 表示新策略采取 `a_t` 的可能性是旧策略的两倍。

**The clipped surrogate.**

`L^{CLIP}(θ) = E_t [ min( r_t(θ) A_t, clip(r_t(θ), 1-ε, 1+ε) A_t ) ]`

Two terms:

- If the advantage `A_t > 0` and the ratio tries to grow past `1 + ε`, the clip flattens the gradient — don't push a good action further than `+ε` above old probability.
- If the advantage `A_t < 0` and the ratio tries to grow past `1 - ε` (meaning we would make a bad action more likely compared to its clipped reduction), the clip caps the gradient — don't push a bad action below `-ε`.

The `min` handles the other direction: if the ratio has moved in the *beneficial* direction, you still get the gradient (no clipping on the side that would hurt you).

Typical `ε = 0.2`. Plot the objective as a function of `r_t`: a piecewise-linear function with a flat roof on the "good side" and a flat floor on the "bad side."

> **裁剪代理。** 两项：如果优势为正且比率超过 `1 + ε`，裁剪使梯度变平——不要把好动作推得比旧概率高 `+ε` 更多。如果优势为负且比率低于 `1 - ε`，裁剪限制梯度——不要把坏动作降得比 `-ε` 更多。典型 `ε = 0.2`。

> **【中文解读】** PPO 裁剪机制的直觉：epsilon=0.2 意味着策略每次更新最多改变 20%。如果某个动作很好（A>0），最多将概率提升 20%；如果某个动作很差（A<0），最多降低 20%。这防止了"灾难性遗忘"——策略不会一步变化太大。

**The full PPO loss.**

`L(θ, φ) = L^{CLIP}(θ) - c_v · (V_φ(s_t) - V_t^{target})² + c_e · H(π_θ(·|s_t))`

Same actor-critic structure as A2C. Three coefficients, usually `c_v = 0.5`, `c_e = 0.01`, `ε = 0.2`.

> **完整的 PPO 损失。** 与 A2C 相同的 Actor-Critic 结构。三个系数，通常 `c_v = 0.5`、`c_e = 0.01`、`ε = 0.2`。

**The training loop.**

1. Collect `N × T` transitions across `N` parallel envs for `T` steps each.
2. Compute advantages (GAE), freeze them as constants.
3. Freeze `π_{θ_old}` as a snapshot of current `π_θ`.
4. For `K` epochs, for each minibatch of `(s, a, A, V_target, log π_old(a|s))`:
   - Compute `r_t(θ) = exp(log π_θ(a|s) - log π_old(a|s))`.
   - Apply `L^{CLIP}` + value loss + entropy.
   - Gradient step.
5. Discard the rollout. Return to step 1.

`K = 10` and minibatches of 64 is a standard hyperparameter set. PPO is robust: the exact numbers rarely matter within ±50%.

> **训练循环。** 收集 → 计算 GAE 优势 → 冻结旧策略 → K 轮更新 → 丢弃数据。`K = 10` 和 64 的小批次是标准超参数。PPO 非常鲁棒：具体数值在 ±50% 内通常无关紧要。

**KL-penalty variant.** The original paper proposed an alternative using an adaptive KL penalty: `L = L^{PG} - β · KL(π_θ || π_old)` with `β` adjusted based on observed KL. The clipping version became dominant; the KL variant survives in RLHF (where KL to the reference policy is a separate constraint you always want anyway).

> **KL 惩罚变体。** 原始论文提出了使用自适应 KL 惩罚的替代方案。裁剪版本成为主流；KL 变体在 RLHF 中存续（那里 KL 到参考策略是你始终想要的独立约束）。

## Build It | 动手实现

### Step 1: capture `log π_old(a | s)` at rollout time

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

The snapshot is taken once, at rollout time. It does not change during the update epochs.

> 快照在 rollout 时拍摄一次。在更新 epoch 期间不变。

### Step 2: compute GAE advantages (Lesson 07)

Same as A2C. Normalize across the batch.

> 与 A2C 相同。跨批次归一化。

### Step 3: clipped surrogate update

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

The "clipped → zero gradient" pattern is the heart of PPO. If the new policy has already drifted too far in the beneficial direction, the update stops.

> "裁剪 → 零梯度"模式是 PPO 的核心。如果新策略在有利方向上已经偏移太远，更新就停止。

### Step 4: value and entropy

Add standard MSE to the critic target and an entropy bonus on the actor, same as A2C.

> 向 critic 目标添加标准 MSE，向 actor 添加熵奖励，与 A2C 相同。

### Step 5: diagnostics

Three things to watch every update:

> 每次更新要监控的三件事：

- **Mean KL** `E[log π_old - log π_θ]`. Should stay in `[0, 0.02]`. If it blows past `0.1`, reduce `K_EPOCHS` or `LR`.
  **平均 KL。** 应保持在 `[0, 0.02]`。如果超过 `0.1`，减少 `K_EPOCHS` 或 `LR`。
- **Clip fraction** — the fraction of samples whose ratio lies outside `[1-ε, 1+ε]`. Should be `~0.1-0.3`. If `~0`, the clip never triggers → raise `LR` or `K_EPOCHS`. If `~0.5+`, you are over-fitting the rollout → lower them.
  **裁剪比例。** 比率超出 `[1-ε, 1+ε]` 的样本比例。应为 `~0.1-0.3`。
- **Explained variance** `1 - Var(V_target - V_pred) / Var(V_target)`. Critic quality metric. Should climb toward 1 as the critic learns.
  **解释方差。** Critic 质量指标。应随着 Critic 学习趋向 1。

## Pitfalls

- **Clip coefficient mistuned.** `ε = 0.2` is the de-facto standard. Going to `0.1` makes updates too timid; `0.3+` invites instability.
  **裁剪系数调错。** `ε = 0.2` 是事实标准。`0.1` 太保守；`0.3+` 导致不稳定。
- **Too many epochs.** `K > 20` routinely destabilizes because the policy drifts far from `π_old`. Cap epochs, especially for large networks.
  **太多 epoch。** `K > 20` 常常不稳定，因为策略偏离 `π_old` 太远。限制 epoch，特别是大网络。
- **No reward normalization.** Large reward scales eat into the clip range. Normalize rewards (running std) before computing advantages.
  **没有奖励归一化。** 大奖励尺度侵蚀裁剪范围。计算优势前归一化奖励。
- **Forgetting advantage normalization.** Per-batch zero-mean/unit-std normalization is standard. Skipping it wrecks PPO on most benchmarks.
  **忘记优势归一化。** 每批次零均值/单位标准差归一化是标准的。跳过它在大多数基准上会破坏 PPO。
- **Learning rate not decayed.** PPO benefits from linear LR decay to zero. Constant LR is often worse.
  **学习率未衰减。** PPO 从线性 LR 衰减到零中受益。常数 LR 通常更差。
- **Importance ratio math errors.** Always `exp(log_new - log_old)` for numerical stability, not `new / old`.
  **重要性比率数学错误。** 始终用 `exp(log_new - log_old)` 保证数值稳定性，而非 `new / old`。
- **Wrong gradient sign.** Maximize the surrogate = *minimize* `-L^{CLIP}`. A flipped sign is the most common PPO bug.
  **梯度符号错误。** 最大化代理 = *最小化* `-L^{CLIP}`。符号反转为 PPO 最常见 bug。

## Use It | 用框架实现

PPO is 2026's default RL algorithm across a surprising number of domains:

> PPO 是 2026 年众多领域的默认 RL 算法：

| Use case | PPO variant |
|----------|-------------|
| Use case / 用例 | PPO variant / PPO 变体 |
| MuJoCo / robotics control / MuJoCo/机器人控制 | PPO with Gaussian policy, GAE(0.95) / 高斯策略的 PPO，GAE(0.95) |
| Atari / discrete games / Atari/离散游戏 | PPO with categorical policy, rolling 128-step rollouts / 分类策略的 PPO |
| RLHF for LLMs / LLM 的 RLHF | PPO with KL penalty to reference model, reward from RM at end of response / 带 KL 惩罚的 PPO |
| Large-scale game agents / 大规模游戏 Agent | IMPALA + PPO (AlphaStar, OpenAI Five) |
| Reasoning LLMs / 推理 LLM | GRPO (Lesson 12) — PPO variant without critic / 无 Critic 的 PPO 变体 |
| Preference-only data / 仅偏好数据 | DPO — closed-form collapsing of PPO+KL, no online sampling / 闭式 PPO+KL 折叠 |

The PPO *loss shape* — clipped surrogate + value + entropy — is the scaffolding for DPO, GRPO, and nearly every RLHF pipeline.

> PPO 的*损失形式*——裁剪代理 + 值 + 熵——是 DPO、GRPO 和几乎所有 RLHF 流水线的脚手架。

## Ship It | 产出物

Save as `outputs/skill-ppo-trainer.md`:

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

## Exercises | 练习题

1. **Easy.** Run PPO on 4×4 GridWorld with `ε=0.2, K=4`. Compare sample efficiency to A2C (one epoch per rollout) at matched env steps.
2. **Medium.** Sweep `K ∈ {1, 4, 10, 30}`. Plot return vs env steps and track mean KL per update. At what `K` does KL explode on this task?
3. **Hard.** Replace the clipped surrogate with an adaptive KL penalty (`β` doubled if `KL > 2·target`, halved if `KL < target/2`). Compare final return, stability, and clip-free-ness.

## Key Terms | 术语速查表

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

## Further Reading | 延伸阅读

- [Schulman et al. (2017). Proximal Policy Optimization Algorithms](https://arxiv.org/abs/1707.06347) — the paper.
- [Schulman et al. (2015). Trust Region Policy Optimization](https://arxiv.org/abs/1502.05477) — TRPO, PPO's predecessor.
- [Andrychowicz et al. (2021). What Matters In On-Policy RL? A Large-Scale Empirical Study](https://arxiv.org/abs/2006.05990) — every PPO hyperparameter ablated.
- [Ouyang et al. (2022). Training language models to follow instructions with human feedback](https://arxiv.org/abs/2203.02155) — InstructGPT; the PPO-in-RLHF recipe.
- [OpenAI Spinning Up — PPO](https://spinningup.openai.com/en/latest/algorithms/ppo.html) — clean modern exposition with PyTorch.
- [CleanRL PPO implementation](https://github.com/vwxyzjn/cleanrl) — reference single-file PPO used by many papers.
- [Hugging Face TRL — PPOTrainer](https://huggingface.co/docs/trl/main/en/ppo_trainer) — the production recipe for PPO on language models; read alongside Lesson 09 (RLHF).
- [Engstrom et al. (2020). Implementation Matters in Deep Policy Gradients](https://arxiv.org/abs/2005.12729) — the "37 code-level optimizations" paper; which PPO tricks are load-bearing and which are folklore.
