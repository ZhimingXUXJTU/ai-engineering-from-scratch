# The Full Transformer — Encoder + Decoder
# 完整 Transformer — 编码器 + 解码器

> Attention is the star. Everything else — residuals, normalization, feed-forward, cross-attention — is the scaffolding that lets you stack it deep.

> 注意力是主角。其他一切——残差连接、归一化、前馈网络、交叉注意力——都是让你能将其堆叠得更深的脚手架。

> **【中文解读】** 把 Self-Attention、Multi-Head、FFN、Residual、LayerNorm 组装成完整的 Transformer。这是 Attention Is All You Need 论文的实现。

**Type:** Build | **类型:** 动手
**Language:** Python | **语言:** Python
**Prerequisites:** Phase 7 · 02 (Self-Attention), Phase 7 · 03 (Multi-Head Attention), Phase 7 · 04 (Positional Encoding) | **前置知识:** 阶段 7 · 02（自注意力），阶段 7 · 03（多头注意力），阶段 7 · 04（位置编码）
**Time:** ~75 minutes | **时间:** ~75 分钟

## The Problem | 问题引入

A single attention layer is a feature extractor, not a model. One matmul per layer is not enough capacity for language. You need depth — and depth breaks without the right plumbing.

> 单个注意力层是特征提取器，不是模型。每层一次矩阵乘法不够语言的容量。你需要深度——而深度没有正确的管道会崩溃。

The 2017 Vaswani paper packaged six design decisions that turned one attention layer into a stackable block. Every transformer since — encoder-only (BERT), decoder-only (GPT), encoder-decoder (T5) — inherits the same skeleton. In 2026 the blocks have been refined (RMSNorm, SwiGLU, pre-norm, RoPE) but the skeleton is identical.

> 2017 年 Vaswani 论文打包了六个设计决策，将一个注意力层变成可堆叠的块。此后每个 Transformer——纯编码器（BERT）、纯解码器（GPT）、编码器-解码器（T5）——都继承了相同的骨架。2026 年，这些块已被优化（RMSNorm、SwiGLU、前归一化、RoPE），但骨架完全相同。

This lesson is the skeleton. Next lessons specialize it — 06 for encoders, 07 for decoders, 08 for encoder-decoder.

> 本课是骨架。接下来的课程专门化它——06 课讲编码器，07 课讲解码器，08 课讲编码器-解码器。

> **【中文解读】** 单个注意力层只是一个特征提取器，不是完整的模型。2017 年的论文将六个设计决策打包成可堆叠的块：嵌入+位置编码、自注意力、FFN、残差连接、层归一化、交叉注意力。所有后续 Transformer 变体——BERT、GPT、T5——都继承了相同的骨架。

## The Concept | 核心概念

![Encoder and decoder block internals, wired](../assets/full-transformer.svg)

### The six pieces | 六个组件

1. **Embedding + positional signal.** Tokens → vectors. Position injected via RoPE (modern) or sinusoidal (classic).
   **嵌入 + 位置信号。** Token → 向量。通过 RoPE（现代）或正弦编码（经典）注入位置。

2. **Self-attention.** Every position attends to every other. Masked in decoders.
   **自注意力。** 每个位置关注所有其他位置。解码器中使用掩码。

3. **Feed-forward network (FFN).** Position-wise two-layer MLP: `W_2 · activation(W_1 · x)`. Expansion ratio 4× by default.
   **前馈网络 (FFN)。** 位置级两层 MLP：`W_2 · activation(W_1 · x)`。默认扩展比 4×。

4. **Residual connection.** `x + sublayer(x)`. Without this, gradients vanish past ~6 layers.
   **残差连接。** `x + sublayer(x)`。没有这个，梯度在约 6 层后消失。

5. **Layer normalization.** `LayerNorm` or `RMSNorm` (modern). Stabilizes the residual stream.
   **层归一化。** `LayerNorm` 或 `RMSNorm`（现代）。稳定残差流。

6. **Cross-attention (decoder only).** Queries come from the decoder, keys and values from the encoder output.
   **交叉注意力（仅解码器）。** 查询来自解码器，键和值来自编码器输出。

### Encoder block (used by BERT, T5 encoder) | 编码器块

```
x → LN → MHA(self) → + → LN → FFN → + → out
                     ^              ^
                     |              |
                     └── residual ──┘
```

Encoder is bidirectional. No masking. All positions see all positions.

> 编码器是双向的。没有掩码。所有位置看到所有位置。

### Decoder block (used by GPT, T5 decoder) | 解码器块

```
x → LN → MHA(masked self) → + → LN → MHA(cross to encoder) → + → LN → FFN → + → out
```

