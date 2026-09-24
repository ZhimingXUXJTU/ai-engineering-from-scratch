# MCP Apps on the Stateless Protocol | 无状态协议上的 MCP Apps

> An interactive result is still an MCP tool and resource exchange. The 2026-07-28 core makes that exchange self-contained, while the Apps extension adds the sandboxed browser surface.

> **【中文解读】** 一个交互式结果仍然是一次 MCP 工具与资源交换。2026-07-28 核心协议让这次交换自包含（每个请求自带版本与能力，无会话），Apps 扩展在其上叠加沙盒化的浏览器表面。注意本课已完全改版：不再围绕 SEP-1724/ext-apps SDK，而是围绕 `io.modelcontextprotocol/ui` 扩展、`server/discover` 发现、以及"UI 声明在工具定义上（调用前元数据）"这一新契约。

> **【拓展：MCP Apps→Agent 的应用平台】** MCP Apps 是 MCP 协议从"文本工具调用"走向"应用平台"的关键一步，类似微信小程序之于微信：写一次 `ui://` 资源，所有兼容宿主都能渲染。2026-07-28 重设计后，它与无状态核心严格分层——核心管发现/工具/资源，Apps 扩展管 UI 声明与 iframe 桥接，浏览器沙箱管最终边界。

> 🔗 **【前置】** 学本节前请先掌握：(1) Phase 13·07（MCP server）与 13·10（resources）——`ui://` 是资源的一种 scheme，Apps 声明挂在 `tools/list` 和 `resources/read` 上；(2) 2026-07-28 无状态核心（Phase 13·11 MRTR、13·12 elicitation 同源）——每个请求携带 `_meta` 能力，没有 `initialize` 会话；(3) HTML/iframe/postMessage/CSP 基础——沙盒与桥接重度依赖它们。

**Type:** Build | **类型:** 构建
**Languages:** Python | **语言:** Python
**Prerequisites:** Phase 13 · 07 (MCP server), Phase 13 · 10 (resources) | **前置知识:** Phase 13 · 07（MCP server）、Phase 13 · 10（resources）
**Time:** ~75 minutes | **时间:** 约 75 分钟

## Learning Objectives | 学习目标

- Advertise MCP Apps through `server/discover` and per-request extension capabilities.
  中文翻译：通过 `server/discover` 和按请求的扩展能力声明 MCP Apps。
- Declare a `ui://` resource on a tool before the tool is called.
  中文翻译：在工具被调用之前就把 `ui://` 资源声明在工具定义上。
- Return complete tool and resource results on the 2026-07-28 stateless wire.
  中文翻译：在 2026-07-28 无状态线格式上返回完整的工具与资源结果。
- Separate the Apps `ui/initialize` bridge message from the removed MCP core handshake.
  中文翻译：把 Apps 的 `ui/initialize` 桥接消息与已移除的 MCP 核心握手区分开。
- Apply origin validation, sandboxing, CSP, and least-privilege permissions.
  中文翻译：应用源校验、沙箱、CSP 和最小权限。

## The Problem | 问题引入

> **【中文解读】** 文本结果只能"描述"时间线，不能给用户一条能过滤、能检查、能操作的时间线。MCP Apps 用可选扩展解决呈现问题：工具定义指向 `ui://` 资源，宿主可以在工具运行前抓取并审查该资源、在沙箱 iframe 里渲染、并通过 JSON-RPC 桥接中介所有 App 动作。前提是别把 App 包进旧的连接生命周期——2026-07-28 核心没有会话。

A text result can describe a timeline. It cannot give the user a timeline they can filter, inspect, or act on.

> 文本结果可以描述一条时间线。它无法给用户一条能过滤、能检查、能操作的时间线。

MCP Apps solves the presentation problem with an optional extension. A tool definition points to a `ui://` resource. The host can fetch and review that resource before the tool runs, render it in a sandboxed iframe, and mediate all app actions through a JSON-RPC bridge.

> MCP Apps 用一个可选扩展解决呈现问题。工具定义指向一个 `ui://` 资源。宿主可以在工具运行前抓取并审查该资源、在沙箱 iframe 中渲染它、并通过 JSON-RPC 桥接中介所有 App 动作。

