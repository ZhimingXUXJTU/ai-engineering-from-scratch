# Hierarchical Architecture and Its Failure Mode | 分层

> Hierarchical is supervisor nested. Manager agents over sub-managers over workers. CrewAI `Process.hierarchical` is the textbook version: a `manager_llm` dynamically delegates tasks and validates outputs. The LangGraph equivalent is `create_supervisor(create_supervisor(...))`. It is the natural pattern when the task is a real org chart. It is also the pattern most likely to collapse into managerial looping — manager agents assign work poorly, misinterpret sub-outputs, or fail to reach consensus. Sequential often beats it.

> **【中文解读】** 本节介绍了分层架构——多层编排器的嵌套组织结构，适用于复杂任务的递归分解。

> **【拓展：hierarchical architecture→具体应用】** 分层架构将监督者模式递归嵌套——顶层主管分配给中层管理者，中层管理者再分配给底层工作者。这类似于人类组织的层级结构。2026 年的实践表明，2-3 层的层次是最优的——太浅（1层）导致主管过载，太深（4+层）导致信息失真和延迟增加。


**Type:** Learn + Build | **类型:** 学习 + 构建
**Languages:** Python (stdlib) | **语言:** Python (标准库)
**Prerequisites:** Phase 16 · 05 (Supervisor Pattern) | **前置知识:** Phase 16 · 05 (监督者模式)
**Time:** ~60 minutes | **时间:** ~60 分钟

> 🔗 **【前置】** 学本节前请先掌握：Phase 16·05（Supervisor 模式）。本节 = Supervisor 嵌套 Supervisor——多层管理。失败模式 = "经理们开会议而不做事"。
> 💡 **【类比】** 分层架构 = "公司层级"。1 层 = 创业公司（CEO 直接带工程师）；2-3 层 = 中型公司（最优）；4+层 = 大企业病（信息失真、决策缓慢、经理们扯皮）。Agent 也一样——2-3 层最优，多了就"管理循环"：经理 Agent 互相指派却不真做事。
> ⚠️ **【易错点】** 看到"任务复杂"就加层级 → 管理开销压垮系统。修复：先用 sequential 或 supervisor 单层跑，确认不够再分层；2-3 层是上限。

## Problem | 问题引入

Once the supervisor pattern clicks, the natural next step is "what if the workers are themselves supervisors?" Teams have sub-teams; companies have departments of departments. Hierarchical architectures mirror that.

> 一旦监督者模式理解了，自然的下一步是"如果工作器本身也是监督者呢？"团队有子团队；公司有部门的部门。分层架构反映了这一点。

The temptation is strong because human organizations work this way. But LLM hierarchies inherit all the pathologies of human hierarchies (information loss, miscommunication, slow iteration) without the stabilizing effects of human relationships and shared culture.

> 诱惑很强，因为人类组织这样工作。但 LLM 层级继承了人类层级的所有病态（信息丢失、错误沟通、缓慢迭代），却没有人类关系和共享文化的稳定效应。

The issue: LLM managers are not the same as human managers. A human manager has stable priors about what their reports know. An LLM manager re-reasons the org every turn from whatever is in its context. Tiny drift in that context, and the whole tree misallocates work.

> 问题在于：LLM 管理者与人类管理者不同。人类管理者对其下属知道什么有稳定的先验。LLM 管理者每轮从其上下文中的内容重新推理组织。上下文中的微小漂移，整个树就会错误分配工作。

This is the core failure mode of hierarchical LLM systems: every manager level amplifies the previous level's errors. A 5% misallocation at the top becomes 25% by level 3, because each level reinterprets the (already-wrong) delegation.

> 这是分层 LLM 系统的核心失败模式：每个管理者层级放大上一层的错误。顶部 5% 的错误分配到第 3 层变成 25%，因为每层重新解释（已经错误的）委派。

## Concept | 核心概念

### The shape

```
                 Manager
                 ┌─────┐
                 └──┬──┘
           ┌────────┴────────┐
           ▼                 ▼
       Sub-Mgr A         Sub-Mgr B
       ┌─────┐           ┌─────┐
       └──┬──┘           └──┬──┘
         ┌┴──┬──┐          ┌┴──┐
         ▼   ▼  ▼          ▼   ▼
       W1  W2  W3         W4  W5
```

Every internal node plans, delegates, and synthesizes. Only leaves do work.

> 每个内部节点规划、委派和综合。只有叶子节点做实际工作。

