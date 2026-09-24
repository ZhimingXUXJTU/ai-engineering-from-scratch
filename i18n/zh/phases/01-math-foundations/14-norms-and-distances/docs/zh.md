# 规范和距离

> 你的距离函数定义了"类似"的意思.
> 距离函数定义了"相似"的含义.

**Type:** Build | **类型:** 动手
**Language:**子**语言:**字符串
**Prerequisites:** Phase 1, Lessons 01 (Linear Algebra Intuition), 02 (Vectors, Matrices & Operations) | **前置知识:** Phase 1, Lessons 01-02
**Time:** ~90 minutes | **时间:** ~90 分钟

## 学习目标

- 实现L1,L2,kosine,Mahalanobis,Jaccard,并从零编辑距离函数
  从零实现 L1、L2、余弦、马氏、杰卡德 和编辑距离函数
- 选择给定的 ML 任务的适当距离指标,并解释替代方案为什么失败
  为确定ML任务选择合适的距离度并解释为什么其他选择会失败
- 连接L1和L2标准到LASSO和Ridge规范化及其几何限制区域
  将L1和L2范数与LASSO和Ridge正规化及其几何约束区域联系起来
- 展示相同数据集如何在不同的指标下产生不同的近邻
  演示相同的数据集在不同度量下产生不同的近邻

> **【中文解读】**
> 距离函数定义了相似的含义──L1对应 LASSO(特征选择),L2对应 Ridge(防止过拟合),余弦距离适合词嵌入,编辑距离适合字符串──梯度剪切 L2 范数限制梯度大小──

## 问题 问题引入

> **【中文解读】**"这两个向量有多相似?"答案完全取决于你选择的距离函数. L2 下的数据对是最近的邻居,余弦距离下可能很远.

## 概念的核心概念

> **【拓展：范数在 AI 中的四大应用】**(1) 其他**L2 正则化**其他:`loss + lambda * ||w||_2^2`防止权重过大,缓解过拟合;**梯度裁剪**其他:`||grad|| > max_norm`时缩放梯度,变压器 训练的标配;**余弦相似度** 检索和推系统的标准度量,只看方向不看大小;**LayerNorm**对于每个层输出做 L2 归结,稳定训练过程.

没有通用最佳距离.L2用于空间数据.宇宙相似性占据了NLP的主导地位.杰卡德处理集合.编辑距离处理字符串.马哈拉诺比斯计算了相关性.瓦斯斯坦移动了概率质量.每个编码了不同的假设关于"相似"的意思.
> 没有万能的最佳距离――L2 适合空间数据,余弦相似度主导NLP,杰卡德处理集合,编辑处理距离字符串,马氏距离考虑相关性,瓦斯斯坦 移动概率质量――每个编码了关于"相似"意义的不同假设――

这一课将从零开始构建每个主要距离函数, 显示每个工具是什么时候正确的工具, 并展示相同的数据如何产生完全不同的近邻,
> 本课程从零构建每个主要距离函数,展示何时使用哪个,并演示相同数据在不同度量下产生完全不同的近邻.

### 标准:测量向量大小

标准测量向量的"大小".两个向量的每一个距离函数都可以作为它们的差异的标准写成: d(a, b) =a - b) 时时.
> 范数量量量向量的"大小"――两个向量的距离函数可以写成它们差的范数――理解范数就是理解距离――

