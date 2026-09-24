# 无状态协议上的 MCP Apps

> 一个交互式结果仍然是一次 MCP 工具与资源交换。2026-07-28 核心协议让这次交换自包含（无会话、每请求自带版本与能力），Apps 扩展在其上叠加沙盒化的浏览器表面。

> **【中文解读】** 一个交互式结果仍然是一次 MCP 工具与资源交换。2026-07-28 核心协议让这次交换自包含，Apps 扩展在其上叠加沙盒化的浏览器表面。注意本课已完全改版：不再围绕 SEP-1724/ext-apps SDK，而是围绕 `io.modelcontextprotocol/ui` 扩展、`server/discover` 发现、以及"UI 声明在工具定义上（调用前元数据）"这一新契约。

> **【拓展：MCP Apps→Agent 的应用平台】** MCP Apps 是 MCP 协议从"文本工具调用"走向"应用平台"的关键一步，类似微信小程序之于微信：写一次 `ui://` 资源，所有兼容宿主都能渲染。2026-07-28 重设计后，它与无状态核心严格分层——核心管发现/工具/资源，Apps 扩展管 UI 声明与 iframe 桥接，浏览器沙箱管最终边界。

> 🔗 **【前置】** 学本节前请先掌握：(1) Phase 13·07（MCP server）与 13·10（resources）——`ui://` 是资源的一种 scheme，Apps 声明挂在 `tools/list` 和 `resources/read` 上；(2) 2026-07-28 无状态核心（Phase 13·11 MRTR、13·12 elicitation 同源）——每个请求携带 `_meta` 能力，没有 `initialize` 会话；(3) HTML/iframe/postMessage/CSP 基础——沙盒与桥接重度依赖它们。

**类型：** 构建
**语言：** Python
**前置条件：** Phase 13 · 07（MCP server）、Phase 13 · 10（resources）
**预计用时：** 约 75 分钟

## 学习目标

- 通过 `server/discover` 和按请求的扩展能力声明 MCP Apps。
- 在工具被调用之前就把 `ui://` 资源声明在工具定义上。
- 在 2026-07-28 无状态线格式上返回完整的工具与资源结果。
- 把 Apps 的 `ui/initialize` 桥接消息与已移除的 MCP 核心握手区分开。
- 应用源校验、沙箱、CSP 和最小权限。

## 问题引入

> **【中文解读】** 文本结果只能"描述"时间线，不能给用户一条能过滤、能检查、能操作的时间线。MCP Apps 用可选扩展解决呈现问题：工具定义指向 `ui://` 资源，宿主可以在工具运行前抓取并审查该资源、在沙箱 iframe 里渲染、并通过 JSON-RPC 桥接中介所有 App 动作。前提是别把 App 包进旧的连接生命周期——2026-07-28 核心没有会话。

文本结果可以描述一条时间线。它无法给用户一条能过滤、能检查、能操作的时间线。

MCP Apps 用一个可选扩展解决呈现问题。工具定义指向一个 `ui://` 资源。宿主可以在工具运行前抓取并审查该资源、在沙箱 iframe 中渲染它、并通过 JSON-RPC 桥接中介所有 App 动作。

核心协议在 2026-07-28 变了。不要把 App 包进旧的连接生命周期：

- 没有核心 `initialize` 请求，也没有 `notifications/initialized` 通知。
- 没有 `Mcp-Session-Id` 头。
- 每个请求都在 `params._meta` 中携带协议版本和客户端能力。
- 服务器实现 `server/discover`，让客户端能检查版本、核心能力和扩展。
- 每个成功结果都有 `resultType` 判别符。
- Streamable HTTP 每个请求用一个 POST。现代 GET 与 DELETE 入口返回 405。

Apps 桥接仍有一个名为 `ui/initialize` 的方法。它属于 iframe postMessage 方言。它不会重建核心 MCP 会话。

