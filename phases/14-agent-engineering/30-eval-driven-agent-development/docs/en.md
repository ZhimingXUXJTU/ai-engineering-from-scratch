# Eval-Driven Agent Development | 开发 驱动 评估

> Anthropic's guidance: "start with simple prompts, optimize them with comprehensive evaluation, and add multi-step agentic systems only when needed." Evaluation is not the last step. It's the outer loop that drives every other choice in Phase 14.

**Type:** Learn + Build
**Languages:** Python (stdlib)
**Prerequisites:** All of Phase 14.
**Time:** ~60 minutes

## Learning Objectives | 学习目标

- Name the three evaluation layers — static benchmarks, custom offline, online production — and what each is for.
- Explain the evaluator-optimizer tight loop.
- Describe the 2026 best practice: evals live next to code, run in CI, gate PRs.
- Connect every Phase 14 lesson to the eval case it generates.

> **【中文解读】** 学习目标：1) 掌握三层评估体系——静态基准、自定义离线评估、在线生产评估；2) 理解评估器-优化器的紧密循环；3) 掌握 2026 年最佳实践——评估与代码同仓、CI 运行、PR 门控；4) 将 Phase 14 每节课映射到对应的评估用例。

## The Problem | 问题

Agents pass demos. They fail in production in ways demos cannot predict. Benchmarks answer "is this model broadly capable?" not "is this agent shipping the right patches for my product?" The answer: evaluation at three layers, running continuously, with every guardrail and learned rule mapped to an eval case.

> **【中文解读】** Agent 能通过演示，但在生产中以演示无法预测的方式失败。基准测试回答的是"这个模型整体能力如何"，而非"这个 Agent 是否为我的产品生成了正确的补丁"。解决方案：三层评估持续运行，每个护栏和学到的规则都映射到一个评估用例。


> **【中文解读】** 本节介绍了 AI Agent 的核心概念和实现方法。Agent 是 LLM 驱动的自主系统，能够观察环境、思考决策、执行行动并循环迭代直到完成目标。

## The Concept | 概念

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

> **【中文解读】** 三层评估体系：1) **静态基准**——标准化的跨模型对比（SWE-bench、GAIA、WebArena 等），注意数据污染问题：SWE-bench+ 发现 32.67% 的解决方案泄漏；2) **自定义离线评估**——针对你产品的特定形状，包括 LLM-as-judge、执行式评估和轨迹式评估；3) **在线评估**——生产环境中的会话回放、护栏告警和成本/延迟追踪。

### Evaluator-optimizer (Anthropic)

The tight loop:

1. Proposer generates output.
2. Evaluator judges.
3. Refine until evaluator passes.

This is Self-Refine (Lesson 05) generalized. Any agent flow you care about can wrap in evaluator-optimizer for reliability.

> **【中文解读】** 评估器-优化器循环：提议者生成输出 → 评估器判断 → 优化器改进 → 重复直到通过。这是 Self-Refine（Lesson 05）的泛化形式。任何你在意的 Agent 流程都可以用评估器-优化器包装来提高可靠性。

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

> **【中文解读】** Phase 14 每节课都生成对应的评估用例：Agent 循环的预算耗尽/无限循环防护、ReWOO 的工具失败重规划、Reflexion 的反思应用、工具使用的参数强制转换、记忆的引用匹配和过期检测、各框架的正确输出验证等。如果评估套件覆盖了每节课的用例，你就完整覆盖了 Phase 14。

### Where eval-driven development fails

- **No baseline.** Evals without a last-known-good are unreadable. Store baselines.
- **LLM-judge without grounding.** Judges hallucinate too. CRITIC pattern (Lesson 05) — judge grounds on external tools.
- **Over-fitting to evals.** Optimizing for the eval diverges from production usefulness. Rotate cases.
- **Flaky evals.** Non-deterministic cases cause false alarms. Pin seeds, snapshot state.

## Build It | 动手构建

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

## Use It | 使用方法

- Write eval cases in the same repo as your agent code.
- Run them on every PR via CI.
- Fail the build on regression.
- Track pass rate over time.
- Tie every production failure to a new case.

## Ship It | 部署上线

`outputs/skill-eval-suite.md` builds a three-layer eval suite for an agent product with CI gates and regression tracking.

## Exercises | 练习题

1. Take one of your production failures. Write an eval case that reproduces it. Does your agent pass it now?
   *思考并实践此练习*
2. Build an LLM-judge rubric for your domain with three dimensions (factual, tone, scope). Score 50 sessions.
   *思考并实践此练习*
3. Wire the eval suite into CI. Fail the build on >=5% regression.
   *思考并实践此练习*
4. Add a trajectory-efficiency metric: how many steps did the agent take vs a gold trajectory?
   *思考并实践此练习*
5. Map every Phase 14 lesson to an eval case in your suite. Any missing? That's a gap to close.
   *思考并实践此练习*

## Key Terms | 关键术语

| Term | What people say | What it actually means | 中文释义 |
|------|----------------|------------------------|---------|
| Static benchmark | "Off-the-shelf eval" | SWE-bench, GAIA, AgentBench, WebArena, OSWorld | 静态基准：标准化的离线评估集，用于跨模型对比和回归门控 |
| Custom offline eval | "Domain eval" | LLM-as-judge / exec / trajectory on your product shape | 自定义离线评估：针对产品特定形状的 LLM 评判/执行/轨迹评估 |
| Online eval | "Production eval" | Session replay, guardrail alerts, cost/latency tracking | 在线评估：生产环境中的会话回放、护栏告警、成本延迟追踪 |
| Evaluator-optimizer | "Propose-judge-refine" | Iterate until judge passes | 评估器-优化器：提议-评判-改进循环，直到评判通过 |
| CI gate | "Merge blocker" | Fail the build on eval regression | CI 门控：评估回归时阻断合并 |
| Baseline | "Last-known-good" | Reference score to detect regression | 基线：上次已知良好分数，用于检测回归 |
| Trajectory efficiency | "Steps over gold" | Agent step count divided by human expert minimum | 轨迹效率：Agent 步数除以人类专家最少步数 |

## Further Reading | 延伸阅读

- [Anthropic, Building Effective Agents](https://www.anthropic.com/research/building-effective-agents) — "start simple, optimize with evals"
- [OpenAI, SWE-bench Verified](https://openai.com/index/introducing-swe-bench-verified/) — the curated benchmark
- [Berkeley Function Calling Leaderboard](https://gorilla.cs.berkeley.edu/leaderboard.html) — tool-use benchmark
- [Langfuse docs](https://langfuse.com/) — evals + session replay in practice
