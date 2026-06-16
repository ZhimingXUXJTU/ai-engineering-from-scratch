# Prompt Caching and Context Caching | 提示缓存与上下文缓存

> Your system prompt is 4,000 tokens. Your RAG context is 20,000 tokens. You send both with every request. You also pay for both — every time. Prompt caching lets the provider keep that prefix warm on their side and bill you 10% of the normal rate on reuse. Used correctly, it cuts inference cost by 50–90% and first-token latency by 40–85%.

> **【中文解读】** 系统提示4000 token + RAG 上下文20000 token，每次请求都要付费。提示缓存让供应商保留前缀，重用时只收10%费用。正确使用可降低50-90%推理成本和40-85%首token延迟。

> **【拓展：提示缓存→RAG生产优化】** Anthropic 的 Prompt Caching 和 OpenAI 的 Cached Response 是 RAG 生产系统降低成本的关键技术，尤其是有固定系统提示和大量检索上下文的场景。

> 🔗 **【前置】** 学本节前请先掌握：Phase 11·01（Prompt Engineering）、Phase 11·05（Context Engineering）、Phase 11·11（Caching Cost）。本节是其延伸，讲 provider 层（Anthropic cache_control、OpenAI 自动缓存、Gemini CachedContent）。

**Type:** Build | **类型:** 构建
**Languages:** Python | **语言:** Python
**Prerequisites:** Phase 11 · 01 (Prompt Engineering), Phase 11 · 05 (Context Engineering), Phase 11 · 11 (Caching and Cost) | **前置知识:** Phase 11 · 01 (提示工程)、05 (上下文工程)、11 (缓存与成本)
**Time:** ~60 minutes | **时间:** ~60 分钟

## The Problem | 问题引入

A coding agent sends the same 15,000-token system prompt to Claude on every turn of a conversation. Twenty turns at $3/M input tokens is $0.90 in input cost alone — before any of the user's actual messages. Multiply by 10,000 daily conversations and the bill hits $9,000/day for text that never changes.

> 一个编程 Agent 在每次对话轮次中发送相同的 15,000 token 系统提示给 Claude。20 轮对话，$3/M 输入 token，仅输入成本就是 $0.90——还不包括用户的实际消息。乘以每天 10,000 次对话，账单达到每天 $9,000。

You cannot shrink the prompt without hurting quality. You cannot avoid sending it — the model needs it on every turn. The only move is to stop paying full price for a prefix the provider has already seen.

> 你不能缩小提示而不损害质量。你不能避免发送它——模型每轮都需要它。唯一的办法是停止为供应商已经见过的前缀支付全价。

> 💡 **【类比】** Prompt caching 像"快递公司记住你的常用地址"——第一次发货要详细说明"北京市朝阳区..."，之后每次发货只需说"老地方"，快递公司自动调出地址。技术上：供应商把 prefix 的 KV cache 存在自己服务器，下次请求来时直接复用，不用重新计算 attention 的 K/V 矩阵。对用户透明——你只需在 API 调用加个 `cache_control` 标记。

> ⚠️ **【易错点】** Prompt caching 的 3 个坑：(1) **prefix 顺序敏感**——cache 命中要求 prefix 完全相同（包括空格、换行），system prompt 末尾多一个空格就 miss；务必把可变部分（用户输入）放最后。(2) **cache TTL 5 分钟**——Anthropic 默认 5 分钟过期，没流量时 cache 失效；用 extended TTL（1 小时）保住冷启动场景。(3) **没监控命中率**——不知道命中率就无法判断收益；Anthropic API response 里有 `cache_creation_input_tokens` 和 `cache_read_input_tokens`，记录到监控面板。

That move is prompt caching. Anthropic shipped it in August 2024 (with a 1-hour extended-TTL variant in 2025), OpenAI automated it later that year, Google shipped explicit context caching alongside Gemini 1.5, and all three now offer it as a first-class feature on their frontier models.

> 这个办法就是提示缓存。Anthropic 在 2024 年 8 月推出了它（2025 年推出了 1 小时扩展 TTL 变体），OpenAI 当年晚些时候自动化了它，Google 在 Gemini 1.5 旁边推出了显式上下文缓存。


> **【中文解读】** Prompt Caching 的价值在于系统 prompt 通常很长（5K+ tokens）且在所有请求中不变。每次请求都重新计算这些 token 的 KV-cache 是巨大的浪费。缓存后，这些 token 的计算成本从 100% 降到接近 0%。


