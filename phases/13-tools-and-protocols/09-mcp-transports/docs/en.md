# MCP Transports: stdio and Stateless Streamable HTTP | MCP 传输层：stdio 与无状态 Streamable HTTP

> Transport carries MCP messages. It does not supply missing protocol state. In `2026-07-28`, local stdio and remote Streamable HTTP both carry self-describing requests.

> **【中文解读】** 传输层只负责搬运 MCP 消息，不负责补齐协议状态。在 2026-07-28 规范中，本地 stdio 和远程 Streamable HTTP 传递的都是"自描述"请求——每个请求自带协议版本与客户端能力，不再依赖连接或会话保存上下文。

> **【拓展：传输层演进→2026-07-28 无状态化】** MCP 传输层三年三变：2024-11 的 HTTP+SSE 双端点、2025-03-26 的 Streamable HTTP（GET 流 + `Mcp-Session-Id` 会话）、再到 2026-07-28 的无状态 POST-only 契约。演进方向始终是"把状态从传输层赶出去"：会话头没了，改成请求体 `_meta` 携带版本与能力；独立 GET 流没了，改成 `subscriptions/listen` 请求级响应流。无状态让任意健康副本都能处理任意请求，是云原生横向扩展的关键。

> 🔗 **【前置】** 学本节前请先掌握：(1) Phase 13·07、08（MCP server 和 client）——理解 JSON-RPC 分发逻辑；(2) HTTP 协议基础（method、header、状态码）；(3) DNS 重绑定攻击概念——本节的 `Origin` 校验是防御手段；(4) 若你学过本课旧版（2025 传输：GET 流 + 会话头 + `Last-Event-ID` 重放），请先清空那套旧心智模型再往下读。

**Type:** Learn | **类型:** 学习
**Languages:** Python | **语言:** Python
**Prerequisites:** Phase 13, Lessons 07 and 08 | **前置知识:** Phase 13 · 07、08（MCP 服务器与客户端）
**Time:** ~65 minutes | **时间:** 约 65 分钟

## Learning Objectives | 学习目标

- Choose stdio for local child processes and Streamable HTTP for network services.
  中文翻译：本地子进程选 stdio，网络服务选 Streamable HTTP。
- Implement the modern single-endpoint, POST-only Streamable HTTP contract.
  中文翻译：实现现代的单端点、仅 POST 的 Streamable HTTP 契约。
- Mirror and validate MCP version, method, and name headers against the JSON-RPC body.
  中文翻译：把 MCP 版本、方法、名称镜像头与 JSON-RPC 请求体做比对校验。
- Deliver request-scoped SSE and long-lived `subscriptions/listen` streams correctly.
  中文翻译：正确交付请求级 SSE 流和长生命周期的 `subscriptions/listen` 流。
- Migrate session-based and legacy HTTP+SSE deployments without presenting legacy behavior as modern.
  中文翻译：迁移基于会话的部署和遗留 HTTP+SSE 部署，且不把遗留行为冒充为现代行为。

## The Problem | 问题引入

> **【中文解读】** 本节讲清"为什么要无状态"。早期 Streamable HTTP 把协议协商、连接行为、会话行为捆在一起——服务器可以铸造 `Mcp-Session-Id`、暴露独立 GET 流、接受 DELETE 终止会话、用 `Last-Event-ID` 恢复 SSE。2026-07-28 把这些机制全部从现代线格式中移除：每个请求都能落在任意健康 worker 上，因为协议版本和客户端能力随请求体传输；HTTP 头只做路由与策略镜像，服务器执行前会校验头与体是否一致。代价是：还在把 2025 传输当作现行规范教的服务器，教的是错误的失败模型和安全模型。

Earlier Streamable HTTP revisions combined protocol negotiation with connection and session behavior. A server could mint `Mcp-Session-Id`, expose a standalone GET stream, accept DELETE for session termination, and resume SSE with `Last-Event-ID`.

