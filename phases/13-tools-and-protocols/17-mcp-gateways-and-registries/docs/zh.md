# 无状态 MCP 网关与注册中心准入

> 网关应让每条路由显式化。2026-07-28 协议在没有传输会话的前提下，为网关提供了方法、名称、版本、能力、身份、缓存与追踪边界。

> **【中文解读】** 旧网关"多路复用一个客户端会话到多个后端会话并重写 `Mcp-Session-Id`"的设计已成遗留兼容路径；现代网关对每个请求重新认证、重新授权、重新构造后端请求。本课走通这条现代路径，并定义注册中心记录与网关准入策略的分工。

> **【拓展】** 网关是企业 MCP 部署的控制平面：把 Phase 13 · 15 的描述符锁定与 Phase 13 · 16 的授权模型集中执行。注册中心（Registry）提供发现证据（server.json），但准入决定权在网关——这是"发现不等于决定"的核心分离。Lesson 30 在此之上构建完整的供应链控制平面（命名空间证明、来源追溯、不可变锁定、漂移检测、回滚）。

> 🔗 **【前置】** 学本节前请先掌握：(1) Phase 13 · 15（安全）与 13 · 16（授权）——网关集中执行这两课的全部校验；(2) Phase 13 · 09 的 Streamable HTTP——单一 POST 端点、请求级 SSE、`subscriptions/listen`；(3) MRTR 与 Tasks 扩展的基本形态。

**类型：** 学习
**语言：** Python
**前置条件：** Phase 13 · 15（安全）、Phase 13 · 16（授权）
**预计用时：** 约 75 分钟

## 学习目标

- 把多个 MCP 服务器聚合到一个 2026-07-28 端点之后，不依赖会话亲和。
- 在策略与转发之前校验每请求元数据和路由头。
- 用稳定命名空间、确定性顺序、描述符锁定、RBAC 和私有缓存合并工具。
- 把注册中心记录当作仍需准入策略的发现证据。
- 正确路由请求级 SSE、`subscriptions/listen`、MRTR 重试和 Tasks 扩展调用。
- 把遗留握手与会话支持同现代路径隔离。

> **【中文解读】** 六个关键词：聚合（无会话亲和）、校验（先于策略）、合并（确定性）、准入（发现不等于决定）、路由（SSE/订阅/MRTR/Tasks 四种流）、隔离（遗留路径版本门控）。

## 问题引入

一个客户端直连一个服务器很简单。更大的部署需要为更难的问题给出一致答案：

- 哪些服务器被允许？
- 哪个主体能看到并调用每个工具？
- 两个后端暴露同名工具时会发生什么？
- 描述符变更如何复审？
- 限流和审计事件作用在哪里？
- 任意实例都能处理下一个请求吗？

网关位于客户端与后端 MCP 服务器之间。它呈现一个 MCP 端点，应用横切策略，转发批准的请求。

较早的网关设计常把一个客户端会话多路复用成多个后端会话并重写 `Mcp-Session-Id`。那是遗留兼容设计。2026-07-28 核心没有协议会话。

> **【中文解读】** 六个问题就是网关的存在理由。注意最后一问——"任意实例能否处理下一个请求"——它把可用性设计也拉进了无状态约束：网关的水平扩展不能依赖会话粘滞。

> 💡 **【类比】** 旧网关像"总机转接的电话系统"——客户先拨总机（建立会话），总机记住线路（会话亲和），断线就得重拨。现代网关像"快递分拣中心"——每个包裹（请求）自带完整面单（元数据 + 路由头 + 凭证），任何分拣员（任意实例）拿起就能处理。注册中心像"供应商黄页"——黄页只证明"有这家店"，不证明"该让这批货进仓库"；准入策略才是仓库的验货单。

## 核心概念

