# The Autonomous Coding Agent Landscape (2026) | 编码 Agent 全景 美国

> SWE-bench Verified went from 4% to 80.9% in under three years. Same Claude Sonnet 4.5 scored 43.2% on SWE-agent v1 and 59.8% on Cline autonomous — the scaffolding around the model now matters as much as the model itself. OpenHands (formerly OpenDevin) is the most active MIT-licensed platform and its CodeAct loop executes Python actions directly in a sandbox instead of JSON tool calls. The headline numbers hide a methodological issue: 161 of 500 SWE-bench Verified tasks require only a 1–2 line change, and SWE-bench Pro (10+ line tasks) sits at 23–59% for the same frontier models.

**Type:** Learn | **类型:** 学习
**Languages:** Python (stdlib, CodeAct vs JSON tool-call comparison) | **语言:** Python (stdlib, CodeAct vs JSON tool-call comparison)
**Prerequisites:** Phase 14 · 07 (Tool use), Phase 15 · 01 (Long-horizon agents) | **前置知识:** Phase 14 · 07 (Tool use), Phase 15 · 01 (Long-horizon agents)
**Time:** ~45 minutes | **时间:** ~45 minutes

## The Problem | 问题引入

> **【中文解读】** 编码 Agent 景观是 2025-2026 年变化最快的 AI 应用领域之一。主要玩家包括 Claude Code、Cursor、GitHub Copilot、Devin、Windsurf 等。关键差异化因素：(1) 自主性级别——从补全建议到完全自主编码；(2) 上下文管理——如何处理大型代码库；(3) 工具集成——支持哪些开发工具。

> **【拓展：coding agent landscape】** 2026年编码 Agent 的竞争格局：(1) Claude Code——Anthropic 的自主编码 Agent，支持全栈开发、Git 操作和终端命令执行；(2) Cursor——基于 VS Code 的 AI 编辑器，强调人机协作；(3) Devin——Cognition AI 的全自主编码 Agent，可以独立完成开发任务；(4) Windsurf（原 Codeium）——AI 优先的 IDE。SWE-bench 上的表现是主要竞争指标。

"Which coding agent is best" is the wrong question. The right question is: on a task distribution that matches my work, with the scaffolding I will run in production, what end-to-end reliability do I get?

> "哪个编码 Agent 最好"是错误的问题。正确的问题是：在与我的工作匹配的任务分布上，我能获得什么端到端可靠性？ The right question is: on a task distribution that matches my work, with the scaffolding I will run in production, what end-to-end reliability do I get?

Between 2022 and 2026 the field learned that scaffolding — the retrieval layer, the planner, the sandbox, the edit-verify loop, the feedback format — is load-bearing. Claude Sonnet 4.5 on SWE-agent v1 scored 43.2% on SWE-bench Verified; the same model inside Cline's autonomous scaffold scored 59.8%. 16.6 absolute points of difference, same weights. The base model is a component; the loop is the product.


> **【中文解读】** 本节介绍了 AI Agent 的核心概念和实现方法。Agent 是 LLM 驱动的自主系统，能够观察环境、思考决策、执行行动并循环迭代直到完成目标。

The companion problem is that benchmark saturation hides regressions.

> 伴随问题是基准饱和隐藏了回归。SWE-bench Verified 接近饱和，简单任务的尾部拉高了顶级分数。 SWE-bench Verified is close to saturated, and the easy-task tail (161 of 500 tasks requiring ≤2 lines) pulls top scores up. Real-world quality is better measured on distributions like SWE-bench Pro (10+ line changes), where the same leaders still sit at 23–59%.

## The Concept | 核心概念

### SWE-bench, one paragraph

SWE-bench (Jimenez et al.) takes real GitHub issues with ground-truth patches and asks an agent to produce a patch that makes the test suite pass. SWE-bench Verified (OpenAI, 2024) is a human-curated 500-task subset with the ambiguous and broken tasks removed. SWE-bench Pro is the harder successor — tasks requiring 10+ lines of change, where current frontier agents sit at 23–59%.

### What the 2022 → 2026 curve actually shows

- **2022**: research models at ~4% on raw SWE-bench.
- **2024**: GPT-4 + Devin-style scaffolding at ~14%; SWE-agent at ~12%.
- **2025**: Claude 3.5/3.7 Sonnet inside Aider and SWE-agent push into the 40–55% range.
- **2026**: Claude Sonnet 4.5 and frontier competitors at 70–80%+ on SWE-bench Verified. Epoch AI's leaderboard tracks this live.

The slope came from three compounding sources: better base models, better scaffolding (CodeAct, reflection, verifier loops), and better benchmarks (Verified removing noise).

### CodeAct vs JSON tool calls

OpenHands (All-Hands-AI, arXiv:2407.16741, formerly OpenDevin) took a specific architectural bet: instead of the model emitting JSON tool calls that a host decodes and executes, the model emits Python code and a Jupyter-style kernel runs it in a sandbox. The agent can loop over files, chain tools, and catch its own exceptions inside one action.

The trade-off:

- **JSON tool calls**: every action is one turn; easy to audit; limited compositionality; safe by default because each call goes through an explicit validator.
- **CodeAct**: one action can be a whole program; compositional; requires a hardened sandbox (OpenHands uses Docker isolation); failure modes include anything the sandbox runtime allows.

