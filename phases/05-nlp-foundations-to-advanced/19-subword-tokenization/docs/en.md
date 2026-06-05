# Subword Tokenization — BPE, WordPiece, Unigram, SentencePiece | 子词分词 — BPE、WordPiece、SentencePiece

> Word tokenizers choke on unseen words. Character tokenizers blow up sequence length. Subword tokenizers split the difference. Every modern LLM ships on one.
> 词级分词器在未见词上卡住。字符分词器爆炸序列长度。子词分词器取中间值。每个现代 LLM 都用子词分词。

> **【中文解读】** BPE 是 GPT 用的分词算法，WordPiece 是 BERT 用的。

**Type:** Learn | **类型:** 学习
**Languages:** Python | **语言:** Python
**Prerequisites:** Phase 5 · 01 (Text Processing), Phase 5 · 04 (GloVe / FastText / Subword) | **前置知识:** Phase 5 · 01（文本处理），Phase 5 · 04（GloVe / FastText / 子词）
**Time:** ~60 minutes | **时间:** ~60 分钟

## The Problem | 问题引入

Your vocabulary has 50,000 words. A user types "untokenizable". Your tokenizer returns `[UNK]`. The model now has no signal about the word. Worse: the 90th-percentile document in your corpus has 40 rare words, which means 40 bits of dropped information per document.

> 你的词表有 50,000 个词。用户输入 "untokenizable"。你的分词器返回 `[UNK]`。模型现在对这个词没有信号。更糟的是：语料中第 90 百分位的文档有 40 个罕见词，意味着每篇文档丢失 40 位信息。

> **【中文解读】** 本节提出的问题是：如何在实际工程中正确理解和应用这一技术。理解问题背景有助于把握技术选型的关键决策点。在实际 AI 系统中，错误的技术选型往往比实现细节的 bug 代价更高。

Subword tokenization solves this. Common words stay single tokens. Rare words decompose into meaningful pieces: `untokenizable` → `un`, `token`, `izable`. Training data covers everything because any string is ultimately a sequence of bytes.

> 子词分词解决了这个问题。常见词保持单个 token。罕见词分解为有意义的片段：`untokenizable` → `un`、`token`、`izable`。训练数据覆盖一切，因为任何字符串最终都是字节序列。

Every frontier LLM in 2026 ships on one of three algorithms (BPE, Unigram, WordPiece), wrapped in one of three libraries (tiktoken, SentencePiece, HF Tokenizers). You cannot ship a language model without picking one.

> 2026 年的每个前沿 LLM 都基于三种算法之一（BPE、Unigram、WordPiece），包装在三种库之一（tiktoken、SentencePiece、HF Tokenizers）中。你无法不选择一个就发布语言模型。

## The Concept | 核心概念

> **【中文解读】** 本节介绍核心概念和理论基础。掌握这些概念是后续动手实现的前提，同时也是面试和工程实践中高频考察的知识点。

![BPE vs Unigram vs WordPiece, character-by-character](../assets/subword-tokenization.svg)

**BPE (Byte-Pair Encoding).** Start with a character-level vocabulary. Count every adjacent pair. Merge the most frequent pair into a new token. Repeat until you hit the target vocabulary size. Dominant algorithm: GPT-2/3/4, Llama, Gemma, Qwen2, Mistral.

> **BPE（字节对编码）。** 从字符级词表开始。统计每个相邻对。将最频繁的对合并为新 token。重复直到达到目标词表大小。主导算法：GPT-2/3/4、Llama、Gemma、Qwen2、Mistral。

**Byte-level BPE.** Same algorithm but over raw bytes (256 base tokens) instead of Unicode characters. Guarantees zero `[UNK]` tokens — any byte sequence encodes. GPT-2 uses 50,257 tokens (256 bytes + 50,000 merges + 1 special).

> **字节级 BPE。** 相同算法但在原始字节（256 个基础 token）而非 Unicode 字符上。保证零 `[UNK]` token — 任何字节序列都可编码。GPT-2 使用 50,257 个 token。

