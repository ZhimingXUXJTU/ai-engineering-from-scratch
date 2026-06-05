# GPT — Causal Language Modeling | GPT — 因果语言模型

> BERT sees both sides. GPT sees only the past. The triangle mask is the most consequential single line of code in modern AI.

> **【中文解读】** GPT 是 Decoder-only Transformer，用因果掩码（下三角矩阵）防止看到未来 token。GPT-2/3/4 都是这个架构。理解因果掩码 = 理解自回归生成。

**Type:** Hands-on | **类型:** 动手
**Language:** Python | **语言:** Python
**Prerequisites:** Phase 7 · 02 (Self-Attention), Phase 7 · 05 (Full Transformer), Phase 7 · 06 (BERT) | **前置知识:** Phase 7 · 02 (Self-Attention), Phase 7 · 05 (Full Transformer), Phase 7 · 06 (BERT)
**Time:** ~75 minutes | **时间:** ~75 分钟

## The Problem | 问题引入

A language model answers one question: given the first `t-1` tokens, what is the probability distribution over token `t`? Train on that signal — next-token prediction — and you get a model that can generate arbitrary text one token at a time.

> 语言模型回答一个问题：给定前 `t-1` 个 token，第 `t` 个 token 的概率分布是什么？在这个信号——下一个 token 预测——上训练，你就能得到一个可以逐 token 生成任意文本的模型。

To train it end-to-end on a whole sequence in parallel, you need each position's prediction to depend only on earlier positions. Otherwise the model trivially cheats by looking at the answer.

> 要在整个序列上端到端并行训练，你需要每个位置的预测只依赖之前的位置。否则模型会直接看到答案，"作弊"地完成任务。

The causal mask does this. It is a single upper-triangular matrix of `-inf` values added to attention scores before softmax. After softmax, those positions become 0. Each position can attend only to itself and earlier positions. And because you apply it once to the whole sequence, you get N parallel next-token predictions in one forward pass.

> 因果掩码实现了这一点。它是一个上三角矩阵（`-inf` 值），加到 softmax 之前的注意力分数上。softmax 后，这些位置变为 0。每个位置只能关注自身及之前的位置。因为对整个序列只应用一次，所以一次前向传播就能得到 N 个并行的下一个 token 预测。

GPT-1 (2018), GPT-2 (2019), GPT-3 (2020), GPT-4 (2023), GPT-5 (2024), Claude, Llama, Qwen, Mistral, DeepSeek, Kimi — they are all decoder-only causal transformers with the same core loop. Just bigger, better data, and better RLHF.

> GPT-1（2018）、GPT-2（2019）、GPT-3（2020）、GPT-4（2023）、GPT-5（2024）、Claude、Llama、Qwen、Mistral、DeepSeek、Kimi——它们都是解码器专用因果 Transformer，核心循环相同。只是更大、数据更好、RLHF 更好。

> **【中文解读】** 因果掩码是现代 AI 中最重要的一行代码。一个上三角矩阵（-inf 值），加到注意力分数上，经 softmax 后被遮蔽位置变为 0。每个位置只能关注自身及之前的 token。训练时并行计算 N 个下一个 token 预测，推理时逐个生成。

## The Concept | 核心概念

![Causal mask creates a triangular attention matrix](../assets/causal-attention.svg)

### The mask

Given a sequence of length `N`, build an `N × N` matrix:

> 给定长度为 `N` 的序列，构建一个 `N × N` 矩阵：

```
M[i, j] = 0       if j <= i
M[i, j] = -inf    if j > i
```

Add `M` to the raw attention scores before softmax. `exp(-inf) = 0`, so masked positions contribute zero weight. Each row of the attention matrix is a probability distribution over previous positions only.

> 将 `M` 加到 softmax 之前的原始注意力分数上。`exp(-inf) = 0`，所以被掩码位置的权重为零。注意力矩阵的每行只是前序位置上的概率分布。

Implementation cost: one `torch.tril()` call. Time to compute: nanoseconds. Impact on the field: everything.

> 实现成本：一行 `torch.tril()` 调用。计算时间：纳秒级。对整个领域的影响：改变了一切。

### Parallel training, serial inference

Training: forward-pass the whole `(N, d_model)` sequence once, compute N cross-entropy losses (one per position), sum, backprop. Parallel along the sequence. This is why GPT training scales — you process 1M tokens in a batch in one GPU pass.

> 训练：对整个 `(N, d_model)` 序列做一次前向传播，计算 N 个交叉熵损失（每个位置一个），求和，反向传播。沿序列并行。这就是 GPT 训练可扩展的原因——一次 GPU 通行就能处理批量中的 1M 个 token。

