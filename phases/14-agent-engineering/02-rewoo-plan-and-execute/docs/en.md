# ReWOO and Plan-and-Execute: Decoupled Planning | ReWOO 与计划-执行模式：解耦规划

> ReAct interleaves thought and action in one stream. ReWOO separates them: one big plan up front, then execute. 5x fewer tokens, +4% accuracy on HotpotQA, and you can distill the planner into a 7B model. Plan-and-Execute generalized it; Plan-and-Act scaled it to web navigation.

> **【中文解读】** ReAct 在一个流中交替思考和行动。ReWOO 将它们分离：先一次性制定完整计划，然后执行。Token 消耗减少 5 倍，HotpotQA 准确率提升 4%，还可以将规划器蒸馏到 7B 模型。Plan-and-Execute 是其泛化版本，Plan-and-Act 将其扩展到网页导航。

> **【拓展：ReWOO → 现代 Agent 架构】** Anthropic 的 "Building Effective Agents" 博文推荐的五种工作流模式中，计划-执行模式是核心之一。2026 年的生产级 Agent（如 Devin、Claude Code 的多步骤任务）都采用类似模式——先规划、再执行、最后整合结果。

**Type:** Build
**Languages:** Python (stdlib)
**Prerequisites:** Phase 14 · 01 (Agent Loop)
**Time:** ~60 minutes

## Learning Objectives

- Explain why ReWOO's Planner / Worker / Solver split saves tokens and improves robustness over ReAct's interleaved loop.
- Implement a plan DAG, a dependency-ordered executor, and a solver that composes worker outputs — all stdlib.
- Decide when a task should run as plan-then-execute vs interleaved ReAct, using the 2026 "five workflow patterns" framing (Anthropic).
- Recognize when Plan-and-Act's synthetic plan data is needed for long-horizon web or mobile tasks.

## The Problem | 问题

ReAct's interleaved thought-action-observation loop is simple and flexible, but each tool call has to carry the full prior context — including every previous thought. Token usage grows quadratically with depth. Worse: when a tool fails mid-loop, the model has to re-derive the whole plan from the error observation.

ReWOO (Xu et al., arXiv:2305.18323, May 2023) noticed this and made a bet: plan the whole thing up front, fetch evidence in parallel, compose the answer at the end. One LLM call to plan, N tool calls for evidence (can be parallel), one LLM call to solve. The trade is less flexibility (the plan is static) for much better token efficiency and clearer failure modes.

> **【中文解读】** ReAct 的交替循环虽然简单灵活，但每次工具调用都需要携带完整的历史上下文，Token 用量随深度二次增长。ReWOO 的方案是：先一次性规划，然后并行获取证据，最后组合答案。代价是灵活性降低（计划是静态的），但换来更好的 Token 效率和更清晰的失败模式。

## The Concept | 核心概念

### The three roles

```
Planner:  user_question -> [plan_dag]        # 规划器：将用户问题转为计划 DAG
Workers:  [plan_dag]     -> [evidence]        # 工作器：执行工具调用获取证据（可并行）
Solver:   user_question, plan_dag, evidence -> final_answer  # 求解器：组合证据生成最终答案
```

Planner produces a DAG. Each node names a tool, its arguments, and which earlier nodes it depends on (references like `#E1`, `#E2`). Workers execute nodes in topological order. Solver stitches everything together.

### Why 5x fewer tokens

ReAct grows prompt length linearly with step count. At step 10, the prompt contains thought 1 plus action 1 plus observation 1 plus thought 2 plus action 2 plus observation 2, and so on. Each intermediate step also redundantly includes the original prompt.

ReWOO pays one planner prompt (large), N small worker prompts (each just the tool call, no chain), and one solver prompt. On HotpotQA the paper measures ~5x fewer tokens while scoring +4 absolute accuracy.

> **【中文解读】** ReAct 的提示长度随步数线性增长——第 10 步时包含前面所有思考、行动和观察。ReWOO 只需：一次规划器提示（较大）、N 个小工作器提示（仅工具调用）、一次求解器提示。在 HotpotQA 上 Token 减少 5 倍，准确率反而提升 4%。

### Why it is more robust

If worker 3 fails in ReAct, the loop has to reason out of the error mid-stream. In ReWOO, worker 3 returns an error string; the solver sees it in context with the original plan and can degrade gracefully. Failure localization is per-node, not per-step.

### Planner distillation

The paper's second result: because the planner does not see observations, you can fine-tune a 7B model on planner outputs from a 175B teacher. The small model handles planning; the big model is not needed at inference. This is now standard — many 2026 production agents use a small planner and a big executor or vice-versa.

> **【拓展：规划器蒸馏 → 成本优化】** 因为规划器不需要观察结果，可以将 175B 教师模型的规划输出蒸馏到 7B 模型。2026 年的生产 Agent 普遍使用"小模型规划 + 大模型执行"的混合架构来优化成本。这也是 vLLM 等推理服务支持模型路由的理论基础。

### Plan-and-Execute (LangChain, 2023)

The LangChain team's August 2023 post generalized ReWOO into a pattern name: Plan-and-Execute. Up-front planner emits a step list, executor runs each step, an optional replanner can revise after observing results. This is closer to ReAct than ReWOO (the replanner brings observations back into planning) but preserves the token savings.

### Plan-and-Act (Erdogan et al., arXiv:2503.09572, ICML 2025)

Plan-and-Act scales the pattern to long-horizon web and mobile agents. The key contribution is synthetic plan data: a labeled trajectory generator produces training data where the plan is explicit. Used to fine-tune planner models that keep working past 30–50 steps on WebArena-like tasks where a single ReAct trajectory loses coherence.