Both architectures are in production. CodeAct is dominant in open platforms (OpenHands, smolagents). JSON tool calls remain dominant in managed services (Anthropic Managed Agents, OpenAI Assistants) where the provider controls the executor.

### Scaffolds in the 2026 landscape

| Scaffold | License | Execution model | Notable property |
|---|---|---|---|
| OpenHands (OpenDevin) | MIT | CodeAct in Docker | Most active open platform; event-stream replayable |
| SWE-agent | MIT | Agent-Computer Interface (ACI) | First end-to-end SWE-bench scaffold |
| Aider | Apache-2 | edit-via-diff in local repo | Minimal scaffold, strong regression stability |
| Cline | Apache-2 | VS Code agent with tool policy | Highest-scoring open scaffold on Sonnet 4.5 |
| Devin (Cognition) | Proprietary | Managed VM + planner | First "AI software engineer" product category |
| Claude Code | Proprietary | Permission modes + routines | Lesson 10 covers the agent loop in detail |

### Why scaffolding dominates

A coding run is a long-horizon trajectory (Lesson 1). Reliability compounds across steps. Three places where scaffolding buys points:

1. **Retrieval**: finding the right files to read is the silent bottleneck. SWE-agent's ACI, OpenHands' file-index, and Aider's repo-map all attack this.
2. **Verifier loop**: running tests, reading stack traces, and re-attempting is a 10+ point delta on SWE-bench.
3. **Failure containment**: a sandbox that rolls back on error prevents compounding damage. The same model with and without a verifier loop looks like two different products.

### Benchmark saturation and the real distribution

The OpenHands authors and Epoch AI both flag that SWE-bench Verified has an easy tail: 161 of 500 tasks need only 1–2 lines of change. High scores are driven partly by this tail. SWE-bench Pro restricts to 10+ line changes and returns scores in the 23–59% range even for frontier systems. Your production distribution is almost certainly closer to Pro than to Verified.

Implication for choosing an agent: run a Pro-like subset of your own bug backlog. The score that matters is the score on tasks representative of what you ship.

## Use It | 用框架实现

`code/main.py` compares two toy agent scaffolds on a fixed mini-task distribution:

1. A **JSON tool-call** scaffold that takes one action per turn.
2. A **CodeAct** scaffold that can emit a small Python snippet per action.

Both use a stub "model" (deterministic rules) so the comparison isolates the scaffold from model quality. The output shows the CodeAct scaffold solves more tasks in fewer turns at the cost of a larger per-action blast radius.

## Ship It | 产出物

`outputs/skill-scaffold-audit.md` helps you audit a proposed coding-agent scaffold before adoption: retrieval quality, verifier presence, sandbox isolation, and benchmark-to-distribution fit.

## Exercises | 练习题

1. Run `code/main.py`. How many turns does each scaffold take on the same task set? What is the per-action blast radius of each?

2. Read the OpenHands paper (arXiv:2407.16741). The paper argues CodeAct beats JSON tool calls on complex tasks. Identify one failure mode the paper acknowledges and write one sentence on when that mode would dominate in production.

3. Pick one task from your bug backlog that would require 10+ lines of change across two files. Estimate the end-to-end success probability for a frontier model under (a) JSON tool calls and (b) CodeAct. Justify the gap.

4. SWE-bench Verified has 161 single-file, 1–2 line tasks. Construct a score that excludes them. How does the leaderboard shuffle?

5. Read "Introducing SWE-bench Verified" (OpenAI). Explain the specific methodology used to remove ambiguous tasks, and name one category the curation would miss.

## Key Terms | 术语速查表

| Term | What people say | What it actually means |
|---|---|---|
| 术语 | 通俗说法 | 实际含义 |
| SWE-bench | "Coding benchmark" | Real GitHub issues with ground-truth patches and test suites |  |
| SWE-bench Verified | "Cleaned subset" | 500 human-curated tasks, easier-tail present |  |
| SWE-bench Pro | "Harder subset" | 10+ line changes; frontier sits at 23–59% |  |
| CodeAct | "Code-as-action" | Agent emits Python; Jupyter-style kernel executes in sandbox |  |
| JSON tool call | "Function calling" | Each action is a structured JSON payload validated before execution |  |
| Scaffold | "Agent framework" | Retrieval + planner + executor + verifier loop around the base model |  |
| ACI (Agent-Computer Interface) | "SWE-agent's format" | Command set designed for LLM ergonomics, not human shells |  |
| Verifier loop | "Test-and-retry" | Run tests, read output, revise patch; biggest non-model reliability gain |  |

## Further Reading | 延伸阅读

- [Jimenez et al. — SWE-bench](https://www.swebench.com/) — the original benchmark and methodology.
- [OpenAI — Introducing SWE-bench Verified](https://openai.com/index/introducing-swe-bench-verified/) — how the curated subset was built.
- [Wang et al. — OpenHands: An Open Platform for AI Software Developers](https://arxiv.org/abs/2407.16741) — CodeAct architecture and event-stream design.
- [Epoch AI — SWE-bench leaderboard](https://epoch.ai/benchmarks) — live-tracked scores.
- [Anthropic — Measuring agent autonomy](https://www.anthropic.com/research/measuring-agent-autonomy) — long-horizon coding-agent reliability framing.