Inference: you generate token by token. Feed `[t1, t2, t3]`, get `t4`. Feed `[t1, t2, t3, t4]`, get `t5`. Feed `[t1, t2, t3, t4, t5]`, get `t6`. The KV cache (Lesson 12) saves the hidden states of `t1…tn` so you don't recompute them each step. But serial depth at inference = output length. That is the autoregressive tax and why decoding is the latency bottleneck of every LLM.

> 推理：逐 token 生成。输入 `[t1, t2, t3]`，得到 `t4`。输入 `[t1, t2, t3, t4]`，得到 `t5`。输入 `[t1, t2, t3, t4, t5]`，得到 `t6`。KV 缓存（第 12 课）保存了 `t1…tn` 的隐藏状态，避免每步重复计算。但推理时的串行深度 = 输出长度。这就是自回归的代价，也是解码成为每个 LLM 延迟瓶颈的原因。

### The loss — shift-by-one

Given tokens `[t1, t2, t3, t4]`:

> 给定 token `[t1, t2, t3, t4]`：

- Input: `[t1, t2, t3]`
  中文翻译：输入：`[t1, t2, t3]`
- Targets: `[t2, t3, t4]`
  中文翻译：目标：`[t2, t3, t4]`

For every position `i`, compute `-log P(target_i | inputs[:i+1])`. Sum. This is the cross-entropy for the whole sequence.

> 对每个位置 `i`，计算 `-log P(target_i | inputs[:i+1])`。求和。这就是整个序列的交叉熵。

Every transformer LM you've heard of trains on this loss. Pre-training, fine-tuning, SFT — same loss, different data.

> 你听说过的每个 Transformer 语言模型都在这个损失上训练。预训练、微调、SFT——同样的损失，不同的数据。

> **【拓展：Teacher Forcing 与暴露偏差】** GPT 训练使用 teacher forcing——每步输入真实前一个 token 而非模型自己的预测。这导致"暴露偏差"（exposure bias）：训练时模型从未见过自己的错误输出，推理时却必须从自己的输出继续生成。Scheduled sampling 和 RLHF 是缓解这一问题的两种方法。

### Decoding strategies

After training, sampling choices matter more than people think.

> 训练完成后，采样策略的选择比人们想象的更重要。

| Method | What it does | When to use |
|--------|--------------|-------------|
| 方法 | 功能 | 适用场景 |
| Greedy | Argmax every step | Deterministic tasks, code completion |
| 贪心 | 每步取最大值 | 确定性任务、代码补全 |
| Temperature | Divide logits by T, sample | Creative tasks, higher T = more diversity |
| 温度 | 将 logits 除以 T 后采样 | 创意任务，T 越高多样性越大 |
| Top-k | Sample from top-k tokens only | Kills low-probability tails |
| Top-k | 只从概率最高的 k 个 token 采样 | 消除低概率尾部 |
| Top-p (nucleus) | Sample from smallest set with cumulative prob ≥ p | 2020+ default; adapts to distribution shape |
| Top-p（核采样） | 从累积概率 ≥ p 的最小集合中采样 | 2020+ 默认策略；自适应分布形状 |
| Min-p | Keep tokens with `p > min_p * max_p` | 2024+; better at rejecting long tails than top-p |
| Min-p | 保留 `p > min_p * max_p` 的 token | 2024+；比 top-p 更好地拒绝长尾 |
| Speculative decoding | Draft model proposes N tokens, big model verifies | 2–3× latency reduction at same quality |
| 推测解码 | 草案模型提出 N 个 token，大模型验证 | 相同质量下延迟降低 2-3 倍 |

In 2026, min-p + temperature 0.7 is a reasonable default for open-weights models. Speculative decoding is table stakes for any production inference stack.

> 在 2026 年，min-p + temperature 0.7 是开源模型的合理默认配置。推测解码已成为任何生产推理系统的标配。

> **【中文解读】** 解码策略的选择直接影响生成质量。贪心搜索（argmax）适合确定性任务，温度采样增加多样性，top-p/min-p 截断低概率尾部。2026 年的推荐默认：min-p + temperature 0.7，比传统的 top-p 能更好地处理分布的锐度变化。

> **【拓展：从 GPT-2 到 GPT-4 的规模跳跃】** GPT-2（1.5B 参数）→ GPT-3（175B）→ GPT-4（估计 1.8T MoE）的规模跳跃中，架构变化很小，但数据和训练方法的改进巨大。GPT-4 使用了 MoE（混合专家）架构和更高质量的数据配比，加上 RLHF 对齐训练。这验证了"规模即一切"的假设，但也表明数据质量和后训练同样关键。

### What made the "GPT recipe" work

1. **Decoder-only.** No encoder overhead. One pass of attention + FFN per layer.
   中文翻译：**解码器专用。** 没有编码器开销。每层一次注意力 + FFN 通行。
