# MCP Apps — Interactive UI Resources via `ui://` | MCP 应用：通过 `ui://` 实现交互式 UI 资源

> Text-only tool output caps what agents can show. MCP Apps (SEP-1724, official January 26, 2026) let a tool return sandboxed interactive HTML rendered inline in Claude Desktop, ChatGPT, Cursor, Goose, and VS Code. Dashboards, forms, maps, 3D scenes, all through one extension. This lesson walks the `ui://` resource scheme, the `text/html;profile=mcp-app` MIME, the iframe-sandbox postMessage protocol, and the security surface that comes with letting a server render HTML.

> **【中文解读】** 传统的 MCP 工具只能返回纯文本。MCP Apps（2026年1月26日发布的 SEP-1724 扩展）让工具能够返回沙盒化的交互式 HTML，在 Claude Desktop、ChatGPT、Cursor 等客户端中内联渲染。仪表盘、表单、地图、3D 场景都可以通过这一扩展实现。

> **【拓展】** MCP Apps 是 MCP 协议从"工具调用"走向"应用平台"的关键一步。类似于微信小程序之于微信，MCP Apps 让 MCP 服务器能提供完整的交互式用户体验。Claude 协议生态中的 AppRenderer（服务端）和 AppFrame（客户端）SDK 原语进一步简化了开发。

**Type:** Build | **类型:** 构建
**Languages:** Python (stdlib, UI resource emitter), HTML (sample app) | **语言:** Python (stdlib, UI resource emitter), HTML (sample app)
**Prerequisites:** Phase 13 · 07 (MCP server), Phase 13 · 10 (resources) | **前置知识:** Phase 13 · 07 (MCP server), Phase 13 · 10 (resources)
**Time:** ~75 minutes | **时间:** ~75 分钟

## Learning Objectives | 学习目标

- Return a `ui://` resource from a tool call and set the correct MIME and metadata.
  中文翻译：从工具调用返回 `ui://` 资源，设置正确的 MIME 和元数据。
- Declare a tool's associated UI with `_meta.ui.resourceUri`, `_meta.ui.csp`, and `_meta.ui.permissions`.
  中文翻译：用 `_meta.ui.resourceUri`、`_meta.ui.csp` 和 `_meta.ui.permissions` 声明工具关联的 UI。
- Implement the iframe sandbox postMessage JSON-RPC for UI-to-host communication.
  中文翻译：实现 iframe 沙盒 postMessage JSON-RPC 用于 UI 到宿主的通信。
- Apply CSP and permissions-policy defaults that defend against UI-originated attacks.

> **【中文解读】** 学习目标：从工具调用返回 `ui://` 资源；通过 `_meta.ui` 声明 UI 关联；实现 iframe 沙盒的 postMessage JSON-RPC 通信；应用 CSP 和权限策略防御 UI 来源的攻击。

## The Problem | 问题引入

> **【中文解读】** 问题是：MCP 工具只能返回纯文本段落，用户实际需要的是交互式界面（如时间线、仪表盘）。MCP Apps 标准化了这一契约——工具返回 `ui://` 资源，客户端在沙盒 iframe 中渲染。一个服务器、一个 HTML 包，在所有兼容客户端中通用渲染。

A 2025-era `visualize_timeline` tool can return "Here are 14 notes organized chronologically: ...". That is a paragraph. Users actually want the interactive timeline. Before MCP Apps, the options were: client-specific widget APIs (Claude artifacts, OpenAI Custom GPT HTML), or no UI at all.

> 一个 2025 时代的 `visualize_timeline` 工具可返回"这里有 14 条按时间排序的笔记：..."。那是一段文字。用户实际想要交互式时间线。MCP Apps 之前，选项是：客户端特定的小组件 API（Claude artifacts、OpenAI Custom GPT HTML）或完全没有 UI。

MCP Apps (SEP-1724, shipped January 26, 2026) standardize the contract. A tool result contains a `resource` whose URI is `ui://...` and whose MIME is `text/html;profile=mcp-app`. The host renders it in a sandboxed iframe with a limited CSP and no network access unless explicitly granted. The UI inside the iframe posts messages to the host via a tiny postMessage JSON-RPC dialect.

> MCP Apps（SEP-1724，2026 年 1 月 26 日发布）标准化契约。工具结果包含一个 `resource`，其 URI 为 `ui://...`、MIME 为 `text/html;profile=mcp-app`。宿主在沙盒 iframe 中渲染它，带有限 CSP，无网络访问除非显式授予。iframe 内的 UI 通过微型 postMessage JSON-RPC 方言向宿主发消息。

