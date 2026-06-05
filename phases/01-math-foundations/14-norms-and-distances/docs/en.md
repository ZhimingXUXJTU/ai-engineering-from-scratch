# Norms and Distances | 范数与距离

> Your distance function defines what "similar" means. Choose wrong and everything downstream breaks.
> 距离函数定义了"相似"的含义。选错了，下游一切都崩溃。

**Type:** Build | **类型:** 动手
**Language:** Python | **语言:** Python
**Prerequisites:** Phase 1, Lessons 01 (Linear Algebra Intuition), 02 (Vectors, Matrices & Operations) | **前置知识:** Phase 1, Lessons 01-02
**Time:** ~90 minutes | **时间:** ~90 分钟

## Learning Objectives | 学习目标

- Implement L1, L2, cosine, Mahalanobis, Jaccard, and edit distance functions from scratch
  从零实现 L1、L2、余弦、马氏、Jaccard 和编辑距离函数
- Select the appropriate distance metric for a given ML task and explain why alternatives fail
  为给定 ML 任务选择合适的距离度量并解释为什么其他选择会失败
- Connect L1 and L2 norms to LASSO and Ridge regularization and their geometric constraint regions
  将 L1 和 L2 范数与 LASSO 和 Ridge 正则化及其几何约束区域联系起来
- Demonstrate how the same dataset produces different nearest neighbors under different metrics
  演示同一数据集在不同度量下产生不同的最近邻

> **【中文解读】**
> 距离函数定义了相似的含义。L1 对应 LASSO（特征选择），L2 对应 Ridge（防止过拟合），余弦距离适合词嵌入，编辑距离适合字符串。梯度裁剪用 L2 范数限制梯度大小。

## The Problem | 问题引入

> **【中文解读】** "这两个向量有多相似？"答案完全取决于你选什么距离函数。同一对数据在 L2 下是最近邻，在余弦距离下可能很远。KNN、推荐系统、向量数据库（RAG）、聚类算法——全都依赖距离函数的选择。选错了，模型优化的就是错误的目标。

## The Concept | 核心概念

> **【拓展：范数在 AI 中的四大应用】** (1) **L2 正则化**：`loss + lambda * ||w||_2^2`，防止权重过大，缓解过拟合；(2) **梯度裁剪**：`||grad|| > max_norm` 时缩放梯度，Transformer 训练的标配；(3) **余弦相似度**：RAG 检索和推荐系统的标准度量，只看方向不看大小；(4) **LayerNorm**：对每层输出做 L2 归一化，稳定训练过程。理解范数就是理解正则化和归一化的数学基础。

There is no universal best distance. L2 works for spatial data. Cosine similarity dominates NLP. Jaccard handles sets. Edit distance handles strings. Mahalanobis accounts for correlations. Wasserstein moves probability mass. Each one encodes a different assumption about what "similar" means.
> 没有万能的最佳距离。L2 适合空间数据，余弦相似度主导 NLP，Jaccard 处理集合，编辑距离处理字符串，马氏距离考虑相关性，Wasserstein 移动概率质量。每个都编码了关于"相似"含义的不同假设。

This lesson builds every major distance function from scratch, shows you when each one is the right tool, and demonstrates how the same data produces completely different nearest neighbors depending on which metric you use.
> 本课程从零构建每个主要距离函数，展示何时使用哪个，并演示相同数据在不同度量下产生完全不同的最近邻。

### Norms: measuring vector magnitude | 范数：衡量向量大小

A norm measures the "size" of a vector. Every distance function between two vectors can be written as the norm of their difference: d(a, b) = ||a - b||. So understanding norms is understanding distances.
> 范数衡量向量的"大小"。两个向量之间的距离函数可以写成它们差的范数。理解范数就是理解距离。

### L1 Norm (Manhattan distance) | L1 范数（曼哈顿距离）

The L1 norm sums the absolute values of all components.
> L1 范数将所有分量的绝对值相加。

```
||x||_1 = |x_1| + |x_2| + ... + |x_n|
```

It is called Manhattan distance because it measures how far you walk on a city grid where you can only move along axes. No diagonals.
> 叫曼哈顿距离因为它衡量在城市网格上沿轴移动的距离，不能走对角线。

When to use L1: high-dimensional sparse data, robustness to outliers, feature selection problems (L1 regularization promotes sparsity).
> 何时使用 L1：高维稀疏数据、对异常值的鲁棒性、特征选择问题。

Connection to L1 regularization (Lasso): adding ||w||_1 to your loss function pushes small weights to exactly zero, performing automatic feature selection. The L1 penalty creates diamond-shaped constraint regions, and corners lie on axes where some weights are zero.
> 与 L1 正则化 (Lasso) 的联系：在损失函数中加 ||w||_1 将小权重推到零，执行自动特征选择。L1 惩罚创建菱形约束区域，角点在轴上。

### L2 Norm (Euclidean distance) | L2 范数（欧氏距离）

