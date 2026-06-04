# 无监督学习

> 没有标签，没有老师。算法自己发现结构。

**类型：** 构建
**语言：** Python
**前置知识：** Phase 1（范数与距离、概率与分布），Phase 2 第 1-6 课
**时长：** 约 90 分钟

## 学习目标

- 从零实现 K-Means、DBSCAN 和高斯混合模型 (GMM)，比较它们的聚类行为
- 使用轮廓系数和肘部法评估聚类质量，选择最优 K
- 解释 DBSCAN 何时优于 K-Means，识别哪种算法能处理非球形簇和异常值
- 使用聚类方法构建异常检测管线，标记偏离正常模式的点

## 问题引入

到目前为止的每一课 ML 都假设有标签数据："这是输入，这是正确输出"。在真实世界中，标签是昂贵的。一家医院有数百万条患者记录，但没有人手动标记每一条的疾病类别。一个电商网站有数百万次用户会话，但没有人手工标注客户分群。一个安全团队有网络日志，但没有人标记每个异常。

无监督学习在不知道该找什么的情况下发现模式。它将相似的数据点分组，发现隐藏结构，浮现异常。如果说监督学习是看有答案的教科书学习，无监督学习就是盯着原始数据直到模式自己浮现。

关键问题：没有标签，你无法直接衡量"对"或"错"。你需要不同的工具来评估算法发现的结构是否有意义。

## 核心概念

### 聚类：将相似的东西分组

聚类将每个数据点分配到一个组（簇），使同一组内的点比其他组的点更相似。问题始终是："相似"意味着什么？

```mermaid
flowchart LR
    A[原始数据] --> B{选择方法}
    B --> C[K-Means]
    B --> D[DBSCAN]
    B --> E[层次聚类]
    B --> F[GMM]
    C --> G[扁平、球形簇]
    D --> H[任意形状、噪声检测]
    E --> I[嵌套簇的树]
    F --> J[软分配、椭圆簇]
```

### K-Means：主力算法

K-Means 将数据划分为恰好 K 个簇。每个簇有一个质心（重心），每个点属于最近的质心。

Lloyd 算法：

1. 随机选择 K 个点作为初始质心
2. 将每个数据点分配到最近的质心
3. 重新计算每个质心为其分配点的均值
4. 重复步骤 2-3 直到分配不再变化

目标函数（惯性/Inertia）衡量每个点到其分配质心的总平方距离。K-Means 最小化这个值，但只找到局部最小值。不同的初始化可能产生不同的结果。

### 选择 K

两种标准方法：

**肘部法则 (Elbow Method)：** 对 K = 1, 2, 3, ..., n 运行 K-Means。绘制惯性 vs K 的图。寻找"肘部"——添加更多簇不再显著减少惯性的位置。

**轮廓系数 (Silhouette Score)：** 对每个点，测量它与自己簇的相似度 (a) 和与最近其他簇的相似度 (b)。轮廓系数为 (b - a) / max(a, b)，范围从 -1（错误簇）到 +1（好的聚类）。对所有点取平均得到全局分数。

### DBSCAN：基于密度的聚类

K-Means 假设簇是球形的，并且需要你预先选 K。DBSCAN 不做这些假设。它将簇发现为被稀疏区域分隔的密集区域。

两个参数：
- **eps**：邻域的半径
- **min_samples**：形成密集区域所需的最小点数

三种类型的点：
- **核心点 (Core Point)**：eps 距离内至少有 min_samples 个点
- **边界点 (Border Point)**：在某个核心点的 eps 内但自身不是核心点
- **噪声点 (Noise Point)**：既不是核心点也不是边界点。这些是异常值。

DBSCAN 将互相在 eps 内的核心点连接到同一个簇。边界点加入附近核心点的簇。噪声点不属于任何簇。

优势：发现任意形状的簇，自动确定簇的数量，识别异常值。劣势：难以处理密度不同的簇。

### 层次聚类

构建嵌套簇的树（树状图/Dendrogram）。

聚合式（自底向上）：
1. 从每个点作为自己的簇开始
2. 合并两个最近的簇
3. 重复直到只剩一个簇
4. 在所需层级切割树状图得到 K 个簇

簇之间的"近"可以用以下方式衡量：
- **单链接 (Single Linkage)**：两个簇中任意两点间的最小距离
- **全链接 (Complete Linkage)**：任意两点间的最大距离
- **平均链接 (Average Linkage)**：所有点对的平均距离
- **Ward 方法**：导致簇内总方差增加最小的合并

### 高斯混合模型 (GMM)

K-Means 给出硬分配：每个点恰好属于一个簇。GMM 给出软分配：每个点有属于每个簇的概率。

GMM 假设数据由 K 个高斯分布混合生成，每个有自己的均值和协方差。期望最大化 (EM) 算法交替进行：

