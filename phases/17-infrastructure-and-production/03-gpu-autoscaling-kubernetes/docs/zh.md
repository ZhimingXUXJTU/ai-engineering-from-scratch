# Kubernetes 上的 GPU 自动扩缩 — Karpenter、KAI 调度器、Gang 调度 | 自动扩缩 Kubernetes 调度器 GPU

> 三层，不是一层。Karpenter 动态供给节点（不到一分钟，比 Cluster Autoscaler 快 40%）。KAI 调度器处理 gang 调度、拓扑感知和分层队列——它防止 8 中缺 1 的部分分配陷阱，即 7 个节点等待烧钱只缺一个 GPU。应用级自动扩缩器（NVIDIA Dynamo Planner、llm-d Workload Variant Autoscaler）基于推理特定信号进行扩缩——队列深度、KV 缓存利用率——而不是 CPU/DCGM 占用率。经典的 HPA 陷阱是 `DCGM_FI_DEV_GPU_UTIL` 是占用率指标：100% 可能是 10 个请求或 100 个。vLLM 预分配 KV 缓存内存，所以内存永远不会触发缩容。本课程教你组合三层，并避免默认的 Karpenter `WhenEmptyOrUnderutilized` 策略在推理过程中终止运行中的 GPU 作业。

> **【中文解读】** 本节介绍了 GPU 自动扩缩——Kubernetes 上 LLM 推理服务的 GPU 资源自动扩展策略。


**类型：** 学习
**语言：** Python（标准库，模拟队列深度自动扩缩器）
**前置条件：** Phase 17 · 02（推理平台经济学），Phase 17 · 04（vLLM 推理服务内部机制）
**时间：** 约 75 分钟

## 学习目标

- 绘制三层自动扩缩图（节点供给、gang 调度、应用级），并命名每层使用的工具。
- 解释为什么 `DCGM_FI_DEV_GPU_UTIL` 是 vLLM 错误的 HPA 信号，并说出两个替代方案（队列深度、KV 缓存利用率）。
- 描述 gang 调度和 KAI 调度器防止的部分分配失败模式（8 个 GPU 中 7 个空闲）。
- 说出 Karpenter 的合并策略（`WhenEmptyOrUnderutilized`）会终止运行中的 GPU 作业，并说明 2026 年的安全替代方案。

## 问题引入

> **【中文解读】** GPU 自动扩缩在 Kubernetes 上有三个层面的故障模式：(1) HPA 使用错误的信号（GPU 占用率而非队列深度），导致该扩时不扩；(2) Cluster Autoscaler 节点供给太慢，长提示请求超时；(3) 多 GPU 分布式推理时部分分配（7-of-8 trap），7 个 GPU 空转等待第 8 个。三层问题需要三种不同的工具组合解决。

> **【拓展：GPU 集群管理】** 2026 年 Kubernetes 已成为 LLM 推理服务的标准编排平台。NVIDIA DGX Cloud、Google GKE、AWS EKS 都提供 GPU 节点池管理。关键挑战在于 GPU 是昂贵且稀缺的资源（H100 约 $3-4/hr），扩缩决策必须精确——过度供给浪费成本，供给不足影响 SLA。Karpenter + KAI Scheduler 的组合是目前最成熟的 GPU 调度方案。

你的团队在 Kubernetes 上部署了 LLM 服务。你用 `DCGM_FI_DEV_GPU_UTIL` 作为信号设置 HPA。服务在营业时间固定在 100% 利用率。HPA 永远不会扩容——它已经认为你满了。你手动添加一个副本；TTFT 下降。HPA 仍然没有扩容。信号在对你撒谎。

另外，你使用 Cluster Autoscaler 管理节点。凌晨 2 点来了一个 1M token 的提示；集群花 3 分钟供给节点，请求超时。

再次另外，你部署了一个需要跨 2 个节点 8 个 GPU 的 70B 模型。集群有 7 个 GPU 空闲，1 个分散在 3 个节点上。Cluster Autoscaler 为缺失的 1 个 GPU 供给一个节点。7 个节点等待 4 分钟烧钱，同时 Kubernetes 启动最后一个 GPU。

三层，三种不同的失败模式。2026 年的 GPU 感知自动扩缩不是"打开 HPA"。它是组合节点供给、gang 调度和应用信号自动扩缩。

