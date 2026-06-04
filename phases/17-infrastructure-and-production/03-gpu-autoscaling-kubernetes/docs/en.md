# GPU Autoscaling on Kubernetes — Karpenter, KAI Scheduler, Gang Scheduling | 自动扩缩 Kubernetes 调度器 GPU

> Three layers, not one. Karpenter provisions nodes dynamically (under one minute, 40% faster than Cluster Autoscaler). KAI Scheduler handles gang scheduling, topology awareness, and hierarchical queues — it prevents the 7-of-8 partial allocation trap where seven nodes wait and burn on one missing GPU. Application-level autoscalers (NVIDIA Dynamo Planner, llm-d Workload Variant Autoscaler) scale on inference-specific signals — queue depth, KV cache utilization — not CPU/DCGM duty cycle. The classic HPA trap is that `DCGM_FI_DEV_GPU_UTIL` is a duty-cycle measurement: 100% could be 10 requests or 100. vLLM pre-allocates KV cache memory, so memory never triggers scale-down. This lesson teaches you to compose the three layers and avoid the default Karpenter `WhenEmptyOrUnderutilized` policy that terminates running GPU jobs mid-inference.

> **【中文解读】** 本节介绍了 GPU 自动扩缩——Kubernetes 上 LLM 推理服务的 GPU 资源自动扩展策略。


**Type:** Learn
**Languages:** Python (stdlib, toy queue-depth autoscaler simulator)
**Prerequisites:** Phase 17 · 02 (Inference Platform Economics), Phase 17 · 04 (vLLM Serving Internals)
**Time:** ~75 minutes

## Learning Objectives | 学习目标

- Diagram the three autoscaling layers (node provisioning, gang scheduling, application-level) and name the tool used at each layer.
- Explain why `DCGM_FI_DEV_GPU_UTIL` is the wrong HPA signal for vLLM and name two replacements (queue depth, KV cache utilization).
- Describe gang scheduling and the partial-allocation failure mode KAI Scheduler prevents (7 of 8 GPUs idle).
- Name the Karpenter consolidation policy (`WhenEmptyOrUnderutilized`) that terminates running GPU jobs and state the 2026 safe alternative.

## The Problem | 问题

> **【中文解读】** GPU 自动扩缩在 Kubernetes 上有三个层面的故障模式：(1) HPA 使用错误的信号（GPU 占用率而非队列深度），导致该扩时不扩；(2) Cluster Autoscaler 节点供给太慢，长提示请求超时；(3) 多 GPU 分布式推理时部分分配（7-of-8 trap），7 个 GPU 空转等待第 8 个。三层问题需要三种不同的工具组合解决。

> **【拓展：GPU 集群管理】** 2026 年 Kubernetes 已成为 LLM 推理服务的标准编排平台。NVIDIA DGX Cloud、Google GKE、AWS EKS 都提供 GPU 节点池管理。关键挑战在于 GPU 是昂贵且稀缺的资源（H100 约 $3-4/hr），扩缩决策必须精确——过度供给浪费成本，供给不足影响 SLA。Karpenter + KAI Scheduler 的组合是目前最成熟的 GPU 调度方案。

Your team ships an LLM-serving service on Kubernetes. You set up HPA with `DCGM_FI_DEV_GPU_UTIL` as the signal. The service pins at 100% utilization during business hours. HPA never scales up — it already thinks you're full. You add a replica manually; TTFT drops. HPA still doesn't scale. The signal is lying to you.

Separately, you use Cluster Autoscaler for nodes. A 1M-token prompt arrives at 2 a.m.; the cluster spends 3 minutes provisioning a node, and the request times out.

Separately again, you deploy a 70B model requiring 8 GPUs across 2 nodes. The cluster has 7 GPUs free and 1 spread across 3 nodes. Cluster Autoscaler provisions a node for the 1 missing GPU. Seven nodes wait 4 minutes burning money while Kubernetes gets the last GPU up.

Three layers, three different failure modes. GPU-aware autoscaling in 2026 is not "turn on HPA." It's composing node provisioning, gang scheduling, and application-signal autoscaling.

## The Concept | 概念

### Layer 1 — node provisioning (Karpenter)

