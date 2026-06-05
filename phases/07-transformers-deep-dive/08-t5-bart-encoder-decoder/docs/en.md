# T5, BART — Encoder-Decoder Models | T5、BART — 编码器-解码器模型

> Encoders understand. Decoders generate. Put them back together and you get a model built for input → output tasks: translate, summarize, rewrite, transcribe.

> **【中文解读】** T5 把所有 NLP 任务统一为 text-to-text 格式。BART 用去噪自编码训练。适用于翻译、摘要等序列转换任务。

**Type:** Study | **类型:** 学习
**Language:** Python | **语言:** Python
**Prerequisites:** Phase 7 · 05 (Full Transformer), Phase 7 · 06 (BERT), Phase 7 · 07 (GPT) | **前置知识:** Phase 7 · 05 (Full Transformer), Phase 7 · 06 (BERT), Phase 7 · 07 (GPT)
**Time:** ~45 minutes | **时间:** ~45 分钟

## The Problem | 问题引入

Decoder-only GPT and encoder-only BERT each strip down the 2017 architecture for a different goal. But many tasks are naturally input-output:

> 解码器专用 GPT 和编码器专用 BERT 各自为不同目标精简了 2017 年的架构。但许多任务天然是输入-输出形式的：

- Translation: English → French.
  中文翻译：翻译：英语 → 法语。
- Summarization: 5,000-token article → 200-token summary.
  中文翻译：摘要：5,000 token 文章 → 200 token 摘要。
- Speech recognition: audio tokens → text tokens.
  中文翻译：语音识别：音频 token → 文本 token。
- Structured extraction: prose → JSON.
  中文翻译：结构化提取：散文 → JSON。

For these, encoder-decoder makes the cleanest fit. The encoder produces a dense representation of the source. The decoder generates the output, cross-attending to that representation at every step. Training is shift-by-one on the output side. Same loss as GPT, just conditioned on the encoder output.

> 对于这些任务，编码器-解码器是最合适的选择。编码器生成源的密集表示。解码器生成输出，在每一步通过交叉注意力访问该表示。输出端的训练采用偏移一位的方式。损失与 GPT 相同，只是以编码器输出为条件。

Two papers defined the modern playbook:

> 两篇论文定义了现代范式：

1. **T5** (Raffel et al. 2019). "Text-to-Text Transfer Transformer." Every NLP task reframed as text-in, text-out. Single architecture, single vocabulary, single loss. Pretrained on masked span prediction (corrupt spans in the input, decode them in the output).
   中文翻译：**T5**（Raffel 等人，2019）。"文本到文本迁移 Transformer"。每个 NLP 任务都被重新定义为文本输入-文本输出。单一架构、单一词表、单一损失。用掩码片段预测进行预训练（破坏输入中的片段，在输出中解码它们）。
2. **BART** (Lewis et al. 2019). "Bidirectional and Auto-Regressive Transformer." Denoising autoencoder: corrupt input in multiple ways (shuffle, mask, delete, rotate), ask the decoder to reconstruct the original.
   中文翻译：**BART**（Lewis 等人，2019）。"双向自回归 Transformer"。去噪自编码器：用多种方式破坏输入（打乱、掩码、删除、旋转），要求解码器重建原始文本。

In 2026 the encoder-decoder format lives on where input structure matters:

> 在 2026 年，编码器-解码器格式在输入结构重要的场景中继续存在：

- Whisper (speech → text).
  中文翻译：Whisper（语音 → 文本）。
- Google's translation stack.
  中文翻译：Google 的翻译系统。
- Some code-completion / repair models that have distinct context-and-edit structures.
  中文翻译：一些具有明确上下文-编辑结构的代码补全/修复模型。
- Flan-T5 and variants for structured reasoning tasks.
  中文翻译：Flan-T5 及其变体，用于结构化推理任务。

Decoder-only won the spotlight, but encoder-decoder never went away.

> 解码器专用模型赢得了聚光灯，但编码器-解码器从未消失。

> **【中文解读】** 编码器-解码器架构在"输入→输出"结构化任务中仍有优势。T5 将所有 NLP 任务统一为 text-to-text 格式，BART 用去噪自编码训练。虽然在纯文本生成领域被 Decoder-only 取代，但在语音识别（Whisper）、翻译、摘要等任务中仍是最佳选择。

## The Concept | 核心概念

![Encoder-decoder with cross-attention](../assets/encoder-decoder.svg)

### The forward loop

```
source tokens ─▶ encoder ─▶ (N_src, d_model)  ──┐
                                                 │
target tokens ─▶ decoder block                   │
                 ├─▶ masked self-attention       │
                 ├─▶ cross-attention ◀───────────┘
                 └─▶ FFN
                ↓
              next-token logits
```

