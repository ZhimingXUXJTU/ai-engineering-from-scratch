# Building an MCP Client — Discovery, Invocation, Session Management | 构建 MCP 客户端：发现、调用与会话管理

> Most MCP content ships server tutorials and waves a hand at the client. Client code is where the hard orchestration lives: process spawning, capability negotiation, tool list merging across multiple servers, sampling callbacks, reconnection, and namespace collision resolution. This lesson builds a multi-server client that lifts three different MCP servers into one flat tool namespace for the model.

> **【中文解读】** 大多数 MCP 内容只教服务器端教程。客户端代码才是真正复杂的编排所在：进程生成、能力协商、多服务器工具列表合并、sampling 回调、重连和命名空间冲突解决。本课构建一个多服务器客户端，将三个不同的 MCP 服务器提升到一个扁平的工具命名空间中。

> **【拓展：MCP 客户端→Agent 编排核心】** MCP 客户端是 Agent 宿主的核心。Claude Desktop、Cursor 等都实现了 MCP 客户端，同时加载多个 MCP 服务器（如文件系统、Postgres、GitHub），将工具列表合并后提供给模型。命名空间冲突解决（前缀 vs 拒绝）是实际部署中的关键设计决策。

**Type:** Build | **类型:** 构建
**Languages:** Python (stdlib, multi-server MCP client) | **语言:** Python (stdlib, multi-server MCP client)
**Prerequisites:** Phase 13 · 07 (building an MCP server) | **前置知识:** Phase 13 · 07 (building an MCP server)
**Time:** ~75 minutes | **时间:** ~75 分钟

## Learning Objectives | 学习目标

- Spawn an MCP server as a child process, complete `initialize`, and send a `notifications/initialized`.
  中文翻译：参见英文条目了解详情。
- Maintain per-server session state (capabilities, tool list, last-seen notification ids).
  中文翻译：参见英文条目了解详情。
- Merge tool lists across multiple servers into one namespace with collision handling.
  中文翻译：参见英文条目了解详情。
- Route a tool call to the server that owns it and reassemble the response.
  中文翻译：参见英文条目了解详情。

## The Problem | 问题引入

A real agent host (Claude Desktop, Cursor, Goose, Gemini CLI) loads multiple MCP servers at once. A user might have a filesystem server, a Postgres server, and a GitHub server running simultaneously. The client's job:

> MCP 服务器端的核心实现：暴露工具、资源和提示模板，通过 JSON-RPC 2.0 与客户端通信。

1. Spawn each server.
  中文翻译：参见英文条目了解详情。
2. Handshake each independently.
  中文翻译：参见英文条目了解详情。
3. Call `tools/list` on each and flatten the result.
  中文翻译：参见英文条目了解详情。
4. When the model emits `notes_search`, look it up in the merged namespace and route to the right server.
  中文翻译：参见英文条目了解详情。
5. Handle notifications from any server (`tools/list_changed`) without blocking.
  中文翻译：参见英文条目了解详情。
6. Reconnect on transport failure.
  中文翻译：参见英文条目了解详情。

Hand-rolling all of that is what separates "toy" from "serviceable". The official SDKs wrap this, but the mental model has to be yours.

> **【中文解读】** 真正的 Agent 宿主同时加载多个 MCP 服务器。客户端的工作：(1) 生成每个服务器；(2) 独立握手；(3) 在每个服务器上调用 `tools/list` 并扁平化结果；(4) 当模型发出 `notes_search` 时，在合并命名空间中查找并路由到正确服务器；(5) 处理任意服务器的通知而不阻塞；(6) 传输失败时重连。

## The Concept | 核心概念

### Child-process spawning

> **【中文解读】** 客户端用 `subprocess.Popen` 生成每个 MCP 服务器子进程，设置 `stdin=PIPE, stdout=PIPE, stderr=PIPE`，`bufsize=1` 并使用文本模式逐行读取。每个服务器是一个进程，客户端持有对应的 Popen 句柄。

`subprocess.Popen` with `stdin=PIPE, stdout=PIPE, stderr=PIPE`. Set `bufsize=1` and use text mode for line-by-line reads. Each server is one process; the client holds one `Popen` handle per server.

> 参见英文原文获取完整的技术说明。

### Per-server session state

A `Session` object per server holds:

> 会话管理相关内容：MCP 会话的建立、维护和终止。

- `process` — the Popen handle.
  中文翻译：参见英文条目了解详情。
- `capabilities` — what the server declared at `initialize`.
  中文翻译：参见英文条目了解详情。
- `tools` — the last `tools/list` result.
  中文翻译：参见英文条目了解详情。
- `pending` — map of request id to a promise/future waiting for the response.
  中文翻译：参见英文条目了解详情。

Requests are async by nature; a `tools/call` sent to server A while server B is mid-call must not block. Either use threads with queues or asyncio.

> 异步任务相关内容：长时间运行工具的进度报告和任务管理。