> **【中文解读】** 本节按网关的处理流水线展开：现代网关七步路径 → 运行时策略是首要决定 → 单一 POST 端点 → 每层实现发现 → 每请求客户端能力 → 确定性命名空间 → 锁定已批准描述符 → 注册中心只助发现不作决定 → 凭证中介 → 无会话限流 → 审计决策链 → 请求级 SSE → 长效变更通知 → 网关中的 MRTR → Tasks 扩展路由 → 兼容边界。

### 现代网关路径

对每个请求：

1. 从传输层授权信息认证主体。
2. 校验 `MCP-Protocol-Version`、`Mcp-Method`、`Mcp-Name` 和 `params._meta`。
3. 授权主体、资源、方法、工具和参数。
4. 应用描述符、注册、限流和数据策略。
5. 为选定后端构造全新的自包含请求。
6. 校验后端结果并返回网关结果。
7. 记录审计事件，但不记录秘密。

没有一步需要隐藏的协议会话。应用状态仍可存在于数据库、显式句柄、Tasks 或受完整性保护的 MRTR 状态中。

> **【中文解读】** 七步是网关的"标准作业程序"：先验明正身，再验请求，再授权，再套策略，然后才构造后端请求。第 5 步最关键——给后端的是"全新自包含请求"，不是外层请求的改写，这保证后端永远拿不到外层的会话痕迹或多余能力。

### 运行时策略是网关的首要决定

准入决定哪个后端版本可以进入网关，但不授权一次实际调用。对每个请求，网关都要从已认证主体、issuer 与资源、租户、匹配的方法与名称、规范化参数、准入描述符锁定、当前后端健康、能力交集、数据分类、限流状态和任何动作绑定批准中重新计算策略。

这个顺序很重要：注册记录可以仍处于 active 而用户的角色已被撤销；描述符可以仍被锁定而目标参数跨越了租户边界；后端可以仍被批准而事故策略隔离了状态变更调用。因此运行时策略是首要的允许/拒绝决定，注册与描述符证据只是输入。

不要把"允许"决定缓存在连接或已移除的会话标识之下。策略不可用时，按操作类别执行已声明的失败策略。安全默认：状态变更与敏感读一律失效关闭（fail-closed）；显式批准的公共读路径只有在风险模型允许时才可用短期的最后已知策略。记录做决定的策略版本与失败路径，然后在返回前校验后端结果。

> **【中文解读】** "准入"与"运行时策略"是两个不同时刻的决定：准入发生在后端接入时（静态），运行时策略发生在每个请求上（动态）。把静态批准当动态授权用，是网关最常见的越权来源——角色撤销、租户越界、事故隔离都会被"曾经批准过"掩盖。

> ⚠️ **【易错点】** 场景：网关把"允许"决定缓存在连接 ID 或旧会话 ID 下 / 后果：用户角色被撤销、租户被隔离后，旧连接上的请求仍被放行 / 修复：(1) 每个请求重算策略，锚点是已认证主体而非连接；(2) 策略服务不可用时按操作类别 fail-closed——写操作和敏感读直接拒绝；(3) 审计里记录策略版本与失败路径，让"为什么放行/拒绝"可复盘。

### 单一 POST 端点

现代 Streamable HTTP 通过 POST 发送每条 JSON-RPC 消息：

```text
POST /mcp
Authorization: Bearer <gateway-token>
MCP-Protocol-Version: 2026-07-28
Mcp-Method: tools/call
Mcp-Name: notes.search
Accept: application/json, text/event-stream
```

网关可以为该 POST 返回 JSON 或请求级 SSE。现代请求的 GET 和 DELETE 返回 405。`Mcp-Session-Id` 与 `Last-Event-ID` 不产生权威、亲和或重放行为。

头与正文的值必须一致。在查找后端之前用 `-32020` 拒绝不匹配。这让负载均衡器、网关和限流器不用解析完整正文就能路由，同时保住端到端完整性。

