# 无状态服务器的可寻址上下文

> 工具执行操作.资源暴露可地址的内容.提示用户选择的信息模板.一个好的MCP服务器将这些合同保持分开和可预测.

> **【中文解读】**三种服务器原语各司其职责:工具 执行操作,资源 暴露可寻址的内容,提示 打包用户选择的消息模板。一个合格的MCP 服务器让这三份契约彼此分离、可预期──本课还把这三者放进2026-07-28的无状态信封:没有初始握手,每个请求自带协议版本和能力,列表结果确定性排序,缓存提示(`ttlMs`现在,我们要去.`cacheScope`)成为正确性的一部分.

> **【拓展：原语三分→真实产品】**现实中分工例:GitHub MCP 把问题 详情做成资源(URI可寻址、宿主可附加到上下文),把"创建问题"做成工具(有副作用),把"代码审查工作流"做成提示模板(用户一键触发) ――2026-07-28 的新约束是:资源订阅不再使用`resources/subscribe`它们是统一的.`subscriptions/listen`要求级响应流与第九课的传输层进步一脉相承

>  **【前置】**学本节前请先掌握:(1) 阶段13·07(构建MCP 服务器) 工具/列表、工具/调用实现;(2) 阶段13·09(MCP 传输层) 无状态信封、`_meta`关键,`subscriptions/listen`的传输背景;(3) URI 概念(`file://`、自定义方案);(4) 若学过旧版(`resources/subscribe`订阅),注意该方法已被遗留时代.

**Type:** Build | **类型:** 构建
**Languages:** Python | **语言:** Python
**Prerequisites:** Phase 13, Lesson 07 (Building an MCP Server), Phase 13, Lesson 09 (MCP Transports) | **前置知识:** Phase 13 · 07（构建 MCP 服务器）、Phase 13 · 09（MCP 传输层）
**Time:** ~60 minutes | **时间:** 约 60 分钟

## 学习目标

- 选择消费者的意图中的工具,资源和提示.
  中文翻译:从消费者意图出发,在工具、资源和提示之间做选择.
- 通过强制性的方式宣传资源和即时地表面`server/discover`现在,我们要去.
  中文翻译:通过强制的`server/discover`公共资源与提示能力面面
- 建立确定性`resources/list`其他`prompts/list`结果.
  中文翻译:构建确定性的`resources/list`和 `prompts/list`结果.
- 申请`ttlMs`其他`cacheScope`没有泄露用户特定数据.
  中文翻译:应用 `ttlMs`和 `cacheScope`而不泄露用户特定数据.
- 返回JSON-RPC错误`-32602`对于无效或未知资源URI.
  中文翻译:对无效或未知的资源URI 返回JSON-RPC 错误`-32602`,我知道.
- 打开一个`subscriptions/listen`通过订阅ID将每个事件进行 POST-响应流和相关联.
  中文翻译:打开`subscriptions/listen`关联每个事件.
- 处理资源内容和提示模板作为不值得信赖的服务器输出.
  中文翻译:把资源内容和提示模板当作不可信的服务器输出.

## 开始从消费者开始.

> **【中文解读】**误用MCP的最简单方式是从实现代码发出:"这是个函数所以做成工具""这是个文件所以做成资源"......正确起点是"谁在选择"",他期待什么":模型/应用执行操作选工具;主机、应用或用户读取URI 内容选资源;用户通过主机UI启动可复用消息工作流选提示――不要为一种能力同时暴露三种原语每个多种能力出面必须付出发现,授权,缓存,错误处理,测试和文档的代价.

滥用MCP的最简单方法是从实施代码开始.数据库查询成为一个工具,因为功能熟悉.可重复使用的工作流成为资源,因为它存储在文件中.提示成为隐藏的政策,因为主机可以注射它.

> 误用MCP的最简单方式是从实现代码发出而成.数据库查询成为工具,因为函数让人熟悉.可复用工作流成为资源,因为它存在于文件中.

首先要知道谁选择,他们期待什么.

> 从"谁在选择他期待什么"开始.

| Primitive | Primary intent | Selection owner | Typical result |
|---|---|---|---|
| Tool | Perform an operation | Model or application | Structured action result |
| Resource | Read content at a URI | Host, application, or user | Text or binary content |
| Prompt | Start a reusable message workflow | User through host UI | One or more prompt messages |

