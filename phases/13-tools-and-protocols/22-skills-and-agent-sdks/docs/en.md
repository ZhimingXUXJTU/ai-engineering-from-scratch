# Skills and Agent SDKs — Anthropic Skills, AGENTS.md, OpenAI Apps SDK | Skills 与 Agent SDK：Anthropic Skills、AGENTS.md 与 OpenAI Apps SDK

> MCP says "what tools exist." Skills say "how to do a task." The 2026 stack layers both. Anthropic's Agent Skills (open standard, December 2025) ship as SKILL.md with progressive disclosure. OpenAI's Apps SDK is MCP plus widget metadata. AGENTS.md (now in 60,000+ repos) sits at the repo root as project-level agent context. This lesson names what each covers and builds a minimal SKILL.md + AGENTS.md bundle that travels across agents.

> **【中文解读】** MCP 说"有哪些工具"。Skills 说"如何完成任务"。2026 年技术栈将两者分层。Anthropic 的 Agent Skills（2025年12月开放标准）以 SKILL.md 发货，支持渐进式披露。OpenAI 的 Apps SDK 是 MCP 加上小组件元数据。AGENTS.md（已在 60,000+ 仓库中）位于仓库根目录作为项目级 Agent 上下文。本课命名每个覆盖的范围并构建最小 SKILL.md + AGENTS.md 包。

> **【拓展】** 三层堆栈是 2026 年 AI Agent 开发的标准模式：AGENTS.md（项目级约定）+ SKILL.md（可复用工作流）+ MCP 服务器（可调用工具）。Anthropic Claude Agent SDK 和 SkillKit 等跨 Agent 分发层让一个 SKILL.md 可以自动翻译为 32+ AI Agent 的原生格式。

> 🔗 **【前置】** 学本节前请先掌握：(1) Phase 13·07（MCP server）——MCP 是三层中的工具层；(2) Markdown + YAML frontmatter 基础；(3) 至少用过 Claude Code 或 Cursor 等 AI coding agent，体会"项目上下文"的痛点。

**Type:** Learn | **类型:** 学习
**Languages:** Python (stdlib, SKILL.md parser and loader) | **语言:** Python（标准库，SKILL.md 解析器与加载器）
**Prerequisites:** Phase 13 · 07 (MCP server) | **前置知识:** Phase 13 · 07（MCP 服务器）
**Time:** ~45 minutes | **时间:** ~45 分钟

## Learning Objectives | 学习目标

- Distinguish the three layers: AGENTS.md (project context), SKILL.md (reusable know-how), MCP (tools).
  中文翻译：区分三层：AGENTS.md（项目上下文）、SKILL.md（可复用知识）、MCP（工具）。
- Write a SKILL.md with YAML frontmatter and progressive disclosure.
  中文翻译：编写带 YAML frontmatter 和渐进式披露的 SKILL.md。
- Load skills filesystem-style into an agent runtime.
  中文翻译：以文件系统方式将技能加载到 Agent 运行时。
- Compose a skill with an MCP server and an AGENTS.md so one package works in Claude Code, Cursor, and Codex.

> **【中文解读】** 学习目标：区分三层（AGENTS.md 项目上下文、SKILL.md 可复用知识、MCP 工具）；编写带 YAML frontmatter 和渐进式披露的 SKILL.md；以文件系统方式加载技能到 Agent 运行时；组合 SKILL.md + MCP 服务器 + AGENTS.md 使一个包在多个 Agent 中通用。

## The Problem | 问题引入

> **【中文解读】** 工程师将发版说明写作工作流提炼为多步骤提示词，放在 Notion 文档中。现在想在 Claude Code、Cursor 和 Codex CLI 中使用，但每个 Agent 加载指令的方式不同。AGENTS.md 和 SKILL.md 一起解决这一问题：AGENTS.md 位于仓库根目录，每个兼容 Agent 在会话启动时读取；SKILL.md 是可移植的技能包。三层、一个可移植工件。

