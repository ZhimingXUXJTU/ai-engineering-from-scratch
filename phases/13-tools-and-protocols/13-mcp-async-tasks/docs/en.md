# MCP Tasks Extension: Durable Work on a Stateless Core | MCP Tasks 扩展：无状态内核上的持久化任务

> Stateless MCP does not mean every operation must finish in one request. The official Tasks extension gives long-running work an explicit durable handle. A server can return that handle from `tools/call`, any instance can answer `tasks/get`, and client input arrives through `tasks/update` without reviving protocol sessions.

> **【中文解读】** 无状态 MCP 不等于每个操作都必须在一个请求内完成。官方 Tasks 扩展给长时间运行的工作一个显式的持久化句柄：服务器从 `tools/call` 返回句柄，任何实例都能应答 `tasks/get`，客户端输入通过 `tasks/update` 送达——全程不需要复活协议会话。注意本课已完全改版：Tasks 从 2025-11-25 的实验性核心特性（SEP-1686）迁移为官方 `io.modelcontextprotocol/tasks` 扩展，方法面也换了（`tasks/status`、`tasks/result`、`tasks/list` 已移除）。

> **【拓展：持久化任务→Agent 长时运行工作】** 异步任务是 MCP 处理长时运行工作的标准模式：深度研究、代码生成、批量导出这类需要几分钟到几小时的工作。与传统同步 `tools/call` 不同，Tasks 让服务器先持久化再返回 taskId，客户端稍后轮询快照或订阅通知。这是 MCP 从"简单工具执行"进化到"复杂工作流编排"的关键一步，与消息队列的"投递—确认—消费"语义遥相呼应。

> 🔗 **【前置】** 学本节前请先掌握：(1) Phase 13·09（transports）——Streamable HTTP 的 POST/SSE 形态，本课的 `Mcp-Method`/`Mcp-Name` 头直接建立在其上；(2) Phase 13·11（stateless MRTR）——无会话重试与 `inputRequests`/`inputResponses` 机制；(3) Phase 13·12（elicitation）——任务执行中收集用户输入用的就是同一套表单 schema。

**Type:** Build | **类型:** 构建
**Languages:** Python | **语言:** Python
**Prerequisites:** Phase 13 · 09 (transports), Phase 13 · 11 (stateless MRTR), Phase 13 · 12 (elicitation) | **前置知识:** Phase 13 · 09（transports）、Phase 13 · 11（无状态 MRTR）、Phase 13 · 12（elicitation）
**Time:** ~90 minutes | **时间:** 约 90 分钟

## Learning Objectives | 学习目标

- Distinguish stateless protocol transport from durable application task state.
  中文翻译：区分无状态的协议传输与持久化的应用任务状态。
- Negotiate the `io.modelcontextprotocol/tasks` extension in per-request capabilities and `server/discover`.
  中文翻译：在按请求能力与 `server/discover` 中协商 `io.modelcontextprotocol/tasks` 扩展。
- Return a server-directed `CreateTaskResult` with `resultType: "task"` only after durable creation.
  中文翻译：只有在持久化创建完成后，才返回带 `resultType: "task"` 的服务器主导 `CreateTaskResult`。
- Poll with `tasks/get`, fulfill task input with `tasks/update`, and request cooperative cancellation with `tasks/cancel`.
  中文翻译：用 `tasks/get` 轮询、用 `tasks/update` 补充任务输入、用 `tasks/cancel` 请求协作式取消。
- Remove the older `tasks/status`, `tasks/result`, and `tasks/list` assumptions.
  中文翻译：清除旧版 `tasks/status`、`tasks/result` 和 `tasks/list` 的假设。
- Subscribe to optional task notifications through `subscriptions/listen` on a POST response SSE stream.
  中文翻译：通过 POST 响应 SSE 流上的 `subscriptions/listen` 订阅可选的任务通知。
- Model task expiry, restart recovery, input-key deduplication, and execution errors correctly.
  中文翻译：正确建模任务过期、重启恢复、输入键去重和执行错误。

## Why Tasks Are an Extension | 为什么 Tasks 变成了扩展

> **【中文解读】** Tasks 最初是 2025-11-25 的实验性核心特性（当时叫 SEP-1686 任务增强）。2026 年 7 月的重设计把它移入官方 `io.modelcontextprotocol/tasks` 扩展——客户端和服务器按需选择加入这套额外生命周期，而不是让所有人为核心协议买单。扩展规范目前仍是草案表面：锁定 SDK 支持的扩展版本、跑一致性场景、把线上适配器与工作器和存储领域隔离。

Tasks first appeared as an experimental core feature in 2025-11-25. The July 2026 redesign moves them into the official `io.modelcontextprotocol/tasks` extension so clients and servers can opt into the extra lifecycle without expanding the core protocol for everyone.

> Tasks 最初作为实验性核心特性出现在 2025-11-25。2026 年 7 月的重设计把它们移入官方 `io.modelcontextprotocol/tasks` 扩展，让客户端和服务器可以按需选择加入这套额外生命周期，而不用为所有人扩大核心协议。

The extension specification remains a draft surface even though it is the current official home for Tasks. Pin the extension version supported by your SDK, run conformance scenarios, and isolate wire adapters from your worker and storage domain.

