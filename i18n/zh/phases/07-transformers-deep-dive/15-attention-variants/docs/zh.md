# 注意力变体 滑动窗口稀疏差分注意力

> 完全的注意力是圆. 每个代币都看到每一个代币,而记忆支付了代价. 四种变体折曲圆形,恢复了成本的一半.

> **【中文解读】**标准注意力 O(n^2) 复杂度太贵――滑动窗口注意力

**Type:** Hands-on | **类型:** 动手
**Language:**子**语言:**字符串
**Prerequisites:** Phase 7 · 02 (Self-Attention), Phase 7 · 03 (Multi-Head), Phase 7 · 12 (KV Cache / Flash Attention) | **前置知识:** Phase 7 · 02 (Self-Attention), Phase 7 · 03 (Multi-Head), Phase 7 · 12 (KV Cache / Flash Attention)
**Time:** ~60 minutes | **时间:** ~60 分钟

## 问题 问题引入

完全注意力成本`O(N²)`记忆力和`O(N²)`对于一个128K文本的Llama 3 70B,这就是每层16亿注意力输入,乘以80层.闪光注意力 (课 12) 隐藏了`O(N²)`激活存储器,但不会改变算术成本 每个代币仍然会关注其他代币.

> 总的关注的是序列长度的内存和计算成本.`O(N²)`对于 128K 上下文的Llama 3 70B,那是每层160亿个注意条,乘以80层.`O(N²)`动态内存,但不改变算术成本每个代币 仍然关注每个其他代币.

三类变体改变了注意力矩阵本身的拓学:

> 三类变体改变了注意力矩阵本身的拓结构:

1. **Sliding window attention (SWA).**每个代币都会在一个固定的邻居窗口中,而不是完整的预सर्ग.`O(N · W)`在哪里`W`马2/3,米斯特拉尔7B的第一层,菲-3-龙.
   翻译: 中文**滑动窗口注意力 (SWA)。**每个代币只关注固定窗口的邻域,而不是完整的前──内存和计算降至`O(N · W)`在其中`W`是窗户大小──Gemma 2/3──Mistral 7B的前几层──Phi-3-Long──
2. **Sparse / block attention.**只有选择的对`(i, j)`长,大鸟,开AI稀疏变压器.
   翻译: 中文**稀疏/块注意力。**只有选择`(i, j)`对于被评分;其余被迫为零权重.
3. **Differential attention.**计算两个注意力地图,使用不同的Q/K投影,减去一个.杀死"注意力沉浸器",使重量流入第一几个代币.微软的DIFF变压器 (2024).
   翻译: 中文**差分注意力。**通过独立的Q/K 投影计算两个注意力图,将一个从另一个中减去――消除将权重汇聚到前几个代币的"注意力汇聚"现象――微软的DIFF变压器(2024)。

它们共存.2026年边界模型经常混合它们:大多数层都是SWA-1024,每五层都是全球全关注,少数是分区头,清理检索.Gemma3的5:1 SWA-to-global ratio是当前的教科书默认.

> 它们可以共存. 2026年前沿模型通常使用混合:大多数层是SWA-1024,每五层是全局全注意力,少数是清理检索的差分头.

> **【中文解读】**三种降低注意力复杂度的方法: 1) 滑窗口(SWA) 只关注局部邻域, O(N*W) 复杂性; 2) 稀疏/块注意力只计算选定的代币对; 3) 差分注意力两组 Q/K 注意力相减,消除"注意力汇聚"现象──2026年模型通常混合使用这些变体──

## 概念的核心概念

### 滑动窗口注意 (SWA)

每个查询在位置`i`仅在职位`[i - W, i]`(因果性SWA) 或`[i - W/2, i + W/2]`窗外的代币得到了`-inf`在分数矩阵中.

> 位置`i`关注每一个查询`[i - W, i]`没有任何其他方法.`[i - W/2, i + W/2]`在分数矩阵中获得的窗户外的标志`-inf`,我知道.

