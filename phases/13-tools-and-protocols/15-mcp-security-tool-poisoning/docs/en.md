# MCP Security: Poisoned Metadata, Routing, and MRTR State | MCP 安全：投毒元数据、路由与 MRTR 状态

> Stateless does not mean trustless. It means every request exposes the evidence a server and gateway need to validate the call independently.

> **【中文解读】** 无状态不等于无需信任。2026-07-28 版 MCP 移除了核心握手与协议会话，安全边界随之改变：工具描述、注解、客户端/服务器信息一律按不可信数据处理。本课把七种攻击面列成具体清单，教你在网关里做描述符整体哈希锁定、路由头先于策略的校验，以及 MRTR 确认状态的防篡改保护。

> **【拓展】** 工具描述直接进入模型上下文，元数据因此成为 MCP 最大的威胁面——等同于让第三方在系统提示里注入任意指令。2025-2026 年 Invariant Labs、Unit 42 等研究测得前沿模型对隐藏指令的遵从率高达 70% 以上；2026-07-28 规范的回应不是单一检测器，而是"证据链"思路：每个请求自带的元数据就是独立校验的依据。防御从"检测会话异常"转为"校验请求自证"。

> 🔗 **【前置】** 学本节前请先掌握：(1) Phase 13 · 07（MCP server）与 13 · 08（MCP client）——理解工具描述如何进入模型上下文；(2) Phase 13 · 09 的 Streamable HTTP——本课直接复用其路由头（`Mcp-Method`/`Mcp-Name`）；(3) MRTR（多轮往返请求）的基本形态。

**Type:** Learn | **类型:** 学习
**Languages:** Python | **语言:** Python
**Prerequisites:** Phase 13 · 07 (MCP server), Phase 13 · 08 (MCP client) | **前置知识:** Phase 13 · 07（MCP 服务器）、Phase 13 · 08（MCP 客户端）
**Time:** ~60 minutes | **时间:** 约 60 分钟

## Learning Objectives | 学习目标

- Treat tool descriptions, annotations, client information, and server information as untrusted data.
  中文翻译：把工具描述、注解、客户端信息和服务器信息当作不可信数据。
- Detect metadata poisoning, descriptor changes, and cross-server name collisions.
  中文翻译：检测元数据投毒、描述符变更和跨服务器命名冲突。
- Validate the 2026-07-28 request metadata and Streamable HTTP routing headers.
  中文翻译：校验 2026-07-28 请求元数据和 Streamable HTTP 路由头。
- Protect MRTR `requestState` against tampering and bind confirmation to exact arguments.
  中文翻译：保护 MRTR `requestState` 免遭篡改，并把确认绑定到精确参数。
- Apply authorization and rate limits to a principal, not a removed protocol session.
  中文翻译：把授权和限流应用到主体（principal），而不是已被移除的协议会话。

> **【中文解读】** 学习目标：所有元数据一律不可信；检测元数据投毒、描述符变更、命名冲突三类问题；按 2026-07-28 规范校验请求信封与路由头；防 MRTR 状态篡改并把确认绑定精确参数；授权与限流锚定到主体而非已删除的会话。

## The Problem | 问题引入

> **【中文解读】** 问题本质：模型、路由器、用户三方都依赖服务器提供的元数据做决策，一个恶意描述符可以同时攻击三方。官方安全指南的态度很直接——除非来自受信服务器，描述和注解一律不可信；即便来自受信服务器，部署信任也会随更新、攻陷、注册失误、网关合并而变化。

A model reads tool descriptions to decide what to call. A router reads tool names to decide where to send a request. A user reads labels to decide what to approve. One malicious descriptor can target all three.

> 模型读工具描述来决定调用什么；路由器读工具名来决定把请求发到哪里；用户读标签来决定批准什么。一个恶意描述符可以同时攻击这三方。

The official MCP security guidance is direct: descriptions and annotations should be treated as untrusted unless they come from a trusted server. Even then, deployment trust can change. A server update, compromised package, registry mistake, or gateway merge can alter what the model sees.

> 官方 MCP 安全指南很直接：除非来自受信服务器，描述和注解都应被视为不可信。即便如此，部署信任也会变化——服务器更新、被攻陷的包、注册中心失误或网关合并，都可能改变模型看到的内容。

