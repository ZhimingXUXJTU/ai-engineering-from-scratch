# GloVe, FastText, và Subword Embeddings

> Word2Vec đào tạo một việc nhúng mỗi từ. GloVe đã tính toán các matrix co-occurrence. FastText nhúng các mảnh. BPE nối với các bộ chuyển đổi.
> Word2Vec 为每个词训练一个嵌入──GloVe 分解共现矩阵──FastText 嵌入词的组成部分──BPE 桥接到变压器──

> **【中文解读】**GloVe sử dụng toàn局共现统计,FastText 处理子词解决 OOV 问题。

**Type:** Build | **类型:** 动手
**Languages:** Python | **语言:** Python
**Prerequisites:** Phase 5 · 03 (Word2Vec from Scratch) | **前置知识:** Phase 5 · 03（Word2Vec 从零实现）
**Time:** ~45 minutes | **时间:** ~45 分钟

## Vấn đề  vấn đề giới thiệu

Word2Vec đã để lại hai câu hỏi mở.

> Word2Vec 留下了两个开放问题.

Đầu tiên, có một dòng nghiên cứu song song phân tích các matrix co-occurrence trực tiếp (LSA, HAL) thay vì làm cập nhật các biểu đồ bỏ qua trực tuyến. Phương pháp lặp lại của Word2Vec có cơ bản tốt hơn, hoặc sự khác biệt là một tác phẩm tạo ra cách xử lý hai phương pháp có tính? **GloVe**trả lời rằng: các yếu tố tử liệu với một lỗ được lựa chọn cẩn thận phù hợp hoặc đánh bại Word2Vec, và chi phí ít hơn để đào tạo.

> Thứ nhất, có một tuyến nghiên cứu đồng hành, trực tiếp phân tích các mô hình hiện tại (LSA、HAL), thay vì làm việc trực tuyến 更新──.**GloVe**回答了:配合精心选择的损失函数矩阵分解匹配或超过 Word2Vec,且训练成本较低――

Thứ hai, không có phương pháp nào có câu chuyện cho những từ mà nó chưa từng thấy.`Zoomer-approved`- `dogecoin`, bất kỳ từ chính xác được đặt ra tuần trước, mọi hình thức cong cong của một gốc hiếm.**FastText**Fixed this by embedding character n-grams: một từ là tổng của các phần của nó, bao gồm cả các morphemes, vì vậy ngay cả từ ngoài từ vựng cũng có một vector hợp lý.

> Thứ hai, hai phương pháp đối với những từ chưa từng thấy đều không có giải pháp.`Zoomer-approved``dogecoin`、上周刚造的任何专名词、稀有词根的每变形形式──**FastText**Bằng cách nhúng chữ n-gram sửa chữa vấn đề này: một từ là các phần của nó, bao gồm các chữ, vì vậy ngay cả từ bên ngoài biểu thức cũng có thể nhận được một khối lượng hợp lý.

Thứ ba, khi những người biến đổi đến, câu hỏi đã thay đổi một lần nữa.**Byte-pair encoding (BPE)**và họ hàng của nó giải quyết điều này bằng cách học một từ vựng của các đơn vị chữ phụ thường xuyên bao gồm mọi thứ.

> Thứ ba, khi Transformer đến, vấn đề lại chuyển đổi.**字节对编码（Byte-Pair Encoding, BPE）**及其变体通过学习覆盖一切的高频子词单元词表解决了这个问题──每个现代 LLM的每个现代分词器都是子词分词器──

Bài học này sẽ đi qua cả ba, sau đó giải thích nên tìm đến ai cho khi nào.

> Bài này sẽ giải thích từng thứ ba, sau đó giải thích khi nào nên sử dụng cái nào.

## Khái niệm cốt lõi

> **【中文解读】**Bài viết này giới thiệu các khái niệm và lý thuyết cốt lõi.

**GloVe (Global Vectors).**Xây dựng các từ từ co-occurrence matrix `X`nơi `X[i][j]`là bao nhiêu lần từ `j`xuất hiện trong ngữ cảnh của từ `i`- Đường dẫn tàu như vậy`v_i · v_j + b_i + b_j ≈ log(X[i][j])`- Chất cân, đôi đôi thường xuyên không chiếm ưu thế.

> **GloVe（全局向量）。**构建词-词共现矩阵 `X`, trong số đó `X[i][j]` 是词 `j`出现在词 `i`上下文中的频率──训练向量使 `v_i · v_j + b_i + b_j ≈ log(X[i][j])`                                                                                                                                                                                                                                                              

