# Parallel / Swarm / Networked Architectures | 并行 群体

> Contrast with supervisor: no central decider. Agents read a shared event bus, pick up work asynchronously, write results back. LangGraph explicitly supports "Swarm Architecture" for decentralized, dynamic environments. Matrix (arXiv:2511.21686) represents both control and data flow as serialized messages passed through distributed queues to eliminate the orchestrator bottleneck. The tradeoff is explicit: determinism and traceability for scalability. Swarm fits tasks with many independent sub-problems; it does not fit tasks that need a single coherent plan.

> **【中文解读】** 本节介绍了并行群体网络——大量 Agent 通过共享状态并行工作的组织模式。

> **【拓展：parallel swarm networks→具体应用】** 并行群体网络让大量 Agent 同时处理子任务，然后聚合结果。适合可并行化的任务（如多文件编辑、多数据源查询）。关键挑战是结果聚合——如何合并可能冲突的部分结果。Map-Reduce 是常见的聚合模式。2026 年的实践表明，5-10 个并行 Agent 是最优范围。


**Type:** Learn | **类型:** 学习
**Languages:** Python | **语言:** Python
**Prerequisites:** Phase 16 · 05 (Supervisor Pattern), Phase 16 · 04 (Primitive Model) | **前置知识:** Phase 16 · 05 (Supervisor Pattern), Phase 16 · 04 (Primitive Model)
**Time:** ~75 minutes | **时间:** ~75 分钟

> 🔗 **【前置】** 学本节前请先掌握：Phase 16·04-05（原语+Supervisor）。本节是 Supervisor 的反面——无中心协调器的群体网络。
> 💡 **【类比】** Swarm vs Supervisor = "去中心化" vs "层级制"。Supervisor = 公司（CEO 调度）；Swarm = 开源社区（每人看 issue 板自己领取）。Swarm 适合独立子任务（多文件编辑、多源查询），不适合需要单一计划的任务。5-10 个 Agent 是最优——太多会聚合时打架。

## Problem | 问题引入

Supervisor scales to a few workers. What about hundreds? The supervisor itself becomes the bottleneck: every decision about who does what funnels through one agent. One slow plan step stalls the whole system.

> 监督者可以扩展到几个工作器。那几百个呢？监督者本身成为瓶颈：每个关于谁做什么的决定都通过一个 Agent。一个缓慢的计划步骤会停滞整个系统。

The supervisor is itself an LLM call. At hundreds of workers, the supervisor makes hundreds of LLM calls just to dispatch. Each call is seconds; the dispatch overhead dominates. Swarm removes the supervisor entirely.

> 监督者本身是 LLM 调用。在数百个工作器时，监督者仅调度就进行数百次 LLM 调用。每次调用几秒钟；调度开销占主导。群体完全移除监督者。

Swarm architectures flip the design. Instead of a central planner dispatching work, workers pick work off a shared queue. The "coordination" is baked into the event bus semantics. No orchestrator; the system scales until the queue does.

> 群体架构翻转了设计。不是中央规划者分发工作，而是工作器从共享队列中获取工作。"协调"被嵌入事件总线语义中。没有编排器；系统扩展直到队列成为瓶颈。

The architectural inversion is significant: the bottleneck moves from "the LLM that decides what to do" to "the message broker that routes work." LLMs are slow and expensive; message brokers are fast and cheap. Swarm trades LLM bottleneck for broker bottleneck — almost always a win.

> 架构反转重大：瓶颈从"决定做什么的 LLM"转移到"路由工作的消息代理"。LLM 慢且昂贵；消息代理快且便宜。群体用代理瓶颈换 LLM 瓶颈——几乎总是赢。

## Concept | 核心概念

### The shape

```
                ┌──── shared queue ────┐
                │                      │
       ┌────────┼────────┐  ◄──────┬───┘
       ▼        ▼        ▼         │
     Worker  Worker  Worker   Worker
      A       B       C        D
       │        │        │         │
       └────────┴────────┴─────────┘
                 │
                 ▼
            results pool
```

No orchestrator. Each worker repeats: pull a task, process, write result (and optionally enqueue follow-ups).

> 没有编排器。每个工作器重复：拉取任务、处理、写入结果（并可选地入队后续任务）。

The lack of a central decider is the defining feature. Workers do not wait for instructions; they self-organize around the queue. This is the actor model applied to LLMs — each worker is an independent actor reacting to messages.

> 缺乏中央决策者是定义特征。工作器不等待指令；它们围绕队列自组织。这是应用于 LLM 的 actor 模型——每个工作器是响应消息的独立 actor。

### When swarm fits

