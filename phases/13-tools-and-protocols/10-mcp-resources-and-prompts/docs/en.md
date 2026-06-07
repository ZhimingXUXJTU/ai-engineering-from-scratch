# MCP Resources and Prompts — Context Exposure Beyond Tools | MCP 资源与提示：工具之外的上下文暴露

> Tools get 90 percent of MCP attention. The other two server primitives solve different problems. Resources expose data for reading; prompts expose reusable templates as slash-commands. Many servers should use resources instead of wrapping reads in tools, and prompts instead of hard-coding workflows in client prompts. This lesson names the decision rule and walks the `resources/*` and `prompts/*` messages.

> **【中文解读】** 工具获得了 MCP 90% 的关注，但另外两个服务器原语解决不同的问题。Resources 暴露可读数据；Prompts 暴露可复用的模板作为斜杠命令。许多服务器应该使用 resources 而非将读操作包装为 tools，使用 prompts 而非在客户端提示中硬编码工作流。

> **【拓展：Resources vs Tools 选择】** 在 MCP 设计中，Resources 用于只读数据暴露（如文件内容、数据库记录），Tools 用于有副作用的操作（如创建、删除、发送）。错误地将读操作包装为 tool 会增加不必要的模型决策负担。Prompts 作为斜杠命令模板，让用户快速触发预设工作流。

**Type:** Build | **类型:** 构建
**Languages:** Python (stdlib, resource + prompt handler) | **语言:** Python (stdlib, resource + prompt handler)
**Prerequisites:** Phase 13 · 07 (MCP server) | **前置知识:** Phase 13 · 07 (MCP server)
**Time:** ~45 minutes | **时间:** ~45 分钟

## Learning Objectives | 学习目标

- Decide between exposing a capability as a tool, a resource, or a prompt for a given domain.
  中文翻译：参见英文条目了解详情。
- Implement `resources/list`, `resources/read`, `resources/subscribe` and handle `notifications/resources/updated`.
  中文翻译：参见英文条目了解详情。
- Implement `prompts/list` and `prompts/get` with argument templates.
  中文翻译：参见英文条目了解详情。
- Recognize when the host surfaces prompts as slash-commands vs auto-injected context.
  中文翻译：参见英文条目了解详情。

## The Problem | 问题引入

> **【中文解读】** 一个简单的笔记 MCP 服务器把所有功能都暴露为工具。但正确的拆分是：数据暴露为资源（resources）、变更/计算动作暴露为工具（tools）、可复用工作流暴露为提示模板（prompts）。每种原语有其特定的 UX 呈现和访问模式。资源可被订阅，客户端 UI（如 Claude Desktop 的资源面板）可以展示数据。

A naive MCP server for a notes app exposes everything as tools: `notes_read`, `notes_list`, `notes_search`. This wraps every data access in a model-driven tool call. Consequences:

> MCP 服务器端的核心实现：暴露工具、资源和提示模板，通过 JSON-RPC 2.0 与客户端通信。

- The model has to decide whether to call `notes_read` for every query that might benefit from context.
  中文翻译：参见英文条目了解详情。
- Read-only content cannot be subscribed to or streamed to the host's side panel.
  中文翻译：参见英文条目了解详情。
- Client UIs (Claude Desktop's resource attachment panel, Cursor's "Include file" picker) cannot surface the data.
  中文翻译：参见英文条目了解详情。

The right split: expose data as a resource, expose mutating or computed actions as tools, expose reusable multi-step workflows as prompts. Each primitive has its UX affordance and its access pattern.

> 资源相关内容：MCP 资源的暴露、订阅和读取机制。

## The Concept | 核心概念

### Tools vs resources vs prompts — the decision rule

> **【中文解读】** 工具/资源/提示的决策规则：搜索/过滤/转换数据用工具；用户想附加到上下文的数据用资源；可复用的多步工作流用提示。判断标准：模型在每次相关查询时都要调用的是工具；用户想附加到对话中的是资源；用户想反复执行的完整工作流是提示。

| Capability | Primitive |
|------------|-----------|
| User wants to search, filter, or transform data | tool |
| User wants the host to include this data as context | resource |
| User wants a templated workflow they can re-run | prompt |

Guideline: if the model would benefit from calling it on every related query, it is a tool. If the user would benefit from attaching it to a conversation, it is a resource. If a whole multi-step workflow is the unit the user wants to re-use, it is a prompt.

> 资源相关内容：MCP 资源的暴露、订阅和读取机制。

### Resources

`resources/list` returns `{resources: [{uri, name, mimeType, description?}]}`. `resources/read` takes `{uri}` and returns `{contents: [{uri, mimeType, text | blob}]}`.

> 资源相关内容：MCP 资源的暴露、订阅和读取机制。

URIs can be anything addressable:

> 参见英文原文获取完整的技术说明。

