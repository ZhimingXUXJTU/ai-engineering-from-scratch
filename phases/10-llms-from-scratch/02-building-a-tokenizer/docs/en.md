# Building a Tokenizer from Scratch | 从零构建分词器

> Lesson 01 gave you a toy. This lesson gives you a weapon.

> **【中文解读】** 第一课的 BPE 是玩具，本课构建生产级分词器：处理 Unicode、空白归一化、特殊 token、字节级回退（让任何输入都能编码，包括 emoji 和中文）。

> **【拓展：tiktoken/HuggingFace】** GPT-4 的 tiktoken 和 Llama 的 sentencepiece 都是生产级分词器的实现。理解它们的内部原理有助于优化 prompt 工程和成本控制。

**Type:** Build
**Languages:** Python
**Prerequisites:** Phase 10, Lesson 01 (Tokenizers: BPE, WordPiece, SentencePiece)
**Time:** ~90 minutes

## Learning Objectives

- Build a production-grade BPE tokenizer that handles Unicode, whitespace normalization, and special tokens
- Implement byte-level fallback so the tokenizer can encode any input (including emoji, CJK, and code) without unknown tokens
- Add pre-tokenization regex patterns that split text at word boundaries before applying BPE merges
- Train a custom tokenizer on a corpus and evaluate its compression ratio against tiktoken on multilingual text

> **【中文解读】** 本课目标是将第一课的玩具 BPE 升级为生产级分词器。关键改进包括：Unicode 归一化（NFKC）、预分词正则（防止跨词边界的合并）、字节级回退（零未知 token）、特殊 token 管理（BOS/EOS/聊天模板标记）。这些是让分词器处理"整个互联网"的必备机制。

## The Problem | 问题引入

Your BPE tokenizer from Lesson 01 works on English text. Now throw Japanese at it. Or emoji. Or Python code with mixed tabs and spaces.

It breaks.

Not because BPE is wrong -- because the implementation is incomplete. A production tokenizer handles raw bytes in any encoding, normalizes Unicode before splitting, manages special tokens that never get merged, chains pre-tokenization with subword splitting, and does all of this fast enough to not bottleneck a training pipeline processing 15 trillion tokens.

GPT-2's tokenizer has 50,257 tokens. Llama 3 has 128,256. GPT-4 has roughly 100,000. These are not toy numbers. The merge tables behind those vocabularies were trained on hundreds of gigabytes of text, and the surrounding machinery -- normalization, pre-tokenization, special token injection, chat template formatting -- is what separates a tokenizer that handles "hello world" from one that handles the entire internet.

You are going to build that machinery.

> **【中文解读】** 生产级分词器不是单一算法，而是一个五阶段管线：归一化 → 预分词 → BPE 合并 → 特殊 token 注入 → ID 映射。每个阶段解决不同的问题。例如 NFKC 归一化把 "fi" 连字（U+FB01）变成 "fi" 两个字符，预分词防止 "the cat" 被合并出 "e c" 这样的 token。

> **【拓展：Llama 3 的分词器升级】** Meta 在 Llama 3 中将词表从 32K（Llama 2 的 SentencePiece BPE）升级到 128K（tiktoken 风格字节级 BPE），专门增加了非英语文字的 token 分配。这个改变使多语言压缩效率提升了约 2 倍，但嵌入矩阵参数量也相应增加了 4 倍（32K→128K）。

## The Concept | 核心概念

### The Full Pipeline

A production tokenizer is not one algorithm. It is a pipeline of five stages, each solving a different problem.

```mermaid
graph LR
    A[Raw Text] --> B[Normalize]
    B --> C[Pre-Tokenize]
    C --> D[BPE Merge]
    D --> E[Special Tokens]
    E --> F[Token IDs]

    style A fill:#1a1a2e,stroke:#e94560,color:#fff
    style B fill:#1a1a2e,stroke:#e94560,color:#fff
    style C fill:#1a1a2e,stroke:#e94560,color:#fff
    style D fill:#1a1a2e,stroke:#e94560,color:#fff
    style E fill:#1a1a2e,stroke:#e94560,color:#fff
    style F fill:#1a1a2e,stroke:#e94560,color:#fff
```