The core protocol changed in 2026-07-28. Do not wrap an App in the old connection lifecycle:

> 核心协议在 2026-07-28 变了。不要把 App 包进旧的连接生命周期：

- There is no core `initialize` request or `notifications/initialized` notification.
  中文翻译：没有核心 `initialize` 请求，也没有 `notifications/initialized` 通知。
- There is no `Mcp-Session-Id` header.
  中文翻译：没有 `Mcp-Session-Id` 头。
- Every request carries protocol version and client capabilities in `params._meta`.
  中文翻译：每个请求都在 `params._meta` 中携带协议版本和客户端能力。
- A server implements `server/discover` so clients can inspect versions, core capabilities, and extensions.
  中文翻译：服务器实现 `server/discover`，让客户端能检查版本、核心能力和扩展。
- Every successful result has a `resultType` discriminator.
  中文翻译：每个成功结果都有 `resultType` 判别符。
- Streamable HTTP uses one POST per request. Modern GET and DELETE entrypoints return 405.
  中文翻译：Streamable HTTP 每个请求用一个 POST。现代 GET 与 DELETE 入口返回 405。

The Apps bridge still has a method named `ui/initialize`. It belongs to the iframe postMessage dialect. It does not recreate a core MCP session.

> Apps 桥接仍有一个名为 `ui/initialize` 的方法。它属于 iframe postMessage 方言。它不会重建核心 MCP 会话。

> 💡 **【类比】** MCP Apps 像"AI 助手版微信小程序"，2026 版又把它搬进了"去中心化货架"：以前每个宿主各有一套挂件 API（Claude artifacts、GPT custom HTML），App 作者要逐家适配；现在一个 `ui://` 资源 + 一份扩展声明，任何实现了 `io.modelcontextprotocol/ui` 的宿主都能渲染，且不需要先"登录会话"——每个请求自带身份与能力，像扫码即用的自助点餐机，而不是办会员卡。

## The Concept | 核心概念

> **【中文解读】** 本节走完整个契约链：双协议分层 → 发现（`server/discover`）→ 工具定义上声明 UI（调用前元数据）→ 工具调用只返回数据 → `resources/read` 提供可执行内容 → 按可执行内容缓存 → 线格式歧义先行拒绝 → 沙箱是边界而非信任判决 → 桥接有自己的生命周期 → 宿主上下文与能力撤销 → 降级是契约的一部分。

### Two protocols, one feature

Keep the layers explicit:

> 让各层保持显式：

1. The MCP core carries `server/discover`, `tools/list`, `tools/call`, `resources/list`, and `resources/read`.
   中文翻译：MCP 核心承载 `server/discover`、`tools/list`、`tools/call`、`resources/list` 和 `resources/read`。
2. The MCP Apps extension declares the UI and defines the iframe-to-host bridge.
   中文翻译：MCP Apps 扩展声明 UI 并定义 iframe 到宿主的桥接。
3. Browser sandbox rules limit what the UI can reach.
   中文翻译：浏览器沙箱规则限制 UI 能触达的范围。

The extension identifier is `io.modelcontextprotocol/ui`. Both peers opt in. A client sends extension support inside the capabilities object on each request:

> 扩展标识符是 `io.modelcontextprotocol/ui`。两端都要选择加入。客户端在每个请求的能力对象内发送扩展支持：

```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "method": "server/discover",
  "params": {
    "_meta": {
      "io.modelcontextprotocol/protocolVersion": "2026-07-28",
      "io.modelcontextprotocol/clientCapabilities": {
        "extensions": {
          "io.modelcontextprotocol/ui": {}
        }
      },
      "io.modelcontextprotocol/clientInfo": {
        "name": "timeline-host",
        "version": "1.0.0"
      }
    }
  }
}
```

`clientInfo` is recommended for diagnostics. It is self-reported data, not an authorization identity.

> 建议包含 `clientInfo` 以便诊断。它是自报数据，不是授权身份。

### Discover before rendering

The server's discovery result advertises the extension:

> 服务器的发现结果声明该扩展：

