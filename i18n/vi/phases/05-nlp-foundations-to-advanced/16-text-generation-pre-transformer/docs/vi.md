# Text Generation Before Transformers  N-gram Language Models  Transformer  trước đây văn bản tạo  N-gram 语言模型

> Nếu một từ là đáng ngạc nhiên, mô hình là xấu. Sự bối rối làm cho một số ngạc nhiên. Nhấp nhàng giữ cho nó hữu hạn.
> Nếu một từ đáng kinh ngạc, mô hình là không tốt.

> **【中文解读】**N-gram 统计词频预测 下一个词──GPT 就是更强大的语言模型──

**Type:** Build | **类型:** 动手
**Languages:** Python | **语言:** Python
**Prerequisites:** Phase 5 · 01 (Text Processing), Phase 2 · 14 (Naive Bayes) | **前置知识:** Phase 5 · 01（文本处理），Phase 2 · 14（朴素贝叶斯）
**Time:** ~45 minutes | **时间:** ~45 分钟

## Vấn đề  vấn đề giới thiệu

Trước khi biến đổi, trước khi RNN, trước khi nhúng từ, một mô hình ngôn ngữ dự đoán từ tiếp theo bằng cách đếm số lần nó sau từ trước `n-1`đếm "mẹ" → "ngồi" 47 lần, "mẹ" → " nhảy" 12 lần, "mẹ" → "tủ lạnh" 0 lần. bình thường để có được phân bố xác suất.

> Trong Transformer  trước, trong RNN  trước, trong từ 嵌入 trước, ngôn ngữ模型通过统计前 `n-1`个词后面跟着当前词的频率来预测下一个词――统计 "hẹ" → "hẹ" xuất hiện 47 lần, "hẹ" → " nhảy" xuất hiện 12 lần, "hẹ" → "hàng lạnh" xuất hiện 0 lần――归结得到概率分布──

> **【中文解读】**Câu hỏi được đặt ra trong phần này là: làm thế nào để hiểu và áp dụng đúng công nghệ này trong công trình thực tế.

Đây là mô hình ngôn ngữ n-gram. Nó chạy mọi bộ nhận dạng ngôn ngữ, mỗi bộ kiểm tra đánh vần, và mọi hệ thống dịch thuật máy dựa trên cụm từ năm 1980 đến năm 2015. Nó vẫn chạy khi bạn cần mô hình ngôn ngữ giá rẻ trên thiết bị.

> Đây là mô hình ngôn ngữ n-gram. Từ năm 1980 đến năm 2015, nó hoạt động trên mỗi bộ nhận dạng tiếng nói, trên mỗi bộ kiểm tra chữ viết và trên mỗi hệ thống dịch thuật máy dựa trên ngôn ngữ ngắn.

Vấn đề thú vị là phải làm gì với n-gram không thấy. Một mô hình dựa trên số liệu thô gán xác suất không cho bất cứ điều gì mà nó không thấy, điều này là thảm họa vì các câu dài và gần như mọi câu dài chứa ít nhất một chuỗi không thấy. Năm mươi năm nghiên cứu làm trơn đã khắc phục điều đó.

> Vấn đề thú vị là: làm thế nào để xử lý các n-gram chưa thấy. Mô hình dựa trên số liệu ban đầu phân phối không xác suất bất kỳ thứ gì chưa thấy, đó là thảm họa, bởi vì câu dài, hầu như mỗi câu dài đều chứa ít nhất một chuỗi chưa thấy. Nghiên cứu trình độ trong 50 năm đã giải quyết vấn đề này.

## Khái niệm cốt lõi

> **【中文解读】**Bài viết này giới thiệu các khái niệm và lý thuyết cốt lõi.

![N-gram model: count, smooth, generate](../assets/ngram.svg)

### Trò chơi dự đoán

Trước khi bất kỳ thiết bị nào tồn tại, một thí nghiệm đã xác định mô hình ngôn ngữ là gì. Hãy bao phủ chữ cái tiếp theo của một câu tiếng Anh. Hãy yêu cầu ai đó đoán nó, một đoán một lần, cho đến khi họ làm đúng. Hãy ghi lại số lượng đoán. Hãy lặp lại cho vài trăm chữ cái.

