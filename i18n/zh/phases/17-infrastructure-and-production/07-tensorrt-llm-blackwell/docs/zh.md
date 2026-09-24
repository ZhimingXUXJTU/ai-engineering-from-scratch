# 黑的缩RT-LLM与FP8和NVFP4
# 硬件专业化输入组合 FP8和NVFP4在Blackwell上

> 专业化硬件推理编译交易可移植性,而TensorRT-LLM  仅为NVIDIA调整,为黑 是交易的最清楚的例子.在GB200 NVL72上,SemiAnalysis InferenceX测量了$0.012 per million tokens on a 120B model in Q1-Q2 2026, against $率为0.09/M,H100+vLLM7倍的经济差距. 堆是三个浮点模式的组合:FP8对于KV缓存和注意内核保持至关重要,因为它具有所需的动态范围;NVFP4 (4位微量化) 处理权重和激活;多代币预测 (MTP) 和分类预填/解码增加了另外2-3x. 支持日-0模型直接加载FP4重量,而不会进行训练后转换. 2026年工程团队的目标:TRT-LLM是开源,但NVIDIA专用, CUDA和Blackwell专业,因此通过它交易了可移植性. 在做出承诺之前,你用模型和硬件进行计算.

> **【中文解读】**本节介绍了TensorRT-LLM和BlackwellNVIDIA的LLM 推理优化框架和最新的GPU架构.
**Type:** Learn
**Languages:** Python (stdlib, toy FP8/NVFP4 memory and cost calculator)
**Prerequisites:** Phase 17 · 04 (Serving Engine Internals), Phase 10 · 13 (Quantization)
**Time:** ~75 minutes


**Type:** Learn | **类型:** 学习
**Languages:** Python (stdlib, toy FP8/NVFP4 memory and cost calculator) | **语言:** Python（标准库，FP8/NVFP4 内存和成本计算器）
**Prerequisites:** Phase 17 · 04 (vLLM Serving Internals), Phase 10 · 13 (Quantization) | **前置知识:** Phase 17 · 04（vLLM 服务内部）, Phase 10 · 13（量化）

>  **【前置】**学本节前请先掌握:阶段17·04(vLLM) 、阶段10·13(量化基础) ――TensorRT-LLM 是NVIDIA 专属优化,在Blackwell GPU上性能最强──
>  **【类比】**电压RT-LLM = "NVIDIA 专属跑车"──GB200 NVL72 上半分析 测:120B 模型 $0.012/百万 token（H100+vLLM $0.09)  7倍经济性差距──三套浮点叠加:FP8(KV缓存+注意力 动态范围) + NVFP4(4-位权重激活) + MTP/解预填-解码 再加 2-3 倍──代价:闭源NVIDIA ,可移植性换吞吐──选型前必须按你的模型/硬件组合账户──
**Time:** ~75 minutes | **时间:** ~75 分钟

## 学习目标

- 解释为什么FP8在NVFP4中重量时仍然对KV缓存和注意力至关重要.
  中文翻译:解释为什么即使权重在NVFP4中,FP8对KV 缓存和注意力仍然关键.
- 在BF16,FP8和NVFP4中计算边界模型的HBM足迹,并解释节省的来源.
  中文翻译:计算前沿模型在BF16、FP8和NVFP4下的HBM占用,分析节省来自哪里──
- 命名黑特征TRT-LLM利用 (日-0 FP4,MTP,分类分类,全至全原始).
  中文翻译:说出TRT-LLM利用的黑特有功能(日-0 FP4、MTP、分离式服务、所有原语) 』
- 决定什么时候TRT-LLM的NVIDIA锁值7倍的成本差距与Hopper的vLLM.
  中文翻译:决定 TRT-LLM 的 NVIDIA 锁定何时值相比 Hopper 上 vLLM 的 7x 成本差距──

## 问题 问题引入

