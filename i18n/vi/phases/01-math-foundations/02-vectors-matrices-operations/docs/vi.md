# Dòng, Matrix & Operations

> Mỗi mạng thần kinh chỉ là sự nhân số của một số matrix với các bước bổ sung.

> Mỗi mạng thần kinh bản chất là một số bước bổ sung.

**Type:** Build | **类型:** 动手
**Languages:** Python, Julia | **语言:** Python, Julia
**Prerequisites:** Phase 1, Lesson 01 (Linear Algebra Intuition) | **前置知识:** Phase 1, Lesson 01 (线性代数直觉)
**Time:** ~60 minutes | **时间:** ~60 分钟

## Mục tiêu học tập

- Xây dựng một lớp Matrix với các hoạt động thông minh về các yếu tố, nhân số matrix, chuyển giao, xác định và ngược lại
  构建包含 từng yếu tố运算、矩阵乘法、转置、行列式、逆矩阵的矩阵类
- Hóa ra sự nhân nhân bằng các yếu tố và sự nhân tử và giải thích khi nào mỗi ứng dụng
  区分 từng yếu tố乘法 và矩阵乘法, giải thích các trường hợp thích hợp của riêng mình
- Thực hiện một lớp mạng thần kinh dày đặc duy nhất (`relu(W @ x + b)`) chỉ sử dụng lớp Matrix từ đầu
  Chỉ cần sử dụng từ không thực hiện Matrix 类 để thực hiện một lớp mạng thần kinh mật`relu(W @ x + b)`(văn)
- Giải thích các quy tắc phát sóng và cách việc bổ sung thiên vị hoạt động trong các khung mạng thần kinh
  解释广播规则和神经网络框架中偏置加法的工作方式

> **【中文解读】**
> Các mô hình của mỗi mạng thần kinh là mô hình mô hình mô hình mô hình mô hình mô hình mô hình mô hình mô hình mô hình mô hình mô hình mô hình mô hình mô hình mô hình mô hình mô hình mô hình mô hình mô hình mô hình mô hình mô hình mô hình mô hình mô hình mô hình mô hình mô hình mô hình mô hình mô hình mô hình mô hình mô hình mô hình mô hình mô hình mô hình mô hình mô hình mô hình mô hình mô hình mô hình mô hình mô hình mô hình mô hình mô hình mô hình mô hình mô hình mô hình mô hình mô hình mô hình mô hình mô hình mô hình mô hình mô hình mô hình mô hình mô hình mô hình mô hình mô hình mô hình mô hình mô hình mô hình mô hình mô hình mô hình mô hình mô hình mô hình mô hình mô hình mô hình mô hình mô hình mô hình mô hình mô hình mô hình mô hình mô hình mô hình mô hình mô hình mô hình mô hình mô hình mô hình mô hình mô hình mô hình mô hình mô hình mô hình mô hình mô hình mô hình mô hình mô hình mô hình mô hình mô hình mô hình mô hình mô hình mô hình mô hình mô hình mô hình mô hình mô hình mô hình mô hình mô hình mô hình mô hình mô hình mô hình mô hình mô hình mô hình mô hình mô hình mô hình mô hình mô hình mô hình mô hình mô hình mô hình mô hình mô hình mô hình mô hình mô hình mô hình mô hình mô hình mô hình mô hình mô hình mô hình mô hình mô hình mô hình mô hình mô hình mô hình mô hình mô hình mô hình mô hình mô hình mô hình mô hình mô hình mô hình mô hình mô hình mô hình mô hình mô hình mô mô mô hình mô hình mô mô mô mô mô mô mô mô mô mô mô mô mô mô mô mô mô mô mô mô mô mô mô mô mô mô mô mô mô mô mô mô mô mô mô mô mô mô mô mô mô mô mô mô mô mô mô mô mô mô mô mô mô mô mô mô mô mô mô mô mô mô mô mô mô mô mô mô mô mô mô mô mô mô mô mô mô mô mô mô mô mô mô mô mô mô mô mô mô mô mô mô mô mô mô mô mô mô mô mô mô mô mô mô mô mô mô mô mô mô mô mô mô mô mô mô mô mô mô mô mô mô mô mô mô mô mô mô mô mô mô mô mô mô mô mô mô mô mô mô mô mô mô mô mô mô mô mô mô mô mô mô mô`output = relu(W @ x + b)`Đây là toán học đằng sau mã.

