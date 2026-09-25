# Thường độ số lượng ư

> Điểm nổi là một sự trừu tượng bị rò rỉ. Nó sẽ cắn bạn trong khi tập luyện, và bạn sẽ không thấy nó đến.
> 浮点数 là một phép thuật của sự thoát nước. Nó sẽ cắn bạn trong buổi tập, nhưng bạn sẽ không thấy nó đến.

**Type:** Build | **类型:** 动手
**Language:**Python**语言:**Python
**Prerequisites:** Phase 1, Lessons 01-04 | **前置知识:** Phase 1, Lessons 01-04
**Time:** ~120 minutes | **时间:** ~120 分钟

## Mục tiêu học tập

- Thực hiện softmax ổn định về số và log-sum-exp bằng cách sử dụng thủ thuật trừ tối đa
  Sử dụng các kỹ thuật giảm giá trị tối đa để đạt được giá trị số ổn định Softmax và log-sum-exp
- Xác định quá tải, quá tải thấp và hủy bỏ thảm họa trong các tính toán điểm nổi
  识别浮点计算中的溢溢,下溢和灾难性抵消
- Kiểm tra gradient phân tích so với gradient số bằng cách sử dụng sự khác biệt hữu hạn trung tâm
  用中心有限差分验证解析梯度
- Giải thích tại sao bfloat16 được ưu tiên so với float16 để đào tạo và cách quy mô lỗ ngăn ngừa dòng chảy thấp gradient
  解释 tại sao bfloat16 hơn float16 thích hợp hơn để tập luyện, cũng như làm thế nào để ngăn ngừa sự giảm bớt

> **【中文解读】**
> 浮点数 là sự trừu tượng của漏水──训练 3 小时后损失 变 NaN là sự sụp đổ phổ biến nhất──本章: 实现数值稳定的软max(减最大值技巧), giải thích tại sao bfloat16 so với float16 更适合训练──混合精度训练中使用损失扩展 防止小梯度下溢──

## Vấn đề  vấn đề giới thiệu

> **【中文解读】**三种典型数值稳定性灾难:(1) 训练 3 小时后损失变化 NaN某步计算溢出;(2) 精度比论文差2%float16的累积舍入差吃掉准确率;(3) tự viết交叉大逻辑时返回infsoftmax 溢出──这些都是浮点数的"漏水抽象",每个种都有标准修复技巧──

Bạn thêm một tuyên bố in. các logit là tốt ở bước 9.000. ở bước 9.001 họ là.`inf`Theo bước 9.002 mỗi độ nghiêng là`nan`và huấn luyện đã chết.
> Bạn đã thêm một bài báo. Các log trong 9.000 bước trở lại bình thường. 9.001 bước trở thành bình thường.`inf`✿ Đến 9,002 bước tất cả các bước đều là ✿`nan`, tập luyện đã chết.

Hoặc: mô hình của bạn đi đến hoàn thành nhưng độ chính xác là 2% tệ hơn các tuyên bố trên giấy. Bạn kiểm tra mọi thứ. Kiến trúc phù hợp. Hiperparameter phù hợp. Dữ liệu phù hợp. Vấn đề là giấy sử dụng float32 và bạn sử dụng float16 mà không có quy mô đúng. 32 bit tích lũy sai lầm tròn lặng lẽ ăn sự chính xác của bạn.
> Hoặc: mô hình đào tạo hoàn thành nhưng độ chính xác so với bài luận là 2%── bạn đã kiểm tra mọi thứ── cấu trúc phù hợp, siêu số liệu phù hợp, dữ liệu phù hợp── vấn đề là bài luận đã sử dụng float32, bạn đã sử dụng float16 nhưng không có sự缩放 chính xác──

