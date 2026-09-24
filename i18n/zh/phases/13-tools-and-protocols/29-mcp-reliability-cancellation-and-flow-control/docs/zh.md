# 通过"MCP可靠性"",取消与流量控制"

> 请求 ID 与消息相关,它不会使副作用安全,阻止一个工作者,或者保护一个流量免受缓慢的消费者.

> **【中文解读】**要求ID只负责关联消息:它不能让副作用变得安全,不能停止一个工人,也不能保护流不被消费者拖. 本课基于MCP 2026-07-28 规范讲分布式系统中最贵的那些 bug:取消竞争态,双钟超时,等重试,背压,重连风暴.核心立场:MCP只定义消息和传输行为,时间预算,业务等,有界列,重试分类,持久任务状态,重连和重策略仍然属于您的应用所有.

> **【拓展：MCP→分布式系统工程】**这里出现的每个概念取消信号和传输绑定,完成/取消竞争态,空+绝对双超时,等键,事务性发件箱,背压,动退避都是分布式系统的经典课程.本课程的特殊性在于将它们放入MCP的具体语境:studio上取消是一个条通知,流动 HTTP上取消是关闭响应流,`tasks/cancel`面向持久任务――第13阶段 · 13期异步任务) 是本课的直接前置――

>  **【前置】**学本课前请先掌握:第13阶段 · 09(MCP 传输:stdio 与流式HTTP的差异)`tasks/cancel`

**Type:** Build | **类型:** 动手实践
**Languages:** Python | **语言:** Python
**Prerequisites:** Phase 13, Lessons 09 and 13 | **前置知识:** Phase 13 · 09、13
**Time:** ~120 minutes | **时间:** 约 120 分钟

## 学习目标

- 执行stdio和流式HTTP的正确取消信号.
  中文翻译:为studio 和 Streamable HTTP 实现各自正确的取消信号──
- 解决完成和取消比赛,而没有在取消后发送消息.
  中文翻译:解决"完成与取消"的竞态,并且在取消后不再发送消息.
- 单独取消请求与持久的取消`tasks/cancel`它们是什么意思?
  中文翻译:把请求取消与持久 `tasks/cancel`语义区分开――
- 根据副作用和明确的无能度关键,重新尝试决策.
  中文翻译:基于副作用和显式等关键构建重试决策.
- 限制进步队列,同时保留最终的回复.
  中文翻译:给进度队列设界,同时保住最终响应──
- 通过重新连接,重新调整和动的后退来恢复流.
  中文翻译:通过重连、权权重取和带动的退避恢复流――

## 问题 问题引入

> **【中文解读】**经典事故链:客户端调工具→服务器开工→进度到来→代理缓冲流→客户端超时断开→服务器一毫秒后完成→客户端换了一个新的JSON-RPC id 重试→变更执行两次.每个组件都在本地操作正确,系统全局失败了.

幸福之路隐藏着最昂贵的分布式系统 bug.

> 快乐路径 (快乐路径) 幸福路径 (快乐路径) 藏在最昂贵的分布式系统 bug.

客户端调用工具.服务器开始工作. 进程到达. 代理缓冲流. 客户端达到其时间过期,然后断开. 服务器完成一毫秒后. 客户端重新尝试一个新的JSON-RPCID. 突变运行两次.

系统在全球范围内失败.

> 每个组件都在本地运作正确,系统在整个局面都失败了.

虽然MCP定义了消息和运输行为,但您的应用程序仍然拥有:

- 时间预算;
- 商业自由;
- 边界排队;
- 复试分类;
- 持续任务状态;
- 重新联系和重新调整政策.

通过这种方式,我们可以将这些决定构成一个确定性模拟器.
没有休息,插座或随机故障.
一个同步的线程测试迫使两个账本客户竞争
对于相同的无权重关.

## 取消请求是特定运输方式的

