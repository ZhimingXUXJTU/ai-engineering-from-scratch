# Reflexion: Verbal Reinforcement Learning | Reflexion：语言强化学习

> Gradient-based RL needs thousands of trials and a GPU cluster to fix a failure mode. Reflexion (Shinn et al., NeurIPS 2023) does it in natural language: after each failed trial, the agent writes a reflection, stores it in episodic memory, and conditions the next trial on that memory. This is the pattern behind Letta's sleep-time compute, Claude Code's CLAUDE.md learnings, and pro-workflow's learn-rule.

> **【中文解读】** 基于梯度的 RL 需要数千次试验和 GPU 集群。Reflexion 用自然语言实现自我改进：每次失败后，Agent 写一段反思存入情景记忆，下一次尝试时参考这些记忆。这正是 Letta 的 sleep-time compute、Claude Code 的 CLAUDE.md 学习机制背后的模式。

> **【拓展：Reflexion → Claude Code 的自我学习】** Claude Code 的 CLAUDE.md 机制本质上就是 Reflexion 的变体——Agent 在工作过程中积累经验教训，存储为规则文件，后续会话自动加载。这也是"从错误中学习"在生产环境中最常见的实现方式。

**Type:** Build
**Languages:** Python (stdlib)
**Prerequisites:** Phase 14 · 01 (Agent Loop), Phase 14 · 02 (ReWOO)
**Time:** ~60 minutes

## Learning Objectives | 学习目标

- Name the three components of Reflexion (Actor, Evaluator, Self-Reflector) and the role of episodic memory.
- Implement a stdlib Reflexion loop with binary evaluator, reflection buffer, and fresh re-attempts.
- Choose between scalar, heuristic, and self-evaluated feedback sources for a given task.
- Explain why verbal reinforcement catches errors that gradient-based RL would need thousands of trials to fix.

> **【中文解读】** 学习 Reflexion 的三个组件：Actor（执行器）、Evaluator（评估器）、Self-Reflector（自我反思器），以及情景记忆的作用。核心洞察：自然语言足以承载"从失败中学到了什么"，不需要梯度更新。

## The Problem | 问题

An agent fails a task. In standard RL you would run thousands more trials, compute gradients, update weights. Expensive, slow, and most production agents do not have a training budget for every failure.

Reflexion (Shinn et al., arXiv:2303.11366) asks a different question: what if the agent just thought about why it failed and tried again with that thought in its prompt? No weight updates. No gradient. Just natural language stored between trials.

The result: on ALFWorld it beats ReAct and other non-fine-tuned baselines. On HotpotQA it improves over ReAct. On code generation (HumanEval/MBPP) it sets state of the art at the time. All without a single gradient step.

> **【中文解读】** Agent 失败时，传统 RL 需要数千次试验和梯度更新。Reflexion 的思路是：让 Agent 思考失败原因，存入记忆，下次尝试时参考。无需权重更新、无需梯度，仅用自然语言在试验间传递经验。在 ALFWorld、HotpotQA、HumanEval 上都取得了显著改进。

## The Concept

### The three components

```
Actor         : generates a trajectory (ReAct-style loop)     # 执行器：生成行动轨迹
Evaluator     : scores the trajectory — binary, heuristic, or self-eval  # 评估器：评分
Self-Reflector: writes a natural-language reflection on the failure      # 自我反思器：写反思
```

Plus one data structure:

```
Episodic memory: list of prior reflections, prepended to the next trial's prompt  # 情景记忆
```

One trial runs the Actor. Evaluator scores it. If the score is low, Self-Reflector produces a reflection ("I picked the wrong tool because I misread the question as asking about X when it was asking about Y"). The reflection goes into episodic memory. Next trial starts fresh but sees the reflection.

### Three evaluator types

1. **Scalar** — an external binary signal. ALFWorld succeeds or fails. HumanEval tests pass or fail. Simplest, highest-signal.
2. **Heuristic** — predefined failure signatures. "If the agent produced the same action twice in a row, mark as stuck." "If the trajectory exceeds 50 steps, mark as inefficient."
3. **Self-evaluated** — the LLM scores its own trajectory. Needed when no ground truth is available. Weaker signal; pairs well with tool-grounded verification (Lesson 05 — CRITIC).

The 2026 default is a mix: scalar when available, self-eval when not, heuristics as safety rails.

### Why this generalizes

Reflexion is not a new algorithm so much as a named pattern. Almost every production "self-healing" agent runs some variant:

- Letta's sleep-time compute (Lesson 08): a separate agent reflects on past conversations and writes to memory blocks.
- Claude Code's `CLAUDE.md` / "save memory" pattern: reflections captured as learnings, prepended to future sessions.
- pro-workflow's `/learn-rule` command: corrections captured as explicit rules.
- LangGraph's reflection nodes: a node that scores output and routes to refine if needed.

All derive from the same insight: natural language is a rich-enough medium to carry "what I learned from failure" between runs.

> **【拓展：Reflexion → 生产环境的自我修复】** 几乎所有生产环境的"自我修复"Agent 都使用 Reflexion 变体：Letta 的 sleep-time compute 异步反思、Claude Code 的 CLAUDE.md 存储学习经验、LangGraph 的反思节点。核心洞察相同：自然语言足够承载"从失败中学到了什么"。

### When it works and when it does not

Reflexion works when:

- There is a clear failure signal (test failure, tool error, wrong answer).
- The task class is reproducible (the same type of question can be asked again).
- The reflection has room to improve on the trajectory (enough action budget).