给我一个笔记`notes://note-1`由于它是可地址的内容,它是资源. `delete_note`它们是工具,因为它们改变了状态.`review_note`是一个提示,因为用户选择了准备的审查工作流程.

> `notes://note-1`上面的笔记是资源,因为它是可查找的内容.`delete_note`是工具,因为它改变了状态.`review_note`是提示,因为用户选择的是预制的审查工作流.

不要把这三项操作都暴露出来,只是为了看起来完整.每一个额外的表面都需要发现,授权,缓存,处理错误,测试和文件.

> 不仅仅是为了完整化,我们必须同时把一个操作暴露在三种原语中.

>  **【类比】**三原语像图书馆的三种资源:工具是借阅台工作人员你请他做事查书、办卡),他执行动作、有副作用;资源是书架上的书URI 就是索书号,主管可以直接接到下文里,不需要每次请示;提示是馆内"自助导览路线"预制好的多步流程,用户按一按一下就走完整的程程.

## 没有国家封面.

> **【中文解读】**本课面向MCP 协议修订版 2026-07-28 的无状态档位:没有初始握手,没有协议会话,每个请求用保留的`_meta`关键自带协议版本和客户端能力――服务器必须实现`server/discover`实现身份和缓存提示――正常结果声明`"resultType": "complete"`支持修订返回`-32022`并同时提供请求修改和服务器支持的修改.设计直觉随之改变:列表不能依赖于相同连接的前调;授权可以改变可见集合 (凭证是请求输入),但连接历史不能.

本课程针对MCP协议修订`2026-07-28`没有启动手握或协议会议.每个请求都包含其协议版本和客户端功能在保留中.`_meta`关键.

> 本课面向MCP 协议修订版 `2026-07-28`没有初始握手,也没有协议会话.`_meta`键中携带自己的协议版本和客户端能力.

```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "method": "resources/list",
  "params": {
    "_meta": {
      "io.modelcontextprotocol/protocolVersion": "2026-07-28",
      "io.modelcontextprotocol/clientInfo": {
        "name": "course-client",
        "version": "1.0.0"
      },
      "io.modelcontextprotocol/clientCapabilities": {}
    }
  }
}
```

服务器必须实现`server/discover`结果广告支持
版本,资源和快速功能,实施身份,以及
客户端可能直接调用另一种方法,但发现给它
在构建UI之前,需要一个稳定的快照.

> 服务器必须实现`server/discover`△其结果公告支持的版本、资源与提示能力、实现身份和缓存提示──客户端可以直接调用其他方法,但发现能够让它在构建UI之前得到稳定的快照──

```json
{
  "resultType": "complete",
  "supportedVersions": ["2026-07-28"],
  "capabilities": {
    "resources": {"listChanged": true, "subscribe": true},
    "prompts": {"listChanged": true}
  },
  "ttlMs": 3600000,
  "cacheScope": "public"
}
```

结果是正常的`"resultType": "complete"`答案`_meta`确定服务执行的情况`io.modelcontextprotocol/serverInfo`对于诊断而言,这些信息是有用的.它不是身份验证.`-32022`要求修改和服务器支持修改.

> 正常结果声明`"resultType": "complete"`应对`_meta`用`io.modelcontextprotocol/serverInfo`标识提供服务的实现. 这些信息对于诊断有用,但不是认证身份.`-32022`同时提供请求修改和服务器支持修改.

无国籍合约改变了您的设计本能.列表不能依赖于一个连接的先前调用.授权可能会改变可见的集合,因为凭证是请求输入,但连接历史不能.

> 无状态契约会改变你的设计直觉――列表不能依赖于相同的连接上的前调用――授权可以改变可见集合,因为凭证是输入请求,但连接历史不能――

## 资源是稳定的URI协议

> **【中文解读】**资源由URI标识的内容先设计的URI,再写处理器――好URI的性质:足够稳定可收藏、按服务器域名命名空间化、独立于进程ID或连接、存储访问前先校验、每次阅读都过授权――`resources/list`返回调用者当前可见的资源,按稳定键 (如URI) 排序 确定性排序可以避免缓存噪音、快照漂移和主机UI 跳动──`resources/read`对于未知的URI不返回"成功空读",而是`-32602`让客户端能区分"不存在"与"合法的空档"――

