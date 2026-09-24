# MCP Fundamentals: Stateless Requests and JSON-RPC | MCP 基础：无状态请求与 JSON-RPC

> Modern MCP has no handshake and no protocol session. Each request must carry enough metadata to be understood, authorized, routed, and retried on its own.

> **【中文解读】** 现代 MCP 没有握手，也没有协议会话。每个请求必须自带足够的元数据，才能被独立地理解、授权、路由和重试。这是 2026-07-28 规范相对旧版（2025-11-25 及更早的 initialize 握手模型）最根本的范式转变：协议核心从"连接级状态"变成"请求级自描述"。

> **【拓展：MCP→协议演进时间线】** MCP 由 Anthropic 于 2024 年 11 月首发，现由 Linux 基金会下的 Agentic AI Foundation 管理。旧版（到 2025-11-25 为止）是"连接 → initialize 握手 → 操作"的三阶段生命周期模型；2026-07-28 版把协议核心改为无状态：每个请求在 `params._meta` 里自带协议版本、客户端能力与身份，`initialize` 降级为旧版兼容路径。本课是这个 MCP 系列的地基，后续 07（服务器）、08（客户端）都基于这个无状态模型。

> 🔗 **【前置】** 学本节前请先掌握：(1) Phase 13 · 01-05——工具接口、函数调用、Schema 设计；(2) JSON-RPC 2.0 基础（request/response/notification 三种信封）；(3) 对旧版 MCP 的 initialize 握手有整体认识（本课会解释它为何被废弃为兼容分支）。本课只讲基础协议；扩展机制在后续课程展开。

**Type:** Learn | **类型:** 学习
**Languages:** Python | **语言:** Python
**Prerequisites:** Phase 13, Lessons 01 through 05 | **前置知识:** Phase 13, Lessons 01 through 05
**Time:** ~55 minutes | **时间:** ~55 分钟

## Learning Objectives | 学习目标

- Distinguish MCP's server primitives from its client-side features.
  中文翻译：区分 MCP 的服务器原语与客户端特性。
- Build valid JSON-RPC 2.0 requests and responses for MCP `2026-07-28`.
  中文翻译：为 MCP `2026-07-28` 构建合法的 JSON-RPC 2.0 请求与响应。
- Attach protocol version, client capabilities, and client identity to every request.
  中文翻译：为每个请求附加协议版本、客户端能力和客户端身份。
- Use `server/discover` and handle `UnsupportedProtocolVersionError` without a handshake.
  中文翻译：在无握手的前提下使用 `server/discover` 并处理 `UnsupportedProtocolVersionError`。
- Trace one independent request from validation through a complete result.
  中文翻译：追踪一个独立请求从校验到完整结果的全程。

## The Problem | 问题引入

An MCP server can receive two consecutive requests from different clients, with different capabilities, on the same process or HTTP worker. If the server remembers what the previous request declared, it can apply the wrong permissions or return the wrong wire shape.

> 一个 MCP 服务器可能在同一个进程或 HTTP worker 上先后收到来自不同客户端、带着不同能力的两个请求。如果服务器记住了上一个请求声明过什么，就可能套用错误的权限，或返回错误的线格式。

MCP `2026-07-28` removes that ambiguity. The protocol core is stateless. A server must decide how to handle the current request from the current request, not from connection history.

> MCP `2026-07-28` 消除了这种歧义。协议核心是无状态的。服务器必须只依据"当前这个请求"本身来决定如何处理它，而不是依据连接历史。

This changes the mental model. The old sequence was connection first, handshake second, operations third. The modern sequence is simpler:

> 这改变了心智模型。旧版的顺序是：先建连接、再握手、后操作。现代的顺序更简单：

1. The client sends a self-describing request.
   中文翻译：客户端发送一个自描述的请求。
2. The server validates that request's version and capabilities.
   中文翻译：服务器校验该请求自带的版本与能力。
3. The server handles the method.
   中文翻译：服务器处理这个方法。
4. The server returns a typed result or a JSON-RPC error.
   中文翻译：服务器返回一个类型化结果或一个 JSON-RPC 错误。

The next request repeats the same process from scratch.

> 下一个请求从头重复同样的流程。

> **【中文解读】** 旧模型的隐患在于"服务器记忆"：同一进程先后服务多个客户端时，上一个请求声明的 capabilities 会污染下一个请求的处理。新规范要求每个请求自描述（版本、能力、身份都写在 `params._meta` 里），服务器处理完即忘。这既适配无共享的多 worker 部署，也让重试和幂等变得简单——任何副本都能独立处理任何请求。

