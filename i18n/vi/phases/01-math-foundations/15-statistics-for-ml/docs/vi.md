# Thống kê cho học máy  机器学习统计学

> Thống kê là cách bạn biết liệu mô hình của bạn thực sự hoạt động hay chỉ là may mắn.
> 统计学 nói với bạn mô hình là thực sự hiệu quả hoặc chỉ là vận động tốt.

**Type:** Build | **类型:** 动手
**Language:**Python**语言:**Python
**Prerequisites:** Phase 1, Lessons 06 (Probability and Distributions), 07 (Bayes' Theorem) | **前置知识:** Phase 1, 第 06 课（概率与分布）、第 07 课（贝叶斯定理）
**Time:** ~120 minutes | **时间:** ~120 分钟

## Mục tiêu học tập

- Xét số liệu mô tả, tương quan Pearson/Spearman và các matrix tính biến từ đầu
  Từ zero tính toán mô tả: √ Pearson/Spearman √

- Thực hiện các thử nghiệm giả thuyết (t-test, chi-quad) và giải thích đúng các giá trị p và khoảng thời gian tin cậy
  执行假设检验(t 检验、卡方检验),正确解释 p 值和置信区间

- Sử dụng bootstrap resampling để xây dựng khoảng thời gian tin cậy cho bất kỳ metric nào mà không có giả định phân phối
  Sử dụng Bootstrap 重采样为任意标标构建置信区间,无需分布假设

- Hóa ra sự quan trọng thống kê từ sự quan trọng thực tế bằng cách sử dụng các biện pháp kích thước hiệu ứng
  Sử dụng hiệu ứng số lượng phân biệt đáng kể thống kê và đáng kể thực tế

> **【中文解读】**
> 统计学告诉你模型是真的有效还是运气好――A/B 测试评估新模型、Bootstrap 构建置信区间、假设检查判断差异显著性这些是ML 实验评估的基础――

## Vấn đề  vấn đề giới thiệu

> **【中文解读】**模型 A 准确率 0.87,模型 B 准确率 0.89,你部署 B。三周后线效果反而变化了因为 0.02 差异是噪音不是真实升级──统计学答案:差异是显著吗?置信区间多宽?样本量不够?没有统计学ML 实验 = 盲摸象──

## Khái niệm cốt lõi

> **【拓展：AI 工程中的统计学实战】**(1) **A/B 测试**:推/搜索模型上线前必须做,统计显著(p<0.05) mới được phát hành;(2) **Bootstrap 置信区间**: không cần giả định phân bố dữ liệu, sử dụng hình thức xây dựng bất kỳ chỉ số nào của một khu vực tín nhiệm;**效应量**:p 值 chỉ nói với bạn" có bất kỳ sự khác biệt",effect量 nói với bạn" sự khác biệt có nhiều hơn" thống kê rõ ràng ≠ 实际有用;**多重比较校正**:调了20 超参数取最好,必须校正否则是"多碰运气"──

Điều này xảy ra liên tục. Chuyển đổi bảng xếp hạng của Kaggle. Các bài báo không thể tái tạo. Các bài kiểm tra A / B tuyên bố người chiến thắng dựa trên vài trăm mẫu. Nguyên nhân gốc luôn giống nhau: ai đó bỏ qua số liệu thống kê.

> Những điều này thường xảy ra. Các bài báo không thể hoàn thành được dựa trên vài trăm mẫu trên A/B test tuyên bố người chiến thắng.

Thống kê cho bạn những công cụ để phân biệt tín hiệu từ tiếng ồn. Nó cho bạn biết khi nào sự khác biệt là thực, bạn nên tự tin đến mức nào, và bạn cần bao nhiêu dữ liệu trước khi bạn có thể tin vào kết quả. Mỗi đường ống dẫn ML, mỗi so sánh mô hình, mỗi thí nghiệm cần thống kê. Nếu không có nó, bạn đang đoán.

> 统计 cho bạn cung cấp một công cụ phân biệt tín hiệu và tiếng ồn. Nó cho bạn biết khi nào sự khác biệt là thực, bạn nên có nhiều niềm tin, và bạn cần bao nhiêu dữ liệu để tin vào một kết quả. Mỗi ống ML, mỗi mô hình so sánh, mỗi thí nghiệm đều cần thống kê. Nếu không có nó, bạn chỉ cần đoán.

## Khái niệm cốt lõi

### Thống kê mô tả: Tóm lại dữ liệu của bạn                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                 

Trước khi bạn mô hình bất cứ thứ gì, bạn cần phải biết dữ liệu của bạn trông như thế nào.

> Trước khi xây dựng bất kỳ mô hình nào, bạn cần phải hiểu mô hình dữ liệu.

**Measures of central tendency**trả lời "nhiều ở giữa đâu?"

> **集中趋势度量** trả lời "中间在哪里?"

```
Mean:   sum of all values / count
        mu = (1/n) * sum(x_i)

Median: middle value when sorted
        Robust to outliers. If you have [1, 2, 3, 4, 1000], the mean is 202
        but the median is 3.

Mode:   most frequent value
        Useful for categorical data. For continuous data, rarely informative.
```

Trung bình là điểm cân bằng. trung bình là dấu hiệu nửa đường. Khi chúng khác nhau, phân phối của bạn bị lệch. Phân phối thu nhập có trung bình >> trung bình (người tỷ phú có sự lệch bên phải). Phân bố mất mát trong quá trình đào tạo thường có trung bình << trung bình (người lệch bên trái từ các mẫu dễ dàng).

> 平均值是平衡点──中位数是中间标志── khi chúng偏离, phân bố của bạn là偏斜──收入分布的平均值远大于中位数(亿万富翁造成的右偏)──训练期间损失分布的平均值通常远小于中位数(简单样本造成的左偏)──

**Measures of spread**trả lời "dữ liệu phân tán như thế nào?"

> **离散程度度量** trả lời "Có dữ liệu có thể được phân tán?"

```
Variance:   average squared deviation from the mean
            sigma^2 = (1/n) * sum((x_i - mu)^2)

Standard deviation:  square root of variance
                     sigma = sqrt(sigma^2)
                     Same units as the data, so more interpretable.

Range:      max - min
            Sensitive to outliers. Almost never useful alone.

IQR:        Q3 - Q1 (interquartile range)
            The range of the middle 50% of the data.
            Robust to outliers. Used for box plots and outlier detection.
```

**Percentiles**chia dữ liệu được sắp xếp thành 100 phần bình đẳng. phần trăm 25 (Q1) có nghĩa là 25% giá trị rơi xuống dưới điểm này. phần trăm 50 là trung bình. phần trăm 75 là Q3.

> **百分位数**Để phân chia dữ liệu sau thứ tự thành 100 等份──第25百分位数(Q1) có nghĩa là 25% giá trị thấp hơn điểm này──第50百分位数就是中位数──第75百分位数是Q3──

```
For latency monitoring:
  P50 = median latency        (typical user experience)
  P95 = 95th percentile       (bad but not worst case)
  P99 = 99th percentile       (tail latency, often 10x the median)
```

Trong ML, bạn quan tâm đến phần trăm cho độ trễ suy luận, phân phối sự tin cậy dự đoán và phân phối lỗi hiểu. Một mô hình với lỗi trung bình thấp nhưng lỗi P99 khủng khiếp có thể vô dụng cho các ứng dụng quan trọng về an toàn.

> Trong ML, bạn quan tâm đến suy đoán trì hoãn, dự đoán và phân phối độ tin cậy và phân phối sai lầm. Một mô hình có độ sai lầm trung bình thấp nhưng P99 rất kém, đối với các ứng dụng quan trọng an ninh có thể là vô dụng.

**Sample vs population statistics.**Khi tính toán sự biến động từ một mẫu, hãy chia bằng (n-1) thay vì n. Đây là sự sửa đổi của Bessel. Nó bù đắp cho thực tế là trung bình mẫu của bạn không phải là trung bình dân số thực. Với n trong tên gọi, bạn có thể đánh giá thấp sự biến động thực sự. Với (n-1), ước tính là không thiên vị.

> **样本统计 vs 总体统计。**Từ mẫu tính toán tỷ lệ khác nhau, trừ với (n-1) thay vì n── đây là sự sửa đổi của Bessel. Nó bù đắp cho thực tế rằng mẫu trung bình không phải là giá trị trung bình tổng thể thực.

```
Population variance: sigma^2 = (1/N) * sum((x_i - mu)^2)
Sample variance:     s^2     = (1/(n-1)) * sum((x_i - x_bar)^2)
```

Thực tế: nếu n lớn (người mẫu hàng ngàn), sự khác biệt là vô cùng nhỏ.

> Thực tế: Nếu n  rất lớn ((1000 mẫu), sự khác biệt có thể bị bỏ qua.

### Sự tương quan: Làm thế nào các biến di chuyển cùng nhau 相关性: biến động làm thế nào thay đổi cùng nhau

Sự tương quan đo lường sức mạnh và hướng của mối quan hệ tuyến tính giữa hai biến.

> 相关性 đo cường độ và hướng của mối quan hệ liên quan giữa hai biến số.

**Pearson correlation coefficient**Các biện pháp liên kết tuyến tính:

> **Pearson 相关系数**衡量线性关联:

```
r = sum((x_i - x_bar)(y_i - y_bar)) / (n * s_x * s_y)

r = +1:  perfect positive linear relationship
r = -1:  perfect negative linear relationship
r =  0:  no linear relationship (but there might be a nonlinear one!)

Range: [-1, 1]
```

Pearson cho rằng mối quan hệ này là tuyến tính và cả hai biến đều được phân phối bình thường. Nó nhạy cảm với các điểm ngoại lệ. Một điểm cực đoan duy nhất có thể kéo r từ 0,1 đến 0,9.

> Pearson giả định mối quan hệ là tuyến tính, và hai biến thể hầu như tuân theo phân bố đúng dạng. Nó nhạy cảm với các giá trị bất thường.

**Spearman rank correlation**Các biện pháp liên kết đơn giản:

> **Spearman 秩相关**衡量单调关联:

```
1. Replace each value with its rank (1, 2, 3, ...)
2. Compute Pearson correlation on the ranks

Spearman catches any monotonic relationship, not just linear.
If y = x^3, Pearson gives r < 1 but Spearman gives rho = 1.
```

**When to use each:**

> **何时使用哪个：**

```
Pearson:    Both variables are continuous and roughly normal.
            You care about the linear relationship specifically.
            No extreme outliers.

Spearman:   Ordinal data (rankings, ratings).
            Data is not normally distributed.
            You suspect a monotonic but not linear relationship.
            Outliers are present.
```

**The golden rule:**sự tương quan không có nghĩa là sự gây nguyên nhân. bán kem và tử vong chết đuối có liên quan bởi vì cả hai đều tăng vào mùa hè. Độ chính xác của mô hình và số lượng các tham số của bạn có liên quan, nhưng việc thêm các tham số không tự động cải thiện độ chính xác (xem: Overfitting).

> **黄金法则：**相关不意味因果──冰淋销售和溺水死亡是相关的,因为它们都在夏季增加──你的模型精度和参数数数量是相关的,但增加参数并不自动提高精度(见:过拟合) ⋅

### Matrix tính biến đổi

Sự đồng biến giữa hai biến đo lường cách chúng thay đổi với nhau:

> Sự khác biệt giữa hai biến số đo lường cách chúng thay đổi cùng nhau:

```
Cov(X, Y) = (1/n) * sum((x_i - x_bar)(y_i - y_bar))

Cov(X, Y) > 0:  X and Y tend to increase together
Cov(X, Y) < 0:  when X increases, Y tends to decrease
Cov(X, Y) = 0:  no linear co-movement
```

Đối với d tính năng, các matrix tính toán C là một d x d matrix nơi C[i][j] = Cov(feature_i, feature_j).

> Đối với d 个特征,协方差矩阵 C là một d x d矩阵, trong đó C[i][j] = Cov(feature_i, feature_j) ―― đối với các yếu tố C[i][i] là mỗi đặc điểm của方差──

```
C = | Var(x1)      Cov(x1,x2)  Cov(x1,x3) |
    | Cov(x2,x1)  Var(x2)      Cov(x2,x3) |
    | Cov(x3,x1)  Cov(x3,x2)  Var(x3)     |

Properties:
  - Symmetric: C[i][j] = C[j][i]
  - Positive semi-definite: all eigenvalues >= 0
  - Diagonal = variances
  - Off-diagonal = covariances
```

**Connection to PCA.**PCA tự cấu thành các matrix có sự biến đổi. Các eigenvector là các thành phần chính (nghĩa của sự biến đổi tối đa). Các eigenvalue cho bạn biết mỗi thành phần nắm bắt được sự biến đổi bao nhiêu. Đây chính xác là điều mà Bài học 10 đã đề cập đến, nhưng bây giờ bạn thấy tại sao matrix có sự biến đổi là điều đúng để phân hủy: nó mã hóa tất cả các mối quan hệ tuyến tính theo cặp trong dữ liệu của bạn.

> **与 PCA 的联系。**PCA đối với một mô hình so sánh so sánh phân tích đặc điểm. Chất lượng so sánh là thành phần chính. Chất lượng so sánh cho bạn biết mỗi thành phần đã nắm bắt được bao nhiêu mô hình so sánh. Đây chính là nội dung của bài học thứ 10, nhưng bây giờ bạn đã hiểu tại sao mô hình so sánh so sánh là đối tượng phân tích chính xác: nó mã hóa tất cả các mối quan hệ tuyến tính trong dữ liệu.

**Connection to correlation.**Matrix tương quan là matrix covariance của các biến tiêu chuẩn hóa (mỗi biến được chia bằng lệch tiêu chuẩn của nó).

> **与相关性的联系。**相关矩阵是标准化变量 (), mỗi bên cạnh với các chuẩn差 ().

### - Hình như là một cái gì đó.

Kiểm tra giả thuyết là một khuôn khổ để đưa ra quyết định trong tình trạng không chắc chắn. Bạn bắt đầu với một yêu cầu, thu thập dữ liệu và xác định liệu dữ liệu có phù hợp với yêu cầu không.

> 假设 kiểm tra là một khuôn khổ của việc đưa ra quyết định dưới sự không chắc chắn. Bạn bắt đầu từ một chủ đề, thu thập dữ liệu, sau đó quyết định liệu dữ liệu có phù hợp với chủ đề hay không.

**The setup:**

> **基本设置：**

```
Null hypothesis (H0):        the default assumption, usually "no effect"
Alternative hypothesis (H1): what you are trying to show

Example:
  H0: Model A and Model B have the same accuracy
  H1: Model B has higher accuracy than Model A
```

**The p-value**là xác suất nhìn thấy dữ liệu cực đoan như những gì bạn quan sát, giả sử H0 là đúng.

> **p 值**Trong giả thuyết thực tế, quan sát có tỷ lệ xác suất của dữ liệu cùng cực hoặc cực hơn với dữ liệu quan sát.

```
p-value = P(data this extreme | H0 is true)

If p-value < alpha (typically 0.05):
    Reject H0. The result is "statistically significant."
If p-value >= alpha:
    Fail to reject H0. You do not have enough evidence.
    This does NOT mean H0 is true.
```

**Confidence intervals**Đưa ra một phạm vi các giá trị hợp lý cho một tham số:

> **置信区间**给出参数 một phạm vi giá trị hợp lý:

```
95% confidence interval for the mean:
    x_bar +/- z * (s / sqrt(n))

where z = 1.96 for 95% confidence

Interpretation: if you repeated this experiment many times, 95% of the
computed intervals would contain the true mean. It does NOT mean there
is a 95% probability the true mean is in this specific interval.
```

Độ rộng của khoảng thời gian tin cậy cho bạn biết về độ chính xác. khoảng thời gian rộng có nghĩa là sự không chắc chắn cao. khoảng thời gian hẹp có nghĩa là ước tính của bạn là chính xác (nhưng không nhất thiết phải chính xác, nếu dữ liệu của bạn bị thiên vị).

> 置信区间的宽度告诉你精度──宽区间意味着高不确定性──窄区间意味着你的估计是精确的(但如果数据有偏见,不一定准确) ⋅

### Thử nghiệm t-t-t-t-t-t-t-t-t-t-t-t-t-t-t-t-t-t-t-t-t-t-t-t-t-t-t-t-t-t-t-t-t-t-t-t-t-t-t-t-t-t-t-t-t-t-t-t-t-t-t-t-t-t-t-t-t-t-t-t-t-t-t-t-t-t-t-t-t-t-t-t-t-t-t-t-t-t-t-t-t-t-t-t-t-t-t-t-t-t-t-t-t-t-t-t-t-t-t-t-t-t-t-t-t-t-t-t-t-t-t-t-t-t-t-t-t-t-t-t-t-t-t-t-t-t-t-t-t-t-t-t-t-t-t-t-t-t-t-t-t-t-t-t-t-t-t-t-t-t-t-t-t-t-t-t-t-t-t-t-t-t-t-t-t-t-t-t-t-t-t-t-t-t-t-t-t-t-t-t-t-t-t-t-t-t-t-t-t-t-t-t-t-t-t-t-t-t-t-t-t-t-t-t-t-t-t-t-t-t-t-t-t-t-t-t-t-t-t-t-t-t-t-t-t-t-t-t-t-t-t-t-t-t-t-t-t-t-t-t-t-t-t-t-t-t-t-t-t-t-t-t-t-t

Thử nghiệm t so sánh các phương tiện.

> t 检测比较平均值── có vài biến thể──

**One-sample t-test:**liệu con số trung bình dân số có khác với giá trị giả định không?

> **单样本 t 检验：** Tổng giá trị trung bình có khác với giả định không?

```
t = (x_bar - mu_0) / (s / sqrt(n))

degrees of freedom = n - 1
```

**Two-sample t-test (independent):**hai nhóm có nghĩa khác nhau không?

> **两样本 t 检验（独立）：**Giá trị trung bình của hai nhóm có khác nhau không?

```
t = (x_bar_1 - x_bar_2) / sqrt(s1^2/n1 + s2^2/n2)

This is Welch's t-test, which does not assume equal variances.
Always use Welch's unless you have a specific reason for equal variances.
```

**Paired t-test:**khi các phép đo được thực hiện bằng cặp (một mô hình được đánh giá trên cùng một phân chia dữ liệu):

> **配对 t 检验：**Khi đo lường là kết quả của cùng một mô hình trong cùng một phân chia dữ liệu đánh giá):

```
Compute d_i = x_i - y_i for each pair
Then run a one-sample t-test on the d_i values against mu_0 = 0
```

Trong ML, thử nghiệm t cặp là phổ biến: bạn chạy cả hai mô hình trên cùng 10 gấp hợp xác nhận chéo và so sánh điểm số của chúng theo cặp.

> Trong ML, việc so sánh t  kiểm tra là rất phổ biến: bạn chạy trên hai mô hình trên cùng 10 vòng kiểm tra giao thông, sau đó so sánh số phân số của chúng.

### Kiểm tra hình chữ số.

Kiểm tra chi-quad kiểm tra xem tần số quan sát được phù hợp với tần số dự kiến.

> 卡方检查检查观测频率是否匹配期望频率──适用于分类数据──

```
chi^2 = sum((observed - expected)^2 / expected)

Example: does a language model's output distribution match the
training distribution across categories?

Category    Observed   Expected
Positive       120        100
Negative        80        100
chi^2 = (120-100)^2/100 + (80-100)^2/100 = 4 + 4 = 8

With 1 degree of freedom, chi^2 = 8 gives p < 0.005.
The difference is significant.
```

### A/B Testing for ML Models  A/B Testing of ML 模型

A/B testing trong ML không giống như A/B testing trên web.

> A/B 测试 trong ML khác với A/B 测试 trên WEB

```
1. Same test set:    Both models must be evaluated on identical data.
                     Different test sets make comparison meaningless.

2. Multiple metrics: Accuracy alone is not enough. You need precision,
                     recall, F1, latency, and fairness metrics.

3. Variance:         Use cross-validation or bootstrap to estimate
                     the variance of each metric, not just point estimates.

4. Data leakage:     If the test set was used during model selection,
                     your comparison is biased. Hold out a final test set.
```

**The procedure:**

> **操作步骤：**

```
1. Define your metric and significance level (alpha = 0.05)
2. Run both models on the same k-fold cross-validation splits
3. Collect paired scores: [(a1, b1), (a2, b2), ..., (ak, bk)]
4. Compute differences: d_i = b_i - a_i
5. Run a paired t-test on the differences
6. Check: is the mean difference significantly different from 0?
7. Compute a confidence interval for the mean difference
8. Compute effect size (Cohen's d) to judge practical significance
```

### Tầm quan trọng thống kê so với tầm quan trọng thực tế .

Kết quả có thể có ý nghĩa thống kê nhưng thực tế là vô nghĩa.

> Một kết quả có thể đáng kể về mặt thống kê nhưng thực tế là vô nghĩa. Khi có đủ dữ liệu, ngay cả sự khác biệt nhỏ cũng sẽ trở nên đáng kể về mặt thống kê.

```
Example:
  Model A accuracy: 0.9234
  Model B accuracy: 0.9237
  n = 1,000,000 test samples
  p-value = 0.001

Statistically significant? Yes.
Practically significant? A 0.03% improvement is not worth the
engineering cost of deploying a new model.
```

**Effect size**định lượng sự khác biệt lớn như thế nào, độc lập với kích thước mẫu:

> **效应量**Sự khác biệt về số lượng có nhiều, không liên quan đến số lượng mẫu:

```
Cohen's d = (mean_1 - mean_2) / pooled_std

d = 0.2:  small effect
d = 0.5:  medium effect
d = 0.8:  large effect
```

Luôn báo cáo cả giá trị p và kích thước hiệu ứng. giá trị p cho bạn biết nếu sự khác biệt là thực.

> 始终同时报告 p 值和效应量──p 值告诉你差异是否真实──效应量告诉你差异是否有意义──

### Vấn đề so sánh nhiều lần

Khi bạn kiểm tra nhiều giả thuyết, một số sẽ "có ý nghĩa" bởi tình cờ. Nếu bạn kiểm tra 20 điều ở alpha = 0.05, bạn mong đợi 1 dương tính sai ngay cả khi không có gì là thực.

> Khi bạn kiểm tra nhiều giả thuyết, có một số sẽ ngẫu nhiên" đáng kể". Nếu bạn kiểm tra 20 điều trong alpha = 0.05 , ngay cả khi không có hiệu ứng thực, bạn cũng dự đoán có 1 giả tích cực.

```
P(at least one false positive) = 1 - (1 - alpha)^m

m = 20 tests, alpha = 0.05:
P(false positive) = 1 - 0.95^20 = 0.64

You have a 64% chance of at least one false positive.
```

**Bonferroni correction:**chia alpha bằng số lượng xét nghiệm.

> **Bonferroni 校正：**Để alpha trừ số lần kiểm tra.

```
Adjusted alpha = alpha / m = 0.05 / 20 = 0.0025

Only reject H0 if p-value < 0.0025.
Conservative but simple. Works when tests are independent.
```

Trong ML, điều này quan trọng khi bạn so sánh một mô hình trên nhiều métrics, kiểm tra nhiều cấu hình siêu tham số, hoặc đánh giá trên nhiều tập dữ liệu.

> Trong ML, khi bạn so sánh mô hình trên nhiều chỉ số, kiểm tra nhiều cấu trúc siêu tham số hoặc đánh giá trên nhiều tập dữ liệu, điều này rất quan trọng.

### Bootstrap Methods  Bootstrap Methods

Bootstrapping ước tính phân bố mẫu của một số thống kê bằng cách lấy lại mẫu dữ liệu của bạn bằng cách thay thế. Không cần phải giả định về phân bố cơ bản.

> Bootstrap 通过有放回地重采采数据来估计统计量的抽样分布――不需要对底层分布做任何假设――

**The algorithm:**

> **算法：**

```
1. You have n data points
2. Draw n samples WITH replacement (some points appear multiple times,
   some not at all)
3. Compute your statistic on this bootstrap sample
4. Repeat B times (typically B = 1000 to 10000)
5. The distribution of bootstrap statistics approximates the
   sampling distribution
```

**Bootstrap confidence interval (percentile method):**

> **Bootstrap 置信区间（百分位数法）：**

```
Sort the B bootstrap statistics
95% CI = [2.5th percentile, 97.5th percentile]
```

**Why bootstrap matters for ML:**

> **Bootstrap 对 ML 为什么重要：**

```
- Test set accuracy is a point estimate. Bootstrap gives you
  confidence intervals.
- You cannot assume metric distributions are normal (especially
  for AUC, F1, precision at k).
- Bootstrap works for ANY statistic: median, ratio of two means,
  difference in AUC between two models.
- No closed-form formula needed.
```

**Bootstrap for model comparison:**

> **Bootstrap 用于模型比较：**

```
1. You have predictions from Model A and Model B on the same test set
2. For each bootstrap iteration:
   a. Resample test indices with replacement
   b. Compute metric_A and metric_B on the resampled set
   c. Store diff = metric_B - metric_A
3. 95% CI for the difference:
   [2.5th percentile of diffs, 97.5th percentile of diffs]
4. If the CI does not contain 0, the difference is significant
```

Đây là mạnh hơn so với thử nghiệm t cặp bởi vì nó không đưa ra giả định phân phối.

> Đây là một thử nghiệm ổn định hơn so với các thử nghiệm, vì nó không làm giả định phân bố.

### Các xét nghiệm tham số đối với các xét nghiệm không tham số

**Parametric tests**giả định phân bố cụ thể (thường là bình thường):

> **参数检验**假设特定分布 (thường là phân bố chính xác):

```
t-test:         assumes normally distributed data (or large n by CLT)
ANOVA:          assumes normality and equal variances
Pearson r:      assumes bivariate normality
```

**Non-parametric tests**không đưa ra giả định phân phối:

> **非参数检验**Không làm giả định phân bố:

```
Mann-Whitney U:     compares two groups (replaces independent t-test)
Wilcoxon signed-rank: compares paired data (replaces paired t-test)
Spearman rho:       correlation on ranks (replaces Pearson)
Kruskal-Wallis:     compares multiple groups (replaces ANOVA)
```

**When to use non-parametric:**

> **何时使用非参数检验：**

```
- Small sample size (n < 30) and data is clearly non-normal
- Ordinal data (ratings, rankings)
- Heavy outliers you cannot remove
- Skewed distributions
```

**When to use parametric:**

> **何时使用参数检验：**

```
- Large sample size (CLT makes the test statistic approximately normal)
- Data is roughly symmetric without extreme outliers
- More statistical power (better at detecting real differences)
```

Trong các thí nghiệm ML, bạn thường có n nhỏ (5 hoặc 10 lần xác nhận chéo), vì vậy các thử nghiệm không tham số như Wilcoxon-signed-rank thường phù hợp hơn các thử nghiệm t.

> Trong thí nghiệm ML, bạn thường có n nhỏ hơn 5 hoặc 10 n giao thông), vì vậy như Wilcoxon 符号 秩 như vậy các kiểm tra không tham số thường phù hợp hơn các kiểm tra t hơn.

