# SGLang and RadixAttention for Prefix-Heavy Workloads | 注意力 SGLang Radix PR

> SGLang treats the KV cache as a first-class, reusable resource stored in a radix tree. Where vLLM schedules requests FCFS (first-come, first-served), SGLang's cache-aware scheduler prioritizes requests with longer shared prefixes — effectively a depth-first radix traversal so hot branches stay resident in HBM. On Llama 3.1 8B with ShareGPT-like 1K prompts, SGLang hits ~16,200 tok/s to vLLM's ~12,500, a ~29% edge. On prefix-heavy RAG workloads the advantage reaches 6.4x. On voice-cloning-shaped workloads cache hit rate cleared 86%. Deployed on 400,000+ GPUs in 2026 across xAI, LinkedIn, Cursor, Oracle, GCP, Azure, AWS. The gotcha is that the 6.4x number evaporates when prefix ordering is inconsistent — ordering is the engineer's lever.

> **【中文解读】** 本节介绍了 SGLang 和 RadixAttention——通过前缀共享优化推理效率。


**Type:** Learn | **类型:** 学习
**Languages:** Python (stdlib, toy radix-tree cache + cache-aware scheduler) | **语言:** Python（标准库，radix tree 缓存 + 缓存感知调度器模拟）
**Prerequisites:** Phase 17 · 04 (vLLM Serving Internals), Phase 14 (Agentic RAG) | **前置知识:** Phase 17 · 04（vLLM 服务内部）, Phase 14（Agentic RAG）
**Time:** ~75 minutes | **时间:** ~75 分钟

## Learning Objectives | 学习目标

- Diagram RadixAttention: how prefixes are stored in a radix tree and how KV blocks are shared across sequences rooted at the same branch.
  中文翻译：绘制 RadixAttention：前缀如何在 radix tree 中存储，KV 块如何在同分支的序列间共享。
- Explain cache-aware scheduling and why FCFS is wrong for prefix-heavy traffic.
  中文翻译：解释缓存感知调度以及为什么 FCFS 对前缀密集流量是错误的。
- Compute expected speedup for a workload given prefix-cache hit rate and prompt length distribution.
  中文翻译：给定前缀缓存命中率和 prompt 长度分布，计算工作负载的预期加速。
- Name the prompt-ordering discipline that makes the 6.4x number real vs a lost upside.
  中文翻译：说出使 6.4x 加速成为现实而非流失的 prompt 排序纪律。

## The Problem | 问题引入

> **【中文解读】** 传统推理服务将每个请求的 prompt 视为不透明的——即使 5000 个 RAG 请求共享相同的 2000-token 系统提示，vLLM 也会执行 5000 次完整的 prefill。RadixAttention 通过将 token 序列存储在 radix tree 中解决此问题：新请求沿树匹配已有前缀，只需 prefill 新增的后缀部分。挑战在于调度——FCFS（先来先服务）会破坏前缀局部性，需要 cache-aware 调度器优先服务共享长前缀的请求。

> **【拓展：前缀共享在 Agent 场景的价值】** Agent 工作负载天然具有前缀共享特征：系统提示、工具 schema、few-shot 示例、对话历史跨请求重复。Cursor（AI 代码编辑器）在 2026 年报告其 Agent 调用中系统提示 + 工具定义占 prompt 的 80%，仅用户查询部分不同。使用 SGLang 的 RadixAttention 后，这些共享前缀只需计算一次，后续请求复用 KV Cache，将推理成本降低 60-80%。

Classic serving treats each request's prompt as opaque. Even when 5,000 RAG requests all start with the same 2,000-token system prompt plus same retrieval preamble, vLLM prefills that 2,000-token prefix 5,000 times. The GPU does the same work over and over.

> 经典服务将每个请求的 prompt 视为不透明的。即使 5,000 个 RAG 请求都以相同的 2,000 token 系统提示加相同检索前缀开始，vLLM 也会预填充那个 2,000 token 前缀 5,000 次。GPU 重复做同样的工作。

The observation: prompts in agentic and RAG workloads share long prefixes almost always. System prompt, tool schemas, few-shot examples, retrieval headers, conversation history — all repeat across requests. If you stored the KV cache for that prefix once and reused it, you would not prefill it again.

