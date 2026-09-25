# Phương pháp lấy mẫu

> Tiêu mẫu là cách AI khám phá không gian của khả năng.
> 采样是 AI 探索空间可能性的方式.

**Type:** Build | **类型:** 动手
**Language:**Python**语言:**Python
**Prerequisites:** Phase 1, Lessons 06-07 (Probability, Bayes' Theorem) | **前置知识:** Phase 1, 第 06-07 课（概率、贝叶斯定理）
**Time:** ~120 minutes | **时间:** ~120 分钟

## Mục tiêu học tập

- Thực hiện ngược CDF, từ chối và quan trọng lấy mẫu từ đầu chỉ sử dụng số ngẫu nhiên đồng nhất
  Sử dụng trung bình theo số từ 0 thực hiện ngược lại CDF (Công dụng ngược lại CDF) 拒绝采样 (Công dụng ngược lại CDF) 拒绝采样 (Công dụng ngược lại CDF) 拒绝采样 (Công dụng ngược lại CDF) 及重要性采样 (Công dụng ngược lại CDF) 重要性采样 (Công dụng ngược lại CDF)
- Xây dựng mô hình nhiệt độ, top-k và top-p (tâm) để tạo token mô hình ngôn ngữ
  构建用于语言模型代号 生成的温度、top-k 和 top-p(nucleus)采样
- Giải thích thủ thuật tái định đo lường và lý do tại sao nó cho phép lây lan ngược thông qua lấy mẫu trong VAEs
  解释重参数化技巧(Reparameterization Trick) và tại sao nó có thể giúp cho các hoạt động trong VAE hỗ trợ chống phát tán
- Tiến hành Metropolis-Hastings MCMC để lấy mẫu từ phân phối mục tiêu không bình thường
  运行 Metropolis-Hastings MCMC Từ chưa được phân phối mục tiêu phân bố trong采样


> **【中文解读】**
> 采样是 AI 探索可能性的方式──LLM sử dụng nhiệt độ/top-k/top-p 控制文本生成多样性──VAE sử dụng kỹ thuật phân tích nặng để tạo mẫu nhỏ──扩散模型的前向过程是采样(加噪),反向过程是去噪生成 ().

## Vấn đề  vấn đề giới thiệu

Một mô hình ngôn ngữ hoàn thành xử lý yêu cầu của bạn và tạo ra một vector 50.000 logit, một cho mỗi token trong từ vựng của nó. Bây giờ nó phải chọn một. Làm thế nào?

> 语言模型 xử lý xong lời khuyên của bạn, sẽ tạo ra một khối lượng có chứa 50.000 logit, đối với mỗi token trong bảng từ ngữ.

Nếu nó luôn chọn mã hiệu có khả năng cao nhất, mọi phản ứng đều giống nhau. Định nghĩa. Chán chán. Nếu nó chọn một cách ngẫu nhiên, kết quả là nhầm lẫn. Câu trả lời sống ở đâu đó giữa những cực đoan này, và ở đâu đó được kiểm soát bằng cách lấy mẫu.

> Nếu mỗi lần chọn mã thông báo xác suất cao nhất, mỗi lần trả lời đều giống nhau  xác định  không trò chuyện  Nếu mỗi lần chọn tùy chọn, đầu ra là 胡言乱语.

Việc lấy mẫu không giới hạn trong việc tạo văn bản. Học tập tăng cường ước tính các gradient chính sách bằng cách lấy mẫu quỹ đạo. VAE học các đại diện ẩn bằng cách lấy mẫu từ các phân phối được học và lây lan ngược qua sự ngẫu nhiên. Các mô hình phân tán tạo ra hình ảnh bằng cách lấy mẫu tiếng ồn và lặp đi lặp lại. Phương pháp Monte Carlo ước tính các tích hợp không có giải pháp hình thức đóng. Các thuật toán MCMC khám phá các phân phối hậu chiều cao không thể đếm được.

> 采样不仅限于文本生成――强化学习通过采样轨迹(轨迹) 来估计策略梯度──VAE 通过从学习到分布中采样并反向传播来学习隐表示──扩散模型通过采样噪音并代去噪声来生成图像──蒙特卡洛方法估算没有解析的积分──MCMC 算法探索无法枚举的高维后验分布──

Mỗi hệ thống AI tạo ra là một hệ thống lấy mẫu. Chiến lược lấy mẫu xác định chất lượng, đa dạng và khả năng kiểm soát của sản phẩm. Bài học này xây dựng mọi phương pháp lấy mẫu lớn từ đầu, bắt đầu từ các số ngẫu nhiên đồng nhất và kết thúc với các kỹ thuật cung cấp năng lượng cho LLM và mô hình tạo ra hiện đại.

> Mỗi hệ thống AI được tạo ra về bản chất là một hệ thống lấy mẫu. Chiến lược lấy mẫu quyết định chất lượng, đa dạng và khả năng kiểm soát của sản phẩm.

## Khái niệm cốt lõi

> **【中文解读】**
> 采样问题无处不在: ngôn ngữ模型 phải được chọn từ 50.000 token 中选一个,VAE phải được chọn từ ẩn không gian,扩散模型 phải được chọn từ tiếng ồn từng bước sang tiếng ồn.

### Tại sao việc lấy mẫu là quan trọng

Việc lấy mẫu xuất hiện trong bốn vai trò cơ bản trên AI và học máy:

> 采样 trong AI và máy học đóng bốn vai trò cơ bản:

**Generation.**Các mô hình ngôn ngữ, mô hình phân tán và GAN đều tạo ra sản lượng bằng cách lấy mẫu.

> **生成。**语言模型、扩散模型和GAN đều thông qua 采样产生输出──采样算法 trực tiếp kiểm soát năng lực sáng tạo、连贯性和多样性──温度、top-k 和核采样是工程师每天调节的"旋"──

**Training.**Các mẫu giảm gradient stochastic nhỏ. Các mẫu bỏ neuron để vô hiệu hóa. Các mẫu tăng dữ liệu biến đổi ngẫu nhiên.

> **训练。**随机梯度下降(SGD)采样 mini-batch──Dropout 采样要禁用神经元──数据增强采样随机变化──重要性采样重新加权样样以降强化学习──PPO、TRPO) trong 梯度方差──

**Estimation.**Nhiều lượng trong ML không có giải pháp hình thức đóng. Sự mất mát dự kiến trên phân phối dữ liệu, chức năng phân vùng của một mô hình dựa trên năng lượng, bằng chứng trong suy luận Bayesian.

> **估计。**Nhiều số lượng trong ML không được giải quyết. Khối thâm lý dự kiến trên phân bố dữ liệu, hàm phân chia dựa trên mô hình năng lượng, bằng chứng trong giả thuyết Bayes.

**Exploration.**Các thuật toán MCMC khám phá các phân bố sau trong suy luận Bayesian. Chiến lược tiến hóa lấy mẫu các nhiễu thông số.

> **探索。**MCMC 算法 trong Bayesian推断探索后验分布──进化策略──Evolutionary Strategies) 采样参数扰动──Thompson 采样在多臂老虎机问题中平衡探索与利用──

