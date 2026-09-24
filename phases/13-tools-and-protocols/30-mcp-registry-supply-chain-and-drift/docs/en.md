# MCP Registry Supply Chain: Admission, Drift, and Rollback | MCP 注册中心供应链：准入、漂移与回滚

> A registry entry tells you what a publisher declared. Production admission proves what you fetched, what you observed, what you approved, and what you can safely restore.

> **【中文解读】** 注册中心条目只告诉你"发布者声明了什么"；生产准入（admission）要证明的是"你实际取回了什么、观察到了什么、审批了什么、以及能安全恢复到什么"。本课把 MCP 服务器的供应链拆成命名空间、记录、执行来源、运行时、准入、运维六个边界，每个边界都要求可验证的证据，最终落地为一个防篡改的准入账本和一个只选已准入版本的可回滚路由。

> 🔗 **【前置】** 学本课前请先掌握：Phase 13 · 17（网关与注册中心——官方 Registry 的命名空间验证、网关在架构中的位置）和 Phase 13 · 18（生产认证——OAuth 2.1 与凭证治理）。本课是这两课的运维延伸：一个 MCP 服务器进入生产之前，证据链如何审批、安装之后漂移如何被发现、出事之后路由如何回滚。本课基于 MCP 2026-07-28 规范的 `server/discover`。

**Type:** Build | **类型:** 动手实践
**Languages:** Python | **语言:** Python
**Prerequisites:** Phase 13 · 17 (gateways and registries), Phase 13 · 18 (production authentication) | **前置知识:** Phase 13 · 17（网关与注册中心）、Phase 13 · 18（生产认证）
**Time:** ~90 minutes | **时间:** 约 90 分钟

## Learning Objectives | 学习目标

- Separate Registry publication, package provenance, runtime discovery, and local approval.
  中文翻译：区分 Registry 发布、包来源证明（provenance）、运行时发现与本地审批这四件事。
- Verify an MCP server namespace without trusting the name inside its own record.
  中文翻译：在不信任记录内部自带名字的前提下，验证 MCP 服务器的命名空间。
- Pin immutable publication, execution-source, provenance, and live descriptor evidence.
  中文翻译：锁定（pin）不可变的发布记录、执行来源、来源证明与在线描述符证据。
- Detect registry status changes and runtime drift after admission.
  中文翻译：在准入之后检测注册中心状态变化与运行时漂移（drift）。
- Roll back routing to a previously admitted version without rewriting history.
  中文翻译：把路由回滚到一个此前已通过准入的版本，且不改写历史。
- Maintain a tamper-evident admission ledger that explains every decision.
  中文翻译：维护一个防篡改（tamper-evident）的准入账本（ledger），能解释每一次决策。

## The Problem | 问题引入

You find `com.example/inventory` in a registry. Its description looks right. Its package exists. The server answers `server/discover`.

> 你在注册中心里找到了 `com.example/inventory`。它的描述看着没问题，包也存在，服务器也响应了 `server/discover`。

> **【中文解读】** "它在注册中心里"并不是一个事实，而是四条来自不同权威方的事实链：发布者认证、包注册中心交付、运行端点自述、组织审批。把它们压扁成"在注册中心里所以可信"，就是供应链盲区的起点。这和 npm/PyPI 依赖进入生产是同一个问题，只是 MCP 服务器还会在安装之后继续变化（工具漂移），所以证据链必须延伸到运行时。

That is not one fact. It is a chain of facts from different authorities:

1. A publisher authenticated for a namespace submitted a record.
2. A package registry served an artifact with a specific identity and digest.
3. A running endpoint reported a protocol version, capabilities, tools, and diagnostic server information.
4. Your organization decided that this exact combination was allowed.

> 这不是一个事实，而是来自不同权威方的一条事实链：(1) 一个通过了命名空间认证的发布者提交了记录；(2) 一个包注册中心交付了具有特定身份和摘要（digest）的制品；(3) 一个运行中的端点报告了协议版本、能力、工具列表和诊断性服务器信息；(4) 你的组织决定"恰好这个组合"被允许。

