# 卡宾特,卡艾计划器,帮派计划器

> 没有一个层. 卡珀特供应节点动态 (低于1分钟,比集群自动测量器快40%). 卡伊计划器处理团队安排,拓意识和等级队列,它防止7/8的部分分配陷,其中七个节点在一个缺失的GPU上等待和燃烧. 应用级自动量化器 (NVIDIA Dynamo Planner, llm-d Workload Variant Autoscaler) 根据推理特定信号进行量化,排队深度,KV缓存使用,而不是CPU/DCGM工作周期. 经典的HPA陷是这样的`DCGM_FI_DEV_GPU_UTIL`作为一个任务周期测量:100%可以是10个请求或100个. vLLM预先分配KV缓存,所以内存永远不会触发缩放.`WhenEmptyOrUnderutilized`在线用户在线用户在线用户在线用户在线用户在线用户在线用户在线用户在线用户在线用户在线用户在线用户在线用户在线用户在线用户在线用户在线用户在线用户在线用户在线用户在线用户在线用户在线用户在线用户在线用户在线用户在线用户在线用户在线用户在线用户在线用户在线用户在线用户在线用户在线用户在线用户在线用户在线用户在线用户在线用户在线用户在线用户在线用户在线用户在线用户在线用户在线用户在线用户在线用户在线用户在线用户在线用户在线用户在线用户在线用户在线用户在线用户在线用户在线用户在线用户在线用户在线用户在线用户网站网站网站网站网站网站网站网站网站网站网站网站网站网站网站网站网站网站网站网站网站网站网站网站网站网站网站网站网站网站网站网站网站网站网站网站网站网站网站网站网站网站网站网站网站网站网站网站网站网站网站网站网站网站网站网站网站网站网站网站网站网站网站网站网站网站网站网站网站网站网站网站网站网站网站网站网站网站网站网站网站网站网站网站网站网站网站网站网站网站网站网站网站网站网站网站网站网站网站网站网站网站网站网站网站网站网站网站网站网站网站网站网站网站网站网站网站网站网站网站网站网站网站网站网站网站网站网站网站网站网站网站网站网站网站网站网站网站网站网站网站网站网站网站网站网站网站网站网站网站网站网站网站网站网站网站网站网站网站网站网站网站网站网站网站网站网站网站网站网站网站网站网站网站网站网站网站网站网站网站网站网站网站网站网站网站网站网站网站网站网站网站网站网站网站网站网站网站网站网站网站网站网站网站网站网站网站网站网站网站网站网站网站网站网站网站网站网站网站网站网站网站网站网站网站网站网站网站网站网站网站网站网站网站网站网站网站网站网站网站网站网站网站网站网站网站网站网站网站网站网站网站网站

> **【中文解读】**本节介绍了GPU自动扩展策略.
**Type:** Learn
**Languages:** Python (stdlib, toy queue-depth autoscaler simulator)
**Prerequisites:** Phase 17 · 02 (Inference Platform Economics), Phase 17 · 04 (Serving Engine Internals)
**Time:** ~75 minutes


**Type:** Learn | **类型:** 学习
**Languages:** Python (stdlib, toy queue-depth autoscaler simulator) | **语言:** Python（标准库，队列深度自动扩缩模拟器）
**Prerequisites:** Phase 17 · 02 (Inference Platform Economics), Phase 17 · 04 (vLLM Serving Internals) | **前置知识:** Phase 17 · 02（推理平台经济学）, Phase 17 · 04（vLLM 服务内部）

>  **【前置】**学本节前请先掌握:阶段17·02(平台经济学)、阶段17·04(vLLM)、Kubernetes 基础──三层扩缩:卡普中心(节点层)+KAI 计划器(Pod 层帮派计划)+应用层(队列深度/KV利用率)──
>  **【类比】**扩缩 = "餐厅运力调度"――卡普中心 = 开新店(分钟级);KAI = 桌位组合(帮派安排 防 7/8 部分分配,7 桌等 1 桌);应用层 = 服务员按等位队列长度调度座座。HPA 陷:DCGM利用率是占空比,100%可能是10个或100个请求必须使用Goodput(Phase 17·08) 替代──

## 学习目标

- 绘制三个自动扩展层 (节点配置,团队安排,应用级别) 并命名每个层使用的工具.
  中文翻译:绘制三层自动扩缩层 (节点供应,帮调度,应用级) 并命名每个层使用的工具――
- 解释原因`DCGM_FI_DEV_GPU_UTIL`是vLLM的错误HPA信号,并命名两个替代 (排队深度,KV缓存使用).
  中文翻译:解释为什么`DCGM_FI_DEV_GPU_UTIL`是vLLM 错误的HPA信号,并说出两个替代方案.