> 扩展规范目前仍是草案表面，尽管它已是 Tasks 当前的官方归宿。锁定你的 SDK 支持的扩展版本，运行一致性场景，并把线上适配器与你的工作器和存储领域隔离。

Use a task when the operation has one or more of these properties:

> 当操作具有以下一个或多个属性时使用任务：

- It may outlive an ordinary request timeout.
  中文翻译：它可能超出普通请求的超时时间。
- A worker queue or external job system already owns execution.
  中文翻译：某个工作队列或外部作业系统已经拥有执行权。
- The client needs to recover after its own restart.
  中文翻译：客户端需要在自己的重启后恢复。
- The operation pauses for user or model input during execution.
  中文翻译：操作在执行中会暂停等待用户或模型输入。
- Cancellation and durable result retrieval are product requirements.
  中文翻译：取消和持久化结果获取是产品需求。

Do not create a task for a cheap deterministic lookup. A handle, persistence, polling, expiry, and cancellation are real complexity.

> 不要为廉价的确定性查找创建任务。句柄、持久化、轮询、过期和取消都是实打实的复杂度。

## Stateless Core, Stateful Application | 无状态内核，有状态应用

> **【中文解读】** 这是本课的概念支点：MCP 2026-07-28 移除了 `initialize`、`notifications/initialized`、协议会话和 `Mcp-Session-Id`——但这不禁止有状态的产品。任务 id 是显式的应用状态：先持久化再返回；客户端可以存下来、重启后再轮询；id 可以路由到同一持久存储背后的任何副本；每次任务方法调用都重新做授权检查；过期与删除由任务字段定义，而非传输生命周期。把任务记录放进进程内存不会让 MCP 变有状态——只会让应用不可靠。

MCP 2026-07-28 removes `initialize`, `notifications/initialized`, protocol sessions, and `Mcp-Session-Id`. That does not prohibit stateful products.

> MCP 2026-07-28 移除了 `initialize`、`notifications/initialized`、协议会话和 `Mcp-Session-Id`。这并不禁止有状态的产品。

A task id is explicit application state:

> 任务 id 是显式的应用状态：

- The server persists it before returning it.
  中文翻译：服务器先持久化它再返回。
- The client can store it and poll again after restart.
  中文翻译：客户端可以存储它，重启后再次轮询。
- The id can route to any replica backed by the same durable store.
  中文翻译：该 id 可以路由到同一持久存储支撑的任何副本。
- Authorization is checked on every task method.
  中文翻译：每次任务方法调用都检查授权。
- Expiry and deletion are defined by task fields, not a transport lifetime.
  中文翻译：过期与删除由任务字段定义，而非传输生命周期。

This is operationally different from hidden state attached to a connection.

> 这在运维上不同于挂接在连接上的隐藏状态。

Keep four lifetimes separate:

> 把四种生命周期分开：

| State | Lifetime | Where it belongs |
|---|---|---|
| Protocol metadata | One request | `params._meta`, validated again on every call |
| Transport work | One stdio request or HTTP response | In-flight coordinator with a bounded deadline |
| MRTR continuation | One retry sequence | Integrity-protected `requestState`, plus replay controls when needed |
| Durable task | Across requests, replicas, restarts, and reconnects | Shared application store keyed by an authorized `taskId` |

> 表格对照（zh 版）：协议元数据——单个请求——`params._meta`，每次调用都重新校验；传输工作——单个 stdio 请求或 HTTP 响应——带有限deadline 的在途协调器；MRTR 续接——单个重试序列——完整性保护的 `requestState`，需要时加重放控制；持久化任务——跨请求、副本、重启和重连——以授权 `taskId` 为键的共享应用存储。

Moving a task record into process memory does not make MCP stateful. It makes the application unreliable. The protocol stays stateless, but a later `tasks/get` routed to another replica cannot recover the record. Persist before returning the handle, then make every task method resolve the same shared record under tenant and principal checks.

> 把任务记录放进进程内存不会让 MCP 变有状态，只会让应用不可靠。协议保持无状态，但稍后路由到另一个副本的 `tasks/get` 无法恢复该记录。先持久化再返回句柄，然后让每个任务方法在租户和主体检查之下解析同一份共享记录。

> 💡 **【类比】** 任务像餐厅的取餐号，但换成了"连锁店通兑"模式：你在 A 店点餐（tools/call），小票上是取餐号 42（taskId）——它存在连锁总部的订单系统（持久存储）里，不是某个店员的脑子里（进程内存）。你可以去任何一家分店问"42 号好了吗"（tasks/get 路由到任意副本）；中途店员问你要不要加辣（input_required），你答一句（tasks/update）；不想要了随时退单（tasks/cancel）。旧的"站在柜台干等"就是同步调用；旧的"SEP-1686 店员反向喊话"需要店员一直盯着你——新协议里没有这种会话了。

## Capability Negotiation | 能力协商

The client advertises support on every eligible request:

> 客户端在每个符合条件的请求上声明支持：

