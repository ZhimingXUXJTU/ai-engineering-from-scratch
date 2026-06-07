# Function Calling Deep Dive — OpenAI, Anthropic, Gemini | 函数调用深入：三大供应商对比

> The three frontier providers converged on the same tool-call loop in 2024 and then diverged on everything else. OpenAI uses `tools` and `tool_calls`. Anthropic uses `tool_use` and `tool_result` blocks. Gemini uses `functionDeclarations` and unique-id correlation. This lesson diffs the three side by side so code that ships on one provider does not break when you port it.

> **【中文解读】** 三大前沿供应商在 2024 年收敛于相同的工具调用循环，但具体实现各有差异。OpenAI 用 `tools`/`tool_calls`，Anthropic 用 `tool_use`/`tool_result` 块，Gemini 用 `functionDeclarations` 和唯一 ID 关联。本课三路对比，让你在一个供应商上写的代码移植到另一个时不至于崩溃。

> **【拓展：Function Calling】** 函数调用（Function Calling）是 LLM 与外部世界交互的核心机制。LLM 不直接执行操作，而是输出结构化的"调用意图"（工具名+参数），由宿主程序执行后返回结果。三大供应商的 API 形状不同但语义等价：声明工具→模型选择调用→宿主执行→结果注入→模型继续推理。理解这一循环是构建跨平台 Agent 的基础。

**Type:** Build | **类型:** 构建
**Languages:** Python (stdlib, schema translators) | **语言:** Python（标准库，模式翻译器）
**Prerequisites:** Phase 13 · 01 (the tool interface) | **前置知识:** Phase 13 · 01（工具接口）
**Time:** ~75 minutes | **时间:** ~75 分钟

## Learning Objectives | 学习目标

- State the three shape differences between OpenAI, Anthropic, and Gemini function-calling payloads (declaration, call, result).
  说明 OpenAI、Anthropic、Gemini 函数调用载荷的三种形态差异（声明、调用、结果）。
- Translate one tool declaration across all three provider formats and predict where strict-mode constraints will differ.
  将一个工具声明翻译为三种供应商格式，预测 strict 模式约束在哪会不同。
- Use `tool_choice` in each provider to force, forbid, or auto-pick tool calls.
  在每个供应商中使用 `tool_choice` 强制、禁止或自动选择工具调用。
- Know the per-provider hard limits (tool count, schema depth, argument length) and the error signatures each one emits when limits are violated.
  了解各供应商的硬限制（工具数量、Schema 深度、参数长度）及违反限制时的错误特征。

## The Problem | 问题引入

The shape of a function-calling request differs by provider. Three concrete examples from 2026 production stacks:

> 函数调用请求的格式因供应商而异。以下是 2026 年生产技术栈中的三个具体示例：

> **【中文解读】** 函数调用请求的格式因供应商而异。OpenAI 用 `tools`+`tool_calls`，响应中 `arguments` 是需要手动解析的 JSON 字符串；Anthropic 用 `tool_use`/`tool_result` 块，`input` 已经是解析好的对象；Gemini 用嵌套的 `functionDeclarations`，结果通过 `functionResponse` 返回。同一个循环，不同的字段名、嵌套方式、字符串 vs 对象约定和关联机制——从一个供应商移植到另一个仅"管道工程"就需要两三天。

**OpenAI Chat Completions / Responses API.** You pass `tools: [{type: "function", function: {name, description, parameters, strict}}]`. The model's response contains `choices[0].message.tool_calls: [{id, type: "function", function: {name, arguments}}]` where `arguments` is a JSON string you must parse. Strict mode (`strict: true`) enforces schema compliance via constrained decoding.

> **OpenAI Chat Completions / Responses API。** 你传入 `tools: [{type: "function", function: {name, description, parameters, strict}}]`。模型的响应包含 `choices[0].message.tool_calls: [{id, type: "function", function: {name, arguments}}]`，其中 `arguments` 是一个需要你手动解析的 JSON 字符串。严格模式（`strict: true`）通过约束解码强制执行模式合规。

**Anthropic Messages API.** You pass `tools: [{name, description, input_schema}]`. The response comes back as `content: [{type: "text"}, {type: "tool_use", id, name, input}]`. `input` is already parsed (an object, not a string). You reply with a new `user` message containing a `{type: "tool_result", tool_use_id, content}` block.

