# Vectores, Matrizes e Operações

> Cada rede neural é apenas uma multiplicação de matriz com passos extras.

> Cada rede neuronal é, em essência, uma matriz multiplicada por vários passos adicionais.

**Type:** Build | **类型:** 动手
**Languages:** Python, Julia | **语言:** Python, Julia
**Prerequisites:** Phase 1, Lesson 01 (Linear Algebra Intuition) | **前置知识:** Phase 1, Lesson 01 (线性代数直觉)
**Time:** ~60 minutes | **时间:** ~60 分钟

## Objetivos de aprendizagem

- Construir uma classe de Matrix com operações de elementos, multiplicação de matriz, transposição, determinante e inversos
  构建包含逐元素运算、矩阵乘法、转置、行列式、逆矩阵的矩阵类 类
- Distinguir a multiplicação por elemento da multiplicação por matriz e explicar quando cada uma se aplica
  区分 từng element乘法和矩阵乘法, explicar seus respectivos cenários de aplicação
- Implementar uma única camada de rede neural densa (`relu(W @ x + b)`) utilizando apenas a classe Matrix do zero
   Utilize apenas um tipo de Matrix  realise de zero  realise uma camada de rede neural`relu(W @ x + b)`)
- Explique as regras de radiodifusão e como a adição de preconceitos funciona em estruturas de rede neural
  解释广播规则和神经网络框架中偏置加法的工作方式 解释广播规则和神经网络框架中偏置加法的工作方式 解释广播规则和神经网络框架中偏置加法的工作方式

> **【中文解读】**
> Cada rede neuronal é baseada em um conjunto de matrizes multiplicadas.`output = relu(W @ x + b)`É o código que está atrás da matemática.

> **【拓展：向量/矩阵在 AI 中的位置】**
> - **词嵌入（Word Embedding）**Cada palavra é representada como uma alta dimensão em um espaço de tensão.
> - **神经网络权重**Cada camada tem um peso de uma matriz, a entrada de um peso de uma matriz é multiplicada pelo peso da matriz e a saída é multiplicada por um peso de uma matriz.
> - **Transformer 的注意力机制**A sua base é Q、K、V, três matrizes multiplicadas e Softmax 运算.

## O problema é o problema da introdução

Se quiser construir uma rede neural, lê o código e vê isto:

> Você quer construir uma rede neuronal.

```
output = activation(weights @ input + bias)
```

Isso .`@`é a multiplicação de matriz.`weights`São uma matriz.`input`Se você não sabe o que essas operações fazem, esta linha é mágica. se você sabe, é toda a passagem para a frente de uma camada em três operações.

> `@`É um método de construção.`weights`É uma rectangular.`input`Se você não sabe o que fazer com estas operações, esta linha de código é mágica. Se você sabe, é uma camada completa de três operações.

Cada imagem que o seu modelo processa é uma matriz de valores de píxeles. Cada palavra incorporada é um vetor. Cada camada de cada rede neural é uma transformação de matriz. Você não pode construir sistemas de IA sem ser fluente em operações de matriz da mesma forma que não pode escrever código sem entender variáveis.

> Cada imagem processada pelo modelo é uma matriz de imagem, cada palavra é um meteoro, cada camada da rede neuronal é uma matriz de mudança.

Esta lição construiu essa fluência a partir do zero.

> Este curso começa a construir essa habilidade a partir de zero.

> **【中文解读】**
> `output = activation(weights @ input + bias)`Esse código é a primeira direção da rede neuronal. Se você não entender a matriz multiplicadora, parece mágica; se você entender, é três operações básicas.

## O conceito central.

### Vectores: listas de números ordenadas.

Um vetor é uma lista de números com uma direção e magnitude.

> Um veículo é um conjunto de números direcionados e grandes.

```
v = [3, 4]        -- a 2D vector # 二维向量
w = [1, 0, -2]    -- a 3D vector # 三维向量
```

Um vetor 2D `[3, 4]`A sua extensão (magnitude) é de 5 (o triângulo 3-4-5).

