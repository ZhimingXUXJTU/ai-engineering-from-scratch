# Bag of Words, TF-IDF, và Text Representation 词袋模型、TF-IDF 与文本表示

> TF-IDF vẫn đánh bại các nhiệm vụ được xác định rõ ràng vào năm 2026.
> Trước tiên tính toán, sau khi suy nghĩ. Trong nhiệm vụ xác định rõ ràng, TF-IDF đến năm 2026 vẫn thắng được.

> **【中文解读】**词袋模型忽略词序只统计词频,TF-IDF 通过惩罚常见词突出关键词――这是最基础的文本表示方法――

**Type:** Build | **类型:** 动手
**Languages:** Python | **语言:** Python
**Prerequisites:** Phase 5 · 01 (Text Processing), Phase 2 · 02 (Linear Regression from Scratch) | **前置知识:** Phase 5 · 01（文本处理），Phase 2 · 02（线性回归从零实现）
**Time:** ~75 minutes | **时间:** ~75 分钟

## Mục tiêu học tập

- Xây dựng các biểu tượng từ đầu của các túi từ và TF-IDF
  Từ零构建词袋模型和 TF-IDF biểu hiện
- Hiểu các vector hiếm, tần suất thuật ngữ và tần suất tài liệu ngược
  hiểu hiếm疏向量、词频和逆文档频率
- Sử dụng CountVectorizer và TfidfVectorizer của scikit-learn trong sản xuất
  Trong sản xuất sử dụng scikit-learn của CountVectorizer và TfidfVectorizer
- Biết khi nào TF-IDF thắng trên các nhúng và khi nào nó thất bại
  知道TF-IDF何时胜过嵌入,何时失败

## Vấn đề  vấn đề giới thiệu

Mô hình cần số, anh có dây.

> 模型需要数字──你的手上的是字符串──

Mỗi đường ống NLP phải trả lời cùng một câu hỏi. Làm thế nào để biến một dòng token dài biến thành một vector kích thước cố định mà một trình phân loại có thể tiêu thụ. Câu trả lời đầu tiên mà trường đáp lại là câu trả lời ngu ngốc nhất.

> Mỗi dòng chảy của NLP đều phải trả lời cùng một câu hỏi: làm thế nào để biến đổi token 流 thành khối lượng lớn cố định, để phân loại có thể tiêu thụ.

Dòng vector đó đã mang lại nhiều NLP sản xuất hơn bất kỳ mô hình nhúng nào. Trình lọc spam, phân loại chủ đề, phát hiện bất thường nhật ký, xếp hạng tìm kiếm (trước BM25), làn sóng đầu tiên của phân tích cảm xúc, thập kỷ đầu tiên của các tiêu chuẩn NLP học thuật. 2026 các học viên vẫn tiếp cận nó trước tiên trong các nhiệm vụ phân loại hẹp. Nó nhanh chóng, có thể giải thích và thường không thể phân biệt với mô hình tích hợp các tham số 400M trong các nhiệm vụ mà sự hiện diện của từ ngữ là điều quan trọng.

> Việc sản xuất NLP mang khối lượng này  áp dụng nhiều hơn bất kỳ mô hình nhúng nào ∙ phân loại thư rác ∙ phân loại chủ đề                                                                                                                                                                                                                                              

Bài học này xây dựng túi từ, sau đó là TF-IDF, từ đầu. sau đó cho thấy scikit-learn làm điều tương tự trong ba dòng. sau đó đặt tên chế độ thất bại khiến bạn tìm kiếm các bản nhúng.

> Bài học này bắt đầu từ mô hình từ zero, sau đó xây dựng TF-IDF, sau đó cho thấy cách học nhỏ bằng cách sử dụng 3 bộ mã hóa để làm điều tương tự.

## Khái niệm cốt lõi

> **【中文解读】**Bài viết này giới thiệu các khái niệm và lý thuyết cốt lõi.

**Bag of Words (BoW)**cho mỗi tài liệu, đếm bao nhiêu lần mỗi từ vựng xuất hiện. chiều dài vector là kích thước từ vựng. vị trí `i`là số từ `i`- Tôi không biết.

> **词袋模型（Bag of Words, BoW）**抛弃顺序――对每文档,统计每词表词出现的次数――向量长度是词表大小――位置`i` 是词 `i`Số lượng:

**TF-IDF**Một từ xuất hiện trong mọi tài liệu là không thông tin, vì vậy hãy giảm nó. Một từ hiếm trên toàn bộ bộ các tập hợp nhưng thường xuyên trong một tài liệu là tín hiệu, vì vậy hãy tăng nó.

> **TF-IDF**Đối với BoW 重新加权. Từ trong mỗi tài liệu hiện không có lượng thông tin, do đó giảm trọng lượng của nó.

```
TF-IDF(w, d) = TF(w, d) * IDF(w)
             = count(w in d) / |d| * log(N / df(w))
```

Ở đâu `TF`là tần số thuật ngữ trong tài liệu, `df`là tần số tài liệu (nhiều tài liệu bao nhiêu chứa từ),`N`là tổng số tài liệu.`log`giữ trọng lượng giới hạn cho các từ ở khắp mọi nơi.

> Trong số đó `TF`là trong văn kiện từ频,`df`là văn bản thường xuyên ((有多少文档包含这个词),`N`Đó là tổng số tài liệu.`log`Để quyền giữ trọng lượng của từ không có ở đâu có giới hạn.

Cấu trúc: cả hai tạo ra các vector hiếm có với trục giải thích. Bạn có thể xem trọng lượng của một phân loại được đào tạo và đọc những từ đẩy một tài liệu hướng tới mỗi lớp. Bạn không thể làm điều này với một nhúng BERT 768 chiều.

> 关键特性: cả hai đều tạo ra một khối lượng hiếm có có thể giải thích. Bạn có thể xem trọng lượng của phân loại được đào tạo tốt, đọc ra những từ nào sẽ đưa tài liệu đến mỗi loại. Bạn không thể sử dụng BERT 768 维 để lắp đặt điều này.

> **【拓展：大语言模型的工程实践】**Từ GPT đến ChatGPT, NLP đã trải qua sự chuyển đổi từ "mỗi nhiệm vụ đào tạo một mô hình" đến "một mô hình giải quyết tất cả các nhiệm vụ". Trong công trình thực tế, việc triển khai LLM cần phải xem xét các vấn đề như: giới hạn token, trì hoãn, chi phí, kiểm tra an toàn, và các vấn đề khác.

> **【拓展：RAG 与企业知识库】**检索增强生成(RAG) là cấu trúc phổ biến nhất trong ứng dụng AI của doanh nghiệp hiện tại: sẽ truy vấn người dùng trước tiên truy vấn các đoạn tài liệu liên quan, tiếp tục truy vấn kết quả như trên dưới đây cho LLM 生成答案──

> **【拓展：NLP 的多语言挑战】**Trên toàn cầu có hơn 7000 ngôn ngữ, nhưng nghiên cứu về NLP tập trung chủ yếu vào tiếng Anh và một số ít ngôn ngữ.

## Hãy xây dựng nó.

> **【中文解读】**本节通过代码实现核心算法从零――这种" từ đầu"的方式能帮助理解框架背后的原理,遇到问题时不会被黑盒困住――
```figure
bow-tfidf
```

## Hãy xây dựng nó

### Bước 1: xây dựng từ vựng

```python
def build_vocab(docs):
    vocab = {}
    for doc in docs:
        for token in doc:
            if token not in vocab:
                vocab[token] = len(vocab)
    return vocab
```

Nhập: danh sách các tài liệu được token hóa (bất kỳ token level nào sẽ làm được; `code/main.py`trong bài học này sử dụng một biến thể chữ nhỏ đơn giản).`{word: index}`Thiết lập lệnh nhập ổn định nghĩa là chữ index 0 là từ đầu tiên được nhìn thấy trong tài liệu đầu tiên.

> 输入:token 化的文档列表(任何词级分词器都可以;本课的 `code/main.py`Sử dụng đơn giản hóa bỏ qua (output:`{word: index}`字典──稳定的插入顺序 nghĩa là từ chỉ mục 0 là từ đầu tiên được thấy trong các tài liệu.

### Bước 2: túi từ

```python
def bag_of_words(docs, vocab):
    matrix = [[0] * len(vocab) for _ in docs]
    for i, doc in enumerate(docs):
        for token in doc:
            if token in vocab:
                matrix[i][vocab[token]] += 1
    return matrix
```

```python
>>> docs = [["cat", "sat", "on", "mat"], ["cat", "cat", "ran"]]
>>> vocab = build_vocab(docs)
>>> bag_of_words(docs, vocab)
[[1, 1, 1, 1, 0], [2, 0, 0, 0, 1]]
```

Các hàng là tài liệu, cột là chỉ số từ vựng.`[i][j]`là "tôi bao nhiêu lần từ `j`xuất hiện trong tài liệu `i`. " Doc 1 đã có `cat`2 lần vì nó đã làm.`ran`không lần vì nó không làm.

> 行是文档──列是词表索引──条目 `[i][j]`là "词 `j`Trong tài liệu`i`Trong đó có bao nhiêu lần xuất hiện.`cat`Vì nó đã xuất hiện hai lần.`ran`Vì nó không xuất hiện.

### Bước 3: Tần suất thuật ngữ và tần suất tài liệu

```python
import math


def term_frequency(doc_bow, doc_length):
    return [c / doc_length if doc_length else 0 for c in doc_bow]


def document_frequency(bow_matrix):
    df = [0] * len(bow_matrix[0])
    for row in bow_matrix:
        for j, count in enumerate(row):
            if count > 0:
                df[j] += 1
    return df


def inverse_document_frequency(df, n_docs):
    return [math.log((n_docs + 1) / (d + 1)) + 1 for d in df]
```

Hai thủ thuật làm trơn đáng để đặt tên.`(n+1)/(d+1)`tránh `log(x/0)`- Đường sau`+1`đảm bảo một từ trong mỗi tài liệu vẫn có IDF 1 (không phải 0), phù hợp với mặc định của scikit-learn.`log(N/df)`Cả hai đều hoạt động, phiên bản trơn hơn là thân thiện hơn.

> Hai kỹ thuật đơn giản đáng chú ý.`(n+1)/(d+1)`避免 `log(x/0)`ᅳ尾部的`+1`确保 xuất hiện trong mỗi tài liệu từ IDF vẫn là 1( thay vì 0), phù hợp với giá trị mặc định của scikit-learn.`log(N/df)`两种都有效;平滑版本更友好

### Bước 4: TF-IDF

```python
def tfidf(bow_matrix):
    n_docs = len(bow_matrix)
    df = document_frequency(bow_matrix)
    idf = inverse_document_frequency(df, n_docs)
    out = []
    for row in bow_matrix:
        length = sum(row)
        tf = term_frequency(row, length)
        out.append([tf_j * idf_j for tf_j, idf_j in zip(tf, idf)])
    return out
```

```python
>>> docs = [
...     ["the", "cat", "sat"],
...     ["the", "dog", "sat"],
...     ["the", "cat", "ran"],
... ]
>>> vocab = build_vocab(docs)
>>> bow = bag_of_words(docs, vocab)
>>> tfidf(bow)
```

Ba tài liệu, năm từ ngữ (`the`- `cat`- `sat`- `dog`- `ran` ).`the`xuất hiện trong cả ba, vì vậy IDF của nó là thấp. `dog`xuất hiện trong một, do đó IDF của nó là cao. Các vector là hiếm (những mục nhập lớn nhất là nhỏ) và các từ phân biệt đối xử pop.

> 三文档,五个词表词(`the``cat``sat``dog``ran`(■)`the`Trong tất cả ba tài liệu đều xuất hiện, vì vậy IDF của nó rất thấp.`dog`Chỉ xuất hiện trong một tài liệu, vì vậy IDF của nó rất cao.

### Bước 5: L2- bình thường hóa hàng

```python
def l2_normalize(matrix):
    out = []
    for row in matrix:
        norm = math.sqrt(sum(x * x for x in row))
        out.append([x / norm if norm else 0 for x in row])
    return out
```

> **【中文解读】**Bài này sẽ trình bày cách sử dụng một khung đã phát triển như PyTorch, HuggingFace, và các khác.

Nếu không có bình thường hóa, một tài liệu dài hơn sẽ có một vector lớn hơn và thống trị điểm tương đồng. bình thường hóa L2 đặt mọi tài liệu trên siêu cầu đơn vị. Sự tương đồng cosine giữa các hàng bây giờ chỉ là một sản phẩm điểm.

> Không hợp nhất, các tập tin dài hơn sẽ có khối lượng lớn hơn và chủ yếu là điểm tương tự. L2 hợp nhất sẽ đặt mỗi tập tin trên một đơn vị siêu cầu.

> **【拓展：Prompt Engineering 与 LLM 应用】**Kỹ thuật nhanh chóng đã trở thành kỹ năng cốt lõi của các kỹ sư NLP. Từ Zero-shot đến Few-shot, từ Chain-of-Thought đến ReAct, các chiến lược khác nhau áp dụng cho các tình huống khác nhau. Trong các dự án thực tế, thiết kế của System提示(System Prompt) ảnh hưởng trực tiếp đến sự ổn định và chất lượng sản xuất của ứng dụng LLM.

## Hãy sử dụng nó để thực hiện

Scikit-learn sẽ đưa ra phiên bản sản xuất.

> Scikit-learn  cung cấp phiên bản cấp sản xuất.

```python
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer

docs = ["the cat sat on the mat", "the dog sat on the mat", "the cat ran"]

bow_vectorizer = CountVectorizer()
bow = bow_vectorizer.fit_transform(docs)
print(bow_vectorizer.get_feature_names_out())
print(bow.toarray())

tfidf_vectorizer = TfidfVectorizer()
tfidf = tfidf_vectorizer.fit_transform(docs)
print(tfidf.toarray().round(3))
```

`CountVectorizer`làm tokenization, từ vựng, và BoW trong một cuộc gọi. `TfidfVectorizer`Thêm trọng lượng IDF và bình thường hóa L2. Cả hai đều trả lại các matrix mỏng. Đối với 100k tài liệu, phiên bản dày đặc không phù hợp với bộ nhớ; giữ mỏng cho đến khi phân loại yêu cầu dày đặc.

> `CountVectorizer`Trong một lần调用中完成分词、构建词表和 BoW。`TfidfVectorizer`增加 IDF 加权和 L2 归结──两者都回归稀疏矩阵── đối với 100.000 bài viết, phiên bản mật khẩu được lưu trữ; trong phân loại 要求密集之前保持稀疏──

Những nút mà thay đổi mọi thứ:

> 改变一切的关键参数:

| Arg | Effect | 参数 | 效果 |
|-----|--------|------|------|
| `ngram_range=(1, 2)` | Include bigrams. Usually boosts classification. | `ngram_range=(1, 2)` | 包含二元组。通常提升分类效果。 |
| `min_df=2` | Drop words in fewer than 2 docs. Trims vocabulary on noisy data. | `min_df=2` | 丢弃出现在少于 2 个文档中的词。在噪声数据上修剪词表。 |
| `max_df=0.95` | Drop words in more than 95% of docs. Approximates stopword removal without a hardcoded list. | `max_df=0.95` | 丢弃出现在超过 95% 文档中的词。近似停用词去除，无需硬编码列表。 |
| `stop_words="english"` | scikit-learn's builtin stopword list. Task-dependent — sentiment analysis should *not* drop negations. | `stop_words="english"` | scikit-learn 内置停用词列表。因任务而异——情感分析不应去除否定词。 |
| `sublinear_tf=True` | Use `1 + log(tf)` instead of raw `tf`. Helps when a term repeats many times in one doc. | `sublinear_tf=True` | 使用 `1 + log(tf)` 代替原始 `tf`。当一个词在一个文档中重复多次时有帮助。 |

### Khi TF-IDF vẫn thắng (từ 2026)

- Phát hiện spam, đánh dấu chủ đề, đánh dấu bất thường nhật ký.
  垃圾邮件检测、主题标签、日志异常标签──词的存在与否是关键;语义细微差不重要──
- Các chế độ dữ liệu thấp (chỉ trăm ví dụ được dán nhãn). TF-IDF cộng với sự lùi hậu cần không có chi phí trước khi đào tạo.
  低数据场景(100标注样本) ――TF-IDF 加逻辑回归没有预训成本――
- Bất cứ nơi nào thời gian trễ quan trọng. TF-IDF cộng với mô hình tuyến tính trả lời trong microsecond. Nhập một tài liệu thông qua một biến thể mất 10-100ms.
  Bất kỳ trường hợp nhạy cảm chậm trễ nào. Thời gian phản ứng của mô hình đường dẫn là từng giây nhỏ.
- Hệ thống phải giải thích dự đoán của họ kiểm tra các hệ số phân loại từ tích cực cao là lý do.
  需要解释预测结果的系统──检查分类器的系数──排名最高正权重词就是原因──

### Khi TF-IDF thất bại

Sự thất bại về mù ngữ học. Hãy xem xét hai tài liệu này:

> 语义盲点──考虑以下两个文档:

- "Trong phim không tốt cả".
- "Tác phẩm phim rất tuyệt vời".

Một là một đánh giá tiêu cực, một là tích cực, sự chồng chéo giữa TF và IDF của họ chính xác`{the, movie, was}`Một người phân loại từ phải ghi nhớ từ đó`not`gần `good`Nó có thể học được điều này với đủ dữ liệu, nhưng không bao giờ như một mô hình hiểu tổng hợp.

> Một là đánh giá tiêu cực, một là đánh giá xác nhận.`{the, movie, was}`                                                                                                                                                                                                                                                              `good` gần `not`Trong đủ dữ liệu nó có thể học được điều này, nhưng sẽ không bao giờ được đẹp như một mô hình hiểu biết về pháp ngữ.

Sự thất bại khác: từ ngoài từ vựng khi suy luận. Một mô hình BoW được đào tạo trên đánh giá IMDb không biết phải làm gì với `Zoomer-approved`Nếu token đó không xuất hiện trong đào tạo. Subword Embeddings (đọc 04) xử lý điều này. TF-IDF không thể.

> 另一个失败:推理时的词表外(Out-of-Vocabulary, OOV)词──在 IMDb 评论上训练的 BoW 模型不知道如何处理 `Zoomer-approved`, Nếu token này không xuất hiện trong tập luyện.

### Hybrid: Thiết bị nhúng trọng TF-IDF

Các mặc định thực tế năm 2026 cho phân loại dữ liệu trung bình: sử dụng trọng lượng TF-IDF như sự chú ý hơn so với việc nhúng từ.

> 2026 năm trung bình phân loại dữ liệu: sử dụng TF-IDF 权重作为词嵌入的注意力──

```python
def tfidf_weighted_embedding(doc, tfidf_scores, embedding_table, dim):
    vec = [0.0] * dim
    total_weight = 0.0
    for token in doc:
        if token not in embedding_table or token not in tfidf_scores:
            continue
        weight = tfidf_scores[token]
        emb = embedding_table[token]
        for i in range(dim):
            vec[i] += weight * emb[i]
        total_weight += weight
    if total_weight == 0:
        return vec
    return [v / total_weight for v in vec]
```

> **【中文解读】**Phần này tập trung vào cách phân phối mô hình như một sản phẩm có thể sử dụng.

Bạn có được khả năng ngữ nghĩa từ nhúng, và nhấn mạnh từ hiếm từ từ TF-IDF. Classifier đào tạo trên vector tập hợp. Điều này vượt qua một mình cho tình cảm, chủ đề và định mệnh phân loại dưới khoảng 50k ví dụ được dán nhãn.

> Bạn có được khả năng ngữ nghĩa từ nhúng, từ TF-IDF  nhận được những từ hiếm nhấn mạnh.

## Chuyển nó đi.

Cứ như `outputs/prompt-vectorization-picker.md`- Có thể là:

```markdown
---
name: vectorization-picker
description: Given a text-classification task, recommend BoW, TF-IDF, embeddings, or a hybrid.
phase: 5
lesson: 02
---

You recommend a text-vectorization strategy. Given a task description, output:

1. Representation (BoW, TF-IDF, transformer embeddings, or a hybrid). Explain why in one sentence.
2. Specific vectorizer configuration. Name the library. Quote the arguments (`ngram_range`, `min_df`, `max_df`, `sublinear_tf`, `stop_words`).
3. One failure mode to test before shipping.

Refuse to recommend embeddings when the user has under 500 labeled examples unless they show evidence of semantic failure in a TF-IDF baseline. Refuse to remove stopwords for sentiment analysis (negations carry signal). Flag class imbalance as needing more than a vectorizer change.

Example input: "Classifying 30k customer support tickets into 12 categories. Most tickets are 2-3 sentences. English only. Need explainability for audit logs."

Example output:

- Representation: TF-IDF. 30k examples is not small; explainability requirement rules out dense embeddings.
- Config: `TfidfVectorizer(ngram_range=(1, 2), min_df=3, max_df=0.95, sublinear_tf=True, stop_words=None)`. Keep stopwords because category keywords sometimes are stopwords ("not working" vs "working").
- Failure to test: verify `min_df=3` does not drop rare category keywords. Run `get_feature_names_out` filtered by class and eyeball.
```

## Tập luyện bài tập

1. **Easy.**Thực hiện`cosine_similarity(doc_vec_a, doc_vec_b)`trên các output TF-IDF chuẩn hóa L2. Kiểm tra rằng các tài liệu giống hệt có điểm số 1.0 và các tài liệu từ vựng không liên kết có điểm số 0.0.
   **简单。**Trong L2 归结的TF-IDF 输出实现 `cosine_similarity(doc_vec_a, doc_vec_b)`▽验证 cùng tài liệu điểm số là 1.0, từ表 hoàn toàn không tương quan
2. **Medium.**Thêm `n-gram`hỗ trợ`bag_of_words`- Parameter`n`tạo ra số lượng hơn `n`- Thử thử.`n=2``["the", "cat", "sat"]`tạo ra số lượng lớn cho `["the cat", "cat sat"]`- Tôi không biết.
   **中等。**Vì vậy`bag_of_words`添加 `n-gram`支持──参数 `n` tạo ra `n`-gram của tính toán.`n=2`时 `["the", "cat", "sat"]`产生二元组 `["the cat", "cat sat"]`Số lượng:
3. **Hard.**Xây dựng bộ lắp ráp hợp chất TF-IDF cân nặng trên bằng cách sử dụng các vector GloVe 100d (tải xuống một lần, cache). So sánh độ chính xác phân loại với TF-IDF đơn giản và các bản lắp ráp trung bình đơn giản trên bộ dữ liệu 20 Newsgroups.
   **困难。**Sử dụng GloVe 100 维向量 (download once并缓存) xây dựng các chương trình hỗn hợp TF-IDF 加权嵌入混合方案── trên 20 Newsgroups dữ liệu tập hợp so sánh tỷ lệ độ chính xác, so sánh với các đơn thuần TF-IDF và đơn thuần trung bình giá trị tích hợp嵌入── báo cáo trong đó có những gì đã thành công──

> **【中文解读】**练题按照 Easy/Medium/Hard 三个难度递进;;建议至少完成 级别的题目, 级别适合深入研究或面试准备;;

## Từ khóa  Từ khóa nhanh chóng

| Term | What people say | What it actually means | 术语 | 人们常说的 | 实际含义 |
|------|-----------------|-----------------------|------|-----------|---------|
| BoW | Word frequency vector | Counts of vocabulary words in one document. Throws away order. | BoW（词袋模型） | 词频向量 | 一个文档中词表词的计数。抛弃顺序。 |
| TF | Term frequency | Count of a word in a document, optionally normalized by document length. | TF（词频） | 词频 | 一个词在文档中的计数，可选按文档长度归一化。 |
| DF | Document frequency | Count of documents containing the word at least once. | DF（文档频率） | 文档频率 | 至少包含该词一次的文档计数。 |
| IDF | Inverse document frequency | `log(N / df)` smoothed. Downweights words that appear everywhere. | IDF（逆文档频率） | 逆文档频率 | 经平滑的 `log(N / df)`。降低到处出现的词的权重。 |
| Sparse vector | Mostly zeros | Vocabulary is typically 10k-100k words; most are absent from any given document. | 稀疏向量 | 大部分为零 | 词表通常有 1 万到 10 万个词；大多数在任何给定文档中都不出现。 |
| Cosine similarity | Vector angle | Dot product of L2-normalized vectors. 1 is identical, 0 is orthogonal. | 余弦相似度 | 向量夹角 | L2 归一化向量的点积。1 表示相同，0 表示正交。 |

> **【中文解读】**Trong 术语表中的"Những gì mọi người nói" vs "Những gì nó thực sự có nghĩa" 区分日常口语和精确技术含义── 在团队协作中,统一术语定义可以避免大量沟通误解──

## Xem thêm 延伸阅读

- [scikit-learn — feature extraction from text](https://scikit-learn.org/stable/modules/feature_extraction.html#text-feature-extraction) tham chiếu API theo quy định, cộng với ghi chú trên mỗi nút. / 权威 API 参考,以及每个参数的说明──
- [Salton, G., & Buckley, C. (1988). Term-weighting approaches in automatic text retrieval](https://www.sciencedirect.com/science/article/pii/0306457388900210) bài báo đã làm cho TF-IDF mặc định trong một thập kỷ. / 使 TF-IDF 成为十年默认方案的论文──
- ["Why TF-IDF Still Beats Embeddings" — Ashfaque Thonikkadavan (Medium)](https://medium.com/@cmtwskb/why-tf-idf-still-beats-embeddings-ad85c123e1b2) 2026 hãy bắt đầu khi nào phương pháp cũ thắng và tại sao. / 2026 年对旧方法何时胜出以及为什么的观点──
