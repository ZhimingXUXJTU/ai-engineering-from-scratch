# Async Tasks (SEP-1686) — Call-Now, Fetch-Later for Long-Running Work | 异步任务：先调用后获取的长时运行工作

> Real agent work takes minutes to hours: CI runs, deep-research synthesis, batch exports. Synchronous tool calls drop connections, time out, or block the UI. SEP-1686, merged in 2025-11-25, adds a Tasks primitive: any request can be augmented to become a task, and the result can be fetched later or streamed via state notifications. Drift-risk note: Tasks are experimental through H1 2026; SDK surface is still being designed around the spec.

> **【中文解读】** 真正的 Agent 工作需要几分钟到几小时：CI 运行、深度研究综合、批量导出。同步工具调用会断开连接、超时或阻塞 UI。SEP-1686 添加了 Tasks 原语：任何请求都可以变成任务，结果可以稍后获取或通过状态通知流式传输。

> **【拓展：异步任务→MCP 长时运行工作】** 异步任务是 MCP 处理长时运行工作的标准模式。与传统同步 `tools/call` 不同，Tasks 允许服务器立即返回 `taskId`，客户端稍后通过 `tasks/status` 轮询进度或通过 `tasks/result` 获取最终结果。这是 MCP 从"简单工具执行"进化到"复杂工作流编排"的关键一步。

**Type:** Build
**Languages:** Python (stdlib, async task state machine)
**Prerequisites:** Phase 13 · 07 (MCP server), Phase 13 · 09 (transports)
**Time:** ~75 minutes

## Learning Objectives

- Identify when to promote a tool from synchronous to task-augmented (>30 seconds of server-side work).
- Walk the task lifecycle: `working` → `input_required` → `completed` / `failed` / `cancelled`.
- Persist task state so crashes do not lose in-flight work.
- Poll `tasks/status` and fetch `tasks/result` correctly.

## The Problem | 问题引入

> **【中文解读】** 异步任务解决长时间运行工具的问题。一个 `generate_report` 工具运行多分钟提取管道，同步模式下要么保持连接三分钟（传输会断、客户端超时），要么立即返回占位符让客户端轮询（破坏 MCP 统一性）。SEP-1686 添加了任务增强：请求可标记为任务，服务器立即返回 task id，客户端用 `tasks/status` 轮询。

A `generate_report` tool runs a multi-minute extraction pipeline. Options under the synchronous model:

1. Hold the connection open for three minutes. Remote transports drop it; clients time out; UIs freeze.
2. Return immediately with a placeholder; require the client to poll a custom endpoint. Breaks the MCP uniformity.
3. Fire-and-forget; no result.

None are good. SEP-1686 adds a fourth: task augmentation. Any request (typically `tools/call`) can be tagged as a task. The server returns a task id immediately. The client polls `tasks/status` and fetches `tasks/result` when done. Server-side state survives restarts.

## The Concept | 核心概念

### Task augmentation

A request becomes a task by setting `params._meta.task.required: true` (or `optional: true`, server decides). The server responds immediately with:

```json
{
  "jsonrpc": "2.0", "id": 1,
  "result": {
    "_meta": {
      "task": {
        "id": "tsk_9f7b...",
        "state": "working",
        "ttl": 900000
      }
    }
  }
}
```

`ttl` is the server's promise to retain state; after ttl the task result is discarded.

### Per-tool opt-in

Tool annotations can declare task support:

- `taskSupport: "forbidden"` — this tool always runs synchronously. Safe for fast tools.
- `taskSupport: "optional"` — client may request task-augmentation.
- `taskSupport: "required"` — client MUST use task augmentation.

A `generate_report` tool would be `required`. A `notes_search` tool would be `forbidden`.

### States

```
working  -> input_required -> working  (loop via elicitation)
working  -> completed
working  -> failed
working  -> cancelled
```

State machine is append-only: once `completed`, `failed`, or `cancelled`, the task is terminal.

### Methods

- `tasks/status {taskId}` — returns current state and a progress hint.
- `tasks/result {taskId}` — blocks or returns 404 if not yet done.
- `tasks/cancel {taskId}` — idempotent; terminal states ignore.
- `tasks/list` — optional; enumerates active and recently-completed tasks.

### Streaming state changes

When the server supports it, the client can subscribe to state notifications:

```
server -> notifications/tasks/updated {taskId, state, progress?}
```

Clients that stream rather than poll get better UX. Polling is always supported as the minimal surface.

### Durable state

> **【拓展：异步任务的持久化存储】** 规范要求声明任务支持的服务器必须持久化状态。崩溃不应丢失 TTL 内的已完成结果。存储方式包括 SQLite、Redis 和文件系统。这对长时间运行的代码生成、数据分析和报告生成工具至关重要——即使服务器崩溃也不需要从头开始。