Every compatible client (Claude Desktop, ChatGPT, Goose, VS Code) renders the same `ui://` resource the same way. One server, one HTML bundle, universal UI.

> 每个兼容客户端（Claude Desktop、ChatGPT、Goose、VS Code）以相同方式渲染相同的 `ui://` 资源。一个服务器、一个 HTML 包、通用 UI。

## The Concept | 核心概念

> **【中文解读】** 本节核心概念：`ui://` 资源方案、iframe 沙盒、postMessage 协议、权限系统、安全风险，以及 `ui/initialize` 握手和 AppRenderer/AppFrame SDK 原语。

### The `ui://` resource scheme

> **【中文解读】** `ui://` 资源方案：工具返回的响应中包含一个 `ui_resource` 类型的内容块，`_meta.ui` 携带 resourceUri、CSP 和权限声明。客户端随后调用 `resources/read` 获取实际 HTML，MIME 类型为 `text/html;profile=mcp-app`。

A tool returns:

```json
{
  "content": [
    {"type": "text", "text": "Here is your notes timeline:"},
    {"type": "ui_resource", "uri": "ui://notes/timeline"}
  ],
  "_meta": {
    "ui": {
      "resourceUri": "ui://notes/timeline",
      "csp": {
        "defaultSrc": "'self'",
        "scriptSrc": "'self' 'unsafe-inline'",
        "connectSrc": "'self'"
      },
      "permissions": []
    }
  }
}
```

The host then calls `resources/read` on the `ui://notes/timeline` URI and gets back:

> 宿主然后调用 `resources/read` 在 `ui://notes/timeline` URI 上并取回：

```json
{
  "contents": [{
    "uri": "ui://notes/timeline",
    "mimeType": "text/html;profile=mcp-app",
    "text": "<!doctype html>..."
  }]
}
```

### Iframe sandbox

> **【中文解读】** iframe 沙盒：HTML 在沙盒 `<iframe>` 中渲染，带 `sandbox="allow-scripts allow-same-origin"`。服务器声明的 CSP 通过响应头应用。无 cookie、无宿主源的 localStorage，网络访问受 `connectSrc` 限制。

The host renders the HTML inside a sandboxed `<iframe>` with:

> 宿主在沙盒 `<iframe>` 中渲染 HTML，带：

- `sandbox="allow-scripts allow-same-origin"` (or stricter per server declaration)
  中文翻译：`sandbox="allow-scripts allow-same-origin"`（或按服务器声明更严格）。
- Server-declared CSP applied via response headers.
  中文翻译：服务器声明的 CSP 通过响应头应用。
- No cookies, no localStorage from the host's origin.
  中文翻译：无 cookie，无来自宿主源的 localStorage。
- Network access limited to `connectSrc` in CSP.
  中文翻译：网络访问限制为 CSP 中的 `connectSrc`。

### postMessage protocol

> **【中文解读】** postMessage 协议：iframe 通过 `window.postMessage` 与宿主通信，使用微型 JSON-RPC 2.0 方言。可用的宿主方法包括 `host.callTool`（调用工具）、`host.readResource`（读取资源）、`host.getPrompt`（获取提示词）、`host.close`（关闭 UI）。每项调用仍通过 MCP 协议并继承服务器权限。

The iframe communicates with the host via `window.postMessage`. A tiny JSON-RPC 2.0 dialect:

> iframe 通过 `window.postMessage` 与宿主通信。一个微型 JSON-RPC 2.0 方言：

Always pin `targetOrigin` to the peer's exact origin, and on the receiving side validate `event.origin` against an allowlist before processing any payload. Never use `"*"` for either side of this channel — the body carries tool calls and resource reads.

> 始终将 `targetOrigin` 固定为对端的精确源，并在接收端处理任何负载前根据白名单验证 `event.origin`。永远不要在此通道的任一侧使用 `"*"`——主体携带工具调用和资源读取。

```js
// iframe to host  (pin to host origin)
window.parent.postMessage({
  jsonrpc: "2.0",
  id: 1,
  method: "host.callTool",
  params: { name: "notes_update", arguments: { id: "note-14", title: "..." } }
}, "https://host.example.com");

// host to iframe  (pin to iframe origin)
iframe.contentWindow.postMessage({
  jsonrpc: "2.0",
  id: 1,
  result: { content: [...] }
}, "https://iframe.example.com");

// receiver on both sides
window.addEventListener("message", (event) => {
  if (event.origin !== "https://expected-peer.example.com") return;
  // safe to process event.data
});
```

Available host-side methods the UI can call:

> UI 可调用的宿主端方法：

