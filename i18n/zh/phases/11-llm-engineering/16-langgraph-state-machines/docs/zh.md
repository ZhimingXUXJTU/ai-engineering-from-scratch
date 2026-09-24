# 长度图  代理的国家机器
# 代理国机器 图表,节点,检查站

> 通过手写的 ReAct 循环是`while True`作为一个明确的图表,写的循环是你可以检查点,打断,分支,时间旅行. 代理没有改变. 环绕它有.

> **【中文解读】**写作的反应循环就是一个`while True`△使用LangGraph写的 ReAct循环是一个图可以检查点保存,中断,分支,时间旅行――代理没有变化,但周围的框架变化――

> **【拓展：LangGraph→Agent工程】**现已成熟的代理编排框架,将代理执行建模为状态图 (StateGraph),支持人机协作、分支逻辑和持久化状态.

>  **【前置】**学本节前请先掌握:(1) 阶段11·09(函数调用);(2) 阶段14·01(代理循环) 理解 ReAct 循环;(3) 状态机概念(有限状态机 FSM、节点、边) ――本节会用 `langgraph`,我知道.`langchain-core`,我知道.

**Type:** Build | **类型:** 构建
**Languages:** Python | **语言:** Python
**Prerequisites:** Phase 11 · 09 (Function Calling), Phase 11 · 14 (Model Context Protocol) | **前置知识:** Phase 11 · 09 (函数调用)、14 (模型上下文协议)
**Time:** ~75 minutes | **时间:** ~75 分钟

## 问题 问题引入

运输一个调用函数的代理.它工作了三次,然后发生了一些问题:模型尝试一个返回500的工具,用户在任务中改变了想法,或者代理决定退还一个订单,没有人签署.`while True:`没有子. 你不能暂停它,你不能转它,你不能分分成"如果模型选择了另一种工具".

> 你发布了一个调用代理函数. 它工作了三轮,然后出现问题:模型尝试了返回500个工具,用户在改变想法,或者代理决定退款,没有人工签名.`while True:`循环没有子. 你不能暂停它,倒回它,或分支到"如果模型选择了另一个工具,

接下来的步骤是显而易见的. 代理已经是一个状态机 系统提示加上消息历史加上等待工具调用加上下一步行动. 让状态机明确:节点为"模型认为","工具运行","人批准",和边缘为它们之间的条件过渡. 一旦图表明确,该带将获得四件事免费:检查点 (节省步骤之间的状态),中断 (人类的暂停),流 (流代币和中间事件),以及时间旅行 (回返以前的状态并尝试不同的分支).

> 让状态机显而易见:节点代表"模型思考"",工具运行"",人工审批",边代表它们之间的条件转换.

兰格格拉夫是传输这种抽象的图书馆.它不是一个代理框架,在兰格链意义上 ("这里有一个代理执行者,好运").它是一个图表运行时间,具有一流状态,一流的持久性和一流的中断. 代理循环是你绘制的东西,而不是你手写的东西.
这种抽象的参考实现是LangGraph.它不是一个代理框架,在LangChain意义上 ("这里有一个代理执行者,好运").它是一个图表运行时间,具有一流状态,一流的持久性和一流的中断.代理循环是你绘制的东西,而不是你手写的东西.

> 兰格格拉夫是提供这种抽象的库――它不是兰格链的代理框架――它是一个具有平等的公民状态―― 一级公民持久化和一级公民中断的图运行时―― 代理循环是你绘制的,而不是手写的――


> **【中文解读】**根据任务类型选择不同工具) 人工审批) 高风险操作需要人工确认) 简单的长链链无法表达这些复杂逻辑――

>  **【类比】**手写 ReAct循环像在沙上画流程图画完没了,潮水一冲就消失了.

> ️ **【易错点】**长度图的3个坑:**状态 schema 太松散**用`dict`当状态 没类型约束,运行时关键 拼错发现不了;用 `TypedDict`或皮达因特模型 定义状态──(2) **条件边写得太复杂**一个边缘 函数里 if/else 嵌套 5 层,调试地狱;拆成多个简单边缘 函数,每个返回单一节点名――(3) **checkpoint 用 SQLite 不持久化**重启服务失败状态;生产用后台或重复做检查点──


## 概念的核心概念