> **【中文解读】**2026年推理经济学的前沿问题是"每美元多少代币"――答案取决于四层叠加选择:硬件代际:Hopper H100/H200 vs Blackwell B200/GB200) 精度(BF16 → FP8 → NVFP4) 、推理引擎(vLLM vs SGLang vs TRT-LLM) 和编排(朴素 vs 分离式 vs 动力) ─在Hopper + vLLM 上运行 120B MoE 约$0.09/M tokens；在 Blackwell + TRT-LLM + Dynamo 上仅 $差距 0.012/M7x 差距的价格是NVIDIA 锁定你不能在其他厂商的硬件上复现

> **【拓展：NVIDIA Blackwell 架构】**黑 (B200/GB200) 是NVIDIA 2024-2025年推出的GPU架构,相比于Hopper (H100) 在LLM推理上每一个GPU吞吐升级的11-15倍.关键特性包括:NVFP4精度,4位微缩浮点,硬件加速)  NVLink 5号 (MoE专家通信延迟降低3倍) 第二代变压器引擎以及GB200 NVL72的72GPU一致内存域.MLPerf 推理 v6.0号 (04月) 显示黑在所有提交任务中全面领先.

2026年推断经济学的边界是"每美元多少代币".答案取决于四个堆叠选择:硬件生成 (Hopper H100/H200 vs Blackwell B200/GB200),精度 (BF16 → FP8 → NVFP4),服务引擎 (vLLM vs SGLang vs TRT-LLM),和配乐 (平面 vs 分类对阵 Dynamo).

> 2026年推理经济学前沿是"每美元多少代币"──答案取决于四个叠加选择:硬件代际(霍珀vs布莱克威尔) 精度(BF16 → FP8 → NVFP4) 推理引擎(vLLM vs SGLang vs TRT-LLM) 和编排(朴素 vs 分离式 vs 动态)──

在Hopper上,一个120B的MoE在 ~$0.09 per million tokens. On Blackwell with TRT-LLM + Dynamo, the same model runs at ~$部分缺口是硬件 (Blackwell为每GPU LLM输出量11-15x对Hopper).部分是堆:FP4重量,MTP草案,分类的预填/解码,以及MoE专家通信的NVLink5.

> 在 Hopper + vLLM 上,120B MoE 运行约$0.09/M tokens。在 Blackwell + TRT-LLM + Dynamo 上，同一模型运行约 $部分差距来自硬件(Blackwell vs Hopper 每 GPU LLM 吞吐 11-15 倍) 部分来自:FP4 权重、MTP草案、分离式预填充/解码和NVLink 5 全面用于MoE 专家通信。

对于经济学来说,这是交易的可移植性.理解哪些选择给出哪些缺口的份额是这门课程的重点.

> 你不能在NVIDIA 之外复现. 这就是衡量可移植性转换性.

## 概念的核心概念

### 为什么FP8仍然是KV缓存的地板

> **【中文解读】**简单的KV缓存的重量密度要求是:KV缓存的重量密度要求跨越了很宽的动态范围将KV量化到FP4导致灾难性精度损失. NVFP4仅适用于重量和激活缩缩让每个权重块具有独立的缩缩因子.典型的黑配置是:权重NVFP4(4-位微缩缩) 激活NVFP4、KV缓存FP8、注意力加加器FP32──

2026年常见的错误:假设NVFP4适用于各处.它不适用于.KV缓存需要FP8 (8位浮点) 因为它存储了跨越广泛动态范围的注意力键和值.将KV量化为FP4导致灾难性的精度损失.

> 2026年的一个常见错误:假设NVFP4适用于所有地方──不是的──KV 缓存需要FP8(8位浮点),因为它储存跨越很宽动态范围的注意力键值──将KV 量化到FP4会导致灾难性精度损失分布尾部衰退,注意力分数崩──FP8的指数给KV 缓存需要的范围──

NVFP4 (2025-2026) 适用于重量和激活.微量化:每个重量块都有自己的尺度因子,因此小块可以跨越不同的动态范围,而不会损失每ensor尺度.对于激活,FP4 保持,因为激活在层内是小范围的.

> NVFP4 (2025-2026) 适用于重量和激活.微缩放:每个重量块都有自己的缩放因子,小块可以跨越不同动态范围,而不损失每张量缩放.

典型的黑尔配置:

- 权重:NVFP4 (4位微量化).
  中文翻译:权重:NVFP4(4-bit 微缩放) 』