Collapsing those facts into “it is in the registry, so trust it” creates a supply chain blind spot. A valid publication can still be deprecated. A package tag can point at an unexpected artifact if you do not pin its digest. A server can add a destructive tool after review. A rollback can silently choose a version that was never admitted.

> 把这些事实压扁成"它在注册中心里，所以可信"，就制造了一个供应链盲区。一条有效的发布记录仍可能被标记为 deprecated；如果你不锁定摘要，包标签可能指向意料之外的制品；服务器可能在评审之后新增一个破坏性工具；回滚可能悄悄选中一个从未通过准入的版本。

The fix is an admission controller with evidence at every boundary.

> 修复方式是一个在每个边界都留下证据的准入控制器（admission controller）。

## The Registry Is an Index, Not Your Approval System | 注册中心是索引，不是你的审批系统

The official MCP Registry stores server metadata. Its `server.json` record names a server version and declares one or more packages or remote endpoints. Publication rules add namespace authentication, package ownership checks, restricted registry rules, and a narrow publisher metadata location.

> 官方 MCP Registry 存储的是服务器元数据。它的 `server.json` 记录为一个服务器版本命名，并声明一个或多个包或远程端点。发布规则额外提供命名空间认证、包所有权检查、受限的注册中心规则，以及一个狭窄的发布者元数据存放位置。

Those controls answer publication questions. Your production policy still answers deployment questions:

> 这些控制回答的是"发布"问题。你的生产策略仍然要自己回答"部署"问题：

| Boundary | Question | Evidence owner |
|---|---|---|
| Namespace | Was the publisher allowed to use this name? | Registry authentication plus your verified namespace input |
| Record | What did the publisher declare for this version? | Immutable `server.json` digest |
| Execution source | Which package or remote endpoint will execute? | Declared source fields, verified ownership result, transport, and trusted digest |
| Runtime | What does the endpoint expose now? | `server/discover` and tool descriptors |
| Admission | Did your policy approve this exact set? | Local pin and ledger entry |
| Operations | Is it still safe, and what can replace it? | Drift checks, status sync, health, and rollback route |

> **【中文解读】** 这张表是全课的骨架：六个边界，每个边界一个问题、一个证据持有方。命名空间问"发布者有权用这个名字吗"，记录问"这个版本声明了什么"（证据是不可变 `server.json` 摘要），执行来源问"实际执行的会是哪个包或端点"，运行时问"端点现在暴露什么"（证据是 `server/discover` 和工具描述符），准入问"你的策略是否恰好批准了这一组"，运维问"它现在还安全吗、坏了拿什么替换"。注意证据持有方各不相同——没有任何一行是"Registry 替你担保"。

> 💡 **【类比】** Registry 像手机应用商店的"上架审核"，你的准入系统像企业的 MDM（移动设备管理）装机审批。App 通过商店审核只说明"发布者身份合规、包没被偷换"，不代表"你的公司允许在办公设备上运行它"。npm/PyPI 与企业内部 Artifactory + 审批流的关系也是同样的分工：注册中心是索引，审批权永远在你自己手里。

The Registry schema version and the MCP protocol version are independent. A record may use the published `2025-12-11` server schema while the live server supports MCP `2026-07-28`. Never infer one from the other.

> Registry 的 schema 版本与 MCP 协议版本是相互独立的。一条记录可能使用已发布的 `2025-12-11` 服务器 schema，而在线服务器支持的是 MCP `2026-07-28`。永远不要从其中一个推断另一个。

```figure
mcp-registry-admission
```

## Seven Controls in One Admission Decision | 一次准入决策中的七项控制

> **【中文解读】** 一次安全的准入要把七个控制点串成一个决策：(1) 命名空间验证——发布者是否真有权用这个名字；(2) 来源拼接（provenance join）——声明的包与实际取回的制品在多个字段上对得齐；(3) 锁定决策而非只锁版本——pin 里要有各层摘要；(4) 在线漂移检测——对将真正接流量的服务器做发现并比对工具描述符；(5) 注册中心状态是活状态——active/deprecated/deleted 要持续同步；(6) 回滚即路由恢复——只选已准入且当前合格的目标；(7) 追加式准入账本——哈希链让历史可验证。下面七个小节逐个展开。