> 更早的 Streamable HTTP 修订版把协议协商与连接、会话行为捆在一起。服务器可以铸造 `Mcp-Session-Id`、暴露一个独立的 GET 流、接受 DELETE 来终止会话，并用 `Last-Event-ID` 恢复 SSE。

MCP `2026-07-28` removes those mechanisms from the modern wire. Every request can land on any healthy worker because its protocol version and client capabilities travel in the request body. HTTP headers mirror selected fields for routing and policy, but the server validates those headers against the body before execution.

> MCP `2026-07-28` 从现代线格式中移除了这些机制。每个请求都可以落在任意健康 worker 上，因为协议版本和客户端能力随请求体传输。HTTP 头为路由和策略镜像了部分字段，但服务器在执行前会把这些头与请求体比对校验。

The result is easier to scale and easier to reason about. It also means that a server teaching the 2025 transport as current is teaching the wrong failure and security model.

> 结果是更容易扩展、也更容易推理。这也意味着：把 2025 传输当作现行规范来教的服务器，教的是错误的失败模型和安全模型。

## The Concept | 核心概念

> 💡 **【类比】** 无状态传输像外卖平台的订单流转。旧模式（会话式传输）像"你只能等当初接单的那个骑手"——骑手下线（副本重启），订单就卡住。新模式（2026-07-28 无状态）像"任何站点都能接手你的订单"——每张订单（请求）都完整写明地址和备注（协议版本、能力），谁接手都能继续干活；贵重物品寄存（应用状态）不塞进骑手口袋（连接亲和性），而是给一张取件码（显式状态句柄）。

### stdio

The stdio binding is for a client-launched subprocess:

> stdio 绑定面向客户端启动的子进程：

- Client writes one UTF-8 JSON-RPC message per line to stdin.
  中文翻译：客户端向 stdin 每行写入一条 UTF-8 JSON-RPC 消息。
- Server writes one UTF-8 JSON-RPC message per line to stdout.
  中文翻译：服务器向 stdout 每行写入一条 UTF-8 JSON-RPC 消息。
- Server writes diagnostics to stderr.
  中文翻译：服务器把诊断信息写入 stderr。
- Server exits promptly on stdin EOF.
  中文翻译：stdin 出现 EOF 时服务器立即退出。
- Every modern request carries version and client capabilities in `params._meta`.
  中文翻译：每个现代请求都在 `params._meta` 中携带版本和客户端能力。

The process may live for many calls, but it is not a modern protocol session. If it exits unexpectedly, in-flight requests are lost. Restart the process, rediscover, relist, reopen subscriptions, and retry safe operations with new request ids.

> 进程可以存活多次调用，但它并不是现代意义上的协议会话。如果进程意外退出，进行中的请求会丢失。正确做法是：重启进程、重新发现、重新列清单、重新打开订阅，并用新的请求 id 重试安全的操作。

### Streamable HTTP in 2026-07-28

> **【中文解读】** 现代服务器只暴露一个接收 POST 的 MCP 端点（如 `/mcp`）。每条 JSON-RPC 请求或通知都是一次新的 HTTP POST，请求体只含一条消息；客户端不向服务器发送 JSON-RPC 响应。请求的应答有两种形态：`application/json`（单条 JSON-RPC 响应）或 `text/event-stream`（先推与该请求相关的通知，最后给最终响应）；通知被接受则返回无主体的 `202 Accepted`。客户端用 `Accept: application/json, text/event-stream` 同时声明两种响应类型。

A modern server exposes one MCP endpoint, such as `/mcp`, that accepts POST.

Every JSON-RPC request or notification is a new HTTP POST. The body contains one JSON-RPC message. Clients do not send JSON-RPC responses to the server.

> 现代服务器暴露一个接收 POST 的 MCP 端点，例如 `/mcp`。每条 JSON-RPC 请求或通知都是一次新的 HTTP POST。请求体包含一条 JSON-RPC 消息。客户端不向服务器发送 JSON-RPC 响应。