Số lượng đoán không phải là thứ thường. Chúng là một mã hóa lại không mất mát của văn bản: trao chuỗi đếm cho một người đoán thứ hai, giống nhau và họ có thể tái cấu trúc mọi chữ cái, bởi vì ở mỗi vị trí họ biết chính xác những đoán nào đi trước. Một thông điệp bạn có thể mã hóa lại bằng ít biểu tượng hơn mang lại ít thông tin hơn cho mỗi biểu tượng, vì vậy số liệu thống kê đoán đặt một giới hạn cho sự nhập khẩu của tiếng Anh.

Shannon đã thực hiện điều này vào năm 1951 và có một số mà vẫn thống trị lĩnh vực.`log2(27) ≈ 4.75`Các con người đoán với 100 chữ cái của ngữ cảnh hạ cánh giữa 0,6 và 1,3 bit mỗi chữ cái. tiếng Anh là khoảng ba phần tư các chuyển động buộc.

Mỗi mô hình ngôn ngữ kể từ đó là một người chơi cơ học của trò chơi này, và mỗi số đánh giá trong bài học này là trò chơi ghi điểm:

- **Cross-entropy loss**là số lượng bit trung bình mà mô hình cần cho mỗi biểu tượng.
- **Perplexity**là `2^bits`(hoặc `e^nats`): yếu tố phân nhánh vẫn đối mặt với mô hình sau khi phỏng đoán.
- **Context length is the player's memory.**Một mô hình trigram chơi với hai token bộ nhớ. Một biến thể chơi cùng một trò chơi với 100K token. Các quy tắc không bao giờ thay đổi; người chơi đã tốt hơn.

Một đơn vị chuyển đổi sang đường đua: điểm số của trò chơi cho mỗi chữ cái trong bit (`log2`), trong khi các công thức n-gram dưới đây ghi điểm cho mỗi từ biểu tượng trong nats (logbock tự nhiên)  và kể từ sự bối rối `e^H`trong nats bằng nhau `2^H`trong bit, hai quan điểm là cùng một thước đo trong các đơn vị khác nhau.

```figure
prediction-game
```

**N-gram probability:** `P(w_i | w_{i-n+1}, ..., w_{i-1})`- Đặt lại .`n`(thường là 3 cho trigram, 4 cho 4 gram).

> **N-gram 概率：** `P(w_i | w_{i-n+1}, ..., w_{i-1})`❖ Đặt `n`(三元组 thường là 3,四元组 là 4)

```text
P(w | context) = count(context, w) / count(context)
```

**The zero-count problem.**Bất kỳ n-gram nào không được nhìn thấy trong đào tạo đều có xác suất bằng không. Một nghiên cứu năm 2007 trên Brown corpus cho thấy rằng ngay cả một mô hình 4 gram có 30% 4 gram không được nhìn thấy trong đào tạo. Bạn không thể đánh giá trên bất kỳ văn bản thực nào mà không làm trơn.

> **零计数问题。**Các n-gram không được thấy trong bất kỳ cuộc tập luyện nào đều có tỷ lệ xác suất 0.  Nghiên cứu năm 2007 về bộ thư viện ngôn ngữ Brown cho thấy, ngay cả các mô hình 4元组 cũng có 30% lượng 4元组 không được thấy trong các cuộc tập luyện.

**Smoothing approaches, in order of sophistication:**

> **平滑方法，按复杂度排序：**

1. **Laplace (add-one).**Thêm 1 vào mỗi con số.
   **拉普拉斯（加一）。**Đưa cho mỗi con số thêm 1... đơn giản, nhưng hiệu quả rất kém trong những sự kiện hiếm hoi.
2. **Good-Turing.**Đổi lại khối lượng xác suất từ các sự kiện tần số cao hơn đến những sự kiện không thể thấy dựa trên tần số tần số.
   **Good-Turing。**Dựa trên tần suất tần suất, sẽ phân bổ chất lượng xác suất từ các sự kiện cao tần suất sang các sự kiện chưa thấy.
