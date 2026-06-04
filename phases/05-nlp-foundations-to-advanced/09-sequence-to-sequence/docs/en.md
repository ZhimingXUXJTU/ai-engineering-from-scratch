# Sequence-to-Sequence Models | 序列到序列模型 (Seq2Seq)

> Two RNNs pretending to be a translator. The bottleneck they hit is the reason attention exists.

> **【中文解读】** 编码器-解码器架构。注意力机制就是为解决它的瓶颈而发明的。

**Type:** Build
**Languages:** Python
**Prerequisites:** Phase 5 · 08 (CNNs + RNNs for Text), Phase 3 · 11 (PyTorch Intro)
**Time:** ~75 minutes

## The Problem | 问题引入

Classification maps a variable-length sequence to a single label. Translation maps a variable-length sequence to another variable-length sequence. The input and output live in different vocabularies, possibly different languages, with no guarantee of length parity.

> **【中文解读】** 本节提出的问题是：如何在实际工程中正确理解和应用这一技术。理解问题背景有助于把握技术选型的关键决策点。在实际 AI 系统中，错误的技术选型往往比实现细节的 bug 代价更高。


The seq2seq architecture (Sutskever, Vinyals, Le, 2014) cracked this with a deliberately simple recipe. Two RNNs. One reads the source sentence and produces a fixed-size context vector. The other reads that vector and generates the target sentence token by token. Same code you wrote for lesson 08, glued together differently.

This is worth studying for two reasons. First, the context-vector bottleneck is the most pedagogically useful failure in NLP. It motivates everything attention and transformers are good at. Second, the training recipe (teacher forcing, scheduled sampling, beam search at inference) still applies to every modern generation system including LLMs.

## The Concept | 核心概念

> **【中文解读】** 本节介绍核心概念和理论基础。掌握这些概念是后续动手实现的前提，同时也是面试和工程实践中高频考察的知识点。


**Encoder.** An RNN that reads the source sentence. Its final hidden state is the **context vector** — a fixed-size summary of the entire input. Lose nothing but the source, supposedly.

**Decoder.** Another RNN initialized from the context vector. At each step it takes the previously generated token as input and produces a distribution over the target vocabulary. Sample or argmax to pick the next token. Feed it back in. Repeat until an `<EOS>` token is produced or max length is hit.

**Training:** Cross-entropy loss at each decoder step, summed over the sequence. Standard backprop through time through both networks.

**Teacher forcing.** During training, the decoder's input at step `t` is the *ground-truth* token at position `t-1`, not the decoder's own previous prediction. This stabilizes training; without it, early mistakes cascade and the model never learns. At inference, you have to use the model's own predictions, so there is always a train/inference distribution gap. That gap is called **exposure bias**.

**The bottleneck.** Everything the encoder learned about the source must be squeezed into that one context vector. Long sentences lose detail. Rare words get blurred. Reordering (chat noir vs. black cat) has to be memorized, not computed.

Attention (lesson 10) fixes this by letting the decoder look at *every* encoder hidden state, not just the last one. That is the whole pitch.

> **【中文解读】** 本节通过代码从零实现核心算法。这种 "from scratch" 的方式能帮助理解框架背后的原理，遇到问题时不会被黑盒困住。

> **【拓展：大语言模型的工程实践】** 从 GPT 到 ChatGPT，NLP 领域经历了从 "每个任务训练一个模型" 到 "一个模型解决所有任务" 的范式转变。在实际工程中，LLM 的部署需要考虑 Token 限制、延迟、成本、安全审查等问题。LangChain、LlamaIndex 等框架简化了 LLM 应用的开发。

> **【拓展：RAG 与企业知识库】** 检索增强生成（RAG）是当前企业 AI 应用最流行的架构：将用户查询先检索相关文档片段，再将检索结果作为上下文喂给 LLM 生成答案。这种方式解决了 LLM 知识过时和幻觉问题。向量数据库（如 Milvus、Pinecone、Weaviate）是 RAG 系统的核心组件。

> **【拓展：NLP 的多语言挑战】** 全球有 7000+ 种语言，但 NLP 研究主要集中在英语等少数语言。跨语言迁移学习、多语言预训练模型（如 mBERT、XLM-R）是解决低资源语言 NLP 的主要方法。字节级模型（如 ByT5）甚至可以在无分词器的情况下处理任何语言。





## Build It | 动手实现

### Step 1: an encoder

```python
import torch
import torch.nn as nn


class Encoder(nn.Module):
    def __init__(self, src_vocab_size, embed_dim, hidden_dim):
        super().__init__()
        self.embed = nn.Embedding(src_vocab_size, embed_dim, padding_idx=0)
        self.gru = nn.GRU(embed_dim, hidden_dim, batch_first=True)

    def forward(self, src):
        e = self.embed(src)
        outputs, hidden = self.gru(e)
        return outputs, hidden
```

