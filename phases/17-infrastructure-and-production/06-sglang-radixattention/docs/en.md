# SGLang and RadixAttention for Prefix-Heavy Workloads | 注意力 SGLang Radix PR

> SGLang treats the KV cache as a first-class, reusable resource stored in a radix tree. Where vLLM schedules requests FCFS (first-come, first-served), SGLang's cache-aware scheduler prioritizes requests with longer shared prefixes — effectively a depth-first radix traversal so hot branches stay resident in HBM. On Llama 3.1 8B with ShareGPT-like 1K prompts, SGLang hits ~16,200 tok/s to vLLM's ~12,500, a ~29% edge. On prefix-heavy RAG workloads the advantage reaches 6.4x. On voice-cloning-shaped workloads cache hit rate cleared 86%. Deployed on 400,000+ GPUs in 2026 across xAI, LinkedIn, Cursor, Oracle, GCP, Azure, AWS. The gotcha is that the 6.4x number evaporates when prefix ordering is inconsistent — ordering is the engineer's lever.

> **【中文解读】** 本节介绍了 SGLang 和 RadixAttention——通过前缀共享优化推理效率。


**Type:** Learn
**Languages:** Python (stdlib, toy radix-tree cache + cache-aware scheduler)
**Prerequisites:** Phase 17 · 04 (vLLM Serving Internals), Phase 14 (Agentic RAG)
**Time:** ~75 minutes

## Learning Objectives | 学习目标

- Diagram RadixAttention: how prefixes are stored in a radix tree and how KV blocks are shared across sequences rooted at the same branch.
- Explain cache-aware scheduling and why FCFS is wrong for prefix-heavy traffic.
- Compute expected speedup for a workload given prefix-cache hit rate and prompt length distribution.
- Name the prompt-ordering discipline that makes the 6.4x number real vs a lost upside.

## The Problem | 问题

> **【中文解读】** 传统推理服务将每个请求的 prompt 视为不透明的——即使 5000 个 RAG 请求共享相同的 2000-token 系统提示，vLLM 也会执行 5000 次完整的 prefill。RadixAttention 通过将 token 序列存储在 radix tree 中解决此问题：新请求沿树匹配已有前缀，只需 prefill 新增的后缀部分。挑战在于调度——FCFS（先来先服务）会破坏前缀局部性，需要 cache-aware 调度器优先服务共享长前缀的请求。

> **【拓展：前缀共享在 Agent 场景的价值】** Agent 工作负载天然具有前缀共享特征：系统提示、工具 schema、few-shot 示例、对话历史跨请求重复。Cursor（AI 代码编辑器）在 2026 年报告其 Agent 调用中系统提示 + 工具定义占 prompt 的 80%，仅用户查询部分不同。使用 SGLang 的 RadixAttention 后，这些共享前缀只需计算一次，后续请求复用 KV Cache，将推理成本降低 60-80%。

Classic serving treats each request's prompt as opaque. Even when 5,000 RAG requests all start with the same 2,000-token system prompt plus same retrieval preamble, vLLM prefills that 2,000-token prefix 5,000 times. The GPU does the same work over and over.

The observation: prompts in agentic and RAG workloads share long prefixes almost always. System prompt, tool schemas, few-shot examples, retrieval headers, conversation history — all repeat across requests. If you stored the KV cache for that prefix once and reused it, you would not prefill it again.

RadixAttention does exactly this. Tokens are indexed in a radix tree; each node owns KV blocks for the token sequence on its path from root. A new request walks the tree: any node whose token matches re-uses that node's KV blocks. Prefill cost becomes proportional to the "new" suffix, not the full prompt.

The challenge is scheduling. If two requests share a 2,000-token prefix and a third shares only 200 tokens of the same prefix, you want to serve the two long-shared requests together so the long prefix stays in HBM. FCFS does the opposite — it serves whoever arrived first, potentially evicting the hot branch before the next long-prefix request hits.

## The Concept | 概念

### The radix tree as a KV index

> **【中文解读】** Radix tree（紧凑前缀树）是 SGLang 的核心数据结构。每个节点拥有一个 token 范围和对应的 KV 块。新请求进入时沿树匹配：系统提示匹配节点复用 124 个 KV 块，文档分支匹配复用 31 个块，只需为新问题分配 4-6 个块。以 160 个总块为例，radix tree 只需 4 块新计算（40x 节省）。这不仅是内核技巧，更是调度策略——SGLang 的 cache-aware 调度器优先路由到热点分支，保持前缀在 HBM 中常驻。

A radix tree (compact trie) stores token sequences. Each node owns a token range and the KV blocks computed for that range. Children extend the sequence one or more tokens.

