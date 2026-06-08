# Scalable Oversight and Weak-to-Strong Generalization | 可扩展监督

> Burns et al. (OpenAI Superalignment, "Weak-to-Strong Generalization", 2023) proposed a proxy for the superalignment problem: fine-tune a strong model using labels produced by a weaker model. If the strong model generalizes correctly from imperfect weak supervision, current human-scale alignment methods may extend to superhuman systems. Scalable oversight and W2SG are complementary. Scalable oversight (debate, recursive reward modeling, task decomposition) increases the overseer's effective capability so it can keep up with the model under oversight. W2SG ensures the strong model generalizes correctly from whatever imperfect supervision the overseer provides. Debate Helps W2SG (arXiv:2501.13124, January 2025) combines them.

> **【中文解读】** 本节介绍了可扩展监督——从弱到强的 AI 安全评估方法。Burns 等人（OpenAI 超级对齐, 2023）提出超级对齐问题的代理：用弱模型产生的标签微调强模型。如果强模型从完美弱监督中正确泛化，当前人类规模的对齐方法可能扩展到超人系统。

> **【拓展：弱到强泛化 → 超级对齐路径】** PGR（Performance Gap Recovered）= (微调后-弱)/(上限-弱)。PGR 为 1.0 意味着弱监督完全弥合了差距；PGR 为 0 意味着弱监督没有帮助。Burns 等人发现 PGR 在 NLP、国际象棋谜题和奖励建模任务上一致为正（约 20%-80%），强模型利用预训练先验"理解"了意图任务，超越了弱监督者的错误。

**Type:** Learn | **类型:** 学习
**Languages:** Python (stdlib, W2SG gap simulator) | **语言:** Python（标准库，W2SG 差距模拟器）
**Prerequisites:** Phase 18 · 01 (instruction-following), Phase 18 · 10 (AI Control), Phase 09 (RL foundations) | **前置知识:** Phase 18 · 01 (指令遵循), Phase 18 · 10 (AI 控制), Phase 09 (RL 基础)
**Time:** ~60 minutes | **时间:** ~60 分钟

## Learning Objectives | 学习目标

- Define scalable oversight and weak-to-strong generalization and explain how they are complementary.
- Describe the Burns et al. 2023 experimental setup: fine-tune GPT-4 using labels from GPT-2.
- Explain the performance gap recovered (PGR) metric and what it measures.
- State the three major scalable-oversight mechanisms (debate, recursive reward modeling, task decomposition) and one strength of each.

## The Problem | 问题引入

Every alignment technique so far in Phase 18 assumes the overseer can evaluate the model's behaviour. When the model is superhuman, the overseer is the weak link. The superalignment question: can a weaker supervisor reliably produce a stronger, aligned model?

> Phase 18 中到目前为止的每种对齐技术都假设监督者可以评估模型的行为。当模型是超人的，监督者就是薄弱环节。超级对齐问题：较弱的监督者能否可靠地产生更强的、对齐的模型？

Burns et al. reduce this to an operationalized empirical setup: supervise strong with weak, measure how much of the strong model's capability survives the weak supervision. This is not a solution to superalignment — it is a proxy that lets us measure progress.

> Burns 等人将其简化为操作化的实证设置：用弱监督强，测量强模型的能力有多少在弱监督下存活。这不是超级对齐的解决方案——它是让我们衡量进展的代理。

## The Concept | 核心概念

> **【中文解读】** Burns 等人实验设置：弱模型 GPT-2 级别，强模型 GPT-4 级别，目标是强模型在金标签上的上限。流程：获取弱模型零样本预测 → 在弱标签上微调强模型 → 测量强微调模型准确率。差距指标 PGR = (微调后-弱)/(上限-弱)，1.0 = 弱监督完全弥合差距，0 = 弱监督没有帮助。

### W2SG: the Burns et al. setup

- Weak model: GPT-2 class.
- Strong model: GPT-4 class.
- Target: strong GPT-4 ceiling on the task.

Procedure:
1. Get weak model's zero-shot predictions on a task.
2. Fine-tune the strong model on weak-labeled data.
3. Measure the strong fine-tuned model's accuracy.

Baselines: weak model's own accuracy, strong model's supervised ceiling on gold labels.

Gap metric: Performance Gap Recovered (PGR) = (fine-tuned - weak) / (ceiling - weak). PGR of 1.0 means weak supervision fully closes the gap; PGR of 0 means weak supervision did not help.

### Burns et al. empirical findings

Across NLP, chess-puzzle, and reward-modeling tasks, PGR was consistently positive: the strong model generalized beyond the weak supervisor's mistakes. Task-specific PGR varied from ~20% to ~80%. The strong model "understands" the intended task from imperfect labels, filling in with its pre-trained priors.

Limitations Burns et al. note:
- The weak-to-strong gap here is capability, not alignment. The weak model is aligned; a truly superhuman model might be aligned by a human but with a much larger capability gap.
- The strong model's generalization may be more about task priors than about recovering ground-truth intent.
- Eliciting the strong model's latent knowledge is the real problem; PGR measures a specific operationalization.

> **【拓展：三种可扩展监督机制 → 辩论/递归奖励建模/任务分解】** 辩论（Irving 等人 2018）：两个 U 实例争论相反立场，弱评判者决定。递归奖励建模（Leike 等人 2018）：U 帮助人类训练 U+1 的奖励模型，监督者的有效能力随模型增长。任务分解（Christiano 等人 2018）：将硬任务分解为人类可检查的子任务，递归执行。每种机制都假设了关于任务结构或中间组件对齐的某些东西。

### Scalable oversight: three mechanisms

