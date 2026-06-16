# Parallel Tool Calls and Streaming with Tools | 并行工具调用与流式工具

> Three independent weather lookups serialized is three round trips. Run them in parallel and total time collapses to the slowest single call. Every frontier provider now emits multiple tool calls in a single turn. The payoff is real; the plumbing is subtle. This lesson walks both halves: the parallel fan-out and the streamed-argument reassembly, with emphasis on the id-correlation trap.

> **【中文解读】** 三个独立的天气查询串行执行需要三次往返。并行运行后，总时间缩减为最慢的单次调用时间。所有前沿模型提供商现在都支持在单轮中发出多个工具调用。收益是真实的，但管道搭建却很微妙。本课涵盖两个部分：并行扇出和流式参数重组，重点讲解 id 关联陷阱。

> **【拓展：并行调用→Agent 效率优化】** 并行工具调用是 AI Agent 效率的关键优化。当 Agent 需要同时查询多个数据源（如多城市天气、多股票价格）时，并行调用可将延迟降低 60-70%。MCP 协议天然支持并行调用，Claude 的 `disable_parallel_tool_use` 参数和 OpenAI 的 `parallel_tool_calls` 参数都控制这一行为。

> 🔗 **【前置】** 学本节前请先掌握：(1) Phase 13·02（Function Calling Deep Dive）——掌握三家 API 形态差异，本节是它的并发延伸；(2) Python `concurrent.futures` 或 `asyncio.gather` 基础，本节会用线程池并行执行器；(3) JSON 拼接技巧——流式 `arguments` 是分片到达，必须累积后再 `json.loads`，不能中途解析。

**Type:** Build | **类型:** 构建
**Languages:** Python (stdlib, thread pool + streaming harness) | **语言:** Python（标准库，线程池 + 流式线束）
**Prerequisites:** Phase 13 · 02 (function calling deep dive) | **前置知识:** Phase 13 · 02（函数调用深入）
**Time:** ~75 minutes | **时间:** ~75 分钟

## Learning Objectives | 学习目标

- Explain why `parallel_tool_calls: true` exists and when to disable it.
  中文翻译：解释为什么存在 `parallel_tool_calls: true` 以及何时禁用它。
- Correlate streamed argument chunks to the right tool-call id during parallel fan-out.
  中文翻译：在并行扇出期间将流式参数块关联到正确的工具调用 id。
- Reassemble partial `arguments` strings into complete JSON without parsing early.
  中文翻译：将部分 `arguments` 字符串重组为完整 JSON，而不提前解析。
- Run a three-city weather benchmark that demonstrates sequential vs parallel latency.
  中文翻译：运行三城市天气基准测试，展示串行与并行延迟的对比。

## The Problem | 问题引入

Without parallel calls, an agent answering "what is the weather in Bengaluru, Tokyo, and Zurich" does this:

> 没有并行调用时，一个回答"Bengaluru、东京和苏黎世的天气如何"的 agent 会这样做：

```
user -> LLM
LLM -> call get_weather(Bengaluru)
host -> run executor, reply with result
LLM -> call get_weather(Tokyo)
host -> run executor, reply with result
LLM -> call get_weather(Zurich)
host -> run executor, reply with result
LLM -> final text answer
```

Three LLM round trips, each of which also pays the executor latency. Roughly 4x the ideal wall-clock time.

> 三次 LLM 往返，每次还要支付执行器延迟。大约是理想挂钟时间的 4 倍。

> **【中文解读】** 没有并行调用时，Agent 回答"Bengaluru、东京和苏黎世的天气如何"需要三次 LLM 往返，每次还要支付执行器延迟，总耗时约为理想时间的 4 倍。

With parallel calls:

> 有并行调用时：

```
user -> LLM
LLM -> call get_weather(Bengaluru); call get_weather(Tokyo); call get_weather(Zurich)
host -> run all three executors concurrently, reply with three results
LLM -> final text answer
```

