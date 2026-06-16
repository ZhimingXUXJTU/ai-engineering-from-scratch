# Planning with HTN and Evolutionary Search | 分层任务网络与进化搜索规划

> Symbolic planning handles the cases where the plan is provably correct. Evolutionary code search handles the cases where the fitness function is machine-checkable. ChatHTN (2025) and AlphaEvolve (2025) show what each unlocks when paired with an LLM.

> **【中文解读】** 符号规划处理计划可证明正确的场景。进化代码搜索处理适应度函数可机器检查的场景。ChatHTN（2025）和 AlphaEvolve（2025）展示了各自与 LLM 配合时解锁的能力。

**Type:** Build | **类型:** 构建
**Languages:** Python (stdlib) | **语言:** Python (标准库)
**Prerequisites:** Phase 14 · 02 (ReWOO and Plan-and-Execute) | **前置知识:** Phase 14 · 02 (ReWOO 与计划-执行)
**Time:** ~75 minutes | **时间:** ~75 分钟

## Learning Objectives | 学习目标

- Explain Hierarchical Task Networks: tasks, methods, operators, preconditions, effects.
  中文翻译：解释分层任务网络：任务、方法、操作符、前置条件、效果。
- Describe ChatHTN's hybrid loop — symbolic search with LLM fallback decomposition.
  中文翻译：描述 ChatHTN 的混合循环——带 LLM 回退分解的符号搜索。
- Explain AlphaEvolve's evolutionary loop and why it only works with a programmatic evaluator.
  中文翻译：解释 AlphaEvolve 的进化循环以及为什么它只在有程序化评估器时有效。
- Implement a toy HTN planner plus a toy evolutionary search in stdlib.
  中文翻译：用标准库实现玩具 HTN 规划器和玩具进化搜索。

## The Problem | 问题引入

ReWOO (Lesson 02), Plan-and-Execute, and ReAct cover most agent planning. Two cases they don't cover well:

> ReWOO（第 2 课）、Plan-and-Execute 和 ReAct 覆盖了大多数 Agent 规划。两种它们不能很好覆盖的情况：

1. **Plans with provable correctness.** Scheduling, flight pathing, compliance workflows — the plan must be sound by construction. A fluent LLM plan that sometimes hallucinates a step is unacceptable.
   中文翻译：**可证明正确性的计划。** 调度、航线规划、合规工作流——计划必须在构造上就是可靠的。一个偶尔幻觉步骤的流利 LLM 计划是不可接受的。
2. **Optimizations with a machine-checkable fitness function.** Matrix multiplication, scheduling heuristics, compiler passes — the goal is not "a correct plan" but "the best plan."
   中文翻译：**有机器可检查适应度函数的优化。** 矩阵乘法、调度启发式、编译器 pass——目标不是"一个正确的计划"而是"最优计划"。

> **【中文解读】** Agent 规划的两种主要范式：分层任务网络（HTN）和进化规划。HTN 将高层目标递归分解为可执行的子任务，适合结构化领域。进化规划使用遗传算法优化计划种群，适合开放世界探索。

HTN planning and AlphaEvolve solve the two different problems. Both use LLMs as amplifiers, not replacements.

> HTN 规划和 AlphaEvolve 解决两个不同的问题。两者都将 LLM 用作放大器而非替代品。

> **【拓展：2026 年 Agent 规划的前沿】** AlphaEvolve 和 Darwin-Godel Machine 将进化算法应用于 Agent 自身的策略优化——不仅是规划任务，更是规划和优化规划过程本身。HTN 在传统 AI 中已成熟数十年，但在 LLM Agent 中的应用仍是一个活跃的研究方向。

> 🔗 **【前置】** 必须先过 Phase 14·02（ReWOO/Plan-and-Execute）——HTN 是其"严格形式化"版本；以及基本的经典 AI 规划知识（状态、前置条件、效果）。如果你没听过 STRIPS 或 PDDL，建议先补一两节"经典符号 AI"教程——本节的"可证明正确性"依赖这套形式化语言。

## The Concept | 核心概念

### Hierarchical Task Networks

An HTN is:

> HTN 是：

- **Tasks** — compound (to be decomposed) and primitive (directly executable).
  中文翻译：**任务**——复合（待分解）和原始（直接可执行）。
- **Methods** — ways to decompose a compound task into subtasks, with preconditions.
  中文翻译：**方法**——将复合任务分解为子任务的方式，带前置条件。
