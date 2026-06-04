# GPT — Causal Language Modeling | GPT — 因果语言模型

> BERT 两边都看。GPT 只看过往。三角掩码是现代 AI 中影响最深远的一行代码。

> **【中文解读】** GPT 是 Decoder-only Transformer，用因果掩码（下三角矩阵）防止看到未来 token。GPT-2/3/4 都是这个架构。理解因果掩码 = 理解自回归生成。

**类型：** 构建
**语言：** Python
**前置条件：** 阶段 7 · 02（自注意力），阶段 7 · 05（完整 Transformer），阶段 7 · 06（BERT）
**时长：** 约 75 分钟

## 问题引入

语言模型回答一个问题：给定前 `t-1` 个 token，token `t` 的概率分布是什么？在这个信号上训练——下一个 token 预测——你得到一个可以逐个 token 生成任意文本的模型。

为了在整个序列上并行地端到端训练它，你需要每个位置的预测仅依赖更早的位置。否则模型会通过看答案轻松作弊。

因果掩码做到了这一点。它是一个 `-inf` 值的上三角矩阵，在 softmax 前加到注意力分数上。softmax 后，这些位置变为 0。每个位置只能关注自身和更早的位置。因为你只对整个序列应用一次，一次前向传播就得到 N 个并行的下一个 token 预测。

GPT-1（2018）、GPT-2（2019）、GPT-3（2020）、GPT-4（2023）、GPT-5（2024）、Claude、Llama、Qwen、Mistral、DeepSeek、Kimi——它们都是具有相同核心循环的纯解码器因果 Transformer。只是更大、更好的数据和更好的 RLHF。

> **【中文解读】** 因果掩码是现代 AI 中最重要的一行代码。一个上三角矩阵（-inf 值），加到注意力分数上，经 softmax 后被遮蔽位置变为 0。每个位置只能关注自身及之前的 token。训练时并行计算 N 个下一个 token 预测，推理时逐个生成。

## 核心概念

![因果掩码创建三角注意力矩阵](../assets/causal-attention.svg)

### 掩码

给定长度为 `N` 的序列，构建一个 `N × N` 矩阵：

```
M[i, j] = 0       如果 j <= i
M[i, j] = -inf    如果 j > i
```

在 softmax 前将 `M` 加到原始注意力分数上。`exp(-inf) = 0`，所以被掩码的位置贡献零权重。注意力矩阵的每一行只是之前位置上的概率分布。

实现成本：一次 `torch.tril()` 调用。计算时间：纳秒级。对该领域的影响：一切。

### 并行训练，串行推理

训练：一次前向传播整个 `(N, d_model)` 序列，计算 N 个交叉熵损失（每个位置一个），求和，反向传播。沿序列并行。这就是 GPT 训练可扩展的原因——你可以在一次 GPU 传递中批量处理 1M 个 token。

推理：你逐个 token 生成。输入 `[t1, t2, t3]`，得到 `t4`。输入 `[t1, t2, t3, t4]`，得到 `t5`。输入 `[t1, t2, t3, t4, t5]`，得到 `t6`。KV 缓存（第 12 课）保存了 `t1…tn` 的隐藏状态，这样你不必每步都重新计算它们。但推理时的串行深度 = 输出长度。这就是自回归税，也是为什么解码是每个 LLM 的延迟瓶颈。

### 损失——偏移一位

给定 token `[t1, t2, t3, t4]`：

- 输入：`[t1, t2, t3]`
- 目标：`[t2, t3, t4]`

对每个位置 `i`，计算 `-log P(target_i | inputs[:i+1])`。求和。这就是整个序列的交叉熵。

你听说过的每个 Transformer LM 都在这个损失上训练。预训练、微调、SFT——相同的损失，不同的数据。

> **【拓展：Teacher Forcing 与暴露偏差】** GPT 训练使用 teacher forcing——每步输入真实前一个 token 而非模型自己的预测。这导致"暴露偏差"（exposure bias）：训练时模型从未见过自己的错误输出，推理时却必须从自己的输出继续生成。Scheduled sampling 和 RLHF 是缓解这一问题的两种方法。