3. **Interpolation.**Kết hợp n-gram, (n-1)-gram, vv, ước tính với trọng lượng có thể điều chỉnh.
   **插值。**Sử dụng có thể điều chỉnh quyền重组合 n-gram, n-1)-gram 等估计.
4. **Backoff.**Nếu n-gram có số không, hãy giảm xuống (n-1) -gram.
   **回退。**Nếu n-gram 计数为零, quay trở lại (n-1) -gram.
5. **Absolute discounting.**Giảm giảm giá cố định `D`Từ mọi thứ, phân phối lại cho những gì không thể thấy được.
   **绝对折扣。**Từ tất cả các tính toán giảm giá cố định`D`, tái phân phối cho các sự kiện chưa thấy.
6. **Kneser-Ney.**Sự giảm giá tuyệt đối cộng với một lựa chọn thông minh cho mô hình thứ tự thấp hơn: sử dụng * xác suất tiếp tục * (nhiều ngữ ngữ ngữ một từ xuất hiện) thay vì tần số nguyên liệu.
   **Kneser-Ney。**绝对折扣加上低阶模型的巧妙选择: sử dụng*续接概率*(一个词出现多少上下文中) thay vì là tần suất nguyên thủy。

Sự hiểu biết của Kneser-Ney rất sâu sắc. "San Francisco" là một chữ lớn phổ biến. Unigram "Francisco" xuất hiện chủ yếu sau "San. " Sự giảm giá tuyệt đối ngây thơ cho "Francisco" xác suất unigram cao (vì số lượng là cao). Kneser-Ney nhận thấy rằng "Francisco" chỉ xuất hiện trong một bối cảnh và giảm khả năng tiếp tục của nó tương ứng. Kết quả: một biểu tượng lớn mới kết thúc bằng "Francisco" có được xác suất thấp thích hợp.

> Kneser-Ney's Insight is very deep──"San Francisco" is a commonplace of二元组──一元组 "Francisco" 主要 appears in "San" 之后──朴素绝对折扣给"Francisco" 高一元组概率(因为计数高)──Kneser-Ney lưu ý "Francisco" chỉ xuất hiện trong một上下文中,相应地降低其续概率──结果:以"Francisco"结尾的新二元组获得适当的低概率──

**Evaluation: perplexity.**Tỷ lệ nhân của tỷ lệ trung bình âm tính log-cho khả năng mỗi từ trên một tập hợp thử nghiệm được tổ chức. thấp hơn là tốt hơn. Một sự bối rối của 100 có nghĩa là mô hình là bối rối như nó sẽ chọn đồng đều trong số 100 từ.

> **评估：困惑度。**留出测试集上每字平均负对数似然的指数──越低越好──困惑度 100 nghĩa là mức độ bối rối của mô hình tương đương với bình chọn trong 100 từ──

```text
perplexity = exp(- (1/N) * Σ log P(w_i | context_i))
```

> **【中文解读】**本节通过代码实现核心算法从零――这种" từ đầu"的方式能帮助理解框架背后的原理,遇到问题时不会被黑盒困住――

> **【拓展：大语言模型的工程实践】**Từ GPT đến ChatGPT, NLP đã trải qua sự chuyển đổi từ "mỗi nhiệm vụ đào tạo một mô hình" đến "một mô hình giải quyết tất cả các nhiệm vụ". Trong công trình thực tế, việc triển khai LLM cần phải xem xét các vấn đề như: giới hạn token, trì hoãn, chi phí, kiểm tra an toàn, và các vấn đề khác.

> **【拓展：RAG 与企业知识库】**检索增强生成(RAG) là cấu trúc phổ biến nhất trong ứng dụng AI của doanh nghiệp hiện tại: sẽ truy vấn người dùng trước tiên truy vấn các đoạn tài liệu liên quan, tiếp tục truy vấn kết quả như trên dưới đây cho LLM 生成答案──

> **【拓展：NLP 的多语言挑战】**Trên toàn cầu có hơn 7000 ngôn ngữ, nhưng nghiên cứu về NLP tập trung chủ yếu vào tiếng Anh và một số ít ngôn ngữ.

## Hãy xây dựng nó.

