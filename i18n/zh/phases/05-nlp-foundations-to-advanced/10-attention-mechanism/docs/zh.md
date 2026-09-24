#                       

> 解码器停止眼看压缩的摘要,开始查看整个来源.
> 解码器不再眼看缩写摘要,开始看整个源.

> **【中文解读】**注意力机制让模型关注输入的相关部分.

**Type:** Build | **类型:** 动手
**Languages:** Python | **语言:** Python
**Prerequisites:** Phase 5 · 09 (Sequence-to-Sequence Models) | **前置知识:** Phase 5 · 09（序列到序列模型）
**Time:** ~45 minutes | **时间:** ~45 分钟

## 问题 问题引入

课程09结束时出现了测量故障.在玩具复制任务上训练的GRU编码器-解码器从89%的精度在长度5到近巧的长度80的原因是结构性,而不是训练错误:编码器收集的每一点信息都必须合适于一个固体尺寸的隐藏状态,解码器从来没有看到任何其他东西.

> 第9课 通过一个可测量的失败结束. 在玩具复制任务上训练的GRU编码器解码器在长度5时89%准确率,在长度80时接近随机.原因是结构性,不是训练错误:编码器收集的每一个信息都必须塞进一个固定的大小的隐藏状态,解码器看不到其他任何东西.

巴哈达纳,乔和孟基奥于2014年发布了一项三行修正.而不是给解码器只给出最后的编码器状态,保持每个编码器状态.在每个编码器步骤上,计算一个权重平均的编码器状态,重量说"解码器需要看多少编码器位置.`i`这就是重量平均的背景,它改变了每一步的解码器.

> 巴哈达努·乔和孟基奥在2014年发表了一篇三行修复――不仅给解码器最终编码器状态,而是保留每个编码器状态――在每个解码器步骤中,计算编码器状态的加权平均,权重表示"解码器现在需要更多看编码器位置.`i`这种加权平均是上下文,它在每个解码器步骤都改变.

这就是整个想法.变压器扩展了它.自我注意力将它应用到单个序列上.多头注意力并行运行它.但2014版本已经打破了瓶,一旦你得到了它,变压器的枢纽是工程,而不是概念.

> 这就是全部的想法. 变压器 扩展了它. 自主注意力将将其应用于单个序列. 多头注意力并行运行它.

## 概念的核心概念

> **【中文解读】**本节介绍核心概念和理论基础.掌握这些概念是后续动手实现的前提,同时也是面试和工程实践中高频考察的知识点.

![Bahdanau attention: decoder queries all encoder states](../assets/attention.svg)

在每个解码器步骤中`t`其他:

> 在每个解码器步骤中`t`其他:

1. 使用之前的解码器隐藏状态`s_{t-1}`作为一个**query**现在,我们要去.
2. 给每一个编码器隐藏状态进行评分`h_1, ..., h_T`每个编码器位置都有一个 skalar.
3. 软max的分数以获得注意力重量`α_{t,1}, ..., α_{t,T}`总数为1.
4. 文本向量`c_t = Σ α_{t,i} * h_i`编码器状态的权重平均值.
5. 解码器需要`c_t`另外一个输出代币,产生了下一个代币.
   1. 使用前一个解码器隐藏状态`s_{t-1}`作为一个**查询（Query）**,我知道.
   2. 将它与每个编码器隐藏状态`h_1, ..., h_T`打分――每个编码器位置一个标量――
   3. 为了分数做软最大 得到注意力权重`α_{t,1}, ..., α_{t,T}`总和为1
   4. 上下文向量 `c_t = Σ α_{t,i} * h_i`编码器状态的加权平均
   5. 解码器取 `c_t`加入前一个输出代币,产生下一个代币.

权重平均值是点.当解码器需要将"Je"转换为"I",它重量化码器状态为"Je"高,其他的低.当它需要"不",它重量化"pas"高.文本向量重量化每个步骤.

> 加权平均是关键. 当解码器需要将"Je" 翻译为"I" 时,它对"Je" 上的编码器状态权重高,其他低. 当需要"不" 时,它对"pas" 权重高.

> **【拓展：大语言模型的工程实践】**从GPT到ChatGPT,NLP领域经历了从"每个任务训练一个模型"到"一个模型解决所有任务"的范式转变. 在实际工程中,LLM的部署需要考虑代币限制,延迟,成本,安全审查等问题.

> **【拓展：RAG 与企业知识库】**检索增强生成 (RAG) 是当前企业人工智能应用中最流行的架构:将用户查询先检索相关文档片段,再将检索结果作为上下文给LLM 生成答案――这种方式解决了LLM 知识过时和幻觉问题――向量数据库――如Milvus、Pinecone、Weaviate) 是RAG系统的核心组件――

