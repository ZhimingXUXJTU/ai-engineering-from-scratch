# Tokenizers: BPE, WordPiece, SentencePiece | 分词器：BPE、WordPiece、SentencePiece

> Your LLM does not read English. It reads integers. The tokenizer decides whether those integers carry meaning or waste it.

> **【中文解读】** LLM 不读英文，它读整数。分词器决定这些整数是有意义还是浪费。子词分词（subword tokenization）在词级和字符级之间找到平衡点：常见词保持完整，罕见词拆分为有意义的片段。GPT-4 用 BPE，Llama 用 SentencePiece。

> **【拓展：BPE→GPT系列】** OpenAI 的所有模型（GPT-2、GPT-3、GPT-4）都使用 BPE 分词器。tiktoken 是 GPT 系列的分词器库。分词质量直接影响上下文窗口利用率——"unfortunately" 拆成4个 token vs 1个 token，等于上下文窗口缩水 75%。

**Type:** Build
**Languages:** Python
**Prerequisites:** Phase 05 (NLP Foundations)
**Time:** ~90 minutes

## Learning Objectives | 学习目标

- Implement BPE, WordPiece, and Unigram tokenization algorithms from scratch and compare their merge strategies
  从零实现 BPE、WordPiece 和 Unigram 分词算法，比较它们的合并策略
- Explain how vocabulary size affects model efficiency: too small creates long sequences, too large wastes embedding parameters
  解释词表大小如何影响模型效率：太小产生长序列，太大浪费嵌入参数
- Analyze tokenization artifacts across languages and code, identifying where specific tokenizers break down
  分析跨语言和代码的分词边界情况，找出特定分词器的失效点
- Use the tiktoken and sentencepiece libraries to tokenize text and inspect the resulting token IDs
  使用 tiktoken 和 sentencepiece 库分词文本并检查生成的 token ID

> **【中文解读】** 本章的学习目标围绕分词器的四个维度：实现（手写 BPE/WordPiece/Unigram 算法）、理解（词表大小的工程权衡）、分析（跨语言分词的边界情况）、应用（tiktoken/sentencepiece 工具库）。分词是 LLM 管线的第一步，直接影响模型效率和成本。

## The Problem | 问题引入

Your LLM does not read English. It does not read any language. It reads numbers.

> 你的 LLM 不读英文。它不读任何语言。它读数字。

The gap between "Hello, world!" and [15496, 11, 995, 0] is the tokenizer. Every word, every space, every punctuation mark must be converted into an integer before a model can process it. This conversion is not neutral. It bakes assumptions into the model that cannot be undone later.

> "Hello, world!" 和 [15496, 11, 995, 0] 之间的桥梁就是分词器。每个词、每个空格、每个标点符号都必须转换为整数，模型才能处理。这种转换并非中性的——它将假设固化到模型中，且日后无法撤销。

Get this wrong and your model wastes capacity encoding common words with multiple tokens. "unfortunately" becomes four tokens instead of one. Your 128K context window just shrank by 75% for text heavy in multi-syllable words. Get it right and the same context window holds twice as much meaning. The difference between "this model handles code well" and "this model chokes on Python" often comes down to how the tokenizer was trained.

> 做错了，你的模型就会浪费容量用多个 token 编码常见词。"unfortunately" 变成四个 token 而不是一个。你 128K 的上下文窗口对于多音节词密集的文本直接缩水了 75%。做对了，同样的上下文窗口能装下两倍的信息。"这个模型处理代码很好"和"这个模型在 Python 上卡壳"的区别，往往取决于分词器是如何训练的。

Every API call you make to GPT-4 or Claude is priced per token. Every token your model generates costs compute. The fewer tokens required to represent an output, the faster the end-to-end inference. Tokenization is not preprocessing. It is architecture.

> 你每次调用 GPT-4 或 Claude 的 API 都是按 token 计费的。你的模型生成的每个 token 都消耗算力。表示一个输出所需的 token 越少，端到端推理就越快。分词不是预处理。它是架构。

> **【中文解读】** 分词不是简单的预处理步骤，而是模型架构的一部分。每次调用 GPT-4 API 都按 token 计费，每个 token 的生成都消耗算力。"unfortunately" 被拆成 4 个 token 意味着上下文窗口利用率下降 75%。分词器的设计直接决定了模型处理不同语言和代码的能力。

> **【拓展：API 定价与分词效率】** GPT-4o 的定价为 $5/M input tokens、$15/M output tokens。同一个中文段落，用 GPT-2 分词器可能消耗 500 tokens，用 GPT-4o 的 o200k_base 分词器只需约 200 tokens，成本差 2.5 倍。这也是为什么 Llama 3 将词表从 32K 扩展到 128K——降低非英语用户的推理成本。

## The Concept | 核心概念

### Three Approaches That Failed (and One That Won)

There are three obvious ways to convert text to numbers. Two of them do not work at scale.

> 有三种显而易见的方法将文本转换为数字。其中两种在大规模场景下无法工作。

