# Capstone 01 — Terminal-Native Coding Agent | 编码 Agent 结业 终端 原生

> By 2026 the shape of a coding agent is settled. A TUI harness, a stateful plan, a sandboxed tool surface, a loop that plans, acts, observes, recovers. Claude Code, Cursor 3, and OpenCode all look the same from 50 feet. This capstone asks you to build one end to end — CLI in, pull request out — and measure it against mini-swe-agent and Live-SWE-agent on SWE-bench Pro. You will learn why the hard part is not the model call but the tool loop, the sandbox, and the cost ceiling on a 50-turn run.

> **【中文解读】** 本节是综合项目——构建终端原生编码 Agent，整合 Agent 循环、工具使用和记忆系统。


**Type:** Capstone | **类型:** 综合项目
**Languages:** TypeScript / Bun (harness), Python (eval scripts) | **语言:** TypeScript / Bun（框架）, Python（评估脚本）
**Prerequisites:** Phase 11 (LLM engineering), Phase 13 (tools and protocols), Phase 14 (agents), Phase 15 (autonomous systems), Phase 17 (infrastructure) | **前置知识:** Phase 11（LLM 工程）, Phase 13（工具与协议）, Phase 14（Agent）, Phase 15（自主系统）, Phase 17（基础设施）
**Phases exercised:** P0 · P5 · P7 · P10 · P11 · P13 · P14 · P15 · P17 · P18 | **涉及阶段:** P0 · P5 · P7 · P10 · P11 · P13 · P14 · P15 · P17 · P18
**Time:** 35 hours | **时间:** 35 小时

## Problem | 问题引入

> **【中文解读】** 本节阐述编码 Agent 面临的核心工程挑战。2026 年编码 Agent 已成为 AI 应用最热门的品类，Claude Code、Cursor、Devin 等产品都采用相似的架构：终端界面 + 工具调度 + 沙箱隔离 + 规划-执行-观察循环。关键瓶颈不在模型能力，而在工具循环稳定性、上下文窗口管理和成本控制。

> **【拓展：Coding Agent 产业格局】** 2026 年编码 Agent 市场规模超 50 亿美元。Anthropic 的 Claude Code 采用 Hook 系统实现生命周期管理，Cursor 的 Composer 2 引入 Agent Tabs 多任务并行，Cognition 的 Devin 专注端到端自主开发。Live-SWE-agent 在 SWE-bench Verified 上达到 79.2% 通过率（使用 Opus 4.5），OpenCode 开源项目获得 112k GitHub 星标，反映出开发者对自主编码工具的巨大需求。

Coding agents became the dominant AI application category in 2026. Claude Code (Anthropic), Cursor 3 with Composer 2 and Agent Tabs (Cursor), Amp (Sourcegraph), OpenCode (112k stars), Factory Droids, and Google Jules all ship variations of the same architecture: a terminal harness, a permissioned tool surface, a sandbox, and a plan-act-observe loop built around a frontier model. The frontier is narrow — Live-SWE-agent reached 79.2% on SWE-bench Verified with Opus 4.5 — but the engineering craft is wide. Most failure modes are not model mistakes. They are tool-loop instability, context poisoning, runaway token cost, and destructive filesystem operations.

> 编码 Agent 在 2026 年成为 AI 应用的主导品类。Claude Code（Anthropic）、带 Composer 2 和 Agent Tabs 的 Cursor 3、Amp（Sourcegraph）、OpenCode（112k 星标）、Factory Droids 和 Google Jules 都采用相同的架构变体：终端框架、权限工具表面、沙箱和围绕前沿模型的规划-执行-观察循环。前沿很窄——Live-SWE-agent 在 SWE-bench Verified 上使用 Opus 4.5 达到了 79.2%——但工程工艺很广。大多数失败模式不是模型错误，而是工具循环不稳定、上下文污染、token 成本失控和破坏性文件系统操作。

You cannot reason about these agents from the outside. You have to build one, watch the loop crash on turn 47 when ripgrep returns 8MB of matches, and rebuild the truncation layer. That is the point of this capstone.