```
root
 |- "You are a helpful assistant..."  (2,000 tokens, 124 KV blocks)
      |- "Context: <doc A>..."        (500 tokens, 31 blocks)
           |- "Question: Alice..."    (80 tokens, 5 blocks)
           |- "Question: Bob..."      (95 tokens, 6 blocks)
      |- "Context: <doc B>..."        (520 tokens, 33 blocks)
```

A new request comes in with system prompt + "Context: <doc A>" + "Question: Carol". The scheduler walks: system prefix matches (124 blocks reused), doc-A branch matches (31 blocks reused), then allocates fresh blocks only for "Question: Carol" (4 blocks). Prefill cost: 4 blocks of new tokens. Without the tree: 160 blocks. ~40x savings on prefill.

### Cache-aware scheduling

> **【中文解读】** 缓存感知调度的两个关键策略：(1) 深度优先调度——优先服务与当前运行集共享分支的请求，保持热点分支常驻 HBM；(2) 分支级 LRU 淘汰——以整棵分支为单位淘汰（从最少使用的叶子开始），而非单个块。FCFS 违反这两个策略——一个共享 2000 token 的请求可能排在共享 50 token 的请求后面，导致长前缀分支被淘汰。

Radix-tree-backed reuse is pointless if the cache churns. Two key policies:

1. **Depth-first dispatch**. When picking the next request from the queue, prefer requests rooted at the same branch as the current running set. This keeps the hot branch pinned.
2. **LRU at branch level, not block level**. Evict whole branches (starting from shortest-used leaves) rather than individual blocks, so cache shape matches radix shape.

FCFS violates both. A request sharing 2,000 tokens sits behind a request sharing 50, then the 2,000-token branch gets evicted to admit the 50-token one.

### Benchmark numbers you should memorize

- Llama 3.1 8B, H100, ShareGPT 1K prompts: SGLang ~16,200 tok/s vs vLLM ~12,500 (~29% edge).
- Prefix-heavy RAG (same system + same doc, varying question): up to 6.4x on SGLang.
- Voice cloning workloads: 86.4% prefix-cache hit rate.
- Production hit rates across SGLang customers: 50-99% depending on prompt discipline.
- Deployed on 400,000+ GPUs in 2026.

### The ordering gotcha

> **【中文解读】** 6.4x 加速依赖于一致的提示模板排序。如果客户端有时构造 `[system, tools, context, history, question]`，有时构造 `[system, context, tools, history, question]`，radix tree 无法找到共享前缀——对人类看起来相同的提示，对 radix tree 是两条不同的序列。工程师的关键杠杆是：将提示模板视为缓存键。将不可变内容（系统提示、工具 schema）放最前，检索上下文居中，用户问题放最后。一次模板排序调整就曾将缓存命中率从 7% 提升到 74%。

> **【拓展：SGLang 在生产中的采用】** SGLang 在 2026 年已部署在超过 40 万块 GPU 上，用户包括 xAI（Grok）、LinkedIn、Cursor、Oracle，以及 GCP/Azure/AWS 的托管服务。核心优势场景是 Agent 和 RAG 工作负载——这些场景中系统提示和工具定义的重复率极高。SGLang 团队由 UC Berkeley LMSYS（Chatbot Arena 的创建者）成员组成，与 vLLM 团队有密切合作。两者不是严格竞争关系——vLLM 也在 2026 年添加了 prefix caching 功能。

The 6.4x number relies on consistent prompt-template ordering. If your client constructs prompts as `[system, tools, context, history, question]` in some requests and `[system, context, tools, history, question]` in others, the tree cannot find the shared prefix. What looks like a shared prefix to a human is two distinct sequences to the radix tree.

Engineer's lever: your prompt template is a cache key. Fix the order. Put everything immutable (system, tools, schemas) first. Put retrieval context next. Put user question last. Do not interleave dynamic content into the prefix.

Real case from the research: moving dynamic content out of the cacheable prefix took one deployment from 7% to 74% cache hit rate in one change.

### Where RadixAttention wins and loses

> **【拓展：RadixAttention vs Prefix Caching 性能对比】** SGLang 与 vLLM 的前缀缓存性能对比：在 Llama 3.1 8B H100 上，通用 ShareGPT 工作负载中 SGLang 达到 ~16,200 tok/s vs vLLM ~12,500 tok/s（29% 优势）；在重度前缀复用的 RAG 工作负载中优势可达 6.4x；语音克隆工作负载缓存命中率 86%。但 vLLM 在 2026 年也添加了 prefix caching 和 cache-aware router（Rust 实现）——差距缩小但未完全消除，因为 SGLang 的整个栈都是 radix-first 设计。