- 激活:NVFP4.
  中文翻译:激活:NVFP4──
- 预测量:FP8.
  中文翻译:KV 缓存:FP8。
- 注意积累器:FP32 (软max稳定).
  中文翻译:注意力累加器:FP32(软max 稳定性) 』

### 黑特异性原始物使用TRT-LLM

- **Day-0 FP4 weights**车型供应商直接运送FP4重量;TRT-LLM负载没有训练后转换.
  翻译: 中文**Day-0 FP4 权重**模型提供商直接发布FP4 权重;TRT-LLM 无需训练后转换即可加载;;FP4 不需要 AWQ/GPTQ 步骤;;
- **Multi-token prediction (MTP)**果:与EAGLE (阶段17 · 05) 的想法相同,但与TRT-LLM构建相结合.
  翻译: 中文**多 token 预测 (MTP)**子与子相似的想法 (第17阶段)
- **Disaggregated serving**通过 NVLink或InfiniBand传输KV缓存.与Dynamo (阶段17 · 20) 的相同想法.
  翻译: 中文**分离式服务**预填充和编码在独立的GPU池上,KV 缓存通过NVLink或InfiniBand传输.
- **All-to-all communication primitives** NVLink 5 降低了MoE专家通信延迟3x对Hopper.
  翻译: 中文**All-to-all 通信原语**网络通信延迟将降低3倍.
- **NVFP4 + MXFP8 microscaling**硬件加速处理黑电芯的尺度因素.
  翻译: 中文**NVFP4 + MXFP8 微缩放**黑电压芯上硬件加速缩缩处理因子

### 你应该记住的数字

- 通过TRT-LLM,GPT-OSS-120B的HGX B200代币价为0.02/M美元.
  中文翻译:HGX B200 在 GPT-OSS-120B 上通过TRT-LLM为0.02/M代币
- 通过Dynamo (配套TRT-LLM) 通过0.012/M美元的GB200 NVL72代币.
  中文翻译:GB200 NVL72 通过Dynamo (TRT-LLM) 为0.012/M美元的代币.
- 对于可比较的工作负载,H100+vLLM ≈ $0.099/M代币.
  中文翻译:H100 + vLLM 在可比工作负载上约0.09美元/M代币.
- 在TRT-LLM更新 (2026) 的三个月内,产量增长2.8倍.
  中文翻译:TRT-LLM 2026 年三月更新的 2.8 倍吞吐量提升──
- 博公司的每次博总额是11-15倍,
  中文翻译:黑 vs 霍珀 每 GPU LLM 吞吐量 11-15 倍──
- 黑主导于每一个提交的任务.
  中文翻译:MLPerf 推理 v6.0(2026 年 4 月):布莱克威尔 在所有提交任务中领先.

### 实际QP4质量成本

> **【中文解读】**在推理密集型工作负载 (思维链、数学、长上下文代码生成) 上会导致可见的质量退化. 每块校准可以缓解但不能消除.2026年的实践指南是:推理模型使用FP8 权重 +FP4 激活作为折扣,或继续使用H200 全FP8――规则是:在提交 NVFP4 权重之前,必须在自己的评估集中验证任务质量.

> **【拓展：量化精度 vs 推理成本权衡】**量化精度的选择是质量和成本的权衡:(1) BF16无质量损失,但内存需求大了(70B 模型需要140GB);(2) FP8几乎没有损失,Hopper/Blackwell 硬件加速,推用于推测密集型任务;(3) INT4(AWQ/GPTQ) 4-bit 权重,MATH 分数下降 3-5 点,适合通用聊天;(4) NVFP4最激进,Blackwell 专业,必须在目标评估上精确进行测试.

NVFP4是积极的.在推理重的工作负载 (思想链,数学,长文本的代码代码),FP4重量显著降低.每块校准减轻,但不消除.团队运输推理模型通常使用FP8重量 +FP4激活作为妥协,或坚持H200与FP8在整个.

> 在推理密集型工作负载 (思维链,数学,长上下文代码生成) 上,FP4 权重明显退化. 每块校准缓解但不能消除.