### 1. Namespace verification | 命名空间验证

Official Registry names use authenticated namespaces. A verified domain can map to a reversed domain prefix. For example, control of `example.com` can establish `com.example/*`.

> 官方 Registry 的名字使用经过认证的命名空间。一个已验证的域可以映射为反转的域名前缀。例如，对 `example.com` 的控制权可以确立 `com.example/*`。

Do not accept a string prefix check:

```python
server_name.startswith("com.example")
```

That also accepts `com.exampleevil/tool`. Split the name at `/`, require a non-empty slug, and compare the namespace segment exactly. More importantly, pass the verified namespace into admission from the authentication result. Do not derive trust from the untrusted record.

> 这个前缀检查也会放行 `com.exampleevil/tool`。正确的做法是按 `/` 切分名字、要求 slug 非空，并对命名空间段做精确比较。更重要的是，要把认证结果中验证过的命名空间传入准入流程——不要从未被信任的记录自身推导信任。

GitHub-backed namespaces and domain-backed namespaces use different authentication paths. Normalize either path into one admission input: the exact verified namespace string.

> GitHub 背书的命名空间和域名背书的命名空间走不同的认证路径。把两种路径都归一化成同一个准入输入：精确的、已验证的命名空间字符串。

### 2. Provenance join | 来源拼接

For a package record, the declaration and fetched artifact must join on explicit fields:

- package registry type
- package identifier
- package version
- verified ownership result
- downloaded artifact digest

> 对于包记录，声明与取回的制品必须在这些显式字段上拼接对齐：包注册中心类型、包标识符、包版本、已验证的所有权结果、下载制品的摘要。任何一个字段对不上，这条 provenance 链就是断的。

Also validate the declared package transport. A record with only a remote endpoint is valid and must not be rejected for lacking a package. For a remote source, join the declared URL and transport type to independently verified endpoint ownership and a digest of the trusted connection or deployment evidence.

> 还要校验声明中包的 transport。一条只带远程端点的记录同样合法，不能因为"没有包"而被拒绝。对于远程来源，要把声明的 URL 和 transport 类型，与独立验证过的端点所有权、以及可信连接或部署证据的摘要拼接在一起。

The lesson code supports both source kinds and hashes the selected source together with the Registry source, server name, Registry version, record digest, and evidence digest. The resulting provenance digest is a compact pointer to the full evidence set. It is not a substitute for retaining the evidence.

> 本课代码同时支持两种来源类型，并把选中的来源与 Registry 来源、服务器名、Registry 版本、记录摘要和证据摘要一起哈希。得到的 provenance 摘要是指向完整证据集的紧凑指针，但不能替代保留证据本身。

Never accept a digest supplied only by the artifact you are trying to verify. Calculate it at a trusted fetch boundary, or receive it from a package service whose verification result you validate.

> 永远不要接受仅由"你正要验证的那个制品"自己提供的摘要。要么在可信的抓取边界上自行计算，要么从一个其验证结果会被你校验的包服务获取。

### 3. Pin the decision, not only the version | 锁定决策，而不只是版本

Registry versions are unique publication identifiers. Published metadata is immutable. A changed record requires a new version. Semantic versioning is recommended, but the Registry does not require it and does not accept version ranges.

> Registry 版本是唯一的发布标识符。已发布的元数据不可变；记录要变就必须发新版本。推荐语义化版本，但 Registry 既不强制，也不接受版本范围。

This means `^1.4` is not an admission pin. Neither is “latest.” A useful pin contains:

> 这意味着 `^1.4` 不是准入 pin，"latest"（最新）也不是。一个有用的 pin 应包含：

```json
{
  "server": "com.example/inventory",
  "version": "1.0.0",
  "recordDigest": "...",
  "source": {"kind": "package", "registryType": "pypi"},
  "sourceDigest": "...",
  "toolsetDigest": "...",
  "provenanceDigest": "...",
  "registryStatus": "active"
}
```

