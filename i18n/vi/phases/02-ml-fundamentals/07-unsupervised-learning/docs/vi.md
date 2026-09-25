# Học hỏi không được giám sát
# 无监督学习


> Không có nhãn, không có giáo viên.

> Không có nhãn, không có giáo viên.

**Type:** Build | **类型：** 构建
**Languages:** Python
**Prerequisites:** Phase 1 (Norms & Distances, Probability & Distributions), Phase 2 Lessons 1-6 | **前置知识：** Phase 1（范数与距离、概率与分布），Phase 2 第 1-6 课
**Time:** ~90 minutes | **时间：** 约 90 分钟

## Mục tiêu học tập

- Thực hiện K-Means, DBSCAN và Gaussian Mix Models từ đầu và so sánh hành vi cluster của chúng
  Từ thực hiện K-Means、DBSCAN 和高斯混合模型 (GMM), so sánh hành vi tập hợp của chúng
- Đánh giá chất lượng cluster bằng cách sử dụng điểm bóng và phương pháp khuỷu tay để chọn K tối ưu
  Sử dụng hệ số vòng và cách đánh giá chất lượng tập hợp, chọn tối ưu K
- Giải thích khi nào DBSCAN vượt qua K-Means và xác định thuật toán nào xử lý các cụm không-thành tráng và các mức ngoại lệ
  解释 DBSCAN 何時優于K-Means,识别哪种算法能处理非球形和异常值
- Xây dựng một đường ống phát hiện bất thường bằng cách sử dụng phương pháp nhóm để đánh dấu các điểm lệch khỏi các mẫu bình thường
  Sử dụng phương pháp tập hợp xây dựng đường ống kiểm tra bất thường, đánh dấu các điểm rời khỏi chế độ bình thường


> **【中文解读】**
> 无监督学习没有标签, mục tiêu là tìm thấy cấu trúc trong dữ liệu. K-Means là thuật toán phân loại cổ điển nhất, DBSCAN có thể tìm thấy bất kỳ hình dạng nào.

