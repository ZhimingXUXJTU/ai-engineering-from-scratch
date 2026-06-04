# Attention Variants — Sliding Window, Sparse, Differential | 注意力变体 — 滑动窗口、稀疏、差分注意力

> 完整注意力是一个圆。每个 token 看到每个 token，内存付出代价。四种变体弯曲圆的形状，收回一半成本。

> **【中文解读】** 标准注意力的 O(n^2) 复杂度太昂贵。滑动窗口注意力(Mistral)、稀疏注意力、差分注意力是降低复杂度的方法。

**类型：** 构建
**语言：** Python
**前置条件：** 阶段 7 · 02（自注意力），阶段 7 · 03（多头注意力），阶段 7 · 12（KV Cache / Flash Attention）
**时长：** 约 60 分钟

## 问题引入

完整注意力在序列长度上花费 `O(N²)` 内存和 `O(N²)` 计算。对于 128K 上下文的 Llama 3 70B，那是每层 160 亿个注意力条目，乘以 80 层。Flash Attention（第 12 课）隐藏了 `O(N²)` 的激活内存但不改变算术成本——每个 token 仍然关注每个其他 token。

三类变体改变了注意力矩阵本身的拓扑结构：

1. **滑动窗口注意力 (SWA)。** 每个 token 关注固定窗口的邻居，而非完整前缀。内存和计算降到 `O(N · W)`，其中 `W` 是窗口大小。Gemma 2/3，Mistral 7B 的前几层，Phi-3-Long。
2. **稀疏 / 块注意力。** 只有选定的对 `(i, j)` 被评分；其余被迫为零权重。Longformer、BigBird、OpenAI 稀疏 Transformer。
3. **差分注意力。** 用独立的 Q/K 投影计算两个注意力图，用一个减去另一个。消除将权重泄漏到前几个 token 的"注意力汇聚"。Microsoft 的 DIFF Transformer（2024）。

这些共存。2026 年的前沿模型通常混合使用：大多数层是 SWA-1024，每五层是全局完整注意力，少数是清理检索的差分头。Gemma 3 的 5:1 SWA 与全局比例是当前的教科书默认。

> **【中文解读】** 三种降低注意力复杂度的方法：(1) 滑动窗口（SWA）——只关注局部邻域，O(N*W) 复杂度；(2) 稀疏/块注意力——只计算选定的 token 对；(3) 差分注意力——两组 Q/K 注意力相减，消除"注意力汇聚"现象。2026 年的模型通常混合使用这些变体。

## 核心概念

### 滑动窗口注意力 (SWA)

位置 `i` 的每个查询只关注 `[i - W, i]`（因果 SWA）或 `[i - W/2, i + W/2]``（双向）范围内的位置。窗口外的 token 在分数矩阵中获得 `-inf`。

```
完整因果：           滑动窗口（W=4）：
位置 0-7             位置 0-7, W=4
    0 1 2 3 4 5 6 7       0 1 2 3 4 5 6 7