- **Many independent tasks.** Scraping, transforming, classifying. Tasks do not depend on each other.
  中文翻译：**许多独立任务。** 抓取、转换、分类。任务之间不相互依赖。
- **Variable-duration work.** If some tasks take 100ms and others take 10s, a swarm balances load automatically — fast workers pull next jobs. A supervisor has to anticipate duration.
  中文翻译：**可变持续时间的工作。** 如果某些任务需要 100ms 而其他需要 10s，群体会自动平衡负载——快速工作器拉取下一个任务。监督者必须预估持续时间。
- **Throughput over determinism.** You care about total completion time, not strict ordering.
  中文翻译：**吞吐量优先于确定性。** 你关心总完成时间，而不是严格排序。

### When swarm fails

- **Ordered workflows.** If step 3 needs step 2's output, a swarm risks step 3 firing before step 2 is done.
  中文翻译：**有序工作流。** 如果步骤 3 需要步骤 2 的输出，群体有步骤 3 在步骤 2 完成之前触发的风险。
- **Global-plan tasks.** Complex research questions benefit from a planner. A swarm of researchers produces independent facts, not a coherent report.
  中文翻译：**全局计划任务。** 复杂的研究问题从规划者中受益。一群研究者产生独立的事实，而不是一份连贯的报告。
- **Debugging.** With no central log and asynchronous work, reproducing a bug is expensive.
  中文翻译：**调试。** 没有中央日志和异步工作，复现 bug 的代价很高。

### Matrix (arXiv:2511.21686)

Matrix is the 2025 paper that takes swarm to its natural conclusion: both control flow and data flow are serialized messages on distributed queues. No central coordinator. Fault tolerance comes from message durability. Scalability is the message broker's problem, not the system's.

> Matrix 是 2025 年将群体推向自然结论的论文：控制流和数据流都是分布式队列上的序列化消息。没有中央协调器。容错来自消息持久性。可扩展性是消息代理的问题，而不是系统的。

By making the broker (Kafka, Redis Streams, NATS) the scaling bottleneck, Matrix sidesteps the LLM-as-orchestrator bottleneck entirely. The system can scale to thousands of agents if the broker can; the LLMs are pure workers, never coordinators.

> 通过使代理（Kafka、Redis Streams、NATS）成为扩展瓶颈，Matrix 完全避开了 LLM 作为编排器的瓶颈。如果代理可以，系统可以扩展到数千个 Agent；LLM 是纯工作器，永远不是协调器。

Contribution: a programming model where multi-agent coordination is "what message topic does this agent subscribe to?" rather than "which agent does the supervisor pick next?" This makes the system look like a pub/sub event mesh.

> 贡献：一个编程模型，多 Agent 协调是"这个 Agent 订阅什么消息主题？"而不是"监督者下一个选择哪个 Agent？"这使系统看起来像一个发布/订阅事件网格。

### LangGraph's Swarm Architecture

LangGraph 2025 docs explicitly describe "Swarm Architecture" as one of the multi-agent patterns: agents are nodes, but edges form a directed graph with cycles and any node can be activated from the pool. A worker picks from available work by condition, not by supervisor assignment.

> LangGraph 2025 文档明确将"群体架构"描述为多 Agent 模式之一：Agent 是节点，但边形成有环的有向图，任何节点都可以从池中激活。工作器按条件从可用工作中选择，而不是按监督者分配。

LangGraph's contribution: the same graph-based mental model now supports swarm dynamics. Nodes that activated based on conditions rather than fixed edges. This bridges the static-graph and pure-swarm worlds.

> LangGraph 的贡献：相同的基于图的心智模型现在支持群体动态。基于条件而非固定边激活的节点。这桥接了静态图和纯群体世界。

### Failure mode: starvation and hot-spotting

If all workers pull the fastest-available task, long-running tasks never get picked until they are the only ones left. Classic queue starvation.

> 如果所有工作器都拉取最快可用的任务，长时间运行的任务永远不会被选中，直到它们成为唯一剩下的。经典的队列饥饿。

Starvation is the swarm's signature failure mode. Without explicit aging (priority increases with wait time) or specialized long-task workers, a 10-second task waits forever behind a stream of 100ms tasks. Production swarms must engineer around this.

> 饥饿是群体的标志性失败模式。没有显式老化（优先级随等待时间增加）或专业化长任务工作器，10 秒任务永远在 100ms 任务流后等待。生产群体必须围绕此工程设计。

Mitigations:
- Priority queues with explicit aging (increase priority with wait time).
  中文翻译：带显式老化的优先队列（随等待时间增加优先级）。