One LLM round trip. Executor time is the maximum of the three, not the sum. Production benchmarks on OpenAI, Anthropic, and Gemini show 60 to 70 percent wall-clock reduction on fan-out workloads.

> 一次 LLM 往返。执行器时间是三个中的最大值，而非总和。OpenAI、Anthropic 和 Gemini 上的生产基准测试显示，扇出工作负载的挂钟时间减少 60-70%。

> 💡 **【类比】** 并行调用像超市结账。串行调用 = 你一个人排队买完肉、再排队买菜、再排队买酒，总时间=三个队伍时间相加。并行调用 = 你给三个朋友打电话"你们各排一个队，同时结账"，总时间=最慢那个队伍的时间。前提是三个购物任务互相独立（朋友买什么不依赖别人买到了什么），这就是为什么"工具间有依赖"时必须串行。

The price is correlation complexity. When the three calls complete out of order, your results must carry the matching `tool_call_id` so the model can line them up. When results stream, you must assemble partial argument fragments into complete JSON before executing. Gemini 3 added unique ids in part to solve a real-world issue where two parallel calls to the same tool were indistinguishable.

> 代价是关联复杂性。当三个调用乱序完成时，结果必须携带匹配的 `tool_call_id`，以便模型对齐。流式场景下，必须在执行前将部分参数片段组装成完整 JSON。Gemini 3 增加唯一 ID 部分是为了解决两个同名工具的并行调用无法区分的现实问题。

> **【中文解读】** 并行调用的代价是关联复杂性。当三个调用乱序完成时，结果必须携带匹配的 `tool_call_id`，以便模型对齐。流式场景下，必须将部分参数片段组装成完整 JSON 后才能执行。Gemini 3 增加唯一 id 正是为了解决两个同名工具的并行调用无法区分的问题。

## The Concept | 核心概念

### Enabling parallel

> **【拓展：何时禁用并行调用】** 禁用并行调用的典型场景包括：(1) 工具有顺序依赖（如先创建文件再写入）；(2) 一个调用的输出是另一个的输入（如先查用户ID再查订单）；(3) 下游 API 有速率限制，10路扇出会导致 429 错误。在实际生产中，约 30% 的工具调用场景需要串行执行。

- **OpenAI.** `parallel_tool_calls: true` on by default. Set `false` to force serial.
  中文翻译：**OpenAI。** `parallel_tool_calls: true` 默认开启。设为 `false` 强制串行。
- **Anthropic.** Parallel via `disable_parallel_tool_use: false` (default on Claude 3.5 and up). Set `true` for serial.
  中文翻译：**Anthropic。** 通过 `disable_parallel_tool_use: false` 并行（Claude 3.5 及以上默认）。设为 `true` 强制串行。
- **Gemini.** Always parallel-capable; `tool_config.function_calling_config.mode = "AUTO"` lets the model decide.
  中文翻译：**Gemini。** 始终支持并行；`tool_config.function_calling_config.mode = "AUTO"` 让模型自行决定。

Disable parallel when tools have ordering dependencies (`create_file` then `write_file`), when one call's output informs another's input, or when the rate limiter cannot handle fan-out.

> 当工具有顺序依赖（先 `create_file` 再 `write_file`）、一个调用的输出影响另一个的输入、或速率限制器无法处理扇出时，禁用并行。

> **【中文解读】** 当工具有顺序依赖（先 `create_file` 再 `write_file`）、一个调用的输出影响另一个的输入、或速率限制器无法处理扇出时，应禁用并行。

> 🤔 **【困惑】** Q: 模型怎么知道哪些调用可以并行？A: 模型并不知道，它只决定"现在要调这几个工具"；并发执行是宿主的事。模型发出 `[get_weather(Tokyo), get_weather(Zurich)]` 时，宿主自己判断这两个无依赖就可以并发；如果模型发出 `[create_file, write_file]`，宿主必须串行（通常做法是禁用并行+顺序执行，或者执行器内做依赖检查）。所以"是否并行"是宿主配置+模型决定共同决定的。

