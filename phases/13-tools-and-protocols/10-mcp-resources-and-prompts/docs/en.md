# MCP Resources and Prompts — Context Exposure Beyond Tools | MCP 资源与提示：工具之外的上下文暴露

> Tools get 90 percent of MCP attention. The other two server primitives solve different problems. Resources expose data for reading; prompts expose reusable templates as slash-commands. Many servers should use resources instead of wrapping reads in tools, and prompts instead of hard-coding workflows in client prompts. This lesson names the decision rule and walks the `resources/*` and `prompts/*` messages.

> **【中文解读】** 工具获得了 MCP 90% 的关注，但另外两个服务器原语解决不同的问题。Resources 暴露可读数据；Prompts 暴露可复用的模板作为斜杠命令。许多服务器应该使用 resources 而非将读操作包装为 tools，使用 prompts 而非在客户端提示中硬编码工作流。

> **【拓展：Resources vs Tools 选择】** 在 MCP 设计中，Resources 用于只读数据暴露（如文件内容、数据库记录），Tools 用于有副作用的操作（如创建、删除、发送）。错误地将读操作包装为 tool 会增加不必要的模型决策负担。Prompts 作为斜杠命令模板，让用户快速触发预设工作流。

> 🔗 **【前置】** 学本节前请先掌握：(1) Phase 13·06（MCP Fundamentals）——理解 resources 和 prompts 是六原语中的两个；(2) Phase 13·07（Building an MCP Server）——掌握 tools/list、tools/call 的实现，本节是平行扩展；(3) URI 概念（`file://`、`http://`、自定义 scheme）。

**Type:** Build | **类型:** 构建
**Languages:** Python (stdlib, resource + prompt handler) | **语言:** Python (stdlib, resource + prompt handler)
**Prerequisites:** Phase 13 · 07 (MCP server) | **前置知识:** Phase 13 · 07 (MCP server)
**Time:** ~45 minutes | **时间:** ~45 分钟

## Learning Objectives | 学习目标

- Decide between exposing a capability as a tool, a resource, or a prompt for a given domain.
  中文翻译：对给定领域，决定将能力暴露为工具、资源还是提示。
- Implement `resources/list`, `resources/read`, `resources/subscribe` and handle `notifications/resources/updated`.
  中文翻译：实现 `resources/list`、`resources/read`、`resources/subscribe`，处理 `notifications/resources/updated`。
- Implement `prompts/list` and `prompts/get` with argument templates.
  中文翻译：实现带参数模板的 `prompts/list` 和 `prompts/get`。
- Recognize when the host surfaces prompts as slash-commands vs auto-injected context.
  中文翻译：识别宿主何时将提示显示为斜杠命令而非自动注入上下文。

## The Problem | 问题引入

> **【中文解读】** 一个简单的笔记 MCP 服务器把所有功能都暴露为工具。但正确的拆分是：数据暴露为资源（resources）、变更/计算动作暴露为工具（tools）、可复用工作流暴露为提示模板（prompts）。每种原语有其特定的 UX 呈现和访问模式。资源可被订阅，客户端 UI（如 Claude Desktop 的资源面板）可以展示数据。

A naive MCP server for a notes app exposes everything as tools: `notes_read`, `notes_list`, `notes_search`. This wraps every data access in a model-driven tool call. Consequences:

> 一个天真的笔记应用 MCP 服务器将一切暴露为工具：`notes_read`、`notes_list`、`notes_search`。这把每次数据访问包装为模型驱动的工具调用。后果：

- The model has to decide whether to call `notes_read` for every query that might benefit from context.
  中文翻译：模型必须为每个可能受益于上下文的查询决定是否调用 `notes_read`。
- Read-only content cannot be subscribed to or streamed to the host's side panel.
  中文翻译：只读内容无法订阅或流式传输到宿主的侧边栏。
- Client UIs (Claude Desktop's resource attachment panel, Cursor's "Include file" picker) cannot surface the data.
  中文翻译：客户端 UI（Claude Desktop 的资源附加面板、Cursor 的"包含文件"选择器）无法显示数据。

The right split: expose data as a resource, expose mutating or computed actions as tools, expose reusable multi-step workflows as prompts. Each primitive has its UX affordance and its access pattern.

> 正确的拆分：将数据暴露为资源，将变更或计算动作暴露为工具，将可复用的多步工作流暴露为提示。每个原语有其 UX 特性和访问模式。

