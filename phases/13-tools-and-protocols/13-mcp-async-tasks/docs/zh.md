# 异步任务（SEP-1686）— 先调用后获取的长时运行工作

> 真正的 Agent 工作需要几分钟到几小时：CI 运行、深度研究综合、批量导出。同步工具调用会断开连接、超时或阻塞 UI。SEP-1686 添加了 Tasks 原语：任何请求都可以变成任务，结果可以稍后获取或通过状态通知流式传输。漂移风险提示：Tasks 在 2026 年上半年之前是实验性的；SDK 表面仍在围绕规范设计中。

> **【中文解读】** 真正的 Agent 工作需要几分钟到几小时：CI 运行、深度研究综合、批量导出。同步工具调用会断开连接、超时或阻塞 UI。SEP-1686 添加了 Tasks 原语：任何请求都可以变成任务，结果可以稍后获取或通过状态通知流式传输。

> **【拓展：异步任务→MCP 长时运行工作】** 异步任务是 MCP 处理长时运行工作的标准模式。与传统同步 `tools/call` 不同，Tasks 允许服务器立即返回 `taskId`，客户端稍后通过 `tasks/status` 轮询进度或通过 `tasks/result` 获取最终结果。这是 MCP 从"简单工具执行"进化到"复杂工作流编排"的关键一步。

**类型：** 构建
**语言：** Python（标准库，异步任务状态机）
**前置条件：** Phase 13 · 07（MCP 服务器），Phase 13 · 09（传输层）
**时间：** 约 75 分钟

## 学习目标

- 识别何时将工具从同步提升为任务增强（超过 30 秒的服务器端工作）。
- 走通任务生命周期：`working` → `input_required` → `completed` / `failed` / `cancelled`。
- 持久化任务状态使崩溃不会丢失进行中的工作。
- 正确轮询 `tasks/status` 并获取 `tasks/result`。

## 问题引入

一个 `generate_report` 工具运行多分钟的提取管道。同步模式下的选项：

1. 保持连接三分钟。远程传输会断开；客户端超时；UI 冻结。
2. 立即返回占位符；要求客户端轮询自定义端点。破坏 MCP 统一性。
3. 即发即忘；无结果。

都不好。SEP-1686 添加了第四种：任务增强。任何请求（通常是 `tools/call`）可以标记为任务。服务器立即返回任务 ID。客户端轮询 `tasks/status` 并在完成时获取 `tasks/result`。服务器端状态在重启后仍然存活。

## 核心概念

### 任务增强

请求通过设置 `params._meta.task.required: true`（或 `optional: true`，服务器决定）成为任务。服务器立即响应：

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

`ttl` 是服务器保留状态的承诺；ttl 之后任务结果被丢弃。

### 每工具选择加入

工具注解可以声明任务支持：

- `taskSupport: "forbidden"` — 此工具始终同步运行。适合快速工具。
- `taskSupport: "optional"` — 客户端可以请求任务增强。
- `taskSupport: "required"` — 客户端必须使用任务增强。

`generate_report` 工具应该是 `required`。`notes_search` 工具应该是 `forbidden`。

### 状态

```
working  -> input_required -> working  (通过 elicitation 循环)
working  -> completed
working  -> failed
working  -> cancelled
```

状态机是只追加的：一旦 `completed`、`failed` 或 `cancelled`，任务就是终态。

### 方法

- `tasks/status {taskId}` — 返回当前状态和进度提示。
- `tasks/result {taskId}` — 阻塞或在未完成时返回 404。
- `tasks/cancel {taskId}` — 幂等；终态忽略。
- `tasks/list` — 可选；枚举活动任务和最近完成的任务。

### 流式状态变更

当服务器支持时，客户端可以订阅状态通知：

```
server -> notifications/tasks/updated {taskId, state, progress?}
```

流式传输而非轮询的客户端获得更好的 UX。轮询始终作为最小表面支持。

### 持久化状态

规范要求声明任务支持的服务器持久化状态。崩溃不应丢失 TTL 内的已完成结果。存储方式从 SQLite 到 Redis 到文件系统。第 13 课的线束使用文件系统。

### 取消语义

`tasks/cancel` 是幂等的。如果任务正在执行中，服务器尝试停止（检查执行器协作取消）。如果已经是终态，请求是空操作。

### 崩溃恢复

当服务器进程重启时：

