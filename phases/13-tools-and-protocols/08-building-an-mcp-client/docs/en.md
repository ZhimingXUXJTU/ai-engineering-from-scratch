# Building an MCP Client: Discovery, Routing, and Dual-Era Fallback | 构建 MCP 客户端：发现、路由与双时代回退

> A modern MCP client repeats its contract on every request. Its hardest compatibility decision is knowing when an old server is truly old and when a modern server is reporting a correctable error.

> **【中文解读】** 现代 MCP 客户端在每个请求上重复携带自己的契约（版本、能力、身份）。它最难的决定是兼容性判断：对端到底是"真旧"（只会 initialize 握手的老服务器），还是"现代服务器在报告一个可修正的错误"？本课构建一个多服务器客户端：现代发现探测、白名单授权的旧版探测、确定性工具合并与路由，全程不发明协议会话。

> **【拓展：MCP 客户端→Agent 编排核心】** MCP 客户端是 Agent 宿主的核心。Claude Desktop、Cursor 等都同时加载多个 MCP 服务器（文件系统、Postgres、GitHub……），把工具列表合并后交给模型。2026-07-28 让稳态更简单（每请求自包含），却让启动更微妙——四种对端形态（现代/报版本错/没听过 discover/沉默等 initialize）必须靠"运营商意图 + 正向协议证据"来区分，而不是把一切探测失败都当旧版。

> 🔗 **【前置】** 学本节前请先掌握：(1) Phase 13 · 07（构建 MCP 服务器）——`server/discover`、逐请求元数据校验、`resultType` 与缓存提示；(2) Phase 13 · 06 的无状态请求模型与 JSON-RPC 信封；(3) Python 可调用对象/回调模拟传输层的方式（本课用进程内 peer 函数代替真实子进程）。多服务器合并与路由是本课新增量。

**Type:** Build | **类型:** 构建
**Languages:** Python | **语言:** Python
**Prerequisites:** Phase 13, Lesson 07 | **前置知识:** Phase 13, Lesson 07
**Time:** ~85 minutes | **时间:** ~85 分钟

## Learning Objectives | 学习目标

- Build every MCP `2026-07-28` request with current metadata.
  中文翻译：为每个 MCP `2026-07-28` 请求构建携带当前元数据的报文。
- Probe stdio servers with `server/discover` and select a mutually supported version.
  中文翻译：用 `server/discover` 探测 stdio 服务器并选定双方都支持的版本。
- Authorize a bounded legacy probe only for explicitly allowlisted peers.
  中文翻译：仅对显式加入白名单的对端授权一次有界的旧版探测。
- Accept a legacy era only after validating a positive `initialize` result for a supported revision.
  中文翻译：只有在验证到受支持修订版的正向 `initialize` 结果后，才接受旧版时代。
- Merge deterministic tool lists without silently overwriting collisions.
  中文翻译：合并确定性工具列表而不静默覆盖命名冲突。
- Route calls to the peer that owns each tool without inventing protocol sessions.
  中文翻译：把调用路由到拥有该工具的对端，且不发明协议会话。

## The Problem | 问题引入

An agent host usually talks to more than one MCP server. It must discover each server, merge tool catalogs, resolve duplicate names, route calls, and recover from transport failure.

> 一个 Agent 宿主通常与多个 MCP 服务器通信。它必须发现每个服务器、合并工具目录、解决重名、路由调用，并从传输层故障中恢复。

The `2026-07-28` revision makes the steady state simpler because each request is self-contained. Compatibility makes startup more subtle. A client may encounter:

> `2026-07-28` 修订让稳态更简单，因为每个请求自包含。兼容性却让启动更微妙。客户端可能遇到：

- a modern server that supports the preferred version;
  中文翻译：支持首选版本的现代服务器；
- a modern server that returns a recognized version or header error;
  中文翻译：返回可识别的版本或头部错误的现代服务器；
- a legacy server that has never heard of `server/discover`;
  中文翻译：从未听说过 `server/discover` 的旧版服务器；
- a legacy server that stays silent until it receives `initialize`.
  中文翻译：收到 `initialize` 之前一直沉默的旧版服务器。

> **【中文解读】** 四种对端形态里最容易踩坑的是后两种与故障的混淆：格式错误的现代请求、过载的服务器、死掉的进程和旧服务器都可能产生同样的超时或连接关闭。这些信号是歧义的。所以客户端的规则是"失败即关闭（fail closed）"——只有"显式的运维配置 + 正向的协议证据"同时到位，才选择旧版时代。