> **【中文解读】**意图在每个传输上都一样:客户端不再需要一个在路上的结果.`notifications/cancelled`通知(火-忘记,服务器不回复任何JSON-RPC响应); 流式HTTP上是直接关闭该请求自己的响应流(不要为普通HTTP请求POST取消通知,流关闭就是取消信号) ⋅服务器侧:观察到断开后应停止工作、不得再为该请求发送消息;对未知、完成或无法安全停止的请求可以忽略取消――注意服务器方向的取消很窄:studio上仅保留用于终止`subscriptions/listen`请我请你

客户不再需要飞行结果. 电线信号不同.

> 意图在每个传输上都一样:客户端不再需要在路上结果.

### 工作室 传输

通过使用一个共享的双向频道,客户端发送通知:

```json
{
  "jsonrpc": "2.0",
  "method": "notifications/cancelled",
  "params": {
    "requestId": 41,
    "reason": "User closed the operation"
  }
}
```

服务器没有发出任何JSON-RPC响应.

> 服务器不会发出任何JSON-RPC响应.

服务器应停止工作,释放资源,避免发送取消请求的回复. 当请求未知,已经完成或无法安全地停止时,它可能会忽视取消.

由于这些比赛被错误化,将会导致更多的比赛.

> 形、未知和完成的取消通知一律忽略把这些竞争态度变成新的错误只会产生更多竞争态度

### 流通的HTTP

现代流式HTTP给每个请求自己的HTTP响应或SSE响应流.客户端通过关闭该请求的响应流取消.

> 现代流通 HTTP 给每一个请求独立的 HTTP 响应或 SSE 响应流,客户端通过关闭该请求的响应流来取消.`notifications/cancelled`流的关闭就是取消信号. 服务器一旦观察到断开,就应停止工作,并且不得再发送任何消息.

不要发帖`notifications/cancelled`关闭流是取消信号.

一旦服务器观察到断开,该服务器应停止工作,不得再发送更多的信息.

### 服务器发送的取消是狭窄的

服务器不使用`notifications/cancelled`在工作室,服务器发送的取消仅用于终止一个 `subscriptions/listen`保持该路径与普通客户请求取消分开.

## 取消是一场竞赛

> **【中文解读】**两种事件顺序都合法的:取消先到服务器标记取消,工人 随后完成,服务器压掉响应;完成先到工人 提交结果,服务器发出响应,迟到的取消被忽视――网络延迟决定了双方都无法证明对方先看到哪个事件,所以客户端也必须忽视自己已经放弃请求的迟到响应――本课的`RequestCoordinator`为了每一个请求,只存在一个终态:取消之后.`complete()`已完成后迟到的取消也没有改变记录.

两项活动订单都有效.

> 两种事件顺序都是合法的.

### 取消胜利

```text
request starts
client sends cancellation signal
server marks request cancelled
worker reaches completion
server suppresses the response
```

### 完成胜利.完成胜利.

```text
request starts
worker commits the result
server sends the response
cancellation arrives late
server ignores the late notification
```

网络延迟意味着双方都无法证明另一方首先观察到哪个事件.

> 客户端也必须忽略自己已经放弃请求的迟到响应.

```figure
mcp-reliability-race
```

我们学会了什么?`RequestCoordinator`存储一个终端状态.`complete()`取消后没有回复. 取消迟到不能改变已完成的记录.

## 时间需要两个小时.

> **【中文解读】**只有一个不活动计时器是不够的. 设置两个上限:空超时 (空超时) 和最大超时 (最大超时) 从请求开始的绝对墙钟预算). 进度事件可以重新置空时钟,但永远不能移除最大期限. 示例里1500ms 由于最近进度只有300ms,而仍然活跃,2000ms 时,即使1999ms 刚到一条进度也必须取消.

一个无活动计时器不够.

使用两个限制:

1. **Idle timeout.**要求可能不会产生有用活动的时间.
2. **Maximum timeout.**要求开始时的绝对墙壁时钟预算.

进步可能会重新设置空时钟,

> 进度可以重新设置空时钟,但绝不能移除最大期限.

```text
start: 0 ms
progress: 400 ms
progress: 800 ms
progress: 1200 ms
idle timeout: 500 ms
maximum timeout: 2000 ms
```

