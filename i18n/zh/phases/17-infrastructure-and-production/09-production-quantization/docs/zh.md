# 产量量化  AWQ,GPTQ,GGUF K-量子,FP8,MXFP4/NVFP4

> 量子化格式不是一个普遍的选择. 它是硬件,服务引擎和工作负载的函数. GGUF Q4_K_M或Q5_K_M拥有CPU和边缘,通过 llama.cpp和Ollama提供. 在VLLM中,GPTQ在同一基地需要多个LoRA时获胜. 通过使用 Marlin-AWQ 核,在 7B 类型模型上提供了741 个_tk/s,最好的 Pass@1 在 INT4  作为2026 年的数据中心生产的默认. ,阿达和布莱克威尔的中期保持几乎没有损失,得到广泛支持. NVFP4和MXFP4 (黑微量化) 是积极的,需要每块验证. 两个陷咬人团队:校准数据集必须与部署域匹配,KV缓存与重量量化分开 AWQ课 "我的模型现在是4GB"在生产批量时忘记了10-30GBKV缓存.

> **【中文解读】**本节介绍了生产环境量化部署INT8/INT4/FP8量化技术在降低推算成本中的应用.
**Type:** Learn
**Languages:** Python (stdlib, toy memory and throughput comparison across formats)
**Prerequisites:** Phase 10 · 13 (Quantization foundations), Phase 17 · 04 (Serving Engine Internals)
**Time:** ~75 minutes


**Type:** Learn | **类型:** 学习
**Languages:** Python (stdlib, toy memory and throughput comparison across formats) | **语言:** Python
**Prerequisites:** Phase 10 · 13 (Quantization foundations), Phase 17 · 04 (vLLM Serving Internals) | **前置知识:** Phase 10 · 13 (Quantization foundations), Phase 17 · 04 (vLLM Serving Internals)

>  **【前置】**学本节前请先掌握:阶段10·13(量化基础) 阶段17·04(vLLM) ◎量化格式不是普适选择按硬件+引擎+工作负载选
>  **【类比】**量化格式 = "压缩行李"。GGUF Q4_K_M = 适合火车/边缘(CPU 友好);GPTQ = vLLM 多 LoRA 场景;AWQ + Marlin 内核 = 数据中心默认(7B 模型 741 tok/s,INT4 最佳);FP8 = Hopper/Ada/Blackwell 中选择(近乎无损);NVFP4/MXFP4 = 激进,需要块逐验证。
> ️ **【易错点】**两个陷:(1) 校准数据集必须匹配部署领域(医疗模型用通用文本校准会失真);(2) "我的模型只有4GB"
**Time:** ~75 minutes | **时间:** ~75 minutes

## 学习目标

- 举个6个生产量化格式和2026年的甜点.
  中文翻译:说出2026年六种生产级量化格式及其最佳使用场景──
- 选择给定的硬件格式 (CPU vs GPU,Hopper vs Blackwell),引擎 (vLLM,TRT-LLM, llama.cpp),和工作负载 (例行聊天,推理,多LoRA).
  中文翻译:根据硬件(CPU VS GPU、Hopper VS Blackwell) ٬引擎(vLLM、TRT-LLM、llama.cpp) 和工作负载(通用聊天、推理、多 LoRA) 选择格式──
- 计算保存的重量内存,并为所选格式留下未触及的KV缓存.
  中文翻译:计算选定格式节省的权重内存和未触及的KV 缓存──
- 命名对域流量量进行量化模型的校准数据集陷.
  中文翻译:说出导致量化模型在领域流量上退化的校准数据集陷.

## 问题 问题引入

> **【中文解读】**量化减少内存和HBM带宽消耗正是最需要的解码阶段.FP16的70B模型重量占140GB,INT4量化后仅35GB,可在一张H100上运行.但量化不是免费的.