### Lý thuyết giới hạn trung tâm: Implications Practical ➡️

CLT nói rằng phân phối mẫu phương tiện gần với phân phối bình thường khi n tăng lên, bất kể phân phối dân số cơ bản.

> CLT nói rằng, theo n  tăng trưởng, phân bố giá trị trung bình mẫu gần như là phân bố đúng, bất kể phân bố tổng thể tầng dưới thế nào.

```
If X_1, X_2, ..., X_n are iid with mean mu and variance sigma^2:

    X_bar ~ Normal(mu, sigma^2 / n)    as n -> infinity

Works for n >= 30 in most cases.
For highly skewed distributions, you might need n >= 100.
```

**Why this matters for ML:**

> **这对 ML 为什么重要：**

```
1. Justifies confidence intervals and t-tests on aggregated metrics
2. Explains why averaging over cross-validation folds gives stable
   estimates even when individual folds vary wildly
3. Mini-batch gradient descent works because the average gradient
   over a batch approximates the true gradient (CLT in action)
4. Ensemble methods: averaging predictions from many models gives
   more stable output than any single model
```

**What CLT does NOT do:**

> **CLT 不能做什么：**

```
- Does NOT make your data normal. It makes the MEAN of samples normal.
- Does NOT work for heavy-tailed distributions with infinite variance
  (Cauchy distribution).
- Does NOT apply to dependent data (time series without correction).
```