For a request, the server returns either:

- `Content-Type: application/json` with one JSON-RPC response; or
- `Content-Type: text/event-stream` with notifications related to that request, followed by the final JSON-RPC response.

For an accepted notification, the server returns `202 Accepted` with no body.

> 对于请求，服务器返回两种之一：`Content-Type: application/json` 带一条 JSON-RPC 响应，或 `Content-Type: text/event-stream` 先带与该请求相关的通知、再带最终 JSON-RPC 响应。对于被接受的通知，服务器返回不带主体的 `202 Accepted`。

Clients advertise both response types:

> 客户端同时声明接受两种响应类型：

```http
Accept: application/json, text/event-stream
```

### POST-only means POST-only

> ⚠️ **【易错点】** 场景：从旧版 Streamable HTTP 迁移来的服务端习惯性地实现 GET 流、DELETE 会话端点，或铸造/回显 `Mcp-Session-Id`、处理 `Last-Event-ID` / 后果：这些都不是 2026-07-28 行为——GET 和 DELETE 必须返回 `405`，会话头必须被忽略；请求级流在最终响应前中断即宣告该请求丢失，只能换新 id 重试，绝不能尝试流恢复 / 修复：对照规范逐条移除遗留端点与头处理逻辑，把"断流恢复"改成"新请求重试"。

Modern Streamable HTTP has no standalone GET stream and no DELETE session endpoint.

> 现代 Streamable HTTP 没有独立 GET 流，也没有 DELETE 会话端点。

- `GET /mcp` returns `405 Method Not Allowed`.
  中文翻译：`GET /mcp` 返回 `405 Method Not Allowed`。
- `DELETE /mcp` returns `405 Method Not Allowed`.
  中文翻译：`DELETE /mcp` 返回 `405 Method Not Allowed`。
- `Mcp-Session-Id` is ignored and never minted or echoed.
  中文翻译：`Mcp-Session-Id` 被忽略，从不铸造也从不回显。
- `Last-Event-ID` is ignored because modern streams are not resumable.
  中文翻译：`Last-Event-ID` 被忽略，因为现代流不可恢复。

If a request-scoped stream breaks before its final response, the client has lost that in-flight request. It may issue a new request with a new JSON-RPC id when retry is safe. It must not attempt stream resumption.

> 如果请求级流在最终响应前中断，客户端就失去了这个进行中的请求。它可以在重试安全时用一个新 JSON-RPC id 发起新请求。它绝不能尝试流恢复。

### Origin validation

> **【中文解读】** 服务器对进入连接做 `Origin` 校验以防 DNS 重绑定：头存在且不在白名单上就返回 `403 Forbidden`；非浏览器客户端可以不带 `Origin`（官方传输规则允许）。三条要点：(1) 本地服务器应绑定 `127.0.0.1` 而非所有网卡；(2) `Origin` 校验不是认证，网络服务仍需对每个请求做认证与授权；(3) 必须用规范化后的精确匹配——`origin.startswith("https://trusted.example")` 这类前缀检查不安全，会放行攻击者控制的后缀。

Servers validate `Origin` on incoming connections to prevent DNS rebinding. If the header is present and not explicitly allowed, return `403 Forbidden`. A non-browser client may omit `Origin`, which the official transport rules permit.

> 服务器在进入连接上校验 `Origin` 以防 DNS 重绑定。如果该头存在且未被显式允许，返回 `403 Forbidden`。非浏览器客户端可以省略 `Origin`，官方传输规则允许这一点。

Local servers should bind to `127.0.0.1`, not every interface. Network services still need authentication and authorization on every request. Origin validation is not authentication.

> 本地服务器应绑定 `127.0.0.1`，而不是所有网卡。网络服务仍然需要对每个请求做认证和授权。Origin 校验不是认证。

Use exact origin matching after canonical configuration. Prefix checks such as `origin.startswith("https://trusted.example")` are unsafe because they can accept attacker-controlled suffixes.