**Word-level tokenization** splits on spaces and punctuation. "The cat sat" becomes ["The", "cat", "sat"]. Simple. But what about "tokenization"? Or "GPT-4o"? Or a German compound word like "Geschwindigkeitsbegrenzung"? Word-level requires a massive vocabulary to cover every word in every language. Miss a word and you get the dreaded `[UNK]` token -- the model's way of saying "I have no idea what this is." English alone has over a million word forms. Add code, URLs, scientific notation, and 100 other languages and you need an infinite vocabulary.

> **词级分词**按空格和标点拆分。"The cat sat" 变成 ["The", "cat", "sat"]。很简单。但 "tokenization" 呢？"GPT-4o" 呢？或者德语复合词 "Geschwindigkeitsbegrenzung" 呢？词级分词需要一个巨大的词表来覆盖每种语言的每个词。遗漏一个词就会出现可怕的 `[UNK]` token——模型在说"我完全不知道这是什么"。仅英语就有超过一百万个词形。加上代码、URL、科学记数法和 100 种其他语言，你需要一个无限大的词表。

**Character-level tokenization** goes the other direction. "hello" becomes ["h", "e", "l", "l", "o"]. Vocabulary is tiny (a few hundred characters). No unknown tokens ever. But sequences become extremely long. A sentence that would be 10 word-level tokens becomes 50 character-level tokens. The model must learn that "t", "h", "e" together mean "the" -- burning attention capacity on something a human learns at age three.

> **字符级分词**走向另一个极端。"hello" 变成 ["h", "e", "l", "l", "o"]。词表很小（几百个字符）。永远不会出现未知 token。但序列变得极长。一个 10 个词级 token 的句子变成 50 个字符级 token。模型必须学会 "t"、"h"、"e" 组合起来是 "the"——把注意力容量浪费在人类三岁就学会的事情上。

**Subword tokenization** finds the sweet spot. Common words stay whole: "the" is one token. Rare words decompose into meaningful pieces: "unhappiness" becomes ["un", "happi", "ness"]. Vocabulary stays manageable (30K to 128K tokens). Sequences stay short. Unknown tokens essentially disappear because any word can be built from subword pieces.

> **子词分词**找到了最佳平衡点。常见词保持完整："the" 是一个 token。罕见词分解为有意义的片段："unhappiness" 变成 ["un", "happi", "ness"]。词表保持在可控范围（30K 到 128K 个 token）。序列保持简短。未知 token 基本消失，因为任何词都可以由子词片段构建。

> **【中文解读】** 词级分词（word-level）的问题是词表爆炸——英语有百万级词形，加上代码、URL、科学记数法和其他语言，词表会无限增长。字符级分词（character-level）虽然词表小，但序列太长，模型要学会 "t"+"h"+"e" 组合为 "the"，浪费注意力容量。子词分词在两者之间取得平衡：常见词保持完整，罕见词拆分为有意义的片段。

Every modern LLM uses subword tokenization. GPT-2, GPT-4, BERT, Llama 3, Claude -- all of them. The question is which algorithm.

> 每个现代 LLM 都使用子词分词。GPT-2、GPT-4、BERT、Llama 3、Claude——全都如此。问题在于使用哪种算法。

```mermaid
graph TD
    A["Text: 'unhappiness'"] --> B{"Tokenization Strategy"}
    B -->|Word-level| C["['unhappiness']\n1 token if in vocab\n[UNK] if not"]
    B -->|Character-level| D["['u','n','h','a','p','p','i','n','e','s','s']\n11 tokens"]
    B -->|Subword BPE| E["['un','happi','ness']\n3 tokens"]

    style C fill:#ff6b6b,color:#fff
    style D fill:#ffa500,color:#fff
    style E fill:#51cf66,color:#fff
```

### BPE: Byte Pair Encoding

BPE is a greedy compression algorithm repurposed for tokenization. The idea is simple enough to fit on an index card.

> BPE 是一种被重新用于分词的贪心压缩算法。其思想简单到可以写在一张索引卡上。

Start with individual characters. Count every adjacent pair in the training corpus. Merge the most frequent pair into a new token. Repeat until you reach your target vocabulary size.

> 从单个字符开始。统计训练语料中所有相邻字符对的出现频率。将最高频的对合并为新 token。重复直到达到目标词表大小。

Here is BPE running on a tiny corpus with the words "lower", "lowest", and "newest":

