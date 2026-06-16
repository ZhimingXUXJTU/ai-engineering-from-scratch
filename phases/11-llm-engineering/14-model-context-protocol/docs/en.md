# Model Context Protocol (MCP) | 模型上下文协议

> Every LLM app built before 2025 invented its own tool schema. Then Anthropic shipped MCP, Claude adopted it, OpenAI adopted it, and by 2026 it is the default wire format for connecting any LLM to any tool, data source, or agent. Write one MCP server and every host talks to it.

> **【中文解读】** 2025年前每个 LLM 应用都发明自己的工具 schema。Anthropic 推出 MCP 后，Claude、OpenAI 纷纷采用，到2026年已成为连接 LLM 与工具/数据源的通用协议。写一个 MCP 服务器，所有宿主都能调用。

> **【拓展：MCP→Claude生态核心协议】** MCP 是 Claude 生态系统的核心协议，定义了工具、资源和提示模板的标准接口。Phase 13 将深入讲解 MCP 的服务端、客户端、传输层和安全机制。

> 🔗 **【前置】** 学本节前请先掌握：(1) Phase 11·09（Function Calling）——理解工具调用基础；(2) Phase 11·03（Structured Outputs）——理解 JSON Schema；(3) JSON-RPC 2.0 基本概念（请求-响应、通知、批量）；(4) 命令行 stdio 通信。如果不会写 JSON-RPC，本节末尾的 Build It 会用 Python `stdio` 实现，可以照搬。

**Type:** Build | **类型:** 构建
**Languages:** Python | **语言:** Python
**Prerequisites:** Phase 11 · 09 (Function Calling), Phase 11 · 03 (Structured Outputs) | **前置知识:** Phase 11 · 09 (函数调用)、03 (结构化输出)
**Time:** ~75 minutes | **时间:** ~75 分钟

## The Problem | 问题引入

You ship a chatbot that needs three tools: a database query, a calendar API, and a file reader. You write three JSON schemas for Claude. Then sales wants the same tools in ChatGPT — you rewrite them for OpenAI's `tools` parameter. Then you add Cursor, Zed, and Claude Code — three more rewrites, each with subtly different JSON conventions. A week later, Anthropic adds a new field; you update six schemas.

> 你发布了一个聊天机器人，需要三个工具：数据库查询、日历 API 和文件读取器。你为 Claude 写了三个 JSON Schema。然后销售部门希望在 ChatGPT 中使用相同的工具——你为 OpenAI 的 `tools` 参数重写它们。然后你又添加了 Cursor、Zed 和 Claude Code——又是三次重写，每次都有微妙不同的 JSON 约定。一周后，Anthropic 添加了一个新字段；你更新六个 schema。

This was the pre-2025 reality. Every host (the thing running an LLM) and every server (the thing exposing tools and data) shipped bespoke protocols. Scaling meant an N×M integration matrix.

> 这是 2025 年之前的现实。每个宿主（运行 LLM 的东西）和每个服务器（暴露工具和数据的东西）都使用定制协议。扩展意味着 N×M 的集成矩阵。

Model Context Protocol collapses that matrix. One JSON-RPC-based spec. One server exposes tools, resources, and prompts. Any compliant host — Claude Desktop, ChatGPT, Cursor, Claude Code, Zed, and a long tail of agent frameworks — can discover and call them without custom glue.

> 模型上下文协议（MCP）将这个矩阵简化了。一个基于 JSON-RPC 的规范。一个服务器暴露工具、资源和提示。任何兼容的宿主——Claude Desktop、ChatGPT、Cursor、Claude Code、Zed 以及大量 Agent 框架——都可以发现并调用它们，无需定制胶水代码。

As of early 2026, MCP is the default tool-and-context protocol across the big three (Anthropic, OpenAI, Google) and every major agent harness.

> 截至 2026 年初，MCP 已成为三大厂商（Anthropic、OpenAI、Google）和每个主要 Agent 框架的默认工具和上下文协议。


