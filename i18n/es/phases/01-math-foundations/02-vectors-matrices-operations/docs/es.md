# Vectores, matrices y operaciones

> Cada red neuronal es sólo una multiplicación de matriz con pasos adicionales.

> Cada red neuronal es en esencia una matriz multiplicada por varios pasos adicionales.

**Type:** Build | **类型:** 动手
**Languages:** Python, Julia | **语言:** Python, Julia
**Prerequisites:** Phase 1, Lesson 01 (Linear Algebra Intuition) | **前置知识:** Phase 1, Lesson 01 (线性代数直觉)
**Time:** ~60 minutes | **时间:** ~60 分钟

## Objetivos de aprendizaje

- Construir una clase de Matrix con operaciones de elementos, multiplicación de matriz, transposición, determinante y inversa
  构建包含逐元素运算、矩阵乘法、转置、行列式、逆矩阵的矩阵类 类
- Distinguir la multiplicación por elemento de la multiplicación por matriz y explicar cuándo cada uno se aplica
  区分分分分元素乘法和矩阵乘法, explicar sus respectivos escenarios de aplicación
- Implementar una sola capa de red neuronal densa (`relu(W @ x + b)`) utilizando únicamente la clase Matrix desde cero
   Sólo con la matriz                                                                                                                                                                                                                                                            `relu(W @ x + b)`(en inglés)
- Explicar las reglas de radiodifusión y cómo funciona la adición de sesgos en los marcos de redes neuronales
  解释广播规则和神经网络框架中偏置加法的工作方式 解释广播规则和神经网络框架中偏置加法的工作方式

> **【中文解读】**
> El núcleo de cada red neuronal es la matriz multiplicada. La matriz representa datos, como una palabra, una imagen, la matriz representa cambios, como la carga de una red neuronal.`output = relu(W @ x + b)`Esta es la matemática detrás del código.

> **【拓展：向量/矩阵在 AI 中的位置】**
> - **词嵌入（Word Embedding）**Cada palabra se representa como un alto dimensionamiento (como 300 dimensiones), y el significado de un término es más cercano a la distancia en el espacio de dimensionamiento.
> - **神经网络权重**: El peso de cada capa es una matriz, la entrada de la matriz multiplicada por el peso de la matriz obtenga la salida de la matriz.
> - **Transformer 的注意力机制**En esencia es Q、K、V √3 y Softmax √√√¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬

## El problema es la introducción del problema

Si quieres construir una red neuronal, lee el código y ve esto:

> ¿Quieres construir una red neuronal?

```
output = activation(weights @ input + bias)
```

Eso es .`@`es la multiplicación de matriz.`weights`Es una matriz.`input`Si no sabes lo que hacen esas operaciones, esta línea es mágica. si lo sabes, es todo el paso hacia adelante de una capa en tres operaciones.

> `@`Es una forma de hacer.`weights`Es una rectangularidad.`input`Si no sabes qué hacer con estas operaciones, este código es magia. Si sabes, esto es la transmisión completa de una capa.

Cada imagen que procesas es una matriz de valores de píxeles. Cada palabra que se incorpora es un vector. Cada capa de cada red neuronal es una transformación de matriz. No puedes construir sistemas de IA sin ser fluido en las operaciones de matriz de la misma manera que no puedes escribir código sin entender variables.

> Cada imagen del modelo procesado es una matriz de imágenes, cada palabra está en un eje, cada capa de la red neuronal es una matriz de cambios.

Esta lección construye esa fluidez desde cero.

> Este curso comenzó a construir esta habilidad desde cero.

> **【中文解读】**
> `output = activation(weights @ input + bias)`Este código es el precursor de la transmisión de la red neuronal de una capa. Si no entiendes la matriz multiplicadora, parece magia; si lo entiendes, es tres operaciones básicas.

## El concepto central.

### Vectores: listas ordenadas de números.

Un vector es una lista de números con una dirección y magnitud. En IA, los vectores representan puntos de datos, características o parámetros.

> El vector es un conjunto de números directivos y grandes. En la IA, el vector representa puntos de datos, características o parámetros.

```
v = [3, 4]        -- a 2D vector # 二维向量
w = [1, 0, -2]    -- a 3D vector # 三维向量
```

Un vector 2D `[3, 4]`El punto de referencia es el punto de referencia de la longitud de un triángulo de 3 a 4 y el punto de referencia de la longitud de un triángulo de 3 a 5 (el triángulo de 3 a 4 a 5).

