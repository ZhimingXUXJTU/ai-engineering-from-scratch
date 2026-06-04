# Capstone Lesson 40: Direct Preference Optimization from Scratch | 直接偏好 优化 结业

> Reward models and PPO are the classical RLHF stack. DPO collapses that stack into a single supervised loss that fits a policy directly against preference pairs. This lesson derives the DPO loss from the reward-difference identity, ships a working reference model plus policy model, computes per-token log-probabilities, and trains a tiny transformer on a preference fixture of chosen and rejected completions. Tests pin the loss math and the gradient direction so you know the implementation matches the paper.

> **【中文解读】** 本节是综合项目——从零实现 DPO（直接偏好优化）。


**类型：** 构建
**语言：** Python (torch, numpy)
**前置知识：** Phase 19 lessons 30-37 (NLP LLM track: tokenizer, embedding table, attention block, transformer body, pre-training loop, checkpointing, generation, perplexity)
**预计时间：** ~90 minutes

## Learning Objectives | 学习目标

- Derive the DPO loss as a sigmoid over a scaled log-ratio difference and connect it to the implicit reward.
- Build a reference model + policy model pair with a frozen reference and a trainable policy.
- Compute sequence-level log-probabilities under both models, masking prompt tokens.
- Train the policy on `(prompt, chosen, rejected)` triples and watch the chosen log-prob rise relative to rejected.
- Pin behaviour with tests on the loss math, the gradient sign, and the reference invariance.

## 问题引入 | 问题

> **【中文解读】** SFT 模型能跟随指令，但输出质量参差不齐。你有一组偏好对：对于同一 prompt，人工标记了一个为 chosen、一个为 rejected。经典 RLHF 管线是两阶段（训练奖励模型 + PPO 优化策略），成本高且复杂。DPO 将两阶段折叠为单一监督损失：不需要显式奖励模型，不需要 PPO，KL 约束 baked into 闭式推导中。

> **【拓展：DPO 在生产中的应用】** DPO (Rafailov et al., 2023) 已成为对齐训练的主流选择。Meta 的 LLaMA-2 Chat 使用 RLHF（PPO），但 LLaMA-3 转向 DPO。Mistral 的 Mixtral-8x7B-Instruct 使用 DPO。Zephyr (HuggingFace) 使用 DPO 在 Mistral-7B 上微调。与 RLHF 相比，DPO 的优势：(1) 不需要奖励模型（省一个完整训练管线）；(2) 训练更稳定（不依赖 on-policy 采样）；(3) 代码量大幅减少。IPO (Azar et al., 2024) 和 KTO (Ethayarajh et al., 2024) 是 DPO 的改进变体。 It follows instructions, but its outputs are uneven; some completions are clear, some are wordy or wrong. You also have a small dataset of preference pairs: for the same prompt, a human marked one completion as chosen and the other as rejected.

The classical RLHF answer is a two-stage pipeline. Train a reward model on the preferences. Optimise the policy against the reward with PPO. This works but is expensive: two models in memory during PPO, KL control to keep the policy near the reference, reward hacking when the reward model is brittle.

DPO replaces both stages with a single supervised loss. The reward model never exists explicitly. The policy is trained directly on the preference pairs, with an explicit KL penalty toward the SFT reference. Same optimal solution under the Bradley-Terry preference model, far less code.

## 核心概念 | 概念

> **【中文解读】** DPO 损失从 Bradley-Terry 偏好模型推导而来。给定 prompt x 和两个完成 y_w（chosen）和 y_l（rejected），人类偏好概率为 sigmoid(r(x, y_w) - r(x, y_l))。通过 KL 约束下的最优策略闭式解，奖励 r 可以用策略与参考模型的 log-prob 差来表示。log Z(x) 项在 chosen 和 rejected 之间抵消。最终损失是四个 log-probability 的 sigmoid 组合，每个样本只需一个标量。

Start from the Bradley-Terry model. Given a prompt `x` and two completions `y_w` (chosen) and `y_l` (rejected), the probability the human prefers `y_w` is