- `host.callTool(name, arguments)` — invokes a server tool.
  中文翻译：`host.callTool(name, arguments)`——调用服务器工具。
- `host.readResource(uri)` — reads an MCP resource.
  中文翻译：`host.readResource(uri)`——读取 MCP 资源。
- `host.getPrompt(name, arguments)` — fetches a prompt template.
  中文翻译：`host.getPrompt(name, arguments)`——获取提示模板。
- `host.close()` — dismisses the UI.
  中文翻译：`host.close()`——关闭 UI。

Every call still goes through the MCP protocol and inherits the server's permissions.

> 每次调用仍通过 MCP 协议并继承服务器的权限。

### Permissions

> **【中文解读】** 权限系统：`_meta.ui.permissions` 列表请求额外能力（camera、microphone、geolocation、network:*），每项权限在 UI 渲染前需要用户确认。

The `_meta.ui.permissions` list requests extra capabilities:

> `_meta.ui.permissions` 列表请求额外能力：

- `camera` — access the user's camera (used for scan-a-document UIs).
  中文翻译：`camera`——访问用户摄像头（用于扫描文档 UI）。
- `microphone` — voice input.
  中文翻译：`microphone`——语音输入。
- `geolocation` — location.
  中文翻译：`geolocation`——位置。
- `network:*` — wider network access than `connectSrc` alone allows.
  中文翻译：`network:*`——比 `connectSrc` 单独允许的更宽网络访问。

Each permission is a prompt the user sees before the UI renders.

> 每个权限是 UI 渲染前用户看到的提示。

### Security risks

> **【中文解读】** 安全风险：(1) UI 提示注入——恶意 UI 显示伪装系统消息的文本；(2) `connectSrc` 数据外泄——CSP 允许 `*` 时 UI 可向任何地址发送数据；(3) 点击劫持——UI 覆盖宿主界面；(4) 焦点劫持——UI 捕获键盘焦点。

> **【拓展】** MCP 安全是一个纵深防御体系。Phase 13 · 15 专门讲解工具投毒等七种攻击类型。MCP Apps 的安全依赖于 CSP 策略的严格程度和宿主对 UI 元素的可视区分。

HTML in an iframe is still HTML. New attack surface:

> iframe 中的 HTML 仍是 HTML。新的攻击面：

- **Prompt-injection via UI.** A malicious server UI can show text that looks like a system message and tricks the user. Host rendering should visibly distinguish server UI from host UI.
  中文翻译：**通过 UI 的提示注入。** 恶意服务器 UI 可显示看起来像系统消息的文本并欺骗用户。宿主渲染应明显区分服务器 UI 和宿主 UI。
- **Exfiltration via `connectSrc`.** If CSP permits `connect-src: *`, the UI can send data anywhere. Default should be strict.
  中文翻译：**通过 `connectSrc` 的数据外泄。** 如果 CSP 允许 `connect-src: *`，UI 可向任何地方发送数据。默认应严格。
- **Clickjacking.** The UI overlays host chrome. Hosts must prevent z-index manipulation and enforce opacity rules.
  中文翻译：**点击劫持。** UI 覆盖宿主 chrome。宿主必须防止 z-index 操作并强制不透明度规则。
- **Steal focus.** UI takes keyboard focus and captures the next message. Hosts must intercept.
  中文翻译：**窃取焦点。** UI 获取键盘焦点并捕获下一条消息。宿主必须拦截。

Phase 13 · 15 covers these in depth as part of MCP security; this lesson introduces them.

> Phase 13 · 15 作为 MCP 安全的一部分深入讲解这些；本课介绍它们。

### `ui/initialize` handshake

> **【中文解读】** `ui/initialize` 握手：iframe 加载后发送 `ui/initialize` postMessage，包含 theme、locale、sessionId。宿主响应能力和会话令牌，后续所有宿主调用都携带此令牌。

After the iframe loads, it sends `ui/initialize` over postMessage:

> iframe 加载后，通过 postMessage 发送 `ui/initialize`：

```json
{"jsonrpc": "2.0", "id": 0, "method": "ui/initialize",
 "params": {"theme": "dark", "locale": "en-US", "sessionId": "..."}}
```

Host responds with capabilities and a session token. The UI uses the session token on every subsequent host call.

> 宿主响应能力和会话令牌。UI 在每次后续宿主调用中使用会话令牌。

### AppRenderer / AppFrame SDK primitives

> **【中文解读】** AppRenderer（服务端）将 React/Vue/Solid 组件封装为 `ui://` 资源；AppFrame（客户端）接收资源、挂载 iframe 并中介 postMessage。可以手写 HTML 和 JSON-RPC 替代。

