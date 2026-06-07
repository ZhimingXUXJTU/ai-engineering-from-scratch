# Prompt Caching and Semantic Caching Economics | 经济学 缓存 PR

> **Pricing snapshot dated 2026-04.** Numeric claims below reflect vendor rate cards captured at this lesson's publication; verify against the linked docs before quoting them downstream.

> **【中文解读】** 本节介绍了提示语义缓存——通过缓存相似提示的响应来降低推理成本。


> Caching happens at two layers. L2 (provider-level) prompt/prefix caching reuses attention KV for repeated prefixes — Anthropic's prompt-caching docs advertise up to 90% cost reduction and 85% latency reduction on long prompts; for Claude 3.5 Sonnet cache reads are $0.30/M vs $3.00/M fresh with a 5-minute TTL and a 2x write premium for the 1-hour TTL option (docs.anthropic.com, 2026-04). OpenAI prompt caching applies automatically for prompts ≥1024 tokens and prices cached input at roughly a 90% discount vs fresh (platform.openai.com, 2026-04); the exact per-model cached rate depends on the live rate card. L1 (app-level) semantic caching skips the LLM entirely on embedding similarity hits. Vendor "95% accuracy" refers to match correctness, not hit rate — reported production hit rates range from 10% (open-ended chat) up to 70% (structured FAQ); neither provider publishes an official baseline, so treat these as community telemetry rather than guarantees. The production pitfalls: parallelization kills caching (N parallel requests issued before the first cache write can inflate spend several-fold), and dynamic content inside the prefix prevents cache hits entirely. ProjectDiscovery reported moving from 7% to 74% hit rate (2025-11) by moving dynamic text out of the cacheable prefix.

**Type:** Learn | **类型:** 学习
**Languages:** Python (stdlib, toy two-layer cache simulator) | **语言:** Python
**Prerequisites:** Phase 17 · 04 (vLLM Serving Internals), Phase 17 · 06 (SGLang RadixAttention) | **前置知识:** Phase 17 · 04 (vLLM Serving Internals), Phase 17 · 06 (SGLang RadixAttention)
**Time:** ~60 minutes | **时间:** ~60 minutes

## Learning Objectives | 学习目标

- Distinguish L2 prompt/prefix caching (KV reuse at provider) from L1 semantic caching (LLM bypass on similar prompts).
  中文翻译：Distinguish L2 prompt/prefix caching (KV reuse at provider) from L1 semantic caching (LLM bypass on similar prompts).
- Explain Anthropic's `cache_control` explicit marking and the two TTL options (5-min vs 1-hour) with their price multipliers.
  中文翻译：Explain Anthropic's `cache_control` explicit marking and the two TTL options (5-min vs 1-hour) with their price multipliers.
- Compute expected monthly savings given hit rate, prompt/response mix, and token prices.
  中文翻译：Compute expected monthly savings given hit rate, prompt/response mix, and token prices.
- Name the parallelization anti-pattern that inflates bills by 5-10x and the dynamic-content anti-pattern that collapses hit rate.
  中文翻译：Name the parallelization anti-pattern that inflates bills by 5-10x and the dynamic-content anti-pattern that collapses hit rate.

## The Problem | 问题引入

> **【中文解读】** 提示缓存有两个常见的失败模式：(1) 并行化反模式——Agent 发出 10 个并行工具调用，所有请求在第一个 cache write 完成前到达，10 次写入、0 次读取，账单膨胀 5-10x；(2) 动态内容反模式——系统提示中包含当前时间、请求 ID 等动态内容，每个请求都唯一，缓存命中率 0%。修复方法：将静态内容放缓存前缀，动态内容放缓存边界之后。

> **【拓展：提示缓存的经济价值】** 提示缓存是 LLM 成本优化中最直接的杠杆。Anthropic 的 cache read 仅 $0.30/M（Claude 3.5 Sonnet），比 fresh input $3.00/M 便宜 10x。OpenAI 对 ≥1024 token 的提示自动缓存，缓存输入约为新鲜输入的 10% 价格。在生产 RAG 系统中，共享系统提示的缓存命中率可达 60-80%，每月可节省数万美元。语义缓存（L1）在结构化 FAQ 场景可达 40-70% 命中率。

You add prompt caching to your RAG service. The bill stays flat. You measure the hit rate; it is 7%. Your prompts look static but they are not — the system prompt includes the current date formatted to the minute, a request ID, and a randomized example reorder for diversity. Every request writes a new cache entry, reads zero.

Separately, your agent runs ten parallel tool calls per user question. All ten arrive at the provider before the first cache write completes. Ten writes, zero reads. Your bill is 5-10x what "with caching" was supposed to cost.

Caching is a protocol, not a flag. Two layers, two different failure modes.

## The Concept | 核心概念

### L2 — provider prompt/prefix caching

