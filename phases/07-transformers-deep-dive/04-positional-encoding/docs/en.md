# Positional Encoding — Sinusoidal, RoPE, ALiBi
# 位置编码 — 正弦、RoPE、ALiBi

> Attention is permutation-invariant. "The cat sat on the mat" and "mat the on sat cat the" produce the same output without positional signal. Three algorithms fix it — each with a different bet on what "position" means.

> 注意力是排列不变的。"The cat sat on the mat" 和 "mat the on sat cat the" 在没有位置信号时产生相同的输出。三种算法修复了这个问题——每种对"位置"的含义有不同的押注。

> **【中文解读】** Transformer 没有位置信息，需要手动注入。RoPE 是 Llama 使用的方法，ALiBi 支持外推到更长序列。

**Type:** Build | **类型:** 动手
**Language:** Python | **语言:** Python
**Prerequisites:** Phase 7 · 02 (Self-Attention), Phase 7 · 03 (Multi-Head Attention) | **前置知识:** 阶段 7 · 02（自注意力），阶段 7 · 03（多头注意力）
**Time:** ~45 minutes | **时间:** ~45 分钟

## The Problem | 问题引入

Scaled dot-product attention is order-blind. The attention matrix `softmax(Q K^T / √d) V` is computed from pairwise similarities. Shuffle the rows of `X`, get the rows of the output shuffled the same way. Nothing inside attention cares about position.

> 缩放点积注意力是顺序无关的。注意力矩阵 `softmax(Q K^T / √d) V` 由成对相似度计算而来。打乱 `X` 的行，输出的行会以相同方式被打乱。注意力内部没有任何东西关心位置。

That is not a bug in a bag-of-words model. For language, code, audio, video — anything where order carries meaning — it is fatal.

> 在词袋模型中这不是 bug。但对于语言、代码、音频、视频——任何顺序承载意义的事物——这是致命的。

The fix is to inject position into the embeddings somehow. Three eras of answers:

> 修复方法是以某种方式将位置注入嵌入。三个时代的答案：

1. **Absolute sinusoidal** (Vaswani 2017). Add `sin/cos` of position to the embedding. Simple, learnable-free, extrapolates poorly beyond trained lengths.
   **绝对正弦编码**（Vaswani 2017）。将位置的 `sin/cos` 加到嵌入上。简单、无需学习、在训练长度之外外推能力差。

2. **RoPE — Rotary Position Embeddings** (Su 2021). Rotate Q and K vectors by an angle proportional to position. Encodes *relative* position directly in the dot product. Dominant in 2026.
   **RoPE — 旋转位置嵌入**（Su 2021）。按与位置成正比的角度旋转 Q 和 K 向量。直接在点积中编码*相对*位置。2026 年占主导地位。

3. **ALiBi — Attention with Linear Biases** (Press 2022). Skip embeddings entirely; add a per-head linear penalty to attention scores based on distance. Excellent length extrapolation.
   **ALiBi — 带线性偏置的注意力**（Press 2022）。完全跳过嵌入；根据距离向注意力分数添加每个头的线性惩罚。出色的长度外推。

As of 2026, essentially every frontier open model uses RoPE: Llama 2/3/4, Qwen 2/3, Mistral, Mixtral, DeepSeek-V3, Kimi. A handful of long-context models use ALiBi or its modern variants. Absolute sinusoidal is historical.

> 截至 2026 年，基本上每个前沿开源模型都使用 RoPE：Llama 2/3/4、Qwen 2/3、Mistral、Mixtral、DeepSeek-V3、Kimi。少数长上下文模型使用 ALiBi 或其现代变体。绝对正弦编码已成为历史。

> **【中文解读】** 自注意力本身是排列不变的——打乱输入顺序，输出只是对应打乱。这对语言是致命的。三种位置编码方案代表了三个时代：(1) 绝对正弦编码——简单但外推差；(2) RoPE——通过旋转编码相对位置，2026 年主流；(3) ALiBi——直接对注意力分数加距离偏置，外推能力最强。

## The Concept | 核心概念

![Sinusoidal absolute vs RoPE rotations vs ALiBi distance bias](../assets/positional-encoding.svg)

### Absolute sinusoidal | 绝对正弦编码

Pre-compute a fixed matrix `PE` of shape `(max_len, d_model)`:

> 预计算一个固定矩阵 `PE`，形状为 `(max_len, d_model)`：

