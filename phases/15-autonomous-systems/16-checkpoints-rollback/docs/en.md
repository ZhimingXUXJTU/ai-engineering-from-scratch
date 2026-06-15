# Checkpoints and Rollback | 检查点与回滚

> Every graph-state transition persists. When a worker crashes, its lease expires and another worker picks up at the latest checkpoint. Cloudflare Durable Objects hold state across hours or weeks. Propose-then-commit (Lesson 15) defines a rollback plan per action. Post-action verification closes the loop. EU AI Act Article 14 makes effective human oversight mandatory for high-risk systems — in practice this means checkpoints must be queryable, rollbacks must be rehearsed, and the audit trail must survive a deploy. The sharp failure mode: without idempotency keys and precondition checks, a retry after a transient failure can double-execute an already-approved action. Post-action verification is what catches it.

> **【中文解读】** 每个图状态转换持久化。worker 崩溃时其租约过期，另一 worker 在最新检查点拾起。Cloudflare Durable Objects 跨数小时或数周持有状态。Propose-then-commit（第 15 课）为每个动作定义回滚计划。动作后验证闭合循环。EU AI 法案第 14 条使高风险系统的有效人类监督强制——实践中意味着检查点必须可查询、回滚必须演练、审计追踪必须跨部署存活。尖锐失败模式：没有幂等键和前置条件检查，瞬态失败后的重试可能双倍执行已批准动作。动作后验证捕获它。

> **【拓展：幂等+前置条件+验证+回滚四件套】** 仅幂等不够：考虑"当余额 > $1000 时从 A 转 $100 到 B"的批准动作。执行中崩溃后恢复，仅幂等检查会通过，但若 A 余额在崩溃和恢复间通过另一工作流降到 $500，前置条件检查失败——没有它就发透支。每个后果性动作需要四件套：幂等键（防双倍）+ 前置条件（状态仍与批准一致）+ 动作后验证（副作用真的发生）+ 验证失败时回滚。

**Type:** Learn | **类型:** 学习
**Languages:** Python (stdlib, checkpoint and rollback state machine) | **语言:** Python（标准库，检查点和回滚状态机）
**Prerequisites:** Phase 15 · 12 (Durable execution), Phase 15 · 15 (Propose-then-commit) | **前置知识:** Phase 15 · 12（持久执行），Phase 15 · 15（propose-then-commit）
**Time:** ~60 minutes | **时间:** ~60 分钟

## The Problem | 问题引入

> **【中文解读】** 检查点和回滚机制允许 Agent 在执行过程中保存状态快照，出错时恢复到之前的良好状态。这类似于数据库的事务和 Git 的版本控制。检查点保存在关键节点（如修改文件前），回滚在检测到错误时执行。LangGraph 的内置检查点和 Git 的 revert 是两个典型实现。

> **【拓展：checkpoints rollback】** 检查点-回滚是可靠 Agent 系统的基础设施。实现选择：(1) 文件系统级——使用 Git 或快照保存文件状态；(2) 数据库级——使用事务保证数据一致性；(3) 应用级——Agent 自己管理检查点（如 LangGraph）。关键权衡是检查点粒度——太细会增加开销，太粗会丢失更多工作。

Durable execution (Lesson 12) makes a crashed agent resumable. Propose-then-commit (Lesson 15) makes an approved action auditable.

> 持久执行（第 12 课）使崩溃 Agent 可恢复。Propose-then-commit（第 15 课）使批准动作可审计。

This lesson joins them: what happens when an approved action executes partially, crashes, and resumes? When does the rollback run, and against what state?

> 本课连接它们：当批准动作部分执行、崩溃、恢复时会发生什么？回滚何时运行，针对什么状态？

Real systems wire this up differently:

> 真实系统连接方式不同：

> **【中文解读】** 本节介绍了 AI Agent 的核心概念和实现方法。Agent 是 LLM 驱动的自主系统，能够观察环境、思考决策、执行行动并循环迭代直到完成目标。

- **LangGraph** checkpoints every graph-state transition to PostgreSQL. On worker crash, the lease releases and another worker resumes at the latest checkpoint. Workflows pause on `interrupt()`, which itself persists.
  中文翻译：**LangGraph** 将每个图状态转换检查点到 PostgreSQL。worker 崩溃时租约释放另一 worker 在最新检查点恢复。工作流在 `interrupt()` 上暂停，其本身持久化。
