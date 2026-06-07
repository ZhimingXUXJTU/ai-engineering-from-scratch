# Self-Refine and CRITIC: Iterative Output Improvement | 自我精炼与 CRITIC：迭代式输出改进

> Self-Refine (Madaan et al., 2023) uses one LLM in three roles — generate, feedback, refine — in a loop. Average gain: +20 absolute on 7 tasks. CRITIC (Gou et al., 2023) hardens the feedback step by routing verification through external tools. In 2026 this pattern ships in every framework as "evaluator-optimizer" (Anthropic) or a guardrail loop (OpenAI Agents SDK).

> **【中文解读】** Self-Refine 让一个 LLM 扮演三个角色：生成、反馈、精炼，循环改进。7 个任务平均提升 20 个百分点。CRITIC 将验证步骤通过外部工具（搜索、代码解释器、计算器）进行强化。2026 年这已成为每个框架的标配——Anthropic 称为"评估器-优化器"，OpenAI Agents SDK 称为"输出护栏"。

> **【拓展：CRITIC → Claude Code 的自我修复】** Claude Code 在编写代码后会自动运行测试验证——这就是 CRITIC 模式的生产实现。当测试失败时，它基于错误反馈修正代码，直到测试通过。

**Type:** Build | **类型:** 构建
**Languages:** Python (stdlib) | **语言:** Python (标准库)
**Prerequisites:** Phase 14 · 01 (Agent Loop), Phase 14 · 03 (Reflexion) | **前置知识:** Phase 14 · 01 (Agent 循环), Phase 14 · 03 (Reflexion)
**Time:** ~60 minutes | **时间:** ~60 分钟

## Learning Objectives | 学习目标

- State Self-Refine's three prompts (generate, feedback, refine) and explain why history matters for the refine prompt.
  中文翻译：陈述 Self-Refine 的三个提示（生成、反馈、精炼）并解释为什么历史记录对精炼提示很重要。
- Explain CRITIC's critical insight: LLMs are unreliable at self-verification without external grounding.
  中文翻译：解释 CRITIC 的关键洞察：没有外部锚定，LLM 在自我验证上不可靠。
- Implement a stdlib Self-Refine loop with history and an optional external verifier.
  中文翻译：用标准库实现带历史记录和可选外部验证器的 Self-Refine 循环。
- Map this pattern to Anthropic's "evaluator-optimizer" workflow and OpenAI Agents SDK's output guardrails.
  中文翻译：将此模式映射到 Anthropic 的"评估器-优化器"工作流和 OpenAI Agents SDK 的输出护栏。

## The Problem | 问题引入

An agent produces an answer that is almost right. Maybe a line of code has a syntax error. Maybe a summary is too long. Maybe a plan misses an edge case. What you want is: the agent critiques its own output, then fixes it.

> Agent 产生了一个几乎正确的答案。也许一行代码有语法错误。也许摘要太长了。也许一个计划遗漏了边缘情况。你想要的是：Agent 批评自己的输出，然后修复它。

Self-Refine shows this works with a single model, no training data, no RL. But there is a catch: LLMs are bad at self-verification on hard facts. CRITIC names the fix — route the verify step through external tools (search, code interpreter, calculator, test runner).

> Self-Refine 证明了这用单一模型就能工作，无需训练数据、无需 RL。但有一个陷阱：LLM 在硬事实上的自我验证能力很差。CRITIC 指出了修复方案——通过外部工具（搜索、代码解释器、计算器、测试运行器）路由验证步骤。

Together these two papers define the 2026 default for iterative improvement: generate, verify (externally when possible), refine, stop when the verifier passes.

> 这两篇论文共同定义了 2026 年迭代改进的默认模式：生成、验证（尽可能外部验证）、精炼、验证通过则停止。

> **【中文解读】** Self-Refine 的核心思路：一个模型扮演生成者、批评者、精炼者三重角色。但 LLM 在硬事实上自我验证不可靠——CRITIC 的修复方案是通过外部工具进行验证。两者共同定义了 2026 年的迭代改进标准：生成→外部验证→精炼→验证通过则停止。

## The Concept | 核心概念

### Self-Refine (Madaan et al., NeurIPS 2023)

One LLM, three roles:

