# MCP 基础 — 原语、生命周期与 JSON-RPC

> MCP 之前的每个集成都是定制的。Model Context Protocol 由 Anthropic 于 2024 年 11 月首发，现由 Linux 基金会的 Agentic AI Foundation 管理，标准化了发现和调用，使任何客户端能与任何服务器通信。2025-11-25 规范定义了六个原语（三个服务器端、三个客户端端）、三阶段生命周期和 JSON-RPC 2.0 线格式。掌握这些，Phase 13 的 MCP 章节其余部分就变成阅读。

> **【中文解读】** MCP 之前的每个集成都是定制的。Model Context Protocol 由 Anthropic 于 2024 年 11 月首发，现由 Linux 基金会的 Agentic AI Foundation 管理。它标准化了发现和调用，使任何客户端能与任何服务器通信。2025-11-25 规范定义了六个原语（三个服务器端、三个客户端端）、三阶段生命周期和 JSON-RPC 2.0 线格式。

> **【拓展：MCP→Claude 协议生态】** MCP 是 Claude 生态的核心协议。Claude Desktop、Cursor、VS Code Copilot 等 300+ 客户端都支持 MCP。一个 MCP 服务器可以在所有这些客户端中工作，无需重复开发。MCP 的六原语模型（tools/resources/prompts + roots/sampling/elicitation）是理解整个协议的基础。

**类型：** 学习
**语言：** Python（标准库，JSON-RPC 解析器）
**前置条件：** Phase 13 · 01-05（工具接口和函数调用）
**时间：** 约 45 分钟

## 学习目标

- 说出所有六个 MCP 原语（服务器端的 tools、resources、prompts；客户端端的 roots、sampling、elicition）并为每个给出一个用例。
- 走通三阶段生命周期（初始化、操作、关闭）并说明每个阶段谁发送什么消息。
- 解析和发出 JSON-RPC 2.0 请求、响应和通知信封。
- 解释 `initialize` 时的能力协商是什么以及没有它会出什么问题。

## 问题引入

MCP 之前，每个使用工具的 Agent 都有自己的协议。Cursor 有一个类似 MCP 但不兼容的工具系统。Claude Desktop 提供了不同的一个。VS Code 的 Copilot 扩展有第三个。一个构建"Postgres 查询"工具的团队将同一个工具写三次，每次对应不同的宿主 API。复用它需要复制代码。

结果是定制集成的大爆发和生态系统速度的天花板。

MCP 通过标准化线格式解决了这个问题。一个 MCP 服务器在每个 MCP 客户端中工作：Claude Desktop、ChatGPT、Cursor、VS Code、Gemini、Goose、Zed、Windsurf，截至 2026 年 4 月已有 300+ 客户端。月 SDK 下载 1.1 亿次。1 万+ 公开服务器。Linux 基金会于 2025 年 12 月在新的 Agentic AI Foundation 下接管了管理工作。

本阶段使用的规范修订版是 **2025-11-25**。它添加了异步 Tasks（SEP-1686）、URL 模式 elicitation（SEP-1036）、带工具的 sampling（SEP-1577）、增量范围同意（SEP-835）和 OAuth 2.1 资源指示器语义。Phase 13 · 09-16 覆盖这些扩展。本课止步于基础。

## 核心概念

### 三个服务器原语

1. **Tools。** 可调用动作。与 Phase 13 · 01 的四步循环相同。
2. **Resources。** 暴露的数据。通过 URI 寻址的只读内容：`file:///path`、`db://query/...`、自定义方案。
3. **Prompts。** 可复用模板。宿主 UI 中的斜杠命令；服务器提供模板，客户端填充参数。

### 三个客户端原语

4. **Roots。** 服务器被允许触碰的 URI 集合。客户端声明它们；服务器遵守。
5. **Sampling。** 服务器请求客户端的模型执行补全。使服务器能承载 Agent 循环而无需服务器端 API 密钥。
6. **Elicitation。** 服务器在飞行途中向客户端用户请求结构化输入。表单或 URL（SEP-1036）。

MCP 中的每个能力恰好属于这六个之一。Phase 13 · 10-14 深入覆盖每一个。

### 线格式：JSON-RPC 2.0

每条消息都是一个 JSON 对象，包含以下字段：

- 请求：`{jsonrpc: "2.0", id, method, params}`。
- 响应：`{jsonrpc: "2.0", id, result | error}`。
- 通知：`{jsonrpc: "2.0", method, params}` — 无 `id`，不期望响应。

基础规范约有 15 个方法，按原语分组。重要的有：

- `initialize` / `initialized`（握手）
- `tools/list`、`tools/call`
- `resources/list`、`resources/read`、`resources/subscribe`
- `prompts/list`、`prompts/get`
- `sampling/createMessage`（服务器到客户端）
- `notifications/tools/list_changed`、`notifications/resources/updated`、`notifications/progress`

### 三阶段生命周期

**阶段 1：初始化。**

客户端发送带有 `capabilities` 和 `clientInfo` 的 `initialize`。服务器响应自己的 `capabilities`、`serverInfo` 和它支持的规范版本。客户端在消化响应后发送 `notifications/initialized`。此后，任一方可以根据协商的能力发送请求。

**阶段 2：操作。**

双向通信。客户端调用 `tools/list` 发现工具，然后 `tools/call` 调用。服务器如果声明了该能力，可发送 `sampling/createMessage`。服务器在其工具集变化时可发送 `notifications/tools/list_changed`。客户端在用户更改根范围时可发送 `notifications/roots/list_changed`。

**阶段 3：关闭。**

任一方关闭传输层。MCP 中无结构化关闭方法；传输层（stdio 或 Streamable HTTP，Phase 13 · 09）携带连接结束信号。

### 能力协商