```json
{
  "_meta": {
    "io.modelcontextprotocol/protocolVersion": "2026-07-28",
    "io.modelcontextprotocol/clientCapabilities": {
      "extensions": {
        "io.modelcontextprotocol/tasks": {}
      }
    },
    "io.modelcontextprotocol/clientInfo": {
      "name": "lesson-client",
      "version": "1.0.0"
    }
  }
}
```

The server returns exact `supportedVersions`, capabilities, `ttlMs`, and `cacheScope` from `server/discover`, with the same extension under capabilities. Because it advertises tools, it also implements mandatory `tools/list`. That result returns a deterministic `generate_report` descriptor, valid object `inputSchema`, `resultType: "complete"`, server identity metadata, and public cache hints.

> 服务器从 `server/discover` 返回精确的 `supportedVersions`、能力、`ttlMs` 和 `cacheScope`，能力之下列出同一扩展。因为它声明了 tools，所以也实现强制的 `tools/list`。该结果返回确定性的 `generate_report` 描述符、合法的对象 `inputSchema`、`resultType: "complete"`、服务器身份元数据和公开缓存提示。

A task method from a client that did not declare the extension returns `-32021`, Missing Required Client Capability, with `data.requiredCapabilities` set to `{"extensions":{"io.modelcontextprotocol/tasks":{}}}`. An unsupported protocol string returns `-32022` with exact `supported` and `requested` data; a missing or non-string version returns `-32602`.

> 未声明扩展的客户端发出任务方法时返回 `-32021`（缺少必需客户端能力），`data.requiredCapabilities` 设为 `{"extensions":{"io.modelcontextprotocol/tasks":{}}}`。不支持的协议字符串返回 `-32022` 并附带精确的 `supported` 与 `requested` 数据；缺失或非字符串的版本返回 `-32602`。

An envelope without a JSON-RPC `id` is a notification. The receiver may process it, but it emits no JSON-RPC result or error. A Streamable HTTP adapter returns `202 Accepted` with no body for an accepted notification.

> 没有 JSON-RPC `id` 的信封是通知。接收方可以处理它，但不发出 JSON-RPC 结果或错误。Streamable HTTP 适配器对被接受的通知返回没有响应体的 `202 Accepted`。

At present, only `tools/call` supports task-augmented execution. Design your internal abstraction so future request types do not require rewriting storage.

> 目前只有 `tools/call` 支持任务增强执行。设计内部抽象时，让未来的请求类型不需要重写存储。

## Server-Directed Task Creation | 服务器主导的任务创建

> **【中文解读】** 这是与旧版最大的方向性变化：旧的客户端标志 `params._meta.task.required` 没了。现在客户端只声明扩展支持，由服务器决定某个 `tools/call` 是否变成任务——返回 `resultType: "task"` 加 `taskId`、`status`、`ttlMs`、`pollIntervalMs` 等字段。关键规则是 durable-before-return：在 `tasks/get` 能解析该 id 之前，服务器不得返回句柄；最终一致存储要先等读可见。

The old client flag `params._meta.task.required` is gone. The client declares extension support, then the server decides whether a particular `tools/call` becomes a task.

> 旧的客户端标志 `params._meta.task.required` 没了。客户端声明扩展支持，然后由服务器决定某个 `tools/call` 是否变成任务。

Request:

> 请求：

```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "method": "tools/call",
  "params": {
    "name": "generate_report",
    "arguments": {"size": "large"},
    "_meta": {
      "io.modelcontextprotocol/protocolVersion": "2026-07-28",
      "io.modelcontextprotocol/clientCapabilities": {
        "extensions": {
          "io.modelcontextprotocol/tasks": {}
        }
      }
    }
  }
}
```

Response:

> 响应：

```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "result": {
    "resultType": "task",
    "taskId": "tsk_786512e29e0d",
    "status": "working",
    "statusMessage": "Preparing report outline.",
    "createdAt": "2026-08-21T10:30:00Z",
    "lastUpdatedAt": "2026-08-21T10:30:00Z",
    "ttlMs": 900000,
    "pollIntervalMs": 1000
  }
}
```

The server must not return this handle until a `tasks/get` for the id can resolve. In an eventually consistent store, wait for read visibility before answering. Otherwise a client can receive a valid-looking id and immediately get "not found."

> 在 `tasks/get` 能解析该 id 之前，服务器不得返回这个句柄。在最终一致的存储中，应答前要等待读可见。否则客户端可能拿到一个看起来合法的 id，紧接着就得到"not found"。

A task response is unsolicited in the sense that the client does not request task mode. It is not unnegotiated: the current request still must advertise the extension.

> 任务响应在"客户端没有请求任务模式"的意义上是未经请求的。但它不是未经协商的：当前请求仍然必须声明该扩展。

> ⚠️ **【易错点】** 场景：先返回 taskId 再异步写存储 / 后果：客户端立刻 `tasks/get` 拿到 "not found"，重试风暴或用户以为任务丢失；多副本部署下别的副本更是必然查不到 / 修复：坚持 durable-before-return——先持久化（最终一致存储要等读可见）再返回句柄；`ttlMs` 从创建时刻起算，是兜底而非"完成后保留结果的承诺"。

## The Task Shape | 任务的数据形状

Every task carries:

> 每个任务都携带：

- `taskId`: stable server-generated identifier;
  中文翻译：`taskId`：服务器生成的稳定标识符；