> **【中文解读】** 第一层是节点供给。Karpenter 监控待调度的 Pod，在 45-60 秒内按需创建 GPU 节点，比传统 Cluster Autoscaler 快约 40%。关键陷阱是 `WhenEmptyOrUnderutilized` 合并策略——它会终止正在运行推理的 GPU 节点来迁移到更便宜的实例类型，导致请求失败和模型重新加载（5-20 分钟中断）。GPU 池应使用 `WhenEmpty` + `consolidateAfter: 1h` 的安全策略。

Karpenter watches pending pods and provisions nodes within ~45-60 seconds (Cluster Autoscaler typically takes 90-120 seconds for GPU nodes). It picks instance types dynamically per the `NodePool` constraint — if your pod needs 8 H100s and the cluster has no matching node, Karpenter provisions one directly instead of scaling an existing group.

**The consolidation trap**: Karpenter's default `consolidationPolicy: WhenEmptyOrUnderutilized` is dangerous for GPU pools. It will terminate a running GPU node to migrate pods to a cheaper right-sized instance. For inference workloads that means evicting running requests and reloading a 70B model on the new node. Loss is minutes of capacity plus request failures.

Safe setting for GPU pools:

```yaml
disruption:
  consolidationPolicy: WhenEmpty
  consolidateAfter: 1h
```

Lets Karpenter consolidate truly empty nodes after an hour but never evict a running job.

### Layer 2 — gang scheduling (KAI Scheduler)

> **【中文解读】** 第二层是调度协调。KAI Scheduler 解决 default kube-scheduler 无法处理的三个问题：(1) Gang Scheduling——全有全无调度，8-GPU 推理要么全部启动要么全部等待；(2) 拓扑感知——根据 NVLink/InfiniBand/机架拓扑放置 Pod；(3) 分层队列——多团队竞争同一 GPU 池时按优先级和配额管理。这对于 tensor parallelism 至关重要，因为 DeepSeek-V3 等 MoE 模型的张量必须在同一 NVLink 域内。

> **【拓展：GPU 调度器生态】** 2026 年 GPU 调度器的选择包括 KAI Scheduler（原 Karp，支持 gang + topology + queue）、YuniKorn（Apache 项目，支持队列和抢占）、以及 default kube-scheduler + 设备插件。KAI Scheduler 是唯一原生支持 gang scheduling 的方案，已被 Ray 和 vLLM production-stack 集成。对于需要多 GPU 分布式推理的场景（70B+ 模型），KAI 是必选项。

KAI Scheduler (project "Karp" then renamed) handles what default kube-scheduler does not:

**Gang scheduling** — schedule all-or-nothing. A distributed inference pod requiring 8 GPUs either all 8 start together or none do. Without this, you get the partial-allocation trap: 7 of 8 pods start, wait indefinitely, burn money.

**Topology awareness** — know which GPUs share NVLink, which sit on the same rack, which have InfiniBand between them. Place pods accordingly. A DeepSeek-V3 67B tensor-parallel workload must stay on one NVLink domain; KAI Scheduler respects that.

**Hierarchical queues** — multiple teams compete for the same GPU pool with priority and quota. Team A's production pinch gets preempted by Team B's training job only if priority rules allow.

KAI is deployed alongside kube-scheduler as a secondary scheduler; you annotate workloads to use it. Ray and vLLM production-stack both integrate.

### Layer 3 — application-level signals

> **【中文解读】** 第三层是应用级信号。传统的 `DCGM_FI_DEV_GPU_UTIL` 是 GPU 占用率（duty cycle）指标——100% 可能意味着 10 个请求或 100 个请求，因为 GPU 都在忙碌。vLLM 预分配 KV Cache 内存，即使只有一个请求，内存使用也接近 90%，导致基于内存的 HPA 永远不会缩容。2026 年正确的扩缩信号应该是队列深度、KV Cache 利用率、每副本 P99 TTFT 和 Goodput。

> **【拓展：推理感知自动扩缩】** NVIDIA Dynamo Planner 和 llm-d Workload Variant Autoscaler 是 2026 年专门为 LLM 推理设计的扩缩器。它们直接消费推理引擎的内部指标（队列深度、KV Cache 块使用率），而非通用的 GPU 指标。这种"推理感知"扩缩比传统 HPA 更精确，可将资源利用率提升 30-50%，同时保持 SLA。配合 Karpenter 的快速节点供给，从零到服务的冷启动时间可从 5 分钟降到 1 分钟。

