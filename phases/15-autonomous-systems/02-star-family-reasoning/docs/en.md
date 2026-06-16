# STaR, V-STaR, Quiet-STaR — Self-Taught Reasoning | STaR 系列自我推理方法

> The smallest possible self-improvement loop sits inside the rationale. A model generates a chain of thought, keeps the ones that land on correct answers, and fine-tunes on those. That is STaR. V-STaR adds a verifier so inference-time selection is better. Quiet-STaR pushes the rationale down to every token. All three work. None of them are magic — the loop preserves any shortcut that happened to reach the right answer.

> **【中文解读】** 最小的自我改进循环隐藏在推理过程中：模型生成思维链，保留正确答案的推理过程，在这些数据上微调。这就是 STaR。V-STaR 添加验证器改善推理时选择。Quiet-STaR 将推理下沉到每个 token。三者都有效，但都不是魔法——循环保留了碰巧得到正确答案的任何捷径。

> **【拓展：STaR → OpenAI o1/o3 的自我改进】** STaR 系列是"自我博弈"训练的核心思路——模型用自己的推理输出来训练自己。OpenAI o1/o3 系列模型背后的强化学习训练就采用了类似思路：生成多个推理路径，选择正确的，用它们来改进模型。这是实现 AI 自我改进闭环的关键技术。

**Type:** Learn | **类型:** 学习
**Languages:** Python (stdlib, bootstrap-loop simulator) | **语言:** Python (标准库，bootstrap 循环模拟器)
**Prerequisites:** Phase 13 · 01-03 (Reasoning and CoT), Phase 15 · 01 (long-horizon framing) | **前置知识:** Phase 13 · 01-03（推理与 CoT），Phase 15 · 01（长程框架）
**Time:** ~60 minutes | **时间:** ~60 分钟

> 🔗 **【前置】** 学本节前请先掌握：Phase 13·01-03（CoT 思维链）、Phase 11·08（SFT 监督微调）、Phase 15·01（长程 Agent 框架）。STaR 是"自蒸馏 + 推理增强"的最小闭环。
> 💡 **【类比】** STaR = "学生自我批改"。普通学习 = 老师改作业学生订正（人工标注推理过程）；STaR = 学生写推理→对答案→对的推理保留并自己再练一遍（自我生成训练数据）。问题是：有时推理过程是错的但答案碰巧对了（蒙对），STaR 会强化这种"蒙对"的推理——V-STaR 加一个判官（verifier）筛掉错误推理。
> ⚠️ **【易错点】** STaR 训练时只看"答案是否正确"会强化"捷径推理"（错误过程但正确结果）。修复：用过程奖励（PRM，Phase 13·03）替代结果奖励，每一步推理都打分；或用 V-STaR 加 verifier 检查推理质量。

## The Problem | 问题引入引入

The straightforward way to teach a model to reason is to collect human-written reasoning traces. That is expensive, slow, and bounded by how much high-quality chain-of-thought humans are willing to write.

> 教模型推理的直接方法是收集人类书写的推理轨迹。这既昂贵又缓慢，还受限于人类愿意写多少高质量思维链。

STaR (Self-Taught Reasoner, Zelikman et al., 2022) asks: what if the model writes its own rationales and grades them against known answers? The loop is:

> STaR（自我教学推理器，Zelikman 等人，2022）提出：如果模型自己编写推理过程并与已知答案对照评分会怎样？循环是：


> **【中文解读】** Star 家族推理技术（STaR、Quiet-STaR、ReST、ReST-EM）通过迭代式自我训练提升 LLM 推理能力。核心思想：让模型生成推理轨迹，过滤高质量轨迹，用这些轨迹微调模型，循环迭代。这是 OpenAI o1/o3 系列和 Anthropic Extended Thinking 的技术基础。

1. Sample a reasoning trace plus answer.
2. If the final answer is correct, keep the trace.
3. Fine-tune on the kept traces.
4. Repeat.

It works. GSM8K and CommonsenseQA both improved without new human annotation. But the loop has a built-in bias: any rationale that produced the right answer is retained, regardless of whether the reasoning itself was sound. V-STaR (Hosseini et al., 2024) patches this with a learned verifier; Quiet-STaR (Zelikman et al., 2024) generalizes the idea to per-token internal rationales.

