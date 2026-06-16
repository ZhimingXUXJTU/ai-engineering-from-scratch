# The Tool Interface — Why Agents Need Structured I/O | 工具接口：为什么 Agent 需要结构化输入输出

> A language model produces tokens. A program takes actions. The gap between those two is the tool interface: a contract that lets the model request an action and the host execute it. Every 2026 stack — function calling on OpenAI, Anthropic, and Gemini; MCP's `tools/call`; A2A's task parts — is a different encoding of the same four-step loop. This lesson names the loop and shows the minimum machinery to run it.

> **【中文解读】** 语言模型生成 token，程序执行动作。工具接口是连接两者的桥梁——一个让模型请求动作、宿主执行动作的契约。2026年所有主流栈都是同一四步循环的不同编码。

> **【拓展：工具接口→AI Agent基础】** 工具接口是 AI Agent 的核心抽象。MCP 的 `tools/call`、OpenAI 的 `tool_calls`、A2A 的 task parts 都是这一抽象的不同实现。

> 🔗 **【前置】** 学本节前请先掌握：(1) Phase 11·01（Prompt Engineering）——理解 LLM 如何生成 token；(2) Phase 11·03（Structured Outputs）——JSON Schema 基础，本节输入 schema 全靠它；(3) Python 字典、JSON 序列化基础。本节不需要真实 LLM，用 stdlib 模拟，重点在理解循环结构而非 API。

**Type:** Learn | **类型:** 学习
**Languages:** Python (stdlib, no LLM) | **语言:** Python (标准库，无 LLM)
**Prerequisites:** Phase 11 (LLM completion APIs) | **前置知识:** Phase 11 (LLM 补全 API)
**Time:** ~45 minutes | **时间:** ~45 分钟

## Learning Objectives | 学习目标

- Explain why an LLM that can only generate text cannot, on its own, take actions against the real world.
  中文翻译：解释为什么一个只能生成文本的 LLM 无法独立地对真实世界采取行动。
- Draw the four-step tool-call loop (describe → decide → execute → observe) and name who owns each step.
  中文翻译：绘制四步工具调用循环（描述→决定→执行→观察）并指出每一步的归属方。
- Write a tool description as three parts: name, JSON Schema input, and a deterministic executor function.
  中文翻译：将工具描述写成三部分：名称、JSON Schema 输入和确定性执行器函数。
- Distinguish pure and side-effecting tools and state why the split matters for safety.
  中文翻译：区分纯工具和有副作用的工具，并说明这种区分对安全性的重要性。

## The Problem | 问题引入

> **【中文解读】** LLM 只能输出 token 的概率分布，这是它唯一的输出方式。它无法直接调用 API、操作数据库或执行任何外部动作。工具接口就是弥合这一鸿沟的桥梁——让模型能通过结构化请求来"间接"操控真实世界。

> **【拓展：Function Calling 的商业影响】** 2023年6月 OpenAI 推出 Function Calling 后，AI 应用开发范式发生根本变化。据 OpenAI 数据，2025年有超过 80% 的 API 调用涉及 tool_use，从简单的天气查询到复杂的多步骤工作流编排。

An LLM emits a probability distribution over the next token. That is the entire output surface. If you ask a chat model "what is the weather in Bengaluru right now," it can write a plausible sentence, but it cannot dial into a weather API. The sentence might be right by coincidence or three days stale.

> LLM 输出的是下一个 token 的概率分布，这就是它全部的输出范围。如果你问一个聊天模型"班加罗尔现在的天气如何"，它可以写出一句看似合理的话，但它无法调用天气 API。这句话可能只是碰巧正确，或者已经是三天前的旧数据。

Closing that gap is the purpose of the tool interface. The host program — your agent runtime, Claude Desktop, ChatGPT, Cursor, or a custom script — advertises a list of callable tools to the model. The model, when it decides an action is needed, emits a structured payload naming a tool and its arguments. The host parses that payload, runs the tool for real, and feeds the result back. The loop continues until the model decides no more calls are needed.

