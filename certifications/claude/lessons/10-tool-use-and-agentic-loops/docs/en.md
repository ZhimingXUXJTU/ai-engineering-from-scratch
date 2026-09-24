# A Tool Loop Is Controlled Delegation | 工具循环是受控的委托

> Claude may propose an action. Your application validates the request, grants the capability, observes the result, and decides whether the loop continues.

> **【中文解读】** 本课把工具调用（tool use）与 Agent 循环（agentic loop）的核心定性为一句话：工具给 Claude 触达世界的能力，不给它执行世界的权力。模型提议（propose）一个具名能力并附结构化参数；确定性应用代码决定是否执行、如何执行、至多执行几次。课程覆盖完整的 `tool_use`/`tool_result` 协议回路、工具契约设计、校验之后才授权的执行边界、并行调用约束、终止条件预算，以及"手写循环 / SDK Tool Runner / 托管 Agent"三种拥有量的选择框架。考试高频点：提议与授权的分离、失败按类别恢复、终局判据看状态不看 prose。

> 🔗 **【前置】** 学本课前请先掌握：(1) 08 课《Messages API 是一台状态机》——stop reason 与内容块是循环的驱动信号；(2) 09 课《结构化输出是不受信任的契约》——工具输入 schema 同样是"帮模型构造调用"的契约，handler 仍须自行校验授权。

**Type:** Build | **类型:** 动手构建
**Languages:** Python | **语言:** Python
**Prerequisites:** [The Messages API Is a State Machine](../../08-messages-api-and-application-lifecycle/), [Structured Output Is an Untrusted Contract](../../09-structured-output-and-defensive-parsing/) | **前置知识:** 08 Messages API 是一台状态机；09 结构化输出是不受信任的契约
**Time:** ~130 minutes | **时间:** 约 130 分钟

## Learning Objectives | 学习目标

- Implement the complete `tool_use` and `tool_result` protocol loop
  中文翻译：实现完整的 `tool_use` 与 `tool_result` 协议回路。
- Design focused tool contracts and choose their execution boundary
  中文翻译：设计聚焦的工具契约并选择它们的执行边界。
- Separate model selection of a tool from deterministic authorization
  中文翻译：把模型的工具选择与确定性授权分开。
- Compare a hand-written loop, SDK Tool Runner, and managed agents
  中文翻译：比较手写循环、SDK Tool Runner 与托管 Agent。
- Return failures as typed results and consume actionable runtime events
  中文翻译：把失败作为类型化结果返回，并消费可行动的运行时事件。
- Bound autonomy and choose a fixed workflow when the path is known
  中文翻译：给自主性设边界；当路径已知时选择固定工作流。

## The Agent That Repeats a Payment | 重复付款的 Agent

> **【中文解读】** 开场事故把"语言生成"与"事务控制"混为一谈的代价具象化：连接在最终文本到达前断开，应用重试整轮，Claude 再次请求 `issue_refund`，客户收到两笔退款。问题不在模型用了工具，而在应用把"模型说了"当成"事务提交了"。由此立下本课的两契约框架：模型可以提议带结构化参数的具名能力；是否、如何、至多几次执行，由确定性代码决定。这也预告了幂等键与对账在练习中的位置。

A billing assistant receives "Refund the duplicate charge." Claude requests `issue_refund`. The application executes it. The response connection drops before the final text arrives. The application retries the entire turn, Claude requests the tool again, and the customer receives two refunds.

> 一个账单助手收到"给重复扣款退款"。Claude 请求 `issue_refund`。应用执行了它。响应连接在最终文本到达之前断开。应用重试了整轮，Claude 再次请求该工具，客户收到了两笔退款。

The problem is not that the model used a tool. The application confused language generation with transaction control.

> 问题不在模型使用了工具。是应用把语言生成当成了事务控制。

A reliable tool loop has two contracts:

1. The model can propose a named capability with structured arguments.
  中文翻译：模型可以用结构化参数提议一个具名能力。
2. Deterministic application code decides whether, how, and at most how many times that capability executes.
  中文翻译：确定性应用代码决定该能力是否执行、如何执行、以及至多执行多少次。

Tool use gives Claude reach. It does not give Claude authority.

> 工具调用给 Claude 触达能力。它不给 Claude 权力。

## The Wire Contract Before the Framework | 先看线格式契约，再谈框架

> **【中文解读】** 在碰任何 SDK 之前先看裸协议：客户端在请求里声明工具（名字、描述、JSON Schema 输入契约）；模型返回 `stop_reason: "tool_use"` 和带 id 的 `tool_use` 内容块；你的客户端原样保留整段 assistant 内容、校验并执行工具，再以 user 角色追加 `tool_result` 并回指同一 id。配对 id 不是装饰——它把结果与唯一一次请求关联；协议还要求 assistant 消息在历史中紧邻结果序列。