### 现在,我们在美国,我们在美国,我们在美国,我们在美国,我们在美国,我们在美国,我们在美国,我们在美国,我们在美国,我们在美国,我们在美国,我们在美国,我们在美国,我们在美国,我们在美国,我们在美国,我们在美国,我们在美国,我们在美国,我们在美国,我们在美国,我们在美国,我们在美国,我们在美国,我们在美国,我们在美国,我们在美国,我们在美国,我们在美国,我们在美国,我们在美国,我们在美国,我们在美国,我们在美国,我们在美国,我们在美国,我们在美国,我们在美国,我们在美国,我们在美国,我们在美国,我们在美国,我们在美国,我们在美国,我们在美国,我们在美国,我们在美国,我们在美国,我们在美国,我们在美国,我们在美国,我们,我们在美国,我们,我们在美国,我们,我们在美国,我们,我们在美国,我们,我们在美国,我们,我们,我们在美国,我们,我们,我们,我们,我们在美国,我们,我们,我们,我们,我们,我们,我们,我们,我们,我们在美国,我们,我们,我们,我们,我们,我们,我们,我们,我们,我们,我们,我们,我们,我们,我们,我们,我们,我们,我们,我们,我们,我们,我们,我们,我们,我们,我们,我们,我们,我们,我们,我们,我们,我们,我们,我们,我们,我们,我们,我们,我们,我们,我们,我们,我们,我们,我们,我们,我们,我们,我们,我们,我们,我们,我们,我们,我们,我们,我们,我们,我们,我们,我们,我们,我们,我们,我们,我们,我们,我们,我们,我们,我们,我们,我们,我们,我们,我们,我们,我们,我们,我们,我们,我们,我们,我们,我们,我们,我们,我们,我们,我们,我们,我们,

标准L1总结了所有组件的绝对值.
> 范数将所有分数的绝对值相加.

```
||x||_1 = |x_1| + |x_2| + ... + |x_n|
```

它被称为曼哈顿距离,因为它测量你在城市网格上走多远,
> 曼哈顿距离是因为它衡量了城市网格上沿轴移动的距离,不能走对角线.

如何使用L1:高维度稀疏数据,强度到异常值,特征选择问题 (L1规律化促进稀疏性).
> 如何使用L1:高维稀疏数据,对异常值的鲁棒性,特征选择问题

连接到L1调整:添加到你的输失函数 (Lasso) 增加小权重到完全零,执行自动特征选择.L1罚款创造了钻石形的限制区域,角落位于某些权重为零的轴上.
> 与 L1 正则化 (Lasso) 联系:在失败函数中加小权重推至零,执行自动特征选择――L1 惩罚创建形束区域,角点在轴上――

### ,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,

标准是直线距离,正方根是正方体组件的总数.
> L2 范数是直线距离的分量平方和的平方根.

```
||x||_2 = sqrt(x_1^2 + x_2^2 + ... + x_n^2)
```

这就是你在几何课中学到的距离.
> 这就是几何学上学到的距离.

连接到L2调整:将UnwwE2加到你的损失函数,会惩罚大重量.就像L1,它不会把重量推到零.L2的惩罚会创造圆形的限制区域,因此轴上没有角.
> 与L2 正则化 (正则化) 的联系:在损失函数中中加2

```
MAE (L1 loss):  |y - y_hat|         Linear penalty. Robust to outliers. / 线性惩罚，对异常值鲁棒。
MSE (L2 loss):  (y - y_hat)^2       Quadratic penalty. Sensitive to outliers. / 二次惩罚，对异常值敏感。
```

### 标签: 标签: 标签: 标签: 标签: 标签: 标签: 标签: 标签: 标签: 标签: 标签: 标签: 标签: 标签: 标签: 标签: 标签: 标签: 标签: 标签: 标签: 标签: 标签: 标签: 标签: 标签: 标签: 标签: 标签: 标签: 标签: 标签: 标签: 标签: 标签: 标签: 标签: 标签: 标签: 标签: 标签: 标签

L1和L2是Lp标准的特殊案例:
> L1 和 L2 是 Lp 范数的特例:

```
||x||_p = (|x_1|^p + |x_2|^p + ... + |x_n|^p)^(1/p)

p=1:    Diamond shape / 菱形
p=2:    Circle/sphere / 圆/球
p=inf:  Square/hypercube / 正方形/超立方体
```

### 余弦相似度与余弦距离

两向量之间的角度,不考虑它们的大小.
> 余弦相似度衡量两个向量之间的角,忽略大小.

```
cos_sim(a, b) = (a . b) / (||a||_2 * ||b||_2)
```