### 解码策略

训练后，采样选择比人们想象的更重要。

| 方法 | 它做什么 | 何时使用 |
|------|---------|---------|
| 贪心 | 每步取 argmax | 确定性任务，代码补全 |
| 温度 | 将 logits 除以 T，采样 | 创意任务，更高的 T = 更多多样性 |
| Top-k | 仅从 top-k token 中采样 | 消除低概率尾部 |
| Top-p（核采样） | 从累积概率 >= p 的最小集合中采样 | 2020+ 默认；适应分布形状 |
| Min-p | 保留 `p > min_p * max_p` 的 token | 2024+；比 top-p 更好地拒绝长尾 |
| 推测解码 | 草案模型提出 N 个 token，大模型验证 | 相同质量下 2-3 倍延迟降低 |

2026 年，min-p + 温度 0.7 是开源模型的合理默认。推测解码是任何生产推理栈的标配。

> **【中文解读】** 解码策略的选择直接影响生成质量。贪心搜索（argmax）适合确定性任务，温度采样增加多样性，top-p/min-p 截断低概率尾部。2026 年的推荐默认：min-p + temperature 0.7，比传统的 top-p 能更好地处理分布的锐度变化。

> **【拓展：从 GPT-2 到 GPT-4 的规模跳跃】** GPT-2（1.5B 参数）→ GPT-3（175B）→ GPT-4（估计 1.8T MoE）的规模跳跃中，架构变化很小，但数据和训练方法的改进巨大。GPT-4 使用了 MoE（混合专家）架构和更高质量的数据配比，加上 RLHF 对齐训练。这验证了"规模即一切"的假设，但也表明数据质量和后训练同样关键。

### "GPT 配方"成功的原因

1. **纯解码器。** 没有编码器开销。每层一次注意力 + FFN 传递。
2. **缩放。** 124M → 1.5B → 175B → 万亿。Chinchilla 缩放定律（第 13 课）告诉你如何花费计算。
3. **上下文学习。** 约在 6B-13B 参数时涌现。模型可以遵循少样本示例而无需微调。
4. **RLHF。** 对人类偏好的后训练将原始预训练文本转化为聊天助手。
5. **前归一化 + RoPE + SwiGLU。** 大规模下的稳定训练。

自 GPT-2 以来核心架构没有太大变化。有趣的创新发生在数据、规模和后训练中。

> **【中文解读】** GPT 的成功要素：Decoder-only 架构的简洁性、规模扩展（从 124M 到万亿参数）、上下文学习能力（约 6B 参数开始涌现）、RLHF 后训练（将预训练文本转化为对话助手）、以及现代块设计（Pre-norm + RoPE + SwiGLU）。核心架构自 GPT-2 以来变化不大，创新主要在数据、规模和后训练。

> **【拓展：自回归生成的推理瓶颈】** GPT 的核心矛盾：训练时并行计算整个序列（高效），推理时必须逐 token 生成（串行）。KV 缓存（Lesson 12）和推测解码（Lesson 16）是缓解推理延迟的两个关键技术。在生产系统中，推理延迟通常是最大的工程挑战，直接决定了用户体验和成本。

## 动手实现

### 步骤 1：因果掩码

参见 `code/main.py`。一行代码：

```python
def causal_mask(n):
    return [[0.0 if j <= i else float("-inf") for j in range(n)] for i in range(n)]
```

在 softmax 前将其加到注意力分数上。这就是整个机制。

### 步骤 2：一个 2 层类 GPT 模型

堆叠两个解码器块（掩码自注意力 + FFN，无交叉注意力）。添加 token 嵌入、位置编码和反嵌入（与 token 嵌入矩阵共享——GPT-2 以来的标准技巧）。

### 步骤 3：下一个 token 预测，端到端

在 20 个 token 的玩具词汇表上，在每个位置产生 logits。对偏移一位的目标计算交叉熵损失。无梯度——这是前向传播健全性检查。

### 步骤 4：采样

实现贪心、温度、top-k、top-p、min-p。在固定提示上运行每个并比较输出。采样函数只需 10 行。

## 用框架实现

