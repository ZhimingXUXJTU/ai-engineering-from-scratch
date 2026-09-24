# 模型上下文协议（MCP）

> MCP 给 AI 宿主一套统一协议来发现和调用工具、资源与提示模板。2026-07-28 修订版把协议改成了无状态：版本与能力上下文随每个请求携带，不再依赖绑定连接的握手。

> **【中文解读】** 本课是 MCP 的第一次系统接触。MCP 由 Anthropic 于 2024 年 11 月首发，现由 Linux 基金会托管，2026 年已成为连接 LLM 与工具/数据源的事实标准。新版最大的变化是"去会话化"：没有 initialize 握手、没有会话 ID，每个请求自证身份。掌握 `params._meta`、`server/discover`、`resultType` 三个关键词，新版 MCP 就掌握了一大半。

> **【拓展：MCP→Phase 13 深入路线】** 本课给出协议模型与最小可运行实现；生产级边界（工具契约、可靠性、注册中心供应链、一致性工程）已被上游拆成 Phase 13 的 28-31 四课，本课末尾有完整路线图。

> 🔗 **【前置】** 学本节前请先掌握：(1) Phase 11·09（Function Calling）；(2) Phase 11·03（Structured Outputs / JSON Schema）；(3) JSON-RPC 2.0 基本概念。学过旧版 MCP 的话，先清掉 `initialize` 握手和 `Mcp-Session-Id` 的记忆——它们已被移除。

**类型：** 构建
**语言：** Python
**前置条件：** Phase 11 · 09（函数调用）、Phase 11 · 03（结构化输出）
**预计用时：** 约 75 分钟

## 学习目标

- 区分 MCP 的宿主（host）、客户端（client）、服务器（server）、传输（transport）与服务器原语。
- 构建携带 MCP 2026-07-28 必需元数据的 JSON-RPC 请求。
- 使用 `server/discover` 探测服务器的版本、身份与能力。
- 从工具、资源和提示返回带类型标记与缓存提示的结果。
- 解释现代无状态 MCP 如何与握手时代的旧服务器互操作。
- 为服务器选择安全的状态、传输与审批边界。

## 问题引入

你的应用需要数据库查询、日历操作和文件读取。没有共享协议时，每个 AI 宿主都要为同样的能力编写定制的发现、调用、错误、传输与授权胶水代码。

MCP 压缩了这个集成矩阵。服务器发布标准 JSON-RPC 接口面；合规的客户端无需服务器专属适配器就能发现接口面、把它呈现给模型或用户、调用它并解释结果。

一个容易忽略的关键边界：MCP 只标准化通信。它不决定模型该调用哪个工具、不会让不可信内容变安全、也不会把无状态请求变成持久的应用状态。这些决策仍归你的宿主和服务器所有。

> 💡 **【类比】** MCP 像"电源插座国标"。没有国标时，每台电器配一种插头，出一次国就要买一次转接头；有了国标，一个插座通吃所有电器。但国标不关心你插的是吹风机还是电钻——用电安全（审批、鉴权）是电器和用户自己的事。

## 核心概念

![MCP 宿主、无状态请求与服务器原语](../assets/mcp-architecture.svg)

### 三个服务器原语

1. **Tools（工具）** 是可调用动作。每个工具有名称、描述、JSON Schema 输入与处理器。
2. **Resources（资源）** 是命名的、URI 寻址的、客户端可读取的内容。
3. **Prompts（提示模板）** 是宿主可以暴露给用户的可复用模板。

宿主是 AI 应用本身；宿主内的一个 MCP 客户端只与一个服务器对话；传输层在两者之间搬运 JSON-RPC 消息。注意"客户端:服务器 = 1:1"——需要多个服务器时就挂多个客户端。

### 无状态请求取代握手

> **【中文解读】** 这是新版最大的变化点。`initialize` 握手、`notifications/initialized` 和协议级会话全部移除，取而代之的是每个请求自带 `params._meta`。缺 `_meta`、缺必填字段或类型不对 → `-32602`；版本格式合法但服务器不支持 → `-32022`。

MCP 2026-07-28 移除了 `initialize` 和 `notifications/initialized`，也移除了协议级会话。每个请求在 `params._meta` 中携带解释该请求所需的上下文：

```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "method": "tools/list",
  "params": {
    "_meta": {
      "io.modelcontextprotocol/protocolVersion": "2026-07-28",
      "io.modelcontextprotocol/clientCapabilities": {},
      "io.modelcontextprotocol/clientInfo": {
        "name": "lesson-client",
        "version": "1.0.0"
      }
    }
  }
}
```