**The HPA trap**: `DCGM_FI_DEV_GPU_UTIL` is a duty-cycle metric — it measures whether the GPU was doing work at each sampling interval. 100% utilization could mean 10 concurrent requests or 100; the GPU was busy either way. Scaling on duty cycle is scaling blindly.

Worse, vLLM and similar engines pre-allocate KV cache memory (up to `--gpu-memory-utilization`). Memory usage stays near 90% even at one request. Memory-based HPA never scales down.

**2026 replacement signals**:

- Queue depth (number of requests waiting for prefill).
- KV cache utilization (what fraction of blocks are allocated to active sequences).
- Per-replica P99 TTFT (your SLA signal).
- Goodput (requests meeting all SLOs per second).

NVIDIA Dynamo Planner and llm-d Workload Variant Autoscaler consume these signals and scale replicas. They replace HPA entirely for LLM serving.

### When to use what

| Scale decision | Tool |
|----------------|------|
| Add/remove nodes | Karpenter |
| Schedule multi-GPU jobs | KAI Scheduler |
| Add/remove replicas | Dynamo Planner / llm-d WVA (or custom HPA on queue depth) |
| Choose GPU type | Karpenter NodePool |
| Preempt low-priority | KAI Scheduler queues |

> **【拓展：GPU 集群成本优化策略】** GPU 集群成本优化在 2026 年的关键策略包括：(1) Spot Instance——AWS/GCP/Azure 的 GPU Spot 实例可节省 60-70%，但需要处理中断（Karpenter + 热池缓解）；(2) 自动扩缩——Karpenter 在非高峰时段自动缩减节点池，50% 成本节省；(3) GPU 共享——通过 MIG（Multi-Instance GPU）将 H100 切分为多个实例，适合小模型推理；(4) 混合精度——FP8/INT4 量化减少 GPU 内存需求，允许更多并发；(5) 分离式部署——prefill/decode 分离到不同 GPU 类型，30-40% 成本节省。

### Disaggregated prefill/decode complicates everything

> **【中文解读】** 分离式预填充/解码架构（Phase 17·17）进一步增加了扩缩复杂性：预填充 Pod 按队列深度扩缩，解码 Pod 按 KV Cache 压力扩缩。不能在两者之上使用单一 HPA——需要各自独立的扩缩策略。llm-d 将两者暴露为独立的 Kubernetes Service，每个 Service 有自己的 HPA。

> **【拓展：Kubernetes GPU 生态】** 2026 年 Kubernetes GPU 管理的关键组件包括：NVIDIA GPU Operator（自动安装驱动/CUDA/container toolkit）、NVIDIA Device Plugin（GPU 资源发现和分配）、MIG（Multi-Instance GPU，将一张 A100/H100 切分为多个实例）、时间分片（GPU 共享）。结合 Karpenter + KAI Scheduler + Dynamo Planner，可以实现从节点供给到 Pod 调度到副本扩缩的完整 GPU 自动扩缩链。

If you run disaggregated prefill/decode (Phase 17 · 17), you have two pod classes with different scaling triggers: prefill pods scale on queue depth, decode pods scale on KV cache pressure. llm-d exposes these as separate `Services` with per-role HPA. Do not try to put a single HPA in front of both.

### Cold start matters here too

Cold-start mitigation (Phase 17 · 10) is where node provisioning time becomes user-visible. Karpenter's 45-60 second warm-up plus a 20GB model load plus engine init means a from-zero request takes 2-5 minutes. Keep a warm pool (`min_workers=1`) for SLO-critical paths, or use Modal-style checkpointing at application layer.

### Numbers you should remember

- Karpenter node provisioning: ~45-60s vs Cluster Autoscaler ~90-120s (GPU nodes).
- KAI Scheduler prevents partial-allocation waste — 7-of-8 trap.
- `DCGM_FI_DEV_GPU_UTIL` as HPA signal: broken; use queue depth or KV utilization.
- Karpenter `WhenEmptyOrUnderutilized`: terminates running GPU jobs. Use `WhenEmpty + consolidateAfter: 1h` for inference.

