# Reflexion: Verbal Reinforcement Learning | Reflexion：语言强化学习

> Gradient-based RL needs thousands of trials and a GPU cluster to fix a failure mode. Reflexion (Shinn et al., NeurIPS 2023) does it in natural language: after each failed trial, the agent writes a reflection, stores it in episodic memory, and conditions the next trial on that memory. This is the pattern behind Letta's sleep-time compute, Claude Code's CLAUDE.md learnings, and pro-workflow's learn-rule.

> **【中文解读】** 基于梯度的 RL 需要数千次试验和 GPU 集群。Reflexion 用自然语言实现自我改进：每次失败后，Agent 写一段反思存入情景记忆，下一次尝试时参考这些记忆。这正是 Letta 的 sleep-time compute、Claude Code 的 CLAUDE.md 学习机制背后的模式。

> **【拓展：Reflexion → Claude Code 的自我学习】** Claude Code 的 CLAUDE.md 机制本质上就是 Reflexion 的变体——Agent 在工作过程中积累经验教训，存储为规则文件，后续会话自动加载。这也是"从错误中学习"在生产环境中最常见的实现方式。

**Type:** Build | **类型:** 构建
**Languages:** Python (stdlib) | **语言:** Python (标准库)
**Prerequisites:** Phase 14 · 01 (Agent Loop), Phase 14 · 02 (ReWOO) | **前置知识:** Phase 14 · 01 (Agent 循环), Phase 14 · 02 (ReWOO)
**Time:** ~60 minutes | **时间:** ~60 分钟

## Learning Objectives | 学习目标

- Name the three components of Reflexion (Actor, Evaluator, Self-Reflector) and the role of episodic memory.
  中文翻译：说出 Reflexion 的三个组件（Actor、Evaluator、Self-Reflector）以及情景记忆的作用。
- Implement a stdlib Reflexion loop with binary evaluator, reflection buffer, and fresh re-attempts.
  中文翻译：用标准库实现 Reflexion 循环，包含二元评估器、反思缓冲区和全新重试。
- Choose between scalar, heuristic, and self-evaluated feedback sources for a given task.
  中文翻译：为给定任务选择标量、启发式或自评估反馈源。
- Explain why verbal reinforcement catches errors that gradient-based RL would need thousands of trials to fix.
  中文翻译：解释为什么语言强化能捕获基于梯度的 RL 需要数千次试验才能修复的错误。

## The Problem | 问题引入

An agent fails a task. In standard RL you would run thousands more trials, compute gradients, update weights. Expensive, slow, and most production agents do not have a training budget for every failure.

> Agent 失败了某个任务。在标准 RL 中，你需要运行数千次更多试验、计算梯度、更新权重。昂贵、缓慢，而且大多数生产 Agent 没有针对每次失败的训练预算。

Reflexion (Shinn et al., arXiv:2303.11366) asks a different question: what if the agent just thought about why it failed and tried again with that thought in its prompt? No weight updates. No gradient. Just natural language stored between trials.

> Reflexion（Shinn 等人，arXiv:2303.11366）提出了一个不同的问题：如果 Agent 只是思考失败原因，然后在下一次尝试的提示中加入这个想法呢？没有权重更新，没有梯度，只有试验间存储的自然语言。

The result: on ALFWorld it beats ReAct and other non-fine-tuned baselines. On HotpotQA it improves over ReAct. On code generation (HumanEval/MBPP) it sets state of the art at the time. All without a single gradient step.

> 结果：在 ALFWorld 上它击败了 ReAct 和其他非微调基线。在 HotpotQA 上它超越了 ReAct。在代码生成（HumanEval/MBPP）上它达到了当时的最佳水平。这一切都无需一次梯度步。

## The Concept | 核心概念

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

> 一次试验运行 Actor。Evaluator 对其评分。如果分数低，Self-Reflector 生成一段反思（"我选错了工具，因为我把问题误解为询问 X，实际上询问的是 Y"）。反思存入情景记忆。下一次试验重新开始但能看到反思。

