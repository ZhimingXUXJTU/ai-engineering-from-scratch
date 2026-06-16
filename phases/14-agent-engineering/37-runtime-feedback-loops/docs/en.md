# Runtime Feedback Loops | 反馈 运行时 循环

> Agents that do not see real command output guess. A feedback runner captures stdout, stderr, exit code, and timing into a structured record the next turn can read. Then the agent reacts to facts instead of to its own prediction of facts.

**Type:** Build | **类型:** 构建
**Languages:** Python (stdlib) | **语言:** Python (标准库)
**Prerequisites:** Phase 14 · 32 (Minimal Workbench), Phase 14 · 35 (Init Script) | **前置知识:** 见原文
**Time:** ~50 minutes | **时间:** 见原文

> 🔗 **【前置】** 学本节前请先掌握：Phase 14·32（Minimal Workbench）、Phase 14·35（Init Script）。本节讲"运行时反馈"——让 Agent 看到命令的真实输出而非自己猜测。
> 💡 **【类比】** 反馈循环 = 闭眼做饭 vs 睁眼做饭。盲猜"煮 5 分钟应该熟了"= 不看输出；睁眼看到"水还没开"= 看真实反馈再决定。Agent 不读 stderr，等于盲改代码；本节教如何把 stdout/stderr 结构化给 Agent 看。

## Learning Objectives | 学习目标

- Distinguish runtime feedback from observability telemetry.
- Build a feedback runner that wraps shell commands and persists structured records.
- Truncate large outputs deterministically so the loop stays within token budget.
- Refuse to advance the loop when feedback is missing.

## The Problem | 问题引入

The agent says "running tests now." The next message says "all tests pass." The reality is that no test ran. The agent imagined the output, or it ran the command and never read the result, or it read the result and silently truncated the failure line.

> Agent 说"现在运行测试"。下一条消息说"所有测试通过"。实际情况是没有运行任何测试。Agent 想象了输出，或者运行了命令但从未读取结果，或者读取了结果但默默地截断了失败行。

A feedback runner removes that gap. Every command goes through the runner. Every record carries the command, the captured stdout and stderr, the exit code, the wall-clock duration, and a one-line agent note. The agent reads the record at the next turn. The verification gate reads the records at the end of the task.

> 反馈运行器消除了这个差距。每个命令都通过运行器。每条记录携带命令、捕获的 stdout 和 stderr、退出码、挂钟时间和一行 Agent 备注。Agent 在下一轮读取记录。验证门控在任务结束时读取记录。


> **【中文解读】** 运行时反馈循环让 Agent 在执行过程中持续获取反馈。三种反馈类型：(1) 工具反馈——命令输出、编译结果、测试结果；(2) 用户反馈——中途中断和纠正；(3) 系统反馈——资源使用、错误率、超时。反馈循环是 Agent 自适应调整的基础。

## The Concept | 核心概念

```mermaid
flowchart LR
  Agent[Agent Loop] --> Runner[run_with_feedback.py]
  Runner --> Shell[subprocess]
  Shell --> Capture[stdout / stderr / exit / duration]
  Capture --> Record[feedback_record.jsonl]
  Record --> Agent
  Record --> Gate[Verification Gate]
```


> **【中文解读】** 运行时反馈循环让 Agent 在执行过程中持续获取反馈。三种反馈类型：(1) 工具反馈——命令输出、编译结果、测试结果；(2) 用户反馈——中途中断和纠正；(3) 系统反馈——资源使用、错误率、超时。反馈循环是 Agent 自适应调整的基础。

### What goes in a feedback record

| Field | Why it matters |
|-------|----------------|
| `command` | Exact argv, no shell expansion surprises |
| `stdout_tail` | Last N lines, deterministic truncation |
| `stderr_tail` | Last N lines, separate from stdout |
| `exit_code` | The unambiguous success signal |
| `duration_ms` | Surfaces slow probes and runaway processes |
| `started_at` | Timestamp for replay |
| `agent_note` | One line the agent writes about what it expected |

### Truncation is deterministic

A 50 MB log destroys the loop. The runner truncates head and tail with a `...truncated N lines...` marker, deterministic so the same output always produces the same record. No sampling; the parts the agent needs to see (final error, final summary) live at the tail.

> 运行时反馈循环在 Agent 执行过程中提供实时纠错。通过监控 Agent 行为并在检测到问题时立即干预，提高成功率。

### Feedback versus telemetry

Telemetry (Phase 14 · 23, OTel GenAI conventions) is for human operators reviewing runs across time. Feedback is for the next turn of this run. They share fields but they live in different files with different retention.

> 运行时反馈循环在 Agent 执行过程中提供实时纠错。通过监控 Agent 行为并在检测到问题时立即干预，提高成功率。

### Refuse to advance without feedback

If the runner errors before capturing exit, the record carries `exit_code: null` and `error: <reason>`. The agent loop must refuse to claim success on a `null` exit. No exit, no progress.

> 运行时反馈循环在 Agent 执行过程中提供实时纠错。通过监控 Agent 行为并在检测到问题时立即干预，提高成功率。

## Build It | 动手实现

`code/main.py` implements:

- `run_with_feedback(command, agent_note)` that wraps `subprocess.run`, captures stdout/stderr/exit/duration, truncates deterministically, appends to `feedback_record.jsonl`.
- A small loader that streams the JSONL into a Python list.
- A demo that runs three commands (success, failure, slow) and prints the last record per command.

