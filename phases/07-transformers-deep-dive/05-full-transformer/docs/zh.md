# The Full Transformer — Encoder + Decoder | 完整 Transformer — 编码器 + 解码器

> 注意力是主角。其他一切——残差连接、归一化、前馈网络、交叉注意力——都是让你能将其堆叠得更深的脚手架。

> **【中文解读】** 把 Self-Attention、Multi-Head、FFN、Residual、LayerNorm 组装成完整的 Transformer。这是 Attention Is All You Need 论文的实现。

**类型：** 构建
**语言：** Python
**前置条件：** 阶段 7 · 02（自注意力），阶段 7 · 03（多头注意力），阶段 7 · 04（位置编码）
**时长：** 约 75 分钟

## 问题引入

单个注意力层是特征提取器，不是模型。每层一次矩阵乘法不够语言的容量。你需要深度——而深度没有正确的管道会崩溃。

2017 年 Vaswani 论文打包了六个设计决策，将一个注意力层变成可堆叠的块。此后每个 Transformer——纯编码器（BERT）、纯解码器（GPT）、编码器-解码器（T5）——都继承了相同的骨架。2026 年，这些块已被优化（RMSNorm、SwiGLU、前归一化、RoPE），但骨架完全相同。

本课是骨架。接下来的课程专门化它——06 课讲编码器，07 课讲解码器，08 课讲编码器-解码器。

> **【中文解读】** 单个注意力层只是一个特征提取器，不是完整的模型。2017 年的论文将六个设计决策打包成可堆叠的块：嵌入+位置编码、自注意力、FFN、残差连接、层归一化、交叉注意力。所有后续 Transformer 变体——BERT、GPT、T5——都继承了相同的骨架。

## 核心概念

![编码器和解码器块内部结构，连接方式](../assets/full-transformer.svg)

### 六个组件

1. **嵌入 + 位置信号。** Token → 向量。通过 RoPE（现代）或正弦编码（经典）注入位置。
2. **自注意力。** 每个位置关注所有其他位置。解码器中使用掩码。
3. **前馈网络 (FFN)。** 位置级两层 MLP：`W_2 · activation(W_1 · x)`。默认扩展比 4×。
4. **残差连接。** `x + sublayer(x)`。没有这个，梯度在约 6 层后消失。
5. **层归一化。** `LayerNorm` 或 `RMSNorm`（现代）。稳定残差流。
6. **交叉注意力（仅解码器）。** 查询来自解码器，键和值来自编码器输出。

### 编码器块（用于 BERT、T5 编码器）

```
x → LN → MHA(self) → + → LN → FFN → + → out
                     ^              ^
                     |              |
                     └── 残差连接 ──┘
```

编码器是双向的。没有掩码。所有位置看到所有位置。

### 解码器块（用于 GPT、T5 解码器）

```
x → LN → MHA(masked self) → + → LN → MHA(cross to encoder) → + → LN → FFN → + → out
```

解码器每块有三个子层。中间那个——交叉注意力——是信息从编码器流向解码器的唯一地方。在纯解码器架构（GPT）中，交叉注意力被省略，你只有掩码自注意力 + FFN。

### 前归一化 vs 后归一化

原始论文：`x + sublayer(LN(x))` vs `LN(x + sublayer(x))`。后归一化在 2019 年左右失宠——没有仔细预热就很难深度训练。前归一化（`LN` 在子层*之前*）是 2026 年的默认：Llama、Qwen、GPT-3+、Mistral 都使用它。

### 2026 年现代化块

Vaswani 2017 发布的是 LayerNorm + ReLU。现代堆栈替换了两者。生产块的实际样子：

| 组件 | 2017 | 2026 |
|------|------|------|
| 归一化 | LayerNorm | RMSNorm |
| FFN 激活函数 | ReLU | SwiGLU |
| FFN 扩展比 | 4× | 2.6×（SwiGLU 使用三个矩阵，总参数匹配） |
| 位置编码 | 绝对正弦 | RoPE |
| 注意力 | 完整 MHA | GQA（或 MLA） |
| 偏置项 | 有 | 无 |