> **【拓展：无监督学习在真实 AI 系统中的价值】**
> Google Photos sử dụng thuật toán phân loại tương tự như phân loại hình ảnh ([[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]; chức năng " phát hiện " của Spotify sử dụng tính năng phân loại người dùng sẽ được phân nhóm sau khi đề xuất; kiểm tra bất thường trong lĩnh vực an ninh mạng sử dụng DBSCAN/Isolation Forest  phát hiện lưu lượng bất thường ٬ trong trường hợp không có nhãn hoặc nhãn có chi phí cực cao, không giám sát học là lựa chọn duy nhất٬

## Vấn đề  vấn đề giới thiệu

Mỗi bài học ML cho đến nay đã giả định dữ liệu có nhãn: "đây là một đầu vào, đây là đầu ra chính xác". Trong thế giới thực, nhãn là đắt tiền. Một bệnh viện có hàng triệu hồ sơ bệnh nhân nhưng không ai tự đánh dấu từng bệnh nhân bằng loại bệnh. Một trang web thương mại điện tử có hàng triệu phiên người dùng nhưng không ai có các phân khúc khách hàng được dán nhãn bằng tay. Một nhóm an ninh có nhật ký mạng nhưng không ai ghi dấu bất thường nào.

> Ước tính mỗi lớp trước đều có dữ liệu đánh dấu:"Đây là nhập, đây là chính xác xuất. " Trong thế giới thực, đánh dấu là tốn kém. Ước tính có hàng triệu bệnh nhân trong một bệnh viện, nhưng không ai di động cho mỗi loại đánh dấu bệnh. Ước tính trên một trang web thương mại điện tử có hàng triệu người dùng, nhưng không ai di động đánh dấu các nhóm khách hàng.

Học tập không giám sát tìm thấy các mẫu mà không được cho biết phải tìm gì. Nó tập hợp các điểm dữ liệu tương tự, phát hiện ra cấu trúc ẩn và làm nổi bật các bất thường. Nếu học tập được giám sát là học từ một cuốn sách giáo khoa với khóa trả lời, học tập không giám sát đang nhìn vào dữ liệu thô cho đến khi các mẫu tiết lộ chính mình.

> 无监督学习在没有被告知寻找什么的情况下发现模式――它 sẽ giống như các dữ liệu phân组, phát hiện cấu trúc ẩn, tiết lộ bất thường―― nếu giám sát học là học từ các giáo khoa có câu trả lời,无监督学习就是着原始数据直到模式自我显现――

Điều quan trọng: nếu không có nhãn, bạn không thể đo "trực sự" hoặc "sai". Bạn cần các công cụ khác nhau để đánh giá liệu cấu trúc mà thuật toán của bạn tìm thấy có ý nghĩa hay không.

> 关键问题: không có nhãn, bạn không thể đo trực tiếp " đối " hoặc " lỗi "―― bạn cần các công cụ khác nhau để đánh giá cấu trúc của thuật toán tìm thấy có ý nghĩa không――

> **【中文解读】**
> 无监督学习的核心挑战是评估:没有标签就无法直接衡量"对错"――需要使用轮系数,肘部法则等标标标间接评估聚类质量――K-Means 假设是球形的且大小相近,对异常值敏感;DBSCAN 能发现任意形的并自动识别噪音点,但需要设置密度参数――

## Khái niệm cốt lõi

### Nhóm: Nhóm các thứ tương tự

Cluster phân bổ từng điểm dữ liệu cho một nhóm (cluster) để các điểm trong cùng nhóm giống nhau hơn các điểm trong các nhóm khác.

> 聚类将每个数据点分配到一个组), làm cho các điểm trong cùng nhóm giống hơn các điểm của các nhóm khác.

```mermaid
flowchart LR
    A[Raw Data] --> B{Choose Method}
    B --> C[K-Means]
    B --> D[DBSCAN]
    B --> E[Hierarchical]
    B --> F[GMM]
    C --> G[Flat, spherical clusters]
    D --> H[Arbitrary shapes, noise detection]
    E --> I[Tree of nested clusters]
    F --> J[Soft assignments, elliptical clusters]
```

### K-Means: Con ngựa lao động

K-Means phân chia dữ liệu thành cụm cụm chính xác K. Mỗi cụm có một trung tâm (trung trọng của nó), và mỗi điểm thuộc về trung tâm gần nhất.

> K-Thiết định phân chia dữ liệu thành K 个── mỗi 个 có một质心, mỗi điểm thuộc về chất心 gần đây.

Algoritm của Lloyd:

> Lloyd 算法:

1. Chọn các điểm ngẫu nhiên K như là các trung tâm ban đầu
   随机选择 K 个点作为初始质心
2. Đưa từng điểm dữ liệu đến trung tâm gần nhất
   Đưa từng điểm dữ liệu cho trung tâm gần đây nhất
3. Tái tính mỗi trung tâm như trung bình của các điểm được gán
   重新计算 mỗi chất tâm cho giá trị trung bình của điểm phân phối của nó
4. Lặp lại các bước 2-3 cho đến khi các nhiệm vụ ngừng thay đổi
   重复步骤 2-3 cho đến khi phân bổ không còn thay đổi

Chức năng khách quan (inerti) đo khoảng cách tổng cộng vuông từ mỗi điểm đến trung tâm được chỉ định của nó. K-Means giảm thiểu điều này, nhưng chỉ tìm thấy một mức tối thiểu địa phương.

> 目标函数 (惯性) đo từng điểm đến tổng khoảng cách vuông phân phối của chất lượng của nó. K-Thiết là tối thiểu hóa nó, nhưng chỉ tìm thấy giá trị tối thiểu ở địa phương.

### Chọn K

Hai phương pháp tiêu chuẩn:

> 两种标准方法:

**Elbow method:**Động K-Mức cho K = 1, 2, 3, ..., n. Trầm trễ tương đối với K. Tìm kiếm "cái tay" nơi việc thêm nhiều cụm dừng lại giảm trễ đáng kể.

> **肘部法则：**Đối với K = 1, 2, 3, ..., n 运行 K-Means── vẽ quen thuộc so với K của hình── tìm kiếm "ngón" tăng thêm không còn giảm đáng kể các vị trí quen thuộc──

**Silhouette score:**Đối với mỗi điểm, đo mức độ tương tự của nó với cụm riêng (a) so với cụm khác gần nhất (b). Tỷ lệ hình ảnh là (b - a) / max(a, b), dao động từ -1 (thống cụm sai) đến +1 (thống cụm tốt).

> **轮廓系数：**Đối với mỗi điểm, đo tương tự của nó với bản thân mình (a) So với tương tự gần khác (b)。 Ròng 系数为 (b - a) / max(a, b), dao động từ -1(错误的) đến +1(良好的聚类)。 đối với tất cả các điểm lấy trung bình toàn局分数。

### DBSCAN: Nhóm dựa trên mật độ

K-Means giả định các cụm là hình cầu và yêu cầu bạn chọn K trước. DBSCAN không đưa ra bất kỳ giả định nào.

> K-Thiết 假设是球形的且需要预选 K――DBSCAN 不做这些假设――它将被发现为被稀疏区域分隔的密集区域――

Hai tham số:
- **eps**: bán kính của một khu phố
  **eps**: 半域
- **min_samples**: số điểm tối thiểu cần thiết để tạo ra một khu vực dày đặc
  **min_samples**: Số điểm tối thiểu cần thiết để hình thành khu vực dày đặc

Ba loại điểm:
- **Core point**: có ít nhất các điểm mẫu trong khoảng cách eps
  **核心点**: trong eps  khoảng cách trong ít nhất có ít_con_con_con_
- **Border point**: trong eps của một điểm cốt lõi nhưng không phải chính nó là một điểm cốt lõi
  **边界点**: trong phạm vi của các điểm trung tâm nhưng không phải là điểm trung tâm
- **Noise point**: không có lõi hay biên giới.
  **噪声点**: cả phi trọng tâm cũng không biên giới.

DBSCAN kết nối các điểm cốt lõi nằm trong eps của nhau vào cùng một cụm. Các điểm biên giới tham gia vào cụm của một điểm cốt lõi gần đó.

> DBSCAN sẽ kết nối với nhau trong các điểm trung tâm trong phạm vi eps.

Nguyên nhân: tìm thấy các cụm bất kỳ hình dạng nào, tự động xác định số lượng cụm, xác định các điểm khác biệt.

> 优势: phát hiện hình dạng tùy chọn, tự xác định số lượng, nhận dạng giá trị bất thường.

### Nhóm xếp hạng

Xây dựng một cây (dendrogram) của các cụm tổ.

> 构建嵌套的树树状图)

