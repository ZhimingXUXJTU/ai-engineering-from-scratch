# Capstone 09 — Code Migration Agent (Repo-Level Language / Runtime Upgrade) | 迁移 结业 运行时 仓库

> Amazon's MigrationBench (Java 8 to 17) and Google's App Engine Py2-to-Py3 migrator set the 2026 bar. Moderne's OpenRewrite does deterministic AST rewrites at scale. Grit targets the same problem with codemod-style DSL. The production pattern combines both: a deterministic substrate for safe rewrites plus an agent layer for the ambiguous cases, a sandbox for per-branch builds, and a test harness that flips green before the PR opens. The capstone is to migrate 50 real repos and publish a pass rate with a failure taxonomy.

> **【中文解读】** 本节是综合项目——构建代码迁移 Agent，自动将代码从一种框架迁移到另一种。


**Type:** Capstone | **类型:** Capstone
**Languages:** Python (agent), Java / Python (targets), TypeScript (dashboard) | **语言:** Python (agent), Java / Python (targets), TypeScript (dashboard)
**Prerequisites:** Phase 5 (NLP), Phase 7 (transformers), Phase 11 (LLM engineering), Phase 13 (tools), Phase 14 (agents), Phase 15 (autonomous), Phase 17 (infrastructure)

> 🔗 **【前置】** 顶点项目 09 = 综合 Phase 5/7/11/13/14/15/17。代码迁移 Agent = Amazon MigrationBench / Google App Engine 迁移器 / Moderne OpenRewrite / Grit。
> 💡 **【类比】** 代码迁移 = "AI 翻译官"。Java 8→17、Python 2→3。生产模式：确定性 AST 重写（OpenRewrite）处理简单情况 + Agent 处理模糊情况 + 沙箱分支构建 + 测试通过才开 PR。目标：迁移 50 个真实仓库+发布通过率+失败分类。| **前置知识:** Phase 5 (NLP), Phase 7 (transformers), Phase 11 (LLM engineering), Phase 13 (tools), Phase 14 (agents), Phase 15 (autonomous), Phase 17 (infrastructure)
**Phases exercised:** P5 · P7 · P11 · P13 · P14 · P15 · P17 | **涉及阶段:** P5 · P7 · P11 · P13 · P14 · P15 · P17
**Time:** 30 hours | **时间:** 30 hours

## Problem | 问题引入

> **【中文解读】** 本节描述大规模代码迁移的 Agent 应用。代码迁移是编码 Agent 最干净的生产应用之一——ground truth 明确（迁移后测试是否通过？）、奖励真实（Java 8 舰队迁移是人力密集项目）、基准公开（MigrationBench 50 仓库子集）。确定性工具（OpenRewrite/libcst）处理 70-80% 的机械化重写，Agent 层处理模糊情况：构建系统漂移、传递依赖冲突、测试抖动、自定义注解。

> **【拓展：代码迁移产业实践】** Amazon MigrationBench（Java 8→17，50 仓库基准）和 Google App Engine Py2→Py3 迁移器是 2026 年标杆。Moderne 的 OpenRewrite 在大规模确定性 AST 重写上领先，Grit 用 codemod DSL 解决同类问题。生产模式是两层架构：确定性基底处理安全重写 + Agent 层处理歧义情况。每个仓库在 Daytona 沙箱中迭代：构建→分类失败→修复→重跑，硬限制 30 分钟/$8/20 轮。

Large-scale code migration is one of the cleanest production applications of 2026 coding agents. The ground truth is obvious (does the test suite pass after the migration?), the rewards are real (a Java-8 fleet migration is a headcount-scale project), and the benchmarks are public (MigrationBench 50-repo subset). Moderne's OpenRewrite handles the deterministic side. The agent layer handles everything OpenRewrite recipes cannot: ambiguous rewrites, build-system drift, long-tail syntax, transitive dependency breakage.

> 大规模代码迁移是 2026 年编码 Agent 最干净的生产应用之一。基准真相是明显的（迁移后测试套件是否通过？），奖励是真实的（Java 8 舰队迁移是人力规模的项目），基准是公开的（MigrationBench 50 仓库子集）。Moderne 的 OpenRewrite 处理确定性侧。Agent 层处理 OpenRewrite 配方无法处理的一切：模糊重写、构建系统漂移、长尾语法、传递依赖破坏。