```json
{
  "resultType": "complete",
  "supportedVersions": ["2026-07-28"],
  "capabilities": {
    "tools": {},
    "resources": {},
    "extensions": {
      "io.modelcontextprotocol/ui": {}
    }
  },
  "ttlMs": 300000,
  "cacheScope": "public",
  "_meta": {
    "io.modelcontextprotocol/serverInfo": {
      "name": "timeline-app-server",
      "version": "2.0.0"
    }
  }
}
```

The server must support discovery. A client is not forced to call discovery before every action because each action carries its own capabilities.

> 服务器必须支持发现。客户端不必在每个动作前都调用发现，因为每个动作都自带能力。

### Declare the UI on the tool definition

> **【中文解读】** 这是新版与旧版（SEP-1724 时代）最大的契约差异：UI 不再挂在工具调用结果的 `_meta.ui` 上，而是提前声明在 `tools/list` 的工具定义里（`_meta.ui.resourceUri`）。换来三个好处：宿主可以预加载、缓存、并在结果要求显示之前做安全审查。工具调用本身只返回普通内容加结构化数据——视图绑定关系宿主早就知道了。

The modern Apps contract binds a UI to the tool in `tools/list`:

> 现代 Apps 契约在 `tools/list` 中把 UI 绑定到工具上：

```json
{
  "name": "notes_timeline",
  "description": "Render a timeline of notes.",
  "inputSchema": {
    "type": "object",
    "properties": {}
  },
  "_meta": {
    "ui": {
      "resourceUri": "ui://notes/timeline.html"
    }
  }
}
```

This is deliberately pre-call metadata. The host can preload, cache, and security-review the HTML before a result asks to display it. Older flat metadata keys may be accepted by compatibility code, but new servers should emit the nested `_meta.ui.resourceUri` form.

> 这是有意为之的调用前元数据。宿主可以在结果要求显示之前预加载、缓存并对 HTML 做安全审查。较旧的扁平元数据键可能被兼容代码接受，但新服务器应发出嵌套的 `_meta.ui.resourceUri` 形式。

`tools/list` is cacheable in the current core. Include deterministic ordering, `ttlMs`, and `cacheScope`. Use `private` when the visible tools vary by user or token.

> `tools/list` 在当前核心中是可缓存的。包含确定性排序、`ttlMs` 和 `cacheScope`。当可见工具随用户或令牌变化时使用 `private`。

### Return data, then let the host bind the view

The tool call returns ordinary content plus structured data:

> 工具调用返回普通内容加结构化数据：

```json
{
  "resultType": "complete",
  "content": [
    {"type": "text", "text": "Timeline ready."}
  ],
  "structuredContent": {
    "notes": [
      {"id": "note-1", "title": "Discover", "created": "2026-07-28"}
    ]
  },
  "isError": false
}
```

The host already knows which view belongs to the tool. Avoid inventing a new content block just to repeat the URI.

> 宿主已经知道哪个视图属于该工具。不要为了重复 URI 而发明新的内容块。

### Serve the app as a resource

The server advertises `resources` in discovery, so it also implements the mandatory `resources/list` operation. Its deterministic list entry includes the canonical URI, a stable name, description, and MIME type. The list result includes `resultType`, server identity metadata, `ttlMs`, and `cacheScope`, just like the deterministic tool list.

> 服务器在发现中声明 `resources`，因此也实现强制的 `resources/list` 操作。其确定性列表条目包含规范 URI、稳定名称、描述和 MIME 类型。列表结果包含 `resultType`、服务器身份元数据、`ttlMs` 和 `cacheScope`，与确定性工具列表一致。

The host sends `resources/read`. On Streamable HTTP, the request has:

> 宿主发送 `resources/read`。在 Streamable HTTP 上，请求形如：

```text
POST /mcp
MCP-Protocol-Version: 2026-07-28
Mcp-Method: resources/read
Mcp-Name: ui://notes/timeline.html
```

The header values and JSON-RPC body must match. A mismatch is protocol error `-32020`.

> 头部值与 JSON-RPC 主体必须匹配。不匹配即协议错误 `-32020`。

The result contains the HTML resource and cache hints:

> 结果包含 HTML 资源和缓存提示：