Thách thức cốt lõi: bạn chỉ có thể lấy mẫu trực tiếp từ phân phối đơn giản (tương tự, bình thường). Đối với tất cả mọi thứ khác, bạn cần một phương pháp để chuyển đổi các mẫu đơn giản thành mẫu từ phân phối mục tiêu của bạn.

> 核心挑战: bạn chỉ có thể trực tiếp từ đơn giản phân bố (均分布、正态分布) trong các mô hình. Đối với tất cả các phân bố khác, bạn cần một phương pháp sẽ chuyển đổi đơn giản thành mục tiêu phân bố mô hình.

> **【拓展：LLM 采样策略的工程实践】**
> GPT-4 等模型推理时,温度通常设为0.0-1.0,顶p 设为0.9-1.0。OpenAI API 默认温度=1.0、top_p=1.0。研究表明 top-p (nucleus) 采样在大多数任务上优于 top-k,因为它能根据模型置信度自适应调整候选集大小──对于代码生成,温度=0.2 + top_p=0.95 是常见配置──

### Phân tích ngẫu nhiên thống nhất

Mỗi phương pháp lấy mẫu bắt đầu ở đây. Một máy phát điện số ngẫu nhiên đồng nhất tạo ra các giá trị trong [0, 1) nơi mỗi phân đoạn cùng chiều dài có xác suất bằng nhau.

> Tất cả các phương pháp so sánh đều bắt đầu từ đây.

```
U ~ Uniform(0, 1)

P(a <= U <= b) = b - a    for 0 <= a <= b <= 1

Properties:
  E[U] = 0.5
  Var(U) = 1/12
```

