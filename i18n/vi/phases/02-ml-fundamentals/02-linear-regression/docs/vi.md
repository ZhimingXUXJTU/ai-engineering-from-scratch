# Sự lùi lại tuyến tính
# Lòng quay lại


> Sự lùi lại tuyến tính vẽ đường thẳng tốt nhất qua dữ liệu của bạn. Đó là "thế giới chào" của máy học.

> 线性回归穿越你的数据画出最佳直线――它是机器学习的"Hello World"――

**Type:** Build | **类型：** 构建
**Languages:** Python
**Prerequisites:** Phase 1 (Linear Algebra, Calculus, Optimization), Phase 2 Lesson 1 | **前置知识：** Phase 1（线性代数、微积分、优化），Phase 2 第 1 课
**Time:** ~90 minutes | **时间：** 约 90 分钟

## Mục tiêu học tập

- Thuộc dẫn các quy tắc cập nhật giảm gradient cho lỗi trung bình vuông và thực hiện hồi quy tuyến tính từ đầu
  推导平均差的梯度下降更新规则并从零实现线性回归
- So sánh sự giảm gradient và phương trình bình thường về độ phức tạp tính toán và khi nào sử dụng mỗi
  So sánh độ giảm và phức tạp tính toán của phương trình chính thức, quyết định khi sử dụng riêng
- Xây dựng mô hình hồi quy tuyến tính nhiều với tiêu chuẩn hóa tính năng và giải thích các trọng lượng được học
  构建带特征标准化的多线性归归归模型并解释学习到的权重
- Giải thích cách thức quay trở lại của Ridge (L2 quy định) ngăn chặn quá phù hợp bằng cách phạt trọng lượng lớn
  解释 Ridge quay trở lại (L2) 正则化) Làm thế nào để thông qua trừng phạt quyền lực lớn để ngăn chặn quá phù hợp


> **【中文解读】**
> Lòng quay lại xơ là mô hình dự đoán đơn giản nhất sử dụng một dòng đường thẳng (hoặc siêu phẳng) để phù hợp với dữ liệu. Nó cũng là mạng thần kinh đơn giản nhất: một mạng không có tầng ẩn, không có chức năng kích hoạt.

> **【拓展：线性回归在真实 AI 系统中的角色】**
> Mặc dù "đọc sâu" được quan tâm nhiều hơn, nhưng tính năng quay lại vẫn là một trong những mô hình được sử dụng phổ biến nhất trong ngành công nghiệp. Google sử dụng rất nhiều tính năng quay lại trong phân tích A / B để ước tính hiệu ứng của kết quả; Uber sử dụng tính năng quay lại để làm cho nhu cầu dự đoán cơ sở; Phương pháp Fama-Pharanh của mô hình ba yếu tố bản chất là tính năng quay lại đa dạng. Trong cuộc thi Kaggle, tính năng quay lại thường là cơ sở, hiệu quả của công trình tính năng kiểm chứng nhanh.

## Vấn đề  vấn đề giới thiệu

Bạn có dữ liệu: kích thước nhà và giá bán của chúng. Bạn muốn dự đoán giá của một ngôi nhà mới với kích thước của nó. Bạn có thể nhìn vào nó trên một cục phân tán, nhưng bạn cần một công thức. Bạn cần một đường phù hợp nhất với dữ liệu để bạn có thể cắm vào bất kỳ kích thước và có được dự đoán giá.

> Bạn có dữ liệu: diện tích nhà và giá bán đối ứng. Bạn có thể xem xét giá dựa trên diện tích nhà mới. Bạn có thể xem xét trên biểu đồ phân tán, nhưng bạn cần một công thức. Bạn cần một đường phù hợp nhất, vì vậy bạn có thể có được giá dự đoán.

Lịch lý quay lại tuyến tính cho bạn đường thẳng đó. Quan trọng hơn, nó giới thiệu toàn bộ vòng đào tạo ML: xác định mô hình, xác định hàm chi phí, tối ưu hóa các tham số. Mỗi thuật toán ML theo cùng một mô hình này. Kiểm soát nó ở đây với trường hợp đơn giản nhất, và bạn sẽ nhận ra nó ở khắp mọi nơi.

> Lập lại về tuyến tính cho bạn cung cấp đường dây đó. Quan trọng hơn, nó giới thiệu toàn bộ vòng tròn đào tạo ML: định nghĩa mô hình, định nghĩa hàm giá, tối ưu hóa các tham số. Mỗi thuật toán ML đều theo cùng một mô hình. Trong trường hợp đơn giản nhất này, bạn có thể nhận ra nó ở bất cứ đâu.

Đây không chỉ là cho các vấn đề đơn giản. Sự lùi ngược tuyến tính được sử dụng trong các hệ thống sản xuất để dự đoán nhu cầu, phân tích thử nghiệm A / B, mô hình hóa tài chính và như là cơ sở cho mọi nhiệm vụ lùi ngược.

