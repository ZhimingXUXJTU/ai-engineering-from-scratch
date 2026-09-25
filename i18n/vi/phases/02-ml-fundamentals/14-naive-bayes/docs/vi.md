# Bayes ngây thơ
# 朴素贝叶斯


> Giả định "tâm nhiên" là sai, và nó vẫn hoạt động. Đó là vẻ đẹp của nó.

> Hiểu tượng "phần tục" là sai lầm, nhưng nó vẫn có thể được sử dụng. Đó là điểm tuyệt vời của nó.

**Type:** Build | **类型：** 构建
**Language:**Python**语言：**Python
**Prerequisites:** Phase 2, Lessons 01-07 (classification, Bayes' theorem) | **前置知识：** Phase 2 第 1-7 课（分类、贝叶斯定理）
**Time:** ~75 minutes | **时间：** 约 75 分钟

## Mục tiêu học tập

- Thực hiện Multinomial Naive Bayes từ đầu với Laplace smoothing cho phân loại văn bản
  Từ zero thực hiện với Laplace 平滑的多项式简单贝叶斯用于文本分类
- Giải thích tại sao giả định độc lập ngây thơ là sai về mặt toán học nhưng tạo ra xếp hạng lớp học chính xác trong thực tế
  解释 tại sao giả định độc lập đơn giản trong toán học là sai nhưng thực tế tạo ra thứ hạng đúng
- So sánh đa số, Bernoulli, và Gaussian Naive Bayes biến thể và chọn đúng cho một loại tính năng nhất định
  So sánh các biến thể đa dạng, Bernuli và Cao Cao đơn giản, cho các biến thể được chọn đúng loại đặc trưng
- Đánh giá Bayes ngây thơ đối với sự lùi lại hậu cần trên dữ liệu hiếm có chiều cao và giải thích sự thỏa hiệp sự thiên vị-các biến tại nơi làm việc
  Trong các dữ liệu rất hiếm để đánh giá đơn giản, phân biệt và phân biệt


> **【中文解读】**
> 朴素贝叶斯 dựa trên định lý贝叶斯 + đặc điểm độc lập giả thuyết。 mặc dù giả thuyết rất mạnh, nhưng trong văn bản phân loại(垃圾邮件过) 中出奇地好──sklearn 中的多边NB/GaussianNB──

> **【拓展：朴素贝叶斯在垃圾邮件过滤和情感分析中的应用】**
> Các bộ lọc thư rác sớm như SpamAssassin) sử dụng rất nhiều đơn giản Bayes, vì nó có thể đạt đến hàng trăm ngàn từ ngữ, nhưng được đào tạo trong một số trường hợp nhỏ.

## Vấn đề  vấn đề giới thiệu

Bạn cần phân loại văn bản. Email vào spam hoặc không spam. đánh giá khách hàng vào tích cực hoặc tiêu cực. Vé hỗ trợ vào các loại. Bạn có hàng ngàn tính năng (một từ) và dữ liệu đào tạo hạn chế.

> Bạn cần phân loại văn bản. Bức thư phân chia thành thư rác hoặc không rác. Nhận xét của khách hàng phân chia thành những bài viết có tính chất khác nhau. Bạn có hàng ngàn đặc điểm (mỗi từ một) và dữ liệu đào tạo hạn chế.

Hầu hết các phân loại viên bị ngạt ở đây. Khản hồi hậu cần đủ mẫu để ước tính hàng ngàn trọng lượng một cách đáng tin cậy. Cây quyết định chia rẽ trên một từ một lần và quá phù hợp. KNN trong 10.000 chiều là vô nghĩa bởi vì mỗi điểm đều cách nhau với mọi điểm khác.

> Phần lớn các phân loại ở đây được đặt trong một cái cục. Khả năng trở lại cần đủ để có thể ước tính đáng tin cậy hàng ngàn trọng lượng.

Bayes ngây thơ sẽ xử lý chuyện này. Nó đưa ra một giả định sai về mặt toán học (nếu mỗi tính năng độc lập với mọi tính năng khác do lớp học), và nó vẫn vượt qua các mô hình " thông minh hơn" về phân loại văn bản, đặc biệt là với các tập hợp đào tạo nhỏ. Nó đào tạo trong một lần qua dữ liệu. Nó có thể đạt tới hàng triệu tính năng. Nó tạo ra ước tính xác suất (mặc dù thường được định đo kém do giả định độc lập).

> 朴贝叶斯能处理这种情况――它 đã đưa ra một giả định sai lầm về toán học, nhưng trong văn bản phân loại vẫn còn tốt hơn mô hình " thông minh hơn ", đặc biệt là trong tập tập luyện nhỏ. Nó chỉ cần trải qua một lần dữ liệu về khả năng đào tạo. Nó mở rộng lên hàng triệu đặc điểm. Nó tạo ra ước tính xác suất (mặc dù giả định độc lập thường không tốt)

Hiểu tại sao một giả định sai dẫn đến dự đoán tốt dạy bạn một điều cơ bản về học máy: mô hình tốt nhất không phải là đúng nhất, nó là một với sự thỏa hiệp biến thiên tốt nhất cho dữ liệu của bạn.

