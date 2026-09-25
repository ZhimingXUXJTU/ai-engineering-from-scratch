# Biện pháp và khoảng cách.

> Chọn sai và mọi thứ sẽ bị phá vỡ.
> 距离函数 định nghĩa ý nghĩa của "相似" 选错了, 下游一切都崩

**Type:** Build | **类型:** 动手
**Language:**Python**语言:**Python
**Prerequisites:** Phase 1, Lessons 01 (Linear Algebra Intuition), 02 (Vectors, Matrices & Operations) | **前置知识:** Phase 1, Lessons 01-02
**Time:** ~90 minutes | **时间:** ~90 分钟

## Mục tiêu học tập

- Thực hiện L1, L2, cosine, Mahalanobis, Jaccard, và chỉnh sửa các hàm khoảng cách từ đầu
  Từ zero thực hiện L1、L2、余弦、马氏、Jaccard 和编辑 khoảng cách hàm
- Chọn số liệu khoảng cách thích hợp cho một nhiệm vụ ML nhất định và giải thích lý do tại sao các thay thế thất bại
  Để xác định ML  nhiệm vụ chọn phù hợp với khoảng cách đo và giải thích tại sao các lựa chọn khác sẽ thất bại
- Kết nối các tiêu chuẩn L1 và L2 với LASSO và Ridge và các khu vực hạn chế hình học của chúng
  L1 và L2 范数 liên kết với LASSO và Ridge 正规化及其几何约束区域
- Hiển thị cách cùng một tập dữ liệu tạo ra các hàng xóm gần nhất khác nhau dưới các số liệu khác nhau
  演示 cùng một tập dữ liệu tạo ra các tương ứng gần nhau ở các mức độ khác nhau

> **【中文解读】**
> 距离函数定义了相似的含义──L1 đối với LASSO(特征选择),L2 đối với应 Ridge(防止过拟合),余弦距离适合词嵌入,编辑距离适合字符串──梯度剪剪 L2 范数限制梯度大小──

## Vấn đề  vấn đề giới thiệu

> **【中文解读】**"Hai khối lượng này có gì tương tự?" Câu trả lời hoàn toàn phụ thuộc vào hàm khoảng cách bạn chọn. Một đối tượng dữ liệu ở L2 dưới là hàng xóm gần nhất, ở khoảng cách dây còn lại có thể rất xa.

## Khái niệm cốt lõi

> **【拓展：范数在 AI 中的四大应用】**(1) **L2 正则化**- Có thể là:`loss + lambda * ||w||_2^2`, ngăn chặn quyền trọng quá lớn,缓解过拟合;**梯度裁剪**- Có thể là:`||grad|| > max_norm`时缩放梯度,Tranformator 训练的标配;(3) **余弦相似度**:RAG 检索和推系统的标准度量, chỉ看方向不看大小;(4) **LayerNorm**Đối với mỗi tầng đầu ra làm L2 归结,稳定训练过程―― hiểu范数 là hiểu cơ sở toán học của chính quy hóa và归结――

Không có khoảng cách tốt nhất phổ quát. L2 hoạt động cho dữ liệu không gian. Sự tương đồng cosine thống trị NLP. Jaccard xử lý tập hợp. Edit distance handles strings. Mahalanobis tính toán cho mối tương quan. Wasserstein di chuyển khối lượng xác suất. Mỗi một mã hóa một giả định khác về điều "tương tự" có nghĩa là gì.
> Không có bất kỳ khả năng nào. L2  thích hợp với dữ liệu không gian, 余弦相似度主导 NLP, Jackard  xử lý tập hợp, biên tập khoảng cách xử lý chuỗi,马氏 khoảng cách xem xét liên quan, Wasserstein 移动概率质量── mỗi người đã lập trình về các giả định khác nhau về ý nghĩa "tương tự".

Bài học này xây dựng mọi hàm khoảng cách lớn từ đầu, cho bạn thấy mỗi công cụ là công cụ phù hợp, và chứng minh cách cùng một dữ liệu tạo ra những người hàng xóm gần nhất hoàn toàn khác nhau tùy thuộc vào số liệu bạn sử dụng.
> Chương trình này bắt đầu từ zero xây dựng từng hàm khoảng cách chính, hiển thị khi nào sử dụng, và thể hiện cùng một dữ liệu tạo ra hoàn toàn khác nhau gần nhau dưới các thước khác nhau.

### Các tiêu chuẩn: đo lường khối lượng vector.