### Id correlation

Every call the model emits has an `id`. Every result the host returns must include the same id. Without this, results are ambiguous.

> 模型发出的每个调用都有一个 `id`。宿主返回的每个结果必须包含相同的 id。没有这个，结果是模糊的。

- **OpenAI.** `tool_call_id` on each tool-role message.
  中文翻译：**OpenAI。** 每个 tool 角色消息上的 `tool_call_id`。
- **Anthropic.** `tool_use_id` on each `tool_result` block.
  中文翻译：**Anthropic。** 每个 `tool_result` 块上的 `tool_use_id`。
- **Gemini.** `id` on each `functionResponse` (Gemini 3 and up; Gemini 2 matched by name which broke for same-name parallel calls).
  中文翻译：**Gemini。** 每个 `functionResponse` 上的 `id`（Gemini 3 及以上；Gemini 2 按名称匹配，同名并行调用时会出错）。

### Running calls concurrently

The host runs each call's executor on its own thread, coroutine, or remote worker. The simplest harness uses a thread pool; production uses asyncio with `asyncio.gather` or structured concurrency. Order of completion is unpredictable — the id is the identifier.

> 宿主在每个调用的执行器上运行自己的线程、协程或远程工作器。最简单的线束使用线程池；生产环境使用 asyncio 的 `asyncio.gather` 或结构化并发。完成顺序不可预测——id 是标识符。

> ⚠️ **【易错点】** 场景：流式模式下对每个 `arguments` 分片立即 `json.loads` / 后果：JSON 不完整触发 `JSONDecodeError`，因为流式可能在你收到 `{"city":"To` 时就触发回调 / 修复：每个 `tool_call_id` 维护一个 `accumulator` 字符串，所有分片 `+=` 后等 `finish_reason="tool_calls"` 才整体解析；并行时用 `{id: accumulator}` 字典隔离。

One common bug: reply with results in call-list order instead of completion order. This usually works because the model only cares about `tool_call_id`, but if a result is dropped or duplicated, out-of-order submission makes debugging harder. Prefer to reply in completion order with explicit ids.

> 一个常见 bug：按调用列表顺序而非完成顺序回复结果。这通常可以工作，因为模型只关心 `tool_call_id`，但如果结果被丢弃或重复，乱序提交会使调试更困难。优先按完成顺序回复并附带明确的 id。

### Streaming tool calls

> **【拓展：流式工具调用的用户体验】** 流式工具调用让用户能看到 Agent 正在"思考"和执行的过程，而非等待一个黑箱操作完成。这对长耗时工具特别有价值——用户可以看到参数逐步构建，提供心理预期。OpenAI 的 ChatGPT 和 Anthropic 的 Claude 都在 UI 中展示了工具调用的流式过程。

When the model streams, `arguments` arrive in pieces. Three separate streams of chunks for three parallel calls interleave on the wire. You need one accumulator per id.

> 当模型流式传输时，`arguments` 分片到达。三个并行调用的三个独立流块在传输中交错。你需要每个 id 一个累加器。

Shape by provider:

> 各供应商的格式：

- **OpenAI.** Each chunk is `choices[0].delta.tool_calls[i].function.arguments` (partial string). The chunk carries `index` (position in the call list). You accumulate per-index, read `id` when it first appears, and parse JSON when `finish_reason = "tool_calls"`.
  中文翻译：**OpenAI。** 每个块是 `choices[0].delta.tool_calls[i].function.arguments`（部分字符串）。块携带 `index`（调用列表中的位置）。你按索引累积，首次出现时读取 `id`，在 `finish_reason = "tool_calls"` 时解析 JSON。
