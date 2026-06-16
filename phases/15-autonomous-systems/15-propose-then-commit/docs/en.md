# Human-in-the-Loop: Propose-Then-Commit | 人类在环：提议-提交

> The 2026 consensus on HITL is specific. It is not "the agent asks, the user clicks Approve." It is propose-then-commit: the proposed action is persisted to a durable store with an idempotency key; surfaced to a reviewer with intent, data lineage, permissions touched, blast radius, and a rollback plan; committed only after positive acknowledgement; verified after execution to confirm the side effect actually happened. LangGraph's `interrupt()` plus PostgreSQL checkpointing, Microsoft Agent Framework's `RequestInfoEvent`, and Cloudflare's `waitForApproval()` all implement the same shape. The canonical failure mode is the rubber-stamp approval: "Approve?" is clicked without review. The documented mitigation is challenge-and-response with an explicit checklist.

> **【中文解读】** 2026 年 HITL 共识是具体的。不是"Agent 问，用户点击 Approve"。是 propose-then-commit：提议动作以幂等键持久化到持久存储；向审查者呈现意图、数据谱系、触及的权限、爆炸半径、回滚计划；仅在正面确认后提交；执行后验证确认副作用实际发生。LangGraph 的 `interrupt()` 加 PostgreSQL 检查点、Microsoft Agent Framework 的 `RequestInfoEvent`、Cloudflare 的 `waitForApproval()` 都实现相同形态。规范失败模式是橡皮章批准：无审查地点击"Approve?"。已记录的缓解是带显式清单的挑战-响应。

> **【拓展：四个状态机步骤】** propose-then-commit 是四步状态机：(1) 提议——Agent 产生动作，以幂等键持久化带意图/数据谱系/触及权限/爆炸半径/回滚计划；(2) 呈现——审查者（人类，非 Agent 自审）看到所有元数据；(3) 提交——正面确认，动作执行；(4) 验证——执行后回读副作用确认。这是数据库 `RETURNING` 子句、AWS `PutObject` 后 `GetObject`、Stripe/AWS API 幂等键模式在 Agent 审批上的复用。

**Type:** Learn | **类型:** 学习
**Languages:** Python (stdlib, propose-then-commit state machine with idempotency) | **语言:** Python（标准库，带幂等的提议-提交状态机）
**Prerequisites:** Phase 15 · 12 (Durable execution), Phase 15 · 14 (Tripwires) | **前置知识:** Phase 15 · 12（持久执行），Phase 15 · 14（触发器）
**Time:** ~60 minutes | **时间:** ~60 分钟

> 🔗 **【前置】** 学本节前请先掌握：Phase 15·12（Durable Execution）、Phase 15·14（Kill Switches）、Phase 14·15（HITL Agent 模式）。本节是 HITL 的工程化标准——四步状态机。
> 💡 **【类比】** Propose-then-Commit = "银行大额转账审批"。普通 LLM 调用 = 即时转账（错了找客服）；Propose-then-Commit = 提交转账申请（含收款人、金额、用途、回滚预案）→ 审查员看到元数据 → 批准 → 执行 → 验证到账。每一步都不能省。这是 Anthropic Computer Use、Claude Code Plan Mode、Stripe API 幂等键的统一模式。
> ⚠️ **【易错点】** "Approve?" 弹窗被用户惯性点"是" → 橡皮章失效。修复：(1) 多选清单（每个动作独立确认）；(2) 强制延迟（3 秒倒计时）；(3) 关键动作双确认（输入金额数字）；(4) 显示"爆炸半径"（影响 N 个文件、M 个用户）。

## The Problem | 问题引入

> **【中文解读】** 先提议后提交（Propose-Then-Commit）模式要求 Agent 先生成修改方案但不立即执行，而是展示给用户或其他 Agent 审查，审查通过后才提交。这是 Agent 安全的关键模式——将'思考'和'执行'分离，给人类或系统一个在执行前检查和纠正的机会。

> **【拓展：propose then commit】** 先提议后提交模式是 2026 年编码 Agent 的标准安全实践。Claude Code 默认使用这一模式——生成修改建议并等待用户确认。Git 的 PR/MR 机制也是这一模式的应用——代码修改先提出，经过审查后才合并。在 Agent 上下文中，这一模式特别重要，因为 Agent 的错误可能比人类错误更具破坏性。

An agent takes an action. The user has to decide: approve or not. If the decision is instant, it is probably not a review.

> Agent 采取行动。用户必须决定：批准还是不批准。如果决定是即时的，那可能不是审查。

If the decision is structured, it is slow but trustworthy. The engineering question is how to make a structured review the path of least resistance.