- **Cloudflare Durable Objects** hold per-key state across hours or weeks. Co-locate the computation with the storage for the approved action.
  中文翻译：**Cloudflare Durable Objects** 跨数小时或数周持有每键状态。将计算与已批准动作的存储同址。
- **Microsoft Agent Framework** exposes `Checkpoint` primitives in the workflow API; replay plus idempotency covers retries.
  中文翻译：**Microsoft Agent Framework** 在工作流 API 中暴露 `Checkpoint` 原语；重放加幂等覆盖重试。

In every case, the combination that actually works is: idempotency key + precondition check + post-action verify + rollback on verify-fail.

> 每个情况下实际有效的组合是：幂等键 + 前置条件检查 + 动作后验证 + 验证失败时回滚。

## The Concept | 核心概念

### Every transition persists | 每个转换持久化

A graph-state transition is any step that moves the workflow from one named state to another. Naive implementations persist only at specific commit points; production implementations persist every transition. The cost (a few extra writes) is small relative to the reliability gain (replay lands anywhere, lease recovery is precise).

> 图状态转换是将工作流从一个命名状态移到另一命名状态的任何步骤。朴素实现只在特定提交点持久化；生产实现持久化每个转换。成本（几次额外写）相对可靠性收益（重放落在任何地方、租约恢复精确）小。

### Lease recovery | 租约恢复

When a worker crashes, the workflow is not lost; the lease (a short-lived claim that this worker is executing this run) simply expires. Another worker picks up the latest checkpoint and resumes. The lease mechanism is what lets production systems survive rolling deploys without losing in-flight work.

> worker 崩溃时工作流不丢失；租约（此 worker 正在执行此运行的短暂声明）只是过期。另一 worker 拾起最新检查点恢复。租约机制让生产系统在不丢失进行中工作的情况下存活滚动部署。

### Idempotency plus preconditions | 幂等加前置条件

Idempotency alone is not enough. Consider: a workflow is approved to "transfer $100 from A to B when balance > $1000." The workflow is committed, crashes mid-execution, and resumes. If only the idempotency key is checked, and the execution resumes, the transfer runs once (correct). But consider that between crash and resume, A's balance drops to $500 via a different workflow. The idempotency check still passes; the precondition does not. Without a precondition check, we ship an overdraft.

> 仅幂等不够。考虑：工作流被批准"当余额 > $1000 时从 A 转 $100 到 B"。工作流提交、执行中崩溃、恢复。若仅检查幂等键执行恢复，转账运行一次（正确）。但考虑崩溃和恢复间 A 余额通过另一工作流降到 $500。幂等检查仍通过；前置条件不。没有前置条件检查，我们发透支。

Every consequential action needs both:

> 每个后果性动作需要两者：

- **Idempotency key**: prevents double-execute.
  中文翻译：**幂等键**：防止双倍执行。
- **Precondition check**: confirms the state is still consistent with what was approved.
  中文翻译：**前置条件检查**：确认状态仍与批准的一致。

### Post-action verification | 动作后验证

"The tool returned 200" is not verification. Real verification re-reads the target state and confirms the side effect actually happened. Patterns:

> "工具返回 200"不是验证。真实验证回读目标状态确认副作用实际发生。模式：

- Database update: `UPDATE ... RETURNING *` then assert the returned row matches intended state.
  中文翻译：数据库更新：`UPDATE ... RETURNING *` 然后断言返回行匹配预期状态。
- Email send: check sent-folder for the message ID after submission.
  中文翻译：邮件发送：提交后检查 sent-folder 中的消息 ID。
- File write: read the file back and hash it.
  中文翻译：文件写：回读文件并哈希。
- API call: follow-up `GET` on the target resource.
  中文翻译：API 调用：对目标资源的后续 `GET`。

If verify fails, the workflow is in a known-bad state. Rollback engages.

> 验证失败时工作流处于已知坏状态。回滚启动。

### Rollback plans | 回滚计划

Every consequential action in propose-then-commit (Lesson 15) carries a rollback plan. Types:

