# Action Budgets, Iteration Caps, and Cost Governors | 动作预算、迭代上限与成本治理器

> A mid-sized e-commerce agent's monthly LLM cost jumped from $1,200 to $4,800 after its team enabled the "order-tracking" skill. That is not a pricing bug. That is an agent that found a new loop and kept spending inside it. Microsoft's Agent Governance Toolkit (April 2, 2026) codifies the defense against this class: per-request `max_tokens`, per-task token and dollar budgets, per-day/month caps, iteration caps, tiered model routing, prompt caching, context windowing, HITL checkpoints on expensive actions, kill switches on budget breach. Anthropic's Claude Code Agent SDK ships the same primitives under different names. Financial velocity limits — e.g. cut access on >$50 in 10 minutes — catch loops faster than monthly caps.

> **【中文解读】** 中型电商 Agent 的月 LLM 成本在团队启用"订单追踪"技能后从 $1,200 跳到 $4,800。这不是定价 bug。这是 Agent 找到新循环并在其中持续花费。Microsoft 的 Agent Governance Toolkit（2026 年 4 月 2 日）编纂了针对此类的防御：每请求 `max_tokens`、每任务 token 和美元预算、每日/月上限、迭代上限、分层模型路由、提示缓存、上下文窗口、昂贵动作上的 HITL 检查点、预算违反时的终止开关。Anthropic 的 Claude Code Agent SDK 以不同名称出货相同原语。金融速度限制——例如 10 分钟内 >$50 切断访问——比月度上限更快捕获循环。

> **【拓展：单一上限不够 → 分层栈】** 失败模式与时间尺度需要对应：5 秒重试的失控循环（速度限制捕获）、每任务 2x 工作的缓慢泄漏（每日上限）、新版本 5x token 的坏发布（每周/月上限）、真实需求的合法激增（小时/日上限带清晰日志）。单一上限在钱包已空后才捕获；分层栈在分钟内捕获失控、数小时内捕获泄漏、一天内捕获坏发布。

**Type:** Learn | **类型:** 学习
**Languages:** Python (stdlib, layered cost-governor simulator) | **语言:** Python（标准库，分层成本治理器模拟器）
**Prerequisites:** Phase 15 · 10 (Permission modes), Phase 15 · 12 (Durable execution) | **前置知识:** Phase 15 · 10（权限模式），Phase 15 · 12（持久执行）
**Time:** ~60 minutes | **时间:** ~60 分钟

## The Problem | 问题引入

> **【中文解读】** 成本控制器（Cost Governors）监控和限制 Agent 的资源消耗——主要是 API 调用费用和 token 使用量。没有成本控制器的 Agent 可能在循环或低效执行中产生巨额账单。三种控制策略：(1) 预算上限——硬性 token/费用限制；(2) 速率限制——每分钟/每小时调用上限；(3) 效率门控——当成本/收益比恶化时暂停。

> **【拓展：cost governors】** 成本控制是 2025-2026 年 Agent 生产部署的关键挑战。公开案例：多个用户报告编码 Agent 在陷入修复循环后产生数千美元的 API 费用。解决方案包括：(1) OpenAI 的 max_output_tokens 限制；(2) Anthropic 的 usage tracking API；(3) 第三方工具如 Helicone 和 Braintrust 的成本监控。最佳实践是为每个任务设置明确的成本上限。

Autonomous agents spend real money on every turn.

> 自主 Agent 在每一轮都花费真金白银。

A chatbot's bad output is a bad reply; an agent's bad loop is a bill. The industry-documented term for the failure mode is "Denial of Wallet" — the agent keeps reasoning, keeps tool-calling, keeps billing, and nothing stops it because nothing was designed to.

> 聊天机器人的错误输出是一条错误回复；Agent 的错误循环是一张账单。行业记录的失败模式术语是"Denial of Wallet"——Agent 持续推理、持续调用工具、持续计费，没东西阻止它，因为没东西被设计来阻止。

The fix is not one number. It is a stack of limits at different time scales and granularities: per-request, per-task, per-hour, per-day, per-month. A well-designed stack catches a runaway loop within minutes, a slow leak within hours, and a bad release within a day. The same stack keeps a budget at all when the agent is long-horizon and autonomous.