> Hiểu tại sao giả định sai lầm có thể tạo ra dự đoán tốt dạy cho bạn một số điều cơ bản trong học máy: mô hình tốt nhất không phải là mô hình chính xác nhất, mà là mô hình tốt nhất để cân nhắc sự khác biệt-lợi nhuận của dữ liệu của bạn.

> **【中文解读】**
> "Poice" của 朴素贝叶斯 nằm trong giả định tất cả các đặc điểm được phân loại nhất định độc lập với nhau. Điều này hầu như không tồn tại trong thực tế như "free" và "优惠" trong thư rác. Nhưng tại sao lại có thể sử dụng? Vì phân loại chỉ cần xếp hạng đúng các loại xác suất, không cần xác định giá trị xác suất. giả định độc lập làm cho các phương diện ước tính số lượng rất thấp.

## Khái niệm cốt lõi

### Lý thuyết Bayes (Quick Review)

Định lý Bayes làm đảo ngược xác suất có điều kiện:

> 贝叶斯定理翻转条件概率:

```
P(class | features) = P(features | class) * P(class) / P(features)
```

Chúng tôi muốn`P(class | features)`-- xác suất rằng một tài liệu thuộc về một lớp được đưa ra từ trong đó.
- `P(features | class)`-- khả năng nhìn thấy những từ này trong các tài liệu của lớp này
  `P(features | class)`- Trong tài liệu này thấy những từ này giống như vậy
- `P(class)`-- xác suất trước của lớp (spam phổ biến như thế nào nói chung?)
  `P(class)`-- 类别的先验概率(垃圾邮件 thường có nhiều thường见?)
- `P(features)`-- bằng chứng, giống nhau cho tất cả các lớp, để chúng ta có thể bỏ qua nó khi so sánh
  `P(features)`-- 证据, đối với tất cả các loại giống nhau, so sánh có thể bỏ qua

Nhóm có lớp cao nhất`P(class | features)`thắng.

> `P(class | features)`Cổ số nhất là thắng.

### Sự giả định độc lập ngây thơ

Máy tính `P(features | class)`với một từ vựng 10.000 từ, bạn sẽ cần ước tính một phân phối trên 2^10.000 kết hợp có thể.

> 精确计算 `P(features | class)`需要估估所有特征的联合概率──对于10,000个词表, bạn cần ước tính2^10,000 种可能组合上的分布──不可能──

Hiểu tưởng ngây thơ: mỗi tính năng đều độc lập theo điều kiện khi xem xét lớp học.

> 朴素假设:给定类别下每个特征条件独立――

```
P(w1, w2, ..., wn | class) = P(w1 | class) * P(w2 | class) * ... * P(wn | class)
```

Thay vì một phân phối chung không thể, bạn ước tính n phân phối đơn giản trên tính năng.

> Bạn không cần ước tính một phân bố chung không thể, mà ước tính n đơn giản phân bố riêng biệt.

Hiểu định này rõ ràng là sai. Từ "máy" và "làm học" không độc lập trong bất kỳ tài liệu nào. Nhưng trình phân loại không cần ước tính xác suất chính xác. Nó cần xếp hạng chính xác - lớp nào có xác suất cao nhất. Hiểu định độc lập giới thiệu những lỗi hệ thống, nhưng những sai lầm đó ảnh hưởng đến tất cả các lớp tương tự, vì vậy xếp hạng vẫn chính xác.

> Hiểu thuyết này rõ ràng là sai lầm. "cỗ máy" và "làm học" không độc lập trong bất kỳ tài liệu nào. Nhưng phân loại không cần ước tính tỷ lệ xác suất chính xác. Nó cần xếp hạng chính xác.

### Tại sao nó vẫn còn hiệu quả

Ba lý do:

> Ba lý do:

1. **Ranking over calibration.**Việc phân loại chỉ cần lớp xếp hạng hàng đầu để đúng. ngay cả khi P(spam) = 0,99999 khi xác suất thực là 0,7, phân loại vẫn chọn spam đúng. Chúng ta không cần xác suất chính xác. Chúng ta cần người chiến thắng chính xác.
   **排名优于校准。**Cổ phần chỉ cần xếp hạng thứ nhất trong danh sách đúng hơn. Ngay cả khi P(spam) = 0.99999 và tỷ lệ thực sự là 0.7, phân loại vẫn đúng trong việc chọn thư rác.

2. **High bias, low variance.**Hiểu thuyết độc lập là một giả định mạnh mẽ. Nó hạn chế mô hình rất nhiều, điều này ngăn chặn quá phù hợp. Với dữ liệu đào tạo hạn chế, một mô hình sai một chút nhưng ổn định đánh bại một mô hình lý thuyết đúng nhưng vô cùng không ổn định. Đây là sự đổi giá sự thiên vị trong hành động.
   **高偏差、低方差。**独立性假设 là một thử nghiệm mạnh mẽ. Nó nghiêm trọng ràng buộc mô hình, ngăn chặn quá phù hợp.

3. **Feature redundancy cancels out.**Các tính năng tương quan cung cấp bằng chứng dư thừa. Các phân loại nhân đôi đếm bằng chứng này, nhưng nó đếm gấp đôi cho lớp đúng cũng như. Nếu "cỗ máy" và "làm học" luôn xuất hiện cùng nhau, cả hai đều cung cấp bằng chứng cho lớp "công nghệ". NB đếm hai lần, nhưng nó đếm hai lần cho lớp đúng.
   **特征冗余相互抵消。**相关特征提供冗余证据――分类重复计数 这些证据,但正确类别的证据也被重复计数――如果"机器"和"学习"总是出现一次,两者都为"技术"类提供证据――简单贝叶斯计数两次,但为正确类别计数两次――

