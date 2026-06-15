# RL for Games — AlphaZero, MuZero, and the LLM-Reasoning Era | 游戏中的强化学习 — AlphaZero、MuZero 与 LLM 推理时代

> 1992: TD-Gammon beat human champions at backgammon with pure TD. 2016: AlphaGo beat Lee Sedol. 2017: AlphaZero dominated chess, shogi, and Go from scratch. 2024: DeepSeek-R1 proved the same recipe, with GRPO replacing PPO, works on reasoning. Games are the benchmark that drives every breakthrough in this phase.

> **【中文解读】** 游戏是 RL 突破的试验场：TD-Gammon (1992) → AlphaGo (2016) → AlphaZero (2017) → DeepSeek-R1 (2025)。DeepSeek-R1 证明了 AlphaZero 的"自我博弈+搜索+策略改进"循环可以直接用于大模型的数学推理——token 就是动作，验证器就是"赢/输"信号。

**Type:** Build | **类型:** 动手
**Languages:** Python | **语言:** Python
**Prerequisites:** Phase 9 · 05 (DQN), Phase 9 · 08 (PPO), Phase 9 · 09 (RLHF), Phase 9 · 10 (MARL) | **前置知识:** Phase 9 · 05 (DQN), Phase 9 · 08 (PPO), Phase 9 · 09 (RLHF), Phase 9 · 10 (多智能体 RL)
**Time:** ~120 minutes | **时间:** ~120 分钟

## The Problem | 问题引入

Games have everything RL wants. Clean reward (win/loss). Infinite episodes (self-play resets). Perfect simulation (the game *is* the simulator). Discrete or small continuous action spaces. Multi-agent structure that forces adversarial robustness.

> 游戏拥有 RL 所需的一切。清晰的奖励（赢/输）。无限回合（自我博弈重置）。完美仿真（游戏*就是*仿真器）。离散或小型连续动作空间。迫使对抗鲁棒性的多智能体结构。

And games are how every major RL breakthrough was tested. TD-Gammon (backgammon, 1992). Atari-DQN (2013). AlphaGo (2016). AlphaZero (2017). OpenAI Five (Dota 2, 2019). AlphaStar (StarCraft II, 2019). MuZero (learned model, 2019). AlphaTensor (matrix multiplication, 2022). AlphaDev (sorting algorithms, 2023). DeepSeek-R1 (math reasoning, 2025) — the latest demonstration that game-RL techniques work on text.

> 游戏是每个 RL 重大突破的试验场。TD-Gammon（西洋双陆棋，1992）、Atari-DQN（2013）、AlphaGo（2016）、AlphaZero（2017）、OpenAI Five（Dota 2，2019）、AlphaStar（星际争霸 II，2019）、MuZero（学习模型，2019）、AlphaTensor（矩阵乘法，2022）、AlphaDev（排序算法，2023）、DeepSeek-R1（数学推理，2025）——最新的证明：游戏 RL 技术可以用于文本。

This capstone surveys the three landmark architectures — AlphaZero, MuZero, and GRPO — through a single unifying lens: **self-play + search + policy improvement**. Each generalizes the previous; GRPO in particular is AlphaZero's recipe applied to LLM reasoning, with tokens as actions and mathematical verification as the win signal.

> 这个总结通过单一统一视角——**自我博弈+搜索+策略改进**——审视三个里程碑架构：AlphaZero、MuZero 和 GRPO。每个都是前一个的推广；GRPO 特别是将 AlphaZero 的配方应用于 LLM 推理，token 是动作，数学验证是获胜信号。

## The Concept | 核心概念

![AlphaZero ↔ MuZero ↔ GRPO: same loop, different environments](../assets/rl-games.svg)

**The unifying loop.**

```
while True:
    trajectory = self_play(current_policy, search)     # play game against self
    policy_target = search.improved_policy(trajectory) # search improves raw policy
    policy_net.update(policy_target, value_target)     # supervised on search output
```

