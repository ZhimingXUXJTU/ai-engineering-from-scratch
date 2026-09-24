# MCP 注册中心供应链：准入、漂移与回滚

> 注册中心条目只告诉你"发布者声明了什么"。生产准入要证明的是：你实际取回了什么、观察到了什么、审批了什么、以及能安全恢复到什么。

> **【中文解读】** 本课把 MCP 服务器的供应链拆成命名空间、记录、执行来源、运行时、准入、运维六个边界，每个边界都要求可验证的证据，最终落地为一个防篡改的准入账本和一个只选已准入版本的可回滚路由。基于 MCP 2026-07-28 规范的 `server/discover` 与官方 Registry 的 `server.json` 契约。

> 🔗 **【前置】** 学本课前请先掌握：Phase 13 · 17（网关与注册中心——官方 Registry 的命名空间验证、网关在架构中的位置）和 Phase 13 · 18（生产认证——OAuth 2.1 与凭证治理）。本课是这两课的运维延伸：一个 MCP 服务器进入生产之前，证据链如何审批、安装之后漂移如何被发现、出事之后路由如何回滚。

**类型：** 动手实践
**语言：** Python
**前置条件：** Phase 13 · 17（网关与注册中心）、Phase 13 · 18（生产认证）
**预计用时：** 约 90 分钟

## 学习目标

- 区分 Registry 发布、包来源证明（provenance）、运行时发现与本地审批这四件事。
- 在不信任记录内部自带名字的前提下，验证 MCP 服务器的命名空间。
- 锁定（pin）不可变的发布记录、执行来源、来源证明与在线描述符证据。
- 在准入之后检测注册中心状态变化与运行时漂移（drift）。
- 把路由回滚到一个此前已通过准入的版本，且不改写历史。
- 维护一个防篡改（tamper-evident）的准入账本（ledger），能解释每一次决策。

## 问题引入

你在注册中心里找到了 `com.example/inventory`。它的描述看着没问题，包也存在，服务器也响应了 `server/discover`。

> **【中文解读】** "它在注册中心里"并不是一个事实，而是四条来自不同权威方的事实链：发布者认证、包注册中心交付、运行端点自述、组织审批。把它们压扁成"在注册中心里所以可信"，就是供应链盲区的起点。这和 npm/PyPI 依赖进入生产是同一个问题，只是 MCP 服务器还会在安装之后继续变化（工具漂移），所以证据链必须延伸到运行时。

这不是一个事实，而是来自不同权威方的一条事实链：

1. 一个通过了命名空间认证的发布者提交了记录。
2. 一个包注册中心交付了具有特定身份和摘要（digest）的制品。
3. 一个运行中的端点报告了协议版本、能力、工具列表和诊断性服务器信息。
4. 你的组织决定"恰好这个组合"被允许。

把这些事实压扁成"它在注册中心里，所以可信"，就制造了一个供应链盲区。一条有效的发布记录仍可能被标记为 deprecated；如果你不锁定摘要，包标签可能指向意料之外的制品；服务器可能在评审之后新增一个破坏性工具；回滚可能悄悄选中一个从未通过准入的版本。

修复方式是一个在每个边界都留下证据的准入控制器（admission controller）。

## 注册中心是索引，不是你的审批系统

官方 MCP Registry 存储的是服务器元数据。它的 `server.json` 记录为一个服务器版本命名，并声明一个或多个包或远程端点。发布规则额外提供命名空间认证、包所有权检查、受限的注册中心规则，以及一个狭窄的发布者元数据存放位置。

这些控制回答的是"发布"问题。你的生产策略仍然要自己回答"部署"问题：

| 边界 | 问题 | 证据持有方 |
|---|---|---|
| 命名空间 | 发布者有权使用这个名字吗？ | Registry 认证加你验证过的命名空间输入 |
| 记录 | 发布者为这个版本声明了什么？ | 不可变的 `server.json` 摘要 |
| 执行来源 | 实际执行的是哪个包或远程端点？ | 声明的来源字段、已验证的所有权结果、transport 与可信摘要 |
| 运行时 | 端点现在暴露什么？ | `server/discover` 与工具描述符 |
| 准入 | 你的策略是否恰好批准了这一组？ | 本地 pin 与账本条目 |
| 运维 | 它现在还安全吗？坏了拿什么替换？ | 漂移检查、状态同步、健康检查与回滚路由 |

