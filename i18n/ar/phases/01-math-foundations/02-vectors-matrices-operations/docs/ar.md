# المتجهات والمعادلات والعمليات

> كل شبكة عصبية هي مجرد مضاعفة المصفوفة مع خطوات إضافية.

> كل شبكة عصبية هي في جوهرها مجرد محور مضاعف إلى عدد قليل من الخطوات الإضافية.

**Type:** Build | **类型:** 动手
**Languages:** Python, Julia | **语言:** Python, Julia
**Prerequisites:** Phase 1, Lesson 01 (Linear Algebra Intuition) | **前置知识:** Phase 1, Lesson 01 (线性代数直觉)
**Time:** ~60 minutes | **时间:** ~60 分钟

## أهداف التعلم

- بناء فئة المصفوفة مع العمليات الحكيمة العنصر، مضاعفة المصفوفة، نقل، تحديد، والعكس
  构建包含逐元素运算、矩阵乘法、转置、行列式、逆矩阵的矩阵类
- تمييز مضاعفة العناصر من مضاعفة المصفوفة وتوضيح متى تنطبق كل واحدة
  区分各元素乘法和矩阵乘法، تفسير المشهد الملائم لها
- تنفيذ طبقة واحدة من شبكة عصبية كثيفة (`relu(W @ x + b)`) باستخدام فئة ماتريكس فقط من الصفر
  فقط باستخدام الصفوف من التحقق من المصفوفة 类 لتحقيق طبقة من شبكة العصبية`relu(W @ x + b)`)
- شرح قواعد البث وكيف يعمل إضافة التحيزات في إطار شبكات الأعصاب
  解释广播规则和神经网络框架中偏置加法的工作方式

> **【中文解读】**
> كل شبكة عصبية هي محور ضربة المقدمة. يمثل حجم البيانات. يمثل المقدمة التغيرات.`output = relu(W @ x + b)`هذا هو ما خلفه الرياضيات

> **【拓展：向量/矩阵在 AI 中的位置】**
> - **词嵌入（Word Embedding）**: كل كلمة تم تمثيلها على حجم عالٍ مثل 300 维) ، كلمة قريبة من الكلمة تقترب من المسافة في الفضاء الكمي.
> - **神经网络权重**: وزن كل طبقة هو محور، والحجم المدخل ضرب محور الوزن يحصل على محور الخروج.
> - **Transformer 的注意力机制**: في الأساس هو Q、K、V ثلاثة محور ضرب و Softmax 运算

## المشكلة المشكلة المشكلة

إذا أردت بناء شبكة عصبية، فاقرأ الرمز وشاهد هذا:

> أنت تريد بناء شبكة عصبية.

```
output = activation(weights @ input + bias)
```

هذا`@`هو مضاعفة المصفوفة.`weights`هي المصفوفة.`input`إذا كنت لا تعرف ما تفعل هذه العمليات، هذا الخط هو السحر. إذا كنت تعرف، انها كامل المضي قدما من طبقة في ثلاث عمليات.

> `@`هو المُحاكمة`weights`إنه محور`input`إن كنت تعرف، فإن هذا هو الطبقة الكاملة من التنقل المباشر إلى التنقل، فمن ثمّة ثلاثة عمليات فقط.

كل صورة يعالجها نموذجك هي ماتريكس من قيم البيكسل. كل كلمة تضمنها متجه. كل طبقة من كل شبكة عصبية هي تحول ماتريكس. لا يمكنك بناء أنظمة الذكاء الاصطناعي دون أن تكون متسلية في عمليات المصفوفة بنفس الطريقة التي لا يمكنك كتابة الشفرة دون فهم المتغيرات.

> كل صورة في النموذج المعالجة هي مجسمة الصورة، كل كلمة تضمنت هي مجسمة، كل طبقة من شبكة العصبية هي مجسمة تغيرها.

هذا الدروس يبني هذه السهولة من الصفر.

> هذا الدرس بدأ من الصفر في بناء هذه المهارة