**Unigram.** Start with a huge vocabulary. Assign each token a unigram probability. Iteratively prune tokens whose removal least increases the corpus log-likelihood. Probabilistic at inference: can sample tokenizations. Used by T5, mBART, ALBERT, XLNet, Gemma.

> **Unigram。** 从巨大词表开始。给每个 token 分配 unigram 概率。迭代剪枝移除后对语料对数似然增加最少的 token。推理时是概率性的：可以采样分词结果。用于 T5、mBART、ALBERT、XLNet、Gemma。

**WordPiece.** Merge pairs that maximize likelihood of the training corpus rather than raw frequency. Used by BERT, DistilBERT, ELECTRA.

> **WordPiece。** 合并使训练语料似然最大化而非原始频率最高的对。用于 BERT、DistilBERT、ELECTRA。

**SentencePiece vs tiktoken.** SentencePiece is the library that *trains* vocabularies (BPE or Unigram) directly on raw Unicode text, encoding whitespace as `▁`. tiktoken is OpenAI's fast *encoder* against pre-built vocabularies; it does not train.

> **SentencePiece vs tiktoken。** SentencePiece 是在原始 Unicode 文本上*训练*词表的库，将空格编码为 `▁`。tiktoken 是 OpenAI 针对预构建词表的快速*编码器*；它不训练。

Rule of thumb:

> 经验法则：

- **Training a new vocabulary:** SentencePiece (multilingual, no pre-tokenization) or HF Tokenizers.
  **训练新词表：** SentencePiece（多语言，无预分词）或 HF Tokenizers。
- **Fast inference against GPT vocab:** tiktoken (cl100k_base, o200k_base).
  **针对 GPT 词表的快速推理：** tiktoken。
- **Both:** HF Tokenizers — one library, training + serving.
  **两者兼有：** HF Tokenizers — 一个库，训练 + 服务。

> **【中文解读】** 本节通过代码从零实现核心算法。这种 "from scratch" 的方式能帮助理解框架背后的原理，遇到问题时不会被黑盒困住。

> **【拓展：大语言模型的工程实践】** 从 GPT 到 ChatGPT，NLP 领域经历了从 "每个任务训练一个模型" 到 "一个模型解决所有任务" 的范式转变。在实际工程中，LLM 的部署需要考虑 Token 限制、延迟、成本、安全审查等问题。LangChain、LlamaIndex 等框架简化了 LLM 应用的开发。

> **【拓展：RAG 与企业知识库】** 检索增强生成（RAG）是当前企业 AI 应用最流行的架构：将用户查询先检索相关文档片段，再将检索结果作为上下文喂给 LLM 生成答案。这种方式解决了 LLM 知识过时和幻觉问题。向量数据库（如 Milvus、Pinecone、Weaviate）是 RAG 系统的核心组件。

> **【拓展：NLP 的多语言挑战】** 全球有 7000+ 种语言，但 NLP 研究主要集中在英语等少数语言。跨语言迁移学习、多语言预训练模型（如 mBERT、XLM-R）是解决低资源语言 NLP 的主要方法。字节级模型（如 ByT5）甚至可以在无分词器的情况下处理任何语言。

## Build It | 动手实现

> **【中文解读】** 本节通过代码从零实现核心算法。这种 "from scratch" 的方式能帮助理解框架背后的原理，遇到问题时不会被黑盒困住。

### Step 1: BPE from scratch

