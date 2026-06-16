# Roots and Elicitation — Scoping and Mid-Flight User Input | Roots 与 Elicitation：作用域与飞行中用户输入

> Hard-coded paths break the moment a user opens a different project. Pre-filled tool arguments break when the user under-specifies. Roots scope the server to a user-controlled set of URIs; elicitation pauses mid-tool-call to ask the user for structured input via a form or URL. Two client primitives, two fixes for common MCP failure modes. SEP-1036 (URL-mode elicitation, 2025-11-25) is experimental through H1 2026 — check SDK versions before depending on it.

> **【中文解读】** 硬编码路径在用户打开不同项目时就会出问题。预填的工具参数在用户信息不足时也会出错。Roots 将服务器限定在用户控制的一组 URI 中；Elicitation 在工具调用中途暂停，通过表单或 URL 向用户请求结构化输入。两个客户端原语，修复两个常见的 MCP 失败模式。

> **【拓展：Roots→MCP 安全边界】** Roots 是 MCP 安全模型的基础。客户端通过声明 roots 控制服务器可以访问的文件/资源范围。例如 Claude Desktop 只允许 MCP 服务器访问用户打开的项目目录。Elicitation 则让工具在需要额外信息时安全地向用户请求，而非假设或幻觉参数值。

> 🔗 **【前置】** 学本节前请先掌握：(1) Phase 13·06（MCP Fundamentals）——roots 是六原语之一，elicitation 同样；(2) Phase 13·07（MCP server）——理解 server 端 capability 声明；(3) 表单 / JSON Schema 基础，elicitation 用 schema 描述用户要填的内容。

**Type:** Build | **类型:** 构建
**Languages:** Python (stdlib, roots + elicitation demo) | **语言:** Python (stdlib, roots + elicitation demo)
**Prerequisites:** Phase 13 · 07 (MCP server) | **前置知识:** Phase 13 · 07 (MCP server)
**Time:** ~45 minutes | **时间:** ~45 分钟

## Learning Objectives | 学习目标

- Declare `roots` and respond to `notifications/roots/list_changed`.
  中文翻译：声明 `roots` 并响应 `notifications/roots/list_changed`。
- Restrict server file operations to URIs inside the declared root set.
  中文翻译：将服务器文件操作限制在声明的根集 URI 内。
- Use `elicitation/create` to ask the user for a confirmation or structured input mid-tool-call.
  中文翻译：使用 `elicitation/create` 在工具调用中途向用户请求确认或结构化输入。
- Choose between form-mode and URL-mode elicitation (the latter is experimental; drift-risk noted).
  中文翻译：在表单模式和 URL 模式 elicitation 间选择（后者实验性；漂移风险已注明）。

## The Problem | 问题引入

> **【中文解读】** Roots 解决路径假设问题：客户端在 `initialize` 时声明服务器可触碰的 URI 集合。Elicitation 解决参数缺失问题：服务器暂停工具调用，向用户请求结构化输入。例如"删除旧 TPS 报告笔记"时有三个匹配项，Elicitation 让用户选择具体哪一个。

Two concrete failures a notes MCP server hits in production.

> 笔记 MCP 服务器在生产中遇到的两个具体失败。

**Broken path assumption.** The server is written against `~/notes`. A user on a different machine with notes in `~/Documents/Notes` gets a tool call that fails silently (no file found) or worse, wrote to the wrong place.

> **破裂的路径假设。** 服务器针对 `~/notes` 编写。一个在 `~/Documents/Notes` 存放笔记的不同机器用户会得到一个静默失败的工具调用（找不到文件）或更糟，写到了错误位置。

**Missing argument the user would know.** The user asks "delete the old TPS report note". The model calls `notes_delete(title: "TPS report")` but there are three matching notes from 2023, 2024, and 2025. The tool cannot guess. Failing with "ambiguous" is annoying; running on all three is catastrophic.

> **用户本应知道的缺失参数。** 用户要求"删除旧 TPS 报告笔记"。模型调用 `notes_delete(title: "TPS report")` 但有 2023、2024、2025 三个匹配笔记。工具无法猜测。"模糊"失败令人恼火；在三个上都运行是灾难性的。

Roots fix the first: the client declares at `initialize` the set of URIs the server may touch. Elicitation fixes the second: the server pauses the tool call and sends `elicitation/create` to ask the user to pick which one.

