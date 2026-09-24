# 缩放定律

> 卡普兰论文说:较大的模型,损失较低. 霍夫曼论文说:你没有训练. 计算分为两个桶参数和代币,分歧不明显.

> **【中文解读】**尼奇拉定律揭示了模型大小,数据量,计算量的最佳关系.

**Type:** Study | **类型:** 学习
**Language:**子**语言:**字符串
**Prerequisites:** Phase 7 · 05 (Full Transformer), Phase 7 · 07 (GPT) | **前置知识:** Phase 7 · 05 (Full Transformer), Phase 7 · 07 (GPT)
**Time:** ~45 minutes | **时间:** ~45 分钟

## 问题 问题引入

训练计算的C FLOP,想要最好的模型,

> 当你有C FLOPs的训练计算量并想要最好的模型时,你面临两个旋律:

1. **How many parameters (N)?**较大的模型,更大的容量.
   翻译: 中文**多少参数（N）？**模型越大,容量越高.
2. **How many training tokens (D)?**更多数据,更好的容量利用.
   翻译: 中文**多少训练 token（D）？**数据越多,容量越好利用.

利率大约为`6 × N × D`你可以把N推上下,或者D推上下.

> 的速度大约按`6 × N × D`扩展――你可以增加N 减小D,或增加D 减小N――哪个更好?

在2022年前,答案是"按N硬".GPT-3 (2020) 是175B参数,训练在300B代币上.每参数约为1.7代币.卡普兰扩展法支持这一点.

> 之前,答案是"推大 N"──GPT-3(2020) 有175B参数,在约300B代币上训练──比例约为每个参数的1.7个代币──卡普兰缩放定律支持这一观点──

霍夫曼等人 (2022年),训练了一家小型号的模型,叫做奇拉,发现了不同的东西:最佳比例接近**20 tokens per parameter**比 (70B参数,1.4T代币) 在每一个基准上都比GPT-3 (175B,300B代币) 低2.5倍的推断成本.

> 霍夫曼等 (Hofmann 等人) 训练了一小组名为Chinchilla的模型,发现不同的结果:最优比例接近**每个参数 20 个 token**△GPT-3 低估训练10倍――Chinchilla(70B参数,1.4T代币) 在每个基准测试中都击败了GPT-3 ((175B,300B代币),推理成本仅为后者的2.5分之一――

2026年是智拉的世界,有一个重要的转折.Llama 3 8B 训练用了15万亿代币,每参数的比率为1,875代币.九十四倍超过智拉的最佳. 推理成本比规模使用的模型的训练成本更重要,因此对较小的可部署足迹进行过度训练 (过去的智拉) 是2026年默认的.

> 2026年是智拉的世界,但有一个重要的转折――Llama 3 8B使用了15亿代币训练,比例为每参数1875代币――是智拉最优的94倍――对于将被大规模使用的模型,推理成本比训练成本更重要,因此为了更小的部署足迹而过度训练 (超过智拉) 是2026年的默认策略――

> **【中文解读】**缩放定律的核心洞察:FLOPs ≈ 6 × N × D 参数 × 代币 数) ‧ ‧ ‧ ‧ ‧ ‧ ‧ ‧ ‧ ‧ ‧ ‧ ‧ ‧ ‧ ‧ ‧ ‧ ‧ ‧ ‧ ‧ ‧ ‧ ‧ ‧ ‧ ‧ ‧ ‧ ‧ ‧ ‧ ‧ ‧ ‧ ‧ ‧ ‧ ‧ ‧ ‧ ‧ ‧ ‧ ‧ ‧ ‧ ‧ ‧ ‧ ‧ ‧ ‧ ‧ ‧ ‧ ‧ ‧ ‧ ‧ ‧ ‧ ‧ ‧ ‧ ‧ ‧ ‧ ‧ ‧ ‧ ‧ ‧ ‧ ‧ ‧ ‧ ‧ ‧ ‧ ‧ ‧ ‧ ‧ ‧ ‧ ‧ ‧ ‧ ‧ ‧ ‧ ‧ ‧ ‧ ‧ ‧ ‧ ‧ ‧ ‧ ‧ ‧ ‧ ‧ ‧ ‧ ‧ ‧ ‧ ‧ ‧ ‧ ‧ ‧ ‧ ‧ ‧ ‧ ‧ ‧ ‧ ‧ ‧ ‧ ‧ ‧ ‧ ‧ ‧ ‧ ‧ ‧ ‧ ‧ ‧ ‧ ‧ ‧ ‧ ‧ ‧ ‧ ‧ ‧ ‧ ‧ ‧ ‧ ‧ ‧ ‧ ‧ ‧ ‧ ‧ ‧ ‧ ‧ ‧ ‧ ‧ ‧ ‧ ‧ ‧ ‧ ‧ ‧ ‧ ‧ ‧ ‧ ‧ ‧ ‧ ‧ ‧ ‧ ‧ ‧ ‧ ‧ ‧ ‧ ‧ ‧ ‧ ‧ ‧ ‧ ‧ ‧ ‧ ‧ ‧ ‧ ‧ ‧ ‧ ‧ ‧ ‧ ‧ ‧ ‧ ‧ ‧ ‧ ‧ ‧ ‧ ‧ ‧ ‧ ‧ ‧ ‧ ‧ ‧ ‧ ‧ ‧ ‧ ‧ ‧ ‧ ‧ ‧ ‧ ‧ ‧ ‧ ‧ ‧ ‧ ‧ ‧ ‧ 