> 💡 **【类比】** 旧版 MCP 像银行柜员办理业务：先取号（建连接）、再出示身份证登记（initialize 握手）、之后每笔业务都默认"还是你这个号"。新版 MCP 像微信扫码支付：每笔支付请求都自带完整凭证（订单号、金额、身份），任何一台收银机、任何一个班次都能独立核销，不需要"记住你是谁"。收银机换班（进程重启、换 worker）对业务零影响。

## The Concept | 核心概念

### Server primitives

> **【中文解读】** 服务器原语仍是三个：Tools（模型可调用的动作）、Resources（按 URI 寻址的数据）、Prompts（可复用模板）。注意新版的重大变化：roots/sampling/logging 这三个旧客户端原语在 2026-07-28 schema 中虽保留但已废弃；elicitation 改走"多轮往返请求"（服务器返回 input_required，客户端补齐输入后重试）。现代服务器不再主动发起任何独立 JSON-RPC 请求。

MCP servers expose three primary primitives:

1. **Tools** are model-controlled actions, discovered with `tools/list` and invoked with `tools/call`.
   中文翻译：**Tools** 是由模型控制的动作，用 `tools/list` 发现、用 `tools/call` 调用。
2. **Resources** are URI-addressed data, discovered with `resources/list` and retrieved with `resources/read`.
   中文翻译：**Resources** 是按 URI 寻址的数据，用 `resources/list` 发现、用 `resources/read` 读取。
3. **Prompts** are reusable templates, discovered with `prompts/list` and rendered with `prompts/get`.
   中文翻译：**Prompts** 是可复用模板，用 `prompts/list` 发现、用 `prompts/get` 渲染。

Roots, sampling, and logging remain in the `2026-07-28` schema for compatibility, but they are deprecated. New implementations should use explicit tool or resource inputs for roots, direct model-provider APIs for sampling, and stderr or OpenTelemetry for logging. Elicitation remains available through Multi Round-Trip Requests, where a server returns an input request and the client retries the original operation. A modern server never starts an independent JSON-RPC request.

> roots、sampling 和 logging 在 `2026-07-28` schema 中为兼容而保留，但已被废弃。新实现应当：roots 用显式的工具或资源输入替代；sampling 直接调用模型提供商 API；logging 用 stderr 或 OpenTelemetry。elicitation 仍可通过"多轮往返请求"（Multi Round-Trip Requests）使用——服务器返回一个输入请求，客户端补齐后重试原操作。现代服务器绝不主动发起独立的 JSON-RPC 请求。

> 🤔 **【困惑】** Q: 旧版引以为傲的 sampling（服务器借用客户端模型）怎么说废弃就废弃？ A: 实践中它把"谁付 token 费、用哪个模型"的决策权搅浑了，而且要求服务器能反向调用客户端，使网关、鉴权和缓存都变复杂。新规范把边界划清：服务器需要模型能力就返回 `input_required`，由客户端补齐输入后重试——控制流始终从客户端发起。理解这段"原语兴衰史"比背六个原语更重要：协议词表会变，"请求自描述 + 服务器不主动发起"这两个不变式才是核心。

### JSON-RPC envelopes

MCP uses JSON-RPC 2.0:

- Request: `{jsonrpc, id, method, params}`
  中文翻译：请求：`{jsonrpc, id, method, params}`。
- Response: `{jsonrpc, id, result}` or `{jsonrpc, id, error}`
  中文翻译：响应：`{jsonrpc, id, result}` 或 `{jsonrpc, id, error}`。
- Notification: `{jsonrpc, method, params}` with no `id`
  中文翻译：通知：`{jsonrpc, method, params}`，没有 `id`。

The request `id` correlates one response. It does not create a protocol session.

> 请求 `id` 只用于关联一个响应。它不创建协议会话。

### Required request metadata

Every modern request carries a `_meta` object inside `params`:

> 每个现代请求都在 `params` 内携带一个 `_meta` 对象：

