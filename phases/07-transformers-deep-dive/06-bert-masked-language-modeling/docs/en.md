# BERT — Masked Language Modeling | BERT — 掩码语言模型

> GPT predicts the next word. BERT predicts a missing word. One sentence of difference — and half a decade of everything embedding-shaped.

> **【中文解读】** BERT 是 Encoder-only Transformer，用掩码预测训练。理解 BERT = 理解双向上下文建模。用于文本分类、NER、问答等。

**Type:** Hands-on | **类型:** 动手
**Language:** Python | **语言:** Python
**Prerequisites:** Phase 7 · 05 (Full Transformer), Phase 5 · 02 (Text Representation) | **前置知识:** Phase 7 · 05 (Full Transformer), Phase 5 · 02 (Text Representation)
**Time:** ~45 minutes | **时间:** ~45 分钟

## The Problem | 问题引入

In 2018 every NLP task — sentiment, NER, QA, entailment — trained its own model from scratch on its own labeled data. There was no pre-trained "understand English" checkpoint you could fine-tune. ELMo (2018) showed you could pre-train contextual embeddings with a bidirectional LSTM; it helped but did not generalize.

> 2018 年，每个 NLP 任务——情感分析、命名实体识别、问答、文本蕴含——都需要在自己的标注数据上从零训练模型。当时没有预训练的"理解英语"检查点可供微调。ELMo（2018）证明可以用双向 LSTM 预训练上下文嵌入，但泛化能力有限。

BERT (Devlin et al. 2018) asked: what if we took a transformer encoder, trained it on every sentence on the internet, and forced it to predict missing words from context on both sides? Then you fine-tune one head on your downstream task. Parameter efficiency was a revelation.

> BERT（Devlin 等人，2018）提出了一个关键问题：如果用 Transformer 编码器，在互联网上所有句子上训练，强迫它根据两侧上下文预测被遮蔽的词，会怎样？然后在下游任务上微调一个输出头。参数效率的提升令人震惊。

The result: within 18 months BERT and its variants (RoBERTa, ALBERT, ELECTRA) dominated every NLP leaderboard that existed. By 2020 every search engine, content moderation pipeline, and semantic-search system on earth had a BERT inside.

> 结果是：在 18 个月内，BERT 及其变体（RoBERTa、ALBERT、ELECTRA）统治了所有 NLP 排行榜。到 2020 年，世界上每个搜索引擎、内容审核管道和语义搜索系统内部都有一个 BERT。

In 2026 encoder-only models are still the right tool for classification, retrieval, and structured extraction — they run 5–10× faster per token than decoders and their embeddings are the backbone of every modern retrieval stack. ModernBERT (Dec 2024) pushed the architecture to 8K context with Flash Attention + RoPE + GeGLU.

> 到 2026 年，编码器专用模型仍然是分类、检索和结构化提取的正确选择——它们每 token 的运行速度比解码器快 5-10 倍，其嵌入是每个现代检索系统的骨干。ModernBERT（2024 年 12 月）用 Flash Attention + RoPE + GeGLU 将架构推到了 8K 上下文长度。

> **【中文解读】** BERT 的革命性在于"预训练+微调"范式：在大规模无标注语料上用掩码语言模型（MLM）预训练，然后在特定任务上微调少量参数。编码器的双向注意力让它能同时利用左右上下文预测被掩码的词，这是自回归模型（如 GPT）做不到的。

## The Concept | 核心概念

![Masked language modeling: pick tokens, mask them, predict originals](../assets/bert-mlm.svg)

### The training signal

Take a sentence: `the quick brown fox jumps over the lazy dog`.

> 取一个句子：`the quick brown fox jumps over the lazy dog`。

Mask 15% of tokens randomly:

> 随机掩码 15% 的 token：

```
input:  the [MASK] brown fox jumps [MASK] the lazy dog
target: the quick brown fox jumps over the lazy dog
```

Train the model to predict the original tokens at masked positions. Because the encoder is bidirectional, predicting `[MASK]` at position 1 can use `brown fox jumps` at positions 2+. That is the thing GPT cannot do.

> 训练模型在被掩码位置预测原始 token。因为编码器是双向的，预测位置 1 的 `[MASK]` 可以利用位置 2 及之后的 `brown fox jumps`。这正是 GPT 做不到的事情。

### The BERT mask rules

Of the 15% of tokens selected for prediction:

> 在被选中用于预测的 15% token 中：

- 80% are replaced with `[MASK]`.
  中文翻译：80% 被替换为 `[MASK]`。
- 10% are replaced with a random token.
  中文翻译：10% 被替换为随机 token。