Để lấy mẫu một cách đồng nhất từ một tập hợp phân biệt n mục, tạo U và trả lại tầng(n * U. Để lấy mẫu từ một phạm vi liên tục [a, b], tính toán a + (b - a) * U.

> Để từ n 个元素的离散集合中均采样,生成 U 并返回楼层(n * U) ―― phải từ连续区间 [a, b] 中采样,计算 a + (b - a) * U。

Ý tưởng chính: một số ngẫu nhiên đồng nhất có chứa chính xác số lượng ngẫu nhiên phù hợp để tạo ra một mẫu từ bất kỳ phân phối nào.

> 关键洞察: Số tự nhiên đơn lẻ có đủ tự nhiên, có thể tạo ra một mẫu trong bất kỳ phân bố nào.

> **【中文解读】**
> Phân bố bình thường là tất cả các loại đáy nền. Phân bố giả tạo số lượng trong máy tính như Mersenne Twister được tạo ra là phân bố bình thường trên [0,1)  Phân bố bình thường trên bản chất là đưa đơn vị bình thường với số lượng "tiến đổi" thành mô hình phân bố mục tiêu, giống như sử dụng một khóa mở khác nhau.

### Phương pháp CDF ngược (Thiết mẫu biến ngược)

Chức năng phân phối tích lũy (CDF) lập bản đồ các giá trị thành xác suất:

```
F(x) = P(X <= x)

Properties:
  F is non-decreasing
  F(-inf) = 0
  F(+inf) = 1
  F maps the real line to [0, 1]
```

CDF ngược sẽ lập bản đồ xác suất trở lại với giá trị. Nếu U ~ Uniform(0, 1), thì X = F_inverse(U) theo phân bố mục tiêu.

> ngược CDF 将概率映射回值──如果 U ~ Uniform(0, 1), thì X = F_inverse(U) 服从目标分布──

```
Algorithm:
  1. Generate u ~ Uniform(0, 1)
  2. Return F_inverse(u)

Why it works:
  P(X <= x) = P(F_inverse(U) <= x) = P(U <= F(x)) = F(x)
```

**Exponential distribution example:**

```
PDF: f(x) = lambda * exp(-lambda * x),   x >= 0
CDF: F(x) = 1 - exp(-lambda * x)

Solve F(x) = u for x:
  u = 1 - exp(-lambda * x)
  exp(-lambda * x) = 1 - u
  x = -ln(1 - u) / lambda

Since (1 - U) and U have the same distribution:
  x = -ln(u) / lambda
```

Điều này hoạt động hoàn hảo khi bạn có thể viết F_inverse trong dạng đóng. Đối với phân bố bình thường, không có CDF ngược hình thức đóng, vì vậy chúng tôi sử dụng các phương pháp khác (Box-Muller, hoặc ước tính số).

> Khi bạn có thể viết ra biểu hiện phân tích của F_inverse, phương pháp này hoàn hảo运作── đối với phân bố trạng thái正, không có hình thức phân tích ngược CDF, vì vậy chúng tôi sử dụng phương pháp khác.

**Discrete version:**Đối với phân phối phân định, xây dựng CDF như một tổng cộng, tạo U, và tìm chỉ số đầu tiên khi tổng cộng vượt quá U. Đây là cách `sample_categorical`làm việc trong Bài học 06.

> **离散版本：**Đối với phân bố phân tán, sẽ xây dựng CDF để tích lũy và tạo ra U, tìm thấy tích lũy và lần đầu tiên vượt quá U của chỉ số.`sample_categorical`

> **【中文解读】**
> 逆 CDF 方法的核心思想:CDF 函数 F(x) Đặt giá trị của biến số随机映射到 [0,1] 上的概率, trong khi hàm ngược của nó F_inverse 正好反过来把 [0,1] 上的均随机数映射回目标分布的值──这个方法精确、高效,但前提是你能写出反函数的解析表达式──

### Phân tích mẫu từ chối

Khi bạn không thể đảo ngược CDF nhưng có thể đánh giá mục tiêu PDF lên đến một liên tục, việc lấy mẫu từ chối hoạt động.

> Khi bạn không thể yêu cầu chống lại CDF, nhưng có thể tính mục tiêu PDF (từ một số lượng thường xuyên)

```
Target distribution: p(x)  (can evaluate, possibly unnormalized)
Proposal distribution: q(x)  (can sample from)
Bound: M such that p(x) <= M * q(x) for all x

Algorithm:
  1. Sample x ~ q(x)
  2. Sample u ~ Uniform(0, 1)
  3. If u < p(x) / (M * q(x)), accept x
  4. Otherwise, reject and go to step 1

Acceptance rate = 1/M
```

M càng chặt chẽ, tỷ lệ chấp nhận càng cao. Trong các chiều kích thấp (1-3), lấy mẫu từ chối hoạt động tốt. Trong các chiều kích cao, tỷ lệ chấp nhận giảm theo cấp số lượng bởi vì phần lớn khối lượng đề xuất bị từ chối. Đây là lời nguyền về chiều kích cho lấy mẫu từ chối.

> Trong không gian cao, tỷ lệ chấp nhận theo chỉ số giảm, vì phần lớn các đề xuất được từ chối.

**Example: sampling from a truncated normal.**Sử dụng một đề xuất thống nhất trên phạm vi cắt giảm. bưu thi M là tối đa của PDF bình thường trong phạm vi đó.

> **示例：从截断正态分布采样。**Trong phạm vi cắt ngang sử dụng均提议分布──包网 M là giá trị lớn nhất trong phạm vi này──

**Example: sampling from a semicircle.**Đề xuất một cách đồng nhất trong hình chữ nhật biên giới. chấp nhận nếu điểm rơi vào vòng bán cầu. Đây là cách Monte Carlo tính toán pi: tỷ lệ chấp nhận bằng tỷ lệ diện tích pi/4.

> **示例：从半圆采样。**Trong hình dạng đường tròn bên ngoài, tỷ lệ đề xuất là: nếu điểm nằm trong một nửa tròn thì được chấp nhận.

> **【拓展：拒绝采样在粒子滤波中的应用】**
> 粒子波(Particle Filter) là một thuật toán cốt lõi của mục tiêu theo dõi và định vị máy tính. Về bản chất nó là một cách từ chối mẫu với một nhóm "các hạt" phân bố gần như sau thử nghiệm, dựa trên kết quả quan sát đối với các hạt tăng trọng lượng mẫu.

### Việc lấy mẫu quan trọng

Đôi khi bạn không cần các mẫu từ phân phối mục tiêu p(x. Bạn cần ước tính một kỳ vọng dưới p(x), và bạn có các mẫu từ phân phối khác q(x.

> Đôi khi bạn không cần thiết phải lấy mẫu từ phân bố mục tiêu p(x) trong khi đó bạn cần phải ước tính một kỳ vọng trong khi bạn có mẫu từ phân bố khác q(x) trên tay bạn.

```
Goal: estimate E_p[f(x)] = integral of f(x) * p(x) dx

Rewrite:
  E_p[f(x)] = integral of f(x) * (p(x)/q(x)) * q(x) dx
            = E_q[f(x) * w(x)]

where w(x) = p(x) / q(x)  are the importance weights.

Estimator:
  E_p[f(x)] ~ (1/N) * sum(f(x_i) * w(x_i))    where x_i ~ q(x)
```

Điều này rất quan trọng trong việc học tập tăng cường. Trong PPO (Proposimal Policy Optimization), bạn thu thập quỹ đạo theo một chính sách cũ nhưng muốn tối ưu hóa một chính sách mới.

> Đây là điều quan trọng trong quá trình tập luyện mạnh mẽ. Trong PPO (Proposal Policy Optimization) bạn đang tập trung vào những chiến lược cũ, nhưng bạn đang nghĩ đến việc tối ưu hóa những chiến lược mới.

> **【拓展：PPO 中的重要性采样】**
> PPO là thuật toán cốt lõi của ChatGPT RLHF  đào tạo. Nó sử dụng tầm quan trọng để sửa đổi sự phân bố giữa các chiến lược mới và cũ.

Sự khác biệt của ước tính lấy mẫu tầm quan trọng phụ thuộc vào sự tương tự của q với p. Nếu q rất khác với p, một vài mẫu có trọng lượng rất lớn và thống trị ước tính.

> Sự khác biệt của các thiết bị đánh giá tầm quan trọng phụ thuộc vào mức độ tương tự của q và p. Nếu q và p khác biệt rất lớn, một số ít các mẫu sẽ nhận được trọng lượng lớn và có thể đánh giá chính.

```
E_p[f(x)] ~ sum(w_i * f(x_i)) / sum(w_i)
```

### Đánh giá Monte Carlo

Phân tích Monte Carlo ước tính gần gũi bằng cách trung bình các mẫu ngẫu nhiên. Luật số lớn đảm bảo sự hội tụ.

> Phân tích của Monte Carlo đã đảm bảo tính nhận được.

```
Goal: estimate I = integral of g(x) dx over domain D

Method:
  1. Sample x_1, ..., x_N uniformly from D
  2. I ~ (Volume of D / N) * sum(g(x_i))

Error: O(1 / sqrt(N))   regardless of dimension
```

Tỷ lệ lỗi là không phụ thuộc vào kích thước. Đó là lý do tại sao phương pháp Monte Carlo thống trị ở các kích thước cao nơi tích hợp dựa trên lưới là không thể.

>  tỷ lệ sai lầm không liên quan đến chiều kích. Đó là lý do tại sao phương pháp Monte Carlo chiếm ưu thế trong không gian cao.

> **【中文解读】**
> Tốt yếu của phương pháp Monte Carlo: sử dụng giá trị trung bình của mẫu tự nhiên để ước tính gần gũi. Quy định số lớn đảm bảo nhận, và tỷ lệ sai lầm O(1/sqrt(N)) không liên quan đến chiều kích.

**Estimating pi:**

```
Sample (x, y) uniformly from [-1, 1] x [-1, 1]
Count how many fall inside the unit circle: x^2 + y^2 <= 1
pi ~ 4 * (count inside) / (total count)
```

**Estimating expectations:**

```
E[f(X)] ~ (1/N) * sum(f(x_i))    where x_i ~ p(x)

The sample mean converges to the true expectation.
Variance of the estimator = Var(f(X)) / N
```

### Đường dây Markov Monte Carlo (MCMC): Metropolis-Hastings

MCMC xây dựng một chuỗi Markov mà phân phối tĩnh là phân phối mục tiêu p(x). Sau đủ bước, các mẫu từ chuỗi là (khoảng) các mẫu từ p(x.

> MCMC  cấu trúc một chuỗi Markov), phân phối ổn định của nó (Rải phân phối tĩnh) là mục tiêu phân phối p (x) ⋅ sau quá trình đủ nhiều bước, mô hình trên chuỗi (x) là mô hình của p (x)).

```
Target: p(x)  (known up to a normalizing constant)
Proposal: q(x'|x)  (how to propose the next state given the current state)

Metropolis-Hastings algorithm:
  1. Start at some x_0
  2. For t = 1, 2, ..., T:
     a. Propose x' ~ q(x'|x_t)
     b. Compute acceptance ratio:
        alpha = [p(x') * q(x_t|x')] / [p(x_t) * q(x'|x_t)]
     c. Accept with probability min(1, alpha):
        - If u < alpha (u ~ Uniform(0,1)): x_{t+1} = x'
        - Otherwise: x_{t+1} = x_t
  3. Discard first B samples (burn-in)
  4. Return remaining samples
```

Đối với các đề xuất đối xứng (q(x' khiếux) = q(x khiếux') , tỷ lệ đơn giản hóa thành p(x')/p(x). Đây là thuật toán Metropolis ban đầu.

> Đối với đối称提议 (q) = q) = x) = x)), tỷ lệ giảm thiểu là p) = x) /p)

