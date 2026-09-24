# 无国籍MCP门户和注册中心准入

> 网关应该明确每个路线. 2026-07-28协议给它方法,名称,版本,能力,身份,缓存和跟踪边界,而无需运输会议.

> **【中文解读】**网关应让每条路由显式化――2026-07-28 协议在没有传输会话的前提下,为网关提供方法,名称,版本,能力,身份,缓存和追踪边界――旧网关"多路复用一个客户端会话到多个后端会话并重写`Mcp-Session-Id`"的设计已成为遗留兼容路径;现代网关对每个请求重新认证、重新授权、重新构建后端请求──

> **【拓展】**网关是企业MCP部署的控制平面:把13期·15期的描述符锁定与13期·16期的授权模型集中执行――注册中心(登记) 提供发现证据(服务器.json),但进入决定权在网关这是"发现不等于决定"的核心分离.

>  **【前置】**学本节前请先掌握:(1) 第13阶段 · 15(安全) 与第13 · 16(授权) 网关集中执行这两课的全部校验;`subscriptions/listen`扩展任务的基本形态.

**Type:** Learn | **类型:** 学习
**Languages:** Python | **语言:** Python
**Prerequisites:** Phase 13 · 15 (security), Phase 13 · 16 (authorization) | **前置知识:** Phase 13 · 15（安全）、Phase 13 · 16（授权）
**Time:** ~75 minutes | **时间:** 约 75 分钟

## 学习目标

- 聚合多个MCP服务器在一个2026-07-28终端点后,而没有会话亲密性.
  中文翻译:把多个MCP服务器聚合到一个2026-07-28端点之后,不依赖会话亲和.
- 在政策或转发之前,按要求验证元数据和路由标题.
  中文翻译:在策略与转发之前的校验每请求元数据和路由头
- 结合工具,使用稳定的命名空间,确定性顺序,描述符针,RBAC和私人缓存.
  中文翻译:用稳定命名空间、确定性顺序、描述符锁定、RBAC 和私有缓存合并工具──
- 作为发现证据,仍然需要入学政策.
  中文翻译:把注册中心记录当作仍需准入策略的发现证据.
- 路线要求范围的SSE,`subscriptions/listen` MRTR 再试, 任务延长调用正确.
  中文翻译:正确路由请求级 SSE`subscriptions/listen`、MRTR 重试和任务 扩展调用──
- 隔离传统的握手和会议支持.
  中文翻译:把遗留握手与会话支持与现代路径隔离――

> **【中文解读】**学习目标:聚合(无会话亲和) 校验(先于策略) 、合并(确定性) 、准入(发现≠决定) 、路由(SSE/订阅/MRTR/任务四种流) 、隔离(遗留路径版本门控) ⋅

## 问题 问题引入

> **【中文解读】**规模化部署应回答六个问题:哪些服务器允许接入?哪个主体可以看到并调用每个工具?两个后端重名怎么办?描述符变更如何复审?限流和审计作用在哪里?任意实例能否处理下一个请求?网关给出一致答案:单个MCP端点 + 横切策略 + 转发批准请求.

直接连接一个客户端到一个服务器是简单的.更大的部署需要一致的答案更难的问题:

> 客户端直连服务器很简单.更大的部署需要更难的问题,

- 哪些服务器可以使用?
  中文翻译:哪些服务器被允许?
- 哪个校长可以看到和打电话每个工具?
  中文翻译:哪个主体能看到并调用每个工具?
- 如果两个后端暴露出同一个名字,会发生什么?
  中文翻译:两次曝光后发生了什么?
- 描述符的变化如何进行审查?
  中文翻译:描述符变更如何复审?
- 利率限制和审计活动在哪里适用?
  中文翻译:限流和审计事件作用在哪里?
- 任何一个案例能处理下一个请求吗?
  中文翻译:任意实例都能处理下一个请求吗?

网关位于客户端和后端MCP服务器之间. 它呈现一个MCP终端点,应用跨界政策,并传递批准的请求.

> 网关位于客户端和后端MCP服务器之间. 它呈现一个MCP端点,应用横切策略,转发批准的请求.

