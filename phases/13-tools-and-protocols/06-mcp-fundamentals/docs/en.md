# MCP Fundamentals — Primitives, Lifecycle, JSON-RPC Base | MCP 基础：原语、生命周期与 JSON-RPC

> Every integration before MCP was a one-off. The Model Context Protocol, first shipped by Anthropic in November 2024 and now stewarded by the Linux Foundation's Agentic AI Foundation, standardizes discovery and invocation so any client can speak to any server. The 2025-11-25 spec names six primitives (three server, three client), a three-phase lifecycle, and a JSON-RPC 2.0 wire format. Learn those and the rest of the MCP chapter of this phase becomes reading.

> **【中文解读】** MCP 之前的每个集成都是定制的。Model Context Protocol 由 Anthropic 于 2024 年 11 月首发，现由 Linux 基金会的 Agentic AI Foundation 管理。它标准化了发现和调用，使任何客户端能与任何服务器通信。2025-11-25 规范定义了六个原语（三个服务器端、三个客户端端）、三阶段生命周期和 JSON-RPC 2.0 线格式。

> **【拓展：MCP→Claude 协议生态】** MCP 是 Claude 生态的核心协议。Claude Desktop、Cursor、VS Code Copilot 等 300+ 客户端都支持 MCP。一个 MCP 服务器可以在所有这些客户端中工作，无需重复开发。MCP 的六原语模型（tools/resources/prompts + roots/sampling/elicitation）是理解整个协议的基础。

> 🔗 **【前置】** 学本节前请先掌握：(1) Phase 13·01 到 05——理解工具接口、函数调用、Schema 设计；(2) JSON-RPC 2.0 基础（request/response/notification 三种消息类型）；(3) Phase 11·14（MCP 简介）有过整体认识。本节是 MCP 系列的基础课，后续 7-18 节都基于此。

**Type:** Learn | **类型:** 学习
**Languages:** Python (stdlib, JSON-RPC parser) | **语言:** Python (stdlib, JSON-RPC parser)
**Prerequisites:** Phase 13 · 01 through 05 (the tool interface and function calling) | **前置知识:** Phase 13 · 01 through 05 (the tool interface and function calling)
**Time:** ~45 minutes | **时间:** ~45 分钟

## Learning Objectives | 学习目标

- Name all six MCP primitives (tools, resources, prompts on the server; roots, sampling, elicitation on the client) and give one use case each.
  中文翻译：说出所有六个 MCP 原语（服务器端的 tools、resources、prompts；客户端端的 roots、sampling、elicution）并为每个给出一个用例。
- Walk through the three-phase lifecycle (initialize, operation, shutdown) and state who sends which message at each phase.
  中文翻译：走一遍三阶段生命周期（初始化、操作、关闭）并说明每个阶段谁发送什么消息。
- Parse and emit JSON-RPC 2.0 request, response, and notification envelopes.
  中文翻译：解析和发出 JSON-RPC 2.0 的请求、响应和通知信封。
- Explain what capability negotiation at `initialize` is and what breaks without it.
  中文翻译：解释 `initialize` 中的能力协商是什么以及没有它会出什么问题。

## The Problem | 问题引入

Before MCP, every tool-using agent had its own protocol. Cursor had an MCP-shaped but incompatible tool system. Claude Desktop shipped with a different one. VS Code's Copilot extension had a third. A team that built a "Postgres query" tool wrote the same tool three times, each to a different host's API. Reusing it required copying code.

> MCP 之前，每个使用工具的 agent 都有自己的协议。Cursor 有一个 MCP 形状但不兼容的工具系统。Claude Desktop 采用了不同的方式。VS Code 的 Copilot 扩展是第三种。一个构建"Postgres 查询"工具的团队要写三次相同的工具，每次针对不同的宿主 API。复用它需要复制代码。

The result was a Cambrian explosion of one-off integrations and a ceiling on ecosystem velocity.

> 结果是一次寒武纪大爆发般的一次性集成，以及生态系统增速的上限。

MCP fixes this by standardizing the wire format. A single MCP server works in every MCP client: Claude Desktop, ChatGPT, Cursor, VS Code, Gemini, Goose, Zed, Windsurf, 300+ clients by April 2026. 110M monthly SDK downloads. 10,000+ public servers. The Linux Foundation took stewardship in December 2025 under the new Agentic AI Foundation.

