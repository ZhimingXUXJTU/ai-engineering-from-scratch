# 注意力机制 — Transformer 的核心突破

> 解码器不再眯眼看压缩摘要，开始查看整个源序列。这之后的一切都是注意力加工程。

> **【中文解读】** 注意力机制让模型关注输入的相关部分。Q/K/V 是核心。

**类型：** 构建
**编程语言：** Python
**前置课程：** Phase 5 · 09（序列到序列模型）
**预计时长：** ~45 分钟

## 问题引入

第 09 课以一个可测量的失败结束。在玩具复制任务上训练的 GRU 编码器-解码器在长度 5 时 89% 准确率，在长度 80 时接近随机。原因是结构性的，不是训练 bug：编码器收集的每一点信息都必须塞进一个固定大小的隐藏状态，解码器看不到其他任何东西。

> **【中文解读】** 本节提出的问题是：如何在实际工程中正确理解和应用这一技术。理解问题背景有助于把握技术选型的关键决策点。在实际 AI 系统中，错误的技术选型往往比实现细节的 bug 代价更高。


Bahdanau、Cho 和 Bengio 在 2014 年发表了一个三行修复。不只给解码器最终编码器状态，而是保留每个编码器状态。在每个解码器步骤，计算编码器状态的加权平均，权重表示 "解码器现在需要多看编码器位置 `i`？" 这个加权平均就是上下文，它在每个解码器步骤都改变。

这就是全部想法。Transformer 扩展了它。自注意力将其应用于单个序列。多头注意力并行运行它。但 2014 年版本已经打破了瓶颈，一旦你有了它，转向 Transformer 就是工程而非概念。

## 核心概念

> **【中文解读】** 本节介绍核心概念和理论基础。掌握这些概念是后续动手实现的前提，同时也是面试和工程实践中高频考察的知识点。


![Bahdanau 注意力：解码器查询所有编码器状态](../assets/attention.svg)

在每个解码器步骤 `t`：

1. 使用前一个解码器隐藏状态 `s_{t-1}` 作为**查询（Query）**。
2. 将它与每个编码器隐藏状态 `h_1, ..., h_T` 打分。每个编码器位置一个标量。
3. 对分数做 softmax 得到注意力权重 `α_{t,1}, ..., α_{t,T}`，总和为 1。
4. 上下文向量 `c_t = Σ α_{t,i} * h_i`。编码器状态的加权平均。
5. 解码器取 `c_t` 加上前一个输出 token，产生下一个 token。

加权平均是关键。当解码器需要将 "Je" 翻译为 "I" 时，它对 "Je" 上的编码器状态权重高，其他低。当需要 "not" 时，它对 "pas" 权重高。上下文向量在每步重塑。

> **【拓展：大语言模型的工程实践】** 从 GPT 到 ChatGPT，NLP 领域经历了从 "每个任务训练一个模型" 到 "一个模型解决所有任务" 的范式转变。在实际工程中，LLM 的部署需要考虑 Token 限制、延迟、成本、安全审查等问题。LangChain、LlamaIndex 等框架简化了 LLM 应用的开发。

> **【拓展：RAG 与企业知识库】** 检索增强生成（RAG）是当前企业 AI 应用最流行的架构：将用户查询先检索相关文档片段，再将检索结果作为上下文喂给 LLM 生成答案。这种方式解决了 LLM 知识过时和幻觉问题。向量数据库（如 Milvus、Pinecone、Weaviate）是 RAG 系统的核心组件。

> **【拓展：NLP 的多语言挑战】** 全球有 7000+ 种语言，但 NLP 研究主要集中在英语等少数语言。跨语言迁移学习、多语言预训练模型（如 mBERT、XLM-R）是解决低资源语言 NLP 的主要方法。字节级模型（如 ByT5）甚至可以在无分词器的情况下处理任何语言。






## 张量形状（每个人都会在这里出错的地方）

这是每个注意力实现第一次出错的地方。慢慢读。

| 对象 | 形状 | 说明 |
|------|------|------|
| 编码器隐藏状态 `H` | `(T_enc, d_h)` | 如果是 BiLSTM，`d_h = 2 * d_hidden` |
| 解码器隐藏状态 `s_{t-1}` | `(d_s,)` | 一个向量 |
| 注意力分数 `e_{t,i}` | 标量 | 每个编码器位置一个 |
| 注意力权重 `α_{t,i}` | 标量 | 对所有 `i` 做 softmax 后 |
| 上下文向量 `c_t` | `(d_h,)` | 与编码器状态相同形状 |

**Bahdanau（加性）分数。** `e_{t,i} = v_α^T * tanh(W_a * s_{t-1} + U_a * h_i)`。

- `s_{t-1}` 形状为 `(d_s,)`，`h_i` 形状为 `(d_h,)`。
- `W_a` 形状为 `(d_attn, d_s)`。`U_a` 形状为 `(d_attn, d_h)`。
- tanh 内部的和形状为 `(d_attn,)`。
- `v_α` 形状为 `(d_attn,)`。与 `v_α` 的内积坍缩为标量。**这就是 `v_α` 的作用。** 它不是魔法。它是将注意力维度向量投影为标量分数的投影。

