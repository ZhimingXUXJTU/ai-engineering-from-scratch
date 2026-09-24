# 长度图:状态图和持久执行
# 状态图管弦乐  持久执行和检查点

> 代理是一个状态机;节点是函数;边缘是过渡;状态是每个节点后的检查点.在最后一个成功检查点中恢复任何失败. 兰格格拉夫是2026年低级状态调整模型的参考.

> **【中文解读】**兰格格拉夫是2026年底层有状态编排的参考实现. 代理是状态机;节点是函数;边是转换;状态是不可变的,并且每步检查点保存.

**Type:** Learn + Build | **类型:** 学习 + 构建
**Languages:** Python (stdlib) | **语言:** Python (标准库)
**Prerequisites:** Phase 14 · 01 (Agent Loop), Phase 14 · 12 (Workflow Patterns) | **前置知识:** Phase 14 · 01 (Agent 循环), Phase 14 · 12 (工作流模式)
**Time:** ~75 minutes | **时间:** ~75 分钟

## 学习目标

- 描述兰格拉夫的核心模型:具有不可变状态的状态机,功能节点,条件边缘和后步骤检查点.
  中文翻译:描述LangGraph的核心模型:带不可变状态"",函数节点"",条件边和步后检查点的状态机"",
- 描述兰格拉夫的核心模型:状态机,具有打字状态,函数节点,条件边缘和节点后检查点.
- 文件强调的四个功能:持久执行,流媒体,人在循环,全面的内存.
  中文翻译:说出文档强调的四种能力:持久执行、流式传输、人回路中、全面记忆──
- 解释LangGraph支持的三个管弦乐拓:监督,同行 (群) 和层次 (嵌套子图).
  中文翻译:解释 LangGraph 支持的三种编排拓:监督者、点对点(群体)、层次化(嵌套子图)。
- 实现一个具有不可变状态,条件边缘和检查点/恢复周期的 stdlib状态图.
  中文翻译:用标准库实现带不可变状态"",条件边和检查点/恢复周期的状态图"",
- 实现一个具有输入状态,条件边缘和检查点/恢复周期的 stdlib状态图.

## 问题 问题引入

代理人和工作流程都有一个问题:当40步运行在38步失败时,你想从38步开始,而不是重新开始.二级状态模型让运营商在一个库中重新尝试,该库假设新的运行.

> 经理和工作流共享一个问题:当40步运行在第38步失败时,你想从第38步恢复而不是从头开始.

兰格拉夫的设计答案:状态是一个第一类类的类型对象,突变是明确的,并且检查点在每个节点之后仍然存在.`load_state(session_id)`给我打电话.

> 张图的设计答案:状态是同等公民带类型的对象,变更操作是显而易见的,检查点在每个节点后持久化――恢复只需要调用`load_state(session_id)`,我知道.

> **【中文解读】**经理和工作流共享一个问题:当40步运行在第38步失败时,你想从第38步恢复而不是从头开始.`load_state(session_id)`,我知道.

> **【拓展：LangGraph → 状态图编排】**兰格拉夫是2026年底层有状态编排的参考实现.它将使代理建模为状态机节点是函数,边是条件转换,状态在每个步骤后被检查点保存.

>  **【前置】**必须先掌握:阶段14·01(代理循环) 和阶段14·12 ((人类工作流模式) 长图就是工作流模式的"持久化版本"――还需要状态机/有限状态自动机 (FSM) 的基本概念节点、边缘、状态、迁移条件――如果这些术语不太熟悉,先看一节编译原理或离散数学――

## 概念的核心概念

### 图表

一个图表由:一个打字的定制 (或Pydantic模型) 每个节点都会读取和变异.

> 图由以下定义:一个每个节点都读写的带类型的句子 (或Pydantic模型) ⋅

- **Nodes.**纯功能的`(state) -> state_update`更新后将合并到状态.
  翻译: 中文**节点。**纯函数`(state) -> state_update`〔更新在返回后合并到状态中〕
- **Edges.**节点之间的条件或直接过渡.
  翻译: 中文**边。**节点之间的条件或直接转换.
- **Entry and exit.** `START`其他`END`卫兵节点标记了边界.
  翻译: 中文**入口和出口。** `START`和 `END`哨兵节点标记边界――

> **【中文解读】**图由三个要素定义:(1) 状态类型每个节点读写的带类型 dict 或 Pydantic 模型;(2) 节点纯函数`(state) -> state_update`返回值合并到状态中; 3) 边节点之间的条件或直接转换.

举个例子:一个代理人`classify`现在`refund`现在`bug`现在`sales`现在`done`节点 作为图的路由工作流程.

> 示例:一个包含`classify`,我知道.`refund`,我知道.`bug`,我知道.`sales`,我知道.`done`节点的代理路由工作流作为图.

### 持续执行

