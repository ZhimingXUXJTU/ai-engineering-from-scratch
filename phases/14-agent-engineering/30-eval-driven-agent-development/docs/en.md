# Eval-Driven Agent Development | 开发 驱动 评估

> Anthropic's guidance: "start with simple prompts, optimize them with comprehensive evaluation, and add multi-step agentic systems only when needed." Evaluation is not the last step. It's the outer loop that drives every other choice in Phase 14.

**Type:** Learn + Build | **类型:** 构建
**Languages:** Python (stdlib) | **语言:** Python (标准库)
**Prerequisites:** All of Phase 14. | **前置知识:** 见原文
**Time:** ~60 minutes | **时间:** 见原文

> 🔗 **【前置】** 学本节前请先掌握：Phase 14·01-29 全部——本节是 Phase 14 的综合应用。还需要 Phase 11·10（Evaluation）的基础。本节是 Phase 14·26（Failure Modes）的"预防版"——用 eval 提前发现失败模式。

## Learning Objectives | 学习目标

- Name the three evaluation layers — static benchmarks, custom offline, online production — and what each is for.
- Explain the evaluator-optimizer tight loop.
- Describe the 2026 best practice: evals live next to code, run in CI, gate PRs.
- Connect every Phase 14 lesson to the eval case it generates.

## The Problem | 问题引入

Agents pass demos. They fail in production in ways demos cannot predict. Benchmarks answer "is this model broadly capable?" not "is this agent shipping the right patches for my product?" The answer: evaluation at three layers, running continuously, with every guardrail and learned rule mapped to an eval case.

> 💡 **【类比】** Agent eval 像给运动员做体检——3 个层级：(1) **静态基准**（SWE-bench、BFCL）=国家体能测试，比平均水平；(2) **定制离线 eval**=针对你的项目设计（如"修这种 bug 的成功率"）=队内训练赛；(3) **在线生产 eval**=真实用户反馈=A/B 测试。三层缺一不可——只看基准会过拟合，只看生产反馈周期太长。

> ⚠️ **【易错点】** Agent eval 的 3 个坑：(1) **只测 happy path**——eval 集全是简单查询，复杂情况没覆盖；务必构造 adversarial 测试（模糊指令、攻击、边界值）。(2) **eval 不进 CI**——开发时手工跑一次就过，上线后没人跑；eval 必须进 GitHub Actions，PR 不过 eval 不能合并。(3) **eval 集污染**——eval 数据混进 prompt 的 few-shot 示例，分数虚高；eval 数据严格隔离。

> Agent 通过了演示。它们在生产中以演示无法预测的方式失败。基准回答的是"这个模型是否有广泛的能力？"而不是"这个 Agent 是否在为我的产品交付正确的补丁？"答案是：三层评估，持续运行，每个护栏和学习规则都映射到一个评估用例。


> **【中文解读】** 评估驱动的 Agent 开发（Eval-Driven Development）将传统软件工程中的 TDD 应用于 Agent：先定义评估标准，再实现 Agent。核心挑战是 Agent 的非确定性——同样的输入可能产生不同的执行路径和输出，需要基于轨迹的评估而非基于快照的评估。

> **{【拓展：Eval-Driven Agent Development 是 2025-2026 年的最佳实践。核...】}** Eval-Driven Agent Development 是 2025-2026 年的最佳实践。核心工具：(1) AgentOps——Agent 追踪和评估平台；(2) LangSmith——LangChain 的评估套件；(3) Braintrust——AI 评估框架。关键洞察：Agent 评估应该基于完整轨迹（trajectory）而非最终输出——两个 Agent 可能得到相同结果，但一个走了 5 步，另一个走了 50 步，质量和成本差异巨大。
## The Concept | 核心概念

### Three evaluation layers

1. **Static benchmarks** — SWE-bench Verified for code (Lesson 19), WebArena/OSWorld for browsing / desktop (Lesson 20), GAIA for generalist (Lesson 19), BFCL V4 for tool use (Lesson 06). Use for cross-model comparison and regression gating. Contamination is real: SWE-bench+ found 32.67% solution leakage. Always report Verified / +-audited scores.

2. **Custom offline evals** — your product's shape:
   - LLM-as-judge (Langfuse, Phoenix, Opik — Lesson 24).
   - Execution-based (run the patch, check tests).
   - Trajectory-based (compare action sequences against gold; OSWorld-Human shows top agents 1.4-2.7x over gold).

3. **Online evals** — production:
   - Session replays (Langfuse).
   - Guardrail-triggered alerts (Lesson 16, 21).
   - Per-step cost / latency tracking (Lesson 23 OTel spans).

### Evaluator-optimizer (Anthropic)

The tight loop:

1. Proposer generates output.
2. Evaluator judges.
3. Refine until evaluator passes.

This is Self-Refine (Lesson 05) generalized. Any agent flow you care about can wrap in evaluator-optimizer for reliability.

> 这是 Self-Refine（第 5 课）的泛化。你关心的任何 Agent 流程都可以用评估器-优化器包裹以提高可靠性。

> 评估驱动的 Agent 开发（Eval-Driven Development）将评估作为 Agent 开发的核心。先定义评估标准，再构建 Agent，用评估轨迹指导改进。

### 2026 best practice

- Evals live next to code.
- Run in CI on every PR.
- Gate merge on eval scores (e.g. "no regression > 5% vs main").
- Every guardrail maps to an eval case.
- Every learned rule (Reflexion, pro-workflow learn-rule) maps to a failure case.

### Tying Phase 14 together

Every lesson in Phase 14 generates eval cases:

| Lesson | Eval case it generates |
|--------|------------------------|
| 01 Agent Loop | Budget-exhausted, infinite-loop guard |
| 02 ReWOO | Planner replans correctly when a tool fails |
| 03 Reflexion | Learned reflections apply on retry |
| 05 Self-Refine/CRITIC | Judge passes refined output |
| 06 Tool Use | Argument coercion works; unknown tools rejected |
| 07-10 Memory | Retrieval citations match sources; stale facts invalidate |
| 12 Workflow Patterns | Each pattern produces correct output |
| 13 LangGraph | Resume reproduces state exactly |
| 14 AutoGen Actors | DLQ catches crashed handlers |
| 16 OpenAI Agents SDK | Guardrail trips on the right inputs |
| 17 Claude Agent SDK | Subagent results return to orchestrator |
| 19-20 Benchmarks | SWE-bench Verified score, WebArena success rate, OSWorld efficiency |
| 21 Computer Use | Per-step safety catches injected DOM |
| 23 OTel | Spans emit required attributes |
| 26 Failure Modes | Detectors tag known failures |
| 27 Prompt Injection | PVE refuses poisoned retrievals |
| 28 Orchestration | Supervisor routes to the right specialist |
| 29 Runtime Shapes | DLQ handles N% failure |

If your eval suite has cases for each, you have covered Phase 14.

> 如果你的评估套件有每个课程的用例，你就覆盖了 Phase 14。

> 评估驱动的 Agent 开发（Eval-Driven Development）将评估作为 Agent 开发的核心。先定义评估标准，再构建 Agent，用评估轨迹指导改进。

### Where eval-driven development fails

- **No baseline.** Evals without a last-known-good are unreadable. Store baselines.
- **LLM-judge without grounding.** Judges hallucinate too. CRITIC pattern (Lesson 05) — judge grounds on external tools.
- **Over-fitting to evals.** Optimizing for the eval diverges from production usefulness. Rotate cases.
- **Flaky evals.** Non-deterministic cases cause false alarms. Pin seeds, snapshot state.

> **没有基线。** 没有最后已知良好状态的评估是不可读的。存储基线。
> **LLM 评审器没有基础。** 评审器也会幻觉。CRITIC 模式（第 5 课）——评审器基于外部工具。
> **过拟合评估。** 为评估优化会偏离生产实用性。轮换用例。
> **不稳定的评估。** 非确定性用例导致误报。固定种子，快照状态。

## Build It | 动手实现

`code/main.py` is a stdlib eval harness:

- Case registry with categories (benchmark, custom, online).
- A scripted agent under test.
- Evaluator-optimizer loop: propose, judge, refine until pass or max rounds.
- CI gate: aggregate pass rate + regression against baseline.

Run it:

```
python3 code/main.py
```

Output: per-case pass/fail, regression flag, CI gate verdict.

> 输出：每用例通过/失败、回归标志、CI 门控裁定。

> 评估驱动的 Agent 开发（Eval-Driven Development）将评估作为 Agent 开发的核心。先定义评估标准，再构建 Agent，用评估轨迹指导改进。

## Use It | 用框架实现

- Write eval cases in the same repo as your agent code.
- Run them on every PR via CI.
- Fail the build on regression.
- Track pass rate over time.
- Tie every production failure to a new case.

## Ship It | 产出物

`outputs/skill-eval-suite.md` builds a three-layer eval suite for an agent product with CI gates and regression tracking.

> `outputs/skill-eval-suite.md` 为 Agent 产品构建三层评估套件，包含 CI 门控和回归追踪。

> 评估驱动的 Agent 开发（Eval-Driven Development）将评估作为 Agent 开发的核心。先定义评估标准，再构建 Agent，用评估轨迹指导改进。

## Exercises | 练习题

1. Take one of your production failures. Write an eval case that reproduces it. Does your agent pass it now?
  中文翻译：思考并实践此练习。
2. Build an LLM-judge rubric for your domain with three dimensions (factual, tone, scope). Score 50 sessions.
  中文翻译：思考并实践此练习。
3. Wire the eval suite into CI. Fail the build on >=5% regression.
  中文翻译：思考并实践此练习。
4. Add a trajectory-efficiency metric: how many steps did the agent take vs a gold trajectory?
  中文翻译：思考并实践此练习。
5. Map every Phase 14 lesson to an eval case in your suite. Any missing? That's a gap to close.
  中文翻译：思考并实践此练习。

## Key Terms | 术语速查表

| Term | What people say | What it actually means |
|------|----------------|------------------------|---|
| Static benchmark | "Off-the-shelf eval" | SWE-bench, GAIA, AgentBench, WebArena, OSWorld |  |
| Custom offline eval | "Domain eval" | LLM-as-judge / exec / trajectory on your product shape |  |
| Online eval | "Production eval" | Session replay, guardrail alerts, cost/latency tracking |  |
| Evaluator-optimizer | "Propose-judge-refine" | Iterate until judge passes |  |
| CI gate | "Merge blocker" | Fail the build on eval regression |  |
| Baseline | "Last-known-good" | Reference score to detect regression |  |
| Trajectory efficiency | "Steps over gold" | Agent step count divided by human expert minimum |  |

## Further Reading | 延伸阅读

- [Anthropic, Building Effective Agents](https://www.anthropic.com/research/building-effective-agents) — "start simple, optimize with evals"
  中文翻译：见原文。
- [OpenAI, SWE-bench Verified](https://openai.com/index/introducing-swe-bench-verified/) — the curated benchmark
  中文翻译：见原文。
- [Berkeley Function Calling Leaderboard](https://gorilla.cs.berkeley.edu/leaderboard.html) — tool-use benchmark
  中文翻译：见原文。
- [Langfuse docs](https://langfuse.com/) — evals + session replay in practice
  中文翻译：见原文。
