# 多头注意力
# 多头注意力

> 一个注意力头一次学会一个关系. 八个头学习八个. 头是自由的. 拿更多的.

> 一个注意力第一次学习一种关系.

> **【中文解读】**多头注意力让模型同时关注不同类型的关系:语法、语义、位置等.

**Type:** Build | **类型:** 动手
**Language:**子**语言:**字符串
**Prerequisites:** Phase 7 · 02 (Self-Attention from Scratch) | **前置知识:** 阶段 7 · 02（从零实现自注意力）
**Time:** ~75 minutes | **时间:** ~75 分钟

## 问题 问题引入

一个自我注意力头计算一个注意力矩阵.那个矩阵捕捉到一种关系,通常是减少任何训练信号的损失.如果你的数据有主体verb协议,共参考,长距离的演讲和语法分断,都在一起,一个头将它们成一个软最大分布,失去了一半的信号.

> 单个自注意头计算一个注意力矩阵.该矩阵捕获一种关系,通常是最小化训练信号损失的一种. 如果你的数据中的主题一致,共指消解,长程语篇和句法分块纠在一起,单个头将它们模糊成单个软最大分布,丢失一半信号.

2017年瓦斯瓦尼论文的修正:并行运行几个注意力函数,每个都具有自己的Q,K,V投影,并连接输出.每个头部都在更小的子空间中运行.`d_model / n_heads`总参数保持相同,表达功率上升.

> 2017年 Vaswani论文的修复方案:并行运行多个注意力函数,每个都有自己的Q、K、V投影,然后拼接输出──每个头在维度为`d_model / n_heads`总参数不变,表达能力上升.

单个论点是关于*多少头,以及键和值是否共享投影 (组列查询注意力,多查询注意力,多头潜伏注意力).

> 多头注意力是2026年每个变压器的默认配置.唯一的争论是关于*多少*头以及关键和值是否共享投影.

> **【中文解读】**单个注意头只能学习一种关系模式,但自然语言中存在多种关系. 许多注意头的核心思想是:使用多个独立的注意头并行工作,每个头在不同的子空间中学习不同的关系,最后拼接混合.

## 概念的核心概念

![Multi-head attention splits, attends, concatenates](../assets/multi-head-attention.svg)

**Split.**接下来`X`形状`(N, d_model)`项目到Q,K,V,每个形状`(N, d_model)`改装到`(N, n_heads, d_head)`在哪里`d_head = d_model / n_heads`转移到`(n_heads, N, d_head)`现在,我们要去.

> **拆分。**取形状为`(N, d_model)`的`X`◎投影到形状各为`(N, d_model)`,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,`(N, n_heads, d_head)`在其中`d_head = d_model / n_heads`转置为`(n_heads, N, d_head)`,我知道.

**Attend in parallel.**运行一个级别的点产品注意力在每个头脑.`(N, d_head)`头部在嵌入器的不同子空间上运行,并且在注意力计算过程中永远不会说话.

> **并行计算注意力。**在每头运行缩小积分注意力.`(N, d_head)`头在嵌入式的不同空间上操作,在注意力计算本身期间相互通信.

**Concatenate and project.**堆头回去`(N, d_model)`并且乘以学习的输出矩阵`W_o`形状`(d_model, d_model)`现在,我们要去.`W_o`这就是头脑的混合.

> **拼接并投影。**将头重新堆叠为`(N, d_model)`乘以学习的输出矩阵`W_o`形状为`(d_model, d_model)`,我知道.`W_o`们都在着.

**Why it works.**每个头都可以专业化,而不与其他对象预算竞争.2019年2024年的探测研究显示了不同的头部角色:位置头,参加前一个代币的头,复制头,命名实体头,诱导头 (这是内文学习的基础).

> **为什么有效。**每个头可以专为而无与其他头争夺表示预算.2019-2024年的探测研究显示了不同的头角色:位置头,关注前一个代币的头,复制头,命名实体头,归纳头.

> **【中文解读】**三步走:分开(分成多个子空间)→参加(每个头独立做注意力)→ Concat+Project(拼接并通过W_o 混合) ――关键洞察:每个头在不同子空间中独立工作,不争夺表示资源――实验表明不同头确实学会了不同的"职责"――

