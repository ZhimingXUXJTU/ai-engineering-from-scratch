# Matrix Transformations | 矩阵变换

> A matrix is a machine that reshapes space. Learn what it does to every point, and you understand the whole transformation.

> 矩阵是一台"重塑空间"的机器。理解它对每个点的作用，就理解了整个变换。

**Type:** Build | **类型:** 动手
**Languages:** Python, Julia | **语言:** Python, Julia
**Prerequisites:** Phase 1, Lessons 01-02 (Linear Algebra Intuition, Vectors & Matrices Operations) | **前置知识:** Phase 1, Lessons 01-02（线性代数直觉、向量与矩阵运算）
**Time:** ~75 minutes | **时间:** ~75 分钟

## Learning Objectives | 学习目标

- Construct rotation, scaling, shearing, and reflection matrices and apply them to 2D and 3D points
  构造旋转、缩放、剪切、反射矩阵并应用于 2D 和 3D 点
- Compose multiple transformations by matrix multiplication and verify that order matters
  通过矩阵乘法组合多个变换，验证顺序的重要性
- Compute eigenvalues and eigenvectors of 2x2 matrices from the characteristic equation
  从特征方程计算 2x2 矩阵的特征值和特征向量
- Explain why eigenvalues determine PCA directions, RNN stability, and spectral clustering behavior
  解释特征值为何决定 PCA 方向、RNN 稳定性和谱聚类行为

> **【中文解读】**
> 矩阵是对空间的变换——旋转、缩放、剪切、翻转。理解矩阵的几何意义后，PCA、RNN 稳定性、谱聚类这些概念就变得直观了。

> **【拓展：特征值/特征向量在 AI 中的位置】**
> - **PCA（主成分分析）**: 找到数据协方差矩阵的特征向量，就是数据方差最大的方向。
> - **RNN 稳定性**: 如果权重矩阵的特征值绝对值大于 1，梯度会指数增长（梯度爆炸）；小于 1 则会衰减到零（梯度消失）。
> - **谱聚类**: 用图拉普拉斯矩阵的特征向量进行聚类，比 K-Means 更适合非球形数据。

## The Problem | 问题引入

> **【中文解读】** PCA 说"找协方差矩阵的特征向量"，模型稳定性说"检查特征值是否小于 1"，数据增强说"随机旋转"——这些都需要理解矩阵对空间的几何变换。矩阵不是数字表格，而是"空间机器"：旋转、缩放、剪切。神经网络每一层都在对数据做这些变换。

## The Concept | 核心概念

> **【拓展：Transformer 中的矩阵变换】** Transformer 的每个注意力头都在做矩阵变换：Q=W_q·x, K=W_k·x, V=W_v·x，其中 W_q/W_k/W_v 是可学习的变换矩阵。模型训练的过程就是自动学习"最优变换"的过程。理解矩阵的几何意义，就能理解 Transformer 如何把输入序列映射到语义空间。

### Transformations as matrices

Every linear transformation in 2D can be written as a 2x2 matrix. The matrix tells you exactly where the basis vectors [1, 0] and [0, 1] end up. Everything else follows.

> 二维空间中的每个线性变换都可以写成一个 2x2 矩阵。矩阵告诉你基向量 [1, 0] 和 [0, 1] 变到了哪里，其余一切由此决定。

> 矩阵的列就是变换后的基向量。如果矩阵第一列是 [2, 0]，说明 e1=[1,0] 被映射到 [2,0]（沿 x 轴拉伸 2 倍）。

```mermaid
graph LR
    subgraph Before["Standard Basis"]
        e1["e1 = [1, 0] (along x)"]
        e2["e2 = [0, 1] (along y)"]
    end
    subgraph Transform["Matrix M"]
        M["M = columns are new basis vectors"]
    end
    subgraph After["After Transformation M"]
        e1p["e1' = new x-basis"]
        e2p["e2' = new y-basis"]
    end
    e1 --> M --> e1p
    e2 --> M --> e2p
```

### Rotation

A 2D rotation by angle theta keeps distances and angles intact. It moves every point along a circular arc.