- 描述团队规划和部分分配故障模式 KAI Scheduler 防止 (7 个8 个GPU 置).
  中文翻译:描述帮派调度和KAI调度器 防止部分分配故障模式(8个GPU中7个空) ⋅
- 提及卡珀特集团政策 (`WhenEmptyOrUnderutilized`) 终止GPU工作,并指出2026年安全的替代方案.
  中文翻译:说出终止正在运行GPU任务的卡宾特 合并策略(`WhenEmptyOrUnderutilized`),并说明2026年安全替代方案.

## 问题 问题引入

> **【中文解读】**在 Kubernetes 上有三个层次的故障模式: 1) HPA 使用错误的信号(GPU 占用率而不是队列深度),导致该扩张时不扩张; 2) 集群自动扩展节点供应太慢,长提示请求超时; 3) 多 GPU 分布推理时部分分配;; 7- of-8 陷),7 个 GPU 空转等第 8 个.

> **【拓展：GPU 集群管理】**2026年,Kubernetes 已成为LLM推理服务的标准编排平台.NVIDIA DGX Cloud,Google GKE,AWS EKS 都提供GPU节点池管理.关键挑战在于GPU是昂贵且稀缺的资源.

你的团队在Kubernetes上提供了法学服务.`DCGM_FI_DEV_GPU_UTIL`现在,我们在电脑上看到一个电脑,它可以使用它,它可以使用它,它可以使用它,它可以使用它,它可以使用它,它可以使用它,它可以使用它,它可以使用它,它可以使用它,它可以使用它,它可以使用它,它可以使用它,它可以使用它,它可以使用它,它可以使用它,它可以使用它,它可以使用它,它可以使用它,它可以使用它,它可以使用它,它可以使用它,它可以使用它,它可以使用它,它可以使用它,它可以使用它,它可以使用它,它可以使用它,它可以使用它,它可以使用它,它可以使用它,它可以使用它,它可以使用它,它可以使用它,它可以使用它,它可以使用它,它可以使用它,它可以使用它,它可以使用它,它可以使用它,它可以使用它,它可以使用它,它可以使用它,它可以使用它,它可以使用它,它可以使用它,它可以使用它,它可以使用它,它可以使用它,它可以使用它,它可以使用它,它可以使用它,它可以使用它,它可以使用它,它可以使用它,它可以使用它,它可以使用它可以使用它,它可以使用它,它可以使用它,它可以使用它可以使用它,它可以使用它,它可以使用它,它可以使用它可以使用它,它可以使用它,它可以使用它可以使用它.

> 你的团队在库伯内特斯部署了法学士服务.`DCGM_FI_DEV_GPU_UTIL`作为信号设置了HPA──服务在业务时段保持100%的利用率──HPA 从不扩容它认为你已经满了──你手动添加一副本;TTFT下降──HPA 仍然不扩容──信号在欺骗你──

单独使用 Cluster Autoscaler 为节点. 一个 1M-代币提示到达凌晨2点; 集群花费3分钟的节点配置, 请求时间.

> 另一方面,你使用 Cluster Autoscaler 管理节点――凌晨2点来一个1M代币的提示;集群花3分钟供应节点,请求超时――

单独的,你部署一个70B模型需要8个GPU在2个节点上.集群有7个GPU免费和1个分布在3个节点上.集群自动测量器为1个缺失的GPU提供一个节点.七个节点等待4分钟燃烧钱,而Kubernetes得到最后一个GPU.

> 再一次,你部署了一个需要2个节点的70B模型8个GPU.集群有7个GPU空,1个分散在3个节点上.集群自动缩放器为缺少的1个GPU提供一个节点.

两个层,三个不同的故障模式. 2026年 GPU 意识到自动扩展不是"启动HPA". 它是构成节点配置,团队规划,和应用信号自动扩展.

> 三层,三种不同的故障模式――2026年GPU感知自动扩展不是"打开HPA"――它是组合节点供应、带调度和应用信号自动扩展――

## 概念的核心概念

### 层1 节点供应 (卡普门特)

> **【中文解读】**卡普内特 监控调节的Pod,在 45-60 秒内按需创建 GPU 节点,比传统的集群自动测量器快约 40% .`WhenEmptyOrUnderutilized`合并策略 它将停止运行推理的GPU节点转移到更便宜的实例类型,导致请求失败和模型重新加载(5-20分钟中断) ・GPU池应使用`WhenEmpty`其他`consolidateAfter: 1h`安全策略.