### Những sai lầm thống kê phổ biến trong các bài báo ML 论文中常见的统计错误

1. **Testing on the training set.**Bảo đảm quá phù hợp. Luôn giữ dữ liệu mà mô hình không thấy trong quá trình đào tạo.

> 1. **在训练集上测试。**Bảo đảm quá phù hợp. Luôn giữ lại dữ liệu chưa từng thấy trong quá trình tập luyện mô hình.

2. **No confidence intervals.**Báo cáo một số chính xác duy nhất mà không có sự không chắc chắn làm cho kết quả không thể tái tạo và không thể xác minh được.

> 2. **没有置信区间。** báo cáo một số chính xác đơn lẻ mà không có thước đo không chắc chắn, làm cho kết quả không thể lặp lại và không thể xác minh được.

3. **Ignoring multiple comparisons.**Kiểm tra 50 cấu hình và báo cáo tốt nhất mà không cần sửa chữa làm tăng tỷ lệ dương tính sai.

> 3. **忽略多重比较。**测试 50 配置并报告 tốt nhất một không làm điều chỉnh, sẽ tăng cường tỷ lệ dương tính giả 

4. **Confusing statistical and practical significance.**Một p-đáng giá 0,001 trên một sự cải thiện độ chính xác 0,01% không có ý nghĩa.