```json
{
  "resultType": "complete",
  "contents": [
    {
      "uri": "ui://notes/timeline.html",
      "mimeType": "text/html;profile=mcp-app",
      "text": "<!doctype html>...",
      "_meta": {
        "ui": {
          "csp": {
            "connectDomains": [],
            "resourceDomains": [],
            "frameDomains": [],
            "baseUriDomains": []
          },
          "permissions": {}
        }
      }
    }
  ],
  "ttlMs": 60000,
  "cacheScope": "public"
}
```

### Cache UI resources as executable content

An App resource is not interchangeable with ordinary prose. Its cache entry can execute bridge code, render tool data, and request host-mediated actions. Key it by canonical `ui://` URI, admitted server identity and version, resource content digest, and authorization context when `cacheScope` is private. Never reuse a private App resource across principals because the HTML or its policy metadata may differ even when the URI is identical.

> App 资源不能与普通文本混为一谈。它的缓存条目可以执行桥接代码、渲染工具数据、请求宿主中介的动作。以规范 `ui://` URI、已准入的服务器身份与版本、资源内容摘要，以及 `cacheScope` 为 private 时的授权上下文作为缓存键。绝不要跨主体复用私有 App 资源——即使 URI 相同，HTML 或其策略元数据也可能不同。

Invalidate the entry when its `ttlMs` expires, the tool's `_meta.ui.resourceUri` binding changes, the server version or admitted descriptor pin changes, or an acknowledged resource-change subscription names the URI. Refetch and reapply CSP and permission review before remounting. A stale iframe must not keep broader permissions merely because a new resource version has not loaded yet.

> 当条目的 `ttlMs` 过期、工具的 `_meta.ui.resourceUri` 绑定变化、服务器版本或已准入描述符锚点变化、或已确认的资源变更订阅点名该 URI 时，使条目失效。重新挂载前重新抓取并重做 CSP 与权限审查。旧 iframe 不能仅因为新资源版本尚未加载就保留更宽的权限。

### Reject wire ambiguity before feature policy

Validation has a deliberate order. First validate the JSON-RPC shape and require string protocol metadata plus an object client capability map. Next compare routing headers with the body. Only then decide whether the matched protocol version is supported. This order prevents a proxy and server from interpreting different requests.

> 校验有刻意的顺序。先校验 JSON-RPC 形状，要求字符串协议元数据和对象型客户端能力映射。再比较路由头与主体。最后才判断匹配到的协议版本是否受支持。这个顺序防止代理与服务器各自解释不同的请求。

| Condition | HTTP | JSON-RPC error |
|-----------|------|----------------|
| Header and body version, method, or name disagree | 400 | `-32020` |
| Header and body agree on an unsupported version | 400 | `-32022`, with `data` exactly `{"supported":["2026-07-28"],"requested":"<actual>"}` |
| `resources/read` lacks the Apps extension capability | 400 | `-32021`, with `data.requiredCapabilities.extensions.io.modelcontextprotocol/ui` |
| Method is unknown | 404 | `-32601` |

> 表格对照（zh 版）：头部与主体的版本/方法/名称不一致——HTTP 400，错误 `-32020`；双方一致但版本不受支持——400，`-32022`，`data` 精确为 `{"supported":["2026-07-28"],"requested":"<actual>"}`；`resources/read` 缺少 Apps 扩展能力——400，`-32021`，`data.requiredCapabilities.extensions.io.modelcontextprotocol/ui`；方法未知——404，`-32601`。

A JSON-RPC notification has no `id`, so the server never emits a JSON-RPC response for it. An accepted HTTP notification returns 202 with an empty body. An error can change the HTTP status, but it still cannot create a JSON-RPC error body for a notification.

> JSON-RPC 通知没有 `id`，所以服务器永不为它发出 JSON-RPC 响应。被接受的 HTTP 通知返回 202 与空主体。错误可以改变 HTTP 状态码，但仍不能为通知生成 JSON-RPC 错误体。

### The sandbox is a boundary, not a trust verdict

