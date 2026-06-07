# GPU Autoscaling on Kubernetes — Karpenter, KAI Scheduler, Gang Scheduling | 自动扩缩 Kubernetes 调度器 GPU

> Three layers, not one. Karpenter provisions nodes dynamically (under one minute, 40% faster than Cluster Autoscaler). KAI Scheduler handles gang scheduling, topology awareness, and hierarchical queues — it prevents the 7-of-8 partial allocation trap where seven nodes wait and burn on one missing GPU. Application-level autoscalers (NVIDIA Dynamo Planner, llm-d Workload Variant Autoscaler) scale on inference-specific signals — queue depth, KV cache utilization — not CPU/DCGM duty cycle. The classic HPA trap is that `DCGM_FI_DEV_GPU_UTIL` is a duty-cycle measurement: 100% could be 10 requests or 100. vLLM pre-allocates KV cache memory, so memory never triggers scale-down. This lesson teaches you to compose the three layers and avoid the default Karpenter `WhenEmptyOrUnderutilized` policy that terminates running GPU jobs mid-inference.

> **【中文解读】** 本节介绍了 GPU 自动扩缩——Kubernetes 上 LLM 推理服务的 GPU 资源自动扩展策略。


**Type:** Learn | **类型:** 学习
**Languages:** Python (stdlib, toy queue-depth autoscaler simulator) | **语言:** Python（标准库，队列深度自动扩缩模拟器）
**Prerequisites:** Phase 17 · 02 (Inference Platform Economics), Phase 17 · 04 (vLLM Serving Internals) | **前置知识:** Phase 17 · 02（推理平台经济学）, Phase 17 · 04（vLLM 服务内部）
**Time:** ~75 minutes | **时间:** ~75 分钟

## Learning Objectives | 学习目标

- Diagram the three autoscaling layers (node provisioning, gang scheduling, application-level) and name the tool used at each layer.
  中文翻译：绘制三层自动扩缩层（节点供给、gang 调度、应用级）并命名每层使用的工具。
- Explain why `DCGM_FI_DEV_GPU_UTIL` is the wrong HPA signal for vLLM and name two replacements (queue depth, KV cache utilization).
  中文翻译：解释为什么 `DCGM_FI_DEV_GPU_UTIL` 是 vLLM 错误的 HPA 信号，并说出两个替代方案（队列深度、KV 缓存利用率）。
- Describe gang scheduling and the partial-allocation failure mode KAI Scheduler prevents (7 of 8 GPUs idle).
  中文翻译：描述 gang 调度和 KAI Scheduler 防止的部分分配故障模式（8 个 GPU 中 7 个空闲）。
- Name the Karpenter consolidation policy (`WhenEmptyOrUnderutilized`) that terminates running GPU jobs and state the 2026 safe alternative.
  中文翻译：说出终止正在运行 GPU 任务的 Karpenter 合并策略（`WhenEmptyOrUnderutilized`），并说明 2026 年的安全替代方案。

## The Problem | 问题引入

> **【中文解读】** GPU 自动扩缩在 Kubernetes 上有三个层面的故障模式：(1) HPA 使用错误的信号（GPU 占用率而非队列深度），导致该扩时不扩；(2) Cluster Autoscaler 节点供给太慢，长提示请求超时；(3) 多 GPU 分布式推理时部分分配（7-of-8 trap），7 个 GPU 空转等待第 8 个。三层问题需要三种不同的工具组合解决。

> **【拓展：GPU 集群管理】** 2026 年 Kubernetes 已成为 LLM 推理服务的标准编排平台。NVIDIA DGX Cloud、Google GKE、AWS EKS 都提供 GPU 节点池管理。关键挑战在于 GPU 是昂贵且稀缺的资源（H100 约 $3-4/hr），扩缩决策必须精确——过度供给浪费成本，供给不足影响 SLA。Karpenter + KAI Scheduler 的组合是目前最成熟的 GPU 调度方案。