Norm đo "sai" của một vector. Mỗi hàm khoảng cách giữa hai vector có thể được viết như chuẩn của sự khác biệt của chúng: d(a, b) = a - b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b
> 范数 đo "大小" của khối lượng các khối lượng. Phương thức khoảng cách giữa hai khối lượng có thể được viết thành số lượng khác nhau của chúng.

### L1 Norm (Mát-hát-tan)  L1 范数(Mát-hát-tan)

Tỷ lệ L1 tổng hợp các giá trị tuyệt đối của tất cả các thành phần.
> L1 范数 sẽ là một phần tuyệt đối của tất cả các phân số.

```
||x||_1 = |x_1| + |x_2| + ... + |x_n|
```

Nó được gọi là khoảng cách Manhattan vì nó đo được bạn đi bao xa trên lưới thành phố mà bạn chỉ có thể di chuyển dọc theo trục. Không có đường chéo.
> gọi là Manhattan Distance vì nó đo khoảng cách di chuyển dọc theo trục trên mạng lưới thành phố, không thể đi ngược góc.

Khi sử dụng L1: dữ liệu hiếm có chiều cao, độ bền đến mức ngoại lệ, các vấn đề lựa chọn tính năng (làm điều chỉnh L1 thúc đẩy sự hiếm có).
> L1: Lợi lượng dữ liệu hiếm, tính chất chọn lọc đối với các giá trị bất thường.

Kết nối với L1 regularisation: thêm vào hàm mất của bạn (Lasso) đẩy trọng lượng nhỏ đến chính xác bằng không, thực hiện lựa chọn tính năng tự động.
> Liên hệ với L1 正则化 (Lasso): trong hàm mất: trong số số số, sẽ thêm phần nhỏ của quyền trục trặc vào 0 , thực hiện tự động đặc điểm chọn;;

### L2 Norm (trái cách Euclidean)  L2 范数(欧氏距离)

L2 là đường thẳng đường dài.
> L2 范数 là đường thẳng cách ⋅分量平方和的平方根⋅

```
||x||_2 = sqrt(x_1^2 + x_2^2 + ... + x_n^2)
```

Đây là khoảng cách bạn học trong lớp hình học. Pythagoras trong n chiều.
> Đó là cách học trên các lớp học về địa chất.

Kết nối với L2 regularisation: thêm Unww Desire_2 vào hàm mất của bạn sẽ phạt các trọng lượng lớn. giống như L1, nó không đẩy trọng lượng xuống không.
> Liên hệ với L2 正则化 (L2): Trong hàm mất tích: 在Ridge                                                                                                                                                                                                                                                     

```
MAE (L1 loss):  |y - y_hat|         Linear penalty. Robust to outliers. / 线性惩罚，对异常值鲁棒。
MSE (L2 loss):  (y - y_hat)^2       Quadratic penalty. Sensitive to outliers. / 二次惩罚，对异常值敏感。
```

### Lp chuẩn: gia đình chung

L1 và L2 là các trường hợp đặc biệt của chuẩn Lp:
> L1 và L2 là các đặc điểm của Lp 范数:

```
||x||_p = (|x_1|^p + |x_2|^p + ... + |x_n|^p)^(1/p)

p=1:    Diamond shape / 菱形
p=2:    Circle/sphere / 圆/球
p=inf:  Square/hypercube / 正方形/超立方体
```

### Sự tương đồng của cosine và khoảng cách cosine.

Sự tương đồng cosine đo góc giữa hai vector, bỏ qua quy mô của chúng.
> 余弦相似度 đo góc giữa hai khối lượng,忽略大小──

```
cos_sim(a, b) = (a . b) / (||a||_2 * ||b||_2)
```

Nó dao động từ -1 (nghĩa ngược) đến +1 (nghĩa tương tự).
> 范围 từ -1 (相反方向) đến +1 (相同方向) ⋅余弦距离 = 1 - 余弦相似度⋅

Tại sao cosine thống trị NLP và nhúng: trong văn bản, chiều dài tài liệu không nên ảnh hưởng đến sự tương đồng. Một tài liệu về mèo dài gấp đôi vẫn nên "tương tự".
> Tại sao các chuỗi chủ đạo NLP và nhúng: Trong văn bản, độ dài của văn bản không nên ảnh hưởng đến sự tương đồng.

### Khơi Mahalanobis Khơi Ma.

Khoảng cách Euclidean đối xử với tất cả các chiều kích bằng nhau. Khoảng cách Mahalanobis giải thích cấu trúc sự khác nhau của dữ liệu.
> 欧氏距离对所有维度一视同仁――马氏距离考虑数据的协同差结构――

