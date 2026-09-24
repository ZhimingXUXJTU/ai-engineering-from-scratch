# Stateless MCP Gateways and Registry Admission | 无状态 MCP 网关与注册中心准入

> A gateway should make every route explicit. The 2026-07-28 protocol gives it method, name, version, capability, identity, cache, and trace boundaries without a transport session.

> **【中文解读】** 网关应让每条路由显式化。2026-07-28 协议在没有传输会话的前提下，为网关提供了方法、名称、版本、能力、身份、缓存与追踪边界。旧网关"多路复用一个客户端会话到多个后端会话并重写 `Mcp-Session-Id`"的设计已成遗留兼容路径；现代网关对每个请求重新认证、重新授权、重新构造后端请求。

> **【拓展】** 网关是企业 MCP 部署的控制平面：把 Phase 13 · 15 的描述符锁定与 Phase 13 · 16 的授权模型集中执行。注册中心（Registry）提供发现证据（server.json），但准入决定权在网关——这是"发现不等于决定"的核心分离。Lesson 30 在此之上构建完整的供应链控制平面（命名空间证明、来源追溯、不可变锁定、漂移检测、回滚）。

> 🔗 **【前置】** 学本节前请先掌握：(1) Phase 13 · 15（安全）与 13 · 16（授权）——网关集中执行这两课的全部校验；(2) Phase 13 · 09 的 Streamable HTTP——单一 POST 端点、请求级 SSE、`subscriptions/listen`；(3) MRTR 与 Tasks 扩展的基本形态。

**Type:** Learn | **类型:** 学习
**Languages:** Python | **语言:** Python
**Prerequisites:** Phase 13 · 15 (security), Phase 13 · 16 (authorization) | **前置知识:** Phase 13 · 15（安全）、Phase 13 · 16（授权）
**Time:** ~75 minutes | **时间:** 约 75 分钟

## Learning Objectives | 学习目标

- Aggregate several MCP servers behind one 2026-07-28 endpoint without session affinity.
  中文翻译：把多个 MCP 服务器聚合到一个 2026-07-28 端点之后，不依赖会话亲和。
- Validate per-request metadata and routing headers before policy or forwarding.
  中文翻译：在策略与转发之前校验每请求元数据和路由头。
- Merge tools with stable namespaces, deterministic order, descriptor pins, RBAC, and private caching.
  中文翻译：用稳定命名空间、确定性顺序、描述符锁定、RBAC 和私有缓存合并工具。
- Treat registry records as discovery evidence that still requires admission policy.
  中文翻译：把注册中心记录当作仍需准入策略的发现证据。
- Route request-scoped SSE, `subscriptions/listen`, MRTR retries, and Tasks extension calls correctly.
  中文翻译：正确路由请求级 SSE、`subscriptions/listen`、MRTR 重试和 Tasks 扩展调用。
- Isolate legacy handshake and session support from the modern path.
  中文翻译：把遗留握手与会话支持同现代路径隔离。

> **【中文解读】** 学习目标：聚合（无会话亲和）、校验（先于策略）、合并（确定性）、准入（发现≠决定）、路由（SSE/订阅/MRTR/Tasks 四种流）、隔离（遗留路径版本门控）。

## The Problem | 问题引入

> **【中文解读】** 规模化部署要回答六个问题：哪些服务器允许接入？哪个主体能看到并调用每个工具？两个后端重名怎么办？描述符变更如何复审？限流和审计作用在哪里？任意实例能否处理下一个请求？网关给出一致答案：单一 MCP 端点 + 横切策略 + 转发批准的请求。

Connecting one client directly to one server is simple. A larger deployment needs a consistent answer to harder questions:

> 一个客户端直连一个服务器很简单。更大的部署需要为更难的问题给出一致答案：

- Which servers are allowed?
  中文翻译：哪些服务器被允许？
- Which principal can see and call each tool?
  中文翻译：哪个主体能看到并调用每个工具？
- What happens when two backends expose the same name?
  中文翻译：两个后端暴露同名工具时会发生什么？
- How are descriptor changes reviewed?
  中文翻译：描述符变更如何复审？
- Where are rate limits and audit events applied?
  中文翻译：限流和审计事件作用在哪里？
- Can any instance handle the next request?
  中文翻译：任意实例都能处理下一个请求吗？

A gateway sits between clients and backend MCP servers. It presents one MCP endpoint, applies cross-cutting policy, and forwards approved requests.

> 网关位于客户端与后端 MCP 服务器之间。它呈现一个 MCP 端点，应用横切策略，转发批准的请求。