Your team ships an LLM-serving service on Kubernetes. You set up HPA with `DCGM_FI_DEV_GPU_UTIL` as the signal. The service pins at 100% utilization during business hours. HPA never scales up — it already thinks you're full. You add a replica manually; TTFT drops. HPA still doesn't scale. The signal is lying to you.

> 你的团队在 Kubernetes 上部署了 LLM 服务。你用 `DCGM_FI_DEV_GPU_UTIL` 作为信号设置了 HPA。服务在业务时段保持在 100% 利用率。HPA 从不扩容——它认为你已经满了。你手动添加一个副本；TTFT 下降。HPA 仍然不扩容。信号在欺骗你。

Separately, you use Cluster Autoscaler for nodes. A 1M-token prompt arrives at 2 a.m.; the cluster spends 3 minutes provisioning a node, and the request times out.

> 另一方面，你使用 Cluster Autoscaler 管理节点。凌晨 2 点来了一个 1M token 的提示；集群花 3 分钟供给节点，请求超时。

Separately again, you deploy a 70B model requiring 8 GPUs across 2 nodes. The cluster has 7 GPUs free and 1 spread across 3 nodes. Cluster Autoscaler provisions a node for the 1 missing GPU. Seven nodes wait 4 minutes burning money while Kubernetes gets the last GPU up.

> 再一方面，你部署了一个需要 2 个节点 8 个 GPU 的 70B 模型。集群有 7 个 GPU 空闲，1 个分散在 3 个节点上。Cluster Autoscaler 为缺少的 1 个 GPU 供给一个节点。7 个节点等 4 分钟烧钱，而 Kubernetes 启动最后一个 GPU。

Three layers, three different failure modes. GPU-aware autoscaling in 2026 is not "turn on HPA." It's composing node provisioning, gang scheduling, and application-signal autoscaling.

> 三层，三种不同的故障模式。2026 年的 GPU 感知自动扩缩不是"打开 HPA"。它是组合节点供给、gang 调度和应用信号自动扩缩。

## The Concept | 核心概念

### Layer 1 — node provisioning (Karpenter)

> **【中文解读】** 第一层是节点供给。Karpenter 监控待调度的 Pod，在 45-60 秒内按需创建 GPU 节点，比传统 Cluster Autoscaler 快约 40%。关键陷阱是 `WhenEmptyOrUnderutilized` 合并策略——它会终止正在运行推理的 GPU 节点来迁移到更便宜的实例类型，导致请求失败和模型重新加载（5-20 分钟中断）。GPU 池应使用 `WhenEmpty` + `consolidateAfter: 1h` 的安全策略。

Karpenter watches pending pods and provisions nodes within ~45-60 seconds (Cluster Autoscaler typically takes 90-120 seconds for GPU nodes). It picks instance types dynamically per the `NodePool` constraint — if your pod needs 8 H100s and the cluster has no matching node, Karpenter provisions one directly instead of scaling an existing group.

> Karpenter 监控待调度的 Pod，在约 45-60 秒内供给节点（Cluster Autoscaler 对 GPU 节点通常需要 90-120 秒）。它根据 `NodePool` 约束动态选择实例类型——如果你的 Pod 需要 8 个 H100 且集群没有匹配节点，Karpenter 直接供给一个，而不是扩展现有组。

**The consolidation trap**: Karpenter's default `consolidationPolicy: WhenEmptyOrUnderutilized` is dangerous for GPU pools. It will terminate a running GPU node to migrate pods to a cheaper right-sized instance. For inference workloads that means evicting running requests and reloading a 70B model on the new node. Loss is minutes of capacity plus request failures.

> **合并陷阱**：Karpenter 的默认 `consolidationPolicy: WhenEmptyOrUnderutilized` 对 GPU 池很危险。它会终止正在运行的 GPU 节点，将 Pod 迁移到更便宜的合适实例。对于推理工作负载，这意味着驱逐运行中的请求并在新节点上重新加载 70B 模型。损失是数分钟的容量加上请求失败。