Each stage has a specific job:

| Stage | What It Does | Why It Matters |
|-------|-------------|----------------|
| Normalize | NFKC Unicode, lowercase optional, strip accents optional | "fi" ligature (U+FB01) becomes "fi" (two chars). Without this, same word gets different tokens. |
| Pre-Tokenize | Split text into chunks before BPE | Prevents BPE from merging across word boundaries. "the cat" should never produce a token "e c". |
| BPE Merge | Apply learned merge rules to byte sequences | The core compression. Turns raw bytes into subword tokens. |
| Special Tokens | Inject [BOS], [EOS], [PAD], chat template markers | These tokens have fixed IDs. They never participate in BPE merges. The model needs them for structure. |
| ID Mapping | Convert token strings to integer IDs | The model sees integers, not strings. |

### Byte-Level BPE

Lesson 01's tokenizer operated on UTF-8 bytes. That was the right call. But we skipped something important: what happens when those bytes are not valid UTF-8?

Byte-level BPE solves this by treating every possible byte value (0-255) as a valid token. Your base vocabulary is exactly 256 entries. Any file -- text, binary, corrupted -- can be tokenized without producing an unknown token.

GPT-2 added a trick: map each byte to a printable Unicode character so the vocabulary stays human-readable. Byte 0x20 (space) becomes the character "G" in their mapping. This is purely cosmetic. The algorithm does not care.

The real power: byte-level BPE handles every language on earth. Chinese characters are 3 UTF-8 bytes each. Japanese can be 3-4 bytes. Arabic, Devanagari, emoji -- all just byte sequences. The BPE algorithm finds patterns in these byte sequences exactly the same way it finds patterns in English ASCII bytes.

> **【中文解读】** 字节级 BPE 的核心优势：基础词表恰好 256 个字节值，任何输入都能编码。GPT-2 还做了一个"花招"——把每个字节映射到一个可打印的 Unicode 字符，让词表更易读。中文字符在 UTF-8 中每个占 3 字节，日文占 3-4 字节，emoji 占 4 字节——BPE 算法在所有这些字节序列上以完全相同的方式工作。

### Pre-Tokenization

Before BPE touches your text, you need to split it into chunks. This prevents the merge algorithm from creating tokens that span word boundaries.

GPT-2 uses a regex pattern to split text:

```
'(?:[sdmt]|ll|ve|re)| ?\p{L}+| ?\p{N}+| ?[^\s\p{L}\p{N}]+|\s+(?!\S)|\s+
```

This pattern splits on contractions ("don't" becomes "don" + "'t"), words with optional leading spaces, numbers, punctuation, and whitespace. The leading space is kept attached to the word -- so "the cat" becomes [" the", " cat"], not ["the", " ", "cat"].

Llama uses SentencePiece, which skips regex entirely. It treats the raw byte stream as one long sequence and lets the BPE algorithm figure out the boundaries. This is simpler but gives BPE more freedom to create cross-word tokens.

The choice matters. GPT-2's regex prevents the tokenizer from learning that "the" at the end of one word and "the" at the start of the next should merge. SentencePiece allows it, which sometimes produces more efficient compression but less interpretable tokens.

### Special Tokens

Every production tokenizer reserves token IDs for structural markers:

| Token | Purpose | Used By |
|-------|---------|---------|
| `[BOS]` / `<s>` | Beginning of sequence | Llama 3, GPT |
| `[EOS]` / `</s>` | End of sequence | All models |
| `[PAD]` | Padding for batch alignment | BERT, T5 |
| `[UNK]` | Unknown token (byte-level BPE eliminates this) | BERT, WordPiece |
| `<\|im_start\|>` | Chat message boundary start | ChatGPT, Qwen |
| `<\|im_end\|>` | Chat message boundary end | ChatGPT, Qwen |
| `<\|user\|>` | User turn marker | Llama 3 |
| `<\|assistant\|>` | Assistant turn marker | Llama 3 |

