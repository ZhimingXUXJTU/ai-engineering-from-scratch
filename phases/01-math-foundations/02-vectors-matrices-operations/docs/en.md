# Vectors, Matrices & Operations | 向量、矩阵与运算

> Every neural network is just matrix multiplication with extra steps.

**Type:** Build
**Languages:** Python, Julia
**Prerequisites:** Phase 1, Lesson 01 (Linear Algebra Intuition)
**Time:** ~60 minutes

## Learning Objectives | 学习目标

- Build a Matrix class with element-wise operations, matrix multiplication, transpose, determinant, and inverse
- Distinguish element-wise multiplication from matrix multiplication and explain when each applies
- Implement a single dense neural network layer (`relu(W @ x + b)`) using only the from-scratch Matrix class
- Explain broadcasting rules and how bias addition works in neural network frameworks

> **【中文解读】**
> 每个神经网络的核心就是矩阵乘法。向量表示数据（如一个词、一张图片），矩阵表示变换（如一层神经网络权重）。本章从零构建向量类和矩阵类，帮你彻底理解 `output = relu(W @ x + b)` 这行代码背后的数学。

> **【拓展：向量/矩阵在 AI 中的位置】**
> - **词嵌入（Word Embedding）**: 每个词被表示为一个高维向量（如 300 维），语义相近的词在向量空间中距离更近。这是 NLP 的基础。
> - **神经网络权重**: 每一层的权重就是一个矩阵，输入向量乘以权重矩阵得到输出向量。
> - **Transformer 的注意力机制**: 本质上是 Q、K、V 三个矩阵的乘法和 Softmax 运算。

## The Problem | 问题描述

You want to build a neural network. You read the code and see this:

```
output = activation(weights @ input + bias)
```

That `@` is matrix multiplication. The `weights` are a matrix. The `input` is a vector. If you do not know what those operations do, this line is magic. If you do know, it is the entire forward pass of a layer in three operations.

Every image your model processes is a matrix of pixel values. Every word embedding is a vector. Every layer of every neural network is a matrix transformation. You cannot build AI systems without being fluent in matrix operations the same way you cannot write code without understanding variables.

This lesson builds that fluency from scratch.

> **【中文解读】**
> `output = activation(weights @ input + bias)` 这行代码就是神经网络一层的前向传播。如果你不懂矩阵乘法，它看起来像魔法；如果你懂，它就是三个基本操作。

## The Concept | 核心概念

### Vectors: ordered lists of numbers | 向量：有序数字列表

A vector is a list of numbers with a direction and magnitude. In AI, vectors represent data points, features, or parameters.

```
v = [3, 4]        -- a 2D vector # 二维向量
w = [1, 0, -2]    -- a 3D vector # 三维向量
```

A 2D vector `[3, 4]` points to coordinates (3, 4) on a plane. Its length (magnitude) is 5 (the 3-4-5 triangle).

### Matrices: grids of numbers | 矩阵：数字网格

A matrix is a 2D grid. Rows and columns. An m x n matrix has m rows and n columns.

```
A = | 1  2  3 |     -- 2x3 matrix (2 rows, 3 columns) # 2行3列矩阵
    | 4  5  6 |
```

In neural networks, weight matrices transform input vectors into output vectors. A layer with 784 inputs and 128 outputs uses a 128x784 weight matrix.

### Why shapes matter | 为什么形状很重要

Matrix multiplication has a strict rule: `(m x n) @ (n x p) = (m x p)`. The inner dimensions must match.

```
(128 x 784) @ (784 x 1) = (128 x 1)
  weights       input       output # 权重矩阵 × 输入向量 = 输出向量

Inner dimensions: 784 = 784  -- valid # 内部维度必须匹配
```

If you get a shape mismatch error in PyTorch, this is why.

> **【中文解读】**
> 矩阵乘法的形状规则：(m x n) @ (n x p) = (m x p)。内部维度必须一致。你在 PyTorch 中遇到 "shape mismatch" 错误时，99% 的原因是这个规则被违反了。

### The operations map | 运算对照表

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

### Element-wise vs matrix multiplication

