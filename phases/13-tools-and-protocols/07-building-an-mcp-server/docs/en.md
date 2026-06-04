# Building an MCP Server — Python + TypeScript SDKs | 构建 MCP 服务器：Python + TypeScript SDK

> Most MCP tutorials show only stdio hello-worlds. A real server exposes tools plus resources plus prompts, handles capability negotiation, emits structured errors, and works the same across SDKs. This lesson builds a notes server end-to-end: stdlib stdio transport, JSON-RPC dispatch, the three server primitives, and a pure-function style that drops into either the Python SDK's FastMCP or the TypeScript SDK when you graduate.

> **【中文解读】** 大多数 MCP 教程只展示 stdio 的 hello-world。真正的服务器需要暴露 tools + resources + prompts、处理能力协商、发出结构化错误，并在不同 SDK 间保持一致。本课端到端构建一个笔记服务器：stdlib stdio 传输、JSON-RPC 分发、三个服务器原语，以及可迁移到 FastMCP 或 TypeScript SDK 的纯函数风格。

> **【拓展：MCP 服务器→Claude 生态开发】** MCP 服务器是 Claude 生态的核心开发模式。通过 stdio 传输，Claude Desktop 等客户端可以启动你的服务器作为子进程。FastMCP (Python) 和 TypeScript SDK 提供装饰器风格的高级 API，使开发更简洁。理解 stdlib 实现有助于排查 SDK 层面的问题。

**Type:** Build
**Languages:** Python (stdlib, stdio MCP server)
**Prerequisites:** Phase 13 · 06 (MCP fundamentals)
**Time:** ~75 minutes

## Learning Objectives

- Implement `initialize`, `tools/list`, `tools/call`, `resources/list`, `resources/read`, `prompts/list`, and `prompts/get` methods.
- Write a dispatch loop that reads JSON-RPC messages from stdin and writes responses to stdout.
- Emit structured error responses per the JSON-RPC 2.0 spec and MCP's additional codes.
- Graduate a stdlib implementation to FastMCP (Python SDK) or the TypeScript SDK without rewriting tool logic.

## The Problem | 问题引入

> **【中文解读】** 在使用远程传输（Phase 13.09）或认证层（Phase 13.16）之前，需要一个干净的本地服务器。本地意味着 stdio：服务器被客户端作为子进程启动，消息通过 stdin/stdout 按换行符分隔传递。笔记服务器是好的范例，因为它练习了所有三个服务器原语：Tools 做变更、Resources 暴露数据、Prompts 提供模板。

Before you can use a remote transport (Phase 13 · 09) or an auth layer (Phase 13 · 16), you need a clean local server. Local means stdio: the server is spawned by the client as a child process, messages flow over stdin/stdout newline-delimited.