> **【中文解读】** 沙箱解决"能不能碰到"，不解决"该不该相信"。宿主控制 iframe：App 不能直接读宿主 cookie、localStorage 或页面 DOM，一切特权操作必须过桥。默认值：CSP 域名列表全空再按需加（`connectDomains` 管 fetch/XHR/WebSocket，`resourceDomains` 管脚本样式图片字体）；能打包就打包；没有可见功能就不要申请摄像头/麦克风/定位；postMessage 钉死精确对端源；工具参数、结果、资源文本、桥接消息全部当不可信输入；用户同意留在宿主——iframe 不能批准自己的重大操作。切记：放行的域名仍是外泄通道，`connectDomains: ["https://api.example.com"]` 意味着 App 内任何脚本都能把获准的数据发往那里。

A host controls the iframe. The App cannot directly read host cookies, local storage, or page DOM. All privileged work must cross the bridge.

> 宿主控制 iframe。App 不能直接读取宿主 cookie、本地存储或页面 DOM。一切特权工作必须经过桥接。

Use these defaults:

> 使用这些默认值：

- Leave all CSP domain lists empty, then add only the origins the App needs. Use `connectDomains` for fetch, XHR, and WebSocket; use `resourceDomains` for scripts, styles, images, and fonts.
  中文翻译：让所有 CSP 域名列表保持为空，然后只添加 App 需要的源。fetch、XHR 和 WebSocket 用 `connectDomains`；脚本、样式、图片和字体用 `resourceDomains`。
- Bundle code and data when practical.
  中文翻译：可行时把代码和数据打包内置。
- Request no camera, microphone, or location permission unless a visible feature needs it.
  中文翻译：除非有可见功能需要，否则不申请摄像头、麦克风或定位权限。
- Pin `postMessage` to the exact peer origin and reject events from every other origin.
  中文翻译：把 `postMessage` 钉在精确的对端源上，拒绝来自其他任何源的事件。
- Treat tool arguments, tool results, resource text, and bridge messages as untrusted input.
  中文翻译：把工具参数、工具结果、资源文本和桥接消息都当作不可信输入。
- Keep user consent in the host. The iframe cannot approve its own consequential action.
  中文翻译：把用户同意留在宿主。iframe 不能批准自己的重大操作。

Do not copy a fixed `sandbox` attribute from a tutorial into every host. The host must choose flags based on the App's origin model and its own isolation design.

> 不要把教程里固定的 `sandbox` 属性复制进每个宿主。宿主必须基于 App 的源模型和自己的隔离设计来选择标志。

An allowed domain is still an exfiltration path. `connectDomains: ["https://api.example.com"]` means any script that executes inside the App can send permitted data there. Exact origin matching prevents destination confusion, but it does not decide whether the payload is appropriate. Keep connect access empty by default, avoid placing bearer tokens in the iframe, proxy narrow operations through the host when practical, limit response and request sizes, and audit which user action caused each outbound request. Treat `resourceDomains` separately from `connectDomains`; permission to load a font or script should not grant arbitrary data upload.

> 被允许的域名仍是一条外泄通道。`connectDomains: ["https://api.example.com"]` 意味着 App 内执行的任何脚本都能把获准的数据发往那里。精确源匹配防止目标混淆，但不判断载荷是否得当。默认保持 connect 访问为空，避免把 bearer 令牌放进 iframe，可行时让窄操作走宿主代理，限制响应与请求大小，并审计每个出站请求由哪个用户动作触发。`resourceDomains` 与 `connectDomains` 要分开对待；加载字体或脚本的权限不应授予任意数据上传。

> ⚠️ **【易错点】** 场景：图省事给 CSP 开 `connectDomains: ["*"]` 或把 `postMessage` 的 targetOrigin 写成 `"*"` / 后果：App 内任何脚本（包括被注入的）都能向任意地址外传数据、接收任意源的恶意消息——精确源匹配只防"发错地方"，不防"发的东西本身不该发" / 修复：域名列表默认全空、按需加白；`targetOrigin` 与 `event.origin` 校验钉死精确对端；加载权（resourceDomains）与上传权（connectDomains）分离；敏感操作走宿主代理并审计。

### The Apps bridge has its own lifecycle