> **Anthropic Messages API。** 你传入 `tools: [{name, description, input_schema}]`。响应以 `content: [{type: "text"}, {type: "tool_use", id, name, input}]` 形式返回。`input` 已经被解析（是一个对象，不是字符串）。你用包含 `{type: "tool_result", tool_use_id, content}` 块的新 `user` 消息回复。

**Google Gemini API.** You pass `tools: [{functionDeclarations: [{name, description, parameters}]}]` (nested under `functionDeclarations`). The response arrives as `candidates[0].content.parts: [{functionCall: {name, args, id}}]` where `id` is unique in Gemini 3 and up for parallel-call correlation. You reply with `{functionResponse: {name, id, response}}`.

> **Google Gemini API。** 你传入 `tools: [{functionDeclarations: [{name, description, parameters}]}]`（嵌套在 `functionDeclarations` 下）。响应以 `candidates[0].content.parts: [{functionCall: {name, args, id}}]` 形式到达，其中 `id` 在 Gemini 3 及以上版本中是唯一的，用于并行调用关联。你用 `{functionResponse: {name, id, response}}` 回复。

Same loop. Different field names, different nesting, different string-vs-object conventions, different correlation mechanisms. A team that writes a weather agent on OpenAI pays a two-day port to Anthropic and another day to Gemini just for the plumbing.

> 同样的循环。不同的字段名、不同的嵌套方式、不同的字符串与对象约定、不同的关联机制。一个在 OpenAI 上写天气 agent 的团队移植到 Anthropic 需要两天，再到 Gemini 又需要一天——仅仅是管道工程。

This lesson builds a translator that unifies the three formats into one canonical tool declaration and routes at the edge. Phase 13 · 17 generalizes the same pattern into an LLM gateway.

> 本课构建一个翻译器，将三种格式统一为一个规范的工具声明，并在边缘进行路由。Phase 13 · 17 将同一模式泛化为 LLM 网关。

## The Concept | 核心概念

### The common structure | 通用结构

Every provider needs five things:

> 每个供应商都需要五样东西：

1. **Tool list.** Per-tool name, description, and input schema.
   中文翻译：**工具列表。** 每个工具的名称、描述和输入模式。
2. **Tool choice.** Force a specific tool, forbid tools, or let the model decide.
   中文翻译：**工具选择。** 强制使用特定工具、禁止使用工具或让模型自行决定。
3. **Call emission.** Structured output naming the tool and arguments.
   中文翻译：**调用输出。** 命名工具和参数的结构化输出。
4. **Call id.** Correlate the response to the right call (matters for parallel).
   中文翻译：**调用 ID。** 将响应关联到正确的调用（并行时很关键）。
5. **Result injection.** A message or block that ties the result back to the call.
   中文翻译：**结果注入。** 将结果绑定回调用的消息或块。

> **【中文解读】** 每个供应商都需要五样东西：工具列表（名称+描述+输入 Schema）、工具选择（强制/禁止/自动）、调用输出（结构化的工具名和参数）、调用 ID（关联响应到正确的调用，并行时关键）、结果注入（将结果绑回调用的消息或块）。

### Shape diffs, field by field