> 修复不是一个数字。它是不同时间尺度和粒度的限制栈：每请求、每任务、每小时、每日、每月。良好设计的栈在分钟内捕获失控循环、数小时内捕获缓慢泄漏、一天内捕获坏发布。同一栈在 Agent 长程自主时保持预算。

> **【中文解读】** 本节介绍了 AI Agent 的核心概念和实现方法。Agent 是 LLM 驱动的自主系统，能够观察环境、思考决策、执行行动并循环迭代直到完成目标。

This is an engineering lesson: the math is trivial, the discipline is where teams fail. The list of limits below is all named either in the Microsoft Agent Governance Toolkit or the Anthropic Claude Code Agent SDK docs.

> 这是工程课：数学平凡，纪律是团队失败之处。下面的限制列表全部在 Microsoft Agent Governance Toolkit 或 Anthropic Claude Code Agent SDK 文档中命名。

## The Concept | 核心概念

### The cost-governor stack | 成本治理栈

1. **`max_tokens` per request.** Simple. Prevents any one call from emitting an unbounded completion.
   中文翻译：**每请求 `max_tokens`。** 简单。防止单次调用发出无界补全。
2. **Per-task token budget.** Across the whole run, do not exceed N tokens. Hard stop at the cap.
   中文翻译：**每任务 token 预算。** 整个运行不超过 N 个 token。上限处硬停。
3. **Per-task dollar budget.** Same as tokens but in currency. `max_budget_usd` in Claude Code.
   中文翻译：**每任务美元预算。** 与 token 相同但以货币计。Claude Code 中是 `max_budget_usd`。
4. **Per-tool call cap.** No more than N `WebFetch` calls, N `shell_exec` calls, etc.
   中文翻译：**每工具调用上限。** 不超过 N 个 `WebFetch` 调用、N 个 `shell_exec` 调用等。
5. **Iteration cap (`max_turns`).** Total agent loop iterations; prevents infinite reasoning loops.
   中文翻译：**迭代上限（`max_turns`）。** 总 Agent 循环迭代数；防止无限推理循环。
6. **Per-minute / per-hour / per-day / per-month cap.** Rolling windows. Catches leaks at different time scales.
   中文翻译：**每分/时/日/月上限。** 滚动窗口。在不同时间尺度捕获泄漏。
7. **Financial velocity limit.** E.g., "if spend exceeds $50 in 10 minutes, cut access." Catches loop-based burn before monthly caps fire.
   中文翻译：**金融速度限制。** 例如"如果 10 分钟内花费超过 $50，切断访问"。在月度上限触发前捕获循环烧钱。
8. **Tiered model routing.** Default to a smaller model; escalate to a larger one only when a classifier judges the task warrants it.
   中文翻译：**分层模型路由。** 默认小模型；仅当分类器判断任务值得时升级到较大模型。
9. **Prompt caching.** System prompt and stable context stored in provider cache; token cost of re-sending is near zero.
   中文翻译：**提示缓存。** 系统提示和稳定上下文存储在提供商缓存；重发的 token 成本接近零。
10. **Context windowing.** Compaction / summarization to keep the active context below a threshold; direct token-cost reduction.
    中文翻译：**上下文窗口。** 压缩/摘要以保持活跃上下文低于阈值；直接 token 成本降低。
11. **HITL checkpoints on expensive actions.** Before an action known to be expensive (long tool call, large download, a costly model upgrade), require a human tap.
    中文翻译：**昂贵动作上的 HITL 检查点。** 在已知昂贵的动作（长工具调用、大下载、昂贵模型升级）前要求人类点击。
12. **Kill switch on budget breach.** Session aborts when any cap fires. Cap is recorded; requires a separate re-enable path.
    中文翻译：**预算违反时终止开关。** 任一上限触发时会话中止。上限被记录；需要单独重新启用路径。

### Why the stack, not one cap | 为什么是栈而非单上限

A single monthly cap catches a runaway agent only after the wallet is gone. A single per-request cap catches nothing at the session level. Different failure modes require different time scales:

> 单一月度上限只在钱包空后捕获失控 Agent。单一每请求上限在会话级什么也不捕获。不同失败模式需要不同时间尺度：