- Worker specialization: some workers only take "long" tasks.
  中文翻译：工作器专业化：一些工作器只接受"长"任务。
- Back-pressure: limit how many fast tasks enter the queue.
  中文翻译：背压：限制多少快速任务进入队列。

### The content-based routing link

Swarm pairs naturally with content-based routing (Lesson 22). Instead of a generic queue, have one queue per message type. Specialist workers subscribe only to their type. This is the basis for message-bus architectures that scale to thousands of agents.

> 群体与基于内容的路由（Lesson 22）自然配对。不是通用队列，而是每种消息类型一个队列。专业化工作器只订阅其类型。这是扩展到数千个 Agent 的消息总线架构的基础。

Content-based routing plus swarm gives you the pub/sub event mesh: a substrate where any agent can publish any message type, and only interested agents receive it. This is the foundation of Matrix, CA-MCP, and most 2026 production multi-agent systems.

> 基于内容的路由加群体给你发布/订阅事件网格：一个任何 Agent 可以发布任何消息类型且只有感兴趣的 Agent 接收它的底层。这是 Matrix、CA-MCP 和大多数 2026 年生产多 Agent 系统的基础。

## Build It | 动手实现

`code/main.py` implements a swarm of 4 worker threads pulling from a shared `queue.Queue`. Tasks have variable durations (some fast, some slow). The demo contrasts:

> `code/main.py` 实现了 4 个从共享 `queue.Queue` 拉取的工作线程。任务有可变持续时间（一些快，一些慢）。演示对比：

The three-way comparison is the educational value: same tasks, same workers, only the dispatch strategy changes. Sequential = slow. Fixed = wasteful. Swarm = optimal. The wall-clock numbers make the case empirically.

> 三方对比是教育价值：相同任务、相同工作器，只有调度策略变化。顺序 = 慢。固定 = 浪费。群体 = 最优。挂钟时间数字经验性地证明了案例。

- **Sequential baseline:** one worker processes all tasks serially.
  中文翻译：**顺序基线：** 一个工作器串行处理所有任务。
- **Fixed assignment:** each task pre-assigned to a specific worker (supervisor-style).
  中文翻译：**固定分配：** 每个任务预先分配给特定工作器（监督者风格）。
- **Swarm:** workers pull from a shared queue.
  中文翻译：**群体：** 工作器从共享队列拉取。

Swarm balances load automatically; fixed assignment leaves fast workers idle when their assigned task is slow.

> 群体自动平衡负载；固定分配在分配的任务慢时让快速工作器空闲。

The "uneven but optimal" distribution is the swarm signature. A worker that finishes its task in 50ms pulls three more while a worker on a 2-second task is still on its first. The total wall-clock is bounded by the slowest single task, not the sum.

> "不均匀但最优"分布是群体特征。50ms 完成任务的工作器在 2 秒任务的工作器仍在第一个任务上时拉取三个更多任务。总挂钟时间受最慢单任务限制，而不是总和。

Output shows per-worker task counts (swarm distributes unevenly but optimally) and wall-clock times.

> 输出显示每个工作器的任务计数（群体分布不均匀但最优）和挂钟时间。

## Use It | 用框架实现

`outputs/skill-swarm-fit.md` evaluates whether a task should use swarm vs supervisor. Inputs: task independence, duration variance, ordering requirements, debuggability needs.

> `outputs/skill-swarm-fit.md` 评估任务应该使用群体还是监督者。输入：任务独立性、持续时间方差、排序要求、可调试性需求。

## Ship It | 产出物

Checklist:

> 检查清单：

- **Priority queue with aging.** Prevent long-task starvation.
  中文翻译：**带老化的优先队列。** 防止长任务饥饿。
- **Worker idempotency.** A task may be pulled more than once if a worker crashes mid-run. Workers must be idempotent.
  中文翻译：**工作器幂等性。** 如果工作器中途崩溃，任务可能被拉取多次。工作器必须是幂等的。
- **Durable queue.** Use Kafka, Redis Streams, or a database-backed queue for production. `queue.Queue` is in-memory only.
  中文翻译：**持久队列。** 生产环境使用 Kafka、Redis Streams 或数据库支持的队列。`queue.Queue` 仅在内存中。
- **Observability per task.** Every task has a trace ID; every worker logs start/end with it.
  中文翻译：**每个任务的可观测性。** 每个任务有跟踪 ID；每个工作器用它记录开始/结束。
- **Back-pressure.** If the queue grows faster than workers drain it, slow the producer.
  中文翻译：**背压。** 如果队列增长速度快于工作器排空速度，减慢生产者。

## Exercises | 练习题