> 你无法从外部推理这些 Agent。你必须构建一个，观察循环在第 47 轮崩溃（当 ripgrep 返回 8MB 匹配时），然后重建截断层。这就是本结业项目的意义。

## Concept | 核心概念

> **【中文解读】** 编码 Agent 的核心架构包含四大模块：Plan（维护待办事项状态）、Act（调度工具调用）、Observe（截断输出并反馈）、Recover（错误恢复）。2026 年新增 Hook 机制——8 种生命周期事件钩子，用于注入策略、遥测和安全防护。沙箱使用 E2B 或 Daytona，每个任务在独立的 git worktree 中运行，永不接触宿主文件系统。

> **【拓展：Plan-Act-Observe 循环】** 这一架构源自 ReAct 论文（Yao et al., 2023），后被所有主流编码 Agent 采用。Claude Code 的 TodoWrite 工具将计划状态持久化到 `.claude/state.json`，支持崩溃恢复。成本控制分三层：每轮 token 上限、每会话美元预算、硬性轮次上限（通常 50 轮）。实际数据显示，一次 SWE-bench 任务的 median 成本约 $0.40-2.00，但尾部可达 $5+，因此成本天花板至关重要。

The harness has four surfaces. **Plan** maintains a TodoWrite-style state object that the model rewrites each turn. **Act** dispatches tool calls (read, edit, run, search, git). **Observe** captures stdout / stderr / exit codes, truncates, and feeds the summary back. **Recover** handles tool errors without blowing the context window or looping forever. The 2026 shape adds one more thing: **hooks**. `PreToolUse`, `PostToolUse`, `SessionStart`, `SessionEnd`, `UserPromptSubmit`, `Notification`, `Stop`, and `PreCompact` — configurable extension points where the operator injects policy, telemetry, and guardrails.

> 框架有四个表面。**Plan** 维护一个 TodoWrite 风格的状态对象，模型每轮重写。**Act** 调度工具调用（读取、编辑、运行、搜索、git）。**Observe** 捕获 stdout/stderr/退出码，截断并反馈摘要。**Recover** 处理工具错误而不破坏上下文窗口或无限循环。2026 年的形态增加了一项：**hooks**。`PreToolUse`、`PostToolUse`、`SessionStart`、`SessionEnd`、`UserPromptSubmit`、`Notification`、`Stop` 和 `PreCompact`——可配置的扩展点，操作员在此注入策略、遥测和护栏。

The sandbox is E2B or Daytona. Each task runs in a fresh devcontainer with a git worktree mounted read-write. The harness never touches the host filesystem. The worktree gets torn down on success or failure. Cost control is enforced at three layers: a per-turn token ceiling, a per-session dollar budget, and a hard turn limit (typically 50). The observability layer is OpenTelemetry spans with GenAI semantic conventions, shipped to a self-hosted Langfuse.

> 沙箱使用 E2B 或 Daytona。每个任务在带有 git worktree 挂载为读写的全新 devcontainer 中运行。框架从不接触宿主文件系统。worktree 在成功或失败后被拆除。成本控制分三层强制执行：每轮 token 上限、每会话美元预算和硬性轮次限制（通常为 50）。可观测层是带有 GenAI 语义约定的 OpenTelemetry span，发送到自托管的 Langfuse。

## Architecture | 架构

```
  user CLI  ->  harness (Bun + Ink TUI)
                  |
                  v
           plan / act / observe loop  <--->  Claude Sonnet 4.7 / GPT-5.4-Codex / Gemini 3 Pro
                  |                          (via OpenRouter, model-agnostic)
                  v
           tool dispatcher (MCP StreamableHTTP client)
                  |
     +------------+------------+----------+
     v            v            v          v
  read/edit    ripgrep     tree-sitter   git/run
     |            |            |          |
     +------------+------------+----------+
                  |
                  v
           E2B / Daytona sandbox  (worktree isolated)
                  |
                  v
           hooks: Pre/Post, Session, Prompt, Compact
                  |
                  v
           OpenTelemetry -> Langfuse (spans, tokens, $)
                  |
                  v
           PR via GitHub app
```

