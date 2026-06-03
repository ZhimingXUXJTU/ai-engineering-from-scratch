# Function Calling Deep Dive — OpenAI, Anthropic, Gemini | 函数调用深入：三大供应商对比

> The three frontier providers converged on the same tool-call loop in 2024 and then diverged on everything else. OpenAI uses `tools` and `tool_calls`. Anthropic uses `tool_use` and `tool_result` blocks. Gemini uses `functionDeclarations` and unique-id correlation. This lesson diffs the three side by side so code that ships on one provider does not break when you port it.

> **【中文解读】** 三大前沿供应商在 2024 年收敛于相同的工具调用循环，但具体实现各有差异。OpenAI 用 `tools`/`tool_calls`，Anthropic 用 `tool_use`/`tool_result` 块，Gemini 用 `functionDeclarations` 和唯一 ID 关联。本课三路对比，让你在一个供应商上写的代码移植到另一个时不至于崩溃。

> **【拓展：Function Calling】** 函数调用（Function Calling）是 LLM 与外部世界交互的核心机制。LLM 不直接执行操作，而是输出结构化的"调用意图"（工具名+参数），由宿主程序执行后返回结果。三大供应商的 API 形状不同但语义等价：声明工具→模型选择调用→宿主执行→结果注入→模型继续推理。理解这一循环是构建跨平台 Agent 的基础。

**Type:** Build
**Languages:** Python (stdlib, schema translators)
**Prerequisites:** Phase 13 · 01 (the tool interface)
**Time:** ~75 minutes

## Learning Objectives | 学习目标

- State the three shape differences between OpenAI, Anthropic, and Gemini function-calling payloads (declaration, call, result).
  说明 OpenAI、Anthropic、Gemini 函数调用载荷的三种形态差异（声明、调用、结果）。
- Translate one tool declaration across all three provider formats and predict where strict-mode constraints will differ.
  将一个工具声明翻译为三种供应商格式，预测 strict 模式约束在哪会不同。
- Use `tool_choice` in each provider to force, forbid, or auto-pick tool calls.
  在每个供应商中使用 `tool_choice` 强制、禁止或自动选择工具调用。
- Know the per-provider hard limits (tool count, schema depth, argument length) and the error signatures each one emits when limits are violated.
  了解各供应商的硬限制（工具数量、Schema 深度、参数长度）及违反限制时的错误特征。

## The Problem | 问题定义

The shape of a function-calling request differs by provider. Three concrete examples from 2026 production stacks:

> **【中文解读】** 函数调用请求的格式因供应商而异。OpenAI 用 `tools`+`tool_calls`，响应中 `arguments` 是需要手动解析的 JSON 字符串；Anthropic 用 `tool_use`/`tool_result` 块，`input` 已经是解析好的对象；Gemini 用嵌套的 `functionDeclarations`，结果通过 `functionResponse` 返回。同一个循环，不同的字段名、嵌套方式、字符串 vs 对象约定和关联机制——从一个供应商移植到另一个仅"管道工程"就需要两三天。

**OpenAI Chat Completions / Responses API.** You pass `tools: [{type: "function", function: {name, description, parameters, strict}}]`. The model's response contains `choices[0].message.tool_calls: [{id, type: "function", function: {name, arguments}}]` where `arguments` is a JSON string you must parse. Strict mode (`strict: true`) enforces schema compliance via constrained decoding.

**Anthropic Messages API.** You pass `tools: [{name, description, input_schema}]`. The response comes back as `content: [{type: "text"}, {type: "tool_use", id, name, input}]`. `input` is already parsed (an object, not a string). You reply with a new `user` message containing a `{type: "tool_result", tool_use_id, content}` block.

**Google Gemini API.** You pass `tools: [{functionDeclarations: [{name, description, parameters}]}]` (nested under `functionDeclarations`). The response arrives as `candidates[0].content.parts: [{functionCall: {name, args, id}}]` where `id` is unique in Gemini 3 and up for parallel-call correlation. You reply with `{functionResponse: {name, id, response}}`.

