# Model Context Protocol (MCP) | 模型上下文协议

> MCP gives an AI host one protocol for discovering and invoking tools, resources, and prompts. The 2026-07-28 revision makes that protocol stateless: capability and version context travels with every request, not in a connection-bound handshake.

> **【中文解读】** MCP 给 AI 宿主一套统一协议来发现和调用工具、资源与提示模板。2026-07-28 修订版把协议改成了无状态：版本与能力上下文随每个请求携带，不再依赖绑定连接的握手。这是理解新版 MCP 的总纲——"每个请求自证身份"。

> **【拓展：MCP→Phase 13 深入路线】** 本课是 MCP 的第一次系统接触：给出协议模型和最小可运行实现。上游已把生产级边界拆成 Phase 13 的 28-31 四课（工具契约、可靠性、注册中心供应链、一致性工程），本课末尾"继续深入"一节给出了完整路线图。

> 🔗 **【前置】** 学本节前请先掌握：(1) Phase 11·09（Function Calling）——理解工具调用基础；(2) Phase 11·03（Structured Outputs）——理解 JSON Schema；(3) JSON-RPC 2.0 基本概念（请求/响应/通知）。旧版教程里的 `initialize` 握手和 `Mcp-Session-Id` 会话在新规范中已被移除——如果你学过旧版，先清掉这些记忆。

**Type:** Build | **类型:** 构建
**Languages:** Python | **语言:** Python
**Prerequisites:** Phase 11 · 09 (Function Calling), Phase 11 · 03 (Structured Outputs) | **前置知识:** Phase 11 · 09（函数调用）、Phase 11 · 03（结构化输出）
**Time:** ~75 minutes | **时间:** 约 75 分钟

## Learning Objectives | 学习目标

- Distinguish an MCP host, client, server, transport, and server primitive.
  中文翻译：区分 MCP 的宿主（host）、客户端（client）、服务器（server）、传输（transport）与服务器原语。
- Build a JSON-RPC request with the metadata required by MCP 2026-07-28.
  中文翻译：构建携带 MCP 2026-07-28 必需元数据的 JSON-RPC 请求。
- Use `server/discover` to inspect versions, identity, and capabilities.
  中文翻译：使用 `server/discover` 探测服务器的版本、身份与能力。
- Return typed and cache-aware results from tools, resources, and prompts.
  中文翻译：从工具、资源和提示返回带类型标记与缓存提示的结果。
- Explain how modern stateless MCP interoperates with handshake-era servers.
  中文翻译：解释现代无状态 MCP 如何与握手时代的旧服务器互操作。
- Choose safe state, transport, and approval boundaries for a server.
  中文翻译：为服务器选择安全的状态、传输与审批边界。

## The Problem | 问题引入

Your application needs a database query, a calendar operation, and a file reader. Without a shared protocol, every AI host needs custom discovery, invocation, errors, transport, and authorization glue for those same capabilities.

> 你的应用需要数据库查询、日历操作和文件读取。没有共享协议时，每个 AI 宿主都要为同样的能力编写定制的发现、调用、错误、传输与授权胶水代码。

MCP reduces that integration matrix. A server publishes a standard JSON-RPC surface. A compliant client can discover the surface, present it to a model or user, invoke it, and interpret the result without a server-specific adapter.

> MCP 压缩了这个集成矩阵。服务器发布标准 JSON-RPC 接口面；合规的客户端无需服务器专属适配器就能发现接口面、把它呈现给模型或用户、调用它并解释结果。

The important boundary is easy to miss. MCP standardizes communication. It does not decide which tool the model should call, make untrusted content safe, or turn a stateless request into durable application state. Your host and server still own those decisions.

> 一个容易忽略的关键边界：MCP 只标准化通信。它不决定模型该调用哪个工具、不会让不可信内容变安全、也不会把无状态请求变成持久的应用状态。这些决策仍归你的宿主和服务器所有。

> 💡 **【类比】** MCP 像"电源插座国标"。没有国标时，每台电器配一种插头，出一次国就要买一次转接头；有了国标，一个插座通吃所有电器。但国标不关心你插的是吹风机还是电钻——用电安全（审批、鉴权）是电器和用户自己的事。