Older gateway designs often multiplexed one client session into several backend sessions and rewrote `Mcp-Session-Id`. That is a legacy compatibility design. The 2026-07-28 core has no protocol sessions.

> 较早的网关设计常把一个客户端会话多路复用成多个后端会话并重写 `Mcp-Session-Id`。那是遗留兼容设计。2026-07-28 核心没有协议会话。

> 💡 **【类比】** 旧网关像"总机转接的电话系统"——客户先拨总机（建立会话），总机记住线路（会话亲和），断线就得重拨。现代网关像"快递分拣中心"——每个包裹（请求）自带完整面单（元数据 + 路由头 + 凭证），任何分拣员（任意实例）拿起就能处理，不需要"上次是谁接的电话"。注册中心像"供应商黄页"——黄页只证明"有这家店"，不证明"该让这批货进仓库"；准入策略才是仓库的验货单。

## The Concept | 核心概念

> **【中文解读】** 本节按网关的处理流水线展开：现代网关七步路径 → 运行时策略是首要决定 → 单一 POST 端点 → 每层实现发现 → 每请求客户端能力 → 确定性命名空间 → 锁定已批准描述符 → 注册中心只助发现不作决定 → 凭证中介 → 无会话限流 → 审计决策链 → 请求级 SSE → 长效变更通知 → 网关中的 MRTR → Tasks 扩展路由 → 兼容边界。

### The modern gateway path

> **【中文解读】** 现代网关对每个请求走七步：认证主体 → 校验版本/路由头/元数据 → 授权主体、资源、方法、工具、参数 → 应用描述符、注册、限流、数据策略 → 为选定后端构造全新自包含请求 → 校验后端结果并返回网关结果 → 记录不含秘密的审计事件。没有一步需要隐藏的协议会话；应用状态放数据库、显式句柄、Tasks 或受完整性保护的 MRTR 状态里。

For each request:

1. Authenticate the principal from transport authorization.
  中文翻译：从传输层授权信息认证主体。
2. Validate `MCP-Protocol-Version`, `Mcp-Method`, `Mcp-Name`, and `params._meta`.
  中文翻译：校验 `MCP-Protocol-Version`、`Mcp-Method`、`Mcp-Name` 和 `params._meta`。
3. Authorize the principal, resource, method, tool, and arguments.
  中文翻译：授权主体、资源、方法、工具和参数。
4. Apply descriptor, registry, rate, and data policy.
  中文翻译：应用描述符、注册、限流和数据策略。
5. Create a fresh self-contained request for the selected backend.
  中文翻译：为选定后端构造全新的自包含请求。
6. Validate the backend result and return a gateway result.
  中文翻译：校验后端结果并返回网关结果。
7. Record an audit event without logging secrets.
  中文翻译：记录审计事件，但不记录秘密。

No step needs a hidden protocol session. Application state can still exist in databases, explicit handles, Tasks, or integrity-protected MRTR state.

> 没有一步需要隐藏的协议会话。应用状态仍可存在于数据库、显式句柄、Tasks 或受完整性保护的 MRTR 状态中。

### Runtime policy is the primary gateway decision

> **【中文解读】** 准入决定"哪个后端版本可以进网关"，但不授权一次活调用。每个请求都要从已认证主体、issuer 与资源、租户、匹配的方法与名称、规范化参数、准入描述符锁定、后端健康、能力交集、数据分类、限流状态和任何动作绑定批准，重新计算策略。顺序很重要：注册记录可以仍有效而用户角色已被撤销——运行时策略才是首要的允许/拒绝决定，注册与描述符证据只是输入。

Admission decides which backend version may enter the gateway. It does not authorize a live call. For every request, the gateway recomputes policy from the authenticated principal, issuer and resource, tenant, matched method and name, normalized arguments, admitted descriptor pin, current backend health, capability intersection, data classification, rate state, and any action-bound approval.

> 准入决定哪个后端版本可以进入网关，但不授权一次实际调用。对每个请求，网关都要从已认证主体、issuer 与资源、租户、匹配的方法与名称、规范化参数、准入描述符锁定、当前后端健康、能力交集、数据分类、限流状态和任何动作绑定批准中重新计算策略。

This ordering matters. A Registry record can remain active while a user's role is revoked. A descriptor can remain pinned while a destination argument crosses a tenant boundary. A backend can remain approved while incident policy quarantines state-changing calls. Runtime policy is therefore the primary allow or deny decision, with Registry and descriptor evidence as inputs.