Decoder has three sublayers per block. The middle one — cross-attention — is the only place information flows from encoder to decoder. In a pure decoder-only architecture (GPT), cross-attention is omitted and you just have masked self-attention + FFN.

> 解码器每块有三个子层。中间那个——交叉注意力——是信息从编码器流向解码器的唯一地方。在纯解码器架构（GPT）中，交叉注意力被省略，你只有掩码自注意力 + FFN。

### Pre-norm vs post-norm | 前归一化 vs 后归一化

Original paper: `x + sublayer(LN(x))` vs `LN(x + sublayer(x))`. Post-norm lost favor around 2019 — it is harder to train deeply without careful warmup. Pre-norm (`LN` *before* sublayer) is the 2026 default: Llama, Qwen, GPT-3+, Mistral all use it.

> 原始论文：`x + sublayer(LN(x))` vs `LN(x + sublayer(x))`。后归一化在 2019 年左右失宠——没有仔细预热就很难深度训练。前归一化（`LN` 在子层*之前*）是 2026 年的默认：Llama、Qwen、GPT-3+、Mistral 都使用它。

### The 2026 modernized block | 2026 年现代化块

| Component / 组件 | 2017 | 2026 |
|-----------|------|------|
| Normalization / 归一化 | LayerNorm | RMSNorm |
| FFN activation / FFN 激活函数 | ReLU | SwiGLU |
| FFN expansion / FFN 扩展比 | 4× | 2.6×（SwiGLU 使用三个矩阵，总参数匹配） |
| Position / 位置编码 | Sinusoidal absolute / 绝对正弦 | RoPE |
| Attention / 注意力 | Full MHA | GQA (or MLA) |
| Bias terms / 偏置项 | Yes / 有 | No / 无 |

RMSNorm drops the mean-centering of LayerNorm (one fewer subtraction), which saves compute and is empirically at least as stable. SwiGLU (`Swish(W1 x) ⊙ W3 x`) consistently outperforms ReLU/GELU FFN by ~0.5 point ppl in the Llama, PaLM and Qwen papers.

> RMSNorm 去掉了 LayerNorm 的均值中心化（少一次减法），节省了计算量，经验上至少同样稳定。SwiGLU（`Swish(W1 x) ⊙ W3 x`）在 Llama、PaLM 和 Qwen 论文中一致地比 ReLU/GELU FFN 好约 0.5 个困惑度点。

> **【中文解读】** 2026 年的现代 Transformer 块与 2017 年原版相比：LayerNorm→RMSNorm，ReLU→SwiGLU，后归一化→前归一化，绝对位置编码→RoPE，全多头注意力→GQA。每一项改进都是渐进的，但组合起来显著提升了训练稳定性和模型质量。

> **【拓展：为什么 Decoder-only 成为主流】** 虽然编码器-解码器架构在翻译等任务上有天然优势，但 Decoder-only 模型（GPT、Llama）在扩展性和通用性上更胜一筹。它可以用同一架构处理理解和生成任务，训练目标统一（下一个 token 预测），且扩展性已被 Chinchilla 定律验证。这正是 2024-2026 年几乎所有前沿大模型选择 Decoder-only 的原因。

### Parameter count | 参数量

For one block with `d_model = d` and FFN expansion `r`:

> 对于一个 `d_model = d` 且 FFN 扩展比为 `r` 的块：

- MHA: `4 · d²` (Q, K, V, O projections)
  MHA：`4 · d²`（Q、K、V、O 投影）
- FFN (SwiGLU): `3 · d · (r · d)` ≈ `3rd²`
  FFN（SwiGLU）：`3 · d · (r · d)` ≈ `3rd²`
- Norms: negligible
  归一化：可忽略

> **【拓展：参数计数与模型规模的实际意义】** Transformer 的参数主要集中在注意力投影（4d^2）和 FFN（约 8d^2 for SwiGLU）中。Llama 3 8B 每层约 1.5B 参数，32 层共约 7B 加上嵌入层和输出头。理解参数分布有助于优化：MoE 替换 FFN 可以增加总参数而不增加活跃计算；量化（如 GPTQ、AWQ）主要压缩 FFN 权重。

## Build It | 动手实现

### Step 1: The building blocks | 步骤 1：构建模块

Using the tiny `Matrix` class from Lesson 03 (copied to this file for independence):

> 使用第 03 课中的微型 `Matrix` 类（已复制到此文件以保持独立）：

- `layer_norm(x, eps=1e-5)` — subtract mean, divide by std.
  `layer_norm(x, eps=1e-5)` — 减去均值，除以标准差。