- `file:///Users/alice/notes/mcp.md`
  中文翻译：参见英文条目了解详情。
- `postgres://my-db/query/SELECT ...`
  中文翻译：参见英文条目了解详情。
- `notes://note-14` (custom scheme)
  中文翻译：参见英文条目了解详情。
- `memory://session-2026-04-22/recent` (server-specific)
  中文翻译：参见英文条目了解详情。

`contents[]` supports both text and binary. Binary uses `blob` as a base64-encoded string plus a `mimeType`.

> 参见英文原文获取完整的技术说明。

### Resource subscriptions

Declare `{resources: {subscribe: true}}` in capabilities. Client calls `resources/subscribe {uri}`. Server sends `notifications/resources/updated {uri}` when the resource changes. Client re-reads.

> 资源相关内容：MCP 资源的暴露、订阅和读取机制。

Use case: a notes server whose resources are files on disk; a file watcher triggers update notifications; Claude Desktop re-pulls the file into context when edited outside the host.

> 资源相关内容：MCP 资源的暴露、订阅和读取机制。

### Resource templates (2025-11-25 addition)

`resourceTemplates` let you expose a parameterized URI pattern: `notes://{id}` with `id` as a completion target. The client can autocomplete ids in the resource picker.

> 资源相关内容：MCP 资源的暴露、订阅和读取机制。

### Prompts

> **【拓展：MCP Prompts 作为 Slash Commands】** MCP Prompts 在 Claude Desktop、VS Code 和 Cursor 中以斜杠命令的形式出现在聊天 UI 中。用户输入 `/code_review` 并从表单中选择参数。服务器的提示模板是"用户快捷方式"和"发送给模型的完整 prompt"之间的契约。这使得服务器可以定义结构化的工作流。

`prompts/list` returns `{prompts: [{name, description, arguments?}]}`. `prompts/get` takes `{name, arguments}` and returns `{description, messages: [{role, content}]}`.

> 参见英文原文获取完整的技术说明。

A prompt is a template that fills to a list of messages the host feeds its model. For example, a `code_review` prompt takes a `file_path` argument and returns a three-message sequence: a system message, a user message with the file body, and an assistant kickoff with a reasoning template.

> 提示模板相关内容：MCP 提示的定义、参数和复用。

### Hosts and prompts

Claude Desktop, VS Code, and Cursor expose prompts as slash-commands in the chat UI. The user types `/code_review` and picks arguments from a form. The server's prompt is the contract between "user shortcut" and "full prompt sent to model".

> 参见英文原文获取完整的技术说明。

Not every client supports prompts yet — check capability negotiation. A server with prompt capability declared but a client without prompt support simply will not see the slash commands.

> 参见英文原文获取完整的技术说明。

### The "list changed" notification

Both resources and prompts emit `notifications/list_changed` when the set mutates. A notes server that just imported 20 new notes emits `notifications/resources/list_changed`; the client re-calls `resources/list` to pick up the additions.

> 资源相关内容：MCP 资源的暴露、订阅和读取机制。

### Content type conventions

For text: `mimeType: "text/plain"`, `text/markdown`, `application/json`.

> 参见英文原文获取完整的技术说明。
For binary: `image/png`, `application/pdf`, plus the `blob` field.

> 参见英文原文获取完整的技术说明。
For MCP Apps (Lesson 14): `text/html;profile=mcp-app` in a `ui://` URI.

> MCP Apps 相关内容：交互式 UI 资源和富界面组件。

### Dynamic resources

> **【拓展：动态资源与缓存策略】** 资源 URI 不必对应静态文件。`notes://recent` 可以每次读取时返回最新 5 条笔记，`db://query/users/active` 可以执行参数化查询。规则是：如果客户端可以按 URI 缓存，则 URI 必须稳定；如果是一次性计算，URI 应包含时间戳或随机数以避免缓存过期。

A resource URI does not have to correspond to a static file. `notes://recent` can return the latest five notes on every read. `db://query/users/active` can execute a parameterized query. The server is free to compute content dynamically.

> 资源相关内容：MCP 资源的暴露、订阅和读取机制。

Rule: if the client can cache by URI, the URI must be stable. If computation is one-shot, the URI should include a timestamp or nonce so the client cache does not stale out.

> 参见英文原文获取完整的技术说明。

### Subscriptions vs polling

Subscription-capable clients get server push via `notifications/resources/updated`. Pre-subscription clients or hosts that do not support it poll by re-reading. Both are spec-compliant. The server's capability declaration tells the client which it supports.

> 资源相关内容：MCP 资源的暴露、订阅和读取机制。

Cost of subscriptions: per-session state on the server (who is subscribed to what). Keep the subscribed set bounded; disconnected clients should time out.

> 会话管理相关内容：MCP 会话的建立、维护和终止。

### Prompts vs system prompts

