# MCP Reliability, Cancellation, and Flow Control | MCP 可靠性、取消与流控

> A request ID correlates a message. It does not make a side effect safe, stop a worker, or protect a stream from a slow consumer.

> **【中文解读】** 请求 ID 只负责关联消息：它不能让副作用变得安全、不能停掉一个 worker、也保护不了流不被慢消费者拖垮。本课基于 MCP 2026-07-28 规范讲分布式系统里最贵的那些 bug：取消竞态、双时钟超时、幂等重试、背压、重连风暴。核心立场：MCP 只定义消息和传输行为，时间预算、业务幂等、有界队列、重试分类、持久 Task 状态、重连与重取策略仍然归你的应用所有。

> **【拓展：MCP→分布式系统工程】** 这里出现的每个概念——取消信号与传输绑定、完成/取消竞态、空闲+绝对双超时、幂等键、事务性发件箱、背压、抖动退避——都是分布式系统的经典课题。本课的特殊性在于把它们放进 MCP 的具体语境：stdio 上取消是一条通知，Streamable HTTP 上取消是关闭响应流，`tasks/cancel` 面向持久 Task。Phase 13 · 13（异步 Tasks）是本课的直接前置。

> 🔗 **【前置】** 学本课前请先掌握：Phase 13 · 09（MCP 传输：stdio 与 Streamable HTTP 的差异）、Phase 13 · 13（异步 Tasks 扩展：Task 生命周期与 `tasks/cancel`）。

**Type:** Build | **类型:** 动手实践
**Languages:** Python | **语言:** Python
**Prerequisites:** Phase 13, Lessons 09 and 13 | **前置知识:** Phase 13 · 09、13
**Time:** ~120 minutes | **时间:** 约 120 分钟

## Learning Objectives | 学习目标

- Implement the correct cancellation signal for stdio and Streamable HTTP.
  中文翻译：为 stdio 和 Streamable HTTP 实现各自正确的取消信号。
- Resolve completion and cancellation races without sending messages after cancellation.
  中文翻译：解决"完成与取消"的竞态，且在取消之后不再发送消息。
- Separate request cancellation from durable `tasks/cancel` semantics.
  中文翻译：把请求取消与持久 `tasks/cancel` 语义区分开。
- Build retry decisions from side effects and explicit idempotency keys.
  中文翻译：基于副作用和显式幂等键构建重试决策。
- Bound progress queues while preserving final responses.
  中文翻译：给进度队列设界，同时保住最终响应。
- Recover streams through reconnect, refetch, and jittered backoff.
  中文翻译：通过重连、权威重取和带抖动的退避恢复流。

## The Problem | 问题引入

> **【中文解读】** 经典事故链：客户端调工具→服务器开工→进度到来→代理缓冲了流→客户端超时断开→服务器一毫秒后完成→客户端换一个新 JSON-RPC id 重试→变更执行了两次。每个组件在本地都行为正确，系统在全局上失败了。MCP 只管消息和传输；时间预算、业务幂等、有界队列、重试分类、持久任务状态、重连与重取策略这六件事归应用。本课的确定性模拟器不依赖 sleep、socket 或随机失败——你直接控制取消事件的顺序，还有一个同步线程测试逼两个账本客户端竞争同一个幂等键。

The happy path hides the most expensive distributed-systems bugs.

> 快乐路径（happy path）藏着最昂贵的分布式系统 bug。

A client calls a tool. The server starts work. Progress arrives. A proxy buffers the stream. The client reaches its timeout and disconnects. The server finishes one millisecond later. The client retries with a new JSON-RPC id. The mutation runs twice.

Every component behaved locally. The system failed globally.

> 每个组件在本地都行为正确，系统在全局上失败了。

MCP defines message and transport behavior, but your application still owns:

- time budgets;
- business idempotency;
- bounded queues;
- retry classification;
- durable task state;
- reconnect and refetch policy.

This lesson builds those decisions into a deterministic simulator. There are
no sleeps, sockets, or random failures. You control cancellation event order
directly. One synchronized thread test forces two ledger clients to compete
for the same idempotency key.

## Request Cancellation Is Transport-Specific | 请求取消是绑定传输方式的

