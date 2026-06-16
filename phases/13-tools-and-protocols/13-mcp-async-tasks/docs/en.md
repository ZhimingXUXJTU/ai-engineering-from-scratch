# Async Tasks (SEP-1686) — Call-Now, Fetch-Later for Long-Running Work | 异步任务：先调用后获取的长时运行工作

> Real agent work takes minutes to hours: CI runs, deep-research synthesis, batch exports. Synchronous tool calls drop connections, time out, or block the UI. SEP-1686, merged in 2025-11-25, adds a Tasks primitive: any request can be augmented to become a task, and the result can be fetched later or streamed via state notifications. Drift-risk note: Tasks are experimental through H1 2026; SDK surface is still being designed around the spec.

> **【中文解读】** 真正的 Agent 工作需要几分钟到几小时：CI 运行、深度研究综合、批量导出。同步工具调用会断开连接、超时或阻塞 UI。SEP-1686 添加了 Tasks 原语：任何请求都可以变成任务，结果可以稍后获取或通过状态通知流式传输。

> **【拓展：异步任务→MCP 长时运行工作】** 异步任务是 MCP 处理长时运行工作的标准模式。与传统同步 `tools/call` 不同，Tasks 允许服务器立即返回 `taskId`，客户端稍后通过 `tasks/status` 轮询进度或通过 `tasks/result` 获取最终结果。这是 MCP 从"简单工具执行"进化到"复杂工作流编排"的关键一步。

> 🔗 **【前置】** 学本节前请先掌握：(1) Phase 13·07（MCP server）和 13·09（transports）——理解同步 `tools/call` 和远程传输的连接管理；(2) 状态机概念（working/completed/failed 等状态转移）；(3) 后台任务 + 持久化基础（任务状态必须能扛重启）。

**Type:** Build | **类型:** 构建
**Languages:** Python (stdlib, async task state machine) | **语言:** Python (stdlib, async task state machine)
**Prerequisites:** Phase 13 · 07 (MCP server), Phase 13 · 09 (transports) | **前置知识:** Phase 13 · 07 (MCP server), Phase 13 · 09 (transports)
**Time:** ~75 minutes | **时间:** ~75 分钟

## Learning Objectives | 学习目标

- Identify when to promote a tool from synchronous to task-augmented (>30 seconds of server-side work).
  中文翻译：识别何时将工具从同步升级为任务增强（>30 秒的服务器端工作）。
- Walk the task lifecycle: `working` → `input_required` → `completed` / `failed` / `cancelled`.
  中文翻译：走通任务生命周期：`working` → `input_required` → `completed` / `failed` / `cancelled`。
- Persist task state so crashes do not lose in-flight work.
  中文翻译：持久化任务状态，使崩溃不丢失进行中的工作。
- Poll `tasks/status` and fetch `tasks/result` correctly.
  中文翻译：正确轮询 `tasks/status` 并获取 `tasks/result`。

## The Problem | 问题引入

> **【中文解读】** 异步任务解决长时间运行工具的问题。一个 `generate_report` 工具运行多分钟提取管道，同步模式下要么保持连接三分钟（传输会断、客户端超时），要么立即返回占位符让客户端轮询（破坏 MCP 统一性）。SEP-1686 添加了任务增强：请求可标记为任务，服务器立即返回 task id，客户端用 `tasks/status` 轮询。

A `generate_report` tool runs a multi-minute extraction pipeline. Options under the synchronous model:

> 一个 `generate_report` 工具运行多分钟的提取管道。同步模型下的选项：

1. Hold the connection open for three minutes. Remote transports drop it; clients time out; UIs freeze.
  中文翻译：保持连接开启三分钟。远程传输会断开；客户端超时；UI 冻结。
2. Return immediately with a placeholder; require the client to poll a custom endpoint. Breaks the MCP uniformity.
  中文翻译：立即返回占位符；要求客户端轮询自定义端点。破坏 MCP 统一性。
3. Fire-and-forget; no result.
  中文翻译：Fire-and-forget；无结果。

None are good. SEP-1686 adds a fourth: task augmentation. Any request (typically `tools/call`) can be tagged as a task. The server returns a task id immediately. The client polls `tasks/status` and fetches `tasks/result` when done. Server-side state survives restarts.

> 没一个是好的。SEP-1686 添加了第四个：任务增强。任何请求（通常是 `tools/call`）可标记为任务。服务器立即返回 task id。客户端轮询 `tasks/status` 并在完成时获取 `tasks/result`。服务器端状态在重启后存活。

> 💡 **【类比】** 异步任务像餐厅点餐的"取餐号"。同步模式：你点了一份煲仔饭（20 分钟），服务员说"请站在柜台等"——你站着不动 20 分钟（连接挂着）。任务模式：服务员给你一张"取餐号 42"的小票（task_id），说"20 分钟后来取"——你可以坐下玩手机（client 不阻塞），服务员做好了叫号（state=completed），你拿号去取餐（tasks/result）。状态在服务员的小本子上（持久化），即使换班也不丢。

## The Concept | 核心概念

### Task augmentation