Lý do thứ tư, thực tế: Bayes ngây thơ là cực kỳ nhanh. Trình luyện là một lần đi qua tần số đếm dữ liệu. Dự đoán là một nhân số tử liệu. Bạn có thể đào tạo trên một triệu tài liệu trong vài giây. Tốc độ này có nghĩa là bạn có thể lặp lại nhanh hơn, thử nhiều bộ tính năng hơn, và chạy nhiều thí nghiệm hơn so với các mô hình chậm hơn.

> Lý do thực tế thứ tư: đơn giản Bayes cực nhanh. Việc tập luyện là một lần xuyên qua tần số dữ liệu. Dự đoán là phép tính矩阵. Bạn có thể tập luyện hàng triệu tài liệu trong vài giây.

### Các môn toán từng bước

Hãy bắt đầu bằng một ví dụ cụ thể. giả sử chúng ta có hai lớp: spam và không spam. Từ vựng của chúng ta có ba từ: "bởi không", "tiền", "các cuộc họp".

Dữ liệu đào tạo:
- Email spam đề cập đến "tự do" 80 lần, "tiền" 60 lần, "các cuộc họp" 10 lần (150 từ tổng thể)
- Các email không spam đề cập đến "tự do" 5 lần, "tiền" 10 lần, "các cuộc họp" 100 lần (115 từ tổng thể)
- 40% email là spam, 60% là không spam

Với Laplace làm trơn (alpha=1):

```
P(free | spam)    = (80 + 1) / (150 + 3) = 81/153 = 0.529
P(money | spam)   = (60 + 1) / (150 + 3) = 61/153 = 0.399
P(meeting | spam) = (10 + 1) / (150 + 3) = 11/153 = 0.072

P(free | not-spam)    = (5 + 1) / (115 + 3) = 6/118 = 0.051
P(money | not-spam)   = (10 + 1) / (115 + 3) = 11/118 = 0.093
P(meeting | not-spam) = (100 + 1) / (115 + 3) = 101/118 = 0.856
```

Email mới có chứa: "tự do" (2 lần), "tiền" (1 lần), "quá trình" (0 lần).

```
log P(spam | email) = log(0.4) + 2*log(0.529) + 1*log(0.399) + 0*log(0.072)
                    = -0.916 + 2*(-0.637) + (-0.919) + 0
                    = -3.109

log P(not-spam | email) = log(0.6) + 2*log(0.051) + 1*log(0.093) + 0*log(0.856)
                        = -0.511 + 2*(-2.976) + (-2.375) + 0
                        = -8.838
```

Spam thắng bằng một tỷ lệ lớn. Từ "tự do" xuất hiện hai lần là bằng chứng mạnh mẽ cho spam. Lưu ý rằng "quá trình" không xuất hiện đóng góp bằng không cho cả hai log sums (0 * log(P)) - trong Multinomial NB, từ vắng mặt không có tác động.

### Ba biến thể

Bayes ngây thơ có 3 loại.`P(feature | class)`khác nhau.

> n đơn giản có ba biến thể.`P(feature | class)`建模方式不同.

#### Bayes đa số ngây thơ

Mô hình mỗi tính năng như một con số. Tốt nhất cho dữ liệu văn bản nơi tính năng là tần số từ hoặc giá trị TF-IDF.

> Đặt mỗi đặc điểm thành một số.

```
P(word_i | class) = (count of word_i in class + alpha) / (total words in class + alpha * vocab_size)
```

- `alpha`là Laplace smoothing (được giải thích dưới đây).

> `alpha`là Laplace 平滑(下面解释)。

#### Gaussian Naive Bayes

Mô hình mỗi tính năng như một phân phối bình thường.

> Hãy đưa mỗi đặc điểm được phân phối đúng cách.

```
P(x_i | class) = (1 / sqrt(2 * pi * var)) * exp(-(x_i - mean)^2 / (2 * var))
```

Mỗi lớp có trung bình và sự khác biệt riêng cho mỗi tính năng. Điều này hoạt động tốt khi các tính năng thực sự theo đường cong chuông trong mỗi lớp.

> Mỗi loại có giá trị trung bình và khác biệt riêng đối với mỗi đặc điểm.

#### Bernoulli ngây thơ Bayes

Mô hình mỗi tính năng như nhị phân (đây hoặc vắng mặt).

> Hãy đưa mỗi đặc điểm thành mô hình thành 2 giá trị ()  ()  ()  ()  ()  ()  ()  ()  () )  ()  ()  ()  ()  ()  ()  ()  ()  ()  ()  ()  ()  ()  ()  ()  ()  ()  ()  ()  ()  ()  ()  ()  ()  ()  ()  ()  ()  ()  ()  ()  () )  ()  ()

```
P(word_i | class) = (docs in class containing word_i + alpha) / (total docs in class + 2 * alpha)
```

Không giống như Multinomial, Bernoulli rõ ràng trừng phạt sự vắng mặt của một từ. Nếu "tự do" thường xuất hiện trong thư rác nhưng vắng mặt trong email này, Bernoulli tính rằng đó là bằng chứng chống lại thư rác.

