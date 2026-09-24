# वेक्टर, मैट्रिक्स और ऑपरेशन

> प्रत्येक तंत्रिका नेटवर्क अतिरिक्त चरणों के साथ मैट्रिक्स गुणन है।

> प्रत्येक तंत्रिका नेटवर्क मूलतः एक रैंक है जो कुछ अतिरिक्त चरणों को जोड़ता है।

**Type:** Build | **类型:** 动手
**Languages:** Python, Julia | **语言:** Python, Julia
**Prerequisites:** Phase 1, Lesson 01 (Linear Algebra Intuition) | **前置知识:** Phase 1, Lesson 01 (线性代数直觉)
**Time:** ~60 minutes | **时间:** ~60 分钟

## सीखने के लक्ष्य

- तत्व-बुद्धिमान संचालन, मैट्रिक्स गुणन, ट्रांसपोस, निर्धारक और विपरीत के साथ मैट्रिक्स वर्ग का निर्माण करें
  构建包含逐元素运算、矩阵乘法、转置、行列式、逆矩阵 के मैट्रिक्स 类
- तत्व-बुद्धिमान गुणा को मैट्रिक्स गुणा से अलग करें और समझाएं कि प्रत्येक कब लागू होता है
  区分分分分元素乘法 और矩阵乘法, अपनी-अपनी उपयुक्त परिदृश्यों की व्याख्या करें
- एक एकल घने तंत्रिका नेटवर्क परत को लागू करें (`relu(W @ x + b)`) केवल स्क्रैच से मैट्रिक्स वर्ग का उपयोग कर
   केवल शून्य से प्राप्त मैट्रिक्स  वर्ग के उपयोग से एक 密神经网络层  को प्राप्त करना`relu(W @ x + b)`)
- प्रसारण नियमों और तंत्रिका नेटवर्क ढांचे में पूर्वाग्रह जोड़ने का काम कैसे करता है, इसकी व्याख्या करें
  解释广播规则和神经网络框架中偏置加法的工作方式

> **【中文解读】**
> प्रत्येक तंत्रिका नेटवर्क का मूल है रेंज गुणा फ़ैसला। रेंज का प्रतिनिधित्व डेटा (जैसे एक शब्द, एक चित्र) के रूप में किया जाता है।`output = relu(W @ x + b)`यह कोड के पीछे गणित है

> **【拓展：向量/矩阵在 AI 中的位置】**
> - **词嵌入（Word Embedding）**: प्रत्येक शब्द को एक उच्च आयामी आयाम के रूप में दर्शाया जाता है, जैसे कि 300 维), शब्द की तुलना में, शब्द का आयाम अंतरिक्ष में दूरी से अधिक निकट है। यह एनएलपी का आधार है।
> - **神经网络权重**: प्रत्येक परत का भार एक矩 है, इनपुट भार गुणा भार矩 प्राप्त होता है।
> - **Transformer 的注意力机制**: मूलतः Q、K、V तीनों मैट्रिक्स का गुणा और Softmax 运算

## समस्या  समस्या परिचय

आप एक तंत्रिका नेटवर्क बनाना चाहते हैं. आप कोड पढ़ते हैं और यह देखते हैंः

> आप एक तंत्रिका नेटवर्क का निर्माण करना चाहते हैं. आप कोड में लिखा हैः

```
output = activation(weights @ input + bias)
```

यह `@`मैट्रिक्स गुणा है।`weights`एक मैट्रिक्स है।`input`यदि आप नहीं जानते कि वे ऑपरेशन क्या करते हैं, तो यह रेखा जादू है. अगर आप जानते हैं, तो यह तीन ऑपरेशन में एक परत के पूरे आगे पारित है.

> `@`है रक्छाँ乘法`weights`एक रक्शा है।`input`यदि आप नहीं जानते कि ये ऑपरेशन क्या करते हैं, तो यह कोड जादू है। यदि आप जानते हैं, तो यह एक परत का पूर्ण पूर्ववर्ती प्रसार है।

आपके मॉडल द्वारा संसाधित की जाने वाली प्रत्येक छवि पिक्सेल मानों की एक मैट्रिक्स है. प्रत्येक शब्द एम्बेडिंग एक वेक्टर है. प्रत्येक तंत्रिका नेटवर्क की प्रत्येक परत मैट्रिक्स परिवर्तन है. आप मैट्रिक्स संचालन में धाराप्रवाह होने के बिना एआई सिस्टम नहीं बना सकते हैं, जिस तरह आप चर को समझने के बिना कोड नहीं लिख सकते हैं।