> 二维旋转保持距离和角度不变，将每个点沿圆弧移动。

> 旋转矩阵 R(θ) = [[cosθ, -sinθ], [sinθ, cosθ]]。θ 为正表示逆时针旋转。R^T = R^(-1)，转置即逆旋转。

```mermaid
graph LR
    subgraph Before["Before Rotation"]
        A["A(2, 1)"]
        B["B(0, 2)"]
    end
    subgraph Rot["Rotate 45 degrees"]
        R["R(θ) = [[cos θ, -sin θ], [sin θ, cos θ]]"]
    end
    subgraph After["After Rotation"]
        Ap["A'(0.71, 2.12)"]
        Bp["B'(-1.41, 1.41)"]
    end
    A --> R --> Ap
    B --> R --> Bp
```

In 3D, you rotate around an axis. Each axis has its own rotation matrix:

> 在三维空间中，你围绕某个轴旋转。每个轴有自己的旋转矩阵：

```
Rz(theta) = | cos  -sin  0 |     Rotate around z-axis
            | sin   cos  0 |     (x-y plane spins, z stays)
            |  0     0   1 |

Rx(theta) = | 1   0     0    |   Rotate around x-axis
            | 0  cos  -sin   |   (y-z plane spins, x stays)
            | 0  sin   cos   |

Ry(theta) = |  cos  0  sin |     Rotate around y-axis
            |   0   1   0  |     (x-z plane spins, y stays)
            | -sin  0  cos |
```

### Scaling

Scaling stretches or compresses along each axis independently.

> 缩放沿每个轴独立地拉伸或压缩。

> 缩放矩阵 S = [[sx, 0], [0, sy]]。sx、sy 可以不同。如果某个为负，等价于沿该轴反射。

```mermaid
graph LR
    subgraph Before["Before Scaling"]
        A["A(2, 1)"]
        B["B(0, 2)"]
    end
    subgraph Scale["Scale sx=2, sy=0.5"]
        S["S = [[2, 0], [0, 0.5]]"]
    end
    subgraph After["After Scaling"]
        Ap["A'(4, 0.5)"]
        Bp["B'(0, 1)"]
    end
    A --> S --> Ap
    B --> S --> Bp
```

### Shearing

Shearing tilts one axis while keeping the other fixed. It turns rectangles into parallelograms.

> 剪切使一个轴倾斜而保持另一个轴固定，将矩形变成平行四边形。

> 剪切保持面积不变（行列式=1）。想象一摞扑克牌向一边推：底牌不动，顶牌平移。

```mermaid
graph LR
    subgraph Before["Before Shear"]
        A["A(1, 0)"]
        B["B(0, 1)"]
    end
    subgraph Shear["Shear in x, k=1"]
        Sh["Shx = [[1, k], [0, 1]]"]
    end
    subgraph After["After Shear"]
        Ap["A(1, 0) unchanged"]
        Bp["B'(1, 1) shifted"]
    end
    A --> Sh --> Ap
    B --> Sh --> Bp
```

Shear matrices:
- `Shx = [[1, k], [0, 1]]` shifts x by k * y
- `Shy = [[1, 0], [k, 1]]` shifts y by k * x

> 剪切矩阵：`Shx` 沿 y 偏移 x（x 新 = x + k*y），`Shy` 沿 x 偏移 y（y 新 = y + k*x）。

### Reflection

Reflection mirrors points across an axis or line.

> 反射将点关于某条轴或线做镜像。

> 反射改变方向（行列式=-1）但保持距离。任何正交矩阵的行列式要么 +1（旋转）要么 -1（含反射）。

```mermaid
graph LR
    subgraph Before["Before Reflection"]
        A["A(2, 1)"]
    end
    subgraph Reflect["Reflect across y-axis"]
        R["[[-1, 0], [0, 1]]"]
    end
    subgraph After["After Reflection"]
        Ap["A'(-2, 1)"]
    end
    A --> R --> Ap
```

Reflection matrices:
- Reflect across y-axis: `[[-1, 0], [0, 1]]`
- Reflect across x-axis: `[[1, 0], [0, -1]]`