```
PE[pos, 2i]   = sin(pos / 10000^(2i / d_model))
PE[pos, 2i+1] = cos(pos / 10000^(2i / d_model))
```

Then `X' = X + PE[:N]` before attention. Each dimension is a sinusoid at a different frequency. The model learns to read position from the phase pattern. Fails beyond `max_len`: nothing told the model what happens at position 2048 when it only saw positions 0–2047.

> 然后在注意力前 `X' = X + PE[:N]`。每个维度是不同频率的正弦波。模型学会从相位模式中读取位置。在 `max_len` 之外失效：模型只见过位置 0-2047 时，没有任何东西告诉它在位置 2048 会发生什么。

### RoPE | 旋转位置嵌入

Rotate the Q and K vectors (not embeddings). For a pair of dimensions `(2i, 2i+1)`:

> 旋转 Q 和 K 向量（不是嵌入）。对于一对维度 `(2i, 2i+1)`：

```
[q'_2i    ]   [ cos(pos·θ_i)  -sin(pos·θ_i) ] [q_2i   ]
[q'_2i+1  ] = [ sin(pos·θ_i)   cos(pos·θ_i) ] [q_2i+1 ]

θ_i = base^(-2i / d_head),  base = 10000 by default
```

Apply the same rotation to keys with position `pos_k`. The dot product `q'_m · k'_n` becomes a function of `(m - n)` alone. That is: **the attention score depends only on the relative distance**, even though the rotation was keyed off absolute positions. Beautiful trick.

> 对键应用位置 `pos_k` 的相同旋转。点积 `q'_m · k'_n` 变成仅 `(m - n)` 的函数。也就是说：**注意力分数只取决于相对距离**，即使旋转是基于绝对位置的。绝妙的技巧。

> **【中文解读】** RoPE 的精妙之处：虽然旋转角度基于绝对位置，但 Q·K 的点积只取决于相对距离 (m-n)。这意味着模型自然地学会了相对位置关系。调整 base 参数还可以实现长上下文外推，Llama 3 正是通过这种方式从 8K 扩展到 128K 上下文。

> **【拓展：RoPE 在 Llama 3 中的长上下文扩展】** Llama 3 通过 YaRN（Yet another RoPE extensioN）方法将上下文从 8K 扩展到 128K。核心思路是调整 RoPE 的 base 频率，使高频维度保持原始分辨率，低频维度进行插值。这种"分维度处理"策略既保持了短距离的精确位置感知，又扩展了长距离的外推能力。

Extending RoPE: `base` can be scaled (NTK-aware, YaRN, LongRoPE) to extrapolate to longer contexts without retraining. Llama 3 extended from 8K to 128K context this way.

> 扩展 RoPE：`base` 可以被缩放（NTK-aware、YaRN、LongRoPE）以在不重新训练的情况下外推到更长的上下文。Llama 3 就是这样从 8K 扩展到 128K 上下文的。

### ALiBi | 带线性偏置的注意力

Skip the embedding trick. Bias the attention scores directly:

> 跳过嵌入技巧。直接偏置注意力分数：

```
attn_score[i, j] = (q_i · k_j) / √d  -  m_h · |i - j|
```

Where `m_h` is a head-specific slope (e.g. `1 / 2^(8·h/H)`). Closer tokens get boosted; far tokens get penalized. No training-time cost. The paper shows length extrapolation beats sinusoidal and matches RoPE on its original trained length.

> 其中 `m_h` 是特定于头的斜率（例如 `1 / 2^(8·h/H)`）。更近的 token 被提升；更远的 token 被惩罚。没有训练时的额外成本。论文显示长度外推超过正弦编码，在其原始训练长度上与 RoPE 匹配。

### What to pick in 2026 | 2026 年选什么

| Variant / 变体 | Extrapolation / 外推能力 | Training cost / 训练成本 | Used by / 使用者 |
|---------|---------------|---------------|---------|
| Absolute sinusoidal / 绝对正弦编码 | poor / 差 | free / 免费 | original transformer, early BERT |
| Learned absolute / 学习式绝对编码 | none / 无 | tiny / 微小 | GPT-2, GPT-3 |
| RoPE | good with scaling / 良好（带缩放） | free / 免费 | Llama 2/3/4, Qwen 2/3, Mistral, DeepSeek-V3, Kimi |
| RoPE + YaRN | excellent / 优秀 | fine-tune stage / 微调阶段 | Qwen2-1M, Llama 3.1 128K |
| ALiBi | excellent / 优秀 | free / 免费 | BLOOM, MPT, Baichuan |

