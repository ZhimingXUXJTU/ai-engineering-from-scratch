# Capstone 16 — GitHub Issue-to-PR Autonomous Agent | GitHub Issue 结业 美国 PR

> AWS Remote SWE Agents, Cursor Background Agents, OpenAI Codex cloud, and Google Jules all ship the same 2026 product shape: label an issue, get a PR. Run an agent in a cloud sandbox, verify tests pass, and post a review-ready PR with rationale. The hard parts are reproducing the repo's build environment automatically, preventing credential leakage, enforcing per-repo budgets, and making sure the agent cannot force-push. This capstone builds the self-hosted version and compares it on cost and pass rate to the hosted alternatives.

> **【中文解读】** 本节是综合项目——构建 GitHub Issue 到 PR 的自动化 Agent。


**Type:** Capstone
**Languages:** Python (agent), TypeScript (GitHub App), YAML (Actions)
**Prerequisites:** Phase 11 (LLM engineering), Phase 13 (tools), Phase 14 (agents), Phase 15 (autonomous), Phase 17 (infrastructure)
**Phases exercised:** P11 · P13 · P14 · P15 · P17
**Time:** 30 hours

## Problem

> **【中文解读】** 本节描述异步云端编码 Agent 的核心挑战。与交互式编码 Agent（Capstone 01）不同，这里 UX 是一个 GitHub 标签——标注 `@agent fix this` 后，工作器在云沙箱中启动，克隆仓库、运行测试、编辑文件、验证并开 PR。工程挑战包括：环境复现（从零构建无缓存开发镜像）、测试抖动、凭据范围控制、每日每仓库预算强制和禁止 force-push。

> **【拓展：异步编码 Agent 产品】** 2026 年异步云端编码 Agent 已成为独立品类。AWS Remote SWE Agents、Cursor Background Agents、OpenAI Codex Cloud、Google Jules、Factory Droids 都采用相同架构：标签触发 → 云沙箱 → 自动构建 → Agent 循环 → CI 验证 → PR 提交。关键安全措施：GitHub App 使用短期安装 token，分支保护禁止直写 main 和 force-push，每日每仓库预算上限（如 5 PR/天，$20/PR）。自托管版本与托管方案对比时，主要看 pass rate 和 $/PR。

The async cloud coding agent is a separate product category from interactive coding agents (capstone 01). The UX is a GitHub label. You label an issue `@agent fix this`, a worker spins up in a cloud sandbox, clones the repo, runs tests, edits files, verifies, and opens a PR with the agent's rationale in the body. No interactive loop, no terminal. AWS Remote SWE Agents, Cursor Background Agents, OpenAI Codex cloud, Google Jules, and Factory Droids all converge on this.

The engineering challenges are concrete: environment reproduction (the agent has to build the repo from scratch without a cached dev image), flaky tests (must be re-run or isolated), credential scoping (a GitHub App with minimal fine-grained permissions), budget enforcement per repo per day, and no-force-push policy. The capstone measures pass rate, cost, and safety vs the hosted alternatives.

## Concept

> **【中文解读】** 触发通过 GitHub webhook（issue 标签或 PR 评论），调度器将任务入队到 ECS Fargate 或 Lambda。工作器将仓库拉入 Daytona/E2B 沙箱，使用从仓库推断的通用 Dockerfile。Agent 运行 mini-swe-agent 循环（读代码→提议修复→打补丁→运行测试）。完整 CI 通过后才开 PR，覆盖率下降超过阈值时标记 `needs-review`。安全通过 GitHub App 短期 token + 分支保护 + 工作器级文件编辑白名单实现。

> **【拓展：沙箱环境复现】** 环境复现是异步 Agent 的核心难点——Agent 必须从零构建仓库的开发环境。自动推断策略包括：检测语言/框架（package.json/pom.xml/Cargo.toml/requirements.txt）、选择基础镜像、安装依赖。Daytona 和 E2B 都提供预构建的开发容器模板。测试抖动处理策略：失败测试重跑 3 次，一致失败才视为真失败。预算强制在调度器层面实现（每日/每仓库/每 PR 三层上限）。

The trigger is a GitHub webhook (issue label or PR comment). A dispatcher enqueues work to ECS Fargate or Lambda. The worker pulls the repo into a Daytona or E2B sandbox with a generic Dockerfile inferred from the repo (language, framework). The agent runs a mini-swe-agent or SWE-agent v2 loop against Claude Opus 4.7 or GPT-5.4-Codex. It iterates: read code, propose fix, apply patch, run tests.