按唯一精确顺序校验：JSON-RPC 与元数据类型、头与正文相等、然后对匹配版本的支持。不匹配返回 HTTP 400 `-32020`；头文一致但版本不支持，返回 HTTP 400 `-32022` 且 `data` 精确为 `{"supported":["2026-07-28"],"requested":"<actual>"}`；未知方法返回 HTTP 404 `-32601`。

`ProtocolError` 携带可选 `data`，网关把它序列化进 JSON-RPC 错误对象。通知没有 `id`，永远不收 JSON-RPC 成功或错误响应。被接受的 HTTP 通知返回 202 空体。

> **【中文解读】** 校验顺序在网关场景多了一层意义：负载均衡器可以只看 `Mcp-Method`/`Mcp-Name` 头做分发，不必解析正文——前提是网关在最终处强制头文相等。三个错误码（`-32020`/`-32022`/`-32601`）与 Phase 13 · 15、13 · 16 完全一致，是贯穿全套课程的一条契约线。

### 在每一层实现发现

网关为客户端实现 `server/discover`；同时也发现每个后端，以便知道协议版本、能力和扩展。

网关结果示例：

```json
{
  "resultType": "complete",
  "supportedVersions": ["2026-07-28"],
  "capabilities": {
    "tools": {"listChanged": true}
  },
  "ttlMs": 30000,
  "cacheScope": "private",
  "_meta": {
    "io.modelcontextprotocol/serverInfo": {
      "name": "enterprise-gateway",
      "version": "2.0.0"
    }
  }
}
```

只通告网关能端到端兑现的能力交集。后端的功能不自动等于可对外暴露；没有后端路径支撑的网关功能通告了也没用。

`serverInfo` 是自报的展示与诊断数据，不要当注册中心或发布者证明用。

> **【中文解读】** 发现是双向的：对外通告能力交集（不是并集），对内摸清每个后端的版本与能力。"交集原则"防止网关承诺自己兑现不了的行为——比如后端都支持 `listChanged` 才能通告它。

### 每请求客户端能力

每个转发的请求都需要当前的 `_meta` 信封：

```json
{
  "io.modelcontextprotocol/protocolVersion": "2026-07-28",
  "io.modelcontextprotocol/clientCapabilities": {},
  "io.modelcontextprotocol/clientInfo": {
    "name": "enterprise-gateway",
    "version": "1.0.0"
  }
}
```

不要把外层客户端的能力原样照抄给后端。网关才是后端的客户端。只通告网关能正确中介的特性。

> **【中文解读】** 网关在外层是服务器、在内层是客户端——两个角色能力不同。外层客户端声明了 elicitation，不代表网关愿意替它向后端转发表单；网关通告给后端的，只能是它自己实现过中介逻辑的那部分。

### 确定性命名空间

用稳定的公开名称合并后端工具：

```text
notes.search
notes.create
issues.list
issues.open
```

保留"公开名 → 后端 + 原始工具名"的映射。绝不在重名冲突里选先来后到。公开名是审批与审计契约的一部分，改它就是一次迁移。

`tools/list` 必须确定性。当可见性因主体而异时返回 `cacheScope: private`。有界的 `ttlMs` 降低后端发现负载，又不让按用户定制的列表跨授权上下文泄漏。

每个暴露的工具描述符都含稳定名称、描述和对象根 `inputSchema`。命名空间化不能删掉必填的描述符字段。完整列表结果还包括 `resultType`、服务器身份元数据和缓存提示。

> **【中文解读】** 确定性有三层含义：同一输入永远得到同一列表；顺序固定（不随发现顺序漂移）；重名解析规则固定（加前缀，不抢占）。`cacheScope: private` 是可见性按主体过滤时的必选项——公共缓存会把 A 用户专属的工具漏给 B 用户。

### 锁定已批准描述符

准入时规范化完整描述符，把摘要存到限定公开名之下。列表与调用时，把线上描述符与已批准摘要比对。

若发生变更：

