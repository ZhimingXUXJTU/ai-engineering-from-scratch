# Capstone 10 — Multi-Agent Software Engineering Team | 多 Agent 工程 结业

> SWE-AF's factory architecture, MetaGPT's role-based prompting, AutoGen 0.4's typed actor graph, Cognition's Devin, and Factory's Droids all converged on the same 2026 shape: an architect plans, N coders work in parallel worktrees, a reviewer gates, a tester verifies. Parallel worktrees convert wall-clock into throughput. Shared state and handoff protocols become the failure surface. The capstone is to build the team, evaluate on SWE-bench Pro, and report which handoffs break and how often.

> **【中文解读】** 本节是综合项目——构建多 Agent 软件团队，模拟完整的开发团队协作。


**Type:** Capstone
**Languages:** Python / TypeScript (agents), Shell (worktree scripts)
**Prerequisites:** Phase 11 (LLM engineering), Phase 13 (tools), Phase 14 (agents), Phase 15 (autonomous), Phase 16 (multi-agent), Phase 17 (infrastructure)
**Phases exercised:** P11 · P13 · P14 · P15 · P16 · P17
**Time:** 40 hours

## Problem

> **【中文解读】** 本节阐述多 Agent 软件团队的核心问题。单 Agent 编码器在大型任务上遇到瓶颈——不是因为个体能力弱，而是 200k token 上下文无法同时容纳架构计划、四个并行代码切片、评审意见和测试输出。多 Agent 工厂将问题拆分：架构师规划、编码者在并行 worktree 中实现、评审者把关、测试者验证。失败面在交接处——架构师计划无法实现、编码者产生冲突 diff、评审者批准幻觉修复、测试者与编写者竞争。

> **【拓展：多 Agent 框架生态】** 2026 年主要多 Agent 框架：SWE-AF（工厂架构）、MetaGPT（角色提示）、AutoGen 0.4（类型化 Actor 图）、Cognition Devin（产品级）、Factory Droids（产品级）。Google A2A 协议（2025）标准化了 Agent 间消息格式。关键发现：多 Agent 的核心问题不是"是否工作"而是"每美元是否更优"——token 放大效应（4 角色总 token 约为单 Agent 的 4 倍）意味着只有在并行提速显著时才值得。

Single-agent coding harnesses hit a ceiling on large tasks. Not because any individual agent is weak, but because a 200k-token context cannot hold an architecture plan plus four parallel codebase slices plus reviewer commentary plus test output. Multi-agent factories split the problem: an architect owns the plan, coders own implementation in parallel worktrees, a reviewer gates, a tester verifies. SWE-AF's "factory" architecture, MetaGPT's roles, AutoGen's typed actor graph — all three framings describe the same shape.

The failure surface is the handoff. Architect plans something the coders cannot implement. Coders produce conflicting diffs. Reviewer approves a hallucinated fix. Tester races a still-writing coder. You will build one of these teams, run it on 50 SWE-bench Pro issues, track every handoff, and publish the post-mortem.

## Concept

> **【中文解读】** 角色是类型化 Agent：架构师（Opus 4.7，读 issue 写计划并分解子任务）、编码者（Sonnet 4.7，N 个并行实例，各自在 git worktree + Daytona 沙箱中）、评审者（GPT-5.4，读合并 diff 批准或打回）、测试者（Gemini 2.5 Pro，独立运行测试套件）。通信通过共享任务板（文件/Redis），交接使用 A2A 协议类型化消息。协调关注点包括合并冲突解决、共享状态同步和评审者利益冲突避免。

> **【拓展：Token 放大效应】** 多 Agent 系统的隐含成本是 token 放大：每次角色边界增加摘要提示和交接上下文。一次 40 轮单 Agent 运行变成 4 角色 160 总轮次。评估指标包括 pass@1（解决率）和 $/solved-issue（每解决一题的美元成本）。实测中，多 Agent 在大型任务上 wall-clock 快 2-3 倍，但总 token 消耗高 3-4 倍，因此需要仔细权衡任务粒度和并行度。

Roles are typed agents. **Architect** (Claude Opus 4.7) reads the issue, writes a plan, and breaks it into subtasks with explicit interfaces. **Coders** (Claude Sonnet 4.7, N parallel instances, each in a `git worktree` + Daytona sandbox) implement subtasks independently. **Reviewer** (GPT-5.4) reads the merged diff and either approves or requests specific changes. **Tester** (Gemini 2.5 Pro) runs the test suite in isolation and reports pass/fail with artifacts.

