# Structured Output — JSON Schema, Pydantic, Zod, Constrained Decoding | 结构化输出：JSON Schema、Pydantic、Zod 与约束解码

> "Ask the model nicely to return JSON" fails 5 to 15 percent of the time, even on frontier models. Structured outputs close that gap with constrained decoding: the model is literally prevented from emitting a token that would violate the schema. OpenAI's strict mode, Anthropic's schema-typed tool use, Gemini's `responseSchema`, Pydantic AI's `output_type`, and Zod's `.parse` are five surface forms of the same idea. This lesson builds the schema validator and the strict-mode contract learners will use for every production extraction pipeline.

> **【中文解读】** "礼貌地让模型返回 JSON"在前沿模型上仍有 5-15% 的失败率。结构化输出通过约束解码弥合这一差距：模型在 token 级别被阻止发出违反 Schema 的内容。OpenAI strict mode、Anthropic schema-typed tool use、Gemini `responseSchema`、Pydantic AI `output_type` 和 Zod `.parse` 是同一思想的五种表面形式。

> **【拓展：结构化输出→Function Calling 的质量保障】** 结构化输出是所有数据提取管道的基础。在 Function Calling 场景中，结构化输出确保工具参数的 JSON 格式始终有效。OpenAI 的 strict mode 通过 constrained decoding 在解码时屏蔽违反 Schema 的 token，Anthropic 通过 `input_schema` 在 tool_use 中实现类似保证。这消除了"模型返回无效 JSON"这一最常见的生产故障模式。

> 🔗 **【前置】** 学本节前请先掌握：(1) Phase 11·03（Structured Outputs）——基础；(2) Phase 13·01（The Tool Interface）和 13·02（Function Calling Deep Dive）——理解 strict mode 出现前的"prompt for JSON"失败模式；(3) Pydantic v2 或 Zod 基础语法，本节会用它们生成 Schema。

**Type:** Build | **类型:** 构建
**Languages:** Python (stdlib, JSON Schema 2020-12 subset) | **语言:** Python（标准库，JSON Schema 2020-12 子集）
**Prerequisites:** Phase 13 · 02 (function calling deep dive) | **前置知识:** Phase 13 · 02（函数调用深入）
**Time:** ~75 minutes | **时间:** ~75 分钟

## Learning Objectives | 学习目标

- Write a JSON Schema 2020-12 for an extraction target using the right constraints (enum, min/max, required, pattern).
  中文翻译：使用正确的约束（enum、min/max、required、pattern）为提取目标编写 JSON Schema 2020-12。
- Explain why strict mode and constrained decoding give different guarantees from "validate after generation".
  中文翻译：解释为什么 strict mode 和约束解码提供与"生成后验证"不同的保证。
- Distinguish the three failure modes: parse error, schema violation, model refusal.
  中文翻译：区分三种失败模式：解析错误、Schema 违规、模型拒绝。
- Ship an extraction pipeline with typed repair and typed refusal handling.
  中文翻译：交付一个带有类型化修复和类型化拒绝处理的提取管道。

## The Problem | 问题引入

An agent reading a purchase-order email needs to turn free text into `{customer, line_items, total_usd}`. Three approaches.

> 一个读取采购订单邮件的 agent 需要将自由文本转换为 `{customer, line_items, total_usd}`。三种方法。

**Approach one: prompt for JSON.** "Reply in JSON with fields customer, line_items, total_usd." Works 85 to 95 percent of the time on frontier models. Fails in six ways: missing brace, trailing comma, wrong types, hallucinated fields, truncated at token limit, leaked prose like "Here is your JSON:".

> **方法一：提示要求 JSON。** "以 JSON 格式回复，包含字段 customer、line_items、total_usd。"在前沿模型上 85-95% 的时间有效。六种失败方式：缺少大括号、尾随逗号、类型错误、幻觉字段、token 限制处截断、泄露散文如"这是你的 JSON："。

**Approach two: validate after generation.** Generate freely, parse, validate against schema, retry on failure. Reliable but expensive — you pay for every retry, and truncation bugs cost one extra turn per occurrence.

> **方法二：生成后验证。** 自由生成、解析、按 Schema 验证、失败时重试。可靠但昂贵——每次重试都要付费，截断 bug 每次发生还多花一轮。

**Approach three: constrained decoding.** The provider enforces the schema at decode time. Invalid tokens are masked out of the sampling distribution. The output is guaranteed to parse and guarantee to validate. Failure collapses to one mode: refusal (the model decides the input does not fit the schema).