> **【拓展：过度训练策略的经济逻辑】**拉马3 8B 用15T代币训练 (远超Chinchilla 最优的160B代币),推理成本却大幅降低了.这是因为推理时每个代币的计算量和参数的正比,8B参数的推理成本仅为70B模型的91/9.

## 概念的核心概念

![Chinchilla curves: loss vs compute at various N/D ratios](../assets/scaling-laws.svg)

### 霍夫曼法

根据"辛奇拉报"的报道,

> ,失败的结论:

```
L(N, D) = A / N^α + B / D^β + E
```

- `N`=参数 (非嵌入式).
  翻译: 中文`N`参数量 (非嵌入)
- `D`训练令牌
  翻译: 中文`D`训练符号数量
- `α ≈ 0.34`现在`β ≈ 0.28`它们的位置是相对的.
  翻译: 中文`α ≈ 0.34`,我知道.`β ≈ 0.28`们都在着.
- `E ≈ 1.69`没有任何可能的损失.
  翻译: 中文`E ≈ 1.69`没有任何损失.
- `A ≈ 406`现在`B ≈ 411`现在,我们要去.
  翻译: 中文`A ≈ 406`,我知道.`B ≈ 411`,我知道.

根据你的规模,两个术语对彼此进行交易.`N`在固定计算 (C = 6ND) 上,解决:

> 两项在扩展时相互制衡.`N`求导并求解:

```
N_opt ≈ 0.6 × (C/6)^0.5
D_opt ≈ 0.6 × (C/6)^0.5
D_opt / N_opt ≈ 20
```

计算最佳:每参数20个代币.

> 计算最优:每个参数是20个代币.

### 无论如何,为什么过度训练

鱼优化降低了每次训练的损失,但你只要一次支付训练费用,

> ,最优极限每次训练FLOP的训练损失――但训练成本只支付一次;推理成本永远持续――

对于一个每月服务的聊天机器人,推理占据总成本.拉马的方法:训练较小,更长. 8B在15T的代币是深入推理优化的:

> 对于每月服务的亿代币,推理主导总成本――Llama 的方法:训练更小,更长――8B 在15T代币上训练是深度推理优化:

- 适合消费者GPU.
  中文翻译:适配消费级 GPU。
- 延迟是70B的微小部分.
  中文翻译:延迟仅为70B林 最优的一小部分──
- 质量对于大多数任务来说是足够的.
  中文翻译:质量对大多数任务来说足够接近.

对于推断主导工作负载,正确的比率是每参数接近100500个代币,具体取决于服务量.

> 对于推理主导工作负载,正确的比例接近每参数100-500个代币,取决于服务量.