> 这个顺序很重要：注册记录可以仍处于 active 而用户的角色已被撤销；描述符可以仍被锁定而目标参数跨越了租户边界；后端可以仍被批准而事故策略隔离了状态变更调用。因此运行时策略是首要的允许/拒绝决定，注册与描述符证据只是输入。

Do not cache an allow decision under a connection or removed session identifier. If policy is unavailable, follow a declared failure policy by operation class. A safe default is to fail closed for state changes and sensitive reads, while explicitly approved public read paths may use a short-lived last-known policy only when their risk model permits it. Record which policy version and failure path made the decision, then validate the backend result before returning it.

> 不要把"允许"决定缓存在连接或已移除的会话标识之下。策略不可用时，按操作类别执行已声明的失败策略。安全默认：状态变更与敏感读一律失效关闭（fail-closed）；显式批准的公共读路径只有在风险模型允许时才可用短期的最后已知策略。记录做决定的策略版本与失败路径，然后在返回前校验后端结果。

> ⚠️ **【易错点】** 场景：网关把"允许"决定缓存在连接 ID 或旧会话 ID 下 / 后果：用户角色被撤销、租户被隔离后，旧连接上的请求仍被放行——策略绕过 / 修复：(1) 每个请求重算策略，锚点是已认证主体而非连接；(2) 策略服务不可用时按操作类别 fail-closed（写操作和敏感读直接拒绝）；(3) 审计里记录策略版本与失败路径，让"为什么放行/拒绝"可复盘。

### One POST endpoint

Modern Streamable HTTP sends each JSON-RPC message through POST:

> 现代 Streamable HTTP 通过 POST 发送每条 JSON-RPC 消息：

```text
POST /mcp
Authorization: Bearer <gateway-token>
MCP-Protocol-Version: 2026-07-28
Mcp-Method: tools/call
Mcp-Name: notes.search
Accept: application/json, text/event-stream
```

The gateway can return JSON or request-scoped SSE for that POST. GET and DELETE return 405 for modern requests. `Mcp-Session-Id` and `Last-Event-ID` do not create authority, affinity, or replay behavior.

> 网关可以为该 POST 返回 JSON 或请求级 SSE。现代请求的 GET 和 DELETE 返回 405。`Mcp-Session-Id` 与 `Last-Event-ID` 不产生权威、亲和或重放行为。

Header and body values must agree. Reject mismatch with `-32020` before looking up a backend. This lets load balancers, gateways, and rate limiters route without parsing the full body while preserving end-to-end integrity.

> 头与正文的值必须一致。在查找后端之前用 `-32020` 拒绝不匹配。这让负载均衡器、网关和限流器不用解析完整正文就能路由，同时保住端到端完整性。

Validate in one exact order: JSON-RPC and metadata types, header and body equality, then support for the matched version. A mismatch returns HTTP 400 with `-32020`. If header and body agree on an unsupported version, return HTTP 400 with `-32022` and `data` exactly `{"supported":["2026-07-28"],"requested":"<actual>"}`. An unknown method returns HTTP 404 with `-32601`.

> 按唯一精确顺序校验：JSON-RPC 与元数据类型、头与正文相等、然后对匹配版本的支持。不匹配返回 HTTP 400 `-32020`；头文一致但版本不支持，返回 HTTP 400 `-32022` 且 `data` 精确为 `{"supported":["2026-07-28"],"requested":"<actual>"}`；未知方法返回 HTTP 404 `-32601`。

`ProtocolError` carries optional `data`, and the gateway serializes it into the JSON-RPC error object. A notification has no `id`, so it never receives a JSON-RPC success or error. An accepted HTTP notification returns 202 with an empty body.

> `ProtocolError` 携带可选 `data`，网关把它序列化进 JSON-RPC 错误对象。通知没有 `id`，永远不收 JSON-RPC 成功或错误响应。被接受的 HTTP 通知返回 202 空体。

### Implement discovery at every layer

The gateway implements `server/discover` for clients. It also discovers each backend so it knows protocol versions, capabilities, and extensions.

> 网关为客户端实现 `server/discover`；同时也发现每个后端，以便知道协议版本、能力和扩展。

Example gateway result:

> 网关结果示例：

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

Advertise only the capability intersection the gateway can honor end to end. A backend feature is not automatically safe to expose. A gateway feature with no backend path is not useful to advertise.

> 只通告网关能端到端兑现的能力交集。后端的功能不自动等于可对外暴露；没有后端路径支撑的网关功能通告了也没用。

`serverInfo` is self-reported display and diagnostic data. Do not use it as registry or publisher proof.

> `serverInfo` 是自报的展示与诊断数据，不要当注册中心或发布者证明用。