Pinning several layers lets you identify which boundary changed. A record digest change under the same Registry version is a Registry integrity failure. A source digest change under the same package coordinate or remote deployment is an execution-source integrity failure. A toolset digest change is runtime drift.

> 锁定多个层次，你才能定位是哪个边界变了：Registry 版本没变而记录摘要变了，是 Registry 完整性故障；包坐标或远程部署没变而来源摘要变了，是执行来源完整性故障；工具集摘要变了，就是运行时漂移。多层 pin 的价值不在于"锁得住"，而在于报警时能精确指认失守的那一层。

### 4. Live drift detection | 在线漂移检测

Admission should observe the server that will actually receive traffic. Call `server/discover`, list or otherwise obtain the exposed tool descriptors through your trusted path, and verify:

> 准入应当观察那个将真正接收流量的服务器。调用 `server/discover`，通过你的可信路径列出或以其他方式取得暴露的工具描述符，然后验证：

- `2026-07-28` is in `supportedVersions`
- all locally required capabilities are present
- every tool descriptor has the required identity and schema surface
- the normalized descriptor digest matches the admitted pin on later checks

> 验证四件事：(1) `2026-07-28` 在 `supportedVersions` 里；(2) 所有本地必需的能力都在；(3) 每个工具描述符具备要求的身份与 schema 结构；(4) 后续检查中，规范化后的描述符摘要与准入 pin 一致。

The optional result `_meta["io.modelcontextprotocol/serverInfo"]` value is self-reported display, log, and debugging context. Record it as diagnostic evidence, but never use it to establish namespace, package ownership, endpoint ownership, admission, or any other security decision. A direct `serverInfo` alias outside `_meta` is not the contract field and should not be promoted into diagnostic evidence.

> 可选结果 `_meta["io.modelcontextprotocol/serverInfo"]` 的值是服务器自述的展示、日志与调试上下文。把它记为诊断证据可以，但绝不能用它来确立命名空间、包所有权、端点所有权、准入或任何其他安全决策。`_meta` 之外的 `serverInfo` 直接别名不是契约字段，不应升级为诊断证据。

Normalize only fields whose order has no meaning. The sample sorts the tool list by stable name before hashing, so a harmless list-order change does not cause drift. It does not discard descriptor fields. A new tool, changed schema, changed description, or new annotations changes the pin.

> 只对"顺序无意义"的字段做规范化。示例在哈希前按稳定名称对工具列表排序，这样无害的列表顺序变化不会触发漂移告警；但它不丢弃描述符字段——新增工具、schema 变化、描述变化或新增 annotations，都会改变 pin。

The sample treats malformed descriptors and any descriptor digest change as drift, quarantines the pin, removes its active route, and blocks that version as a rollback target. A production policy may allow an editorial change only through a new review, because descriptions influence model tool selection. “Cosmetic” metadata can alter agent behavior.

> 示例把畸形描述符和任何描述符摘要变化都当作漂移：隔离（quarantine）该 pin、摘除其活跃路由、并把这个版本拉入回滚黑名单。生产策略若要放行一处"编辑性改动"，只能走一次新的评审——因为描述会影响模型的工具选择。"纯外观"元数据也能改变 agent 行为。

> **【中文解读】** 第 4 项控制是全课的核心洞察：供应链审查不是一次性动作。服务器审查通过之后、运行之中，工具面还可能变化——这就是运行时漂移（对应 Phase 13 · 15 的工具投毒场景）。对策是"描述符摘要"这个锚点：准入时算一次、此后每次巡检再算一次，任何差异即隔离加摘路由。特别注意最后一段——工具描述文本的变化也要算漂移，因为它直接影响 LLM 选不选这个工具。

### 5. Registry status is live state | 注册中心状态是活状态

The Registry API attaches a response-level `_meta` object beside each server record. Registry-managed fields live under `_meta["io.modelcontextprotocol.registry/official"]`. Pass the response `_meta` object to admission and read `_meta["io.modelcontextprotocol.registry/official"].status`. A direct `_meta.status` value is not the official wire shape. Do not confuse response metadata with the publication record's own `_meta`. Status can be:

