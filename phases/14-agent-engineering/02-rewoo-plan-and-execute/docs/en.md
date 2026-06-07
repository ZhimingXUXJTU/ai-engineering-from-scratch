# ReWOO and Plan-and-Execute: Decoupled Planning | ReWOO 与计划-执行模式：解耦规划

> ReAct interleaves thought and action in one stream. ReWOO separates them: one big plan up front, then execute. 5x fewer tokens, +4% accuracy on HotpotQA, and you can distill the planner into a 7B model. Plan-and-Execute generalized it; Plan-and-Act scaled it to web navigation.

> **【中文解读】** ReAct 在一个流中交替思考和行动。ReWOO 将它们分离：先一次性制定完整计划，然后执行。Token 消耗减少 5 倍，HotpotQA 准确率提升 4%，还可以将规划器蒸馏到 7B 模型。Plan-and-Execute 是其泛化版本，Plan-and-Act 将其扩展到网页导航。

> **【拓展：ReWOO → 现代 Agent 架构】** Anthropic 的 "Building Effective Agents" 博文推荐的五种工作流模式中，计划-执行模式是核心之一。2026 年的生产级 Agent（如 Devin、Claude Code 的多步骤任务）都采用类似模式——先规划、再执行、最后整合结果。

**Type:** Build | **类型:** 构建
**Languages:** Python (stdlib) | **语言:** Python (标准库)
**Prerequisites:** Phase 14 · 01 (Agent Loop) | **前置知识:** Phase 14 · 01 (Agent 循环)
**Time:** ~60 minutes | **时间:** ~60 分钟

## Learning Objectives | 学习目标

- Explain why ReWOO's Planner / Worker / Solver split saves tokens and improves robustness over ReAct's interleaved loop.
  中文翻译：解释为什么 ReWOO 的规划器/工作器/求解器分离能节省 token 并比 ReAct 的交替循环更健壮。
- Implement a plan DAG, a dependency-ordered executor, and a solver that composes worker outputs — all stdlib.
  中文翻译：实现计划 DAG、依赖顺序执行器和组合工作器输出的求解器——全部使用标准库。
- Decide when a task should run as plan-then-execute vs interleaved ReAct, using the 2026 "five workflow patterns" framing (Anthropic).
  中文翻译：使用 2026 年"五种工作流模式"框架（Anthropic），决定任务是应该用计划-执行还是交替 ReAct。
- Recognize when Plan-and-Act's synthetic plan data is needed for long-horizon web or mobile tasks.
  中文翻译：识别何时需要 Plan-and-Act 的合成计划数据来处理长程网页或移动任务。

## The Problem | 问题引入

ReAct's interleaved thought-action-observation loop is simple and flexible, but each tool call has to carry the full prior context — including every previous thought. Token usage grows quadratically with depth. Worse: when a tool fails mid-loop, the model has to re-derive the whole plan from the error observation.

> ReAct 的交替思考-行动-观察循环简单灵活，但每次工具调用都需要携带完整的前置上下文——包括之前的每一个思考。Token 用量随深度二次增长。更糟的是：当工具在循环中间失败时，模型必须从错误观察中重新推导整个计划。

ReWOO (Xu et al., arXiv:2305.18323, May 2023) noticed this and made a bet: plan the whole thing up front, fetch evidence in parallel, compose the answer at the end. One LLM call to plan, N tool calls for evidence (can be parallel), one LLM call to solve. The trade is less flexibility (the plan is static) for much better token efficiency and clearer failure modes.

> ReWOO（Xu 等人，arXiv:2305.18323，2023 年 5 月）注意到了这一点并提出一个方案：先规划整个任务，并行获取证据，最后组合答案。一次 LLM 调用来规划、N 次工具调用获取证据（可并行）、一次 LLM 调用来求解。代价是灵活性降低（计划是静态的），但换来更好的 token 效率和更清晰的失败模式。

## The Concept | 核心概念

### The three roles