Tóm lại (từ dưới lên):

> 聚合式(自底上):

1. Bắt đầu với mỗi điểm như một cụm riêng của nó
   Bắt đầu mỗi điểm là của riêng mình
2. Thêm hai nhóm gần nhất
   合并两个最近的
3. Lặp lại cho đến khi chỉ còn một cluster
   重复 Cho đến khi còn lại một người
4. Cắt dendrogram ở mức mong muốn để có được các cụm K
   Trong cấp độ cần thiết cắt hình cây hình được K 个

"Tương gần" giữa các cụm có thể được đo bằng cách:
- **Single linkage**: khoảng cách tối thiểu giữa hai điểm trong hai cluster
  **单链接**: 2 trong 2 điểm bất kỳ khoảng cách tối thiểu
- **Complete linkage**: khoảng cách tối đa giữa hai điểm
  **全链接**: khoảng cách tối đa giữa hai điểm tùy chọn
- **Average linkage**: khoảng cách trung bình giữa tất cả các cặp
  **平均链接**: tất cả các điểm đối với khoảng cách trung bình
- **Ward's method**: sự sáp nhập gây ra sự gia tăng nhỏ nhất trong tổng sự khác biệt trong cluster
  **Ward 方法**: dẫn đến sự gia tăng tổng quãng trong

### Mô hình hỗn hợp Gaussian (GMM)

K-Means cho các bài tập khó khăn: mỗi điểm thuộc về chính xác một cluster. GMM cho các bài tập mềm: mỗi điểm có khả năng thuộc về mỗi cluster.

> K-Công nghĩa đưa ra phân phối cứng: mỗi điểm đúng là thuộc về một ──GMM đưa ra phân phối mềm: mỗi điểm có tỷ lệ thuộc về mỗi ──

GMM giả định dữ liệu được tạo ra từ một hỗn hợp phân bố K Gaussian, mỗi phân bố có trung bình và tính biến khác nhau của riêng mình.

> GMM giả định dữ liệu được tạo ra bởi sự hỗn hợp phân bố K, mỗi có giá trị trung bình và sự khác biệt của riêng mình.

- **E-step**: tính toán xác suất rằng mỗi điểm thuộc về mỗi Gaussian
  **E 步**: tính toán mỗi điểm thuộc về tỷ lệ phân bố cao của mỗi điểm