> **【中文解读】** 桥接是 postMessage 上的 JSON-RPC 方言，拥有自己的小生命周期：View 发 `ui/initialize`（带 `appInfo` 和 `appCapabilities`）→ 宿主返回能力与宿主上下文 → View 才发 `ui/notifications/initialized` → 此后宿主才开始向 View 发消息。注意前缀的精确性：核心的 `notifications/initialized` 已被移除，Apps 的 `ui/notifications/initialized` 仍然存在。这个本地握手只建立"一个 iframe 与一个宿主帧"之间的桥，不协商 MCP 协议版本、不创建服务器状态、不铸造传输会话；桥接产生的核心请求是全新的自包含请求（新 JSON-RPC id + 完整请求元数据）。

The Apps bridge is a JSON-RPC dialect over `postMessage`. It can exchange `ui/initialize` and `ui/*` notifications and can proxy core-looking methods such as `tools/call`.

> Apps 桥接是 `postMessage` 上的 JSON-RPC 方言。它可以交换 `ui/initialize` 和 `ui/*` 通知，并可以代理形似核心的方法（如 `tools/call`）。

The View sends `ui/initialize` with `appInfo` and an `appCapabilities` object. The host returns its capabilities and host context. Only after that response does the View send `ui/notifications/initialized`. The host must wait for this Apps notification before sending messages to the View.

> View 发送带 `appInfo` 和 `appCapabilities` 对象的 `ui/initialize`。宿主返回自己的能力与宿主上下文。只有在那次响应之后，View 才发送 `ui/notifications/initialized`。宿主必须等到这条 Apps 通知之后才能向 View 发消息。

That local handshake creates a bridge between one iframe and one host frame. It does not negotiate the MCP protocol version, create server state, or mint a transport session. Notice the exact prefix: core `notifications/initialized` was removed, while Apps `ui/notifications/initialized` remains. A core request generated by a bridged tool call is a new self-contained request with a new JSON-RPC id and full request metadata.

> 那个本地握手在"一个 iframe 与一个宿主帧"之间建立桥接。它不协商 MCP 协议版本、不创建服务器状态、也不铸造传输会话。注意精确前缀：核心的 `notifications/initialized` 已被移除，而 Apps 的 `ui/notifications/initialized` 仍在。桥接工具调用生成的核心请求是一个全新的自包含请求，带新的 JSON-RPC id 和完整请求元数据。

### Host context, actions, and revocation

The host remains the authority after bridge initialization. A View can request a tool action, navigation, clipboard use, or another privileged effect only through a capability the host advertised. The host validates the typed request, current user, target, and arguments, applies approval policy, and may refuse it. A button click and a valid bridge message express intent; neither grants authority.

> 桥接初始化之后宿主仍是权威。View 只能通过宿主声明过的能力请求工具动作、导航、剪贴板或其他特权效果。宿主校验类型化请求、当前用户、目标和参数，应用审批策略，并可以拒绝。按钮点击和合法的桥接消息表达的是意图；两者都不授予权限。

Treat theme, size, and accessibility as changing host context rather than one-time render inputs:

> 把主题、尺寸和无障碍当作会变化的宿主上下文，而非一次性的渲染输入：

- Apply host-provided color and typography tokens, then react when theme or contrast preference changes.
  中文翻译：应用宿主提供的颜色与排版令牌，并在主题或对比度偏好变化时做出反应。
- Let the View report desired dimensions, but let the host cap and apply iframe size so content cannot escape its layout or create deceptive overlays.
  中文翻译：让 View 报告期望尺寸，但由宿主封顶并应用 iframe 尺寸，使内容无法逃出布局或制造欺骗性覆盖层。
- Preserve keyboard order, visible focus, accessible names, screen-reader status, sufficient contrast, zoom, and reduced-motion behavior inside the iframe.
  中文翻译：在 iframe 内保留键盘顺序、可见焦点、无障碍名称、屏幕阅读器状态、足够对比度、缩放和减少动效行为。
- Re-test focus transfer between host controls and View controls after resize and rerender.
  中文翻译：在缩放和重渲染之后重新测试宿主控件与 View 控件之间的焦点转移。