> **【中文解读】** L2 层（提供商级）提示缓存复用重复前缀的注意力 KV。Anthropic 使用显式 `cache_control` 标记，TTL 选项有 5 分钟（写入成本 1.25x）和 1 小时（2x），读取成本仅为新鲜输入的 1/10。OpenAI 对 ≥1024 token 提示自动缓存，无需标记。Google Gemini 通过显式 API 提供 context caching。自部署方案使用 vLLM prefix caching 或 SGLang RadixAttention。

Provider stores the attention KV for a cacheable prefix and reuses it on the next request that matches the prefix. You pay a write cost once, reads nearly free.

**Anthropic (Claude 3.5 / 3.7 / 4 series)**: explicit `cache_control` marker in the request. You tag which blocks are cacheable. TTL: 5-minute (write costs 1.25x base) or 1-hour (write costs 2x base). Cache reads: $0.30/M on Claude 3.5 Sonnet vs $3.00/M fresh — 10x cheaper (docs.anthropic.com, as of 2026-04). Rates differ per model (Opus/Haiku published separately); always cross-check the live pricing page.

**OpenAI**: automatic caching for prompts ≥1024 tokens (platform.openai.com, 2026-04). No explicit flag. Cached input is roughly 10x cheaper than fresh on current gpt-4o/gpt-5 rate cards. Neither docs nor release notes publish an official hit-rate baseline; community reports cluster around 30–60% with careful prompt design. Monitor `usage.cached_tokens` to measure your own.

**Google (Gemini)**: context caching via explicit API; 1M-token context means caching pays even more.

**Self-hosted (vLLM, SGLang)**: Phase 17 · 06 covers RadixAttention — same pattern at your own compute.

### L1 — app-level semantic caching

> **【中文解读】** L1 层（应用级）语义缓存在调用 LLM 之前，对提示做哈希和嵌入查找。如果找到相似度超过阈值（通常 0.95+）的缓存请求，直接返回缓存响应。开源实现有 Redis Vector Similarity、GPTCache、Qdrant；商业实现有 Portkey Cache、Helicone Cache。注意：供应商的"95% 准确率"指匹配正确性而非命中率——生产命中率从 10%（开放聊天）到 70%（结构化 FAQ）不等。

Before calling the LLM at all, hash the prompt, embed it, and look for a similar cached request (cosine similarity above threshold, typically 0.95+). On hit, return the cached response. On miss, call LLM and cache the result.

Open-source: Redis Vector Similarity, GPTCache, Qdrant. Commercial: Portkey Cache, Helicone Cache.

Vendor accuracy claims refer to how often the returned cached response was semantically appropriate — not how often you hit. Production hit rates:

- Open-ended chat: 10-15%.
- Structured FAQ / support: 40-70%.
- Code questions: 20-30% (small variants kill hits).
- Voice agents repeating prompts: 50-80% (voice normalization fixed set).

### The parallelization anti-pattern

> **【拓展：并行化反模式的真实案例】** 并行化反模式在生产中的典型表现：Agent 向 Anthropic 发出 10 个并行工具调用，共享同一个 4K-token 系统提示。Anthropic 的 cache write 在约 300ms 后完成，但请求 2-10 在同一毫秒窗口到达，每个都看到 cache miss。结果：10 次写入溢价、0 次读取折扣。修复方法：sequential-first——先单独发送请求 1，等 cache 填充后再发出 2-10。增加 300ms 到第一个工具调用，但节省 5-10x 账单。ProjectDiscovery 通过将动态内容移出缓存前缀，将命中率从 7% 提升到 74%（2025 年 11 月发布案例）。

Your agent makes 10 tool calls in parallel. All 10 have the same 4K-token system prompt. Anthropic cache writes are per-request; the first cache-write completes around 300 ms after the provider sees the prompt. Requests 2-10 arrive in the same millisecond window and each sees cache miss. You pay 10 write premiums, 0 read discounts.

Fix: batch with sequential-first — make request 1 alone, then fire 2-10 once 1's cache has populated. Adds 300 ms to the first tool call; saves 5-10x the bill.

### The dynamic content anti-pattern

Your system prompt looks like:

```
You are a helpful assistant. The current time is 14:32:17.
User ID: abc123. Today is Tuesday...
```

Every request is unique. Every request writes. Zero hits.

Fix: move everything truly static to the cacheable prefix; append dynamic content after the cache boundary:

```
[cacheable]
You are a helpful assistant. [rules, examples, instructions]
[/cacheable]
[dynamic, not cached]
Current time: 14:32:17. User: abc123.
```

ProjectDiscovery moved from 7% to 74% cache hit rate this way and published the anatomy.

### Stack batch + cache for overnight workloads

Batch APIs (Phase 17 · 15) give 50% discount at 24-hour turnaround. Cached input on top gets you ~10x on top of that. Overnight classification, labeling, and report generation workloads can drop to ~10% of synchronous-uncached cost by stacking.