- **M-step**: cập nhật trung bình, tính biến và trọng lượng trộn của mỗi Gaussian để tối đa hóa khả năng của dữ liệu
  **M 步**: cập nhật giá trị trung bình, tỷ lệ khác biệt và trọng lượng hỗn hợp của mỗi phân bố cao để tối đa hóa dữ liệu giống nhau

GMM có thể mô hình các cụm hình hình elip (không chỉ hình cầu như K-Means) và tự nhiên xử lý các cụm chồng chéo.

> GMM 能建模圆(不只是 K-Means 的球形), tự nhiên xử lý重叠──

### Khi nào sử dụng

| Method | Best for | Avoid when |
|--------|----------|------------|
| K-Means | Large datasets, spherical clusters, known K | Irregular shapes, outliers present |
| DBSCAN | Unknown K, arbitrary shapes, outlier detection | Varying densities, very high dimensions |
| Hierarchical | Small datasets, need dendrogram, unknown K | Large datasets (O(n^2) memory) |
| GMM | Overlapping clusters, soft assignments needed | Very large datasets, too many dimensions |

| 方法 | 最适合 | 避免使用 |
|------|--------|---------|
| K-Means | 大数据集，球形簇，已知 K | 不规则形状，有异常值 |
| DBSCAN | 未知 K，任意形状，异常检测 | 密度不均匀，极高维度 |
| 层次聚类 | 小数据集，需要树状图，未知 K | 大数据集（O(n^2) 内存） |
| GMM | 重叠簇，需要软分配 | 非常大的数据集，维度太高 |

### Khám phá bất thường bằng cách tập hợp

Các nhóm tự nhiên hỗ trợ phát hiện bất thường:
- **K-Means**: các điểm xa từ bất kỳ trung tâm nào là bất thường
  **K-Means**Từ bất cứ chất lượng nào là rất xa.
- **DBSCAN**: các điểm tiếng ồn là bất thường theo định nghĩa
  **DBSCAN**: noise point theo định nghĩa là bất thường
- **GMM**: các điểm có khả năng thấp dưới tất cả các Gaussans là bất thường
  **GMM**Trong tất cả các phân bố cao , tỷ lệ rất thấp là điểm bất thường

> 聚类天然支持异常检测:

## Hãy xây dựng nó.

> **【中文解读】**
> Từ zero thực hiện K-Means、DBSCAN 和高斯混合模型──K-Means 的三步代:随机初始化中心 → 分配每个点到最近中心 → 重新计算中心──重复直到收──DBSCAN Từ khu vực mật độ cao bắt đầu mở rộng, tự động xử lý điểm tiếng ồn──
```figure
kmeans-step
```

## Hãy xây dựng nó

### Bước 1: K-Công nghĩa từ đầu

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
            print(f"  Converged at iteration {iteration + 1}")
            break

        centroids = new_centroids

    return assignments, centroids
```

### Bước 2: Phương pháp cằm và điểm bóng

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
    print("Elbow method:")
    inertias = []
    for k in range(1, max_k + 1):
        assignments, centroids = kmeans(data, k)
        inertia = compute_inertia(data, assignments, centroids)
        inertias.append(inertia)
        print(f"  K={k}: inertia={inertia:.2f}")

    print("\nSilhouette scores:")
    for k in range(2, max_k + 1):
        assignments, centroids = kmeans(data, k)
        score = silhouette_score(data, assignments)
        print(f"  K={k}: silhouette={score:.4f}")

    return inertias
```

### Bước 3: DBSCAN từ đầu

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

### Bước 4: Mô hình hỗn hợp Gaussian (EM algorithm)

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
            print(f"  GMM converged at iteration {iteration + 1}")
            break

    assignments = []
    for i in range(n):
        assignments.append(responsibilities[i].index(max(responsibilities[i])))

    return assignments, means, weights, responsibilities