## 核心概念

### 第 1 层 — 节点供给（Karpenter）

> **【中文解读】** 第一层是节点供给。Karpenter 监控待调度的 Pod，在 45-60 秒内按需创建 GPU 节点，比传统 Cluster Autoscaler 快约 40%。关键陷阱是 `WhenEmptyOrUnderutilized` 合并策略——它会终止正在运行推理的 GPU 节点来迁移到更便宜的实例类型，导致请求失败和模型重新加载（5-20 分钟中断）。GPU 池应使用 `WhenEmpty` + `consolidateAfter: 1h` 的安全策略。

Karpenter 监控待调度 Pod 并在约 45-60 秒内供给节点（Cluster Autoscaler 对 GPU 节点通常需要 90-120 秒）。它根据 `NodePool` 约束动态选择实例类型——如果你的 Pod 需要 8 个 H100 而集群没有匹配的节点，Karpenter 直接供给一个，而不是扩展现有组。

**合并陷阱**：Karpenter 的默认 `consolidationPolicy: WhenEmptyOrUnderutilized` 对 GPU 池是危险的。它会终止运行中的 GPU 节点以将 Pod 迁移到更便宜的适当大小实例。对于推理工作负载，这意味着驱逐运行中的请求并在新节点上重新加载 70B 模型。损失是数分钟的容量加上请求失败。

GPU 池的安全设置：

```yaml
disruption:
  consolidationPolicy: WhenEmpty
  consolidateAfter: 1h
```

让 Karpenter 在一小时后合并真正空的节点，但永远不会驱逐运行中的作业。

### 第 2 层 — Gang 调度（KAI 调度器）

> **【中文解读】** 第二层是调度协调。KAI Scheduler 解决 default kube-scheduler 无法处理的三个问题：(1) Gang Scheduling——全有全无调度，8-GPU 推理要么全部启动要么全部等待；(2) 拓扑感知——根据 NVLink/InfiniBand/机架拓扑放置 Pod；(3) 分层队列——多团队竞争同一 GPU 池时按优先级和配额管理。这对于 tensor parallelism 至关重要，因为 DeepSeek-V3 等 MoE 模型的张量必须在同一 NVLink 域内。

> **【拓展：GPU 调度器生态】** 2026 年 GPU 调度器的选择包括 KAI Scheduler（原 Karp，支持 gang + topology + queue）、YuniKorn（Apache 项目，支持队列和抢占）、以及 default kube-scheduler + 设备插件。KAI Scheduler 是唯一原生支持 gang scheduling 的方案，已被 Ray 和 vLLM production-stack 集成。对于需要多 GPU 分布式推理的场景（70B+ 模型），KAI 是必选项。

KAI 调度器（项目"Karp"后更名）处理默认 kube-scheduler 不处理的问题：

**Gang 调度** — 全有全无调度。需要 8 个 GPU 的分布式推理 Pod 要么全部 8 个一起启动，要么都不启动。没有这个，你会遇到部分分配陷阱：8 个 Pod 中 7 个启动，无限等待，烧钱。

**拓扑感知** — 知道哪些 GPU 共享 NVLink，哪些在同一机架上，哪些之间有 InfiniBand。相应地放置 Pod。DeepSeek-V3 67B 的张量并行工作负载必须在一个 NVLink 域内；KAI 调度器尊重这一点。

**分层队列** — 多个团队以优先级和配额竞争同一个 GPU 池。团队 A 的生产紧急情况只有在优先级规则允许时才会被团队 B 的训练作业抢占。

KAI 作为二级调度器与 kube-scheduler 一起部署；你通过注解让工作负载使用它。Ray 和 vLLM production-stack 都已集成。

### 第 3 层 — 应用级信号

> **【中文解读】** 第三层是应用级信号。传统的 `DCGM_FI_DEV_GPU_UTIL` 是 GPU 占用率（duty cycle）指标——100% 可能意味着 10 个请求或 100 个请求，因为 GPU 都在忙碌。vLLM 预分配 KV Cache 内存，即使只有一个请求，内存使用也接近 90%，导致基于内存的 HPA 永远不会缩容。2026 年正确的扩缩信号应该是队列深度、KV Cache 利用率、每副本 P99 TTFT 和 Goodput。