旧的网关设计通常将一个客户端会议复杂化成多个后端会议,然后重新写`Mcp-Session-Id`这是一个传统的兼容性设计. 2026-07-28核心没有协议会议.

> 早期的网关设计常将一个客户端会话多路复用成多个后端会话并重写`Mcp-Session-Id`〔那就是遗留兼容设计〕2026-07-28 核心没有协议会话〕

>  **【类比】**旧网关像"总机转接的电话系统"客户先拨总机(建立会话),总机记住线路(会话亲和),断线就重拨.现代网关像"快递分拣中心"每个包裹(请求) 自带完整面单 (元数据+路由头+凭证),任何分拣员 ((任意实例) 起起就能处理,不需要"上次是谁接的电话"――注册中心像"供应商黄页"黄页证明"只有这个店",不证明"该让这批货进入仓库";准入策略只是仓库的验货单.

## 概念的核心概念

> **【中文解读】**本节按网关的处理流水线展开:现代网关七步路径 → 运行时策略是首要决定 → 单一 POST 端点 → 每层实现发现 → 每个请求客户端能力 → 确定性命名空间 → 锁定已批准描述符 → 注册中心只帮助发现不作决定 → 证中介 → 无会话限流 → 审计决策链 → 请求级 SSE → 长效变更通知 → 网关中的 MRTR → 任务 扩展路由 → 兼容边界.

### 现代门口之路

> **【中文解读】**现代网关对每一个请求走七步:认证主体 → 校验版本/路由头/元数据 → 授权主体、资源、方法、工具、参数 → 应用描述符、注册、限流、数据策略 → 为选择后端构建全新的自含请求 → 校验后端结果并返回网关结果 → 记录不含秘密审计事件──没有需要隐藏协议话;应用状态放库、显式句柄、任务或受完整性保护的MRTR 状态里──

对于每项请求:

1. 确认出境许可证的本人身份.
  中文翻译:从传输层授权信息认证主体──
2. 验证`MCP-Protocol-Version`现在`Mcp-Method`现在`Mcp-Name`其他`params._meta`现在,我们要去.
  中文翻译:校验 `MCP-Protocol-Version`,我知道.`Mcp-Method`,我知道.`Mcp-Name`和 `params._meta`,我知道.
3. 授权主题,资源,方法,工具和论点.
  中文翻译:授权主体、资源、方法、工具和参数──
4. 应用描述符,注册表,利率和数据政策.
  中文翻译:应用描述符、注册、限流和数据策略。
5. 创建一个新的独立请求,为选择的后端.
  中文翻译:为选定后端构造全新的自包含请求.
6. 验证后端结果并返回网关结果.
  中文翻译:校验后端结果并返回网关结果──
7. 记录一个审计事件,没有记录秘密.
  中文翻译:记录审计事件,但不记录秘密──

没有步骤需要隐藏协议会议.应用状态仍然可以存在数据库,明确手柄,任务或完整性保护的MRTR状态中.

> 没有需要隐藏协议会话. 应用状态仍然存在于数据库,显式句柄,任务或被完整性保护的MRTR状态中.

### 运行时间政策是主要的关门决定

> **【中文解读】**准入决定"哪个后端版本可以进网关",但没有授权一次活调.每个请求都必须从已认证的主体,发行商和资源,租户,匹配的方法和名称,规范化参数,进入描述符锁定,后端健康,能力交换,数据分类,流量状态和任何动作绑定批准,重新计算策略.

录取决定后端版本可以进入门口.它不授权直播通话.对于每个请求,门口从认证的主,发行者和资源,租户,匹配的方法和名称,正常化参数,被允许的描述符针,当前后端健康,能力交叉,数据分类,利率状态以及任何行动相关的批准重新计算了政策.

> 准入决定哪个后端版本可以进入网关,但没有授权一次实际调用. 对每个请求,网关必须从已认证的主体,发行者和资源,租户,匹配的方法和名称,规范化参数,准入描述符锁定,当前后端健康,能力交换,数据分类,流量状态和任何动作绑定批准中重新计算策略.

登记记录可以保持活跃,而用户的角色被撤销.一个描述符可以保持固定,而一个目的地参数跨越租户界限.一个后端可以保持批准,而事件政策隔离状态变化的呼叫.因此,运行时间政策是主要允许或拒绝决定,登记和描述符证据作为输入.

> 这个顺序很重要:注册记录可以仍然活跃,用户的角色已经被撤销;描述符仍然被锁定,目标参数跨越租户边界;后端仍然可以批准,事故策略隔离状态变调.因此运行时策略是首要的允许/拒绝决定,注册和描述符证据只是输入.

不要在连接或删除会议识别器下缓存允许决定. 如果没有可用的政策,按操作类进行声明的失败政策. 安全默认是,如果无法关闭状态变化和敏感阅读,而明确批准的公共阅读路径只能使用短期的最后已知政策,只有当其风险模型允许时. 记录该政策版本和失败路径作出决定,然后在返回之前验证后端结果.

> 不要把"允许"决定缓存连接或已移除的会话标志下. 策略不可用时,按操作类执行已声明的失败策略. 安全默认:状态变化与敏感读一律失效关闭.

> ️ **【易错点】**场景:网关把"允许"决定缓存连接ID或旧会话ID 下 / 后果:用户角色被撤销、租户被隔离后,旧连接上的请求仍被放行 策略绕过/修复:

### 一个POST终点

现代流向 HTTP 通过 POST 发送每个 JSON-RPC 消息:

> 现代流通 HTTP 通过邮件 发送每条 JSON-RPC 消息:

```text
POST /mcp
Authorization: Bearer <gateway-token>
MCP-Protocol-Version: 2026-07-28
Mcp-Method: tools/call
Mcp-Name: notes.search
Accept: application/json, text/event-stream
```

网关可以返回JSON或请求-scoped SSE,为 POST. GET和 DELETE返回405现代请求. `Mcp-Session-Id`其他`Last-Event-ID`不要创造权威,亲密关系或重复行为.

> 网关可以为该 POST 返回 JSON 或请求级 SSE。现代请求的 GET 和 DELETE 返回 405。`Mcp-Session-Id`与`Last-Event-ID`没有权力,亲和或重放行为.

标题和体值必须一致. 拒绝与`-32020`在搜索后端之前,这允许负载平衡器,门户和速度限制器路由,而不会分析整个机体,同时保持端到端完整性.

> 头和正文的值必须一致. 在搜索后端之前使用.`-32020`拒绝不匹配. 这让负载平衡器,网关和限流器不需要解析完整的正文就能路由,同时保持端到端完整性.

验证在一个确切的顺序:JSON-RPC和元数据类型,标题和体格等,然后支持匹配的版本.一个不匹配返回HTTP 400`-32020`如果标题和体格同意不支持的版本,请返回HTTP 400`-32022`其他`data`完全是`{"supported":["2026-07-28"],"requested":"<actual>"}`未知方法返回了HTTP 404`-32601`现在,我们要去.

> 按唯一精确顺序验证:JSON-RPC与元数据类型,头和正文相等等,然后支持匹配版本.`-32020`标题一致但版本不支持,返回HTTP 400 `-32022`且`data`精确为`{"supported":["2026-07-28"],"requested":"<actual>"}`无法返回HTTP 404`-32601`,我知道.

`ProtocolError`带有可选的`data`通过一个通道将其串行到JSON-RPC错误对象中.`id`通过 HTTP 通知,它返回 202 个空格.

> `ProtocolError`携带可选`data`网关将其序列化为JSON-RPC 错误对象.`id`永远不接受JSON-RPC成功或错误响应.

### 实现发现在每个层

通过网关实现`server/discover`它还发现每个后端,所以它知道协议版本,功能和扩展.

> 网关为客户端实现`server/discover`为了了解协议版本,能力和扩展.

举例的网关结果:

> 网关结果示例:

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

广告只能在网关可以尊重的功能交叉点.后端功能不自动安全地暴露.没有后端路径的网关功能不有用广告.

> 后端功能不自动等于可对外暴露;没有后端路径支的网关功能通告也没有用.

`serverInfo`没有任何数据显示或诊断数据,请不要使用它们作为注册表或出版商证明.

> `serverInfo`报表和诊断数据,不要作为注册中心或发行人证明.

### 客户端要求能力

每个转发的请求都需要一个最新的信息`_meta`包裹:

> 每个转发的请求都需要当前的.`_meta`封信:

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

通过后端,不要盲目复制外部客户端功能.门户端是后端客户端. 广告只能具有门户端正确的调解功能.

> 网关才是后端的客户端. 只有通告网关能正确介绍的特性.

### 确定性名称空间

合并后端工具以稳定的公共名称:

> 用稳定的公开名称合并后端工具:

```text
notes.search
notes.create
issues.list
issues.open
```

保持一个地图从公众名称到后端和原始工具名称. 永远不要选择第一个或最后的碰撞. 公众名称是批准和审计合同的一部分,所以更改它是一个迁移.

> 保留"公开名 → 后端 + 原始工具名"的映射──绝对没有重名冲突里选先来后到──公开名是审核与审计契约的一部分,改它就是一次迁移──

`tools/list`显度因主体而异时,返回`cacheScope: private`没有任何限制.`ttlMs`减少后端发现负载,而不会允许用户特定列表在授权环境中泄露.

> `tools/list`必须确定性.`cacheScope: private`有界的`ttlMs`降低后端发现负载,再不让按用户定制列表跨授权下文泄漏.

每个暴露的工具描述符都包含一个稳定的名称,描述和对象根`inputSchema`名称空间不能删除所需的描述字段.完整列表结果还包括`resultType`服务器身份元数据,以及缓存提示.

> 每个暴露的工具描述符都包含稳定名称,描述和对象根.`inputSchema`△命名空间化不能删掉必填的描述符字段──完整列表结果还包括`resultType`、服务器身份元数据和缓存提示──

### 印批准的描述符

在入学时,将完整的描述符归类为法典,并将其消化器存储在合格的公众名称下.在列表和电话时间,将现场描述器与批准的消化器进行比较.

> 准入时规范化完整描述符,把摘要保存到有限公开名下.

如果变化:

- 删除它`tools/list`现在,我们要去.
  中文翻译:从 `tools/list`移除它.
- 拒绝直接电话.
  中文翻译:拒绝直接调用。
- 发出审计活动.
  中文翻译:发出审计事件.
- 需要在更新之前重新批准政策或人类.
  中文翻译:更新锁定前要求策略或人工重新批准.

网关是一个有用的中央执行点,但它不会使一条第一次看到的描述符成为安全的描述符.

> 网关是有用的集中执行点,但它不能把"第一次见到的描述符"变成安全的.

### 登记文件帮助发现,而不是决定

> **【中文解读】**注册中心`server.json`只是发布元数据:它说明"这个包叫什么"",怎么装"",版本号是多少",不带网关的安全决定.`server.json`与准入状态做连接(加入) ⋅每个准入后端要记录:精确注册中心与记录标识、已验证发行人命名空间、允许传输与端点、锁定版本、工件/描述符摘要、授权发行者与资源、评审员/审批时间/有效期──

一个注册书`server.json`提供出版元数据. 包装支持的记录可以看起来像这样:

> 注册中心`server.json`提供发布元数据――一个带包的记录长如下:

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

发布元数据不包含网关的安全决定. 保存经验证的出版商和来源证据在单独的录取状态:

> 发布元数据不承载网关的安全决定.

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

门口检查了`server.json`通过通过该网关,我们可以将其与外部状态联系起来.

> 网关检查 `server.json`网关仍然需要自己的准入策略.

对于每一个被允许的后端,记录:

- 记录和记录的确切标识.
  中文翻译:精确的注册中心与记录标识.
- 经过验证的出版商名字空间或域名证据.
  中文翻译:已验证的发行者命名空间或域名证据──
- 允许运输和终点.
  中文翻译:允许的传输与端点――
- 嵌版本或批准的升级政策.
  中文翻译:锁定的版本或已批准的升级策略.
- 艺术品或描述器消化.
  中文翻译:工件或描述符摘要.
- 授权发行人和资源.
  中文翻译:授权发行者与资源──
- 审核,批准时间,和过期.
  中文翻译:评审人、批准时间与有效期──

由于其显示名称类似于熟悉的产品,所以不要接受服务器.不要把登记器存在视为运营安全审查.即使它们从未出现在公开登记器中,也可以通过相同的证据方案接入私人服务器.

> 不要因为展示名字像某个熟悉产品而接受服务器;不要把"登记中心"当作一次运营维安全评审.

这一课实现了门口接:在后端成为可路由之前,将出版证据与本地录取相结合. [Lesson 30: MCP Registry Supply Chain, Admission, Drift, and Rollback](../../30-mcp-registry-supply-chain-and-drift/docs/en.md)建立完整的控制平面,以确定名称空间的确切性,文物来源,不可变的针头,直播描述器漂移,登记处状态调整,具有明显的录取账本和证据支持的反转.保持供应链状态与上述按要求运行时间决定分开.

> 本课程实现了网关接:在后端可路由之前,把发布证据连接到本地准入.30课时,要构建完整控制平面精确命名空间证明,工件来源,不可变锁定,线上描述符漂移,注册中心状态对账户,防改准入账本和有证据支的回滚.

>  **【困惑】**问:注册中心都验证了发布者,为什么网关还需要自己的进入策略?A:注册中心验证的是"发布者是谁",不是"你的企业不应该使用"――注册记录可以保持有效而用户角色已被撤销;描述符保持锁定而目标参数跨租户;后端保持批准而事故策略隔离状态变调.

### 权证调解

后端的身份证件从未传递给客户端.

> 网关认证自己的调用方,并单独向后端做认证.后端凭证永远不到客户端手上.

保持这些义务明确:

> 让这些绑定保持显然:

```text
outer principal -> gateway role and policy
backend issuer + resource -> backend registration and token
```

永远不要将外部门口代币传递给后端.永远不要在不同的发行商或资源中重复使用后端代币.如果工具代表最终用户,则用设计的交易或索赔模型保存该代权,而不是用共享服务凭证伪装用户.

> 绝对不会把外部网关代币传递给后端;绝对不会把后端代币用给另一个发行商或资源. 如果工具代表最终用户行动,则使用设计的交换或声明模型保留该层委托,而不是拿到共享服务凭证冒充用户.

### 没有会议的定位限制

通过认证的资本,发行人,资源,公共工具,成本类别和时间窗口的关键限制. 会议ID是缺失的,即使存在,也很容易旋转.

> 限流按已认证主体,发行商,资源,公开工具,成本类别和时间窗口取键――会话 id 已不存在;即便存在也容易轮换,不可作键――

在消耗昂贵的工作之前,请使用廉价验证.

> 首先做便宜的校验,再消耗昂贵的工作.并决定被拒绝调用是否包括滥用限制,业务配额或两者.

### 审计决策链

记录足以重建电话:

> 记录足够重建一次调用信息:

- 要求和追踪标识符.
  中文翻译:请求与追踪标识符──
- 证实资本和发行人
  中文翻译:已认证主体与发行人──
- 公共工具和后端路线.
  中文翻译:公开工具与后端路由──
- 描述器印版本.
  中文翻译:描述符锁定版本.
- 政策决定和理由.
  中文翻译:策略决定与理由。
- 延迟和结果类.
  中文翻译:延迟与结果类别.
- 适用时MRTR轮或任务标识符.
  中文翻译:适用时的MRTR轮次或任务标识符──

编辑代码,授权代码,更新代码,原始秘密和不必要的敏感论点.

> 对于持有符号,授权码,更新符号,原始秘密和不必要的敏感参数做敏.

### 根据要求进行的SSE

当一个请求中工作流时,正常的POST可能会返回请求-scopeed SSE.关闭响应流会取消飞行中现代HTTP请求.

> 当工作在一个请求中流式产出时,普通 POST 可以返回请求级 SSE──关闭响应流即取消这个正在进行的现代 HTTP 请求──

别创建一个独立的GET流,不要承诺重播最后事件ID.

> 不要再建成GET流,也不要承诺最后事件身份重放――那些是旧传输假设――

### 长期变化通知

对于列表和资源更改通知,当前客户端发送`subscriptions/listen`通知过器使用精确的平面字段 `toolsListChanged`现在`promptsListChanged`现在`resourcesListChanged`其他`resourceSubscriptions`其他:

> 关于列表和资源变化通知,当前客户端通过 POST 发送 `subscriptions/listen`并收到SSE响应. 通知过器使用精确的平字段.`toolsListChanged`,我知道.`promptsListChanged`,我知道.`resourcesListChanged`和 `resourceSubscriptions`其他:

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

首先,确认支持的子集.其订阅标识符是开放流的请求的JSON-RPC id:

> 第一个事件确认受支持的子集. 订阅标识符就是打开该条流的请求的JSON-RPC id:

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

接下来,网关只传输确认的变更类型.`io.modelcontextprotocol/subscriptionId`在`params._meta`没有自动重播或自动重听.重连接后,客户端重新打开订阅并更新其依赖的列表.服务器启动的优雅闭幕返回最终完整结果,标记为相同的订阅ID.

> 之后网关只转发已确认的变更类型.`params._meta`带同一个`io.modelcontextprotocol/subscriptionId`△没有自动重复,也没有自动重复监听. △重连时客户端重新开订单并更新依赖的列表. △服务器主动优雅关闭时,返回相同订单ID的最终完整结果.

现代道路取代了`resources/subscribe`现在`resources/unsubscribe`保持这些只在一个版本封闭的旧路径.

> 现代路径取代了`resources/subscribe`,我知道.`resources/unsubscribe`它们只保留在版本门控的旧路径中.

### 通过门口的MRTR

> **【中文解读】**后端返回`resultType: input_required`网关只能在外部客户端支持所需输入请求的情况下转发结果.`requestState`必须按字节原样保留──客户端使用新的JSON-RPC id 和 `inputResponses`重试原公开工具;网关对重试重新授权;检查同一公开路由,再转发全新的后端请求绝不假设早一轮授予无限批准

当一个后端回来时`resultType: input_required`通过输入,网关只能转发该结果,如果外部客户端支持所需的输入请求.`requestState`字节对字节,除非门户故意终止并重新发行互动.

> 后端返回`resultType: input_required`只有外部客户端支持所需输入请求,网关才能转发结果.`requestState`为了保留节目.

客户端将使用新 JSON-RPC ID 重新尝试原始公共工具`inputResponses`网关重新授权重新尝试,检查相同的公共路线,然后发送新的后端请求. 它不能假设一个早些时候获得无限批准.

> 客户端使用新的JSON-RPCID 和 `inputResponses`重试原公开工具──网关对重试重新授权──检查同一公开路由,然后转发全新的后端请求──绝不能假设早一轮给予无限批准──

### 任务扩展路由

> **【中文解读】**任务是官方扩展`io.modelcontextprotocol/tasks`),不是核心会话的替代品.`tools/call`返回`resultType: task`带`taskId`、状态,时间`ttlMs`可选`pollIntervalMs`);后续`tasks/get`现在,我们要去.`tasks/update`现在,我们要去.`tasks/cancel`用`params.taskId`作者:`Mcp-Name`给中间件一个路由键. 网关为不透明任务 id 记录主体和后端路由. 不要实现新的.`tasks/list`或`tasks/result`那是旧实验模型的词汇.

