# 服务器无服务器LLM的冷启动缓解服务器LLM

> 20 GB 模型图像需要5-10分钟 (7B) 到20+分钟 (70B) 从冷到服务. 在一个真正的无服务器世界里,这不是一个热点, 减轻功能在五层运行:预种的节点图像 (AWS上的Bottlerocket,双体弧),模型流 (NVIDIA Run:ai Model Streamer,本地在vLLM中),GPU内存快照 (Modal检查站,重启速度高达10倍),热池 (`min_workers=1`),层次加载 (ServerlessLLM的NVMe→DRAM→HBM管道,10-200x延迟降低),以及移动输入代币 (KB) 而不是KV缓存 (GB) 的现场迁移.Modal将2~4s冷开始作为一个层次;Baseten 5-10s默认,以预加热为次.本课程教你测量,预算和堆叠五层.

> **【中文解读】**本节介绍了冷启动缓解 减少 LLM 推理服务首次响应延迟的策略.


**Type:** Learn | **类型:** 学习
**Languages:** Python (stdlib, toy cold-start path simulator) | **语言:** Python
**Prerequisites:** Phase 17 · 02 (Inference Platform Economics), Phase 17 · 03 (GPU Autoscaling) | **前置知识:** Phase 17 · 02 (Inference Platform Economics), Phase 17 · 03 (GPU Autoscaling)

>  **【前置】**学本节前请先掌握:阶段17·02(平台经济学) 阶段17·03(GPU 扩缩) ・无服务器LLM冷启动 = 5-20 分钟(不是热身,是停服)
>  **【类比】**冷启动缓解 = "汽车预热"──朴素加载 = 钥匙一从零启动(20分钟);五层加速:(1) 预热节点镜像;(2) 模型流式加载;(3) GPU 内存快照(Modal 10 倍提速);(4) 暖池 min_workers=1;(5) 分层加载(ServerlessLLM NVMe→DRAM→HBM,10-200倍延迟降低)──Modal实测 2-4 秒冷启动,Baseten 5-10 秒预热版亚秒)。
**Time:** ~60 minutes | **时间:** ~60 minutes

## 学习目标

- 列出冷启动减轻五层,并在每个层中指定一个工具或模式.
  中文翻译:列举冷启动缓解的五层策略,并说出每个层次的一个工具或模式.
- 计算70B型号的冷启动时间总数为 (节点提供) + (重量下载) + (重量加载到HBM) + (发动机初始).
  中文翻译:计算 70B 模型总冷启动时间 = 节点供应 + 权重下载 + 权重加载到HBM + 引擎初始化――
- 解释为什么直播迁移传输输入代币 (KB) 而不是KV缓存 (GB) 以及惩罚是什么 (重新计算).
  中文翻译:解释为什么实时迁移传输输入代币(KB) 而不是KV 缓存(GB),以及代价是什么(重新计算)。