> Đây không chỉ là một vấn đề đơn giản. Lợi lượng quay lại được sử dụng trong hệ thống sản xuất để dự đoán nhu cầu, phân tích A/B, xây dựng tài chính, cũng như là cơ sở của mỗi nhiệm vụ quay lại.

> **【中文解读】**
> Lần quay lại không chỉ là một sự hiểu biết nhập học, mà còn là một kết hợp của toàn bộ vòng tròn đào tạo máy học: định nghĩa mô hình → định nghĩa hàm mất → tối ưu hóa các tham số.

## Khái niệm cốt lõi

### Mô hình

Sự lùi lại tuyến tính giả định một mối quan hệ tuyến tính giữa đầu vào (x) và đầu ra (y):

> 线性归归假设输入 (x) và输出 (y) 之间存在线性关系:

```
y = wx + b
```

- `w`( trọng lượng/ độ nghiêng): y thay đổi bao nhiêu khi x tăng 1
  `w`(权重/斜率):x 增加 1 时 y 变化多少
- `b`(vi-se/cắt lưng): giá trị của y khi x = 0
  `b`(偏置/截距): Khi x = 0 时 y 的值

Đối với nhiều đầu vào (các tính năng), điều này mở rộng đến:

> 对于多个输入(特征), mở rộng为:

```
y = w1*x1 + w2*x2 + ... + wn*xn + b
```

Hoặc trong dạng vector: `y = w^T * x + b`

> hoặc dùng向量形式表示:`y = w^T * x + b`

Mục tiêu: tìm các giá trị của w và b làm cho y dự đoán gần như có thể với y thực tế trong tất cả các ví dụ đào tạo.

> 目标: tìm giá trị của w 和 b, làm cho tất cả các mô hình đào tạo trong dự đoán của y 尽可能接近 thực tế của y ⋅

> **【中文解读】**
> 线性归归的模型非常直观:`y = wx + b`,w là độ nghiêng (权重),b là độ cắt (偏置) ⋅多种情况下变化`y = w1*x1 + w2*x2 + ... + wn*xn + b`, bằng cách sử dụng dữ liệu siêu phẳng phù hợp. Mục tiêu của việc đào tạo là tìm ra những điểm tốt nhất w và b, làm cho sự khác biệt giữa giá trị dự đoán và giá trị thực tối thiểu.

### Chức năng chi phí (Lỗi bình phương trung bình)

Bạn cần một số đơn để ghi lại những dự đoán sai lầm của bạn.

> Bạn cần một loại hình có thể ghi nhận mức độ sai lầm dự đoán.

```
MSE = (1/n) * sum((y_predicted - y_actual)^2)
```

Tại sao vuông? Hai lý do. Thứ nhất, nó phạt lỗi lớn hơn các lỗi nhỏ (một lỗi 10 là 100x tồi tệ hơn một lỗi 1, không phải 10x). Thứ hai, hàm vuông là mượt mà và có thể phân biệt ở mọi nơi, điều này làm cho tối ưu hóa dễ dàng hơn.

> Tại sao sử dụng vuông? hai lý do. Thứ nhất, nó có thể trừng phạt lỗi lớn hơn so với lỗi nhỏ hơn.

Chức năng chi phí tạo ra bề mặt. Đối với một trọng lượng đơn w và thiên hướng b, bề mặt MSE trông giống như một bát (một hình phẳng ngọc).

> 代价函数 tạo ra một曲面── đối với một trọng lượng đơn lẻ w 和偏置 b,MSE 曲面 trông giống như một bát (凸抛物面)── mặt dưới của bát là MSE 最小的地方──训练就是找到那个底部──

### Sự giảm dần

Giảm dần tìm ra đáy bát bằng cách thực hiện các bước xuống đồi.

> 梯度下降通过向下走步来找到碗底部.

```mermaid
flowchart TD
    A[Initialize w and b randomly] --> B[Compute predictions: y_hat = wx + b]
    B --> C[Compute cost: MSE]
    C --> D[Compute gradients: dMSE/dw, dMSE/db]
    D --> E[Update parameters]
    E --> F{Cost low enough?}
    F -->|No| B
    F -->|Yes| G[Done: optimal w and b found]
```

Các gradient cho bạn biết hai điều: hướng nào để di chuyển từng tham số, và bao nhiêu để di chuyển.

> 梯度 cho bạn biết hai điều: mỗi tham số nên di chuyển theo hướng nào, và di chuyển bao nhiêu.

Đối với MSE với y_hat = wx + b:

> 对于 MSE 且 y_hat = wx + b:

```
dMSE/dw = (2/n) * sum((y_hat - y) * x)
dMSE/db = (2/n) * sum(y_hat - y)
```

Quy tắc cập nhật:

> 更新规则:

```
w = w - learning_rate * dMSE/dw
b = b - learning_rate * dMSE/db
```

Tốc độ học tập kiểm soát kích thước bước quá lớn: bạn vượt quá mức tối thiểu và đi xa. quá nhỏ: đào tạo mất mãi mãi.

> Học tập tỷ lệ kiểm soát bước dài. : bạn sẽ nhảy qua giá trị tối thiểu và phát triển. : tập luyện cần thời gian dài.

> **【中文解读】**
> 梯度下降 là thuật toán tối ưu hóa trung tâm nhất của machine learning. Nhìn giác của nó rất đơn giản: đứng trên đồi, hướng đi một bước, lặp lại cho đến khi đạt đến đáy谷. 梯度(导数) cho bạn biết hướng và độ, tỷ lệ học tập kiểm soát bước nhỏ.

> **【拓展：梯度下降在现代 AI 中的演进】**
> GPT-4 được đào tạo bằng cách sử dụng bộ điều chỉnh AdamW  tối ưu hóa máy (Adam + 权重衰减), nó là biến thể cao cấp giảm thang, nhưng ý tưởng cốt lõi vẫn là "nghĩa hướng theo thang" ( along the gradient direction, one step).

### Phương trình bình thường (Solution Closed Form)

Đối với sự lùi lại tuyến tính cụ thể, có một công thức trực tiếp cho trọng lượng tối ưu mà không có bất kỳ lặp lại nào:

> Khusus đối với quay lại tuyến tính, có một công thức trực tiếp không cần phải có quá trình để cung cấp quyền tối ưu:

```
w = (X^T * X)^(-1) * X^T * y
```

Điều này đảo ngược một số liệu để giải quyết cho w trong một bước. Nó hoạt động hoàn hảo cho các tập dữ liệu nhỏ. Đối với các tập dữ liệu lớn (mọi triệu hàng hoặc hàng ngàn tính năng), giảm gradient được ưa thích vì sự đảo ngược của số liệu là O(n^3) trong số lượng các tính năng.

> Đây là một phương pháp tìm kiếm các bước ngược cho các tập hợp dữ liệu nhỏ rất hiệu quả. Đối với tập hợp dữ liệu lớn, thang độ giảm tốt hơn, bởi vì các tập hợp tìm kiếm ngược trên số tính năng là O (n^3) của.

> **【拓展：正规方程 vs 梯度下降的选择】**
> Sự phức tạp thời gian của phương trình thông thường là O (n^3) (n) là số tính năng), khi các tính năng vượt quá hàng ngàn lần tính toán cực chậm. Mô hình học sâu có hàng tỷ tham số, chỉ có thể sử dụng thang xuống.

### Sự lùi lại hàng tuyến

Với nhiều tính năng, mô hình trở thành:

> Có nhiều đặc điểm, mô hình biến đổi:

```
y = w1*x1 + w2*x2 + ... + wn*xn + b
```

Mọi thứ đều hoạt động giống nhau: MSE là hàm chi phí, độ giảm gradient cập nhật tất cả các trọng lượng cùng một lúc.

> Tất cả nguyên tắc đều giống nhau:MSE là hàm giá, thang độ giảm đồng thời cập nhật quyền trọng lượng.

Nếu một tính năng dao động từ 0 đến 1 và một tính năng khác dao động từ 0 đến 1.000.000, giảm độ nghiêng sẽ khó khăn vì bề mặt chi phí trở nên dài.

> Tính năng thu hẹp ở đây rất quan trọng. Nếu một tính năng có phạm vi từ 0 đến 1, một tính năng khác là 0 đến 1,000,000, độ giảm sẽ trở nên khó khăn, vì giá cả sẽ tăng lên.

> **【中文解读】**
> Trong quá trình quay lại đa dạng, tính năng thu hẹp là rất quan trọng. Nếu tính năng khác biệt cấp lượng rất lớn (như diện tích 500-3000 so với số phòng ngủ 1-5), hàm mất mát giảm độ sẽ bị kéo dài nghiêm trọng, dẫn đến sự chậm lại hoặc thậm chí không thể nhận được.

### Phục hồi đa nôn

Nếu mối quan hệ không phải là tuyến tính thì sao? Bạn vẫn có thể sử dụng sự lùi lại tuyến tính bằng cách tạo các tính năng đa nôn:

> Nếu mối quan hệ không phải là tuyến tính thì bạn có thể tiếp tục sử dụng các tính năng liên kết bằng cách tạo nhiều tính năng:

```
y = w1*x + w2*x^2 + w3*x^3 + b
```

Đây vẫn là sự hồi quy "lín" bởi vì mô hình là tuyến tính trong trọng lượng (w1, w2, w3). Bạn chỉ sử dụng các tính năng không tuyến tính của x.

> Đây vẫn là "lợi lý" trở lại, bởi vì mô hình ở trọng lượng (w1, w2, w3) trên là tuyến tính. Bạn chỉ sử dụng các đặc điểm không tuyến tính của x.

