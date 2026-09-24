# Vecteurs, matrices et opérations

> Chaque réseau neural est juste une multiplication de matrice avec des étapes supplémentaires.

> Chaque réseau neural est en fait un matrix multiplié par quelques étapes supplémentaires.

**Type:** Build | **类型:** 动手
**Languages:** Python, Julia | **语言:** Python, Julia
**Prerequisites:** Phase 1, Lesson 01 (Linear Algebra Intuition) | **前置知识:** Phase 1, Lesson 01 (线性代数直觉)
**Time:** ~60 minutes | **时间:** ~60 分钟

## Objectifs d'apprentissage

- Construire une classe de Matrix avec des opérations par élément, la multiplication de la matrice, la transposition, le déterminant et l'inverse
  构建包含逐元素运算、矩阵乘法、转置、行列式、逆矩阵的矩阵类
- Distinguer la multiplication par élément de la multiplication par matrice et expliquer quand chaque élément s'applique
  区分分分分分分分分分分分分分分分分分分分分分分分分分分分分分分分分分分分分分分分分分分分分分分分分分分分分分分分分分分分分分分分分分分分分分分分分分分分分分分分分分分分分分分分分分分分分分分分分分分分分分分分分分分分分分分分分分分分分分分分分分分分分分分分分分分分分分分分分分分分分分分分分分分分分分分分分分分分分分分分分分分分分分分分分分分分分分分分分分分分分分分分分分分分分分分分分分分分分分分分分分分分分分分分分分分分分分分分分分分分分分分分分分分分分分分分分分分分分分分分分分分分分分分分分分分分分分分分分分分分分分分分分分分分分分分分分分分分分分分分分分分分分分分分分分分分分分分分分分分分分分分分分分分分分分分分分分分分分分分分分分分分分分分分分分分分分分分分分分分分分分分分分分分分分分分分分分分分分分分分分分分分分分分分分分分分分分分分分分分分分分分分分分分分分分分分分分分分分分分分分分分分分分分分分分分分分分分分分分分分分分分分分分分分分分分分分分分分分分分分分分分分分分分分分分分分分分分分分分分分分分分分分分分分分分分分分分分分分分分分分分分分分分分分分分分分分分分分分分分分分分分分分分分分分
- Implementer une seule couche de réseau neural dense (`relu(W @ x + b)`) utilisant uniquement la classe Matrix à partir de zéro
   Utiliser uniquement une matrice  class réalisée à partir de zéro pour réaliser un  layer de réseau neuronal `relu(W @ x + b)`)
- Expliquer les règles de radiodiffusion et comment l'addition de biais fonctionne dans les cadres de réseaux neuronaux
  解释广播规则和神经网络框架中偏置加法的工作方式

> **【中文解读】**
> Le cœur de chaque réseau neural est la fréquence multiplicative. Le flux représente les données (comme un mot, une image), le flux représente les changements (comme un niveau de poids du réseau neural).`output = relu(W @ x + b)`C'est le code derrière la mathématiques.

> **【拓展：向量/矩阵在 AI 中的位置】**
> - **词嵌入（Word Embedding）**: Chaque mot est représenté comme un volume élevé (comme 300 dimensions), les mots qui se trouvent à proximité dans l'espace de volume sont plus proches de la distance.
> - **神经网络权重**: Le poids de chaque couche est une matrice, la puissance d'entrée multipliée par la puissance de la matrice obtient la puissance de sortie.
> - **Transformer 的注意力机制**En substance, il s'agit de Q、K、V, de multiplication de trois matrices et de calcul de la Softmax.

## Le problème , l' introduction du problème

Vous voulez construire un réseau neuronal, vous lisez le code et voyez ceci:

> Tu veux construire un réseau neuronal. Tu vois dans le code:

```
output = activation(weights @ input + bias)
```

Ça ...`@`est la multiplication de matrice.`weights`sont une matrice.`input`Si vous ne savez pas ce que ces opérations font, cette ligne est magique. si vous le savez, c'est l'ensemble de la passée vers l'avant d'une couche en trois opérations.

> `@`C'est une façon de faire.`weights`C'est une réaction.`input`Si vous ne savez pas ce que ces opérations font, ce code est magique. Si vous le savez, c'est la propagation de la couche complète de trois opérations.

Chaque image que votre modèle traite est une matrice de valeurs de pixels. Chaque mot intégré est un vecteur. Chaque couche de chaque réseau neural est une transformation de matrice. Vous ne pouvez pas construire des systèmes d'IA sans être fluide dans les opérations de matrice de la même manière que vous ne pouvez pas écrire de code sans comprendre les variables.

> Chaque image du modèle traité est une matrice de images, chaque mot est un métrage, chaque couche du réseau neural est une matrice de changements.

Cette leçon construit cette fluidité à partir de zéro.

> Le cours commence à construire cette compétence de zéro.