> Roots 修复第一个：客户端在 `initialize` 声明服务器可触及的 URI 集合。Elicitation 修复第二个：服务器暂停工具调用并发送 `elicitation/create` 请求用户选择哪一个。

> 💡 **【类比】** Roots 像酒店的房卡授权。前台（client）发卡时设定"只能开 305 房间和健身房"（roots 列表），客房服务（MCP server）拿着这张卡只能进这些地方，不能去其他客人的房间。Elicitation 像客房服务过程中服务员敲门问"您要哪种枕头？"——服务器在工作时遇到歧义，暂停一下问用户，用户回答后继续。两种原语都把"用户控制权"显式化：前者控制范围，后者控制判断。

## The Concept | 核心概念

### Roots

> **【拓展：Roots 作为安全边界】** Roots 是 MCP 的安全边界机制。客户端声明服务器可访问的目录/URI 集合，服务器必须在边界内操作——任何在根集外的文件读写都应被拒绝。这不是客户端强制执行的（服务器仍是用户信任的代码），而是规范合规的要求。当用户添加或删除根目录时，客户端发送 `notifications/roots/list_changed`。

The client declares a root list at `initialize`:

> 客户端在 `initialize` 中声明根列表：

```json
{
  "capabilities": {"roots": {"listChanged": true}}
}
```

Server can then call `roots/list`:

> 服务器然后可以调用 `roots/list`：

```json
{"roots": [{"uri": "file:///Users/alice/Documents/Notes", "name": "Notes"}]}
```

Servers MUST treat roots as the boundary: any file read or write outside the root set is rejected. This is not enforced by the client (the server is still code the user trusted), but spec-compliant servers honor it.

> 服务器必须将 roots 视为边界：根集外的任何文件读写都被拒绝。这不是客户端强制执行的（服务器仍是用户信任的代码），但规范合规的服务器遵守它。

> ⚠️ **【易错点】** 场景：服务器忽略 roots 检查，直接用绝对路径访问文件 / 后果：(1) 用户在 Claude Desktop 切换项目后，服务器还按旧路径读写，写错地方覆盖用户数据；(2) 安全审计失败——CI/CD 检查 roots 合规性会拒绝发布 / 修复：所有文件操作前必须 `if not path.startswith(root): raise PermissionError`，并在测试用例里覆盖"越界访问"场景。

When the user adds or removes a root, the client sends `notifications/roots/list_changed`. The server re-calls `roots/list` and updates its boundary.

> 当用户添加或删除根时，客户端发送 `notifications/roots/list_changed`。服务器重新调用 `roots/list` 并更新其边界。

### Why roots are a client primitive

Roots are declared by the client because they represent the user's consent model. The user told Claude Desktop "give this notes server access to these two directories". The server cannot widen that scope.

> Roots 由客户端声明，因为它们代表用户的同意模型。用户告诉 Claude Desktop"给这个笔记服务器访问这两个目录"。服务器无法扩大该范围。

> 🤔 **【困惑】** Q: 既然 elicitation 可以问用户，那为什么不每次工具调用都用 elicitation 确认参数？这样最安全。 A: 因为 elicitation 是阻塞的——会暂停整个工具调用，弹出表单让用户填，**严重破坏 Agent 流畅性**。规则：(1) 仅在"信息不足、无法安全继续"时用（如多选项无法消歧）；(2) 不要让用户做模型本可以做的事（如"猜一个城市"应该让模型自己猜，而非问用户）；(3) 生产环境 10 次工具调用里最多 1 次 elicitation，超过就是 UX 设计错误。

### Elicitation: the form-mode default

> **【中文解读】** Elicitation 让服务器在工具执行过程中暂停，向用户请求结构化输入。`elicitation/create` 接受表单 Schema 和自然语言提示。用户填写后响应返回服务器，服务器继续执行。这是 MCP 的"人机协作"原语——让服务器在需要人类判断时优雅暂停。

`elicitation/create` takes a form schema plus a natural-language prompt:

> `elicitation/create` 接受表单 schema 和自然语言提示：

```json
{
  "method": "elicitation/create",
  "params": {
    "message": "Delete 'TPS report'? Multiple notes match; pick one.",
    "requestedSchema": {
      "type": "object",
      "properties": {
        "note_id": {
          "type": "string",
          "enum": ["note-3", "note-7", "note-14"]
        },
        "confirm": {"type": "boolean"}
      },
      "required": ["note_id", "confirm"]
    }
  }
}
```

