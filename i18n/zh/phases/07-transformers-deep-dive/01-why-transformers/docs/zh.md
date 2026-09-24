# 为什么变革器  问题与RNN
# 为什么是变压器RNN的问题

> 转变器一次处理所有代币.这一次建筑投注改变了深度学习的每一个扩展曲线,2017年后.

> 转换器 一次性处理所有代币――这一个结构注在2017年之后改变了深度学习中的每条扩展曲线――

> **【中文解读】**转变器用自主注意力解决了这三个问题,开启了深度学习的新时代.

**Type:** Learn | **类型:** 学习
**Language:**子**语言:**字符串
**Prerequisites:** Phase 3 (Deep Learning Core), Phase 5 · 09 (Sequence-to-Sequence), Phase 5 · 10 (Attention Mechanism) | **前置知识:** 阶段 3（深度学习基础），阶段 5 · 09（序列到序列），阶段 5 · 10（注意力机制）
**Time:** ~45 minutes | **时间:** ~45 分钟

## 学习目标

- 了解复发神经网络 (RNN) 的三大致命弱点
  了解循环神经网络的三个致命弱点
- 解释为什么连续深度,而不是运行数量,决定了GPU训练时间
  解释为什么串行深度 (而不是操作数) 决定了GPU训练时间
- 进行序列建模任务中的RNN与变压器复杂性比较
  与变压器相比,序列建模任务的复杂性
- 确定RNN或国家空间模型仍然可能优先的场景
  识别RNN或状态空间模型仍然更优秀的场景
- 识别从本地转向全球关注的诱导偏见
  认识从局部性转向全局注意力归纳偏好转移

## 问题 问题引入

在2017年之前,地球上每一个最先进的序列模型都是一个反复的神经网络.LST和GRU在半十年内获得了像网相当的翻译基准.它们是唯一的工具.

> 在2017年之前,全球每一个最先进的序列模型语言"",翻译"",语音都是循环神经网络――LSTM和GRU在相当于Imagnet级的翻译基准测试上称了五年――它们是所有人的唯一工具――

它们有三个致命的缺点. 序列计算意味着你不能沿时间轴平行化:`t+1`需要隐藏状态的代币`t`一个1024代币的序列意味着1 024个串行步骤在一个GPU上,可以每周期完成1,000,000个浮点操作.训练墙钟时间以线性方式与平行设计的硬件上的序列长度进行扩展.

> 它们有三个致命的弱点.`t+1`需要来自代币`t`隐藏状态――一个1024个代币的序列意味着每周期可执行1,000,000次浮点运算的GPU上要运行1024个串行步骤――在设计为并行性的硬件上,训练时间随序列长度线性增长――

> **【中文解读】**第一个致命弱点:串行计算.RNN必须按顺序处理每个代币,完全无法利用GPU的并行计算能力.

消失的梯度意味着50代币的信息已经被压缩到50个非线性.关闭的复发单位 (LSTM,GRU) 缓和了压缩,但从来没有消除过它.长距离的依赖性"我去年夏天在飞机上读到的书..."经常失败.

> 梯度消失意味着50个代币 之前的信息已经被50个非线性变化压缩了大部分.门控循环单元 (LSTM、GRU) 缓解了这种压力,但从未消除过.长程依赖"我去年夏天在飞往京都的飞机上读的书是......"经常失败了。

> **【中文解读】**第二个致命弱点:梯度消失.经过50层非线性变化后,远处的信息几乎完全丢失.

固定的宽度隐藏状态意味着编码器在解码器看到任何东西之前将整个源序列挤入一个单个向量.源源是否是5个代币或500个,不管是什么,瓶是相同的形状.

> 固定宽度的隐藏状态意味着编码器在解码器看到任何内容之前,将整个源序列压缩成一个向量――无论源序列是5个代币还是500个;瓶的形状都一样――

> **【中文解读】**第三个致命弱点:固定宽度瓶──编码器必须将整个源序列压缩到一个固定长度的向量中信息瓶──是结构性的──变压器的自主注意力使每个位置都能够直接访问所有其他位置,彻底消除了这个瓶──

2017年"注意力是你需要的"论文提出了一些根本的建议:完全放弃复发.让每个位置并行地关注其他位置.

> 2017年论文"注意力是你需要的"提出了一个激进的方案:完全放弃循环――让每个位置同时关注所有其他位置――用一次大规模矩阵乘法代替1024次串行计算――

结果在2026年之前占据所有模式的主导地位.语言 (GPT-5,Claude 4,Llama 4),视觉 (ViT,DINOv2,SAM 3),音频 (声),生物学 (AlphaFold 3),机器人 (RT-2).相同的区块,不同的输入.