## Stack | 技术栈

- Harness runtime: Bun 1.2 + Ink 5 (React-in-terminal)
  中文翻译：Harness runtime: Bun 1.2 + Ink 5 (React-in-terminal)
- Model access: OpenRouter unified API with Claude Sonnet 4.7, GPT-5.4-Codex, Gemini 3 Pro, Opus 4.5 (for hardest tasks)
  中文翻译：Model access: OpenRouter unified API with Claude Sonnet 4.7, GPT-5.4-Codex, Gemini 3 Pro, Opus 4.5 (for hardest tasks)
- Tool transport: Model Context Protocol StreamableHTTP (MCP 2026 revision)
  中文翻译：Tool transport: Model Context Protocol StreamableHTTP (MCP 2026 revision)

> 中文翻译：Tool transport: Model Context Protocol StreamableHTTP (MCP 2026 revision)（翻译）

- Sandbox: E2B sandboxes (JS SDK) or Daytona devcontainers
  中文翻译：Sandbox: E2B sandboxes (JS SDK) or Daytona devcontainers
- Code search: ripgrep subprocess, tree-sitter parsers for 17 languages (pre-compiled)
  中文翻译：Code search: ripgrep subprocess, tree-sitter parsers for 17 languages (pre-compiled)
- Isolation: `git worktree add` per task, cleanup on success / failure
  中文翻译：Isolation: `git worktree add` per task, cleanup on success / failure
- Eval harness: SWE-bench Pro (verified subset) + Terminal-Bench 2.0 + your own 30-task holdout
  中文翻译：Eval harness: SWE-bench Pro (verified subset) + Terminal-Bench 2.0 + your own 30-task holdout

> 中文翻译：Eval harness: SWE-bench Pro (verified subset) + Terminal-Bench 2.0 + your own 30-task holdout（翻译）

- Observability: OpenTelemetry SDK with `gen_ai.*` semconv → self-hosted Langfuse
  中文翻译：Observability: OpenTelemetry SDK with `gen_ai.*` semconv → self-hosted Langfuse

> 中文翻译：Observability: OpenTelemetry SDK with `gen_ai.*` semconv → self-hosted Langfuse（翻译）

- PR posting: GitHub App with fine-grained token, scope limited to the target repo
  中文翻译：PR posting: GitHub App with fine-grained token, scope limited to the target repo

## Build It | 动手构建

> **【中文解读】** 构建步骤分为 8 个阶段：从 TUI 界面搭建开始，逐步实现计划状态管理、六大工具（文件读写/搜索/符号解析/Shell/Git）、E2B 沙箱包装、8 种 Hook 钩子、SWE-bench 评估、成本控制到最终 PR 提交。每步都有明确的量化指标，如工具输出截断至 4k token、50 轮硬限制、$5 单任务上限。

> **【拓展：SWE-bench 评估体系】** SWE-bench 是目前编码 Agent 最权威的评测基准，包含真实 GitHub issue 和对应 patch。SWE-bench Verified 子集经过人工验证，确保 issue 描述足够明确。2026 年排行榜上，排名靠前的系统 pass@1 在 60-80% 区间。衡量维度不仅看通过率，还包括每任务轮次、token 消耗和美元成本。mini-swe-agent 作为最简基线实现，通常作为对比起点。

1. **TUI and command loop.** Scaffold a Bun project with Ink. Accept `agent run <repo> "<task>"`. Print a split view: plan pane (top), tool-call stream (middle), token budget (bottom). Add cancel on Ctrl-C that fires `SessionEnd` hook before exit.
   中文翻译：1. **TUI and command loop.** Scaffold a Bun project with Ink. Accept `agent run <repo> "<task>"`. Print a split view: plan pane (top), tool-call stream (middle), token budget (bottom). Add cancel on Ctrl-C that fires `SessionEnd` hook before exit.