```
Planner:  user_question -> [plan_dag]        # 规划器：将用户问题转为计划 DAG
Workers:  [plan_dag]     -> [evidence]        # 工作器：执行工具调用获取证据（可并行）
Solver:   user_question, plan_dag, evidence -> final_answer  # 求解器：组合证据生成最终答案
```

Planner produces a DAG. Each node names a tool, its arguments, and which earlier nodes it depends on (references like `#E1`, `#E2`). Workers execute nodes in topological order. Solver stitches everything together.

> 规划器生成一个 DAG。每个节点指定一个工具、其参数以及依赖的先前节点（如 `#E1`、`#E2` 等引用）。工作器按拓扑顺序执行节点。求解器将所有内容拼接在一起。

### Why 5x fewer tokens

ReAct grows prompt length linearly with step count. At step 10, the prompt contains thought 1 plus action 1 plus observation 1 plus thought 2 plus action 2 plus observation 2, and so on. Each intermediate step also redundantly includes the original prompt.

> ReAct 的提示长度随步数线性增长。到第 10 步时，提示包含思考 1 + 行动 1 + 观察 1 + 思考 2 + 行动 2 + 观察 2，依此类推。每个中间步骤还冗余地包含原始提示。

ReWOO pays one planner prompt (large), N small worker prompts (each just the tool call, no chain), and one solver prompt. On HotpotQA the paper measures ~5x fewer tokens while scoring +4 absolute accuracy.

> ReWOO 只需一次规划器提示（较大）、N 个小工作器提示（每个仅包含工具调用，无链式历史）和一次求解器提示。在 HotpotQA 上论文测得减少约 5 倍 token，同时准确率绝对提升 4%。

### Why it is more robust

If worker 3 fails in ReAct, the loop has to reason out of the error mid-stream. In ReWOO, worker 3 returns an error string; the solver sees it in context with the original plan and can degrade gracefully. Failure localization is per-node, not per-step.

> 如果工作器 3 在 ReAct 中失败，循环必须在流程中间从错误中推理。在 ReWOO 中，工作器 3 返回一个错误字符串；求解器在原始计划的上下文中看到它并可以优雅降级。故障定位是按节点的，不是按步骤的。

### Planner distillation

The paper's second result: because the planner does not see observations, you can fine-tune a 7B model on planner outputs from a 175B teacher. The small model handles planning; the big model is not needed at inference. This is now standard — many 2026 production agents use a small planner and a big executor or vice-versa.

> 论文的第二个成果：因为规划器不看到观察结果，你可以在 175B 教师模型的规划输出上微调一个 7B 模型。小模型处理规划；大模型在推理时不需要。这现在是标准做法——许多 2026 年的生产 Agent 使用小规划器和大执行器，反之亦然。

> **【拓展：规划器蒸馏 → 成本优化】** 因为规划器不需要观察结果，可以将 175B 教师模型的规划输出蒸馏到 7B 模型。2026 年的生产 Agent 普遍使用"小模型规划 + 大模型执行"的混合架构来优化成本。这也是 vLLM 等推理服务支持模型路由的理论基础。

### Plan-and-Execute (LangChain, 2023)

The LangChain team's August 2023 post generalized ReWOO into a pattern name: Plan-and-Execute. Up-front planner emits a step list, executor runs each step, an optional replanner can revise after observing results. This is closer to ReAct than ReWOO (the replanner brings observations back into planning) but preserves the token savings.

> LangChain 团队 2023 年 8 月的文章将 ReWOO 泛化为一个模式名称：Plan-and-Execute。前置规划器发出步骤列表，执行器运行每一步，可选的重新规划器可以在观察结果后修订。这比 ReWOO 更接近 ReAct（重新规划器将观察带回规划），但保留了 token 节省。

### Plan-and-Act (Erdogan et al., arXiv:2503.09572, ICML 2025)

Plan-and-Act scales the pattern to long-horizon web and mobile agents. The key contribution is synthetic plan data: a labeled trajectory generator produces training data where the plan is explicit. Used to fine-tune planner models that keep working past 30–50 steps on WebArena-like tasks where a single ReAct trajectory loses coherence.