**AlphaZero (2017).** Silver et al. Given a game (chess, shogi, Go) with known rules:

- Policy-value network: one tower `f_θ(s) → (p, v)`. `p` is a prior over legal moves. `v` is the expected game outcome.
- Monte Carlo Tree Search (MCTS): at each move, expand a tree of possible continuations. Use `(p, v)` as the prior + bootstrap. Select nodes by UCB (PUCT): `a* = argmax Q(s, a) + c · p(a|s) · √N(s) / (1 + N(s, a))`.
- Self-play: play games agent-vs-agent. At move `t`, the MCTS visit distribution `π_t` becomes the policy training target.
- Loss: `L = (v - z)² - π · log p + c · ||θ||²`. `z` is the game outcome (+1 / 0 / -1).

Zero human knowledge. Zero handcrafted heuristics. A single recipe that mastered chess, shogi, and Go after a few tens of millions of self-play games each.

> 零人类知识。零手工启发式。一个配方在数千万自我博弈后掌握了国际象棋、将棋和围棋。

**MuZero (2019).** Schrittwieser et al. Removes the requirement that the rules are known.

- Instead of a fixed environment, learn a *latent dynamics model* `(h, g, f)`:
  - `h(s)`: encode observation to latent state.
  - `g(s_latent, a)`: predict next latent state + reward.
  - `f(s_latent)`: predict policy prior + value.
- MCTS runs in the *learned latent space*. Same search, same training loop.
- Works on Go, chess, shogi *and* Atari — one algorithm, no rule knowledge.

> 在围棋、国际象棋、将棋和 Atari 上都有效——一个算法，无需规则知识。

> **【中文解读】** AlphaZero 和 MuZero 的核心循环：自我博弈 → MCTS 搜索改进策略 → 监督学习更新网络。AlphaZero 需要已知游戏规则，MuZero 通过学习隐空间动力学模型消除了这个限制。这个"自我博弈+搜索+策略改进"循环直接启发了 DeepSeek-R1 的推理训练——用可验证奖励替代游戏胜负信号。

> **【拓展：DeepSeek-R1 与 AlphaZero 范式】** DeepSeek-R1（2025）将 AlphaZero 的范式应用于 LLM 推理：token 就是动作，推理过程就是"游戏"，验证器（数学题对错、代码是否通过测试）就是"胜负信号"。GRPO 替代 PPO，组内采样替代自我博弈。这验证了游戏 AI 的方法论可以迁移到大模型推理训练。

**Stochastic MuZero (2022).** Adds stochastic dynamics and chance nodes; extends to backgammon-class games.

> **随机 MuZero (2022)。** 添加随机动力学和机会节点；扩展到双陆棋类游戏。

**Muesli, Gumbel MuZero (2022-2024).** Improvements on sample efficiency and deterministic search.

> **Muesli、Gumbel MuZero (2022-2024)。** 样本效率和确定性搜索的改进。

**GRPO (2024-2025).** DeepSeek-R1 recipe. Same AlphaZero-shaped loop, applied to language-model reasoning:

- "Game": answer a math / coding / reasoning problem. "Win" = verifier (test case passes, numerical answer matches) returns 1.
- Policy: the LLM. Actions: tokens. State: prompt + response-so-far.
- No critic (PPO-style V_φ). Instead, for each prompt, sample `G` completions from the policy. Compute reward for each. Use the **group-relative advantage** `A_i = (r_i - mean_r) / std_r` as the signal for REINFORCE-style update.
- KL penalty to reference policy to prevent drift (like RLHF).
- Full loss:

  `L_GRPO(θ) = -E_{q, {o_i}} [ (1/G) Σ_i A_i · log π_θ(o_i | q) ] + β · KL(π_θ || π_ref)`

No reward model, no critic, no MCTS. Group-relative baseline replaces all three. Matches or exceeds PPO-RLHF quality on reasoning benchmarks at a fraction of the compute.

