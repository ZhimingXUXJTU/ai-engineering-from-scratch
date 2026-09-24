# 生产规模 排队,检查站,耐用性 检查点 生产 扩展队列

> 扩展多代理系统到数千次同时运行需要**durable execution**工作队列加上检查站,因此任何工人都可以在任何事故后恢复任何运行,只要租处理,无效的副作用和确定性重播都在位. 兰格拉夫的运行时间是参考例子:它在每个超级步骤后写出检查站`thread_id`工人失业后,工人重新开始租,代理人可以无限期地等待人力投入. **MegaAgent**根据该报告,该报告的内容包括:**Fiber/async**对于LLM流媒体,线程在99%的时间里停留无事,纤维在合作中输入/运输.**FastAPI + Postgres + nothing else**在负载证明不一样之前,简单的架构比预期要远.这个课程建立了一个持久的检查点日志,一个每个代理的工作队列,状态过渡,一个asyncvsthread演示,并降落实态的"开始简单"规则.

> **【中文解读】**本节介绍了多代理系统的生产扩展队列,检查点和扩展策略.

> **【拓展：production scaling queues checkpoints→具体应用】**多代理 系统的生产扩展需要:(1) 消息队列Kafka/RabbitMQ 缓冲代理 间的消息;(2) 检查点定期保存系统状态以支持恢复;(3) 负载平衡将任务均分配给可用的代理 实例;(4) 水平扩展动态增长减小代理 数量应对负载变化――长度图云和时间云是该领域的两个主要选择――


**Type:** Learn + Build | **类型:** 学习 + 构建
**Languages:** Python (stdlib, `asyncio`, `sqlite3`) | **语言:** Python（标准库，`asyncio`，`sqlite3`）
**Prerequisites:** Phase 16 · 09 (Parallel Swarm Networks), Phase 16 · 13 (Shared Memory) | **前置知识:** Phase 16 · 09（并行群体网络），Phase 16 · 13（共享内存）

>  **【前置】**学本节前请先掌握:阶段16·09(群) 阶段16·13(共享内存) 阶段15·12(可持续执行) 异步编程(asyncio) 〔多 代理 生产扩展 = 分布式系统工程问题〕
>  **【类比】**多代理 扩展 = "外卖平台架构"――检查点:快API + Postgres + 都不加,先跑起来――简单架构往往比预期走得远――
**Time:** ~75 minutes | **时间:** ~75 分钟

## 问题 问题引入

一个原型多代理系统在一个笔记本电脑上运行,有三个代理在内存事件循环中.

> 原型多代理 系统在一个笔记本电脑上使用三个代理 在内存事件循环中运行.

- 代理人有时会花费几个小时 (长时间的研究,
  中文翻译:代理 有时运行数小时
- 工人进程崩,重新启动失去了状态.
  中文翻译:工作者进程崩──重启丢失状态──
- 平均水平是10倍,需要水平扩展.
  中文翻译:峰值负载是平均的10倍;你需要水平扩展.
- 用户每次运行都会付费,需要一次性语义来充电.
  中文翻译:用户按代理运行付费;你需要恰好一次的计费语义。

记忆中的事件循环没有任何这些.你需要一个持久的执行层. 2026 规范的选项是:

> 您需要一个持久执行层.

1. 工作流动引擎,具有检查点 (时间,长图运行时间).
   中文翻译:带检查点工作流引擎(时间、长图 运行时) ⋅
2. 随着国家商店的消息排队 (Postgres + SQS/RabbitMQ).
   中文翻译:带状态存储的消息队列(Postgres + SQS/RabbitMQ) 』
3. 演员模式框架 (每代理人每位MegaAgent的生产者-消费者).
   中文翻译:演员模型框架 (MegaAgent的每一个代理生产者消费者)
4. 手动 FastAPI + Postgres (贝迪的论点).
   中文翻译:手工搭建的快API + 后生的论点) 』

这一课构建了每个小图.

> 本课构建每个微型版本.

## 概念的核心概念

### 持续执行,模式

长期执行引擎在每一步之后保持完整的程序状态 (在LangGraph语言中说超级步骤).

```
worker crashes mid-step
  -> lease timeout
  -> another worker picks up the thread_id
  -> resumes from last checkpoint
  -> no duplicate side effects
```

要求:

- **Serializable state.**任何代理状态都必须持续. 连接数据库的功能关闭不会存活.
- **Deterministic resume.**由于相同状态和相同的输入,代理产生相同的行动 (或将其推迟到外部确定性预言器来进行LLM调用).
- **Idempotent side effects.**外部调用 (工具调用,支付) 必须无效或使用减倍密钥.