> **【中文解读】** 意图在每个传输上都一样：客户端不再需要一个在途结果。但线上信号不同——stdio 上是一条 `notifications/cancelled` 通知（fire-and-forget，服务器不回任何 JSON-RPC 响应）；Streamable HTTP 上是直接关闭该请求自己的响应流（不要为普通 HTTP 请求 POST 取消通知，流关闭就是取消信号）。服务器侧：观察到断开后应停止工作、不得再为该请求发消息；对未知、已完成或无法安全停止的请求可以忽略取消。注意服务器方向的取消很窄：stdio 上仅保留用于终止 `subscriptions/listen` 请求。

The intent is the same on every transport: the client no longer needs an in-flight result. The wire signal is different.

> 意图在每个传输上都一样：客户端不再需要一个在途结果。线上信号却是不同的。

### stdio | stdio 传输

stdio uses one shared bidirectional channel. A client sends a notification:

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

The notification is fire-and-forget. The server emits no JSON-RPC response to it.

> 这条通知是发后即忘的，服务器不会为它发出任何 JSON-RPC 响应。

The server should stop work, free resources, and avoid sending a response for the cancelled request. It may ignore cancellation when the request is unknown, already finished, or cannot be stopped safely.

Malformed, unknown, and already completed cancellation notifications are ignored. Turning those races into new errors would create more races.

> 畸形、未知和已完成的取消通知一律忽略——把这些竞态变成新错误只会制造更多竞态。

### Streamable HTTP | Streamable HTTP 传输

Modern Streamable HTTP gives each request its own HTTP response or SSE response stream. The client cancels by closing that request's response stream.

> 现代 Streamable HTTP 给每个请求独立的 HTTP 响应或 SSE 响应流，客户端通过关闭该请求的响应流来取消。不要为普通 HTTP 请求 POST `notifications/cancelled`——流的关闭就是取消信号。服务器一旦观察到断开，就应停止工作，并且不得再为该请求发送任何消息。

Do not POST `notifications/cancelled` for an ordinary HTTP request. Stream closure is the cancellation signal.

Once the server observes the disconnect, it should stop work and must not send more messages for that request.

### Server-sent cancellation is narrow

A server does not use `notifications/cancelled` to cancel arbitrary client calls. On stdio, server-sent cancellation is reserved for terminating a `subscriptions/listen` request. Keep that path separate from ordinary client-request cancellation.

## Cancellation Is a Race | 取消是一场竞态

> **【中文解读】** 两种事件顺序都合法：取消先到——服务器标记取消，worker 随后完成，服务器压掉响应；完成先到——worker 提交结果，服务器发出响应，迟到的取消被忽略。网络延迟决定了双方都无法证明对方先看到哪个事件，所以客户端也必须忽略自己已放弃请求的迟到响应。本课的 `RequestCoordinator` 为每个请求只存一个终态：取消之后 `complete()` 不再返回响应，已完成之后迟到的取消也改变不了记录。

Two event orders are both valid.

> 两种事件顺序都是合法的。

### Cancellation wins | 取消获胜

```text
request starts
client sends cancellation signal
server marks request cancelled
worker reaches completion
server suppresses the response
```

### Completion wins | 完成获胜

```text
request starts
worker commits the result
server sends the response
cancellation arrives late
server ignores the late notification
```

The client must also ignore a late response for a request it already abandoned. Network latency means neither side can prove which event the other side observed first.

> 客户端也必须忽略自己已放弃请求的迟到响应。网络延迟意味着双方都无法证明对方先观察到哪个事件。

```figure
mcp-reliability-race
```

The lesson's `RequestCoordinator` stores one terminal state. `complete()` returns no response after cancellation. A late cancellation cannot change a completed record.

## Timeouts Need Two Clocks | 超时需要两个时钟

> **【中文解读】** 只有一个不活动计时器是不够的。要设两个上限：空闲超时（多久没有有用活动）和最大超时（从请求开始的绝对墙钟预算）。进度事件可以重置空闲时钟，但永远不能移除最大期限——示例里 1500ms 时因最近进度只有 300ms 而仍然活跃，2000ms 时即使 1999ms 刚到一条进度也必须取消。另外：进度是可选的，服务器可以收下进度 token 却一条都不发，绝不能把"token 的存在"变成无限超时；MCP 进度值必须递增，完成或取消后通知停止，并且要限速防止快 worker 淹没传输。

