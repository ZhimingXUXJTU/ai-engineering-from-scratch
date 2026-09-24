# 支持向量机
# 支持向量机 (SVM)


> 找出两个阶级之间的最宽的街道.

> 找到两类之间最宽的街道.

**Type:** Build | **类型：** 构建
**Language:**子**语言：**字符串
**Prerequisites:** Phase 1 (Lessons 08 Optimization, 14 Norms and Distances, 18 Convex Optimization) | **前置知识：** Phase 1（第 8 课优化、第 14 课范数与距离、第 18 课凸优化）
**Time:** ~90 minutes | **时间：** 约 90 分钟

## 学习目标

- 实现从零开始使用原始配方的链损失和梯度下降的线性SVM
  基本形式使用合页损失和梯度从零实现线性SVM下降
- 解释最大边缘原则,并从训练有素的模型中确定支持向量
  解释最大间隔原理,并从训练好的模型中识别支持向量
- 比较线性,多项和RBF内核,并解释内核技巧如何避免明确的高维映射
  比较线性核、多项式核和RBF核,解释核技巧如何避免显而易见高维映射
- 评估边缘宽度和分类错误之间的C参数控制的权衡
  评估C参数控制间隔宽度与分类错误之间的权衡


> **【中文解读】**
> 试图在高维空间中处理非线性问题. 直观理解就是升维后再切分.

> **【拓展：SVM 在深度学习时代仍然重要的场景】**
> 在小数据集中 (从数百到数千个样本) 仍然优于深度学习. 在早期垃圾邮件分类中,Google仍然使用线性SVM (LIBLINEAR),因为TF-IDF特征维度高但样本稀少,SVM的高维优势恰好发挥作用.在生物信息学中 (蛋白质分类、基因表现分析) 中,SVM仍然是主流算法.

## 问题 问题引入

您有两个类的数据点,需要画一个线 (或超平面) 分离它们.无限的许多线可以工作.你应该选择哪一个?

> 你有两个类型的数据点,需要画一条线 (或超平面) 将它们分开.

差距是决定边界和每一边最接近的数据点之间的距离. 较宽的差距意味着分类器更有信心,更好地将未见的数据概括.

> 间隔最大的条款.间隔是决策边界,到每一边最近的数据点的距离.

这种直觉导致了支持向量机,这是 ML 中最具数学优雅的算法之一.SVM在深度学习之前是主导分类方法,并且仍然是小数据集,高维度数据和需要原则,理解良好模型的理论保障的问题最好的选择.

> 这种直觉引发了支持量机ML中数学中最优雅的算法之一.SVM在深度学习之前是主流分类方法,至今仍然是小数据集,高维数据以及需要理论保证的问题的最佳选择.

 SVM 直接连接到第1阶段:优化是曲的 (课时18),边缘是用规范 (课时14) 测量的,并且内核技巧利用点产品来处理非线性界限,而无需在高维空间中计算.

> 优化是凸的 (第18课),间隔用范数量衡 (第14课),核技巧利用点积处理非线性边界而无需在高维空间中计算.

> **【中文解读】**
> 基于SVM的核心思想:在无数条可以分离两类数据的直线中,选择离最近数据点最远的条款即"最大间隔"原则──间隔越大,分类器越大,泛化能力越好──只有恰好位于间隔边界的少数点 (支持向量) 决定决策边界,其他点不会影响结果──这使SVM在预测时内存效率很高──

## 概念的核心概念

### 最大利分类器

由于线性分离的数据, 标签 y_i 在 {-1, +1} 和特征向量 x_i, 我们想要一个超平面 w^T x + b = 0 分离类.

> 给定标签 y_i 为 {-1, +1} 的线性可分数据和特征向量 x_i,我们需要一个超平面 w^T x + b = 0 来分离类.

从点 x_i 到超平面的距离是:

> 距离到超平面为:

```
distance = |w^T x_i + b| / ||w||
```

对于正确分类的点:y_i * (w^T x_i + b) > 0. 边缘是从超平面到两侧最近的点的距离的两倍.

> 对于正确分类点:y_i * (w^T x_i + b) > 0──间隔是超平面到两侧最近点距离的两倍──