协议版本与客户端能力是必填的，客户端身份是建议提供的。`_meta` 缺失、必填字段缺失或类型错误都是畸形请求，返回 Invalid Params（`-32602`）。格式合法但服务器不支持的版本返回 `UnsupportedProtocolVersionError`（`-32022`）。服务器无需恢复先前的协商记录就能处理合法请求。

"无状态"不等于应用不能有状态，而是状态不能藏在 MCP 连接或 `Mcp-Session-Id` 后面。工作流需要连续性时，由服务器签发一个不透明句柄（handle），客户端在后续调用中把它当普通工具参数传回。鉴权仍然必须逐请求检查。

> ⚠️ **【易错点】** 旧代码把客户端元数据缓存在"连接对象"里、只在握手时发一次——新版服务器会逐请求校验 `_meta`，漏带的请求直接被拒。每个请求都要重建元数据。

### 发现与版本选择

> **【中文解读】** `server/discover` 是新版服务器的必选方法：返回支持的版本、能力与服务器身份，并带 `ttlMs`/`cacheScope` 缓存提示。双时代客户端在 stdio 上先用它探测：收到发现结果或可识别的现代错误（如 `-32022`）说明是现代服务器；遇到无法识别的错误或超时才允许回退到 2025-11-25 的 `initialize` 流程——旧流程是兼容代码，不是现代默认。

每个现代服务器都实现 `server/discover`。结果通告支持的版本、能力与服务器身份：

```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "result": {
    "resultType": "complete",
    "supportedVersions": ["2026-07-28"],
    "capabilities": {
      "tools": {},
      "resources": {},
      "prompts": {}
    },
    "ttlMs": 3600000,
    "cacheScope": "public",
    "_meta": {
      "io.modelcontextprotocol/serverInfo": {
        "name": "demo-server",
        "version": "1.0.0"
      }
    }
  }
}
```

客户端也可以直接调用其他方法并自行处理版本错误，但发现流程让能力展示与版本选择变得显式。不支持的版本返回 `UnsupportedProtocolVersionError`（`-32022`），其 data 包含 `supported`（服务器支持的修订版数组）和 `requested`（被拒绝的修订版）。

在 stdio 上，双时代客户端用 `server/discover` 探测：发现结果或可识别的现代错误（如 `UnsupportedProtocolVersionError`）标识现代服务器；任何未被识别为现代的错误或超时允许回退到 2025-11-25 的 `initialize` 流程。旧行为是兼容代码，不是现代默认。

### 结果是显式的

> **【中文解读】** 每个核心结果都带 `resultType`：`complete` 或 `input_required`。旧式省略 `resultType` 的结果必须按 `complete` 处理。列表/读取结果还带 `ttlMs` 与 `cacheScope`——确定性排序 + 新鲜度提示让客户端可以安全缓存，并提升 prompt cache 命中率。

每个 2026-07-28 核心结果都有 `resultType`：

- `complete` 表示操作已完成。
- `input_required` 表示服务器需要按 Multi Round-Trip Requests（MRTR）模式再来一轮往返。核心服务器只允许从 `tools/call`、`resources/read` 或 `prompts/get` 返回它。

服务器应在每个结果的 `_meta` 中包含 `io.modelcontextprotocol/serverInfo`。这个身份是自报的，用于展示、日志与调试，不能作为安全决策依据。

### 线格式与传输层

> **【中文解读】** 线格式仍是 JSON-RPC 2.0。现代 Streamable HTTP 只暴露一个接受 POST 的端点，每条消息独立一个 POST；请求 POST 的响应是一个 JSON 对象或一条请求级 SSE 流；通知 POST 被接受时返回 HTTP 202 空响应体。没有独立 GET 流、没有 DELETE 会话端点、没有 `Mcp-Session-Id`、没有 `Last-Event-ID` 重放——长期变更通知改用 `subscriptions/listen` POST。

MCP 在 stdio 或 Streamable HTTP 上使用 JSON-RPC 2.0。

- 请求有 `jsonrpc`、`id`、`method` 和 `params`。
- 响应有匹配的 `id`，以及 `result` 或 `error` 二者之一。
- 通知没有 `id`，也不期望响应。

现代 Streamable HTTP 暴露一个接受 POST 的端点。每条 JSON-RPC 消息使用独立的 POST。请求 POST 收到的是一个 JSON 对象，或一个以最终响应结束的请求级 Server-Sent Events 流。被接受的通知 POST 收到 HTTP 202 且无响应体；本核心修订没有定义 Streamable HTTP 上的客户端到服务器通知。

2026-07-28 中没有独立的 MCP GET 流、DELETE 会话端点、`Mcp-Session-Id` 或 `Last-Event-ID` 重放。长期变更通知使用 `subscriptions/listen` POST，其响应保持为打开的 SSE 流。

