# 完整变压器 编码器+解码器
# 完整变压器 编码器 + 解码器

> 其他一切,剩余物,正常化,向前传递,交叉注意,

> 注意力是主角. 其他一切的差连接,归结,前网络,交叉注意力是让你能够堆积更深的脚架.

> **【中文解读】**让自我注意力,多头脑,FFN,残留,层规则 组装成完整的变压器.

**Type:** Build | **类型:** 动手
**Language:**子**语言:**字符串
**Prerequisites:** Phase 7 · 02 (Self-Attention), Phase 7 · 03 (Multi-Head Attention), Phase 7 · 04 (Positional Encoding) | **前置知识:** 阶段 7 · 02（自注意力），阶段 7 · 03（多头注意力），阶段 7 · 04（位置编码）
**Time:** ~75 minutes | **时间:** ~75 分钟

## 问题 问题引入

单一注意力层是一个特征提取器,而不是模型.每层一个不够语言容量.你需要没有正确的管道.

> 单个注意层是特征提取器,不是模型. 每层一次矩阵乘法不够语言容量.

2017年瓦斯瓦尼论文包装了六项设计决定,将一个注意层转化为可堆叠的块.自编码器 (BERT),解码器 (GPT),编码器-解码器 (T5) 以来,每个变压器都继承了相同的骨架.2026年,这些块已经被精炼 (RMSNorm,SwiGLU,预规范,RoPE),但骨架是相同的.

> 2017年 Vaswani 论文打包了六个设计决策,将一个注意层变成可堆叠的块.

接下来的课程将其专业化为编码器,07为解码器,08为编码器-解码器.

> 本课是骨架. 下课专用化它.

> **【中文解读】**单个注意力层只是一个特征提取器,不是完整的模型――2017年论文将六个设计决策包装成可堆积的块:嵌入+位置编码、自注意力、FFN、残差连接、层归化、交叉注意力――所有后续变体 变体BERT、GPT、T5都继承了相同的骨架――

## 概念的核心概念

![Encoder and decoder block internals, wired](../assets/full-transformer.svg)

### 六个零件.

1. **Embedding + positional signal.**标志 → 矢量. 通过 RoPE (现代) 或突形 (经典) 注射的位置.
   **嵌入 + 位置信号。**标志 → 向量──通过 RoPE(现代) 或正弦编码(经典) 注入位置──

2. **Self-attention.**每个位置都在互相关联,隐藏在解码器中.
   **自注意力。**每个位置关注所有其他位置.

3. **Feed-forward network (FFN).**位置的两层MLP: `W_2 · activation(W_1 · x)`预设扩展率为4×.
   **前馈网络 (FFN)。**位置级两层MLP:`W_2 · activation(W_1 · x)`默认扩展比4×──

4. **Residual connection.** `x + sublayer(x)`没有它,梯度消失了6层.
   **残差连接。** `x + sublayer(x)`没有这个,梯度在6层后消失了.

5. **Layer normalization.** `LayerNorm`或`RMSNorm`稳定了剩余的流量.
   **层归一化。** `LayerNorm`或`RMSNorm`现在,我还在着.

6. **Cross-attention (decoder only).**查询来自解码器,密钥和值来自编码器输出.
   **交叉注意力（仅解码器）。**查询来自解码器,键和值来自编码器输出.

### 编码器块 (使用BERT,T5编码器)
观察一个向量通过一个块流动:注意力在各个位置之间混合,残余物将其运行向前,FFN将其转化,并且规范保持流动稳定.

```figure
transformer-block
```

### 编码器块 (BERT,T5编码器使用)

```
x → LN → MHA(self) → + → LN → FFN → + → out
                     ^              ^
                     |              |
                     └── residual ──┘
```

编码器是双向的,没有掩盖,所有位置都能看到所有位置.

> 编码器是双向的.没有掩盖.

### 解码器块的解码器块

```
x → LN → MHA(masked self) → + → LN → MHA(cross to encoder) → + → LN → FFN → + → out
```

解码器每块有三个子层.中间的  交叉注意力是信息从编码器流向解码器的唯一地方.在纯解码器架构 (GPT) 中,交叉注意力被遗漏,你只掩盖了自我注意力 + FFN.

> 解码器每块有三个子层.中间的交叉注意力是编码器流向解码器的唯一地方. 在纯解码器架构中,交叉注意力被省略,你只掩码自注意力+FFN。

### 之前的规范与后的规范

原始纸:`x + sublayer(LN(x))`其他`LN(x + sublayer(x))`在没有仔细的加热的情况下,更难进行深度训练.`LN`之前的子层) 是2026年默认的:Llama,Qwen,GPT-3+,Mistral都使用它.

> 开始的论文:`x + sublayer(LN(x))`其他`LN(x + sublayer(x))`◎后归结在2019年左右失没有仔细预热就很难深度训练──前归结(`LN`在子层*之前*) 是2026年的默认:Llama、Qwen、GPT-3+、Mistral 都使用它──

### 2026年现代化块