```
full causal:           sliding window (W=4):
positions 0-7          positions 0-7, W=4
    0 1 2 3 4 5 6 7        0 1 2 3 4 5 6 7
0 | x                0 |  x
1 | x x              1 |  x x
2 | x x x            2 |  x x x
3 | x x x x          3 |  x x x x
4 | x x x x x        4 |    x x x x
5 | x x x x x x      5 |      x x x x
6 | x x x x x x x    6 |        x x x x
7 | x x x x x x x x  7 |          x x x x
```

为了`N = 8192`其他`W = 1024`预期的数值矩阵有1024 × 8192个非零行  8 × 减少.

> 对于`N = 8192`和 `W = 1024`预期1024 × 8192个非零行数量减少了8倍.

**KV cache shrinks with SWA.**只有最后一个`W`对于Gemma-3ish配置 (1024窗口, 128K文本),KV缓存量下降 128x.

> **KV 缓存随 SWA 缩小。**每层只需要保留K和V的最后.`W`个标志──对于类型宝石-3的配置(1024 窗口,128K 上下文),KV 缓存减少 128 倍──

**Quality cost.**仅使用SWA的变压器与远程检索斗争.解决方案:将SWA层与全注意层交换.Gemma 3使用 5:1 SWA:全球.Mistral 7B使用了因果性SWA堆,信息通过重叠窗户"向前流动".`W`在此之后`L`模型可以参加的层次`L × W`返回代币.

> **质量代价。**纯SWA变压器在长距离检索上表现不佳――修复方案:将SWA层与全注意层交换使用――Gemma 3 使用 5:1 的SWA:全局比例――Mistral 7B 使用因果SWA 堆,信息通过重叠窗口"向前流动"每层将有效感受野扩展`W`没有任何`L`层后模型可以追溯`L × W`个标志.

### 缩/阻注意力

选择一个`N × N`率模式是提前的.

> 预先选择`N × N`稀疏模式──三种经典形状:

- **Local + strided (OpenAI sparse transformer).**待在最后一个`W`代币加上每一个`stride`捕捉了当地和远程的`O(N · sqrt(N))`计算.
  翻译: 中文**局部 + 步进（OpenAI 稀疏 Transformer）。**关注最后`W`个标志加上之前每隔`stride`个标志.`O(N · sqrt(N))`计算量同时捕获局部和长距离信息.
- **Longformer / BigBird.**局部窗口+一个小组全球代币 (例如 `[CLS]`) 随时随时随时随时随时随时随时随时随时随时随时随时随时随时随时随时随时随时随时随时随时随时随时随时随时随时随时随时随时随时随时随时随时随时随时随时随时随时随时随时随时随时随时随时随时随时随时随时随时随时随时随时随时随时随时随时随时随时随时随时随时随时随时随时随时随时随时随时随时随时随时随时随时随时随时随时随时随时随时随时随时随时随时随时随时随时随时随时随时随时随时随时随时随时随时随时随时随时随时随时随时随时随时随时随时随时随时随时随时随时随时随时随时随时随时随时随时随时随时随时随时随时随时随的随时随时随时随时随的随时随时随时随的随时随时随时随时随的随时随时随时随的随时随时随的随时随的随时随的随时随时随的随时随的随时随的随时随的随的随时随的随的随时随的随的随的随时随时随的随的随的随的随的随的随的随的随的随的随的随的随的随的随的随的随的随的随的随的随的随的随的.
  翻译: 中文**Longformer / BigBird。**局部窗口 + 少量全局标志(如 `[CLS]`) 与所有代币 双向关注 + 随机稀疏连接――实验表明在相同质量下下文扩大了2倍――
- **Native Sparse Attention (DeepSeek, 2025).**了解哪些区块的`(Q, K)`核层面的零块,可以兼容FlashAttention.
  翻译: 中文**原生稀疏注意力（DeepSeek，2025）。**学习哪些 `(Q, K)`块重要;在内核级别跳过零块──与FlashAttention兼容──

稀疏注意是一个核工程故事.数学很简单 (掩盖分数矩阵);获胜来自从未将零条目加载到SRAM中.FlashAttention-3和2026 FlexAttention API在 PyTorch中实现了自定义稀疏模式的第一类.