> 在规范化配置之后使用精确的 origin 匹配。`origin.startswith("https://trusted.example")` 这类前缀检查不安全，因为它们可能接受攻击者控制的后缀。

### Required HTTP metadata headers

> **【中文解读】** 每个现代 POST 都带三个镜像头：`MCP-Protocol-Version` 必须等于 `params._meta` 中的协议版本；`Mcp-Method` 必须等于 JSON-RPC `method`；`tools/call`、`resources/read`、`prompts/get` 必带 `Mcp-Name`（等于 `params.name`，`resources/read` 时等于 `params.uri`）。头值大小写敏感。不安全或非 ASCII 的 `Mcp-Name` 用 `=?base64?{...}?=` 哨兵编码，服务器解码后再与请求体比对。缺失/畸形/不匹配 → HTTP `400` + JSON-RPC `-32020`；版本不支持 → HTTP `400` + `-32022` 并带精确的 `supported`/`requested` 数据；未知现代方法 → HTTP `404` + `-32601`（JSON-RPC 体很重要，双时代客户端靠它区分现代错误和遗留端点未命中）。

Every modern POST request includes:

```http
MCP-Protocol-Version: 2026-07-28
Mcp-Method: tools/call
Mcp-Name: notes_search
```

Header rules:

> 头规则：

- `MCP-Protocol-Version` is required and must equal `params._meta.io.modelcontextprotocol/protocolVersion`.
  中文翻译：`MCP-Protocol-Version` 必填，且必须等于 `params._meta.io.modelcontextprotocol/protocolVersion`。
- `Mcp-Method` is required and must equal the JSON-RPC `method`.
  中文翻译：`Mcp-Method` 必填，且必须等于 JSON-RPC `method`。
- `Mcp-Name` is required for `tools/call`, `resources/read`, and `prompts/get`.
  中文翻译：`tools/call`、`resources/read`、`prompts/get` 必带 `Mcp-Name`。
- `Mcp-Name` equals `params.name`, or `params.uri` for `resources/read`.
  中文翻译：`Mcp-Name` 等于 `params.name`；对 `resources/read` 则等于 `params.uri`。
- Header values are case-sensitive even though header names are case-insensitive.
  中文翻译：头值大小写敏感，尽管头名大小写不敏感。

Unsafe or non-ASCII `Mcp-Name` values use the exact UTF-8 Base64 sentinel:

```text
=?base64?{Base64EncodedValue}?=
```

The server decodes that value before comparing it with the body.

> 不安全或非 ASCII 的 `Mcp-Name` 值使用精确的 UTF-8 Base64 哨兵格式（如上）。服务器先解码该值再与请求体比对。

Missing, malformed, or mismatched mirrored headers return HTTP `400` with JSON-RPC code `-32020`. If header and body agree on a version the server does not support, return HTTP `400` with `-32022` and exact error data such as `{"supported":["2026-07-28"],"requested":"2027-01-01"}`.

> 镜像头缺失、畸形或不匹配时返回 HTTP `400` 和 JSON-RPC 错误码 `-32020`。如果头与请求体一致地指向一个服务器不支持的版本，返回 HTTP `400` 和 `-32022`，并带精确的错误数据，例如 `{"supported":["2026-07-28"],"requested":"2027-01-01"}`。

An unknown modern method returns HTTP `404` with JSON-RPC `-32601`. The JSON-RPC body is important because a dual-era client uses it to distinguish a modern error from a legacy endpoint miss.

> 未知的现代方法返回 HTTP `404` 和 JSON-RPC `-32601`。JSON-RPC 响应体很重要，因为双时代客户端靠它区分"现代错误"与"遗留端点未命中"。

### Request-scoped SSE