| Aspect | OpenAI | Anthropic | Gemini |
|--------|--------|-----------|--------|
| 方面 | OpenAI | Anthropic | Gemini |
| Declaration envelope | `{type: "function", function: {...}}` | `{name, description, input_schema}` | `{functionDeclarations: [{...}]}` |
| 声明信封 | `{type: "function", function: {...}}` | `{name, description, input_schema}` | `{functionDeclarations: [{...}]}` |
| Schema field | `parameters` | `input_schema` | `parameters` |
| Schema 字段 | `parameters` | `input_schema` | `parameters` |
| Response container | `tool_calls[]` on assistant message | `content[]` of type `tool_use` | `parts[]` of type `functionCall` |
| 响应容器 | assistant 消息上的 `tool_calls[]` | `content[]` 中类型为 `tool_use` 的块 | `parts[]` 中类型为 `functionCall` 的条目 |
| Arguments type | stringified JSON | parsed object | parsed object |
| 参数类型 | 字符串化 JSON | 已解析对象 | 已解析对象 |
| Id format | `call_...` (OpenAI generates) | `toolu_...` (Anthropic) | UUID (Gemini 3+) |
| ID 格式 | `call_...`（OpenAI 生成） | `toolu_...`（Anthropic） | UUID（Gemini 3+） |
| Result block | role `tool`, `tool_call_id` | `user` with `tool_result`, `tool_use_id` | `functionResponse` with matching `id` |
| 结果块 | 角色 `tool`，`tool_call_id` | 带有 `tool_result` 的 `user` 消息，`tool_use_id` | 带有匹配 `id` 的 `functionResponse` |
| Force-a-tool | `tool_choice: {type: "function", function: {name}}` | `tool_choice: {type: "tool", name}` | `tool_config: {function_calling_config: {mode: "ANY"}}` |
| 强制工具 | `tool_choice: {type: "function", function: {name}}` | `tool_choice: {type: "tool", name}` | `tool_config: {function_calling_config: {mode: "ANY"}}` |
| Forbid tools | `tool_choice: "none"` | `tool_choice: {type: "none"}` | `mode: "NONE"` |
| 禁止工具 | `tool_choice: "none"` | `tool_choice: {type: "none"}` | `mode: "NONE"` |
| Strict schema | `strict: true` | schema-is-schema (always enforced) | `responseSchema` at request level |
| 严格模式 | `strict: true` | 模式即模式（始终强制执行） | 请求级别的 `responseSchema` |

### Limits you will actually hit | 实际会遇到的限制

> **【中文解读】** OpenAI：128 个工具/请求，Schema 深度 5，参数字符串 ≤8192 字节，strict 模式不支持 `$ref`/`oneOf` 等重叠组合。Anthropic：64 个工具/请求，Schema 深度无硬限制但实际约 10，无 strict 模式标志但模型倾向于遵守。Gemini：64 个函数/请求，使用 OpenAPI 3.0 子集（与 JSON Schema 2020-12 有细微差异），Gemini 3 起支持唯一 ID。

- **OpenAI.** 128 tools per request. Schema depth 5. Argument string <= 8192 bytes. Strict mode requires no `$ref`, no `oneOf`/`anyOf`/`allOf` with overlap, every property listed in `required`.
  中文翻译：**OpenAI。** 每个请求 128 个工具。Schema 深度 5。参数字符串 ≤ 8192 字节。严格模式要求无 `$ref`，无重叠的 `oneOf`/`anyOf`/`allOf`，每个属性都列在 `required` 中。
- **Anthropic.** 64 tools per request. Schema depth effectively unbounded but practical limit 10. No strict-mode flag; schema is a contract and the model tends to comply.
  中文翻译：**Anthropic。** 每个请求 64 个工具。Schema 深度实际上无限制但实际约 10。无严格模式标志；模式是契约，模型倾向于遵守。
- **Gemini.** 64 functions per request. Schema types are OpenAPI 3.0 subset (slight divergence from JSON Schema 2020-12). Parallel calls unique-id since Gemini 3.
  中文翻译：**Gemini。** 每个请求 64 个函数。Schema 类型是 OpenAPI 3.0 子集（与 JSON Schema 2020-12 有细微差异）。Gemini 3 起支持并行调用的唯一 ID。

### `tool_choice` behavior

Three modes everyone supports, named differently.

> 三种模式每个供应商都支持，但命名不同。

- **Auto.** Model picks tool or text. Default.
  中文翻译：**自动。** 模型选择工具或文本。默认值。
- **Required / Any.** Model must call at least one tool.
  中文翻译：**必需 / 任意。** 模型必须至少调用一个工具。
- **None.** Model must not call tools.
  中文翻译：**无。** 模型不得调用工具。

Plus one mode unique to each provider:

> 加上每个供应商独有的一个模式：

- **OpenAI.** Force a specific tool by name.
  中文翻译：**OpenAI。** 按名称强制特定工具。
- **Anthropic.** Force a specific tool by name; `disable_parallel_tool_use` flag separates single vs multi.
  中文翻译：**Anthropic。** 按名称强制特定工具；`disable_parallel_tool_use` 标志区分单次与多次调用。