> 4. **混淆统计显著性和实际显著性。**0,01% 精度提升上 p 值 0.001 没有意义──

5. **Using accuracy on imbalanced data.**99% độ chính xác trên một tập dữ liệu với 99% lớp âm nghĩa là mô hình không học được gì.

> 5. **在不平衡数据上使用精度。**Trong 99% dữ liệu loại tiêu cực, 99% độ chính xác có nghĩa là mô hình không học được gì.

6. **Cherry-picking metrics.**Chỉ báo số số liệu mô hình của bạn thắng.

> 6. **挑选指标。**Chỉ báo chỉ số chiến thắng của mô hình của bạn 

7. **Leaking information across train/test splits.**Tiêu chuẩn hóa trước khi chia, hoặc sử dụng dữ liệu trong tương lai để dự đoán quá khứ.

> 7. **在训练/测试划分之间泄露信息。**Trong phân chia trước làm phân tích, hoặc sử dụng dữ liệu dự đoán quá khứ trong tương lai.

8. **Small test sets with no variance estimates.**Đánh giá trên 100 mẫu và tuyên bố cải thiện 2% là tiếng ồn, không phải tín hiệu.

> 8. **小测试集没有方差估计。**Trong 100 mẫu đánh giá, họ tuyên bố 2% tăng là tiếng ồn, không phải là tín hiệu.