> 💡 **【类比】** Registry 像手机应用商店的"上架审核"，你的准入系统像企业的 MDM（移动设备管理）装机审批。App 通过商店审核只说明"发布者身份合规、包没被偷换"，不代表"你的公司允许在办公设备上运行它"。npm/PyPI 与企业内部 Artifactory + 审批流的关系也是同样的分工：注册中心是索引，审批权永远在你自己手里。

Registry 的 schema 版本与 MCP 协议版本是相互独立的。一条记录可能使用已发布的 `2025-12-11` 服务器 schema，而在线服务器支持的是 MCP `2026-07-28`。永远不要从其中一个推断另一个。

```figure
mcp-registry-admission
```

> **【中文解读】** 六个边界、六个问题、六个证据持有方——没有任何一行是"Registry 替你担保"。最容易被忽视的是"执行来源"与"运行时"两行：前者问的是实际跑起来的到底是哪个制品（不是发布者说跑哪个），后者问的是此刻真正暴露的工具面（不是评审那天看到的）。

## 一次准入决策中的七项控制

> **【中文解读】** 一次安全的准入要把七个控制点串成一个决策：(1) 命名空间验证——发布者是否真有权用这个名字；(2) 来源拼接（provenance join）——声明的包与实际取回的制品在多个字段上对得齐；(3) 锁定决策而非只锁版本——pin 里要有各层摘要；(4) 在线漂移检测——对将真正接流量的服务器做发现并比对工具描述符；(5) 注册中心状态是活状态——active/deprecated/deleted 要持续同步；(6) 回滚即路由恢复——只选已准入且当前合格的目标；(7) 追加式准入账本——哈希链让历史可验证。下面七个小节逐个展开。

### 1. 命名空间验证

官方 Registry 的名字使用经过认证的命名空间。一个已验证的域可以映射为反转的域名前缀。例如，对 `example.com` 的控制权可以确立 `com.example/*`。

不要接受字符串前缀检查：

```python
server_name.startswith("com.example")
```

这个前缀检查也会放行 `com.exampleevil/tool`。正确的做法是按 `/` 切分名字、要求 slug 非空，并对命名空间段做精确比较。更重要的是，要把认证结果中验证过的命名空间传入准入流程——不要从未被信任的记录自身推导信任。

GitHub 背书的命名空间和域名背书的命名空间走不同的认证路径。把两种路径都归一化成同一个准入输入：精确的、已验证的命名空间字符串。

### 2. 来源拼接

对于包记录，声明与取回的制品必须在这些显式字段上拼接对齐：

- 包注册中心类型
- 包标识符
- 包版本
- 已验证的所有权结果
- 下载制品的摘要

还要校验声明中包的 transport。一条只带远程端点的记录同样合法，不能因为"没有包"而被拒绝。对于远程来源，要把声明的 URL 和 transport 类型，与独立验证过的端点所有权、以及可信连接或部署证据的摘要拼接在一起。

本课代码同时支持两种来源类型，并把选中的来源与 Registry 来源、服务器名、Registry 版本、记录摘要和证据摘要一起哈希。得到的 provenance 摘要是指向完整证据集的紧凑指针，但不能替代保留证据本身。

永远不要接受仅由"你正要验证的那个制品"自己提供的摘要。要么在可信的抓取边界上自行计算，要么从一个其验证结果会被你校验的包服务获取。

> **【中文解读】** 来源拼接的核心原则：每一层证据都来自一个独立于被验证对象的权威方。发布者声明包坐标，包注册中心交付制品并证明所有权，你的抓取边界计算摘要——三者互相咬合，任何一方单方面说谎都会在拼接处断裂。

### 3. 锁定决策，而不只是版本

Registry 版本是唯一的发布标识符。已发布的元数据不可变；记录要变就必须发新版本。推荐语义化版本，但 Registry 既不强制，也不接受版本范围。

这意味着 `^1.4` 不是准入 pin，"latest"（最新）也不是。一个有用的 pin 应包含：

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

锁定多个层次，你才能定位是哪个边界变了：Registry 版本没变而记录摘要变了，是 Registry 完整性故障；包坐标或远程部署没变而来源摘要变了，是执行来源完整性故障；工具集摘要变了，就是运行时漂移。多层 pin 的价值不在于"锁得住"，而在于报警时能精确指认失守的那一层。

### 4. 在线漂移检测

准入应当观察那个将真正接收流量的服务器。调用 `server/discover`，通过你的可信路径列出或以其他方式取得暴露的工具描述符，然后验证：

- `2026-07-28` 在 `supportedVersions` 里
- 所有本地必需的能力都在
- 每个工具描述符具备要求的身份与 schema 结构
- 后续检查中，规范化后的描述符摘要与准入 pin 一致

