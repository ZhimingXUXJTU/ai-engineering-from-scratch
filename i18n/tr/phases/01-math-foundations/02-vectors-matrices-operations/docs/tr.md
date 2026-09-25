# vektörler, matrisler ve işlemler

> Her sinir ağı sadece ekstra adımlarla matris çarpımı.

> Her sinir ağı aslında bir dizi ek adımla çarpılmış bir metrajdır.

**Type:** Build | **类型:** 动手
**Languages:** Python, Julia | **语言:** Python, Julia
**Prerequisites:** Phase 1, Lesson 01 (Linear Algebra Intuition) | **前置知识:** Phase 1, Lesson 01 (线性代数直觉)
**Time:** ~60 minutes | **时间:** ~60 分钟

## Öğrenme hedefleri

- Element-bilge işlemler, matris çarpımı, transpose, determinant ve tersine ile bir Matrix sınıfı oluşturun
  构建包含逐元素运算、矩阵乘法、转置、行列式、逆矩阵的矩阵类
- Elementli çarpımı matris çarpımından ayırt edin ve her birinin ne zaman uygulanacağını açıklayın
  区分 từng元素乘法和矩阵乘法, kendi uygunluklarını açıklayın
- Tek yoğun nöral ağ katmanı uygula (`relu(W @ x + b)`) sadece sıfırdan Matrix sınıfını kullanıyor
  Sadece sıfırdan gerçekleşen bir Matrix sınıfı ile yoğun bir sinir ağını gerçekleştirmek için`relu(W @ x + b)`)
- Yayınlama kurallarını ve sinir ağ çerçevelerinde önyargı eklemenin nasıl çalıştığını açıklayın
  解释广播规则和神经网络框架中偏置加法的工作方式

> **【中文解读】**
> Her sinir ağının merkezi, bir kelime gibi, bir resim gibi, bir kütle ifade eder. Bu bölümden sıfırdan oluşan bir kütle ve bir matron sınıfı olarak, size tam anlamıyla yardım eder.`output = relu(W @ x + b)`Bu kodun arkasındaki matematik.

> **【拓展：向量/矩阵在 AI 中的位置】**
> - **词嵌入（Word Embedding）**Her kelime yüksek bir vektör olarak ifade edilir. Bu, NLP'nin temelidir.
> - **神经网络权重**: Her katın ağırlığı bir matron, giriş vectürü çarpı ağırlık vectürü çıkarım vectürü elde eder.
> - **Transformer 的注意力机制**Asıl olarak Q、K、V üç matronun çarpı ve Softmax 运算ı vardır.

## Sorunlar. Sorunlar.

Bir sinir ağı inşa etmek istiyorsanız, kodunu okuyun ve şunu görün:

> Bir sinir ağı inşa etmek istiyorsun.

```
output = activation(weights @ input + bias)
```

- Bu ...`@`Bu da matris çarpımı.`weights`- Bir matris.`input`Eğer bu işlemlerin ne olduğunu bilmiyorsanız, bu çizgi sihirli. Eğer biliyorsanız, bu bir katmanın üç işlemde ileriye geçmesi.

> `@`- Evet, evet.`weights`Bir rektür.`input`Bu bir yöntemi değilse, bu yöntemi sihirdir. Eğer biliyorsan, bu bir yöntemi tamamlıyor.

Modeliniz işleyen her görüntü, piksel değerlerinin bir matrisidir. Her kata yerleştirme bir vektördür. Her sinir ağının her katmanı bir matris dönüşümüdür. Matris işlemlerinde akıcı olmadan AI sistemlerini inşa edemezsiniz. Değişkenleri anlamadan kod yazabileceğiniz gibi.

> Model işleme yapıldığı her resim bir resimlik matrasıdır, her sözcük yerleşiminin bir vektörüdür, sinir ağının her katmanı bir matras değişikliği vardır.

Bu ders, bu akıcılığı sıfırdan inşa eder.

> Bu ders bu becerileri oluşturmaya zero'dan başladı.

> **【中文解读】**
> `output = activation(weights @ input + bias)`Bu kod, sinir ağının bir katmanının ön yönünde yayılmaktadır. Eğer bu kodun çarpma biçimini anlamıyorsanız, sihir gibi görünür. Eğer anlarsanız, bu üç temel işlemdir.

## Konsepten bir şey.

### Vektörler: sıralamalı sayılar listesini.

Bir vektör, yön ve büyüklüğü olan sayılar listesidir. AI'de vektörler veri noktalarını, özelliklerini veya parametreleri temsil eder.

> Vektör, yönlü ve büyük sayıların bir grupudur. AI'de, vektor verileri ifade eder.