Hoặc: bạn thực hiện mất tích entropy chéo từ đầu. Nó hoạt động trên logits nhỏ. Khi logits vượt quá 100, nó trở lại`inf`- Tối cao mềm chảy quá vì`exp(100)`là lớn hơn float32 có thể đại diện. mỗi framework ML xử lý điều này với một trò chơi hai dòng.
> Hoặc: bạn từ đầu thực hiện giao thông 损失 ⋅小 logits 时正常 ⋅当 logits 超过100 时返回 ⋅`inf`✿softmax 溢出了, vì ✿`exp(100)`超过了 float32 的表示范围.

Sự ổn định số không phải là một mối quan tâm lý thuyết. Nó là sự khác biệt giữa một cuộc tập luyện thành công và một cuộc tập luyện thất bại lặng lẽ.
> Định vị số không phải là vấn đề lý thuyết. Nó là sự khác biệt giữa đào tạo thành công và thất bại tĩnh lặng.

## Khái niệm cốt lõi

> **【拓展：Softmax 的数值稳定技巧是面试必考题】**原始 Softmax:`softmax(x) = exp(x) / sum(exp(x))`, khi x trong có giá trị lớn khi exp 溢出――解法: giảm giá trị tối đa `softmax(x) = exp(x - max(x)) / sum(exp(x - max(x)))`Kết quả toán học không thay đổi nhưng số lượng ổn định.`F.cross_entropy`内部 sử dụng log-softmax 而非分开计算, đó là lý do.

### IEEE 754: Làm thế nào máy tính lưu trữ số thực

Máy tính lưu trữ số thực như các giá trị điểm nổi theo tiêu chuẩn IEEE 754. Một float có ba phần: một bit dấu hiệu, một biểu tượng và một mantissa (sự quan trọng).
> 计算机 theo tiêu chuẩn IEEE 754 sẽ lưu trữ số thực cho giá trị浮点──浮点数 có ba phần:符号位、指数和尾数──

```
Float32 layout (32 bits total):
[1 sign] [8 exponent] [23 mantissa]

Value = (-1)^sign * 2^(exponent - 127) * 1.mantissa
```