> 💡 **【类比】** MCP Apps 像"AI 助手版微信小程序"，2026 版又把它搬进了"去中心化货架"：以前每个宿主各有一套挂件 API（Claude artifacts、GPT custom HTML），App 作者要逐家适配；现在一个 `ui://` 资源 + 一份扩展声明，任何实现了 `io.modelcontextprotocol/ui` 的宿主都能渲染，且不需要先"登录会话"——每个请求自带身份与能力，像扫码即用的自助点餐机，而不是办会员卡。

## 核心概念

> **【中文解读】** 本节走完整个契约链：双协议分层 → 发现（`server/discover`）→ 工具定义上声明 UI（调用前元数据）→ 工具调用只返回数据 → `resources/read` 提供可执行内容 → 按可执行内容缓存 → 线格式歧义先行拒绝 → 沙箱是边界而非信任判决 → 桥接有自己的生命周期 → 宿主上下文与能力撤销 → 降级是契约的一部分。

### 两个协议，一个特性

让各层保持显式：

1. MCP 核心承载 `server/discover`、`tools/list`、`tools/call`、`resources/list` 和 `resources/read`。
2. MCP Apps 扩展声明 UI 并定义 iframe 到宿主的桥接。
3. 浏览器沙箱规则限制 UI 能触达的范围。

扩展标识符是 `io.modelcontextprotocol/ui`。两端都要选择加入。客户端在每个请求的能力对象内发送扩展支持：

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

建议包含 `clientInfo` 以便诊断。它是自报数据，不是授权身份。

### 渲染之前先发现

服务器的发现结果声明该扩展：

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

服务器必须支持发现。客户端不必在每个动作前都调用发现，因为每个动作都自带能力。

### 在工具定义上声明 UI

> **【中文解读】** 这是新版与旧版（SEP-1724 时代）最大的契约差异：UI 不再挂在工具调用结果的 `_meta.ui` 上，而是提前声明在 `tools/list` 的工具定义里（`_meta.ui.resourceUri`）。换来三个好处：宿主可以预加载、缓存、并在结果要求显示之前做安全审查。工具调用本身只返回普通内容加结构化数据——视图绑定关系宿主早就知道了。

现代 Apps 契约在 `tools/list` 中把 UI 绑定到工具上：

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

这是有意为之的调用前元数据。宿主可以在结果要求显示之前预加载、缓存并对 HTML 做安全审查。较旧的扁平元数据键可能被兼容代码接受，但新服务器应发出嵌套的 `_meta.ui.resourceUri` 形式。

`tools/list` 在当前核心中是可缓存的。包含确定性排序、`ttlMs` 和 `cacheScope`。当可见工具随用户或令牌变化时使用 `private`。

### 返回数据，再让宿主绑定视图

工具调用返回普通内容加结构化数据：

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

宿主已经知道哪个视图属于该工具。不要为了重复 URI 而发明新的内容块。

### 把 App 作为资源提供

服务器在发现中声明 `resources`，因此也实现强制的 `resources/list` 操作。其确定性列表条目包含规范 URI、稳定名称、描述和 MIME 类型。列表结果包含 `resultType`、服务器身份元数据、`ttlMs` 和 `cacheScope`，与确定性工具列表一致。

宿主发送 `resources/read`。在 Streamable HTTP 上，请求形如：

```text
POST /mcp
MCP-Protocol-Version: 2026-07-28
Mcp-Method: resources/read
Mcp-Name: ui://notes/timeline.html
```

头部值与 JSON-RPC 主体必须匹配。不匹配即协议错误 `-32020`。

结果包含 HTML 资源和缓存提示：

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

### 把 UI 资源当可执行内容缓存

App 资源不能与普通文本混为一谈。它的缓存条目可以执行桥接代码、渲染工具数据、请求宿主中介的动作。以规范 `ui://` URI、已准入的服务器身份与版本、资源内容摘要，以及 `cacheScope` 为 private 时的授权上下文作为缓存键。绝不要跨主体复用私有 App 资源——即使 URI 相同，HTML 或其策略元数据也可能不同。