> **【中文解读】**本节通过代码实现核心算法从零――这种" từ đầu"的方式能帮助理解框架背后的原理,遇到问题时不会被黑盒困住――
```figure
ngram-backoff
```

## Hãy xây dựng nó

### Bước 1: đếm trigram

```python
from collections import Counter, defaultdict


def train_ngram(corpus_tokens, n=3):
    ngrams = Counter()
    contexts = Counter()
    for sentence in corpus_tokens:
        padded = ["<s>"] * (n - 1) + sentence + ["</s>"]
        for i in range(len(padded) - n + 1):
            ctx = tuple(padded[i:i + n - 1])
            word = padded[i + n - 1]
            ngrams[ctx + (word,)] += 1
            contexts[ctx] += 1
    return ngrams, contexts


def raw_probability(ngrams, contexts, context, word):
    ctx = tuple(context)
    if contexts.get(ctx, 0) == 0:
        return 0.0
    return ngrams.get(ctx + (word,), 0) / contexts[ctx]
```

Input là một danh sách các câu được token hóa. Output là n-gram và contexts. `<s>`và `</s>`là giới hạn của câu.

> 输入是分词后的句子列表──输出是 n-gram 计数和上下文计数──`<s>`和 `</s>`Đó là giới hạn của nó.

### Bước 2: Lượt nhẵn Laplace

```python
def laplace_probability(ngrams, contexts, vocab_size, context, word):
    ctx = tuple(context)
    numerator = ngrams.get(ctx + (word,), 0) + 1
    denominator = contexts.get(ctx, 0) + vocab_size
    return numerator / denominator
```

Thêm 1 vào mỗi đếm, làm cho khối lượng của các sự kiện không thể nhìn thấy được phân bổ quá mức, làm tổn thương những sự kiện hiếm gặp.

> Đưa cho mỗi số lượng thêm 1 ∙ Đưa cho các sự kiện chưa từng thấy, cũng gây tổn thương cho những sự kiện hiếm gặp đã được biết

### Bước 3: Kneser-Ney (những chữ cái lớn, được phân tích)

```python
def kneser_ney_bigram_model(corpus_tokens, discount=0.75):
    unigrams = Counter()
    bigrams = Counter()
    unigram_contexts = defaultdict(set)

    for sentence in corpus_tokens:
        padded = ["<s>"] + sentence + ["</s>"]
        for i, w in enumerate(padded):
            unigrams[w] += 1
            if i > 0:
                prev = padded[i - 1]
                bigrams[(prev, w)] += 1
                unigram_contexts[w].add(prev)

    total_unique_bigrams = sum(len(ctx_set) for ctx_set in unigram_contexts.values())
    continuation_prob = {
        w: len(ctx_set) / total_unique_bigrams for w, ctx_set in unigram_contexts.items()
    }

    context_totals = Counter()
    for (prev, w), count in bigrams.items():
        context_totals[prev] += count

    unique_follow = defaultdict(set)
    for (prev, w) in bigrams:
        unique_follow[prev].add(w)

    def prob(prev, w):
        count = bigrams.get((prev, w), 0)
        denom = context_totals.get(prev, 0)
        if denom == 0:
            return continuation_prob.get(w, 1e-9)
        first_term = max(count - discount, 0) / denom
        lambda_prev = discount * len(unique_follow[prev]) / denom
        return first_term + lambda_prev * continuation_prob.get(w, 1e-9)

    return prob
```

Ba phần di chuyển.`continuation_prob`"Thật ngữ này xuất hiện trong bao nhiêu ngữ cảnh khác nhau?" (khiến đổi Kneser-Ney).`lambda_prev`là khối lượng được giải phóng bởi giá giảm, được sử dụng để cân nặng backkoff.

> 3 động thái phần:`continuation_prob`捕获 "这个词出现在多少不同上下文中?"`lambda_prev`là chất lượng của giảm giá, được sử dụng để tăng giá trị trở lại.

### Bước 4: tạo văn bản bằng cách lấy mẫu