**Why it works.**Quy tắc chấp nhận đảm bảo sự cân bằng chi tiết: xác suất ở x và di chuyển đến x' bằng với xác suất ở x' và di chuyển đến x. Sự cân bằng chi tiết cho thấy p ((x) là sự phân bố tĩnh của chuỗi.

> **为什么有效。**Ưu điểm quy tắc đảm bảo các điều kiện cân bằng chi tiết: ở x và chuyển sang x' tỷ lệ tương đương với ở x' và chuyển sang x tỷ lệ.

> **【拓展：MCMC 在贝叶斯深度学习中的应用】**
> PyMC、NumPyro 等 Bayesian 推理框架的核心就是MCMC。NUTS (No-U-Turn Sampler) là biến thể MCMC tiên tiến nhất, nó tự động điều chỉnh bước dài và hướng。 Trong quá trình phát hiện thuốc, các nhà nghiên cứu sử dụng MCMC 采样分子构造后验分布, xử lý hàng ngàn维参数空间。Stan 语言(以统计学家 Stanislaw Ulam命名) để các nhà nghiên cứu không cần phải viết tay MCMC để có thể tiến hành các推理贝尔。

**Practical considerations:**
- Đốt: loại bỏ các mẫu sơ khai trước khi chuỗi đạt được cân bằng
  预热期(Burn-in): bỏ chuỗi đạt cân bằng trước
- Thinning: giữ mỗi mẫu k-th để giảm sự tương quan tự
  稀释(Thining): mỗi phần k 个样本保留一个以减少自相关
- Skala đề xuất: quá nhỏ và chuỗi di chuyển chậm (tự chấp nhận cao, khám phá chậm); quá lớn và hầu hết các đề xuất bị từ chối (tự chấp nhận thấp, bị mắc kẹt)
  提议尺度(Tỷ lệ đề xuất): quá nhỏ, quá chậm, quá nhiều đề xuất bị từ chối, quá thấp, quá thấp, quá nhiều
- Tỷ lệ chấp nhận tối ưu cho một đề xuất Gaussian ở kích thước cao là khoảng 0,234
  Tỷ lệ chấp nhận tối ưu của cao tầng trung tâm cao tầng là khoảng 0,234

### Gibbs Sampling

Phân tích Gibbs là một trường hợp đặc biệt của MCMC cho phân phối đa biến. Thay vì đề xuất chuyển động trong tất cả các chiều kích cùng một lúc, nó cập nhật một biến một lần từ phân phối điều kiện của nó.

> Gibbs 采样 là một đặc điểm trong phân bố nhiều biến số MCMC. Nó không cùng lúc di chuyển trên tất cả các chiều, mà thay vào đó, mỗi lần từ phân bố điều kiện cập nhật một biến số.

```
Target: p(x_1, x_2, ..., x_d)

Algorithm:
  For each iteration t:
    Sample x_1^{t+1} ~ p(x_1 | x_2^t, x_3^t, ..., x_d^t)
    Sample x_2^{t+1} ~ p(x_2 | x_1^{t+1}, x_3^t, ..., x_d^t)
    ...
    Sample x_d^{t+1} ~ p(x_d | x_1^{t+1}, x_2^{t+1}, ..., x_{d-1}^{t+1})
```

Phân tích Gibbs đòi hỏi bạn có thể lấy mẫu từ mỗi phân bố điều kiện p ((x_i ∈ x_{-i}).
- Các mạng Bayesian: điều kiện theo sau từ cấu trúc đồ thị
  贝叶斯网络: điều kiện phân phối bởi cấu trúc quyết định
- Các hỗn hợp Gaussian: điều kiện là Gaussian
  Mô hình hỗn hợp cao: điều kiện phân phối là cao
- Các mô hình Ising: điều kiện của mỗi spin chỉ phụ thuộc vào các hàng xóm của nó
  Ising 模型: Mỗi điều kiện tự xoay phân bố chỉ phụ thuộc vào hàng xóm của nó

Tỷ lệ chấp nhận luôn là 1 (mỗi đề xuất đều được chấp nhận) vì việc lấy mẫu từ điều kiện chính xác tự động đáp ứng cân bằng chi tiết.

> Ưu điểm chấp nhận luôn luôn là 1 (mỗi đề nghị đều được chấp nhận), vì từ phân bố điều kiện chính xác, các mẫu tự động đáp ứng các điều kiện cân bằng nhỏ.

**Limitation.**Khi các biến có liên quan cao, việc lấy mẫu Gibbs trộn chậm vì cập nhật một biến một lần không thể thực hiện các chuyển động đường vạch lớn thông qua phân phối.

> **局限性。**Khi các biến thể có liên quan cao, hình thức của Gibbs hỗn hợp rất chậm, bởi vì mỗi lần chỉ cập nhật một biến thể không thể tạo ra chuyển động lớn đối với góc trong phân bố.

> **【中文解读】**
> Gibbs 采样 là một đặc điểm của MCMC: mỗi lần chỉ cập nhật một biến, từ phân bố điều kiện 采样. Bởi vì mỗi lần 采样 đều từ phân bố điều kiện chính xác, do đó tỷ lệ chấp nhận luôn là 100%.

### Tiêu chuẩn nhiệt độ (được sử dụng trong LLM)

Các mô hình ngôn ngữ xuất logit z_1, ..., z_V cho mỗi token trong từ vựng. Softmax chuyển đổi chúng thành xác suất. Nhiệt độ tái định lượng logit trước softmax:

> 语言模型为词汇表中的每个代号 输出 logits z_1, ..., z_V──Softmax sẽ chuyển chúng thành概率──Temperature(温度) 在 softmax 之前对 logits 进行缩放:

```
p_i = exp(z_i / T) / sum(exp(z_j / T))

T = 1.0: standard softmax (original distribution)
T -> 0:  argmax (deterministic, always picks highest logit)
T -> inf: uniform (all tokens equally likely)
T < 1.0: sharpens the distribution (more confident, less diverse)
T > 1.0: flattens the distribution (less confident, more diverse)
```

**Why it works.**Chia logit bằng T < 1 làm tăng sự khác biệt giữa logit. Nếu z_1 = 2 và z_2 = 1, chia bằng T = 0.5 sẽ tạo ra z_1/T = 4 và z_2/T = 2, làm cho khoảng cách lớn hơn. Sau softmax, token logit cao nhất sẽ có phần lớn hơn nhiều.

> **为什么有效。**Để phân chia logit với T < 1 sẽ làm tăng sự khác biệt giữa logit 👇 Nếu z_1 = 2、z_2 = 1, phân chia với T = 0.5  nhận được z_1/T = 4、z_2/T = 2, sự khác biệt lớn hơn.

**In practice:**
- T = 0,0: giải mã tham lam, tốt nhất cho Q&A thực tế
  贪心解码, nhất phù hợp với thực tế câu hỏi
- T = 0,3-0,7: hơi sáng tạo, tốt cho việc tạo ra mã
  略有创意, phù hợp với code generate
- T = 0,7-1,0: cân bằng, tốt cho cuộc trò chuyện chung
  均衡,适合一般对话
- T = 1.0-1.5: viết sáng tạo, suy nghĩ
  创意写作、头脑风暴
- T > 1,5: ngày càng ngẫu nhiên, hiếm khi hữu ích
  越来越随时, rất ít hữu ích

Nhiệt độ không thay đổi các token có thể, nó thay đổi khối lượng xác suất được phân bổ cho mỗi token.

> 温度 sẽ không thay đổi các token có thể được chọn. Nó thay đổi là phân bổ cho mỗi token.

> **【中文解读】**
> Nhiệt độ là LLM 输出多样性的"旋"──T < 1 让分布更尖(更像贪心),T > 1 让分布更平坦(更随机)──T → 0 退化为 argmax,T → ∞ 退化为均分布──实际中T=0.7 là điểm cân bằng thường xuyên nhất──注意: nhiệt độ không thay đổi bất kỳ biểu tượng nào có thể được chọn, chỉ thay đổi tỷ lệ phân phối──

### Top-k Sampling

Top-k lấy mẫu hạn chế bộ ứng cử viên cho các token k có xác suất cao nhất, sau đó tái bình thường hóa và lấy mẫu từ bộ hạn chế đó.

> Top-k 采样将候选集限制为概率最高的 k 个代币, sau đó tái归纳并从该受限集中采样.

```
Algorithm:
  1. Compute softmax probabilities for all V tokens
  2. Sort tokens by probability (descending)
  3. Keep only the top k tokens
  4. Renormalize: p_i' = p_i / sum(p_j for j in top-k)
  5. Sample from the renormalized distribution

k = 1:  greedy decoding
k = V:  no filtering (standard sampling)
k = 40: typical setting, removes long tail of unlikely tokens
```

Top-k ngăn chặn mô hình chọn các token cực kỳ không có khả năng (typos, nonsense) tồn tại trong đuôi dài của phân phối từ vựng. Vấn đề: k được cố định bất kể bối cảnh. Khi mô hình tự tin (một token có khả năng 95%), k = 40 vẫn cho phép 39 lựa chọn thay thế. Khi mô hình không chắc chắn (có khả năng được phân phối trên 1000 token), k = 40 cắt giảm các tùy chọn đáng tin cậy.

> Top-k 防止模型选择词汇分布长尾中极不可能的代币(错别字、无意义的词)  vấn đề nằm ở:k là cố định, không theo sau văn bản thay đổi;. khi mô hình rất tự tin khi một token chiếm 95% 概率),k = 40 vẫn cho phép 39 tùy chọn thay thế;. khi mô hình không chắc chắn khi tỷ lệ phân tán trên 1000 代币),k = 40 lựa chọn hợp lý.

