# 矢量,矩阵和运算

> 每个神经网络都是一个矩阵乘法,

> 每个神经网络本质上都是矩阵乘法加上几个额外步骤.

**Type:** Build | **类型:** 动手
**Languages:** Python, Julia | **语言:** Python, Julia
**Prerequisites:** Phase 1, Lesson 01 (Linear Algebra Intuition) | **前置知识:** Phase 1, Lesson 01 (线性代数直觉)
**Time:** ~60 minutes | **时间:** ~60 分钟

## 学习目标

- 构建一个矩阵类,以元素理性操作,矩阵乘法,转换,定数和反
  构建包含各元素运算"",矩阵乘法"",转置"",行列式"",逆矩阵的矩阵类型
- 区分元素式乘法与矩阵乘法,并解释每一个乘法是什么时候适用的
  区分各元素乘法和矩阵乘法,解释各自的适用场景
- 实现单一密集神经网络层 (`relu(W @ x + b)`) 仅使用从零开始的矩阵类
  仅用从零实现的矩阵类实现一个密集神经网络层`relu(W @ x + b)`)
- 解释广播规则以及神经网络框架中偏见加算的运作方式
  解释广播规则和神经网络框架中偏置加法的工作方式

> **【中文解读】**
> 每个神经网络的核心就是矩阵乘法――向量表示数据(如一个词、一张图片),矩阵表示变化(如一层神经网络重量) ・本章从零构建向量类和矩阵类,帮助你彻底理解`output = relu(W @ x + b)`这就是背后的数学.

> **【拓展：向量/矩阵在 AI 中的位置】**
> - **词嵌入（Word Embedding）**每个词被表示为高维向量 (如300维),语义相近的词在向量空间中距离更近.这是NLP的基础.
> - **神经网络权重**每层的重量是一个矩阵,输入矩阵乘以重量矩阵得到输出矩阵.
> - **Transformer 的注意力机制**基本上是Q、K、V 三矩阵的乘法和软max运算.

## 问题 问题引入

你想建立一个神经网络,你读出代码,看看这个:

> 你想建立一个神经网络.

```
output = activation(weights @ input + bias)
```

这`@`它们是矩阵乘法.`weights`它们是矩阵.`input`如果您不知道这些操作是什么,这个线是魔术.如果您知道,这是一个层的整个前进通过在三个操作.

> `@`是矩阵乘法.`weights`是一个矩阵.`input`如果你不知道这些操作是什么,这个代码就是魔法.如果你知道,这是一个层的完整前向传播,只有三个操作.

你的模型处理的每一个图像都是像素值的矩阵.每个嵌入的字符都是矢量.每个神经网络的每个层都是矩阵转换.你不能在矩阵操作中流利地构建人工智能系统,就像你不能在理解变量的情况下编写代码一样.

> 模型处理的每张图像都是像素矩阵,每个词嵌入都是向量,神经网络的每层都是矩阵变化――不精通矩阵运算就无法构建人工智能系统,就像不理解变量就无法写代码一样――

这一课从零开始就能让你变得流利.

> 本课从零开始建立这种熟练度.

> **【中文解读】**
> `output = activation(weights @ input + bias)`这条代码就是神经网络一层的前向传播.如果你不懂矩阵乘法,它看起来像魔法;如果你懂,它就是三个基本操作.

## 概念的核心概念

### 矢量:排序列列数列

矢量是指向和大小的数量列表.在人工智能中,矢量代表数据点,特征或参数.

> 向量是一个有方向和大小的数字. 在AI中,向量表示数据点,特征或参数.

```
v = [3, 4]        -- a 2D vector # 二维向量
w = [1, 0, -2]    -- a 3D vector # 三维向量
```

两个维向量`[3, 4]`它们的长度 (大小) 是5 (三角形3-4-5).

> 量`[3, 4]`指向平面上的坐标 (3, 4),长度为 5(勾股定理 3-4-5 三角形) ⋅

### 矩阵:数字网格

矩阵是一个二维格格. 列和列.一个m x n矩阵有m列和n列.

> 矩阵是二维网格,由行和列组成.

```
A = | 1  2  3 |     -- 2x3 matrix (2 rows, 3 columns) # 2行3列矩阵
    | 4  5  6 |
```

在神经网络中,重量矩阵将输入向量转化为输出向量.一个有784个输入和128个输出的层使用 128x784的重量矩阵.

> 在神经网络中,权重矩阵将输入向量变换为输出向量――一个有784个输入和128个输出层使用 128x784的权重矩阵――

### 为什么形状很重要

矩阵乘法有一个严格的规则:`(m x n) @ (n x p) = (m x p)`内部的尺寸必须相匹配.

> 矩阵乘法有严格的形状规则:`(m x n) @ (n x p) = (m x p)`内部维度必须一致.

```
(128 x 784) @ (784 x 1) = (128 x 1)
  weights       input       output # 权重矩阵 × 输入向量 = 输出向量

Inner dimensions: 784 = 784  -- valid # 内部维度必须匹配
```

如果在 PyTorch 中出现了形状不匹配错误,

> 在 PyTorch 中遇到"形状不匹配"的错误时,99%的原因是这个规则被违反了.