> 如果决定是结构化的，它慢但可信。工程问题是如何使结构化审查成为阻力最小路径。

The 2023-era HITL pattern was a synchronous prompt: "Agent wants to send email to X with body Y — approve?" The user clicks Approve. Everyone feels the system is safe. In practice this surface is heavily rubber-stamped: users approve fast, approvals predict little, and when the agent goes wrong, the audit trail shows a long history of approvals the user cannot recall.

> 2023 时代 HITL 模式是同步提示："Agent 要发邮件给 X，正文 Y——批准？"用户点击 Approve。每个人都感觉系统安全。实践中此界面被严重橡皮章化：用户快速批准，批准预测性低，当 Agent 出错时审计追踪显示用户无法回忆的长批准历史。

> **【中文解读】** 本节介绍了 AI Agent 的核心概念和实现方法。Agent 是 LLM 驱动的自主系统，能够观察环境、思考决策、执行行动并循环迭代直到完成目标。

The 2026 pattern — propose-then-commit — moves HITL onto a durable substrate, attaches structured metadata, and requires positive commit.

> 2026 年模式——propose-then-commit——将 HITL 移到持久基板上，附加结构化元数据，要求正面提交。

Every managed agent SDK ships a version: LangGraph `interrupt()`, Microsoft Agent Framework `RequestInfoEvent`, Cloudflare `waitForApproval()`. The API names differ; the shape does not.

> 每个托管 Agent SDK 出货一版：LangGraph `interrupt()`、Microsoft Agent Framework `RequestInfoEvent`、Cloudflare `waitForApproval()`。API 名称不同；形态不。

## The Concept | 核心概念

### The propose-then-commit state machine | propose-then-commit 状态机

1. **Propose.** Agent produces a proposed action. Persisted to a durable store (PostgreSQL, Redis, Durable Object). Includes:
   中文翻译：**提议。** Agent 产生提议动作。持久化到持久存储（PostgreSQL、Redis、Durable Object）。包括：
   - intent (why is the agent doing this)
     中文翻译：意图（Agent 为什么做这个）
   - data lineage (what source led to this proposal)
     中文翻译：数据谱系（什么源导致此提议）
   - permissions touched (which scopes / files / endpoints)
     中文翻译：触及的权限（哪些范围/文件/端点）
   - blast radius (what is the worst case)
     中文翻译：爆炸半径（最坏情况是什么）
   - rollback plan (if committed, how do we undo it)
     中文翻译：回滚计划（如提交，如何撤销）
   - idempotency key (unique per proposal; resubmission returns the same record)
     中文翻译：幂等键（每提议唯一；重提交返回同一记录）
2. **Surface.** Reviewer sees the proposal with all metadata. The reviewer is a person (not the agent reviewing itself).
   中文翻译：**呈现。** 审查者看到带所有元数据的提议。审查者是个人（不是 Agent 自审）。
3. **Commit.** Positive acknowledgement. The action executes.
   中文翻译：**提交。** 正面确认。动作执行。
4. **Verify.** After execution, the side effect is read back and confirmed. If the verify step fails, the system is in a known bad state and alerting engages.
   中文翻译：**验证。** 执行后副作用被回读确认。如果验证步骤失败，系统处于已知坏状态并启动警报。

### The idempotency key | 幂等键

Without an idempotency key, a retry after a transient failure can double-execute an approved action.

> 没有幂等键，瞬态失败后的重试可能双倍执行已批准动作。

Concrete example: user approves "transfer $100 from A to B." Network blips. Workflow retries. The user has approved once but the transfer executes twice. The idempotency key ties the approval to a single, unique side effect; the second execution is a no-op.

> 具体例子：用户批准"从 A 转 $100 到 B"。网络闪断。工作流重试。用户批准一次但转账执行两次。幂等键将批准绑定到单一唯一副作用；第二次执行是 no-op。

This is the same idempotency pattern Stripe and AWS APIs use. Reusing it for agent approvals is explicit in the Microsoft Agent Framework docs.

> 这是 Stripe 和 AWS API 使用的相同幂等模式。Microsoft Agent Framework 文档明确将其复用于 Agent 批准。

### Durability: why approvals outlast processes | 持久性：为什么批准比进程寿命长

The approval waiting room is a piece of state the agent does not own. The workflow is paused (Lesson 12). When the approval arrives, the workflow resumes from exactly that point. This is why LangGraph pairs `interrupt()` with PostgreSQL checkpointing and not just in-memory state — an approval two days later still finds the workflow intact.