> **【拓展：NLP 的多语言挑战】**全球有7000多种语言,但NLP研究主要集中在英语等少数语言.跨语言迁移学习,多语言预训模型 (如 mBERT,XLM-R) 是解决低资源语言NLP的主要方法.

## 形状,让每个人都在头上种下东西.

这就是每次注意力实施的第一次错误.

> 这是每个注意力实现第一次出错的地方.慢慢读.

| Thing / 对象 | Shape / 形状 | Notes / 说明 |
|-------|-------|-------|
| Encoder hidden states `H` / 编码器隐藏状态 `H` | `(T_enc, d_h)` | If BiLSTM, `d_h = 2 * d_hidden` / 如果是 BiLSTM，`d_h = 2 * d_hidden` |
| Decoder hidden state `s_{t-1}` / 解码器隐藏状态 | `(d_s,)` | One vector / 一个向量 |
| Attention score `e_{t,i}` / 注意力分数 | scalar / 标量 | One per encoder position / 每个编码器位置一个 |
| Attention weight `α_{t,i}` / 注意力权重 | scalar / 标量 | After softmax over all `i` / 对所有 `i` 做 softmax 后 |
| Context vector `c_t` / 上下文向量 | `(d_h,)` | Same shape as an encoder state / 与编码器状态相同形状 |

**Bahdanau (additive) score.** `e_{t,i} = v_α^T * tanh(W_a * s_{t-1} + U_a * h_i)`现在,我们要去.

> **Bahdanau（加性）分数。** `e_{t,i} = v_α^T * tanh(W_a * s_{t-1} + U_a * h_i)`,我知道.

- `s_{t-1}`具有形状`(d_s,)`现在`h_i`具有形状`(d_h,)`现在,我们要去.
- `W_a`具有形状`(d_attn, d_s)`现在,我们要去.`U_a`具有形状`(d_attn, d_h)`现在,我们要去.
- 它们的子里面的积分有形状.`(d_attn,)`现在,我们要去.
- `v_α`具有形状`(d_attn,)`内部产品与`v_α`升到一个度.**This is what `v_α` does.**它们不是魔法,而是投影,使注意力光向量变成了尺度分数.
  - `s_{t-1}`形状为`(d_s,)`没有任何`h_i`形状为`(d_h,)`,我知道.
  - `W_a`形状为`(d_attn, d_s)`,我知道.`U_a`形状为`(d_attn, d_h)`,我知道.
  - 内部的和形状为`(d_attn,)`,我知道.
  - `v_α`形状为`(d_attn,)`△与`v_α`积缩为标量.**这就是 `v_α` 的作用。**它不是魔法. 它是将注意力维度向量投影为标量分数的投影.

**Luong (multiplicative) score.**它们有三个变体:

> **Luong（乘性）分数。**三个变体:

- `dot`其他`e_{t,i} = s_t^T * h_i`需要`d_s == d_h`如果你的编码器是双向的,就跳过.
  `dot`其他:`e_{t,i} = s_t^T * h_i`△要求`d_s == d_h`如果编码器是双向的则跳过.
- `general`其他`e_{t,i} = s_t^T * W * h_i`随着`W`形状`(d_s, d_h)`消除了同等度的限制.
  `general`其他:`e_{t,i} = s_t^T * W * h_i`没有任何`W`形状为`(d_s, d_h)`移除等维约束
- `concat`基本上是巴哈达努形式.
  `concat`由于前两种更便宜,很少使用.

**One Bahdanau / Luong gotcha worth naming.**巴哈达努使用`s_{t-1}`路恩使用了 语,`s_t`它们混合后,产生了微妙的错误梯度,非常难以调试.

> **一个值得注意的 Bahdanau / Luong 陷阱。**百达纳乌 使用`s_{t-1}`长时间使用 长时间使用 长时间使用 长时间使用`s_t`它们会产生极其难以调试的微妙错误梯度.

## 建立它,实现它.

> **【中文解读】**本节通过代码实现从零到核心算法――这种"从零开始"的方式可以帮助理解框架背后的原理,遇到问题时不会被黑盒困住――
```figure
attention-heatmap
```

## 建立它

### 步骤1:添加剂 (Bahdanau) 注意

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

检查你的形状与上面的表.`encoder_states`具有形状`(T_enc, d_h)`现在,我们要去.`projected_enc`具有形状`(T_enc, d_attn)`现在,我们要去.`projected_dec`具有形状`(d_attn,)`广播.`combined`具有形状`(T_enc, d_attn)`现在,我们要去.`scores`具有形状`(T_enc,)`现在,我们要去.`weights`具有形状`(T_enc,)`现在,我们要去.`context`具有形状`(d_h,)`运送它.