- **Anthropic.** Stream events are `message_start`, then one `content_block_start` per block with type `tool_use` (containing id, name, empty input). `content_block_delta` events carry `input_json_delta` chunks. `content_block_stop` closes each block.
  中文翻译：**Anthropic。** 流事件先是 `message_start`，然后每个类型为 `tool_use` 的块有一个 `content_block_start`（包含 id、name、空 input）。`content_block_delta` 事件携带 `input_json_delta` 块。`content_block_stop` 关闭每个块。
- **Gemini.** `streamFunctionCallArguments` (Gemini 3 and up) emits chunks with a `functionCallId` so calls interleave cleanly. Before Gemini 3, streaming returned one complete call at a time.
  中文翻译：**Gemini。** `streamFunctionCallArguments`（Gemini 3 及以上）发出带有 `functionCallId` 的块，使调用可以干净地交错。Gemini 3 之前，流式每次返回一个完整调用。

### Partial JSON and the parse-early trap

You cannot parse `arguments` until it is complete. Partial JSON such as `{"city": "Beng` is not valid and will raise. The correct gate is the provider's end-of-call signal: OpenAI's `finish_reason = "tool_calls"`, Anthropic's `content_block_stop`, or Gemini's stream-end event. Only then attempt `json.loads`. A more robust approach uses an incremental JSON parser that yields events as structure completes; OpenAI's streaming guide recommends this for UX that shows a live "thinking" indicator. Brace-counting is unreliable as a completeness test (braces inside quoted strings or escaped content cause false positives) and should only be used as an informal debug heuristic.

> 在 `arguments` 完成之前不能尝试解析。像 `{"city": "Beng` 这样的部分 JSON 无效，会抛出异常。正确的门控是提供商的调用结束信号：OpenAI 的 `finish_reason = "tool_calls"`、Anthropic 的 `content_block_stop`、或 Gemini 的 stream-end 事件。只有那时才尝试 `json.loads`。更健壮的方法使用增量 JSON 解析器，在结构完成时产生事件；OpenAI 的流式指南推荐用于显示实时"思考"指示器的 UX。大括号计数作为完整性测试不可靠（引号字符串或转义内容中的括号会导致误判），只应作为非正式的调试启发式方法。

> **【中文解读】** 不能在 `arguments` 完成之前尝试解析。`{"city": "Beng` 这样的部分 JSON 无效，会抛出异常。正确的门控是提供商的调用结束信号（OpenAI 的 `finish_reason`、Anthropic 的 `content_block_stop`、Gemini 的 stream-end）。大括号计数作为完整性测试不可靠，因为引号字符串内的括号或转义内容会导致误判。

### Out-of-order completion

```
call_A: fast API, returns first
call_B: slow API, returns second
call_C: median API, returns third
```

The host reply must still cite the ids:

> 宿主回复仍须引用 id：

```
[{role: "tool", tool_call_id: "call_A", content: ...},
 {role: "tool", tool_call_id: "call_B", content: ...},
 {role: "tool", tool_call_id: "call_C", content: ...}]
```

Order in the reply does not matter for correctness on OpenAI or Anthropic. Gemini accepts any order so long as ids match.

> 回复中的顺序对 OpenAI 或 Anthropic 的正确性无关紧要。Gemini 接受任何顺序，只要 id 匹配。

### Benchmark: sequential vs parallel

The harness in `code/main.py` simulates three executors with 400, 600, and 800 ms latency. Sequential runs it in 1800 ms total. Parallel runs it in max(400, 600, 800) = 800 ms. The difference is constant, not proportional, so the savings grow with tool count.

> `code/main.py` 中的线束模拟三个延迟分别为 400、600 和 800 毫秒的执行器。串行总耗时 1800 毫秒。并行耗时 max(400, 600, 800) = 800 毫秒。差异是恒定的而非比例的，因此工具数量越多节省越多。

Real-world caveat: parallel calls stress downstream APIs. A 10-way fan-out to a rate-limited service will fail. Phase 13 · 17 covers gateway-level backpressure; retry semantics are planned for a future phase.