> **【拓展：GQA 在 Llama 3 中的实际应用】**拉马370B使用64个查询头,但只有8个KV头,将KV缓存压缩8倍.

**The 2026 lineage of variations:**

> **2026 年的变体谱系：**

| Variant | Q heads / Q 头数 | K/V heads / K/V 头数 | Used by / 使用者 |
|---------|---------|-----------|---------|
| Multi-head (MHA) / 多头 | N | N | GPT-2, BERT, T5 |
| Multi-query (MQA) / 多查询 | N | 1 | PaLM, Falcon |
| Grouped-query (GQA) / 分组查询 | N | G (e.g. N/8) | Llama 2 70B, Llama 3+, Qwen 2+, Mistral |
| Multi-head latent (MLA) / 多头潜在 | N | compressed to low-rank / 压缩为低秩 | DeepSeek-V2, V3 |

由于它削减了KV缓存存储量`N/G`通过将K/V压缩到隐藏空间,然后在计算时间上投影回来,

> 由于它将减少KV缓存内存,`N/G`倍,同时保持几乎完整质量――MLA 通过将K/V 压缩到隐藏空间进一步,然后在计算时投影回来花费FLOP,节省更多内存――

## 建立它,实现它.
```figure
multihead-split
```

## 建立它

### 步骤1:从我们已经有的单头注意力中分开头

拿起`SelfAttention`子,子,子,子,子,子,子,子,子,子,子,子,子,子,子,子,子,子,子,子,子,子,子,子,子,子,子,子,子,子,子,子,子,子,子,子,子,子,子,子,子,子,子,子,子,子,子,子,子,子,子,子,子,子,子,子,子,子,子,子,子,子,子,子,子,子,子,子,子,子,子,子,子,子,子,子,子,子,子,子,子,子,子,子,子,子,子,子,子,子,子,子,子,子,子,子,子,子,子,子,子,子,子,子,子,子,子,子,子,子,子,子,子,子,子`code/main.py`对于一个无数的实现,逻辑是:

> 取第02课的`SelfAttention`,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,`code/main.py`中的 numpy 实现;逻辑如下:

```python
def split_heads(X, n_heads):
    n, d = X.shape
    d_head = d // n_heads
    return X.reshape(n, n_heads, d_head).transpose(1, 0, 2)  # (heads, n, d_head)

def combine_heads(H):
    h, n, d_head = H.shape
    return H.transpose(1, 0, 2).reshape(n, h * d_head)
```

一个重塑,一个转换,没有循环. 这正是PyTorch在做的事情.`nn.MultiheadAttention`现在,我们要去.

> 一次重塑和一次转换.没有循环.`nn.MultiheadAttention`底层做什么.

> **【中文解读】** `split_heads`和 `combine_heads`只是重塑+转换操作,无需循环. 这就是 GPU 上高效的原因.

### 步骤2: 运行一个个节点的产品关注个头.

每个头都得到了自己的Q,K,V.

> 每个头都得到了自己的Q、K、V切片.

```python
def mha_forward(X, W_q, W_k, W_v, W_o, n_heads):
    Q = X @ W_q
    K = X @ W_k
    V = X @ W_v
    Qh = split_heads(Q, n_heads)         # (heads, n, d_head)
    Kh = split_heads(K, n_heads)
    Vh = split_heads(V, n_heads)
    scores = Qh @ Kh.transpose(0, 2, 1) / np.sqrt(Qh.shape[-1])
    weights = softmax(scores, axis=-1)
    out = weights @ Vh                    # (heads, n, d_head)
    concat = combine_heads(out)
    return concat @ W_o, weights
```

在真正的硬件上`Qh @ Kh.transpose(...)`是一个`bmm` GPU 看到一个单批的形状.`(heads, N, d_head) × (heads, d_head, N) -> (heads, N, N)`增加头子是免费的.

> 在真实硬件上,`Qh @ Kh.transpose(...)`是一次的`bmm`△GPU 看到的是形状为`(heads, N, d_head) × (heads, d_head, N) -> (heads, N, N)`单次批量矩阵乘法.

