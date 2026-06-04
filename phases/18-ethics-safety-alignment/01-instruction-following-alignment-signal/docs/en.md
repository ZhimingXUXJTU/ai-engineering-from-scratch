# Instruction-Following as Alignment Signal | 指令遵循作为对齐信号

> Every later critique of RLHF argues against this pipeline. Before you study how optimization pressure distorts a proxy, you have to see the proxy. InstructGPT (Ouyang et al., 2022) defined the reference architecture: supervised fine-tuning on instruction-response pairs, a reward model trained on pairwise preference rankings, and PPO against the reward model with a KL penalty to the SFT policy. A 1.3B InstructGPT was preferred over a 175B GPT-3. That single result is the reason every frontier lab in 2026 still ships an RLHF-shaped post-training pipeline.

> **【中文解读】** InstructGPT（Ouyang 等人, 2022）定义了对齐的参考架构：1) 监督微调（SFT）在指令-响应对上训练；2) 奖励模型在成对偏好排序上训练；3) PPO 对抗奖励模型，带 KL 惩罚保护。1.3B 的 InstructGPT 在人类偏好评估上超越了 175B 的 GPT-3。这就是为什么 2026 年每个前沿实验室仍在使用 RLHF 形式的后训练管线。

> **【拓展：RLHF → 现代 AI 对齐】** RLHF（基于人类反馈的强化学习）是 ChatGPT 成功的关键技术。InstructGPT 的三阶段管线——SFT→RM→PPO——已成为行业标准。2026 年的变体包括 DPO（直接偏好优化）、Constitutional AI（宪法 AI）等，但核心思路相同：用人类偏好信号引导模型行为。

**Type:** Learn
**Languages:** Python (stdlib, toy three-stage pipeline)
**Prerequisites:** Phase 10 · 06 (SFT), Phase 10 · 07 (RLHF), Phase 10 · 08 (DPO)
**Time:** ~45 minutes

## Learning Objectives | 学习目标

- Name the three stages of the InstructGPT pipeline and the loss used in each.
- Explain why a 1.3B instruction-tuned model beat the raw 175B GPT-3 on human preference evaluation.
- State what the KL penalty in stage 3 is protecting against and why removing it collapses to mode-seeking behaviour.
- Describe the alignment tax and the PPO-ptx mitigation Ouyang et al. used against it.

## The Problem | 问题

Pre-trained language models complete text. They do not answer questions. Ask GPT-3 "write a Python function that reverses a list" and you often get back another prompt, because most of the training distribution is web text that continues with more web text. The model is doing its job — the job is wrong.

The proxy every serious lab used to fix this is human preference. Two completions go to a rater; the rater picks the better one; a reward model learns the rater. Then an RL loop shifts the policy toward outputs the reward model scores high. That is the full InstructGPT thesis in three sentences. The rest of the paper is engineering.

## The Concept | 概念

### Stage 1: supervised fine-tuning (SFT)

Collect prompt-response pairs where the response is what a well-intentioned human would write. Ouyang et al. used 13k prompts from labelers and the OpenAI API. Fine-tune the base model on this data with standard cross-entropy loss.

What SFT gives you: the model now answers questions instead of continuing them. What it does not give you: any signal about which answer the rater prefers when multiple are plausible.

> **【中文解读】** SFT 阶段使模型从"补全文本"转向"回答问题"，但无法提供关于多个合理答案中哪个更好的信号。RM 阶段使用 Bradley-Terry 成对偏好损失 L_RM = -log sigmoid(r(x,y_w) - r(x,y_l)) 在标注者排序的补全对上训练奖励模型。RM 通常从 SFT 模型初始化并替换 LM 头为标量头，6B 就足以指导 175B 模型。

### Stage 2: reward model (RM)

For each prompt, sample K completions from the SFT model. A labeler ranks them. Train a reward model that scores any prompt-response pair so that, for pairs where `y_w` was preferred over `y_l`:

```
L_RM = -log sigmoid(r(x, y_w) - r(x, y_l))
```