> 它有效。GSM8K 和 CommonsenseQA 在没有新人类标注的情况下都有提升。但循环有一个内置偏差：任何产生正确答案的推理过程都被保留，无论推理本身是否合理。V-STaR（Hosseini 等人，2024）通过学习的验证器修补了这个问题；Quiet-STaR（Zelikman 等人，2024）将这个想法推广到每个 token 的内部推理。

## The Concept | 核心概念

### STaR: bootstrap on what worked

Start from a base model with some weak reasoning ability. On each training problem, sample a rationale plus answer. If the answer matches the label, keep the (problem, rationale, answer) triple. Fine-tune the model on the kept set. Repeat.

> 从一个具有较弱推理能力的基础模型开始。在每个训练问题上，采样一个推理过程加答案。如果答案与标签匹配，保留（问题、推理过程、答案）三元组。在保留的集合上微调模型。重复。

One twist matters. If the model can never get a problem right, the loop cannot learn on it. STaR adds **rationalization**: for problems the model fails, inject the correct answer as a hint and re-prompt the model to produce a rationale that leads to it. Rationalized rationales are added to the training set.

> 一个关键的转折。如果模型永远无法正确回答一个问题，循环就无法从中学习。STaR 添加了**合理化**：对于模型失败的问题，将正确答案作为提示注入，重新提示模型产生导向该答案的推理过程。合理化的推理被添加到训练集中。

Result in the original paper (Zelikman et al., 2022): a GPT-J base model improved on GSM8K from 5.8% to 10.7% through repeated STaR rounds with rationalization — about 5 percentage points absolute. On CommonsenseQA, STaR-trained GPT-J 6B reached 72.5%, comparable to a fine-tuned GPT-3 175B (~73%) — a roughly 30x larger model trained on hand-annotated rationales.

> 原始论文的结果（Zelikman 等人，2022）：GPT-J 基础模型通过带合理化的重复 STaR 轮次，在 GSM8K 上从 5.8% 提升到 10.7%——约 5 个百分点的绝对提升。在 CommonsenseQA 上，STaR 训练的 GPT-J 6B 达到 72.5%，可与微调的 GPT-3 175B（约 73%）相比——后者是用手工标注推理训练的大约 30 倍大的模型。

### V-STaR: train a verifier with DPO

STaR throws away incorrect rationales. Hosseini et al. (2024) observed those are also data: every pair of (rationale, "is this correct") can train a verifier. They use Direct Preference Optimization over both correct and incorrect solutions to build a ranker. At inference time, sample N rationales and pick the verifier's top choice.

> STaR 丢弃不正确的推理。Hosseini 等人（2024）观察到这些也是数据：每对（推理过程，"这是否正确"）都可以训练验证器。他们使用直接偏好优化（DPO）在正确和错误的解决方案上构建排名器。在推理时，采样 N 个推理并选择验证器排名最高的。

Reported delta: +4 to +17 percentage points over prior self-improvement baselines on GSM8K and MATH, with most of the gain coming from using the verifier for inference-time selection rather than for additional generator fine-tuning.

> 报告的提升：在 GSM8K 和 MATH 上比先前的自我改进基线提升 +4 到 +17 个百分点，大部分提升来自推理时选择验证器而非额外的生成器微调。

### Quiet-STaR: per-token internal rationales

Zelikman et al. (2024) asked: what if the model learns to generate a short internal rationale at every token position, not just between problem and answer? Quiet-STaR trains a model to emit a hidden "thought" before each predicted token, then mixes the thought-aware prediction with the baseline prediction via a learned weight.

> Zelikman 等人（2024）提出：如果模型学会在每个 token 位置生成一个简短的内部推理，而不仅仅是在问题和答案之间呢？Quiet-STaR 训练模型在每个预测 token 之前发出一个隐藏的"思考"，然后通过学习的权重将思考感知的预测与基线预测混合。

Result: Mistral 7B gained absolute zero-shot improvements on GSM8K from 5.9% to 10.9% and CommonsenseQA from 36.3% to 47.2% without task-specific fine-tuning. The model learned "when to think" — hard tokens get longer internal rationales; easy ones get almost none.

> 结果：Mistral 7B 在 GSM8K 上零样本绝对提升从 5.9% 到 10.9%，在 CommonsenseQA 上从 36.3% 到 47.2%，无需任务特定的微调。模型学会了"何时思考"——困难的 token 获得更长的内部推理；简单的几乎不获得。

