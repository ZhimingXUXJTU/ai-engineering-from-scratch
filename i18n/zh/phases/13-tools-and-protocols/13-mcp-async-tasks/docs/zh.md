# 扩展:无状态内核上的持久化任务

> 无国籍MCP并不意味着每个操作都必须在一个请求中完成.官方任务扩展提供了长时间工作的明确持久的手柄.`tools/call`任何一个例子都能回答.`tasks/get`通过客户输入`tasks/update`没有恢复协议会议.

> **【中文解读】**无状态MCP 不等于每个操作都必须在一个请求内完成. 官方任务 扩展到长时间运行的工作`tools/call`返回句柄,任何实例都能应答`tasks/get`客户端输入通过`tasks/update`送达全程不需要复活协议会话――注意本课已完全改版:从2025-11-25的实验性核心特性(SEP-1686) 迁移为官方`io.modelcontextprotocol/tasks`扩展,方法面也换了`tasks/status`,我知道.`tasks/result`,我知道.`tasks/list`已移除) 』

> **【拓展：持久化任务→Agent 长时运行工作】**异步任务是MCP处理长时间运行工作的标准模式:深度研究,代码生成,批量导出,需要几分钟到几小时的工作.`tools/call`不同,让服务器先持久化再返回任务Id,客户端稍后轮询快照或订阅通知.

>  **【前置】**课本节前请先掌握:(1) 阶段13·09(运输) 可流的HTTP的POST/SSE形态,本课的 `Mcp-Method`现在,我们要去.`Mcp-Name`头直接建立在它上; (2) 阶段13·11`inputRequests`现在,我们要去.`inputResponses`机器;(3) 阶段13·12(发出) 任务执行中收集用户输入的就是同一套表单方案──

**Type:** Build | **类型:** 构建
**Languages:** Python | **语言:** Python
**Prerequisites:** Phase 13 · 09 (transports), Phase 13 · 11 (stateless MRTR), Phase 13 · 12 (elicitation) | **前置知识:** Phase 13 · 09（transports）、Phase 13 · 11（无状态 MRTR）、Phase 13 · 12（elicitation）
**Time:** ~90 minutes | **时间:** 约 90 分钟

## 学习目标

- 区分无状态协议运输与耐用应用任务状态.
  中文翻译:区分无状态的协议传输与持久化应用任务状态.
- 谈判`io.modelcontextprotocol/tasks`扩大每次请求能力`server/discover`现在,我们要去.
  中文翻译:在按请求能力与`server/discover`中协商 `io.modelcontextprotocol/tasks`扩展.
- 返回一个服务器导向的`CreateTaskResult`随着`resultType: "task"`只有在永恒的创造之后.
  中文翻译:只有在持久化创建完成后才回带`resultType: "task"`的服务器主导`CreateTaskResult`,我知道.
- 调查`tasks/get`完成任务输入`tasks/update`要求合作取消`tasks/cancel`现在,我们要去.
  中文翻译:用`tasks/get`轮询 用`tasks/update`补充任务输入 用`tasks/cancel`请求协作式取消――
- 删除老人`tasks/status`现在`tasks/result`其他`tasks/list`假设
  中文翻译:清除旧版 `tasks/status`,我知道.`tasks/result`和 `tasks/list`假设.
- 通过 订阅可选任务通知`subscriptions/listen`在 POST 响应 SSE 流上.
  中文翻译:通过 POST 响应 SSE 流上 `subscriptions/listen`订阅可选任务通知.
- 模型任务过期,重新启动恢复,输入键的排版,以及执行错误正确.
  中文翻译:正确建模任务过期、重启恢复、输入键去重复和执行错误――

## 为什么任务是扩展?为什么任务变得扩展?

> **【中文解读】**任务最初是2025-11-25的实验性核心特性.当时称之为SEP-1686 任务增强.`io.modelcontextprotocol/tasks`扩展客户端和服务器按需选择加入这个额外生命周期,而不是让所有人为核心协议购买单单. 扩展规范目前仍在草案表面:锁定SDK支持的扩展版本,运行一致性场景,将线上适应器与工作器和存储领域隔离.

任务首次在2025年1月25日出现为实验核心功能.`io.modelcontextprotocol/tasks`扩展,使客户和服务器可以选择额外的生命周期,

> 任务最初作为实验性核心特性出现了2025年7月2026年重新设计将它们转移到官方的位置.`io.modelcontextprotocol/tasks`扩展,让客户端和服务器按需选择加入此套额外生命周期,而不需要所有人扩大核心协议.

扩展规范仍然是一个草稿表面,尽管它是目前的官方主页任务. 插入 SDK 支持的扩展版本,运行符合性场景,并将线索适配器从您的工作者和存储域中隔离.

> 扩展规范目前仍然是草案表面,尽管它已经是目前的官方归宿.

使用操作具有以下一个或多个特性时的任务:

> 当操作具有以下一个或多个属性时使用任务:

- 要求时间可能超过普通的要求时间.
  中文翻译:它可能超越普通请求的超时时间.