> Không giống như nhiều kiểu khác, Bernuly không có từ trừng phạt. Nếu "tự do" thường xuất hiện trong thư rác nhưng thư rác không có, Bernuly coi nó là bằng chứng chống lại thư rác.

### Khi nào nên sử dụng mỗi biến thể

| Variant | Feature Type | Best For | Example |
|---------|-------------|----------|---------|
| Multinomial | Counts or frequencies | Text classification, bag-of-words | Email spam, topic classification |
| Gaussian | Continuous values | Tabular data with normal-ish features | Iris classification, sensor data |
| Bernoulli | Binary (0/1) | Short text, binary feature vectors | SMS spam, presence/absence features |

| 变体 | 特征类型 | 最适合 | 示例 |
|------|---------|--------|------|
| Multinomial | 计数或频率 | 文本分类、词袋 | 邮件垃圾过滤、主题分类 |
| Gaussian | 连续值 | 近正态的表格数据 | 鸢尾花分类、传感器数据 |
| Bernoulli | 二值（0/1） | 短文本、二值特征向量 | 短信垃圾过滤、出现/缺失特征 |

### Laplace Smoothing

Điều gì xảy ra khi một từ xuất hiện trong dữ liệu thử nghiệm nhưng không xuất hiện trong dữ liệu đào tạo cho một lớp cụ thể?

> Nếu một từ xuất hiện trong dữ liệu thử nghiệm, nhưng không xuất hiện trong dữ liệu đào tạo của một loại nào đó, sẽ xảy ra gì?

Không làm trơn:`P(word | class) = 0/N = 0`Một số 0 nhân qua toàn bộ sản phẩm tạo ra`P(class | features) = 0`Một lời nói không được nhìn thấy sẽ phá hủy toàn bộ dự đoán, bất kể có nhiều bằng chứng nào khác hỗ trợ nó.

> Không tính:`P(word | class) = 0/N = 0`◊ một 零乘到整个乘积中会使 `P(class | features) = 0`Bất kể bằng chứng khác nào, một từ chưa thấy đã phá hủy toàn bộ dự đoán, bất kể bằng chứng khác nào, nhiều người ủng hộ.

Lượt độ Laplace thêm một con số nhỏ `alpha`(thường là 1) cho mỗi tính năng:

> Địa điểm bình thường cho mỗi tính năng đếm thêm một tính nhỏ `alpha`(thường là 1):

```
P(word_i | class) = (count(word_i, class) + alpha) / (total_words_in_class + alpha * vocab_size)
```

Với alpha = 1, mỗi từ có ít nhất một xác suất nhỏ. Từ "discombobulate" xuất hiện trong email thử nghiệm không còn giết chết xác suất spam.

> Alpha=1 时, mỗi từ ít nhất có được một tỷ lệ rất nhỏ. "Discombobulate" xuất hiện trong testmail không còn phá hủy tỷ lệ rác thải.

Alpha cao hơn có nghĩa là làm trơn hơn (các phân phối thống nhất hơn). alpha thấp hơn có nghĩa là mô hình tin tưởng dữ liệu nhiều hơn. Alpha là một siêu tham số bạn điều chỉnh.

> Alpha cao hơn có nghĩa là đơn giản hơn, gần hơn với phân bố bình thường hơn.

Ảnh hưởng của alpha:

> ảnh hưởng của alpha:

| Alpha | Effect | When to use |
|-------|--------|-------------|
| 0.001 | Almost no smoothing, trust the data | Very large training set, no unseen features expected |
| 0.1 | Light smoothing | Large training set |
| 1.0 | Standard Laplace smoothing | Default starting point |
| 10.0 | Heavy smoothing, flattens distributions | Very small training set, many unseen features expected |

| Alpha | 效果 | 使用场景 |
|-------|------|---------|
| 0.001 | 几乎不平滑，相信数据 | 非常大的训练集，预期不会有未见特征 |
| 0.1 | 轻度平滑 | 大训练集 |
| 1.0 | 标准 Laplace 平滑 | 默认起点 |
| 10.0 | 重度平滑，拉平分布 | 非常小的训练集，预期有很多未见特征 |

### Lượng tính toán log-space

Bội số hàng trăm xác suất (mỗi số ít hơn 1) gây ra dòng chảy thấp ở điểm nổi.

> Đặt một trăm xác suất (tất cả đều nhỏ hơn 1) sẽ dẫn đến điểm lở xuống.

Giải pháp: làm việc trong không gian log. Thay vì nhân xác suất, hãy thêm các logarithm của chúng:

> Giải pháp: Trong số lượng không gian tính toán, biến tỷ lệ tỷ lệ tăng lên số lượng:

```
log P(class | x1, x2, ..., xn) = log P(class) + sum_i log P(xi | class)
```

Điều này biến dự đoán thành một sản phẩm điểm:

> Cái dự đoán này đã biến thành điểm:

```
log_scores = X @ log_feature_probs.T + log_class_priors
prediction = argmax(log_scores)
```

Đó là lý do tại sao dự đoán của Bayes ngây thơ rất nhanh -- đó là hoạt động tương tự như mô hình tuyến tính một lớp.

> Đó là lý do đơn giản khiến Bayes dự đoán nhanh như vậy.