> 一个 LLM，三个角色：

```
generate(task)            -> output_0                          # 生成初始输出
feedback(task, output_0)  -> critique_0                        # 自我批评
refine(task, output_0, critique_0, history) -> output_1       # 根据批评精炼
feedback(task, output_1)  -> critique_1                        # 再次批评
refine(task, output_1, critique_1, history) -> output_2       # 再次精炼
...
stop when feedback says "no issues" or budget exhausted.       # 停止条件
```

Key detail: `refine` sees the full history — all prior outputs and critiques — so it does not repeat mistakes. The paper ablates this: drop history and quality drops sharply.

> 关键细节：`refine` 能看到完整历史——所有先前的输出和批评——因此不会重复错误。论文对此做了消融实验：去掉历史记录后质量急剧下降。

Headline: +20 absolute improvement averaged across 7 tasks (math, code, acronym, dialog) including GPT-4. No training, no external tools, single model.

> 核心数据：在 7 个任务（数学、代码、缩写、对话）上平均绝对提升 20 个百分点，包括 GPT-4。无需训练、无需外部工具、单一模型。

### CRITIC (Gou et al., arXiv:2305.11738, v4 Feb 2024)

Self-Refine's weakness: the feedback step is an LLM scoring itself. For factual claims this is unreliable (a hallucination often looks convincing to the model that produced it). CRITIC replaces `feedback(task, output)` with `verify(task, output, tools)` where `tools` includes:

> Self-Refine 的弱点：反馈步骤是 LLM 给自己评分。对于事实性声明这不可靠（幻觉对产生它的模型来说通常看起来很有说服力）。CRITIC 用 `verify(task, output, tools)` 替代 `feedback(task, output)`，其中 `tools` 包括：

- A search engine for factual claims.
  中文翻译：用于事实性声明的搜索引擎。
- A code interpreter for code correctness.
  中文翻译：用于代码正确性的代码解释器。
- A calculator for arithmetic.
  中文翻译：用于算术的计算器。
- Domain-specific verifiers (unit tests, type checkers, linters).
  中文翻译：领域特定验证器（单元测试、类型检查器、代码检查器）。

The verifier produces a structured critique grounded in tool results. The refiner then conditions on this critique.

> 验证器产生基于工具结果的结构化批评。精炼器然后基于这个批评进行条件化。

Headline: CRITIC outperforms Self-Refine on factual tasks because the critique is grounded. On tasks without external verifiers (creative writing, formatting), CRITIC reduces to Self-Refine.

> 核心数据：CRITIC 在事实性任务上超越 Self-Refine，因为批评是有依据的。在没有外部验证器的任务上（创意写作、格式化），CRITIC 退化为 Self-Refine。

### The stop condition

Two common shapes:

> 两种常见形式：

1. **Verifier passes.** External test returns success. Preferred when available (unit tests, type checker, guardrail assertion).
   中文翻译：**验证器通过。** 外部测试返回成功。在可用时优先（单元测试、类型检查器、护栏断言）。
2. **No feedback issued.** Model says "the output is fine." Cheaper but unreliable; pair with a max-iteration cap.
   中文翻译：**无反馈发出。** 模型说"输出没问题"。更便宜但不可靠；配合最大迭代次数上限。

2026 default: combine them. "Stop if verifier passes OR model says fine AND iterations >= 2 OR iterations >= max_iterations."

> 2026 年默认做法：组合使用。"如果验证器通过，或模型说没问题且迭代次数 >= 2，或迭代次数 >= 最大迭代次数，则停止。"

### Evaluator-Optimizer (Anthropic, 2024)

Anthropic's Dec 2024 post names this as one of the five workflow patterns. Two roles:

> Anthropic 2024 年 12 月的文章将此命名为五种工作流模式之一。两个角色：

- Evaluator: scores the output and produces a critique.
  中文翻译：评估器：对输出评分并产生批评。
- Optimizer: revises the output given the critique.
  中文翻译：优化器：根据批评修改输出。

Loop until the evaluator passes. This is Self-Refine/CRITIC in Anthropic's framing. The critical engineering detail Anthropic adds: the evaluator and optimizer prompts should be substantially different so the model does not just rubber-stamp.