- `rms_norm(x, eps=1e-6)` — divide by RMS. No mean subtraction.
  `rms_norm(x, eps=1e-6)` — 除以 RMS。不减均值。
- `gelu(x)` and `silu(x) * W3 x` (SwiGLU).
  `gelu(x)` 和 `silu(x) * W3 x`（SwiGLU）。
- `ffn_swiglu(x, W1, W2, W3)`.
- `encoder_block(x, params)` and `decoder_block(x, enc_out, params)`.

### Step 2: Wire a 2-layer encoder and a 2-layer decoder | 步骤 2：连接 2 层编码器和 2 层解码器

Stack them. Pass the encoder output into every decoder cross-attention. Add a final LN before the output projection.

> 堆叠它们。将编码器输出传入每个解码器交叉注意力。在输出投影前添加最终 LN。

```python
def encode(tokens, params):
    x = embed(tokens, params.emb) + sinusoidal(len(tokens), params.d)
    for block in params.encoder_blocks:
        x = encoder_block(x, block)
    return x

def decode(target_tokens, encoder_out, params):
    x = embed(target_tokens, params.emb) + sinusoidal(len(target_tokens), params.d)
    for block in params.decoder_blocks:
        x = decoder_block(x, encoder_out, block)
    return x
```

### Step 3: Run forward on a toy example | 步骤 3：在玩具示例上运行前向传播

Feed a 6-token source and a 5-token target through. Verify the output shape is `(5, vocab)`. No training — this lesson is about the architecture, not the loss.

> 输入 6 个 token 的源和 5 个 token 的目标。验证输出形状是 `(5, vocab)`。不训练——本课关注架构，不关注损失。

### Step 4: Swap in RMSNorm + SwiGLU | 步骤 4：替换为 RMSNorm + SwiGLU

Replace LayerNorm and ReLU-FFN with RMSNorm and SwiGLU. Confirm shapes still match. This is the 2026 modernization with one function substitution.

> 用 RMSNorm 和 SwiGLU 替换 LayerNorm 和 ReLU-FFN。确认形状仍然匹配。这是通过一次函数替换实现的 2026 年现代化。

## Use It | 用框架实现

The PyTorch/TF reference implementations: `nn.TransformerEncoderLayer`, `nn.TransformerDecoderLayer`. But most 2026 production code rolls its own block because:

> PyTorch/TF 参考实现：`nn.TransformerEncoderLayer`、`nn.TransformerDecoderLayer`。但大多数 2026 年的生产代码自建块，因为：

- Flash Attention is called inside attention, not via `nn.MultiheadAttention`.
  Flash Attention 在注意力内部调用，不通过 `nn.MultiheadAttention`。
- GQA / MLA are not in the stdlib reference.
  GQA / MLA 不在标准库参考中。
- RoPE, RMSNorm, SwiGLU are not the PyTorch defaults.
  RoPE、RMSNorm、SwiGLU 不是 PyTorch 的默认值。

**Encoder vs decoder vs encoder-decoder — when to pick:**

> **编码器 vs 解码器 vs 编码器-解码器——何时选择：**

| Need / 需求 | Pick / 选择 | Example / 示例 |
|------|------|---------|
| Classification, embeddings, QA over text / 分类、嵌入、文本 QA | Encoder-only / 纯编码器 | BERT, DeBERTa, ModernBERT |
| Text generation, chat, code, reasoning / 文本生成、聊天、代码、推理 | Decoder-only / 纯解码器 | GPT, Llama, Claude, Qwen |
| Structured input → structured output (translation, summarization) / 结构化转换 | Encoder-decoder / 编码器-解码器 | T5, BART, Whisper |

> **【中文解读】** 三种架构的选择：Encoder-only（BERT）适合分类和嵌入；Decoder-only（GPT/Llama）适合生成和通用任务；Encoder-Decoder（T5/BART）适合有明确"源序列"的结构化转换任务。2026 年的主流选择是 Decoder-only，因为它的扩展性最好、训练最简洁。

> **【拓展：SwiGLU 为何优于 ReLU】** SwiGLU（Swish-Gated Linear Unit）通过门控机制让 FFN 的表达能力更强。Llama、PaLM、Qwen 等模型的实验一致表明 SwiGLU 比 ReLU/GELU 在语言建模困惑度上低约 0.5 个点。虽然它需要三个权重矩阵而非两个（参数量增加 50%），但通常通过将扩展比从 4x 降到 2.6x 来补偿。

## Ship It | 产出物

See `outputs/skill-transformer-block-reviewer.md`. The skill reviews a new transformer block implementation against the 2026 defaults and flags missing pieces (pre-norm, RoPE, RMSNorm, GQA, FFN expansion ratio).