任务是官方扩展,`io.modelcontextprotocol/tasks`它们不是一个核心会议的替代品.

> 任务是由`io.modelcontextprotocol/tasks`标识的官方扩展,不是核心会话的替代品.

客户端声明扩展在每次请求客户端功能内,门口只在能够保存生命周期终端时将其公布在发现中.`tools/call`后端单独决定是否返回普通结果`resultType: task`任务结果带有`taskId`现在`status`时间,`ttlMs`其他选择性`pollIntervalMs`任务必须在发送结果之前已经可读.

> 客户端在每一个请求的客户端能力中声明该扩展;网关只有在能端到端维持任务生命周期时才在发现中通知它.`tools/call`返回正常结果或`resultType: task`后端单独决定.任务的结果直接在结果中带来.`taskId`,我知道.`status`时间`ttlMs`和可选的`pollIntervalMs`◎ 应先发送该结果,任务必须已经可持久读取.

后者是: 通过该网关记录了不透明任务识别器的认证主和后端路线.`tasks/get`现在`tasks/update`其他`tasks/cancel`电话使用`params.taskId`作为`Mcp-Name`通过此, 提供了路由密钥.`tasks/get`收益`resultType: complete`输入到终端状态的终端结果或协议错误. `tasks/update`发送钥匙`inputResponses`对于未完成任务输入,返回一个空白的完整确认. `tasks/cancel`合作的意图是完全承认的,而不是保证工作停止.

