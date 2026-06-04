# 函数调用深入 — OpenAI、Anthropic、Gemini 对比

> 三大前沿供应商在 2024 年收敛于相同的工具调用循环，但在其他方面各不相同。OpenAI 使用 `tools` 和 `tool_calls`。Anthropic 使用 `tool_use` 和 `tool_result` 块。Gemini 使用 `functionDeclarations` 和唯一 ID 关联。本课并排对比三者，使在一个供应商上编写的代码在移植时不会出错。

> **【中文解读】** 三大前沿供应商在 2024 年收敛于相同的工具调用循环，但具体实现各有差异。OpenAI 用 `tools`/`tool_calls`，Anthropic 用 `tool_use`/`tool_result` 块，Gemini 用 `functionDeclarations` 和唯一 ID 关联。本课三路对比，让你在一个供应商上写的代码移植到另一个时不至于崩溃。

> **【拓展：Function Calling】** 函数调用（Function Calling）是 LLM 与外部世界交互的核心机制。LLM 不直接执行操作，而是输出结构化的"调用意图"（工具名+参数），由宿主程序执行后返回结果。三大供应商的 API 形状不同但语义等价：声明工具→模型选择调用→宿主执行→结果注入→模型继续推理。理解这一循环是构建跨平台 Agent 的基础。

**类型：** 构建
**语言：** Python（标准库，Schema 翻译器）
**前置条件：** Phase 13 · 01（工具接口）
**时间：** 约 75 分钟

## 学习目标

- 说明 OpenAI、Anthropic、Gemini 函数调用载荷的三种形态差异（声明、调用、结果）。
- 将一个工具声明翻译为三种供应商格式，预测 strict 模式约束在哪会不同。
- 在每个供应商中使用 `tool_choice` 强制、禁止或自动选择工具调用。
- 了解各供应商的硬限制（工具数量、Schema 深度、参数长度）及违反限制时的错误特征。

## 问题引入

函数调用请求的格式因供应商而异。2026 年生产栈中的三个具体示例：

**OpenAI Chat Completions / Responses API。** 你传递 `tools: [{type: "function", function: {name, description, parameters, strict}}]`。模型响应包含 `choices[0].message.tool_calls: [{id, type: "function", function: {name, arguments}}]`，其中 `arguments` 是你需要解析的 JSON 字符串。严格模式（`strict: true`）通过约束解码强制执行 Schema 合规性。

**Anthropic Messages API。** 你传递 `tools: [{name, description, input_schema}]`。响应返回为 `content: [{type: "text"}, {type: "tool_use", id, name, input}]`。`input` 已经解析完毕（一个对象，而非字符串）。你用包含 `{type: "tool_result", tool_use_id, content}` 块的新 `user` 消息回复。

**Google Gemini API。** 你传递 `tools: [{functionDeclarations: [{name, description, parameters}]}]`（嵌套在 `functionDeclarations` 下）。响应以 `candidates[0].content.parts: [{functionCall: {name, args, id}}]` 形式到达，其中 `id` 在 Gemini 3 及以上版本中是唯一的，用于并行调用关联。你用 `{functionResponse: {name, id, response}}` 回复。

同一个循环。不同的字段名、不同的嵌套方式、不同的字符串 vs 对象约定、不同的关联机制。一个在 OpenAI 上编写天气 Agent 的团队需要两天的 Anthropic 移植和一天的 Gemini 移植，仅仅是为了管道工程。

本课构建一个翻译器，将三种格式统一为一个规范的工具声明并在边缘路由。Phase 13 · 17 将相同的模式泛化为 LLM 网关。

## 核心概念

### 通用结构

每个供应商需要五样东西：

1. **工具列表。** 每个工具的名称、描述和输入 Schema。
2. **工具选择。** 强制特定工具、禁止工具或让模型决定。
3. **调用发出。** 命名工具和参数的结构化输出。
4. **调用 ID。** 将响应关联到正确的调用（并行时很重要）。
5. **结果注入。** 将结果绑定回调用的消息或块。

### 逐字段对比

