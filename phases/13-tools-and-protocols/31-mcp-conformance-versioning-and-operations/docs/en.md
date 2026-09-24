# MCP Conformance Engineering: Versioning, Evidence, and Operations | MCP 一致性工程：版本化、证据与运维

> A server is not conformant because its happy path worked through one SDK. Conformance lives at the wire, at version boundaries, through intermediaries, and during rollback.

> **【中文解读】** 一个服务器不会因为"快乐路径在某个 SDK 里跑通了"就算一致（conformant）。一致性活在四个地方：线格式（wire）上、版本边界上、穿过中间设备时、以及回滚过程中。本课是 MCP 2026-07-28 规范系列的收尾课：把规范性规则变成可执行的黄金/负面转录（transcript）语料库，把版本纪元、头部完整性、SDK 归一化差分、代理证据、脱敏、健康窗口与回滚证据全部接进一个发布门（release gate）。

> **【拓展：MCP→质量工程与 SRE】** 这里出现的每个手段——黄金样本与负面测试、降级攻击防护、透传代理差分、发布门与证据化回滚——都是协议工程与 SRE 的经典课题（HTTP/TLS 一致性套件、降级保护、金丝雀发布都是同构问题）。本课的特殊性在于把它们对准 MCP 的具体契约：`resultType` 判别器、镜像路由头、通知不变量、以及 2026-07-28 的自包含元数据。它与 Phase 13 · 29（可靠性）和 Phase 13 · 30（注册中心准入）首尾相接：29 管"出事了怎么活"，30 管"进门前怎么审"，本课管"凭什么说它一直是对的"。

> 🔗 **【前置】** 学本课前请先掌握：Phase 13 · 09（MCP 传输——Streamable HTTP 与头部）、Phase 13 · 17（网关与注册中心——中间设备与镜像头）、Phase 13 · 30（注册中心准入——pin、证据摘要与回滚目标）。

**Type:** Build | **类型:** 动手实践
**Languages:** Python | **语言:** Python
**Prerequisites:** Phase 13 · 09 (transports), Phase 13 · 17 (gateways), Phase 13 · 30 (registry admission) | **前置知识:** Phase 13 · 09（传输）、Phase 13 · 17（网关）、Phase 13 · 30（注册中心准入）
**Time:** ~100 minutes | **时间:** 约 100 分钟

## Learning Objectives | 学习目标

- Turn normative MCP rules into golden and negative wire transcripts.
  中文翻译：把规范性的 MCP 规则变成黄金与负面线格式转录（transcript）。
- Keep strict `2026-07-28` behavior separate from bounded legacy fallback.
  中文翻译：让严格的 `2026-07-28` 行为与有界的旧版回退（legacy fallback）保持分离。
- Distinguish additive unknown fields from an invalid unknown `resultType`.
  中文翻译：区分"增量式未知字段"与"非法的未知 `resultType`"。
- Compare raw JSON-RPC evidence with an SDK-normalized view.
  中文翻译：把原始 JSON-RPC 证据与 SDK 归一化后的视图做差分比较。
- Prove header and body integrity through a real proxy boundary.
  中文翻译：穿过真实的代理边界证明头部与主体的完整性。
- Gate releases with redacted transcript, health, and rollback evidence.
  中文翻译：用脱敏后的转录、健康与回滚证据为发布把关。

## The Problem | 问题引入

> **【中文解读】** "SDK 里调 `tools/list` 拿到了工具、集成测试绿了"——这个结果回答不了真正的问题：请求带没带现代的逐请求元数据？头部与 JSON-RPC 主体一致吗？`resultType` 是线上真实存在的还是 SDK 合成的？未来新增字段会被保留吗？一个现代错误会不会意外触发旧版握手？代理保住了源站状态码和错误吗？通知序列化器有没有吐出被禁止的响应？运维能不能不存 secret 就证明一次发布或回滚的理由？一致性就是一组可观察的不变量——在生产流量替你发现问题之前，先造一个能捕获这些不变量的测试架（harness）。

Your client calls `tools/list` through an SDK and gets tools. The integration test passes.

> 你的客户端通过 SDK 调用 `tools/list` 并拿到了工具，集成测试通过了。

That result leaves important questions unanswered:

> 这个结果留下了许多没有回答的重要问题：

- Did the request carry modern per-request protocol metadata?
- Did `MCP-Protocol-Version`, `Mcp-Method`, and `Mcp-Name` match the JSON-RPC body?
- Did the response contain a valid `resultType` on the wire, or did the SDK synthesize one?
- Would the client preserve a future additive field?
- Would a recognized modern error accidentally trigger a legacy handshake?
- Did a proxy preserve the origin status and JSON-RPC error?
- Did the notification serializer emit a forbidden response?
- Can operations prove why a release was promoted or rolled back without storing secrets?

Conformance is a set of observable invariants. Build a harness that captures those invariants before production traffic has to discover them.

> 一致性是一组可观察的不变量。在生产流量不得不发现它们之前，先构建一个能捕获这些不变量的测试架。

```figure
mcp-conformance-operations
```

## Start With Version Eras | 从版本纪元开始

> **【中文解读】** 两个纪元两套规则，绝不做"一个宽松验证器同时吃两种形态"。现代纪元（`2026-07-28`）：自包含的逐请求元数据——`params._meta.io.modelcontextprotocol/protocolVersion` 与 `.../clientCapabilities`，裸的 `protocolVersion` 别名是畸形的；镜像路由头在场时必须与 JSON-RPC 主体一致；成功结果带 `resultType`。旧纪元（截至 `2025-11-25`）：早期初始化时代，客户端选定旧纪元之后，没有 `resultType` 的结果才被解释为 complete。分开的分支防止"畸形的现代对端反而获得更弱的验证"。严格模式要求现代行为的正面证明（成功的 `server/discover` 或被识别的现代错误），绝不因 `-32020/-32021/-32022` 降级；回退模式先做一次有界现代探测，超时/空响应/断连只是"无结论"、不证明旧版，只有显式 allowlist 的端点才可做有界旧版探测，且必须验证其 `initialize` 结果后才选定旧分支。把选定的纪元记录在每条转录旁边。