```mermaid
graph LR
    subgraph Margin
        direction TB
        A["w^T x + b = +1"] ~~~ B["w^T x + b = 0"] ~~~ C["w^T x + b = -1"]
    end
    D["+ class points"] --> A
    E["- class points"] --> C
    B --- F["Decision boundary"]
```

优化问题:

> 优化问题:

```
maximize    2 / ||w||     (the margin width)
subject to  y_i * (w^T x_i + b) >= 1  for all i
```

同样 (最小化时的时间更容易优化):

> 其他地方:

```
minimize    (1/2) ||w||^2
subject to  y_i * (w^T x_i + b) >= 1  for all i
```

这是一个曲的方形程序. 它有一个独特的全球解决方案.坐落在边界边界 (w^T x_i + b) = 1) 的数据点是支持向量.它们是决定边界的唯一点.移动或移除任何非支持向量点,边界不会改变.

> 这是一个凸二规划问题. 它有一个唯一的全局解答.恰好位于隔边界的数据点. y_i * (w^T x_i + b) = 1)就是支持向量.它们是唯一决定边界的决定点.

### 支持向量:少数关键

```mermaid
graph TD
    subgraph Classification
        SV1["Support Vector (+ class)<br>y(w'x+b) = 1"] --- DB["Decision Boundary<br>w'x+b = 0"]
        DB --- SV2["Support Vector (- class)<br>y(w'x+b) = 1"]
    end
    O1["Other + points<br>(do not affect boundary)"] -.-> SV1
    O2["Other - points<br>(do not affect boundary)"] -.-> SV2
```

大多数训练点是无关紧要的.只有支持向量才有所重要.这就是为什么SVM在预测时间上具有记忆效率:你只需要存储支持向量,而不是整个训练集.

> 大多数训练点是无关的. 只有支持向量起作用. 这就是SVM在预测时内存效率高的原因:你只需要存储支持向量,而不是整个训练集.

支持向量数量也给出了通用错误的限制.与数据集尺寸相比,支持向量较少意味着更好的通用.

> 支持向量数量也给出了泛化差异的上界面.

### 软边缘:使用C参数处理噪音

实际数据很少完全可以分开.一些点可能位于边界的错误侧面或边界内部.软边界公式允许通过引入宽松变量来违反.

> 真实数据很少完全可分. 有些点可能在边界的错误一边,或在间隔内.

```
minimize    (1/2) ||w||^2 + C * sum(xi_i)
subject to  y_i * (w^T x_i + b) >= 1 - xi_i
            xi_i >= 0  for all i
```

宽松变量 xi_i 测量了 i 点违反了边际的程度. C 控制了交易:

> 松变量 xi_i 衡量点 i 违反间隔的程度──C 控制权衡:

| C value | Behavior |
|---------|----------|
| Large C | Penalizes violations heavily. Narrow margin, fewer misclassifications. Overfits |
| Small C | Allows more violations. Wide margin, more misclassifications. Underfits |

| C 值 | 行为 |
|------|------|
| 大 C | 严重惩罚违规。窄间隔，较少误分类。易过拟合 |
| 小 C | 允许更多违规。宽间隔，较多误分类。易欠拟合 |

是规律化强度,逆转.大 C = 规律化较少.小 C = 规律化较大.

> 是正则化强度的反面──大C = 较少正则化──小C = 较多正则化──

### 损失:SVM损失函数

软边缘SVM可以被重写为无限制优化:

> 软间隔 SVM 可以重写为无约束优化:

```
minimize    (1/2) ||w||^2 + C * sum(max(0, 1 - y_i * (w^T x_i + b)))
```

术语max(0,1 - y_i * f(x_i)) 是链损失.当点正确分类后,它是零.当点在边缘内或错误分类后,它是线性.

> 项 max(0, 1 - y_i * f(x_i)) 是合页损失──当点被正确分类而在间隔之外时为零──当点在间隔内或被误分类时为线性惩罚──

```
Hinge loss for a single point:

loss
  |
  | \
  |  \
  |   \
  |    \
  |     \_______________
  |
  +-----|-----|-------->  y * f(x)
       0     1

Zero loss when y*f(x) >= 1 (correctly classified, outside margin).
Linear penalty when y*f(x) < 1.
```

进行物流损失 (物流回归) 的比较:

> 与逻辑回归的逻辑损失相比:

```
Hinge:     max(0, 1 - y*f(x))          Hard cutoff at margin
Logistic:  log(1 + exp(-y*f(x)))        Smooth, never exactly zero
```

损产生稀缺的解决方案 (只有支持向量有非零的贡献).物流损失使用所有数据点.这使得SVM在预测时间更有效的存储.

> 合页损失产生稀疏解解(只有支持向量有非零贡献) ――逻辑损失使用所有数据点――这使SVM在预测时更省内存――

### 训练直线SVM,梯度下降

您可以使用链损失的梯度下降加上L2规律化来训练线性SVM,而不需要解决限制的QP:

> 您可以在合页损失加 L2 正则化上使用梯度下降训练线性SVM,无需解约束二次规划:

```
L(w, b) = (lambda/2) * ||w||^2 + (1/n) * sum(max(0, 1 - y_i * (w^T x_i + b)))

Gradient with respect to w:
  If y_i * (w^T x_i + b) >= 1:  dL/dw = lambda * w
  If y_i * (w^T x_i + b) < 1:   dL/dw = lambda * w - y_i * x_i

Gradient with respect to b:
  If y_i * (w^T x_i + b) >= 1:  dL/db = 0
  If y_i * (w^T x_i + b) < 1:   dL/db = -y_i
```

这称为原始式.它运行在O(n * d) 每个时代,其中n是样本数,d是特征数.对于大小,稀少,高维度数据 (文本分类),这是快速的.

> 这被称为原始形式. 每轮运行时间为 O (n * d),其中 n 是样本数,d 是特征数.

> **【中文解读】**
> 合页损失 (Hinge Loss) 是SVM的核心损失函数:当样本正确分类且在间隔之外时损失为0,否则线性惩罚. 与逻辑回归交叉损失不同,合页损失产生稀疏解只有支持向量有非零贡献,预测时只需要存储这些点.

### 双重配方和核心技巧

根据第一阶段18课,KKT条件,SVM问题的拉格兰基双数是:

> 问题: 问题: 问题: 问题: 问题: 问题: 问题: 问题: 问题: 问题: 问题: 问题: 问题: 问题: 问题: 问题: 问题: 问题: 问题: 问题: 问题: 问题: 问题: 问题: 问题: 问题: 问题: 问题: 问题: 问题:

```
maximize    sum(alpha_i) - (1/2) * sum_ij(alpha_i * alpha_j * y_i * y_j * (x_i . x_j))
subject to  0 <= alpha_i <= C
            sum(alpha_i * y_i) = 0
```

双只涉及数据点之间的点产品x_i.x_j.这是关键见解.用内核函数K(x_i,x_j) 取代每个点产品,SVM可以学习非线性界限,而不会明确计算转换.

> 偶尔形式只涉及数据点之间的点积 x_i. x_j──这是关键洞察.将每个点积替换为核函数 K(x_i, x_j),SVM 就能学习非线性边界而无需显著计算变化──

```
Linear kernel:      K(x, z) = x . z
Polynomial kernel:  K(x, z) = (x . z + c)^d
RBF (Gaussian):     K(x, z) = exp(-gamma * ||x - z||^2)
```

 RBF 核将数据映射到无限维度空间中.输入空间中接近的点具有接近 1 的核值.距离较远的点具有接近 0 的核值.它可以学习任何平滑的决策界限.

> 核核将数据映射到无限维空间――输入空间中相近点核值接近1――远离点核值接近0――它可以学习任何光滑的决策边界――

```mermaid
graph LR
    subgraph "Input Space (not separable)"
        A["Data points in 2D<br>circular boundary"]
    end
    subgraph "Feature Space (separable)"
        B["Data points in higher dim<br>linear boundary"]
    end
    A -->|"Kernel trick<br>K(x,z) = phi(x).phi(z)"| B
```

核技巧在高维空间中计算点产量,但从来没有到达那里.对于 D 维度的多项内核,明确的特征空间有 O  D 维度.但 K  x, z 计算在 O  D 时间.

> 核技巧在高维空间中计算点积而无需实际到达那里――对于 D 维中的 d 次多项式核,显式特征空间有 O  D 维.

> **【中文解读】**
> 核技巧是SVM最优秀的数学贡献.对偶数形式只涉及数据点之间的点积 x_i · x_j,将其替换为核函数 K(x_i, x_j) 即可在高维度 (甚至无限维度) 空间中学习非线性边界,而无需显式计算高维映射.