Wins:
- RAG (same retrieval preamble, varying question).
- Agents (same tool schemas, varying query).
- Chat with long system prompt.
- Voice / vision workloads with repeated preambles.

Loses (returns to vLLM-level throughput):
- Single-shot generation with unique prompts (code completion, open-ended chat without system prompt).
- Dynamic prompts where every request interleaves unique content into the prefix.

### Why this is a scheduler problem, not just a kernel problem

You can implement KV reuse as a kernel trick. SGLang's insight is that reuse only pays if the scheduler keeps the hot branch resident. A naive "reuse if available" policy will churn the cache under mixed load. The radix-tree-indexed scheduler is what turns the kernel trick into a 29% production edge.

### Interplay with vLLM

The two systems are not strict competitors. In 2026 vLLM added prefix caching (`--enable-prefix-caching`) and a cache-aware router (vLLM Router in Rust). The gap closed but did not fully disappear — SGLang's whole stack is radix-first; vLLM grafted it on. For workloads dominated by prefix reuse, SGLang remains the default. For general-purpose serving without strong prefix patterns, vLLM remains equal or better.

## Use It | 使用方法

`code/main.py` implements a toy radix-tree KV cache plus a scheduler with two policies: FCFS and cache-aware. Runs the same workload through both, reports prefix-cache hit rate and throughput delta. Then runs a "scrambled ordering" workload to show the 6.4x collapse.

## Ship It | 部署上线

> **【拓展：前缀缓存策略选择】** 2026 年前缀缓存有三个层面：(1) 应用级语义缓存（Phase 17·14）——在调用 LLM 前用嵌入相似度匹配历史响应，命中率 10-70%；(2) 服务端前缀缓存（SGLang RadixAttention / vLLM prefix caching）——复用 KV Cache，10x 延迟降低；(3) 跨节点缓存路由（Phase 17·11）——通过 cache-aware router 将请求路由到持有前缀的副本。三者可以叠加：语义缓存避免 LLM 调用 → 服务端前缀缓存避免重复 prefill → 跨节点路由避免请求错配。

This lesson produces `outputs/skill-radix-scheduler-advisor.md`. Given a workload description (prompt-template shape, retrieval pattern, number of concurrent tenants), it produces a prompt-ordering prescription and a go/no-go for SGLang adoption.

## Exercises | 练习题

1. Run `code/main.py`. Compare FCFS and cache-aware on the same workload. Where does the delta come from — prefill savings, decode savings, or queue delay?
2. Modify the workload so prompts randomly permute `[system, tools, context]`. Re-run. What happens to hit rate? Why?
3. Compute the HBM cost of keeping a 2,000-token system prompt resident as one radix branch on Llama 3.1 8B. Compare to the cost of a 16-sequence batch without prefix reuse.
4. Read the SGLang RadixAttention paper. Explain in three sentences why tree-shaped LRU eviction beats block-shaped LRU under prefix-heavy load.
5. A customer reports only 8% cache hit rate. Name three likely causes and the diagnostic you would run for each.

## Key Terms | 关键术语

| Term | What people say | What it actually means |
|------|----------------|------------------------|
| RadixAttention | "the SGLang thing" | KV cache indexed as a radix tree so shared prefixes reuse blocks |
| Radix tree | "compact trie" | Tree where each node owns a token range and its KV blocks |
| Cache-aware scheduler | "hot-branch-first" | Scheduler that prefers requests sharing the resident branch |
| Prefix-cache hit rate | "how much of your prompt was free" | Fraction of prompt tokens served from reused KV blocks |
| FCFS | "first-come first-served" | Default scheduling that breaks prefix locality |
| Branch-level LRU | "evict the leaf" | Eviction policy matched to radix shape |
| Prompt template ordering | "the cache key" | The prompt's component order determines what the tree can share |
| System prompt pinning | "resident prefix" | Keep the immutable system portion pinned to avoid eviction thrash |

## Further Reading | 延伸阅读

- [SGLang GitHub](https://github.com/sgl-project/sglang) — source and docs.
- [SGLang documentation](https://sgl-project.github.io/) — RadixAttention and scheduling details.
- [SGLang paper — Efficiently Programming Large Language Models (arXiv:2312.07104)](https://arxiv.org/abs/2312.07104) — the design reference.
- [LMSYS blog — SGLang with RadixAttention](https://www.lmsys.org/blog/2024-01-17-sglang/) — benchmark numbers and scheduler rationale.
- [vLLM — Prefix Caching](https://docs.vllm.ai/en/latest/features/prefix_caching.html) — vLLM's own radix-like implementation, for comparison.