## The Concept | 核心概念

![MCP host, stateless request, and server primitives](../assets/mcp-architecture.svg)

### The three server primitives | 三个服务器原语

1. **Tools** are callable actions. Each tool has a name, description, JSON Schema input, and handler.
2. **Resources** are named, URI-addressed content that a client can read.
3. **Prompts** are reusable templates that a host can expose to a user.

The host is the AI application. An MCP client inside that host speaks to one server. The transport carries JSON-RPC messages between them.

> 宿主是 AI 应用本身；宿主内的一个 MCP 客户端只与一个服务器对话；传输层在两者之间搬运 JSON-RPC 消息。注意"客户端:服务器 = 1:1"——需要多个服务器时就挂多个客户端。

### Stateless requests replace the handshake | 无状态请求取代握手

> **【中文解读】** 这一节是新版规范最大的变化点：`initialize` 握手、`notifications/initialized` 和协议级会话全部移除。取而代之的是每个请求自带 `params._meta`（协议版本、客户端能力、客户端身份）。缺 `_meta`、缺必填字段或类型不对 → `-32602`；版本格式合法但服务器不支持 → `-32022`。

MCP 2026-07-28 removes `initialize` and `notifications/initialized`. It also removes protocol-level sessions. Every request carries the context needed to interpret it in `params._meta`:

```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "method": "tools/list",
  "params": {
    "_meta": {
      "io.modelcontextprotocol/protocolVersion": "2026-07-28",
      "io.modelcontextprotocol/clientCapabilities": {},
      "io.modelcontextprotocol/clientInfo": {
        "name": "lesson-client",
        "version": "1.0.0"
      }
    }
  }
}
```

The protocol version and client capabilities are required. Client identity is recommended. A missing `_meta`, a missing required field, or a required field with the wrong type is malformed and returns Invalid Params (`-32602`). A well-formed version string that the server does not support returns `UnsupportedProtocolVersionError` (`-32022`). A server can process a valid request without recovering a prior negotiation record.

Stateless does not mean an application can never maintain state. It means that state is not hidden behind an MCP connection or `Mcp-Session-Id`. If a workflow needs continuity, the server mints an opaque handle and the client passes that handle as an ordinary tool argument on later calls. Authorization must still be checked on every request.

> "无状态"不等于应用不能有状态，而是状态不能藏在 MCP 连接或 `Mcp-Session-Id` 后面。工作流需要连续性时，由服务器签发一个不透明句柄（handle），客户端在后续调用中把它当普通工具参数传回。鉴权仍然必须逐请求检查。

> ⚠️ **【易错点】** 旧代码把客户端元数据缓存在"连接对象"里、只在握手时发一次——新版服务器会逐请求校验 `_meta`，漏带的请求直接被拒。每个请求都要重建元数据。

### Discovery and version selection | 发现与版本选择

> **【中文解读】** `server/discover` 是新版服务器的必选方法：返回支持的版本、能力与服务器身份，并带 `ttlMs`/`cacheScope` 缓存提示。双时代客户端在 stdio 上先用 `server/discover` 探测：收到发现结果或可识别的现代错误（如 `-32022`）说明是现代服务器；遇到无法识别的错误或超时才允许回退到 2025-11-25 的 `initialize` 流程——旧流程是兼容代码，不是现代默认。

Every modern server implements `server/discover`. The result advertises supported versions, capabilities, and server identity:

```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "result": {
    "resultType": "complete",
    "supportedVersions": ["2026-07-28"],
    "capabilities": {
      "tools": {},
      "resources": {},
      "prompts": {}
    },
    "ttlMs": 3600000,
    "cacheScope": "public",
    "_meta": {
      "io.modelcontextprotocol/serverInfo": {
        "name": "demo-server",
        "version": "1.0.0"
      }
    }
  }
}
```

A client may call another method directly and handle a version error, but discovery makes capability display and version selection explicit. An unsupported version returns `UnsupportedProtocolVersionError` with code `-32022`. Its data contains `supported`, an array of server revisions, and `requested`, the rejected revision.

