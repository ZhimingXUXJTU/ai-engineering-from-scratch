# 并行工具调用与流式工具

> 三个独立的天气查询串行执行需要三次往返。并行运行后，总时间缩减为最慢的单次调用时间。所有前沿供应商现在都支持在单轮中发出多个工具调用。收益是真实的，但管道搭建却很微妙。本课涵盖两个部分：并行扇出和流式参数重组，重点讲解 ID 关联陷阱。

> **【中文解读】** 三个独立的天气查询串行执行需要三次往返。并行运行后，总时间缩减为最慢的单次调用时间。所有前沿模型提供商现在都支持在单轮中发出多个工具调用。收益是真实的，但管道搭建却很微妙。本课涵盖两个部分：并行扇出和流式参数重组，重点讲解 id 关联陷阱。

> **【拓展：并行调用→Agent 效率优化】** 并行工具调用是 AI Agent 效率的关键优化。当 Agent 需要同时查询多个数据源（如多城市天气、多股票价格）时，并行调用可将延迟降低 60-70%。MCP 协议天然支持并行调用，Claude 的 `disable_parallel_tool_use` 参数和 OpenAI 的 `parallel_tool_calls` 参数都控制这一行为。

**类型：** 构建
**语言：** Python（标准库，线程池 + 流式线束）
**前置条件：** Phase 13 · 02（函数调用深入）
**时间：** 约 75 分钟

## 学习目标

- 解释 `parallel_tool_calls: true` 存在的原因以及何时应该禁用它。
- 在并行扇出期间将流式参数块关联到正确的工具调用 ID。
- 在不提前解析的情况下将部分 `arguments` 字符串重组为完整 JSON。
- 运行三城市天气基准测试，展示串行与并行的延迟差异。

## 问题引入

没有并行调用时，Agent 回答"Bengaluru、东京和苏黎世的天气如何"需要这样做：

```
用户 -> LLM
LLM -> 调用 get_weather(Bengaluru)
宿主 -> 运行执行器，返回结果
LLM -> 调用 get_weather(东京)
宿主 -> 运行执行器，返回结果
LLM -> 调用 get_weather(苏黎世)
宿主 -> 运行执行器，返回结果
LLM -> 最终文本回答
```

三次 LLM 往返，每次还要支付执行器延迟。大约是理想挂钟时间的 4 倍。

有并行调用时：

```
用户 -> LLM
LLM -> 调用 get_weather(Bengaluru); 调用 get_weather(东京); 调用 get_weather(苏黎世)
宿主 -> 并发运行三个执行器，返回三个结果
LLM -> 最终文本回答
```

一次 LLM 往返。执行器时间是三个中的最大值，而非总和。在 OpenAI、Anthropic 和 Gemini 上的生产基准测试显示，扇出工作负载的挂钟时间减少 60% 到 70%。

代价是关联复杂性。当三个调用乱序完成时，你的结果必须携带匹配的 `tool_call_id`，以便模型能对齐它们。当结果流式传输时，你必须在执行前将部分参数片段组装成完整 JSON。Gemini 3 添加唯一 ID 部分是为了解决一个实际问题：两个对同一工具的并行调用是无法区分的。

## 核心概念

### 启用并行

- **OpenAI。** `parallel_tool_calls: true` 默认开启。设 `false` 强制串行。
- **Anthropic。** 通过 `disable_parallel_tool_use: false` 并行（Claude 3.5 起默认）。设 `true` 为串行。
- **Gemini。** 始终支持并行；`tool_config.function_calling_config.mode = "AUTO"` 让模型决定。

当工具有顺序依赖（`create_file` 然后 `write_file`）、一个调用的输出影响另一个的输入、或速率限制器无法处理扇出时，应禁用并行。

### ID 关联

模型发出的每个调用都有一个 `id`。宿主返回的每个结果必须包含相同的 ID。没有这个，结果就会产生歧义。

- **OpenAI。** 每个 tool-role 消息上的 `tool_call_id`。
- **Anthropic。** 每个 `tool_result` 块上的 `tool_use_id`。
- **Gemini。** 每个 `functionResponse` 上的 `id`（Gemini 3 及以上；Gemini 2 按名称匹配，对同名并行调用会出错）。