This mirrors a human org chart, which is both its strength (familiar mental model) and weakness (human orgs have stable priors that LLMs lack). Each LLM level re-reasons the org from scratch every turn.

> 这映射了人类组织架构，这既是其优势（熟悉的心智模型）也是其弱点（人类组织有 LLM 缺乏的稳定先验）。每个 LLM 层级每轮从头重新推理组织。

### Where it shines

- **Clear org mapping.** If the real task is departmental ("legal review the doc, finance review the doc, engineering review the doc, then summarize for exec"), the hierarchy is explicit.
  中文翻译：**清晰的组织映射。** 如果实际任务是部门性的（"法务审阅文档、财务审阅文档、工程审阅文档，然后为高管总结"），层级结构是明确的。
- **Local summarization.** Each sub-manager synthesizes its team's output before the top manager sees it. Top manager sees three sub-manager summaries, not fifteen worker outputs.
  中文翻译：**局部摘要。** 每个子管理者在顶层管理者看到之前综合其团队的输出。顶层管理者看到三个子管理者摘要，而不是十五个工作器输出。

### Where it breaks

Three failure modes the 2026 post-mortems keep finding:

> 2026 年事后分析不断发现的三种失败模式：

Cemri et al. (MAST, arXiv:2503.13657) document these as "specification failure" and "interpersonal misalignment" sub-families. Hierarchical systems exhibit them more than flat ones because each level adds a reinterpretation step.

> Cemri 等人（MAST，arXiv:2503.13657）将这些记录为"规范失败"和"人际不对齐"子家族。分层系统比扁平系统更容易出现这些问题，因为每层添加重新解释步骤。

1. **Task assignment error.** The manager reads the goal, hallucinates a decomposition, and delegates to the wrong sub-manager. Because the sub-manager obediently works on what it was given, the error only surfaces at the top synthesis — one level removed from where a human could have caught it.
   中文翻译：**任务分配错误。** 管理者读取目标，幻觉出分解，并委派给错误的子管理者。因为子管理者服从地处理给定的任务，错误只在顶层综合时浮现——比人类本可以捕获的位置高了一层。
2. **Output misinterpretation.** Sub-manager returns "unable to verify claim X." Top manager summarizes as "claim X not confirmed." Meaning drifts at every level.
   中文翻译：**输出误解。** 子管理者返回"无法验证声明 X。"顶层管理者总结为"声明 X 未确认。"含义在每一层都漂移了。
3. **Consensus loops.** Two sub-managers disagree; top manager asks them to reconcile; they re-delegate down; workers re-run; sub-managers return slightly different answers; loop. CrewAI's `Process.hierarchical` guards against this with step limits, but the limit itself is now a hyperparameter.
   中文翻译：**共识循环。** 两个子管理者不一致；顶层管理者要求他们协调；他们向下重新委派；工作器重新运行；子管理者返回略有不同的答案；循环。CrewAI 的 `Process.hierarchical` 通过步骤限制来防护，但限制本身现在是一个超参数。

### The deciding question

Sequential (linear pipeline) vs hierarchical: does your task actually have independent sub-teams, or is it one linear flow pretending to be a tree? If the latter, use sequential. If the former, use hierarchical but budget explicit reconciliation rules.

> 顺序（线性流水线）vs 分层：你的任务真的有独立的子团队，还是一个伪装成树的线性流程？如果是后者，使用顺序。如果是前者，使用分层但要预算明确的协调规则。

This is the test most teams skip. They reach for hierarchical because it sounds sophisticated, then spend weeks debugging decomposition drift. Sequential pipelines finish faster, debug easier, and rarely "lose the plot."

> 这是大多数团队跳过的测试。他们因为听起来高级而选择分层，然后花几周调试分解漂移。顺序流水线完成更快、调试更容易、很少"偏离主题"。

### CrewAI's implementation

`Process.hierarchical` wires a manager LLM over specialist crews. The manager:

> `Process.hierarchical` 在专家团队上连接一个管理者 LLM。管理者：

The manager LLM is itself a full agent with its own context, prompt, and tools. It is not a deterministic dispatcher — it makes judgement calls about delegation, which means it can make wrong judgement calls. This is the source of the task-assignment failure mode.

> 管理者 LLM 本身是一个带自己上下文、提示和工具的完整 Agent。它不是确定性调度器——它对委派做出判断调用，这意味着它可以做出错误判断调用。这是任务分配失败模式的来源。

- receives the top-level task,
  中文翻译：接收顶层任务，
- assigns subtasks to crews,
  中文翻译：将子任务分配给团队，