- `status`: `working`, `input_required`, `completed`, `cancelled`, or `failed`;
  中文翻译：`status`：`working`、`input_required`、`completed`、`cancelled` 或 `failed`；
- `createdAt` and `lastUpdatedAt`: ISO 8601 timestamps;
  中文翻译：`createdAt` 与 `lastUpdatedAt`：ISO 8601 时间戳；
- `ttlMs`: expiry duration from creation, or `null` for no advertised limit;
  中文翻译：`ttlMs`：从创建起算的过期时长，`null` 表示不声明上限；
- optional `pollIntervalMs`: the server's current minimum suggested polling cadence;
  中文翻译：可选的 `pollIntervalMs`：服务器当前建议的最小轮询间隔；
- optional `statusMessage`: user-facing or model-facing context.
  中文翻译：可选的 `statusMessage`：面向用户或模型的上下文说明。

Status-specific fields appear only when relevant:

> 状态相关字段只在相关时出现：

- `input_required` includes `inputRequests`.
  中文翻译：`input_required` 包含 `inputRequests`。
- `completed` includes the original request's `result` shape.
  中文翻译：`completed` 包含原始请求的 `result` 形状。
- `failed` includes a JSON-RPC `error` object.
  中文翻译：`failed` 包含 JSON-RPC `error` 对象。

The client should honor `pollIntervalMs`. A server may rate-limit more aggressive polling and may change the interval over the task lifetime.

> 客户端应当遵守 `pollIntervalMs`。服务器可以对更激进的轮询限流，也可以在任务生命周期内改变该间隔。

## Poll with `tasks/get` | 用 `tasks/get` 轮询

The client asks for a current snapshot:

> 客户端请求当前快照：

```http
POST /mcp HTTP/1.1
Content-Type: application/json
MCP-Protocol-Version: 2026-07-28
Mcp-Method: tasks/get
Mcp-Name: tsk_786512e29e0d
```

```json
{
  "jsonrpc": "2.0",
  "id": 2,
  "method": "tasks/get",
  "params": {
    "taskId": "tsk_786512e29e0d",
    "_meta": {
      "io.modelcontextprotocol/protocolVersion": "2026-07-28",
      "io.modelcontextprotocol/clientCapabilities": {
        "extensions": {
          "io.modelcontextprotocol/tasks": {}
        }
      }
    }
  }
}
```

`tasks/get` itself completed, so its result always has `resultType: "complete"`. The nested task can still have `status: "working"` or `status: "input_required"`.

> `tasks/get` 本身已完成，所以它的结果总是 `resultType: "complete"`。嵌套的任务仍可能是 `status: "working"` 或 `status: "input_required"`。

This distinction prevents a common parser bug:

> 这个区分能防止一个常见的解析器 bug：

```text
result.resultType = complete    means the tasks/get RPC finished
result.status = working        means the represented job is still running
```

> 对照翻译：`result.resultType = complete` 表示 tasks/get 这个 RPC 结束了；`result.status = working` 表示它所代表的任务还在跑。

There is no `tasks/result` call. When the task completes, the next `tasks/get` response inlines the original `CallToolResult` under `result`:

> 没有 `tasks/result` 调用。任务完成后，下一次 `tasks/get` 响应把原始的 `CallToolResult` 内联在 `result` 下：

```json
{
  "resultType": "complete",
  "taskId": "tsk_786512e29e0d",
  "status": "completed",
  "createdAt": "2026-08-21T10:30:00Z",
  "lastUpdatedAt": "2026-08-21T10:34:12Z",
  "ttlMs": 900000,
  "result": {
    "resultType": "complete",
    "content": [
      {"type": "text", "text": "Generated large report with approved outline."}
    ],
    "structuredContent": {"size": "large", "approved": true},
    "isError": false,
    "_meta": {
      "io.modelcontextprotocol/serverInfo": {
        "name": "tasks-demo",
        "version": "1.0.0"
      }
    }
  },
  "_meta": {
    "io.modelcontextprotocol/serverInfo": {
      "name": "tasks-demo",
      "version": "1.0.0"
    }
  }
}
```

The outer `resultType` says the `tasks/get` RPC completed. The nested `result.resultType` says the original tool call completed. That nested discriminator is required. The nested `CallToolResult` SHOULD also carry its own `io.modelcontextprotocol/serverInfo`; this lesson includes it instead of storing an untyped payload.

> 外层 `resultType` 说明 `tasks/get` RPC 完成了。嵌套的 `result.resultType` 说明原始工具调用完成了。那个嵌套判别符是必需的。嵌套的 `CallToolResult` 还应当携带自己的 `io.modelcontextprotocol/serverInfo`；本课包含它，而不是存一个无类型载荷。

There is no `tasks/list`. Sessionless servers cannot safely infer which tasks belong in a connection-scoped list. Applications that need history should expose an authorized domain tool with explicit filters and ownership rules.

> 没有 `tasks/list`。无会话服务器无法安全推断哪些任务属于某个连接范围的列表。需要历史记录的应用应当暴露一个带显式过滤器和所有权规则的授权领域工具。