On stdio, a dual-era client probes with `server/discover`. A discovery result or a recognized modern error such as `UnsupportedProtocolVersionError` identifies a modern server. Any error or timeout that is not recognized as modern permits fallback to the 2025-11-25 `initialize` flow. Legacy behavior is compatibility code, not the modern default.

### Results are explicit | 结果是显式的

> **【中文解读】** 每个核心结果都带 `resultType`：`complete`（操作完成）或 `input_required`（需要客户端按 MRTR 模式再来一轮往返；核心服务器只允许在 `tools/call`、`resources/read`、`prompts/get` 里返回它）。旧式省略 `resultType` 的结果必须按 `complete` 处理。列表/读取结果还带 `ttlMs` 与 `cacheScope`——确定性排序 + 新鲜度提示让客户端可以安全缓存，并提升 prompt cache 命中率。

Every core 2026-07-28 result has `resultType`:

- `complete` means the operation finished.
- `input_required` means the server needs another round trip through the Multi Round-Trip Requests pattern. Core servers may return it only from `tools/call`, `resources/read`, or `prompts/get`.

Clients must treat a legacy result that omits `resultType` as complete.

Servers should include `io.modelcontextprotocol/serverInfo` in every result's `_meta`. This identity is self-reported and is for display, logging, and debugging, not for security decisions.

List and read results also carry `ttlMs` and `cacheScope`. A deterministic `tools/list` order plus a freshness hint lets clients cache discovery safely and improves prompt-cache stability. `cacheScope: public` permits shared caching; `private` confines reuse to the calling context.

### The wire format and transport | 线格式与传输层

> **【中文解读】** 线格式仍是 JSON-RPC 2.0。现代 Streamable HTTP 只暴露一个接受 POST 的端点，每条 JSON-RPC 消息独立一个 POST；请求 POST 的响应是一个 JSON 对象或一条请求级 SSE 流；通知 POST 被接受时返回 HTTP 202 空响应体。2026-07-28 里没有独立 GET 流、没有 DELETE 会话端点、没有 `Mcp-Session-Id`、没有 `Last-Event-ID` 重放——长期变更通知改用 `subscriptions/listen` POST（响应保持为打开的 SSE 流）。

MCP uses JSON-RPC 2.0 over stdio or Streamable HTTP.

- A request has `jsonrpc`, `id`, `method`, and `params`.
- A response has the matching `id` and either `result` or `error`.
- A notification has no `id` and expects no response.

Modern Streamable HTTP exposes one endpoint that accepts POST. Each JSON-RPC message gets its own POST. A request POST receives either one JSON object or a request-scoped Server-Sent Events stream that ends with the final response. An accepted notification POST receives HTTP 202 with no response body; this core revision defines no client-to-server notifications over Streamable HTTP.

There is no standalone MCP GET stream, DELETE session endpoint, `Mcp-Session-Id`, or `Last-Event-ID` replay in 2026-07-28. Long-lived change notifications use a `subscriptions/listen` POST whose response remains open as an SSE stream.

### Client input without server-initiated requests | 没有服务器主动请求的客户端输入

> **【中文解读】** 旧规范允许服务器反向发请求（`sampling/createMessage`、`roots/list`、`elicitation/create`）；现行协议改用 MRTR（Multi Round-Trip Requests）：工具调用返回 `resultType: input_required` 并附 `inputRequests`/`requestState`，客户端收集输入后用**新的 JSON-RPC ID** 重试原方法并携带 `inputResponses`，原样回传 `requestState`。Roots/Sampling/Logging 仍可用但已弃用——新实现不要再采用，优先用显式文件/目录参数、资源 URI 和直连模型提供商。

Older revisions let a server send requests such as `sampling/createMessage`, `roots/list`, or `elicitation/create` over a stream. The current protocol uses Multi Round-Trip Requests instead. An eligible tool call, resource read, or prompt get returns `resultType: input_required` with at least one of `inputRequests` or `requestState`. The client gathers any requested input, retries the original method with a new JSON-RPC ID and the corresponding `inputResponses`, and echoes the exact `requestState` when one was provided. If no `inputRequests` were present, the retry omits `inputResponses`.