> 2 dimensões`[3, 4]`Indicações de posição em plano (3, 4), longitudem 5 ((勾股定理 3-4-5 三角形) ⋅

### Matriz: Grades de números.

Uma matriz é uma grade 2D. fileiras e colunas. uma matriz m x n tem m fileiras e n colunas.

> A linha é formada por um m x n 矩阵有 m 行 n 列──

```
A = | 1  2  3 |     -- 2x3 matrix (2 rows, 3 columns) # 2行3列矩阵
    | 4  5  6 |
```

Em redes neurais, matrizes de peso transformam vetores de entrada em vetores de saída. Uma camada com 784 entradas e 128 saídas usa uma matriz de peso de 128x784.

> Em redes neuronais, a massa de peso será transformada em massa de entrada e saída. Uma tem 784 entradas e 128 saídas usando uma massa de peso de 128x784.

### Porque é que as formas importam?

A multiplicação de matriz tem uma regra estritamente regida:`(m x n) @ (n x p) = (m x p)`As dimensões internas devem corresponder.

> A regulamentação da matriz é rigorosa:`(m x n) @ (n x p) = (m x p)`, dimensões internas devem ser uniformes.

```
(128 x 784) @ (784 x 1) = (128 x 1)
  weights       input       output # 权重矩阵 × 输入向量 = 输出向量

Inner dimensions: 784 = 784  -- valid # 内部维度必须匹配
```

Se você receber um erro de desajuste de forma em PyTorch, é por isso.

> Você encontrou "desconformidade de forma" no PyTorch.

> **【中文解读】**
> 矩阵乘法形状规则: ((m x n) @ (n x p) = (m x p) ・・・ dimensão interna deve concordar。 Você em PyTorch 中 é encontrado com "desconformidade de forma" 错误时,99% de causa é esta regra foi violada。

### O mapa de operações.

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

### Multiplicação por elemento versus matriz

Esta distinção atrapalha os iniciantes constantemente.

> Esta diferença faz com que os iniciantes fiquem confusos.

Elementos-wise: multiplicar posições correspondentes. Ambas as matrizes devem ser da mesma forma.

> 逐元素乘法:对应位置相乘, duas matrizes de forma devem ser iguais.`*`- Não.

```
| 1  2 |   | 5  6 |   | 5  12 |
| 3  4 | * | 7  8 | = | 21 32 |
```

Multiplicação de matriz: produtos de pontos de linhas e colunas.

> 矩阵乘法:行与列做点积, dimensiones internas devem concordar.`@`- Não.

```
| 1  2 |   | 5  6 |   | 1*5+2*7  1*6+2*8 |   | 19  22 |
| 3  4 | @ | 7  8 | = | 3*5+4*7  3*6+4*8 | = | 43  50 |
```

Diferentes operações, resultados diferentes, regras diferentes.

> Diferentes operações, diferentes resultados, diferentes regras.`*`和 `@`Em NumPy/PyTorch 中含义完全不同,混会导致沉默 bug──

### Transmissão

Quando adicionar um vetor de viés a uma matriz de saídas, as formas não coincidem.

>  Mecanismo de difusão: quando a forma do torque de saída e do torque de direção não se encaixam, a difusão se expande automaticamente para que um número menor se adapte.

```
| 1  2  3 |   +   [10, 20, 30]
| 4  5  6 |

Broadcasting stretches the vector across rows:

| 1  2  3 |   | 10  20  30 |   | 11  22  33 |
| 4  5  6 | + | 10  20  30 | = | 14  25  36 |
```

Cada estrutura moderna faz isso automaticamente.

> Cada quadro moderno é automaticamente em movimento.

## Construí-lo e realizei-o.
```figure
vector-projection
```

## Construí-lo

### Passo 1: Classe de vetores

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

> Vector 类实现:加法/减法是逐元素运算;标量乘法扩至每个分量;点是积点;大小是模长;大小是模长;大小是模长;大小是模长;大小是模长;大小是模长;大小是模长;大小是模长;大小是模长;大小是模长;大小是模长;大小是模长;大小是模长;大小是模长;大小是模长;大小是模长;大小是模长;大小是模长;大小是模长;大小是模长;大小是模长;大小是模长;大小是模长;大小是模长;大小是模长;大小是模长;大小是模长;大小是模长;大小是模长;大小是模长;大小是模长的的数是模长;大小是模长的数是模长的数是个数;大小是的数是的数是的数是的数是的数;大小是是的数是的数是的数是的数是的数是的数是的数是的数是的数是的数是的数是的数的数是的数是的数是的数是的数的数是的数是的数是的数是的数的数是的数是的数的数是的数是的数是的数的数是的数是的数的数是的数的数是的数.

### Passo 2: Classe de matriz com operações de núcleo

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

> Matrix 类核心操作:matmul 是矩阵乘法(行×列做点积);transpose 行列互换;determinante 用递归拉普拉斯展开;inverse_2x2 用 (1/det) × [[d,-b],[-c,a]];identidade 创建单位矩阵。

### Passo 3: Veja como funciona

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

> 验证矩阵类:A+B、A@B、A^T、det(A)、A−1 都正确──最关键的验证是A @ A−1 = I(单位矩阵),这确认逆矩阵实现正确──

### Passo 4: Conectar-se a redes neurais

> 第4步: Conexão à rede neuronalUsar a matriz 类  construindo uma camada completa de rede neuronal realizada a partir de zero

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

Esta é uma única camada densa:`output = relu(W @ x + b)`Cada camada densa em cada rede neural faz exatamente isso.

> **【中文解读】**
> É a realização completa da rede de ligação completa: mudança de linha: W @ x + b) + atividade não-linear (ReLU) ⋅ seja uma rede de 1 ou 100 níveis, cada nível está fazendo a mesma coisa.

## Use-o com o framework implementado.

NumPy faz tudo acima em menos linhas e ordens de magnitude mais rápido.

> NumPy usando menos código, rápido em vários níveis numéricos para completar a mesma operação.

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

O `@`operador em chamadas Python `__matmul__`NumPy implementa com rotinas BLAS optimizadas escritas em C e Fortran.

> Python `@`运算符调用                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        `__matmul__`◊ NumPy Utilize C 和 Fortran 编写的优化 BLAS 例例,同样数学,快 100倍──

Transmissão em NumPy:

```python
matrix = np.array([[1, 2, 3], [4, 5, 6]])
bias = np.array([10, 20, 30])
print(matrix + bias)
```

NumPy transmite automaticamente o preconceito 1D em ambas as linhas. É assim que a adição de preconceitos funciona em cada framework de rede neural.

> NumPy automaticamente irá um dimensional de partilha de velocidades propagadas a todos os níveis.

## Envia-o . Produto .

Esta lição produz um prompt para ensinar operações de matriz através da intuição geométrica.`outputs/prompt-matrix-operations.md`- Não .

> Esta aula foi produzida por um professor de geometria direta.`outputs/prompt-matrix-operations.md`- Não.

A classe Matrix construída aqui é a base para a estrutura de rede neural mini que construímos na fase 3, lição 10.

> A matriz construída aqui é a base da fase 3 do 10o curso do framework da rede neuronal.

## Exercícios.

1. **Verify the inverse.**Multiplicar`A @ A.inverse_2x2()`e confirmar que você tem a matriz de identidade. Tente com três diferentes matriz 2x2. O que acontece quando o determinante é zero?
   **验证逆矩阵。**- Não .`A @ A.inverse_2x2()`Como se confirme que temos uma unidade de massa?

2. **Implement 3x3 inverse.**Extenda a classe Matrix para calcular inversos para matrizes 3x3 usando o método de adjugação.`np.linalg.inv`- Não .
   **实现 3x3 逆矩阵。**Utilizando o método de expansão de matrizes, com resultados de NumPy em relação à

3. **Build a two-layer network.**Usando apenas a sua classe Matrix (sem NumPy), crie uma rede neural de duas camadas: entrada (3) -> oculta (4) -> saída (2). Inicie pesos aleatórios, execute uma passagem para a frente e verifique se todas as formas são corretas.
   **构建双层网络。**Apenas usando Matrix 类((( não usando NumPy), criar entrada (s) 3) -> ocultar (s) 4) -> sair (s) 2) da rede,运行前向传播并验证形状──

## Termos-chave .

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

## Mais leitura 延伸阅读

- [3Blue1Brown: Essence of Linear Algebra](https://www.3blue1brown.com/topics/linear-algebra)- Intuição visual para cada operação aqui coberta
- [NumPy documentation on broadcasting](https://numpy.org/doc/stable/user/basics.broadcasting.html)- as regras exatas que o NumPy segue
- [Stanford CS229 Linear Algebra Review](http://cs229.stanford.edu/section/cs229-linalg.pdf)- referência concisa para a álgebra linear específica do ML