### Per-request client capabilities

Every forwarded request needs a current `_meta` envelope:

> 每个转发的请求都需要当前的 `_meta` 信封：

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

Do not blindly copy the outer client capabilities to a backend. The gateway is the backend's client. Advertise only features the gateway will mediate correctly.

> 不要把外层客户端的能力原样照抄给后端。网关才是后端的客户端。只通告网关能正确中介的特性。

### Deterministic namespacing

Merge backend tools under stable public names:

> 用稳定的公开名称合并后端工具：

```text
notes.search
notes.create
issues.list
issues.open
```

Keep a mapping from public name to backend and original tool name. Never choose the first or last collision. A public name is part of the approval and audit contract, so changing it is a migration.

> 保留"公开名 → 后端 + 原始工具名"的映射。绝不在重名冲突里选先来后到。公开名是审批与审计契约的一部分，改它就是一次迁移。

`tools/list` must be deterministic. When visibility differs by principal, return `cacheScope: private`. A bounded `ttlMs` reduces backend discovery load without allowing a user-specific list to leak across authorization contexts.

> `tools/list` 必须确定性。当可见性因主体而异时返回 `cacheScope: private`。有界的 `ttlMs` 降低后端发现负载，又不让按用户定制的列表跨授权上下文泄漏。

Every exposed tool descriptor includes a stable name, description, and object-root `inputSchema`. Namespacing cannot remove required descriptor fields. The complete list result also includes `resultType`, server identity metadata, and cache hints.

> 每个暴露的工具描述符都含稳定名称、描述和对象根 `inputSchema`。命名空间化不能删掉必填的描述符字段。完整列表结果还包括 `resultType`、服务器身份元数据和缓存提示。

### Pin approved descriptors

At admission time, canonicalize the complete descriptor and store its digest under the qualified public name. At list and call time, compare the live descriptor with the approved digest.

> 准入时规范化完整描述符，把摘要存到限定公开名之下。列表与调用时，把线上描述符与已批准摘要比对。

If it changes:

- Remove it from `tools/list`.
  中文翻译：从 `tools/list` 移除它。
- Reject direct calls.
  中文翻译：拒绝直接调用。
- Emit an audit event.
  中文翻译：发出审计事件。
- Require policy or human re-approval before updating the pin.
  中文翻译：更新锁定前要求策略或人工重新批准。

A gateway is a useful central enforcement point, but it does not turn a first-seen descriptor into a safe one. Initial review remains necessary.

> 网关是有用的集中执行点，但它不能把"第一次见到的描述符"变成安全的。初始评审仍然必要。

### Registries help discover, not decide

> **【中文解读】** 注册中心的 `server.json` 只是发布元数据：它说明"这个包叫什么、怎么装、版本号是多少"，不带网关的安全决定。已验证的发布者与来源证据要放在独立的准入状态里，网关把 `server.json` 与准入状态做连接（join）。每个准入后端要记录：精确注册中心与记录标识、已验证发布者命名空间、允许的传输与端点、锁定版本、工件/描述符摘要、授权 issuer 与资源、评审人/审批时间/有效期。

A Registry `server.json` provides publication metadata. A package-backed record can look like this:

> 注册中心的 `server.json` 提供发布元数据。一个带包的记录长这样：

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

Publication metadata does not carry the gateway's security decision. Keep verified publisher and provenance evidence in separate admission state:

> 发布元数据不承载网关的安全决定。把已验证的发布者与来源证据放进独立的准入状态：

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

The gateway checks the `server.json` shape and joins it to that external state. The gateway still needs an admission policy.

> 网关检查 `server.json` 的形状并把它与那份外部状态做连接。网关仍然需要自己的准入策略。

For each admitted backend, record:

- Exact registry and record identifier.
  中文翻译：精确的注册中心与记录标识。
- Verified publisher namespace or domain evidence.
  中文翻译：已验证的发布者命名空间或域名证据。
- Allowed transport and endpoint.
  中文翻译：允许的传输与端点。
- Pinned version or approved upgrade policy.
  中文翻译：锁定的版本或已批准的升级策略。
- Artifact or descriptor digest.
  中文翻译：工件或描述符摘要。
- Authorization issuer and resource.
  中文翻译：授权 issuer 与资源。
- Reviewer, approval time, and expiry.
  中文翻译：评审人、批准时间与有效期。

Do not accept a server because its display name resembles a familiar product. Do not treat registry presence as an operational security review. Private servers can be admitted through the same evidence schema even when they never appear in a public registry.