> **【中文解读】** 服务器可以为单个长运行请求选择 SSE 作为响应载体：POST 发出 `tools/call`，响应流上依次推送与该请求 id 相关的进度通知，最后给出最终 JSON-RPC 响应，流随即关闭。约束有三条：(1) 服务器不得在这条流上发送独立的 JSON-RPC 请求——sampling、elicitation、roots 交互都改走 Multi Round-Trip Request 结果；(2) 关闭响应流即取消该请求；(3) 不要为重放添加 SSE 事件 id——`Last-Event-ID` 恢复不属于现代修订。

A server may choose SSE for one long-running request:

```text
POST tools/call id=41
  <- notifications/progress related to id=41
  <- notifications/progress related to id=41
  <- JSON-RPC response id=41
stream closes
```

The server must not send independent JSON-RPC requests on this stream. Sampling, elicitation, and roots interactions use Multi Round-Trip Request results. Closing the response stream cancels that request.

> 服务器不得在这条流上发送独立的 JSON-RPC 请求。Sampling、elicitation 和 roots 交互使用 Multi Round-Trip Request（MRTR）结果。关闭响应流即取消该请求。

Do not add SSE event ids for replay. `Last-Event-ID` resumption is not part of the modern revision.

> 不要为重放添加 SSE 事件 id。`Last-Event-ID` 恢复不属于现代修订。

### Long-lived changes use subscriptions/listen

> **【中文解读】** 变更通知不再走独立 GET，而是客户端主动发起 `subscriptions/listen` 请求：POST 的响应保持打开，成为一条长生命周期 SSE 流。`notifications` 对象是允许清单——服务器不得投递未被请求的通知类型。流上第一条协议消息是 `notifications/subscriptions/acknowledged`；确认、每条变更通知和最终结果都在 `_meta` 中携带等于 listen 请求 id 的 `subscriptionId`。服务器可用 SSE 注释做保活。流断开后，客户端换新请求 id 重新 listen 并重新拉取受影响的数据。`resources/subscribe` 和 `resources/unsubscribe` 属于遗留时代，禁止在现代连接上使用。

Change notifications use a client-opened request, not standalone GET:

```json
{
  "jsonrpc": "2.0",
  "id": "listen-1",
  "method": "subscriptions/listen",
  "params": {
    "notifications": {
      "toolsListChanged": true,
      "resourceSubscriptions": ["notes://note-1"]
    },
    "_meta": {
      "io.modelcontextprotocol/protocolVersion": "2026-07-28",
      "io.modelcontextprotocol/clientCapabilities": {},
      "io.modelcontextprotocol/clientInfo": {
        "name": "course-client",
        "version": "1.0.0"
      }
    }
  }
}
```

The POST response is a long-lived SSE stream. Its first protocol message is `notifications/subscriptions/acknowledged`. The acknowledgement, every change notification, and the final result carry `io.modelcontextprotocol/subscriptionId` in `_meta`, equal to the listen request id. The server may emit SSE comments as keepalives. When the stream drops, the client reissues `subscriptions/listen` with a new request id and refetches affected data.

> POST 的响应是一条长生命周期 SSE 流。它的第一条协议消息是 `notifications/subscriptions/acknowledged`。确认消息、每条变更通知和最终结果都在 `_meta` 中携带 `io.modelcontextprotocol/subscriptionId`，其值等于 listen 请求的 id。服务器可以用 SSE 注释作为保活。当流断开时，客户端用新的请求 id 重新发出 `subscriptions/listen` 并重新拉取受影响的数据。

`resources/subscribe` and `resources/unsubscribe` belong to the legacy era. Do not use them on a modern connection.

> `resources/subscribe` 和 `resources/unsubscribe` 属于遗留时代。不要在现代连接上使用它们。

### Explicit application state