> Registry API 在每条服务器记录旁附带一个响应级 `_meta` 对象。Registry 管理的字段位于 `_meta["io.modelcontextprotocol.registry/official"]` 之下。把响应的 `_meta` 对象传入准入流程，读取 `_meta["io.modelcontextprotocol.registry/official"].status`。直接的 `_meta.status` 值不是官方线格式。不要把响应元数据与发布记录自身的 `_meta` 混为一谈。状态可以是：

- `active`: returned by default and eligible for local admission
- `deprecated`: still discoverable with a warning, but no longer a safe automatic choice
- `deleted`: hidden by default while its historical record remains available through deleted or incremental views

> 三种状态：`active`（默认返回，可进入本地准入）、`deprecated`（仍可被发现但带警告，不再是安全的自动选择）、`deleted`（默认隐藏，但历史记录仍可通过 deleted 或增量视图获取）。

Sync status after admission. If an active version becomes deprecated or deleted, quarantine its pin and stop routing new work to it. Keep the evidence. Deletion from the default listing is not permission to erase your audit trail.

> 准入之后要持续同步状态。如果一个 active 版本变成 deprecated 或 deleted，就隔离它的 pin、停止把新工作路由给它。但证据要保留——从默认列表中消失，并不是让你抹掉审计轨迹的许可。

Publisher-provided custom metadata belongs only under `_meta.io.modelcontextprotocol.registry/publisher-provided` in a publication record. Registry-managed response metadata is separate. Do not let a publisher set its own official status.

> 发布者自定义的元数据只能放在发布记录的 `_meta.io.modelcontextprotocol.registry/publisher-provided` 之下。Registry 管理的响应元数据与之分离。绝不让发布者自己设置自己的官方状态。

### 6. Rollback means route restoration | 回滚即路由恢复

An immutable publication is not edited during rollback. Rollback selects a previously admitted, currently eligible pin and changes the active route.

> 回滚不会去改写不可变的发布记录。回滚是选中一个此前已准入、当前仍合格的 pin，然后切换活跃路由。

A safe target must:

1. Have a completed admission record.
2. Still have an active Registry status under your policy.
3. Not be quarantined by runtime or security evidence.
4. Still resolve to the pinned package and live descriptor set.
5. Pass current health checks.

> 安全的回滚目标必须：(1) 有一条完整的准入记录；(2) 在你的策略下 Registry 状态仍是 active；(3) 没有被运行时或安全证据隔离；(4) 仍能解析到 pin 住的包和在线描述符集；(5) 通过当前健康检查。

The sample focuses on the first three conditions. A real reconciler should re-fetch the package and re-check the live endpoint before activation.

> 示例聚焦前三个条件。真实的 reconciler 在激活之前还应重新抓取包并复查在线端点。

### 7. Append an admission ledger | 追加式准入账本

An admission database says what is active. A ledger explains why.

> 准入数据库说的是"现在什么在活跃"；账本（ledger）解释的是"为什么"。

Each sample entry contains a sequence, time, event, server, version, outcome, reasons, evidence, the previous entry hash, and its own hash. Changing an older outcome breaks verification of that entry and every later link.

> 示例的每条账目包含序号、时间、事件、服务器、版本、结论、原因、证据、前一条目的哈希以及自身的哈希。改动任何一条旧结论，都会让该条目以及其后所有链上条目的校验失败。

This is tamper-evident, not magically tamper-proof. Anchor periodic ledger heads in a separate trust domain, such as signed release metadata or write-once storage. Restrict who can append. Keep authorization tokens, package credentials, tool arguments, and private endpoint data out of evidence.

> 这是"可证篡改"（tamper-evident），不是神奇的"防篡改"（tamper-proof）。要周期性地把账本头锚定到一个独立的信任域，例如签名的发布元数据或一次写入存储。限制谁可以追加账目。授权 token、包凭证、工具参数和私有端点数据一律不得进入证据。

## Build It | 动手实现

The runnable controller is in `code/main.py`. It uses only the Python standard library.