> **【拓展：向量/矩阵在 AI 中的位置】**
> - **词嵌入（Word Embedding）**Mỗi từ được biểu thị cho một chiều dài cao như 300维, từ ngữ nghĩa gần trong không gian chiều dài gần hơn. Đây là cơ sở của NLP.
> - **神经网络权重**Mỗi tầng trọng lượng là một khối, khối lượng nhập nhân khối lượng ra ngoài.
> - **Transformer 的注意力机制**Về bản chất là Q、K、V 三矩阵的乘法和软max运算──

## Vấn đề  vấn đề giới thiệu

Bạn muốn xây dựng một mạng lưới thần kinh. Bạn đọc mã và thấy điều này:

> Bạn muốn xây dựng một mạng lưới thần kinh. Bạn thấy mã trong đó viết:

```
output = activation(weights @ input + bias)
```

Đó là`@`là nhân tử liệu.`weights`là một matrix.`input`nếu bạn không biết các hoạt động đó làm gì, đường này là phép thuật. nếu bạn biết, nó là toàn bộ chuyển tiếp về phía trước của một lớp trong ba hoạt động.

> `@`Đó là một cách thức.`weights`Đó là một trận đấu.`input`Nếu bạn không biết những điều này làm gì, thì mã này là phép thuật. Nếu bạn biết, đó là một tầng hoàn chỉnh của một tầng truyền tải.

Mỗi hình ảnh mà mô hình của bạn xử lý là một matrix của các giá trị pixel. Mỗi từ nhúng là một vector. Mỗi lớp của mỗi mạng thần kinh là một sự chuyển đổi matrix. Bạn không thể xây dựng hệ thống AI mà không biết matrix một cách thông thạo, giống như bạn không thể viết mã mà không hiểu các biến.

> Mỗi hình ảnh trong mô hình xử lý là một mô hình, mỗi từ được đặt là một mô hình, mỗi tầng của mạng thần kinh là một mô hình thay đổi. Không biết mô hình vận hành là không thể xây dựng AI  hệ thống, giống như không hiểu biến số là không thể viết mã như vậy.

Bài học này giúp bạn có sự thịnh vượng từ đầu.

> 本课从零开始建立这种熟练度.

> **【中文解读】**
> `output = activation(weights @ input + bias)`Đây là một phần của một mạng lưới thần kinh. Nếu bạn không hiểu được phương pháp nhân số, nó trông giống như ma thuật; nếu bạn hiểu, nó là ba hoạt động cơ bản.

## Khái niệm cốt lõi

### Các vector: danh sách số được sắp xếp.

Một vector là một danh sách số với một hướng và quy mô. Trong AI, vector đại diện cho các điểm dữ liệu, tính năng hoặc tham số.

> Vòng là một tập hợp có hướng và số lớn. Trong AI, khối đại diện cho các điểm dữ liệu, đặc điểm hoặc tham số.

```
v = [3, 4]        -- a 2D vector # 二维向量
w = [1, 0, -2]    -- a 3D vector # 三维向量
```

Một vector 2D `[3, 4]`chỉ ra các phối hợp (3, 4) trên một máy bay. chiều dài (lượng lớn) của nó là 5 (lối ba - 3-4 - 5).

> 2 chiều`[3, 4]`指向平面上的坐标 (3, 4),长度为 5(勾股定理 3-4-5 三角形) ⋅

### Matrix: lưới số 矩阵: số lưới

Một matrix là một lưới 2D. Dòng và cột. Một m x n matrix có m hàng và n cột.

> 矩阵是二维网格,由行和列组成──一个 m x n 矩阵有 m 行 n 列──

```
A = | 1  2  3 |     -- 2x3 matrix (2 rows, 3 columns) # 2行3列矩阵
    | 4  5  6 |
```

Trong mạng thần kinh, các matrices trọng lượng chuyển đổi các vector đầu vào thành vector đầu ra. Một lớp có 784 đầu vào và 128 đầu ra sử dụng một matrices trọng lượng 128x784.

> Trong mạng thần kinh, khối trọng lượng sẽ chuyển đổi khối lượng nhập thành khối lượng ra. Một có 784 khối lượng nhập và 128 khối lượng ra.

### Tại sao hình dạng quan trọng