资源是由URI识别的内容. 在处理器之前设计URI.

> 资源由URI标识的内容──先设计URI,再写处理器──

良好的URI特性:

> 良好的URI的性质:

- 足以预示或通过请求之间的稳定性.
  中文翻译:足够稳定,可收藏或在请求中传递.
- 给服务器域名空间.
  中文翻译:按服务器域名做命名空间。
- 独立于进程身份证或连接.
  中文翻译:独立于进程ID或连接──
- 在存储访问前验证.
  中文翻译:在访问存储之前先校验。
- 在每一次阅读中都得到授权.
  中文翻译:每次读取都做授权──

`notes://note-1`没有什么比`note-1`因为它的名字空间是明确的.`file://`解决符号链接和相对段落后,它仍然必须检查配置目录边界.

> `notes://note-1`优于`note-1`文件服务器可以使用.`file://`解析符串链接和相对段后,仍然必须检查配置的目录边界.

`resources/list`确定性顺序防止噪音缓存错失,改变快照和主机UI在更新之间跳跃.

> `resources/list`返回调用者当前可见的资源――按稳定键如URI排序――确定性排序可防止杂的缓存未预期、不断变化的快照,以及在两个刷新之间跳跃跳去的宿主UI――

```json
{
  "resultType": "complete",
  "resources": [
    {
      "uri": "notes://note-1",
      "name": "Architecture decision",
      "description": "Why the service uses a stateless boundary",
      "mimeType": "text/markdown"
    }
  ],
  "ttlMs": 300000,
  "cacheScope": "public",
  "_meta": {
    "io.modelcontextprotocol/serverInfo": {
      "name": "notes-server",
      "version": "2.0.0"
    }
  }
}
```

`resources/read`返回一个或多个内容项.未知URI不是成功的空读.当前资源规格将无效或未知资源URI分配给 JSON-RPC无效参数,代码 `-32602`现在,我们要去.

> `resources/read`返回一个或多个内容项──未知URI不等于一次成功空读──现行资源 规范把无效或未知资源URI归类为JSON-RPC 无效参数,错码`-32602`,我知道.

```json
{
  "jsonrpc": "2.0",
  "id": 2,
  "error": {
    "code": -32602,
    "message": "Unknown or invalid resource URI",
    "data": {
      "uri": "notes://missing"
    }
  }
}
```

这种区别使客户端能够将缺席与有效的空文件分开.

> 这种区别使客户端能够将"不存在"与"合法空档"分开.

### 资源模板

> **【中文解读】**资源模板描述一族参数化URI,适用于"列出每个具体项目的成本高昂或无上界"的场景.模板不松校验:解析变量,过授权,限长度和字符集,使用类型化参数构建存储查询绝不会将任意的URI尾巴拼进文件路径或数据库语句.

资源模板描述了一个参数化的URI家族. 列出每个具体项目时使用一个. 例如,`notes://projects/{project}/decisions/{decision}`告诉客户如何形成有效地址,而不返回每一个决定.

> 资源模板描述一族参数化的URI──当列出每个具体项目的使用时高昂或无上界――例如`notes://projects/{project}/decisions/{decision}`告诉客户端如何构建合法地址,而不必回复每一个决定.

模板不会削弱验证.解析变量,应用授权,执行长度和字符限制,并构建使用输入参数的存储查询.永远不要将任意的URI尾巴连接到文件系统路径或数据库声明中.

> 模板不会放松学习.解析变量,应用授权,强制长度和字符限制,并使用类型化参数构建存储查询.

### 内容不是可信的指令

> ️ **【易错点】**场景:把资源文真实命令执行,或让提示成为绕过资源授权的旁路 / 后果:资源文本可能含提示注入、秘密、误导性命令或形标记;未授权的字段泄露给调用者 / 修复:宿主保留信息并将资源内容作为数据;服务器限制内容大小、返回准确的MIME类型、脱敏调用者无权访问的字段、不返回无关记录;即时的URI参数与直接资源阅读相同的授权检查.

