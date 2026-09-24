# 门,漂移和滚动

> 编辑录制证明你收到的内容,你观察到的内容,你批准的内容,以及你可以安全地恢复的内容.

> **【中文解读】**注册中心条目只告诉你"发行者声明了什么";生产准入) 证明是"你实际取回了什么,观察了什么,批准了什么以及能安全恢复到什么"――本课程将MCP服务器的供应链拆分成命名空间,记录,执行来源,运行时间,进入,运营维护六个边界,每个边界都要求可验证的证据,最终落地为一个防改的准入账本和一个只选择的准入版本的可回路.

>  **【前置】**学本课前请先掌握:第13阶段 · 17期网关与注册中心官方登记库的命名空间验证、网关在架构中的位置) 和第13期 · 18期生产认证OAuth 2.1与凭证治理) ⋅本课是这两课的运维延伸:一个MCP 服务器进入生产之前,证链如何审批、安装后漂移如何被发现、如何滚滚之后. 本课基于MCP 2026-07-28 规范的`server/discover`,我知道.

**Type:** Build | **类型:** 动手实践
**Languages:** Python | **语言:** Python
**Prerequisites:** Phase 13 · 17 (gateways and registries), Phase 13 · 18 (production authentication) | **前置知识:** Phase 13 · 17（网关与注册中心）、Phase 13 · 18（生产认证）
**Time:** ~90 minutes | **时间:** 约 90 分钟

## 学习目标

- 单独的登记库发布,包装来源,运行时间发现和当地批准.
  中文翻译:区分登记 发布、包来源证明 (来源) 、运行时发现与本地审批这四件事――
- 检查一个MCP服务器名字空间,而不需要相信其名字在自己的记录中.
  中文翻译:在不信任记录内部自带名字的前提下,验证MCP 服务器的命名空间──
- 标签不可变的出版物,执行源,来源,现场描述符证据.
  中文翻译:锁定(pin)不可变的发布记录、执行来源、来源证明与在线描述符证据──
- 检测登记状态变化和录取后运行时间漂移.
  中文翻译:在准入后检测注册中心状态变化与运行时漂移 (漂移) .
- 转换路由到之前被允许的版本,而不需要重写历史.
  中文翻译:把路由回滚到一个已通过的版本,并且不改写历史.
- 保持一个明确的录取账本,解释每一个决定.
  中文翻译:维护一个防改 (防改) 的准入账本 (准入账本) 账本 (账本),能解释每一次决策.

## 问题 问题引入

你发现了`com.example/inventory`文件的描述是正确的,包裹存在,服务器回答了.`server/discover`现在,我们要去.

> 你在注册中心找到了`com.example/inventory`◎ 描述: 没有问题,包也存在,服务器也响应了`server/discover`,我知道.

> **【中文解读】**"它在注册中心"不是一个事实,而是来自不同权威的四条事实链:发行人认证"",包注册中心交付"",运行端点自述"",组织审批"",把它们压成"在注册中心里所以可信",就是供应链盲区的起点.

这不是一个事实,而是来自不同当局的数据链.

1. 发行商认证一个名字空间提交了记录.
2. 一个包装登记库提供了一个具有特定身份和消化的文物.
3. 运行终端报告了协议版本,功能,工具和诊断服务器信息.
4. 你的组织决定允许这种结合.

> 这不是一个事实,而是来自不同权威方的一个事实链: 1) 一个通过命名空间认证的发行人提交记录; 2) 一个包注册中心交付具有特定身份和摘要的产品; 3) 一个运行端点报告协议版本;

倒这些事实到"它"是注册表中的,所以相信它会造成供应链盲点.一个有效的出版物仍然可以被废除.如果您不将其结,包装标签可以指向一个意想不到的文物.服务器可以在审查后添加破坏性工具.滚动可以默默地选择一个未被承认的版本.

> 把这些事实压成"它在注册中心,所以可信",就创造了一个供应链盲区. 一条有效的发布记录可能被标记为过时;如果你不锁定摘要,包标可能指向意料之外的产品;服务器可能在审核后添加一个破坏性的工具;回滚可能选中一个从未通过的版本.

