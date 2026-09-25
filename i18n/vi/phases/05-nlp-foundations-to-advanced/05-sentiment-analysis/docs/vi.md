# Phân tích cảm xúc

> Nhiệm vụ NLP theo quy luật. Hầu hết những gì bạn cần biết về phân loại văn bản cổ điển được hiển thị ở đây.
> Các nhiệm vụ NLP cổ điển nhất... phần lớn những gì bạn cần biết đều ở đây...

> **【中文解读】**判断文本的情感倾向──是NLP最经典的分类任务之一──

**Type:** Build | **类型:** 动手
**Languages:** Python | **语言:** Python
**Prerequisites:** Phase 5 · 02 (BoW + TF-IDF), Phase 2 · 14 (Naive Bayes) | **前置知识:** Phase 5 · 02（BoW + TF-IDF），Phase 2 · 14（朴素贝叶斯）
**Time:** ~75 minutes | **时间:** ~75 分钟

## Vấn đề  vấn đề giới thiệu

"Món ăn không ngon lắm". Tốt hay xấu?

> "Món ăn không tuyệt vời". 正面还是负面?

Một nhà phê bình nói rằng họ thích hoặc không thích một thứ gì đó. Đánh dấu câu. Lý do nó trở thành nhiệm vụ NLP công giáo là mỗi trường hợp dễ nhìn ẩn một trường hợp khó khăn. Phản ứng đảo chiều ý nghĩa. Sự khinh bỉ đảo ngược nó. "Không tệ chút nào" là tích cực mặc dù hai từ có mã âm. Emoji mang theo nhiều tín hiệu hơn văn bản xung quanh.`tight`trong bài đánh giá âm nhạc`tight`trong cuộc xem xét thời trang).