> 批准等候室是 Agent 不拥有的一片状态。工作流暂停（第 12 课）。批准到达时，工作流从该精确点恢复。这就是为什么 LangGraph 将 `interrupt()` 与 PostgreSQL 检查点配对而非仅内存状态——两天后的批准仍找到完整工作流。

### Rubber-stamp approvals and the challenge-and-response mitigation | 橡皮章批准和挑战-响应缓解

The default UI for HITL ("Approve" / "Reject" buttons) produces fast approvals with no genuine review. Documented mitigation: a challenge-and-response checklist that requires positive answers to specific questions before the Approve button is enabled. Concrete shape:

> HITL 默认 UI（"Approve"/"Reject" 按钮）产生快速批准无真实审查。已记录缓解：在 Approve 按钮启用前要求对特定问题正面回答的挑战-响应清单。具体形状：

- "Do you understand what resource this touches? [ ]"
  中文翻译："你了解这触及什么资源吗？[ ]"
- "Have you verified the blast radius is acceptable? [ ]"
  中文翻译："你验证了爆炸半径可接受吗？[ ]"
- "Do you have a rollback plan if this fails? [ ]"
  中文翻译："如果失败你有回滚计划吗？[ ]"

Not bureaucracy for its own sake — a forcing function. The reviewer who cannot tick the boxes either asks for clarification (escalation) or declines (safe default). The Anthropic agent-safety research explicitly cites checklist-driven HITL as a mitigation for rubber-stamp approval patterns.

> 不是为官僚而官僚——是强制函数。不能勾选框的审查者要么要求澄清（升级）要么拒绝（安全默认）。Anthropic Agent 安全研究明确引用清单驱动 HITL 作为橡皮章批准模式的缓解。

### What counts as consequential | 什么算后果性

Not every action needs propose-then-commit. The 2026 guidance:

> 不是每个动作都需要 propose-then-commit。2026 指导：

- **Consequential actions** (always HITL): irreversible writes, financial transactions, outbound communication, production database changes, destructive file-system operations.
  中文翻译：**后果性动作**（总 HITL）：不可逆写、金融交易、外发通信、生产数据库变更、破坏性文件系统操作。
- **Reversible actions** (sometimes HITL): edits to local files, staging-env changes, reversible writes with clear rollback.
  中文翻译：**可逆动作**（有时 HITL）：本地文件编辑、staging 环境变更、带清晰回滚的可逆写。
- **Reads and inspections** (never HITL): reading a file, listing resources, calling a read-only API.
  中文翻译：**读和检查**（从不 HITL）：读文件、列资源、调用只读 API。

### Post-action verification | 动作后验证

"The commit ran" is not the same as "the side effect happened." Network-partition and race conditions can produce a workflow that thinks it succeeded while the backend did not persist. The verify step re-reads the target resource after commit to confirm. This is the same pattern as database transactions with `RETURNING` clauses or AWS `GetObject` after `PutObject`.

> "提交运行了"不等于"副作用发生了"。网络分区和竞态条件可产生工作流以为成功而后端未持久化。验证步骤在提交后回读目标资源确认。这与带 `RETURNING` 子句的数据库事务或 `PutObject` 后 `GetObject` 的 AWS 相同模式。

### EU AI Act Article 14 | EU AI 法案第 14 条

Article 14 mandates effective human oversight for high-risk AI systems in the EU. "Effective" is not decorative. Regulatory language specifically excludes rubber-stamp patterns. Propose-then-commit with challenge-and-response is the shape that survives Article 14 scrutiny in the Microsoft Agent Governance Toolkit compliance docs.

> 第 14 条强制 EU 高风险 AI 系统的有效人类监督。"有效"不是装饰性。监管语言明确排除橡皮章模式。带挑战-响应的 propose-then-commit 是在 Microsoft Agent Governance Toolkit 合规文档中通过第 14 条审查的形态。

## Use It | 用框架实现

`code/main.py` implements a propose-then-commit state machine in stdlib Python. Durable store is a JSON file. Idempotency key is a hash of (thread_id, action_signature). The driver simulates three cases: a clean approval flow, a retry after transient failure (which must not double-execute), and a rubber-stamp default versus a challenge-and-response flow.

> `code/main.py` 用标准库 Python 实现 propose-then-commit 状态机。持久存储是 JSON 文件。幂等键是 (thread_id, action_signature) 的哈希。驱动器模拟三例：干净批准流、瞬态失败后的重试（必须不双倍执行）、橡皮章默认 vs 挑战-响应流。

## Ship It | 产出物