### 出现与流

声称:某些能力 (算术,多步推理,思想链接) 突然在某种程度上"出现".

> 声称:某些能力 (算术多步推理思维链遵循) 在某种规模"涌现"中.

谢弗等人 (2023) 认为这是一个测量器件:新兴指标使用不连续的分数 (准确匹配,门准确性) 隐藏了底层的逻辑的流改善.连续指标 (跨) 显示了流曲线.

> 谢弗等 (S Schaeffer 等人) 认为这是度量伪影:涌现指标使用不连续的评分 (精确匹配、值准确率),隐藏了底层逻辑的平滑改善──连续指标──交叉)显示平滑曲线──

根据2026年的统一意见,持续损失的预测是可靠的.基准跳跃通常是得分高的文物.根据持续指标规划预算.

> 2026年共识是:通过连续损失进行预测是可靠的.基准测试的跳转往往是评分标准的问题.

> **【中文解读】**"涌现能力" (涌现能力) 在2023年引发了大量的讨论.某些能力似乎突然出现在特定规模.但 Schaeffer等人证明,这可能是测量伪影:不连续的评分标准.

> **【拓展：数据质量比数据量更重要】**2026年缩小定律的新变量是数据质量――微软的 Phi 系列证明,精心选择的"高质量"代币可以有效提高计算量2倍以上――Llama 3 使用数据配分优化和合成数据增强――MoE 架构则进一步解了总参数数和活跃计算量――这些因素使传统的曲线需要重新校准――

### 2026年图片

规模化法仍然有效,但:

> 缩放定律仍然有效,但:

| Factor | Changed how |
|--------|-------------|
| 因素 | 变化方式 |
| Data quality | Curating "good" tokens (Phi-style) shifts curves by >2× effective compute |
| 数据质量 | 筛选"优质" token（Phi 风格）使曲线偏移超过 2 倍有效计算 |
| MoE | Total params decouple from active FLOPs; scaling laws per-active-FLOP |
| MoE | 总参数量与活跃 FLOPs 解耦；按活跃 FLOPs 的缩放定律 |
| Post-training | Some capabilities (instruction following, code) shift with SFT+RLHF more than pretraining |
| 后训练 | 某些能力（指令遵循、代码）通过 SFT+RLHF 的提升大于预训练 |
| Multimodality | Image + text tokens scale together; separate curves per modality |
| 多模态 | 图像 + 文本 token 一起扩展；每种模态有独立曲线 |
| Synthetic data | Models generate training data; effective compute can compound |
| 合成数据 | 模型生成训练数据；有效计算可复合增长 |

> **【拓展：合成数据与缩放定律的未来】**2026年缩写定律面临数据墙问题高质量的人类文本数据可能在未来几年耗尽.合成数据 (模型生成的训练数据) 是潜在的解决方案.微软的 Phi 系列使用GPT-4 生成的"教科书质量"合成数据进行训练,NVIDIA的 Nemotron使用合成数据增强.如果合成数据有效,缩写定律的"有效计算"可以持续增长.

光优化器 (Kimi Moonlight, 2024) 在匹配数据时显示了对 AdamW 的有效计算增长2x.一些2026 训练运行默认使用 Muon.改变了扩展法中的绝对常数,而不是其形状.

> 光光光光光光光光光光光光光光光光光光光光光光光光光光光光光光光光光光光光光光光光光光光光光光光光光光光光光光光光光光光光光光光光光光光光光光光光光光光光光光光光光光光光光光光光光光光光光光光光光光光光光光光光光光光光光光光光光光光光光光光光光光光光光光光光光光光光光光光光光光光光光光光光光光光光光光光光光光光光光光光光光光光光光光光光光光光光光光光光光光光光光光光光光光光光光光光光光光光光光光光光光光光光光光光光光光光光光光光光光光光光光光光光光光光光光光光光光光光光光光光光光光光光光光光光光光光光光光

## 建立它,实现它.
```figure
scaling-laws
```

## 建立它