## The Concept | 核心概念

> **【中文解读】** Prompt Caching 利用 LLM 推理的特性——如果多个请求共享相同的 prompt 前缀，可以缓存该前缀的 KV-cache 计算结果，避免重复计算。这对系统 prompt 长且固定的应用（如 RAG、Agent）特别有效。

> **【拓展：Prompt Caching 的成本节省】** Anthropic 的 Prompt Caching 将重复前缀的 input 成本降低约 90%。OpenAI 的类似功能将 cached input 价格降至 $0.50/M tokens（原价 $5）。对系统 prompt 5K tokens + 平均 10 次复用的场景，月成本可降低约 75%。


![Prompt caching: write once, read cheap](../assets/prompt-caching.svg)

**The mechanic.** When a request's prefix matches one from a recent request, the provider serves the KV-cache from the previous run instead of re-encoding the tokens. You pay a small write premium the first time and a large read discount every time after.

> **机制。** 当请求的前缀与最近请求的前缀匹配时，供应商从上次运行中提供 KV-cache，而不是重新编码 token。你第一次支付少量写入溢价，之后每次享受大幅读取折扣。

**Three provider flavors in 2026.**

| Provider | API style | Hit discount | Write premium | Default TTL | Min cacheable |
|---------|-----------|--------------|---------------|-------------|---------------|
| Anthropic | Explicit `cache_control` markers on content blocks | 90% off input | 25% surcharge | 5 min (extendable to 1 hour) | 1,024 tokens (Sonnet/Opus), 2,048 (Haiku) |
| OpenAI | Automatic prefix detection | 50% off input | none | Up to 1 hour (best-effort) | 1,024 tokens |
| Google (Gemini) | Explicit `CachedContent` API | Storage-billed; read at ~25% of normal | Storage fee per token·hour | User-set (default 1 hour) | 4,096 tokens (Flash), 32,768 (Pro) |

**The invariant.** All three cache prefixes only. If any token differs between requests, everything after the first differing token is a miss. Put the *stable* parts at the top, the *variable* parts at the bottom.

> **不变量。** 三者都只缓存前缀。如果请求之间有任何 token 不同，第一个不同 token 之后的所有内容都是未命中。将*稳定*部分放在顶部，*可变*部分放在底部。

### The cache-friendly layout

```
[system prompt]          <-- cache this
[tool definitions]       <-- cache this
[few-shot examples]      <-- cache this
[retrieved documents]    <-- cache if reused, else don't
[conversation history]   <-- cache up to last turn
[current user message]   <-- never cache (different every time)
```

Violate the order — put the user message above the system prompt, interleave dynamic retrievals between few-shots — and the cache never hits.

> 违反顺序——将用户消息放在系统提示之上，在少样本之间穿插动态检索——缓存永远不会命中。

### The break-even calculation

Anthropic's 25% write premium means a cached block has to be read at least twice to net-save money. 1 write + 1 read averages 0.675x cost per request (saves 32%); 1 write + 10 reads averages 0.205x (saves 80%). Rule of thumb: cache anything you expect to reuse at least 3 times within the TTL.

> Anthropic 的 25% 写入溢价意味着缓存块必须被读取至少两次才能净省钱。经验法则：缓存任何你期望在 TTL 内重用至少 3 次的内容。

## Build It | 动手实现

### Step 1: Anthropic prompt caching with explicit markers

```python
import anthropic

client = anthropic.Anthropic()

SYSTEM = [
    {
        "type": "text",
        "text": "You are a senior Python reviewer. Follow the rubric exactly.\n\n" + RUBRIC_15K_TOKENS,
        "cache_control": {"type": "ephemeral"},
    }
]

def review(code: str):
    return client.messages.create(
        model="claude-opus-4-7",
        max_tokens=1024,
        system=SYSTEM,
        messages=[{"role": "user", "content": code}],
    )
```

The `cache_control` marker tells Anthropic to store the block for 5 minutes. Reuse within that window hits; reuse after expires and writes again.

> `cache_control` 标记告诉 Anthropic 将该块存储 5 分钟。在该窗口内重用则命中；过期后重用则重新写入。

**Response usage fields:**