卡宾特在45-60秒内观察待定的 pods和储备节点 (集群自动测量器通常需要90-120秒用于GPU节点).它根据数据的动态选择实例类型.`NodePool`限制如果你的小组需要8个H100,并且集群没有匹配的节点,

> 卡珀特 监控调节的Pod,在约45-60秒内供应节点(集群自动缩放器对 GPU节点通常需要90-120秒) ⋅根据`NodePool`约束动态选择实例类型 如果你的 Pod 需要8个 H100 且集群没有匹配节点,卡普内特 直接提供一个,而不是扩展现有组组──

**The consolidation trap**卡宾特的默认`consolidationPolicy: WhenEmptyOrUnderutilized`对于 GPU 池来说,它会终止运行 GPU 节点,将 pods 迁移到更便宜的正确尺寸实例.对于推断工作负载,这意味着驱逐运行请求和重新加载70B 模型在新节点上.损失是数分钟的容量加上请求失败.

> **合并陷阱**卡普特的默认`consolidationPolicy: WhenEmptyOrUnderutilized`对GPU池很危险.它将停止运行的GPU节点,将将Pod迁移到更便宜的合适实例.对于推理工作负载,这意味着驱逐运行中的请求,并在新节点上重新加载70B模型.损失是数分钟的容量加上请求失败.

对于GPU池的安全设置:

```yaml
disruption:
  consolidationPolicy: WhenEmpty
  consolidateAfter: 1h
```

让卡宾特在一个小时后整合真正空的节点,但从来没有驱逐出一个正在运行的工作.

> 让卡珀特在一小时后合并真正空中的节点,但永远不驱逐运行中的任务.

### 层2 帮派安排 (KAI安排器)

> **【中文解读】**第二层是调度协调――KAI 调度器 解决默认的be-scheduler 无法处理的三个问题: 1) 团队调度全有全无调度, 8-GPU 推理要么全部启动要么全部等待; 2) 拓感知根据NVLink/InfiniBand/机架拓放置 Pod; 3) 分层队列多团队竞争同一个NVLink 池时按优先级和配额管理.

> **【拓展：GPU 调度器生态】**2026年GPU调度器的选择包括KAI调度器(原卡普,支持帮+拓+排队)、YuniKorn(Apache 项目,支持队列和抢占)、以及默认的Kube-调度器+设备插件。KAI调度器是唯一原生支持帮派调度方案,已被Ray 和 vLLM生产堆积集成──对于需要的GPU 分布式推理场景(70B+模型),KAI 是必选项──

卡伊定制器 (随后改名为"卡普"项目) 处理默认的 kube-scheduler 不:

**Gang scheduling**计划所有或什么都.一个需要8个GPU的分布式推理器,或者8个GPU都开始在一起,或者没有.没有这个,你得到了部分分配陷:8个子中的7个开始,等待无限时间,烧钱.

**Topology awareness**知道哪些GPU共享NVLink,这些GPU都坐在同一架子上,它们之间有InfiniBand. 根据此,放置 pods.一个DeepSeek-V3 67B的子平行工作负载必须保持在一个NVLink域;KAI Scheduler尊重这一点.

**Hierarchical queues**多个团队以优先级和配额竞争同一个GPU池.A团队的生产只会在优先规则允许的情况下被B团队的训练工作先进.

作为二级调度器,KAI与 kube-scheduler一起部署;您注释工作负载使用它.Ray和vLLM生产堆都集成.

> 作为二级调度器和be-scheduler 一起部署;你通过注解让工作负载使用它――Ray 和 vLLM生产堆都集成――

### 层3 应用级信号

> **【中文解读】**第三层是应用级信号.`DCGM_FI_DEV_GPU_UTIL`是GPU占用率 (任务周期) 指标100%可能意味着10个请求或100个请求,因为GPU都忙碌了.vLLM预分配KV缓存内存,即使只有一个请求,内存使用也接近90%,导致基于内存的HPA永远不会缩放容量.

> **【拓展：推理感知自动扩缩】**纳维达动态计划器和 llm-d 工作负载变量自动缩放器是2026年专门用于LLM推理设计的扩展器.它们直接消费推理引擎的内部指标.

**The HPA trap**其他`DCGM_FI_DEV_GPU_UTIL`测量GPU是否在每个样本中段工作.100%的利用可能意味着10个同时请求或100个;GPU无论如何都忙.在工作周期上进行扩展是盲目扩展.