- 从 `tools/list` 移除它。
- 拒绝直接调用。
- 发出审计事件。
- 更新锁定前要求策略或人工重新批准。

网关是有用的集中执行点，但它不能把"第一次见到的描述符"变成安全的。初始评审仍然必要。

> **【中文解读】** 这是 Phase 13 · 15 地毯拉扯防御的集中化版本：网关在发现与分发两个时刻核对摘要，变更即下架加告警。锁定的对象仍是完整描述符（不只是描述文本），且首版安全性靠准入评审，不靠锁定。

### 注册中心只助发现，不作决定

注册中心的 `server.json` 提供发布元数据。一个带包的记录长这样：

```json
{
  "$schema": "https://static.modelcontextprotocol.io/schemas/2025-12-11/server.schema.json",
  "name": "com.example/notes",
  "description": "Example notes MCP server.",
  "version": "1.0.0",
  "packages": [
    {
      "registryType": "npm",
      "identifier": "@example/notes-mcp",
      "version": "1.0.0",
      "transport": {"type": "stdio"}
    }
  ]
}
```

发布元数据不承载网关的安全决定。把已验证的发布者与来源证据放进独立的准入状态：

```json
{
  "registryName": "com.example/notes",
  "registryVersion": "1.0.0",
  "publisher": {"namespace": "com.example", "status": "verified"},
  "provenance": {
    "source": "registry.modelcontextprotocol.io",
    "recordId": "com.example/notes@1.0.0"
  },
  "admission": {"status": "approved", "reviewedBy": "gateway-policy"}
}
```

网关检查 `server.json` 的形状并把它与那份外部状态做连接。网关仍然需要自己的准入策略。

对每个准入后端，记录：

- 精确的注册中心与记录标识。
- 已验证的发布者命名空间或域名证据。
- 允许的传输与端点。
- 锁定的版本或已批准的升级策略。
- 工件或描述符摘要。
- 授权 issuer 与资源。
- 评审人、批准时间与有效期。

不要因为展示名像某个熟悉产品就接受一台服务器；不要把"上了注册中心"当作一次运维安全评审。私有服务器即使从未出现在公共注册中心，也可以走同一套证据模式准入。

本课实现的是网关接缝：在后端可路由之前，把发布证据连接到本地准入。[Lesson 30: MCP Registry Supply Chain, Admission, Drift, and Rollback](../../30-mcp-registry-supply-chain-and-drift/docs/en.md) 构建完整控制平面——精确命名空间证明、工件来源、不可变锁定、线上描述符漂移、注册中心状态对账、防篡改准入账本和有证据支撑的回滚。要把那套供应链状态与上面的每请求运行时决定分开。

> **【中文解读】** "发现不等于决定"：`server.json` 说的是"这个包存在、叫这个名字、这样安装"；准入状态说的是"我们验证过发布者、批准了这个版本、锁定在这个摘要"。两张表分开存、显式 join，谁也不能冒充谁。

> 🤔 **【困惑】** Q: 注册中心都验证了发布者，为什么网关还要自己的准入策略？A: 注册中心验证的是"发布者是谁"，不是"你的企业该不该用"。注册记录可以保持有效而用户角色已被撤销；描述符保持锁定而目标参数跨租户；后端保持批准而事故策略隔离状态变更调用。发现证据解决"这货是谁家的"，准入与运行时策略解决"这货现在能不能进、能上哪条产线"。

### 凭证中介

网关认证自己的调用方，并单独向后端做认证。后端凭证永远不到客户端手上。

让这些绑定保持显式：

```text
outer principal -> gateway role and policy
backend issuer + resource -> backend registration and token
```

绝不把外层网关 token 传给后端；绝不把后端 token 用到另一个 issuer 或资源上。如果工具代表最终用户行动，要用设计过的交换或声明模型保留这层委托，而不是拿共享服务凭证冒充用户。

