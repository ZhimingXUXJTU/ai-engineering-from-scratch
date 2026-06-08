# Scope Contracts and Task Boundaries | 契约 范围

> The model does not know where the work ends. A scope contract is a per-task file that says where the work begins, where it ends, and how to roll back if it spills. The contract turns "stay in scope" from a wish into a check.

**Type:** Build | **类型:** 构建
**Languages:** Python (stdlib) | **语言:** Python (标准库)
**Prerequisites:** Phase 14 · 32 (Minimal Workbench), Phase 14 · 33 (Rules as Constraints) | **前置知识:** 见原文
**Time:** ~50 minutes | **时间:** 见原文

## Learning Objectives | 学习目标

- Write a scope contract that an agent reads at task start and a verifier reads at task end.
- Specify allowed files, forbidden files, acceptance criteria, rollback plan, and approval boundaries.
- Implement a scope checker that compares a diff against the contract and flags violations.
- Make scope creep visible, automatic, and reviewable.

## The Problem | 问题引入

Agents creep. The task is "fix the login bug." The diff touches the login route, the email helper, the database driver, the README, and the release script. Each touch had a plausible reason in the moment. Together they are a different change than the one that was reviewed.

> Agent 会蔓延。任务是"修复登录 bug"。diff 触及登录路由、邮件辅助函数、数据库驱动、README 和发布脚本。每次触及在当下都有合理的理由。但加在一起，它们与审查的更改不同。

Scope creep is the most under-monitored failure mode in agent work because the agent narrates each step in good faith. The fix is not a stricter prompt. The fix is a contract on disk that says what was promised and a check that compares the result against the promise.

> 范围蔓延是 Agent 工作中最缺乏监控的失败模式，因为 Agent 诚实地叙述每一步。修复不是更严格的提示。修复是磁盘上的契约，说明承诺了什么，以及将结果与承诺进行比较的检查。


> **【中文解读】** 范围契约定义 Agent 可以做什么和不能做什么。显式的范围契约包括：(1) 文件范围——Agent 可以修改哪些文件和目录；(2) 操作范围——可以执行哪些命令；(3) 依赖范围——可以安装哪些包。范围越明确，Agent 的可预测性越高。

## The Concept | 核心概念

```mermaid
flowchart LR
  Task[Task] --> Contract[scope_contract.json]
  Contract --> Agent[Agent Loop]
  Agent --> Diff[final diff]
  Diff --> Checker[scope_checker.py]
  Contract --> Checker
  Checker --> Verdict{in scope?}
  Verdict -- yes --> Verify[Verification Gate]
  Verdict -- no --> Block[block + open question]
```


> **【中文解读】** 范围契约定义 Agent 可以做什么和不能做什么。显式的范围契约包括：(1) 文件范围——Agent 可以修改哪些文件和目录；(2) 操作范围——可以执行哪些命令；(3) 依赖范围——可以安装哪些包。范围越明确，Agent 的可预测性越高。

### What goes in a scope contract

| Field | Purpose |
|-------|---------|
| `task_id` | Links to the task on the board |
| `goal` | One sentence the reviewer can verify |
| `allowed_files` | Globs the agent may write |
| `forbidden_files` | Globs the agent must not touch even by accident |
| `acceptance_criteria` | Test commands or assertion lines that prove done |
| `rollback_plan` | One paragraph the operator can execute if a halt is required |
| `approvals_required` | Actions outside scope that need explicit human sign-off |

A contract without `forbidden_files` is incomplete. The negative space is half the contract.

> 范围契约（Scope Contracts）定义 Agent 的操作边界。通过明确指定 Agent 可以和不可以做什么，防止越界操作。

### Globs, not raw paths

Real repos move files. Pin contracts to globs (`app/**/*.py`, `tests/test_signup*.py`) so a refactor between sessions does not invalidate the contract.

> 范围契约（Scope Contracts）定义 Agent 的操作边界。通过明确指定 Agent 可以和不可以做什么，防止越界操作。

### Rollback is part of scope

Listing how to roll back forces the contract author to think about what could go wrong. A contract you cannot roll back from is a contract that should not be approved.

> 范围契约（Scope Contracts）定义 Agent 的操作边界。通过明确指定 Agent 可以和不可以做什么，防止越界操作。

### Scope check is a diff check

The agent writes a diff. The checker reads the diff, the allowed globs, the forbidden globs, and a list of any acceptance commands that ran. Each violation is a tagged finding the verification gate can refuse.

> 范围契约（Scope Contracts）定义 Agent 的操作边界。通过明确指定 Agent 可以和不可以做什么，防止越界操作。

## Build It | 动手实现

`code/main.py` implements:

- `scope_contract.json` schema (subset of JSON Schema, glob arrays).
- A diff parser that turns a list of touched files plus a list of run commands into a `RunSummary`.
- A `scope_check` that returns `(violations, in_scope, off_scope)` against the contract.
- Two demo runs: one that stays in scope, one that creeps. The checker flags the creep with the exact file and reason.

Run it:

```
python3 code/main.py
```

Output: the contract, the two runs, the per-run verdicts, and a saved `scope_report.json`.

> 范围契约（Scope Contracts）定义 Agent 的操作边界。通过明确指定 Agent 可以和不可以做什么，防止越界操作。

## Production patterns in the wild

A practitioner running "specsmaxxing" (scope contracts in YAML before invoking the agent) reports rabbit-hole rate dropped from 52% to 21% in three weeks without changing the agent. The contract did the work, not the model. Three patterns make the gain stick.

> 范围契约（Scope Contracts）定义 Agent 的操作边界。通过明确指定 Agent 可以和不可以做什么，防止越界操作。