An engineer distills a release-notes-writing workflow into a multi-step prompt: "Read the latest merged PRs. Group by area. Summarize each. Write a changelog entry following the team's style. Post to Slack draft." They put it in a Notion doc for their team.

> 工程师将发版说明写作工作流提炼为多步 prompt："读最近合并的 PR。按领域分组。摘要每个。按团队风格写 changelog 条目。发到 Slack 草稿。"他们放在 Notion 文档中供团队使用。

Now they want to use this workflow from Claude Code, Cursor, and Codex CLI. Each agent has a different way to load instructions: Claude Code slash-commands, Cursor rules, Codex `.codex.md`. The engineer copies the workflow three times and maintains three copies.

> 现在他们想从 Claude Code、Cursor 和 Codex CLI 使用此工作流。每个 Agent 有不同的加载指令方式：Claude Code 斜杠命令、Cursor 规则、Codex `.codex.md`。工程师复制工作流三次并维护三个副本。

AGENTS.md and SKILL.md together fix this:

> AGENTS.md 和 SKILL.md 一起修复此问题：

- **AGENTS.md** sits at the repo root. Every compatible agent reads it on session start. "How does this project work? What are the conventions? Which commands run tests?"
  中文翻译：**AGENTS.md** 位于仓库根目录。每个兼容 Agent 在会话启动时读取它。"此项目如何工作？有哪些约定？哪些命令运行测试？"
- **SKILL.md** is a portable bundle: YAML frontmatter (name, description) + markdown body + optional resources. Agents that support skills load them by name on demand.
  中文翻译：**SKILL.md** 是可移植包：YAML frontmatter（名、描述）+ markdown 正文 + 可选资源。支持技能的 Agent 按需按名加载。
- **MCP** (Phase 13 · 06-14) handles the tools the skill needs to invoke.
  中文翻译：**MCP**（Phase 13 · 06-14）处理技能需调用的工具。

Three layers, one portable artifact.

> 三层，一个可移植工件。

> 💡 **【类比】** 三层堆栈像软件公司的"职位说明书 + 操作手册 + 工具箱"分工：(1) **AGENTS.md** = 公司入职手册——告诉新人"我们用 TypeScript、跑 pnpm test"，每个项目一份；(2) **SKILL.md** = 操作手册——"如何写发版说明"是具体流程，可跨公司复用（你跳槽到下家也能用）；(3) **MCP server** = 工具箱——里面是具体工具（GitHub CLI、Slack API）。新人入职读手册（AGENTS.md）、按需学操作手册（SKILL.md）、用工具（MCP）干活。三者解耦，每个都能独立复用。

## The Concept | 核心概念

### AGENTS.md (agents.md)

Launched late 2025, adopted by 60,000+ repos by April 2026. One file at repo root. Format:

> 2025 年末发布，截至 2026 年 4 月被 60,000+ 仓库采用。一个文件在仓库根目录。格式：

```markdown
# Project: my-service

## Conventions
- TypeScript with strict mode.
- Use Pydantic for models on the Python side.
- Tests run with `pnpm test`.

## Build and run
- `pnpm dev` for local dev server.
- `pnpm build` for production bundle.
```

Agents read this on session start and use it to calibrate their behavior for that project. Every coding agent in 2026 supports AGENTS.md: Claude Code, Cursor, Codex, Copilot Workspace, opencode, Windsurf, Zed.

> Agent 在会话启动时读此并用它为该项目校准行为。2026 年每个编码 Agent 都支持 AGENTS.md：Claude Code、Cursor、Codex、Copilot Workspace、opencode、Windsurf、Zed。

> ⚠️ **【易错点】** 场景：把 SKILL.md 写成 5000 字的详尽文档 / 后果：每次触发技能模型上下文被爆掉，反而降低质量；YAML frontmatter 字段缺失或不规范，跨 Agent 加载失败 / 修复：(1) SKILL.md 主体 < 500 字，详细资源放 `resources/*.md` 用渐进式披露；(2) frontmatter 必填 `name` 和 `description`，描述用"Use when X. Do not use for Y." 模式；(3) 测试技能在多个 Agent（Claude Code/Cursor）下加载是否成功，差异通常是 frontmatter 字段命名。

