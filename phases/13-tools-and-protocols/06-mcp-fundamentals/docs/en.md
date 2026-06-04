# MCP Fundamentals — Primitives, Lifecycle, JSON-RPC Base | MCP 基础：原语、生命周期与 JSON-RPC

> Every integration before MCP was a one-off. The Model Context Protocol, first shipped by Anthropic in November 2024 and now stewarded by the Linux Foundation's Agentic AI Foundation, standardizes discovery and invocation so any client can speak to any server. The 2025-11-25 spec names six primitives (three server, three client), a three-phase lifecycle, and a JSON-RPC 2.0 wire format. Learn those and the rest of the MCP chapter of this phase becomes reading.

> **【中文解读】** MCP 之前的每个集成都是定制的。Model Context Protocol 由 Anthropic 于 2024 年 11 月首发，现由 Linux 基金会的 Agentic AI Foundation 管理。它标准化了发现和调用，使任何客户端能与任何服务器通信。2025-11-25 规范定义了六个原语（三个服务器端、三个客户端端）、三阶段生命周期和 JSON-RPC 2.0 线格式。

> **【拓展：MCP→Claude 协议生态】** MCP 是 Claude 生态的核心协议。Claude Desktop、Cursor、VS Code Copilot 等 300+ 客户端都支持 MCP。一个 MCP 服务器可以在所有这些客户端中工作，无需重复开发。MCP 的六原语模型（tools/resources/prompts + roots/sampling/elicitation）是理解整个协议的基础。

**Type:** Learn
**Languages:** Python (stdlib, JSON-RPC parser)
**Prerequisites:** Phase 13 · 01 through 05 (the tool interface and function calling)
**Time:** ~45 minutes

## Learning Objectives

- Name all six MCP primitives (tools, resources, prompts on the server; roots, sampling, elicitation on the client) and give one use case each.
- Walk through the three-phase lifecycle (initialize, operation, shutdown) and state who sends which message at each phase.
- Parse and emit JSON-RPC 2.0 request, response, and notification envelopes.
- Explain what capability negotiation at `initialize` is and what breaks without it.

## The Problem | 问题引入

Before MCP, every tool-using agent had its own protocol. Cursor had an MCP-shaped but incompatible tool system. Claude Desktop shipped with a different one. VS Code's Copilot extension had a third. A team that built a "Postgres query" tool wrote the same tool three times, each to a different host's API. Reusing it required copying code.

The result was a Cambrian explosion of one-off integrations and a ceiling on ecosystem velocity.

MCP fixes this by standardizing the wire format. A single MCP server works in every MCP client: Claude Desktop, ChatGPT, Cursor, VS Code, Gemini, Goose, Zed, Windsurf, 300+ clients by April 2026. 110M monthly SDK downloads. 10,000+ public servers. The Linux Foundation took stewardship in December 2025 under the new Agentic AI Foundation.

> **【中文解读】** MCP 之前，Cursor、Claude Desktop、VS Code Copilot 各有自己的工具协议。一个"Postgres 查询"工具要写三次。MCP 通过标准化线格式解决了这个问题：一个 MCP 服务器可在所有 MCP 客户端中工作。截至 2026 年 4 月，已有 300+ 客户端、月 SDK 下载 1.1 亿、1 万+ 公开服务器。

The spec revision used in this phase is **2025-11-25**. It adds async Tasks (SEP-1686), URL-mode elicitation (SEP-1036), sampling with tools (SEP-1577), incremental scope consent (SEP-835), and OAuth 2.1 resource-indicator semantics. Phase 13 · 09 through 16 cover those extensions. This lesson stops at the base.

## The Concept | 核心概念

### Three server primitives

> **【中文解读】** MCP 定义了三个服务器原语：(1) Tools——可调用动作，与 Phase 13.01 的四步循环相同；(2) Resources——暴露的数据，只读内容通过 URI 寻址（`file:///`、`db://`等）；(3) Prompts——可复用模板，宿主 UI 中的斜杠命令。

1. **Tools.** Callable actions. Same four-step loop from Phase 13 · 01.
2. **Resources.** Exposed data. Read-only content addressable by URI: `file:///path`, `db://query/...`, custom schemes.
3. **Prompts.** Reusable templates. Slash-commands in the host UI; server supplies the template, client fills arguments.

### Three client primitives

> **【拓展：MCP 的双向通信模型】** MCP 的独特之处在于它是双向协议。不仅客户端可以调用服务器的工具，服务器也能反过来请求客户端的模型执行补全（sampling），或请求用户输入（elicitation）。这种对称性使得服务器可以托管 Agent 循环而不需要自己的 API key——它借用客户端的模型能力。