### Three evaluator types

1. **Scalar** — an external binary signal. ALFWorld succeeds or fails. HumanEval tests pass or fail. Simplest, highest-signal.
   中文翻译：**标量**——外部二元信号。ALFWorld 成功或失败。HumanEval 测试通过或不通过。最简单，信号最强。
2. **Heuristic** — predefined failure signatures. "If the agent produced the same action twice in a row, mark as stuck." "If the trajectory exceeds 50 steps, mark as inefficient."
   中文翻译：**启发式**——预定义的失败签名。"如果 Agent 连续两次产生相同行动，标记为卡住。""如果轨迹超过 50 步，标记为低效。"
3. **Self-evaluated** — the LLM scores its own trajectory. Needed when no ground truth is available. Weaker signal; pairs well with tool-grounded verification (Lesson 05 — CRITIC).
   中文翻译：**自评估**——LLM 对自己的轨迹评分。在没有真值时需要。信号较弱；与工具锚定验证（第 5 课——CRITIC）配合使用。

The 2026 default is a mix: scalar when available, self-eval when not, heuristics as safety rails.

> 2026 年的默认做法是混合使用：有标量时用标量，没有时用自评估，启发式作为安全护栏。

### Why this generalizes

Reflexion is not a new algorithm so much as a named pattern. Almost every production "self-healing" agent runs some variant:

> Reflexion 与其说是一个新算法，不如说是一个命名模式。几乎每个生产环境的"自我修复"Agent 都运行某种变体：

- Letta's sleep-time compute (Lesson 08): a separate agent reflects on past conversations and writes to memory blocks.
  中文翻译：Letta 的 sleep-time compute（第 8 课）：一个独立 Agent 反思过去的对话并写入记忆块。
- Claude Code's `CLAUDE.md` / "save memory" pattern: reflections captured as learnings, prepended to future sessions.
  中文翻译：Claude Code 的 `CLAUDE.md`/"保存记忆"模式：反思被捕获为学习经验，前置到未来会话。
- pro-workflow's `/learn-rule` command: corrections captured as explicit rules.
  中文翻译：pro-workflow 的 `/learn-rule` 命令：纠正被捕获为显式规则。
- LangGraph's reflection nodes: a node that scores output and routes to refine if needed.
  中文翻译：LangGraph 的反思节点：一个评分输出并在需要时路由到精炼的节点。

All derive from the same insight: natural language is a rich-enough medium to carry "what I learned from failure" between runs.

> 它们都源于同一个洞察：自然语言是一种足够丰富的媒介，可以在运行之间传递"我从失败中学到了什么"。

> **【拓展：Reflexion → 生产环境的自我修复】** 几乎所有生产环境的"自我修复"Agent 都使用 Reflexion 变体：Letta 的 sleep-time compute 异步反思、Claude Code 的 CLAUDE.md 存储学习经验、LangGraph 的反思节点。核心洞察相同：自然语言足够承载"从失败中学到了什么"。

### When it works and when it does not

Reflexion works when:

> Reflexion 在以下情况有效：

- There is a clear failure signal (test failure, tool error, wrong answer).
  中文翻译：有明确的失败信号（测试失败、工具错误、错误答案）。
- The task class is reproducible (the same type of question can be asked again).
  中文翻译：任务类别可重现（可以再次提出相同类型的问题）。
- The reflection has room to improve on the trajectory (enough action budget).
  中文翻译：反思有改进轨迹的空间（足够的行动预算）。

Reflexion does not help when:

> Reflexion 在以下情况无帮助：

- The agent already succeeds on the first try.
  中文翻译：Agent 首次尝试即成功。
- The failure is external (network down, tool broken) — reflection on "the network was down" does not help future runs.
  中文翻译：失败是外部的（网络中断、工具损坏）——对"网络中断"的反思对未来运行无帮助。