Safe setting for GPU pools:

```yaml
disruption:
  consolidationPolicy: WhenEmpty
  consolidateAfter: 1h
```

Lets Karpenter consolidate truly empty nodes after an hour but never evict a running job.

> 让 Karpenter 在一小时后合并真正空的节点，但永不驱逐运行中的任务。

### Layer 2 — gang scheduling (KAI Scheduler)

> **【中文解读】** 第二层是调度协调。KAI Scheduler 解决 default kube-scheduler 无法处理的三个问题：(1) Gang Scheduling——全有全无调度，8-GPU 推理要么全部启动要么全部等待；(2) 拓扑感知——根据 NVLink/InfiniBand/机架拓扑放置 Pod；(3) 分层队列——多团队竞争同一 GPU 池时按优先级和配额管理。这对于 tensor parallelism 至关重要，因为 DeepSeek-V3 等 MoE 模型的张量必须在同一 NVLink 域内。

> **【拓展：GPU 调度器生态】** 2026 年 GPU 调度器的选择包括 KAI Scheduler（原 Karp，支持 gang + topology + queue）、YuniKorn（Apache 项目，支持队列和抢占）、以及 default kube-scheduler + 设备插件。KAI Scheduler 是唯一原生支持 gang scheduling 的方案，已被 Ray 和 vLLM production-stack 集成。对于需要多 GPU 分布式推理的场景（70B+ 模型），KAI 是必选项。

KAI Scheduler (project "Karp" then renamed) handles what default kube-scheduler does not:

**Gang scheduling** — schedule all-or-nothing. A distributed inference pod requiring 8 GPUs either all 8 start together or none do. Without this, you get the partial-allocation trap: 7 of 8 pods start, wait indefinitely, burn money.

**Topology awareness** — know which GPUs share NVLink, which sit on the same rack, which have InfiniBand between them. Place pods accordingly. A DeepSeek-V3 67B tensor-parallel workload must stay on one NVLink domain; KAI Scheduler respects that.

**Hierarchical queues** — multiple teams compete for the same GPU pool with priority and quota. Team A's production pinch gets preempted by Team B's training job only if priority rules allow.

KAI is deployed alongside kube-scheduler as a secondary scheduler; you annotate workloads to use it. Ray and vLLM production-stack both integrate.

> KAI 作为二级调度器与 kube-scheduler 一起部署；你通过注解让工作负载使用它。Ray 和 vLLM production-stack 都已集成。

### Layer 3 — application-level signals

> **【中文解读】** 第三层是应用级信号。传统的 `DCGM_FI_DEV_GPU_UTIL` 是 GPU 占用率（duty cycle）指标——100% 可能意味着 10 个请求或 100 个请求，因为 GPU 都在忙碌。vLLM 预分配 KV Cache 内存，即使只有一个请求，内存使用也接近 90%，导致基于内存的 HPA 永远不会缩容。2026 年正确的扩缩信号应该是队列深度、KV Cache 利用率、每副本 P99 TTFT 和 Goodput。

> **【拓展：推理感知自动扩缩】** NVIDIA Dynamo Planner 和 llm-d Workload Variant Autoscaler 是 2026 年专门为 LLM 推理设计的扩缩器。它们直接消费推理引擎的内部指标（队列深度、KV Cache 块使用率），而非通用的 GPU 指标。这种"推理感知"扩缩比传统 HPA 更精确，可将资源利用率提升 30-50%，同时保持 SLA。配合 Karpenter 的快速节点供给，从零到服务的冷启动时间可从 5 分钟降到 1 分钟。

**The HPA trap**: `DCGM_FI_DEV_GPU_UTIL` is a duty-cycle metric — it measures whether the GPU was doing work at each sampling interval. 100% utilization could mean 10 concurrent requests or 100; the GPU was busy either way. Scaling on duty cycle is scaling blindly.

Worse, vLLM and similar engines pre-allocate KV cache memory (up to `--gpu-memory-utilization`). Memory usage stays near 90% even at one request. Memory-based HPA never scales down.