| Component / 组件 | 2017 | 2026 |
|-----------|------|------|
| Normalization / 归一化 | LayerNorm | RMSNorm |
| FFN activation / FFN 激活函数 | ReLU | SwiGLU |
| FFN expansion / FFN 扩展比 | 4× | 2.6×（SwiGLU 使用三个矩阵，总参数匹配） |
| Position / 位置编码 | Sinusoidal absolute / 绝对正弦 | RoPE |
| Attention / 注意力 | Full MHA | GQA (or MLA) |
| Bias terms / 偏置项 | Yes / 有 | No / 无 |

格鲁 (SwiGLU) 则可以通过格鲁 (SwiGLU) 进行格鲁 (SwiGLU) 进行格鲁 (SwiGLU) 格鲁 (SwiGLU) 格鲁 (SwiGLU) 格鲁 (SwiGLU) 格鲁 (SwiGLU) 格鲁 (SwiGLU) 格鲁 (SwiGLU) 格鲁 (SwiGLU) 格鲁 (SwiGLU) 格鲁 (SwiGLU) 格鲁 (SwiGLU) 格鲁 (SwiGLU) 格鲁 (SwiGLU) 格鲁 (SwiGLU) 格鲁 (SwiGLU) 格鲁 (SwiGLU) 格鲁 (SwiGLU) 格鲁 (SwiGLU) 格鲁 (SwiGLU) 格鲁 (SwiGLU) 格鲁 (SwiGLU) 格鲁 (SwiGLU) 格鲁 (SwiGLU) 格鲁 (S) 格鲁) 格鲁 (Sw) 格鲁 (Sw) 格鲁) 格鲁 (Sw) 格鲁 (Sw) 格鲁 (Sw) 格鲁) 格鲁 (Sw)`Swish(W1 x) ⊙ W3 x`) 持续超过Llama,PaLM和Qwen论文中的ReLU/GELU FFN的0.5分点.

> 们的计算量,经验至少同样稳定.`Swish(W1 x) ⊙ W3 x`) 在Llama、PaLM 和 Qwen 论文中一致地比RELU/GELU FFN 好约0.5个困惑度点──

> **【中文解读】**2026 年的现代变压器块与 2017 年原版相比:LayerNorm→RMSNorm,ReLU→SwiGLU,后归一化→前归一化,绝对位置编码→RoPE,全多头注意力→GQA──每项改进都是渐进的,但组合显著提高了训练稳定性和模型质量──

> **【拓展：为什么 Decoder-only 成为主流】**虽然编码器解码器架构在翻译等任务上有自然优势,但仅编码器模型 (GPT、Llama) 在扩展性和通用性上更胜一筹――它可以使用相同的架构处理理解和生成任务,训练目标统一,预测),并且扩展性已被Chinchilla 定律验证――这正是2024-2026年几乎所有前沿的大模型的选择.

### 参数数量

为了一个街区`d_model = d`及FFN扩张`r`其他:

> 对于一个`d_model = d`且FFN 扩展比为`r`块:

- 鱼类`4 · d²`预测量
  鱼类`4 · d²`投影的时间
- 转移: 转移:`3 · d · (r · d)`≈ ≈`3rd²`
  鱼类:`3 · d · (r · d)`≈ ≈`3rd²`
- 标准: 无关可视
  归一化:可忽略

> **【拓展：参数计数与模型规模的实际意义】**变压器的参数主要集中在注意力投影(4d^2) 和FFN(约8d^2为SwiGLU) 中──Llama 3 8B 每层约1.5B参数,32层共约7B加上嵌入层和输出头──理解参数分布有助于优化:MOE 替换FFN可以增加总参数而不增加活跃计算;量化(如GPTQ、AWQ) 主要压缩FFN 权重──

## 建立它,实现它.

### 建构块的第一步.

通过使用小小的`Matrix`课03 (为了独立,复制到本文件):

> 使用第03课中的微型`Matrix`类(已复制到此文件以保持独立):

- `layer_norm(x, eps=1e-5)`减去平均值,分为 std.
  `layer_norm(x, eps=1e-5)` 减去平均值,除以标准差.
- `rms_norm(x, eps=1e-6)` 分为RMS. 没有中减.
  `rms_norm(x, eps=1e-6)`除以RMS──不减平均值──
- `gelu(x)`其他`silu(x) * W3 x`现在我们要去做什么?
  `gelu(x)`和 `silu(x) * W3 x`没有什么可言.
- `ffn_swiglu(x, W1, W2, W3)`现在,我们要去.
- `encoder_block(x, params)`其他`decoder_block(x, enc_out, params)`现在,我们要去.

### 步骤2:连接2层编码器和2层解码器

输出出码器输入每个解码器交叉注意力. 在输出投影之前添加最后的LN.

> 堆叠它们――将编码器输出传入每个解码器交叉注意力――在输出投影前添加最终LN――

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

### 步骤3:在玩具的例子上运行前向传播

输出源源和目标源源为5个代币.`(5, vocab)`没有培训,这堂课是关于建筑,不是损失.

> 输入 6 个代币的源和 5 个代币的目标――验证输出形状是`(5, vocab)`│不训练本课关注结构,不关注损失──

### 步骤4:换成RMSNorm + SwiGLU