RoPE won because it slots into attention without changing the architecture, encodes relative position, and its `base` hyperparameter gives a clean knob for long-context fine-tuning.

> RoPE 胜出是因为它无需改变架构即可插入注意力、编码相对位置，并且其 `base` 超参数为长上下文微调提供了清晰的调节旋钮。

> **【中文解读】** 2026 年位置编码的选择很明确：新项目默认 RoPE。它不改变架构、编码相对位置、且通过 base 参数提供了长上下文微调的清晰路径。只有在极端外推场景（训练 4K、推理 1M）才考虑 ALiBi。

> **【拓展：位置编码对长上下文 RAG 的影响】** 在 RAG（检索增强生成）系统中，位置编码直接影响长文档处理能力。RoPE + YaRN 让 Llama 3 能处理 128K token 的上下文，这意味着可以一次性处理约 300 页文档。位置编码方案的选择决定了 RAG 系统是否需要复杂的分块策略。

## Build It | 动手实现

### Step 1: Sinusoidal encoding | 步骤 1：正弦编码

See `code/main.py`. A 4-line computation:

> 参见 `code/main.py`。4 行计算：

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

Add this to the embedding matrix before the first attention layer.

> 在第一个注意力层之前将此加到嵌入矩阵上。

### Step 2: RoPE applied to Q, K | 步骤 2：将 RoPE 应用于 Q、K

RoPE operates in-place on Q and K. For each pair of dims:

> RoPE 对 Q 和 K 原地操作。对每一对维度：

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

Crucial: apply the same function to Q at position `m` and K at position `n`. Their dot product picks up a `cos((m-n)·θ_i)` factor on every coordinate pair. Attention learns relative position for free.

> 关键：对位置 `m` 的 Q 和位置 `n` 的 K 应用相同函数。它们的点积在每个坐标对上获得一个 `cos((m-n)·θ_i)` 因子。注意力免费学习了相对位置。

> **【中文解读】** RoPE 的实现核心：对 Q 和 K 的每一对维度 (2i, 2i+1) 做位置相关的旋转。旋转角度与位置成正比，因此 Q_m · K_n 的点积中会出现 cos((m-n)*theta) 项，自然编码了相对距离。

### Step 3: ALiBi slopes and bias | 步骤 3：ALiBi 斜率和偏置

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

Add `bias[h]` to the `(seq_len, seq_len)` attention score matrix of head `h`, then softmax.

> 将 `bias[h]` 加到头 `h` 的 `(seq_len, seq_len)` 注意力分数矩阵上，然后 softmax。

### Step 4: Verify relative-distance property of RoPE | 步骤 4：验证 RoPE 的相对距离属性

Pick two random vectors `a, b`. Rotate by `(pos_a, pos_b)`. Then by `(pos_a + k, pos_b + k)`. Both dot products must match within floating-point error. That property is the whole point of RoPE — it is invariant to the absolute offset, only the relative gap matters.

> 选择两个随机向量 `a, b`。用 `(pos_a, pos_b)` 旋转。然后用 `(pos_a + k, pos_b + k)` 旋转。两个点积在浮点误差范围内必须匹配。这个属性就是 RoPE 的全部意义——它对绝对偏移不变，只有相对差距重要。

> **【拓展：位置编码的历史演进】** 从 Vaswani（2017）的绝对正弦编码，到 GPT-2/3 的学习式位置嵌入，再到 RoPE（2021）和 ALiBi（2022），位置编码经历了从"绝对位置"到"相对位置"的范式转变。RoPE 的成功在于它不改变注意力架构，直接在 Q/K 旋转中编码相对位置，同时提供了长上下文扩展的清晰路径。

## Use It | 用框架实现

PyTorch 2.5+ ships RoPE utilities in `torch.nn.functional`. Most production code uses `flash_attn` or `xformers` where RoPE is applied inside the attention kernel.

> PyTorch 2.5+ 在 `torch.nn.functional` 中内置了 RoPE 工具。大多数生产代码使用 `flash_attn` 或 `xformers`，其中 RoPE 在注意力内核内部应用。

```python
from transformers import AutoModel
model = AutoModel.from_pretrained("meta-llama/Llama-3.2-3B")
# model.config.rope_scaling → {"type": "yarn", "factor": 32.0, "original_max_position_embeddings": 8192}
```