> **方法三：约束解码。** 提供商在解码时强制执行 Schema。无效 token 从采样分布中被屏蔽。输出保证可解析且可验证。失败归结为一种模式：拒绝（模型判定输入不适合 Schema）。

> 💡 **【类比】** 约束解码像填空题的"格子"约束。普通生成是写作文，想写啥写啥，可能跑题（无效 JSON）。约束解码是给你一张表格，每个格子已经标好"姓名/年龄/邮箱"，模型只能在格子里填对应类型的内容，不会出现"年龄"那栏填了"小明"。技术实现：在每个 token 采样时，预先屏蔽掉所有会导致 Schema 违规的 token，让概率为零。

> **【中文解读】** 第三种方法——约束解码——在解码时强制执行 Schema。无效 token 被从采样分布中屏蔽。输出保证可解析且可验证。失败只归结为一种模式：拒绝（模型认为输入不符合 Schema）。

Every 2026 frontier provider ships some form of approach three.

> 2026 年的每个前沿提供商都发布了某种形式的方法三。

- **OpenAI.** `response_format: {type: "json_schema", strict: true}` plus `refusal` in the response if the model declines.
  中文翻译：**OpenAI。** `response_format: {type: "json_schema", strict: true}`，如果模型拒绝则在响应中加上 `refusal`。
- **Anthropic.** Schema enforcement on `tool_use` inputs; `stop_reason: "refusal"` is not a thing, but `end_turn` with no tool call is the signal.
  中文翻译：**Anthropic。** 在 `tool_use` 输入上强制执行 Schema；`stop_reason: "refusal"` 不存在，但无工具调用的 `end_turn` 是信号。
- **Gemini.** `responseSchema` at request level; in 2026 Gemini ships token-level grammar constraints for selected types.
  中文翻译：**Gemini。** 请求级别的 `responseSchema`；2026 年 Gemini 为选定类型提供了 token 级语法约束。
- **Pydantic AI.** `output_type=InvoiceModel` emits a structured `RunResult` typed to `InvoiceModel`.
  中文翻译：**Pydantic AI。** `output_type=InvoiceModel` 发出类型化为 `InvoiceModel` 的结构化 `RunResult`。
- **Zod (TypeScript).** Runtime parser that validates provider output against a Zod schema; pairs with OpenAI's `beta.chat.completions.parse`.
  中文翻译：**Zod (TypeScript)。** 根据 Zod Schema 验证提供商输出的运行时解析器；与 OpenAI 的 `beta.chat.completions.parse` 配合使用。

The common thread: declare the schema once, enforce it end to end.

> 共同主线：声明 Schema 一次，端到端强制执行。

## The Concept | 核心概念

### JSON Schema 2020-12 — the lingua franca

> **【中文解读】** JSON Schema 2020-12 是所有供应商共同接受的 Schema 语言。最常用的构造包括：`type`（类型）、`properties`（字段映射）、`required`（必填字段）、`enum`（枚举值）、`minimum`/`maximum`（数值范围）、`pattern`（正则约束）等。OpenAI strict mode 额外要求所有属性必须在 `required` 中列出、所有层级 `additionalProperties: false`、不得使用未解析的 `$ref`。

Every provider accepts JSON Schema 2020-12. The constructs you use most:

> 每个提供商都接受 JSON Schema 2020-12。你使用最多的构造：

- `type`: one of `object`, `array`, `string`, `number`, `integer`, `boolean`, `null`.
  中文翻译：`type`：`object`、`array`、`string`、`number`、`integer`、`boolean`、`null` 之一。
- `properties`: map of field name to subschema.
  中文翻译：`properties`：字段名到子 Schema 的映射。
- `required`: list of field names that must appear.
  中文翻译：`required`：必须出现的字段名列表。
- `enum`: closed set of allowed values.
  中文翻译：`enum`：允许值的封闭集合。
- `minimum` / `maximum` (numbers), `minLength` / `maxLength` / `pattern` (strings).
  中文翻译：`minimum` / `maximum`（数值）、`minLength` / `maxLength` / `pattern`（字符串）。
- `items`: subschema applied to every array element.
  中文翻译：`items`：应用于每个数组元素的子 Schema。
- `additionalProperties`: `false` forbids extra fields (default varies by mode).
  中文翻译：`additionalProperties`：`false` 禁止额外字段（默认值因模式而异）。

OpenAI strict mode adds three requirements: every property must be listed in `required`, `additionalProperties: false` everywhere, and no unresolved `$ref`. If you break these, the API returns 400 at request time.