Verification is the gating step. Full CI must pass in the sandbox before the PR opens. Coverage delta is computed; if negative beyond a threshold, the PR opens but gets labeled `needs-review`. The agent posts the rationale as the PR description plus an `@agent` thread the reviewer can ping for follow-ups.

Safety is scoped through two different GitHub surfaces: the App provides a short-lived installation token with `workflows: read` and narrow repo contents/PR scopes; branch protection (not app permissions) enforces "no direct writes to `main`" and "no force-push" — the app is never added to the bypass list. Path-scoped read-only access to `.github/workflows` is not a real GitHub App primitive, so the agent's allow-list on file edits has to enforce that at the worker. Budget ceilings per repo per day are enforced at the dispatcher (e.g., max 5 PRs per repo per day, $20 per PR).

## Architecture | 架构

```
GitHub issue labeled `@agent fix` or PR comment
            |
            v
    GitHub App webhook -> AWS Lambda dispatcher
            |
            v
    ECS Fargate task (or GitHub Actions self-hosted runner)
       - pull repo
       - infer Dockerfile (language, package manager)
       - Daytona / E2B sandbox with target runtime
       - clone -> git worktree -> agent branch
            |
            v
    mini-swe-agent / SWE-agent v2 loop
       Claude Opus 4.7 or GPT-5.4-Codex
       tools: ripgrep, tree-sitter, read/edit, run_tests, git
            |
            v
    verify CI passes in-sandbox + coverage delta check
            |
            v (verified)
    git push + open PR via GitHub App
       PR body = rationale + diff summary + trace URL
       label: needs-review
            |
            v
    operator reviews; can @-mention agent for follow-ups
```

## Stack

- Trigger: GitHub App with fine-grained token; webhook receiver via Lambda or Fly.io
- Worker: ECS Fargate task (or GitHub Actions self-hosted runner)
- Sandbox: Daytona devcontainer or E2B sandbox per task
- Agent loop: mini-swe-agent baseline or SWE-agent v2 over Claude Opus 4.7 / GPT-5.4-Codex
- Retrieval: tree-sitter repo-map + ripgrep
- Verification: full CI in-sandbox + coverage delta gate
- Observability: Langfuse with per-PR trace archive linked from the PR body
- Budget: per-repo daily dollar ceiling; max PRs per repo per day

## Build It | 动手构建

> **【中文解读】** 构建 GitHub Issue 到 PR 的自动化 Agent：GitHub App 权限管理（细粒度安装 token）、Issue 分类器（bug/feature/refactor 分类）、实现 Agent（SWE-bench 级别的问题解决）、PR 创建和审查。安全设计强调：不允许直接推送到 main、不允许 force-push、不允许修改 .github/workflows。

> **【拓展：GitHub Copilot Autofix 和 SWE-Agent 的自动化 PR 实践】** GitHub 的 Copilot Autofix（2024 年 GA）自动为安全漏洞生成修复 PR。SWE-Agent（Princeton）在 SWE-bench 上达到 50%+ 通过率。OpenHands（原 OpenDevin）的 CodeAct Agent 将 Issue 到 PR 的流程完全自动化。关键挑战是分支策略和 CI 集成——Agent 创建的 PR 必须通过项目的 CI 检查，但 CI 本身可能依赖 Agent 修改的代码。本课的分支保护和工作流限制设计解决了这个自举问题。

1. **GitHub App.** Fine-grained installation token: issues read+write, pull_requests write, contents read+write, workflows read. Branch protection (the only surface that can do this) enforces "no direct push to `main`" and "no force-push"; the app is not in the bypass list. The worker enforces "no writes under `.github/workflows`" as an allow-list check on the proposed diff, since GitHub App permissions are not path-scoped.

2. **Webhook receiver.** Lambda function accepts issue label / PR comment webhooks. Filters by label `@agent fix this`. Enqueues to SQS.

3. **Dispatcher.** Pops tasks from SQS. Enforces per-repo per-day budget. Spins up an ECS Fargate task with the repo URL, issue body, and a fresh Daytona sandbox.

