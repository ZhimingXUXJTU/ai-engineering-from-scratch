# 截止到终端的细调管道 (数据到SFT到DPO服务)

> 基于你自己的数据训练的8B模型,根据你自己的偏好进行了DPO排列,量化,投机式解码, 2026 开放堆是Axolotl v0.8,TRL 0.15,代的Unsloth,量化的GPTQ/AWQ/GGUF,配送的VLLM 0.7和EAGLE-3. 终点是将整个管道可复制的运行  YAML 进入,服务端点 ,并在2026年模型开放框架下发布模型卡.

> **【中文解读】**本节是综合项目,从数据准备到模型评估.


**Type:** Capstone | **类型:** 综合项目
**Languages:** Python (pipeline), YAML (configs), Bash (scripts) | **语言:** Python（管道）, YAML（配置）, Bash（脚本）
**Prerequisites:** Phase 2 (ML), Phase 3 (DL), Phase 7 (transformers), Phase 10 (LLMs from scratch), Phase 11 (LLM engineering), Phase 17 (infrastructure), Phase 18 (safety)

>  **【前置】**顶点项目 07 = 综合几乎全部阶段──端到端微调流水线:数据→SFT→DPO→服务──
>  **【类比】**微调流水线 = "AI 训练厨房"──2026 开源:Axolotl v0.8(配置) + TRL 0.15(训练) + 代加速) + GPTQ/AWQ/GGUF(量化) + vLLM 0.7+EAGLE-3(服务)──目标:8B 模型在自有数据上 SFT+DPO+量化+投机解码+可测 $/1M代币,YAML 输入→服务端输出,附2026 模型开放框架 模型卡──**前置知识:**工程,基础设施,安全,安全,安全,安全,安全,安全,安全,安全,安全,安全,安全,安全,安全,安全,安全,安全,安全,安全,安全,安全,安全等等
**Phases exercised:**现在,我们在这个世界里,**涉及阶段:**子,子,子,子,子,子,子,子,子,子,子,子,子,子,子,子,子,子,子,子,子,子,子,子,子,子,子,子,子,子,子,子,子,子,子,子,子,子,子,子,子,子,子,子,子,子,子,子,子,子,子,子,子,子,子,子,子,子,子,子,子,子,子,子,子,子,子,子,子,子,子,子,子,子,子,子,子,子,子,子,子,子,子,子,子,子,子,子,子,子,子,子,子,子,子,子,子,子,子
**Time:** 35 hours | **时间:** 35 小时

## 问题 问题引入

> **【中文解读】**本节描述端到端微调流水线的核心挑战.2026年每一个认真的AI团队都维护一个微调流水线,不是为了训练前沿模型,而是为了下游适应 SFT、DPO 偏好对齐、蒸草稿模型用于投机解码、EAGLE-3 推理加速.工具链已经成熟了(Axolotl v0.8 + TRL 0.15 + Unsloth + vLLM 0.7),真正的工艺在YAML 配置、数据卫生和评估纪律中.

> **【拓展：微调工具链生态】**2026年微调工具:Axolotl v0.8(多 GPU SFT 配置驱动) 、TRL 0.15(DPO/GRPO/RLHF) 、Unsloth(单个 GPU 快速代,2-5x 加速) ⋅量化选择:GPTQ(马林 后端,推理最快)、AWQ(精度保持好)、GGUF(llama.cpp 兼容,CPU 推理好) ⋅服务端 vLLM 0.7 配合EAGLE-3 投机解吐码达2-3倍 吞升,接受率通常在0.65-0.80──8B 模型在 8xH100 上约6 小时,DPO  1.5时.──

每个认真的人工智能团队在2026年都会保持一个精细调节管道. 不是因为它们运输了一个边界基模型,而是因为下游适应 域 SFT,DPO与标记的偏好,蒸的草稿用于投机解码,使用EAGLE-3 是可测量的胜利现实. 亚克索洛特l v0.8处理多GPU SFT配置. 升值为0.15的DPO和GRPO. 不让你快速使用单GPU代. 通过使用 EAGLE-3 的 vLLM 0.7 能够在质量不损失的情况下推出2~3倍的解码吞吐量. 工具工作;工艺在YAML,数据卫生和评估纪律.

