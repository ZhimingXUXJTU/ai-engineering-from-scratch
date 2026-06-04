# 结构化输出 — JSON Schema、Pydantic、Zod 与约束解码

> "礼貌地让模型返回 JSON"在前沿模型上仍有 5-15% 的失败率。结构化输出通过约束解码弥合这一差距：模型在 token 级别被阻止发出违反 Schema 的内容。OpenAI strict mode、Anthropic schema-typed tool use、Gemini `responseSchema`、Pydantic AI `output_type` 和 Zod `.parse` 是同一思想的五种表面形式。本课构建 Schema 验证器和严格模式契约，学习者将在每个生产提取管道中使用它们。

> **【中文解读】** "礼貌地让模型返回 JSON"在前沿模型上仍有 5-15% 的失败率。结构化输出通过约束解码弥合这一差距：模型在 token 级别被阻止发出违反 Schema 的内容。OpenAI strict mode、Anthropic schema-typed tool use、Gemini `responseSchema`、Pydantic AI `output_type` 和 Zod `.parse` 是同一思想的五种表面形式。

> **【拓展：结构化输出→Function Calling 的质量保障】** 结构化输出是所有数据提取管道的基础。在 Function Calling 场景中，结构化输出确保工具参数的 JSON 格式始终有效。OpenAI 的 strict mode 通过 constrained decoding 在解码时屏蔽违反 Schema 的 token，Anthropic 通过 `input_schema` 在 tool_use 中实现类似保证。这消除了"模型返回无效 JSON"这一最常见的生产故障模式。

**类型：** 构建
**语言：** Python（标准库，JSON Schema 2020-12 子集）
**前置条件：** Phase 13 · 02（函数调用深入）
**时间：** 约 75 分钟

## 学习目标

- 使用正确的约束（enum、min/max、required、pattern）为提取目标编写 JSON Schema 2020-12。
- 解释严格模式和约束解码与"生成后验证"提供不同保证的原因。
- 区分三种失败模式：解析错误、Schema 违规、模型拒绝。
- 构建带有类型化修复和类型化拒绝处理的提取管道。

## 问题引入

一个读取采购订单邮件的 Agent 需要将自由文本转换为 `{customer, line_items, total_usd}`。三种方法。

**方法一：提示返回 JSON。** "以 JSON 回复，包含 customer、line_items、total_usd 字段。"在前沿模型上 85% 到 95% 的时间有效。失败有六种方式：缺少大括号、尾随逗号、类型错误、幻觉字段、在 token 限制处截断、泄漏散文如"这是你的 JSON："。

**方法二：生成后验证。** 自由生成，解析，根据 Schema 验证，失败时重试。可靠但昂贵——你为每次重试付费，而且截断 bug 每次发生都要额外花费一轮。

**方法三：约束解码。** 供应商在解码时强制执行 Schema。无效 token 被从采样分布中屏蔽。输出保证可解析且保证可验证。失败归结为一种模式：拒绝（模型认为输入不符合 Schema）。

每个 2026 年的前沿供应商都提供了某种形式的方法三。

- **OpenAI。** `response_format: {type: "json_schema", strict: true}` 加上响应中的 `refusal`（如果模型拒绝）。
- **Anthropic。** 在 `tool_use` 输入上进行 Schema 强制执行；`stop_reason: "refusal"` 不存在，但 `end_turn` 且没有工具调用就是信号。
- **Gemini。** 请求级的 `responseSchema`；2026 年 Gemini 为选定类型提供 token 级语法约束。
- **Pydantic AI。** `output_type=InvoiceModel` 发出类型化为 `InvoiceModel` 的结构化 `RunResult`。
- **Zod（TypeScript）。** 根据 Zod Schema 验证供应商输出的运行时解析器；与 OpenAI 的 `beta.chat.completions.parse` 配对使用。

共同主线：声明一次 Schema，端到端强制执行。

## 核心概念

### JSON Schema 2020-12 — 通用语言

每个供应商都接受 JSON Schema 2020-12。你最常用的构造：