2. **Plan state.** Define a typed TodoWrite schema (pending / in_progress / done items with notes). Model rewrites the full state each turn as a tool call — do not let it mutate incrementally. Persist plan to `.agent/state.json` so crashes can resume.
   中文翻译：2. **Plan state.** Define a typed TodoWrite schema (pending / in_progress / done items with notes). Model rewrites the full state each turn as a tool call — do not let it mutate incrementally. Persist plan to `.agent/state.json` so crashes can resume.

3. **Tool surface.** Define six tools: `read_file`, `edit_file` (with diff preview), `ripgrep`, `tree_sitter_symbols`, `run_shell` (with timeout), `git` (status / diff / commit / push). Expose over MCP StreamableHTTP so the harness is transport-agnostic. Every tool returns truncated output (cap at 4k tokens per call).
   中文翻译：3. **Tool surface.** Define six tools: `read_file`, `edit_file` (with diff preview), `ripgrep`, `tree_sitter_symbols`, `run_shell` (with timeout), `git` (status / diff / commit / push). Expose over MCP StreamableHTTP so the harness is transport-agnostic. Every tool returns truncated output (cap at 4k tokens per call).

4. **Sandbox wrapping.** Each task spawns an E2B sandbox. `git worktree add -b agent/$TASK_ID` a fresh branch. All tool calls execute inside the sandbox. Host filesystem is unreachable.
   中文翻译：4. **Sandbox wrapping.** Each task spawns an E2B sandbox. `git worktree add -b agent/$TASK_ID` a fresh branch. All tool calls execute inside the sandbox. Host filesystem is unreachable.

5. **Hooks.** Implement all eight 2026 hook types. Wire at least four user-authored hooks: (a) `PreToolUse` destructive-command guard that blocks `rm -rf` outside the worktree, (b) `PostToolUse` token accounting, (c) `SessionStart` budget initialization, (d) `Stop` writes a final trace bundle.
   中文翻译：5. **Hooks.** Implement all eight 2026 hook types. Wire at least four user-authored hooks: (a) `PreToolUse` destructive-command guard that blocks `rm -rf` outside the worktree, (b) `PostToolUse` token accounting, (c) `SessionStart` budget initialization, (d) `Stop` writes a final trace bundle.

6. **Eval loop.** Clone a 30-issue subset of SWE-bench Pro Python. Run your harness against each. Compare to mini-swe-agent (the minimal baseline) on pass@1, turns-per-task, and $-per-task. Write the results to `eval/results.jsonl`.
   中文翻译：6. **Eval loop.** Clone a 30-issue subset of SWE-bench Pro Python. Run your harness against each. Compare to mini-swe-agent (the minimal baseline) on pass@1, turns-per-task, and $-per-task. Write the results to `eval/results.jsonl`.

7. **Cost control.** Hard cutoffs: 50 turns, 200k context, $5 per task. `PreCompact` hook summarizes older turns into a prior-state block at the 150k mark, freeing room for new observations without losing the plan.
   中文翻译：7. **Cost control.** Hard cutoffs: 50 turns, 200k context, $5 per task. `PreCompact` hook summarizes older turns into a prior-state block at the 150k mark, freeing room for new observations without losing the plan.

8. **PR posting.** On success, the final step is `git push` + a GitHub API call that opens a PR with the plan and the diff summary in the body.
   中文翻译：8. **PR posting.** On success, the final step is `git push` + a GitHub API call that opens a PR with the plan and the diff summary in the body.

## Use It | 使用方法

```
$ agent run ./my-repo "Fix the race condition in worker.rs"
[plan]  1 locate worker.rs and enumerate mutex uses
        2 identify shared state under contention
        3 propose fix, verify tests
[tool]  ripgrep mutex.*lock -t rust           (44 matches, truncated)
[tool]  read_file src/worker.rs 120..180
[tool]  edit_file src/worker.rs (+8 -3)
[tool]  run_shell cargo test worker::          (passed)
[plan]  1 done · 2 done · 3 done
[done]  PR opened: #482   turns=9   tokens=38k   cost=$0.41
```