> 网关为不透明任务标识符记录已认证主体与后端路由──后续的 `tasks/get`,我知道.`tasks/update`,我知道.`tasks/cancel`调用使用`params.taskId`作者:`Mcp-Name`给中间件一个路由键.`tasks/get`返回`resultType: complete`与当前任务状态,并终态内联最终结果或协议错误.`tasks/update`为未决任务输入发送带键的`inputResponses`返回空的完成确认.`tasks/cancel`是协作意图加空的完成确认,不保证工作真的停止.

不要实施新的`tasks/list`或`tasks/result`需要输入的任务将通过 系统中包含的请求进行解明.`tasks/get`客户通过回复`tasks/update`客户端仍然在建议的间隔中进行投票;任务创建仍然是服务器导向的.

> 不要实现新的`tasks/list`或`tasks/result`方法它们属于较旧的实验模型.`tasks/get`暴露完整的内嵌请求;客户端通过 `tasks/update`回答,而不是重试原工具调用――客户端仍按建议间隔轮询;任务创建仍由服务器主导――

持久任务路径状态是应用程序数据,由任务处理器键化,而不是协议会议.

> 持久任务路由状态是按任务句子取取关键的应用数据,而不是协议会话.

### 兼容性界限

如果网关必须为旧客户端或后端服务:

> 如果网关必须服务较旧的客户端或后端:

- 显然可以探测到时代.
  中文翻译:显式检测协议年代──
- 保存初始化,运输会议,GET流,资源订阅和旧任务词汇在旧适配器中.
  中文翻译:把初始化、传输会话、GET 流、资源订阅和旧任务词汇全部留在遗留适配器里──
- 永远不要将旧的会议身份证泄露到现代路由或授权中.
  中文翻译:绝不让遗留会话 id 泄漏进现代路由或授权。
- 宁愿有限于发现探测器和明确的反弹政策,
  中文翻译:优先使用有界的发现探测加显然回归策略,而非静默降级.

```figure
t3-gateway-funnel
```

## 动手构建

> **【中文解读】** `code/main.py`实现进程内协议网关 + 两个后端服务器. 每个后端都收到全新的当前协议请求;网关提供发现,根据用户过的确定性.`tools/list`、命名空间路由、注册中心 `server.json`根据主体取决的限制流程,审计决定以及建模`subscriptions/listen`证实――模型接收已解析的请求正文、路由头和已认证的载体身份,不是完整的HTTP 适配器传输层契约归 09课――

`code/main.py`通过程序中协议网关和两个后端服务器实现.每个后端都收到一个新的当前协议请求.`tools/list`名称间路由,登记`server.json`另外,外接状态,描述符,RBAC,主要关键利率限制,审计决定以及一个模型`subscriptions/listen`证实安全性.