> 到2026年,其成果主导了每种模态――语言――GPT-5、Claude 4、Llama 4)、视觉――ViT、DINOv2、SAM 3)、音频――语)、生物学――AlphaFold 3)、机器人――RT-2――相同的模块,不同的输入――

## 概念的核心概念

![RNN sequential compute vs Transformer parallel attention](../assets/rnn-vs-transformer.svg)

**Recurrence as a bottleneck.**电脑计算器`h_t = f(h_{t-1}, x_t)`每一步都取决于前一步.`h_5`在之前`h_4`在现代GPU上,有10,000多个并行芯,

> **循环即瓶颈。**计算`h_t = f(h_{t-1}, x_t)`,每一步都取决于前一步.`h_4`之前计算`h_5`在拥有10,000+的现代GPU中,这浪费了99%的芯片计算能力.

> **【中文解读】**循环是瓶的本质:每时间步骤的计算都取决于前一步的结果.GPU擅长数以千计的并行操作,而RNN的串行依赖使其只能用于 GPU的极小部分算力.

**Attention as a broadcast.**自我注意力计算`output_i = sum_j(a_ij * v_j)`对于每一个对`(i, j)`整个N×N注意力矩阵都填充了一个批量的. 没有一步取决于另一个. GPU 很喜欢它.

> **注意力即广播。**为了每对`(i, j)`计算`output_i = sum_j(a_ij * v_j)`△整个N×N注意力矩阵在一次批量矩阵乘法中填满.

**The speedup is not a constant.**它们的区别是`O(N)`系列深度和`O(1)`在实践中,变压器在N=512的匹配硬件上每时训练510倍快,并且随着序列长度的增加,间隙会扩大,直到你达到`O(N²)`记忆注意力墙 (后者被Flash Attention修复了见12课).

> **加速不是常数。**它是`O(N)`串行深度与`O(1)`在实践中,在匹配硬件上N=512时,变压器每个时代的训练速度快5到10倍,而且随着序列长度的增加,差距不断扩大,直到你碰到注意力.`O(N²)`后修复了它见第12课)

**What transformers cost.**关注记忆规模如`O(N²)`对于2K文本来说,很好.对于128K文本来说,你需要滑窗,ROPE外分,闪光注意力,或线性注意力变体.`O(N)`转换器将时间换取记忆,然后通过平行性获取时间.

> **Transformer 的代价。**注意力内存按 `O(N²)`增长――对于2K上下文,没有问题――对于128K上下文,你需要滑动窗口――RoPE外推――Flash Attention 分块计算或线性注意力变化――循环在时间和内存上都是`O(N)`转换器用内存换时间,然后通过并行性赢回时间.

**The inductive bias shift.**变压器认为没有什么每个对都是关注的候选人.这就是为什么变压器需要更多的数据来训练好,但一旦有了更大的规模.辛奇拉 (2022) 正式化了这一点:给出足够的代币,变压器总是击败一个相同参数数数的RNN.

> **归纳偏好的转变。**转变器不做任何假设 每对都是注意力的候选人. 这就是为什么转变器需要更多数据来训练好,但一旦拥有足够的数据就能扩展得更远.

> **【中文解读】**归纳偏好转移是变压器成功的关键洞察.RNN 隐式假设"近处的代币更重要",而变压器不做任何假设任何两个位置之间可以建立直接联系.