A request becomes a task by setting `params._meta.task.required: true` (or `optional: true`, server decides). The server responds immediately with:

> 一个请求通过设置 `params._meta.task.required: true`（或 `optional: true`，服务器决定）成为任务。服务器立即响应：

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

> `ttl` 是服务器保留状态的承诺；超过 ttl 后任务结果被丢弃。

### Per-tool opt-in

Tool annotations can declare task support:

> 工具注解可声明任务支持：

- `taskSupport: "forbidden"` — this tool always runs synchronously. Safe for fast tools.
  中文翻译：`taskSupport: "forbidden"`——此工具始终同步运行。对快速工具安全。
- `taskSupport: "optional"` — client may request task-augmentation.
  中文翻译：`taskSupport: "optional"`——客户端可请求任务增强。
- `taskSupport: "required"` — client MUST use task augmentation.
  中文翻译：`taskSupport: "required"`——客户端必须使用任务增强。

A `generate_report` tool would be `required`. A `notes_search` tool would be `forbidden`.

> `generate_report` 工具应该是 `required`。`notes_search` 工具应该是 `forbidden`。

### States

```
working  -> input_required -> working  (loop via elicitation)
working  -> completed
working  -> failed
working  -> cancelled
```

State machine is append-only: once `completed`, `failed`, or `cancelled`, the task is terminal.

> 状态机是 append-only：一旦 `completed`、`failed` 或 `cancelled`，任务即终止。

> ⚠️ **【易错点】** 场景：任务状态只存在内存里 / 后果：服务器进程重启（部署、OOM、崩溃）后所有 in-flight 任务全部丢失，客户端轮询永远拿不到结果，用户体验是"卡死了" / 修复：(1) 状态必须持久化（Redis/SQLite/文件），每次状态转移立即写盘；(2) 进程启动时扫描未完成任务，根据策略恢复（继续/标记 failed/通知用户）；(3) `ttl` 字段不能太短，至少覆盖预期最长任务 + 重启窗口。

> 🤔 **【困惑】** Q: 轮询（polling）会不会浪费资源？为什么不用纯推送（push）？ A: 推送需要长连接（SSE/websocket），而 Streamable HTTP 客户端不一定持续监听。MCP 选择"轮询 + 可选推送"组合：(1) 客户端默认每 5-10 秒 poll 一次；(2) 若客户端打开了 GET /mcp SSE 通道，server 主动推 `notifications/tasks/progress` 减少轮询频率；(3) 进入 `completed` 后客户端停止轮询。这样既兼容简单客户端（纯轮询），又给高级客户端优化空间。

### Methods

- `tasks/status {taskId}` — returns current state and a progress hint.
  中文翻译：`tasks/status {taskId}`——返回当前状态和进度提示。
- `tasks/result {taskId}` — blocks or returns 404 if not yet done.
  中文翻译：`tasks/result {taskId}`——阻塞或如未完成返回 404。
- `tasks/cancel {taskId}` — idempotent; terminal states ignore.
  中文翻译：`tasks/cancel {taskId}`——幂等；终止状态被忽略。
- `tasks/list` — optional; enumerates active and recently-completed tasks.
  中文翻译：`tasks/list`——可选；枚举活动任务和最近完成任务。

### Streaming state changes

When the server supports it, the client can subscribe to state notifications:

> 当服务器支持时，客户端可订阅状态通知：

```
server -> notifications/tasks/updated {taskId, state, progress?}
```

Clients that stream rather than poll get better UX. Polling is always supported as the minimal surface.

> 流式而非轮询的客户端获得更好的 UX。轮询始终作为最小表面支持。

### Durable state

> **【拓展：异步任务的持久化存储】** 规范要求声明任务支持的服务器必须持久化状态。崩溃不应丢失 TTL 内的已完成结果。存储方式包括 SQLite、Redis 和文件系统。这对长时间运行的代码生成、数据分析和报告生成工具至关重要——即使服务器崩溃也不需要从头开始。

The spec requires servers that declare task support to persist state. A crash should not lose completed results within ttl. Stores range from SQLite to Redis to the filesystem. The Lesson 13 harness uses the filesystem.

> 规范要求声明任务支持的服务器持久化状态。崩溃不应丢失 ttl 内已完成的结果。存储从 SQLite 到 Redis 到文件系统。Lesson 13 的线束使用文件系统。

### Cancellation semantics

`tasks/cancel` is idempotent. If the task is mid-execution, the server attempts to stop (check executor-cooperative cancellation). If already terminal, the request is a no-op.

> `tasks/cancel` 是幂等的。如果任务正在执行，服务器尝试停止（检查执行器协作取消）。如果已终止，请求是 no-op。

### Crash recovery

When the server process restarts:

> 当服务器进程重启时：

1. Load all persisted task states.
  中文翻译：加载所有持久化的任务状态。
2. Mark any `working` tasks whose process died as `failed` with error `CRASH_RECOVERY`.
  中文翻译：将进程已死亡的 `working` 任务标记为 `failed`，错误为 `CRASH_RECOVERY`。