> **GRPO (2024-2025)。** DeepSeek-R1 配方。同样的 AlphaZero 形状循环，应用于语言模型推理：不需要奖励模型、Critic 或 MCTS。组相对基线替代了三者。在推理基准上匹配或超越 PPO-RLHF 质量，计算量仅为一小部分。

> **【中文解读】** GRPO 是 DeepSeek-R1 的核心创新：不需要 critic 网络（省一半内存），用组内均值和标准差构造优势。对每个问题采样 G 个回答，正确回答的优势为正（增强概率），错误的为负（降低概率）。这是"没有 critic 的 PPO"，是 2025 年大模型推理训练最重要的算法突破。

> **【拓展：GRPO→DeepSeek-R1→开源推理革命】** DeepSeek-R1 的四阶段训练流程：冷启动 SFT → 推理导向 GRPO → 拒绝采样+SFT → 全谱 GRPO。R1-Zero（纯 GRPO 无 SFT）证明了 LLM 可以从零学会推理，但输出可读性差。蒸馏实验表明：用强 RL 教师的推理轨迹做 SFT，比小模型从头做 RL 效果更好。

**The R1 recipe in full.** DeepSeek-R1 (DeepSeek 2025) is two models in one paper:

> **R1 完整配方。** DeepSeek-R1 是一篇论文中的两个模型：

- **R1-Zero.** Start from the DeepSeek-V3 base model. No SFT. Apply GRPO directly with two reward components: *accuracy reward* (rule-based — did the final answer parse to the correct number / did the code pass unit tests) and *format reward* (did the completion wrap its chain-of-thought in `<think>…</think>` tags). Over thousands of steps, average response length grows from ~100 to ~10,000 tokens and math benchmark scores climb to near-o1-preview levels. The model learns to reason from scratch. The downside: its chains of thought are often unreadable, mix languages, and lack stylistic polish.
- **R1.** Fix R1-Zero's readability problems with a four-stage pipeline:
  1. **Cold-start SFT.** Collect a few thousand long-CoT demonstrations with clean formatting. Supervised-finetune the base model on them. This gives a readable starting point.
  2. **Reasoning-oriented GRPO.** Apply GRPO with the accuracy+format rewards plus a *language-consistency* reward to prevent code-switching.
  3. **Rejection sampling + SFT round 2.** Sample ~600K reasoning trajectories from the RL checkpoint, keep only those with correct final answers and readable CoT, and combine with ~200K non-reasoning SFT examples (writing, QA, self-cognition). Fine-tune the base again.
  4. **Full-spectrum GRPO.** One more RL round covering both reasoning (rule-based rewards) and general alignment (helpfulness/harmlessness preference-based rewards).

The result matches o1 on AIME and MATH-500 at open weights, and is small enough to distill. The same paper also releases six distilled dense models (Qwen-1.5B through Llama-70B) by SFT'ing on R1's reasoning traces — no RL at the student. Distillation of a strong RL teacher consistently beats RL from scratch at the student's scale.

> 结果在 AIME 和 MATH-500 上匹配 o1，且足够小可以蒸馏。蒸馏强 RL 教师的推理轨迹始终优于学生规模的从头 RL。

**Why GRPO instead of PPO for reasoning.** Three reasons in the DeepSeekMath paper (Feb 2024): (1) no value network to train, halving memory; (2) the group baseline naturally handles the sparse end-of-trajectory reward that reasoning tasks produce; (3) per-prompt normalization makes advantages comparable across problems of wildly different difficulty, which PPO's single critic cannot.

> **为什么推理用 GRPO 而非 PPO。** 三个原因：(1) 无需训练值网络，内存减半；(2) 组基线自然处理推理任务产生的稀疏回合末奖励；(3) 每提示归一化使优势在难度差异巨大的问题间可比较。

**Search-free vs search-based.** Games have branched:

> **Search-free vs search-based.**

- *Perfect-information games with long horizons* (Go, chess): still search-based. AlphaZero / MuZero dominate.
- *LLM reasoning*: no MCTS yet in production; GRPO on full rollouts, best-of-N for inference compute. Process reward models (PRMs) hint at step-level search being added back.

## Build It | 动手实现

The code in `code/main.py` implements **GRPO in miniature** — a bandit with multiple groups of samples. The algorithm is the same as on an LLM; only the policy and environment are simpler. It teaches the *loss* and the *group-relative advantage*, which is the 2025 innovation.

> `code/main.py` 中的代码实现了**微型 GRPO**——一个带有多组样本的赌博机。算法与 LLM 上相同；只是策略和环境更简单。它教授*损失*和*组相对优势*，这是 2025 年的创新。

### Step 1: a tiny verifier environment

```python
QUESTIONS = [
    {"prompt": "q1", "correct": 3},
    {"prompt": "q2", "correct": 1},
]

def verify(prompt_idx, answer_token):
    return 1.0 if answer_token == QUESTIONS[prompt_idx]["correct"] else 0.0
```

In real GRPO the verifier runs unit tests or checks math equality.

> 真实 GRPO 中验证器运行单元测试或检查数学等式。

### Step 2: policy: softmax over K answer tokens per prompt

```python
def policy_probs(theta, p_idx):
    return softmax(theta[p_idx])
```

Equivalent to the final-layer output of an LLM conditioned on a prompt.

> 等价于 LLM 在给定提示下最后一层的输出。

### Step 3: group sampling and group-relative advantage

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
    # KL penalty: pull theta toward reference
    for i in range(len(probs)):
        theta[p_idx][i] -= beta * (theta[p_idx][i] - reference[p_idx][i])
