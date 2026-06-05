# Build a Transformer from Scratch — The Capstone | 从零构建 Transformer — 毕业项目

> Thirteen lessons. One model. No shortcuts.

> **【中文解读】** 整合所有知识，从零实现完整的 GPT 架构。这是本阶段的核心实践——理解这个，你就能读懂任何 Transformer 的代码。

**Type:** Hands-on | **类型:** 动手
**Language:** Python | **语言:** Python
**Prerequisites:** Phase 7 · 01 through 13. Don't skip. | **前置知识:** Phase 7 · 01 through 13. Don't skip.
**Time:** ~120 minutes | **时间:** ~120 分钟

## The Problem | 问题引入

You've read every paper. You've implemented attention, multi-head splits, positional encodings, encoder and decoder blocks, BERT and GPT losses, MoE, KV cache. Now make them work together on a real task.

> 你已经读了每篇论文。你实现了注意力、多头拆分、位置编码、编码器和解码器块、BERT 和 GPT 损失、MoE、KV 缓存。现在让它们在一个真实任务上协同工作。

The capstone: train a small decoder-only transformer end-to-end on a character-level language modeling task. It reads Shakespeare. It generates new Shakespeare. It is small enough to train on a laptop in under 10 minutes. It is correct enough that swapping in a bigger dataset and longer training gets you a real LM.

> 毕业项目：在字符级语言建模任务上端到端训练一个小型解码器专用 Transformer。它读取 Shakespeare，生成新的 Shakespeare。它足够小，可以在笔记本上 10 分钟内训练完成。它足够正确，换成更大的数据集和更长的训练时间就能得到真正的语言模型。

This is the "nanoGPT" of the course. It is not original — Karpathy's 2023 nanoGPT tutorial is the reference implementation every student writes at least once. We lift the shape and retool it around what we've covered.

> 这是课程的"nanoGPT"。它不是原创的——Karpathy 2023 年的 nanoGPT 教程是每个学生至少写一次的参考实现。我们借鉴了它的结构，并根据我们学过的内容进行了改造。

> **【中文解读】** 这个毕业项目将前 13 节课的所有知识整合：字符级语言建模、token 嵌入、位置编码、RMSNorm、多头因果注意力、SwiGLU FFN、残差连接，训练一个能在笔记本上 10 分钟内完成的 Shakespeare 生成器。虽然小，但架构与 GPT-4 相同——增大数据和训练量就能得到真正的语言模型。

> **【拓展：从 nanoGPT 到生产级 LLM】** Karpathy 的 nanoGPT 是学习 Transformer 的最佳起点。从 nanoGPT 到生产级 LLM 的关键差异在于：数据规模（从 MB 到 TB）、训练基础设施（从单 GPU 到数千 GPU 集群）、分布式训练（数据并行、模型并行、流水线并行）、以及后训练（SFT + RLHF）。但核心架构是一样的。

## The Concept | 核心概念

![Transformer-from-scratch block diagram](../assets/capstone.svg)

The architecture, annotated:

> 架构，带注释：

```
input tokens (B, N)
   │
   ▼
token embedding + positional embedding  ◀── Lesson 04 (RoPE option)
   │
   ▼
┌──── block × L ────────────────────┐
│  RMSNorm                          │  ◀── Lesson 05
│  MultiHeadAttention (causal)      │  ◀── Lesson 03 + 07 (causal mask)
│  residual                         │
│  RMSNorm                          │
│  SwiGLU FFN                       │  ◀── Lesson 05
│  residual                         │
└────────────────────────────────── ┘
   │
   ▼
final RMSNorm
   │
   ▼
lm_head (tied to token embedding)
   │
   ▼
logits (B, N, V)
   │
   ▼
shift-by-one cross-entropy            ◀── Lesson 07
```

### What we ship

> 我们交付的内容：

- `GPTConfig` — one place to configure all hyperparameters.
  中文翻译：`GPTConfig` — 一个配置所有超参数的地方。