- **E 步**：计算每个点属于每个高斯分布的概率
- **M 步**：更新每个高斯分布的均值、协方差和混合权重以最大化数据的似然

GMM 可以建模椭圆簇（不只是 K-Means 那样的球形），自然处理重叠簇。

### 何时用哪种方法

| 方法 | 适合 | 避免 |
|------|------|------|
| K-Means | 大数据集、球形簇、已知 K | 不规则形状、有异常值 |
| DBSCAN | 未知 K、任意形状、异常检测 | 密度差异大、非常高维 |
| 层次聚类 | 小数据集、需要树状图、未知 K | 大数据集（O(n^2) 内存） |
| GMM | 重叠簇、需要软分配 | 非常大的数据集、维度太多 |

### 用聚类做异常检测

聚类天然支持异常检测：
- **K-Means**：远离任何质心的点是异常
- **DBSCAN**：噪声点按定义就是异常
- **GMM**：在所有高斯分布下概率都很低的点是异常

## 动手实现

### 步骤 1：从零实现 K-Means

```python
import math
import random


def euclidean_distance(a, b):
    return math.sqrt(sum((ai - bi) ** 2 for ai, bi in zip(a, b)))


def kmeans(data, k, max_iterations=100, seed=42):
    random.seed(seed)
    n_features = len(data[0])

    centroids = random.sample(data, k)

    for iteration in range(max_iterations):
        clusters = [[] for _ in range(k)]
        assignments = []

        for point in data:
            distances = [euclidean_distance(point, c) for c in centroids]
            nearest = distances.index(min(distances))
            clusters[nearest].append(point)
            assignments.append(nearest)

        new_centroids = []
        for cluster in clusters:
            if len(cluster) == 0:
                new_centroids.append(random.choice(data))
                continue
            centroid = [
                sum(point[j] for point in cluster) / len(cluster)
                for j in range(n_features)
            ]
            new_centroids.append(centroid)

        if all(
            euclidean_distance(old, new) < 1e-6
            for old, new in zip(centroids, new_centroids)
        ):
            print(f"  在第 {iteration + 1} 次迭代收敛")
            break

        centroids = new_centroids

    return assignments, centroids
```

### 步骤 2：肘部法则和轮廓系数

```python
def compute_inertia(data, assignments, centroids):
    total = 0.0
    for point, cluster_id in zip(data, assignments):
        total += euclidean_distance(point, centroids[cluster_id]) ** 2
    return total


def silhouette_score(data, assignments):
    n = len(data)
    if n < 2:
        return 0.0

    clusters = {}
    for i, c in enumerate(assignments):
        clusters.setdefault(c, []).append(i)

    if len(clusters) < 2:
        return 0.0

    scores = []
    for i in range(n):
        own_cluster = assignments[i]
        own_members = [j for j in clusters[own_cluster] if j != i]

        if len(own_members) == 0:
            scores.append(0.0)
            continue

        a = sum(euclidean_distance(data[i], data[j]) for j in own_members) / len(own_members)

        b = float("inf")
        for cluster_id, members in clusters.items():
            if cluster_id == own_cluster:
                continue
            avg_dist = sum(euclidean_distance(data[i], data[j]) for j in members) / len(members)
            b = min(b, avg_dist)

        if max(a, b) == 0:
            scores.append(0.0)
        else:
            scores.append((b - a) / max(a, b))

    return sum(scores) / len(scores)


def find_best_k(data, max_k=10):
    print("肘部法则:")
    inertias = []
    for k in range(1, max_k + 1):
        assignments, centroids = kmeans(data, k)
        inertia = compute_inertia(data, assignments, centroids)
        inertias.append(inertia)
        print(f"  K={k}: 惯性={inertia:.2f}")

    print("\n轮廓系数:")
    for k in range(2, max_k + 1):
        assignments, centroids = kmeans(data, k)
        score = silhouette_score(data, assignments)
        print(f"  K={k}: 轮廓系数={score:.4f}")

    return inertias
```

### 步骤 3：从零实现 DBSCAN

```python
def dbscan(data, eps, min_samples):
    n = len(data)
    labels = [-1] * n
    cluster_id = 0

    def region_query(point_idx):
        neighbors = []
        for i in range(n):
            if euclidean_distance(data[point_idx], data[i]) <= eps:
                neighbors.append(i)
        return neighbors

    visited = [False] * n

    for i in range(n):
        if visited[i]:
            continue
        visited[i] = True

        neighbors = region_query(i)

        if len(neighbors) < min_samples:
            labels[i] = -1
            continue

        labels[i] = cluster_id
        seed_set = list(neighbors)
        seed_set.remove(i)

        j = 0
        while j < len(seed_set):
            q = seed_set[j]

            if not visited[q]:
                visited[q] = True
                q_neighbors = region_query(q)
                if len(q_neighbors) >= min_samples:
                    for nb in q_neighbors:
                        if nb not in seed_set:
                            seed_set.append(nb)

            if labels[q] == -1:
                labels[q] = cluster_id

            j += 1

        cluster_id += 1

    return labels
```