- 指定热池交易 (为空置GPU付款或接受冷启动尾) 和 SLA 门值`min_workers > 0`成为强制性的.
  中文翻译:说出热池权衡 ((为空 GPU 付费或接受冷启动尾部),以及`min_workers > 0`变为强制性的SLA 值──

## 问题 问题引入

> **【中文解读】**无服务器LLM端点的冷启动问题:70B 模型从零到服务需要3-8分钟(节点供应45-60s + 容器拉取120-300s +权重加载45-120s + 引擎初始化10-30s),远超2s的SLA──解决方案是保留热池(min_workers=1),但这意味着24/7 支付空 GPU 费用5个产品各保留1个热副本,每月3600 GPU-小时 无论是否有用户调调.

> **【拓展：Serverless LLM 平台对比】**2026年无服务器LLM 平台的冷启动表现:Modal 凭借GPU 快照技术实现 2-4s冷启动(业界最快);Baseten 默认 5-10s,预加热后可低于 1s;AWS Lambda + 容器镜像通常10-30s(不包含模型加载);GCP云运行 + GPU 较新,冷启动约15-30s──对于TTFT P99 < 60s 的 70B+ 模型,热池是强制性的没有任何冷启动优化能在 60s内完成全流程──

你的无服务器LLM终点在一夜之间变得零.

> 你的无服务器 LLM 端点在夜间缩小容量到零.

1. 卡宾特提供一个GPU节点: 45-60s.
   中文翻译:卡普特供给GPU节点:45-60秒.
2. 容器可以拍摄30GB的图像,重量为120-300s.
   中文翻译:容器拉取 30GB 的含权重镜像:120-300秒.
3. 发动机将重量加载到HBM:根据模型大小和存储速度45-120s.
   中文翻译:引擎将权重加载到HBM:45-120秒,取决于模型大小和存储速度.
4. 存器: 10-30s.
   中文翻译:vLLM 或 TRT-LLM 初始化 CUDA图片、KV 缓存池、分词器:10-30秒──

总数: 220-510s (约3-8分钟) 在一个代币回来之前.你的SLA是2s.你发送一个热池 (`min_workers=1`现在你支付一个空置的GPU24x7. 如果你的服务有5个产品,每个产品都有一个热复制,那么5 × 24 × 30 =3600个GPU-小时/月,无论一个用户是否打电话.

> 总计:220-510秒 (约3-8分钟)才能回归一个代币.`min_workers=1`) 问题似乎消失了但现在你24/7为空GPU付费. 如果你的服务有5个产品,每一个热副本,那么5 × 24 × 30 =3,600个GPU-小时/月,无论用户是否使用.

缓解冷启动是如何保持无服务器经济,同时近似始终开放的延迟.

> 缓解冷启动是保持无服务器经济性的同时接近常驻服务的延迟.

## 概念的核心概念

### 层1 预种节点图像 (Bottlerocket)

> **【中文解读】**第一层预播种节点镜像──AWS Bottlerocket的双卷架构将操作系统与数据分离──将容器镜像(含模型权重)预到数据卷快照中,在 `EC2NodeClass`中引用快照 ID──新节点启动时权重已在本地NVMe上消除镜像拉取步骤,为大型模型节省 2-4 分钟──GCP和Azure有类似的自定义VM 镜像模式──

在 AWS 上,Bottlerocket 的双体积架构将操作系统与数据分开.`EC2NodeClass`通过NVMe,新节点启动,并且已经在本地NVMe上重量了. 步骤2和3的部分消失. 与卡宾特本土操作.

> 在 AWS 上,Bottlerocket的双卷架构将操作系统与数据分离.`EC2NodeClass`中引用快照 ID──新节点启动时权重已在本地NVMe 上步骤 2 和部分步骤 3 消除──原生与卡宾特配合──典型节省:大型模型每次冷启动 2-4 分钟──

在GCP上:有预备容器层的自定义VM图像.在Azure上:有相同模式的管理磁盘快照.

> 预容器层的自定义VM镜像――Azure:托管磁盘快照加相同模式――

### 层2 模式流 (Run:ai模型流器)

> **【中文解读】**第二层模型流式加载――NVIDIA Run:ai Model Streamer 不需要等整个文件加载完才开始服务,而是将权重逐层流式加载到GPU内存,并在第一个变压器块加载完成后就开始处理――2026年 vLLM 原生支持此功能――兼容S3、GCS 和本地 NVMe――通过重叠I/O和计算设置,可将大型模型的权重加载时间减半――

在回答第一个请求之前,不要加载完整的文件,而是将权重流入GPU内存层次,并立即开始处理,当第一个变压器区块成为居民.NVIDIA Run:ai Model Streamer在 vLLM 2026 中原生.它与S3,GCS和本地NVMe合作.通过重叠I/O和计算设置,大型模型的权重加载时间大约减少了一半.

> 不需要在回答第一个请求之前加载完整文件,而是将权重逐层流式加载到GPU内存,并在第一个变压器块加载完成后立即开始处理.

### 层3  GPU内存快照 (Modal)

> **【中文解读】**第三层GPU 内存快照――Modal 在第一次加载后对 GPU 状态进行检查点,后续重启直接反序列化到 HBM比重启动快 10x――这是"2秒启动热 GPU"最接近的技术――代价是快照与 GPU 拓绑定如果卡宾特将你迁移到不同的 SKU,需要重建快照――

> **【拓展：冷启动优化策略叠加】**五层冷启动缓解可叠加使用:(1) 预播种镜像(消除镜像拉取) + (2) 模型流式加载(减重重量加载时间) + (3) GPU 快照(消除重重重量加载) + (4) 热池(避免冷启动) + (5) 分层加载(NVMe→DRAM→HBM) 。全叠加可将70B 模型从328s冷启动降至约15s22x改善。选择哪几层取决于SLA 严格程度和预算。

后续重启将直接消散到HBM  10倍快于重新启动.这是"在2秒内启动热的GPU"的最接近点.

> 后续重启直接反序列化到HBM比重启动快10倍――这是"2秒启动热GPU"最接近的技术――代价:快照与GPU拓绑定,如果卡珀特搬到不同的SKU需要重制快照――

### 层4 热池 (min_workers=1)

> **【拓展：Serverless LLM 平台的冷启动对比】**2026年无服务器LLM 平台的冷启动表现:Modal 以 GPU 快照技术实现 2-4s(业界最快);Baseten 默认 5-10s,预加热后 <1s;AWS Lambda + 容器镜像通常 10-30s(不含模型加载);原始 70B 模型冷启动 3-8 分钟.

简单的减轻:总是准备好一个复制品.成本是1GPU的小时速24x7.$0.85-$为了避免30s冷开始,每小时1.50美元) 和宽松的大型 (为了避免5分钟冷开始,每小时付4美元).温池成为强制性的SLA门:通常在70B+模型上是TTFT P99 <60s.

