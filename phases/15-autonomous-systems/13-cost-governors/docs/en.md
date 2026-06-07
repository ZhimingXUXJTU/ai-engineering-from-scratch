# Action Budgets, Iteration Caps, and Cost Governors | 控制器 迭代 成本 行动

> A mid-sized e-commerce agent's monthly LLM cost jumped from $1,200 to $4,800 after its team enabled the "order-tracking" skill. That is not a pricing bug. That is an agent that found a new loop and kept spending inside it. Microsoft's Agent Governance Toolkit (April 2, 2026) codifies the defense against this class: per-request `max_tokens`, per-task token and dollar budgets, per-day/month caps, iteration caps, tiered model routing, prompt caching, context windowing, HITL checkpoints on expensive actions, kill switches on budget breach. Anthropic's Claude Code Agent SDK ships the same primitives under different names. Financial velocity limits — e.g. cut access on >$50 in 10 minutes — catch loops faster than monthly caps.

**Type:** Learn | **类型:** 学习
**Languages:** Python (stdlib, layered cost-governor simulator) | **语言:** Python (stdlib, layered cost-governor simulator)
**Prerequisites:** Phase 15 · 10 (Permission modes), Phase 15 · 12 (Durable execution) | **前置知识:** Phase 15 · 10 (Permission modes), Phase 15 · 12 (Durable execution)
**Time:** ~60 minutes | **时间:** ~60 minutes

## The Problem | 问题引入

> **【中文解读】** 成本控制器（Cost Governors）监控和限制 Agent 的资源消耗——主要是 API 调用费用和 token 使用量。没有成本控制器的 Agent 可能在循环或低效执行中产生巨额账单。三种控制策略：(1) 预算上限——硬性 token/费用限制；(2) 速率限制——每分钟/每小时调用上限；(3) 效率门控——当成本/收益比恶化时暂停。

> **【拓展：cost governors】** 成本控制是 2025-2026 年 Agent 生产部署的关键挑战。公开案例：多个用户报告编码 Agent 在陷入修复循环后产生数千美元的 API 费用。解决方案包括：(1) OpenAI 的 max_output_tokens 限制；(2) Anthropic 的 usage tracking API；(3) 第三方工具如 Helicone 和 Braintrust 的成本监控。最佳实践是为每个任务设置明确的成本上限。

Autonomous agents spend real money on every turn.

> 自主 Agent 在每一轮都花费真金白银。聊天机器人的错误输出是一条错误回复；Agent 的错误循环是一张账单。 A chatbot's bad output is a bad reply; an agent's bad loop is a bill. The industry-documented term for the failure mode is "Denial of Wallet" — the agent keeps reasoning, keeps tool-calling, keeps billing, and nothing stops it because nothing was designed to.

The fix is not one number. It is a stack of limits at different time scales and granularities: per-request, per-task, per-hour, per-day, per-month. A well-designed stack catches a runaway loop within minutes, a slow leak within hours, and a bad release within a day. The same stack keeps a budget at all when the agent is long-horizon and autonomous.


> **【中文解读】** 本节介绍了 AI Agent 的核心概念和实现方法。Agent 是 LLM 驱动的自主系统，能够观察环境、思考决策、执行行动并循环迭代直到完成目标。

This is an engineering lesson: the math is trivial, the discipline is where teams fail. The list of limits below is all named either in the Microsoft Agent Governance Toolkit or the Anthropic Claude Code Agent SDK docs.

## The Concept | 核心概念

### The cost-governor stack

1. **`max_tokens` per request.** Simple. Prevents any one call from emitting an unbounded completion.
2. **Per-task token budget.** Across the whole run, do not exceed N tokens. Hard stop at the cap.
3. **Per-task dollar budget.** Same as tokens but in currency. `max_budget_usd` in Claude Code.
4. **Per-tool call cap.** No more than N `WebFetch` calls, N `shell_exec` calls, etc.
5. **Iteration cap (`max_turns`).** Total agent loop iterations; prevents infinite reasoning loops.
6. **Per-minute / per-hour / per-day / per-month cap.** Rolling windows. Catches leaks at different time scales.
7. **Financial velocity limit.** E.g., "if spend exceeds $50 in 10 minutes, cut access." Catches loop-based burn before monthly caps fire.
8. **Tiered model routing.** Default to a smaller model; escalate to a larger one only when a classifier judges the task warrants it.
9. **Prompt caching.** System prompt and stable context stored in provider cache; token cost of re-sending is near zero.
10. **Context windowing.** Compaction / summarization to keep the active context below a threshold; direct token-cost reduction.
11. **HITL checkpoints on expensive actions.** Before an action known to be expensive (long tool call, large download, a costly model upgrade), require a human tap.
12. **Kill switch on budget breach.** Session aborts when any cap fires. Cap is recorded; requires a separate re-enable path.

