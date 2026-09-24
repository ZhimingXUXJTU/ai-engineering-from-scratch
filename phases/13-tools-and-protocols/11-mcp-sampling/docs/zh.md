# MCP 模型输入：Sampling 迁移与无状态 MRTR

> MCP 2026-07-28 为新设计弃用了 Sampling，并移除了服务器到客户端的请求通道。如果既有工作流仍需要客户端的模型，服务器返回一个 `input_required` 结果，客户端带着模型输出重试原始请求。推理循环因此在协议层变得显式、有界且无状态。

> **【中文解读】** 本课讲 MCP 里"模型输入"的三种方式：新服务器默认直连模型提供商；存量 Sampling 工作流迁移到 MRTR（Multi Round-Trip Request，多轮往返请求）——服务器返回 `input_required` 结果嵌入采样请求，客户端带着模型输出用新 id 重试；`requestState` 用 HMAC 做完整性保护、五重绑定。学完你应能为新服务器选直连路径，也能把旧采样循环安全地迁到无状态形态。

> **【拓展：Sampling→MRTR 的方向反转】** 旧版 Sampling 是协议里唯一的"反向通道"：服务器在处理请求时反过来调用客户端的 LLM——这正是它被移除的原因，反向通道让服务器逻辑依赖连接存活、难以无状态部署。MRTR 把"反向调用"改写成"结果 + 重试"：服务器把要做的事装进 `inputRequests` 返回，客户端拿到模型输出后用新 id 重新发起同一方法。方向反转与 Lesson 09 的传输层无状态化、Lesson 10 的 `subscriptions/listen` 是同一场架构演进。

> 🔗 **【前置】** 学本课前请先掌握：(1) Phase 13·07（MCP server）——tools/call 的分发与校验；(2) Phase 13·10（resources and prompts）——`_meta` 保留键、`server/discover`、`resultType` 判别符；(3) HMAC / 认证加密的基本概念——`requestState` 的完整性保护要用；(4) 若学过旧版（服务器直接发 `sampling/createMessage` 请求），请把那套"反向请求"心智模型换成"结果 + 重试"。

**类型：** 构建
**语言：** Python
**前置条件：** Phase 13 · 07（MCP 服务器）、Phase 13 · 10（资源与提示）
**预计用时：** 约 75 分钟

## 学习目标

- 解释 Sampling 在 MCP 2026-07-28 中被弃用的原因，并为新服务器选择直连模型集成的默认路径。
- 实现通过多轮往返请求（MRTR）承载 `sampling/createMessage` 的兼容工作流。
- 把协议修订版和客户端能力放进每个请求的 `_meta` 对象。
- 返回 `resultType: "input_required"`，并用全新的 JSON-RPC id 重试原始方法。
- 对 `requestState` 做完整性保护，并把它绑定到主体、方法、参数和过期时间。
- 用能力检查、审批、响应校验和轮数上限给模型辅助循环设界。

## 协议之前的决策

> **【中文解读】** 先做架构决策，再谈协议：什么时候直连模型提供商、什么时候保留采样兼容路径。判据是"用客户端的模型和凭证是不是真实的产品需求"——不是的话一律直连。

像 `summarize_repo` 这样的工具需要两类工作：

1. 确定性工作：列出文件、读取允许的文件、校验路径、拼装内容。
2. 模型工作：选择代表性文件并综合出摘要。

你现在有两条合法的架构。

### 新服务器：直连模型提供商

这是当前的默认。服务器自持模型选择、凭证、预算、重试和可观测性。它对 MCP 客户端返回一个普通的 `tools/call` 结果。

当服务器已经是托管服务，或当可预期的模型行为比"用宿主的模型"更重要时，选这条路径。

### 存量 Sampling 工作流：迁移到 MRTR

Sampling 在弃用窗口期内仍然存在。面向 2026-07-28 的服务器不能向客户端发送活的 `sampling/createMessage` 请求。它改为把该请求嵌入一个 `InputRequiredResult`。

仅当"使用客户端的模型和凭证"是真实的产品需求时才选这条兼容路径。记录一份移除计划，因为新实现不应采用已弃用的 Sampling。

## 无状态契约