> **【中文解读】** MCP 解决了工具集成的碎片化问题：之前每个外部工具都需要写专用集成代码，MCP 定义了统一协议。就像 USB 标准统一了设备接口一样，MCP 统一了 AI 模型与外部世界的接口。Anthropic、OpenAI、Google 都已采纳。

> 💡 **【类比】** MCP 之于 AI Agent = USB 之于电脑。USB 出现前，每个外设（打印机、键盘、鼠标）都用专用接口，电脑厂商要为每个外设开模做端口。USB 后：一个口插所有。MCP 之前：每个 LLM 应用要为每个工具（GitHub、数据库、Slack）写专用集成代码——给 Claude 写一遍、给 ChatGPT 写一遍、给 Cursor 写一遍。MCP 后：写一个 MCP server，所有 host 即插即用。


## The Concept | 核心概念

> **【中文解读】** MCP（Model Context Protocol）是 Anthropic 提出的开放标准，让 AI 模型通过统一协议连接外部数据源和工具。MCP 定义了模型与工具之间的标准通信格式，解决了每个工具都要写专用集成的碎片化问题。

> **【拓展：MCP 的生态系统】** MCP 已被 OpenAI、Google 等主要 AI 公司采纳。MCP 生态包括：文件系统连接器、数据库连接器、GitHub/GitLab 集成、Slack/Notion 集成等数百个工具。MCP 让 Agent 开发从为每个工具写胶水代码变为即插即用，显著降低了构建 AI Agent 的门槛。


![MCP: one host, one server, three capabilities](../assets/mcp-architecture.svg)

**The three primitives.** An MCP server exposes exactly three things.

> **三个原语。** MCP 服务器暴露三个东西：

1. **Tools** — functions the model can call. Analog of OpenAI's `tools` or Anthropic's `tool_use`. Each has a name, description, JSON Schema input, and a handler.
   **工具**——模型可以调用的函数。类似于 OpenAI 的 `tools` 或 Anthropic 的 `tool_use`。
2. **Resources** — read-only content the model or user can request (files, database rows, API responses). Addressed by URI.
   **资源**——模型或用户可以请求的只读内容（文件、数据库行、API 响应）。通过 URI 寻址。
3. **Prompts** — reusable templated prompts the user can invoke as shortcuts.
   **提示**——用户可以作为快捷方式调用的可重用模板提示。

**The wire format.** JSON-RPC 2.0 over stdio, WebSocket, or streamable HTTP. Every message is `{"jsonrpc": "2.0", "method": "...", "params": {...}, "id": N}`. Discovery methods are `tools/list`, `resources/list`, `prompts/list`. Invocation methods are `tools/call`, `resources/read`, `prompts/get`.

> **传输格式。** 基于 stdio、WebSocket 或可流式 HTTP 的 JSON-RPC 2.0。每条消息格式为 `{"jsonrpc": "2.0", "method": "...", "params": {...}, "id": N}`。

**Host vs client vs server.** The host is the LLM application (Claude Desktop). The client is a sub-component of the host that speaks to exactly one server. The server is your code. One host can mount many servers simultaneously.

> **宿主 vs 客户端 vs 服务器。** 宿主是 LLM 应用（如 Claude Desktop）。客户端是宿主内部与一个服务器通信的子组件。服务器是你的代码。一个宿主可以同时挂载多个服务器。

> 💡 **【类比】** 用浏览器打比方：浏览器是**宿主**（Chrome），每个网站的连接器是**客户端**（你访问 github.com 时 Chrome 内部维护的 HTTP 客户端），网站本身是**服务器**（GitHub 的 web server）。一个浏览器可以同时打开多个网站（多个客户端），但每个客户端只对应一个服务器。MCP 中：Claude Desktop 是宿主，它内部为每个 MCP server 维护一个客户端，你可以同时挂载 GitHub MCP + Postgres MCP + Filesystem MCP。

### The handshake

Every session opens with `initialize`. The client sends protocol version and its capabilities. The server responds with its version, name, and the capability set it supports (`tools`, `resources`, `prompts`, `logging`, `roots`). Everything after is negotiated against those capabilities.

