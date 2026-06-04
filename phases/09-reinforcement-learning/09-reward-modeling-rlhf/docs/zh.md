# 奖励建模与 RLHF

> 人类无法为"好的助手回复"写奖励函数，但可以比较两个回复选更好的。用这些比较训练奖励模型，再用 RL 优化语言模型。Christiano 2017。InstructGPT 2022。把 GPT-3 变成 ChatGPT 的配方。2026 年大多被 DPO 取代，但思维方式不变。

> **【中文解读】** 人类无法为"好的助手回复"写奖励函数，但可以比较两个回复选更好的。用这些比较训练奖励模型，再用 RL 优化语言模型。这就是把 GPT-3 变成 ChatGPT 的方法。2026 年大多被 DPO 取代，但思维方式不变。

> **【拓展：RLHF 是大模型对齐的关键】** RLHF（基于人类反馈的强化学习）是 ChatGPT 成功的核心技术。三步流程：(1) 监督微调 SFT；(2) 训练奖励模型 RM；(3) 用 PPO 优化 LM。DPO 简化了第 2-3 步，但本质相同。

**类型：** 构建
**语言：** Python
**前置知识：** Phase 5 · 05（情感分析），Phase 9 · 08（PPO）
**用时：** 约 45 分钟

## 问题引入

你在下一 token 预测目标上训练了一个语言模型。它能写出语法正确的英语。但它也会撒谎、跑题、拒绝拒绝。你无法通过更多预训练来修复——网页文本是问题的根源，不是解药。

你需要一个*标量奖励*来表达"回复 A 比回复 B 更适合指令 X"。手写这个奖励函数是不可能的。"有用性"不是 token 上的闭式表达式。但人类可以比较两个输出并标记偏好。这在大规模上收集很便宜。

RLHF（Christiano 等人 2017；Ouyang 等人 2022）将偏好转化为奖励模型，然后通过 PPO 对该奖励优化 LM。分三步：SFT → RM → PPO。这是发布 ChatGPT、Claude、Gemini 和 2023-2025 年所有其他对齐 LLM 的配方。

2026 年，PPO 步骤大多被 DPO（Phase 10 · 08）取代，因为它更便宜且对齐调优几乎一样好。但*奖励模型*部分仍然支撑着每个 Best-of-N 采样器、每个基于可验证奖励的 RL 管线、以及每个使用过程奖励模型的推理模型。理解 RLHF 就理解整个对齐技术栈。

> **【中文解读】** RLHF 三阶段流程：(1) SFT——在人类示范数据上监督微调基础模型；(2) RM——用人类偏好对训练 Bradley-Terry 奖励模型；(3) PPO——用奖励模型的信号优化语言模型，同时加 KL 惩罚防止偏离 SFT 太远。虽然 2026 年 PPO 步骤多被 DPO 替代，但奖励模型仍在 Best-of-N 采样、可验证奖励 RL、过程奖励模型等场景中广泛使用。

> **【拓展：DPO 与 RLHF 的对比】** DPO（Direct Preference Optimization）将 RLHF 的 RM+PPO 两步合并为一步——直接从偏好对训练策略，无需显式训练奖励模型。数学上等价于在 Bradley-Terry 模型下优化策略。DPO 更简单、更稳定，但在需要"可验证奖励"（如数学题对错）的场景中，显式奖励模型仍有优势。DeepSeek-R1 使用 GRPO 是另一个有趣的替代方案。

## 核心概念

![三阶段 RLHF：SFT、RM 偏好对训练、带 KL 惩罚的 PPO](../assets/rlhf.svg)

**第 1 阶段：监督微调 (SFT)。** 从预训练基础模型开始。在目标行为的人类编写示范上微调（指令遵循回复、有用回答等）。结果：一个*偏向良好行为*但仍有无限动作空间的模型 `π_SFT`。

**第 2 阶段：奖励模型训练。**

- 收集提示 `x` 的回复对 `(y_+, y_-)`，由人类标注"y_+ 优于 y_-"。
- 训练奖励模型 `R_φ(x, y)` 使 `y_+` 获得更高分数。
- 损失函数：**Bradley-Terry 成对逻辑回归**：

  `L(φ) = -E[ log σ(R_φ(x, y_+) - R_φ(x, y_-)) ]`

  σ 是 sigmoid。奖励差异隐含了偏好的对数几率。BT 自 1952 年以来就是标准（Bradley-Terry），是现代 RLHF 中的主导选择。

- `R_φ` 通常从 SFT 模型初始化，顶部加一个标量头。相同的 Transformer 主干；一个线性层输出奖励。