### 并发运行调用

宿主在自己的线程、协程或远程 worker 上运行每个调用的执行器。最简单的线束使用线程池；生产环境使用 asyncio 的 `asyncio.gather` 或结构化并发。完成顺序不可预测——ID 是标识符。

一个常见 bug：按调用列表顺序而非完成顺序回复。这通常可以工作，因为模型只关心 `tool_call_id`，但如果结果被丢弃或重复，乱序提交会使调试更困难。优先按完成顺序回复并使用显式 ID。

### 流式工具调用

当模型流式传输时，`arguments` 分片到达。三个并行调用的三股独立流在线上交错。你需要每个 ID 一个累加器。

各供应商的形状：

- **OpenAI。** 每个块是 `choices[0].delta.tool_calls[i].function.arguments`（部分字符串）。块携带 `index`（调用列表中的位置）。你按索引累积，当 `id` 首次出现时读取，在 `finish_reason = "tool_calls"` 时解析 JSON。
- **Anthropic。** 流事件是 `message_start`，然后每个类型为 `tool_use` 的块一个 `content_block_start`（包含 id、name、空 input）。`content_block_delta` 事件携带 `input_json_delta` 块。`content_block_stop` 关闭每个块。
- **Gemini。** `streamFunctionCallArguments`（Gemini 3 及以上）发出带有 `functionCallId` 的块，使调用干净地交错。Gemini 3 之前，流式传输一次返回一个完整调用。

### 部分 JSON 和过早解析陷阱

你不能在 `arguments` 完成之前尝试解析。`{"city": "Beng` 这样的部分 JSON 无效，会抛出异常。正确的门控是供应商的调用结束信号：OpenAI 的 `finish_reason = "tool_calls"`、Anthropic 的 `content_block_stop` 或 Gemini 的 stream-end 事件。只有在那之后才尝试 `json.loads`。更健壮的方法使用增量 JSON 解析器，在结构完成时产生事件；OpenAI 的流式传输指南推荐这种方式，用于显示实时"思考"指示器的 UX。大括号计数作为完整性测试不可靠（引号字符串内的括号或转义内容会导致误判），应仅作为非正式的调试启发式使用。

### 乱序完成

```
call_A: 快速 API，首先返回
call_B: 慢速 API，第二返回
call_C: 中速 API，第三返回
```

宿主回复仍必须引用 ID：

```
[{role: "tool", tool_call_id: "call_A", content: ...},
 {role: "tool", tool_call_id: "call_B", content: ...},
 {role: "tool", tool_call_id: "call_C", content: ...}]
```

回复中的顺序在 OpenAI 或 Anthropic 上不影响正确性。Gemini 接受任何顺序，只要 ID 匹配。

### 基准测试：串行 vs 并行

`code/main.py` 中的线束模拟三个具有 400、600 和 800 毫秒延迟的执行器。串行总共运行 1800 毫秒。并行运行 max(400, 600, 800) = 800 毫秒。差异是恒定的，非比例的，因此节省量随工具数量增长。

现实世界的注意事项：并行调用会对下游 API 施加压力。10 路扇出到限速服务会失败。Phase 13 · 17 涵盖网关级背压；重试语义计划在未来的阶段中。

### 流式扇出挂钟时间

如果模型本身流式传输，你可以在一个调用的参数完成后立即开始执行，而不必等待所有调用完成。这是 OpenAI 文档记录的优化，但并非所有 SDK 都暴露。本课的线束实现了这一点：模拟流产生完整参数对象后，宿主立即启动该调用。

## 用框架实现

`code/main.py` 有两个部分。第一部分使用 `concurrent.futures.ThreadPoolExecutor` 串行和并行运行三个模拟天气调用，并打印挂钟时间。第二部分回放一个假的流式响应——三个并行调用的 `arguments` 块在一个流上交错——并通过 `StreamAccumulator` 按 ID 重组。无 LLM、无网络，只有重组逻辑。

关注点：