检查员在每一个边界都有证据.

> 修复方式是一个在每个边界都留下证据的准入控制器 (准入控制器) .

## 登记是指数,不是你的审批系统.

官方MCP登记处存储服务器的元数据.`server.json`记录服务器版本名称,并声明一个或多个包或远程终端点. 出版规则增加名称空间认证,包所有权检查,限制登记规则和狭窄的出版商元数据位置.

> 官方MCP注册表存储的是服务器元数据.`server.json`记录一个服务器版本命名,并声明一个或多个包或远端点. 发布规则额外提供命名空间认证,包所有权检查,有限的注册中心规则以及一个狭窄的发行商数据存储位置.

您的生产政策仍然回答部署问题:

> 这些控制回答是"发布"问题.

| Boundary | Question | Evidence owner |
|---|---|---|
| Namespace | Was the publisher allowed to use this name? | Registry authentication plus your verified namespace input |
| Record | What did the publisher declare for this version? | Immutable `server.json` digest |
| Execution source | Which package or remote endpoint will execute? | Declared source fields, verified ownership result, transport, and trusted digest |
| Runtime | What does the endpoint expose now? | `server/discover` and tool descriptors |
| Admission | Did your policy approve this exact set? | Local pin and ledger entry |
| Operations | Is it still safe, and what can replace it? | Drift checks, status sync, health, and rollback route |

> **【中文解读】**这张表是全课的骨架:六边界,每个边界一个问题,一个证据持有人.`server.json`摘要),执行来源问"实际执行会是哪个包或端点",运行时问"端点现在暴露什么" (证据是)`server/discover`准入问"你的策略是否恰好批准了这个组",运维问"它现在还安全吗"",坏了拿什么替换了"......注意证券持有人不同没有任何一行是"注册表替你保证"――

>  **【类比】**登记器 像手机应用商店的"上架审核",你的入门系统像企业的MDM(移动设备管理) 装机审核.

登记方案版本和MCP协议版本是独立的.`2025-12-11`现场服务器支持MCP `2026-07-28`永远不要把一个推断到另一个.

> 登记器的方案版本与MCP协议版本是相互独立的.`2025-12-11`服务器方案,而在线服务器支持的是MCP`2026-07-28`永远不要从一个推断到另一个.

```figure
mcp-registry-admission
```

## 七个控制在一个接入决定中的七个控制

> **【中文解读】**一次安全准入将七个控制点串成一个决策: 1) 命名空间验证发布者是否真正有权使用这个名称; 2) 来源拼音: 源联) 声明包与实际取回的产品在多个段落上与齐齐; 3) 锁定决策而不是仅锁版本pin 里需要有各层次的摘要; 4) 在线漂移检测对将真正接流的服务器进行发现与工具描述符; 5) 注册中心状态是活状态动/衰退/删除必须持续同步; 6) 回滚路由恢复选准入和当前合格目标; 7) 额外准入账本哈哈链历史让验证;

### 1. 命名空间验证

官方注册名字使用验证的名称空间.一个验证的域名可以映射到一个倒置域名前.例如,控制`example.com`能确定`com.example/*`现在,我们要去.

> 官方登记名字使用经过认证的命名空间──已验证的域名可以被映射为反转域名──例如,对`example.com`控制权可以建立`com.example/*`,我知道.

没有接受字符串前置检查:

```python
server_name.startswith("com.example")
```

这也可以接受.`com.exampleevil/tool`分别在`/`需要一个不空的字符串,并精确地比较名字空间段. 更重要的是,通过验证名字空间进入认证结果.不要从不值得信赖的记录中获得信任.

> 这次检查也会放行.`com.exampleevil/tool`正确的做法是按`/`切分名字、要求非空,并对命名空间段做精确比较. 更重要的是,要把验证结果中验证的命名空间传入进入流程不要从来没有被信任的记录自行推导信任.