> 2026年每个认真的AI团队都保持一个随时可用的微调管道――不是因为它们发布前沿基础模型,而是因为下游适应领域的SFT――针对标记偏好的DPO――用于投机解码的蒸草稿――使用EAGLE-3 服务是可衡量的收益所在――Axolotl v0.8 处理多GPU SFT配置――TRL 0.15 处理 DPO 和 GRPO――Unsloth 让你快速进行单个GPU ──vLLM 0.7 配合EAGLE-3 在不损失质量的情况下解码吞吐量高2-3倍――工具链推行有效;工艺在YAML 配置、数据和健康评估纪律中.

您将通过SFT运行8B基 (Llama 3.3,Qwen3或Gemma 3) 然后通过任务特定数据进行DPO,为服务量化,并对lm-评估-harness,RewardBench-2,MT-Bench-v2和MMLU-Pro进行加密测量.您将根据2026模型开放框架生成一个模型卡.问题是可复制性一个命令重复整个管道端到端.

> 你将在任务特定数据上对8B基础模型进行运行,然后DPO,量化用于服务,并对照lm-评估-运营,RewardBench-2、MT-Bench-v2 和MMLU-Pro测量收益.

## 概念的核心概念

> **【中文解读】**流水线分五个阶段:数据(去重/质量过/PII 脱敏/污染检查)→SFT(Axolotl YAML, ZeRO-3, 8xH100,余弦调度,2-3轮)→DPO/GRPO(TRL, 偏好对,beta 调参)→ 量化(GPTQ+AWQ+GGUF 三种格式)→ 服务物(vLLM 0.7 + EAGLE-3,K8s 部署) ─交付是消融实验对比表:SFT-only vs SFT+DPO vs SFT+GRPO,以及服务标志和安全性评估──

> **【拓展：GRPO 与 DPO 对比】**直接偏好优化) 直在偏好对上训练,简单高效,但需要人工标注.

管道有五个阶段.**Data**除 (MinHash/Datatrove),质量过器 (Nemotron-CC类别分类器),PII除,对公共基准污染进行分离卫生检查. **SFT**子,子,子,子,子,子,子,子,子,子,子,子,子,子,子,子,子,子,子,子,子,子,子,子,子,子,子,子,子,子,子,子,子,子,子,子,子,子,子,子,子,子,子,子,子,子,子,子,子,子,子,子,子,子,子,子,子,子,子,子,子,子,子,子,子,子,子,子,子,子,子,子,子,子,子,子,子,子,子,子,子,子,子,子,子.**DPO or GRPO**: TRL配置, 1 时代, 偏好对, 无论是标记或模型判断, beta调整. **Quantize**:GPTQ+AWQ+GGUF 实现部署灵活性. **Serve**果: 果: 果: 果: 果: 果: 果: 果: 果: 果: 果: 果: 果: 果: 果: 果: 果: 果: 果: 果: 果: 果: 果: 果: 果: 果: 果: 果: 果: 果: 果: 果: 果: 果: 果: 果: 果: 果: 果: 果: 果: 果: 果: 果: 果: 果: 果: 果: 果: 果: 果: 果: 果: 果: 果: 果: 果: 果: 果: 果: 果: 果: 果: 果: 果: 果:

> 管道有五个阶段.**数据**为了防止污染,我们必须要做好一些检查.**SFT**,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,**DPO 或 GRPO**预测:TRL 配置,1轮,偏好对人工标记或模型评判,beta调参.**量化**据报道,该部门的负责人在此期间表示,**服务**根据排队等待的HPA,K8s部署.

运行量是可交付的:仅SFT对SFT+DPO对SFT+GRPO在三个任务特定基准上.服务量:批量1/8/32,EAGLE-3接受率,$/1M代币.安全评估:Llama Guard4通过率.模型卡:偏见评估,可再生性种子,数据许可.