> **【中文解读】**
> `output = activation(weights @ input + bias)`هذا الكود هو التوزيع الأمامي للطبقة الأولى من شبكة العصبية. إذا لم تفهم الموجة المتعددة، فإنه يبدو وكأنه سحر. إذا فهمت، فإنه هو ثلاثة عمليات أساسية.

## المفهوم الأساسي

### المتجهات: قائمة مرتبة للأرقام

المتجه هو قائمة بالأرقام ذات الاتجاه والحجم. في الذكاء الاصطناعي، يمثل المتجهون نقاط البيانات أو الخصائص أو المعلمات.

> القطر هو مجموعة من الأرقام ذات الاتجاهات والكبار. في الذكاء الاصطناعي، القطر يعبر عن نقاط البيانات أو الخصائص أو العناصر.

```
v = [3, 4]        -- a 2D vector # 二维向量
w = [1, 0, -2]    -- a 3D vector # 三维向量
```

متجه ثنائي الأبعاد`[3, 4]`تشير إلى إحداثيات (3, 4) على مستوى مسطح. طولها (الكبيرة) هو 5 (الثلاثي 3-4-5).

> ثاني حجم`[3, 4]`إندوانس على التوالي (3, 4) ، طوله 5 ((勾股定理 3-4-5 三角形) 』

### المصفوفات: شبكات الأرقام

المصفوفة هي شبكة ثنائية الأبعاد. الصفوف والعمدة. المصفوفة m x n لديها m الصفوف و n العمدة.

> الموجة هي شبكة، بواسطة الموجة والصفوف.

```
A = | 1  2  3 |     -- 2x3 matrix (2 rows, 3 columns) # 2行3列矩阵
    | 4  5  6 |
```

في الشبكات العصبية، تقوم المصفوفات الوزنية بتحويل متجهات المدخلات إلى متجهات الخروج. تستخدم طبقة ذات 784 مدخلًا و 128 خروجاً ماتريساً وزناً 128 × 784.

> في شبكة العصبية، يتم تغيير الموجات الوزنية إلى الموجات الخارجة.

### لماذا الأشكال مهمة لماذا الشكل مهم

مضاعفة المصفوفة لديها قاعدة صارمة:`(m x n) @ (n x p) = (m x p)`الأبعاد الداخلية يجب أن تتطابق

> القانون لديه قواعد صارمة للشكل:`(m x n) @ (n x p) = (m x p)`, الدرجة الداخلية يجب أن تكون متطابقة

```
(128 x 784) @ (784 x 1) = (128 x 1)
  weights       input       output # 权重矩阵 × 输入向量 = 输出向量

Inner dimensions: 784 = 784  -- valid # 内部维度必须匹配
```

إذا حصلت على خطأ عدم مطابقة الشكل في PyTorch، هذا هو السبب.

> في "بيتورش" تعرضت لـ "مضايقة الشكل"  خطأ في الوقت، 99٪ من الأسباب هي أن هذه القاعدة قد خرقت

> **【中文解读】**
> 矩阵乘法形状规则: ((م x ن) @ (ن x p) = (م x p) ・・・ الدرجة الداخلية يجب أن تكون متوافقة。 أنت في PyTorch وسط تواجه "الاختلاف في الشكل" 错误时,99% من السبب هو هذا القاعدة تم خرقها。

### خريطة العمليات

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

### النسب العنصرية مقابل مضاعفة المصفوفة

هذا التمييز يثير الابتدائيين باستمرار

> هذا الفصل يجعل المبتدئين مشوشين

في العنصر: ضرب المواقع المتطابقة يجب أن تكون كلا المصفوفتين ذات الشكل

> 逐元素乘法:对应位置相乘, يجب أن تكون شكل الموجتين متشابهة.`*`أظهرت

```
| 1  2 |   | 5  6 |   | 5  12 |
| 3  4 | * | 7  8 | = | 21 32 |
```

مضاعفة المصفوفة: منتجات النقاط من الصفوف والعمود. يجب أن تتطابق الأبعاد الداخلية.

> 矩阵乘法:行与列做点积,内部维度必须一致──在 PyTorch 中 中用 `@`أظهرت

```
| 1  2 |   | 5  6 |   | 1*5+2*7  1*6+2*8 |   | 19  22 |
| 3  4 | @ | 7  8 | = | 3*5+4*7  3*6+4*8 | = | 43  50 |
```

عمليات مختلفة، نتائج مختلفة، قواعد مختلفة.

> مختلفة العمليات، نتائج مختلفة، قواعد مختلفة.`*`和 `@`في NumPy/PyTorch 中含义完全不同,混会导致 صمت البغ.

### الإذاعة

عندما تضيف متجه التحيز إلى صفوف الخروج، فإن الشكول لا تتطابق. الإذاعة تمدد المجموعة الأصغر لتتناسب.

> آلية الإشعاع: عندما لا يتطابق شكل محور التحكم مع محور الخروج، فإن الإشعاع يتنمى تلقائياً لتناسب عدد أصغر من الأعداد.

```
| 1  2  3 |   +   [10, 20, 30]
| 4  5  6 |

Broadcasting stretches the vector across rows:

| 1  2  3 |   | 10  20  30 |   | 11  22  33 |
| 4  5  6 | + | 10  20  30 | = | 14  25  36 |
```

كل إطار جديد يفعل هذا تلقائياً، فهمه يمنع الارتباك عندما تبدو الأشكال خاطئة ولكن الرمز يعمل.

> كل إطار حديث يقوم بتوزيعه تلقائياً. فهمه يمكن تجنب مشاكل "الشكل لا يتوافق مع الكود ولكن يمكن أن يسرع".

## بناء ذلك تحرك لتحقيق
```figure
vector-projection
```

## بناءها

### الخطوة الأولى: فئة المتجهات

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

> النقاط 类实现:加法/减法是逐元素运算;标量乘法扩大到每个分量;قطة 是点积(对应分量乘积之和);大小 是模长(√(x2+y2+...))。

### الخطوة الثانية: فئة المصفوفة مع العمليات الأساسية

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

> المصفوفة 类核心操作:matmul 是矩阵乘法(行×列做点积);Transpose 行列互换;determinant 用递归拉普拉斯展开;inverse_2x2 用 (1/det) × [[d-,b],[-c,a]];identity 创建单位矩阵。

### الخطوة الثالثة: شاهدوا أن الأمر يعمل

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

> 验证 ماتريكس 类:A+B、A@B、A^T、det(A)、A−1 都正确──最关键的验证是A @ A−1 = I(单位矩阵), وهذا يؤكد على عكس矩阵实现正确──

### الخطوة الرابعة: التواصل مع الشبكات العصبية

> 第4 خطوة: الاتصال بالشبكة العصبية باستخدام نوع المصفوفة من الصفر لإنشاء طبقة كاملة من شبكة العصبية

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

هذه طبقة كثيفة واحدة:`output = relu(W @ x + b)`كل طبقة كثيفة في كل شبكة عصبية تفعل هذا بالضبط.

> **【中文解读】**
> هذا هو التنفيذ الكامل للشبكة العصبية على جميع مستوياتها: التغييرات السلكية ((W @ x + b) + غير السلكية النشطة ((ReLU) )). سواء كانت شبكة 1 طبقة أو 100 طبقة، كل طبقة تقوم بنفس الشيء‬

## استخدمها في إطار التنفيذ

إنّ (نومبي) يقوم بكلّ شيء أعلاه في خطوط أقل وأوامر أكبر أسرع.

> عدد بكميات أقل من الكود، بسرعة عدد قليل من الدرجات الكمية لإنجاز نفس العملية.

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

- نعم`@`عامل في مكالمات Python `__matmul__`ينفذها NumPy مع روتينات BLAS المثلى مكتوبة باللغة C و Fortran نفس الرياضيات، أسرع بنسبة 100 مرة

> Python `@`运算符调用 `__matmul__`◊NumPy استخدام C 和 Fortran 编写的优化 BLAS مثال,同样数学,快 100 倍──

الإذاعة في NumPy:

```python
matrix = np.array([[1, 2, 3], [4, 5, 6]])
bias = np.array([10, 20, 30])
print(matrix + bias)
```

يُبث NumPy تلقائيًا التحيز 1D عبر كل من الصفوف. هكذا يعمل إضافة التحيز في كل إطار شبكة عصبية.

> يُمكن أن يُحكم النّاس بشكلٍ مستقلٍ على الـ 1 وحدةٍ من الـ 2 وحدةٍ من الـ 2 وحدةٍ من الـ 3 وحدةٍ من الـ 3 وحدةٍ من الـ 3 وحدةٍ من الـ 3 وحدةٍ من الـ 3 وحدةٍ من الـ 3 وحدةٍ من الـ 3 وحدةٍ من الـ 3 وحدةٍ من الـ 3 وحدةٍ من الـ 3 وحدةٍ من الـ 3 وحدةٍ من الـ 3 وحدةٍ من الـ 3 وحدةٍ من الـ 3 وحدةٍ من الـ 3 وحدةٍ من الـ 3 وحدةٍ من الـ 3 وحدةٍ من الـ 3 وحدةٍ من الـ 3 وحدةٍ من الـ 3 وحدةٍ من الـ 3 وحدةٍ من الـ 3 وحدةٍ من الـ 3 وحدةٍ من الـ 3 وحدةٍ من الـ 3 وحدةٍ من الـ 3 وحدةٍ من الـ 3 وحدةٍ من الـ 3 وحدةٍ من الـ 3 وُحُجُدّةٍ من الـ 3 وُدّةٍ من الـ 3 وُدّةٍ من الـ

## أرسلها .

هذه الدروس تنتج طلب لتعليم عمليات المصفوفة من خلال الحدس الهندسي. انظر `outputs/prompt-matrix-operations.md`. . .

> هذا المرحلة من المنتج من خلال هندسة مباشرة أستاذ المجموعة من النظرية`outputs/prompt-matrix-operations.md`.

فصيلة المصفوفة التي بنيت هنا هي أساس إطار شبكة عصبية صغيرة بنيت في المرحلة 3، الدروس 10.

> هذه المصفوفة المتركسية التي تم بناؤها هي أساس المرحلة 3

## تمارين التدريب

1. **Verify the inverse.**ضرب`A @ A.inverse_2x2()`و تأكد من الحصول على المصفوفة الهوية. حاولي ذلك مع ثلاث مصفوفات مختلفة 2x2. ماذا يحدث عندما يكون المحدد هو الصفر؟
   **验证逆矩阵。**ستعمل`A @ A.inverse_2x2()`相乘, تأكد الحصول على الوحدة الموجة. حاول ثلاثة مختلفة 2x2 الموجة.

2. **Implement 3x3 inverse.**تمديد فئة المصفوفة لحساب العكسات للمصفوفات 3x3 باستخدام طريقة الجمع. اختبرها ضد NumPy `np.linalg.inv`. . .
   **实现 3x3 逆矩阵。**مع معالجة المصفوفة لتوسيع المصفوفة، مع نتائج NumPy مقابل

3. **Build a two-layer network.**باستخدام فئة المصفوفة الخاصة بك فقط (لا يوجد NumPy) ، قم بإنشاء شبكة عصبية ذات طبقتين: المدخل (3) -> الخفية (4) -> الخروج (2). قم بتشغيل الأوزان العشوائية ، و قم بتشغيل مرور إلى الأمام ، وتحقق من صحة جميع الأشكال.
   **构建双层网络。**فقط باستخدام المصفوفات 类((不用 NumPy) ، create输入(3)->隐藏(4)->输出(2) من شبكة،运行前向传播并验证形状。

## شروط رئيسية

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

## المزيد من القراءة

- [3Blue1Brown: Essence of Linear Algebra](https://www.3blue1brown.com/topics/linear-algebra)- البصرية للعمليات التي تم تغطيتها هنا
- [NumPy documentation on broadcasting](https://numpy.org/doc/stable/user/basics.broadcasting.html)- القواعد الدقيقة التي تتبعها NumPy
- [Stanford CS229 Linear Algebra Review](http://cs229.stanford.edu/section/cs229-linalg.pdf)- إشارة موجزة للجزرية الخطية الخاصة بالجهاز