支持GitHub的名字空间和域名空间使用不同的身份验证路径.将任何路径都正常化为一个输入:确切验证的名字空间字符串.

> 基特哈布 背书的命名空间和域名背书的命名空间走不同认证路径──把两种路径归结为一个准入输入:精确的、已验证的命名空间字符串──

### 2. 亲属加入

对于包装记录,声明和采集的文物必须在明确的字段上结合:

- 包装登记类型
- 包装标识符
- 包装版本
- 经验证的所有权结果
- 下载的文物消化

> 对于包记录,声明和取回的产品必须在这些明显字段上拼写对齐:包注册中心类型、包标识符、包版本、已验证的所有权结果、下载的产品摘要──任何一个字段对不上,这个条款的来源链就是断定的──

确认声明的包运输.仅有一个远程终端点的记录是有效的,不能因为缺乏包而拒绝.对于远程源,将声明的URL和运输类型加入独立验证的终端点所有权和可信的连接或部署证据.

> 对于远程来源,要将声明的URL和运输类型,与独立验证的端点所有权以及可信连接或部署证据的摘要拼接在一起.

课程代码支持源类型,并将选定的源源与注册表源,服务器名称,注册表版本,记录消化和证据消化一起哈希.结果的来源消化是完整的证据集的紧指针.它不是保留证据的替代品.

> 本课程代码同时支持两种来源类型,并将选中的来源与注册表来源,服务器名称,注册表版本,记录摘要和证据摘要一起哈希.

永远不要接受只通过你试图验证的文物提供的化, 计算在一个可信的收货界限, 或从一个你验证的验证结果的包装服务中收到它.

> 永远不要只接受自己提供的摘要,即"你正在验证的产品".

### 3. 定决策,不仅仅是版本,而不是只是版本.

登记版本是唯一的出版标识符. 发表的元数据是不可变的. 改变的记录需要一个新的版本. 推语义版本化,但登记程序不需要它,也不接受版本范围.

> 登记版是唯一的发布标识符.已发布的元数据不可变;记录要变就必须发出新版本.

这意味着`^1.4`最新                                                                                                                                                                                                                                                             

> 这意味着`^1.4`不准入,"最新"也不是.

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

通过将多层粘贴,可以确定哪个界限发生了变化.在同一注册表版本下发生的记录消化变化是注册表完整性失败.在同一包坐标或远程部署下发生的源消化变化是执行源完整性失败.工具集消化变化是运行时间漂移.

> 锁定多层次,你才能定位是哪个边界变化:注册表 版本不变而记录摘要变化,是注册表 完整性故障;包坐标或远程部署不变而来源摘要变化,是执行来源完整性故障;工具集摘要变化,就是运行时漂移.多层的价值不在于"锁定住",而在报警时可以精确识别失败的层面.

### 4. 现场漂移检测

接收者应该观察实际接收流量的服务器.`server/discover`通过您的可信路径列出或以其他方式获取暴露的工具描述符,并验证:

> 准入应观察将真正接收流量服务器.调用.`server/discover`通过您可信的路径列出或以其他方式获得暴露的工具描述符,然后验证:

- `2026-07-28`现在`supportedVersions`
- 现有所有本地要求的能力
- 每个工具描述器都有所需的身份和方案表面
- 标准化描述器消化与后检验中被允许的匹配

> 验证四件事:`2026-07-28`在`supportedVersions`里;(2) 所有本地必需能力都在;(3) 每个工具描述符都有要求的身份和方案结构;(4) 后续检查中,规范化后的描述符摘要和准入 一致.

选择性结果`_meta["io.modelcontextprotocol/serverInfo"]`值是自主报告的显示,日志和调试文本. 记录它作为诊断证据,但永远不要使用它来确定名字空间,包所有权,终端点所有权,录取或任何其他安全决定.`serverInfo`别名:外面`_meta`没有合同领域,不应被推广为诊断证据.