> **【拓展：量化技术演进】**量化技术经历了三代: ((1) 均量化(INT8/INT4) 简单但精度损失大;(2) 感知量化(AWQ/GPTQ) 保护重权重量,INT4 下质量接近BF16;(3) 浮点量化(FP8/NVFP4) 硬件加速,动态范围更好.

量子化减少了内存和HBM带宽,这正是解码所需的.FP16 70B模型的重量为140GB.量化重量为INT4 (AWQ或GPTQ),模型为35GB 适合一个H100,可容纳KV缓存,这很重要,因为在2k文本的128个同时序列中,KV缓存仅为20-30GB.

> 量化减少内存和HBM带宽消耗,正是解码阶段最需要的.FP16的70B模型权重占140GB.后的模型将重量化为INT4(AWQ或GPTQ) 仅35GB可以在一张H100上运行,还有空间放 KV缓存,这在128并发序列、2K上下文时很重要,因为KV缓存单独需要20-30GB.

量子化不是免费的. 侵略性量子化降低了质量,特别是在推理重任务上. 不同的格式与不同的引擎工作. 不同的硬件支持不同的精度. 2026 格式动物园是真实的,你不能复制别人的选择.

> 但是量化不是免费的. 激进量化降低质量,特别是推理密集型任务. 不同的形式配合不同的引擎. 不同的硬件原生支持不同精度.

## 概念的核心概念

### 六种格式

| Format | Bits | Sweet spot | Engines |
|--------|------|-----------|---------|
| GGUF Q4_K_M / Q5_K_M | 4-5 | CPU, edge, laptops | llama.cpp, Ollama |
| GPTQ | 4-8 | Multi-LoRA on vLLM | vLLM, TGI |
| AWQ | 4 | Datacenter GPU production | vLLM (Marlin-AWQ), TGI |
| FP8 | 8 | Hopper/Ada/Blackwell datacenter | vLLM, TRT-LLM, SGLang |
| MXFP4 | 4 | Blackwell multi-user | TRT-LLM |
| NVFP4 | 4 | Blackwell multi-user | TRT-LLM |

### 关键键字:

> **【拓展：GGUF 在边缘推理中的地位】**在 GPU 上使用vLLM 时,GGUF 性能差距大约~93 tok/s,因为它不是为 GPU 内核优化而设.

GGUF是一个文件格式,而不是一个量子化方案.它将K-量子变体 (Q2_K,Q3_K_M,Q4_K_M,Q5_K_M,Q6_K,Q8_0) 捆绑在一个容器中.Q4_K_M和Q5_K_M是生产默认的4BF16质量在4-5位.最好的选择是CPU或边缘服务,因为 llama.cpp是迄今为止最快的CPU推断引擎.

> GGUF是一种文件格式,本身不是量化方案. 它将K-量子变体包装在一个容器中. Q4_K_M 和 Q5_K_M 是默认的生产4-5位. 下接近BF16质量.

在vLLM中吞吐量处罚:在7B上~93tok/s 格式不适用于GPU内核.使用GGUF当部署目标是CPU/edge时.否则.

> 模型约93个/s该格式未针对GPU内核优化──仅在部署目标是CPU/边缘使用GGUF,否则不使用──

### 多洛拉在vLLM中

GPTQ是一个后训练量化算法,具有校准度过.马林内核在GPU上实现速度2.6倍,而非马林GPTQ. ~712tc/s在7B上.

> 马林内核使其在 GPU 上快速(比非马林 GPTQ 快 2.6 倍) ・7B 模型约 712 个/秒。

唯一的胜利:GPTQ-Int4支持vLLM中的LoRA适配器.如果你正在使用基模型加上10-50个细调变量 (每个变量都是LoRA),GPTQ是你的路径.NVFP4尚未支持LoRA2026年初.

> 独特优势:GPTQ-Int4 在vLLM中支持LoRA 适配器──如果你在服务中一个基础模型加上10-50个微调变体──每个作为LoRA,GPTQ是你的路径──截至2026年初NVFP4尚不支持LoRA──

### AWQ 数据中心 GPU 默认

> **【中文解读】**AWQ(激活意识重量定量化) 是2026年数据中心GPU推理的默认选择――它保护量化过程中约占最显著的重量,配合Marlin-AWQ内核实现10.9倍加快――在7B模型上达到~741个/秒,是INT4格式中最高的――除非需要多个LORA(选择GPTQ) 或Blackwell FP4(选择 NVFP4),否则应对新GPU推理项目默认使用 AWQ――

激活意识重量量化. 在量化过程中保护了最突出的重量1%.马林-AWQ核: 10.9x速度与天真. 7B 上的741个通/秒,是 INT4 格式中最好的 Pass@1.

> 激活感知权重量化――保护量化过程中约1% 最显著的权重――马林-AWQ 内核:比朴素方法快 10.9倍――7B 模型约 741 个/秒,INT4 格式中 Pass@1 最高――

选择AWQ为新的GPU服务,除非你需要多LoRA (GPTQ) 或积极的Blackwell FP4 (NVFP4).

> 新GPU 推理项目选择AWQ,除非需要多个LORA(选择GPTQ) 或激进的黑尔FP4(选择NVFP4)。

### 可靠的中部

> **【拓展：FP8 量化的生产应用】**质量风险远低在推理,医疗,代码生成等场景中几乎没有损失. LM、TRT-LLM、SGLang都支持FP8──典型配置:70B FP8 模型重量约70GB + KV Cache,可在一张H100 80GB运行 128 并发.

八位浮点.几乎没有损失.广泛支持. 霍珀电压芯以原生方式加速FP8. 黑继承.FP8是安全的2026默认,当质量不可谈判时 (理性,医学,代码代码). 存储量是INT4的一半,但质量风险要低得多.

> 八位浮点──近乎无损──广泛支持──Hopper Tensor Cores 原生加速FP8──布莱克威尔 继承──当质量不可妥协时(推理、医疗、代码生成),FP8是2026年安全默认选择──内存节省是INT4的一半,但质量风险远低──

### 黑攻击性

微量化FP4.每个重量块都有自己的尺度因子.黑尔子芯上具有侵略性但硬件加速性.每代币的字节减半,而FP8 在17期的经济胜利.

> 微缩放FP4──每块权重都有自己的缩放因子──激进但黑电芯硬件加速──相比FP8 每字节减半 17期 · 07 中的经济优势──

洞穴:
- 目前没有LoRA支持 (2026年初).
  中文翻译:截至2026年初尚不支持洛拉──
- 在沉重的工作负载上,质量下降明显.
  中文翻译:推理密集型工作负载上可见质量下降──
- 根据模型的评估设置验证.
  中文翻译:每个模型在评估集上验证.

### 校准陷

> **【中文解读】**校准数据集陷:AWQ 和 GPTQ 需要校准数据集来决定保护哪些权力――通用C4/WikiText 数据集在领域模型 ((代码、医疗、法律) 上会导致错误决策HumanEval Pass@1可能下降几百分点――修复方法是用于领域内数据校准,通常几百个样本就足够了,发货前在评估集中验证――

> **【拓展：量化对 LLM 能力的影响】**量化对不同能力的影响程度不同:(1) 简单聊天/摘要INT4 几乎没有影响;(2) 翻译/写作INT4 轻微退化;(3) 数学/推理INT4 损失 3-5 分(MATH基准);(4) 长上下文理解INT4 在 128K+ 背景上质量显著下降;(5) 代码生成INT4 在 HumanEval 上下降 2-3 分──核心原则:推理密集型任务应使用 FP8 或 BF16,通用聊天可使用 INT4──

AWQ和GPTQ需要一个校准数据集,通常是C4或WikiText.对于域名模型 (代码,医学,法律),在通用网页文本上校准使算法做出错误的决定,关于保护的权重.

> 对于领域模型 (代码,医疗,法律),在通用网络文本上校准会让算法误决策保护哪些权重.

解决方案:在域内数据进行校准.通常需要数百个域名样本. 在运输之前,在评估组上测试.

> 修复方法: 用领域内数据校准.几百个领域的样本通常足够.

### 卡车预存陷

> **【中文解读】**卡维存储器陷:AWQ将权重压缩到4位,但卡维存储器是独立的,保持在FP16/FP8。70B卡维存储量预算是:权重35GB+卡维存储器(128 并发 ×2K文本) 20GB+ 激活5GB = 总量60GB。朴素地认为"我的模型量化将达到4GB 了"忘记另外30-50GB──必须整体预算HBM。

AWQ将重量缩小到4位.KV缓存是独立的,保持在FP16/FP8.对于AWQ的70B模型:

- 权重: ~ 35 GB (INT4从 140 GB).
  中文翻译:权重:约35GB(从140GB的INT4)。
- 在 128 个同时 × 2k 语境中的 KV缓存: ~ 20 GB.
  中文翻译:128 并发 × 2K 上下文的 KV 缓存:约20GB──
- 激活: ~ 5 GB.
  中文翻译:激活:约5GB──
- 总量:60GB 适合H10080GB.
  中文翻译:总计:约60GB适合H10080GB.

简单地说",我把我的模型量化为4GB",忘记了其他30-50GB.

> 简单地认为"我的模型量化为4GB了"忘记了另外30-50GB.

单独,KV缓存量化 (FP8 KV或INT8 KV) 是一个不同的选择,它有自己的权衡.

> 另外,KV 缓存量化 (FP8 KV 或 INT8 KV) 是一个有不同的权重的独立选择,它直接影响注意力精度,而不是免费收益.

###  AWQ INT4 对于推理是危险的

思想链,数学,长文本的代码代码这些显然受到攻击性量化的影响.AWQ INT4在 MATH 上损失3-5分.对于推理重的工作负载,请运送FP8或BF16;接受存储成本.

> 对于推理密集型工作负载,使用FP8或BF16;接受内存成本――

### 2026 选用指南

- 处理器/边缘服务:GGUF Q4_K_M.完成.
  中文翻译:CPU/边缘服务:GGUF Q4_K_M。
-  GPU服务,常规聊天,没有LORA: AWQ.
  中文翻译:GPU 服务,通用聊天,无 LoRA:AWQ。
- 接下来,我们将把它带到一个地方.
  中文翻译:GPU 服务,多 LoRA:GPTQ + Marlin。
- 推理工作量:FP8.
  中文翻译:推理工作负载:FP8。
- 黑数据中心,验证质量:NVFP4+FP8KV.
  中文翻译:布莱克威尔 数据中心,已验证质量:NVFP4 + FP8 KV。
- 模糊:对每个候选人格式进行1000个样本的评估.
  中文翻译:不确定:在每个候选人格式上运行1000个样本评估.

## 用它实现框架
```figure
gpu-memory-breakdown
```

## 用它

`code/main.py`计算内存足迹 (权重+KV+激活) 和相对吞吐量在六种格式中,用于一系列模型尺寸.显示KV缓存在哪里占主导地位,重量压缩在哪里,以及FP8是安全选择的地方.

> `code/main.py`计算一系列模型大小在六种格式下内存占用(权重+KV+ 激活) 和相对吞吐量――展示KV 缓存在哪里占主导、权重压缩在哪里划算、FP8在哪里是安全选择――

## 运送它.

> **【拓展：量化选型决策树】**2026年量化格式选择决策树:(1) CPU/边缘部署 → GGUF Q4_K_M;(2) GPU通用聊天、无 LoRA → AWQ;(3) GPU 多 LoRA → GPTQ + Marlin;(4) 推理密集型任务 → FP8;(5) Blackwell 数据中心、已验证质量 → NVFP4 + FP8 KV;(6) 不确定 → 在候选格式运行1000个样本评估――量化后的验证步骤不可避免 每个模型 × 量化格式 × 硬件组合都需要独立验.

这一课产生了`outputs/skill-quantization-picker.md`鉴于硬件,模型尺寸,工作负载类型和质量耐受性,选择格式并制定校准/验证计划.

> 本课产出发 `outputs/skill-quantization-picker.md`△给定硬件、模型大小、工作负载类型和质量耐受性,选择格式并生成校准/验证方案──

## 练习题

1. 跑步`code/main.py`对于一个70B模型的128同时和2k文本,计算每个格式的总HBM. 哪个格式允许你适合一个H100 80GB?
   中文翻译:运行 `code/main.py`△对于 128 个并发 2K 上下文的 70B 模型,计算每种格式的总 HBM △ 哪种格式可以放置一个 H100 80GB 上?
2. 如果你对质量宽容有错,恢复的路径是什么?
   中文翻译:你有一个7B编码模型――选择一个格式并说明理由――如果你对质量耐受性做出判断错误,恢复路径是什么?
3. 为什么更多数据并不总是更好?
   中文翻译:计算医疗领域模型 AWQ 校准所需的数据集大小――为什么更多数据不总是更好?
4. 在7B上,AWQ为什么达到741个单/秒,而原始GPTQ为712个单.
   中文翻译:阅读马林-AWQ 内核论文或发布说明.
5. 什么时候可以将 AWQ 重量与FP8 KV缓存相比,保持KV在BF16?
   中文翻译:何时将 AWQ权重与 FP8 KV 缓存组合有意义,何时保持 BF16 KV?

## 关键词 快速查找表

| Term | What people say | What it actually means |
|------|----------------|------------------------|
| GGUF | "llama.cpp format" | File format bundling K-quant variants; CPU/edge default |
| Q4_K_M | "Q4 K M" | 4-bit K-quant medium; the production GGUF default |
| GPTQ | "gee pee tee q" | Post-train INT4 with calibration; supports LoRA in vLLM |
| AWQ | "a w q" | Activation-aware INT4; Marlin kernels; best Pass@1 at INT4 |
| Marlin kernels | "fast INT4 kernels" | Custom CUDA kernels for INT4 on Hopper; 10x speedup |
| FP8 | "eight-bit float" | Safe precision default on Hopper/Ada/Blackwell |
| MXFP4 / NVFP4 | "microscaling four" | Blackwell 4-bit FP with per-block scale factors |
| Calibration dataset | "cal data" | Input text used to pick quantization parameters; must match domain |
| KV cache quantization | "KV INT8" | Separate choice from weights; affects attention accuracy |

## 继续阅读 继续阅读

- [VRLA Tech — LLM Quantization 2026](https://vrlatech.com/llm-quantization-explained-int4-int8-fp8-awq-and-gptq-in-2026/)比较基准.
- [Jarvis Labs — vLLM Quantization Complete Guide](https://jarvislabs.ai/blog/vllm-quantization-complete-guide-benchmarks)按格式的吞吐量数.
- [PremAI — GGUF vs AWQ vs GPTQ vs bitsandbytes 2026](https://blog.premai.io/llm-quantization-guide-gguf-vs-awq-vs-gptq-vs-bitsandbytes-compared-2026/)按格式选择.
- [vLLM docs — Quantization](https://docs.vllm.ai/en/latest/features/quantization/index.html)支持的格式和旗.
- [AWQ paper (arXiv:2306.00978)](https://arxiv.org/abs/2306.00978) AWQ原始表达式.
- [GPTQ paper (arXiv:2210.17323)](https://arxiv.org/abs/2210.17323)原始GPTQ制剂.