Sự nhân số của matrix có một quy tắc nghiêm ngặt:`(m x n) @ (n x p) = (m x p)`- Các kích thước bên trong phải phù hợp.

> 矩阵乘法 có quy tắc hình dạng nghiêm ngặt:`(m x n) @ (n x p) = (m x p)`, kích thước bên trong phải phù hợp.

```
(128 x 784) @ (784 x 1) = (128 x 1)
  weights       input       output # 权重矩阵 × 输入向量 = 输出向量

Inner dimensions: 784 = 784  -- valid # 内部维度必须匹配
```

Nếu bạn nhận được một sai lầm không phù hợp hình dạng trong PyTorch, đây là lý do tại sao.

> Bạn gặp "sự không phù hợp hình dạng" trong PyTorch  lỗi thời, 99% nguyên nhân là quy tắc này đã bị vi phạm.

> **【中文解读】**
> 矩阵乘法形状规则: ((m x n) @ (n x p) = (m x p) ・・・ nội kích phải phù hợp。 Bạn trong PyTorch 中 gặp phải "không phù hợp hình dạng" 错误时,99% của nguyên nhân là quy tắc này đã bị vi phạm。

### Bản đồ hoạt động.

| Operation | What it does | Neural network use |
|-----------|-------------|-------------------|
| Addition | Element-wise combine | Adding bias to output |
| Scalar multiply | Scale every element | Learning rate * gradients |
| Matrix multiply | Transform vectors | Layer forward pass |
| Transpose | Flip rows and columns | Backpropagation |
| Determinant | Single number summary | Checking invertibility |
| Inverse | Undo a transformation | Solving linear systems |
| Identity | Do-nothing matrix | Initialization, residual connections |

| 运算 | 作用 | 神经网络中的用途 |
|------|------|---------------|
| 加法 | 逐元素相加 | 给输出加偏置(bias) |
| 标量乘法 | 缩放所有元素 | 学习率 × 梯度 |
| 矩阵乘法 | 变换向量 | 层的前向传播 |
| 转置 | 行列互换 | 反向传播 |
| 行列式 | 单个数字概括 | 检查可逆性 |
| 逆矩阵 | 撤销变换 | 解线性方程组 |
| 单位矩阵 | 不做任何变换 | 初始化、残差连接(ResNet) |

### Sự nhân từ các yếu tố so với số tử

Sự phân biệt này thường khiến người mới bắt đầu gặp khó khăn.

> Sự khác biệt này thường khiến học viên mới bắt đầu bối rối.

Điểm yếu tố: nhân các vị trí phù hợp. Cả hai matrices phải có cùng hình dạng.

> 逐元素乘法: đối với vị trí乘, hai hình dạng矩阵 phải giống nhau.`*`Cảm thấy

```
| 1  2 |   | 5  6 |   | 5  12 |
| 3  4 | * | 7  8 | = | 21 32 |
```

Tần số tử liệu: sản phẩm điểm của các hàng và cột.

> 矩阵乘法:行与列做点积, kích thước bên trong phải phù hợp.`@`Cảm thấy

```
| 1  2 |   | 5  6 |   | 1*5+2*7  1*6+2*8 |   | 19  22 |
| 3  4 | @ | 7  8 | = | 3*5+4*7  3*6+4*8 | = | 43  50 |
```

Các hoạt động khác nhau, kết quả khác nhau, quy tắc khác nhau.

> Diễn biến khác nhau, kết quả khác nhau, quy tắc khác nhau.`*`和 `@`Trong số số số / PyTorch 中含义完全不同,混会导致无声 bug──

### Truyền thông

Khi bạn thêm một vector thiên vị vào một số lượng đầu ra, các hình dạng không phù hợp.

>  Cơ chế phát thanh: Khi hình dạng của khối chuyển hướng không phù hợp với khối đầu ra, thì bộ phát thanh sẽ tự động mở rộng số lượng nhỏ hơn để phù hợp.

```
| 1  2  3 |   +   [10, 20, 30]
| 4  5  6 |

Broadcasting stretches the vector across rows:

| 1  2  3 |   | 10  20  30 |   | 11  22  33 |
| 4  5  6 | + | 10  20  30 | = | 14  25  36 |
```

Mỗi khung hiện đại tự động làm điều này. hiểu nó ngăn ngừa sự nhầm lẫn khi hình dạng dường như sai nhưng mã chạy.

> Mỗi khung hình hiện đại đều tự động phát sóng.

## Hãy xây dựng nó.
```figure
vector-projection
```

## Hãy xây dựng nó

### Bước 1: lớp vector

```python
class Vector:
    def __init__(self, data):
        self.data = list(data)
        self.size = len(self.data)

    def __repr__(self):
        return f"Vector({self.data})"

    def __add__(self, other):
        return Vector([a + b for a, b in zip(self.data, other.data)])

    def __sub__(self, other):
        return Vector([a - b for a, b in zip(self.data, other.data)])

    def __mul__(self, scalar):
        return Vector([x * scalar for x in self.data])

    def dot(self, other):
        return sum(a * b for a, b in zip(self.data, other.data)])

    def magnitude(self):
        return sum(x ** 2 for x in self.data) ** 0.5
```

> Vector 类实现:加法/减法是逐元素运算;标量乘法扩至每个分量;点是点积(对应分量乘积之和);大小是模长(√(x2+y2+...))。

### Bước 2: lớp matrix với các hoạt động cốt lõi

```python
class Matrix:
    def __init__(self, data):
        self.data = [list(row) for row in data]
        self.rows = len(self.data)
        self.cols = len(self.data[0])
        self.shape = (self.rows, self.cols)

    def __repr__(self):
        rows_str = "\n  ".join(str(row) for row in self.data)
        return f"Matrix({self.shape}):\n  {rows_str}"

    def __add__(self, other):
        return Matrix([
            [self.data[i][j] + other.data[i][j] for j in range(self.cols)]
            for i in range(self.rows)
        ])

    def __sub__(self, other):
        return Matrix([
            [self.data[i][j] - other.data[i][j] for j in range(self.cols)]
            for i in range(self.rows)
        ])

    def scalar_multiply(self, scalar):
        return Matrix([
            [self.data[i][j] * scalar for j in range(self.cols)]
            for i in range(self.rows)
        ])

    def element_wise_multiply(self, other):
        return Matrix([
            [self.data[i][j] * other.data[i][j] for j in range(self.cols)]
            for i in range(self.rows)
        ])

    def matmul(self, other):
        return Matrix([
            [
                sum(self.data[i][k] * other.data[k][j] for k in range(self.cols))
                for j in range(other.cols)
            ]
            for i in range(self.rows)
        ])

    def transpose(self):
        return Matrix([
            [self.data[j][i] for j in range(self.rows)]
            for i in range(self.cols)
        ])

    def determinant(self):
        if self.shape == (1, 1):
            return self.data[0][0]
        if self.shape == (2, 2):
            return self.data[0][0] * self.data[1][1] - self.data[0][1] * self.data[1][0]
        det = 0
        for j in range(self.cols):
            minor = Matrix([
                [self.data[i][k] for k in range(self.cols) if k != j]
                for i in range(1, self.rows)
            ])
            det += ((-1) ** j) * self.data[0][j] * minor.determinant()
        return det

    def inverse_2x2(self):
        det = self.determinant()
        if det == 0:
            raise ValueError("Matrix is singular, no inverse exists")
        return Matrix([
            [self.data[1][1] / det, -self.data[0][1] / det],
            [-self.data[1][0] / det, self.data[0][0] / det]
        ])

    @staticmethod
    def identity(n):
        return Matrix([
            [1 if i == j else 0 for j in range(n)]
            for i in range(n)
        ])
```

> Matrix 类核心操作:matmul 是矩阵乘法(行×列做点积); chuyển 行列互换;determinant 用递归拉普拉斯展开;inverse_2x2 用 (1/det) × [[d,-b],[-c,a]];identity 创建单位矩阵。

### Bước 3: Hãy xem nó hoạt động

```python
A = Matrix([[1, 2], [3, 4]])
B = Matrix([[5, 6], [7, 8]])

print("A + B =", (A + B).data)
print("A @ B =", A.matmul(B).data)
print("A^T =", A.transpose().data)
print("det(A) =", A.determinant())
print("A^-1 =", A.inverse_2x2().data)

I = Matrix.identity(2)
print("A @ A^-1 =", A.matmul(A.inverse_2x2()).data)
```

> 验证 Matrix 类:A+B、A@B、A^T、det(A)、A−1 都正确──最关键的验证是A @ A−1 = I(单位矩阵),这确认逆矩阵实现正确──

### Bước 4: Kết nối với mạng lưới thần kinh  Kết nối với mạng lưới thần kinh

> Bước 4: Kết nối với mạng thần kinh sử dụng các loại Matrix thực hiện từ không để xây dựng một lớp mạng thần kinh hoàn chỉnh.

```python
import random

inputs = Matrix([[0.5], [0.8], [0.2]])  # 输入向量（3 维）
weights = Matrix([  # 权重矩阵（2x3），将 3 维输入映射到 2 维输出
    [random.uniform(-1, 1) for _ in range(3)]
    for _ in range(2)
])
bias = Matrix([[0.1], [0.1]])  # 偏置向量（2 维）

def relu_matrix(m):
    return Matrix([[max(0, val) for val in row] for row in m.data])  # ReLU 激活函数：小于0的值变为0

pre_activation = weights.matmul(inputs) + bias  # W @ x + b（线性变换加偏置）
output = relu_matrix(pre_activation)  # relu(W @ x + b)（加非线性激活）

print(f"Input shape: {inputs.shape}")
print(f"Weight shape: {weights.shape}")
print(f"Output shape: {output.shape}")
print(f"Output: {output.data}")
```

Đây là một lớp dày đặc đơn:`output = relu(W @ x + b)`Mỗi lớp dày đặc trong mỗi mạng thần kinh đều làm điều này.

> **【中文解读】**
> Đây là sự thực hiện hoàn toàn của toàn bộ mạng lưới thần kinh: chuyển đổi liên kết: W @ x + b) + hoạt động không liên kết: ReLU) ⋅ dù là 1 tầng hay 100 tầng mạng, mỗi tầng đều làm điều tương tự.