当条目的 `ttlMs` 过期、工具的 `_meta.ui.resourceUri` 绑定变化、服务器版本或已准入描述符锚点变化、或已确认的资源变更订阅点名该 URI 时，使条目失效。重新挂载前重新抓取并重做 CSP 与权限审查。旧 iframe 不能仅因为新资源版本尚未加载就保留更宽的权限。

### 先拒绝线格式歧义，再谈特性策略

校验有刻意的顺序。先校验 JSON-RPC 形状，要求字符串协议元数据和对象型客户端能力映射。再比较路由头与主体。最后才判断匹配到的协议版本是否受支持。这个顺序防止代理与服务器各自解释不同的请求。

| 条件 | HTTP | JSON-RPC 错误 |
|------|------|----------------|
| 头部与主体的版本/方法/名称不一致 | 400 | `-32020` |
| 双方一致但版本不受支持 | 400 | `-32022`，`data` 精确为 `{"supported":["2026-07-28"],"requested":"<actual>"}` |
| `resources/read` 缺少 Apps 扩展能力 | 400 | `-32021`，`data.requiredCapabilities.extensions.io.modelcontextprotocol/ui` |
| 方法未知 | 404 | `-32601` |

JSON-RPC 通知没有 `id`，所以服务器永不为它发出 JSON-RPC 响应。被接受的 HTTP 通知返回 202 与空主体。错误可以改变 HTTP 状态码，但仍不能为通知生成 JSON-RPC 错误体。

### 沙箱是边界，不是信任判决

> **【中文解读】** 沙箱解决"能不能碰到"，不解决"该不该相信"。宿主控制 iframe：App 不能直接读宿主 cookie、localStorage 或页面 DOM，一切特权操作必须过桥。默认值：CSP 域名列表全空再按需加；能打包就打包；没有可见功能就不申请摄像头/麦克风/定位；postMessage 钉死精确对端源；一切输入当不可信处理；用户同意留在宿主。切记：放行的域名仍是外泄通道。

宿主控制 iframe。App 不能直接读取宿主 cookie、本地存储或页面 DOM。一切特权工作必须经过桥接。

使用这些默认值：

- 让所有 CSP 域名列表保持为空，然后只添加 App 需要的源。fetch、XHR 和 WebSocket 用 `connectDomains`；脚本、样式、图片和字体用 `resourceDomains`。
- 可行时把代码和数据打包内置。
- 除非有可见功能需要，否则不申请摄像头、麦克风或定位权限。
- 把 `postMessage` 钉在精确的对端源上，拒绝来自其他任何源的事件。
- 把工具参数、工具结果、资源文本和桥接消息都当作不可信输入。
- 把用户同意留在宿主。iframe 不能批准自己的重大操作。

不要把教程里固定的 `sandbox` 属性复制进每个宿主。宿主必须基于 App 的源模型和自己的隔离设计来选择标志。

被允许的域名仍是一条外泄通道。`connectDomains: ["https://api.example.com"]` 意味着 App 内执行的任何脚本都能把获准的数据发往那里。精确源匹配防止目标混淆，但不判断载荷是否得当。默认保持 connect 访问为空，避免把 bearer 令牌放进 iframe，可行时让窄操作走宿主代理，限制响应与请求大小，并审计每个出站请求由哪个用户动作触发。`resourceDomains` 与 `connectDomains` 要分开对待；加载字体或脚本的权限不应授予任意数据上传。

> ⚠️ **【易错点】** 场景：图省事给 CSP 开 `connectDomains: ["*"]` 或把 `postMessage` 的 targetOrigin 写成 `"*"` / 后果：App 内任何脚本（包括被注入的）都能向任意地址外传数据、接收任意源的恶意消息——精确源匹配只防"发错地方"，不防"发的东西本身不该发" / 修复：域名列表默认全空、按需加白；`targetOrigin` 与 `event.origin` 校验钉死精确对端；加载权（resourceDomains）与上传权（connectDomains）分离；敏感操作走宿主代理并审计。