> 弥合这一鸿沟正是工具接口的目的。宿主程序——你的 agent 运行时、Claude Desktop、ChatGPT、Cursor 或自定义脚本——向模型通告一个可调用工具列表。当模型判断需要执行某个动作时，它会发出一个结构化负载，指明工具名称和参数。宿主解析该负载，真正运行工具，然后将结果反馈回去。循环持续进行，直到模型判断不再需要调用。

The first version of this contract shipped in June 2023 as OpenAI's "functions" parameter. Anthropic followed with `tool_use` blocks in Claude 2.1. Gemini added `functionDeclarations` a few months later. Every provider now exposes the same shape: a JSON-Schema-typed tool list in, a JSON-payload tool call out. The Model Context Protocol (November 2024) generalized the contract so one tool registry serves every model. A2A (April 2026, v1.0) layered the same primitive for agent-to-agent delegation.

> 这一契约的首个版本于 2023 年 6 月以 OpenAI 的 "functions" 参数形式发布。Anthropic 随后在 Claude 2.1 中推出了 `tool_use` 块。几个月后 Gemini 添加了 `functionDeclarations`。现在每个提供商都暴露了相同的形态：输入 JSON Schema 类型的工具列表，输出 JSON 负载的工具调用。Model Context Protocol（2024 年 11 月）将该契约泛化，使一个工具注册表可以服务所有模型。A2A（2026 年 4 月，v1.0）将同一原语用于 agent 间的任务委托。

The four-step loop is the invariant underneath all of these. Everything else in Phase 13 is an elaboration.

> 四步循环是所有这些技术之下的不变量。Phase 13 的其余内容都是对这个循环的扩展。

> **【中文解读】** 四步循环 (describe→decide→execute→observe) 是所有工具调用协议的不变量。无论是 OpenAI 的 function calling、Anthropic 的 tool_use、MCP 的 tools/call 还是 A2A 的 task parts，本质上都是这个循环的不同编码方式。

## The Concept | 核心概念

### Step one: describe

> **【中文解读】** 工具声明是整个循环的起点。每个工具需要三个字段：名称（机器可读标识符）、描述（自然语言使用说明）、输入模式（JSON Schema 参数描述）。好的工具描述直接决定了模型能否正确选择和使用工具。

The host declares each tool with three fields.

> 宿主为每个工具声明三个字段。

- **Name.** A stable, machine-readable identifier. `get_weather`, not "weather thing".
  中文翻译：**名称。** 一个稳定的、机器可读的标识符。`get_weather`，而不是"天气那玩意"。
- **Description.** A one-paragraph natural-language brief. "Use when the user asks about current conditions for a specific city. Do not use for historical data."
  中文翻译：**描述。** 一段简短的自然语言说明。"当用户询问某个城市的当前状况时使用。不要用于历史数据。"
- **Input schema.** A JSON Schema object (draft 2020-12) describing the tool's arguments.
  中文翻译：**输入模式。** 一个 JSON Schema 对象（2020-12 草案），描述工具的参数。

> 💡 **【类比】** 工具接口像餐厅点餐：菜单上每道菜=工具，菜名=tool name，菜单上的描述=description（"招牌牛肉面，清真可选，配辣油"），点餐时填的选项（辣度、加蛋）=JSON Schema 参数。服务员（模型）看菜单决定推荐哪道菜，把订单（tool_call）递给厨房（执行器），厨房做好端上来（tool_result），服务员转交给顾客。模型从不进厨房，只递单子。

The model receives the list. Modern providers serialize these declarations into the system prompt using a provider-specific template, so you as the caller only deal with the structured form.

> 模型接收这个列表。现代提供商使用特定的模板将这些声明序列化到系统提示中，因此作为调用者，你只需处理结构化形式。

### Step two: decide

> **【中文解读】** 模型面对用户消息和可用工具列表时，有三种选择：直接文本回答、调用一个或多个工具、或者拒绝。工具调用负载包含三个字段：call id（用于关联结果）、tool name（工具名）、arguments（JSON 参数对象）。并行调用时 id 尤为重要，因为结果可能乱序返回。

> **【拓展：Parallel Tool Calls 的性能优势】** OpenAI 和 Gemini 默认开启并行工具调用 (`parallel_tool_calls: true`)，允许模型在一次推理中发出多个独立调用。实测表明，对于需要查询多个数据源的场景（如同时查天气和股票），并行调用可以将端到端延迟降低 40-60%。