> 💡 **【类比】** MCP 三原语像图书馆的三种资源：(1) **Tools** = 借阅台工作人员——你请他"帮我查这本书在哪""帮我办张卡"，他执行动作（带副作用）；(2) **Resources** = 书架上的书——你可以自己取下来读（只读），但不需要每次都请示工作人员，能直接附加到对话上下文；(3) **Prompts** = 馆内的"自助导览路线"——预制的多步骤流程（"先看 2 楼、再看 3 楼"），你按一个按钮就走完整个流程。把书当成工具是浪费，把工作人员当成书是错配。

## The Concept | 核心概念

### Tools vs resources vs prompts — the decision rule

> **【中文解读】** 工具/资源/提示的决策规则：搜索/过滤/转换数据用工具；用户想附加到上下文的数据用资源；可复用的多步工作流用提示。判断标准：模型在每次相关查询时都要调用的是工具；用户想附加到对话中的是资源；用户想反复执行的完整工作流是提示。

| Capability | Primitive |
|------------|-----------|
| User wants to search, filter, or transform data | tool |
| User wants the host to include this data as context | resource |
| User wants a templated workflow they can re-run | prompt |

Guideline: if the model would benefit from calling it on every related query, it is a tool. If the user would benefit from attaching it to a conversation, it is a resource. If a whole multi-step workflow is the unit the user wants to re-use, it is a prompt.

> 准则：如果模型在每次相关查询时调用它有益，那是工具。如果用户将它附加到对话中有益，那是资源。如果整个多步工作流是用户想复用的单元，那是提示。

### Resources

`resources/list` returns `{resources: [{uri, name, mimeType, description?}]}`. `resources/read` takes `{uri}` and returns `{contents: [{uri, mimeType, text | blob}]}`.

> `resources/list` 返回 `{resources: [{uri, name, mimeType, description?}]}`。`resources/read` 接收 `{uri}` 并返回 `{contents: [{uri, mimeType, text | blob}]}`。

URIs can be anything addressable:

> URI 可以是任何可寻址的：

- `file:///Users/alice/notes/mcp.md`
  中文翻译：`file:///Users/alice/notes/mcp.md`（本地文件）
- `postgres://my-db/query/SELECT ...`
  中文翻译：`postgres://my-db/query/SELECT ...`（数据库查询）
- `notes://note-14` (custom scheme)
  中文翻译：`notes://note-14`（自定义方案）
- `memory://session-2026-04-22/recent` (server-specific)
  中文翻译：`memory://session-2026-04-22/recent`（服务器特定）

`contents[]` supports both text and binary. Binary uses `blob` as a base64-encoded string plus a `mimeType`.

> `contents[]` 同时支持文本和二进制。二进制使用 `blob` 作为 base64 编码字符串加 `mimeType`。

> ⚠️ **【易错点】** 场景：把 100MB 大文件作为 Resource 一次性返回 / 后果：客户端 OOM 或者 LLM 上下文爆炸（超过 token 限制），整个对话卡死 / 修复：(1) Resource 在 server 端分页或预览（只返回前 N 字符 + 总大小元数据）；(2) 大文件用专门的 "search_in_file" tool 而非 Resource；(3) 在 `resources/list` 里声明 `size` 字段，让客户端能预判；(4) 二进制（图片/PDF）先在 server 端提取文本再返回，blob 仅用于必需场景。

### Resource subscriptions

Declare `{resources: {subscribe: true}}` in capabilities. Client calls `resources/subscribe {uri}`. Server sends `notifications/resources/updated {uri}` when the resource changes. Client re-reads.

> 在能力中声明 `{resources: {subscribe: true}}`。客户端调用 `resources/subscribe {uri}`。服务器在资源变化时发送 `notifications/resources/updated {uri}`。客户端重新读取。

Use case: a notes server whose resources are files on disk; a file watcher triggers update notifications; Claude Desktop re-pulls the file into context when edited outside the host.

> 用例：笔记服务器的资源是磁盘上的文件；文件监视器触发更新通知；当文件在宿主外被编辑时，Claude Desktop 重新拉取文件到上下文。

### Resource templates (2025-11-25 addition)

`resourceTemplates` let you expose a parameterized URI pattern: `notes://{id}` with `id` as a completion target. The client can autocomplete ids in the resource picker.

> `resourceTemplates` 让你暴露参数化的 URI 模式：`notes://{id}`，`id` 作为补全目标。客户端可以在资源选择器中自动补全 id。

### Prompts

> **【拓展：MCP Prompts 作为 Slash Commands】** MCP Prompts 在 Claude Desktop、VS Code 和 Cursor 中以斜杠命令的形式出现在聊天 UI 中。用户输入 `/code_review` 并从表单中选择参数。服务器的提示模板是"用户快捷方式"和"发送给模型的完整 prompt"之间的契约。这使得服务器可以定义结构化的工作流。