- 10% are left unchanged.
  中文翻译：10% 保持不变。

Why not always `[MASK]`? Because `[MASK]` never appears at inference time. Training the model to expect `[MASK]` at 100% of masked positions would create a distribution shift between pretraining and fine-tuning. The 10% random + 10% unchanged keeps the model honest.

> 为什么不总是用 `[MASK]`？因为 `[MASK]` 在推理时永远不会出现。如果训练模型在 100% 的掩码位置都期望看到 `[MASK]`，会在预训练和微调之间造成分布偏移。10% 随机替换 + 10% 保持不变让模型保持"诚实"。

> **【中文解读】** BERT 掩码的三条规则（80% [MASK]、10% 随机替换、10% 保持不变）是为了缩小预训练和微调之间的分布差异。推理时不会出现 [MASK] token，所以需要让模型在训练时也见到正常和随机替换的 token。

> **【拓展：BERT 在 RAG 系统中的角色】** 现代 RAG（检索增强生成）系统中，BERT 变体仍然是检索阶段的核心。sentence-transformers 模型（如 all-MiniLM-L6-v2）本质上就是用对比学习微调的 BERT。交叉编码器（cross-encoder）重排序器也是 BERT 架构——它让查询和文档在同一注意力层中交互，质量远超双编码器。

### Next Sentence Prediction (NSP) — and why it was dropped

Original BERT also trained on NSP: given two sentences A and B, predict if B follows A. RoBERTa (2019) ablated it and showed NSP hurt, not helped. Modern encoders skip it.

> 原始 BERT 还在 NSP 上训练：给定两个句子 A 和 B，预测 B 是否紧跟 A。RoBERTa（2019）通过消融实验证明 NSP 反而有害。现代编码器已弃用它。

### What changed in 2026: ModernBERT

The 2024 ModernBERT paper rebuilt the block with 2026 primitives:

> 2024 年的 ModernBERT 论文用现代组件重建了编码器块：

| Component | Original BERT (2018) | ModernBERT (2024) |
|-----------|----------------------|-------------------|
| 组件 | 原始 BERT (2018) | ModernBERT (2024) |
| Positional | Learned absolute | RoPE |
| 位置编码 | 学习式绝对位置 | RoPE |
| Activation | GELU | GeGLU |
| 激活函数 | GELU | GeGLU |
| Normalization | LayerNorm | Pre-norm RMSNorm |
| 归一化 | LayerNorm | 前归一化 RMSNorm |
| Attention | Full dense | Alternating local (128) + global |
| 注意力 | 全密集 | 交替局部 (128) + 全局 |
| Context length | 512 | 8192 |
| 上下文长度 | 512 | 8192 |
| Tokenizer | WordPiece | BPE |
| 分词器 | WordPiece | BPE |

And unlike the 2018 stack, it is Flash-Attention-native. Inference is 2–3× faster at sequence length 8K than DeBERTa-v3 with better GLUE scores.

> 与 2018 年的技术栈不同，ModernBERT 原生支持 Flash Attention。在序列长度 8K 时推理速度比 DeBERTa-v3 快 2-3 倍，同时 GLUE 分数更高。

### Use cases that still pick an encoder in 2026

| Task | Why encoder beats decoder |
|------|---------------------------|
| 任务 | 为什么编码器优于解码器 |
| Retrieval / semantic search embeddings | Bidirectional context = better embedding quality per token |
| 检索/语义搜索嵌入 | 双向上下文 = 每个 token 更好的嵌入质量 |
| Classification (sentiment, intent, toxicity) | One forward pass; no generation overhead |
| 分类（情感、意图、毒性） | 一次前向传播；无生成开销 |
| NER / token labeling | Per-position output, natively bidirectional |
| NER/token 标注 | 逐位置输出，天然双向 |
| Zero-shot entailment (NLI) | Classifier head on top of encoder |
| 零样本蕴含 (NLI) | 编码器之上的分类器头 |
| Reranker for RAG | Cross-encoder scoring, 10x faster than LLM rerankers |
| RAG 重排序器 | 交叉编码器评分，比 LLM 重排序器快 10 倍 |

## Build It | 动手实现

### Step 1: masking logic