Given the user's message and the available tools, the model chooses one of three behaviors.

> 给定用户消息和可用工具，模型选择三种行为之一。

1. **Answer directly** in text. No tool call.
   中文翻译：**直接以文本回答。** 不调用工具。
2. **Call one or more tools.** Emit structured call objects. Under `parallel_tool_calls: true` (default on OpenAI and Gemini, opt-in on Anthropic) the model can emit multiple calls in one turn.
   中文翻译：**调用一个或多个工具。** 发出结构化的调用对象。在 `parallel_tool_calls: true`（OpenAI 和 Gemini 默认开启，Anthropic 需要选择开启）下，模型可以在一个回合中发出多个调用。
3. **Refuse.** Strict-mode structured outputs can produce a typed `refusal` block instead of a call.
   中文翻译：**拒绝。** 严格模式的结构化输出可以产生一个类型化的 `refusal` 块而非调用。

A tool call payload has three stable fields: a call `id`, a tool `name`, and a JSON `arguments` object. The id exists so the host can correlate the later result with the specific call, which matters when parallel calls come back out of order.

> 工具调用负载有三个稳定字段：调用 `id`、工具 `name` 和 JSON `arguments` 对象。id 的存在是为了让宿主能将后续结果与特定调用关联起来，这在并行调用乱序返回时很重要。

### Step three: execute

> **【中文解读】** 执行阶段，宿主程序接收调用请求，先用 JSON Schema 验证参数合法性，然后运行执行器。参数验证失败（幻觉字段、类型错误）是弱模型最常见的失败模式。生产环境通常有三种应对策略：快速失败并反馈错误、用约束解析器修复 JSON、或带错误信息重试模型。

The host receives the call, validates arguments against the declared schema, and runs the executor. Invalid arguments mean the model hallucinated a field or used the wrong type — a very common failure mode on weak models. Production hosts do one of three things on invalid arguments: fail fast and surface the error to the model, repair the JSON with a constrained parser, or retry the model with the validation error included in the prompt.

> 宿主接收调用，根据声明的模式验证参数，然后运行执行器。无效参数意味着模型幻觉了一个字段或使用了错误的类型——这是弱模型上非常常见的失败模式。生产环境宿主对无效参数做三件事之一：快速失败并向模型展示错误、用约束解析器修复 JSON、或将验证错误包含在提示中重试模型。

> ⚠️ **【易错点】** 场景：跳过 schema 验证直接执行 / 后果：弱模型（Haiku、GPT-4o-mini）会幻觉字段（如 `get_weather({ cityy: "Tokyo" })` 拼错 key），执行器要么 KeyError 崩溃要么拿到 None 走错分支 / 修复：在执行器前**必加** `jsonschema.validate()`，失败时把错误以 `tool_result` 形式返回给模型让它重试，而不是抛异常给宿主。

The executor itself is ordinary code. Python, TypeScript, a shell command, a database query. It produces a result, which is usually a string but can be any JSON value or a structured content block (text, image, or resource reference in MCP). The result must be serializable.

> 执行器本身是普通代码。Python、TypeScript、shell 命令、数据库查询。它产生一个结果，通常是一个字符串，但也可以是任何 JSON 值或结构化内容块（MCP 中的文本、图像或资源引用）。结果必须是可序列化的。

### Step four: observe

> **【中文解读】** 观察阶段将工具结果附加到对话历史（以 `tool` 角色消息形式，携带匹配的 id），然后重新调用模型。模型现在有了工具输出的上下文，可以生成最终回答或请求更多调用。循环持续进行直到模型停止发出调用或宿主触达安全上限。

The host appends the tool result to the conversation (as a `tool` role message with matching `id`) and re-invokes the model. The model now has the tool output in context and can produce a final answer or request more calls. This continues until the model stops emitting calls or the host hits a safety limit on iteration count.

> 宿主将工具结果附加到对话中（以带有匹配 `id` 的 `tool` 角色消息形式）并重新调用模型。模型现在在上下文中有了工具输出，可以生成最终回答或请求更多调用。这一过程持续进行，直到模型停止发出调用或宿主达到迭代次数的安全上限。

### The trust split