> 🤔 **【困惑】** Q: SKILL.md 和 MCP prompts 有什么区别？不都是预设工作流吗？ A: 三点核心差异：(1) **载体**——MCP prompts 是协议消息（运行时获取），SKILL.md 是文件（文件系统加载）；(2) **触发**——MCP prompts 是 slash command 显式触发，SKILL.md 是模型读 description 后自动决定何时用；(3) **可移植性**——SKILL.md 跨所有 Agent 通用，MCP prompts 只在支持 MCP 的客户端用。两者互补：复杂逻辑放 MCP prompts（能调 sampling），简单工作流放 SKILL.md（更轻量）。

### SKILL.md format

Anthropic's Agent Skills (released as an open standard December 2025):

> Anthropic 的 Agent Skills（2025 年 12 月作为开放标准发布）：

```markdown
---
name: release-notes-writer
description: Write a changelog entry for the latest merged PRs following this project's style.
---

# Release notes writer

When invoked, run these steps:

1. List PRs merged since the last tag. Use `gh pr list --base main --state merged`.
2. Group by label: feature, fix, chore, docs.
3. For each PR in each group, write one line: `- <title> (#<num>)`.
4. Draft the release notes and stage them in CHANGELOG.md.

If the user says "ship", run `git tag vX.Y.Z` and `gh release create`.

## Notes

- Never include commits without a PR.
- Skip "chore" entries from the public changelog.
```

Frontmatter declares the skill's identity. The body is the prompt shown to the model when the skill loads.

> Frontmatter 声明技能的身份。正文是技能加载时显示给模型的 prompt。

### Progressive disclosure

Skills can reference sub-resources that the agent fetches only when needed. Example:

> 技能可引用 Agent 仅在需要时获取的子资源。示例：

```
skills/
  release-notes-writer/
    SKILL.md
    style-guide.md
    template.md
    scripts/
      generate.sh
```

SKILL.md says "see style-guide.md for the style rules." The agent pulls style-guide.md only when the skill is actively running. This avoids bloating the prompt with detail the model may not need.

> SKILL.md 说"参见 style-guide.md 了解风格规则"。Agent 仅在技能激活运行时拉取 style-guide.md。这避免用模型可能不需要的细节膨胀 prompt。

### Filesystem discovery

Agent runtimes scan known directories for SKILL.md files:

> Agent 运行时扫描已知目录的 SKILL.md 文件：

- `~/.anthropic/skills/*/SKILL.md`
  中文翻译：`~/.anthropic/skills/*/SKILL.md`（用户全局）。
- Project `./skills/*/SKILL.md`
  中文翻译：项目 `./skills/*/SKILL.md`（项目级）。
- `~/.claude/skills/*/SKILL.md`
  中文翻译：`~/.claude/skills/*/SKILL.md`（Claude Code 用户级）。

Loading is by folder name and frontmatter `name`. Claude Code, Anthropic Claude Agent SDK, and SkillKit (cross-agent) all follow this pattern.

> 加载按文件夹名和 frontmatter `name`。Claude Code、Anthropic Claude Agent SDK 和 SkillKit（跨 Agent）都遵循此模式。

### Anthropic Claude Agent SDK

`@anthropic-ai/claude-agent-sdk` (TypeScript) and `claude-agent-sdk` (Python) load skills at session start, expose them as callable "agents" inside the runtime. The agent loop dispatches to a skill when the user invokes it.

> `@anthropic-ai/claude-agent-sdk`（TypeScript）和 `claude-agent-sdk`（Python）在会话启动时加载技能，将它们作为运行时内可调用的"agent"暴露。Agent 循环在用户调用时分发到技能。

### OpenAI Apps SDK

Launched October 2025; built directly on MCP. Unifies OpenAI's prior Connectors and Custom GPT Actions under a single developer surface. An Apps SDK app is:

> 2025 年 10 月发布；直接建立在 MCP 上。统一 OpenAI 先前的 Connectors 和 Custom GPT Actions 为单一开发者表面。Apps SDK 应用是：

- An MCP server (tools, resources, prompts).
  中文翻译：一个 MCP 服务器（tools、resources、prompts）。
- Plus widget metadata for ChatGPT's UI.
  中文翻译：加上 ChatGPT UI 的小组件元数据。
- Plus an optional MCP Apps `ui://` resource for interactive surfaces.
  中文翻译：加上可选的 MCP Apps `ui://` 资源用于交互式表面。

Same protocol, richer UX.

> 相同协议，更丰富 UX。

### Cross-agent portability via SkillKit

Tools like SkillKit and similar cross-agent distribution layers translate a single SKILL.md into the native format of each of 32+ AI agents (Claude Code, Cursor, Codex, Gemini CLI, OpenCode, etc.). One source of truth; many consumers.

> SkillKit 等工具和类似跨 Agent 分发层将单个 SKILL.md 翻译为 32+ AI Agent（Claude Code、Cursor、Codex、Gemini CLI、OpenCode 等）的原生格式。单一真相源；多消费者。

### The three-layer stack

| Layer | File | Loaded when | Purpose |
|-------|------|-------------|---------|
| AGENTS.md | repo root | session start | project-level conventions |
| SKILL.md | skills directory | skill invoked | reusable workflow |
| MCP server | external process | tools needed | callable actions |

All three compose: the agent reads AGENTS.md on session start, the user invokes a skill, the skill's instructions include MCP tool calls, the agent dispatches via an MCP client.

> 三者组合：Agent 在会话启动时读 AGENTS.md、用户调用技能、技能的指令包含 MCP 工具调用、Agent 通过 MCP 客户端分发。

## Use It | 用框架实现

> **【中文解读】** `code/main.py` 实现标准库 SKILL.md 解析器和加载器：在 `./skills/` 下发现技能文件，解析 YAML frontmatter 和 markdown 正文，生成按技能名索引的字典。然后模拟 Agent 循环按名称调用 `release-notes-writer`。关注点：YAML 用最小标准库解析器（无 pyyaml 依赖）；技能正文原样存储，调用时拼接到系统提示前；渐进式披露通过 `read_subresource` 按需拉取引用文件。

`code/main.py` ships a stdlib SKILL.md parser and loader. It discovers skills under `./skills/`, parses the YAML frontmatter plus markdown body, and produces a dict keyed by skill name. It then simulates an agent loop that invokes `release-notes-writer` by name.

> `code/main.py` 提供标准库 SKILL.md 解析器和加载器。它在 `./skills/` 下发现技能、解析 YAML frontmatter 和 markdown 正文、生成按技能名索引的字典。然后模拟按名调用 `release-notes-writer` 的 Agent 循环。

What to look at:

- YAML frontmatter parsed with a minimal stdlib parser (no `pyyaml` dependency).
  中文翻译：YAML frontmatter 用最小标准库解析器解析（无 `pyyaml` 依赖）。
- Skill body stored verbatim; agent prepends it to the system prompt on invocation.
  中文翻译：技能正文原样存储；Agent 在调用时前置到系统 prompt。
- Progressive disclosure demoed via a `read_subresource` function that pulls referenced files on demand.
  中文翻译：渐进式披露通过 `read_subresource` 函数演示，按需拉取引用文件。

## Ship It | 产出物

> **【中文解读】** 本课产出 `outputs/skill-agent-bundle.md`——给定一个工作流，生成 SKILL.md + AGENTS.md + MCP 服务器蓝图组合包，可跨 Agent 移植。

This lesson produces `outputs/skill-agent-bundle.md`. Given a workflow, the skill produces the combined SKILL.md + AGENTS.md + MCP-server-blueprint bundle, portable across agents.

> 本课产出 `outputs/skill-agent-bundle.md`。给定一个工作流，该 skill 生成组合的 SKILL.md + AGENTS.md + MCP 服务器蓝图包，可跨 Agent 移植。

## Exercises | 练习题

1. Run `code/main.py`. Add a second skill under `skills/` and confirm the loader picks it up.
   中文翻译：运行 `code/main.py`。在 `skills/` 下添加第二个技能，确认加载器拾取它。

2. Write an AGENTS.md for this course repo. Include testing commands, style conventions, and the Phase 13 mental model.
   中文翻译：为此课程仓库编写 AGENTS.md。包含测试命令、风格约定和 Phase 13 心智模型。

3. Port a multi-step workflow from your team's internal docs into a SKILL.md. Verify it loads in Claude Code.
   中文翻译：将团队内部文档中的多步工作流移植到 SKILL.md。验证它在 Claude Code 中加载。

4. Translate the skill into Cursor's and Codex's native rule formats by hand. Count the diff between formats — this is the translation surface SkillKit automates.
   中文翻译：手动将技能翻译到 Cursor 和 Codex 的原生规则格式。计算格式间 diff——这是 SkillKit 自动化的翻译表面。

5. Read the Anthropic Agent Skills blog post. Identify one feature in the Claude Agent SDK that this lesson's loader does not cover. (Hint: agent sub-invocation.)
   中文翻译：阅读 Anthropic Agent Skills 博客。识别 Claude Agent SDK 中本课加载器未涵盖的一个功能。（提示：Agent 子调用。）

## Key Terms | 术语速查表

| Term | What people say | What it actually means | 中文 |
|------|----------------|------------------------|------|
| SKILL.md | "The skill file" | YAML frontmatter plus markdown body, loaded by agent runtime | 技能文件：YAML 元数据+Markdown 正文 |
| AGENTS.md | "Repo-root agent context" | Project-level conventions file read on session start | 项目级 Agent 上下文文件 |
| Progressive disclosure | "Lazy-load sub-resources" | Skill body references files pulled only when needed | 渐进式披露：按需加载子资源 |
| Frontmatter | "YAML block at top" | Metadata (name, description) in `---` delimiters | YAML 前置元数据 |
| Claude Agent SDK | "Anthropic's skill runtime" | `@anthropic-ai/claude-agent-sdk`, loads skills and routes | Anthropic 的技能运行时 |
| OpenAI Apps SDK | "MCP + widget meta" | OpenAI's dev surface built on MCP plus ChatGPT UI hooks | OpenAI 的 MCP+UI 开发平台 |
| Skill discovery | "Filesystem scan" | Walk known dirs for SKILL.md, key by name | 技能发现：文件系统扫描 |
| Cross-agent portability | "One skill many agents" | Translate one SKILL.md to 32+ agents via SkillKit-style tools | 跨 Agent 可移植性 |
| Agent Skill | "Portable know-how" | Reusable task template outside MCP's tool concept | Agent 技能：可移植的任务模板 |
| Apps SDK | "MCP plus ChatGPT UI" | Connectors and Custom GPTs unified on MCP | Apps SDK：MCP+ChatGPT UI 统一平台 |

## Further Reading | 延伸阅读

- [Anthropic — Agent Skills announcement](https://www.anthropic.com/engineering/equipping-agents-for-the-real-world-with-agent-skills) — December 2025 launch
  中文翻译：2025 年 12 月发布
- [Anthropic — Agent Skills docs](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/overview) — SKILL.md format reference
  中文翻译：SKILL.md 格式参考
- [OpenAI — Apps SDK](https://developers.openai.com/apps-sdk) — MCP-based developer platform for ChatGPT
  中文翻译：基于 MCP 的 ChatGPT 开发者平台
- [agents.md](https://agents.md/) — AGENTS.md format and adoption list
  中文翻译：AGENTS.md 格式和采用列表
- [Anthropic — anthropics/skills GitHub](https://github.com/anthropics/skills) — official skill examples
  中文翻译：官方技能示例