资源文本可能包含即时注射,秘密,误导命令或错误的标记.主机应该保留来源,并将资源内容视为数据.服务器应该限制内容大小,返回准确的MIME类型,编辑调用者无法访问的字段,避免返回无关记录.

> 资源文本可能包含提示注入、秘密、误导性命令或形标记──主机应保留出处信息并将资源内容作为数据──服务器应限制内容的大小、返回准确的MIME类型、脱敏调用者无权访问的段段,并避免返回无关记录──

## 提示是用户控制的模板

> **【中文解读】**面向显式的用户选择:主机可以染成斜命令、菜单项或工作流按,协议不限制UI。`prompts/list`对于相同请求授权应保持确定性;每个提示都必须有稳定的名称,有用的描述和参数声明,让主持人在`prompts/get`之前收集输入.`prompts/get`把参数解析成消息,但不取代主机系统指令主机决定如何返回消息进入模型下文,并让自己的可信策略保持更高的优先级.

简单的MCP提示是为用户选择设计的.主机可以将它们作为切片命令,菜单项或工作流按.协议不需要一个UI.

> 作为用户选择的设计,MCP提示. 主持人可以将其染成斜命令,菜单项或工作流按.协议不要求某种特定的UI.

`prompts/list`每个提示需要一个稳定的名称,一个有用的描述和参数声明,让主机收集输入之前`prompts/get`现在,我们要去.

> `prompts/list`对于相同的请求权限应保持确定性. 每个提示都需要稳定的名称,有用的描述和参数声明,让主机能够在`prompts/get`之前收集输入.

```json
{
  "resultType": "complete",
  "prompts": [
    {
      "name": "review_note",
      "title": "Review a note",
      "description": "Review one note for a named concern",
      "arguments": [
        {
          "name": "uri",
          "description": "The note resource URI",
          "required": true
        }
      ]
    }
  ],
  "ttlMs": 600000,
  "cacheScope": "public"
}
```

`prompts/get`解决参数成消息. 它不取代主机的系统说明.主机决定如何返回消息进入模型背景,并将自己的可信度政策放在更高的优先级.

> `prompts/get`把参数解析成消息――它不取代主机系统指令――主机决定如何返回消息进入模型下文,并让自己的可信策略保持更高的优先级――

验证服务器边界的提示参数.提示URI应通过直接资源阅读的相同授权检查.不要使提示作为资源访问的侧通道.

> 在服务器边界校验提示参数──提示 URI 应通过与直接资源阅读相同的授权检查──不要让提示成为绕过资源访问的旁路──

## 缓存提示是正确的部分

> **【中文解读】** `ttlMs`告诉客户端结果可复用多久,`cacheScope`描述谁可以共享缓存值──MCP只定义`public`和 `private`两种`cacheScope`携带秘密或快速变化的结果`private`其他`ttlMs: 0`没有店铺规则更严格 通过宿主缓存策略实现`no-store`不是MCP的`cacheScope`值──缓存提示永远不能取代授权:缓存键必须包含所有可见变化的请求维度(租户、用户、范围、语言、分页游标);共享缓存表达不了这些维度,就用`private`零 TTL + 宿主级无店铺――

`ttlMs`告诉客户,结果可以再使用多久. `cacheScope`描述谁可能分享存储值.

> `ttlMs`告诉客户端一个结果可以被重复使用很久.`cacheScope`描述谁可以分享该缓存值.

| Scope | Meaning | Typical use |
|---|---|---|
| `public` | May be reused across users when authorization permits | Public prompt catalog |
| `private` | Bound to the requesting user or credential context | User-owned note content |

根据数据的变化速度和延迟损害,选择一个TTL.五分钟可能适合公开提示目录.私人笔记阅读可能需要一分钟.

> 根据数据的变化速度和过时的价格选择 TTL──公共提示目录五分钟可能合适;私人笔记阅读可能用一分钟──

只有MCP定义了`public`其他`private`作为`cacheScope`对于一个秘密的结果或快速变化的结果,返回`cacheScope: "private"`随着`ttlMs: 0`通过"存储器"的方法,`no-store`本身不是MCP`cacheScope`价值