```
d_M(x, y) = sqrt((x - y)^T * S^(-1) * (x - y))
```

Nhận thức: Khoảng cách Mahalanobis trước tiên giải thích và bình thường hóa dữ liệu (tẩy trắng), sau đó tính khoảng cách L2 trong không gian biến đổi đó.
> 直觉上: Má氏距离先去相关并归归化数据 (), sau đó tính L2 距离在变换后的空间中──

### Jaccard tương tự (đối với các bộ)

Các biện pháp tương đồng Jaccard chồng chéo giữa hai bộ.
> Jaccard tương tự đo lường sự chồng lên của hai tập hợp.

```
J(A, B) = |A intersect B| / |A union B|
```

Khi nào sử dụng Jaccard: so sánh các tập hợp thẻ, sự tương đồng tài liệu, phát hiện gần trùng lặp, đánh giá các mô hình phân đoạn (IoU = Jaccard).
> 何時使用 Jaccard:比较标签集、文档相似度、近似重复检测、评估分割模型 ((IoU = Jaccard) 』

### Edit Distance (Levenshtein Distance) 编辑距离(Levenshtein 距离)

Edit distance đếm số lượng tối thiểu các hoạt động đơn ký tự cần thiết để chuyển đổi một chuỗi thành một chuỗi khác.
> 编辑 khoảng cách tính toán sẽ chuyển đổi một字符串 thành một số hoạt động đơn giản nhất cần thiết khác.

```
"kitten" -> "sitting"
kitten -> sitten  (substitute k -> s)
sitten -> sittin  (substitute e -> i)
sittin -> sitting (insert g)

Edit distance = 3
```

### KL Divergence (không phải khoảng cách, nhưng được sử dụng như một)

KL phân biệt đo lường cách phân phối xác suất khác nhau. thuộc tính quan trọng: KHÔNG đối xứng. D_KL(P Ưu Q) != D_KL(Q Ưu P). Đó là một phân biệt, không phải là khoảng cách.
> KL 散度 đo một sự phân bố xác suất với sự khác biệt của một khác.

Khi bạn thấy sự khác biệt KL: VAEs, chưng cất kiến thức, RLHF, phương pháp gradient chính sách.
> Trong các trường hợp sau đây xem KL 散度:VAE、知识蒸、RLHF、策略梯度方法──

### Wasserstein Distance (Tạm dịch: khoảng cách của người di chuyển Trái đất)

Khoảng cách Wasserstein đo "phát" tối thiểu cần thiết để biến đổi phân bố xác suất thành một phân bố khác. Nó là một phép đo thực sự (tương đối, đáp ứng bất bình đẳng tam giác). Nó cung cấp gradient ngay cả khi phân bố không chồng chéo (khiến độ KL đi đến vô hạn).
> Wasserstein  khoảng cách đo sẽ chuyển đổi một phân bố xác suất thành một "功" khác cần thiết tối thiểu. Nó là một thước đo thực sự.

### Tại sao các nhiệm vụ khác nhau cần khoảng cách khác nhau

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

### Liên kết với quy định và sự hợp lý hóa

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

Tại sao L1 tạo ra sự thô lỗ nhưng L2 không tạo ra: hình dung khu vực hạn chế trong không gian trọng lượng 2D. L1 là kim cương, L2 là một vòng tròn. Các đường viền của hàm mất có nhiều khả năng chạm vào kim cương ở góc, nơi một trọng lượng là không. Chúng chạm vào vòng tròn ở một điểm mịn, nơi cả hai trọng lượng không bằng không.
> Tại sao L1  tạo ra sự hiếm khi L2 không: tưởng tượng 2D  vùng ràng buộc trong không gian trọng lượng. L1 là hình xám, L2 là hình tròn.

### Tìm kiếm hàng xóm gần nhất Tìm kiếm gần nhất

Các thuật toán hàng xóm gần nhất (ANN) giao dịch một lượng nhỏ độ chính xác để tăng tốc độ lớn:
> 近似近邻 (ANN) 算法 sử dụng ít lượng chính xác để thay đổi tăng tốc đáng kể:

```
Algorithm         Approach                      Used by
HNSW              Hierarchical navigable         FAISS, Qdrant, Weaviate
                  small-world graph
IVF               Inverted file index with       FAISS (billion-scale)
                  cluster-based search
Product quant.    Compress vectors, search       FAISS (memory-constrained)
                  in compressed space
```

HNSW là thuật toán thống trị trong cơ sở dữ liệu vector hiện đại.
> HNSW là hệ thống chính trong bộ dữ liệu mô hình hiện đại.

## Hãy xây dựng nó.
```figure
norm-unit-balls
```

## Hãy xây dựng nó

### Bước 1: Tất cả các chức năng chuẩn và khoảng cách .

Nhìn xem`code/distances.py`Mỗi hàm được xây dựng từ đầu chỉ bằng toán học Python cơ bản.
> 完整实现见 `code/distances.py`

### Bước 2: cùng dữ liệu, khoảng cách khác nhau, hàng xóm khác nhau.

Demo trong `distances.py`tạo ra một bộ dữ liệu, chọn một điểm truy vấn, và cho thấy hàng xóm gần nhất thay đổi như thế nào tùy thuộc vào métrics khoảng cách.
> 演示 tạo tập dữ liệu, chọn điểm truy vấn, hiển thị cách gần gũi thay đổi theo độ đo:

### Bước 3: Nhập tìm kiếm tương đồng bước 3: Nhập tìm kiếm tương đồng

Mã bao gồm một tìm kiếm tương đồng giả mạo nhúng tìm kiếm "các tài liệu" tương tự nhất với một truy vấn sử dụng tương đồng cosine so với khoảng cách L2.
> 代码包含模拟嵌入相似度搜索, sử dụng余弦相似度和L2 距离寻找最相似的"文档"──

## Hãy sử dụng nó để thực hiện

Sử dụng thực tế phổ biến nhất: tìm các mục tương tự trong cơ sở dữ liệu vector.
>  dụng thực tế phổ biến nhất: tìm kiếm các mục tương tự trong bộ dữ liệu khối lượng

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

Khi anh gọi`model.encode(text)`và sau đó tìm kiếm một cơ sở dữ liệu vector, đây là những gì xảy ra dưới nắp.
> Khi bạn调用`model.encode(text)`Sau đó, khi tìm kiếm dữ liệu khối lượng, đó là những gì xảy ra ở tầng dưới.

## Tập luyện bài tập

1. Xét khoảng cách L1, L2 và L-lực lượng vô hạn giữa (1, 2, 3) và (4, 0, 6). Kiểm tra rằng L-inf <= L2 <= L1 luôn giữ.
   计算 (1, 2, 3) 和 (4, 0, 6) 之间的 L1、L2 和 L-inf 距离――验证 L-inf <= L2 <= L1始终成立──

2. Tạo hai vector nơi sự tương đồng cosine cao (> 0,9) nhưng khoảng cách L2 lớn (> 10). Giải thích theo hình học.
   创建两个余弦相似度高(> 0.9) nhưng L2 距离大(> 10) của向量──几何解释──

3. Thực hiện một hàm trả lại hàng xóm gần nhất dưới khoảng cách L1, L2, cosine và Mahalanobis. Tìm một tập dữ liệu mà cả bốn không đồng ý.
   实现 hàm ở L1、L2、余弦和马氏 khoảng cách xuống trở lại gần nhất. Tìm bốn loại dữ liệu không phù hợp về các thước đo.

4. Xét khoảng cách Wasserstein giữa [0,5, 0,5, 0,0] và [0, 0, 0, 0,5, 0,5] bằng cách sử dụng phương pháp CDF.
   用 CDF 方法计算 [0,5, 0,5, 0, 0] 和 [0, 0, 0,5, 0.5] của Wasserstein 距离──

5. Thực hiện MinHash để tương tự với Jaccard.
   实现 MinHash 近似 Jaccard 相似度──与精确 Jaccard 比较──

## Từ khóa  Từ khóa nhanh chóng

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

## Xem thêm 延伸阅读

- [FAISS: A Library for Efficient Similarity Search](https://github.com/facebookresearch/faiss)- Thư viện Meta cho tìm kiếm ANN tỷ tỷ
  Meta của tỷ cấp ANN 搜索库
- [Wasserstein GAN (Arjovsky et al., 2017)](https://arxiv.org/abs/1701.07875)- Khoảng cách của Earth Mover trong GAN
  Wasserstein  khoảng cách trong GAN
- [Efficient Estimation of Word Representations (Mikolov et al., 2013)](https://arxiv.org/abs/1301.3781)- Word2Vec, nơi cosine trở thành mặc định
  Word2Vec,余弦相似度 trở thành默认选择
- [sklearn.neighbors documentation](https://scikit-learn.org/stable/modules/neighbors.html)- hướng dẫn thực tế về các métrics khoảng cách
   thực tế chỉ dẫn về khoảng cách