This distinction trips up beginners constantly.

Element-wise: multiply matching positions. Both matrices must be the same shape.

```
| 1  2 |   | 5  6 |   | 5  12 |
| 3  4 | * | 7  8 | = | 21 32 |
```

Matrix multiplication: dot products of rows and columns. Inner dimensions must match.

```
| 1  2 |   | 5  6 |   | 1*5+2*7  1*6+2*8 |   | 19  22 |
| 3  4 | @ | 7  8 | = | 3*5+4*7  3*6+4*8 | = | 43  50 |
```

Different operations, different results, different rules.

### Broadcasting

When you add a bias vector to a matrix of outputs, the shapes do not match. Broadcasting stretches the smaller array to fit.

```
| 1  2  3 |   +   [10, 20, 30]
| 4  5  6 |

Broadcasting stretches the vector across rows:

| 1  2  3 |   | 10  20  30 |   | 11  22  33 |
| 4  5  6 | + | 10  20  30 | = | 14  25  36 |
```

Every modern framework does this automatically. Understanding it prevents confusion when shapes seem wrong but the code runs.

## Build It

### Step 1: Vector class

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
        return sum(a * b for a, b in zip(self.data, other.data))

    def magnitude(self):
        return sum(x ** 2 for x in self.data) ** 0.5
```

### Step 2: Matrix class with core operations

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

### Step 3: See it work

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

### Step 4: Connect to neural networks | 连接到神经网络

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

This is a single dense layer: `output = relu(W @ x + b)`. Every dense layer in every neural network does exactly this.

> **【中文解读】**
> 这就是神经网络全连接层的完整实现：线性变换（W @ x + b）+ 非线性激活（ReLU）。无论是 1 层还是 100 层的网络，每一层都在做同样的事情。

## Use It

NumPy does everything above in fewer lines and orders of magnitude faster.

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

The `@` operator in Python calls `__matmul__`. NumPy implements it with optimized BLAS routines written in C and Fortran. Same math, 100x faster.

Broadcasting in NumPy:

```python
matrix = np.array([[1, 2, 3], [4, 5, 6]])
bias = np.array([10, 20, 30])
print(matrix + bias)
```

NumPy automatically broadcasts the 1D bias across both rows. This is how bias addition works in every neural network framework.

## Ship It

This lesson produces a prompt for teaching matrix operations through geometric intuition. See `outputs/prompt-matrix-operations.md`.

The Matrix class built here is the foundation for the mini neural network framework we build in Phase 3, Lesson 10.

## Exercises | 练习题

1. **Verify the inverse.** Multiply `A @ A.inverse_2x2()` and confirm you get the identity matrix. Try it with three different 2x2 matrices. What happens when the determinant is zero?
   **验证逆矩阵。** 将 `A @ A.inverse_2x2()` 相乘，确认得到单位矩阵。尝试三个不同的 2x2 矩阵。行列式为零时会怎样？

2. **Implement 3x3 inverse.** Extend the Matrix class to compute inverses for 3x3 matrices using the adjugate method. Test it against NumPy's `np.linalg.inv`.
   **实现 3x3 逆矩阵。** 用伴随矩阵法扩展 Matrix 类，与 NumPy 的结果对比。

3. **Build a two-layer network.** Using only your Matrix class (no NumPy), create a two-layer neural network: input (3) -> hidden (4) -> output (2). Initialize random weights, run a forward pass, and verify all shapes are correct.
   **构建双层网络。** 只用 Matrix 类（不用 NumPy），创建输入(3)->隐藏(4)->输出(2)的网络，运行前向传播并验证形状。

## Key Terms | 关键术语

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

## Further Reading

- [3Blue1Brown: Essence of Linear Algebra](https://www.3blue1brown.com/topics/linear-algebra) - visual intuition for every operation covered here
- [NumPy documentation on broadcasting](https://numpy.org/doc/stable/user/basics.broadcasting.html) - the exact rules NumPy follows
- [Stanford CS229 Linear Algebra Review](http://cs229.stanford.edu/section/cs229-linalg.pdf) - concise reference for ML-specific linear algebra