它从 -1 (相反方向) 到 +1 (相同方向). 位数距离 = 1 - 位数_相似性.
> 范围从 -1 相反方向) 到 +1 相同方向) ――余弦距离 = 1 - 余弦相似度──

为什么Cosin占据了NLP和嵌入式的地位:在文本中,文档长度不应该影响相似性.关于猫的文档长度是两倍的,应该仍然是"相似的".Cosin相似性忽视大小,只关心方向.
> 为什么余弦主导 NLP 和嵌入:在文本中,文档长度不应影响相似度――一篇关于猫文档即使两倍长度仍然应"相似"――余弦相似度忽略大小,只关注方向――

### 马氏距离

欧基德式距离对待所有维度均等. 马哈拉诺比距离对数据的共变结构负责.
> 欧氏距离对所有维度的同仁视力.

```
d_M(x, y) = sqrt((x - y)^T * S^(-1) * (x - y))
```

直观:马哈拉诺比距离首先调解和正常化数据 (白化),然后计算在转换空间中的L2距离.
> 直觉上:马氏距离先去相关并归纳数据 (白化),然后在变化后的空间中计算 L2 距离――

### 杰卡德相似度 (集合)

杰卡德的相似度测量重叠了两个组.
> 杰卡德相似度衡量两个集合的重叠.

```
J(A, B) = |A intersect B| / |A union B|
```