> **【中文解读】**长格拉夫将LLM代理 建模为状态机 (State Machine):定义状态节点 (如检索,生成,验证) 和转换边 (如转换边) 条件分支) ⋅相比简单的链式调用,状态机支持循环,条件分支,人工审批等复杂控制流――

> **【拓展：LangGraph 与 Agent 编排】**长度图是团队推出的代理编排框架,支持:多代理协作、人工干预 (Human-in-the-loop) 、持久化状态、时间旅行调试――与机组人员AI (角色扮演代理) 和AutoGen (多代理对话) 相比,长度图更适合需要精确控制流的复杂业务场景――


![LangGraph StateGraph: nodes, edges, and the checkpointer](../assets/langgraph-stategraph.svg)

`StateGraph`有三个东西.

> `StateGraph`有三件事.

1. **State.**输入式命令 (TypedDict或Pydantic模型) 通过图表流动.每个节点都收到完整状态并返回部分更新,LangGraph将其通过每个字段的 *reducer* 合并`operator.add`对于应该积累的列表,默认上重写.
   **状态。**流过图的类型化字典──每个节点收到完整状态并返回部分更新──
2. **Nodes.** Python 函数`state -> partial_state`每一步都是一个分别的步骤: "调用模型", "运行工具", "总结".
   **节点。**字符串函数`state -> partial_state`每个都是一个分离步骤.
3. **Edges.**节点之间的过渡.静态边缘将移动到一个地方. 条件边缘将接收路由器函数`state -> next_node_name`图表可以分为模型输出.
   **边。**节点之间的转换――静态边去一个地方――条件边接受路由函数以在模型输出上分支――

编译将拓链接,附加一个检查点 (可选但对于生产至关重要),并返回一个可运行的.您使用一个初始状态和一个`thread_id`每一步执行都会有一个关键的检查点`(thread_id, checkpoint_id)`现在,我们要去.

> 你编译图――编译绑定拓、附加检查点器并返回可运行对象――你使用初始状态和`thread_id`调用它. 执行的每一步都会持续一个检查点.

### 它们是四大超级大国.

**Checkpointing.**每个节点过渡都会将新状态写入一个存储器 (在内存中进行测试,Postgres/Redis/SQLite为 prod).再重复,再用相同的方式调用图表.`thread_id`图表从停留的地方恢复.

> **检查点。**每个节点转换将新状态写入存储库.`thread_id`恢复的图片.

**Interrupts.**标记一个节点`interrupt_before=["human_review"]`您的API会以"等待批准"回复用户. 随后请求相同的`thread_id`随着`Command(resume=...)`恢复执行.

> **中断。**用`interrupt_before`标记一个节点,执行在该节点运行前停止――状态被持久化――后续请求可恢复执行――

**Streaming.** `graph.stream(state, mode="updates")`随着这些事件,`mode="messages"`通过模特节点中流动LLM代币. `mode="values"`您可以选择在用户界面中出现什么.

> **流式输出。** `graph.stream`按发生顺序产出状态增量──你选择在UI中显示什么──

**Time-travel.** `graph.get_state_history(thread_id)`返回检查站的全部日志.`checkpoint_id`为了`graph.invoke`对于调试 ("如果模型选择了工具B?") 和重播生产痕迹的回归测试来说,

> **时间旅行。**返回完整的检查点日志――传入任何先前的`checkpoint_id`现在,你从那个分叉点.

### 减少者是个问题

每个状态字段都有减小器.大多数默认值都很好一个新的值覆盖了旧值.但消息列表需要`operator.add`通过减速器将其更新合并.如果两个节点都更新`messages`你忘了了这个`Annotated[list, add_messages]`减速器是图书馆唯一的微妙东西;把它做得好,剩下的都是编曲.

> 每个状态字段都有一个减小器.`operator.add`减少器是库中唯一微妙的东西; 搞对,剩下的自然组合.

### 通过4个节点的 ReAct图

生产 ReAct 代理是四个节点和两个边缘:

> 一个生产级反应剂是四节点和两边:

1. `agent`将当前消息历史记录传递给LLM. 返回助理消息 (可能包含工具_调用).
2. `tools`执行最后一个助理消息中的任何工具_调用,将工具结果添加为工具消息.
3. 一个条件边缘`agent`航线到`tools`如果最后一个消息有工具_调用,否则`END`现在,我们要去.
4. 一个静态边缘`tools`回到`agent`现在,我们要去.

