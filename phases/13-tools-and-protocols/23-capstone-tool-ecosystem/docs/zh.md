# 毕业项目 — 构建完整的工具生态系统

> Phase 13 教了每个组件。本毕业项目将它们连线为一个生产级系统：MCP 服务器（tools+resources+prompts+tasks+UI）、边缘 OAuth 2.1、RBAC 网关、多服务器客户端、A2A 子 Agent 调用、OTel 全链路追踪、CI 中的工具投毒检测、AGENTS.md + SKILL.md 打包。完成后你能为每个架构选择辩护。

> **【中文解读】** Phase 13 教了每个组件。本毕业项目将它们连线为一个生产级系统：MCP 服务器（tools+resources+prompts+tasks+UI）、边缘 OAuth 2.1、RBAC 网关、多服务器客户端、A2A 子 Agent 调用、OTel 全链路追踪、CI 中的工具投毒检测、AGENTS.md + SKILL.md 打包。

> **【拓展】** 这是 Phase 13 的集大成课程，整合了全部23课内容为一个可运行的端到端系统。架构模式：用户 -> 客户端 -> OAuth 2.1 + RBAC 网关 -> 研究 MCP 服务器（工具/资源/提示词/任务/UI/A2A 调用/OTel span）。这是 Anthropic（Claude Research）和 OpenAI（GPTs with Apps SDK）2026年发布的生产研究助手系统的精确形状。

**类型：** 构建
**语言：** Python（标准库，端到端生态系统线束）
**前置条件：** Phase 13 · 01-21
**时间：** 约 120 分钟

## 学习目标

- 构建一个暴露工具、资源、提示、任务和 `ui://` 应用的 MCP 服务器。
- 在服务器前面放置一个强制 RBAC 和锁定哈希的 OAuth 2.1 网关。
- 编写一个用 OTel GenAI 属性端到端追踪的多服务器客户端。
- 将部分工作负载委托给 A2A 子 Agent；验证不透明性保持。
- 用 AGENTS.md + SKILL.md 打包整个技术栈使其他 Agent 可以驱动它。

## 问题引入

构建"研究和报告"系统：

- 用户请求："总结 2026 年关于 Agent 协议的被引用最多的三篇 arXiv 论文。"
- 系统：通过 MCP 搜索 arXiv；通过 A2A 将论文摘要委托给专门的写作 Agent；聚合结果；渲染交互式报告作为 MCP Apps `ui://` 资源；每步记录到 OTel。

Phase 13 的所有原语都出现了。这不是玩具——Anthropic（Claude Research 产品）、OpenAI（GPTs with Apps SDK）和第三方在 2026 年发布的生产研究助手系统有这个精确形状。

## 核心概念

### 架构

```
[用户] -> [客户端] -> [网关 (OAuth 2.1 + RBAC)] -> [研究 MCP 服务器]
                                                      |
                                                      +- MCP 工具: arxiv_search (纯)
                                                      +- MCP 资源: notes://recent
                                                      +- MCP 提示: /research_topic
                                                      +- MCP 任务: generate_report (长时)
                                                      +- MCP Apps UI: ui://report/current
                                                      +- A2A 调用: writer-agent (tasks/send)
                                                      |
                                                      +- OTel GenAI spans
```

### 追踪层次

```
agent.invoke_agent
 ├── llm.chat (启动)
 ├── mcp.call -> tools/call arxiv_search
 ├── mcp.call -> resources/read notes://recent
 ├── mcp.call -> prompts/get research_topic
 ├── a2a.tasks/send -> writer-agent
 │    └── task transitions (不透明内部)
 ├── mcp.call -> tools/call generate_report (任务增强)
 │    └── tasks/status 轮询
 │    └── tasks/result (completed, 返回 ui:// 资源)
 └── llm.chat (最终综合)
```

一个 trace id。每个 span 有正确的 `gen_ai.*` 属性。

### 安全态势

- OAuth 2.1 + PKCE 带资源指示器将受众绑定到网关。
- 网关持有上游凭证；用户永远看不到。
- RBAC：`alice` 有 `research:read`、`research:write`，可调用所有工具。`bob` 有 `research:read`，不能调用 `generate_report`。
- 锁定描述清单：丢弃任何工具哈希变更的服务器。
- Rule of Two 审计：没有工具组合不可信输入、敏感数据和后果性行为。

### 渲染

最终 `generate_report` 任务返回内容块加 `ui://report/current` 资源。客户端宿主（Claude Desktop 等）在沙盒 iframe 中渲染交互式仪表盘。仪表盘包含排序的论文列表、引用计数和一个按钮，用户点击任何论文时调用 `host.callTool('summarize_paper', {arxiv_id})`。

### 打包

整个系统以以下结构发布：