### Apps 桥接有自己的生命周期

> **【中文解读】** 桥接是 postMessage 上的 JSON-RPC 方言，拥有自己的小生命周期：View 发 `ui/initialize`（带 `appInfo` 和 `appCapabilities`）→ 宿主返回能力与宿主上下文 → View 才发 `ui/notifications/initialized` → 此后宿主才开始向 View 发消息。注意前缀的精确性：核心的 `notifications/initialized` 已被移除，Apps 的 `ui/notifications/initialized` 仍然存在。这个本地握手只建立"一个 iframe 与一个宿主帧"之间的桥，不协商 MCP 协议版本、不创建服务器状态、不铸造传输会话。

Apps 桥接是 `postMessage` 上的 JSON-RPC 方言。它可以交换 `ui/initialize` 和 `ui/*` 通知，并可以代理形似核心的方法（如 `tools/call`）。

View 发送带 `appInfo` 和 `appCapabilities` 对象的 `ui/initialize`。宿主返回自己的能力与宿主上下文。只有在那次响应之后，View 才发送 `ui/notifications/initialized`。宿主必须等到这条 Apps 通知之后才能向 View 发消息。

那个本地握手在"一个 iframe 与一个宿主帧"之间建立桥接。它不协商 MCP 协议版本、不创建服务器状态、也不铸造传输会话。注意精确前缀：核心的 `notifications/initialized` 已被移除，而 Apps 的 `ui/notifications/initialized` 仍在。桥接工具调用生成的核心请求是一个全新的自包含请求，带新的 JSON-RPC id 和完整请求元数据。

### 宿主上下文、动作与撤销

桥接初始化之后宿主仍是权威。View 只能通过宿主声明过的能力请求工具动作、导航、剪贴板或其他特权效果。宿主校验类型化请求、当前用户、目标和参数，应用审批策略，并可以拒绝。按钮点击和合法的桥接消息表达的是意图；两者都不授予权限。

把主题、尺寸和无障碍当作会变化的宿主上下文，而非一次性的渲染输入：

- 应用宿主提供的颜色与排版令牌，并在主题或对比度偏好变化时做出反应。
- 让 View 报告期望尺寸，但由宿主封顶并应用 iframe 尺寸，使内容无法逃出布局或制造欺骗性覆盖层。
- 在 iframe 内保留键盘顺序、可见焦点、无障碍名称、屏幕阅读器状态、足够对比度、缩放和减少动效行为。
- 在缩放和重渲染之后重新测试宿主控件与 View 控件之间的焦点转移。

能力可以在 App 打开期间被撤销——用户切换账号、策略变化、服务器被隔离、宿主收窄同意。在动作时刻检查能力与授权，而不只在 `ui/initialize` 期间。撤销时：拒绝待处理的特权调用、停止不再符合策略的网络活动、清除已渲染的敏感状态，并在 UI 资源本身不再被准入时重新挂载或回退到文本。View 必须把拒绝当作正常结果处理，而不是重试到宿主让步为止。

### 降级是契约的一部分

感知 Apps 的服务器仍能服务未声明 UI 扩展的宿主：

- 在 `tools/list` 中返回不带 `_meta.ui` 的同一工具。
- 为 `tools/call` 保留有用的文本结果。
- 对 UI 的 `resources/read` 以缺少能力错误拒绝。
- 判断工具是否完成时，永远不要假设 iframe 存在。

## 动手构建

`code/main.py` 构建一个不用 SDK 的小型进程内协议模型。它校验现行请求信封与 Streamable HTTP 路由值、通过 `server/discover` 声明 Apps、列出工具与资源、执行工具、并提供一个自包含的 HTML 资源。

