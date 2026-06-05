# GPT — Causal Language Modeling | GPT — 因果语言模型

> BERT sees both sides. GPT sees only the past. The triangle mask is the most consequential single line of code in modern AI.

> **【中文解读】** GPT 是 Decoder-only Transformer，用因果掩码（下三角矩阵）防止看到未来 token。GPT-2/3/4 都是这个架构。理解因果掩码 = 理解自回归生成。

**Type:**  | **类型:** 动手
**Language:** Python | **语言:** Python | **语言:** Python
**Prerequisites:** Phase 7 · 02 (Self-Attention), Phase 7 · 05 (Full Transformer), Phase 7 · 06 (BERT) | **前置知识:** Phase 7 · 02 (Self-Attention), Phase 7 · 05 (Full Transformer), Phase 7 · 06 (BERT)
**Time:** ~75 minutes | **时间:** ~75 分钟

## The Problem | 问题引入

A language model answers one question: given the first `t-1` tokens, what is the probability distribution over token `t`? Train on that signal — next-token prediction — and you get a model that can generate arbitrary text one token at a time.

To train it end-to-end on a whole sequence in parallel, you need each position's prediction to depend only on earlier positions. Otherwise the model trivially cheats by looking at the answer.

The causal mask does this. It is a single upper-triangular matrix of `-inf` values added to attention scores before softmax. After softmax, those positions become 0. Each position can attend only to itself and earlier positions. And because you apply it once to the whole sequence, you get N parallel next-token predictions in one forward pass.

GPT-1 (2018), GPT-2 (2019), GPT-3 (2020), GPT-4 (2023), GPT-5 (2024), Claude, Llama, Qwen, Mistral, DeepSeek, Kimi — they are all decoder-only causal transformers with the same core loop. Just bigger, better data, and better RLHF.

> **【中文解读】** 因果掩码是现代 AI 中最重要的一行代码。一个上三角矩阵（-inf 值），加到注意力分数上，经 softmax 后被遮蔽位置变为 0。每个位置只能关注自身及之前的 token。训练时并行计算 N 个下一个 token 预测，推理时逐个生成。

## The Concept | 核心概念

![Causal mask creates a triangular attention matrix](../assets/causal-attention.svg)

### The mask

Given a sequence of length `N`, build an `N × N` matrix:

```
M[i, j] = 0       if j <= i
M[i, j] = -inf    if j > i
```

Add `M` to the raw attention scores before softmax. `exp(-inf) = 0`, so masked positions contribute zero weight. Each row of the attention matrix is a probability distribution over previous positions only.

Implementation cost: one `torch.tril()` call. Time to compute: nanoseconds. Impact on the field: everything.

### Parallel training, serial inference

Training: forward-pass the whole `(N, d_model)` sequence once, compute N cross-entropy losses (one per position), sum, backprop. Parallel along the sequence. This is why GPT training scales — you process 1M tokens in a batch in one GPU pass.

Inference: you generate token by token. Feed `[t1, t2, t3]`, get `t4`. Feed `[t1, t2, t3, t4]`, get `t5`. Feed `[t1, t2, t3, t4, t5]`, get `t6`. The KV cache (Lesson 12) saves the hidden states of `t1…tn` so you don't recompute them each step. But serial depth at inference = output length. That is the autoregressive tax and why decoding is the latency bottleneck of every LLM.

### The loss — shift-by-one

Given tokens `[t1, t2, t3, t4]`:

- Input: `[t1, t2, t3]`
- Targets: `[t2, t3, t4]`

For every position `i`, compute `-log P(target_i | inputs[:i+1])`. Sum. This is the cross-entropy for the whole sequence.

Every transformer LM you've heard of trains on this loss. Pre-training, fine-tuning, SFT — same loss, different data.

> **【拓展：Teacher Forcing 与暴露偏差】** GPT 训练使用 teacher forcing——每步输入真实前一个 token 而非模型自己的预测。这导致"暴露偏差"（exposure bias）：训练时模型从未见过自己的错误输出，推理时却必须从自己的输出继续生成。Scheduled sampling 和 RLHF 是缓解这一问题的两种方法。

### Decoding strategies

After training, sampling choices matter more than people think.

| Method | What it does | When to use |
|--------|--------------|-------------|
| Greedy | Argmax every step | Deterministic tasks, code completion |
| Temperature | Divide logits by T, sample | Creative tasks, higher T = more diversity |
| Top-k | Sample from top-k tokens only | Kills low-probability tails |
| Top-p (nucleus) | Sample from smallest set with cumulative prob ≥ p | 2020+ default; adapts to distribution shape |
| Min-p | Keep tokens with `p > min_p * max_p` | 2024+; better at rejecting long tails than top-p |
| Speculative decoding | Draft model proposes N tokens, big model verifies | 2–3× latency reduction at same quality |

In 2026, min-p + temperature 0.7 is a reasonable default for open-weights models. Speculative decoding is table stakes for any production inference stack.

> **【中文解读】** 解码策略的选择直接影响生成质量。贪心搜索（argmax）适合确定性任务，温度采样增加多样性，top-p/min-p 截断低概率尾部。2026 年的推荐默认：min-p + temperature 0.7，比传统的 top-p 能更好地处理分布的锐度变化。

> **【拓展：从 GPT-2 到 GPT-4 的规模跳跃】** GPT-2（1.5B 参数）→ GPT-3（175B）→ GPT-4（估计 1.8T MoE）的规模跳跃中，架构变化很小，但数据和训练方法的改进巨大。GPT-4 使用了 MoE（混合专家）架构和更高质量的数据配比，加上 RLHF 对齐训练。这验证了"规模即一切"的假设，但也表明数据质量和后训练同样关键。