### 步骤 4：高斯混合模型（EM 算法）

```python
def gmm(data, k, max_iterations=100, seed=42):
    random.seed(seed)
    n = len(data)
    d = len(data[0])

    indices = random.sample(range(n), k)
    means = [list(data[i]) for i in indices]
    variances = [1.0] * k
    weights = [1.0 / k] * k

    def gaussian_pdf(x, mean, variance):
        d = len(x)
        coeff = 1.0 / ((2 * math.pi * variance) ** (d / 2))
        exponent = -sum((xi - mi) ** 2 for xi, mi in zip(x, mean)) / (2 * variance)
        return coeff * math.exp(max(exponent, -500))

    for iteration in range(max_iterations):
        responsibilities = []
        for i in range(n):
            probs = []
            for j in range(k):
                probs.append(weights[j] * gaussian_pdf(data[i], means[j], variances[j]))
            total = sum(probs)
            if total == 0:
                total = 1e-300
            responsibilities.append([p / total for p in probs])

        old_means = [list(m) for m in means]

        for j in range(k):
            r_sum = sum(responsibilities[i][j] for i in range(n))
            if r_sum < 1e-10:
                continue

            weights[j] = r_sum / n

            for dim in range(d):
                means[j][dim] = sum(
                    responsibilities[i][j] * data[i][dim] for i in range(n)
                ) / r_sum

            variances[j] = sum(
                responsibilities[i][j]
                * sum((data[i][dim] - means[j][dim]) ** 2 for dim in range(d))
                for i in range(n)
            ) / (r_sum * d)
            variances[j] = max(variances[j], 1e-6)

        shift = sum(
            euclidean_distance(old_means[j], means[j]) for j in range(k)
        )
        if shift < 1e-6:
            print(f"  GMM 在第 {iteration + 1} 次迭代收敛")
            break

    assignments = []
    for i in range(n):
        assignments.append(responsibilities[i].index(max(responsibilities[i])))

    return assignments, means, weights, responsibilities
```

### 步骤 5：生成测试数据并运行

```python
def make_blobs(centers, n_per_cluster=50, spread=0.5, seed=42):
    random.seed(seed)
    data = []
    true_labels = []
    for label, (cx, cy) in enumerate(centers):
        for _ in range(n_per_cluster):
            x = cx + random.gauss(0, spread)
            y = cy + random.gauss(0, spread)
            data.append([x, y])
            true_labels.append(label)
    return data, true_labels


def make_moons(n_samples=200, noise=0.1, seed=42):
    random.seed(seed)
    data = []
    labels = []
    n_half = n_samples // 2
    for i in range(n_half):
        angle = math.pi * i / n_half
        x = math.cos(angle) + random.gauss(0, noise)
        y = math.sin(angle) + random.gauss(0, noise)
        data.append([x, y])
        labels.append(0)
    for i in range(n_half):
        angle = math.pi * i / n_half
        x = 1 - math.cos(angle) + random.gauss(0, noise)
        y = 1 - math.sin(angle) - 0.5 + random.gauss(0, noise)
        data.append([x, y])
        labels.append(1)
    return data, labels


if __name__ == "__main__":
    centers = [[2, 2], [8, 3], [5, 8]]
    data, true_labels = make_blobs(centers, n_per_cluster=50, spread=0.8)

    print("=== K-Means 聚类（3 个簇）===")
    assignments, centroids = kmeans(data, k=3)
    print(f"  质心: {[[round(c, 2) for c in cent] for cent in centroids]}")
    sil = silhouette_score(data, assignments)
    print(f"  轮廓系数: {sil:.4f}")

    print("\n=== 肘部法则 ===")
    find_best_k(data, max_k=6)

    print("\n=== DBSCAN（3 个簇）===")
    db_labels = dbscan(data, eps=1.5, min_samples=5)
    n_clusters = len(set(db_labels) - {-1})
    n_noise = db_labels.count(-1)
    print(f"  发现 {n_clusters} 个簇, {n_noise} 个噪声点")

    print("\n=== GMM（3 个簇）===")
    gmm_assignments, gmm_means, gmm_weights, _ = gmm(data, k=3)
    print(f"  均值: {[[round(m, 2) for m in mean] for mean in gmm_means]}")
    print(f"  权重: {[round(w, 3) for w in gmm_weights]}")
    gmm_sil = silhouette_score(data, gmm_assignments)
    print(f"  轮廓系数: {gmm_sil:.4f}")

    print("\n=== DBSCAN 月牙数据（非球形簇）===")
    moon_data, moon_labels = make_moons(n_samples=200, noise=0.1)
    moon_db = dbscan(moon_data, eps=0.3, min_samples=5)
    n_moon_clusters = len(set(moon_db) - {-1})
    n_moon_noise = moon_db.count(-1)
    print(f"  发现 {n_moon_clusters} 个簇, {n_moon_noise} 个噪声点")

    print("\n=== K-Means 月牙数据（无法分离）===")
    moon_km, moon_centroids = kmeans(moon_data, k=2)
    moon_sil = silhouette_score(moon_data, moon_km)
    print(f"  轮廓系数: {moon_sil:.4f}")
    print("  K-Means 不能很好地分割月牙，因为它们不是球形的")

    print("\n=== DBSCAN 异常检测 ===")
    anomaly_data = list(data)
    anomaly_data.append([20.0, 20.0])
    anomaly_data.append([-5.0, -5.0])
    anomaly_data.append([15.0, 0.0])
    anomaly_labels = dbscan(anomaly_data, eps=1.5, min_samples=5)
    anomalies = [
        anomaly_data[i]
        for i in range(len(anomaly_labels))
        if anomaly_labels[i] == -1
    ]
    print(f"  检测到 {len(anomalies)} 个异常点")
    for a in anomalies[-3:]:
        print(f"    点 {[round(v, 2) for v in a]}")
```