```python
response = review(code_a)
response.usage
# InputTokensUsage(
#     input_tokens=120,
#     cache_creation_input_tokens=15023,   # paid at 1.25x
#     cache_read_input_tokens=0,
#     output_tokens=340,
# )

response_b = review(code_b)
response_b.usage
# cache_creation_input_tokens=0
# cache_read_input_tokens=15023           # paid at 0.1x
```

Check both fields in CI — if `cache_read_input_tokens` stays at zero across requests, your cache keys are drifting.

> 在 CI 中检查这两个字段——如果 `cache_read_input_tokens` 在多次请求中保持为零，你的缓存键正在漂移。

### Step 2: one-hour extended TTL

For long-running batch jobs, the 5-minute default expires between jobs. Set `ttl`:

```python
{"type": "text", "text": RUBRIC, "cache_control": {"type": "ephemeral", "ttl": "1h"}}
```

1-hour TTL costs 2x the write premium (50% over baseline instead of 25%) but pays back fast on any batch reusing the prefix more than 5 times.

> 1 小时 TTL 的写入溢价是 2 倍（基准的 50% 而非 25%），但在任何重用前缀超过 5 次的批处理中很快回本。

### Step 3: OpenAI automatic caching

OpenAI gives you nothing to configure. Any prefix over 1,024 tokens that matches a recent request gets a 50% discount automatically.

```python
from openai import OpenAI
client = OpenAI()

resp = client.chat.completions.create(
    model="gpt-5",
    messages=[
        {"role": "system", "content": SYSTEM_PROMPT},   # long and stable
        {"role": "user", "content": user_msg},
    ],
)
resp.usage.prompt_tokens_details.cached_tokens  # the discounted portion
```

Same cache-friendly layout rule applies. Two things kill OpenAI's cache that don't kill Anthropic's: changing the `user` field (used as a cache key component) and reordering tools.

> 同样的缓存友好布局规则适用。两件事会杀死 OpenAI 的缓存而不会杀死 Anthropic 的：更改 `user` 字段和重新排序工具。

### Step 4: Gemini explicit context caching

Gemini treats the cache as a first-class object you create and name:

```python
from google import genai
from google.genai import types

client = genai.Client()

cache = client.caches.create(
    model="gemini-3-pro",
    config=types.CreateCachedContentConfig(
        display_name="rubric-v3",
        system_instruction=RUBRIC,
        contents=[FEW_SHOT_EXAMPLES],
        ttl="3600s",
    ),
)

resp = client.models.generate_content(
    model="gemini-3-pro",
    contents=["Review this code:\n" + code],
    config=types.GenerateContentConfig(cached_content=cache.name),
)
```

Gemini charges storage per token·hour for as long as the cache lives, and reads at ~25% of normal input rate. This is the right shape when you reuse the same giant prompt across many sessions over days.

> Gemini 按缓存存活期间每 token·小时收取存储费，读取费率约为正常输入的 25%。当你在多个会话中跨天重用相同的大型提示时，这是正确的选择。

### Step 5: measuring hit rate in production

See `code/main.py` for a simulated three-provider accountant that tracks write/read/miss counts and computes blended cost per 1K requests. Gate deploys on a target hit rate — most production Anthropic setups should see >80% read fraction after warmup.

> 见 `code/main.py` 获取模拟的三提供商会计师，跟踪写入/读取/未命中计数并计算每千请求的混合成本。按目标命中率门控部署——多数生产 Anthropic 设置在预热后应见 >80% 读取比例。

## Pitfalls that still ship in 2026

> 2026 年仍在上线的陷阱：

- **Dynamic timestamps at the top.** `"Current time: 2026-04-22 15:30:02"` at the top of the system prompt. Every request misses. Move timestamps below the cache breakpoint.
  **顶部的动态时间戳。** 系统提示顶部放 `"Current time: 2026-04-22 15:30:02"`。每次请求都未命中。把时间戳移到缓存断点之下。
- **Tool reordering.** Serialize tools in a stable order — a dict reshuffle between deploys breaks every hit.
  **工具重排序。** 以稳定顺序序列化工具——部署间的字典重排破坏每次命中。
- **Free-text near-duplicates.** "You are helpful." vs "You are a helpful assistant." — one byte difference = full miss.
  **自由文本近似重复。** "You are helpful." vs "You are a helpful assistant."——一字节差异 = 完全未命中。