Client tools are declared in the request. Each declaration gives the model a name, a description, and a JSON Schema input contract.

> 客户端工具在请求中声明。每个声明给模型一个名字、一段描述和一份 JSON Schema 输入契约。

```json
{
  "name": "lookup_order",
  "description": "Look up one order by its exact public order ID. Returns status and last update. This tool never changes an order.",
  "input_schema": {
    "type": "object",
    "required": ["order_id"],
    "additionalProperties": false,
    "properties": {
      "order_id": {
        "type": "string",
        "description": "Order ID in the form A-12345"
      }
    }
  }
}
```

Claude may return:

```json
{
  "stop_reason": "tool_use",
  "content": [
    {
      "type": "tool_use",
      "id": "toolu_7f3",
      "name": "lookup_order",
      "input": {"order_id": "A-12345"}
    }
  ]
}
```

Your client preserves that entire assistant content, validates and runs the tool, then appends:

> 你的客户端原样保留整段 assistant 内容，校验并运行该工具，然后追加：

```json
{
  "role": "user",
  "content": [
    {
      "type": "tool_result",
      "tool_use_id": "toolu_7f3",
      "content": "{\"found\":true,\"status\":\"in_transit\"}"
    }
  ]
}
```

The matching ID is not decoration. It correlates a result with one request. The assistant message must remain immediately before the result sequence in the conversation history expected by the protocol.

> 配对的 ID 不是装饰。它把一个结果与一次请求关联。assistant 消息在协议期望的会话历史中必须保持在结果序列之前紧邻的位置。

