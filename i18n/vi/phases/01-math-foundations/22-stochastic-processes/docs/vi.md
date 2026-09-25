# Quá trình Stochastic

> Sự ngẫu nhiên với cấu trúc, toán học đằng sau những bước đi ngẫu nhiên, chuỗi Markov và mô hình phân tán.
> Có tính tự nhiên cấu trúc.

**Type:** Learn | **类型:** 学习
**Language:**Python**语言:**Python
**Prerequisites:** Phase 1, Lessons 06-07 (probability, Bayes) | **前置知识:** Phase 1, 第 06-07 课（概率、贝叶斯）
**Time:** ~75 minutes | **时间:** ~75 分钟

## Mục tiêu học tập

- Chơi mô phỏng 1D và 2D đi bộ ngẫu nhiên và xác minh quy mô của sự di chuyển
  模拟一维和二维随机游走,验证位移的 √n 缩放规律
- Xây dựng một mô phỏng chuỗi Markov và tính toán phân bố tĩnh của nó thông qua cấu trúc riêng
   cấu trúc máy mô phỏng chuỗi Markov, thông qua tính cách phân tích tính toán phân bố bình tĩnh
- Thực hiện Metropolis-Hastings MCMC và động lực Langevin để lấy mẫu từ các phân phối mục tiêu
  实现 Metropolis-Hastings MCMC 和 Langevin 动力学, từ mục tiêu phân bố trong采样
- Kết nối quá trình phân tán về phía trước với chuyển động Brownian và giải thích cách quá trình ngược tạo ra dữ liệu
  Kết nối quá trình mở rộng hướng trước với chuyển động Brown, giải thích cách tạo dữ liệu ngược hướng


> **【中文解读】**
> 随机过程是有结构的随机性――马尔可夫链( trạng thái hiện tại chỉ phụ thuộc vào bước trước) là cơ sở của PageRank。 tiến trình trước của mô hình phổ biến là Brown运动(加噪), ngược tiến trình là tạo ra tiếng ồn。MCMC là nền tảng của thống kê của Bayesian。

## Vấn đề  vấn đề giới thiệu

Nhiều hệ thống AI liên quan đến sự ngẫu nhiên mà phát triển theo thời gian, không phải sự ngẫu nhiên tĩnh -- sự ngẫu nhiên cấu trúc, theo dõi nơi mỗi bước phụ thuộc vào những gì đã xảy ra trước đó.

> Nhiều hệ thống AI liên quan đến sự tự nhiên của sự phát triển theo thời gian. Không phải là sự tự nhiên tĩnh, mà là sự tự nhiên cấu trúc, sắp xếp.

Các mô hình ngôn ngữ tạo ra các token một lần. Mỗi token phụ thuộc vào bối cảnh trước đó. mô hình đưa ra phân phối xác suất, lấy mẫu từ nó, và di chuyển về phía trước. Đó là một quá trình stochastic.

> 语言模型逐个生成代币――每个代币取决于之前的上下文――模型输出一个概率分布,从中采样,然后继续――这是随机过程――

Các mô hình phân phối thêm tiếng ồn vào một hình ảnh từng bước cho đến khi nó trở thành tĩnh hoàn toàn. Sau đó chúng đảo ngược quá trình, từ chối từng bước cho đến khi một hình ảnh mới xuất hiện.

> Mô hình mở rộng từng bước vào hình ảnh thêm tiếng ồn, cho đến khi trở thành trạng thái tĩnh hoàn hảo.

Các đại lý học tập tăng cường thực hiện các hành động trong một môi trường. Mỗi hành động dẫn đến một trạng thái mới với một số xác suất. Đại lý theo một chính sách ngẫu nhiên trong một thế giới ngẫu nhiên.

> 强化学习智能体在环境中执行动作──每个动作以一定概率导致新状态──智能体在随机世界中遵循随机策略──整个系统是马尔可夫决策过程 (MDP)──

Việc lấy mẫu MCMC -- xương sống của suy luận Bayesian -- xây dựng một chuỗi Markov mà phân bố tĩnh là phía sau bạn muốn lấy mẫu từ.

> MCMC 采采贝叶斯推理的基石构建一个马尔可夫链,它的平稳分布就是你想从中采的后验分布

Tất cả đều dựa trên bốn ý tưởng cơ bản:
1. Đi bộ ngẫu nhiên - quá trình stochastic đơn giản nhất
2. Dòng chuỗi Markov -- sự ngẫu nhiên được cấu trúc với một matrix chuyển tiếp
3. Động lực Langevin - giảm gradient với tiếng ồn
4. Metropolis-Hastings - lấy mẫu từ bất kỳ phân phối nào

> Tất cả đều dựa trên bốn khái niệm cơ bản: 1. 随机游走简单的随机过程; 2. 马尔可夫链带转移矩阵的结构化随机性; 3. 动力学带噪音梯度下降; 4.

## Khái niệm cốt lõi

### Đi bộ ngẫu nhiên

Bắt đầu từ vị trí 0. Ở mỗi bước, ném một đồng xu công bằng. Đầu: di chuyển sang bên phải (+1). đuôi: di chuyển sang trái (-1).

> Từ vị trí 0 开始── từng bước抛一枚公平硬币──正面:向右 (+1)──反面:向左 (-1)──

Sau n bước, vị trí của bạn là tổng số n giá trị ngẫu nhiên +/-1. vị trí dự kiến là 0 (lần đi không thiên vị). Nhưng khoảng cách dự kiến từ nguồn tăng lên như sqrt(n).

> N 步后, vị trí của bạn là n 个随机 ±1 值的求和――期望位置为 0(游走无偏), nhưng khoảng cách từ điểm gốc 期望距离按√n 增长――

Điều này trái với trực giác. Đi bộ là công bằng - không có trôi dạt theo cả hai hướng. Nhưng theo thời gian, nó đi lang thang xa hơn và xa hơn từ nơi nó bắt đầu. Phản độ tiêu chuẩn sau n bước là sqrt(n).