> OpenAI strict mode 增加了三个要求：每个属性都必须列在 `required` 中、所有层级 `additionalProperties: false`、不得使用未解析的 `$ref`。如果违反这些要求，API 会在请求时返回 400。

> ⚠️ **【易错点】** 场景：OpenAI strict mode 下用 Pydantic 的 `Optional[int] = None` / 后果：API 返回 400 报"additionalProperties or required"错误，因为 strict mode 要求**所有**字段在 `required`，即使可选 / 修复：用 `Union[int, None]` 并显式 `required=[..., "field_name"]`；或者 Pydantic AI 框架会自动处理这个转换；最佳实践是定义所有字段都必填，缺省值用空字符串/null 而非"省略"。

### Pydantic, the Python binding

> **【拓展：Pydantic AI 在结构化输出中的地位】** Pydantic AI 是 2024-2025 年兴起的 Python Agent 框架，其核心竞争力就是利用 Pydantic v2 的 `model_json_schema()` 自动生成供应商兼容的 Schema。开发者只需定义一个 `BaseModel` 类，框架自动处理 strict mode 兼容性、类型验证和拒绝处理。据统计，Pydantic AI 在 2025 年 GitHub 增长最快的 AI 框架中排名前三。

Pydantic v2 generates JSON Schema from dataclass-shaped models via `model_json_schema()`. Pydantic AI wraps this so you write:

> Pydantic v2 通过 `model_json_schema()` 从数据类形式的模型生成 JSON Schema。Pydantic AI 封装了这一点，你只需写：

```python
class Invoice(BaseModel):
    customer: str
    line_items: list[LineItem]
    total_usd: Decimal
```

and the agent framework translates the schema into OpenAI strict mode, Anthropic `input_schema`, or Gemini `responseSchema` at the edge. The model's output comes back as a typed `Invoice` instance. Validation errors raise `ValidationError` with typed error paths.

> 然后 agent 框架在边缘将 Schema 翻译为 OpenAI strict mode、Anthropic `input_schema` 或 Gemini `responseSchema`。模型的输出以类型化的 `Invoice` 实例返回。验证错误会引发带有类型化错误路径的 `ValidationError`。

### Zod, the TypeScript binding

Zod (`z.object({customer: z.string(), ...})`) is the TS equivalent. OpenAI's Node SDK exposes `zodResponseFormat(Invoice)` which translates to the API's JSON Schema payload.

> Zod (`z.object({customer: z.string(), ...})`) 是 TypeScript 的等价方案。OpenAI 的 Node SDK 暴露了 `zodResponseFormat(Invoice)`，将其翻译为 API 的 JSON Schema 负载。

### Refusals

Strict mode cannot force the model to answer. If the input cannot fit the schema ("the email was a poem, not an invoice"), the model emits a `refusal` field containing the reason. Your code must handle this as a first-class outcome, not a failure. The refusal is also useful as a safety signal: a model asked to extract a credit card number from a protected-content email returns a refusal with the safety reason attached.

> 🤔 **【困惑】** Q: refusal 算"成功"还是"失败"？返回什么 HTTP 状态码？ A: 算**业务成功**，HTTP 200。因为模型按 schema 约定给出了正确的"无法处理"信号（不是技术错误）。代码上把它当成 `Result<T, Refusal>` 处理：要么走"拒绝分支"（如记录到日志、回退到人工审核），要么再次提示用户。把 refusal 当 500 错误是新手最常见误判，会导致监控告警噪音。


> Strict mode 不能强制模型回答。如果输入无法适配 Schema（"邮件是诗歌而非发票"），模型会发出包含原因的 `refusal` 字段。你的代码必须将其作为一等公民结果处理，而非失败。拒绝也可用作安全信号：当模型被要求从受保护内容邮件中提取信用卡号时，会返回附带安全原因的拒绝。

> **【中文解读】** Strict mode 不能强制模型回答。如果输入无法适配 Schema（如"邮件是诗歌而非发票"），模型会发出 `refusal` 字段。拒绝不是失败，而是一等公民类型的返回结果。拒绝也可用作安全信号：当模型被要求从受保护内容中提取信用卡号时，会返回附有安全原因的拒绝。

### Constrained decoding in the open

> **【拓展：开源约束解码工具对比】** 主要开源工具包括：(1) `outlines`（GitHub 10k+ stars）基于有限状态自动机构建 token 掩码；(2) `guidance`（微软出品）用模板语言控制生成；(3) `lm-format-enforcer` 通过流式 JSON 解析器计算有效下一 token 集合。2026年的最新进展是这些工具的速度已接近无约束生成，短结构化输出场景甚至更快（因为减少了采样空间）。