| 方面 | OpenAI | Anthropic | Gemini |
|------|--------|-----------|--------|
| 声明信封 | `{type: "function", function: {...}}` | `{name, description, input_schema}` | `{functionDeclarations: [{...}]}` |
| Schema 字段 | `parameters` | `input_schema` | `parameters` |
| 响应容器 | assistant 消息上的 `tool_calls[]` | `content[]` 中 `tool_use` 类型 | `parts[]` 中 `functionCall` 类型 |
| 参数类型 | 字符串化 JSON | 解析后对象 | 解析后对象 |
| ID 格式 | `call_...`（OpenAI 生成） | `toolu_...`（Anthropic） | UUID（Gemini 3+） |
| 结果块 | role `tool`，`tool_call_id` | `user` 携带 `tool_result`，`tool_use_id` | `functionResponse` 携带匹配的 `id` |
| 强制工具 | `tool_choice: {type: "function", function: {name}}` | `tool_choice: {type: "tool", name}` | `tool_config: {function_calling_config: {mode: "ANY"}}` |
| 禁止工具 | `tool_choice: "none"` | `tool_choice: {type: "none"}` | `mode: "NONE"` |
| 严格 Schema | `strict: true` | schema-is-schema（始终强制） | 请求级 `responseSchema` |

### 实际会遇到的限制

- **OpenAI。** 每个请求 128 个工具。Schema 深度 5。参数字符串 ≤ 8192 字节。严格模式不支持 `$ref`、不支持有重叠的 `oneOf`/`anyOf`/`allOf`，每个属性必须在 `required` 中列出。
- **Anthropic。** 每个请求 64 个工具。Schema 深度实际上无硬限制但实际约 10。无 strict 模式标志；Schema 是契约，模型倾向于遵守。
- **Gemini。** 每个请求 64 个函数。Schema 类型是 OpenAPI 3.0 子集（与 JSON Schema 2020-12 有细微差异）。Gemini 3 起并行调用支持唯一 ID。

### `tool_choice` 行为

每个人都支持的三种模式，名称不同。

- **Auto（自动）。** 模型选择工具或文本。默认。
- **Required / Any（必需/任意）。** 模型必须调用至少一个工具。
- **None（无）。** 模型不得调用工具。

加上每个供应商独有的模式：

- **OpenAI。** 按名称强制特定工具。
- **Anthropic。** 按名称强制特定工具；`disable_parallel_tool_use` 标志区分单次 vs 多次。
- **Gemini。** `mode: "VALIDATED"` 将每个响应通过 Schema 验证器路由，无论模型意图如何。

### 并行调用

OpenAI 的 `parallel_tool_calls: true`（默认）在一个 assistant 消息中发出多个调用。你运行它们全部并用包含每个 `tool_call_id` 条目的批量 tool-role 消息回复。Anthropic 历史上是单次调用；`disable_parallel_tool_use: false`（Claude 3.5 起默认）启用多次。Gemini 2 允许并行调用但不提供稳定 ID；Gemini 3 添加 UUID 使乱序响应可以干净地关联。

### 流式传输

三者都支持流式工具调用。线格式不同：

- **OpenAI。** `tool_calls[i].function.arguments` 的增量块逐步到达。你累积直到 `finish_reason: "tool_calls"`。
- **Anthropic。** block-start / block-delta / block-stop 事件。`input_json_delta` 块携带部分参数。
- **Gemini。** `streamFunctionCallArguments`（Gemini 3 新增）发出带有 `functionCallId` 的块，使多个并行调用可以交错。

Phase 13 · 03 深入讲解并行 + 流式重组。本课聚焦声明和单次调用形状。

### 错误与修复

无效参数错误看起来也不同。

- **OpenAI（非严格）。** 模型返回 `arguments: "{bad json}"`，你的 JSON 解析失败，你注入错误消息并重新调用。
- **OpenAI（严格）。** 解码期间进行验证；无效 JSON 不可能出现，但 `refusal` 可能出现。
- **Anthropic。** `input` 可能包含意外字段；Schema 是建议性的。需在服务端验证。
- **Gemini。** OpenAPI 3.0 怪癖：对象字段上的 `enum` 被静默忽略；需自行验证。

### 翻译器模式

你代码中的规范工具声明看起来像这样（你选择形状）：

```python
Tool(
    name="get_weather",
    description="Use when ...",
    input_schema={"type": "object", "properties": {...}, "required": [...]},
    strict=True,
)
```

三个小函数将其翻译为三种供应商形状。`code/main.py` 中的线束正是这样做的，然后通过每个供应商的响应形状进行一次往返。不需要网络——本课教授形状，而非 HTTP。

