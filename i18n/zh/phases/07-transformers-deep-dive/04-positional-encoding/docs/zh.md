# 位置编码 鼻状,ROPE,ALiBi
# 位置编码  正弦、RoPE、ALiBi

> 关注是变量不变的. "猫坐在床上"和"猫坐在床上"产生相同的输出,没有位置信号.三个算法每一个通过不同的投注来解决它.

> 注意力是排列不变的. 猫坐在床上和猫在床上,在没有位置信号时产生相同的输出. 三种算法修复了这个问题.

> **【中文解读】**变压器 没有位置信息,需要手动注入.

**Type:** Build | **类型:** 动手
**Language:**子**语言:**字符串
**Prerequisites:** Phase 7 · 02 (Self-Attention), Phase 7 · 03 (Multi-Head Attention) | **前置知识:** 阶段 7 · 02（自注意力），阶段 7 · 03（多头注意力）
**Time:** ~45 minutes | **时间:** ~45 分钟

## 问题 问题引入

关注点产品的规模是顺序盲目的.`softmax(Q K^T / √d) V`通过对式相似性计算.`X`没有什么在注意力中关心位置.

> 缩放点积注意力是无关的.`softmax(Q K^T / √d) V`由于相似度而来.`X`,输出,都被打乱了.

对于语言,代码,音频,视频,任何有序的东西都意味着,

> 在词袋模型中,这不是错误. 但对于语言,代码,音频,视频,任何顺序的东西,

解决方案是以某种方式注入位置.

> 修复方法是以某种方式将位置注入嵌入.

1. **Absolute sinusoidal**加入 `sin/cos`简单,无需学习,不适合超越训练的长度.
   **绝对正弦编码**现在,我们在这个世界里.`sin/cos`简单无需学习 培训长度之外的外推能力差距

2. **RoPE — Rotary Position Embeddings**旋转Q和K向量以与位置相对的角度. 编码直在点数中 *相对*位置. 2026年占主导地位.
   **RoPE — 旋转位置嵌入**根据位置成正比的角度旋转 Q 和 K 向量──直接在点积中编码*相对*位置──2026年占主导地位──

3. **ALiBi — Attention with Linear Biases**根据距离,对注意力分数添加一个每头线性罚款. 极好的长度抽出.
   **ALiBi — 带线性偏置的注意力**根据注意力分数的距离,加上每个头的线性惩罚.

截至2026年,基本上每个边境开放模型都使用RoPE:Llama 2/3/4,Qwen 2/3,Mistral,Mixtral,DeepSeek-V3,Kimi.少数长文本模型使用ALiBi或其现代变体.绝对突形是历史性的.

> 截至2026年,基本上每个前沿开源模型都使用RoPE:Llama 2/3/4、Qwen 2/3、Mistral、Mixtral、DeepSeek-V3、Kimi──少数长上下文模型使用ALiBi或其现代变体──绝对正弦编码已成为历史──

> **【中文解读】**自注意本身是排列不变的打乱输入序列,输出只是对应打乱.对语言是致命的.三种位置编码方案代表三个时代:

## 概念的核心概念

![Sinusoidal absolute vs RoPE rotations vs ALiBi distance bias](../assets/positional-encoding.svg)

### 绝对正弦编码

预先计算一个固定矩阵`PE`形状`(max_len, d_model)`其他:

> 预计算一个固定矩阵`PE`形状为`(max_len, d_model)`其他:

```
PE[pos, 2i]   = sin(pos / 10000^(2i / d_model))
PE[pos, 2i+1] = cos(pos / 10000^(2i / d_model))
```

那么`X' = X + PE[:N]`模型学会从相模式中读取位置. 失败超出了`max_len`没有什么告诉模型在2048位置发生什么,当它只看到位置02047时.

> 然后在注意力前`X' = X + PE[:N]`△每维度是不同频率的正弦波.`max_len`失效:模型只见到位置0-2047 时,没有什么告诉它在位置2048会发生什么.

### 转换位置嵌入

转换Q和K向量 (不是嵌入式).`(2i, 2i+1)`其他:

> 旋转Q 和 K 向量(不是嵌入) ⋅对对维度`(2i, 2i+1)`其他:

```
[q'_2i    ]   [ cos(pos·θ_i)  -sin(pos·θ_i) ] [q_2i   ]
[q'_2i+1  ] = [ sin(pos·θ_i)   cos(pos·θ_i) ] [q_2i+1 ]

θ_i = base^(-2i / d_head),  base = 10000 by default
```