在 1500 ms 时,请求仍然活跃,因为最新的进展仅仅是300 ms 时.在 2000 ms 时,最大的截止日期会取消它,即使在 1999 ms 时,另一个进展事件也会出现.

服务器可以接受一个进步代币,并且不会发出任何更新.

必须增加MCP进步值.通知完成或取消后停止. 速度限制进步,以便快速工人无法淹没运输.

## 取消请求是没有的`tasks/cancel`請取消`tasks/cancel`

> **【中文解读】**两种机制面对不同的生命周期:请求取消针对一条在路上 RPC的应用程序,成功含义是"客户端放弃了请求,服务器应酌情停止";`tasks/cancel`针对一个持久任务,是普通MCP请求,成功含义只是"服务器确认取消意图"不证明工人已停止,任务可能保持`working`由于 HTTP 连接关闭时不要清除持久任务状态:创建任务的原因是它的生命周期比单个请求和单个连接更长.

这些机制可以解决不同的生命.

| Mechanism | Target | Signal | What success means |
|-----------|--------|--------|--------------------|
| Request cancellation on stdio | One in-flight RPC | `notifications/cancelled` | Client abandoned the request; server should stop if practical |
| Request cancellation on HTTP | One in-flight response stream | Close the stream | Client abandoned the request; server should stop if practical |
| `tasks/cancel` | One durable Task | Ordinary MCP request | Server acknowledged cancellation intent |

一个成功的人`tasks/cancel`工作人员的工作可能仍然在工作中.`working`工人检查站观察旗之前.工作可能在该检查站之前完成.

> `tasks/cancel`工作成功结果并不证明工人已经停止了.`working`工作也可能在检查点之前完成.

当HTTP连接关闭时,不要删除持久任务状态.创建任务的原因是其生命周期超过一个请求和一个连接.

> 创建任务的原因是它的生命周期比单个请求和单个连接都长.

## 现在,我们需要一个新的JSON-RPCID,

> **【中文解读】**客户端使用 id 41 提交扣款、丢响、使用 id 42 重试服务器看到的是两个不同的消息,没有应用层键就无法知道它们是相同的结算──等键标识业务意图:服务器存储键、参数纹和已提交的结果;同键与返回存储的结果,同键不同参数直接拒绝防止键被误用到另一个业务操作造成二次变化.

 JSON-RPC id 相关请求和响应.它们不识别一个业务操作.

假设客户提交一个指控,`41`输出了回应,然后再试用ID`42`服务器看到两个不同的消息. 没有应用程序密钥,它不能知道它们代表一个支票.

无权密钥标识了商业意图:

```json
{
  "name": "charge_account",
  "arguments": {
    "account": "acct-7",
    "cents": 1200,
    "idempotencyKey": "checkout-7"
  }
}
```

服务器存储:

- 关键;
- 操作论证的指纹;
- 承诺的结果.

同样的关键和相同的参数返回存储的结果.同样的关键与不同的参数被拒绝. 这防止意外重复使用的关键改变了不同的业务操作.

> 服务器存储:键、操作参数的指纹、已提交的结果──同键同参返回存储的结果;同键不同参数被拒绝防止键被误用到另一个业务操作上──

>  **【类比】**等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等

### 账本边界必须是原子和持久的

> **【中文解读】**查键→执行变更→存储结果"这个序列不安全:两个工人都能观察到键缺失并都执行变更;效果后、存储之前崩也会在重试时制造相同的差异.`BEGIN IMMEDIATE`把键检查、模拟业务效果、执行计数和结果存储串入一个事务两个独立账本连接在同一键竞争时只会观察到一个已提交的结果和一次执行;关闭重开账本记录仍然存在.所有返回值都来自存储的JSON重建(防御性副本),调用方永远无法获得账本内部可变的对象.重要界:模拟业务效果是同一SQLite的回执和计数器,真实支付,部署或外部API调用不会因为写了一个本地表需要共享的持久数据库事务,事务性发送箱,或上游提供者使用相同的键等;仅靠锁既不存在多个副本的进程,也无法启动强有力的重组件.

这种序列是不安全的:

```text
check key
run mutation
store result
```