The current protocol also changes the security boundary. In 2026-07-28 there is no core handshake and no transport session. A security design that keys approval, rate limits, or audit history only by `Mcp-Session-Id` is not a current design.

> 当前协议也改变了安全边界。2026-07-28 版没有核心握手，也没有传输会话。只按 `Mcp-Session-Id` 关联审批、限流或审计历史的安全设计，已经不符合现行规范。

> 💡 **【类比】** 元数据像商品外包装上的标签：采购员（模型）看标签决定进哪个货，分拣线（路由器）看标签决定送哪条线，收货人（用户）看标签决定签不签收——攻击者只要在标签上印一行小字（投毒描述），三方全部中招。2026-07-28 的无状态化相当于"每件货自带完整报关单"（请求元数据）：校验依据随货同行，不再依赖"老客户脸熟"（会话）。哈希锁定像定期比对标签指纹——能发现偷换标签（地毯拉扯），但发现不了第一版标签就印错了字（投毒），所以还要叠加验货环节（执行前削减权限）。

## The Concept | 核心概念

> **【中文解读】** 本节是全课核心，按防御纵深排列：七个攻击面清单 → 请求信封是证据而非身份 → 路由校验先于策略 → 锁定完整描述符 → 静态扫描是绊线 → 合并前先命名空间 → 能力声明不等于授权 → 保护无状态 MRTR 确认 → 高危调用的 Rule of Two → 执行前削减权限 → 遗留交互路径 → 无状态传输检查。

### Seven attack surfaces worth checking

Use a concrete list instead of the vague instruction to be careful.

> 用具体清单取代"要小心"这类空泛提醒。

> **【中文解读】** 七个攻击面：元数据投毒、描述符地毯拉扯、跨服务器影射、头/正文混淆、能力冒用升级、MRTR 状态篡改、供应链身份混淆。注意它们相互重叠——哈希锁定只防"变更"防不了"初版即毒"，静态扫描只抓明显短语，命名空间只消一类冲突。必须叠加控制。

1. **Metadata poisoning.** A description contains instructions unrelated to the declared tool behavior.
  中文翻译：**元数据投毒。** 描述中包含与声明的工具行为无关的指令。
2. **Descriptor rug pull.** A previously approved name, description, schema, or annotation changes.
  中文翻译：**描述符地毯拉扯。** 先前已批准的名称、描述、schema 或注解发生变更。
3. **Cross-server shadowing.** Two backends expose the same unqualified tool name and routing chooses one silently.
  中文翻译：**跨服务器影射。** 两个后端暴露同名未限定工具名，路由静默选择其一。
4. **Header and body confusion.** `Mcp-Method` or `Mcp-Name` disagrees with the JSON-RPC request.
  中文翻译：**头/正文混淆。** `Mcp-Method` 或 `Mcp-Name` 与 JSON-RPC 请求不一致。
5. **Capability escalation.** A peer claims an extension or client feature and the server mistakes that declaration for authorization.
  中文翻译：**能力冒用升级。** 对端声明某扩展或客户端特性，服务器误把声明当授权。
6. **MRTR state tampering.** A client changes `requestState`, answers a different question, or reuses confirmation with different arguments.
  中文翻译：**MRTR 状态篡改。** 客户端篡改 `requestState`、回答另一个问题，或把确认换参数重用。
7. **Supply-chain identity confusion.** A familiar display name is treated as proof of publisher or server identity.
  中文翻译：**供应链身份混淆。** 熟悉的展示名被当作发布者或服务器身份的证明。

These surfaces overlap. Hash pinning helps with descriptor changes but does not prove that the first descriptor was safe. Static scanning catches obvious phrases but not subtle instructions. Namespacing prevents one collision class but not a malicious namespaced server. Stack the controls.

> 这些攻击面相互重叠。哈希锁定有助于发现描述符变更，但证明不了第一个描述符是安全的；静态扫描能抓明显短语，抓不到隐晦指令；命名空间能防一类冲突，防不了恶意的带命名空间服务器。所以要叠加控制。

### The current request envelope is evidence, not identity

> **【中文解读】** 请求信封是证据而非身份：`_meta` 里的 `clientInfo` 是自报的，不能当已认证主体；`serverInfo` 适合日志与调试，但不是证书、注册证明或授权决定。每个请求都要校验版本号和能力形状，用能力选择兼容的响应形状。