## Ship It | 部署上线

The deliverable skill lives in `outputs/skill-terminal-coding-agent.md`. Given a repo path and a task description, it runs the full plan-act-observe loop in a sandbox and returns a PR URL plus a trace bundle. The rubric for this capstone:

> 交付物 skill 位于 `outputs/skill-terminal-coding-agent.md`。给定仓库路径和任务描述，它在沙箱中运行完整的规划-执行-观察循环，返回 PR URL 和追踪包。本结业项目的评分标准：

| Weight | Criterion | How it is measured |
| 权重 | 标准 | 如何衡量 |
|:-:|---|---|
| 25 | SWE-bench Pro pass@1 vs baseline | Your harness vs mini-swe-agent on 30 matched Python tasks |
| 25 | SWE-bench Pro pass@1 对比基线 | 你的框架 vs mini-swe-agent 在 30 个匹配 Python 任务上 |
| 20 | Architecture clarity | Plan/act/observe separation, hook surface, tool schema — reviewed against Live-SWE-agent layout |
| 20 | 架构清晰度 | Plan/act/observe 分离、hook 表面、tool schema——对照 Live-SWE-agent 布局审查 |
| 20 | Safety | Sandbox escape tests, permission prompts, destructive-command guard passes red-team |
| 20 | 安全性 | 沙箱逃逸测试、权限提示、破坏性命令守卫通过红队测试 |
| 20 | Observability | Trace completeness (100% of tool calls spanned), token accounting per turn |
| 20 | 可观测性 | 追踪完整性（100% 工具调用被 span 覆盖）、每轮 token 计费 |
| 15 | Developer UX | Cold-start < 2s, crash recovery resumes plan, Ctrl-C cancels mid-tool cleanly |
| 15 | 开发者体验 | 冷启动 < 2s、崩溃恢复续接计划、Ctrl-C 干净取消工具调用 |
| **100** | | |

## Exercises | 练习题

1. Swap the backing model from Claude Sonnet 4.7 to Qwen3-Coder-30B served on vLLM. Compare pass@1 and $-per-task. Report where the open model underperforms.
   中文翻译：将支持模型从 Claude Sonnet 4.7 换为 vLLM 上的 Qwen3-Coder-30B。比较 pass@1 和每任务成本。报告开源模型表现不佳之处。

> 中文翻译：将支持模型从 Claude Sonnet 4.7 换为 vLLM 上的 Qwen3-Coder-30B。比较 pass@1 和每任务成本。报告开源模型表现不佳之处。（翻译）


2. Add a `reviewer` sub-agent that reads the diff before PR posting and can request a revision loop. Measure whether false-positive reviews drop SWE-bench pass rate below the single-agent baseline (hint: usually yes).
   中文翻译：添加一个 `reviewer` 子 Agent，在 PR 发布前读取 diff 并可请求修订循环。测量误报审查是否会将 SWE-bench 通过率降至单 Agent 基线以下（提示：通常是）。

> 中文翻译：添加一个 `reviewer` 子 Agent，在 PR 发布前读取 diff 并可请求修订循环。测量误报审查是否会将 SWE-bench 通过率降至单 Agent 基线以下（提示：通常是）。（翻译）


3. Stress-test the sandbox: write a task that tries to `curl` an external URL and a task that writes outside the worktree. Confirm both are blocked by the PreToolUse hook. Log the attempts.
   中文翻译：压力测试沙箱：编写一个尝试 `curl` 外部 URL 的任务和一个在 worktree 外写入的任务。确认两者都被 PreToolUse hook 阻止。记录尝试。

> 中文翻译：压力测试沙箱：编写一个尝试 `curl` 外部 URL 的任务和一个在 worktree 外写入的任务。确认两者都被 PreToolUse hook 阻止。记录尝试。（翻译）


4. Implement `PreCompact` summarization with a smaller model (Haiku 4.5). Measure how much plan fidelity is lost at 3x compaction.
   中文翻译：用更小的模型（Haiku 4.5）实现 `PreCompact` 摘要。测量 3 倍压缩后计划保真度损失多少。