Treating every probe error as legacy is dangerous. A malformed modern request, an overloaded server, a dead process, and an old server can all produce the same timeout or connection close. Those signals are ambiguous. The client must combine explicit operator intent with positive protocol evidence before it chooses the legacy era.

> 把每个探测错误都当作旧版是危险的。格式错误的现代请求、过载的服务器、死掉的进程和旧服务器都可能产生同样的超时或连接关闭。这些信号是歧义的。客户端必须把"显式的运维者意图"与"正向的协议证据"结合起来，才能选择旧版时代。

> 💡 **【类比】** 时代判断像医院急诊分诊：病人（对端服务器）送来时，你不能因为"叫不应"就断定他是外国人（旧版服务器）——他可能只是昏睡（过载）、耳背（请求格式错）或已心跳停止（进程死了）。正确流程：先用标准语系喊话（`server/discover`），听得懂并规范应答 → 现代病人；听得懂但纠正你的用语（-32022/-32020/-32021）→ 还是现代病人，改口即可；完全叫不醒 → 也不能直接按外国人处理，除非病历上写着"确认是外国人，允许换方言再喊一次"（allowlist 授权的有界 initialize 探测），且换方言后得到了清醒的规范应答（正向 initialize 证据）才算确诊。

## The Concept | 核心概念

### A peer, not a protocol session

> **【中文解读】** 客户端为每个服务器进程或端点保留一条"对端记录"（peer record）：传输句柄、选定的时代与版本、最近发现的能力、最近的确定性工具列表、待关联的请求 id、传输健康度。注意分寸：这是客户端自己的记账，不是协议会话状态——现代 MCP 下，服务器仍然在每个请求上收到当前的版本与能力。

Keep one transport peer record for each server process or endpoint:

- transport handle or send function;
  中文翻译：传输句柄或发送函数；
- selected protocol era and version;
  中文翻译：选定的协议时代与版本；
- last discovered server capabilities;
  中文翻译：最近发现的服务器能力；
- last deterministic tool list;
  中文翻译：最近的确定性工具列表；
- pending request ids for correlation;
  中文翻译：用于关联的待处理请求 id；
- transport health.
  中文翻译：传输健康度。

This is client bookkeeping. It is not protocol session state. On modern MCP, the server still receives current version and capabilities on every request.

> 这是客户端记账。它不是协议会话状态。在现代 MCP 上，服务器仍然在每个请求上收到当前的版本与能力。

### Build every modern request from scratch

```python
def modern_request(request_id, method, params, version, capabilities):
    return {
        "jsonrpc": "2.0",
        "id": request_id,
        "method": method,
        "params": {
            **params,
            "_meta": {
                "io.modelcontextprotocol/protocolVersion": version,
                "io.modelcontextprotocol/clientCapabilities": capabilities,
                "io.modelcontextprotocol/clientInfo": CLIENT_INFO,
            },
        },
    }
```

Do not attach metadata once to a connection object and assume it reached the wire. Stamp and inspect the final serialized request.

> 不要把元数据一次性挂到连接对象上就默认它到了线上。要在最终序列化后的请求上盖章并检查。

### Modern discovery

`server/discover` returns supported versions, server capabilities, instructions, cache hints, and recommended server identity. A client chooses the highest mutually supported modern version.

> `server/discover` 返回支持的版本、服务器能力、使用说明、缓存提示与建议的服务器身份。客户端选择双方都支持的最新现代版本。

Discovery is optional for a modern-only client, but it is recommended on stdio. Some legacy servers accept an operation before initialization, so sending `tools/list` first can produce an ambiguous success. `server/discover` creates a clean era boundary.

> 对纯现代客户端而言发现是可选的，但在 stdio 上建议做。某些旧版服务器在初始化之前也接受操作，所以先发 `tools/list` 可能产生歧义的成功。`server/discover` 制造一个干净的时代边界。

### The stdio compatibility probe

> **【中文解读】** stdio 兼容探测的判定树只有三条分支：(1) 收到 DiscoverResult → 现代对端，选定版本后继续；(2) 收到可识别的现代错误（-32020/-32021/-32022）→ 仍是现代对端——-32022 就从 data.supported 选版本重试，其他错误修正请求，绝不发 initialize；(3) 歧义信号（未识别的 JSON-RPC 错误、超时、连接关闭、空响应）→ 不判定时代，除非该对端配置了旧版兼容就失败关闭。关键不变式：一旦对端证明它认识现代错误词表，即使它在白名单里也不许降级。