> propose-then-commit（第 15 课）中每个后果性动作带回滚计划。类型：

- **In-band rollback**: reverse the side effect directly (`DELETE` after `INSERT`, `Send-correction-email` after send).
  中文翻译：**带内回滚**：直接反转副作用（`INSERT` 后 `DELETE`、发送后发送更正邮件）。
- **Compensating transaction**: a new action that neutralizes the original (standard SAGA pattern).
  中文翻译：**补偿事务**：抵消原始动作的新动作（标准 SAGA 模式）。
- **Out-of-band rollback**: alert a human, pause the workflow, leave the bad state for investigation.
  中文翻译：**带外回滚**：警报人类、暂停工作流、留下坏状态供调查。

No-op rollback ("we cannot undo this") must be named in the proposal. Actions with no rollback require stronger HITL at commit time (Lesson 15 challenge-and-response).

> No-op 回滚（"我们不能撤销此"）必须在提议中命名。无回滚动作在提交时需更强 HITL（第 15 课挑战-响应）。

### EU AI Act Article 14 operational reading | EU AI 法案第 14 条运营解读

Article 14 requires "effective human oversight" for high-risk systems. In operational terms, implementers read it as:

> 第 14 条要求高风险系统的"有效人类监督"。运营术语中，实现者读为：

- Checkpoints are queryable by an auditor.
  中文翻译：检查点可被审计者查询。
- Rollbacks are rehearsed (tested end-to-end at least once).
  中文翻译：回滚演练（至少端到端测试一次）。
- The audit trail survives a deploy (checkpoint backend is not ephemeral).
  中文翻译：审计追踪跨部署存活（检查点后端非临时）。
- Failed verifications are alerted on, not silently logged.
  中文翻译：失败验证被警报而非静默记录。

A workflow that crashes mid-commit, resumes, and completes the side effect without a verify + rollback pathway does not survive the Article 14 test.

> 提交中崩溃、恢复、无验证+回滚路径完成副作用的工作流不通过第 14 条测试。

### The sharp failure mode: the double-execute | 尖锐失败模式：双倍执行

The most common production incident in this space: Action approved, commit starts, returns 200, workflow crashes before persisting status, resumes and re-executes.

> 此领域最常见生产事故：动作批准、提交开始、返回 200、工作流在持久化状态前崩溃、恢复并重新执行。

1. Action approved, idempotency key k.
   中文翻译：动作批准，幂等键 k。
2. Commit starts, executes, returns 200.
   中文翻译：提交开始、执行、返回 200。
3. Workflow crashes before persisting the "committed" status.
   中文翻译：工作流在持久化"已提交"状态前崩溃。
4. Workflow resumes; sees "approved but not committed"; re-executes.
   中文翻译：工作流恢复；看到"批准但未提交"；重新执行。
5. Side effect fires twice.
   中文翻译：副作用触发两次。

Mitigation: persist an "in-flight" intent before execution, execute with an idempotency key, then mark "committed" only after post-action verification succeeds. If the action fires and the status write fails, you know to verify and (if necessary) re-fire. If the status write succeeds and the action fails, you verify and fire exactly once via the recovery path.

> 缓解：执行前持久化"in-flight"意图，用幂等键执行，仅在动作后验证成功后标记"已提交"。如动作触发而状态写失败，你知道要验证（如必要）重触发。如状态写成功而动作失败，你验证并通过恢复路径精确触发一次。

## Use It | 用框架实现

`code/main.py` implements a checkpointed workflow with idempotency, preconditions, verify, and rollback. The driver simulates four scenarios: clean run, retry after crash (idempotency catches), precondition fail (workflow aborts without firing), verify fail (rollback fires).

> `code/main.py` 实现带幂等、前置条件、验证和回滚的检查点工作流。驱动器模拟四场景：干净运行、崩溃后重试（幂等捕获）、前置条件失败（工作流中止不触发）、验证失败（回滚触发）。

## Ship It | 产出物

`outputs/skill-rollback-rehearsal.md` designs a rollback-rehearsal test for a proposed workflow and audits the checkpoint backend for audit-trail persistence.