> 反射矩阵：关于 y 轴反射 `[[-1, 0], [0, 1]]`，关于 x 轴反射 `[[1, 0], [0, -1]]`。

### Composition: chaining transformations

Applying transformation A then B is the same as multiplying their matrices: `result = B @ A @ point`. Order matters. Rotate then scale gives different results than scale then rotate.

> 先做变换 A 再做变换 B 等于乘以它们的矩阵：`result = B @ A @ point`。顺序很重要——先旋转再缩放与先缩放再旋转结果不同。

> 这就是为什么 PyTorch 中的 nn.Sequential 严格按顺序应用模块，且矩阵乘法顺序在反向传播中通过转置自动反转。

```mermaid
graph LR
    subgraph Path1["Rotate 90 then Scale (2, 0.5)"]
        P1["(1, 0)"] -->|"Rotate 90"| P2["(0, 1)"] -->|"Scale"| P3["(0, 0.5)"]
    end
```

Composed: `S @ R = [[0, -2], [0.5, 0]]`

> 先旋转 90° 再缩放 (2, 0.5)：从 (1,0) → 旋转后 (0,1) → 缩放后 (0, 0.5)。组合矩阵 S @ R = [[0, -2], [0.5, 0]]。

```mermaid
graph LR
    subgraph Path2["Scale (2, 0.5) then Rotate 90"]
        Q1["(1, 0)"] -->|"Scale"| Q2["(2, 0)"] -->|"Rotate 90"| Q3["(0, 2)"]
    end
```

Composed: `R @ S = [[0, -0.5], [2, 0]]`

> 先缩放 (2, 0.5) 再旋转 90°：从 (1,0) → 缩放后 (2, 0) → 旋转后 (0, 2)。组合矩阵 R @ S = [[0, -0.5], [2, 0]]，与上面完全不同。

Different results. Matrix multiplication is not commutative.

> 结果不同。矩阵乘法不满足交换律——这就是为什么 Transformer 注意力中 Q、K、V 的相乘顺序至关重要。

### Eigenvalues and eigenvectors

Most vectors change direction when a matrix hits them. Eigenvectors are special: the matrix only scales them, never rotates them. The scaling factor is the eigenvalue.

> 大多数向量被矩阵变换后会改变方向。特征向量是特殊的：矩阵只对它做缩放，不旋转。缩放倍数就是特征值。

> 几何直觉：特征向量是变换中"方向不变"的方向。如果矩阵是椭圆变换，特征向量指向椭圆的长短轴。

```
A @ v = lambda * v

v is the eigenvector (direction that survives)
lambda is the eigenvalue (how much it stretches)

Example: A = | 2  1 |
             | 1  2 |

Eigenvector [1, 1] with eigenvalue 3:
  A @ [1,1] = [3, 3] = 3 * [1, 1]     (same direction, scaled by 3)

Eigenvector [1, -1] with eigenvalue 1:
  A @ [1,-1] = [1, -1] = 1 * [1, -1]  (same direction, unchanged)
```

The matrix stretches space by 3x along [1, 1] and keeps [1, -1] unchanged. Every other direction is a mix of these two.

> 该矩阵沿 [1, 1] 方向拉伸 3 倍，保持 [1, -1] 方向不变。其他所有方向都是这两个方向的组合。

### Eigendecomposition

If a matrix has n linearly independent eigenvectors, it can be decomposed:

> 如果矩阵有 n 个线性无关的特征向量，它可以分解为 A = V D V⁻¹。

> 特征分解的几何意义：把任意变换拆解为"旋转到特征向量坐标系 → 沿轴缩放 → 旋转回来"三步。这就是 PCA 的核心数学。

```
A = V @ D @ V^(-1)

V = matrix whose columns are eigenvectors
D = diagonal matrix of eigenvalues
V^(-1) = inverse of V

This says: rotate into eigenvector coordinates, scale along each axis, rotate back.
```

> 这意味着：旋转到特征向量坐标系，沿每个轴缩放，再旋转回来。