> **【中文解读】** 凭证中介是网关的核心价值之一：开发者只见网关 token，后端 token 锁在网关内。"两次认证、两套凭证、零透传"。代表最终用户的场景要显式建模委托（token 交换或声明传递），不能靠共享服务账号冒充。

### 无会话限流

限流按已认证主体、issuer、资源、公开工具、成本类别和时间窗口取键。会话 id 已不存在；即便存在也容易轮换，不可作键。

先做便宜的校验，再消耗昂贵的工作。并决定被拒绝的调用是否计入滥用限额、业务配额或两者。

> **【中文解读】** 限流键的选择决定攻击成本：按 IP 会被代理池绕过，按会话已无会话可按，按主体+工具+时间窗是最小可行组合。"先便宜校验后昂贵工作"还有个隐性收益——畸形请求烧不掉后端算力。

### 审计决策链

记录足够重建一次调用的信息：

- 请求与追踪标识符。
- 已认证主体与 issuer。
- 公开工具与后端路由。
- 描述符锁定版本。
- 策略决定与理由。
- 延迟与结果类别。
- 适用时的 MRTR 轮次或任务标识符。

对 bearer token、授权码、refresh token、原始秘密和不必要的敏感参数做脱敏。

> **【中文解读】** 审计的目标是"事后能回答为什么"：哪个策略版本、哪个锁定版本、为什么放行或拒绝。脱敏清单里的每一样都是泄露高发区——日志聚合系统往往是比数据库更宽松的攻击面。

### 请求级 SSE

当工作在这一个请求内流式产出时，普通 POST 可以返回请求级 SSE。关闭响应流即取消这个进行中的现代 HTTP 请求。

不要另建 GET 流，也不要承诺 Last-Event-ID 重放。那些是旧的传输假设。

> **【中文解读】** 请求级 SSE 与旧 GET 流的本质区别：流的生命周期属于这一次 POST 请求，连接断开即任务取消，没有独立于请求的"推送通道"。这把连接管理简化成 HTTP 语义本身，网关也无需维护跨请求的流状态。

### 长效变更通知

对列表与资源变更通知，当前客户端通过 POST 发送 `subscriptions/listen` 并收到 SSE 响应。通知过滤器使用精确的扁平字段 `toolsListChanged`、`promptsListChanged`、`resourcesListChanged` 和 `resourceSubscriptions`：

```json
{
  "jsonrpc": "2.0",
  "id": "listen-tools",
  "method": "subscriptions/listen",
  "params": {
    "notifications": {
      "toolsListChanged": true
    },
    "_meta": {
      "io.modelcontextprotocol/protocolVersion": "2026-07-28",
      "io.modelcontextprotocol/clientCapabilities": {}
    }
  }
}
```

第一个事件确认受支持的子集。其订阅标识符就是打开这条流的那个请求的 JSON-RPC id：

```json
{
  "jsonrpc": "2.0",
  "method": "notifications/subscriptions/acknowledged",
  "params": {
    "_meta": {
      "io.modelcontextprotocol/subscriptionId": "listen-tools"
    },
    "notifications": {
      "toolsListChanged": true
    }
  }
}
```

之后网关只转发已确认的变更类型。这条流上的每个通知都在 `params._meta` 里带同一个 `io.modelcontextprotocol/subscriptionId`。没有自动重放，也没有自动重新监听。重连时客户端重新打开订阅并刷新它依赖的列表。服务器主动优雅关闭时，返回带同一订阅 id 的最终完整结果。

现代路径取代了 `resources/subscribe`、`resources/unsubscribe` 和未经请求的独立 GET 流。把这些只保留在版本门控的旧路径里。

> **【中文解读】** 订阅模型的三条纪律：客户端主动开流（POST，不是服务器推送 GET）、确认制（先 ack 子集再转发）、无重放承诺（断了就重开订阅并刷新列表）。订阅 id 复用打开请求的 JSON-RPC id，省掉一层状态。