See `code/main.py`. The function `create_mlm_batch` takes a list of token IDs, a vocab size, and a mask probability. Returns input IDs (with masks applied) and labels (only at masked positions, -100 elsewhere — PyTorch's ignore index convention).

> 参见 `code/main.py`。函数 `create_mlm_batch` 接受 token ID 列表、词表大小和掩码概率，返回输入 ID（已应用掩码）和标签（仅在掩码位置有值，其余为 -100——PyTorch 的忽略索引约定）。

```python
def create_mlm_batch(tokens, vocab_size, mask_prob=0.15, rng=None):
    input_ids = list(tokens)
    labels = [-100] * len(tokens)
    for i, t in enumerate(tokens):
        if rng.random() < mask_prob:
            labels[i] = t
            r = rng.random()
            if r < 0.8:
                input_ids[i] = MASK_ID
            elif r < 0.9:
                input_ids[i] = rng.randrange(vocab_size)
            # else: keep original
    return input_ids, labels
```

### Step 2: run MLM prediction on a tiny corpus

Train a 2-layer encoder + MLM head on a vocabulary of 20 words, 200 sentences. No gradient — we do forward-pass sanity checks. Full training needs PyTorch.

> 在 20 个词的词表和 200 个句子上训练一个 2 层编码器 + MLM 头。不涉及梯度——只做前向传播的合理性检查。完整训练需要 PyTorch。

### Step 3: compare mask types

Show how the three-way rule keeps the model usable without `[MASK]`. Predict on an unmasked sentence and on a masked sentence. Both should produce reasonable token distributions because the model saw both patterns in training.

> 展示三路规则如何让模型在没有 `[MASK]` 的情况下仍然可用。对未掩码句子和掩码句子分别预测。两者都应该产生合理的 token 分布，因为模型在训练中见过这两种模式。

### Step 4: fine-tune head

Replace the MLM head with a classification head on a toy sentiment dataset. Only the head trains; the encoder is frozen. This is the pattern every BERT application follows.

> 用分类头替换 MLM 头，在一个玩具情感数据集上训练。只有头部训练，编码器冻结。这是每个 BERT 应用的标准模式。

> **【拓展：BERT 微调的实践技巧】** BERT 微调的最佳实践包括：(1) 使用较小的学习率（2e-5 到 5e-5）避免破坏预训练权重；(2) 对分类任务使用 [CLS] token 的输出作为句子表示；(3) 对于 NER 等逐 token 任务，使用每个位置的输出；(4) 逐步解冻（gradual unfreezing）可以在小数据集上提升泛化能力。

## Use It | 用框架实现

```python
from transformers import AutoModel, AutoTokenizer

tok = AutoTokenizer.from_pretrained("answerdotai/ModernBERT-base")
model = AutoModel.from_pretrained("answerdotai/ModernBERT-base")

text = "Attention is all you need."
inputs = tok(text, return_tensors="pt")
out = model(**inputs).last_hidden_state   # (1, N, 768)
```

**Embedding models are fine-tuned BERT.** `sentence-transformers` models like `all-MiniLM-L6-v2` are BERTs trained with contrastive loss. The encoder is the same. The loss changed.

> **嵌入模型是微调后的 BERT。** `sentence-transformers` 模型如 `all-MiniLM-L6-v2` 本质上是用对比损失训练的 BERT。编码器架构相同，只是损失函数变了。

**Cross-encoder rerankers are also fine-tuned BERT.** Pair-classification on `[CLS] query [SEP] doc [SEP]`. The bidirectional attention between query and doc is exactly what gives cross-encoders their quality edge over biencoders.

> **交叉编码器重排序器也是微调后的 BERT。** 在 `[CLS] query [SEP] doc [SEP]` 上做配对分类。查询和文档之间的双向注意力正是交叉编码器质量优于双编码器的原因。

**When not to pick BERT in 2026.** Anything generative. The encoder has no sensible way to autoregressively produce tokens. Also: anything under 1B params where a small decoder can match quality with more flexibility (Phi-3-Mini, Qwen2-1.5B).

> **2026 年何时不选 BERT。** 任何生成式任务。编码器没有合理的方式进行自回归 token 生成。此外，在 1B 参数以下的场景，小型解码器（如 Phi-3-Mini、Qwen2-1.5B）可以用更少的参数获得相当的灵活性。

> **【拓展：ModernBERT 的现代化改进】** ModernBERT（2024）将 2018 年的 BERT 架构全面升级：RoPE 替代学习式位置编码、GeGLU 替代 GELU、前归一化 RMSNorm 替代后归一化 LayerNorm、交替使用局部和全局注意力以支持 8K 上下文。推理速度比 DeBERTa-v3 快 2-3 倍，同时 GLUE 分数更高。

## Ship It | 产出物

See `outputs/skill-bert-finetuner.md`. The skill scopes a BERT fine-tune (backbone choice, head spec, data, eval, stopping) for a new classification or extraction task.

> 参见 `outputs/skill-bert-finetuner.md`。该 skill 为新的分类或提取任务规划 BERT 微调方案（骨干网络选择、头部规格、数据、评估、停止条件）。

## Exercises | 练习题

1. **Easy.** Run `code/main.py` and print the mask distribution across 10,000 tokens. Confirm ~15% are selected, and of those ~80% become `[MASK]`.
   中文翻译：运行 `code/main.py`，打印 10,000 个 token 的掩码分布。确认约 15% 被选中，其中约 80% 变为 `[MASK]`。
2. **Medium.** Implement whole-word masking: if a word is tokenized into subwords, mask all subwords together or none. Measure whether this improves MLM accuracy on a 500-sentence corpus.
   中文翻译：实现全词掩码：如果一个词被分词为多个子词，要么全部掩码要么全部不掩码。测量这是否在 500 个句子的语料上提升了 MLM 准确率。
3. **Hard.** Train a tiny (2-layer, d=64) BERT on 10,000 sentences from a public dataset. Fine-tune the `[CLS]` token for SST-2 sentiment. Compare against a decoder-only baseline at matched params — which wins?
   中文翻译：在公开数据集的 10,000 个句子上训练一个小型（2 层，d=64）BERT。微调 `[CLS]` token 用于 SST-2 情感分类。与相同参数量的解码器基线对比——哪个更好？

## Key Terms | 术语速查表

| Term | What people say | What it actually means |
|------|-----------------|-----------------------|
| 术语 | 通俗说法 | 实际含义 |
| MLM | "Masked language modeling" | Training signal: randomly replace 15% of tokens with `[MASK]`, predict the originals. |
| MLM | "掩码语言建模" | 训练信号：随机将 15% 的 token 替换为 `[MASK]`，预测原始 token。 |
| Bidirectional | "Looks both ways" | Encoder attention has no causal mask — every position sees every other position. |
| 双向 | "看两边" | 编码器注意力没有因果掩码——每个位置都能看到其他所有位置。 |
| `[CLS]` | "The pooler token" | A special token prepended to every sequence; its final embedding is used as the sentence-level representation. |
| `[CLS]` | "池化 token" | 一个特殊 token，添加到每个序列开头；其最终嵌入用作句子级表示。 |
| `[SEP]` | "Segment separator" | Separates paired sequences (e.g. query/doc, sentence A/B). |
| `[SEP]` | "片段分隔符" | 分隔成对序列（如查询/文档、句子 A/B）。 |
| NSP | "Next sentence prediction" | BERT's second pretraining task; shown to be useless in RoBERTa, dropped after 2019. |
| NSP | "下一句预测" | BERT 的第二个预训练任务；RoBERTa 证明其无用，2019 年后弃用。 |
| Fine-tuning | "Adapt to a task" | Keep the encoder mostly frozen; train a small head on top for the downstream task. |
| 微调 | "适应任务" | 保持编码器基本冻结；在顶部训练一个小头用于下游任务。 |
| Cross-encoder | "A reranker" | A BERT that takes both query and doc as input, outputs a relevance score. |
| 交叉编码器 | "重排序器" | 同时接收查询和文档作为输入的 BERT，输出相关性分数。 |
| ModernBERT | "2024 refresh" | Encoder rebuilt with RoPE, RMSNorm, GeGLU, alternating local/global attention, 8K context. |
| ModernBERT | "2024 刷新版" | 用 RoPE、RMSNorm、GeGLU、交替局部/全局注意力重建的编码器，8K 上下文。 |

## Further Reading | 延伸阅读

- [Devlin et al. (2018). BERT: Pre-training of Deep Bidirectional Transformers for Language Understanding](https://arxiv.org/abs/1810.04805) — original paper.
  中文翻译：BERT 原始论文。
- [Liu et al. (2019). RoBERTa: A Robustly Optimized BERT Pretraining Approach](https://arxiv.org/abs/1907.11692) — how to train BERT right; kills NSP.
  中文翻译：如何正确训练 BERT；证明了 NSP 无用。
- [Clark et al. (2020). ELECTRA: Pre-training Text Encoders as Discriminators Rather Than Generators](https://arxiv.org/abs/2003.10555) — replaced-token detection beats MLM at matched compute.
  中文翻译：替换 token 检测在相同计算量下优于 MLM。
- [Warner et al. (2024). Smarter, Better, Faster, Longer: A Modern Bidirectional Encoder](https://arxiv.org/abs/2412.13663) — ModernBERT paper.
  中文翻译：ModernBERT 论文。
- [HuggingFace `modeling_bert.py`](https://github.com/huggingface/transformers/blob/main/src/transformers/models/bert/modeling_bert.py) — canonical encoder reference.
  中文翻译：HuggingFace BERT 模型实现参考代码。