### Why eigenvalues matter

**PCA.** The eigenvectors of the covariance matrix are the principal components. The eigenvalues tell you how much variance each component captures. Sort by eigenvalue, keep the top k, and you have dimensionality reduction.

> **PCA（主成分分析）。** 协方差矩阵的特征向量就是主成分，特征值告诉你每个主成分捕获了多少方差。按特征值排序，保留前 k 个，就完成了降维。

**Stability.** In recurrent networks and dynamical systems, eigenvalues with magnitude > 1 cause outputs to explode. Magnitude < 1 causes them to vanish. This is the vanishing/exploding gradient problem stated in one sentence.

> **稳定性。** 在循环网络和动力系统中，特征值绝对值 > 1 导致输出爆炸，< 1 导致消失。这就是梯度爆炸/消失问题。

**Spectral methods.** Graph neural networks use eigenvalues of the adjacency matrix. Spectral clustering uses eigenvalues of the Laplacian. The eigenvectors reveal the structure of the graph.

> **谱方法。** 图神经网络使用邻接矩阵的特征值，谱聚类使用拉普拉斯矩阵的特征值。特征向量揭示了图的结构。

### Determinant as volume scaling factor

The determinant of a transformation matrix tells you how much it scales area (2D) or volume (3D).

> 变换矩阵的行列式告诉你它缩放面积（2D）或体积（3D）的程度。

> det=0 是"灾难"——矩阵把空间压缩到低维（如 2D → 1D 线），信息丢失，矩阵不可逆。神经网络初始化时要避免权重矩阵接近奇异。

```
det = 1:   area preserved (rotation)
det = 2:   area doubled
det = 0:   space crushed to lower dimension (singular)
det = -1:  area preserved but orientation flipped (reflection)

| det(Rotation) | = 1        (always)
| det(Scale sx, sy) | = sx * sy
| det(Shear) | = 1           (area preserved)
| det(Reflection) | = -1     (orientation flipped)
```

> 行列式含义：det=1 保面积（旋转）；det=2 面积翻倍；det=0 空间塌缩到低维（奇异，矩阵不可逆）；det=-1 保面积但翻转方向（反射）。

## Build It | 动手实现

### Step 1: Transformation matrices from scratch (Python)

> 第1步：从零实现变换矩阵

> 从零实现旋转、缩放、剪切、反射矩阵。所有变换都是 2x2 矩阵。还实现 mat_vec_mul 和 mat_mul 用于变换向量和组合变换。

```python
import math

def rotation_2d(theta):
    c, s = math.cos(theta), math.sin(theta)
    return [[c, -s], [s, c]]

def scaling_2d(sx, sy):
    return [[sx, 0], [0, sy]]

def shearing_2d(kx, ky):
    return [[1, kx], [ky, 1]]

def reflection_x():
    return [[1, 0], [0, -1]]

def reflection_y():
    return [[-1, 0], [0, 1]]

def mat_vec_mul(matrix, vector):
    return [
        sum(matrix[i][j] * vector[j] for j in range(len(vector)))
        for i in range(len(matrix))
    ]

def mat_mul(a, b):
    rows_a, cols_b = len(a), len(b[0])
    cols_a = len(a[0])
    return [
        [sum(a[i][k] * b[k][j] for k in range(cols_a)) for j in range(cols_b)]
        for i in range(rows_a)
    ]

point = [1.0, 0.0]
angle = math.pi / 4

rotated = mat_vec_mul(rotation_2d(angle), point)
print(f"Rotate (1,0) by 45 deg: ({rotated[0]:.4f}, {rotated[1]:.4f})")

scaled = mat_vec_mul(scaling_2d(2, 3), [1.0, 1.0])
print(f"Scale (1,1) by (2,3): ({scaled[0]:.1f}, {scaled[1]:.1f})")

sheared = mat_vec_mul(shearing_2d(1, 0), [1.0, 1.0])
print(f"Shear (1,1) kx=1: ({sheared[0]:.1f}, {sheared[1]:.1f})")

reflected = mat_vec_mul(reflection_y(), [2.0, 1.0])
print(f"Reflect (2,1) across y: ({reflected[0]:.1f}, {reflected[1]:.1f})")
```