Mantissa xác định độ chính xác (càng số đáng kể).
> 尾数决定精度 ((多少有效数字), chỉ số quyết định phạm vi ((数字可以多大或多小) 👇

```
Format     Bits   Exponent  Mantissa  Decimal digits  Range (approx)
float64    64     11        52        ~15-16          +/- 1.8e308
float32    32     8         23        ~7-8            +/- 3.4e38
float16    16     5         10        ~3-4            +/- 65,504
bfloat16   16     8         7         ~2-3            +/- 3.4e38
```

float32 cho bạn khoảng 7 chữ số thập phân độ chính xác. float16 cho bạn khoảng 3 chữ số. bfloat16 là câu trả lời của Google cho vấn đề phạm vi của float16 -- cùng một số lượng 8 bit như float32 nhưng chỉ 7 bit mantissa.
> float32 给你约7位十进制精度──float16 约3位──bfloat16 là câu trả lời của Google cho câu hỏi về float16 范围 tương tự như float32 chỉ số 8位 nhưng chỉ có 7位尾数── đào tạo phạm vi của mạng lưới thần kinh khi quan trọng hơn độ chính xác, vì vậy bfloat16 thường tốt hơn──

### Tại sao 0.1 + 0.2 != 0.3 ? Tại sao 0.1 + 0.2 != 0.3 ?

Số 0.1 không thể được đại diện chính xác trong điểm nổi nhị phân. Ở cơ sở 2, nó là một phần nhỏ lặp lại. Float32 cắt giảm điều này thành 23 bit mantissa.
> 0.1 Trong các điểm trôi nổi thứ hai không thể xác định được.

```
In Python:
>>> 0.1 + 0.2
0.30000000000000004

>>> 0.1 + 0.2 == 0.3
False
```

Điều này quan trọng đối với ML bởi vì: (1) So sánh thua lỗ như `if loss < threshold`có thể đưa ra những câu trả lời sai. (2) Việc tích lũy nhiều giá trị nhỏ bị trôi qua từ tổng thật. (3) Các tổng kiểm tra và các bài kiểm tra tái tạo thất bại nếu bạn so sánh các floats với `==`- Phong cách: đừng bao giờ so sánh con tàu nổi với `==`- Sử dụng`abs(a - b) < epsilon`hoặc `math.isclose()`- Tôi không biết.
> Đây đối với ML rất quan trọng: 1) 损失比较可能出错.`==`So sánh điểm trên số điểm của các bài kiểm tra và thử nghiệm sẽ thất bại.`==`So với số điểm trên.

### Sự hủy bỏ thảm họa 灾难性抵消

Khi bạn trừ hai số điểm nổi gần như bằng nhau, các con số quan trọng bị hủy bỏ và bạn còn lại với tiếng ồn tròn được nâng lên các con số hàng đầu.
> Khi bạn giảm hai điểm tăng gần nhau, số hiệu quả giảm, tiếng ồn được nâng lên số dẫn trước.

```
a = 1.0000001    (stored as 1.00000011920929 in float32)
b = 1.0000000    (stored as 1.00000000000000 in float32)

True difference:  0.0000001
Computed:         0.00000011920929

Relative error: 19.2%
```

Giải pháp: sắp xếp lại công thức để tránh trừ số lớn, gần như bằng nhau. Để thay đổi, sử dụng thuật toán Welford hoặc trung tâm dữ liệu trước.
> 修复: tái xếp hạng công thức để tránh giảm số lượng lớn gần giống nhau.

### Tăng và giảm dòng chảy

Overflow xảy ra khi kết quả quá lớn để đại diện. Underflow xảy ra khi nó quá nhỏ.
> 溢出是结果太大不能表示,下溢是结果太小.

```
Float32 boundaries:
  Maximum:  3.4028235e+38
  Overflow:  anything > 3.4e38 becomes inf
  Underflow: anything < 1.4e-45 becomes 0.0

exp(88.7)  = 3.40e+38   (barely fits in float32)
exp(89.0)  = inf         (overflow)
```

Trong ML, `exp()`xuất hiện trong các tính toán softmax, sigmoid và xác suất. `log()`xuất hiện trong sự tương ứng chéo, khả năng log và sự khác biệt KL.
> Trong ML,`exp()`Hiện tại, tính toán mềmmax,sigmoid và tỷ lệ dự đoán`log()`Hiện tại giao giao ≠ đối với số giống như và KL 散度中.

### Trận thuật Log-Sum-Exp 技巧 Log-Sum-Exp

Máy tính `log(sum(exp(x_i)))`Trù: trừ giá trị tối đa trước khi tăng số.
> trực tiếp tính toán`log(sum(exp(x_i)))`Số giá trị nguy hiểm: giảm giá trị tối đa trước khi chỉ số hóa.

```
log(sum(exp(x_i))) = max(x) + log(sum(exp(x_i - max(x))))
```

Tại sao điều này hoạt động: sau khi trừ `max(x)`, số nhân lớn nhất là `exp(0) = 1`Không có quá tải là có thể. ít nhất một thuật ngữ trong tổng là 1, vì vậy tổng là ít nhất là 1, và`log(1) = 0`Không có dòng chảy xuống `-inf`có thể.
> Tại sao hiệu quả: giảm đi`max(x)`后, 最大指数 là `exp(0) = 1` không thể tràn ra ít nhất 1 vì vậy và ít nhất là 1,`log(1) = 0`Không thể xuống được.`-inf`

Trù này xuất hiện ở khắp mọi nơi trong ML: bình thường hóa softmax, mất entropi chéo, tổng hợp xác suất log, hỗn hợp Gaussians, suy luận biến.
> Kỹ thuật này không tồn tại trong ML:softmax 归化、交叉损失、对数概率求和、高斯混合、变分推断──

### Tại sao Softmax cần thủ thuật trừu tượng Max ?

Nếu không có thủ thuật, logit của [100, 101, 102] gây ra quá tải.
> Không có kỹ năng, thời gian, logits [100, 101, 102]  dẫn đến tràn đi.

```
exp(100 - 102) = exp(-2) = 0.135
exp(101 - 102) = exp(-1) = 0.368
exp(102 - 102) = exp(0)  = 1.000
sum = 1.503

softmax = [0.090, 0.245, 0.665]
```

Những xác suất giống nhau, tính toán là an toàn, đây không phải là một tối ưu hóa, đó là yêu cầu cho sự chính xác.
> 概率 hoàn toàn giống nhau. 計算安全.

### NaN và Inf: Khám phá và phòng ngừa

`nan`và `inf`truyền nhiễm qua tính toán.`nan`trong một cập nhật gradient làm cho trọng lượng `nan`, tạo ra mọi sản phẩm tiếp theo `nan`Trình luyện chỉ trong vòng một bước thôi.
> `nan`和 `inf`通过计算病毒式传播――梯度更新中的一个 `nan`使权重变为`nan`, để sau tất cả các xuất phát biến đổi cho `nan`                                                                                                                                                                                                                                                              

Làm sao ?`nan`xuất hiện: `0.0 / 0.0`- `inf - inf`- `inf * 0`- `sqrt()`của âm, `log()`Thiết lập: các đầu vào clamp để `exp()`, thêm epsilon vào tên gọi, sử dụng thực hiện ổn định, cắt gradient.
> `nan`如何出现:`0.0/0.0``inf-inf``inf*0`、负数 của `sqrt()`、负数 của `log()` phòng ngừa: giới hạn`exp()`输入、给分母加 epsilon、使用稳定实现、梯度剪──

### Kiểm tra số lượng độ phân tích kiểm tra số lượng giá trị

Các gradient phân tích (từ backpropagation) có thể có lỗi. kiểm tra gradient số xác minh chúng bằng cách tính toán gradient với sự khác biệt hữu hạn.
> 解析梯度 (được phân tích từ ngược chiều) có thể có lỗi.

```
df/dx ~= (f(x + h) - f(x - h)) / (2h)
```

Quy tắc ngón tay: relative_error < 1e-7: hoàn hảo; < 1e-5: chấp nhận được; > 1e-3: có gì đó sai; > 1: hoàn toàn sai.
> 经验法则:相对错误 < 1e-7:完美;< 1e-5:可接受;> 1e-3:有问题;> 1:完全错误──

### Tập luyện chính xác hỗn hợp tập luyện chính xác hỗn hợp

Các GPU hiện đại có các lõi Tensor tính toán các nhân số matrix float16 nhanh hơn 2-8 lần so với float32.
> 现代 GPU có Tensor Core,float16 矩阵乘法比float32 快 2-8倍──混合精度训练利用这一点──

```
1. Maintain float32 master copy of weights
2. Forward pass in float16 (fast)
3. Compute loss in float32 (prevents overflow)
4. Backward pass in float16 (fast)
5. Scale gradients to float32
6. Update float32 master weights
```

Việc khắc phục cho dòng chảy dưới float16 là quy mô mất mát: nhân mất mát bằng một nhân tố quy mô lớn, vượt qua ngược tính toán các gradient lớn hơn, chia theo quy mô trước khi cập nhật trọng lượng.
> Float16 下溢的修复是损失缩放: sẽ mất gấp nhiều so với yếu tố缩放, ngược chiều truyền tính toán thang độ lớn hơn, nâng cấp trọng lượng trước trừ so với yếu tố缩放.

### bfloat16 vs float16: Tại sao bfloat16 thắng trong tập luyện

float16 có độ chính xác hơn (10 bit mantissa) nhưng phạm vi hạn chế (tối đa là ~65,504). bfloat16 có độ chính xác ít hơn nhưng phạm vi tương tự như float32 (tối đa là ~3.4e38).
> float16 精度更高(10 位尾数) nhưng phạm vi hạn chế(最大 ~65,504) ・bfloat16 精度较低但范围与 float32 相同(最大 ~3.4e38) ・训练时范围更重要──

### Giảm độ cắt đứt độ cắt

Các gradient nổ xảy ra khi gradient tăng theo tốc độ tăng trưởng. Hai loại cắt: clip theo giá trị (cập từng yếu tố) và clip theo chuẩn (tăng quy mô toàn bộ vector để chuẩn của nó không vượt quá ngưỡng). Clip theo chuẩn duy trì hướng gradient. Đây là những gì`torch.nn.utils.clip_grad_norm_()`- Không.
> 梯度爆炸发生在梯度指数增长时――两种剪裁:按值剪裁 (限制每个元素) 和按范数剪裁 (缩缩整量使范数不超过值)――按范数剪裁保留梯度方向――

Giá trị điển hình: `max_norm=1.0`cho các bộ biến đổi, `max_norm=0.5`cho RL, `max_norm=5.0`cho các mạng đơn giản hơn.
> 典型值:Tranformator 用 `max_norm=1.0`,RL dùng `max_norm=0.5`, đơn giản sử dụng mạng`max_norm=5.0`

### Thói quen ML số Bugs  thường thấy ML số giá trị Bug

**Bug: Loss is NaN after a few epochs.**Nguyên nhân: logits quá lớn, softmax tràn.
> **Bug: 几个 epoch 后 loss 变 NaN。**原因:logits 太大,softmax 溢出──修复: sử dụng稳定softmax,降低学习率,添加梯度剪──

**Bug: Validation accuracy is lower by 1-3%.**Nguyên nhân: độ chính xác hỗn hợp mà không có quy mô mất tích thích hợp.
> **Bug: 验证精度低 1-3%。**原因:混合精度没有正确的损失缩放──修复:启动动态损失缩放,或转换到 bfloat16──

**Bug: `exp()` returns `inf` in loss computation.**Phong sửa: sử dụng `torch.nn.functional.log_softmax()`thực hiện log-sum-exp bên trong.
> **Bug: 损失计算中 `exp()` 返回 `inf`。**修复: sử dụng `torch.nn.functional.log_softmax()`

## Hãy xây dựng nó.

### Bước 1: Bước 1: Bước 1: Bước 1: Bước 1: Bước 1: Bước 1: Bước 1: Bước 1: Bước 1: Bước 1: Bước 1: Bước 1: Bước 1: Bước 1: Bước 1: Bước 1: Bước 1: Bước 1: Bước 1: Bước 1: Bước 1: Bước 1: Bước 1: Bước 1: Bước 1: Bước 1: Bước 1: Bước 1: Bước 1: Bước 1: Bước 1: Bước 1: Bước 1: Bước 1: Bước 1: Bước 1: Bước 1: Bước 1: Bước 3: Bước 3: Bước 3: Bước 3: Bước 3: Bước 3: Bước 3: Bước 3: Bước 3: Bước 3: Bước 3: Bước 3: Bước 3: Bước 3: Bước 3: Bước 3: Bước 3: Bước 3: Bước 3: Bước 3: Bước 3: Bước 3: Bước 3: Bước 3: Bước 3: Bước 3: Bước 3: Bước 3: Bước 3: Bước 3: Bước 3: Bước 3: Bước 3: Bước 3: Bước 3: Bước 3: Bước 3: Bước 3: Bước 3: Bước 3: Bước 3: Bước 3: Bước 3: Bước 3: Bước 3: Bước 3: Bước 3: Bước 3: Bước 3: Bước 3: Bước 3: Bước 3: Bước 3: Bước 3: Bước 3: Bước 3: Bước 3: Bước 3: Bước 3: Bước 3: Bước 3: Bước 3: Bước 3: Bước 3: Bước 3: Bước 3: Bước 3: Bước 3: Bước 3: Bước 3: Bước 3: Bước 3: Bước 3: Bước 3: Bước 3: Bước 3: Bước 3: Bước: Bước: Bước: Bước: Bước: Bước: Bước: Bước: Bước: Bước: Bước: Bước: Bước: Bước: Bước: Bước: Bước: Bước: Bước: Bước: Bước: Bước: Bước: Bước: Bước: Bước: Bước:
**Bug: Validation accuracy is lower than expected by 1-3%.**
Nguyên nhân: độ chính xác hỗn hợp mà không có quy mô mất tích thích hợp.
Lắp đặt: bật quy mô mất mát động, hoặc chuyển sang bfloat16.

**Bug: Gradient norms are 0.0 for some layers.**
Nguyên nhân: các tế bào thần kinh ReLU chết (tất cả đầu vào âm), hoặc float16 dưới dòng chảy.
Lấy LeakyReLU hoặc GELU, sử dụng quy mô gradient, kiểm tra kích hoạt trọng lượng.

**Bug: Model works on one GPU but gives different results on another.**
Nguyên nhân: thứ tự tích lũy điểm nổi không xác định. Giảm song song GPU tổng hợp trong các thứ tự khác nhau trên phần cứng khác nhau, và việc bổ sung điểm nổi không liên quan.
Xác định: chấp nhận những khác biệt nhỏ (1e-6), hoặc đặt `torch.use_deterministic_algorithms(True)`và chấp nhận hình phạt tốc độ.

**Bug: `exp()` returns `inf` in loss computation.**
Nguyên nhân: logit thô được chuyển đến `exp()`Không có thủ thuật trừ tối đa.
Phong sửa: sử dụng `torch.nn.functional.log_softmax()`thực hiện log-sum-exp bên trong.

**Bug: Training diverges after switching from float32 to float16.**
Nguyên nhân: float16 không thể đại diện cho độ lớn gradient dưới 6e-8 hoặc kích hoạt trên 65.504.
Lắp đặt: sử dụng độ chính xác hỗn hợp với quy mô mất mát (AMP), hoặc sử dụng bfloat16 thay vào đó.

```figure
logsumexp-stability
```

## Hãy xây dựng nó

### Bước 1: Cố gắng giới hạn độ chính xác điểm nổi

```python
print("=== Floating Point Precision ===")
print(f"0.1 + 0.2 = {0.1 + 0.2}")
print(f"0.1 + 0.2 == 0.3? {0.1 + 0.2 == 0.3}")
print(f"Difference: {(0.1 + 0.2) - 0.3:.2e}")
```

### Bước 2: Thực hiện ngây thơ so với ổn định mềmmax.

```python
import math

def softmax_naive(logits):
    exps = [math.exp(z) for z in logits]
    total = sum(exps)
    return [e / total for e in exps]

def softmax_stable(logits):
    max_logit = max(logits)
    exps = [math.exp(z - max_logit) for z in logits]
    total = sum(exps)
    return [e / total for e in exps]

safe_logits = [2.0, 1.0, 0.1]
print(f"Naive:  {softmax_naive(safe_logits)}")
print(f"Stable: {softmax_stable(safe_logits)}")

dangerous_logits = [100.0, 101.0, 102.0]
print(f"Stable: {softmax_stable(dangerous_logits)}")
# softmax_naive(dangerous_logits) would return [nan, nan, nan]
```

### Bước 3: Thực hiện log-sum-exp ổn định.

```python
def logsumexp_stable(values):
    c = max(values)
    return c + math.log(sum(math.exp(v - c) for v in values))
```

### Bước 4: Thực hiện sự liên kết ổn định.

```python
def cross_entropy_stable(true_class, logits):
    max_logit = max(logits)
    shifted = [z - max_logit for z in logits]
    log_sum_exp = math.log(sum(math.exp(s) for s in shifted))
    log_prob = shifted[true_class] - log_sum_exp
    return -log_prob
```

### Bước 5: Kiểm tra độ.

```python
def numerical_gradient(f, x, h=1e-5):
    grad = []
    for i in range(len(x)):
        x_plus = x[:]
        x_minus = x[:]
        x_plus[i] += h
        x_minus[i] -= h
        grad.append((f(x_plus) - f(x_minus)) / (2 * h))
    return grad

def check_gradient(analytical, numerical, tolerance=1e-5):
    for i, (a, n) in enumerate(zip(analytical, numerical)):
        denom = max(abs(a), abs(n), 1e-8)
        rel_error = abs(a - n) / denom
        status = "OK" if rel_error < tolerance else "FAIL"
        print(f"  param {i}: analytical={a:.8f} numerical={n:.8f} "
              f"rel_error={rel_error:.2e} [{status}]")
```

## Hãy sử dụng nó để thực hiện

Nhìn xem`code/numerical.py`cho các triển khai hoàn chỉnh với tất cả các trường hợp cạnh được chứng minh.
> 完整实现见 `code/numerical.py`

```python
# 梯度裁剪
def clip_by_norm(gradients, max_norm):
    total_norm = math.sqrt(sum(g**2 for g in gradients))
    if total_norm > max_norm:
        scale = max_norm / total_norm
        return [g * scale for g in gradients]
    return gradients

# NaN/Inf 检测
def check_tensor(name, values):
    has_nan = any(math.isnan(v) for v in values)
    has_inf = any(math.isinf(v) for v in values)
    if has_nan or has_inf:
        print(f"WARNING {name}: nan={has_nan} inf={has_inf}")
        return False
    return True
```

## Chuyển nó đi.

Bài học này mang lại:
> 本课程产出:

- `code/numerical.py`Với softmax ổn định, log-sum-exp, cross-entropy, kiểm tra gradient và mô phỏng chính xác hỗn hợp
  包含稳定软max, log-sum-exp,交叉, 梯度检查和混合精度模拟
- `outputs/prompt-numerical-debugger.md`cho việc chẩn đoán NaN/Inf và các vấn đề số trong đào tạo
  Sử dụng trong việc đào tạo chẩn đoán vấn đề NaN/Inf và số lượng

## Tập luyện bài tập

1. **Catastrophic cancellation.**Xét sự khác biệt của [1000000.0, 1000001.0, 1000002.0] bằng cách sử dụng công thức ngây thơ `E[x^2] - E[x]^2`Sau đó tính toán nó bằng cách sử dụng thuật toán trực tuyến của Welford. So sánh các lỗi với sự khác biệt thực (0,6667).
   **灾难性抵消。**用朴素公式和 Welford 算法计算 [1000000.0, 1000001.0, 1000002.0] 的方差,比较误差──

2. **Precision hunt.**Tìm giá trị float32 tích cực nhỏ nhất `x`như thế này`1.0 + x == 1.0`- Hãy kiểm tra xem nó phù hợp.`numpy.finfo(numpy.float32).eps`- Tôi không biết.
   **精度搜索。**找到使 `1.0 + x == 1.0`Ưu điểm float32 ⋅

3. **Log-sum-exp edge cases.**Thử nghiệm `logsumexp_stable`hàm với: (a) tất cả các giá trị bằng nhau, (b) một giá trị lớn hơn nhiều so với các giá trị khác, (c) tất cả các giá trị rất âm (-1000).
   **Log-sum-exp 边界情况。**测试稳定 log-sum-exp 在极端输入下表现──

4. **Gradient checking a neural network layer.**Thực hiện một lớp tuyến tính đơn `y = Wx + b`và xác minh sự chính xác cho một số liệu trọng lượng 3x2.
   **梯度检查神经网络层。**实现单层线性层并验证正确性──

5. **Loss scaling experiment.**Mô phỏng đào tạo với float16: đo phần nào của gradient trở thành không.
   **损失缩放实验。**模拟 float16 训练, đo gradiente biến thành tỷ lệ 0, rồi áp dụng mất tích giảm và đo lại.

## Từ khóa  Từ khóa nhanh chóng

| Term / 术语 | What people say | What it actually means / 实际含义 |
|------|----------------|----------------------|
| IEEE 754 | "The float standard" | International standard defining binary floating point formats. / 定义二进制浮点格式的国际标准。 |
| Machine epsilon / 机器精度 | "The precision limit" | The smallest value e such that 1.0 + e != 1.0. For float32, ~1.19e-7. / 使 1.0 + e != 1.0 的最小值。float32 约 1.19e-7。 |
| Catastrophic cancellation / 灾难性抵消 | "Precision loss from subtraction" | Significant digits cancel when subtracting nearly equal numbers. / 相减近似相等数时有效数字抵消。 |
| Overflow / 溢出 | "Number too big" | A result exceeds the maximum representable value and becomes inf. / 结果超过最大可表示值变为 inf。 |
| Underflow / 下溢 | "Number too small" | A result is closer to zero than the smallest representable positive number. / 结果比最小可表示正数更接近零。 |
| Log-sum-exp trick / Log-sum-exp 技巧 | "Subtract the max first" | Computing log(sum(exp(x))) by factoring out exp(max(x)). / 通过提取 exp(max(x)) 计算 log(sum(exp(x)))。 |
| Stable softmax / 稳定 softmax | "Softmax that does not explode" | Subtracting max(logits) before exponentiating. / 指数化前减去最大 logit。 |
| Gradient checking / 梯度检查 | "Verify your backprop" | Comparing analytical vs numerical gradients to catch bugs. / 比较解析和数值梯度以捕获 bug。 |
| Mixed precision / 混合精度 | "Float16 forward, float32 backward" | Using lower-precision for speed, higher-precision for accuracy. / 低精度加速，高精度保准确。 |
| Loss scaling / 损失缩放 | "Prevent gradient underflow" | Multiplying loss by a large constant to keep gradients in float16 range. / 将损失乘以大常数使梯度保持在 float16 范围内。 |
| bfloat16 | "Brain floating point" | Google's 16-bit format with 8 exponent bits. Preferred for training. / Google 的 16 位格式，8 位指数。训练首选。 |
| Gradient clipping / 梯度裁剪 | "Cap the gradient norm" | Scaling the gradient vector so its norm does not exceed a threshold. / 缩放梯度向量使范数不超过阈值。 |
| NaN | "Not a Number" | Special float value from undefined operations. Propagates through all arithmetic. / 未定义操作的特殊浮点值。通过所有算术传播。 |
| Inf | "Infinity" | Special float value from overflow or division by zero. / 溢出或除零产生的特殊浮点值。 |
| Numerical gradient / 数值梯度 | "Brute force derivative" | Approximating a derivative by evaluating f(x+h) and f(x-h). / 通过求 f(x+h) 和 f(x-h) 近似导数。 |

## Xem thêm 延伸阅读

- [What Every Computer Scientist Should Know About Floating-Point Arithmetic (Goldberg 1991)](https://docs.oracle.com/cd/E19957-01/806-3568/ncg_goldberg.html)-- tham chiếu cuối cùng
  浮点算术 quyền hạn tham khảo
- [Mixed Precision Training (Micikevicius et al., 2018)](https://arxiv.org/abs/1710.03740)-- bài báo của NVIDIA về việc mở rộng quy mô lỗ
  NVIDIA 损失缩放论文
- [AMP: Automatic Mixed Precision (PyTorch docs)](https://pytorch.org/docs/stable/amp.html)-- hướng dẫn thực tế
  PyTorch 混合精度实践指南
- [bfloat16 format (Google Cloud TPU docs)](https://cloud.google.com/tpu/docs/bfloat16)-- tại sao Google chọn định dạng này
  Google  chọn bfloat16 的原因
- [Kahan Summation (Wikipedia)](https://en.wikipedia.org/wiki/Kahan_summation_algorithm)-- thuật toán để giảm lỗi tròn
  减少舍进差的 Kahan 求和算法