- The reflection turns into superstition — storing a narrative about a one-off flaky run.
  中文翻译：反思变成迷信——存储关于一次性不稳定运行的叙述。

2026 pitfall: memory rot. Reflections accumulate; some are obsolete or wrong; re-runs get slower as the episodic buffer grows. Mitigation: periodic compaction (Lesson 06), TTL on reflections, or a separate sleep-time cleanup agent (Letta).

> 2026 年的陷阱：记忆腐化。反思不断积累，部分已过时或错误；随着情景缓冲区增长，重新运行变得更慢。缓解措施：定期压缩（第 6 课）、反思的 TTL，或独立的 sleep-time 清理 Agent（Letta）。

## Build It | 动手实现

`code/main.py` implements Reflexion on a toy puzzle: produce a 3-element list that sums to a target. The Actor emits candidate lists; the Evaluator checks the sum; the Self-Reflector writes a line about what went wrong. The reflection goes into episodic memory for the next trial.

> `code/main.py` 在一个玩具谜题上实现 Reflexion：生成一个和为目标值的 3 元素列表。Actor 发出候选列表；Evaluator 检查总和；Self-Reflector 写一行关于出了什么问题的诊断。反思存入情景记忆供下一次试验使用。

Components:

> 组件：

- `Actor` — a scripted policy that improves when it sees reflections.
  中文翻译：`Actor`——看到反思时会改进的脚本策略。
- `Evaluator.binary()` — pass/fail on the target sum.
  中文翻译：`Evaluator.binary()`——对目标总和的通过/失败判断。
- `SelfReflector` — generates a one-line diagnosis of the failure.
  中文翻译：`SelfReflector`——生成一行失败诊断。
- `EpisodicMemory` — a bounded list with TTL semantics.
  中文翻译：`EpisodicMemory`——带 TTL 语义的有界列表。

Run it:

> 运行：

```
python3 code/main.py
```

The trace shows three trials. Trial 1 fails, a reflection is stored, trial 2 sees the reflection and improves but still fails, trial 3 succeeds. Compare with a baseline run (no reflection) — it stays stuck at trial 1's answer.

> 轨迹显示三次试验。试验 1 失败，存储反思，试验 2 看到反思并改进但仍失败，试验 3 成功。与基线运行（无反思）对比——它停留在试验 1 的答案。

## Use It | 用框架实现

LangGraph ships reflection as a node pattern. Claude Code's `/memory` command and pro-workflow's `/learn-rule` externalize the episodic buffer as a markdown file. Letta's sleep-time compute runs the Self-Reflector on downtime so the primary agent stays latency-bound. OpenAI Agents SDK does not ship Reflexion directly; you build it with a custom Guardrail that rejects trajectories by score and a memory `Session` that survives across runs.

> LangGraph 将反思作为节点模式提供。Claude Code 的 `/memory` 命令和 pro-workflow 的 `/learn-rule` 将情景缓冲区外部化为 markdown 文件。Letta 的 sleep-time compute 在空闲时运行 Self-Reflector，使主 Agent 保持低延迟。OpenAI Agents SDK 不直接提供 Reflexion；你用自定义 Guardrail（按分数拒绝轨迹）和跨运行持久化的内存 `Session` 来构建它。

## Ship It | 产出物

`outputs/skill-reflexion-buffer.md` creates and maintains an episodic buffer with reflection capture, TTL, and deduplication. Given a task class and a failure, it emits a reflection that actually helps the next trial (not a generic "be more careful").

> `outputs/skill-reflexion-buffer.md` 创建并维护一个带反思捕获、TTL 和去重的情景缓冲区。给定任务类别和失败，它生成一段真正有助于下一次试验的反思（而非通用的"要更小心"）。

## Exercises | 练习题