`outputs` has shape `[batch, seq_len, hidden_dim]` — one hidden state per input position. `hidden` has shape `[1, batch, hidden_dim]` — the final step. Lesson 08 said "pool over outputs for classification." Here we keep the last hidden state as the context vector, and ignore the per-step outputs.

### Step 2: a decoder

```python
class Decoder(nn.Module):
    def __init__(self, tgt_vocab_size, embed_dim, hidden_dim):
        super().__init__()
        self.embed = nn.Embedding(tgt_vocab_size, embed_dim, padding_idx=0)
        self.gru = nn.GRU(embed_dim, hidden_dim, batch_first=True)
        self.fc = nn.Linear(hidden_dim, tgt_vocab_size)

    def forward(self, token, hidden):
        e = self.embed(token)
        out, hidden = self.gru(e, hidden)
        logits = self.fc(out)
        return logits, hidden
```

Decoder is called one step at a time. Input: a batch of single tokens and the current hidden state. Output: vocabulary logits for the next token and the updated hidden state.

### Step 3: training loop with teacher forcing

```python
def train_batch(encoder, decoder, src, tgt, bos_id, optimizer, teacher_forcing_ratio=0.9):
    optimizer.zero_grad()
    _, hidden = encoder(src)
    batch_size, tgt_len = tgt.shape
    input_token = torch.full((batch_size, 1), bos_id, dtype=torch.long)
    loss = 0.0
    loss_fn = nn.CrossEntropyLoss(ignore_index=0)

    for t in range(tgt_len):
        logits, hidden = decoder(input_token, hidden)
        step_loss = loss_fn(logits.squeeze(1), tgt[:, t])
        loss += step_loss
        use_teacher = torch.rand(1).item() < teacher_forcing_ratio
        if use_teacher:
            input_token = tgt[:, t].unsqueeze(1)
        else:
            input_token = logits.argmax(dim=-1)

    loss.backward()
    optimizer.step()
    return loss.item() / tgt_len
```

Two knobs worth naming. `ignore_index=0` skips loss on padding tokens. `teacher_forcing_ratio` is the probability of using the true token vs. the model's prediction at each step. Start at 1.0 (full teacher forcing) and anneal down to ~0.5 over training to close the exposure-bias gap.

### Step 4: inference loop (greedy)

```python
@torch.no_grad()
def greedy_decode(encoder, decoder, src, bos_id, eos_id, max_len=50):
    _, hidden = encoder(src)
    batch_size = src.shape[0]
    input_token = torch.full((batch_size, 1), bos_id, dtype=torch.long)
    output_ids = []
    for _ in range(max_len):
        logits, hidden = decoder(input_token, hidden)
        next_token = logits.argmax(dim=-1)
        output_ids.append(next_token)
        input_token = next_token
        if (next_token == eos_id).all():
            break
    return torch.cat(output_ids, dim=1)
```

Greedy decoding picks the highest-probability token at every step. It can wander off: once you commit to a token, you cannot unsay it. **Beam search** keeps the top-`k` partial sequences alive and picks the highest-scoring complete one at the end. Beam width 3-5 is standard.

### Step 5: the bottleneck, demonstrated

Train the model on a toy copy task: source `[a, b, c, d, e]`, target `[a, b, c, d, e]`. Increase sequence length. Observe accuracy.

```
seq_len=5   copy accuracy: 98%
seq_len=10  copy accuracy: 91%
seq_len=20  copy accuracy: 62%
seq_len=40  copy accuracy: 23%
```

> **【中文解读】** 本节展示如何用成熟框架（如 PyTorch、HuggingFace 等）快速应用该技术。在实际项目中，优先使用经过验证的框架实现，可以减少 bug 并提高开发效率。


A single GRU hidden state cannot losslessly memorize a 40-token input. The information is there at every encoder step, but the decoder only sees the last state. Attention fixes this directly.




> **【拓展：Prompt Engineering 与 LLM 应用】** Prompt Engineering 已成为 NLP 工程师的核心技能。从 Zero-shot 到 Few-shot，从 Chain-of-Thought 到 ReAct，不同的提示策略适用于不同场景。在实际项目中，系统提示（System Prompt）的设计直接影响 LLM 应用的稳定性和输出质量。

## Use It | 用框架实现

PyTorch has `nn.Transformer` and `nn.LSTM`-based seq2seq templates. Hugging Face's `transformers` library ships full encoder-decoder models (BART, T5, mBART, NLLB) trained on billions of tokens.

```python
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

tok = AutoTokenizer.from_pretrained("facebook/bart-base")
model = AutoModelForSeq2SeqLM.from_pretrained("facebook/bart-base")

src = tok("Translate this to French: Hello, how are you?", return_tensors="pt")
out = model.generate(**src, max_new_tokens=50, num_beams=4)
print(tok.decode(out[0], skip_special_tokens=True))
```