更糟糕的是,vLLM和类似的引擎预先分配KV缓存 (高达 `--gpu-memory-utilization`记忆使用率即使是一次请求,也保持接近90%.

**2026 replacement signals**其他:

- 排队深度 (等待预填的请求数量).
  中文翻译:队列深度 (等待预填充的请求数量)
- 存储器存储器使用量 (区块的多少分量被分配到活跃序列中).
  中文翻译:KV 缓存利用率 (缓存利用率) 分配给活跃序列的块比例) ⋅
- 按复制 P99 TTFT (您的SLA信号).
  中文翻译:每副本 P99 TTFT(你的SLA 信号) 』
- 产量 (每秒满足所有SLO的要求).
  中文翻译:Goodput(每秒满足所有SLO的请求数)。

根据NVIDIA 动态规划器和 llm-d 工作负载变量自动测量器的使用,它们完全取代了HPA.

> 消费这些信号并扩缩副本──它们完全取代了LLM服务中的HPA──

### 什么时候使用

| Scale decision / 扩缩决策 | Tool / 工具 |
|----------------|------|
| Add/remove nodes / 添加/移除节点 | Karpenter |
| Schedule multi-GPU jobs / 调度多 GPU 任务 | KAI Scheduler |
| Add/remove replicas / 添加/移除副本 | Dynamo Planner / llm-d WVA (or custom HPA on queue depth) |
| Choose GPU type / 选择 GPU 类型 | Karpenter NodePool |
| Preempt low-priority / 抢占低优先级 | KAI Scheduler queues |

> **【拓展：GPU 集群成本优化策略】** GPU集群成本优化2026年关键策略包括:(1) Spot InstanceAWS/GCP/Azure的 GPU Spot实例可节省60-70%,但需要处理中断(卡普林+热池缓解);(2) 自动扩展卡普林在非高峰时段自动缩减节点池,50%的成本节省;(3) GPU共享通过MIG(多实例 GPU) 将H100分为多个实例,适合小模型推;(4) 混合FP8/INT4 量化减少内存需求,允许更多并发;(5) 分离式部署预填/解码 分离到不同本类的 GPU,30-40% 成本节省.

### 解密的预填/解码复杂化了一切

> **【中文解读】**分离式预填/解码架构 (Phase 17·17) 进一步增加了扩张复杂性:预填Pod 按队列深度扩张,解码Pod 按KV缓存压力扩张――不能在两者上使用单个HPA需要各自独立的扩张策略――llm-d将两者暴露为独立的Kubernetes服务,每个服务都有自己的HPA――

> **【拓展：Kubernetes GPU 生态】**2026年Kubernetes GPU 管理的关键组件包括:NVIDIA GPU 运营商(自动安装驱动/CUDA/容器工具包) 、NVIDIA 设备插件(GPU 资源发现和分配) 、MIG(多实例 GPU,将一张A100/H100 切分为多个实例) 、时间分片(GPU 共享) ──结合Karpenter + KAI 计划器 + 动态计划器,可实现从节点给到Pod 调度到副本扩展的完整 GPU 自动扩展链──

如果运行分类的预填/解码 (阶段17·17),则有两个类,具有不同的扩展触发器:排列深度的预填尺度,KV缓存压力上的解码尺度. llm-d将这些分开.`Services`试着把一个HPA放在两者面前.

> 如果运行分离式预填/解码(17期 · 17期),你有两个具有不同扩缩触发器的Pod 类型:预填Pod 按队列深度扩充,解码Pod 按KV 缓存压力扩充.llm-d将它们暴露为独立的`Services`没有任何一个角色的HPA.

### 寒冷开始也在这个地方重要

卡宾特的45-60秒加热加上20GB模型负载加上发动机 init意味着零请求需要2-5分钟.保持一个温暖的池 (`min_workers=1`) 对于SLO关键路径,或在应用层使用Modal样式的检查点.

> 冷启动缓解(17 · 10) 是节点供应时间变得用户可感知的地方──卡普中心的45-60秒预热加上20GB 模型加上引擎初始化意味着从零开始的请求需要2-5分钟──对SLO 关键路径保持热池(`min_workers=1`),或在应用层使用模拟风格的检查点.

### 你应该记住的数字

- 卡珀特节点供应: ~ 45-60s vs 集群自动测量器 ~ 90-120s (GPU节点).
  中文翻译:卡巴特节点供应:约45-60秒对集群自动测量器约90-120秒(GPU节点) 』
- 卡伊计划器防止部分分配废物 7/8陷.
  中文翻译:KAI 规划器 防止部分分配浪费7/8陷──