A single inactivity timer is not enough.

Use two limits:

1. **Idle timeout.** How long the request may produce no useful activity.
2. **Maximum timeout.** The absolute wall-clock budget from request start.

Progress may reset the idle clock. It must never remove the maximum deadline.

> 进度可以重置空闲时钟，但绝不能移除最大期限。

```text
start: 0 ms
progress: 400 ms
progress: 800 ms
progress: 1200 ms
idle timeout: 500 ms
maximum timeout: 2000 ms
```

At 1500 ms, the request is still active because the latest progress is only 300 ms old. At 2000 ms, the maximum deadline cancels it even if another progress event arrived at 1999 ms.

Progress is optional. A server can accept a progress token and emit no updates. Never turn the presence of a token into an infinite timeout.

MCP progress values must increase. Notifications stop after completion or cancellation. Rate-limit progress so a fast worker cannot flood the transport.

## Request Cancellation Is Not `tasks/cancel` | 请求取消不是 `tasks/cancel`

> **【中文解读】** 两种机制面对不同的生命周期：请求取消针对一条在途 RPC（stdio 发通知、HTTP 关流），成功含义是"客户端放弃了请求，服务器应酌情停止"；`tasks/cancel` 针对一个持久 Task，是普通 MCP 请求，成功含义只是"服务器确认了取消意图"——并不证明 worker 已停止，Task 可能保持 `working` 直到某个 worker 检查点观察到标志，工作也可能在那个检查点之前完成。因此 HTTP 连接关闭时不要清除持久 Task 状态：创建 Task 的理由就是它的生命周期比单个请求和单个连接更长。

These mechanisms solve different lifetimes.

| Mechanism | Target | Signal | What success means |
|-----------|--------|--------|--------------------|
| Request cancellation on stdio | One in-flight RPC | `notifications/cancelled` | Client abandoned the request; server should stop if practical |
| Request cancellation on HTTP | One in-flight response stream | Close the stream | Client abandoned the request; server should stop if practical |
| `tasks/cancel` | One durable Task | Ordinary MCP request | Server acknowledged cancellation intent |

A successful `tasks/cancel` result does not prove the worker stopped. The task may remain `working` until a worker checkpoint observes the flag. Work may complete before that checkpoint.

> `tasks/cancel` 的成功结果并不证明 worker 已停止。Task 可能保持 `working`，直到某个 worker 检查点观察到取消标志；工作也可能在那个检查点之前完成。

Do not erase durable task state when the HTTP connection closes. The reason to create a Task is that its lifecycle outlives one request and one connection.

> HTTP 连接关闭时不要清除持久 Task 状态。创建 Task 的理由，就是它的生命周期比单个请求和单个连接都长。

## A New JSON-RPC ID Is Not Idempotency | 新的 JSON-RPC ID 不等于幂等

> **【中文解读】** JSON-RPC id 只关联请求与响应，不标识业务操作。客户端用 id 41 提交扣款、丢了响应、用 id 42 重试——服务器看到的是两条不同的消息，没有应用层键就无法知道它们是同一笔结算。幂等键标识业务意图：服务器存下键、参数指纹和已提交结果；同键同参返回存储的结果，同键不同参直接拒绝——防止键被误用到另一个业务操作上造成二次变更。

JSON-RPC ids correlate requests and responses. They do not identify a business operation.

Suppose a client submits a charge with id `41`, loses the response, and retries with id `42`. The server sees two different messages. Without an application key, it cannot know they represent one checkout.

An idempotency key identifies the business intent:

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

The server stores:

- the key;
- a fingerprint of operation arguments;
- the committed result.

The same key and same arguments return the stored result. The same key with different arguments is rejected. This prevents accidental key reuse from mutating a different business operation.

> 服务器存储：键、操作参数的指纹、已提交的结果。同键同参返回存储的结果；同键不同参被拒绝——防止键被误用到另一个业务操作上。