### 网关中的 MRTR

后端返回 `resultType: input_required` 时，只有外层客户端支持所需输入请求，网关才能转发该结果。除非网关刻意终结并重新发起交互，`requestState` 要逐字节保留。

客户端用新的 JSON-RPC id 和 `inputResponses` 重试原公开工具。网关对重试重新授权、检查同一公开路由，然后转发全新的后端请求。绝不能假设早先一轮授予了无限批准。

> **【中文解读】** 网关在 MRTR 里是"透传但不信任"：`requestState` 逐字节转发（签名仍由后端持有），但重试必须走完整的重新授权链。能力检查也在此发生——后端要表单 elicitation 而外层客户端只声明了 URL，网关就得拦下。

### Tasks 扩展路由

Tasks 是由 `io.modelcontextprotocol/tasks` 标识的官方扩展，不是核心会话的替代品。

客户端在每请求客户端能力里声明该扩展；网关只有在能端到端保住任务生命周期时才在发现中通告它。对受支持的 `tools/call`，是否返回普通结果或 `resultType: task` 由后端单独决定。任务结果直接在结果里带 `taskId`、`status`、时间戳、`ttlMs` 和可选的 `pollIntervalMs`。发送该结果之前，任务必须已经可持久读取。

网关为不透明的任务标识符记录已认证主体与后端路由。后续的 `tasks/get`、`tasks/update`、`tasks/cancel` 调用用 `params.taskId` 作 `Mcp-Name`，给中间件一个路由键。`tasks/get` 返回 `resultType: complete` 与当前任务状态，并在终态内联最终结果或协议错误。`tasks/update` 为未决的任务输入发送带键的 `inputResponses`，返回空的完成确认。`tasks/cancel` 是协作式意图加空的完成确认，不保证工作真的停止。

不要实现新的 `tasks/list` 或 `tasks/result` 方法——它们属于较旧的实验模型。需要输入的任务通过 `tasks/get` 暴露完整的内嵌请求；客户端通过 `tasks/update` 回答，而不是重试原工具调用。客户端仍按建议间隔轮询；任务创建仍由服务器主导。

持久的任务路由状态是按任务句柄取键的应用数据，不是协议会话。

> **【中文解读】** Tasks 路由的巧思在 `Mcp-Name`：任务操作把 `params.taskId` 放进 `Mcp-Name`，让网关不用解析正文就能按头路由——与 `tools/call` 的路由键设计完全同构。任务状态是应用数据（数据库里的一行），不是协议状态，所以天然无状态。

### 兼容边界

如果网关必须服务较旧的客户端或后端：

- 显式检测协议年代。
- 把初始化、传输会话、GET 流、资源订阅和旧任务词汇全部留在遗留适配器里。
- 绝不让遗留会话 id 泄漏进现代路由或授权。
- 优先用有界的发现探测加显式回退策略，而非静默降级。

> **【中文解读】** 兼容的关键词是"显式"：显式检测年代、显式版本门控、显式回退决策。最危险的模式是静默降级——客户端发了旧消息，网关没吭声就按旧规则处理，于是两条路径的状态悄悄耦合。隔离的目标是：现代 `Gateway` 类里找不到任何遗留状态。

## 动手构建

`code/main.py` 实现进程内协议网关和两个后端服务器。每个后端收到全新的当前协议请求。网关提供发现、按用户过滤的确定性 `tools/list`、命名空间路由、注册中心 `server.json` 加外部准入状态、描述符锁定、RBAC、按主体取键的限流、审计决定，以及建模的 `subscriptions/listen` SSE 确认。

模型接收已解析的请求正文、路由头和已认证的 Bearer 身份。它不是完整 HTTP 适配器，不解析 `Content-Type` 或完整的 `Accept` 契约。把它接到 Lesson 09 的 Streamable HTTP 适配器上——那边要求 `Content-Type: application/json`，且 `Accept` 同时包含 `application/json` 与 `text/event-stream`。