> 最简单的缓解:保持一个副本始终就绪.$0.85-$1,50/小时以避免30秒冷启动),大模型则相对友好(付 $4/小时以避免5分钟冷启动) ――热池变为强制性SLA 值:通常是70B+ 模型上TTFT P99 < 60秒──

### 五层 层次加载 (ServerlessLLM)

服务器无LLM将存储视为一个层次结构:NVMe (快速但大),DRAM (中型但层次),HBM (小但即时).重量预装到DRAM;按需加载到HBM.纸报告了冷负载上的延迟减少10-200倍,而无明的磁盘到HBM.生产采用是早期的,但与vLLM的集成存在.

> 无服务器LLM将存储视为层级:NVMe(快但大)、DRAM(中等但分层)、HBM(小但即时)。权重预加载到DRAM;按需加载到HBM。论文报告冷启动延迟降低10-200倍──生产采用早,但已经存在与vLLM的集成──

### 层6 直播迁移 (奖金模式)

当一个节点不可用时 (点驱逐,节点排泄),传统模式是冷启动另一个复制和排泄请求队列.直播迁移将输入代币 (千字节) 移动到一个目标地带,该模型被加载,并重新计算KV缓存.重新计算比网络上传输GBKV缓存便宜.适用于分类部署.

> 当节点不可用时(Spot 中断、节点排空),传统模式是冷启动另一个副本并排空请求队列──实时迁移将输入代币(千字节) 移到已载模型的目标节点,并重新计算 KV 缓存──重新计算通过网络传输 GB 级 KV 缓存更便宜──适用于分离式部署──

### 热池的数学

