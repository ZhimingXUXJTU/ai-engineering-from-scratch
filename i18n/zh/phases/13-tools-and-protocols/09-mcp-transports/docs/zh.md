# 无状态的HTTPS流程

> 运输运输传输信息. 它不提供缺失协议状态.`2026-07-28`通过本地工作室和远程流向 HTTP, 两个都包含自我描述的请求.

> **【中文解读】**传输层仅负责搬运MCP消息,不负责补齐协议状态. 在2026-07-28 规范中,本地工作室和远程流媒体HTTP传递的都是"自定义"请求每个请求自带协议版本和客户端能力,不再依赖连接或会话保存上下文.

> **【拓展：传输层演进→2026-07-28 无状态化】**通过MCP传输层三年三变:2024-11的HTTP+SSE 双端点、2025-03-26的流通性HTTP(GET 流 + `Mcp-Session-Id`演进方向始终是"把状态从传输层赶出去":会话头没了,改成请求体`_meta`携带版本与能力;独立 GET 流没了,改成`subscriptions/listen`没有状态让任何健康副本都能处理任何请求,是云原生横向扩张的关键.

>  **【前置】**学习节前请先掌握:(1) 阶段13·07、08(MCP服务器和客户端) 理解JSON-RPC 分发逻辑;(2) HTTP 协议基础(方法、标题、状态码);(3) DNS 重绑定攻击概念本节的`Origin`校验是防御手段;(4) 若你学过本课旧版(2025 传输:GET 流 + 会话头 + `Last-Event-ID`重放),请先清空那套旧心智模型再往下读.

**Type:** Learn | **类型:** 学习
**Languages:** Python | **语言:** Python
**Prerequisites:** Phase 13, Lessons 07 and 08 | **前置知识:** Phase 13 · 07、08（MCP 服务器与客户端）
**Time:** ~65 minutes | **时间:** 约 65 分钟

## 学习目标

- 选择本地儿童进程的studio和网络服务的 Streamable HTTP.
  中文翻译:本地子进程选studio,网络服务选 流式HTTP──
- 实现现代单端点,仅供POST使用的流向HTTP合同.
  中文翻译:实现现代的单端点、仅 POST的流向性HTTP契约。
- 镜像和验证MCP版本,方法和名称标题与JSON-RPC体.
  中文翻译:把 MCP 版本、方法、名称镜像头与 JSON-RPC 请求体做比对校验。
- 提供按要求范围的SSE和长寿命`subscriptions/listen`流量正确.
  中文翻译:正确交付请求级 SSE流和长期生命周期的`subscriptions/listen`流,我知道.
- 迁移基于会议和传统的HTTP+SSE部署,而不用将传统行为呈现为现代.
  中文翻译:迁移基于会话的部署和遗留 HTTP+SSE 部署,且不把遗留行为冒充为现代行为.

## 问题 问题引入

> **【中文解读】**本节讲清"为什么要没有状态"――早期流媒体 HTTP 把协议协商,连接行为,会话行为捆绑在一起 服务器可以造`Mcp-Session-Id`‧ 暴露独立 流 ‧ 接受 DELETE 终止会话 ‧ 用`Last-Event-ID`恢复SSE──2026-07-28 把这些机制全部从现代线路格式中移除:每个请求都能落在任意健康工作者上,因为协议版本和客户端能力随着请求的传输;HTTP 头条只做路由与策略镜像,服务器执行前会验头是否与体一致.代价是:还在将2025 传输作为现行规范教导的服务器,教导错误的失败模型和安全模型.

之前的流媒体HTTP修改将协议谈判与连接和会议行为结合在一起.`Mcp-Session-Id`通过GET,将一个独立的GET流暴露,接受 DELETE,并恢复SSE.`Last-Event-ID`现在,我们要去.

> 服务器可以造.`Mcp-Session-Id`露一个独立的GET流 接受 DELETE 来终止会话,并使用`Last-Event-ID`恢复SSE.

股`2026-07-28`通过 HTTP 标题,可以将这些机制从现代电线中移除.每个请求都可以落地在任何健康的员工上,因为其协议版本和客户端功能在请求器内. HTTP 标题反映了路由和政策的选择领域,但服务器在执行之前验证了这些标题对身体的验证.

> 股`2026-07-28`现代线路格式中移除了这些机制. 由于协议版本和客户端能力随着请求传输而每个请求都能落在任何健康工作者身上.

结果更容易扩展,更容易推理. 这也意味着一个教导2025运输的服务器正在教导错误的故障和安全模型.

> 结果更容易扩展也更容易推断. 这也意味着:把2025 传输作为现行规范来教导的服务器,教导错误的失败模型和安全模型.

## 概念的核心概念

>  **【类比】**无状态传输像外卖平台的订单流转.旧模式(会话式传输) 如"你只能等到初次接单的那个骑手"骑手下线(副本重启),订单就卡住.新模式(2026-07-28 无状态) 如"任何站点都能接你的订单"每张订单(请求) 都完整写明地址和备注(协议版本、能力),谁接手都能继续工作;贵重物寄存(应用状态) 不塞进骑手口袋(连接亲和件),而是给一个张取性码(显式句柄) 状态.

### 工作室

工作室绑定是针对客户端启动的子进程:

> 工作室 绑定面向客户端启动的子进程:

- 客户端每行写一个 UTF-8 JSON-RPC 消息到 stdin.
  中文翻译:客户端向 stdin 每行写入一条 UTF-8 JSON-RPC 消息──
- 服务器每行写一个 UTF-8 JSON-RPC 消息到 stdout.
  中文翻译:服务器向stdout 每行写入一条 UTF-8 JSON-RPC 消息──
- 服务器将诊断写给SDR.
  中文翻译:服务器把诊断信息写入 stderr。
- 服务器在EOF中即时离开.
  中文翻译:stdin 出现 EOF 时服务器立即退出──
- 每个现代化请求都包含了版本和客户端功能.`params._meta`现在,我们要去.
  中文翻译:每个现代请求都在`params._meta`中携带版本和客户端能力

进程可能会在许多电话中运行,但它不是一个现代协议会议.如果它突然出发,飞行中的请求会丢失.重新启动过程,重新发现,重新列表,重新开放订阅,并重新尝试使用新的请求ID安全操作.

> 进程可以存活多次调用,但它不是现代意义上的协议会话. 如果进程意外退出,所进行的请求会丢失. 正确的做法是:重启进程,重新发现,重新列清单,重新开订阅,并使用新的请求 id 重试安全操作.

### 流向的HTTP在2026-07-28

> **【中文解读】**现代服务器只暴露一个接收 POST 的 MCP端点(如 `/mcp`)──每条 JSON-RPC 请求或通知都是一条新的HTTP POST,请求体只包含一条消息;客户端不向服务器发送 JSON-RPC 响应──请求的响应有两种形式:`application/json`(单条 JSON-RPC 响应) 或`text/event-stream`通知被接受,则返回无主体的通知.`202 Accepted`△客户端使用`Accept: application/json, text/event-stream`同时声明两种响应类型.

现代服务器暴露了一个MCP终端点,例如`/mcp`通过邮件.

每个JSON-RPC请求或通知都是新的HTTP POST. 机体包含一个JSON-RPC消息. 客户端不会向服务器发送JSON-RPC响应.

> 现代服务器暴露一个接收 POST 的 MCP端点,例如`/mcp`△每条 JSON-RPC 请求或通知都是一条新的HTTP POST──请求体包含一个条 JSON-RPC消息──客户端不向服务器发送 JSON-RPC 响应──

服务器对请求返回:

- `Content-Type: application/json`通过一个JSON-RPC响应;或
- `Content-Type: text/event-stream`要求的通知,随后是最终的JSON-RPC响应.

对于被接受的通知,服务器返回`202 Accepted`没有尸体.

> 对于请求,服务器返回两种之一:`Content-Type: application/json`带一条 JSON-RPC 响应,或 `Content-Type: text/event-stream`首先带与该请求相关的通知 再带最终的JSON-RPC响应 对于接受的通知,服务器返回不带主体的`202 Accepted`,我知道.

客户广告两种响应类型:

> 客户端同时声明接受两种响应类型:

```http
Accept: application/json, text/event-stream
```

### 仅仅POST的意思是仅仅POST

> ️ **【易错点】**场景:从旧版本的流向 HTTP 迁移来的服务端习惯性实现 GET 流、DELETE 会话端点,或造/回显 `Mcp-Session-Id`处理`Last-Event-ID`/ 后果:这些都不是2026-07-28 行为GET 和 DELETE 必须返回`405`会议头必须被忽视;请求级流在最终响应前中断即宣告请求丢失,只能换新ID 重试,绝不能尝试流恢复 / 修复:对照规范逐条移除遗留端点与头处理逻辑,把"断流恢复"改成"新请求重试"――

现代流式HTTP没有独立的GET流和 DELETE会话终点.

> 现代流向 HTTP 没有独立 GET 流,也没有 DELETE 会话端点。

- `GET /mcp`收益`405 Method Not Allowed`现在,我们要去.
  翻译: 中文`GET /mcp`返回`405 Method Not Allowed`,我知道.
- `DELETE /mcp`收益`405 Method Not Allowed`现在,我们要去.
  翻译: 中文`DELETE /mcp`返回`405 Method Not Allowed`,我知道.
- `Mcp-Session-Id`没有任何和回声.
  翻译: 中文`Mcp-Session-Id`被忽视,从不造也从不回来显而易见.
- `Last-Event-ID`由于现代流程无法恢复,
  翻译: 中文`Last-Event-ID`由于现代流无法恢复.

如果请求范围的流在最终响应之前断裂,客户端已经失去了飞行中的请求.它可能会在安全的重试时发出新的请求,并使用新的JSON-RPC id.它不得尝试重启流.

> 如果请求级流在最终响应前中断,客户端就失去了正在进行的请求.

### 验证原产地

> **【中文解读】**服务器对进入连接做`Origin`校验以防DNS重绑定:头存在且不在白名单上就返回`403 Forbidden`无浏览器客户端可以不带`Origin`据悉,该公司的服务器应被绑定.`127.0.0.1`没有所有网卡;`Origin`校验不是认证,网络服务仍然需要认证和授权每一个请求;`origin.startswith("https://trusted.example")`这类前检查不安全,会让攻击者控制后.

服务器验证`Origin`如果头条存在,并且没有明确允许,返回`403 Forbidden`非浏览器客户端可能会省略`Origin`官方交通规则允许的.

> 服务器在进入连接上校验`Origin`如果该头条存在且未被明确允许,返回`403 Forbidden`〔非浏览器客户端可以省略〕`Origin`官方传输规则允许这一点.

地方服务器应与 `127.0.0.1`网络服务仍然需要在每一个请求中进行验证和授权.

> 本地服务器应绑定`127.0.0.1`网络服务仍然需要对每个请求进行认证和授权.

使用正确的原始匹配后的定制.`origin.startswith("https://trusted.example")`它们是不安全的,因为它们可以接受攻击者控制的后音.

> 在规范化配置后使用精确的来源匹配.`origin.startswith("https://trusted.example")`由于它们可能接受攻击者控制后,

### 需要的HTTP元数据标题

> **【中文解读】**每个现代 POST 都带有三个镜头:`MCP-Protocol-Version`必须等于`params._meta`中的协议版本;`Mcp-Method`必须等于JSON-RPC`method`其他`tools/call`,我知道.`resources/read`,我知道.`prompts/get`必须带`Mcp-Name`(等于`params.name`没有任何`resources/read`时等于`params.uri`首值大小写敏感──不安全或非ASCII的 `Mcp-Name`用`=?base64?{...}?=`哨兵编码,服务器解码后再与请求体比对.`400`其他类型`-32020`版本不支持 → HTTP `400`其他`-32022`并带精确的`supported`现在,我们要去.`requested`数据;未知现代方法 → HTTP `404`其他`-32601`(JSON-RPC 体很重要,双时代客户端依赖于它区分现代错误和遗留端点未定命)

每个现代 POST 请求都包括:

```http
MCP-Protocol-Version: 2026-07-28
Mcp-Method: tools/call
Mcp-Name: notes_search
```

标题规则:

> 头规则:

- `MCP-Protocol-Version`要求和必须等等`params._meta.io.modelcontextprotocol/protocolVersion`现在,我们要去.
  翻译: 中文`MCP-Protocol-Version`必须填,必须等于`params._meta.io.modelcontextprotocol/protocolVersion`,我知道.
- `Mcp-Method`需要和必须等于JSON-RPC`method`现在,我们要去.
  翻译: 中文`Mcp-Method`必须填写,必须等于JSON-RPC`method`,我知道.
- `Mcp-Name`需要`tools/call`现在`resources/read`其他`prompts/get`现在,我们要去.
  翻译: 中文`tools/call`,我知道.`resources/read`,我知道.`prompts/get`必须带`Mcp-Name`,我知道.
- `Mcp-Name`相当于`params.name`其他`params.uri`为了`resources/read`现在,我们要去.
  翻译: 中文`Mcp-Name`等于`params.name`对`resources/read`则等于`params.uri`,我知道.
- 标题值对案例敏感,尽管标题名称对案例不敏感.
  中文翻译:头值大小写敏感,尽管头名大小写不敏感――

不安全或非ASCII `Mcp-Name`值使用 UTF-8 Base64 哨兵:

```text
=?base64?{Base64EncodedValue}?=
```

在与机体比较之前,服务器会解码这个值.

> 不安全或非ASCII的`Mcp-Name`值使用精确的 UTF-8 Base64 哨兵格式(如上) ――服务器先解码该值再与请求体比对――

缺失,错误的或不匹配的镜头标题返回 HTTP `400`使用JSON-RPC代码`-32020`如果标题和体格同意服务器不支持的版本,返回HTTP `400`随着`-32022`错误数据`{"supported":["2026-07-28"],"requested":"2027-01-01"}`现在,我们要去.

> 镜像缺失、形或不匹配时返回HTTP `400`和 JSON-RPC 错误码`-32020`如果头和请求一致地指向一个服务器不支持的版本,返回HTTP`400`和 `-32022`带有精确的错误数据,例如`{"supported":["2026-07-28"],"requested":"2027-01-01"}`,我知道.

未知现代方法返回HTTP`404`通过JSON-RPC`-32601`由于双代客户端使用它来区分现代错误与传统终端错误,所以JSON-RPC的实体很重要.

> 未知的现代方法返回 HTTP `404`和JSON-RPC `-32601`◎JSON-RPC 响应体很重要,因为双时代客户端依赖于它区分"现代错误"和"遗留端点未定命"――

### 根据要求进行的SSE

> **【中文解读】**服务器可为单个长运行请求选择SSE 作为响应载体:POST 发出 `tools/call`响应流上随着推送与该请求 id 相关的进步通知,最后给出最终的 JSON-RPC 响应,流随即关闭.约束有三条条:(1) 服务器不得在该流上发送独立的 JSON-RPC 请求样本,发出,根交都改向多轮旅行请求结果;(2) 关闭响应流即取消该请求;(3) 不要重置添加 SSE 事件 id `Last-Event-ID`恢复不属于现代修订.

服务器可以选择SSE用于一个长期请求:

```text
POST tools/call id=41
  <- notifications/progress related to id=41
  <- notifications/progress related to id=41
  <- JSON-RPC response id=41
stream closes
```

服务器不得在此流中发送独立的JSON-RPC请求.采样,调用和根交互使用多轮通行请求结果.关闭响应流取消该请求.

> 服务器必须在此条流上发送独立的JSON-RPC 请求──样本取消此请求──使用多轮回访问请求──MRTR结果──关闭响应流即取消该请求──

不要添加SSE事件ID来重播. `Last-Event-ID`恢复并非现代修订的一部分.

> 不要重放添加 SSE 事件ID.`Last-Event-ID`恢复不属于现代修订.

### 长期的变化使用订阅/听

> **【中文解读】**变更通知不再独立 GET,而是客户端主动发起`subscriptions/listen`请问:POST 的响应保持开放,成为一个长生命周期 SSE流.`notifications`目标是允许清单服务器不得发送未请求的通知类型.`notifications/subscriptions/acknowledged`确认,每条变更通知和最终结果都在`_meta`中携带等于听 请求ID 的`subscriptionId`△服务器可用 SSE 注释做保活. 流断开后,客户端换新请求ID 重新听并重新拉取受影响的数据.`resources/subscribe`和 `resources/unsubscribe`属于遗留时代,禁止在现代连接上使用.

变更通知使用客户端开放的请求,而不是独立的GET:

```json
{
  "jsonrpc": "2.0",
  "id": "listen-1",
  "method": "subscriptions/listen",
  "params": {
    "notifications": {
      "toolsListChanged": true,
      "resourceSubscriptions": ["notes://note-1"]
    },
    "_meta": {
      "io.modelcontextprotocol/protocolVersion": "2026-07-28",
      "io.modelcontextprotocol/clientCapabilities": {},
      "io.modelcontextprotocol/clientInfo": {
        "name": "course-client",
        "version": "1.0.0"
      }
    }
  }
}
```

后者是一个长期的SSE流.`notifications/subscriptions/acknowledged`确认,每次变更通知以及最终结果都会带来`io.modelcontextprotocol/subscriptionId`在`_meta`服务器可能会作为保留符发出SSE评论.当流量下降时,客户端会重新发出`subscriptions/listen`具有新的请求身份和重新调整影响数据.

> 文章的响应是一个长期生命周期的 SSE流.`notifications/subscriptions/acknowledged`确认消息,每条变更通知和最终结果都在`_meta`携带中`io.modelcontextprotocol/subscriptionId`服务器可以使用SSE注释作为保证. 当流通开启时,客户端使用新的请求ID 重新发行.`subscriptions/listen`并重新获取受影响的数据.

`resources/subscribe`其他`resources/unsubscribe`现在,我们在这个世界里,

> `resources/subscribe`和 `resources/unsubscribe`属于遗留时代. 不要在现代连接上使用它们.

### 明确申请状态

> **【中文解读】**移除协议会话不等于禁止有状态的工作流程.服务器可以生成一个不透明的状态句柄,作为普通工具结果返回;客户端在后调中将其作为显式参数传输回来.句柄必须绑定到已认证的主体,不可猜测的,可过期的,每次使用都被授权,这使状态在应用层上可见,而不是藏进传输和性质.隐藏副本状态的失败是机械性的:请求 A 在副本 1 内存中创建草稿但不返回句柄,请求 B 落下副本 2 无法命名或加载草稿,粘性路由看起来修复症状,直到重新启动,发布,重新调节或转移.通过正确的协议,两个协议部分:请求保留在下载中存储器的状态;请求 B 落下载的副本 2 无法命名或加载草稿,直到重新启动,重新调节或转移.`requestState`草稿或持久任务用显式句柄 + 共享持久化 + 过期 + 并发控制 + 等.

删除协议会议不会禁止使用状态的工作流程.服务器可能会打印一个不透明的状态手柄,并将其返回为正常工具结果.客户端在后来的电话中将该手柄作为明确的参数.

> 移除协议会话不禁止带状态工作流.服务器可以造一个不透明的状态句柄,并作为普通工具结果返回.

绑定手柄与认证的主体,使它们无法测试,过期,并授权所有使用. 这使状态在应用层上可见,而不是隐藏在运输亲密度.

> 把句柄绑定到已认证的主体,使其不可猜测,可过期,并授权每次使用.

隐藏复制状态导致的故障是机械的:

> 由于隐藏的副本状态导致的失败是机械性的:

1. 要求A达到复制1并创建一个草案在该过程的记忆中.
  中文翻译:请求 A 到达副本 1,在该进程内存中创建草稿──
2. 答案不会返回草案处理器,因为实施假设连接识别了草案.
  中文翻译:响应不回复草稿句柄,因为实现假设"连接"能标识草稿──
3. 要求B是新 POST,达到复制 2.
  中文翻译:请求B 是一次全新的 POST,到达副本 2──
4. 复制2有有效的协议元数据,但没有方法命名或加载草案,因此工作流失败或读取错误的本地对象.
  中文翻译:副本 2 持有合法的协议元数据,但无法命名或加载草稿,于是工作流失败或读到错误的本地对象.
5. 粘性路由似乎会修复症状,直到重新启动,推出,重新安排或失败转移下一个请求.
  中文翻译:粘性路由看似修复了症状,直到某次重启,发布,重调度或故障转移挪走了下一个请求.

正确的边界有两个部分. 每个请求都包含了协议的文本. 持久应用状态在服务器硬件的手柄下,返回给客户端. 接下来的调用器提供处理器,任何复制器都加载相同的记录, 复制记忆可能会缓存记录,但不能是唯一需要对准的副本.

> 正确的边界有两个部分.协议上下文留在每个请求中.永久的应用状态存储在共享存储中,由服务器造句柄返回客户端.下一次调用提供该句柄,任意副本都能加载相同的记录,授权将记录绑定到已认证的主体和租户.

选择状态机制根据寿命.请求本地变量可以服务于一个调用.短时间的MRTR延续可以使用完整性保护 `requestState`草案或持久任务需要明确的处理,加上共享的持久性,过期,同步控制和无效性.这些对象中没有一个是MCP协议会议.

> 根据生命周期选择状态机制――请求局部变量可用于单次调用――短的MRTR 延续可用于带完整性保护的`requestState`◎草稿或持久任务需要显式的句柄,外加共享持久化,过期,并发控制和等性.

### 双时代 HTTP 兼容性

> **【中文解读】**双时代客户端先尝试现代 POST;收到HTTP `400`现在,我们要去.`404`现在,我们要去.`405`对于检查响应体:识别出现代JSON-RPC 错误证明服务器是现代的修正请求或重试已公布的版本,绝不降级;空体或无法识别的响应才可能是遗留的HTTP+SSE 服务器,此时才去试验旧的GET端点并期待其遗留.`endpoint`事件──迁移期的服务器可以把现代元数据路由到现代POST-only实现、为老客户端保留独立遗留端点,但绝不能把遗留的 GET、DELETE、会话 id 或重放行为描述为`2026-07-28`部分的部分.

如果客户端支持现代和传统服务器,首先尝试一个现代 POST.`400`现在`404`其他`405`检查了身体:

> 同时支持现代和遗留服务器的客户端先尝试现代 POST――如果收到HTTP`400`,我知道.`404`或`405`检查响应体:

- 已识别的现代JSON-RPC错误证明服务器是现代化的. 纠正请求或重新尝试广告版本. 不要降级.
  中文翻译:识别出的现代 JSON-RPC 错误证明服务器是现代的──修正请求或重试已公布的版本──绝不降级──
- 只有试用旧的GET终端点,并预计其遗产 `endpoint`事件
  中文翻译:空体或无法识别的响应可能表明这是遗留的HTTP+SSE 服务器.`endpoint`事件.

服务器可以通过将现代的元数据向现代的POST实现并保留旧客户端的独立遗产终端点来支持迁移期间的两个时代.永远不要将遗产GET, DELETE,会议ID或重播行为描述为`2026-07-28`现在,我们要去.

> 服务器在迁移期可以同时支持两个时代:把现代元数据路由到现代POST-only实现,为老客户端保留独立遗留端点――绝不要把遗留的 GET、DELETE、会话 id或重放行为描述为`2026-07-28`部分的部分.

```figure
tp-transport-handshake
```

## 用它实现框架

> **【中文解读】** `code/main.py`使用Python 标准库实现一个有限的现代流式HTTP服务器:校验`Origin`和镜像头、忽略已移除的会话头、普通调用返回JSON,并演示一个有限的条目 `subscriptions/listen`其他国家`--probe`)逐项验证:非法`Origin`被拒绝,无会话 id 也能完成发现,`Mcp-Session-Id`和 `Last-Event-ID`被忽视,头不匹配回来`-32020`、不支持的版本返回 `-32022`且带精确的数据,无身份通知被接受,返回无主体`202`、GET 和 DELETE 返回 `405`、听 流的确认/通知/最终结果都带着订阅 id──

`code/main.py`通过 Python 标准库实现一个有限的,现代的 Streamable HTTP 服务器.它验证了 Origin 和 Mirrored 头条,忽略了删除的会话头条,返回了 JSON 用于正常调用,并显示了一个有限的 `subscriptions/listen`水电流.

> `code/main.py`使用Python 标准库实现一个有限的现代流式HTTP服务器. 它的起源和镜像,忽略已移除的会话头,普通调用返回JSON,并演示一个有限的条目.`subscriptions/listen`,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,.

```bash
cd code
python3 main.py --probe
python3 -m unittest discover tests -v
```

探测器检查:

- 拒绝无效的起源;
  中文翻译:非法起源被拒绝;
- 没有会议ID的情况下发现成功;
  中文翻译:无需会话 id 即可完成发现;
- `Mcp-Session-Id`其他`Last-Event-ID`无视;
  翻译: 中文`Mcp-Session-Id`和 `Last-Event-ID`被忽视;
- 标题不匹配返回`-32020`其他
  中文翻译:头不匹配返回 `-32020`其他
- 没有支持的版本返回`-32022`确切的`supported`其他`requested`数据;
  中文翻译:不支持的版本返回 `-32022`并带精确的`supported`和 `requested`数据
- 已接受的无 id 通知返回 HTTP `202`没有尸体;
  中文翻译:被接受的无 id 通知返回 HTTP `202`且无主体;
- 获取和删除返回`405`其他
  中文翻译:GET 和 DELETE 返回 `405`其他
- `subscriptions/listen`是一个 POST 响应流,其确认,通知和最终结果包含其订阅ID.
  翻译: 中文`subscriptions/listen`是一条 POST 响应流,其确认、通知和最终结果都携带订阅 id──

## 运送它.

这一课是很好的.`outputs/skill-mcp-transport-migrator.md`它删除了现代协议会议,增加了标题体验证,并取代了独立的GET.`subscriptions/listen`任何遗产桥梁都会显著分开.

> 本课产出发 `outputs/skill-mcp-transport-migrator.md` 移除现代协议会话加入头体校验 用`subscriptions/listen`取代独立 GET,并让任何遗留桥接保持明显隔离.

## 练习题

1. 删除`Mcp-Method`通过一个POST. 确认HTTP`400`错误`-32020`现在,我们要去.
   中文翻译:从 POST 中移除 `Mcp-Method`△确认HTTP`400`和错误`-32020`,我知道.
2. 发送相匹配的标题和体格版本`2027-01-01`确认HTTP`400`错误`-32022`准确的数据`{"supported":["2026-07-28"],"requested":"2027-01-01"}`现在,我们要去.
   中文翻译:发送头与体一致的版本 `2027-01-01`△确认HTTP`400`、错误`-32022`和精确数据`{"supported":["2026-07-28"],"requested":"2027-01-01"}`,我知道.
3. 派一个Base64哨兵`Mcp-Name`确认解码值与 已解码值的值进行比较`params.uri`现在,我们要去.
   中文翻译:为非ASCII资源URI发送基地64哨兵`Mcp-Name`△确认解码后的值与`params.uri`没有什么.
4. 在最终响应之前打破有限的听声流,用新的JSON-RPCID重新发布并重复工具.
   中文翻译:在最终响应前打断有限的听力流――用新的JSON-RPC id 重新发发发并重新拉取工具――
5. 添加一个明确的工作流程手柄到ping工具. 绑定它到一个授权主题,而不使用连接亲密性.
   中文翻译:给ping 工具加一个显式工作流句柄──不需要连接亲和性,把它绑定到一个授权主体──

## 关键词 快速查找表

| Term | Meaning | 中文术语 |
|------|---------|----------|
| stdio | Newline-delimited JSON-RPC over a client-launched subprocess | stdio 传输 |
| Streamable HTTP | Single endpoint where each modern message is a new POST | Streamable HTTP 传输 |
| Request-scoped SSE | POST response stream containing related notifications and final response | 请求级 SSE 流 |
| `subscriptions/listen` | Long-lived POST request for opted-in change notifications | 订阅监听请求 |
| Header mismatch | HTTP `400` and JSON-RPC `-32020` when mirrored headers disagree with body | 头不匹配错误 |
| Origin validation | DNS-rebinding defense for incoming connections, not authentication | Origin 校验（防 DNS 重绑定） |
| Explicit state handle | Application token passed as an ordinary argument instead of hidden session state | 显式状态句柄 |
| Legacy bridge | Separate earlier-era behavior kept only for compatibility | 遗留桥接 |

## 继续阅读 继续阅读

- [MCP Transport Overview](https://modelcontextprotocol.io/specification/2026-07-28/basic/transports)
  中文翻译:MCP 传输总览两种现代传输的权威入口
- [MCP stdio Transport](https://modelcontextprotocol.io/specification/2026-07-28/basic/transports/stdio)
  中文翻译:stdio 传输的完整规范
- [MCP Streamable HTTP](https://modelcontextprotocol.io/specification/2026-07-28/basic/transports/streamable-http)
  中文翻译:可流的HTTP的仅仅在邮件中
- [MCP Subscriptions](https://modelcontextprotocol.io/specification/2026-07-28/basic/patterns/subscriptions)
  翻译: 中文`subscriptions/listen`订阅模式规范
- [MCP 2026-07-28 Changelog](https://modelcontextprotocol.io/specification/2026-07-28/changelog)
  中文翻译:2026-07-28 修订的完整变更清单(会话移除的官方说明)