### Bayes ngây thơ vs Lịch lý

Cả hai đều là phân loại đường thẳng cho văn bản. Sự khác biệt là trong những gì chúng mô hình.

> Cả hai đều là các phân loại trực tuyến của văn bản. Sự khác biệt nằm ở các đối tượng được xây dựng.

| Aspect | Naive Bayes | Logistic Regression |
|--------|------------|-------------------|
| Type | Generative (models P(X\|Y)) | Discriminative (models P(Y\|X)) |
| Training | Count frequencies | Optimize loss function |
| Small data | Better (strong prior helps) | Worse (not enough to estimate weights) |
| Large data | Worse (wrong assumption hurts) | Better (flexible boundary) |
| Features | Assumes independence | Handles correlations |
| Speed | Single pass, very fast | Iterative optimization |
| Calibration | Poor probabilities | Better probabilities |

| 方面 | 朴素贝叶斯 | 逻辑回归 |
|------|----------|---------|
| 类型 | 生成式（建模 P(X\|Y)） | 判别式（建模 P(Y\|X)） |
| 训练 | 统计频率 | 优化损失函数 |
| 小数据 | 更好（强先验有帮助） | 更差（数据不足以估计权重） |
| 大数据 | 更差（错误假设有害） | 更好（灵活边界） |
| 特征 | 假设独立 | 能处理相关性 |
| 速度 | 单次遍历，极快 | 迭代优化 |
| 校准 | 概率校准差 | 概率校准更好 |

Quy tắc: bắt đầu với Bayes ngây thơ. Nếu bạn có đủ dữ liệu và cao nguyên NB, chuyển sang sự lùi hậu cần.

> 经验法则:先用朴素贝叶斯―― Nếu dữ liệu đủ và NB 性能停滞, đổi logic trở lại――

### Đường ống phân loại

```mermaid
flowchart LR
    A[Raw Text] --> B[Tokenize]
    B --> C[Build Vocabulary]
    C --> D[Count Word Frequencies]
    D --> E[Apply Smoothing]
    E --> F[Compute Log Probabilities]
    F --> G[Predict: argmax P class given words]

    style A fill:#f9f,stroke:#333
    style G fill:#9f9,stroke:#333
```

Thực tế, chúng ta làm việc trong không gian log để tránh dòng chảy dưới điểm nổi. thay vì nhân nhiều xác suất nhỏ, chúng ta thêm các logarithm của chúng:

```
log P(class | features) = log P(class) + sum_i log P(feature_i | class)
```

## Hãy xây dựng nó.

> **【中文解读】**
> Từ zero thực hiện đa số đơn giản phân loại (x) và高斯朴素贝叶斯 (x) GaussianNB, được sử dụng để liên tục đặc điểm (x) ⋅ nhiều số phiên bản thống kê mỗi từ xuất hiện trong mỗi phân loại (x) ⋅ Laplace (x) ⋅平滑防止零概率 (x) ⋅高斯版本假设 mỗi đặc điểm trong mỗi phân loại tuân theo đúng phân bố (x) ⋅