- 工人队列或外部工作系统已经拥有执行.
  中文翻译:某个工作队列或外部作业系统已经拥有执行权.
- 客户需要恢复,
  中文翻译:客户端需要在自己的重启后恢复.
- 执行过程中,操作暂停用户或模型输入.
  中文翻译:操作在执行中会暂停等待用户或模型输入.
- 取消和持久的结果检索是产品要求.
  中文翻译:取消和持久化结果获取是产品需求.

没有什么可做,但我们必须要做一个好事.

> 不要为廉价确定性寻找创建任务.

## 无状态内核,有状态应用

> **【中文解读】**现在,我们在学习中学习了.`initialize`,我知道.`notifications/initialized`协议会话和`Mcp-Session-Id`但这不禁止有状态的产品.任务 id 是显而易见的应用状态:先持久化再返回;客户端可以存活下来,再启动后再轮询;ID可以路由到同一持久存储后的任何副本;每次任务方法调用都重新进行授权检查;过期和删除由任务字段定义,而不是传输生命周期.

移除MCP 2026-07-28 `initialize`现在`notifications/initialized`会议,`Mcp-Session-Id`这并不禁止有国产.

> 移除了`initialize`,我知道.`notifications/initialized`协议会话和`Mcp-Session-Id`,这并不禁止有状态的产品.

任务 id 是明确的应用状态:

> 任务 id 是显而易见的应用状态:

- 在返回之前,服务器坚持使用.
  中文翻译:服务器先持久化它再返回──
- 客户可以重新启动后存储并进行重新调查.
  中文翻译:客户端可以存储它,重启后再次轮询.
- 身份证可以向任何复制品提供相同的持久商店的支持.
  中文翻译:该ID可以路由到同一持久存储支的任何副本.
- 每个任务方法都会检查授权.
  中文翻译:每次任务方法调用都检查授权.
- 过期和删除由任务领域定义,而不是运输寿命.
  中文翻译:过期与删除由任务字段定义,而不是传输生命周期.

这从操作上来看,与连接连接的隐藏状态不同.

> 这在运维上不同于在连接上隐藏的状态.

让四个生命分开:

> 分开四个生命周期:

| State | Lifetime | Where it belongs |
|---|---|---|
| Protocol metadata | One request | `params._meta`, validated again on every call |
| Transport work | One stdio request or HTTP response | In-flight coordinator with a bounded deadline |
| MRTR continuation | One retry sequence | Integrity-protected `requestState`, plus replay controls when needed |
| Durable task | Across requests, replicas, restarts, and reconnects | Shared application store keyed by an authorized `taskId` |

> 表格对照(zh 版):协议元数据单个请求`params._meta`通过每次调用都重新进行;传输工作单个工作室请求或HTTP响应带有有限的截止时间的路由协调器;MRTR 续接单个重试序列完整性保护`requestState`需要加重控制; 持久任务跨请求,副本,重启和重连授权`taskId`为了关键的共享应用存储.

移动一个任务记录到进程内存并不能使MCP变得状态.`tasks/get`继续前回手柄,然后让每个任务方法在租户和主管检查下解决相同的共享记录.

> 将任务记录放入进程内存不会使MCP变为状态,只会使应用不可靠.协议保持无状态,但后来路由到另一个副本.`tasks/get`无法恢复该记录. 首先持久化再返回句子,然后让每个任务方法在租户和主体检查下解析相同的共享记录.