**第 3 阶段：带 KL 惩罚的 PPO 对 RM 优化。**

- 从 `π_SFT` 初始化可训练策略 `π_θ`。保持冻结的*参考* `π_ref = π_SFT`。
- 回复 `y` 结束时的奖励：

  `r_total(x, y) = R_φ(x, y) - β · KL(π_θ(·|x) || π_ref(·|x))`

  KL 惩罚防止 `π_θ` 从 `π_SFT` 任意漂移——它是*正则化器*，而非硬信赖域。`β` 通常 `0.01`-`0.05`。
- 用此奖励运行 PPO（第 08 课）。优势在 token 级轨迹上计算，但 RM 仅对完整回复评分。

**为什么需要 KL？** 没有它，PPO 会愉快地找到奖励黑客策略——RM 只在分布内补全上训练。分布外回复可能比任何人写的都高。KL 让 `π_θ` 保持在 RM 训练的流形附近。它是 RLHF 中最重要的旋钮。

**2026 年现状：**

- **DPO**（Rafailov 2023）：闭式代数将第 2+3 阶段坍缩为偏好数据上的单个监督损失。无 RM，无 PPO。对齐基准上质量相同，计算量只是零头。在 Phase 10 · 08 中涵盖。
- **GRPO**（DeepSeek 2024-2025）：PPO 用组相对基线替代评论家，奖励来自*验证器*（代码运行 / 数学答案匹配）而非人类训练的 RM。推理模型的主导方法。在 Phase 9 · 12 中涵盖。
- **过程奖励模型 (PRM)：** 对部分解（每个推理步骤）评分，用于 RLHF 和 GRPO 推理变体。
- **宪法 AI / RLAIF：** 使用对齐的 LLM 生成偏好而非人类。扩大偏好预算。

## 动手实现

本课使用微小的合成"提示"和"回复"，用字符串表示。RM 是词袋表示上的线性评分器。没有真正的 LLM——*管线的形状*才是重要的，而非规模。参见 `code/main.py`。

### 第 1 步：合成偏好数据

```python
PROMPTS = ["help me", "answer me", "explain this"]
GOOD_WORDS = {"clear", "specific", "kind", "thorough"}
BAD_WORDS = {"vague", "rude", "wrong", "short"}

def make_pair(rng):
    x = rng.choice(PROMPTS)
    y_good = rng.choice(list(GOOD_WORDS)) + " " + rng.choice(list(GOOD_WORDS))
    y_bad = rng.choice(list(BAD_WORDS)) + " " + rng.choice(list(BAD_WORDS))
    return (x, y_good, y_bad)
```

在真实 RLHF 中，这由人类标注员替代。形状——`(提示, 偏好回复, 拒绝回复)`——完全相同。

### 第 2 步：Bradley-Terry 奖励模型

线性评分：`R(x, y) = w · bag(y)`。训练以最小化 BT 成对对数损失：

```python
def rm_train_step(w, x, y_pos, y_neg, lr):
    r_pos = dot(w, bag(y_pos))
    r_neg = dot(w, bag(y_neg))
    p = sigmoid(r_pos - r_neg)
    for tok, cnt in bag(y_pos).items():
        w[tok] += lr * (1 - p) * cnt
    for tok, cnt in bag(y_neg).items():
        w[tok] -= lr * (1 - p) * cnt
```

几百次更新后，`w` 给好词 token 分配正权重，给坏词分配负权重。

### 第 3 步：RM 之上的类 PPO 策略

我们的玩具策略从词表中产生单个 token。我们在 RM 下对 token 评分，计算 `log π_θ(token | prompt)`，添加到参考的 KL 惩罚，应用裁剪的 PPO 代理。

```python
def rlhf_step(theta, ref, w, prompt, rng, eps=0.2, beta=0.1, lr=0.05):
    logits_theta = policy_logits(theta, prompt)
    probs = softmax(logits_theta)
    token = sample(probs, rng)
    logits_ref = policy_logits(ref, prompt)
    probs_ref = softmax(logits_ref)
    reward = dot(w, bag([token])) - beta * kl(probs, probs_ref)
    # 对 theta 做 PPO 风格更新，将奖励视为回报
    ...
```

### 第 4 步：监控 KL

每次更新追踪平均 `KL(π_θ || π_ref)`。如果它悄悄超过 `~5-10`，策略已经漂移远离 `π_SFT`——降低 `β` 正在上升或奖励黑客行为正在开始。这是真实 RLHF 中的首要诊断。

### 第 5 步：使用 TRL 的生产配方