> `outputs/skill-rollback-rehearsal.md` 为提议工作流设计回滚演练测试并审计检查点后端的审计追踪持久性。

## Exercises | 练习题

1. Run `code/main.py`. Verify the four scenarios. For the crash-during-commit case, confirm the action fires exactly once across retries.
   中文翻译：运行 `code/main.py`。验证四场景。对提交中崩溃案例，确认动作在重试间精确触发一次。

2. Modify the "mark as done first, then do it" pattern so the status write fires after the action. Rerun the crash scenario. Measure how many duplicate actions fire.
   中文翻译：修改"先标记完成再做"模式使状态写在动作后触发。重跑崩溃场景。测量多少重复动作触发。

3. Design a rollback plan for a specific production action (e.g., "post to a Slack channel"). Classify as in-band, compensating, or out-of-band. Justify the choice.
   中文翻译：为特定生产动作（例如"发到 Slack 频道"）设计回滚计划。分类为带内、补偿或带外。论证选择。

4. Take one workflow you know. Identify every state transition. Mark each with a durability requirement (persist / do not persist). Count the ones you are currently not persisting.
   中文翻译：取一个你了解的工作流。识别每个状态转换。标记各的持久性要求（持久化/不持久化）。计数你当前不持久化的。

5. Rehearsed-rollback test: design an end-to-end test that runs a real workflow, crashes it, and confirms the rollback path fires. What does the test assert?
   中文翻译：演练回滚测试：设计端到端测试运行真实工作流、崩溃、确认回滚路径触发。测试断言什么？

## Key Terms | 术语速查表

| Term | What people say | What it actually means |
|---|---|---|
| 术语 | 通俗说法 | 实际含义 |
| Checkpoint | "Save point" | Every graph-state transition persists to a durable store |
| 检查点 | "保存点" | 每个图状态转换持久化到持久存储 |
| Lease | "Worker claim" | Short-lived claim that a worker is executing a run; expires on crash |
| 租约 | "Worker 声明" | worker 正在执行运行的短暂声明；崩溃时过期 |
| Precondition | "State gate" | Assertion that the state is still consistent with the approved action |
| 前置条件 | "状态门" | 状态仍与批准动作一致的断言 |
| Post-action verify | "Re-read check" | Confirm the side effect actually happened in the target system |
| 动作后验证 | "回读检查" | 确认副作用在目标系统中实际发生 |
| In-band rollback | "Direct undo" | Reverse the side effect with the inverse operation |
| 带内回滚 | "直接撤销" | 用逆操作反转副作用 |
| Compensating transaction | "SAGA undo" | A new action that neutralizes the original |
| 补偿事务 | "SAGA 撤销" | 抵消原始动作的新动作 |
| Mark-as-done-first | "Status write order" | Persist the committed status before returning from commit |
| 先标记完成 | "状态写顺序" | 从提交返回前持久化已提交状态 |
| Article 14 | "EU AI Act human oversight" | Operational: queryable checkpoints, rehearsed rollbacks, auditable trail |
| 第 14 条 | "EU AI 法案人类监督" | 运营：可查询检查点、演练回滚、可审计追踪 |

## Further Reading | 延伸阅读

- [Microsoft Agent Framework — Checkpointing and HITL](https://learn.microsoft.com/en-us/agent-framework/workflows/human-in-the-loop) — checkpoint primitives and lease recovery.
  中文翻译：检查点原语和租约恢复。
- [Cloudflare Agents — Human in the loop](https://developers.cloudflare.com/agents/concepts/human-in-the-loop/) — Durable Objects as a state substrate.
  中文翻译：Durable Objects 作为状态基板。
- [EU AI Act — Article 14: Human oversight](https://artificialintelligenceact.eu/article/14/) — regulatory baseline.
  中文翻译：监管基线。
- [Anthropic — Measuring agent autonomy in practice](https://www.anthropic.com/research/measuring-agent-autonomy) — reliability framing for long-horizon workflows.
  中文翻译：长程工作流的可靠性框架。
- [Anthropic — Claude Code Agent SDK: agent loop](https://code.claude.com/docs/en/agent-sdk/agent-loop) — workflow shape for Claude Code Routines.
  中文翻译：Claude Code Routines 的工作流形态。
