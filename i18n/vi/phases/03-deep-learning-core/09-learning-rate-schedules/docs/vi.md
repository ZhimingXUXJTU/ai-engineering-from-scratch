# Học tập tỷ lệ lịch trình và ấm lên  Học tập tỷ lệ điều chỉnh và dự kiến

> Tốc độ học tập là một siêu tham số quan trọng nhất. Không phải kiến trúc, không phải kích thước tập dữ liệu, không phải chức năng kích hoạt, tốc độ học tập. Nếu bạn không điều chỉnh gì khác, điều chỉnh này.

> **【中文解读】**Tỷ lệ học tập là siêu yếu tố quan trọng nhất không phải là cấu trúc, không phải là số lượng dữ liệu, là tỷ lệ học tập. Llama 3 sử dụng giá trị đỉnh lr = 3e-4 + 2000 bước nóng lên + sự phân rã của vũ trụ. GPT-3 sử dụng lr = 6e-4 + nóng lên.

**Type:** Build
**Languages:** Python
**Prerequisites:** Lesson 03.06 (Optimizers), Lesson 03.08 (Weight Initialization)
**Time:** ~90 minutes

## Mục tiêu học tập

- Thực hiện các lịch trình học tập liên tục, phân rã từng bước, gia tăng co-sin, ấm lên + co-sin và tốc độ học tập 1 chu kỳ từ đầu
- Hiển thị ba chế độ thất bại trong việc lựa chọn tốc độ học tập: chênh lệch (quá cao), trì hoãn (quá thấp) và dao động (không phân rã)
- Giải thích tại sao sự ấm áp là cần thiết cho những người cải thiện dựa trên Adam và làm thế nào nó ổn định việc đào tạo sớm
- So sánh tốc độ hội tụ trong tất cả năm lịch trình trên cùng một nhiệm vụ và chọn một phù hợp cho một ngân sách đào tạo nhất định

> **【中文解读】**本章实现五种学习率调度:恒定、阶梯衰减、余弦退火、加热+余弦、1周期 策略。 chuẩn cấu trúc của mô hình lớn hiện đại là nóng lên(前 1-5% 步数线性升温) + sự phân rã của vũ trụ(余弦衰减到接近零)。 hiểu nóng lên Tại sao cần thiết là关键。

## Vấn đề  vấn đề giới thiệu

Đặt tốc độ học tập là 0.1. Trình luyện khác nhau -- mất mát nhảy vô hạn trong 3 bước. Đặt nó là 0.0001. Trình luyện xẻo - sau 100 thời đại, mô hình hầu như không di chuyển từ ngẫu nhiên. Đặt nó là 0.01. Trình luyện hoạt động trong 50 thời đại, sau đó mất mát dao động xung quanh mức tối thiểu nó không bao giờ đạt được bởi vì các bước quá lớn.

> Một số học sinh đã học được từ một thời điểm đến một thời điểm khác, nhưng không thể tìm thấy một số học sinh khác.

Tốc độ học tập tối ưu không phải là một sự ổn định. Nó thay đổi trong quá trình đào tạo. Đầu tiên, bạn muốn các bước lớn để phủ mặt đất nhanh chóng. Cuối buổi đào tạo, bạn muốn các bước nhỏ để ổn định thành một mức tối thiểu sắc nét. Sự khác biệt giữa mô hình 90% chính xác và mô hình 95% chính xác thường chỉ là lịch trình.

> Tỷ lệ học tập tối ưu không phải là một con số thường xuyên. Nó thay đổi trong quá trình đào tạo.

Mỗi mô hình lớn được xuất bản trong ba năm qua sử dụng một lịch trình tốc độ học tập. Llama 3 sử dụng đỉnh lr = 3e-4 với 2000 bước nóng lên và sự phân rã cosine đến 3e-5. GPT-3 sử dụng lr = 6e-4 với nóng lên hơn 375 triệu token.

> 过去三年发表的每个主要模型都使用学习率调度──Llama 3 使用峰值 lr=3e-4,2000 步升和余弦衰减到3e-5──GPT-3 使用 lr=6e-4,warmup 覆盖3.75亿代币──这些不是随意的选择──它们是花费数百万美元进行大量超参数搜索的结果──