3. Preserve `completed` / `failed` / `cancelled` for their ttl.
  中文翻译：保留 `completed` / `failed` / `cancelled` 直到其 ttl。

### Async tasks plus sampling

A task can itself call `sampling/createMessage`. This is how long-running research tasks work: the server's task thread samples the client's model as needed, while the client's UI shows the task as `working` with periodic progress updates.

> 任务自身可调用 `sampling/createMessage`。这就是长运行研究任务的工作方式：服务器的任务线程按需采样客户端的模型，同时客户端 UI 显示任务为 `working` 并定期更新进度。

### Why this is experimental

SEP-1686 shipped in 2025-11-25 but the broader roadmap calls out three open issues: durable subscription primitives, subtasks (parent-child task relationships), and result-TTL standardization. Expect the spec to evolve through 2026. Production code should treat Tasks as stable only for the common case and guard against future SDK changes for subtasks.

> SEP-1686 在 2025-11-25 发布，但更广泛的路线图列出三个开放问题：持久订阅原语、子任务（父子任务关系）和 result-TTL 标准化。预计规范会在 2026 年演进。生产代码应仅在常见情况下将 Tasks 视为稳定，并对子任务的未来 SDK 变更加守卫。

## Use It | 用框架实现

`code/main.py` implements a durable task store (filesystem-backed) and a `generate_report` tool that runs in a background thread. Clients call the tool, get a task id immediately, poll `tasks/status` while the worker updates progress, and fetch `tasks/result` when done. Cancellation works; crash recovery is simulated by killing the worker thread and reloading state.

> `code/main.py` 实现持久任务存储（文件系统支持）和一个在后台线程运行的 `generate_report` 工具。客户端调用工具，立即获得 task id，工作器更新进度时轮询 `tasks/status`，完成时获取 `tasks/result`。取消工作；崩溃恢复通过杀死工作线程并重载状态模拟。

What to look at:

- Task state JSON persisted to `/tmp/lesson-13-tasks/<id>.json`.
  中文翻译：任务状态 JSON 持久化到 `/tmp/lesson-13-tasks/<id>.json`。
- Worker thread updates `progress` field; poll shows it advancing.
  中文翻译：工作线程更新 `progress` 字段；轮询显示其推进。
- Cancellation from client side sets an event; worker checks and exits early.
  中文翻译：客户端取消设置事件；工作器检查并提前退出。
- State reload on "crash" marks the in-flight task as `failed` with `CRASH_RECOVERY`.
  中文翻译："崩溃"时状态重载将进行中任务标记为 `failed` 带 `CRASH_RECOVERY`。

## Ship It | 产出物

This lesson produces `outputs/skill-task-store-designer.md`. Given a long-running tool (research, build, export), the skill designs the task store (state shape, ttl, durability), picks the right taskSupport flag, and sketches progress notifications.

> 本课产出 `outputs/skill-task-store-designer.md`。给定一个长运行工具（研究、构建、导出），该 skill 设计任务存储（状态形态、ttl、持久性），选择正确的 taskSupport 标志，并勾勒进度通知。

## Exercises | 练习题

1. Run `code/main.py`. Kick off a `generate_report` task, poll status, then fetch the result.
   中文翻译：运行 `code/main.py`。启动 `generate_report` 任务，轮询状态，然后获取结果。

2. Add a `tasks/cancel` call mid-run. Verify the worker honors it and the state becomes `cancelled`.
   中文翻译：运行中添加 `tasks/cancel` 调用。验证工作器遵守它，状态变为 `cancelled`。

3. Simulate crash recovery: kill the worker thread, restart the loader, and observe the `CRASH_RECOVERY` failure mode.
   中文翻译：模拟崩溃恢复：杀死工作线程，重启加载器，观察 `CRASH_RECOVERY` 失败模式。

4. Extend the store to SQLite. Durability wins are the same; query options open up (list all tasks from session X).
   中文翻译：将存储扩展到 SQLite。持久性收益相同；查询选项开放（列出 session X 的所有任务）。

5. Read the MCP roadmap post for 2026. Identify the one Tasks-related open issue most likely to affect SDK API design in the next year.
   中文翻译：阅读 MCP 2026 路线图帖子。识别最可能影响下年 SDK API 设计的 Tasks 相关开放问题。

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
  中文翻译：原始提案和完整讨论
- [WorkOS — MCP async tasks for AI agent workflows](https://workos.com/blog/mcp-async-tasks-ai-agent-workflows) — design walkthrough with rationale
  中文翻译：带理由的设计演练
- [DeepWiki — MCP task system and async operations](https://deepwiki.com/modelcontextprotocol/modelcontextprotocol/2.7-task-system-and-async-operations) — mechanics and state machine
  中文翻译：机制和状态机
- [FastMCP — Tasks](https://gofastmcp.com/servers/tasks) — SDK-level task implementation patterns
  中文翻译：SDK 级任务实现模式
- [MCP blog — 2026 roadmap](https://blog.modelcontextprotocol.io/posts/2026-mcp-roadmap/) — open issues and 2026 priorities including subtasks
  中文翻译：开放问题和 2026 优先级，包括子任务