运行：

```bash
cd phases/13-tools-and-protocols/17-mcp-gateways-and-registries
python3 code/main.py
python3 -m unittest discover code/tests -v
```

演示会打印外层请求 id 和全新的后端请求 id，让这一跳的无状态性可见。

> **【中文解读】** 读代码先看 `Gateway.handle` 的主干七步，再对照三个字典：`RBAC`（主体→工具集）、描述符锁定表（公开名→摘要）、准入目录（server.json+admission 的 join）。演示输出里"外层 id ≠ 后端 id"就是无状态一跳的直接证据。

## 实际使用

把进程内后端对象换成真实的当前协议客户端。保留同样的接缝：

- 连接之前先有准入记录。
- 能力暴露之前先完成后端发现。
- 授权之前先确定限定公开名。
- 列表或调用之前先核对描述符锁定。
- 转发之前先构造新鲜的每请求元数据。
- 返回之前先校验结果。

> **【中文解读】** 六个接缝就是六个"不可绕过的检查点"。换真实后端时，只要接缝还在，网关的安全性质就不变；接缝一旦被"临时跳过"，前面的准入、锁定、命名空间全部失效。

## 产出物

本课产出 `outputs/skill-gateway-bootstrap.md`。它生成现代网关设计，覆盖入口、发现、准入、命名空间、授权、缓存、流式、订阅、MRTR、Tasks、可观测性和遗留隔离。

> **【中文解读】** 这份 skill 的用法：拿着企业 MCP 计划（用户规模、后端清单、合规要求）逐节填空，产出的设计文档直接对应本课十六个小节的检查清单——从入口到遗留隔离一条不落。

## 练习题

1. 给外层与转发的请求元数据加追踪上下文，并把关联关系记进审计事件。

2. 添加支持 Tasks 的后端，并按 `Mcp-Name` 里的任务 id 路由 `tasks/get`。

3. 变更一个后端描述符，证明发现和直接调用都被阻止。

4. 添加按主体定制的服务器能力，并解释为什么发现必须保持私有缓存。

5. 编写遗留适配器接口，且不给现代 `Gateway` 类添加任何遗留状态。

## 术语速查表

| 术语 | 含义 | 英文 |
|------|------|------|
| MCP 网关 | 客户端与后端 MCP 服务器之间的策略与路由服务器 | MCP gateway |
| 准入记录 | 允许一个后端进入网关的证据与策略决定 | Admission record |
| 限定工具名 | 稳定的公开路由，如 `notes.search` | Qualified tool name |
| 描述符锁定 | 发现与分发期间核对的已批准摘要 | Descriptor pin |
| 私有缓存范围 | 缓存结果限定于单一授权上下文 | Private cache scope |
| 请求级 SSE | 附着于单个 POST 请求的流式响应 | Request-scoped SSE |
| `subscriptions/listen` | 客户端打开的 SSE 流，用于选定的长效变更通知 | subscriptions/listen |
| 任务路由 | 从不透明任务 id 到其后端的应用层映射 | Task route |
| 遗留适配器 | 为旧握手与会话行为设置的显式版本门控边界 | Legacy adapter |

## 延伸阅读

- [Streamable HTTP 传输](https://modelcontextprotocol.io/specification/2026-07-28/basic/transports/streamable-http) — 单 POST 端点与请求级 SSE 契约
- [服务器发现](https://modelcontextprotocol.io/specification/2026-07-28/server/discover) — `server/discover` 规范，网关与后端的双层发现依据
- [官方注册中心 server.json 要求](https://github.com/modelcontextprotocol/registry/blob/main/docs/reference/server-json/official-registry-requirements.md) — 发布元数据的字段契约
- [MCP Tasks 扩展](https://tasks.extensions.modelcontextprotocol.io/specification/draft/tasks) — 任务生命周期与 `Mcp-Name` 路由键