- **Runaway loop** (agent stuck in a 5-second retry): caught by velocity limit.
  中文翻译：**失控循环**（Agent 卡在 5 秒重试）：速度限制捕获。
- **Slow leak** (agent doing ~2x expected work per task): caught by daily cap.
  中文翻译：**缓慢泄漏**（Agent 每任务做约 2x 预期工作）：每日上限捕获。
- **Bad release** (new version uses 5x tokens): caught by weekly / monthly cap.
  中文翻译：**坏发布**（新版本用 5x token）：每周/月上限捕获。
- **Legitimate surge** (real demand, not a bug): caught by hour / day cap with clear log.
  中文翻译：**合法激增**（真实需求，非 bug）：小时/日上限带清晰日志捕获。

### Claude Code's budget surface | Claude Code 的预算面

The Claude Code Agent SDK exposes (public docs):

> Claude Code Agent SDK 暴露（公开文档）：

- `max_turns` — iteration cap.
  中文翻译：`max_turns`——迭代上限。
- `max_budget_usd` — dollar cap; session aborts on breach.
  中文翻译：`max_budget_usd`——美元上限；违反时会话中止。
- `allowed_tools` / `disallowed_tools` — tool allowlist and denylist.
  中文翻译：`allowed_tools` / `disallowed_tools`——工具允许列表和拒绝列表。
- Hook points before tool use for custom cost-accounting.
  中文翻译：工具使用前的钩子点用于自定义成本核算。

Combine with the permission-mode ladder (Lesson 10). An `autoMode` session without `max_budget_usd` is ungoverned autonomy. Anthropic explicitly frames Auto Mode as requiring budget controls; the classifier is orthogonal to cost.

> 与权限模式阶梯（第 10 课）结合。无 `max_budget_usd` 的 `autoMode` 会话是未治理的自主。Anthropic 明确将 Auto Mode 框定为需要预算控制；分类器与成本正交。

### EU AI Act, OWASP Agentic Top 10 | EU AI 法案、OWASP Agentic Top 10

Microsoft's Agent Governance Toolkit covers the OWASP Agentic Top 10 and the EU AI Act Article 14 (human oversight) requirements. For production in the EU, logging and cap enforcement are not optional.

> Microsoft 的 Agent Governance Toolkit 覆盖 OWASP Agentic Top 10 和 EU AI 法案第 14 条（人类监督）要求。对于 EU 生产，日志记录和上限执行不是可选的。

### The observed $1,200 → $4,800 case | 观察到的 $1,200 → $4,800 案例

The real case in the Microsoft docs: an e-commerce agent whose monthly cost tripled after a new tool was added.

> Microsoft 文档中的真实案例：一个电商 Agent 在添加新工具后月成本翻了三倍。

The tool allowed the agent to poll order status during every session. No loop detection. No per-tool cap. No alert on week-over-week growth. The fix was a per-tool cap plus a daily-growth alert. This is a template: every new tool surface is a new potential loop; every new tool needs its own cap and its own alert.

> 该工具允许 Agent 在每次会话期间轮询订单状态。无循环检测。无每工具上限。无周环比增长警报。修复是每工具上限加每日增长警报。这是模板：每个新工具面是新潜在循环；每个新工具需要自己的上限和自己的警报。

## Use It | 用框架实现

`code/main.py` simulates an agent run with and without a layered cost-governor stack. The simulated agent drifts into a polling loop after some turns; the layered stack catches it within the velocity window while a single monthly cap would not fire until days later.

> `code/main.py` 模拟有和没有分层成本治理栈的 Agent 运行。模拟 Agent 在某些轮次后漂移到轮询循环；分层栈在速度窗口内捕获它，而单一月度上限直到数天后才触发。

## Ship It | 产出物

`outputs/skill-agent-budget-audit.md` audits a proposed agent deployment's cost-governor stack and flags missing layers.

> `outputs/skill-agent-budget-audit.md` 审计提议的 Agent 部署的成本治理栈并标记缺失层。

## Exercises | 练习题

1. Run `code/main.py`. Confirm the velocity limit fires before the iteration cap on a polling-loop trajectory. Now disable the velocity limit and measure how much the agent "spends" before the iteration cap catches it.
   中文翻译：运行 `code/main.py`。确认速度限制在轮询循环轨迹的迭代上限前触发。现在禁用速度限制并测量 Agent 在迭代上限捕获前"花费"多少。