Special tokens are never split by BPE. They are matched exactly before the merge algorithm runs, replaced with their fixed ID, and the surrounding text is tokenized normally.

> **【中文解读】** 特殊 token 是分词器中"不可触碰"的保留标记：`[BOS]`（序列开始）、`[EOS]`（序列结束）、`[PAD]`（批次填充）、聊天模板标记等。它们有固定的 ID，永远不参与 BPE 合并，而是在合并之前通过精确匹配被提取出来。Llama 3 使用 `<|start_header_id|>`、`<|end_header_id|>`、`<|eot_id|>` 来标记对话结构，ChatGPT 使用 `<|im_start|>` 和 `<|im_end|>`。

> **【拓展：聊天模板的工程陷阱】** 聊天模板是实际部署中最容易出错的地方。每个模型在训练时使用特定格式的特殊 token，任何偏差——缺少换行、多一个空格、token 顺序错误——都会让输入偏离训练分布，导致模型输出垃圾。HuggingFace 的 `chat_template` Jinja2 模板机制就是为了标准化这个过程。

### Chat Templates

This is where most people get confused and most implementations break.

When you send messages to a chat model, the API accepts a list of messages:

```
[
  {"role": "system", "content": "You are helpful."},
  {"role": "user", "content": "Hello"},
  {"role": "assistant", "content": "Hi there!"}
]
```

The model does not see JSON. It sees a flat token sequence. The chat template converts messages into that flat sequence using special tokens. Every model does this differently:

```
Llama 3:
<|begin_of_text|><|start_header_id|>system<|end_header_id|>

You are helpful.<|eot_id|><|start_header_id|>user<|end_header_id|>

Hello<|eot_id|><|start_header_id|>assistant<|end_header_id|>

Hi there!<|eot_id|>

ChatGPT:
<|im_start|>system
You are helpful.<|im_end|>
<|im_start|>user
Hello<|im_end|>
<|im_start|>assistant
Hi there!<|im_end|>
```

Get the template wrong and the model produces garbage. It was trained on one exact format. Any deviation -- a missing newline, a swapped token, an extra space -- puts the input outside the training distribution.

### Speed

Python is too slow for production tokenization.

tiktoken (OpenAI) is written in Rust with Python bindings. HuggingFace tokenizers is also Rust. SentencePiece is C++. These achieve 10-100x speedups over pure Python.

For perspective: tokenizing 15 trillion tokens for Llama 3 pre-training at 1 million tokens per second (fast Python) would take 174 days. At 100 million tokens per second (Rust), it takes 1.7 days.

You are building in Python to understand the algorithm. In production, you would use a compiled implementation and only touch the Python wrapper.

## Build It | 动手实现

### Step 1: Byte-Level Encoding

The foundation. Convert any string into a sequence of bytes, map each byte to a printable character for display, and reverse the process.

```python
def bytes_to_tokens(text):
    return list(text.encode("utf-8"))

def tokens_to_text(token_bytes):
    return bytes(token_bytes).decode("utf-8", errors="replace")
```

Test on multilingual text to see the byte counts:

```python
texts = [
    ("English", "hello"),
    ("Chinese", "你好"),
    ("Emoji", "🔥"),
    ("Mixed", "hello你好🔥"),
]

for label, text in texts:
    b = bytes_to_tokens(text)
    print(f"{label}: {len(text)} chars -> {len(b)} bytes -> {b}")
```

"hello" is 5 bytes. "你好" is 6 bytes (3 per character). The fire emoji is 4 bytes. The byte-level tokenizer does not care what language it is. Bytes are bytes.

### Step 2: Pre-Tokenizer with Regex

