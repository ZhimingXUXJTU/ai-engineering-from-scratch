# Batch APIs — the 50% Discount as Industry Standard | 批处理 API 美国

> Every major provider ships an async batch API with a 50% discount and ~24-hour turnaround. OpenAI, Anthropic, Google, and most of the inference platforms (Fireworks batch tier, Together batch) implement the same pattern. Stack batch with prompt caching and overnight pipelines drop to ~10% of synchronous-uncached cost. The rule is brutally simple: if it is not interactive, it belongs on batch. Content generation pipelines, document classification, data extraction, report generation, bulk labeling, catalog tagging — anything tolerant of 24-hour latency is money left on the table until it moves to batch. The 2026 production pattern is to triage every new LLM workload into three lanes: interactive (synchronous with caching), semi-interactive (async queue with fallback), batch (overnight, cached input stacked). Workloads that pretend to be interactive but tolerate minutes of latency waste most.

> **【中文解读】** 本节介绍了批处理 API——大规模异步处理 LLM 请求的接口和优化。


**Type:** Learn
**Languages:** Python (stdlib, toy batch-vs-sync cost simulator)
**Prerequisites:** Phase 17 · 14 (Prompt & Semantic Caching)
**Time:** ~45 minutes

## Learning Objectives | 学习目标

- Name the three provider batch APIs (OpenAI, Anthropic, Google) and the common 50% discount + 24h turnaround guarantees.
- Compute the cost for stacking batch + cached-input on an overnight classification workload and compare to synchronous-uncached baseline.
- Triage a workload into interactive / semi-interactive / batch and justify the lane.
- Name the two traps: partial interactivity (user expects faster than 24h) and output-schema drift (batch file format differs per provider).

## The Problem | 问题

> **【中文解读】** 批处理 API 是 LLM 成本工具箱中最便宜的杠杆——每个主要提供商都提供 50% 折扣 + 24 小时周转的异步批处理接口。叠加缓存后，隔夜工作负载可降至同步-未缓存成本的约 10%。但大多数团队不使用它——原因是组织性的：团队认为"实时"处理，而 SLA 实际上是"到早上"。

> **【拓展：三大提供商的批处理 API】** 2026 年三大 LLM 提供商的批处理接口：(1) OpenAI Batch API——JSONL 文件上传，/v1/batches 端点，50% 折扣，实际周转 2-8 小时；(2) Anthropic Message Batches——JSONL 上传，支持 cache_control，50% 折扣；(3) Google Vertex AI Batch Prediction——BigQuery 或 GCS 输入，Gemini 50% 折扣。文件格式各不相同，跨提供商的统一批处理客户端需要适配器代码。Portkey 和 LiteLLM 的部分层级提供多提供商批处理的薄封装。

Your team ships a nightly report generation pipeline. 50,000 documents, summarize each, cluster the summaries, draft an executive brief. Running synchronously it takes 4 hours at $2,000/night. You hear about batch APIs.

The batch gets you 50% off. You also enable prompt caching on the system prompt (shared across all 50k calls). Stacked, the bill drops to $180/night — ~9% of baseline. Same pipeline, three config changes.

Batch is the cheapest lever in the LLM cost toolkit that nobody pulls. The reason is mostly organizational: teams think "real-time" when the SLA actually is "by morning." This lesson is about not leaving 90% of the bill on the table.

## The Concept | 概念

### The three batch APIs

**OpenAI Batch API**: JSONL file upload with a list of requests. Promised 24-hour turnaround (usually ~2-8 hours in practice). 50% discount on input and output tokens. `/v1/batches` endpoint. Cache-eligible inputs also get cached-input pricing on top.

**Anthropic Message Batches**: JSONL upload. 24-hour turnaround. 50% discount. Supports `cache_control` — cache writes are explicit, reads happen automatically within the batch.

**Google Vertex AI Batch Prediction**: BigQuery or GCS input. Similar 50% discount for Gemini. Integrates with Vertex pipelines.

### Semantic: asynchronous, not slow

Batch is "I promise to return within 24 hours" — not "this will take 24 hours." Typical P50 is 2-6 hours. Provider schedules your batch during off-peak windows when GPU inventory is underutilized.

### Stack with caching

> **【拓展：批处理 + 缓存的叠加经济模型】** 批处理 + 缓存叠加的具体经济模型：50K 文档摘要任务，共享 4K-token 系统提示。同步未缓存：50000 × ($input × 4000 + $output × 200) 全价；同步+缓存：系统提示首次写入后，后续 49999 次享受约 10x 更便宜的输入；批处理+缓存：上述所有基础上再加 50% 折扣。最终结果：批处理 + 缓存 = 同步未缓存成本的约 10%。任何隔夜运行且共享系统提示的工作负载都应使用这个组合。

A 50k-document summarization with the same 4K-token system prompt:

- Synchronous uncached: 50000 × ($input × 4000 + $output × 200) at full rates.
- Synchronous cached: system prompt cached after first write; remaining 49999 get 10x cheaper input.
- Batch cached: all of the above plus 50% discount on both read and write.