### Why all three share a safety concern

All three methods use the final answer as the gradient signal. A rationale that reaches the right answer via flawed reasoning — exploiting a shortcut, guessing, or using a non-generalizing pattern — gets positively reinforced. On in-distribution problems the shortcut works. On out-of-distribution problems it breaks silently.

> 三种方法都使用最终答案作为梯度信号。通过有缺陷的推理达到正确答案的推理过程——利用捷径、猜测或使用不可泛化的模式——被正面强化。在分布内问题上捷径有效。在分布外问题上它静默地失败。

V-STaR's verifier mitigates by learning to rank rationales, but the verifier is trained on the same label set. It can learn to prefer well-formatted wrong reasoning over honest uncertainty. The safer design is to combine STaR-style data with (a) process-supervised reward models (rewarding intermediate steps, not just answers) and (b) held-out OOD evaluation that breaks simple shortcuts.

> V-STaR 的验证器通过学习对推理进行排名来缓解，但验证器是在相同的标签集上训练的。它可能学会偏好格式良好但错误的推理而非诚实的不确定性。更安全的设计是将 STaR 风格的数据与（a）过程监督奖励模型（奖励中间步骤，不仅仅是答案）和（b）打破简单捷径的保留 OOD 评估相结合。

### Comparison

| Method | Training signal | Inference cost | Data waste | Known failure mode |
|---|---|---|---|---|
| 方法 | 训练信号 | 推理成本 | 数据浪费 | 已知失败模式 |
| STaR | keep (rationale, answer) if correct | 1x | discards all incorrect rationales | shortcut rationales |
| STaR | 正确时保留（推理，答案） | 1x | 丢弃所有不正确的推理 | 捷径推理 |
| STaR + rationalization | above + correct-answer hinted retries | 1x | less | rationalized rationales may be implausible |
| STaR + 合理化 | 上述 + 正确答案提示重试 | 1x | 较少 | 合理化的推理可能不可信 |
| V-STaR | STaR + DPO verifier from both classes | Nx (best-of-N) | minimal | verifier can reinforce confident wrongness |
| V-STaR | STaR + 两类 DPO 验证器 | Nx（N 中选优） | 最少 | 验证器可能强化自信的错误 |
| Quiet-STaR | per-token rationale + mixing weight | 1.5-3x | minimal | still answer-conditioned gradient |
| Quiet-STaR | 每 token 推理 + 混合权重 | 1.5-3x | 最少 | 仍是答案条件梯度 |

### Where this sits in the 2026 stack

STaR is old. But the pattern reappears everywhere in 2025-2026. RL on verifiable math problems (DeepSeek-R1, Kimi-k1.5, o1) is STaR's answer-conditioned gradient signal, scaled up. Process reward models (Lightman et al., 2023; OpenAI's "Let's verify step by step") are the process-supervised alternative. AlphaEvolve (Lesson 3) is STaR for code, with a program evaluator instead of a label. Darwin Godel Machine (Lesson 4) is STaR for the agent scaffolding itself.

> STaR 很老了。但这个模式在 2025-2026 年到处出现。在可验证数学问题上的 RL（DeepSeek-R1、Kimi-k1.5、o1）是 STaR 的答案条件梯度信号的放大版。过程奖励模型（Lightman 等人，2023；OpenAI 的"逐步验证"）是过程监督的替代方案。AlphaEvolve（第 3 课）是代码的 STaR，用程序评估器代替标签。Darwin Godel Machine（第 4 课）是 Agent 脚手架本身的 STaR。

Understanding STaR makes all of these click. It is the minimum-viable self-improvement loop.

> 理解 STaR 让所有这些都说得通。它是最小可行的自我改进循环。

## Use It | 用框架实现

`code/main.py` runs a simulated STaR loop on a toy arithmetic task. You can watch:

- How accuracy climbs over bootstrap rounds.
  中文翻译：准确率如何在 bootstrap 轮次中攀升。
- How shortcuts sneak in: the simulator includes a "lazy" rationale class that gets the right answer 40% of the time but generalizes badly. Watch whether STaR keeps them.
  中文翻译：捷径如何潜入——模拟器包含一个"懒惰"推理类，40% 的时间得到正确答案但泛化很差。观察 STaR 是否保留它们。