> **【中文解读】** 无状态契约四要点：每个请求 `_meta` 自带版本与能力；版本校验的三个错误码（`-32602`/`-32022`/`-32021`）；无 `id` 是通知、不发响应；结果判别符 `complete`/`input_required`/扩展类型。

2026 年 7 月的协议没有 `initialize` 交换、没有 `notifications/initialized`、也没有 `Mcp-Session-Id`。每个请求都携带原本活在握手里的信息：

```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "method": "tools/call",
  "params": {
    "name": "summarize_repo",
    "arguments": {"audience": "developer"},
    "_meta": {
      "io.modelcontextprotocol/protocolVersion": "2026-07-28",
      "io.modelcontextprotocol/clientCapabilities": {"sampling": {}},
      "io.modelcontextprotocol/clientInfo": {
        "name": "lesson-client",
        "version": "1.0.0"
      }
    }
  }
}
```

服务器在每个请求上校验修订版。缺失或非字符串的版本是无效参数 `-32602`。不支持的字符串返回 `-32022` 并带精确数据 `{"supported":["2026-07-28"],"requested":"<client version>"}`。缺失 Sampling 能力返回 `-32021`，`data.requiredCapabilities` 设为 `{"sampling":{}}`。

不带 JSON-RPC `id` 的信封是通知。接收方可以处理它，但既不发出成功响应也不发出错误响应。Streamable HTTP 适配器对被接受的通知返回不带主体的 `202 Accepted`。

服务器还实现 `server/discover`，带精确的 `supportedVersions` 键、能力、`ttlMs` 和 `cacheScope`，让客户端能在调用工具之前学习并缓存服务器契约。因为发现公告了 `tools`，服务器还要实现强制的 `tools/list`。其确定性的 `summarize_repo` 描述符包含合法的对象 `inputSchema`、`resultType: "complete"`、服务器身份元数据和公共缓存提示。

每个成功的现代结果都带判别符：

- `resultType: "complete"` 表示操作已完成。
- `resultType: "input_required"` 表示客户端必须履行嵌入的请求并重试。
- 扩展可以定义更多结果类型。Tasks 扩展在 Lesson 13 中加入 `"task"`。

## 一轮 MRTR

> **【中文解读】** 一轮 MRTR 的完整形状：服务器返回 `input_required`（`inputRequests` 装嵌入的采样请求、`requestState` 是不透明完整性保护值）；客户端验证能力、过审批、拿模型响应；客户端用新 id 重发原始方法 + 本轮 `inputResponses` + 逐字节回显 `requestState`。重试是新的独立请求，不是会话延续；MRTR 只允许出现在 `tools/call`、`prompts/get`、`resources/read` 上。

> 💡 **【类比】** MRTR 像政务大厅的"一次性告知单"。旧 Sampling 像"工作人员直接替你打电话问上级"（服务器反向调用客户端）——上级下班（连接断开）事就办不完。MRTR 改成：工作人员给你一张告知单（`inputRequests`：要盖章的材料清单）和一张回执（`requestState`：证明你已排队到这一步），你盖好章（客户端模型补全），再取一个新号（新 JSON-RPC id）回来续办。窗口谁当班都能凭回执接着办（无状态），回执盖章防伪（HMAC），且只能办你自己的事（绑定主体和参数摘要）。

服务器在处理请求时无法调用客户端。它改为返回这个结果：

```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "result": {
    "resultType": "input_required",
    "inputRequests": {
      "pick_files": {
        "method": "sampling/createMessage",
        "params": {
          "messages": [
            {
              "role": "user",
              "content": {
                "type": "text",
                "text": "Choose three representative files and return a JSON array."
              }
            }
          ],
          "systemPrompt": "Return only the requested value.",
          "modelPreferences": {
            "costPriority": 0.8,
            "intelligencePriority": 0.2
          },
          "maxTokens": 400
        }
      }
    },
    "requestState": "opaque-integrity-protected-value"
  }
}
```

客户端验证自己支持 Sampling、应用它的审批和模型策略，并取得模型响应。然后它用不同的 JSON-RPC id 发送新请求：