一旦你理解了玩具管线，以下是真实库用户编写相同循环的方式。Hugging Face 的 [TRL](https://huggingface.co/docs/trl) 是参考实现——`RewardTrainer` 用于第 2 阶段，`PPOTrainer`（内置到参考的 KL）用于第 3 阶段。

```python
# 第 2 阶段：从成对偏好训练奖励模型
from trl import RewardTrainer, RewardConfig
from transformers import AutoModelForSequenceClassification, AutoTokenizer

tok = AutoTokenizer.from_pretrained("meta-llama/Llama-3.1-8B-Instruct")
rm = AutoModelForSequenceClassification.from_pretrained(
    "meta-llama/Llama-3.1-8B-Instruct", num_labels=1
)

# 数据集行：{"prompt", "chosen", "rejected"} — Bradley-Terry 格式
trainer = RewardTrainer(
    model=rm,
    tokenizer=tok,
    train_dataset=preference_data,
    args=RewardConfig(output_dir="./rm", num_train_epochs=1, learning_rate=1e-5),
)
trainer.train()
```

```python
# 第 3 阶段：带 KL 惩罚到 SFT 参考的 PPO 对 RM 优化
from trl import PPOTrainer, PPOConfig, AutoModelForCausalLMWithValueHead

policy = AutoModelForCausalLMWithValueHead.from_pretrained("./sft-checkpoint")
ref    = AutoModelForCausalLMWithValueHead.from_pretrained("./sft-checkpoint")  # 冻结

ppo = PPOTrainer(
    config=PPOConfig(learning_rate=1.41e-5, batch_size=64, init_kl_coef=0.05,
                     target_kl=6.0, adap_kl_ctrl=True),
    model=policy, ref_model=ref, tokenizer=tok,
)

for batch in dataloader:
    responses = ppo.generate(batch["query_ids"], max_new_tokens=128)
    rewards   = rm(torch.cat([batch["query_ids"], responses], dim=-1)).logits[:, 0]
    stats     = ppo.step(batch["query_ids"], responses, rewards)
    # stats 包含：mean_kl, clip_frac, value_loss — 三个 PPO 诊断
```

库为你做的三件事。`adap_kl_ctrl=True` 实现自适应 β 调度：如果观测 KL 超过 `target_kl`，β 翻倍；低于一半则减半。参考模型按约定冻结——你不能意外地与 `policy` 共享参数。值头与策略在同一主干上（`AutoModelForCausalLMWithValueHead` 附加一个标量 MLP 头），这就是为什么 TRL 分别报告 `policy/kl` 和 `value/loss`。

## 常见陷阱

- **过度优化 / 奖励黑客行为。** RM 不完美；`π_θ` 找到评分高但质量差的对抗性补全。症状：奖励持续攀升而人类评估分数停滞或下降。修复：早停，提高 `β`，扩展 RM 训练数据。
- **长度黑客行为。** 在有用回复上训练的 RM 通常隐含地奖励长度。策略学会填充回复。缓解：长度归一化奖励，或使用长度感知 RM 的 RLAIF。
- **RM 太小。** RM 需要至少与策略一样大。小型 RM 无法忠实地评分策略的输出。
- **KL 调优。** β 太低 → 漂移和奖励黑客。β 太高 → 策略几乎不变。标准技巧是自适应 β，目标固定每步 KL。
- **偏好数据噪声。** 约 30% 的人类标签有噪声或模糊。通过在一致性过滤数据上训练 RM 或在 BT 上使用温度来校准。
- **离策略问题。** PPO 数据在第一轮后略微偏策略。如第 08 课一样监控裁剪比例。

## 用框架实现

2026 年的 RLHF 是分层的：

| 层级 | 目标 | 方法 |
|------|------|------|
| 指令遵循、有用性、无害性 | 对齐 | DPO（Phase 10 · 08）优于 RLHF-PPO。 |
| 推理正确性（数学、代码） | 能力 | 带验证器奖励的 GRPO（Phase 9 · 12）。 |
| 长视野多步任务 | 智能体 | 带过程奖励模型的 PPO / GRPO。 |
| 安全 / 拒绝行为 | 安全 | 带独立安全 RM 的 RLHF-PPO，或宪法 AI。 |
| 推理时 Best-of-N | 快速对齐 | 解码时使用 RM；无需策略训练。 |
| 奖励蒸馏 | 推理计算 | 在冻结 LM 上训练小型"奖励头"。 |

RLHF 在 2022-2024 年是*主流*方法。2026 年，生产对齐管线是 DPO 优先的，PPO 仅用于 RM 密集或安全关键的步骤。

## 产出物

保存为 `outputs/skill-rlhf-architect.md`：

```markdown
---
name: rlhf-architect
description: 为语言模型设计 RLHF / DPO / GRPO 对齐管线，包括 RM、KL 和数据策略。
version: 1.0.0
phase: 9
lesson: 9
tags: [rl, rlhf, alignment, llm]
---

给定基础 LM、目标行为（对齐 / 推理 / 拒绝 / 智能体）和偏好或验证器预算，输出：

1. 阶段。SFT？RM？DPO？GRPO？附理由。
2. 偏好或验证器来源。人类、AI 反馈、基于规则、单元测试通过、或奖励蒸馏。
3. KL 策略。固定 β、自适应 β、或 DPO（隐式 KL）。
4. 诊断。平均 KL、奖励稳定性、过度优化防护（盲测人类评估）。
5. 安全门。红队测试集、拒绝率、独立于有用性 RM 的安全 RM。

拒绝发布没有 KL 监控的 RLHF-PPO。拒绝使用小于目标策略的 RM。拒绝仅长度奖励。标记任何未保留盲测人类评估集的管线为缺少过度优化防护。
```

## 练习题

1. **简单。** 在 500 对合成偏好对上训练 `code/main.py` 中的 Bradley-Terry 奖励模型。在 100 对保留集上测量成对准确率。应超过 90%。
2. **中等。** 用 `β ∈ {0.0, 0.1, 1.0}` 运行玩具 PPO-RLHF 循环。对每个值，绘制 RM 分数 vs 到参考的 KL 随更新变化。哪个运行出现奖励黑客？
3. **困难。** 在相同偏好数据上实现 DPO（闭式偏好似然损失），与 RLHF-PPO 管线比较计算使用量和最终 RM 分数。

## 术语速查表

| 术语 | 通俗说法 | 实际含义 |
|------|----------|----------|
| RLHF | "对齐 RL" | 三阶段 SFT + RM + PPO 管线（Christiano 2017，Ouyang 2022）。 |
| 奖励模型 (RM) | "评分网络" | 通过 Bradley-Terry 拟合成对偏好的学习标量函数。 |
| Bradley-Terry | "成对逻辑损失" | `P(y_+ ≻ y_-) = σ(R(y_+) - R(y_-))`；标准 RM 目标。 |
| KL 惩罚 | "靠近参考" | 奖励中的 `β · KL(π_θ \|\| π_ref)`；反奖励黑客正则化器。 |
| 奖励黑客行为 | "古德哈特定律" | 策略利用 RM 缺陷；症状：奖励上升，人类评估不变。 |
| RLAIF | "AI 标注偏好" | 标签来自另一个 LM 而非人类的 RLHF。 |
| PRM | "过程奖励模型" | 对部分推理步骤评分；用于推理管线。 |
| 宪法 AI | "Anthropic 的方法" | 由显式规则指导的 AI 生成偏好。 |

## 延伸阅读

- [Christiano et al. (2017). Deep Reinforcement Learning from Human Preferences](https://arxiv.org/abs/1706.03741) — 开创 RLHF 的论文。
- [Ouyang et al. (2022). InstructGPT — Training language models to follow instructions with human feedback](https://arxiv.org/abs/2203.02155) — ChatGPT 背后的配方。
- [Stiennon et al. (2020). Learning to summarize with human feedback](https://arxiv.org/abs/2009.01325) — 早期的摘要 RLHF。
- [Rafailov et al. (2023). Direct Preference Optimization](https://arxiv.org/abs/2305.18290) — DPO；2026 年后 RLHF 的默认选择。
- [Bai et al. (2022). Constitutional AI: Harmlessness from AI Feedback](https://arxiv.org/abs/2212.08073) — RLAIF 和自我批评循环。
- [Anthropic RLHF paper (Bai et al. 2022). Training a Helpful and Harmless Assistant](https://arxiv.org/abs/2204.05862) — HH 论文。
- [Hugging Face TRL library](https://huggingface.co/docs/trl) — 生产 `RewardTrainer` 和 `PPOTrainer`。阅读训练器源码了解自适应 KL 和值头细节。
- [Hugging Face — Illustrating Reinforcement Learning from Human Feedback](https://huggingface.co/blog/rlhf) by Lambert, Castricato, von Werra, Havrilla — 带图表的三阶段管线经典图文教程。
- [von Werra et al. (2020). TRL: Transformer Reinforcement Learning](https://github.com/huggingface/trl) — 库；`examples/` 有 Llama、Mistral 和 Qwen 的端到端 RLHF 脚本。
- [Sutton & Barto (2018). Ch. 17.4 — Designing Reward Signals](http://incompleteideas.net/book/RLbook2020.pdf) — 奖励假设视角；思考奖励黑客的必要前提。