> 🤔 **【困惑】** Q: 旧的 `tasks/status`、`tasks/result` 不是更直观吗？为什么合并成一个 `tasks/get`？ A: 因为旧方法隐含"会话能圈定任务集合"的假设。无会话之后，服务器只能靠每次请求里的 `taskId` 定位任务，那就没有理由为"状态"和"结果"分设两个方法——`tasks/get` 一次返回完整快照，完成时内联结果。同理 `tasks/list` 被移除：需要列表就做一个显式的领域工具，自己定义过滤与授权。

## Input During Task Execution | 任务执行中的输入

Task input and core MRTR look similar but use different continuations.

> 任务输入与核心 MRTR 看着相似，但使用不同的续接方式。

### Input needed before task creation

Return core `resultType: "input_required"` from the original `tools/call`. The client fulfills it and retries that original call. Only create the task after those synchronous MRTR rounds finish.

> 在原始 `tools/call` 上返回核心的 `resultType: "input_required"`。客户端补全它并重试那个原始调用。只有等这些同步 MRTR 轮次结束后才创建任务。

### Input needed after task creation

Set the task to `input_required`. `tasks/get` exposes the outstanding `inputRequests`, and the client sends responses through `tasks/update`. The client does not retry the original `tools/call`.

> 把任务置为 `input_required`。`tasks/get` 暴露未决的 `inputRequests`，客户端通过 `tasks/update` 发送响应。客户端不重试原始的 `tools/call`。

> **【中文解读】** 输入时机决定续接方式，这是新规范里最容易搞混的点：创建任务前缺输入——走核心 MRTR（`input_required` 结果 + 客户端重试原始 `tools/call`）；创建任务后缺输入——走任务输入（任务状态置 `input_required`，客户端用 `tasks/update` 应答，不再重试原调用）。每条 `inputRequests` 的键在任务整个生命周期内必须唯一，客户端按键去重，服务器忽略未知/已作废/已应答的键。

Snapshot:

> 快照：

```json
{
  "resultType": "complete",
  "taskId": "tsk_786512e29e0d",
  "status": "input_required",
  "createdAt": "2026-08-21T10:30:00Z",
  "lastUpdatedAt": "2026-08-21T10:31:00Z",
  "ttlMs": 900000,
  "inputRequests": {
    "approve_outline": {
      "method": "elicitation/create",
      "params": {
        "mode": "form",
        "message": "Approve the generated report outline?",
        "requestedSchema": {
          "type": "object",
          "properties": {"approved": {"type": "boolean"}},
          "required": ["approved"]
        }
      }
    }
  }
}
```

Update:

> 更新：

```http
POST /mcp HTTP/1.1
Content-Type: application/json
MCP-Protocol-Version: 2026-07-28
Mcp-Method: tasks/update
Mcp-Name: tsk_786512e29e0d
```

```json
{
  "jsonrpc": "2.0",
  "id": 4,
  "method": "tasks/update",
  "params": {
    "taskId": "tsk_786512e29e0d",
    "inputResponses": {
      "approve_outline": {
        "action": "accept",
        "content": {"approved": true}
      }
    },
    "_meta": {
      "io.modelcontextprotocol/protocolVersion": "2026-07-28",
      "io.modelcontextprotocol/clientCapabilities": {
        "extensions": {
          "io.modelcontextprotocol/tasks": {}
        }
      }
    }
  }
}
```

The success response is an empty acknowledgement plus `resultType: "complete"`. The state change may be eventually consistent, so the client continues polling or listening.

> 成功响应是空确认加 `resultType: "complete"`。状态变更可能是最终一致的，所以客户端继续轮询或监听。

Each `inputRequests` key must be unique for the entire task lifetime. Repeated `tasks/get` snapshots may show the same outstanding key; clients deduplicate the UI and servers ignore responses for unknown, superseded, or already fulfilled keys. A partial update can leave the task in `input_required` until all required keys are answered.

> 每条 `inputRequests` 的键在任务整个生命周期内必须唯一。重复的 `tasks/get` 快照可能显示同一个未决键；客户端对 UI 去重，服务器忽略针对未知、已作废或已应答键的响应。部分更新可能让任务停留在 `input_required`，直到所有必需键都被应答。

## Cancellation Is Cooperative | 取消是协作式的

`tasks/cancel` signals intent and returns an empty complete acknowledgement. That acknowledgement does not guarantee the worker stopped. Work may finish first, ignore cancellation, or transition later.

> `tasks/cancel` 表达意图并返回空的完成确认。该确认不保证工作器已停止。工作可能先完成、忽略取消或稍后才转移状态。

```http
POST /mcp HTTP/1.1
Content-Type: application/json
MCP-Protocol-Version: 2026-07-28
Mcp-Method: tasks/cancel
Mcp-Name: tsk_786512e29e0d
```

```json
{
  "jsonrpc": "2.0",
  "id": 5,
  "method": "tasks/cancel",
  "params": {
    "taskId": "tsk_786512e29e0d",
    "_meta": {
      "io.modelcontextprotocol/protocolVersion": "2026-07-28",
      "io.modelcontextprotocol/clientCapabilities": {
        "extensions": {
          "io.modelcontextprotocol/tasks": {}
        }
      }
    }
  }
}
```