You will build an agent that takes a Java 8 repo (or Python 2 repo) and produces a green-CI migrated branch. You will measure pass rate, test-coverage preservation, cost per repo, and build a failure taxonomy. The side-by-side against a deterministic-only baseline tells you where the agent's value actually lives.

> 你将构建一个 Agent，它接受一个 Java 8 仓库（或 Python 2 仓库）并产生一个绿色 CI 的迁移分支。你将测量通过率、测试覆盖率保持、每仓库成本，并构建一个失败分类学。与仅确定性基线的并排比较告诉你 Agent 的价值到底在哪里。

## Concept | 核心概念

> **【中文解读】** 管道分两层：确定性基底（OpenRewrite 处理 Java 的导入/方法签名/空安全/try-with-resources 等机械化重写）和 Agent 层（Claude Opus 4.7 / GPT-5.4-Codex 处理构建文件升级、传递依赖冲突、测试抖动、自定义注解）。每个仓库在 Daytona 沙箱中独立运行，迭代直到全部测试通过且覆盖率不下降，否则归入失败分类。

> **【拓展：失败分类学】** 50 个仓库的迁移失败分类是本项目的核心交付物。典型分类：dep_upgrade_required（传递依赖需升级）、build_tool_drift（构建工具版本差异）、custom_annotation（自定义注解）、test_flake（无关测试抖动）、syntax_edge_case（语法边界情况）、budget_exhausted（预算耗尽）。每种分类附带计数和示例 diff，为后续 recipe 开发提供方向。

The pipeline has two layers. The **deterministic substrate** (OpenRewrite for Java, libcst for Python) runs the bulk of mechanical rewrites safely: imports, method signatures, null-safety edits, try-with-resources, deprecated API replacements. It is fast and produces auditable diffs. The **agent layer** (OpenAI Agents SDK or LangGraph over Claude Opus 4.7 and GPT-5.4-Codex) handles cases the recipes cannot: build-file upgrades (Maven/Gradle/pyproject), transitive dependency conflicts, test flakes, custom annotations.

> 管道有两层。**确定性基底**（Java 用 OpenRewrite，Python 用 libcst）安全地运行大量机械化重写：导入、方法签名、空安全编辑、try-with-resources、弃用 API 替换。它快速且产生可审计的 diff。**Agent 层**（OpenAI Agents SDK 或基于 Claude Opus 4.7 和 GPT-5.4-Codex 的 LangGraph）处理配方无法处理的情况：构建文件升级（Maven/Gradle/pyproject）、传递依赖冲突、测试抖动、自定义注解。

Each repo gets a Daytona sandbox with the target runtime preinstalled. The agent iterates: run build, classify failures, apply fix, rerun. Hard limits: 30 minutes per repo, $8 per repo, 20 agent turns. If all tests pass and the coverage delta is not negative, the branch opens a PR. If not, the repo gets filed under a failure class with evidence.

> 每个仓库获得一个预装目标运行时的 Daytona 沙箱。Agent 迭代：运行构建、分类失败、应用修复、重跑。硬性限制：每仓库 30 分钟、$8、20 轮 Agent 调用。如果所有测试通过且覆盖率差值不为负，分支打开 PR。否则，仓库被归入带证据的失败分类。

The failure taxonomy is the deliverable. Across 50 repos, what broke? Transitive deps? Custom annotations? Build tool version? Test flakes unrelated to migration? Each class gets a count and an exemplar diff. Future recipe authors can target the top three.

> 失败分类学是交付物。在 50 个仓库中，什么破坏了？传递依赖？自定义注解？构建工具版本？与迁移无关的测试抖动？每个分类获得一个计数和一个示例 diff。未来的配方作者可以针对前三名。

## Architecture | 架构

```
target repo
      |
      v
OpenRewrite / libcst deterministic recipes
   (safe, fast, auditable, ~70-80% of fixes)
      |
      v
Daytona sandbox per branch
      |
      v
agent loop (Claude Opus 4.7 / GPT-5.4-Codex):
   - run build -> capture failures
   - classify failures (build, test, lint)
   - apply fix (patch or retry recipe)
   - rerun
   - budget: 30 min, $8, 20 turns
      |
      v
test + coverage delta gate
      |
      v (passed)
open PR
      |
      v (failed)
file under failure class + attach repro
```

