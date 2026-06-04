# 人在环路：先提议后提交

> 2026 年关于 HITL 的共识是具体的。它不是"Agent 询问，用户点击批准"。它是先提议后提交 (propose-then-commit)：提议的操作持久化到带有幂等键 (idempotency key) 的持久存储中；呈现给审查者时附带意图、数据血缘、触及的权限、爆炸半径和回滚计划；仅在正面确认后提交；执行后验证以确认副作用实际发生。LangGraph 的 `interrupt()` 加 PostgreSQL 检查点、Microsoft Agent Framework 的 `RequestInfoEvent` 和 Cloudflare 的 `waitForApproval()` 都实现了相同的形状。典型的失败模式是橡皮图章审批："批准？"在未审查的情况下被点击。已记录的缓解措施是带显式清单的挑战-响应。

**类型：** 学习
**语言：** Python（标准库，带幂等性的先提议后提交状态机）
**前置条件：** Phase 15 · 12（持久执行），Phase 15 · 14（绊线）
**时间：** ~60 分钟

## 问题引入

> **【中文解读】** 先提议后提交（Propose-Then-Commit）模式要求 Agent 先生成修改方案但不立即执行，而是展示给用户或其他 Agent 审查，审查通过后才提交。这是 Agent 安全的关键模式——将'思考'和'执行'分离，给人类或系统一个在执行前检查和纠正的机会。

> **【拓展：propose then commit】** 先提议后提交模式是 2026 年编码 Agent 的标准安全实践。Claude Code 默认使用这一模式——生成修改建议并等待用户确认。Git 的 PR/MR 机制也是这一模式的应用——代码修改先提出，经过审查后才合并。在 Agent 上下文中，这一模式特别重要，因为 Agent 的错误可能比人类错误更具破坏性。

Agent 采取一个行动。用户必须决定：批准还是不批准。如果决定是即时的，它可能不是审查。如果决定是结构化的，它很慢但可信。工程问题是如何使结构化审查成为阻力最小的路径。

2023 年代的 HITL 模式是同步提示："Agent 想要发送邮件给 X，内容为 Y — 批准？"用户点击批准。每个人都觉得系统是安全的。实际上这个界面被大量橡皮图章化：用户快速批准，批准预测不了什么，当 Agent 出错时，审计追踪显示一长串用户无法回忆的批准。

> **【中文解读】** 本节介绍了 AI Agent 的核心概念和实现方法。Agent 是 LLM 驱动的自主系统，能够观察环境、思考决策、执行行动并循环迭代直到完成目标。

2026 年的模式——先提议后提交——将 HITL 移到持久基底上，附加结构化元数据，并要求正面提交。每个托管 Agent SDK 都发布一个版本：LangGraph `interrupt()`、Microsoft Agent Framework `RequestInfoEvent`、Cloudflare `waitForApproval()`。API 名称不同；形状不不同。

## 核心概念

### 先提议后提交状态机

1. **提议。** Agent 产生一个提议的操作。持久化到持久存储（PostgreSQL、Redis、Durable Object）。包括：
   - 意图（Agent 为什么这样做）
   - 数据血缘（什么来源导致了这个提议）
   - 触及的权限（哪些范围/文件/端点）
   - 爆炸半径（最坏情况是什么）
   - 回滚计划（如果提交了，我们如何撤销）
   - 幂等键（每个提议唯一；重新提交返回相同记录）
2. **呈现。** 审查者看到带有所有元数据的提议。审查者是人（不是 Agent 审查自己）。
3. **提交。** 正面确认。操作执行。
4. **验证。** 执行后，副作用被回读并确认。如果验证步骤失败，系统处于已知不良状态并启动告警。

### 幂等键

没有幂等键，瞬态故障后的重试可能双重执行一个已批准的操作。具体例子：用户批准"从 A 转账 100 美元到 B"。网络闪断。工作流重试。用户已批准一次但转账执行了两次。幂等键将批准与唯一的单一副作用绑定；第二次执行是空操作。

这与 Stripe 和 AWS API 使用的幂等模式相同。Microsoft Agent Framework 文档中明确将其复用于 Agent 批准。

### 持久性：为什么批准比进程存活更久

批准等候室是 Agent 不拥有的一块状态。工作流已暂停（第 12 课）。当批准到达时，工作流从该点精确恢复。这就是为什么 LangGraph 将 `interrupt()` 与 PostgreSQL 检查点配对而不仅仅是内存中状态——两天后的批准仍然能找到完整的工作流。

### 橡皮图章批准和挑战-响应缓解

HITL 的默认 UI（"批准"/"拒绝"按钮）产生没有真正审查的快速批准。已记录的缓解措施：一个挑战-响应清单，在批准按钮启用前要求对特定问题的正面回答。具体形态：