> 可选结果`_meta["io.modelcontextprotocol/serverInfo"]`值是服务器自述的展示,日志和调试下文. 记得它作为诊断证据,但绝不能使用它来确定命名空间,包所有权,端点所有权,准入或任何其他安全决策.`_meta`之外的`serverInfo`直接别名不是契约字段,不应升级为诊断证据.

标准化仅仅是没有意义的字段.样本在哈希之前按稳定名称排序工具列表,因此无害的列表序变化不会导致漂移.它不会丢弃描述字段.新工具,改变方案,改变描述或新注释改变了.

> 仅对"顺序无意义"的字段进行规范化. 例如在哈希前按稳定名称对工具列表排序,这样无害的列表顺序变化不会触发漂移告警;但它不会丢弃描述符字段新增工具、方案 变化、描述变化或新增注释,都会改变点.

样本将错误的描述符和任何描述符消化变化视为漂移,隔离,删除其活跃路线,并将该版本作为反弹目标.生产政策只允许通过新的审查进行编辑变化,因为描述影响模型工具选择.

> 示例把形描述符和任何描述符摘要变化都当作漂移:隔离(隔离) 这个,摘除其活跃路由、并把这个版本拉入回滚黑单――生产策略如果要放出"编辑性改动",只能走一次新的评审因为描述会影响模型的工具选择――"纯外观"元数据也可以改变代理行为――

> **【中文解读】**第四节控制是全课的核心洞察:供应链审查不是一次性动作. 服务器审查通过后,在运行中,工具面也可能变化.

### 5. 登记中心状态是现实状态

登记器API附加响应级别`_meta`文件的管理范围在 文件中.`_meta["io.modelcontextprotocol.registry/official"]`通过答案`_meta`反对录取和阅读`_meta["io.modelcontextprotocol.registry/official"].status`直接的`_meta.status`答案的元数据与出版记录的元数据不要混为一谈`_meta`状态可以是:

> 登记API 在每个服务器记录旁附带一个响应级`_meta`对象──登记管理的字段位于`_meta["io.modelcontextprotocol.registry/official"]`之下. 响应的`_meta`象传入入流程,读取`_meta["io.modelcontextprotocol.registry/official"].status`直播`_meta.status`值不是官方线程格式. 不要把响应数据与发布记录本身的`_meta`混为一谈.状态可以是:

- `active`: 违约返回,可接受本地接入
- `deprecated`虽然可以通过警告发现,但不再是安全的自动选择
- `deleted`:默认隐藏,而其历史记录仍然可通过删除或增量查看

> 三种状态:`active`(默认返回,可进入本地准入)`deprecated`(仍可发现,但警告,不再是安全的自动选择)`deleted`(默认隐藏,但历史记录仍然可通过删除或增量视图获取)

录取后同步状态. 如果一个活跃版本变得过时或删除,请关闭其点,停止向它调用新工作. 保存证据. 从默认列表中删除不是删除审计轨迹的许可.

> 准入后要继续同步状态. 如果一个活跃的版本变得过时或删除,就把它隔离,停止将新工作路由给它.

出版商提供的定制元数据仅属于`_meta.io.modelcontextprotocol.registry/publisher-provided`管理登记的响应元数据是单独的. 不要让出版商设定自己的官方状态.

> 发布者自定义的元数据只能放在发布记录中`_meta.io.modelcontextprotocol.registry/publisher-provided`之下. 管理的 பதிவேடு数据与分离.

### 6. 滚动意味着恢复路线.

滚动时不会编辑不可变的出版物.滚动选择以前被允许的,目前符合条件的脚,并改变主动路线.

> 回滚不会去改写不可变的发布记录. 回滚是选出一个已准备的先前的,然后切换活跃路由.

安全目标必须:

1. 填写入学记录.
2. 您的保险仍然具有活跃的登记处状态.
3. 没有因运行时间或安全证据而被隔离.
4. 仍然要把它固定到封装上,并将描述器设置.
5. 通过目前的健康检查.