> MCP 通过标准化线格式解决了这个问题。一个 MCP 服务器可以在每个 MCP 客户端中工作：Claude Desktop、ChatGPT、Cursor、VS Code、Gemini、Goose、Zed、Windsurf，截至 2026 年 4 月有 300+ 客户端。月 SDK 下载 1.1 亿。1 万+ 公开服务器。Linux 基金会于 2025 年 12 月在新成立的 Agentic AI Foundation 下接管了管理工作。

> 💡 **【类比】** MCP 像 USB-C 标准。USB-C 之前，每个设备都有自己的充电口（Micro-USB、Lightning、专用圆口），出差要带 5 根线。USB-C 后：一根线充所有。MCP 之前：每个 AI 应用（Claude/Cursor/ChatGPT）都有自己的工具集成 API，开发者要给每个写一遍适配。MCP 后：写一个 MCP server，所有 host 即插即用。MCP 的六原语就像 USB-C 规范里定义的"功率/数据/视频"通道标准。

> **【中文解读】** MCP 之前，Cursor、Claude Desktop、VS Code Copilot 各有自己的工具协议。一个"Postgres 查询"工具要写三次。MCP 通过标准化线格式解决了这个问题：一个 MCP 服务器可在所有 MCP 客户端中工作。截至 2026 年 4 月，已有 300+ 客户端、月 SDK 下载 1.1 亿、1 万+ 公开服务器。

The spec revision used in this phase is **2025-11-25**. It adds async Tasks (SEP-1686), URL-mode elicitation (SEP-1036), sampling with tools (SEP-1577), incremental scope consent (SEP-835), and OAuth 2.1 resource-indicator semantics. Phase 13 · 09 through 16 cover those extensions. This lesson stops at the base.

> 本 phase 使用的规范版本是 **2025-11-25**。它添加了异步任务（SEP-1686）、URL 模式 elicitation（SEP-1036）、带工具的采样（SEP-1577）、增量范围同意（SEP-835）和 OAuth 2.1 资源指示器语义。Phase 13 · 09 到 16 涵盖这些扩展。本课只讲基础。

## The Concept | 核心概念

### Three server primitives

> **【中文解读】** MCP 定义了三个服务器原语：(1) Tools——可调用动作，与 Phase 13.01 的四步循环相同；(2) Resources——暴露的数据，只读内容通过 URI 寻址（`file:///`、`db://`等）；(3) Prompts——可复用模板，宿主 UI 中的斜杠命令。

1. **Tools.** Callable actions. Same four-step loop from Phase 13 · 01.
   中文翻译：**Tools。** 可调用动作。与 Phase 13 · 01 的四步循环相同。
2. **Resources.** Exposed data. Read-only content addressable by URI: `file:///path`, `db://query/...`, custom schemes.
   中文翻译：**Resources。** 暴露的数据。通过 URI 寻址的只读内容：`file:///path`、`db://query/...`、自定义方案。
3. **Prompts.** Reusable templates. Slash-commands in the host UI; server supplies the template, client fills arguments.
   中文翻译：**Prompts。** 可复用模板。宿主 UI 中的斜杠命令；服务器提供模板，客户端填充参数。

### Three client primitives

> **【拓展：MCP 的双向通信模型】** MCP 的独特之处在于它是双向协议。不仅客户端可以调用服务器的工具，服务器也能反过来请求客户端的模型执行补全（sampling），或请求用户输入（elicitation）。这种对称性使得服务器可以托管 Agent 循环而不需要自己的 API key——它借用客户端的模型能力。

4. **Roots.** The set of URIs the server is allowed to touch. Client declares them; server respects them.
   中文翻译：**Roots。** 服务器被允许触及的 URI 集合。客户端声明它们；服务器遵守它们。
5. **Sampling.** Server requests the client's model to perform a completion. Enables server-hosted agent loops without server-side API keys.
   中文翻译：**Sampling。** 服务器请求客户端的模型执行一次补全。使服务器托管的 agent 循环无需服务器端 API 密钥。
6. **Elicitation.** Server asks the client's user for structured input mid-flight. Forms or URLs (SEP-1036).
   中文翻译：**Elicitation。** 服务器在执行过程中请求客户端用户输入结构化信息。表单或 URL（SEP-1036）。

> 🤔 **【困惑】** Q: Sampling 不就是服务器反过来调用客户端的模型吗？为什么不直接让服务器用自己的 API key？ A: 三个理由：(1) **成本归属**——API 调用费用算在用户头上，用户已经付费，不让用户重复付费；(2) **模型选择权**——用户用 Claude 还是 GPT 由用户决定，服务器不应该锁死；(3) **隐私**——服务器可能不可信，让它直接拿到 API key 等于把用户凭证外泄。Sampling 是"借用"客户端能力，权限边界清晰。