两个工人可以观察一个缺失的钥匙,
在效果之后,但在商店之前,重新尝试时会产生相同的模糊性.

课程使用文件支持的SQLite账本.`BEGIN IMMEDIATE`连续化
密钥检查,模拟业务效果,执行计数,以及存储成绩
两个独立的账本连接,用相同的密钥竞争
因此,观察一个承诺结果和一个执行.
记本保存了记录.

根据存储的JSON,每一个返回值都被重建.
由于本书所持的可变物体,因此更改返回的字典不能
后续复制结果.

模拟器的商业效果是收件和执行柜台
实际的支付,部署或外部API调用是
只有通过写一个本地表来制造原子.
共有数据库交易,交易输出箱或上游供应商
只有一个过程锁,不能保护
复制或重启.

### 试试矩阵

> **【中文解读】**实现重试之前先分类――安全类 (无副作用的确定性读) 了解失败边界后可换新的JSON-RPC id 重试;有条件类 (带持久等键的变化) 用同一个键和完全相同的参数重试;不安全类 (无业务重变) 不要自动重试,先对账――`readOnlyHint`,我知道.`idempotentHint`由于这种方法,它将被应用程序和服务器实现.

在实施之前重新分类尝试.

| Class | Example | Retry rule |
|------|---------|------------|
| Safe | Deterministic read with no side effect | Retry with a new JSON-RPC id after the failure boundary is understood |
| Conditional | Mutation with a durable idempotency key | Retry with the same key and identical arguments |
| Unsafe | Mutation without business deduplication | Do not retry automatically; reconcile first |

工具注释如`readOnlyHint`其他`idempotentHint`应用程序合同和服务器实现决定了重新尝试安全性.

## 压力是正确的部分.

> **【中文解读】**缓冲区的策略是"有界损+显然恢复":合并同代币的相邻进步;容量满时丢失最旧进步;将流标记为需要权威重取;始终保持最终响应;绝对不值保证一个最终响应而另一个.进步是可替代的,后代取代前值),最终JSON-RPC响应是不可替代的.

无限排队将缓慢转化为记忆耗尽.

通过一个有限的排队来定义可能丢失的东西.

进步可替换.后来的进步值取代了之前的值.最终的JSON-RPC响应是无法替换的.

课程缓冲适用于以下政策:

1. 为了同样实现相邻的进展.
2. 能达到最大的容量时,就放弃最古老的进步.
3. 标记流需要权威的改造.
4. 保存最后的反应.
5. 拒绝一个状态, 保存最终反应需要放下另一个最终反应.

丧不是一个策略.

> 这是一个失败的策略.

### 代理缓冲

一个服务器可以正确流动,而一个反向代理在缓冲中保存事件.

为了获得SSE的回应,请发送:

```http
Content-Type: text/event-stream
Cache-Control: no-cache
X-Accel-Buffering: no
```

2026 流式HTTP规范建议`X-Accel-Buffering: no`让兼容的代理人立即传递事件.

对于静静长期的流,定期发出SSE评论:

```text
:
```

客户忽略评论行,中间人看到流量,更不太可能关闭空置连接.

保持效率不是进步. 不要仅仅因为输送评论到达,重新设置操作的语义空置时间.

## 重连意味着重取

> **【中文解读】**现代流通 HTTP 不支持通过 `Last-Event-ID`恢复SSE.`subscriptions/listen`流断开后的五步恢复:使用新的JSON-RPC id 开新监听请求;恢复期望的订阅过器;从权威方法重获受影响的工具/资源/提示/任务;按稳定标识符对应用状态重重;绝不因为丢失了响应重放不安全的变化.`sendLastEventId`设为错误并列出重量资源.

现代流式HTTP不支持可重启的SSE通过 `Last-Event-ID`现在,我们要去.

在一个`subscriptions/listen`流量下降:

1. 打开一个新的听取请求,使用新的JSON-RPCID.
2. 恢复所需的订阅过器.
3. 根据权威方法,重新查找所影响的工具,资源,提示或任务.
4. 通过稳定标识符进行减复应用状态.
5. 不要因为没有反应而重复一个不安全的突变.

