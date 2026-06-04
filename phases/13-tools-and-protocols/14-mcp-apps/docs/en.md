# MCP Apps — Interactive UI Resources via `ui://` | MCP 应用：通过 `ui://` 实现交互式 UI 资源

> Text-only tool output caps what agents can show. MCP Apps (SEP-1724, official January 26, 2026) let a tool return sandboxed interactive HTML rendered inline in Claude Desktop, ChatGPT, Cursor, Goose, and VS Code. Dashboards, forms, maps, 3D scenes, all through one extension. This lesson walks the `ui://` resource scheme, the `text/html;profile=mcp-app` MIME, the iframe-sandbox postMessage protocol, and the security surface that comes with letting a server render HTML.

> **【中文解读】** 传统的 MCP 工具只能返回纯文本。MCP Apps（2026年1月26日发布的 SEP-1724 扩展）让工具能够返回沙盒化的交互式 HTML，在 Claude Desktop、ChatGPT、Cursor 等客户端中内联渲染。仪表盘、表单、地图、3D 场景都可以通过这一扩展实现。

> **【拓展】** MCP Apps 是 MCP 协议从"工具调用"走向"应用平台"的关键一步。类似于微信小程序之于微信，MCP Apps 让 MCP 服务器能提供完整的交互式用户体验。Claude 协议生态中的 AppRenderer（服务端）和 AppFrame（客户端）SDK 原语进一步简化了开发。

**Type:** Build
**Languages:** Python (stdlib, UI resource emitter), HTML (sample app)
**Prerequisites:** Phase 13 · 07 (MCP server), Phase 13 · 10 (resources)
**Time:** ~75 minutes

## Learning Objectives

- Return a `ui://` resource from a tool call and set the correct MIME and metadata.
- Declare a tool's associated UI with `_meta.ui.resourceUri`, `_meta.ui.csp`, and `_meta.ui.permissions`.
- Implement the iframe sandbox postMessage JSON-RPC for UI-to-host communication.
- Apply CSP and permissions-policy defaults that defend against UI-originated attacks.

> **【中文解读】** 学习目标：从工具调用返回 `ui://` 资源；通过 `_meta.ui` 声明 UI 关联；实现 iframe 沙盒的 postMessage JSON-RPC 通信；应用 CSP 和权限策略防御 UI 来源的攻击。

## The Problem | 问题引入

> **【中文解读】** 问题是：MCP 工具只能返回纯文本段落，用户实际需要的是交互式界面（如时间线、仪表盘）。MCP Apps 标准化了这一契约——工具返回 `ui://` 资源，客户端在沙盒 iframe 中渲染。一个服务器、一个 HTML 包，在所有兼容客户端中通用渲染。

A 2025-era `visualize_timeline` tool can return "Here are 14 notes organized chronologically: ...". That is a paragraph. Users actually want the interactive timeline. Before MCP Apps, the options were: client-specific widget APIs (Claude artifacts, OpenAI Custom GPT HTML), or no UI at all.

MCP Apps (SEP-1724, shipped January 26, 2026) standardize the contract. A tool result contains a `resource` whose URI is `ui://...` and whose MIME is `text/html;profile=mcp-app`. The host renders it in a sandboxed iframe with a limited CSP and no network access unless explicitly granted. The UI inside the iframe posts messages to the host via a tiny postMessage JSON-RPC dialect.

Every compatible client (Claude Desktop, ChatGPT, Goose, VS Code) renders the same `ui://` resource the same way. One server, one HTML bundle, universal UI.

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

- `sandbox="allow-scripts allow-same-origin"` (or stricter per server declaration)
- Server-declared CSP applied via response headers.
- No cookies, no localStorage from the host's origin.
- Network access limited to `connectSrc` in CSP.

### postMessage protocol