Capabilities can be revoked while the App is open because the user changes account, policy changes, a server is quarantined, or the host narrows consent. Check capability and authorization at action time, not only during `ui/initialize`. On revocation, reject pending privileged calls, stop network activity that no longer fits policy, clear sensitive rendered state, and remount or fall back to text when the UI resource itself is no longer admitted. A View must handle refusal as a normal result, not retry until the host gives in.

> 能力可以在 App 打开期间被撤销——用户切换账号、策略变化、服务器被隔离、宿主收窄同意。在动作时刻检查能力与授权，而不只在 `ui/initialize` 期间。撤销时：拒绝待处理的特权调用、停止不再符合策略的网络活动、清除已渲染的敏感状态，并在 UI 资源本身不再被准入时重新挂载或回退到文本。View 必须把拒绝当作正常结果处理，而不是重试到宿主让步为止。

### Fallback is part of the contract

An Apps-aware server can still serve hosts that do not advertise the UI extension:

> 感知 Apps 的服务器仍能服务未声明 UI 扩展的宿主：

- Return the same tool without `_meta.ui` in `tools/list`.
  中文翻译：在 `tools/list` 中返回不带 `_meta.ui` 的同一工具。
- Keep a useful text result for `tools/call`.
  中文翻译：为 `tools/call` 保留有用的文本结果。
- Refuse `resources/read` for the UI with a missing-capability error.
  中文翻译：对 UI 的 `resources/read` 以缺少能力错误拒绝。
- Never assume an iframe exists when deciding whether the tool completed.
  中文翻译：判断工具是否完成时，永远不要假设 iframe 存在。

```figure
t3-ui-sandbox
```

## Build It | 动手构建

`code/main.py` builds a small in-process protocol model without an SDK. It validates the current request envelope and Streamable HTTP routing values, advertises Apps through `server/discover`, lists tools and resources, executes the tool, and serves a self-contained HTML resource.

> `code/main.py` 构建一个不用 SDK 的小型进程内协议模型。它校验现行请求信封与 Streamable HTTP 路由值、通过 `server/discover` 声明 Apps、列出工具与资源、执行工具、并提供一个自包含的 HTML 资源。

The model receives already parsed bodies and routing headers. It is not a complete HTTP adapter and does not parse `Content-Type` or `Accept`. Use Lesson 09 for the full Streamable HTTP adapter that requires `Content-Type: application/json` and an `Accept` value containing both `application/json` and `text/event-stream`.

> 该模型接收已解析的主体和路由头。它不是完整的 HTTP 适配器，也不解析 `Content-Type` 或 `Accept`。完整的 Streamable HTTP 适配器（要求 `Content-Type: application/json` 且 `Accept` 值同时包含 `application/json` 与 `text/event-stream`）见 Lesson 09。

Run it:

> 运行：

```bash
cd phases/13-tools-and-protocols/14-mcp-apps
python3 code/main.py
python3 -m unittest discover code/tests -v
```

Inspect four things in the output:

> 在输出中检查四件事：

1. Every call is independent.
   中文翻译：每个调用都是独立的。
2. Every request has `_meta` capabilities.
   中文翻译：每个请求都有 `_meta` 能力。
3. `resources/list` returns a stable descriptor before any resource read.
   中文翻译：`resources/list` 在任何资源读取之前返回稳定描述符。
4. Every result has `resultType` and server identity metadata.
   中文翻译：每个结果都有 `resultType` 和服务器身份元数据。
5. No core session identifier appears.
   中文翻译：不出现任何核心会话标识符。

## Use It | 运行验证

Start with `server/discover`. Confirm `io.modelcontextprotocol/ui` appears in the server extension map. Then call `tools/list` twice, once with Apps capability and once without it. The first response declares the resource. The second remains a usable text-only tool.

> 从 `server/discover` 开始。确认 `io.modelcontextprotocol/ui` 出现在服务器扩展映射中。然后调用 `tools/list` 两次，一次带 Apps 能力、一次不带。第一个响应声明资源；第二个仍是可用的纯文本工具。

Read `ui://notes/timeline.html`. Search the HTML for `hostOrigin` and the `event.origin` guard. Those two lines are the minimum visible proof that the bridge does not use a wildcard target.