> 安全的回滚目标必须: 1) 有一个完整的入门记录; 2) 在你的策略下注册表状态仍然活跃; 3) 没有运行时或安全证据隔离; 4) 仍然可以解析到 pin 住的包和在线描述符集; 5) 通过当前健康检查.

实际调整者应该重新检查包裹,并在激活之前重新检查现场终端点.

> 实际调解者 在激活之前还应重新抓取包并复查在线端点.

### 7. 加入一个录取账本.

录取数据库显示了什么是活跃的.

> 准入数据库说是"现在什么在活跃";账本(账本) 解释是"为什么"――

每个样本输入包含一个序列,时间,事件,服务器,版本,结果,原因,证据,前一个输入哈希,以及自己的哈希.更改一个旧的结果打破了该输入和每一个后来的链接的验证.

> 举例中的每一条账户包含序号,时间,事件,服务器,版本,结论,原因,证据,前一条目的哈希以及自己的哈希.

根据"数据库"的定义,数据库的数据库可以被编写成一个数据库,并且可以被编写成一个数据库.

> 必须周期性地把账本头定在一个独立的信任域,例如签名发布元数据或一次写入存储库.

## 建立它,实现它.

运行控制器已启动`code/main.py`它只使用Python标准库.

> 可运行的控制器在`code/main.py`只有使用Python标准库.

开始于有限的示范:

```bash
cd phases/13-tools-and-protocols/30-mcp-registry-supply-chain-and-drift
python3 code/main.py
```

演示活动进行了五次:

1. 承认`1.0.0`具有匹配的名称空间,包源,协议,功能和工具.
2. 承认`1.1.0`让它变得活跃.
3. 在运行时观察一个意外的删除工具.
4. 观察注册表的状态`1.1.0`成为`deprecated`现在,我们要去.
5. 恢复路由到仍被允许的`1.0.0`子.

> 演示的五个操作:准入`1.0.0`标签: 标签: 标签: 标签: 标签: 标签: 标签: 标签: 标签: 标签: 标签: 标签: 标签: 标签: 标签: 标签: 标签: 标签: 标签: 标签: 标签: 标签: 标签: 标签: 标签: 标签: 标签: 标签: 标签: 标签: 标签: 标签: 标签: 标签: 标签: 标签: 标签: 标签: 标签: 标签: 标签: 标签: 标签: 标签: 标签: 标签: 标签: 标签: 标签: 标签: 标签: 标签: 标签: 标签: 标签: 标签: 标签: 标签: 标签: 标签: 标签: 标签:`1.1.0`设置为活跃;运行时观察到意外删除工具;观察注册表将`1.1.0`状态变为`deprecated`恢复路由到仍处于准备状态`1.0.0`子

预期的形状:

```json
{
  "admitted": [true, true],
  "driftAllowed": false,
  "rollbackAllowed": true,
  "activeVersion": "1.0.0",
  "ledgerValid": true
}
```

在下列顺序下阅读执行情况:

> 预期输出形状:两次准入都成功`admitted: [true, true]`运行时漂移被拒绝路由`driftAllowed: false`),回滚被允许`rollbackAllowed: true`),活跃版本回到`1.0.0`通过: 按下列顺序阅读实现:

1. `namespace_for_domain()`其他`namespace_matches()`确定确切的命名权.
2. `digest()`其他`normalized_tools()`它们可以产生确定性证据.
3. `RegistryAdmissionController.admit()`加入出版,来源,运行时间和政策.
4. `check_live()`通过笔来比较一个新的观察.
5. `observe_registry_status()`隔离版本,注册表状态变化.
6. `rollback()`仅激活已被允许的可接受目标.
7. `AdmissionLedger.verify()`检测记录历史的变化.

## 用它实现框架

设置控制器在发现和路由之间:

> 把准入控制器放在发现和路由之间:

```text
Registry sync -> artifact verifier -> live discovery -> admission controller -> route table
                                               |                 |
                                               v                 v
                                          evidence store    admission ledger
```

对于这些工作使用单独的身份. 登记器同步工作者需要阅读访问转录数据. 文物验证器需要获取数据包. 路线调整器需要许可才能激活一个批准的针. 它们都不需要每个凭证.