### Why the stack, not one cap

A single monthly cap catches a runaway agent only after the wallet is gone. A single per-request cap catches nothing at the session level. Different failure modes require different time scales:

- **Runaway loop** (agent stuck in a 5-second retry): caught by velocity limit.
- **Slow leak** (agent doing ~2x expected work per task): caught by daily cap.
- **Bad release** (new version uses 5x tokens): caught by weekly / monthly cap.
- **Legitimate surge** (real demand, not a bug): caught by hour / day cap with clear log.

### Claude Code's budget surface

The Claude Code Agent SDK exposes (public docs):

- `max_turns` — iteration cap.
- `max_budget_usd` — dollar cap; session aborts on breach.
- `allowed_tools` / `disallowed_tools` — tool allowlist and denylist.
- Hook points before tool use for custom cost-accounting.

Combine with the permission-mode ladder (Lesson 10). An `autoMode` session without `max_budget_usd` is ungoverned autonomy. Anthropic explicitly frames Auto Mode as requiring budget controls; the classifier is orthogonal to cost.

### EU AI Act, OWASP Agentic Top 10

Microsoft's Agent Governance Toolkit covers the OWASP Agentic Top 10 and the EU AI Act Article 14 (human oversight) requirements. For production in the EU, logging and cap enforcement are not optional.

### The observed $1,200 → $4,800 case

The real case in the Microsoft docs: an e-commerce agent whose monthly cost tripled after a new tool was added.

> Microsoft 文档中的真实案例：一个电子商务 Agent 在添加新工具后月成本翻了三倍。没有循环检测，没有按工具上限。 The tool allowed the agent to poll order status during every session. No loop detection. No per-tool cap. No alert on week-over-week growth. The fix was a per-tool cap plus a daily-growth alert. This is a template: every new tool surface is a new potential loop; every new tool needs its own cap and its own alert.

## Use It | 用框架实现

`code/main.py` simulates an agent run with and without a layered cost-governor stack. The simulated agent drifts into a polling loop after some turns; the layered stack catches it within the velocity window while a single monthly cap would not fire until days later.

## Ship It | 产出物

`outputs/skill-agent-budget-audit.md` audits a proposed agent deployment's cost-governor stack and flags missing layers.

## Exercises | 练习题

1. Run `code/main.py`. Confirm the velocity limit fires before the iteration cap on a polling-loop trajectory. Now disable the velocity limit and measure how much the agent "spends" before the iteration cap catches it.

2. Design a per-tool cap set for a browser agent (Lesson 11). Which tool needs the tightest cap? Which tool can run unbounded without risk?

3. Read the Microsoft Agent Governance Toolkit docs. List every cap type the toolkit names. Map each to one of the failure modes (runaway loop, slow leak, bad release, surge).

4. Price an overnight unattended run for a realistic task (e.g., "triage 50 issues in a repo"). Set `max_budget_usd` at 2x your point estimate. Justify the 2x.

5. Claude Code's `max_budget_usd` fires on session aggregate cost. Design a complementary velocity limit you would enforce externally. What triggers the cut-off, and what does re-enable look like?

## Key Terms | 术语速查表

| Term | What people say | What it actually means |
|---|---|---|
| 术语 | 通俗说法 | 实际含义 |
| Denial of Wallet | "Runaway bill" | Agent loop generating spend with no cap to stop it |  |
| max_tokens | "Per-request cap" | Ceiling on a single completion's size |  |
| max_turns | "Iteration cap" | Ceiling on agent loop iterations in a session |  |
| max_budget_usd | "Dollar kill switch" | Session cost cap; aborts on breach |  |
| Velocity limit | "Rate cap" | Limit on spend per short window (e.g., $50 / 10 min) |  |
| Tiered routing | "Small model first" | Cheap model default; escalate only when classifier warrants |  |
| Prompt caching | "Cached system prompt" | Provider-side cache reduces re-send token cost to near zero |  |
| HITL checkpoint | "Human approval gate" | Human tap required before expensive action |  |

## Further Reading | 延伸阅读

- [Anthropic Claude Code Agent SDK — agent loop and budgets](https://code.claude.com/docs/en/agent-sdk/agent-loop) — `max_turns`, `max_budget_usd`, tool allowlists.
- [Microsoft Agent Framework — human-in-the-loop and governance](https://learn.microsoft.com/en-us/agent-framework/workflows/human-in-the-loop) — cost-governor checkpoints.
- [Anthropic — Claude Managed Agents overview](https://platform.claude.com/docs/en/managed-agents/overview) — provider-side cost controls.
- [Anthropic — Prompt caching (Claude API docs)](https://platform.claude.com/docs/en/prompt-caching) — caching mechanics.
- [Anthropic — Measuring agent autonomy in practice](https://www.anthropic.com/research/measuring-agent-autonomy) — cost profile for long-horizon agents.