> 可运行的控制器在 `code/main.py`，只使用 Python 标准库。

Start with the finite demonstration:

```bash
cd phases/13-tools-and-protocols/30-mcp-registry-supply-chain-and-drift
python3 code/main.py
```

The demonstration performs five operations:

1. Admit `1.0.0` with matching namespace, package provenance, protocol, capabilities, and tools.
2. Admit `1.1.0` and make it active.
3. Observe an unexpected delete tool at runtime.
4. Observe the Registry status for `1.1.0` become `deprecated`.
5. Restore routing to the still-admitted `1.0.0` pin.

> 演示的五个操作：准入 `1.0.0`（命名空间、包 provenance、协议、能力、工具全部匹配）；准入 `1.1.0` 并设为活跃；运行时观察到一个意外的 delete 工具；观察 Registry 把 `1.1.0` 的状态改为 `deprecated`；把路由恢复到仍处于已准入状态的 `1.0.0` pin。

Expected shape:

```json
{
  "admitted": [true, true],
  "driftAllowed": false,
  "rollbackAllowed": true,
  "activeVersion": "1.0.0",
  "ledgerValid": true
}
```

Read the implementation in this order:

> 预期输出形状：两次准入都成功（`admitted: [true, true]`），运行时漂移被拒绝路由（`driftAllowed: false`），回滚被允许（`rollbackAllowed: true`），活跃版本回到 `1.0.0`，账本校验通过。按以下顺序阅读实现：

1. `namespace_for_domain()` and `namespace_matches()` establish exact naming authority.
2. `digest()` and `normalized_tools()` produce deterministic evidence.
3. `RegistryAdmissionController.admit()` joins publication, provenance, runtime, and policy.
4. `check_live()` compares a new observation with the pin.
5. `observe_registry_status()` quarantines versions whose Registry state changes.
6. `rollback()` activates only a previously admitted eligible target.
7. `AdmissionLedger.verify()` detects changes to recorded history.

## Use It | 用框架实现

Put the controller between discovery and routing:

> 把准入控制器放在发现（discovery）与路由（routing）之间：

```text
Registry sync -> artifact verifier -> live discovery -> admission controller -> route table
                                               |                 |
                                               v                 v
                                          evidence store    admission ledger
```

Use separate identities for these jobs. A Registry sync worker needs read access to metadata. An artifact verifier needs package fetch access. A route reconciler needs permission to activate an approved pin. None of them needs every credential.

> 为这些工作使用相互分离的身份。Registry 同步 worker 只需要元数据读取权限；制品验证器只需要包抓取权限；路由 reconciler 只需要激活已批准 pin 的权限。没有一个角色需要持有全部凭证——最小权限原则在供应链流水线里同样成立。

Make rollout state explicit. “Approved” means the evidence passed policy. “Active” means the route currently selects it. “Quarantined” means it cannot receive new work. “Superseded” means another admitted version is active. Do not encode all four meanings in one Boolean.

> 让发布状态显式化："Approved"（已批准）表示证据通过了策略；"Active"（活跃）表示路由当前选中的是它；"Quarantined"（已隔离）表示它不能再接收新工作；"Superseded"（已被取代）表示另一个已准入版本处于活跃。不要把这四层含义塞进一个布尔值。

Run admission before exposing a server in `tools/list`. Otherwise a client can discover a tool during the gap between publication and policy evaluation.

> 在把服务器暴露进 `tools/list` 之前先完成准入。否则客户端可能在"已发布"与"策略已评估"之间的空窗期里发现并调用一个工具。

> **【中文解读】** Use It 一节给出三个生产化要点：流水线各环节用独立身份（防一个组件失陷即全线失守）；发布状态用四个词而非一个布尔（Approved/Active/Quarantined/Superseded 各有含义）；准入必须先于 `tools/list` 暴露（堵住发布与审批之间的发现空窗）。这条"text diagram"里的 evidence store 与 admission ledger 正是第 7 项控制的两类持久化产物。

## Interactive Lab | 交互实验

You will watch one boundary fail at a time.