您可以在约40行代码中获得全 ReAct循环 (思维 → 行动 → 观察 → 思考 → ...) 通过检查点,中断和流.

> 您得到了完整的 ReAct 循环, 思考 → 行动 → 观察 → 思考 → ...),带检查点、中断和流式输出,大约40 行代码──

### 状态图与发送 (预测)

`Send(node_name, state)`让节点发送平行子图. 举个例子:代理决定同时查询三个检索器. 每个`Send`通过状态减小器,它们的输出融合. 这就是LangGraph在没有线程原始的情况下表达了乐队员-工作者模式.

> `Send(node_name, state)`让一个节点分派并行子图.`Send`生成目标节点的并行执行;它们的输出通过状态减小器合并.

### 字幕

编译图可以是另一个图中的节点. 外面图看到单个节点;内部图有自己的状态和检查点.这就是团队构建监督员工代理的方式:监督员工图将用户意图导向每个域名的员工子图.

> 编译后图可以是另一个图中的节点. 外层图看到一个单一节点;内层图有自己的状态和检查点.

## 建立它,实现它.
```figure
l5-state-graph-ledger
```

## 建立它

### 步骤1:状态和节点

> 步骤1:状态和节点

```python
from typing import Annotated, TypedDict
from langchain_core.messages import AnyMessage, HumanMessage, AIMessage
from langgraph.graph import StateGraph, END
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode
from langgraph.checkpoint.memory import MemorySaver

class State(TypedDict):
    messages: Annotated[list[AnyMessage], add_messages]

def agent_node(state: State) -> dict:
    response = llm.invoke(state["messages"])
    return {"messages": [response]}

def should_continue(state: State) -> str:
    last = state["messages"][-1]
    return "tools" if getattr(last, "tool_calls", None) else END

tool_node = ToolNode(tools=[search_web, read_file])

graph = StateGraph(State)
graph.add_node("agent", agent_node)
graph.add_node("tools", tool_node)
graph.set_entry_point("agent")
graph.add_conditional_edges("agent", should_continue, {"tools": "tools", END: END})
graph.add_edge("tools", "agent")

app = graph.compile(checkpointer=MemorySaver())
```

`add_messages`错误的原因是,它是最常见的LangGraph错误.

> `add_messages`让消息列表积累而不是覆盖的减小器.

### 步骤2:用线程运行

> 步骤2:用线程运行.

```python
config = {"configurable": {"thread_id": "user-42"}}
for event in app.stream(
    {"messages": [HumanMessage("find the Anthropic headquarters address")]},
    config,
    stream_mode="updates",
):
    print(event)
```

每次更新都是一个命令`{node_name: state_delta}`你的前端可以向用户界面传输这些,以便用户看到"代理正在考虑...打电话搜索_网...得到结果...回复".

> 每次更新都是`{node_name: state_delta}`字典──前端可流式传到UI,让用户看到"代理思考中...调用搜索_网...得到结果...回答中"──

### 步骤3:添加一个人-在循环中中断

标记一个节点,以便执行停止运行之前.

> 步骤3:添加人机协作中断――标记节点使执行在运行前暂停――

```python
app = graph.compile(
    checkpointer=MemorySaver(),
    interrupt_before=["tools"],  # pause before every tool call
)

state = app.invoke({"messages": [HumanMessage("delete the production database")]}, config)
# state["__interrupt__"] is set. Inspect proposed tool calls.
# If approved:
from langgraph.types import Command
app.invoke(Command(resume=True), config)
# If denied: write a rejection message and resume
app.update_state(config, {"messages": [AIMessage("Blocked by human reviewer.")]})
```

状态,检查点和线程都在中断期间持续存在. 除了执行时,没有任何东西被记住.

> 状态,检查点和线程在中断期间全部持久化――除了执行期间,没有任何东西在内存中――

### 步骤4:调试时间旅行

> 步骤4:调试使用时间旅行.

```python
history = list(app.get_state_history(config))
for snapshot in history:
    print(snapshot.values["messages"][-1].content[:80], snapshot.config)

# Fork from a prior checkpoint
target = history[3].config  # three steps back
for event in app.stream(None, target, stream_mode="values"):
    pass  # replay from that point forward
```