> 💡 **【类比】** 幂等键像高铁购票的"订单号"。你在 12306 下单后支付超时，重新发起支付用的是同一个订单号——系统认出"这单已经出过票"，直接把原来的票给你，而不是再扣一次款卖你第二张。JSON-RPC id 则像每次点击生成的会话流水号：换个流水号重试，售票系统就当成全新的购买。

### The ledger boundary must be atomic and durable | 账本边界必须原子且持久

> **【中文解读】** "查键→执行变更→存结果"这个序列不安全：两个 worker 都能观察到键缺失并都执行变更；效果之后、存储之前崩溃也会在重试时制造同样的歧义。本课用文件型 SQLite 账本，以 `BEGIN IMMEDIATE` 把键检查、模拟业务效果、执行计数和结果存储串进一个事务——两个独立账本连接用同一个键竞争时只会观察到一个已提交结果和一次执行；关闭重开账本记录仍在。所有返回值都从存储的 JSON 重建（防御性副本），调用方永远拿不到账本内部的可变对象。重要边界：模拟的业务效果是同一 SQLite 事务里的回执和计数器，真实的支付、部署或外部 API 调用不会因为写了一张本地表就变原子——生产需要可共享的持久数据库事务、事务性发件箱，或上游提供方强制同样的幂等键；仅靠进程锁既护不住多副本也活不过重启。

This sequence is unsafe:

```text
check key
run mutation
store result
```

Two workers can both observe a missing key and both run the mutation. A crash
after the effect but before the store creates the same ambiguity on retry.

The lesson uses a file-backed SQLite ledger. `BEGIN IMMEDIATE` serializes the
key check, simulated business effect, execution counter, and stored result into
one transaction. Two independent ledger connections racing with the same key
therefore observe one committed result and one execution. Closing and reopening
the ledger keeps that record.

Every return value is reconstructed from stored JSON. The caller never receives
the mutable object held by the ledger, so changing a returned dictionary cannot
corrupt later replay results.

The simulator's business effect is the receipt and execution counter inside the
same SQLite transaction. A real payment, deployment, or external API call is
not made atomic merely by writing a local table. Production needs a durable
shared database transaction, a transactional outbox, or an upstream provider
that enforces the same idempotency key. A process lock alone does not protect
multiple replicas or survive a restart.

### Retry matrix | 重试矩阵

> **【中文解读】** 实现重试之前先分类。安全类（无副作用的确定性读）理解失败边界后可换新 JSON-RPC id 重试；有条件类（带持久幂等键的变更）用同一个键和完全相同的参数重试；不安全类（没有业务去重的变更）不要自动重试，先对账。`readOnlyHint`、`idempotentHint` 这类工具注解始终是不可信提示——重试安全由应用契约和服务器实现决定。

Classify retries before implementing them.

| Class | Example | Retry rule |
|------|---------|------------|
| Safe | Deterministic read with no side effect | Retry with a new JSON-RPC id after the failure boundary is understood |
| Conditional | Mutation with a durable idempotency key | Retry with the same key and identical arguments |
| Unsafe | Mutation without business deduplication | Do not retry automatically; reconcile first |

Tool annotations such as `readOnlyHint` and `idempotentHint` remain untrusted hints. The application contract and server implementation decide retry safety.

## Backpressure Is Part of Correctness | 背压是正确性的一部分

> **【中文解读】** SSE 生产者产生进度的速度可能快于客户端、代理或网络的消费速度，无界队列会把"慢"变成"内存耗尽"。本课缓冲区的策略是"有界丢失 + 显式恢复"：合并同一 token 的相邻进度；容量满时丢最旧进度；把流标记为需要权威重取；始终保住最终响应；绝不为保一个最终响应而丢另一个。进度是可替代的（后值取代前值），最终 JSON-RPC 响应不可替代。静默丢失不是策略。

An SSE producer can generate progress faster than a client, proxy, or network can consume it. An unbounded queue converts slowness into memory exhaustion.

Use a bounded queue and define what can be lost.

Progress is replaceable. A later progress value supersedes an earlier one for the same token. A final JSON-RPC response is not replaceable.