> 循环直到评估器通过。这是 Anthropic 框架下的 Self-Refine/CRITIC。Anthropic 添加的关键工程细节：评估器和优化器提示应该有实质性差异，以免模型只是橡皮图章。

### OpenAI Agents SDK output guardrails

OpenAI Agents SDK ships this pattern as "output guardrails." A guardrail is a validator that runs on the final output of an agent. If the guardrail trips (raises `OutputGuardrailTripwireTriggered`), the output is rejected and the agent can retry. Guardrails can call tools (CRITIC-style) or be pure functions (Self-Refine-style).

> OpenAI Agents SDK 将此模式作为"输出护栏"提供。护栏是在 Agent 最终输出上运行的验证器。如果护栏触发（抛出 `OutputGuardrailTripwireTriggered`），输出被拒绝，Agent 可以重试。护栏可以调用工具（CRITIC 风格）或使用纯函数（Self-Refine 风格）。

### 2026 pitfalls

- **Rubber-stamp loops.** Same model doing generation and critique with the same prompt style converges on "looks good to me." Use structurally different prompts, or a smaller cheap model for critique.
  中文翻译：**橡皮图章循环。** 同一模型用相同提示风格做生成和批评会收敛到"看起来不错"。使用结构性不同的提示，或用更小更便宜的模型做批评。
- **Over-refinement.** Each refine pass adds latency and tokens. Budget 1-3 passes; after that, escalate to human review.
  中文翻译：**过度精炼。** 每次精炼增加延迟和 token。预算 1-3 轮；之后升级为人工审查。
- **CRITIC on trivial tasks.** If there is no external verifier, CRITIC degenerates to Self-Refine; do not pay the latency for a stub verifier.
  中文翻译：**在简单任务上使用 CRITIC。** 如果没有外部验证器，CRITIC 退化为 Self-Refine；不要为桩验证器付出延迟代价。

## Build It | 动手实现

`code/main.py` implements Self-Refine and CRITIC on a toy task: produce a short bullet list given a topic. The verifier checks format (3 bullets, each under 60 chars). CRITIC adds an external "fact verifier" that penalizes known hallucinations.

> `code/main.py` 在一个玩具任务上实现 Self-Refine 和 CRITIC：给定主题生成短列表。验证器检查格式（3 个要点，每个 60 字符以下）。CRITIC 添加了惩罚已知幻觉的外部"事实验证器"。

Components:

> 组件：

- `generate` — scripted producer.
  中文翻译：`generate`——脚本生成器。
- `feedback` — LLM-style self-critique.
  中文翻译：`feedback`——LLM 风格自我批评。
- `verify_external` — CRITIC-style grounded verifier.
  中文翻译：`verify_external`——CRITIC 风格锚定验证器。
- `refine` — rewrites output given history.
  中文翻译：`refine`——根据历史重写输出。
- Stop condition — verifier passes or max 4 iterations.
  中文翻译：停止条件——验证器通过或最多 4 次迭代。

Run it:

> 运行：

```
python3 code/main.py
```

Compare the Self-Refine vs CRITIC runs. CRITIC catches a factual error Self-Refine missed because the external verifier has grounding the self-critic does not.

> 比较 Self-Refine 和 CRITIC 运行。CRITIC 捕获了 Self-Refine 遗漏的事实错误，因为外部验证器拥有自我批评所没有的锚定依据。

## Use It | 用框架实现

Anthropic's evaluator-optimizer is this pattern in Claude-friendly language. OpenAI Agents SDK's output guardrails are CRITIC-shaped (guardrails can call tools). LangGraph ships a reflection node that reads like Self-Refine. Google's Gemini 2.5 Computer Use adds a per-step safety evaluator that is a CRITIC variant: every action is verified before commit.

> Anthropic 的评估器-优化器是用 Claude 友好语言表达的这一模式。OpenAI Agents SDK 的输出护栏是 CRITIC 形式的（护栏可以调用工具）。LangGraph 提供了一个类似 Self-Refine 的反思节点。Google 的 Gemini 2.5 Computer Use 添加了每步安全评估器——一种 CRITIC 变体：每个动作在提交前都经过验证。

## Ship It | 产出物