拉格格拉夫在每一个超级步骤之后写一个检查点; 时间表在每一个活动之后写一个检查点; 重新使用事件来源的日志.所有三个都实现相同的模式.

### 检查点每步运行时间

运行时间是工作的例子:每个代理都有一个`thread_id`总结: 运行时间从最后一个检查点重播,而不是从零开始. 代理人可以`interrupt()`工作时间持续,释放了工人.

根据"中国"的标题,

### 对于每位代理人,MegaAgent的排队

建筑: 建筑: 建筑: 建筑: 建筑: 建筑: 建筑: 建筑: 建筑: 建筑: 建筑: 建筑: 建筑: 建筑: 建筑: 建筑: 建筑: 建筑: 建筑: 建筑: 建筑: 建筑: 建筑: 建筑: 建筑: 建筑: 建筑: 建筑: 建筑: 建筑: 建筑: 建筑: 建筑: 建筑: 建筑: 建筑: 建筑: 建筑: 建筑: 建筑: 建筑: 建筑: 建筑: 建筑: 建筑: 建筑: 建筑: 建筑: 建筑: 建筑: 建筑: 建筑: 建筑: 建筑: 建筑: 建筑: 建筑: 建筑: 建筑: 建筑: 建筑: 建筑: 建筑: 建筑: 建筑: 建筑: 建筑: 建筑: 建筑: 建筑: 建筑: 建筑: 建筑: 建筑: 建筑: 建筑: 建筑: 建筑: 建筑: 建筑: 建筑: 建筑: 建筑: 建筑: 建筑: 建筑: 建筑: 建筑: 建筑: 建筑: 建筑: 建筑: 建筑: 建筑: 建筑: 建筑: 建筑: 建筑: 建筑: 建筑: 建筑: 建筑: 建筑: 建筑: 建筑: 建筑: 建筑: 建筑: 建筑:

```
agent i:
  state ∈ {Idle, Processing, Response}
  in_queue   <- messages addressed to agent i
  out_queue  -> replies + side effects

coordinators:
  intra-group chat  (agents in the same group)
  inter-group admin chat  (high-level routing)
```

两层协调使得集团内部对话发生密集,而集团间保持稀少.

### 同比对每项工作的线程

电话是 I/O 绑定.一个线程等待下一个代币是置的99%.线程每一个成本 ~ 1MB RAM;在 10,000 个同时电话,这仅仅是10GB 堆.

纤维 (Python `asyncio`走进节日,烂`tokio`) 合作地实现I/O. 同样的10,000通话舒适地适应过程.在LLM代理规模上,async不是一个优化,而是架构.

唯一的例外: CPU 相关后处理 (嵌入,代币化技巧) 仍然需要线程或进程.将您的 I/O 层与 CPU 层分开.

### 贝迪的反点

"扩展代理软件" (Ashpreet Bedi, 2026) 认为大多数团队在测量负载之前过度工程.

- 快速API+后期.
- 每次代理运行都是一行;状态在现场更新,同时保持乐观.
- 通过 `pg_notify`或是一个简单的菜工人.
- 申请代码中重新尝试.

对于可管理任务的负载量低于100个同时运行的代理,通常只需要这么做.

规则:当你遇到一个具体的问题, 简单的建筑无法解决时, 采用持久的执行框架.

### 精确的语义

对于付费代理运行,你需要"一次有效" (至少一次交付 +无权消费者).

- **Dedup key per run.**加入每次副作用电话.
- **Outbox pattern.**后果首先写到一个表,然后一个单独的过程执行它们.
- **Compensating transactions.**如果副作用成功,但其追踪写失败,

法律法师税仅仅是法律法师调用速度缓慢;其他的一切都是标准分布式系统.

### 彩虹部署

普奇的多代理研究系统使用"彩虹部署":代理运行时间的多个版本同时运行,因此长期运行的代理人不需要在每个代码部署中被杀害.卡纳里新版本在一片流量上;当他们的代理人完成时退休旧版本.

这对于长期运行的状态系统是标准的; 2026年适应是代理人可以活多小时,所以部署周期必须适应.

### 标准生产检查清单

- 持久状态 (检查点,快照或输出箱+可播放日志).
- 无效的副作用.
- 对于LLM电话来说,Async I/O层.
- 至少一次送货,带着.
- 适用于工作负载的彩虹/加拿大鱼部署.
- 观察性:每位代理的痕迹,超级审计,重试计数.

## 动手构建
```figure
sw-checkpoint-replay
```

## 建立它

`code/main.py`执行:

- `CheckpointStore` SQLite支持的检查点日志,有线索ID键.每个超级步骤添加了一行.
- `run_with_checkpoint(agent, thread_id)`模拟一次中跑事故;第二名工人从最后一个检查点恢复.
- `AgentQueue`每代理                                                                                                                                                                                                                                                             
- `demo_async_vs_threads()`通过无线和线程运行500个同时模拟的LLM调用;报告墙钟和峰值内存 (近似).