- evaluates crew outputs,
  中文翻译：评估团队输出，
- decides whether to accept, re-delegate, or iterate.
  中文翻译：决定是接受、重新委派还是迭代。

Documentation: https://docs.crewai.com/en/introduction (look for "Hierarchical Process" under Core Concepts).

> 文档：https://docs.crewai.com/en/introduction（在核心概念中查找"Hierarchical Process"）。

### LangGraph's implementation

LangGraph uses nested `create_supervisor` calls. The inner supervisor has its own graph; the outer supervisor treats the inner graph as an opaque node. This is cleaner than CrewAI for debugging (you can step through each graph separately) but harder to express dynamic reshaping of the tree.

> LangGraph 使用嵌套的 `create_supervisor` 调用。内部监督者有自己的图；外部监督者将内部图视为不透明节点。这在调试方面比 CrewAI 更清晰（你可以分别步进每个图），但更难表达树的动态重塑。

The debugging win is real: when something goes wrong in a 3-level LangGraph hierarchy, you can isolate which level failed by stepping through each graph independently. In CrewAI, the manager LLM is one opaque call that may have delegated wrong.

> 调试优势真实：当 3 层 LangGraph 层级出错时，你可以通过独立步进每个图来隔离哪个层级失败了。在 CrewAI 中，管理者 LLM 是一个可能委派错误的不透明调用。

Reference: https://reference.langchain.com/python/langgraph-supervisor.

> 参考：https://reference.langchain.com/python/langgraph-supervisor。

## Build It | 动手实现

`code/main.py` runs a 3-level hierarchy:

> `code/main.py` 运行一个 3 层层级：

- top manager: splits a task into "engineering" and "legal" branches,
  中文翻译：顶层管理者：将任务拆分为"工程"和"法务"分支，
- engineering sub-manager: splits into "frontend" and "backend" workers,
  中文翻译：工程子管理者：拆分为"前端"和"后端"工作器，
- legal sub-manager: one worker.
  中文翻译：法务子管理者：一个工作器。

Demo contrasts happy path (everyone agrees) against a **perturbed path** where the top manager's decomposition mislabels "legal" as "finance" and watches the error cascade — the sub-manager obediently does finance work, the top synthesizer reports finance findings, the original legal question goes unanswered.

> 演示对比了正常路径（所有人一致）与**扰动路径**，其中顶层管理者的分解将"法务"错误标记为"财务"并观察错误级联——子管理者服从地做财务工作，顶层综合者报告财务发现，原始的法务问题没有得到回答。

The perturbed path is the warning: hierarchical systems amplify errors silently. The sub-manager does not push back ("you said finance, but the task said legal"). It assumes the manager knows better. By the time anyone notices, the original intent is lost.

> 扰动路径是警告：分层系统静默放大错误。子管理者不反驳（"你说的财务，但任务说的法务"）。它假设管理者更了解。当任何人注意到时，原始意图已丢失。

Run:

```
python3 code/main.py
```

Output shows both paths with a clear side-by-side of "what was asked" vs "what was delivered."

> 输出显示两条路径的清晰并排对比："要求什么"与"交付了什么"。

## Use It | 用框架实现

`outputs/skill-hierarchy-fitness.md` evaluates whether a given task should use hierarchical, sequential, or flat supervisor. Inputs: task description, org structure, reconciliation budget. Output: pattern recommendation with the specific failure modes to guard against.

> `outputs/skill-hierarchy-fitness.md` 评估给定任务应该使用分层、顺序还是扁平监督者。输入：任务描述、组织结构、协调预算。输出：模式建议及需要防护的特定失败模式。

## Ship It | 产出物

If you ship hierarchical:

> 如果你部署分层架构：

- **Cap tree depth at 2.** Three levels already hides most errors from observability.
  中文翻译：**将树深度限制在 2。** 三层已经将大多数错误隐藏在可观测性之外。
- **Explicit reconciliation budget.** Set max rounds before the top manager must commit. Usually 2.
  中文翻译：**明确的协调预算。** 在顶层管理者必须提交之前设置最大轮数。通常是 2。
- **Provenance on every synthesis.** Each node's summary must cite which leaf outputs produced it.
  中文翻译：**每次综合的来源追溯。** 每个节点的摘要必须引用产生它的叶子输出。
- **Alert on decomposition drift.** Log the manager's decomposition per step; diff against the user query. If the decomposition no longer covers the query, fire an alert.
  中文翻译：**分解漂移告警。** 记录管理者每步的分解；与用户查询对比。如果分解不再覆盖查询，触发告警。