```

### Bước 5: Tạo dữ liệu thử nghiệm và chạy tất cả

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

    print("=== K-Means on 3 blobs ===")
    assignments, centroids = kmeans(data, k=3)
    print(f"  Centroids: {[[round(c, 2) for c in cent] for cent in centroids]}")
    sil = silhouette_score(data, assignments)
    print(f"  Silhouette score: {sil:.4f}")

    print("\n=== Elbow Method ===")
    find_best_k(data, max_k=6)

    print("\n=== DBSCAN on 3 blobs ===")
    db_labels = dbscan(data, eps=1.5, min_samples=5)
    n_clusters = len(set(db_labels) - {-1})
    n_noise = db_labels.count(-1)
    print(f"  Found {n_clusters} clusters, {n_noise} noise points")

    print("\n=== GMM on 3 blobs ===")
    gmm_assignments, gmm_means, gmm_weights, _ = gmm(data, k=3)
    print(f"  Means: {[[round(m, 2) for m in mean] for mean in gmm_means]}")
    print(f"  Weights: {[round(w, 3) for w in gmm_weights]}")
    gmm_sil = silhouette_score(data, gmm_assignments)
    print(f"  Silhouette score: {gmm_sil:.4f}")

    print("\n=== DBSCAN on moons (non-spherical clusters) ===")
    moon_data, moon_labels = make_moons(n_samples=200, noise=0.1)
    moon_db = dbscan(moon_data, eps=0.3, min_samples=5)
    n_moon_clusters = len(set(moon_db) - {-1})
    n_moon_noise = moon_db.count(-1)
    print(f"  Found {n_moon_clusters} clusters, {n_moon_noise} noise points")

    print("\n=== K-Means on moons (will fail to separate) ===")
    moon_km, moon_centroids = kmeans(moon_data, k=2)
    moon_sil = silhouette_score(moon_data, moon_km)
    print(f"  Silhouette score: {moon_sil:.4f}")
    print("  K-Means splits moons poorly because they are not spherical")

    print("\n=== Anomaly detection with DBSCAN ===")
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
    print(f"  Detected {len(anomalies)} anomalies")
    for a in anomalies[-3:]:
        print(f"    Point {[round(v, 2) for v in a]}")
```

## Hãy sử dụng nó để thực hiện

Với scikit-learn, các thuật toán tương tự là một dòng:

> Sử dụng scikit-learn, cùng một thuật toán chỉ cần một dòng mã:

```python
from sklearn.cluster import KMeans, DBSCAN, AgglomerativeClustering
from sklearn.mixture import GaussianMixture
from sklearn.metrics import silhouette_score as sklearn_silhouette

km = KMeans(n_clusters=3, random_state=42).fit(data)  # K-Means 聚类（默认 K-Means++ 初始化）
db = DBSCAN(eps=1.5, min_samples=5).fit(data)  # DBSCAN 密度聚类（eps 为邻域半径）
agg = AgglomerativeClustering(n_clusters=3).fit(data)  # 层次聚类
gmm_model = GaussianMixture(n_components=3, random_state=42).fit(data)  # 高斯混合模型（EM 算法）
```

Các phiên bản từ đầu cho bạn thấy chính xác những gì các thư viện này tính toán. K-Means lặp lại giữa phân bổ và tính lại. DBSCAN phát triển các cụm từ hạt giống dày đặc. GMM thay thế giữa kỳ vọng và tối đa hóa. Các phiên bản thư viện thêm ổn định số, khởi đầu thông minh hơn (K-Means ++), và tăng tốc GPU, nhưng logic cốt lõi là giống nhau.

> Từ phiên bản 0 đến bạn đã cho thấy các bộ nhớ này đã tính đến cuối cùng. K-Means trong phân phối và tính toán nặng giữa các thế hệ. DBSCAN từ hạt giống dày đặc mở rộng. GMM trong sự thay đổi giữa kỳ vọng và tối đa hóa.

## Chuyển nó đi.

Bài học này tạo ra các triển khai hoạt động của K-Means, DBSCAN và GMM từ đầu. Mã cluster có thể được sử dụng lại như một nền tảng cho các phương pháp không giám sát tiên tiến hơn.

> Các khóa học này được phát triển từ thực hiện từ không K-Means、DBSCAN 和 GMM──聚类代码 có thể được sử dụng như một cơ sở cho phương pháp không giám sát cao hơn──

> **【拓展：聚类在用户分群和推荐系统中的应用】**
> Spotify sẽ phân loại người dùng thành "các nhóm hương vị" để giới thiệu nhạc Người dùng trong mỗi nhóm có thói quen nghe nhạc tương tự. Airbnb sử dụng nhóm tập hợp để tối ưu hóa thứ hạng tìm kiếm. Amazon sử dụng nhóm tập hợp để tìm thấy mô hình mua hàng để giới thiệu hàng hóa. Trong thị trường, RFM mô hình (Recency, Frequency, Monetary) + K-Means phân chia khách hàng thành giá cao, tiềm năng, rủi ro mất giá trị, và các nhóm khác nhau, hướng dẫn chiến lược tiếp thị khác biệt.