The lesson buffer applies this policy:

1. Coalesce adjacent progress for the same token.
2. Drop the oldest progress when capacity is reached.
3. Mark the stream as needing authoritative refetch.
4. Preserve the final response.
5. Refuse a state where preserving the final response would require dropping another final response.

This is bounded loss with explicit recovery. Silent loss is not a strategy.

> 这是有界丢失加显式恢复。静默丢失不是策略。

### Proxy buffering | 代理缓冲

A server can stream correctly while a reverse proxy holds events in a buffer.

For an SSE response, send:

```http
Content-Type: text/event-stream
Cache-Control: no-cache
X-Accel-Buffering: no
```

The 2026 Streamable HTTP specification recommends `X-Accel-Buffering: no` so compatible proxies deliver events immediately.

For quiet long-lived streams, periodically emit an SSE comment:

```text
:
```

The client ignores comment lines. Intermediaries see traffic and are less likely to close an idle connection.

Keepalive is not progress. Do not reset an operation's semantic idle timeout merely because a transport comment arrived.

## Reconnect Means Refetch | 重连意味着重取

> **【中文解读】** 现代 Streamable HTTP 不支持通过 `Last-Event-ID` 恢复 SSE。`subscriptions/listen` 流断开后的五步恢复：用新 JSON-RPC id 开新的监听请求；恢复期望的订阅过滤器；从权威方法重取受影响的 tools/resources/prompts/Tasks；按稳定标识符对应用状态去重；绝不因为丢了响应就重放不安全的变更。示例恢复计划显式把 `sendLastEventId` 设为 false 并列出要重取的资源。

Modern Streamable HTTP does not support resumable SSE through `Last-Event-ID`.

After a `subscriptions/listen` stream drops:

1. Open a new listen request with a new JSON-RPC id.
2. Restore the desired subscription filter.
3. Refetch affected tools, resources, prompts, or Tasks from authoritative methods.
4. Deduplicate application state by stable identifiers.
5. Do not replay an unsafe mutation just because its response was lost.

The sample recovery plan explicitly sets `sendLastEventId` to false and lists resources to refetch.

### Prevent a reconnect herd | 防止重连风暴

If 10,000 clients reconnect at exactly one second, the recovering server fails again.

> 如果一万个客户端在同一秒重连，正在恢复的服务器会再次倒下。用带上限的指数退避加抖动。本课从客户端 id 和尝试序号计算确定性抖动以保证测试可复现；生产可以用密码学安全或运行时随机性。不变量是分布形态，不是某个具体公式。

Use exponential backoff with jitter and a cap. The lesson computes deterministic jitter from client id and attempt number so tests remain reproducible:

```text
attempt 0: up to 250 ms
attempt 1: up to 500 ms
attempt 2: up to 1000 ms
...
cap: 8000 ms
```

Production can use cryptographically secure or runtime randomness. The invariant is distribution, not a specific formula.

## Build It | 动手实现

> **【中文解读】** `code/main.py` 实现五个小组件：`RequestCoordinator`（双期限在途请求、单调进度、正确的 stdio/HTTP 取消信号、忽略非法取消、把取消与完成的终态竞态显式化、服务器方向取消仅保留给 stdio 订阅）；`MutationLedger`（证明两个 JSON-RPC id 会执行两次、SQLite 事务串起键检查/效果/计数/提交、跨连接去重、同键异参拒绝、防御性副本、重开账本记录仍在）；`DurableTaskService`（确认取消请求但保持 `working` 直到 worker 检查点，演示"确认不是终态"）；`BoundedSseBuffer`（压力下合并或丢进度、标记需权威重取、绝不动最终响应）；恢复辅助（代理安全的 SSE 头与保活注释、重连重取计划、确定性指数退避加抖动）。

`code/main.py` builds five small reliability components.

### `RequestCoordinator`

- starts an in-flight request with idle and maximum deadlines;
- emits monotonic progress notifications;
- produces the correct stdio or HTTP cancellation signal;
- ignores invalid cancellation notifications;
- makes cancellation and completion terminal races explicit;
- reserves server-sent cancellation for stdio subscriptions.