Every 2026-07-28 request contains:

```json
{
  "_meta": {
    "io.modelcontextprotocol/protocolVersion": "2026-07-28",
    "io.modelcontextprotocol/clientCapabilities": {
      "elicitation": {"form": {}}
    },
    "io.modelcontextprotocol/clientInfo": {
      "name": "security-lab",
      "version": "1.0.0"
    }
  }
}
```

Validate the version and capability shape on every request. Use capabilities to choose a compatible response shape. Do not use `clientInfo` as an authenticated principal. It is self-reported.

> 每个请求都校验版本和能力形状。用能力选择兼容的响应形状。不要把 `clientInfo` 当作已认证的主体——它是自报的。

The same warning applies to `io.modelcontextprotocol/serverInfo` in result metadata. It is useful for logs and debugging. It is not a certificate, registry proof, or authorization decision.

> 同样的警告适用于结果元数据里的 `io.modelcontextprotocol/serverInfo`。它适合写日志和调试，但不是证书、注册证明或授权决定。

### Validate routing before policy

> **【中文解读】** 路由校验必须先于策略：`Mcp-Method` 必须等于正文 method，`Mcp-Name` 必须等于 `params.name`，不一致一律用 `-32020` 拒绝——而且要发生在选择后端、应用 RBAC、扣限流令牌之前。错误码序列固定：头与正文不匹配 → HTTP 400 `-32020`；头文一致但版本不支持 → HTTP 400 `-32022` 且 `data` 精确为 `{"supported":["2026-07-28"],"requested":"<actual>"}`；未知方法 → HTTP 404 `-32601`。通知没有 `id`，永远不收 JSON-RPC 成功/错误响应，HTTP 层接受后返回 202 空体。

For `tools/call`, Streamable HTTP includes:

```text
MCP-Protocol-Version: 2026-07-28
Mcp-Method: tools/call
Mcp-Name: notes.export
```

The header method must equal the body method. The header name must equal `params.name`. Reject disagreement with `-32020` before selecting a backend, applying RBAC, or consuming a rate-limit token.

> 头里的 method 必须等于正文 method，头里的 name 必须等于 `params.name`。不一致时用 `-32020` 拒绝——要在选择后端、应用 RBAC、消耗限流令牌之前完成。

This ordering closes a common ambiguity: one component authorizes the body while another routes by the header.

> 这个顺序堵住一个常见歧义：一个组件按正文做授权，另一个组件却按路由头做转发。

> ⚠️ **【易错点】** 场景：组件 A 按 JSON-RPC 正文做授权，组件 B 按 `Mcp-Name` 头做路由，头与正文不一致时没人拦截 / 后果：攻击者构造"正文说 notes.search、头说 notes.export"的请求绕过授权直达高危工具 / 修复：(1) 固定校验顺序——先校验 JSON-RPC 与元数据类型，再比对头与正文相等，最后检查版本支持；(2) 头文不一致一律 HTTP 400 `-32020`，绝不"取其一继续"；(3) 限流令牌在全部校验通过后才扣减，防止垃圾请求烧光配额。

Wire validation follows one exact sequence. Validate JSON-RPC and metadata types, compare header values with the body, then check whether the matched version is supported. A mismatched header returns HTTP 400 with `-32020`. If header and body agree on an unsupported version, return HTTP 400 with `-32022` and `data` exactly `{"supported":["2026-07-28"],"requested":"<actual>"}`. An unknown method returns HTTP 404 with `-32601`.

> 线格式校验遵循唯一精确顺序：先校验 JSON-RPC 与元数据类型，再比对头值与正文，最后检查匹配到的版本是否受支持。头不匹配返回 HTTP 400 `-32020`；头文一致但版本不支持，返回 HTTP 400 `-32022` 且 `data` 精确为 `{"supported":["2026-07-28"],"requested":"<actual>"}`；未知方法返回 HTTP 404 `-32601`。

Every error object includes optional `data` when the contract needs structured recovery information. A notification has no `id`, so it never receives a JSON-RPC success or error response. An accepted HTTP notification returns 202 with an empty body.