## Stack | 技术栈

- Deterministic substrate: OpenRewrite (Java) or libcst (Python)
  中文翻译：Deterministic substrate: OpenRewrite (Java) or libcst (Python)
- Agent: OpenAI Agents SDK or LangGraph over Claude Opus 4.7 + GPT-5.4-Codex
  中文翻译：Agent: OpenAI Agents SDK or LangGraph over Claude Opus 4.7 + GPT-5.4-Codex

> 中文翻译：Agent: OpenAI Agents SDK or LangGraph over Claude Opus 4.7 + GPT-5.4-Codex（翻译）

- Sandbox: Daytona devcontainers per branch, pre-installed target runtime (Java 17 / Python 3.12)
  中文翻译：Sandbox: Daytona devcontainers per branch, pre-installed target runtime (Java 17 / Python 3.12)

> 中文翻译：Sandbox: Daytona devcontainers per branch, pre-installed target runtime (Java 17 / Python 3.12)（翻译）

- Build systems: Maven, Gradle, uv (Python)
  中文翻译：Build systems: Maven, Gradle, uv (Python)
- Benchmarks: Amazon MigrationBench 50-repo subset (Java 8 to 17), Google App Engine Py2-to-Py3 repos
  中文翻译：Benchmarks: Amazon MigrationBench 50-repo subset (Java 8 to 17), Google App Engine Py2-to-Py3 repos

> 中文翻译：Benchmarks: Amazon MigrationBench 50-repo subset (Java 8 to 17), Google App Engine Py2-to-Py3 repos（翻译）

- Test harness: parallel runner, coverage via Jacoco (Java) or coverage.py (Python)
  中文翻译：Test harness: parallel runner, coverage via Jacoco (Java) or coverage.py (Python)
- Observability: Langfuse + trace bundle per repo with every diff chunk
  中文翻译：Observability: Langfuse + trace bundle per repo with every diff chunk
- Dashboard: failure-taxonomy dashboard with per-class counts and exemplar diffs
  中文翻译：Dashboard: failure-taxonomy dashboard with per-class counts and exemplar diffs

## Build It | 动手构建

> **【中文解读】** 构建代码迁移 Agent 的 8 个阶段：先运行确定性迁移脚本（OpenRewrite/libcst）处理 70-80% 的机械性变更，再让 Agent 处理剩余的语义级迁移。每个迁移任务在 Daytona 沙箱中运行，构建失败时自动移交给 Agent。

> **【拓展：AI 代码迁移在企业中的应用】** 2026 年的代码迁移场景：Java 8 -> 17+、Python 2 -> 3（长尾）、AngularJS -> React、REST -> GraphQL。Amazon Q Developer Agent 专门支持 AWS 服务迁移。GPT-5 和 Claude 在代码迁移中的优势在于理解跨文件依赖和 API 语义变化——确定性脚本只能做语法级转换，Agent 能理解"这个方法签名变了，调用方需要适配新参数"。

1. **Recipe pass.** Run OpenRewrite (Java) or libcst (Python) recipes first. Catch the 70-80% of migrations that are mechanical. Commit as "recipe" commit.
   中文翻译：1. **Recipe pass.** Run OpenRewrite (Java) or libcst (Python) recipes first. Catch the 70-80% of migrations that are mechanical. Commit as "recipe" commit.

2. **Build trial.** Daytona sandbox: install target runtime, run the build. If green, skip to tests. If red, hand off to agent.
   中文翻译：2. **Build trial.** Daytona sandbox: install target runtime, run the build. If green, skip to tests. If red, hand off to agent.

3. **Agent loop.** LangGraph with tools: `run_build`, `read_file`, `edit_file`, `run_test`, `git_diff`. Agent classifies the failure (dep, syntax, test, build-tool) and applies a targeted fix. Rerun.
   中文翻译：3. **Agent loop.** LangGraph with tools: `run_build`, `read_file`, `edit_file`, `run_test`, `git_diff`. Agent classifies the failure (dep, syntax, test, build-tool) and applies a targeted fix. Rerun.

4. **Budget caps.** 30 minutes wall-clock per repo, $8 cost, 20 agent turns. Any breach halts and files under "budget_exhausted" with the current diff.
   中文翻译：4. **Budget caps.** 30 minutes wall-clock per repo, $8 cost, 20 agent turns. Any breach halts and files under "budget_exhausted" with the current diff.