每个节点返回后,运行时间将状态串行并将其写入一个检查点 (SQLite,Postgres,Redis,定制).在步骤N中失败时,运行时间可以`resume(session_id)`接下来从步骤N+1进行精确状态.

> 每个节点返回后,运行时序列化状态并写入检查点器(SQLite、Postgres、Redis、自定义) ⋅在步骤N 失败时,运行时可以`resume(session_id)`没有从步骤N+1 用精确状态继续.

拉格格拉夫文件明确强调生产用户在哪里重要:克拉纳,Uber,J.P.摩根.

>  **【类比】**拉格格拉夫的检查点 像游戏的"自动档案":每过一个关卡(节点) 就自动档案一次――第38关老板 战挂了,你不需要从第1关重打读第37关档接下来打就行――生产代理 运行40步长任务在第38步失败时,没有检查点就从头重运行(烧代币),有检查点 直接`resume(session_id)`接着干

> 张格拉夫文档明确强调了这一点的生产用户:克larna、Uber、J.P. Morgan──声明不是图形形;而是图形形加上检查点使恢复成本很低──

### 流媒体

每个节点都能产生部分输出. 图表向调用者传输每个节点-delta事件,以便随着图表运行 UI 更新.

> 每节点可产生部分输出.图向调用者流式传输. 每节点增量事件,使 UI 在图运行时更新.

### 轮中的人

检查和修改节点之间的状态. 实现:在关键节点之前暂停,向人类表现状态,接受修改,恢复. 检查点使这很容易,因为状态已经串行.

> 在关键节点前暂停,向人类展示状态,接受修改,恢复.

### 记忆

短期 (运行中对话历史状态) 和长期 (通过检查点加上单独的长期存储器持续的跨运行). 兰格拉夫通过工具与外部内存系统 (Mem0,定制) 集成.

> 短期 (一次运行内状态中的对话历史) 和长期 (长期) 跨运行 (通过检查点器加独立长期储存持久化) 长度图 (通过工具和外部记忆系统) 记忆 自定义) 集成――

### 三种拓

1. **Supervisor.**专业的子管. `create_supervisor()`在`langgraph-supervisor`(尽管2026年兰格链团队建议通过直接调用工具来进行更多的语境控制).
   翻译: 中文**监督者。**中央路由法师师范大学 分派到专家子代理.
2. **Swarm / peer-to-peer.**代理人直接通过共享工具表面交付.
   翻译: 中文**群体/点对点。**通过共享工具接口直接移交.
3. **Hierarchical.**监管部门管理子监管部门,作为嵌套子图.
   翻译: 中文**层次化。**监督者管理子监督者实现为嵌套子图.

### 在这个模式出现错误的地方

> ️ **【易错点】**最常见的失败:节点里用了`datetime.now()`随着时间的推移,这些价值会变化.**后果**检查点恢复后,节点重新执行与原运行不同结果,整个状态机进入混乱.**一行修复**时间,随机,外部API返回) 都必须被捕获到状态,节点函数读状态而不是直接调用`datetime.now()`,我知道.

- **Checkpoints too small.**只有检查对话转换, 工具状态和记忆写不可回收. 完整状态必须串行.
  翻译: 中文**检查点太小。**仅查点对话轮次会留下不可恢复的工具状态和记忆写入――必须序列化完整状态――
- **Non-deterministic nodes.**简历假设节点输入产生相同状态更新. 随机种子,墙钟,外部API必须捕获.
  翻译: 中文**非确定性节点。**恢复假设节点输入产生相同状态更新.随机种子,挂钟时间,外部API必须被捕获.
- **Over-use of conditional edges.**图表的每个边缘都是条件的,这是一个无法推理的状态机器.
  翻译: 中文**过度使用条件边。**每条边都是条件图是无法推理的状态机.

>  **【困惑】**问:三种拓(监督员,群众,等级) 到底该选哪个?**任务可分解为独立角色**监管员 (如客服/退款/技术) 选;**Agent 之间是协作关系而非派发关系**选择群众 (如辩论、相互审查)**任务有天然层次结构**长链团队2026年建议:能直接用工具调用解决别人的监督直接工具调用下文控制更精细――

## 动手构建
```figure
langgraph-state
```

## 建立它

`code/main.py`执行一个 stdlib 状态图:

> `code/main.py`使用标准库实现了状态图:

- `State`一个字符号的字符号`messages`现在`step`现在`route`现在`output`现在`human_approval`现在,我们要去.
  翻译: 中文`State`包含`messages`,我知道.`step`,我知道.`route`,我知道.`output`,我知道.`human_approval`带类型的命令.
- `Node`可调用状态检查和返回更新命令.
  翻译: 中文`Node`接受状态并返回更新命令的可调用对象──
- `StateGraph`节点+边缘+条件边缘+运行+续航.
  翻译: 中文`StateGraph`节点 + 边 + 条件边 + 运行 + 恢复。
