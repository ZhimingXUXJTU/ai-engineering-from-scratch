# Structured Output — JSON Schema, Pydantic, Zod, Constrained Decoding | 结构化输出：JSON Schema、Pydantic、Zod 与约束解码

> "Ask the model nicely to return JSON" fails 5 to 15 percent of the time, even on frontier models. Structured outputs close that gap with constrained decoding: the model is literally prevented from emitting a token that would violate the schema. OpenAI's strict mode, Anthropic's schema-typed tool use, Gemini's `responseSchema`, Pydantic AI's `output_type`, and Zod's `.parse` are five surface forms of the same idea. This lesson builds the schema validator and the strict-mode contract learners will use for every production extraction pipeline.

> **【中文解读】** "礼貌地让模型返回 JSON"在前沿模型上仍有 5-15% 的失败率。结构化输出通过约束解码弥合这一差距：模型在 token 级别被阻止发出违反 Schema 的内容。OpenAI strict mode、Anthropic schema-typed tool use、Gemini `responseSchema`、Pydantic AI `output_type` 和 Zod `.parse` 是同一思想的五种表面形式。

> **【拓展：结构化输出→Function Calling 的质量保障】** 结构化输出是所有数据提取管道的基础。在 Function Calling 场景中，结构化输出确保工具参数的 JSON 格式始终有效。OpenAI 的 strict mode 通过 constrained decoding 在解码时屏蔽违反 Schema 的 token，Anthropic 通过 `input_schema` 在 tool_use 中实现类似保证。这消除了"模型返回无效 JSON"这一最常见的生产故障模式。

**Type:** Build
**Languages:** Python (stdlib, JSON Schema 2020-12 subset)
**Prerequisites:** Phase 13 · 02 (function calling deep dive)
**Time:** ~75 minutes

## Learning Objectives

- Write a JSON Schema 2020-12 for an extraction target using the right constraints (enum, min/max, required, pattern).
- Explain why strict mode and constrained decoding give different guarantees from "validate after generation".
- Distinguish the three failure modes: parse error, schema violation, model refusal.
- Ship an extraction pipeline with typed repair and typed refusal handling.

## The Problem | 问题引入

An agent reading a purchase-order email needs to turn free text into `{customer, line_items, total_usd}`. Three approaches.

**Approach one: prompt for JSON.** "Reply in JSON with fields customer, line_items, total_usd." Works 85 to 95 percent of the time on frontier models. Fails in six ways: missing brace, trailing comma, wrong types, hallucinated fields, truncated at token limit, leaked prose like "Here is your JSON:".

**Approach two: validate after generation.** Generate freely, parse, validate against schema, retry on failure. Reliable but expensive — you pay for every retry, and truncation bugs cost one extra turn per occurrence.

**Approach three: constrained decoding.** The provider enforces the schema at decode time. Invalid tokens are masked out of the sampling distribution. The output is guaranteed to parse and guaranteed to validate. Failure collapses to one mode: refusal (the model decides the input does not fit the schema).

> **【中文解读】** 第三种方法——约束解码——在解码时强制执行 Schema。无效 token 被从采样分布中屏蔽。输出保证可解析且可验证。失败只归结为一种模式：拒绝（模型认为输入不符合 Schema）。

Every 2026 frontier provider ships some form of approach three.

- **OpenAI.** `response_format: {type: "json_schema", strict: true}` plus `refusal` in the response if the model declines.
- **Anthropic.** Schema enforcement on `tool_use` inputs; `stop_reason: "refusal"` is not a thing, but `end_turn` with no tool call is the signal.
- **Gemini.** `responseSchema` at request level; in 2026 Gemini ships token-level grammar constraints for selected types.
- **Pydantic AI.** `output_type=InvoiceModel` emits a structured `RunResult` typed to `InvoiceModel`.
- **Zod (TypeScript).** Runtime parser that validates provider output against a Zod schema; pairs with OpenAI's `beta.chat.completions.parse`.

The common thread: declare the schema once, enforce it end to end.

## The Concept | 核心概念

### JSON Schema 2020-12 — the lingua franca

> **【中文解读】** JSON Schema 2020-12 是所有供应商共同接受的 Schema 语言。最常用的构造包括：`type`（类型）、`properties`（字段映射）、`required`（必填字段）、`enum`（枚举值）、`minimum`/`maximum`（数值范围）、`pattern`（正则约束）等。OpenAI strict mode 额外要求所有属性必须在 `required` 中列出、所有层级 `additionalProperties: false`、不得使用未解析的 `$ref`。

Every provider accepts JSON Schema 2020-12. The constructs you use most:

- `type`: one of `object`, `array`, `string`, `number`, `integer`, `boolean`, `null`.
- `properties`: map of field name to subschema.
- `required`: list of field names that must appear.
- `enum`: closed set of allowed values.
- `minimum` / `maximum` (numbers), `minLength` / `maxLength` / `pattern` (strings).
- `items`: subschema applied to every array element.
- `additionalProperties`: `false` forbids extra fields (default varies by mode).

OpenAI strict mode adds three requirements: every property must be listed in `required`, `additionalProperties: false` everywhere, and no unresolved `$ref`. If you break these, the API returns 400 at request time.

### Pydantic, the Python binding

> **【拓展：Pydantic AI 在结构化输出中的地位】** Pydantic AI 是 2024-2025 年兴起的 Python Agent 框架，其核心竞争力就是利用 Pydantic v2 的 `model_json_schema()` 自动生成供应商兼容的 Schema。开发者只需定义一个 `BaseModel` 类，框架自动处理 strict mode 兼容性、类型验证和拒绝处理。据统计，Pydantic AI 在 2025 年 GitHub 增长最快的 AI 框架中排名前三。

Pydantic v2 generates JSON Schema from dataclass-shaped models via `model_json_schema()`. Pydantic AI wraps this so you write:

```python
class Invoice(BaseModel):
    customer: str
    line_items: list[LineItem]
    total_usd: Decimal
```

and the agent framework translates the schema into OpenAI strict mode, Anthropic `input_schema`, or Gemini `responseSchema` at the edge. The model's output comes back as a typed `Invoice` instance. Validation errors raise `ValidationError` with typed error paths.

### Zod, the TypeScript binding

Zod (`z.object({customer: z.string(), ...})`) is the TS equivalent. OpenAI's Node SDK exposes `zodResponseFormat(Invoice)` which translates to the API's JSON Schema payload.

### Refusals

Strict mode cannot force the model to answer. If the input cannot fit the schema ("the email was a poem, not an invoice"), the model emits a `refusal` field containing the reason. Your code must handle this as a first-class outcome, not a failure. The refusal is also useful as a safety signal: a model asked to extract a credit card number from a protected-content email returns a refusal with the safety reason attached.

> **【中文解读】** Strict mode 不能强制模型回答。如果输入无法适配 Schema（如"邮件是诗歌而非发票"），模型会发出 `refusal` 字段。拒绝不是失败，而是一等公民类型的返回结果。拒绝也可用作安全信号：当模型被要求从受保护内容中提取信用卡号时，会返回附有安全原因的拒绝。

### Constrained decoding in the open

> **【拓展：开源约束解码工具对比】** 主要开源工具包括：(1) `outlines`（GitHub 10k+ stars）基于有限状态自动机构建 token 掩码；(2) `guidance`（微软出品）用模板语言控制生成；(3) `lm-format-enforcer` 通过流式 JSON 解析器计算有效下一 token 集合。2026年的最新进展是这些工具的速度已接近无约束生成，短结构化输出场景甚至更快（因为减少了采样空间）。

Open-weights implementations use three techniques.

1. **Grammar-based decoding** (`outlines`, `guidance`, `lm-format-enforcer`): build a deterministic finite automaton from the schema; at every step, mask the logits of tokens that would violate the FSM.
2. **Logit masking with a JSON parser**: run a streaming JSON parser in lockstep with the model; at every step, compute the valid-next-token set.
3. **Speculative decoding with a verifier**: cheap draft model proposes tokens, verifier enforces the schema.

Commercial providers pick one of these behind the scenes. The 2026 state of the art is faster than plain generation for short structured outputs and roughly the same speed for long ones.

### The three failure modes

1. **Parse error.** The output is not valid JSON. Cannot happen under strict mode. Can still happen on non-strict providers.
2. **Schema violation.** The output parses but violates the schema. Cannot happen under strict mode. Common outside it.
3. **Refusal.** The model declines. Must be handled as a typed outcome.

### Retry strategy

> **【中文解读】** 非 strict mode 下的恢复模式是"生成→解析→验证→失败则注入错误重试，最多 3 次"。通常一次重试就够了，三次覆盖弱模型的偶然失败。超过三次说明 Schema 设计有问题，需要修改 prompt 或 Schema。

When you are outside strict mode (Anthropic tool use, non-strict OpenAI, older Gemini), the recovery pattern is:

```
generate -> parse -> validate -> if fail, inject error and retry, max 3x
```

One retry is usually enough. Three retries catches weak-model flakes. Beyond three is a sign of a bad schema: the model cannot satisfy it for some inputs, and the prompt or the schema needs fixing.