`prompts/list` returns `{prompts: [{name, description, arguments?}]}`. `prompts/get` takes `{name, arguments}` and returns `{description, messages: [{role, content}]}`.

> `prompts/list` 返回 `{prompts: [{name, description, arguments?}]}`。`prompts/get` 接收 `{name, arguments}` 并返回 `{description, messages: [{role, content}]}`。

A prompt is a template that fills to a list of messages the host feeds its model. For example, a `code_review` prompt takes a `file_path` argument and returns a three-message sequence: a system message, a user message with the file body, and an assistant kickoff with a reasoning template.

> Prompt 是一个模板，填充为宿主喂给其模型的消息列表。例如，`code_review` prompt 接受 `file_path` 参数并返回三消息序列：系统消息、带文件正文的用户消息，以及带推理模板的助手启动消息。

### Hosts and prompts

Claude Desktop, VS Code, and Cursor expose prompts as slash-commands in the chat UI. The user types `/code_review` and picks arguments from a form. The server's prompt is the contract between "user shortcut" and "full prompt sent to model".

> Claude Desktop、VS Code 和 Cursor 将提示暴露为聊天 UI 中的斜杠命令。用户输入 `/code_review` 并从表单中选择参数。服务器的提示是"用户快捷方式"和"发送给模型的完整 prompt"之间的契约。

Not every client supports prompts yet — check capability negotiation. A server with prompt capability declared but a client without prompt support simply will not see the slash commands.

> 不是每个客户端都支持提示——检查能力协商。声明了 prompt 能力的服务器，但客户端不支持 prompt，则看不到斜杠命令。

> 🤔 **【困惑】** Q: Prompt 和我直接在 system prompt 里写"如何做代码评审"有什么区别？ A: 三点关键差异：(1) **触发方式**——prompt 是斜杠命令显式触发（用户主动选择），system prompt 是隐式常驻；(2) **参数化**——prompt 支持 `arguments`（如 `file_path`），system prompt 难以优雅参数化；(3) **可发现性**——`prompts/list` 让客户端 UI 自动列出可用命令，用户不需要记忆。如果你的"system 提示"实际上是个工作流模板（"读文件→分析→给建议"），用 prompt 才是正解。

### The "list changed" notification

Both resources and prompts emit `notifications/list_changed` when the set mutates. A notes server that just imported 20 new notes emits `notifications/resources/list_changed`; the client re-calls `resources/list` to pick up the additions.

> 资源和提示在集合变化时都发出 `notifications/list_changed`。刚导入 20 条新笔记的笔记服务器发出 `notifications/resources/list_changed`；客户端重新调用 `resources/list` 获取新增。

### Content type conventions

For text: `mimeType: "text/plain"`, `text/markdown`, `application/json`.

> 文本：`mimeType: "text/plain"`、`text/markdown`、`application/json`。

For binary: `image/png`, `application/pdf`, plus the `blob` field.

> 二进制：`image/png`、`application/pdf`，加上 `blob` 字段。

For MCP Apps (Lesson 14): `text/html;profile=mcp-app` in a `ui://` URI.

> MCP Apps（Lesson 14）：在 `ui://` URI 中的 `text/html;profile=mcp-app`。

### Dynamic resources

> **【拓展：动态资源与缓存策略】** 资源 URI 不必对应静态文件。`notes://recent` 可以每次读取时返回最新 5 条笔记，`db://query/users/active` 可以执行参数化查询。规则是：如果客户端可以按 URI 缓存，则 URI 必须稳定；如果是一次性计算，URI 应包含时间戳或随机数以避免缓存过期。

A resource URI does not have to correspond to a static file. `notes://recent` can return the latest five notes on every read. `db://query/users/active` can execute a parameterized query. The server is free to compute content dynamically.

> 资源 URI 不必对应静态文件。`notes://recent` 可以在每次读取时返回最新 5 条笔记。`db://query/users/active` 可以执行参数化查询。服务器可自由动态计算内容。

Rule: if the client can cache by URI, the URI must be stable. If computation is one-shot, the URI should include a timestamp or nonce so the client cache does not stale out.

> 规则：如果客户端可按 URI 缓存，URI 必须稳定。如果计算是一次性的，URI 应包含时间戳或 nonce，避免客户端缓存过期。

### Subscriptions vs polling

Subscription-capable clients get server push via `notifications/resources/updated`. Pre-subscription clients or hosts that do not support it poll by re-reading. Both are spec-compliant. The server's capability declaration tells the client which it supports.

> 支持订阅的客户端通过 `notifications/resources/updated` 获得服务器推送。不支持订阅的旧客户端或宿主通过重新读取轮询。两者都符合规范。服务器的能力声明告知客户端支持哪种。