> 不要因为展示名像某个熟悉产品就接受一台服务器；不要把"上了注册中心"当作一次运维安全评审。私有服务器即使从未出现在公共注册中心，也可以走同一套证据模式准入。

This lesson implements the gateway seam: join publication evidence to local admission before a backend becomes routable. [Lesson 30: MCP Registry Supply Chain, Admission, Drift, and Rollback](../../30-mcp-registry-supply-chain-and-drift/docs/en.md) builds the full control plane for exact namespace proof, artifact provenance, immutable pins, live descriptor drift, Registry status reconciliation, a tamper-evident admission ledger, and evidence-backed rollback. Keep that supply-chain state separate from the per-request runtime decision above.

> 本课实现的是网关接缝：在后端可路由之前，把发布证据连接到本地准入。Lesson 30 构建完整控制平面——精确命名空间证明、工件来源、不可变锁定、线上描述符漂移、注册中心状态对账、防篡改准入账本和有证据支撑的回滚。要把那套供应链状态与上面的每请求运行时决定分开。

> 🤔 **【困惑】** Q: 注册中心都验证了发布者，为什么网关还要自己的准入策略？A: 注册中心验证的是"发布者是谁"，不是"你的企业该不该用"。注册记录可以保持有效而用户角色已被撤销；描述符保持锁定而目标参数跨租户；后端保持批准而事故策略隔离状态变更调用。发现证据解决"这货是谁家的"，准入与运行时策略解决"这货现在能不能进、能上哪条产线"。

### Credential mediation

The gateway authenticates its callers and separately authenticates to backends. Backend credentials never go to the client.

> 网关认证自己的调用方，并单独向后端做认证。后端凭证永远不到客户端手上。

Keep these bindings explicit:

> 让这些绑定保持显式：

```text
outer principal -> gateway role and policy
backend issuer + resource -> backend registration and token
```

Never pass the outer gateway token to a backend. Never reuse a backend token at a different issuer or resource. If a tool acts on behalf of an end user, preserve that delegation with a designed exchange or claims model rather than impersonating the user with a shared service credential.

> 绝不把外层网关 token 传给后端；绝不把后端 token 用到另一个 issuer 或资源上。如果工具代表最终用户行动，要用设计过的交换或声明模型保留这层委托，而不是拿共享服务凭证冒充用户。

### Rate limits without sessions

Key limits by authenticated principal, issuer, resource, public tool, cost class, and time window. A session id is absent and would be easy to rotate even if it existed.

> 限流按已认证主体、issuer、资源、公开工具、成本类别和时间窗口取键。会话 id 已不存在；即便存在也容易轮换，不可作键。

Apply cheap validation before consuming expensive work. Decide whether rejected calls count against abuse limits, business quotas, or both.

> 先做便宜的校验，再消耗昂贵的工作。并决定被拒绝的调用是否计入滥用限额、业务配额或两者。

### Audit the decision chain

Record enough to reconstruct a call:

> 记录足够重建一次调用的信息：

- Request and trace identifiers.
  中文翻译：请求与追踪标识符。
- Authenticated principal and issuer.
  中文翻译：已认证主体与 issuer。
- Public tool and backend route.
  中文翻译：公开工具与后端路由。
- Descriptor pin version.
  中文翻译：描述符锁定版本。
- Policy decision and reason.
  中文翻译：策略决定与理由。
- Latency and result class.
  中文翻译：延迟与结果类别。
- MRTR round or task identifier when applicable.
  中文翻译：适用时的 MRTR 轮次或任务标识符。

Redact bearer tokens, authorization codes, refresh tokens, raw secrets, and unnecessary sensitive arguments.

> 对 bearer token、授权码、refresh token、原始秘密和不必要的敏感参数做脱敏。

### Request-scoped SSE

A normal POST may return request-scoped SSE when work streams during that one request. Closing the response stream cancels that in-flight modern HTTP request.

> 当工作在这一个请求内流式产出时，普通 POST 可以返回请求级 SSE。关闭响应流即取消这个进行中的现代 HTTP 请求。

Do not create a separate GET stream and do not promise Last-Event-ID replay. Those are older transport assumptions.

> 不要另建 GET 流，也不要承诺 Last-Event-ID 重放。那些是旧的传输假设。

### Long-lived change notifications

For list and resource change notifications, a current client sends `subscriptions/listen` through POST and receives an SSE response. Notification filters use the exact flat fields `toolsListChanged`, `promptsListChanged`, `resourcesListChanged`, and `resourceSubscriptions`:

> 对列表与资源变更通知，当前客户端通过 POST 发送 `subscriptions/listen` 并收到 SSE 响应。通知过滤器使用精确的扁平字段 `toolsListChanged`、`promptsListChanged`、`resourcesListChanged` 和 `resourceSubscriptions`：

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

The first event acknowledges the supported subset. Its subscription identifier is the JSON-RPC id of the request that opened the stream:

> 第一个事件确认受支持的子集。其订阅标识符就是打开这条流的那个请求的 JSON-RPC id：

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

The gateway then forwards only the acknowledged change types. Every notification on that stream carries the same `io.modelcontextprotocol/subscriptionId` in `params._meta`. There is no automatic replay or automatic re-listen. On reconnect, the client reopens the subscription and refreshes the lists it relies on. A server-initiated graceful close returns a final complete result tagged with the same subscription id.

> 之后网关只转发已确认的变更类型。这条流上的每个通知都在 `params._meta` 里带同一个 `io.modelcontextprotocol/subscriptionId`。没有自动重放，也没有自动重新监听。重连时客户端重新打开订阅并刷新它依赖的列表。服务器主动优雅关闭时，返回带同一订阅 id 的最终完整结果。

The modern path replaces `resources/subscribe`, `resources/unsubscribe`, and unsolicited standalone GET streaming. Keep those only in a version-gated older path.

> 现代路径取代了 `resources/subscribe`、`resources/unsubscribe` 和未经请求的独立 GET 流。把这些只保留在版本门控的旧路径里。

### MRTR through a gateway

> **【中文解读】** 后端返回 `resultType: input_required` 时，网关只有在外层客户端支持所需输入请求的情况下才能转发该结果。除非网关刻意终结并重新发起交互，`requestState` 必须逐字节原样保留。客户端用新的 JSON-RPC id 和 `inputResponses` 重试原公开工具；网关对重试重新授权、检查同一公开路由，再转发一个全新的后端请求——绝不假设早先一轮授予了无限批准。

When a backend returns `resultType: input_required`, the gateway can forward that result only if the outer client supports the needed input request. Preserve `requestState` byte for byte unless the gateway deliberately terminates and reissues the interaction.

> 后端返回 `resultType: input_required` 时，只有外层客户端支持所需输入请求，网关才能转发该结果。除非网关刻意终结并重新发起交互，`requestState` 要逐字节保留。

The client retries the original public tool with a fresh JSON-RPC id and `inputResponses`. The gateway re-authorizes the retry, checks the same public route, then forwards a fresh backend request. It must not assume an earlier round granted unlimited approval.

> 客户端用新的 JSON-RPC id 和 `inputResponses` 重试原公开工具。网关对重试重新授权、检查同一公开路由，然后转发全新的后端请求。绝不能假设早先一轮授予了无限批准。

### Tasks extension routing

> **【中文解读】** Tasks 是官方扩展（`io.modelcontextprotocol/tasks`），不是核心会话的替代品。后端可对 `tools/call` 返回 `resultType: task`（带 `taskId`、状态、时间戳、`ttlMs`、可选 `pollIntervalMs`）；后续 `tasks/get`/`tasks/update`/`tasks/cancel` 用 `params.taskId` 作 `Mcp-Name`，给中间件一个路由键。网关为不透明任务 id 记录主体与后端路由。不要实现新的 `tasks/list` 或 `tasks/result`——那是旧实验模型的词汇。

Tasks are an official extension identified by `io.modelcontextprotocol/tasks`. They are not a core session replacement.

> Tasks 是由 `io.modelcontextprotocol/tasks` 标识的官方扩展，不是核心会话的替代品。

The client declares the extension inside per-request client capabilities, and the gateway advertises it in discovery only when it can preserve the lifecycle end to end. For a supported `tools/call`, the backend alone decides whether to return the ordinary result or `resultType: task`. A task result carries `taskId`, `status`, timestamps, `ttlMs`, and an optional `pollIntervalMs` directly in the result. The task must already be durably readable before that result is sent.

> 客户端在每请求客户端能力里声明该扩展；网关只有在能端到端保住任务生命周期时才在发现中通告它。对受支持的 `tools/call`，是否返回普通结果或 `resultType: task` 由后端单独决定。任务结果直接在结果里带 `taskId`、`status`、时间戳、`ttlMs` 和可选的 `pollIntervalMs`。发送该结果之前，任务必须已经可持久读取。