```
Corpus (with word frequencies):
  "lower"  x5
  "lowest" x2
  "newest" x6

Step 0 -- Start with characters:
  l o w e r       (x5)
  l o w e s t     (x2)
  n e w e s t     (x6)

Step 1 -- Count adjacent pairs:
  (e,s): 8    (s,t): 8    (l,o): 7    (o,w): 7
  (w,e): 13   (e,r): 5    (n,e): 6    ...

Step 2 -- Merge most frequent pair (w,e) -> "we":
  l o we r        (x5)
  l o we s t      (x2)
  n e we s t      (x6)

Step 3 -- Recount and merge (e,s) -> "es":
  l o we r        (x5)
  l o we s t      (x2)    <- 'es' only forms from 'e'+'s', not 'we'+'s'
  n e we s t      (x6)    <- wait, the 'e' before 'we' and 's' after 'we'

Actually tracking this precisely:
  After "we" merge, remaining pairs:
  (l,o): 7   (o,we): 7   (we,r): 5   (we,s): 8
  (s,t): 8   (n,e): 6    (e,we): 6

Step 3 -- Merge (we,s) -> "wes" or (s,t) -> "st" (tied at 8, pick first):
  Merge (we,s) -> "wes":
  l o we r        (x5)
  l o wes t       (x2)
  n e wes t       (x6)

Step 4 -- Merge (wes,t) -> "west":
  l o we r        (x5)
  l o west        (x2)
  n e west        (x6)

...continue until target vocab size reached.
```

The merge table is the tokenizer. To encode new text, apply merges in the order they were learned. The training corpus determines which merges exist, and that choice permanently shapes what the model sees.

> 合并表就是分词器。编码新文本时，按学习顺序应用合并。训练语料决定了哪些合并存在，这个选择永久地塑造了模型看到的内容。

> **【中文解读】** BPE 的核心训练循环：从单个字符开始，统计所有相邻字符对的出现频率，将最高频的对合并为新 token，重复直到达到目标词表大小。合并表（merge table）就是分词器本身。编码新文本时，按训练时学到的顺序依次应用合并规则——顺序很重要，因为合并 1 可能产生 "th"，合并 5 才能在 "th"+"e" 的基础上产生 "the"。

> **【拓展：BPE 的压缩原理】** BPE 最初是 1994 年的通用数据压缩算法。Sennrich 等人在 2016 年将其引入 NLP 领域。在生产环境中，tiktoken 在 Rust 中实现了 BPE，编码速度可达每秒数百万 token。GPT-4 的 cl100k_base 编码器在数百 GB 文本上训练了约 100,000 次合并。

```mermaid
graph LR
    subgraph Training["BPE Training Loop"]
        direction TB
        T1["Start: character vocabulary"] --> T2["Count all adjacent pairs"]
        T2 --> T3["Merge most frequent pair"]
        T3 --> T4["Add merged token to vocab"]
        T4 --> T5{"Reached target\nvocab size?"}
        T5 -->|No| T2
        T5 -->|Yes| T6["Done: save merge table"]
    end
```

### Byte-Level BPE (GPT-2, GPT-3, GPT-4)

Standard BPE operates on Unicode characters. Byte-level BPE operates on raw bytes (0-255). This gives you a base vocabulary of exactly 256, handles any language or encoding, and never produces an unknown token.

> 标准 BPE 操作 Unicode 字符。字节级 BPE 操作原始字节（0-255）。这给你一个恰好 256 个的基础词表，能处理任何语言或编码，永远不会产生未知 token。

GPT-2 introduced this approach. The base vocabulary covers every possible byte. BPE merges build on top of that. OpenAI's tiktoken library implements byte-level BPE with these vocabulary sizes:

> GPT-2 引入了这种方法。基础词表覆盖每个可能的字节。BPE 合并在其之上构建。OpenAI 的 tiktoken 库实现了字节级 BPE，词表大小如下：

> **【中文解读】** 字节级 BPE（Byte-level BPE）是 GPT-2 引入的关键创新。传统 BPE 操作 Unicode 字符，而字节级 BPE 直接操作原始字节（0-255），基础词表恰好 256 个，理论上可处理任何语言或编码，永远不会出现 [UNK] token。这就是为什么 GPT 系列模型能处理代码、emoji、多语言混合文本而不会"卡住"。

- GPT-2: 50,257 tokens
- GPT-3.5/GPT-4: ~100,256 tokens (cl100k_base encoding)
- GPT-4o: 200,019 tokens (o200k_base encoding)

### WordPiece (BERT)

WordPiece looks similar to BPE but picks merges differently. Instead of raw frequency, it maximizes the likelihood of the training data:

> WordPiece 看起来与 BPE 类似，但选择合并的方式不同。它不使用原始频率，而是最大化训练数据的似然：

```
BPE merge criterion:      count(A, B)
WordPiece merge criterion: count(AB) / (count(A) * count(B))
```

BPE asks: "Which pair appears most often?" WordPiece asks: "Which pair appears together more often than you would expect by chance?" This subtle difference produces different vocabularies. WordPiece favors merges where co-occurrence is surprising, not just frequent.

> BPE 问："哪对出现最频繁？"WordPiece 问："哪对一起出现的频率超出随机预期？"这个微妙差异产生不同的词表。WordPiece 偏好共现令人惊讶的合并，而非仅仅频繁的。

WordPiece also uses a "##" prefix for continuation subwords:

> WordPiece 还使用 "##" 前缀标记续接子词：

```
"unhappiness" -> ["un", "##happi", "##ness"]
"embedding"   -> ["em", "##bed", "##ding"]
```

