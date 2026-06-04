# Build a Transformer from Scratch — The Capstone | 从零构建 Transformer — 毕业项目

> 十三节课。一个模型。没有捷径。

> **【中文解读】** 整合所有知识，从零实现完整的 GPT 架构。这是本阶段的核心实践——理解这个，你就能读懂任何 Transformer 的代码。

**类型：** 构建
**语言：** Python
**前置条件：** 阶段 7 · 01 到 13。不要跳过。
**时长：** 约 120 分钟

## 问题引入

你读了每篇论文。你实现了注意力、多头拆分、位置编码、编码器和解码器块、BERT 和 GPT 损失、MoE、KV 缓存。现在把它们在一个真实任务上协同工作。

毕业项目：在字符级语言建模任务上端到端训练一个小型纯解码器 Transformer。它读莎士比亚。它生成新的莎士比亚。它足够小，可以在笔记本上不到 10 分钟内训练。它足够正确，换成更大的数据集和更长的训练就能得到一个真正的 LM。

这是本课程的"nanoGPT"。它不是原创的——Karpathy 2023 年的 nanoGPT 教程是每个学生至少写一次的参考实现。我们借用其形状并根据我们学过的内容重新调整。

> **【中文解读】** 这个毕业项目将前 13 节课的所有知识整合：字符级语言建模、token 嵌入、位置编码、RMSNorm、多头因果注意力、SwiGLU FFN、残差连接，训练一个能在笔记本上 10 分钟内完成的 Shakespeare 生成器。虽然小，但架构与 GPT-4 相同——增大数据和训练量就能得到真正的语言模型。

> **【拓展：从 nanoGPT 到生产级 LLM】** Karpathy 的 nanoGPT 是学习 Transformer 的最佳起点。从 nanoGPT 到生产级 LLM 的关键差异在于：数据规模（从 MB 到 TB）、训练基础设施（从单 GPU 到数千 GPU 集群）、分布式训练（数据并行、模型并行、流水线并行）、以及后训练（SFT + RLHF）。但核心架构是一样的。

## 核心概念

![Transformer-from-scratch 块图](../assets/capstone.svg)

架构，带注释：

```
输入 token (B, N)
   │
   ▼
token 嵌入 + 位置嵌入  ◀── 第 04 课（RoPE 选项）
   │
   ▼
┌──── block × L ────────────────────┐
│  RMSNorm                          │  ◀── 第 05 课
│  MultiHeadAttention (因果)        │  ◀── 第 03 课 + 07 课（因果掩码）
│  残差连接                         │
│  RMSNorm                          │
│  SwiGLU FFN                       │  ◀── 第 05 课
│  残差连接                         │
└────────────────────────────────── ┘
   │
   ▼
最终 RMSNorm
   │
   ▼
lm_head（与 token 嵌入共享）
   │
   ▼
logits (B, N, V)
   │
   ▼
偏移一位交叉熵                    ◀── 第 07 课
```

### 我们要交付的

- `GPTConfig` —— 一个地方配置所有超参数。
- `MultiHeadAttention` —— 因果、批量化的，带可选 Flash 风格路径（PyTorch 的 `scaled_dot_product_attention`）。
- `SwiGLUFFN` —— 现代 FFN。
- `Block` —— 前归一化，残差包装的注意力 + FFN。
- `GPT` —— 嵌入，堆叠块，LM 头，generate()。
- 训练循环，使用 AdamW，余弦学习率，梯度裁剪。
- Shakespeare 文本上的字符级分词器。

> **【中文解读】** 完整的 GPT 实现包含：配置类、多头因果注意力（可选 Flash Attention）、SwiGLU FFN、前归一化残差块、完整的 GPT 模型类（嵌入 + 堆叠块 + LM 头 + 生成函数）、AdamW + 余弦学习率训练循环。为了简洁，使用了学习式位置嵌入（而非 RoPE）且未实现 KV 缓存，但练习要求你添加这些。

### 我们不交付的

- RoPE —— 在第 04 课中概念上实现了。这里为了简洁使用学习式位置嵌入。练习要求你替换为 RoPE。
- 生成时的 KV 缓存 —— 每个生成步骤重新计算完整前缀的注意力。更慢但更简单。练习要求你添加 KV 缓存。
- Flash Attention —— PyTorch 2.0+ 在输入匹配时自动调用；我们使用 `F.scaled_dot_product_attention`。
- MoE —— 每块单个 FFN。你在第 11 课中看到了 MoE。

### 目标指标

在 Mac M2 笔记本上，一个 4 层、4 头、d_model=128 的 GPT 在 `tinyshakespeare.txt` 上训练 2,000 步：

- 训练损失在约 6 分钟内从约 4.2（随机）收敛到约 1.5。
- 采样输出看起来像莎士比亚风格的：古词、换行、"ROMEO:"等专有名词出现。
- 验证损失（留出的最后 10% 文本）紧跟训练损失；此大小/预算下无过拟合。

> **【拓展：从字符级到子词级 Tokenizer】** 本项目使用字符级 tokenizer（简单但低效）。生产级 LLM 使用 BPE（Byte Pair Encoding）或 SentencePiece 等子词级 tokenizer。Llama 使用 BPE，GPT-4 使用 cl100k_base BPE tokenizer。子词 tokenization 在词汇量、序列长度和语义粒度之间取得平衡，是现代 LLM 的标配。