Run it:

```
python3 code/main.py
```

Output: three feedback records appended to `feedback_record.jsonl`, the last one of each printed inline. Tail the file across re-runs to see the loop accumulate.

> 运行时反馈循环在 Agent 执行过程中提供实时纠错。通过监控 Agent 行为并在检测到问题时立即干预，提高成功率。

## Production patterns in the wild

Three patterns harden the runner enough to ship.

**Redact at write, not at read.** Any record that touches stdout or stderr can leak secrets. The runner ships a redaction pass before the JSONL append: strip lines matching `^Bearer `, `password=`, `api[_-]?key=`, `AKIA[0-9A-Z]{16}` (AWS), `xox[baprs]-` (Slack). Redaction at read time is a foot-gun; the file on disk is what an attacker reaches. Audit the redaction patterns quarterly against the production runtime's observed secret formats.

**Rotation policy, not a single file.** Cap `feedback_record.jsonl` at 1 MB per file; on overflow rotate to `.1`, `.2`, drop `.5`. The agent's loop only reads the current file, so the runtime cost is bounded. CI artifact storage gets the full rotated set. Without rotation the file becomes the bottleneck on every loader call.

**Parent-command id for retry chains.** Every record gets `command_id`; retries carry `parent_command_id` pointing at the previous attempt. The reviewer's "failed attempts" list (Phase 14 · 40) and the verification gate's audit both follow the chain. Without this link, retries look like independent successes and the audit hides the failure history.

## Use It | 用框架实现

Production patterns:

- **Claude Code Bash tool.** The tool already captures stdout, stderr, exit, and duration. The runner in this lesson is the framework-agnostic equivalent for any agent product.
- **LangGraph nodes.** Wrap any shell node in the runner so the record persists outside graph state.
- **CI logs.** Pipe the JSONL into your CI artifact store; reviewers can replay any command without rerunning the session.

The runner is a thin wrapper that survives every framework migration because it owns the shape of the record.

> 运行时反馈循环在 Agent 执行过程中提供实时纠错。通过监控 Agent 行为并在检测到问题时立即干预，提高成功率。

## Ship It | 产出物

`outputs/skill-feedback-runner.md` generates a project-specific `run_with_feedback.py` with the right truncation budget, a JSONL writer wired to the workbench, and a loader the agent reads at every turn.

> 运行时反馈循环在 Agent 执行过程中提供实时纠错。通过监控 Agent 行为并在检测到问题时立即干预，提高成功率。

## Exercises | 练习题

1. Add a `cwd` field per record so the same command run from different directories is distinguishable.
  中文翻译：思考并实践此练习。
2. Add a `redaction` step that strips lines matching `^Bearer ` or `password=`. Test on a fixture record.
  中文翻译：思考并实践此练习。
3. Cap total `feedback_record.jsonl` size at 1 MB by rotating to `.1`, `.2` files. Defend the rotation policy.
  中文翻译：思考并实践此练习。
4. Add a `parent_command_id` so retry chains are visible: which command produced the input that the next command consumed.
  中文翻译：思考并实践此练习。
5. Pipe the JSONL into a tiny TUI that highlights the latest non-zero exit. Eight key features the TUI must show to be useful in a review.
  中文翻译：思考并实践此练习。

## Key Terms | 术语速查表

| Term | What people say | What it actually means |
|------|----------------|------------------------|---|
| Feedback record | "Run log" | Structured JSONL entry with command, output, exit, duration |  |
| Tail truncation | "Trim the log" | Deterministic head+tail capture so records fit in token budget |  |
| Refuse-on-null | "Block on missing data" | The loop must not advance when `exit_code` is null |  |
| Agent note | "Expectation tag" | The one-line prediction the agent writes before reading the result |  |
| Telemetry split | "Two log files" | Feedback for the next turn, telemetry for the operator |  |

## Further Reading | 延伸阅读

- [OpenTelemetry GenAI semantic conventions](https://opentelemetry.io/docs/specs/semconv/gen-ai/)
  中文翻译：见原文。
- [Anthropic, Effective harnesses for long-running agents](https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents)
  中文翻译：见原文。
- [Guardrails AI x MLflow — deterministic safety, PII, quality validators](https://guardrailsai.com/blog/guardrails-mlflow) — redaction patterns as regression tests
  中文翻译：见原文。
- [Aport.io, Best AI Agent Guardrails 2026: Pre-Action Authorization Compared](https://aport.io/blog/best-ai-agent-guardrails-2026-pre-action-authorization-compared/) — pre/post-tool capture
  中文翻译：见原文。
- [Andrii Furmanets, AI Agents in 2026: Practical Architecture for Tools, Memory, Evals, Guardrails](https://andriifurmanets.com/blogs/ai-agents-2026-practical-architecture-tools-memory-evals-guardrails) — observability surfaces
  中文翻译：见原文。
- Phase 14 · 23 — OTel GenAI conventions for the telemetry side
- Phase 14 · 24 — agent observability platforms (Langfuse, Phoenix, Opik)
- Phase 14 · 33 — the rule that demands feedback before declaring done
- Phase 14 · 38 — the verification gate that reads the JSONL