The "##" prefix tells you this piece continues a previous token. BERT uses WordPiece with a vocabulary of 30,522 tokens. Every BERT variant -- DistilBERT, RoBERTa's tokenizer is actually BPE, but BERT itself is WordPiece.

> "##" 前缀告诉你这个片段续接前一个 token。BERT 使用 WordPiece，词表为 30,522 个 token。每个 BERT 变体——DistilBERT，RoBERTa 的分词器实际上是 BPE，但 BERT 本身是 WordPiece。

### SentencePiece (Llama, T5)

SentencePiece treats the input as a raw stream of Unicode characters, including whitespace. No pre-tokenization step. No language-specific rules about word boundaries. This makes it genuinely language-agnostic -- it works on Chinese, Japanese, Thai, and other languages where spaces do not separate words.

> SentencePiece 将输入视为原始 Unicode 字符流，包括空格。没有预分词步骤。没有关于词边界的特定语言规则。这使它真正做到了语言无关——它适用于中文、日文、泰文和其他不以空格分隔词语的语言。

SentencePiece supports two algorithms:

> SentencePiece 支持两种算法：

- **BPE mode**: same merge logic as standard BPE, applied to raw character sequences
  中文翻译：**BPE 模式**：与标准 BPE 相同的合并逻辑，应用于原始字符序列
- **Unigram mode**: starts with a large vocabulary and iteratively removes tokens that least affect the overall likelihood. The reverse of BPE -- prune instead of merge.
  中文翻译：**Unigram 模式**：从大词表开始，迭代移除对整体似然影响最小的 token。与 BPE 相反——剪枝而非合并。

Llama 2 uses SentencePiece BPE with a vocabulary of 32,000 tokens. T5 uses SentencePiece Unigram with 32,000 tokens. Note: Llama 3 switched to a tiktoken-based byte-level BPE tokenizer with 128,256 tokens.

> Llama 2 使用 SentencePiece BPE，词表为 32,000 个 token。T5 使用 SentencePiece Unigram，词表为 32,000 个 token。注意：Llama 3 切换到了基于 tiktoken 的字节级 BPE 分词器，词表为 128,256 个 token。

> **【中文解读】** SentencePiece 的独特之处在于它把输入当作原始 Unicode 字符流（包括空格），不做任何语言的预分词。这让它在中文、日文、泰文等不使用空格分隔词语的语言上表现优秀。它支持两种算法：BPE 模式（自底向上合并）和 Unigram 模式（自顶向下剪枝）。Llama 2 用 SentencePiece BPE（32K 词表），而 Llama 3 切换到了 tiktoken 风格的字节级 BPE（128K 词表）。

> **【拓展：SentencePiece 在开源模型中的地位】** Google T5（110亿参数）、Llama 2（7B-70B）、Mistral 7B 等开源模型都使用 SentencePiece。它的优势在于语言无关性——同一个分词器可以处理 100+ 种语言而不需要任何语言特定的预处理规则。Unigram 模式还有一个独特优势：它能输出多个分词候选及其概率，用于鲁棒的模型训练。

### Vocabulary Size Tradeoffs

This is a real engineering decision with measurable consequences.

> 这是一个有可衡量后果的真实工程决策。

```mermaid
graph LR
    subgraph Small["Small Vocab (32K)\ne.g., BERT, T5"]
        S1["More tokens per text"]
        S2["Longer sequences"]
        S3["Smaller embedding matrix"]
        S4["Better rare-word handling"]
    end
    subgraph Large["Large Vocab (128K+)\ne.g., Llama 3, GPT-4o"]
        L1["Fewer tokens per text"]
        L2["Shorter sequences"]
        L3["Larger embedding matrix"]
        L4["Faster inference"]
    end
```

Concrete numbers. For a 128K vocabulary with 4,096-dimensional embeddings, the embedding matrix alone is 128,000 x 4,096 = 524 million parameters. For a 32K vocabulary, it is 131 million parameters. That is a 400M parameter difference from the tokenizer choice alone.

> 具体数字。对于 128K 词表和 4,096 维嵌入，仅嵌入矩阵就有 128,000 x 4,096 = 5.24 亿个参数。对于 32K 词表，则是 1.31 亿个参数。仅分词器选择就带来了 4 亿参数的差异。

But larger vocabularies compress text more aggressively. The same English paragraph that takes 100 tokens with a 32K vocabulary might take 70 tokens with a 128K vocabulary. That means 30% fewer forward passes during generation. For a model serving millions of requests, that is a direct reduction in compute cost.

> 但更大的词表更积极地压缩文本。同一段英文段落用 32K 词表可能需要 100 个 token，用 128K 词表可能只需 70 个 token。这意味着生成时减少 30% 的前向传播。对于服务数百万请求的模型，这是计算成本的直接降低。

The trend is clear: vocabulary sizes are growing. GPT-2 used 50,257. GPT-4 uses ~100K. Llama 3 uses 128K. GPT-4o uses 200K.