> 当契约需要结构化恢复信息时，每个错误对象都带可选 `data`。通知没有 `id`，因此永远不收 JSON-RPC 成功或错误响应。被接受的 HTTP 通知返回 202 空体。

### Pin the whole descriptor

A description hash alone misses schema and annotation changes. Canonicalize and hash the descriptor fields the user approved:

> 只哈希描述文本会漏掉 schema 和注解的变更。要对用户批准过的完整描述符字段做规范化并哈希：

```python
normalized = json.dumps(tool, sort_keys=True, separators=(",", ":"))
digest = hashlib.sha256(normalized.encode()).hexdigest()
```

Store the digest under a qualified key such as `notes.export`, together with publisher evidence and approval time outside this toy example.

> 把摘要存到限定名（如 `notes.export`）之下；真实部署中还要附带发布者证据与审批时间——本示例从简。

On every refresh:

- Unknown key: quarantine until review.
  中文翻译：未知键：隔离待审。
- Same key, different digest: quarantine as a rug pull until re-approved.
  中文翻译：同键不同摘要：按地毯拉扯隔离，直到重新批准。
- Duplicate unqualified name: require deterministic namespacing.
  中文翻译：重复的未限定名：要求确定性命名空间。
- Scanner hit: block and review the complete descriptor.
  中文翻译：扫描器命中：阻止并复审完整描述符。

Hash equality proves stability, not safety. A poisoned descriptor stays poisoned when perfectly pinned.

> 哈希相等证明的是稳定性，不是安全性。投毒的描述符被完美锁定之后，依然是投毒的。

> 🤔 **【困惑】** Q: 静态扫描和哈希锁定都不完美，为什么还要做？A: 因为它们便宜且互补。哈希锁定把"描述符变更必须重审"从自觉变成机制，堵死地毯拉扯；静态扫描在安装时和 CI 阶段拦住明显注入。真正兜底的是"执行前削减权限"：typed verb、参数校验、主体授权层层收窄，让漏网的调用也做不成坏事——纵深防御的本意就是每层都假设上一层会失守。

### Static scanning is a tripwire

Simple patterns can flag role tags, instruction overrides, concealment, secret access, and obscured network destinations. They are cheap enough for install time and CI.

> 简单模式可以标记角色标签、指令覆盖、隐匿行为、机密访问和混淆的网络目的地。它们足够便宜，可以放进安装时和 CI。

They are not a semantic proof. A safe description can contain a flagged phrase in a legitimate warning. A malicious description can avoid every phrase. Treat scanner output as review evidence, not an automatic innocence score.

> 静态扫描不是语义证明。安全的描述可能因合法警告含被标记短语；恶意的描述可以避开所有短语。把扫描输出当评审证据，而不是自动的"无害分"。

### Namespace before merging

Suppose two servers both expose `search`. Never let discovery order decide which wins.

> 假设两个服务器都暴露 `search`。绝不要让发现顺序决定谁生效。

```text
notes.search
issues.search
```

The qualified name is the public gateway name. Record the backend mapping separately. Stable names make approval, audit, hash pins, and `Mcp-Name` routing refer to the same object.

> 限定名是网关对外公开的名称；后端映射单独记录。稳定的名字让审批、审计、哈希锁定和 `Mcp-Name` 路由指向同一个对象。

### Capabilities are compatibility declarations

Per-request `clientCapabilities` tells a server which protocol features the client can process. It does not grant the client access to tools, data, or actions.

> 每请求的 `clientCapabilities` 告诉服务器客户端能处理哪些协议特性。它不授予客户端对工具、数据或动作的任何访问权。

Authorization still comes from the authenticated principal and resource policy. The sequence is:

> 授权仍来自已认证主体和资源策略。顺序是：

1. Authenticate transport credentials.
  中文翻译：认证传输层凭证。
2. Validate version, headers, and request shape.
  中文翻译：校验版本、头部和请求形状。
3. Check capability compatibility.
  中文翻译：检查能力兼容性。
4. Authorize principal, tool, resource, and arguments.
  中文翻译：授权主体、工具、资源和参数。
5. Execute or request user input.
  中文翻译：执行或请求用户输入。

### Protect stateless MRTR confirmation