1. Switch from binary to scalar evaluator that returns a distance metric (how far from target). Does it converge faster?
   中文翻译：将评估器从二元切换为返回距离度量的标量评估器。收敛更快吗？
2. Add a TTL of 10 trials to reflections. Do older reflections hurt or help after that point?
   中文翻译：给反思添加 10 次试验的 TTL。更早的反思在之后是有害还是有益？
3. Implement heuristic evaluator: mark the trial as stuck if the same action repeats. How does this interact with Self-Reflector?
   中文翻译：实现启发式评估器：重复相同行动时标记为卡住。这与自我反思器如何交互？
4. Run Reflexion with an adversarial Actor that ignores reflections. What is the minimum reflection prompt engineering that forces the Actor to notice them?
   中文翻译：用忽略反思的对抗性 Actor 运行 Reflexion。最少需要什么提示工程才能迫使 Actor 注意到反思？
5. Read Section 4 of the Reflexion paper on AlfWorld. Reproduce the 130% success-rate improvement conceptually: what is the key delta vs vanilla ReAct?
   中文翻译：阅读 Reflexion 论文第 4 节关于 AlfWorld 的内容。概念上重现 130% 成功率改进：相比原始 ReAct 的关键差异是什么？

## Key Terms | 术语速查表

| Term | What people say | What it actually means |
|------|-----------------|-----------------------|
| 术语 | 通俗说法 | 实际含义 |
| Reflexion | "Self-correction" / "自我纠错" | Shinn et al. 2023 — Actor, Evaluator, Self-Reflector plus episodic memory / Shinn 等人 2023——Actor、Evaluator、Self-Reflector 加情景记忆 |
| Verbal reinforcement | "Learning without gradients" / "无梯度学习" | Natural-language reflection prepended to the next trial's prompt / 自然语言反思前置到下一次试验的提示 |
| Episodic memory | "Per-task reflections" / "按任务的反思" | Bounded buffer of prior reflections for one task class / 一个任务类别的先前反思有界缓冲区 |
| Scalar evaluator | "Binary success signal" / "二元成功信号" | Pass/fail or numeric score from ground truth / 来自真值的通过/失败或数值评分 |
| Heuristic evaluator | "Pattern-based detector" / "基于模式的检测器" | Predefined failure signatures (e.g. stuck-loop, too-many-steps) / 预定义的失败签名（如卡住循环、步数过多） |
| Self-evaluator | "LLM-as-judge on own trace" / "LLM 评价自身轨迹" | Lower-signal fallback when no ground truth — pair with tool-grounded verification / 无真值时的低信号后备——与工具锚定验证配合 |
| Memory rot | "Stale reflections" / "过时反思" | Episodic buffer fills with obsolete entries; fix with compaction/TTL / 情景缓冲区填满过时条目；用压缩/TTL 修复 |
| Sleep-time reflection | "Async self-reflection" / "异步自我反思" | Run Self-Reflector off the hot path so primary agent stays fast / 在非关键路径上运行 Self-Reflector 使主 Agent 保持快速 |

## Further Reading | 延伸阅读

- [Shinn et al., Reflexion: Language Agents with Verbal Reinforcement Learning (arXiv:2303.11366)](https://arxiv.org/abs/2303.11366) — the canonical paper
  中文翻译：Reflexion 经典论文——语言 Agent 的语言强化学习。
- [Letta, Sleep-time Compute](https://www.letta.com/blog/sleep-time-compute) — async reflection in production
  中文翻译：Letta 关于生产环境中异步反思的博客文章。
- [Anthropic, Effective context engineering for AI agents](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents) — managing the episodic buffer as part of context
  中文翻译：Anthropic 关于 AI Agent 上下文工程的文章——将情景缓冲区作为上下文的一部分管理。
- [LangGraph overview](https://docs.langchain.com/oss/python/langgraph/overview) — reflection node pattern
  中文翻译：LangGraph 概览——反思节点模式。