For all three task methods, `Mcp-Name` mirrors `params.taskId`. It does not repeat the JSON-RPC method name. `code/main.py` centralizes this rule in `make_http_request`.

> 对全部三个任务方法，`Mcp-Name` 镜像 `params.taskId`。它不重复 JSON-RPC 方法名。`code/main.py` 在 `make_http_request` 中集中实现了这条规则。

The lesson worker honors cancellation immediately, making repeated calls idempotent. A production client must still treat cancellation as cooperative rather than infer a final task status from the acknowledgement.

> 本课的工作器立即响应取消，使重复调用幂等。生产客户端仍必须把取消视为协作式的，而不是从确认推断最终任务状态。

Do not use `notifications/cancelled` to cancel a task. That notification belongs to request cancellation, not durable Tasks.

> 不要用 `notifications/cancelled` 取消任务。那个通知属于请求取消，而非持久化 Tasks。

> **【中文解读】** 记住两条分界线：(1) `notifications/cancelled` 取消的是"请求"，`tasks/cancel` 取消的是"任务"——一旦 `tools/call` 已返回 `resultType: "task"`，那个请求就已完结，断开连接碰不到持久化任务；(2) `tasks/cancel` 的确认只代表"意图已记录"，不代表工作器已停止——生产客户端要从后续 `tasks/get` 快照确认终态，而不是从确认推断。

The distinction matters at the routing boundary. Request cancellation targets one in-flight JSON-RPC operation or its request-scoped HTTP response. If `tools/call` has already returned `resultType: "task"`, that request is complete and closing its transport cannot name or stop the durable job. `tasks/cancel` is a new authorized RPC. It carries `params.taskId`, mirrors that id in `Mcp-Name`, resolves the task's owning backend, records cooperative cancellation intent, and returns an acknowledgement without claiming the worker has stopped.

> 这个区分在路由边界很重要。请求取消针对一个在途 JSON-RPC 操作或其请求范围的 HTTP 响应。如果 `tools/call` 已返回 `resultType: "task"`，该请求就完结了，关闭其传输既无法点名也无法停止那个持久化任务。`tasks/cancel` 是一个新的授权 RPC。它携带 `params.taskId`、在 `Mcp-Name` 中镜像该 id、解析任务归属的后端、记录协作取消意图，并返回确认——但不声称工作器已停止。

A gateway must therefore keep request coordinators and task routes in different tables. The request table can disappear when the response finishes. The task route must survive until terminal state and retention expiry. [Lesson 29: MCP Reliability, Cancellation, and Flow Control](../../29-mcp-reliability-cancellation-and-flow-control/docs/en.md) builds the race, timeout, idempotency, backpressure, and retry rules for both paths.

> 因此网关必须把请求协调器和任务路由放在不同的表里。请求表可以在响应结束后消失。任务路由必须存活到终态和保留期过期。[Lesson 29: MCP Reliability, Cancellation, and Flow Control](../../29-mcp-reliability-cancellation-and-flow-control/docs/en.md) 构建了两条路径的竞争、超时、幂等、背压和重试规则。

## Optional Notifications | 可选通知

Polling is the baseline. A client that wants push updates sends `subscriptions/listen` with task ids. For Streamable HTTP, this is a POST whose response is a request-scoped SSE stream. There is no standalone GET event stream and no protocol session to keep alive.

> 轮询是基线。想要推送更新的客户端发送携带任务 id 的 `subscriptions/listen`。对 Streamable HTTP 而言，这是一个 POST，其响应是请求范围的 SSE 流。没有独立的 GET 事件流，也没有需要保活的协议会话。

The server acknowledges the accepted ids with `notifications/subscriptions/acknowledged` and can then send full snapshots through `notifications/tasks`. The acknowledgement and every task notification carry `io.modelcontextprotocol/subscriptionId` in `_meta`, equal to the `subscriptions/listen` request id. Each task notification is otherwise equivalent to what `tasks/get` would return at that moment.

> 服务器用 `notifications/subscriptions/acknowledged` 确认被接受的 id，然后可以通过 `notifications/tasks` 发送完整快照。确认和每条任务通知都在 `_meta` 中携带 `io.modelcontextprotocol/subscriptionId`，等于 `subscriptions/listen` 的请求 id。每条任务通知在其他方面等价于 `tasks/get` 当时会返回的内容。

Clients must still declare the Tasks extension. They should reconnect and resume from durable task ids rather than depend on event replay or `Last-Event-ID`.

> 客户端仍必须声明 Tasks 扩展。它们应当重连并从持久化任务 id 恢复，而不是依赖事件重放或 `Last-Event-ID`。

## Failure Semantics | 失败语义

Use the two error layers correctly.

> 正确使用两个错误层。

### Protocol error

Invalid method parameters or an unknown task id return a JSON-RPC error, commonly `-32602`. Missing extension support returns `-32021` with the required capability object.

> 无效的方法参数或未知的任务 id 返回 JSON-RPC 错误，通常是 `-32602`。缺少扩展支持返回 `-32021` 并附带所需能力对象。

### Task execution outcome

- A normal tool result with `isError: true` is still a `completed` task because the tool call produced its defined result.
  中文翻译：带 `isError: true` 的普通工具结果仍是 `completed` 任务，因为工具调用产生了其定义的结果。