### What made the "GPT recipe" work

1. **Decoder-only.** No encoder overhead. One pass of attention + FFN per layer.
2. **Scaling.** 124M → 1.5B → 175B → trillions. Chinchilla scaling laws (Lesson 13) tell you how to spend compute.
3. **In-context learning.** Emerged around 6B–13B. The model can follow few-shot examples without fine-tuning.
4. **RLHF.** Post-training on human preferences converted raw pretrained text into chat assistants.
5. **Pre-norm + RoPE + SwiGLU.** Stable training at scale.

The core architecture hasn't changed much since GPT-2. Everything interesting has happened in data, scale, and post-training.

> **【中文解读】** GPT 的成功要素：Decoder-only 架构的简洁性、规模扩展（从 124M 到万亿参数）、上下文学习能力（约 6B 参数开始涌现）、RLHF 后训练（将预训练文本转化为对话助手）、以及现代块设计（Pre-norm + RoPE + SwiGLU）。核心架构自 GPT-2 以来变化不大，创新主要在数据、规模和后训练。

> **【拓展：自回归生成的推理瓶颈】** GPT 的核心矛盾：训练时并行计算整个序列（高效），推理时必须逐 token 生成（串行）。KV 缓存（Lesson 12）和推测解码（Lesson 16）是缓解推理延迟的两个关键技术。在生产系统中，推理延迟通常是最大的工程挑战，直接决定了用户体验和成本。

## Build It | 动手实现

### Step 1: the causal mask

See `code/main.py`. A one-liner:

```python
def causal_mask(n):
    return [[0.0 if j <= i else float("-inf") for j in range(n)] for i in range(n)]
```

Add it to attention scores before softmax. That's the entire mechanism.

### Step 2: a 2-layer GPT-ish model

Stack two decoder blocks (masked self-attention + FFN, no cross-attention). Add a token embedding, a positional encoding, and an unembedding (tied to the token embedding matrix — a standard trick since GPT-2).

### Step 3: next-token prediction, end-to-end

On a 20-token toy vocab, produce logits at every position. Compute cross-entropy loss against the shift-by-one target. No gradient — this is a forward-pass sanity check.

### Step 4: sampling

Implement greedy, temperature, top-k, top-p, min-p. Run each on a fixed prompt and compare outputs. A sampling function is 10 lines.

## Use It | 用框架实现

PyTorch, 2026 idiom:

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

**GPT vs BERT, one line each:** GPT predicts `P(x_t | x_{<t})`. BERT predicts `P(x_masked | x_unmasked)`. The loss determines whether the model can generate.

## Ship It | 产出物

See `outputs/skill-sampling-tuner.md`. The skill picks sampling parameters for a new generation task and flags when deterministic decoding is required.

## Exercises | 练习题

1. **Easy.** Run `code/main.py` and verify the causal attention matrix is lower-triangular after softmax. Spot-check: row 3 should have weights only in columns 0–3.
2. **Medium.** Implement beam search for width 4. Compare perplexity of beam-4 vs greedy on 10 short prompts. Does beam always win? (Hint: usually for translation, not for open-ended chat.)
3. **Hard.** Implement speculative decoding: use a tiny 2-layer model as the draft and a 6-layer model as the verifier. Measure wall-clock speedup on 100 completions of length 64. Confirm outputs match greedy of the verifier.

## Key Terms | 术语速查表

| Term | What people say | What it actually means |
|------|-----------------|-----------------------|
| Causal mask | "The triangle" | Upper-triangular `-inf` matrix added to attention scores so position `i` only sees positions `≤ i`. |
| Next-token prediction | "The loss" | Cross-entropy of the model's distribution against the true next token at every position. |
| Autoregressive | "Generate one at a time" | Feed output back as input; parallelism only during training, not during generation. |
| Logits | "Pre-softmax scores" | Raw output of the LM head before softmax; sampling happens on these. |
| Temperature | "Creativity knob" | Divide logits by T; T→0 = greedy, T→∞ = uniform. |
| Top-p | "Nucleus sampling" | Truncate distribution to smallest set summing to ≥p; sample from what remains. |
| Min-p | "Better than top-p" | Keep tokens where `p ≥ min_p × max_p`; adapts cutoff to sharpness of distribution. |
| Speculative decoding | "Draft + verify" | Cheap model proposes N tokens; big model verifies in parallel. |
| Teacher forcing | "Training trick" | During training, feed the true previous token, not the model's prediction. Standard for every seq2seq LM. |

## Further Reading | 延伸阅读

- [Radford et al. (2018). Improving Language Understanding by Generative Pre-Training](https://cdn.openai.com/research-covers/language-unsupervised/language_understanding_paper.pdf) — GPT-1.
- [Radford et al. (2019). Language Models are Unsupervised Multitask Learners](https://cdn.openai.com/better-language-models/language_models_are_unsupervised_multitask_learners.pdf) — GPT-2.
- [Brown et al. (2020). Language Models are Few-Shot Learners](https://arxiv.org/abs/2005.14165) — GPT-3 and in-context learning.
- [Leviathan, Kalman, Matias (2023). Fast Inference from Transformers via Speculative Decoding](https://arxiv.org/abs/2211.17192) — spec decoding paper.
- [HuggingFace `modeling_llama.py`](https://github.com/huggingface/transformers/blob/main/src/transformers/models/llama/modeling_llama.py) — canonical causal-LM reference code.