可选结果 `_meta["io.modelcontextprotocol/serverInfo"]` 的值是服务器自述的展示、日志与调试上下文。把它记为诊断证据可以，但绝不能用它来确立命名空间、包所有权、端点所有权、准入或任何其他安全决策。`_meta` 之外的 `serverInfo` 直接别名不是契约字段，不应升级为诊断证据。

只对"顺序无意义"的字段做规范化。示例在哈希前按稳定名称对工具列表排序，这样无害的列表顺序变化不会触发漂移告警；但它不丢弃描述符字段——新增工具、schema 变化、描述变化或新增 annotations，都会改变 pin。

示例把畸形描述符和任何描述符摘要变化都当作漂移：隔离（quarantine）该 pin、摘除其活跃路由、并把这个版本拉入回滚黑名单。生产策略若要放行一处"编辑性改动"，只能走一次新的评审——因为描述会影响模型的工具选择。"纯外观"元数据也能改变 agent 行为。

> **【中文解读】** 第 4 项控制是全课的核心洞察：供应链审查不是一次性动作。服务器审查通过之后、运行之中，工具面还可能变化——这就是运行时漂移。对策是"描述符摘要"这个锚点：准入时算一次、此后每次巡检再算一次，任何差异即隔离加摘路由。特别注意：工具描述文本的变化也要算漂移，因为它直接影响 LLM 选不选这个工具。

### 5. 注册中心状态是活状态

Registry API 在每条服务器记录旁附带一个响应级 `_meta` 对象。Registry 管理的字段位于 `_meta["io.modelcontextprotocol.registry/official"]` 之下。把响应的 `_meta` 对象传入准入流程，读取 `_meta["io.modelcontextprotocol.registry/official"].status`。直接的 `_meta.status` 值不是官方线格式。不要把响应元数据与发布记录自身的 `_meta` 混为一谈。状态可以是：

- `active`：默认返回，可进入本地准入
- `deprecated`：仍可被发现但带警告，不再是安全的自动选择
- `deleted`：默认隐藏，但历史记录仍可通过 deleted 或增量视图获取

准入之后要持续同步状态。如果一个 active 版本变成 deprecated 或 deleted，就隔离它的 pin、停止把新工作路由给它。但证据要保留——从默认列表中消失，并不是让你抹掉审计轨迹的许可。

发布者自定义的元数据只能放在发布记录的 `_meta.io.modelcontextprotocol.registry/publisher-provided` 之下。Registry 管理的响应元数据与之分离。绝不让发布者自己设置自己的官方状态。

### 6. 回滚即路由恢复

回滚不会去改写不可变的发布记录。回滚是选中一个此前已准入、当前仍合格的 pin，然后切换活跃路由。

安全的回滚目标必须：

1. 有一条完整的准入记录。
2. 在你的策略下 Registry 状态仍是 active。
3. 没有被运行时或安全证据隔离。
4. 仍能解析到 pin 住的包和在线描述符集。
5. 通过当前健康检查。

示例聚焦前三个条件。真实的 reconciler 在激活之前还应重新抓取包并复查在线端点。

### 7. 追加式准入账本

准入数据库说的是"现在什么在活跃"；账本（ledger）解释的是"为什么"。

示例的每条账目包含序号、时间、事件、服务器、版本、结论、原因、证据、前一条目的哈希以及自身的哈希。改动任何一条旧结论，都会让该条目以及其后所有链上条目的校验失败。

这是"可证篡改"（tamper-evident），不是神奇的"防篡改"（tamper-proof）。要周期性地把账本头锚定到一个独立的信任域，例如签名的发布元数据或一次写入存储。限制谁可以追加账目。授权 token、包凭证、工具参数和私有端点数据一律不得进入证据。

> **【中文解读】** 数据库与账本的分工值得记住：数据库回答"现在哪个版本活跃"，账本回答"当时为什么批准、依据哪些证据"。哈希链只能证明"历史没有被悄悄改过"，证明不了"写历史的人没骗你"——所以需要限制追加权限，并把账本头锚定到外部信任域。

## 动手实现

可运行的控制器在 `code/main.py`，只使用 Python 标准库。

先跑有限演示：

```bash
cd phases/13-tools-and-protocols/30-mcp-registry-supply-chain-and-drift
python3 code/main.py
```

演示的五个操作：