- **Operators** — primitive actions with preconditions and effects.
  中文翻译：**操作符**——带前置条件和效果的原始动作。
- **State** — a set of facts.
  中文翻译：**状态**——一组事实。

Planning: given a goal task and an initial state, find a decomposition into primitive operators whose preconditions are satisfied in sequence.

> 规划：给定目标任务和初始状态，找到一个分解为原始操作符的方案，其前置条件按序满足。

HTN is older than LLMs and still the reference for provably-correct plans.

> HTN 比 LLM 更古老，仍然是可证明正确计划的参考。

### ChatHTN (Gopalakrishnan et al., 2025)

ChatHTN (arXiv:2505.11814) interleaves symbolic HTN with LLM queries:

> ChatHTN（arXiv:2505.11814）交替进行符号 HTN 和 LLM 查询：

1. Try to decompose the current compound task with existing methods.
   中文翻译：尝试用现有方法分解当前复合任务。
2. If no method applies, ask the LLM: "how would you decompose `task` in state `s`?"
   中文翻译：如果没有方法适用，问 LLM："在状态 `s` 中你会如何分解 `task`？"
3. Translate the LLM response into candidate subtasks.
   中文翻译：将 LLM 响应翻译为候选子任务。
4. Validate against the operator schema; reject invalid decompositions.
   中文翻译：对照操作符模式验证；拒绝无效分解。
5. Recurse.
   中文翻译：递归。

The paper's central claim: every plan produced is provably sound because LLM suggestions only enter as candidate decompositions, never as direct plan edits. The symbolic layer owns correctness; the LLM expands the method library.

> 💡 **【类比】** ChatHTN 像严格的审计员（符号层）+ 创意实习生（LLM）。实习生提建议："我觉得这个目标可以这样分解..."审计员严格检查："你的子任务的前置条件在当前状态下是否成立？效果是否符合 operator schema？" 不符合就拒绝，符合才采纳。**结果**：所有最终采纳的计划都被审计过，可靠性有保证。LLM 是"建议者"而非"决策者"。

> 论文的核心主张：每个产生的计划都可证明是可靠的，因为 LLM 建议只作为候选分解进入，从不作为直接计划编辑。符号层拥有正确性；LLM 扩展方法库。

Online method learning (OpenReview `gwYEDY9j2x`, 2025 follow-up) adds a learner that generalizes LLM-produced decompositions by regression — cutting LLM query frequency up to 75%.

> 在线方法学习（2025 年后续研究）添加了通过回归泛化 LLM 产生分解的学习器——将 LLM 查询频率降低最多 75%。

### AlphaEvolve (Novikov et al., 2025)

AlphaEvolve (arXiv:2506.13131, DeepMind, June 2025) is a different beast: evolutionary code search orchestrated by a Gemini 2.0 Flash/Pro ensemble.

> AlphaEvolve（arXiv:2506.13131，DeepMind，2025 年 6 月）是一个不同的存在：由 Gemini 2.0 Flash/Pro 集群编排的进化代码搜索。

Loop:

> 循环：

1. Start with a seed program + a programmatic evaluator (returns a fitness score).
   中文翻译：从种子程序 + 程序化评估器（返回适应度分数）开始。
2. Ensemble of LLMs proposes mutations.
   中文翻译：LLM 集群提出变异。
3. Run mutations through the evaluator.
   中文翻译：通过评估器运行变异。
4. Keep the best; mutate again.
   中文翻译：保留最好的；再次变异。

Published wins:

> 已发表成果：

- First improvement over Strassen for 4x4 complex matrix multiplication in 56 years (48 scalar multiplications).
  中文翻译：56 年来首次改进 4x4 复矩阵乘法的 Strassen 算法（48 次标量乘法）。
- 0.7% recovered Google compute via a Borg scheduling heuristic.
  中文翻译：通过 Borg 调度启发式回收 0.7% 的 Google 计算资源。
- 32% FlashAttention speedup on a frontier workload.
  中文翻译：在前沿工作负载上 FlashAttention 加速 32%。

The hard constraint: the fitness function must be machine-checkable. Evolutionary search over prose answers does not converge.