> Đây là một điểm phản trực giác. Đi bộ là một cách công bằng.

```
Step 0:  Position = 0
Step 1:  Position = +1 or -1
Step 2:  Position = +2, 0, or -2
...
Step 100: Expected distance from origin ~ 10 (sqrt(100))
Step 10000: Expected distance from origin ~ 100 (sqrt(10000))
```

**In 2D**, bước đi di chuyển lên, xuống, trái, hoặc phải với xác suất tương đương.

> **二维情况下**,游走以等概率上下左右移动── tương tự √n 缩放 thích hợp cho khoảng cách đến điểm gốc, đường dẫn hình dạng hình dạng.

**Why sqrt(n)?**Mỗi bước là +1 hoặc -1 với xác suất tương đương. Sau n bước, vị trí S_n = X_1 + X_2 + ... + X_n nơi mỗi X_i là +/-1. Sự khác biệt của mỗi bước là 1, và các bước là độc lập, vì vậy Var(S_n) = n. Chỉnh tiêu chuẩn = sqrt(n. Theo định lý giới hạn trung tâm, S_n / sqrt(n) hội tụ với phân bố bình thường tiêu chuẩn.

> **为什么是 √n？**Mỗi bước khác biệt là 1, bước và bước độc lập, vì vậy Var(S_n) = n, chuẩn khác biệt = √n。由中心极限定理,S_n/√n 收到标准正态分布。

Quy mô này xuất hiện ở mọi nơi trong ML. SGD âm thanh scale như 1/sqrt(batch_size). Nhập kích thước scale như sqrt(d). Quảng gốc là chữ ký của các sự bổ sung ngẫu nhiên độc lập.

> √n 缩放放在 ML 中无处不在──SGD 噪音按1/√(batch_size) 缩放,嵌入维度按√d 缩放──平方根是独立随机叠加的标志──

**Connection to Brownian motion.**Hãy đi bộ ngẫu nhiên với kích thước bước 1/sqrt(n) và n bước mỗi đơn vị thời gian. Khi n đi đến vô tận, bước đi hội tụ với chuyển động Brownian B(t) - một quá trình liên tục thời gian nơi B(t) thường được phân phối với trung bình 0 và biến số t.

> **与布朗运动的联系。**取步长 1/√n、每单位时间 n 步的随机游走──当 n → ∞ 时,游走收到布朗运动 B(t) 一个连续时间过程,B(t) ~ N(0, t) ・・・

Hành động Brown là nền tảng toán học của sự phân tán. Nó mô hình hóa sự rung chuyển ngẫu nhiên của các hạt trong một chất lỏng, biến động của giá cổ phiếu, và - quan trọng hơn - quá trình tiếng ồn trong các mô hình phân tán.

> Phong trào Brown là nền tảng toán học của mô hình phổ biến. Nó mô tả sự biến động bất thường của các hạt trong cơ thể, biến động của giá cổ phiếu, cũng như quá trình âm thanh trong mô hình phổ biến quan trọng nhất.

**Gambler's ruin.**Một người đi bộ ngẫu nhiên bắt đầu ở vị trí k, với các rào cản hấp thụ ở 0 và N. xác suất đạt đến N trước 0 là gì? Đối với một bước đi công bằng: P(reach N) = k/N. Điều này là đáng ngạc nhiên đơn giản và thanh lịch. Nó kết nối với lý thuyết của martingales - bước đi ngẫu nhiên công bằng là một martingale (tín giá trị tương lai dự kiến = giá trị hiện tại).

> **赌徒破产问题。**Từ vị trí k xuất phát, ở 0 和 N 处有吸收壁──到 N(而不是 0) xác suất là bao nhiêu? fair游走:P = k/N── This link to 论 fair随机游走是一个──

### Dòng dây chuyền Markov

Một chuỗi Markov là một hệ thống chuyển đổi giữa các trạng thái theo xác suất cố định.

> Markov链 là một hệ thống chuyển đổi giữa các trạng thái dựa trên tỷ lệ cố định.

```
P(X_{t+1} = j | X_t = i, X_{t-1} = ...) = P(X_{t+1} = j | X_t = i)
```

Đây là tính năng Markov. nó có nghĩa là bạn có thể mô tả toàn bộ động lực bằng một số liệu chuyển tiếp P:

> Đó là tính chất của Markov. Nó có nghĩa là bạn có thể sử dụng chuyển động P để mô tả toàn bộ động lực.

```
P[i][j] = probability of going from state i to state j
```

Mỗi hàng của P cộng với 1 (bạn phải đi đâu đó).

> P của mỗi dòng và là 1 (((đúng là phải đi đâu đó))

**Example -- Weather:**

> **示例——天气：**

```
States: Sunny (0), Rainy (1), Cloudy (2)

P = [[0.7, 0.1, 0.2],    (if sunny: 70% sunny, 10% rainy, 20% cloudy)
     [0.3, 0.4, 0.3],    (if rainy: 30% sunny, 40% rainy, 30% cloudy)
     [0.4, 0.2, 0.4]]    (if cloudy: 40% sunny, 20% rainy, 40% cloudy)
```

Bắt đầu ở bất kỳ trạng thái nào. Sau nhiều chuyển đổi, phân phối các trạng thái hội tụ đến phân phối tĩnh pi, nơi pi * P = pi. Đây là vector tự bên trái của P với giá trị tự 1.

> Từ trạng thái bất kỳ bắt đầu, sau quá trình chuyển đổi đủ nhiều, phân bố trạng thái nhận được đến phân bố bình tĩnh π, đáp ứng π·P = π── đây là giá trị đặc điểm của P là 1 của các đặc điểm hướng trái.

Đối với chuỗi thời tiết, phân phối tĩnh có thể là [0,53, 0,18, 0,29] -- trong thời gian dài, nó là nắng 53% thời gian bất kể trạng thái khởi đầu.
Đối với chuỗi thời tiết, phân phối tĩnh là [0,55, 0,18, 0,27] -- trong thời gian dài, nó có mặt trời 55% thời gian bất kể trạng thái khởi đầu.

> Đối với chuỗi khí hậu, phân bố ổn định có thể là [0.53, 0.18, 0.29] dài hạn nhìn thấy 53% thời gian trong ngày, không liên quan đến trạng thái khởi điểm.

```mermaid
graph LR
    S["Sunny"] -->|0.7| S
    S -->|0.1| R["Rainy"]
    S -->|0.2| C["Cloudy"]
    R -->|0.3| S
    R -->|0.4| R
    R -->|0.3| C
    C -->|0.4| S
    C -->|0.2| R
    C -->|0.4| C
```

**Computing the stationary distribution.**Có hai cách tiếp cận:

1. **Power method**: nhân bất kỳ phân bố ban đầu bằng P nhiều lần. Sau đủ lần lặp lại, nó hội tụ.
2. **Eigenvalue method**: tìm được phương tiện riêng bên trái của P với giá trị riêng 1. Đây là phương tiện riêng của P^T với giá trị riêng 1.

> **计算平稳分布。**两种方法:1. **幂法**:反复用任意初始分布乘 P,足足多次后收──2. **特征值法**: Tìm giá trị đặc điểm của P với 1 ư cấu bên trái của P^T với giá trị đặc điểm bên phải của 1 ư cấu bên phải của P^T)

Cả hai cách tiếp cận đều đòi hỏi chuỗi đáp ứng các điều kiện hội tụ.

> 两种方法都要求链满足收条件.

**Convergence conditions.**Một chuỗi Markov hội tụ với một phân phối tĩnh độc đáo nếu:
- **Irreducible**: mọi bang đều có thể tiếp cận từ mọi bang khác
- **Aperiodic**: chuỗi không có chu kỳ với thời gian cố định

> **收敛条件。**Các chuỗi có thể được phân phối một cách ổn định nhất:**不可约**(mỗi trạng thái đều có thể từ trạng thái khác đến);**非周期**(Cây sẽ không được định hình vòng quay)

Hầu hết các chuỗi mà bạn gặp trong ML đáp ứng cả hai điều kiện.

> Phần lớn các chuỗi bạn gặp trong ML đều đáp ứng hai điều kiện này.

**Absorbing states.**Một trạng thái hấp thụ nếu một khi bạn nhập nó, bạn không bao giờ rời đi (P[i][i] = 1). hấp thụ chuỗi Markov mô hình hóa các quy trình với các trạng thái cuối cùng - một trò chơi kết thúc, một khách hàng trộn trộn, một chuỗi token chạm vào token cuối văn bản.

> **吸收状态。**Một khi vào trạng thái không rời đi mãi mãi (P[i][i]=1) ⋅ hấp thụ các mã thông báo kết thúc của game 流失的客户、命中结束代币的序列

**Mixing time.**Số bước cho đến khi chuỗi "gần" với phân phối tĩnh? Về hình thức, số bước cho đến khi khoảng cách thay đổi tổng thể từ tĩnh giảm xuống dưới một số ngưỡng.

> **混合时间。**链"接近"平稳分布需要多少步骤? 链"接近"平稳分布需要多少步骤? 形式上,是与平稳分布的总变差距降至值以下的步数──快混合 = 步数少──谱间隙(1 - 第二大特征值) 控制混合时间:间隙越大,混合越快──

### Kết nối với các mô hình ngôn ngữ

Tạo token trong một mô hình ngôn ngữ là một quá trình Markov. Với bối cảnh hiện tại, mô hình sẽ phát ra phân phối trên token tiếp theo. Nhiệt độ kiểm soát độ sắc:

> 语言模型的代币 生成近似是一个马尔可夫过程――给定当前上下文,模型输出下一个代币的概率分布――温度 控制分布的尖度:

```
P(token_i) = exp(logit_i / temperature) / sum(exp(logit_j / temperature))
```

- Nhiệt độ = 1,0: phân phối tiêu chuẩn
- Nhiệt độ < 1,0: sắc hơn (đối đa xác định)
- Nhiệt độ > 1,0: phẳng hơn (thường tình cờ hơn)
- Nhiệt độ -> 0: argmax (cười tham)

> Nhiệt độ=1.0 标准分布;<1.0 更尖(更确定性);>1.0 更平坦(更随机);→0 退化为 argmax(贪心解码)

Top-k lấy mẫu cắt giảm đến các token có xác suất cao nhất k. Top-p (tâm) lấy mẫu cắt giảm đến các token nhỏ nhất có xác suất tích lũy vượt quá p. Cả hai đều sửa đổi xác suất chuyển đổi Markov.

> Top-k 采样保留概率最高的 k 个代币;Top-p(核采样) giữ概率累积超过p 的最小代币集合──两者都修改了马可夫转移概率──

### Động thái Brown

Giới hạn thời gian liên tục của bước ngẫu nhiên.
1. B(0) = 0
2. B(t) - B(s) thường được phân phối với trung bình 0 và biến số t - s (cho t > s)
3. Các sự gia tăng trên các khoảng không chồng chéo là độc lập

> 布朗运动是随机游走的连续时间极限──B(t) 有三条性质:B(0)=0;B(t) -B(s) ~ N(0, t-s); không chồng lên区间上的增量独立──

Phong trào Brown liên tục nhưng không thể phân biệt được ở đâu cả - nó rung động ở mọi thang.

> Bronh vận động liên tục nhưng ở đâu không thể dẫn dắt nó di chuyển ở mỗi thước.

Trong mô phỏng riêng biệt, bạn ước tính chuyển động của Browni bằng:

```
B(t + dt) = B(t) + sqrt(dt) * z,    where z ~ N(0, 1)
```

Các sqrt(dt) quy mô là quan trọng. Nó đến từ định lý giới hạn trung tâm áp dụng cho các bước ngẫu nhiên.

> 离散仿真中用 B(t+dt) = B(t) + √dt × z 近似布朗运动(z ~ N(0,1)) √dt 缩放很关键,源自随机游走的中心极限理。

### Langevin Dynamics

Sự giảm gradient tìm thấy tối thiểu của một hàm. Dinamika Langevin tìm thấy phân bố xác suất tương xứng với exp(-U(x) / T), nơi U là một hàm năng lượng và T là nhiệt độ.

> 梯度下降找函数最小值──Langevin 动力学找概率分布  exp(-U(x) /T), trong đó U là hàm năng lượng, T là nhiệt độ──

```
x_{t+1} = x_t - dt * gradient(U(x_t)) + sqrt(2 * T * dt) * z_t
```

Hai lực tác động lên hạt:
1. **Gradient force**(-dt * gradient(U)): đẩy về hướng năng lượng thấp (như giảm gradient)
2. **Random force**(sqrt(2*T*dt) * z): đẩy theo hướng ngẫu nhiên (khám phá)

> 两种力作用在粒子上:1. **梯度力**推向低能量(类似梯度下降); 2. **随机力**推向随机方向 (tiếp theo hướng)

Ở nhiệt độ T = 0, đây là sự giảm gradient tinh khiết. Ở nhiệt độ cao, nó gần như là một bước đi ngẫu nhiên.

> 温度 T=0 时是纯梯度下降. 温度高时近似随机游走. 适应的温度下, các hạt tìm kiếm năng lượng cảnh quan và ở lại trong vùng năng lượng thấp lâu hơn.

**Connection to diffusion models.**Quá trình tiến bộ của mô hình phân tán là:

```
x_t = sqrt(alpha_t) * x_{t-1} + sqrt(1 - alpha_t) * noise
```

Đây là một chuỗi Markov liên tục trộn dữ liệu với tiếng ồn.

> 扩散模型的前向过程:x_t = √α_t × x_{t-1} + √(1-α_t) × 噪音──这是逐步混入噪音的马尔可夫链,足足多步后 x_T 变为纯高的噪音──

Quá trình ngược -- từ tiếng ồn trở lại dữ liệu -- cũng là chuỗi Markov, nhưng xác suất chuyển đổi của nó được tìm hiểu bởi một mạng lưới thần kinh. mạng học cách dự đoán tiếng ồn được thêm vào mỗi bước, sau đó trừ nó.

> Quá trình ngược từ tiếng ồn trở lại dữ liệu cũng là chuỗi của Markov, nhưng tỷ lệ chuyển đổi được học bởi mạng lưới thần kinh.

```mermaid
graph LR
    subgraph "Forward Process (add noise)"
        X0["x_0 (data)"] -->|"+ noise"| X1["x_1"]
        X1 -->|"+ noise"| X2["x_2"]
        X2 -->|"..."| XT["x_T (pure noise)"]
    end
    subgraph "Reverse Process (denoise)"
        XT2["x_T (noise)"] -->|"neural net"| XR2["x_{T-1}"]
        XR2 -->|"neural net"| XR1["x_{T-2}"]
        XR1 -->|"..."| XR0["x_0 (generated data)"]
    end
```

### MCMC: Markov Chain Monte Carlo

Đôi khi bạn cần lấy mẫu từ phân bố p ((x) mà bạn có thể đánh giá (trong một liên tục) nhưng không thể lấy mẫu trực tiếp. Bayesian hậu là ví dụ cổ điển - bạn biết khả năng gấp đôi trước, nhưng các định hình bình thường hóa là khó xử lý.

> Đôi khi bạn cần một số có thể tính toán nhưng thiếu một số thường xuyên được tính toán nhưng không thể trực tiếp lấy được phân bố p (x) trong các mẫu.

**Metropolis-Hastings**xây dựng chuỗi Markov có phân bố tĩnh là p(x):

1. Bắt đầu ở một số vị trí x
2. Đề xuất một vị trí mới x' từ một phân phối đề xuất Q(x' ảix)
3. Tỷ lệ chấp nhận tính toán: a(x') * Q(x khiếu x') / (p(x) * Q(x khiếu x))
4. Hãy chấp nhận x' với xác suất min ((1, a). Nếu không, hãy ở x.
5. Lặp lại.

> **Metropolis-Hastings**构建一个平稳分布为 p(x) 的马尔可夫链:1) Từ một điểm nào đó x 出发;2) 从提议分布 Q(x' còn x) 提出新位置 x';3) 计算接受率 a = p(x') Q(x' 了x') /(p(x) Q(x' 了x));4) 以概率 min(1,a) 接受,否则停留;5) 重复.