The gateway records the authenticated principal and backend route for the opaque task identifier. Subsequent `tasks/get`, `tasks/update`, and `tasks/cancel` calls use `params.taskId` as `Mcp-Name`, which gives intermediaries a routing key. `tasks/get` returns `resultType: complete` with the current task state and inlines the final result or protocol error in a terminal state. `tasks/update` sends keyed `inputResponses` for outstanding task input and returns an empty complete acknowledgment. `tasks/cancel` is a cooperative intent with an empty complete acknowledgment, not a guarantee that work stops.

> 网关为不透明的任务标识符记录已认证主体与后端路由。后续的 `tasks/get`、`tasks/update`、`tasks/cancel` 调用用 `params.taskId` 作 `Mcp-Name`，给中间件一个路由键。`tasks/get` 返回 `resultType: complete` 与当前任务状态，并在终态内联最终结果或协议错误。`tasks/update` 为未决的任务输入发送带键的 `inputResponses`，返回空的完成确认。`tasks/cancel` 是协作式意图加空的完成确认，不保证工作真的停止。

Do not implement new `tasks/list` or `tasks/result` methods. They belong to the older experimental model. A task that needs input exposes complete embedded requests through `tasks/get`; the client answers them through `tasks/update`, not by retrying the original tool call. The client still polls at the suggested interval; task creation remains server-directed.

> 不要实现新的 `tasks/list` 或 `tasks/result` 方法——它们属于较旧的实验模型。需要输入的任务通过 `tasks/get` 暴露完整的内嵌请求；客户端通过 `tasks/update` 回答，而不是重试原工具调用。客户端仍按建议间隔轮询；任务创建仍由服务器主导。

Durable task route state is application data keyed by the task handle, not a protocol session.

> 持久的任务路由状态是按任务句柄取键的应用数据，不是协议会话。

### Compatibility boundary

If the gateway must serve an older client or backend:

> 如果网关必须服务较旧的客户端或后端：

- Detect the era explicitly.
  中文翻译：显式检测协议年代。
- Keep initialization, transport sessions, GET streams, resource subscriptions, and old task vocabulary inside a legacy adapter.
  中文翻译：把初始化、传输会话、GET 流、资源订阅和旧任务词汇全部留在遗留适配器里。
- Never leak a legacy session id into modern routing or authorization.
  中文翻译：绝不让遗留会话 id 泄漏进现代路由或授权。
- Prefer a bounded discovery probe and explicit fallback policy over silent downgrade.
  中文翻译：优先用有界的发现探测加显式回退策略，而非静默降级。

```figure
t3-gateway-funnel
```

## Build It | 动手构建

> **【中文解读】** `code/main.py` 实现进程内协议网关 + 两个后端服务器。每个后端收到全新的当前协议请求；网关提供发现、按用户过滤的确定性 `tools/list`、命名空间路由、注册中心 `server.json` + 外部准入状态、描述符锁定、RBAC、按主体取键的限流、审计决定，以及建模的 `subscriptions/listen` SSE 确认。模型接收已解析的请求正文、路由头和已认证的 Bearer 身份，不是完整 HTTP 适配器——传输层契约归 Lesson 09。

`code/main.py` implements an in-process protocol gateway and two backend servers. Each backend receives a fresh current-protocol request. The gateway provides discovery, user-filtered deterministic `tools/list`, namespaced routing, Registry `server.json` plus external admission state, descriptor pins, RBAC, principal-keyed rate limits, audit decisions, and a modeled `subscriptions/listen` SSE acknowledgment.

> `code/main.py` 实现进程内协议网关和两个后端服务器。每个后端收到全新的当前协议请求。网关提供发现、按用户过滤的确定性 `tools/list`、命名空间路由、注册中心 `server.json` 加外部准入状态、描述符锁定、RBAC、按主体取键的限流、审计决定，以及建模的 `subscriptions/listen` SSE 确认。

The model receives parsed request bodies, routing headers, and an authenticated bearer identity. It is not a complete HTTP adapter and does not parse `Content-Type` or the full `Accept` contract. Connect it to Lesson 09's Streamable HTTP adapter, which requires `Content-Type: application/json` and an `Accept` value containing both `application/json` and `text/event-stream`.

> 模型接收已解析的请求正文、路由头和已认证的 Bearer 身份。它不是完整 HTTP 适配器，不解析 `Content-Type` 或完整的 `Accept` 契约。把它接到 Lesson 09 的 Streamable HTTP 适配器上——那边要求 `Content-Type: application/json`，且 `Accept` 同时包含 `application/json` 与 `text/event-stream`。

Run it:

> 运行：

```bash
cd phases/13-tools-and-protocols/17-mcp-gateways-and-registries
python3 code/main.py
python3 -m unittest discover code/tests -v
```