Every capability in MCP belongs to exactly one of these six. Phase 13 · 10 through 14 cover each in depth.

> MCP 中的每个能力恰好属于这六个之一。Phase 13 · 10 到 14 分别深入讲解。

### Wire format: JSON-RPC 2.0

> **【中文解读】** MCP 使用 JSON-RPC 2.0 作为线格式。三种消息类型：请求（有 id，需要响应）、响应（包含 result 或 error）、通知（无 id，不需要响应）。基础规范约 15 个方法，按原语分组：`initialize`/`initialized`、`tools/list`/`tools/call`、`resources/list`/`resources/read`、`prompts/list`/`prompts/get` 等。

Every message is a JSON object with these fields:

> 每条消息都是一个包含以下字段的 JSON 对象：

- Requests: `{jsonrpc: "2.0", id, method, params}`.
  中文翻译：请求：`{jsonrpc: "2.0", id, method, params}`。
- Responses: `{jsonrpc: "2.0", id, result | error}`.
  中文翻译：响应：`{jsonrpc: "2.0", id, result | error}`。
- Notifications: `{jsonrpc: "2.0", method, params}` — no `id`, no response expected.
  中文翻译：通知：`{jsonrpc: "2.0", method, params}`——无 `id`，不需要响应。

> ⚠️ **【易错点】** 场景：把通知当请求处理并回复响应 / 后果：客户端会忽略该响应（无 id），但若你在循环里"等待响应才继续"会导致死锁；或反之，把请求当通知不回 / 后果：客户端超时报错 / 修复：实现 dispatch 时先 `if "id" in msg` 判断分支；通知如 `notifications/initialized` 直接 ack 后丢弃，请求如 `tools/call` 必须以相同 id 回响应。

The base spec has ~15 methods, grouped by primitive. The important ones:

> 基础规范约 15 个方法，按原语分组。重要的有：

- `initialize` / `initialized` (handshake)
  中文翻译：`initialize` / `initialized`（握手）
- `tools/list`, `tools/call`
  中文翻译：`tools/list`、`tools/call`
- `resources/list`, `resources/read`, `resources/subscribe`
  中文翻译：`resources/list`、`resources/read`、`resources/subscribe`
- `prompts/list`, `prompts/get`
  中文翻译：`prompts/list`、`prompts/get`
- `sampling/createMessage` (server-to-client)
  中文翻译：`sampling/createMessage`（服务器到客户端）
- `notifications/tools/list_changed`, `notifications/resources/updated`, `notifications/progress`
  中文翻译：`notifications/tools/list_changed`、`notifications/resources/updated`、`notifications/progress`

### Three-phase lifecycle

> **【中文解读】** MCP 三阶段生命周期：(1) 初始化——客户端发送 `initialize` 携带 `capabilities` 和 `clientInfo`，服务器响应自己的 `capabilities`、`serverInfo` 和协议版本；(2) 操作——双向通信，客户端调用工具、读取资源，服务器可发采样请求和变更通知；(3) 关闭——任一方关闭传输层。

**Phase 1: initialize.**

> **阶段 1：初始化。**

Client sends `initialize` with its `capabilities` and `clientInfo`. Server responds with its own `capabilities`, `serverInfo`, and the spec version it speaks. Client sends `notifications/initialized` when it has digested the response. From here on, either side can send requests per the negotiated capabilities.

> 客户端发送 `initialize`，携带其 `capabilities` 和 `clientInfo`。服务器响应自己的 `capabilities`、`serverInfo` 和它支持的规范版本。客户端在消化响应后发送 `notifications/initialized`。从此以后，双方都可以根据协商的能力发送请求。

**Phase 2: operation.**

> **阶段 2：操作。**

Bidirectional. Client calls `tools/list` to discover, then `tools/call` to invoke. Server may send `sampling/createMessage` if it declared that capability. Server may send `notifications/tools/list_changed` when its tool set mutates. Client may send `notifications/roots/list_changed` when the user changes root scope.

> 双向通信。客户端调用 `tools/list` 发现工具，然后 `tools/call` 调用。如果服务器声明了该能力，可以发送 `sampling/createMessage`。服务器在工具集变更时可发送 `notifications/tools/list_changed`。客户端在用户更改根范围时可发送 `notifications/roots/list_changed`。

**Phase 3: shutdown.**

> **阶段 3：关闭。**

Either side closes the transport. No structured shutdown method in MCP; the transport (stdio or Streamable HTTP, Phase 13 · 09) carries the end-of-connection signal.