看到`code/main.py`我们将吉拉损失方程运行,并解决计算最佳问题.`(N, D)`在每一个数个计算预算中.

> 参见`code/main.py`我们实现了比损失方程,并在多个计算预算下寻求最优的计算.`(N, D)`,我知道.

### 步骤1: 虫的损失

```python
def chinchilla_loss(N, D, A=406.4, B=410.7, alpha=0.34, beta=0.28, E=1.69):
    return A / N ** alpha + B / D ** beta + E
```

剧情`L`作为一个轮`(N, D)`在固定`C = 6ND`找最少的东西.

> 将`L`作为一个`(N, D)`等高线图,固定 `C = 6ND`△找到最小值.

### 步骤2:计算最佳边界

对于从 `1e17`为了`1e25`找出`(N, D)`减少损失`6ND = C`检查比率`D/N ≈ 20`现在,我们要去.

> 对于`1e17`到了`1e25`计算预算, 找到使损失最小化`(N, D)`约束`6ND = C`△验证比例`D/N ≈ 20`,我知道.

### 步骤3:过度培训成本

计算训练10×较小模型 (1/10的最佳N,10×最佳D) 所支付的额外损失.

> 计算训练一个10倍小模型 ((最优N的 1/10,最优D的 10倍) 所支付额外损失――报告作为交换的推理FLOP节约(与N 成正比) 』

### 步骤4:与实际模型进行比较

报名`(N, D)`对于GPT-3,Chinchilla,Llama 3 8B,DeepSeek-V3 (活性参数) 的对,并比较预测与报告损失.

> 输入GPT-3、Chinchilla、Llama 3 8B、DeepSeek-V3(活跃参数) 的已知 `(N, D)`对,比较预测损失与报告损失.

## 用它实现框架

你不可能自己训练一个边界模型,但扩展法则告诉你:

> 你不太可能自己训练前沿模型.

1. **Whether your fine-tune has enough data.**如果您的任务特定数据在基本模型的每个参数的20个代币以下,
   翻译: 中文**你的微调是否有足够数据。**如果你的任务的特定数据低于基础模型的每参数20个代币,预期会在某种损失下限和.
2. **Whether to pick a bigger base model.**如果您把所有的预算都花在推断上, 宁愿使用更小,更长的训练模型.
   翻译: 中文**是否选择更大的基础模型。**如果把所有的预算都放在推理上, 优先选择更小的模型,
3. **Where the returns diminish.**超过1000倍的吉拉最佳, 变量变得噪音.
   翻译: 中文**收益递减在哪里。**超过比较优 1000 倍后, 变化对数量损失变成噪音.

**The research trajectory in 2026:**

> **2026 年的研究方向：**

- **Data-constrained regime.**网络拥有有限的高质量的代币 (过后英语510万亿).边界预训练正在接近这个限度.合成数据,多语言,多模式和RLHF尺度的细调是下一个杆.
  翻译: 中文**数据受限时代。**网络上高质量代币 数量有限 过后约5-10亿英语) ⋅前沿预训练正在接近这个上限 ⋅合成数据 多语言多模态和RLHF 缩小微调是下一个杆──
- **Compute-multiplier tricks.**子优化器,MoE,更好的数据策划 每个都移动了绝对常数,而不是异常.
  翻译: 中文**计算倍增技巧。**变化 优化器,MoE,更好的数据策展各自改变绝对常数,而不是渐近线.
- **Scaling laws for RL.**早期证据表明,在RL样本中,
  翻译: 中文**RL 的缩放定律。**开放问题:早期证据表明,RL样本有律关系,但指数与预训大不相同.

## 运送它.

看到`outputs/skill-training-budget-estimator.md`技能选择`(N, D, hours, GPU)`根据计算预算,部署限制和目标损失,对新训练运行.

> 参见`outputs/skill-training-budget-estimator.md`△根据计算预算,部署约束和目标损失,为新训练运行选择`(N, D, hours, GPU)`,我知道.

## 练习题