> **【中文解读】** MCP 中的 Prompts 不是系统提示。宿主的系统提示（操作指令）和 MCP 提示（服务器提供的模板，由用户调用）并存。行为良好的客户端不会让服务器提示覆盖自己的系统提示，而是分层叠加。这是一个重要的安全边界。

Prompts in MCP are not system prompts. The host's system prompt (its own operating instructions) and MCP prompts (server-supplied templates invoked by user) live side by side. A well-behaved client never lets a server prompt override its own system prompt; it layers them.

> MCP 服务器端的核心实现：暴露工具、资源和提示模板，通过 JSON-RPC 2.0 与客户端通信。

## Use It | 用框架实现

`code/main.py` extends the notes server from Lesson 07 with:

> 代码实现说明：参见 code/main.py 中的具体实现。

- Per-note resources (`notes://note-1`, etc.) with `resources/subscribe` support.
  中文翻译：参见英文条目了解详情。
- A `review_note` prompt that renders to a three-message template.
  中文翻译：参见英文条目了解详情。
- A file-watcher simulation that emits `notifications/resources/updated` when a note is modified.
  中文翻译：参见英文条目了解详情。
- A `notes://recent` dynamic resource that always returns the latest five notes.
  中文翻译：参见英文条目了解详情。

Run the demo to see the full flow.

> 参见英文原文获取完整的技术说明。

## Ship It | 产出物

This lesson produces `outputs/skill-primitive-splitter.md`. Given a proposed MCP server, the skill categorizes each capability as tool / resource / prompt with a rationale.

> MCP 服务器端的核心实现：暴露工具、资源和提示模板，通过 JSON-RPC 2.0 与客户端通信。

## Exercises | 练习题

1. Run `code/main.py`. Observe the initial resource list, then trigger a note edit and verify the `notifications/resources/updated` event fires.
   中文翻译：运行相关练习。参见英文原文了解完整要求。

2. Add a `resources/list_changed` emitter: when a new note is created, send the notification so clients re-discover.
   中文翻译：添加相关练习。参见英文原文了解完整要求。

3. Design three prompts for a GitHub MCP server: `summarize_pr`, `triage_issue`, `release_notes`. Each with argument schemas. The prompt body should be runnable without further edits.
   中文翻译：设计相关练习。参见英文原文了解完整要求。

4. Take an existing tool in the Lesson 07 server and classify whether it should remain a tool or be split into a resource plus tool pair. Justify in one sentence.
   中文翻译：参见英文原文了解完整练习要求。

5. Read the spec's `server/resources` and `server/prompts` sections. Identify the one field in `resources/read` that is rarely populated but spec-supported. Hint: look at `_meta` on resource content.
   中文翻译：阅读相关练习。参见英文原文了解完整要求。

## Key Terms | 术语速查表

| Term | What people say | What it actually means | 中文术语 |
|------|----------------|------------------------|----------|
| Resource | "Exposed data" | URI-addressable content the host can read | 资源 |
| Resource URI | "Pointer to data" | Scheme-prefixed identifier (`file://`, `notes://`, etc.) | 资源 URI |
| `resources/subscribe` | "Watch for changes" | Client-opt-in server-push updates for a specific URI | 资源订阅 |
| `notifications/resources/updated` | "Resource changed" | Signal to client that a subscribed resource has new content | 资源更新通知 |
| Resource template | "Parameterized URI" | URI pattern with completion hints for the host picker | 资源模板 |
| Prompt | "Slash-command template" | Named multi-message template with argument slots | 提示模板 |
| Prompt arguments | "Template inputs" | Typed parameters the host collects before rendering | 提示参数 |
| `prompts/get` | "Render template" | Server returns the filled-in message list | 渲染提示 |
| Content block | "Typed chunk" | `{type: text \| image \| resource \| ui_resource}` | 内容块 |
| Slash-command UX | "User shortcut" | Host surfaces prompts as commands starting with `/` | 斜杠命令 |

## Further Reading | 延伸阅读

- [MCP — Concepts: Resources](https://modelcontextprotocol.io/docs/concepts/resources) — resource URIs, subscriptions, and templates
  中文翻译：resource URIs, subscriptions, and templates
- [MCP — Concepts: Prompts](https://modelcontextprotocol.io/docs/concepts/prompts) — prompt templates and slash-command integration
  中文翻译：prompt templates and slash-command integration
- [MCP — Server resources spec 2025-11-25](https://modelcontextprotocol.io/specification/2025-11-25/server/resources) — full `resources/*` message reference
  中文翻译：full `resources/*` message reference
- [MCP — Server prompts spec 2025-11-25](https://modelcontextprotocol.io/specification/2025-11-25/server/prompts) — full `prompts/*` message reference
  中文翻译：full `prompts/*` message reference
- [MCP — Protocol info site: resources](https://modelcontextprotocol.info/docs/concepts/resources/) — community guide expanding on the official docs
  中文翻译：community guide expanding on the official docs
