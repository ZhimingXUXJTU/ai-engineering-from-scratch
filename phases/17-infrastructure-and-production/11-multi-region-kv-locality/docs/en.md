# Multi-Region LLM Serving and KV Cache Locality | 多区域 局部性 服务 LLM KV

> Round-robin load balancing is actively harmful for cached LLM inference. A request that does not land on the node holding its prefix pays full prefill cost — roughly 800 ms at P50 on a long prompt versus ~80 ms with a cache hit. In 2026 the production pattern is a cache-aware router (vLLM Router in Rust, llm-d router) that consumes KV-cache events and routes on prefix-hash match. Recent research (GORGO) makes cross-region network latency an explicit term in the routing objective. Commercial "cross-region inference" offerings (Bedrock cross-region inference, GKE multi-cluster gateways) treat inference as opaque — they handle availability, not TTFT. JPMorgan and Mayo Clinic ran us-east-1 failover in Nov 2024 at ~22 minutes. The DR reality: 32% of LLM DR failures are because teams backed up weights but forgot tokenizer files or quantization configs.

> **【中文解读】** 本节介绍了多区域 KV 局部性——跨区域部署 LLM 时的 KV Cache 优化策略。


**Type:** Learn
**Languages:** Python (stdlib, toy prefix-cache-aware router simulator)
**Prerequisites:** Phase 17 · 04 (vLLM Serving), Phase 17 · 06 (SGLang RadixAttention)
**Time:** ~60 minutes

## Learning Objectives | 学习目标

- Explain why round-robin load balancing breaks cached inference and quantify the TTFT penalty.
- Diagram a cache-aware router: inputs (KV-cache events), algorithm (prefix-hash match), tie-breaker (GPU utilization).
- Name the 32% DR failure driver for LLMs (missing tokenizer files / quantization configs) and state a three-file DR checklist.
- Distinguish commercial cross-region offerings (Bedrock CRI, GKE Multi-Cluster Gateway) from KV-aware routing.

## The Problem | 问题

> **【中文解读】** 多区域 LLM 服务的三个核心问题：(1) 缓存路由——轮询负载均衡破坏了 KV Cache 局部性，导致缓存命中率从 70% 跌到 8%；(2) DR 卫生——32% 的 LLM DR 失败是因为团队备份了权重但忘记了分词器文件或量化配置；(3) 数据驻留——GDPR 要求 EU 用户数据不能离开 EU，cache-aware router 不能为了前缀匹配将巴黎用户的请求路由到 us-east-1。

> **【拓展：多区域推理的产业实践】** 2026 年多区域 LLM 部署的最佳实践包括：(1) 每 region 独立的 cache-aware router（vLLM Router / llm-d router），避免跨区域 KV 转移的高延迟（US-EU RTT 约 75ms，US-APAC 约 220ms）；(2) GORGO 研究将网络延迟作为路由目标的显式项——联合优化 prefill_time + network_latency；(3) Bedrock cross-region inference 和 GKE Multi-Cluster Gateway 处理可用性，但不处理 TTFT——你仍需要应用层 cache-aware router。

Your service runs in us-east-1, us-west-2, and eu-west-1. You put an ALB in front with round-robin. Prefix cache hit rate in production drops to 8%. TTFT P50 triples. Your vLLM logs show every request is paying full prefill cost.

Round-robin is optimal for stateless services. LLM inference is stateful by design — the KV cache encodes everything the model has seen. Routing blind is routing into the wrong cache.

Separately, your team has a DR plan. You back up model weights to S3 cross-region. A regional outage hits; you attempt failover; the replica refuses to start. You forgot tokenizer.json, the quantization config, and the RoPE scaling config were in a separate bucket you didn't sync.

Multi-region LLM serving is a cache problem, a routing problem, and a DR-hygiene problem — not a load-balancer problem.

## The Concept | 概念

### Cache-aware routing

