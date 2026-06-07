# Transformer Block from Scratch | Transformer 块

> One block is the unit of every modern decoder LLM. Layer norm, multi head attention, residual, MLP, residual. The pre-LN variant trains stably without warmup. The post-LN variant is what the original paper shipped. This lesson builds both, side by side, and shows which one survives a 12 layer stack at common learning rates.

> **【中文解读】** 本节是综合项目——实现 Transformer 块。


**Type:** Build | **类型:** Build
**Languages:** Python | **语言:** Python
**Prerequisites:** Phase 19 lessons 30 to 33 (tokenizer, embeddings, attention math, batched data loader) | **前置知识:** Phase 19 lessons 30 to 33 (tokenizer, embeddings, attention math, batched data loader)
**Time:** ~90 minutes | **时间:** ~90 minutes

## Learning Objectives | 学习目标

- Build a transformer block in PyTorch from the four moving pieces: LayerNorm, multi head causal attention, residual connections, position wise MLP.
  中文翻译：Build a transformer block in PyTorch from the four moving pieces: LayerNorm, multi head causal attention, residual connections, position wise MLP.
- Place the LayerNorms in two configurations (pre-LN and post-LN) and explain why one trains stably without warmup.
  中文翻译：Place the LayerNorms in two configurations (pre-LN and post-LN) and explain why one trains stably without warmup.
- Implement causal masking inside the multi head attention so token `i` cannot see tokens `j > i`.
  中文翻译：Implement causal masking inside the multi head attention so token `i` cannot see tokens `j > i`.
- Track gradient flow through both variants on a 12 layer stack and read the result without hand waving.
  中文翻译：Track gradient flow through both variants on a 12 layer stack and read the result without hand waving.
- Reuse the block as a drop-in unit when the next lesson assembles a 124 million parameter GPT.
  中文翻译：Reuse the block as a drop-in unit when the next lesson assembles a 124 million parameter GPT.

## The Problem | 问题

> **【中文解读】** Transformer 是一个块的重复。如果块本身有错，重复 12 次就会产生一个在第一个 epoch 就发散或需要 warmup 技巧的模型。两种常见故障模式：(1) 注意力层看到了未来（因果掩码遗漏）；(2) LayerNorm 放在无法控制深度处残差信号的位置。修复是机械性的——正确选择两个归一化位置即可。

> **【拓展：Pre-LN vs Post-LN 的工程影响】** GPT-2（2019）使用 Post-LN，训练需要 warmup。GPT-3（2020）及之后所有主流 LLM（LLaMA、Mistral、Qwen）使用 Pre-LN。Pre-LN 的关键优势：残差路径上的梯度不被 LayerNorm 衰减，12 层甚至 96 层（GPT-3 175B）的堆叠中梯度传播更稳定。LLaMA 进一步将 LayerNorm 替换为 RMSNorm（参数更少，计算更快），配合 SiLU 激活函数。 Get the block wrong once, repeat it twelve times, and you ship a model that diverges in the first epoch or that needs warmup hacks the rest of the way. The two failure modes you will see in this lesson are not exotic. They show up the first time a learner stacks blocks naively. One is the attention layer attending to the future. The other is the LayerNorm placed where it cannot tame the residual signal at depth.

The fix is mechanical once you see it. The block has exactly two residual paths and exactly two normalization positions. Choose the positions correctly and the rest of the stack is just bookkeeping.

> fix is mechanical once you see it. The block has exactly two residual paths and exactly two normalization positions. Choose the positions correctly and the rest of the stack is just bookkeeping.


## The Concept | 概念

Every decoder only transformer block is a function that takes a tensor of shape `(batch, sequence, embedding)` and returns a tensor of the same shape. Inside, two sublayers do the work.

> 每个decoder only transformer block is a function that takes a tensor of shape `(batch, sequence, embedding)` and returns a tensor of the same shape. Inside, two sublayers do the work.


```mermaid
flowchart TB
  X[Input embedding<br/>shape B, T, D] --> N1[LayerNorm 1]
  N1 --> MHA[Multi head causal attention]
  MHA --> R1[Add residual]
  X --> R1
  R1 --> N2[LayerNorm 2]
  N2 --> MLP[Position wise MLP<br/>D to 4D to D]
  MLP --> R2[Add residual]
  R1 --> R2
  R2 --> Y[Output, same shape]
```

This is the pre-LN variant. The LayerNorm sits inside the residual branch, before the sublayer. The residual connection carries the unnormalized signal forward.

> 这个is the pre-LN variant. The LayerNorm sits inside the residual branch, before the sublayer. The residual connection carries the unnormalized signal forward.


The post-LN variant moves the LayerNorm to after the residual add.

> POst-LN variant moves the LayerNorm to after the residual add.（翻译）