### Step 2: Composition of transformations

> 第2步：变换的组合

> 验证矩阵乘法不可交换：先旋转 90° 再缩放 (2, 0.5) 与先缩放再旋转得到完全不同的结果。这解释了为什么 PyTorch nn.Sequential 中层顺序至关重要。

```python
R = rotation_2d(math.pi / 2)
S = scaling_2d(2, 0.5)

rotate_then_scale = mat_mul(S, R)
scale_then_rotate = mat_mul(R, S)

point = [1.0, 0.0]
result1 = mat_vec_mul(rotate_then_scale, point)
result2 = mat_vec_mul(scale_then_rotate, point)

print(f"Rotate 90 then scale: ({result1[0]:.2f}, {result1[1]:.2f})")
print(f"Scale then rotate 90: ({result2[0]:.2f}, {result2[1]:.2f})")
print(f"Same? {result1 == result2}")
```

> 验证：先旋转后缩放，结果与先缩放后旋转不同。这就是矩阵乘法不可交换律——B@A ≠ A@B。在神经网络中，这意味着层的顺序至关重要。

### Step 3: Eigenvalues from scratch (2x2)

> 第3步：从零计算特征值

> 2x2 矩阵的特征值通过解二次方程 λ² - trace·λ + det = 0 得到，其中 trace=a+d，det=ad-bc。特征向量通过 (A - λI)v = 0 求解。

For a 2x2 matrix `[[a, b], [c, d]]`, eigenvalues solve the characteristic equation: `lambda^2 - (a+d)*lambda + (ad - bc) = 0`.

> 对 2x2 矩阵 `[[a, b], [c, d]]`，特征值满足特征方程 λ² - (a+d)λ + (ad-bc) = 0。其中 (a+d) 是迹（trace），(ad-bc) 是行列式。

```python
def eigenvalues_2x2(matrix):
    a, b = matrix[0]
    c, d = matrix[1]
    trace = a + d
    det = a * d - b * c
    discriminant = trace ** 2 - 4 * det
    if discriminant < 0:
        real = trace / 2
        imag = (-discriminant) ** 0.5 / 2
        return (complex(real, imag), complex(real, -imag))
    sqrt_disc = discriminant ** 0.5
    return ((trace + sqrt_disc) / 2, (trace - sqrt_disc) / 2)

def eigenvector_2x2(matrix, eigenvalue):
    a, b = matrix[0]
    c, d = matrix[1]
    if abs(b) > 1e-10:
        v = [b, eigenvalue - a]
    elif abs(c) > 1e-10:
        v = [eigenvalue - d, c]
    else:
        if abs(a - eigenvalue) < 1e-10:
            v = [1, 0]
        else:
            v = [0, 1]
    mag = (v[0] ** 2 + v[1] ** 2) ** 0.5
    return [v[0] / mag, v[1] / mag]

A = [[2, 1], [1, 2]]
vals = eigenvalues_2x2(A)
print(f"Matrix: {A}")
print(f"Eigenvalues: {vals[0]:.4f}, {vals[1]:.4f}")

for val in vals:
    vec = eigenvector_2x2(A, val)
    result = mat_vec_mul(A, vec)
    scaled = [val * vec[0], val * vec[1]]
    print(f"  lambda={val:.1f}, v={[round(x,4) for x in vec]}")
    print(f"    A@v = {[round(x,4) for x in result]}")
    print(f"    l*v = {[round(x,4) for x in scaled]}")
```

> 验证 A=[[2,1],[1,2]] 的特征值是 3 和 1，对应特征向量 [1,1]/√2 和 [1,-1]/√2。验证 A@v = λ×v 成立。

### Step 4: Determinant as volume scaling factor

> 第4步：行列式作为体积缩放因子