样本回收计划明确规定`sendLastEventId`其他地方的资源.

### 防止一群重新联系

如果1万个客户在1秒内重新连接,恢复服务器再次失败.

> 如果一万个客户端重连,正在恢复的服务器会再次倒下――使用上限的指数退加动――本课程从客户端 id 和尝试序号计算确定性动以确保测试可复制;生产可随机使用密码学安全或运行时――不变量是分布式,不是某种具体公式――

课程计算了客户端ID和尝试号码的确定性 jitter,因此测试仍然可复制:

```text
attempt 0: up to 250 ms
attempt 1: up to 500 ms
attempt 2: up to 1000 ms
...
cap: 8000 ms
```

产品可以使用加密安全或运行时间随机性. 不变量是分布,而不是特定的公式.

## 建立它,实现它.

> **【中文解读】** `code/main.py`实现五个小组件:`RequestCoordinator`(双期在请求中"",单调进度"",正确的录像室/HTTP 取消信号"",忽略非法取消"",取消与完成的终端竞争状态显式化"",服务器方向取消仅保留给录像室订阅);`MutationLedger`(证明两个JSON-RPC id 会执行两次的SQLite事件串起键检查/效果/计数/提交、跨连接重复、同键异参拒绝、防御性副本、重开账本记录仍存在);`DurableTaskService`(确认取消请求但保持 `working`工作者检查点,演示"确认不是终态");`BoundedSseBuffer`恢复辅助; 代理安全的SSE头与保生注释; 重连重取计划;确定性指数退避加动) 

`code/main.py`构建了五个小型可靠性组件.

### `RequestCoordinator`

- 开始在飞行时提出的空置和最高截止日期请求;
- 发出单调的进展通知;
- 产生正确的stdio或HTTP取消信号;
- 忽略无效的取消通知;
- 明确取消和完成终端比赛;
- 保留服务器发送的取消,

### `MutationLedger`

- 证明两个JSON-RPCID没有商用密钥执行两次;
- 使用文件支持的SQLite交易进行键检查,模拟效果,
  执行计数和结果承诺;
- 在一个独立的无能率键下,将匹配的参数进行排版
  账本连接;
- 拒绝使用不同的参数重复使用的单个关键;
- 恢复了防守副本,并保存了已提交的记录.

### `DurableTaskService`

- 确认取消请求;
- 能完成任务`working`直到工人检查站;
- 证明确认为什么不是最终状态.

### `BoundedSseBuffer`

- 压力下合或降低进展;
- 记录需要进行权威的改编;
- 没有任何最终反应.

### 恢复人员

- 返回安全的代理SSE标题和保留意见;
- 建立重新连接和重新调整计划;
- 扩散复试, 具有决定性指数的反弹和.

## 让它变得更好.

根据数据库根:

```bash
cd phases/13-tools-and-protocols/29-mcp-reliability-cancellation-and-flow-control/code
python3 main.py
python3 -m unittest discover tests -v
```

演示程序运行了中央竞赛的两侧,
在临时文件支持的本书中,除复制突变,超载了有限的
显示一个持续的任务从已确认的取消移动
工人观察到的取消.

## 互动实验室

运行四次活动,没有增加睡眠.

> 不加任何睡眠,跑四种事件序列:A 先取消后完成;B 先完成 后送达取消;;响应保留、迟到取消被忽略);C 在每个空期限前发进度然后过最大期限;;仍被取消;D 在 Streamable HTTP 上关闭其响应流;;每个场景记录:请求终态是否存在最终响应、线上发射的取消、信号客户端应忽略哪个事件──再把D 换成工作室操作完全相同,取消信号必须改变──

1. 开始请求`A`取消,然后打电话`complete()`现在,我们要去.
2. 开始请求`B`完成,然后取消.
3. 开始请求`C`在每一个空的最后期限之前发出进展,然后超过最大的最后期限.
4. 开始请求`D`通过流式HTTP,关闭其响应流.

记录每个场景:

- 终端请求状态;
- 是否存在最终回应;
- 放到电线上的取消信号;
- 客户应该忽略哪个事件.

