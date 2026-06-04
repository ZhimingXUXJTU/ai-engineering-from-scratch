# Parallel Tool Calls and Streaming with Tools | 并行工具调用与流式工具

> Three independent weather lookups serialized is three round trips. Run them in parallel and total time collapses to the slowest single call. Every frontier provider now emits multiple tool calls in a single turn. The payoff is real; the plumbing is subtle. This lesson walks both halves: the parallel fan-out and the streamed-argument reassembly, with emphasis on the id-correlation trap.

> **【中文解读】** 三个独立的天气查询串行执行需要三次往返。并行运行后，总时间缩减为最慢的单次调用时间。所有前沿模型提供商现在都支持在单轮中发出多个工具调用。收益是真实的，但管道搭建却很微妙。本课涵盖两个部分：并行扇出和流式参数重组，重点讲解 id 关联陷阱。

> **【拓展：并行调用→Agent 效率优化】** 并行工具调用是 AI Agent 效率的关键优化。当 Agent 需要同时查询多个数据源（如多城市天气、多股票价格）时，并行调用可将延迟降低 60-70%。MCP 协议天然支持并行调用，Claude 的 `disable_parallel_tool_use` 参数和 OpenAI 的 `parallel_tool_calls` 参数都控制这一行为。

**Type:** Build
**Languages:** Python (stdlib, thread pool + streaming harness)
**Prerequisites:** Phase 13 · 02 (function calling deep dive)
**Time:** ~75 minutes

## Learning Objectives

- Explain why `parallel_tool_calls: true` exists and when to disable it.
- Correlate streamed argument chunks to the right tool-call id during parallel fan-out.
- Reassemble partial `arguments` strings into complete JSON without parsing early.
- Run a three-city weather benchmark that demonstrates sequential vs parallel latency.

## The Problem | 问题引入

Without parallel calls, an agent answering "what is the weather in Bengaluru, Tokyo, and Zurich" does this:

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

> **【中文解读】** 没有并行调用时，Agent 回答"Bengaluru、东京和苏黎世的天气如何"需要三次 LLM 往返，每次还要支付执行器延迟，总耗时约为理想时间的 4 倍。

With parallel calls:

```
user -> LLM
LLM -> call get_weather(Bengaluru); call get_weather(Tokyo); call get_weather(Zurich)
host -> run all three executors concurrently, reply with three results
LLM -> final text answer
```

One LLM round trip. Executor time is the maximum of the three, not the sum. Production benchmarks on OpenAI, Anthropic, and Gemini show 60 to 70 percent wall-clock reduction on fan-out workloads.

The price is correlation complexity. When the three calls complete out of order, your results must carry the matching `tool_call_id` so the model can line them up. When results stream, you must assemble partial argument fragments into complete JSON before executing. Gemini 3 added unique ids in part to solve a real-world issue where two parallel calls to the same tool were indistinguishable.

> **【中文解读】** 并行调用的代价是关联复杂性。当三个调用乱序完成时，结果必须携带匹配的 `tool_call_id`，以便模型对齐。流式场景下，必须将部分参数片段组装成完整 JSON 后才能执行。Gemini 3 增加唯一 id 正是为了解决两个同名工具的并行调用无法区分的问题。

## The Concept | 核心概念

### Enabling parallel

> **【拓展：何时禁用并行调用】** 禁用并行调用的典型场景包括：(1) 工具有顺序依赖（如先创建文件再写入）；(2) 一个调用的输出是另一个的输入（如先查用户ID再查订单）；(3) 下游 API 有速率限制，10路扇出会导致 429 错误。在实际生产中，约 30% 的工具调用场景需要串行执行。

- **OpenAI.** `parallel_tool_calls: true` on by default. Set `false` to force serial.
- **Anthropic.** Parallel via `disable_parallel_tool_use: false` (default on Claude 3.5 and up). Set `true` for serial.
- **Gemini.** Always parallel-capable; `tool_config.function_calling_config.mode = "AUTO"` lets the model decide.

Disable parallel when tools have ordering dependencies (`create_file` then `write_file`), when one call's output informs another's input, or when the rate limiter cannot handle fan-out.

> **【中文解读】** 当工具有顺序依赖（先 `create_file` 再 `write_file`）、一个调用的输出影响另一个的输入、或速率限制器无法处理扇出时，应禁用并行。

### Id correlation

Every call the model emits has an `id`. Every result the host returns must include the same id. Without this, results are ambiguous.

- **OpenAI.** `tool_call_id` on each tool-role message.
- **Anthropic.** `tool_use_id` on each `tool_result` block.
- **Gemini.** `id` on each `functionResponse` (Gemini 3 and up; Gemini 2 matched by name which broke for same-name parallel calls).

### Running calls concurrently

The host runs each call's executor on its own thread, coroutine, or remote worker. The simplest harness uses a thread pool; production uses asyncio with `asyncio.gather` or structured concurrency. Order of completion is unpredictable — the id is the identifier.

One common bug: reply with results in call-list order instead of completion order. This usually works because the model only cares about `tool_call_id`, but if a result is dropped or duplicated, out-of-order submission makes debugging harder. Prefer to reply in completion order with explicit ids.

### Streaming tool calls

> **【拓展：流式工具调用的用户体验】** 流式工具调用让用户能看到 Agent 正在"思考"和执行的过程，而非等待一个黑箱操作完成。这对长耗时工具特别有价值——用户可以看到参数逐步构建，提供心理预期。OpenAI 的 ChatGPT 和 Anthropic 的 Claude 都在 UI 中展示了工具调用的流式过程。

When the model streams, `arguments` arrive in pieces. Three separate streams of chunks for three parallel calls interleave on the wire. You need one accumulator per id.

Shape by provider:

- **OpenAI.** Each chunk is `choices[0].delta.tool_calls[i].function.arguments` (partial string). The chunk carries `index` (position in the call list). You accumulate per-index, read `id` when it first appears, and parse JSON when `finish_reason = "tool_calls"`.
- **Anthropic.** Stream events are `message_start`, then one `content_block_start` per block with type `tool_use` (containing id, name, empty input). `content_block_delta` events carry `input_json_delta` chunks. `content_block_stop` closes each block.
- **Gemini.** `streamFunctionCallArguments` (Gemini 3 and up) emits chunks with a `functionCallId` so calls interleave cleanly. Before Gemini 3, streaming returned one complete call at a time.

### Partial JSON and the parse-early trap

You cannot parse `arguments` until it is complete. Partial JSON such as `{"city": "Beng` is not valid and will raise. The correct gate is the provider's end-of-call signal: OpenAI's `finish_reason = "tool_calls"`, Anthropic's `content_block_stop`, or Gemini's stream-end event. Only then attempt `json.loads`. A more robust approach uses an incremental JSON parser that yields events as structure completes; OpenAI's streaming guide recommends this for UX that shows a live "thinking" indicator. Brace-counting is unreliable as a completeness test (braces inside quoted strings or escaped content cause false positives) and should only be used as an informal debug heuristic.

> **【中文解读】** 不能在 `arguments` 完成之前尝试解析。`{"city": "Beng` 这样的部分 JSON 无效，会抛出异常。正确的门控是提供商的调用结束信号（OpenAI 的 `finish_reason`、Anthropic 的 `content_block_stop`、Gemini 的 stream-end）。大括号计数作为完整性测试不可靠，因为引号字符串内的括号或转义内容会导致误判。

### Out-of-order completion

```
call_A: fast API, returns first
call_B: slow API, returns second
call_C: median API, returns third
```

The host reply must still cite the ids:

```
[{role: "tool", tool_call_id: "call_A", content: ...},
 {role: "tool", tool_call_id: "call_B", content: ...},
 {role: "tool", tool_call_id: "call_C", content: ...}]
```

Order in the reply does not matter for correctness on OpenAI or Anthropic. Gemini accepts any order so long as ids match.

### Benchmark: sequential vs parallel

The harness in `code/main.py` simulates three executors with 400, 600, and 800 ms latency. Sequential runs it in 1800 ms total. Parallel runs it in max(400, 600, 800) = 800 ms. The difference is constant, not proportional, so the savings grow with tool count.

Real-world caveat: parallel calls stress downstream APIs. A 10-way fan-out to a rate-limited service will fail. Phase 13 · 17 covers gateway-level backpressure; retry semantics are planned for a future phase.

### Streaming fan-out wall-clock

If the model itself streams, you can start executing as soon as one call's arguments are complete, rather than waiting for all calls to finalize. This is an optimization OpenAI documents but not all SDKs expose. The harness in this lesson does it: as soon as the simulated stream yields a complete argument object, the host kicks off that call.

## Use It | 用框架实现

`code/main.py` has two halves. The first runs three simulated weather calls sequentially and in parallel using `concurrent.futures.ThreadPoolExecutor` and prints wall-clock time. The second half replays a fake streaming response — chunks of `arguments` for three parallel calls interleaved on one stream — and reassembles them per-id with `StreamAccumulator`. No LLM, no network, just the reassembly logic.

What to look at:

- The sequential timer hits 1.8 seconds. The parallel timer hits 0.8 seconds on the same fake latencies.
- The accumulator handles chunks arriving out of order by buffering per-id and parsing only when each call's JSON is complete.
- The executor kicks off as soon as an id's arguments finalize, not after all streams end.

## Ship It | 产出物

This lesson produces `outputs/skill-parallel-call-safety-check.md`. Given a tool registry, the skill audits which tools are safe to parallelize, which have ordering dependencies, and which would overwhelm downstream rate limits — returning a revised registry with per-tool `parallel_safe` flags.

## Exercises | 练习题

1. Run `code/main.py` and vary the simulated latencies. Confirm that the parallel-to-sequential ratio is approximately `max/sum` (real runs deviate slightly from the ideal because of thread scheduling, serialization, and harness overhead). At what latency distribution does parallel stop mattering?

2. Extend the accumulator to handle a "call was cancelled mid-stream" case by dropping its buffer and emitting a `cancelled` event. What provider documents this case explicitly? Check Anthropic's `content_block_stop` semantics and OpenAI's `finish_reason: "length"` behavior.

3. Replace the thread pool with `asyncio.gather`. Benchmark both. You should see small wins on async because of lower context-switch cost, but only if executors do real I/O.

4. Pick two tools that should NOT parallelize (e.g. `create_file` then `write_file`). Add an `ordering_dependency` graph to the registry and gate the parallel fan-out on that graph. This is the minimum machinery for dependency-aware scheduling, which a future agent-engineering phase formalizes.

5. Read OpenAI's parallel-function-calling section and Anthropic's `disable_parallel_tool_use` docs. Identify the one real-world tool type where Anthropic recommends disabling parallelism. (Hint: consequential mutations on the same resource.)

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
- [Anthropic — Tool use: implementing tool use](https://docs.anthropic.com/en/docs/agents-and-tools/tool-use/implementing-tool-use) — `disable_parallel_tool_use` and result batching
- [Google — Gemini function calling parallel section](https://ai.google.dev/gemini-api/docs/function-calling) — id-correlated parallel calls from Gemini 3
- [OpenAI — Streaming responses with tools](https://platform.openai.com/docs/api-reference/responses-streaming) — chunked argument reassembly for OpenAI streams
- [Anthropic — Streaming messages](https://docs.anthropic.com/en/api/messages-streaming) — `content_block_delta` with `input_json_delta`