通过`None`通过一个值,在恢复之前将其添加到该点状态的更新中. 这就是你在没有重新运行整个对话的情况下重复一个坏代理运行的方式.

> 传入`None`作为输入从给定的检查点重放;传入值则在恢复前将其作为更新添加到该检查点的状态――这就是如何在不重新运行整个对话的情况下复现一个错误的代理运行――

### 步骤5:换取检查点进行生产

> 步骤5:生产环境替换检查点器

```python
from langgraph.checkpoint.postgres import PostgresSaver

with PostgresSaver.from_conn_string("postgresql://...") as checkpointer:
    checkpointer.setup()
    app = graph.compile(checkpointer=checkpointer)
```

石,雷迪斯和后生已经出货了.`MemorySaver`任何持续在重启过程中都需要真正的商店.

> 已提供了SQLite、Redis 和 Postgres`MemorySaver`任何需要重启的东西都需要真正的存储.

## 技能

> 你把代理作为图形,而不是作为图形.`while True`子,子.
> 你把代理构建为图,而不是`while True`循环

在你拿到兰格拉夫之前,做一个60秒的设计:

> 在使用LangGraph之前,做一个60秒的设计:

1. **Name the nodes.**任何单独的决定或副作用都是节点. "代理认为", "工具运行", "评论员批准", "响应流".如果你不能列出它们,任务还没有代理形状.
   **命名节点。**每个分离决策或副作用动作都是一个节点.
2. **Declare the state.**单词单词,每一个单词单词单词单词单词单词单词单词单词单词单词单词单词单词单词单词单词单词单词单词单词单词单词单词单词单词单词单词单词单词单词单词单词单词单词单词单词单词单词单词单词单词单词单词单词单词单词单词单词单词单词单词单词单词单词单词单词单词单词单词单词单词单词单词单词单词单词单词单词单词单词单词单词单词单词单词单词单词单词单词单词单词单词单词单词单词单词单词单词单词单词单词单词单词单词单词单词单词单词单词单词单词单词单词单词单词单词单词单词单词单词单词单词单词单词单词单词单词单词单词单词单词单词单词单词单词单词单词单词`messages`提升任务特定领域 (一个工作`plan`其他`budget`计数器`retrieved_docs`列表) 到最高水平.
   **声明状态。**最小的类型,每个列表字段都有减小器.
3. **Draw the edges.**只有下一步取决于模型输出.每个条件边缘需要一个具有命名分支的路由器函数.
   **画边。**除了下一步依赖模型输出,否则使用静态边缘.
4. **Choose a checkpointer up front.** `MemorySaver`对于测试, Postgres/Redis/SQLite. 没有一个 没有检查点意味着没有简历,没有中断,没有时间旅行.
   **提前选择检查点器。**测试用`MemorySaver`其他用 Postgres/Redis/SQLite──
5. **Decide interrupts before tools run, not after.**通过将边缘进入一个副作用节点,以便您可以在损害之前取消;验证将在模型边缘取消,
   **在工具运行之前决定中断，而不是之后。**
6. **Stream by default.** `mode="updates"`对于UI,`mode="messages"`对于模型节点内部的代币级流,`mode="values"`在评估期间,
   **默认使用流式输出。**

拒绝运送没有检查点的LangGraph代理.拒绝运送中断后的代理.拒绝运送一个`messages`没有字段`add_messages`作为其减小剂.

> 拒绝发布没有检查点器的 LangGraph 代理.拒绝发布后中断的代理.拒绝发布没有.`add_messages`作为减轻剂`messages`字段.

## 练习题

1. **Easy.**通过计算器工具和网页搜索工具实现上述四节点 ReAct 图.`list(app.get_state_history(config))`返回至少四个检查站,进行两轮对话.
   **简单。**实现上述四节点 ReAct图,验证检查点历史记录――
2. **Medium.**添加一个`planner`之前运行的节点`agent`编写一个结构化`plan: list[str]`现在,我在美国.`agent`测试中失败,如果`plan`检查点简历 (错误减小器) 上丢失.
   **中等。**添加一个在`agent`之前运行的`planner`节点,写入结构化计划到状态中.