Communication is through a shared task board (file-backed or Redis). Each role consumes tasks it is permitted to handle. Handoffs are A2A-protocol-typed messages. Coordination concerns: merge-conflict resolution (coordinator role or automatic three-way merge), shared-state synchronization (the plan is frozen once coders start; replans are separate events), and reviewer gatekeeping (the reviewer cannot approve its own changes or changes it proposed).

Token amplification is the hidden cost. Every role boundary adds summary prompts and handoff context. A 40-turn single-agent run becomes 160 total turns across four roles. The rubric specifically weighs token efficiency vs single-agent baseline because the question is not "does multi-agent work" but "does it win per dollar."

## Architecture | 架构

```
GitHub issue URL
      |
      v
Architect (Opus 4.7)
   reads issue, produces plan with subtasks + interfaces
      |
      v
Task board (file / Redis)
      |
   +-- subtask 1 ---+-- subtask 2 ---+-- subtask 3 ---+-- subtask 4 ---+
   v                v                v                v                v
Coder A          Coder B          Coder C          Coder D          (4 parallel)
 (Sonnet)         (Sonnet)         (Sonnet)         (Sonnet)
 worktree A       worktree B       worktree C       worktree D
 Daytona          Daytona          Daytona          Daytona
      |                |                |                |
      +--------+-------+-------+--------+
               v
           merge coordinator  (three-way merge + conflict resolution)
               |
               v
           Reviewer (GPT-5.4)
               |
               v
           Tester  (Gemini 2.5 Pro)  -> passes? -> open PR
                                     -> fails?  -> route back to coder
```

## Stack

- Orchestration: LangGraph with shared state + per-agent sub-graphs
- Messaging: A2A protocol (Google 2025) for typed inter-agent messages
- Models: Opus 4.7 (architect), Sonnet 4.7 (coders), GPT-5.4 (reviewer), Gemini 2.5 Pro (tester)
- Worktree isolation: `git worktree add` per coder + Daytona sandbox
- Merge coordinator: custom three-way merge + LLM-mediated conflict resolution
- Eval: SWE-bench Pro (50 issues), SWE-AF scenarios, HumanEval++ for unit tests
- Observability: Langfuse with role-tagged spans, per-agent token accounting
- Deployment: K8s with each role as a separate Deployment + HPA on backlog

## Build It | 动手构建

> **【中文解读】** 构建多 Agent 软件开发团队：架构师（分解任务为 DAG）、多个编码 Agent（并行实现子任务）、代码审查 Agent（检查正确性和风格）、测试 Agent（编写和运行测试）。任务板是文件支持的 JSONL，角色通过标签订阅消息。关键设计是子任务接口的显式声明——每个子任务指定涉及的文件、公共函数和测试影响。

> **【拓展：多 Agent 软件开发的产业实践】** Meta 的多人协作编程工具、Sourcegraph 的 Cody Team 模式、Devin 的多 Agent 架构都采用类似的"架构师 + 工人 + 审查者"模式。ChatDev 和 MetaGPT 的学术研究显示，多 Agent 协作在代码生成质量上优于单 Agent，关键因素是角色分离带来的上下文隔离。本课的 JSONL 任务板是这些系统核心通信协议的教育性简化。

1. **Task board.** File-backed JSONL with typed messages: `plan_request`, `subtask`, `diff_ready`, `review_needed`, `test_needed`, `approved`, `rejected`, `replan_needed`. Agents subscribe to tags.

2. **Architect.** Reads the GitHub issue, runs Opus 4.7 with a plan template requiring explicit subtask interfaces (files touched, public functions, test impact). Emits one `plan_request` with a DAG of subtasks.

3. **Coders.** N parallel workers, each claims one subtask from the board. Each spawns a fresh `git worktree add` branch plus a Daytona sandbox. Implements the subtask. Emits `diff_ready` with the patch + test deltas.

4. **Merge coordinator.** On all-coders-done, three-way merges the N branches into a staging branch. LLM-mediated conflict resolution only when file-level overlap exists.

5. **Reviewer.** GPT-5.4 reads the merged diff. Cannot approve diffs it authored. Emits `approved` (no-op) or `review_feedback` with specific change requests routed back to the relevant coder.

6. **Tester.** Gemini 2.5 Pro runs the test suite in a clean sandbox. Captures artifacts. Emits `test_passed` or `test_failed` with stacktraces. Failed tests loop back to the coder owning the failing subtask.