> `code/main.py`实现进程内协议网关和两个后端服务器. 每个后端都收到全新的当前协议请求.`tools/list`、命名空间路由、注册中心 `server.json`根据主体取键的限制流,审计决定,以及建模的`subscriptions/listen`证实

该模型接收解析请求体,路由标题和认证的载体身份.它不是完整的HTTP适配器,也不解析`Content-Type`或是全部`Accept`连接到第09课的流向HTTP适配器,`Content-Type: application/json`其他`Accept`含有两者中的值`application/json`其他`text/event-stream`现在,我们要去.

> 模型接收已解析的请求正文、路由头和已认证的载体身份──它不是完整的HTTP适配器,不解析`Content-Type`或完整的`Accept`契约──把它接到第09课的流动HTTP适配器上那边要求`Content-Type: application/json`且`Accept`同时包含`application/json`与`text/event-stream`,我知道.

运行它:

> 运行:

```bash
cd phases/13-tools-and-protocols/17-mcp-gateways-and-registries
python3 code/main.py
python3 -m unittest discover code/tests -v
```

演示程序将打印外部请求 ID 和新版本的后端请求 ID,

> 演示会打印外层请求 id 和全新的后端请求 id,让这个跳跃的无状态可见.

## 实际使用

换取实时协议客户端的进程后端对象.保持相同的连接:

> 把进程内后端对象转换为真实的当前协议客户端──保留相同的接:

- 在连接前的录取记录.
  中文翻译:连接之前先有准入记录――
- 在能力曝光之前的后端发现.
  中文翻译:能力暴露之前先完成后发现.
- 在授权之前的合格公众名称.
  中文翻译:授权之前先确定限定公开名──
- 在列表或电话之前,点描述符.
  中文翻译:列表或调用之前先核对描述符锁定.
- 在转发前,每次请求的新型元数据.
  中文翻译:转发之前先构建新鲜的每一个请求元数据.
- 在返回之前验证结果.
  中文翻译:返回之前先校验结果──

## 运送它.

这一课是很好的.`outputs/skill-gateway-bootstrap.md`它生产了一个现代化的门户设计,涵盖入口,发现,录取,命名空间,授权,缓存,流媒体,订阅,MRTR,任务,可观察性和遗产隔离.

> 本课产出发 `outputs/skill-gateway-bootstrap.md`△它产生现代网关设计,覆盖入口,发现,准入,命名空间,授权,缓存,流式,订阅,MRTR,任务,可观测性和遗留隔离.

## 练习题

1. 添加跟踪文本到外部和转发的请求元数据,并记录在审计事件中相关性.
   中文翻译:给外层与转发的请求元数据加追踪上下文,并把关联关系记入审计事件.