```mermaid
flowchart TB
  X[Input] --> MHA[Multi head causal attention]
  MHA --> R1[Add residual]
  X --> R1
  R1 --> N1[LayerNorm 1]
  N1 --> MLP[Position wise MLP]
  MLP --> R2[Add residual]
  N1 --> R2
  R2 --> N2[LayerNorm 2]
  N2 --> Y[Output]
```

Shape is identical. Training behavior is not. With post-LN, the gradient that flows back through the residual path must pass through the LayerNorm. At depth twelve and learning rate `3e-4`, that gradient shrinks fast enough to need a warmup schedule. Pre-LN leaves the residual path unnormalized, so gradients propagate cleanly to the embedding layer. Pre-LN is the configuration GPT-2 onward ships with for that reason.

> Shape is identical.


### Causal multi head attention

> **【中文解读】** 注意力子层将输入投影为 Q、K、V 三个张量，每个从 `(B, T, D)` 重塑为 `(B, H, T, D/H)`。计算 `softmax(Q K^T / sqrt(d_k))` 并应用因果掩码（上三角设为负无穷），然后乘以 V。头拼接回 `(B, T, D)` 后再做一次输出投影。因果掩码是唯一使模型成为 decoder 的组件——忘记掩码等于训练一个作弊的模型。

The attention sublayer projects the input three ways into query, key, value tensors. Each is reshaped from `(B, T, D)` to `(B, H, T, D/H)` where `H` is the head count. Scaled dot product attention computes `softmax(Q K^T / sqrt(d_k))` per head, masks the upper triangle to negative infinity, applies the mask via softmax, then multiplies by `V`. Heads are concatenated back into a single `(B, T, D)` tensor and projected once more. The mask is the only piece that makes the model causal. Forget the mask and you train a model that cheats.

> attention sublayer projects the input three ways into query, key, value tensors. Each is reshaped from `(B, T, D)` to `(B, H, T, D/H)` where `H` is the head count. Scaled dot product attention computes `softmax(Q K^T / sqrt(d_k))` per head, masks the upper triangle to negative infinity, applies the mask via softmax, then multiplies by `V`. Heads are concatenated back into a single `(B, T, D)` tensor and projected once more. The mask is the only piece that makes the model causal. Forget the mask and you train a model that cheats.


### The MLP

The position wise MLP applies the same two layer network to every token independently. The hidden width is four times the embedding width, the activation is GELU, and a dropout follows the second linear. No tokens talk to each other inside the MLP. All token mixing happens in attention.

> position wise MLP applies the same two layer network to every token independently. The hidden width is four times the embedding width, the activation is GELU, and a dropout follows the second linear. No tokens talk to each other inside the MLP. All token mixing happens in attention.


### Residual connections do two things

> **【中文解读】** 残差连接做两件事：(1) 使梯度路径跨深度加法式累加，保持梯度范数在 12 层中稳定；(2) 让每个块学习对运行表征的加法更新而非完全替换。两个效应是 Transformer 可扩展到 100+ 层的关键。

They make the gradient path additive across depth, which keeps the gradient norm in scale through twelve layers. They also let each block learn an additive update to the running representation rather than a full replacement. Both effects are why the block scales.

> They make the gradient path additive across depth, which keeps the gradient norm in scale through twelve layers.


## Build It | 动手构建

`code/main.py` implements:

- `class LayerNorm` with learnable scale and shift, biased eps, applied per token vector.
  中文翻译：`class LayerNorm` with learnable scale and shift, biased eps, applied per token vector.
- `class MultiHeadAttention` with `num_heads`, `head_dim = d_model // num_heads`, fused QKV projection, registered causal mask, attention and residual dropout.
  中文翻译：`class MultiHeadAttention` with `num_heads`, `head_dim = d_model // num_heads`, fused QKV projection, registered causal mask, attention and residual dropout.
- `class FeedForward` with two linear layers, GELU activation, dropout.
  中文翻译：`class FeedForward` with two linear layers, GELU activation, dropout.
- `class TransformerBlock` with a `pre_ln` flag that toggles between the two variants.
  中文翻译：`class TransformerBlock` with a `pre_ln` flag that toggles between the two variants.
- A demo that builds a 6 layer pre-LN stack and a 6 layer post-LN stack with identical inputs and prints (a) output shape, (b) gradient norm at the embedding after one backward pass.
  中文翻译：A demo that builds a 6 layer pre-LN stack and a 6 layer post-LN stack with identical inputs and prints (a) output shape, (b) gradient norm at the embedding after one backward pass.

Run it:

```bash
python3 code/main.py
```

Output: shape check on both stacks, gradient norms side by side. The pre-LN stack's embedding gradient is order of magnitude larger than the post-LN stack at the same learning rate, which is the empirical signal pre-LN trains without warmup.

> Output: shape check on both stacks, gradient norms side by side.