7. **Handoff accounting.** Every message crossing a role boundary gets a span in Langfuse with payload size and model used. Compute per-subtask token amplification (coder_tokens + reviewer_tokens + tester_tokens + architect_share / coder_tokens).

8. **Eval.** Run on 50 SWE-bench Pro issues. Compare pass@1 and $-per-solved-issue against a single-agent baseline (one Sonnet 4.7 in a single worktree).

9. **Post-mortem.** For each failed issue, identify the handoff that broke (plan too vague, merge conflict, reviewer false-approve, tester flake). Produce a handoff-failure histogram.

## Use It | 使用方法

```
$ team run --issue https://github.com/acme/widget/issues/842
[architect] plan: 4 subtasks (parser, cache, api, migration)
[board]     dispatched to 4 coders in parallel worktrees
[coder-A]   subtask parser  -> 42 lines, tests pass locally
[coder-B]   subtask cache   -> 88 lines, tests pass locally
[coder-C]   subtask api     -> 31 lines, tests pass locally
[coder-D]   subtask migration -> 19 lines, tests pass locally
[merge]     3-way merge: 0 conflicts
[reviewer]  comments on cache (thread pool sizing); routed to coder-B
[coder-B]   revision: 92 lines; submits
[reviewer]  approved
[tester]    all 412 tests pass
[pr]        opened #3382   4 coders, 1 revision, $4.90, 18m
```

## Ship It | 部署上线

`outputs/skill-multi-agent-team.md` is the deliverable. Given an issue URL and parallelism level, the team produces a merge-ready PR with per-role token accounting.

| Weight | Criterion | How it is measured |
|:-:|---|---|
| 25 | SWE-bench Pro pass@1 | Matched 50-issue subset, pass@1 |
| 20 | Parallel speedup | Wall-clock vs single-agent baseline |
| 20 | Review quality | False-approval rate on injected-bug probe |
| 20 | Token efficiency | Total tokens per solved issue vs single-agent |
| 15 | Coordination engineering | Merge-conflict resolution, handoff-failure histogram |
| **100** | | |

## Exercises | 练习题

1. Inject an obvious bug into a diff mid-run (extra `return None` before the main body). Measure the reviewer's false-approve rate. Tune the reviewer prompt until false-approval is under 5%.

2. Reduce to two coders (architect + coder + reviewer + tester, coder runs two subtasks sequentially). Compare wall-clock and pass rate.

3. Replace the merge coordinator with a single-writer constraint (subtasks touch disjoint file sets). Measure the planning burden on the architect.

4. Swap reviewer from GPT-5.4 to Claude Opus 4.7. Measure false-approval rate and token cost delta.

5. Add a fifth role: documenter (Haiku 4.5). After review, it produces a changelog entry. Measure whether documentation quality justifies the extra token spend.

## Key Terms | 关键术语

| Term | What people say | What it actually means |
|------|-----------------|------------------------|
| Parallel worktree | "Isolated branch" | `git worktree add` producing a fresh working tree per coder |
| Task board | "Shared message bus" | File or Redis store of typed messages agents subscribe to |
| Handoff | "Role boundary" | Any message crossing from one role's context to another's |
| Token amplification | "Multi-agent overhead" | Total tokens across roles / single-agent tokens for the same task |
| A2A protocol | "Agent-to-agent" | Google's 2025 spec for typed inter-agent messages |
| Merge coordinator | "Integrator" | Component that runs three-way merge and mediates conflicts |
| False approval | "Reviewer hallucination" | Reviewer approves a diff with known bugs |

## Further Reading | 延伸阅读

- [SWE-AF factory architecture](https://github.com/Agent-Field/SWE-AF) — the reference 2026 multi-agent factory
- [MetaGPT](https://github.com/FoundationAgents/MetaGPT) — role-based multi-agent framework
- [AutoGen v0.4](https://github.com/microsoft/autogen) — Microsoft's typed actor framework
- [Cognition AI (Devin)](https://cognition.ai) — reference product
- [Factory Droids](https://www.factory.ai) — alternate reference product
- [Google A2A protocol](https://developers.google.com/agent-to-agent) — inter-agent messaging spec
- [git worktree documentation](https://git-scm.com/docs/git-worktree) — the isolation substrate
- [SWE-bench Pro](https://www.swebench.com) — the evaluation target