## Hãy sử dụng nó để thực hiện

NumPy làm mọi thứ ở trên trong ít đường và các thứ tự lớn hơn nhanh hơn.

> NumPy sử dụng ít mã hơn, nhanh chóng một số lượng cấp độ hoàn thành các hoạt động tương tự.

```python
import numpy as np

A = np.array([[1, 2], [3, 4]])
B = np.array([[5, 6], [7, 8]])

print("A + B =\n", A + B)
print("A * B (element-wise) =\n", A * B)
print("A @ B (matrix multiply) =\n", A @ B)
print("A^T =\n", A.T)
print("det(A) =", np.linalg.det(A))
print("A^-1 =\n", np.linalg.inv(A))
print("I =\n", np.eye(2))

inputs = np.random.randn(3, 1)
weights = np.random.randn(2, 3)
bias = np.array([[0.1], [0.1]])
output = np.maximum(0, weights @ inputs + bias)

print(f"\nNeural network layer: {weights.shape} @ {inputs.shape} = {output.shape}")
print(f"Output:\n{output}")
```

- `@`operator trong Python call `__matmul__`NumPy thực hiện nó với các thói quen BLAS tối ưu được viết bằng C và Fortran.

> Python của `@`运算符调用 `__matmul__`◊NumPy sử dụng C và Fortran 编写的优化 BLAS 例例,同样数学,快 100倍──

