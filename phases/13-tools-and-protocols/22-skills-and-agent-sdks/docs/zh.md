# Skills 与 Agent SDK — Anthropic Skills、AGENTS.md 与 OpenAI Apps SDK

> MCP 说"有哪些工具"。Skills 说"如何完成任务"。2026 年技术栈将两者分层。Anthropic 的 Agent Skills（2025年12月开放标准）以 SKILL.md 发货，支持渐进式披露。OpenAI 的 Apps SDK 是 MCP 加上小组件元数据。AGENTS.md（已在 60,000+ 仓库中）位于仓库根目录作为项目级 Agent 上下文。本课命名每个覆盖的范围并构建最小 SKILL.md + AGENTS.md 包。

> **【中文解读】** MCP 说"有哪些工具"。Skills 说"如何完成任务"。2026 年技术栈将两者分层。Anthropic 的 Agent Skills 以 SKILL.md 发货，支持渐进式披露。OpenAI 的 Apps SDK 是 MCP 加上小组件元数据。AGENTS.md 位于仓库根目录作为项目级 Agent 上下文。

> **【拓展】** 三层堆栈是 2026 年 AI Agent 开发的标准模式：AGENTS.md（项目级约定）+ SKILL.md（可复用工作流）+ MCP 服务器（可调用工具）。Anthropic Claude Agent SDK 和 SkillKit 等跨 Agent 分发层让一个 SKILL.md 可以自动翻译为 32+ AI Agent 的原生格式。

**类型：** 学习
**语言：** Python（标准库，SKILL.md 解析器和加载器）
**前置条件：** Phase 13 · 07（MCP 服务器）
**时间：** 约 45 分钟

## 学习目标

- 区分三层：AGENTS.md（项目上下文）、SKILL.md（可复用知识）、MCP（工具）。
- 编写带 YAML frontmatter 和渐进式披露的 SKILL.md。
- 以文件系统方式加载技能到 Agent 运行时。
- 组合 SKILL.md + MCP 服务器 + AGENTS.md 使一个包在 Claude Code、Cursor 和 Codex 中通用。

## 问题引入

工程师将发版说明写作工作流提炼为多步骤提示词："读取最新合并的 PR。按领域分组。每个写摘要。按团队风格写 changelog 条目。发到 Slack 草稿。"他们放在 Notion 文档中供团队使用。

现在他们想从 Claude Code、Cursor 和 Codex CLI 中使用此工作流。每个 Agent 有不同的加载指令方式：Claude Code 斜杠命令、Cursor rules、Codex `.codex.md`。工程师复制工作流三次并维护三份。

AGENTS.md 和 SKILL.md 一起解决此问题：

- **AGENTS.md** 位于仓库根目录。每个兼容 Agent 在会话启动时读取。"这个项目怎么工作？约定是什么？哪些命令运行测试？"
- **SKILL.md** 是一个可移植包：YAML frontmatter（名称、描述）+ markdown 正文 + 可选资源。支持技能的 Agent 按名称按需加载。
- **MCP**（Phase 13 · 06-14）处理技能需要调用的工具。

三层、一个可移植工件。

## 核心概念

### AGENTS.md (agents.md)

2025 年末发布，截至 2026 年 4 月已有 60,000+ 仓库采用。一个文件在仓库根目录。格式：

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

Agent 在会话启动时读取此文件并用来校准该项目的行为。2026 年的每个编码 Agent 都支持 AGENTS.md：Claude Code、Cursor、Codex、Copilot Workspace、opencode、Windsurf、Zed。

### SKILL.md 格式

Anthropic 的 Agent Skills（2025年12月作为开放标准发布）：

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

Frontmatter 声明技能的身份。正文是技能加载时显示给模型的提示。

### 渐进式披露

技能可以引用仅在需要时才获取的子资源。示例：

```
skills/
  release-notes-writer/
    SKILL.md
    style-guide.md
    template.md
    scripts/
      generate.sh
```

SKILL.md 说"参见 style-guide.md 了解样式规则"。Agent 仅在技能活跃运行时拉取 style-guide.md。这避免了用模型可能不需要的细节膨胀提示。

### 文件系统发现

Agent 运行时扫描已知目录寻找 SKILL.md 文件：

- `~/.anthropic/skills/*/SKILL.md`
- 项目 `./skills/*/SKILL.md`
- `~/.claude/skills/*/SKILL.md`

按文件夹名和 frontmatter `name` 加载。Claude Code、Anthropic Claude Agent SDK 和 SkillKit（跨 Agent）都遵循此模式。

### Anthropic Claude Agent SDK

`@anthropic-ai/claude-agent-sdk`（TypeScript）和 `claude-agent-sdk`（Python）在会话启动时加载技能，将它们暴露为运行时内部可调用的"agent"。Agent 循环在用户调用时分发到技能。

### OpenAI Apps SDK