> 💡 **【类比】** 版本纪元像充电口的"全程 USB-C"与"备用转接头"。默认只走 USB-C（严格模式）；转接头（旧版回退）只给登记在白名单里的老设备用，而且要先确认那台设备真的是老设备（合法的 legacy `initialize` 证据）——不能因为"新线没插上"（超时/无响应）就默认对方是老设备。否则一个干扰你的中间人就能靠"弄丢现代响应"把整个连接拖回旧协议，这正是降级攻击（downgrade attack）的套路。

MCP `2026-07-28` uses self-contained per-request metadata. A modern request carries `params._meta.io.modelcontextprotocol/protocolVersion` and `params._meta.io.modelcontextprotocol/clientCapabilities`. The exact namespaced keys matter; bare `protocolVersion` or `clientCapabilities` aliases are malformed. When mirrored routing headers are present at the HTTP boundary, their values must agree with the JSON-RPC body. Modern successful results carry `resultType`.

> MCP `2026-07-28` 使用自包含的逐请求元数据。现代请求携带 `params._meta.io.modelcontextprotocol/protocolVersion` 和 `params._meta.io.modelcontextprotocol/clientCapabilities`。精确的命名空间键很重要：裸的 `protocolVersion` 或 `clientCapabilities` 别名是畸形的。镜像路由头出现在 HTTP 边界时，其值必须与 JSON-RPC 主体一致。现代成功结果携带 `resultType`。

Versions through `2025-11-25` use the earlier initialization era. A legacy result without `resultType` is interpreted as complete only after the client has selected that earlier era.

> 截至 `2025-11-25` 的版本使用更早的初始化纪元。一个没有 `resultType` 的旧版结果，只有在客户端已经选定那个更早纪元之后，才会被解释为 complete。

Do not create one permissive validator that accepts both shapes at once. Use two branches:

> 不要做一个"同时接受两种形态"的宽松验证器。用两个分支：

| Branch | Entry evidence | Missing `resultType` | Initialization |
|---|---|---|---|
| Modern | Successful `server/discover` or recognized modern response | Invalid | Not the default path |
| Legacy | Configured allowlist plus a valid legacy `initialize` result after an inconclusive modern probe | Interpreted as complete | Required by that era |

> 分支表：现代分支的入口证据是成功的 `server/discover` 或被识别的现代响应，缺失 `resultType` 视为非法，初始化不是默认路径；旧版分支的入口证据是"已配置的 allowlist + 一次无结论的现代探测之后有效的旧版 `initialize` 结果"，缺失 `resultType` 被解释为 complete，初始化是该纪元必需的。

The separation prevents a malformed modern peer from being rewarded with weaker validation.

> 这种分离防止一个畸形的现代对端反而获得更弱的验证。

### Strict mode | 严格模式

Strict mode requires proof of modern behavior. A successful `server/discover` proves the modern branch. A recognized modern JSON-RPC error also proves it. Correct the request or stop. Never downgrade because the server returned `-32020`, `-32021`, or `-32022`.

> 严格模式要求现代行为的正面证明：一次成功的 `server/discover` 证明现代分支，一个被识别的现代 JSON-RPC 错误同样证明它。修正请求或直接停止——绝不因为服务器返回 `-32020`、`-32021` 或 `-32022` 而降级。

### Fallback mode | 回退模式

Fallback mode performs one bounded modern probe. A timeout, empty reply, closed connection, or unrecognized response is inconclusive. It does not prove that the peer is legacy. Only an endpoint explicitly configured or allowlisted for compatibility may then receive a bounded legacy probe, and the client selects the legacy branch only after validating that probe's `initialize` result and negotiated legacy revision.

> 回退模式先做一次有界的现代探测。超时、空响应、断连或无法识别的响应都是"无结论"——它们不证明对端是旧版。只有被显式配置或列入兼容 allowlist 的端点，才可以接收一次有界的旧版探测；而且客户端只有在验证了那次探测的 `initialize` 结果与协商出的旧版修订之后，才选定旧分支。

Fallback is not “try legacy after any error.” A recognized modern error contains useful correction information. Downgrading after it can hide a header mismatch, missing capability declaration, or unsupported version.

> 回退不是"任何错误之后都试试旧版"。一个被识别的现代错误携带有用的修正信息；在它之后降级，可能掩盖头部不匹配、能力声明缺失或版本不受支持。

This prevents an attacker, outage, or filtering proxy from forcing downgrade by dropping the modern response. Record the endpoint policy, inconclusive modern observation, exact positive legacy evidence, and selected era together.

> 这防止攻击者、故障或过滤型代理靠"弄丢现代响应"强迫降级。要把端点策略、无结论的现代观察、确切的旧版正面证据和选定的纪元记录在一起。

Record the selected era beside every transcript. Without that fact, a missing field can look acceptable in one test run and invalid in another.

> 把选定的纪元记录在每条转录旁边。没有这个事实，同一个缺失字段可能这一次测试运行看着合法、下一次就变成非法。

## Build a Transcript Corpus | 构建转录语料库

> **【中文解读】** 转录（transcript）fixture 记录的是"真实跨过了边界的东西"——头部、请求体、响应状态码、响应体、选定纪元——而不只是"SDK 调用返回了什么"。语料库分两类：黄金转录证明"接受的行为"（元数据与头部匹配、`resultType` 合法、通知无响应等）；负面转录证明"拒绝的行为"（头部与主体不匹配、未知判别器、代理吞错误等）。每条负面用例都要断言拒绝边界和稳定错误码——"调用失败了"太弱，代理造的 500 和源站的 `-32020` 都叫失败，但讲给运维的故事完全不同。

A transcript fixture records what crossed the boundary, not only the SDK call:

> 一条转录 fixture 记录的是跨过边界的内容，而不只是那次 SDK 调用：

```json
{
  "name": "golden-modern-list",
  "era": "modern",
  "headers": {
    "MCP-Protocol-Version": "2026-07-28",
    "Mcp-Method": "tools/list"
  },
  "request": {
    "jsonrpc": "2.0",
    "id": 1,
    "method": "tools/list",
    "params": {
      "_meta": {
        "io.modelcontextprotocol/protocolVersion": "2026-07-28",
        "io.modelcontextprotocol/clientCapabilities": {}
      }
    }
  },
  "responseStatus": 200,
  "responseBody": {
    "jsonrpc": "2.0",
    "id": 1,
    "result": {
      "resultType": "complete",
      "tools": []
    }
  }
}
```

Keep two classes of fixtures.

> 保留两类 fixture。

### Golden transcripts | 黄金转录

Golden transcripts prove accepted behavior:

> 黄金转录证明"被接受的行为"：

A golden transcript is precise, not large. Keep volatile IDs and timestamps deterministic or normalize them before comparison.

> 黄金转录要精确，不要庞大。把易变的 ID 与时间戳做成确定性的，或在比较前先规范化。

- modern discovery or method request with matching metadata and headers
- complete result with required fields
- `input_required` result when the method can request more input
- extension result only after the corresponding capability was advertised
- legacy result without `resultType`, but only in the selected legacy era
- notification processing with no JSON-RPC response

A golden transcript is precise, not large. Keep volatile IDs and timestamps deterministic or normalize them before comparison.

### Negative transcripts | 负面转录

Negative transcripts prove refusal behavior:

> 负面转录证明"被拒绝的行为"：

- header and body mismatch
- missing per-request capabilities
- unsupported matched protocol version
- missing modern `resultType`
- unknown or unadvertised `resultType`
- response `jsonrpc` other than `2.0` or an ID that differs in value or JSON type
- a response containing both `result` and `error`, or neither one
- an error without an integer `code` and string `message`
- a known protocol error mapped to the wrong HTTP status
- response emitted for a notification
- malformed JSON-RPC envelope
- proxy collapse of a protocol error

For each negative case, assert the rejection boundary and stable error code. “The call failed” is too weak. A proxy-generated 500 and an origin `-32020` can both look like failure while telling operators completely different stories.

> 对每条负面用例，断言拒绝边界和稳定的错误码。"调用失败了"太弱——代理生成的 500 与源站的 `-32020` 看起来都像失败，但它们讲给运维的故事完全不同。

The header-mismatch fixture must include the server's actual HTTP 400 JSON-RPC response with the matching request ID and error code `-32020`. Enforce that automatically whenever the local validator observes `HeaderMismatch`; do not make response verification an optional fixture flag. A case with HTTP 500 and no body fails even when the local rejection code was correct. A harness that stops after its own request validator throws has tested only itself, not the server's wire behavior.

> 头部不匹配的 fixture 必须包含服务器真实的 HTTP 400 JSON-RPC 响应——带匹配的请求 ID 和错误码 `-32020`。只要本地验证器观察到 `HeaderMismatch`，就自动强制这一点；不要把响应校验做成可选的 fixture 开关。一个"HTTP 500 且无响应体"的用例，即使本地拒绝码是对的也算失败。一个在自己的请求验证器抛出异常之后就停下的测试架，只测试了它自己，没有测试服务器的线上行为。

The official MCP conformance project is useful as an external suite and versioned reference. Keep your local transcripts too. They capture your proxy, SDK, authentication, extensions, and release path, which a general suite cannot know.

> 官方 MCP 一致性项目适合作为外部套件和带版本的参照。但本地的转录也要保留：它们捕获的是你的代理、SDK、认证、扩展与发布路径——这些是一般性套件不可能知道的。

## Header Values Must Match the RPC Body | 头部值必须与 RPC 主体一致

> **【中文解读】** 现代 Streamable HTTP 允许中间设备用镜像头部做路由或策略执行，但 JSON-RPC 主体才是协议的事实来源——不匹配是完整性故障，不是"二选一挑一个"的提示。验证顺序：先解析校验 JSON-RPC 信封与元数据类型，再比对 `MCP-Protocol-Version` 与主体里的命名空间键、`Mcp-Method` 与 `method`、有路由名时比对 `Mcp-Name`，相等确立之后才判断版本与能力是否受支持。这个顺序把"不匹配 `-32020`"与"版本不受支持 `-32022`"区分开，也挡住了"网关按头部名字授权、源站按另一个主体名字执行"的攻击。HTTP 字段名大小写不敏感而值大小写敏感；`Mcp-Name` 含不安全字符时走 Base64 UTF-8 哨兵解码，解码失败或首尾空白都以 `-32020` 拒绝。

In modern Streamable HTTP, intermediaries can route or enforce policy using mirrored headers. The JSON-RPC body remains the protocol source of truth. A mismatch is an integrity failure, not a hint to choose one value.

> 在现代 Streamable HTTP 中，中间设备可以用镜像头部做路由或执行策略，但 JSON-RPC 主体仍是协议的事实来源。不匹配是完整性故障，不是"提示你挑一个值"。

Validate in this order:

> 按以下顺序验证：

1. Parse and validate the JSON-RPC envelope and metadata types.
2. Compare `MCP-Protocol-Version` with `params._meta.io.modelcontextprotocol/protocolVersion`.
3. Compare `Mcp-Method` with `method`.
4. When the method has a routing name, compare `Mcp-Name` with the corresponding body value.
5. After equality is established, decide whether the matched version and capability set are supported.

This order distinguishes mismatch `-32020` from unsupported version `-32022`. It also stops a gateway from authorizing the header name while the origin executes a different body name.

> 这个顺序把不匹配 `-32020` 与版本不受支持 `-32022` 区分开，也阻止了"网关按头部名字授权、而源站执行另一个主体名字"的情况。