## 动手实现

本课使用 PyTorch。安装 `torch`（CPU 构建即可）。参见 `code/main.py`。脚本处理：

- 下载 `tinyshakespeare.txt`（如果缺失）或读取本地副本。
- 字节级字符分词器。
- 90/10 训练/验证拆分。
- 支持硬件上使用 bf16 autocast 的训练循环。
- 训练完成后采样。

### 步骤 1：数据

```python
text = open("tinyshakespeare.txt").read()
chars = sorted(set(text))
stoi = {c: i for i, c in enumerate(chars)}
itos = {i: c for c, i in stoi.items()}
encode = lambda s: [stoi[c] for c in s]
decode = lambda xs: "".join(itos[x] for x in xs)
```

65 个唯一字符。微型词汇表。适合 4 字节的 vocab_size。没有 BPE，没有分词器问题。

### 步骤 2：模型

参见 `code/main.py`。块是第 05 课的教科书实现——前归一化，RMSNorm，SwiGLU，因果 MHA。4/4/128 的参数量：约 800K。

### 步骤 3：训练循环

获取一个随机的长度 256 token 窗口批次。前向传播。偏移一位交叉熵。反向传播。AdamW 步进。记录。重复。

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

### 步骤 4：采样

给定一个提示，重复前向传播、从 top-p logits 采样、追加、继续。500 个 token 后停止。

### 步骤 5：阅读输出

2,000 步后：

```
ROMEO:
Away and mild will not thy friend, that thou shalt wit:
The chief that well shame and hath been his friends,
...
```

不是莎士比亚。但是莎士比亚风格的。约 800K 参数和笔记本上 6 分钟的明确胜利。

## 用框架实现

这个毕业项目是一个参考架构。三个扩展方向将其变成真正的东西：

1. **替换分词器。** 使用 BPE（例如 `tiktoken.get_encoding("cl100k_base")`）。词汇量从 65 跳到约 50,000。模型容量需要相应扩展。
2. **在更大的语料库上训练。** 使用 `OpenWebText` 或 `fineweb-edu`（HuggingFace）。单个 A100 上 125M 参数 GPT 训练 10B token 约需 24 小时。
3. **添加 RoPE + KV 缓存 + Flash Attention。** 下面的练习引导你完成每一个。

这最终成为一个 125M 参数的 GPT，能生成流利的英语。不是前沿模型。但相同的代码路径——只是更大——是 Karpathy、EleutherAI 和 Allen Institute 在 2026 年训练研究检查点的方式。

> **【拓展：Karpathy 的 nanoGPT 与教育意义】** Andrej Karpathy 的 nanoGPT（2023）是 AI 教育史上最有影响力的教程之一。它证明了一个完整、可训练的 GPT 可以用约 300 行 PyTorch 实现。这种"从零构建"的教学方法让你真正理解每个组件的作用，而不是把 Transformer 当作黑盒。

## 产出物

参见 `outputs/skill-transformer-review.md`。该技能根据前 13 课的所有内容审查从零构建的 Transformer 实现的正确性。

## 练习题

1. **简单。** 运行 `code/main.py`。验证你训练模型的最终步验证损失低于 2.0。将 `max_steps` 从 2,000 改为 5,000——验证损失是否继续改善？
2. **中等。** 用 RoPE 替换学习式位置嵌入。在 `MultiHeadAttention` 内部对 Q 和 K 应用旋转。训练并验证验证损失至少同样低。
3. **中等。** 在采样循环中实现 KV 缓存。带缓存和不带缓存各生成 500 个 token。时间开销应改善 5-20 倍（笔记本上）。
4. **困难。** 为模型添加第二个预测下一个加一个 token 的头（MTP——来自 DeepSeek-V3 的 Multi-Token Prediction）。联合训练。是否有帮助？
5. **困难。** 将每块的单个 FFN 替换为 4 专家 MoE。路由器 + top-2 路由。观察匹配活跃参数下验证损失的变化。

## 术语速查表

| 术语 | 人们的说法 | 实际含义 |
|------|-----------|---------|
| nanoGPT | "Karpathy 的教程仓库" | 最小纯解码器 Transformer 训练代码，约 300 LOC；规范参考。 |
| tinyshakespeare | "标准玩具语料库" | 约 1.1 MB 文本；2015 年以来每个字符级 LM 教程都使用它。 |
| 共享嵌入 | "共享输入/输出矩阵" | LM 头权重 = token 嵌入矩阵的转置；节省参数，改善质量。 |
| bf16 autocast | "训练精度技巧" | 在 bf16 中运行前向/反向，保持优化器状态在 fp32；2021 年以来的标准。 |
| 梯度裁剪 | "阻止尖峰" | 将全局梯度范数限制在 1.0；防止训练爆炸。 |
| 余弦学习率调度 | "2020+ 默认" | 学习率线性预热，然后余弦衰减到峰值的 10%。 |
| MFU | "模型 FLOP 利用率" | 实际 FLOP / 理论峰值；2026 年 40% 稠密、30% MoE 为强。 |
| 验证损失 | "留出损失" | 模型从未见过的数据上的交叉熵；过拟合检测器。 |

## 延伸阅读

- [The Annotated Transformer（Harvard NLP）](https://nlp.seas.harvard.edu/annotated-transformer/) —— 经典的注释实现。