```

The group-relative advantage is the 2024 DeepSeek trick. No critic needed. The "baseline" is the group mean, and normalization uses group std.

> 组相对优势是 2024 年 DeepSeek 的技巧。无需 Critic。"基线"是组均值，归一化使用组标准差。

### Step 4: compare to REINFORCE baseline (value-free)

Same setup, same compute, plain REINFORCE. GRPO converges faster and more stably.

> 相同设置，相同计算量，纯 REINFORCE。GRPO 收敛更快更稳定。

### Step 5: observe entropy and KL

Same diagnostics as RLHF: mean KL to reference, policy entropy, reward-over-time. Once these stabilize, training is done.

> 与 RLHF 相同的诊断：平均 KL 到参考策略、策略熵、奖励随时间变化。一旦稳定，训练完成。

## Pitfalls

- **Reward hacking via verifier gaming.** GRPO inherits RLHF's risk: if the verifier is wrong or exploitable, the LLM will find the exploit. Robust verifiers (multiple test cases, formal proofs) matter.
  **通过验证器博弈的奖励黑客。** GRPO 继承了 RLHF 的风险：如果验证器错误或可利用，LLM 会找到漏洞。健壮的验证器（多个测试用例、形式化证明）很重要。
- **Group size too small.** Variance of the group baseline goes like `1/√G`. Below `G = 4`, the advantage signal is noisy; standard choice is `G = 8` to `64`.
  **组大小太小。** 组基线的方差与 `1/√G` 成正比。`G = 4` 以下优势信号有噪声；标准选择是 `G = 8` 到 `64`。
- **Length bias.** LLM completions of different lengths have different log-probabilities. Normalize by token count, or use sequence-level log-prob, or truncate to max length.
  **长度偏差。** 不同长度的 LLM 完成有不同的对数概率。按 token 数归一化或截断到最大长度。
- **Pure self-play cycles.** AlphaZero-style training can get stuck in dominance loops on general-sum games. Mitigated by diverse opponent pools (league play, Lesson 10).
  **纯自我博弈循环。** AlphaZero 式训练在一般和博弈上可能陷入支配循环。通过多样化对手池缓解。
- **Search-policy mismatch.** AlphaZero trains the policy to mimic search output. If the policy net is too small to represent the search's distribution, training stalls.
  **搜索-策略不匹配。** AlphaZero 训练策略模仿搜索输出。如果策略网络太小无法表示搜索分布，训练停滞。
- **Compute floor.** MuZero / AlphaZero need massive compute. A single ablation is often hundreds of GPU-hours. Miniature demos exist (e.g., AlphaZero on Connect Four) for learning.
  **计算下限。** MuZero/AlphaZero 需要大量计算。单次消融通常需要数百 GPU 小时。
- **Verifier coverage.** Unit tests that pass for a buggy solution reinforce the bug. Design verifiers that catch edge cases.
  **验证器覆盖。** 通过有 bug 解决方案的单元测试会强化 bug。设计能捕获边缘情况的验证器。

## Use It | 用框架实现

The 2026 game-RL landscape, by domain:

> 2026 年游戏 RL 版图，按领域：

| Domain | Dominant method |
|--------|-----------------|
| Domain / 领域 | Dominant method / 主导方法 |
| Two-player zero-sum board games (Go, chess, shogi) / 双人零和棋类 | AlphaZero / MuZero / KataGo |
| Imperfect info card games (poker) / 不完全信息纸牌 | CFR + deep learning (DeepStack, Libratus, Pluribus) / CFR + 深度学习 |
| Atari / pixel games / Atari/像素游戏 | Muesli / MuZero / IMPALA-PPO |
| Large multiplayer strategy (Dota, StarCraft) / 大型多人策略 | PPO + self-play + league (OpenAI Five, AlphaStar) |
| LLM math/code reasoning / LLM 数学/代码推理 | GRPO (DeepSeek-R1, Qwen-RL, open replications) |
| LLM alignment / LLM 对齐 | DPO / RLHF-PPO (not GRPO; verifier is preference not verifiable) / DPO/RLHF-PPO |
| Robotics / 机器人 | PPO + DR (not game-RL, but uses same policy-gradient tools) / PPO+DR |
| Combinatorial problems / 组合问题 | AlphaZero variants (AlphaTensor, AlphaDev) / AlphaZero 变体 |

The *recipe* — self-play, search-augmented improvement, policy distillation — spans text, pixels, and physical control. GRPO is the youngest instance; more are coming.

> 这个*配方*——自我博弈、搜索增强改进、策略蒸馏——跨越文本、像素和物理控制。GRPO 是最新的实例；更多即将到来。

## Ship It | 产出物

Save as `outputs/skill-game-rl-designer.md`:

```markdown
---
name: game-rl-designer
description: Design a game-RL or reasoning-RL training pipeline (AlphaZero / MuZero / GRPO) for a given domain.
version: 1.0.0
phase: 9
lesson: 12
tags: [rl, alphazero, muzero, grpo, self-play]
---

Given a target (perfect-info game / imperfect-info / Atari / LLM reasoning / combinatorial), output:

1. Environment fit. Known rules? Markov? Stochastic? Multi-agent? Informs AlphaZero vs MuZero vs GRPO.
2. Search strategy. MCTS (PUCT with learned prior), Gumbel-sampled, best-of-N, or none.
3. Self-play plan. Symmetric self-play / league / offline data / verifier-generated.
4. Target signal. Game outcome / verifier reward / preference / learned model. Include robustness plan.
5. Diagnostics. Win rate vs baseline, ELO curve, verifier pass rate, KL to reference.

