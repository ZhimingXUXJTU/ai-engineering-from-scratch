# 代理框架交易 兰格拉夫 VS 机组人AI VS 自动生成者vs阿格诺
# 代理框架交易 图表,角色和演员配乐

> 每个框架都销售相同的演示 (研究代理构建报告) 并隐藏相同的错误 (状态方案与编排层作战). 选择一个框架,其抽象与您的问题的形状相匹配; 其余的东西都是您写的两次粘合.

> **【中文解读】**每个框架都显示相同的示范,都隐藏相同的错误,状态方案与编排层冲突.

> **【拓展：框架选择→Agent工程实践】**机器人机器人机器人机器人机器人机器人机器人机器人机器人机器人机器人机器人机器人机器人机器人机器人机器人机器人机器人机器人机器人机器人机器人机器人机器人机器人机器人机器人机器人机器人机器人机器人机器人机器人机器人机器人机器人机器人机器人机器人机器人机器人机器人机器人机器人机器人机器人机器人机器人机器人机器人机器人机器人机器人机器人机器人机器人机器人机器人机器人机器人机器人机器人机器人机器人机器人机器人机器人机器人机器人机器人机器人机器人机器人机器人机器人机器人机器人机器人机器人机器人机器人机器人机器人机器人机器人机器人机器人机器人机器人机器人机器人机器人机器人机器人机器人机器人机器人机器人机器人机器人机器人机器人机器人机器人机器人机器人机器人机器人机器人机器人机器人机器人机器人机器人机器人机器人机器人机器人机器人机器人机器人机器人机器人机器人机器人机器人机器人机器人机器人机器人机器人机器人机器人机器人机器人机器人机器人机器人机器人机器人机器人机器人机器人机器人机器人机器人机器人机器人机器人机器人机器人机器人机器人机器人机器人机器人机器人机器人机器人机器人机器人机器人机器人机器人机器人机器人机器人机器人机器

>  **【前置】**节前请先掌握:阶段11·09(函数调用) 阶段11·16(长度图) 节是阶段11的最后一节,对比 4个主要框架 (长度图,机组,自动机,机器人,机器人,机器人,机器人,机器人,机器人,机器人,机器人) 的优劣――最好已经分别使用过其中的2个个.

**Type:** Learn | **类型:** 学习
**Languages:** Python | **语言:** Python
**Prerequisites:** Phase 11 · 09 (Function Calling), Phase 11 · 16 (LangGraph) | **前置知识:** Phase 11 · 09 (函数调用)、16 (LangGraph)
**Time:** ~45 minutes | **时间:** ~45 分钟

## 问题 问题引入

你有一个需要多次LLM调试的任务.也许这是一个研究工作流程 (计划,搜索,总结,引用).也许这是一个代码审查管道 (解析差异,批评,补丁,验证).也许这是一个多轮辅助员,谁会预订飞行,写电子邮件,文件支出报告.你选择一个框架.

> 你需要多次调用LLM的任务――也许是研究工作流 (规划,搜索,总结,引用)――也许是代码审查流水线 (解析,评价,修补,验证)――你选择了一个框架――

之后三天,你发现了框架的抽象漏洞. 机器人给你提供角色,但当"研究人员"需要把结构化的计划交给"作家"时,它会对你进行斗争. 兰格拉夫给你一个状态图, 但迫使你在你知道代理会做什么之前, 命名每个转变. 艾格诺给你一个单机抽象,当你试图扩散到三个同时工作者时,它会尖叫.

> 三天后,你发现框架的抽象会泄漏――机组人员给你角色,但当"研究员"需要把结构化计划交给"作家"时会出现问题――AutoGen给你代理间聊天,但没有等级公民状态――长图给你状态图,但迫使你知道代理会做什么之前就给你一个名称每个转换――Agno给你单个代理人抽象,当你试图推出三个并发出员工时会出现问题――

解决方案不是"选择最好的框架". 解决方案是将框架的核心抽象与您的问题的形状相匹配.