3. **Hard.**建立一个监督图,该图将三个子图之间的路线 (`researcher`现在`writer`现在`reviewer`) 使用`Send`每个子图都有自己的状态和检查点.`interrupt_before=["writer"]`确认从前一个检查点的时间旅行只运行了叉子分支.
   **困难。**构建一个监督者 图,在三个子图之间使用 图`Send`路由而来.

## 关键词 快速查找表

| Term | What people say | What it actually means | 中文释义 |
|------|-----------------|-----------------------|---------|
| StateGraph | "The LangGraph graph" / "LangGraph 图" | The builder object you add nodes and edges to before compile. | StateGraph：编译前添加节点和边的构建器对象 |
| Reducer | "How the field merges" / "字段如何合并" | A function `(old, new) -> merged` applied when a node returns an update for that field; default is overwrite, `add_messages` appends. | Reducer：节点返回更新时应用的合并函数 |
| Thread | "A conversation ID" / "对话 ID" | A `thread_id` string that scopes all checkpoints for one session. | Thread：限定一个会话所有检查点的 thread_id 字符串 |
| Checkpoint | "A paused state" / "暂停的状态" | A persisted snapshot of the full graph state after a node transition, keyed on `(thread_id, checkpoint_id)`. | Checkpoint：节点转换后持久化的完整图状态快照 |
| Interrupt | "Pause for a human" / "暂停等人工" | `interrupt_before` / `interrupt_after` stop execution at a node boundary; resume with `Command(resume=...)`. | Interrupt：在节点边界停止执行，可恢复 |
| Time-travel | "Fork from a prior step" / "从先前步骤分叉" | `graph.invoke(None, config_with_old_checkpoint_id)` replays from that checkpoint forward. | Time-travel：从先前检查点重放 |
| Send | "Parallel subgraph dispatch" / "并行子图分派" | A constructor a node can return to spawn N parallel executions of a target node. | Send：节点返回以生成 N 个并行执行的构造器 |
| Subgraph | "A compiled graph as a node" / "编译后的图作为节点" | A compiled StateGraph used as a node in another graph; preserves its own state scope. | Subgraph：作为另一个图中节点使用的编译后 StateGraph |

## 继续阅读 继续阅读

- [LangGraph documentation](https://langchain-ai.github.io/langgraph/)对国家图表,减小器,检查点和中断的常规参考.
  长图 文档 状态图 减速器 检查点器和中断权力参考
- [LangGraph concepts: state, reducers, checkpointers](https://langchain-ai.github.io/langgraph/concepts/low_level/)本课中使用的心理模型,直接从源头.
  语法 概念:状态、降低器、检查点器──
- [LangGraph Persistence and Checkpoints](https://langchain-ai.github.io/langgraph/concepts/persistence/) Postgres/SQLite/Redis 商店,检查点名字空间和线程ID的细节.
  长度化和检查点详情
- [LangGraph Human-in-the-loop](https://langchain-ai.github.io/langgraph/concepts/human_in_the_loop/) `interrupt_before`现在`interrupt_after`现在`Command(resume=...)`它们是"化"的.
  拉格格拉夫 人机协作 断和恢复 模式――
- [Yao et al., "ReAct: Synergizing Reasoning and Acting in Language Models" (ICLR 2023)](https://arxiv.org/abs/2210.03629)每一个LangGraph代理所实施的模式;阅读它,以推理后果理性.
  每个LangGraph代理实现的反应模式.
- [Anthropic — Building effective agents (Dec 2024)](https://www.anthropic.com/research/building-effective-agents) 什么图形 (链,路由器,管弦工作者,评价者优化器) 首选,何时.
  关于选择哪种图形以及何时使用指南
- 阶段11 · 09 (函数调用) 每一个LangGraph代理节点重复使用工具调用原始.
  第11阶段 · 09(函数调用) 每个LangGraph 节点重用工具调用原语。
- 11 · 14阶段 (模式文本协议) 外部工具发现,将其插入到一个LangGraph`ToolNode`通过MCP适配器.
  第11阶段 · 14(MCP) 通过MCP 适配器插入LangGraph `ToolNode`发现的外部工具.
- 阶段11 · 17 (代理框架交易) 什么时候选择LangGraph而不是CrewAI,AutoGen或Agno.
  第11阶段 · 17(代理 框架对比) 何时选择 LangGraph──