See [Implement client tools](https://platform.claude.com/docs/en/agents-and-tools/tool-use/implement-tool-use) for the current SDK and API shapes.

> 当前 SDK 与 API 形状参见 [Implement client tools](https://platform.claude.com/docs/en/agents-and-tools/tool-use/implement-tool-use)。

## The Loop Has Explicit States | 循环有显式状态

> **【中文解读】** 状态机图把循环拆成可命名、可测试的转移：检查 stop reason → 校验调用 → 授权 → 执行 → 追加结果 → 检查预算 → 回到提问模型或升级。每一步都可能失败：缺工具 id、未知工具名、参数违反 schema、授权拒绝、handler 超时、结果过大、模型继续要工具、最终答案不过输出契约。考试要点：不要用一个宽泛的 `try/except` 加通用重试把这些状态藏起来——按失败类别分类，按类别选恢复策略。

```mermaid
stateDiagram-v2
    [*] --> AskModel
    AskModel --> InspectStopReason
    InspectStopReason --> ValidateFinal: end_turn
    InspectStopReason --> ValidateCalls: tool_use
    InspectStopReason --> RecoverOrStop: other reason
    ValidateCalls --> AuthorizeCalls
    AuthorizeCalls --> ExecuteCalls: allowed
    AuthorizeCalls --> ReturnDenial: denied
    ExecuteCalls --> ReturnResults
    ReturnDenial --> AppendResults
    ReturnResults --> AppendResults
    AppendResults --> CheckBudgets
    CheckBudgets --> AskModel: budget remains
    CheckBudgets --> Escalate: budget exhausted
    ValidateFinal --> [*]
    Escalate --> [*]
```

Every transition can fail. The response may omit a tool ID. The tool name may be unknown. Arguments may violate the schema. Authorization may deny the call. The handler may time out. A result may be too large. Claude may request another tool. The final answer may still fail its output contract.

> 每个转移都可能失败。响应可能缺少工具 ID。工具名可能未知。参数可能违反 schema。授权可能拒绝调用。handler 可能超时。结果可能过大。Claude 可能再请求一个工具。最终答案仍可能不满足它的输出契约。

Do not hide these states behind one broad `try/except` and a generic retry. Classify them and choose recovery by failure class.

> 不要把这些状态藏在一个宽泛的 `try/except` 和通用重试后面。给它们分类，按失败类别选择恢复策略。

## Tool Design Is Interface Design | 工具设计就是接口设计

Claude chooses tools from their interfaces. A human should be able to infer when to use each tool without reading its handler.

> Claude 依据接口选择工具。一个人应该能不看 handler 就推断出每个工具何时使用。

### Give Each Tool One Job | 一个工具只做一件事

`manage_customer` is vague. It might search, edit, refund, suspend, or delete. A narrow catalog is easier to select and easier to secure:

> `manage_customer` 是模糊的。它可能搜索、编辑、退款、冻结或删除。窄目录更容易被选中，也更容易被加固：

- `get_customer_profile`
  中文翻译：获取客户档案。
- `list_customer_invoices`
  中文翻译：列出客户发票。
- `propose_refund`
  中文翻译：提议退款。
- `issue_approved_refund`
  中文翻译：执行已批准的退款。

The separation between proposal and execution matters. A low-risk tool can calculate a proposed amount. A high-risk tool requires an authenticated approval token generated outside the model.

> 提议与执行的分离很重要。低风险工具可以计算提议金额。高风险工具需要一个在模型之外生成的、经过认证的批准令牌。

### Write Selection Descriptions, Not Internal Documentation | 写供选择的描述，不是内部文档

A useful description says what the tool does, when to use it, when not to use it, and what the result means. It does not paste an entire API manual.

> 一段有用的描述说明这个工具做什么、何时用、何时不用、结果意味着什么。它不粘贴整本 API 手册。

Bad:

```text
Calls GET /v3/orders/{id} in the Commerce service.
```

Better:

```text
Read the current status of one existing order from the commerce system.
Use only when the user supplies an exact order ID. This tool is read-only.
Do not use it to search by email or to modify shipment details.
```

Examples inside descriptions can clarify tricky formats, but every token repeats with the tool catalog. Measure whether an example improves selection enough to earn its context cost.

> 描述里的示例能澄清棘手的格式，但每个 token 都会随工具目录重复出现。衡量一个示例对选择准确率的提升是否值回它的上下文成本。

### Make Invalid Calls Hard to Express | 让非法调用难以表达

Use enums, required fields, bounds, and `additionalProperties: false`. Split mutually exclusive modes. Avoid free-form shell commands, SQL, URLs, and filesystem paths when a narrow domain value will work.

> 使用枚举、必填字段、边界和 `additionalProperties: false`。拆分互斥的模式。当一个窄域值就能工作时，避免自由形式的 shell 命令、SQL、URL 和文件系统路径。

The schema guides generation. The handler still validates it. Never assume model-produced input is safe because it was generated from a schema.

> schema 引导生成。handler 仍然要校验它。绝不要因为输入是从 schema 生成就假定模型产出是安全的。

## Keep the Tool Catalog Small and Distinct | 保持工具目录小而互异

More tools do not always create more capability. Overlapping names and long catalogs create selection ambiguity and consume context.

> 更多工具不总是带来更多能力。重叠的名字和过长的目录制造选择歧义并消耗上下文。

Start with the fewest tools required by realistic tasks. Add a tool when an eval shows a capability gap. Remove or consolidate a tool when trajectories show confusion.

> 从现实任务所需的最少工具起步。当评估显示能力缺口时才加工具。当轨迹显示混淆时删除或合并工具。

Use these questions:

> 用这些问题自检：

- Do two tools appear interchangeable from their names and descriptions?
  中文翻译：两个工具从名字和描述看是否可以互换？
- Can a general code or CLI tool already perform this task under a sandbox?
  中文翻译：一个通用代码或 CLI 工具是否已在沙箱下就能完成这个任务？
- Does the agent need this capability on every turn?
  中文翻译：Agent 是否每一轮都需要这个能力？
- Can the capability live in a Skill and be loaded only when relevant?
  中文翻译：这个能力能否放进 Skill，只在相关时才加载？
- Should a separate subagent receive this tool instead of the main agent?
  中文翻译：这个工具是否应该交给一个独立的子 Agent 而不是主 Agent？
- Would a standardized MCP server let several hosts share it safely?
  中文翻译：一个标准化的 MCP 服务器是否能让多个宿主安全共享它？

Tool count is not an architecture score. Correct selection and controlled execution are.

> 工具数量不是架构得分。正确的选择和受控的执行才是。

## Authorization Happens After Validation | 授权发生在校验之后

> **【中文解读】** 安全执行边界的八步顺序是本课的骨架：解析工具名对允许清单 → 校验输入类型与边界 → 从应用（而非参数）绑定认证身份与租户上下文 → 检查能力范围与资源所有权 → 后果性动作要求批准 → 应用幂等、超时、速率和大小限制 → 在最窄沙箱中执行 → 返回前脱敏。两条红线：工具参数里的 `user_id` 不是身份；会话文本里的"用户之前同意过"不是安全批准令牌——批准记录必须绑定用户、动作、规范化参数、过期时间和操作 ID。

A safe execution boundary follows this order:

1. Resolve the tool name against an allowlist.
  中文翻译：对照允许清单解析工具名。
2. Validate input types and bounds.
  中文翻译：校验输入类型和边界。
3. Bind authenticated identity and tenant context from the application, not arguments.
  中文翻译：从应用而非参数绑定认证身份与租户上下文。
4. Check capability scope and resource ownership.
  中文翻译：检查能力范围和资源所有权。
5. Require approval for consequential actions.
  中文翻译：后果性动作要求批准。
6. Apply idempotency, timeout, rate, and size limits.
  中文翻译：应用幂等、超时、速率和大小限制。
7. Execute in the narrowest sandbox available.
  中文翻译：在可用的最窄沙箱中执行。
8. Redact the result before returning it to Claude or logs.
  中文翻译：把结果返回给 Claude 或日志之前先脱敏。

If a tool argument contains `user_id`, do not trust it as identity. Compare it with the authenticated session or remove it from model control entirely.

> 如果工具参数里有 `user_id`，不要把它当身份信任。与已认证会话比对，或把它完全移出模型控制。

For mutation, an approval record should bind the user, action, normalized arguments, expiry, and operation ID. "The user said yes earlier" inside conversation text is not a secure approval token.

> 对于变更操作，批准记录应绑定用户、动作、规范化参数、过期时间和操作 ID。会话文本里的"用户之前说过同意"不是安全的批准令牌。

## Return Failures as Results | 把失败作为结果返回

A handler failure is not automatically an application crash. Claude may recover if it receives a concise, truthful tool result.

> handler 失败不自动等于应用崩溃。如果 Claude 收到一个简洁、诚实的工具结果，它可能自行恢复。

```json
{
  "type": "tool_result",
  "tool_use_id": "toolu_7f3",
  "is_error": true,
  "content": "Order service timed out. No order state was changed. Retry is allowed once."
}
```

Good error content tells the model:

> 好的错误内容告诉模型：

- What failed.
  中文翻译：什么失败了。
- Whether any side effect occurred.
  中文翻译：是否发生了副作用。
- Whether retry is safe.
  中文翻译：重试是否安全。
- Which correction is possible.
  中文翻译：可以做哪种修正。

Do not expose stack traces, environment values, database queries, access tokens, or internal hostnames. Preserve those in protected telemetry with redaction and access control.

> 不要暴露堆栈跟踪、环境变量值、数据库查询、访问令牌或内部主机名。把它们保存在带脱敏和访问控制的受保护遥测里。

Validation failures can include field paths. Policy denials should not invite the model to find a bypass. A denial such as "This agent cannot issue refunds" is safer than enumerating every security rule.

> 校验失败可以包含字段路径。策略拒绝不应引导模型去找绕行方案。"这个 Agent 不能发起退款"这样的拒绝，比枚举每条安全规则更安全。

Unknown tools should become a correlated error result or a terminal protocol error according to your design. Never dynamically import and run a handler named by the model.

> 按你的设计，未知工具应变成一个关联的错误结果或一个终局协议错误。绝不动态导入并运行一个由模型命名的 handler。

## Multiple and Parallel Tool Calls | 多工具调用与并行调用

Claude can request more than one tool in a response. Execute them in parallel only when they are independent, read-only, and safe to reorder.

> Claude 可以在一个响应里请求多个工具。只有当它们相互独立、只读、且重排安全时才并行执行。

Two searches can often run concurrently. "Create invoice" followed by "send invoice" has a dependency and must remain sequential. Two writes to the same record may conflict. A payment and an email may require a transaction or compensating workflow.

> 两个搜索通常可以并发。"创建发票"接"发送发票"存在依赖，必须保持顺序。对同一条记录的两次写入可能冲突。一次付款和一封邮件可能需要事务或补偿工作流。

Return one `tool_result` for every requested `tool_use` ID. Preserve enough ordering to reconstruct the trajectory. If one parallel call fails, report each outcome rather than pretending the batch was uniformly successful.

> 为每个被请求的 `tool_use` ID 返回一个 `tool_result`。保留足够的顺序信息以重建轨迹。如果一个并行调用失败，逐个报告结果，而不是假装整批一致成功。

Product note, verified 2026-08-08: helper APIs for automatic tool execution and parallel calls vary by SDK. They do not remove application authorization responsibilities. Check the current [Tool use overview](https://platform.claude.com/docs/en/agents-and-tools/tool-use/overview).

> 产品说明（2026-08-08 核实）：自动工具执行与并行调用的辅助 API 因 SDK 而异。它们不免除应用的授权职责。查阅当前的 [Tool use overview](https://platform.claude.com/docs/en/agents-and-tools/tool-use/overview)。

## Bound the Agent | 给 Agent 设边界

> **【中文解读】** Agent 循环需要 `end_turn` 之外的终止条件清单：最大轮数、全局与单工具调用上限、墙上时钟截止、token 与金钱预算、最大连续错误、最大相同重复调用、用户取消、必需的人工批准、已验证的终局谓词。终局谓词比"回答听起来完整"强得多——部署 Agent 的成功标准是预期版本健康，不是它说"部署完了"。轨迹要记录提示词版本、模型、stop reason、工具名、规范化参数指纹、决策、延迟、结果类别和状态变更，敏感值脱敏。

An agent loop needs terminal conditions beyond `end_turn`:

> Agent 循环需要 `end_turn` 之外的终止条件：

- Maximum model turns.
  中文翻译：最大模型轮数。
- Maximum tool calls, globally and per tool.
  中文翻译：最大工具调用数（全局与单工具）。
- Wall-clock deadline.
  中文翻译：墙上时钟截止时间。
- Token and monetary budget.
  中文翻译：token 与金钱预算。
- Maximum consecutive errors.
  中文翻译：最大连续错误数。
- Maximum repeated identical call.
  中文翻译：最大相同重复调用数。
- User cancellation.
  中文翻译：用户取消。
- Required human approval.
  中文翻译：必需的人工批准。
- Verified final-state predicate.
  中文翻译：已验证的终局谓词。

The final-state predicate is stronger than asking whether the response sounds complete. A deployment agent succeeds when the expected version is healthy, not when it says "deployed." A research agent succeeds when required claims have resolvable sources, not when it produces a long report.

> 终局谓词比"响应听起来是否完整"更强。部署 Agent 的成功标准是预期版本健康，而不是它说"已部署"。研究 Agent 的成功标准是必需论断有可解析的来源，而不是它产出一份长报告。

Record the trajectory: prompt version, model, stop reason, tool name, normalized argument fingerprint, decision, latency, result class, and state change. Redact sensitive values.

> 记录轨迹：提示词版本、模型、stop reason、工具名、规范化参数指纹、决策、延迟、结果类别和状态变更。敏感值脱敏。

## Workflow or Agent | 工作流还是 Agent

Use a fixed workflow when the steps and branches are known. Use an agent when the path depends on observations and the model must choose among tools.

> 步骤和分支已知时用固定工作流。路径取决于观察、且模型必须在工具间做选择时才用 Agent。

| Task | Better default | Reason |
|---|---|---|
| Extract fields, validate, store | Workflow | Known sequence and clear contract |
| Classify then route to one queue | Workflow | Finite branch set |
| Investigate an unfamiliar repository defect | Agent | Search path depends on findings |
| Refund after a verified duplicate charge | Workflow with approval | Consequential action and known controls |
| Gather evidence across changing internal systems | Bounded agent | Tool choice depends on missing evidence |

Autonomy is justified when the task is valuable, the environment is tool-accessible, mistakes are detectable, and recovery is possible. If errors cannot be detected, adding more agent turns only hides risk.

> 当任务有价值、环境可被工具触达、错误可检测、恢复有可能时，自主性才站得住。如果错误无法被检测，增加更多 Agent 轮次只是在隐藏风险。

## Choose How Much Loop to Own | 选择拥有多少循环

> **【中文解读】** 这是全课的架构决策核心：过了"工作流还是 Agent"的门之后，再选满足运维要求的最小执行框架。手写 Messages 循环只替你做你实现的协议工作，其余全归你；SDK Tool Runner 接管工具声明、`tool_use`/`tool_result` 序列和消息状态更新，但授权、沙箱、幂等、错误披露、迭代上限、可观测性和终局证明仍是你的；Claude Managed Agents 提供远程 Agent/会话/环境框架与内置沙箱，但你仍要管配置、数据边界批准、自定义工具执行、确认决策、事件持久化、业务授权和结果核实。换框架永远换不掉安全责任。

After the workflow gate, choose the smallest harness that meets the operational requirement.

> 过了工作流这道门之后，选择满足运维要求的最小执行框架。

| Runtime | What it handles | What your application still handles | Prefer it when |
|---|---|---|---|
| Hand-written Messages loop | Only the protocol work you implement | Full history, stop reasons, schema and policy, execution, retries, budgets, traces, and recovery | You need wire-level control, a constrained runtime, a custom state machine, or protocol education and testing |
| SDK Tool Runner | Tool declaration helpers, `tool_use` and `tool_result` sequencing, message-state updates, and optional per-turn streaming | Authorization, sandbox, idempotency, error disclosure, iteration limit, observability, and final-state proof | A supported SDK fits and client tools still run under your application's control |
| Claude Managed Agents | A remote agent/session/environment harness with configured sandbox, built-in tools, and event-driven execution | Agent configuration, data-boundary approval, custom-tool execution, confirmation decisions, event persistence, business authorization, and outcome verification | You need the managed session and sandbox boundary and accept its current beta, platform, and event contracts |

The code in this lesson is deliberately the first option. It exposes every transition. Moving it to the [Tool Runner](https://platform.claude.com/docs/en/agents-and-tools/tool-use/tool-runner) removes repetitive loop plumbing, but it does not make a refund safe. Set an iteration bound, intercept or wrap tool execution, preserve application approval, and validate the final state.

> 本课代码刻意选择第一种。它暴露每一个转移。把它迁移到 [Tool Runner](https://platform.claude.com/docs/en/agents-and-tools/tool-use/tool-runner) 能省去重复的循环管道，但不会让一笔退款变安全。设置迭代上限、拦截或包装工具执行、保留应用批准、验证最终状态。

Product note, verified 2026-08-09: [Claude Managed Agents](https://platform.claude.com/docs/en/managed-agents/overview) is currently public beta and uses a versioned beta contract. It provides managed agents, environments, sessions, built-in tools, and server-sent event streaming. Treat the header, resources, event types, toolset, limits, and provider availability as volatile. Do not select it merely because the task is called an agent.

> 产品说明（2026-08-09 核实）：[Claude Managed Agents](https://platform.claude.com/docs/en/managed-agents/overview) 目前是公开测试版，使用带版本的测试契约。它提供托管 Agent、环境、会话、内置工具和服务器发送事件流。把请求头、资源、事件类型、工具集、限制和可用供应商都当作易变项对待。不要仅仅因为任务被叫作"Agent"就选它。

A managed-agent integration is an event consumer, not a final-text call. The application sends user events, consumes persisted session and agent events, and tracks status. A custom tool call or permission-gated tool can pause the session with `requires_action`; the application resolves the referenced event IDs with results or confirmation decisions. A closed SSE connection is not success. Reconcile persisted events and terminal status. Lesson 12 implements this boundary against an offline event fixture; the current source is [Session event stream](https://platform.claude.com/docs/en/managed-agents/events-and-streaming).

> 托管 Agent 集成是一个事件消费者，不是一次"拿最终文本"的调用。应用发送用户事件、消费已持久化的会话与 Agent 事件、跟踪状态。自定义工具调用或权限门控工具可以用 `requires_action` 暂停会话；应用用结果或确认决策解析被引用的事件 ID。SSE 连接关闭不等于成功。要对账已持久化事件与终局状态。12 课会针对离线事件夹具实现这条边界；当前来源是 [Session event stream](https://platform.claude.com/docs/en/managed-agents/events-and-streaming)。

## First-Party Does Not Mean One Execution Boundary | 第一方不等于只有一条执行边界

> **【中文解读】** 按"代码和数据在哪执行、谁授权、如何被发现"给能力分类，而不是按"是不是第一方"：Messages 服务器工具由 Anthropic 执行；Anthropic-schema 客户端工具用官方训练过的 schema 但由你的应用执行；托管 Agent 内置工具在配置的 Agent 环境里执行；自定义客户端工具完全归你的应用；Skill 是按需披露的过程性内容；MCP 是跨宿主的标准化连接边界。考试要点：Skill 和工具常常互补而非二选一；任何一层 schema 合法都不等于身份、授权或幂等证据。

Classify a capability by where code and data execute, who authorizes it, and how it is discovered.

> 按"代码和数据在哪执行、谁授权它、它如何被发现"给能力分类。

| Surface | Execution and data boundary | Use it for | Do not assume |
|---|---|---|---|
| Messages server tool | Anthropic executes supported tools such as web search, web fetch, code execution, and tool search | A supported first-party capability whose provider-side execution and data policy fit | Your application receives a client `tool_use` to execute in the ordinary case |
| Anthropic-schema client tool | Anthropic defines a trained-in schema; your application executes tools such as bash, text editor, memory, or computer use | Common operations where the standard schema improves model familiarity but the client must own execution | First-party schema means provider-executed or automatically authorized |
| Managed-agent built-in | The configured managed or self-hosted agent environment executes its toolset | Repository and web work that fits that runtime's sandbox and permission policy | Enabling the toolset grants business authority or removes confirmation work |
| Custom client tool | Your application validates and executes your JSON Schema contract | Private business operations, narrow domain APIs, and exact application policy | Schema-valid input is identity, authorization, or idempotency evidence |
| Skill | A supported runtime loads reusable instructions, references, scripts, or assets | A procedure that should be disclosed only when relevant | A Skill is an execution or authorization boundary by itself |
| MCP | An MCP client or connector calls a standardized external server | Capabilities or context shared across compatible hosts with an explicit server, identity, and transport boundary | Server discovery makes every returned tool safe or relevant |

A Skill and a tool are often complementary, not alternatives. A refund-review Skill can teach the procedure while a custom client tool exposes the approved operation. MCP can carry that operation when several hosts need the same standard interface. Choose a provider-executed server tool only when its network, retention, and result semantics fit the data. Choose an Anthropic-schema client tool only when your sandbox and action validator are ready to execute it.

> Skill 和工具常常互补，而不是二选一。一个退款审查 Skill 可以教流程，同时一个自定义客户端工具暴露已批准的操作。当多个宿主需要同一标准接口时，MCP 可以承载该操作。只有当供应商执行的服务器工具的网络、留存和结果语义适合该数据时才选它；只有当你的沙箱和动作校验器准备好执行时才选 Anthropic-schema 客户端工具。

The current execution categories are documented in [How tool use works](https://platform.claude.com/docs/en/agents-and-tools/tool-use/how-tool-use-works), and the managed harness has a separate [tool configuration](https://platform.claude.com/docs/en/managed-agents/tools). Versions and model compatibility change, so persist the selected tool type and version in the trace.

> 当前的执行类别见 [How tool use works](https://platform.claude.com/docs/en/agents-and-tools/tool-use/how-tool-use-works)，托管框架另有单独的[工具配置](https://platform.claude.com/docs/en/managed-agents/tools)。版本和模型兼容性会变化，所以要把选定的工具类型和版本持久化进 trace。

## Build the Loop | 构建工具循环

`code/main.py` implements a tool registry and a raw loop. It supports multiple calls, schema checks, mutating-tool approval, handler errors, unknown tools, correlation IDs, and a turn budget. Its offline decision lab separately selects workflow, hand-written loop, SDK Tool Runner, or managed agents from explicit requirements. It also composes an execution surface with an optional Skill instead of pretending Skills are tools.

> `code/main.py` 实现了一个工具注册表和一个裸循环。它支持多调用、schema 检查、变更类工具批准、handler 错误、未知工具、关联 ID 和轮次预算。它的离线决策实验从显式需求出发，单独在工作流、手写循环、SDK Tool Runner 和托管 Agent 之间做选择；还会把可选 Skill 组合进执行面，而不是假装 Skill 是工具。

```bash
cd certifications/claude/lessons/10-tool-use-and-agentic-loops/code
python3 main.py
python3 -m unittest discover tests -v
```

Read the transcript printed by the demo. Find the assistant `tool_use` block and its following user `tool_result`. Then inspect the decision fixture printed after it. Change the managed-agent case so beta is not accepted and make the decision fail before any runtime is started. Protocol and architecture correctness should be visible, not assumed.

> 阅读演示打印的转录。找到 assistant 的 `tool_use` 块和紧随其后的 user `tool_result`。再检查其后打印的决策夹具。把托管 Agent 案例改成不接受测试版，让决策在任何运行时启动之前就失败。协议和架构正确性应该是看得见的，不是被假定的。

## Interactive Lab | 交互实验室

Use the tool-loop figure to allocate turn, tool-call, time, and approval budgets. Trigger repeated calls or a denied mutation and observe which deterministic terminal condition stops the loop.

> 用工具循环图为轮次、工具调用、时间和批准分配预算。触发重复调用或被拒绝的变更，观察哪条确定性终止条件停下了循环。

```figure
10-tool-loop-budget
```

## Practice Lab | 练习实验室

Run the tool loop, then test an unknown tool, invalid arguments, a denied mutation, multiple calls, a handler error, and an exhausted turn budget. Confirm that every result preserves its tool-use ID. Next, classify a provider server tool, Anthropic-schema client tool, private custom tool, Skill-backed procedure, and MCP service by execution boundary and authorization owner.

> 运行工具循环，然后依次测试未知工具、非法参数、被拒绝的变更、多调用、handler 错误和耗尽的轮次预算。确认每个结果都保留其 tool-use ID。接着按执行边界和授权所有者，对供应商服务器工具、Anthropic-schema 客户端工具、私有自定义工具、Skill 支撑的流程和 MCP 服务做分类。

## Shipped Artifact | 交付产物

`outputs/tool-loop-transcript.json` is a filled, correlated execution transcript from `demo()`. `outputs/runtime-and-tool-surface-decisions.json` is a dated, provider-free comparison across four runtimes and four capability compositions. Run `python3 main.py` to inspect both and execute the unit suite to verify artifacts, schema bounds, approval denial, runtime gates, execution boundaries, handler failure, and runaway prevention.

> `outputs/tool-loop-transcript.json` 是 `demo()` 产出的已填充、带关联的执行转录。`outputs/runtime-and-tool-surface-decisions.json` 是带日期、不依赖真实服务商的四种运行时与四种能力组合的对比。运行 `python3 main.py` 检查两者，并执行单元套件验证产物、schema 边界、批准拒绝、运行时门控、执行边界、handler 失败和失控防护。

## Verify It | 验证

```bash
cd certifications/claude/lessons/10-tool-use-and-agentic-loops/code
python3 main.py
python3 -m unittest discover tests -v
```

## Capstone Connection | 毕业设计衔接

The quiz tests proposal versus authorization, tool descriptions, idempotency, parallelism, final-state checks, and workflow selection. Carry the verified transcript into Developer capstone 30 and Architect capstones 31 and 32 as tool-boundary evidence.

> 测验考的是提议与授权之分、工具描述、幂等、并行性、终局检查和工作流选择。把已验证的转录带进开发者毕业设计 30 和架构师毕业设计 31、32，作为工具边界证据。

## Exam Decision Rules | 考试决策规则

- Tool selection by Claude is a proposal, never authorization.
  中文翻译：Claude 的工具选择是提案，永远不是授权。
- Validate schema before policy, and policy before execution.
  中文翻译：先校验 schema，再查策略，最后才执行。
- Use narrow names and descriptions that distinguish when tools apply.
  中文翻译：用能区分适用时机的窄名字和描述。
- Return concise, correlated errors when recovery is safe.
  中文翻译：当恢复安全时，返回简洁、带关联的错误。
- Require idempotency or reconciliation for retryable side effects.
  中文翻译：对可重试的副作用要求幂等或对账。
- Parallelize only independent calls whose ordering does not matter.
  中文翻译：只并行化顺序无关的独立调用。
- Stop on budgets, repeated calls, cancellation, or unrecognized control states.
  中文翻译：在预算耗尽、重复调用、用户取消或无法识别的控制状态时停止。
- Prefer a deterministic workflow when the path is already known.
  中文翻译：路径已知时优先用确定性工作流。
- Prefer SDK Tool Runner when client execution fits and custom wire control adds no value.
  中文翻译：客户端执行合适且自定义线控制没有价值时，优先用 SDK Tool Runner。
- Select managed agents only for a concrete managed-runtime requirement and an accepted beta and data boundary.
  中文翻译：只有存在具体的托管运行时需求且接受了测试版与数据边界时，才选托管 Agent。
- Treat a managed session as an event state machine; resolve `requires_action` by event ID and never infer success from a disconnected stream.
  中文翻译：把托管会话当作事件状态机；按事件 ID 解析 `requires_action`，绝不从断开的流推断成功。
- Distinguish server-executed tools, Anthropic-schema client tools, managed built-ins, and custom client tools by execution location.
  中文翻译：按执行位置区分服务器执行工具、Anthropic-schema 客户端工具、托管内置工具和自定义客户端工具。
- Treat Skills as procedure and MCP as a connection boundary; neither grants authorization.
  中文翻译：把 Skill 当流程、把 MCP 当连接边界；两者都不授予授权。
- Evaluate tool trajectory and final state, not only the final prose.
  中文翻译：评估工具轨迹和最终状态，而不只是最终的文字。

## Exercises | 练习

1. Add `issue_refund` with a required approval token. Prove that conversation text cannot substitute for the token.
   中文翻译：加一个带必填批准令牌的 `issue_refund`。证明会话文本代替不了令牌。
2. Add two read-only calls in one response and execute them concurrently. Preserve deterministic result correlation.
   中文翻译：在一个响应里加两个只读调用并并发执行。保留确定性的结果关联。
3. Make one tool time out after a side effect. Add an idempotency key and reconciliation check before retry.
   中文翻译：让一个工具在副作用之后超时。重试前加幂等键和对账检查。
4. Add a repeated-call detector that stops after the same normalized tool request appears twice.
   中文翻译：加一个重复调用检测器：同一规范化工具请求出现两次即停止。
5. Rework one private custom tool as an MCP capability shared by two hosts. Identify which authentication, consent, result filtering, and availability responsibilities move to the server boundary and which remain in each host.
   中文翻译：把一个私有自定义工具改造成由两个宿主共享的 MCP 能力。指出哪些认证、同意、结果过滤和可用性职责移到服务器边界，哪些留在各宿主。

## Further Reading | 延伸阅读

- [Tool use overview](https://platform.claude.com/docs/en/agents-and-tools/tool-use/overview)
  中文翻译：工具调用总览——入口文档
- [Implement client tools](https://platform.claude.com/docs/en/agents-and-tools/tool-use/implement-tool-use)
  中文翻译：实现客户端工具——线格式契约与序列要求
- [Handle tool errors](https://platform.claude.com/docs/en/agents-and-tools/tool-use/implement-tool-use#handling-tool-use-and-tool-result-content-blocks)
  中文翻译：处理工具错误——`is_error` 结果的构造
- [Tool Runner](https://platform.claude.com/docs/en/agents-and-tools/tool-use/tool-runner)
  中文翻译：Tool Runner——SDK 层的循环管道
- [How tool use works](https://platform.claude.com/docs/en/agents-and-tools/tool-use/how-tool-use-works)
  中文翻译：工具调用如何工作——执行类别划分
- [Claude Managed Agents](https://platform.claude.com/docs/en/managed-agents/overview)
  中文翻译：Claude 托管 Agent——公开测试版框架
- [Session event stream](https://platform.claude.com/docs/en/managed-agents/events-and-streaming)
  中文翻译：会话事件流——`requires_action` 与事件对账
- [Managed-agent tools](https://platform.claude.com/docs/en/managed-agents/tools)
  中文翻译：托管 Agent 工具配置
- [Building effective agents](https://www.anthropic.com/research/building-effective-agents)
  中文翻译：构建有效的 Agent——Anthropic 的模式论文
- [Handling stop reasons](https://platform.claude.com/docs/en/build-with-claude/handling-stop-reasons)
  中文翻译：处理 stop reason——循环的驱动信号
