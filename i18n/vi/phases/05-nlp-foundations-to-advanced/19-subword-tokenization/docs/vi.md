# Đánh dấu từ phụ  BPE, WordPiece, Unigram, SentencePiece  子词分词  BPE、WordPiece、SentencePiece

> Các mã thông báo từ bị ngạt vào những từ không thể thấy, các mã thông báo ký tự làm tăng chiều dài chuỗi, các mã thông báo từ dưới chia khác biệt, mỗi chương trình đại học hiện đại đều được chuyển sang một.
> 词级分词器在未见词上卡住──字符分词器爆炸序列长度──子词分词器取中值──每个现代 LLM 都用子词分词──

> **【中文解读】**BPE là GPT dùng của phân từ thuật toán, WordPiece là BERT dùng của.

**Type:** Learn | **类型:** 学习
**Languages:** Python | **语言:** Python
**Prerequisites:** Phase 5 · 01 (Text Processing), Phase 5 · 04 (GloVe / FastText / Subword) | **前置知识:** Phase 5 · 01（文本处理），Phase 5 · 04（GloVe / FastText / 子词）
**Time:** ~60 minutes | **时间:** ~60 分钟

## Vấn đề  vấn đề giới thiệu

Từ vựng của bạn có 50.000 từ. Người dùng gõ "không thể nhận dạng".`[UNK]`Mô hình hiện không có tín hiệu về từ. Tệ hơn: tài liệu phần trăm 90 trong cơ quan của bạn có 40 từ hiếm, nghĩa là 40 bit thông tin bị bỏ rơi cho mỗi tài liệu.

> Bạn của từ表 có 50.000 个词. Người dùng nhập "không thể nhận ra".`[UNK]`◊ Mô hình hiện nay không có tín hiệu đối với từ này.

> **【中文解读】**Câu hỏi được đặt ra trong phần này là: làm thế nào để hiểu và áp dụng đúng công nghệ này trong công trình thực tế.

Các từ chung vẫn là các token đơn lẻ.`untokenizable`→ `un`- `token`- `izable`Dữ liệu đào tạo bao gồm tất cả bởi vì bất kỳ chuỗi nào là một chuỗi của các byte.

> 子词分词 giải quyết vấn đề này.`untokenizable`→ `un``token``izable`❖ tập dữ liệu bao gồm tất cả, vì bất kỳ chữ cái nào cuối cùng là chuỗi chữ cái.

Mỗi LLM biên giới vào năm 2026 được gửi trên một trong ba thuật toán (BPE, Unigram, WordPiece), được gói trong một trong ba thư viện (tiktoken, SentencePiece, HF Tokenizers). Bạn không thể gửi một mô hình ngôn ngữ mà không chọn một.

> Mỗi năm 2026 LLM trên đường lối tiên tiến đều dựa trên một trong ba thuật toán (BPE, Unigram, WordPiece), bao gồm trong ba bộ sưu tập (tiktoken, SentencePiece, HF Tokenizers).

## Khái niệm cốt lõi

> **【中文解读】**Bài viết này giới thiệu các khái niệm và lý thuyết cốt lõi.

![BPE vs Unigram vs WordPiece, character-by-character](../assets/subword-tokenization.svg)

**BPE (Byte-Pair Encoding).**Bắt đầu với một từ vựng ở cấp độ ký tự. Đếm từng cặp lân cận. Thôi cặp thường xuyên nhất vào một mã thông báo mới. Lặp lại cho đến khi bạn đạt đến kích thước từ vựng mục tiêu.

> **BPE（字节对编码）。**Từ字符级词表开始──统计每个相邻对──将最频繁的对合并为新代币──重复直到达到目标词表大小──主导算法:GPT-2/3/4、Llama、Gemma、Qwen2、Mistral──

**Byte-level BPE.**Cùng thuật toán nhưng trên các byte thô (256 mã thông báo cơ sở) thay vì các ký tự Unicode.`[UNK]`token  bất kỳ mã hóa chuỗi byte nào. GPT-2 sử dụng 50.257 token (256 byte + 50.000 hợp nhất + 1 đặc biệt).

> **字节级 BPE。**tương tự như các thuật toán nhưng trong phần nguyên bản (256 个基础 token) thay vì Unicode 字符上──保证零 `[UNK]`token  任何字节序列都可编码──GPT-2 使用 50,257 个 token──

**Unigram.**Bắt đầu với một từ vựng khổng lồ. Đề xuất cho mỗi token một xác suất unigram. Thử cắt đứt một cách lặp đi lặp lại các token mà việc loại bỏ ít nhất làm tăng xác suất ghi chép corpus.

> **Unigram。**Từ biểu tượng từ khổng lồ bắt đầu. Để mỗi token phân chia các biểu tượng 概率.

**WordPiece.**Các cặp hợp nhất để tối đa hóa khả năng tập hợp tập thể thay vì tần số nguyên liệu.

> **WordPiece。**合并使训练语料似然最大化而非原始频率最高对――用于BERT、DistilBERT、ELECTRA。