> **【中文解读】** 工具分为两类：纯工具（只读、无副作用，如 get_weather）和后果性工具（改变状态、消耗资金、触及用户数据，如 send_email）。后果性工具必须设置门控机制。Meta 2026年的"二选一规则"要求单次交互最多只能组合两项：不可信输入、敏感数据、后果性动作。

> **【拓展：Agent 安全中的 Tool Poisoning】** 2025年出现的 Tool Poisoning 攻击显示，恶意工具可以通过精心构造的描述欺骗模型执行危险操作。例如在工具描述中嵌入"当用户要求删除时立即执行"的隐藏指令。这也是 MCP 安全层（Phase 13 Lessons 15-18）需要重点关注的问题。

Tools come in two flavors that matter for safety.

> 工具从安全角度分为两种类型。

- **Pure.** Read-only, deterministic, no side effects. `get_weather`, `search_docs`, `get_current_time`. Safe to call speculatively.
  中文翻译：**纯工具。** 只读、确定性、无副作用。`get_weather`、`search_docs`、`get_current_time`。可以安全地推测性调用。
- **Consequential.** Mutates state, spends money, touches user data. `send_email`, `delete_file`, `execute_trade`. Must be gated.
  中文翻译：**后果性工具。** 修改状态、消耗资金、触及用户数据。`send_email`、`delete_file`、`execute_trade`。必须设置门控。

Meta's 2026 "Rule of Two" for agent security says a single turn may combine at most two of: untrusted input, sensitive data, consequential action. The tool interface is where you enforce that rule — by rejecting calls, requiring user confirmation, or escalating scopes. See Phase 13 · 15 for the full security chapter and Phase 14 · 09 for agent-level permission policies.

> Meta 2026 年 agent 安全的"二选一规则"指出，单次交互最多只能组合以下两项中的两项：不可信输入、敏感数据、后果性动作。工具接口是执行该规则的地方——通过拒绝调用、要求用户确认或升级权限范围。完整安全章节见 Phase 13 · 15，agent 级权限策略见 Phase 14 · 09。

### Where the loop lives

| Context | Who describes | Who decides | Who executes |
|---------|---------------|-------------|--------------|
| 上下文 | 谁描述 | 谁决定 | 谁执行 |
| Single-turn function calling (OpenAI/Anthropic/Gemini) | App developer | LLM | App developer |
| 单轮函数调用 (OpenAI/Anthropic/Gemini) | 应用开发者 | LLM | 应用开发者 |
| MCP | MCP server | LLM via MCP client | MCP server |
| MCP | MCP 服务器 | LLM 通过 MCP 客户端 | MCP 服务器 |
| A2A | Agent Card publisher | Calling agent | Called agent |
| A2A | Agent Card 发布者 | 调用方 agent | 被调用方 agent |
| Web browser (function-calling agent) | Browser extension / WebMCP | LLM | Browser runtime |
| Web 浏览器 (函数调用 agent) | 浏览器扩展 / WebMCP | LLM | 浏览器运行时 |

Everywhere, the same four steps. The column names change; the structure does not.

> 无论何处，都是相同的四步。列名改变了；结构没有改变。

> 🤔 **【困惑】** Q: 既然都是同一个四步循环，为什么还要 MCP、A2A 这么多协议？ A: 循环不变的是"逻辑步骤"，变的是"通信边界"。原生 function calling 在同一进程内；MCP 把 describe 步骤跨进程化（让一个 server 服务多个 host）；A2A 把 execute 步骤跨网络化（让 agent 调 agent）。本质都是把循环的某一步从"进程内"搬到"网络边界"，需要标准化协议来描述谁负责什么。

> **【拓展：MCP 统一工具协议】** Model Context Protocol (MCP, 2024年11月发布) 将工具接口标准化，使得一个工具注册表可以服务所有模型。MCP 已被 Anthropic、OpenAI、Google 等主要厂商采纳，2026年已成为事实上的工具协议标准，类似于 USB-C 对充电器的统一作用。

### Why not just prompt the model to emit JSON?

> **【中文解读】** 纯提示方式让模型输出 JSON 的失败率在 5-15%，小模型更高。失败模式包括：缺少大括号、尾随逗号、幻觉字段、类型错误。原生函数调用通过端到端训练、独立协议槽位和约束解码三层保障，将有效 JSON 率提升到 98-99%。