### Small-model support

Constrained decoding works on small models. A 3B-parameter open model with grammar enforcement out-performs a 70B-parameter model with raw prompting on structured tasks. This is the main reason structured outputs matter for production: it decouples reliability from model size.

> **【中文解读】** 约束解码也适用于小模型。一个 3B 参数的开源模型配合语法强制，在结构化任务上可超越 70B 参数模型的纯提示方法。这是结构化输出在生产中重要的主因：它解耦了可靠性与模型大小。

## Use It | 用框架实现

`code/main.py` ships a minimal JSON Schema 2020-12 validator in stdlib (types, required, enum, min/max, pattern, items, additionalProperties). It wraps an `Invoice` schema and runs a fake LLM output through the validator, demonstrating parse error, schema violation, and refusal paths. Swap the fake output for any provider's real response in production.

What to look at:

- The validator returns a typed `[ValidationError]` list with path and message. That is the shape you want surfaced to the retry prompt.
- The refusal branch does NOT retry. It logs and returns a typed refusal. Phase 14 · 09 uses refusals as a safety signal.
- The `additionalProperties: false` check fires on the adversarial test input, showing why strict mode shuts the door on hallucinated fields.

## Ship It | 产出物

This lesson produces `outputs/skill-structured-output-designer.md`. Given a free-text extraction target (invoices, support tickets, resumes, etc.), the skill produces a JSON Schema 2020-12 that is strict-mode-compatible and a Pydantic model that mirrors it, with typed refusal and retry handling stubbed in.

## Exercises | 练习题

1. Run `code/main.py`. Add a fourth test case whose `total_usd` is a negative number. Confirm the validator rejects it with the `minimum` constraint path.

2. Extend the validator to support `oneOf` with a discriminator. The common case: `line_item` is either a product or a service, tagged by `kind`. Strict mode has subtle rules here; check OpenAI's structured outputs guide.

3. Write the same Invoice schema as a Pydantic BaseModel and compare `model_json_schema()` output to your hand-rolled schema. Identify the one field Pydantic sets by default that the hand-rolled version omits.

4. Measure refusal rates. Construct ten inputs that should not be extractable (a song lyric, a math proof, a blank email) and run them through a real provider with strict mode. Count refusals vs hallucinated outputs. This is your ground truth for refusal-aware retries.

5. Read OpenAI's structured outputs guide top to bottom. Identify the one construct it explicitly forbids in strict mode that plain JSON Schema allows. Then design a schema that uses the forbidden construct non-essentially and refactor it to be strict-compatible.

## Key Terms | 术语速查表

| Term | What people say | What it actually means | 中文术语 |
|------|----------------|------------------------|----------|
| JSON Schema 2020-12 | "The schema spec" | IETF-draft schema dialect every modern provider speaks | JSON Schema 2020-12 规范 |
| Strict mode | "Guaranteed schema" | OpenAI flag that enforces schema via constrained decoding | 严格模式 |
| Constrained decoding | "Logit masking" | Decode-time enforcement that masks invalid next-tokens | 约束解码 |
| Refusal | "Model declines" | Typed outcome when input cannot fit the schema | 模型拒绝 |
| Parse error | "Invalid JSON" | Output did not parse as JSON; impossible under strict | 解析错误 |
| Schema violation | "Wrong shape" | Parsed but violated types / required / enum / range | Schema 违规 |
| `additionalProperties: false` | "No extras allowed" | Forbids unknown fields; required in OpenAI strict | 禁止额外属性 |
| Pydantic BaseModel | "Typed output" | Python class that emits and validates JSON Schema | Pydantic 基础模型 |
| Zod schema | "TypeScript output type" | TS runtime schema for provider output validation | Zod 类型定义 |
| Grammar enforcement | "Open-weights constrained decode" | FSM-based logit masking, as in outlines / guidance | 语法强制 |

## Further Reading | 延伸阅读

- [OpenAI — Structured outputs](https://platform.openai.com/docs/guides/structured-outputs) — strict mode, refusals, and schema requirements
- [OpenAI — Introducing structured outputs](https://openai.com/index/introducing-structured-outputs-in-the-api/) — August 2024 launch post explaining the decoding guarantee
- [Pydantic AI — Output](https://ai.pydantic.dev/output/) — typed output_type bindings that serialize to each provider
- [JSON Schema — 2020-12 release notes](https://json-schema.org/draft/2020-12/release-notes) — the canonical spec
- [Microsoft — Structured outputs in Azure OpenAI](https://learn.microsoft.com/en-us/azure/foundry/openai/how-to/structured-outputs) — enterprise deployment notes and strict-mode caveats