### Top-p (Nucleus) lấy mẫu

Top-p lấy mẫu điều chỉnh động lực kích thước tập hợp ứng cử viên. Thay vì giữ một số lượng mã thông báo cố định, nó giữ tập hợp nhỏ nhất của mã thông báo có xác suất tích lũy vượt quá p.

> Top-p 采样动态调整候选人集大小──它 không giữ lại số lượng mã thông báo cố định, mà giữ lại tỷ lệ tích lũy hơn 集合 p của mã thông báo tối thiểu──

```
Algorithm:
  1. Compute softmax probabilities for all V tokens
  2. Sort tokens by probability (descending)
  3. Find smallest k such that sum of top-k probabilities >= p
  4. Keep only those k tokens
  5. Renormalize and sample

p = 0.9:  keeps tokens covering 90% of probability mass
p = 1.0:  no filtering
p = 0.1:  very restrictive, nearly greedy
```

Khi mô hình tự tin, lấy mẫu hạt nhân giữ ít mã thông báo (có lẽ 2-3). Khi mô hình không chắc chắn, nó giữ nhiều (có lẽ 200). Hành vi thích ứng này là lý do tại sao lấy mẫu hạt nhân thường tạo ra văn bản tốt hơn so với top-k.

> Khi mô hình có niềm tin, hạt nhân 采样 chỉ giữ một lượng nhỏ token (~ 2-3 个) ⋅ Khi mô hình không chắc chắn, nó giữ rất nhiều (~ 200 个) ⋅

**Common combinations:**
- Nhiệt độ 0,7 + top-p 0,9: thiết lập mục đích chung tốt
  Thiết lập chung tốt
- Nhiệt độ 0.0 (cười tham): tốt nhất cho các nhiệm vụ xác định
  Ưu hợp nhất nhiệm vụ xác định
- Nhiệt độ 1.0 + top-k 50: Fan et al. (2018) thiết lập giấy gốc
  Fan 等人 (2018) 原论文设置

Top-k và top-p có thể được kết hợp.

> Top-k 和 top-p có thể được sử dụng hợp nhất.

### Trù sửa chữa (chỉ sử dụng trong VAEs)

Các bộ tự động mã hóa biến thể (VAE) học bằng cách mã hóa đầu vào vào một phân phối trong không gian ẩn, lấy mẫu từ phân phối đó và giải mã lại mẫu. Vấn đề: bạn không thể lây lan trở lại thông qua một hoạt động lấy mẫu.

> 变分自编码器(VAE) thông qua sẽ nhập mã hóa cho phân bố trong không gian ẩn ̇ từ đó phân bố mẫu ̇ rồi sẽ phân giải mã mẫu trở lại để học ̇ vấn đề là: bạn không thể thông qua thao tác mẫu để truyền ngược ̇

```
Standard sampling (not differentiable):
  z ~ N(mu, sigma^2)

  The randomness blocks gradient flow.
  d/d_mu [sample from N(mu, sigma^2)] = ???
```

Tránh tái định đo phân tách sự ngẫu nhiên từ các tham số:

> Các kỹ thuật hóa trọng số sẽ được chọn tùy chọn và phân chia thành phần:

```
Reparameterized sampling:
  epsilon ~ N(0, 1)          (fixed random noise, no parameters)
  z = mu + sigma * epsilon   (deterministic function of parameters)

  Now z is a deterministic, differentiable function of mu and sigma.
  d(z)/d(mu) = 1
  d(z)/d(sigma) = epsilon

  Gradients flow through mu and sigma.
```

Điều này hoạt động bởi vì N(mu, sigma^2) có phân bố tương tự như mu + sigma * N(0, 1). Nhìn sâu: di chuyển sự ngẫu nhiên đến một nguồn không có tham số (epsilon), sau đó thể hiện mẫu như một biến đổi có thể phân biệt các tham số.

> Đây là lý do tại sao có hiệu quả, bởi vì N(mu, sigma^2) với mu + sigma * N(0, 1) có phân bố tương tự.

**In the VAE training loop:**
1. Các đầu ra mã hóa mu và log(sigma^2) cho mỗi đầu vào
2. mẫu epsilon ~ N(0, 1)
3. Xét z = mu + sigma * epsilon
4. Tự giải mã z để tái cấu trúc đầu vào
5. Chuyển ngược qua các bước 4, 3, 2, 1 (có thể bởi vì bước 3 có thể phân biệt)

Nếu không có thủ thuật tái định đo lường, VAE không thể được đào tạo với sự lây lan ngược tiêu chuẩn.

> Không có kỹ thuật phân tích nặng, VAE không thể sử dụng các bài tập chống chiều hướng.

> **【拓展：重参数化技巧的广泛应用】**
> Trong các bài học về phân tích, các kỹ thuật của SAC (Soft Actor-Critic) sử dụng các phương pháp tính toán về phân tích.

### Gumbel-Softmax (Phân tích phân loại khác nhau)

Tránh tái định đo lường hoạt động cho phân phối liên tục (Gaussian). Đối với phân phối thể loại riêng biệt, chúng ta cần một cách tiếp cận khác. Gumbel-Softmax cung cấp một sự gần gũi phân biệt với lấy mẫu thể loại.

> Các kỹ thuật phân tích nặng được áp dụng cho phân bố liên tục. Đối với phân bố phân loại phân tán, chúng ta cần các phương pháp khác nhau.