> **【拓展：朴素贝叶斯在现代 NLP 中的角色演变】**
> Mặc dù Transformer 模型 ((BERT、GPT) vượt quá rất nhiều công việc của NLP, nhưng công việc của nó vẫn còn có một lợi thế: thực时垃圾邮件过(毫秒级延迟) 、大规模文本预分类(成本极低) 、 như là cơ sở 快速验证特征工程效果. Trong chẩn đoán y tế,高斯朴素贝叶斯 được sử dụng rộng rãi vì khả năng xuất phát có thể giải thích được.
```figure
naive-bayes
```

## Hãy xây dựng nó

Mã trong `code/naive_bayes.py`thực hiện cả MultinomialNB và GaussianNB từ đầu.

### MultinomialNB

Việc thực hiện từ đầu:

1. **fit(X, y)**: Đối với mỗi lớp, đếm tần số của mỗi tính năng. Thêm thanh toán Laplace. Xét xác suất log. Cấp trước lớp (log tần số lớp).

2. **predict_log_proba(X)**: Đối với mỗi mẫu, tính toán log P(class) + tổng của log P(feature_i ≠class) cho tất cả các lớp. Đây là một số nhân tử liệu: X @ log_probs.T + log_priors.

3. **predict(X)**: Trở lại lớp có xác suất log cao nhất.

```python
class MultinomialNB:
    def __init__(self, alpha=1.0):
        self.alpha = alpha

    def fit(self, X, y):
        classes = np.unique(y)
        n_classes = len(classes)
        n_features = X.shape[1]

        self.classes_ = classes
        self.class_log_prior_ = np.zeros(n_classes)
        self.feature_log_prob_ = np.zeros((n_classes, n_features))

        for i, c in enumerate(classes):
            X_c = X[y == c]
            self.class_log_prior_[i] = np.log(X_c.shape[0] / X.shape[0])
            counts = X_c.sum(axis=0) + self.alpha
            self.feature_log_prob_[i] = np.log(counts / counts.sum())

        return self
```

Điều quan trọng: sau khi được gắn, dự đoán chỉ là nhân tử liệu cộng với một thiên vị.

### GaussianNB

Đối với các tính năng liên tục, chúng tôi ước tính trung bình và sự biến động cho mỗi lớp cho mỗi tính năng:

```python
class GaussianNB:
    def __init__(self):
        pass

    def fit(self, X, y):
        classes = np.unique(y)
        self.classes_ = classes
        self.means_ = np.zeros((len(classes), X.shape[1]))
        self.vars_ = np.zeros((len(classes), X.shape[1]))
        self.priors_ = np.zeros(len(classes))

        for i, c in enumerate(classes):
            X_c = X[y == c]
            self.means_[i] = X_c.mean(axis=0)
            self.vars_[i] = X_c.var(axis=0) + 1e-9
            self.priors_[i] = X_c.shape[0] / X.shape[0]

        return self
```

Dự đoán sử dụng Gaussian PDF cho mỗi tính năng, nhân trên các tính năng (được thêm vào không gian log).

### Demo: Định dạng văn bản

Mã tạo ra dữ liệu túi từ tổng hợp mô phỏng hai lớp (những bài viết công nghệ so với các bài viết thể thao). Mỗi lớp có phân bố tần số từ khác nhau. MultinomialNB phân loại chúng bằng cách sử dụng số lượng từ.

Các dữ liệu tổng hợp hoạt động như sau: chúng tôi tạo ra 200 "lời" (cột tính năng). Từ 0-39 có tần suất cao trong các bài viết công nghệ và thấp trong thể thao. Từ 80-119 có tần suất cao trong thể thao và thấp trong công nghệ. Từ 40-79 là tần suất trung bình trong cả hai. Điều này tạo ra một kịch bản thực tế nơi một số từ là chỉ số hạng mạnh và những từ khác là tiếng ồn.

### Demo: Các tính năng liên tục

Mã tạo ra dữ liệu giống như Iris (3 lớp, 4 tính năng, cụm Gaussian). GaussianNB phân loại bằng cách sử dụng trung bình và biến thể cho mỗi lớp. Mỗi lớp có trung tâm khác nhau (vêctơ trung bình) và sự lan rộng khác nhau (hác biến), bắt chước dữ liệu trong thế giới thực nơi các phép đo khác nhau theo hệ thống giữa các loại.

Bộ luật cũng chứng minh:
- **Smoothing comparison:**Đào tạo MultinomialNB với các giá trị alpha khác nhau để thể hiện tác động của sức mạnh làm trơn trên độ chính xác.
- **Training size experiment:**Làm thế nào độ chính xác NB cải thiện khi dữ liệu đào tạo tăng từ 20 đến 1600 mẫu. NB đạt được độ chính xác tốt ngay cả với rất ít mẫu - đây là lợi thế chính của nó.
- **Confusion matrix:**Độ chính xác, nhớ lại và điểm số F1 cho thấy NB mắc sai lầm.

### Tốc độ dự đoán

Dự đoán Bayes ngây thơ là một nhân số tử liệu. Đối với n mẫu có d tính năng và lớp k:
- MultinomialNB: một số tử liệu nhân (n x d) @ (d x k) = O(n * d * k)
- GaussianNB: n * k Đánh giá PDF Gaussian, mỗi tính năng d = O(n * d * k)

Cả hai đều tuyến tính trong mọi chiều kích. So sánh với KNN (cần tính khoảng cách đến tất cả các điểm đào tạo) hoặc SVM với lõi RBF (cần đánh giá lõi đối với tất cả các vector hỗ trợ). NB nhanh hơn theo thứ tự quy mô tại thời gian dự đoán.

## Hãy sử dụng nó để thực hiện

Với sklearn, cả hai biến thể là một dòng:

```python
from sklearn.naive_bayes import GaussianNB, MultinomialNB

gnb = GaussianNB()
gnb.fit(X_train, y_train)
print(f"GaussianNB accuracy: {gnb.score(X_test, y_test):.3f}")

mnb = MultinomialNB(alpha=1.0)
mnb.fit(X_train_counts, y_train)
print(f"MultinomialNB accuracy: {mnb.score(X_test_counts, y_test):.3f}")
```

Đối với phân loại văn bản với sklearn:

```python
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline

text_clf = Pipeline([
    ("vectorizer", CountVectorizer()),
    ("classifier", MultinomialNB(alpha=1.0)),
])

text_clf.fit(train_texts, train_labels)
accuracy = text_clf.score(test_texts, test_labels)
```

Mã trong `naive_bayes.py`so sánh các triển khai từ đầu với sklearn trên cùng một dữ liệu để xác minh sự chính xác.

### TF-IDF với Naive Bayes

Số từ thô cho mỗi từ trọng lượng bằng nhau cho mỗi sự kiện. Nhưng các từ phổ biến như "the" và "is" xuất hiện thường xuyên trong mỗi lớp - chúng không mang thông tin. TF-IDF (Term Frequency - Inverse Document Frequency) giảm trọng lượng từ phổ biến và tăng trọng lượng từ hiếm, phân biệt đối xử.

```python
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline

text_clf = Pipeline([
    ("tfidf", TfidfVectorizer()),
    ("classifier", MultinomialNB(alpha=0.1)),
])
```

Các giá trị TF-IDF không âm tính, vì vậy chúng hoạt động với MultinomialNB. Sự kết hợp của TF-IDF + MultinomialNB là một trong những đường cơ sở mạnh nhất cho phân loại văn bản. Nó thường đánh bại các mô hình phức tạp hơn trên tập dữ liệu với ít hơn 10.000 mẫu đào tạo.

### BernoulliNB cho văn bản ngắn

Đối với văn bản ngắn (tweet, SMS, tin nhắn trò chuyện), BernoulliNB có thể vượt qua MultinomialNB. Các văn bản ngắn có số lượng từ thấp, vì vậy thông tin tần số mà MultinomialNB dựa vào là tiếng ồn. BernoulliNB chỉ quan tâm đến sự hiện diện hoặc vắng mặt, điều này đáng tin cậy hơn với văn bản ngắn.

```python
from sklearn.naive_bayes import BernoulliNB
from sklearn.feature_extraction.text import CountVectorizer

text_clf = Pipeline([
    ("vectorizer", CountVectorizer(binary=True)),
    ("classifier", BernoulliNB(alpha=1.0)),
])
```

- `binary=True`cờ trong CountVectorizer chuyển đổi tất cả các con số thành 0/1. Không có nó, BernoulliNB vẫn hoạt động nhưng đang nhìn thấy con số mà nó không được thiết kế cho.

### Định so sánh NB Khả năng

NB xác suất được chuẩn bị kém. Khi NB nói P(spam) = 0,95, xác suất thực có thể là 0,7. Nếu bạn cần ước tính xác suất đáng tin cậy (ví dụ, để đặt ngưỡng hoặc kết hợp với các mô hình khác), sử dụng sklearn's CalibratedClassifierCV:

```python
from sklearn.calibration import CalibratedClassifierCV

calibrated_nb = CalibratedClassifierCV(MultinomialNB(), cv=5, method="sigmoid")
calibrated_nb.fit(X_train, y_train)
proba = calibrated_nb.predict_proba(X_test)
```

Điều này phù hợp với một sự lùi hậu cần trên đỉnh điểm thô của NB bằng cách sử dụng xác thực chéo.

### Gotcha thông thường

1. **Negative feature values.**MultinomialNB yêu cầu các tính năng không âm. Nếu bạn có các giá trị tiêu cực (như TF-IDF với một số cài đặt hoặc các tính năng tiêu chuẩn hóa), hãy sử dụng GaussianNB thay vào đó, hoặc chuyển các tính năng để tích cực.

2. **Zero variance features.**GaussianNB chia theo sự biến động. Nếu một tính năng có sự biến động không cho một lớp (tất cả các giá trị đều giống nhau), tính toán xác suất bị phá vỡ. Mã thêm một thuật ngữ thanh thản nhỏ (1e-9) vào tất cả các biến động để ngăn chặn điều này.

3. **Class imbalance.**Nếu 99% email không spam, P không spam trước = 0,99 là mạnh đến nỗi nó áp đảo bằng chứng xác suất. Bạn có thể đặt các ưu tiên lớp bằng tay hoặc sử dụng tham số class_prior trong sklearn.

4. **Feature scaling.**MultinomialNB không cần quy mô (nó hoạt động trên đếm). GaussianNB cũng không cần quy mô (nó ước tính thống kê tính năng).

## Chuyển nó đi.

Bài học này mang lại:
- `outputs/skill-naive-bayes-chooser.md`-- một kỹ năng quyết định để chọn đúng biến thể NB
- `code/naive_bayes.py`-- MultinomialNB và GaussianNB từ đầu, với so sánh sklearn

### Khi Bayes ngây thơ thất bại

NB thất bại khi giả định độc lập gây ra xếp hạng không chính xác (không chỉ có xác suất không chính xác).

1. **Strong feature interactions.**Nếu lớp phụ thuộc vào sự kết hợp của hai tính năng nhưng không phải là một mình (chương trình giống như XOR), NB sẽ bỏ qua nó hoàn toàn.

2. **Highly correlated features with opposing evidence.**Nếu tính năng A nói "spam" và tính năng B nói "không spam", nhưng A và B tương quan hoàn hảo (bạn luôn đồng ý trong thực tế), NB sẽ thấy bằng chứng mâu thuẫn nơi không có.

3. **Very large training sets.**Với đủ dữ liệu, các mô hình phân biệt đối xử như sự lùi hậu cần học được ranh giới quyết định thực sự và vượt qua NB. Giả định độc lập đã giúp với dữ liệu nhỏ bây giờ giữ lại mô hình.

Trong thực tế, các chế độ thất bại này hiếm khi xảy ra cho phân loại văn bản. Các tính năng văn bản rất nhiều, yếu kém riêng lẻ, và các lỗi của giả định độc lập có xu hướng bị hủy bỏ. Đối với dữ liệu bảng với một số tính năng tương quan mạnh mẽ, hãy xem xét sự lùi lại hậu cần hoặc mô hình dựa trên cây trước.

## Tập luyện bài tập

1. **Smoothing experiment.**Đào tạo MultinomialNB trên dữ liệu văn bản với giá trị alpha là 0.01, 0.1, 1.0, 10.0 và 100.0. Độ chính xác của bản vẽ so với alpha.
   1. **平滑实验。**Sử dụng alpha  giá trị 0.01、0.1、1.0、10.0、100.0 trong bài tập trên dữ liệu văn bản MultinomialNB── vẽ tỷ lệ chính xác so với alpha── hiệu suất đỉnh ở đâu?

2. **Feature independence test.**Hãy lấy một tập dữ liệu văn bản thực. Chọn hai từ có liên quan rõ ràng ("máy" và "làm học"). Xét P n 1 n lớp) * P n 2 n lớp) và so sánh với P n 1 n lớp 2 n lớp. Giả định độc lập là sai đến mức nào? Nó ảnh hưởng đến độ chính xác phân loại?
   2. **特征独立性测试。**取一个真文本数据集. 选择两个明显相关词 (如"机器"和"学习") 计算 P(word1 类) * P(word2 类) 并与 P(word1 AND word2 类) 比较.