> **【中文解读】**
> 矩阵乘法形状规则: ((m x n) @ (n x p) = (m x p) ・・・内部维度必须一致──你在 PyTorch 中遇到"形状不匹配" 错误时,99% 的原因是这个规则被违反──

### 运算对照表

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

### 元素智能与矩阵乘法

这种区别会让初学者不断地陷入困境.

> 这种区别经常让初学者困惑.

按元素的角度,乘以相匹配的位置.

> 逐元素乘法:对应位置相乘,两个矩阵形状必须相同.`*`显示

```
| 1  2 |   | 5  6 |   | 5  12 |
| 3  4 | * | 7  8 | = | 21 32 |
```

矩阵乘法:列和列的点产量.内面尺寸必须匹配.

> 矩阵乘法:行与列做点积,内部维度必须一致.`@`显示

```
| 1  2 |   | 5  6 |   | 1*5+2*7  1*6+2*8 |   | 19  22 |
| 3  4 | @ | 7  8 | = | 3*5+4*7  3*6+4*8 | = | 43  50 |
```

不同的操作,不同的结果,不同的规则.

> 不同的操作,不同的结果,不同的规则.`*`和 `@`在NumPy/PyTorch 中含义完全不同,混会导致沉默 bug──

### 广播

输出矩阵中添加偏差向量时,形状不匹配.

> 广播机制:当偏向向量与输出矩阵形状不匹配时,广播会自动扩展较小的数组来适应.

```
| 1  2  3 |   +   [10, 20, 30]
| 4  5  6 |

Broadcasting stretches the vector across rows:

| 1  2  3 |   | 10  20  30 |   | 11  22  33 |
| 4  5  6 | + | 10  20  30 | = | 14  25  36 |
```

任何现代框架都会自动做到这一点.

> 每个现代框架都会自动播放.

## 建立它,实现它.
```figure
vector-projection
```

## 建立它

### 步骤1:向量类

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

> 矢量 类实现:加法/减法是逐元素运算;标量乘法扩大到每个分量;点是积点;大小是模长;√√√x2+y2+...))。

### 步骤2: 核心操作的矩阵类

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

> 矩阵 类核心操作:matmul 是矩阵乘法(行×列做点积);转换 行列互换;确定符 用递归拉普拉斯展开;反向_2x2 用 (1/det) × [[d,-b],[-c,a]];身份 创建单位矩阵。

### 步骤3: 让它发挥作用

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

> 验证矩阵类:A+B、A@B、A^T、det(A)、A−1 都正确──最关键的验证是A @A−1 = I(单位矩阵),这确认逆矩阵实现正确──

### 连接到神经网络.

> 第4步:连接到神经网络使用从零实现的矩阵类构建一个完整的神经网络层

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

这是一个单密层:`output = relu(W @ x + b)`每个神经网络的密集层都会做这么做.

> **【中文解读】**
> 这就是神经网络全连接层的完整实现:线性变换 ((W @ x + b) +非线性激活 ((ReLU) ⋅无论是1层还是100层的网络,每个层都在做同样的事情──

## 用它实现框架

平在更少的线上和更快的规模上完成了以上的一切.

> 通过更少的代码,快速完成相同的操作.

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

其他`@`在Python调用中操作员`__matmul__`通过C和Fortan编写的优化BLAS程序实现了它.

> 字符串的`@`运算符调用`__matmul__`△数Py 使用C 和 Fortran 编写的优化 BLAS 例例,同样的数学,快 100倍──

在NumPy中播放:

```python
matrix = np.array([[1, 2, 3], [4, 5, 6]])
bias = np.array([10, 20, 30])
print(matrix + bias)
```

通过 NumPy 实现了自动播放1D偏差在两个行中.

> 网络的每个神经网络框架中偏移加法工作方式.

## 运送它.

通过几何直觉来教导矩阵操作.`outputs/prompt-matrix-operations.md`现在,我们要去.

> 本课产出了一个通过几何直觉教授矩阵运算的提示词.`outputs/prompt-matrix-operations.md`,我知道.

在这个阶段建立的矩阵类是我们在3阶段的10课时建立的微神经网络框架的基础.

> 在此构建的矩阵类是第三阶段第十课迷你神经网络框架的基础.

## 练习题

1. **Verify the inverse.**乘以`A @ A.inverse_2x2()`现在我们可以通过两个不同的2x2矩阵来测试,然后确认我们得到了身份矩阵.
   **验证逆矩阵。**将`A @ A.inverse_2x2()`乘,确认得到单位矩阵. 尝试三个不同的2x2矩阵.

2. **Implement 3x3 inverse.**通过结方法,将矩阵类扩展到计算3x3矩阵的逆数.`np.linalg.inv`现在,我们要去.
   **实现 3x3 逆矩阵。**用随矩阵法扩展矩阵类,与NumPy的结果对比

3. **Build a two-layer network.**通过使用您的矩阵类 (没有NumPy),创建一个两个层神经网络:输入 (3) ->隐藏 (4) ->输出 (2). 启动随机权重,运行前进传递,并验证所有形状是正确的.
   **构建双层网络。**仅使用矩阵类型 (不用编号),创建输入 (3) ->隐藏 (4) ->输出 (2) 的网络,运行前向传播并验证形状――

## 关键词 关键词

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

## 继续阅读 继续阅读

- [3Blue1Brown: Essence of Linear Algebra](https://www.3blue1brown.com/topics/linear-algebra)- 视觉直觉对于每一个操作
- [NumPy documentation on broadcasting](https://numpy.org/doc/stable/user/basics.broadcasting.html)- 准确的规则
- [Stanford CS229 Linear Algebra Review](http://cs229.stanford.edu/section/cs229-linalg.pdf)- 简要参考 ML 特定线性代数