**The Gumbel-Max trick (non-differentiable):**

```
To sample from a categorical distribution with log-probabilities log(p_1), ..., log(p_k):
  1. Sample g_i ~ Gumbel(0, 1) for each category
     (g = -log(-log(u)), where u ~ Uniform(0, 1))
  2. Return argmax(log(p_i) + g_i)

This produces exact categorical samples.
```

**Gumbel-Softmax (differentiable approximation):**

```
Replace the hard argmax with a soft softmax:
  y_i = exp((log(p_i) + g_i) / tau) / sum(exp((log(p_j) + g_j) / tau))

tau (temperature) controls the approximation:
  tau -> 0:  approaches a one-hot vector (hard categorical)
  tau -> inf: approaches uniform (1/k, 1/k, ..., 1/k)
  tau = 1.0: soft approximation
```

Gumbel-Softmax tạo ra sự thư giãn liên tục của một mẫu phân biệt. Kết quả là một vector xác suất (mềm một nóng) thay vì một nóng cứng. Các gradient chảy qua softmax. Trong quá trình đi về phía trước trong đào tạo, bạn có thể sử dụng ước tính "thẳng qua": sử dụng argmax cứng cho quá trình đi về phía trước nhưng gradient mềm Gumbel-Softmax cho quá trình đi về phía sau.

> Gumbel-Softmax 产生离散样本的连续松(Continuous Relaxation) ――输出是一个概率向量(软一个热) thay vì cứng một热――梯度可以流过软max──在训练的前向传播中,你可以使用"直通估计器"(Straight-Through Estimator):前向传播使用硬 argmax,反向传播使用软 Gumbel-Softmax 梯度──

**Applications:**
- Các biến ẩn trong các VAE
  Số lượng biến đổi phân tán trong VAE
- Tìm kiếm kiến trúc thần kinh (chọn các hoạt động riêng biệt)
  神经架构搜索 (đưa ra các hoạt động)
- Cơ chế chú ý cứng
  硬注意力机械
- Học tập tăng cường bằng các hành động riêng biệt
  离散动作强化学习

### Tiêu chuẩn lấy mẫu

Các mẫu mẫu Monte Carlo tiêu chuẩn có thể để lại khoảng trống trong không gian mẫu do tình cờ.

> 标准蒙特卡洛采样可能会偶然留下空隙在样本空间中──分层采样──Stratified Sampling) thông qua phân chia không gian thành tầng──Strata)并从每层中采样来强制均覆盖──

```
Standard Monte Carlo:
  Sample N points uniformly from [0, 1]
  Some regions may have clusters, others gaps

Stratified sampling:
  Divide [0, 1] into N equal strata: [0, 1/N), [1/N, 2/N), ..., [(N-1)/N, 1)
  Sample one point uniformly within each stratum
  x_i = (i + u_i) / N   where u_i ~ Uniform(0, 1),  i = 0, ..., N-1
```

Các mẫu phân cấp luôn có sự biến dạng thấp hơn hoặc bằng nhau so với Monte Carlo tiêu chuẩn:

> Sự khác biệt về các tầng thường thấp hơn hoặc bằng với tiêu chuẩn Monte Carlo:

```
Var(stratified) <= Var(standard Monte Carlo)

The improvement is largest when f(x) varies smoothly.
For piecewise-constant functions, stratified sampling is exact.
```

**Applications:**
- Kết hợp số (quasi-Monte Carlo)
  Số giá trị积分(准蒙特卡洛)
- Các phân chia dữ liệu đào tạo (đảm bảo sự cân bằng lớp học trong mỗi lần)
  训练数据划分( đảm bảo mỗi折的类别平衡)
- Tiêu chuẩn lấy mẫu quan trọng với phân bố lớp (combination of both techniques)
  结合分层的重要性采样
- NeRF (Neural Radiance Fields) sử dụng lấy mẫu phân tầng dọc theo các tia máy ảnh
  NeRF(đường xạ thần kinh) dọc theo quang điện sử dụng phân tầng

### Kết nối với các mô hình phân phối

Các mô hình phân phối tạo ra hình ảnh thông qua một quá trình lấy mẫu. quá trình tiến thêm tiếng ồn Gaussian vào một hình ảnh qua các bước T cho đến khi nó trở thành tiếng ồn thuần túy.

> 扩散模型通过采样过程生成图像――前向过程在T 步骤内逐渐向图像增加高噪音,直到变成纯噪音――反向过程学习去噪音,逐步恢复原始图像――

```
Forward process (known):
  x_t = sqrt(alpha_t) * x_{t-1} + sqrt(1 - alpha_t) * epsilon
  where epsilon ~ N(0, I)

  After T steps: x_T ~ N(0, I)  (pure noise)

Reverse process (learned):
  x_{t-1} = (1/sqrt(alpha_t)) * (x_t - (1 - alpha_t)/sqrt(1 - alpha_bar_t) * epsilon_theta(x_t, t)) + sigma_t * z
  where z ~ N(0, I)

  Each denoising step is a sampling step.
```

Kết nối với các phương pháp trong bài học này:
- Mỗi bước khử sử dụng thủ thuật tái định đo (mô hình tiếng ồn, áp dụng biến đổi xác định)
  Mỗi bước đi tiếng ồn đều sử dụng kỹ thuật tái số hóa (từ tiếng ồn, ứng dụng xác định thay đổi)