4. **Roots.** The set of URIs the server is allowed to touch. Client declares them; server respects them.
5. **Sampling.** Server requests the client's model to perform a completion. Enables server-hosted agent loops without server-side API keys.
6. **Elicitation.** Server asks the client's user for structured input mid-flight. Forms or URLs (SEP-1036).

Every capability in MCP belongs to exactly one of these six. Phase 13 · 10 through 14 cover each in depth.

### Wire format: JSON-RPC 2.0

> **【中文解读】** MCP 使用 JSON-RPC 2.0 作为线格式。三种消息类型：请求（有 id，需要响应）、响应（包含 result 或 error）、通知（无 id，不需要响应）。基础规范约 15 个方法，按原语分组：`initialize`/`initialized`、`tools/list`/`tools/call`、`resources/list`/`resources/read`、`prompts/list`/`prompts/get` 等。

Every message is a JSON object with these fields:

- Requests: `{jsonrpc: "2.0", id, method, params}`.
- Responses: `{jsonrpc: "2.0", id, result | error}`.
- Notifications: `{jsonrpc: "2.0", method, params}` — no `id`, no response expected.

The base spec has ~15 methods, grouped by primitive. The important ones:

- `initialize` / `initialized` (handshake)
- `tools/list`, `tools/call`
- `resources/list`, `resources/read`, `resources/subscribe`
- `prompts/list`, `prompts/get`
- `sampling/createMessage` (server-to-client)
- `notifications/tools/list_changed`, `notifications/resources/updated`, `notifications/progress`

### Three-phase lifecycle

> **【中文解读】** MCP 三阶段生命周期：(1) 初始化——客户端发送 `initialize` 携带 `capabilities` 和 `clientInfo`，服务器响应自己的 `capabilities`、`serverInfo` 和协议版本；(2) 操作——双向通信，客户端调用工具、读取资源，服务器可发采样请求和变更通知；(3) 关闭——任一方关闭传输层。

**Phase 1: initialize.**

Client sends `initialize` with its `capabilities` and `clientInfo`. Server responds with its own `capabilities`, `serverInfo`, and the spec version it speaks. Client sends `notifications/initialized` when it has digested the response. From here on, either side can send requests per the negotiated capabilities.

**Phase 2: operation.**

Bidirectional. Client calls `tools/list` to discover, then `tools/call` to invoke. Server may send `sampling/createMessage` if it declared that capability. Server may send `notifications/tools/list_changed` when its tool set mutates. Client may send `notifications/roots/list_changed` when the user changes root scope.

**Phase 3: shutdown.**

Either side closes the transport. No structured shutdown method in MCP; the transport (stdio or Streamable HTTP, Phase 13 · 09) carries the end-of-connection signal.

### Capability negotiation

`capabilities` in the `initialize` handshake is the contract. Example from a server:

```json
{
  "tools": {"listChanged": true},
  "resources": {"subscribe": true, "listChanged": true},
  "prompts": {"listChanged": true}
}
```

The server declares it can emit `tools/list_changed` notifications and supports `resources/subscribe`. The client agrees by declaring its own:

```json
{
  "roots": {"listChanged": true},
  "sampling": {},
  "elicitation": {}
}
```

If the client does not declare `sampling`, the server must not call `sampling/createMessage`. Symmetric: if the server does not declare `resources.subscribe`, the client must not try to subscribe.

This is what prevents ecosystem drift. A client that does not support sampling is still a valid MCP client; a server that does not call `sampling` is still a valid MCP server. They just do not use that feature together.

> **【中文解读】** 能力协商是 MCP 防止生态漂移的关键机制。不支持 sampling 的客户端仍是合法 MCP 客户端；不调用 sampling 的服务器仍是合法 MCP 服务器。它们只是不一起使用那个特性。对称性：服务器不声明 `resources.subscribe`，客户端就不能订阅。

### Structured content and error shapes

`tools/call` returns a `content` array of typed blocks: `text`, `image`, `resource`. Phase 13 · 14 adds MCP Apps (`ui://` interactive UI) to that list.

Errors use JSON-RPC error codes. The spec-defined additions: `-32002` "Resource not found", `-32603` "Internal error", plus MCP-specific error data as `error.data`.

### Client capabilities vs tool call details

A common confusion: `capabilities.tools` is whether the client supports tool-list-changed notifications. Whether the client WILL call specific tools is a runtime choice driven by its model, not a capability flag. The capability flag is the spec-level contract. The model's choice is orthogonal.

### Why JSON-RPC and not REST?