> 消融实验是交付物品:三个任务特定基准上的SFT-only vs SFT+DPO vs SFT+GRPO──服务指标:批量1/8/32 时的代币/s、EAGLE-3 接受率、$/1M代币──安全评估:Llama Guard 4 通过率──模型卡:偏见评估、可复现性种子、数据许可──

## 建筑,建筑

```
raw data (HF datasets + internal)
    |
    v
Datatrove dedup + Nemotron-CC quality filter + PII scrub
    |
    v
split hygiene (MMLU-Pro contamination check)
    |
    v
Axolotl SFT config (YAML)  ---> 8xH100, ZeRO-3
    |
    v
TRL DPO / GRPO config       ---> 4xH100, 1 epoch
    |
    v
GPTQ + AWQ + GGUF quantize
    |
    v
vLLM 0.7 + EAGLE-3 speculative decoding
    |
    v
K8s deployment, HPA on queue-wait
    |
    v
lm-eval-harness + RewardBench-2 + MT-Bench-v2 + MMLU-Pro
    |
    v
model card (2026 MOF) + safety eval (Llama Guard 4)
```

##  技术

- 数据:用于减产的数据库,用于质量的Nemotron-CC分类器,用于PII的Presidio
  中文翻译:数据:数据源用于测试,质量为Nemotron-CC分类器,PII的Presidio
- 基:拉马3.3 8B,Qwen3 14B,或Gemma3 12B
  中文翻译:基础:拉马3.3 8B,Qwen3 14B,或Gemma 3 12B
- 光:Axolotl v0.8 配备ZERO-3,闪光注意3,包装序列
  中文翻译:SFT:Axolotl v0.8 与ZERO-3,闪光注意3,包装序列
- 偏好调整:DPO或GRPO的TRL0.15;单GPU代的Unsloth
  中文翻译:偏好调整:DPO或GRPO的TRL0.15;单GPU代的Unsloth
- 量化:GPTQ (马林),AWQ,GGUF通过 llama.cpp
  中文翻译:量化:GPTQ (马林),AWQ,GGUF通过 llama.cpp
- 服务:vLLM 0.7 含有EAGLE-3投机解码 (或SGLang 0.4 + SpecForge)
  中文翻译:服务:vLLM 0.7 含EGLE-3 投机解码 (或SGLang 0.4 + SpecForge)
- 评价:lm评价,回报-2,MT,v2,MMLU-Pro
  中文翻译:Eval:lm-评估-,回报Bench-2,MT-Bench-v2,MMLU-Pro

> 中文翻译:Eval:lm-评估-利用,回报Bench-2,MT-Bench-v2,MMLU-Pro(翻译)

- 安全评估:Llama Guard 4,ShieldGemma-2
  中文翻译:安全评估:拉马卫队4,盾牌Gemma-2
- 基础设施:Kubernetes + NVIDIA设备插件,HPA在排队等待量度上
  中文翻译:基础设施:Kubernetes + NVIDIA设备插件,HPA在排队等待量度上
- 观察性:W&B用于训练,Langfuse用于推断
  中文翻译:可观察性:W&B用于训练,Langfuse用于推断

## 动手构建