Open-weights implementations use three techniques.

> 开源权重实现使用三种技术。

1. **Grammar-based decoding** (`outlines`, `guidance`, `lm-format-enforcer`): build a deterministic finite automaton from the schema; at every step, mask the logits of tokens that would violate the FSM.
   中文翻译：**基于语法的解码**（`outlines`、`guidance`、`lm-format-enforcer`）：从 Schema 构建确定性有限自动机；每一步屏蔽会违反 FSM 的 token 的 logits。
2. **Logit masking with a JSON parser**: run a streaming JSON parser in lockstep with the model; at every step, compute the valid-next-token set.
   中文翻译：**带 JSON 解析器的 Logit 屏蔽**：与模型同步运行流式 JSON 解析器；每一步计算有效的下一 token 集合。
3. **Speculative decoding with a verifier**: cheap draft model proposes tokens, verifier enforces the schema.
   中文翻译：**带验证器的推测解码**：廉价的草稿模型提出 token，验证器强制执行 Schema。

Commercial providers pick one of these behind the scenes. The 2026 state of the art is faster than plain generation for short structured outputs and roughly the same speed for long ones.

> 商业提供商在幕后选择其中一种。2026 年的最先进技术对于短结构化输出比普通生成更快，对于长输出大致相同。

### The three failure modes

1. **Parse error.** The output is not valid JSON. Cannot happen under strict mode. Can still happen on non-strict providers.
   中文翻译：**解析错误。** 输出不是有效 JSON。strict mode 下不可能发生。非 strict 提供商上仍可能发生。
2. **Schema violation.** The output parses but violates the schema. Cannot happen under strict mode. Common outside it.
   中文翻译：**Schema 违规。** 输出可解析但违反 Schema。strict mode 下不可能发生。在非 strict 下很常见。
3. **Refusal.** The model declines. Must be handled as a typed outcome.
   中文翻译：**拒绝。** 模型拒绝。必须作为类型化结果处理。

### Retry strategy

> **【中文解读】** 非 strict mode 下的恢复模式是"生成→解析→验证→失败则注入错误重试，最多 3 次"。通常一次重试就够了，三次覆盖弱模型的偶然失败。超过三次说明 Schema 设计有问题，需要修改 prompt 或 Schema。

When you are outside strict mode (Anthropic tool use, non-strict OpenAI, older Gemini), the recovery pattern is:

> 当你不在 strict mode 下时（Anthropic tool use、非 strict OpenAI、旧版 Gemini），恢复模式是：

```
generate -> parse -> validate -> if fail, inject error and retry, max 3x
```

One retry is usually enough. Three retries catches weak-model flakes. Beyond three is a sign of a bad schema: the model cannot satisfy it for some inputs, and the prompt or the schema needs fixing.

> 一次重试通常就够了。三次重试覆盖弱模型的偶然失败。超过三次说明 Schema 设计有问题：模型对某些输入无法满足，需要修改 prompt 或 Schema。

### Small-model support

Constrained decoding works on small models. A 3B-parameter open model with grammar enforcement out-performs a 70B-parameter model with raw prompting on structured tasks. This is the main reason structured outputs matter for production: it decouples reliability from model size.

> 约束解码也适用于小模型。一个配合语法强制的 3B 参数开源模型，在结构化任务上可超越 70B 参数模型的纯提示方法。这是结构化输出在生产中重要的主因：它解耦了可靠性与模型大小。

> **【中文解读】** 约束解码也适用于小模型。一个 3B 参数的开源模型配合语法强制，在结构化任务上可超越 70B 参数模型的纯提示方法。这是结构化输出在生产中重要的主因：它解耦了可靠性与模型大小。

## Use It | 用框架实现

`code/main.py` ships a minimal JSON Schema 2020-12 validator in stdlib (types, required, enum, min/max, pattern, items, additionalProperties). It wraps an `Invoice` schema and runs a fake LLM output through the validator, demonstrating parse error, schema violation, and refusal paths. Swap the fake output for any provider's real response in production.

> `code/main.py` 提供了一个用标准库实现的最小 JSON Schema 2020-12 验证器（类型、必填、枚举、最小/最大值、模式、items、additionalProperties）。它包装了一个 `Invoice` Schema 并将一个假的 LLM 输出通过验证器运行，演示解析错误、Schema 违规和拒绝路径。在生产中将假输出替换为任何提供商的真实响应。