**Long-context tricks in 2026:**

> **2026 年的长上下文技巧：**

- **NTK-aware interpolation.** Rescale `base` to `base * (scale_factor)^(d/(d-2))` when extending from 4K to 16K+.
  **NTK-aware 插值。** 当从 4K 扩展到 16K+ 时，将 `base` 重新缩放为 `base * (scale_factor)^(d/(d-2))`。
- **YaRN.** Smarter interpolation that preserves attention entropy on long contexts. Llama 3.1 128K uses it.
  **YaRN。** 更智能的插值，保留长上下文上的注意力熵。Llama 3.1 128K 使用它。
- **LongRoPE.** Microsoft's 2024 method that uses evolutionary search to pick per-dimension scale factors. Phi-3-Long uses it.
  **LongRoPE。** Microsoft 2024 年的方法，使用进化搜索选择每维度缩放因子。Phi-3-Long 使用它。
- **Position interpolation + fine-tuning.** Just shrink positions by the extension factor and fine-tune for 1–5B tokens. Surprisingly effective.
  **位置插值 + 微调。** 只需按扩展因子缩小位置并微调 1-5B token。效果惊人。

## Ship It | 产出物

See `outputs/skill-positional-encoding-picker.md`. The skill picks an encoding strategy for a new model given target context length, extrapolation needs, and training budget.

> 参见 `outputs/skill-positional-encoding-picker.md`。该技能为新模型选择编码策略，给定目标上下文长度、外推需求和训练预算。

## Exercises | 练习题

1. **Easy / 简单。** Plot the sinusoidal `PE` matrix as a heatmap for `max_len=512, d=128`. Confirm the "stripes get wider as dimension index grows" pattern.
   将正弦 `PE` 矩阵绘制为 `max_len=512, d=128` 的热力图。确认"随维度索引增长条纹变宽"的模式。

2. **Medium / 中等。** Implement NTK-aware RoPE scaling. Train a tiny LM on sequences of length 256, then test on length 1024 with and without scaling. Measure perplexity.
   实现 NTK-aware RoPE 缩放。在长度 256 的序列上训练一个微型 LM，然后在有缩放和无缩放的情况下测试长度 1024。测量困惑度。

3. **Hard / 困难。** Implement ALiBi and RoPE in the same attention module. Train a 4-layer transformer on a copy task with sequences of length 512. Extrapolate to 2048 at test time. Compare degradation.
   在同一个注意力模块中实现 ALiBi 和 RoPE。在序列长度 512 的复制任务上训练一个 4 层 Transformer。在测试时外推到 2048。比较退化程度。

## Key Terms | 术语速查表

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

## Further Reading | 延伸阅读

- [Vaswani et al. (2017). Attention Is All You Need §3.5](https://arxiv.org/abs/1706.03762) — original sinusoidal.
  Vaswani 等人（2017）— 原始正弦编码。

- [Su et al. (2021). RoFormer: Enhanced Transformer with Rotary Position Embedding](https://arxiv.org/abs/2104.09864) — RoPE paper.
  Su 等人（2021）— RoPE 论文。

- [Press, Smith, Lewis (2021). Train Short, Test Long: Attention with Linear Biases Enables Input Length Extrapolation](https://arxiv.org/abs/2108.12409) — ALiBi.
  Press, Smith, Lewis（2021）— ALiBi。

- [Peng et al. (2023). YaRN: Efficient Context Window Extension of Large Language Models](https://arxiv.org/abs/2309.00071) — state of the art RoPE scaling.
  Peng 等人（2023）— 最先进的 RoPE 缩放。

- [Chen et al. (2023). Extending Context Window of Large Language Models via Positional Interpolation](https://arxiv.org/abs/2306.15595) — Meta's Llama 2 long-context paper.
  Chen 等人（2023）— Meta 的 Llama 2 长上下文论文。

- [Ding et al. (2024). LongRoPE: Extending LLM Context Window Beyond 2 Million Tokens](https://arxiv.org/abs/2402.13753) — the Microsoft method used by Phi-3-Long.
  Ding 等人（2024）— Microsoft 的方法，被 Phi-3-Long 使用。

- [HuggingFace Transformers — `modeling_rope_utils.py`](https://github.com/huggingface/transformers/blob/main/src/transformers/modeling_rope_utils.py) — production-grade implementations of every RoPE scaling scheme.
  HuggingFace Transformers — 所有 RoPE 缩放方案的生产级实现。