```python
def det_2x2(matrix):
    return matrix[0][0] * matrix[1][1] - matrix[0][1] * matrix[1][0]

print(f"det(rotation 45) = {det_2x2(rotation_2d(math.pi/4)):.4f}")
print(f"det(scale 2,3)   = {det_2x2(scaling_2d(2, 3)):.1f}")
print(f"det(shear kx=1)  = {det_2x2(shearing_2d(1, 0)):.1f}")
print(f"det(reflect y)   = {det_2x2(reflection_y()):.1f}")

singular = [[1, 2], [2, 4]]
print(f"det(singular)     = {det_2x2(singular):.1f}")
print("Singular: columns are proportional, space collapses to a line.")
```

> 奇异矩阵示例：[[1, 2], [2, 4]] 的行列式为 0，因为两行成比例。空间被压缩到一条线，变换不可逆。

## Use It | 用框架实现

NumPy handles all of this with optimized routines.

> NumPy 用优化过的例程处理所有这些操作。

> NumPy 的 `np.linalg.eig` 和 `np.linalg.det` 底层调用 LAPACK（C/Fortran 写的线性代数库），比手写 Python 快 100-1000 倍。

```python
import numpy as np

theta = np.pi / 4
R = np.array([[np.cos(theta), -np.sin(theta)],
              [np.sin(theta),  np.cos(theta)]])

point = np.array([1.0, 0.0])
print(f"Rotate (1,0) by 45 deg: {R @ point}")

S = np.diag([2.0, 3.0])
composed = S @ R
print(f"Scale(2,3) after Rotate(45): {composed @ point}")

A = np.array([[2, 1], [1, 2]], dtype=float)
eigenvalues, eigenvectors = np.linalg.eig(A)
print(f"\nEigenvalues: {eigenvalues}")
print(f"Eigenvectors (columns):\n{eigenvectors}")

for i in range(len(eigenvalues)):
    v = eigenvectors[:, i]
    lam = eigenvalues[i]
    print(f"  A @ v{i} = {A @ v}, lambda * v{i} = {lam * v}")

print(f"\ndet(R) = {np.linalg.det(R):.4f}")
print(f"det(S) = {np.linalg.det(S):.1f}")

B = np.array([[3, 1], [0, 2]], dtype=float)
vals, vecs = np.linalg.eig(B)
D = np.diag(vals)
V = vecs
reconstructed = V @ D @ np.linalg.inv(V)
print(f"\nEigendecomposition A = V @ D @ V^-1:")
print(f"Original:\n{B}")
print(f"Reconstructed:\n{reconstructed}")
```

> 特征分解验证：A = V @ D @ V⁻¹ 应能完美重建原矩阵。这证明了任何可对角化矩阵都能分解为"旋转 → 缩放 → 旋转回来"三步。

### 3D rotations with NumPy

```python
def rotation_3d_z(theta):
    c, s = np.cos(theta), np.sin(theta)
    return np.array([[c, -s, 0], [s, c, 0], [0, 0, 1]])

def rotation_3d_x(theta):
    c, s = np.cos(theta), np.sin(theta)
    return np.array([[1, 0, 0], [0, c, -s], [0, s, c]])

point_3d = np.array([1.0, 0.0, 0.0])
rotated_z = rotation_3d_z(np.pi / 2) @ point_3d
rotated_x = rotation_3d_x(np.pi / 2) @ point_3d

print(f"\n3D point: {point_3d}")
print(f"Rotate 90 around z: {np.round(rotated_z, 4)}")
print(f"Rotate 90 around x: {np.round(rotated_x, 4)}")
```

> NumPy 实现 3D 旋转矩阵：绕 z 轴和绕 x 轴各有独立的 3x3 旋转矩阵。3D 图形学、机器人学、计算机视觉都依赖这些矩阵。

## Ship It | 产出物

This lesson builds the geometric foundation for PCA (Phase 2) and neural network weight analysis. The eigenvalue/eigenvector code built here is the same algorithm that powers dimensionality reduction, spectral clustering, and stability analysis in production ML systems.

> 本课构建了 PCA（Phase 2）和神经网络权重分析的几何基础。这里的特征值/特征向量代码与生产 ML 系统中的降维、谱聚类和稳定性分析使用相同的算法。