- `SQLiteCheckpointer`将每个节点后的状态串行;`load(session_id)`恢复.
  翻译: 中文`SQLiteCheckpointer`节点后序列化状态`load(session_id)`恢复
- 展示图:分类 -> 分类(退款 / 错误 / 销售) -> 人类门 -> 发送.
  中文翻译:演示图:分类 -> 分支(退款 / 错误 / 销售) -> 人类门 -> 发送──

运行它:

> 运行:

```
python3 code/main.py
```

后续的痕迹显示,第一次跑步失败了,

> 轨迹显示第一次运行在人类门口控制处失败,持续,然后恢复产生最终输出.

## 用它实现框架

- **LangGraph**参考,生产准备. 使用`create_react_agent`现在`create_supervisor`没有任何可能的图表.
  翻译: 中文**LangGraph**参考实现,生产就绪──使用 `create_react_agent`,我知道.`create_supervisor`或构建自己的图片.
- **AutoGen v0.4**演员模式替代性高竞争性场景.
  翻译: 中文**AutoGen v0.4**演员模型替代方案──
- **Claude Agent SDK**管理带有内置的会议商店.
  翻译: 中文**Claude Agent SDK**带内置会话存储的托管框架
- **Custom**当你需要对状态形状或检查点后端的确切控制时.
  翻译: 中文**自定义**当你需要精确控制状态形状或检查点器后端时.

## 运送它.

`outputs/skill-state-graph.md`在任何目标运行时间内生成一个长图形状态图,

> `outputs/skill-state-graph.md`在任何目标运行中生成LangGraph形状状态图,内置检查点和恢复.

## 练习题

1. 添加一个条件边缘从`classify`为了`end`继续运行,然后再追踪人类的设置.`route`通过手动.
   中文翻译:当分类置信度低于值时添加从`classify`到了`end`条件边缘. 人手动设置.`route`后恢复运行.
2. 换一个真实的SQLite检查点,按步骤测量序列化.
   中文翻译:将SQLite 模拟替换为真实SQLite 检查点器――测量每步序列化开销――
3. 实现平行边缘:两个节点同时运行,通过定制减速器合并.
   中文翻译:实现并行边:两个节点并发运行,用自定义减速器合并――不可变状态在这里带来什么?
4. 阅读`langgraph-supervisor`转移玩具到`create_supervisor`比较了痕迹的形状.
   中文翻译:阅读 `langgraph-supervisor`参考――将玩具移植为`create_supervisor`比轨迹形态
5. 添加流量:每一个节点在运行时都会产生部分状态.
   中文翻译:添加流式传输:每节点运行时产生部分状态――印到达的增量――

## 关键词 快速查找表

| Term | What people say | What it actually means |
|------|-----------------|-----------------------|
| 术语 | 通俗说法 | 实际含义 |
| State graph | "Agent as state machine" / "Agent 即状态机" | Typed state + nodes + edges + reducers / 带类型状态 + 节点 + 边 + reducer |
| Checkpointer | "Persistence backend" / "持久化后端" | Serializes state after every node; enables resume / 每个节点后序列化状态；支持恢复 |
| Reducer | "State merger" / "状态合并器" | Function that combines current state with a node's update / 将当前状态与节点更新合并的函数 |
| Conditional edge | "Branch" / "分支" | Edge chosen by a function of state / 由状态函数选择的边 |
| Subgraph | "Nested graph" / "嵌套图" | A graph used as a node inside another graph / 作为另一个图内节点使用的图 |
| Durable execution | "Resume from failure" / "从失败恢复" | Restart at the last successful node with exact state / 在最后成功节点处用精确状态重启 |
| Supervisor | "Router LLM" / "路由 LLM" | Central dispatcher for specialist subagents / 专家子 Agent 的中央分派器 |
| Swarm | "P2P agents" / "P2P Agent" | Agents hand off via shared tools; no central router / Agent 通过共享工具移交；无中央路由 |

## 继续阅读 继续阅读

- [LangGraph overview](https://docs.langchain.com/oss/python/langgraph/overview)参考文件
  中文翻译:长图概览 参考文档。
- [langgraph-supervisor reference](https://reference.langchain.com/python/langgraph/supervisor/)监督模式API
  中文翻译:langgraph-supervisor 参考监督者模式API。
- [AutoGen v0.4, Microsoft Research](https://www.microsoft.com/en-us/research/articles/autogen-v0-4-reimagining-the-foundation-of-agentic-ai-for-scale-extensibility-and-robustness/)演员模式替代
  中文翻译:AutoGen v0.4 微软研究Actor 模型替代方案。
- [Claude Agent SDK overview](https://platform.claude.com/docs/en/agent-sdk/overview)会议店和副行
  中文翻译:Claude Agent SDK 概览会话存储和子代理──