> **【中文解读】** postMessage 协议：iframe 通过 `window.postMessage` 与宿主通信，使用微型 JSON-RPC 2.0 方言。可用的宿主方法包括 `host.callTool`（调用工具）、`host.readResource`（读取资源）、`host.getPrompt`（获取提示词）、`host.close`（关闭 UI）。每项调用仍通过 MCP 协议并继承服务器权限。

The iframe communicates with the host via `window.postMessage`. A tiny JSON-RPC 2.0 dialect:

Always pin `targetOrigin` to the peer's exact origin, and on the receiving side validate `event.origin` against an allowlist before processing any payload. Never use `"*"` for either side of this channel — the body carries tool calls and resource reads.

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

- `host.callTool(name, arguments)` — invokes a server tool.
- `host.readResource(uri)` — reads an MCP resource.
- `host.getPrompt(name, arguments)` — fetches a prompt template.
- `host.close()` — dismisses the UI.

Every call still goes through the MCP protocol and inherits the server's permissions.

### Permissions

> **【中文解读】** 权限系统：`_meta.ui.permissions` 列表请求额外能力（camera、microphone、geolocation、network:*），每项权限在 UI 渲染前需要用户确认。

The `_meta.ui.permissions` list requests extra capabilities:

- `camera` — access the user's camera (used for scan-a-document UIs).
- `microphone` — voice input.
- `geolocation` — location.
- `network:*` — wider network access than `connectSrc` alone allows.

Each permission is a prompt the user sees before the UI renders.

### Security risks

> **【中文解读】** 安全风险：(1) UI 提示注入——恶意 UI 显示伪装系统消息的文本；(2) `connectSrc` 数据外泄——CSP 允许 `*` 时 UI 可向任何地址发送数据；(3) 点击劫持——UI 覆盖宿主界面；(4) 焦点劫持——UI 捕获键盘焦点。

> **【拓展】** MCP 安全是一个纵深防御体系。Phase 13 · 15 专门讲解工具投毒等七种攻击类型。MCP Apps 的安全依赖于 CSP 策略的严格程度和宿主对 UI 元素的可视区分。

HTML in an iframe is still HTML. New attack surface:

- **Prompt-injection via UI.** A malicious server UI can show text that looks like a system message and tricks the user. Host rendering should visibly distinguish server UI from host UI.
- **Exfiltration via `connectSrc`.** If CSP permits `connect-src: *`, the UI can send data anywhere. Default should be strict.
- **Clickjacking.** The UI overlays host chrome. Hosts must prevent z-index manipulation and enforce opacity rules.
- **Steal focus.** UI takes keyboard focus and captures the next message. Hosts must intercept.

Phase 13 · 15 covers these in depth as part of MCP security; this lesson introduces them.

### `ui/initialize` handshake

> **【中文解读】** `ui/initialize` 握手：iframe 加载后发送 `ui/initialize` postMessage，包含 theme、locale、sessionId。宿主响应能力和会话令牌，后续所有宿主调用都携带此令牌。

After the iframe loads, it sends `ui/initialize` over postMessage:

```json
{"jsonrpc": "2.0", "id": 0, "method": "ui/initialize",
 "params": {"theme": "dark", "locale": "en-US", "sessionId": "..."}}
```

Host responds with capabilities and a session token. The UI uses the session token on every subsequent host call.

### AppRenderer / AppFrame SDK primitives

> **【中文解读】** AppRenderer（服务端）将 React/Vue/Solid 组件封装为 `ui://` 资源；AppFrame（客户端）接收资源、挂载 iframe 并中介 postMessage。可以手写 HTML 和 JSON-RPC 替代。

> **【拓展】** Claude 协议生态中，ext-apps SDK 提供了这两个便捷原语。AppRenderer 负责将框架组件转换为 MCP Apps 能理解的格式，AppFrame 负责在宿主中安全渲染。

The ext-apps SDK exposes two convenience primitives:

- `AppRenderer` (server side) — wraps a React / Vue / Solid component and emits a `ui://` resource with the right MIME and metadata.
- `AppFrame` (client side) — receives the resource, mounts the iframe, and mediates postMessage.