> 2 dimensiones`[3, 4]`Indicando el asiento en la superficie (3, 4), la longitud es de 5 ((勾股定理 3-4-5 三角形) ⋅

### Matrices: redes de números.

Una matriz es una cuadrícula 2D. filas y columnas.

> La matriz es de dos dimensiones, por la que se componen las filas.

```
A = | 1  2  3 |     -- 2x3 matrix (2 rows, 3 columns) # 2行3列矩阵
    | 4  5  6 |
```

En las redes neuronales, las matrices de peso transforman los vectores de entrada en vectores de salida.

> En la red neuronal, la matriz de peso se transformará en la entrada de velocidad de entrada y de salida. Una tiene 784 entradas y 128 salidas utilizando una matriz de peso de 128x784.

### ¿Por qué las formas importan ?

La multiplicación de matrices tiene una regla estricta:`(m x n) @ (n x p) = (m x p)`Las dimensiones internas deben coincidir.

> La regla de la forma tiene una estricta regla:`(m x n) @ (n x p) = (m x p)`, las dimensiones internas deben ser de acuerdo.

```
(128 x 784) @ (784 x 1) = (128 x 1)
  weights       input       output # 权重矩阵 × 输入向量 = 输出向量

Inner dimensions: 784 = 784  -- valid # 内部维度必须匹配
```

Si obtienes un error de desajuste de forma en PyTorch, es por esto.

> En PyTorch, el 99% de las razones por las que se ha encontrado una "incumplimiento de la forma" es porque esta regla ha sido violada.

> **【中文解读】**
> 矩阵乘法形状规则: ((m x n) @ (n x p) = (m x p) ・・・ dimensiones internas deben coincidir。 Usted en PyTorch en el centro se encuentra con "desajuste de forma" 错误时,99% de la causa es esta regla fue violada。

### El mapa de operaciones.

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

### El elemento-sabio vs. multiplicación de matriz

Esta distinción atraviesa a los principiantes constantemente.

> Esta diferencia a menudo deja a los principiantes confundidos.

El elemento-sabio: multiplicar las posiciones coinciden. Ambas matrices deben tener la misma forma.

> 逐元素乘法:对应位置相乘, dos matrices de forma deben ser iguales.`*`¿Qué es esto?

```
| 1  2 |   | 5  6 |   | 5  12 |
| 3  4 | * | 7  8 | = | 21 32 |
```

Multiplicación de matriz: productos de puntos de filas y columnas.

> 矩阵乘法:行与列做点积, dimensiones internas deben coincidir.`@`¿Qué es esto?

```
| 1  2 |   | 5  6 |   | 1*5+2*7  1*6+2*8 |   | 19  22 |
| 3  4 | @ | 7  8 | = | 3*5+4*7  3*6+4*8 | = | 43  50 |
```

Diferentes operaciones, diferentes resultados, diferentes reglas.

> Diferentes operaciones, diferentes resultados, diferentes reglas.`*`Y `@`En NumPy/PyTorch 中含义完全不同,混会导致 silencioso bug。

### La radiodifusión

Cuando se añade un vector de sesgo a una matriz de salidas, las formas no coinciden.

>  Mecanismo de difusión: Cuando la forma de la torsión de parámetro no coincide con la de la matriz de salida, la difusión se expande automáticamente a un número menor de grupos para adaptarse.

```
| 1  2  3 |   +   [10, 20, 30]
| 4  5  6 |

Broadcasting stretches the vector across rows:

| 1  2  3 |   | 10  20  30 |   | 11  22  33 |
| 4  5  6 | + | 10  20  30 | = | 14  25  36 |
```

Cada marco moderno hace esto automáticamente.

> Cada marco moderno se hace automáticamente. Comprender que puede evitar la confusión de "forma no es contra pero el código puede correr".

## Construye y realiza.
```figure
vector-projection
```

## Construye el mismo

### Paso 1: Clase de vectores

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

> Vector 类实现:加法/减法是逐元素运算;标量乘法扩展到每个分量;点是积点;对应分量乘积之和;大小是模长;√√√ x2+y2+...))。

### Paso 2: Clase de matriz con operaciones centrales

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

> Matrix 类核心操作:matmul 是矩阵乘法(行×列做点积);transpose 行列互换;determinante 用递归拉普拉斯展开;inverse_2x2 用 (1/det) × [[d,-b],[-c,a]];identidad 创建单位矩阵。

### Paso 3: Vean cómo funciona

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

> 验证矩阵 类:A+B、A@B、A^T、det(A)、A−1 都正确──最关键的验证是A @ A−1 = I(单位矩阵), esto confirma que la reversa矩阵 se ha realizado correctamente──

### Paso 4: Conectar a las redes neuronales  Conectar a la red neuronal

> Paso 4: Conexión a la red neuronal con la matriz  de la realización desde cero para construir una capa completa de la red neuronal

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

Esta es una sola capa densa:`output = relu(W @ x + b)`Cada capa densa en cada red neuronal hace exactamente esto.

> **【中文解读】**
> Esto es la realización completa de la red de la red de conexión completa: cambios de línea: W @ x + b) + activación de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de red de red de la red de red de red de red de red de red de red de red de red de red de red de red de red de red de red de red de red de red de red de red de red de red de red de red de red de red de red de red de red de red de red de red de red de red de red de red de red de red de red de red de red de red de red de red de red de red

