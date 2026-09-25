# 概率 và phân bố

> Khả năng là ngôn ngữ AI sử dụng để thể hiện sự không chắc chắn.
> 概率 là AI biểu hiện ngôn ngữ không chắc chắn.

**Type:** Learn | **类型:** 学习
**Language:**Python**语言:**Python
**Prerequisites:** Phase 1, Lessons 01-04 | **前置知识:** Phase 1, Lessons 01-04
**Time:** ~75 minutes | **时间:** ~75 分钟

## Mục tiêu học tập

- Thực hiện PMF và PDF từ đầu cho phân phối Bernoulli, categorical, Poisson, đồng nhất và bình thường
- Xét giá trị dự kiến, sự khác biệt và sử dụng định lý giới hạn trung tâm để giải thích lý do tại sao người Gauss chiếm ưu thế
- Xây dựng các hàm softmax và log-softmax bằng thủ thuật ổn định số (từ logit max)
- Xét mất tích entropy chéo từ logits và kết nối nó với xác suất log âm

> **【中文解读】**
> 概率 là AI biểu hiện ngôn ngữ không chắc chắn. 概率 phân bố, mô hình ngôn ngữ từ 50.000 từ ứng cử viên theo mẫu概率, mô hình phổ biến từ phân bố học tập tạo ra hình ảnh.

> **【拓展：概率在 AI 中的位置】**
> - **Softmax**: Chuyển đầu ra mạng thần kinh thành phân bố xác suất, là bước cuối cùng của tất cả các mô hình phân loại.
> - **交叉熵损失**: Cấp độ mất mát của các nhiệm vụ, tương đương với số lượng tương tự.
> - **高斯分布**Trung tâm giới hạn giải thích tại sao cao được phân phối rất phổ biến trong thiên nhiên và AI.

## Vấn đề  vấn đề giới thiệu

> **【中文解读】**分类器输出 `[0.03, 0.91, 0.06]`(91% 概率是猫), mô hình ngôn ngữ được chọn từ 50.000 từ trong các từ 候选, mô hình phổ biến được chọn từ phân bố được học, tạo ra hình ảnh.

## Khái niệm cốt lõi

> **【拓展：概率分布是 AI 生成模型的基础】**生成模型 (VAE、GAN、扩散模型) là trung tâm của phân bố xác suất: học đến một phân bố dữ liệu p(x), sau đó từ trung ỏi tạo ra dữ liệu mới.

Mỗi dự đoán mà mô hình đưa ra là phân bố xác suất. Mỗi hàm mất mát đo lường sự phân bố dự đoán xa như thế nào so với sự phân bố thực. Mỗi bước đào tạo điều chỉnh các tham số để làm cho một phân bố trông giống như một phân bố khác hơn. Nếu không có xác suất, bạn không thể đọc một bài báo ML duy nhất, sửa lỗi một mô hình duy nhất, hoặc hiểu tại sao mất mát đào tạo của bạn là NaN.

> Mỗi dự đoán của mô hình là một phân bố xác suất. Mỗi hàm mất đo sự khác biệt giữa phân bố dự đoán và phân bố thực tế. Mỗi bước tập tập đều điều chỉnh các tham số để làm cho một phân bố gần gũi hơn với một khác. Không hiểu xác suất, bạn đã không thể đọc bài báo, điều chỉnh mô hình hoặc hiểu tại sao mất tập là NaN.

## Khái niệm cốt lõi

### Sự kiện, không gian mẫu và khả năng

Không gian mẫu S là tập hợp tất cả các kết quả có thể. Một sự kiện là một bộ phận của không gian mẫu.

> 样本空间 S là tập hợp tất cả các kết quả có thể. Sự kiện là tập hợp của 样本空间.

```
Coin flip:
  S = {H, T}
  P(H) = 0.5,  P(T) = 0.5

Single die roll:
  S = {1, 2, 3, 4, 5, 6}
  P(even) = P({2, 4, 6}) = 3/6 = 0.5
```

Ba định nghĩa định nghĩa xác suất:
1. P(A) >= 0 cho bất kỳ sự kiện nào A
2. P(S) = 1 (một cái gì đó luôn xảy ra)
3. P(A hoặc B) = P(A) + P(B) khi A và B không thể xảy ra cả hai