> 情感分析听起来简单――评论员说喜欢或不喜欢什么――标记句子――它之所以成为经典的NLP 任务,是因为每个看似简单的案例背后都隐藏着一个困难的案例――否定翻转含义――刺反转含义――"Không tệ chút nào" Mặc dù có hai từ mã âm, nhưng là thẳng thắn――表符号带着更多信号比周围文本――领域词汇很重要(在音乐评论中`tight`Trong khi đó,`tight`(■)

Sentiment là một phòng thí nghiệm làm việc cho NLP cổ điển. Nếu bạn hiểu tại sao mỗi dòng cơ sở ngây thơ có một chế độ thất bại cụ thể, bạn sẽ hiểu tại sao mọi mô hình giàu có hơn đã được phát minh ra. Bài học này xây dựng một dòng cơ sở Bayes ngây thơ từ đầu, thêm sự lùi lại hậu cần, và đặt tên những cái bẫy làm cho tình cảm sản xuất trở thành vấn đề cấp độ tuân thủ.

> 情感分析 là phòng thí nghiệm làm việc của NLP cổ điển. Nếu bạn hiểu tại sao mỗi dòng đơn giản có một mô hình thất bại cụ thể, bạn sẽ hiểu tại sao mỗi loại mô hình phong phú hơn được phát minh ra.

## Khái niệm cốt lõi

> **【中文解读】**Bài viết này giới thiệu các khái niệm và lý thuyết cốt lõi.

Tâm lý cổ điển là một công thức hai bước.

> Phân tích cảm xúc cổ điển là một cách hai bước.

1. **Represent.**Chuyển văn bản thành một vector tính năng.
   **表示。**将文本转换为特征向量──BoW、TF-IDF 或 n-gram──
2. **Classify.**Đưa ra một mô hình tuyến tính (Naive Bayes, sự lùi hậu cần, SVM) trên các ví dụ được dán nhãn.
   **分类。**Trong các mô hình trên các mẫu thẻ được chuẩn bị để phù hợp với mô hình đường thẳng (SVM)

Bayes ngây thơ là mô hình ngu ngốc nhất có thể làm việc.`P(word | positive)`và `P(word | negative)`Trong khi đó, các phương pháp phân loại có thể được sử dụng để phân tích các tính năng của các chữ cái.

> Bây-lê-s là mô hình tốt nhất nhưng có thể sử dụng.`P(word | positive)`和 `P(word | negative)`◊ Quan điểm sẽ tăng tỷ lệ tương đương. ◊ giả định độc lập của "đơn giản" là sai lầm, nhưng kết quả là đáng ngạc nhiên.

Sự lùi hậu cần sửa chữa giả định độc lập. Nó học được trọng lượng cho mỗi tính năng, bao gồm cả trọng lượng âm. `not good`Bayes ngây thơ không thể làm điều đó cho các hình ảnh mà nó chưa bao giờ dán nhãn.

> 逻辑归修复了独立性假设── nó dành cho mỗi đặc điểm học một quyền lực, bao gồm cả quyền lực负──`not good`作为二元组特征获得负权重──朴贝叶斯 đối với hai元组 chưa bao giờ được đánh dấu không làm được điều này──

> **【拓展：大语言模型的工程实践】**Từ GPT đến ChatGPT, NLP đã trải qua sự chuyển đổi từ "mỗi nhiệm vụ đào tạo một mô hình" đến "một mô hình giải quyết tất cả các nhiệm vụ". Trong công trình thực tế, việc triển khai LLM cần phải xem xét các vấn đề như: giới hạn token, trì hoãn, chi phí, kiểm tra an toàn, và các vấn đề khác.

> **【拓展：RAG 与企业知识库】**检索增强生成(RAG) là cấu trúc phổ biến nhất trong ứng dụng AI của doanh nghiệp hiện tại: sẽ truy vấn người dùng trước tiên truy vấn các đoạn tài liệu liên quan, tiếp tục truy vấn kết quả như trên dưới đây cho LLM 生成答案──

> **【拓展：NLP 的多语言挑战】**Trên toàn cầu có hơn 7000 ngôn ngữ, nhưng nghiên cứu về NLP tập trung chủ yếu vào tiếng Anh và một số ít ngôn ngữ.

## Hãy xây dựng nó.

> **【中文解读】**本节通过代码实现核心算法从零――这种" từ đầu"的方式能帮助理解框架背后的原理,遇到问题时不会被黑盒困住――
```figure
sentiment-logits
```

## Hãy xây dựng nó

### Bước 1: một bộ dữ liệu mini thực sự

```python
POSITIVE = [
    "absolutely loved this movie",
    "beautiful cinematography and a great story",
    "one of the best films of the year",
    "brilliant acting from the lead",
    "heartwarming and funny",
]

NEGATIVE = [
    "boring and far too long",
    "not worth your time",
    "the plot made no sense",
    "terrible acting, awful script",
    "i want my two hours back",
]
```

Công việc thực sự sử dụng hàng chục ngàn ví dụ (IMDb, SST-2, độ cực của Yelp).

> Vì vậy, thực tế làm rất nhỏ. Thực tế làm bằng cách sử dụng hàng ngàn mẫu.

### Bước 2: Bayes đa số ngây thơ từ đầu

```python
import math
from collections import Counter


def train_nb(docs_by_class, vocab, alpha=1.0):
    class_priors = {}
    class_word_probs = {}
    total_docs = sum(len(d) for d in docs_by_class.values())

    for cls, docs in docs_by_class.items():
        class_priors[cls] = len(docs) / total_docs
        counts = Counter()
        for doc in docs:
            for token in doc:
                counts[token] += 1
        total = sum(counts.values()) + alpha * len(vocab)
        class_word_probs[cls] = {
            w: (counts[w] + alpha) / total for w in vocab
        }
    return class_priors, class_word_probs


def predict_nb(doc, class_priors, class_word_probs):
    scores = {}
    for cls in class_priors:
        s = math.log(class_priors[cls])
        for token in doc:
            if token in class_word_probs[cls]:
                s += math.log(class_word_probs[cls][token])
        scores[cls] = s
    return max(scores, key=scores.get)
```

Đơn giản hóa phụ gia (alpha = 1.0) là Đơn giản hóa Laplace. Không có nó, một từ không được nhìn thấy trong một lớp có xác suất bằng không và nhật ký nổ ra. `alpha=0.01`là phổ biến trong thực tế. `alpha=1.0`là trường học không được dạy.

> 加法平滑(alpha=1.0) là 拉普拉斯平滑──没有它,一个类别中未见过的词概率为零,log会爆炸──实践中 `alpha=0.01`很常见──`alpha=1.0`Là học tập tiêu chuẩn.

### Bước 3: Khản hồi hậu cần từ đầu

```python
import numpy as np


def sigmoid(x):
    return 1.0 / (1.0 + np.exp(-np.clip(x, -20, 20)))


def train_lr(X, y, epochs=500, lr=0.05, l2=0.01):
    n_features = X.shape[1]
    w = np.zeros(n_features)
    b = 0.0
    for _ in range(epochs):
        logits = X @ w + b
        preds = sigmoid(logits)
        err = preds - y
        grad_w = X.T @ err / len(y) + l2 * w
        grad_b = err.mean()
        w -= lr * grad_w
        b -= lr * grad_b
    return w, b


def predict_lr(X, w, b):
    return (sigmoid(X @ w + b) >= 0.5).astype(int)
```

L2 điều chỉnh quan trọng ở đây. các tính năng văn bản là hiếm; mà không có L2 mô hình ghi nhớ các ví dụ đào tạo.`0.01`và âm thanh.

> L2 chính thức hóa ở đây rất quan trọng.`0.01`开始调参。

### Bước 4: xử lý từ chối (cơ chế thất bại)

Hãy xem xét "không tốt" và "không xấu". Một phân loại BoW thấy `{not, good}`và `{not, bad}`và học hỏi từ những người xuất hiện nhiều hơn trong huấn luyện.`not_good`và `not_bad`Và nó học được những đặc điểm khác nhau.

> 考虑 "không tốt" 和 "không xấu"──BoW 分类器看 `{not, good}`和 `{not, bad}`, tùy thuộc vào việc đào tạo nào xuất hiện nhiều hơn để học.`not_good`和 `not_bad`作为不同特征学习──这通常就够了──

Một phương pháp khắc phục khó khăn hơn có hiệu quả khi bạn không có bigram: **negation scoping**. Đơn vị tiền ký sau từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ`NOT_`cho đến dấu chấm tiếp theo.

> Một sửa chữa thô hơn nhưng có hiệu lực trong không có 2元组时:**否定范围标记**                                                                                                                                                                                                                                                              `NOT_`Trước, cho đến khi một dấu hiệu khác đi.

```python
NEGATION_WORDS = {"not", "no", "never", "nor", "none", "nothing", "neither"}
NEGATION_TERMINATORS = {".", "!", "?", ",", ";"}


def apply_negation(tokens):
    out = []
    negate = False
    for token in tokens:
        if token in NEGATION_TERMINATORS:
            negate = False
            out.append(token)
            continue
        if token in NEGATION_WORDS:
            negate = True
            out.append(token)
            continue
        out.append(f"NOT_{token}" if negate else token)
    return out
```

```python
>>> apply_negation(["not", "good", "at", "all", ".", "but", "funny"])
['not', 'NOT_good', 'NOT_at', 'NOT_all', '.', 'but', 'funny']
```

Giờ thì`good`và `NOT_good`3 dòng xử lý trước, độ chính xác có thể đo lường nhảy trên các điểm chuẩn cảm xúc.

> 现在 `good`和 `NOT_good`Các phân loại có thể cung cấp cho chúng trọng lượng ngược lại.

### Bước 5: Các số liệu đánh giá quan trọng

Sự chính xác đơn độc là sai lầm nếu các lớp không cân bằng. Các quan điểm cảm xúc thực sự thường là 70-80% tích cực hoặc 70-80% tiêu cực; một phân loại đa số liên tục có độ chính xác 80% và không có giá trị.

> Nếu các phân loại không cân bằng, chỉ có tỷ lệ xác định sẽ gây ra sai lầm. Các ngôn ngữ cảm xúc thực thường là 70-80% là tích cực hoặc 70-80% là tiêu cực. Một số lượng thường xuyên đa số phân loại có thể đạt được tỷ lệ xác định 80% nhưng không có giá trị.

- **Per-class precision and recall.**Một cặp cho mỗi lớp, và phân tích chúng để có được một số duy nhất tôn trọng sự cân bằng của lớp.
  **每类精确率和召回率。**Mỗi loại một đối số.
- **Macro-F1 (primary metric for imbalanced data).**Tỷ lệ trung bình điểm F1 cho mỗi lớp, cân nặng bằng nhau. Sử dụng nó thay vì độ chính xác khi các lớp không cân bằng.
  **Macro-F1（不平衡数据的主要指标）。**Giá trị trung bình của các phân số F1 khác nhau, bằng trọng lượng.
- **Weighted-F1 (alternative).**Tương tự như macro nhưng cân nặng theo tần số lớp. báo cáo cùng với macro-F1 khi sự mất cân bằng có ý nghĩa kinh doanh.
  **Weighted-F1（替代方案）。**Khi không cân bằng có ý nghĩa kinh doanh, báo cáo với Macro-F1
- **Confusion matrix.**Luôn kiểm tra trước khi tin tưởng bất kỳ métric scalar nào; nó cho thấy cặp lớp nào mô hình nhầm lẫn.
  **混淆矩阵。**Trong khi đó, các mô hình được phân loại là:
- **Per-class error samples.**Hãy rút ra 5 dự đoán sai lầm cho mỗi lớp học. Hãy đọc chúng. Không gì thay thế việc đọc sai lầm thực tế.
  **每类错误样本。**Mỗi loại rút ra 5 sai lầm dự đoán. Đọc chúng. Không có gì có thể thay thế đọc sai lầm thực tế.

Đối với dữ liệu mất cân bằng nghiêm trọng (> tỷ lệ 95-5), báo cáo **AUROC**và **AUPRC**AUPRC nhạy cảm hơn với tầng lớp thiểu số, đó là điều bạn thường quan tâm (như spam, gian lận, cảm xúc hiếm hoi).

> 对于严重不平衡的数据 ((> 95-5 比例), báo cáo **AUROC**和 **AUPRC**代替准确率──AUPRC đối với một nhóm thiểu số nhạy cảm hơn, thường là bạn quan tâm đến 垃圾邮件、欺诈、罕见情感)

**Common bug to avoid.**Báo cáo micro-F1 thay vì macro-F1 trên dữ liệu không cân bằng cung cấp một số có vẻ cao bởi vì nó bị chi phối bởi lớp đa số.

> **常见错误。**Trong dữ liệu không cân bằng, báo cáo micro-F1 thay vì macro-F1 sẽ cung cấp một con số trông rất cao, vì nó được thống trị bởi đa số các loại.

```python
def evaluate(y_true, y_pred):
    tp = sum(1 for t, p in zip(y_true, y_pred) if t == 1 and p == 1)
    fp = sum(1 for t, p in zip(y_true, y_pred) if t == 0 and p == 1)
    fn = sum(1 for t, p in zip(y_true, y_pred) if t == 1 and p == 0)
    tn = sum(1 for t, p in zip(y_true, y_pred) if t == 0 and p == 0)
    precision = tp / (tp + fp) if tp + fp else 0
    recall = tp / (tp + fn) if tp + fn else 0
    f1 = 2 * precision * recall / (precision + recall) if precision + recall else 0
    return {"tp": tp, "fp": fp, "tn": tn, "fn": fn, "precision": precision, "recall": recall, "f1": f1}
```

> **【中文解读】**Bài này sẽ trình bày cách sử dụng một khung đã phát triển như PyTorch, HuggingFace, và các khác.

> **【拓展：Prompt Engineering 与 LLM 应用】**Kỹ thuật nhanh chóng đã trở thành kỹ năng cốt lõi của các kỹ sư NLP. Từ Zero-shot đến Few-shot, từ Chain-of-Thought đến ReAct, các chiến lược khác nhau áp dụng cho các tình huống khác nhau. Trong các dự án thực tế, thiết kế của System提示(System Prompt) ảnh hưởng trực tiếp đến sự ổn định và chất lượng sản xuất của ứng dụng LLM.

## Hãy sử dụng nó để thực hiện

Scikit-learn làm nó trong sáu dòng, đúng.

> Sikit-learn 六行代码搞定,而且正确──

```python
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline

pipe = Pipeline([
    ("tfidf", TfidfVectorizer(ngram_range=(1, 2), min_df=2, sublinear_tf=True, stop_words=None)),
    ("clf", LogisticRegression(C=1.0, max_iter=1000)),
])
pipe.fit(X_train, y_train)
print(pipe.score(X_test, y_test))
```

Ba điều cần chú ý.`stop_words=None`giữ sự phủ nhận. `ngram_range=(1, 2)`thêm các biểu tượng lớn như vậy `not_good`trở thành một tính năng. `sublinear_tf=True`Những dấu hiệu này là sự khác biệt giữa một đường cơ sở chính xác 75% và một đường cơ sở chính xác 85% trên SST-2.

> Có 3 điểm đáng chú ý.`stop_words=None`保留否定词──`ngram_range=(1, 2)`添加二元组使 `not_good`成为特征――`sublinear_tf=True`抑制重复词──Thêm ba dấu hiệu này là sự khác biệt giữa SST-2 trên 75% 准确率基线 và 85% 准确率基线──

### Khi nào để tìm một bộ biến đổi

- Chẩn đoán sự ngạo mạn, mô hình cổ điển thất bại ở đây.
  刺检测──经典模型在这里会失败──无例外──
- Những bài đánh giá dài nơi tình cảm thay đổi giữa tài liệu.
  情感在文档中转变的长评论──
- "Hình ảnh rất tuyệt, nhưng pin rất tệ". Bạn cần phải gán cảm xúc cho các khía cạnh.
  基于方面情感分析――"Hình ảnh rất tuyệt vời nhưng pin rất tệ". 你需要将情感归因到方面――只有变压器或结构化输出模型能做到――
- Các ngôn ngữ không phải tiếng Anh, nguồn lực thấp. BERT đa ngôn ngữ cung cấp cho bạn một đường cơ sở không chụp miễn phí.
  Không tiếng Anh, nguồn lực thấp,... nhiều ngôn ngữ BERT vì bạn miễn phí cung cấp không mẫu nền tảng.

Nếu bạn cần bất kỳ điều gì trên, hãy vượt qua giai đoạn 7 (cấp sâu biến áp). Nếu không, Bayes ngây thơ hoặc sự lùi lại hậu cần trên TF-IDF cộng với các bigram cộng với xử lý phủ nhận là cơ sở sản xuất của bạn vào năm 2026.

> Nếu bạn cần bất kỳ điều gì, nhảy vào giai đoạn 7 (Transformer deep inside) ⋅ nếu không, trong TF-IDF 加二元组加否定处理上的朴素贝叶斯或逻辑回归就是你的2026年生产基线――

### Trầm lẫy tái tạo (một lần nữa)

Việc đào tạo lại các mô hình cảm xúc là thói quen. Việc đánh giá lại chúng không phải là. Số liệu chính xác được báo cáo trong các giấy sử dụng phân chia cụ thể, xử lý trước cụ thể, các mã hóa cụ thể. Nếu bạn so sánh mô hình mới của bạn với một đường cơ sở mà không sử dụng đường ống giống nhau, bạn sẽ nhận được các điểm phân tích gây hiểu lầm. Luôn tái tạo đường cơ sở trên đường ống của bạn, chứ không phải số giấy.

> 重新训练情感模型是常规操作――重新评估却不是―― 论文报告的准确率数字使用特定数据划分、特定预处理、特定分词器―― 如果你不使用完全相同的流水线来比较新模型与基线,你会得到误导差值――永远在你的流水线上重新生成基线,而不是用论文中的数字――

> **【中文解读】**Phần này tập trung vào cách phân phối mô hình như một sản phẩm có thể sử dụng.

## Chuyển nó đi.

Cứ như `outputs/prompt-sentiment-baseline.md`- Có thể là:

```markdown
---
name: sentiment-baseline
description: Design a sentiment analysis baseline for a new dataset.
phase: 5
lesson: 05
---

Given a dataset description (domain, language, size, label granularity, latency budget), you output:

1. Feature extraction recipe. Specify tokenizer, n-gram range, stopword policy (usually keep), negation handling (scoped prefix or bigrams).
2. Classifier. Naive Bayes for baseline, logistic regression for production, transformer only if the domain needs sarcasm / aspects / cross-lingual.
3. Evaluation plan. Report precision, recall, F1, confusion matrix, and per-class error samples (not just scalars).
4. One failure mode to monitor post-deployment. Domain drift and sarcasm are the top two.

> **【中文解读】** 练习题按照 Easy/Medium/Hard 三个难度递进。建议至少完成 Medium 级别的题目，Hard 级别适合深入研究或面试准备。

Refuse to recommend dropping stopwords for sentiment tasks. Refuse to report accuracy as the sole metric when classes are imbalanced (e.g., 90% positive). Flag subword-rich languages as needing FastText or transformer embeddings over word-level TF-IDF.
```

## Tập luyện bài tập

1. **Easy.**Thêm `apply_negation`như một bước xử lý trước trong đường ống học scikit và đo đạc F1 delta trên một bộ dữ liệu cảm xúc nhỏ.
   **简单。**sẽ`apply_negation`作为预处理步骤添加到小学流水线中,在一个小情感数据集上测量F1 变化.
2. **Medium.**Thực hiện sự lùi lại hậu cần cân bằng lớp học (thành `class_weight="balanced"`để học scikit-, hoặc lấy gradient tự mình). đo tác động đến sự mất cân bằng lớp 90-10 tổng hợp.
   **中等。**实现类别加权逻辑归归(传递 `class_weight="balanced"`给小学学习,或自导梯度) ⋅ trong tổng hợp 90-10 类别不平衡上测量效果
3. **Hard.**Xây dựng một máy dò khạo báng bằng cách đào tạo một bộ phân loại thứ hai về các dư lượng của mô hình cảm xúc. Tài liệu thiết lập thí nghiệm của bạn. Hãy cảnh báo người đọc khi độ chính xác của bạn thấp hơn sự ngẫu nhiên (thực suất trên khạo báng 2 lớp là ~ 50% và hầu hết các nỗ lực đầu tiên hạ cánh ở đó).
   **困难。**Trong mô hình cảm xúc, tập một bộ phân loại thứ hai để xây dựng một bộ kiểm tra 刺. ghi lại thiết lập thí nghiệm của bạn.

> **【中文解读】**练题按照 Easy/Medium/Hard 三个难度递进;;建议至少完成 级别的题目, 级别适合深入研究或面试准备;;

## Từ khóa  Từ khóa nhanh chóng

| Term | What people say | What it actually means | 术语 | 人们常说的 | 实际含义 |
|------|-----------------|-----------------------|------|-----------|---------|
| Polarity | Positive or negative | Binary label; sometimes extended to neutral or fine-grained (5-star). | 极性（Polarity） | 正面或负面 | 二分类标签；有时扩展到中性或细粒度（5 星）。 |
| Aspect-based sentiment | Per-aspect polarity | Attribute sentiment to specific entities or attributes mentioned in text. | 基于方面的情感分析 | 每个方面的极性 | 将情感归因到文本中提到的特定实体或属性。 |
| Negation scoping | Reversing nearby tokens | Prefix tokens after "not" with `NOT_` until punctuation. | 否定范围标记 | 反转附近的 token | 在 "not" 后给 token 加 `NOT_` 前缀直到标点符号。 |
| Laplace smoothing | Adding 1 to counts | Prevents zero-probability features in Naive Bayes. | 拉普拉斯平滑 | 给计数加 1 | 防止朴素贝叶斯中出现零概率特征。 |
| L2 regularization | Shrinking weights | Adds `lambda * sum(w^2)` to loss. Essential for sparse text features. | L2 正则化 | 缩小权重 | 在损失中添加 `lambda * sum(w^2)`。对稀疏文本特征必不可少。 |

> **【中文解读】**Trong 术语表中的"Những gì mọi người nói" vs "Những gì nó thực sự có nghĩa" 区分日常口语和精确技术含义── 在团队协作中,统一术语定义可以避免大量沟通误解──

## Xem thêm 延伸阅读

- [Pang and Lee (2008). Opinion Mining and Sentiment Analysis](https://www.cs.cornell.edu/home/llee/opinion-mining-sentiment-analysis-survey.html) cuộc khảo sát cơ bản. dài, nhưng bốn phần đầu tiên bao gồm tất cả mọi thứ cổ điển.
- [Wang and Manning (2012). Baselines and Bigrams: Simple, Good Sentiment and Topic Classification](https://aclanthology.org/P12-2018/) báo cáo cho thấy Bigrams + Naive Bayes khó đánh bại trên văn bản ngắn. / 证明二元组 + 朴素贝叶斯在短文上难以被超越的论文──
- [scikit-learn text feature extraction docs](https://scikit-learn.org/stable/modules/feature_extraction.html#text-feature-extraction) tham chiếu cho `CountVectorizer`- `TfidfVectorizer`, và mỗi nút mà bạn sẽ điều chỉnh. / `CountVectorizer``TfidfVectorizer`及你将调参的每个参数的参考──