## Usalo con el marco de ejecución

NumPy hace todo lo anterior en menos líneas y órdenes de magnitud más rápido.

> NumPy con menos código, rápido en varios niveles numéricos para hacer la misma operación.

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

El `@`operador en llamadas Python `__matmul__`NumPy lo implementa con rutinas BLAS optimizadas escritas en C y Fortran.

> Python de `@`运算符调用                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        `__matmul__`◊ Número de veces utiliza C y Fortran 编写的优化 BLAS Ejemplo, igual matemática,快 100 倍──

La radiodifusión en NumPy:

```python
matrix = np.array([[1, 2, 3], [4, 5, 6]])
bias = np.array([10, 20, 30])
print(matrix + bias)
```

NumPy transmite automáticamente el sesgo 1D a través de ambas filas. Así es como la adición de sesgos funciona en cada marco de red neuronal.

> NumPy automáticamente se genera una dimensión de parámetro de parámetro de parámetro de parámetro de parámetro de parámetro de parámetro de parámetro de parámetro de parámetro de parámetro de parámetro de parámetro de parámetro de parámetro de parámetro de parámetro de parámetro de parámetro de parámetro de parámetro de parámetro de parámetro de parámetro de parámetro de parámetro de parámetro de parámetro de parámetro de parámetro de parámetro de parámetro de parámetro de parámetro de parámetro de parámetro de parámetro de parámetro de parámetro de parámetro de parámetro de parámetro de parámetro de parámetro de parámetro de parámetro de parámetro de parámetro de parámetro de parámetro de parámetro de parámetro de parámetro de parámetro de parámetro de parámetro de parámetro de parámetro de parámetro de parámetro de parámetro de parámetro de parámetro de parámetro de parámetro de parámetro de parámetro de parámetro de parámetro de parámetro de parámetro de parámetro de parámetro de parámetro de parámetro de parámetro de parámetro de parámetro de parámetro de parámetro de parámetro de parámetro de parámetro de parámetro de parámetro de parámetro de parámetro de parámetro de parámetro de parámetro de parámetro de parámetro de parámetro de parámetro de parámetro de parámetro de parámetro de parámetro de parámetro de parámetro de parámetro de parámetro de parámetro de parámetro de parámetro de parámetro de parámetro de parámetro de parámetro de parámetro de parámetro de parámetro de parámetro de parámetro de parámetro de parámetro de parámetro de parámetro de parámetro de parámetro de parámetro de parámetro de parámetro de parámetro de parám

## Envíe el producto .

Esta lección produce un prompt para enseñar operaciones de matriz a través de la intuición geométrica.`outputs/prompt-matrix-operations.md`¿ Qué ?

> Este curso ha producido un consejo de la matemática de la matemática.`outputs/prompt-matrix-operations.md`¿Qué es eso?

La clase Matrix construida aquí es la base para el marco de la red neuronal mini que construimos en la fase 3, lección 10.

> La matriz de la clase construida en esta es la base de la Fase 3 del 10o curso del marco de la red neuronal.

## Los ejercicios.

1. **Verify the inverse.**Multiplicado `A @ A.inverse_2x2()`y confirmar que obtiene la matriz de identidad. Prueba con tres diferentes matrices 2x2. ¿Qué sucede cuando el determinante es cero?
   **验证逆矩阵。**¿ Qué ?`A @ A.inverse_2x2()`Como se confirma que se obtiene una matriz. ¿Cómo se puede hacer una matriz de 2x2 diferente?

2. **Implement 3x3 inverse.**Extenda la clase de Matrix para calcular inversos de matrices 3x3 usando el método de adjugación.`np.linalg.inv`¿ Qué ?
   **实现 3x3 逆矩阵。**Utilizando el método de expansión de la matriz, con el resultado de NumPy en comparación.

3. **Build a two-layer network.**Utilizando sólo su clase Matrix (sin NumPy), cree una red neuronal de dos capas: entrada (3) -> oculta (4) -> salida (2). Inicializa pesos aleatorios, ejecuta un pase hacia adelante y verifique que todas las formas son correctas.
   **构建双层网络。**Sólo con Matrix 类((no con NumPy), crear输入(3)->隐藏(4)->输出(2) de la red,运行前向传播并验证形状。

## Términos clave .

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

## Más Leer más Leer más

- [3Blue1Brown: Essence of Linear Algebra](https://www.3blue1brown.com/topics/linear-algebra)- Intuición visual para cada operación que se cubre aquí
- [NumPy documentation on broadcasting](https://numpy.org/doc/stable/user/basics.broadcasting.html)- las reglas exactas que sigue NumPy
- [Stanford CS229 Linear Algebra Review](http://cs229.stanford.edu/section/cs229-linalg.pdf)- referencia concisa para el álgebra lineal específico de ML