按位置的键进行相同的旋转`pos_k`点的产品`q'_m · k'_n`成为一个函数`(m - n)`只有一个人.**the attention score depends only on the relative distance**虽然旋转是绝对位置的.

> 对于关键应用位置`pos_k`它们的旋转也相同.`q'_m · k'_n`变得仅仅`(m - n)`的函数──也就是说:**注意力分数只取决于相对距离**虽然旋转是基于绝对位置的.

> **【中文解读】**罗佩的精妙之处:虽然旋转角基于绝对位置,但Q·K的点积只取决于相对距离 (m-n) ⋅这意味着模型自然地学会了相对位置关系――调整基础参数也可以实现长上下文外推,Llama 3 正通过这种方式从8K 扩展到128K 上下文──

> **【拓展：RoPE 在 Llama 3 中的长上下文扩展】**通过 YaRN (Llama 3 通过 YaRN) 另一种RoPE扩展N) 方法将从8K扩展到128K.核心思路是调整RoPE的基频率,使高频维度保持原始分辨率,低频维度进行插值.这种"分维度处理"策略既保持了短距离的精确位置感知,又扩大了长距离的外推能力.

扩展ROPE: `base`通过这种方式,Llama 3从8K到128K的环境扩展.

> 扩展 罗佩:`base`由于不重新训练,可以缩放到更长的上下文──Llama 3就是这样从8K扩展到128K 上下文──

### 带着线性偏移的注意力

忽略嵌入技巧. 偏见的注意力直接得分:

> 跳过嵌入技巧──直接偏置注意力分数:

```
attn_score[i, j] = (q_i · k_j) / √d  -  m_h · |i - j|
```