Roots, Sampling, and Logging remain functional but are deprecated, so new implementations should not adopt them. Existing Roots or Sampling requests travel inside MRTR `inputRequests`, never as independent server-to-client JSON-RPC requests. Prefer explicit file or directory parameters, resource URIs, server configuration, and direct model-provider integration. Use stderr for stdio diagnostics and OpenTelemetry for production telemetry.

```figure
mcp-nxm-collapse
```

## Build It | 动手构建

> **【中文解读】** 五步构建：(1) 注册服务器接口面（工具/资源/提示）；(2) 给每个请求附加 `_meta` 元数据——不要只缓存在连接对象里；(3) 可选地先 `server/discover` 再 `tools/list`；(4) HTTP 远程调用时带上与请求体镜像的路由头（`MCP-Protocol-Version`/`Mcp-Method`/`Mcp-Name`），头体不一致 → HTTP 400 + `-32020`；(5) 把安全边界放在协议状态之外——逐请求鉴权、localhost 绑定 + Origin 校验、`destructiveHint` 标记破坏性工具并要求宿主审批。

### Step 1: register a server surface | 第一步：注册服务器接口面

Registration stays simple even though the request contract changed:

```python
server = MCPServer("demo-server")

@server.tool(
    "add",
    "Add two integers.",
    {
        "type": "object",
        "properties": {
            "a": {"type": "integer"},
            "b": {"type": "integer"}
        },
        "required": ["a", "b"]
    }
)
def add(a: int, b: int) -> dict:
    return {"sum": a + b}
```

The shipped implementation in `code/main.py` also registers a resource and prompt. It deliberately uses the standard library so you can see each envelope rather than delegating the protocol to an SDK.

### Step 2: attach metadata to every request | 第二步：给每个请求附加元数据

```python
def request(method, params=None):
    body_params = dict(params or {})
    body_params["_meta"] = {
        "io.modelcontextprotocol/protocolVersion": "2026-07-28",
        "io.modelcontextprotocol/clientCapabilities": {},
        "io.modelcontextprotocol/clientInfo": {
            "name": "demo-client",
            "version": "1.0.0"
        }
    }
    return {
        "jsonrpc": "2.0",
        "id": 1,
        "method": method,
        "params": body_params
    }
```

Do not cache this metadata only in a connection object. The server validates it on each request.

### Step 3: optionally discover before listing | 第三步：可选地在列表前先发现

Call `server/discover`, choose a supported version, then call `tools/list`. A direct `tools/list` is also valid if you already know the version and can handle `-32022`.

The demo returns tool lists in name order and attaches `ttlMs`, `cacheScope`, `resultType`, and server identity. A tool call returns a complete, non-cacheable result because its output can depend on current state.

### Step 4: map the same request to HTTP | 第四步：把同一请求映射到 HTTP

A remote `tools/call` POST includes headers that mirror the JSON-RPC body:

```http
POST /mcp HTTP/1.1
Content-Type: application/json
Accept: application/json, text/event-stream
MCP-Protocol-Version: 2026-07-28
Mcp-Method: tools/call
Mcp-Name: add
```

The `MCP-Protocol-Version` header must match the version in `_meta`. `Mcp-Method` is required on every JSON-RPC request and must match `method`. `Mcp-Name` is required only for `tools/call`, `resources/read`, and `prompts/get`, where it must match the tool name, resource URI, or prompt name. A missing required header or mismatch returns HTTP 400 with `HeaderMismatch` code `-32020`.

### Step 5: enforce safety outside protocol state | 第五步：在协议状态之外落实安全

- Validate authorization and audience on every HTTP request.
- Bind local servers to localhost and validate `Origin` on Streamable HTTP.
- Mark mutating tools with `destructiveHint: true` and require host approval.
- Pass directory and file scope explicitly instead of depending on deprecated Roots.
- Treat resources and tool output as untrusted data.
- Keep stdout reserved for JSON-RPC under stdio; write diagnostics to stderr.

## Use It | 运行验证

Run the lesson from its directory:

```bash
python3 code/main.py
cd code
python3 -m unittest discover tests -v
```