规则:在承诺 NVFP4 权重之前,总是验证您的评估设置中的任务质量.

> 规则:在提交 NVFP4 权重之前,始终在您的评估集中验证任务质量.

### 为什么这是NVIDIA锁定决定

> **【中文解读】**如果您的基础设施策略是多供应商,TRT-LLM 对于这个层面是不可选项您仍然可以在混合硬件上使用vLLM.

> **【拓展：NVIDIA vs AMD 推理生态】**2026年 AI 推理芯片市场格局:NVIDIA 借助CUDA 生态和TRT-LLM 占据约80%的数据中心推理份额.AMD MI300X在原始计算力上有竞争力,但软件(ROCm + vLLM) 仍在追赶.Intel Gaudi 3 是另一个选择,但采用率较低.

如果您的基础战略是多供应商,TRT-LLM是 TRT-LLM 服务的层次的非启动器.您仍然可以从vLLM上服务于混合硬件.如果您仅使用NVIDIA,则7x差距支付锁.

> 如果您的基础设施策略是多供应商,TRT-LLM不可行您仍然可以在混合硬件上使用VLLM. 如果您只使用NVIDIA,7x 差距值得锁定.

### 2026 实用食谱

对于每年100万美元以上的推断账单,运行Hopper + vLLM将在表上留下7-10倍.将成本主导的工作负载迁移到Blackwell + TRT-LLM + Dynamo.为模型代速度,保持H100 + vLLM的实验级别.在生产前验证每个NVFP4转换模型的质量.

> 对于100万美元以上的年度推算支出,在Hopper + vLLM上运行意味着留下7-10倍的节省空间.

### 分类奖励

在Blockwell上,乘数堆积:FP4重量 × MTP加速 × 分类配置 ×缓存知路线. 7x数量假设这个完整堆积.

> 在黑尔上,乘数叠加:FP4权重 × MTP 加速 × 分离式部署 × 缓存感知路由──7x 数字假设使用完整──

## 用它实现框架

> **【拓展：Blackwell 迁移决策】**从Hopper 迁移到Blackwell + TRT-LLM的决策框架:(1) 年推理支出是否超过5亿美元?是→值得评估迁移;(2) 是否可以接受NVIDIA 锁定?否→继续使用vLLM + Hopper;(3) 工作负载是否包含MoE 模型?是→Blackwell的NVLink 5全方位 提供额外的3倍加快;(4) 推理密集型任务占比是否超过30%?是→需要验证NVFP4 质量――迁移 ROI通常在6-12个月内回本.
```figure
pipeline-parallel
```

## 用它

`code/main.py`计算HBM足迹,解码吞吐量 (内存绑定模式) 和$/M代币为模型跨三个堆:H100 + BF16 + vLLM,H100 + FP8 + vLLM,B200 + NVFP4/FP8 + TRT-LLM.运行它以查看合并效果和每个变化所贡献的差距.

> `code/main.py`计算模型在三个上 HBM 占用、解码吞吐量(内存受限) 和 $/M代币:H100 + BF16 + vLLM、H100 + FP8 + vLLM、B200 + NVFP4/FP8 + TRT-LLM──运行它查看复合效应和每个变化贡献差距份额──

## 运送它.

这一课产生了`outputs/skill-trtllm-blackwell-advisor.md`鉴于工作量,模型规模和年次代币量,它决定了黑+TRT-LLM堆是否值得NVIDIA锁.

> 本课产出发 `outputs/skill-trtllm-blackwell-advisor.md`◎给定工作负载、模型大小和年度代币量,它决定了黑+TRT-LLM 是否值得NVIDIA锁定──

## 练习题

1. 跑步`code/main.py`在一个有30%活跃参数的120B MoE上,计算H100 BF16,H100 FP8和B200 NVFP4/FP8的内存带宽限制解码吞吐量.
   中文翻译:运行 `code/main.py`△在 30% 活跃参数的 120B MoE 上,计算 H100 BF16、H100 FP8 和 B200 NVFP4/FP8 的内存带宽限解码吞吐量──最大跳跃来自哪里?