Split text into chunks using the GPT-2 regex pattern. Each chunk gets tokenized independently by BPE.

```python
import re

try:
    import regex
    GPT2_PATTERN = regex.compile(
        r"""'(?:[sdmt]|ll|ve|re)| ?\p{L}+| ?\p{N}+| ?[^\s\p{L}\p{N}]+|\s+(?!\S)|\s+"""
    )
except ImportError:
    GPT2_PATTERN = re.compile(
        r"""'(?:[sdmt]|ll|ve|re)| ?[a-zA-Z]+| ?[0-9]+| ?[^\s\w]+|\s+(?!\S)|\s+"""
    )

def pre_tokenize(text):
    return [match.group() for match in GPT2_PATTERN.finditer(text)]
```

The `regex` module supports Unicode property escapes (`\p{L}` for letters, `\p{N}` for numbers). The standard library `re` module does not, so we fall back to ASCII character classes. For production multilingual tokenizers, install `regex`.

Try it:

```python
print(pre_tokenize("Hello, world! Don't stop."))
# [' Hello', ',', ' world', '!', " Don", "'t", ' stop', '.']
```

The leading space stays attached to the word. Contractions split at the apostrophe. Punctuation becomes its own chunk. BPE will never merge tokens across these boundaries.

### Step 3: BPE on Byte Sequences

The core algorithm from Lesson 01, but now operating on pre-tokenized chunks independently.

```python
from collections import Counter

def get_byte_pairs(chunks):
    pairs = Counter()
    for chunk in chunks:
        byte_seq = list(chunk.encode("utf-8"))
        for i in range(len(byte_seq) - 1):
            pairs[(byte_seq[i], byte_seq[i + 1])] += 1
    return pairs

def apply_merge(byte_seq, pair, new_id):
    merged = []
    i = 0
    while i < len(byte_seq):
        if i < len(byte_seq) - 1 and byte_seq[i] == pair[0] and byte_seq[i + 1] == pair[1]:
            merged.append(new_id)
            i += 2
        else:
            merged.append(byte_seq[i])
            i += 1
    return merged
```

### Step 4: Special Token Handling

Special tokens need exact matching and fixed IDs. They bypass BPE entirely.

```python
class SpecialTokenHandler:
    def __init__(self):
        self.special_tokens = {}
        self.pattern = None

    def add_token(self, token_str, token_id):
        self.special_tokens[token_str] = token_id
        escaped = [re.escape(t) for t in sorted(self.special_tokens.keys(), key=len, reverse=True)]
        self.pattern = re.compile("|".join(escaped))

    def split_with_specials(self, text):
        if not self.pattern:
            return [(text, False)]
        parts = []
        last_end = 0
        for match in self.pattern.finditer(text):
            if match.start() > last_end:
                parts.append((text[last_end:match.start()], False))
            parts.append((match.group(), True))
            last_end = match.end()
        if last_end < len(text):
            parts.append((text[last_end:], False))
        return parts
```

### Step 5: Full Tokenizer Class

Chain everything together: normalize, split on special tokens, pre-tokenize, BPE merge, map to IDs.