PyTorch，2026 年惯用法：

```python
from transformers import AutoModelForCausalLM, AutoTokenizer
model = AutoModelForCausalLM.from_pretrained("meta-llama/Llama-3.2-3B-Instruct")
tok = AutoTokenizer.from_pretrained("meta-llama/Llama-3.2-3B-Instruct")

prompt = "Attention is all you need because"
inputs = tok(prompt, return_tensors="pt")
out = model.generate(
    **inputs,
    max_new_tokens=64,
    temperature=0.7,
    top_p=0.9,
    do_sample=True,
)
print(tok.decode(out[0]))
```

底层上，`generate()` 运行前向传播，提取最终位置的 logits，采样下一个 token，追加，然后重复。每个生产 LLM 推理栈（vLLM、TensorRT-LLM、llama.cpp、Ollama、MLX）都实现了相同的循环并进行大量优化——批量预填充、连续批处理、KV 缓存分页、推测解码。

**GPT vs BERT，各一句话：** GPT 预测 `P(x_t | x_{<t})`。BERT 预测 `P(x_masked | x_unmasked)`。损失函数决定模型是否能生成。

## 产出物

参见 `outputs/skill-sampling-tuner.md`。该技能为新的生成任务选择采样参数，并在需要确定性解码时发出警告。

## 练习题

1. **简单。** 运行 `code/main.py` 并验证 softmax 后因果注意力矩阵是下三角的。抽查：第 3 行应该只在第 0-3 列有权重。
2. **中等。** 实现宽度 4 的束搜索。在 10 个短提示上比较束-4 与贪心的困惑度。束搜索总是赢吗？（提示：翻译通常赢，开放式聊天不一定。）
3. **困难。** 实现推测解码：用一个微型 2 层模型作为草案，一个 6 层模型作为验证器。在 100 个长度为 64 的补全上测量时间开销加速。确认输出与验证器的贪心输出匹配。

## 术语速查表

| 术语 | 人们的说法 | 实际含义 |
|------|-----------|---------|
| 因果掩码 | "三角形" | 加到注意力分数上的上三角 `-inf` 矩阵，使位置 `i` 只能看到位置 `≤ i`。 |
| 下一个 token 预测 | "损失函数" | 模型分布对每个位置真实下一个 token 的交叉熵。 |
| 自回归 | "一次生成一个" | 将输出反馈为输入；仅在训练时并行，不在生成时。 |
| Logits | "softmax 前的分数" | LM 头在 softmax 前的原始输出；采样在这些上面进行。 |
| 温度 | "创造力旋钮" | 将 logits 除以 T；T→0 = 贪心，T→∞ = 均匀。 |
| Top-p | "核采样" | 将分布截断为总和 >= p 的最小集合；从剩余部分采样。 |
| Min-p | "比 top-p 更好" | 保留 `p ≥ min_p × max_p` 的 token；截断截止点适应分布的锐度。 |
| 推测解码 | "草案 + 验证" | 廉价模型提出 N 个 token；大模型并行验证。 |
| Teacher forcing | "训练技巧" | 训练时，输入真实的前一个 token，而非模型的预测。每个 seq2seq LM 的标准做法。 |

## 延伸阅读

- [Radford 等人（2018）。Improving Language Understanding by Generative Pre-Training](https://cdn.openai.com/research-covers/language-unsupervised/language_understanding_paper.pdf) —— GPT-1。
- [Radford 等人（2019）。Language Models are Unsupervised Multitask Learners](https://cdn.openai.com/better-language-models/language_models_are_unsupervised_multitask_learners.pdf) —— GPT-2。
- [Brown 等人（2020）。Language Models are Few-Shot Learners](https://arxiv.org/abs/2005.14165) —— GPT-3 和上下文学习。
- [Leviathan, Kalman, Matias（2023）。Fast Inference from Transformers via Speculative Decoding](https://arxiv.org/abs/2211.17192) —— 推测解码论文。
- [HuggingFace `modeling_llama.py`](https://github.com/huggingface/transformers/blob/main/src/transformers/models/llama/modeling_llama.py) —— 规范的因果 LM 参考代码。