A dual-era stdio client sends `server/discover` with its preferred modern metadata before any other request. There are three outcome classes:

1. **DiscoverResult.** The server is modern. Select a mutually supported version and continue with per-request metadata.
   中文翻译：**DiscoverResult。** 服务器是现代的。选定双方支持的版本，以逐请求元数据继续。
2. **Recognized modern error.** The server is modern. For `-32022`, choose from `data.supported` and retry with a new request id. For header or capability errors, correct the request. Do not send `initialize`.
   中文翻译：**可识别的现代错误。** 服务器是现代的。`-32022` 就从 `data.supported` 中选择并用新请求 id 重试；头部或能力错误就修正请求。不要发送 `initialize`。
3. **Ambiguous signal.** An unrecognized JSON-RPC error, timeout, connection close, or empty response does not identify an era. Fail closed unless that exact peer is configured for legacy compatibility.
   中文翻译：**歧义信号。** 未识别的 JSON-RPC 错误、超时、连接关闭或空响应不能判定时代。失败即关闭，除非该对端恰好配置了旧版兼容。

Recognized modern protocol errors include:

- `-32020` HeaderMismatch
  中文翻译：`-32020` 头部不一致（HeaderMismatch）
- `-32021` MissingRequiredClientCapability
  中文翻译：`-32021` 缺失必需的客户端能力（MissingRequiredClientCapability）
- `-32022` UnsupportedProtocolVersion
  中文翻译：`-32022` 不支持的协议版本（UnsupportedProtocolVersion）

Recognized modern errors remain modern even when the peer is on the legacy allowlist. Once a server proves that it understands the modern error vocabulary, sending `initialize` would be a downgrade.

> 可识别的现代错误即使来自白名单上的对端也仍判定为现代。一旦服务器证明它理解现代错误词表，再发 `initialize` 就是降级。

Do not treat `-32601` as positive legacy evidence. It only makes an explicitly allowlisted peer eligible for one legacy probe. The same rule applies to a timeout, connection close, or empty response.

> 不要把 `-32601` 当作旧版的正向证据。它只是让显式白名单上的对端获得一次旧版探测的资格。同样的规则适用于超时、连接关闭或空响应。

### Allowlisting is operator intent, not evidence

Legacy compatibility must be an explicit property of one pinned peer configuration:

> 旧版兼容必须是一条固定对端配置的显式属性：

```python
client.add_server("archive", archive_transport, allow_legacy=True)
```

Bind that choice to the configured command or endpoint. Do not use a wildcard that lets an arbitrary server opt itself into weaker semantics. A peer without `allow_legacy=True` fails after an ambiguous discovery outcome and never receives `initialize`.

> 把这个选择绑定到配置的命令或端点上。不要用通配符让任意服务器自行选择更弱的语义。没有 `allow_legacy=True` 的对端在歧义发现结果后直接失败，永远收不到 `initialize`。

The allowlist grants permission to probe. It does not select the era. The client sends one `initialize` under a transport-enforced deadline, then requires all of the following:

> 白名单授予的是探测许可，不是时代选择。客户端在传输层强制限时的前提下发送一次 `initialize`，然后要求以下条件全部成立：

- a JSON-RPC `2.0` response with the matching request id;
  中文翻译：带匹配请求 id 的 JSON-RPC `2.0` 响应；
- exactly one `result` and no `error`;
  中文翻译：恰好一个 `result` 且没有 `error`；
- a `protocolVersion` in the client's configured legacy revision set;
  中文翻译：`protocolVersion` 在客户端配置的旧版修订集合内；
- an object-valued `capabilities` field;
  中文翻译：`capabilities` 字段是对象值；
- a `serverInfo` object with non-empty string `name` and `version` fields.
  中文翻译：`serverInfo` 对象带非空字符串的 `name` 与 `version` 字段。

A timeout, connection close, error response, malformed result, mismatched id, or unsupported revision fails closed. Only a structurally valid positive result selects the legacy era. The code passes `legacy_probe_timeout_ms` to the transport adapter; a real stdio or HTTP adapter must enforce that deadline rather than merely record it.