- Các lịch trình tiếng ồn {alpha_t} điều khiển một hình thức của nhiệt độ
  噪音调度 {alpha_t} 控制一种形式的温度退火(Tâm nhiệt độ 
- Việc đào tạo sử dụng ước tính Monte Carlo để gần ELBO (bằng chứng bên dưới)
  训练 sử dụng 蒙特卡洛 ước tính để gần như ELBO(Bộ chứng Lower Bound, chứng cứ
- Tiêu mẫu tổ tiên trong các mô hình phân tán là chuỗi Markov (mỗi bước chỉ phụ thuộc vào trạng thái hiện tại)
  扩散模型中的祖先采样 (Phân mẫu tổ tiên) là một chuỗi có thể được sử dụng (mỗi bước chỉ phụ thuộc vào trạng thái hiện tại)

Toàn bộ quá trình tạo hình ảnh là lấy mẫu lặp lại: bắt đầu từ tiếng ồn, và ở mỗi bước, lấy mẫu một phiên bản ít tiếng ồn hơn một chút theo mô hình từ chối được học.

> Toàn bộ quá trình tạo hình ảnh là một phiên bản nhỏ hơn: từ tiếng ồn bắt đầu, trong mỗi bước, dựa trên mô hình học tập để lấy một phiên bản nhỏ hơn.

## Hãy xây dựng nó.
```figure
monte-carlo-pi
```

## Hãy xây dựng nó

### Bước 1: Tiểu mẫu CDF thống nhất và ngược

```python
import math
import random

def sample_uniform(a, b):
    return a + (b - a) * random.random()  # 线性变换：把 [0,1) 映射到 [a,b)

def sample_exponential_inverse_cdf(lam):
    u = random.random()                   # 生成均匀随机数
    return -math.log(u) / lam             # 逆 CDF：x = -ln(u) / lambda
```

Tạo 10.000 mẫu biểu diễn và xác minh trung bình là 1/lambda.

> 生成 10,000 个指数分布样本,验证平均值是否为1/lambda──

### Bước 2: Tiểu mẫu từ chối

```python
def rejection_sample(target_pdf, proposal_sample, proposal_pdf, M):
    while True:                           # 持续采样直到被接受
        x = proposal_sample()             # 从提议分布采样
        u = random.random()               # 均匀随机数用于决定接受/拒绝
        if u < target_pdf(x) / (M * proposal_pdf(x)):  # 接受条件
            return x
```

Sử dụng mẫu từ chối để rút ra từ phân bố bình thường bị cắt.

> Sử dụng từ chối lấy mẫu từ phân bố phân chia chính xác.

### Bước 3: Tiểu mẫu tầm quan trọng

```python
def importance_sampling_estimate(f, target_pdf, proposal_pdf, proposal_sample, n):
    total = 0
    for _ in range(n):
        x = proposal_sample()
        w = target_pdf(x) / proposal_pdf(x)
        total += f(x) * w
    return total / n
```

Đếm E[X^2] dưới phân bố bình thường bằng cách sử dụng một đề xuất đồng nhất. So sánh với câu trả lời được biết (mu^2 + sigma^2).

> Sử dụng均提议分布估计正态分布下 E[X^2]──与已知答案 (mu^2 + sigma^2) 比较──

### Bước 4: ước tính Monte Carlo của pi

```python
def monte_carlo_pi(n):
    inside = 0
    for _ in range(n):
        x = random.uniform(-1, 1)
        y = random.uniform(-1, 1)
        if x*x + y*y <= 1:
            inside += 1
    return 4 * inside / n
```

### Bước 5: Metropolis-Hastings MCMC

```python
def metropolis_hastings(target_log_pdf, proposal_sample, proposal_log_pdf, x0, n_samples, burn_in):
    samples = []
    x = x0                                # 初始状态
    for i in range(n_samples + burn_in):
        x_new = proposal_sample(x)        # 从提议分布生成新候选
        log_alpha = (target_log_pdf(x_new) + proposal_log_pdf(x, x_new)  # 计算接受比的对数
                     - target_log_pdf(x) - proposal_log_pdf(x_new, x))
        if math.log(random.random()) < log_alpha:  # 以 min(1, alpha) 的概率接受
            x = x_new
        if i >= burn_in:                  # 丢弃 burn-in 阶段的样本
            samples.append(x)
    return samples
```

Mô hình từ phân bố bimodal (cộn lẫn hai Gaussians).

> Từ phân bố hai đỉnh (từ hai đỉnh)

### Bước 6: lấy mẫu Gibbs

```python
def gibbs_sampling_2d(conditional_x_given_y, conditional_y_given_x, x0, y0, n_samples, burn_in):
    x, y = x0, y0
    samples = []
    for i in range(n_samples + burn_in):
        x = conditional_x_given_y(y)
        y = conditional_y_given_x(x)
        if i >= burn_in:
            samples.append((x, y))
    return samples
```

### Bước 7: Tiêu chuẩn nhiệt độ

```python
def softmax(logits):
    max_l = max(logits)
    exps = [math.exp(z - max_l) for z in logits]
    total = sum(exps)
    return [e / total for e in exps]

def temperature_sample(logits, temperature):
    scaled = [z / temperature for z in logits]  # 温度缩放：除以 T
    probs = softmax(scaled)                      # 计算缩放后的概率分布
    return sample_from_probs(probs)
```

Hiển thị cách nhiệt độ thay đổi phân phối đầu ra cho một tập hợp logit token.

> 展示温度如何改变一组代币 logits 的输出分布──

### Bước 8: Tiêu chuẩn top-k và top-p

```python
def top_k_sample(logits, k):
    indexed = sorted(enumerate(logits), key=lambda x: -x[1])
    top = indexed[:k]
    top_logits = [l for _, l in top]
    probs = softmax(top_logits)
    idx = sample_from_probs(probs)
    return top[idx][0]

def top_p_sample(logits, p):
    probs = softmax(logits)
    indexed = sorted(enumerate(probs), key=lambda x: -x[1])
    cumsum = 0
    selected = []
    for token_idx, prob in indexed:
        cumsum += prob
        selected.append((token_idx, prob))
        if cumsum >= p:
            break
    sel_probs = [pr for _, pr in selected]
    total = sum(sel_probs)
    sel_probs = [pr / total for pr in sel_probs]
    idx = sample_from_probs(sel_probs)
    return selected[idx][0]
```

### Bước 9: Tránh sửa chữa

```python
def reparam_sample(mu, sigma):
    epsilon = random.gauss(0, 1)          # 标准正态噪声，不含可学习参数
    return mu + sigma * epsilon            # 确定性变换，梯度可流过

def reparam_gradient(mu, sigma, epsilon):
    dz_dmu = 1.0                          # z 对 mu 的梯度恒为 1
    dz_dsigma = epsilon                   # z 对 sigma 的梯度是 epsilon
    return dz_dmu, dz_dsigma
```

Hiển thị rằng gradient chảy qua mẫu tái định đo nhưng không thông qua lấy mẫu trực tiếp.

>  trình độ có thể chảy qua các mẫu phân tích nặng, nhưng không thể chảy qua các mẫu trực tiếp.

### Bước 10: Gumbel-Softmax

```python
def gumbel_sample():
    u = random.random()
    return -math.log(-math.log(u))

def gumbel_softmax(logits, temperature):
    gumbels = [math.log(p) + gumbel_sample() for p in logits]
    return softmax([g / temperature for g in gumbels])
```

Hãy cho thấy nhiệt độ giảm làm cho đầu ra tiếp cận một vector nóng.

> 展示降低温度 làm thế nào để làm cho xuất gần một nhiệt độ 向量

Các thực hiện đầy đủ với tất cả các hình ảnh hóa là trong `code/sampling.py`- Tôi không biết.

> Sự hoàn toàn của tất cả các khả năng hiển thị`code/sampling.py`Ở giữa.

## Hãy sử dụng nó để thực hiện

> **【拓展：扩散模型中的采样工程】**
> Từ năm 2022 xuất bản, phương pháp soạn thảo từ 1000 bước tiến tiến thành DDIM、DPM-Solver++等 chỉ cần phương pháp 20-50 bước.

Với NumPy và SciPy, các phiên bản sản xuất:

> Sử dụng NumPy 和 SciPy phiên bản sản xuất:

```python
import numpy as np

rng = np.random.default_rng(42)

exponential_samples = rng.exponential(scale=2.0, size=10000)
print(f"Exponential mean: {exponential_samples.mean():.4f} (expected 2.0)")

from scipy import stats
normal = stats.norm(loc=0, scale=1)
print(f"CDF at 1.96: {normal.cdf(1.96):.4f}")
print(f"Inverse CDF at 0.975: {normal.ppf(0.975):.4f}")

logits = np.array([2.0, 1.0, 0.5, 0.1, -1.0])
temperature = 0.7
scaled = logits / temperature
probs = np.exp(scaled - scaled.max()) / np.exp(scaled - scaled.max()).sum()
token = rng.choice(len(logits), p=probs)
print(f"Sampled token index: {token}")
```

Đối với MCMC trên quy mô, sử dụng thư viện chuyên dụng:
- PyMC: mô hình Bayesian đầy đủ với NUTS (HMC thích ứng)
  完整的贝叶斯建模, sử dụng NUTS(自适应 HMC)
- emcee: bộ mẫu MCMC
  集成 MCMC 采样器
- NumPyro/JAX: MCMC tăng tốc GPU
  GPU gia tốc MCMC

Anh đã xây dựng những cái này từ đầu rồi, giờ anh biết những gì thư viện gọi đang làm.

> Bạn đã xây dựng những phương pháp này từ không. Bây giờ bạn biết các hàm thư viện đang làm gì.

## Tập luyện bài tập

1. Thực hiện lấy mẫu CDF ngược cho phân bố Cauchy. CDF là F(x) = 0.5 + arctan(x) / pi. Tạo 10.000 mẫu và vẽ histogram so với PDF thực. Nhận thức những đuôi nặng (giá trị cực xa trung tâm).
   实现柯西分布(Cauchy Distribution) 的逆 CDF 采样──CDF 为 F(x) = 0.5 + arctan(x) /pi──生成 10,000 个样本并绘制直方图与真实 PDF 对比──注意重尾(远离中心极端值)。

2. Sử dụng mẫu từ chối để tạo mẫu từ phân phối Beta(2, 5) sử dụng đề xuất Uniform(0, 1). Chụp các mẫu được chấp nhận so với PDF Beta thực tế. Tỷ lệ chấp nhận lý thuyết là gì?
   Sử dụng từ chối mẫu từ Beta(2, 5) 分布中生成样本,提议分布使用Uniform(0, 1)─绘制接受样本与真实Beta PDF的比图──理论接受率是多少?

3. Đếm số tích tích hợp của sin(x) từ 0 đến pi bằng cách sử dụng Monte Carlo với 1.000, 10.000 và 100.000 mẫu. So sánh lỗi ở mỗi cấp độ.
   Sử dụng phương pháp ước tính lỗi (x) trong 0 đến pi trên积分, phân biệt sử dụng 1,000、10,000 và 100,000 个样本── so sánh các cấp độ khác nhau của sai lầm──验证错误按 O(1/sqrt(N)) 缩放──

4. Thực hiện Metropolis-Hastings để lấy mẫu từ phân bố 2D p ((x, y) tương xứng với exp ((-(x^2 * y^2 + x^2 + y^2 - 8*x - 8*y) / 2).
   实现 Metropolis-Hastings Từ 2D 分布 p(x, y) ~ exp(-(x^2*y^2 + x^2 + y^2 - 8x - 8y) /2) 中采样──绘制样本和链的轨迹──尝试不同的提议标准差──

5. Xây dựng một bản demo tạo văn bản hoàn chỉnh: với một từ vựng 10 từ với logit, tạo ra chuỗi 20 mã thông báo bằng cách sử dụng (a) tham lam, (b) nhiệt độ = 0,7, (c) top-k = 3, (d) top-p = 0,9. So sánh sự đa dạng của các đầu ra trong 5 lần chạy.
   构建一个完整的文本生成演示:给定 10 个词的词汇表和逻辑,使用 (a) 贪心、(b) nhiệt độ=0.7、(c) top-k=3、((d) top-p=0.9 生成 20 个代币的序列──比较 5次运行的输出多样性──

## Từ khóa  Từ khóa nhanh chóng

| Term | What people say | What it actually means |
|------|----------------|----------------------|
| Sampling | "Drawing random values" | Generating values according to a probability distribution. The mechanism behind all generative AI |
| Uniform distribution | "All equally likely" | Every value in [a, b] has equal probability density 1/(b-a). The starting point for all sampling methods |
| Inverse CDF | "Probability transform" | F_inverse(U) converts a uniform sample into a sample from any distribution with known CDF. Exact and efficient |
| Rejection sampling | "Propose and accept/reject" | Generate from a simple proposal, accept with probability proportional to target/proposal ratio. Exact but wastes samples |
| Importance sampling | "Reweight samples" | Estimate expectations under p(x) using samples from q(x) by weighting each sample by p(x)/q(x). Core to PPO in RL |
| Monte Carlo | "Average random samples" | Approximate integrals as sample averages. Error O(1/sqrt(N)) regardless of dimension |
| MCMC | "Random walk that converges" | Construct a Markov chain whose stationary distribution is the target. Metropolis-Hastings is the foundational algorithm |
| Metropolis-Hastings | "Accept uphill, sometimes downhill" | Propose moves, accept based on density ratio. Detailed balance ensures convergence to target distribution |
| Gibbs sampling | "One variable at a time" | Update each variable from its conditional distribution holding others fixed. 100% acceptance rate |
| Temperature | "Confidence knob" | Divides logits by T before softmax. T<1 sharpens (more confident), T>1 flattens (more diverse) |
| Top-k sampling | "Keep the k best" | Zero out all but the k highest-probability tokens, renormalize, sample. Fixed candidate set size |
| Nucleus sampling (top-p) | "Keep the probable ones" | Keep the smallest set of tokens whose cumulative probability exceeds p. Adaptive candidate set size |
| Reparameterization trick | "Move randomness outside" | Write z = mu + sigma * epsilon where epsilon ~ N(0,1). Makes sampling differentiable. Essential for VAE training |
| Gumbel-Softmax | "Soft categorical sampling" | Differentiable approximation to categorical sampling using Gumbel noise + softmax with temperature |
| Stratified sampling | "Forced coverage" | Divide sample space into strata, sample from each. Always lower variance than naive Monte Carlo |
| Burn-in | "Warm-up period" | Initial MCMC samples discarded before the chain reaches its stationary distribution |
| Detailed balance | "Reversibility condition" | p(x) * T(x->y) = p(y) * T(y->x). Sufficient condition for p to be the stationary distribution of a Markov chain |
| Diffusion sampling | "Iterative denoising" | Generate data by starting from noise and applying learned denoising steps. Each step is a conditional sampling operation |

## Xem thêm 延伸阅读

- [Holbrook (2023): The Metropolis-Hastings Algorithm](https://arxiv.org/abs/2304.07010)- hướng dẫn chi tiết về cơ sở MCMC
- [Jang, Gu, Poole (2017): Categorical Reparameterization with Gumbel-Softmax](https://arxiv.org/abs/1611.01144)- giấy gốc Gumbel-Softmax
- [Holtzman et al. (2020): The Curious Case of Neural Text Degeneration](https://arxiv.org/abs/1904.09751)- giấy lấy mẫu hạt nhân (top-p)
- [Kingma & Welling (2014): Auto-Encoding Variational Bayes](https://arxiv.org/abs/1312.6114)- VAE giấy giới thiệu thủ thuật tái định đo lường
- [Ho, Jain, Abbeel (2020): Denoising Diffusion Probabilistic Models](https://arxiv.org/abs/2006.11239)- DDPM kết nối lấy mẫu với việc tạo hình ảnh