The 2025-11-25 spec prescribes that stdio messages are encoded as JSON objects with an explicit `\n` separator. No SSE here; SSE was the old remote mode and is being removed in mid-2026 (Atlassian's Rovo MCP server deprecated it on June 30, 2026; Keboola on April 1, 2026). For stdio, one JSON object per line is the whole wire format.

A notes server is a good shape because it exercises all three server primitives. Tools do mutations (`notes_create`). Resources expose data (`notes://{id}`). Prompts ship templates (`review_note`). The shape of this lesson generalizes to any domain.

## The Concept | 核心概念

### Dispatch loop

> **【中文解读】** 分发循环三条规则：(1) 不要向 stdout 输出任何非 JSON-RPC 信封的内容，调试日志输出到 stderr；(2) 每个请求必须匹配一个携带相同 `id` 的响应；(3) 通知不得有响应。

```
loop:
  line = stdin.readline()
  msg = json.loads(line)
  if has id:
    handle request -> write response
  else:
    handle notification -> no response
```

Three rules:

- Do not print anything to stdout that is not a JSON-RPC envelope. Debug logs go to stderr.
- Every request MUST be matched with a response carrying the same `id`.
- Notifications MUST NOT be responded to.

### Implementing `initialize`

```python
def initialize(params):
    return {
        "protocolVersion": "2025-11-25",
        "capabilities": {
            "tools": {"listChanged": True},
            "resources": {"listChanged": True, "subscribe": False},
            "prompts": {"listChanged": False},
        },
        "serverInfo": {"name": "notes", "version": "1.0.0"},
    }
```

Declare only what you support. The client relies on the capability set to gate features.

### Implementing `tools/list` and `tools/call`

> **【拓展：MCP 工具错误的两层模型】** MCP 区分两种错误：(1) 协议级错误（未知方法、参数错误）用 JSON-RPC error 返回；(2) 工具级错误（调用合法但执行失败）返回 `{content: [...], isError: true}`。这种区分让模型能在上下文中看到失败信息并做出调整，而不是简单地收到一个连接错误。

`tools/list` returns `{tools: [...]}` with each entry having `name`, `description`, `inputSchema`. `tools/call` takes `{name, arguments}` and returns `{content: [blocks], isError: bool}`.

Content blocks are typed. The most common:

```json
{"type": "text", "text": "Found 2 notes"}
{"type": "resource", "resource": {"uri": "notes://14", "text": "..."}}
{"type": "image", "data": "<base64>", "mimeType": "image/png"}
```

Tool errors come in two shapes. Protocol-level errors (unknown method, bad params) are JSON-RPC errors. Tool-level errors (valid call but the tool failed) are returned as `{content: [...], isError: true}`. That lets the model see the failure in its context.

### Implementing resources

Resources are read-only by design. `resources/list` returns a manifest; `resources/read` returns the content. URIs can be `file://...`, `http://...`, or a custom scheme like `notes://`.

When you expose data as a resource instead of a tool:

- The model does not "call" it; the client can inject it into context on user request.
- Subscriptions let the server push updates when the resource changes (Phase 13 · 10).
- Phase 13 · 14 extends this with `ui://` for interactive resources.

### Implementing prompts

Prompts are templates with named arguments. The host surfaces them as slash-commands. A `review_note` prompt might take a `note_id` argument and produce a multi-message prompt template the client feeds to its model.

### Stdio transport subtleties

> **【中文解读】** stdio 传输的细节：换行分隔的 JSON，无长度前缀帧；不要缓冲，每次写入后 `sys.stdout.flush()`；客户端控制生命周期，stdin 关闭时干净退出；不要静默处理 SIGPIPE。

- Newline-delimited JSON. No length-prefixed framing.
- Do not buffer. `sys.stdout.flush()` after each write.
- The client controls the lifetime. When stdin closes (EOF), exit cleanly.
- Do not handle SIGPIPE silently; log and exit.

### Annotations

Each tool can carry `annotations` describing safety properties:

- `readOnlyHint: true` — pure read, safe to retry.
- `destructiveHint: true` — irreversible side effects; client should confirm.
- `idempotentHint: true` — same inputs produce same outputs.
- `openWorldHint: true` — interacts with external systems.

> **【中文解读】** 每个工具可携带 `annotations` 描述安全属性：`readOnlyHint`（只读，可重试）、`destructiveHint`（不可逆副作用，需确认）、`idempotentHint`（幂等）、`openWorldHint`（与外部系统交互）。客户端使用这些决定 UX（确认对话框）和路由。

The client uses these to decide UX (confirmation dialogs, status indicators) and routing (Phase 13 · 17).

### Graduation path

> **【拓展：FastMCP 的装饰器风格开发】** FastMCP 是 MCP Python SDK 的高级封装，使用装饰器风格将 stdlib 版 180 行代码缩减到约 80 行。`@app.tool()` 注册工具、`@app.resource()` 注册资源、`@app.prompt()` 注册提示模板。概念不变（能力协商、分发、内容块），只是语法更简洁。TypeScript SDK 有等价形式。从 stdlib 迁移到 SDK 是无痛的。

The stdlib server in `code/main.py` is about 180 lines. FastMCP (Python) collapses the same logic to decorator-style:

```python
from fastmcp import FastMCP
app = FastMCP("notes")

@app.tool()
def notes_search(query: str, limit: int = 10) -> list[dict]:
    ...
```

The TypeScript SDK has an equivalent shape. The graduation path is drop-in when you are ready; the concepts (capabilities, dispatch, content blocks) are the same.

## Use It | 用框架实现

`code/main.py` is a complete notes MCP server over stdio, stdlib only. It handles `initialize`, `tools/list`, `tools/call` for three tools (`notes_list`, `notes_search`, `notes_create`), `resources/list` and `resources/read` for each note, and a `review_note` prompt. You can drive it by piping JSON-RPC messages:

```
echo '{"jsonrpc":"2.0","id":1,"method":"initialize","params":{}}' | python main.py
```

What to look at:

- The dispatcher is a `dict[str, Callable]` keyed by method name.
- Every tool executor returns a list of content blocks, not a bare string.
- `isError: true` is set when the executor raises.

## Ship It | 产出物

This lesson produces `outputs/skill-mcp-server-scaffolder.md`. Given a domain (notes, tickets, files, database), the skill scaffolds an MCP server with the right tools / resources / prompts split and SDK graduation path.

## Exercises | 练习题

1. Run `code/main.py` and drive it with hand-built JSON-RPC messages. Exercise `notes_create`, then `resources/read` to retrieve the new note.

2. Add a `notes_delete` tool with `annotations: {destructiveHint: true}`. Verify the client would surface a confirmation dialog (this requires a real host; Claude Desktop works).

3. Implement `resources/subscribe` so the server pushes `notifications/resources/updated` whenever a note is modified. Add a keepalive task.

4. Port the server to FastMCP. The Python file should shrink to under 80 lines. The wire behavior must be identical; verify with the same JSON-RPC test harness.

5. Read the spec's `server/tools` section and identify one field of a tool definition not implemented in this lesson's server. (Hint: there are several; pick one and add it.)

## Key Terms | 术语速查表

| Term | What people say | What it actually means | 中文术语 |
|------|----------------|------------------------|----------|
| MCP server | "The thing that exposes tools" | Process that speaks MCP JSON-RPC over stdio or HTTP | MCP 服务器 |
| stdio transport | "Child process model" | Server is spawned by client; communicates via stdin/stdout | stdio 传输 |
| Dispatcher | "Method router" | Map of JSON-RPC method name to handler function | 分发器 |
| Content block | "Tool result chunk" | Typed element in the `content` array of a tool response | 内容块 |
| `isError` | "Tool-level failure" | Signals the tool failed; distinguishes from JSON-RPC error | 工具级错误 |
| Annotations | "Safety hints" | readOnly / destructive / idempotent / openWorld flags | 安全注解 |
| FastMCP | "Python SDK" | Decorator-based higher-level framework on top of the MCP protocol | FastMCP 框架 |
| Resource URI | "Addressable data" | `file://`, `db://`, or custom scheme identifying a resource | 资源 URI |
| Prompt template | "Slash-command brief" | Server-supplied template with argument slots for host UIs | 提示模板 |
| Capability declaration | "Feature toggle" | Per-primitive flags declared in `initialize` | 能力声明 |

## Further Reading | 延伸阅读

- [Model Context Protocol — Python SDK](https://github.com/modelcontextprotocol/python-sdk) — the reference Python implementation
- [Model Context Protocol — TypeScript SDK](https://github.com/modelcontextprotocol/typescript-sdk) — parallel TS implementation
- [FastMCP — server framework](https://gofastmcp.com/) — decorator-style Python API for MCP servers
- [MCP — Quickstart server guide](https://modelcontextprotocol.io/quickstart/server) — end-to-end tutorial using either SDK
- [MCP — Server tools spec](https://modelcontextprotocol.io/specification/2025-11-25/server/tools) — complete reference for tools/* messages