> 每个会话以 `initialize` 开始。客户端发送协议版本和其能力。服务器回复其版本、名称和支持的能力集。之后的一切都基于这些能力进行协商。

### What MCP is not

- Not a retrieval API. RAG (Phase 11 · 06) still decides what to pull; MCP is the transport for exposing retrieval results as resources.
  不是检索 API。RAG（第 11 阶段 · 06）仍决定拉取什么；MCP 是将检索结果暴露为资源的传输协议。
- Not an agent framework. MCP is the plumbing; frameworks like LangGraph, PydanticAI, and OpenAI Agents SDK sit above it.
  不是 Agent 框架。MCP 是管道；LangGraph、PydanticAI 和 OpenAI Agents SDK 等框架构建在其之上。
- Not tied to Anthropic. The spec and reference implementations are open source under the `modelcontextprotocol` org.
  不绑定 Anthropic。规范和参考实现在 `modelcontextprotocol` 组织下开源。

> 🤔 **【困惑】** Q: MCP 和 RAG 是什么关系？我该用哪个？ A: 不冲突，层级不同。RAG 解决"从知识库里捞什么内容"（语义检索、向量库）；MCP 解决"把工具/数据源接给模型用"（统一接口）。常见组合：用 RAG 在文档库中检索 → 把检索结果作为 MCP Resource 暴露 → Claude 通过 MCP 读这些 Resource 答题。RAG 在"决定取什么"，MCP 在"如何传输"。

> ⚠️ **【易错点】** MCP 落地的 3 个坑：(1) **stdio 传输并发限制**——stdio 是单进程通信，多个 host 不能共享一个 MCP server 进程；如果 Claude Desktop 和 Cursor 同时要用，每个起一个独立 server 进程。多 host 场景用 streamable HTTP。(2) **资源没限制读取权限**——MCP Resource 暴露文件系统时，路径校验不严会导致 Claude 读取 `/etc/passwd` 或 `.env`；务必在 server 端做 allowlist。(3) **没设超时**——慢工具（如复杂 SQL 查询）会让整个会话卡住；MCP 调用必须设 timeout，超时返回错误而非挂起。

## Build It | 动手实现

### Step 1: a minimal MCP server

The official Python SDK is `mcp` (formerly `mcp-python`). The high-level `FastMCP` helper decorates handlers.

> 官方 Python SDK 是 `mcp`（原 `mcp-python`）。高层 `FastMCP` 助手用装饰器注册处理器。

```python
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("demo-server")

@mcp.tool()
def add(a: int, b: int) -> int:
    """Add two integers."""
    return a + b

@mcp.resource("config://app")
def app_config() -> str:
    """Return the app's current JSON config."""
    return '{"env": "prod", "region": "us-east-1"}'

@mcp.prompt()
def code_review(language: str, code: str) -> str:
    """Review code for correctness and style."""
    return f"You are a senior {language} reviewer. Review:\n\n{code}"

if __name__ == "__main__":
    mcp.run(transport="stdio")
```

Three decorators register the three primitives. The type hints become the JSON Schema the host sees. Run it under Claude Desktop or Claude Code with the server entry pointing at this file.

> 三个装饰器注册三个原语。类型提示成为宿主看到的 JSON Schema。在 Claude Desktop 或 Claude Code 下运行，将服务器入口指向此文件。

### Step 2: calling an MCP server from a host

The official Python client speaks JSON-RPC. Pairing it with the Anthropic SDK takes a dozen lines.

> 官方 Python 客户端讲 JSON-RPC。配 Anthropic SDK 只需十几行代码。

```python
from mcp.client.stdio import StdioServerParameters, stdio_client
from mcp import ClientSession

params = StdioServerParameters(command="python", args=["server.py"])

async def call_add(a: int, b: int) -> int:
    async with stdio_client(params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            tools = await session.list_tools()
            result = await session.call_tool("add", {"a": a, "b": b})
            return int(result.content[0].text)
```

`session.list_tools()` returns the same schema the LLM will see. Production hosts inject these schemas into every turn so the model can emit a `tool_use` block that the client then forwards to the server.