> 观察：Agent 和 RAG 工作负载中的 prompt 几乎总是共享长前缀。系统提示、工具 schema、few-shot 示例、检索头、对话历史——都在请求间重复。如果你存储一次前缀的 KV 缓存并复用，就不需要再次预填充。

RadixAttention does exactly this. Tokens are indexed in a radix tree; each node owns KV blocks for the token sequence on its path from root. A new request walks the tree: any node whose token matches re-uses that node's KV blocks. Prefill cost becomes proportional to the "new" suffix, not the full prompt.

> RadixAttention 正是这样做的。Token 在 radix tree 中索引；每个节点拥有从根到该路径的 token 序列的 KV 块。新请求遍历树：任何 token 匹配的节点复用该节点的 KV 块。预填充成本与"新"后缀成正比，而非完整 prompt。

The challenge is scheduling. If two requests share a 2,000-token prefix and a third shares only 200 tokens of the same prefix, you want to serve the two long-shared requests together so the long prefix stays in HBM. FCFS does the opposite — it serves whoever arrived first, potentially evicting the hot branch before the next long-prefix request hits.

> 挑战在于调度。如果两个请求共享 2,000 token 前缀，第三个只共享 200 token，你希望同时服务两个长共享请求以保持长前缀在 HBM 中。FCFS 做法相反——它先服务先到的请求，可能在下一个长前缀请求到达前淘汰热分支。

## The Concept | 核心概念

### The radix tree as a KV index

> **【中文解读】** Radix tree（紧凑前缀树）是 SGLang 的核心数据结构。每个节点拥有一个 token 范围和对应的 KV 块。新请求进入时沿树匹配：系统提示匹配节点复用 124 个 KV 块，文档分支匹配复用 31 个块，只需为新问题分配 4-6 个块。以 160 个总块为例，radix tree 只需 4 块新计算（40x 节省）。这不仅是内核技巧，更是调度策略——SGLang 的 cache-aware 调度器优先路由到热点分支，保持前缀在 HBM 中常驻。

A radix tree (compact trie) stores token sequences. Each node owns a token range and the KV blocks computed for that range. Children extend the sequence one or more tokens.

> Radix tree（紧凑前缀树）存储 token 序列。每个节点拥有一个 token 范围和为该范围计算的 KV 块。子节点扩展序列一个或多个 token。

```
root
 |- "You are a helpful assistant..."  (2,000 tokens, 124 KV blocks)
      |- "Context: <doc A>..."        (500 tokens, 31 blocks)
           |- "Question: Alice..."    (80 tokens, 5 blocks)
           |- "Question: Bob..."      (95 tokens, 6 blocks)
      |- "Context: <doc B>..."        (520 tokens, 33 blocks)
```

A new request comes in with system prompt + "Context: <doc A>" + "Question: Carol". The scheduler walks: system prefix matches (124 blocks reused), doc-A branch matches (31 blocks reused), then allocates fresh blocks only for "Question: Carol" (4 blocks). Prefill cost: 4 blocks of new tokens. Without the tree: 160 blocks. ~40x savings on prefill.

> 一个新请求带着系统提示 + "Context: <doc A>" + "Question: Carol" 进入。调度器遍历：系统前缀匹配（复用 124 块），doc-A 分支匹配（复用 31 块），然后只为 "Question: Carol" 分配新块（4 块）。预填充成本：4 块新 token。没有树：160 块。预填充节省约 40 倍。

### Cache-aware scheduling

> **【中文解读】** 缓存感知调度的两个关键策略：(1) 深度优先调度——优先服务与当前运行集共享分支的请求，保持热点分支常驻 HBM；(2) 分支级 LRU 淘汰——以整棵分支为单位淘汰（从最少使用的叶子开始），而非单个块。FCFS 违反这两个策略——一个共享 2000 token 的请求可能排在共享 50 token 的请求后面，导致长前缀分支被淘汰。

Radix-tree-backed reuse is pointless if the cache churns. Two key policies:

> 如果缓存不断抖动，radix tree 支持的复用毫无意义。两个关键策略：