Các đa nguyên cấp cao hơn có thể phù hợp với các đường cong phức tạp hơn nhưng có nguy cơ quá phù hợp. Một đa nguyên cấp 10 sẽ đi qua mọi điểm trong một tập dữ liệu 10 điểm nhưng dự đoán kém về dữ liệu mới.

> Một hệ số đa số cao có thể phù hợp với đường cong phức tạp hơn nhưng có rủi ro phù hợp hơn. Một hệ số đa số 10 lần sẽ đi qua mỗi điểm trong 10 tập hợp dữ liệu, nhưng dự đoán trên dữ liệu mới rất kém.

### Điểm số R-Tứ

MSE cho bạn biết bạn sai, nhưng số lượng phụ thuộc vào quy mô của y. R-quadrat (R^2) cho một thước đo độc lập quy mô:

> MSE  nói với bạn đã sai nhiều, nhưng con số này phụ thuộc vào lượng y của y. R-quad (R ^ 2)  cho một lượng không liên quan đến lượng:

```
R^2 = 1 - (sum of squared residuals) / (sum of squared deviations from mean)
    = 1 - SS_res / SS_tot
```

- R^2 = 1,0: dự đoán hoàn hảo
  R^2 = 1.0:完美预测
- R^2 = 0.0: mô hình không tốt hơn so với dự đoán trung bình mỗi lần
  R^2 = 0.0: mô hình không so với giá trị trung bình dự đoán tốt
- R^2 < 0.0: mô hình tồi tệ hơn dự đoán trung bình
  R^2 < 0.0: mô hình so với dự đoán trung bình giá trị còn khác

### Hình trước quy định (Ridge Regression)

Khi bạn có nhiều tính năng, mô hình có thể overfit bằng cách gán trọng lượng lớn.

> Khi bạn có nhiều đặc điểm, mô hình có thể thông qua trao quyền trọng lượng lớn để được phù hợp.

```
Cost = MSE + lambda * sum(w_i^2)
```

Từ phạt ngăn cản trọng lượng lớn. Lambda siêu tham số kiểm soát sự đổi giá: lambda cao hơn có nghĩa là trọng lượng nhỏ hơn và quy định hơn.

> 惩罚项阻止权重过大──超参数 lambda 控制权衡:lambda 越大意味着权重越小、正则化越强── điều này sẽ được thảo luận sâu sắc trong các bài học tiếp theo── bây giờ chỉ cần hiểu được sự tồn tại và tác dụng của nó──

> **【中文解读】**
> Ridge quay trở lại(L2 正则化) thông qua việc thêm trọng lượng vuông và của trừng phạt trong hàm mất để ngăn chặn quá phù hợp。直觉: hạn chế trọng lượng lớn, buộc mô hình "保守" sử dụng đặc điểm, thay vì dựa vào một đặc điểm của cực trọng để phù hợp với tiếng ồn。正则化强度由 lambda 控制lambda 越大,权重越小,模型越简单。 đây là một trong những kỹ thuật phổ biến nhất trong việc học sâu.

## Hãy xây dựng nó.
```figure
linear-regression-fit
```

## Hãy xây dựng nó

### Bước 1: Tạo dữ liệu mẫu

```python
import random
import math

random.seed(42)  # 设置随机种子以确保结果可复现

TRUE_W = 3.0  # 真实斜率（权重）
TRUE_B = 7.0  # 真实截距（偏置）
N_SAMPLES = 100  # 样本数量

X = [random.uniform(0, 10) for _ in range(N_SAMPLES)]  # 生成 0-10 之间的随机特征值
y = [TRUE_W * x + TRUE_B + random.gauss(0, 2.0) for x in X]  # 真实关系 + 高斯噪声

print(f"Generated {N_SAMPLES} samples")
print(f"True relationship: y = {TRUE_W}x + {TRUE_B} (+ noise)")
print(f"First 5 points: {[(round(X[i], 2), round(y[i], 2)) for i in range(5)]}")
```

### Bước 2: Khản hồi tuyến tính từ đầu với sự giảm gradient