Refuse AlphaZero on imperfect-info games (route to CFR). Refuse GRPO without a trusted verifier. Refuse any game-RL pipeline without a fixed baseline opponent set (self-play ELO is uncalibrated otherwise).
```

## Exercises | 练习题

1. **Easy.** Implement the GRPO bandit in `code/main.py`. Train on 2 prompts × 4 answer tokens each. Converge in < 1,000 updates with `G=8`.
2. **Medium.** Plug in PPO (clipped) and vanilla REINFORCE. Compare sample efficiency and reward variance to GRPO on the same bandit.
3. **Hard.** Extend to a length-2 "reasoning chain": the agent emits two tokens and the verifier rewards the pair. Measure how GRPO handles the credit assignment across two-step sequences. (Hint: compute group advantage per *full sequence*, propagate to both token positions.)

## Key Terms | 术语速查表

| Term | What people say | What it actually means |
|------|-----------------|-----------------------|
| MCTS | "Tree search with learned net" / 蒙特卡洛树搜索 | Monte Carlo Tree Search; UCB1/PUCT selection with learned `(p, v)` priors. |
| AlphaZero | "Self-play + MCTS" / AlphaZero | Policy-value net trained to match MCTS visits and game outcome. |
| MuZero | "Learned-model AlphaZero" / MuZero | Same loop but in latent space via learned dynamics. |
| GRPO | "Critic-free PPO" / 组相对策略优化 | Group Relative Policy Optimization; REINFORCE with group-mean baseline + KL. |
| PUCT | "AlphaZero's UCB" / PUCT 选择公式 | `Q + c · p · √N / (1 + N_a)` — balances value estimate with prior. |
| Self-play | "Agent vs past self" / 自我博弈 | Standard for zero-sum; symmetric training signal. |
| League play | "Population-based self-play" / 联盟训练 | Past + current + exploiters sampled as opponents. |
| Verifier reward | "Verifiable RL" / 验证器奖励 | Reward comes from a deterministic checker (tests pass, answer matches). |
| Process reward | "PRM" / 过程奖励模型 | Scores each reasoning step, not just the final answer. |

## Further Reading | 延伸阅读

- [Silver et al. (2017). Mastering the game of Go without human knowledge (AlphaGo Zero)](https://www.nature.com/articles/nature24270).
- [Silver et al. (2018). A general reinforcement learning algorithm that masters chess, shogi, and Go through self-play (AlphaZero)](https://www.science.org/doi/10.1126/science.aar6404).
- [Schrittwieser et al. (2020). Mastering Atari, Go, chess and shogi by planning with a learned model (MuZero)](https://www.nature.com/articles/s41586-020-03051-4).
- [Vinyals et al. (2019). Grandmaster level in StarCraft II (AlphaStar)](https://www.nature.com/articles/s41586-019-1724-z).
- [DeepSeek-AI (2024). DeepSeekMath: Pushing the Limits of Mathematical Reasoning in Open Language Models (GRPO)](https://arxiv.org/abs/2402.03300) — the paper that introduced GRPO and the group-relative baseline.
- [DeepSeek-AI (2025). DeepSeek-R1: Incentivizing Reasoning Capability in LLMs via Reinforcement Learning](https://arxiv.org/abs/2501.12948) — the full four-stage R1 recipe plus the R1-Zero ablation.
- [Brown et al. (2019). Superhuman AI for multiplayer poker (Pluribus)](https://www.science.org/doi/10.1126/science.aay2400) — CFR + deep-learning at scale.
- [Tesauro (1995). Temporal Difference Learning and TD-Gammon](https://dl.acm.org/doi/10.1145/203330.203343) — the paper that started it all.
- [Hugging Face TRL — GRPOTrainer](https://huggingface.co/docs/trl/main/en/grpo_trainer) — the production reference for applying GRPO with custom reward functions.
- [Qwen Team (2024). Qwen2.5-Math — GRPO replication](https://github.com/QwenLM/Qwen2.5-Math) — open replication of the R1 recipe at multiple scales.
- [Sutton & Barto (2018). Ch. 17 — Frontiers of Reinforcement Learning](http://incompleteideas.net/book/RLbook2020.pdf) — the textbook framing for self-play, search, and "designed reward" that R1 instantiates at LLM scale.