2. 顾客每年花费2亿美元用于H100+vLLM. 考虑到经济差距7倍,他们需要购买多少黑GPU才能在12个月内抵偿 TRT-LLM迁移?
   中文翻译:客户在H100+vLLM上每年花费2M美元.给定7x 经济差距,他们需要购买多少布莱克威尔GPU才能在12个月内销售转移到TRT-LLM的成本?
3. 在 NVFP4 重量转换后,您会看到精度在 MATH 上下降3点. 举个恢复路径:一个质量第一 (保持FP8 重量),一个成本第一 (与域内数据校准).
   中文翻译:NVFP4 权重转换后 MATH 精度下降 3 点──说出两条恢复路径:一条质量优先(保持FP8 权重),一条成本优先(用领域内数据校准) ・・・
4. 读一读MLPerf v6.0推断结果. 哪个任务有最小的黑超 Hopper差距,为什么?
   中文翻译:阅读MLPerf v6.0 推理结果── Blackwell-over-Hopper的哪个任务差距最小,为什么?
5. 在NVFP4重量下计算405B模型所需的HBM + 128k背景下FP8KV缓存.它是否适合单个GB200NVL72节点?
   中文翻译:计算 405B 模型在 NVFP4 权重 + FP8 KV 缓存 + 128k 上下文下 HBM 需求――它是否适合单个 GB200 NVL72 节点?

## 关键词 快速查找表

| Term / 术语 | What people say / 通俗说法 | What it actually means / 实际含义 |
|------|----------------|------------------------|
| FP8 | "eight-bit float" / "8-bit 浮点" | 8-bit floating point; used for KV cache and attention due to dynamic range / 8-bit 浮点；因动态范围用于 KV 缓存和注意力 |
| NVFP4 | "four-bit micro" / "4-bit 微缩放" | NVIDIA's 4-bit microscaling FP format; weights and activations on Blackwell / NVIDIA 4-bit 微缩放浮点格式；Blackwell 上的权重和激活 |
| MXFP8 | "MX eight" / "MX 8-bit" | Microscaling FP8 variant; hardware-accelerated on Blackwell Tensor Cores / 微缩放 FP8 变体；Blackwell Tensor Core 硬件加速 |
| Day-0 FP4 | "ship FP4 weights" / "直接发布 FP4 权重" | Model providers release weights already in FP4; no post-train conversion step / 模型提供商直接发布 FP4 权重；无训练后转换步骤 |
| MTP | "multi-token prediction" / "多 token 预测" | TRT-LLM's integrated speculative-decoding draft (Phase 17 · 05) / TRT-LLM 集成的推测解码 draft |
| Disaggregated serving | "split prefill/decode" / "分离预填充/解码" | Prefill and decode on separate GPU pools; KV transferred over NVLink/IB / 独立 GPU 池的预填充和解码 |
| All-to-all | "MoE expert comm" / "MoE 专家通信" | Communication pattern routing tokens to expert GPUs; NVLink 5 cuts 3x / 将 token 路由到专家 GPU 的通信模式 |
| InferenceX | "SemiAnalysis inference bench" / "推理基准" | The 2026 industry-accepted cost-per-token benchmark / 2026 年行业接受的每 token 成本基准 |

## 继续阅读 继续阅读

- [NVIDIA — Blackwell Ultra MLPerf Inference v6.0](https://developer.nvidia.com/blog/nvidia-blackwell-ultra-sets-new-inference-records-in-mlperf-debut/) 2026年4月MLPerf结果.
- [NVIDIA — MoE Inference on Blackwell](https://developer.nvidia.com/blog/delivering-massive-performance-leaps-for-mixture-of-experts-inference-on-nvidia-blackwell/) NVLink 5 全面和MoE核.
- [TensorRT-LLM Overview](https://nvidia.github.io/TensorRT-LLM/overview.html)官方发动机文件.
- [NVIDIA — Introducing Dynamo](https://developer.nvidia.com/blog/introducing-nvidia-dynamo-a-low-latency-distributed-inference-framework-for-scaling-reasoning-ai-models/)在TRT-LLM以上的分类配乐.
- [MLPerf Inference](https://mlcommons.org/benchmarks/inference-datacenter/)发布黑数字的基准数据集.