**Luong（乘性）分数。** 三个变体：

- `dot`：`e_{t,i} = s_t^T * h_i`。要求 `d_s == d_h`。硬约束。如果编码器是双向的则跳过。
- `general`：`e_{t,i} = s_t^T * W * h_i`，`W` 形状为 `(d_s, d_h)`。移除等维约束。
- `concat`：本质上是 Bahdanau 形式。由于前两种更便宜，很少使用。

**一个值得注意的 Bahdanau / Luong 陷阱。** Bahdanau 使用 `s_{t-1}`（生成当前词*之前*的解码器状态）。Luong 使用 `s_t`（*之后*的状态）。混淆它们会产生极其难以调试的微妙错误梯度。选择一篇论文并坚持其约定。

## 动手实现

> **【中文解读】** 本节通过代码从零实现核心算法。这种 "from scratch" 的方式能帮助理解框架背后的原理，遇到问题时不会被黑盒困住。


### 步骤 1：加性（Bahdanau）注意力

```python
import numpy as np


def additive_attention(decoder_state, encoder_states, W_a, U_a, v_a):
    projected_dec = W_a @ decoder_state
    projected_enc = encoder_states @ U_a.T
    combined = np.tanh(projected_enc + projected_dec)
    scores = combined @ v_a
    weights = softmax(scores)
    context = weights @ encoder_states
    return context, weights


def softmax(x):
    x = x - np.max(x)
    e = np.exp(x)
    return e / e.sum()
```

对照上面的表格检查你的形状。`encoder_states` 形状为 `(T_enc, d_h)`。`projected_enc` 形状为 `(T_enc, d_attn)`。`projected_dec` 形状为 `(d_attn,)` 并广播。`combined` 形状为 `(T_enc, d_attn)`。`scores` 形状为 `(T_enc,)`。`weights` 形状为 `(T_enc,)`。`context` 形状为 `(d_h,)`。搞定了。

### 步骤 2：Luong 点积和通用

```python
def dot_attention(decoder_state, encoder_states):
    scores = encoder_states @ decoder_state
    weights = softmax(scores)
    return weights @ encoder_states, weights


def general_attention(decoder_state, encoder_states, W):
    projected = W.T @ decoder_state
    scores = encoder_states @ projected
    weights = softmax(scores)
    return weights @ encoder_states, weights
```

每个三行。这就是 Luong 论文的意义。在大多数任务上相同准确率，代码少得多。

### 步骤 3：一个计算示例

给定三个编码器状态（大致是 "cat"、"sat"、"mat"）和一个与第一个最对齐的解码器状态，注意力分布集中在位置 0。如果解码器状态移动到与最后一个对齐，注意力移到位置 2。上下文向量随之追踪。

```python
H = np.array([
    [1.0, 0.0, 0.2],
    [0.5, 0.5, 0.1],
    [0.1, 0.9, 0.3],
])

s_close_to_cat = np.array([0.9, 0.1, 0.2])
ctx, w = dot_attention(s_close_to_cat, H)
print("weights:", w.round(3))
```

```
weights: [0.464 0.305 0.231]
```

第一行胜出。然后将解码器状态移近第三个编码器状态，观察权重变化。就是这样。注意力就是显式对齐。

### 步骤 4：为什么这是通往 Transformer 的桥梁

将上面的语言翻译为 Q/K/V：

- **查询（Query）** = 解码器状态 `s_{t-1}`
- **键（Key）** = 编码器状态（我们用来打分的对象）
- **值（Value）** = 编码器状态（我们用来加权和的对象）

在经典注意力中，键和值是同一个东西。自注意力将它们分开：你可以用不同的学习投影查询一个序列自身作为 K 和 V。多头注意力用不同的学习投影并行运行它。Transformer 将整个阶段堆叠多次并丢弃 RNN。

数学是相同的。形状是相同的。从 Bahdanau 注意力到缩放点积注意力的教学跳跃主要是符号。

> **【中文解读】** 本节展示如何用成熟框架（如 PyTorch、HuggingFace 等）快速应用该技术。在实际项目中，优先使用经过验证的框架实现，可以减少 bug 并提高开发效率。




> **【拓展：Prompt Engineering 与 LLM 应用】** Prompt Engineering 已成为 NLP 工程师的核心技能。从 Zero-shot 到 Few-shot，从 Chain-of-Thought 到 ReAct，不同的提示策略适用于不同场景。在实际项目中，系统提示（System Prompt）的设计直接影响 LLM 应用的稳定性和输出质量。

## 用框架实现

PyTorch 和 TensorFlow 直接提供注意力。

```python
import torch
import torch.nn as nn

mha = nn.MultiheadAttention(embed_dim=128, num_heads=8, batch_first=True)
query = torch.randn(2, 5, 128)
key = torch.randn(2, 10, 128)
value = torch.randn(2, 10, 128)

output, weights = mha(query, key, value)
print(output.shape, weights.shape)
```