Client renders a form, collects the user's answer, returns:

> 客户端渲染表单、收集用户答案、返回：

```json
{
  "action": "accept",
  "content": {"note_id": "note-14", "confirm": true}
}
```

Three possible actions: `accept` (user filled it), `decline` (user closed it), `cancel` (user aborted the whole tool call).

> 三种可能动作：`accept`（用户填写了）、`decline`（用户关闭了）、`cancel`（用户中止了整个工具调用）。

Form schemas are flat — nested objects are not supported in v1. SDKs typically reject anything more complex than a single layer.

> 表单 schemas 是扁平的——v1 不支持嵌套对象。SDK 通常拒绝任何比单层更复杂的内容。

### Elicitation: URL mode (SEP-1036, experimental)

New in 2025-11-25. Instead of a schema, the server sends a URL:

> 2025-11-25 新增。服务器发送 URL 而非 schema：

```json
{
  "method": "elicitation/create",
  "params": {
    "message": "Sign in to GitHub",
    "url": "https://github.com/login/oauth/authorize?client_id=..."
  }
}
```

Client opens the URL in a browser, waits for completion, returns when the user comes back. Useful for OAuth flows, payment authorization, and document signing where a form is insufficient.

> 客户端在浏览器中打开 URL，等待完成，用户回来时返回。适用于表单不足的 OAuth 流程、支付授权和文档签署。

Drift-risk note: the SEP-1036 response shape is still settling; some SDKs return the callback URL, others return a completion token. Read your SDK's release notes before using URL mode in production.

> 漂移风险提示：SEP-1036 响应形态仍在稳定；某些 SDK 返回回调 URL，其他返回完成令牌。在生产中使用 URL 模式前阅读你的 SDK 发行说明。

### When elicitation is the right tool

- User confirmation before destructive actions (destructive hint + elicitation).
  中文翻译：破坏性操作前的用户确认（destructive 提示 + elicitation）。
- Disambiguation (pick one of N matches).
  中文翻译：消歧义（从 N 个匹配中选一个）。
- First-run setup (API keys, directories, preferences).
  中文翻译：首次运行设置（API 密钥、目录、偏好）。
- OAuth-style flows (URL mode).
  中文翻译：OAuth 式流程（URL 模式）。

### When elicitation is wrong

- Filling a tool's required arguments that the model could have asked for in prose. Use a normal re-prompt, not an elicitation dialog.
  中文翻译：填充模型本可用散文询问的工具必填参数。使用普通重新提示，而非 elicitation 对话框。
- High-frequency calls. Elicitation interrupts the conversation; do not fire it inside a loop.
  中文翻译：高频调用。Elicitation 中断对话；不要在循环中触发。
- Anything the server could validate after the fact. Validate, return an error, let the model ask the user in text.
  中文翻译：服务器可事后验证的任何内容。验证、返回错误，让模型用文本询问用户。

### Human-in-the-loop bridge

Elicitation plus sampling together enable MCP's "human-in-the-loop" model. A server's agent loop can pause for either user input (elicitation) or model reasoning (sampling). Phase 13 · 11 covered sampling; this lesson covers elicitation. Put them together for full mid-loop control.

> Elicitation 加 sampling 共同实现 MCP 的"人在回路"模型。服务器的 Agent 循环可以为用户输入（elicitation）或模型推理（sampling）暂停。Phase 13 · 11 涵盖 sampling；本课涵盖 elicitation。组合它们获得完整的循环中控制。

## Use It | 用框架实现

`code/main.py` extends the notes server with:

> `code/main.py` 扩展了笔记服务器：

- `roots/list` response that the server re-queries after root-list-changed notifications.
  中文翻译：服务器在 root-list-changed 通知后重新查询的 `roots/list` 响应。
- A `notes_delete` tool that uses `elicitation/create` to disambiguate when multiple notes match.
  中文翻译：多个笔记匹配时使用 `elicitation/create` 消歧的 `notes_delete` 工具。
- A `notes_setup` tool that uses URL-mode elicitation to open a first-run config page (simulated).
  中文翻译：使用 URL 模式 elicitation 打开首次运行配置页（模拟）的 `notes_setup` 工具。
- A boundary check that refuses operations on URIs outside the declared roots.
  中文翻译：拒绝声明 roots 外 URI 操作的边界检查。