Reflexion does not help when:

- The agent already succeeds on the first try.
- The failure is external (network down, tool broken) — reflection on "the network was down" does not help future runs.
- The reflection turns into superstition — storing a narrative about a one-off flaky run.

2026 pitfall: memory rot. Reflections accumulate; some are obsolete or wrong; re-runs get slower as the episodic buffer grows. Mitigation: periodic compaction (Lesson 06), TTL on reflections, or a separate sleep-time cleanup agent (Letta).

> **【中文解读】** Reflexion 适用场景：有明确失败信号、任务可重现、反思有改进空间。不适用场景：首次即成功、外部故障、反思变成迷信。2026 年的陷阱：记忆腐化——反思不断积累但部分已过时，解决方案是定期压缩、TTL 或异步清理 Agent。

## Build It

`code/main.py` implements Reflexion on a toy puzzle: produce a 3-element list that sums to a target. The Actor emits candidate lists; the Evaluator checks the sum; the Self-Reflector writes a line about what went wrong. The reflection goes into episodic memory for the next trial.

Components:

- `Actor` — a scripted policy that improves when it sees reflections.
- `Evaluator.binary()` — pass/fail on the target sum.
- `SelfReflector` — generates a one-line diagnosis of the failure.
- `EpisodicMemory` — a bounded list with TTL semantics.

Run it:

```
python3 code/main.py
```

The trace shows three trials. Trial 1 fails, a reflection is stored, trial 2 sees the reflection and improves but still fails, trial 3 succeeds. Compare with a baseline run (no reflection) — it stays stuck at trial 1's answer.

## Use It

LangGraph ships reflection as a node pattern. Claude Code's `/memory` command and pro-workflow's `/learn-rule` externalize the episodic buffer as a markdown file. Letta's sleep-time compute runs the Self-Reflector on downtime so the primary agent stays latency-bound. OpenAI Agents SDK does not ship Reflexion directly; you build it with a custom Guardrail that rejects trajectories by score and a memory `Session` that survives across runs.

## Ship It

`outputs/skill-reflexion-buffer.md` creates and maintains an episodic buffer with reflection capture, TTL, and deduplication. Given a task class and a failure, it emits a reflection that actually helps the next trial (not a generic "be more careful").

## Exercises | 练习题

1. Switch from binary to scalar evaluator that returns a distance metric (how far from target). Does it converge faster?
   *将评估器从二值切换为返回距离度量的标量评估器。收敛更快吗？*
2. Add a TTL of 10 trials to reflections. Do older reflections hurt or help after that point?
   *给反思添加 10 次试验的 TTL。更早的反思在之后是有害还是有益？*
3. Implement heuristic evaluator: mark the trial as stuck if the same action repeats. How does this interact with Self-Reflector?
   *实现启发式评估器：重复相同行动时标记为卡住。这与自我反思器如何交互？*
4. Run Reflexion with an adversarial Actor that ignores reflections. What is the minimum reflection prompt engineering that forces the Actor to notice them?
   *用忽略反思的对抗性执行器运行 Reflexion。最少需要什么提示工程才能迫使执行器注意到反思？*
5. Read Section 4 of the Reflexion paper on AlfWorld. Reproduce the 130% success-rate improvement conceptually: what is the key delta vs vanilla ReAct?
   *阅读 Reflexion 论文第 4 节关于 AlfWorld 的内容。概念上重现 130% 成功率改进：相比原始 ReAct 的关键差异是什么？*

## Key Terms | 关键术语

| Term | What people say | What it actually means | 中文释义 |
|------|----------------|------------------------|----------|
| Reflexion | "Self-correction" | Shinn et al. 2023 — Actor, Evaluator, Self-Reflector plus episodic memory | 反思——执行器+评估器+自我反思器+情景记忆 |
| Verbal reinforcement | "Learning without gradients" | Natural-language reflection prepended to the next trial's prompt | 语言强化——无需梯度的自然语言学习 |
| Episodic memory | "Per-task reflections" | Bounded buffer of prior reflections for one task class | 情景记忆——按任务类别存储的反思缓冲区 |
| Scalar evaluator | "Binary success signal" | Pass/fail or numeric score from ground truth | 标量评估器——来自真值的二元/数值评分 |
| Heuristic evaluator | "Pattern-based detector" | Predefined failure signatures (e.g. stuck-loop, too-many-steps) | 启发式评估器——预定义的失败模式检测 |
| Self-evaluator | "LLM-as-judge on own trace" | Lower-signal fallback when no ground truth — pair with tool-grounded verification | 自评估器——LLM 评价自身轨迹 |
| Memory rot | "Stale reflections" | Episodic buffer fills with obsolete entries; fix with compaction/TTL | 记忆腐化——情景缓冲区填满过时条目 |
| Sleep-time reflection | "Async self-reflection" | Run Self-Reflector off the hot path so primary agent stays fast | 异步反思——在非关键路径上运行反思 |

## Further Reading

- [Shinn et al., Reflexion: Language Agents with Verbal Reinforcement Learning (arXiv:2303.11366)](https://arxiv.org/abs/2303.11366) — the canonical paper
- [Letta, Sleep-time Compute](https://www.letta.com/blog/sleep-time-compute) — async reflection in production
- [Anthropic, Effective context engineering for AI agents](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents) — managing the episodic buffer as part of context
- [LangGraph overview](https://docs.langchain.com/oss/python/langgraph/overview) — reflection node pattern