> 你将逐个观察每个边界是如何失效的。

### Lab A: namespace collision | 实验 A：命名空间碰撞

Open a Python shell from the code directory:

```bash
cd phases/13-tools-and-protocols/30-mcp-registry-supply-chain-and-drift/code
python3 -q
```

Then run:

```python
from main import namespace_matches
namespace_matches("com.example/inventory", "com.example")
namespace_matches("com.exampleevil/inventory", "com.example")
```

The first result is `True`; the second is `False`. Replace the exact comparison with `startswith` locally and observe why the second name crosses the boundary. Restore the exact comparison before continuing.

> 第一个结果是 `True`，第二个是 `False`。在本地把精确比较换成 `startswith`，观察第二个名字为什么能越过边界。继续之前记得恢复精确比较。

### Lab B: descriptor drift | 实验 B：描述符漂移

```python
from main import *
times = iter(f"2026-08-21T12:00:{n:02d}+00:00" for n in range(10))
c = RegistryAdmissionController(clock=lambda: next(times))
meta = {OFFICIAL_META_KEY: {"status": "active"}}
c.admit(sample_record("1.0.0"), meta, "com.example", evidence_for("1.0.0"), sample_live("1.0.0"))
c.check_live("com.example/inventory", "1.0.0", sample_live("1.0.0", True))
```

Inspect the reasons and route state. The package and Registry record did not change. The runtime tool surface did, so the controller quarantined and deactivated the pin. This is why supply chain control must continue after installation.

> 检查 reasons 和路由状态：包与 Registry 记录都没变，变的是运行时工具面——于是控制器隔离并停用了这个 pin。这就是供应链控制必须在安装之后继续存在的原因。

### Lab C: status and rollback | 实验 C：状态与回滚

Admit `1.1.0`, mark it deprecated, and try both rollback targets:

```python
c.admit(sample_record("1.1.0"), meta, "com.example", evidence_for("1.1.0"), sample_live("1.1.0"))
c.observe_registry_status("com.example/inventory", "1.1.0", "deprecated")
c.rollback("com.example/inventory", "1.1.0", "unsafe retry")
c.rollback("com.example/inventory", "1.0.0", "restore known release")
c.ledger.verify()
```

The quarantined target is rejected. The earlier active pin is accepted. The ledger remains valid.

> 被隔离的回滚目标被拒绝；更早的活跃 pin 被接受；账本校验仍然通过。

## Practice Lab | 进阶练习

Extend the controller with a two-person approval gate.

> 给控制器扩展一道双人审批门（two-person approval gate）。

> **【中文解读】** 进阶练习把第 7 项控制升级为"破坏性工具必须两人审批"：审批要以签名证据引用的形式存储，不能是 pin 里可变的名字；工具集里出现 `destructiveHint: true` 的工具时，要求两个不同的评审身份；重复身份被拒绝；审批未完成时，最初的准入尝试也要保留在账本里。这相当于给"可以删除东西的工具"加了双人规则（two-person rule）——单人失陷或单人失误都不足以把它送进生产。

Requirements:

- Store approvals as signed evidence references, not mutable names in the pin.
- Require two different reviewer identities for a toolset that contains a tool with `destructiveHint: true`.
- Reject duplicate reviewer identities.
- Preserve the original admission attempt in the ledger when approval is incomplete.
- Add tests for zero, one, duplicate, and two distinct approvals.
- Do not log signatures, credentials, or full private tool arguments.

Success means a destructive tool cannot become active until both identities approved the exact record, package, and toolset digests.

> 成功的标准：在两个身份都批准了那条精确的记录摘要、包摘要和工具集摘要之前，破坏性工具不可能进入活跃状态。

## Shipped Artifact | 产出物

This lesson ships `outputs/skill-mcp-registry-admission.md`. Use it as a flat, reusable runbook when reviewing a new Registry version or investigating drift. It defines the inputs, refusal rules, evidence bundle, status reconciliation, and rollback proof without depending on the sample class names.