**SentencePiece vs tiktoken.**SentencePiece là thư viện * đào tạo * từ vựng (BPE hoặc Unigram) trực tiếp trên văn bản Unicode thô, mã hóa không gian trắng như `▁`. tiktoken là mã hóa nhanh * của OpenAI chống lại từ vựng được xây dựng sẵn; nó không đào tạo.

> **SentencePiece vs tiktoken。**SentencePiece là trong bộ bưu trữ từ ngữ của Unicode nguyên thủy, sẽ được mã hóa bởi`▁` tiktoken là OpenAI 针对预构建词表的快速*编码器*; nó không được đào tạo。

Quy tắc:

> 经验法则:

- **Training a new vocabulary:**SentencePiece (hiện ngữ đa ngôn ngữ, không có pre-tokenization) hoặc HF Tokenizers.
  **训练新词表：**CâuPiece(多语言,无预分词) hoặc HF Tokenizers。
- **Fast inference against GPT vocab:**tiktoken (cl100k_base, o200k_base).
  **针对 GPT 词表的快速推理：**Tiktoken.
- **Both:**HF Tokenizers  một thư viện, đào tạo + phục vụ.
  **两者兼有：**HF Tokenizers  一个库,训练 + 服务。

> **【中文解读】**本节通过代码实现核心算法从零――这种" từ đầu"的方式能帮助理解框架背后的原理,遇到问题时不会被黑盒困住――
```figure
bpe-merge
```

## Hãy xây dựng nó

> **【拓展：大语言模型的工程实践】**Từ GPT đến ChatGPT, NLP đã trải qua sự chuyển đổi từ "mỗi nhiệm vụ đào tạo một mô hình" đến "một mô hình giải quyết tất cả các nhiệm vụ". Trong công trình thực tế, việc triển khai LLM cần phải xem xét các vấn đề như: giới hạn token, trì hoãn, chi phí, kiểm tra an toàn, và các vấn đề khác.

> **【拓展：RAG 与企业知识库】**检索增强生成(RAG) là cấu trúc phổ biến nhất trong ứng dụng AI của doanh nghiệp hiện tại: sẽ truy vấn người dùng trước tiên truy vấn các đoạn tài liệu liên quan, tiếp tục truy vấn kết quả như trên dưới đây cho LLM 生成答案──

> **【拓展：NLP 的多语言挑战】**Trên toàn cầu có hơn 7000 ngôn ngữ, nhưng nghiên cứu về NLP tập trung chủ yếu vào tiếng Anh và một số ít ngôn ngữ.

## Hãy xây dựng nó.

> **【中文解读】**本节通过代码实现核心算法从零――这种" từ đầu"的方式能帮助理解框架背后的原理,遇到问题时不会被黑盒困住――

### Bước 1: BPE từ đầu

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

Các thứ tự hợp nhất là quan trọng. BPE áp dụng các hợp nhất trong thứ tự đào tạo, vì vậy các hợp nhất trước tạo ra các token dài hơn ngăn chặn các thứ tự sau đó.

> 合并顺序 rất quan trọng. BPE 按训练顺序应用合并, do đó, sooner of 合并创建更长的代币,阻止后续合并.

### Bước 2: token hóa với tiktoken và SentencePiece

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

### Bước 3: So sánh khả năng sinh sản

```python
def fertility(text, tokenizer_fn):
    return len(tokenizer_fn(text))

# BPE on English: ~1.3 tokens/word
# BPE on Hindi: ~3.5 tokens/word
# BPE on Amharic: ~8 tokens/word
```

> **【中文解读】**Bài này sẽ trình bày cách sử dụng một khung đã phát triển như PyTorch, HuggingFace, và các khác.

> **【拓展：Prompt Engineering 与 LLM 应用】**Kỹ thuật nhanh chóng đã trở thành kỹ năng cốt lõi của các kỹ sư NLP. Từ Zero-shot đến Few-shot, từ Chain-of-Thought đến ReAct, các chiến lược khác nhau áp dụng cho các tình huống khác nhau. Trong các dự án thực tế, thiết kế của System提示(System Prompt) ảnh hưởng trực tiếp đến sự ổn định và chất lượng sản xuất của ứng dụng LLM.

## Hãy sử dụng nó để thực hiện

Chọn theo hệ sinh thái.

> 按生态系统选择──

- **OpenAI models (GPT-4, GPT-4o):**tiktoken. nhanh chóng, tái tạo chính xác của OpenAI của tokenization. / tiktoken。快速、精确复现 OpenAI 分词。
- **Multilingual / custom training:**SentencePiece. Trèn từ văn bản thô, xử lý bất kỳ kịch bản nào.
- **Hugging Face models:**AutoTokenizer. tự động lật lại phần sau bên phải. / AutoTokenizer.
- **Maximum speed at inference:**HF Tokenizers (Rust backend) hoặc tiktoken (Python + C). / 推理最高速度:HF Tokenizers 或 tiktoken。

> **【中文解读】**Phần này tập trung vào cách phân phối mô hình như một sản phẩm có thể sử dụng.

## Chuyển nó đi.

Cứ như `outputs/prompt-tokenizer-picker.md`- Có thể là:

> 保存为 `outputs/prompt-tokenizer-picker.md`- Có thể là:

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

> **【中文解读】**练题按照 Easy/Medium/Hard 三个难度递进;;建议至少完成 级别的题目, 级别适合深入研究或面试准备;;

## Tập luyện bài tập

1. **Easy.**Đào tạo BPE trên một bộ phận nhỏ (1000 từ). mã hóa và giải mã 20 từ thử nghiệm.**简单。**Trong các ngôn ngữ nhỏ tập BPE. 编码解码 20 个测试词.
2. **Medium.**So sánh khả năng sinh sản của token cho tiếng Anh, Trung Quốc và tiếng Hindi bằng cách sử dụng cl100k_base của tiktoken.**中等。**Sử dụng mã thông báo so sánh tiếng Anh, tiếng Trung và tiếng Ấn Độ tỷ lệ sinh sản phân từ.
3. **Hard.**Trình hình SentencePiece Unigram trên một tập hợp tiếng Anh-Hindu hỗn hợp. So sánh khả năng sinh sản với mô hình BPE được đào tạo trên cùng một dữ liệu. / **困难。**Trong tập hợp ngôn ngữ tiếng Anh-Hindí, tập hợp các tập hợp ngôn ngữ tiếng Anh-Hindí, tập hợp các tập hợp ngôn ngữ tiếng Anh-Hindí, tập hợp các tập hợp ngôn ngữ tiếng Anh-Hindí, tập hợp các tập hợp ngôn ngữ tiếng Anh-Hindí, tập hợp các tập hợp ngôn ngữ tiếng Anh-Hindí, tập hợp các tập hợp ngôn ngữ tiếng Anh-Hindí, tập hợp các tập hợp ngôn ngữ tiếng Anh-Hindí, tập hợp các tập hợp ngôn ngữ tiếng Anh-Hindí, tập hợp các tập hợp ngôn ngữ tiếng Anh-Hindí, tập hợp các tập hợp ngôn ngữ tiếng Anh-Hindí, tập hợp các tập hợp ngôn ngữ tiếng Anh-Hindí, tập hợp các tập hợp ngôn ngữ tiếng Anh-Hindí, tập hợp các tập hợp ngôn ngữ tiếng Anh-Hindí, tập hợp các tập hợp ngôn ngữ tiếng Anh-Hindí, tập hợp các tập hợp ngôn ngữ tiếng Anh-Hindí, tập hợp các tập hợp các tập hợp ngôn ngữ tiếng Anh-Hindí, tập hợp các tập hợp các tập hợp các tập hợp các tập hợp.

> **【中文解读】**Trong 术语表中的"Những gì mọi người nói" vs "Những gì nó thực sự có nghĩa" 区分日常口语和精确技术含义── 在团队协作中,统一术语定义可以避免大量沟通误解──

## Từ khóa  Từ khóa nhanh chóng

| Term / 术语 | What people say / 人们常说的 | What it actually means / 实际含义 |
|------|-----------------|-----------------------|
| BPE（字节对编码） | GPT's tokenizer / GPT 的分词器 | Iteratively merge most frequent adjacent pairs. / 迭代合并最频繁的相邻对。 |
| Unigram | T5's tokenizer / T5 的分词器 | Prune tokens from large vocabulary by likelihood. / 按似然从大词表剪枝。 |
| WordPiece | BERT's tokenizer / BERT 的分词器 | Merge pairs that maximize corpus likelihood. / 合并使语料似然最大化的对。 |
| SentencePiece | Training library / 训练库 | Train BPE or Unigram on raw text. Encodes whitespace as `▁`. / 在原始文本上训练 BPE 或 Unigram。 |
| tiktoken | OpenAI's encoder / OpenAI 编码器 | Fast encoding against pre-built GPT vocabularies. / 针对预构建 GPT 词表的快速编码。 |
| Fertility（繁殖率） | Tokens per word / 每词 token 数 | How many subword tokens a word produces. Lower is better. / 一个词产生多少子词 token。越低越好。 |

> **【中文解读】**延伸阅读 cung cấp các nguồn chất lượng cao cho việc học sâu. Những bài báo và giảng dạy này là tài liệu tham khảo cổ điển trong lĩnh vực này, phù hợp với những người đọc cần hiểu sâu hơn.

## Xem thêm 延伸阅读

- [Sennrich et al. (2016). Neural Machine Translation of Rare Words with Subword Units](https://arxiv.org/abs/1508.07909) bài báo BPE. / BPE 论文。
- [Kudo (2018). Subword Regularization](https://arxiv.org/abs/1804.10959) báo Unigram. / Unigram 论文。
- [SentencePiece documentation](https://github.com/google/sentencepiece) đào tạo và phục vụ. / 训练和服务。
- [tiktoken](https://github.com/openai/tiktoken) OpenAI's fast tokenizer. / OpenAI 快速分词器──
- [Hugging Face Tokenizers](https://huggingface.co/docs/tokenizers/) Đào tạo hỗ trợ dung dịch. / Rust 后端训练 + 服务。