> **【中文解读】**热池数学:对于P99 TTFT SLA 为2s 的服务,问题不是"热池是/没有"而是"多少热副本、哪些路径需要"──高价值交互路径 ((实时聊天、语音代理)→ min_workers=1-2;后台批处理路径(夜间分类)→规模到零可接受;高级层级 →按租户专用热副本。简单算术:5个产品每 1 热副本 = 5 × 24 × 30 = 3600 GPU-小时/月,无论是否有用户调用──

对于一个 P99 TTFT SLA 的服务,问题不是"热池是/不是"而是"有多少热复制品,哪些路径得到它们".

> 对于P99 TTFT SLA 为2秒的服务,问题不是"热池是/没有"而是"多少热副本,哪些路径需要它们"――

- 高价值互动路径 (直播聊天,语音代理): `min_workers=1-2`现在,我们要去.
  中文翻译:高价值交互路径 ((实时聊天、语音代理):`min_workers=1-2`,我知道.
- 背景批量路径 (夜间分类):接受从规模到零,可承受5至10分钟冷开始.
  中文翻译:后台批处理路径 (后台批处理路径) 接受缩容到零,5-10分钟冷启动可容忍──
- 优质级别:`min_workers`租户每位有专用容量.
  中文翻译:高级层级:按租户 `min_workers`专用容量

### 在优化之前测量

> **【中文解读】**70B 模型冷启动解剖(示意数据):节点供应50s + 镜像拉取180s + 权重到HBM 75s + 引擎初始化20s + 首次前向3s = 总计 328s。全缓解后:预播种消除镜像拉取、模型流式加载减半权重加载、GPU 快照消除重复初始化 = 约15s 总冷启动(22x 降低)。

对于70B模型在新节点上进行冷启动解剖学 (说明):

| Phase | Time | Mitigation |
|-------|------|-----------|
| Node provision | 50s | Bottlerocket + pre-seeded image, warm pool |
| Image pull | 180s | Pre-seeded data volume (eliminate) |
| Weights to HBM | 75s | Model streamer (halve); GPU snapshot (eliminate) |
| Engine init | 20s | Persistent CUDA graph cache |
| First forward | 3s | Min inherent latency |
| **Total cold** | **328s** | |
| **Total with mitigations** | **~15s** | 22x reduction |

### 你应该记住的数字

- 模特冷启动: 2-4秒 (使用GPU快照).
  中文翻译:Modal冷启动:2-4 秒(使用GPU快照) 』
- 基本默认冷启动:5-10秒;以预加热的次下.
  中文翻译:Baseten默认冷启动:5-10秒;预加热后亚秒级。
-  70B冷开始:3-8分钟.
  中文翻译:原始 70B 冷启动:3-8 分钟.
- 运行:ai 流量模型:重量加载速度2倍.
  中文翻译:Run:ai 模式流:约 2倍权重加载加速──
- 服务器无LLM级载荷:延迟减少10-200倍 (纸号).
  中文翻译:ServerlessLLM 分层加载:10-200倍延迟降低(论文数据) 』

## 用它实现框架
```figure
cold-start-pipeline
```

## 用它

`code/main.py`报告冷开始时间,热池成本和热池自偿的破产要求率.

> `code/main.py`建模有/无每种缓解的冷启动路径――报告总冷启动时间、热池成本和热池自给自付的亏平衡请求率――

## 运送它.

这一课产生了`outputs/skill-cold-start-planner.md`鉴于SLA,模型大小和交通形状,选择哪些减轻措施.

> 本课产出发 `outputs/skill-cold-start-planner.md`△给定SLA、模型大小和流量形状,选择哪些缓解策略.

## 练习题

1. 跑步`code/main.py`计算比较低的热复制比通过SLO额外的请求降低付冷开始税的破产要求率.
   中文翻译:运行 `code/main.py`△计算热副本比通过SLO下额外请求放弃付冷启动税更便宜的亏平衡请求率──
2. 您将部署一个13B模型, P99 TTFT SLA3s. 选择最小减轻堆 (最小层) 实现这一目标.
   中文翻译:你部署一个13B模型,P99 TTFT SLA 为3秒.
3. 提前播放瓶子将消除图像拉力,但重量仍然从快照到HBM. 如果快照支持的NVMe以7GB/s读取,则计算70B模型的墙钟.
   中文翻译:Bottlerocket 预播种消除镜像拉取,但权重仍然需要从快照加载到HBM――计算快照支持的NVMe 以7GB/s 读取时70B 模型的实际耗时――
4. 双方都认为 什么是现实风险,以及减轻 (即时快照,加密,名区隔离)?
   中文翻译:你的无服务器提供GPU快照(Modal),但团队拒绝因为"快照泄露PII"――辩论双方实际风险是什么,缓解方案是什么(临时快照、加密、命名空间隔离)?
5. 设计一个层次的热池政策:为付费用户,试用用户和批量工作负载提供多少热复制?
   中文翻译:设计分层热池策略:付费用户、试用用户和批量处理工作负载各多少热副本?展示计算。

## 关键词 快速查找表

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

## 继续阅读 继续阅读

- [Modal — Cold start performance](https://modal.com/docs/guide/cold-start)莫达尔发布的基准和检查点架构.
- [AWS Bottlerocket](https://github.com/bottlerocket-os/bottlerocket)预先播种数据量快照模式.
- [NVIDIA Run:ai Model Streamer](https://github.com/run-ai/runai-model-streamer)重量重量重量重量重量重量重量重量重量重量重量重量重量重量重量重量重量重量重量重量重量重量重量重量重量重量重量重量重量重量重量重量重量重量重量重量重量重量重量重量重量重量重量重量重量重量重量重量重量重量重量重量重量重量重量重量重量重量重量重量重量重量重量重量重量重量重量重量重量重量重量重量重量重量重量重量重量重量重量重量重量重量重量重量重量重量重量重量重量重量重量重量重量重量重量重量重量重量重量重量重量重量重量重量重量重量重量重量重量重量重量重量重量重量重量重量重量重量重量重量重量重量重量重量重量重量重量重量重量重量重量重量重量重量重量重量重量重量重量重量重量重量重量重量重量重量重量重量重量重量重量重量重量重量重量重量重量重量重量重量重量重量重量重量重量重量重量重量重量重量重量重量重量重量重量重量重量重量重量重量重量重量重量重量重量重量重量重量重量重量重量重量重量重量重量重量重量重量重量重量重量重量重量重量重量重量重量重量重量重量重量重量重量重量重量重量重量重量重量重量重量重量重量重量重量重量重量重量重量重量重量重量重量重量重量重量重量重量重量重量重量重量重量重量重量重量重量重量重量重量重量重量重量重量
- [Baseten — Cold-start mitigation](https://www.baseten.co/blog/cold-start-mitigation/)预热的游戏手册.
- [ServerlessLLM paper (USENIX OSDI'24)](https://www.usenix.org/conference/osdi24/presentation/fu) 层次装载设计.
- [NVIDIA — Disaggregated LLM Inference on Kubernetes](https://developer.nvidia.com/blog/deploying-disaggregated-llm-inference-workloads-on-kubernetes/) 活迁移,用于分类部署.