Crucially, the encoder runs once per input. The decoder runs autoregressively but cross-attends to the *same* encoder output at every step. Caching the encoder output is a free speedup for long inputs.

> 关键是，编码器对每个输入只运行一次。解码器自回归运行，但在每一步都交叉关注*相同的*编码器输出。缓存编码器输出对长输入是免费的加速。

> **【中文解读】** 交叉注意力是编码器-解码器架构的信息桥梁：Q 来自解码器，K/V 来自编码器输出。编码器只运行一次（高效），解码器每步都通过交叉注意力访问编码器的完整输出。

> **【拓展：Whisper 的编码器-解码器设计】** OpenAI 的 Whisper 语音识别模型使用编码器-解码器架构，因为音频（梅尔频谱图）和文本是完全不同的模态。编码器处理音频特征，解码器生成文本。这种设计让 Whisper 能处理多语言语音识别和翻译任务，是 2026 年语音领域的事实标准。

### T5 pretraining — span corruption

Pick random spans of the input (average length 3 tokens, 15% total). Replace each span with a unique sentinel: `<extra_id_0>`, `<extra_id_1>`, etc. The decoder outputs only the corrupted spans with their sentinel prefix:

> 随机选择输入中的片段（平均长度 3 个 token，总计 15%）。用唯一的哨兵标记替换每个片段：`<extra_id_0>`、`<extra_id_1>` 等。解码器只输出被破坏的片段及其哨兵前缀：

```
source: The quick <extra_id_0> fox jumps <extra_id_1> dog
target: <extra_id_0> brown <extra_id_1> over the lazy
```

Cheaper signal than predicting the whole sequence. Competitive with MLM (BERT) and prefix-LM (UniLM) in the T5 paper's ablation.

> 比预测整个序列的信号更廉价。在 T5 论文的消融实验中，与 MLM（BERT）和前缀 LM（UniLM）竞争力相当。

### BART pretraining — multi-noise denoising

BART tries five noising functions:

> BART 尝试五种噪声函数：

1. Token masking.
   中文翻译：Token 掩码。
2. Token deletion.
   中文翻译：Token 删除。
3. Text infilling (mask a span, decoder inserts the right length).
   中文翻译：文本填充（掩码一个片段，解码器插入正确长度）。
4. Sentence permutation.
   中文翻译：句子排列。
5. Document rotation.
   中文翻译：文档旋转。

Combining text infilling + sentence permutation produced the best downstream numbers. The decoder always reconstructs the original. BART's output is the full sequence, not just the corrupted spans — so pretraining compute is higher than T5.

> 组合文本填充 + 句子排列产生了最好的下游效果。解码器总是重建原始文本。BART 的输出是完整序列，而不仅仅是被破坏的片段——因此预训练计算量高于 T5。

> **【中文解读】** T5 和 BART 的预训练策略不同：T5 的 span corruption 只预测被破坏的片段（高效），BART 的去噪自编码重建整个序列（更彻底但更贵）。选择取决于任务——T5 更适合 extractive 任务，BART 更适合 abstractive 任务。

### Inference

Same autoregressive generation as GPT. Greedy / beam / top-p sampling apply. Beam search (width 4–5) is standard for translation and summarization because the output distribution is narrower than chat.

> 推理与 GPT 的自回归生成相同。贪心/束搜索/top-p 采样都适用。束搜索（宽度 4-5）是翻译和摘要的标准策略，因为输出分布比对话更窄。

> **【拓展：Beam Search 在翻译中的重要性】** 编码器-解码器模型在翻译和摘要任务中常用 beam search（宽度 4-5），因为输出分布较窄。Beam search 维护多个候选序列，每步保留得分最高的几个继续扩展。相比贪心搜索，beam search 能找到更优的全局序列；相比随机采样，它更稳定。在对话生成中通常不需要 beam search，因为输出分布更广。

### When to pick each variant in 2026

| Task | Encoder-decoder? | Why |
|------|------------------|-----|
| 任务 | 是否用编码器-解码器？ | 原因 |
| Translation | Yes, usually | Clear source sequence; fixed output distribution; beam search works |
| 翻译 | 通常是 | 明确的源序列；固定的输出分布；束搜索有效 |
| Speech-to-text | Yes (Whisper) | Input modality differs from output; encoder shapes audio features |
| 语音转文本 | 是（Whisper） | 输入模态与输出不同；编码器处理音频特征 |
| Chat / reasoning | No, decoder-only | No persistent "input" — the conversation is the sequence |
| 对话/推理 | 否，解码器专用 | 没有持久的"输入"——对话本身就是序列 |
| Code completion | Usually no | Decoder-only with long context wins; code models like Qwen 2.5 Coder are decoder-only |
| 代码补全 | 通常否 | 带长上下文的解码器专用胜出；Qwen 2.5 Coder 等代码模型是解码器专用 |
| Summarization | Either works | BART, PEGASUS beat earlier decoder-only baselines; modern decoder-only LLMs match them |
| 摘要 | 都可以 | BART、PEGASUS 超越早期解码器专用基线；现代解码器专用 LLM 能匹配它们 |
| Structured extraction | Either | T5 is clean because "text → text" absorbs any output format |
| 结构化提取 | 都可以 | T5 很干净，因为"文本 → 文本"可以吸收任何输出格式 |

