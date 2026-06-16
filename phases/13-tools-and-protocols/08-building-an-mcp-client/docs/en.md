# Building an MCP Client — Discovery, Invocation, Session Management | 构建 MCP 客户端：发现、调用与会话管理

> Most MCP content ships server tutorials and waves a hand at the client. Client code is where the hard orchestration lives: process spawning, capability negotiation, tool list merging across multiple servers, sampling callbacks, reconnection, and namespace collision resolution. This lesson builds a multi-server client that lifts three different MCP servers into one flat tool namespace for the model.

> **【中文解读】** 大多数 MCP 内容只教服务器端教程。客户端代码才是真正复杂的编排所在：进程生成、能力协商、多服务器工具列表合并、sampling 回调、重连和命名空间冲突解决。本课构建一个多服务器客户端，将三个不同的 MCP 服务器提升到一个扁平的工具命名空间中。

> **【拓展：MCP 客户端→Agent 编排核心】** MCP 客户端是 Agent 宿主的核心。Claude Desktop、Cursor 等都实现了 MCP 客户端，同时加载多个 MCP 服务器（如文件系统、Postgres、GitHub），将工具列表合并后提供给模型。命名空间冲突解决（前缀 vs 拒绝）是实际部署中的关键设计决策。

> 🔗 **【前置】** 学本节前请先掌握：(1) Phase 13·07（Building an MCP Server）——理解服务器端的 initialize/tools/call 协议；(2) Python `subprocess.Popen` 和管道 I/O；(3) asyncio 或 threading 基础，多服务器并发必须；(4) Phase 13·06 的 JSON-RPC 信封格式。

**Type:** Build | **类型:** 构建
**Languages:** Python (stdlib, multi-server MCP client) | **语言:** Python (stdlib, multi-server MCP client)
**Prerequisites:** Phase 13 · 07 (building an MCP server) | **前置知识:** Phase 13 · 07 (building an MCP server)
**Time:** ~75 minutes | **时间:** ~75 分钟

## Learning Objectives | 学习目标

- Spawn an MCP server as a child process, complete `initialize`, and send a `notifications/initialized`.
  中文翻译：将 MCP 服务器作为子进程生成，完成 `initialize`，并发送 `notifications/initialized`。
- Maintain per-server session state (capabilities, tool list, last-seen notification ids).
  中文翻译：维护每服务器会话状态（能力、工具列表、最近见过的通知 id）。
- Merge tool lists across multiple servers into one namespace with collision handling.
  中文翻译：跨多服务器合并工具列表到一个命名空间，并处理冲突。
- Route a tool call to the server that owns it and reassemble the response.
  中文翻译：将工具调用路由到拥有它的服务器并重组响应。

## The Problem | 问题引入

A real agent host (Claude Desktop, Cursor, Goose, Gemini CLI) loads multiple MCP servers at once. A user might have a filesystem server, a Postgres server, and a GitHub server running simultaneously. The client's job:

> 一个真正的 Agent 宿主（Claude Desktop、Cursor、Goose、Gemini CLI）同时加载多个 MCP 服务器。用户可能同时运行文件系统服务器、Postgres 服务器和 GitHub 服务器。客户端的工作：

1. Spawn each server.
  中文翻译：生成每个服务器。
2. Handshake each independently.
  中文翻译：独立与每个服务器握手。
3. Call `tools/list` on each and flatten the result.
  中文翻译：在每个服务器上调用 `tools/list` 并扁平化结果。
4. When the model emits `notes_search`, look it up in the merged namespace and route to the right server.
  中文翻译：当模型发出 `notes_search` 时，在合并命名空间中查找并路由到正确服务器。
5. Handle notifications from any server (`tools/list_changed`) without blocking.
  中文翻译：处理任何服务器的通知（`tools/list_changed`）而不阻塞。
6. Reconnect on transport failure.
  中文翻译：传输失败时重连。

Hand-rolling all of that is what separates "toy" from "serviceable". The official SDKs wrap this, but the mental model has to be yours.

> **【中文解读】** 真正的 Agent 宿主同时加载多个 MCP 服务器。客户端的工作：(1) 生成每个服务器；(2) 独立握手；(3) 在每个服务器上调用 `tools/list` 并扁平化结果；(4) 当模型发出 `notes_search` 时，在合并命名空间中查找并路由到正确服务器；(5) 处理任意服务器的通知而不阻塞；(6) 传输失败时重连。