> **【拓展：推理感知自动扩缩】** NVIDIA Dynamo Planner 和 llm-d Workload Variant Autoscaler 是 2026 年专门为 LLM 推理设计的扩缩器。它们直接消费推理引擎的内部指标（队列深度、KV Cache 块使用率），而非通用的 GPU 指标。这种"推理感知"扩缩比传统 HPA 更精确，可将资源利用率提升 30-50%，同时保持 SLA。配合 Karpenter 的快速节点供给，从零到服务的冷启动时间可从 5 分钟降到 1 分钟。

**HPA 陷阱**：`DCGM_FI_DEV_GPU_UTIL` 是占用率指标——它测量 GPU 在每个采样间隔是否在工作。100% 利用率可能意味着 10 个并发请求或 100 个；GPU 无论哪种情况都在忙。基于占用率扩缩就是盲目扩缩。

更糟的是，vLLM 和类似引擎预分配 KV 缓存内存（高达 `--gpu-memory-utilization`）。即使只有一个请求，内存使用也接近 90%。基于内存的 HPA 永远不会缩容。

**2026 年替代信号**：

- 队列深度（等待预填充的请求数）。
- KV 缓存利用率（活跃序列分配的块占比）。
- 每副本 P99 TTFT（你的 SLA 信号）。
- Goodput（满足所有 SLO 的每秒请求数）。

NVIDIA Dynamo Planner 和 llm-d Workload Variant Autoscaler 消费这些信号并扩缩副本。它们完全取代了 LLM 服务的 HPA。

### 何时使用什么

| 扩缩决策 | 工具 |
|---------|------|
| 添加/删除节点 | Karpenter |
| 调度多 GPU 作业 | KAI 调度器 |
| 添加/删除副本 | Dynamo Planner / llm-d WVA（或基于队列深度的自定义 HPA） |
| 选择 GPU 类型 | Karpenter NodePool |
| 抢占低优先级 | KAI 调度器队列 |

> **【拓展：GPU 集群成本优化策略】** GPU 集群成本优化在 2026 年的关键策略包括：(1) Spot Instance——AWS/GCP/Azure 的 GPU Spot 实例可节省 60-70%，但需要处理中断（Karpenter + 热池缓解）；(2) 自动扩缩——Karpenter 在非高峰时段自动缩减节点池，50% 成本节省；(3) GPU 共享——通过 MIG（Multi-Instance GPU）将 H100 切分为多个实例，适合小模型推理；(4) 混合精度——FP8/INT4 量化减少 GPU 内存需求，允许更多并发；(5) 分离式部署——prefill/decode 分离到不同 GPU 类型，30-40% 成本节省。

### 分离式预填充/解码使一切复杂化

> **【中文解读】** 分离式预填充/解码架构（Phase 17·17）进一步增加了扩缩复杂性：预填充 Pod 按队列深度扩缩，解码 Pod 按 KV Cache 压力扩缩。不能在两者之上使用单一 HPA——需要各自独立的扩缩策略。llm-d 将两者暴露为独立的 Kubernetes Service，每个 Service 有自己的 HPA。

> **【拓展：Kubernetes GPU 生态】** 2026 年 Kubernetes GPU 管理的关键组件包括：NVIDIA GPU Operator（自动安装驱动/CUDA/container toolkit）、NVIDIA Device Plugin（GPU 资源发现和分配）、MIG（Multi-Instance GPU，将一张 A100/H100 切分为多个实例）、时间分片（GPU 共享）。结合 Karpenter + KAI Scheduler + Dynamo Planner，可以实现从节点供给到 Pod 调度到副本扩缩的完整 GPU 自动扩缩链。

如果你运行分离式预填充/解码（Phase 17 · 17），你有两种具有不同扩缩触发器的 Pod 类别：预填充 Pod 按队列深度扩缩，解码 Pod 按 KV 缓存压力扩缩。llm-d 将这些暴露为独立的 `Service`，每个角色有自己的 HPA。不要试图在两者前面放一个单一的 HPA。

### 冷启动在这里也很重要

冷启动缓解（Phase 17 · 10）是节点供给时间变得对用户可见的地方。Karpenter 的 45-60 秒预热加上 20GB 模型加载加上引擎初始化意味着从零开始的请求需要 2-5 分钟。为 SLO 关键路径保持热池（`min_workers=1`），或在应用层使用 Modal 风格的检查点。