> 概率论由三条公理定义:
> 1. Đối với bất kỳ sự kiện A,P(A) >= 0
> 2. P (S) = 1 (Nó chắc chắn sẽ có một số kết quả xảy ra)
> 3. 当 A 和 B 不能同时发生时,P(A 或 B) = P(A) + P(B)

Mọi thứ khác (định lý Bayes, kỳ vọng, phân phối) đều theo sau ba quy tắc này.

> Mọi thứ khác đều được dẫn dắt bởi những quy tắc này.

### Có thể có điều kiện và độc lập

P ((A) là xác suất của A cho rằng B đã xảy ra.

> P (A) là tỷ lệ xảy ra của A trong điều kiện B đã xảy ra.

```
P(A|B) = P(A and B) / P(B)

Example: deck of cards
  P(King | Face card) = P(King and Face card) / P(Face card)
                      = (4/52) / (12/52)
                      = 4/12 = 1/3
```

Hai sự kiện độc lập khi biết một không nói gì về người khác:

> Hai sự kiện độc lập là biết rằng một trong hai sẽ không nói với bạn bất cứ thông tin nào về một sự kiện khác:

```
Independent:   P(A|B) = P(A)
Equivalent to: P(A and B) = P(A) * P(B)
```

Việc đánh tiền xu là độc lập, và việc rút thẻ mà không có người thay thế thì không.

> Đưa tiền tệ là độc lập.

### Vận động cơ lượng xác suất so với Vận động mật độ xác suất

Các biến ngẫu nhiên nhỏ có hàm khối lượng xác suất (PMF). Mỗi kết quả có xác suất cụ thể mà bạn có thể đọc trực tiếp.

> 离散随机变量有概率质量函数 (PMF) ⋅ mỗi kết quả có một概率 cụ thể có thể trực tiếp đọc được ⋅

```
PMF: P(X = k)

Fair die:
  P(X = 1) = 1/6
  P(X = 2) = 1/6
  ...
  P(X = 6) = 1/6

  Sum of all probabilities = 1
```

Các biến ngẫu nhiên liên tục có hàm mật độ xác suất (PDF). mật độ tại một điểm không phải là xác suất.

> 连续随机变量有概率密度函数 (PDF) ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅                                                                                                                                                                                            

```
PDF: f(x)

P(a <= X <= b) = integral of f(x) from a to b

f(x) can be greater than 1 (density, not probability)
integral from -inf to +inf of f(x) dx = 1
```

Sự phân biệt này quan trọng trong ML. Các sản phẩm phân loại là PMF (các lựa chọn riêng biệt).

> Đây là một sự khác biệt rất quan trọng trong ML.

### Phân phối chung

**Bernoulli:**Một thử nghiệm, hai kết quả.

> **伯努利分布：**Một thử nghiệm, hai kết quả.

```
P(X = 1) = p
P(X = 0) = 1 - p
Mean = p,  Variance = p(1-p)
```

**Categorical:**Một thử nghiệm, k kết quả. Mô hình phân loại đa lớp (tạo ra tối đa mềm).

> **分类分布：**Một lần thử nghiệm, kết quả khác nhau.

```
P(X = i) = p_i,  where sum of p_i = 1
Example: P(cat) = 0.7,  P(dog) = 0.2,  P(bird) = 0.1
```

**Uniform:**được sử dụng để khởi tạo ngẫu nhiên.

> **均匀分布：**Tất cả kết quả và tỷ lệ xuất hiện.

```
Discrete: P(X = k) = 1/n for k in {1, ..., n}
Continuous: f(x) = 1/(b-a) for x in [a, b]
```

**Normal (Gaussian):**đường cong chuông. được định nghĩa bằng trung bình (mu) và biến số (sigma^2).

> **正态（高斯）分布：**钟形曲线──由均值 (mu) 和方差 (sigma^2) 参数化──

```
f(x) = (1 / sqrt(2*pi*sigma^2)) * exp(-(x - mu)^2 / (2*sigma^2))

Standard normal: mu = 0, sigma = 1
  68% of data within 1 sigma
  95% within 2 sigma
  99.7% within 3 sigma
```

**Poisson:**Số lượng các sự kiện hiếm trong một khoảng thời gian cố định.

> **泊松分布：**Số lượng các sự kiện hiếm trong khu vực cố định.

```
P(X = k) = (lambda^k * e^(-lambda)) / k!
Mean = lambda,  Variance = lambda
```

### Giá trị dự kiến và sự khác biệt

Giá trị dự kiến là kết quả trung bình trọng lượng.

> 期望值是加权平均结果──

```
Discrete:   E[X] = sum of x_i * P(X = x_i)
Continuous: E[X] = integral of x * f(x) dx
```

Các biện pháp biến thể được trải rộng xung quanh trung bình.

> 方差 đo lường mức độ phân tán xung quanh giá trị trung bình.

```
Var(X) = E[(X - E[X])^2] = E[X^2] - (E[X])^2
Standard deviation = sqrt(Var(X))
```

Trong ML, giá trị dự kiến xuất hiện như hàm mất (sự mất trung bình trên phân phối dữ liệu).

> Trong ML, giá trị dự kiến biểu hiện là hàm mất mát (đối thiểu mất mát trên phân bố dữ liệu), độ khác nhau cho bạn biết mô hình ổn định.

### Phân phối chung và biên giới

Một phân phối chung P ((X, Y) mô tả hai biến ngẫu nhiên cùng nhau.

> 联合分布 P(X, Y)  mô tả hai biến động tự nhiên xuất hiện cùng một lúc.

Ví dụ về PMF chung (X = thời tiết, Y = dù):
联合 PMF示例(X = 天气,Y = 是否带):

| | Y=0 (no umbrella / 不带伞) | Y=1 (umbrella / 带伞) | Marginal P(X) / 边缘 P(X) |
|---|---|---|---|
| X=0 (sun / 晴天) | 0.40 | 0.10 | P(X=0) = 0.50 |
| X=1 (rain / 下雨) | 0.05 | 0.45 | P(X=1) = 0.50 |
| **Marginal P(Y) / 边缘 P(Y)** | P(Y=0) = 0.45 | P(Y=1) = 0.55 | 1.00 |

Phân bố biên cộng lại biến khác:

> 边缘 phân phối qua một biến đổi khác

```
P(X = x) = sum over all y of P(X = x, Y = y)
```

Tổng hàng và cột trong bảng trên là biên giới.

> Trong bảng trên, các tập hợp và tập hợp là phân bố bên cạnh.

### Tại sao sự phân phối bình thường xuất hiện khắp nơi

Định lý giới hạn trung tâm: tổng (hoặc trung bình) của nhiều biến ngẫu nhiên độc lập hội tụ với phân bố bình thường, bất kể phân bố ban đầu.

> Trung tâm极限理: Nhiều biến số độc lập và (hoặc trung bình) thu được đến phân bố đúng trạng thái, bất kể phân bố nguyên thủy là gì.

```
Roll 1 die:  uniform distribution (flat)
Average of 2 dice:  triangular (peaked)
Average of 30 dice: nearly perfect bell curve

This works for ANY starting distribution.
```

Đây là lý do tại sao:
- Các lỗi đo lường là bình thường (nhiều nguồn độc lập nhỏ)
  Trung ngữ翻译:测量误差近似正态 (由许多小的独立来源叠加)
- Các khởi tạo trọng lượng trong mạng thần kinh sử dụng phân phối bình thường
  Trung ngữ翻译:权重初始化使用正态分布
- Âm thanh gradient trong SGD là bình thường (tổng số các gradient mẫu)
  Trung ngữ翻译:SGD 中的梯度噪音近似正态(许多样本梯度的总和)
- Phân bố bình thường là phân bố entropy tối đa cho một trung bình và sự biến động nhất định
  Trung ngữ翻译: 正态分布是给定平均值和方差下最大分布

### Khoản log

Những xác suất nguyên liệu gây ra các vấn đề số.

> Sự xác suất ban đầu sẽ dẫn đến vấn đề số lượng.

```
P(sentence) = P(word1) * P(word2) * ... * P(word_n)
            = 0.01 * 0.003 * 0.02 * ...
            -> 0.0 (underflow after ~30 terms)
```

Log xác suất sửa chữa điều này.

> Đối với số xác suất giải quyết vấn đề này.

```
log P(sentence) = log P(word1) + log P(word2) + ... + log P(word_n)
                = -4.6 + -5.8 + -3.9 + ...
                -> finite number (no underflow)
```

Quy tắc:
- log(a * b) = log(a) + log(b)
- xác suất log luôn là <= 0 (vì 0 < P <= 1)
- Thêm âm tính = ít khả năng
- Thiệt hại giao hợp là xác suất log âm của lớp chính xác

> Quy tắc:
> - log(a * b) = log(a) + log(b)
> - Đối với số tỷ lệ thường là <= 0(vì 0 < P <= 1)
> - 越负 = 越不可能
> - 交叉损失就是正确类别的负对数概率

### Softmax như một phân phối xác suất

Các mạng thần kinh phát ra điểm số thô (logits). Softmax chuyển đổi chúng thành phân bố xác suất hợp lệ.

> 神经网络输出原始分数(logits) ――Softmax sẽ chuyển chúng thành phân bố xác suất hiệu quả―

```
softmax(z_i) = exp(z_i) / sum(exp(z_j) for all j)

Properties:
  - All outputs are in (0, 1)
  - All outputs sum to 1
  - Preserves relative ordering of inputs
  - exp() amplifies differences between logits
```

Trù mềmmax: trừ logit tối đa trước khi tăng số để ngăn chặn quá tải.

> Softmax 技巧: trong取指数 trước khi giảm logit tối đa, ngăn ngừa溢出。

```
z = [100, 101, 102]
exp(102) = overflow

z_shifted = z - max(z) = [-2, -1, 0]
exp(0) = 1  (safe)

Same result, no overflow.
```

Log-softmax kết hợp softmax và log cho sự ổn định số. PyTorch sử dụng điều này bên trong để mất entropy chéo.

> Log-softmax sẽ làm cho softmax và log 合并 một bước để giữ sự ổn định số lượng.

### Tiêu chuẩn

Phân tích mẫu có nghĩa là rút ra các giá trị ngẫu nhiên từ phân phối.
- Thả các mẫu ngẫu nhiên mà các tế bào thần kinh để nới
  Trung ngữ翻译:Dropout 随机采样决定哪些神经元置零
- Dữ liệu tăng cường mẫu biến đổi ngẫu nhiên
  Trung ngữ翻译: dữ liệu tăng cường采样随机变化
- Các mô hình ngôn ngữ lấy mẫu token tiếp theo từ phân phối dự đoán
  Trung文翻译:语言模型从预测分布中采样下一个词
- Các mô hình phân phối lấy mẫu tiếng ồn và dần dần tiêu diệt
  Trung ngữ翻译:扩散模型采样噪音并逐步去噪音

Việc lấy mẫu từ phân phối tùy tiện đòi hỏi các kỹ thuật như lấy mẫu biến đổi ngược, lấy mẫu từ chối hoặc thủ thuật tái định đo (chỉ được sử dụng trong VAEs).

> Từ phân bố tùy chọn trong mẫu cần phải ngược thay đổi trong mẫu, từ chối trong mẫu hoặc kỹ thuật tái số hóa (VAE trong sử dụng) và các kỹ thuật khác.

## Hãy xây dựng nó.
```figure
gaussian-pdf
```

## Hãy xây dựng nó

### Bước 1: Các cơ sở xác suất

```python
import math
import random

def factorial(n):
    result = 1
    for i in range(2, n + 1):
        result *= i
    return result

def combinations(n, k):
    return factorial(n) // (factorial(k) * factorial(n - k))

def conditional_probability(p_a_and_b, p_b):
    return p_a_and_b / p_b

p_king_given_face = conditional_probability(4/52, 12/52)
print(f"P(King | Face card) = {p_king_given_face:.4f}")
```

### Bước 2: PMF và PDF từ đầu

```python
def bernoulli_pmf(k, p):
    return p if k == 1 else (1 - p)

def categorical_pmf(k, probs):
    return probs[k]

def poisson_pmf(k, lam):
    return (lam ** k) * math.exp(-lam) / factorial(k)

def uniform_pdf(x, a, b):
    if a <= x <= b:
        return 1.0 / (b - a)
    return 0.0

def normal_pdf(x, mu, sigma):
    coeff = 1.0 / (sigma * math.sqrt(2 * math.pi))
    exponent = -0.5 * ((x - mu) / sigma) ** 2
    return coeff * math.exp(exponent)
```

### Bước 3: Giá trị dự kiến và sự khác biệt

```python
def expected_value(values, probabilities):
    return sum(v * p for v, p in zip(values, probabilities))

def variance(values, probabilities):
    mu = expected_value(values, probabilities)
    return sum(p * (v - mu) ** 2 for v, p in zip(values, probabilities))

die_values = [1, 2, 3, 4, 5, 6]
die_probs = [1/6] * 6
mu = expected_value(die_values, die_probs)
var = variance(die_values, die_probs)
print(f"Die: E[X] = {mu:.4f}, Var(X) = {var:.4f}, SD = {var**0.5:.4f}")
```

### Bước 4: Tiêu mẫu từ phân phối

```python
def sample_bernoulli(p, n=1):
    return [1 if random.random() < p else 0 for _ in range(n)]

def sample_categorical(probs, n=1):
    cumulative = []
    total = 0
    for p in probs:
        total += p
        cumulative.append(total)
    samples = []
    for _ in range(n):
        r = random.random()
        for i, c in enumerate(cumulative):
            if r <= c:
                samples.append(i)
                break
    return samples

def sample_normal_box_muller(mu, sigma, n=1):
    samples = []
    for _ in range(n):
        u1 = random.random()
        u2 = random.random()
        z = math.sqrt(-2 * math.log(u1)) * math.cos(2 * math.pi * u2)
        samples.append(mu + sigma * z)
    return samples
```

### Bước 5: Softmax và xác suất log

```python
def softmax(logits):
    max_logit = max(logits)
    shifted = [z - max_logit for z in logits]
    exps = [math.exp(z) for z in shifted]
    total = sum(exps)
    return [e / total for e in exps]

def log_softmax(logits):
    max_logit = max(logits)
    shifted = [z - max_logit for z in logits]
    log_sum_exp = max_logit + math.log(sum(math.exp(z) for z in shifted))
    return [z - log_sum_exp for z in logits]

def cross_entropy_loss(logits, target_index):
    log_probs = log_softmax(logits)
    return -log_probs[target_index]
```

### Bước 6: Phương pháp giới hạn trung tâm

```python
def demonstrate_clt(dist_fn, n_samples, n_averages):
    averages = []
    for _ in range(n_averages):
        samples = [dist_fn() for _ in range(n_samples)]
        averages.append(sum(samples) / len(samples))
    return averages
```

### Bước 7: Hình ảnh

```python
import matplotlib.pyplot as plt

xs = [mu + sigma * (i - 500) / 100 for i in range(1001)]
ys = [normal_pdf(x, mu, sigma) for x, mu, sigma in ...]
plt.plot(xs, ys)
```

Các thực hiện đầy đủ với tất cả các hình ảnh hóa là trong `code/probability.py`- Tôi không biết.

> 包含所有可见的完整实现见`code/probability.py`

## Hãy sử dụng nó để thực hiện

Với NumPy và SciPy, tất cả trên đều là một dòng:

> Sử dụng NumPy và SciPy, tất cả các chức năng trên chỉ cần một dòng mã:

```python
import numpy as np
from scipy import stats

normal = stats.norm(loc=0, scale=1)
samples = normal.rvs(size=10000)
print(f"Mean: {np.mean(samples):.4f}, Std: {np.std(samples):.4f}")
print(f"P(X < 1.96) = {normal.cdf(1.96):.4f}")

logits = np.array([2.0, 1.0, 0.1])
from scipy.special import softmax, log_softmax
probs = softmax(logits)
log_probs = log_softmax(logits)
print(f"Softmax: {probs}")
print(f"Log-softmax: {log_probs}")
```

Anh đã xây dựng những cái này từ đầu rồi, giờ anh biết những gì thư viện gọi đang làm.

> Bạn đã xây dựng những thứ này từ không. Bây giờ bạn biết các hàm thư viện đang làm gì.

## Tập luyện bài tập

1. Thực hiện lấy mẫu biến đổi ngược cho phân bố theo hàm số. Kiểm tra bằng cách lấy mẫu 10.000 giá trị và so sánh histogram với PDF thực.

2. Xây dựng một bảng phân phối chung cho hai con số đốm có tải, tính toán các phân phối biên và kiểm tra xem các con số đốm có độc lập hay không.

3. Xét mất lượng entropy chéo cho một phân loại 5 lớp xuất logits `[2.0, 0.5, -1.0, 3.0, 0.1]`khi lớp đúng là chỉ số 3. Sau đó xác minh câu trả lời của bạn với PyTorch `nn.CrossEntropyLoss`- Tôi không biết.

4. Viết một hàm lấy danh sách xác suất log và trả lại chuỗi có khả năng nhất, tổng xác suất log và xác suất nguyên thô tương đương.

## Từ khóa  Từ khóa nhanh chóng

| Term | What people say | What it actually means |
|------|----------------|----------------------|
| Sample space | "All the possibilities" / "所有可能性" | The set S of every possible outcome of an experiment / 实验所有可能结果的集合 S |
| PMF | "The probability function" / "概率函数" | A function that gives the exact probability of each discrete outcome, summing to 1 / 给出每个离散结果精确概率的函数，总和为 1 |
| PDF | "The probability curve" / "概率曲线" | A density function for continuous variables. Integrate it over an interval to get probability / 连续变量的密度函数，在区间上积分得到概率 |
| Conditional probability | "Probability given something" / "条件概率" | P(A\|B) = P(A and B) / P(B). The foundation of Bayesian thinking and Bayes' theorem / 贝叶斯思维和贝叶斯定理的基础 |
| Independence | "They don't affect each other" / "互不影响" | P(A and B) = P(A) * P(B). Knowing one event tells you nothing about the other / 知道一个事件不影响另一个 |
| Expected value | "The average" / "平均值" | The probability-weighted sum of all outcomes. The loss function is an expected value / 所有结果的概率加权求和，损失函数就是一种期望值 |
| Variance | "How spread out" / "离散程度" | The expected squared deviation from the mean. High variance = noisy, unstable estimates / 偏离均值的平方的期望，方差大 = 噪声大、不稳定 |
| Normal distribution | "The bell curve" / "钟形曲线" | f(x) = (1/sqrt(2*pi*sigma^2)) * exp(-(x-mu)^2/(2*sigma^2)). Appears everywhere due to the CLT / 因中心极限定理而无处不在 |
| Central Limit Theorem | "Averages become normal" / "平均趋于正态" | The mean of many independent samples converges to a normal distribution regardless of the source / 许多独立样本的均值收敛到正态分布 |
| Joint distribution | "Two variables together" / "两个变量一起" | P(X, Y) describes the probability of every combination of X and Y outcomes / 描述 X 和 Y 每种组合的概率 |
| Marginal distribution | "Sum out the other variable" / "消去另一个变量" | P(X) = sum_y P(X, Y). Recovers one variable's distribution from the joint / 从联合分布中恢复单个变量的分布 |
| Log probability | "Log of the probability" / "概率的对数" | log P(x). Turns products into sums, preventing numerical underflow in long sequences / 将乘法变加法，防止长序列数值下溢 |
| Softmax | "Turn scores into probabilities" / "分数转概率" | softmax(z_i) = exp(z_i) / sum(exp(z_j)). Maps real-valued logits to a valid probability distribution / 将实数值 logits 映射为有效概率分布 |
| Cross-entropy | "The loss function" / "损失函数" | -sum(p_true * log(p_predicted)). Measures how different two distributions are. Lower is better / 衡量两个分布的差异，越小越好 |
| Logits | "Raw model outputs" / "模型原始输出" | Unnormalized scores before softmax. Named after the logistic function / softmax 之前的未归一化分数 |
| Sampling | "Drawing random values" / "随机取值" | Generating values according to a probability distribution. How models generate output / 按概率分布生成值，模型用它生成输出 |

## Xem thêm 延伸阅读

- [3Blue1Brown: But what is the Central Limit Theorem?](https://www.youtube.com/watch?v=zeJD6dqJ5lo)- bằng chứng trực quan về lý do tại sao trung bình trở nên bình thường
- [Stanford CS229 Probability Review](https://cs229.stanford.edu/section/cs229-prob.pdf)- tham chiếu ngắn gọn bao gồm tất cả mọi thứ ở đây và nhiều hơn nữa
- [The Log-Sum-Exp Trick](https://gregorygundersen.com/blog/2020/02/09/log-sum-exp/)- tại sao sự ổn định số lượng quan trọng và làm thế nào để đạt được nó