The L2 norm is the straight-line distance. Square root of the sum of squared components.
> L2 范数是直线距离。分量平方和的平方根。

```
||x||_2 = sqrt(x_1^2 + x_2^2 + ... + x_n^2)
```

This is the distance you learned in geometry class. Pythagoras in n dimensions.
> 这是几何课上学到的距离。n 维的勾股定理。

Connection to L2 regularization (Ridge): adding ||w||_2^2 to your loss function penalizes large weights. Unlike L1, it does not push weights to zero. The L2 penalty creates circular constraint regions, so there are no corners on axes.
> 与 L2 正则化 (Ridge) 的联系：在损失函数中加 ||w||_2^2 惩罚大权重。与 L1 不同，它不会将权重推到零。L2 惩罚创建圆形约束区域。

```
MAE (L1 loss):  |y - y_hat|         Linear penalty. Robust to outliers. / 线性惩罚，对异常值鲁棒。
MSE (L2 loss):  (y - y_hat)^2       Quadratic penalty. Sensitive to outliers. / 二次惩罚，对异常值敏感。
```

### Lp Norms: the general family | Lp 范数：通用族

L1 and L2 are special cases of the Lp norm:
> L1 和 L2 是 Lp 范数的特例：

```
||x||_p = (|x_1|^p + |x_2|^p + ... + |x_n|^p)^(1/p)

p=1:    Diamond shape / 菱形
p=2:    Circle/sphere / 圆/球
p=inf:  Square/hypercube / 正方形/超立方体
```

### Cosine Similarity and Cosine Distance | 余弦相似度与余弦距离

Cosine similarity measures the angle between two vectors, ignoring their magnitudes.
> 余弦相似度衡量两个向量之间的角度，忽略大小。

```
cos_sim(a, b) = (a . b) / (||a||_2 * ||b||_2)
```

It ranges from -1 (opposite directions) to +1 (same direction). Cosine distance = 1 - cosine_similarity.
> 范围从 -1（相反方向）到 +1（相同方向）。余弦距离 = 1 - 余弦相似度。

Why cosine dominates NLP and embeddings: in text, document length should not affect similarity. A document about cats that is twice as long should still be "similar." Cosine similarity ignores magnitude and only cares about direction.
> 为什么余弦主导 NLP 和嵌入：在文本中，文档长度不应影响相似度。一篇关于猫的文档即使两倍长仍应"相似"。余弦相似度忽略大小，只关注方向。

### Mahalanobis Distance | 马氏距离

Euclidean distance treats all dimensions equally. Mahalanobis distance accounts for the covariance structure of the data.
> 欧氏距离对所有维度一视同仁。马氏距离考虑数据的协方差结构。

```
d_M(x, y) = sqrt((x - y)^T * S^(-1) * (x - y))
```

Intuitively: Mahalanobis distance first decorrelates and normalizes the data (whitening), then computes L2 distance in that transformed space.
> 直觉上：马氏距离先去相关并归一化数据（白化），然后在变换后的空间中计算 L2 距离。

### Jaccard Similarity (for sets) | Jaccard 相似度（集合）

Jaccard similarity measures overlap between two sets.
> Jaccard 相似度衡量两个集合的重叠。

```
J(A, B) = |A intersect B| / |A union B|
```

When to use Jaccard: comparing sets of tags, document similarity, near-duplicate detection, evaluating segmentation models (IoU = Jaccard).
> 何时使用 Jaccard：比较标签集、文档相似度、近似重复检测、评估分割模型（IoU = Jaccard）。

### Edit Distance (Levenshtein Distance) | 编辑距离（Levenshtein 距离）

Edit distance counts the minimum number of single-character operations needed to transform one string into another. Computed using dynamic programming.
> 编辑距离计算将一个字符串转换为另一个所需的最少单字符操作数。用动态规划计算。

```
"kitten" -> "sitting"
kitten -> sitten  (substitute k -> s)
sitten -> sittin  (substitute e -> i)
sittin -> sitting (insert g)

Edit distance = 3
```

### KL Divergence (not a distance, but used like one) | KL 散度（不是距离，但被当作距离使用）

KL divergence measures how one probability distribution differs from another. Critical property: NOT symmetric. D_KL(P || Q) != D_KL(Q || P). It is a divergence, not a distance.
> KL 散度衡量一个概率分布与另一个的差异。关键性质：不对称。它是散度，不是距离。

When you see KL divergence: VAEs, knowledge distillation, RLHF, policy gradient methods.
> 在以下场景看到 KL 散度：VAE、知识蒸馏、RLHF、策略梯度方法。

### Wasserstein Distance (Earth Mover's Distance) | Wasserstein 距离（推土机距离）

Wasserstein distance measures the minimum "work" needed to transform one probability distribution into another. It is a true metric (symmetric, satisfies triangle inequality). It provides gradients even when distributions do not overlap (KL divergence goes to infinity). This property made it central to WGANs.
> Wasserstein 距离衡量将一个概率分布转换为另一个所需的最小"功"。它是真正的度量（对称、满足三角不等式）。在分布不重叠时仍提供梯度（KL 散度变为无穷大）。这个性质使它成为 WGAN 的核心。