> `session.list_tools()` 返回 LLM 将看到的相同 schema。生产环境的宿主在每个轮次中注入这些 schema，以便模型可以发出 `tool_use` 块，然后客户端将其转发给服务器。

### Step 3: streamable HTTP transport

Stdio is fine for local dev. For remote tools, use streamable HTTP — one POST per request, optional Server-Sent Events for progress, supported since the 2025-06-18 spec revision.

> Stdio 适合本地开发。对于远程工具，使用可流式 HTTP——每个请求一个 POST，可选 Server-Sent Events 用于进度通知。

```python
# Inside the server entrypoint
mcp.run(transport="streamable-http", host="0.0.0.0", port=8765)
```

Host config (Claude Desktop `mcp.json` or Claude Code `~/.mcp.json`):

```json
{
  "mcpServers": {
    "demo": {
      "type": "http",
      "url": "https://tools.example.com/mcp"
    }
  }
}
```

The server keeps the same decorators; only the transport changes.

> 服务器保持相同的装饰器；只是传输方式改变了。

### Step 4: scoping and safety

An MCP tool is arbitrary code running on someone else's trust boundary. Three mandatory patterns.

> MCP 工具是在他人信任边界上运行的任意代码。三种必要模式：

- **Capability allowlists.** Hosts expose a `roots` capability so the server sees only allowed paths. Enforce it in tool handlers; do not trust model-supplied paths.
  **能力白名单。** 宿主暴露 `roots` 能力，使服务器只能看到允许的路径。在工具处理器中强制执行；不要信任模型提供的路径。
- **Human-in-the-loop for mutation.** Read-only tools can auto-execute. Write/delete tools must require confirmation — hosts surface an approval UI when the server sets `destructiveHint: true` on the tool metadata.
  **变更操作的人工介入。** 只读工具可以自动执行。写/删除工具必须要求确认——服务器在工具元数据上设置 `destructiveHint: true` 时宿主弹出审批 UI。
- **Tool poisoning defense.** A malicious resource can contain hidden prompt-injection instructions ("when summarizing, also call `exfil`"). Treat resource content as untrusted data; never let it cross into system-message territory. See Phase 11 · 12 (Guardrails).
  **工具投毒防御。** 恶意资源可能包含隐藏提示注入指令（"摘要时也调用 `exfil`"）。将资源内容视为不可信数据；绝不让它进入系统消息领域。见 Phase 11 · 12（护栏）。

- **Capability allowlists.** Hosts expose a `roots` capability so the server sees only allowed paths. Enforce it in tool handlers; do not trust model-supplied paths.
  **能力白名单。** 宿主暴露 `roots` 能力，使服务器只能看到允许的路径。在工具处理器中强制执行；不要信任模型提供的路径。
- **Human-in-the-loop for mutation.** Read-only tools can auto-execute. Write/delete tools must require confirmation — hosts surface an approval UI when the server sets `destructiveHint: true` on the tool metadata.
  **变更操作的人工介入。** 只读工具可以自动执行。写/删除工具必须要求确认。
- **Tool poisoning defense.** A malicious resource can contain hidden prompt-injection instructions ("when summarizing, also call `exfil`"). Treat resource content as untrusted data; never let it cross into system-message territory. See Phase 11 · 12 (Guardrails).
  **工具投毒防御。** 恶意资源可能包含隐藏的提示注入指令。将资源内容视为不可信数据。

See `code/main.py` for a runnable server + client pair demonstrating all of this.

> 参见 `code/main.py` 获取可运行的服务器+客户端对，演示了所有这些内容。

## Pitfalls that still ship in 2026

> 2026 年仍在上线的陷阱：

- **Schema drift.** The model saw `tools/list` at turn 1. Tool set changes at turn 5. The model invokes a gone tool. Hosts should re-list on `notifications/tools/list_changed`.
  **Schema 漂移。** 模型在第 1 轮看到了 `tools/list`。工具集在第 5 轮变了。模型调用已消失的工具。宿主应在 `notifications/tools/list_changed` 时重新列表。