> **【拓展：Chinchilla 缩放定律】**深思之中的智论文 (DeepMind's Chinchilla 论文) 证明,模型参数和训练数据量应等比例增长. 这解释了为什么Llama、GPT-4等模型需要数亿级的训练数据,

## 建立它,实现它.
```figure
rnn-vs-parallel
```

## 建立它

我们数量模拟核心瓶,让你感觉到笔记本电脑上的空隙.

> 没有神经网络,我们用数值模拟核心瓶子,让你在笔记本电脑上感觉到差距.

> **【中文解读】**这一节使用纯数值模拟让你亲切感受串行与串行的性能差距.关键在于"依赖深度"串行链的深度为N,而并行归约深度仅为O(1) 或O(log N) ⋅这是变压器比RNN快的根本原因.

### 步骤1:测量连线深度

看到`code/main.py`我们构建两个函数.一个编码一个序列作为一个连接链 (连续,像RNN一样).一个编码它作为一个平行减小 (像广播,像注意力).同样的数学,不同的依赖图.

> 参见`code/main.py`我们构建两个函数――一个将序列编码为加法链(串行,类似RNN) ――一个将其编码为并行归约(广播,类似注意力) ――相同的数学,不同的依赖图――

```python
def rnn_style(xs):
    h = 0.0
    for x in xs:
        h = 0.9 * h + x   # can't parallelize: h depends on previous h
    return h

def attention_style(xs):
    return sum(xs) / len(xs)  # every x is independent
```

我们在连续上都能计时到10万个元素.RNN版本是O(N) 和单个CPU管道.即使在纯Python中,注意力式的减小也超过了1000,因为Python的`sum()`执行C语言,并且每步无解释器的代价.

> 我们对长达10万个元素的序列进行计数.RNN版本是O(N) 的单个CPU流水线.即使在纯Python中,注意力式归约在长度≥1000时也能胜出,因为Python的`sum()`没有解释器的逐步开销.

### 计算理论操作数

两个算法都会增加N. 区别是 *依赖深度*:在下一个开始之前,必须进行多次操作. RNN深度 = N. 注意深度 = log(N) 通过树缩小,或1通过并行扫描.深度,而不是操作数量,决定了GPU时间.

> 两种算法都做N 次加法――区别在于*依赖深度*:在下一个操作开始之前,必须顺序执行多少操作――RNN深度 = N――注意力深度 = 用树形归约时为 log(N),用并行扫描时为 1――决定GPU 时间是深度,而不是操作数――

### 步骤3:长序列上的实证扩展

我们打印了一个时间表,使得O(N) 差距可见.在2026 Mac笔记本电脑上,1000个元素以下的序列太快以测量.100,000的序列显示了清洁的线性扫描.将其量化为16,384个代币变压器和12层LSTM等级,你会看到为什么训练墙钟在2016年是阻碍者.

> 我们打印了一张使 O(N) 差距可见的计时表――在2026年Mac笔记本上,少于1,000个元素的序列太快,无法测量――100,000个元素的序列显示出清晰的线性扫描――将其扩展到具有12层LSTM等效力的16,384个代币变压器,你就会明白为什么2016年训练时间是瓶――

## 用它实现框架

在2026年,还可以选择什么时候:

> 2026 年何时仍应选择RNN:

> **【中文解读】**虽然变压器在大多数场景中胜出,但并非万能――流式推理(每次只处理一个代币) 超长序列(>1M代币) 和边缘设备场景下,RNN或状态空间模型(如Mamba) 仍然有优势――2026年趋势是混合架构(如Jamba),结合两者优势――

> **【拓展：Mamba 与状态空间模型】**通过选择性扫描机制实现了O (N) 复杂的序列建模,同时支持并行训练. 它本质上是一种参数化的RNN,但在训练效率上接近变压器. 在代码生成,长文档理解等任务中,混合的Mamba+变压器架构已成为前沿实验室的重要探索方向.

| Situation | Pick / 场景 | 选择 |
|-----------|-------------|------|
| Streaming inference, one token at a time, constant memory | RNN or state-space model (Mamba, RWKV) |
| Very long sequences (>1M tokens) where attention memory explodes | Linear attention, Mamba 2, Hyena |
| Edge device with no matmul accelerator | Depthwise-separable RNN still wins on FLOPs/watt |
| Anything else (training, batched inference, context up to 128K) | Transformer |

像Mamba这样的国家空间模型 (SSM) 基本上是具有结构化参数化的RNN,`O(N)`通过选择性扫描,他们恢复了变压器质量的90%通过更好的长文本扩展. 2026年,大多数边境实验室都将混合型SSM+变压器模型 (例如Jamba,Samba) 训练.

> 状态空间模型 (SSM) 如Mamba本质上是具有结构化参数化的RNN,兼具两者的优势:`O(N)`扫描内存,通过选择性扫描实现并行训练――它们恢复了变压器90%的质量,同时具有更好的长上下文扩展性――2026年大多数前沿实验室训练混合SSM+变压器模型(如Jamba、Samba) 循环没有消失,它是一个组件――

## 运送它.

看到`outputs/skill-architecture-picker.md`由于长度,吞吐量和训练预算限制,技能选择一个新序列问题架构. 它应该始终拒绝推纯粹的RNN在训练运行超过1B代币的情况下,而不说明交易.

> 参见`outputs/skill-architecture-picker.md`△该技能为新序列问题选择架构,给定长度,吞吐量和训练预算约束. 它应永远拒绝推纯RNN,除非声明权衡.

> **【拓展：架构选择决策树】**在实际工程中,架构选择需要考虑多个维度:序列长度,延迟要求,内存预算,训练数据量,部署硬件.对于大多数NLP任务,仅使用Decoder的变压器是默认选择.对于超长序列,考虑Mamba或混合架构.对于边缘部署,量化RNN/SSM可能更合适.

## 练习题

1. **Easy / 简单。**接下来`rnn_style`其他`code/main.py`测量重复. 随着隐藏状态的维度,连续上层多少长?
   取 `code/main.py`中中 `rnn_style`标量隐藏状态向量将被换成长度64的隐藏状态向量.

2. **Medium / 中等。**通过纯 Python 实现平行前总数 (Hillis-Steele 扫描). 验证它产生与1024长度的连续扫描相同的数值输出.
   使用纯Python 实现并行前和(Hillis-Steele 扫描) 验证它在长度 1024 上产生与串行扫描相同的数值输出――计算深度――

3. **Hard / 困难。**按GPU上将注意力式降低调整到PyTorch. 时间同时扫描序列长度从64到65,536. 绘制并解释曲线形状.
   将注意力风格归约移植到GPU上方的PyTorch――在序列长度从64扫到65,536时对两者计时――绘制并解释曲线形状――

## 关键词 快速查找表

| Term | What people say / 术语 | 人们怎么说 | What it actually means / 实际含义 |
|------|----------------------|-----------|----------------------------------|
| Recurrence | "RNNs are sequential" | 循环 (Recurrence) | Computation where step `t` depends on step `t-1`, forcing serial execution along the time axis. 步骤 `t` 依赖于步骤 `t-1` 的计算，强制沿时间轴串行执行。 |
| Serial depth | "How deep the graph is" | 串行深度 (Serial depth) | Longest chain of dependent ops; bounds wall-clock even on infinite hardware. 依赖操作的最长链；即使在无限硬件上也限制了时间开销。 |
| Attention | "Let tokens look at each other" | 注意力 (Attention) | Weighted sum `sum_j a_ij v_j` where `a_ij` comes from a similarity score between positions i and j. 加权求和 `sum_j a_ij v_j`，其中 `a_ij` 来自位置 i 和 j 之间的相似度得分。 |
| Context window | "How much the model sees" | 上下文窗口 (Context window) | Number of positions an attention layer can take as input; quadratic memory cost scales here. 注意力层可作为输入的位置数；二次内存开销在这里缩放。 |
| Inductive bias | "Assumptions baked into the architecture" | 归纳偏好 (Inductive bias) | Prior about what the data looks like; CNNs assume translation invariance, RNNs assume recency. 关于数据外观的先验；CNN 假设平移不变性，RNN 假设邻近性。 |
| State-space model | "RNN with algebra behind it" | 状态空间模型 (State-space model) | Recurrence parameterized for parallel training via structured state-space matrices. 通过结构化状态空间矩阵参数化以实现并行训练的循环。 |
| Quadratic bottleneck | "Why context costs so much" | 二次瓶颈 (Quadratic bottleneck) | Attention memory = `O(N²)` in sequence length; Flash Attention hides the constants, not the scaling. 注意力内存 = 序列长度的 `O(N²)`；Flash Attention 隐藏了常数，而非缩放。 |

## 继续阅读 继续阅读

- [Vaswani et al. (2017). Attention Is All You Need](https://arxiv.org/abs/1706.03762)这篇论文杀死了主流NLP的复发.
  瓦斯瓦尼等 (Vaswani et al. ) 终结了主流NLP中循环论文.

- [Bahdanau, Cho, Bengio (2014). Neural MT by Jointly Learning to Align and Translate](https://arxiv.org/abs/1409.0473)在一个RNN上着注意力.
  注意力出生的地方,附加在RNN上.

- [Hochreiter, Schmidhuber (1997). Long Short-Term Memory](https://www.bioinf.jku.at/publications/older/2604.pdf)原始的LSTM纸,为了记录.
  霍克莱特,施密德布尔 (Schmidhuber) 1997年

- [Gu, Dao (2023). Mamba: Linear-Time Sequence Modeling with Selective State Spaces](https://arxiv.org/abs/2312.00752)现代回复式答案变压器.
  ,道 (,道)  变压器的现代循环替代方案

> **【拓展："Attention Is All You Need" 的历史影响】**瓦斯瓦尼等 2017年的论文不仅解决了RNN的并行化问题,还引发了一场范式革命──从BERT(2018年到GPT-4(2023年),从ViT(2020年到AlphaFold 2(2021年),变革架构已成为现代人工智能的基础模块──它证明了"弱归纳偏好+大数据+大算力"可以超越精心设计的领域特定架构──