### Why Different Tasks Need Different Distances | 为什么不同任务需要不同距离

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

### Connection to Regularization | 与正则化的联系

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

Why L1 produces sparsity but L2 does not: picture the constraint region in 2D weight space. L1 is a diamond, L2 is a circle. The loss function's contours are most likely to touch the diamond at a corner, where one weight is zero. They touch the circle at a smooth point, where both weights are nonzero.
> 为什么 L1 产生稀疏性而 L2 不会：想象 2D 权重空间中的约束区域。L1 是菱形，L2 是圆形。损失函数的等高线最可能在菱形的角上接触，那里一个权重为零。在圆上的接触点是平滑的，两个权重都非零。

### Nearest Neighbor Search | 最近邻搜索

Approximate Nearest Neighbor (ANN) algorithms trade a small amount of accuracy for massive speed gains:
> 近似最近邻 (ANN) 算法用少量精度换取大幅加速：

```
Algorithm         Approach                      Used by
HNSW              Hierarchical navigable         FAISS, Qdrant, Weaviate
                  small-world graph
IVF               Inverted file index with       FAISS (billion-scale)
                  cluster-based search
Product quant.    Compress vectors, search       FAISS (memory-constrained)
                  in compressed space
```

HNSW is the dominant algorithm in modern vector databases.
> HNSW 是现代向量数据库中的主流算法。

## Build It | 动手实现

### Step 1: All norm and distance functions | 第1步：所有范数和距离函数

See `code/distances.py` for the complete implementation. Every function is built from scratch using only basic Python math.
> 完整实现见 `code/distances.py`。

### Step 2: Same data, different distances, different neighbors | 第2步：相同数据，不同距离，不同邻居

The demo in `distances.py` creates a dataset, picks a query point, and shows how the nearest neighbor changes depending on the distance metric.
> 演示创建数据集，选取查询点，展示最近邻如何随距离度量而变化。

### Step 3: Embedding similarity search | 第3步：嵌入相似度搜索

The code includes a mock embedding similarity search that finds the most similar "documents" to a query using cosine similarity vs L2 distance.
> 代码包含模拟嵌入相似度搜索，用余弦相似度和 L2 距离找最相似的"文档"。

## Use It | 用框架实现

The most common practical use: finding similar items in a vector database.
> 最常见的实际用途：在向量数据库中查找相似项。

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

When you call `model.encode(text)` and then search a vector database, this is what happens under the hood.
> 当你调用 `model.encode(text)` 然后搜索向量数据库时，这就是底层发生的事。

## Exercises | 练习题

1. Compute L1, L2, and L-infinity distances between (1, 2, 3) and (4, 0, 6). Verify that L-inf <= L2 <= L1 always holds. Prove why this ordering is guaranteed.
   计算 (1, 2, 3) 和 (4, 0, 6) 之间的 L1、L2 和 L-inf 距离。验证 L-inf <= L2 <= L1 始终成立。

2. Create two vectors where cosine similarity is high (> 0.9) but L2 distance is large (> 10). Explain geometrically.
   创建两个余弦相似度高（> 0.9）但 L2 距离大（> 10）的向量。几何解释。

3. Implement a function that returns the nearest neighbor under L1, L2, cosine, and Mahalanobis distance. Find a dataset where all four disagree.
   实现函数在 L1、L2、余弦和马氏距离下返回最近邻。找到四种度量全部不一致的数据集。

4. Compute Wasserstein distance between [0.5, 0.5, 0, 0] and [0, 0, 0.5, 0.5] using the CDF method.
   用 CDF 方法计算 [0.5, 0.5, 0, 0] 和 [0, 0, 0.5, 0.5] 的 Wasserstein 距离。

5. Implement MinHash for approximate Jaccard similarity. Compare with exact Jaccard.
   实现 MinHash 近似 Jaccard 相似度。与精确 Jaccard 比较。

## Key Terms | 术语速查表

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

## Further Reading | 延伸阅读

- [FAISS: A Library for Efficient Similarity Search](https://github.com/facebookresearch/faiss) - Meta's library for billion-scale ANN search
  Meta 的十亿级 ANN 搜索库
- [Wasserstein GAN (Arjovsky et al., 2017)](https://arxiv.org/abs/1701.07875) - Earth Mover's distance in GANs
  Wasserstein 距离在 GAN 中的应用
- [Efficient Estimation of Word Representations (Mikolov et al., 2013)](https://arxiv.org/abs/1301.3781) - Word2Vec, where cosine became the default
  Word2Vec，余弦相似度成为默认选择
- [sklearn.neighbors documentation](https://scikit-learn.org/stable/modules/neighbors.html) - practical guide to distance metrics
  距离度量的实践指南