```python
import unicodedata

class ProductionTokenizer:
    def __init__(self):
        self.merges = {}
        self.vocab = {i: bytes([i]) for i in range(256)}
        self.special_handler = SpecialTokenHandler()
        self.next_id = 256

    def normalize(self, text):
        return unicodedata.normalize("NFKC", text)

    def train(self, text, num_merges):
        text = self.normalize(text)
        chunks = pre_tokenize(text)
        chunk_bytes = [list(chunk.encode("utf-8")) for chunk in chunks]

        for i in range(num_merges):
            pairs = Counter()
            for seq in chunk_bytes:
                for j in range(len(seq) - 1):
                    pairs[(seq[j], seq[j + 1])] += 1
            if not pairs:
                break
            best = max(pairs, key=pairs.get)
            new_id = self.next_id
            self.next_id += 1
            self.merges[best] = new_id
            self.vocab[new_id] = self.vocab[best[0]] + self.vocab[best[1]]
            chunk_bytes = [apply_merge(seq, best, new_id) for seq in chunk_bytes]

    def add_special_token(self, token_str):
        token_id = self.next_id
        self.next_id += 1
        self.special_handler.add_token(token_str, token_id)
        self.vocab[token_id] = token_str.encode("utf-8")
        return token_id

    def encode(self, text):
        text = self.normalize(text)
        parts = self.special_handler.split_with_specials(text)
        all_ids = []
        for part_text, is_special in parts:
            if is_special:
                all_ids.append(self.special_handler.special_tokens[part_text])
            else:
                for chunk in pre_tokenize(part_text):
                    byte_seq = list(chunk.encode("utf-8"))
                    for pair, new_id in self.merges.items():
                        byte_seq = apply_merge(byte_seq, pair, new_id)
                    all_ids.extend(byte_seq)
        return all_ids

    def decode(self, ids):
        byte_parts = []
        for token_id in ids:
            if token_id in self.vocab:
                byte_parts.append(self.vocab[token_id])
        return b"".join(byte_parts).decode("utf-8", errors="replace")

    def vocab_size(self):
        return len(self.vocab)
```

### Step 6: Multilingual Test

The real test. Throw English, Chinese, emoji, and code at it.

```python
corpus = (
    "The quick brown fox jumps over the lazy dog. "
    "The quick brown fox runs through the forest. "
    "Machine learning models process natural language. "
    "Deep learning transforms how we build software. "
    "def train(model, data): return model.fit(data) "
    "def predict(model, x): return model(x) "
)

tok = ProductionTokenizer()
tok.train(corpus, num_merges=50)

bos = tok.add_special_token("<|begin|>")
eos = tok.add_special_token("<|end|>")

test_texts = [
    "The quick brown fox.",
    "你好世界",
    "Hello 🌍 World",
    "def foo(x): return x + 1",
    f"<|begin|>Hello<|end|>",
]

for text in test_texts:
    ids = tok.encode(text)
    decoded = tok.decode(ids)
    print(f"Input:   {text}")
    print(f"Tokens:  {len(ids)} ids")
    print(f"Decoded: {decoded}")
    print()
```

Chinese characters produce 3 bytes each. The emoji produces 4 bytes. None of these crash the tokenizer. None produce unknown tokens. That is the power of byte-level BPE.

> **【中文解读】** 以上代码将所有组件串联起来：归一化 → 特殊 token 分割 → 预分词 → BPE 合并 → ID 映射。测试覆盖了英文、中文、emoji、代码和特殊 token 的混合场景。字节级 BPE 保证任何输入都不会产生未知 token——这就是它成为工业标准的根本原因。

> **【拓展：分词速度的工程意义】** 纯 Python 分词器每秒处理约 1M tokens，Llama 3 的预训练语料有 15 万亿 tokens，用 Python 需 174 天。tiktoken（Rust 实现）每秒 100M tokens，只需 1.7 天。这就是为什么生产级分词器都用编译语言：tiktoken 用 Rust，HuggingFace tokenizers 用 Rust，SentencePiece 用 C++。

## Use It | 用框架实现

### Comparing Real Tokenizers

Load the actual tokenizers from Llama 3, GPT-4, and Mistral. See how each handles the same multilingual paragraph.

```python
import tiktoken

gpt4_enc = tiktoken.get_encoding("cl100k_base")

test_paragraph = "Machine learning is powerful. 机器学习很强大。 L'apprentissage automatique est puissant. 🤖💪"

tokens = gpt4_enc.encode(test_paragraph)
pieces = [gpt4_enc.decode([t]) for t in tokens]
print(f"GPT-4 ({len(tokens)} tokens): {pieces}")
```