然后改变`D`操作是相同的,但取消信号必须改变.

## 实验室 进步实验

添加一个`reserve_inventory`变化到`MutationLedger`现在,我们要去.

> 给我一个`MutationLedger`另一个`reserve_inventory`变更──十条要求覆盖:键绑定 SKU/数量/租户/操作名;同键同参返回首次预约;改数则失败且不再预约;已提交但丢响可按键对账;结果不含密与付款数据;客户端没给键就禁自动重试;模拟订阅断开后先重复库存记录再决策;两个账户连接在屏障上并发钥提交断言只一次预约;改变首次返回的预约对象、重放钥匙、证明存储结果;关闭重账户文件后按键对账.保持诚实:如果库存存在于另一个服务中,说明是否接受同一个键,还是需要事务性提交账户到远端连接桥梁的效果.

要求:

1. 密钥将 SKU,数量,租户和运营名称绑定.
2. 通过相同的键和相同的参数再次尝试,将返回第一个预订.
3. 没有另一个保留,改变数量的重试失败.
4. 执行但失去了回应的执行可以通过关键调和.
5. 结果没有记录秘密或支付数据.
6. 如果客户端未提供钥匙,则将自动重新尝试禁用.
7. 在决定接下来要做什么之前,添加一个模拟的订阅下降,
8. 在一个屏障中启动两个账本连接,并提交相同的键
   确认已提交一个保留.
9. 转换返回的首个预订对象. 重复播放键,证明
   存储结果没有改变.
10. 关闭和重新打开本书文件,然后按键调整预订.

实验室诚实:如果库存存存入另一个服务,
服务接受相同的无权密钥,或者是否是交易输出箱
桥梁,地方的承诺是远程效应.

## 运送的艺术品产品

`outputs/skill-mcp-reliability-reviewer.md`提供MCP操作,运输,时间限度政策,重试行为,队列政策和恢复计划.它返回比赛表,重试分类,无能度边界,流量控制检查和故障装置.

> `outputs/skill-mcp-reliability-reviewer.md`是一个平面可靠评审技能:给它一个MCP操作,传输方式,超时策略,重试行为,队列策略和恢复计划,它回归竞争表,重试分类等边界,流量检查和失败设置.

## 检查一下.

> **【中文解读】**验收清单逐条过:studio 取消发送通知且未接收响应;HTTP 取消关流且未发取消 POST;先取消后完成压掉最终响应;先完成后取消保留响应并忽略迟到取消;进度能重置空超时但无法动最大时;只换新JSON-RPC id将再次执行变更;同键与参与两连接并发竞争中只执行一次;已提交记录可重载、重返返防御性开复本;改回对象不变存结果;有界缓冲不超容并保证最终响应;连接新请求、不发`Last-Event-ID`、重受影响状态;`tasks/cancel`确认后 工作人员观察到它之前保持非终态.

如果这些说法是真的,课程就会完整:

- 工作室取消发送`notifications/cancelled`他没有得到任何回应.
- 流式HTTP取消关闭请求流,并不会发送取消POST.
- 取消前完成抑制最终反应.
- 完全取消之前保留响应,忽略迟到取消.
- 进步可以重新设置空置时间,但永远不会达到最大的时间.
- 单独一个新的JSON-RPCID再次执行突变.
- 一个无效键和相同的参数执行一次在同时
  两连接的比赛.
- 复制后,可以恢复,反复复复制后,可以恢复.
- 转换返回结果不能改变存储的结果.
- 限制式缓冲器保持容量内,保持最终反应.
- 连接重新使用新的请求,不发送`Last-Event-ID`并且重新调整受影响的状态.
- `tasks/cancel`确认将使任务不终结,直到工人遵守它.

## 产品失败模式

> 下表左列失败、中列可观察症状、右列正确响应──最贵的三行:把新 RPC id 当重重时(扣款/部署/删除跑了两次) 关键检查与效果分离(并发工都看到了关键缺失) 、把任务 确认当最终取消(UI 显示已停停,工人还在跑) ⋅