> 修复方法不是"选择最好的框架"",而是将框架的核心抽象与你问题的形状相匹配. 本课程绘制了这个地图.


> **【中文解读】**框架选型的三个维度:(1) 任务复杂性简单RAG 用LlamaIndex,复杂代理用LangGraph;(2) 团队经验新手使用LangChain 模板,专家使用原生API;(3) 生产要求需要LangSmith 集成选择LangChain 生态。

>  **【类比】**选 框架像选交通工具短途买菜用自行车(stdlib + 函数调用),跨城出差用车(LangGraph 状态机),多人旅行用面包车(CrewAI 角色),即时通讯用电话(AutoGen 对话) ⋅每种工具有适用场景,"哪个好"是错误问题,"哪个匹配你的问题形状"才是――

> ️ **【易错点】**框架选错的3个常见原因:**跟风最热门**AutoGen 火就上了AutoGen,结果发现任务只是单个代理+工具,过度工程;先评估任务复杂度再选择框架――(2) **被 demo 误导**CrewAI的"研究员+作家"示范看起来很酷,但实际任务里角色边界模糊,CrewAI的角色抽象反而拖累;先做PoC验证抽象匹配――(3) **低估迁移成本**开始使用Agno 简单,后期要增加 发现Agno 不支持,重写到 LangGraph 花两周;选择框架时看 6 个月后的需求──


## 概念的核心概念

> **【中文解读】**机器框架的选择是工程权衡:长链 生态最完整但最复杂,LlamaIndex 专注于RAG,CrewAI 适合多个机器协作,长图 适合状态机控制流,直接使用API最灵活但要自己写更多代码――

> **【拓展：Agent 框架的选型指南】**选型维度:(1) 任务复杂度(简单RAG 用LlamaIndex,复杂代理用LangGraph);(2) 团队经验(新手用LangChain 模板,专家用原生API);(3) 生产要求(LangSmith 集成选LangChain 生态) ・2025年趋势是框架轻量化――


![Agent framework matrix: core abstraction vs problem shape](../assets/framework-matrix.svg)

它们的核心抽象不一样.

> 它们的核心抽象不同.

| Framework | Core abstraction | Best fit | Worst fit |
|-----------|------------------|----------|-----------|
| **LangGraph** | `StateGraph` — typed state, nodes, conditional edges, checkpointer. | Workflows with explicit state and human-in-the-loop interrupts; production agents needing time-travel debugging. | Loose, role-driven brainstorming where the topology is unknown. |
| **CrewAI** | `Crew` — roles (goal, backstory), tasks, process (sequential or hierarchical). | Role-playing or persona-driven workflows with a short linear/hierarchical plan. | Anything stateful beyond the crew's turn history; complex branching. |
| **AutoGen** | `ConversableAgent` pair — two or more agents that speak in turns until an exit condition. | Multi-agent *dialogue* (teacher-student, proposer-critic, actor-reviewer) where the thinking emerges from the chat. | Deterministic workflows with a known DAG; anything needing durable state across restarts. |
| **Agno** | `Agent` — a single LLM + tools + memory, composable into teams. | Fast-to-build single agents and lightweight teams; strong multi-modality and built-in storage drivers. | Deep, explicitly-branched graphs with custom reducers. |

### "抽象"实际上意味着什么

框架的核心抽象是你在设计时绘制在白板上的东西.

> 框架的核心抽象是你在白板上画的东西,

- **LangGraph**结点是步骤,边缘是过渡,每个点都打字状态对象.
  你画一个图.节点是步骤,边是转换.心智模型是状态机.
- **CrewAI**工作人员的职位描述,管理员的任务路线.
  你画一个组织图.每个角色都有责任描述,管理分配任务.
- **AutoGen**两个代理人互相发短信,如果需要一个调节者,第三个加入.
  你画一个 Slack 私信. 两个代理.