Modern encoder-decoders dropped RNNs for transformers. The high-level shape (encoder, decoder, generate-token-by-token) is identical to the 2014 seq2seq paper. The mechanism inside each block is different.

### When to still reach for RNN-based seq2seq

Almost never, for new projects. Specific exceptions:

- Streaming translation where you consume input one token at a time with bounded memory.
- On-device text generation where transformer memory cost is prohibitive.
- Pedagogy. Understanding the encoder-decoder bottleneck is the fastest path to understanding why transformers won.

### Exposure bias and its mitigations

- **Scheduled sampling.** Anneal teacher forcing ratio during training so the model learns to recover from its own mistakes.
- **Minimum risk training.** Train on sentence-level BLEU score instead of token-level cross-entropy. Closer to what you actually want.
- **Reinforcement learning fine-tuning.** Reward the sequence generator with a metric. Used in modern LLM RLHF.

> **【中文解读】** 本节关注如何将模型部署为可用的产品。从原型到生产级系统需要考虑性能优化、错误处理、监控等多个维度。


All three still apply to transformer-based generation.



## Ship It | 产出物

Save as `outputs/prompt-seq2seq-design.md`:

```markdown
---
name: seq2seq-design
description: Design a sequence-to-sequence pipeline for a given task.
phase: 5
lesson: 09
---

Given a task (translation, summarization, paraphrase, question rewrite), output:

1. Architecture. Pretrained transformer encoder-decoder (BART, T5, mBART, NLLB) is the default. RNN-based seq2seq only for specific constraints.
2. Starting checkpoint. Name it (`facebook/bart-base`, `google/flan-t5-base`, `facebook/nllb-200-distilled-600M`). Match the checkpoint to task and language coverage.
3. Decoding strategy. Greedy for deterministic output, beam search (width 4-5) for quality, sampling with temperature for diversity. One sentence justification.
4. One failure mode to verify before shipping. Exposure bias manifests as generation drift on longer outputs; sample 20 outputs at the 90th-percentile length and eyeball.

> **【中文解读】** 练习题按照 Easy/Medium/Hard 三个难度递进。建议至少完成 Medium 级别的题目，Hard 级别适合深入研究或面试准备。


Refuse to recommend training a seq2seq from scratch for under a million parallel examples. Flag any pipeline that uses greedy decoding for user-facing content as fragile (greedy repeats and loops).
```

## Exercises | 练习题

1. **Easy.** Implement the toy copy task. Train a GRU seq2seq on input-output pairs where the target equals the source. Measure accuracy at lengths 5, 10, 20. Reproduce the bottleneck.
2. **Medium.** Add beam search decoding with beam width 3. Measure BLEU on a small parallel corpus against greedy. Document where beam search wins (usually last tokens) and where it makes no difference.
3. **Hard.** Fine-tune `facebook/bart-base` on a 10k-pair paraphrase dataset. Compare the fine-tuned model's beam-4 output to the base model's on held-out inputs. Report BLEU and pick 10 qualitative examples.

> **【中文解读】** 术语表中的 "What people say" vs "What it actually means" 区分了日常口语和精确技术含义。在团队协作中，统一术语定义可以避免大量沟通误解。


## Key Terms | 术语速查表

| Term | What people say | What it actually means |
|------|-----------------|-----------------------|
| Encoder | Input RNN | Reads source. Produces per-step hidden states and a final context vector. |
| Decoder | Output RNN | Initialized from context vector. Generates target tokens one at a time. |
| Context vector | The summary | Final encoder hidden state. Fixed size. The bottleneck attention solves. |
| Teacher forcing | Use true tokens | Feed the ground-truth previous token at training time. Stabilizes learning. |
| Exposure bias | Train/test gap | Model trained on true tokens never practiced recovering from its own mistakes. |
| Beam search | Better decoding | Keep top-k partial sequences alive at each step instead of committing greedily. |

> **【中文解读】** 延伸阅读提供了深入学习的高质量资源。这些论文和教程是该领域的经典参考文献，适合需要深入理解的读者。


## Further Reading | 延伸阅读

- [Sutskever, Vinyals, Le (2014). Sequence to Sequence Learning with Neural Networks](https://arxiv.org/abs/1409.3215) — the original seq2seq paper. Four pages.
- [Cho et al. (2014). Learning Phrase Representations using RNN Encoder-Decoder for Statistical Machine Translation](https://arxiv.org/abs/1406.1078) — introduced the GRU and the encoder-decoder framing.
- [Bahdanau, Cho, Bengio (2014). Neural Machine Translation by Jointly Learning to Align and Translate](https://arxiv.org/abs/1409.0473) — the attention paper. Read immediately after this lesson.
- [PyTorch NLP from Scratch tutorial](https://pytorch.org/tutorials/intermediate/seq2seq_translation_tutorial.html) — buildable seq2seq + attention code.