- `type`：`object`、`array`、`string`、`number`、`integer`、`boolean`、`null` 之一。
- `properties`：字段名到子 Schema 的映射。
- `required`：必须出现的字段名列表。
- `enum`：允许值的封闭集合。
- `minimum` / `maximum`（数字），`minLength` / `maxLength` / `pattern`（字符串）。
- `items`：应用于每个数组元素的子 Schema。
- `additionalProperties`：`false` 禁止额外字段（默认值因模式而异）。

OpenAI 严格模式添加三个要求：每个属性必须在 `required` 中列出，所有地方 `additionalProperties: false`，不得有未解析的 `$ref`。如果你违反这些，API 在请求时返回 400。

### Pydantic，Python 绑定

Pydantic v2 通过 `model_json_schema()` 从数据类形状的模型生成 JSON Schema。Pydantic AI 封装了这一点，使你只需编写：

```python
class Invoice(BaseModel):
    customer: str
    line_items: list[LineItem]
    total_usd: Decimal
```

Agent 框架在边缘将 Schema 翻译为 OpenAI 严格模式、Anthropic `input_schema` 或 Gemini `responseSchema`。模型的输出以类型化的 `Invoice` 实例返回。验证错误抛出带有类型化错误路径的 `ValidationError`。

### Zod，TypeScript 绑定

Zod（`z.object({customer: z.string(), ...})`）是 TypeScript 的等价物。OpenAI 的 Node SDK 暴露了 `zodResponseFormat(Invoice)`，将其翻译为 API 的 JSON Schema 载荷。

### 拒绝

严格模式不能强制模型回答。如果输入无法适配 Schema（"邮件是诗歌而非发票"），模型发出一个包含原因的 `refusal` 字段。你的代码必须将此作为一等公民结果处理，而非失败。拒绝也可用作安全信号：当模型被要求从受保护内容中提取信用卡号时，会返回附有安全原因的拒绝。

### 开源约束解码

开源实现使用三种技术。

1. **基于语法的解码**（`outlines`、`guidance`、`lm-format-enforcer`）：从 Schema 构建确定性有限自动机；在每一步屏蔽会违反 FSM 的 token 的 logits。
2. **带 JSON 解析器的 Logit 屏蔽**：与模型同步运行流式 JSON 解析器；在每一步计算有效下一 token 集合。
3. **带验证器的推测解码**：廉价草稿模型提出 token，验证器强制执行 Schema。

商业供应商在幕后选择其中之一。2026 年的先进水平对于短结构化输出比纯生成更快，对于长结构化输出大约相同速度。

### 三种失败模式

1. **解析错误。** 输出不是有效的 JSON。在严格模式下不可能发生。在非严格供应商上仍可能发生。
2. **Schema 违规。** 输出解析了但违反了 Schema。在严格模式下不可能发生。在非严格模式下常见。
3. **拒绝。** 模型拒绝。必须作为类型化结果处理。

### 重试策略

在严格模式之外（Anthropic tool use、非严格 OpenAI、旧版 Gemini），恢复模式是：

```
生成 -> 解析 -> 验证 -> 失败则注入错误重试，最多 3 次
```

一次重试通常就够了。三次重试覆盖弱模型的偶然失败。超过三次说明 Schema 设计有问题：模型在某些输入上无法满足它，需要修改 prompt 或 Schema。

### 小模型支持

约束解码也适用于小模型。一个 3B 参数的开源模型配合语法强制，在结构化任务上可超越 70B 参数模型的纯提示方法。这是结构化输出在生产中重要的主因：它解耦了可靠性与模型大小。

## 用框架实现

`code/main.py` 提供了一个标准库中最小的 JSON Schema 2020-12 验证器（类型、必填、枚举、最小/最大值、pattern、items、additionalProperties）。它包装了一个 `Invoice` Schema 并通过验证器运行假的 LLM 输出，展示解析错误、Schema 违规和拒绝路径。在生产中将假输出替换为任何供应商的真实响应。

关注点：

