# 开发 驱动 评估

> Anthropic's guidance: "start with simple prompts, optimize them with comprehensive evaluation, and add multi-step agentic systems only when needed." Evaluation is not the last step. It's the outer loop that drives every other choice in Phase 14.


**类型：** 学习 + 构建
**语言：** Python (stdlib)
**前置条件：** All of Phase 14.
**预计时间：** ~60 minutes

## 学习目标

- Name the three evaluation layers — static benchmarks, custom offline, online production — and what each is for.
- Explain the evaluator-optimizer tight loop.
- Describe the 2026 best practice: evals live next to code, run in CI, gate PRs.
- Connect every Phase 14 lesson to the eval case it generates.

## 问题引入

> **【中文解读】** 评估驱动的 Agent 开发（Eval-Driven Development）将传统软件工程中的 TDD 应用于 Agent：先定义评估标准，再实现 Agent。核心挑战是 Agent 的非确定性——同样的输入可能产生不同的执行路径和输出，需要基于轨迹的评估而非基于快照的评估。
> **【拓展：Eval-Driven Agent Development 是 2025-2026 年的最佳实践。核...】** Eval-Driven Agent Development 是 2025-2026 年的最佳实践。核心工具：(1) AgentOps——Agent 追踪和评估平台；(2) LangSmith——LangChain 的评估套件；(3) Braintrust——AI 评估框架。关键洞察：Agent 评估应该基于完整轨迹（trajectory）而非最终输出——两个 Agent 可能得到相同结果，但一个走了 5 步，另一个走了 50 步，质量和成本差异巨大。

## 核心概念

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
### Where eval-driven development fails
- **No baseline.** Evals without a last-known-good are unreadable. Store baselines.
- **LLM-judge without grounding.** Judges hallucinate too. CRITIC pattern (Lesson 05) — judge grounds on external tools.
- **Over-fitting to evals.** Optimizing for the eval diverges from production usefulness. Rotate cases.
- **Flaky evals.** Non-deterministic cases cause false alarms. Pin seeds, snapshot state.

## 动手实现

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

## 用框架实现

- Write eval cases in the same repo as your agent code.
- Run them on every PR via CI.
- Fail the build on regression.
- Track pass rate over time.
- Tie every production failure to a new case.

## 产出物

`outputs/skill-eval-suite.md` builds a three-layer eval suite for an agent product with CI gates and regression tracking.

## 练习题

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

## 术语速查表

| 术语 | 实际含义 |
|------|---------|
| Static benchmark | "Off-the-shelf eval" |
| Custom offline eval | "Domain eval" |
| Online eval | "Production eval" |
| Evaluator-optimizer | "Propose-judge-refine" |
| CI gate | "Merge blocker" |
| Baseline | "Last-known-good" |
| Trajectory efficiency | "Steps over gold" |

## 延伸阅读