> 💡 **【类比】** MCP 客户端像医院分诊台。病人（用户请求）进来后，分诊台要快速判断该往哪个科室（哪个 MCP 服务器）送——挂号的（filesystem server）、化验的（postgres server）、放射的（github server）。分诊台手里有一本"科室能力清单"（合并的工具列表），并能同时指挥多科室会诊（并发调用）。每个科室是独立子进程，分诊台要在它们之间高效路由，还要应对某个科室突然掉线（重连）。

## The Concept | 核心概念

### Child-process spawning

> **【中文解读】** 客户端用 `subprocess.Popen` 生成每个 MCP 服务器子进程，设置 `stdin=PIPE, stdout=PIPE, stderr=PIPE`，`bufsize=1` 并使用文本模式逐行读取。每个服务器是一个进程，客户端持有对应的 Popen 句柄。

`subprocess.Popen` with `stdin=PIPE, stdout=PIPE, stderr=PIPE`. Set `bufsize=1` and use text mode for line-by-line reads. Each server is one process; the client holds one `Popen` handle per server.

> `subprocess.Popen` 设置 `stdin=PIPE, stdout=PIPE, stderr=PIPE`。设置 `bufsize=1` 并使用文本模式逐行读取。每个服务器是一个进程；客户端为每个服务器持有一个 `Popen` 句柄。

### Per-server session state

A `Session` object per server holds:

> 每服务器的 `Session` 对象持有：

- `process` — the Popen handle.
  中文翻译：`process`——Popen 句柄。
- `capabilities` — what the server declared at `initialize`.
  中文翻译：`capabilities`——服务器在 `initialize` 中声明的能力。
- `tools` — the last `tools/list` result.
  中文翻译：`tools`——最近的 `tools/list` 结果。
- `pending` — map of request id to a promise/future waiting for the response.
  中文翻译：`pending`——请求 id 到等待响应的 promise/future 的映射。

Requests are async by nature; a `tools/call` sent to server A while server B is mid-call must not block. Either use threads with queues or asyncio.

> 请求天然是异步的；当服务器 B 正在执行调用时，发给服务器 A 的 `tools/call` 不应阻塞。使用带队列的线程或 asyncio。

> ⚠️ **【易错点】** 场景：单线程同步实现，循环读取每个服务器的 stdout / 后果：一个慢工具（如长 SQL）阻塞整个客户端，其他服务器即使响应快也无法处理 / 修复：每个服务器必须有独立的 reader 线程/任务，主循环只负责 dispatch；用 `selectors` 或 `asyncio` 监听多个 stdin，按到达顺序处理。stdout 写入也要加锁避免消息交错。

### Merged namespace

> **【拓展：多 MCP 服务器命名空间冲突处理】** 当多个服务器有同名工具时，客户端有三种处理策略：(1) 按服务器名前缀（`notes/search`、`files/search`），清晰但冗长——Claude Desktop 和 VS Code 用这种方式；(2) 先到先得，后加载的覆盖先加载的——风险高，隐藏冲突；(3) 碰撞拒绝，拒绝加载第二个服务器——Cursor 用这种方式，对安全敏感的宿主最安全。

When the client sees the aggregate tool list, names can collide. Two servers might both expose `search`. The client has three options:

> 当客户端看到聚合的工具列表时，名称可能冲突。两个服务器可能都暴露 `search`。客户端有三个选项：

1. **Prefix by server name.** `notes/search`, `files/search`. Clear but ugly.
  中文翻译：**按服务器名加前缀。** `notes/search`、`files/search`。清晰但难看。
2. **Silent first-come.** Later server's `search` overrides the earlier. Risky; hides collisions.
  中文翻译：**静默先到先得。** 后续服务器的 `search` 覆盖先到的。有风险；隐藏冲突。
3. **Collision rejection.** Refuse to load the second server; notify the user. Safest for security-sensitive hosts.
  中文翻译：**冲突拒绝。** 拒绝加载第二个服务器；通知用户。对安全敏感的宿主最安全。

Claude Desktop uses prefix-by-server. Cursor uses collision rejection with a clear error. VS Code MCP adopts prefix-by-server as well.

> Claude Desktop 使用按服务器加前缀。Cursor 使用带清晰错误的冲突拒绝。VS Code MCP 也采用按服务器加前缀。

> 🤔 **【困惑】** Q: 加了前缀（如 `notes/search`）后，模型会不会因为名字带斜号而选不准？ A: 实测影响很小，因为前缀本身有语义（"notes"是领域），模型反而更准。但要注意：(1) 不要混用——一会儿前缀一会儿不前缀会让模型困惑；(2) 描述里要呼应——`notes/search` 的描述里要写"在笔记中搜索"；(3) 测试时跑 StableToolBench 验证选择准确率，前缀通常带来 3-5% 提升。