5. **Test + coverage gate.** After the build goes green, run the test suite. Compare coverage to the base repo. If coverage dropped more than 2%, file under "coverage_regression".
   中文翻译：5. **Test + coverage gate.** After the build goes green, run the test suite. Compare coverage to the base repo. If coverage dropped more than 2%, file under "coverage_regression".

6. **PR open.** On success, push the branch, open the PR with the diff and a summary of which recipes applied and which commits the agent authored.
   中文翻译：6. **PR open.** On success, push the branch, open the PR with the diff and a summary of which recipes applied and which commits the agent authored.

7. **Failure taxonomy.** For each failed repo, tag with a class: `dep_upgrade_required`, `build_tool_drift`, `custom_annotation`, `test_flake`, `syntax_edge_case`, `budget_exhausted`. Build a dashboard.
   中文翻译：7. **Failure taxonomy.** For each failed repo, tag with a class: `dep_upgrade_required`, `build_tool_drift`, `custom_annotation`, `test_flake`, `syntax_edge_case`, `budget_exhausted`. Build a dashboard.

8. **50-repo run.** Execute across the MigrationBench subset. Report per-class pass rate, cost-per-repo, coverage-preservation, and a compare-vs-deterministic-only baseline.
   中文翻译：8. **50-repo run.** Execute across the MigrationBench subset. Report per-class pass rate, cost-per-repo, coverage-preservation, and a compare-vs-deterministic-only baseline.

## Use It | 使用方法

```
$ migrate legacy-java-service --target java17
[recipe]   27 rewrites applied (JUnit 4->5, HashMap initializer, try-with-resources)
[build]    FAIL: cannot find symbol sun.misc.BASE64Encoder
[agent]    turn 1 classify: removed_jdk_api
[agent]    turn 2 apply: sun.misc.BASE64Encoder -> java.util.Base64
[build]    OK
[tests]    412/412 passing; coverage 84.1% -> 84.3%
[pr]       opened #1841  cost=$3.20  turns=4
```

## Ship It | 部署上线

`outputs/skill-migration-agent.md` is the deliverable. Given a repo, it executes deterministic recipes then an agent loop to produce a green migrated branch, or files the repo under a taxonomy class.

> `outputs/skill-migration-agent.md` 是交付物。给定仓库，它执行确定性配方然后 Agent 循环以产生绿色迁移分支，或将仓库归入分类学分类。

| Weight | Criterion | How it is measured |
| 权重 | 标准 | 如何衡量 |
|:-:|---|---|
| 25 | MigrationBench pass rate | 50-repo subset pass@1 |
| 25 | MigrationBench 通过率 | 50 仓库子集 pass@1 |
| 20 | Test-coverage preservation | Mean coverage delta vs base |
| 20 | 测试覆盖率保持 | 与基础仓库的平均覆盖率差值 |
| 20 | Cost per migrated repo | $/repo on passing runs |
| 20 | 每迁移仓库成本 | 通过运行中的 $/仓库 |
| 20 | Agent / deterministic-tool integration | Fraction of fixes that OpenRewrite handled vs agent authored |
| 20 | Agent / 确定性工具集成 | OpenRewrite 处理的修复比例 vs Agent 编写的 |
| 15 | Failure analysis write-up | Taxonomy completeness with exemplars |
| 15 | 失败分析报告 | 带示例的分类学完整性 |
| **100** | | |

## Exercises | 练习题

1. Run the migrate pipeline with OpenRewrite only (no agent). Compare pass rate to the full pipeline. Identify the cases where the agent alone is the difference.
   中文翻译：仅用 OpenRewrite（无 Agent）运行迁移管道。将通过率与完整管道比较。识别仅 Agent 是差异的情况。

> 中文翻译：仅用 OpenRewrite（无 Agent）运行迁移管道。将通过率与完整管道比较。识别仅 Agent 是差异的情况。（翻译）


2. Implement a "lint-clean" check: after migration, run a style linter (spotless for Java, ruff for Python). Fail the PR if new lint errors appear. Measure the coverage-preserved-but-style-regressed rate.
   中文翻译：实现"lint-clean"检查：迁移后运行风格 linter（Java 用 spotless，Python 用 ruff）。如果出现新的 lint 错误则 PR 失败。测量覆盖率保持但风格退化的比率。