HTTP field names are case-insensitive, while their values remain case-sensitive. Normalize header names before lookup and reject conflicting duplicates. For an unsafe, non-ASCII, or leading-or-trailing-whitespace `Mcp-Name`, decode the exact `=?base64?{Base64EncodedValue}?=` UTF-8 sentinel before comparing it with the body. Reject an incomplete sentinel, invalid Base64, invalid UTF-8, or raw unsafe value with `-32020`. Raw surrounding whitespace is invalid even when the body contains the same characters because that value required sentinel encoding before transport.

An intermediary can reject malformed HTTP before a request reaches the MCP server, so its failure may be an HTTP error without JSON-RPC. Capture whether a rejection came from the intermediary or origin. The origin MCP server should use the protocol error contract when it handled a valid JSON-RPC request.

## Unknown Fields Are Not Unknown Results | 未知字段不等于未知结果

> **【中文解读】** 前向兼容需要两条不同的规则。增量式未知字段：result 对象和 `_meta` 映射可以新增字段——透明代理通常应保留（转发），应用客户端可以忽略，但要靠差分测试让"SDK 丢掉了它"变成一个显式、有意的决定。未知的 `resultType`：它是生命周期判别器，未知或未声明的判别器不能安全地当作 complete——客户端不知道自己会丢弃怎样的生命周期，必须拒绝。同一份原始响应可以同时包含"可接受的未知字段"和"不可接受的未知结果类型"，两种情况都要测。判别器只是第一层，之后还要校验方法特定的载荷：`tools/list` 需要 tools 数组且描述符合法，`task` 结果需要 `taskId`/状态/时间戳/`ttlMs`，completion 结果需要合法的 `completion` 对象。

Forward compatibility requires two different rules.

> 前向兼容需要两条不同的规则。

### Additive unknown fields | 增量式未知字段

Result objects and `_meta` maps can gain fields. A validator should preserve or ignore an additive field according to its role, unless the field violates a reserved contract. The sample keeps the full raw result in evidence and accepts `futureHint` beside a known result.

> result 对象与 `_meta` 映射可以新增字段。验证器应根据自身角色保留或忽略增量字段，除非该字段违反了保留契约。示例把完整原始结果留在证据里，并接受已知结果旁边的 `futureHint`。

If you are a transparent proxy, preserving an unknown field is usually safer than stripping it. If you are an application client, ignoring it can be valid. Your differential test should still reveal that the SDK omitted it so the behavior is deliberate.

> 如果你是透明代理，保留未知字段通常比剥掉它更安全；如果你是应用客户端，忽略它可以合法。但差分测试仍应揭示"SDK 略过了它"，让这个行为成为有意为之。

### Unknown `resultType` | 未知的 resultType

`resultType` is a discriminator. Core modern results use `complete` or `input_required`. An extension can add another value only when its capability was advertised. The Tasks extension, for example, can add `task` in that negotiated capability context.

> `resultType` 是一个判别器。核心现代结果使用 `complete` 或 `input_required`；扩展只有在对应能力已被声明的情况下才能新增别的值——例如 Tasks 扩展在协商出的能力上下文里可以新增 `task`。

An unknown or unadvertised discriminator cannot be safely treated as complete. The client does not know the lifecycle it would be discarding. Reject it.

> 未知或未声明的判别器不能被安全地当作 complete。客户端不知道自己将丢弃怎样的生命周期。拒绝它。

The same raw response can therefore contain an acceptable unknown field and an unacceptable unknown result type. Test both cases.

> 因此，同一份原始响应可以既包含可接受的未知字段、又包含不可接受的未知结果类型。两种情况都要测。

The discriminator is only the first layer. Validate the method-specific payload after it. A complete `tools/list` result needs a `tools` array whose descriptors have unique non-empty names, useful descriptions, and object-root `inputSchema` values. A `task` result is valid only for an eligible `tools/call` with the Tasks capability and requires `taskId`, known status, creation and update timestamps, and `ttlMs`, plus a valid optional polling interval. A complete `completion/complete` result requires a `completion` object with no more than 100 string values, an optional non-negative integer `total` that is not smaller than the returned values, and an optional Boolean `hasMore`. A well-spelled `resultType` cannot make a malformed payload conformant.

> 判别器只是第一层，其后还要校验方法特定的载荷：complete 的 `tools/list` 结果需要 `tools` 数组，描述符要有唯一非空名字、有用的描述和对象根的 `inputSchema`；`task` 结果只有在带 Tasks 能力的合规 `tools/call` 里才合法，需要 `taskId`、已知状态、创建与更新时间戳和 `ttlMs`，外加合法的可选轮询间隔；complete 的 `completion/complete` 结果需要 `completion` 对象——字符串值不超过 100 个、可选的非负整数 `total` 不得小于返回值数量、可选的布尔 `hasMore`。拼写正确的 `resultType` 救不了畸形的载荷。

## The Notification Invariant | 通知不变量

A JSON-RPC notification has no `id`. The receiver must not send a JSON-RPC success or error response.

> 一条 JSON-RPC 通知没有 `id`。接收方不得发送 JSON-RPC 成功或错误响应。

For an accepted HTTP notification shape, the harness expects an HTTP `202` with an empty body. MCP `2026-07-28` defines no core client-to-server notifications over Streamable HTTP. The sample uses a namespaced course extension notification only to test the one-way serializer invariant. Do not present it as a new core method.

> 对被接受的 HTTP 通知形态，测试架期望 HTTP `202` 和空主体。MCP `2026-07-28` 没有定义核心的客户端到服务器 Streamable HTTP 通知。示例使用一个命名空间的课程扩展通知，只为测试单向序列化器不变量；不要把它当成新的核心方法。

Test the serializer, not only the handler. A handler may return `None` while middleware wraps it in a JSON success object. Capture the final egress bytes.

> 测序列化器，而不只是处理器。处理器可能返回 `None`，而中间件把它包成一个 JSON 成功对象。捕获最终的出口字节。

## Add an SDK Differential | 增加 SDK 差分