> **【中文解读】** Cache-aware 路由的工作机制：请求到达后，路由器对前缀（如前 512 tokens）做哈希，查询每个副本"你是否有这个前缀缓存？"。副本通过 pub/sub 频道发布 KV Cache 事件（分配/淘汰块），路由器维护前缀哈希→副本的索引。匹配到则路由到该副本，未匹配则按 GPU 利用率选择。vLLM Router（Rust 实现，2026 production-stack）支持 O(1) 查找，未匹配时回退到最小队列深度。

Request arrives with a prompt. Router hashes the prefix (say, first 512 tokens); it asks each replica "do you have this prefix cached?". Replicas publish KV-cache events on a pub/sub channel as they allocate and evict blocks. Router picks the replica with the match, falls through to GPU-util-based tie-breaker if no one does.

**vLLM Router** (Rust, 2026 production-stack): subscribes to `kv.cache.block_added` events, maintains a prefix-hash → replica index, routes with O(1) lookup. Falls through to least-queue-depth when no match.

**llm-d router**: same pattern, Kubernetes-native. Publishes events via the ControlPlane API.

**SGLang RadixAttention** (Phase 17 · 06) is the intra-replica equivalent. Cross-replica routing is strictly upstream.

### Numbers

> **【拓展：KV Cache 路由的性能数据】** 多区域 KV Cache 路由的性能差距：2K-token 提示在 Llama 3.3 70B FP8 H100 上，cache hit（同副本、前缀常驻）TTFT ~80ms；cache miss（冷 prefill）TTFT ~800ms——10x 差距。如果路由器在副本间实现 60-80% 的前缀缓存命中率，可以在 N 副本容量下近似单副本性能。区域间 RTT 也是关键因素：us-east-1 ↔ us-west-2 ~65ms、us-east-1 ↔ eu-west-1 ~75ms、us-east-1 ↔ ap-southeast-1 ~220ms——跨区域路由只在 prefill 时间远大于网络延迟时才有价值。

TTFT P50 on a 2K-token prompt, Llama 3.3 70B FP8, H100:
- Cache hit (same replica, prefix resident): ~80 ms.
- Cache miss (cold prefill): ~800 ms.

10x gap. If your router hits 60-80% of prefix cache across replicas, you approximate single-replica performance at N-replica capacity. If it hits 10%, you approximate naive scaling.

### Cross-region has a new constraint — network latency

Inter-region RTT:
- us-east-1 ↔ us-west-2: ~65 ms.
- us-east-1 ↔ eu-west-1: ~75 ms.
- us-east-1 ↔ ap-southeast-1: ~220 ms.

If routing takes a request from us-east-1 to a hot prefix in ap-southeast-1, the saved prefill (800 → 80 ms) is dwarfed by 440 ms round-trip. GORGO (2026 research) makes this explicit — minimize `prefill_time + network_latency` jointly, not prefill alone. Often the answer is to keep routing regional except on massive multi-MB prefixes where prefill dominates.

### Commercial "cross-region inference" does not help here

AWS Bedrock cross-region inference automatically routes requests to other regions during capacity pressure. It optimizes availability, not TTFT, and treats inference as opaque. GKE Multi-Cluster Gateway is the same — service-level failover, no awareness of KV cache.

You still need an app-layer cache-aware router even when using these. They handle the "us-east-1 is on fire" case. Cache-aware routing handles the TTFT case.

### DR hygiene — the 32% missing-files problem

> **【中文解读】** DR 卫生的三文件最低清单：(1) HF 模型仓库下的所有文件（权重 + 配置 + 分词器）；(2) 引擎特定的服务配置（vllm_config.yaml 等）；(3) 部署清单（K8s YAML、Dockerfile、依赖锁文件）。加上：每季度演练 DR——JPMorgan 2024 年 11 月的 us-east-1 故障演练达到 22 分钟恢复，正是因为预案经过了排练。

> **【拓展：LLM 灾难恢复最佳实践】** 2026 年 LLM DR 的关键实践：(1) 模型制品完整性——不只是权重文件，还包含 tokenizer.json、quantize_config.json、RoPE 缩放配置、聊天模板；(2) 跨区域同步——S3 cross-region replication 用于模型仓库，确保所有 region 有完整副本；(3) 自动化 DR 测试——使用 Chaos Engineering（Phase 17·24）定期验证 failover 流程；(4) RTO 目标——企业级 LLM 服务通常要求 RTO < 30 分钟。