> Plan-and-Act 将该模式扩展到长程网页和移动 Agent。关键贡献是合成计划数据：标注轨迹生成器产生训练数据，其中计划是显式的。用于微调规划器模型，使其在 WebArena 类任务上 30-50 步后仍能保持工作，而单一 ReAct 轨迹会失去连贯性。

### When to pick which

| Pattern | When | 适用场景 |
|---------|------|----------|
| ReAct | Short tasks, unknown environment, need reactive exception handling | 短任务、未知环境、需要响应式异常处理 |
| ReWOO | Structured tasks with known tools, token-sensitive, parallelizable evidence | 结构化任务、已知工具、Token 敏感、可并行 |
| Plan-and-Execute | Like ReWOO but with replanning after partial execution | 类似 ReWOO 但支持执行后重新规划 |
| Plan-and-Act | Long-horizon (>30 steps), web/mobile/computer-use | 长程任务(>30步)、网页/移动端/计算机使用 |
| Tree of Thoughts | Search is worth paying for (Lesson 04) | 值得付出搜索成本的场景 |

Anthropic's Dec 2024 guidance: start with the simplest. If the task is one tool call plus a summary, do not build ReWOO. If the task is a 40-step research assignment, do not do ReAct alone.

> Anthropic 2024 年 12 月的指导：从最简单的开始。如果任务是一个工具调用加一个摘要，不要构建 ReWOO。如果任务是 40 步的研究任务，不要只用 ReAct。

## Build It | 动手实现

`code/main.py` implements a toy ReWOO:

> `code/main.py` 实现了一个玩具 ReWOO：

- `Planner` — a scripted policy that emits a plan DAG from a prompt.
  中文翻译：`Planner`——从提示生成计划 DAG 的脚本策略。
- `Worker` — dispatches each node's tool call via the registry.
  中文翻译：`Worker`——通过注册表分派每个节点的工具调用。
- `Solver` — scripted composition that reads evidence and produces a final answer.
  中文翻译：`Solver`——读取证据并生成最终答案的脚本组合器。
- Dependency resolution — references like `#E1` are substituted with earlier worker outputs.
  中文翻译：依赖解析——如 `#E1` 的引用被替换为先前的工作器输出。

The demo answers "What is the population of the capital of France, rounded to millions?" using a two-step plan: (1) look up the capital, (2) look up the population, then solve.

> 演示回答"法国首都的人口是多少，四舍五入到百万？"使用两步计划：(1) 查找首都，(2) 查找人口，然后求解。

Run it:

> 运行：

```
python3 code/main.py
```

The trace shows the full plan first, then worker results, then solver composition. Compare the token count (we print a rough character count) to a ReAct-style interleaved run — ReWOO wins on this kind of structured task.

> 轨迹首先显示完整计划，然后是工作器结果，最后是求解器组合。比较 token 数量（我们打印粗略的字符数）与 ReAct 风格的交替运行——ReWOO 在这种结构化任务上获胜。

## Use It | 用框架实现

LangGraph ships Plan-and-Execute as a recipe (`create_react_agent` for ReAct, custom graphs for plan-execute). CrewAI's Flows encode the pattern directly: you define tasks up front and the Flow DAG executes them. Plan-and-Act's synthetic data approach is still mostly research; the runtime pattern (explicit plan DAG) ships in production through LangGraph and CrewAI Flows.

> LangGraph 将 Plan-and-Execute 作为配方提供（`create_react_agent` 用于 ReAct，自定义图用于计划-执行）。CrewAI 的 Flows 直接编码了该模式：你预先定义任务，Flow DAG 执行它们。Plan-and-Act 的合成数据方法仍主要在研究阶段；运行时模式（显式计划 DAG）通过 LangGraph 和 CrewAI Flows 在生产环境中使用。

## Ship It | 产出物

`outputs/skill-rewoo-planner.md` generates a ReWOO plan DAG from a user request, given a tool catalog. It validates the plan (acyclic, every reference resolved, every tool exists) before handing off to an executor.

> `outputs/skill-rewoo-planner.md` 根据用户请求和工具目录生成 ReWOO 计划 DAG。它在移交给执行器之前验证计划（无环、每个引用已解析、每个工具存在）。