1. 准入 `1.0.0`（命名空间、包 provenance、协议、能力、工具全部匹配）。
2. 准入 `1.1.0` 并设为活跃。
3. 运行时观察到一个意外的 delete 工具。
4. 观察 Registry 把 `1.1.0` 的状态改为 `deprecated`。
5. 把路由恢复到仍处于已准入状态的 `1.0.0` pin。

预期输出形状：

```json
{
  "admitted": [true, true],
  "driftAllowed": false,
  "rollbackAllowed": true,
  "activeVersion": "1.0.0",
  "ledgerValid": true
}
```

按以下顺序阅读实现：

1. `namespace_for_domain()` 与 `namespace_matches()` 确立精确的命名权威。
2. `digest()` 与 `normalized_tools()` 产生确定性证据。
3. `RegistryAdmissionController.admit()` 拼接发布、来源、运行时与策略。
4. `check_live()` 把新观察与 pin 比对。
5. `observe_registry_status()` 隔离 Registry 状态变化的版本。
6. `rollback()` 只激活一个此前已准入且合格的目标。
7. `AdmissionLedger.verify()` 检测被改动的记录历史。

## 用框架实现

把准入控制器放在发现（discovery）与路由（routing）之间：

```text
Registry sync -> artifact verifier -> live discovery -> admission controller -> route table
                                               |                 |
                                               v                 v
                                          evidence store    admission ledger
```

为这些工作使用相互分离的身份。Registry 同步 worker 只需要元数据读取权限；制品验证器只需要包抓取权限；路由 reconciler 只需要激活已批准 pin 的权限。没有一个角色需要持有全部凭证——最小权限原则在供应链流水线里同样成立。

让发布状态显式化："Approved"（已批准）表示证据通过了策略；"Active"（活跃）表示路由当前选中的是它；"Quarantined"（已隔离）表示它不能再接收新工作；"Superseded"（已被取代）表示另一个已准入版本处于活跃。不要把这四层含义塞进一个布尔值。

在把服务器暴露进 `tools/list` 之前先完成准入。否则客户端可能在"已发布"与"策略已评估"之间的空窗期里发现并调用一个工具。

> **【中文解读】** 三个生产化要点：流水线各环节用独立身份（防一个组件失陷即全线失守）；发布状态用四个词而非一个布尔（Approved/Active/Quarantined/Superseded 各有含义）；准入必须先于 `tools/list` 暴露（堵住发布与审批之间的发现空窗）。这条 text 图里的 evidence store 与 admission ledger 正是第 7 项控制的两类持久化产物。

## 交互实验

你将逐个观察每个边界是如何失效的。

### 实验 A：命名空间碰撞

在 code 目录打开 Python shell：

```bash
cd phases/13-tools-and-protocols/30-mcp-registry-supply-chain-and-drift/code
python3 -q
```

然后运行：

```python
from main import namespace_matches
namespace_matches("com.example/inventory", "com.example")
namespace_matches("com.exampleevil/inventory", "com.example")
```

第一个结果是 `True`，第二个是 `False`。在本地把精确比较换成 `startswith`，观察第二个名字为什么能越过边界。继续之前记得恢复精确比较。

### 实验 B：描述符漂移

```python
from main import *
times = iter(f"2026-08-21T12:00:{n:02d}+00:00" for n in range(10))
c = RegistryAdmissionController(clock=lambda: next(times))
meta = {OFFICIAL_META_KEY: {"status": "active"}}
c.admit(sample_record("1.0.0"), meta, "com.example", evidence_for("1.0.0"), sample_live("1.0.0"))
c.check_live("com.example/inventory", "1.0.0", sample_live("1.0.0", True))
```

检查 reasons 和路由状态：包与 Registry 记录都没变，变的是运行时工具面——于是控制器隔离并停用了这个 pin。这就是供应链控制必须在安装之后继续存在的原因。

### 实验 C：状态与回滚

准入 `1.1.0`，把它标记为 deprecated，然后尝试两个回滚目标：

```python
c.admit(sample_record("1.1.0"), meta, "com.example", evidence_for("1.1.0"), sample_live("1.1.0"))
c.observe_registry_status("com.example/inventory", "1.1.0", "deprecated")
c.rollback("com.example/inventory", "1.1.0", "unsafe retry")
c.rollback("com.example/inventory", "1.0.0", "restore known release")
c.ledger.verify()
```

被隔离的回滚目标被拒绝；更早的活跃 pin 被接受；账本校验仍然通过。

## 进阶练习

给控制器扩展一道双人审批门（two-person approval gate）。

要求：