1. **Depth-first dispatch**. When picking the next request from the queue, prefer requests rooted at the same branch as the current running set. This keeps the hot branch pinned.
   中文翻译：**深度优先调度**。从队列中选择下一个请求时，优先选择与当前运行集同分支的请求。这保持热分支固定。
2. **LRU at branch level, not block level**. Evict whole branches (starting from shortest-used leaves) rather than individual blocks, so cache shape matches radix shape.
   中文翻译：**分支级 LRU**。淘汰整个分支（从最少使用的叶子开始），而非单个块，使缓存形状匹配 radix 形状。

FCFS violates both. A request sharing 2,000 tokens sits behind a request sharing 50, then the 2,000-token branch gets evicted to admit the 50-token one.

> FCFS 违反两者。一个共享 2,000 token 的请求排在共享 50 token 的请求后面，然后 2,000 token 分支被淘汰以接纳 50 token 的请求。

### Benchmark numbers you should memorize

- Llama 3.1 8B, H100, ShareGPT 1K prompts: SGLang ~16,200 tok/s vs vLLM ~12,500 (~29% edge).
  中文翻译：Llama 3.1 8B，H100，ShareGPT 1K prompt：SGLang 约 16,200 tok/s vs vLLM 约 12,500（约 29% 优势）。
- Prefix-heavy RAG (same system + same doc, varying question): up to 6.4x on SGLang.
  中文翻译：前缀密集 RAG（相同系统 + 相同文档，不同问题）：SGLang 上最高 6.4 倍。
- Voice cloning workloads: 86.4% prefix-cache hit rate.
  中文翻译：语音克隆工作负载：86.4% 前缀缓存命中率。
- Production hit rates across SGLang customers: 50-99% depending on prompt discipline.
  中文翻译：SGLang 客户的生产命中率：50-99%，取决于 prompt 排序纪律。
- Deployed on 400,000+ GPUs in 2026.
  中文翻译：2026 年部署在 400,000+ GPU 上。

### The ordering gotcha

> **【中文解读】** 6.4x 加速依赖于一致的提示模板排序。如果客户端有时构造 `[system, tools, context, history, question]`，有时构造 `[system, context, tools, history, question]`，radix tree 无法找到共享前缀——对人类看起来相同的提示，对 radix tree 是两条不同的序列。工程师的关键杠杆是：将提示模板视为缓存键。将不可变内容（系统提示、工具 schema）放最前，检索上下文居中，用户问题放最后。一次模板排序调整就曾将缓存命中率从 7% 提升到 74%。

> **【拓展：SGLang 在生产中的采用】** SGLang 在 2026 年已部署在超过 40 万块 GPU 上，用户包括 xAI（Grok）、LinkedIn、Cursor、Oracle，以及 GCP/Azure/AWS 的托管服务。核心优势场景是 Agent 和 RAG 工作负载——这些场景中系统提示和工具定义的重复率极高。SGLang 团队由 UC Berkeley LMSYS（Chatbot Arena 的创建者）成员组成，与 vLLM 团队有密切合作。两者不是严格竞争关系——vLLM 也在 2026 年添加了 prefix caching 功能。

The 6.4x number relies on consistent prompt-template ordering. If your client constructs prompts as `[system, tools, context, history, question]` in some requests and `[system, context, tools, history, question]` in others, the tree cannot find the shared prefix. What looks like a shared prefix to a human is two distinct sequences to the radix tree.

> 6.4x 数字依赖于一致的 prompt 模板排序。如果你的客户端在某些请求中构造 `[system, tools, context, history, question]`，在其他请求中构造 `[system, context, tools, history, question]`，树无法找到共享前缀。对人类看起来是共享前缀的，对 radix tree 是两条不同的序列。

Engineer's lever: your prompt template is a cache key. Fix the order. Put everything immutable (system, tools, schemas) first. Put retrieval context next. Put user question last. Do not interleave dynamic content into the prefix.

> 工程师的杠杆：你的 prompt 模板是缓存键。固定顺序。将所有不可变内容（系统、工具、schema）放最前。检索上下文放中间。用户问题放最后。不要在可缓存前缀中交错动态内容。

Real case from the research: moving dynamic content out of the cacheable prefix took one deployment from 7% to 74% cache hit rate in one change.

> 研究中的真实案例：将动态内容移出可缓存前缀，一次部署的缓存命中率从 7% 提升到 74%。