> 超时、连接关闭、错误响应、畸形结果、id 不匹配或修订不受支持，都会失败即关闭。只有结构合法的正向结果才选择旧版时代。代码把 `legacy_probe_timeout_ms` 传给传输适配器；真实的 stdio 或 HTTP 适配器必须强制执行这个时限，而不是仅仅记录它。

Cache the selected era for the transport peer. Do not probe again before every call.

> 把选定的时代缓存到传输对端上。不要在每次调用前都重新探测。

> ⚠️ **【易错点】** 场景：把 `-32601`（Method not found）或超时直接当成"对端是旧版"的证据，随即发送 initialize / 后果：现代服务器上这是一次降级握手；恶意或故障服务器借机把客户端拖入更弱的语义；无界等待挂死启动流程 / 修复：坚持"白名单只给探测资格 + 五条正向验证全部通过才选旧版"，并让传输适配器真正强制 `legacy_probe_timeout_ms` 时限；任何一条不满足就失败关闭，对端保持不可用。

### Legacy is a compatibility branch

Once the bounded probe returns valid positive legacy evidence, the client uses the selected legacy version exactly as defined by that revision:

1. Verify the response envelope and correlation id.
   中文翻译：校验响应信封与关联 id。
2. Verify the negotiated revision is in the configured legacy set.
   中文翻译：确认协商出的修订在配置的旧版集合内。
3. Record validated capabilities and server identity.
   中文翻译：记录已验证的能力与服务器身份。
4. Send `notifications/initialized` only after all checks pass.
   中文翻译：所有检查通过后才发送 `notifications/initialized`。
5. Use legacy request shapes for that transport lifetime.
   中文翻译：在该传输层生命周期内使用旧版请求形状。

This branch exists for interoperability with known peers. It is not the default design for new servers or new requests. If the transport restarts or its endpoint changes, discard the peer-era cache and negotiate again.

> 这条分支为与已知对端互通而存在。它不是新服务器或新请求的默认设计。如果传输层重启或端点变化，丢弃对端时代缓存并重新协商。

### Discovering and caching tools

For each active peer, call `tools/list`. A modern result includes `resultType`, `ttlMs`, and `cacheScope`. Honor the freshness hint within the correct authorization context. Re-fetch after expiry or a subscribed list-change event.

> 对每个活跃对端调用 `tools/list`。现代结果包含 `resultType`、`ttlMs` 和 `cacheScope`。在正确的授权上下文内尊重新鲜度提示。过期或收到订阅的列表变更事件后重新拉取。

Clients must treat a missing `resultType` from a legacy server as `"complete"`. Do not require modern cache fields on a response from an earlier negotiated era.

> 客户端必须把旧版服务器缺失 `resultType` 的响应当作 `"complete"`。不要对按更早协商时代返回的响应要求现代缓存字段。

The server should return deterministic ordering. The client should also sort before merging so local registry order does not depend on process startup timing.

> 服务器应返回确定性排序。客户端在合并前也应排序，这样本地注册表顺序就不依赖进程启动时序。

### Collision-safe namespace merge

> **【中文解读】** 两个服务器可能都叫 `search`。三种声明的策略：(1) 冲突加前缀——保留第一个规范名，后来的冲突暴露为 `<server>/<tool>`；(2) 冲突拒绝——不加载重复项并报出清晰的配置错误；(3) 静默覆盖——永远不要用，它隐藏了"模型选中的动作实际发给了哪个服务器"。同时存规范名和本地名：模型看到规范名，发出的 `tools/call` 用拥有该工具的服务器声明的本地名。

Two servers may both expose `search`. Choose a declared policy:

1. **Prefix on collision.** Keep the first canonical name and expose later collisions as `<server>/<tool>`.
   中文翻译：**冲突加前缀。** 保留第一个规范名，把后来的冲突暴露为 `<server>/<tool>`。
2. **Reject on collision.** Do not load the duplicate and surface a clear configuration error.
   中文翻译：**冲突拒绝。** 不加载重复项，抛出清晰的配置错误。
3. **Silent overwrite.** Never use this. It hides which server receives a model-selected action.
   中文翻译：**静默覆盖。** 永远不要用。它隐藏了哪个服务器收到模型选中的动作。

Store both canonical and local names. The model sees the canonical name. The outgoing `tools/call` uses the local name the owning server declared.