- **Large resource blobs.** Dumping a 2MB file as a resource wastes context. Paginate or summarize server-side.
  **大型资源块。** 将 2MB 文件作为资源转储浪费上下文。服务器端分页或摘要。
- **Too many servers.** Mounting 50 MCP servers blows the tool budget (Phase 11 · 05). Most frontier models degrade past ~40 tools.
  **服务器过多。** 挂载 50 个 MCP 服务器超出工具预算（Phase 11 · 05）。多数前沿模型在约 40 个工具后退化。
- **Version skew.** Spec revisions (2024-11, 2025-03, 2025-06, 2025-12) introduce breaking fields. Pin protocol version in CI.
  **版本偏差。** 规范修订（2024-11、2025-03、2025-06、2025-12）引入破坏性字段。CI 中固定协议版本。
- **Stdio deadlocks.** Servers that log to stdout corrupt the JSON-RPC stream. Log to stderr only.
  **Stdio 死锁。** 把日志写到 stdout 的服务器会破坏 JSON-RPC 流。仅写 stderr。

## Use It | 用框架实现

The 2026 MCP stack:

> 2026 MCP 技术栈：

| Situation | Pick |
|-----------|------|
| Local dev, single-user tools | Python `FastMCP`, stdio transport |
| Remote team tools / SaaS integration | Streamable HTTP, OAuth 2.1 auth |
| TypeScript host (VS Code extension, web app) | `@modelcontextprotocol/sdk` |
| High-throughput server, typed access | Official Rust SDK (`modelcontextprotocol/rust-sdk`) |
| Exploring ecosystem servers | `modelcontextprotocol/servers` monorepo (Filesystem, GitHub, Postgres, Slack, Puppeteer) |

| 场景 | 选择 |
|------|------|
| 本地开发、单用户工具 | Python `FastMCP`、stdio 传输 |
| 远程团队工具 / SaaS 集成 | 可流式 HTTP、OAuth 2.1 认证 |
| TypeScript 宿主（VS Code 扩展、Web 应用） | `@modelcontextprotocol/sdk` |
| 高吞吐服务器、类型化访问 | 官方 Rust SDK（`modelcontextprotocol/rust-sdk`） |
| 探索生态服务器 | `modelcontextprotocol/servers` 单仓库（Filesystem、GitHub、Postgres、Slack、Puppeteer） |

Rule of thumb: if a tool is read-only, cacheable, and called from two or more hosts, ship it as an MCP server. If it is one-off inline logic, keep it as a local function (Phase 11 · 09).

> 经验法则：如果一个工具是只读的、可缓存的、并且被两个或更多宿主调用，就把它作为 MCP 服务器发布。如果是临时内联逻辑，保持为本地函数。

## Ship It | 产出物

Save `outputs/skill-mcp-server-designer.md`:

```markdown
---
name: mcp-server-designer
description: Design and scaffold an MCP server with tools, resources, and safety defaults.
version: 1.0.0
phase: 11
lesson: 14
tags: [llm-engineering, mcp, tool-use]
---

Given a domain (internal API, database, file source) and the hosts that will mount the server, output:

1. Primitive map. Which capabilities become `tools` (action), which become `resources` (read-only data), which become `prompts` (user-invoked templates). One line per primitive.
2. Auth plan. Stdio (trusted local), streamable HTTP with API key, or OAuth 2.1 with PKCE. Pick and justify.
3. Schema draft. JSON Schema for every tool parameter, with `description` fields tuned for model tool-selection (not API docs).
4. Destructive-action list. Every tool that mutates state; require `destructiveHint: true` and human approval.
5. Test plan. Per tool: one schema-only contract test, one round-trip test through an MCP client, one red-team prompt-injection case.

Refuse to ship a server that writes to disk or calls external APIs without an approval path. Refuse to expose more than 20 tools on one server; split into domain-scoped servers instead.
```

## Exercises | 练习题

1. **Easy.** Extend the `demo-server` with a `subtract` tool. Connect it from Claude Desktop. Confirm the host picks up the new tool without a restart by emitting a `tools/list_changed` notification.
   **简单。** 用 `subtract` 工具扩展 `demo-server`。从 Claude Desktop 连接。