- **Too-small blocks.** Anthropic enforces a 1,024-token floor (2,048 for Haiku). Smaller blocks silently do not cache.
  **过小的块。** Anthropic 强制 1,024 token 下限（Haiku 为 2,048）。更小的块静默不缓存。
- **Blind cost dashboards.** Split "input tokens" into cached vs uncached. Otherwise a traffic drop looks like a cache win.
  **盲目的成本仪表板。** 把"输入 token"拆成缓存 vs 未缓存。否则流量下降看起来像缓存赢。

## Use It | 用框架实现

The 2026 caching stack:

> 2026 缓存技术栈：

| Situation | Pick |
|-----------|------|
| Agent with stable 10k+ system prompt, many turns | Anthropic `cache_control` with 5-min TTL |
| Batch job reusing a prefix for 30+ minutes | Anthropic with `ttl: "1h"` |
| Serverless endpoints on GPT-5, no custom infra | OpenAI automatic (just make your prefix stable and long) |
| Multi-day reuse of a giant code/doc corpus | Gemini explicit `CachedContent` |
| Cross-provider fallback | Keep the cacheable prefix layout identical across providers so any hit works |

| 场景 | 选择 |
|------|------|
| Agent 有稳定 10k+ 系统提示、多轮 | Anthropic `cache_control` 配 5 分钟 TTL |
| 批处理重用前缀 30+ 分钟 | Anthropic 配 `ttl: "1h"` |
| GPT-5 上的无服务器端点、无定制基建 | OpenAI 自动（让前缀稳定且够长） |
| 多天重用大型代码/文档语料 | Gemini 显式 `CachedContent` |
| 跨提供商回退 | 跨提供商保持可缓存前缀布局一致，任何命中都工作 |

Combine with semantic caching (Phase 11 · 11) for the user-message layer: prompt caching handles *token-identical* reuse, semantic caching handles *meaning-identical* reuse.

> 与语义缓存（Phase 11 · 11）结合用于用户消息层：提示缓存处理*token 完全相同*的重用，语义缓存处理*语义相同*的重用。

## Ship It | 产出物

Save `outputs/skill-prompt-caching-planner.md`:

```markdown
---
name: prompt-caching-planner
description: Design a cache-friendly prompt layout and pick the right provider caching mode.
version: 1.0.0
phase: 11
lesson: 15
tags: [llm-engineering, caching, cost]
---

Given a prompt (system + tools + few-shot + retrieval + history + user) and a usage profile (requests per hour, TTL needed, provider), output:

1. Layout. Reordered sections with a single cache breakpoint marked; explain which sections are stable, which are volatile.
2. Provider mode. Anthropic cache_control, OpenAI automatic, or Gemini CachedContent. Justify from TTL and reuse pattern.
3. Break-even. Expected reads per write within TTL; net cost vs no-cache with math.
4. Verification plan. CI assertion that cache_read_input_tokens > 0 on the second identical request; dashboard split by cached vs uncached tokens.
5. Failure modes. List the three most likely reasons the cache will miss in this setup (dynamic timestamp, tool reorder, near-duplicate text) and how you will prevent each.

Refuse to ship a cache plan that places a dynamic field above the breakpoint. Refuse to enable 1h TTL without a reuse count that makes the 2x write premium pay back.
```

## Exercises | 练习题

1. **Easy.** Take a 10-turn conversation with a 5,000-token system prompt against Claude. Run it without `cache_control` and then with. Report the input-token bill for each.
   取一个 10 轮对话和 5,000 token 系统提示，不使用和使用 `cache_control` 分别运行，报告输入 token 费用。
2. **Medium.** Write a test harness that, given a prompt template and a request log, computes the expected hit rate and dollar savings per provider (Anthropic 5m, Anthropic 1h, OpenAI automatic, Gemini explicit).
   编写测试工具，给定提示模板和请求日志，计算每个提供商的预期命中率和节省金额。
3. **Hard.** Build a layout optimizer: given a prompt and a list of fields marked `stable=True/False`, rewrite the prompt to put a single cache breakpoint at the maximum cache-friendly position without losing information. Verify on a real Anthropic endpoint.
   构建布局优化器：重写提示将缓存断点放在最大缓存友好位置。

## Key Terms | 术语速查表