- 把审批存储为签名证据引用，而不是 pin 里可变的名字。
- 工具集里出现带 `destructiveHint: true` 的工具时，要求两个不同的评审身份。
- 拒绝重复的评审身份。
- 审批未完成时，把最初的准入尝试保留在账本里。
- 为零个、一个、重复、两个不同审批各加测试。
- 不记录签名、凭证或完整的私有工具参数。

成功的标准：在两个身份都批准了那条精确的记录摘要、包摘要和工具集摘要之前，破坏性工具不可能进入活跃状态。

> **【中文解读】** 这道练习把第 7 项控制升级为"破坏性工具必须两人审批"——相当于双人规则（two-person rule）：单人失陷或单人失误都不足以把"可以删除东西的工具"送进生产。注意审批存的是签名证据引用而不是名字，防止事后改名字冒充审批人。

## 产出物

本课附带 `outputs/skill-mcp-registry-admission.md`。在评审一个新的 Registry 版本或调查漂移时，把它当作一份扁平、可复用的 runbook 使用。它定义了输入、拒绝规则、证据包、状态对账与回滚证明，且不依赖示例代码中的类名。

## 验证

运行演示与确定性测试套件：

```bash
cd phases/13-tools-and-protocols/30-mcp-registry-supply-chain-and-drift
python3 code/main.py
python3 -m unittest discover -s code/tests -v
```

验证应证明：

- 精确的命名空间边界拒绝形似的前缀
- 只有官方命名空间的 Registry 状态能让一个版本合格
- 未验证或不匹配的包与远程证据被拒绝
- 发布者元数据无法冒充 Registry 管理的元数据
- 工具顺序被规范化，但不掩盖描述符变化
- 畸形的包与工具结构安全拒绝
- `serverInfo` 始终只是诊断，不提供准入权威
- 描述符漂移会隔离、停用并封锁该 pin 的回滚
- 状态变化隔离活跃 pin
- 回滚选不出被隔离或未知的版本
- 账本篡改被检测到

## 生产失败模式

| 失败 | 为什么发生 | 必需的响应 |
|---|---|---|
| 名字看着合法但命名空间从未认证 | 策略信任了记录文本 | 拒绝，直到可信的命名空间验证方给出精确前缀 |
| 同一包坐标返回了新字节 | 可变上游或被攻陷的分发渠道 | 停止激活，保留两份摘要，调查抓取边界 |
| "latest" 未经评审就变了 | 浮动选择逃出了 pin | 只解析精确的已准入版本与摘要 |
| 审批之后出现新工具 | 运行时漂移或另一个部署 | 隔离路由并抓取新的描述符观察 |
| deprecated 版本仍然活跃 | 状态同步缺失或延迟 | 按计划并在激活前对账状态 |
| deleted 记录从默认同步中消失 | 客户端只请求了 active 记录 | 使用增量或 deleted 感知的对账，并保留本地历史 |
| 回滚目标从未通过准入 | 路由控制与审批状态脱节 | 拒绝回滚并对目标重新准入 |
| 攻击者重写全部条目后账本仍本地通过 | 哈希链没有外部锚点 | 把签名账本头发布到独立信任域 |
| 证据里含有 bearer token 或工具参数 | 日志复制了完整请求 | 在采集时脱敏，只存最小证明 |

> **【中文解读】** 这张表按"失败→响应"组织，可直接当供应链 on-call 手册用。共同主线：每一行都是"某条证据缺位或被绕过"——所以响应几乎都是"补证据、堵边界"，而不是"改配置重启"。

## 运维准则

发布回答的是"这个身份可以发布这个名字吗？"准入回答的是"我们会执行这个精确的制品、暴露这个精确的行为吗？"把这两个决策分开，锁定每一次拼接，让回滚基于证据而不是记忆做选择。

> **【中文解读】** 一句话总结全课：Registry 管发布，你管执行。两者之间靠多层 pin 和追加式账本连接，漂移检测保证连接持续有效，回滚保证断开时有着落。

## 延伸阅读

- [Official Registry server.json requirements](https://github.com/modelcontextprotocol/registry/blob/main/docs/reference/server-json/official-registry-requirements.md)：官方 Registry 对 `server.json` 记录的发布要求——命名空间认证、包所有权与受限规则。
- [Official Registry OpenAPI contract](https://registry.modelcontextprotocol.io/openapi.yaml)：Registry API 的 OpenAPI 契约，含响应级 `_meta` 与状态字段的线格式。
- [MCP 2026-07-28 server discovery](https://modelcontextprotocol.io/specification/2026-07-28/server/discover)：`server/discover` 与诊断性 `serverInfo` 的规范原文。