### Routing

> **【中文解读】** 合并后，调度表将 `tool_name -> session` 映射起来。模型按名称发出调用，客户端找到对应 session 并向该服务器的 stdin 写入 `tools/call` 消息，然后等待响应。

After merging, a dispatch table maps `tool_name -> session`. The model emits a call by name; the client finds the session and writes a `tools/call` message to that server's stdin, then awaits the response.

> 合并后，调度表将 `tool_name -> session` 映射起来。模型按名发出调用；客户端找到 session 并向该服务器的 stdin 写入 `tools/call` 消息，然后等待响应。

### Sampling callback

If the server declared the `sampling` capability at `initialize`, it may send `sampling/createMessage` asking the client to run its LLM. The client must:

> 如果服务器在 `initialize` 中声明了 `sampling` 能力，它可以发送 `sampling/createMessage` 请求客户端运行其 LLM。客户端必须：

1. Block further requests to that server until the sample resolves, or pipeline if its implementation supports concurrency.
  中文翻译：在该样本完成前阻止对该服务器的进一步请求，或如实现支持并发则流水线处理。
2. Call its LLM provider.
  中文翻译：调用其 LLM 提供商。
3. Send the response back to the server.
  中文翻译：将响应发回服务器。

Lesson 11 covers sampling end-to-end. This lesson stubs it for completeness.

> Lesson 11 端到端讲解 sampling。本课为完整性做了简单实现。

### Notification handling

> **【中文解读】** `notifications/tools/list_changed` 意味着重新调用 `tools/list`。`notifications/resources/updated` 意味着重新读取正在使用的资源。通知不得产生响应。常见客户端 bug：在 `tools/call` 上阻塞读取循环，而通知排在流中。解决方案：使用后台读取线程将每条消息推入队列，主线程出队并分发。

`notifications/tools/list_changed` means re-call `tools/list`. `notifications/resources/updated` means re-read the resource if it is in use. Notifications must not produce responses — do not try to ack them.

> `notifications/tools/list_changed` 意味着重新调用 `tools/list`。`notifications/resources/updated` 意味着如果资源正在使用就重新读取。通知不得产生响应——不要尝试 ack 它们。

A common client bug: blocking the read loop on `tools/call` while a notification sits in the stream. Use a background reader thread that pushes every message onto a queue; the main thread dequeues and dispatches.

> 一个常见的客户端 bug：在 `tools/call` 上阻塞读取循环，而通知排在流中。使用后台读取线程将每条消息推入队列；主线程出队并分发。

### Reconnection

> **【拓展：MCP 传输失败与重连策略】** 传输可能因服务器崩溃、OS 杀进程或 stdio 管道断裂而失败。客户端检测 stdout 上的 EOF 并将会话标记为死亡。两种重连策略：(1) 静默重启服务器并重新握手——适合纯只读服务器；(2) 向用户报告失败——适合有状态和用户可见会话的服务器。Phase 13.09 覆盖 Streamable HTTP 重连语义。

Transport can fail: server crashed, OS killed the process, stdio pipe broke. The client detects EOF on stdout and treats the session as dead. Options:

> 传输可能失败：服务器崩溃、OS 杀进程、stdio 管道断裂。客户端检测到 stdout 上的 EOF 并将 session 视为死亡。选项：

- Silently restart the server and re-handshake. OK for pure read-only servers.
  中文翻译：静默重启服务器并重新握手。适合纯只读服务器。
- Surface the failure to the user. OK for stateful servers with user-visible sessions.
  中文翻译：将失败暴露给用户。适合有状态和用户可见会话的服务器。

Phase 13 · 09 covers the Streamable HTTP reconnection semantics; stdio is simpler.

> Phase 13 · 09 涵盖 Streamable HTTP 重连语义；stdio 更简单。

### Keepalive and session id

Streamable HTTP uses a `Mcp-Session-Id` header. Stdio has no session id — the process identity IS the session. Keepalive pings are optional; stdio pipes do not break under inactivity.

> Streamable HTTP 使用 `Mcp-Session-Id` 头。stdio 没有 session id——进程身份就是 session。保活 ping 是可选的；stdio 管道不会因不活动而断裂。

## Use It | 用框架实现

`code/main.py` spawns three simulated MCP servers as subprocesses, handshakes each, merges their tool lists, and routes tool calls to the right one. The "servers" are actually other Python processes running toy responders (no real LLM). Run it to see:

> `code/main.py` 将三个模拟的 MCP 服务器作为子进程生成，与每个握手，合并其工具列表，并将工具调用路由到正确的服务器。这些"服务器"实际上是运行玩具响应器的其他 Python 进程（无真实 LLM）。运行它可以看到：

- Three initializations, each with their own capability set.
  中文翻译：三次初始化，每次带自己的能力集合。
- Three `tools/list` results merged into a 7-tool namespace.
  中文翻译：三个 `tools/list` 结果合并为 7 个工具的命名空间。
- A routing decision based on the tool name.
  中文翻译：基于工具名的路由决策。
- A collision prevented by namespace prefixing.
  中文翻译：通过命名空间前缀防止的冲突。

What to look at:

- The `Session` dataclass holds per-server state cleanly.
  中文翻译：`Session` 数据类干净地保存每服务器状态。
- The background reader thread dequeues every line on stdout without blocking the main thread.
  中文翻译：后台读取线程从 stdout 出队每行而不阻塞主线程。
- The dispatch table is a simple `dict[str, Session]`.
  中文翻译：调度表是一个简单的 `dict[str, Session]`。
- Collision handling is explicit: when two servers declare the same name, the later one is renamed with a prefix.
  中文翻译：冲突处理是显式的：当两个服务器声明同名时，后者被重命名加前缀。

## Ship It | 产出物

This lesson produces `outputs/skill-mcp-client-harness.md`. Given a declarative list of MCP servers (name, command, args), the skill produces a harness that spawns them, merges tool lists, and ships a routing function with collision resolution.

> 本课产出 `outputs/skill-mcp-client-harness.md`。给定一个声明式 MCP 服务器列表（名称、命令、参数），该 skill 生成一个线束：生成它们、合并工具列表，并附带带冲突解决的路由函数。

## Exercises | 练习题

1. Run `code/main.py` and watch the server spawn log. Kill one of the simulated server processes with a SIGTERM and observe how the client detects the EOF and marks that session as dead.
   中文翻译：运行 `code/main.py` 并观察服务器生成日志。用 SIGTERM 杀死一个模拟服务器进程，观察客户端如何检测到 EOF 并将 session 标记为死亡。

2. Implement namespace prefixing. When two servers expose `search`, rename the second as `<server>/search`. Update the dispatch table and verify tool calls route correctly.
   中文翻译：实现命名空间前缀。当两个服务器暴露 `search` 时，将第二个重命名为 `<server>/search`。更新调度表并验证工具调用正确路由。

3. Add a connection-pool-style backoff for server restart: exponential backoff on consecutive failures, cap at 30 seconds, emit a notification to the user after three failures.
   中文翻译：添加连接池式的服务器重启退避：连续失败时指数退避，上限 30 秒，三次失败后向用户发出通知。

4. Sketch a client that supports 100 concurrent MCP servers. What data structure replaces the simple dispatch dict? (Hint: trie for prefix namespacing, plus a metric for tool-count-per-server.)
   中文翻译：勾勒支持 100 个并发 MCP 服务器的客户端。什么数据结构替代简单的调度字典？（提示：用于前缀命名空间的 trie，加每服务器工具数指标。）

5. Port the client to the official MCP Python SDK. The SDK wraps `stdio_client` and `ClientSession`. The code should shrink from ~200 lines to ~40 lines while preserving multi-server routing.
   中文翻译：将客户端迁移到官方 MCP Python SDK。SDK 包装了 `stdio_client` 和 `ClientSession`。代码应从约 200 行缩减到约 40 行，同时保留多服务器路由。

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
  中文翻译：权威客户端行为参考
- [MCP — Quickstart client guide](https://modelcontextprotocol.io/quickstart/client) — hello-world client tutorial with the Python SDK
  中文翻译：使用 Python SDK 的 hello-world 客户端教程
- [MCP Python SDK — client module](https://github.com/modelcontextprotocol/python-sdk) — reference `ClientSession` and `stdio_client`
  中文翻译：`ClientSession` 和 `stdio_client` 参考
- [MCP TypeScript SDK — Client](https://github.com/modelcontextprotocol/typescript-sdk) — TS parallel
  中文翻译：TypeScript 并行实现
- [VS Code — MCP in extensions](https://code.visualstudio.com/api/extension-guides/ai/mcp) — how VS Code multiplexes multiple MCP servers in a single editor host
  中文翻译：VS Code 如何在单个编辑器宿主中多路复用多个 MCP 服务器