Truyền thông trong NumPy:

```python
matrix = np.array([[1, 2, 3], [4, 5, 6]])
bias = np.array([10, 20, 30])
print(matrix + bias)
```

NumPy tự động phát sóng sự thiên vị 1D qua cả hai hàng. Đây là cách việc bổ sung thiên vị hoạt động trong mọi khung mạng thần kinh.

> NumPy tự động sẽ có một chiều hướng định vị và tải rộng đến tất cả các đường. Đây là cách thức làm việc của mỗi hệ thống mạng thần kinh.

## Chuyển nó đi.

Bài học này tạo ra một lời nhắc để dạy các hoạt động matrix thông qua trực giác hình học.`outputs/prompt-matrix-operations.md`- Tôi không biết.

> Bài học này đã được phát triển bởi một thông qua Quý vị trực tiếp giáo sư矩阵运算的提示词──见面`outputs/prompt-matrix-operations.md`

Các lớp Matrix được xây dựng ở đây là nền tảng cho các hệ thống mạng lưới thần kinh nhỏ chúng tôi xây dựng trong giai đoạn 3, Bài học 10.

> Các loại Matrix được xây dựng trong đó là cơ sở của khuôn khổ mạng lưới thần kinh ảo giai đoạn 3 thứ 10.

## Tập luyện bài tập