> **【中文解读】** MRTR（多轮往返请求）取代了服务器到客户端的回调：服务器返回 `resultType: input_required` + `inputRequests`（完整内嵌请求）+ 不透明的 `requestState`；客户端拿到用户输入后用新的 JSON-RPC id 重试原方法并附上 `inputResponses`。安全要点：`requestState` 是敌意输入——必须签名或加密，并绑定到 method、工具、精确参数、用途、过期时间、主体，重放要紧时还要绑定一次性 nonce。nonce 账本不能放在单个网关对象里，要外置为可共享、带 TTL 清理的条件占用存储。

A consequential tool may need user confirmation. Current MCP uses Multi Round-Trip Requests instead of a server-to-client callback.

> 后果性工具可能需要用户确认。当前 MCP 用多轮往返请求（MRTR）取代服务器到客户端的回调。

First response:

```json
{
  "resultType": "input_required",
  "inputRequests": {
    "confirm": {
      "method": "elicitation/create",
      "params": {
        "mode": "form",
        "message": "Export notes to archive?",
        "requestedSchema": {
          "type": "object",
          "properties": {
            "confirm": {"type": "boolean"}
          },
          "required": ["confirm"]
        }
      }
    }
  },
  "requestState": "opaque-integrity-protected-value"
}
```

The client obtains input and retries the original method with a new JSON-RPC id:

```json
{
  "jsonrpc": "2.0",
  "id": 2,
  "method": "tools/call",
  "params": {
    "name": "notes.export",
    "arguments": {"query": "private", "destination": "archive"},
    "requestState": "opaque-integrity-protected-value",
    "inputResponses": {
      "confirm": {
        "action": "accept",
        "content": {"confirm": true}
      }
    },
    "_meta": {
      "io.modelcontextprotocol/protocolVersion": "2026-07-28",
      "io.modelcontextprotocol/clientCapabilities": {
        "elicitation": {"form": {}}
      }
    }
  }
}
```

Each `inputRequests` value is a complete embedded request with `method` and `params`. Its key must match the corresponding entry in `inputResponses`. A form elicitation uses an object-root `requestedSchema`, and the client must have declared form elicitation capability before the server requests it.

> 每个 `inputRequests` 值都是带 `method` 和 `params` 的完整内嵌请求，其键必须与 `inputResponses` 中对应条目匹配。表单诱导输入（elicitation）使用对象根的 `requestedSchema`，且服务器发起请求前，客户端必须已声明表单诱导能力。

The current capability has two valid form declarations. `{"elicitation":{}}` implicitly supports form elicitation, while `{"elicitation":{"form":{}}}` states it explicitly. A URL-only declaration such as `{"elicitation":{"url":{}}}` does not support a form request. The server returns HTTP 400 with `-32021` and `data.requiredCapabilities` equal to `{"elicitation":{"form":{}}}`.

> 当前能力有两种有效的表单声明：`{"elicitation":{}}` 隐式支持表单，`{"elicitation":{"form":{}}}` 显式声明。仅 URL 的声明（如 `{"elicitation":{"url":{}}}`）不支持表单请求，服务器返回 HTTP 400 `-32021`，且 `data.requiredCapabilities` 为 `{"elicitation":{"form":{}}}`。

Treat `requestState` as hostile input. Sign or encrypt it, validate it, and bind it to method, tool, exact arguments, purpose, expiry, principal, and a one-time nonce when replay matters. The lesson code uses HMAC and exact argument matching to make the boundary visible.

> 把 `requestState` 当敌意输入：签名或加密、校验，并绑定到 method、工具、精确参数、用途、过期时间、主体，重放要紧时再绑定一次性 nonce。本课代码用 HMAC 和精确参数匹配让这条边界可见。

The nonce ledger must not live inside one gateway object. The runnable model injects a bounded, TTL-pruned replay store that can be shared by multiple gateway instances. Its atomic claim is the execution boundary: only a validated acceptance or explicit terminal decline consumes state. A malformed response or `cancel` executes nothing and remains retryable until expiry. A production fleet needs the same conditional claim in shared durable storage.

> nonce 账本不能放在单个网关对象里。可运行模型注入一个有界、按 TTL 清理、可被多个网关实例共享的重放存储。它的原子占用就是执行边界：只有校验通过的接受或明确的终局拒绝才消费状态；畸形响应或 `cancel` 不执行任何东西，且在过期前保持可重试。生产集群要把同样的条件占用放进共享持久存储。