> 趋势很明确：词表大小在增长。GPT-2 用 50,257。GPT-4 用约 100K。Llama 3 用 128K。GPT-4o 用 200K。

| Model | Vocab Size | Tokenizer Type | Avg Tokens per English Word |
|-------|-----------|----------------|---------------------------|
| BERT | 30,522 | WordPiece | ~1.4 |
| GPT-2 | 50,257 | Byte-level BPE | ~1.3 |
| Llama 2 | 32,000 | SentencePiece BPE | ~1.4 |
| GPT-4 | ~100,256 | Byte-level BPE | ~1.2 |
| Llama 3 | 128,256 | Byte-level BPE (tiktoken) | ~1.1 |
| GPT-4o | 200,019 | Byte-level BPE | ~1.0 |

### The Multilingual Tax

Tokenizers trained primarily on English are brutal to other languages. Korean text in GPT-2's tokenizer averages 2-3 tokens per word. Chinese can be worse. This means a Korean user effectively has a context window that is half the size of an English user's -- paying the same price for less information density.

> 主要在英文上训练的分词器对其他语言很残酷。韩文在 GPT-2 分词器中平均每词 2-3 个 token。中文可能更糟。这意味着韩文用户的有效上下文窗口只有英文用户的一半——付同样的价格，信息密度却更低。

This is why Llama 3 quadrupled its vocabulary from 32K to 128K. More tokens dedicated to non-English scripts means fairer compression across languages.

> 这就是为什么 Llama 3 将词表从 32K 扩大到 128K。为非英语文字分配更多 token 意味着跨语言的更公平压缩。

> **【中文解读】** 多语言税（Multilingual Tax）是分词器设计中最容易被忽略的公平性问题。以 GPT-2 分词器为例，韩文平均每个词需要 2-3 个 token，中文可能更糟。这意味着韩文/中文用户的有效上下文窗口只有英文用户的一半——付同样的价格，获得的信息密度却更低。Llama 3 将词表从 32K 扩展到 128K，正是为了给非英语文字分配更多 token，实现跨语言的公平压缩。

> **【拓展：多语言分词的实际影响】** 在 GPT-3.5 的 cl100k_base 分词器中，一段 1000 字的中文大约需要 ~1500 tokens，而等量英文信息可能只需 ~500 tokens。这意味着中文用户的 API 成本是英文用户的 3 倍。Llama 3 的 128K 词表将中文的 token 效率提升了约 2 倍，但与英文相比仍有差距。这也是为什么国产模型（如 Qwen、DeepSeek）专门针对中文优化了分词器。

## Build It | 动手实现

### Step 1: Character-Level Tokenizer

Start at the foundation. A character-level tokenizer maps each character to its Unicode code point. No training needed. No unknown tokens. Just a direct mapping.

> 从基础开始。字符级分词器将每个字符映射到其 Unicode 码点。无需训练。无未知 token。只是直接映射。

```python
class CharTokenizer:
    def encode(self, text):
        return [ord(c) for c in text]

    def decode(self, tokens):
        return "".join(chr(t) for t in tokens)
```

"hello" becomes [104, 101, 108, 108, 111]. Every character is its own token. This is the baseline we improve on.

> "hello" 变成 [104, 101, 108, 108, 111]。每个字符是自己的 token。这是我们要改进的基线。

### Step 2: BPE Tokenizer from Scratch

The real implementation. We train on raw bytes (like GPT-2), count pairs, merge the most frequent, and record every merge in order. The merge table is the tokenizer.

> 真正的实现。我们在原始字节上训练（如 GPT-2），统计对频，合并最高频的，并按顺序记录每次合并。合并表就是分词器。

```python
from collections import Counter

class BPETokenizer:
    def __init__(self):
        self.merges = {}
        self.vocab = {}

    def _get_pairs(self, tokens):
        pairs = Counter()
        for i in range(len(tokens) - 1):
            pairs[(tokens[i], tokens[i + 1])] += 1
        return pairs

    def _merge_pair(self, tokens, pair, new_token):
        merged = []
        i = 0
        while i < len(tokens):
            if i < len(tokens) - 1 and tokens[i] == pair[0] and tokens[i + 1] == pair[1]:
                merged.append(new_token)
                i += 2
            else:
                merged.append(tokens[i])
                i += 1
        return merged

    def train(self, text, num_merges):
        tokens = list(text.encode("utf-8"))
        self.vocab = {i: bytes([i]) for i in range(256)}

        for i in range(num_merges):
            pairs = self._get_pairs(tokens)
            if not pairs:
                break
            best_pair = max(pairs, key=pairs.get)
            new_token = 256 + i
            tokens = self._merge_pair(tokens, best_pair, new_token)
            self.merges[best_pair] = new_token
            self.vocab[new_token] = self.vocab[best_pair[0]] + self.vocab[best_pair[1]]

        return self

    def encode(self, text):
        tokens = list(text.encode("utf-8"))
        for pair, new_token in self.merges.items():
            tokens = self._merge_pair(tokens, pair, new_token)
        return tokens

    def decode(self, tokens):
        byte_sequence = b"".join(self.vocab[t] for t in tokens)
        return byte_sequence.decode("utf-8", errors="replace")
```