Same loop. Different field names, different nesting, different string-vs-object conventions, different correlation mechanisms. A team that writes a weather agent on OpenAI pays a two-day port to Anthropic and another day to Gemini just for the plumbing.

This lesson builds a translator that unifies the three formats into one canonical tool declaration and routes at the edge. Phase 13 · 17 generalizes the same pattern into an LLM gateway.

## The Concept | 核心概念

### The common structure | 通用结构

Every provider needs five things:

1. **Tool list.** Per-tool name, description, and input schema.
2. **Tool choice.** Force a specific tool, forbid tools, or let the model decide.
3. **Call emission.** Structured output naming the tool and arguments.
4. **Call id.** Correlate the response to the right call (matters for parallel).
5. **Result injection.** A message or block that ties the result back to the call.

> **【中文解读】** 每个供应商都需要五样东西：工具列表（名称+描述+输入 Schema）、工具选择（强制/禁止/自动）、调用输出（结构化的工具名和参数）、调用 ID（关联响应到正确的调用，并行时关键）、结果注入（将结果绑回调用的消息或块）。

### Shape diffs, field by field

| Aspect | OpenAI | Anthropic | Gemini |
|--------|--------|-----------|--------|
| Declaration envelope | `{type: "function", function: {...}}` | `{name, description, input_schema}` | `{functionDeclarations: [{...}]}` |
| Schema field | `parameters` | `input_schema` | `parameters` |
| Response container | `tool_calls[]` on assistant message | `content[]` of type `tool_use` | `parts[]` of type `functionCall` |
| Arguments type | stringified JSON | parsed object | parsed object |
| Id format | `call_...` (OpenAI generates) | `toolu_...` (Anthropic) | UUID (Gemini 3+) |
| Result block | role `tool`, `tool_call_id` | `user` with `tool_result`, `tool_use_id` | `functionResponse` with matching `id` |
| Force-a-tool | `tool_choice: {type: "function", function: {name}}` | `tool_choice: {type: "tool", name}` | `tool_config: {function_calling_config: {mode: "ANY"}}` |
| Forbid tools | `tool_choice: "none"` | `tool_choice: {type: "none"}` | `mode: "NONE"` |
| Strict schema | `strict: true` | schema-is-schema (always enforced) | `responseSchema` at request level |

### Limits you will actually hit | 实际会遇到的限制

> **【中文解读】** OpenAI：128 个工具/请求，Schema 深度 5，参数字符串 ≤8192 字节，strict 模式不支持 `$ref`/`oneOf` 等重叠组合。Anthropic：64 个工具/请求，Schema 深度无硬限制但实际约 10，无 strict 模式标志但模型倾向于遵守。Gemini：64 个函数/请求，使用 OpenAPI 3.0 子集（与 JSON Schema 2020-12 有细微差异），Gemini 3 起支持唯一 ID。

- **OpenAI.** 128 tools per request. Schema depth 5. Argument string <= 8192 bytes. Strict mode requires no `$ref`, no `oneOf`/`anyOf`/`allOf` with overlap, every property listed in `required`.
- **Anthropic.** 64 tools per request. Schema depth effectively unbounded but practical limit 10. No strict-mode flag; schema is a contract and the model tends to comply.
- **Gemini.** 64 functions per request. Schema types are OpenAPI 3.0 subset (slight divergence from JSON Schema 2020-12). Parallel calls unique-id since Gemini 3.

### `tool_choice` behavior

Three modes everyone supports, named differently.

- **Auto.** Model picks tool or text. Default.
- **Required / Any.** Model must call at least one tool.
- **None.** Model must not call tools.

Plus one mode unique to each provider:

- **OpenAI.** Force a specific tool by name.
- **Anthropic.** Force a specific tool by name; `disable_parallel_tool_use` flag separates single vs multi.
- **Gemini.** `mode: "VALIDATED"` routes every response through a schema validator regardless of model intent.

### Parallel calls

