# Capstone: Ship a Reusable Agent Workbench Pack | 工作台 结业 欧盟

> The mini-track ends with a pack you drop into any repo. Eleven lessons of surfaces compressed into a directory you can `cp -r` and have an agent working reliably the next morning. The capstone is the artifact this curriculum trades on.

**Type:** Build | **类型:** 构建
**Languages:** Python (stdlib) | **语言:** Python (标准库)
**Prerequisites:** Phases 14 · 31 to 14 · 41 | **前置知识:** 见原文
**Time:** ~75 minutes | **时间:** 见原文

## Learning Objectives | 学习目标

- Package the seven workbench surfaces into one drop-in directory.
- Pin the schemas, scripts, and templates so a new repo gets a known-good baseline.
- Add a single installer script that lays down the pack idempotently.
- Decide what stays in the pack and what stays out, defending the cut for each.

## The Problem | 问题引入

A workbench that lives in a Google Doc, a chat history, and three half-remembered scripts is a workbench that gets rebuilt every quarter. The cure is a versioned pack: a repo or directory with the surfaces, the schemas, the scripts, and a one-command installer.

> 一个存在于 Google 文档、聊天历史和三个半记忆脚本中的工作台是一个每季度都要重建的工作台。修复是一个版本化的包：一个包含表面、schema、脚本和一条命令安装器的仓库或目录。

You will end this lesson with `outputs/agent-workbench-pack/` shipped on disk and a `bin/install.sh` that drops it into any target repo.

> 你将在这一课结束时在磁盘上交付 `outputs/agent-workbench-pack/` 和一个 `bin/install.sh`，可以将其放入任何目标仓库。


> **【中文解读】** Agent Workbench 顶点项目：将前面 11 课的所有概念整合到一个完整的编码 Agent 中。该 Agent 能够：(1) 理解项目结构和约定；(2) 执行范围受限的修改；(3) 运行验证门检查；(4) 通过审查者 Agent 质检；(5) 跨会话保持状态。这是最小可行生产 Agent 的设计。

## The Concept | 核心概念

```mermaid
flowchart TD
  Pack[agent-workbench-pack/] --> Docs[AGENTS.md + docs/]
  Pack --> Schemas[schemas/]
  Pack --> Scripts[scripts/]
  Pack --> Bin[bin/install.sh]
  Bin --> Repo[target repo]
  Repo --> Surfaces[all seven workbench surfaces wired]
```


> **【中文解读】** 本节介绍了 AI Agent 的核心概念和实现方法。Agent 是 LLM 驱动的自主系统，能够观察环境、思考决策、执行行动并循环迭代直到完成目标。

### The pack layout

```
outputs/agent-workbench-pack/
├── AGENTS.md
├── docs/
│   ├── agent-rules.md
│   ├── reliability-policy.md
│   ├── handoff-protocol.md
│   └── reviewer-rubric.md
├── schemas/
│   ├── agent_state.schema.json
│   ├── task_board.schema.json
│   └── scope_contract.schema.json
├── scripts/
│   ├── init_agent.py
│   ├── run_with_feedback.py
│   ├── verify_agent.py
│   └── generate_handoff.py
├── bin/
│   └── install.sh
└── README.md
```

### What stays in, what stays out

In:

- Surface schemas. They are the contract.
- The four scripts above. They are the runtime.
- The four docs. They are the rules and the rubric.

Out:

- Project-specific tasks. Tasks belong on the target repo's board, not in the pack.
- Vendor SDK calls. The pack is framework-agnostic.
- Onboarding prose. The pack lives next to the team's existing onboarding, not inside it.

### The installer

A short `bin/install.sh` (or `bin/install.py`):

1. Refuses to install over an existing pack without `--force`.
2. Copies the pack into the target repo.
3. Wires up CI if a `.github/workflows/` exists.
4. Prints next steps: fill in the board, set acceptance commands, run the init script.

### Versioning

The pack carries a `VERSION` file. Schema bumps and script changes that require migrations bump the major. Doc-only changes bump the patch. The target repo's `agent_state.json` records which pack version it was initialized against.

> Agent Workbench 毕业项目综合运用 Phase 14 所有知识，在真实代码仓库中构建一个生产级 Agent。

## Build It | 动手实现

`code/main.py` assembles the pack into `outputs/agent-workbench-pack/` next to the lesson, seeded with the schemas and scripts from the previous lessons in this mini-track and the docs you already wrote.

> Agent Workbench 毕业项目综合运用 Phase 14 所有知识，在真实代码仓库中构建一个生产级 Agent。

Run it:

```
python3 code/main.py
```

The script copies and pins the surfaces, writes the README, prints the pack tree, and exits zero. Re-running is idempotent.

> Agent Workbench 毕业项目综合运用 Phase 14 所有知识，在真实代码仓库中构建一个生产级 Agent。

## Production patterns in the wild

A pack is only valuable if it survives forks, updates, and an unfriendly upstream. Four patterns make that work.

> Agent Workbench 毕业项目综合运用 Phase 14 所有知识，在真实代码仓库中构建一个生产级 Agent。