The training loop is the core of BPE: count pairs, merge the winner, repeat. Each merge reduces the total token count. After `num_merges` rounds, the vocabulary grows from 256 (base bytes) to 256 + num_merges.

> 训练循环是 BPE 的核心：统计对频，合并胜者，重复。每次合并减少总 token 数。经过 `num_merges` 轮后，词表从 256（基础字节）增长到 256 + num_merges。

Encoding applies merges in the exact order they were learned. This matters. If merge 1 created "th" and merge 5 created "the", encoding must apply merge 1 first so that "the" can form from "th" + "e" in merge 5.

> 编码按学习的确切顺序应用合并。这很重要。如果合并 1 创建了 "th"，合并 5 创建了 "the"，编码必须先应用合并 1，这样 "the" 才能在合并 5 中由 "th" + "e" 形成。

Decoding is the inverse: look up each token ID in the vocabulary, concatenate the bytes, decode to UTF-8.

> 解码是逆过程：在词表中查找每个 token ID，拼接字节，解码为 UTF-8。

### Step 3: Encode and Decode Roundtrip

```python
corpus = (
    "The cat sat on the mat. The cat ate the rat. "
    "The dog sat on the log. The dog ate the frog. "
    "Natural language processing is the study of how computers "
    "understand and generate human language. "
    "Tokenization is the first step in any NLP pipeline."
)

tokenizer = BPETokenizer()
tokenizer.train(corpus, num_merges=40)

test_sentences = [
    "The cat sat on the mat.",
    "Natural language processing",
    "tokenization pipeline",
    "unhappiness",
]

for sentence in test_sentences:
    encoded = tokenizer.encode(sentence)
    decoded = tokenizer.decode(encoded)
    raw_bytes = len(sentence.encode("utf-8"))
    ratio = len(encoded) / raw_bytes
    print(f"'{sentence}'")
    print(f"  Tokens: {len(encoded)} (from {raw_bytes} bytes) -- ratio: {ratio:.2f}")
    print(f"  Roundtrip: {'PASS' if decoded == sentence else 'FAIL'}")
```

The compression ratio tells you how effective the tokenizer is. A ratio of 0.50 means the tokenizer compressed the text to half as many tokens as raw bytes. Lower is better. On the training corpus, the ratio will be good. On out-of-distribution text like "unhappiness" (which does not appear in the corpus), the ratio will be worse -- the tokenizer falls back to character-level encoding for unseen patterns.

> 压缩比告诉你分词器的效率。比率 0.50 意味着分词器将文本压缩为原始字节数的一半。越低越好。在训练语料上，比率会很好。在分布外文本如 "unhappiness"（不出现在语料中）上，比率会更差——分词器对未见模式退回到字符级编码。

### Step 4: Compare with tiktoken

```python
import tiktoken

enc = tiktoken.get_encoding("cl100k_base")

texts = [
    "The cat sat on the mat.",
    "unhappiness",
    "Hello, world!",
    "def fibonacci(n): return n if n < 2 else fibonacci(n-1) + fibonacci(n-2)",
    "Geschwindigkeitsbegrenzung",
]

for text in texts:
    our_tokens = tokenizer.encode(text)
    tiktoken_tokens = enc.encode(text)
    tiktoken_pieces = [enc.decode([t]) for t in tiktoken_tokens]
    print(f"'{text}'")
    print(f"  Our BPE:   {len(our_tokens)} tokens")
    print(f"  tiktoken:  {len(tiktoken_tokens)} tokens -> {tiktoken_pieces}")
```

tiktoken uses the exact same algorithm but trained on hundreds of gigabytes of text with 100,000 merges. The algorithm is identical. The difference is the training data and the number of merges. Your tokenizer trained on a paragraph with 40 merges cannot compete with tiktoken's 100K merges on a massive corpus. But the mechanism is the same.

> tiktoken 使用完全相同的算法，但在数百 GB 文本上训练了 100,000 次合并。算法完全一样。区别在于训练数据和合并次数。你在一段文本上训练 40 次合并的分词器无法与 tiktoken 在大规模语料上的 100K 次合并竞争。但机制是相同的。

### Step 5: Vocabulary Analysis

```python
def analyze_vocabulary(tokenizer, test_texts):
    total_tokens = 0
    total_chars = 0
    token_usage = Counter()

    for text in test_texts:
        encoded = tokenizer.encode(text)
        total_tokens += len(encoded)
        total_chars += len(text)
        for t in encoded:
            token_usage[t] += 1

    print(f"Vocabulary size: {len(tokenizer.vocab)}")
    print(f"Total tokens across all texts: {total_tokens}")
    print(f"Total characters: {total_chars}")
    print(f"Avg tokens per character: {total_tokens / total_chars:.2f}")

    print(f"\nMost used tokens:")
    for token_id, count in token_usage.most_common(10):
        token_bytes = tokenizer.vocab[token_id]
        display = token_bytes.decode("utf-8", errors="replace")
        print(f"  Token {token_id:4d}: '{display}' (used {count} times)")

    unused = [t for t in tokenizer.vocab if t not in token_usage]
    print(f"\nUnused tokens: {len(unused)} out of {len(tokenizer.vocab)}")
```