## Stack | 技术栈

- `torch` for the tensor math, autograd, and `nn.Module` plumbing.
  中文翻译：`torch` for the tensor math, autograd, and `nn.Module` plumbing.
- No `transformers`, no pretrained weights. The block is implemented from primitives.
  中文翻译：No `transformers`, no pretrained weights. The block is implemented from primitives.

## Production patterns in the wild

> **【拓展：现代 Transformer 块的变体】** 除了本课的 GPT-2 风格块，主流变体包括：(1) LLaMA 块：RMSNorm + SwiGLU 激活（MLP 中 gate 分支）+ RoPE 旋转位置编码，无 bias；(2) Mistral 块：与 LLaMA 类似但使用 Sliding Window Attention（SWA，窗口大小 4096）降低长序列成本；(3) Mixtral 块：在 MLP 层使用稀疏混合专家（8 个专家中选 2 个），参数量增大但计算量不变。

**Fused QKV projection.** Three separate linear layers cost three kernel launches and three matmuls. One linear layer of width `3 * d_model` does the same work in one launch, then splits the output along the last axis. The fused path is faster on every accelerator and matches what reference implementations of GPT-2, LLaMA, and Mistral all ship.

**Registered causal mask buffer.** The mask depends only on the maximum context length. Allocate it once at construction with `register_buffer`, slice the active window per forward pass, and skip the per-call allocation. Forgetting this turns the mask into an allocator hot spot at long context.

**Dropout in two places, not three.** Dropout belongs after the attention softmax (attention dropout) and after the second linear of the MLP (residual dropout). A dropout on the residual itself breaks the additive identity that lets the gradient flow at depth. Some early implementations got this wrong and paid for it with brittle training.

## Use It | 使用方法

- The block in this lesson plugs straight into the GPT assembly in lesson 35 without modification.
  中文翻译：The block in this lesson plugs straight into the GPT assembly in lesson 35 without modification.
- The pre-LN variant is what every modern open weights LLM uses. The post-LN variant is what the original 2017 attention paper used. Knowing both is enough to read any decoder architecture you will encounter.
  中文翻译：The pre-LN variant is what every modern open weights LLM uses. The post-LN variant is what the original 2017 attention paper used. Knowing both is enough to read any decoder architecture you will encounter.
- Swap the GELU for SiLU and you have the LLaMA family activation. Swap the LayerNorm for RMSNorm and you have the LLaMA family normalization. Same skeleton.
  中文翻译：Swap the GELU for SiLU and you have the LLaMA family activation. Swap the LayerNorm for RMSNorm and you have the LLaMA family normalization. Same skeleton.

## Exercises | 练习题

1. Add a `bias=False` flag to every linear in the block. Modern open weights LLMs ship without biases on the linear layers. Measure how many parameters you save in a 12 layer 768 dim model.
2. Replace `nn.LayerNorm` with a hand rolled RMSNorm and verify the output shape is unchanged.
3. Add a flag that returns the attention weights for the first head as a `(B, T, T)` tensor. Plot the upper triangle to confirm it is zero after softmax.
4. Build a sanity check that feeds a `(2, 16, 384)` tensor with `H=6` through both variants and asserts the forward outputs are different (for example, `not torch.allclose`) when weights are initialized identically and dropout is set to zero.

## Key Terms | 关键术语

| Term | What people say | What it actually means |
|------|-----------------|------------------------|
| Pre-LN | "Pre norm" | LayerNorm inside the residual branch, before each sublayer; the residual carries the unnormalized signal |
| Post-LN | "Post norm" | LayerNorm after the residual add; what the 2017 paper shipped and what needs warmup |
| Causal mask | "Triangle mask" | The upper triangle of the attention logits set to negative infinity so token i cannot read token j when j is greater than i |
| Fused QKV | "Combined projection" | One linear of width 3D instead of three linears of width D; one kernel, one matmul |
| Residual stream | "Skip connection" | The unnormalized tensor that flows top to bottom through every block; what each block adds to |

## Further Reading | 延伸阅读

- Phase 7 lesson 02 (self attention from scratch) for the attention math underneath this block.
  中文翻译：Phase 7 lesson 02 (self attention from scratch) for the attention math underneath this block.
- Phase 7 lesson 05 (full transformer) for the encoder decoder version of the same skeleton.
  中文翻译：Phase 7 lesson 05 (full transformer) for the encoder decoder version of the same skeleton.
- Phase 10 lesson 04 (pre training mini GPT) for the training procedure that this block plugs into.
  中文翻译：Phase 10 lesson 04 (pre training mini GPT) for the training procedure that this block plugs into.
- Phase 19 lesson 35 (this track) which stacks twelve of these blocks into a GPT model.
  中文翻译：Phase 19 lesson 35 (this track) which stacks twelve of these blocks into a GPT model.