0 | x                 0 |  x
1 | x x               1 |  x x
2 | x x x             2 |  x x x
3 | x x x x           3 |  x x x x
4 | x x x x x         4 |    x x x x
5 | x x x x x x       5 |      x x x x
6 | x x x x x x x     6 |        x x x x
7 | x x x x x x x x   7 |          x x x x
```

对于 `N = 8192` 和 `W = 1024`，分数矩阵有 1024 × 8192 个非零行——8 倍缩减。

**KV 缓存随 SWA 缩小。** 每层只需保留最后 `W` 个 token 的 K 和 V。对于 Gemma-3 风格配置（1024 窗口，128K 上下文），KV 缓存减少 128 倍。

**质量代价。** 纯 SWA Transformer 在长程检索上挣扎。修复：交替 SWA 层与全注意力层。Gemma 3 使用 5:1 SWA:全局。Mistral 7B 使用因果 SWA 堆叠，信息通过重叠窗口"向前流动"——每层将有效感受野扩展 `W`，`L` 层后模型可以关注 `L × W` 个之前的 token。

### 稀疏 / 块注意力

预先选择一个 `N × N` 的稀疏模式。三种规范形状：

- **局部 + 步幅（OpenAI 稀疏 Transformer）。** 关注最后 `W` 个 token 加上之前每隔 `stride` 个 token。以 `O(N · sqrt(N))` 计算捕获局部和长程。
- **Longformer / BigBird。** 局部窗口 + 一小组全局 token（例如 `[CLS]`），它们关注所有人也被所有人关注 + 随机稀疏链接。匹配质量下 2 倍上下文。
- **原生稀疏注意力（DeepSeek，2025）。** 学习哪些 `(Q, K)` 块重要；在内核级跳过零块。FlashAttention 兼容。

稀疏注意力是一个内核工程故事。数学很简单（掩码分数矩阵）；收益来自从不将零条目加载到 SRAM。FlashAttention-3 和 2026 年的 FlexAttention API 使自定义稀疏模式成为 PyTorch 中的一等公民。

> **【拓展：滑动窗口的信息传递机制】** 滑动窗口注意力看似只能捕获局部信息，但通过多层堆叠，信息可以"渗透"到更远的位置。W 窗口的 L 层注意力，有效感受野为 L×W。例如 W=1024、L=32 的模型有效感受野为 32K token。Mistral 7B 正是利用了这个特性在保持 O(N*W) 计算复杂度的同时实现长上下文建模。

### 差分注意力（DIFF Transformer，2024）

常规注意力有"注意力汇聚"问题：softmax 强制每行总和为 1，所以不想特别关注任何东西的 token 将权重倾倒到第一个 token（或前几个）。这窃取了本应流向真实内容的容量。

差分注意力通过计算**两个**注意力图并相减来修复：

```
A1 = softmax(Q1 K1^T / √d)
A2 = softmax(Q2 K2^T / √d)
DiffAttn = (A1 - λ · A2) V
```

其中 `λ` 是学习的标量（通常 0.5-0.8）。A1 捕获真实内容权重；A2 捕获汇聚。减法消除汇聚，将权重重新分配给相关 token。

报告结果（Microsoft 2024）：困惑度降低 5-10%，相同训练长度下有效上下文 1.5-2 倍更长，needle-in-haystack 检索更锐利。

> **【中文解读】** 差分注意力的创新之处：标准注意力因 softmax 归一化导致"注意力汇聚"（attention sink）——不相关的 token 把权重集中在序列开头的 token 上。差分注意力计算两组注意力并相减，A1 捕获真实内容权重，A2 捕获汇聚噪声，相减后消除汇聚现象。困惑度降低 5-10%。

> **【拓展：Gemma 3 的混合注意力策略】** Google 的 Gemma 3 使用 5:1 的滑动窗口与全局注意力比例——每 5 层局部注意力后接 1 层全局注意力。这既保持了长上下文的建模能力（全局层提供远程连接），又大幅降低了计算成本（局部层只有 O(N*W) 复杂度）。这种混合策略已成为 2026 年长上下文模型的标准范式。

### 变体比较

| 变体 | 计算 | KV 缓存 | vs 完整注意力的质量 | 生产使用 |
|------|------|---------|-------------------|---------|
| 完整注意力 | O(N²) | 每层 O(N) | 基线 | 每个模型的默认层 |
| SWA（窗口 1024） | O(N·W) | 每层 O(W) | -0.1 困惑度，配合全局层良好 | Gemma 2/3, Phi-3-Long |
| 局部 + 步幅稀疏 | O(N·√N) | 混合 | 类似 SWA | OpenAI 稀疏 Transformer, Longformer |
| BigBird（局部 + 全局 + 随机） | 近似 O(N) | 混合 | 2 倍上下文下匹配完整 | 早期长上下文 BERT |
| 原生稀疏（DeepSeek-V3.2） | O(N · 活跃比例) | O(N) | 0.05 困惑度以内 | DeepSeek-V3.2, 2025 |
| 差分 | O(2·N²) | O(2N) | -5 到 -10% 困惑度 | DIFF Transformer, 2026 年早期模型 |

## 动手实现

参见 `code/main.py`。我们实现一个因果掩码比较器，在玩具序列上并排展示完整、SWA、局部+步幅和差分注意力。

### 步骤 1：完整因果掩码（基线）

```python
def causal_mask(n):
    return [[0.0 if j <= i else float("-inf") for j in range(n)] for i in range(n)]
```

第 07 课的基线。下三角；对角线上方零权重。

### 步骤 2：滑动窗口因果掩码

```python
def swa_mask(n, window):
    M = [[float("-inf")] * n for _ in range(n)]
    for i in range(n):
        lo = max(0, i - window + 1)
        for j in range(lo, i + 1):
            M[i][j] = 0.0
    return M
```

一个参数——`window`。对于 `window >= n`，你恢复完整因果注意力。对于 `window = 1`，每个 token 只关注自身。

### 步骤 3：局部 + 步幅稀疏掩码

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

密集局部窗口加上每隔 `stride` 个 token 回到序列开头。感受野随额外层以对数步增长。

### 步骤 4：差分注意力

```python
def diff_attention(Q1, K1, Q2, K2, V, lam):
    A1 = softmax_causal(Q1 @ K1.T / sqrt_d)
    A2 = softmax_causal(Q2 @ K2.T / sqrt_d)
    return (A1 - lam * A2) @ V
```

两次注意力计算，用学习的混合系数相减。在代码中，我们比较单个与差分的注意力汇聚热力图，观察汇聚的消退。

### 步骤 5：KV 缓存大小

打印每个变体在 `N = 131072` 时每层的缓存大小。SWA 和稀疏变体减少 10-100 倍。差分翻倍。有意识地支付你的内存账单。

## 用框架实现

2026 年生产模式：

```python
from transformers import AutoModelForCausalLM
# Gemma 3 以 5:1 混合 SWA（窗口=1024）和全局层。
model = AutoModelForCausalLM.from_pretrained("google/gemma-3-27b-it")
# print(model.config.sliding_window, model.config.layer_types)
```

PyTorch 2.5+ 中的 FlexAttention 接受掩码函数：

```python
from torch.nn.attention.flex_attention import flex_attention, create_block_mask