> **【中文解读】** 移除协议会话不等于禁止有状态的工作流。服务器可以铸造一个不透明的状态句柄，作为普通工具结果返回；客户端在后续调用中把它作为显式参数传回。句柄要绑定到已认证主体、不可猜测、可过期、每次使用都过授权——这让状态在应用层可见，而不是藏进传输亲和性。隐式副本状态的失败是机械性的五步：请求 A 在副本 1 内存里创建草稿却不返回句柄，请求 B 落到副本 2 就无法命名或加载草稿，粘性路由看似修复了症状，直到重启、发布、重调度或故障转移把它打破。正确边界是两部分：协议上下文留在每个请求里；持久应用状态放进共享存储、由服务器铸造句柄返回给客户端。按生命周期选机制——单次调用用请求局部变量；短 MRTR 延续用带完整性保护的 `requestState`；草稿或持久任务用显式句柄 + 共享持久化 + 过期 + 并发控制 + 幂等。这些都不是 MCP 协议会话。

Removing protocol sessions does not forbid workflows with state. The server may mint an opaque state handle and return it as a normal tool result. The client passes that handle as an explicit argument on later calls.

> 移除协议会话并不禁止带状态的工作流。服务器可以铸造一个不透明的状态句柄，并作为普通工具结果返回。客户端在后续调用中把这个句柄作为显式参数传入。

Bind handles to the authenticated principal, make them unguessable, expire them, and authorize every use. This makes state visible at the application layer instead of hiding it in transport affinity.

> 把句柄绑定到已认证主体，使其不可猜测、可过期，并对每次使用做授权。这让状态在应用层可见，而不是藏在传输亲和性里。

The failure caused by hidden replica state is mechanical:

> 由隐藏的副本状态导致的失败是机械性的：

1. Request A reaches replica 1 and creates a draft in that process's memory.
  中文翻译：请求 A 到达副本 1，在该进程内存中创建草稿。
2. The response does not return a draft handle because the implementation assumes the connection identifies the draft.
  中文翻译：响应不返回草稿句柄，因为实现假设"连接"能标识草稿。
3. Request B is a fresh POST and reaches replica 2.
  中文翻译：请求 B 是一次全新的 POST，到达副本 2。
4. Replica 2 has valid protocol metadata but no way to name or load the draft, so the workflow fails or reads the wrong local object.
  中文翻译：副本 2 持有合法的协议元数据，却无法命名或加载草稿，于是工作流失败或读到错误的本地对象。
5. Sticky routing appears to fix the symptom until a restart, rollout, reschedule, or failover moves the next request.
  中文翻译：粘性路由看似修复了症状，直到某次重启、发布、重调度或故障转移挪走了下一个请求。

The correct boundary has two parts. Protocol context stays in each request. Durable application state lives in a shared store under a server-minted handle returned to the client. The next call supplies that handle, any replica loads the same record, and authorization binds the record to the authenticated principal and tenant. Replica memory may cache a record, but it cannot be the only copy required for correctness.

> 正确的边界有两部分。协议上下文留在每个请求里。持久的应用状态存放在共享存储中，由服务器铸造句柄返回给客户端。下一次调用提供该句柄，任意副本都能加载同一条记录，授权把记录绑定到已认证主体和租户。副本内存可以缓存记录，但不能成为正确性所依赖的唯一副本。

Choose the state mechanism by lifetime. Request-local variables can serve one call. A short MRTR continuation can use integrity-protected `requestState`. A draft or durable task needs an explicit handle plus shared persistence, expiry, concurrency control, and idempotency. None of those objects is an MCP protocol session.

> 按生命周期选择状态机制。请求局部变量可以服务单次调用。短的 MRTR 延续可以使用带完整性保护的 `requestState`。草稿或持久任务需要显式句柄，外加共享持久化、过期、并发控制和幂等性。这些对象没有一个是 MCP 协议会话。

### HTTP dual-era compatibility

> **【中文解读】** 双时代客户端先尝试现代 POST；收到 HTTP `400`/`404`/`405` 就检查响应体：识别出的现代 JSON-RPC 错误证明服务器是现代的——修正请求或重试一个已公告的版本，绝不降级；空体或无法识别的响应才可能是遗留 HTTP+SSE 服务器，此时才去试旧 GET 端点并期待它的遗留 `endpoint` 事件。迁移期的服务器可以把现代元数据路由到现代 POST-only 实现、为老客户端保留独立的遗留端点，但绝不能把遗留的 GET、DELETE、会话 id 或重放行为描述为 `2026-07-28` 的一部分。