2. 添加一个可执行任务的后端和路线`tasks/get`按任务ID`Mcp-Name`现在,我们要去.
   中文翻译:添加支持任务的后端,并按 `Mcp-Name`里任务 id 路由 `tasks/get`,我知道.
3. 改变一个后端描述符,证明发现和直接调用都被阻止了.
   中文翻译:变更一个后端描述符,证明发现和直接调用都被阻止了。
4. 添加一个主要特定的服务器功能,并解释为什么发现必须保持私密缓存.
   中文翻译:添加按主体定制的服务器能力,并解释为什么发现必须保持私有缓存.
5. 写一个旧的适配器界面,而不需要添加任何旧状态到现代的`Gateway`课程.
   中文翻译:编写遗留适配器接口,且不给现代 `Gateway`类添加任何遗留状态──

## 关键词 快速查找表

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

## 继续阅读 继续阅读

- [Streamable HTTP transport](https://modelcontextprotocol.io/specification/2026-07-28/basic/transports/streamable-http)
  中文说明:可流动的HTTP传输规范单 POST端点与请求级SSE契约
- [Server discovery](https://modelcontextprotocol.io/specification/2026-07-28/server/discover)
  中文说明:`server/discover`规范网关与后端的双层发现依据.
- [Official Registry server.json requirements](https://github.com/modelcontextprotocol/registry/blob/main/docs/reference/server-json/official-registry-requirements.md)
  中文说明:官方注册中心 `server.json`要求发布元数据的字段契约。
- [MCP Tasks extension](https://tasks.extensions.modelcontextprotocol.io/specification/draft/tasks)
  中文说明:MCP任务 扩展草案 任务生命周期与 `Mcp-Name`路由键.