| Term | What people say | What it actually means | 中文释义 |
|------|-----------------|-----------------------|---------|
| Prompt caching | "Makes long prompts cheap" / "让长提示变便宜" | Reusing a provider-side KV-cache for matching prefixes; 50-90% discount on repeated input tokens. | 提示缓存：重用供应商端的 KV-cache，对重复输入 token 提供 50-90% 折扣 |
| `cache_control` | "The Anthropic marker" / "Anthropic 标记" | Content-block attribute that declares "everything up to here is cacheable"; `{"type": "ephemeral"}`. | cache_control：内容块属性，声明"到这里为止的内容可缓存" |
| Cache write | "Paying the premium" / "付溢价" | The first request that populates the cache; billed at ~1.25x input rate on Anthropic, free on OpenAI. | 缓存写入：第一次填充缓存的请求 |
| Cache read | "The discount" / "折扣" | Subsequent requests matching the prefix; billed at 10% (Anthropic), 50% (OpenAI), ~25% (Gemini). | 缓存读取：匹配前缀的后续请求 |
| TTL | "How long it lives" / "存活时间" | Seconds the cache stays warm; Anthropic 5m default (extendable 1h), OpenAI best-effort up to 1h, Gemini user-set. | TTL：缓存保持活跃的秒数 |
| Extended TTL | "1-hour Anthropic cache" / "1小时缓存" | `{"type": "ephemeral", "ttl": "1h"}`; 2x write premium but worth it for batch reuse. | 扩展 TTL：1 小时缓存，2 倍写入溢价 |
| Prefix match | "Why my cache missed" / "为什么缓存未命中" | Caches only hit when every token from the start up to the breakpoint is byte-identical. | 前缀匹配：缓存只在从开头到断点的每个 token 完全相同时才命中 |
| Context caching (Gemini) | "The explicit one" / "显式缓存" | Google's named, storage-billed cache object; best for multi-day reuse of large corpora. | 上下文缓存 (Gemini)：命名、按存储计费的缓存对象 |

## Further Reading | 延伸阅读

- [Anthropic — Prompt caching](https://docs.anthropic.com/en/docs/build-with-claude/prompt-caching) — `cache_control`, 1h TTL, break-even tables.
  Anthropic 提示缓存文档——cache_control、1 小时 TTL、盈亏平衡表。
- [OpenAI — Prompt caching](https://platform.openai.com/docs/guides/prompt-caching) — automatic prefix matching.
  OpenAI 提示缓存文档——自动前缀匹配。
- [Google — Context caching](https://ai.google.dev/gemini-api/docs/caching) — `CachedContent` API and storage pricing.
  Google 上下文缓存文档——CachedContent API 和存储定价。
- [Anthropic engineering — Prompt caching for long-context workloads](https://www.anthropic.com/news/prompt-caching) — original launch post with latency numbers.
  Anthropic 工程博客——长上下文工作负载的提示缓存，含延迟数据。
- Phase 11 · 05 (Context Engineering) — where to slice the prompt so the cache can land.
  第 11 阶段 · 05（上下文工程）——在哪里切分提示以便缓存生效。
- Phase 11 · 11 (Caching and Cost) — pair prompt caching with a semantic cache on user messages.
  第 11 阶段 · 11（缓存与成本）——将提示缓存与用户消息的语义缓存配对。
- [Pope et al., "Efficiently Scaling Transformer Inference" (2022)](https://arxiv.org/abs/2211.05102) — the KV-cache memory model that prompt caching exposes to users; explains why a cached prefix is ~10× cheaper to reread than to recompute.
  解释为什么缓存前缀比重算便宜约 10 倍的 KV-cache 内存模型论文。
- [Agrawal et al., "SARATHI: Efficient LLM Inference by Piggybacking Decodes with Chunked Prefills" (2023)](https://arxiv.org/abs/2308.16369) — prefill is the phase prompt caching shortcuts; this paper explains why TTFT drops dramatically on cache hit while TPOT is unaffected.
  解释为什么缓存命中时 TTFT 大幅下降而 TPOT 不受影响的论文。
- [Leviathan et al., "Fast Inference from Transformers via Speculative Decoding" (2023)](https://arxiv.org/abs/2211.17192) — prompt caching sits alongside speculative decoding, Flash Attention, and MQA/GQA as levers that bend the inference cost curve; read this for the other three.
  提示缓存与投机解码、Flash Attention 和 MQA/GQA 并列的推理成本曲线杠杆。