>  **【类比】**任务像餐厅的取餐号,但换成"连锁店通"模式:你在 A 店点餐 (工具/调用),小票上是取餐号 42(任务Id) 它存在连锁总部的订单系统 (连锁总部的订单系统) 持久存储) 里,不是某个店员的脑子里 (进程内存) 里.你可以去任何分店问"42号好吗" ("任务/获路由到任意副本);中店员问你不要加 (你需要输入_),你答一句话 ((任务/更新);不想随时单任务/退货) .旧的"柜台"就是同步调用等等等;旧的"SEP-1686 站员 站 响应员工"的"店 协议没有你一直可以回来.

## 能力谈判能力谈判

客户在每一个符合条件的请求上宣告支持:

> 客户端在每个符合条件的请求上声明支持:

```json
{
  "_meta": {
    "io.modelcontextprotocol/protocolVersion": "2026-07-28",
    "io.modelcontextprotocol/clientCapabilities": {
      "extensions": {
        "io.modelcontextprotocol/tasks": {}
      }
    },
    "io.modelcontextprotocol/clientInfo": {
      "name": "lesson-client",
      "version": "1.0.0"
    }
  }
}
```

服务器返回了确切的信息`supportedVersions`其他国家`ttlMs`其他`cacheScope`其他`server/discover`由于它宣传工具,它也实施强制性`tools/list`这结果返回了确定性`generate_report`描述符,有效的对象`inputSchema`现在`resultType: "complete"`服务器身份元数据,以及公共缓存提示.

> 服务器从`server/discover`返回精确的`supportedVersions`能力`ttlMs`和 `cacheScope`由于它声明工具,所以也实现强制性`tools/list`△该结果返回确定性`generate_report`描述符,合法的对象`inputSchema`,我知道.`resultType: "complete"`、服务器身份元数据和公开缓存提示──

没有声明延长返回的客户端的任务方法`-32021`缺失客户能力,`data.requiredCapabilities`设置为`{"extensions":{"io.modelcontextprotocol/tasks":{}}}`没有支持的协议链返回`-32022`确切的`supported`其他`requested`输出数据; 输出缺失或非字符串版本 `-32602`现在,我们要去.

> 没有声明扩展的客户端发出任务方法时返回`-32021`(缺少必需客户端能力),`data.requiredCapabilities`设为`{"extensions":{"io.modelcontextprotocol/tasks":{}}}`△不支持的协议字符串返回 `-32022`并附精确的`supported`与`requested`数据;缺失或非字符串的版本返回 `-32602`,我知道.

没有JSON-RPC的封面`id`接收器可能会处理它,但它不会发出任何JSON-RPC结果或错误.`202 Accepted`没有接受通知的机构.

> 没有JSON-RPC`id`收件者可以处理它,但不会发出JSON-RPC 结果或错误.`202 Accepted`,我知道.

目前,只有`tools/call`设计您的内部抽象,以便未来的请求类型不需要重写存储.

> 目前只有`tools/call`支持任务增强执行. 设计内部抽象时,让未来的请求类型不需要重写存储.

## 服务器导向任务创建

> **【中文解读】**这与旧版本最大的方向变化:旧客户端标志`params._meta.task.required`没有了.现在客户端只声明扩展支持,服务器决定某种.`tools/call`是否成为任务返回`resultType: "task"`加  `taskId`,我知道.`status`,我知道.`ttlMs`,我知道.`pollIntervalMs`等字段──关键规则是持久前回归:在`tasks/get`能解析该 id 之前,服务器不得返回句柄;最终一致存储必须先等阅读可见.

旧客户旗`params._meta.task.required`客户端宣布扩展支持,然后服务器决定是否提供特定的服务器.`tools/call`成为一个任务.

> 旧客户端标志`params._meta.task.required`没有了. 客户端声明扩展支持,然后服务器决定某种.`tools/call`是否成为任务.

要求:

> 求你:

```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "method": "tools/call",
  "params": {
    "name": "generate_report",
    "arguments": {"size": "large"},
    "_meta": {
      "io.modelcontextprotocol/protocolVersion": "2026-07-28",
      "io.modelcontextprotocol/clientCapabilities": {
        "extensions": {
          "io.modelcontextprotocol/tasks": {}
        }
      }
    }
  }
}
```

答案:

> 响应:

```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "result": {
    "resultType": "task",
    "taskId": "tsk_786512e29e0d",
    "status": "working",
    "statusMessage": "Preparing report outline.",
    "createdAt": "2026-08-21T10:30:00Z",
    "lastUpdatedAt": "2026-08-21T10:30:00Z",
    "ttlMs": 900000,
    "pollIntervalMs": 1000
  }
}
```

服务器不得返回此手柄,直到一个`tasks/get`在最终一致的存储中,在回答之前等待读取可见性.否则客户端可以收到一个有效的ID,然后立即得到"没有找到".

> 在`tasks/get`在最终一致的存储中,应答前要等待可见.否则客户端可能会得到一个看起来合法的ID,紧接着就得到"未找到"――

任务响应是未要求的,即客户端不要求任务模式. 它并非未经谈判:当前的请求仍然必须广告扩展.

> 任务响应在"客户端没有请求任务模式"的意义上是未经请求的.

> ️ **【易错点】**场景:先返回任务Id 再异步写存储 / 后果:客户端立刻 `tasks/get`获取"未找到",重试风暴或用户以为任务丢失;多副本部署下别的副本更是必然查不到 / 修复:坚持持持久前回报先持久化(最终一致存储要等阅读可见) 再返回句柄;`ttlMs`从创建时起算,是底而不是"完成后保留结果的承诺".

## 任务形状的数据形状

每个任务都包含:

> 每个任务都带着:

- `taskId`:稳定服务器生成的标识符;
  翻译: 中文`taskId`:服务器生成的稳定标识符;
- `status`其他`working`现在`input_required`现在`completed`现在`cancelled`其他`failed`其他
  翻译: 中文`status`其他:`working`,我知道.`input_required`,我知道.`completed`,我知道.`cancelled`或`failed`其他
- `createdAt`其他`lastUpdatedAt`:ISO 8601时间标签;
  翻译: 中文`createdAt`与`lastUpdatedAt`时间:ISO 8601 时间;
- `ttlMs`:自创建到期,或`null`没有广告的限制;
  翻译: 中文`ttlMs`创建起算的过期时间长,`null`表示不声明上限;
- 选择性`pollIntervalMs`:服务器目前的最低建议投票时间;
  中文翻译:可选的`pollIntervalMs`服务器当前建议的最小轮询间隔;
- 选择性`statusMessage`面向用户或面向模型的环境.
  中文翻译:可选的`statusMessage`面向用户或模型的上下文说明:

只有当相关时,状态特定的字段才会出现:

> 状态相关字段只在相关时出现:

- `input_required`包括`inputRequests`现在,我们要去.
  翻译: 中文`input_required`包含`inputRequests`,我知道.
- `completed`包括原本请求的文件`result`它们的形状.
  翻译: 中文`completed`包含原始请求的`result`形状――
- `failed`包含一个JSON-RPC`error`它们是什么?
  翻译: 中文`failed`包含JSON-RPC`error`象征

客户应该尊重`pollIntervalMs`服务器可能会限制更具攻击性的民意调查,并且可能会在任务寿命中改变间隔.

> 客户端应遵守`pollIntervalMs`服务器可以对更激进的轮流限制进行调整,也可以在任务生命周期内改变此间隔.

## 调查`tasks/get`现在我在做什么?`tasks/get`轮询

客户端要求一个当前的快照:

> 客户端请求当前快照:

```http
POST /mcp HTTP/1.1
Content-Type: application/json
MCP-Protocol-Version: 2026-07-28
Mcp-Method: tasks/get
Mcp-Name: tsk_786512e29e0d
```

```json
{
  "jsonrpc": "2.0",
  "id": 2,
  "method": "tasks/get",
  "params": {
    "taskId": "tsk_786512e29e0d",
    "_meta": {
      "io.modelcontextprotocol/protocolVersion": "2026-07-28",
      "io.modelcontextprotocol/clientCapabilities": {
        "extensions": {
          "io.modelcontextprotocol/tasks": {}
        }
      }
    }
  }
}
```

`tasks/get`结果总是有着`resultType: "complete"`嵌的任务仍然可以得到`status: "working"`或`status: "input_required"`现在,我们要去.

> `tasks/get`结果总是这样.`resultType: "complete"`嵌套的任务仍然可能是`status: "working"`或`status: "input_required"`,我知道.

这种区别可以防止一个常见的解析器错误:

> 这个区分可以防止常见的解析器 bug:

```text
result.resultType = complete    means the tasks/get RPC finished
result.status = working        means the represented job is still running
```

> 对于照翻译:`result.resultType = complete`表示任务/得到这个 RPC 结束了;`result.status = working`表示它所代表的任务还在运行.

没有.`tasks/result`接下来,我们将会做一个任务.`tasks/get`答案是原始的`CallToolResult`根据`result`其他:

> 没有`tasks/result`调用.任务完成后,下一次.`tasks/get`响应把原始的`CallToolResult`内部的关系`result`下:

```json
{
  "resultType": "complete",
  "taskId": "tsk_786512e29e0d",
  "status": "completed",
  "createdAt": "2026-08-21T10:30:00Z",
  "lastUpdatedAt": "2026-08-21T10:34:12Z",
  "ttlMs": 900000,
  "result": {
    "resultType": "complete",
    "content": [
      {"type": "text", "text": "Generated large report with approved outline."}
    ],
    "structuredContent": {"size": "large", "approved": true},
    "isError": false,
    "_meta": {
      "io.modelcontextprotocol/serverInfo": {
        "name": "tasks-demo",
        "version": "1.0.0"
      }
    }
  },
  "_meta": {
    "io.modelcontextprotocol/serverInfo": {
      "name": "tasks-demo",
      "version": "1.0.0"
    }
  }
}
```

外面的`resultType`现在,`tasks/get`完成了. 嵌套`result.resultType`需要一个嵌套的区分符.`CallToolResult`应该还要带着自己的.`io.modelcontextprotocol/serverInfo`没有类型的有效载荷的存储,

> 层外`resultType`解释`tasks/get`现在,我们已经完成了.`result.resultType`解释原始工具调用完成了. 嵌套的判定符是必需的.`CallToolResult`应该带着自己的东西.`io.modelcontextprotocol/serverInfo`本课包含它,而不是存在无类型的负载.

没有.`tasks/list`无会议服务器无法安全地推断哪些任务属于连接范围列表.需要历史记录的应用程序应该暴露出一个有权限的域名工具,有明确的过器和所有权规则.

> 没有`tasks/list`△无会话服务器无法安全地推断哪些任务属于某个连接范围列表.

>  **【困惑】**旧的`tasks/status`,我知道.`tasks/result`没有直观吗?为什么合并成一个?`tasks/get`答:因为旧方法包含"会话能圈定任务集合"的假设.`taskId`定位任务,那就没有理由为"状态"和"结果"分设两个方法`tasks/get`一次回归完整快照,完成时内联结果.`tasks/list`被移除:需要列表就做一个显而易见的领域工具,自我定义过与授权.

## 在执行任务时输入 任务执行中的输入

任务输入和核心MRTR看起来相似,但使用不同的延续.

> 任务输入与核心MRTR看起来相似,但使用不同的续航方式.

### 任务创建前所需的输入

返回核心`resultType: "input_required"`根据原始的版本`tools/call`客户端完成了任务,然后再尝试原来的调用,

> 在原始`tools/call`返回核心`resultType: "input_required"`△客户端补充全它并重试原始调用. 只有等这些同步MRTR轮次结束后才创建任务.

### 任务创建后所需的输入

设定任务`input_required`现在,我们要去.`tasks/get`揭示了突出的`inputRequests`客户通过`tasks/update`客户不会再试原始`tools/call`现在,我们要去.

> 把任务置为`input_required`,我知道.`tasks/get`暴露未决的`inputRequests`通过客户端`tasks/update`发送响应──客户端不重试原始的 `tools/call`,我知道.

> **【中文解读】**输入时机决定续航方式,这是新规范里最容易混的点:创建任务前缺输入走核心MRTR(`input_required`结果 + 客户端重试原始 `tools/call`创建任务后缺输入 走任务输入 任务状态置`input_required`客户端使用`tasks/update`应答,不再重试原调用) ⋅每条 `inputRequests`关键在任务的整个生命周期中必须是唯一的,客户端按键重重,服务器忽略未知/已废/已应答的键.

快速拍摄:

> 快照:

```json
{
  "resultType": "complete",
  "taskId": "tsk_786512e29e0d",
  "status": "input_required",
  "createdAt": "2026-08-21T10:30:00Z",
  "lastUpdatedAt": "2026-08-21T10:31:00Z",
  "ttlMs": 900000,
  "inputRequests": {
    "approve_outline": {
      "method": "elicitation/create",
      "params": {
        "mode": "form",
        "message": "Approve the generated report outline?",
        "requestedSchema": {
          "type": "object",
          "properties": {"approved": {"type": "boolean"}},
          "required": ["approved"]
        }
      }
    }
  }
}
```

更新:

> 更新:

```http
POST /mcp HTTP/1.1
Content-Type: application/json
MCP-Protocol-Version: 2026-07-28
Mcp-Method: tasks/update
Mcp-Name: tsk_786512e29e0d
```

```json
{
  "jsonrpc": "2.0",
  "id": 4,
  "method": "tasks/update",
  "params": {
    "taskId": "tsk_786512e29e0d",
    "inputResponses": {
      "approve_outline": {
        "action": "accept",
        "content": {"approved": true}
      }
    },
    "_meta": {
      "io.modelcontextprotocol/protocolVersion": "2026-07-28",
      "io.modelcontextprotocol/clientCapabilities": {
        "extensions": {
          "io.modelcontextprotocol/tasks": {}
        }
      }
    }
  }
}
```

成功的反应是空白的承认,加上`resultType: "complete"`总之,客户继续进行投票或听取.

> 成功响应是空确认加加`resultType: "complete"`△状态变更可能是最终一致的,所以客户端继续询问或监听.

每个`inputRequests`重复  重复 重复 重复 重复`tasks/get`快照可能显示相同的未完成密钥;客户端将UI复制,服务器忽略对未知,取代或已经完成的密钥的响应.`input_required`在所有必要的钥匙被回答之前.

> 每条`inputRequests`关键在任务的整个生命周期必须是唯一的.`tasks/get`快照可能显示相同未决键;客户端对UI进行重负,服务器忽略对未知已废或已应答键的响应.`input_required`直到所有必需关键都得到了答案.

## 取消是合作式的

`tasks/cancel`工作人员的工作可能会先完成,忽略取消或过渡.

> `tasks/cancel`表明意图并返回空空的完成确认――该确认不保证工作器已停止――工作可能先完成、忽略取消或稍后才转移状态――

```http
POST /mcp HTTP/1.1
Content-Type: application/json
MCP-Protocol-Version: 2026-07-28
Mcp-Method: tasks/cancel
Mcp-Name: tsk_786512e29e0d
```

```json
{
  "jsonrpc": "2.0",
  "id": 5,
  "method": "tasks/cancel",
  "params": {
    "taskId": "tsk_786512e29e0d",
    "_meta": {
      "io.modelcontextprotocol/protocolVersion": "2026-07-28",
      "io.modelcontextprotocol/clientCapabilities": {
        "extensions": {
          "io.modelcontextprotocol/tasks": {}
        }
      }
    }
  }
}
```

对于所有三个任务方法,`Mcp-Name`镜子`params.taskId`没有重复JSON-RPC方法名称. `code/main.py`们的们在`make_http_request`现在,我们要去.

> 对于所有三个任务方法,`Mcp-Name`镜像`params.taskId`△它不重复JSON-RPC 方法名──`code/main.py`在`make_http_request`中集中实现了这一条规则.

课程工作者立即尊重取消,并会重复打电话无权.

> 本课程的工作器立即响应取消,使重复调用等.

不要使用`notifications/cancelled`通知属于取消请求,而不是持久任务.

> 不要使用`notifications/cancelled`取消任务――那个通知属于取消请求而不是持久化任务――

> **【中文解读】**记住两条分界线:(1) `notifications/cancelled`取消的是"请求",`tasks/cancel`取消的是"任务"一旦`tools/call`已回归`resultType: "task"`要求已经完成, 断开连接, 没有完成任务;`tasks/cancel`确认只代表"意图已记录",不代表工作器已停止生产客户端从后续`tasks/get`快照确认终态,而不是确认推断.

要求取消是针对飞行中一个JSON-RPC操作或其请求范围的HTTP响应.`tools/call`已经回来了`resultType: "task"`要求已完成,关闭运输不能提及或停止持久的工作. `tasks/cancel`具有授权的新PCP.`params.taskId`镜像是个身份证`Mcp-Name`解决任务的后端,记录合作伙伴取消意图,并返回确认,而不要求工人停止.

> 要求取消针对正在进行的 JSON-RPC 操作或其请求范围的 HTTP 响应.`tools/call`已回归`resultType: "task"`要求已经完成,关闭其传输既无法点名也无法停止那个持久任务.`tasks/cancel`是一个新的授权PC.`params.taskId`在`Mcp-Name`中镜像该 id、解析任务归属后端、记录协作取消意图,并返回确认但不声称工作器已停止

通过一个网关,请求协调器和任务路线必须在不同的表格中存储.请求表可能会在响应完成时消失.任务路线必须存活到终端状态和保留期限到期. [Lesson 29: MCP Reliability, Cancellation, and Flow Control](../../29-mcp-reliability-cancellation-and-flow-control/docs/en.md)建立竞赛,时间过期,无力,压力,再试规则.

> 因此,网关必须把请求协调器和任务路由放在不同的表中.请求表可以在响应结束后消失.任务路由必须存活到终态和保留期过期.[Lesson 29: MCP Reliability, Cancellation, and Flow Control](../../29-mcp-reliability-cancellation-and-flow-control/docs/en.md)构建了两条竞争,超时,等,背压和重试规则.

## 选择性通知

客户想要推送更新的发送`subscriptions/listen`对于 Streamable HTTP,这是一个 POST,其响应是请求-scoped SSE 流.没有独立的 GET 事件流和没有协议会议保持活跃.

> 轮询是基线. 想要推送更新的客户端发送携带任务ID的.`subscriptions/listen`△对流式HTTP而言,这是一个POST,其响应是请求范围的SSE流.

服务器确认接受的ID`notifications/subscriptions/acknowledged`然后可以通过全息图发送`notifications/tasks`确认和每项任务通知都包含`io.modelcontextprotocol/subscriptionId`在`_meta`等于`subscriptions/listen`要求 id. 其他情况下,每个任务通知等于`tasks/get`现在,我会回来.

> 服务器用`notifications/subscriptions/acknowledged`确认被接受的身份证,然后可以通过`notifications/tasks`发送完整快照. 确认和每条任务通知都在.`_meta`携带中`io.modelcontextprotocol/subscriptionId`其他地方`subscriptions/listen`要求的信息.`tasks/get`那时会回归的内容.

客户仍然必须声明任务扩展. 他们应该从持久的任务ID重新连接和恢复,而不是依赖于事件重播或`Last-Event-ID`现在,我们要去.

> 客户端仍必须声明 扩展任务. 它们应重连并从持久化任务 id 恢复,而不是依赖事件重放或`Last-Event-ID`,我知道.

## 失败语义

运用两个错误层正确.

> 正确使用两个错误层.

### 协议错误

无效方法参数或未知的任务ID返回JSON-RPC错误,通常是`-32602`缺失延期支持的回报`-32021`具有所需能力对象.

> 无效方法参数或未知的任务ID 返回JSON-RPC 错误,通常是`-32602`△缺少扩展支持返回`-32021`并附带所需能力对象.

### 任务执行结果

- 具有正常的工具结果`isError: true`现在还在`completed`由于工具调用产生了所定义的结果.
  中文翻译:带 `isError: true`的普通工具结果仍然是`completed`任务,因为工具调用产生了其定义的结果.
- 延期执行过程中出现了JSON-RPC错误,使得任务完成`failed`存储在 中的 JSON-RPC 错误`error`现在,我们要去.
  中文翻译:延迟执行期间的 JSON-RPC 错误使任务变为`failed`并把这个JSON-RPC 错误存储`error`,我知道.
- 用户拒绝可能会产生`cancelled`文件文件,文件文件,文件文件,文件文件,文件文件,文件,文件,文件,文件,文件,文件,文件,文件,文件,文件,文件,文件,文件,文件,文件,文件,文件,文件,文件,文件,文件,文件,文件,文件,文件,文件,文件,文件,文件,文件,文件,文件,文件,文件,文件,文件,文件,文件,文件,文件,文件,文件,文件,文件,文件,文件,文件,文件,文件,文件,文件,文件,文件,文件,文件,文件,文件,文件,文件,文件,文件,文件,文件,文件,文件,文件,文件,文件,文件,文件,文件,文件,文件,文件,文件,文件,文件,文件,文件,文件,文件,文件,文件,文件,文件,文件,文件,文件,文件,文件,文件,文件,文件,文件,文件,文件,文件,文件,文件,文件,文件,文件,文件,文件,文件,文件,文件,
  中文翻译:用户拒绝可以产生`cancelled`、一个完成的拒绝结果,或其他领域的特定安全结局――把你的选择写入文档――

## 持久性,期限和所有权

保持至少任务 id,状态,时间标签, ttl,投票间隔,最初操作所有权,结果或错误,未完成的输入请求以及所有发行的输入密钥.

> 至少持久化任务 id、状态、时间、ttl、轮询间隔、原始操作所有权、结果或错误、未决输入请求和所有已发出的输入键──

存储密钥必须包含或解决一个权威的租户和主管.知道一个任务ID不能允许访问. 检查所有权`tasks/get`现在`tasks/update`现在`tasks/cancel`加入

> 存储键必须包含或能够解析权威的租户和主体――知道一个任务ID 不应授予访问权――在每次`tasks/get`,我知道.`tasks/update`,我知道.`tasks/cancel`和订阅上检查所有权.

`ttlMs`服务器可能会失败,然后删除过期任务.不要描述它为承诺保留完成结果完成后的数毫秒.

> `ttlMs`从创建起起算且可能变化. 当任务停止产生可观察更新时,客户端可以将其作为一个底部.服务器可能失败,然后删除过期任务.

课程编写一个临时文件,并将其原子改名.多重复制服务应该使用共享的持久存储器和工人租或同等的同时控制.

> 使用原子写或事务. 本课写临时文件再原子改名. 多副本服务应使用共享持久储存和员工租或等价的并发控制.

```figure
tp-task-lifecycle
```

## 动手构建

`code/main.py`执行确定性任务服务:

> `code/main.py`实现一个确定性的任务服务:

- `server/discover`收益`supportedVersions`预存提示,和任务扩展.
  翻译: 中文`server/discover`返回`supportedVersions`、缓存提示和任务 扩展──
- `tools/list`返回一个确定性,可缓存的`generate_report`具有有效输入方案的描述符.
  翻译: 中文`tools/list`返回带合法输入方案的确定性可缓存`generate_report`描述符.
- `tools/call`在返回之前创建和持续任务`resultType: "task"`现在,我们要去.
  翻译: 中文`tools/call`在回归`resultType: "task"`之前创建并持久化任务.
- 重新启动恢复的新服务实例重新加载相同任务.
  中文翻译:新服务实例重载同任务,演示重启恢复。
- `tasks/get`返回完整任务快照.
  翻译: 中文`tasks/get`返回完整任务快照.
- 工人从`working`为了`input_required`现在,我们要去.
  中文翻译:工作器从 `working`转到`input_required`,我知道.
- `tasks/update`接受表格回复并返回空白的完全确认.
  翻译: 中文`tasks/update`接受表单响应并返回空的完成确认.
- 工人存储一个子`CallToolResult`自己的`resultType`服务器身份,然后转向`completed`现在,我们要去.
  中文翻译:工作器存储带自己的`resultType`和服务器身份嵌套`CallToolResult`然后转移到`completed`,我知道.
- `tasks/cancel`在此实施中,它是无力的.
  中文翻译:本实现中`tasks/cancel`是等等的.
-  HTTP 构建器设置`Mcp-Name`为了`params.taskId`为了`tasks/get`现在`tasks/update`其他`tasks/cancel`现在,我们要去.
  中文翻译:HTTP 构建器为`tasks/get`,我知道.`tasks/update`和 `tasks/cancel`让我`Mcp-Name`设为`params.taskId`,我知道.
- 通知助理使用`notifications/subscriptions/acknowledged`其他`notifications/tasks`两者都标记着听取请求的身份.
  中文翻译:通知辅助函数使用 `notifications/subscriptions/acknowledged`和 `notifications/tasks`两者都带监听请求的标签.
- 无 id 的通知没有产生 JSON-RPC 响应.
  中文翻译:无 id 的通知不产生 JSON-RPC 响应.

工人显然进步,而不是睡在背景线程中. 这使得每个状态过渡都具有确定性,并且使协议示例与队列机制保持分开.

> 工作器显然推进,而不是在后台线程里睡觉. 这使每次状态转移都是确定性的,并使协议示例和队列机制保持分离.

## 运行证

根据数据库根:

> 从仓库根目录:

```bash
cd phases/13-tools-and-protocols/13-mcp-async-tasks/code
python3 main.py
python3 -m unittest discover tests -v
```

预期结果序列:

> 预期结果序列:

```text
id=0 resultType=complete status=ack
id=1 resultType=task status=working
id=2 resultType=complete status=working
id=3 resultType=complete status=input_required
id=4 resultType=complete status=ack
id=5 resultType=complete status=completed
```

检查一下`tasks/status`现在`tasks/result`其他`tasks/list`报价方法在现代服务中没有找到.
> 需要验证`tasks/status`,我知道.`tasks/result`和 `tasks/list`在现代服务中返回方法-未找到――
检查一下`tools/list`现在的 HTTP 任务方法都反映了其任务 id 通过`Mcp-Name`现在,我们要去.

> 验证`tools/list`并且每个现行HTTP任务方法都通过`Mcp-Name`镜像其任务的身份.

## 运送它.

`outputs/skill-task-store-designer.md`现在生产一个知情的扩展设计:能力谈判,持续前回归创建,当前的方法,输入更新流量,所有权,过期,取消,订阅和从删除的实验方法迁移.

> `outputs/skill-task-store-designer.md`现在产出扩展感知的设计:能力协商、持久前回报 创建、现行方法、输入更新流、所有权、过期、取消、订阅,以及从移除的实验性方法迁移――

## 练习题

1. 添加第二个未完成输入键.`tasks/update`证明任务仍然存在`input_required`直到两个钥匙都被回答.
   中文翻译:添加第二个未决输入键――发送部分 `tasks/update`证明任务在两个关键都被应答前保持`input_required`,我知道.
2. 增加租户的所有权,并拒绝由错误的认证主体提供的有效任务身份.
   中文翻译:给存储增加租户所有权,拒绝由错误的已认证主体表达的合法任务ID.
3. 增加到到期的工人租合同. 证明两个服务实例不能同时完成同一个任务.
   中文翻译:添加带过期工作者租约――证明两个服务实例不能并发完成同一任务――
4. 实现一个POST响应SSE适配器`subscriptions/listen`不要添加GET,`Last-Event-ID`没有任何问题,
   中文翻译:为 `subscriptions/listen`实现 POST 响应 SSE 适配器――不要添加 GET、`Last-Event-ID`或会话头.
5. 加入过期清理. 区分过期任务与错误的任务身份证,而不会泄露跨租户存在.
   中文翻译:添加过期清理──区分过期任务与形式错误的任务ID,并不泄露跨租户的存在──

## 关键词 快速查找表

| Term | Meaning in the current extension |
|------|----------------------------------|
| Tasks extension | Optional `io.modelcontextprotocol/tasks` capability for durable async work |
| `CreateTaskResult` | Server-directed `resultType: "task"` response to an eligible request |
| `tasks/get` | Poll a full current task snapshot, including terminal result or pending input |
| `tasks/update` | Submit responses to a task's outstanding `inputRequests` |
| `tasks/cancel` | Acknowledge cooperative cancellation intent |
| `input_required` | Task status indicating client input is outstanding |
| `pollIntervalMs` | Server-suggested minimum delay before another poll |
| `ttlMs` | Expiry duration measured from task creation |
| Durable-before-return | Rule that the task id must resolve before its handle is sent |
| `notifications/tasks` | Optional full task snapshot delivered on a subscribed SSE response |

> **【中文解读】**术语速查(中英对照):任务延长=官方 `io.modelcontextprotocol/tasks`扩展能力;CreateTaskResult=对合格请求的主导服务器`resultType: "task"`响应`tasks/get`=轮询完整任务快照 (含终态结果或未决输入);`tasks/update`提交对未决`inputRequests`的响应;`tasks/cancel`=确认协作取消意图;input_required=任务状态,表示客户端输入未决;pollIntervalMs=服务器建议的最小轮询间隔;ttlMs=从任务创建起算的过期时间长;`notifications/tasks`应对应对应对应对应对应对应对应对应对应对应对应对应对应对应对应对应对应对应对应对应对应对应对应对应对应对应对应对应对应对应对应对应对应对应对应对应对应对应对应对应对应对应对应对应对应对应对应对应对应对应对应对应对应对应对应对应对应对应对应对应对应对应对应对应对应对应对应对应对应对应对应对应对应对应对应对应对应对应对应对应对应对应对应对应对应对应对应对应对应对应对应对应对应对应对应对应对应对应对应对应对应对应对应对应对应对应对应对应对应对应对应对应对应对应对应对应对应

## 遗产兼容性

根据客户要求,`tasks/status`现在`tasks/result`其他选择性`tasks/list`现在的客户端使用扩展功能,接受服务器导向手柄,投票`tasks/get`提供输入`tasks/update`读取任务快照的最终结果.

> 2025-11-25 实验性表面使用客户端请求任务增强,`tasks/status`,我知道.`tasks/result`和可选的`tasks/list`△只保留这些名字在锁定的旧版本适配器内.`tasks/get`  `tasks/update`补充输入,并从任务快照读取最终结果.

## 继续阅读 继续阅读

- [Official MCP Tasks extension](https://tasks.extensions.modelcontextprotocol.io/specification/draft/tasks)
  中文翻译:官方MCP任务 扩展规范(当前为草案) 』
- [MCP 2026-07-28 Multi Round-Trip Requests](https://modelcontextprotocol.io/specification/2026-07-28/basic/patterns/mrtr)
  中文翻译:MRTR 模式规范,任务创建前输入收集的机制来源──
- [MCP 2026-07-28 Streamable HTTP](https://modelcontextprotocol.io/specification/2026-07-28/basic/transports/streamable-http)
  中文翻译:可流的HTTP传输规范,`Mcp-Method`现在,我们要去.`Mcp-Name`头与 POST 响应 SSE 的定义处──