The demo prints the outer request id and fresh backend request id so the stateless hop is visible.

> 演示会打印外层请求 id 和全新的后端请求 id，让这一跳的无状态性可见。

## Use It | 实际使用

Replace the in-process backend objects with real current-protocol clients. Keep the same seams:

> 把进程内后端对象换成真实的当前协议客户端。保留同样的接缝：

- Admission record before connection.
  中文翻译：连接之前先有准入记录。
- Backend discovery before capability exposure.
  中文翻译：能力暴露之前先完成后端发现。
- Qualified public name before authorization.
  中文翻译：授权之前先确定限定公开名。
- Descriptor pin before list or call.
  中文翻译：列表或调用之前先核对描述符锁定。
- Fresh per-request metadata before forwarding.
  中文翻译：转发之前先构造新鲜的每请求元数据。
- Result validation before returning.
  中文翻译：返回之前先校验结果。

## Ship It | 产出物

This lesson ships `outputs/skill-gateway-bootstrap.md`. It produces a modern gateway design covering ingress, discovery, admission, namespaces, authorization, caching, streaming, subscriptions, MRTR, Tasks, observability, and legacy isolation.

> 本课产出 `outputs/skill-gateway-bootstrap.md`。它生成现代网关设计，覆盖入口、发现、准入、命名空间、授权、缓存、流式、订阅、MRTR、Tasks、可观测性和遗留隔离。

## Exercises | 练习题

1. Add trace context to the outer and forwarded request metadata and record the correlation in the audit event.
   中文翻译：给外层与转发的请求元数据加追踪上下文，并把关联关系记进审计事件。
2. Add a Tasks-capable backend and route `tasks/get` by task id in `Mcp-Name`.
   中文翻译：添加支持 Tasks 的后端，并按 `Mcp-Name` 里的任务 id 路由 `tasks/get`。
3. Change one backend descriptor and prove both discovery and direct call are blocked.
   中文翻译：变更一个后端描述符，证明发现和直接调用都被阻止。
4. Add a principal-specific server capability and explain why discovery must remain privately cached.
   中文翻译：添加按主体定制的服务器能力，并解释为什么发现必须保持私有缓存。
5. Write a legacy adapter interface without adding any legacy state to the modern `Gateway` class.
   中文翻译：编写遗留适配器接口，且不给现代 `Gateway` 类添加任何遗留状态。

## Key Terms | 术语速查表

| Term | Meaning | 中文 |
|------|---------|------|
| MCP gateway | Policy and routing server between clients and backend MCP servers | MCP 网关：客户端与后端 MCP 服务器之间的策略与路由服务器 |
| Admission record | Evidence and policy decision allowing one backend into the gateway | 准入记录：允许一个后端进入网关的证据与策略决定 |
| Qualified tool name | Stable public route such as `notes.search` | 限定工具名：稳定的公开路由，如 `notes.search` |
| Descriptor pin | Approved digest checked during discovery and dispatch | 描述符锁定：发现与分发期间核对的已批准摘要 |
| Private cache scope | Cached result restricted to one authorization context | 私有缓存范围：缓存结果限定于单一授权上下文 |
| Request-scoped SSE | Streaming response attached to one POST request | 请求级 SSE：附着于单个 POST 请求的流式响应 |
| `subscriptions/listen` | Client-opened SSE stream for selected long-lived change notifications | 客户端打开的 SSE 流，用于选定的长效变更通知 |
| Task route | Application mapping from an opaque task id to its backend | 任务路由：从不透明任务 id 到其后端的应用层映射 |
| Legacy adapter | Explicit version-gated boundary for old handshake and session behavior | 遗留适配器：为旧握手与会话行为设置的显式版本门控边界 |

## Further Reading | 延伸阅读

- [Streamable HTTP transport](https://modelcontextprotocol.io/specification/2026-07-28/basic/transports/streamable-http)
  中文说明：Streamable HTTP 传输规范——单 POST 端点与请求级 SSE 契约。
- [Server discovery](https://modelcontextprotocol.io/specification/2026-07-28/server/discover)
  中文说明：`server/discover` 规范——网关与后端的双层发现依据。
- [Official Registry server.json requirements](https://github.com/modelcontextprotocol/registry/blob/main/docs/reference/server-json/official-registry-requirements.md)
  中文说明：官方注册中心 `server.json` 要求——发布元数据的字段契约。
- [MCP Tasks extension](https://tasks.extensions.modelcontextprotocol.io/specification/draft/tasks)
  中文说明：MCP Tasks 扩展草案——任务生命周期与 `Mcp-Name` 路由键。