> **【中文解读】** SDK 常把线上对象转成方便的语言类型，这有用，但归一化后的对象证明不了"收到的是什么"。对每条高风险 fixture 抓四样东西：SDK 解码前的原始状态、头部、响应体；SDK 归一化的返回值或异常；选定纪元的期望语义投影；SDK 抬升、合成、剥除或改变了的字段。示例允许 SDK 专门移除已知的线上簿记字段（`resultType`、`_meta`、`ttlMs`、`cacheScope`）并同时比较应用载荷，但 `futureHint` 被丢弃要如实报告——那个未知语义字段消失了。差分要对每个在产的 SDK 与版本运行：两个 SDK 对同一转录归一化得不一样时，发布策略应写明哪种行为可接受，而不是事后挑最顺手的输出。

SDKs often turn wire objects into convenient language types. That is useful, but a normalized object cannot prove what was received.

> SDK 常把线上对象转成方便的语言类型。这很有用，但一个归一化的对象证明不了实际收到了什么。

For every high-risk fixture, capture:

1. Raw status, headers, and response body before SDK decoding.
2. SDK-normalized return value or exception.
3. The expected semantic projection for the selected era.
4. Fields lifted, synthesized, stripped, or changed by the SDK.

The sample permits SDK-only removal of known wire bookkeeping such as `resultType`, `_meta`, `ttlMs`, and `cacheScope` while comparing the application payload. It reports a dropped `futureHint` because that unknown semantic field disappeared.

Do not assume every difference is an SDK bug. The point is to make the transformation visible. Decide whether your component is an application endpoint, which may ignore an additive field, or a transparent intermediary, which should preserve it.

> 不要假设每一处差异都是 SDK bug。差分的意义是让转换可见。先想清楚你的组件是"可以忽略增量字段的应用端点"，还是"应当保留它的透明中间人"。

Run the differential against every SDK and version you ship. If two SDKs normalize the same transcript differently, release policy should say which behavior is acceptable rather than choosing the most convenient output after the fact.

> 对你发布的每一个 SDK 与版本运行差分。如果两个 SDK 对同一转录的归一化不同，发布策略应当写明哪种行为可接受，而不是事后挑最顺手的输出。

## Capture Proxy Evidence | 捕获代理证据

Most production MCP failures occur across more than one process. Record three views:

> 大多数生产 MCP 故障跨越不止一个进程。记录三个视角：

| View | Minimum evidence |
|---|---|
| Ingress | request headers, JSON-RPC body, content type, authenticated route, receive time |
| Origin | forwarded headers and body digest, origin status, response headers and body |
| Egress | client-visible status, headers, body, and send time |

> 三个视角表：入口（Ingress）至少记请求头部、JSON-RPC 主体、内容类型、已认证路由与接收时间；源站（Origin）至少记转发头部与主体摘要、源站状态码、响应头部与主体；出口（Egress）至少记客户端可见的状态码、头部、主体与发送时间。

The sample detects two common transformations:

> 示例检测两类常见变换：

- an origin HTTP 400 or 404 JSON-RPC error becomes a generic proxy 500
- the egress JSON-RPC body differs from the origin body

> 两类变换：源站的 HTTP 400 或 404 JSON-RPC 错误变成代理的通用 500；出口 JSON-RPC 主体与源站主体不一致。

Add deployment-specific assertions for content type, `Accept`, compression, request-scoped SSE, cache headers, and trace correlation. Capture both sides of TLS termination when policy permits. Never log credentials just to prove the path.

> 再为内容类型、`Accept`、压缩、请求级 SSE、缓存头和 trace 关联加上部署特定的断言。策略允许时捕获 TLS 终止的两侧。绝不要为了证明路径而记录凭证。

## Redact Before Evidence Leaves Memory | 证据离开内存前先脱敏

> **【中文解读】** 脱敏是一致性运维的一部分，不是事后的清理工作——在序列化、哈希、日志、测试工件或失败上传之前完成。示例把键名做小写折叠并去掉分隔符后再匹配，然后递归替换 `Authorization`、`Cookie`、`accessToken`、`clientSecret`、`token`、`password`、`secret`、`api_key` 等键下的值；规范化与 denylist 必须用同一种形态，防止 camelCase、连字符、下划线、点号变体互相绕过。生产采集器还应加方法特定的参数策略——像 `query` 这种无害的键也可能装着个人或受监管数据。对脱敏后的证据包做哈希：摘要证明是哪一份脱敏包驱动了决策，却不会泄露被移除的值；原始抓包只在特定调查需要时留在受批准的短生命周期系统里。

Redaction is part of conformance operations, not a later cleanup job. Apply it before serialization, hashing, logs, test artifacts, or failure uploads.

> 脱敏是一致性运维的一部分，不是之后的清理工作。在序列化、哈希、日志、测试工件或失败上传之前完成它。

The sample case-folds key names and removes separators before matching, then recursively replaces values under keys such as `Authorization`, `Cookie`, `Set-Cookie`, `X-Api-Key`, `accessToken`, `clientSecret`, `registrationAccessToken`, `token`, `password`, `secret`, and `api_key`. Canonicalization and the denylist must use the same form so camelCase, hyphenated, underscored, and dotted variants cannot bypass one another's policy. A production collector should add method-specific argument policy, because a harmless key like `query` can still contain personal or regulated data.

> 示例先把键名做大小写折叠并移除分隔符再匹配，然后递归替换 `Authorization`、`Cookie`、`Set-Cookie`、`X-Api-Key`、`accessToken`、`clientSecret`、`registrationAccessToken`、`token`、`password`、`secret`、`api_key` 等键下的值。规范化与 denylist 必须使用同一种形态，这样 camelCase、连字符、下划线和点号变体就无法互相绕过对方的策略。生产采集器还应增加方法特定的参数策略，因为像 `query` 这样无害的键仍可能携带个人或受监管数据。