- **Gemini.** `mode: "VALIDATED"` routes every response through a schema validator regardless of model intent.
  中文翻译：**Gemini。** `mode: "VALIDATED"` 将每个响应通过模式验证器，不论模型意图如何。

### Parallel calls

> **【拓展：并行调用的生产实践】** 并行工具调用可以显著减少端到端延迟。例如一个旅行规划 Agent 需要同时查询航班、酒店、天气三个独立 API，串行需要 3 轮 LLM 调用（约 15 秒），并行只需 1 轮（约 5 秒）。但要注意：并行调用会增加 token 消耗和执行复杂度，且需要正确处理乱序结果。

OpenAI's `parallel_tool_calls: true` (default) emits multiple calls in one assistant message. You run them all and reply with a batched tool-role message containing one entry per `tool_call_id`. Anthropic historically did single-call; `disable_parallel_tool_use: false` (default as of Claude 3.5) enables multi. Gemini 2 allowed parallel calls but did not give stable ids; Gemini 3 adds UUIDs so out-of-order responses correlate cleanly.

> OpenAI 的 `parallel_tool_calls: true`（默认）在一条 assistant 消息中发出多个调用。你运行所有调用，然后回复一个批量工具角色消息，每个 `tool_call_id` 一个条目。Anthropic 历史上只做单次调用；`disable_parallel_tool_use: false`（Claude 3.5 起默认）启用了多次调用。Gemini 2 允许并行调用但没有稳定的 ID；Gemini 3 添加了 UUID，使乱序响应可以干净地关联。

### Streaming

All three support streamed tool calls. The wire format differs:

> 三者都支持流式工具调用。传输格式有所不同：

- **OpenAI.** Delta chunks of `tool_calls[i].function.arguments` arrive incrementally. You accumulate until `finish_reason: "tool_calls"`.
  中文翻译：**OpenAI。** `tool_calls[i].function.arguments` 的增量块逐步到达。你累积直到 `finish_reason: "tool_calls"`。
- **Anthropic.** Block-start / block-delta / block-stop events. `input_json_delta` chunks carry partial arguments.
  中文翻译：**Anthropic。** 块开始 / 块增量 / 块停止事件。`input_json_delta` 块携带部分参数。
- **Gemini.** `streamFunctionCallArguments` (new in Gemini 3) emits chunks with a `functionCallId` so multiple parallel calls can interleave.
  中文翻译：**Gemini。** `streamFunctionCallArguments`（Gemini 3 新增）发出带有 `functionCallId` 的块，使多个并行调用可以交错。

Phase 13 · 03 goes deep on parallel + streaming reassembly. This lesson focuses on the declaration and single-call shapes.

> Phase 13 · 03 深入讲解并行和流式重组。本课侧重于声明和单调用格式。

### Errors and repair

> **【拓展：JSON Repair 的工业实践】** 生产环境中模型返回无效 JSON 是常见问题。开源库如 `json-repair`（GitHub 2k+ stars）专门处理这类问题。更现代的方案是使用结构化输出（structured output），通过约束解码在 token 生成阶段就保证格式正确，从根本上消除 JSON 解析失败的风险。

Invalid-argument errors look different too.

> 无效参数的错误表现也不同。

- **OpenAI (non-strict).** Model returns `arguments: "{bad json}"`, your JSON parse fails, you inject an error message and re-call.
  中文翻译：**OpenAI（非严格模式）。** 模型返回 `arguments: "{bad json}"`，你的 JSON 解析失败，你注入错误消息并重新调用。
- **OpenAI (strict).** Validation happens during decoding; invalid JSON is impossible but `refusal` can appear.
  中文翻译：**OpenAI（严格模式）。** 验证在解码期间进行；无效 JSON 不可能出现，但可能出现 `refusal`。
- **Anthropic.** `input` may contain unexpected fields; schema is advisory. Validate server-side.
  中文翻译：**Anthropic。** `input` 可能包含意外字段；模式是建议性的。在服务端验证。
- **Gemini.** OpenAPI 3.0 quirk: `enum` on object fields silently ignored; validate yourself.
  中文翻译：**Gemini。** OpenAPI 3.0 怪癖：对象字段上的 `enum` 会被静默忽略；自行验证。