> 为这些工作使用相互分离的身份. 注册和步工只需要元数据读取权限;制品验证器只需要包抓取权限;路由调解员只需要激活已批准的脚权限.

 已批准  意思是经过证据的政策.  活动  意思是目前选择的路线.  隔离 意思是它不能接收新工作.  补充 表示另一个被承认的版本是活跃的.不要用一个布尔语编码所有四个意思.

> 让发布状态显式化:"批准"(已批准) 表示证据通过策略;"活跃"(活跃) 表示路由当前选中的是它;"隔离"(已隔离) 表示它不能再接收新工作;"补充"(已取代) 表示另一个已准备的版本处于活跃――不要把这四层含义塞进一个布尔――

在曝光服务器之前运行入口`tools/list`否则,客户可以在发布和政策评估之间的差距中发现工具.

> 在把服务器暴露进来`tools/list`之前先完成准入.否则客户端可能在"已发布"和"策略已评估"之间的空窗期里发现并调用一个工具.

> **【中文解读】**使用它 一节给出三个生产化要点:流水线各环节用独立身份;;防一个组件失陷即全线失守);发布状态用四个词而不是一个布尔(批准/活跃/隔离/超级各有含义);准入必须先于`tools/list`暴露 (堵住发布与审批之间的发现空窗) . 这条"文字图"中的证据库和录取账本正是第7项控制的两类持久化产品.

## 互动实验室

你会看到一个边界一次失败.

> 你将逐个观察每个边界是如何失败的.

### 实验室A:命名空间碰撞

从代码目录中打开Python shell:

```bash
cd phases/13-tools-and-protocols/30-mcp-registry-supply-chain-and-drift/code
python3 -q
```

然后运行:

```python
from main import namespace_matches
namespace_matches("com.example/inventory", "com.example")
namespace_matches("com.exampleevil/inventory", "com.example")
```

结果是`True`第二个是`False`取代对比的确切值为`startswith`在继续之前,请恢复准确的比较.

> 第一个结果是`True`第二个是`False`在本地把精确比较换成`startswith`继续前记得恢复精确比较.

### 实验室B:描述器漂移

```python
from main import *
times = iter(f"2026-08-21T12:00:{n:02d}+00:00" for n in range(10))
c = RegistryAdmissionController(clock=lambda: next(times))
meta = {OFFICIAL_META_KEY: {"status": "active"}}
c.admit(sample_record("1.0.0"), meta, "com.example", evidence_for("1.0.0"), sample_live("1.0.0"))
c.check_live("com.example/inventory", "1.0.0", sample_live("1.0.0", True))
```

检查原因和路线状态.包装和注册表记录没有改变.运行时间工具表面确实改变了,因此控制器隔离和禁用了针.这就是为什么供应链控制必须在安装后继续.

> 检查原因和路由状态:包与注册表记录都没有变化,变化是运行时工具面于控制器隔离并停止使用这个脚.

### 实验室C:状态和回滚

承认`1.1.0`标记为"过期"并尝试两个反弹目标:

```python
c.admit(sample_record("1.1.0"), meta, "com.example", evidence_for("1.1.0"), sample_live("1.1.0"))
c.observe_registry_status("com.example/inventory", "1.1.0", "deprecated")
c.rollback("com.example/inventory", "1.1.0", "unsafe retry")
c.rollback("com.example/inventory", "1.0.0", "restore known release")
c.ledger.verify()
```

已被拒绝了被隔离的目标, 已被接受了早期的活跃脚本, 账本仍然有效.

> 隔离的回滚目标被拒绝;更早的活跃被接受;账本校验仍然通过.

## 实验室 进步实验

扩展控制器,使用两个人使用的批准门.

> 给控制器扩展一道双人审批门 (双人审批门)

> **【中文解读】**进阶练习把第7项控制升级为"破坏性工具必须两人审批":审批应以签名证书引用的形式存储,不能是可变的名称;工具集出现`destructiveHint: true`在工具时,要求两个不同的评审身份;重复身份被拒绝;审批未完成时,最初的进入尝试也应该保留在账本里.

