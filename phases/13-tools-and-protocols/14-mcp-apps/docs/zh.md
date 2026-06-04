# MCP 应用 — 通过 `ui://` 实现交互式 UI 资源

> 传统的 MCP 工具只能返回纯文本。MCP Apps（SEP-1724，2026年1月26日发布）让工具能够返回沙盒化的交互式 HTML，在 Claude Desktop、ChatGPT、Cursor、Goose 和 VS Code 中内联渲染。仪表盘、表单、地图、3D 场景都可以通过这一扩展实现。本课走通 `ui://` 资源方案、`text/html;profile=mcp-app` MIME、iframe-sandbox postMessage 协议以及让服务器渲染 HTML 带来的安全面。

> **【中文解读】** 传统的 MCP 工具只能返回纯文本。MCP Apps（2026年1月26日发布的 SEP-1724 扩展）让工具能够返回沙盒化的交互式 HTML，在 Claude Desktop、ChatGPT、Cursor 等客户端中内联渲染。仪表盘、表单、地图、3D 场景都可以通过这一扩展实现。

> **【拓展】** MCP Apps 是 MCP 协议从"工具调用"走向"应用平台"的关键一步。类似于微信小程序之于微信，MCP Apps 让 MCP 服务器能提供完整的交互式用户体验。Claude 协议生态中的 AppRenderer（服务端）和 AppFrame（客户端）SDK 原语进一步简化了开发。

**类型：** 构建
**语言：** Python（标准库，UI 资源发射器），HTML（示例应用）
**前置条件：** Phase 13 · 07（MCP 服务器），Phase 13 · 10（资源）
**时间：** 约 75 分钟

## 学习目标

- 从工具调用返回 `ui://` 资源并设置正确的 MIME 和元数据。
- 通过 `_meta.ui.resourceUri`、`_meta.ui.csp` 和 `_meta.ui.permissions` 声明工具关联的 UI。
- 实现 iframe 沙盒的 postMessage JSON-RPC 用于 UI 到宿主的通信。
- 应用 CSP 和权限策略默认值以防御 UI 来源的攻击。

## 问题引入

2025 年的 `visualize_timeline` 工具只能返回"这里有 14 条按时间排列的笔记：..."。这是一段文字。用户实际需要的是交互式时间线。MCP Apps 之前，选项是：客户端特定的小部件 API（Claude artifacts、OpenAI Custom GPT HTML），或者根本没有 UI。

MCP Apps（SEP-1724，2026年1月26日发布）标准化了这一契约。工具结果包含一个 URI 为 `ui://...`、MIME 为 `text/html;profile=mcp-app` 的 `resource`。宿主在沙盒 iframe 中渲染它，带有有限的 CSP 且无网络访问（除非显式授予）。iframe 内的 UI 通过微型 postMessage JSON-RPC 方言与宿主通信。

每个兼容客户端（Claude Desktop、ChatGPT、Goose、VS Code）以相同方式渲染相同的 `ui://` 资源。一个服务器、一个 HTML 包、通用 UI。

## 核心概念

### `ui://` 资源方案

工具返回：

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

宿主然后对 `ui://notes/timeline` URI 调用 `resources/read` 并获取：

```json
{
  "contents": [{
    "uri": "ui://notes/timeline",
    "mimeType": "text/html;profile=mcp-app",
    "text": "<!doctype html>..."
  }]
}
```

### iframe 沙盒

宿主在沙盒 `<iframe>` 中渲染 HTML，带有：

- `sandbox="allow-scripts allow-same-origin"`（或根据服务器声明更严格）
- 服务器声明的 CSP 通过响应头应用。
- 无 cookie、无宿主源的 localStorage。
- 网络访问受 CSP 中的 `connectSrc` 限制。

### postMessage 协议

iframe 通过 `window.postMessage` 与宿主通信。一个微型 JSON-RPC 2.0 方言：

始终将 `targetOrigin` 固定为对等方的确切源，并在接收端根据白名单验证 `event.origin` 后再处理任何载荷。永远不要对此信道的任一侧使用 `"*"`——载荷携带工具调用和资源读取。

```js
// iframe 到宿主（固定到宿主源）
window.parent.postMessage({
  jsonrpc: "2.0",
  id: 1,
  method: "host.callTool",
  params: { name: "notes_update", arguments: { id: "note-14", title: "..." } }
}, "https://host.example.com");

// 宿主到 iframe（固定到 iframe 源）
iframe.contentWindow.postMessage({
  jsonrpc: "2.0",
  id: 1,
  result: { content: [...] }
}, "https://iframe.example.com");
```

UI 可以调用的宿主端方法：

- `host.callTool(name, arguments)` — 调用服务器工具。
- `host.readResource(uri)` — 读取 MCP 资源。
- `host.getPrompt(name, arguments)` — 获取提示模板。
- `host.close()` — 关闭 UI。

每项调用仍通过 MCP 协议并继承服务器的权限。

### 权限

`_meta.ui.permissions` 列表请求额外能力：

- `camera` — 访问用户摄像头（用于扫描文档的 UI）。
- `microphone` — 语音输入。
- `geolocation` — 位置。
- `network:*` — 比 `connectSrc` 单独允许的更广泛的网络访问。

每个权限是 UI 渲染前用户看到的提示。

### 安全风险

iframe 中的 HTML 仍然是 HTML。新的攻击面：