> 本课附带 `outputs/skill-mcp-registry-admission.md`。在评审一个新的 Registry 版本或调查漂移时，把它当作一份扁平、可复用的 runbook 使用。它定义了输入、拒绝规则、证据包、状态对账与回滚证明，且不依赖示例代码中的类名。

## Verify It | 验证

> **【中文解读】** 验收清单逐条过：形似前缀的命名空间被精确边界拒绝；只有官方命名空间的 Registry 状态能让版本合格；未验证或不匹配的包与远程证据被拒绝；发布者元数据冒充不了 Registry 管理元数据；工具顺序被规范化但不掩盖描述符变化；畸形的包和工具结构安全拒绝；`serverInfo` 始终只是诊断、不提供准入权威；描述符漂移会隔离、停用并封锁该 pin 的回滚；状态变化隔离活跃 pin；回滚选不出被隔离或未知的版本；账本篡改被检测到。

Run the demonstration and the deterministic suite:

```bash
cd phases/13-tools-and-protocols/30-mcp-registry-supply-chain-and-drift
python3 code/main.py
python3 -m unittest discover -s code/tests -v
```

Verification should prove:

- exact namespace boundaries reject lookalike prefixes
- only the official namespaced Registry status can make a version eligible
- unverified or mismatched package and remote evidence is rejected
- publisher metadata cannot impersonate Registry-managed metadata
- tool ordering is normalized without hiding descriptor changes
- malformed package and tool structures refuse safely
- `serverInfo` remains diagnostic and never supplies admission authority
- descriptor drift quarantines, deactivates, and blocks rollback to the pin
- status changes quarantine active pins
- rollback cannot select a quarantined or unknown version
- ledger tampering is detected

## Production Failure Modes | 生产失败模式

> 下表三列：失败、为什么发生、必需的响应。最贵的三行：同一包坐标返回了新字节（可变上游或被攻陷的分发渠道——停止激活、保留两份摘要、调查抓取边界）；回滚目标从未通过准入（路由控制与审批状态脱节——拒绝回滚、对目标重新准入）；账本被整体重写后仍本地通过（哈希链没有外部锚点——把签名账本头发布到独立信任域）。

| Failure | Why it happens | Required response |
|---|---|---|
| Name looks valid but namespace was never authenticated | Policy trusted record text | Reject until a trusted namespace verifier supplies the exact prefix |
| Same package coordinate returns new bytes | Mutable upstream or compromised distribution | Stop activation, retain both digests, investigate the fetch boundary |
| “Latest” changes without review | Floating selection escaped the pin | Resolve only exact admitted versions and digests |
| New tool appears after approval | Runtime drift or a different deployment | Quarantine the route and capture a fresh descriptor observation |
| Deprecated version remains active | Status sync is missing or delayed | Reconcile status on a schedule and before activation |
| Deleted record disappears from default sync | Client requested only active records | Use incremental or deleted-aware reconciliation and preserve local history |
| Rollback target was never admitted | Route control and approval state are disconnected | Refuse rollback and run a new admission for the target |
| Ledger verifies locally after an attacker rewrites all entries | Hash chain has no external anchor | Publish signed ledger heads to a separate trust domain |
| Evidence contains bearer tokens or tool arguments | Logging copied whole requests | Redact at collection time and store only the minimum proof |

## Operational Rule | 运维准则

Publication answers “can this identity publish this name?” Admission answers “will we execute this exact artifact and expose this exact behavior?” Keep those decisions separate, pin every join, and make rollback choose evidence rather than memory.

> 发布回答的是"这个身份可以发布这个名字吗？"准入回答的是"我们会执行这个精确的制品、暴露这个精确的行为吗？"把这两个决策分开，锁定每一次拼接，让回滚基于证据而不是记忆做选择。

## Further Reading | 延伸阅读

- [Official Registry server.json requirements](https://github.com/modelcontextprotocol/registry/blob/main/docs/reference/server-json/official-registry-requirements.md)
- [Official Registry OpenAPI contract](https://registry.modelcontextprotocol.io/openapi.yaml)
- [MCP 2026-07-28 server discovery](https://modelcontextprotocol.io/specification/2026-07-28/server/discover)