Hash the redacted evidence bundle. Keep raw captures only in an approved short-lived system when a specific investigation requires them. A digest proves which redacted bundle drove the decision; it does not reveal the removed value.

> 对脱敏后的证据包做哈希。只有特定调查确实需要时，才把原始抓包保留在受批准的短生命周期系统里。摘要证明的是哪一份脱敏包驱动了决策；它不会泄露被移除的值。

## Make Health and Rollback Part of the Gate | 把健康与回滚纳入发布门

> **【中文解读】** 协议一致是发布的必要条件，不是充分条件——一个完全一致的候选版本仍可能超时、泄漏内存或压垮依赖。发布前先定义健康窗口（最小样本数、最大错误率、最大延迟分位、饱和或资源上限、观察时长、与已准入基线的比较）；同样在发布前定义回滚证据（精确的先前版本、准入证据摘要、SHA-256 制品与描述符 pin、当前 Registry 状态、当前健康结果、路由恢复程序、以及可信发布控制器身份对以上字段的一次认证）。回滚目标要在晋升之前就完成验证并且健康——不是等候选版本失败之后才补。候选失败而回滚目标缺证据时，宁可保持流量不动，也不要猜。不要把就绪检查退化成真值判断（非空版本号、`healthy: "yes"`、任意证据字符串）：示例要求精确类型、active 状态、三个 SHA-256 摘要、可信签名者和对完整回滚载荷的有效 HMAC-SHA-256 认证；demo 用的确定性密钥是非机密 fixture，生产要在发布边界注入受保护的密钥、KMS 验证结果或公钥认证验证器。发布门还拒绝空的转录、SDK 差分或代理证据——每个来源都必须携带有效证据摘要，绿了的健康窗口填不上一个从未观察过的边界。

Protocol conformance is necessary but not sufficient for release. A conformant candidate can still time out, leak memory, or overload a dependency.

> 协议一致是发布的必要条件而非充分条件。一个一致的候选版本仍可能超时、泄漏内存或压垮某个依赖。

Define a health window before rollout:

> 发布之前先定义健康窗口：

- minimum sample count
- maximum error rate
- maximum latency percentile
- saturation or resource limits
- observation duration
- comparison with the admitted baseline

Define rollback evidence before rollout too:

> 发布之前同样定义回滚证据：

- exact prior version
- admission evidence digest
- SHA-256 artifact and descriptor pins
- current Registry status
- current health result
- route restoration procedure
- an attestation over those exact fields from a trusted release-controller identity

Require that rollback target to be verified and healthy before promotion, not only after the candidate fails. A successful release without a usable recovery path is not production-ready.

> 要求回滚目标在晋升之前就完成验证并且健康，而不是只等候选失败之后才查。一次没有可用恢复路径的成功发布并不算生产就绪。

If a candidate fails and the rollback target lacks that evidence, hold traffic instead of guessing. “Roll back to whatever was there” is not an operational control.

> 如果候选失败而回滚目标缺少证据，那就稳住流量，不要去猜。"回到之前随便哪个版本"不是一种运维控制。

Do not reduce readiness to truthiness checks such as a non-empty version, `healthy: "yes"`, or an arbitrary evidence string. The sample requires exact types, an active status, three SHA-256 digests, a trusted signer, and a valid HMAC-SHA-256 attestation over the complete rollback payload. Its deterministic demo key is a non-secret fixture. Inject a protected key, KMS verification result, or public-key attestation verifier at the release boundary in production.

> 不要把就绪检查退化成真值判断——比如非空的版本号、`healthy: "yes"` 或任意的证据字符串。示例要求精确类型、active 状态、三个 SHA-256 摘要、可信签名者，以及对完整回滚载荷的有效 HMAC-SHA-256 认证。它确定性的 demo 密钥是非机密 fixture；生产中要在发布边界注入受保护的密钥、KMS 验证结果或公钥认证验证器。

The release gate also refuses empty transcript, SDK differential, or proxy evidence. Each source must carry valid evidence digests. A green health window cannot fill in a boundary that was never observed.

> 发布门还拒绝空的转录、SDK 差分或代理证据：每个来源都必须携带有效的证据摘要。一个绿了的健康窗口，填不上一个从未被观察过的边界。

## Build It | 动手实现

Run the standard-library harness:

> 运行标准库测试架：

```bash
cd phases/13-tools-and-protocols/31-mcp-conformance-versioning-and-operations
python3 code/main.py
```

The demo runs exactly fifteen golden and negative transcripts, including valid and malformed completion results, compares a raw result with an SDK view, inspects a proxy that collapsed an origin error, evaluates health, authenticates the rollback evidence, and selects that target.

> demo 恰好运行十五条黄金与负面转录（含合法与畸形的 completion 结果），把原始结果与 SDK 视图做比较，检视一个吞掉了源站错误的代理，评估健康，认证回滚证据，并选中该目标。

Expected shape:

> 预期输出形状：

```json
{
  "transcriptsPassed": 15,
  "transcriptsTotal": 15,
  "sdkDroppedFields": ["futureHint"],
  "proxyIssues": [
    "proxy collapsed a protocol error into HTTP 500",
    "proxy changed the origin JSON-RPC body"
  ],
  "releaseAction": "rollback",
  "evidenceDigest": "..."
}
```

Read `code/main.py` in this order:

> 按以下顺序阅读 `code/main.py`：

1. `validate_request()` enforces era-specific request and header rules.
2. `validate_result()` separates missing legacy discriminators, valid modern values, extensions, and unknown values.
3. `select_era()` implements strict and bounded fallback policy.
4. `run_transcript()` evaluates golden and negative fixtures.
5. `compare_sdk_view()` exposes normalization differences.
6. `inspect_proxy()` compares ingress, origin, and egress evidence.
7. `redact()` removes obvious secrets before evidence hashing.
8. `rollback_evidence_ready()` validates exact pin fields and the trusted release attestation.
9. `ReleaseGate.evaluate()` joins non-empty conformance, SDK, proxy, health, and rollback evidence.