> 稀疏注意力是一个内核工程的故事――数学很简单――从不将零条目加载到SRAM――优势来自FlashAttention-3和2026年的FlexAttention API 使自己定义稀疏模式在 PyTorch成为一等公民――

> **【拓展：滑动窗口的信息传递机制】**滑窗注意力看似只能捕获局部信息,但通过多层堆积,信息可以"透透"到更远的位置.

### 变化注意 (DIFF变压器, 2024)

定期关注有一个"注意力沉没"问题:软max强迫每一行总和到1,所以不想关注任何特定的代币在第一个代币 (或第一几个) 上掉了重量. 这就会窃取应该进入真实内容的容量.

> 标准注意力有"注意力汇聚"问题:软max 强制每行总和为 1,所以不想关注任何特定内容的代币会重量倾倒到第一个代币 (或前几个) .

差异性注意力通过计算来解决这个问题**two**关注地图和减值:

> 差分注意力通过计算**两个**注意力图并相减来修复这个问题:

```
A1 = softmax(Q1 K1^T / √d)
A2 = softmax(Q2 K2^T / √d)
DiffAttn = (A1 - λ · A2) V
```

在哪里`λ`取取取取取取取取取取取取取取取取取取取取取取取取取取取取取取取取取取取取取取取取取取取取取取取取取取取取取取取取取取取取取取取取取取取取取取取取取取取取取取取取取取取取取取取取取取取取取取取取取取取取取取取取取取取取取取取取取取取取取取取取取取取取取取取取取取取取取取取取取取取取取取取取取取取取取取取取取取取取取取取取取取取取取取取取取取取取取取取取取取取取取取取取取取取取取取取取取取取取取取取取取取取取取取取取取取取取取取取取取取取取取取取取取取取取取取取取取取取取取取取取取取取取取取取取取取取取取取取取取取取取取取取取取取取取取取取取取取取取取取取取取取取取取取取取取取取取取取取取取取取取取取取取取取取取取取取取取取取取取取取取取取取取取取取取取取取取取取取取取取取取取取取取取取取取取取取取取取取取取取取取取取取取取取取取取取取取取取取取取取取取取取取取取取取取取取取取取取取取取取取取取取取取取取取取取取取取取取取取取取取取取取取取取取取取取取取取取取取取取取取取取取取取取取取取取取取取取取取取取取取取取取取取取取取取取取取取取取取取取取取取取取取取取取取取取取取取取取取取取取取取取取取取取取取取

> 其中`λ`是一个学习到的标量(通常是0.5-0.8)。A1 捕获真实内容权重;A2 捕获汇聚――相减消除汇聚,将权重重新分配给相关代币――

报告结果 (微软 2024): 510%较低的困惑,在相同的训练长度下效果较长的环境 1.52x,针在子中更敏的检索.