- 验证器返回类型化的 `[ValidationError]` 列表，带有路径和消息。这是你应该向重试提示中暴露的形状。
- 拒绝分支不会重试。它记录日志并返回类型化的拒绝。Phase 14 · 09 使用拒绝作为安全信号。
- `additionalProperties: false` 检查在对抗性测试输入上触发，展示了严格模式为什么关上了幻觉字段的大门。

## 产出物

本课产生 `outputs/skill-structured-output-designer.md`。给定一个自由文本提取目标（发票、支持工单、简历等），该技能生成一个兼容严格模式的 JSON Schema 2020-12 和镜像它的 Pydantic 模型，并内置类型化拒绝和重试处理桩。

## 练习题

1. 运行 `code/main.py`。添加第四个测试用例，其中 `total_usd` 为负数。确认验证器以 `minimum` 约束路径拒绝它。

2. 扩展验证器以支持带判别器的 `oneOf`。常见情况：`line_item` 是产品或服务，由 `kind` 标记。严格模式在这里有细微的规则；查看 OpenAI 的结构化输出指南。

3. 用 Pydantic BaseModel 编写相同的 Invoice Schema，并将 `model_json_schema()` 输出与你手写的 Schema 比较。识别 Pydantic 默认设置而手写版本省略的一个字段。

4. 测量拒绝率。构造十个不应可提取的输入（一首歌词、一个数学证明、一封空白邮件），用严格模式通过真实供应商运行。计算拒绝与幻觉输出的数量。这是你拒绝感知重试的基本事实。

5. 从头到尾阅读 OpenAI 的结构化输出指南。识别它在严格模式中明确禁止而普通 JSON Schema 允许的一个构造。然后设计一个非必要地使用该禁止构造的 Schema，并将其重构为严格兼容。

## 术语速查表

| 术语 | 人们怎么说 | 实际含义 | 英文 |
|------|-----------|---------|------|
| JSON Schema 2020-12 | "Schema 规范" | 每个现代供应商都使用的 IETF 草案 Schema 方言 | JSON Schema 2020-12 规范 |
| 严格模式 | "保证 Schema" | 通过约束解码强制执行 Schema 的 OpenAI 标志 | Strict mode |
| 约束解码 | "Logit 屏蔽" | 解码时屏蔽无效下一 token 的强制执行 | Constrained decoding |
| 模型拒绝 | "模型拒绝" | 输入无法适配 Schema 时的类型化结果 | Refusal |
| 解析错误 | "无效 JSON" | 输出未解析为 JSON；严格模式下不可能 | Parse error |
| Schema 违规 | "形状错误" | 解析了但违反了类型/必填/枚举/范围 | Schema violation |
| `additionalProperties: false` | "不允许额外" | 禁止未知字段；OpenAI 严格模式要求 | 禁止额外属性 |
| Pydantic BaseModel | "类型化输出" | 生成和验证 JSON Schema 的 Python 类 | Pydantic 基础模型 |
| Zod Schema | "TypeScript 输出类型" | 用于供应商输出验证的 TS 运行时 Schema | Zod 类型定义 |
| 语法强制 | "开源约束解码" | 基于 FSM 的 logit 屏蔽，如 outlines / guidance | Grammar enforcement |

## 延伸阅读

- [OpenAI — Structured outputs](https://platform.openai.com/docs/guides/structured-outputs) — 严格模式、拒绝和 Schema 要求
- [OpenAI — Introducing structured outputs](https://openai.com/index/introducing-structured-outputs-in-the-api/) — 2024 年 8 月发布文章，解释解码保证
- [Pydantic AI — Output](https://ai.pydantic.dev/output/) — 序列化为每个供应商的类型化 output_type 绑定
- [JSON Schema — 2020-12 release notes](https://json-schema.org/draft/2020-12/release-notes) — 权威规范
- [Microsoft — Structured outputs in Azure OpenAI](https://learn.microsoft.com/en-us/azure/foundry/openai/how-to/structured-outputs) — 企业部署说明和严格模式注意事项