> 中文翻译：实现"lint-clean"检查：迁移后运行风格 linter（Java 用 spotless，Python 用 ruff）。如果出现新的 lint 错误则 PR 失败。测量覆盖率保持但风格退化的比率。（翻译）


3. Add a "minimal-diff" optimizer: after the agent's branch passes tests, trim unnecessary changes with a second pass. Report diff-size reduction.
   中文翻译：添加"最小 diff"优化器：Agent 分支通过测试后，用第二轮修剪不必要的变更。报告 diff 大小减少。

> 中文翻译：添加"最小 diff"优化器：Agent 分支通过测试后，用第二轮修剪不必要的变更。报告 diff 大小减少。（翻译）


4. Extend to a third migration: Node 18 to Node 22. Reuse the sandbox wrapping; swap the recipe layer for a custom codemod.
   中文翻译：扩展到第三种迁移：Node 18 到 Node 22。复用沙箱包装；将配方层换为自定义 codemod。

5. Measure time-to-first-green-build (TTFGB) as a UX metric. Target: p50 under 10 minutes.
   中文翻译：测量首次绿色构建时间（TTFGB）作为 UX 指标。目标：p50 低于 10 分钟。

## Key Terms | 关键术语

| Term | What people say | What it actually means |
| 术语 | 通俗说法 | 实际含义 |
|------|-----------------|------------------------|
| Deterministic substrate | "Recipe engine" | OpenRewrite / libcst: declarative AST rewrites with safety guarantees |
| 确定性基底 | "配方引擎" | OpenRewrite / libcst：带安全保证的声明式 AST 重写 |
| Codemod | "Code-modifying program" | A rewrite rule that changes source code mechanically |
| Codemod | "代码修改程序" | 机械地改变源代码的重写规则 |
| Build drift | "Tool version skew" | Subtle Maven / Gradle / uv behavior changes between major versions |
| 构建漂移 | "工具版本偏差" | 主要版本之间 Maven / Gradle / uv 的细微行为变化 |
| Failure class | "Taxonomy bucket" | A labeled reason a repo did not migrate: dep, syntax, test, build-tool, budget |
| 失败分类 | "分类学桶" | 仓库未能迁移的标记原因：依赖、语法、测试、构建工具、预算 |
| Coverage delta | "Coverage preservation" | Change in test coverage % from base to migrated branch |
| 覆盖率差值 | "覆盖率保持" | 从基础到迁移分支的测试覆盖率变化 |
| Agent turn | "Tool-call round" | One plan -> act -> observe cycle in the agent loop |
| Agent 轮次 | "工具调用轮" | Agent 循环中的一个规划 -> 执行 -> 观察周期 |
| Budget exhaustion | "Hit the ceiling" | The repo consumed its 30-min / $8 / 20-turn limit without passing |
| 预算耗尽 | "触及上限" | 仓库消耗了 30 分钟 / $8 / 20 轮限制但未通过 |

## Further Reading | 延伸阅读

- [Amazon MigrationBench](https://aws.amazon.com/blogs/devops/amazon-introduces-two-benchmark-datasets-for-evaluating-ai-agents-ability-on-code-migration/) — the canonical 2026 benchmark
  中文翻译：2026 年规范基准
- [Moderne.io OpenRewrite platform](https://www.moderne.io) — the deterministic substrate reference
  中文翻译：确定性基底参考
- [OpenRewrite documentation](https://docs.openrewrite.org) — recipe authoring
  中文翻译：配方编写
- [Grit.io](https://www.grit.io) — alternate codemod DSL
  中文翻译：备选 codemod DSL
- [OpenAI sandboxed migration cookbook](https://developers.openai.com/cookbook/examples/agents_sdk/sandboxed-code-migration/sandboxed_code_migration_agent) — the Agents SDK reference
  中文翻译：Agents SDK 参考
- [Google App Engine Py2 to Py3 migrator](https://cloud.google.com/appengine) — alternate migration benchmark
  中文翻译：备选迁移基准
- [libcst](https://github.com/Instagram/LibCST) — Python deterministic substrate
  中文翻译：Python 确定性基底
- [Daytona sandboxes](https://daytona.io) — reference per-branch sandbox
  中文翻译：参考每分支沙箱