> 只有定义的MCP`public`和 `private`作为一个`cacheScope`值――对携带秘密或快速变化的结果,返回`cacheScope: "private"`加  `ttlMs: 0`后,在主机缓存策略中应用任何更严格的无店规则.`no-store`没有MCP的`cacheScope`值

缓存提示永远不会取代授权.缓存密钥必须包含所有改变可见性的请求维度,包括租户,用户,范围,本地和页面化缓冲器.如果共享缓存无法安全表达这些维度,则使用`private`没有任何店铺政策.

> 缓存提示永远不能取代授权.缓存键必须包含每个可见变化的请求维度,包括租户,用户,范围,语言和分页游标.`private`增加零的TL 和宿主级无店 策略

## 订阅使用客户端开放的响应流

> **【中文解读】**现代订阅模式取代了旧的`resources/subscribe`事件端点――客户端把 `subscriptions/listen`作为普通的JSON-RPC 请发出;在流式HTTP上,这是一个 POST,其响应保持开放成为SSE流.`notifications`目标是允许清单服务器不得发送未请求的通知类型――请求 ID就是订阅 ID;在任何请求事件之前,服务器先发`notifications/subscriptions/acknowledged`过器只包含服务器接受的子集;流上后续的每一个事件都带着相同的`subscriptionId`据悉, 报道只说"资源变了",客户端必须通过.`resources/read`重新读取并重新过当前授权不要假设事件里带有新文档──不要把订阅流当协议会话使用:后续读取仍然可落到任意健康实例的完整请求──

现代订阅模式取代了前一种模式.`resources/subscribe`通过RPC和旧的HTTP GET事件终点.

> 现代订阅模式取代了前者`resources/subscribe`事件端点.

客户发送了`subscriptions/listen`通过流式HTTP,这是一个POST,其响应仍然作为SSE流开放.`notifications`服务器不得提供未请求的通知类型.

> 客户端把 `subscriptions/listen`作为普通的JSON-RPC 请发送. 在流式HTTP上,这是一个 POST,其响应保持开放成为SSE流.`notifications`服务器不得发送未请求的通知类型.

```json
{
  "jsonrpc": "2.0",
  "id": 17,
  "method": "subscriptions/listen",
  "params": {
    "_meta": {
      "io.modelcontextprotocol/protocolVersion": "2026-07-28",
      "io.modelcontextprotocol/clientCapabilities": {},
      "io.modelcontextprotocol/clientInfo": {
        "name": "course-client",
        "version": "1.0.0"
      }
    },
    "notifications": {
      "resourcesListChanged": true,
      "promptsListChanged": true,
      "resourceSubscriptions": [
        "notes://note-1"
      ]
    }
  }
}
```

请求 ID 是订阅 ID. 在任何请求事件之前,服务器发送`notifications/subscriptions/acknowledged`服务器只接受的子集.

> 在任何被请求事件之前,服务器发送`notifications/subscriptions/acknowledged`△其过器只包含服务器接受的子集──

```json
{
  "jsonrpc": "2.0",
  "method": "notifications/subscriptions/acknowledged",
  "params": {
    "_meta": {
      "io.modelcontextprotocol/subscriptionId": 17
    },
    "notifications": {
      "resourcesListChanged": true,
      "resourceSubscriptions": [
        "notes://note-1"
      ]
    }
  }
}
```

后来的每一个事件都包含相同的元数据.

> 后续的每一次事件都带着相同的数据.

```json
{
  "jsonrpc": "2.0",
  "method": "notifications/resources/updated",
  "params": {
    "_meta": {
      "io.modelcontextprotocol/subscriptionId": 17
    },
    "uri": "notes://note-1"
  }
}
```

客户端再次阅读了它.`resources/read`根据目前的授权,它不假设事件包含新的文件.

> 通知说是"资源变了"――客户端通过`resources/read`重新读取,并接受当前授权的约束.

通过 HTTP,关闭响应流取消订阅.一个结束流的服务器优雅地返回一个最终的 服务器 通过 HTTP 关闭响应流取消订阅.`resultType: "complete"`与原始请求相关的反应.