## Use It | 使用方法

> **【拓展：GPU 自动扩缩成本模型】** GPU 自动扩缩的成本优化核心是减少空转时间。以 H100（$3/hr）为例，8-GPU 集群 24/7 运行每月成本约 $17,280。通过 Karpenter 按需供给 + `WhenEmpty` 合并策略 + 推理感知 HPA，可在非高峰时段自动缩容到 2-GPU，将月成本降至约 $8,640（节省 50%）。Spot Instance 可进一步节省 60-70%，但需要处理中断。

`code/main.py` simulates a three-layer autoscaler on a bursty GPU workload. Compares naive HPA (duty cycle), queue-depth HPA, and KAI-gang-scheduled scaling. Reports unmet requests, idle-GPU minutes, and a composite score.

## Ship It | 部署上线

This lesson produces `outputs/skill-gpu-autoscaler-plan.md`. Given cluster topology, workload shape, and SLO, it designs a three-layer autoscaling plan.

## Exercises | 练习题

1. Run `code/main.py`. Under a bursty workload, how many requests does naive duty-cycle HPA drop that queue-depth HPA catches? Where does the difference come from?
2. Design a Karpenter NodePool for a cluster serving Llama 3.3 70B FP8 on H100 SXM5. Specify `capacity-type`, `disruption.consolidationPolicy`, `consolidateAfter`, and a taint that keeps non-GPU workloads off these nodes.
3. Your team reports that deployments are stuck in Pending because "GPUs available but pod won't schedule." Diagnose — is this Karpenter, kube-scheduler, or KAI Scheduler? Which metrics confirm?
4. Pick a signal to autoscale disaggregated prefill pods and a different signal for decode pods. Justify both.
5. Compute the cost of the `WhenEmptyOrUnderutilized` consolidation trap on a 24x7 production service that averages 60 request-dropping events/day at P99 TTFT > 10s.

## Key Terms | 关键术语

| Term | What people say | What it actually means |
|------|----------------|------------------------|
| Karpenter | "the node provisioner" | Kubernetes node autoscaler; sub-minute provisioning |
| Cluster Autoscaler | "the old scaler" | Kubernetes node autoscaler predecessor; slower, group-based |
| KAI Scheduler | "the GPU scheduler" | Secondary scheduler for gang + topology + queues |
| Gang scheduling | "all or nothing" | Schedule N pods atomically or defer all of them |
| Topology awareness | "rack-aware" | Place pods based on NVLink/IB/rack placement |
| `DCGM_FI_DEV_GPU_UTIL` | "GPU utilization" | Duty-cycle metric; NOT a scaling signal for LLMs |
| Queue depth | "waiting requests" | Correct HPA signal for prefill-bound scaling |
| KV cache utilization | "memory pressure" | Correct HPA signal for decode-bound scaling |
| Consolidation | "Karpenter consolidation" | Node termination to cheaper instance type |
| `WhenEmpty + 1h` | "safe consolidation" | Policy that doesn't evict running GPU jobs |

## Further Reading | 延伸阅读

- [KAI Scheduler GitHub](https://github.com/kai-scheduler/KAI-Scheduler) — design docs and configuration examples.
- [Karpenter Disruption Controls](https://karpenter.sh/docs/concepts/disruption/) — consolidation policy semantics and GPU-safe defaults.
- [NVIDIA — Disaggregated LLM Inference on Kubernetes](https://developer.nvidia.com/blog/deploying-disaggregated-llm-inference-workloads-on-kubernetes/) — Dynamo Planner scaling signals.
- [Ray docs — KAI Scheduler for RayClusters](https://docs.ray.io/en/latest/cluster/kubernetes/k8s-ecosystem/kai-scheduler.html) — Ray integration pattern.
- [AWS EKS Compute and Autoscaling Best Practices](https://docs.aws.amazon.com/eks/latest/best-practices/aiml-compute.html) — managed-Kubernetes-specific guidance.
- [llm-d GitHub](https://github.com/llm-d/llm-d) — Workload Variant Autoscaler design.