- A JSON-RPC error during deferred execution makes the task `failed` and stores that JSON-RPC error under `error`.
  中文翻译：延迟执行期间的 JSON-RPC 错误使任务变为 `failed`，并把该 JSON-RPC 错误存入 `error`。
- User refusal can produce `cancelled`, a completed refusal result, or another domain-specific safe outcome. Document the choice.
  中文翻译：用户拒绝可以产生 `cancelled`、一个完成的拒绝结果，或其他领域特定的安全结局。把你的选择写进文档。

## Durability, Expiry, and Ownership | 持久化、过期与所有权

Persist at least the task id, status, timestamps, ttl, poll interval, original operation ownership, result or error, outstanding input requests, and all issued input keys.

> 至少持久化任务 id、状态、时间戳、ttl、轮询间隔、原始操作所有权、结果或错误、未决输入请求和所有已发出的输入键。

The storage key must include or resolve an authoritative tenant and principal. Knowing a task id must not grant access. Check ownership on every `tasks/get`, `tasks/update`, `tasks/cancel`, and subscription.

> 存储键必须包含或能解析出权威的租户和主体。知道一个任务 id 不应授予访问权。在每次 `tasks/get`、`tasks/update`、`tasks/cancel` 和订阅上检查所有权。

`ttlMs` is measured from creation and may change. A client can treat it as a backstop when a task has stopped producing observable updates. A server may fail and later delete an expired task. Do not describe it as a promise to retain a completed result for that many milliseconds after completion.

> `ttlMs` 从创建起算且可能变化。当任务停止产生可观察更新时，客户端可以把它当兜底。服务器可能失败并在之后删除过期任务。不要把它描述成"完成后还会把结果保留那么多少毫秒"的承诺。

Use atomic writes or transactions. The lesson writes a temporary file and atomically renames it. A multi-replica service should use a shared durable store and a worker lease or equivalent concurrency control.

> 使用原子写或事务。本课写临时文件再原子改名。多副本服务应使用共享持久存储和工作者租约或等价的并发控制。

```figure
tp-task-lifecycle
```

## Build It | 动手构建

`code/main.py` implements a deterministic task service:

> `code/main.py` 实现一个确定性的任务服务：

- `server/discover` returns `supportedVersions`, cache hints, and the Tasks extension.
  中文翻译：`server/discover` 返回 `supportedVersions`、缓存提示和 Tasks 扩展。
- `tools/list` returns a deterministic, cacheable `generate_report` descriptor with a valid input schema.
  中文翻译：`tools/list` 返回带合法输入 schema 的确定性、可缓存 `generate_report` 描述符。
- `tools/call` creates and persists the task before returning `resultType: "task"`.
  中文翻译：`tools/call` 在返回 `resultType: "task"` 之前创建并持久化任务。
- A new service instance reloads the same task, demonstrating restart recovery.
  中文翻译：新的服务实例重载同一任务，演示重启恢复。
- `tasks/get` returns complete task snapshots.
  中文翻译：`tasks/get` 返回完整任务快照。
- The worker moves from `working` to `input_required`.
  中文翻译：工作器从 `working` 转到 `input_required`。
- `tasks/update` accepts a form response and returns an empty complete acknowledgement.
  中文翻译：`tasks/update` 接受表单响应并返回空的完成确认。
- The worker stores a nested `CallToolResult` with its own `resultType` and server identity, then transitions to `completed`.
  中文翻译：工作器存储带自己的 `resultType` 和服务器身份的嵌套 `CallToolResult`，然后转移到 `completed`。
- `tasks/cancel` is idempotent in this implementation.
  中文翻译：本实现中 `tasks/cancel` 是幂等的。
- The HTTP builder sets `Mcp-Name` to `params.taskId` for `tasks/get`, `tasks/update`, and `tasks/cancel`.
  中文翻译：HTTP 构建器为 `tasks/get`、`tasks/update` 和 `tasks/cancel` 把 `Mcp-Name` 设为 `params.taskId`。
- Notification helpers use `notifications/subscriptions/acknowledged` and `notifications/tasks`, both tagged with the listen request id.
  中文翻译：通知辅助函数使用 `notifications/subscriptions/acknowledged` 和 `notifications/tasks`，两者都带监听请求 id 的标签。
- Id-less notifications produce no JSON-RPC response.
  中文翻译：无 id 的通知不产生 JSON-RPC 响应。

The worker advances explicitly instead of sleeping in a background thread. That makes every state transition deterministic and keeps the protocol example separate from queue mechanics.

> 工作器显式推进，而不是在后台线程里睡眠。这使每次状态转移都是确定性的，并让协议示例与队列机制保持分离。

## Use It | 运行验证

From the repository root:

> 从仓库根目录：

```bash
cd phases/13-tools-and-protocols/13-mcp-async-tasks/code
python3 main.py
python3 -m unittest discover tests -v
```

Expected result sequence:

> 预期结果序列：

```text
id=0 resultType=complete status=ack
id=1 resultType=task status=working
id=2 resultType=complete status=working
id=3 resultType=complete status=input_required
id=4 resultType=complete status=ack
id=5 resultType=complete status=completed
```