> 任一方关闭传输层。MCP 没有结构化的关闭方法；传输层（stdio 或 Streamable HTTP，Phase 13 · 09）承载连接结束信号。

### Capability negotiation

`capabilities` in the `initialize` handshake is the contract. Example from a server:

> `initialize` 握手中的 `capabilities` 是契约。来自服务器的示例：

```json
{
  "tools": {"listChanged": true},
  "resources": {"subscribe": true, "listChanged": true},
  "prompts": {"listChanged": true}
}
```

The server declares it can emit `tools/list_changed` notifications and supports `resources/subscribe`. The client agrees by declaring its own:

> 服务器声明它可以发出 `tools/list_changed` 通知并支持 `resources/subscribe`。客户端通过声明自己的能力来同意：

```json
{
  "roots": {"listChanged": true},
  "sampling": {},
  "elicitation": {}
}
```

If the client does not declare `sampling`, the server must not call `sampling/createMessage`. Symmetric: if the server does not declare `resources.subscribe`, the client must not try to subscribe.

> 如果客户端不声明 `sampling`，服务器不得调用 `sampling/createMessage`。对称地：如果服务器不声明 `resources.subscribe`，客户端不得尝试订阅。

This is what prevents ecosystem drift. A client that does not support sampling is still a valid MCP client; a server that does not call `sampling` is still a valid MCP server. They just do not use that feature together.

> 这就是防止生态系统漂移的机制。不支持 sampling 的客户端仍是合法的 MCP 客户端；不调用 `sampling` 的服务器仍是合法的 MCP 服务器。它们只是不一起使用那个特性。

> **【中文解读】** 能力协商是 MCP 防止生态漂移的关键机制。不支持 sampling 的客户端仍是合法 MCP 客户端；不调用 sampling 的服务器仍是合法 MCP 服务器。它们只是不一起使用那个特性。对称性：服务器不声明 `resources.subscribe`，客户端就不能订阅。

### Structured content and error shapes

`tools/call` returns a `content` array of typed blocks: `text`, `image`, `resource`. Phase 13 · 14 adds MCP Apps (`ui://` interactive UI) to that list.

> `tools/call` 返回一个类型化块的 `content` 数组：`text`、`image`、`resource`。Phase 13 · 14 将 MCP Apps（`ui://` 交互式 UI）添加到该列表。

Errors use JSON-RPC error codes. The spec-defined additions: `-32002` "Resource not found", `-32603` "Internal error", plus MCP-specific error data as `error.data`.

> 错误使用 JSON-RPC 错误码。规范定义的补充：`-32002`"资源未找到"、`-32603`"内部错误"，加上 MCP 特定的错误数据作为 `error.data`。

### Client capabilities vs tool call details

A common confusion: `capabilities.tools` is whether the client supports tool-list-changed notifications. Whether the client WILL call specific tools is a runtime choice driven by its model, not a capability flag. The capability flag is the spec-level contract. The model's choice is orthogonal.

> 一个常见的混淆：`capabilities.tools` 是客户端是否支持工具列表变更通知。客户端是否调用特定工具是由其模型驱动的运行时选择，而非能力标志。能力标志是规范级别的契约。模型的选择是正交的。

### Why JSON-RPC and not REST?

> **【拓展：MCP 为什么选择 JSON-RPC 而非 REST】** JSON-RPC 2.0 是轻量级双向协议（2010年标准）。REST 是客户端发起的单向协议。MCP 需要服务器主动发起消息（sampling、notifications），JSON-RPC 的对称请求/响应形状天然适合。JSON-RPC 还可以在 stdio 和 WebSocket/Streamable HTTP 上干净地组合，无需重新发明 HTTP 请求格式。

JSON-RPC 2.0 (2010) is a lightweight bidirectional protocol. REST is client-initiated. MCP needed server-initiated messages (sampling, notifications), so JSON-RPC with its symmetric request/response shape was a natural fit. JSON-RPC also composes cleanly over stdio and WebSocket/Streamable HTTP without re-inventing HTTP's request shape.

> JSON-RPC 2.0（2010）是轻量级双向协议。REST 是客户端发起的。MCP 需要服务器主动发起消息（sampling、通知），因此具有对称请求/响应形状的 JSON-RPC 是自然之选。JSON-RPC 还可以在 stdio 和 WebSocket/Streamable HTTP 上干净地组合，无需重新发明 HTTP 的请求格式。

## Use It | 用框架实现

`code/main.py` ships a minimal JSON-RPC 2.0 parser and emitter, then walks the `initialize` → `tools/list` → `tools/call` → `shutdown` sequence by hand, printing every message. No real transport; just the message shapes. Compare to the spec linked in Further Reading to verify each envelope.