> 模型处理 के प्रत्येक चित्र में विजुअल矩阵, प्रत्येक शब्द में इम्बेडमेंट में वेक्टर हैं, तंत्रिका नेटवर्क के प्रत्येक परत में मेट्रैक परिवर्तन हैं── अपरिचित矩阵运算 में एआई 系统 का निर्माण नहीं हो सकता, जैसे कि परिवर्तन को समझ नहीं पा रहा है, कोड लिखने में असमर्थ है──

यह सबक उस धाराप्रवाहता को शून्य से बनाती है।

> इस प्रकार की प्रथा को शून्य से स्थापित करना शुरू कर दिया गया है।

> **【中文解读】**
> `output = activation(weights @ input + bias)`यह कोड तंत्रिका नेटवर्क के एक स्तर का अग्रिम प्रसार है। यदि आप इसे नहीं समझते हैं तो यह जादू की तरह दिखता है; यदि आप इसे समझते हैं, तो यह तीन बुनियादी संचालन है।

## अवधारणा का मूल अवधारणा

### वेक्टरः क्रमबद्ध संख्याओं की सूची

वेक्टर एक दिशा और परिमाण के साथ संख्याओं की एक सूची है। एआई में, वेक्टर डेटा बिंदुओं, विशेषताओं या मापदंडों का प्रतिनिधित्व करते हैं।

> वेक्टर एक समूह है जिसमें दिशाएँ और बड़ी संख्याएँ हैं।

```
v = [3, 4]        -- a 2D vector # 二维向量
w = [1, 0, -2]    -- a 3D vector # 三维向量
```

एक 2D वेक्टर `[3, 4]`एक विमान पर निर्देशांक (3, 4) पर इंगित करता है। इसकी लंबाई (महानता) 5 (तीन-चार-पांच त्रिकोण) है।

> दो आयाम `[3, 4]`                                                                                                                                                                                                                                                              

### मैट्रिक्सः संख्याओं के ग्रिड 矩阵: डिजिटल नेट格

एक मैट्रिक्स एक 2D ग्रिड है। पंक्तियों और स्तंभों। एक m x n मैट्रिक्स में m पंक्तियों और n स्तंभ हैं।

> 矩阵是二维网格,由行和列组成──一个 m x n 矩阵有 m 行 n 列──

```
A = | 1  2  3 |     -- 2x3 matrix (2 rows, 3 columns) # 2行3列矩阵
    | 4  5  6 |
```

न्यूरल नेटवर्क में, वजन मैट्रिक्स इनपुट वेक्टरों को आउटपुट वेक्टरों में बदल देते हैं। 784 इनपुट और 128 आउटपुट वाली परत में 128x784 वजन मैट्रिक्स का उपयोग किया जाता है।

> तंत्रिका नेटवर्क में, वजन मैट्रिक्स में इनपुट वेट्यूम परिवर्तन के लिए आउटपुट वेट्यूम में परिवर्तन होता है। एक में 784 इनपुट और 128 आउटपुट लेयर होते हैं।

### क्यों आकार महत्वपूर्ण है

मैट्रिक्स गुणन का एक सख्त नियम हैः`(m x n) @ (n x p) = (m x p)`आंतरिक आयामों को मेल खाना चाहिए.

> 矩阵乘法 के सख्त रूप नियम हैंः`(m x n) @ (n x p) = (m x p)`, आंतरिक आयामों को एक साथ होना चाहिए।

```
(128 x 784) @ (784 x 1) = (128 x 1)
  weights       input       output # 权重矩阵 × 输入向量 = 输出向量

Inner dimensions: 784 = 784  -- valid # 内部维度必须匹配
```

यदि आप PyTorch में एक आकार असंगतता त्रुटि प्राप्त करते हैं, तो यह क्यों है.

> आप PyTorch में "शैली असंगतता" का सामना करते हैं  गलती समय, 99% कारण यह है कि इस नियम का उल्लंघन किया गया है 