Do not store hidden confirmation context in a protocol session. Any server instance should be able to validate the retry.

> 不要把隐藏的确认上下文存进协议会话。任何服务器实例都应能校验这次重试。

### Rule of two for high-risk calls

> **【中文解读】** Rule of Two：沿三条轴分类一次调用——消耗不可信输入、可访问敏感数据、引发后果性外部动作。单次自动步骤不应三者兼得：要么拆分、要么降权、要么通过 MRTR 请求显式用户输入。这是设计启发式，不是协议能力。

Classify a call along three axes:

- It consumes untrusted input.
  中文翻译：它消耗不可信输入。
- It can access sensitive data.
  中文翻译：它可能访问敏感数据。
- It causes a consequential external action.
  中文翻译：它引发后果性的外部动作。

A single automatic step should not combine all three. Split it, reduce privilege, or request explicit user input through MRTR. This is a design heuristic, not a protocol capability.

> 单次自动步骤不应同时组合三项。拆分它、降低权限，或通过 MRTR 请求显式用户输入。这是设计启发式，不是协议能力。

### Reduce authority before execution

Statelessness alone is not safety. It removes hidden protocol history, but a self-contained request can still ask an overpowered handler to leak data or make an irreversible change. Safety comes from reducing authority at each boundary:

> 仅靠无状态并不安全。它移除了隐藏的协议历史，但一个自包含的请求仍可能让权限过大的处理器泄数据或做不可逆变更。安全来自在每个边界削减权限：

1. **Typed verb.** Expose one bounded operation such as `archive_note`, not a generic `run` or `request` tool that can express unrelated powers.
  中文翻译：**类型化动词。** 暴露一个有界操作如 `archive_note`，而不是能表达无关权力的通用 `run` 或 `request` 工具。
2. **Validated arguments.** Use a closed schema where practical, reject unknown fields, normalize identifiers once, cap sizes, and validate destination, tenant, and resource ownership before policy evaluation.
  中文翻译：**校验过的参数。** 尽可能用封闭 schema，拒绝未知字段，标识符只规范化一次，限制大小，并在策略评估前校验目的地、租户和资源归属。
3. **Current authorization.** Bind the authenticated principal to the exact verb, resource, environment, and normalized arguments. Tool annotations and client capabilities do not grant this authority.
  中文翻译：**现行授权。** 把已认证主体绑定到精确的动词、资源、环境和规范化参数。工具注解和客户端能力不授予此权限。
4. **Action-bound approval.** For a consequential call, bind approval to a digest of the typed verb and normalized arguments, plus principal, expiry, and one-time policy. Any changed field requires a new decision.
  中文翻译：**绑定动作的批准。** 对后果性调用，把批准绑定到"类型化动词 + 规范化参数"的摘要，外加主体、过期时间和一次性策略。任何字段变更都需要重新决策。
5. **First-class refusal.** Model deny, expired approval, user decline, and unsafe destination as ordinary outcomes that execute no side effect. Do not translate refusal into a weaker fallback tool.
  中文翻译：**一等公民式的拒绝。** 把拒绝、过期批准、用户否决和不安全目的地当作不执行副作用的普通结果建模，不要把拒绝翻译成更弱的兜底工具。
6. **Redacted audit evidence.** Record who asked, which admitted descriptor and policy version were used, what normalized target was authorized, why the decision allowed or refused, and whether execution began. Store digests or redacted values instead of secrets.
  中文翻译：**脱敏的审计证据。** 记录谁发起、用了哪个准入描述符与策略版本、授权了什么规范化目标、决策为何允许或拒绝、执行是否开始。存摘要或脱敏值，不存秘密。

Each step narrows what the next component may do. The final handler should receive an already validated domain command, not raw model text plus broad credentials. Repeat the entire chain on an MRTR retry, task update, or gateway-forwarded call. An earlier approval does not turn later requests into trusted session traffic.

> 每一步都收窄下一组件能做的事。最终处理器应收到已校验的领域命令，而不是原始模型文本加宽泛凭证。MRTR 重试、任务更新或网关转发时都要重跑整条链。早先的批准不会把后续请求变成可信的会话流量。