### 没有服务器主动请求的客户端输入

> **【中文解读】** 旧规范允许服务器反向发请求（sampling/roots/elicitation）；现行协议改用 MRTR：工具调用返回 `resultType: input_required` 并附 `inputRequests`/`requestState`，客户端收集输入后用**新的 JSON-RPC ID** 重试原方法并携带 `inputResponses`，原样回传 `requestState`。Roots/Sampling/Logging 仍可用但已弃用——新实现不要再采用。

旧修订版允许服务器在流上发送 `sampling/createMessage`、`roots/list` 或 `elicitation/create` 等请求。现行协议改用 Multi Round-Trip Requests。合格的工具调用、资源读取或提示获取可以返回 `resultType: input_required`，并至少附带 `inputRequests` 或 `requestState` 之一。客户端收集所请求的输入，用新的 JSON-RPC ID 和相应的 `inputResponses` 重试原方法，并在服务器提供了 `requestState` 时原样回传。如果没有 `inputRequests`，重试时省略 `inputResponses`。

Roots、Sampling 和 Logging 仍可工作但已弃用，新实现不应再采用。现有的 Roots 或 Sampling 请求在 MRTR `inputRequests` 内传输，绝不作为独立的服务器到客户端 JSON-RPC 请求。优先使用显式文件/目录参数、资源 URI、服务器配置和直连模型提供商集成。stdio 诊断用 stderr，生产遥测用 OpenTelemetry。

```figure
mcp-nxm-collapse
```

## 动手构建

### 第一步：注册服务器接口面

注册保持简单，尽管请求契约已经改变：

```python
server = MCPServer("demo-server")

@server.tool(
    "add",
    "Add two integers.",
    {
        "type": "object",
        "properties": {
            "a": {"type": "integer"},
            "b": {"type": "integer"}
        },
        "required": ["a", "b"]
    }
)
def add(a: int, b: int) -> dict:
    return {"sum": a + b}
```

`code/main.py` 中的实现还注册了一个资源和一个提示模板。它刻意只用标准库，让你看清每个信封，而不是把协议委托给 SDK。

### 第二步：给每个请求附加元数据

```python
def request(method, params=None):
    body_params = dict(params or {})
    body_params["_meta"] = {
        "io.modelcontextprotocol/protocolVersion": "2026-07-28",
        "io.modelcontextprotocol/clientCapabilities": {},
        "io.modelcontextprotocol/clientInfo": {
            "name": "demo-client",
            "version": "1.0.0"
        }
    }
    return {
        "jsonrpc": "2.0",
        "id": 1,
        "method": method,
        "params": body_params
    }
```

不要把这些元数据只缓存在连接对象里。服务器逐请求校验它。

### 第三步：可选地在列表前先发现

调用 `server/discover`，选择一个受支持的版本，再调用 `tools/list`。如果你已经知道版本并能处理 `-32022`，直接 `tools/list` 也合法。

演示程序按名称顺序返回工具列表，并附上 `ttlMs`、`cacheScope`、`resultType` 和服务器身份。工具调用返回完整的、不可缓存的结果，因为其输出可能依赖当前状态。

### 第四步：把同一请求映射到 HTTP

远程 `tools/call` POST 包含与 JSON-RPC 请求体镜像的头：

```http
POST /mcp HTTP/1.1
Content-Type: application/json
Accept: application/json, text/event-stream
MCP-Protocol-Version: 2026-07-28
Mcp-Method: tools/call
Mcp-Name: add
```

`MCP-Protocol-Version` 头必须与 `_meta` 中的版本一致。`Mcp-Method` 在每个 JSON-RPC 请求上都是必填的，且必须与 `method` 一致。`Mcp-Name` 只在 `tools/call`、`resources/read` 和 `prompts/get` 上必填，且必须与工具名、资源 URI 或提示名一致。缺失必填头或不一致返回 HTTP 400，错误码 `HeaderMismatch`（`-32020`）。

### 第五步：在协议状态之外落实安全

- 在每个 HTTP 请求上校验授权与受众。
- 本地服务器绑定 localhost，并在 Streamable HTTP 上校验 `Origin`。
- 用 `destructiveHint: true` 标记破坏性工具并要求宿主审批。
- 显式传递目录与文件范围，不要依赖已弃用的 Roots。
- 把资源与工具输出当作不可信数据。
- stdio 下 stdout 保留给 JSON-RPC；诊断信息写到 stderr。

## 运行验证

在课程目录下运行：

```bash
python3 code/main.py
cd code
python3 -m unittest discover tests -v
```