> 同时存储规范名与本地名。模型看到规范名。发出的 `tools/call` 使用拥有该工具的服务器声明的本地名。

### Routing a call

Routing is a pure lookup:

> 路由是一次纯查表：

```text
canonical tool name
  -> peer name + local tool name
  -> new JSON-RPC request id
  -> modern request metadata or explicit legacy shape
  -> matching response id
```

Do not send a call when its owning transport is unavailable. Reconnect or restart the transport, then re-run discovery and `tools/list`. Modern in-flight requests lost on a broken transport can be retried with a new JSON-RPC id when the operation's safety policy permits it.

> 当拥有该工具的传输层不可用时不要发送调用。重连或重启传输层，然后重跑发现与 `tools/list`。断掉的传输层上丢失的现代在途请求，在操作的安全策略允许时可以用新的 JSON-RPC id 重试。

### Notifications and subscriptions

Modern list and resource changes arrive only on a client-opened `subscriptions/listen` stream. The client sends the notification filter, waits for `notifications/subscriptions/acknowledged`, and correlates events with the listen request id in notification metadata.

> 现代的列表与资源变更只到达客户端打开的 `subscriptions/listen` 流上。客户端发送通知过滤器，等待 `notifications/subscriptions/acknowledged`，并用通知元数据里的 listen 请求 id 关联事件。

On disconnect, open a new listen request and refetch relevant lists or resources. Modern streams do not resume with `Last-Event-ID`.

> 断连时，打开一个新的 listen 请求并重新拉取相关列表或资源。现代流不用 `Last-Event-ID` 恢复。

### No server-initiated requests

Modern servers do not call the client with independent JSON-RPC requests for sampling, elicitation, or roots. They return `input_required`, and the client retries the original request after fulfilling the embedded input requests.

> 现代服务器不会用独立的 JSON-RPC 请求调用客户端来要 sampling、elicitation 或 roots。它们返回 `input_required`，客户端补齐内嵌的输入请求后重试原请求。

Do not block the peer's response reader while fulfilling input. Preserve correlation and create a new JSON-RPC id for the retry.

> 补齐输入时不要阻塞对端的响应读取器。保持关联性，并为重试创建新的 JSON-RPC id。

> **【拓展：与旧版客户端课的对照】** 旧版这节课的主角是"子进程管理 + initialize 握手 + sampling 回调"；新版把它们全部让位给"时代协商"：sampling/elicitation 已废弃为多轮往返请求，握手只剩一条白名单授权的有界探测分支，进程管理抽象成对端记录（peer record）。变化最大也最值得体会的一点：客户端的复杂度从"运行时会话编排"转移到了"启动时的时代判定与失败关闭策略"。

```figure
tp-client-merge
```

## Use It | 用框架实现

`code/main.py` uses in-process peer functions so the protocol decisions stay visible. It connects to two modern peers and one intentionally allowlisted legacy peer, then merges and routes their tools. The transport callable receives a timeout budget so the compatibility branch cannot hide an unbounded probe.

> `code/main.py` 使用进程内的对端函数，好让协议决策保持可见。它连接两个现代对端和一个刻意加入白名单的旧版对端，然后合并并路由它们的工具。传输可调用对象会收到超时预算，兼容分支就无法隐藏一次无界探测。

```bash
cd code
python3 main.py
python3 -m unittest discover tests -v
```

The tests prove boundaries that normal demos miss:

> 这些测试证明了普通演示会漏掉的边界：

- modern requests repeat metadata;
  中文翻译：现代请求重复携带元数据；
- `-32022` retries modern discovery without initialization;
  中文翻译：`-32022` 重试现代发现而不做初始化；
- recognized modern errors never downgrade, even for an allowlisted peer;
  中文翻译：可识别的现代错误绝不降级——即使对端在白名单上；
- timeouts, connection closes, empty responses, and unrecognized errors do not trigger `initialize` without an allowlist;
  中文翻译：超时、连接关闭、空响应和未识别的错误在没有白名单时不会触发 `initialize`；
- an allowlisted peer becomes legacy only after a valid, supported `initialize` result;
  中文翻译：白名单对端只有在收到合法且受支持的 `initialize` 结果后才成为旧版；
- malformed and unsupported legacy results leave the peer unavailable;
  中文翻译：畸形或不受支持的旧版结果使对端保持不可用；