| Failure | Observable symptom | Correct response |
|---------|--------------------|------------------|
| HTTP client POSTs cancellation notification | Server and client disagree about request lifetime | Close the request's SSE response stream |
| Server responds after accepted cancellation | Client receives an unusable late result | Stop work and suppress further messages when cancellation wins |
| Progress resets every deadline | Hung work survives forever | Keep a separate absolute maximum timeout |
| New RPC id treated as deduplication | Charge, deployment, or deletion runs twice | Add a durable application idempotency key |
| Key check and effect are separate | Concurrent workers both observe a missing key | Commit key claim, effect record, and result atomically |
| In-memory ledger used across replicas | Restart or another worker forgets prior commits | Use shared durable storage or upstream idempotency |
| Stored mutable result returned directly | Caller mutation corrupts later replays | Serialize committed results and return defensive copies |
| Key reused with changed arguments | One key aliases two business intents | Store and compare an argument fingerprint |
| Unbounded progress queue | Memory rises with a slow consumer | Coalesce and drop replaceable progress within a bound |
| Final response dropped under pressure | Client cannot know the request outcome | Reserve capacity or evict progress, never the final response |
| Proxy buffers SSE | Progress arrives in bursts or after timeout | Disable buffering and configure compatible proxy timeouts |
| `Last-Event-ID` assumed | Client resumes from state the server does not support | Reconnect with a new request and refetch |
| Every client reconnects immediately | Recovery creates another outage | Use capped exponential backoff with jitter |
| Task ack treated as final cancellation | Worker keeps running after UI says stopped | Poll the Task until a terminal status |

## 毕业项目 接下来

工具生态系统的终点石应该将可靠性视为可执行的证据,而不是建筑图中的段落.

> 工具生态毕业项目应将可靠性视为可执行的证据,而不是结构图中的一段文字. 要求的工件:每种传输一个取消竞争态记录,每种暴露变化的重试表,等键记录和失配配件,同键并发记录,重新开检,别名检查,有界缓冲过载结果,反向代理SSE头和空策略,点名权重取方法重连接,使用任务时持久任务 取消痕迹. 本地进程中的一项绿色请求只证明快乐路径丧失响应,迟到消耗,慢消费者和重连风暴有确定性结局,毕业项目达到生产能力的计划.

需要这些文物:

- 每辆运输的取消赛车记录;
- 每个暴露的突变的重试表;
- 无效密钥记录和不匹配装置;
- 一次同步的相同密钥转录,重新开放检查和突变代号检查;
- 限制缓冲过载结果;
- 逆代理SSE标题和空置政策;
- 连接计划,其中列出了权威的重复方法;
- 终点石使用Task时,具有持久的任务取消痕迹.

绿色要求在本地过程中证明了只有幸福的道路. 失败的反应,迟到的取消,消费者缓慢和重新连接的群体产生决定性结果时,终点石是生产准备的.

## 关键词 关键词

| Term | Meaning |
|------|---------|
| Request cancellation | Abandonment of one in-flight MCP request |
| Cancellation race | Competition between terminal completion and cancellation events |
| Idle timeout | Limit since the last useful request activity |
| Maximum timeout | Absolute limit from request start, unaffected by progress |
| Idempotency key | Application identifier that deduplicates one business intent |
| Atomic ledger | Durable boundary that commits the key claim, effect record, and result as one unit |
| Backpressure | Control applied when producers outpace consumers |
| Progress coalescing | Replacing older progress with a newer authoritative value |
| Refetch | Reading current state again after a stream gap |
| Jitter | Deliberate variation that spreads retries across time |

## 继续阅读 继续阅读

- [MCP Cancellation](https://modelcontextprotocol.io/specification/2026-07-28/basic/patterns/cancellation)
- [MCP Progress](https://modelcontextprotocol.io/specification/2026-07-28/basic/patterns/progress)
- [MCP Streamable HTTP](https://modelcontextprotocol.io/specification/2026-07-28/basic/transports/streamable-http)
- [MCP Tasks Extension](https://tasks.extensions.modelcontextprotocol.io/specification/draft/tasks)