> 读取 `ui://notes/timeline.html`。在 HTML 中搜索 `hostOrigin` 和 `event.origin` 守卫。这两行是"桥接不使用通配目标"的最小可见证据。

## Ship It | 产出物

This lesson ships `outputs/skill-mcp-apps-spec.md`. Use it to review an App contract before writing framework code. It forces the author to state the current core envelope, extension negotiation, fallback, UI resource, cache policy, CSP, permissions, bridge methods, and consent boundary.

> 本课产出 `outputs/skill-mcp-apps-spec.md`。在写框架代码之前用它审查 App 契约。它强制作者说清现行核心信封、扩展协商、降级、UI 资源、缓存策略、CSP、权限、桥接方法和同意边界。

## Exercises | 练习题

1. Change the client capability to an empty extension map. Confirm `tools/list` keeps the tool but removes the UI binding.
   中文翻译：把客户端能力改为空的扩展映射。确认 `tools/list` 保留工具但移除 UI 绑定。
2. Send `Mcp-Name: ui://notes/other.html` with a body that reads the timeline. Confirm error `-32020`.
   中文翻译：发送 `Mcp-Name: ui://notes/other.html`，主体却读取时间线。确认错误 `-32020`。
3. Change the resource to `cacheScope: private`. Describe the user-specific condition that justifies it.
   中文翻译：把资源改为 `cacheScope: private`。描述支持这一点的用户特定条件。
4. Move the script to `https://static.example.com/app.js`. Add that origin to `resourceDomains` and explain the new supply-chain risk.
   中文翻译：把脚本移到 `https://static.example.com/app.js`。把该源加入 `resourceDomains` 并解释新的供应链风险。
5. Add an `notes_open` tool and route the button click through the host. Keep user approval in the host.
   中文翻译：添加 `notes_open` 工具并让按钮点击经由宿主路由。把用户批准留在宿主。

## Key Terms | 术语速查表

| Term | Meaning |
|------|---------|
| MCP Apps | Optional extension for interactive HTML rendered by an MCP host |
| `io.modelcontextprotocol/ui` | Extension identifier advertised by both peers |
| `ui://` | Resource scheme for an App's UI template |
| `text/html;profile=mcp-app` | MIME type for MCP App HTML |
| `server/discover` | Current RPC for protocol and capability discovery |
| `resources/list` | Mandatory resource listing method when the server advertises resources |
| `resultType` | Required discriminator for modern successful results |
| `ui/initialize` | First Apps bridge request, separate from removed core initialization |
| `ui/notifications/initialized` | Apps View readiness notification sent after the host responds |
| CSP | Browser policy that restricts scripts, styles, images, and network origins |
| Text fallback | Tool behavior retained for a host without Apps support |

> **【中文解读】** 术语速查（中英对照）：MCP Apps=由 MCP 宿主渲染交互式 HTML 的可选扩展；`io.modelcontextprotocol/ui`=两端声明的扩展标识符；`ui://`=App UI 模板的资源 scheme；`text/html;profile=mcp-app`=MCP App HTML 的 MIME 类型；`server/discover`=协议与能力发现的现行 RPC；`resources/list`=服务器声明 resources 后强制的资源列表方法；`resultType`=现代成功结果的必需判别符；`ui/initialize`=Apps 桥接的第一个请求，与已移除的核心初始化无关；`ui/notifications/initialized`=宿主应答后由 View 发出的就绪通知；CSP=限制脚本、样式、图片和网络源的浏览器策略；Text fallback=为不支持 Apps 的宿主保留的文本降级。

## Further Reading | 延伸阅读

- [MCP 2026-07-28 base protocol](https://modelcontextprotocol.io/specification/2026-07-28/basic)
  中文翻译：2026-07-28 基础协议规范。
- [MCP Apps overview](https://modelcontextprotocol.io/extensions/apps/overview)
  中文翻译：MCP Apps 扩展总览。
- [MCP Apps build guide](https://modelcontextprotocol.io/extensions/apps/build)
  中文翻译：MCP Apps 构建指南。
- [Official extension support matrix](https://modelcontextprotocol.io/extensions/client-matrix)
  中文翻译：官方扩展支持矩阵（各客户端对扩展的支持情况）。