```
v = [3, 4]        -- a 2D vector # 二维向量
w = [1, 0, -2]    -- a 3D vector # 三维向量
```

2 boyutlu bir vektör .`[3, 4]`Düzlemde koordinatlara (3, 4) işaret eder. Uzunluğu (geniüt) 5 ( 3-4-5 üçgen)

> İki boyut`[3, 4]`Görevi düzlemdeki oturma (3, 4), uzunluğu 5 ((勾股定理 3-4-5 三角形) ・・・

### Matrisler: Sayılar ağı.

Bir matris 2 boyutlu bir şebeke. Satırlar ve sütunlar.

> 矩阵是二维网格,由行和列组成──一个 m x n 矩阵有 m 行 n 列──

```
A = | 1  2  3 |     -- 2x3 matrix (2 rows, 3 columns) # 2行3列矩阵
    | 4  5  6 |
```

Nöral ağlarda ağırlık matrisleri giriş vektörlerini çıkış vektörlerine dönüştürür. 784 giriş ve 128 çıkış olan bir katman 128x784 ağırlık matrisini kullanır.

> Sinir ağlarında, ağırlıklı matçlar giriş ve çıkış vezleri için değişir. Birinde 784 giriş ve 128 çıkış katmanı kullanılır.

### Neden şekiller önemli?

Matrix çarpımı sıkı bir kuralı vardır:`(m x n) @ (n x p) = (m x p)`İç boyutlar aynı olmalı.

> 矩阵乘法'nın sert şekil kuralları vardır:`(m x n) @ (n x p) = (m x p)`İç boyutlar aynı olmalıdır.

```
(128 x 784) @ (784 x 1) = (128 x 1)
  weights       input       output # 权重矩阵 × 输入向量 = 输出向量

Inner dimensions: 784 = 784  -- valid # 内部维度必须匹配
```

PyTorch'de bir şekil eşleşme hatası varsa, bunun nedeni budur.

> PyTorch'te "şekil eşleşmezliği" ile karşılaştığınızda %99'un nedeni bu kuralın ihlal edilmesidir.

> **【中文解读】**
> 矩阵乘法形状规则: ((m x n) @ (n x p) = (m x p) ・・・内部维度必须一致──你在 PyTorch 中遇到"形不匹配" 错误时,99% 的原因是这个规则被违反了──

### Operasyon haritası.

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

### Element-wise vs matris çarpımı

Bu fark yeni başlayanları sürekli şaşırtıyor.

> Bu farkı sık sık yeni öğrencileri şaşırtıyor.

Element açısından: eşleşen pozisyonları çarpın.

> 逐元素乘法:对应位置相乘, iki矩阵 şekli aynı olmalıdır.`*`Göstermek

```
| 1  2 |   | 5  6 |   | 5  12 |
| 3  4 | * | 7  8 | = | 21 32 |
```

Matrix çarpımı: Satır ve sütunların nokta ürünleri. İç boyutlar eşleşmelidir.

> 矩阵乘法:行与列做点积,内部维度必须一致──在 PyTorch 中 中用 `@`Göstermek

```
| 1  2 |   | 5  6 |   | 1*5+2*7  1*6+2*8 |   | 19  22 |
| 3  4 | @ | 7  8 | = | 3*5+4*7  3*6+4*8 | = | 43  50 |
```

Farklı operasyonlar, farklı sonuçlar, farklı kurallar.

> Farklı operasyonlar, farklı sonuçlar, farklı kurallar.`*`和 `@`NumPy/PyTorch 中含义完全不同,混会导致沉默 bug──

### Yayınlama

Bir çıkış matrisine bir önyargı vektörü eklediğinizde şekiller eşleşmez.

> 广播机制: Geçici yönlü ve çıkış matron şekli uyumsuz olduğunda, yayın otomatik olarak daha küçük bir diziyi genişletir.

```
| 1  2  3 |   +   [10, 20, 30]
| 4  5  6 |

Broadcasting stretches the vector across rows:

| 1  2  3 |   | 10  20  30 |   | 11  22  33 |
| 4  5  6 | + | 10  20  30 | = | 14  25  36 |
```

Her modern çerçeve bunu otomatik olarak yapar. Şekiller yanlış görünse de kod çalışsa da, anlayış karışıklığı önler.

> Her modern çerçeve otomatik olarak yayımlanır. Bu yüzden "şekil değil, kod da çalışabilir" sorunu önleyebilirsiniz.

## Yapın.
```figure
vector-projection
```

## Yapın

### Adım 1: Vektör sınıfı

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

> vektör 类实现:加法/减法是逐元素运算;标量乘法扩至每个分量;dot 是点积(对应分量乘积之和);magnitude 是模长(√(x2+y2+...))。

### Adım 2: Temel işlemleri olan matris sınıfı

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

> Matrix 类核心操作:matmul 是矩阵乘法(行×列做点积);transpose 行列互换;determinant 用递归拉普拉斯展开;inverse_2x2 用 (1/det) × [[d,-b],[-c,a]];identity 创建单位矩阵。

### Üçüncü adım: Çalışın

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

> 验证 Matrix 类:A+B、A@B、A^T、det(A)、A−1 都正确──最关键的验证是A @ A−1 = I(单位矩阵), bu da逆矩阵实现正确──

### Dördüncü adım: Nöral ağlara bağlanın.

> 第4 adım: Sinir ağına bağlanmak, sıfırdan gerçekleşen Matrix sınıfını kullanarak tam bir sinir ağını oluşturmak.

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

Bu tek yoğun bir katman:`output = relu(W @ x + b)`Her sinir ağının yoğun katmanları tam olarak bunu yapar.

> **【中文解读】**
> İşte sinir ağının tüm bağlantı katmanının tam gerçekleşmesi: 线性变换 ((W @ x + b) + 非线性活 ((ReLU) ⋅ ister 1 katman ister 100 katmanlı bir ağ olsun, her katman aynı şeyi yapıyor。

## Çerçeveyi kullanın.

NumPy yukarıdaki her şeyi daha az çizgi ve büyüklük sıralarında daha hızlı yapar.

> NumPy daha az kod kullanarak birkaç sayısal seviyeye benzer işlemleri tamamlamak için.

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

- Evet .`@`Python çağrılarında operatör `__matmul__`NumPy, C ve Fortran'da yazılmış optimize edilmiş BLAS rutinleri ile uyguluyor. Aynı matematik, 100 kat daha hızlı.

> Python'un `@`运算符调用 `__matmul__`◊ NumPy C ve Fortran 编写的优化 BLAS 例例,同样数学,快 100倍──

NumPy'de yayınlama:

```python
matrix = np.array([[1, 2, 3], [4, 5, 6]])
bias = np.array([10, 20, 30])
print(matrix + bias)
```

NumPy, her iki satır boyunca 1D tersi otomatik olarak yayınlar.

> NumPy otomatik olarak bir boyutlu özenli bir yönlendirme yaparak tüm yönlere yayılır.

## İndirin . Ürünler .

Bu ders, geometrik sezgilerle matris işlemlerini öğretmek için bir ipucu üretir.`outputs/prompt-matrix-operations.md`- Evet .

> Bu ders bir geometristik direkt profesörlük matç işletiminin önerisi kelimesi olarak üretilmiştir.`outputs/prompt-matrix-operations.md`- Evet.

Burada inşa edilen Matrix sınıfı, 3. aşamada oluşturduğumuz mini sinir ağı çerçevesinin temelidir. 10. ders.

> Bu yapılandırılan Matrix sınıfı, 3. aşama 10. sınıfı büyüleyici sinir ağ çerçevesinin temelini oluşturur.

## Egzersizler.

1. **Verify the inverse.**Çoklu `A @ A.inverse_2x2()`2x2 matrisleri ile deneyin. belirleyici sıfır olduğunda ne olur?
   **验证逆矩阵。**- Ben de .`A @ A.inverse_2x2()`Birimlik birimliği olarak belirlenmiş.

2. **Implement 3x3 inverse.**Matrix sınıfını 3x3 matrisler için ters hesaplamak için adjugaat yöntemi kullanarak genişlet. NumPy'nin `np.linalg.inv`- Evet .
   **实现 3x3 逆矩阵。**Matrix 类, NumPy'nin sonuçları karşılaştırma

3. **Build a two-layer network.**Sadece Matrix sınıfınızı kullanarak (NumPy yok), iki katlı bir nöron ağı oluşturun: giriş (3) -> gizli (4) -> çıkış (2). Kasıtlı ağırlıkları başlatın, ileri geçiş çalıştırın ve tüm şekillerin doğru olduğunu doğrulayın.
   **构建双层网络。**Sadece Matrix 类((numPy kullanmayarak), oluşturmak için giriş yapın (3)-> gizlenmek için giriş yapın (4)-> çıkış yapın (2)

## Anahtar Terimler

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

## Daha fazla okumak

- [3Blue1Brown: Essence of Linear Algebra](https://www.3blue1brown.com/topics/linear-algebra)- Burada ele alınan her operasyon için görsel sezgisellik
- [NumPy documentation on broadcasting](https://numpy.org/doc/stable/user/basics.broadcasting.html)- NumPy'nin takip ettiği kesin kurallar
- [Stanford CS229 Linear Algebra Review](http://cs229.stanford.edu/section/cs229-linalg.pdf)- ML spesifik çizgi cebir için kısa bir referans