> **【拓展：MCP 为什么选择 JSON-RPC 而非 REST】** JSON-RPC 2.0 是轻量级双向协议（2010年标准）。REST 是客户端发起的单向协议。MCP 需要服务器主动发起消息（sampling、notifications），JSON-RPC 的对称请求/响应形状天然适合。JSON-RPC 还可以在 stdio 和 WebSocket/Streamable HTTP 上干净地组合，无需重新发明 HTTP 请求格式。

JSON-RPC 2.0 (2010) is a lightweight bidirectional protocol. REST is client-initiated. MCP needed server-initiated messages (sampling, notifications), so JSON-RPC with its symmetric request/response shape was a natural fit. JSON-RPC also composes cleanly over stdio and WebSocket/Streamable HTTP without re-inventing HTTP's request shape.

## Use It | 用框架实现

`code/main.py` ships a minimal JSON-RPC 2.0 parser and emitter, then walks the `initialize` → `tools/list` → `tools/call` → `shutdown` sequence by hand, printing every message. No real transport; just the message shapes. Compare to the spec linked in Further Reading to verify each envelope.

What to look at:

- `initialize` declares capabilities both ways; the response has `serverInfo` and `protocolVersion: "2025-11-25"`.
- `tools/list` returns a `tools` array; each entry has `name`, `description`, `inputSchema`.
- `tools/call` uses `params.name` and `params.arguments`.
- The response `content` is an array of `{type, text}` blocks.

## Ship It | 产出物

This lesson produces `outputs/skill-mcp-handshake-tracer.md`. Given a pcap-style transcript of an MCP client-server interaction, the skill annotates each message with which primitive, which lifecycle phase, and which capability it depends on.

## Exercises | 练习题

1. Run `code/main.py`. Identify the line where capability negotiation happens and describe what would change if the server did not declare `tools.listChanged`.

2. Extend the parser to handle `notifications/progress`. The message shape: `{method: "notifications/progress", params: {progressToken, progress, total}}`. Emit it while a long-running `tools/call` is in progress and confirm the client handler would display a progress bar.

3. Read the MCP 2025-11-25 spec top to bottom — the whole document is about 80 pages. Identify the one capability flag most servers do NOT need. Hint: it relates to resource subscription.

4. Sketch on paper the primitive a hypothetical "cron job" feature would belong to. (Hint: the server wants the client to invoke it at a scheduled time. None of the six primitives fit today.) MCP's 2026 roadmap has a draft SEP for this.

5. Parse one session log from an open MCP server on GitHub. Count request vs response vs notification messages. Compute what fraction of traffic is lifecycle vs operation.

## Key Terms | 术语速查表

| Term | What people say | What it actually means | 中文术语 |
|------|----------------|------------------------|----------|
| MCP | "Model Context Protocol" | Open protocol for model-to-tool discovery and invocation | 模型上下文协议 |
| Server primitive | "What a server exposes" | tools (actions), resources (data), prompts (templates) | 服务器原语 |
| Client primitive | "What a client lets servers use" | roots (scope), sampling (LLM callbacks), elicitation (user input) | 客户端原语 |
| JSON-RPC 2.0 | "The wire format" | Symmetric request/response/notification envelopes | JSON-RPC 2.0 线格式 |
| `initialize` handshake | "Capability negotiation" | First message pair; servers and clients declare features they support | 初始化握手 |
| `tools/list` | "Discovery" | Client asks server for its current tool set | 工具发现 |
| `tools/call` | "Invocation" | Client asks server to execute a tool with arguments | 工具调用 |
| `notifications/*_changed` | "Mutation events" | Server tells client that its primitive list has changed | 变更通知 |
| Content block | "Typed result" | `{type: "text" \| "image" \| "resource" \| "ui_resource"}` in tool result | 内容块 |
| SEP | "Spec Evolution Proposal" | Named draft proposal (e.g. SEP-1686 for async Tasks) | 规范演进提案 |

## Further Reading | 延伸阅读

- [Model Context Protocol — Specification 2025-11-25](https://modelcontextprotocol.io/specification/2025-11-25) — the canonical spec document
- [Model Context Protocol — Architecture concepts](https://modelcontextprotocol.io/docs/concepts/architecture) — the six-primitive mental model
- [Anthropic — Introducing the Model Context Protocol](https://www.anthropic.com/news/model-context-protocol) — November 2024 launch post
- [MCP blog — First MCP anniversary](https://blog.modelcontextprotocol.io/posts/2025-11-25-first-mcp-anniversary/) — one-year retrospective and the 2025-11-25 spec changes
- [WorkOS — MCP 2025-11-25 spec update](https://workos.com/blog/mcp-2025-11-25-spec-update) — summary of SEP-1686, 1036, 1577, 835, and 1724