A client that supports modern and legacy servers attempts a modern POST first. If it receives HTTP `400`, `404`, or `405`, it inspects the body:

> 同时支持现代和遗留服务器的客户端先尝试现代 POST。如果收到 HTTP `400`、`404` 或 `405`，就检查响应体：

- A recognized modern JSON-RPC error proves the server is modern. Correct the request or retry an advertised version. Do not downgrade.
  中文翻译：识别出的现代 JSON-RPC 错误证明服务器是现代的。修正请求或重试一个已公告的版本。绝不降级。
- An empty body or an unrecognized response may indicate a legacy HTTP+SSE server. Only then try the old GET endpoint and expect its legacy `endpoint` event.
  中文翻译：空体或无法识别的响应可能表明这是遗留 HTTP+SSE 服务器。只有此时才去尝试旧的 GET 端点并期待它的遗留 `endpoint` 事件。

A server can support both eras during migration by routing modern metadata to the modern POST-only implementation and retaining separate legacy endpoints for old clients. Never describe the legacy GET, DELETE, session id, or replay behavior as part of `2026-07-28`.

> 服务器在迁移期可以同时支持两个时代：把现代元数据路由到现代 POST-only 实现，为老客户端保留独立的遗留端点。绝不要把遗留的 GET、DELETE、会话 id 或重放行为描述为 `2026-07-28` 的一部分。

```figure
tp-transport-handshake
```

## Use It | 用框架实现

> **【中文解读】** `code/main.py` 用 Python 标准库实现了一个有限、现代的 Streamable HTTP 服务器：校验 `Origin` 和镜像头、忽略已移除的会话头、普通调用返回 JSON，并演示一条有限的 `subscriptions/listen` SSE 流。自检（`--probe`）逐项验证：非法 `Origin` 被拒、无会话 id 也能完成发现、`Mcp-Session-Id` 和 `Last-Event-ID` 被忽略、头不匹配返回 `-32020`、不支持的版本返回 `-32022` 且带精确数据、无 id 通知被接受时返回无主体 `202`、GET 和 DELETE 返回 `405`、listen 流的确认/通知/最终结果都携带订阅 id。

`code/main.py` implements a finite, modern Streamable HTTP server with the Python standard library. It validates Origin and mirrored headers, ignores removed session headers, returns JSON for normal calls, and demonstrates a finite `subscriptions/listen` SSE stream.

> `code/main.py` 用 Python 标准库实现了一个有限、现代的 Streamable HTTP 服务器。它校验 Origin 和镜像头，忽略已移除的会话头，普通调用返回 JSON，并演示一条有限的 `subscriptions/listen` SSE 流。

```bash
cd code
python3 main.py --probe
python3 -m unittest discover tests -v
```

The probe checks:

- invalid Origin is rejected;
  中文翻译：非法 Origin 被拒绝；
- discovery succeeds without a session id;
  中文翻译：无需会话 id 即可完成发现；
- `Mcp-Session-Id` and `Last-Event-ID` are ignored;
  中文翻译：`Mcp-Session-Id` 和 `Last-Event-ID` 被忽略；
- header mismatch returns `-32020`;
  中文翻译：头不匹配返回 `-32020`；
- unsupported version returns `-32022` with exact `supported` and `requested` data;
  中文翻译：不支持的版本返回 `-32022` 并带精确的 `supported` 和 `requested` 数据；
- an accepted id-less notification returns HTTP `202` with no body;
  中文翻译：被接受的无 id 通知返回 HTTP `202` 且无主体；
- GET and DELETE return `405`;
  中文翻译：GET 和 DELETE 返回 `405`；