2025年10月发布；直接构建在 MCP 上。统一了 OpenAI 之前的 Connectors 和 Custom GPT Actions 为单一开发者表面。Apps SDK 应用是：

- 一个 MCP 服务器（tools、resources、prompts）。
- 加上 ChatGPT UI 的小部件元数据。
- 加上可选的 MCP Apps `ui://` 资源用于交互式表面。

相同协议、更丰富的 UX。

### 通过 SkillKit 的跨 Agent 可移植性

SkillKit 等跨 Agent 分发层将单个 SKILL.md 翻译为 32+ AI Agent 的原生格式（Claude Code、Cursor、Codex、Gemini CLI、OpenCode 等）。一个真相来源；多个消费者。

### 三层堆栈

| 层 | 文件 | 何时加载 | 目的 |
|----|------|---------|------|
| AGENTS.md | 仓库根目录 | 会话启动 | 项目级约定 |
| SKILL.md | skills 目录 | 技能调用 | 可复用工作流 |
| MCP 服务器 | 外部进程 | 需要工具时 | 可调用动作 |

三者组合：Agent 在会话启动时读取 AGENTS.md，用户调用技能，技能指令包含 MCP 工具调用，Agent 通过 MCP 客户端分发。

## 用框架实现

`code/main.py` 提供标准库 SKILL.md 解析器和加载器。它在 `./skills/` 下发现技能文件，解析 YAML frontmatter 和 markdown 正文，并生成按技能名索引的字典。然后模拟 Agent 循环按名称调用 `release-notes-writer`。

关注点：

- YAML frontmatter 用最小标准库解析器解析（无 `pyyaml` 依赖）。
- 技能正文原样存储；调用时拼接到系统提示前。
- 渐进式披露通过 `read_subresource` 按需拉取引用文件演示。

## 产出物

本课产生 `outputs/skill-agent-bundle.md`。给定一个工作流，该技能生成组合的 SKILL.md + AGENTS.md + MCP-服务器-蓝图包，可跨 Agent 移植。

## 练习题

1. 运行 `code/main.py`。在 `skills/` 下添加第二个技能并确认加载器发现它。

2. 为本课程仓库编写 AGENTS.md。包含测试命令、风格约定和 Phase 13 心智模型。

3. 将团队内部文档中的多步工作流移植到 SKILL.md。验证在 Claude Code 中加载。

4. 手动将技能翻译为 Cursor 和 Codex 的原生规则格式。计算格式之间的差异——这是 SkillKit 自动化的翻译表面。

5. 阅读 Anthropic Agent Skills 博文。识别 Claude Agent SDK 中一个本课加载器未覆盖的功能。（提示：agent 子调用。）

## 术语速查表

| 术语 | 人们怎么说 | 实际含义 | 英文 |
|------|-----------|---------|------|
| 技能文件 | "那个技能文件" | YAML frontmatter + markdown 正文，由 Agent 运行时加载 | SKILL.md |
| 项目级 Agent 上下文 | "仓库根 Agent 上下文" | 会话启动时读取的项目级约定文件 | AGENTS.md |
| 渐进式披露 | "懒加载子资源" | 技能正文引用的文件仅在需要时拉取 | Progressive disclosure |
| YAML 前置元数据 | "顶部 YAML 块" | `---` 分隔符中的元数据（名称、描述） | Frontmatter |
| Anthropic 技能运行时 | "Anthropic 的技能运行时" | `@anthropic-ai/claude-agent-sdk`，加载技能并路由 | Claude Agent SDK |
| OpenAI MCP+UI 开发平台 | "MCP + 小部件元数据" | OpenAI 构建在 MCP 上的开发表面，加 ChatGPT UI 钩子 | OpenAI Apps SDK |
| 技能发现 | "文件系统扫描" | 遍历已知目录找 SKILL.md，按名称索引 | Skill discovery |
| 跨 Agent 可移植性 | "一个技能多个 Agent" | 通过 SkillKit 风格工具将一个 SKILL.md 翻译为 32+ Agent | Cross-agent portability |
| Agent 技能 | "可移植知识" | MCP 工具概念之外的可复用任务模板 | Agent Skill |
| Apps SDK | "MCP + ChatGPT UI" | Connectors 和 Custom GPTs 在 MCP 上统一 | Apps SDK |

## 延伸阅读

- [Anthropic — Agent Skills announcement](https://www.anthropic.com/engineering/equipping-agents-for-the-real-world-with-agent-skills) — 2025 年 12 月发布
- [Anthropic — Agent Skills docs](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/overview) — SKILL.md 格式参考
- [OpenAI — Apps SDK](https://developers.openai.com/apps-sdk) — 基于 MCP 的 ChatGPT 开发者平台
- [agents.md](https://agents.md/) — AGENTS.md 格式和采用列表
- [Anthropic — anthropics/skills GitHub](https://github.com/anthropics/skills) — 官方技能示例