The spec requires servers that declare task support to persist state. A crash should not lose completed results within ttl. Stores range from SQLite to Redis to the filesystem. The Lesson 13 harness uses the filesystem.

### Cancellation semantics

`tasks/cancel` is idempotent. If the task is mid-execution, the server attempts to stop (check executor-cooperative cancellation). If already terminal, the request is a no-op.

### Crash recovery

When the server process restarts:

1. Load all persisted task states.
2. Mark any `working` tasks whose process died as `failed` with error `CRASH_RECOVERY`.
3. Preserve `completed` / `failed` / `cancelled` for their ttl.

### Async tasks plus sampling

A task can itself call `sampling/createMessage`. This is how long-running research tasks work: the server's task thread samples the client's model as needed, while the client's UI shows the task as `working` with periodic progress updates.

### Why this is experimental

SEP-1686 shipped in 2025-11-25 but the broader roadmap calls out three open issues: durable subscription primitives, subtasks (parent-child task relationships), and result-TTL standardization. Expect the spec to evolve through 2026. Production code should treat Tasks as stable only for the common case and guard against future SDK changes for subtasks.

## Use It | 用框架实现

`code/main.py` implements a durable task store (filesystem-backed) and a `generate_report` tool that runs in a background thread. Clients call the tool, get a task id immediately, poll `tasks/status` while the worker updates progress, and fetch `tasks/result` when done. Cancellation works; crash recovery is simulated by killing the worker thread and reloading state.

What to look at:

- Task state JSON persisted to `/tmp/lesson-13-tasks/<id>.json`.
- Worker thread updates `progress` field; poll shows it advancing.
- Cancellation from client side sets an event; worker checks and exits early.
- State reload on "crash" marks the in-flight task as `failed` with `CRASH_RECOVERY`.

## Ship It | 产出物

This lesson produces `outputs/skill-task-store-designer.md`. Given a long-running tool (research, build, export), the skill designs the task store (state shape, ttl, durability), picks the right taskSupport flag, and sketches progress notifications.

## Exercises | 练习题

1. Run `code/main.py`. Kick off a `generate_report` task, poll status, then fetch the result.

2. Add a `tasks/cancel` call mid-run. Verify the worker honors it and the state becomes `cancelled`.

3. Simulate crash recovery: kill the worker thread, restart the loader, and observe the `CRASH_RECOVERY` failure mode.

4. Extend the store to SQLite. Durability wins are the same; query options open up (list all tasks from session X).

5. Read the MCP roadmap post for 2026. Identify the one Tasks-related open issue most likely to affect SDK API design in the next year.

## Key Terms | 术语速查表

| Term | What people say | What it actually means | 中文术语 |
|------|----------------|------------------------|----------|
| Task | "Long-running tool call" | Request augmented with `_meta.task` for async execution | 异步任务 |
| SEP-1686 | "Tasks spec" | Spec Evolution Proposal that added Tasks in 2025-11-25 | 任务规范提案 |
| `_meta.task` | "Task envelope" | Per-request metadata containing id, state, ttl | 任务元数据 |
| taskSupport | "Tool flag" | `forbidden` / `optional` / `required` per tool | 任务支持标志 |
| `tasks/status` | "Poll method" | Fetch current state and optional progress hint | 任务状态轮询 |
| `tasks/result` | "Fetch result" | Returns the completed payload or 404 if not yet done | 获取任务结果 |
| `tasks/cancel` | "Stop it" | Idempotent cancellation request | 取消任务 |
| ttl | "Retention budget" | Milliseconds the server promises to keep the task state | 任务保留时间 |
| `notifications/tasks/updated` | "State push" | Server-initiated state-change event | 任务状态通知 |
| Durable store | "Crash-safe state" | Filesystem / SQLite / Redis persistence layer | 持久化存储 |

## Further Reading | 延伸阅读

- [MCP — GitHub SEP-1686 issue](https://github.com/modelcontextprotocol/modelcontextprotocol/issues/1686) — the originating proposal and full discussion
- [WorkOS — MCP async tasks for AI agent workflows](https://workos.com/blog/mcp-async-tasks-ai-agent-workflows) — design walkthrough with rationale
- [DeepWiki — MCP task system and async operations](https://deepwiki.com/modelcontextprotocol/modelcontextprotocol/2.7-task-system-and-async-operations) — mechanics and state machine
- [FastMCP — Tasks](https://gofastmcp.com/servers/tasks) — SDK-level task implementation patterns
- [MCP blog — 2026 roadmap](https://blog.modelcontextprotocol.io/posts/2026-mcp-roadmap/) — open issues and 2026 priorities including subtasks