- "你了解这触及什么资源吗？[ ]"
- "你已验证爆炸半径是可接受的吗？[ ]"
- "你有失败时的回滚计划吗？[ ]"

不是为了官僚主义——而是一个强制函数。无法勾选复选框的审查者要么请求澄清（升级），要么拒绝（安全默认值）。Anthropic 的 Agent 安全研究明确引用了清单驱动的 HITL 作为橡皮图章审批模式的缓解措施。

### 什么算作有后果

不是每个操作都需要先提议后提交。2026 年的指导：

- **有后果的操作**（始终 HITL）：不可逆写入、金融交易、对外通信、生产数据库更改、破坏性文件系统操作。
- **可逆的操作**（有时 HITL）：本地文件编辑、暂存环境更改、有清晰回滚的可逆写入。
- **读取和检查**（从不 HITL）：读取文件、列出资源、调用只读 API。

### 操作后验证

"提交已运行"不等于"副作用已发生"。网络分区和竞态条件可能产生一个认为已成功的工作流，而后端没有持久化。验证步骤在提交后重新读取目标资源以确认。这与带 `RETURNING` 子句的数据库事务或 `PutObject` 后的 AWS `GetObject` 是相同的模式。

### EU AI 法案第 14 条

第 14 条要求对欧盟的高风险 AI 系统实施有效的人类监督。"有效"不是装饰性的。监管语言明确排除橡皮图章模式。先提议后提交加挑战-响应是在 Microsoft Agent 治理工具包合规文档中经受第 14 条审查的形状。

## 用框架实现

`code/main.py` 用标准库 Python 实现一个先提议后提交状态机。持久存储是一个 JSON 文件。幂等键是（thread_id, action_signature）的哈希。驱动器模拟三种情况：一个干净的批准流程、瞬态故障后的重试（不得双重执行）和橡皮图章默认值对比挑战-响应流程。

## 产出物

`outputs/skill-hitl-design.md` 审查一个提议的 HITL 工作流的先提议后提交形状，并标记缺失的元数据、幂等性、验证或挑战-响应层。

## 练习题

1. 运行 `code/main.py`。确认已批准提议的重试使用持久记录且不重新执行。现在将幂等键改为包含时间戳并展示重试双重执行。
   *思考并实践此练习*

2. 用 `rollback` 字段扩展提议记录。模拟一个验证步骤失败的执行。展示回滚自动触发。
   *思考并实践此练习*

3. 阅读 Microsoft Agent Framework 的 `RequestInfoEvent` 文档。识别 API 包含的一个玩具引擎缺少的元数据字段。添加它并解释它防护什么。
   *思考并实践此练习*

4. 为特定操作（例如，"发布到公共 Twitter 账号"）设计一个挑战-响应清单。审查者必须回答哪三个问题？为什么是那三个？
   *思考并实践此练习*

5. 选择一个同步"批准？"提示就足够的案例（不需要持久存储）。解释原因，并命名你接受的风险类别。
   *思考并实践此练习*

## 术语速查表

| 术语 | 人们常说的 | 实际含义 |
|---|---|---|
| 先提议后提交 (Propose-then-commit) | "两阶段批准" | 持久化提议 + 正面提交 + 验证 |
| 幂等键 (Idempotency Key) | "重试安全令牌" | 每个提议唯一；第二次执行为空操作 |
| 数据血缘 (Data Lineage) | "来源是什么" | 导致提议的特定来源内容 |
| 爆炸半径 (Blast Radius) | "最坏情况" | 操作出错时的影响范围 |
| 橡皮图章 (Rubber-stamp) | "快速批准" | 没有真正审查就点击"批准" |
| 挑战-响应 (Challenge-and-response) | "强制清单" | 审查者必须正面确认特定问题 |
| RequestInfoEvent | "MS Agent Framework 原语" | 带有结构化元数据的持久 HITL 请求 |
| `interrupt()` / `waitForApproval()` | "框架原语" | LangGraph / Cloudflare 的相同形状的等效物 |

## 延伸阅读

- [Microsoft Agent Framework — 人在环路](https://learn.microsoft.com/en-us/agent-framework/workflows/human-in-the-loop) — `RequestInfoEvent`，持久批准。
- [Cloudflare Agents — 人在环路](https://developers.cloudflare.com/agents/concepts/human-in-the-loop/) — `waitForApproval()` 和 Durable Objects。
- [Anthropic — 实践中测量 Agent 自主性](https://www.anthropic.com/research/measuring-agent-autonomy) — HITL 作为长程风险的缓解措施。
- [EU AI 法案 — 第 14 条：人类监督](https://artificialintelligenceact.eu/article/14/) — 高风险系统的监管基线。
- [Anthropic — Claude 的宪法（2026 年 1 月）](https://www.anthropic.com/news/claudes-constitution) — 围绕监督的宪法框架化。