生产团队将此翻译器包装为 `AbstractToolset`（Pydantic AI）、`UniversalToolNode`（LangGraph）或 `BaseTool`（LlamaIndex）。Phase 13 · 17 提供一个在前端暴露 OpenAI 形状 API 并后端对接三个中任何一个的网关。

## 用框架实现

`code/main.py` 定义了一个规范的 `Tool` 数据类和三个翻译器，分别发出 OpenAI、Anthropic 和 Gemini 的声明 JSON。然后将每个形状的手工供应商响应解析为相同的规范调用对象，证明底层语义完全相同。运行它并并排对比三种声明。

关注点：

- 三个声明块仅在信封和字段名上有所不同。
- 三个响应块在调用位置上有所不同（顶层 `tool_calls`、`content[]` 块、`parts[]` 条目）。
- 一个 `canonical_call()` 函数从所有三种响应形状中提取 `{id, name, args}`。

## 产出物

本课产生 `outputs/skill-provider-portability-audit.md`。给定一个针对某个供应商的函数调用集成，该技能生成可移植性审计：依赖了哪些供应商限制、哪些字段需要重命名、移植到其他供应商时会出什么问题。

## 练习题

1. 运行 `code/main.py`，验证三个供应商声明 JSON 都序列化同一个 `Tool` 对象。修改规范工具添加 enum 参数，确认只有 Gemini 翻译器需处理 OpenAPI 怪癖。

2. 为每个供应商添加 `ListToolsResponse` 解析器，提取模型在 `list_tools` 或发现调用后返回的工具列表。注意 OpenAI 原生不支持这一功能的非对称性。

3. 实现 `tool_choice` 转换：将规范的 `ToolChoice(mode="force", tool_name="x")` 映射到三种供应商格式。然后映射 `mode="any"` 和 `mode="none"`。对照本课的对比表检查。

4. 选择三个供应商中的一个，从头到尾阅读其函数调用指南。找出一个其 Schema 规范中其他两个不支持的字段。候选：OpenAI `strict`、Anthropic `disable_parallel_tool_use`、Gemini `function_calling_config.allowed_function_names`。

5. 编写测试向量：一个参数违反声明 Schema 的工具调用。通过每个供应商的验证器运行（第 01 课的标准库版本可以作为代理），记录哪些错误触发。记录在生产中你会选择哪个供应商来获得严格性。

## 关键术语

| 术语 | 人们怎么说 | 实际含义 |
|------|-----------|---------|
| Function calling（函数调用） | "工具使用" | 用于结构化工具调用发出的供应商级 API |
| Tool declaration（工具声明） | "工具规格" | 名称 + 描述 + JSON Schema 输入载荷 |
| `tool_choice` | "强制 / 禁止" | auto / required / none / 指定名称模式 |
| Strict mode（严格模式） | "Schema 强制执行" | OpenAI 标志，通过约束解码匹配 Schema |
| `tool_use` 块 | "Anthropic 的调用形状" | 内联内容块，包含 id、name、input |
| `functionCall` 部分 | "Gemini 的调用形状" | 包含 name、args 和 id 的 `parts[]` 条目 |
| Arguments-as-string（参数为字符串） | "字符串化 JSON" | OpenAI 将参数作为 JSON 字符串返回，而非对象 |
| Parallel tool calls（并行工具调用） | "一轮扇出" | 一个 assistant 消息中的多个工具调用 |
| Refusal（拒绝） | "模型拒绝" | 严格模式下代替调用的拒绝块 |
| OpenAPI 3.0 子集 | "Gemini Schema 怪癖" | Gemini 使用与 JSON Schema 略有不同的类方言 |

## 延伸阅读

- [OpenAI — Function calling guide](https://platform.openai.com/docs/guides/function-calling) — 包含严格模式和并行调用的权威参考
- [Anthropic — Tool use overview](https://docs.anthropic.com/en/docs/agents-and-tools/tool-use/overview) — `tool_use` 和 `tool_result` 块语义
- [Google — Gemini function calling](https://ai.google.dev/gemini-api/docs/function-calling) — 并行调用、唯一 ID 和 OpenAPI 子集
- [Vertex AI — Function calling reference](https://docs.cloud.google.com/vertex-ai/generative-ai/docs/multimodal/function-calling) — Gemini 的企业表面
- [OpenAI — Structured outputs](https://platform.openai.com/docs/guides/structured-outputs) — 严格模式 Schema 强制执行详情