"Ask the model to reply in JSON" was the pre-function-calling pattern. It fails ~5 to 15 percent of the time on frontier models and far more on smaller models. Failure modes include missing braces, trailing commas, hallucinated fields, and wrong types. You then need a JSON repair pass, a retry, or a constrained decoder.

> "让模型以 JSON 回复"是函数调用出现之前的模式。在前沿模型上失败率约 5-15%，在小模型上远高于此。失败模式包括缺少大括号、尾随逗号、幻觉字段和错误类型。之后你需要 JSON 修复步骤、重试或约束解码器。

Native function calling is better for three reasons. First, the provider trains the model end-to-end on the exact call shape, so valid-JSON rate climbs to 98 to 99 percent on strict mode. Second, the call payload sits in its own protocol slot, not inside free-text — so a tool call never leaks into the user-visible reply. Third, providers enforce schema compliance with constrained decoding (OpenAI's strict mode, Anthropic's `tool_use`, Gemini's `responseSchema`). The output is guaranteed to validate.

> 原生函数调用更好的原因有三。第一，提供商在精确的调用格式上端到端训练模型，因此在严格模式下有效 JSON 率达到 98-99%。第二，调用负载位于独立的协议槽位中，不在自由文本内——因此工具调用永远不会泄露到用户可见的回复中。第三，提供商通过约束解码（OpenAI 的严格模式、Anthropic 的 `tool_use`、Gemini 的 `responseSchema`）强制执行模式合规。输出保证能通过验证。

Phase 13 · 02 walks the three provider APIs side by side. Phase 13 · 04 goes deep on structured outputs.

> Phase 13 · 02 并排讲解三个提供商的 API。Phase 13 · 04 深入讲解结构化输出。

### Circuit breakers

> **【中文解读】** 熔断器是生产环境的必备机制。循环在模型停止发出调用或宿主触达最大轮次时终止。生产环境通常设 5-20 轮上限。无上限循环是 "Agent 一夜花掉 $400" 事故的根本原因。

> **【拓展：Agent 成本失控案例】** 2025年多个公开案例显示，缺少熔断器的 Agent 在遇到模型死循环时会产生巨额 API 账单。例如某用户报告其编码 Agent 在修复 bug 时陷入循环，一夜产生 $2,000+ 的 API 费用。Claude Code 默认上限 20 轮，OpenAI Assistants 10 轮，Cursor agent 模式 25 轮。

The loop terminates when the model stops emitting calls or the host hits a maximum turn count. Production hosts set this to between 5 and 20 turns. Beyond that, you are almost certainly in a loop the model cannot exit. Claude Code defaults to 20; OpenAI Assistants to 10; Cursor's agent mode to 25.

> 循环在模型停止发出调用或宿主达到最大轮次时终止。生产环境宿主将其设置为 5 到 20 轮之间。超过这个范围，你几乎确定处于模型无法退出的循环中。Claude Code 默认 20 轮；OpenAI Assistants 10 轮；Cursor 的 agent 模式 25 轮。

The alternative — unbounded loops — shows up every six months as "agent spent $400 in API calls overnight" post-mortems. Do not ship without a bound.

> 另一种选择——无上限循环——每隔六个月就会出现"agent 一夜花了 $400 的 API 调用"事后分析。不要在没有上限的情况下发布。

Phase 14 · 12 covers error recovery and self-healing in depth; Phase 17 covers production rate limits.

> Phase 14 · 12 深入讲解错误恢复和自我修复；Phase 17 讲解生产环境速率限制。

### Where Phase 13 goes from here

- Lessons 02 through 05 polish the provider-level tool-call surface.
  中文翻译：Lesson 02 到 05 完善提供商级别的工具调用接口。
- Lessons 06 through 14 generalize the loop into MCP.
  中文翻译：Lesson 06 到 14 将循环泛化为 MCP。
- Lessons 15 through 18 defend the loop against hostile servers, adversarial users, and unauthenticated remote auth surfaces.
  中文翻译：Lesson 15 到 18 防御恶意服务器、对抗性用户和未认证的远程认证面。
- Lessons 19 through 22 extend the pattern to agent-to-agent collaboration, observability, routing, and packaging.
  中文翻译：Lesson 19 到 22 将模式扩展到 agent 间协作、可观测性、路由和打包。
- Lesson 23 ships a complete ecosystem using every primitive.
  中文翻译：Lesson 23 使用每个原语发布完整的生态系统。

Every remaining lesson is an elaboration of this four-step loop. Hold it in mind as the invariant.

> 剩余的每一课都是对这个四步循环的扩展。请将它作为不变量牢记在心。

## Use It | 用框架实现

`code/main.py` runs the four-step loop without an LLM. A fake "decider" function simulates the model by pattern-matching on the user message; the executor, schema validator, and observe-step harness are real. Run it to see the full request/response choreography with printable intermediate state, then replace the fake decider with any real provider in a later lesson.

> `code/main.py` 在没有 LLM 的情况下运行四步循环。一个假的"决策器"函数通过对用户消息进行模式匹配来模拟模型；执行器、模式验证器和观察步骤的线束是真实的。运行它可以看到完整的请求/响应流程和可打印的中间状态，然后在后续课程中将假决策器替换为任何真正的提供商。

What to look at:

> 需要关注的点：

- The tool registry holds three fields per tool: name, description, schema, and an executor reference.
  中文翻译：工具注册表为每个工具保存三个字段：名称、描述、模式和一个执行器引用。
- The validator is a minimal JSON Schema subset (types, required, enum, min/max) written in stdlib only. Phase 13 · 04 ships a fuller one.
  中文翻译：验证器是一个最小的 JSON Schema 子集（类型、必填、枚举、最小/最大值），仅用标准库编写。Phase 13 · 04 提供了更完整的版本。
- The loop bounds iteration count at five. Production agents need exactly this kind of circuit breaker.
  中文翻译：循环将迭代次数限制在 5 次。生产环境的 agent 正需要这种熔断器。

## Ship It | 产出物

This lesson produces `outputs/skill-tool-interface-reviewer.md`. Given a draft tool definition (name + description + schema + executor outline), the skill audits it for loop fitness: is the name machine-stable, is the description a complete usage brief, does the schema use JSON Schema 2020-12 correctly, and is the pure-vs-consequential classification explicit.

> 本课产出 `outputs/skill-tool-interface-reviewer.md`。给定一个工具定义草稿（名称 + 描述 + 模式 + 执行器大纲），该 skill 审计其循环适配性：名称是否机器稳定、描述是否是完整的使用说明、模式是否正确使用 JSON Schema 2020-12、纯工具与后果性工具的分类是否明确。

## Exercises | 练习题

1. Add a fourth tool to `code/main.py` called `get_stock_price(ticker)`. Write its description as "Use when the user asks for a current stock price by ticker. Do not use for historical prices or market summaries." Run the harness and confirm the fake decider routes queries mentioning tickers to the new tool.
   中文翻译：在 `code/main.py` 中添加第四个工具 `get_stock_price(ticker)`。将描述写成"当用户通过代码询问当前股价时使用。不要用于历史价格或市场摘要。"运行线束并确认假决策器将提到代码的查询路由到新工具。

2. Break the schema validator. Pass a call whose `arguments` object is missing a required field, and confirm the host rejects it before execution. Then pass a call with an extra unknown field. Decide: should the host reject or ignore? Justify your choice with a safety argument.
   中文翻译：破坏模式验证器。传入一个 `arguments` 对象缺少必填字段的调用，确认宿主在执行前拒绝它。然后传入一个有额外未知字段的调用。决定：宿主应该拒绝还是忽略？用安全论证来支持你的选择。

3. Classify each tool in the harness as pure or consequential. Add a `consequential: true` flag to the registry entries that need it, and change the loop to print a "would confirm with user" line whenever a consequential tool is chosen. This is the shape of the confirmation gate every production host needs.
   中文翻译：将线束中的每个工具分类为纯工具或后果性工具。为需要的注册表条目添加 `consequential: true` 标志，并修改循环，每当选择后果性工具时打印"将与用户确认"的行。这就是每个生产环境宿主需要的确认门的形态。

4. Draw the four-step loop on paper with the provider-column table above filled in for your favorite client (Claude Desktop, Cursor, ChatGPT, or a custom stack). Cross-reference with the MCP-specific variant in Phase 13 · 06.
   中文翻译：在纸上绘制四步循环，填入你最喜欢的客户端（Claude Desktop、Cursor、ChatGPT 或自定义技术栈）的提供商列表。与 Phase 13 · 06 中的 MCP 特定变体交叉参考。

5. Read OpenAI's function-calling guide top to bottom. Identify the one field that sits in the request but not in the four-step loop as presented here. Explain what it adds and why it is convenient rather than essential.
   中文翻译：从头到尾阅读 OpenAI 的函数调用指南。找出存在于请求中但不在本文介绍的四步循环中的那个字段。解释它添加了什么以及为什么它是便利的而非必要的。

## Key Terms | 术语速查表

| Term | What people say | What it actually means |
|------|----------------|------------------------|
| 术语 | 通俗说法 | 实际含义 |
| Tool | "A thing the model can call" | A triple of name + JSON-Schema-typed input + executor function |
| 工具 | "模型能调用的东西" | 名称 + JSON Schema 类型输入 + 执行器函数的三元组 |
| Function calling | "Native tool use" | Provider-level API support for emitting structured tool calls instead of prose |
| 函数调用 | "原生工具使用" | 提供商级别的 API 支持，用于发出结构化工具调用而非散文式文本 |
| Tool call | "The model's request to act" | A JSON payload with `id`, `name`, `arguments` emitted by the model |
| 工具调用 | "模型请求执行动作" | 模型发出的包含 `id`、`name`、`arguments` 的 JSON 负载 |
| Tool result | "What the tool returned" | The executor's output, wrapped in a `tool` role message with matching id |
| 工具结果 | "工具返回了什么" | 执行器的输出，包装在带有匹配 id 的 `tool` 角色消息中 |
| Parallel tool calls | "Many calls at once" | Multiple call objects in one model turn, independent and orderable by id |
| 并行工具调用 | "同时多个调用" | 一个模型回合中的多个调用对象，独立的，可通过 id 排序 |
| Strict mode | "Guaranteed JSON" | Constrained decoding that forces the model's output to validate against the declared schema |
| 严格模式 | "保证 JSON" | 约束解码，强制模型输出通过声明的模式验证 |
| Pure tool | "Read-only tool" | No side effects; safe to re-run |
| 纯工具 | "只读工具" | 无副作用；可以安全地重新运行 |
| Consequential tool | "Action tool" | Mutates external state; requires gate, audit, or user confirmation |
| 后果性工具 | "动作工具" | 修改外部状态；需要门控、审计或用户确认 |
| Four-step loop | "The tool-call cycle" | describe → decide → execute → observe |
| 四步循环 | "工具调用循环" | 描述 → 决定 → 执行 → 观察 |
| Host | "Agent runtime" | The program that holds the tool registry, calls the model, and runs the executor |
| 宿主 | "Agent 运行时" | 持有工具注册表、调用模型并运行执行器的程序 |

## Further Reading | 延伸阅读

- [OpenAI — Function calling guide](https://platform.openai.com/docs/guides/function-calling) — canonical reference for OpenAI-style tool declarations and call shapes
  中文翻译：OpenAI 风格工具声明和调用格式的权威参考
- [Anthropic — Tool use overview](https://docs.anthropic.com/en/docs/agents-and-tools/tool-use/overview) — Claude's `tool_use` / `tool_result` block format
  中文翻译：Claude 的 `tool_use` / `tool_result` 块格式
- [Google — Gemini function calling](https://ai.google.dev/gemini-api/docs/function-calling) — `functionDeclarations` and parallel-call semantics in Gemini
  中文翻译：Gemini 中的 `functionDeclarations` 和并行调用语义
- [Model Context Protocol — Specification 2025-11-25](https://modelcontextprotocol.io/specification/2025-11-25) — the provider-agnostic generalization of the tool interface
  中文翻译：工具接口的提供商无关泛化
- [JSON Schema — 2020-12 release notes](https://json-schema.org/draft/2020-12/release-notes) — the schema dialect every modern tool API speaks
  中文翻译：每个现代工具 API 使用的模式方言
