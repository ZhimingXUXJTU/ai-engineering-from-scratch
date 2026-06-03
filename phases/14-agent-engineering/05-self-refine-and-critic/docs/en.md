# Self-Refine and CRITIC: Iterative Output Improvement | 自我精炼与 CRITIC：迭代式输出改进

> Self-Refine (Madaan et al., 2023) uses one LLM in three roles — generate, feedback, refine — in a loop. Average gain: +20 absolute on 7 tasks. CRITIC (Gou et al., 2023) hardens the feedback step by routing verification through external tools. In 2026 this pattern ships in every framework as "evaluator-optimizer" (Anthropic) or a guardrail loop (OpenAI Agents SDK).

> **【中文解读】** Self-Refine 让一个 LLM 扮演三个角色：生成、反馈、精炼，循环改进。7 个任务平均提升 20 个百分点。CRITIC 将验证步骤通过外部工具（搜索、代码解释器、计算器）进行强化。2026 年这已成为每个框架的标配——Anthropic 称为"评估器-优化器"，OpenAI Agents SDK 称为"输出护栏"。

> **【拓展：CRITIC → Claude Code 的自我修复】** Claude Code 在编写代码后会自动运行测试验证——这就是 CRITIC 模式的生产实现。当测试失败时，它基于错误反馈修正代码，直到测试通过。

**Type:** Build
**Languages:** Python (stdlib)
**Prerequisites:** Phase 14 · 01 (Agent Loop), Phase 14 · 03 (Reflexion)
**Time:** ~60 minutes

## Learning Objectives | 学习目标

- State Self-Refine's three prompts (generate, feedback, refine) and explain why history matters for the refine prompt.
- Explain CRITIC's critical insight: LLMs are unreliable at self-verification without external grounding.
- Implement a stdlib Self-Refine loop with history and an optional external verifier.
- Map this pattern to Anthropic's "evaluator-optimizer" workflow and OpenAI Agents SDK's output guardrails.

## The Problem | 问题

An agent produces an answer that is almost right. Maybe a line of code has a syntax error. Maybe a summary is too long. Maybe a plan misses an edge case. What you want is: the agent critiques its own output, then fixes it.

Self-Refine shows this works with a single model, no training data, no RL. But there is a catch: LLMs are bad at self-verification on hard facts. CRITIC names the fix — route the verify step through external tools (search, code interpreter, calculator, test runner).

Together these two papers define the 2026 default for iterative improvement: generate, verify (externally when possible), refine, stop when the verifier passes.

> **【中文解读】** Self-Refine 的核心思路：一个模型扮演生成者、批评者、精炼者三重角色。但 LLM 在硬事实上自我验证不可靠——CRITIC 的修复方案是通过外部工具进行验证。两者共同定义了 2026 年的迭代改进标准：生成→外部验证→精炼→验证通过则停止。

## The Concept

### Self-Refine (Madaan et al., NeurIPS 2023)

One LLM, three roles:

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

Headline: +20 absolute improvement averaged across 7 tasks (math, code, acronym, dialog) including GPT-4. No training, no external tools, single model.

### CRITIC (Gou et al., arXiv:2305.11738, v4 Feb 2024)

Self-Refine's weakness: the feedback step is an LLM scoring itself. For factual claims this is unreliable (a hallucination often looks convincing to the model that produced it). CRITIC replaces `feedback(task, output)` with `verify(task, output, tools)` where `tools` includes:

- A search engine for factual claims.          # 搜索引擎验证事实
- A code interpreter for code correctness.     # 代码解释器验证代码
- A calculator for arithmetic.                 # 计算器验证算术
- Domain-specific verifiers (unit tests, type checkers, linters).  # 领域验证器

The verifier produces a structured critique grounded in tool results. The refiner then conditions on this critique.

Headline: CRITIC outperforms Self-Refine on factual tasks because the critique is grounded. On tasks without external verifiers (creative writing, formatting), CRITIC reduces to Self-Refine.

### The stop condition

Two common shapes:

1. **Verifier passes.** External test returns success. Preferred when available (unit tests, type checker, guardrail assertion).
2. **No feedback issued.** Model says "the output is fine." Cheaper but unreliable; pair with a max-iteration cap.

2026 default: combine them. "Stop if verifier passes OR model says fine AND iterations >= 2 OR iterations >= max_iterations."

### Evaluator-Optimizer (Anthropic, 2024)

Anthropic's Dec 2024 post names this as one of the five workflow patterns. Two roles:

- Evaluator: scores the output and produces a critique.
- Optimizer: revises the output given the critique.

Loop until the evaluator passes. This is Self-Refine/CRITIC in Anthropic's framing. The critical engineering detail Anthropic adds: the evaluator and optimizer prompts should be substantially different so the model does not just rubber-stamp.

### OpenAI Agents SDK output guardrails

OpenAI Agents SDK ships this pattern as "output guardrails." A guardrail is a validator that runs on the final output of an agent. If the guardrail trips (raises `OutputGuardrailTripwireTriggered`), the output is rejected and the agent can retry. Guardrails can call tools (CRITIC-style) or be pure functions (Self-Refine-style).