**Violation budgets, not binary failures.** `agent-guardrails` (the OSS merge gate used by Claude Code, Cursor, Windsurf, Codex via MCP) ships a `violationBudget` per task: minor scope slips within budget are surfaced as warnings; only when the budget is exceeded does the merge gate refuse. Pair with `violationSeverity: "error" | "warning"`. The budget is the difference between a gate that ships and a gate that gets disabled by the team that hated it.

**Severity asymmetry by path family.** Off-scope writes to `docs/**` are usually `warn`; off-scope writes to `scripts/**`, `migrations/**`, `config/prod/**` are always `block`. This asymmetry has to live in the contract, not in the runtime, because it is project-specific and changes per task.

**Time and network budgets next to file budgets.** A `time_budget_minutes` field bounds the wall clock; the runtime refuses to continue past it without re-approval. A `network_egress` allowlist on hostnames prevents the agent from quietly hitting an external API that was not part of the task. These are scope dimensions too; the file globs are necessary, not sufficient.

**Multi-contract merge semantics (least privilege).** When two scope contracts apply (e.g., a project-wide contract plus a task-specific one), the merge is: **intersect** `allowed_files` (both contracts must permit the path), **union** `forbidden_files` (either can prohibit), `time_budget_minutes` is the most restrictive (min), `approvals_required` accumulates. `network_egress` is `None` for no enforcement, `[]` for deny-all, `[...]` as an allowlist; under merge, `None` defers to the other side, two lists intersect, and deny-all stays deny-all. State this in the contract schema so the merge is mechanical and reviewable.

## Use It | 用框架实现

Production patterns:

- **Claude Code slash commands.** A `/scope` command writes the contract and pins it as session context. Subagents read the contract before acting.
- **GitHub PRs.** Push the contract as a JSON file in the PR body or as a checked-in artifact. CI runs the scope checker against the merge diff.
- **LangGraph interrupts.** A scope violation triggers an interrupt; the handler asks the human whether the contract needs to grow or the agent needs to back off.

The contract travels with the task. When the task closes, the contract is archived under `outputs/scope/closed/`.

> 范围契约（Scope Contracts）定义 Agent 的操作边界。通过明确指定 Agent 可以和不可以做什么，防止越界操作。

## Ship It | 产出物

`outputs/skill-scope-contract.md` generates a scope contract for a task description and a glob-aware checker that runs in CI on every agent diff.

> 范围契约（Scope Contracts）定义 Agent 的操作边界。通过明确指定 Agent 可以和不可以做什么，防止越界操作。

## Exercises | 练习题

1. Add a `network_egress` field listing allowed external hosts. Refuse runs that touch other hosts.
  中文翻译：思考并实践此练习。
2. Extend the checker to fail soft on `docs/**` and hard on `scripts/**`. Justify the asymmetry.
3. Make the contract derive `allowed_files` from a `goal` field using a static rule set (no LLM). What goes wrong on the first edge case?
  中文翻译：思考并实践此练习。
4. Add a `time_budget_minutes` and refuse to continue once the wall clock exceeds it.
  中文翻译：思考并实践此练习。
5. Run two contracts against the same diff. What is the right merge semantics when both apply?
  中文翻译：思考并实践此练习。

## Key Terms | 术语速查表

| Term | What people say | What it actually means |
|------|----------------|------------------------|---|
| Scope contract | "The task brief" | Per-task JSON listing allowed/forbidden files, acceptance, rollback |  |
| Scope creep | "It also touched..." | Files outside the contract changed in the same task |  |
| Rollback plan | "We can revert" | The one-paragraph operator runbook for halting |  |
| Approval boundary | "Needs sign-off" | An action listed in the contract as requiring explicit human approval |  |
| Diff check | "Path audit" | Comparing touched files against the contract globs |  |

## Further Reading | 延伸阅读

- [LangGraph human-in-the-loop interrupts](https://langchain-ai.github.io/langgraph/concepts/human_in_the_loop/)
  中文翻译：见原文。
- [OpenAI Agents SDK tool approval policies](https://platform.openai.com/docs/guides/agents-sdk)
  中文翻译：见原文。
- [logi-cmd/agent-guardrails — merge gates and scope validation](https://github.com/logi-cmd/agent-guardrails) — violation budgets, severity tiers
  中文翻译：见原文。
- [Dev|Journal, Preventing AI Agent Configuration Drift with Agent Contract Testing](https://earezki.com/ai-news/2026-05-05-i-built-a-tiny-ci-tool-to-keep-ai-agent-configs-from-drifting-in-my-repo/) — `--strict` mode without external deps
  中文翻译：见原文。
- [Agentic Coding Is Not a Trap (production logs)](https://dev.to/jtorchia/agentic-coding-is-not-a-trap-i-answered-the-viral-hn-post-with-my-own-production-logs-33d9) — specsmaxxing receipts: 52% → 21%
  中文翻译：见原文。
- [OpenCode permission globs](https://opencode.ai/docs/agents/) — fine-grained per-permission scope
  中文翻译：见原文。
- [Knostic, AI Coding Agent Security: Threat Models and Protection Strategies](https://www.knostic.ai/blog/ai-coding-agent-security) — scope as part of least privilege
  中文翻译：见原文。
- [Augment Code, AI Spec Template](https://www.augmentcode.com/guides/ai-spec-template) — three-tier boundary system (must/ask/never)
  中文翻译：见原文。
- Phase 14 · 27 — prompt injection defenses that pair with scope locks
- Phase 14 · 33 — the rule set this contract specializes per task
- Phase 14 · 38 — the verification gate the checker reports into