- `DCGM_FI_DEV_GPU_UTIL`作为HPA信号:断裂;使用队列深度或KV利用.
  翻译: 中文`DCGM_FI_DEV_GPU_UTIL`作为HPA信号:有缺陷;使用队列深度或KV利用率──
- 匠`WhenEmptyOrUnderutilized`停止运行GPU工作. 使用`WhenEmpty + consolidateAfter: 1h`为了推断.
  中文翻译:石`WhenEmptyOrUnderutilized`终止运行中的GPU任务.`WhenEmpty + consolidateAfter: 1h`,我知道.

## 用它实现框架

> **【拓展：GPU 自动扩缩成本模型】** GPU自动扩展的成本优化核心是减少空转时间.$3/hr）为例，8-GPU 集群 24/7 运行每月成本约 $17,280──通过卡珀特尔按需供应`WhenEmpty`合并策略 + 推理感知HPA,可在非高峰时段自动缩小容量到2GPU,将月成本降至约8,640美元 (节省50%).
```figure
autoscaling
```

## 用它

`code/main.py`模拟一个在一个破裂的GPU工作负载上进行三层自动扩展器. 进行了天真的HPA (职务周期),排队深度HPA和KAI团队计划的扩展. 报告未满的请求,空置GPU分钟和复合分数.

> `code/main.py`在突发 GPU 工作负载上模拟三层自动扩缩机――比较简单的 HPA(占用率) 、队列深度 HPA 和 KAI 调度扩缩――报告未满足的请求数、空 GPU 分钟数和综合评分分――

## 运送它.

这一课产生了`outputs/skill-gpu-autoscaler-plan.md`鉴于集群拓,工作负载形状和SLO,它设计了一个三层的自动扩展计划.

> 本课产出发 `outputs/skill-gpu-autoscaler-plan.md`△给定集群拓、工作负载形状和SLO,设计三层自动扩展方案.

## 练习题

1. 跑步`code/main.py`在一个繁忙的工作量下, 无辜的职务周期HPA会放下排队深度HPA捕获的请求? 区别来自于什么?
   中文翻译:运行 `code/main.py`在突发工作负载下,简单占用率HPA 丢弃了多少请求被队列深度HPA 捕获?差异来自何?
2. 设计一个Karpenter NodePool,用于H100 SXM5上服务Llama 3.3 70B FP8的集群. 指定 `capacity-type`现在`disruption.consolidationPolicy`现在`consolidateAfter`并且可以将非GPU工作负载远离这些节点.
   中文翻译:为在H100 SXM5 上服务 Llama 3.3 70B FP8 的集群设计 卡珀特 NodePool──指定 `capacity-type`,我知道.`disruption.consolidationPolicy`,我知道.`consolidateAfter`和将非GPU工作负载隔离污点.
3. 诊断 是卡宾特,Kube-Scheduler,或KAI Scheduler?哪些指标证实?
   中文翻译:你的团队报告部署卡在等待状态因为"GPU可用但Pod无法调度"――诊断是卡宾特,布-调度器还是KAI调度器?
4. 选择一个信号,以自动化分类的预填和一个不同的信号,以解码.
   中文翻译:选择一个信号来扩大分离式预填充Pod,另一个信号用于解码Pod──为两者提供理由──
5. 计算成本`WhenEmptyOrUnderutilized`在24×7生产服务中,平均每天有60次请求降低事件,P99 TTFT>10s.
   中文翻译:计算`WhenEmptyOrUnderutilized`合并陷在24x7生产服务上的成本,该服务平均每天60次请求丢弃事件,P99 TTFT > 10秒.

## 关键词 快速查找表

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

## 继续阅读 继续阅读

- [KAI Scheduler GitHub](https://github.com/kai-scheduler/KAI-Scheduler)设计文件和配置示例.
- [Karpenter Disruption Controls](https://karpenter.sh/docs/concepts/disruption/)整合政策语义和GPU安全的默认.
- [NVIDIA — Disaggregated LLM Inference on Kubernetes](https://developer.nvidia.com/blog/deploying-disaggregated-llm-inference-workloads-on-kubernetes/) 动力计划器扩展信号.
- [Ray docs — KAI Scheduler for RayClusters](https://docs.ray.io/en/latest/cluster/kubernetes/k8s-ecosystem/kai-scheduler.html)射线集成模式.
- [AWS EKS Compute and Autoscaling Best Practices](https://docs.aws.amazon.com/eks/latest/best-practices/aiml-compute.html)管理-库伯内特斯具体指导.
- [llm-d GitHub](https://github.com/llm-d/llm-d) 工作负载变量自动尺设计.