在哪里?`m_h`是一个特定的头斜率 (例如 `1 / 2^(8·h/H)`报纸显示,长度抽出比较像座形状,与RoPE在原始训练长度上相匹配.

> 其中`m_h`是特定的头斜率`1 / 2^(8·h/H)`论文显示长度外推超过正弦编码,其原始训练长度与RoPE相匹配.

### 2026年,我们要选择什么?

| Variant / 变体 | Extrapolation / 外推能力 | Training cost / 训练成本 | Used by / 使用者 |
|---------|---------------|---------------|---------|
| Absolute sinusoidal / 绝对正弦编码 | poor / 差 | free / 免费 | original transformer, early BERT |
| Learned absolute / 学习式绝对编码 | none / 无 | tiny / 微小 | GPT-2, GPT-3 |
| RoPE | good with scaling / 良好（带缩放） | free / 免费 | Llama 2/3/4, Qwen 2/3, Mistral, DeepSeek-V3, Kimi |
| RoPE + YaRN | excellent / 优秀 | fine-tune stage / 微调阶段 | Qwen2-1M, Llama 3.1 128K |
| ALiBi | excellent / 优秀 | free / 免费 | BLOOM, MPT, Baichuan |

由于它没有改变建筑,它编码相对位置,它引起了人们的注意.`base`超参数为长文本细调提供了清洁的按.

> 由于它不需要改变结构,所以它可以插入注意力,编码相对位置,并且它`base`超参数长期下文微调提供了清晰的调节旋.

> **【中文解读】**2026年位置编码的选择很明确:新项目默认 RoPE──它不会改变结构、编码相对位置、并且通过基数提供长上下文微调的清晰路径──只有在极端外推场景(训练4K、推1M)才考虑ALiBi──

> **【拓展：位置编码对长上下文 RAG 的影响】**在RAG系统中,位置编码直接影响长文档处理能力.RoPE + YaRN 让Llama 3 能处理128K代币的上下文,这意味着可以一次性处理约300页文档.位置编码方案的选择决定了RAG系统是否需要复杂的分块策略.
```figure
rope-explorer
```

## 建立它

## 建立它,实现它.

### 步骤1:正弦编码

看到`code/main.py`计算四行:

> 参见`code/main.py`△4 行计算:

```python
def sinusoidal(N, d):
    pe = [[0.0] * d for _ in range(N)]
    for pos in range(N):
        for i in range(d // 2):
            theta = pos / (10000 ** (2 * i / d))
            pe[pos][2 * i]     = math.sin(theta)
            pe[pos][2 * i + 1] = math.cos(theta)
    return pe
```

在第一层注意力之前,将此添加到嵌入矩阵中.

> 在第一层注意力之前将会增加到嵌入矩阵上.

### 步骤2:将RoPE应用于Q,K.

罗佩在Q和K上在现场运行.

> 对于Q和K原地操作――对每对维度:

```python
def apply_rope(x, pos, base=10000):
    d = len(x)
    out = list(x)
    for i in range(d // 2):
        theta = pos / (base ** (2 * i / d))
        c, s = math.cos(theta), math.sin(theta)
        a, b = x[2 * i], x[2 * i + 1]
        out[2 * i]     = a * c - b * s
        out[2 * i + 1] = a * s + b * c
    return out
```

关键:在位置上将相同的函数应用到Q`m`,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,.`n`他们的点产品接收了一个`cos((m-n)·θ_i)`关注可以免费学习相对位置.

> 关键:对位置`m`的Q和位置`n`它们的点积在每个坐标对得到一个.`cos((m-n)·θ_i)`由于子,注意力免费学习相对位置.

> **【中文解读】**实现核心:对Q和K的每对维度 (2i,2i+1) 做位置相关的旋转.旋转角与位置成正比,因此Q_m · K_n的点积中会出现 cos(((m-n) *theta) 项,自然编码了相对距离.

### 步骤3:ALiBi斜率和偏移

```python
def alibi_bias(n_heads, seq_len):
    # slope_h = 2 ** (-8 * h / n_heads) for h = 1..n_heads
    slopes = [2 ** (-8 * (h + 1) / n_heads) for h in range(n_heads)]
    bias = []
    for m in slopes:
        row = [[-m * abs(i - j) for j in range(seq_len)] for i in range(seq_len)]
        bias.append(row)
    return bias  # add to attention scores before softmax
```

加入`bias[h]`对于`(seq_len, seq_len)`注意力分数矩阵`h`接着是软max.

> 将`bias[h]`加入到头`h`的`(seq_len, seq_len)`上,然后软max.

### 步骤4:验证RoPE的相对距离属性

选择两个随机向量`a, b`旋转`(pos_a, pos_b)`然后,通过`(pos_a + k, pos_b + k)`两种点产品必须在浮点误差内匹配.该属性是RoPE的整点,它与绝对的偏移不变,只有相对差距才有意义.

> 选择两个随机向量`a, b`用`(pos_a, pos_b)`然后用它.`(pos_a + k, pos_b + k)`旋转. 两个点积在浮点差距范围内必须匹配. 这种属性就是RoPE的全部意义.

> **【拓展：位置编码的历史演进】**从 Vaswani (Vaswani) 2017 年的绝对正弦编码,到 GPT-2/3 的学习式位置嵌入,再到 RoPE (Rope) 2021 年和 ALiBi (Rope) 2022 年,位置编码经历了从"绝对位置"到"相对位置"的范式转变.RoPE 的成功是它不改变注意力架构,直接在 Q/K 旋转中编码相对位置,同时提供了长上下文扩展的清晰路径.

## 用它实现框架

托尔奇2.5+ 运输了RoPE公用品`torch.nn.functional`生产代码的大部分使用`flash_attn`或`xformers`在注意内核内应用RoPE.

> 火 2.5+ 在`torch.nn.functional`中内置了RoPE工具──大多数生产代码使用`flash_attn`或`xformers`它们中的Rope在注意力内核内部应用中.

```python
from transformers import AutoModel
model = AutoModel.from_pretrained("meta-llama/Llama-3.2-3B")
# model.config.rope_scaling → {"type": "yarn", "factor": 32.0, "original_max_position_embeddings": 8192}
```

**Long-context tricks in 2026:**

> **2026 年的长上下文技巧：**

- **NTK-aware interpolation.**重新扩展`base`为了`base * (scale_factor)^(d/(d-2))`在4K到16K+的时间内.
  **NTK-aware 插值。**当从4K扩展到16K+时,将`base`重新缩放为`base * (scale_factor)^(d/(d-2))`,我知道.
- **YaRN.**智能的插射,可以在长度的环境中保持注意力缩.
  **YaRN。**更智能插值,保留长上下文上的注意力.
- **LongRoPE.**微软的2024方法,使用进化搜索来选择每维度尺度的因素.
  **LongRoPE。**微软2024年方法,使用进化搜索选择每维度缩小因子――Phi-3-Long 使用它――
- **Position interpolation + fine-tuning.**只是缩小位置,扩展因素, 调整15B代币.
  **位置插值 + 微调。**只有按扩展因子缩小位置并微调1-5B代币.

## 运送它.

看到`outputs/skill-positional-encoding-picker.md`技能选择一个新模型编码策略,考虑到目标背景长度,外分需求和培训预算.

> 参见`outputs/skill-positional-encoding-picker.md`△该技能为新模型选择编码策略,给定目标下文长度,外推需求和训练预算.

## 练习题

1. **Easy / 简单。**绘制一个突形图`PE`作为热图的矩阵`max_len=512, d=128`确认"随着尺寸指数的增长,条纹变得更宽".
   将正弦`PE`矩阵绘制为`max_len=512, d=128`热力图――确认"随着尺寸索引增长条纹变宽"的模式――

2. **Medium / 中等。**运行NTK知性ROPE扩展. 训练一个小的LM在长度256的序列,然后测试在长度1024的与没有扩展. 测量困难.
   实现NTK意识的ROPE缩放――在长度256的序列上训练一个微型LM,然后在有缩放和无缩放的情况下测试长度1024――测量困惑度――

3. **Hard / 困难。**运用 ALiBi 和 RoPE 在同一注意力模块中. 训练一个4层变压器在长度512的序列复制任务上. 在测试时,将其推移到2048年. 进行降解比较.
   在同一注意力模块中实现ALiBi和RoPE──在序列长度512的复制任务上训练一个4层变压器──在测试时推出到2048──比较退化程度──

## 关键词 快速查找表

| Term | What people say / 人们怎么说 | What it actually means / 实际含义 |
|------|------------------------------|----------------------------------|
| Positional encoding / 位置编码 | "Tells attention about order" / "告诉注意力顺序" | Any signal added to embeddings or attention that encodes position. 添加到嵌入或注意力中编码位置的任何信号。 |
| Sinusoidal / 正弦编码 | "The original one" / "原始的那种" | `sin/cos` at geometric frequencies added to embeddings; doesn't extrapolate. 以几何频率加到嵌入上的 `sin/cos`；不能外推。 |
| RoPE | "Rotary embeddings" / "旋转嵌入" | Rotate Q, K by position-dependent angle; dot product encodes relative distance. 按位置相关角度旋转 Q、K；点积编码相对距离。 |
| ALiBi | "Linear bias trick" / "线性偏置技巧" | Add `-m·|i-j|` to attention scores; no embedding needed, great extrapolation. 向注意力分数添加 `-m·|i-j|`；无需嵌入，出色的外推。 |
| base | "RoPE's knob" / "RoPE 的旋钮" | The frequency scaler in RoPE; increase to extend context at inference. RoPE 中的频率缩放器；增大以在推理时扩展上下文。 |
| NTK-aware | "A RoPE scaling trick" / "RoPE 缩放技巧" | Rescale `base` so high-frequency dims aren't squeezed when context expands. 重新缩放 `base` 使高频维度在上下文扩展时不被挤压。 |
| YaRN | "The fancy one" / "高级的那种" | Per-dimension interpolation+extrapolation that preserves attention entropy. 保留注意力熵的每维度插值+外推。 |
| Extrapolation / 外推 | "Works beyond trained length" / "超过训练长度还能用" | Can the position scheme serve correct output past `max_len` seen in training? 位置方案能否在训练中见过的 `max_len` 之后提供正确的输出？ |

## 继续阅读 继续阅读

- [Vaswani et al. (2017). Attention Is All You Need §3.5](https://arxiv.org/abs/1706.03762)原始的鼻状.
  瓦斯瓦尼等 (Vaswani) 于2017年

- [Su et al. (2021). RoFormer: Enhanced Transformer with Rotary Position Embedding](https://arxiv.org/abs/2104.09864)    纸
  其他2021年)  RoPE 论文。

- [Press, Smith, Lewis (2021). Train Short, Test Long: Attention with Linear Biases Enables Input Length Extrapolation](https://arxiv.org/abs/2108.12409)  
  报道,史密斯,路易斯,2021年

- [Peng et al. (2023). YaRN: Efficient Context Window Extension of Large Language Models](https://arxiv.org/abs/2309.00071)最新的ROPE扩展.
   等人 (2023)  最先进的RoPE缩放

- [Chen et al. (2023). Extending Context Window of Large Language Models via Positional Interpolation](https://arxiv.org/abs/2306.15595)Meta的Llama2长文本论文.
  陈等人(2023)  Meta 的拉马 2 长上下文论文──

- [Ding et al. (2024). LongRoPE: Extending LLM Context Window Beyond 2 Million Tokens](https://arxiv.org/abs/2402.13753)微软使用的方法 Phi-3-Long.
  微软的方法,被 Phi-3-Long 使用.

- [HuggingFace Transformers — `modeling_rope_utils.py`](https://github.com/huggingface/transformers/blob/main/src/transformers/modeling_rope_utils.py)每项ROPE扩展方案的生产级实施.
  拥抱面孔变压器 所有 RoPE 缩放方案的生产阶段实现
