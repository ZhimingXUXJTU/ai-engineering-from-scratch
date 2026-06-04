# 会话 Agent Claude SDK

> The Claude Agent SDK is the library form of the Claude Code harness. Built-in tools, subagents for context isolation, hooks, W3C trace propagation, session store parity. Claude Managed Agents is the hosted alternative for long-running async work.


**类型：** 学习 + 构建
**语言：** Python (stdlib)
**前置条件：** Phase 14 · 01 (Agent Loop), Phase 14 · 10 (Skill Libraries)
**预计时间：** ~75 minutes

## 学习目标

- Explain the difference between the Anthropic Client SDK (raw API) and the Claude Agent SDK (harness shape).
- Describe subagents — parallelization and context isolation — and when to reach for them.
- Name the Python SDK's session store surface (`append`, `load`, `list_sessions`, `delete`, `list_subkeys`) and the role of `--session-mirror`.
- Implement a stdlib harness with built-in tools, subagent spawning with isolated context, lifecycle hooks, and a session store.

## 问题引入

> **【中文解读】** Claude Agent SDK 是 Anthropic 官方的 Agent 开发框架。核心特性：(1) 内置工具（文件读写、代码执行等）；(2) 子 Agent 支持——Agent 可以生成子 Agent 处理子任务；(3) 生命周期钩子——在 Agent 执行的关键节点插入自定义逻辑。SDK 深度集成 Claude 的 Extended Thinking 能力。
> **【拓展：Claude Agent SDK 是 2026 年 Claude 生态的核心开发工具。与 OpenA...】** Claude Agent SDK 是 2026 年 Claude 生态的核心开发工具。与 OpenAI Agents SDK 相比，它更注重深度集成 Claude 的独特能力（如 Extended Thinking、Computer Use）。SDK 的子 Agent 模式允许 Agent 将复杂任务分解为子任务，每个子任务由专门的子 Agent 处理，类似于组织中的部门分工。

## 核心概念

### Client SDK vs Agent SDK
- **Client SDK (`anthropic`).** Raw Messages API. You own the loop, the tools, the state.
- **Agent SDK (`claude-agent-sdk`).** Built-in tool execution, MCP connections, hooks, subagent spawning, session store. The Claude Code loop as a library.
### Built-in tools
The SDK ships 10+ tools out of the box: file read/write, shell, grep, glob, web fetch, more. Custom tools register via the standard tool-schema interface.
### Subagents
Two purposes documented by Anthropic:
1. **Parallelization.** Run independent work concurrently. "Find the test file for each of these 20 modules" is 20 parallel subagent tasks.
2. **Context isolation.** Subagents use their own context window; only results return to the orchestrator. The orchestrator's budget is preserved.
Python SDK recent additions: `list_subagents()`, `get_subagent_messages()` for reading subagent transcripts.
### Session store
Protocol parity with TypeScript:
- `append(session_id, message)` — add a turn.
- `load(session_id)` — restore conversation.
- `list_sessions()` — enumerate.
- `delete(session_id)` — with cascade to subagent sessions.
- `list_subkeys(session_id)` — list subagent keys.
`--session-mirror` (CLI flag) mirrors the transcript to an external file as it streams, for debugging.
### Hooks
Lifecycle hooks you can register:
- `PreToolUse`, `PostToolUse` — gate or audit tool calls.
- `SessionStart`, `SessionEnd` — set up and tear down.
- `UserPromptSubmit` — act on user input before the model sees it.
- `PreCompact` — run before context compaction.
- `Stop` — cleanup on agent exit.
- `Notification` — side-channel alerts.
Hooks are how pro-workflow (Phase 14 curriculum reference) and similar systems add cross-cutting behavior.
### W3C trace context
OTel spans active on the caller propagate into the CLI subprocess via W3C trace context headers. The whole multi-process trace shows up as one trace in your backend.
### Claude Managed Agents
The hosted alternative (beta header `managed-agents-2026-04-01`). Long-running async work, built-in prompt caching, built-in compaction. Trade control for managed infrastructure.
### Where this pattern goes wrong
- **Subagent over-spawn.** Spawning 100 subagents for 100 tiny tasks. Overhead dominates. Batch instead.
- **Hook creep.** Every team adds hooks; startup time balloons. Review hooks quarterly.
- **Session bloat.** Sessions accumulate; size grows. Use `list_sessions` + expiry policy.

## 动手实现

`code/main.py` implements the SDK shape in stdlib:
- `Tool`, `ToolRegistry` with built-in `read_file`, `write_file`, `list_dir`.
- `Subagent` — private context, isolated run, results returned.
- `SessionStore` — append, load, list, delete, list_subkeys.
- `Hooks` — `pre_tool_use`, `post_tool_use`, `session_start`, `session_end`.
- A demo: main agent spawns 3 subagents in parallel (each isolated), aggregates results, persists session.
Run it:
```
python3 code/main.py
```
The trace shows subagent context isolation (orchestrator context size stays bounded), hook execution, and session persistence.

## 用框架实现

- **Claude Agent SDK** for Claude-first products that want the Claude Code harness shape.
- **Claude Managed Agents** for hosted long-running async work.
- **OpenAI Agents SDK** (Lesson 16) for OpenAI-first counterparts.
- **LangGraph + custom tools** if you want the graph-shaped state machine instead.

## 产出物

`outputs/skill-claude-agent-scaffold.md` scaffolds a Claude Agent SDK app with subagents, hooks, session store, MCP server attachment, and W3C trace propagation.

## 练习题

1. Add a subagent spawner that batches 20 tasks into groups of 5 parallel subagents. Measure orchestrator context size vs one-per-task.
   *思考并实践此练习*
2. Implement a `PreToolUse` hook that rate-limits `write_file` calls (5 per minute per session). Trace the behavior.
   *思考并实践此练习*
3. Wire `list_subkeys` to render a subagent tree. What does deep nesting look like?
   *思考并实践此练习*
4. Port the toy to the real `claude-agent-sdk` Python package. What changes about tool registration?
   *思考并实践此练习*
5. Read the Claude Managed Agents docs. When would you switch from self-hosted to managed?
   *思考并实践此练习*

## 术语速查表

| 术语 | 实际含义 |
|------|---------|
| Agent SDK | "Claude Code as a library" |
| Subagent | "Child agent" |
| Session store | "Conversation DB" |
| Hook | "Lifecycle callback" |
| W3C trace context | "Cross-process trace" |
| Managed Agents | "Hosted harness" |
| `--session-mirror` | "Transcript mirror" |
| MCP server | "Tool surface" |

## 延伸阅读