The first line should report discovery of `demo-server` at protocol `2026-07-28`. Then inspect `MCPClient.request`: it reconstructs `_meta` for every call. Remove the metadata from one request and observe the server reject it.

## Ship It | 交付产物

`outputs/skill-mcp-server-designer.md` turns a domain into a stateless MCP design. Its acceptance gate requires a discovery result, per-request metadata policy, deterministic cache-aware lists, explicit state handles, transport headers, authorization, and approval rules.

## Continue the MCP Deep Dive | 继续深入 MCP

This lesson gives you the protocol model. Phase 13 turns four production boundaries into separate build-and-verify lessons:

1. [MCP Tool Contracts and Content](../../../13-tools-and-protocols/28-mcp-tool-contracts-and-content/docs/en.md) covers closed input schemas, structured content, routing metadata, opaque pagination, completion authorization, and the difference between protocol and tool-domain errors.
2. [MCP Reliability, Cancellation, and Flow Control](../../../13-tools-and-protocols/29-mcp-reliability-cancellation-and-flow-control/docs/en.md) covers request cancellation, durable task cancellation, deadlines, idempotency, backpressure, proxy buffering, and reconnect behavior.
3. [MCP Registry Supply Chain, Admission, Drift, and Rollback](../../../13-tools-and-protocols/30-mcp-registry-supply-chain-and-drift/docs/en.md) covers namespace proof, artifact provenance, immutable pins, live drift, Registry status, admission evidence, and rollback.
4. [MCP Conformance Engineering](../../../13-tools-and-protocols/31-mcp-conformance-versioning-and-operations/docs/en.md) covers golden and negative wire transcripts, strict version eras, SDK differentials, proxy evidence, redaction, health gates, and release rollback.

Follow them in order when the server will cross a team or trust boundary. Together they move from “the method works” to “the contract remains safe and diagnosable through deployment.”

## Exercises | 练习

1. Add a `subtract` tool and confirm `tools/list` remains alphabetically ordered.
2. Remove the protocol-version key and verify Invalid Params (`-32602`). Then send the well-formed but unsupported version `2025-11-25`, verify `-32022`, confirm `requested` echoes that revision, and choose from `supported`.
3. Add a server-minted `draftId` to a create operation, then require it as an argument to update. Explain why that is application state rather than a protocol session.
4. Return `input_required` from a tool that needs user confirmation. Retry the original call with a new ID, an `inputResponses` entry, and the exact `requestState` instead of inventing a server-to-client JSON-RPC request.
5. Sketch a dual-era stdio client. Treat a result or recognized modern error as modern, and permit fallback to `initialize` only for an unrecognized error or timeout.

## Key Terms | 关键术语

| Term | What people say | What it actually means |
|------|-----------------|------------------------|
| MCP | "Tool protocol for LLMs" | JSON-RPC protocol for server discovery, tools, resources, prompts, and extensions |
| Host | "The AI app" | Owns the model and UI and mounts one or more MCP clients |
| Client | "The connector" | Speaks MCP to one server on behalf of a host |
| Stateless MCP | "No session" | Every request carries version and capabilities; no protocol state is keyed by a connection |
| `server/discover` | "Capability probe" | Required server method advertising versions, capabilities, and identity |
| `resultType` | "Result state" | Marks a result as `complete` or `input_required` |
| State handle | "Workflow id" | Server-minted application identifier passed as an ordinary argument |
| Streamable HTTP | "Remote transport" | One POST endpoint with JSON or request-scoped SSE responses |
| MRTR | "Ask and retry" | Input request embedded in a result, followed by a retry of the original operation |

## Further Reading | 延伸阅读

- [MCP 2026-07-28 key changes](https://modelcontextprotocol.io/specification/2026-07-28/changelog)
- [MCP server discovery](https://modelcontextprotocol.io/specification/2026-07-28/server/discover)
- [MCP Streamable HTTP](https://modelcontextprotocol.io/specification/2026-07-28/basic/transports/streamable-http)
- [MCP Multi Round-Trip Requests](https://modelcontextprotocol.io/specification/2026-07-28/basic/patterns/mrtr)
- [MCP deprecated features](https://modelcontextprotocol.io/specification/2026-07-28/deprecated)