### Where RadixAttention wins and loses

> **【拓展：RadixAttention vs Prefix Caching 性能对比】** SGLang 与 vLLM 的前缀缓存性能对比：在 Llama 3.1 8B H100 上，通用 ShareGPT 工作负载中 SGLang 达到 ~16,200 tok/s vs vLLM ~12,500 tok/s（29% 优势）；在重度前缀复用的 RAG 工作负载中优势可达 6.4x；语音克隆工作负载缓存命中率 86%。但 vLLM 在 2026 年也添加了 prefix caching 和 cache-aware router（Rust 实现）——差距缩小但未完全消除，因为 SGLang 的整个栈都是 radix-first 设计。

Wins:
- RAG (same retrieval preamble, varying question).
  中文翻译：RAG（相同检索前缀，不同问题）。
- Agents (same tool schemas, varying query).
  中文翻译：Agent（相同工具 schema，不同查询）。
- Chat with long system prompt.
  中文翻译：长系统提示的聊天。
- Voice / vision workloads with repeated preambles.
  中文翻译：重复前缀的语音/视觉工作负载。

Loses (returns to vLLM-level throughput):
- Single-shot generation with unique prompts (code completion, open-ended chat without system prompt).
  中文翻译：独立 prompt 的单次生成（代码补全、无系统提示的开放聊天）。
- Dynamic prompts where every request interleaves unique content into the prefix.
  中文翻译：每个请求在可缓存前缀中交错独特内容的动态 prompt。

### Why this is a scheduler problem, not just a kernel problem

You can implement KV reuse as a kernel trick. SGLang's insight is that reuse only pays if the scheduler keeps the hot branch resident. A naive "reuse if available" policy will churn the cache under mixed load. The radix-tree-indexed scheduler is what turns the kernel trick into a 29% production edge.

> 你可以将 KV 复用实现为内核技巧。SGLang 的洞察是复用只有在调度器保持热分支常驻时才有价值。朴素的"有则复用"策略在混合负载下会抖动缓存。radix tree 索引的调度器将内核技巧转化为 29% 的生产优势。

### Interplay with vLLM

The two systems are not strict competitors. In 2026 vLLM added prefix caching (`--enable-prefix-caching`) and a cache-aware router (vLLM Router in Rust). The gap closed but did not fully disappear — SGLang's whole stack is radix-first; vLLM grafted it on. For workloads dominated by prefix reuse, SGLang remains the default. For general-purpose serving without strong prefix patterns, vLLM remains equal or better.

> 两个系统不是严格竞争者。2026 年 vLLM 添加了前缀缓存（`--enable-prefix-caching`）和缓存感知路由器（Rust 实现的 vLLM Router）。差距缩小但未完全消失——SGLang 的整个栈是 radix-first 设计；vLLM 是嫁接上去的。对于前缀复用主导的工作负载，SGLang 仍是默认选择。对于没有强前缀模式的通用服务，vLLM 仍然相当或更好。

## Use It | 用框架实现

`code/main.py` implements a toy radix-tree KV cache plus a scheduler with two policies: FCFS and cache-aware. Runs the same workload through both, reports prefix-cache hit rate and throughput delta. Then runs a "scrambled ordering" workload to show the 6.4x collapse.

> `code/main.py` 实现了一个模拟 radix tree KV 缓存加两个策略的调度器：FCFS 和缓存感知。用两者运行相同工作负载，报告前缀缓存命中率和吞吐量差异。然后运行"乱序排序"工作负载展示 6.4x 崩溃。

## Ship It | 产出物

> **【拓展：前缀缓存策略选择】** 2026 年前缀缓存有三个层面：(1) 应用级语义缓存（Phase 17·14）——在调用 LLM 前用嵌入相似度匹配历史响应，命中率 10-70%；(2) 服务端前缀缓存（SGLang RadixAttention / vLLM prefix caching）——复用 KV Cache，10x 延迟降低；(3) 跨节点缓存路由（Phase 17·11）——通过 cache-aware router 将请求路由到持有前缀的副本。三者可以叠加：语义缓存避免 LLM 调用 → 服务端前缀缓存避免重复 prefill → 跨节点路由避免请求错配。