Nếu Q là đối xứng ví dụ, Q(x' (ởx) = Q(x (ởx') = N(x, sigma^2)), tỷ lệ đơn giản hóa thành a = p(x') / p(x. Bạn chỉ cần tỷ lệ xác suất - các định kỳ bình thường hóa hủy bỏ.

> Nếu Q đối với các phương pháp (如高斯), tỷ lệ chấp nhận được đơn giản hóa thành a = p(x') / p(x)  chỉ cần tỷ lệ xác suất so với các phương pháp tự động loại bỏ, đó chính là lý do MCMC cho các phương pháp chấp nhận sau đó rất hữu ích.

Mạng lưới này được đảm bảo sẽ hội tụ với p ((x) trong điều kiện nhẹ. Nhưng hội tụ có thể chậm nếu đề xuất quá nhỏ (quá trình ngẫu nhiên) hoặc quá lớn (đánh giá cao).

> Trong điều kiện nhiệt độ và thấp, nhưng nhận có thể chậm hơn, trở thành quá nhỏ hoặc quá lớn.

**Why it works.**Tỷ lệ chấp nhận đảm bảo sự cân bằng chi tiết: xác suất ở x và di chuyển đến x' bằng với xác suất ở x' và di chuyển đến x. Sự cân bằng chi tiết cho thấy p(x) là phân bố tĩnh của chuỗi.

> **为什么有效**: tỷ lệ chấp nhận đảm bảo tỉ lệ tỉ lệ tỉ lệ tỉ lệ tỉ lệ tỉ lệ tỉ lệ tỉ lệ tỉ lệ tỉ lệ tỉ lệ tỉ lệ tỉ lệ tỉ lệ tỉ lệ tỉ lệ tỉ lệ tỉ lệ tỉ lệ tỉ lệ tỉ lệ tỉ lệ tỉ lệ tỉ lệ tỉ lệ tỉ lệ tỉ lệ tỉ lệ tỉ lệ tỉ lệ tỉ lệ tỉ lệ tỉ lệ tỉ lệ tỉ lệ tỉ lệ tỉ lệ tỉ lệ tỉ lệ tỉ lệ tỉ lệ tỉ lệ tỉ lệ tỉ lệ tỉ lệ tỉ lệ tỉ lệ tỉ lệ tỉ lệ tỉ lệ tỉ lệ tỉ lệ tỉ lệ tỉ lệ tỉ lệ tỉ lệ tỉ lệ tỉ lệ tỉ lệ tỉ lệ tỉ lệ tỉ lệ tỉ lệ tỉ lệ tỉ lệ tỉ lệ tỉ lệ tỉ lệ tỉ lệ tỉ lệ tỉ lệ tỉ lệ tỉ lệ tỉ lệ tỉ lệ tỉ lệ tỉ lệ tỉ lệ tỉ lệ tỉ lệ tỉ lệ tỉ lệ tỉ lệ tỉ lệ tỉ lệ tỉ lệ tỉ lệ tỉ lệ tỉ lệ tỉ lệ tỉ lệ tỉ lệ tỉ lệ tỉ lệ tỉ lệ tỉ lệ tỉ lệ tỉ lệ tỉ lệ tỉ lệ tỉ lệ tỉ lệ tỉ lệ tỉ lệ tỉ lệ tỉ lệ tỉ lệ tỉ lệ tỉ lệ tỉ lệ tỉ lệ tỉ lệ tỉ lệ tỉ lệ tỉ lệ tỉ lệ tỉ lệ tỉ lệ tỉ lệ tỉ lệ tỉ lệ tỉ lệ tỉ lệ tỉ lệ tỉ lệ tỉ lệ tỉ lệ tỉ lệ tỉ lệ tỉ số tỉ số tỉ lệ tỉ lệ tỉ lệ tỉ lệ tỉ lệ tỉ số tỉ số tỉ lệ tỉ số tỉ số tỉ lệ tỉ lệ tỉ số tỉ số tỉ số tỉ số tỉ số tỉ số tỉ số tỉ số tỉ số tỉ số tỉ số tỉ số tỉ số tỉ số tỉ số tỉ số tỉ số tỉ số tỉ số tỉ số tỉ số tỉ số tỉ số tỉ số tỉ số tỉ số tỉ số tỉ số tỉ số tỉ số tỉ số tỉ số tỉ số tỉ số tỉ số tỉ số tỉ số tỉ số tỉ số tỉ số tỉ số tỉ số tỉ số tỉ số tỉ số tỉ số tỉ số tỉ số tỉ số tỉ số tỉ số tỉ số tỉ số tỉ số tỉ số tỉ số tỉ số tỉ số tỉ số tỉ số tỉ số tỉ số tỉ số tỉ số tỉ số tỉ số tỉ số tỉ số tỉ số tỉ số tỉ số tỉ số tỉ số tỉ số tỉ số tỉ số tỉ số tỉ số tỉ số tỉ số tỉ số tỉ số tỉ số tỉ số tỉ số tỉ số tỉ số tỉ số tỉ số tỉ số tỉ số tỉ số tỉ số tỉ số tỉ số tỉ số tỉ số tỉ số tỉ số tỉ số tỉ số tỉ số tỉ số tỉ số tỉ số tỉ số tỉ số tỉ số tỉ

**Practical considerations:**
- **Burn-in**: loại bỏ các mẫu N đầu tiên. chuỗi cần thời gian để đạt được phân phối tĩnh từ điểm khởi đầu của nó.
- **Thinning**: giữ mỗi mẫu k-th để giảm sự tương quan tự động.
- **Multiple chains**: chạy nhiều chuỗi từ các điểm khởi đầu khác nhau. Nếu chúng hội tụ đến cùng một phân bố, bạn có bằng chứng về hội tụ.
- **Acceptance rate**: cho các đề xuất Gaussian trong d chiều, tỷ lệ chấp nhận tối ưu là khoảng 23% (Roberts & Rosenthal, 2001).

> 实战要点:**Burn-in**丢弃前 N 个样本(链需要时间到达平稳分布);**Thinning**Mỗi k 个样本取一个(降低自相关);**Multiple chains**Từ các điểm khác nhau chạy nhiều条链 ((Nếu nhận đến cùng phân phối, thì có chứng cứ nhận);**Acceptance rate**Tỷ lệ chấp nhận tối ưu của đề nghị cao hơn khoảng 23%

### Quá trình Stochastic trong AI

| Process | AI Application |
|---------|---------------|
| Random walk | Exploration in RL, Node2Vec embeddings |
| Markov chain | Text generation, MCMC sampling |
| Brownian motion | Diffusion models (forward process) |
| Langevin dynamics | Score-based generative models, SGLD |
| Markov decision process | Reinforcement learning |
| Metropolis-Hastings | Bayesian inference, posterior sampling |

> 随机过程在 AI 中的应用:随机游走:RL 探索、Node2Vec 嵌入) 、马尔可夫链 (文本生成、MCMC) 、布朗运动 (扩散模型前向) 、Langevin 动力学 (Score-based 模型、SGLD) 、马尔可夫决策过程 (强化学习) 、Metropolis-Hastings (Mỹ) ̇贝叶斯推理、后验采样) ⋅

## Hãy xây dựng nó.
```figure
random-walk-diffusion
```

## Hãy xây dựng nó

### Bước 1: Máy mô phỏng đi bộ ngẫu nhiên

> 第1步:随机游走模拟器──1D 用累加和,2D 用四个方向(上下左右) 的累加──

```python
import numpy as np

def random_walk_1d(n_steps, seed=None):
    rng = np.random.RandomState(seed)
    steps = rng.choice([-1, 1], size=n_steps)
    positions = np.concatenate([[0], np.cumsum(steps)])
    return positions


def random_walk_2d(n_steps, seed=None):
    rng = np.random.RandomState(seed)
    directions = rng.choice(4, size=n_steps)
    dx = np.zeros(n_steps)
    dy = np.zeros(n_steps)
    dx[directions == 0] = 1   # right
    dx[directions == 1] = -1  # left
    dy[directions == 2] = 1   # up
    dy[directions == 3] = -1  # down
    x = np.concatenate([[0], np.cumsum(dx)])
    y = np.concatenate([[0], np.cumsum(dy)])
    return x, y
```

1D walk lưu trữ tổng tích lũy. Mỗi bước là +1 hoặc -1. Sau n bước, vị trí là tổng. Sự khác biệt tăng tuyến tính với n, do đó lệch chuẩn tăng như sqrt(n.

> Một chiều theo thời gian đi lưu trữ tích lũy và── mỗi bước là +1 hoặc -1──n bước sau vị trí là tổng cộng──方差线性增长 n, tiêu chuẩn差按 √n 增长──

### Bước 2: Dòng dây chuyền Markov

> 第2步:Markoff链――step() 按转移概率选下一状态;模拟() 跑多步生成轨迹;stationary_distribution() 用特征分解求平稳分布;;

```python
class MarkovChain:
    def __init__(self, transition_matrix, state_names=None):
        self.P = np.array(transition_matrix, dtype=float)
        self.n_states = len(self.P)
        self.state_names = state_names or [str(i) for i in range(self.n_states)]

    def step(self, current_state, rng=None):
        if rng is None:
            rng = np.random.RandomState()
        probs = self.P[current_state]
        return rng.choice(self.n_states, p=probs)

    def simulate(self, start_state, n_steps, seed=None):
        rng = np.random.RandomState(seed)
        states = [start_state]
        current = start_state
        for _ in range(n_steps):
            current = self.step(current, rng)
            states.append(current)
        return states

    def stationary_distribution(self):
        eigenvalues, eigenvectors = np.linalg.eig(self.P.T)
        idx = np.argmin(np.abs(eigenvalues - 1.0))
        stationary = np.real(eigenvectors[:, idx])
        stationary = stationary / stationary.sum()
        return np.abs(stationary)
```

Phân bố tĩnh là vector tự động trái của P với giá trị tự động 1. Chúng ta tìm thấy nó bằng cách tính toán vector tự động của P^T (trả chuyển các vector tự động trái thành vector tự động phải).

> Phân bố bình thường là một khối lượng đặc điểm bên trái của P với giá trị 1 ⋅ qua P^T 求 đặc điểm đạt được ⋅ chuyển đổi khối lượng đặc điểm bên trái thành khối lượng đặc điểm bên phải ⋅

### Bước 3: Động lực Langevin

> 第3步:Langevin 动力学──梯度下降 + 高斯噪音 = 探索能量景观并采样──

```python
def langevin_dynamics(grad_U, x0, dt, temperature, n_steps, seed=None):
    rng = np.random.RandomState(seed)
    x = np.array(x0, dtype=float)
    trajectory = [x.copy()]
    for _ in range(n_steps):
        noise = rng.randn(*x.shape)
        x = x - dt * grad_U(x) + np.sqrt(2 * temperature * dt) * noise
        trajectory.append(x.copy())
    return np.array(trajectory)
```

Phong trào đẩy x về phía năng lượng thấp. tiếng ồn ngăn chặn nó bị kẹt. Ở trạng thái cân bằng, phân bố các mẫu tương xứng với exp ((-U(x) / nhiệt độ).

> 梯度把 x 推向低能量区, tiếng ồn ngăn chặn bị mắc kẹt trong vùng 优──平衡时样本分布  exp(-U(x) /温度) 

### Bước 4: Metropolis-Hastings

> 第4步:Metropoles-Hastings MCMC──从目标分布(无需归归化常数)采用样式经典算法──

```python
def metropolis_hastings(target_log_prob, proposal_std, x0, n_samples, seed=None):
    rng = np.random.RandomState(seed)
    x = np.array(x0, dtype=float)
    samples = [x.copy()]
    accepted = 0
    for _ in range(n_samples - 1):
        x_proposed = x + rng.randn(*x.shape) * proposal_std
        log_ratio = target_log_prob(x_proposed) - target_log_prob(x)
        if np.log(rng.rand()) < log_ratio:
            x = x_proposed
            accepted += 1
        samples.append(x.copy())
    acceptance_rate = accepted / (n_samples - 1)
    return np.array(samples), acceptance_rate
```

Các thuật toán đề xuất một điểm mới, kiểm tra xem nó có xác suất cao hơn (hoặc chấp nhận với xác suất tương xứng với tỷ lệ), và lặp lại. Tỷ lệ chấp nhận nên khoảng 23-50% cho sự trộn tốt.

> 算法流程:提议新点 → 检查概率是否更高 (或按比例接受)→ 重复.

## Hãy sử dụng nó để thực hiện

Thực tế, bạn sử dụng thư viện đã được thiết lập cho các thuật toán này. Nhưng hiểu cơ học là quan trọng để gỡ lỗi và điều chỉnh.

> Thực tế, bạn sử dụng cơ sở dữ liệu đã trưởng thành để thực hiện các thuật toán này.

```python
import numpy as np

rng = np.random.RandomState(42)
walk = np.cumsum(rng.choice([-1, 1], size=10000))
print(f"Final position: {walk[-1]}")
print(f"Expected distance: {np.sqrt(10000):.1f}")
print(f"Actual distance: {abs(walk[-1])}")
```

> NumPy 实现随机游走:一行代码生成 10000 步 ±1 随机游走,验证实际距离与理论值 √10000 = 100 接近──

### Numpy cho các matrices chuyển tiếp

```python
import numpy as np

P = np.array([[0.7, 0.1, 0.2],
              [0.3, 0.4, 0.3],
              [0.4, 0.2, 0.4]])

distribution = np.array([1.0, 0.0, 0.0])
for _ in range(100):
    distribution = distribution @ P

print(f"Stationary distribution: {np.round(distribution, 4)}")
```

> NumPy  xử lý chuyển chuyển矩阵: từ [1,0,0] 出发,反复左乘 P 100 lần, tự động nhận到平稳分布──这就是PageRank等算法的核心──

Bội số phân bố ban đầu bằng P nhiều lần. Sau đủ lần lặp lại, nó hội tụ với phân bố tĩnh bất kể bạn bắt đầu ở đâu. Đây là phương pháp năng lượng để tìm ra vector tự chủ bên trái.

> 反复使用初始分布乘 P. 足够多次代后,无论从哪个开始都收到平稳分布.

### Kết nối với các khung thực tế

- **PyTorch diffusion:**- `DDPMScheduler`Trong khuôn mặt ôm `diffusers`thực hiện các chuỗi Markov phía trước và ngược
- **NumPyro / PyMC:**Sử dụng MCMC (NUTS samplingler, cải thiện trên Metropolis-Hastings) cho suy luận Bayesian
- **Gymnasium (RL):**Chức năng bước môi trường xác định quá trình quyết định Markov

> Với khung thực tế                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                          `diffusers`DDPMScheduler đã thực hiện các mô hình mở rộng trước / ngược về chuỗi Markoff;NumPyro / PyMC sử dụng NUTS 采样器 (Métropolis-Hastings phiên bản cải tiến) làm các suy luận của Bayes;Phương thức bước của trường Đào tạo xác định quá trình quyết định Markoff;;

### Kiểm tra sự hội tụ chuỗi Markov

```python
import numpy as np

P = np.array([[0.9, 0.1], [0.3, 0.7]])

eigenvalues = np.linalg.eigvals(P)
spectral_gap = 1 - sorted(np.abs(eigenvalues))[-2]
print(f"Eigenvalues: {eigenvalues}")
print(f"Spectral gap: {spectral_gap:.4f}")
print(f"Approximate mixing time: {1/spectral_gap:.1f} steps")
```

Khoảng cách quang phổ cho bạn biết chuỗi quên đi trạng thái ban đầu nhanh như thế nào. Khoảng cách 0,2 nghĩa là khoảng 5 bước để trộn. Khoảng cách 0,01 nghĩa là khoảng 100 bước. Luôn kiểm tra điều này trước khi chạy mô phỏng dài - một chuỗi trộn chậm tính toán chất thải.

> 谱隙告诉你链多快忘初状态――0.2 间隙约需要5步混合;0.01 约需要100步――运行长仿真前总要检查这个慢混合的链浪费算力――

## Chuyển nó đi.

Bài học này mang lại:
- `outputs/prompt-stochastic-process-advisor.md`-- một lời nhắc giúp xác định khung quy trình stochastic áp dụng cho một vấn đề nhất định

> 本课产出: giúp nhận ra các vấn đề được xác định phù hợp với các khuôn khổ quy trình tự do.

## Liên kết khái niệm liên kết bản đồ

| Concept | Where it shows up |
|---------|------------------|
| Random walk | Node2Vec graph embeddings, exploration in RL |
| Markov chain | Token generation in LLMs, MCMC sampling |
| Brownian motion | Forward diffusion process in DDPM, SDE-based models |
| Langevin dynamics | Score-based generative models, stochastic gradient Langevin dynamics (SGLD) |
| Stationary distribution | MCMC convergence target, PageRank |
| Metropolis-Hastings | Bayesian posterior sampling, simulated annealing |
| Temperature | LLM sampling, Boltzmann exploration in RL, simulated annealing |
| Mixing time | Convergence speed of MCMC, spectral gap analysis |
| Absorbing state | End-of-sequence token, terminal states in RL |
| Detailed balance | Correctness guarantee for MCMC samplers |

> 概念关联:随机游走(Node2Vec、RL 探索)、马尔可夫链(LLM token 生成、MCMC)、布朗运动)、DDPM 前向过程)、Langevin 动力学(Score-based 模型、SGLD)、平稳分布(MCMC 收目标、PageRank)、Metropolis-Hastings(贝叶斯后验、模拟退火)、Temperatur (((M 采样、Boltzmann 探索)、Mixing time ((MCMC 收速度)、Absorbing state ((序列结束、RL 终止状态)、详细平衡证券(MCMC 采样器的正确性保证)、

Các mô hình phân tán xứng đáng được chú ý đặc biệt. DDPM (Ho et al., 2020) xác định chuỗi Markov phía trước:

```
q(x_t | x_{t-1}) = N(x_t; sqrt(1-beta_t) * x_{t-1}, beta_t * I)
```

khi beta_t là một lịch trình tiếng ồn. Sau bước T, x_T là khoảng N(0, I).

```
p_theta(x_{t-1} | x_t) = N(x_{t-1}; mu_theta(x_t, t), sigma_t^2 * I)
```

Mỗi bước của thế hệ là một bước trong một chuỗi Markov học.

SGLD (Stochastic Gradient Langevin Dynamics) kết hợp giảm gradient mini-batch với tiếng ồn Langevin. Thay vì tính toán độ tốc đầy đủ, bạn sử dụng ước tính stochastic và thêm âm thanh chuẩn. Khi tốc độ học tập giảm, SGLD chuyển từ tối ưu hóa sang lấy mẫu -- bạn có được mẫu sau Bayesian gần như miễn phí. Đây là một trong những cách đơn giản nhất để có được ước tính không chắc chắn từ một mạng lưới thần kinh.

Ý tưởng quan trọng trong tất cả các mối liên hệ này: các quy trình stochastic không chỉ là các công cụ lý thuyết. Chúng là cơ chế tính toán bên trong các hệ thống AI hiện đại. Khi bạn điều chỉnh nhiệt độ của một LLM, bạn đang điều chỉnh một chuỗi Markov. Khi bạn đào tạo một mô hình phân tán, bạn đang học cách đảo ngược một quá trình giống như chuyển động Brownian. Khi bạn chạy suy luận Bayesian, bạn đang xây dựng một chuỗi hội tụ với phía sau.

> Tham khảo tất cả các liên kết này: quá trình tự động không chỉ là công cụ lý thuyết, chúng là cơ chế tính toán trong hệ thống AI hiện đại.

## Tập luyện bài tập

1. **Simulate 1000 random walks of 10000 steps.**Chụp bản phân phối các vị trí cuối cùng. Kiểm tra nó là khoảng Gaussian với trung bình 0 và lệch chuẩn sqrt(10000) = 100.

2. **Build a text generator using a Markov chain.**Trình luyện trên một tập hợp nhỏ: cho mỗi từ, đếm chuyển tiếp đến từ tiếp theo. Xây dựng các trận chuyển tiếp. Tạo ra các câu mới bằng cách lấy mẫu từ chuỗi.

3. **Implement simulated annealing**sử dụng Metropolis-Hastings. Bắt đầu ở nhiệt độ cao (tận dụng hầu hết mọi thứ) và dần dần làm mát (tận dụng chỉ cải tiến). Sử dụng nó để tìm tối thiểu của một chức năng với nhiều tối thiểu địa phương.

4. **Compare Langevin dynamics at different temperatures.**Mô hình từ tiềm năng hố hai U(x) = (x^2 - 1)^2. ở nhiệt độ thấp, các mẫu tập hợp trong một hố.

5. **Implement the forward diffusion process.**Bắt đầu với một tín hiệu 1D (ví dụ, một sóng âm đạo). Thêm tiếng ồn dần dần hơn 100 bước với một lịch trình tiếng ồn tuyến tính. Hãy cho thấy tín hiệu suy giảm xuống là tiếng ồn tinh khiết. Sau đó thực hiện một biểu tượng đơn giản đảo ngược quá trình (ngay cả một sự ngây thơ mà chỉ trừ được tiếng ồn ước tính).

## Từ khóa  Từ khóa nhanh chóng

| Term | What people say | What it actually means |
|------|----------------|----------------------|
| Random walk | "Coin-flip movement" | A process where position changes by random increments at each step |
| Markov property | "Memoryless" | The future depends only on the present state, not on the history |
| Transition matrix | "The probability table" | P[i][j] = probability of moving from state i to state j |
| Stationary distribution | "The long-run average" | The distribution pi where pi*P = pi -- the chain's equilibrium |
| Brownian motion | "Random jiggling" | The continuous-time limit of a random walk, B(t) ~ N(0, t) |
| Langevin dynamics | "Gradient descent with noise" | Update rule that combines deterministic gradient and random perturbation |
| MCMC | "Walking toward the target" | Constructing a Markov chain whose stationary distribution is the one you want |
| Metropolis-Hastings | "Propose and accept/reject" | MCMC algorithm that uses acceptance ratios to ensure convergence |
| Temperature | "The randomness knob" | Parameter controlling the tradeoff between exploration and exploitation |
| Diffusion process | "Noise in, noise out" | Forward: gradually add noise. Reverse: gradually remove it. Generates data. |

> 术语速查:Tự ngẫu nhiên đi (随机游走) ‧Mỹkov thuộc tính (无记忆性) ‧Trix chuyển (转移矩阵) ‧P[i][j]) ‧Phack phân phối (stationary distribution) ‧平稳分布 π·P=π) ‧Brownian motion ‧布朗运动 B(t) ~N(0,t)) ‧Langevin dynamics ‧带噪音的梯度下降) ‧MCMC ‧构造平稳分布为目标分布的马尔可夫链) ‧Mètropolis-Hastings ‧提议-接受/拒绝MC 算法) ‧Temperatur ‧探索/利用平衡参数) ‧Diffusion process ‧前加噪、反向去噪音生成数据) ‧

## Xem thêm 延伸阅读

- **Ho, Jain, Abbeel (2020)**- "Thử bác bỏ các mô hình xác suất phân tán". Bài báo DDPM đã khởi động cuộc cách mạng mô hình phân tán.
- **Song & Ermon (2019)**-- "Mô hình hóa tổng thể bằng cách ước tính các gradient của phân phối dữ liệu". Phương pháp dựa trên điểm sử dụng động lực Langevin cho việc lấy mẫu.
- **Roberts & Rosenthal (2004)**-- "Thống kê Markov và thuật toán MCMC". Lý thuyết đằng sau khi và tại sao MCMC hoạt động.
- **Norris (1997)**- "Markov Chains". - Cuốn sách giáo khoa tiêu chuẩn.
- **Welling & Teh (2011)**"Sự học Bayesian thông qua động lực Langevin Gradient Stochastic". Kết hợp SGD với động lực Langevin cho suy luận Bayesian có thể mở rộng.