> **【拓展】** Claude 协议生态中，ext-apps SDK 提供了这两个便捷原语。AppRenderer 负责将框架组件转换为 MCP Apps 能理解的格式，AppFrame 负责在宿主中安全渲染。

The ext-apps SDK exposes two convenience primitives:

> ext-apps SDK 暴露两个便捷原语：

- `AppRenderer` (server side) — wraps a React / Vue / Solid component and emits a `ui://` resource with the right MIME and metadata.
  中文翻译：`AppRenderer`（服务器端）——包装 React/Vue/Solid 组件并发出带正确 MIME 和元数据的 `ui://` 资源。
- `AppFrame` (client side) — receives the resource, mounts the iframe, and mediates postMessage.
  中文翻译：`AppFrame`（客户端）——接收资源、挂载 iframe 并中介 postMessage。

You can use these or hand-roll the HTML and JSON-RPC.

> 你可以使用这些或手写 HTML 和 JSON-RPC。

### Ecosystem status

> **【中文解读】** 生态系统状态：MCP Apps 于 2026年1月26日发布。Claude Desktop 全面支持；ChatGPT 通过 Apps SDK 支持；Cursor Beta；VS Code 仅 Insider 构建；Goose 全面支持。生产中的服务器包括仪表盘、地图可视化、数据表格、图表构建器、沙盒 IDE 预览。

MCP Apps shipped January 26, 2026. Client support as of April 2026:

> MCP Apps 于 2026 年 1 月 26 日发布。截至 2026 年 4 月的客户端支持：

- **Claude Desktop.** Full support since January 2026.
  中文翻译：**Claude Desktop。** 2026 年 1 月起全面支持。
- **ChatGPT.** Full support via the Apps SDK (same underlying MCP Apps protocol).
  中文翻译：**ChatGPT。** 通过 Apps SDK 全面支持（相同底层 MCP Apps 协议）。
- **Cursor.** Beta; enable via settings.
  中文翻译：**Cursor。** Beta；通过设置启用。
- **VS Code.** Insider builds only.
  中文翻译：**VS Code。** 仅 Insider 构建。
- **Goose.** Full support.
  中文翻译：**Goose。** 全面支持。
- **Zed, Windsurf.** Roadmapped.
  中文翻译：**Zed、Windsurf。** 已规划。

Servers in production: dashboards, map visualizations, data tables, chart builders, sandbox IDE previews.

> 生产中的服务器：仪表盘、地图可视化、数据表、图表构建器、沙盒 IDE 预览。

## Use It | 用框架实现

> **【中文解读】** `code/main.py` 扩展了笔记服务器，添加 `visualize_timeline` 工具返回 `ui://notes/timeline` 资源，以及 `resources/read` 处理器返回完整 HTML+SVG 时间线。HTML 使用标准库模板生成，postMessage 以 JS 注释形式记录。关注点：`_meta.ui` 携带 resourceUri/CSP/permissions；HTML 无需网络访问，数据全部内联；JS 通过 `window.parent.postMessage` 调用 `host.callTool`。

`code/main.py` extends the notes server with a `visualize_timeline` tool that returns a `ui://notes/timeline` resource, plus a handler for `resources/read` on that URI which returns a small but complete HTML bundle with an SVG timeline. The HTML is stdlib-templated — no build system. postMessage is sketched in JS comments since stdlib cannot drive a browser.

> `code/main.py` 扩展笔记服务器，添加 `visualize_timeline` 工具返回 `ui://notes/timeline` 资源，以及该 URI 上 `resources/read` 的处理器，返回一个小但完整的 HTML 包，带 SVG 时间线。HTML 是标准库模板化的——无构建系统。postMessage 在 JS 注释中勾勒，因为标准库无法驱动浏览器。

What to look at:

- `_meta.ui` on the tool response carries resourceUri, CSP, permissions.
  中文翻译：工具响应上的 `_meta.ui` 携带 resourceUri、CSP、permissions。
- The HTML renders without network access; all data is inlined.
  中文翻译：HTML 无网络访问渲染；所有数据内联。
- JS calls `host.callTool` via `window.parent.postMessage` (documented but inert in this stdlib demo).
  中文翻译：JS 通过 `window.parent.postMessage` 调用 `host.callTool`（已文档化但在本标准库 demo 中无效果）。

## Ship It | 产出物

> **【中文解读】** 本课产出 `outputs/skill-mcp-apps-spec.md`——给定一个需要交互式 UI 的工具，生成完整的 MCP Apps 契约：`ui://` URI、CSP、权限、postMessage 入口和安全检查清单。

