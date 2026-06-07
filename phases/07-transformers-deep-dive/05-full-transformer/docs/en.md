# The Full Transformer — Encoder + Decoder | 完整 Transformer — 编码器 + 解码器

> Attention is the star. Everything else — residuals, normalization, feed-forward, cross-attention — is the scaffolding that lets you stack it deep.

> **【中文解读】** 把 Self-Attention、Multi-Head、FFN、Residual、LayerNorm 组装成完整的 Transformer。这是 Attention Is All You Need 论文的实现。

**Type:** Build
**Languages:** Python
**Prerequisites:** Phase 7 · 02 (Self-Attention), Phase 7 · 03 (Multi-Head Attention), Phase 7 · 04 (Positional Encoding)
**Time:** ~75 minutes

## The Problem

A single attention layer is a feature extractor, not a model. One matmul per layer is not enough capacity for language. You need depth — and depth breaks without the right plumbing.

The 2017 Vaswani paper packaged six design decisions that turned one attention layer into a stackable block. Every transformer since — encoder-only (BERT), decoder-only (GPT), encoder-decoder (T5) — inherits the same skeleton. In 2026 the blocks have been refined (RMSNorm, SwiGLU, pre-norm, RoPE) but the skeleton is identical.

This lesson is the skeleton. Next lessons specialize it — 06 for encoders, 07 for decoders, 08 for encoder-decoder.

> **【中文解读】** 单个注意力层只是特征提取器，不是完整的模型。Transformer 的核心在于将注意力堆叠成深层网络。2017 年 Vaswani 论文提出了六个关键设计决策——嵌入+位置信号、自注意力、前馈网络、残差连接、层归一化、交叉注意力——将单层注意力变成了可堆叠的模块。2026 年的变体（RMSNorm、SwiGLU、pre-norm、RoPE）只是替换了组件，骨架完全一致。

## The Concept

![Encoder and decoder block internals, wired](../assets/full-transformer.svg)

### The six pieces

1. **Embedding + positional signal.** Tokens → vectors. Position injected via RoPE (modern) or sinusoidal (classic).
2. **Self-attention.** Every position attends to every other. Masked in decoders.
3. **Feed-forward network (FFN).** Position-wise two-layer MLP: `W_2 · activation(W_1 · x)`. Expansion ratio 4× by default.
4. **Residual connection.** `x + sublayer(x)`. Without this, gradients vanish past ~6 layers.
5. **Layer normalization.** `LayerNorm` or `RMSNorm` (modern). Stabilizes the residual stream.
6. **Cross-attention (decoder only).** Queries come from the decoder, keys and values from the encoder output.

### Encoder block (used by BERT, T5 encoder)

```
x → LN → MHA(self) → + → LN → FFN → + → out
                     ^              ^
                     |              |
                     └── residual ──┘
```

Encoder is bidirectional. No masking. All positions see all positions.

### Decoder block (used by GPT, T5 decoder)

```
x → LN → MHA(masked self) → + → LN → MHA(cross to encoder) → + → LN → FFN → + → out
```

Decoder has three sublayers per block. The middle one — cross-attention — is the only place information flows from encoder to decoder. In a pure decoder-only architecture (GPT), cross-attention is omitted and you just have masked self-attention + FFN.

### Pre-norm vs post-norm

Original paper: `x + sublayer(LN(x))` vs `LN(x + sublayer(x))`. Post-norm lost favor around 2019 — it is harder to train deeply without careful warmup. Pre-norm (`LN` *before* sublayer) is the 2026 default: Llama, Qwen, GPT-3+, Mistral all use it.

### The 2026 modernized block

Vaswani 2017 shipped LayerNorm + ReLU. Modern stacks replaced both. What production blocks actually look like:

| Component | 2017 | 2026 |
|-----------|------|------|
| Normalization | LayerNorm | RMSNorm |
| FFN activation | ReLU | SwiGLU |
| FFN expansion | 4× | 2.6× (SwiGLU uses three matrices, total params match) |
| Position | Sinusoidal absolute | RoPE |
| Attention | Full MHA | GQA (or MLA) |
| Bias terms | Yes | No |

RMSNorm drops the mean-centering of LayerNorm (one fewer subtraction), which saves compute and is empirically at least as stable. SwiGLU (`Swish(W1 x) ⊙ W3 x`) consistently outperforms ReLU/GELU FFN by ~0.5 point ppl in the Llama, PaLM and Qwen papers.

> **【中文解读】** 2017 到 2026 年的 Transformer 现代化演进：LayerNorm → RMSNorm（去掉均值中心化，节省计算）；ReLU → SwiGLU（三矩阵门控，困惑度降低约 0.5）；后归一化 → 前归一化（训练更稳定，无需预热技巧）；绝对正弦 → RoPE（相对位置编码）；全多头 → GQA/MLA（KV 缓存优化）；有偏置 → 无偏置。这些替换看似简单，但每一个都经过大量实验验证。

> **【拓展：为什么 Decoder-only 赢了语言任务】** 2026 年主流大模型（GPT、Llama、Claude、Qwen）全部采用 Decoder-only 架构。原因：1) 去掉编码器后参数利用更高效；2) 单向注意力计算图更简单，训练和推理都更快；3) 在足够规模下，Decoder-only 的理解能力不弱于 Encoder。编码器-解码器架构仍保留在翻译、语音识别等有明确"源序列"的任务中。

### Parameter count

For one block with `d_model = d` and FFN expansion `r`:

- MHA: `4 · d²` (Q, K, V, O projections)
- FFN (SwiGLU): `3 · d · (r · d)` ≈ `3rd²`
- Norms: negligible