### 阶段3:分组查询注意力变体

只有关键和值预测变化.`n_heads`组; K 和 V 得到`n_kv_heads < n_heads`组,并重复一致:

> 只有关键和值的投影发生变化.`n_heads`个组;K 和 V 有`n_kv_heads < n_heads`个组,并被重复以匹配:

```python
def gqa_project(X, W, n_kv_heads, n_heads):
    kv = split_heads(X @ W, n_kv_heads)       # (kv_heads, n, d_head)
    repeat = n_heads // n_kv_heads
    return np.repeat(kv, repeat, axis=0)      # (n_heads, n, d_head)
```

根据推论,这节省了记忆力,因为只有`n_kv_heads`没有在KV缓存中存活的副本`n_heads`拉马370B使用64个查询头,8个KV头,一个8倍缓存缩小器.

> 在推理时,这节省了内存,因为只有`n_kv_heads`份副本存在于KV 缓存中,而不是`n_heads`份额: 拉马370B 使用64个查询头和8个KV头

> **【拓展：MQA/GQA 在推理中的内存节约】**对于128K上下文,这意味着节省GB显存量――这是大模型长下文推理的关键优化QA几乎没有损失质量,但显著降低推理成本――

### 步骤4:检查每个头脑学到了什么

按一个短句子,用4个头来运行MHA.`(N, N)`随机初始化,也就是部分信号,部分旋转对称性.

> 在短句子中,使用4个头运行MHA.`(N, N)`注意力矩阵──你会看到即使使用随机初始化,不同的头也会挑选不同的结构

## 用它实现框架

在 PyTorch 中,单行版本:

> 火中,一行版本:

```python
import torch.nn as nn

mha = nn.MultiheadAttention(embed_dim=512, num_heads=8, batch_first=True)
```

根据 PyTorch 2.5+ 的 GQA:

> 光 2.5+:

```python
from torch.nn.functional import scaled_dot_product_attention

# scaled_dot_product_attention auto-dispatches Flash Attention on CUDA.
# For GQA, pass Q of shape (B, n_heads, N, d_head) and K,V of shape
# (B, n_kv_heads, N, d_head). PyTorch handles the repeat.
out = scaled_dot_product_attention(q, k, v, is_causal=True, enable_gqa=True)
```

**How many heads?**2026年生产模型的指纹规则:

> **多少个头？**2026年生产模型的经验法则:

| Model size / 模型大小 | d_model | n_heads | d_head |
|------------|---------|---------|--------|
| Small (~125M) / 小型 | 768 | 12 | 64 |
| Base (~350M) / 基础 | 1024 | 16 | 64 |
| Large (~1B) / 大型 | 2048 | 16 | 128 |
| Frontier (~70B) / 前沿 | 8192 | 64 | 128 |

`d_head`几乎总是降落在64或128位.这是一个头能"看到"多少的单位.`sqrt(d_head)`您将失去"许多小专家"的福利.

> `d_head`几乎总是64或128个. 它是一个头能"看到"多少的量单位.`sqrt(d_head)`冲突;超过256时,你失去了"许多小专家"的好处.

## 运送它.

看到`outputs/skill-mha-configurator.md`技能建议对新变压器进行头数, kv头数和投影策略,以设置参数预算,序列长度和部署目标.

> 参见`outputs/skill-mha-configurator.md`△ 应对新变压器的技能 推头号,KV头号和投影策略,给定参数预算,序列长度和部署目标.

## 练习题

1. **Easy / 简单。**取出MHA的`code/main.py`改变`n_heads`从1到16`d_model=64`更多头脑有助于,高,或伤害?
   取 `code/main.py`中的MHA,在`d_model=64`在一定情况下将`n_heads`从1改为16――在一个合成复制任务上绘制微型单层模型的损失――更多头有帮助吗?

2. **Medium / 中等。**实现MQA (所有查询头都共享一个KV头).测量参数数量多少下降与全MHA.计算在推断时KV缓存尺寸缩小多少为N=2048.
   实现MQA(一个KV头在所有查询头间共享) ――测量与完整MHA相比参数数量下降多少――计算在N=2048的推理时KV缓存大小缩小多少――