### `MutationLedger`

- proves that two JSON-RPC ids execute twice without a business key;
- uses a file-backed SQLite transaction for the key check, simulated effect,
  execution counter, and result commit;
- deduplicates matching arguments under one idempotency key across independent
  ledger connections;
- rejects one key reused with different arguments;
- returns defensive copies and preserves committed records across reopen.

### `DurableTaskService`

- acknowledges a cancellation request;
- keeps the task `working` until a worker checkpoint;
- demonstrates why acknowledgement is not final status.

### `BoundedSseBuffer`

- coalesces or drops progress under pressure;
- records that authoritative refetch is required;
- never drops the final response.

### Recovery helpers

- return proxy-safe SSE headers and keepalive comments;
- create a reconnect and refetch plan;
- spread retries with deterministic exponential backoff and jitter.

## Use It | 学以致用

From the repository root:

```bash
cd phases/13-tools-and-protocols/29-mcp-reliability-cancellation-and-flow-control/code
python3 main.py
python3 -m unittest discover tests -v
```

The demo runs both sides of the central race, executes a transactionally
deduplicated mutation in a temporary file-backed ledger, overloads a bounded
progress buffer, and shows a durable Task moving from acknowledged cancellation
to worker-observed cancellation.

## Interactive Lab | 交互实验

Run four event orderings without adding sleeps.

> 不加任何 sleep，跑四种事件顺序：A 先取消后 complete（响应被压掉）；B 先 complete 后送达取消（响应保留、迟到取消被忽略）；C 在每个空闲期限前发进度然后越过最大期限（仍被取消）；D 在 Streamable HTTP 上关闭其响应流。每个场景记录：请求终态、是否存在最终响应、线上发出的取消信号、客户端该忽略哪个事件。再把 D 换成 stdio——操作完全相同，取消信号必须换。

1. Start request `A`, cancel it, then call `complete()`.
2. Start request `B`, complete it, then deliver cancellation.
3. Start request `C`, emit progress before every idle deadline, then cross the maximum deadline.
4. Start request `D` over Streamable HTTP and close its response stream.

Record for each scenario:

- the terminal request state;
- whether a final response exists;
- the cancellation signal placed on the wire;
- which event the client should ignore.

Then change `D` to stdio. The operation is identical, but the cancellation signal must change.

## Practice Lab | 进阶练习

Add a `reserve_inventory` mutation to `MutationLedger`.

> 给 `MutationLedger` 加一个 `reserve_inventory` 变更。十条要求覆盖：键绑定 SKU/数量/租户/操作名；同键同参返回首次预约；改数量则失败且不再预约；已提交但丢响应可按键对账；结果不含 secret 与支付数据；客户端没给键就禁用自动重试；模拟订阅断开后先重取库存记录再决策；两个账本连接在 barrier 上并发同键提交、断言只有一次预约；改掉第一次返回的预约对象、重放键、证明存储结果没变；关闭重开账本文件后按键对账。保持诚实：如果库存在另一个服务里，说明它是否接受同一个幂等键，还是需要事务性发件箱把本地提交桥接到远端效果。

Requirements:

1. The key binds SKU, quantity, tenant, and operation name.
2. A retry with the same key and same arguments returns the first reservation.
3. A retry with changed quantity fails without another reservation.
4. An execution that committed but lost its response can be reconciled by key.
5. The result records no secret or payment data.
6. Automatic retry is disabled when the client did not provide a key.
7. Add a simulated subscription drop and refetch the inventory record before deciding what to do next.
8. Start two ledger connections at a barrier and submit the same key
   concurrently. Assert one reservation was committed.
9. Mutate the first returned reservation object. Replay the key and prove the
   stored result did not change.
10. Close and reopen the ledger file, then reconcile the reservation by key.

Keep the lab honest: if inventory lives in another service, explain whether
that service accepts the same idempotency key or whether a transactional outbox
bridges the local commit to the remote effect.

## Shipped Artifact | 产出物

`outputs/skill-mcp-reliability-reviewer.md` is a flat reliability review skill. Give it an MCP operation, transport, timeout policy, retry behavior, queue policy, and recovery plan. It returns a race table, retry classification, idempotency boundary, flow-control checks, and failure fixtures.