## Exercises | 练习题

1. Run `code/main.py` and compare happy vs perturbed. How many levels of manager hand-off does it take before the top output fully diverges from the user's question?
   中文翻译：运行 `code/main.py` 并比较正常路径与扰动路径。需要多少层管理者交接才能使顶层输出完全偏离用户的问题？
2. Add a third level (top -> sub -> sub-sub -> worker). Measure how often the perturbed path corrects itself vs fully diverges as depth grows.
   中文翻译：添加第三层（顶层 -> 子 -> 子子 -> 工作器）。测量随着深度增加，扰动路径自我纠正与完全偏离的频率。
3. Implement a "canary" worker at each sub-manager that is always asked the original user question unchanged. Use the canary answer to detect decomposition drift. How should the manager react when the canary disagrees with the synthesized answer?
   中文翻译：在每个子管理者处实现一个"金丝雀"工作器，总是被问及原始用户问题不变。使用金丝雀答案检测分解漂移。当金丝雀与综合答案不一致时管理者应该如何反应？
4. Read CrewAI's `Process.hierarchical` docs. Identify one concrete guardrail CrewAI applies (step limit, manager_llm constraint) and describe what failure mode it targets.
   中文翻译：阅读 CrewAI 的 `Process.hierarchical` 文档。识别 CrewAI 应用的一个具体防护措施（步骤限制、manager_llm 约束）并描述它针对的失败模式。
5. Compare nested LangGraph supervisors to CrewAI hierarchical. Which makes reconciliation loops cheaper to detect?
   中文翻译：比较嵌套的 LangGraph 监督者与 CrewAI 分层。哪个使协调循环更容易检测？

## Key Terms | 术语速查表

| Term | What people say | What it actually means |
|------|----------------|------------------------|
| Hierarchical / 分层 | "Org chart pattern" / "组织架构模式" | Supervisors over supervisors; only leaves do work. / 监督者之上还有监督者；只有叶子节点做实际工作。 |
| Manager LLM / 管理者 LLM | "The boss" / "老板" | The LLM that decomposes, assigns, and validates at an internal node. / 在内部节点进行分解、分配和验证的 LLM。 |
| Decomposition drift / 分解漂移 | "The boss lost the plot" / "老板偏离了主题" | Top manager's split no longer covers the original question. / 顶层管理者的拆分不再覆盖原始问题。 |
| Reconciliation loop / 协调循环 | "Endless meetings" / "无尽会议" | Sub-managers disagree; top re-delegates; workers re-run; loop until budget exhausted. / 子管理者不一致；顶层重新委派；工作器重新运行；循环直到预算耗尽。 |
| Depth-2 ceiling / 深度-2 上限 | "Don't go deeper than 2 levels" / "不要超过 2 层" | Empirical guardrail: 3+ levels collapses observability. / 经验防护：3+ 层使可观测性崩溃。 |
| Canary question / 金丝雀问题 | "Ground truth at every level" / "每层的基准真相" | A worker that is always asked the original query unchanged, to detect drift. / 一个总是被问及原始查询不变的工作器，用于检测漂移。 |
| Provenance chain / 来源链 | "Who said what" / "谁说了什么" | Trace from each synthesis back to the leaf outputs that produced it. / 从每个综合追溯到产生它的叶子输出。 |

## Further Reading | 延伸阅读

- [CrewAI introduction — Process.hierarchical](https://docs.crewai.com/en/introduction) — textbook hierarchical with a manager LLM
  中文翻译：CrewAI 介绍 — Process.hierarchical — 带管理者 LLM 的教科书式分层
- [LangGraph supervisor reference](https://reference.langchain.com/python/langgraph-supervisor) — nested supervisor via `create_supervisor`
  中文翻译：LangGraph 监督者参考 — 通过 `create_supervisor` 的嵌套监督者
- [Anthropic engineering — Research system](https://www.anthropic.com/engineering/multi-agent-research-system) — why Anthropic deliberately chose flat supervisor over hierarchical
  中文翻译：Anthropic 工程 — 研究系统 — 为什么 Anthropic 有意选择扁平监督者而不是分层
- [Cemri et al. — Why Do Multi-Agent LLM Systems Fail?](https://arxiv.org/abs/2503.13657) — MAST taxonomy; section on coordination failures documents decomposition drift
  中文翻译：Cemri 等人 — 为什么多 Agent LLM 系统会失败？ — MAST 分类法；协调失败部分记录了分解漂移