- How a verifier (V-STaR style) helps at inference but cannot fully prune shortcuts introduced during training.
  中文翻译：验证器（V-STaR 风格）如何在推理时帮助但不能完全修剪训练期间引入的捷径。

## Ship It | 产出物

`outputs/skill-star-loop-reviewer.md` helps you audit a proposed self-taught-reasoning pipeline before you train on it.

> `outputs/skill-star-loop-reviewer.md` 帮助你在训练之前审计提议的自我教学推理管道。

## Exercises | 练习题

1. Run the simulator. Set the shortcut frequency to zero, then to 0.4. How much does final accuracy diverge between the two runs, even though both hit >90% on the training distribution?
   中文翻译：两次运行之间最终准确率分歧多少，即使两者在训练分布上都达到 >90%？

2. Add a held-out OOD test to the simulator. Draw problems from a different distribution and evaluate the bootstrapped model on both in-distribution and OOD sets. Quantify the gap.
   中文翻译：量化差距。

3. Read the Quiet-STaR paper (arXiv:2403.09629) Section 3. Explain the "end-of-thought" token and the mixing-weight head in three sentences each.
   中文翻译：用三句话分别解释"思考结束"token 和混合权重头。

4. Compare STaR's keep-if-correct filter to a process-supervised alternative that rewards each rationale step independently. Identify the labelling cost difference and the plausible quality difference.
   中文翻译：识别标注成本差异和质量差异。

5. Design one evaluation that would catch shortcut rationales in a deployed model. It does not have to be perfect — it has to break the simplest shortcuts a STaR loop would reinforce.
   中文翻译：它只需打破 STaR 循环会强化的最简单捷径。

## Key Terms | 术语速查表

| Term | What people say | What it actually means |
|---|---|---|
| 术语 | 通俗说法 | 实际含义 |
| STaR | "Self-Taught Reasoner" | Fine-tune on model-generated rationales that land correct answers; repeat |
| STaR | "自我教学推理器" | 在模型生成的正确推理上微调；重复 |
| Rationalization | "Hinted retry" | Inject the correct answer and re-prompt for a rationale |
| 合理化 | "提示重试" | 注入正确答案重新提示推理 |
| V-STaR | "Verifier STaR" | DPO-train a verifier on both correct and incorrect rationales |
| V-STaR | "验证器 STaR" | DPO 训练验证器用于推理时选择 |
| Quiet-STaR | "Per-token rationales" | Generate hidden thoughts at every token position; mix with baseline |
| Quiet-STaR | "每 token 推理" | 在每个 token 位置生成隐藏思考；与基线预测混合 |
| Answer-conditioned gradient | "Outcome-based signal" | The training loop rewards final answers, not reasoning steps |
| 答案条件梯度 | "基于结果的信号" | 训练循环奖励最终答案，而非推理步骤 |
| Process reward model | "Step-level verifier" | Reward model trained on per-step correctness, not outcome |
| 过程奖励模型 | "步骤级验证器" | 在每步正确性上训练的奖励模型 |
| Shortcut rationale | "Right answer, wrong reasoning" | A rationale that reaches the label via a non-generalizing pattern |
| 捷径推理 | "正确答案，错误推理" | 通过不可泛化模式达到标签的推理 |

## Further Reading | 延伸阅读

- [Zelikman et al. (2022). STaR: Bootstrapping Reasoning With Reasoning](https://arxiv.org/abs/2203.14465) — the original paper.
  中文翻译：原始论文。
- [Hosseini et al. (2024). V-STaR: Training Verifiers for Self-Taught Reasoners](https://arxiv.org/abs/2402.06457) — adds a DPO verifier for inference-time selection.
  中文翻译：添加 DPO 验证器用于推理时选择。
- [Zelikman et al. (2024). Quiet-STaR: Language Models Can Teach Themselves to Think Before Speaking](https://arxiv.org/abs/2403.09629) — per-token internal rationales.
  中文翻译：每 token 内部推理。
- [Lightman et al. (2023). Let's Verify Step by Step](https://arxiv.org/abs/2305.20050) — process reward models, the alternative gradient signal.
  中文翻译：过程奖励模型，替代梯度信号。
- [DeepSeek-R1 paper (arXiv:2501.12948)](https://arxiv.org/abs/2501.12948) — RL on verifiable tasks, STaR scaled to frontier training.
  中文翻译：可验证任务上的 RL，STaR 扩展到前沿训练。