3. **Bernoulli implementation.**Lớn thêm mã bằng lớp BernoulliNB. Chuyển đổi túi từ thành nhị phân (đây/không có) và so sánh độ chính xác so với MultinomialNB trên dữ liệu văn bản.
   3. **伯努利实现。**扩展代码添加 BernoulliNB 类──将词袋转为二值(存在/不存在)并与多语数NB 在文本数据上比较准确率──伯努利何时赢?

4. **NB vs Logistic Regression.**Căn luyện cả hai trên dữ liệu văn bản. Bắt đầu với 100 mẫu đào tạo và tăng lên 10.000. Độ chính xác của cốt truyện so với kích thước tập hợp đào tạo cho cả hai.
   4. **NB vs 逻辑回归。**Trong dữ liệu văn bản, tập luyện hai người. Từ 100 mẫu tập luyện bắt đầu tăng lên 10.000.

5. **Spam filter.**Xây dựng một phân loại spam hoàn chỉnh: mã hóa văn bản email nguyên liệu, xây dựng từ vựng, tạo các tính năng túi từ, đào tạo MultinomialNB, đánh giá với độ chính xác và nhớ lại (không chỉ chính xác - tại sao?).
   5. **垃圾邮件过滤器。**构建完整的垃圾邮件分类器:分词原始邮件文本、构建词汇表、创建词袋特征、训练 MultinomialNB、使用精确率和召回率评估──

