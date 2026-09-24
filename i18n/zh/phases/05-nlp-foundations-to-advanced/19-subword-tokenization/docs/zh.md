# 字符标签  BPE,WordPiece,单字体,句子片子

> 字符符符符符符符符符符符符符符符符符符符符符符符符符符符符符符符符符符符符符符符符符符符符符符符符符符符符符符符符符符符符符符符符符符符符符符符符符符符符符符符符符符符符符符符符符符符符符符符符符符符符符符符符符符符符符符符符符符符符符符符符符符符符符符符符符符符符符符符符符符符符符符符符符符符符符符符符符符符符符符符符符符符符符符符符符符符符符符符符符符符符符符符符符符符符符符符符符符符符符符符符符符符符符符符符符符符符符符符符符符符符符符符符符符符符符符符符符符符符符符符符符符符符符符符符符符符符符符符符符符符符符符符符符符符符符符符符符符符符符符符符符符符符符符符符符符符符符符符符符符符符符符符符符符符符符符符符符符符符符符符符符符符符符符符符符符符符符符符符符符符符符符符符符符符符符符符符符符符符符符符符符符符符符符符符符符符符符符符符符符符符符符符符符符符符符符符符符符符符符符符符符符符符符符符符符符符符符符符符符符符符符符符符符符符符符符符符符符符符符符符符符符符符符符符符符符符符符符符符符符符符符符符符符符符符符符符符符符符符符符符符符符符符符符符符符符符符符符符符符符符符符符符符符符符符
> 词级分词器在未见词上卡住──字符分词器爆炸序列长度──子词分词器取中值──每现代的LLM都用子词分词──

> **【中文解读】**字块是BERT 用的.

**Type:** Learn | **类型:** 学习
**Languages:** Python | **语言:** Python
**Prerequisites:** Phase 5 · 01 (Text Processing), Phase 5 · 04 (GloVe / FastText / Subword) | **前置知识:** Phase 5 · 01（文本处理），Phase 5 · 04（GloVe / FastText / 子词）
**Time:** ~60 minutes | **时间:** ~60 分钟

## 问题 问题引入

你的词汇有5万个词.一个用户输入"不可代码化".你的代码化器返回.`[UNK]`现在模型没有任何信号,更糟糕的是,您的文件中90个百分比的文件包含40个罕见的词,这意味着每文件中丢掉的信息是40个.

> 你的词表有5万个词.用户输入"不可认可".`[UNK]`模型现在对这个词没有信号. 更糟糕的是:语料中第90百分位文档有40个罕见词,这意味着每个文档丢失了40个信息.

> **【中文解读】**本节提出的问题是:如何在实际工程中正确理解和应用这一技术――理解问题背景有助于把握技术选择的关键决策点――在实际人工智能系统中,错误的技术选择往往比实现细节的错误成本更高――

常见词语保持单个标记.罕见词语分解成有意义的部分:`untokenizable`其他`un`现在`token`现在`izable`训练数据涵盖了一切,因为任何字符串最终都是字节的序列.

> 子词分词解决了这个问题.`untokenizable`其他`un`,我知道.`token`,我知道.`izable`△训练数据覆盖一切,因为任何字符串最终都是字节序列.

2026年每一个跨境LLM都使用三个算法 (BPE,UniGram,WordPiece) 运行,包裹在三个图书馆 (tiktoken,SentencePiece,HF Tokenizers) 中.

> 2026年每一个前沿的LLM都基于三种算法之一 (BPE、Unigram、WordPiece),包装在三种库之一 (Tiktoken、SentencePiece、HF Tokenizers) 中.

## 概念的核心概念

> **【中文解读】**本节介绍核心概念和理论基础.掌握这些概念是后续动手实现的前提,同时也是面试和工程实践中高频考察的知识点.

![BPE vs Unigram vs WordPiece, character-by-character](../assets/subword-tokenization.svg)

**BPE (Byte-Pair Encoding).**开始一个字符级词汇. 计算每一个相邻的对. 融合最频繁的对 into a new token. 重复直到你达到目标词汇尺寸. 主导算法:GPT-2/3/4,Llama,Gemma,Qwen2,Mistral.