3. **Hard / 困难。**执行多头潜伏注意的小版本:压缩K,V到一个级别`r`隐藏在KV缓存中,在注意时解压.`r`缓存内存在满满MHA的1/8以下,而质量在验证后保持在1位内?
   实现迷你版的多头潜伏注意:将 K,V 压缩为秩 `r`隐向量,在 KV 缓存中存储隐向量,在注意力计算时解压.`r`低值缓存内存降至完整的MHA的1/8以下,同时质量保持在验证困惑度的1比特以内?

## 关键词 快速查找表

| Term | What people say / 人们怎么说 | What it actually means / 实际含义 |
|------|------------------------------|----------------------------------|
| Head / 头 | "A single attention circuit" / "一个注意力电路" | One Q/K/V projection of dimension `d_head = d_model / n_heads` with its own attention matrix. 维度为 `d_head = d_model / n_heads` 的一个 Q/K/V 投影，有自己的注意力矩阵。 |
| d_head | "Head dimension" / "头维度" | Per-head hidden width; almost always 64 or 128 in production. 每个头的隐藏宽度；生产中几乎总是 64 或 128。 |
| Split / combine / 拆分/合并 | "Reshape tricks" / "reshape 技巧" | `(N, d_model) ↔ (n_heads, N, d_head)` reshape+transpose around attention. 围绕注意力的 `(N, d_model) ↔ (n_heads, N, d_head)` reshape+transpose。 |
| W_o | "Output projection" / "输出投影" | `(d_model, d_model)` matrix applied after concatenating heads; where heads mix. 拼接头后应用的 `(d_model, d_model)` 矩阵；头混合的地方。 |
| MQA | "One KV head" / "一个 KV 头" | Multi-Query Attention: single shared K/V projection. Smallest KV cache, some quality loss. 多查询注意力：单个共享的 K/V 投影。最小 KV 缓存，有一些质量损失。 |
| GQA | "The default since Llama 2" / "Llama 2 之后的默认" | Grouped-Query Attention with `n_kv_heads < n_heads`; repeats to match Q. 分组查询注意力，`n_kv_heads < n_heads`；重复以匹配 Q。 |
| MLA | "DeepSeek's trick" / "DeepSeek 的技巧" | Multi-head Latent Attention: K,V compressed to low-rank latent, decompressed at attend time. 多头潜在注意力：K,V 压缩为低秩隐向量，在注意力计算时解压。 |
| Induction head / 归纳头 | "The circuit behind in-context learning" / "上下文学习背后的电路" | A pair of heads that detect previous occurrences and copy what followed them. 一对检测先前出现模式并复制后续内容的头。 |

## 继续阅读 继续阅读

- [Vaswani et al. (2017). Attention Is All You Need §3.2.2](https://arxiv.org/abs/1706.03762)原始多头型规格.
  瓦斯瓦尼 等人 (Vaswani) 于2017年

- [Shazeer (2019). Fast Transformer Decoding: One Write-Head is All You Need](https://arxiv.org/abs/1911.02150)MQA论文
   MQA 论文──

- [Ainslie et al. (2023). GQA: Training Generalized Multi-Query Transformer Models from Multi-Head Checkpoints](https://arxiv.org/abs/2305.13245)如何在培训后将MHA转换为GQA.
  如何将MHA转换为GQA──

- [DeepSeek-AI (2024). DeepSeek-V2 Technical Report](https://arxiv.org/abs/2405.04434) MLA 和为什么它超过MHA/GQA在缓存内存.
  据悉,在2024年,MLA 及为何在缓存内存上击败了MHA/GQA.

- [Olsson et al. (2022). In-context Learning and Induction Heads](https://transformer-circuits.pub/2022/in-context-learning-and-induction-heads/index.html)机械化看看头部实际上做什么.
                                                                                                                                                                                                                                                                

> **【拓展：Induction Heads 与上下文学习】**人类研究发现,变革者的上下文学习能力 (在文本中学习) 主要是由一种称为"诱导头"的注意力头实现的.它们在检测序列中出现的模式并复制后续内容. 这解释了为什么大模型能"从示例中学习"而无需更新权重.