```python
class LinearRegression:
    def __init__(self, learning_rate=0.01):
        self.w = 0.0  # 权重初始化为 0
        self.b = 0.0  # 偏置初始化为 0
        self.lr = learning_rate  # 学习率控制梯度下降步长
        self.cost_history = []  # 记录每轮的损失值

    def predict(self, X):
        return [self.w * x + self.b for x in X]  # y_hat = wx + b

    def compute_cost(self, X, y):
        predictions = self.predict(X)
        n = len(y)
        # 计算 MSE：均方误差
        cost = sum((pred - actual) ** 2 for pred, actual in zip(predictions, y)) / n
        return cost

    def compute_gradients(self, X, y):
        predictions = self.predict(X)
        n = len(y)
        # 对 w 的偏导数
        dw = (2 / n) * sum((pred - actual) * x for pred, actual, x in zip(predictions, y, X))
        # 对 b 的偏导数
        db = (2 / n) * sum(pred - actual for pred, actual in zip(predictions, y))
        return dw, db

    def fit(self, X, y, epochs=1000, print_every=200):
        for epoch in range(epochs):
            dw, db = self.compute_gradients(X, y)  # 计算梯度
            self.w -= self.lr * dw  # 沿梯度反方向更新权重
            self.b -= self.lr * db  # 沿梯度反方向更新偏置
            cost = self.compute_cost(X, y)
            self.cost_history.append(cost)
            if epoch % print_every == 0:
                print(f"  Epoch {epoch:4d} | Cost: {cost:.4f} | w: {self.w:.4f} | b: {self.b:.4f}")
        return self

    def r_squared(self, X, y):
        predictions = self.predict(X)
        y_mean = sum(y) / len(y)
        ss_res = sum((actual - pred) ** 2 for actual, pred in zip(y, predictions))  # 残差平方和
        ss_tot = sum((actual - y_mean) ** 2 for actual in y)  # 总变差
        return 1 - (ss_res / ss_tot)  # R² = 1 - SS_res/SS_tot


print("=== Training Linear Regression (Gradient Descent) ===")
model = LinearRegression(learning_rate=0.005)
model.fit(X, y, epochs=1000, print_every=200)
print(f"\nLearned: y = {model.w:.4f}x + {model.b:.4f}")
print(f"True:    y = {TRUE_W}x + {TRUE_B}")
print(f"R-squared: {model.r_squared(X, y):.4f}")
```

### Bước 3: Phương trình bình thường (trình thức đóng)

```python
class LinearRegressionNormal:
    def __init__(self):
        self.w = 0.0  # 斜率
        self.b = 0.0  # 截距

    def fit(self, X, y):
        n = len(X)
        x_mean = sum(X) / n  # 计算 x 的均值
        y_mean = sum(y) / n  # 计算 y 的均值
        # 协方差 / 方差 = 最优斜率
        numerator = sum((X[i] - x_mean) * (y[i] - y_mean) for i in range(n))
        denominator = sum((X[i] - x_mean) ** 2 for i in range(n))
        self.w = numerator / denominator
        # 截距 = y 均值 - 斜率 * x 均值
        self.b = y_mean - self.w * x_mean
        return self

    def predict(self, X):
        return [self.w * x + self.b for x in X]

    def r_squared(self, X, y):
        predictions = self.predict(X)
        y_mean = sum(y) / len(y)
        ss_res = sum((actual - pred) ** 2 for actual, pred in zip(y, predictions))
        ss_tot = sum((actual - y_mean) ** 2 for actual in y)
        return 1 - (ss_res / ss_tot)


print("\n=== Normal Equation (Closed-Form) ===")
model_normal = LinearRegressionNormal()
model_normal.fit(X, y)
print(f"Learned: y = {model_normal.w:.4f}x + {model_normal.b:.4f}")
print(f"R-squared: {model_normal.r_squared(X, y):.4f}")
```

### Bước 4: Sự lùi lại tuyến tính nhiều