> **BPE（字节对编码）。**从字符级词表开始――统计每个相邻对――将最频繁的对合并为新代币――重复直到达到目标词表大小――主导算法:GPT-2/3/4、Llama、Gemma、Qwen2、Mistral――

**Byte-level BPE.**虽然它是无码的,但它是无码的.`[UNK]`代币 任何字节序列编码.GPT-2使用了50,257个代币 (256字节+50,000合并+1个特殊).

> **字节级 BPE。**相同算法但在原始字节 (原始字节) 没有单码字符.`[UNK]`标志  任何字节序列都可编码――GPT-2 使用 50,257个标志――

**Unigram.**开始一个巨大的词汇库. 赋予每个代币一个单数概率. 偶尔切割代币,其删除至少增加了体积日志概率. 推断可能:可以样本代币化. T5, mBART,ALBERT,XLNet,Gemma使用.

> **Unigram。**从巨大的词表开始.给每个符号 分布单格式概率. 代剪枝移除后对语料对数似增加最小的符号. 推理时是概率性的:可采样分词结果. 用于T5、mBART、ALBERT、XLNet、Gemma。

**WordPiece.**结合对,最大化了训练体的可能性,而不是原始频率.

> **WordPiece。**合并使训练语料似然最大化而非原始频率最高对比──用于BERT、DistilBERT、ELECTRA──

**SentencePiece vs tiktoken.**文本Piece是直接在原始的Unicode文本上训练语文库 (BPE或Unigram),编码白色空间为`▁`提克是OpenAI的快速*编码器*对待预先构建的词汇库;它不训练.

> **SentencePiece vs tiktoken。**文文Piece 是原始的 Unicode 文本上*训练*词表的库,将空格编码为 `▁`△tiktoken 是 OpenAI 针对预构建词表的快速编码器;它不训练──

基本规则:

> 经验法则:

- **Training a new vocabulary:**语句Piece (多语言,没有预先代币化) 或HF代币化器.
  **训练新词表：**语句Piece(多语言,无预分词) 或HF标记者──
- **Fast inference against GPT vocab:**投资者:
  **针对 GPT 词表的快速推理：**标签:
- **Both:**一本图书馆,培训+服务.
  **两者兼有：** 一个库,训练+服务.

> **【中文解读】**本节通过代码实现从零到核心算法――这种"从零开始"的方式可以帮助理解框架背后的原理,遇到问题时不会被黑盒困住――
```figure
bpe-merge
```

## 建立它

> **【拓展：大语言模型的工程实践】**从GPT到ChatGPT,NLP领域经历了从"每个任务训练一个模型"到"一个模型解决所有任务"的范式转变. 在实际工程中,LLM的部署需要考虑代币限制,延迟,成本,安全审查等问题.

> **【拓展：RAG 与企业知识库】**检索增强生成 (RAG) 是当前企业人工智能应用中最流行的架构:将用户查询先检索相关文档片段,再将检索结果作为上下文给LLM 生成答案――这种方式解决了LLM 知识过时和幻觉问题――向量数据库――如Milvus、Pinecone、Weaviate) 是RAG系统的核心组件――

> **【拓展：NLP 的多语言挑战】**全球有7000多种语言,但NLP研究主要集中在英语等少数语言.跨语言迁移学习,多语言预训模型 (如 mBERT,XLM-R) 是解决低资源语言NLP的主要方法.

## 建立它,实现它.

> **【中文解读】**本节通过代码实现从零到核心算法――这种"从零开始"的方式可以帮助理解框架背后的原理,遇到问题时不会被黑盒困住――

### 步骤1:从零开始的BPE

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

合并顺序是重要的.BPE在训练顺序中应用合并,因此早期合并会产生更长的代币,从而阻断后来的代币.这就是为什么BPE词汇不适用于不同模型.

> 合并顺序很重要――BPE 按训练顺序应用合并,所以较早的合并创建更长的代币,阻止后续合并――这就是为什么BPE 词表不能跨模型移植――

### 步骤2:使用Tik Token和SentencePiece进行代码化

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

### 步骤3:生育率比较

```python
def fertility(text, tokenizer_fn):
    return len(tokenizer_fn(text))

# BPE on English: ~1.3 tokens/word
# BPE on Hindi: ~3.5 tokens/word
# BPE on Amharic: ~8 tokens/word
```