> **【拓展：核技巧的思想在现代 AI 中的延续】**
> 核技巧的核心思想"在高维空间中计算相似性而不显然映射"在变压器的注意力机制中有类似体现.注意力分数 A(q,k) =软max(qK^T/√d) 本质上也是相似性核函数.

### 逆转的SVM (SVR)

支持向量回归将宽度的子环绕数据.子内部的点是零损失的.子以外的点是线性地处罚的.

> 支持向量回归在数据周围拟合一个宽度为一的管道──管道内的点损失为零──管道外的点被线性惩罚──

```
minimize    (1/2) ||w||^2 + C * sum(xi_i + xi_i*)
subject to  y_i - (w^T x_i + b) <= epsilon + xi_i
            (w^T x_i + b) - y_i <= epsilon + xi_i*
            xi_i, xi_i* >= 0
```

宽管 = 支持向量较少 = 适合性更高.窄管 = 支持向量较多 = 适合性更紧.

> 子 参数控制管道宽度――更宽的管道 = 更少的支持向量 = 更平滑的配合――更窄的管道 = 更多的支持向量 = 更紧密的配合――

### 为什么SVM输给深度学习 (以及当他们仍然赢得时)

从1990年代末到2010年代初,SVM主导了 ML.深度学习因多种原因超过了它们:

> 在20世纪90年代末至2010年代初,SVM主导了ML──深度学习超越了它们,原因如下:

| Factor | SVMs | Deep learning |
|--------|------|---------------|
| Feature engineering | Requires it | Learns features |
| Scalability | O(n^2) to O(n^3) for kernel | O(n) per epoch with SGD |
| Image/text/audio | Needs handcrafted features | Learns from raw data |
| Large datasets (>100k) | Slow | Scales well |
| GPU acceleration | Limited benefit | Massive speedup |

| 因素 | SVM | 深度学习 |
|------|-----|---------|
| 特征工程 | 需要手动 | 自动学习 |
| 可扩展性 | 核方法 O(n^2) 到 O(n^3) | SGD 每轮 O(n) |
| 图像/文本/音频 | 需要手工特征 | 从原始数据学习 |
| 大数据集（>10 万） | 较慢 | 扩展性好 |
| GPU 加速 | 有限收益 | 大幅提速 |

