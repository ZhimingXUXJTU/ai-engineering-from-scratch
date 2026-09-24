# 现在,我们在线观看,我们在线观看,我们在线观看,我们在线观看,我们在线观看,我们在线观看,我们在线观看,我们在线观看,我们在线观看,我们在线观看,我们在线观看,我们在线观看,我们在线观看,我们在线观看,我们在线观看,我们在线观看,我们在线观看,我们在线观看,我们在线观看,我们在线观看,我们在线观看,我们在线观看,我们在线观看,我们在线观看,我们在线观看,我们在线观看,我们在线观看,我们在线观看,我们在线观看,我们在线观看,我们在线观看,我们在线观看,我们在线观看,我们在线观看,我们在线观看,我们在线观看,我们在线观看,我们在线观看,我们在线观看,我们在线观看,我们在线观看,我们在线观看,我们在线观看,我们在线观看,我们在线观看,我们在线观看,我们在线观看.

> 在64k代币时,注意力耗费了70到80%的解码延迟. 每个开放模型实验室都有一个解决方案. 密搜索的NSA (ACL 2025最佳论文) 是一个住的:三个平行关注分支压缩的粗粒的代币,选择性保留的细粒的代币,以及用于本地环境的滑窗通过学习门组合. 它是硬件配合 (核友好),可以本地训练 (在预训练中工作,在推断时不插电),在64k解码上,它比FlashAttention更快,同时匹配或超过全注意力质量. 这一课将三个分支构建到底,

> **【中文解读】**64K代币 时注意力消耗 70-80%的解码延迟――DeepSeek NSA(ACL 2025 最佳论文) 使用三条并行注意力分支解决:压缩粗粒度代币、选择保留细粒度代币、滑窗局部上下文,通过可学习门控组合──硬件友好、可预训、比FlashAttention更快──

> **【拓展：稀疏注意力→长上下文】**长上下文(64K-128K代币) 是2025-2026年大模型的核心能力──NSA、MHA、GQA 都是降低注意力计算复杂性的方案──DeepSeek的创新在稀疏性上是端到端可微分的,可以直接在预训练阶段使用──

>  **【前置】**学本节前请先掌握:阶段10·16;;差分注意力);FlashAttention 概念;软max 门控机制――本节是注意力优化进阶――
>  **【类比】**美国国家安全局 (NSA) 进行了三种策略:**压缩分支**              **选择分支**现在,我在看看自己感兴趣的章节.**滑动窗口**现在的位置是什么? 现在的位置是什么?

**Type:** Build
**Languages:** Python (stdlib)
**Prerequisites:** Phase 7 · 12 (KV cache, flash-attention), Phase 7 · 15 (attention variants), Phase 10 · 16 (differential attention)
**Time:** ~60 minutes

## 学习目标

- 告诉我们, NSA 的三个关注部门,
  解释 NSA 的三条注意力分支及其各自捕获的信息
- 解释为什么 NSA 是"本地训练的",而以前的稀疏注意力方法仅仅是推断的.
  解释为什么 NSA 是"原生训练的",而之前的稀疏注意力方法只能用于推
- 计算NSA的注意力计算节省率与64k文本中的全注意力,作为压缩块大小和选择顶-k的函数.
  计算在 64K 上下文中 NSA 相对全注意力计算节省量(作为压缩块大小和选择顶-k的函数)
- 实现在 stdlib Python 中的三分组合在短合成序列上,并验证盖特权重的行为.
  使用 Python 实现短合成序列中的三分支组合,验证门控制权重行为

## 问题 问题引入

完全关注序列长度N成本 `O(N^2)`时间和`O(N)`根据美国国家安全局 (NSA) 论文的测量理论估计,注意力占64k的总解码延迟的70-80%. 下游所有东西都由注意力成本主导.

> 序列长度 N 的全注意力成本为 `O(N^2)`时间和每层`O(N)`在64k代币中,计算和显存带宽的数字是灾难性的.

很少有人注意, 之前的尝试都被分为两个桶. 固定模式稀缺性 (滑动窗口,步骤,区块本地) 丢弃信息,并失败于远程召回任务. 输入时间稀缺性 (KV缓存切割,H2O,流程LLM) 应用于密集注意力上预先训练的模型,并且只恢复了潜在的加速量的很小一部分,因为模型从未被要求通过稀疏模式路由信息.

> 稀疏注意力是显而易见的答案.之前的尝试分为两类. 固定模式稀疏性 (滑窗,跨步,块局部) 丢弃信息并未能完成长程记忆任务.