**`VERSION` is the contract, not the marketing.** Major bumps require a state migration. Minor bumps require a checker re-run. Patch bumps are doc-only. The installer writes `.workbench-version` into the target repo on every install; `lint_pack.py` refuses to ship if the target's lock disagrees with the pack's `VERSION`. This is how `npm`, `Cargo`, and `pyproject.toml` survive 10 years of churn; nothing about agents changes the rules.

**Single source for cross-tool distribution.** Nx ships one `nx ai-setup` that lays down `AGENTS.md`, `CLAUDE.md`, `.cursor/rules/`, `.github/copilot-instructions.md`, and an MCP server from a single config. The pack should do the same; the installer emits the symlinks (`ln -s AGENTS.md CLAUDE.md`) so a single source of truth fans out to every coding agent. Forking the pack to support one tool over another is a failure mode.

**`uninstall.sh` that refuses on non-trivial state.** Uninstalling the pack must not delete the user's `agent_state.json`, `task_board.json`, or `outputs/`. The uninstaller removes the schemas, scripts, docs, and `AGENTS.md` (with `--keep-agents-md` opt-out) and refuses to proceed if state files have any uncommitted changes. State belongs to the user; the pack does not own it.

**Skill-as-publishable. SkillKit-style distribution.** The pack ships as a SkillKit skill: `skillkit install agent-workbench-pack` lays it down across 32 AI agents from a single source. The pack repo is the source of truth; SkillKit is the distribution channel. Vendor lock-in collapses; the seven surfaces stay the same.

## Use It | 用框架实现

Three places the pack ships:

- **As a directory you drop into a repo.** `cp -r outputs/agent-workbench-pack /path/to/repo`.
- **As a public template repo.** Fork-and-customize, with `VERSION` controlling drift.
- **As a SkillKit skill.** Wired into your agent product so a single command lays it down.

The pack is the recipe. Each install is a serving.

> Agent Workbench 毕业项目综合运用 Phase 14 所有知识，在真实代码仓库中构建一个生产级 Agent。

## Ship It | 产出物

`outputs/skill-workbench-pack.md` generates a project-tuned pack: rules sharpened to the team's history, scope globs matched to the repo, rubric dimensions extended with one domain-specific entry.

> Agent Workbench 毕业项目综合运用 Phase 14 所有知识，在真实代码仓库中构建一个生产级 Agent。

## Exercises | 练习题

1. Decide which optional fifth doc deserves promotion into the canonical pack. Defend the cut.
  中文翻译：思考并实践此练习。
2. Rewrite the installer as Python with a `--dry-run` flag. Compare ergonomics against bash.
  中文翻译：思考并实践此练习。
3. Add a `bin/uninstall.sh` that safely removes the pack and refuses if state files have non-trivial history. What counts as non-trivial?
  中文翻译：思考并实践此练习。
4. Add a `lint_pack.py` that fails when the pack drifts from `VERSION`. Wire it into CI for the pack's own repo.
  中文翻译：思考并实践此练习。
5. Author the migration runbook from a hand-rolled workbench to this pack. What is the order of operations that minimizes downtime?
  中文翻译：思考并实践此练习。

## Key Terms | 术语速查表

| Term | What people say | What it actually means |
|------|----------------|------------------------|---|
| Workbench pack | "The starter kit" | A versioned directory carrying all seven surfaces |  |
| Installer | "Setup script" | `bin/install.sh` that lays the pack down idempotently |  |
| Pack version | "VERSION" | Major bumps for schema/script changes, patch for doc-only |  |
| Drop-in pack | "cp -r and go" | Pack works without per-repo customization on day one |  |
| Forkable template | "GitHub template" | Public repo that GitHub's "Use this template" can clone from |  |

## Further Reading | 延伸阅读

- Phases 14 · 31 to 14 · 41 — every surface this pack bundles
- [SkillKit](https://github.com/rohitg00/skillkit) — install this skill across 32 AI agents
  中文翻译：见原文。
- [Nx Blog, Teach Your AI Agent How to Work in a Monorepo](https://nx.dev/blog/nx-ai-agent-skills) — single-source generator across six tools
  中文翻译：见原文。
- [agents.md — the open spec](https://agents.md/) — what your pack's router must implement
  中文翻译：见原文。
- [HKUDS/OpenHarness](https://github.com/HKUDS/OpenHarness) — reference implementation of a pack-equivalent
  中文翻译：见原文。
- [andrewgarst/agentic_harness](https://github.com/andrewgarst/agentic_harness) — Redis-backed reference with eval suite
  中文翻译：见原文。
- [Augment Code, A good AGENTS.md is a model upgrade](https://www.augmentcode.com/blog/how-to-write-good-agents-dot-md-files) — pack docs quality bar
  中文翻译：见原文。
- [Anthropic, Effective harnesses for long-running agents](https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents)
  中文翻译：见原文。
- [Anthropic, Harness design for long-running application development](https://www.anthropic.com/engineering/harness-design-long-running-apps)
  中文翻译：见原文。
- Phase 14 · 30 — eval-driven agent development that consumes the pack's verification gate
- Phase 14 · 41 — the before/after benchmark this pack improves on