2. **Scaling.** 124M → 1.5B → 175B → trillions. Chinchilla scaling laws (Lesson 13) tell you how to spend compute.
   中文翻译：**规模扩展。** 从 124M 到 1.5B 到 175B 再到万亿参数。Chinchilla 缩放定律（第 13 课）告诉你如何分配计算资源。
3. **In-context learning.** Emerged around 6B–13B. The model can follow few-shot examples without fine-tuning.
   中文翻译：**上下文学习。** 约在 6B-13B 参数时涌现。模型无需微调就能遵循少样本示例。
4. **RLHF.** Post-training on human preferences converted raw pretrained text into chat assistants.
   中文翻译：**RLHF。** 在人类偏好上进行后训练，将原始预训练文本转化为对话助手。
5. **Pre-norm + RoPE + SwiGLU.** Stable training at scale.
   中文翻译：**Pre-norm + RoPE + SwiGLU。** 大规模稳定训练。

The core architecture hasn't changed much since GPT-2. Everything interesting has happened in data, scale, and post-training.

> 自 GPT-2 以来，核心架构变化不大。所有有趣的事情都发生在数据、规模和后训练方面。

> **【中文解读】** GPT 的成功要素：Decoder-only 架构的简洁性、规模扩展（从 124M 到万亿参数）、上下文学习能力（约 6B 参数开始涌现）、RLHF 后训练（将预训练文本转化为对话助手）、以及现代块设计（Pre-norm + RoPE + SwiGLU）。核心架构自 GPT-2 以来变化不大，创新主要在数据、规模和后训练。

> **【拓展：自回归生成的推理瓶颈】** GPT 的核心矛盾：训练时并行计算整个序列（高效），推理时必须逐 token 生成（串行）。KV 缓存（Lesson 12）和推测解码（Lesson 16）是缓解推理延迟的两个关键技术。在生产系统中，推理延迟通常是最大的工程挑战，直接决定了用户体验和成本。

## Build It | 动手实现

### Step 1: the causal mask

See `code/main.py`. A one-liner:

> 参见 `code/main.py`。一行代码：

```python
def causal_mask(n):
    return [[0.0 if j <= i else float("-inf") for j in range(n)] for i in range(n)]
```

Add it to attention scores before softmax. That's the entire mechanism.

> 将它加到 softmax 之前的注意力分数上。这就是全部机制。

### Step 2: a 2-layer GPT-ish model

Stack two decoder blocks (masked self-attention + FFN, no cross-attention). Add a token embedding, a positional encoding, and an unembedding (tied to the token embedding matrix — a standard trick since GPT-2).

> 堆叠两个解码器块（掩码自注意力 + FFN，无交叉注意力）。添加 token 嵌入、位置编码和反嵌入（与 token 嵌入矩阵绑定——GPT-2 以来的标准技巧）。

### Step 3: next-token prediction, end-to-end

On a 20-token toy vocab, produce logits at every position. Compute cross-entropy loss against the shift-by-one target. No gradient — this is a forward-pass sanity check.

> 在 20 个 token 的玩具词表上，在每个位置生成 logits。对偏移一位的目标计算交叉熵损失。不涉及梯度——这是前向传播的合理性检查。

### Step 4: sampling

Implement greedy, temperature, top-k, top-p, min-p. Run each on a fixed prompt and compare outputs. A sampling function is 10 lines.

> 实现贪心、温度、top-k、top-p、min-p 采样。在固定提示上分别运行并比较输出。一个采样函数只需 10 行代码。

## Use It | 用框架实现

PyTorch, 2026 idiom:

> PyTorch，2026 年的惯用写法：

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

Under the hood, `generate()` runs the forward pass, pulls the final-position logits, samples the next token, appends it, and repeats. Every production LLM inference stack (vLLM, TensorRT-LLM, llama.cpp, Ollama, MLX) implements the same loop with heavy optimization — batched prefill, continuous batching, KV cache paging, speculative decoding.

> 在底层，`generate()` 运行前向传播，取出最后位置的 logits，采样下一个 token，追加到序列中，重复。每个生产 LLM 推理栈（vLLM、TensorRT-LLM、llama.cpp、Ollama、MLX）都用大量优化实现相同的循环——批量预填充、连续批处理、KV 缓存分页、推测解码。

**GPT vs BERT, one line each:** GPT predicts `P(x_t | x_{<t})`. BERT predicts `P(x_masked | x_unmasked)`. The loss determines whether the model can generate.

> **GPT 与 BERT 各一句话：** GPT 预测 `P(x_t | x_{<t})`。BERT 预测 `P(x_masked | x_unmasked)`。损失函数决定了模型是否能生成。

## Ship It | 产出物

See `outputs/skill-sampling-tuner.md`. The skill picks sampling parameters for a new generation task and flags when deterministic decoding is required.

> 参见 `outputs/skill-sampling-tuner.md`。该 skill 为新的生成任务选择采样参数，并标记何时需要确定性解码。