在这些情况下,SVM仍然赢得胜利:
- 小数据集 (数百到数千个样本)
  小数据集 ((数百到数千样本)
- 高维度稀疏数据 (含TF-IDF功能的文本)
  高维稀疏数据 (文本的TF-IDF特征)
- 需要数学保证时 (边际额度)
  需要数学保证时(间隔边界)
- 训练时间必须最小 (线性SVM非常快)
  训练时间必须最短时间 (非常快)
- 具有明确的利结构的二元分类
  具有清晰间隔结构的二分类
- 异常检测 (单类SVM)
  异常检测 (单类SVM)

> 由于此,SVM在以下情况下仍然胜出:

## 建立它,实现它.
```figure
svm-margin
```

## 建立它

### 步骤1:痕损失和梯度

根据,计算一批的杆损失及其梯度.

> 基础――计算数据集的合页损失及其梯度――

```python
def hinge_loss(X, y, w, b):
    n = len(X)
    total_loss = 0.0
    for i in range(n):
        margin = y[i] * (dot(w, X[i]) + b)  # 计算样本到决策边界的函数间隔
        total_loss += max(0.0, 1.0 - margin)  # 合页损失：间隔 < 1 时才有惩罚
    return total_loss / n  # 返回平均损失
```

### 步骤2:通过梯度下降的线性SVM

通过减少规律化关损失来训练.

> 通过最小化正则化合物损失训练――无需QP求解器――

```python
class LinearSVM:
    def __init__(self, lr=0.001, lambda_param=0.01, n_epochs=1000):
        self.lr = lr  # 学习率
        self.lambda_param = lambda_param  # 正则化参数（对应 1/C）
        self.n_epochs = n_epochs
        self.w = None  # 权重向量
        self.b = 0.0  # 偏置

    def fit(self, X, y):
        n_features = len(X[0])
        self.w = [0.0] * n_features
        self.b = 0.0

        for epoch in range(self.n_epochs):
            for i in range(len(X)):
                margin = y[i] * (dot(self.w, X[i]) + self.b)  # 函数间隔
                if margin >= 1:
                    # 样本在间隔之外，只需正则化梯度
                    self.w = [wj - self.lr * self.lambda_param * wj
                              for wj in self.w]
                else:
                    # 样本在间隔内或被误分类，需要额外的损失梯度
                    self.w = [wj - self.lr * (self.lambda_param * wj - y[i] * X[i][j])
                              for j, wj in enumerate(self.w)]
                    self.b -= self.lr * (-y[i])

    def predict(self, X):
        return [1 if dot(self.w, x) + self.b >= 0 else -1 for x in X]  # 根据符号预测类别
```

### 步骤3:内核函数

实现线性,多项和RBF核.

> 实现线性核、多项式核和RBF核──

```python
def linear_kernel(x, z):
    return dot(x, z)  # 线性核：直接点积

def polynomial_kernel(x, z, degree=3, c=1.0):
    return (dot(x, z) + c) ** degree  # 多项式核：(x·z + c)^d

def rbf_kernel(x, z, gamma=0.5):
    diff = [xi - zi for xi, zi in zip(x, z)]  # 计算差向量
    return math.exp(-gamma * dot(diff, diff))  # RBF 核：exp(-γ||x-z||²)
```

### 步骤4:边缘和支持向量识别

训练后,确定哪些点是支向量,并计算边缘宽度.

> 训练后,识别哪些点是支持向量并计算间隔宽度.

```python
def find_support_vectors(X, y, w, b, tol=1e-3):
    support_vectors = []
    for i in range(len(X)):
        margin = y[i] * (dot(w, X[i]) + b)
        if abs(margin - 1.0) < tol:
            support_vectors.append(i)
    return support_vectors
```

看到`code/svm.py`对于所有演示的全面实施.

> 完整实现 (含所有演示) 见`code/svm.py`,我知道.

## 用它实现框架

> **【中文解读】**
> 由于间隔依赖于特征尺度而SVM对特征尺度敏感; 2) 小数据集使用SVC(支持核函数),大数据集使用LinearSVC(使用原始形式,O(n) 每轮); 3) 马控制RBF核影响范围,太大→过拟合,太小→欠拟合.

通过"学习"

> 使用小说学习:

```python
from sklearn.svm import SVC, LinearSVC, SVR
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline

# 标准化 + SVM 的标准管线
clf = Pipeline([
    ("scaler", StandardScaler()),  # 标准化是 SVM 的必选项
    ("svm", SVC(kernel="rbf", C=1.0, gamma="scale")),  # RBF 核 SVM
])
clf.fit(X_train, y_train)
print(f"Accuracy: {clf.score(X_test, y_test):.4f}")
print(f"Support vectors: {clf['svm'].n_support_}")
```

重要:在训练SVM之前,总是扩展特征.SVM对特征大小敏感,因为边缘取决于未扩展的特征,而扭曲了几何学.

> 重要:训练SVM 前务必缩小特征――SVM对特征量级敏感,因为间隔依赖于变化,未缩小的特征会扭曲几何结构――

对于大型数据集,使用`LinearSVC`(原始表达式,O(n) 按时代)`SVC`(双式表达,O(n^2) 到O(n^3)):

> 对于大数据集,使用 `LinearSVC`没有任何其他方法`SVC`(对偶尔形式,O(n^2) 到O(n^3)):

```python
from sklearn.svm import LinearSVC

clf = Pipeline([
    ("scaler", StandardScaler()),
    ("svm", LinearSVC(C=1.0, max_iter=10000)),
])
```

## 练习题

1. 生成一个2D线性可分离的数据集.训练你的线性SVM并识别支持向量. 检查支持向量是决策边界最接近的点.
   1. 生成一个2D线性可分数据集――训练你的线性SVM 并识别支持向量――验证支持向量是离决策边界的最近点――

2. 在噪音集中的C从0.001到1000变化.为每个C值绘制决定界限.观察从宽边缘 (不适合) 到狭窄边缘 (过适合) 的过渡.
   2. 在有噪音的数据集中,将C从0.001 变化到1000――为每一个C 值绘制决策边界――观察从宽间隔 (缺合) 到狭间隔 (过合) 的转变――