- **通过 UI 的提示注入。** 恶意服务器 UI 可以显示看起来像系统消息的文本并欺骗用户。宿主渲染应明显区分服务器 UI 和宿主 UI。
- **通过 `connectSrc` 的数据外泄。** 如果 CSP 允许 `connect-src: *`，UI 可以向任何地方发送数据。默认应该是严格的。
- **点击劫持。** UI 覆盖宿主界面。宿主必须防止 z-index 操纵并强制不透明度规则。
- **焦点窃取。** UI 获取键盘焦点并捕获下一条消息。宿主必须拦截。

Phase 13 · 15 作为 MCP 安全的一部分深入覆盖这些内容；本课介绍它们。

### `ui/initialize` 握手

iframe 加载后，通过 postMessage 发送 `ui/initialize`：

```json
{"jsonrpc": "2.0", "id": 0, "method": "ui/initialize",
 "params": {"theme": "dark", "locale": "en-US", "sessionId": "..."}}
```

宿主以能力和会话令牌响应。UI 在后续每个宿主调用中使用会话令牌。

### AppRenderer / AppFrame SDK 原语

ext-apps SDK 暴露两个便捷原语：

- `AppRenderer`（服务端）— 包装 React / Vue / Solid 组件并发出带有正确 MIME 和元数据的 `ui://` 资源。
- `AppFrame`（客户端）— 接收资源、挂载 iframe 并中介 postMessage。

你可以使用这些或手写 HTML 和 JSON-RPC。

### 生态系统状态

MCP Apps 于 2026年1月26日发布。截至 2026 年 4 月的客户端支持：

- **Claude Desktop。** 2026年1月起全面支持。
- **ChatGPT。** 通过 Apps SDK 全面支持（相同的底层 MCP Apps 协议）。
- **Cursor。** Beta；通过设置启用。
- **VS Code。** 仅 Insider 构建。
- **Goose。** 全面支持。
- **Zed、Windsurf。** 已规划。

生产中的服务器：仪表盘、地图可视化、数据表格、图表构建器、沙盒 IDE 预览。

## 用框架实现

`code/main.py` 扩展了笔记服务器，添加 `visualize_timeline` 工具返回 `ui://notes/timeline` 资源，以及该 URI 的 `resources/read` 处理器返回一个小而完整的 HTML 包含 SVG 时间线。HTML 使用标准库模板生成——无构建系统。postMessage 以 JS 注释形式记录。

关注点：

- 工具响应上的 `_meta.ui` 携带 resourceUri、CSP、permissions。
- HTML 无需网络访问即可渲染；所有数据内联。
- JS 通过 `window.parent.postMessage` 调用 `host.callTool`（已记录但在此标准库演示中不活跃）。

## 产出物

本课产生 `outputs/skill-mcp-apps-spec.md`。给定一个受益于交互式 UI 的工具，该技能生成完整的 MCP Apps 契约：`ui://` URI、CSP、permissions、postMessage 入口和安全检查清单。

## 练习题

1. 运行 `code/main.py` 并检查发出的 HTML。直接在浏览器中打开 HTML；验证 SVG 渲染。然后勾画 UI 用于调用 `host.callTool("notes_update", ...)` 的 postMessage 契约。

2. 收紧 CSP：移除 `'unsafe-inline'` 并使用基于 nonce 的脚本策略。HTML 生成代码中有什么变化？

3. 添加第二个 UI 资源 `ui://notes/editor`，带有用于就地编辑笔记的表单。用户提交时，iframe 调用 `host.callTool("notes_update", ...)`。

4. 审计 UI 的攻击面。恶意服务器可以在哪里注入内容？iframe 沙盒防御了什么，不能防御什么？

5. 阅读 SEP-1724 规范并识别 MCP Apps SDK 中一个此玩具实现未使用的功能。（提示：组件级状态同步。）

## 术语速查表

| 术语 | 人们怎么说 | 实际含义 | 英文 |
|------|-----------|---------|------|
| MCP 应用 | "交互式 UI 资源" | 2026-01-26 发布的 SEP-1724 扩展 | MCP Apps |
| UI 资源方案 | "App URI 方案" | UI 包的资源方案 | `ui://` |
| MCP App MIME | "内容类型" | MCP App HTML 的内容类型标识 | `text/html;profile=mcp-app` |
| iframe 沙盒 | "渲染容器" | 带 CSP 和权限的浏览器沙盒化 UI | Iframe sandbox |
| UI 到宿主通信 | "UI 到宿主的线" | 用于宿主调用的微型 JSON-RPC-over-postMessage 方言 | postMessage JSON-RPC |
| 工具 UI 绑定 | "工具结果元数据" | 链接工具结果到 UI 资源的元数据 | `_meta.ui` |
| 内容安全策略 | "CSP" | 声明允许的脚本、网络、样式来源 | CSP |
| AppRenderer | "服务端 SDK 原语" | 将框架组件转换为 `ui://` 资源 | AppRenderer |
| AppFrame | "客户端 SDK 原语" | iframe 挂载助手，中介 postMessage | AppFrame |
| UI 初始化握手 | "握手" | UI 到宿主的第一个 postMessage | `ui/initialize` |

## 延伸阅读

- [MCP ext-apps — GitHub](https://github.com/modelcontextprotocol/ext-apps) — 权威实现和 SDK
- [MCP Apps specification 2026-01-26](https://github.com/modelcontextprotocol/ext-apps/blob/main/specification/2026-01-26/apps.mdx) — 正式规范文档
- [MCP — Apps extension overview](https://modelcontextprotocol.io/extensions/apps/overview) — 高级文档
- [MCP blog — MCP Apps launch](https://blog.modelcontextprotocol.io/posts/2026-01-26-mcp-apps/) — 2026 年 1 月发布文章
- [MCP Apps API reference](https://apps.extensions.modelcontextprotocol.io/api/) — JSDoc 风格的 SDK 参考