> `code/main.py` 提供了一个最小的 JSON-RPC 2.0 解析器和发射器，然后手动走完 `initialize` → `tools/list` → `tools/call` → `shutdown` 序列，打印每条消息。没有真实传输；只有消息格式。与延伸阅读中链接的规范进行比较以验证每个信封。

What to look at:

> 需要关注的点：

- `initialize` declares capabilities both ways; the response has `serverInfo` and `protocolVersion: "2025-11-25"`.
  中文翻译：`initialize` 双向声明能力；响应包含 `serverInfo` 和 `protocolVersion: "2025-11-25"`。
- `tools/list` returns a `tools` array; each entry has `name`, `description`, `inputSchema`.
  中文翻译：`tools/list` 返回一个 `tools` 数组；每个条目有 `name`、`description`、`inputSchema`。
- `tools/call` uses `params.name` and `params.arguments`.
  中文翻译：`tools/call` 使用 `params.name` 和 `params.arguments`。
- The response `content` is an array of `{type, text}` blocks.
  中文翻译：响应的 `content` 是一个 `{type, text}` 块数组。

## Ship It | 产出物

This lesson produces `outputs/skill-mcp-handshake-tracer.md`. Given a pcap-style transcript of an MCP client-server interaction, the skill annotates each message with which primitive, which lifecycle phase, and which capability it depends on.

> 本课产出 `outputs/skill-mcp-handshake-tracer.md`。给定一个 MCP 客户端-服务器交互的 pcap 风格转录，该 skill 为每条消息标注它属于哪个原语、哪个生命周期阶段以及依赖哪个能力。

## Exercises | 练习题

1. Run `code/main.py`. Identify the line where capability negotiation happens and describe what would change if the server did not declare `tools.listChanged`.
   中文翻译：运行 `code/main.py`。找出能力协商发生的行，描述如果服务器不声明 `tools.listChanged` 会发生什么变化。

2. Extend the parser to handle `notifications/progress`. The message shape: `{method: "notifications/progress", params: {progressToken, progress, total}}`. Emit it while a long-running `tools/call` is in progress and confirm the client handler would display a progress bar.
   中文翻译：扩展解析器以处理 `notifications/progress`。消息格式：`{method: "notifications/progress", params: {progressToken, progress, total}}`。在一个长时间运行的 `tools/call` 进行中时发出它，确认客户端处理器会显示进度条。

3. Read the MCP 2025-11-25 spec top to bottom — the whole document is about 80 pages. Identify the one capability flag most servers do NOT need. Hint: it relates to resource subscription.
   中文翻译：从头到尾阅读 MCP 2025-11-25 规范——整个文档约 80 页。找出大多数服务器不需要的一个能力标志。提示：它与资源订阅有关。

4. Sketch on paper the primitive a hypothetical "cron job" feature would belong to. (Hint: the server wants the client to invoke it at a scheduled time. None of the six primitives fit today.) MCP's 2026 roadmap has a draft SEP for this.
   中文翻译：在纸上勾勒一个假设的"定时任务"功能属于哪个原语。（提示：服务器希望客户端在预定时间调用它。目前六个原语都不适合。）MCP 的 2026 路线图有一个草案 SEP。

5. Parse one session log from an open MCP server on GitHub. Count request vs response vs notification messages. Compute what fraction of traffic is lifecycle vs operation.
   中文翻译：解析 GitHub 上一个开源 MCP 服务器的会话日志。统计请求、响应和通知消息的数量。计算生命周期流量与操作流量的比例。

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
  中文翻译：权威规范文档
- [Model Context Protocol — Architecture concepts](https://modelcontextprotocol.io/docs/concepts/architecture) — the six-primitive mental model
  中文翻译：六原语心智模型
- [Anthropic — Introducing the Model Context Protocol](https://www.anthropic.com/news/model-context-protocol) — November 2024 launch post
  中文翻译：2024 年 11 月发布公告
- [MCP blog — First MCP anniversary](https://blog.modelcontextprotocol.io/posts/2025-11-25-first-mcp-anniversary/) — one-year retrospective and the 2025-11-25 spec changes
  中文翻译：一周年回顾和 2025-11-25 规范变更
- [WorkOS — MCP 2025-11-25 spec update](https://workos.com/blog/mcp-2025-11-25-spec-update) — summary of SEP-1686, 1036, 1577, 835, and 1724
  中文翻译：SEP-1686、1036、1577、835 和 1724 的摘要