### 你应该记住的数字

- Karpenter 节点供给：约 45-60s vs Cluster Autoscaler 约 90-120s（GPU 节点）。
- KAI 调度器防止部分分配浪费——8 中缺 7 陷阱。
- `DCGM_FI_DEV_GPU_UTIL` 作为 HPA 信号：有问题；使用队列深度或 KV 利用率。
- Karpenter `WhenEmptyOrUnderutilized`：终止运行中的 GPU 作业。推理使用 `WhenEmpty + consolidateAfter: 1h`。

## 用框架实现

`code/main.py` 在突发 GPU 工作负载上模拟三层自动扩缩器。比较朴素 HPA（占用率）、队列深度 HPA 和 KAI-gang 调度扩缩。报告未满足请求、空闲 GPU 分钟数和综合评分。

## 产出物

本课程产出 `outputs/skill-gpu-autoscaler-plan.md`。给定集群拓扑、工作负载形状和 SLO，它设计三层自动扩缩计划。

## 练习题

1. 运行 `code/main.py`。在突发工作负载下，朴素占用率 HPA 丢弃了多少请求，而队列深度 HPA 捕获了？差异从何而来？
2. 为在 H100 SXM5 上服务 Llama 3.3 70B FP8 的集群设计 Karpenter NodePool。指定 `capacity-type`、`disruption.consolidationPolicy`、`consolidateAfter`，以及保持非 GPU 工作负载离开这些节点的污点。
3. 你的团队报告部署卡在 Pending，因为"GPU 可用但 Pod 无法调度"。诊断——这是 Karpenter、kube-scheduler 还是 KAI 调度器的问题？哪些指标可以确认？
4. 选择一个信号来自动扩缩分离式预填充 Pod，选择不同的信号用于解码 Pod。论证两者。
5. 计算一个 24x7 生产服务上 `WhenEmptyOrUnderutilized` 合并陷阱的成本，该服务平均每天有 60 次请求丢弃事件，P99 TTFT > 10s。

## 术语速查表

| 术语 | 人们常说的 | 实际含义 |
|------|-----------|---------|
| Karpenter | "节点供给器" | Kubernetes 节点自动扩缩器；亚分钟级供给 |
| Cluster Autoscaler | "旧扩缩器" | Kubernetes 节点自动扩缩器前身；较慢，基于组 |
| KAI 调度器 | "GPU 调度器" | 用于 gang + 拓扑 + 队列的二级调度器 |
| Gang 调度 | "全有全无" | 原子调度 N 个 Pod 或推迟全部 |
| 拓扑感知 | "机架感知" | 基于 NVLink/IB/机架放置 Pod |
| `DCGM_FI_DEV_GPU_UTIL` | "GPU 利用率" | 占用率指标；不是 LLM 的扩缩信号 |
| 队列深度 | "等待请求" | 预填充受限扩缩的正确 HPA 信号 |
| KV 缓存利用率 | "内存压力" | 解码受限扩缩的正确 HPA 信号 |
| 合并 | "Karpenter 合并" | 节点终止以迁移到更便宜的实例类型 |
| `WhenEmpty + 1h` | "安全合并" | 不驱逐运行中 GPU 作业的策略 |

## 延伸阅读

- [KAI 调度器 GitHub](https://github.com/kai-scheduler/KAI-Scheduler) — 设计文档和配置示例。
- [Karpenter 中断控制](https://karpenter.sh/docs/concepts/disruption/) — 合并策略语义和 GPU 安全默认值。
- [NVIDIA — Kubernetes 上的分离式 LLM 推理](https://developer.nvidia.com/blog/deploying-disaggregated-llm-inference-workloads-on-kubernetes/) — Dynamo Planner 扩缩信号。
- [Ray 文档 — RayClusters 的 KAI 调度器](https://docs.ray.io/en/latest/cluster/kubernetes/k8s-ecosystem/kai-scheduler.html) — Ray 集成模式。
- [AWS EKS 计算和自动扩缩最佳实践](https://docs.aws.amazon.com/eks/latest/best-practices/aiml-compute.html) — 托管 Kubernetes 特定指南。
- [llm-d GitHub](https://github.com/llm-d/llm-d) — Workload Variant Autoscaler 设计。