> 中文翻译：用更小的模型（Haiku 4.5）实现 `PreCompact` 摘要。测量 3 倍压缩后计划保真度损失多少。（翻译）


5. Swap MCP StreamableHTTP transport for stdio. Benchmark cold-start and per-call latency. Pick a winner for local-only use.
   中文翻译：将 MCP StreamableHTTP 传输换为 stdio。基准测试冷启动和每次调用延迟。为纯本地使用选择胜者。

> 中文翻译：将 MCP StreamableHTTP 传输换为 stdio。基准测试冷启动和每次调用延迟。为纯本地使用选择胜者。（翻译）


## Key Terms | 关键术语

| Term | What people say | What it actually means |
| 术语 | 通俗说法 | 实际含义 |
|------|-----------------|------------------------|
| Harness | "The agent loop" | The code surrounding the model that dispatches tools, maintains plan state, and enforces budgets |
| 框架 | "Agent 循环" | 围绕模型的代码，调度工具、维护计划状态和强制预算 |
| Hook | "Agent event listener" | A user-authored script run on one of eight lifecycle events by the harness |
| 钩子 | "Agent 事件监听器" | 在框架的八种生命周期事件之一上运行的用户编写脚本 |
| Worktree | "Git sandbox" | A linked git checkout at a separate path; disposable without touching the main clone |
| 工作树 | "Git 沙箱" | 在独立路径上的链接 git 检出；可丢弃而不影响主克隆 |
| TodoWrite | "Plan state" | A typed list of pending/in-progress/done items the model rewrites each turn |
| TodoWrite | "计划状态" | 模型每轮重写的待处理/进行中/已完成项的类型化列表 |
| StreamableHTTP | "MCP transport" | 2026 MCP revision: long-lived HTTP connection with bidirectional streaming; replaces SSE |
| StreamableHTTP | "MCP 传输" | 2026 MCP 修订版：支持双向流式的长连接 HTTP 连接；替代 SSE |
| Token ceiling | "Context budget" | Per-turn or per-session cap on input+output tokens; triggers compaction or termination |
| Token 上限 | "上下文预算" | 每轮或每会话的输入+输出 token 上限；触发压缩或终止 |
| pass@1 | "Single-attempt pass rate" | Fraction of SWE-bench tasks solved on the first run without retry or test-set peeking |
| pass@1 | "单次通过率" | 首次运行（无重试或偷看测试集）解决的 SWE-bench 任务比例 |

## Further Reading | 延伸阅读

- [Claude Code documentation](https://docs.anthropic.com/en/docs/claude-code) — reference harness from Anthropic
  中文翻译：Anthropic 的参考框架
- [Cursor 3 changelog](https://cursor.com/changelog) — Agent Tabs and Composer 2 product notes
  中文翻译：Agent Tabs 和 Composer 2 产品说明
- [mini-swe-agent](https://github.com/SWE-agent/mini-swe-agent) — minimal baseline for SWE-bench harness comparison
  中文翻译：SWE-bench 框架对比的最小基线
- [Live-SWE-agent](https://github.com/OpenAutoCoder/live-swe-agent) — 79.2% SWE-bench Verified with Opus 4.5
  中文翻译：使用 Opus 4.5 在 SWE-bench Verified 上达到 79.2%
- [OpenCode](https://opencode.ai) — open harness, 112k stars
  中文翻译：开源框架，112k 星标
- [SWE-bench Pro leaderboard](https://www.swebench.com) — the evaluation this capstone targets
  中文翻译：本结业项目目标的评估排行榜
- [Model Context Protocol 2026 roadmap](https://blog.modelcontextprotocol.io/posts/2026-mcp-roadmap/) — StreamableHTTP, capability metadata
  中文翻译：StreamableHTTP、能力元数据
- [OpenTelemetry GenAI semantic conventions](https://opentelemetry.io/docs/specs/semconv/gen-ai/) — span schema for tool calls and token usage
  中文翻译：工具调用和 token 使用的 span 模式