## 用框架实现

使用 scikit-learn，这些算法都是一行代码：

```python
from sklearn.cluster import KMeans, DBSCAN, AgglomerativeClustering
from sklearn.mixture import GaussianMixture
from sklearn.metrics import silhouette_score as sklearn_silhouette

km = KMeans(n_clusters=3, random_state=42).fit(data)  # K-Means 聚类
db = DBSCAN(eps=1.5, min_samples=5).fit(data)  # DBSCAN 密度聚类
agg = AgglomerativeClustering(n_clusters=3).fit(data)  # 层次聚类
gmm_model = GaussianMixture(n_components=3, random_state=42).fit(data)  # GMM
```

从零实现的版本准确展示了这些库计算了什么。K-Means 在分配和重计算之间迭代。DBSCAN 从密集种子扩展簇。GMM 在期望和最大化之间交替。库版本增加了数值稳定性、更智能的初始化（K-Means++）和 GPU 加速，但核心逻辑相同。

## 产出物

本课产出了 K-Means、DBSCAN 和 GMM 的可工作从零实现。聚类代码可以作为更高级无监督方法的基础。

## 练习题

1. 实现 K-Means++ 初始化：不是随机选择质心，而是随机选择第一个，然后每个后续质心以与其到最近已有质心的平方距离成正比的概率选择。比较收敛速度与随机初始化的差别。

2. 向代码中添加层次聚合聚类。实现 Ward 链接并生成树状图（作为合并的嵌套列表）。在不同层级切割并与 K-Means 结果比较。

3. 构建简单的异常检测管线：在同一数据上运行 DBSCAN 和 GMM，标记两种方法都认为是异常值的点（DBSCAN 中的噪声、GMM 中的低概率点）。测量重叠并讨论方法何时不一致。

## 术语速查表

| 术语 | 实际含义 |
|------|---------|
| 聚类 (Clustering) | 将数据划分为子集，使组内相似度超过组间相似度 |
| 质心 (Centroid) | 分配给某簇的所有点的均值；K-Means 用作簇代表 |
| 惯性 (Inertia) | 每个点到其分配质心的平方距离之和；越低越紧凑 |
| 轮廓系数 (Silhouette Score) | 对每个点，(b - a) / max(a, b)，其中 a 是簇内平均距离，b 是最近簇平均距离 |
| 核心点 (Core Point) | 在 eps 距离内有至少 min_samples 个邻居的点，在 DBSCAN 中 |
| EM 算法 | 期望最大化：迭代计算成员概率（E 步）和更新分布参数（M 步） |
| 树状图 (Dendrogram) | 显示层次聚类中簇合并顺序和距离的树形图 |
| 异常值 (Anomaly) | 不符合预期模式的数据点，DBSCAN 标记为噪声或 GMM 下概率很低 |

## 延伸阅读

- [Stanford CS229 - 无监督学习](https://cs229.stanford.edu/notes2022fall/main_notes.pdf) - Andrew Ng 的聚类和 EM 讲义
- [scikit-learn 聚类指南](https://scikit-learn.org/stable/modules/clustering.html) - 所有聚类算法的实用比较和可视化示例
- [DBSCAN 原始论文 (Ester et al., 1996)](https://www.aaai.org/Papers/KDD/1996/KDD96-037.pdf) - 引入基于密度聚类的论文