Bạn cần phải hiểu lịch trình vì các mặc định sẽ không làm việc cho vấn đề của bạn. Khi bạn điều chỉnh một mô hình được đào tạo trước, lịch trình đúng là khác với đào tạo từ đầu. Khi bạn tăng kích thước lô, thời gian ấm lên cần phải thay đổi. Khi đào tạo nghỉ ở bước 10.000, bạn cần biết liệu đó là một vấn đề lịch trình hay gì khác.

> Bạn cần hiểu quy trình điều chỉnh, vì giá trị mặc định không phù hợp với vấn đề của bạn. Khi bạn điều chỉnh mô hình huấn luyện trước, điều chỉnh chính xác khác với từ đầu. Khi bạn tăng lượng lớn, thời gian nóng lên cần phải thay đổi. Khi tập luyện trong 10,000 bước sụp đổ, bạn cần biết liệu đó là vấn đề điều chỉnh hay các vấn đề khác.

> **【中文解读】**Tỷ lệ học tập quá cao →  tập phát triển(kết đến vô hạn); quá thấp →  tập rất chậm; thích hợp nhưng không suy giảm → 振荡 ở gần giá trị tối thiểu.

> **【拓展：大模型的学习率配置】**Llama 3 405B: đỉnh lr=3e-4, nóng lên=2000 步, phân rã cosine đến 3e-5, 训练 1.8T token。GPT-3 175B: đỉnh lr=6e-4, nóng lên=375M token。BERT-base: đỉnh lr=1e-4, nóng lên=10K 步, phân rã tuyến tính。规律:模型越大,学习率通常越小;预训比微调的学习率高10-100倍。

## Khái niệm cốt lõi

### Tốc độ học tập liên tục

Cách đơn giản nhất là chọn một con số, sử dụng nó cho từng bước.

> Cách đơn giản nhất là chọn một con số, mỗi bước đều dùng nó.

```
lr(t) = lr_0
```

Nó hiếm khi tối ưu. Nó hoặc quá cao cho cuối tập luyện (sự dao động xung quanh mức tối thiểu) hoặc quá thấp cho sự bắt đầu (sự tính toán lãng phí trên các bước nhỏ).