> **【中文解读】**构建 8 个阶段:数据管道(数据库 去重量 + 质量分类 + PII 清洗) 污染检查(MinHash对基准测试集) SFT(Axolotl SFT(ZeRO-3 + FA3 + 序列打包) 、TRL DPO/GRPO 偏好对齐、GPTQ/AWQ/GGUF 三种量化、vLLM 投机解码推理、完整评估(SWE-bench/HumanEval+/GPQA) 和成本分析────

> **【拓展：端到端微调在 LLM 公司中的标准化流程】**测量系统的LLaMA 微调流程、Mistral的模型工厂、Cohere的命令系列都遵循相同的阶段:预训练 -> SFT -> DPO/RLHF -> 量化 -> 部署──2026年的标准化工具链:Axolotl或 LLaMA-Factory(训练配置)、TRL(对齐)、AutoGPTQ/AutoAWQ(量化、vLLM或TensorRT-LLM(推推) ─关键指标:$/1M代币对商业API 价格──
```figure
ce-finetune-stages
```

## 建立它

1. **Data pipeline.**运行数据库的原始数据库,应用Nemotron-CC类型的质量分类器,Presidio扫描PII,写列车/分区,用明确的种子.
   中文翻译:1. **Data pipeline.**运行数据库的原始数据库,应用Nemotron-CC类型的质量分类器,Presidio扫描PII,写列车/分区,用明确的种子.

2. **Contamination check.**对于每次验证分区,计算MinHash与MMLU-Pro,MT-Bench-v2,RewardBench-2测试组. 拒绝任何重叠.
   翻译: 翻译:**Contamination check.**对于每次验证分区,计算MinHash与MMLU-Pro,MT-Bench-v2,RewardBench-2测试组. 拒绝任何重叠.

3. **Axolotl SFT.**果,果,果,果,果,果,果,果,果,果,果,果,果,果,果,果,果,果,果,果,果,果,果,果,果,果,果,果,果,果,果,果,果,果,果,果,果,果,果,果,果,果,果,果,果,果,果,果,果,果,果,果,果,果,果,果,果,果,果,果,果,果,果,果,果,果,果,果,果,果,果,果,果,果,果,果,果,果,果,果,果,果,果,果,果,果,果,果,果,果,.
   翻译: 翻译:**Axolotl SFT.**果,果,果,果,果,果,果,果,果,果,果,果,果,果,果,果,果,果,果,果,果,果,果,果,果,果,果,果,果,果,果,果,果,果,果,果,果,果,果,果,果,果,果,果,果,果,果,果,果,果,果,果,果,果,果,果,果,果,果,果,果,果,果,果,果,果,果,果,果,果,果,果,果,果,果,果,果,果,果,果,果,果,果,果,果,果,果,果,果,果,.

> 翻译: 翻译:**Axolotl SFT.**姆尔与ZERO-3,FA3,序列包装.8xH100上2-3个时代.登录W&B.


4. **TRL DPO / GRPO.**通过SFT检查点,在优先对进行一次DPO (或GROP以数学/代码的可验证奖励).
   翻译: 翻译:**TRL DPO / GRPO.**通过SFT检查点,在优先对进行一次DPO (或GROP以数学/代码的可验证奖励).

5. **Quantize.**产生三个量子:GPTQ-INT4-Marlin,AWQ-INT4,GGUF-Q4_K_M,用于 llama.cpp. 记录大小和名义吞吐量.
   翻译: 五.**Quantize.**产生三个量子:GPTQ-INT4-Marlin,AWQ-INT4,GGUF-Q4_K_M,用于 llama.cpp. 记录大小和名义吞吐量.

6. **Serve with speculative decoding.**通过Red Hat Speculators训练的EAGLE-3草案负责人配置. 测量批量1/8/32的接受率和尾延迟. 报告 $/1M代币与人类/OpenAI在同一评估.
   翻译: 七个字**Serve with speculative decoding.**通过Red Hat Speculators训练的EAGLE-3草案负责人配置. 测量批量1/8/32的接受率和尾延迟. 报告 $/1M代币与人类/OpenAI在同一评估.

7. **Eval matrix.**运行lm-eval-harness,RewardBench-2,MT-Bench-v2,MMLU-Pro,仅基于SFT,SFT+DPO,SFT+GRPO. 制作表.
   翻译:7.**Eval matrix.**运行lm-eval-harness,RewardBench-2,MT-Bench-v2,MMLU-Pro,仅基于SFT,SFT+DPO,SFT+GRPO. 制作表.

8. **Safety eval.**发射器的Llama Guard4传输速率.
   翻译:8.**Safety eval.**发射器的Llama Guard4传输速率.

9. **Model card.**文件: 文件: 文件: 文件: 文件: 文件: 文件: 文件: 文件: 文件: 文件: 文件: 文件: 文件: 文件: 文件: 文件: 文件: 文件: 文件: 文件: 文件: 文件: 文件: 文件: 文件: 文件: 文件: 文件: 文件: 文件: 文件: 文件: 文件: 文件: 文件: 文件: 文件: 文件: 文件: 文件: 文件: 文件: 文件: 文件: 文件: 文件: 文件: 文件: 文件: 文件: 文件: 文件: 文件: 文件: 文件: 文件: 文件: 文件: 文件: 文件: 文件: 文件: 文件: 文件:
   翻译:9.**Model card.**文件: 文件: 文件: 文件: 文件: 文件: 文件: 文件: 文件: 文件: 文件: 文件: 文件: 文件: 文件: 文件: 文件: 文件: 文件: 文件: 文件: 文件: 文件: 文件: 文件: 文件: 文件: 文件: 文件: 文件: 文件: 文件: 文件: 文件: 文件: 文件: 文件: 文件: 文件: 文件: 文件: 文件: 文件: 文件: 文件: 文件: 文件: 文件: 文件: 文件: 文件: 文件: 文件: 文件: 文件: 文件: 文件: 文件: 文件: 文件: 文件: 文件: 文件: 文件: 文件:

## 用它使用方法

```
$ ./pipeline.sh config/llama3.3-8b-domainX.yaml
[data]    300k deduped, 12k filtered, 280k accepted (seed=7)
[SFT]     3 epochs, 8xH100, 6h12m, val loss 1.42 -> 1.03
[DPO]     1 epoch, beta=0.08, 4xH100, 1h40m
[quant]   GPTQ-INT4 4.6 GB, AWQ-INT4 4.8 GB, GGUF-Q4_K_M 5.1 GB
[serve]   vLLM 0.7, EAGLE-3 acceptance 0.74, p99 126ms @ bs=8
[eval]    MMLU-Pro +3.2, MT-Bench-v2 +0.41, RewardBench-2 +0.08
[card]    model-card.md generated under 2026 MOF
```

## 发射上线

`outputs/skill-finetuning-pipeline.md`单个命令通过SFT运行数据,通过DPO运行数据,通过quant运行数据,通过evalu运行数据,并发出一个模型卡+服务的终端点.

> `outputs/skill-finetuning-pipeline.md`描述交付物品. 一条命令从数据到SFT到DPO到量化到服务到评估,并输出模型卡+服务端点.

| Weight | Criterion | How it is measured |
| 权重 | 标准 | 如何衡量 |
|:-:|---|---|
| 25 | Eval delta vs base | Measured gain on target tasks (MMLU-Pro, MT-Bench-v2, task-specific) |
| 25 | 评估增量 vs 基础 | 目标任务上的测量增益（MMLU-Pro、MT-Bench-v2、任务特定） |
| 20 | Pipeline reproducibility | One command reruns end to end with identical seeds |
| 20 | 管道可复现性 | 一条命令用相同种子端到端重跑 |
| 20 | Data hygiene | Dedup rate, PII scrub coverage, contamination check green |
| 20 | 数据卫生 | 去重率、PII 清洗覆盖率、污染检查通过 |
| 20 | Serving efficiency | tokens/s at bs=1/8/32, EAGLE-3 acceptance rate, $/1M tokens |
| 20 | 服务效率 | 批量 1/8/32 时的 tokens/s、EAGLE-3 接受率、$/1M tokens |
| 15 | Model card + safety eval | 2026 MOF completeness + Llama Guard 4 pass rate |
| 15 | 模型卡 + 安全评估 | 2026 MOF 完整性 + Llama Guard 4 通过率 |
| **100** | | |

## 练习题

1. 运行SFT+DPO vs SFT+GRPO仅针对SFT+DPO,并使用相同的任务指标. 报告哪种优先方法获胜以及多少.
   中文翻译:在同一任务特定基准上运行SFT-only vs SFT+DPO vs SFT+GRPO──报告哪种偏好方法获胜以及领先多少──

2. 换Llama 3.3 8B为Qwen3 14B. 测量1百万美元的代币,质量相匹配.
   中文翻译:将 Llama 3.3 8B 换为 Qwen3 14B──测量匹配质量下 $/1M代币──

3. 测量EAGLE-3域数据接受率与通用ShareGPT. 报告 delta和对延迟预算的含义.
   中文翻译:测量领域数据与通用 ShareGPT 上的EAGLE-3 接受率――报告差异及其对延迟预算的意义――

4. 射1%的污染 (泄漏MMLU-Pro答案到训练数据中) 然后再运行评估. 看MMLU-Pro精度跳不现实的. 建立一个检查污染的CI门,
   中文翻译:注入1% 污染(将MMLU-Pro 答案泄漏到训练数据中)并重跑评估;;观察MMLU-Pro 准确率不切实际跳跃;;构建能捕获这个问题的污染检查CI 门。

5. 添加LoRA SFT作为完全细调的替代品. 在10倍较低的内存下测量质量差距.
   中文翻译:添加LoRA SFT 作为全量微调的替代.

## 关键词 快速查找表

| Term | What people say | What it actually means |
| 术语 | 通俗说法 | 实际含义 |
|------|-----------------|------------------------|
| Axolotl | "SFT trainer" | Unified YAML-driven trainer for SFT, DPO, and distillation |
| Axolotl | "SFT 训练器" | 统一的 YAML 驱动训练器，用于 SFT、DPO 和蒸馏 |
| TRL | "Preference tuner" | Hugging Face library for DPO, GRPO, PPO on LLMs |
| TRL | "偏好调优器" | Hugging Face 库，用于 LLM 上的 DPO、GRPO、PPO |
| GRPO | "Group-relative policy optimization" | DeepSeek R1's RL recipe with verifiable rewards |
| GRPO | "组相对策略优化" | DeepSeek R1 的 RL 方法，使用可验证奖励 |
| EAGLE-3 | "Speculative decoding draft" | Draft heads that predict N tokens ahead; vLLM verifies with target model |
| EAGLE-3 | "投机解码草稿" | 预测 N 个 token 的草稿头；vLLM 用目标模型验证 |
| MOF | "Model Openness Framework" | 2026 standard for grading model releases on data, code, license |
| MOF | "模型开放框架" | 2026 年按数据、代码、许可对模型发布评分的标准 |
| Contamination check | "Split hygiene" | MinHash-based detection of test-set leakage into training |
| 污染检查 | "分割卫生" | 基于 MinHash 的测试集泄漏到训练中的检测 |
| Acceptance rate | "EAGLE / MTP metric" | Fraction of drafted tokens the target model accepts |
| 接受率 | "EAGLE / MTP 指标" | 目标模型接受的草稿 token 比例 |

## 继续阅读 继续阅读

- [Axolotl documentation](https://axolotl-ai-cloud.github.io/axolotl/)参考SFT/DPO培训员
  中文翻译:参考SFT / DPO 训练器
- [TRL documentation](https://huggingface.co/docs/trl) DPO和GRPO参考实施
  中文翻译:DPO 和 GRPO 参考实现
- [Unsloth](https://github.com/unslothai/unsloth)单GPU代引用
  中文翻译:单 GPU 代参考
- [DeepSeek R1 paper (arXiv:2501.12948)](https://arxiv.org/abs/2501.12948) GRPO 方法
  中文翻译:GRPO 方法论
- [vLLM + EAGLE-3 documentation](https://docs.vllm.ai)参考服务堆
  中文翻译:参考服务
- [SGLang SpecForge](https://github.com/sgl-project/SpecForge)替代投机解码训练师
  中文翻译:备选投机解码训练器
- [Model Openness Framework 2026](https://isocpp.org/)公开释放分类标准
  中文翻译:开放发布评分标准
- [lm-evaluation-harness](https://github.com/EleutherAI/lm-evaluation-harness)定律评价运行器
  中文翻译:规范评估运行器