- `MultiHeadAttention` — causal, batched, with optional Flash-style pathway (PyTorch's `scaled_dot_product_attention`).
  中文翻译：`MultiHeadAttention` — 因果的、批量的，可选 Flash 风格路径（PyTorch 的 `scaled_dot_product_attention`）。
- `SwiGLUFFN` — modern FFN.
  中文翻译：`SwiGLUFFN` — 现代 FFN。
- `Block` — pre-norm, residual-wrapped attention + FFN.
  中文翻译：`Block` — 前归一化，残差包裹的注意力 + FFN。
- `GPT` — embeddings, stacked blocks, LM head, generate().
  中文翻译：`GPT` — 嵌入、堆叠块、LM 头、generate()。
- Training loop with AdamW, cosine LR, gradient clipping.
  中文翻译：带 AdamW、余弦学习率、梯度裁剪的训练循环。
- Char-level tokenizer on Shakespeare text.
  中文翻译：Shakespeare 文本上的字符级分词器。

> **【中文解读】** 完整的 GPT 实现包含：配置类、多头因果注意力（可选 Flash Attention）、SwiGLU FFN、前归一化残差块、完整的 GPT 模型类（嵌入 + 堆叠块 + LM 头 + 生成函数）、AdamW + 余弦学习率训练循环。为了简洁，使用了学习式位置嵌入（而非 RoPE）且未实现 KV 缓存，但练习要求你添加这些。

### What we don't ship

> 我们不交付的内容：

- RoPE — implemented conceptually in Lesson 04. Here we use learned positional embeddings for simplicity. The exercises ask you to swap in RoPE.
  中文翻译：RoPE — 在第 04 课有概念实现。这里为简洁起见使用学习式位置嵌入。练习要求你替换为 RoPE。
- KV cache during generation — each generation step recomputes attention over the full prefix. Slower but simpler. The exercises ask you to add a KV cache.
  中文翻译：生成时的 KV 缓存 — 每个生成步骤对完整前缀重新计算注意力。更慢但更简单。练习要求你添加 KV 缓存。
- Flash Attention — PyTorch 2.0+ auto-dispatches if the inputs match; we use `F.scaled_dot_product_attention`.
  中文翻译：Flash Attention — PyTorch 2.0+ 在输入匹配时自动分派；我们使用 `F.scaled_dot_product_attention`。
- MoE — single FFN per block. You saw MoE in Lesson 11.
  中文翻译：MoE — 每块单个 FFN。你在第 11 课见过 MoE。

### Target metrics

On a Mac M2 laptop, a 4-layer, 4-head, d_model=128 GPT trained for 2,000 steps on `tinyshakespeare.txt`:

> 在 Mac M2 笔记本上，4 层、4 头、d_model=128 的 GPT 在 `tinyshakespeare.txt` 上训练 2,000 步：

- Training loss converges from ~4.2 (random) to ~1.5 in about 6 minutes.
  中文翻译：训练损失从约 4.2（随机）在约 6 分钟内收敛到约 1.5。
- Sampled output looks Shakespeare-shaped: archaic words, line breaks, proper names like "ROMEO:" emerge.
  中文翻译：采样输出看起来像 Shakespeare：古词、换行、"ROMEO:" 等专有名词出现。
- Val loss (held-out final 10% of text) tracks training loss closely; no overfitting at this size/budget.
  中文翻译：验证损失（留出最后 10% 的文本）紧跟训练损失；在这个规模/预算下没有过拟合。

> **【拓展：从字符级到子词级 Tokenizer】** 本项目使用字符级 tokenizer（简单但低效）。生产级 LLM 使用 BPE（Byte Pair Encoding）或 SentencePiece 等子词级 tokenizer。Llama 使用 BPE，GPT-4 使用 cl100k_base BPE tokenizer。子词 tokenization 在词汇量、序列长度和语义粒度之间取得平衡，是现代 LLM 的标配。

## Build It | 动手实现

This lesson uses PyTorch. Install `torch` (CPU build is fine). See `code/main.py`. The script handles:

> 本课使用 PyTorch。安装 `torch`（CPU 版本即可）。参见 `code/main.py`。该脚本处理：

- Downloading `tinyshakespeare.txt` if missing (or reading a local copy).
  中文翻译：如果缺失则下载 `tinyshakespeare.txt`（或读取本地副本）。
- Byte-level char tokenizer.
  中文翻译：字节级字符分词器。
- Train/val split at 90/10.
  中文翻译：90/10 的训练/验证分割。
- Training loop with bf16 autocast on supported hardware.
  中文翻译：支持硬件上的 bf16 自动混合精度训练循环。
- Sampling after training completes.
  中文翻译：训练完成后的采样。

### Step 1: data

```python
text = open("tinyshakespeare.txt").read()
chars = sorted(set(text))
stoi = {c: i for i, c in enumerate(chars)}
itos = {i: c for c, i in stoi.items()}
encode = lambda s: [stoi[c] for c in s]
decode = lambda xs: "".join(itos[x] for x in xs)
```

65 unique characters. Tiny vocabulary. Fits a 4-byte vocab_size. No BPE, no tokenizer drama.

> 65 个唯一字符。微型词表。适配 4 字节 vocab_size。没有 BPE，没有分词器的麻烦。

### Step 2: model

See `code/main.py`. The block is textbook from Lesson 05 — pre-norm, RMSNorm, SwiGLU, causal MHA. Parameter count for 4/4/128: ~800K.

> 参见 `code/main.py`。该块是第 05 课的教科书实现——前归一化、RMSNorm、SwiGLU、因果多头注意力。4/4/128 的参数量：约 800K。

### Step 3: training loop

Get a random batch of length-256 token windows. Forward. Shift-by-one cross-entropy. Backward. AdamW step. Log. Repeat.

> 获取随机批量长度为 256 的 token 窗口。前向传播。偏移一位的交叉熵。反向传播。AdamW 步进。记录。重复。

```python
for step in range(max_steps):
    x, y = get_batch("train")
    logits = model(x)
    loss = F.cross_entropy(logits.view(-1, vocab_size), y.view(-1))
    loss.backward()
    torch.nn.utils.clip_grad_norm_(model.parameters(), 1.0)
    opt.step()
    opt.zero_grad()
```

### Step 4: sample

Given a prompt, repeatedly forward, sample from top-p logits, append, and continue. Stop after 500 tokens.

> 给定一个提示，反复前向传播，从 top-p logits 采样，追加，继续。500 个 token 后停止。

### Step 5: read the output

After 2,000 steps:

> 2,000 步后：

```
ROMEO:
Away and mild will not thy friend, that thou shalt wit:
The chief that well shame and hath been his friends,
...
```

Not Shakespeare. But Shakespeare-shaped. A clear win for ~800K parameters and 6 minutes on a laptop.

> 不是 Shakespeare。但像 Shakespeare。约 800K 参数在笔记本上 6 分钟的明确胜利。

## Use It | 用框架实现

This capstone is a reference architecture. Three extensions to ship it to something real:

> 这个毕业项目是一个参考架构。三个扩展可以将它变成真正可用的系统：

1. **Swap the tokenizer.** Use BPE (e.g. `tiktoken.get_encoding("cl100k_base")`). Vocab size jumps from 65 to ~50,000. Model capacity needs to scale up to compensate.
   中文翻译：**替换分词器。** 使用 BPE（如 `tiktoken.get_encoding("cl100k_base")`）。词表大小从 65 跳到约 50,000。模型容量需要相应扩展。
2. **Train on a bigger corpus.** Use `OpenWebText` or `fineweb-edu` (HuggingFace). 10B tokens on a single A100 takes ~24 hours for a 125M-param GPT.
   中文翻译：**在更大的语料上训练。** 使用 `OpenWebText` 或 `fineweb-edu`（HuggingFace）。在单张 A100 上用 10B token 训练 125M 参数 GPT 约需 24 小时。
3. **Add RoPE + KV cache + Flash Attention.** The exercises below walk you through each.
   中文翻译：**添加 RoPE + KV 缓存 + Flash Attention。** 下面的练习将引导你完成每一步。

This ends up as a 125M-parameter GPT that generates fluent English. Not a frontier model. But the same code path — just bigger — is what Karpathy, EleutherAI, and the Allen Institute use to train research checkpoints in 2026.

> 最终得到一个能生成流利英语的 125M 参数 GPT。不是前沿模型。但同样的代码路径——只是更大——是 Karpathy、EleutherAI 和 Allen Institute 在 2026 年训练研究检查点所使用的。

> **【拓展：Karpathy 的 nanoGPT 与教育意义】** Andrej Karpathy 的 nanoGPT（2023）是 AI 教育史上最有影响力的教程之一。它证明了一个完整、可训练的 GPT 可以用约 300 行 PyTorch 实现。这种"从零构建"的教学方法让你真正理解每个组件的作用，而不是把 Transformer 当作黑盒。

## Ship It | 产出物

See `outputs/skill-transformer-review.md`. The skill reviews a transformer-from-scratch implementation for correctness across all 13 prior lessons.

> 参见 `outputs/skill-transformer-review.md`。该 skill 审查一个从零构建的 Transformer 实现，检查所有前 13 课的正确性。

## Exercises | 练习题

1. **Easy.** Run `code/main.py`. Verify your trained model's final-step validation loss is under 2.0. Change `max_steps` from 2,000 to 5,000 — does val loss keep improving?
   中文翻译：运行 `code/main.py`。验证你训练模型的最终步验证损失低于 2.0。将 `max_steps` 从 2,000 改为 5,000——验证损失是否继续改善？
2. **Medium.** Replace learned positional embeddings with RoPE. Apply the rotation to Q and K inside `MultiHeadAttention`. Train and verify val loss is at least as low.
   中文翻译：用 RoPE 替换学习式位置嵌入。在 `MultiHeadAttention` 中对 Q 和 K 应用旋转。训练并验证验证损失至少不差。
3. **Medium.** Implement a KV cache in the sampling loop. Generate 500 tokens with and without cache. Wall-clock should improve by 5–20× on a laptop.
   中文翻译：在采样循环中实现 KV 缓存。有缓存和无缓存各生成 500 个 token。笔记本上应该有 5-20 倍的实际时间改善。
4. **Hard.** Add a second head to the model that predicts the next-plus-one token (MTP — Multi-Token Prediction from DeepSeek-V3). Train jointly. Does it help?
   中文翻译：添加第二个头预测下下一个 token（MTP——来自 DeepSeek-V3 的多 token 预测）。联合训练。是否有帮助？
5. **Hard.** Replace the single FFN per block with a 4-expert MoE. Router + top-2 routing. See how val loss changes at matched active parameters.
   中文翻译：将每块的单个 FFN 替换为 4 专家 MoE。路由器 + top-2 路由。观察在匹配活跃参数量下验证损失的变化。

## Key Terms | 术语速查表

| Term | What people say | What it actually means |
|------|-----------------|-----------------------|
| 术语 | 通俗说法 | 实际含义 |
| nanoGPT | "Karpathy's tutorial repo" | Minimal decoder-only transformer training code, ~300 LOC; the canonical reference. |
| nanoGPT | "Karpathy 的教程仓库" | 最小解码器专用 Transformer 训练代码，约 300 行；经典参考。 |
| tinyshakespeare | "The standard toy corpus" | ~1.1 MB of text; every character-LM tutorial since 2015 uses it. |
| tinyshakespeare | "标准玩具语料库" | 约 1.1 MB 文本；自 2015 年以来每个字符级语言模型教程都用它。 |
| Tied embeddings | "Share input/output matrix" | LM head weight = transpose of token embedding matrix; saves parameters, improves quality. |
| 绑定嵌入 | "共享输入/输出矩阵" | LM 头权重 = token 嵌入矩阵的转置；节省参数，提高质量。 |
| bf16 autocast | "Training precision trick" | Run forward/back in bf16, keep optimizer state in fp32; standard since 2021. |
| bf16 自动混合精度 | "训练精度技巧" | 前向/反向用 bf16，优化器状态用 fp32；2021 年以来的标准。 |
| Gradient clipping | "Stops spikes" | Cap global grad norm at 1.0; prevents training blowups. |
| 梯度裁剪 | "阻止尖峰" | 将全局梯度范数限制在 1.0；防止训练爆炸。 |
| Cosine LR schedule | "The 2020+ default" | LR ramps up linearly (warmup) then decays cosine-shaped to 10% of peak. |
| 余弦学习率调度 | "2020+ 默认" | 学习率线性升温（warmup）然后余弦衰减到峰值的 10%。 |
| MFU | "Model FLOP Utilization" | Achieved FLOPs / theoretical peak; 40% dense, 30% MoE is strong in 2026. |
| MFU | "模型 FLOP 利用率" | 实际 FLOPs / 理论峰值；2026 年稠密 40%、MoE 30% 是好的。 |
| Val loss | "Held-out loss" | Cross-entropy on data the model never saw; overfit detector. |
| 验证损失 | "留出损失" | 模型从未见过的数据上的交叉熵；过拟合检测器。 |

## Further Reading | 延伸阅读

- [The Annotated Transformer (Harvard NLP)](https://nlp.seas.harvard.edu/annotated-transformer/) — the classic annotated implementation.
  中文翻译：哈佛 NLP 的注解版 Transformer，经典参考实现。