This lesson produces `outputs/skill-radix-scheduler-advisor.md`. Given a workload description (prompt-template shape, retrieval pattern, number of concurrent tenants), it produces a prompt-ordering prescription and a go/no-go for SGLang adoption.

> 本课产出 `outputs/skill-radix-scheduler-advisor.md`。给定工作负载描述（prompt 模板形状、检索模式、并发租户数），它生成 prompt 排序处方和 SGLang 采用的 go/no-go 建议。

## Exercises | 练习题

1. Run `code/main.py`. Compare FCFS and cache-aware on the same workload. Where does the delta come from — prefill savings, decode savings, or queue delay?
   中文翻译：运行 `code/main.py`。在相同工作负载上比较 FCFS 和缓存感知。差异从何而来——预填充节省、解码节省还是队列延迟？
2. Modify the workload so prompts randomly permute `[system, tools, context]`. Re-run. What happens to hit rate? Why?
   中文翻译：修改工作负载使 prompt 随机排列 `[system, tools, context]`。重新运行。命中率发生什么变化？为什么？
3. Compute the HBM cost of keeping a 2,000-token system prompt resident as one radix branch on Llama 3.1 8B. Compare to the cost of a 16-sequence batch without prefix reuse.
   中文翻译：计算在 Llama 3.1 8B 上保持 2,000 token 系统提示作为一个 radix 分支常驻的 HBM 成本。与无前缀复用的 16 序列批次成本比较。
4. Read the SGLang RadixAttention paper. Explain in three sentences why tree-shaped LRU eviction beats block-shaped LRU under prefix-heavy load.
   中文翻译：阅读 SGLang RadixAttention 论文。用三句话解释为什么树形 LRU 淘汰在前缀密集负载下优于块形 LRU。
5. A customer reports only 8% cache hit rate. Name three likely causes and the diagnostic you would run for each.
   中文翻译：客户报告仅 8% 缓存命中率。说出三个可能原因和每个的诊断方法。

## Key Terms | 术语速查表

| Term / 术语 | What people say / 通俗说法 | What it actually means / 实际含义 |
|------|----------------|------------------------|
| RadixAttention | "the SGLang thing" / "SGLang 的那个" | KV cache indexed as a radix tree so shared prefixes reuse blocks / KV 缓存以 radix tree 索引，共享前缀复用块 |
| Radix tree | "compact trie" / "紧凑前缀树" | Tree where each node owns a token range and its KV blocks / 每个节点拥有 token 范围和 KV 块的树 |
| Cache-aware scheduler | "hot-branch-first" / "热分支优先" | Scheduler that prefers requests sharing the resident branch / 优先服务共享常驻分支请求的调度器 |
| Prefix-cache hit rate | "how much of your prompt was free" / "prompt 多少是免费的" | Fraction of prompt tokens served from reused KV blocks / 从复用 KV 块服务的 prompt token 比例 |
| FCFS | "first-come first-served" / "先来先服务" | Default scheduling that breaks prefix locality / 破坏前缀局部性的默认调度 |
| Branch-level LRU | "evict the leaf" / "淘汰叶子" | Eviction policy matched to radix shape / 匹配 radix 形状的淘汰策略 |
| Prompt template ordering | "the cache key" / "缓存键" | The prompt's component order determines what the tree can share / prompt 组件顺序决定树能共享什么 |
| System prompt pinning | "resident prefix" / "常驻前缀" | Keep the immutable system portion pinned to avoid eviction thrash / 保持不可变系统部分固定避免淘汰抖动 |

## Further Reading | 延伸阅读

- [SGLang GitHub](https://github.com/sgl-project/sglang) — source and docs.
- [SGLang documentation](https://sgl-project.github.io/) — RadixAttention and scheduling details.
- [SGLang paper — Efficiently Programming Large Language Models (arXiv:2312.07104)](https://arxiv.org/abs/2312.07104) — the design reference.
- [LMSYS blog — SGLang with RadixAttention](https://www.lmsys.org/blog/2024-01-17-sglang/) — benchmark numbers and scheduler rationale.
- [vLLM — Prefix Caching](https://docs.vllm.ai/en/latest/features/prefix_caching.html) — vLLM's own radix-like implementation, for comparison.