RMSNorm 去掉了 LayerNorm 的均值中心化（少一次减法），节省了计算量，经验上至少同样稳定。SwiGLU（`Swish(W1 x) ⊙ W3 x`）在 Llama、PaLM 和 Qwen 论文中一致地比 ReLU/GELU FFN 好约 0.5 个困惑度点。

> **【中文解读】** 2026 年的现代 Transformer 块与 2017 年原版相比：LayerNorm→RMSNorm，ReLU→SwiGLU，后归一化→前归一化，绝对位置编码→RoPE，全多头注意力→GQA。每一项改进都是渐进的，但组合起来显著提升了训练稳定性和模型质量。

> **【拓展：为什么 Decoder-only 成为主流】** 虽然编码器-解码器架构在翻译等任务上有天然优势，但 Decoder-only 模型（GPT、Llama）在扩展性和通用性上更胜一筹。它可以用同一架构处理理解和生成任务，训练目标统一（下一个 token 预测），且扩展性已被 Chinchilla 定律验证。这正是 2024-2026 年几乎所有前沿大模型选择 Decoder-only 的原因。

### 参数量

对于一个 `d_model = d` 且 FFN 扩展比为 `r` 的块：

- MHA：`4 · d²`（Q、K、V、O 投影）
- FFN（SwiGLU）：`3 · d · (r · d)` ≈ `3rd²`
- 归一化：可忽略

在 `d = 4096, r = 2.6, layers = 32`（大致为 Llama 3 8B）时，总计：`32 · (4·4096² + 3·2.6·4096²) ≈ 32 · (16 + 32) M = ~1.5B parameters per layer × 32 ≈ 7B`（加上嵌入和输出头）。与公布数量匹配。

> **【拓展：参数计数与模型规模的实际意义】** Transformer 的参数主要集中在注意力投影（4d^2）和 FFN（约 8d^2 for SwiGLU）中。Llama 3 8B 每层约 1.5B 参数，32 层共约 7B 加上嵌入层和输出头。理解参数分布有助于优化：MoE 替换 FFN 可以增加总参数而不增加活跃计算；量化（如 GPTQ、AWQ）主要压缩 FFN 权重。

## 动手实现

### 步骤 1：构建模块

使用第 03 课中的微型 `Matrix` 类（已复制到此文件以保持独立）：

- `layer_norm(x, eps=1e-5)` —— 减去均值，除以标准差。
- `rms_norm(x, eps=1e-6)` —— 除以 RMS。不减均值。
- `gelu(x)` 和 `silu(x) * W3 x`（SwiGLU）。
- `ffn_swiglu(x, W1, W2, W3)`。
- `encoder_block(x, params)` 和 `decoder_block(x, enc_out, params)`。

参见 `code/main.py` 获取完整布线。

### 步骤 2：连接 2 层编码器和 2 层解码器

堆叠它们。将编码器输出传入每个解码器交叉注意力。在输出投影前添加最终 LN。

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

### 步骤 3：在玩具示例上运行前向传播

输入 6 个 token 的源和 5 个 token 的目标。验证输出形状是 `(5, vocab)`。不训练——本课关注架构，不关注损失。

### 步骤 4：替换为 RMSNorm + SwiGLU

用 RMSNorm 和 SwiGLU 替换 LayerNorm 和 ReLU-FFN。确认形状仍然匹配。这是通过一次函数替换实现的 2026 年现代化。

## 用框架实现

PyTorch/TF 参考实现：`nn.TransformerEncoderLayer`、`nn.TransformerDecoderLayer`。但大多数 2026 年的生产代码自建块，因为：

- Flash Attention 在注意力内部调用，不通过 `nn.MultiheadAttention`。
- GQA / MLA 不在标准库参考中。
- RoPE、RMSNorm、SwiGLU 不是 PyTorch 的默认值。

HF `transformers` 有干净的可参考块，你应该阅读：`modeling_llama.py` 是 2026 年规范的纯解码器块。约 500 行，值得通读一次。

**编码器 vs 解码器 vs 编码器-解码器——何时选择：**

| 需求 | 选择 | 示例 |
|------|------|------|
| 分类、嵌入、文本 QA | 纯编码器 | BERT, DeBERTa, ModernBERT |
| 文本生成、聊天、代码、推理 | 纯解码器 | GPT, Llama, Claude, Qwen |
| 结构化输入 → 结构化输出（翻译、摘要） | 编码器-解码器 | T5, BART, Whisper |