```python
from collections import Counter, defaultdict


def train_bpe(corpus, vocab_size, special_tokens=None):
    """Train BPE tokenizer from a list of pre-tokenized word strings."""
    special_tokens = special_tokens or ["<unk>"]
    word_freqs = Counter(corpus)
    splits = {word: list(word) for word in word_freqs}
    merges = {}

    while len(special_tokens) + len(set(t for parts in splits.values() for t in parts)) + len(merges) < vocab_size:
        pair_counts = Counter()
        for word, freq in word_freqs.items():
            symbols = splits[word]
            for i in range(len(symbols) - 1):
                pair_counts[(symbols[i], symbols[i + 1])] += freq
        if not pair_counts:
            break
        best = max(pair_counts, key=pair_counts.get)
        new_token = best[0] + best[1]
        merges[best] = new_token
        for word in splits:
            symbols = splits[word]
            new_symbols = []
            i = 0
            while i < len(symbols):
                if i < len(symbols) - 1 and (symbols[i], symbols[i + 1]) == best:
                    new_symbols.append(new_token)
                    i += 2
                else:
                    new_symbols.append(symbols[i])
                    i += 1
            splits[word] = new_symbols
    return merges, special_tokens


def bpe_encode(text, merges, special_tokens):
    """Encode text using learned BPE merges."""
    tokens = list(text)
    for (a, b), merged in merges.items():
        new_tokens = []
        i = 0
        while i < len(tokens):
            if i < len(tokens) - 1 and tokens[i] == a and tokens[i + 1] == b:
                new_tokens.append(merged)
                i += 2
            else:
                new_tokens.append(tokens[i])
                i += 1
        tokens = new_tokens
    return tokens
```

The merge order matters. BPE applies merges in training order, so earlier merges create longer tokens that block later ones. That is why BPE vocabularies are not portable across models.

> 合并顺序很重要。BPE 按训练顺序应用合并，所以较早的合并创建更长的 token，阻止后续合并。这就是为什么 BPE 词表不能跨模型移植。

### Step 2: tokenization with tiktoken and SentencePiece

```python
import tiktoken

enc = tiktoken.get_encoding("cl100k_base")
tokens = enc.encode("Hello, world!")
print(tokens)           # [9906, 11, 1917, 0]
print(enc.decode(tokens))  # Hello, world!
```

```python
import sentencepiece as spm

spm.SentencePieceTrainer.train(input="corpus.txt", model_prefix="m", vocab_size=1000)
sp = spm.SentencePieceProcessor(model_file="m.model")
print(sp.encode("Hello world", out_type=str))  # ['▁Hello', '▁world']
```

### Step 3: fertility comparison

```python
def fertility(text, tokenizer_fn):
    return len(tokenizer_fn(text))

# BPE on English: ~1.3 tokens/word
# BPE on Hindi: ~3.5 tokens/word
# BPE on Amharic: ~8 tokens/word
```

> **【中文解读】** 本节展示如何用成熟框架（如 PyTorch、HuggingFace 等）快速应用该技术。在实际项目中，优先使用经过验证的框架实现，可以减少 bug 并提高开发效率。

> **【拓展：Prompt Engineering 与 LLM 应用】** Prompt Engineering 已成为 NLP 工程师的核心技能。从 Zero-shot 到 Few-shot，从 Chain-of-Thought 到 ReAct，不同的提示策略适用于不同场景。在实际项目中，系统提示（System Prompt）的设计直接影响 LLM 应用的稳定性和输出质量。

## Use It | 用框架实现

Pick by ecosystem.

> 按生态系统选择。

- **OpenAI models (GPT-4, GPT-4o):** tiktoken. Fast, exact reproduction of OpenAI's tokenization. / tiktoken。快速、精确复现 OpenAI 分词。
- **Multilingual / custom training:** SentencePiece. Trains from raw text, handles any script. / SentencePiece。从原始文本训练，处理任何书写系统。
- **Hugging Face models:** AutoTokenizer. Wraps the right backend automatically. / AutoTokenizer。自动包装正确的后端。
- **Maximum speed at inference:** HF Tokenizers (Rust backend) or tiktoken (Python + C). / 推理最高速度：HF Tokenizers 或 tiktoken。

> **【中文解读】** 本节关注如何将模型部署为可用的产品。从原型到生产级系统需要考虑性能优化、错误处理、监控等多个维度。

## Ship It | 产出物