> 报告结果(微软2024:困惑度降低5-10%,同样的训练长度下有效上下文长度增加1.5-2倍,针头在草中检索更精确――

> **【中文解读】**差分注意力创新之处:标准注意力因软max 归结导致"注意力汇聚" (注意力沉没) 不相关的代币 把重量集中在序列开头的代币上下.差分注意力计算两组注意力并相减,A1 捕获真实内容重量,A2 捕获汇聚噪音,相减后消除汇聚现象──困惑度降低5-10%.──

> **【拓展：Gemma 3 的混合注意力策略】**谷歌的Gemma 3 使用 5:1的滑动窗口与全局注意力比例每5层的局部注意力后1层的局部注意力.这既保持了长上下文的建模能力,也大幅降低了计算成本.

### 变量比较

| Variant | Compute | KV cache | Quality vs full | Production use |
|---------|---------|----------|-----------------|----------------|
| 变体 | 计算量 | KV 缓存 | 相对全注意力的质量 | 生产使用 |
| Full attention | O(N²) | O(N) per layer | baseline | every model's default layer |
| 全注意力 | O(N²) | 每层 O(N) | 基线 | 每个模型的默认层 |
| SWA (window 1024) | O(N·W) | O(W) per layer | -0.1 ppl, good with global layers | Gemma 2/3, Phi-3-Long |
| 滑动窗口 (窗口 1024) | O(N·W) | 每层 O(W) | -0.1 ppl，配合全局层效果好 | Gemma 2/3, Phi-3-Long |
| Local + strided sparse | O(N·√N) | mixed | similar to SWA | OpenAI sparse transformer, Longformer |
| 局部+步进稀疏 | O(N·√N) | 混合 | 类似 SWA | OpenAI 稀疏 Transformer, Longformer |
| BigBird (local + global + random) | O(N) approx | mixed | matches full at 2× context | early long-context BERT |
| BigBird (局部+全局+随机) | O(N) 近似 | 混合 | 2 倍上下文下匹配全注意力 | 早期长上下文 BERT |
| Native Sparse (DeepSeek-V3.2) | O(N · active fraction) | O(N) | within 0.05 ppl | DeepSeek-V3.2, 2025 |
| 原生稀疏 (DeepSeek-V3.2) | O(N · 活跃比例) | O(N) | 0.05 ppl 以内 | DeepSeek-V3.2, 2025 |
| Differential | O(2·N²) | O(2N) | -5 to -10% ppl | DIFF Transformer, early 2026 models |
| 差分 | O(2·N²) | O(2N) | 困惑度降低 5-10% | DIFF Transformer, 2026 早期模型 |

## 建立它,实现它.
```figure
gqa-kv-sharing
```

## 建立它

看到`code/main.py`我们实施了一个因果化面具比较器,显示一个玩具序列的全,SWA,本地+步骤,和差别注意力.

> 参见`code/main.py` 我们实现了一个因果掩盖比较器,在玩具序列上并排展示全注意力,SWA,局部+步进和差分注意力.

### 步骤1:完整的因果性面具 (基线)

```python
def causal_mask(n):
    return [[0.0 if j <= i else float("-inf") for j in range(n)] for i in range(n)]
```

从第七课开始的基线.

> 第七课的基线――下三角;对角线上权重为零――

### 步骤2:滑窗因果化面具

```python
def swa_mask(n, window):
    M = [[float("-inf")] * n for _ in range(n)]
    for i in range(n):
        lo = max(0, i - window + 1)
        for j in range(lo, i + 1):
            M[i][j] = 0.0
    return M
```

一个参数`window`为了`window >= n`由于你已经开始恢复了完全的因果性注意力.`window = 1`每个代币只能为自己提供服务.

> 一个参数`window`,当`window >= n`时,恢复为全因果注意力.`window = 1`时,每个代币只关注自己.

### 步骤3:局部+步骤稀疏面具

```python
def strided_mask(n, window, stride):
    M = [[float("-inf")] * n for _ in range(n)]
    for i in range(n):
        lo = max(0, i - window + 1)
        for j in range(lo, i + 1):
            M[i][j] = 0.0
        for j in range(0, i + 1, stride):
            M[i][j] = 0.0
    return M
```

密集的地方窗户加上每一个`stride`接收场在日志步骤增加了额外的层次.

> 密集局部窗户加上从序列开启到每隔`stride`个标志――感受随着数量增长而增长.

### 步骤4: 差异性注意

```python
def diff_attention(Q1, K1, Q2, K2, V, lam):
    A1 = softmax_causal(Q1 @ K1.T / sqrt_d)
    A2 = softmax_causal(Q2 @ K2.T / sqrt_d)
    return (A1 - lam * A2) @ V
```

在代码中,我们比较单对差的注意力-沉热地图,看着洗崩.

> 两次注意力计算,使用学习的混合系数相减. 在代码中,我们比较单次注意力和差别注意力的汇聚热图,观察汇聚现象的消除.

### 步骤5: KV缓存尺寸

按每层打印缓存尺寸`N = 131072`对于每个变体.SWA和稀有变体下降了10100×. 差异性双倍. 意识地支付你的内存账单.

> 打印`N = 131072`时每种变体的缓存量大小──SWA 和稀疏变体减少10-100倍──差分变体翻倍──要意识地管理你的内存开销──

## 用它实现框架

2026年生产模式:

> 2026年生产模式:

```python
from transformers import AutoModelForCausalLM
# Gemma 3 mixes SWA (window=1024) and global layers at 5:1.
model = AutoModelForCausalLM.from_pretrained("google/gemma-3-27b-it")
# print(model.config.sliding_window, model.config.layer_types)
```

在 PyTorch 2.5+ 中,FlexAttention 接受一个面具功能:

> PyTorch 2.5+ 中的FlexAttention 接受掩码函数:

```python
from torch.nn.attention.flex_attention import flex_attention, create_block_mask

def swa_pattern(b, h, q_idx, kv_idx):
    return (q_idx - kv_idx < 1024) & (q_idx >= kv_idx)

mask = create_block_mask(swa_pattern, B=batch, H=heads, Q_LEN=n, KV_LEN=n)
out = flex_attention(q, k, v, block_mask=mask)
```

这将编译成一个定制的Triton内核.在普通模式的FlashAttention-3速度的10%内,面具函数是Python调用.

> 这将编译为自定义Triton内核.对于常见模式,速度在FlashAttention-3的10%内,并且掩码函数是一个Python可调用对象.

**When to pick each:**

> **何时选择每种变体：**

- **Pure full attention**每层到16K的文本,或者检索质量至关重要时.
  翻译: 中文**纯全注意力** 每层都用到约16K 上下文,或检查质量至关重要场景.
- **SWA + global mix**长文本 (>32K),训练和推断内存. 2026年默认超过32K.
  翻译: 中文**SWA + 全局混合**长上下文(>32K),训练和推理受内存约束──32K以上的2026年默认配置──
- **Sparse block attention**定制内核,定制模式. 专用工作负载 (检索,音频) 预留.
  翻译: 中文**稀疏块注意力**自定义内核,自定义模式――专用于特殊工作负载(检索、音频) 』
- **Differential attention**任何注意力污染造成伤害的工作负载 (长文本RAG,子子子).
  翻译: 中文**差分注意力** 注意力汇聚污染有害的任何工作负载

## 运送它.

看到`outputs/skill-attention-variant-picker.md`技能选择一个针对新模型的注意力拓,因为目标背景长度,检索要求和训练/推理计算配置.

> 参见`outputs/skill-attention-variant-picker.md`△根据目标下文长度,检查需求和训练/推理计算配置,为新模型选择注意力拓──

## 练习题

1. **Easy.**跑步`code/main.py`检查SWA`window=4`检查查,每行最后4个代币以外的所有东西都是零的.`window=n`完全因果注意力的重复比特相同.
   中文翻译:运行 `code/main.py`验证`window=4`通过SWA将每行最后4个代币外的所有内容置零.`window=n`能逐位复现全因果注意力――
2. **Medium.**执行因果性SWA`window=1024`训练1000步小小, 什么值减值与全注意力?
   中文翻译:在第07课毕业项目上实现`window=1024`由于SWA. 在小小的Shakespeare上训练1000步.验证损失比全注意力回归多少?峰值内存降低多少?
3. **Hard.**在顶点模型中实现Gemma-3式 5:1层混合 (5 SWA, 1 全球).在匹配参数时,对纯SWA和纯全球基线进行损失,内存和生成质量进行比较.
   中文翻译:在毕业项目模型中实现类宝石-3的5层混合,5层SWA、1层全局) ・在匹配参数下与纯SWA和纯全局基线相比损失、内存和生成质量。