### 2026 pitfalls

- **Rubber-stamp loops.** Same model doing generation and critique with the same prompt style converges on "looks good to me." Use structurally different prompts, or a smaller cheap model for critique.
- **Over-refinement.** Each refine pass adds latency and tokens. Budget 1-3 passes; after that, escalate to human review.
- **CRITIC on trivial tasks.** If there is no external verifier, CRITIC degenerates to Self-Refine; do not pay the latency for a stub verifier.

## Build It

`code/main.py` implements Self-Refine and CRITIC on a toy task: produce a short bullet list given a topic. The verifier checks format (3 bullets, each under 60 chars). CRITIC adds an external "fact verifier" that penalizes known hallucinations.

Components:

- `generate` — scripted producer.
- `feedback` — LLM-style self-critique.
- `verify_external` — CRITIC-style grounded verifier.
- `refine` — rewrites output given history.
- Stop condition — verifier passes or max 4 iterations.

Run it:

```
python3 code/main.py
```

Compare the Self-Refine vs CRITIC runs. CRITIC catches a factual error Self-Refine missed because the external verifier has grounding the self-critic does not.

## Use It

Anthropic's evaluator-optimizer is this pattern in Claude-friendly language. OpenAI Agents SDK's output guardrails are CRITIC-shaped (guardrails can call tools). LangGraph ships a reflection node that reads like Self-Refine. Google's Gemini 2.5 Computer Use adds a per-step safety evaluator that is a CRITIC variant: every action is verified before commit.

## Ship It

`outputs/skill-refine-loop.md` configures an evaluator-optimizer loop given task shape, verifier availability, and iteration budget. Emits prompts for generator, evaluator/verifier, and optimizer, plus a stop policy.

## Exercises | 练习题

1. Run the toy with max_iterations=1. Does CRITIC still help?
   *用 max_iterations=1 运行。CRITIC 仍然有帮助吗？*
2. Replace the external verifier with a noisy one (random 30% false positives). What does the loop do? This is the 2026 reality of most guardrail stacks.
   *将外部验证器替换为嘈杂的版本（30% 误报）。循环会做什么？这是 2026 年大多数护栏栈的现实。*
3. Implement a "generator-critic on different models" variant: big model generates, small model critiques. Does it beat same-model?
   *实现"不同模型的生成-批评"变体：大模型生成，小模型批评。比同模型更好吗？*
4. Read CRITIC Section 3 (arXiv:2305.11738 v4). Name the three verification-tool categories and give an example for each.
   *阅读 CRITIC 第 3 节。说出三种验证工具类别并各举一例。*
5. Map OpenAI Agents SDK's `output_guardrails` to CRITIC's verifier role. What does the SDK get wrong, and what does it get right?
   *将 OpenAI Agents SDK 的 output_guardrails 映射到 CRITIC 的验证器角色。SDK 哪里做得好，哪里不够？*

## Key Terms | 关键术语

| Term | What people say | What it actually means | 中文释义 |
|------|----------------|------------------------|----------|
| Self-Refine | "LLM that fixes itself" | Generate -> feedback -> refine loop in one model, with history | 自我精炼——一个模型内的生成→反馈→精炼循环 |
| CRITIC | "Tool-grounded verification" | Replace feedback with an external verifier (search, code, calc, tests) | CRITIC——用外部工具替代自我反馈 |
| Evaluator-Optimizer | "Anthropic workflow pattern" | Two roles — evaluator scores, optimizer revises — looped to convergence | 评估器-优化器——Anthropic 的工作流模式 |
| Output guardrail | "Post-hoc check" | OpenAI Agents SDK validator that runs after an agent produces output | 输出护栏——Agent 输出后的验证器 |
| Verify step | "Critique phase" | The load-bearing decision: grounded or self-rated | 验证步骤——基于外部工具还是自我评价 |
| Refine history | "What the model already tried" | Prior outputs + critiques prepended to refine prompt; drop and quality collapses | 精炼历史——之前输出和批评的记录 |
| Rubber-stamp loop | "Self-agreement failure" | Same-prompt critique returns "looks good"; fix with structurally different prompts | 橡皮图章循环——自我认同导致无法发现问题 |
| Stop condition | "Convergence test" | Verifier passes OR no feedback AND iteration cap; never single-condition | 停止条件——验证通过或达到迭代上限 |

## Further Reading

- [Madaan et al., Self-Refine (arXiv:2303.17651)](https://arxiv.org/abs/2303.17651) — the canonical paper
- [Gou et al., CRITIC (arXiv:2305.11738)](https://arxiv.org/abs/2305.11738) — tool-grounded verification
- [Anthropic, Building Effective Agents](https://www.anthropic.com/research/building-effective-agents) — evaluator-optimizer workflow pattern
- [OpenAI Agents SDK docs](https://openai.github.io/openai-agents-python/) — output guardrails as CRITIC-shaped verifiers