The stack: batch + cache = ~10% of sync uncached bill. Any workload that runs overnight and has a shared system prompt should use this.

### Workload triage

> **【中文解读】** 工作负载分诊是使用批处理 API 的前提。三条车道：(1) 交互式（用户等待响应）——TTFT 重要，必须同步调用+提示缓存；(2) 半交互式（用户提交任务，几分钟后回来查看）——异步队列+同步后备；(3) 批处理（用户期望"明早"或"一小时后"）——内容流水线、大规模分类、离线分析，必须批处理+叠加缓存。常见错误是将所有工作负载标记为"交互式"，仅仅因为流水线是生产级的。

> **【拓展：批处理 API 的陷阱】** 批处理 API 有两个常见陷阱：(1) 部分交互性——用户期望比 24 小时更快（如带有"刷新"按钮的夜间报告），团队错误地使用同步调用；(2) 输出 schema 漂移——不同提供商的批处理文件格式不同（OpenAI JSONL、Anthropic JSONL、Vertex BigQuery/TFRecord），编写"一个批处理客户端"需要每个提供商的适配器代码。

**Interactive** — user waits for the response. TTFT matters. Synchronous call with prompt caching. Cannot batch.

**Semi-interactive** — user submits a task, checks back in minutes. Async queue with fallback to sync if batch not available. Think moderate-volume RAG indexing.

**Batch** — user expects results "by morning" or "next hour." Content pipelines, classification at scale, offline analysis. Always batch, always stack caching.

Common mistake: classifying everything as interactive because the pipeline is production. Production is not a latency spec — SLA is.

### The partial-interactivity trap

Some features look interactive but tolerate 5-10 minutes. Example: a nightly customer health report with "refresh" button. User clicks refresh; wait 10 minutes is fine. Team ships it as synchronous. 50 concurrent refreshes cost 10x what batched-and-delivered-via-email would cost.

The question to ask: "What does 24-hour mean for this user?" If the answer is "they wouldn't notice," batch it.

### The output-schema trap

Batch file formats differ per provider:

- OpenAI: JSONL, one request per line.
- Anthropic: JSONL, one message per line; response format embedded.
- Vertex: BigQuery table or GCS prefix with TFRecord.

Writing "one batch client" across providers means adapter code per provider. Gateways that advertise multi-provider batch (Portkey, LiteLLM some tiers) still thin-wrap the raw format.

### Numbers you should remember

- Batch discount across providers: 50% flat on input + output.
- Turnaround SLA: 24 hours guaranteed, 2-6 hours typical P50.
- Stacked batch + cached input: ~10% of sync uncached cost.
- Workload triage rule: if 24h latency acceptable, always batch.

## Use It | 使用方法

`code/main.py` computes costs across sync, sync+cache, batch, and batch+cache for a 50k-document workload. Reports savings in $ and percent.

## Ship It | 部署上线

This lesson produces `outputs/skill-batch-triager.md`. Given workload characteristics, triages into interactive/semi/batch and estimates savings.

## Exercises | 练习题

1. Run `code/main.py`. For a 100k-doc pipeline with 3K-token system prompt and 500-token output, compute the savings of full stack (batch + cache) vs sync baseline.
2. Pick three features in a real product you know. Triage each into interactive/semi/batch.
3. A user complains their report took 3 hours. Was that a batch mis-triage or a legitimate interactive? Write the decision criterion.
4. Your batch API return SLA is 24h but P99 is 20 hours. How do you communicate this to the user — what is the downstream system behavior on the edge case?
5. Compute break-even: at what shared-prefix length does batch + cache become cheaper than running overnight on your own reserved GPU?

## Key Terms | 关键术语

| Term | What people say | What it actually means |
|------|----------------|------------------------|
| Batch API | "async discount" | 50% off with 24h turnaround |
| JSONL | "batch format" | One JSON request per line; OpenAI/Anthropic standard |
| Message Batches | "Anthropic batch" | Anthropic's batch API product name |
| Batch prediction | "Vertex batch" | Vertex AI's batch API product |
| Turnaround SLA | "24h promise" | Guarantee, not typical; typical is 2-6h |
| Workload triage | "interactivity decision" | Interactive / semi / batch routing decision |
| Output schema | "response format" | Per-provider JSONL layout; not portable |
| Stacked discount | "batch + cache" | ~10% of uncached sync bill when both apply |

## Further Reading | 延伸阅读

- [OpenAI Batch API](https://platform.openai.com/docs/guides/batch) — JSONL format and `/v1/batches` semantics.
- [Anthropic Message Batches](https://docs.anthropic.com/en/docs/build-with-claude/batch-processing) — batch format and `cache_control` interaction.
- [Vertex AI Batch Prediction](https://cloud.google.com/vertex-ai/generative-ai/docs/model-reference/batch-prediction) — Gemini batch semantics.
- [Finout — OpenAI vs Anthropic API Pricing 2026](https://www.finout.io/blog/openai-vs-anthropic-api-pricing-comparison)
- [Zen Van Riel — LLM API Cost Comparison 2026](https://zenvanriel.com/ai-engineer-blog/llm-api-cost-comparison-2026/)