> 参见 `outputs/skill-transformer-block-reviewer.md`。该技能根据 2026 年默认设置审查新的 Transformer 块实现，并标记缺失的部分。

## Exercises | 练习题

1. **Easy / 简单。** Count the parameters in your encoder_block at `d_model=512, n_heads=8, ffn_expansion=4, swiglu=True`. Validate by implementing the block and using `sum(p.numel() for p in block.parameters())`.
   计算 `d_model=512, n_heads=8, ffn_expansion=4, swiglu=True` 时 encoder_block 的参数量。通过实现块并使用 `sum(p.numel() for p in block.parameters())` 验证。

2. **Medium / 中等。** Switch from post-norm to pre-norm. Initialize both and measure the activation norm after 12 stacked layers on random input. Post-norm's activations should explode; pre-norm's should stay bounded.
   从后归一化切换到前归一化。初始化两者并测量 12 个堆叠层在随机输入上的激活范数。后归一化的激活应该爆炸；前归一化的应该保持有界。

3. **Hard / 困难。** Implement a 4-layer encoder-decoder on a toy copy task (copy `x` reversed). Train 100 steps. Report loss. Swap in RMSNorm + SwiGLU + RoPE — does loss drop?
   在玩具复制任务（反转复制 `x`）上实现 4 层编码器-解码器。训练 100 步。报告损失。替换为 RMSNorm + SwiGLU + RoPE——损失是否下降？

## Key Terms | 术语速查表

| Term | What people say / 人们怎么说 | What it actually means / 实际含义 |
|------|------------------------------|----------------------------------|
| Block / 块 | "One transformer layer" / "一个 Transformer 层" | Stack of norm + attention + norm + FFN, wrapped in residual connections. 归一化 + 注意力 + 归一化 + FFN 的堆叠，包裹在残差连接中。 |
| Residual / 残差连接 | "Skip connection" / "跳跃连接" | `x + f(x)` output; enables gradient flow through deep stacks. `x + f(x)` 输出；使梯度流能穿过深层堆叠。 |
| Pre-norm / 前归一化 | "Normalize before, not after" / "先归一化，不是后归一化" | Modern: `x + sublayer(LN(x))`. Trains deeper without warmup gymnastics. 现代：`x + sublayer(LN(x))`。无需预热技巧即可训练更深的网络。 |
| RMSNorm | "LayerNorm without the mean" / "没有均值的 LayerNorm" | Divide by RMS; one less op, same empirical stability. 除以 RMS；少一次操作，经验上同样稳定。 |
| SwiGLU | "The FFN everyone switched to" / "大家都换成的 FFN" | `Swish(W1 x) ⊙ W3 x → W2`. Beats ReLU/GELU on LM ppl. 在 LM 困惑度上击败 ReLU/GELU。 |
| Cross-attention / 交叉注意力 | "How the decoder sees the encoder" / "解码器如何看到编码器" | MHA with Q from decoder, K/V from encoder outputs. MHA 的 Q 来自解码器，K/V 来自编码器输出。 |
| FFN expansion / FFN 扩展比 | "How wide the middle MLP is" / "中间 MLP 有多宽" | Ratio of hidden-size to d_model, usually 4 or 2.6 (SwiGLU). 隐藏大小与 d_model 的比率，通常为 4 或 2.6（SwiGLU）。 |
| Bias-free / 无偏置 | "Drop the +b terms" / "去掉 +b 项" | Modern stacks omit biases in linear layers; slight ppl improvement, smaller model. 现代堆栈在线性层中省略偏置；轻微的困惑度改善，更小的模型。 |

## Further Reading | 延伸阅读

- [Vaswani et al. (2017). Attention Is All You Need](https://arxiv.org/abs/1706.03762) — original block spec.
  Vaswani 等人（2017）— 原始块规范。

- [Xiong et al. (2020). On Layer Normalization in the Transformer Architecture](https://arxiv.org/abs/2002.04745) — why pre-norm beats post-norm deeply.
  Xiong 等人（2020）— 为什么前归一化在深层中胜过后归一化。

- [Zhang, Sennrich (2019). Root Mean Square Layer Normalization](https://arxiv.org/abs/1910.07467) — RMSNorm.

- [Shazeer (2020). GLU Variants Improve Transformer](https://arxiv.org/abs/2002.05202) — the SwiGLU paper.
  Shazeer（2020）— SwiGLU 论文。

- [HuggingFace `modeling_llama.py`](https://github.com/huggingface/transformers/blob/main/src/transformers/models/llama/modeling_llama.py) — canonical 2026 decoder-only block.
  HuggingFace `modeling_llama.py` — 2026 年规范的纯解码器块。