> 查看上面的表格查看你的形状.`encoder_states`形状为`(T_enc, d_h)`,我知道.`projected_enc`形状为`(T_enc, d_attn)`,我知道.`projected_dec`形状为`(d_attn,)`并广播.`combined`形状为`(T_enc, d_attn)`,我知道.`scores`形状为`(T_enc,)`,我知道.`weights`形状为`(T_enc,)`,我知道.`context`形状为`(d_h,)`,我已经确定了.

### 步骤2: 卢昂点和一般

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

由于这就是为什么卢昂的论文登陆了. 在大多数任务上,相同的准确性,更少的代码.

> 每三行. 这就是卢昂论文的意义. 在大多数任务上,相同的准确率,代码更少.

### 步骤3:一个工作的数值示例

鉴于有三个编码状态 (大致是"猫","卫星","") 和一个与第一个最一致的编码状态,注意力分布集中在位置0. 如果编码状态转向最后的位置,注意力将转移到位置2.

> 给定三个编码器状态 ((大致是"猫"、"sat"、"mat") 和一个与第一个最相对的编码器状态,注意力分布集中在位置0――如果编码器状态移动到最后一个对齐,注意力移动到位置2――下文向量随其追踪――

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

首先是获胜的,然后把解码器状态移到第三个编码器状态,然后观察重量转移.

> 首先,我们将解码器状态移到第三个编码器状态,观察权重变化.

### 步骤4:为什么这就是转换器的桥梁

翻译上述语言为Q/K/V:

> 将上述语言翻译为 Q/K/V:

- **Query**= 解码器状态`s_{t-1}`
  **查询（Query）**解码器状态`s_{t-1}`
- **Key**= 编码状态 (我们对比的分数)
  **键（Key）**编码器状态 (我们用来打分的对象)
- **Value**=编码状态 (我们重量和总数)
  **值（Value）**编码器状态 (我们使用的权力和对象)

在经典的注意力中,密钥和值是一样的.自我注意力分开它们:你可以对一个序列进行查询,使用不同的学习投影为K和V.多头注意力与不同的学习投影并行运行.变压器堆叠整个阶段多次,然后放下RNN.

> 在经典的注意力中,键和值是同一个东西.自注意力将它们分开:你可以用不同的学习投影查询一个序列作为K和V.多头注意力用不同的学习投影并行运行它.

数学是相同的.形状是相同的.从巴哈达纳注意力到扩展点产品注意力的教学跳跃主要是符号.

> 数学是相同的. 形状是相同的. 从巴哈达努注意力到缩放点积注意力的教学跳跃主要是符号.

> **【中文解读】**本节展示了如何使用成熟框架 (如PyTorch、HuggingFace等) 快速应用该技术.

> **【拓展：Prompt Engineering 与 LLM 应用】**快速工程已成为NLP工程师的核心技能. 从零射到少射,从思想链到反应,不同的提示策略适用于不同场景. 在实际项目中,系统提示 (系统提示) 的设计直接影响了LLM应用的稳定性和输出质量.

## 用它实现框架

鱼和鱼流直接送上注意力.

> 火和光流直接提供注意力.

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
torch.Size([2, 5, 128]) torch.Size([2, 5, 10]
```

查询组5个位置,关键/值组10个位置,每个128个,8个头.`output`对于这些问题来说,`weights`它们是5×10的对齐矩阵,

> 这就是一个变压器注意力层.查询批次 5 个位置,键/值批次 10 个位置,每个 128 个维,8 个头.`output`是新的上下文增强查询.`weights`五×10的矩阵,你可以看到.

### 当古典的注意力仍然重要时

- 单头,单层,基于RNN的版本使每个概念都可见.
  教学──单头、单层、基于RNN的版本让每个概念都可见──
- 变压器不适合的设备上序列任务.
  变压器 放不下设备端序列任务.
- 你会错误地读到任何2014-2017年报纸,
  没有了解巴哈达努的约定你会误读它.
- 精细的对齐分析在MT中. 粗的注意力重量即使在变压器模型上也是一个可解释的工具,
  机器翻译中的细分量对齐分析――原始注意力权重甚至在变压器模型上也是可解释的工具,阅读它们需要知道它们是什么――

### 关注重量作为解释陷

关注重量看起来可以解释.它们是重量,可以在一个位置上加起来;你可以绘制它们;高意味着"看到了这个".评论家喜欢它们.

> 注意力权重看起来可以解释.它们是跨位置总和为 1 的权重;你可以绘制它们;高意味着"看到了这个".

简和瓦莱斯 (2019) 表明,注意力分布可以通过任意替代品来改变,而不会改变某些任务的模型预测.永远不要报告注意力重量作为没有抽象或反事实检查的推理证据.

> 它们看起来并不像这样的解释. 简和华莱斯 (2019) 表明,注意力分布可以被替换和替换为任意的替代,而不改变某些任务的模型预测.

> **【中文解读】**本节关注如何将模型部署为可用的产品. 从原型到生产级系统需要考虑性能优化,错误处理,监控等多个维度.

## 运送它.

保存如`outputs/prompt-attention-shapes.md`其他:

> 保存为`outputs/prompt-attention-shapes.md`其他:

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

For Bahdanau confusion, insist the decoder input is `s_{t-1}` (pre-step state). For Luong, `s_t` (post-step state). For dot-product, flag dimension mismatch between query and key as the most common first-time error.
```

> **【中文解读】**练习题按照易/中/难 三个难度递进;;建议至少完成中级题,Hard级适合深入研究或面试准备;;

## 练习题

1. **Easy.**实施`softmax`测试一批具有变长序列的批量.
   **简单。**实现`softmax`掩码,使编码器中填充代币的注意力权重为零──在变长序列的批次上测试──
2. **Medium.**增加多头关注的路昂`general`形式,分开`d_h`进入`n_heads`检查单头案例是否符合您的早期实施.
   **中等。**为长期`general`形式添加多头注意力──将 `d_h`分割为`n_heads`组,每个头运行注意力,拼接,拼接, 验证, 验证, 验证, 验证, 验证, 验证, 验证, 验证, 验证, 验证, 验证, 验证, 验证, 验证, 验证, 验证, 验证, 验证, 验证, 验证, 验证, 验证, 验证, 验证, 验证, 验证, 验证, 验证, 验证, 验证, 验证, 验证, 验证, 验证, 验证, 验证, 验证, 验证, 验证, 验证, 验证, 验证, 验证, 验证, 验证,验证,验证,验证,验证,验证,验证,验证,验证,验证,验证,验证,验证,验证,验证,验证,验证,验证,验证,验证,验证,验证,验证,验证,验证,验证,验证,验证,验证,验证,验证,验证,验证,验证,验证,验证,验证,验证,验证,验证,验证,验证,验证,验证,验证,验证,验证,验证,验证,验证,
3. **Hard.**训练一个GRU编码器-解码器,用巴哈达纳注意力从第09课开始的玩具复制任务. 剧情精度与序列长度. 与没有注意力基线相比较.随着长度的增加,你应该看到差距扩大,确认注意力提高了瓶.
   **困难。**在第九课的玩具复制任务上训练带巴哈达努注意 GRU编码器解码器――绘制准确率与序列长度――与无注意基线相比――你应该看到随着长度的增长和扩大差距,确认注意力解除了瓶──

> **【中文解读】**在团队协作中,统一术语定义可以避免大量沟通误解.

## 关键词 快速查找表

| Term / 术语 | What people say / 人们常说的 | What it actually means / 实际含义 |
|------|-----------------|-----------------------|
| Attention（注意力） | Looking at things / 看东西 | Weighted average of a value sequence, weights computed from a query-key similarity. / 值序列的加权平均，权重从查询-键相似度计算。 |
| Query, Key, Value（查询、键、值） | QKV | Three projections: Q asks, K is what to match, V is what to return. / 三个投影：Q 询问，K 是要匹配的，V 是要返回的。 |
| Additive attention（加性注意力） | Bahdanau | Feed-forward score: `v^T tanh(W q + U k)`. / 前馈分数：`v^T tanh(W q + U k)`。 |
| Multiplicative attention（乘性注意力） | Luong dot / general | Score is `q^T k` or `q^T W k`. Cheaper, same accuracy on most tasks. / 分数是 `q^T k` 或 `q^T W k`。更便宜，大多数任务上相同准确率。 |
| Alignment matrix（对齐矩阵） | The pretty picture / 那张漂亮的图 | Attention weights as a `(T_dec, T_enc)` grid. Read it to see what the model attended to. / 注意力权重作为 `(T_dec, T_enc)` 网格。阅读它看模型关注了什么。 |

> **【中文解读】**延伸阅读提供了深入学习的高质量资源. 这些论文和教程是该领域的经典参考文献,适合需要深入了解的读者.

## 继续阅读 继续阅读

- [Bahdanau, Cho, Bengio (2014). Neural Machine Translation by Jointly Learning to Align and Translate](https://arxiv.org/abs/1409.0473)报纸. / 那篇论文.
- [Luong, Pham, Manning (2015). Effective Approaches to Attention-based Neural Machine Translation](https://arxiv.org/abs/1508.04025)三分数变体及其比较.
- [Jain and Wallace (2019). Attention is not Explanation](https://arxiv.org/abs/1902.10186)解释性警示.
- [Dive into Deep Learning — Bahdanau Attention](https://d2l.ai/chapter_attention-mechanisms-and-transformers/bahdanau-attention.html)可运行演练.