> **【中文解读】**
> `output = activation(weights @ input + bias)`Ce code est le premier à se propager de la couche du réseau neuronal. Si vous ne comprenez pas le mode de multiplication, il ressemble à la magie; si vous le comprenez, il est trois opérations fondamentales.

## Le concept de base.

### Vecteurs: listes de nombres dans l'ordre.

Un vecteur est une liste de nombres avec une direction et une magnitude.

> Le torsion est un ensemble de nombres orientés et de nombres de taille.

```
v = [3, 4]        -- a 2D vector # 二维向量
w = [1, 0, -2]    -- a 3D vector # 三维向量
```

Un vecteur 2D `[3, 4]`Il est le point de départ de la ligne de référence de la ligne de référence.

> Deuxième dimension`[3, 4]`Indice vers le plan de la séquence (3, 4), longueur est de 5 ((勾股定理 3-4-5 三角形) ⋅

### Matrices: grilles de nombres

Une matrice est une grille 2D. Les lignes et les colonnes.

> La matrice est en deux dimensions, composée de lignes et de lignes.

```
A = | 1  2  3 |     -- 2x3 matrix (2 rows, 3 columns) # 2行3列矩阵
    | 4  5  6 |
```

Dans les réseaux neuronaux, les matrices de poids transforment les vecteurs d'entrée en vecteurs de sortie.

> Dans le réseau nerveux, la charge de gravité est transformée en charge d'entrée et de sortie.

### Pourquoi les formes comptent ? Pourquoi les formes comptent ?

La multiplication de matrice a une règle stricte:`(m x n) @ (n x p) = (m x p)`Les dimensions internes doivent être correspondantes.

> La réglementation est stricte:`(m x n) @ (n x p) = (m x p)`Les dimensions internes doivent être harmonieuses.

```
(128 x 784) @ (784 x 1) = (128 x 1)
  weights       input       output # 权重矩阵 × 输入向量 = 输出向量

Inner dimensions: 784 = 784  -- valid # 内部维度必须匹配
```

Si vous obtenez une erreur de déséquilibre de forme dans PyTorch, c'est pourquoi.

> Vous avez rencontré une "incohérence de forme" dans PyTorch. 99% des raisons sont que cette règle a été violée.

> **【中文解读】**
> 矩阵乘法形状规则: ((m x n) @ (n x p) = (m x p) ・・・ la dimension interne doit être concordante。 vous êtes en PyTorch en milieu rencontré "incohérence de forme" 错误时, 99% des causes est cette règle été violée。

### La carte des opérations.

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

### Multiplication par élément par matrice

Cette distinction fait trébucher constamment les débutants.

> Cette différence rend souvent les débutants confus.

Par élément: multipliez les positions correspondantes.

> 逐元素乘法: à la position de la position, les deux matrices doivent être identiques.`*`Je veux dire...

```
| 1  2 |   | 5  6 |   | 5  12 |
| 3  4 | * | 7  8 | = | 21 32 |
```

Multiplication de matrice: produits de points de lignes et de colonnes.

> 矩阵乘法:行与列做点积, dimension interne doit être consensuelle.`@`Je veux dire...

```
| 1  2 |   | 5  6 |   | 1*5+2*7  1*6+2*8 |   | 19  22 |
| 3  4 | @ | 7  8 | = | 3*5+4*7  3*6+4*8 | = | 43  50 |
```

Des opérations différentes, des résultats différents, des règles différentes.

> Différentes opérations, différents résultats, différentes règles.`*`et `@`Dans NumPy/PyTorch, la signification est complètement différente, la confusion entraînera un bug silencieux.

### La radiodiffusion

Quand on ajoute un vecteur de biais à une matrice de sorties, les formes ne correspondent pas.

>  广播机制: Lorsque la forme du vecteur de décalage et de la matrice de sortie ne correspondent pas, la diffusion se développe automatiquement pour adapter un plus petit nombre de groupes.

```
| 1  2  3 |   +   [10, 20, 30]
| 4  5  6 |

Broadcasting stretches the vector across rows:

| 1  2  3 |   | 10  20  30 |   | 11  22  33 |
| 4  5  6 | + | 10  20  30 | = | 14  25  36 |
```

Chaque cadre moderne le fait automatiquement, ce qui empêche la confusion lorsque les formes semblent erronées mais que le code fonctionne.

> Chaque cadre moderne se répand automatiquement. Comprendre que cela peut éviter le défi de "la forme n'est pas pour le code mais peut courir".

## Construisez-le et mettez-le en œuvre.
```figure
vector-projection
```

## Faites-le

### Étape 1: classe vectorielle

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

> Vecteur 类实现:加法/减法是个元素运算;标量乘法扩大到每个分量;点是积点;大小是模长;大小是模长;大小是模长;大小是个数;大小是个数;大小是个数;大小是个数;大小是个数;大小是个数;大小是个数;大小是个数;大小是个数;大小是个数;大小是个数;大小是个数;大小是个数;大小是个数;大小是个数;大小是个数;大小是个数;大小是个数;大小是个数;大小是个数;大小是个数;大小是个数;大小是个数;大小是个数;大小是个数;大小是个数是个数;大小是个数是个数;大小数是个数是个数;大小数是个数是个数;大小数是个数是个数是个数;大小数是个数是个数是个数是个数;大小数是个数是个数是个数是个数是个数;

### Étape 2: classe de matrice avec les opérations de base

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

> Matrix 类核心操作:matmul 是矩阵乘法(行×列做点积);transpose 行列互换;determinant 用递归拉普拉斯展开;inverse_2x2 用 (1/det) × [[d,-b],[-c,a]];identité 创建单位矩阵。

### Étape 3: voir fonctionner

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

> 验证 Matrix 类:A+B、A@B、A^T、det(A)、A−1 都正确──最关键的验证是A @ A−1 = I(单位矩阵), ce qui confirme l'inversion de la矩阵 实现正确──

### Étape 4: Connectez-vous aux réseaux neuronaux

> 第4 étape: Connexion au réseau neuronalUtilisez des classes de matrice réalisées à partir de zéro pour construire une couche complète du réseau neuronal

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

C' est une seule couche dense:`output = relu(W @ x + b)`Chaque couche dense de chaque réseau neural fait exactement ça.

> **【中文解读】**
> C'est la réalisation complète de la couche complète de réseau de neurones: transition de la connexion: W @ x + b) + activation non-linee (ReLU) ⋅ soit 1 ou 100 couches de réseau, chaque couche fait la même chose ⋅

## Utilisez-le avec le cadre de réalisation

NumPy fait tout ce qui est en haut en moins de lignes et des ordres de magnitude plus rapidement.

> NumPy avec moins de code, plusieurs niveaux de numéros pour effectuer la même opération.

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

Le `@`opérateur dans les appels Python `__matmul__`NumPy le met en œuvre avec des routines BLAS optimisées écrites en C et Fortran.

> Python `@`运算符调用 `__matmul__`◊ NumPy Utilisation C 和 Fortran 编写的优化 BLAS 例例,同样数学,快 100倍──

La diffusion en numPy:

```python
matrix = np.array([[1, 2, 3], [4, 5, 6]])
bias = np.array([10, 20, 30])
print(matrix + bias)
```

NumPy diffuse automatiquement le biais 1D sur les deux rangées. C'est ainsi que l'addition de biais fonctionne dans chaque cadre de réseau neuronal.

> NumPy automatiquement un dimension de décalage de la charge de propagation à tous les secteurs.

## Envoyez-le . Produit .

Cette leçon fournit un prompt pour enseigner les opérations de matrice par intuition géométrique.`outputs/prompt-matrix-operations.md`- Je suis désolé .

> Cette classe a été élaborée par un professeur de géométrie.`outputs/prompt-matrix-operations.md`Il y a une autre.

La classe Matrix construite ici est la base du framework de réseau mini-néural que nous construisons dans la phase 3, leçon 10.

> La matrice de la construction est la base du cadre de la phase 3 du cours 10 du réseau neuronal.

## Les exercices

1. **Verify the inverse.**Multipliez`A @ A.inverse_2x2()`et confirmez que vous obtenez la matrice d'identité. essayez avec trois matrices 2x2 différentes.
   **验证逆矩阵。**Il va`A @ A.inverse_2x2()`À la fois, confirmez que vous avez une unité de réaction.

2. **Implement 3x3 inverse.**Élargir la classe Matrix pour calculer les inverses pour les matrices 3x3 en utilisant la méthode adjugée.`np.linalg.inv`- Je suis désolé .
   **实现 3x3 逆矩阵。**Utilisation de la matrice avec le modèle de l'expansion de la matrice, avec le résultat de NumPy par rapport à la matrice.

3. **Build a two-layer network.**En utilisant uniquement votre classe Matrix (pas de NumPy), créez un réseau neural à deux couches: entrée (3) -> cachée (4) -> sortie (2). Initialize des poids aléatoires, exécutez un passage vers l'avant et vérifiez que toutes les formes sont correctes.
   **构建双层网络。**Il est également possible de créer un réseau de données en ligne avec des données de type matrice (nombre de données), en utilisant le nombre de données.

## Les termes clés

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

## Encore une lecture

- [3Blue1Brown: Essence of Linear Algebra](https://www.3blue1brown.com/topics/linear-algebra)- l' intuition visuelle pour chaque opération couverte ici
- [NumPy documentation on broadcasting](https://numpy.org/doc/stable/user/basics.broadcasting.html)- les règles exactes que suit NumPy
- [Stanford CS229 Linear Algebra Review](http://cs229.stanford.edu/section/cs229-linalg.pdf)- référence concise pour l'algèbre linéaire spécifique à la méthode ML