**2026 replacement signals**:

- Queue depth (number of requests waiting for prefill).
  中文翻译：队列深度（等待预填充的请求数量）。
- KV cache utilization (what fraction of blocks are allocated to active sequences).
  中文翻译：KV 缓存利用率（分配给活跃序列的块比例）。
- Per-replica P99 TTFT (your SLA signal).
  中文翻译：每副本 P99 TTFT（你的 SLA 信号）。
- Goodput (requests meeting all SLOs per second).
  中文翻译：Goodput（每秒满足所有 SLO 的请求数）。

NVIDIA Dynamo Planner and llm-d Workload Variant Autoscaler consume these signals and scale replicas. They replace HPA entirely for LLM serving.

> NVIDIA Dynamo Planner 和 llm-d Workload Variant Autoscaler 消费这些信号并扩缩副本。它们完全替代了 LLM 服务中的 HPA。

### When to use what

| Scale decision / 扩缩决策 | Tool / 工具 |
|----------------|------|
| Add/remove nodes / 添加/移除节点 | Karpenter |
| Schedule multi-GPU jobs / 调度多 GPU 任务 | KAI Scheduler |
| Add/remove replicas / 添加/移除副本 | Dynamo Planner / llm-d WVA (or custom HPA on queue depth) |
| Choose GPU type / 选择 GPU 类型 | Karpenter NodePool |
| Preempt low-priority / 抢占低优先级 | KAI Scheduler queues |

> **【拓展：GPU 集群成本优化策略】** GPU 集群成本优化在 2026 年的关键策略包括：(1) Spot Instance——AWS/GCP/Azure 的 GPU Spot 实例可节省 60-70%，但需要处理中断（Karpenter + 热池缓解）；(2) 自动扩缩——Karpenter 在非高峰时段自动缩减节点池，50% 成本节省；(3) GPU 共享——通过 MIG（Multi-Instance GPU）将 H100 切分为多个实例，适合小模型推理；(4) 混合精度——FP8/INT4 量化减少 GPU 内存需求，允许更多并发；(5) 分离式部署——prefill/decode 分离到不同 GPU 类型，30-40% 成本节省。

### Disaggregated prefill/decode complicates everything

> **【中文解读】** 分离式预填充/解码架构（Phase 17·17）进一步增加了扩缩复杂性：预填充 Pod 按队列深度扩缩，解码 Pod 按 KV Cache 压力扩缩。不能在两者之上使用单一 HPA——需要各自独立的扩缩策略。llm-d 将两者暴露为独立的 Kubernetes Service，每个 Service 有自己的 HPA。

> **【拓展：Kubernetes GPU 生态】** 2026 年 Kubernetes GPU 管理的关键组件包括：NVIDIA GPU Operator（自动安装驱动/CUDA/container toolkit）、NVIDIA Device Plugin（GPU 资源发现和分配）、MIG（Multi-Instance GPU，将一张 A100/H100 切分为多个实例）、时间分片（GPU 共享）。结合 Karpenter + KAI Scheduler + Dynamo Planner，可以实现从节点供给到 Pod 调度到副本扩缩的完整 GPU 自动扩缩链。

If you run disaggregated prefill/decode (Phase 17 · 17), you have two pod classes with different scaling triggers: prefill pods scale on queue depth, decode pods scale on KV cache pressure. llm-d exposes these as separate `Services` with per-role HPA. Do not try to put a single HPA in front of both.

> 如果你运行分离式预填充/解码（Phase 17 · 17），你有两个具有不同扩缩触发器的 Pod 类：预填充 Pod 按队列深度扩缩，解码 Pod 按 KV 缓存压力扩缩。llm-d 将它们暴露为独立的 `Services`，每个角色有自己的 HPA。不要试图在两者前面放单个 HPA。

### Cold start matters here too