产生的稀疏注意 (Yuan et al.,DeepSeek + PKU + UW,ACL 2025最佳论文,arXiv:2502.11089) 是两者:模型在预训练中学习的稀疏性模式,作为一个基于内核的算法实现,实际上在推断时提供了计算节省.

> 原生稀疏注意力(元 等人,DeepSeek + PKU + UW,ACL 2025 最佳论文,arXiv:2502.11089) 两者兼顾:一个模型在预训中学习的稀疏模式,实现内核对齐算法,在推理时真正交付计算节省――两年后,NSA或其直接继承人将是每个前沿长上下文模型的默认注意力――

## 概念的核心概念

> **【中文解读】**原生稀疏注意力 (原生稀疏注意力) 让模型学习哪些位置需要关注,哪些可以跳过.相比密集注意力 (O     ) 复杂性,稀疏注意力将计算量降至O                                                                                                                                                                                                                               

> **【拓展：长上下文的稀疏注意力方案】**稀疏注意力工程实现包括:滑动窗口(Mistral 的 32K 窗口) + 全局代币([CLS]) + 选择性关注──Google 的环注和区块-节省注意力将上下文扩展到百万代币──DeepSeek 的 NSA(Native Sparse Attention) 在训练中直接学习稀疏模式──


### 两的三支

对于每一个查询,NSA三次向KV缓存的三个不同的视图运行注意力:

1. **Compressed branch.**代币分成大小的块`l`通过一个小的学习MLP,每个块被压缩成一个单个总结代币.查询通过这些压缩代币进行,从而获得整个序列的粗粒度视图.

2. **Selected branch.**通过使用压缩分支的注意力分数,确定了对当前查询最相关的顶级k块.这些块的细粒度 (未压缩) 代币被读取,查询会在所有这些块上进行. 想象压缩分支的注意力作为选择的路由信号.

3. **Sliding-window branch.**查询内容包括最新的查询内容.`W`对于本地语境,该分支捕捉到其他两个可能错过的结构重的短距离模式 (语法,本地核心引用).

通过学习的位置通道,三个分支输出组合在一起:

```
out = g_cmp * out_cmp + g_sel * out_sel + g_win * out_win
```

`g_cmp, g_sel, g_win`它们不必总和到1 ,它们可以独立权重分支.

### 为什么这"可以本地训练"

选择步骤 (顶-k块) 是离散的.离散操作打破梯度流量.以前的稀疏注意力工作要么通过选择 (限制训练) 跳过后方,要么使用连续放松,在推断时没有真正的稀疏性.

美国国家安全局忽略了这一点:压缩分支的关注是整个序列上的可分化粗粒度的关注. 压缩分支的最高注意力分数, 才能选择哪些细粒块要加载. 渐变体通过压缩分支分数流 (影响压缩输出和选择逻辑),并且选定的块对最终输出的贡献也可分化. 无区别的`top_k`运算是前进计算图的无运行 它只控制哪些块从内存中加载.

这就是为什么 NSA 可以用于预训练的终端. 该模型学习通过三个分支共同路由信息,产生稀疏的模式,

### 硬件对齐的内核

由于每个查询组看到相同的选定的块 (选择是每个查询组,而不是每个查询头),因此KV负载在整个组中被抵消.算术强度保持高.

该论文报告说,Triton内核在64k解码上运行速度比FlashAttention快9倍,随着序列长度而增长速度.

### 计算预算

让我们`N`连续时间`l`压缩块大小`k`选拔的最高数量,`w`滑窗,`b`选择的块大小 (通常等于`l`)

- 压缩的分支:`O(N/l)`按查询的密钥,所以`O(N * N / l)`总的来说.
- 选择的分支:`O(k * b)`按查询的密钥,所以`O(N * k * b)`现在,我们要去.
- 滑动分支: `O(w)`按查询的密钥,所以`O(N * w)`现在,我们要去.

总数:`O(N * (N/l + k*b + w))`现在,我们要去.

随着`N = 64k, l = 64, k = 16, b = 64, w = 512`:每次查询成本为`1000 + 1024 + 512 = 2536 keys`完全关注`64000 keys`计算减少了25倍.

随着`N = 128k, l = 64, k = 16, b = 64, w = 512`:每次查询成本为`2000 + 1024 + 512 = 3536 keys`完全关注`128000 keys`效益随着序列长度而增长,这是整个观点.

### 如何比较