### The translator pattern | 翻译器模式

> **【中文解读】** 翻译器模式：定义一个规范的 `Tool` 数据类，三个小函数分别翻译为三种供应商的声明格式。生产团队将其包装为 `AbstractToolset`（Pydantic AI）、`UniversalToolNode`（LangGraph）或 `BaseTool`（LlamaIndex）。Phase 13 Lesson 17 会构建一个网关，在前端暴露 OpenAI 格式 API，后端对接任意供应商。

A canonical tool declaration in your code looks like this (you pick the shape):

```python
Tool(
    name="get_weather",
    description="Use when ...",
    input_schema={"type": "object", "properties": {...}, "required": [...]},
    strict=True,
)
```

Three tiny functions translate it to the three provider shapes. The harness in `code/main.py` does exactly this, then round-trips a fake tool call through each provider's response shape. No network required — this lesson teaches the shapes, not the HTTP.

> 三个小函数将其翻译为三种供应商格式。`code/main.py` 中的线束正是这样做的，然后通过每个供应商的响应格式往返一次假的工具调用。不需要网络——本课讲解的是格式，不是 HTTP。

Production teams wrap this translator in `AbstractToolset` (Pydantic AI), `UniversalToolNode` (LangGraph), or `BaseTool` (LlamaIndex). Phase 13 · 17 ships a gateway that exposes an OpenAI-shaped API in front of any of the three.

> 生产团队将此翻译器包装为 `AbstractToolset`（Pydantic AI）、`UniversalToolNode`（LangGraph）或 `BaseTool`（LlamaIndex）。Phase 13 · 17 发布一个网关，在三个供应商中任何一个之前暴露 OpenAI 格式的 API。

## Use It | 用框架实现

`code/main.py` defines one canonical `Tool` dataclass and three translators that emit the OpenAI, Anthropic, and Gemini declaration JSON. It then parses a hand-crafted provider response of each shape into the same canonical call object, demonstrating that the semantics are identical under the skin. Run it and diff the three declarations side by side.

> `code/main.py` 定义了一个规范的 `Tool` 数据类和三个翻译器，分别输出 OpenAI、Anthropic 和 Gemini 的声明 JSON。然后它将每种格式手工制作的供应商响应解析为同一个规范调用对象，证明表层之下语义是相同的。运行它并并排比较三个声明。

What to look at:

> 需要关注的点：

- The three declaration blocks differ only in envelope and field names.
  中文翻译：三个声明块仅在信封和字段名上不同。
- The three response blocks differ in where the call lives (top-level `tool_calls`, `content[]` block, `parts[]` entry).
  中文翻译：三个响应块在调用所在位置上不同（顶层 `tool_calls`、`content[]` 块、`parts[]` 条目）。
- One `canonical_call()` function extracts `{id, name, args}` from all three response shapes.
  中文翻译：一个 `canonical_call()` 函数从所有三种响应格式中提取 `{id, name, args}`。

## Ship It | 产出物

This lesson produces `outputs/skill-provider-portability-audit.md`. Given a function-calling integration against one provider, the skill produces a portability audit: which provider limits it relies on, which fields need renaming, and what breaks when ported to each other provider.

> 本课产出 `outputs/skill-provider-portability-audit.md`。给定针对一个供应商的函数调用集成，该 skill 生成一个可移植性审计：依赖了哪些供应商限制、哪些字段需要重命名、以及移植到其他供应商时什么会出错。

## Exercises | 练习题

1. Run `code/main.py` and verify that the three provider declaration JSONs all serialize the same underlying `Tool` object. Modify the canonical tool to add an enum parameter and confirm only the Gemini translator needs to handle the OpenAPI quirk.
   运行代码，验证三个供应商声明 JSON 都序列化同一个 `Tool` 对象。添加 enum 参数，确认只有 Gemini 翻译器需处理 OpenAPI 怪癖。

2. Add a `ListToolsResponse` parser for each provider that extracts the tool list a model returns after a `list_tools` or discovery call. OpenAI does not have one natively; note this asymmetry.
   为每个供应商添加 `ListToolsResponse` 解析器。注意 OpenAI 原生不支持这一功能的非对称性。