- **Agno**让一个团队一起画一个单一的盒子,上面挂着工具. 让一个团队一起画一个盒子. 心理模型是"包括电池的代理".
  你画了一个挂在工具的方框.

### 国家问题

制造业的框架选择在大多数国家都会崩.

> 状态是大多数框架选择在生产中出问题的地方.

- **LangGraph.**类型状态 (`TypedDict`简历,中断和时间旅行是免费的. *(见第11期 · 16期.) *
  **LangGraph。**类型化状态`TypedDict`或 Pydantic 模型) 、每字段减小器、一等公民检查点器(SQLite/Postgres/Redis) ⋅恢复、中断和时间旅行免费──(见阶段11 · 16──)
- **CrewAI.**通过                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            `context`其他类型的`output_pydantic`没有一个持久的每员工店出盒子,如果你必须生存一个重启,你自己就会跳.
  **CrewAI。**状态作为字符串在任务间通过`context`字段流动,或通过`output_pydantic`结构化――开箱无持久的每人机组 储存;若机组人员 需要活着,需要自己外挂――
- **AutoGen.**状态是聊天历史和任何用户定义的状态`context`对话转录仍然存在,除非你写适配器,否则任意工作流状态不会存在.
  **AutoGen。**状态是聊天历史和任何用户定义的 `context`△对话记录持久化;任意工作流状态不持久化,除非写适配器──
- **Agno.**连接到一个 `Agent`通过`storage=`对话会话和用户记忆会自动保存.
  **Agno。**通过SQLite、Postgres、Mongo、Redis、DynamoDB`storage=`附在`Agent`上对话会话和用户记忆自动持久化──不是完整图片检查点器;是会话存储──