> 现实注意事项：并行调用会给下游 API 施加压力。10 路扇出到速率受限的服务会失败。Phase 13 · 17 涵盖网关级背压；重试语义计划在未来的 phase 中。

### Streaming fan-out wall-clock

If the model itself streams, you can start executing as soon as one call's arguments are complete, rather than waiting for all calls to finalize. This is an optimization OpenAI documents but not all SDKs expose. The harness in this lesson does it: as soon as the simulated stream yields a complete argument object, the host kicks off that call.

> 如果模型本身是流式的，你可以在一个调用的参数完成后立即开始执行，而不必等待所有调用完成。这是 OpenAI 记录的一种优化，但并非所有 SDK 都暴露了这个能力。本课的线束做到了这一点：一旦模拟流产生完整的参数对象，宿主就启动该调用。

## Use It | 用框架实现

`code/main.py` has two halves. The first runs three simulated weather calls sequentially and in parallel using `concurrent.futures.ThreadPoolExecutor` and prints wall-clock time. The second half replays a fake streaming response — chunks of `arguments` for three parallel calls interleaved on one stream — and reassembles them per-id with `StreamAccumulator`. No LLM, no network, just the reassembly logic.

> `code/main.py` 有两部分。第一部分使用 `concurrent.futures.ThreadPoolExecutor` 顺序和并行运行三个模拟天气调用，并打印挂钟时间。第二部分回放一个假的流式响应——三个并行调用的 `arguments` 块在一个流上交错——并用 `StreamAccumulator` 按 id 重组。不需要 LLM，不需要网络，只是重组逻辑。

What to look at:

> 需要关注的点：

- The sequential timer hits 1.8 seconds. The parallel timer hits 0.8 seconds on the same fake latencies.
  中文翻译：串行计时器达到 1.8 秒。并行计时器在相同假延迟下达到 0.8 秒。
- The accumulator handles chunks arriving out of order by buffering per-id and parsing only when each call's JSON is complete.
  中文翻译：累加器通过按 id 缓冲乱序到达的块来处理，只在每个调用的 JSON 完成时才解析。
- The executor kicks off as soon as an id's arguments finalize, not after all streams end.
  中文翻译：执行器在一个 id 的参数完成后立即启动，而非所有流结束后。

## Ship It | 产出物

This lesson produces `outputs/skill-parallel-call-safety-check.md`. Given a tool registry, the skill audits which tools are safe to parallelize, which have ordering dependencies, and which would overwhelm downstream rate limits — returning a revised registry with per-tool `parallel_safe` flags.

> 本课产出 `outputs/skill-parallel-call-safety-check.md`。给定一个工具注册表，该 skill 审计哪些工具可以安全地并行化、哪些有顺序依赖、哪些会使下游速率限制不堪重负——返回一个带有每个工具 `parallel_safe` 标志的修订注册表。

## Exercises | 练习题

1. Run `code/main.py` and vary the simulated latencies. Confirm that the parallel-to-sequential ratio is approximately `max/sum` (real runs deviate slightly from the ideal because of thread scheduling, serialization, and harness overhead). At what latency distribution does parallel stop mattering?
   中文翻译：运行 `code/main.py` 并改变模拟延迟。确认并行与串行比率约为 `max/sum`（实际运行因线程调度、序列化和线束开销与理想值略有偏差）。在什么延迟分布下并行不再有意义？

2. Extend the accumulator to handle a "call was cancelled mid-stream" case by dropping its buffer and emitting a `cancelled` event. What provider documents this case explicitly? Check Anthropic's `content_block_stop` semantics and OpenAI's `finish_reason: "length"` behavior.
   中文翻译：扩展累加器以处理"调用在流中途被取消"的情况，丢弃其缓冲区并发出 `cancelled` 事件。哪个供应商明确记录了这种情况？检查 Anthropic 的 `content_block_stop` 语义和 OpenAI 的 `finish_reason: "length"` 行为。