1. **Easy.**跑步`code/main.py`打印西拉最佳`(N, D)`计算预算`1e20`现在`1e22`现在`1e24`比较真实模型表.
   中文翻译:运行 `code/main.py`印记计算预算为`1e20`,我知道.`1e22`,我知道.`1e24`时的鱼 最优 `(N, D)`与真实模型表相比
2. **Medium.**执行霍夫曼的损失函数计算曲线.`log10(C)`确定法律预测我们需要什么时候`>10^28`对于下一个0.1的交叉缩减.
   中文翻译:实现霍夫曼损失计算量曲线――绘制计算最优前沿的损失与`log10(C)`△确定定律预测何时需要`>10^28`才能使交叉再降低0.1──
3. **Hard.**根据你自己的规模法, 根据同一数据集训练的5个小模型 (100K到10M参数).`α`其他`E`你的表达符与出版的表达符有多好?
   中文翻译:在同一数据集上训练5个小模型 (参数100K到10M) 并适应自己的缩放定律.`α`和 `E`,你的指数与发布值的匹配性如何?

## 关键词 快速查找表

| Term | What people say | What it actually means |
|------|-----------------|-----------------------|
| 术语 | 通俗说法 | 实际含义 |
| Parameters (N) | "Model size" | Non-embedding weight count; determines capacity. |
| 参数 (N) | "模型大小" | 非嵌入权重数量；决定容量。 |
| Tokens (D) | "Training data" | Number of training tokens seen; determines how well the parameters get used. |
| Token (D) | "训练数据" | 看到的训练 token 数量；决定参数被利用的程度。 |
| Compute (C) | "FLOPs spent" | Approximately `6 × N × D` for a standard transformer. |
| 计算量 (C) | "FLOPs 花费" | 标准 Transformer 约为 `6 × N × D`。 |
| Chinchilla-optimal | "D/N ≈ 20" | Ratio that minimizes loss per FLOP of pretraining. |
| Chinchilla 最优 | "D/N ≈ 20" | 最小化每个预训练 FLOP 损失的比例。 |
| Over-training | "Past Chinchilla" | Spend extra training FLOPs to save inference FLOPs; D/N >> 20. |
| 过度训练 | "超过 Chinchilla" | 额外训练 FLOPs 以节省推理 FLOPs；D/N >> 20。 |
| Irreducible loss | "The floor" | The `E` term in the scaling law; the entropy of the data itself. |
| 不可约损失 | "底线" | 缩放定律中的 `E` 项；数据本身的熵。 |
| Emergent capability | "Sudden jumps at scale" | Often a scorer artifact; continuous loss is smooth. |
| 涌现能力 | "规模上的突然跳变" | 通常是评分伪影；连续损失是平滑的。 |
| Effective compute | "Training-efficiency multiplier" | Better data / optimizer / architecture multiplies how far a FLOP goes. |
| 有效计算 | "训练效率倍增器" | 更好的数据/优化器/架构使每个 FLOP 走得更远。 |

## 继续阅读 继续阅读

- [Kaplan et al. (2020). Scaling Laws for Neural Language Models](https://arxiv.org/abs/2001.08361)第一份规模化法律论文;
  中文翻译:第一篇缩放定律论文;低估训练了──
- [Hoffmann et al. (2022). Training Compute-Optimal Large Language Models](https://arxiv.org/abs/2203.15556) ,我知道.
  中文翻译:Chinchilla论文。
- [Schaeffer et al. (2023). Are Emergent Abilities of Large Language Models a Mirage?](https://arxiv.org/abs/2304.15004)作为测量器件出现.
  中文翻译:涌现能力是否是幻觉的论文──
- [Sardana, Frankle (2024). Beyond Chinchilla-Optimal: Accounting for Inference in Language Model Scaling Laws](https://arxiv.org/abs/2401.00448)为什么拉马的过度训练是适合工作量.
  中文翻译:为什么拉马的过度训练对其工作负载是正确的.
- [Jordan et al. (2024). Muon: An optimizer for hidden layers in neural networks](https://kellerjordan.github.io/posts/muon/) 2x计算乘法.
  中文翻译:Muon 优化器,2倍计算倍增器──