1. Run `code/main.py`. How much faster is swarm than sequential on the variable-duration workload? How much faster than fixed assignment?
   中文翻译：运行 `code/main.py`。群体在可变持续时间工作负载上比顺序快多少？比固定分配快多少？
2. Add a priority queue variant (use `queue.PriorityQueue`). Assign priority by task "importance" field. Observe whether low-priority tasks ever starve under continuous load.
   中文翻译：添加优先队列变体（使用 `queue.PriorityQueue`）。按任务"重要性"字段分配优先级。观察低优先级任务是否在持续负载下饥饿。
3. Implement a hot-spot detector: log when any worker processes 3x more tasks than the slowest worker. What does that indicate about task-duration distribution?
   中文翻译：实现热点检测器：当任何工作器处理比最慢工作器多 3 倍的任务时记录。这表明任务持续时间分布有什么特点？
4. Read the Matrix paper (arXiv:2511.21686) abstract and Section 3. Identify one specific tradeoff Matrix accepts (scalability gain) and one it gives up (traceability, determinism).
   中文翻译：阅读 Matrix 论文（arXiv:2511.21686）摘要和第 3 节。识别 Matrix 接受的一个具体权衡（可扩展性收益）和一个放弃的（可追溯性、确定性）。
5. Convert the swarm demo to use a `queue.Queue` of (task_type, payload) tuples, with workers subscribing only to specific types. What routing rules make sense when tasks are heterogeneous?
   中文翻译：将群体演示转换为使用 (task_type, payload) 元组的 `queue.Queue`，工作器只订阅特定类型。当任务异构时什么路由规则合理？

## Key Terms | 术语速查表

| Term | What people say | What it actually means |
|------|----------------|------------------------|
| Swarm architecture / 群体架构 | "Decentralized agents" / "去中心化 Agent" | Workers pull from shared queue; no central orchestrator. / 工作器从共享队列拉取；没有中央编排器。 |
| Event bus / 事件总线 | "Agents subscribe to topics" / "Agent 订阅主题" | Message broker that routes tasks to workers by type or content. / 按类型或内容将任务路由到工作器的消息代理。 |
| Starvation / 饥饿 | "Task never runs" / "任务永远不运行" | Low-priority task never gets picked because higher-priority work arrives continuously. / 低优先级任务因为高优先级工作持续到达而永远不被选中。 |
| Hot-spotting / 热点 | "One worker drowns" / "一个工作器淹没" | Load imbalance where one worker gets most tasks. / 一个工作器获得大部分任务的负载不均衡。 |
| Back-pressure / 背压 | "Slow down the producer" / "减慢生产者" | Mechanism that signals upstream to stop producing when the queue fills up. / 当队列填满时向上游发出停止生产的信号机制。 |
| Idempotent worker / 幂等工作器 | "Safe to re-run" / "安全重新运行" | A task processed twice produces the same result. Required because workers may crash mid-run. / 任务处理两次产生相同结果。因为工作器可能中途崩溃所以需要。 |
| Durable queue / 持久队列 | "Survives crashes" / "崩溃后存活" | Queue backed by disk or replicated storage; tasks are not lost when a worker crashes. / 由磁盘或复制存储支持的队列；工作器崩溃时任务不丢失。 |
| Matrix framework / Matrix 框架 | "Full message-passing swarm" / "全消息传递群体" | Both data and control flow are serialized messages on distributed queues. / 数据流和控制流都是分布式队列上的序列化消息。 |

## Further Reading | 延伸阅读

- [LangGraph workflows and agents — Swarm Architecture](https://docs.langchain.com/oss/python/langgraph/workflows-agents) — explicit swarm support
  中文翻译：LangGraph 工作流和 Agent — 群体架构 — 明确的群体支持
- [Matrix — A Decentralized Framework for Multi-Agent Systems](https://arxiv.org/abs/2511.21686) — full message-passing swarm
  中文翻译：Matrix — 多 Agent 系统的去中心化框架 — 全消息传递群体
- [Anthropic engineering — why supervisor not swarm in Research](https://www.anthropic.com/engineering/multi-agent-research-system) — why a specific production system explicitly chose supervisor over swarm
  中文翻译：Anthropic 工程 — 为什么研究系统选择监督者而非群体 — 为什么一个特定生产系统明确选择监督者而非群体
- [AutoGen v0.4 actor-model docs](https://microsoft.github.io/autogen/stable/) — the event-driven actor rewrite, closer to swarm than v0.2's GroupChat
  中文翻译：AutoGen v0.4 actor 模型文档 — 事件驱动 actor 重写，比 v0.2 的 GroupChat 更接近群体