纯解码器赢得了语言领域，因为它的扩展最干净，同时处理理解和生成。编码器-解码器在输入有明确"源序列"身份（翻译、语音识别、结构化任务）时仍然最佳。

> **【中文解读】** 三种架构的选择：Encoder-only（BERT）适合分类和嵌入；Decoder-only（GPT/Llama）适合生成和通用任务；Encoder-Decoder（T5/BART）适合有明确"源序列"的结构化转换任务。2026 年的主流选择是 Decoder-only，因为它的扩展性最好、训练最简洁。

> **【拓展：SwiGLU 为何优于 ReLU】** SwiGLU（Swish-Gated Linear Unit）通过门控机制让 FFN 的表达能力更强。Llama、PaLM、Qwen 等模型的实验一致表明 SwiGLU 比 ReLU/GELU 在语言建模困惑度上低约 0.5 个点。虽然它需要三个权重矩阵而非两个（参数量增加 50%），但通常通过将扩展比从 4x 降到 2.6x 来补偿。

## 产出物

参见 `outputs/skill-transformer-block-reviewer.md`。该技能根据 2026 年默认设置审查新的 Transformer 块实现，并标记缺失的部分（前归一化、RoPE、RMSNorm、GQA、FFN 扩展比）。

## 练习题

1. **简单。** 计算 `d_model=512, n_heads=8, ffn_expansion=4, swiglu=True` 时 encoder_block 的参数量。通过实现块并使用 `sum(p.numel() for p in block.parameters())` 验证。
2. **中等。** 从后归一化切换到前归一化。初始化两者并测量 12 个堆叠层在随机输入上的激活范数。后归一化的激活应该爆炸；前归一化的应该保持有界。
3. **困难。** 在玩具复制任务（反转复制 `x`）上实现 4 层编码器-解码器。训练 100 步。报告损失。替换为 RMSNorm + SwiGLU + RoPE——损失是否下降？

## 术语速查表

| 术语 | 人们的说法 | 实际含义 |
|------|-----------|---------|
| 块 (Block) | "一个 Transformer 层" | 归一化 + 注意力 + 归一化 + FFN 的堆叠，包裹在残差连接中。 |
| 残差连接 (Residual) | "跳跃连接" | `x + f(x)` 输出；使梯度流能穿过深层堆叠。 |
| 前归一化 (Pre-norm) | "先归一化，不是后归一化" | 现代：`x + sublayer(LN(x))`。无需预热技巧即可训练更深的网络。 |
| RMSNorm | "没有均值的 LayerNorm" | 除以 RMS；少一次操作，经验上同样稳定。 |
| SwiGLU | "大家都换成的 FFN" | `Swish(W1 x) ⊙ W3 x → W2`。在 LM 困惑度上击败 ReLU/GELU。 |
| 交叉注意力 | "解码器如何看到编码器" | MHA 的 Q 来自解码器，K/V 来自编码器输出。 |
| FFN 扩展比 | "中间 MLP 有多宽" | 隐藏大小与 d_model 的比率，通常为 4（LayerNorm）或 2.6（SwiGLU）。 |
| 无偏置 | "去掉 +b 项" | 现代堆栈在线性层中省略偏置；轻微的困惑度改善，更小的模型。 |

## 延伸阅读

- [Vaswani 等人（2017）。Attention Is All You Need](https://arxiv.org/abs/1706.03762) —— 原始块规范。
- [Xiong 等人（2020）。On Layer Normalization in the Transformer Architecture](https://arxiv.org/abs/2002.04745) —— 为什么前归一化在深层中胜过后归一化。
- [Zhang, Sennrich（2019）。Root Mean Square Layer Normalization](https://arxiv.org/abs/1910.07467) —— RMSNorm。
- [Shazeer（2020）。GLU Variants Improve Transformer](https://arxiv.org/abs/2002.05202) —— SwiGLU 论文。
- [HuggingFace `modeling_llama.py`](https://github.com/huggingface/transformers/blob/main/src/transformers/models/llama/modeling_llama.py) —— 2026 年规范的纯解码器块。