> **【中文解读】**
> 无监督学习的评估比监督学习更困难──轮系数衡量内密度 vs 间分离度,范围 [-1, 1],越高越好──肘部法则寻找 WCSS(内平方和)随着K 增加的"拐点"──GMM 使用EM 算法(期望最大化)交换更新分配和参数,比K-Means 更灵活(圆而非球形) nhưng慢 hơn──

## Tập luyện bài tập

1. Thực hiện khởi tạo K-Means ++: thay vì chọn các trung tâm vô tình, chọn trung tâm vô tình đầu tiên và mỗi trung tâm sau đó với xác suất tương xứng với khoảng cách vuông của nó từ trung tâm hiện có gần nhất. So sánh tốc độ hội tụ với khởi tạo vô tình.
   1. 实现 K-Means++ khởi nghiệp: không phải chọn lựa tự nhiên, mà chọn lựa tự nhiên thứ nhất, sau đó mỗi tiếp tục được chọn để so sánh với gần đây đã có chất lượng từ khoảng cách vuông thành tỷ lệ xác suất lựa chọn.
2. Thêm các nhóm tập hợp hàng bậc vào mã. Thực hiện liên kết của Ward và tạo ra một biểu tượng dendrogram (như một danh sách hợp nhất tổ hợp).
   2. Kế hoạch kết nối và tạo hình dạng cây (tương tự như các danh sách nhựa của hợp nhất)
3. Xây dựng một đường ống phát hiện bất thường đơn giản: chạy DBSCAN và GMM trên cùng một dữ liệu, các điểm dấu hiệu mà cả hai phương pháp đều đồng ý là ngoại lệ (ồn ào trong DBSCAN, xác suất thấp trong GMM). đo sự chồng chéo và thảo luận khi các phương pháp không đồng ý.
   3.  cấu trúc đơn giản của các ống kiểm tra bất thường: trên cùng dữ liệu chạy trên DBSCAN và GMM, đánh dấu hai phương pháp đều được coi là điểm bất thường của điểm 

## Từ khóa  Từ khóa nhanh chóng

| Term | What people say | What it actually means |
|------|----------------|----------------------|
| Clustering | "Grouping similar things" | Partitioning data into subsets where within-group similarity exceeds between-group similarity, measured by a specific distance metric |
| Centroid | "The center of a cluster" | The mean of all points assigned to a cluster; used by K-Means as the cluster representative |
| Inertia | "How tight the clusters are" | Sum of squared distances from each point to its assigned centroid; lower is tighter |
| Silhouette score | "How well-separated clusters are" | For each point, (b - a) / max(a, b) where a is mean intra-cluster distance and b is mean nearest-cluster distance |
| Core point | "A point in a dense region" | A point with at least min_samples neighbors within eps distance, in DBSCAN |
| EM algorithm | "Soft K-Means" | Expectation-Maximization: iteratively compute membership probabilities (E-step) and update distribution parameters (M-step) |
| Dendrogram | "A tree of clusters" | A tree diagram showing the order and distance at which clusters were merged in hierarchical clustering |
| Anomaly | "An outlier" | A data point that does not conform to the expected pattern, identified as noise by DBSCAN or low-probability by GMM |

## Xem thêm 延伸阅读

- [Stanford CS229 - Unsupervised Learning](https://cs229.stanford.edu/notes2022fall/main_notes.pdf)- Bài giảng của Andrew Ng về cluster và EM
  [Stanford CS229 - 无监督学习](https://cs229.stanford.edu/notes2022fall/main_notes.pdf)- Andrew Ng của tập hợp và EM 讲义
- [scikit-learn Clustering Guide](https://scikit-learn.org/stable/modules/clustering.html)- so sánh thực tế của tất cả các thuật toán cluster với các ví dụ trực quan
  [scikit-learn 聚类指南](https://scikit-learn.org/stable/modules/clustering.html)- Hiệu ứng so sánh và hình dung các ví dụ về các thuật toán tập hợp
- [DBSCAN original paper (Ester et al., 1996)](https://www.aaai.org/Papers/KDD/1996/KDD96-037.pdf)- giấy giới thiệu việc phân nhóm dựa trên mật độ
  [DBSCAN 原始论文 (Ester et al., 1996)](https://www.aaai.org/Papers/KDD/1996/KDD96-037.pdf)-  giới thiệu các bài báo dựa trên mật độ tập trung