## Use It | 用框架实现

Run the harness at four points:

> 在四个时间点运行测试架：

1. On every implementation change with an in-process test adapter.
2. Against the built client and server binaries over the real transport.
3. Through the deployed proxy or gateway in a staging environment.
4. During canary rollout with live health and rollback evidence.

Keep the same stable case names across layers. `negative-header-body-mismatch` should mean the same invariant in unit, end-to-end, proxy, and canary reports. The evidence digest will differ because the boundary changed; the requirement should not.

> 在各层之间保持相同的稳定用例名：`negative-header-body-mismatch` 在单元、端到端、代理和金丝雀报告里必须指同一个不变量。证据摘要会不同——因为边界变了；但要求不能变。

Store fixture schemas in version control. Store redacted run evidence in your release system. Store short-lived raw captures only under incident access controls.

> fixture schema 存进版本控制；脱敏后的运行证据存进发布系统；短生命周期的原始抓包只放在事件访问控制之下。

> 四个运行点对应四层边界：进程内实现改动、真实传输上的成品二进制、staging 里的代理或网关、带真实健康与回滚证据的金丝雀。测试架本身可以复用，变的是它观察的边界——这正是"同一不变量、不同证据摘要"的含义。

## Interactive Lab | 交互实验

### Lab A: prove the era boundary | 实验 A：证明纪元边界

From the `code` directory, open Python:

> 从 `code` 目录打开 Python：

```bash
cd phases/13-tools-and-protocols/31-mcp-conformance-versioning-and-operations/code
python3 -q
```

Run:

```python
from main import *
validate_result({"tools": []}, "legacy")
validate_result({"tools": []}, "modern")
```

The legacy call infers `complete`. The modern call raises `ProtocolViolation`. Now test fallback:

> 旧版调用推断出 `complete`；现代调用抛出 `ProtocolViolation`。接着测回退：

```python
select_era({"kind": "timeout"}, "fallback")
select_era(
    {"kind": "timeout"},
    "fallback",
    legacy_allowed=True,
    legacy_evidence={"kind": "initialize_success", "protocolVersion": LEGACY_VERSION},
)
select_era({"kind": "jsonrpc_error", "code": -32021}, "fallback")
```

The first timeout fails closed because silence is not legacy evidence. The second call selects legacy only because configuration allows it and a valid legacy initialization result was observed. The recognized missing-capability error proves the modern branch.

> 第一个超时失败闭合（fail closed），因为沉默不是旧版证据。第二个调用之所以能选定旧版，只是因为配置允许、且观察到了一个有效的旧版初始化结果。而被识别的"能力缺失"错误证明的是现代分支。

### Lab B: additive field versus discriminator | 实验 B：增量字段与判别器

```python
validate_result({"resultType": "complete", "tools": [], "futureHint": True}, "modern")
validate_result({"resultType": "future_mode", "tools": []}, "modern")
```

The first result preserves `futureHint`. The second is rejected because the lifecycle discriminator is unknown.

> 第一个结果保留了 `futureHint`；第二个被拒绝，因为生命周期判别器是未知的。

### Lab C: inspect an SDK transformation | 实验 C：检视 SDK 转换

```python
compare_sdk_view(
    {"resultType": "complete", "tools": [], "futureHint": {"mode": "new"}},
    {"tools": []},
)
```

Decide whether your component may ignore `futureHint` or must forward it. Write that choice into release policy. Do not silently erase the differential.

> 决定你的组件可以忽略 `futureHint`，还是必须转发它。把这个选择写进发布策略，不要悄悄抹掉差分结果。

### Lab D: repair the proxy | 实验 D：修复代理

Modify the demo exchange so egress preserves the origin status and body. Run `python3 main.py` again. The proxy issues should disappear, but the SDK differential still blocks promotion. Then include `futureHint` in the SDK view and observe the action change to `promote` when every evidence source passes.

> 修改 demo 交换，让出口保留源站状态码与主体。再跑一次 `python3 main.py`：代理问题应该消失，但 SDK 差分仍然挡住晋升。然后把 `futureHint` 加进 SDK 视图，观察当每个证据来源都通过时，动作变成 `promote`。

## Practice Lab | 进阶练习

Add request-scoped SSE transcripts to the harness.

> 给测试架增加请求级 SSE 转录。

> 进阶练习把语料库从"一请求一响应"扩展到"一请求一流"：捕获响应状态、内容类型、有序 SSE 事件与流终止；证明每个 JSON-RPC 事件都有合法的纪元特定结果或错误；加"代理把整个流缓冲完再转发"和"SSE 事件的 JSON-RPC id 与请求不符"两个负面用例；写证据前先脱敏事件数据；把流时长、首事件延迟和事件计数纳入健康窗口；流失败时发布门只选有证据的回滚目标。成功标准是同一条用例既能直连跑、也能穿代理跑，报告能精确指出改变行为的那一层边界。

Requirements:

- Capture response status, content type, ordered SSE events, and stream termination.
- Prove each JSON-RPC event has a valid era-specific result or error.
- Add a negative case for a proxy that buffers the full stream before forwarding.
- Add a negative case for an SSE event whose JSON-RPC id differs from the request.
- Redact event data before writing evidence.
- Include stream duration, first-event latency, and event count in the health window.
- Make the release gate choose only an evidenced rollback target when the stream fails.

Success means the same case runs directly and through the proxy, with a report that identifies the exact boundary that changed behavior.

> 成功的标准：同一条用例既能直连运行也能穿代理运行，报告能指出改变行为的精确边界。

## Shipped Artifact | 产出物

This lesson ships `outputs/skill-mcp-conformance-release-gate.md`. Use it to turn a server, client, gateway, or SDK change into a versioned conformance matrix and release decision. The artifact requires raw wire evidence, negative cases, explicit era selection, SDK differentials, proxy proof, redaction, health thresholds, and rollback evidence.