9. **Assuming independence when data is not independent.**Hình ảnh y tế từ cùng một bệnh nhân, nhiều câu từ cùng một tài liệu.

> 9. **数据不独立时假设独立。**Từ hình ảnh y tế của cùng bệnh nhân, từ nhiều câu trong cùng tài liệu.

10. **P-hacking.**Thử thử các thử nghiệm khác nhau, các bộ phụ hoặc các tiêu chí loại trừ cho đến khi bạn có được p < 0,05. Kết quả là một tạo vật của tìm kiếm.

> 10. **P 值操纵（P-hacking）。**尝试不同的检查、子集或排除标准, cho đến khi có được p < 0.05── kết quả là hình ảnh giả của quá trình tìm kiếm──

## Xây dựng nó.

Bạn sẽ thực hiện:

> Bạn sẽ thực hiện:

1. **Descriptive statistics from scratch**(tỷ lệ trung bình, trung bình, chế độ, lệch chuẩn, phần trăm, IQR)
   **从零实现描述性统计**(tỷ lệ trung bình, số lượng lớn, tiêu chuẩn khác nhau, tỷ lệ trung bình, IQR)
2. **Correlation functions**(Pearson và Spearman, với matrix tính hợp lệ)
   **相关函数**(Pearson và Spearman, cũng như các phương diện khác nhau)