> **【中文解读】**
> 朴素贝叶斯的三种变体:(1) 多项式朴素贝叶斯(MultinomialNB) 适用于词频/TF-IDF特征文本分类;(2) 伯努利朴素贝叶斯(BernoulliNB) 适用于二值特征(词是否出现);(3) 高斯朴素贝叶斯(GaussianNB) 适用于连续特征, giả định mỗi类内特征服从正态分布――Laplace 平滑加) sẽ không ngăn chặn vấn đề xác suất 遇到训练集中没见过的词时,概率为零.

## Từ khóa  Từ khóa nhanh chóng

| Term | What people say | What it actually means |
|------|----------------|----------------------|
| Naive Bayes | "Simple probabilistic classifier" | A classifier that applies Bayes' theorem with the assumption that features are conditionally independent given the class |
| Conditional independence | "Features don't affect each other" | P(A, B \| C) = P(A \| C) * P(B \| C) -- knowing B tells you nothing new about A once you know C |
| Laplace smoothing | "Add-one smoothing" | Adding a small count to every feature to prevent zero probabilities from dominating the prediction |
| Prior | "What you believed before seeing data" | P(class) -- the probability of each class before observing any features |
| Likelihood | "How well the data fits" | P(features \| class) -- the probability of observing these features if the class is known |
| Posterior | "What you believe after seeing data" | P(class \| features) -- the updated probability of the class after observing the features |
| Generative model | "Models how data is generated" | A model that learns P(X \| Y) and P(Y), then uses Bayes' theorem to get P(Y \| X) |
| Discriminative model | "Models the decision boundary" | A model that directly learns P(Y \| X) without modeling how X is generated |
| Log probability | "Avoid underflow" | Working with log P instead of P to prevent the product of many small numbers from becoming zero in floating point |

## Xem thêm 延伸阅读

- [scikit-learn Naive Bayes docs](https://scikit-learn.org/stable/modules/naive_bayes.html)-- tất cả ba biến thể với chi tiết toán học
  [scikit-learn 朴素贝叶斯文档](https://scikit-learn.org/stable/modules/naive_bayes.html)- 三种变体及数学细节
- [McCallum and Nigam, A Comparison of Event Models for Naive Bayes Text Classification (1998)](https://www.cs.cmu.edu/~knigam/papers/multinomial-aaaiws98.pdf)-- so sánh cổ điển của Multinomial vs Bernoulli cho văn bản
  [McCallum and Nigam (1998)](https://www.cs.cmu.edu/~knigam/papers/multinomial-aaaiws98.pdf)- nhiều bài học vs 伯努利文本分类经典比较
- [Rennie et al., Tackling the Poor Assumptions of Naive Bayes Text Classifiers (2003)](https://people.csail.mit.edu/jrennie/papers/icml03-nb.pdf)-- cải tiến NB cho văn bản
  [Ng and Jordan (2001)](https://ai.stanford.edu/~ang/papers/nips01-discriminativegenerative.pdf)- chứng minh NB trong ít dữ liệu nhận được nhanh chóng trong LR
- [Ng and Jordan, On Discriminative vs. Generative Classifiers (2001)](https://ai.stanford.edu/~ang/papers/nips01-discriminativegenerative.pdf)-- chứng minh NB hội tụ nhanh hơn LR với ít dữ liệu