`outputs/skill-hitl-design.md` reviews a proposed HITL workflow for propose-then-commit shape and flags missing metadata, idempotency, verification, or challenge-and-response layers.

> `outputs/skill-hitl-design.md` 审查提议 HITL 工作流的 propose-then-commit 形态并标记缺失的元数据、幂等、验证或挑战-响应层。

## Exercises | 练习题

1. Run `code/main.py`. Confirm that a retry of an approved proposal uses the durable record and does not re-execute. Now change the idempotency key to include a timestamp and show the retry double-executes.
   中文翻译：运行 `code/main.py`。确认已批准提议的重试使用持久记录且不重新执行。现在将幂等键改为包含时间戳并展示重试双倍执行。

2. Extend the proposal record with a `rollback` field. Simulate an execution whose verify step fails. Show the rollback firing automatically.
   中文翻译：用 `rollback` 字段扩展提议记录。模拟验证步骤失败的执行。展示回滚自动触发。

3. Read Microsoft Agent Framework's `RequestInfoEvent` docs. Identify one metadata field the API includes that the toy engine is missing. Add it and explain what it protects against.
   中文翻译：阅读 Microsoft Agent Framework 的 `RequestInfoEvent` 文档。识别 API 包含而玩具引擎缺失的一个元数据字段。添加它并解释它防止什么。

4. Design a challenge-and-response checklist for a specific action (e.g., "post to a public Twitter account"). What three questions must the reviewer answer? Why those three?
   中文翻译：为特定动作（例如"发到公共 Twitter 账号"）设计挑战-响应清单。审查者必须回答哪三个问题？为什么这三个？

5. Pick one case where a synchronous "Approve?" prompt would be sufficient (no durable store needed). Explain why, and name the risk class you are accepting.
   中文翻译：选一个同步"Approve?"提示就足够（不需持久存储）的案例。解释为什么，并命名你接受的风险类。

## Key Terms | 术语速查表

| Term | What people say | What it actually means |
|---|---|---|
| 术语 | 通俗说法 | 实际含义 |
| Propose-then-commit | "Two-phase approval" | Persisted proposal + positive commit + verify |
| Propose-then-commit | "两阶段批准" | 持久提议 + 正面提交 + 验证 |
| Idempotency key | "Retry-safe token" | Unique per proposal; second execution no-ops |
| 幂等键 | "重试安全 token" | 每提议唯一；第二次执行 no-op |
| Data lineage | "Where it came from" | The specific source content that led to the proposal |
| 数据谱系 | "它从哪来" | 导致提议的特定源内容 |
| Blast radius | "Worst case" | Scope of effect if the action goes wrong |
| 爆炸半径 | "最坏情况" | 动作出错时的影响范围 |
| Rubber-stamp | "Fast approval" | "Approve" clicked without genuine review |
| 橡皮章 | "快速批准" | 无真实审查地点击"Approve" |
| Challenge-and-response | "Forcing checklist" | Reviewer must positively acknowledge specific questions |
| 挑战-响应 | "强制清单" | 审查者必须正面确认特定问题 |
| RequestInfoEvent | "MS Agent Framework primitive" | Durable HITL request with structured metadata |
| RequestInfoEvent | "MS Agent Framework 原语" | 带结构化元数据的持久 HITL 请求 |
| `interrupt()` / `waitForApproval()` | "Framework primitives" | LangGraph / Cloudflare equivalents of the same shape |
| `interrupt()` / `waitForApproval()` | "框架原语" | 相同形态的 LangGraph / Cloudflare 等价物 |

## Further Reading | 延伸阅读

- [Microsoft Agent Framework — Human in the loop](https://learn.microsoft.com/en-us/agent-framework/workflows/human-in-the-loop) — `RequestInfoEvent`, durable approvals.
  中文翻译：`RequestInfoEvent`、持久批准。
- [Cloudflare Agents — Human in the loop](https://developers.cloudflare.com/agents/concepts/human-in-the-loop/) — `waitForApproval()` and Durable Objects.
  中文翻译：`waitForApproval()` 和 Durable Objects。
- [Anthropic — Measuring agent autonomy in practice](https://www.anthropic.com/research/measuring-agent-autonomy) — HITL as a mitigation for long-horizon risk.
  中文翻译：HITL 作为长程风险缓解。
- [EU AI Act — Article 14: Human oversight](https://artificialintelligenceact.eu/article/14/) — regulatory baseline for high-risk systems.
  中文翻译：高风险系统的监管基线。
- [Anthropic — Claude's Constitution (January 2026)](https://www.anthropic.com/news/claudes-constitution) — constitutional framing around oversight.
  中文翻译：监督的宪法框架。