```python
class MultipleLinearRegression:
    def __init__(self, n_features, learning_rate=0.01):
        self.weights = [0.0] * n_features
        self.bias = 0.0
        self.lr = learning_rate
        self.cost_history = []

    def predict_single(self, x):
        return sum(w * xi for w, xi in zip(self.weights, x)) + self.bias

    def predict(self, X):
        return [self.predict_single(x) for x in X]

    def compute_cost(self, X, y):
        predictions = self.predict(X)
        n = len(y)
        return sum((pred - actual) ** 2 for pred, actual in zip(predictions, y)) / n

    def fit(self, X, y, epochs=1000, print_every=200):
        n = len(y)
        n_features = len(X[0])
        for epoch in range(epochs):
            predictions = self.predict(X)
            errors = [pred - actual for pred, actual in zip(predictions, y)]
            for j in range(n_features):
                grad = (2 / n) * sum(errors[i] * X[i][j] for i in range(n))
                self.weights[j] -= self.lr * grad
            grad_b = (2 / n) * sum(errors)
            self.bias -= self.lr * grad_b
            cost = self.compute_cost(X, y)
            self.cost_history.append(cost)
            if epoch % print_every == 0:
                print(f"  Epoch {epoch:4d} | Cost: {cost:.4f}")
        return self

    def r_squared(self, X, y):
        predictions = self.predict(X)
        y_mean = sum(y) / len(y)
        ss_res = sum((actual - pred) ** 2 for actual, pred in zip(y, predictions))
        ss_tot = sum((actual - y_mean) ** 2 for actual in y)
        return 1 - (ss_res / ss_tot)


random.seed(42)
N = 100
X_multi = []
y_multi = []
for _ in range(N):
    size = random.uniform(500, 3000)
    bedrooms = random.randint(1, 5)
    age = random.uniform(0, 50)
    price = 50 * size + 10000 * bedrooms - 1000 * age + 50000 + random.gauss(0, 20000)
    X_multi.append([size, bedrooms, age])
    y_multi.append(price)


def standardize(X):
    n_features = len(X[0])
    means = [sum(X[i][j] for i in range(len(X))) / len(X) for j in range(n_features)]
    stds = []
    for j in range(n_features):
        variance = sum((X[i][j] - means[j]) ** 2 for i in range(len(X))) / len(X)
        stds.append(variance ** 0.5)
    X_scaled = []
    for i in range(len(X)):
        row = [(X[i][j] - means[j]) / stds[j] if stds[j] > 0 else 0 for j in range(n_features)]
        X_scaled.append(row)
    return X_scaled, means, stds


y_mean_val = sum(y_multi) / len(y_multi)
y_std_val = (sum((yi - y_mean_val) ** 2 for yi in y_multi) / len(y_multi)) ** 0.5
y_scaled = [(yi - y_mean_val) / y_std_val for yi in y_multi]

X_scaled, x_means, x_stds = standardize(X_multi)

print("\n=== Multiple Linear Regression (3 features) ===")
print("Features: house size, bedrooms, age")
multi_model = MultipleLinearRegression(n_features=3, learning_rate=0.01)
multi_model.fit(X_scaled, y_scaled, epochs=1000, print_every=200)

print(f"\nWeights (standardized): {[round(w, 4) for w in multi_model.weights]}")
print(f"Bias (standardized): {multi_model.bias:.4f}")
print(f"R-squared: {multi_model.r_squared(X_scaled, y_scaled):.4f}")
```

### Bước 5: Phục hồi đa nôn

```python
class PolynomialRegression:
    def __init__(self, degree, learning_rate=0.01):
        self.degree = degree
        self.weights = [0.0] * degree
        self.bias = 0.0
        self.lr = learning_rate

    def make_features(self, X):
        return [[x ** (d + 1) for d in range(self.degree)] for x in X]

    def predict(self, X):
        features = self.make_features(X)
        return [sum(w * f for w, f in zip(self.weights, row)) + self.bias for row in features]

    def fit(self, X, y, epochs=1000, print_every=200):
        features = self.make_features(X)
        n = len(y)
        for epoch in range(epochs):
            predictions = [sum(w * f for w, f in zip(self.weights, row)) + self.bias for row in features]
            errors = [pred - actual for pred, actual in zip(predictions, y)]
            for j in range(self.degree):
                grad = (2 / n) * sum(errors[i] * features[i][j] for i in range(n))
                self.weights[j] -= self.lr * grad
            grad_b = (2 / n) * sum(errors)
            self.bias -= self.lr * grad_b
            if epoch % print_every == 0:
                cost = sum(e ** 2 for e in errors) / n
                print(f"  Epoch {epoch:4d} | Cost: {cost:.6f}")
        return self

    def r_squared(self, X, y):
        predictions = self.predict(X)
        y_mean = sum(y) / len(y)
        ss_res = sum((actual - pred) ** 2 for actual, pred in zip(y, predictions))
        ss_tot = sum((actual - y_mean) ** 2 for actual in y)
        return 1 - (ss_res / ss_tot)


random.seed(42)
X_poly = [x / 10.0 for x in range(0, 50)]
y_poly = [0.5 * x ** 2 - 2 * x + 3 + random.gauss(0, 1.0) for x in X_poly]

x_max = max(abs(x) for x in X_poly)
X_poly_norm = [x / x_max for x in X_poly]
y_poly_mean = sum(y_poly) / len(y_poly)
y_poly_std = (sum((yi - y_poly_mean) ** 2 for yi in y_poly) / len(y_poly)) ** 0.5
y_poly_norm = [(yi - y_poly_mean) / y_poly_std for yi in y_poly]

print("\n=== Polynomial Regression (degree 2 vs degree 5) ===")
print("True relationship: y = 0.5x^2 - 2x + 3")

print("\nDegree 2:")
poly2 = PolynomialRegression(degree=2, learning_rate=0.1)
poly2.fit(X_poly_norm, y_poly_norm, epochs=2000, print_every=500)
print(f"  R-squared: {poly2.r_squared(X_poly_norm, y_poly_norm):.4f}")

print("\nDegree 5:")
poly5 = PolynomialRegression(degree=5, learning_rate=0.1)
poly5.fit(X_poly_norm, y_poly_norm, epochs=2000, print_every=500)
print(f"  R-squared: {poly5.r_squared(X_poly_norm, y_poly_norm):.4f}")

print("\nDegree 2 fits the true curve well. Degree 5 fits training data slightly better")
print("but risks overfitting on new data.")
```