Widely cited 2026 stat: 32% of LLM DR failures happen because teams backed up weights but forgot:

- `tokenizer.json` or `tokenizer.model`
- Quantization configs (`quantize_config.json`, AWQ scales, GPTQ zero-points)
- Model-specific configs (RoPE scaling, attention masks, chat templates)
- Engine config (`vllm_config.yaml`, sampling defaults, LoRA adapter manifests)

The fix is a three-file minimum DR manifest:

1. All files under the HF model repo (weights + configs + tokenizer).
2. Engine-specific serving config.
3. Deployment manifest (K8s YAML, Dockerfile, dependency lock).

Plus: run a DR drill quarterly. The JPMorgan us-east-1 drill hit 22 minutes recovery in Nov 2024 only because the playbook was rehearsed.

### Data residency is orthogonal

EU customer PHI cannot leave EU. If your cache-aware router sends a Paris-originated request to us-east-1 for a prefix match, you have violated GDPR regardless of TTFT gain. Partition routers by residency boundary before optimizing for cache.

### Numbers you should remember

- Cache hit vs miss TTFT gap: ~10x (80 ms vs 800 ms on 2K prompt).
- Inter-region RTT US-EU: ~75 ms.
- DR failure: 32% miss tokenizer/quant configs.
- JPMorgan us-east-1 failover Nov 2024: 22 minutes (30-min SLA).

## Use It | 使用方法

`code/main.py` simulates three routing strategies (round-robin, cache-aware regional, cache-aware global) on a multi-region workload. Reports cache hit rate, TTFT P50/P99, and cross-region bill.

## Ship It | 部署上线

This lesson produces `outputs/skill-multi-region-router.md`. Given regions, residency constraints, and SLA, designs a routing plan.

## Exercises | 练习题

1. Run `code/main.py`. At what prompt length does cross-region routing beat local-only routing, given 75 ms RTT?
2. Your cache hit rate drops from 70% to 12%. Diagnose three possible causes and the observables that would confirm each.
3. Design a DR manifest for a 70B AWQ-quantized model served in vLLM with 5 LoRA adapters. List every file and config.
4. Argue whether Bedrock cross-region inference is "enough" for a fintech with strict TTFT SLOs. Cite specific behaviors.
5. A Paris-origin request matches a prefix in us-east-1. Do you route it? Write the policy.

## Key Terms | 关键术语

| Term | What people say | What it actually means |
|------|----------------|------------------------|
| Cache-aware routing | "smart LB" | Route on prefix-hash match to KV-cache-holding replica |
| KV-cache events | "cache pub-sub" | Replicas publish block add/evict; router indexes |
| Prefix hash | "cache key" | Hash of first N tokens used as router lookup |
| GORGO | "cross-region routing research" | arXiv 2602.11688; network latency as explicit term |
| Cross-region inference | "Bedrock CRI" | AWS product; availability failover, not TTFT awareness |
| DR manifest | "the backup list" | Every file needed to restore — not just weights |
| Data residency | "GDPR boundary" | Legal constraint on which region sees user data |
| RTT | "round-trip time" | Network latency; 75 ms US-EU, 220 ms US-APAC |
| LLM-aware LB | "cache-hit LB" | Cache-aware router as a product category |

## Further Reading | 延伸阅读

- [BentoML — Multi-cloud and cross-region inference](https://bentoml.com/llm/infrastructure-and-operations/multi-cloud-and-cross-region-inference)
- [arXiv — GORGO (2602.11688)](https://arxiv.org/html/2602.11688v1) — cross-region KV-cache reuse with network latency term.
- [TianPan — Multi-Region LLM Serving Cache Locality](https://tianpan.co/blog/2026-04-17-multi-region-llm-serving-data-residency-routing)
- [AWS Bedrock Cross-Region Inference](https://docs.aws.amazon.com/bedrock/latest/userguide/cross-region-inference.html) — availability failover documentation.
- [vLLM Production Stack Router](https://github.com/vllm-project/production-stack) — cache-aware router source.