This is the Bradley-Terry pairwise preference loss. The RM is usually initialized from the SFT model with the LM head replaced by a scalar head.

Reward models are small: 6B was enough for the 175B InstructGPT. They are also fragile — section 5 of the paper is mostly about reward-hacking behaviours that showed up at small scale.

> **【拓展：PPO 阶段 → RLHF 的核心工程】** PPO 阶段的目标函数 J(pi) = E[r(x,y)] - beta * KL(pi || pi_SFT) 最大化奖励同时保持策略接近 SFT。KL 系数 beta 是最重要的 RLHF 超参数——太低导致奖励黑客，太高则 SFT 上无改进。没有 KL 项，优化器找到的是 RM 从未见过的对抗样本——分数高不是因为人类真正偏好，而是因为 RM 从未评估过这些输入。

### Stage 3: PPO with a KL penalty

Define the objective:

```
J(pi) = E_{x~D, y~pi(.|x)} [ r(x, y) ] - beta * KL(pi(.|x) || pi_SFT(.|x))
```

Maximize with PPO. The KL term keeps `pi` from drifting far from the SFT policy. Without it, the optimizer finds adversarial examples — strings that score high under the RM because the RM never saw them, not because humans actually prefer them.

The KL coefficient `beta` is the single most important RLHF hyperparameter. Too low: reward hacking. Too high: no improvement over SFT.

> **【中文解读】** 对齐税：RLHF 后模型在人类偏好上更好但在标准基准（SQuAD, HellaSwag, DROP）上退步。Ouyang 等人称之为"对齐税"并用 PPO-ptx 修复——将预训练梯度混入 RL 目标，使模型不忘记从未被奖励过的下游任务。PPO-ptx 成为标准——Anthropic、DeepMind 和 Meta 都使用某种变体。

### The alignment tax

After RLHF, the model is preferred by humans but regresses on standard benchmarks (SQuAD, HellaSwag, DROP). Ouyang et al. call this the alignment tax and fix it with PPO-ptx: mix pre-training gradients into the RL objective so the model does not forget how to do downstream tasks it was never rewarded for.

```
J_ptx(pi) = J(pi) + gamma * E_{x~D_pretrain} [ log pi(x) ]
```

PPO-ptx became standard. Anthropic, DeepMind, and Meta all use some variant.

> **【拓展：1.3B vs 175B → 对齐独立于能力】** 1.3B InstructGPT 在标注者偏好上约 70% 的时间胜过 175B GPT-3。差距在生产流量隐藏测试提示上更大。两个要点：（1）对齐是与能力不同的轴——175B 有更多能力，1.3B 有更多对齐，标注者偏好对齐的；（2）能力下限由基础模型设定——你不能 RLHF 一个基础模型使其知道它从未见过的事实。

### The result

A 1.3B InstructGPT (SFT + RM + PPO-ptx) is preferred by labelers over the 175B base GPT-3 about 70% of the time. The gap widens on hidden-test prompts from production traffic. Two things to read off this number:

1. Alignment is a different axis from capability. The 175B model had more capability; the 1.3B model had more alignment; labelers preferred the aligned one.
2. The capability floor is set by the base model. You cannot RLHF a base model into knowing facts it never saw.

> **【拓展：Phase 18 后续课程 → 每个都在攻击此管线】** 后续课程的每个批评都在攻击此管线的某个部分：奖励黑客（Lesson 2）攻击阶段 2，DPO（Lesson 3）合并阶段 2 和 3，CAI（Lesson 5）替换人类标注者，谄媚（Lesson 4）展示标注者是有偏信号，对齐伪装（Lesson 9）展示策略可以完全绕过阶段 3。如果不先在脑中有这个管线，就无法理解这些批评。

### Why this is the reference point for Phase 18