The trend since ~2022: decoder-only takes over tasks that encoder-decoder used to own because (a) instruction-tuned decoder-only LLMs generalize to anything via prompting, (b) one architecture scales easier than two, (c) RLHF assumes a decoder. Encoder-decoder holds on where input modality differs (speech, images) or where beam search quality matters.

> 自 2022 年以来的趋势：解码器专用接管了编码器-解码器曾经拥有的任务，因为 (a) 指令微调的解码器专用 LLM 通过提示可以泛化到任何任务，(b) 单一架构比两个更容易扩展，(c) RLHF 假设使用解码器。编码器-解码器在输入模态不同（语音、图像）或束搜索质量重要时仍然有用。

> **【拓展：T5 的 text-to-text 统一范式】** T5 的核心理念是将所有 NLP 任务统一为"文本输入→文本输出"格式。翻译："translate English to French: Hello → Bonjour"；分类："sentiment: This movie is great → positive"。这种统一简化了架构和训练流程，也是后来 instruction tuning 和 prompt engineering 的思想源头。Flan-T5 更是通过指令微调大幅提升了零样本能力。

## Build It | 动手实现

See `code/main.py`. We implement T5-style span corruption for a toy corpus — the most useful single piece of this lesson because it shows up in every encoder-decoder pretraining recipe since.

> 参见 `code/main.py`。我们为玩具语料实现 T5 风格的片段破坏——这是本课最有用的部分，因为它出现在此后的每个编码器-解码器预训练方案中。

### Step 1: span corruption

```python
def corrupt_spans(tokens, mask_rate=0.15, mean_span=3.0, rng=None):
    """Pick spans summing to ~mask_rate of tokens. Return (corrupted_input, target)."""
    n = len(tokens)
    n_mask = max(1, int(n * mask_rate))
    n_spans = max(1, int(round(n_mask / mean_span)))
    ...
```

The target format is the T5 convention: `<sent0> span0 <sent1> span1 ...`. The corrupted input interleaves unchanged tokens with the sentinel tokens at span locations.

> 目标格式遵循 T5 约定：`<sent0> span0 <sent1> span1 ...`。被破坏的输入将未更改的 token 与片段位置的哨兵 token 交替排列。

### Step 2: verify round-trip

Given the corrupted input and target, reconstruct the original sentence. If your corruption is reversible, the forward pass is well-defined. This is a sanity check — real training never does this, but the test is cheap and catches off-by-one bugs in your span bookkeeping.

> 给定被破坏的输入和目标，重建原始句子。如果破坏是可逆的，前向传播就是良定义的。这是一个合理性检查——真实训练从不这样做，但测试成本低且能发现片段簿记中的差一错误。

### Step 3: BART noising

Five functions: `token_mask`, `token_delete`, `text_infill`, `sentence_permute`, `document_rotate`. Compose two of them and show the result.

> 五个函数：`token_mask`、`token_delete`、`text_infill`、`sentence_permute`、`document_rotate`。组合其中两个并展示结果。

## Use It | 用框架实现

HuggingFace reference:

> HuggingFace 参考：

```python
from transformers import T5ForConditionalGeneration, T5Tokenizer
tok = T5Tokenizer.from_pretrained("google/flan-t5-base")
model = T5ForConditionalGeneration.from_pretrained("google/flan-t5-base")

inputs = tok("translate English to French: Attention is all you need.", return_tensors="pt")
out = model.generate(**inputs, max_new_tokens=32)
print(tok.decode(out[0], skip_special_tokens=True))
```

The T5 trick: the task name goes into the input text. Same model handles dozens of tasks because each task is text-in, text-out. In 2026 this pattern has been generalized by instruction-tuned decoder-only models, but T5 codified it first.

> T5 的技巧：任务名称写在输入文本中。同一个模型可以处理数十种任务，因为每个任务都是文本输入-文本输出。在 2026 年，这种模式已被指令微调的解码器专用模型泛化，但 T5 是最早将其规范化的。

## Ship It | 产出物

See `outputs/skill-seq2seq-picker.md`. The skill picks between encoder-decoder and decoder-only for a new task given input-output structure, latency, and quality targets.