> 本课产出：从零实现的变换矩阵库 + 特征值/特征向量求解器。代码可以直接用于理解 PCA、谱聚类、GNN 谱方法等高级主题。

## Exercises | 练习题

1. Apply rotation, scaling, and shearing to a unit square (corners at [0,0], [1,0], [1,1], [0,1]). Print the transformed corners for each. Verify that rotation preserves distances between corners.
   对单位正方形（角在 [0,0]、[1,0]、[1,1]、[0,1]）应用旋转、缩放、剪切。打印每个变换后的角。验证旋转保持角之间距离不变。

2. Find the eigenvalues of the matrix [[4, 2], [1, 3]] by hand using the characteristic equation. Then verify with your from-scratch function and with NumPy.
   手工用特征方程求矩阵 [[4, 2], [1, 3]] 的特征值，然后用从零实现的函数和 NumPy 验证。

3. Create a composition of three transformations (rotate 30 degrees, scale by [1.5, 0.8], shear with kx=0.3) and apply it to 8 points arranged in a circle. Print before and after coordinates. Compute the determinant of the composed matrix and verify it equals the product of the individual determinants.
   组合三个变换（旋转 30°、缩放 [1.5, 0.8]、剪切 kx=0.3），应用到圆上的 8 个点。打印前后坐标。计算组合矩阵的行列式，验证它等于各自行列式的乘积。

## Key Terms | 术语速查表

| Term | What people say | What it actually means |
|------|----------------|----------------------|
| Rotation matrix | "Spins things" | An orthogonal matrix that moves points along circular arcs while preserving distances and angles. Determinant is always 1. |
| Scaling matrix | "Makes things bigger" | A diagonal matrix that stretches or compresses independently along each axis. Determinant is the product of scale factors. |
| Shearing matrix | "Slants things" | A matrix that shifts one coordinate proportionally to another, turning rectangles into parallelograms. Determinant is 1. |
| Reflection | "Mirrors things" | A matrix that flips space across an axis or plane. Determinant is -1. |
| Composition | "Do two things" | Multiplying transformation matrices to chain operations. Order matters: B @ A means apply A first, then B. |
| Eigenvector | "Special direction" | A direction that the matrix only scales, never rotates. The transformation's fingerprint. |
| Eigenvalue | "How much it stretches" | The scalar factor by which the matrix scales its eigenvector. Can be negative (flip) or complex (rotation). |
| Eigendecomposition | "Break the matrix apart" | Writing a matrix as V @ D @ V^(-1), separating it into its fundamental scaling directions and magnitudes. |
| Determinant | "A single number from a matrix" | The factor by which the transformation scales area (2D) or volume (3D). Zero means the transformation is irreversible. |
| Characteristic equation | "Where eigenvalues come from" | det(A - lambda * I) = 0. The polynomial whose roots are the eigenvalues. |

> 术语速查：Rotation matrix（旋转矩阵，正交，行列式=1）、Scaling matrix（缩放矩阵，对角）、Shearing（剪切，矩形→平行四边形）、Reflection（反射，行列式=-1）、Composition（组合，B@A 表示先 A 后 B）、Eigenvector（特征向量，只缩放不旋转的方向）、Eigenvalue（特征值，缩放倍数，可为负或复数）、Eigendecomposition（特征分解 A=VDV⁻¹）、Determinant（行列式，面积/体积缩放因子，0 = 奇异）、Characteristic equation（特征方程 det(A-λI)=0）。

## Further Reading | 延伸阅读

- [3Blue1Brown: Linear Transformations](https://www.3blue1brown.com/lessons/linear-transformations) -- visual intuition for how matrices reshape space
- [3Blue1Brown: Eigenvectors and Eigenvalues](https://www.3blue1brown.com/lessons/eigenvalues) -- the best visual explanation of what eigenvectors mean geometrically
- [MIT 18.06 Lecture 21: Eigenvalues and Eigenvectors](https://ocw.mit.edu/courses/18-06-linear-algebra-spring-2010/) -- Gilbert Strang's classic treatment