要求:

- 存储批准作为签署的证据引用,而不是在子中可变的名称.
- 需要两个不同的审查员身份,以提供一个工具集`destructiveHint: true`现在,我们要去.
- 拒绝复制审查员身份.
- 在批准未完整时,保存原始录取尝试在本书中.
- 增加零,一,双重和两种不同的批准的测试.
- 不要记录签名,凭证或完整的私人工具参数.

成功意味着,直到两个身份批准了准确的记录,包装和工具集消化,

> 成功标准:在两种身份都批准了那条精确的记录摘要,包摘要和工具集摘要之前,破坏性工具不可能进入活跃状态.

## 运送的艺术品产品

这一课是很好的.`outputs/skill-mcp-registry-admission.md`通过使用它作为一个平坦的可重复使用的运行簿,来审查新的登记库版本或调查漂移.它定义了输入,拒绝规则,证据捆绑,状态调整和反弹证明,而不会依赖于样本类名称.

> 本课附带 `outputs/skill-mcp-registry-admission.md`△在评审一个新的登记库 版本或调查漂移时,把它视为一个平可复制的跑本使用. 它定义了输入,拒绝规则,证据包,状态对账户和回滚证明,并且不依赖于示例代码中的类名.

## 检查一下.

> **【中文解读】**验收清单逐条过:形似前的命名空间被精确边界拒绝;只有官方命名空间的登记处 状态能让版本合格;未验证或不匹配的包与远程证书被拒绝;发行者元数据冒充不了登记处 管理元数据;工具顺序规范化但不掩盖描述符变化;形的包和工具结构安全拒绝;`serverInfo`始终只是诊断、不提供准入权威;描述符漂移会隔离、停止使用并封锁该的回滚;状态变化隔离活跃;回滚不出被隔离或未知的版本;账本改被检测到。

运行示范和确定性套件:

```bash
cd phases/13-tools-and-protocols/30-mcp-registry-supply-chain-and-drift
python3 code/main.py
python3 -m unittest discover -s code/tests -v
```

验证应证明:

- 确切的命名空间界限拒绝类似的预写
- 只有官方名称空间登记处的状态才能使版本符合条件
- 未经验证或不匹配的包装和远程证据被拒绝
- 出版商的元数据不能伪装登记管理的元数据
- 工具的排序是正常化的,而不隐藏描述符的变化
- 错误的包装和工具结构安全地拒绝
- `serverInfo`仍然是诊断的,从来没有提供录取权
- 描述器漂移隔离,禁用和阻塞回转到杆
- 状态变化隔离活跃针
- 转换不能选择隔离或未知版本
- 检测到本书的改

## 产品失败模式

> 下表三列:失败、为什么发生、必需响应──最贵的三行:同一包坐标返回新字节(可变上游或被攻陷的分发道停止激活、保留两份摘要、调查抓取边界);回滚目标从未通过准入(路由控制和审批状态脱节拒绝回滚、对目标重新进入);账本被整体重量写后仍在本地通过(哈希链外部没有点把签名本头发布到独立信任账域)

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

## 运营规则

发表答案 这个身份能发布这个名字吗? 录取答案 我们会执行这个精确的文物并暴露这个精确的行为吗?

> 发布答案是"这个身份可以发布这个名字吗?"进入答案是"我们会执行这个精确的产品吗"",暴露这个精确的行为吗?"把这两个决策分开,锁定每次拼写,让回滚基于证据而不是记忆做选择.

## 继续阅读 继续阅读

- [Official Registry server.json requirements](https://github.com/modelcontextprotocol/registry/blob/main/docs/reference/server-json/official-registry-requirements.md)
- [Official Registry OpenAPI contract](https://registry.modelcontextprotocol.io/openapi.yaml)
- [MCP 2026-07-28 server discovery](https://modelcontextprotocol.io/specification/2026-07-28/server/discover)