3. Implement `tool_choice` conversion: map a canonical `ToolChoice(mode="force", tool_name="x")` into all three provider shapes. Then map `mode="any"` and `mode="none"`. Check the lesson's diff table.
   实现 `tool_choice` 转换：将规范的 `ToolChoice` 映射到三种供应商格式，覆盖 force/any/none 模式。

4. Pick one of the three providers and read its function-calling guide end to end. Find one field in its schema spec that the other two do not support. Candidates: OpenAI `strict`, Anthropic `disable_parallel_tool_use`, Gemini `function_calling_config.allowed_function_names`.
   选择一个供应商阅读其函数调用指南，找出一个其他两个不支持的字段。

5. Write a test vector: a tool call whose arguments violate the declared schema. Run it through each provider's validator (the stdlib one in Lesson 01 will do as a proxy) and record which errors fire. Document which provider you would use in production for strictness.
   编写违反 Schema 的测试向量，通过各供应商验证器运行，记录哪些错误触发。

## Key Terms | 关键术语

| Term | What people say | What it actually means |
|------|----------------|------------------------|
| 术语 | 通俗说法 | 实际含义 |
| Function calling | "Tool use" | Provider-level API for structured tool-call emission |
| 函数调用 | "工具使用" | 提供商级别的结构化工具调用输出 API |
| Tool declaration | "Tool spec" | Name + description + JSON Schema input payload |
| 工具声明 | "工具规格" | 名称 + 描述 + JSON Schema 输入负载 |
| `tool_choice` | "Force / forbid" | Auto / required / none / specific-name modes |
| `tool_choice` | "强制 / 禁止" | 自动 / 必需 / 无 / 指定名称模式 |
| Strict mode | "Schema enforcement" | OpenAI flag that constrains decoding to match schema |
| 严格模式 | "Schema 强制执行" | OpenAI 约束解码以匹配模式的标志 |
| `tool_use` block | "Anthropic's call shape" | Inline content block with id, name, input |
| `tool_use` 块 | "Anthropic 的调用格式" | 包含 id、name、input 的内联内容块 |
| `functionCall` part | "Gemini's call shape" | A `parts[]` entry containing name, args, and id |
| `functionCall` 部分 | "Gemini 的调用格式" | 包含 name、args 和 id 的 `parts[]` 条目 |
| Arguments-as-string | "Stringified JSON" | OpenAI returns args as a JSON string, not an object |
| 参数为字符串 | "字符串化 JSON" | OpenAI 以 JSON 字符串而非对象返回参数 |
| Parallel tool calls | "Fan-out in one turn" | Multiple tool calls in one assistant message |
| 并行工具调用 | "一回合扇出" | 一条 assistant 消息中的多个工具调用 |
| Refusal | "Model declines" | Strict-mode-only refusal block instead of a call |
| 拒绝 | "模型拒绝" | 仅严格模式下的拒绝块，替代调用 |
| OpenAPI 3.0 subset | "Gemini schema quirk" | Gemini uses a JSON-Schema-like dialect with minor differences |
| OpenAPI 3.0 子集 | "Gemini Schema 怪癖" | Gemini 使用类似 JSON Schema 的方言，存在细微差异 |

## Further Reading | 延伸阅读

- [OpenAI — Function calling guide](https://platform.openai.com/docs/guides/function-calling) — canonical reference including strict mode and parallel calls
  中文翻译：包含严格模式和并行调用的权威参考
- [Anthropic — Tool use overview](https://docs.anthropic.com/en/docs/agents-and-tools/tool-use/overview) — `tool_use` and `tool_result` block semantics
  中文翻译：`tool_use` 和 `tool_result` 块语义
- [Google — Gemini function calling](https://ai.google.dev/gemini-api/docs/function-calling) — parallel calls, unique ids, and OpenAPI subset
  中文翻译：并行调用、唯一 ID 和 OpenAPI 子集
- [Vertex AI — Function calling reference](https://docs.cloud.google.com/vertex-ai/generative-ai/docs/multimodal/function-calling) — Gemini's enterprise surface
  中文翻译：Gemini 的企业级接口
- [OpenAI — Structured outputs](https://platform.openai.com/docs/guides/structured-outputs) — strict-mode schema enforcement details
  中文翻译：严格模式 Schema 强制执行细节