You can use these or hand-roll the HTML and JSON-RPC.

### Ecosystem status

> **【中文解读】** 生态系统状态：MCP Apps 于 2026年1月26日发布。Claude Desktop 全面支持；ChatGPT 通过 Apps SDK 支持；Cursor Beta；VS Code 仅 Insider 构建；Goose 全面支持。生产中的服务器包括仪表盘、地图可视化、数据表格、图表构建器、沙盒 IDE 预览。

MCP Apps shipped January 26, 2026. Client support as of April 2026:

- **Claude Desktop.** Full support since January 2026.
- **ChatGPT.** Full support via the Apps SDK (same underlying MCP Apps protocol).
- **Cursor.** Beta; enable via settings.
- **VS Code.** Insider builds only.
- **Goose.** Full support.
- **Zed, Windsurf.** Roadmapped.

Servers in production: dashboards, map visualizations, data tables, chart builders, sandbox IDE previews.

## Use It | 用框架实现

> **【中文解读】** `code/main.py` 扩展了笔记服务器，添加 `visualize_timeline` 工具返回 `ui://notes/timeline` 资源，以及 `resources/read` 处理器返回完整 HTML+SVG 时间线。HTML 使用标准库模板生成，postMessage 以 JS 注释形式记录。关注点：`_meta.ui` 携带 resourceUri/CSP/permissions；HTML 无需网络访问，数据全部内联；JS 通过 `window.parent.postMessage` 调用 `host.callTool`。

`code/main.py` extends the notes server with a `visualize_timeline` tool that returns a `ui://notes/timeline` resource, plus a handler for `resources/read` on that URI which returns a small but complete HTML bundle with an SVG timeline. The HTML is stdlib-templated — no build system. postMessage is sketched in JS comments since stdlib cannot drive a browser.

What to look at:

- `_meta.ui` on the tool response carries resourceUri, CSP, permissions.
- The HTML renders without network access; all data is inlined.
- JS calls `host.callTool` via `window.parent.postMessage` (documented but inert in this stdlib demo).

## Ship It | 产出物

> **【中文解读】** 本课产出 `outputs/skill-mcp-apps-spec.md`——给定一个需要交互式 UI 的工具，生成完整的 MCP Apps 契约：`ui://` URI、CSP、权限、postMessage 入口和安全检查清单。

This lesson produces `outputs/skill-mcp-apps-spec.md`. Given a tool that would benefit from an interactive UI, the skill produces the full MCP Apps contract: `ui://` URI, CSP, permissions, postMessage entrypoints, and a security checklist.

## Exercises | 练习题

1. Run `code/main.py` and inspect the HTML emitted. Open the HTML directly in a browser; verify the SVG renders. Then sketch the postMessage contract the UI would use to call `host.callTool("notes_update", ...)`.

2. Tighten the CSP: remove `'unsafe-inline'` and use a nonce-based script policy. What changes in the HTML generation code?

3. Add a second UI resource `ui://notes/editor` with a form for editing a note in place. When the user submits, the iframe calls `host.callTool("notes_update", ...)`.

4. Audit the UI's attack surface. Where could a malicious server inject content? What does the iframe sandbox defend against and what does it not?

5. Read the SEP-1724 spec and identify one capability in the MCP Apps SDK that this toy implementation does not use. (Hint: component-level state sync.)

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
- [MCP Apps specification 2026-01-26](https://github.com/modelcontextprotocol/ext-apps/blob/main/specification/2026-01-26/apps.mdx) — formal spec document
- [MCP — Apps extension overview](https://modelcontextprotocol.io/extensions/apps/overview) — high-level documentation
- [MCP blog — MCP Apps launch](https://blog.modelcontextprotocol.io/posts/2026-01-26-mcp-apps/) — January 2026 launch post
- [MCP Apps API reference](https://apps.extensions.modelcontextprotocol.io/api/) — JSDoc-style SDK reference