4. **Hard.**通过学习的学习者来实现分别注意力`λ`按头.训练一个合成检索任务 (一个针,2000个分心器).在匹配的参数上测量检索精度与单次注意的基线.
   中文翻译:实现每个头有学习`λ`分注意力. 在合成检查任务 (针,2000个干扰项) 上练习.

## 关键词 快速查找表

| Term | What people say | What it actually means |
|------|-----------------|-----------------------|
| 术语 | 通俗说法 | 实际含义 |
| Sliding window attention (SWA) | "Local attention" | Each query attends to its last `W` tokens; KV cache shrinks to `O(W)`. |
| 滑动窗口注意力 (SWA) | "局部注意力" | 每个查询关注其最后 `W` 个 token；KV 缓存缩小到 `O(W)`。 |
| Effective receptive field | "How far back the model sees" | In an `L`-layer SWA stack with window `W`, up to `L × W` tokens. |
| 有效感受野 | "模型能看多远" | 在 `L` 层 SWA 堆栈中，窗口 `W`，最多 `L × W` 个 token。 |
| Longformer / BigBird | "Local + global + random" | Sparse patterns with a few always-attending global tokens; early long-context approach. |
| Longformer / BigBird | "局部+全局+随机" | 带少量始终关注的全局 token 的稀疏模式；早期长上下文方案。 |
| Native Sparse Attention | "DeepSeek's kernel trick" | Learn block-level sparsity; skip zero blocks at the kernel level while keeping quality. |
| 原生稀疏注意力 | "DeepSeek 的内核技巧" | 学习块级稀疏性；在内核级别跳过零块同时保持质量。 |
| Differential attention | "Two maps, one subtracts" | DIFF Transformer: subtract a learned `λ` times a second attention map from the first to cancel attention sinks. |
| 差分注意力 | "两个图，一个相减" | DIFF Transformer：用第一个注意力图减去学习 `λ` 倍的第二个注意力图，消除注意力汇聚。 |
| Attention sink | "Weight bleeds to token 0" | Softmax normalization forces rows to sum to 1; uninformative queries dump weight on position 0. |
| 注意力汇聚 | "权重流向 token 0" | Softmax 归一化迫使每行总和为 1；无信息查询将权重倾倒到位置 0。 |
| FlexAttention | "Mask-as-Python" | PyTorch 2.5+ API that compiles arbitrary mask functions into FlashAttention-shape kernels. |
| FlexAttention | "掩码即 Python" | PyTorch 2.5+ API，将任意掩码函数编译为 FlashAttention 形式的内核。 |
| Layer type mix | "5:1 SWA-to-global" | Interleave sparse and full attention layers in a stack to keep quality at lower memory. |
| 层类型混合 | "5:1 SWA 与全局" | 在堆栈中交替使用稀疏和全注意力层，以较低内存保持质量。 |