3. **Hypothesis tests**(một mẫu thử nghiệm t, hai mẫu thử nghiệm t, thử nghiệm chi vuông)
   **假设检验**(单样本 t 检验、两样本 t 检验、卡方检验)
4. **Bootstrap confidence intervals**(cho bất kỳ thống kê nào, không cần phải giả định)
   **Bootstrap 置信区间**(tương tự thống kê, không cần giả định)
5. **A/B test simulator**(tạo dữ liệu, kiểm tra, kiểm tra lỗi loại I và loại II)
   **A/B 测试模拟器**(tạo dữ liệu, kiểm tra, kiểm tra lớp 1 và lớp 2 sai lầm)
6. **Statistical vs practical significance demo**(khải thị rằng n lớn làm cho mọi thứ "có ý nghĩa")
   **统计 vs 实际显著性演示**(khải thị lớn n 使 tất cả mọi thứ" đáng chú ý")

Tất cả từ đầu, chỉ sử dụng `math`và `random`Không có người đùa, không có người đùa.

> Tất cả từ không thực hiện, chỉ sử dụng `math`和 `random`❖不使用 numpy、scipy。

## Từ khóa  Từ khóa nhanh chóng
```figure
f3-bootstrap-resample
```

## Các điều khoản chính

| Term / 术语 | Definition / 定义 |
|---|---|
| Mean / 均值 | Sum of values divided by count. Sensitive to outliers. / 值的总和除以个数。对异常值敏感。 |
| Median / 中位数 | Middle value of sorted data. Robust to outliers. / 排序后数据的中间值。对异常值稳健。 |
| Standard deviation / 标准差 | Square root of variance. Measures spread in original units. / 方差的平方根。用原始单位衡量离散程度。 |
| Percentile / 百分位数 | Value below which a given percentage of data falls. / 给定百分比的数据低于此值。 |
| IQR / 四分位距 | Interquartile range. Q3 minus Q1. The spread of the middle 50%. / 四分位距。Q3 减 Q1。中间 50% 的展幅。 |
| Pearson correlation / Pearson 相关系数 | Measures linear association between two variables. Range [-1, 1]. / 衡量两个变量间的线性关联。范围 [-1, 1]。 |
| Spearman correlation / Spearman 相关系数 | Measures monotonic association using ranks. / 用排名衡量单调关联。 |
| Covariance matrix / 协方差矩阵 | Matrix of pairwise covariances between all features. / 所有特征间成对协方差的矩阵。 |
| Null hypothesis / 零假设 | Default assumption of no effect or no difference. / 无效应或无差异的默认假设。 |
| p-value / p 值 | Probability of data this extreme given the null hypothesis is true. / 在零假设为真的条件下观察到如此极端数据的概率。 |
| Confidence interval / 置信区间 | Range of plausible values for a parameter at a given confidence level. / 给定置信水平下参数的合理值范围。 |
| t-test / t 检验 | Tests whether means differ significantly. Uses the t-distribution. / 检验均值是否有显著差异。使用 t 分布。 |
| Chi-squared test / 卡方检验 | Tests whether observed frequencies differ from expected frequencies. / 检验观测频率是否与期望频率不同。 |
| Effect size / 效应量 | Magnitude of a difference, independent of sample size. Cohen's d is common. / 差异的大小，与样本量无关。常用 Cohen's d。 |
| Bonferroni correction / Bonferroni 校正 | Divides significance threshold by number of tests to control false positives. / 将显著性阈值除以检验次数以控制假阳性。 |
| Bootstrap / Bootstrap | Resampling with replacement to estimate sampling distributions. / 有放回重采样以估计抽样分布。 |
| Type I error / 第一类错误 | False positive. Rejecting H0 when it is true. / 假阳性。H0 为真时拒绝 H0。 |
| Type II error / 第二类错误 | False negative. Failing to reject H0 when it is false. / 假阴性。H0 为假时未能拒绝 H0。 |
| Statistical power / 统计功效 | Probability of correctly rejecting a false H0. Power = 1 minus Type II error rate. / 正确拒绝假 H0 的概率。功效 = 1 减第二类错误率。 |
| Central limit theorem / 中心极限定理 | Sample means converge to a normal distribution as sample size grows. / 样本均值随样本量增大趋近于正态分布。 |
| Parametric test / 参数检验 | Assumes a specific distribution for the data (usually normal). / 假设数据服从特定分布（通常是正态分布）。 |
| Non-parametric test / 非参数检验 | Makes no distributional assumptions. Works on ranks or signs. / 不做分布假设。基于排名或符号工作。 |