使用Jaccard的时间:比较标签集,文件相似性,近似重复检测,评估细分模型 (IoU = Jaccard).
> 何时使用Jaccard:比较标签集、文档相似度、近似重复检测、评估分类模型 ((IoU = Jaccard) 』

### 编辑距离

编辑距离计算一个字符串转换成另一个字符串所需的单字符操作的最小数量.
> 编辑距离计算将一个字符串转换为另一个所需的最小单字符操作数――用动态规划计算――

```
"kitten" -> "sitting"
kitten -> sitten  (substitute k -> s)
sitten -> sittin  (substitute e -> i)
sittin -> sitting (insert g)

Edit distance = 3
```

### 距离不太远,但被当作距离使用)

基因差距测量一个概率分布与另一个分布不同.关键属性:非对称.
> 散度衡量一个概率分布与另一个差异.

对于这些问题,我们需要注意:
> 在以下场景中看 KL 散度:VAE、知识蒸、RLHF、策略梯度方法──

### 瓦斯斯坦距离 (地球移动距离) 瓦斯斯坦距离

瓦斯斯特恩距离测量了转换一个概率分布到另一个所需的最小"工作".它是一个真正的指标 (对称,满足三角形不平等).即使分布没有重叠 (KL差距到无限).这种属性使其成为WGAN的核心.
> 瓦斯斯特林的距离测量将一个概率分布转换为另一个所需的最小"功"――它是真正的测量量――对称,满足三角不等式. 在分布不重叠时,仍然提供梯度.

### 为什么不同的任务需要不同的距离

| Task / 任务 | Best distance / 最佳距离 | Why / 原因 |
|------|--------------|-----|
| Text similarity / 文本相似度 | Cosine / 余弦 | Magnitude is noise, direction is meaning / 大小是噪声，方向是含义 |
| Image pixel comparison / 图像像素比较 | L2 | Spatial relationships matter / 空间关系重要 |
| Sparse high-dim features / 稀疏高维特征 | L1 | Robust, does not amplify rare large differences / 鲁棒 |
| Set overlap / 集合重叠 | Jaccard | Data is naturally set-valued / 数据天然是集合 |
| String matching / 字符串匹配 | Edit distance / 编辑距离 | Operations map to human editing / 操作映射人类编辑 |
| Outlier detection / 异常检测 | Mahalanobis / 马氏距离 | Accounts for feature correlations / 考虑特征相关性 |
| GAN training / GAN 训练 | Wasserstein | Provides gradients without overlap / 不重叠时仍提供梯度 |
| Embeddings (vector DB) / 嵌入（向量数据库） | Cosine or dot product / 余弦或点积 | Embeddings encode meaning in direction / 嵌入在方向中编码含义 |

### 对于规律化和规律化的联系.

```
L1 regularization (Lasso):   loss + lambda * ||w||_1
  -> Sparse weights. Some weights become exactly zero. / 稀疏权重，某些权重变为零。
  -> Automatic feature selection. / 自动特征选择。

L2 regularization (Ridge):   loss + lambda * ||w||_2^2
  -> Small weights. All weights shrink toward zero. / 小权重，所有权重向零收缩。
  -> No feature selection. / 无特征选择。

Elastic Net:                  loss + lambda_1 * ||w||_1 + lambda_2 * ||w||_2^2
  -> Combines sparsity of L1 with stability of L2. / 结合 L1 的稀疏性和 L2 的稳定性。
```

为什么L1产生稀疏性,但L2没有:在2D权重空间中描绘制约束区域.L1是一个钻石,L2是一个圆.损失函数的轮最有可能触及角落的钻石,其中一个权重是零.它们触及圆圈在平滑点,其中两个权重是非零.
> 为什么L1 产生稀疏性而L2 不会:想象 2D 权重空间中的束区域――L1 是形,L2 是圆形――损失函数等高线最可能在形角上接触,在那里一个权重为零――在圆上接触点是平平平,两个权重都非零――

### 最近邻居搜索 最近邻居搜索

接近近邻 (ANN) 算法以小的精度进行交易,
> 类似近邻 (ANN) 算法使用少量精度换取大幅加速:

```
Algorithm         Approach                      Used by
HNSW              Hierarchical navigable         FAISS, Qdrant, Weaviate
                  small-world graph
IVF               Inverted file index with       FAISS (billion-scale)
                  cluster-based search
Product quant.    Compress vectors, search       FAISS (memory-constrained)
                  in compressed space
```

现代向量数据库中,HNSW是主导的算法.
> 现代向量数据库中主要流算法.

## 建立它,实现它.
```figure
norm-unit-balls
```

## 建立它

### 步骤1:所有规范和距离函数.

看到`code/distances.py`每个函数都是从零开始构建的,只使用基本的Python数学.
> 完整实现见`code/distances.py`,我知道.

### 步骤2:相同的数据,不同的距离,不同的邻居.

演示在`distances.py`创建数据集,选择查询点,并显示最近的邻居如何根据距离的测量变化.
> 展示创建数据集,选择查询点,展示近邻如何随距离量而变化.

### 步骤3:嵌入相似性搜索

该代码包括一个模拟嵌入式类似性搜索,该代码使用kosine相似性与L2距离的查询找到最相似的"文件".
> 代码包含模拟嵌入式相似度搜索,使用余弦相似度和L2 距离寻找最相似的"文档"――

## 用它实现框架

最常见的实用用途:在向量数据库中找到类似的项目.
> 最常见的实际用途:在向量数据库中搜索相似项.

```python
import numpy as np

def cosine_similarity_matrix(X):
    norms = np.linalg.norm(X, axis=1, keepdims=True)
    norms = np.where(norms == 0, 1, norms)
    X_normalized = X / norms
    return X_normalized @ X_normalized.T

embeddings = np.random.randn(1000, 768)

sim_matrix = cosine_similarity_matrix(embeddings)

query_idx = 0
similarities = sim_matrix[query_idx]
top_k = np.argsort(similarities)[::-1][1:6]
print(f"Top 5 most similar to item 0: {top_k}")
print(f"Similarities: {similarities[top_k]}")
```

当你打电话时`model.encode(text)`然后搜索向量数据库,这是发生在罩杯下的事情.
> 当你调用`model.encode(text)`然后在搜索量数据库时,这就是底层发生的事情.

## 练习题

1. 计算 (1, 2, 3) 和 (4, 0, 6) 之间的 L1, L2 和 L-无限距离. 检查 L-inf <= L2 <= L1 总是保持. 证明为什么这个顺序是保证的.
   计算 (1, 2, 3) 和 (4, 0, 6) 之间的 L1、L2 和 L-inf 距离――验证 L-inf <= L2 <= L1始终成立──

2. 创建两个向量,其中的相似性高 (> 0.9) ,但L2距离大 (> 10).
   创建两个余弦相似度高(> 0.9) 但L2 距离大(> 10) 的向量──几何解释──

3. 执行一个函数,将近邻在L1,L2,kosine和Mahalanobis距离下返回.找到四个不同意的数据集.
   实现函数在 L1、L2、余弦和马氏距离下回近邻. 找到四种尺度全部不一致的数据集.

4. 使用CDF方法计算[0.5,0.5,0,0]和[0,0,0,0,5,0.5]之间的瓦斯斯特林距离.
   用CDF 方法计算 [0.5,0.5,0,0] 和 [0,0,0.5,0.5] 的Wasserstein距离

5. 运用MinHash来获得一个接近Jaccard的相似性.
   实现MinHash 近似Jaccard 相似度──与精确Jaccard 比较──

## 关键词 快速查找表

| Term / 术语 | What people say | What it actually means / 实际含义 |
|------|----------------|----------------------|
| Norm / 范数 | "Size of a vector" | A function that maps a vector to a non-negative scalar / 将向量映射到非负标量的函数 |
| L1 norm / L1 范数 | "Manhattan distance" | Sum of absolute component values. Produces sparsity. / 分量绝对值之和。产生稀疏性。 |
| L2 norm / L2 范数 | "Euclidean distance" | Square root of sum of squared components. / 分量平方和的平方根。 |
| Cosine similarity / 余弦相似度 | "Angle between vectors" | Dot product normalized by both magnitudes. Ranges -1 to +1. / 双方大小归一化的点积。范围 -1 到 +1。 |
| Mahalanobis distance / 马氏距离 | "Correlation-aware distance" | L2 distance in whitened space using covariance matrix. / 用协方差矩阵白化后的 L2 距离。 |
| Jaccard similarity / Jaccard 相似度 | "Set overlap" | Intersection size divided by union size. / 交集大小除以并集大小。 |
| Edit distance / 编辑距离 | "Levenshtein distance" | Minimum insertions, deletions, substitutions to transform strings. / 转换字符串的最少插入、删除、替换次数。 |
| KL divergence / KL 散度 | "Distance between distributions" | Not a true distance (not symmetric). / 不是真正的距离（不对称）。 |
| Wasserstein distance / Wasserstein 距离 | "Earth mover's distance" | Minimum work to transport mass between distributions. A true metric. / 在分布间传输质量的最小功。真正的度量。 |
| HNSW | "The vector DB algorithm" | Multi-layer graph for fast approximate nearest neighbor search. / 用于快速近似最近邻搜索的多层图。 |
| L1 regularization / L1 正则化 | "Lasso" | Drives weights to zero (sparsity). / 将权重驱动到零（稀疏性）。 |
| L2 regularization / L2 正则化 | "Ridge" or "weight decay" | Shrinks weights toward zero without sparsity. / 将权重向零收缩但不产生稀疏性。 |
| Elastic Net / 弹性网络 | "L1 + L2" | Combines L1 and L2 regularization. / 结合 L1 和 L2 正则化。 |

## 继续阅读 继续阅读

- [FAISS: A Library for Efficient Similarity Search](https://github.com/facebookresearch/faiss)- 测量数据库用于数亿次的ANN搜索
  测量的亿级 ANN 搜索库
- [Wasserstein GAN (Arjovsky et al., 2017)](https://arxiv.org/abs/1701.07875)- 机的距离在GAN中
  瓦斯斯坦 距离在GAN中应用
- [Efficient Estimation of Word Representations (Mikolov et al., 2013)](https://arxiv.org/abs/1301.3781)- Word2Vec,其中的代码是默认的
  词2Vec,余弦相似度成为默认选择
- [sklearn.neighbors documentation](https://scikit-learn.org/stable/modules/neighbors.html)- 距离指标的实用指南
  距离量实践指南