## 继续阅读 继续阅读

- [Beltagy, Peters, Cohan (2020). Longformer: The Long-Document Transformer](https://arxiv.org/abs/2004.05150)可行滑动窗口+全球标志纸.
  中文翻译:长期论文,经典的滑动窗口 + 全局代币方案
- [Zaheer et al. (2020). Big Bird: Transformers for Longer Sequences](https://arxiv.org/abs/2007.14062)本地+全球+随机.
  中文翻译:大鸟论文,局部 + 全局 +随机模式──
- [Child et al. (2019). Generating Long Sequences with Sparse Transformers](https://arxiv.org/abs/1904.10509)OpenAI的本地+步骤模式.
  中文翻译:OpenAI 稀疏变压器论文,局部+步进模式──
- [Gemma Team (2024). Gemma 2: Improving Open Language Models at a Practical Size](https://arxiv.org/abs/2408.00118)全球混合物:1:
  中文翻译:Gemma 2 论文,1:1 SWA 与全局混合──
- [Gemma Team (2025). Gemma 3 technical report](https://arxiv.org/abs/2503.19786)5:1的混合和窗口=1024现在是教科书默认的.
  中文翻译:Gemma 3 技术报告,5:1 混合,窗口=1024,现已成为教科书默认.
- [Ye et al. (2024). Differential Transformer](https://arxiv.org/abs/2410.05258) DIFF变压器纸.
  中文翻译:DIFF变压器
- [Yuan et al. (2025). Native Sparse Attention](https://arxiv.org/abs/2502.11089)深度搜索V3.2的学习度注意力.
  中文翻译:DeepSeek-V3.2 的原生稀疏注意力论文
- [PyTorch — FlexAttention blog and docs](https://pytorch.org/blog/flexattention/)使用它中的面具作为可调用模式的API参考.
  中文翻译:PyTorch FlexAttention 文档,掩码即可调用模式的API参考