2. **Medium.** Add a `resource` that exposes the last 100 lines of `/var/log/app.log`. Enforce a roots allowlist so `../etc/passwd` is blocked even if the model asks for it.
   **中等。** 添加一个暴露 `/var/log/app.log` 最后 100 行的 `resource`。强制执行 roots 白名单。
3. **Hard.** Build an MCP proxy that multiplexes three upstream servers (Filesystem, GitHub, Postgres) into one aggregate surface. Handle name collisions and forward `notifications/tools/list_changed` cleanly.
   **困难。** 构建一个 MCP 代理，将三个上游服务器复用到一个聚合界面。

## Key Terms | 术语速查表

| Term | What people say | What it actually means | 中文释义 |
|------|-----------------|-----------------------|---------|
| MCP | "Tool protocol for LLMs" / "LLM 工具协议" | JSON-RPC 2.0 spec for exposing tools, resources, and prompts to any LLM host. | MCP：向任何 LLM 宿主暴露工具、资源和提示的 JSON-RPC 2.0 规范 |
| Host | "Claude Desktop" | The LLM application — owns the model and user UI, mounts one or more clients. | 宿主：LLM 应用——拥有模型和用户 UI |
| Client | "Connection" / "连接" | A per-server connection inside the host that speaks JSON-RPC to exactly one server. | 客户端：宿主内部与一个服务器通信的连接 |
| Server | "The thing with the tools" / "带工具的那个" | Your code; advertises tools/resources/prompts and handles their invocation. | 服务器：你的代码；发布工具/资源/提示并处理调用 |
| Tool | "Function call" / "函数调用" | Model-invokable action with a JSON Schema input and a text/JSON result. | 工具：模型可调用的动作，带 JSON Schema 输入 |
| Resource | "Read-only data" / "只读数据" | URI-addressed content (file, row, API response) the host can request. | 资源：通过 URI 寻址的只读内容 |
| Prompt | "Saved prompt" / "保存的提示" | User-invokable template (often with arguments) surfaced as a slash-command. | 提示：用户可调用的模板 |
| Stdio transport | "Local dev mode" / "本地开发模式" | Parent host spawns the server as a child process; JSON-RPC over stdin/stdout. | Stdio 传输：宿主将服务器作为子进程启动 |
| Streamable HTTP | "The 2025-06 remote transport" / "远程传输" | POST for requests, optional SSE for server-initiated messages; replaces the older SSE-only transport. | 可流式 HTTP：POST 请求 + 可选 SSE 消息 |

## Further Reading | 延伸阅读

- [Model Context Protocol specification](https://modelcontextprotocol.io/specification) — canonical reference, versioned by date.
  MCP 规范的权威参考，按日期版本化。
- [modelcontextprotocol/servers](https://github.com/modelcontextprotocol/servers) — Filesystem, GitHub, Postgres, Slack, Puppeteer reference servers.
  Filesystem、GitHub、Postgres、Slack、Puppeteer 参考服务器。
- [Anthropic — Introducing MCP (Nov 2024)](https://www.anthropic.com/news/model-context-protocol) — launch post with design rationale.
  Anthropic 发布 MCP 的公告及设计理念。
- [Python SDK](https://github.com/modelcontextprotocol/python-sdk) — official SDK used in this lesson.
  本课使用的官方 Python SDK。
- [Security considerations for MCP](https://modelcontextprotocol.io/docs/concepts/security) — roots, destructive hints, tool poisoning.
  MCP 安全考虑：roots、破坏性提示、工具投毒。
- [Google A2A specification](https://google.github.io/A2A/) — Agent2Agent protocol; the sibling standard for agent-to-agent communication that complements MCP's agent-to-tool scope.
  Google A2A 协议；Agent 间通信的兄弟标准。
- [Anthropic — Building effective agents (Dec 2024)](https://www.anthropic.com/research/building-effective-agents) — where MCP sits in the broader pattern library for agent design (augmented LLM, workflows, autonomous agents).
  MCP 在 Agent 设计更广泛模式库中的定位。