```python
from transformers import AutoTokenizer

llama_tok = AutoTokenizer.from_pretrained("meta-llama/Meta-Llama-3-8B")
mistral_tok = AutoTokenizer.from_pretrained("mistralai/Mistral-7B-v0.1")

for name, tok in [("Llama 3", llama_tok), ("Mistral", mistral_tok)]:
    tokens = tok.encode(test_paragraph)
    pieces = tok.convert_ids_to_tokens(tokens)
    print(f"{name} ({len(tokens)} tokens): {pieces[:20]}...")
```

You will see different token counts for the same text. Llama 3 with 128K vocabulary is more aggressive at merging common patterns. GPT-4 with 100K sits in the middle. Mistral with 32K produces more tokens but has a smaller embedding layer.

The tradeoff is always the same: larger vocabulary means shorter sequences but more parameters.

## Ship It | 产出物

This lesson produces a prompt for building and debugging production tokenizers. See `outputs/prompt-tokenizer-builder.md`.

## Exercises | 练习题

1. **Easy:** Add a `get_token_bytes(id)` method that shows the raw bytes for any token ID. Use it to inspect what your most common merged tokens actually represent.
2. **Medium:** Implement the Llama-style pre-tokenizer that splits on whitespace and digits but keeps leading spaces. Compare its vocabulary with the GPT-2 regex approach on the same corpus.
3. **Hard:** Add a chat template method that takes a list of `{"role": ..., "content": ...}` messages and produces the correct token sequence for the Llama 3 chat format. Test it against the HuggingFace implementation.

## Key Terms | 术语速查表

| Term | What people say | What it actually means | 中文释义 |
|------|----------------|----------------------|---------|
| Byte-level BPE | "Tokenizer that works on bytes" | BPE with a base vocabulary of 256 byte values -- handles any input without unknown tokens | 字节级 BPE，基础词表 256 个字节值 |
| Pre-tokenization | "Splitting before BPE" | Regex or rule-based splitting that prevents BPE from merging across word boundaries | 预分词，防止跨词边界的 token 合并 |
| NFKC normalization | "Unicode cleanup" | Canonical decomposition followed by compatibility composition -- "fi" ligature becomes "fi", fullwidth "A" becomes "A" | NFKC 归一化，统一 Unicode 表示 |
| Chat template | "How messages become tokens" | The exact format for converting a list of role/content messages into a flat token sequence -- model-specific and must match training format | 聊天模板，消息转 token 的格式规则 |
| Special tokens | "Control tokens" | Reserved token IDs that bypass BPE -- [BOS], [EOS], [PAD], chat markers -- matched exactly before merge | 特殊 token，绕过 BPE 的控制标记 |
| Fertility | "Tokens per word" | Ratio of output tokens to input words -- 1.3 for English in GPT-4, 2-3 for Korean, higher means wasted context | 生育率，每词 token 数 |
| tiktoken | "OpenAI tokenizer" | Rust BPE implementation with Python bindings -- 10-100x faster than pure Python | OpenAI 的 Rust 分词器实现 |
| Merge table | "The vocabulary" | Ordered list of byte-pair merges learned during training -- this IS the tokenizer's learned knowledge | 合并表，分词器的核心知识 |

## Further Reading | 延伸阅读

- [OpenAI tiktoken source](https://github.com/openai/tiktoken) -- Rust BPE implementation used by GPT-3.5/4
- [HuggingFace tokenizers](https://github.com/huggingface/tokenizers) -- Rust tokenizer library supporting BPE, WordPiece, Unigram
- [Llama 3 paper (Meta, 2024)](https://arxiv.org/abs/2407.21783) -- details on 128K vocabulary and tokenizer training
- [SentencePiece (Kudo & Richardson, 2018)](https://arxiv.org/abs/1808.06226) -- language-agnostic tokenization
- [GPT-2 tokenizer source](https://github.com/openai/gpt-2/blob/master/src/encoder.py) -- the original byte-to-Unicode mapping