OpenAI's `parallel_tool_calls: true` (default) emits multiple calls in one assistant message. You run them all and reply with a batched tool-role message containing one entry per `tool_call_id`. Anthropic historically did single-call; `disable_parallel_tool_use: false` (default as of Claude 3.5) enables multi. Gemini 2 allowed parallel calls but did not give stable ids; Gemini 3 adds UUIDs so out-of-order responses correlate cleanly.

### Streaming

All three support streamed tool calls. The wire format differs:

- **OpenAI.** Delta chunks of `tool_calls[i].function.arguments` arrive incrementally. You accumulate until `finish_reason: "tool_calls"`.
- **Anthropic.** Block-start / block-delta / block-stop events. `input_json_delta` chunks carry partial arguments.
- **Gemini.** `streamFunctionCallArguments` (new in Gemini 3) emits chunks with a `functionCallId` so multiple parallel calls can interleave.

Phase 13 · 03 goes deep on parallel + streaming reassembly. This lesson focuses on the declaration and single-call shapes.

### Errors and repair

Invalid-argument errors look different too.

- **OpenAI (non-strict).** Model returns `arguments: "{bad json}"`, your JSON parse fails, you inject an error message and re-call.
- **OpenAI (strict).** Validation happens during decoding; invalid JSON is impossible but `refusal` can appear.
- **Anthropic.** `input` may contain unexpected fields; schema is advisory. Validate server-side.
- **Gemini.** OpenAPI 3.0 quirk: `enum` on object fields silently ignored; validate yourself.

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

Production teams wrap this translator in `AbstractToolset` (Pydantic AI), `UniversalToolNode` (LangGraph), or `BaseTool` (LlamaIndex). Phase 13 · 17 ships a gateway that exposes an OpenAI-shaped API in front of any of the three.

## Use It

`code/main.py` defines one canonical `Tool` dataclass and three translators that emit the OpenAI, Anthropic, and Gemini declaration JSON. It then parses a hand-crafted provider response of each shape into the same canonical call object, demonstrating that the semantics are identical under the skin. Run it and diff the three declarations side by side.

What to look at:

- The three declaration blocks differ only in envelope and field names.
- The three response blocks differ in where the call lives (top-level `tool_calls`, `content[]` block, `parts[]` entry).
- One `canonical_call()` function extracts `{id, name, args}` from all three response shapes.

## Ship It

This lesson produces `outputs/skill-provider-portability-audit.md`. Given a function-calling integration against one provider, the skill produces a portability audit: which provider limits it relies on, which fields need renaming, and what breaks when ported to each other provider.

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
| Function calling | "Tool use" | Provider-level API for structured tool-call emission |
| Tool declaration | "Tool spec" | Name + description + JSON Schema input payload |
| `tool_choice` | "Force / forbid" | Auto / required / none / specific-name modes |
| Strict mode | "Schema enforcement" | OpenAI flag that constrains decoding to match schema |
| `tool_use` block | "Anthropic's call shape" | Inline content block with id, name, input |
| `functionCall` part | "Gemini's call shape" | A `parts[]` entry containing name, args, and id |
| Arguments-as-string | "Stringified JSON" | OpenAI returns args as a JSON string, not an object |
| Parallel tool calls | "Fan-out in one turn" | Multiple tool calls in one assistant message |
| Refusal | "Model declines" | Strict-mode-only refusal block instead of a call |
| OpenAPI 3.0 subset | "Gemini schema quirk" | Gemini uses a JSON-Schema-like dialect with minor differences |

## Further Reading

- [OpenAI — Function calling guide](https://platform.openai.com/docs/guides/function-calling) — canonical reference including strict mode and parallel calls
- [Anthropic — Tool use overview](https://docs.anthropic.com/en/docs/agents-and-tools/tool-use/overview) — `tool_use` and `tool_result` block semantics
- [Google — Gemini function calling](https://ai.google.dev/gemini-api/docs/function-calling) — parallel calls, unique ids, and OpenAPI subset
- [Vertex AI — Function calling reference](https://docs.cloud.google.com/vertex-ai/generative-ai/docs/multimodal/function-calling) — Gemini's enterprise surface
- [OpenAI — Structured outputs](https://platform.openai.com/docs/guides/structured-outputs) — strict-mode schema enforcement details