> ⚠️ **【易错点】** 把 AlphaEvolve 套到"创意写作优化"上——让 LLM 用进化算法改写小说，用 LLM 评分作为 fitness。**后果**：完全不会收敛，因为 fitness 函数本身是 LLM（随机+不稳定），同一篇小说跑两次得分可能差 30%。**一行修复**：只对"有客观指标的程序化任务"用 AlphaEvolve（代码性能、测试覆盖率、调度效率），创意类任务退回 Self-Refine/CRITIC。

> 硬约束：适应度函数必须是机器可检查的。对文本答案的进化搜索不会收敛。

### When to use which

| Problem class | Use | Why |
|---------------|-----|-----|
| 问题类别 | 使用 | 原因 |
| Scheduling with hard constraints | HTN + ChatHTN | Provable soundness / 可证明的可靠性 |
| Compiler optimization | AlphaEvolve | Machine-checkable fitness / 机器可检查的适应度 |
| Multi-step task execution | ReAct / ReWOO | LLM in the loop, no formal guarantees / LLM 在循环中，无形式化保证 |
| Code improvement with tests | AlphaEvolve | Tests are the evaluator / 测试即评估器 |
| Policy-bound automation | HTN | Preconditions encode policy / 前置条件编码策略 |

### Where this pattern goes wrong

- **HTN without operators.** Without precondition/effect schemas the soundness claim collapses. ChatHTN's "LLM suggests decomposition" requires the schema to reject invalid moves.
  中文翻译：**没有操作符的 HTN。** 没有前置条件/效果模式，可靠性声明就崩塌了。ChatHTN 的"LLM 建议分解"需要模式来拒绝无效动作。
- **AlphaEvolve without a real evaluator.** "Ask the LLM if the code is better" is not a fitness function. The evaluator must be deterministic and fast.
  中文翻译：**没有真正评估器的 AlphaEvolve。** "问 LLM 代码是否更好"不是适应度函数。评估器必须是确定性和快速的。
- **Over-engineering.** Most agent tasks don't need either. Reach for ReAct or ReWOO first.
  中文翻译：**过度工程。** 大多数 Agent 任务不需要任何一个。先使用 ReAct 或 ReWOO。

> 🤔 **【困惑】** Q: ChatHTN 论文说"LLM 只提建议不直接进计划"——这跟 LangChain Agent 调用工具不是一回事吗？ A: 不一样。普通 Agent 里 LLM 决定调用哪个工具就直接执行了，没人验证"调用这个工具在当前状态是否合法"。ChatHTN 强制 LLM 提议后经过符号层的 precondition 检查——只有 precondition 满足才执行。这个"强制审计"层就是"可证明可靠性"的来源，普通 Agent 没有这层。

## Build It | 动手构建

`code/main.py` implements two toys:

> `code/main.py` 实现了两个玩具：

- A stdlib HTN planner with operators, methods, preconditions, effects, and a `LLMFallback` that kicks in when no method matches a compound task. The "LLM" is a scripted decomposer so the planner runs offline.
  中文翻译：一个标准库 HTN 规划器，带操作符、方法、前置条件、效果和当没有方法匹配复合任务时触发的 `LLMFallback`。"LLM" 是一个脚本分解器，规划器可离线运行。
- A stdlib evolutionary search over arithmetic programs: grow expressions whose output minimizes `|f(x) - target|` over a test set. Evaluator is deterministic.
  中文翻译：一个标准库进化搜索，在算术程序上：生长使 `|f(x) - target|` 在测试集上最小的表达式。评估器是确定性的。

Run it:

> 运行：

```
python3 code/main.py
```

The trace shows the HTN planner decomposing a compound task (with a mid-plan LLM fallback) and the evolutionary loop converging on a target expression.

> 轨迹显示 HTN 规划器分解复合任务（带中途 LLM 回退）和进化循环收敛到目标表达式。

## Use It | 用框架实现

- **HTN planners** — `pyhop`, `SHOP3`, or build your own for domain-specific policy enforcement.
  中文翻译：**HTN 规划器**——`pyhop`、`SHOP3`，或为领域特定策略执行自己构建。
- **ChatHTN** — research code; the pattern (symbolic + LLM fallback) ports cleanly to any HTN planner.
  中文翻译：**ChatHTN**——研究代码；模式（符号 + LLM 回退）可干净地移植到任何 HTN 规划器。