- **Debate (Irving et al. 2018).** Two instances of U argue opposite sides; the weak judge decides. The assumption: finding a convincing true answer is easier than finding a convincing false answer. Recent 2024-2025 work (Khan et al., Michael et al.) shows debate sometimes helps and sometimes does not, and whether it helps depends on task structure.
- **Recursive Reward Modeling (Leike et al. 2018).** U helps the human train the reward model for U+1. The overseer's effective capability grows with the model's.
- **Task Decomposition (Christiano, Shlegeris, Amodei 2018).** Decompose a hard task into sub-tasks the human can check, recursively. Assumes decomposability.

Each mechanism assumes something about the structure of the task or the alignment of the intermediate components.

### Why scalable oversight and W2SG are complementary

Scalable oversight increases the overseer's effective signal quality.
W2SG closes the gap from whatever imperfect signal the overseer can provide.

Lang et al. — Debate Helps Weak-to-Strong Generalization (arXiv:2501.13124) combines them: a debate protocol provides better weak labels, and the strong model is trained on those labels. Reported PGR gains on NLP tasks.

> **【中文解读】** 组织戏剧：OpenAI 的超级对齐团队在 2024 年 5 月 Jan Leike 离职加入 Anthropic 后解散。但研究议程（可扩展监督、弱到强泛化、自动化对齐研究）在 Anthropic 和学术实验室继续——MATS（Lesson 28）、Redwood（Lesson 10）、Apollo（Lesson 8）、METR（Lesson 28）。组织结构变了，研究问题没变。

### The organizational drama

OpenAI's Superalignment team dissolved in May 2024 after Jan Leike's departure to Anthropic. The agenda (scalable oversight, W2SG, automated alignment research) continued at Anthropic and at academic labs — MATS (Lesson 28), Redwood (Lesson 10), Apollo (Lesson 8), METR (Lesson 28). The organizational structure changed; the research questions did not.

### Where this fits in Phase 18

Lessons 6-10 describe the threat and the defensive paradigm under the assumption U is untrustworthy. Lesson 11 is the offensive paradigm: make the overseer strong enough to verify U's alignment. Lessons 12-16 then turn to the practical tooling of adversarial evaluation.

> **【拓展：辩论帮助弱到强泛化 → 2025 组合】** Lang 等人（arXiv:2501.13124, 2025 年 1 月）将可扩展监督和弱到强泛化结合：辩论协议提供更好的弱标签，强模型在这些标签上训练。报告在 NLP 任务上的 PGR 提升。这验证了两种方法是互补的——可扩展监督增加监督者的有效信号质量，弱到强泛化闭合从任何信号中恢复的差距。

## Use It | 用框架实现

`code/main.py` simulates a W2SG fine-tune on a synthetic task. Weak labeler has 70% accuracy with structured errors; strong model has 95% ceiling on gold labels. You fine-tune the strong model on weak labels, measure PGR, and compare to strong-on-gold and weak-alone.

## Ship It | 产出物

This lesson produces `outputs/skill-w2sg-pgr.md`. Given an oversight setup description, it identifies the weak supervisor, the strong model, the supervision quality, and computes (or requests) PGR. It flags whether the claim is "weak can supervise strong" or "weak + oversight mechanism can supervise strong."

## Exercises | 练习题

1. Run `code/main.py`. Report PGR for weak_accuracy = 0.60, 0.70, 0.80. Explain the shape of the PGR curve.

2. Modify the weak labeler to have structured error (e.g., always wrong on a specific input class). Does PGR increase, decrease, or stay the same? Explain.

3. Read Burns et al. 2023 Section 4.3 (NLP tasks). Reproduce the "confidence auxiliary loss" intuition: when the strong model is more confident than the weak labels, who wins?

4. Design a scalable-oversight protocol that combines debate and task decomposition for a software-engineering task. Name one failure mode of each component and explain how the combination addresses or fails to address each.

5. Articulate what would falsify the "weak-to-strong generalization is a viable path to superalignment" claim. Be specific about the empirical signature you would need to see.

## Key Terms | 关键术语

| Term | What people say | What it actually means |
|------|-----------------|------------------------|
| Scalable oversight | "making the overseer stronger" | Mechanisms that increase an overseer's ability to evaluate a more-capable model |
| W2SG | "weak supervises strong" | Fine-tuning a strong model on weak labels and measuring the capability recovered |
| PGR | "performance gap recovered" | (fine-tuned - weak) / (ceiling - weak); 1.0 = fully closed, 0 = no help |
| Debate | "two U instances argue" | Scalable oversight mechanism where a weak judge picks between two U defenders |
| RRM | "recursive reward modeling" | U helps train the reward model for U+1; overseer capability tracks U |
| Task decomposition | "sub-tasks the human checks" | Break a hard task into sub-tasks the human can verify, recursively |
| Superalignment | "aligning superhuman AI" | The research agenda concerned with aligning models the human cannot directly evaluate |

## Further Reading | 延伸阅读

- [Burns et al. — Weak-to-Strong Generalization (OpenAI 2023)](https://openai.com/index/weak-to-strong-generalization/) — the W2SG paper
- [Irving, Christiano, Amodei — AI safety via debate (arXiv:1805.00899)](https://arxiv.org/abs/1805.00899) — the debate mechanism
- [Leike et al. — Scalable agent alignment via reward modeling (arXiv:1811.07871)](https://arxiv.org/abs/1811.07871) — recursive reward modeling
- [Khan et al. — Debating with More Persuasive LLMs Leads to More Truthful Answers (arXiv:2402.06782)](https://arxiv.org/abs/2402.06782) — 2024 empirical study of debate with stronger debaters
- [Lang et al. — Debate Helps Weak-to-Strong Generalization (arXiv:2501.13124)](https://arxiv.org/abs/2501.13124) — 2025 combination of debate + W2SG