### Merged namespace

> **【拓展：多 MCP 服务器命名空间冲突处理】** 当多个服务器有同名工具时，客户端有三种处理策略：(1) 按服务器名前缀（`notes/search`、`files/search`），清晰但冗长——Claude Desktop 和 VS Code 用这种方式；(2) 先到先得，后加载的覆盖先加载的——风险高，隐藏冲突；(3) 碰撞拒绝，拒绝加载第二个服务器——Cursor 用这种方式，对安全敏感的宿主最安全。

When the client sees the aggregate tool list, names can collide. Two servers might both expose `search`. The client has three options:

> 工具调用相关内容：工具发现、调用和结果返回。

1. **Prefix by server name.** `notes/search`, `files/search`. Clear but ugly.
  中文翻译：**Prefix by server name.** — 参见英文原文了解详情。
2. **Silent first-come.** Later server's `search` overrides the earlier. Risky; hides collisions.
  中文翻译：**Silent first-come.** — 参见英文原文了解详情。
3. **Collision rejection.** Refuse to load the second server; notify the user. Safest for security-sensitive hosts.
  中文翻译：**Collision rejection.** — 参见英文原文了解详情。

Claude Desktop uses prefix-by-server. Cursor uses collision rejection with a clear error. VS Code MCP adopts prefix-by-server as well.

> MCP 服务器端的核心实现：暴露工具、资源和提示模板，通过 JSON-RPC 2.0 与客户端通信。

### Routing

> **【中文解读】** 合并后，调度表将 `tool_name -> session` 映射起来。模型按名称发出调用，客户端找到对应 session 并向该服务器的 stdin 写入 `tools/call` 消息，然后等待响应。

After merging, a dispatch table maps `tool_name -> session`. The model emits a call by name; the client finds the session and writes a `tools/call` message to that server's stdin, then awaits the response.

> 工具调用相关内容：工具发现、调用和结果返回。

### Sampling callback

If the server declared the `sampling` capability at `initialize`, it may send `sampling/createMessage` asking the client to run its LLM. The client must:

> 采样相关内容：服务器请求客户端模型执行补全的机制。

1. Block further requests to that server until the sample resolves, or pipeline if its implementation supports concurrency.
  中文翻译：参见英文条目了解详情。
2. Call its LLM provider.
  中文翻译：参见英文条目了解详情。
3. Send the response back to the server.
  中文翻译：参见英文条目了解详情。

Lesson 11 covers sampling end-to-end. This lesson stubs it for completeness.

> 采样相关内容：服务器请求客户端模型执行补全的机制。

### Notification handling

> **【中文解读】** `notifications/tools/list_changed` 意味着重新调用 `tools/list`。`notifications/resources/updated` 意味着重新读取正在使用的资源。通知不得产生响应。常见客户端 bug：在 `tools/call` 上阻塞读取循环，而通知排在流中。解决方案：使用后台读取线程将每条消息推入队列，主线程出队并分发。

`notifications/tools/list_changed` means re-call `tools/list`. `notifications/resources/updated` means re-read the resource if it is in use. Notifications must not produce responses — do not try to ack them.

> 资源相关内容：MCP 资源的暴露、订阅和读取机制。

A common client bug: blocking the read loop on `tools/call` while a notification sits in the stream. Use a background reader thread that pushes every message onto a queue; the main thread dequeues and dispatches.

> 工具调用相关内容：工具发现、调用和结果返回。

### Reconnection

> **【拓展：MCP 传输失败与重连策略】** 传输可能因服务器崩溃、OS 杀进程或 stdio 管道断裂而失败。客户端检测 stdout 上的 EOF 并将会话标记为死亡。两种重连策略：(1) 静默重启服务器并重新握手——适合纯只读服务器；(2) 向用户报告失败——适合有状态和用户可见会话的服务器。Phase 13.09 覆盖 Streamable HTTP 重连语义。

Transport can fail: server crashed, OS killed the process, stdio pipe broke. The client detects EOF on stdout and treats the session as dead. Options:

> 传输层相关内容：stdio 用于本地通信，Streamable HTTP 用于远程部署。

- Silently restart the server and re-handshake. OK for pure read-only servers.
  中文翻译：参见英文条目了解详情。
- Surface the failure to the user. OK for stateful servers with user-visible sessions.
  中文翻译：参见英文条目了解详情。

Phase 13 · 09 covers the Streamable HTTP reconnection semantics; stdio is simpler.

> 传输层相关内容：stdio 用于本地通信，Streamable HTTP 用于远程部署。

### Keepalive and session id

Streamable HTTP uses a `Mcp-Session-Id` header. Stdio has no session id — the process identity IS the session. Keepalive pings are optional; stdio pipes do not break under inactivity.

> 传输层相关内容：stdio 用于本地通信，Streamable HTTP 用于远程部署。

## Use It | 用框架实现