This lesson produces `outputs/skill-mcp-apps-spec.md`. Given a tool that would benefit from an interactive UI, the skill produces the full MCP Apps contract: `ui://` URI, CSP, permissions, postMessage entrypoints, and a security checklist.

> 本课产出 `outputs/skill-mcp-apps-spec.md`。给定一个可受益于交互式 UI 的工具，该 skill 生成完整的 MCP Apps 契约：`ui://` URI、CSP、权限、postMessage 入口点和安全清单。

## Exercises | 练习题

1. Run `code/main.py` and inspect the HTML emitted. Open the HTML directly in a browser; verify the SVG renders. Then sketch the postMessage contract the UI would use to call `host.callTool("notes_update", ...)`.
   中文翻译：运行 `code/main.py` 并检查发出的 HTML。直接在浏览器中打开 HTML；验证 SVG 渲染。然后勾勒 UI 调用 `host.callTool("notes_update", ...)` 的 postMessage 契约。

2. Tighten the CSP: remove `'unsafe-inline'` and use a nonce-based script policy. What changes in the HTML generation code?
   中文翻译：收紧 CSP：移除 `'unsafe-inline'` 并使用基于 nonce 的脚本策略。HTML 生成代码中改变了什么？

3. Add a second UI resource `ui://notes/editor` with a form for editing a note in place. When the user submits, the iframe calls `host.callTool("notes_update", ...)`.
   中文翻译：添加第二个 UI 资源 `ui://notes/editor`，带表单用于就地编辑笔记。用户提交时，iframe 调用 `host.callTool("notes_update", ...)`。

4. Audit the UI's attack surface. Where could a malicious server inject content? What does the iframe sandbox defend against and what does it not?
   中文翻译：审计 UI 的攻击面。恶意服务器能在哪里注入内容？iframe 沙盒防御什么，不防御什么？

5. Read the SEP-1724 spec and identify one capability in the MCP Apps SDK that this toy implementation does not use. (Hint: component-level state sync.)
   中文翻译：阅读 SEP-1724 规范，识别 MCP Apps SDK 中此玩具实现未使用的一个能力。（提示：组件级状态同步。）

## Key Terms | 术语速查表

| Term | What people say | What it actually means | 中文 |
|------|----------------|------------------------|------|
| MCP Apps | "Interactive UI resources" | SEP-1724 extension shipped 2026-01-26 | MCP 应用：交互式 UI 资源扩展 |
| `ui://` | "App URI scheme" | Resource scheme for UI bundles | UI 资源的 URI 方案 |
| `text/html;profile=mcp-app` | "The MIME" | Content-type for MCP App HTML | MCP App HTML 的内容类型标识 |
| Iframe sandbox | "Render container" | Browser sandboxing of the UI with CSP and permissions | iframe 沙盒渲染容器 |
| postMessage JSON-RPC | "UI-to-host wire" | Tiny JSON-RPC-over-postMessage dialect for host calls | UI 到宿主的 JSON-RPC 通信协议 |
| `_meta.ui` | "Tool-UI binding" | Metadata linking a tool result to a UI resource | 工具与 UI 资源的绑定元数据 |
| CSP | "Content-Security-Policy" | Declares allowed sources for scripts, network, styles | 内容安全策略，限制脚本/网络/样式来源 |
| AppRenderer | "Server SDK primitive" | Converts a framework component into a `ui://` resource | 服务端 SDK 原语，组件转 `ui://` 资源 |
| AppFrame | "Client SDK primitive" | Iframe mount helper that mediates postMessage | 客户端 SDK 原语，iframe 挂载与消息中介 |
| `ui/initialize` | "Handshake" | First postMessage from UI to host | UI 到宿主的初始化握手 |

## Further Reading | 延伸阅读

- [MCP ext-apps — GitHub](https://github.com/modelcontextprotocol/ext-apps) — reference implementation and SDK
  中文翻译：参考实现和 SDK
- [MCP Apps specification 2026-01-26](https://github.com/modelcontextprotocol/ext-apps/blob/main/specification/2026-01-26/apps.mdx) — formal spec document
  中文翻译：正式规范文档
- [MCP — Apps extension overview](https://modelcontextprotocol.io/extensions/apps/overview) — high-level documentation
  中文翻译：高层文档
- [MCP blog — MCP Apps launch](https://blog.modelcontextprotocol.io/posts/2026-01-26-mcp-apps/) — January 2026 launch post
  中文翻译：2026 年 1 月发布公告
- [MCP Apps API reference](https://apps.extensions.modelcontextprotocol.io/api/) — JSDoc-style SDK reference
  中文翻译：JSDoc 风格 SDK 参考