3. 创建一个类界限圆形 (非线性) 的数据集. 显示线性SVM失败.计算RBF内核矩阵,并显示内核诱导的功能空间中类变得可分离.
   3. 创建一个类别边界为圆形的数据集――展示线性SVM 失败――计算RBF 核矩阵,展示在核诱导的特征空间中类别变得可分――

4. 根据数据集进行链损失与物流损失的比较.训练线性SVM和物流回归.计算每个模型的决策边界 (支持向量与所有点) 贡献多少训练点.
   4. 在同一数据集中,比较合页损失和逻辑损失――训练线性SVM和逻辑归归――统计每个模型的决策界限贡献了多少训练点(支持向量与所有点) ⋅

5. 执行SVR (epsilon-insensitive loss).将其调整为y = sin(x) +噪音. 围绕预测图画出epsilon管,并突出支持向量 (管外的点).
   5. 实现SVR(epsilon 不敏感损失) ・拟合 y = sin(x) +噪音──绘制预测周围的epsilon 管道并标记支持向量(管道外的点)。

## 关键词 快速查找表

| Term | What it actually means |
|------|----------------------|
| Support vectors | The training points closest to the decision boundary. The only points that determine the hyperplane |
| Margin | The distance between the decision boundary and the nearest support vectors. SVMs maximize this |
| Hinge loss | max(0, 1 - y*f(x)). Zero when correctly classified and outside the margin. Linear penalty otherwise |
| C parameter | Trade-off between margin width and classification errors. Large C = narrow margin, small C = wide margin |
| Soft margin | SVM formulation that allows margin violations via slack variables. Handles non-separable data |
| Kernel trick | Computing dot products in a high-dimensional feature space without explicitly mapping to that space |
| Linear kernel | K(x, z) = x . z. Equivalent to standard dot product. For linearly separable data |
| RBF kernel | K(x, z) = exp(-gamma * \|\|x-z\|\|^2). Maps to infinite dimensions. Learns any smooth boundary |
| Polynomial kernel | K(x, z) = (x . z + c)^d. Maps to a feature space of polynomial combinations |
| Dual formulation | Reformulation of the SVM problem that depends only on dot products between data points. Enables kernels |
| SVR | Support Vector Regression. Fits an epsilon-tube around the data. Points inside the tube have zero loss |
| Slack variables | xi_i: measures how much a point violates the margin. Zero for correctly classified points outside margin |
| Maximum margin | The principle of choosing the hyperplane that maximizes the distance to the nearest points of each class |

## 继续阅读 继续阅读

- [Vapnik: The Nature of Statistical Learning Theory (1995)](https://link.springer.com/book/10.1007/978-1-4757-3264-1)- 关于SVM和统计学学习的基础文本
  [Vapnik: The Nature of Statistical Learning Theory (1995)](https://link.springer.com/book/10.1007/978-1-4757-3264-1)- 统计学习理论的基础著作
- [Cortes & Vapnik: Support-vector networks (1995)](https://link.springer.com/article/10.1007/BF00994018)- 原始的SVM纸
  [Cortes & Vapnik: Support-vector networks (1995)](https://link.springer.com/article/10.1007/BF00994018)- 苏联原始论文
- [Platt: Sequential Minimal Optimization (1998)](https://www.microsoft.com/en-us/research/publication/sequential-minimal-optimization-a-fast-algorithm-for-training-support-vector-machines/)-使SM培训成为实践的SMO算法
  [Platt: Sequential Minimal Optimization (1998)](https://www.microsoft.com/en-us/research/publication/sequential-minimal-optimization-a-fast-algorithm-for-training-support-vector-machines/)- 使SVM训练成为实用的SMO算法
- [scikit-learn SVM documentation](https://scikit-learn.org/stable/modules/svm.html)- 具体实施的实践指南
  [scikit-learn SVM 文档](https://scikit-learn.org/stable/modules/svm.html)- 实用指南及实现细节
- [LIBSVM: A Library for Support Vector Machines](https://www.csie.ntu.edu.tw/~cjlin/libsvm/)- 支持大多数SVM实现的C++库
  [LIBSVM](https://www.csie.ntu.edu.tw/~cjlin/libsvm/)- 大多数SVM实现后背的C++库