```
research-system/
  AGENTS.md                     # 项目约定
  skills/
    run-research/
      SKILL.md                  # 顶层工作流
  servers/
    research-mcp/               # MCP 服务器
      pyproject.toml
      src/
  agents/
    writer/                     # A2A Agent
  gateway/
    config.yaml                 # RBAC + 锁定清单
```

用户用 `docker compose up` 部署。Claude Code、Cursor、Codex 和 opencode 用户可以通过调用 `run-research` 技能驱动系统。

### 每个 Phase 13 课程的贡献

| 课程 | 毕业项目使用 |
|------|-------------|
| 01-05 | 工具接口、供应商可移植性、并行调用、Schema、lint |
| 06-10 | MCP 原语、服务器、客户端、传输层、资源 + 提示 |
| 11-14 | Sampling、roots + elicitation、异步任务、`ui://` 应用 |
| 15-17 | 工具投毒、OAuth 2.1、网关 + 注册中心 |
| 18 | A2A 子 Agent 委托 |
| 19 | OTel GenAI 追踪 |
| 20 | LLM 层的路由网关 |
| 21 | SKILL.md + AGENTS.md 打包 |

## 用框架实现

`code/main.py` 将前课模式缝合为一个可运行的端到端演示。全部标准库，全部进程内运行便于从头到尾阅读。它运行研究和报告场景的完整流程：与网关握手、模拟 OAuth 2.1、合并 tools/list、generate_report 作为任务、A2A 调用写作 Agent、ui:// 资源返回、OTel span 发射。

关注点：

- 一个 trace id 贯穿每跳。
- 网关策略阻止第二个用户写入。
- 任务生命周期 working -> completed 返回文本和 ui:// 内容。
- A2A 调用内部状态对编排者不透明。
- AGENTS.md 和 SKILL.md 是其他 Agent 复现工作流所需的唯一文件。

## 产出物

本课产生 `outputs/skill-ecosystem-blueprint.md`。给定产品需求（研究、摘要、自动化），该技能生成完整架构：哪些 MCP 原语、哪些网关控制、哪些 A2A 调用、哪些遥测、哪些打包。

## 练习题

1. 运行 `code/main.py`。注意单一 trace id 和 span 如何嵌套。计算演示触及 Phase 13 的多少个原语。

2. 扩展演示：添加第二个后端 MCP 服务器（如 `bibliography`）并确认网关将其工具合并到同一命名空间。

3. 用在子进程上运行的真实 A2A 写作 Agent 替换假的。使用第 19 课的线束。

4. 在编排器和 LLM 之间的路由网关中添加 PII 脱敏步骤。确认用户查询中的电子邮件被擦除。

5. 为将要维护此系统的队友编写 AGENTS.md。它应该在 5 分钟内读完并提供他们需要在 Cursor 或 Codex 中驱动毕业项目的一切。

## 术语速查表

| 术语 | 人们怎么说 | 实际含义 | 英文 |
|------|-----------|---------|------|
| 毕业项目 | "Phase 13 集成演示" | 使用每个原语的端到端系统 | Capstone |
| 研究与报告 | "那个场景" | 搜索-摘要-渲染模式 | Research and report |
| 生态系统 | "所有组件的整合" | 服务器 + 客户端 + 网关 + 子 Agent + 遥测 + 包 | Ecosystem |
| 追踪层次 | "单一 trace id" | 每跳的 span 共享 trace；父子通过 span id | Trace hierarchy |
| 网关签发 token | "传递式认证" | 客户端只看到网关的 token；网关持有上游凭证 | Gateway-issued token |
| 合并命名空间 | "所有工具在一个扁平列表" | 网关的多服务器合并，冲突时前缀 | Merged namespace |
| 不透明边界 | "A2A 调用隐藏内部" | 子 Agent 的推理对编排者不可见 | Opacity boundary |
| 三层堆栈 | "AGENTS.md + SKILL.md + MCP" | 项目上下文 + 工作流 + 工具 | Three-layer stack |
| 纵深防御 | "多层安全" | 锁定哈希、OAuth、RBAC、Rule of Two、审计日志 | Defense-in-depth |
| 规范合规矩阵 | "我们发布的规范要求什么" | 交付物映射到 2025-11-25 要求的检查清单 | Spec compliance matrix |

## 延伸阅读

- [MCP — Specification 2025-11-25](https://modelcontextprotocol.io/specification/2025-11-25) — 合并参考
- [MCP blog — 2026 roadmap](https://blog.modelcontextprotocol.io/posts/2026-mcp-roadmap/) — 协议走向哪里
- [a2a-protocol.org](https://a2a-protocol.org/latest/) — A2A v1.0 参考
- [OpenTelemetry — GenAI semconv](https://opentelemetry.io/docs/specs/semconv/gen-ai/) — 权威追踪约定
- [Anthropic — Claude Agent SDK overview](https://code.claude.com/docs/en/agent-sdk/overview) — 生产 Agent 运行时模式