> `outputs/skill-mcp-reliability-reviewer.md` 是一个扁平的可靠性评审 skill：给它一个 MCP 操作、传输方式、超时策略、重试行为、队列策略和恢复计划，它返回竞态表、重试分类、幂等边界、流控检查和失败 fixture。

## Verify It | 验证

> **【中文解读】** 验收清单逐条过：stdio 取消发通知且收不到响应；HTTP 取消关流且不发取消 POST；先取消后完成压掉最终响应；先完成后取消保留响应并忽略迟到取消；进度能重置空闲超时但动不了最大超时；仅换新 JSON-RPC id 会再次执行变更；同键同参在双连接并发竞争下只执行一次；已提交记录经得起重开、重放返回防御性副本；改返回对象改不动存储结果；有界缓冲不超容量且保住最终响应；重连用新请求、不发 `Last-Event-ID`、重取受影响状态；`tasks/cancel` 确认后 Task 保持非终态直到 worker 观察到它。

The lesson is complete when these statements are true:

- stdio cancellation sends `notifications/cancelled` and receives no response.
- Streamable HTTP cancellation closes the request stream and sends no cancellation POST.
- Cancel-before-complete suppresses the final response.
- Complete-before-cancel preserves the response and ignores the late cancellation.
- Progress can reset idle timeout but never maximum timeout.
- A new JSON-RPC id alone executes the mutation again.
- One idempotency key and identical arguments execute once under a concurrent
  two-connection race.
- A committed record survives reopen and replay returns a defensive copy.
- Mutating one returned result cannot alter the stored result.
- The bounded buffer stays within capacity and preserves the final response.
- Reconnect uses a new request, does not send `Last-Event-ID`, and refetches affected state.
- `tasks/cancel` acknowledgement leaves the task non-terminal until the worker observes it.

## Production Failure Modes | 生产失败模式

> 下表左列失败、中列可观察症状、右列正确响应。最贵的三行：把新 RPC id 当去重（扣款/部署/删除跑了两次）、键检查与效果分离（并发 worker 都看到键缺失）、把 Task 确认当最终取消（UI 显示已停、worker 还在跑）。

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

## Capstone Connection | 毕业项目衔接

The tool-ecosystem capstone should treat reliability as executable evidence, not a paragraph in an architecture diagram.

> 工具生态毕业项目应把可靠性当作可执行的证据，而不是架构图里的一段文字。要求的工件：每种传输一份取消竞态记录、每个暴露变更的重试表、幂等键记录与失配 fixture、同键并发记录、重开检查、别名检查、有界缓冲过载结果、反向代理 SSE 头与空闲策略、点名权威重取方法的重连计划、使用 Tasks 时的持久 Task 取消 trace。本地进程里的一次绿色请求只证明了快乐路径——丢失响应、迟到取消、慢消费者和重连风暴都有确定性结局时，毕业项目才达到生产就绪。

Require these artifacts:

- one cancellation race transcript for each transport;
- a retry table for every exposed mutation;
- an idempotency-key record and mismatch fixture;
- a concurrent same-key transcript, a reopen check, and a mutation-alias check;
- a bounded-buffer overload result;
- reverse-proxy SSE headers and idle policy;
- a reconnect plan that names authoritative refetch methods;
- a durable Task cancellation trace when the capstone uses Tasks.

A green request in a local process proves only the happy path. The capstone is production-ready when lost responses, late cancellation, slow consumers, and reconnect herds have deterministic outcomes.

## Key Terms | 关键术语

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

## Further Reading | 延伸阅读

- [MCP Cancellation](https://modelcontextprotocol.io/specification/2026-07-28/basic/patterns/cancellation)
- [MCP Progress](https://modelcontextprotocol.io/specification/2026-07-28/basic/patterns/progress)
- [MCP Streamable HTTP](https://modelcontextprotocol.io/specification/2026-07-28/basic/transports/streamable-http)
- [MCP Tasks Extension](https://tasks.extensions.modelcontextprotocol.io/specification/draft/tasks)