Every critique in later lessons — reward hacking (Lesson 2), DPO (Lesson 3), sycophancy (Lesson 4), CAI (Lesson 5), sleeper agents (Lesson 7), alignment faking (Lesson 9) — argues against some part of this pipeline. Reward hacking attacks stage 2. DPO collapses stages 2 and 3. CAI replaces the human labeler. Sycophancy shows the labeler is a biased signal. Alignment faking shows the policy can route around stage 3 entirely. You cannot follow any of these critiques without the pipeline in your head first.

## Use It | 使用方法

`code/main.py` simulates the three stages on toy preference data. The base "policy" is a biased coin over actions {A, B, C}. Stage 1 SFT mimics labeler actions on 200 prompts. Stage 2 fits a Bradley-Terry reward model from 500 pairwise rankings. Stage 3 runs a simplified PPO update with a KL penalty to the SFT policy. You can watch the reward climb, the KL divergence grow, and the policy drift — and you can turn off the KL term to see reward hacking appear inside 50 update steps.

What to look at:

- Reward trajectory with `beta = 0.1` vs `beta = 0.0`.
- KL(pi || pi_SFT) over training steps.
- Final action distribution compared to labeler preference.

## Ship It | 部署上线

This lesson produces `outputs/skill-instructgpt-explainer.md`. Given an RLHF pipeline description or a paper abstract, it identifies which of the three stages is being modified, what loss is being used at each stage, and whether a KL penalty or equivalent regularizer is present.

## Exercises | 练习题

1. Run `code/main.py`. Set `beta = 0.0` and report the action distribution after 200 PPO steps. Explain the mode-seeking behaviour in one paragraph.

2. Modify the reward model to have a +0.5 bias for action B (a simulated reward bug). Run PPO with `beta = 0.1`. Does the KL penalty prevent the policy from exploiting the bias? At what `beta` does exploitation become visible?

3. Read Ouyang et al. (arXiv:2203.02155) Figure 1. Reproduce the labeler-preference curve by running PPO for 1, 5, 20, 100 steps and measuring preference against the SFT model.

4. The paper's Section 4.3 reports a 1.3B InstructGPT beats 175B GPT-3 about 70% of the time. Why would the ratio be higher on hidden production prompts than on the labeler's own prompts?

5. Replace the PPO loss with DPO (Phase 10 · 08) on the same preference data. Compare final policy drift (KL to SFT) and final reward. Which method drifts further at matched reward?

## Key Terms | 关键术语

| Term | What people say | What it actually means |
|------|-----------------|------------------------|
| SFT | "instruction tuning" | Stage 1: cross-entropy fine-tune on prompt-response pairs |
| Reward model | "the RM" | Scalar regressor over (prompt, response) trained with Bradley-Terry on pairwise labels |
| Bradley-Terry | "pairwise preference loss" | -log sigmoid(r_w - r_l); reduces pairwise ranking to binary classification |
| KL penalty | "the regularizer" | `beta * KL(pi \|\| pi_SFT)` — keeps the RL policy near the SFT anchor |
| PPO-ptx | "PPO with pretraining mix" | Adds a fraction of pre-training log-likelihood to the PPO objective to offset the alignment tax |
| Alignment tax | "the RLHF regression" | Post-RLHF drop on standard benchmarks that RLHF did not target |
| Labeler preference | "the ground truth" | Sample of human rankings; the RM is a statistical proxy for this, not for "human values" |

## Further Reading | 延伸阅读

- [Ouyang et al. — Training language models to follow instructions with human feedback (arXiv:2203.02155)](https://arxiv.org/abs/2203.02155) — the InstructGPT paper, foundation for every RLHF pipeline that followed
- [Stiennon et al. — Learning to summarize from human feedback (arXiv:2009.01325)](https://arxiv.org/abs/2009.01325) — the RLHF-for-summarization predecessor
- [Christiano et al. — Deep reinforcement learning from human preferences (arXiv:1706.03741)](https://arxiv.org/abs/1706.03741) — the original preference-based RL formulation
- [Bai et al. — Training a Helpful and Harmless Assistant with RLHF (arXiv:2204.05862)](https://arxiv.org/abs/2204.05862) — Anthropic's HH extension of the InstructGPT pipeline