2. Design a per-tool cap set for a browser agent (Lesson 11). Which tool needs the tightest cap? Which tool can run unbounded without risk?
   中文翻译：为浏览器 Agent（第 11 课）设计每工具上限集。哪个工具需最紧上限？哪个工具可无界运行无风险？

3. Read the Microsoft Agent Governance Toolkit docs. List every cap type the toolkit names. Map each to one of the failure modes (runaway loop, slow leak, bad release, surge).
   中文翻译：阅读 Microsoft Agent Governance Toolkit 文档。列出工具包命名的每个上限类型。将各映射到失败模式之一（失控循环、缓慢泄漏、坏发布、激增）。

4. Price an overnight unattended run for a realistic task (e.g., "triage 50 issues in a repo"). Set `max_budget_usd` at 2x your point estimate. Justify the 2x.
   中文翻译：为真实任务（例如"分类 50 个仓库 issue"）定价隔夜无人值守运行。设置 `max_budget_usd` 为你点估计的 2x。论证 2x。

5. Claude Code's `max_budget_usd` fires on session aggregate cost. Design a complementary velocity limit you would enforce externally. What triggers the cut-off, and what does re-enable look like?
   中文翻译：Claude Code 的 `max_budget_usd` 在会话总成本上触发。设计你会在外部强制的互补速度限制。什么触发切断，重新启用什么样？

## Key Terms | 术语速查表

| Term | What people say | What it actually means |
|---|---|---|
| 术语 | 通俗说法 | 实际含义 |
| Denial of Wallet | "Runaway bill" | Agent loop generating spend with no cap to stop it |
| Denial of Wallet | "失控账单" | 无上限阻止的 Agent 循环产生花费 |
| max_tokens | "Per-request cap" | Ceiling on a single completion's size |
| max_tokens | "每请求上限" | 单次补全大小上限 |
| max_turns | "Iteration cap" | Ceiling on agent loop iterations in a session |
| max_turns | "迭代上限" | 会话中 Agent 循环迭代数上限 |
| max_budget_usd | "Dollar kill switch" | Session cost cap; aborts on breach |
| max_budget_usd | "美元终止开关" | 会话成本上限；违反时中止 |
| Velocity limit | "Rate cap" | Limit on spend per short window (e.g., $50 / 10 min) |
| 速度限制 | "速率上限" | 短窗口花费限制（例如 $50/10 分钟） |
| Tiered routing | "Small model first" | Cheap model default; escalate only when classifier warrants |
| 分层路由 | "小模型优先" | 默认廉价模型；仅当分类器批准时升级 |
| Prompt caching | "Cached system prompt" | Provider-side cache reduces re-send token cost to near zero |
| 提示缓存 | "缓存系统提示" | 提供商侧缓存将重发 token 成本降至接近零 |
| HITL checkpoint | "Human approval gate" | Human tap required before expensive action |
| HITL 检查点 | "人类批准门" | 昂贵动作前需人类点击 |

## Further Reading | 延伸阅读

- [Anthropic Claude Code Agent SDK — agent loop and budgets](https://code.claude.com/docs/en/agent-sdk/agent-loop) — `max_turns`, `max_budget_usd`, tool allowlists.
  中文翻译：`max_turns`、`max_budget_usd`、工具允许列表。
- [Microsoft Agent Framework — human-in-the-loop and governance](https://learn.microsoft.com/en-us/agent-framework/workflows/human-in-the-loop) — cost-governor checkpoints.
  中文翻译：成本治理器检查点。
- [Anthropic — Claude Managed Agents overview](https://platform.claude.com/docs/en/managed-agents/overview) — provider-side cost controls.
  中文翻译：提供商侧成本控制。
- [Anthropic — Prompt caching (Claude API docs)](https://platform.claude.com/docs/en/prompt-caching) — caching mechanics.
  中文翻译：缓存机制。
- [Anthropic — Measuring agent autonomy in practice](https://www.anthropic.com/research/measuring-agent-autonomy) — cost profile for long-horizon agents.
  中文翻译：长程 Agent 的成本档案。