This reveals the Zipf distribution in your vocabulary. A few tokens dominate (spaces, "the", "e"). Most tokens are rarely used. Production tokenizers optimize for this distribution -- common patterns get short token IDs, rare patterns get longer representations.

> **【中文解读】** 词表分析揭示了 Zipf 分布规律：少数 token 占据了绝大部分使用量（如空格、"the"、"e"），大多数 token 很少被使用。生产级分词器针对这个分布进行优化——常见模式获得短 token ID，罕见模式使用更长的表示。这也是为什么词表大小是工程权衡而非越大越好。

> **【拓展：生产环境的词表优化】** GPT-4o 的 o200k_base 词表有 200,019 个 token，但最常用的 1000 个 token 覆盖了日常英文文本约 80% 的出现频率。在部署 LLM 时，embedding 矩阵的大小直接由词表决定：128K 词表 x 4096 维 = 5.24 亿参数，仅嵌入层就占用了约 2GB 显存（FP16）。

## Use It | 用框架实现

Your scratch BPE works. Now see what production tools look like.

> 你的 BPE 实现可以工作了。现在看看生产工具是什么样的。

### tiktoken (OpenAI)

```python
import tiktoken

enc = tiktoken.get_encoding("cl100k_base")

text = "Tokenizers convert text to integers"
tokens = enc.encode(text)
print(f"Tokens: {tokens}")
print(f"Pieces: {[enc.decode([t]) for t in tokens]}")
print(f"Roundtrip: {enc.decode(tokens)}")
```

tiktoken is written in Rust with Python bindings. It encodes millions of tokens per second. Same BPE algorithm, industrial-strength implementation.

> tiktoken 用 Rust 编写并提供 Python 绑定。每秒编码数百万 token。同样的 BPE 算法，工业级实现。

### Hugging Face tokenizers

```python
from tokenizers import Tokenizer
from tokenizers.models import BPE
from tokenizers.trainers import BpeTrainer
from tokenizers.pre_tokenizers import ByteLevel

tokenizer = Tokenizer(BPE())
tokenizer.pre_tokenizer = ByteLevel()

trainer = BpeTrainer(vocab_size=1000, special_tokens=["<pad>", "<eos>", "<unk>"])
tokenizer.train(["corpus.txt"], trainer)

output = tokenizer.encode("The cat sat on the mat.")
print(f"Tokens: {output.tokens}")
print(f"IDs: {output.ids}")
```

The Hugging Face tokenizers library is also Rust under the hood. It trains BPE on gigabyte-scale corpora in seconds. This is what you use when training your own model.

> Hugging Face tokenizers 库底层也是 Rust。它能在几秒内在 GB 级语料上训练 BPE。这是你训练自己的模型时使用的工具。

### Loading Llama's Tokenizer

```python
from transformers import AutoTokenizer

tokenizer = AutoTokenizer.from_pretrained("meta-llama/Llama-3.1-8B")

text = "Tokenizers are the unsung heroes of LLMs"
tokens = tokenizer.encode(text)
print(f"Token IDs: {tokens}")
print(f"Tokens: {tokenizer.convert_ids_to_tokens(tokens)}")
print(f"Vocab size: {tokenizer.vocab_size}")

multilingual = ["Hello world", "Hola mundo", "Bonjour le monde"]
for text in multilingual:
    ids = tokenizer.encode(text)
    print(f"'{text}' -> {len(ids)} tokens")
```

Llama 3's 128K vocabulary compresses non-English text significantly better than GPT-2's 50K vocabulary. You can verify this yourself -- encode the same sentence in multiple languages and count the tokens.

> Llama 3 的 128K 词表压缩非英文文本比 GPT-2 的 50K 词表好得多。你可以自己验证——用多种语言编码同一个句子并计算 token 数。

## Ship It | 产出物

This lesson produces `outputs/prompt-tokenizer-analyzer.md` -- a reusable prompt that analyzes tokenization efficiency for any text and model combination. Feed it a text sample and it tells you which model's tokenizer handles it best.

> 本课产出 `outputs/prompt-tokenizer-analyzer.md`——一个可复用的 prompt，分析任意文本和模型组合的分词效率。输入文本样本，它会告诉你哪个模型的分词器处理得最好。

## Exercises | 练习题

1. Modify the BPE tokenizer to print the vocabulary at each merge step. Watch how "t" + "h" becomes "th", then "th" + "e" becomes "the". Track how common English words get assembled piece by piece.
   中文翻译：修改 BPE 分词器，在每次合并步骤打印词表。观察 "t" + "h" 如何变成 "th"，然后 "th" + "e" 如何变成 "the"。追踪常见英文词汇如何被逐步组装。