## Exercises | 练习题

1. Parallelize worker execution for independent plan nodes. What does it buy you on a 6-node DAG with 2 parallel groups?
   中文翻译：将独立计划节点的工作器并行化。在 6 节点 DAG 中 2 组并行的情况下有什么收益？
2. Add a replanner node that fires if any worker returns an error. What is the smallest change to ReWOO that makes it Plan-and-Execute?
   中文翻译：添加一个在工作器返回错误时触发的重新规划节点。ReWOO 变成 Plan-and-Execute 的最小改动是什么？
3. Replace `Planner` with a small model (7B class) and keep `Solver` on a frontier model. Compare end-to-end quality — where does the split fail?
   中文翻译：用小模型（7B 级）替换规划器，保留前沿模型作为求解器。对比端到端质量——分裂在哪里失败？
4. Read Section 4 of the ReWOO paper on planner distillation. Reproduce the 175B -> 7B result conceptually: what training data do you need, and how do you score plan quality?
   中文翻译：阅读 ReWOO 论文第 4 节关于规划器蒸馏的内容。概念上重现 175B→7B 结果：需要什么训练数据？如何评估计划质量？
5. Port the toy to Plan-and-Act's trajectory shape: plan is a sequence, not a DAG. What tradeoffs change?
   中文翻译：将玩具系统移植为 Plan-and-Act 的轨迹形式：计划是序列而非 DAG。哪些权衡发生了变化？

## Key Terms | 术语速查表

| Term | What people say | What it actually means |
|------|-----------------|-----------------------|
| 术语 | 通俗说法 | 实际含义 |
| ReWOO | "Reasoning without observations" / "无观察推理" | Plan, then fetch evidence in parallel, then solve — no observations in the planning prompt / 先规划，再并行获取证据，最后求解——规划提示中不包含观察 |
| Plan-and-Execute | "LangChain's plan-execute pattern" / "LangChain 的计划-执行模式" | ReWOO with an optional replanner node after execution / 带可选重新规划节点的 ReWOO |
| Plan-and-Act | "Scaled plan-execute" / "扩展版计划-执行" | Explicit planner/executor split with synthetic plan training data for long-horizon tasks / 使用合成计划训练数据的长程任务显式规划器/执行器分离 |
| Evidence reference | "#E1, #E2, ..." / "证据引用" | Plan-node placeholder substituted with prior worker output at dispatch time / 计划节点占位符，在分派时替换为工作器输出 |
| Planner distillation | "Small planner, big executor" / "小规划器，大执行器" | Fine-tune a small model on planner traces from a large teacher / 用大模型的规划轨迹微调小模型 |
| Token efficiency | "Fewer round trips" / "更少往返" | 5x fewer tokens on HotpotQA vs ReAct in the paper / 论文中 HotpotQA 上比 ReAct 减少 5 倍 token |
| DAG executor | "Topological dispatcher" / "拓扑分派器" | Runs plan nodes in dependency order; parallel at each level / 按依赖顺序运行计划节点；每层可并行 |

## Further Reading | 延伸阅读

- [Xu et al., ReWOO: Decoupling Reasoning from Observations (arXiv:2305.18323)](https://arxiv.org/abs/2305.18323) — the canonical paper
  中文翻译：ReWOO 经典论文——将推理与观察解耦。
- [Erdogan et al., Plan-and-Act (arXiv:2503.09572)](https://arxiv.org/abs/2503.09572) — scaled planner-executor with synthetic plans
  中文翻译：Plan-and-Act——使用合成计划的扩展版规划器-执行器。
- [LangGraph Plan-and-Execute tutorial](https://docs.langchain.com/oss/python/langgraph/overview) — the framework recipe
  中文翻译：LangGraph Plan-and-Execute 教程——框架配方。
- [Anthropic, Building Effective Agents](https://www.anthropic.com/research/building-effective-agents) — pick the simplest pattern that works
  中文翻译：Anthropic 关于构建有效 Agent 的指导——选择最简单的可行模式。