### Numbers you should remember

Pricing points are captured 2026-04 from the linked vendor docs and drift every few months — re-check before relying on them.

- Anthropic cached read: $0.30/M on Claude 3.5 Sonnet, roughly 10x cheaper than fresh input (docs.anthropic.com).
- Anthropic cache write premium: 1.25x (5-min TTL) or 2x (1-hour TTL).
- OpenAI auto-cache: applies to prompts ≥1024 tokens; cached input priced at roughly 10% of fresh input on current rate cards (platform.openai.com).
- Semantic cache hit rate (community-reported): ~10% open chat; up to ~70% structured FAQ. Not a vendor-documented baseline.
- ProjectDiscovery: 7% → 74% hit rate by moving dynamic out of prefix (project blog, 2025-11).
- Parallelization anti-pattern: typical reports of 5–10x bill inflation when N parallel requests miss the first cache write.

## Use It | 用框架实现

`code/main.py` simulates L1 + L2 caching on mixed workloads. Reports hit rates, bill, and shows the parallelization penalty.

> `code/main.py` simulates L1 + L2 caching on mixed workloads. Reports hit rates, bill, and shows the parallelization penalty.

> `code/main.py` simulates L1 + L2 caching on mixed workloads. Reports hit rates, bill, and shows the parallelization penalty.

## Ship It | 产出物

> **【拓展：缓存 + 批处理叠加优化】** 缓存与批处理 API（Phase 17·15）的叠加效果：批处理 API 50% 折扣 + 缓存输入 ~10x 折扣 = 约 10% 的同步-未缓存成本。隔夜分类、标注和报告生成工作负载可以通过叠加这两种优化降至基准的约 10%。关键是将提示模板视为缓存键——修复排序、移出动态内容，这是最容易被忽视但最有效的优化。

This lesson produces `outputs/skill-cache-auditor.md`. Given prompt template and traffic, audits cacheability and recommends restructure.

> 本课产出 `outputs/skill-cache-auditor.md`. Given prompt template and traffic, audits cacheability and recommends restructure.

## Exercises | 练习题

1. Run `code/main.py`. Toggle the parallelization flag. How much does the bill change?
   中文翻译：Run `code/main.py`. Toggle the parallelization flag. How much does the bill change?
2. Your system prompt has a date. Move it out. Show before/after hit rate math.
   中文翻译：Your system prompt has a date. Move it out. Show before/after hit rate math.
3. Calculate break-even for 1-hour TTL (2x write) vs 5-minute TTL (1.25x write) given your request arrival rate.
   中文翻译：Calculate break-even for 1-hour TTL (2x write) vs 5-minute TTL (1.25x write) given your request arrival rate.
4. Semantic cache at 0.95 threshold hits 20%. At 0.85 it hits 50% but you see incorrect cached responses. Pick the right threshold and justify.
   中文翻译：Semantic cache at 0.95 threshold hits 20%. At 0.85 it hits 50% but you see incorrect cached responses. Pick the right threshold and justify.
5. You batch 10 parallel sub-queries per user question. Rewrite for cache-friendliness without adding end-to-end latency.

## Key Terms | 术语速查表

| Term | What people say | What it actually means |
|------|----------------|------------------------|
| L2 prompt cache | "prefix cache" | Provider stores KV for repeated prefix |
| `cache_control` | "Anthropic cache marker" | Explicit attribute marking cacheable blocks |
| Cache write premium | "write tax" | Extra cost for first miss-to-cache (1.25x or 2x) |
| L1 semantic cache | "embedding cache" | App-level hash-and-embed before calling LLM |
| GPTCache | "LLM caching lib" | Popular OSS L1 cache library |
| Cache hit rate | "hits / total" | Fraction of requests served from cache |
| Parallelization anti-pattern | "the N-write trap" | N parallel requests miss cache N times |
| Dynamic content trap | "the time-in-prompt trap" | Dynamic bytes in prefix kill hit rate |
| RadixAttention | "intra-replica cache" | SGLang's prefix-cache implementation |

## Further Reading | 延伸阅读

- [Anthropic Prompt Caching](https://docs.anthropic.com/en/docs/build-with-claude/prompt-caching) — official `cache_control` semantics and TTLs.
- [OpenAI Prompt Caching](https://platform.openai.com/docs/guides/prompt-caching) — automatic caching behavior and eligibility.
- [TianPan — Semantic Caching for LLMs Production](https://tianpan.co/blog/2026-04-10-semantic-caching-llm-production)
- [ProjectDiscovery — Cut LLM Costs 59% With Prompt Caching](https://projectdiscovery.io/blog/how-we-cut-llm-cost-with-prompt-caching)
- [DigitalOcean / Anthropic — Prompt Caching](https://www.digitalocean.com/blog/prompt-caching-with-digital-ocean)