```python
import random


def generate(prob_fn, vocab, prefix, max_len=30, seed=0):
    rng = random.Random(seed)
    tokens = list(prefix)
    for _ in range(max_len):
        candidates = [(w, prob_fn(tokens[-1], w)) for w in vocab]
        total = sum(p for _, p in candidates)
        r = rng.random() * total
        acc = 0.0
        for w, p in candidates:
            acc += p
            if r <= acc:
                tokens.append(w)
                break
        if tokens[-1] == "</s>":
            break
    return tokens
```

Các mẫu tương ứng với xác suất. luôn cho ra hiệu suất khác nhau cho mỗi hạt. Đối với hiệu suất giống như chùm tìm kiếm, chọn argmax tại mỗi bước (cười tham) và thêm một nút ngẫu nhiên nhỏ (giới nhiệt).

> 按概率比例采样. Mỗi hạt luôn luôn đưa ra các kết quả khác nhau. Đối với các kết quả tìm kiếm tương tự, mỗi bước lấy argmax.

### Bước 5: bối rối

```python
import math


def perplexity(prob_fn, sentences):
    total_log_prob = 0.0
    total_tokens = 0
    for sentence in sentences:
        padded = ["<s>"] + sentence + ["</s>"]
        for i in range(1, len(padded)):
            p = prob_fn(padded[i - 1], padded[i])
            total_log_prob += math.log(max(p, 1e-12))
            total_tokens += 1
    return math.exp(-total_log_prob / total_tokens)
```

Với Brown corpus, một mô hình KN 4 gram được điều chỉnh tốt đạt độ phức tạp khoảng 140. Một biến thể LM đạt 15-30 trên cùng bộ thử nghiệm. khoảng cách là khoảng 10x.

> 越低越好── đối với Brown 语料库, một sự chú ý trong việc điều chỉnh các mô hình KN 模型困惑度约140──Transformer 语言模型 đạt 15-30 trên cùng một tập thể kiểm tra── khoảng cách khoảng 10 lần──

> **【中文解读】**Bài này sẽ trình bày cách sử dụng một khung đã phát triển như PyTorch, HuggingFace, và các khác.

> **【拓展：Prompt Engineering 与 LLM 应用】**Kỹ thuật nhanh chóng đã trở thành kỹ năng cốt lõi của các kỹ sư NLP. Từ Zero-shot đến Few-shot, từ Chain-of-Thought đến ReAct, các chiến lược khác nhau áp dụng cho các tình huống khác nhau. Trong các dự án thực tế, thiết kế của System提示(System Prompt) ảnh hưởng trực tiếp đến sự ổn định và chất lượng sản xuất của ứng dụng LLM.

## Hãy sử dụng nó để thực hiện

- **Classical NLP teaching.**Sự tiếp xúc rõ ràng nhất với sự trơn tru, MLE, và sự bối rối mà bạn có thể nhận được.
  **经典 NLP 教学。**Bạn có thể có được sự trải nghiệm thanh thản nhất, MLE và bối rối nhất.
- **KenLM.**Tác phẩm n-gram thư viện. được sử dụng như một rescorer trong các hệ thống nói chuyện và MT nơi độ trễ thấp quan trọng.
  **KenLM。**生产级 n-gram 库──用作低延迟语音和MT 系统的重评分器──
- **On-device autocomplete.**Mô hình hình âm âm trong bàn phím.
  **设备端自动补全。**Mô hình 3元组 trong bàn phím.
- **Baselines.**Luôn tính toán một n-gram LM phức tạp trước khi tuyên bố LM thần kinh của bạn tốt.
  **基线。**Trong khi đó, bạn sẽ phải tính toán n-gram LM 困惑度. Nếu Transformer của bạn không đánh bại KN, thì có vấn đề.

> **【中文解读】**Phần này tập trung vào cách phân phối mô hình như một sản phẩm có thể sử dụng.

## Chuyển nó đi.

Cứ như `outputs/prompt-lm-baseline.md`- Có thể là:

> 保存为 `outputs/prompt-lm-baseline.md`- Có thể là:

```markdown
---
name: lm-baseline
description: Build a reproducible n-gram language model baseline before training a neural LM.
phase: 5
lesson: 16
---

Given a corpus and target use (next-word prediction, rescoring, perplexity baseline), output:

1. N-gram order. Trigram for general English, 4-gram if corpus is large, 5-gram for speech rescoring.
2. Smoothing. Modified Kneser-Ney is the default; Laplace only for teaching.
3. Library. `kenlm` for production, `nltk.lm` for teaching, roll your own only to learn.
4. Evaluation. Held-out perplexity with consistent tokenization between train and test sets.

Refuse to report perplexity computed with different tokenization between systems being compared — perplexity numbers are comparable only under identical tokenization. Flag OOV rate in test set; KN handles OOV poorly unless you reserve a special <UNK> token during training.
```

> **【中文解读】**练题按照 Easy/Medium/Hard 三个难度递进;;建议至少完成 级别的题目, 级别适合深入研究或面试准备;;

## Tập luyện bài tập

1. **Easy.**Hãy tập một chữ trigram LM trên một tập thể Shakespeare 1000 câu. tạo ra 20 câu. Chúng sẽ có khả năng tại địa phương nhưng không phù hợp trên toàn cầu. Đây là bản demo truyền thống.
   **简单。**Trong 1000 câu nói của Shakespeare, tập luyện mô hình ngôn ngữ.
2. **Medium.**Thực hiện sự bối rối cho mô hình KN của bạn trên một phân chia Shakespeare kéo dài. So sánh với Laplace. Bạn nên thấy sự bối rối KN thấp hơn 30-50%.
   **中等。**Trong phần còn lại của Shakespeare, bạn nên thấy KN giảm con số con số con số con số con số con số con số con số con số con số con số con số con số con số con số con số con số con số con số con số con số con số con số con số con số con số con số con số con số con số con số con số con số con số con số con số con số con số con số con số con số con số con số con số con số con số con số con số con số con số con số con số con số con số con số con số con số con số con số con số con số con số con số con số con số con số con số con số con số con số con số con số con số con số con số con số con số con số con số con số con số con số con số con số con số con số con số con số con số con số con số con số con số con số con số con số con số con số con số con số con số con số con số con số con số con số con số con số con số con số con số con số con số con số con số con số con số con số con số con số con số con số con số con số con số con số con số con số con số con số con số con số con số con số con số con số con số con số con số con số con số con số con số con số con số con số con số con số con số con số con số con số con số con số con số con số con số con số con số con số con số con số con số con số con số con số con số con số con số con số con số con số con số con số con số con số con số con số con số con số con số con số con số con số con số con số con số con số con số con số con số con số con số con số con số con số con số con số con số con số con số con số con số con số con số con số con số con số con số con số con số con số con số con số con số con số con số con số con số con số con số con số con số con số con số con số con số con số con số con số con số con số con số con số con số con số con số con số con số con số con số con số con số con số con số con số con số con số con số
3. **Hard.**Xây dựng một trình chỉnh đúc chữ trigram: với một từ bị đánh dấu sai và bối cảnh của nó, tạo ra các sửa đổi và xếp hạng theo xác suất ngữ cảnh theo LM. Đánh giá trên các chữ viết Birkbeck (thường).
   **困难。**构建三元组拼写纠错器:给定一个拼写错误的词及其上下文,生成纠正并按LM 下的上下文概率排序── 在 Birkbeck 拼写语料库(公开) 上评估──

> **【中文解读】**Trong 术语表中的"Những gì mọi người nói" vs "Những gì nó thực sự có nghĩa" 区分日常口语和精确技术含义── 在团队协作中,统一术语定义可以避免大量沟通误解──

## Từ khóa  Từ khóa nhanh chóng