3. Replace the thread pool with `asyncio.gather`. Benchmark both. You should see small wins on async because of lower context-switch cost, but only if executors do real I/O.
   中文翻译：用 `asyncio.gather` 替换线程池。对两者进行基准测试。你应该看到异步有小的优势，因为上下文切换成本更低，但前提是执行器做真正的 I/O。

4. Pick two tools that should NOT parallelize (e.g. `create_file` then `write_file`). Add an `ordering_dependency` graph to the registry and gate the parallel fan-out on that graph. This is the minimum machinery for dependency-aware scheduling, which a future agent-engineering phase formalizes.
   中文翻译：选择两个不应该并行化的工具（如 `create_file` 然后 `write_file`）。在注册表中添加 `ordering_dependency` 图，并基于该图门控并行扇出。这是依赖感知调度的最小机制，未来的 agent 工程 phase 会将其形式化。

5. Read OpenAI's parallel-function-calling section and Anthropic's `disable_parallel_tool_use` docs. Identify the one real-world tool type where Anthropic recommends disabling parallelism. (Hint: consequential mutations on the same resource.)
   中文翻译：阅读 OpenAI 的并行函数调用章节和 Anthropic 的 `disable_parallel_tool_use` 文档。找出 Anthropic 建议禁用并行的一种真实工具类型。（提示：对同一资源的后果性修改。）

## Key Terms | 术语速查表

| Term | What people say | What it actually means | 中文术语 |
|------|----------------|------------------------|----------|
| Parallel tool calls | "Fan-out in one turn" | Model emits multiple tool calls in a single assistant message | 并行工具调用 |
| `parallel_tool_calls` | "OpenAI's flag" | Enable or disable multi-call emission | OpenAI 并行调用开关 |
| `disable_parallel_tool_use` | "Anthropic's inverse" | Opt-out flag; default is parallel enabled | Anthropic 并行禁用开关 |
| Tool call id | "Correlation handle" | Per-call identifier the result message must echo | 工具调用标识符 |
| Accumulator | "Stream buffer" | Per-id string buffer for partial `arguments` chunks | 流式累加器 |
| Out-of-order completion | "Fastest first" | Parallel calls finish in unpredictable order; ids are the glue | 乱序完成 |
| Dependency graph | "Ordering constraints" | Tools whose outputs feed into inputs of other tools; cannot parallelize | 依赖图 |
| Parse-early trap | "JSON.parse exploded" | Attempting to parse an incomplete `arguments` string | 过早解析陷阱 |
| `streamFunctionCallArguments` | "Gemini 3 feature" | Streamed argument chunks with unique id per call | Gemini 3 流式参数 |
| Completion-order reply | "Don't wait for all" | Reply with results as they arrive, keyed by id | 按完成顺序回复 |

## Further Reading | 延伸阅读

- [OpenAI — Parallel function calling](https://platform.openai.com/docs/guides/function-calling#parallel-function-calling) — default behavior and the opt-out flag
  中文翻译：默认行为和退出标志
- [Anthropic — Tool use: implementing tool use](https://docs.anthropic.com/en/docs/agents-and-tools/tool-use/implementing-tool-use) — `disable_parallel_tool_use` and result batching
  中文翻译：`disable_parallel_tool_use` 和结果批处理
- [Google — Gemini function calling parallel section](https://ai.google.dev/gemini-api/docs/function-calling) — id-correlated parallel calls from Gemini 3
  中文翻译：Gemini 3 的 id 关联并行调用
- [OpenAI — Streaming responses with tools](https://platform.openai.com/docs/api-reference/responses-streaming) — chunked argument reassembly for OpenAI streams
  中文翻译：OpenAI 流的分块参数重组
- [Anthropic — Streaming messages](https://docs.anthropic.com/en/api/messages-streaming) — `content_block_delta` with `input_json_delta`
  中文翻译：带 `input_json_delta` 的 `content_block_delta`