> 很少是最优的──要么 đối với thời gian cuối tập luyện quá cao (((在极小值附近振荡),要么 đối với thời gian đầu tập luyện quá thấp (((微小步长浪费计算) ──适用于小模型和调试── đối với nhiệm vụ tập luyện trên một giờ là lựa chọn tồi tệ──

### - Đường xuống xuống.

Cách thức cũ từ thời đại ResNet: Giảm tốc độ học tập bằng một nhân tố (thường là 10 lần) ở thời kỳ cố định.

> ResNet 时代的老派方法──在固定的时代将学习率降低一个因子 (通常是10倍)──

```
lr(t) = lr_0 * gamma^(floor(epoch / step_size))
```

Ở đó gamma = 0,1 và step_size = 30, nghĩa là: lr giảm 10x mỗi 30 thời kỳ. ResNet-50 sử dụng điều này -- lr = 0,1, giảm 10x ở thời kỳ 30, 60, và 90.

> gamma = 0.1 và step_size = 30 nghĩa là: mỗi 30 thời đại tỷ lệ học giảm 10 lần. ResNet-50 sử dụng lr=0.1, trong thời đại 30、60 và 90 từng giảm 10 lần.

Vấn đề: điểm suy giảm tối ưu phụ thuộc vào bộ dữ liệu và kiến trúc. Hãy chuyển sang một vấn đề khác và bạn cần phải điều chỉnh lại khi nào để giảm.

> 问题: 优衰减点取决于数据集和架构. 换一个问题就需要重新调整何时降低. 转过是突然的学习率突然变化时损失可能升.

### Cosine Annealing 余弦退火

Sự suy giảm trơn tru từ tốc độ học tập tối đa xuống tối thiểu, theo đường cong cosine:

> Từ tỷ lệ học tập lớn nhất đến tỷ lệ học tập tối thiểu giảm dần, theo đường dẫn của các đường dẫn:

```
lr(t) = lr_min + 0.5 * (lr_max - lr_min) * (1 + cos(pi * t / T))
```

Ở đó t là bước hiện tại và T là tổng số bước.

> Trong đó t là số bước hiện tại, T là số bước toàn bộ.

Tại t=0, thuật ngữ cosine là 1, vì vậy lr = lr_max. Tại t=T, thuật ngữ cosine là -1, vì vậy lr = lr_min. Sự phân rã là nhẹ nhàng lúc đầu, tăng tốc ở giữa, và trở nên nhẹ nhàng lại gần cuối.

> t=0 时,余弦项为1,所以 lr = lr_max──t=T 时,余弦项为 -1,所以 lr = lr_min──衰减开始平缓,中间加速,末期又变平缓──

Đây là mặc định cho hầu hết các khóa đào tạo hiện đại. Không có các siêu tham số để điều chỉnh vượt quá lr_max và lr_min. Hình dạng cosine phù hợp với quan sát thực nghiệm rằng hầu hết các học tập xảy ra giữa đào tạo - bạn muốn kích thước bước hợp lý trong thời gian quan trọng đó.

> Đây là lựa chọn mặc định của hầu hết các hoạt động đào tạo hiện đại. Ngoài lr_max và lr_min, không cần phải điều chỉnh siêu số lượng.

### Warmup: Tại sao bạn bắt đầu nhỏ hơn

Adam và các trình tối ưu hóa thích ứng khác duy trì ước tính chạy của trung bình và biến thể gradient. Ở bước 0, những ước tính này được khởi tạo thành không.

> Adam và các máy tự thích ứng khác Ưu điểm hoạt động của trung bình và tỷ lệ khác nhau. Trong bước 0, những ước tính này được khởi tạo thành 0.

Warmup sửa chữa điều này. Bắt đầu với một tốc độ học tập nhỏ (thường là lr_max / warmup_steps hoặc thậm chí là không) và tăng lên lr_max theo đường thẳng qua các bước N đầu tiên.

> Warmup đã sửa chữa vấn đề này. Từ một tỷ lệ học rất nhỏ bắt đầu (thường là lr_max / warmup_steps thậm chí là zero), sau đó tăng lên lr_max ở giai đoạn trước.

```
lr(t) = lr_max * (t / warmup_steps)     for t < warmup_steps
```

LMA 3 được đào tạo với khoảng 1,8 nghìn tỷ token và được nóng lên cho 2000 bước. GPT-3 đã nóng lên hơn 375 triệu token.

> **【拓展：Warmup 的数学解释】**Sự cố định độ phân biệt của Adam (m_hat = m_t / (1-beta1^t)) trong vài bước trước là thiếu hụt bù đắp. Ví dụ, m_1 của m_1 = 0,1*gradient, trừ (1-0.9) = 0,1 được ước tính độ chính xác.

### Sự nóng lên tuyến tính + sự suy giảm vũ trụ .

Đường mặc định hiện đại. tăng lên tuyến tính, sau đó phân hủy với cosine:

```
if t < warmup_steps:
    lr(t) = lr_max * (t / warmup_steps)
else:
    progress = (t - warmup_steps) / (total_steps - warmup_steps)
    lr(t) = lr_min + 0.5 * (lr_max - lr_min) * (1 + cos(pi * progress))
```

Đây là những gì Llama, GPT, PaLM và hầu hết các biến đổi hiện đại sử dụng. Sự nóng lên ngăn ngừa sự bất ổn sớm. Sự phân hủy cosine đặt mô hình vào mức tối thiểu tốt.

> Đây là Llama、GPT、PaLM 和大多数现代变压器 使用的方法──warmup 防止早期不稳定──余弦衰减使模型稳定到一个好的极小值──

### Chính sách 1 vòng

Phát hiện của Leslie Smith (2018): tăng tốc độ học tập từ giá trị thấp lên giá trị cao trong nửa đầu đào tạo, sau đó tăng nó lại trong nửa sau.

> Phát hiện của Leslie Smith (2018): Trong nửa đầu tập luyện tỷ lệ học tập sẽ tăng từ giá trị thấp lên giá trị cao, nửa cuối sẽ giảm lại.

Lý thuyết: tốc độ học tập cao hoạt động như một sự điều chỉnh bằng cách thêm tiếng ồn vào quỹ đạo tối ưu hóa. Mô hình khám phá nhiều hơn về cảnh quan mất mát trong giai đoạn tăng lên, tìm thấy bể bể tốt hơn.

> 理论: tỷ lệ học cao thông qua việc tăng cường đường mòn tăng tiếng ồn lên đến hiệu quả hóa tác dụng.

```
Phase 1 (0 to T/2):    lr ramps from lr_max/25 to lr_max
Phase 2 (T/2 to T):    lr ramps from lr_max to lr_max/10000
```

1cycle thường chạy nhanh hơn coisinetching cho một ngân sách tính toán cố định.

> 1 vòng trong ngân sách tính toán cố định thường nhanh hơn so với tập luyện quay lại.

> **【拓展：微调时的学习率策略】**微调预训练模型(如BERT、Llama)时,学习率通常比预训小 10-100倍。LoRA 微调 Llama:lr=2e-5~1e-4,warmup=总步数的3%,cosine decay。关键技巧: đối với các tầng khác nhau sử dụng tỷ lệ học khác nhau底层(接近输入) với lr nhỏ hơn(因为 chung đặc điểm đã học tốt),顶层(接近输出) sử dụng lr lớn hơn vì cần thích ứng với nhiệm vụ mới)。PyTorch 通过参数组实现。

### Chế độ hình dạng đối với hình dạng

```mermaid
graph LR
    subgraph "Constant"
        C1["lr"] --- C2["lr"] --- C3["lr"]
    end

    subgraph "Step Decay"
        S1["0.1"] --- S2["0.1"] --- S3["0.01"] --- S4["0.001"]
    end

    subgraph "Cosine Annealing"
        CS1["lr_max"] --> CS2["gradual"] --> CS3["steep"] --> CS4["lr_min"]
    end

    subgraph "Warmup + Cosine"
        WC1["0"] --> WC2["lr_max"] --> WC3["cosine"] --> WC4["lr_min"]
    end
```

### Chữ liệu định hình

```mermaid
flowchart TD
    Start["Choosing a LR schedule"] --> Know{"Know total<br/>training steps?"}

    Know -->|"Yes"| Budget{"Compute budget?"}
    Know -->|"No"| Constant["Use constant LR<br/>with manual decay"]

    Budget -->|"Large (days/weeks)"| WarmCos["Warmup + Cosine Decay<br/>(Llama/GPT default)"]
    Budget -->|"Small (hours)"| OneCycle["1cycle Policy<br/>(fastest convergence)"]
    Budget -->|"Moderate"| Cosine["Cosine Annealing<br/>(safe default)"]

    WarmCos --> Warmup["Warmup = 1-5% of steps"]
    OneCycle --> FindLR["Find lr_max with LR range test"]
    Cosine --> MinLR["Set lr_min = lr_max / 10"]
```

### Số thực từ các mô hình được xuất bản  Các tham số thực tế của mô hình đã được xuất bản

```mermaid
graph TD
    subgraph "Published LR Configs"
        L3["Llama 3 (405B)<br/>Peak: 3e-4<br/>Warmup: 2000 steps<br/>Schedule: Cosine to 3e-5"]
        G3["GPT-3 (175B)<br/>Peak: 6e-4<br/>Warmup: 375M tokens<br/>Schedule: Cosine to 0"]
        R50["ResNet-50<br/>Peak: 0.1<br/>Warmup: none<br/>Schedule: Step decay x0.1 at 30,60,90"]
        B["BERT (340M)<br/>Peak: 1e-4<br/>Warmup: 10K steps<br/>Schedule: Linear decay"]
    end
```

## Hãy xây dựng nó.
```figure
lr-schedule
```

## Hãy xây dựng nó

> **【中文解读】**Sau đây là cách thực hiện từ zero 5 phương pháp điều chỉnh, sau đó sử dụng cùng một vòng tròn dữ liệu tập tập huấn mạng để so sánh hiệu quả.

### Bước 1: Định trình chức năng Bước 1: Định trình chức năng

Mỗi hàm thực hiện bước hiện tại và trả lại tốc độ học tập ở bước đó.

> Mỗi hàm nhận được số bước trước, trở lại tỷ lệ học của bước này.

```python
import math


def constant_schedule(step, lr=0.01, **kwargs):
    return lr


def step_decay_schedule(step, lr=0.1, step_size=100, gamma=0.1, **kwargs):
    return lr * (gamma ** (step // step_size))


def cosine_schedule(step, lr=0.01, total_steps=1000, lr_min=1e-5, **kwargs):
    if step >= total_steps:
        return lr_min
    return lr_min + 0.5 * (lr - lr_min) * (1 + math.cos(math.pi * step / total_steps))


def warmup_cosine_schedule(step, lr=0.01, total_steps=1000, warmup_steps=100, lr_min=1e-5, **kwargs):
    if total_steps <= warmup_steps:
        return lr * (step / max(warmup_steps, 1))
    if step < warmup_steps:
        return lr * step / warmup_steps
    progress = (step - warmup_steps) / (total_steps - warmup_steps)
    return lr_min + 0.5 * (lr - lr_min) * (1 + math.cos(math.pi * progress))


def one_cycle_schedule(step, lr=0.01, total_steps=1000, **kwargs):
    mid = max(total_steps // 2, 1)
    if step < mid:
        return (lr / 25) + (lr - lr / 25) * step / mid
    else:
        progress = (step - mid) / max(total_steps - mid, 1)
        return lr * (1 - progress) + (lr / 10000) * progress
```

### Bước 2: Hình ảnh tất cả các lịch trình. Bước 2: Hình ảnh tất cả các điều chỉnh.

In một biểu đồ dựa trên văn bản cho thấy mỗi lịch trình phát triển theo cách đào tạo.

> 印文图表, hiển thị mỗi thứ điều chỉnh trong quá trình đào tạo

```python
def visualize_schedule(name, schedule_fn, total_steps=500, **kwargs):
    steps = list(range(0, total_steps, total_steps // 20))
    if total_steps - 1 not in steps:
        steps.append(total_steps - 1)

    lrs = [schedule_fn(s, total_steps=total_steps, **kwargs) for s in steps]
    max_lr = max(lrs) if max(lrs) > 0 else 1.0

    print(f"\n{name}:")
    for s, lr_val in zip(steps, lrs):
        bar_len = int(lr_val / max_lr * 40)
        bar = "#" * bar_len
        print(f"  Step {s:4d}: lr={lr_val:.6f} {bar}")
```

### Bước 3: Mạng lưới đào tạo.

Một mạng lưới hai tầng đơn giản trên bộ dữ liệu vòng tròn, giống như các bài học trước đây, nhưng bây giờ chúng tôi thay đổi lịch trình.

> Trong tập dữ liệu hình tròn, mạng đơn giản hai tầng, giống như các bài học trước, nhưng bây giờ chúng ta thay đổi các chương trình điều chỉnh.

```python
import random


def sigmoid(x):
    x = max(-500, min(500, x))
    return 1.0 / (1.0 + math.exp(-x))


def relu(x):
    return max(0.0, x)


def relu_deriv(x):
    return 1.0 if x > 0 else 0.0


def make_circle_data(n=200, seed=42):
    random.seed(seed)
    data = []
    for _ in range(n):
        x = random.uniform(-2, 2)
        y = random.uniform(-2, 2)
        label = 1.0 if x * x + y * y < 1.5 else 0.0
        data.append(([x, y], label))
    return data


def train_with_schedule(schedule_fn, schedule_name, data, epochs=300, base_lr=0.05, **kwargs):
    random.seed(0)
    hidden_size = 8
    total_steps = epochs * len(data)

    std = math.sqrt(2.0 / 2)
    w1 = [[random.gauss(0, std) for _ in range(2)] for _ in range(hidden_size)]
    b1 = [0.0] * hidden_size
    w2 = [random.gauss(0, std) for _ in range(hidden_size)]
    b2 = 0.0

    step = 0
    epoch_losses = []

    for epoch in range(epochs):
        total_loss = 0
        correct = 0

        for x, target in data:
            lr = schedule_fn(step, lr=base_lr, total_steps=total_steps, **kwargs)

            z1 = []
            h = []
            for i in range(hidden_size):
                z = w1[i][0] * x[0] + w1[i][1] * x[1] + b1[i]
                z1.append(z)
                h.append(relu(z))

            z2 = sum(w2[i] * h[i] for i in range(hidden_size)) + b2
            out = sigmoid(z2)

            error = out - target
            d_out = error * out * (1 - out)

            for i in range(hidden_size):
                d_h = d_out * w2[i] * relu_deriv(z1[i])
                w2[i] -= lr * d_out * h[i]
                for j in range(2):
                    w1[i][j] -= lr * d_h * x[j]
                b1[i] -= lr * d_h
            b2 -= lr * d_out

            total_loss += (out - target) ** 2
            if (out >= 0.5) == (target >= 0.5):
                correct += 1
            step += 1

        avg_loss = total_loss / len(data)
        accuracy = correct / len(data) * 100
        epoch_losses.append(avg_loss)

    return epoch_losses
```

### Bước 4: So sánh tất cả các lịch trình.

Tập luyện cùng một mạng với mỗi lịch trình và so sánh hành vi mất mát cuối cùng và hội tụ.

> Sử dụng mỗi bài tập điều chỉnh cùng một mạng, so sánh hành vi mất mát và nhận được cuối cùng.

```python
def compare_schedules(data):
    configs = [
        ("Constant", constant_schedule, {}),
        ("Step Decay", step_decay_schedule, {"step_size": 15000, "gamma": 0.1}),
        ("Cosine", cosine_schedule, {"lr_min": 1e-5}),
        ("Warmup+Cosine", warmup_cosine_schedule, {"warmup_steps": 3000, "lr_min": 1e-5}),
        ("1cycle", one_cycle_schedule, {}),
    ]

    print(f"\n{'Schedule':<20} {'Start Loss':>12} {'Mid Loss':>12} {'End Loss':>12} {'Best Loss':>12}")
    print("-" * 70)

    for name, schedule_fn, extra_kwargs in configs:
        losses = train_with_schedule(schedule_fn, name, data, epochs=300, base_lr=0.05, **extra_kwargs)
        mid_idx = len(losses) // 2
        best = min(losses)
        print(f"{name:<20} {losses[0]:>12.6f} {losses[mid_idx]:>12.6f} {losses[-1]:>12.6f} {best:>12.6f}")
```

### Bước 5: LR quá cao vs quá thấp.

Hiển thị ba chế độ thất bại: quá cao (sự phân lập), quá thấp (crawling), và chỉ đúng.

> 展示三种失败模式: quá cao (发散) 、 quá thấp (爬行) 、刚好。

```python
def lr_sensitivity(data):
    learning_rates = [1.0, 0.1, 0.01, 0.001, 0.0001]

    print("\nLR Sensitivity (constant schedule, 100 epochs):")
    print(f"  {'LR':>10} {'Start Loss':>12} {'End Loss':>12} {'Status':>15}")
    print("  " + "-" * 52)

    for lr in learning_rates:
        losses = train_with_schedule(constant_schedule, f"lr={lr}", data, epochs=100, base_lr=lr)
        start = losses[0]
        end = losses[-1]

        if end > start or math.isnan(end) or end > 1.0:
            status = "DIVERGED"
        elif end > start * 0.9:
            status = "BARELY MOVED"
        elif end < 0.15:
            status = "CONVERGED"
        else:
            status = "LEARNING"

        end_str = f"{end:.6f}" if not math.isnan(end) else "NaN"
        print(f"  {lr:>10.4f} {start:>12.6f} {end_str:>12} {status:>15}")
```

## Hãy sử dụng nó để thực hiện

> **【中文解读】**PyTorch  cung cấp 15+ loại điều chỉnh. Các thiết bị thường xuyên nhất là CosineAnnealingLR 和 HuggingFace của get_cosine_schedule_with_warmup.

PyTorch cung cấp các lập trình viên trong `torch.optim.lr_scheduler`- Có thể là:

```python
import torch
import torch.optim as optim
from torch.optim.lr_scheduler import CosineAnnealingLR, OneCycleLR, StepLR

model = nn.Sequential(nn.Linear(10, 64), nn.ReLU(), nn.Linear(64, 1))
optimizer = optim.Adam(model.parameters(), lr=3e-4)

scheduler = CosineAnnealingLR(optimizer, T_max=1000, eta_min=1e-5)

for step in range(1000):
    loss = train_step(model, optimizer)
    scheduler.step()
```

Đối với warmup + cosine, sử dụng một lập trình lambda hoặc `get_cosine_schedule_with_warmup`từ HuggingFace:

> Đối với sự ấm áp + 余弦, sử dụng lambda 调度器 hoặc HuggingFace của `get_cosine_schedule_with_warmup`- Có thể là:

```python
from transformers import get_cosine_schedule_with_warmup

scheduler = get_cosine_schedule_with_warmup(
    optimizer,
    num_warmup_steps=2000,
    num_training_steps=100000,
)
```

Chức năng HuggingFace là điều mà hầu hết các kịch bản chỉnh sửa tinh tế Llama và GPT sử dụng. Khi nghi ngờ, sử dụng warmup + cosine với warmup = 3-5% tổng bước. Nó hoạt động cho hầu hết mọi thứ.

> Hỗng mặt của hàm là hầu hết các Llama và GPT 微调脚本使用的──不确定时,使用热up + 余弦,热up 为总步数的 3-5%──它几乎适用于所有场景──

## Chuyển nó đi.

Bài học này mang lại:
- `outputs/prompt-lr-schedule-advisor.md`-- một lời nhắc đề nghị đúng lịch trình học tập và các siêu tham số cho thiết lập đào tạo của bạn

> 本课产 出:`outputs/prompt-lr-schedule-advisor.md`- một lời khuyên về tỷ lệ học tập chính xác và các siêu số

## Tập luyện bài tập

1. Thực hiện phân rã theo hàm số: lr(t) = lr_0 * gamma^t nơi gamma = 0,999. So sánh với cosine annealing trên bộ dữ liệu vòng tròn.

   1. 实现指数衰减:lr(t) = lr_0 * gamma^t, gamma = 0,999──在圆形数据集上和余弦退火对比──

2. Thực hiện thử nghiệm phạm vi tốc độ học tập (Leslie Smith): tập luyện vài trăm bước trong khi tăng theo tỉ lệ tăng từ 1e-7 đến 1.

   2. 实现学习率范围测试(Leslie Smith): tập vài trăm bước, đồng thời tăng LR từ 1e-7 chỉ số lên 1── vẽ mất mát so với LR 曲线──最优最大 LR 是 mất mát 开始上升前的值──

3. Tập luyện với warmup + cosine nhưng thay đổi thời gian làm nóng: 0%, 1%, 5%, 10%, 20% tổng bước. Tìm điểm ngọt ngào nơi tập luyện ổn định nhất.

   3. Sử dụng  弦训练, nhưng biến đổi  长度:总步数的0%、1%、5%、10%、20%── tìm được điểm tốt nhất nhất của tập luyện

4. Thực hiện cosine annealing với khởi động lại ấm (SGDR): thiết lập lại tốc độ học tập để lr_max mỗi bước T và phân rã một lần nữa. So sánh với cosine tiêu chuẩn trong một cuộc tập luyện dài hơn.

   4. 实现带热重启的余弦退火(SGDR): mỗi bước 把学习率重置为 lr_max 并再次衰减──在更长的训练上和标准余弦对比──

5. Xây dựng một "chúng phẫu thuật lịch trình" theo dõi mất tập luyện và tự động chuyển từ ấm lên cosine khi mất ổn định, và giảm lr nếu mất cao nguyên quá lâu.

   5. 构建调度医生: giám sát tập luyện mất, mất 稳定时自动 từ sưởi ấm  chuyển sang dây dư, mất 停滞太久时降低 lr。

## Từ khóa  Từ khóa nhanh chóng

| Term | What people say | What it actually means |
|------|----------------|----------------------|
| Learning rate | "How fast the model learns" | The scalar that multiplies the gradient to determine the parameter update size |
| Schedule | "Change the LR over time" | A function that maps training step to learning rate, designed to optimize convergence |
| Warmup | "Start with a small LR" | Linearly ramping the LR from near-zero to the target value over the first N steps to stabilize optimizer statistics |
| Cosine annealing | "Smooth LR decay" | Decreasing the LR following a cosine curve from lr_max to lr_min over training |
| Step decay | "Drop LR at milestones" | Multiplying the LR by a factor (usually 0.1) at fixed epoch intervals |
| 1cycle policy | "Up then down" | Leslie Smith's method of ramping LR up then down in a single cycle for faster convergence |
| LR range test | "Find the best learning rate" | Training briefly while increasing LR to find the value where loss starts diverging |
| Cosine with warm restarts | "Reset and repeat" | Periodically resetting the LR to lr_max and decaying again (SGDR) |
| Eta min | "The floor for the LR" | The minimum learning rate that the schedule decays to |
| Peak learning rate | "The maximum LR" | The highest LR reached during training, typically after warmup |

| 术语 | 俗称 | 实际含义 |
|------|------|---------|
| Learning rate / 学习率 | "模型学得多快" | 乘以梯度决定参数更新大小的标量 |
| Schedule / 调度 | "随时间变 LR" | 把训练步数映射到学习率的函数，旨在优化收敛 |
| Warmup / 预热 | "从小 LR 开始" | 在前 N 步把 LR 从近零线性升到目标值，稳定优化器统计 |
| Cosine annealing / 余弦退火 | "平滑 LR 衰减" | 训练中按余弦曲线从 lr_max 降到 lr_min |
| Step decay / 阶梯衰减 | "里程碑式降 LR" | 在固定 epoch 间隔把 LR 乘以一个因子（通常 0.1） |
| 1cycle policy / 1cycle 策略 | "先升后降" | Leslie Smith 的方法：单周期内先升 LR 后降，加速收敛 |
| LR range test / LR 范围测试 | "找最佳学习率" | 短训练中增加 LR，找到 loss 开始发散的点 |
| Cosine with warm restarts / 带热重启的余弦 | "重置并重复" | 周期性把 LR 重置为 lr_max 再次衰减（SGDR） |
| Eta min / 最小学习率 | "LR 的下限" | 调度衰减到的最小学习率 |
| Peak learning rate / 峰值学习率 | "最大 LR" | 训练期间达到的最高 LR，通常在 warmup 之后 |

## Xem thêm 延伸阅读

- Loshchilov & Hutter, "SGDR: Stochastic Gradient Descent with Warm Restarts" (2017) -- giới thiệu cosine annealing và warm restarts
  Loshchilov & Hutter,SGDR:带热重启的随机梯度下降(2017)引入余弦退火和热重启
- Smith, "Super-Convergence: Trình đào tạo rất nhanh của mạng thần kinh sử dụng tỷ lệ học tập lớn" (2018) -- bài báo chính sách 1 vòng
  Smith,超收: sử dụng tỷ lệ học đại học 快速训练神经网络(2018)1cycle 策略论文
- Touvron et al., "Llama 2: Open Foundation and Fine-Tuned Chat Models" (2023) -- ghi lại lịch trình ấm lên + cosine được sử dụng ở quy mô
  Touvron 等人,Llama 2: Opening Basis和微调聊天模型(2023) ghi lại việc sử dụng rộng rãi sự nóng lên + 余弦调度
- Goyal et al., "Sự chính xác, Sản lượng nhỏ lớn SGD: đào tạo ImageNet trong 1 giờ" (2017) -- quy tắc quy mô tuyến tính và nóng lên cho đào tạo hàng lớn
  Goyal 等人,精确 大批量 SGD:1 小时训练 ImageNet(2017) 线性缩放规则和大批量训练的热升