What to look at:

> 需要关注的点：

- The validator returns a typed `[ValidationError]` list with path and message. That is the shape you want surfaced to the retry prompt.
  中文翻译：验证器返回一个带有路径和消息的类型化 `[ValidationError]` 列表。这就是你想要显示在重试提示中的格式。
- The refusal branch does NOT retry. It logs and returns a typed refusal. Phase 14 · 09 uses refusals as a safety signal.
  中文翻译：拒绝分支不会重试。它记录日志并返回类型化的拒绝。Phase 14 · 09 使用拒绝作为安全信号。
- The `additionalProperties: false` check fires on the adversarial test input, showing why strict mode shuts the door on hallucinated fields.
  中文翻译：`additionalProperties: false` 检查在对抗性测试输入上触发，展示了为什么 strict mode 关闭了幻觉字段的大门。

## Ship It | 产出物

This lesson produces `outputs/skill-structured-output-designer.md`. Given a free-text extraction target (invoices, support tickets, resumes, etc.), the skill produces a JSON Schema 2020-12 that is strict-mode-compatible and a Pydantic model that mirrors it, with typed refusal and retry handling stubbed in.

> 本课产出 `outputs/skill-structured-output-designer.md`。给定一个自由文本提取目标（发票、支持工单、简历等），该 skill 生成一个 strict mode 兼容的 JSON Schema 2020-12 和一个镜像它的 Pydantic 模型，并预置类型化的拒绝和重试处理。

## Exercises | 练习题

1. Run `code/main.py`. Add a fourth test case whose `total_usd` is a negative number. Confirm the validator rejects it with the `minimum` constraint path.
   中文翻译：运行 `code/main.py`。添加第四个测试用例，`total_usd` 为负数。确认验证器以 `minimum` 约束路径拒绝它。

2. Extend the validator to support `oneOf` with a discriminator. The common case: `line_item` is either a product or a service, tagged by `kind`. Strict mode has subtle rules here; check OpenAI's structured outputs guide.
   中文翻译：扩展验证器以支持带判别器的 `oneOf`。常见用例：`line_item` 是产品或服务，由 `kind` 标记。Strict mode 在此有微妙规则；查看 OpenAI 的结构化输出指南。

3. Write the same Invoice schema as a Pydantic BaseModel and compare `model_json_schema()` output to your hand-rolled schema. Identify the one field Pydantic sets by default that the hand-rolled version omits.
   中文翻译：将相同的 Invoice Schema 写成 Pydantic BaseModel，比较 `model_json_schema()` 输出与手写 Schema。找出 Pydantic 默认设置但手写版本遗漏的字段。

4. Measure refusal rates. Construct ten inputs that should not be extractable (a song lyric, a math proof, a blank email) and run them through a real provider with strict mode. Count refusals vs hallucinated outputs. This is your ground truth for refusal-aware retries.
   中文翻译：测量拒绝率。构造十个不应可提取的输入（歌词、数学证明、空白邮件），通过 strict mode 的真实提供商运行。统计拒绝与幻觉输出的数量。这是拒绝感知重试的基准事实。

5. Read OpenAI's structured outputs guide top to bottom. Identify the one construct it explicitly forbids in strict mode that plain JSON Schema allows. Then design a schema that uses the forbidden construct non-essentially and refactor it to be strict-compatible.
   中文翻译：从头到尾阅读 OpenAI 的结构化输出指南。找出它在 strict mode 中明确禁止但普通 JSON Schema 允许的构造。然后设计一个非必要地使用该禁止构造的 Schema，并重构为 strict 兼容。

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
  中文翻译：strict mode、拒绝和 Schema 要求
- [OpenAI — Introducing structured outputs](https://openai.com/index/introducing-structured-outputs-in-the-api/) — August 2024 launch post explaining the decoding guarantee
  中文翻译：2024 年 8 月发布博文，解释解码保证
- [Pydantic AI — Output](https://ai.pydantic.dev/output/) — typed output_type bindings that serialize to each provider
  中文翻译：序列化到各提供商的类型化 output_type 绑定
- [JSON Schema — 2020-12 release notes](https://json-schema.org/draft/2020-12/release-notes) — the canonical spec
  中文翻译：规范权威文档
- [Microsoft — Structured outputs in Azure OpenAI](https://learn.microsoft.com/en-us/azure/foundry/openai/how-to/structured-outputs) — enterprise deployment notes and strict-mode caveats
  中文翻译：企业部署说明和 strict mode 注意事项