- 串行计时器达到 1.8 秒。并行计时器在相同假延迟下达到 0.8 秒。
- 累加器通过按 ID 缓冲并仅在 JSON 完成时解析来处理乱序到达的块。
- 执行器在 ID 的参数完成后立即启动，而非在所有流结束后。

## 产出物

本课产生 `outputs/skill-parallel-call-safety-check.md`。给定一个工具注册表，该技能审计哪些工具可以安全并行化、哪些有顺序依赖、哪些会压垮下游速率限制——返回带有每个工具 `parallel_safe` 标志的修订注册表。

## 练习题

1. 运行 `code/main.py` 并调整模拟延迟。确认并行与串行的比例约为 `max/sum`（实际运行因线程调度、序列化和线束开销与理想值略有偏差）。在什么延迟分布下并行不再重要？

2. 扩展累加器以处理"调用在流中途被取消"的情况，丢弃其缓冲区并发出 `cancelled` 事件。哪个供应商明确文档化了这种情况？检查 Anthropic 的 `content_block_stop` 语义和 OpenAI 的 `finish_reason: "length"` 行为。

3. 用 `asyncio.gather` 替换线程池。对两者进行基准测试。如果执行器进行真正的 I/O，你应该能看到 async 的小幅优势。

4. 选择两个不应该并行化的工具（如 `create_file` 然后 `write_file`）。向注册表添加 `ordering_dependency` 图，并在该图上限制并行扇出。这是依赖感知调度的最小机制，未来的 Agent 工程阶段将正式化。

5. 阅读 OpenAI 的并行函数调用部分和 Anthropic 的 `disable_parallel_tool_use` 文档。识别 Anthropic 建议禁用并行的一种真实世界工具类型。（提示：对同一资源的后果性变更。）

## 术语速查表

| 术语 | 人们怎么说 | 实际含义 | 英文 |
|------|-----------|---------|------|
| 并行工具调用 | "一轮扇出" | 模型在一个 assistant 消息中发出多个工具调用 | Parallel tool calls |
| `parallel_tool_calls` | "OpenAI 的开关" | 启用或禁用多次调用发出 | OpenAI 并行调用开关 |
| `disable_parallel_tool_use` | "Anthropic 的反转" | 选择禁用标志；默认启用并行 | Anthropic 并行禁用开关 |
| 工具调用 ID | "关联句柄" | 结果消息必须回显的每次调用标识符 | Tool call id |
| 流式累加器 | "流缓冲" | 按ID的字符串缓冲区用于部分 `arguments` 块 | Accumulator |
| 乱序完成 | "最快的先到" | 并行调用以不可预测的顺序完成；ID 是粘合剂 | Out-of-order completion |
| 依赖图 | "顺序约束" | 输出馈入其他工具输入的工具；不能并行化 | Dependency graph |
| 过早解析陷阱 | "JSON.parse 爆炸了" | 尝试解析不完整的 `arguments` 字符串 | Parse-early trap |
| `streamFunctionCallArguments` | "Gemini 3 功能" | 带有每次调用唯一 ID 的流式参数块 | Gemini 3 流式参数 |
| 按完成顺序回复 | "不要等所有" | 按到达顺序带 ID 键回复结果 | Completion-order reply |

## 延伸阅读

- [OpenAI — Parallel function calling](https://platform.openai.com/docs/guides/function-calling#parallel-function-calling) — 默认行为和选择禁用标志
- [Anthropic — Tool use: implementing tool use](https://docs.anthropic.com/en/docs/agents-and-tools/tool-use/implementing-tool-use) — `disable_parallel_tool_use` 和结果批处理
- [Google — Gemini function calling parallel section](https://ai.google.dev/gemini-api/docs/function-calling) — Gemini 3 起的 ID 关联并行调用
- [OpenAI — Streaming responses with tools](https://platform.openai.com/docs/api-reference/responses-streaming) — OpenAI 流的块化参数重组
- [Anthropic — Streaming messages](https://docs.anthropic.com/en/api/messages-streaming) — 携带 `input_json_delta` 的 `content_block_delta`