- **LangGraph.**类型状态 (`TypedDict`简历,中断和时间旅行是免费的. *(见第11期 · 16期.) *
- **CrewAI.**通过                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            `context`其他类型的`output_pydantic`没有一个持久的每员工店出盒子,如果你必须生存一个重启,你自己就会跳.
- **AutoGen.**状态是聊天历史和任何用户定义的状态`context`对话转录仍然存在,除非你写适配器,否则任意工作流状态不会存在.
- **Agno.**连接到一个 `Agent`通过`storage=`对话会话和用户记忆会自动保存.

### 分支问题

每个非微不足道的代理都分支,谁决定分支的事.

> 每个非凡的代理都有分支.

- **LangGraph**您决定,通过条件边缘.路由是一个名字分支的Python函数.分支在编译图中是第一类;检查点记录了哪个分支被取.
  **LangGraph**你决定,通过条件边缘──路由是带命名分支的 Python 函数──分支是编译图中的一等公民;检查点器记录走哪条──
- **CrewAI**管理者在等级模式下决定;在序列模式下,你决定在构建时.路由是隐含的任务列表中;管理者的提示之外没有一级"如果".
  **CrewAI**分层模式由经理决定;顺序模式你在构建时决定――路由隐含在任务列表中;经理提示外无一等公民"如果"――
- **AutoGen**代理人通过聊天决定. 分支是从谁接下来说.`GroupChatManager`选择下一个扬声器;你可以手写一个`speaker_selection_method`但默认的原因是,
  **AutoGen**经理通过聊天决定. 分支从谁下一个说话中涌现.`GroupChatManager`选下一个发言人;可手写`speaker_selection_method`但认可的法学士
- **Agno**代理人决定下一步使用哪个工具.团队有协调员/路由器/合作者模式;在此之外,分支是开发者的责任.
  **Agno**经过下一个调用哪个工具决定――团队有协调员/路由器/合作者模式;外分支由开发者负责――

- **LangGraph**您决定,通过条件边缘.路由是一个名字分支的Python函数.分支在编译图中是第一类;检查点记录了哪个分支被取.
- **CrewAI**管理者在等级模式下决定;在序列模式下,你决定在构建时.路由是隐含的任务列表中;管理者的提示之外没有一级"如果".
- **AutoGen**代理人通过聊天决定. 分支是从谁接下来说.`GroupChatManager`选择下一个扬声器;你可以手写一个`speaker_selection_method`但默认的原因是,
- **Agno**代理人决定下一步使用哪个工具.团队有协调员/路由器/合作者模式;在此之外,分支是开发者的责任.

### 观察性问题

> 观测性问题

- **LangGraph**通过兰格斯密或任何OTel出口商的OpenTelemetry.每个节点过渡都是追踪时间;检查站是可重复的追踪.兰格斯密是第一方选项;兰格斯密/尼克斯也拥有适配器.
  **LangGraph**通过LangSmith或任何 OTel导出器的OpenTelemetry──每个节点转换是一个追踪跨度;检查点兼作可重置追踪──LangSmith是第一方选项;Langfuse/Phoenix也有适配器──
- **CrewAI**自2025年底以来的第一级开放电气;与兰格斯,城,奥皮克,代理运营公司的集成.
  **CrewAI**2025年末起一等公民开放电讯;集成 朗夫斯、尼克斯、奥皮克、代理操作──
- **AutoGen**通过OpenTelemetry集成`autogen-core`检测细分度是每个代理信息,而不是每个节点.
  **AutoGen**通过`autogen-core`随访者对象的数据量是每一个代理的信息,而不是每一个节点.
- **Agno**内置`monitoring=True`旗加上OpenTelemetry出口商;密切与Langfuse集成,以便进行会议追踪.
  **Agno**内置 `monitoring=True`标志加 开放电气导出器;与兰格斯 紧密集成会话追踪.

### 成本和延迟

所有四个框架都增加了每次通话的通用费用 (框架逻辑,验证,序列化).大致的通用费用增加顺序:Agno ≈ LangGraph < CrewAI ≈ AutoGen. 差异由框架的额外LLM路由所占主导地位. CrewAI的层次管理人员花费代币决定谁接下来; AutoGen的代码.`GroupChatManager`长图只在你写的位置花钱.`llm.invoke`亚格诺的单机代理路线很薄.

> 四个框架都会增加每次调用开销.

当每次运行成本重要时,更好选择明确的路由 (长图边缘,自动生成`speaker_selection_method`) 通过选择LLM路线.

> 当每次运行成本重要时,优先使用显式路由而不是LLM选择路由.

### 互操作性

> 互操作性

- **LangGraph** **LangChain**工具,检索器,LLM. 一级MCP适配器 (作为MCP服务器进口的工具).
  **LangGraph** **LangChain**工具、检索器、LLM──一等公民MCP 适配器(工具作为MCP 服务器导入)。
- **CrewAI**工具继承`BaseTool`通过机组人员的代表团通过机组人员的代表团,`allow_delegation=True`现在,我们要去.
  **CrewAI** 工具继承自`BaseTool`长链工具 拉马指数工具 MCP工具都适合进来`allow_delegation=True`,我知道.
- **AutoGen**其他`FunctionTool`通过"Python"来调用,可使用的MCP适配器,并将其紧密地连接到AG2生态系统,以实现代理对代理模式.
  **AutoGen**其他`FunctionTool`包装任何Python可调用;MCP可适配器可用――与AG2生态紧密合用于代理模式――
- **Agno**其他`@tool`装饰器或BaseTool子类;MCP适配器;工具可在代理人和团队之间共享.
  **Agno**其他`@tool`装饰器或基工具 子类;MCP 适配器;工具可跨 Agent 和团队共享──

## 技能

> 您可以用一句话解释为什么给定的框架适合给定的代理问题.
> 你能用一句话解释为什么某个框架适合某个代理问题.

预制清单:

> 构建前检查清单:

1. **Draw the shape.**这是一个图表 (类型状态,命名的过渡);一个角色扮演 (专家放弃工作);一个聊天 (代理人谈到完成);一个单独的代理人有工具?
   **画出形状。**这是一个角色扮演的图片,聊天,还是带着工具的单身代理人?
2. **Decide who branches.**开发者决定分支 → 兰格拉夫. 管理者-代理人决定 → 机组人员等级. 聊天出现 → 自动生成. 工具调用决定 → Agno.
   **决定谁分支。**开发者决定 → LangGraph──经理 代理决定 → 机组人员AI──聊天涌现 → 机器人.工具调用决定 → 行动.
3. **Check the state budget.**如果是,则是LangGraph默认,AgnO会话覆盖对话范围状态.
   **检查状态预算。**你需要从检查点恢复吗?时间旅行?运行中人工中断?
4. **Check the cost budget.**如果代理人每天运行数千次, 宁愿明确的路由.
   **检查成本预算。**选择的路由每轮额外消耗代币
5. **Budget the framework overhead.**如果任务是两个LLM调用和一个工具,请写30行简单的Python;没有框架比没有框架便宜.
   **预算框架开销。**如果任务只是两次LLM调用一个工具,写30行纯 Python.

拒绝在绘制图表,组织图表,聊天或代理框之前寻找一个框架.拒绝选择一个强迫你为你真正需要的东西而战的框架.

> 在你能画图,组织图,聊天或代理框之前,不要伸出手拿一个框架.

## 决策矩阵

| Problem shape | Preferred framework | Why |
|---------------|---------------------|-----|
| Workflow DAG with typed state, human approvals, long-running | LangGraph | First-class state, checkpointer, interrupts, time-travel. |
| Research / writing pipeline with distinct roles | CrewAI (sequential) or LangGraph subgraphs | Role-per-task is cheap to express in CrewAI; scale up with LangGraph when branching gets complex. |
| Proposer-critic or teacher-student dialogue | AutoGen | Two-agent chat is its native shape. |
| Single agent with tools, sessions, memory | Agno | Thinnest setup, built-in storage and memory. |
| Thousands of parallel fanouts with reducers | LangGraph + `Send` | The only one with a first-class parallel-dispatch API. |
| Quick prototype, no framework commitment | Plain Python + provider SDK | No framework is the fastest framework. |

| 问题形状 | 推荐框架 | 原因 |
|---------|---------|------|
| 类型化状态的工作流 DAG、人工审批、长期运行 | LangGraph | 一等公民状态、检查点、中断、时间旅行 |
| 研究写作流水线带不同角色 | CrewAI（顺序）或 LangGraph 子图 | CrewAI 表达每任务角色便宜；分支复杂时用 LangGraph |
| 提议者-评论者或师生对话 | AutoGen | 双 Agent 聊天是其原生形状 |
| 单 Agent 带工具、会话、记忆 | Agno | 最薄设置，内置存储和记忆 |
| 数千并行扇出带 reducer | LangGraph + `Send` | 唯一带一等公民并行分派 API 的 |
| 快速原型、不绑定框架 | 纯 Python + 提供商 SDK | 无框架是最快的框架 |

## 练习题
```figure
l5-framework-fit
```

## 运动

1. **Easy.**"研究人类总部,写一个200字的简要,引用来源",并将其实现在LangGraph (四个节点:计划,搜索,写,引用) 和CrewAI (三个角色:研究人员,作家,编辑). 报告每次运行和代码行代码成本.
   通过在LangGraph和CrewAI中实现相同任务,报告每次运行的代码和代码行数.
2. **Medium.**在AutoGen中构建相同的任务 (研究人员 作家聊天,编辑通过 加入`GroupChat`) 和阿格诺 (一个代理人`search_tools`其他`write_tools`根据 (a) 每次运行成本, (b) 事故后恢复能力, (c) 在写作步骤之前注入人类批准的能力,将四个实现分类.
   在AutoGen和Agno实现相同任务,按成本,崩恢复能力,人工审批注入能力排名.
3. **Hard.**建立一个决策树脚本`pick_framework.py`需要简短的问题描述 (JSON: `{has_typed_state, has_roles, has_dialogue, has_parallel_fanout, needs_resume}`) 并返回一个句子的推,请在您自己设计的六个案例上验证.
   构建决策树脚本,根据问题描述返回框架推.

## 关键词 快速查找表

| Term | What people say | What it actually means | 中文释义 |
|------|-----------------|-----------------------|---------|
| Orchestration | "How the agents coordinate" / "Agent 如何协调" | The layer that decides which node/role/agent runs next. | 编排：决定哪个节点/角色/Agent 下一步运行的层 |
| Durable state | "Resume after a restart" / "重启后恢复" | State that survives process death, attached to a checkpoint or session store. | 持久状态：在进程终止后仍存活的状态 |
| LLM-selected routing | "Let the model decide" / "让模型决定" | A planner LLM picks the next step each turn; flexible but pays tokens on every decision. | LLM 选择路由：规划 LLM 每轮选择下一步 |
| Explicit routing | "Developer decides" / "开发者决定" | A Python function or static edge picks the next step; cheap and auditable. | 显式路由：Python 函数或静态边选择下一步 |
| Crew | "A CrewAI team" / "CrewAI 团队" | Roles + tasks + process (sequential or hierarchical) bound into a single runnable. | Crew：角色+任务+流程绑定成一个可运行单元 |
| GroupChat | "AutoGen's multi-agent chat" / "AutoGen 多 Agent 聊天" | A managed conversation between N agents with a speaker selector. | GroupChat：N 个 Agent 之间的托管对话 |
| Team (Agno) | "Multi-agent Agno" / "多 Agent Agno" | Route / coordinate / collaborate mode over a set of agents. | Team (Agno)：Agent 集合上的路由/协调/协作模式 |
| StateGraph | "LangGraph's graph" / "LangGraph 图" | Typed-state, node, conditional-edge, checkpointer abstraction. | StateGraph：类型化状态、节点、条件边、检查点抽象 |

## 继续阅读 继续阅读

- [LangGraph documentation](https://langchain-ai.github.io/langgraph/)国家图,检查点,中断,时间旅行.
  长度图文档 状态图检查点 断时间旅行
- [CrewAI documentation](https://docs.crewai.com/) 机组人员,流动,代理人,任务,过程.
  工作人员 文档 工作人员 流动 代理 任务 过程
- [AutoGen documentation](https://microsoft.github.io/autogen/)可交谈的代理,集团聊天,团队,工具.
  交谈可用代理,群体聊天,团队,工具.
- [Agno documentation](https://docs.agno.com/)代理,团队,工作流程,存储,内存.
  工作流程,存储,记忆.
- [Anthropic — Building effective agents (Dec 2024)](https://www.anthropic.com/research/building-effective-agents)模式图书馆 (即时链接,路由,并行,管弦工作者,评估者优化器) 框架-无知.
  关于构建有效代理的模式库,框架无关.
- [Yao et al., "ReAct: Synergizing Reasoning and Acting" (ICLR 2023)](https://arxiv.org/abs/2210.03629)每个框架都穿着循环.
  每个框架都包含在包装中的 ReAct 循环的原始论文.
- [Wu et al., "AutoGen: Enabling Next-Gen LLM Applications via Multi-Agent Conversation" (2023)](https://arxiv.org/abs/2308.08155) 汽车代购设计文件.
  汽车代码的设计论文
- [Park et al., "Generative Agents: Interactive Simulacra of Human Behavior" (UIST 2023)](https://arxiv.org/abs/2304.03442)角色扮演基础, CrewAI风格的人物堆建立在.
  员工的角色扮演基础.
-                                                                                                                                                                                                                                                               
  本课对比的基准框架
- 阶段11·19 (反射) 一个图案,它清晰地映射到LangGraph,但对CrewAI来说很尬.
  一个在LangGraph中清晰映射,但在CrewAI中拙的模式.
- 如何使用仪器,无论你选择哪个框架.
  如何为您选择任何框架添加可观测性.