```
torch.Size([2, 5, 128]) torch.Size([2, 5, 10])
```

这就是一个 Transformer 注意力层。查询批次 5 个位置，键/值批次 10 个位置，每个 128 维，8 个头。`output` 是新的上下文增强查询。`weights` 是 5x10 的对齐矩阵，你可以可视化。

### 经典注意力仍然重要的场景

- 教学。单头、单层、基于 RNN 的版本让每个概念都可见。
- Transformer 放不下的设备端序列任务。
- 2014-2017 年的任何论文。不了解 Bahdanau 的约定你会误读它。
- 机器翻译中的细粒度对齐分析。原始注意力权重甚至在 Transformer 模型上也是可解释性工具，阅读它们需要知道它们是什么。

### 注意力权重作为解释的陷阱

注意力权重看起来可解释。它们是跨位置总和为 1 的权重；你可以绘制它们；高意味着 "看了这个"。审稿人喜欢它们。

它们并不像看起来那么可解释。Jain 和 Wallace (2019) 表明，注意力分布可以被置换和替换为任意替代，而不改变某些任务的模型预测。永远不要在没有消融或反事实检查的情况下将注意力权重作为推理的证据报告。

> **【中文解读】** 本节关注如何将模型部署为可用的产品。从原型到生产级系统需要考虑性能优化、错误处理、监控等多个维度。



## 产出物

保存为 `outputs/prompt-attention-shapes.md`：

```markdown
---
name: attention-shapes
description: Debug shape bugs in attention implementations.
phase: 5
lesson: 10
---

Given a broken attention implementation, you identify the shape mismatch. Output:

1. Which matrix has the wrong shape. Name the tensor.
2. What its shape should be, derived from (d_s, d_h, d_attn, T_enc, T_dec, batch_size).
3. One-line fix. Transpose, reshape, or project.
4. A test to catch regressions. Typically: assert `output.shape == (batch, T_dec, d_h)` and `weights.shape == (batch, T_dec, T_enc)` and `weights.sum(dim=-1) close to 1`.

Refuse to recommend fixes that silently broadcast. Broadcast-hiding bugs surface later as silent accuracy degradation, the worst kind of attention bug.

> **【中文解读】** 练习题按照 Easy/Medium/Hard 三个难度递进。建议至少完成 Medium 级别的题目，Hard 级别适合深入研究或面试准备。


For Bahdanau confusion, insist the decoder input is `s_{t-1}` (pre-step state). For Luong, `s_t` (post-step state). For dot-product, flag dimension mismatch between query and key as the most common first-time error.
```

## 练习题

1. **简单。** 实现 `softmax` 掩码，使编码器中的填充 token 的注意力权重为零。在变长序列的批次上测试。
2. **中等。** 为 Luong `general` 形式添加多头注意力。将 `d_h` 分割为 `n_heads` 组，每个头运行注意力，拼接。验证单头情况与你之前的实现匹配。
3. **困难。** 在第 09 课的玩具复制任务上训练带 Bahdanau 注意力的 GRU 编码器-解码器。绘制准确率 vs 序列长度。与无注意力基线比较。你应该看到差距随长度增长而扩大，确认注意力解除了瓶颈。

> **【中文解读】** 术语表中的 "What people say" vs "What it actually means" 区分了日常口语和精确技术含义。在团队协作中，统一术语定义可以避免大量沟通误解。


## 术语速查表

| 术语 | 人们常说的 | 实际含义 |
|------|-----------|---------|
| 注意力（Attention） | 看东西 | 值序列的加权平均，权重从查询-键相似度计算。 |
| 查询、键、值（QKV） | QKV | 三个投影：Q 询问，K 是要匹配的，V 是要返回的。 |
| 加性注意力 | Bahdanau | 前馈分数：`v^T tanh(W q + U k)`。 |
| 乘性注意力 | Luong 点积/通用 | 分数是 `q^T k` 或 `q^T W k`。更便宜，大多数任务上相同准确率。 |
| 对齐矩阵 | 那张漂亮的图 | 注意力权重作为 `(T_dec, T_enc)` 网格。阅读它看模型关注了什么。 |

> **【中文解读】** 延伸阅读提供了深入学习的高质量资源。这些论文和教程是该领域的经典参考文献，适合需要深入理解的读者。


## 延伸阅读

- [Bahdanau, Cho, Bengio (2014). Neural Machine Translation by Jointly Learning to Align and Translate](https://arxiv.org/abs/1409.0473) — 那篇论文。
- [Luong, Pham, Manning (2015). Effective Approaches to Attention-based Neural Machine Translation](https://arxiv.org/abs/1508.04025) — 三种分数变体及其比较。
- [Jain and Wallace (2019). Attention is not Explanation](https://arxiv.org/abs/1902.10186) — 可解释性警示。
- [Dive into Deep Learning — Bahdanau Attention](https://d2l.ai/chapter_attention-mechanisms-and-transformers/bahdanau-attention.html) — 带 PyTorch 的可运行演练。