### Current and legacy interaction paths

Roots, Sampling, and Logging are deprecated for new 2026-07-28 implementations. A gateway may retain older request-channel code only as a version-gated compatibility path.

> Roots、Sampling 和 Logging 在新的 2026-07-28 实现中已弃用。网关只能把旧请求通道代码保留为版本门控的兼容路径。

Do not build a new defense around a per-session sampling limiter. Apply quotas to authenticated principal, issuer, resource, tool, and time window. For current interactive work, inspect MRTR input requests and responses.

> 不要围绕"按会话的 sampling 限流器"构建新防御。把配额应用到已认证主体、签发方、资源、工具和时间窗。当前的交互式工作应检查 MRTR 输入请求与响应。

### Stateless transport checks

- Accept modern MCP messages at the single POST endpoint.
  中文翻译：在单一 POST 端点接收现代 MCP 消息。
- Return 405 for modern GET and DELETE.
  中文翻译：对现代 GET 和 DELETE 返回 405。
- Do not mint or depend on `Mcp-Session-Id`.
  中文翻译：不铸造、不依赖 `Mcp-Session-Id`。
- Ignore legacy session and replay headers as authority inputs.
  中文翻译：把旧式会话与重放头忽略掉，不作为权威输入。
- Return JSON or request-scoped SSE for that POST.
  中文翻译：为该 POST 返回 JSON 或请求级 SSE。
- Use `subscriptions/listen` only for opted-in long-lived change notifications.
  中文翻译：仅对明确订阅的长效变更通知使用 `subscriptions/listen`。

```figure
tp-tool-poisoning
```

## Build It | 动手构建

> **【中文解读】** `code/main.py` 实现一个小型进程内安全网关模型：规范化并锁定完整工具描述符、报告元数据投毒与跨服务器影射、校验现代请求信封与路由值，并用签名 `requestState` 加注入的共享重放存储完成两轮确认导出。模型假定 HTTP 适配器已解析好 JSON 正文与路由头；传输层契约（`Content-Type`/`Accept`）归 Lesson 09 的 Streamable HTTP 适配器。

`code/main.py` implements a small in-process security gateway model. It canonicalizes and pins full tool descriptors, reports metadata poisoning and shadowing, validates the modern request envelope and routing values, and performs a two-round confirmed export with signed `requestState` and an injected shared replay store.

> `code/main.py` 实现一个小型进程内安全网关模型：规范化并锁定完整工具描述符、报告元数据投毒与影射、校验现代请求信封与路由值，并用签名的 `requestState` 和注入的共享重放存储完成两轮确认导出。

The model starts after an HTTP adapter has parsed the JSON body and routing headers. It does not validate `Content-Type` or `Accept`. Connect the same dispatcher to Lesson 09's complete Streamable HTTP adapter, which requires `Content-Type: application/json` and an `Accept` value containing both `application/json` and `text/event-stream`.

> 模型在 HTTP 适配器解析完 JSON 正文与路由头之后接手，它不校验 `Content-Type` 或 `Accept`。把同一分发器接到 Lesson 09 的完整 Streamable HTTP 适配器上——那边要求 `Content-Type: application/json`，且 `Accept` 同时包含 `application/json` 与 `text/event-stream`。

Run it:

> 运行：

```bash
cd phases/13-tools-and-protocols/15-mcp-security-tool-poisoning
python3 code/main.py
python3 -m unittest discover code/tests -v
```

The sample intentionally mutates a descriptor. The scanner and digest comparison produce independent findings. The export then demonstrates the `input_required` response and stateless retry.

> 示例故意变更一个描述符：扫描器和摘要比较各自产出独立发现；随后的导出演示 `input_required` 响应与无状态重试。

## Use It | 实际使用

Replace `SAFE_TOOLS` with a normalized snapshot from your own approved servers. Keep credentials and secrets out of the snapshot. Review every new or changed descriptor before updating its digest.

> 把 `SAFE_TOOLS` 换成你自己已批准服务器的规范化快照。凭证和秘密不要进快照。每个新增或变更的描述符都要先复审、再更新摘要。

At a gateway, run the same checks during discovery and again before dispatch. A cache can reduce discovery work, but a cached approval must expire or be invalidated when the descriptor changes.