Save as `outputs/prompt-tokenizer-picker.md`:

> 保存为 `outputs/prompt-tokenizer-picker.md`：

```markdown
---
name: tokenizer-picker
description: Pick the right tokenizer for a given model or training pipeline.
phase: 5
lesson: 19
---

Given a model family or training goal, output:

1. Algorithm. BPE (GPT family), Unigram (T5 family), WordPiece (BERT family).
2. Library. tiktoken (GPT inference), SentencePiece (training), HF Tokenizers (both).
3. Vocabulary size and its impact on context window utilization.
4. Fertility estimate for the target language(s).

Refuse to mix tokenizer families in the same pipeline without explicit encode/decode boundaries.
```

> **【中文解读】** 练习题按照 Easy/Medium/Hard 三个难度递进。建议至少完成 Medium 级别的题目，Hard 级别适合深入研究或面试准备。

## Exercises | 练习题

1. **Easy.** Train BPE on a small corpus (1000 words). Encode and decode 20 test words. Verify round-trip fidelity. / **简单。** 在小型语料上训练 BPE。编码解码 20 个测试词。验证往返保真度。
2. **Medium.** Compare tokenization fertility for English, Chinese, and Hindi using tiktoken's cl100k_base. Report tokens-per-word for each. / **中等。** 使用 tiktoken 比较英语、中文和印地语的分词繁殖率。报告每种语言的每词 token 数。
3. **Hard.** Train a SentencePiece Unigram model on a mixed English-Hindi corpus. Compare fertility against a BPE model trained on the same data. / **困难。** 在混合英语-印地语语料上训练 SentencePiece Unigram 模型。与在相同数据上训练的 BPE 模型比较繁殖率。

> **【中文解读】** 术语表中的 "What people say" vs "What it actually means" 区分了日常口语和精确技术含义。在团队协作中，统一术语定义可以避免大量沟通误解。

## Key Terms | 术语速查表

| Term / 术语 | What people say / 人们常说的 | What it actually means / 实际含义 |
|------|-----------------|-----------------------|
| BPE（字节对编码） | GPT's tokenizer / GPT 的分词器 | Iteratively merge most frequent adjacent pairs. / 迭代合并最频繁的相邻对。 |
| Unigram | T5's tokenizer / T5 的分词器 | Prune tokens from large vocabulary by likelihood. / 按似然从大词表剪枝。 |
| WordPiece | BERT's tokenizer / BERT 的分词器 | Merge pairs that maximize corpus likelihood. / 合并使语料似然最大化的对。 |
| SentencePiece | Training library / 训练库 | Train BPE or Unigram on raw text. Encodes whitespace as `▁`. / 在原始文本上训练 BPE 或 Unigram。 |
| tiktoken | OpenAI's encoder / OpenAI 编码器 | Fast encoding against pre-built GPT vocabularies. / 针对预构建 GPT 词表的快速编码。 |
| Fertility（繁殖率） | Tokens per word / 每词 token 数 | How many subword tokens a word produces. Lower is better. / 一个词产生多少子词 token。越低越好。 |

> **【中文解读】** 延伸阅读提供了深入学习的高质量资源。这些论文和教程是该领域的经典参考文献，适合需要深入理解的读者。

## Further Reading | 延伸阅读

- [Sennrich et al. (2016). Neural Machine Translation of Rare Words with Subword Units](https://arxiv.org/abs/1508.07909) — the BPE paper. / BPE 论文。
- [Kudo (2018). Subword Regularization](https://arxiv.org/abs/1804.10959) — the Unigram paper. / Unigram 论文。
- [SentencePiece documentation](https://github.com/google/sentencepiece) — training and serving. / 训练和服务。
- [tiktoken](https://github.com/openai/tiktoken) — OpenAI's fast tokenizer. / OpenAI 快速分词器。
- [Hugging Face Tokenizers](https://huggingface.co/docs/tokenizers/) — Rust-backed training + serving. / Rust 后端训练 + 服务。