第一行应报告发现 `demo-server`，协议版本 `2026-07-28`。然后检查 `MCPClient.request`：它为每次调用重建 `_meta`。从某个请求中去掉元数据，观察服务器拒绝它。

## 交付产物

`outputs/skill-mcp-server-designer.md` 把一个领域变成无状态 MCP 设计。它的验收门要求：发现结果、逐请求元数据策略、确定性的缓存感知列表、显式状态句柄、传输头、授权与审批规则。

## 继续深入 MCP

> **【中文解读】** 本课给出协议模型；Phase 13 把四个生产边界拆成独立的"构建并验证"课程（28-31 课）。当你的服务器要跨团队或跨信任边界时按顺序学习——四课合起来，把你从"方法能跑通"带到"契约在部署全程保持安全且可诊断"。

本课给你协议模型。Phase 13 把四个生产边界变成独立的构建与验证课程：

1. [MCP 工具契约与内容](../../../13-tools-and-protocols/28-mcp-tool-contracts-and-content/docs/zh.md)覆盖封闭输入 schema、结构化内容、路由元数据、不透明分页、补全授权，以及协议错误与工具域错误的区别。
2. [MCP 可靠性、取消与流控](../../../13-tools-and-protocols/29-mcp-reliability-cancellation-and-flow-control/docs/zh.md)覆盖请求取消、持久任务取消、截止时间、幂等性、背压、代理缓冲与重连行为。
3. [MCP 注册中心供应链、准入、漂移与回滚](../../../13-tools-and-protocols/30-mcp-registry-supply-chain-and-drift/docs/zh.md)覆盖命名空间证明、产物来源、不可变 pin、在线漂移、Registry 状态、准入证据与回滚。
4. [MCP 一致性工程](../../../13-tools-and-protocols/31-mcp-conformance-versioning-and-operations/docs/zh.md)覆盖黄金与负面线格式记录、严格版本时代、SDK 差分、代理证据、脱敏、健康门与发布回滚。

## 练习

1. 添加一个 `subtract` 工具，确认 `tools/list` 保持字母序。
2. 移除协议版本键，验证 Invalid Params（`-32602`）。然后发送格式合法但不支持的版本 `2025-11-25`，验证 `-32022`，确认 `requested` 回显该修订版，并从 `supported` 中选择。
3. 给创建操作加上服务器签发的 `draftId`，再要求更新操作把它作为参数。解释为什么这是应用状态而不是协议会话。
4. 让一个需要用户确认的工具返回 `input_required`。用新 ID、一条 `inputResponses` 记录和原样的 `requestState` 重试原调用，而不是发明一个服务器到客户端的 JSON-RPC 请求。
5. 勾画一个双时代 stdio 客户端：把结果或可识别的现代错误视为现代服务器；只对无法识别的错误或超时允许回退到 `initialize`。

## 关键术语

| 术语 | 常见说法 | 实际含义 |
|------|----------|----------|
| MCP | "LLM 的工具协议" | 用于服务器发现、工具、资源、提示与扩展的 JSON-RPC 协议 |
| Host（宿主） | "那个 AI 应用" | 拥有模型与 UI，挂载一个或多个 MCP 客户端 |
| Client（客户端） | "连接器" | 代表宿主与一个服务器对话 |
| Stateless MCP（无状态 MCP） | "没有会话" | 每个请求携带版本与能力；没有按连接键控的协议状态 |
| `server/discover` | "能力探测" | 必选的服务器方法，通告版本、能力与身份 |
| `resultType` | "结果状态" | 把结果标记为 `complete` 或 `input_required` |
| State handle（状态句柄） | "工作流 id" | 服务器签发的应用标识符，作为普通参数传递 |
| Streamable HTTP | "远程传输" | 一个 POST 端点，返回 JSON 或请求级 SSE 响应 |
| MRTR | "问了再重试" | 输入请求嵌入结果中，随后重试原操作 |

## 延伸阅读

- [MCP 2026-07-28 关键变更](https://modelcontextprotocol.io/specification/2026-07-28/changelog) — 官方变更日志
- [MCP 服务器发现](https://modelcontextprotocol.io/specification/2026-07-28/server/discover) — `server/discover` 规范
- [MCP Streamable HTTP](https://modelcontextprotocol.io/specification/2026-07-28/basic/transports/streamable-http) — 传输层规范
- [MCP Multi Round-Trip Requests](https://modelcontextprotocol.io/specification/2026-07-28/basic/patterns/mrtr) — MRTR 模式规范
- [MCP 已弃用特性](https://modelcontextprotocol.io/specification/2026-07-28/deprecated) — Roots/Sampling/Logging 弃用说明