def swa_pattern(b, h, q_idx, kv_idx):
    return (q_idx - kv_idx < 1024) & (q_idx >= kv_idx)

mask = create_block_mask(swa_pattern, B=batch, H=heads, Q_LEN=n, KV_LEN=n)
out = flex_attention(q, k, v, block_mask=mask)
```

这编译为自定义 Triton 内核。常见模式下在 FlashAttention-3 速度的 10% 以内，掩码函数是一个 Python 可调用对象。

**何时选择每种：**

- **纯完整注意力** —— 每层至约 16K 上下文，或检索质量至关重要时。
- **SWA + 全局混合** —— 长上下文（>32K），训练和推理受内存限制。2026 年 32K 以上的默认。
- **稀疏块注意力** —— 自定义内核，自定义模式。保留给专门工作负载（检索、音频）。
- **差分注意力** —— 注意力汇聚污染有影响的任何工作负载（长上下文 RAG、needle-in-haystack）。

## 产出物

参见 `outputs/skill-attention-variant-picker.md`。该技能为新模型选择注意力拓扑，给定目标上下文长度、检索需求和训练/推理计算概况。

## 练习题

1. **简单。** 运行 `code/main.py`。验证 `window=4` 的 SWA 将每行最后 4 个 token 之外的所有位置归零。验证 `window=n` 位相同地复现完整因果注意力。
2. **中等。** 在第 07 课毕业项目之上实现 `window=1024` 的因果 SWA。在 tinyshakespeare 上训练 1,000 步。验证损失与完整注意力相比退化了多少？峰值内存下降了多少？
3. **困难。** 在毕业项目模型中实现 Gemma-3 风格的 5:1 层混合（5 SWA，1 全局）。在匹配参数下比较纯 SWA 和纯全局基线的损失、内存和生成质量。
4. **困难。** 实现每头学习 `λ` 的差分注意力。在合成检索任务（一根针，2,000 个干扰项）上训练。测量与匹配参数的单注意力基线的检索准确率。

## 术语速查表

| 术语 | 人们的说法 | 实际含义 |
|------|-----------|---------|
| 滑动窗口注意力 (SWA) | "局部注意力" | 每个查询关注其最后 `W` 个 token；KV 缓存缩小到 `O(W)`。 |
| 有效感受野 | "模型能看多远" | 在 `L` 层窗口为 `W` 的 SWA 堆叠中，可达 `L × W` 个 token。 |
| Longformer / BigBird | "局部 + 全局 + 随机" | 带少量始终关注的全局 token 的稀疏模式；早期长上下文方法。 |
| 原生稀疏注意力 | "DeepSeek 的内核技巧" | 学习块级稀疏性；在内核级跳过零块同时保持质量。 |
| 差分注意力 | "两个图，一个减去另一个" | DIFF Transformer：从第一个减去学习 `λ` 乘以第二个注意力图来消除注意力汇聚。 |
| 注意力汇聚 | "权重泄漏到 token 0" | Softmax 归一化强制行总和为 1；无信息的查询将权重倾倒到位置 0。 |
| FlexAttention | "掩码即 Python" | PyTorch 2.5+ API，将任意掩码函数编译为 FlashAttention 形状的内核。 |
| 层类型混合 | "5:1 SWA 与全局" | 在堆叠中交替稀疏和完整注意力层以在更低内存下保持质量。 |

## 延伸阅读

- [Beltagy, Peters, Cohan（2020）。Longformer: The Long-Document Transformer](https://arxiv.org/abs/2004.05150) —— 规范的滑动窗口 + 全局 token 论文。
- [Zaheer 等人（2020）。Big Bird: Transformers for Longer Sequences](https://arxiv.org/abs/2007.14062) —— 局部 + 全局 + 随机。
- [Child 等人（2019）。Generating Long Sequences with Sparse Transformers](https://arxiv.org/abs/1904.10509) —— OpenAI 的局部+步幅模式。
- [Gemma Team（2024）。Gemma 2: Improving Open Language Models at a Practical Size](https://arxiv.org/abs/2408.00118) —— 1:1 SWA:全局混合。
- [Gemma Team（2025）。Gemma 3 technical report](https://arxiv.org/abs/2503.19786) —— 现在是教科书默认的窗口=1024 的 5:1 混合。
- [Ye 等人（2024）。Differential Transformer](https://arxiv.org/abs/2410.05258) —— DIFF Transformer 论文。
- [Yuan 等人（2025）。Native Sparse Attention](https://arxiv.org/abs/2502.11089) —— DeepSeek-V3.2 的学习稀疏性注意力。
- [PyTorch — FlexAttention 博客和文档](https://pytorch.org/blog/flexattention/) —— "用框架实现"部分中掩码即可调用模式的 API 参考。