1. 加载所有持久化的任务状态。
2. 将进程死亡的 `working` 任务标记为 `failed`，错误为 `CRASH_RECOVERY`。
3. 在其 TTL 内保留 `completed` / `failed` / `cancelled` 任务。

### 异步任务加采样

任务本身可以调用 `sampling/createMessage`。这就是长时间运行的研究任务的工作方式：服务器的任务线程根据需要采样客户端的模型，同时客户端的 UI 将任务显示为 `working` 并定期更新进度。

### 为什么这是实验性的

SEP-1686 在 2025-11-25 中发布，但更广泛的路线图指出了三个开放问题：持久订阅原语、子任务（父子任务关系）和结果 TTL 标准化。预计规范在 2026 年全年会演化。生产代码应仅在常见情况下将 Tasks 视为稳定，并防范未来子任务的 SDK 变更。

## 用框架实现

`code/main.py` 实现了一个持久化任务存储（文件系统支持）和一个在后台线程中运行的 `generate_report` 工具。客户端调用工具，立即获得任务 ID，在线程更新进度时轮询 `tasks/status`，并在完成时获取 `tasks/result`。取消功能正常；崩溃恢复通过杀死工作线程并重新加载状态来模拟。

关注点：

- 任务状态 JSON 持久化到 `/tmp/lesson-13-tasks/<id>.json`。
- 工作线程更新 `progress` 字段；轮询显示它递增。
- 从客户端取消设置事件；工作线程检查并提前退出。
- "崩溃"时状态重载将进行中的任务标记为 `CRASH_RECOVERY` 失败。

## 产出物

本课产生 `outputs/skill-task-store-designer.md`。给定一个长时间运行的工具（研究、构建、导出），该技能设计任务存储（状态形状、ttl、持久性），选择正确的 taskSupport 标志，并勾画进度通知。

## 练习题

1. 运行 `code/main.py`。启动一个 `generate_report` 任务，轮询状态，然后获取结果。

2. 在运行中途添加一个 `tasks/cancel` 调用。验证工作线程遵守它，状态变为 `cancelled`。

3. 模拟崩溃恢复：杀死工作线程，重启加载器，观察 `CRASH_RECOVERY` 失败模式。

4. 将存储扩展到 SQLite。持久化收益相同；查询选项更多（列出会话 X 的所有任务）。

5. 阅读 MCP 2026 年路线图文章。识别最有可能在明年影响 SDK API 设计的一个与 Tasks 相关的开放问题。

## 术语速查表

| 术语 | 人们怎么说 | 实际含义 | 英文 |
|------|-----------|---------|------|
| 异步任务 | "长时运行工具调用" | 用 `_meta.task` 增强的请求用于异步执行 | Task |
| SEP-1686 | "Tasks 规范" | 2025-11-25 中添加 Tasks 的规范演进提案 | Tasks spec |
| `_meta.task` | "任务信封" | 包含 id、state、ttl 的每请求元数据 | Task envelope |
| 任务支持标志 | "工具标志" | 每工具的 `forbidden` / `optional` / `required` | taskSupport |
| 任务状态轮询 | "轮询方法" | 获取当前状态和可选进度提示 | `tasks/status` |
| 获取任务结果 | "获取结果" | 返回完成的载荷或在未完成时返回 404 | `tasks/result` |
| 取消任务 | "停止它" | 幂等的取消请求 | `tasks/cancel` |
| 任务保留时间 | "保留预算" | 服务器承诺保留任务状态的毫秒数 | ttl |
| 任务状态通知 | "状态推送" | 服务器发起的状态变更事件 | `notifications/tasks/updated` |
| 持久化存储 | "崩溃安全状态" | 文件系统 / SQLite / Redis 持久化层 | Durable store |

## 延伸阅读

- [MCP — GitHub SEP-1686 issue](https://github.com/modelcontextprotocol/modelcontextprotocol/issues/1686) — 原始提案和完整讨论
- [WorkOS — MCP async tasks for AI agent workflows](https://workos.com/blog/mcp-async-tasks-ai-agent-workflows) — 带理由的设计演练
- [DeepWiki — MCP task system and async operations](https://deepwiki.com/modelcontextprotocol/modelcontextprotocol/2.7-task-system-and-async-operations) — 机制和状态机
- [FastMCP — Tasks](https://gofastmcp.com/servers/tasks) — SDK 级别的任务实现模式
- [MCP blog — 2026 roadmap](https://blog.modelcontextprotocol.io/posts/2026-mcp-roadmap/) — 开放问题和 2026 年优先事项，包括子任务