- **AlphaEvolve** — DeepMind paper; the pattern (ensemble + evaluator) is reproducible. OpenEvolve and similar open-source forks are emerging.
  中文翻译：**AlphaEvolve**——DeepMind 论文；模式（集群 + 评估器）可复现。OpenEvolve 和类似开源分支正在涌现。
- **Agent frameworks** — none ship first-class HTN or AlphaEvolve yet. Build it as a subagent or a background worker.
  中文翻译：**Agent 框架**——目前没有一个内置 HTN 或 AlphaEvolve。将其构建为子 Agent 或后台工作者。

## Ship It | 产出物

`outputs/skill-hybrid-planner.md` generates a hybrid planner scaffold (HTN or evolutionary) with the LLM role explicitly scoped.

> `outputs/skill-hybrid-planner.md` 生成混合规划器脚手架（HTN 或进化），LLM 角色显式限定。

## Exercises | 练习题

1. Extend the HTN planner with backtracking: when an operator's postcondition fails at runtime, roll back and try the next method.
   中文翻译：为 HTN 规划器添加回溯：当操作符的后置条件在运行时失败时，回滚并尝试下一个方法。
2. Add a LLM-method cache to ChatHTN: when the LLM decomposes task `T` in state pattern `P`, store the result. Re-check the method library first on the next call.
   中文翻译：为 ChatHTN 添加 LLM 方法缓存：当 LLM 在状态模式 `P` 中分解任务 `T` 时，存储结果。下次调用时先重新检查方法库。
3. Swap the evolutionary search evaluator to a real test suite. Evolve a sort function that passes 20 test cases; report generations to convergence.
   中文翻译：将进化搜索评估器替换为真实测试套件。进化一个通过 20 个测试用例的排序函数；报告收敛代数。
4. Read AlphaEvolve's evaluator design notes. Design an evaluator for a domain you care about (SQL query optimization, test-suite minimization, deployment YAML).
   中文翻译：阅读 AlphaEvolve 的评估器设计笔记。为你关心的领域设计一个评估器（SQL 查询优化、测试套件最小化、部署 YAML）。
5. Combine: use HTN to decompose a compound task into subtasks, then use evolutionary search on each subtask's primitive operator. Where does it shine, where does it over-engineer?
   中文翻译：组合使用：用 HTN 分解复合任务为子任务，然后对每个子任务的原始操作符使用进化搜索。哪里出色，哪里过度工程？

## Key Terms | 术语速查表

| Term | What people say | What it actually means |
|------|-----------------|-----------------------|
| 术语 | 通俗说法 | 实际含义 |
| HTN | "Hierarchical planner" / "分层规划器" | Task decomposition with operators, preconditions, effects / 带操作符、前置条件、效果的任务分解 |
| Method | "Decomposition rule" / "分解规则" | Way to break a compound task into subtasks / 将复合任务分解为子任务的方式 |
| Operator | "Primitive action" / "原始动作" | Concrete step with precondition and effect / 带前置条件和效果的具体步骤 |
| ChatHTN | "LLM + HTN" / "LLM + HTN" | Symbolic planner asks LLM when no method matches / 符号规划器在没有方法匹配时询问 LLM |
| AlphaEvolve | "Evolutionary code search" / "进化代码搜索" | Ensemble LLMs mutate code; deterministic evaluator selects / LLM 集群变异代码；确定性评估器选择 |
| Fitness function | "Evaluator" / "评估器" | Deterministic, machine-checkable score over outputs / 输出上的确定性、机器可检查分数 |
| Online method learning | "Cached LLM decomposition" / "缓存的 LLM 分解" | Store + generalize LLM plans to cut query cost / 存储并泛化 LLM 计划以降低查询成本 |

## Further Reading | 延伸阅读

- [Gopalakrishnan et al., ChatHTN (arXiv:2505.11814)](https://arxiv.org/abs/2505.11814) — symbolic + LLM hybrid planner
  中文翻译：ChatHTN 论文——符号 + LLM 混合规划器。
- [Novikov et al., AlphaEvolve (arXiv:2506.13131)](https://arxiv.org/abs/2506.13131) — evolutionary code search with LLM mutations
  中文翻译：AlphaEvolve 论文——带 LLM 变异的进化代码搜索。
- [Anthropic, Building Effective Agents](https://www.anthropic.com/research/building-effective-agents) — when to reach for a planner vs a simple loop
  中文翻译：Anthropic 关于构建有效 Agent 的指导——何时使用规划器而非简单循环。