| Method | Differentiable | Real inference speedup | Long-range recall |
|--------|---------------|----------------------|-------------------|
| Sliding window only | yes | yes | fails |
| Strided / block-sparse | yes | yes | partial |
| KV pruning (H2O, StreamingLLM) | N/A (inference-time) | yes | partial |
| MoBA (Moonshot) | partial | yes | good |
| NSA | yes (natively) | yes (9x at 64k) | matches full attention |

根据MoE原则,MoBA (Moonshot, arXiv:2502.13189) 同时发布,并采用类似的三比一个方法,将MoE原则应用于注意力块.


> **【拓展：稀疏注意力在长上下文中的应用】**密集注意力 O(n^2) 计算量使 128K 上下文的预填充阶段需要约30秒──稀疏方法(如 NSA、环注意力) 将降至可接受范围──Gemini 1.5 Pro 的1M代币 上下文依赖于稀疏注意力──


## 建立它,实现它.
```figure
sliding-window-attention
```

## 建立它

`code/main.py`执行三个分支在短的合成序列上,并显示:

- 压缩MLP (用于教学清晰度使用简单的平均池基线;真正的NSA使用学习MLP).
- 根据压缩分支的分数进行的顶级k区块选择.
- 滑窗的注意力在最后`w`它们是什么?
- 封闭的组合.
- 计算计算的打印,比较于全注意力.

### 步骤1:将代币压缩成块

```python
def compress(K, l):
    n = len(K)
    n_blocks = (n + l - 1) // l
    out = []
    for b in range(n_blocks):
        start, end = b * l, min((b + 1) * l, n)
        block = K[start:end]
        summary = [sum(row[d] for row in block) / len(block) for d in range(len(K[0]))]
        out.append(summary)
    return out
```

### 步骤2:压缩分支注意

运行软max注意力对压缩键.压缩分支分数是双重的信号.

### 步骤3: 选择顶部k块

选择该类型的指数`k`输入原始的未压缩代币,并关注它们.

### 步骤4:滑动窗口注意

接下来拿下最后一个`w`通过电子商务来控制这些代币,并对它们进行标准的注意.

### 步骤5:门 + 组合

查询中的一个小 MLP 产生三个门权重.最终输出是三个分支输出的权重总和.

### 步骤 6:计算计算

打印每一个分支的每个查询中参观的键数量和总数.`N`通过1024代币的合成,`l = 32, k = 4, w = 128`美国国家安全局看到`32 + 128 + 128 = 288`对于全重关注,每次查询的密钥比1024低了3.5倍.

## 用它实现框架

美国国家安全局正在 DeepSeek 的长文本预训练管道中运输.

- **DeepSeek internal**:本土,发表的权重使用NSA或其继任者DSA (Deepseek Sparse Attention).
- **vLLM**: 实验性 NSA 支持开发 DeepSeek-V3.x 重量.
- **SGLang**: NSA 发布的基准;生产路径遵循vLLM.
- **llama.cpp / CPU**核分解的总费用在CPU吞吐量上不值得.

什么时候联系NSA:

- 预训或继续训练运行,针对64k以上的环境,具有严格的计算预算.
- 调查了深度搜索的长文本检查站.

什么时候不:

- 没有持续训练,就不能再调整NSA.
- 经过三支支的开支, 占据了储蓄的地位.
- 批量-1互动聊天, 缓慢解码效益, 但只有在长时间的环境中.

## 运送它.

这一课产生了`outputs/skill-nsa-integrator.md`鉴于长文本预训练运行规格,它产生了NSA集成计划:压缩块大小,顶部k,滑窗,门 MLP宽度,内核选择,以及具体的长文本评估,这将证明建筑变化.

> 本课产出发 `outputs/skill-nsa-integrator.md`△给定长度上下文预训运行规范,它产生了NSA集成计划:压缩块大小,顶-k滑窗,门控MLP宽度,内核选择以及证明架构变得更合理的特定长度下文评估――

## 练习题

1. 跑步`code/main.py`在1024代码的合成器上.`(l, k, w)`在一个子中针的测试中,保持95%的回忆,而完全注意力.
   中文翻译:在1024代币合成数据上运行`code/main.py`在三个预设上扫描`(l, k, w)`并打印计算量――在草测试中保持全注意力 95% 召回率同时实现每查询键计数的最低预设――