`initialize` 握手中的 `capabilities` 就是契约。服务器示例：

```json
{
  "tools": {"listChanged": true},
  "resources": {"subscribe": true, "listChanged": true},
  "prompts": {"listChanged": true}
}
```

服务器声明它可以发出 `tools/list_changed` 通知并支持 `resources/subscribe`。客户端通过声明自己的能力来同意：

```json
{
  "roots": {"listChanged": true},
  "sampling": {},
  "elicitation": {}
}
```

如果客户端不声明 `sampling`，服务器就不能调用 `sampling/createMessage`。对称地：如果服务器不声明 `resources.subscribe`，客户端就不能尝试订阅。

这就是 MCP 防止生态漂移的机制。不支持 sampling 的客户端仍是合法 MCP 客户端；不调用 sampling 的服务器仍是合法 MCP 服务器。它们只是不一起使用那个特性。

### 结构化内容和错误形状

`tools/call` 返回一个类型化块的 `content` 数组：`text`、`image`、`resource`。Phase 13 · 14 将 MCP Apps（`ui://` 交互式 UI）添加到该列表。

错误使用 JSON-RPC 错误码。规范定义的附加码：`-32002` "Resource not found"、`-32603` "Internal error"，加上 MCP 特定的错误数据作为 `error.data`。

### 为什么用 JSON-RPC 而非 REST？

JSON-RPC 2.0（2010年）是轻量级双向协议。REST 是客户端发起的单向协议。MCP 需要服务器发起的消息（sampling、notifications），因此具有对称请求/响应形状的 JSON-RPC 是天然选择。JSON-RPC 还可以在 stdio 和 WebSocket/Streamable HTTP 上干净地组合，无需重新发明 HTTP 的请求格式。

## 用框架实现

`code/main.py` 提供了一个最小的 JSON-RPC 2.0 解析器和发射器，然后手动走通 `initialize` → `tools/list` → `tools/call` → `shutdown` 序列，打印每条消息。无真实传输层；只有消息形状。与延伸阅读中链接的规范比较以验证每个信封。

关注点：

- `initialize` 双向声明能力；响应有 `serverInfo` 和 `protocolVersion: "2025-11-25"`。
- `tools/list` 返回 `tools` 数组；每个条目有 `name`、`description`、`inputSchema`。
- `tools/call` 使用 `params.name` 和 `params.arguments`。
- 响应 `content` 是 `{type, text}` 块的数组。

## 产出物

本课产生 `outputs/skill-mcp-handshake-tracer.md`。给定一份 pcap 风格的 MCP 客户端-服务器交互记录，该技能标注每条消息属于哪个原语、哪个生命周期阶段以及依赖哪个能力。

## 练习题

1. 运行 `code/main.py`。识别能力协商发生的位置，描述如果服务器不声明 `tools.listChanged` 会改变什么。

2. 扩展解析器以处理 `notifications/progress`。消息形状：`{method: "notifications/progress", params: {progressToken, progress, total}}`。在长时间运行的 `tools/call` 进行中发出它，确认客户端处理器会显示进度条。

3. 从头到尾阅读 MCP 2025-11-25 规范——整个文档约 80 页。识别大多数服务器不需要的一个能力标志。提示：与资源订阅有关。

4. 在纸上勾画一个假设的"cron job"功能应该属于哪个原语。（提示：服务器希望客户端在计划时间调用它。目前六个原语都不适合。）MCP 的 2026 年路线图有这方面的草案 SEP。

5. 从 GitHub 上的一个开放 MCP 服务器解析一个会话日志。计算请求 vs 响应 vs 通知消息的数量。计算生命周期 vs 操作的流量比例。

## 术语速查表

| 术语 | 人们怎么说 | 实际含义 | 英文 |
|------|-----------|---------|------|
| MCP | "Model Context Protocol" | 用于模型到工具发现和调用的开放协议 | 模型上下文协议 |
| 服务器原语 | "服务器暴露什么" | tools（动作）、resources（数据）、prompts（模板） | Server primitive |
| 客户端原语 | "客户端让服务器使用什么" | roots（范围）、sampling（LLM 回调）、elicitation（用户输入） | Client primitive |
| JSON-RPC 2.0 | "线格式" | 对称的请求/响应/通知信封 | JSON-RPC 2.0 |
| `initialize` 握手 | "能力协商" | 第一对消息；服务器和客户端声明支持的功能 | Initialize handshake |
| `tools/list` | "发现" | 客户端向服务器请求当前工具集 | Discovery |
| `tools/call` | "调用" | 客户端请求服务器用参数执行工具 | Invocation |
| `notifications/*_changed` | "变更事件" | 服务器告知客户端其原语列表已变化 | Mutation events |
| 内容块 | "类型化结果" | 工具结果中的 `{type: "text" | "image" | "resource" | "ui_resource"}` | Content block |
| SEP | "规范演进提案" | 命名的草案提案（如 SEP-1686 用于异步 Tasks） | Spec Evolution Proposal |

## 延伸阅读

- [Model Context Protocol — Specification 2025-11-25](https://modelcontextprotocol.io/specification/2025-11-25) — 权威规范文档
- [Model Context Protocol — Architecture concepts](https://modelcontextprotocol.io/docs/concepts/architecture) — 六原语心智模型
- [Anthropic — Introducing the Model Context Protocol](https://www.anthropic.com/news/model-context-protocol) — 2024 年 11 月发布文章
- [MCP blog — First MCP anniversary](https://blog.modelcontextprotocol.io/posts/2025-11-25-first-mcp-anniversary/) — 一周年回顾和 2025-11-25 规范变更
- [WorkOS — MCP 2025-11-25 spec update](https://workos.com/blog/mcp-2025-11-25-spec-update) — SEP-1686、1036、1577、835 和 1724 的摘要