1. **Verify the inverse.**Tăng nhiều`A @ A.inverse_2x2()`và xác nhận bạn có được các mã số danh tính. thử với ba mã số 2x2 khác nhau.
   **验证逆矩阵。**sẽ`A @ A.inverse_2x2()`相乘, xác nhận được đơn vị矩阵.

2. **Implement 3x3 inverse.**Lớn thêm lớp Matrix để tính toán ngược cho các matrices 3x3 bằng cách sử dụng phương pháp adjugate.`np.linalg.inv`- Tôi không biết.
   **实现 3x3 逆矩阵。**Sử dụng cùng với các mô hình mở rộng Matrix 类, với kết quả của NumPy đối với

3. **Build a two-layer network.**Sử dụng chỉ lớp Matrix của bạn (không có NumPy), tạo một mạng thần kinh hai lớp: đầu vào (3) -> ẩn (4) -> đầu ra (2). Tạo ra các trọng lượng ngẫu nhiên, chạy một bước đi về phía trước và xác minh tất cả các hình dạng đều chính xác.
   **构建双层网络。**Chỉ sử dụng Matrix 类(不用 NumPy), tạo输入(3)-> ẩn藏(4)->输出(2) của mạng,运行前向传播并验证形状。

## Từ khóa  Keyword

| Term | What people say | What it actually means |
|------|----------------|----------------------|
| Vector | "An arrow" | An ordered list of numbers. In AI: a point in high-dimensional space. |
| Matrix | "A table of numbers" | A linear transformation. It maps vectors from one space to another. |
| Matrix multiply | "Just multiply the numbers" | Dot products between every row of the first matrix and every column of the second. Order matters. |
| Transpose | "Flip it" | Swap rows and columns. Turns an m x n matrix into n x m. Critical in backpropagation. |
| Determinant | "Some number from the matrix" | Measures how much the matrix scales area (2D) or volume (3D). Zero means the transformation crushes a dimension. |
| Inverse | "Undo the matrix" | The matrix that reverses the transformation. Only exists when the determinant is not zero. |
| Identity matrix | "The boring matrix" | The matrix equivalent of multiplying by 1. Used in residual connections (ResNets). |
| Broadcasting | "Magic shape fixing" | Stretching a smaller array to match a larger one by repeating along missing dimensions. |
| Element-wise | "Regular multiplication" | Multiply matching positions. Both arrays must have the same shape (or be broadcastable). |

| 术语 | 俗称 | 实际含义 |
|------|------|---------|
| Vector（向量） | "箭头" | 有序数字列表。AI 中表示高维空间中的点 |
| Matrix（矩阵） | "数字表格" | 线性变换，将向量从一个空间映射到另一个空间 |
| Matrix multiply（矩阵乘法） | "数字相乘" | 第一个矩阵的行与第二个矩阵的列做点积，顺序很重要 |
| Transpose（转置） | "翻转" | 行列互换，反向传播中必不可少 |
| Determinant（行列式） | "矩阵的某个数字" | 衡量矩阵缩放面积/体积的程度，为零意味着维度被压缩 |
| Inverse（逆矩阵） | "撤销矩阵" | 逆转变换的矩阵，仅在行列式非零时存在 |
| Identity（单位矩阵） | "无聊的矩阵" | 相当于乘以 1 的矩阵，用于残差连接(ResNet) |
| Broadcasting（广播） | "魔法形状修复" | 沿缺失维度复制小数组以匹配大数组 |
| Element-wise（逐元素） | "普通乘法" | 逐位相乘，两个数组形状必须相同 |

## Xem thêm 延伸阅读

- [3Blue1Brown: Essence of Linear Algebra](https://www.3blue1brown.com/topics/linear-algebra)- trực giác thị giác cho mỗi hoạt động được đề cập ở đây
- [NumPy documentation on broadcasting](https://numpy.org/doc/stable/user/basics.broadcasting.html)- các quy tắc chính xác của NumPy
- [Stanford CS229 Linear Algebra Review](http://cs229.stanford.edu/section/cs229-linalg.pdf)- tham chiếu ngắn gọn cho toán toán tuyến tính cụ thể ML