- `subscriptions/listen` is a POST response stream whose acknowledgement, notifications, and final result carry its subscription id.
  中文翻译：`subscriptions/listen` 是一条 POST 响应流，其确认、通知和最终结果都携带订阅 id。

## Ship It | 产出物

This lesson ships `outputs/skill-mcp-transport-migrator.md`. It removes modern protocol sessions, adds header-body validation, replaces standalone GET with `subscriptions/listen`, and keeps any legacy bridge visibly separate.

> 本课产出 `outputs/skill-mcp-transport-migrator.md`。它移除现代协议会话、加入头-体校验、用 `subscriptions/listen` 取代独立 GET，并让任何遗留桥接保持显眼隔离。

## Exercises | 练习题

1. Remove `Mcp-Method` from a POST. Confirm HTTP `400` and error `-32020`.
   中文翻译：从 POST 中移除 `Mcp-Method`。确认 HTTP `400` 和错误 `-32020`。
2. Send matching header and body version `2027-01-01`. Confirm HTTP `400`, error `-32022`, and exact data `{"supported":["2026-07-28"],"requested":"2027-01-01"}`.
   中文翻译：发送头与体一致的版本 `2027-01-01`。确认 HTTP `400`、错误 `-32022` 和精确数据 `{"supported":["2026-07-28"],"requested":"2027-01-01"}`。
3. Send a Base64 sentinel `Mcp-Name` for a non-ASCII resource URI. Confirm the decoded value is compared with `params.uri`.
   中文翻译：为非 ASCII 资源 URI 发送 Base64 哨兵 `Mcp-Name`。确认解码后的值与 `params.uri` 比对。
4. Break the finite listen stream before its final response. Reissue it with a new JSON-RPC id and refetch tools.
   中文翻译：在最终响应前打断有限的 listen 流。用新 JSON-RPC id 重新发出并重新拉取工具。
5. Add an explicit workflow handle to the ping tool. Bind it to an authorization subject without using connection affinity.
   中文翻译：给 ping 工具加一个显式工作流句柄。不用连接亲和性，把它绑定到一个授权主体。

## Key Terms | 术语速查表

| Term | Meaning | 中文术语 |
|------|---------|----------|
| stdio | Newline-delimited JSON-RPC over a client-launched subprocess | stdio 传输 |
| Streamable HTTP | Single endpoint where each modern message is a new POST | Streamable HTTP 传输 |
| Request-scoped SSE | POST response stream containing related notifications and final response | 请求级 SSE 流 |
| `subscriptions/listen` | Long-lived POST request for opted-in change notifications | 订阅监听请求 |
| Header mismatch | HTTP `400` and JSON-RPC `-32020` when mirrored headers disagree with body | 头不匹配错误 |
| Origin validation | DNS-rebinding defense for incoming connections, not authentication | Origin 校验（防 DNS 重绑定） |
| Explicit state handle | Application token passed as an ordinary argument instead of hidden session state | 显式状态句柄 |
| Legacy bridge | Separate earlier-era behavior kept only for compatibility | 遗留桥接 |

## Further Reading | 延伸阅读

- [MCP Transport Overview](https://modelcontextprotocol.io/specification/2026-07-28/basic/transports)
  中文翻译：MCP 传输总览——两种现代传输的权威入口
- [MCP stdio Transport](https://modelcontextprotocol.io/specification/2026-07-28/basic/transports/stdio)
  中文翻译：stdio 传输的完整规范
- [MCP Streamable HTTP](https://modelcontextprotocol.io/specification/2026-07-28/basic/transports/streamable-http)
  中文翻译：Streamable HTTP 的 POST-only 契约细节
- [MCP Subscriptions](https://modelcontextprotocol.io/specification/2026-07-28/basic/patterns/subscriptions)
  中文翻译：`subscriptions/listen` 订阅模式规范
- [MCP 2026-07-28 Changelog](https://modelcontextprotocol.io/specification/2026-07-28/changelog)
  中文翻译：2026-07-28 修订的完整变更清单（会话移除的官方说明）