### When to pick which

| Pattern | When | 适用场景 |
|---------|------|----------|
| ReAct | Short tasks, unknown environment, need reactive exception handling | 短任务、未知环境、需要响应式异常处理 |
| ReWOO | Structured tasks with known tools, token-sensitive, parallelizable evidence | 结构化任务、已知工具、Token 敏感、可并行 |
| Plan-and-Execute | Like ReWOO but with replanning after partial execution | 类似 ReWOO 但支持执行后重新规划 |
| Plan-and-Act | Long-horizon (>30 steps), web/mobile/computer-use | 长程任务(>30步)、网页/移动端/计算机使用 |
| Tree of Thoughts | Search is worth paying for (Lesson 04) | 值得付出搜索成本的场景 |

Anthropic's Dec 2024 guidance: start with the simplest. If the task is one tool call plus a summary, do not build ReWOO. If the task is a 40-step research assignment, do not do ReAct alone.

## Build It | 动手实现

`code/main.py` implements a toy ReWOO:

- `Planner` — a scripted policy that emits a plan DAG from a prompt.
- `Worker` — dispatches each node's tool call via the registry.
- `Solver` — scripted composition that reads evidence and produces a final answer.
- Dependency resolution — references like `#E1` are substituted with earlier worker outputs.

The demo answers "What is the population of the capital of France, rounded to millions?" using a two-step plan: (1) look up the capital, (2) look up the population, then solve.

Run it:

```
python3 code/main.py
```

The trace shows the full plan first, then worker results, then solver composition. Compare the token count (we print a rough character count) to a ReAct-style interleaved run — ReWOO wins on this kind of structured task.

## Use It | 用框架实现

LangGraph ships Plan-and-Execute as a recipe (`create_react_agent` for ReAct, custom graphs for plan-execute). CrewAI's Flows encode the pattern directly: you define tasks up front and the Flow DAG executes them. Plan-and-Act's synthetic data approach is still mostly research; the runtime pattern (explicit plan DAG) ships in production through LangGraph and CrewAI Flows.

## Ship It | 产出物

`outputs/skill-rewoo-planner.md` generates a ReWOO plan DAG from a user request, given a tool catalog. It validates the plan (acyclic, every reference resolved, every tool exists) before handing off to an executor.

## Exercises | 练习题

1. Parallelize worker execution for independent plan nodes. What does it buy you on a 6-node DAG with 2 parallel groups?
   *将独立计划节点的工作器并行化。在 6 节点 DAG 中 2 组并行的情况下有什么收益？*
2. Add a replanner node that fires if any worker returns an error. What is the smallest change to ReWOO that makes it Plan-and-Execute?
   *添加一个在工作器返回错误时触发的重新规划节点。ReWOO 变成 Plan-and-Execute 的最小改动是什么？*
3. Replace `Planner` with a small model (7B class) and keep `Solver` on a frontier model. Compare end-to-end quality — where does the split fail?
   *用小模型(7B)替换规划器，保留前沿模型作为求解器。对比端到端质量——分裂在哪里失败？*
4. Read Section 4 of the ReWOO paper on planner distillation. Reproduce the 175B -> 7B result conceptually: what training data do you need, and how do you score plan quality?
   *阅读 ReWOO 论文第 4 节关于规划器蒸馏的内容。概念上重现 175B→7B 结果：需要什么训练数据？如何评估计划质量？*
5. Port the toy to Plan-and-Act's trajectory shape: plan is a sequence, not a DAG. What tradeoffs change?
   *将玩具系统移植为 Plan-and-Act 的轨迹形式：计划是序列而非 DAG。哪些权衡发生了变化？*

## Key Terms | 关键术语

| Term | What people say | What it actually means | 中文释义 |
|------|----------------|------------------------|----------|
| ReWOO | "Reasoning without observations" | Plan, then fetch evidence in parallel, then solve — no observations in the planning prompt | 无观察推理——规划时不依赖观察结果 |
| Plan-and-Execute | "LangChain's plan-execute pattern" | ReWOO with an optional replanner node after execution | 计划-执行模式——带可选重新规划的 ReWOO |
| Plan-and-Act | "Scaled plan-execute" | Explicit planner/executor split with synthetic plan training data for long-horizon tasks | 计划-行动——使用合成计划训练数据的长程任务模式 |
| Evidence reference | "#E1, #E2, ..." | Plan-node placeholder substituted with prior worker output at dispatch time | 证据引用——计划节点占位符，在分派时替换为工作器输出 |
| Planner distillation | "Small planner, big executor" | Fine-tune a small model on planner traces from a large teacher | 规划器蒸馏——用大模型的规划输出训练小模型 |
| Token efficiency | "Fewer round trips" | 5x fewer tokens on HotpotQA vs ReAct in the paper | Token 效率——比 ReAct 减少 5 倍 Token |
| DAG executor | "Topological dispatcher" | Runs plan nodes in dependency order; parallel at each level | DAG 执行器——按依赖顺序运行计划节点 |

## Further Reading | 延伸阅读

- [Xu et al., ReWOO: Decoupling Reasoning from Observations (arXiv:2305.18323)](https://arxiv.org/abs/2305.18323) — the canonical paper
- [Erdogan et al., Plan-and-Act (arXiv:2503.09572)](https://arxiv.org/abs/2503.09572) — scaled planner-executor with synthetic plans
- [LangGraph Plan-and-Execute tutorial](https://docs.langchain.com/oss/python/langgraph/overview) — the framework recipe
- [Anthropic, Building Effective Agents](https://www.anthropic.com/research/building-effective-agents) — pick the simplest pattern that works