> 参见 `outputs/skill-seq2seq-picker.md`。该 skill 根据输入-输出结构、延迟和质量目标，为新任务选择编码器-解码器或解码器专用架构。

## Exercises | 练习题

1. **Easy.** Run `code/main.py`, apply span corruption to a 30-token sentence, verify that concatenating the non-sentinel source tokens with the decoded target spans reproduces the original.
   中文翻译：运行 `code/main.py`，对一个 30 token 的句子应用片段破坏，验证将非哨兵源 token 与解码的目标片段拼接可以还原原始文本。
2. **Medium.** Implement BART's `text_infill` noise: replace random spans with a single `<mask>` token, and the decoder must infer the correct span length plus contents. Show one example.
   中文翻译：实现 BART 的 `text_infill` 噪声：用单个 `<mask>` token 替换随机片段，解码器必须推断正确的片段长度和内容。展示一个示例。
3. **Hard.** Fine-tune `flan-t5-small` on a tiny English → pig-Latin corpus (200 pairs). Measure BLEU on a held-out 50-pair set. Compare against fine-tuning `Llama-3.2-1B` on the same data with the same compute.
   中文翻译：在小型英语 → Pig Latin 语料库（200 对）上微调 `flan-t5-small`。在留出的 50 对测试集上测量 BLEU 分数。与在相同数据、相同计算量上微调 `Llama-3.2-1B` 对比。

## Key Terms | 术语速查表

| Term | What people say | What it actually means |
|------|-----------------|-----------------------|
| 术语 | 通俗说法 | 实际含义 |
| Encoder-decoder | "Seq2seq transformer" | Two stacks: bidirectional encoder for input, causal decoder with cross-attention for output. |
| 编码器-解码器 | "Seq2seq Transformer" | 两个堆栈：双向编码器处理输入，带交叉注意力的因果解码器生成输出。 |
| Cross-attention | "Where source talks to target" | Decoder's Q × encoder's K/V. The only place encoder information enters the decoder. |
| 交叉注意力 | "源与目标对话的地方" | 解码器的 Q × 编码器的 K/V。编码器信息进入解码器的唯一通道。 |
| Span corruption | "T5's pretraining trick" | Replace random spans with sentinel tokens; decoder outputs the spans. |
| 片段破坏 | "T5 的预训练技巧" | 用哨兵 token 替换随机片段；解码器输出这些片段。 |
| Denoising objective | "BART's game" | Apply a noise function to the input, train the decoder to reconstruct the clean sequence. |
| 去噪目标 | "BART 的游戏" | 对输入应用噪声函数，训练解码器重建干净序列。 |
| Sentinel token | "The `<extra_id_N>` placeholder" | Special tokens that tag corrupted spans in the source and re-tag them in the target. |
| 哨兵 token | "`<extra_id_N>` 占位符" | 在源端标记被破坏片段、在目标端重新标记的特殊 token。 |
| Flan | "Instruction-tuned T5" | T5 fine-tuned on >1,800 tasks; made encoder-decoder competitive at instruction-following. |
| Flan | "指令微调的 T5" | 在 1,800+ 任务上微调的 T5；使编码器-解码器在指令遵循方面具有竞争力。 |
| Beam search | "Decoding strategy" | Keep top-k partial sequences at each step; standard for translation/summarization. |
| 束搜索 | "解码策略" | 每步保留得分最高的 k 个部分序列；翻译/摘要的标准策略。 |
| Teacher forcing | "Training-time input" | During training, feed the true previous output token to the decoder, not the sampled one. |
| Teacher forcing | "训练时输入" | 训练时向解码器输入真实的上一个输出 token，而非采样的 token。 |

## Further Reading | 延伸阅读

- [Raffel et al. (2019). Exploring the Limits of Transfer Learning with a Unified Text-to-Text Transformer](https://arxiv.org/abs/1910.10683) — T5.
  中文翻译：T5 论文。
- [Lewis et al. (2019). BART: Denoising Sequence-to-Sequence Pre-training for Natural Language Generation, Translation, and Comprehension](https://arxiv.org/abs/1910.13461) — BART.
  中文翻译：BART 论文。
- [Chung et al. (2022). Scaling Instruction-Finetuned Language Models](https://arxiv.org/abs/2210.11416) — Flan-T5.
  中文翻译：Flan-T5 论文。
- [Radford et al. (2022). Robust Speech Recognition via Large-Scale Weak Supervision](https://arxiv.org/abs/2212.04356) — Whisper, the canonical 2026 encoder-decoder.
  中文翻译：Whisper 论文，2026 年典型的编码器-解码器模型。
- [HuggingFace `modeling_t5.py`](https://github.com/huggingface/transformers/blob/main/src/transformers/models/t5/modeling_t5.py) — reference implementation.
  中文翻译：HuggingFace T5 参考实现。