通过RMSNorm和SwiGLU取代LayerNorm和ReLU-FFN. 确认形状仍然匹配.这是2026年现代化,一个函数的替代.

> 用RMSNorm 和 SwiGLU 替换LayerNorm 和 ReLU-FFN──确认形状仍然匹配──这是通过一次函数替换实现的2026年现代化──

## 用它实现框架

 PyTorch/TF 参考实施方案: `nn.TransformerEncoderLayer`现在`nn.TransformerDecoderLayer`但大部分2026生产代码都用了自己的块,因为:

> 参考实现:`nn.TransformerEncoderLayer`,我知道.`nn.TransformerDecoderLayer`,但大多数2026年生产代码自建块,因为:

- 闪光注意力是通过内部注意力而不是通过`nn.MultiheadAttention`现在,我们要去.
  闪光注意力 在注意力内部调用,不通过 `nn.MultiheadAttention`,我知道.
- 没有任何关于GQA/MLA的参考.
  标准库参考中不在
- ,RMSNorm,SwiGLU不是PyTorch默认的.
  罗佩、RMSNorm、SwiGLU 不是PyTorch的默认值.

**Encoder vs decoder vs encoder-decoder — when to pick:**

> **编码器 vs 解码器 vs 编码器-解码器——何时选择：**

| Need / 需求 | Pick / 选择 | Example / 示例 |
|------|------|---------|
| Classification, embeddings, QA over text / 分类、嵌入、文本 QA | Encoder-only / 纯编码器 | BERT, DeBERTa, ModernBERT |
| Text generation, chat, code, reasoning / 文本生成、聊天、代码、推理 | Decoder-only / 纯解码器 | GPT, Llama, Claude, Qwen |
| Structured input → structured output (translation, summarization) / 结构化转换 | Encoder-decoder / 编码器-解码器 | T5, BART, Whisper |

> **【中文解读】**三种架构的选择:仅编码器 (BERT) 适合分类和嵌入;仅编码器 (GPT/Llama) 适合生成和通用任务;仅编码器 (T5/BART) 适合有明确的"源序列"的结构化转换任务――2026年的主流选择是仅编码器,因为它的扩展性最好,训练最简洁――

> **【拓展：SwiGLU 为何优于 ReLU】**通过门控机制使FFN的表达能力更强. 模型的实验表明,SwiGLU比ReLU/GELU在语言建模困惑度低约0.5个点. 虽然它需要三个权重矩阵而不是两个,参数增加50%),但通常通过将扩大比率从4x降至2.6x来补偿.

## 运送它.

看到`outputs/skill-transformer-block-reviewer.md`技能检查了对2026年默认的变压器块的新实施,并标记了缺失的零件 (前标准,RoPE,RMSNorm,GQA,FFN扩展比).

> 参见`outputs/skill-transformer-block-reviewer.md`△该技能根据2026年默认设置审查新的变压器块实现,并标记缺失部分──

## 练习题

1. **Easy / 简单。**计算您的编码_区块中的参数`d_model=512, n_heads=8, ffn_expansion=4, swiglu=True`通过实现区块和使用`sum(p.numel() for p in block.parameters())`现在,我们要去.
   计算`d_model=512, n_heads=8, ffn_expansion=4, swiglu=True`时代码器_区块的参数量──通过实现区块并使用 `sum(p.numel() for p in block.parameters())`验证.

2. **Medium / 中等。**切换从后规范到前规范. 启动两者,并在随机输入中测量12层堆叠后的激活规范. 后规范的激活应爆炸; 前规则应保持局限.
   从后归结转换到前归结.初始化两者并测量了随机输入的12个堆叠层的激活范数.后归结的激活应该爆炸.前归结应该保持有界.

3. **Hard / 困难。**实现4层编码解码器在玩具复制任务 (复制 `x`换 RMSNorm + SwiGLU + RoPE  损失下降吗?
   在玩具复制任务中`x`实现4层编码器解码器――训练100步――报告损失――替换为RMSNorm + SwiGLU + RoPE损失是否下降?

## 关键词 快速查找表

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

## 继续阅读 继续阅读

- [Vaswani et al. (2017). Attention Is All You Need](https://arxiv.org/abs/1706.03762)原始的块规格.
  瓦斯瓦尼 等人(2017)  原始块规范──

- [Xiong et al. (2020). On Layer Normalization in the Transformer Architecture](https://arxiv.org/abs/2002.04745)为什么前规则比后规则更深.
  习近平等 (2020)  为什么在深层中胜过后归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归

- [Zhang, Sennrich (2019). Root Mean Square Layer Normalization](https://arxiv.org/abs/1910.07467)        

- [Shazeer (2020). GLU Variants Improve Transformer](https://arxiv.org/abs/2002.05202)SwiGLU的报纸.
                                                                                                                                                                                                                                                                

- [HuggingFace `modeling_llama.py`](https://github.com/huggingface/transformers/blob/main/src/transformers/models/llama/modeling_llama.py)可信 2026 单独使用解码器的区块.
  拥抱脸`modeling_llama.py` 2026年规范的纯解码器块