`outputs/skill-refine-loop.md` configures an evaluator-optimizer loop given task shape, verifier availability, and iteration budget. Emits prompts for generator, evaluator/verifier, and optimizer, plus a stop policy.

> `outputs/skill-refine-loop.md` 根据任务形状、验证器可用性和迭代预算配置评估器-优化器循环。输出生成器、评估器/验证器和优化器的提示，以及停止策略。

## Exercises | 练习题

1. Run the toy with max_iterations=1. Does CRITIC still help?
   中文翻译：用 max_iterations=1 运行。CRITIC 仍然有帮助吗？
2. Replace the external verifier with a noisy one (random 30% false positives). What does the loop do? This is the 2026 reality of most guardrail stacks.
   中文翻译：将外部验证器替换为嘈杂的版本（30% 误报）。循环会做什么？这是 2026 年大多数护栏栈的现实。
3. Implement a "generator-critic on different models" variant: big model generates, small model critiques. Does it beat same-model?
   中文翻译：实现"不同模型的生成-批评"变体：大模型生成，小模型批评。比同模型更好吗？
4. Read CRITIC Section 3 (arXiv:2305.11738 v4). Name the three verification-tool categories and give an example for each.
   中文翻译：阅读 CRITIC 第 3 节。说出三种验证工具类别并各举一例。
5. Map OpenAI Agents SDK's `output_guardrails` to CRITIC's verifier role. What does the SDK get wrong, and what does it get right?
   中文翻译：将 OpenAI Agents SDK 的 `output_guardrails` 映射到 CRITIC 的验证器角色。SDK 哪里做得好，哪里不够？

## Key Terms | 术语速查表

| Term | What people say | What it actually means |
|------|-----------------|-----------------------|
| 术语 | 通俗说法 | 实际含义 |
| Self-Refine | "LLM that fixes itself" / "自我修复的 LLM" | Generate -> feedback -> refine loop in one model, with history / 一个模型内的生成→反馈→精炼循环，带历史记录 |
| CRITIC | "Tool-grounded verification" / "工具锚定验证" | Replace feedback with an external verifier (search, code, calc, tests) / 用外部验证器替代反馈 |
| Evaluator-Optimizer | "Anthropic workflow pattern" / "Anthropic 工作流模式" | Two roles — evaluator scores, optimizer revises — looped to convergence / 两个角色——评估器评分、优化器修改——循环到收敛 |
| Output guardrail | "Post-hoc check" / "事后检查" | OpenAI Agents SDK validator that runs after an agent produces output / Agent 输出后运行的验证器 |
| Verify step | "Critique phase" / "批评阶段" | The load-bearing decision: grounded or self-rated / 核心决策：基于外部工具还是自我评价 |
| Refine history | "What the model already tried" / "模型已尝试的内容" | Prior outputs + critiques prepended to refine prompt; drop and quality collapses / 先前输出+批评前置到精炼提示；去掉则质量崩溃 |
| Rubber-stamp loop | "Self-agreement failure" / "自我认同失败" | Same-prompt critique returns "looks good"; fix with structurally different prompts / 相同提示批评返回"看起来不错"；用结构性不同的提示修复 |
| Stop condition | "Convergence test" / "收敛测试" | Verifier passes OR no feedback AND iteration cap; never single-condition / 验证器通过或无反馈且达到迭代上限；永不使用单一条件 |

## Further Reading | 延伸阅读

- [Madaan et al., Self-Refine (arXiv:2303.17651)](https://arxiv.org/abs/2303.17651) — the canonical paper
  中文翻译：Self-Refine 经典论文——自我精炼迭代改进。
- [Gou et al., CRITIC (arXiv:2305.11738)](https://arxiv.org/abs/2305.11738) — tool-grounded verification
  中文翻译：CRITIC——工具锚定验证。
- [Anthropic, Building Effective Agents](https://www.anthropic.com/research/building-effective-agents) — evaluator-optimizer workflow pattern
  中文翻译：Anthropic 关于构建有效 Agent 的指导——评估器-优化器工作流模式。
- [OpenAI Agents SDK docs](https://openai.github.io/openai-agents-python/) — output guardrails as CRITIC-shaped verifiers
  中文翻译：OpenAI Agents SDK 文档——输出护栏作为 CRITIC 形式的验证器。