2. 替换中积压机用一个小的学习MLP (2层,隐藏32).训练它在一个合成任务,信号是一个块的平均值.测量与中积基线的困惑差距.
   中文翻译:用小型学习MLP(2层,隐藏 32) 替换平均值池化压缩机――在信号为块平均值的合成任务中训练――在保留数据上测量与平均值池化基线的困惑差距――

3. 执行门 MLP. 它将查询作为输入,并输出三个尺度. 显示门行为合理:随机查询几乎均的权重,查询击中远后区块时,选择的分支重量.
   中文翻译:实现门控 MLP──它以查询为输入输出三个标量──展示门控行为合理:随机查询时近似均加权,查询命中远回块时对选分支重量加权──

4. 计算NSA启用70B模型的KV缓存预算在128k语境下.KV头为8,头暗128,BF16.比较全注意和MLA (阶段10 · 14显示MLA的数字).确定NSA的细粒子分支KV缓存等于全注意的序列长度.
   中文翻译:计算 NSA 启动的70B 模型在 128K 上下文 下 KV 缓存内存预算。KV 头 8 个,头维度 128,BF16──与全注意力和 MLA 比较──找到 NSA 细粒度分支 KV 缓存等于全注意力序列长度──

5. 阅读 NSA 论文的第 4 节 (arXiv:2502.11089) 并用三句话解释为什么压缩分支的注意力分数被重复用于顶级选项而不是计算单独的路由分数.
   中文翻译:阅读NSA论文第4节,用三句话解释为什么压缩分支的注意分数被重复用于顶级选择而不是计算单独的路由分数――将答案与梯度流联系起来――

## 关键词 快速查找表

| Term | What people say | What it actually means | 中文释义 |
|------|----------------|------------------------|---------|
| Compressed branch | "Coarse view" | Attention over block-averaged keys that provides global context in O(N/l) keys per query | 压缩分支，块平均键上的注意力 |
| Selected branch | "Top-k blocks" | Fine-grained attention over the `k` blocks with highest compressed-branch scores | 选择分支，对 top-k 块做细粒度注意力 |
| Sliding window | "Local context" | Attention over the last `W` tokens for short-range patterns | 滑动窗口，最近 W 个 token 的局部上下文 |
| Native trainability | "Pre-train with the sparsity on" | The sparsity pattern is learned during pre-training, not bolted on at inference | 原生可训练，预训练时就使用稀疏模式 |
| Compression block size l | "Group size for coarse view" | How many tokens get merged into one summary; 32-64 typical | 压缩块大小，每组合并多少 token |
| Top-k | "Blocks to keep" | Number of compressed blocks whose uncompressed tokens get read; 16 typical | Top-k，保留的压缩块数量 |
| Sliding window W | "Local attention radius" | Typically 512; shorter hurts local coherence, longer wastes compute | 滑动窗口大小，典型值 512 |
| Branch gate | "How to mix the three" | Per-position MLP output that weights the three branches' contributions | 分支门控，MLP 输出加权三分支贡献 |
| Hardware alignment | "Kernel-friendly sparsity" | Sparse pattern chosen so that the actual GPU kernel achieves the theoretical speedup | 硬件对齐，稀疏模式适配 GPU 核函数 |
| DSA | "NSA's successor" | Deepseek Sparse Attention, the architecture that followed NSA in DeepSeek's lineage | DSA，DeepSeek 稀疏注意力，NSA 的后继架构 |

## 继续阅读 继续阅读

- [Yuan et al. — Native Sparse Attention: Hardware-Aligned and Natively Trainable Sparse Attention (arXiv:2502.11089, ACL 2025 Best Paper)](https://arxiv.org/abs/2502.11089)报纸
- [DeepSeek-V3 Technical Report (arXiv:2412.19437)](https://arxiv.org/abs/2412.19437)建筑家族 NSA 目标
- [Moonshot AI — MoBA: Mixture of Block Attention for Long-Context LLMs (arXiv:2502.13189)](https://arxiv.org/abs/2502.13189)同时工作,以MoE风格的关注
- [Beltagy et al. — Longformer: The Long-Document Transformer (arXiv:2004.05150)](https://arxiv.org/abs/2004.05150)滑窗的起源
- [Xiao et al. — StreamingLLM: Efficient Streaming Language Models with Attention Sinks (arXiv:2309.17453)](https://arxiv.org/abs/2309.17453) 推断时间稀缺度基线 NSA改善
- [Dao et al. — FlashAttention-2 (arXiv:2307.08691)](https://arxiv.org/abs/2307.08691)全重视基线NSA核在64k