2. Add special tokens (`<pad>`, `<eos>`, `<unk>`) to the BPE tokenizer. Assign them IDs 0, 1, 2 and shift all other tokens accordingly. Implement a pre-tokenization step that splits on whitespace before running BPE.
   中文翻译：向 BPE 分词器添加特殊 token（`<pad>`、`<eos>`、`<unk>`）。分配 ID 0、1、2 并相应移动其他 token。实现一个在运行 BPE 前按空格拆分的预分词步骤。

3. Implement the WordPiece merge criterion (likelihood ratio instead of frequency). Train both BPE and WordPiece on the same corpus with the same number of merges. Compare the resulting vocabularies -- which one produces more linguistically meaningful subwords?
   中文翻译：实现 WordPiece 合并标准（似然比替代频率）。在相同语料上用相同合并次数训练 BPE 和 WordPiece。比较生成的词表——哪个产生更有语言学意义的子词？

4. Build a multilingual tokenizer efficiency benchmark. Take 10 sentences in English, Spanish, Chinese, Korean, and Arabic. Tokenize each with tiktoken (cl100k_base) and measure the average tokens per character. Quantify the "multilingual tax" for each language.
   中文翻译：构建多语言分词效率基准。取英文、西班牙文、中文、韩文和阿拉伯文各 10 个句子。用 tiktoken（cl100k_base）分词并测量每字符平均 token 数。量化每种语言的"多语言税"。

5. Train your BPE tokenizer on a larger corpus (download a Wikipedia article). Tune the number of merges to achieve a compression ratio within 10% of tiktoken on that same text. This forces you to understand the relationship between corpus size, merge count, and compression quality.
   中文翻译：在更大的语料上训练 BPE 分词器（下载一篇维基百科文章）。调整合并次数使压缩比在相同文本上与 tiktoken 相差不超过 10%。这迫使你理解语料大小、合并次数和压缩质量之间的关系。

## Key Terms | 术语速查表

| Term | What people say | What it actually means | 中文释义 |
|------|----------------|----------------------|---------|
| Token | "A word" | A unit in the model's vocabulary -- could be a character, subword, word, or multi-word chunk | 词元，模型词表中的基本单元 |
| BPE | "Some compression thing" | Byte Pair Encoding -- iteratively merge the most frequent adjacent pair of tokens until the target vocabulary size is reached | 字节对编码，贪心合并最高频相邻对 |
| WordPiece | "BERT's tokenizer" | Like BPE but merges maximize the likelihood ratio count(AB)/(count(A)*count(B)) instead of raw frequency | 基于似然比的子词分词，BERT 使用 |
| SentencePiece | "A tokenizer library" | A language-agnostic tokenizer that operates on raw Unicode without pre-tokenization, supporting BPE and Unigram algorithms | 语言无关的分词库，支持 BPE/Unigram |
| Vocabulary size | "How many words it knows" | The total number of unique tokens: GPT-2 has 50,257, BERT has 30,522, Llama 3 has 128,256 | 词表大小，直接影响嵌入矩阵参数量 |
| Fertility | "Not a tokenizer term" | Average number of tokens per word -- measures tokenizer efficiency across languages (1.0 is perfect, 3.0 means the model works three times harder) | 生育率，每词平均 token 数，衡量分词效率 |
| Byte-level BPE | "GPT's tokenizer" | BPE operating on raw bytes (0-255) instead of Unicode characters, guaranteeing no unknown tokens for any input | 字节级 BPE，基础词表恰好 256 个字节 |
| Merge table | "The tokenizer file" | Ordered list of pair merges learned during training -- this IS the tokenizer, and order matters | 合并表，训练学到的有序合并规则 |
| Pre-tokenization | "Splitting on spaces" | Rules applied before subword tokenization: whitespace splitting, digit separation, punctuation handling | 预分词，子词分词前的规则化拆分 |
| Compression ratio | "How efficient the tokenizer is" | Tokens produced divided by input bytes -- lower means better compression and faster inference | 压缩比，token 数/输入字节数，越低越好 |

## Further Reading | 延伸阅读

- [Sennrich et al., 2016 -- "Neural Machine Translation of Rare Words with Subword Units"](https://arxiv.org/abs/1508.07909) -- the paper that introduced BPE for NLP, turning a 1994 compression algorithm into the foundation of modern tokenization
- [Kudo & Richardson, 2018 -- "SentencePiece: A simple and language independent subword tokenizer"](https://arxiv.org/abs/1808.06226) -- language-agnostic tokenization that made multilingual models practical
- [OpenAI tiktoken repository](https://github.com/openai/tiktoken) -- production BPE implementation in Rust with Python bindings, used by GPT-3.5/4/4o
- [Hugging Face Tokenizers documentation](https://huggingface.co/docs/tokenizers) -- production-grade tokenizer training with Rust performance