```json
{
  "jsonrpc": "2.0",
  "id": 2,
  "method": "tools/call",
  "params": {
    "name": "summarize_repo",
    "arguments": {"audience": "developer"},
    "inputResponses": {
      "pick_files": {
        "role": "assistant",
        "content": {
          "type": "text",
          "text": "[\"README.md\", \"server.py\", \"docs/intro.md\"]"
        },
        "model": "host-model",
        "stopReason": "endTurn"
      }
    },
    "requestState": "opaque-integrity-protected-value",
    "_meta": {
      "io.modelcontextprotocol/protocolVersion": "2026-07-28",
      "io.modelcontextprotocol/clientCapabilities": {"sampling": {}}
    }
  }
}
```

重试不是协议会话的延续。它是一个新请求：重复原始方法和参数、只添加当前轮次的 `inputResponses`，并逐字节回显 `requestState`。

MRTR 只允许用于 `tools/call`、`prompts/get` 和 `resources/read`。服务器不得从无关方法返回 `input_required`。

## 多轮状态

> **【中文解读】** 多轮工作流的状态载体是 `requestState`。核心安全立场：把它当作攻击者可控——只签名裸阶段名不够，要五重绑定（主体、方法、参数摘要、过期、阶段与中间值）。HMAC 够用就不必认证加密；客户端唯一职责是逐字节回显。

本课需要两次模型调用：

1. `pick_files` 返回一个 JSON 数组。
2. `summary` 返回最终的散文摘要。

每次重试只携带该轮的响应。因此服务器把阶段和已校验的中间数据放进下一个 `requestState`。

把这个值当作攻击者可控的来对待。只签名一个裸的阶段名是不够的。把状态绑定到：

- 已认证主体，而不是自报的 `clientInfo`；
- 发起方法；
- 原始参数的摘要；
- 较短的过期时间；
- 当前阶段和已校验的中间值。

不需要机密性时用 HMAC。客户端不得读取状态时用认证加密。坏签名、过期值、变更的主体或变更的参数都用 `-32602` 拒绝。

客户端不得解析或修改 `requestState`。它唯一的工作是在重试时回显那个精确的字符串。

> ⚠️ **【易错点】** 场景：`requestState` 只编码阶段名不做绑定校验，或客户端图省事解析/篡改它 / 后果：攻击者伪造状态跳到任意阶段、跨请求重放旧状态、换参数续跑别人开了头的工作流 / 修复：HMAC 或认证加密 + 五重绑定，任何校验失败一律 `-32602`；客户端侧只做逐字节回显。

## 模型偏好只是提示

`costPriority`、`speedPriority`、`intelligencePriority` 是独立的偏好。它们不是概率分布，也不需要求和为一。客户端可以忽略它们，因为模型策略归客户端所有。

如果你维护遗留 Sampling 流程，把 `includeContext` 保持为 `"none"`。其他上下文模式会增加泄漏风险且本身已弃用。在请求中传递最少的显式上下文。

## 安全不变量

> **【中文解读】** 客户端是信任边界，七条不变量加一条铁律。铁律：`clientInfo` 和 `serverInfo` 是展示与诊断元数据，绝不能当认证身份。

客户端是嵌入 Sampling 请求的信任边界。

- 策略要求审批时，向用户展示服务器正在让模型做什么。
- 给 MRTR 轮数设上限。否则恶意服务器可以制造模型花费循环。
- 每个采样响应在被用作文件名、URL 或工具输入之前都要校验。
- 限制每轮的字节数和 token 数。
- 拒绝未在当前客户端能力中声明的输入请求。
- 模型输出不得参与授权决策。
- 记录发起方法和输入请求键，但不记录敏感的提示内容。

`clientInfo` 和 `serverInfo` 是展示和诊断元数据。绝不要把任何一个当作已认证身份。

```figure
t3-sampling-flip
```

## 动手实现

> **【中文解读】** 示例代码用纯标准库跑通两轮流程，重点是"状态机确定、可测"：接真宿主时只替换 `fake_host_model`。

`code/main.py` 无第三方依赖地实现了完整的两轮流程：

- `server/discover` 返回 `supportedVersions`、公告工具支持并返回缓存提示。
- `tools/list` 返回带对象输入 schema 的确定性、可缓存 `summarize_repo` 描述符。
- `tools/call` 校验逐请求元数据。
- 第一个结果嵌入用于选文件的 `sampling/createMessage`。
- 第一次重试验证模型结果并嵌入第二个请求。
- HMAC 保护的 `requestState` 在独立请求之间携带阶段。
- 最终结果使用 `resultType: "complete"`。