**FastText.**Một từ là tổng số n-gram của ký tự cộng với chính từ. `where`trở thành `<wh, whe, her, ere, re>, <where>`. Từ vector là tổng số các vector thành phần đó.`whereupon`) được tạo thành từ n-gram được biết đến.

> **FastText。**Một từ là chữ n-gram của nó và thêm từ chính nó.`where`变成 `<wh, whe, her, ere, re>, <where>`△词向量是这些组件的向量和──像 Word2Vec 一样训练──好处:未见过的词(`whereupon`) từ các n-gram 组合而成

**BPE (Byte-Pair Encoding).**Bắt đầu với một từ vựng của các byte (hoặc ký tự) riêng lẻ. Đếm từng cặp lân cận trong corpus. Thủy cặp thường xuyên nhất thành một token mới.`k`Kết quả: một từ vựng của `k + 256`token nơi các chuỗi thường xuyên (`ing`- `tion`- `the`(văn) là các biểu tượng đơn lẻ và các từ hiếm được chia thành các mảnh quen thuộc.

> **BPE（字节对编码）。**Từ đơn phương chữ cái (或字符) từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ đến đến đến đến đến đến đến đến đến đến đến đến đến đến đến đến đến đến đến đến đến đến đến đến đến đến đến đến đến đến đến đến đến đến đến đến đến đến đến đến đến đến đến đến`k`Kết quả: Một`k + 256`个 token 的词表, trong đó高频序列(`ing``tion``the`(văn) là một biểu tượng đơn lẻ, một từ hiếm được phân chia thành một đoạn quen thuộc.

> **【拓展：大语言模型的工程实践】**Từ GPT đến ChatGPT, NLP đã trải qua sự chuyển đổi từ "mỗi nhiệm vụ đào tạo một mô hình" đến "một mô hình giải quyết tất cả các nhiệm vụ". Trong công trình thực tế, việc triển khai LLM cần phải xem xét các vấn đề như: giới hạn token, trì hoãn, chi phí, kiểm tra an toàn, và các vấn đề khác.

> **【拓展：RAG 与企业知识库】**检索增强生成(RAG) là cấu trúc phổ biến nhất trong ứng dụng AI của doanh nghiệp hiện tại: sẽ truy vấn người dùng trước tiên truy vấn các đoạn tài liệu liên quan, tiếp tục truy vấn kết quả như trên dưới đây cho LLM 生成答案──

> **【拓展：NLP 的多语言挑战】**Trên toàn cầu có hơn 7000 ngôn ngữ, nhưng nghiên cứu về NLP tập trung chủ yếu vào tiếng Anh và một số ít ngôn ngữ.

## Hãy xây dựng nó.

> **【中文解读】**本节通过代码实现核心算法从零――这种" từ đầu"的方式能帮助理解框架背后的原理,遇到问题时不会被黑盒困住――
```figure
n5-subword-merge
```

## Hãy xây dựng nó

### GloVe: tính toán các matrix co-occurrence

```python
import numpy as np
from collections import Counter


def build_cooccurrence(docs, window=5):
    pair_counts = Counter()
    vocab = {}
    for doc in docs:
        for token in doc:
            if token not in vocab:
                vocab[token] = len(vocab)
    for doc in docs:
        indexed = [vocab[t] for t in doc]
        for i, center in enumerate(indexed):
            for j in range(max(0, i - window), min(len(indexed), i + window + 1)):
                if i != j:
                    distance = abs(i - j)
                    pair_counts[(center, indexed[j])] += 1.0 / distance
    return vocab, pair_counts


def glove_train(vocab, pair_counts, dim=16, epochs=100, lr=0.05, x_max=100, alpha=0.75, seed=0):
    n = len(vocab)
    rng = np.random.default_rng(seed)
    W = rng.normal(0, 0.1, size=(n, dim))
    W_tilde = rng.normal(0, 0.1, size=(n, dim))
    b = np.zeros(n)
    b_tilde = np.zeros(n)

    for epoch in range(epochs):
        for (i, j), x_ij in pair_counts.items():
            weight = (x_ij / x_max) ** alpha if x_ij < x_max else 1.0
            diff = W[i] @ W_tilde[j] + b[i] + b_tilde[j] - np.log(x_ij)
            coef = weight * diff

            grad_W_i = coef * W_tilde[j]
            grad_W_tilde_j = coef * W[i]
            W[i] -= lr * grad_W_i
            W_tilde[j] -= lr * grad_W_tilde_j
            b[i] -= lr * coef
            b_tilde[j] -= lr * coef

    return W + W_tilde
```

Hai mảnh chuyển động đáng để đặt tên.`f(x) = (x/x_max)^alpha`trọng lượng thấp đôi rất thường xuyên (như `(the, and)`) để họ không thống trị tổn thất.`W`(trung tâm) và `W_tilde`(context) bảng. Kết hợp cả hai là một trò lừa được công bố mà có xu hướng vượt qua chỉ bằng một.

> 两个值得指出的要点──加权函数 `f(x) = (x/x_max)^alpha`降低非常频繁的对(如 `(the, and)`(văn) của trọng lượng, làm cho nó không chủ yếu mất tích.`W`(中心词) 和 `W_tilde`(上下文词)表之和──对两者求和是一个已发表的技巧, thường tốt hơn là chỉ sử dụng một trong số đó──

### FastText: các bản nhúng có ý thức về các từ phụ

```python
def char_ngrams(word, n_min=3, n_max=6):
    wrapped = f"<{word}>"
    grams = {wrapped}
    for n in range(n_min, n_max + 1):
        for i in range(len(wrapped) - n + 1):
            grams.add(wrapped[i:i + n])
    return grams
```

```python
>>> char_ngrams("where")
{'<where>', '<wh', 'whe', 'her', 'ere', 're>', '<whe', 'wher', 'here', 'ere>', '<wher', 'where', 'here>'}
```

Mỗi từ được đại diện bởi bộ n-gram của nó (thường là 3 đến 6 ký tự).

> Mỗi từ từ từ n-gram 集合 (thường là 3 đến 6 chữ cái) biểu hiện.

```python
def fasttext_vector(word, ngram_table):
    grams = char_ngrams(word)
    vecs = [ngram_table[g] for g in grams if g in ngram_table]
    if not vecs:
        return None
    return np.sum(vecs, axis=0)
```

Đối với một từ không nhìn thấy, bạn vẫn nhận được một vector miễn là một số n-gram của nó được biết. `whereupon`cổ phiếu `<wh`- `her`- `ere`, và`<where`với `where`, nên hai cánh đất gần nhau.

> Đối với những từ chưa thấy, miễn là phần n-gram của nó là đã biết, bạn vẫn có thể nhận được một khối lượng.`whereupon`Với`where`共享 `<wh``her``ere`和 `<where`Vì vậy cả hai đều nằm ở vị trí gần nhau.

### BPE: từ vựng phụ học

```python
def learn_bpe(corpus, k_merges):
    vocab = Counter()
    for word, freq in corpus.items():
        tokens = tuple(word) + ("</w>",)
        vocab[tokens] = freq

    merges = []
    for _ in range(k_merges):
        pair_freq = Counter()
        for tokens, freq in vocab.items():
            for a, b in zip(tokens, tokens[1:]):
                pair_freq[(a, b)] += freq
        if not pair_freq:
            break
        best = pair_freq.most_common(1)[0][0]
        merges.append(best)

        new_vocab = Counter()
        for tokens, freq in vocab.items():
            new_tokens = []
            i = 0
            while i < len(tokens):
                if i + 1 < len(tokens) and (tokens[i], tokens[i + 1]) == best:
                    new_tokens.append(tokens[i] + tokens[i + 1])
                    i += 2
                else:
                    new_tokens.append(tokens[i])
                    i += 1
            new_vocab[tuple(new_tokens)] = freq
        vocab = new_vocab
    return merges


def apply_bpe(word, merges):
    tokens = list(word) + ["</w>"]
    for a, b in merges:
        new_tokens = []
        i = 0
        while i < len(tokens):
            if i + 1 < len(tokens) and tokens[i] == a and tokens[i + 1] == b:
                new_tokens.append(a + b)
                i += 2
            else:
                new_tokens.append(tokens[i])
                i += 1
        tokens = new_tokens
    return tokens
```

```python
>>> corpus = Counter({"low": 5, "lower": 2, "newest": 6, "widest": 3})
>>> merges = learn_bpe(corpus, k_merges=10)
>>> apply_bpe("lowest", merges)
['low', 'est</w>']
```

Lần lặp đầu tiên kết hợp cặp lân cận phổ biến nhất.`low`- `est`- `tion`) trở thành các token đơn lẻ và các từ hiếm gặp phá vỡ sạch.

> Lần đầu tiên 代合并 邻近                                                                                                                                                                                                                                                         `low``est``tion`(văn) trở thành một biểu tượng đơn lẻ, hiếm thấy từ làm sạch địa phân hủy.

Các token GPT / BERT / T5 thực sự học được 30k-100k hợp nhất. Kết quả: bất kỳ văn bản nào được token hóa thành một chuỗi dài hạn hạn của các ID được biết đến, không có OOV bao giờ.

> GPT / BERT / T5 分词器学习 3 万到 10 万次合并──结果: bất kỳ văn bản nào đều được phân từ thành chuỗi có giới hạn của ID đã biết, sẽ không bao giờ có OOV──

> **【中文解读】**Bài này sẽ trình bày cách sử dụng một khung đã phát triển như PyTorch, HuggingFace, và các khác.

> **【拓展：Prompt Engineering 与 LLM 应用】**Kỹ thuật nhanh chóng đã trở thành kỹ năng cốt lõi của các kỹ sư NLP. Từ Zero-shot đến Few-shot, từ Chain-of-Thought đến ReAct, các chiến lược khác nhau áp dụng cho các tình huống khác nhau. Trong các dự án thực tế, thiết kế của System提示(System Prompt) ảnh hưởng trực tiếp đến sự ổn định và chất lượng sản xuất của ứng dụng LLM.

## Hãy sử dụng nó để thực hiện

Thực tế, bạn hiếm khi tự huấn luyện những thứ này.

> Thực tế, bạn hầu như không tự tập luyện những điều này.

```python
import fasttext.util
fasttext.util.download_model("en", if_exists="ignore")
ft = fasttext.load_model("cc.en.300.bin")
print(ft.get_word_vector("whereupon").shape)
print(ft.get_word_vector("zoomerapproved").shape)
```

Đối với token hóa các từ phụ theo kiểu BPE trong thời đại biến thể:

> 对于 Transformer 时代的 BPE 风格子词分词:

```python
from transformers import AutoTokenizer

tok = AutoTokenizer.from_pretrained("gpt2")
print(tok.tokenize("unbelievably tokenized"))
```

```
['un', 'bel', 'iev', 'ably', 'Ġtoken', 'ized']
```

- `Ġ`Prefix đánh dấu ranh giới từ (một quy ước GPT-2).

> `Ġ`前标记词边界(GPT-2 的约定) ・・・每个现代分词器都是 BPE 变体、WordPiece(BERT) 或 SentencePiece(T5、LLaMA) ・・・

### Khi nào để chọn

| Situation | Pick | 场景 | 选择 |
|-----------|------|------|------|
| Pretrained general-purpose word vectors, no OOV tolerance needed | GloVe 300d | 预训练通用词向量，不需要处理 OOV | GloVe 300 维 |
| Pretrained general-purpose word vectors, must handle misspellings / neologisms / morphologically rich languages | FastText | 预训练通用词向量，必须处理拼写错误 / 新词 / 形态丰富的语言 | FastText |
| Anything going into a transformer (training or inference) | Whatever tokenizer the model shipped with. Never swap. | 输入 Transformer 的任何场景（训练或推理） | 模型自带的分词器。永远不要替换。 |
| Training your own language model from scratch | Train a BPE or SentencePiece tokenizer on your corpus first | 从零训练自己的语言模型 | 先在你的语料上训练 BPE 或 SentencePiece 分词器 |
| Production text classification with a linear model | Still TF-IDF. Lesson 02. | 使用线性模型的生产文本分类 | 仍然用 TF-IDF。第 02 课。 |

> **【中文解读】**Phần này tập trung vào cách phân phối mô hình như một sản phẩm có thể sử dụng.

## Chuyển nó đi.

Cứ như `outputs/skill-embeddings-picker.md`- Có thể là:

```markdown
---
name: tokenizer-picker
description: Pick a tokenization approach for a new language model or text pipeline.
version: 1.0.0
phase: 5
lesson: 04
tags: [nlp, tokenization, embeddings]
---

Given a task and dataset description, you output:

1. Tokenization strategy (word-level, BPE, WordPiece, SentencePiece, byte-level). One-sentence reason.
2. Vocabulary size target (e.g., 32k for an English-only LM, 64k-100k for multilingual).
3. Library call with the exact training command. Name the library. Quote the arguments.
4. One reproducibility pitfall. Tokenizer-model mismatch is the single most common silent production bug; call out which pair must be used together.

> **【中文解读】** 练习题按照 Easy/Medium/Hard 三个难度递进。建议至少完成 Medium 级别的题目，Hard 级别适合深入研究或面试准备。

Refuse to recommend training a custom tokenizer when the user is fine-tuning a pretrained LLM. Refuse to recommend word-level tokenization for any model targeting production inference. Flag non-English / multi-script corpora as needing SentencePiece with byte fallback.
```

## Tập luyện bài tập

1. **Easy.**Đi chạy`char_ngrams("playing")`và `char_ngrams("played")`- tính toán sự chồng chéo Jaccard của hai bộ n-gram.`pla`- `lay`- `play`), đó là lý do tại sao FastText chuyển giao tốt qua các biến thể hình thái.
   **简单。**运行 `char_ngrams("playing")`和 `char_ngrams("played")`△计算两个n-gram 集合的Jaccard 重叠度──你应该看到大量共享片段(`pla``lay``play`), đây là lý do FastText trong hình dạng thay đổi trong quá trình di chuyển tốt.
2. **Medium.**Tăng `learn_bpe`để theo dõi sự tăng trưởng từ vựng. ghi mã thông báo-per-corpus-character như là một hàm số hợp nhất. Bạn nên thấy nén nhanh ban đầu, như bắt đầu gần ~2-3 chars mỗi mã thông báo.
   **中等。**扩展 `learn_bpe`以跟踪词表增长──绘制 mỗi chữ ký của biểu tượng số như hàm của số lần hợp并── bạn nên thấy bắt đầu khi nhanh chóng nén, trong khoảng 2-3 chữ ký/ biểu tượng 附近渐近──
3. **Hard.**Hãy tập 1k-mích BPE trên toàn bộ tác phẩm của Shakespeare. So sánh các biểu tượng từ thông thường so với các danh từ hiếm. đo mức trung bình biểu tượng mỗi từ trước và sau. Viết ra những gì đã làm bạn ngạc nhiên.
   **困难。**Trong Shakespeare toàn tập tập 1 千次合并的 BPE──比较常见词与罕见专名词的分词结果──测量前后的平均每词符号 数──写下让你惊的地方──

> **【中文解读】**练题按照 Easy/Medium/Hard 三个难度递进;;建议至少完成 级别的题目, 级别适合深入研究或面试准备;;

## Từ khóa  Từ khóa nhanh chóng

| Term | What people say | What it actually means | 术语 | 人们常说的 | 实际含义 |
|------|-----------------|-----------------------|------|-----------|---------|
| Co-occurrence matrix | Word-word frequency table | `X[i][j]` = how often word `j` appears in a window around word `i`. | 共现矩阵 | 词-词频率表 | `X[i][j]` = 词 `j` 在词 `i` 周围窗口中出现的频率。 |
| Subword | Piece of a word | A character n-gram (FastText) or learned token (BPE/WordPiece/SentencePiece). | 子词 | 词的片段 | 字符 n-gram（FastText）或学习到的 token（BPE/WordPiece/SentencePiece）。 |
| BPE | Byte-pair encoding | Iterative merging of most-frequent adjacent pairs until vocabulary hits target size. | BPE（字节对编码） | 字节对编码 | 迭代合并最频繁的相邻对，直到词表达到目标大小。 |
| OOV | Out of vocabulary | Word the model has never seen. Word2Vec/GloVe fail. FastText and BPE handle it. | OOV（词表外） | 词表外 | 模型从未见过的词。Word2Vec/GloVe 会失败。FastText 和 BPE 能处理。 |
| Byte-level BPE | BPE on raw bytes | GPT-2's scheme. Vocabulary starts with 256 bytes, so nothing is ever OOV. | 字节级 BPE | 对原始字节的 BPE | GPT-2 的方案。词表从 256 个字节开始，所以永远不会有 OOV。 |

> **【中文解读】**Trong 术语表中的"Những gì mọi người nói" vs "Những gì nó thực sự có nghĩa" 区分日常口语和精确技术含义── 在团队协作中,统一术语定义可以避免大量沟通误解──

## Xem thêm 延伸阅读

- [Pennington, Socher, Manning (2014). GloVe: Global Vectors for Word Representation](https://nlp.stanford.edu/pubs/glove.pdf) Glove paper, bảy trang, vẫn là dẫn xuất tốt nhất của sự mất mát. / Glove 论文,七页,仍然是损失函数最好的推导──
- [Bojanowski et al. (2017). Enriching Word Vectors with Subword Information](https://arxiv.org/abs/1607.04606) FastText. / FastText 论文。
- [Sennrich, Haddow, Birch (2016). Neural Machine Translation of Rare Words with Subword Units](https://arxiv.org/abs/1508.07909) bài báo giới thiệu BPE vào NLP hiện đại. / 将 BPE 引入现代 NLP 的论文──
- [Hugging Face tokenizer summary](https://huggingface.co/docs/transformers/tokenizer_summary) cách BPE, WordPiece và SentencePiece thực sự khác nhau trong thực tế.