该模型接收已解析的主体和路由头。它不是完整的 HTTP 适配器，也不解析 `Content-Type` 或 `Accept`。完整的 Streamable HTTP 适配器（要求 `Content-Type: application/json` 且 `Accept` 值同时包含 `application/json` 与 `text/event-stream`）见 Lesson 09。

运行：

```bash
cd phases/13-tools-and-protocols/14-mcp-apps
python3 code/main.py
python3 -m unittest discover code/tests -v
```

在输出中检查四件事：

1. 每个调用都是独立的。
2. 每个请求都有 `_meta` 能力。
3. `resources/list` 在任何资源读取之前返回稳定描述符。
4. 每个结果都有 `resultType` 和服务器身份元数据。
5. 不出现任何核心会话标识符。

## 运行验证

从 `server/discover` 开始。确认 `io.modelcontextprotocol/ui` 出现在服务器扩展映射中。然后调用 `tools/list` 两次，一次带 Apps 能力、一次不带。第一个响应声明资源；第二个仍是可用的纯文本工具。

读取 `ui://notes/timeline.html`。在 HTML 中搜索 `hostOrigin` 和 `event.origin` 守卫。这两行是"桥接不使用通配目标"的最小可见证据。

## 产出物

本课产出 `outputs/skill-mcp-apps-spec.md`。在写框架代码之前用它审查 App 契约。它强制作者说清现行核心信封、扩展协商、降级、UI 资源、缓存策略、CSP、权限、桥接方法和同意边界。

## 练习题

1. 把客户端能力改为空的扩展映射。确认 `tools/list` 保留工具但移除 UI 绑定。

2. 发送 `Mcp-Name: ui://notes/other.html`，主体却读取时间线。确认错误 `-32020`。

3. 把资源改为 `cacheScope: private`。描述支持这一点的用户特定条件。

4. 把脚本移到 `https://static.example.com/app.js`。把该源加入 `resourceDomains` 并解释新的供应链风险。

5. 添加 `notes_open` 工具并让按钮点击经由宿主路由。把用户批准留在宿主。

## 术语速查表

| 术语 | 含义 |
|------|------|
| MCP Apps | 由 MCP 宿主渲染交互式 HTML 的可选扩展 |
| `io.modelcontextprotocol/ui` | 两端声明的扩展标识符 |
| `ui://` | App UI 模板的资源 scheme |
| `text/html;profile=mcp-app` | MCP App HTML 的 MIME 类型 |
| `server/discover` | 协议与能力发现的现行 RPC |
| `resources/list` | 服务器声明 resources 后强制的资源列表方法 |
| `resultType` | 现代成功结果的必需判别符 |
| `ui/initialize` | Apps 桥接的第一个请求，与已移除的核心初始化无关 |
| `ui/notifications/initialized` | 宿主应答后由 View 发出的就绪通知 |
| CSP | 限制脚本、样式、图片和网络源的浏览器策略 |
| Text fallback（文本降级） | 为不支持 Apps 的宿主保留的工具行为 |

> **【中文解读】** 术语速查要点：扩展标识是 `io.modelcontextprotocol/ui`；UI 绑定在工具定义（调用前）而非调用结果；`resources/list` 因声明 resources 而强制；桥接握手（`ui/initialize` + `ui/notifications/initialized`）只是 iframe 与宿主之间的事，别与核心会话混淆；不给 Apps 的宿主留好文本降级是契约的一部分。

## 延伸阅读

- [MCP 2026-07-28 base protocol](https://modelcontextprotocol.io/specification/2026-07-28/basic) — 2026-07-28 基础协议规范
- [MCP Apps overview](https://modelcontextprotocol.io/extensions/apps/overview) — MCP Apps 扩展总览
- [MCP Apps build guide](https://modelcontextprotocol.io/extensions/apps/build) — MCP Apps 构建指南
- [Official extension support matrix](https://modelcontextprotocol.io/extensions/client-matrix) — 官方扩展支持矩阵（各客户端对扩展的支持情况）