> 本课附带 `outputs/skill-mcp-conformance-release-gate.md`。用它把一次服务器、客户端、网关或 SDK 的变更，变成一份带版本的一致性矩阵和发布决策。该工件要求原始线上证据、负面用例、显式纪元选择、SDK 差分、代理证明、脱敏、健康阈值与回滚证据。

## Verify It | 验证

> **【中文解读】** 验收清单逐条过：所有黄金与负面转录都到达预期结局；现代请求要求精确的命名空间元数据键；HTTP 头部名大小写不敏感地匹配、编码的 `Mcp-Name` 值被精确解码；头部与主体不匹配返回现代不匹配码；响应版本、ID、result/error 互斥、错误形态与 HTTP 映射都被校验；方法特定的 tool-list/task/completion 载荷要求被执行；每个观察到的 `HeaderMismatch` 都要求真实的 HTTP 400 JSON-RPC `-32020` 响应；原始 `Mcp-Name` 空白被拒绝而哨兵编码的空白精确往返；缺失 `resultType` 只在选定的旧纪元合法；增量字段活着而未知结果类型失败；扩展结果类型要求其能力已声明；被识别的现代错误绝不触发旧版回退；通知不产生 JSON-RPC 响应；SDK 簿记移除与语义字段丢失被区分；代理错误坍缩被检测、凭证在 camelCase 与分隔符变体上被递归脱敏；晋升要求非空的转录、SDK、代理与健康运维证据；晋升与回滚都要求一个已认证、已 pin、active、健康的回滚目标。

Run the demo and deterministic suite:

> 运行 demo 与确定性测试套件：

```bash
cd phases/13-tools-and-protocols/31-mcp-conformance-versioning-and-operations
python3 code/main.py
python3 -m unittest discover -s code/tests -v
```

Verification should prove:

- every included golden and negative transcript reaches its expected outcome
- modern requests require the exact namespaced metadata keys
- HTTP header names are matched case-insensitively and encoded `Mcp-Name` values are decoded exactly
- header and body mismatch returns the modern mismatch code
- response version, ID, result or error exclusivity, error shape, and HTTP mapping are validated
- method-specific tool-list, task, and completion payload requirements are enforced
- every observed `HeaderMismatch` requires an actual HTTP 400 JSON-RPC `-32020` response
- raw `Mcp-Name` whitespace is rejected while exact sentinel-encoded whitespace round-trips
- a missing `resultType` is valid only in the selected legacy era
- additive fields survive raw validation while unknown result types fail
- extension result types require their advertised capability
- recognized modern errors never cause legacy fallback
- notifications produce no JSON-RPC response
- SDK bookkeeping removal and semantic field loss are distinguished
- proxy error collapse is detected and credentials are redacted recursively across camelCase and separator variants
- promotion requires non-empty transcript, SDK, proxy, and healthy operational evidence
- promotion and rollback both require an authenticated, pinned, active, healthy rollback target

## Production Failure Modes | 生产失败模式

> 下表三列：失败、弱测试会报告什么、测试架必须证明什么。最贵的三行：SDK 合成了缺失的判别器（"tools/list 通过了"，实际上原始现代结果缺 `resultType`、是非法的）；代理授权一个工具而源站执行另一个（`Mcp-Name` 必须在每一跳都等于主体路由名）；金丝雀零样本却显示健康（最小样本数必须被强制）。

| Failure | What the weak test reports | What the harness must prove |
|---|---|---|
| SDK synthesizes a missing discriminator | “tools/list passed” | Raw modern result lacked `resultType` and is invalid |
| Client downgrades after `-32021` | “legacy retry worked” | Recognized modern error forbids fallback |
| Unknown result type treated as complete | “response parsed” | Unadvertised lifecycle discriminator is rejected |
| Proxy authorizes one tool and origin executes another | “request reached server” | `Mcp-Name` equals the body routing name at every hop |
| Harness throws before reading the server response | “header mismatch test passed” | HTTP 400 and JSON-RPC `-32020` response are captured and validated |
| Proxy turns origin 400 into generic 500 | “upstream error” | Origin and egress statuses and JSON-RPC bodies are preserved |
| Notification middleware emits `{result: null}` | “handler returned none” | Final egress body is empty and no JSON-RPC response exists |
| SDK strips an additive field | “typed objects match” | Raw and normalized views show the exact dropped field |
| Failure artifact leaks a bearer token | “debug bundle uploaded” | Redaction occurred before hashing, logging, or upload |
| Credential key style bypasses redaction | “denylist contains api_key” | CamelCase and separator variants share one canonical denylist form |
| Canary has no samples but appears healthy | “zero errors” | Minimum sample count is enforced |
| Rollback selects an unknown build | “previous deployment restored” | Target version, admission digest, pins, status, and health are present |

## Operational Rule | 运维准则

Test the bytes you send, the bytes every intermediary forwards, the semantics each SDK exposes, and the evidence operations will use under pressure. Compatibility is an explicit branch. Rollback is an evidence-backed release action. Neither should be an accidental side effect of a permissive parser.

> 测试你发出的字节、每个中间设备转发的字节、每个 SDK 暴露的语义，以及运维在压力之下要用的证据。兼容是一个显式分支；回滚是一个有证据支撑的发布动作。两者都不应该是宽松解析器意外产生的副作用。

> 一句话总结全课：一致性不是"跑通一次"，而是"每个边界都有可观察、可复现的证据"。宽松解析器会把"兼容"和"回滚"都变成意外的副作用；显式分支加证据化决策，才把它们变回受控的工程行为。

## Further Reading | 延伸阅读

- [MCP 2026-07-28 base protocol](https://modelcontextprotocol.io/specification/2026-07-28/basic)
- [MCP version negotiation](https://modelcontextprotocol.io/specification/2026-07-28/basic/versioning)
- [MCP Streamable HTTP](https://modelcontextprotocol.io/specification/2026-07-28/basic/transports/streamable-http)
- [Official MCP conformance project](https://github.com/modelcontextprotocol/conformance)