### Bước 6: Khản hồi đồi (L2 quy định)

```python
class RidgeRegression:
    def __init__(self, n_features, learning_rate=0.01, alpha=1.0):
        self.weights = [0.0] * n_features
        self.bias = 0.0
        self.lr = learning_rate
        self.alpha = alpha

    def predict_single(self, x):
        return sum(w * xi for w, xi in zip(self.weights, x)) + self.bias

    def predict(self, X):
        return [self.predict_single(x) for x in X]

    def fit(self, X, y, epochs=1000, print_every=200):
        n = len(y)
        n_features = len(X[0])
        for epoch in range(epochs):
            predictions = self.predict(X)
            errors = [pred - actual for pred, actual in zip(predictions, y)]
            mse = sum(e ** 2 for e in errors) / n
            reg_term = self.alpha * sum(w ** 2 for w in self.weights)
            cost = mse + reg_term
            for j in range(n_features):
                grad = (2 / n) * sum(errors[i] * X[i][j] for i in range(n))
                grad += 2 * self.alpha * self.weights[j]
                self.weights[j] -= self.lr * grad
            grad_b = (2 / n) * sum(errors)
            self.bias -= self.lr * grad_b
            if epoch % print_every == 0:
                print(f"  Epoch {epoch:4d} | Cost: {cost:.4f} | L2 penalty: {reg_term:.4f}")
        return self


print("\n=== Ridge Regression (L2 Regularization) ===")
print("Same data as multiple regression, with alpha=0.1")
ridge = RidgeRegression(n_features=3, learning_rate=0.01, alpha=0.1)
ridge.fit(X_scaled, y_scaled, epochs=1000, print_every=200)
print(f"\nRidge weights: {[round(w, 4) for w in ridge.weights]}")
print(f"Plain weights: {[round(w, 4) for w in multi_model.weights]}")
print("Ridge weights are smaller (shrunk toward zero) due to the L2 penalty.")
```

## Hãy sử dụng nó để thực hiện

Bây giờ điều tương tự với scikit-learn, đó là những gì bạn thực sự sẽ sử dụng trong sản xuất.

> Bây giờ sử dụng scikit-learn để thực hiện cùng một chức năng, đây là công cụ bạn sử dụng trong sản xuất thực tế.

```python
from sklearn.linear_model import LinearRegression as SklearnLR
from sklearn.linear_model import Ridge
from sklearn.preprocessing import PolynomialFeatures, StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score
import numpy as np

# 生成与从零实现相同的数据
np.random.seed(42)
X_sk = np.random.uniform(0, 10, (100, 1))
y_sk = 3.0 * X_sk.squeeze() + 7.0 + np.random.normal(0, 2.0, 100)

# 划分训练集和测试集（80/20）
X_train, X_test, y_train, y_test = train_test_split(X_sk, y_sk, test_size=0.2, random_state=42)

# 线性回归
lr = SklearnLR()
lr.fit(X_train, y_train)
y_pred = lr.predict(X_test)

print("=== Scikit-learn Linear Regression ===")
print(f"Coefficient (w): {lr.coef_[0]:.4f}")
print(f"Intercept (b): {lr.intercept_:.4f}")
print(f"R-squared (test): {r2_score(y_test, y_pred):.4f}")
print(f"MSE (test): {mean_squared_error(y_test, y_pred):.4f}")

# 多项式回归（degree=2）
poly = PolynomialFeatures(degree=2, include_bias=False)
X_poly_sk = poly.fit_transform(X_train)  # 生成 x, x² 特征
X_poly_test = poly.transform(X_test)

lr_poly = SklearnLR()
lr_poly.fit(X_poly_sk, y_train)
print(f"\nPolynomial degree 2 R-squared: {r2_score(y_test, lr_poly.predict(X_poly_test)):.4f}")

# 标准化后使用 Ridge 回归
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)  # 在训练集上拟合并转换
X_test_scaled = scaler.transform(X_test)  # 在测试集上只转换

ridge = Ridge(alpha=1.0)  # alpha 即正则化强度 lambda
ridge.fit(X_train_scaled, y_train)
print(f"Ridge R-squared: {r2_score(y_test, ridge.predict(X_test_scaled)):.4f}")
print(f"Ridge coefficient: {ridge.coef_[0]:.4f}")
```

Việc thực hiện từ đầu và scikit-learn của bạn tạo ra kết quả tương tự. Sự khác biệt: scikit-learn xử lý các trường hợp cạnh, ổn định số và tối ưu hóa hiệu suất. Sử dụng thư viện để sản xuất. Sử dụng phiên bản từ đầu để hiểu những gì đang xảy ra.

> Sự khác biệt nằm ở: học tập nhỏ xử lý tình huống biên giới, ổn định số và tối ưu hóa hiệu suất, sử dụng trong sản xuất, sử dụng từ phiên bản 0.