> **【中文解读】**
> 矩阵乘法形状规则: ((m x n) @ (n x p) = (m x p) ・・・ आंतरिक आयाम अवश्य一致──आप PyTorch में "आकार असंगतता" 错误时,99% का कारण है इस नियम के उल्लंघन किया गया है──

### ऑपरेशन नक्शा

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

### तत्व-बुद्धि बनाम मैट्रिक्स गुणा

यह अंतर शुरुआती लोगों को लगातार ठोकर खाता है।

> यह अंतर अक्सर शुरुआती छात्रों को उलझाने देता है।

तत्व-बुद्धिमानः मिलान वाली स्थिति को गुणा करें. दोनों मैट्रिक्स एक ही आकार के होने चाहिए।

> 逐元素乘法:对应位置相乘, दो矩阵形状 अनिवार्य रूप से समान है।`*`दिखाएँ

```
| 1  2 |   | 5  6 |   | 5  12 |
| 3  4 | * | 7  8 | = | 21 32 |
```

मैट्रिक्स गुणाः पंक्तियों और स्तंभों के अंक उत्पाद। आंतरिक आयामों को मेल खाना चाहिए।

> 矩阵乘法:行与列做点积, आंतरिक आयाम अवश्य一致──在 PyTorch 中 中使用 `@`दिखाएँ

```
| 1  2 |   | 5  6 |   | 1*5+2*7  1*6+2*8 |   | 19  22 |
| 3  4 | @ | 7  8 | = | 3*5+4*7  3*6+4*8 | = | 43  50 |
```

अलग-अलग ऑपरेशन, अलग-अलग परिणाम, अलग-अलग नियम।

> अलग-अलग ऑपरेशन, अलग-अलग परिणाम, अलग-अलग नियम।`*`和 `@`में NumPy/PyTorch 中含义完全不同,混会导致沉默 bug──

### प्रसारण

जब आप आउटपुट मैट्रिक्स में एक पूर्वाग्रह वेक्टर जोड़ते हैं, तो आकार मेल नहीं खाते हैं। प्रसारण छोटे सरणी को फिट करने के लिए बढ़ाता है।

> 广播机制: जब विकिरण वेक्टर और आउटपुट矩阵 के आकार में असंगति होती है, तो प्रसारण स्वचालित रूप से छोटे संख्याओं का विस्तार करता है।

```
| 1  2  3 |   +   [10, 20, 30]
| 4  5  6 |

Broadcasting stretches the vector across rows:

| 1  2  3 |   | 10  20  30 |   | 11  22  33 |
| 4  5  6 | + | 10  20  30 | = | 14  25  36 |
```

प्रत्येक आधुनिक ढांचे यह स्वचालित रूप से करता है। इसे समझना भ्रम को रोकता है जब आकृति गलत लगती है लेकिन कोड चल रहा है।

> प्रत्येक आधुनिक ढांचे में स्वचालित रूप से प्रसारण होता है। इसे समझने से "आकार नहीं है, लेकिन कोड चल सकता है" की उलझन से बचा जा सकता है।

## इसे बनाओ, इसे पूरा करो।
```figure
vector-projection
```

## इसे बनाओ

### चरण 1: वेक्टर वर्ग

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

> वेक्टर 类实现:加法/减法是逐元素运算;标量乘法扩大到每个分量;点是积点;

### चरण 2: कोर ऑपरेशन के साथ मैट्रिक्स वर्ग

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

> मैट्रिक्स 类核心操作:matmul 是矩阵乘法(行×列做点积);Transpose 行列互换;determinant 用递归拉普拉斯展开;inverse_2x2 用 (1/det) × [[d,-b],[-c,a]];identity 创建单位矩阵。

### चरण 3: इसे काम करते हुए देखें

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

> 验证矩阵 类:A+B、A@B、A^T、det(A)、A−1 都正确──最关键的验证是A @ A−1 = I(单位矩阵), यह पुष्टि करता है विपरीत矩阵实现正确──

### चरण 4: तंत्रिका नेटवर्क से कनेक्ट करें  तंत्रिका नेटवर्क से कनेक्ट करें

> चौथा चरण: तंत्रिका नेटवर्क से कनेक्ट करना शून्य से प्राप्त मैट्रिक्स वर्ग का उपयोग करके एक पूर्ण तंत्रिका नेटवर्क परत का निर्माण करना है।

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

यह एक ही घने परत हैः`output = relu(W @ x + b)`प्रत्येक तंत्रिका नेटवर्क में प्रत्येक घने परत ठीक यही करती है।

> **【中文解读】**
> यही तंत्रिका नेटवर्क के पूरे कनेक्शन स्तर की पूर्ण पूर्ति हैः 线性变换(W @ x + b) + 非线性 सक्रियण(ReLU) ⋅ चाहे वह 1 स्तर का हो या 100 स्तर का नेटवर्क, प्रत्येक स्तर एक ही काम कर रहा है。

## इसे फ्रेमवर्क के साथ लागू करें

NumPy ऊपर की सभी चीजों को कम लाइनों और बड़े पैमाने के आदेशों में तेजी से करता है।

> NumPy के साथ कम कोड,, कुछ संख्यात्मक स्तरों पर एक ही ऑपरेशन को पूरा करने के लिए।

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

`@`पायथन कॉल में ऑपरेटर `__matmul__`NumPy इसे अनुकूलित BLAS दिनचर्या के साथ लागू करता है C और Fortran में लिखा है. एक ही गणित, 100 गुना तेजी से.

> पायथन की `@`运算符调用 `__matmul__`◊NumPy उपयोग C 和 Fortran 编写的优化 BLAS उदाहरन, इसी तरह गणित,快 100 倍──

NumPy में प्रसारणः

```python
matrix = np.array([[1, 2, 3], [4, 5, 6]])
bias = np.array([10, 20, 30])
print(matrix + bias)
```

NumPy स्वचालित रूप से दोनों पंक्तियों पर 1D पूर्वाग्रह प्रसारित करता है। यह हर तंत्रिका नेटवर्क फ्रेमवर्क में पूर्वाग्रह जोड़ने का काम करता है।

> NumPy स्वचालित रूप से एक आयाम विकृति विवर्तन को सभी पंक्तियों तक प्रसारित करेगा।

## इसे भेजें उत्पाद

इस पाठ में ज्यामितीय अंतर्ज्ञान के माध्यम से मैट्रिक्स संचालन को सिखाने के लिए एक संकेत उत्पन्न होता है।`outputs/prompt-matrix-operations.md`. .

> इस वर्ग में एक माध्यम के रूप में एक उदाहरण के रूप में एक उदाहरण के रूप में एक उदाहरण के रूप में एक उदाहरण के रूप में एक उदाहरण के रूप में एक उदाहरण के रूप में एक उदाहरण के रूप में एक उदाहरण के रूप में एक उदाहरण के रूप में एक उदाहरण के रूप में एक उदाहरण के रूप में एक उदाहरण के रूप में एक उदाहरण के रूप में एक उदाहरण के रूप में एक उदाहरण के रूप में एक उदाहरण के रूप में एक उदाहरण के रूप में एक उदाहरण के रूप में एक उदाहरण के रूप में एक उदाहरण के रूप में एक उदाहरण के रूप में एक उदाहरण के रूप में एक उदाहरण के रूप में एक उदाहरण के रूप में एक उदाहरण के रूप में एक उदाहरण के रूप में एक उदाहरण के रूप में एक उदाहरण के रूप में एक उदाहरण के रूप में एक उदाहरण के रूप में एक उदाहरण के रूप में एक उदाहरण के रूप में एक उदाहरण के रूप में एक उदाहरण के रूप में एक उदाहरण के रूप में एक उदाहरण के रूप में एक उदाहरण के रूप में एक उदाहरण के रूप में एक उदाहरण के रूप में एक उदाहरण के रूप में एक उदाहरण के रूप में एक उदाहरण के रूप में एक उदाहरण के रूप में एक उदाहरण के रूप में एक उदाहरण के रूप में एक उदाहरण के रूप में एक उदाहरण के रूप में एक उदाहरण के रूप में एक उदाहरण के रूप में एक उदाहरण के रूप में एक उदाहरण के रूप में एक उदाहरण के रूप में एक उदाहरण के रूप में एक उदाहरण के रूप में एक उदाहरण के रूप में एक उदाहरण के रूप में एक उदाहरण के रूप में एक उदाहरण के रूप में एक उदाहरण के रूप में एक उदाहरण के रूप में एक उदाहरण के रूप में एक उदाहरण के रूप में एक उदाहरण के रूप में एक उदाहरण के रूप में एक उदाहरण के रूप में एक`outputs/prompt-matrix-operations.md`

यहाँ निर्मित मैट्रिक्स वर्ग मिनी न्यूरल नेटवर्क फ्रेमवर्क की नींव है जिसे हम चरण 3, पाठ 10 में बनाते हैं।

> इसमे निर्मित मैट्रिक्स वर्ग चरण 3 के 10 वें वर्ग के रूप में निर्मित है।

## अभ्यास विषय

1. **Verify the inverse.**गुणा करें `A @ A.inverse_2x2()`और पुष्टि करें कि आप पहचान मैट्रिक्स प्राप्त करते हैं. यह तीन अलग 2x2 मैट्रिक्स के साथ कोशिश करें. क्या होता है जब निर्धारक शून्य है?
   **验证逆矩阵。**`A @ A.inverse_2x2()`√ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √

2. **Implement 3x3 inverse.**3x3 मैट्रिक्स के लिए विपरीत गणना करने के लिए मैट्रिक्स वर्ग का विस्तार करें।`np.linalg.inv`. .
   **实现 3x3 逆矩阵。**Matrix 类, के परिणामों के साथ-साथ संख्याओं के परिणामों के साथ तुलना

3. **Build a two-layer network.**केवल अपने मैट्रिक्स वर्ग (नहीं NumPy) का उपयोग करके, दो-परत तंत्रिका नेटवर्क बनाएंः इनपुट (3) -> छिपा हुआ (4) -> आउटपुट (2). यादृच्छिक वजन शुरू करें, आगे की पास चलाएं, और सभी आकारों की पुष्टि करें कि वे सही हैं।
   **构建双层网络。**केवल मैट्रिक्स 类 (n) का उपयोग करके, create input (n) - > छिपा हुआ (n) - > आउटपुट (n) का उपयोग करके, संजाल का उपयोग करके,运行前向传播并验证形状──

## Key Terms  Key Terms  Key Terms  Key Terms  Key Terms  Key Terms  Key Terms  Key Terms  Key Terms  Key Terms  Key Terms  Key Terms  Key Terms  Key Terms  Key Terms  Key Terms  Key Terms  Key Terms  Key Terms  Key Terms  Key Terms  Key Terms  Key Terms  Key Terms  Key Terms  Key Terms  Key Terms  Key Terms  Key Terms  Key Terms  Key Terms  Key Terms  Key Terms  Key Terms  Key Terms  Key Terms  Key Terms  Key Terms  Key Terms  Key Terms  Key Terms  Key Terms  Key Terms  Key Terms  Key Terms  Key Terms  Key Terms  Key Terms  Key Terms  Key Terms  Key Terms  Key Terms  Key Terms  Key Terms  Key Terms  Key Terms  Key Terms  Key Terms  Key Terms  Key Terms  Key Terms  Key Terms  Key Terms  Key Terms  Key Terms  Key Terms  Key Terms  Key Terms  Key Terms  Key Terms  Key Terms  Key Terms  Key Terms  Key Terms  Key Terms  Key Terms  Key Terms  Key Terms  Key Terms  Key Terms  Key Terms  Key Terms  Key Terms  Key Terms  Key Terms  Key Terms  Key Terms  Key Terms  Key Terms  Key Terms  Key Terms  Key Terms  Key Terms  Key Terms  Key Terms  Key Terms  Key Terms  Key Terms  Key Terms  Key Terms  Key Terms  Key Terms  Key Terms  Key Terms  Key Terms  Key Terms  Key Terms  Key Terms  Key

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

## आगे पढ़ना 延伸閱讀

- [3Blue1Brown: Essence of Linear Algebra](https://www.3blue1brown.com/topics/linear-algebra)- यहाँ कवर किए गए प्रत्येक ऑपरेशन के लिए दृश्य अंतर्ज्ञान
- [NumPy documentation on broadcasting](https://numpy.org/doc/stable/user/basics.broadcasting.html)- NumPy के अनुसार सही नियम
- [Stanford CS229 Linear Algebra Review](http://cs229.stanford.edu/section/cs229-linalg.pdf)- एमएल विशिष्ट रैखिक बीजगणित के लिए संक्षिप्त संदर्भ