假宿主模型让示例保持确定性。接入真实宿主时只替换 `fake_host_model`。服务器侧状态机应保持确定和可测试。

## 用框架实现

从仓库根目录：

```bash
cd phases/13-tools-and-protocols/11-mcp-sampling/code
python3 main.py
python3 -m unittest discover tests -v
```

预期检查点：

- 发现返回带 `ttlMs` 和 `cacheScope` 的完整结果。
- 工具发现返回相同排序的描述符，带 `resultType`、服务器身份和缓存提示。
- 能力缺失和不支持的版本使用精确的 `-32021` 和 `-32022` 错误数据。
- 无 id 的通知不产生 JSON-RPC 响应。
- 请求 id 是 `[1, 2, 3]`，证明每个 MRTR 轮次相互独立。
- 前两个结果是 `input_required`。
- 最终结果是 `complete`，包含选出的文件和摘要。
- 重试时改变原始参数会未通过请求状态检查。

## 产出物

`outputs/skill-sampling-loop-designer.md` 现在是一份迁移规划器。它先决定是否应该移除 Sampling、改用直连模型集成。如果需要兼容，它产出 MRTR 轮次、状态绑定、能力门、预算、校验和移除计划。

## 练习题

1. 把文件选择响应改成非法 JSON。确认服务器返回 `-32602` 而不是信任模型输出。
2. 在首次调用和重试之间改变 `audience`。解释为什么密封状态能阻断跨请求复用。
3. 添加请宿主评审摘要的第三轮。把较早的摘要放进签名状态里携带，并把整个流程限制在三轮。
4. 用服务器自有的模型适配器替换假宿主回调以移除 Sampling。列出哪些审批、计费和可观测性职责转移到服务器。
5. 用一个超过截止时间一秒的状态值添加过期测试。

## 术语速查表

| 术语 | 2026-07-28 中的含义 |
|------|----------------------|
| Sampling（采样） | 已弃用特性：请求客户端的模型做补全 |
| MRTR | 请求中需要客户端输入时的无状态重试模式 |
| `InputRequiredResult` | 带 `resultType: "input_required"` 的结果 |
| `inputRequests` | 服务器命名的映射，装嵌入的 elicitation、sampling 或 roots 请求 |
| `inputResponses` | 本轮客户端结果，键与 `inputRequests` 对应 |
| `requestState` | 不透明的服务器状态，客户端逐字节回显、服务器校验 |
| `resultType` | 现代化 MCP 结果的必需判别符 |
| 直连模型集成 | 需要模型推理的新服务器的推荐替代 |
| 能力门 | 阻止发送客户端未声明的嵌入请求的规则 |
| 循环预算 | 该操作允许的最大轮数、token 数、字节数、时间和花费 |

## 遗留兼容

> **【中文解读】** 旧客户端可以活在版本隔离的适配器里，但那是兼容边界，不是新架构的许可。

钉在 2025-11-25 的客户端仍可在活连接上使用较旧的服务器发起式 `sampling/createMessage` 流程。那种行为只保留在按版本隔离的适配器里。不要让有会话的路径成为 2026-07-28 服务器的架构。

官方 SDK 可以为较旧的对端翻译现代 `input_required` 处理器。那个垫片是兼容边界，不是添加新的依赖会话逻辑的许可。

## 延伸阅读

- [MCP 2026-07-28 Multi Round-Trip Requests](https://modelcontextprotocol.io/specification/2026-07-28/basic/patterns/mrtr) — MRTR 模式的权威规范
- [MCP 2026-07-28 changelog](https://modelcontextprotocol.io/specification/2026-07-28/changelog) — 2026-07-28 修订的完整变更清单
- [MCP Sampling deprecation](https://modelcontextprotocol.io/seps/2577-deprecate-roots-sampling-and-logging) — Sampling 弃用的 SEP 提案原文
- [MCP 2026-07-28 server discovery](https://modelcontextprotocol.io/specification/2026-07-28/server/discover) — `server/discover` 发现契约规范