- a successfully selected era is cached for the transport lifetime.
  中文翻译：成功选定的时代会缓存整个传输层生命周期。

## Ship It | 产出物

This lesson ships `outputs/skill-mcp-client-harness.md`. It scaffolds modern request stamping, stdio era negotiation, deterministic namespace merge, routing, and a fail-closed legacy compatibility branch.

> 本课交付 `outputs/skill-mcp-client-harness.md`。它搭建现代请求盖章、stdio 时代协商、确定性命名空间合并、路由，以及一条失败关闭的旧版兼容分支。

## Exercises | 练习题

1. Make a fake server return `-32022` with no mutually supported version. Confirm the client fails instead of sending `initialize`.
   中文翻译：让一个假服务器返回 `-32022` 且没有双方都支持的版本。确认客户端直接失败而不是发送 `initialize`。

2. Allowlist a fake legacy server, make its bounded `initialize` probe time out, and prove the peer stays `unknown` and unavailable.
   中文翻译：把一个假旧版服务器加入白名单，让它有界的 `initialize` 探测超时，证明该对端保持 `unknown` 且不可用。

3. Add `cacheScope: "private"` tool lists for two authorization contexts. Confirm the client never shares one context's cached result with the other.
   中文翻译：为两个授权上下文添加 `cacheScope: "private"` 的工具列表。确认客户端绝不把一个上下文的缓存结果共享给另一个。

4. Change the collision policy to rejection and make startup fail with both peer names in the error.
   中文翻译：把冲突策略改为拒绝，让启动失败并在错误信息中带上两个对端的名字。

5. Add a finite `subscriptions/listen` simulator. On stream loss, re-listen with a new request id and refetch tools.
   中文翻译：添加一个有限的 `subscriptions/listen` 模拟器。流断开时，用新请求 id 重新监听并重新拉取工具。

## Key Terms | 术语速查表

| Term | Meaning |
|------|---------|
| Peer | Client-side record for one server transport and its discovered data |
| Protocol era | Modern per-request metadata or legacy initialization semantics |
| Discovery probe | Initial `server/discover` used to identify the stdio era |
| Recognized modern error | Error that proves modern behavior and forbids legacy fallback |
| Legacy allowlist | Operator configuration permitting one bounded compatibility probe for a pinned peer |
| Positive legacy evidence | Valid, correlated `initialize` result for an explicitly supported legacy revision |
| Merged namespace | Canonical tool names across all active peers |
| Collision policy | Prefix or reject rule for duplicate tool names |
| Era cache | Selected modern or legacy behavior stored for one transport peer |
| Transport recovery | Restart or reconnect, rediscover, relist, and retry safely with a new id |

> 术语中文对照：Peer=对端（客户端侧对一个服务器传输层及其发现数据的记录）；Protocol era=协议时代（现代逐请求元数据或旧版初始化语义）；Discovery probe=发现探测（用于判定 stdio 时代的首次 `server/discover`）；Recognized modern error=可识别的现代错误（证明对端是现代的并禁止旧版回退）；Legacy allowlist=旧版白名单（允许为一个固定对端做一次有界兼容探测的运维配置）；Positive legacy evidence=正向旧版证据（对显式受支持旧版修订的合法且关联的 `initialize` 结果）；Merged namespace=合并命名空间（跨所有活跃对端的规范工具名）；Collision policy=冲突策略（重名工具的前缀或拒绝规则）；Era cache=时代缓存（为一个传输对端存下选定的现代或旧行为）；Transport recovery=传输层恢复（重启/重连、重新发现、重新列表、用新 id 安全重试）。

## Further Reading | 延伸阅读

- [MCP Specification 2026-07-28](https://modelcontextprotocol.io/specification/2026-07-28/)
  中文翻译：MCP 2026-07-28 规范全文
- [MCP Server Discovery](https://modelcontextprotocol.io/specification/2026-07-28/server/discover)
  中文翻译：server/discover 方法规范
- [MCP stdio Transport](https://modelcontextprotocol.io/specification/2026-07-28/basic/transports/stdio)
  中文翻译：stdio 传输层规范
- [MCP Versioning](https://modelcontextprotocol.io/specification/2026-07-28/basic/versioning)
  中文翻译：MCP 版本协商机制
- [MCP Tools](https://modelcontextprotocol.io/specification/2026-07-28/server/tools)
  中文翻译：tools 原语规范