## Chuyển nó đi.

Bài học này mang lại:
- `outputs/skill-regression.md`- kỹ năng để chọn cách tiếp cận hồi quy đúng đắn dựa trên vấn đề

> 本课产 出:
> - `outputs/skill-regression.md`- Một kỹ năng về cách chọn đúng cách trở lại dựa trên vấn đề

## Tập luyện bài tập

1. Thực hiện giảm độ sốc hàng loạt, giảm độ sốc stochastic (SGD), và giảm độ sốc hàng loạt nhỏ. So sánh tốc độ hội tụ trên cùng một tập dữ liệu.
   1. 实现批量梯度下降,随机梯度下降 (SGD) 和小批量梯度下降.
2. Tạo dữ liệu từ hàm khối (y = ax^3 + bx^2 + cx + d + tiếng ồn). Phù hợp nhiều chữ số của độ 1, 3 và 10. So sánh đào tạo R^2 và thử nghiệm R^2.
   2. Từ 3 hàm (y = ax^3 + bx^2 + cx + d + noise) 生成数据──拟合 1、3 和 10 次多项式──比较训练 R^2 和测试 R^2──几次多项式时过拟合变得明显吗?
3. Thực hiện hồi quy Lasso (L1 regularization: penalty alpha *(((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((
   3. 实现 Lasso 回归(L1 正则化:penalty * alpha sum *(((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((

## Từ khóa  Từ khóa nhanh chóng

| Term | What people say | What it actually means |
|------|----------------|----------------------|
| Linear regression | "Draw a line through data" | Find weight w and bias b that minimize the sum of squared differences between wx+b and actual y values |
| Cost function | "How bad the model is" | A function that maps model parameters to a single number measuring prediction error, which optimization minimizes |
| Mean squared error | "Average of squared errors" | (1/n) * sum of (predicted - actual)^2, penalizing large errors disproportionately |
| Gradient descent | "Walk downhill" | Iteratively adjust parameters in the direction that reduces the cost function, using partial derivatives |
| Learning rate | "Step size" | A scalar that controls how much parameters change per gradient descent step |
| Normal equation | "Solve it directly" | The closed-form solution w = (X^T X)^-1 X^T y that gives optimal weights without iteration |
| R-squared | "How good the fit is" | The fraction of variance in y explained by the model, ranging from negative infinity to 1.0 |
| Feature scaling | "Make features comparable" | Transforming features to similar ranges (e.g., zero mean, unit variance) so gradient descent converges faster |
| Regularization | "Penalize complexity" | Adding a term to the cost function that shrinks weights, preventing overfitting |
| Ridge regression | "L2 regularization" | Linear regression with a penalty of lambda * sum(w_i^2) added to MSE |
| Polynomial regression | "Fitting curves with linear math" | Linear regression on polynomial features (x, x^2, x^3, ...), still linear in the weights |
| Overfitting | "Memorizing training data" | Using a model so complex that it fits noise in training data and fails on new data |

## Xem thêm 延伸阅读

- [An Introduction to Statistical Learning (ISLR)](https://www.statlearning.com/)-- PDF miễn phí, chương 3 và 6 bao gồm sự lùi lại tuyến tính và quy định với các ví dụ R thực tế
  [An Introduction to Statistical Learning (ISLR)](https://www.statlearning.com/)-- 免费教材, Chương 3 và Chương 6 sử dụng thực tế R ví dụ bao gồm đường dẫn trở lại và chính thức hóa
- [The Elements of Statistical Learning (ESL)](https://hastie.su.domains/ElemStatLearn/)-- miễn phí PDF, là một người bạn toán học hơn với ISLR với điều trị sâu hơn của sườn núi và lasso
  [The Elements of Statistical Learning (ESL)](https://hastie.su.domains/ElemStatLearn/)- 免费教材,ISLR 的数学版,对 ridge 和 lasso có một xử lý sâu hơn
- [Stanford CS229 Lecture Notes on Linear Regression](https://cs229.stanford.edu/main_notes.pdf)-- Các ghi chú của Andrew Ng lấy phương trình bình thường và sự giảm gradient từ các nguyên tắc đầu tiên
  [Stanford CS229 Lecture Notes on Linear Regression](https://cs229.stanford.edu/main_notes.pdf)- ghi chú của Andrew Ng từ nguyên tắc đầu tiên của quy định quy định và thang độ giảm
- [scikit-learn LinearRegression documentation](https://scikit-learn.org/stable/modules/linear_model.html)-- tham khảo thực tế cho LinearRegression, Ridge, Lasso và ElasticNet với các ví dụ mã
  [scikit-learn LinearRegression documentation](https://scikit-learn.org/stable/modules/linear_model.html)-- LinearRegression、Ridge、Lasso 和 ElasticNet's thực tế tham khảo及代码 ví dụ