`code/main.py` spawns three simulated MCP servers as subprocesses, handshakes each, merges their tool lists, and routes tool calls to the right one. The "servers" are actually other Python processes running toy responders (no real LLM). Run it to see:

> MCP 服务器端的核心实现：暴露工具、资源和提示模板，通过 JSON-RPC 2.0 与客户端通信。

- Three initializations, each with their own capability set.
  中文翻译：参见英文条目了解详情。
- Three `tools/list` results merged into a 7-tool namespace.
  中文翻译：参见英文条目了解详情。
- A routing decision based on the tool name.
  中文翻译：参见英文条目了解详情。
- A collision prevented by namespace prefixing.
  中文翻译：参见英文条目了解详情。

What to look at:

- The `Session` dataclass holds per-server state cleanly.
  中文翻译：参见英文条目了解详情。
- The background reader thread dequeues every line on stdout without blocking the main thread.
  中文翻译：参见英文条目了解详情。
- The dispatch table is a simple `dict[str, Session]`.
  中文翻译：参见英文条目了解详情。
- Collision handling is explicit: when two servers declare the same name, the later one is renamed with a prefix.
  中文翻译：参见英文条目了解详情。

## Ship It | 产出物

This lesson produces `outputs/skill-mcp-client-harness.md`. Given a declarative list of MCP servers (name, command, args), the skill produces a harness that spawns them, merges tool lists, and ships a routing function with collision resolution.

> MCP 服务器端的核心实现：暴露工具、资源和提示模板，通过 JSON-RPC 2.0 与客户端通信。

## Exercises | 练习题

1. Run `code/main.py` and watch the server spawn log. Kill one of the simulated server processes with a SIGTERM and observe how the client detects the EOF and marks that session as dead.
   中文翻译：运行相关练习。参见英文原文了解完整要求。

2. Implement namespace prefixing. When two servers expose `search`, rename the second as `<server>/search`. Update the dispatch table and verify tool calls route correctly.
   中文翻译：实现相关练习。参见英文原文了解完整要求。

3. Add a connection-pool-style backoff for server restart: exponential backoff on consecutive failures, cap at 30 seconds, emit a notification to the user after three failures.
   中文翻译：添加相关练习。参见英文原文了解完整要求。

4. Sketch a client that supports 100 concurrent MCP servers. What data structure replaces the simple dispatch dict? (Hint: trie for prefix namespacing, plus a metric for tool-count-per-server.)
   中文翻译：勾勒相关练习。参见英文原文了解完整要求。

5. Port the client to the official MCP Python SDK. The SDK wraps `stdio_client` and `ClientSession`. The code should shrink from ~200 lines to ~40 lines while preserving multi-server routing.
   中文翻译：参见英文原文了解完整练习要求。

## Key Terms | 术语速查表

| Term | What people say | What it actually means | 中文术语 |
|------|----------------|------------------------|----------|
| MCP client | "The agent host" | Process that spawns servers and orchestrates tool calls | MCP 客户端 |
| Session | "Per-server state" | Capabilities, tool list, and pending-request bookkeeping | 会话状态 |
| Merged namespace | "One tool list" | Flat set of tool names across all active servers | 合并命名空间 |
| Namespace collision | "Two servers same tool" | Client must prefix, reject, or first-come the duplicate | 命名空间冲突 |
| Routing | "Who gets this call?" | Dispatch from tool name to owning server | 工具路由 |
| Background reader | "Non-blocking stdout" | Thread or task that drains server stdout into a queue | 后台读取线程 |
| Sampling callback | "LLM-as-a-service" | Client handler for `sampling/createMessage` from server | 采样回调 |
| `notifications/*_changed` | "Primitive mutated" | Signal the client must re-discover or re-read | 变更通知 |
| Reconnection policy | "When server dies" | Restart semantics when transport fails | 重连策略 |
| Stdio session | "Process = session" | No session id; child process lifetime is the session | stdio 会话 |

## Further Reading | 延伸阅读

- [Model Context Protocol — Client spec](https://modelcontextprotocol.io/specification/2025-11-25/client) — canonical client behavior
  中文翻译：canonical client behavior
- [MCP — Quickstart client guide](https://modelcontextprotocol.io/quickstart/client) — hello-world client tutorial with the Python SDK
  中文翻译：hello-world client tutorial with the Python SDK
- [MCP Python SDK — client module](https://github.com/modelcontextprotocol/python-sdk) — reference `ClientSession` and `stdio_client`
  中文翻译：reference `ClientSession` and `stdio_client`
- [MCP TypeScript SDK — Client](https://github.com/modelcontextprotocol/typescript-sdk) — TS parallel
  中文翻译：TS parallel
- [VS Code — MCP in extensions](https://code.visualstudio.com/api/extension-guides/ai/mcp) — how VS Code multiplexes multiple MCP servers in a single editor host
  中文翻译：how VS Code multiplexes multiple MCP servers in a single editor host