| Term / 术语 | What people say / 人们常说的 | What it actually means / 实际含义 |
|------|-----------------|-----------------------|
| N-gram | Word sequence / 词序列 | Sequence of `n` consecutive tokens. / `n` 个连续 token 的序列。 |
| Smoothing（平滑） | Avoiding zeros / 避免零 | Reallocating probability mass so unseen events get non-zero probability. / 重新分配概率质量使未见事件获得非零概率。 |
| Perplexity（困惑度） | LM quality metric / LM 质量指标 | `exp(-average log-prob)` on held-out data. Lower is better. / 留出数据上的 `exp(-平均对数概率)`。越低越好。 |
| Backoff（回退） | Fallback to shorter context / 回退到更短上下文 | If trigram count is zero, use bigram. Katz backoff formalizes this. / 如果三元组计数为零，使用二元组。Katz 回退将其形式化。 |
| Kneser-Ney | Best smoothing for n-grams / 最佳 n-gram 平滑 | Absolute discounting + continuation probability for the lower-order model. / 绝对折扣 + 低阶模型的续接概率。 |
| Continuation probability（续接概率） | KN-specific / KN 特有 | `P(w)` weighted by number of contexts `w` appears in, not by raw count. / `P(w)` 按 `w` 出现的上下文数量加权，而非原始计数。 |

> **【中文解读】**延伸阅读 cung cấp các nguồn chất lượng cao cho việc học sâu. Những bài báo và giảng dạy này là tài liệu tham khảo cổ điển trong lĩnh vực này, phù hợp với những người đọc cần hiểu sâu hơn.

## Xem thêm 延伸阅读

- [Jurafsky and Martin — Speech and Language Processing, Chapter 3 (2026 draft)](https://web.stanford.edu/~jurafsky/slp3/3.pdf) điều trị theo quy luật của n-gram LM và làm trơn. / n-gram 语言模型和平滑的经典教材。
- [Chen and Goodman (1998). An Empirical Study of Smoothing Techniques for Language Modeling](https://dash.harvard.edu/handle/1/25104739) bài báo đã định nghĩa Kneser-Ney là tốt nhất n-gram smoother. / 确定 Kneser-Ney 为最佳 n-gram 平滑器的论文──
- [Kneser and Ney (1995). Improved Backing-off for M-gram Language Modeling](https://ieeexplore.ieee.org/document/479394) giấy KN gốc. / 原始 KN 论文。
- [KenLM](https://kheafield.com/code/kenlm/) sản xuất nhanh n-gram LM, vẫn được sử dụng vào năm 2026 cho các ứng dụng nhạy cảm với độ trễ. / 快速生产级 n-gram 语言模型,2026年仍用于延迟敏感应用──
| N-gram | Word sequence | Sequence of `n` consecutive tokens. |
| Smoothing | Avoiding zeros | Reallocating probability mass so unseen events get non-zero probability. |
| Perplexity | LM quality metric | `exp(-average log-prob)` on held-out data. Lower is better. |
| Backoff | Fallback to shorter context | If trigram count is zero, use bigram. Katz backoff formalizes this. |
| Kneser-Ney | Best smoothing for n-grams | Absolute discounting + continuation probability for the lower-order model. |
| Continuation probability | KN-specific | `P(w)` weighted by number of contexts `w` appears in, not by raw count. |
| Entropy of text | Information per symbol | Average bits needed to encode the next symbol given the context. Shannon's 1951 estimate for printed English with up to 100 letters of context: 0.6-1.3 bits/letter, measured before any model existed. |

## Đọc thêm

- [Shannon (1951). Prediction and Entropy of Printed English](https://www.princeton.edu/~wbialek/rome/refs/shannon_51.pdf) thí nghiệm trò chơi đoán định nghĩa mục tiêu mà mỗi mô hình ngôn ngữ vẫn tối ưu hóa.
- [Jurafsky and Martin — Speech and Language Processing, Chapter 3 (2026 draft)](https://web.stanford.edu/~jurafsky/slp3/3.pdf) xử lý và làm trơn các LM n-gram theo quy định.
- [Chen and Goodman (1998). An Empirical Study of Smoothing Techniques for Language Modeling](https://dash.harvard.edu/handle/1/25104739)- tờ báo đã xác định Kneser-Ney là tốt nhất n-gram smoother.
- [Kneser and Ney (1995). Improved Backing-off for M-gram Language Modeling](https://ieeexplore.ieee.org/document/479394) giấy KN gốc.
- [KenLM](https://kheafield.com/code/kenlm/) sản xuất nhanh n-gram LM, vẫn được sử dụng vào năm 2026 cho các ứng dụng nhạy cảm với độ trễ.