> 多个订阅可以共享一个工作室通道――订阅ID 让客户端能够对它们进行分流――在HTTP上,关闭响应流即取消订阅――优雅结束流的服务器返回与原始请求关联的最终`resultType: "complete"`响应.

您不能使用订阅流作为协议会议. 后续阅读仍然是完整的请求,可以达到任何健康的服务器实例.

> 后续阅读仍可达成任意健康服务器实例的完整请求.

```figure
t3-primitive-sort
```

## 互动实验室互动练习

使用这个图表来分类一个项目跟踪器的五个功能:问题细节,创建问题,冲刺审查模板,项目政策和关闭问题.然后决定哪些列表可以向公众缓存,哪些列表必须保持私密,哪些资源应该更新通知.

> 查看项目跟踪器的五种能力分类:问题 详情 创建问题 代评模板 项目政策 关闭问题 然后决定哪些列表可以公开缓存 哪些读取必须保持私有 哪些资源值更新通知 

如果模型执行操作,请使用工具.如果主机阅读了URI地址的内容,请使用资源.如果用户启动一个准备的消息工作流程,请使用提示.

> 对于每个分类,说出"谁在选择"――模型执行动作用工具;主播读取URI寻址的内容资源;用户启动预制消息工作流用提示――

## 实践实验室 实践实践

> **【中文解读】**按给定的顺序检查转录:发现公告当前修订和两种能力;两个列表结果有序和`resultType: "complete"`列表和读取结果带着刻意设置的缓存提示;把读取URI改成`notes://missing`观察`-32602`订阅确认先于资源事件;事件与优雅关闭都携带订阅 ID 5。注意:Python 模型不开真实HTTP 连接,它呈现的是SDK 必须放到请求级响应流上的消息;生产环境使用官方SDK做组与传输──

运行模拟器从存储器根:

```bash
cd phases/13-tools-and-protocols/10-mcp-resources-and-prompts/code
python3 main.py
python3 -m unittest discover tests -v
```

检查转录的顺序:

1. 确认`server/discover`广告目前的修改和两项功能.
   中文翻译:确认 `server/discover`广告当前修订和两种能力
2. 确认列表结果均有序,并使用`resultType: "complete"`现在,我们要去.
   中文翻译:确认两个列表结果有序且使用`resultType: "complete"`,我知道.
3. 确认列表,并阅读结果带有故意缓存提示.
   中文翻译:确认列表和读取结果带有意图设置的缓存提示──
4. 改变读取URI为`notes://missing`观察`-32602`现在,我们要去.
   中文翻译:把读取URI 改成`notes://missing`观察`-32602`,我知道.
5. 确认订阅确认之前的资源事件.
   中文翻译:确认订阅确认先于资源事件──
6. 确认活动,并以优雅的方式关闭,同时携带订阅身份证.`5`现在,我们要去.
   中文翻译:确认事件与优雅关闭都携带订阅身份证 `5`,我知道.

 Python 模型不会打开真正的 HTTP 连接.它代表一个 SDK 必须在请求范围响应流中放置的信息.使用官方 SDK 为框架和输送在生产中.

>  Python 模型不开真实的 HTTP 连接. 它呈现的是 SDK 必须放到请求级响应流上的消息.

## 运送的艺术品产品

`outputs/skill-primitive-splitter.md`是MCP原始选择的可重复使用设计审查.它现在检查了确定性发现,缓存范围,无效的URI行为和现代订阅过器.

> `outputs/skill-primitive-splitter.md`是一个可复制的MCP 原语选择设计评审. 它现在检查确定性发现,缓存范围,无效的URI行为和现代订阅过器.

课程也会带来影响.`assets/primitive-split.svg`对于非线学习,原始和订阅界限的静态版本.

> 本课还附带`assets/primitive-split.svg`作为一个学习的原语和订阅边界的静态版本.

## 检查一下.

```bash
cd phases/13-tools-and-protocols/10-mcp-resources-and-prompts/code
python3 main.py
python3 -m unittest discover tests -v
```

预期结果:主程序打印一个JSON转录,测试命令报告至少12次通过测试.

> 预期结果:主程序打印一个JSON转录,测试命令报告至少12次通过测试.

## 毕业项目 接下来