运行:

```
python3 code/main.py
```

预期输出:检查点恢复在模拟崩后成功;async版本在<1s内处理500次同时调用;线程版本需要几秒钟,每次同时使用数量更高的内存.

## 用它使用方法

`outputs/skill-scaling-advisor.md`建议使用耐用执行选项:FastAPI + Postgres,LangGraph运行时间,时间或定制.按负载,状态保留需求和部署频率进行校准.

## 发射上线

制产品硬化:

- **Start simple (Bedi's rule).**快API+后期,直到测量失败.
- **Instrument everything before optimizing.**运行延迟历史图,步骤时间,重复试数,失败分类.
- **Outbox pattern for side effects.**尤其是支付和外部API通话.
- **Rainbow deploys.**在部署时,不要杀死飞行中的特工.
- **Adopt durable-execution engines (Temporal / LangGraph / Restate) when**您遇到特定问题:一个小时的循环等待,跨地区协调,复杂的重试/补偿政策.
- **Async for the I/O layer.**仅用于处理后处理.

## 练习题

1. 跑步`code/main.py`检查点恢复工作;测量异步与线程同步差异.
2. 实施一个**outbox**每个工具调用首先写到输出框,然后执行一个单独的 goroutine/任务.通过两次运行工具调用来验证无效性.
3. 模拟一个**rainbow deploy**:两个同时运行版本;将新线程_ID的半个线程向每一个;确认旧版本的飞行线程没有被打断.
4. 阅读LangGraph的运行时间文件 (下面链接).确定运行时间的哪些功能在手动滚动的FastAPI + Postgres版本中需要最长时间复制.这是否可以采取理由,或者您可以推迟?
5. 阅读MegaAgent (arXiv:2408.09955) 第三节. 两层协调 (组内 + 组间管理员聊天) 是明确的. 绘制一幅图,说明你如何将此映射到两个队列家庭的消息队列中.

## 关键词 关键词

| Term | What people say | What it actually means |
|------|----------------|------------------------|
| Durable execution / 持久执行 | "Persist the program state" / "持久化程序状态" | Engine writes state after each super-step; crash recovery is deterministic. / 引擎在每个超步后写入状态；崩溃恢复是确定性的。 |
| Super-step / 超步 | "Transactional boundary" / "事务边界" | Unit of work between checkpoints. LangGraph term. / 检查点之间的工作单元。LangGraph 术语。 |
| thread_id / 线程 ID | "Agent run identifier" / "Agent 运行标识符" | Key that binds checkpoints and resume logic. / 绑定检查点和恢复逻辑的键。 |
| Idempotency / 幂等性 | "Safe to retry" / "安全重试" | Repeating a side effect produces the same result as one attempt. / 重复副作用产生与一次尝试相同的结果。 |
| Outbox pattern / 发件箱模式 | "Decouple side effects" / "解耦副作用" | Write intent to a table; a separate executor performs and marks done. / 将意图写入表；单独的执行器执行并标记完成。 |
| At-least-once delivery / 至少一次投递 | "Possible duplicates" / "可能重复" | Message queue semantics; dedup key makes consumer effective-once. / 消息队列语义；去重键使消费者有效一次。 |
| Rainbow deploy / 彩虹部署 | "Overlapping versions" / "重叠版本" | Multiple runtime versions concurrent during long-running workloads. / 多个运行时版本在长时间工作负载期间并发。 |
| Async fiber / 异步纤程 | "Cooperative yielding" / "协作让步" | User-mode concurrency; cheap compared to threads for I/O-bound loads. / 用户态并发；I/O 密集负载下比线程廉价。 |
| Checkpoint / 检查点 | "State snapshot" / "状态快照" | Serialized state at a super-step boundary; key for resume. / 超步边界处的序列化状态；恢复的关键。 |

## 继续阅读 继续阅读

- [LangChain — The runtime behind production deep agents](https://www.langchain.com/conceptual-guides/runtime-behind-production-deep-agents) 兰格拉夫运行时间设计
- [MegaAgent](https://arxiv.org/abs/2408.09955)每代理生产者-消费者队列;在数千个同时代理的两层协调
- [Matrix](https://arxiv.org/abs/2511.21686) 分离式框架,配合基层是信息队列
- [Temporal docs](https://docs.temporal.io/) 适用于耐用执行的参考工作流动引擎
- [Anthropic — Multi-agent research system](https://www.anthropic.com/engineering/multi-agent-research-system)生产课程,包括彩虹部署
