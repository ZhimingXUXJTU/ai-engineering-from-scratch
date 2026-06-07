# Cold Start Mitigation for Serverless LLMs | 冷启动 缓解 服务器 LLM

> A 20 GB model image takes 5-10 minutes (7B) to 20+ minutes (70B) to go from cold to serving. In a true serverless world, that is not a warm-up — it is an outage. Mitigations operate at five layers: pre-seeded node images (Bottlerocket on AWS, dual-volume arch), model streaming (NVIDIA Run:ai Model Streamer, native in vLLM), GPU memory snapshots (Modal checkpoints, up to 10x faster restart), warm pools (`min_workers=1`), tiered loading (ServerlessLLM's NVMe→DRAM→HBM pipeline, 10-200x latency reduction), and live migration that moves input tokens (KB) rather than KV cache (GB). Modal publishes 2-4s cold starts as a floor; Baseten 5-10s default, sub-second with pre-warming. This lesson teaches you to measure, budget, and stack the five layers.

> **【中文解读】** 本节介绍了冷启动缓解——减少 LLM 推理服务首次响应延迟的策略。


**Type:** Learn | **类型:** 学习
**Languages:** Python (stdlib, toy cold-start path simulator) | **语言:** Python
**Prerequisites:** Phase 17 · 02 (Inference Platform Economics), Phase 17 · 03 (GPU Autoscaling) | **前置知识:** Phase 17 · 02 (Inference Platform Economics), Phase 17 · 03 (GPU Autoscaling)
**Time:** ~60 minutes | **时间:** ~60 minutes

## Learning Objectives | 学习目标

- Enumerate the five layers of cold-start mitigation and name one tool or pattern at each layer.
  中文翻译：列举冷启动缓解的五层策略，并说出每层的一个工具或模式。
- Compute total cold-start time as a sum of (node provision) + (weights download) + (weights load into HBM) + (engine init) for a 70B model.
  中文翻译：计算 70B 模型总冷启动时间 = 节点供给 + 权重下载 + 权重加载到 HBM + 引擎初始化。
- Explain why live migration transfers input tokens (KB) not KV cache (GB) and what the penalty is (recomputation).
  中文翻译：解释为什么实时迁移传输输入 token（KB）而非 KV 缓存（GB），以及代价是什么（重新计算）。
- Name the warm-pool trade-off (pay for idle GPU or accept cold-start tail) and the SLA threshold at which `min_workers > 0` becomes mandatory.
  中文翻译：说出热池权衡（为空闲 GPU 付费或接受冷启动尾部），以及 `min_workers > 0` 变为强制性的 SLA 阈值。

## The Problem | 问题引入

> **【中文解读】** Serverless LLM 端点的冷启动问题：70B 模型从零到服务需要 3-8 分钟（节点供给 45-60s + 容器拉取 120-300s + 权重加载 45-120s + 引擎初始化 10-30s），远超 2s 的 SLA。解决方案是保留热池（min_workers=1），但这意味着 24/7 支付空闲 GPU 费用——5 个产品各保留 1 个热副本，每月 3600 GPU-hours 无论是否有用户调用。

> **【拓展：Serverless LLM 平台对比】** 2026 年 Serverless LLM 平台的冷启动表现：Modal 凭借 GPU 快照技术实现 2-4s 冷启动（业界最快）；Baseten 默认 5-10s，预加热后可低于 1s；AWS Lambda + 容器镜像通常 10-30s（不包含模型加载）；GCP Cloud Run + GPU 较新，冷启动约 15-30s。对于 TTFT P99 < 60s 的 70B+ 模型，热池是强制性的——没有任何冷启动优化能在 60s 内完成全流程。

Your serverless LLM endpoint scales to zero overnight. At 8 a.m. traffic spikes. The first request waits while:

> 你的无服务器 LLM 端点在夜间缩容到零。早上 8 点流量激增。第一个请求等待：

1. Karpenter provisions a GPU node: 45-60s.
   中文翻译：Karpenter 供给 GPU 节点：45-60 秒。
2. The container pulls a 30 GB image with weights: 120-300s.
   中文翻译：容器拉取 30GB 的含权重镜像：120-300 秒。
3. The engine loads weights into HBM: 45-120s depending on model size and storage speed.
   中文翻译：引擎将权重加载到 HBM：45-120 秒，取决于模型大小和存储速度。
4. vLLM or TRT-LLM initializes CUDA graphs, KV cache pool, tokenizer: 10-30s.
   中文翻译：vLLM 或 TRT-LLM 初始化 CUDA graph、KV 缓存池、分词器：10-30 秒。

Total: 220-510s (roughly 3-8 minutes) before one token comes back. Your SLA is 2s. You ship a warm-pool (`min_workers=1`) and the problem seems to vanish — but now you pay for one idle GPU 24x7. If your service has 5 products each with one warm replica, that's 5 × 24 × 30 = 3,600 GPU-hours/month whether or not a single user called.

> 总计：220-510 秒（约 3-8 分钟）才能返回一个 token。你的 SLA 是 2 秒。你部署热池（`min_workers=1`）问题似乎消失了——但现在你 24/7 为一个空闲 GPU 付费。如果你的服务有 5 个产品各一个热副本，那就是 5 × 24 × 30 = 3,600 GPU-hours/月，无论是否有用户调用。

Cold-start mitigation is how to keep the serverless economics while approximating the latency of always-on.

> 冷启动缓解是在保持无服务器经济性的同时逼近常驻服务的延迟。

## The Concept | 核心概念

### Layer 1 — pre-seeded node images (Bottlerocket)

> **【中文解读】** 第一层——预播种节点镜像。AWS Bottlerocket 的双卷架构将操作系统与数据分离。将容器镜像（含模型权重）预烘焙到数据卷快照中，在 `EC2NodeClass` 中引用快照 ID。新节点启动时权重已在本地 NVMe 上——消除了镜像拉取步骤，为大型模型节省 2-4 分钟。GCP 和 Azure 有类似的自定义 VM 镜像模式。

On AWS, Bottlerocket's dual-volume architecture separates OS from data. Snapshot the data volume with your container image pre-pulled; reference the snapshot ID in your `EC2NodeClass`. New nodes boot with weights already on local NVMe — steps 2 and part of 3 vanish. Works with Karpenter natively. Typical savings: 2-4 minutes per cold start for large models.

> 在 AWS 上，Bottlerocket 的双卷架构将操作系统与数据分离。将容器镜像预拉取到数据卷快照中；在 `EC2NodeClass` 中引用快照 ID。新节点启动时权重已在本地 NVMe 上——步骤 2 和部分步骤 3 消除。原生与 Karpenter 配合。典型节省：大型模型每次冷启动 2-4 分钟。

Equivalent on GCP: custom VM images with pre-baked container layers. On Azure: managed disk snapshots with the same pattern.

> GCP 等价方案：预烘焙容器层的自定义 VM 镜像。Azure：托管磁盘快照加相同模式。

### Layer 2 — model streaming (Run:ai Model Streamer)

> **【中文解读】** 第二层——模型流式加载。NVIDIA Run:ai Model Streamer 不需要等整个文件加载完才开始服务，而是将权重逐层流式加载到 GPU 内存，并在第一个 transformer 块加载完成后就开始处理。2026 年 vLLM 原生支持此功能。兼容 S3、GCS 和本地 NVMe。通过重叠 I/O 和计算设置，可将大型模型的权重加载时间减半。

Instead of loading the full file before answering the first request, stream weights into GPU memory layer-by-layer and start processing as soon as the first transformer block is resident. The NVIDIA Run:ai Model Streamer ships native in vLLM 2026. Works with S3, GCS, and local NVMe. Cuts weight-load time roughly in half for large models by overlapping I/O with compute setup.

> 不需要在回答第一个请求前加载完整文件，而是将权重逐层流式加载到 GPU 内存，并在第一个 transformer 块加载完成后立即开始处理。NVIDIA Run:ai Model Streamer 在 2026 年 vLLM 中原生提供。兼容 S3、GCS 和本地 NVMe。通过重叠 I/O 和计算设置，将大型模型的权重加载时间大约减半。

### Layer 3 — GPU memory snapshots (Modal)

> **【中文解读】** 第三层——GPU 内存快照。Modal 在首次加载后对 GPU 状态（权重、CUDA graph、KV Cache 区域）做检查点，后续重启直接反序列化到 HBM——比重新初始化快 10x。这是"2 秒启动热 GPU"最接近的技术。代价是快照与 GPU 拓扑绑定——如果 Karpenter 将你迁移到不同 SKU，需要重新制作快照。

> **【拓展：冷启动优化策略叠加】** 五层冷启动缓解可以叠加使用：(1) 预播种镜像（消除镜像拉取）+ (2) 模型流式加载（减半权重加载时间）+ (3) GPU 快照（消除重复加载）+ (4) 热池（避免冷启动）+ (5) 分层加载（NVMe→DRAM→HBM）。全栈叠加可将 70B 模型从 328s 冷启动降到约 15s——22x 改善。选择哪几层取决于 SLA 严格程度和预算。

Modal takes a checkpoint of the GPU state (weights, CUDA graphs, KV cache region) after first load. Subsequent restarts deserialize directly into HBM — 10x faster than re-initializing. This is the closest thing to "boot a warm GPU in 2 seconds." Trade-off: snapshots are per-GPU-topology, so if Karpenter migrates you to a different SKU, you re-checkpoint.

> Modal 在首次加载后对 GPU 状态（权重、CUDA graph、KV 缓存区域）做检查点。后续重启直接反序列化到 HBM——比重新初始化快 10 倍。这是"2 秒启动热 GPU"最接近的技术。代价：快照与 GPU 拓扑绑定，如果 Karpenter 迁移到不同 SKU 需要重新制作快照。

### Layer 4 — warm pools (min_workers=1)

> **【拓展：Serverless LLM 平台的冷启动对比】** 2026 年 Serverless LLM 平台的冷启动表现：Modal 以 GPU 快照技术实现 2-4s（业界最快）；Baseten 默认 5-10s，预加热后 <1s；AWS Lambda + 容器镜像通常 10-30s（不含模型加载）；原始 70B 模型冷启动 3-8 分钟。Modal 的快照技术是关键差异——它将 GPU 状态（权重 + CUDA graph + KV Cache 区域）序列化，重启时直接反序列化到 HBM，比重新初始化快 10x。代价是快照与 GPU 拓扑绑定，迁移到不同 SKU 需要重新制作快照。

Simplest mitigation: keep one replica always ready. Cost is one GPU's hourly rate 24x7. The arithmetic is brutal on small models (you pay $0.85-$1.50/hr to avoid a 30s cold start) and kind to large ones (pay $4/hr to avoid a 5-minute cold start). The SLA threshold where warm pools become mandatory: typically TTFT P99 < 60s on a 70B+ model.

> 最简单的缓解：保持一个副本始终就绪。成本是一个 GPU 的小时费率 24/7。小模型的算术很残酷（你付 $0.85-$1.50/小时来避免 30 秒冷启动），大模型则相对友好（付 $4/小时来避免 5 分钟冷启动）。热池变为强制性的 SLA 阈值：通常是 70B+ 模型上 TTFT P99 < 60 秒。

### Layer 5 — tiered loading (ServerlessLLM)

ServerlessLLM treats storage as a hierarchy: NVMe (fast but big), DRAM (medium but tiered), HBM (tiny but instant). Weights are pre-loaded to DRAM; load-on-demand into HBM. Paper reports 10-200x latency reduction on cold loads versus naive disk-to-HBM. Production adoption is early but integrations with vLLM exist.

> ServerlessLLM 将存储视为层级：NVMe（快但大）、DRAM（中等但分层）、HBM（小但即时）。权重预加载到 DRAM；按需加载到 HBM。论文报告冷启动延迟降低 10-200 倍。生产采用尚早，但已存在与 vLLM 的集成。

### Layer 6 — live migration (bonus pattern)

When a node becomes unavailable (spot eviction, node drain), traditional pattern is cold-start another replica and drain request queue. Live migration moves the input tokens (kilobytes) to a destination that has the model loaded and recomputes KV cache on the destination. Recomputation is cheaper than transferring GB of KV cache over the network. Applicable to disaggregated deployments.

> 当节点不可用时（Spot 中断、节点排空），传统模式是冷启动另一个副本并排空请求队列。实时迁移将输入 token（千字节）移到已加载模型的目标节点，并在目标上重新计算 KV 缓存。重新计算比通过网络传输 GB 级 KV 缓存更便宜。适用于分离式部署。

### The warm-pool math

> **【中文解读】** 热池数学：对于 P99 TTFT SLA 为 2s 的服务，问题不是"热池 yes/no"而是"多少热副本、哪些路径需要"。高价值交互路径（实时聊天、语音 Agent）→ min_workers=1-2；后台批处理路径（夜间分类）→ scale-to-zero 可接受；高级层级 → 按租户专用热副本。简单算术：5 个产品各 1 个热副本 = 5 × 24 × 30 = 3600 GPU-hours/月，无论是否有用户调用。

For a service with P99 TTFT SLA of 2s, the question is not "warm pool yes/no" but "how many warm replicas, and which paths get them."

> 对于 P99 TTFT SLA 为 2 秒的服务，问题不是"热池 yes/no"而是"多少热副本，哪些路径需要它们"。

- High-value interactive paths (live chat, voice agent): `min_workers=1-2`.
  中文翻译：高价值交互路径（实时聊天、语音代理）：`min_workers=1-2`。
- Background batch paths (nightly classification): scale-to-zero accepted, 5-10 minute cold start tolerable.
  中文翻译：后台批处理路径（夜间分类）：接受缩容到零，5-10 分钟冷启动可容忍。
- Premium tier: `min_workers` per tenant with dedicated capacity.
  中文翻译：高级层级：按租户 `min_workers` 专用容量。

### Measure before optimizing

> **【中文解读】** 70B 模型冷启动解剖（示意数据）：节点供给 50s + 镜像拉取 180s + 权重到 HBM 75s + 引擎初始化 20s + 首次前向 3s = 总计 328s。全栈缓解后：预播种消除镜像拉取、模型流式加载减半权重加载、GPU 快照消除重复初始化 = 约 15s 总冷启动（22x 降低）。

Cold-start anatomy for a 70B model on a fresh node (illustrative):

| Phase | Time | Mitigation |
|-------|------|-----------|
| Node provision | 50s | Bottlerocket + pre-seeded image, warm pool |
| Image pull | 180s | Pre-seeded data volume (eliminate) |
| Weights to HBM | 75s | Model streamer (halve); GPU snapshot (eliminate) |
| Engine init | 20s | Persistent CUDA graph cache |
| First forward | 3s | Min inherent latency |
| **Total cold** | **328s** | |
| **Total with mitigations** | **~15s** | 22x reduction |

### Numbers you should remember

- Modal cold start: 2-4s (with GPU snapshots).
  中文翻译：Modal 冷启动：2-4 秒（使用 GPU 快照）。
- Baseten default cold start: 5-10s; sub-second with pre-warming.
  中文翻译：Baseten 默认冷启动：5-10 秒；预加热后亚秒级。
- Raw 70B cold start: 3-8 minutes.
  中文翻译：原始 70B 冷启动：3-8 分钟。
- Run:ai Model Streamer: ~2x weight-load speedup.
  中文翻译：Run:ai Model Streamer：约 2 倍权重加载加速。
- ServerlessLLM tiered loading: 10-200x latency reduction (paper numbers).
  中文翻译：ServerlessLLM 分层加载：10-200 倍延迟降低（论文数据）。

## Use It | 用框架实现

`code/main.py` models a cold-start path with and without each mitigation. Reports total cold-start time, warm-pool cost, and the break-even request rate above which warm pool pays for itself.

> `code/main.py` 建模有/无每种缓解的冷启动路径。报告总冷启动时间、热池成本和热池自付自足的盈亏平衡请求率。

## Ship It | 产出物

This lesson produces `outputs/skill-cold-start-planner.md`. Given SLA, model size, and traffic shape, picks which mitigations to stack.

> 本课产出 `outputs/skill-cold-start-planner.md`。给定 SLA、模型大小和流量形状，选择叠加哪些缓解策略。

## Exercises | 练习题

1. Run `code/main.py`. Compute the break-even request rate above which a warm replica is cheaper than paying the cold-start tax via extra request drops at SLO.
   中文翻译：运行 `code/main.py`。计算热副本比通过 SLO 下额外请求丢弃支付冷启动税更便宜的盈亏平衡请求率。
2. You deploy a 13B model with P99 TTFT SLA of 3s. Pick the minimum mitigation stack (fewest layers) that achieves it.
   中文翻译：你部署一个 13B 模型，P99 TTFT SLA 为 3 秒。选择实现它的最小缓解栈（最少层级）。
3. Bottlerocket pre-seeding eliminates image pull but weights still load from snapshot to HBM. Compute wall-clock for a 70B model if the snapshot-backed NVMe reads at 7 GB/s.
   中文翻译：Bottlerocket 预播种消除了镜像拉取，但权重仍需从快照加载到 HBM。计算快照支持的 NVMe 以 7 GB/s 读取时 70B 模型的实际耗时。
4. Your serverless provider offers GPU snapshots (Modal) and your team refuses because "snapshots leak PII." Argue both sides — what is the realistic risk, and what is the mitigation (ephemeral snapshots, encryption, namespace isolation)?
   中文翻译：你的无服务器提供商提供 GPU 快照（Modal），但团队拒绝因为"快照泄露 PII"。辩论双方——实际风险是什么，缓解方案是什么（临时快照、加密、命名空间隔离）？
5. Design a tiered warm-pool policy: how many warm replicas for paid users, trial users, and batch workloads? Show the math.
   中文翻译：设计分层热池策略：付费用户、试用用户和批处理工作负载各多少热副本？展示计算。

## Key Terms | 术语速查表

| Term | What people say | What it actually means |
|------|----------------|------------------------|
| Cold start | "the big pause" | Time from request to first token on a fresh replica |
| Warm pool | "always-on minimum" | `min_workers >= 1` to keep at least one replica ready |
| Pre-seeded image | "baked AMI" | Node image with container weights pre-resident |
| Bottlerocket | "AWS node OS" | AWS container-optimized OS with dual-volume snapshot support |
| Model streamer | "streaming load" | Overlap weights I/O with compute setup |
| GPU snapshot | "checkpoint to HBM" | Serialize post-load GPU state; deserialize on restart |
| Tiered loading | "NVMe + DRAM + HBM" | Hierarchy of storage tiers; load on demand |
| Live migration | "move tokens" | Transfer input (KB), recompute KV on destination |
| `min_workers` | "warm replicas" | Serverless minimum keep-alive count |
| Scale-to-zero | "full serverless" | No cost when idle; accept full cold-start tax |

## Further Reading | 延伸阅读

- [Modal — Cold start performance](https://modal.com/docs/guide/cold-start) — Modal's published benchmarks and checkpoint architecture.
- [AWS Bottlerocket](https://github.com/bottlerocket-os/bottlerocket) — pre-seeded data volume snapshot pattern.
- [NVIDIA Run:ai Model Streamer](https://github.com/run-ai/runai-model-streamer) — overlap weights load with compute setup.
- [Baseten — Cold-start mitigation](https://www.baseten.co/blog/cold-start-mitigation/) — pre-warming playbook.
- [ServerlessLLM paper (USENIX OSDI'24)](https://www.usenix.org/conference/osdi24/presentation/fu) — tiered loading design.
- [NVIDIA — Disaggregated LLM Inference on Kubernetes](https://developer.nvidia.com/blog/deploying-disaggregated-llm-inference-workloads-on-kubernetes/) — live migration for disaggregated deployments.