包含一个确定性目录快照,一个授权资源阅读,一个快速分辨率,一个不有效的URI案例和一个订阅转录.

> 当你的毕业项目服务器在动作之外暴露可寻址知识时,使用本契约.

您的证据应该表明,没有列表依赖于连接历史,并且订阅事件从来没有允许访问底层资源.

> 你的证据表明:没有任何列表依赖于连接历史,并且订阅事件绝对不授予访问底层资源.

## 练习题

1. 添加一个`notes://projects/{project}/notes/{id}`资源模板并验证两个变量.
   中文翻译:添加 `notes://projects/{project}/notes/{id}`资源模板并校验两个变量.
2. 添加页面`resources/list`保持确定性秩序.
   中文翻译:给`resources/list`增加分页,同时保持确定性排序.
3. 改变一个资源为`cacheScope: "private"`随着`ttlMs: 0`添加一个主机级别的禁店政策,并解释了这两个控制的威胁.
   中文翻译:把一个资源改为`cacheScope: "private"`加  `ttlMs: 0`并且同时需要这两个控制器的威胁模型.
4. 添加提示列表变更订阅,证明当过器遗漏时没有发送事件`promptsListChanged`现在,我们要去.
   中文翻译:添加提示列表变更订阅,并证明过器省略 `promptsListChanged`时不发送事件――
5. 创建两个同时订阅,证明每个事件都包含了正确的请求ID.
   中文翻译:创建两个同时存在的订阅,证明每个事件都携带正确的请求ID──
6. 添加一个被读取处理器的权限,证明缓存输入不能跨越主题.
   中文翻译:给读取处理器加授权主体,并证明缓存条目不能跨主体――

## 关键词 快速查找表

- **Resource:**通过MCP服务器暴露的URI地址内容.
  中文翻译:资源MCP 服务器暴露的URI 寻址内容──
- **Prompt:**通过MCP服务器暴露的用户控制信息模板.
  中文翻译:提示MCP 服务器暴露的用户控制消息模板。
- **Deterministic list:**发现结果,有稳定的成员和订单相同的请求输入.
  中文翻译:确定性列表对相同请求输入具有稳定成员和排序的发现结果.
- **`ttlMs`:**缓存新鲜度持续时间在毫秒.
  中文翻译:缓存新鲜期,单位毫秒――
- **`cacheScope`:**为了缓存结果的共享界限.
  中文翻译:缓存结果的共享边界――
- **`subscriptions/listen`:**长期的请求,其响应流提供了明确过的通知.
  中文翻译:长生命周期请求,其响应流流投递经过显式过的通知.
- **Subscription ID:**听取请求的原始身份证,在通知元数据中重复.
  中文翻译:订阅 ID原始听 请求 ID,在通知元数据中重复出现。
- **Invalid parameters:** JSON-RPC 错误`-32602`用于无效或未知资源URI.
  中文翻译:无效参数JSON-RPC 错误 `-32602`用于无效或未知的资源URI.
- **Unsupported protocol version:** JSON-RPC 错误`-32022`包括`supported`其他`requested`修订
  中文翻译:不支持的协议版本JSON-RPC 错误 `-32022`包含`supported`和 `requested`修订:
- **`server/discover`:**强制性服务器方法,返回支持的修改,功能,身份和可选缓存提示.
  中文翻译:强制服务器方法,返回支持修改,能力,身份和可选缓存提示.

## 继续阅读 继续阅读

- [MCP 2026-07-28 Resources](https://modelcontextprotocol.io/specification/2026-07-28/server/resources)
  中文翻译:资源契约的权威规范`-32602`语义)
- [MCP 2026-07-28 Prompts](https://modelcontextprotocol.io/specification/2026-07-28/server/prompts)
  中文翻译:提示契约的权威规范
- [MCP 2026-07-28 Subscriptions](https://modelcontextprotocol.io/specification/2026-07-28/basic/patterns/subscriptions)
  翻译: 中文`subscriptions/listen`订阅模式规范
- [MCP 2026-07-28 Caching](https://modelcontextprotocol.io/specification/2026-07-28/basic/utilities/caching)
  翻译: 中文`ttlMs`现在,我们要去.`cacheScope`缓存提示语义