## Exercises | 练习题

1. **Easy.** Run `code/main.py` and verify the causal attention matrix is lower-triangular after softmax. Spot-check: row 3 should have weights only in columns 0–3.
   中文翻译：运行 `code/main.py`，验证因果注意力矩阵在 softmax 后是下三角的。抽查：第 3 行应该只在第 0-3 列有权重。
2. **Medium.** Implement beam search for width 4. Compare perplexity of beam-4 vs greedy on 10 short prompts. Does beam always win? (Hint: usually for translation, not for open-ended chat.)
   中文翻译：实现宽度为 4 的束搜索。在 10 个短提示上比较束搜索和贪心搜索的困惑度。束搜索一定更好吗？（提示：通常翻译任务有优势，开放式对话则不然。）
3. **Hard.** Implement speculative decoding: use a tiny 2-layer model as the draft and a 6-layer model as the verifier. Measure wall-clock speedup on 100 completions of length 64. Confirm outputs match greedy of the verifier.
   中文翻译：实现推测解码：用 2 层小模型作为草案模型，6 层模型作为验证器。在 100 个长度为 64 的补全上测量实际加速比。确认输出与验证器的贪心解码一致。

## Key Terms | 术语速查表

| Term | What people say | What it actually means |
|------|-----------------|-----------------------|
| 术语 | 通俗说法 | 实际含义 |
| Causal mask | "The triangle" | Upper-triangular `-inf` matrix added to attention scores so position `i` only sees positions `≤ i`. |
| 因果掩码 | "三角矩阵" | 加到注意力分数上的上三角 `-inf` 矩阵，使位置 `i` 只能看到位置 `≤ i`。 |
| Next-token prediction | "The loss" | Cross-entropy of the model's distribution against the true next token at every position. |
| 下一个 token 预测 | "损失函数" | 模型分布与每个位置真实下一个 token 之间的交叉熵。 |
| Autoregressive | "Generate one at a time" | Feed output back as input; parallelism only during training, not during generation. |
| 自回归 | "逐个生成" | 将输出反馈为输入；仅在训练时并行，生成时不并行。 |
| Logits | "Pre-softmax scores" | Raw output of the LM head before softmax; sampling happens on these. |
| Logits | "softmax 前的分数" | LM 头在 softmax 之前的原始输出；采样基于这些值。 |
| Temperature | "Creativity knob" | Divide logits by T; T→0 = greedy, T→∞ = uniform. |
| 温度 | "创造力旋钮" | 将 logits 除以 T；T→0 为贪心，T→∞ 为均匀分布。 |
| Top-p | "Nucleus sampling" | Truncate distribution to smallest set summing to ≥p; sample from what remains. |
| Top-p | "核采样" | 将分布截断为累积概率 ≥ p 的最小集合；从剩余部分采样。 |
| Min-p | "Better than top-p" | Keep tokens where `p ≥ min_p × max_p`; adapts cutoff to sharpness of distribution. |
| Min-p | "比 top-p 更好" | 保留 `p ≥ min_p × max_p` 的 token；根据分布锐度自适应调整截断。 |
| Speculative decoding | "Draft + verify" | Cheap model proposes N tokens; big model verifies in parallel. |
| 推测解码 | "草案+验证" | 廉价模型提出 N 个 token；大模型并行验证。 |
| Teacher forcing | "Training trick" | During training, feed the true previous token, not the model's prediction. Standard for every seq2seq LM. |
| Teacher forcing | "训练技巧" | 训练时输入真实的前一个 token，而非模型的预测。所有 seq2seq 语言模型的标准做法。 |

## Further Reading | 延伸阅读

- [Radford et al. (2018). Improving Language Understanding by Generative Pre-Training](https://cdn.openai.com/research-covers/language-unsupervised/language_understanding_paper.pdf) — GPT-1.
  中文翻译：GPT-1 论文。
- [Radford et al. (2019). Language Models are Unsupervised Multitask Learners](https://cdn.openai.com/better-language-models/language_models_are_unsupervised_multitask_learners.pdf) — GPT-2.
  中文翻译：GPT-2 论文。
- [Brown et al. (2020). Language Models are Few-Shot Learners](https://arxiv.org/abs/2005.14165) — GPT-3 and in-context learning.
  中文翻译：GPT-3 和上下文学习论文。
- [Leviathan, Kalman, Matias (2023). Fast Inference from Transformers via Speculative Decoding](https://arxiv.org/abs/2211.17192) — spec decoding paper.
  中文翻译：推测解码论文。
- [HuggingFace `modeling_llama.py`](https://github.com/huggingface/transformers/blob/main/src/transformers/models/llama/modeling_llama.py) — canonical causal-LM reference code.
  中文翻译：HuggingFace Llama 因果语言模型参考代码。