```text
P(y_w > y_l | x) = sigmoid( r(x, y_w) - r(x, y_l) )
```

where `r` is some latent reward function. RLHF first fits `r` from preferences, then trains a policy `pi` to maximise `r` with a KL anchor:

```text
max_pi   E_{x, y~pi} [ r(x, y) ] - beta * KL(pi || pi_ref)
```

The DPO derivation observes that the optimal policy `pi*` under this objective has a closed form in terms of `r`:

```text
pi*(y | x) = (1/Z(x)) * pi_ref(y | x) * exp( r(x, y) / beta )
```

Re-arrange for `r`:

```text
r(x, y) = beta * ( log pi*(y | x) - log pi_ref(y | x) ) + beta * log Z(x)
```

The `log Z(x)` term is the same for both `y_w` and `y_l` (it depends on `x`, not `y`), so it cancels when you compute the preference difference:

```text
r(x, y_w) - r(x, y_l) = beta * ( log pi_theta(y_w|x) - log pi_ref(y_w|x)
                                - log pi_theta(y_l|x) + log pi_ref(y_l|x) )
```

Substitute into the Bradley-Terry sigmoid and take negative log likelihood over preference pairs:

```text
L_DPO(theta) = - E_{(x, y_w, y_l)} [
  log sigmoid( beta * ( log pi_theta(y_w|x) - log pi_ref(y_w|x)
                       - log pi_theta(y_l|x) + log pi_ref(y_l|x) ) )
]
```

This is the loss. It is a sigmoid over a single scalar per example, computed from four log-probabilities. No separate reward model. No PPO. No KL term in the loss; the KL constraint is baked into the closed-form derivation.

```mermaid
flowchart LR
  Triple[(x, y_w, y_l)] --> Pol[policy<br/>pi_theta]
  Triple --> Ref[reference<br/>pi_ref, frozen]
  Pol --> LWP[log pi_theta y_w]
  Pol --> LLP[log pi_theta y_l]
  Ref --> LWR[log pi_ref y_w]
  Ref --> LLR[log pi_ref y_l]
  LWP --> Diff[beta * log-ratio diff]
  LLP --> Diff
  LWR --> Diff
  LLR --> Diff
  Diff --> Sig[sigmoid]
  Sig --> NLL[- log sigmoid]
```

## The Sign of the Gradient

A useful sanity check before any training run. Take the gradient with respect to `log pi_theta(y_w | x)`:

```text
d L_DPO / d log pi_theta(y_w | x) = - beta * (1 - sigmoid(z))
```

where `z` is the argument to the sigmoid. This is negative for all `z`, which means: increasing the policy's log-probability of the chosen completion decreases the loss. Symmetrically, the gradient with respect to `log pi_theta(y_l | x)` is positive: increasing the rejected log-probability increases the loss. Training pushes the chosen up and the rejected down. The reference is frozen; it does not move.

## The Data

> **【拓展：偏好数据收集与 DPO 变体】** 本课的 12 个偏好三元组是教育性简化。生产级 DPO 需要数万到数十万偏好对。数据来源：1）人类标注（Anthropic 的 HH-RLHF 数据集）；2）AI 反馈（RLAIF，用 GPT-4 标注）；3）隐式反馈（KTO 只需 binary good/bad 标签，不需要成对比较）。UltraFeedback (Cui et al., 2024) 提供了 64K 指令的偏好数据，是开源社区最常用的 DPO 训练数据。

Twelve preference triples ship with the lesson. Each is `(prompt, chosen, rejected)`. The chosen completion is short and precise. The rejected is wordy, off-topic, or wrong. The pairs cover the same task families as lesson 39 (capital, arithmetic, list) so a policy that started from an SFT base has a reasonable starting point.

The fixture is intentionally small. DPO works on tens of thousands of pairs in production; here, the point is that the loss math and the loop run end-to-end on a tiny dataset and the chosen-versus-rejected log-prob gap visibly grows.

## Reference Invariance

A DPO implementation has to handle the reference model carefully. The reference is the SFT model frozen in place. Three properties have to hold:

- The reference parameters never receive gradients.
- The reference log-probabilities never change between epochs.
- The policy starts from the same weights as the reference. (The optimal `theta` is the reference plus a learned update; initialising the policy as a copy of the reference is the well-defined start.)

The implementation enforces these by:

- Wrapping the reference in `torch.no_grad()` during forward passes.
- Setting `requires_grad=False` on every reference parameter.
- Constructing the policy via `policy.load_state_dict(reference.state_dict())` after the reference is built.

## 架构 | 架构

```mermaid
flowchart TD
  P[(preference triples)] --> Tok[InstructionTokenizer]
  Tok --> DS[PreferenceDataset]
  DS --> DL[DataLoader<br/>per-row decode]
  DL --> Pol[Policy TinyGPT]
  DL --> Ref[Reference TinyGPT<br/>frozen]
  Pol --> LP[log pi for chosen and rejected]
  Ref --> LR[log pi_ref for chosen and rejected]
  LP --> Loss[DPO loss<br/>sigmoid * log-ratio diff]
  LR --> Loss
  Loss --> Bwd[backward]
  Bwd --> Opt[Adam optimiser]
```

The model is the same TinyGPT used in lesson 39 (decoder-only, causal, byte tokeniser). The reference and policy share the architecture; the policy's weights drift from the reference under training while the reference stays fixed.

## 你将构建什么

The implementation is one `main.py` plus tests.

1. `InstructionTokenizer`: byte tokeniser with `INST` and `RESP` specials. Same shape as lesson 39.
2. `TinyGPT`: decoder-only transformer. Same shape as lesson 39 so the lesson is self-contained even if you skipped 39.
3. `make_preferences`: returns twelve `(prompt, chosen, rejected)` triples.
4. `sequence_log_prob`: given the model, a prompt prefix, and a completion, returns the sum of next-token log-probabilities over the completion (no prompt-position contribution).
5. `dpo_loss`: takes the four log-probabilities and `beta`, returns the per-example loss tensor and the implicit reward delta for logging.
6. `train_dpo`: per-epoch loop that computes chosen and rejected log-probs under policy and reference, applies the loss, and steps Adam.
7. `evaluate_margins`: returns the mean chosen-rejected log-probability margin under the policy at any point.
8. `run_demo`: builds reference and policy from a small warm-up pretrain, copies weights, trains for thirty steps, prints the per-step loss and margin, and exits zero on success.

## Why DPO works

> **【中文解读】** DPO 在 Bradley-Terry 偏好模型下与 RLHF 数学等价。隐式奖励 r(x,y) = beta * (log pi(y|x) - log pi_ref(y|x)) 从偏好中可辨识到仅差一个 x 的函数，后者在差分中抵消。KL 约束是结构性强制的：策略偏离参考使 log-ratio 增大，sigmoid 饱和抑制梯度，防止策略跑太远。参考模型是安全网。

DPO is mathematically equivalent to RLHF under the Bradley-Terry preference model, up to the parameterisation of the reward. The implicit reward `r(x, y) = beta * (log pi(y|x) - log pi_ref(y|x))` is identifiable from preferences up to a function of `x`, which cancels in the difference. The closed-form policy lets you skip the explicit reward model. The KL constraint is enforced structurally: any deviation of `pi` from `pi_ref` makes the log-ratio larger, and the sigmoid saturates, which damps the gradient when the policy moves too far. The reference is your safety net.

## Stretch goals

- Add a length normalisation to the log-probability sum: divide by completion length. Length bias is a known DPO failure mode where the model preferentially chooses shorter completions because their log-probabilities are larger in absolute terms.
- Add the IPO variant of the loss: replace the sigmoid + log with `(z - 1)^2`. Compare convergence on the fixture.
- Add a label-smoothing parameter that interpolates between the hard chosen-rejected label and a uniform 0.5.
- Replace the reference with a smaller cheaper model (knowledge distillation flavour).

The implementation gives you the loss, the reference invariance, and the training loop. The math is the lesson. The code makes the math concrete.