Cold-start mitigation (Phase 17 · 10) is where node provisioning time becomes user-visible. Karpenter's 45-60 second warm-up plus a 20GB model load plus engine init means a from-zero request takes 2-5 minutes. Keep a warm pool (`min_workers=1`) for SLO-critical paths, or use Modal-style checkpointing at application layer.

> 冷启动缓解（Phase 17 · 10）是节点供给时间变得用户可感知的地方。Karpenter 的 45-60 秒预热加上 20GB 模型加载加上引擎初始化意味着从零开始的请求需要 2-5 分钟。对 SLO 关键路径保持热池（`min_workers=1`），或在应用层使用 Modal 风格的检查点。

### Numbers you should remember

- Karpenter node provisioning: ~45-60s vs Cluster Autoscaler ~90-120s (GPU nodes).
  中文翻译：Karpenter 节点供给：约 45-60 秒 vs Cluster Autoscaler 约 90-120 秒（GPU 节点）。
- KAI Scheduler prevents partial-allocation waste — 7-of-8 trap.
  中文翻译：KAI Scheduler 防止部分分配浪费——7-of-8 陷阱。
- `DCGM_FI_DEV_GPU_UTIL` as HPA signal: broken; use queue depth or KV utilization.
  中文翻译：`DCGM_FI_DEV_GPU_UTIL` 作为 HPA 信号：有缺陷；使用队列深度或 KV 利用率。
- Karpenter `WhenEmptyOrUnderutilized`: terminates running GPU jobs. Use `WhenEmpty + consolidateAfter: 1h` for inference.
  中文翻译：Karpenter `WhenEmptyOrUnderutilized`：终止运行中的 GPU 任务。推理使用 `WhenEmpty + consolidateAfter: 1h`。

## Use It | 用框架实现

> **【拓展：GPU 自动扩缩成本模型】** GPU 自动扩缩的成本优化核心是减少空转时间。以 H100（$3/hr）为例，8-GPU 集群 24/7 运行每月成本约 $17,280。通过 Karpenter 按需供给 + `WhenEmpty` 合并策略 + 推理感知 HPA，可在非高峰时段自动缩容到 2-GPU，将月成本降至约 $8,640（节省 50%）。Spot Instance 可进一步节省 60-70%，但需要处理中断。

`code/main.py` simulates a three-layer autoscaler on a bursty GPU workload. Compares naive HPA (duty cycle), queue-depth HPA, and KAI-gang-scheduled scaling. Reports unmet requests, idle-GPU minutes, and a composite score.

> `code/main.py` 在突发 GPU 工作负载上模拟三层自动扩缩器。比较朴素 HPA（占用率）、队列深度 HPA 和 KAI gang 调度扩缩。报告未满足的请求数、空闲 GPU 分钟数和综合评分。

## Ship It | 产出物

This lesson produces `outputs/skill-gpu-autoscaler-plan.md`. Given cluster topology, workload shape, and SLO, it designs a three-layer autoscaling plan.

> 本课产出 `outputs/skill-gpu-autoscaler-plan.md`。给定集群拓扑、工作负载形状和 SLO，设计三层自动扩缩方案。

## Exercises | 练习题

1. Run `code/main.py`. Under a bursty workload, how many requests does naive duty-cycle HPA drop that queue-depth HPA catches? Where does the difference come from?
   中文翻译：运行 `code/main.py`。在突发工作负载下，朴素占用率 HPA 丢弃了多少请求被队列深度 HPA 捕获？差异从何而来？
2. Design a Karpenter NodePool for a cluster serving Llama 3.3 70B FP8 on H100 SXM5. Specify `capacity-type`, `disruption.consolidationPolicy`, `consolidateAfter`, and a taint that keeps non-GPU workloads off these nodes.
   中文翻译：为在 H100 SXM5 上服务 Llama 3.3 70B FP8 的集群设计 Karpenter NodePool。指定 `capacity-type`、`disruption.consolidationPolicy`、`consolidateAfter` 和将非 GPU 工作负载隔离的污点。