At `d = 4096, r = 2.6, layers = 32` (roughly Llama 3 8B), total: `32 · (4·4096² + 3·2.6·4096²) ≈ 32 · (16 + 32) M = ~1.5B parameters per layer × 32 ≈ 7B` (plus embeddings and head). Matches published counts.

## Build It

### Step 1: the building blocks

Using the tiny `Matrix` class from Lesson 03 (copied to this file for independence):

- `layer_norm(x, eps=1e-5)` — subtract mean, divide by std.
- `rms_norm(x, eps=1e-6)` — divide by RMS. No mean subtraction.
- `gelu(x)` and `silu(x) * W3 x` (SwiGLU).
- `ffn_swiglu(x, W1, W2, W3)`.
- `encoder_block(x, params)` and `decoder_block(x, enc_out, params)`.

See `code/main.py` for the full wiring.

### Step 2: wire a 2-layer encoder and a 2-layer decoder

Stack them. Pass the encoder output into every decoder cross-attention. Add a final LN before the output projection.

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

### Step 3: run forward on a toy example

Feed a 6-token source and a 5-token target through. Verify the output shape is `(5, vocab)`. No training — this lesson is about the architecture, not the loss.

### Step 4: swap in RMSNorm + SwiGLU

Replace LayerNorm and ReLU-FFN with RMSNorm and SwiGLU. Confirm shapes still match. This is the 2026 modernization with one function substitution.

## Use It

The PyTorch/TF reference implementations: `nn.TransformerEncoderLayer`, `nn.TransformerDecoderLayer`. But most 2026 production code rolls its own block because:

- Flash Attention is called inside attention, not via `nn.MultiheadAttention`.
- GQA / MLA are not in the stdlib reference.
- RoPE, RMSNorm, SwiGLU are not the PyTorch defaults.

HF `transformers` has clean reference blocks you should read: `modeling_llama.py` is the canonical 2026 decoder-only block. It's ~500 lines and worth walking through once.

**Encoder vs decoder vs encoder-decoder — when to pick:**

| Need | Pick | Example |
|------|------|---------|
| Classification, embeddings, QA over text | Encoder-only | BERT, DeBERTa, ModernBERT |
| Text generation, chat, code, reasoning | Decoder-only | GPT, Llama, Claude, Qwen |
| Structured input → structured output (translation, summarization) | Encoder-decoder | T5, BART, Whisper |

Decoder-only won language because it scales cleanest and handles both comprehension and generation. Encoder-decoder is still best when the input has a clear "source sequence" identity (translation, speech recognition, structured tasks).

## Ship It

See `outputs/skill-transformer-block-reviewer.md`. The skill reviews a new transformer block implementation against the 2026 defaults and flags missing pieces (pre-norm, RoPE, RMSNorm, GQA, FFN expansion ratio).

## Exercises

1. **Easy.** Count the parameters in your encoder_block at `d_model=512, n_heads=8, ffn_expansion=4, swiglu=True`. Validate by implementing the block and using `sum(p.numel() for p in block.parameters())`.
2. **Medium.** Switch from post-norm to pre-norm. Initialize both and measure the activation norm after 12 stacked layers on random input. Post-norm's activations should explode; pre-norm's should stay bounded.
3. **Hard.** Implement a 4-layer encoder-decoder on a toy copy task (copy `x` reversed). Train 100 steps. Report loss. Swap in RMSNorm + SwiGLU + RoPE — does loss drop?

## Key Terms

| Term | What people say | What it actually means | 中文释义 |
|------|-----------------|-----------------------|---------|
| Block | "One transformer layer" | Stack of norm + attention + norm + FFN, wrapped in residual connections. | Transformer 块——一个完整的编码/解码层 |
| Residual | "Skip connection" | `x + f(x)` output; enables gradient flow through deep stacks. | 残差连接——保证深层网络的梯度流通 |
| Pre-norm | "Normalize before, not after" | Modern: `x + sublayer(LN(x))`. Trains deeper without warmup gymnastics. | 前归一化——2026 年默认方案 |
| RMSNorm | "LayerNorm without the mean" | Divide by RMS; one less op, same empirical stability. | 均方根归一化——LayerNorm 的高效替代 |
| SwiGLU | "The FFN everyone switched to" | `Swish(W1 x) ⊙ W3 x → W2`. Beats ReLU/GELU on LM ppl. | SwiGLU 前馈网络——2026 年 FFN 标准 |
| Cross-attention | "How the decoder sees the encoder" | MHA with Q from decoder, K/V from encoder outputs. | 交叉注意力——解码器获取编码器信息的通道 |
| FFN expansion | "How wide the middle MLP is" | Ratio of hidden-size to d_model, usually 4 (LayerNorm) or 2.6 (SwiGLU). | FFN 扩展比——前馈网络中间层的宽度比 |
| Bias-free | "Drop the +b terms" | Modern stacks omit biases in linear layers; slight ppl improvement, smaller model. | 无偏置——现代模型去掉线性层偏置项 |

## Further Reading

- [Vaswani et al. (2017). Attention Is All You Need](https://arxiv.org/abs/1706.03762) — original block spec.
- [Xiong et al. (2020). On Layer Normalization in the Transformer Architecture](https://arxiv.org/abs/2002.04745) — why pre-norm beats post-norm deeply.
- [Zhang, Sennrich (2019). Root Mean Square Layer Normalization](https://arxiv.org/abs/1910.07467) — RMSNorm.
- [Shazeer (2020). GLU Variants Improve Transformer](https://arxiv.org/abs/2002.05202) — the SwiGLU paper.
- [HuggingFace `modeling_llama.py`](https://github.com/huggingface/transformers/blob/main/src/transformers/models/llama/modeling_llama.py) — canonical 2026 decoder-only block.