4. **Environment inference.** Detect language (Python, Node, Go, Rust) and package manager (uv, pnpm, go mod, cargo). Generate a Dockerfile on the fly if one does not exist.

5. **Agent loop.** mini-swe-agent or SWE-agent v2 with Claude Opus 4.7. Tools: ripgrep, tree-sitter repo-map, read_file, edit_file, run_tests, git. Hard limits: $20 cost, 30 min wall-clock, 30 agent turns.

6. **Verification.** After the loop concludes, run the full test suite in-sandbox. Compute coverage delta via jacoco / coverage.py. If CI red: halt, do not open PR. If coverage drops more than 2%: open PR with `needs-review` label.

7. **PR posting.** Push the agent branch. Open PR via GitHub API with: title, rationale, diff summary, trace URL, cost, turns.

8. **Credential hygiene.** Worker runs with a short-lived GitHub App installation token. Logs are scrubbed for secrets before archival.

9. **Eval.** 30 seeded internal issues of varying difficulty. Measure pass rate, PR quality (diff size, style, coverage), cost, latency. Compare with Cursor Background Agents and AWS Remote SWE Agents on the same issues.

## Use It | 使用方法

```
# on github.com
  - user labels issue #842 with `@agent fix this`
  - PR #1903 appears 14 minutes later
  - body:
    > Fixed NPE in widget.dedupe() caused by null comparator entry.
    > Added regression test widget_test.go::TestDedupeNullComparator.
    > Coverage delta: +0.12%
    > Turns: 7  Cost: $1.80  Trace: langfuse:...
    > Label: needs-review
```

## Ship It | 部署上线

`outputs/skill-issue-to-pr.md` is the deliverable. A GitHub App + async cloud worker that turns labeled issues into review-ready PRs with bounded cost and scoped credentials.

| Weight | Criterion | How it is measured |
|:-:|---|---|
| 25 | Pass rate on 30 issues | End-to-end success (CI green + coverage OK) |
| 20 | PR quality | Diff size, coverage delta, style conformance |
| 20 | Cost and latency per resolved issue | $ and wall-clock per PR |
| 20 | Safety | Scoped token, per-repo budget, no force-push, credential hygiene |
| 15 | Operator UX | Rationale comments, retry affordance, @-mention follow-up |
| **100** | | |

## Exercises | 练习题

1. Add a "fix flaky test" mode: the label `@agent stabilize-flake TestX` runs the test 50 times in-sandbox and proposes a minimal change that stabilizes it.

2. Compare cost vs Cursor Background Agents on three shared issues. Report which tools win where.

3. Implement a budget dashboard: per-repo per-day cost, per-user cost. Alert on anomaly.

4. Build a "dry-run" mode that opens a draft PR without running CI, so reviewers can examine the plan cheap.

5. Add a retention policy: PR branches older than 7 days without merge get deleted automatically.

## Key Terms | 关键术语

| Term | What people say | What it actually means |
|------|-----------------|------------------------|
| GitHub App | "Scoped bot identity" | App with fine-grained permissions + short-lived installation token |
| Async cloud agent | "Background agent" | Non-interactive worker that runs in a cloud sandbox, not a terminal |
| Environment inference | "Dockerfile synthesis" | Detect language + package manager, generate a Dockerfile if absent |
| Verification | "CI-in-sandbox" | Run the full test suite inside the worker before opening a PR |
| Coverage delta | "Coverage preservation" | Change in test coverage % from base to agent branch |
| Per-repo budget | "Daily ceiling" | Dollar and PR-count cap enforced at the dispatcher |
| Rationale | "PR body explanation" | Agent's summary of what changed and why; required in the PR body |

## Further Reading | 延伸阅读

- [AWS Remote SWE Agents](https://github.com/aws-samples/remote-swe-agents) — the canonical async cloud agent reference
- [SWE-agent](https://github.com/SWE-agent/SWE-agent) — CLI reference
- [Cursor Background Agents](https://docs.cursor.com/background-agent) — commercial alternative
- [OpenAI Codex (cloud)](https://openai.com/codex) — hosted competitor
- [Google Jules](https://jules.google) — Google's hosted version
- [Factory Droids](https://www.factory.ai) — alternate commercial reference
- [GitHub App documentation](https://docs.github.com/en/apps) — scoped bot identity
- [Daytona cloud sandboxes](https://daytona.io) — reference sandbox