> 在网关处，发现阶段和分发前各跑一遍同样的检查。缓存可以减少发现工作量，但描述符变更时，缓存的批准必须过期或失效。

## Ship It | 产出物

This lesson ships `outputs/skill-mcp-threat-model.md`. It produces a current-protocol threat model across metadata, routing, capability, authorization, MRTR, caching, registry, and compatibility boundaries.

> 本课产出 `outputs/skill-mcp-threat-model.md`。它按当前协议生成威胁模型，覆盖元数据、路由、能力、授权、MRTR、缓存、注册中心和兼容性八类边界。

## Exercises | 练习题

1. Bind the authenticated principal and current authorization decision to the sealed MRTR state, then reject a retry under a different principal.
   中文翻译：把已认证主体和现行授权决定绑定进密封的 MRTR 状态，然后拒绝换一个主体的重试。
2. Replace the in-memory replay store with a persistent conditional insert and prove two processes cannot both claim one nonce.
   中文翻译：把内存重放存储换成持久化的条件插入，证明两个进程无法同时占用同一个 nonce。
3. Inject a failure after replay claim but before a simulated export. Define and test the transaction or idempotency rule that makes recovery safe.
   中文翻译：在占用重放状态之后、模拟导出之前注入一个故障。定义并测试让恢复安全的事务或幂等规则。
4. Change a tool's `inputSchema` without changing its description. Confirm whole-descriptor pinning catches it.
   中文翻译：只改工具的 `inputSchema` 不改描述。确认整体描述符锁定能抓住它。
5. Add a policy that refuses public caching when `tools/list` differs by principal.
   中文翻译：当 `tools/list` 因主体而异时，添加拒绝公共缓存的策略。
6. Model an older server behind the gateway. Put all handshake and session behavior behind an explicit `2025-11-25` compatibility branch.
   中文翻译：在网关后面建模一台旧服务器。把所有握手与会话行为放进显式的 `2025-11-25` 兼容分支。

## Key Terms | 术语速查表

| Term | Meaning | 中文 |
|------|---------|------|
| Metadata poisoning | Instructions or deceptive claims embedded in a tool descriptor | 元数据投毒：工具描述符中嵌入指令或欺骗性声明 |
| Rug pull | Change to a previously approved descriptor | 地毯拉扯：已批准描述符发生变更 |
| Tool shadowing | Ambiguous routing caused by duplicate unqualified names | 工具影射：未限定重名导致路由歧义 |
| Header mismatch | Routing header and JSON-RPC body disagreement, error `-32020` | 头不匹配：路由头与正文不一致，错误码 `-32020` |
| Hash pin | Digest of the complete approved descriptor | 哈希锁定：完整已批准描述符的摘要 |
| MRTR | Stateless response and retry pattern for server-requested input | 多轮往返请求：服务器请求输入的无状态响应与重试模式 |
| `requestState` | Opaque round-trip value that must be treated as untrusted input | 不透明的往返值，必须视为不可信输入 |
| Capability declaration | Statement of protocol compatibility, not authorization | 能力声明：协议兼容性声明，不是授权 |
| Implicit form support | An empty `elicitation` capability object, equivalent to form support | 隐式表单支持：空 `elicitation` 能力对象，等价于支持表单 |
| Qualified tool name | Stable gateway name such as `notes.search` | 限定工具名：稳定的网关名，如 `notes.search` |

## Further Reading | 延伸阅读

- [MCP security and trust guidance](https://modelcontextprotocol.io/specification/2026-07-28#security-and-trust--safety)
  中文说明：MCP 官方安全与信任指南（2026-07-28 版规范内嵌章节）。
- [Multi Round-Trip Requests](https://modelcontextprotocol.io/specification/2026-07-28/basic/patterns/mrtr)
  中文说明：MRTR 模式规范——本课确认状态防篡改的权威来源。
- [Streamable HTTP transport](https://modelcontextprotocol.io/specification/2026-07-28/basic/transports/streamable-http)
  中文说明：Streamable HTTP 传输规范——路由头与 POST 端点契约。
- [Deprecated features](https://modelcontextprotocol.io/specification/2026-07-28/deprecated)
  中文说明：弃用特性清单——Roots/Sampling/Logging 等旧路径的归宿。