```json
{
  "jsonrpc": "2.0",
  "id": 7,
  "method": "tools/list",
  "params": {
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

The protocol version and client capabilities are required. Client identity is recommended. It is self-reported display and debugging data, not a security credential.

> 协议版本和客户端能力是必填的。客户端身份是建议提供的。它是自报的展示与调试数据，不是安全凭证。

The server must not infer any of these values from an earlier request, a stdio process, an HTTP connection, or a transport header alone.

> 服务器不得从更早的请求、stdio 进程、HTTP 连接或单个传输层头部推断这些值。

> ⚠️ **【易错点】** 场景：从旧版迁移过来的实现只在第一条请求里带 `_meta`，后续请求"省略"以图省事 / 后果：服务器按规范必须拒绝（缺元数据即 `-32602`），且不同 worker 可能给出不一致行为；另一种坑是只依赖 HTTP 头里的版本号而不校验 body——规范要求边界处比对头部与 body，不一致返回 `-32020` / 修复：用统一的请求构造函数为每条请求盖全 `_meta` 三件套（版本、能力、身份），并在发送前检查序列化后的最终报文。

### Complete results and server identity

Every successful modern result includes `resultType`. A normal final result uses `"complete"`. Servers should also identify themselves in result metadata:

> 每个成功的现代结果都包含 `resultType`。普通最终结果用 `"complete"`。服务器还应在结果元数据中标识自己：

```json
{
  "jsonrpc": "2.0",
  "id": 7,
  "result": {
    "resultType": "complete",
    "tools": [],
    "ttlMs": 30000,
    "cacheScope": "public",
    "_meta": {
      "io.modelcontextprotocol/serverInfo": {
        "name": "notes-server",
        "version": "1.0.0"
      }
    }
  }
}
```

`tools/list`, `resources/list`, `prompts/list`, `resources/templates/list`, `resources/read`, and `server/discover` are cacheable results. They include `ttlMs` and `cacheScope`. A safe default is `ttlMs: 0` and `cacheScope: "private"`. List items should have deterministic ordering so equivalent responses produce stable cache keys and stable model context.

> `tools/list`、`resources/list`、`prompts/list`、`resources/templates/list`、`resources/read` 和 `server/discover` 是可缓存结果，它们包含 `ttlMs` 和 `cacheScope`。安全默认值是 `ttlMs: 0` 加 `cacheScope: "private"`。列表项应有确定性排序，这样等价的响应才能产生稳定的缓存键和稳定的模型上下文。

### Discovery without a handshake

> **【中文解读】** `server/discover` 取代了旧版 initialize 握手的"探路"角色：客户端可以先用它拿到服务器支持的版本集合、能力、使用说明和身份。但它是便利而非闸门——因为每个请求本来就自带版本与能力，客户端跳过 discover 直接发 `tools/list` 也完全合法。版本不匹配时返回 `-32022`，data 里带上 requested 与 supported，客户端换一个双方都支持的版本重试即可。

Every modern server must implement `server/discover`. The client may call it before another method to retrieve:

- `supportedVersions`
  中文翻译：`supportedVersions`（支持的版本集合）
- server `capabilities`
  中文翻译：服务器 `capabilities`（能力）
- optional usage `instructions`
  中文翻译：可选的使用 `instructions`（说明）
- server identity in result `_meta`
  中文翻译：结果 `_meta` 中的服务器身份
- cache hints
  中文翻译：缓存提示

Discovery is useful, but it is not a gate. A client can send `tools/list` first because that request already carries its protocol version and capabilities.

> 发现很有用，但它不是闸门。客户端可以先发 `tools/list`，因为那个请求本来就携带了自己的协议版本和能力。

If the requested version is unsupported, the server returns JSON-RPC code `-32022` with:

> 如果请求的版本不受支持，服务器返回 JSON-RPC 错误码 `-32022`，附带：

```json
{
  "requested": "2027-01-01",
  "supported": ["2026-07-28"]
}
```

The client selects a mutually supported modern version and retries with a new JSON-RPC request id.

> 客户端选定一个双方都支持的现代版本，用一个新的 JSON-RPC 请求 id 重试。

### One request lifecycle

Trace a modern request in this order:

> 按以下顺序追踪一个现代请求：

1. Parse one JSON-RPC envelope.
   中文翻译：解析一个 JSON-RPC 信封。
2. Confirm `jsonrpc` is `"2.0"`, an `id` exists, `method` is a string, and `params` is an object.
   中文翻译：确认 `jsonrpc` 是 `"2.0"`、存在 `id`、`method` 是字符串、`params` 是对象。
3. Require the version string and capability object in `params._meta`; malformed or missing metadata is `-32602`.
   中文翻译：要求 `params._meta` 中有版本字符串和能力对象；元数据畸形或缺失返回 `-32602`。
4. At an HTTP boundary, compare the version, method, and applicable name headers with the body. A mismatch is `-32020` even when one of the two version values is unsupported.
   中文翻译：在 HTTP 边界处比对版本、方法和适用的名称头部与 body。不一致返回 `-32020`——即使两个版本值中有一个本身就不受支持。
5. After equality is established, reject a matched but unsupported version with `-32022`.
   中文翻译：确认一致之后，再拒绝"一致但不受支持"的版本，返回 `-32022`。
6. Check required capabilities, then route by `method` and validate method-specific arguments.
   中文翻译：检查必需能力，然后按 `method` 路由并校验方法级参数。
7. Authenticate and authorize the concrete operation before its handler runs.
   中文翻译：在 handler 运行之前对具体操作做认证与授权。
8. Return a complete result with server identity.
   中文翻译：返回带服务器身份的完整结果。
9. Forget request-scoped protocol metadata.
   中文翻译：忘掉请求级的协议元数据。

> **【中文解读】** 这个顺序本身就是安全设计：先验证信封、再验证元数据、再比对头部与 body（防"头说 notes.read、body 却是 notes.delete"的走私）、然后才授权和执行。每一步的失败都有独立的错误码（-32600/-32602/-32020/-32022/-32001 等），排查时能精确定位是哪一层出了问题，而不是拿到一锅粥的"400 Bad Request"。

That order prevents two components from interpreting different calls. A gateway must not authorize `Mcp-Name: notes.read` while the origin executes `params.name: notes.delete`. It also keeps malformed input, header confusion, version negotiation, capability failure, authorization, and handler failure as distinct evidence.

> 这个顺序防止两个组件对"同一个调用"做出不同解读。网关不得授权 `Mcp-Name: notes.read` 的同时源站却执行 `params.name: notes.delete`。它还让畸形输入、头部混淆、版本协商、能力缺失、授权失败和 handler 故障各自留下独立的证据。

Closing stdin or an HTTP response ends transport activity. It does not terminate a protocol session because modern MCP has no protocol session.

> 关闭 stdin 或返回 HTTP 响应只是结束传输层活动。它并不终止协议会话，因为现代 MCP 根本没有协议会话。

### Explicit legacy compatibility

Versions through `2025-11-25` use `initialize`, `notifications/initialized`, connection-scoped capabilities, and, on earlier Streamable HTTP, optional protocol sessions. That behavior is still relevant when a dual-era client talks to an old server.

> 到 `2025-11-25` 为止的版本使用 `initialize`、`notifications/initialized`、连接级能力，以及在早期 Streamable HTTP 上可选的协议会话。当双时代客户端要对接旧服务器时，这些行为仍然相关。

Keep the eras separate. A modern request is identified by the required per-request metadata. A legacy connection is selected only through the documented fallback path. Do not send `initialize` as the default for a `2026-07-28` server.

> 把两个时代分开。现代请求由必需的逐请求元数据识别。旧版连接只能通过文档规定的回退路径选择。不要把 `initialize` 当作发给 `2026-07-28` 服务器的默认行为。

“Stateless” therefore has an era-specific meaning. In `2026-07-28`, it is a protocol invariant: every ordinary request is independently interpretable and no MCP session exists. In versions through `2025-11-25`, initialization and negotiated capabilities belong to a connection, so a compatibility adapter may retain that legacy connection state. A dual-era implementation is not one permissive state machine. It is a stateless modern core beside an isolated legacy adapter, with an explicit selection decision before either parser runs.

> 因此"无状态"有时代特定的含义。在 `2026-07-28` 中它是协议不变式：每个普通请求都可独立解读，不存在 MCP 会话。在到 `2025-11-25` 为止的版本中，初始化和协商出的能力属于连接，所以兼容适配器可以保留那份旧版连接状态。双时代实现不是一台"什么都能容"的状态机，而是：一个无状态的现代内核，旁边挂一个隔离的旧版适配器，在任何解析器运行之前先做一次显式的时代选择。

Neither meaning forbids durable application state. A workflow, task, or draft can live behind an opaque handle in a shared store. The client sends that handle as ordinary input, and every replica authenticates and authorizes its use. Protocol context must not leak into that store as a substitute for the removed session.

> 两种含义都不禁止持久的应用状态。工作流、任务或草稿可以活在共享存储中的一个不透明句柄后面。客户端把这个句柄当普通输入发送，每个副本都对它的使用做认证与授权。协议上下文不得作为被移除会话的替身泄漏进那个存储。

> **【拓展：双时代并存的现实】** "无状态"绝不等于"不能有业务状态"——这是最常见的误读。笔记、任务、工作流照常存库；被禁止的只是"把协议上下文当隐式会话用"（例如靠'这条连接上次声明过什么能力'来解码下一条请求）。分清"应用状态（可以持久）"与"协议会话状态（已移除）"，就抓住了 2026-07-28 版的精神。

```figure
mcp-tool-call
```

## Use It | 用框架实现

`code/main.py` builds, validates, traces, and dispatches modern MCP messages without a framework. Run:

> `code/main.py` 在不借助任何框架的情况下构建、校验、追踪并分发现代 MCP 消息。运行：

```bash
python3 code/main.py
python3 -m unittest discover code/tests -v
```

Watch for three invariants in the output:

> 在输出中关注三个不变式：

- Every request repeats its `_meta` fields.
  中文翻译：每个请求都重复携带自己的 `_meta` 字段。
- Every successful result is `resultType: "complete"` and includes server identity.
  中文翻译：每个成功结果都是 `resultType: "complete"` 且包含服务器身份。
- The list result is deterministically ordered and has explicit cache hints.
  中文翻译：列表结果有确定性排序并带显式缓存提示。

## Ship It | 产出物

This lesson ships `outputs/skill-mcp-handshake-tracer.md`. The historical filename remains stable, but the artifact is now a stateless request tracer. It audits each message independently and labels legacy handshake traffic only when it is genuinely present.

> 本课交付 `outputs/skill-mcp-handshake-tracer.md`。文件名沿用历史名称，但产物现在是一个无状态请求追踪器：它独立审计每条消息，只有当握手流量真实出现时才标注为 legacy。

## Exercises | 练习题

1. Change one request's protocol version to `2027-01-01`. Confirm the error code is `-32022` and the data advertises the supported version.
   中文翻译：把某个请求的协议版本改成 `2027-01-01`。确认错误码是 `-32022` 且 data 中公示了受支持的版本。

2. Remove `io.modelcontextprotocol/clientCapabilities` from the second request. Confirm the server does not reuse capabilities from the first request.
   中文翻译：从第二个请求中移除 `io.modelcontextprotocol/clientCapabilities`。确认服务器不会复用第一个请求的能力声明。

3. Reverse the in-memory tool registry. Confirm `tools/list` still returns the same deterministic order.
   中文翻译：反转内存中的工具注册表。确认 `tools/list` 仍返回同样的确定性顺序。

4. Change `cacheScope` from `public` to `private`. Explain which authorization contexts may reuse the response in each case.
   中文翻译：把 `cacheScope` 从 `public` 改成 `private`。解释两种情况下哪些授权上下文可以复用该响应。

5. Add an optional `clientInfo` omission test. The request should remain valid because client identity is recommended, not required.
   中文翻译：添加一个可选的 `clientInfo` 缺省测试。该请求应当仍然合法，因为客户端身份是建议项而非必填项。

## Key Terms | 术语速查表

| Term | Meaning |
|------|---------|
| Stateless protocol | Every request supplies the metadata needed to interpret it |
| Request metadata | Version, client capabilities, and recommended client identity in `params._meta` |
| `server/discover` | Mandatory server method for versions, capabilities, instructions, and identity |
| `resultType` | Discriminator on every successful modern result |
| Cacheable result | Result that includes required `ttlMs` and `cacheScope` hints |
| Protocol era | Modern per-request metadata or legacy connection-scoped initialization |
| Transport lifetime | Process, connection, or response-stream lifetime, not protocol session state |
| `-32022` | Unsupported protocol version error with requested and supported versions |

> 术语中文对照：Stateless protocol=无状态协议；Request metadata=请求元数据（`params._meta` 中的版本、客户端能力与建议的客户端身份）；server/discover=服务器发现（必选方法，公示版本、能力、说明与身份）；resultType=结果类型（每个成功现代结果上的判别字段）；Cacheable result=可缓存结果（必含 `ttlMs` 与 `cacheScope` 提示）；Protocol era=协议时代（现代逐请求元数据 vs 旧版连接级初始化）；Transport lifetime=传输层生命周期（进程/连接/响应流的存活期，不是协议会话状态）；-32022=不支持的协议版本错误（附 requested 与 supported）。

## Further Reading | 延伸阅读

- [MCP Architecture](https://modelcontextprotocol.io/specification/2026-07-28/architecture)
  中文翻译：MCP 架构文档（2026-07-28 版）
- [MCP Base Protocol](https://modelcontextprotocol.io/specification/2026-07-28/basic)
  中文翻译：MCP 基础协议（JSON-RPC 信封、元数据、生命周期）
- [MCP Server Discovery](https://modelcontextprotocol.io/specification/2026-07-28/server/discover)
  中文翻译：server/discover 方法规范
- [MCP 2026-07-28 Changelog](https://modelcontextprotocol.io/specification/2026-07-28/changelog)
  中文翻译：2026-07-28 版变更日志（相对旧版的核心差异清单）