> **【中文解读】**本节展示了如何使用成熟框架 (如PyTorch、HuggingFace等) 快速应用该技术.

> **【拓展：Prompt Engineering 与 LLM 应用】**快速工程已成为NLP工程师的核心技能. 从零射到少射,从思想链到反应,不同的提示策略适用于不同场景. 在实际项目中,系统提示 (系统提示) 的设计直接影响了LLM应用的稳定性和输出质量.

## 用它实现框架

根据生态系统来选择.

> 按生态系统选择.

- **OpenAI models (GPT-4, GPT-4o):**快速,精确的转载. / tiktoken──快速──精确复现
- **Multilingual / custom training:**训练从原始文本,处理任何书写系统.
- **Hugging Face models:**机器自动包装正确的后端.
- **Maximum speed at inference:**推理最高速度:HF Tokenizers 或 tiktoken──

> **【中文解读】**本节关注如何将模型部署为可用的产品. 从原型到生产级系统需要考虑性能优化,错误处理,监控等多个维度.

## 运送它.

保存如`outputs/prompt-tokenizer-picker.md`其他:

> 保存为`outputs/prompt-tokenizer-picker.md`其他:

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

> **【中文解读】**练习题按照易/中/难 三个难度递进;;建议至少完成中级题,Hard级适合深入研究或面试准备;;

## 练习题

1. **Easy.**训练BPE在一个小的体积上 (1000字). 编码和解码20个测试字. 检查回路忠实性. / **简单。**在小型语料上训练BPE──编码解码 20个测试词──验证往返保真度──
2. **Medium.**使用TikToken的 cl100k_base来比较英语,中国和印度语的代币化生育率. 每个代币的代币报告. / **中等。**使用TikToken比较英语,中文和印地语分词繁殖率――报告每种语言的每个词代币数量――
3. **Hard.**根据相同数据训练的BPE模型,比较生育率. / **困难。**在混合英语-印度语语料上训练 SentencePiece Unigram 模型――与在相同数据上训练的 BPE 模型相比繁殖率――

> **【中文解读】**在团队协作中,统一术语定义可以避免大量沟通误解.

## 关键词 快速查找表

| Term / 术语 | What people say / 人们常说的 | What it actually means / 实际含义 |
|------|-----------------|-----------------------|
| BPE（字节对编码） | GPT's tokenizer / GPT 的分词器 | Iteratively merge most frequent adjacent pairs. / 迭代合并最频繁的相邻对。 |
| Unigram | T5's tokenizer / T5 的分词器 | Prune tokens from large vocabulary by likelihood. / 按似然从大词表剪枝。 |
| WordPiece | BERT's tokenizer / BERT 的分词器 | Merge pairs that maximize corpus likelihood. / 合并使语料似然最大化的对。 |
| SentencePiece | Training library / 训练库 | Train BPE or Unigram on raw text. Encodes whitespace as `▁`. / 在原始文本上训练 BPE 或 Unigram。 |
| tiktoken | OpenAI's encoder / OpenAI 编码器 | Fast encoding against pre-built GPT vocabularies. / 针对预构建 GPT 词表的快速编码。 |
| Fertility（繁殖率） | Tokens per word / 每词 token 数 | How many subword tokens a word produces. Lower is better. / 一个词产生多少子词 token。越低越好。 |

> **【中文解读】**延伸阅读提供了深入学习的高质量资源. 这些论文和教程是该领域的经典参考文献,适合需要深入了解的读者.

## 继续阅读 继续阅读

- [Sennrich et al. (2016). Neural Machine Translation of Rare Words with Subword Units](https://arxiv.org/abs/1508.07909) BPE论文.
- [Kudo (2018). Subword Regularization](https://arxiv.org/abs/1804.10959) 统计论文.
- [SentencePiece documentation](https://github.com/google/sentencepiece)培训和服务. / 培训和服务.
- [tiktoken](https://github.com/openai/tiktoken) 开放AI的快速代币化器.
- [Hugging Face Tokenizers](https://huggingface.co/docs/tokenizers/)   后端训练 + 服务