3. Your team reports that deployments are stuck in Pending because "GPUs available but pod won't schedule." Diagnose — is this Karpenter, kube-scheduler, or KAI Scheduler? Which metrics confirm?
   中文翻译：你的团队报告部署卡在 Pending 状态因为"GPU 可用但 Pod 无法调度"。诊断——是 Karpenter、kube-scheduler 还是 KAI Scheduler？哪些指标可以确认？
4. Pick a signal to autoscale disaggregated prefill pods and a different signal for decode pods. Justify both.
   中文翻译：选择一个信号来扩缩分离式预填充 Pod，另一个信号用于解码 Pod。为两者提供理由。
5. Compute the cost of the `WhenEmptyOrUnderutilized` consolidation trap on a 24x7 production service that averages 60 request-dropping events/day at P99 TTFT > 10s.
   中文翻译：计算 `WhenEmptyOrUnderutilized` 合并陷阱在 24x7 生产服务上的成本，该服务平均每天 60 次请求丢弃事件，P99 TTFT > 10 秒。

## Key Terms | 术语速查表

| Term / 术语 | What people say / 通俗说法 | What it actually means / 实际含义 |
|------|----------------|------------------------|
| Karpenter | "the node provisioner" / "节点供给器" | Kubernetes node autoscaler; sub-minute provisioning / Kubernetes 节点自动扩缩器；亚分钟级供给 |
| Cluster Autoscaler | "the old scaler" / "旧扩缩器" | Kubernetes node autoscaler predecessor; slower, group-based / K8s 节点扩缩前身；更慢，基于组 |
| KAI Scheduler | "the GPU scheduler" / "GPU 调度器" | Secondary scheduler for gang + topology + queues / 用于 gang + 拓扑 + 队列的二级调度器 |
| Gang scheduling | "all or nothing" / "全有全无" | Schedule N pods atomically or defer all of them / 原子调度 N 个 Pod 或全部推迟 |
| Topology awareness | "rack-aware" / "机架感知" | Place pods based on NVLink/IB/rack placement / 基于 NVLink/IB/机架放置 Pod |
| `DCGM_FI_DEV_GPU_UTIL` | "GPU utilization" / "GPU 利用率" | Duty-cycle metric; NOT a scaling signal for LLMs / 占用率指标；不是 LLM 的扩缩信号 |
| Queue depth | "waiting requests" / "等待请求" | Correct HPA signal for prefill-bound scaling / 预填充扩缩的正确 HPA 信号 |
| KV cache utilization | "memory pressure" / "内存压力" | Correct HPA signal for decode-bound scaling / 解码扩缩的正确 HPA 信号 |
| Consolidation | "Karpenter consolidation" / "Karpenter 合并" | Node termination to cheaper instance type / 终止节点迁移到更便宜实例 |
| `WhenEmpty + 1h` | "safe consolidation" / "安全合并" | Policy that doesn't evict running GPU jobs / 不驱逐运行中 GPU 任务的政策 |

## Further Reading | 延伸阅读

- [KAI Scheduler GitHub](https://github.com/kai-scheduler/KAI-Scheduler) — design docs and configuration examples.
- [Karpenter Disruption Controls](https://karpenter.sh/docs/concepts/disruption/) — consolidation policy semantics and GPU-safe defaults.
- [NVIDIA — Disaggregated LLM Inference on Kubernetes](https://developer.nvidia.com/blog/deploying-disaggregated-llm-inference-workloads-on-kubernetes/) — Dynamo Planner scaling signals.
- [Ray docs — KAI Scheduler for RayClusters](https://docs.ray.io/en/latest/cluster/kubernetes/k8s-ecosystem/kai-scheduler.html) — Ray integration pattern.
- [AWS EKS Compute and Autoscaling Best Practices](https://docs.aws.amazon.com/eks/latest/best-practices/aiml-compute.html) — managed-Kubernetes-specific guidance.
- [llm-d GitHub](https://github.com/llm-d/llm-d) — Workload Variant Autoscaler design.