The demo runs three scenarios: happy path (one match), disambiguation (three matches, elicitation fires), out-of-root-write (rejected).

> Demo 运行三个场景：正常路径（一个匹配）、消歧义（三个匹配，elicitation 触发）、根外写入（被拒绝）。

## Ship It | 产出物

This lesson produces `outputs/skill-elicitation-form-designer.md`. Given a tool that might need user confirmation or disambiguation, the skill designs the elicitation form schema and the message template.

> 本课产出 `outputs/skill-elicitation-form-designer.md`。给定一个可能需要用户确认或消歧义的工具，该 skill 设计 elicitation 表单 schema 和消息模板。

## Exercises | 练习题

1. Run `code/main.py`. Trigger the disambiguation path; confirm the simulated user answer gets routed back to the tool.
   中文翻译：运行 `code/main.py`。触发消歧义路径；确认模拟用户答案路由回工具。

2. Add a new tool `notes_archive` that requires elicitation confirmation every time (destructive hint). Check the UX: how does this compare to the model re-asking in text?
   中文翻译：添加新工具 `notes_archive`，每次都需要 elicitation 确认（destructive 提示）。检查 UX：这与模型用文本重新询问相比如何？

3. Implement URL-mode elicitation for a first-run OAuth flow. Note the drift risk and add an SDK-version guard.
   中文翻译：为首次运行 OAuth 流程实现 URL 模式 elicitation。注意漂移风险并添加 SDK 版本守卫。

4. Extend `roots/list` handling: when a notification arrives, the server should atomically re-read and rescan open file handles that might now be out of scope.
   中文翻译：扩展 `roots/list` 处理：当通知到达时，服务器应原子地重新读取并重新扫描可能现已超出范围的打开文件句柄。

5. Read the SEP-1036 issue discussion thread on GitHub. Identify one open question that affects how servers should handle URL-mode callbacks.
   中文翻译：阅读 GitHub 上的 SEP-1036 issue 讨论串。识别一个影响服务器如何处理 URL 模式回调的开放问题。

## Key Terms | 术语速查表

| Term | What people say | What it actually means | 中文术语 |
|------|----------------|------------------------|----------|
| Root | "Consent boundary" | URI the client has allowed the server to touch | 根路径（授权边界） |
| `roots/list` | "Server asks for scope" | Client returns the current root set | 查询根路径 |
| `notifications/roots/list_changed` | "User changed scope" | Client signals the root set has mutated | 根路径变更通知 |
| Elicitation | "Ask the user mid-call" | Server-initiated request for structured user input | 用户征询 |
| `elicitation/create` | "The method" | JSON-RPC method for elicitation requests | 征询请求方法 |
| Form mode | "Schema-driven form" | Flat JSON Schema rendered as a form in the client UI | 表单模式 |
| URL mode | "Browser redirect" | SEP-1036 experimental; opens a URL and waits | URL 模式 |
| `accept` / `decline` / `cancel` | "User response outcomes" | Three branches the server handles | 接受/拒绝/取消 |
| Disambiguation | "Pick one" | Common elicitation use case when a tool has N candidates | 消歧义 |
| Flat form | "Top-level properties only" | Elicitation schemas cannot nest | 扁平表单 |

## Further Reading | 延伸阅读

- [MCP — Client roots spec](https://modelcontextprotocol.io/specification/draft/client/roots) — canonical roots reference
  中文翻译：权威 roots 参考
- [MCP — Client elicitation spec](https://modelcontextprotocol.io/specification/draft/client/elicitation) — canonical elicitation reference
  中文翻译：权威 elicitation 参考
- [Cisco — What's new in MCP elicitation, structured content, OAuth enhancements](https://blogs.cisco.com/developer/whats-new-in-mcp-elicitation-structured-content-and-oauth-enhancements) — 2025-11-25 additions walk-through
  中文翻译：2025-11-25 新增功能演练
- [MCP — GitHub SEP-1036](https://github.com/modelcontextprotocol/modelcontextprotocol) — URL-mode elicitation proposal (experimental, drift-risk)
  中文翻译：URL 模式 elicitation 提案（实验性，漂移风险）
- [The New Stack — How elicitation brings human-in-the-loop to AI tools](https://thenewstack.io/how-elicitation-in-mcp-brings-human-in-the-loop-to-ai-tools/) — UX walkthrough
  中文翻译：UX 演练