Also verify that `tasks/status`, `tasks/result`, and `tasks/list` return method-not-found in the modern service.
> 还要验证 `tasks/status`、`tasks/result` 和 `tasks/list` 在现代服务中返回 method-not-found。
Verify that `tools/list` is deterministic and every current HTTP task method mirrors its task id through `Mcp-Name`.

> 验证 `tools/list` 是确定性的，且每个现行 HTTP 任务方法都通过 `Mcp-Name` 镜像其任务 id。

## Ship It | 产出物

`outputs/skill-task-store-designer.md` now produces an extension-aware design: capability negotiation, durable-before-return creation, current methods, input update flow, ownership, expiry, cancellation, subscription, and migration from the removed experimental methods.

> `outputs/skill-task-store-designer.md` 现在产出扩展感知的设计：能力协商、durable-before-return 创建、现行方法、输入更新流、所有权、过期、取消、订阅，以及从已移除的实验性方法迁移。

## Exercises | 练习题

1. Add a second outstanding input key. Send a partial `tasks/update` and prove the task remains `input_required` until both keys are answered.
   中文翻译：添加第二个未决输入键。发送部分 `tasks/update`，证明任务在两个键都被应答前保持 `input_required`。
2. Add tenant ownership to the store and reject a valid task id presented by the wrong authenticated principal.
   中文翻译：给存储添加租户所有权，拒绝由错误的已认证主体出示的合法任务 id。
3. Add a worker lease with expiry. Demonstrate that two service instances cannot complete the same task concurrently.
   中文翻译：添加带过期的工作者租约。证明两个服务实例不能并发完成同一任务。
4. Implement a POST-response SSE adapter for `subscriptions/listen`. Do not add GET, `Last-Event-ID`, or a session header.
   中文翻译：为 `subscriptions/listen` 实现 POST 响应 SSE 适配器。不要添加 GET、`Last-Event-ID` 或会话头。
5. Add expiry cleanup. Distinguish an expired task from a malformed task id without leaking cross-tenant existence.
   中文翻译：添加过期清理。区分过期任务与格式错误的任务 id，且不泄露跨租户的存在性。

## Key Terms | 术语速查表

| Term | Meaning in the current extension |
|------|----------------------------------|
| Tasks extension | Optional `io.modelcontextprotocol/tasks` capability for durable async work |
| `CreateTaskResult` | Server-directed `resultType: "task"` response to an eligible request |
| `tasks/get` | Poll a full current task snapshot, including terminal result or pending input |
| `tasks/update` | Submit responses to a task's outstanding `inputRequests` |
| `tasks/cancel` | Acknowledge cooperative cancellation intent |
| `input_required` | Task status indicating client input is outstanding |
| `pollIntervalMs` | Server-suggested minimum delay before another poll |
| `ttlMs` | Expiry duration measured from task creation |
| Durable-before-return | Rule that the task id must resolve before its handle is sent |
| `notifications/tasks` | Optional full task snapshot delivered on a subscribed SSE response |

> **【中文解读】** 术语速查（中英对照）：Tasks extension=官方 `io.modelcontextprotocol/tasks` 扩展能力；CreateTaskResult=对合格请求的服务器主导 `resultType: "task"` 响应；`tasks/get`=轮询完整任务快照（含终态结果或未决输入）；`tasks/update`=提交对未决 `inputRequests` 的响应；`tasks/cancel`=确认协作取消意图；input_required=任务状态，表示客户端输入未决；pollIntervalMs=服务器建议的最小轮询间隔；ttlMs=从任务创建起算的过期时长；Durable-before-return=句柄发出前任务 id 必须已可解析；`notifications/tasks`=订阅 SSE 响应上投递的可选完整任务快照。

## Legacy Compatibility | 旧版兼容

The 2025-11-25 experimental surface used client-requested task augmentation, `tasks/status`, `tasks/result`, and optional `tasks/list`. Keep those names only inside a pinned legacy adapter. A current client uses the extension capability, accepts server-directed handles, polls `tasks/get`, supplies input with `tasks/update`, and reads the final result from the task snapshot.

> 2025-11-25 实验性表面使用客户端请求的任务增强、`tasks/status`、`tasks/result` 和可选的 `tasks/list`。只在锁定的旧版适配器内保留这些名字。现行客户端使用扩展能力、接受服务器主导的句柄、轮询 `tasks/get`、用 `tasks/update` 补充输入，并从任务快照读取最终结果。

## Further Reading | 延伸阅读

- [Official MCP Tasks extension](https://tasks.extensions.modelcontextprotocol.io/specification/draft/tasks)
  中文翻译：官方 MCP Tasks 扩展规范（当前为草案）。
- [MCP 2026-07-28 Multi Round-Trip Requests](https://modelcontextprotocol.io/specification/2026-07-28/basic/patterns/mrtr)
  中文翻译：MRTR 模式规范，任务创建前输入收集的机制来源。
- [MCP 2026-07-28 Streamable HTTP](https://modelcontextprotocol.io/specification/2026-07-28/basic/transports/streamable-http)
  中文翻译：Streamable HTTP 传输规范，`Mcp-Method`/`Mcp-Name` 头与 POST 响应 SSE 的定义处。