Cost of subscriptions: per-session state on the server (who is subscribed to what). Keep the subscribed set bounded; disconnected clients should time out.

> 订阅的成本：服务器上的每会话状态（谁订阅了什么）。保持订阅集有界；断连的客户端应超时。

### Prompts vs system prompts

> **【中文解读】** MCP 中的 Prompts 不是系统提示。宿主的系统提示（操作指令）和 MCP 提示（服务器提供的模板，由用户调用）并存。行为良好的客户端不会让服务器提示覆盖自己的系统提示，而是分层叠加。这是一个重要的安全边界。

Prompts in MCP are not system prompts. The host's system prompt (its own operating instructions) and MCP prompts (server-supplied templates invoked by user) live side by side. A well-behaved client never lets a server prompt override its own system prompt; it layers them.

> MCP 中的 Prompts 不是系统提示。宿主的系统提示（其自身操作指令）和 MCP prompts（服务器提供的、由用户调用的模板）并存。行为良好的客户端不会让服务器提示覆盖自己的系统提示；它会分层叠加。

## Use It | 用框架实现

`code/main.py` extends the notes server from Lesson 07 with:

> `code/main.py` 扩展了 Lesson 07 的笔记服务器：

- Per-note resources (`notes://note-1`, etc.) with `resources/subscribe` support.
  中文翻译：每笔记资源（`notes://note-1` 等）带 `resources/subscribe` 支持。
- A `review_note` prompt that renders to a three-message template.
  中文翻译：渲染为三消息模板的 `review_note` prompt。
- A file-watcher simulation that emits `notifications/resources/updated` when a note is modified.
  中文翻译：文件监视器模拟，笔记被修改时发出 `notifications/resources/updated`。
- A `notes://recent` dynamic resource that always returns the latest five notes.
  中文翻译：始终返回最新 5 条笔记的 `notes://recent` 动态资源。

Run the demo to see the full flow.

> 运行 demo 看完整流程。

## Ship It | 产出物

This lesson produces `outputs/skill-primitive-splitter.md`. Given a proposed MCP server, the skill categorizes each capability as tool / resource / prompt with a rationale.

> 本课产出 `outputs/skill-primitive-splitter.md`。给定一个拟议的 MCP 服务器，该 skill 将每个能力归类为 tool/resource/prompt 并附理由。

## Exercises | 练习题

1. Run `code/main.py`. Observe the initial resource list, then trigger a note edit and verify the `notifications/resources/updated` event fires.
   中文翻译：运行 `code/main.py`。观察初始资源列表，然后触发笔记编辑并验证 `notifications/resources/updated` 事件触发。

2. Add a `resources/list_changed` emitter: when a new note is created, send the notification so clients re-discover.
   中文翻译：添加 `resources/list_changed` 发射器：创建新笔记时发送通知让客户端重新发现。

3. Design three prompts for a GitHub MCP server: `summarize_pr`, `triage_issue`, `release_notes`. Each with argument schemas. The prompt body should be runnable without further edits.
   中文翻译：为 GitHub MCP 服务器设计三个提示：`summarize_pr`、`triage_issue`、`release_notes`。每个带参数 schema。提示正文应无需进一步编辑即可运行。

4. Take an existing tool in the Lesson 07 server and classify whether it should remain a tool or be split into a resource plus tool pair. Justify in one sentence.
   中文翻译：取 Lesson 07 服务器中的一个现有工具，分类它是应保留为工具还是拆分为资源加工具对。用一句话说明理由。

5. Read the spec's `server/resources` and `server/prompts` sections. Identify the one field in `resources/read` that is rarely populated but spec-supported. Hint: look at `_meta` on resource content.
   中文翻译：阅读规范的 `server/resources` 和 `server/prompts` 章节。识别 `resources/read` 中一个很少填充但规范支持的字段。提示：看资源内容上的 `_meta`。

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
  中文翻译：资源 URI、订阅和模板
- [MCP — Concepts: Prompts](https://modelcontextprotocol.io/docs/concepts/prompts) — prompt templates and slash-command integration
  中文翻译：提示模板和斜杠命令集成
- [MCP — Server resources spec 2025-11-25](https://modelcontextprotocol.io/specification/2025-11-25/server/resources) — full `resources/*` message reference
  中文翻译：完整的 `resources/*` 消息参考
- [MCP — Server prompts spec 2025-11-25](https://modelcontextprotocol.io/specification/2025-11-25/server/prompts) — full `prompts/*` message reference
  中文翻译：完整的 `prompts/*` 消息参考
- [MCP — Protocol info site: resources](https://modelcontextprotocol.info/docs/concepts/resources/) — community guide expanding on the official docs
  中文翻译：扩展官方文档的社区指南
