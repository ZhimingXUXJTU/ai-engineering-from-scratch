# Normalar ve mesafeler.

> Mesafe fonksiyonunuz "aynı" ne anlama geldiğini belirler.
> 距离函数 defines "相似" anlamını seçti, aşağı yukarı her şey çöktü.

**Type:** Build | **类型:** 动手
**Language:**Python .**语言:**Python
**Prerequisites:** Phase 1, Lessons 01 (Linear Algebra Intuition), 02 (Vectors, Matrices & Operations) | **前置知识:** Phase 1, Lessons 01-02
**Time:** ~90 minutes | **时间:** ~90 分钟

## Öğrenme hedefleri

- L1, L2, cosine, Mahalanobis, Jaccard uygulaması ve mesafe fonksiyonlarını sıfırdan düzenle
  L1、L2、余弦、马氏、Jaccard 和编辑距离函数
- Verilmiş bir ML görevi için uygun mesafe ölçüsünü seçin ve alternatiflerin neden başarısız olduğunu açıklayın
  Bu nedenle, diğer seçeneklerin neden başarısız olduğunu açıklayın.
- L1 ve L2 normlarını LASSO ve Ridge düzenlenmesi ve geometrik kısıtlama bölgelerine bağlayın
  L1 ve L2 范数 ile LASSO ve Ridge  正则化 ve onun geometrik kısıtlama bölgesi ile bağlantı kurmak
- Aynı veri kümesinin farklı metrikler altında farklı en yakın komşuları nasıl ürettiğini göster
  演示 Aynı veri kümesi farklı ölçüde farklı yakın komşu oluşturuyor

> **【中文解读】**
> 距離函数 defines similar signification──L1 应 LASSO(特征选择),L2 应 Ridge(overadaptation 防止),余弦距離適合词嵌入,编辑距離適字串──梯度剪剪用 L2 范数限制梯度大小──

## Sorunlar. Sorunlar.

> **【中文解读】**"Bu iki vektör ne kadar benzer?" cevabı tamamen hangi mesafe fonksiyonuna bağlıdır. L2 altında olan veriler aynıdır, öbür string mesafesinden çok uzak olabilir.

## Konsepten bir şey.

> **【拓展：范数在 AI 中的四大应用】**(1) **L2 正则化**- ...`loss + lambda * ||w||_2^2`, ağırlıklı yükün önlenmesi, ağırlıklı yükün azaltılması;**梯度裁剪**- ...`||grad|| > max_norm`时缩放梯度,Transformer 训练的标配;(3) **余弦相似度**:RAG 检索和推系统的标准度,只看方向不看大小;(4) **LayerNorm**L2 归结,稳定训练过程――理解范数就是理解正则化和归结的数学基础――

En iyi evrensel mesafe yoktur. L2 uzay verileri için çalışır. Kosin benzerliği NLP'ye hakimdir. Jaccard setleri ele alıyor. Edit distance strings'i ele alıyor. Mahalanobis ilişkileri hesaplıyor. Wasserstein olasılık kütlesini hareket ettirir. Her biri " benzer " ne anlama geldiği hakkında farklı bir varsayımı kodlar.
> 没有万能的最佳距离――L2 适合空间数据,余弦相似度主导 NLP,Jaccard 处理集合,编辑距离处理字串,马氏距离考虑相关性,Wasserstein 移动概率质量──每个都编码了关于"相似"意义的不同假设──

Bu ders, her büyük mesafe fonksiyonunu sıfırdan inşa eder, her biri doğru araç olduğunda gösterir ve hangi metrik kullanıldığına bağlı olarak aynı verilerin en yakın komşuları tamamen farklı nasıl ürettiğini gösterir.
> Bu ders, her ana mesafe fonksiyonunu sıfırdan oluşturarak, hangi fonksiyonu ne zaman kullanıldığını gösterir ve aynı verileri farklı ölçüde tamamen farklı yakın komşuların oluşturduğu gösterir.

### Normalar: vektör büyüklüğünü ölçmek.

norm bir vektörün "çeşitliğini" ölçer. İki vektör arasındaki her mesafe fonksiyonu farklarının normı olarak yazılabilir: d(a, b) = a - b)
> 范数, bir yön yönünün "大小" ◊ iki yön yönünün arasındaki mesafe işlevi olarak onların farkı için bir yön olarak yazılabilir.

### L1 Norm (Manhattan uzaklığı)

L1 normı tüm bileşenlerin mutlak değerlerini toplamaktadır.
> L1 范数 tüm bölüklerin mutlak değerine katılır.

```
||x||_1 = |x_1| + |x_2| + ... + |x_n|
```

Manhattan mesafe adı veriliyor çünkü şehir şebekesinde ne kadar uzak yürüydüğünüzü ölçüyor.
> Manhattan uzaklığı, şehir ağının üzerinde hareket eden asların uzaklığını ölçtüğü için köşelerle hareket edemiyor.

L1'i kullanırken: Yüksek boyutlu nadir veriler, dış değerlere dayanıklılık, özellik seçimi sorunları (L1 düzenlenmesi nadirliği teşvik eder).
> L1: Yüksek Rarıklık Verileri, Eşsiz Değerler, Özellik Seçimi Sorunu

L1 düzenlenmesine bağlamak: Kayıp işlevi (Lasso) 'ye eklemek küçük ağırlıkları tam olarak sıfıra doğru itiyor ve otomatik özellik seçimi yapar. L1 cezası elmas şeklinde kısıtlama bölgelerini oluşturur ve köşeler bazı ağırlıkların sıfır olduğu eksellerde yer alır.
> L1 正则化 (Lasso) 联系:在损失函数中加小权重推至零,执行自动特征选择──L1 惩罚创建形束区域,角点在轴上──

### L2 Norm (Euklid mesafesi)

L2 normı düz çizgi mesafesi.
> L2 范数, düz çizgi mesafesidir.

```
||x||_2 = sqrt(x_1^2 + x_2^2 + ... + x_n^2)
```

Bu geometri sınıfında öğrendiğiniz mesafedir.
> Bu, geometri dersinde öğrenilen mesafe.

L2 düzenlenmesi ile bağlantı: Kayıp fonksiyonunuza Unww Des Des Des Des Des Des des des des des des des des des des des des des des des des des des des des des des des des des des des des des des des des des des des des des des des des des des des des des des des des des des des des des des des des des des des des des des des des des des des des des des des des des des des des des des des des des des des des des des des des des des des des des des des des des des des des des des des des des des des des des des des des des des des des des des des des des des des des des des des des des des des des des des des des des des des des des des des des des des des des des des des des des des des des des des des des des des des des des des des des des des des des des des des des des des des des des des des des des des des des des des des des des des des des des des des des des des des des des des des des des des des des des des des des des des des des des des des des des des des des des des des des des des des des des des des des des des des des des des des des des des des des des des des des des des des des des des des des des des des des des des des des des des des des des des des des des des des des des des des des des des des des des des des des des des des des des des des des des des des des des des des des des des des des des des des des des des des des des des des des des des des des des des des des des des des des des des des des des des des des des des des des des des des des des des des des des des des des des des des des des des des des des des des des des des des des des des des des des des des des des des des des des des des des des des des des des des des des des des des des des des des des des des des des des des des des des des des des des des des des des des des des des des des des des des des des des des des des des des des des des des des des des des des des des des des des des des des des des des des des des des des des des des des des des des des des des des des des des des
> L2 正则化 (L2) ile bağlantı: Ridge                                                                                                                                                                                                                                                        

```
MAE (L1 loss):  |y - y_hat|         Linear penalty. Robust to outliers. / 线性惩罚，对异常值鲁棒。
MSE (L2 loss):  (y - y_hat)^2       Quadratic penalty. Sensitive to outliers. / 二次惩罚，对异常值敏感。
```

### Lp Normaları: Genel aile

L1 ve L2 Lp normunun özel durumlarıdır:
> L1 ve L2 Lp 范数'in özellikleri:

```
||x||_p = (|x_1|^p + |x_2|^p + ... + |x_n|^p)^(1/p)

p=1:    Diamond shape / 菱形
p=2:    Circle/sphere / 圆/球
p=inf:  Square/hypercube / 正方形/超立方体
```

### Cosine benzerliği ve cosine mesafe .

Kosinus benzerliği, iki vektör arasındaki açıyı ölçer ve büyüklüklerini görmezden gelir.
> 余弦相似度 iki 矢量 arasındaki açıyı ölçer, 忽略大小──

```
cos_sim(a, b) = (a . b) / (||a||_2 * ||b||_2)
```

-1 (karşı yönler) ile +1 (aynı yön) arasında değişir.
> 范围 from -1(相反方向) to +1( aynı yön)。余弦距离 = 1 - 余弦相似度。

Neden kozin NLP ve gömülmeler üzerinde egemenlik gösterir: metinde, belge uzunluğu benzerliği etkilememeli. kediler hakkında iki kat uzunluğunda bir belge hala "böyle" olmalıdır.
> Neden余弦主导 NLP 和嵌入:文本中文档长度不应影响相似度──一篇关于猫的文档即使两倍长仍应"相似"──余弦相似度忽略大小,只关注方向──

### Mahalanobis Uzaklığı.

Euclidean mesafe tüm boyutları eşit şekilde değerlendirir. Mahalanobis mesafe verilerin kovarianlık yapısını hesaplar.
> 欧氏距離对所有维度一视同仁――马氏距離考虑数据的协同差结构――

```
d_M(x, y) = sqrt((x - y)^T * S^(-1) * (x - y))
```

İntüütüel olarak: Mahalanobis mesafi önce verileri dekorele eder ve normalleştirir (beyazlama), sonra bu dönüştürülen alanın L2 mesafesini hesaplar.
> Doğrudan: Mars uzaklığı önce ilişkilendirilmiş ve birleştirilmiş verilerde (bkz.

### Jackard benzerliği (seti için)

Jaccard benzerlik ölçüleri iki set arasında örtüşmektedir.
> Jaccard, iki topluluğun üst üstelik oluşumunu ölçmektedir.

```
J(A, B) = |A intersect B| / |A union B|
```

Jaccard'ı ne zaman kullanmak: etiket kümelerini karşılaştırmak, belge benzerliği, neredeyse çiftleme tespit etmek, segmentasyon modelleri değerlendirmek (IoU = Jaccard).
> 何時使用 Jaccard:比较标签集、文档相似度、近似重复检测、评估分割模型(IoU = Jaccard) ・・・

### Edit Distance (Levenshtein Distance) 編集距離(Levenshtein 距離)

Düzenleme mesafesinin bir dizeyi diğerine dönüştürmek için gerekli olan en az tek karakterli işlem sayısını sayması.
> 编辑距离计算将一个字符串转换为另一个所需的最小单字符操作数――动态规划计算――

```
"kitten" -> "sitting"
kitten -> sitten  (substitute k -> s)
sitten -> sittin  (substitute e -> i)
sittin -> sitting (insert g)

Edit distance = 3
```

### KL Divergence ( mesafe değil ama bir gibi kullanılır)

KL farklılığı, bir olasılık dağılımının diğerinden nasıl farklı olduğunu ölçer. Kritik özellik: simetrik değildir. D_KL(P
> KL 散度 bir olasılık dağılımını diğerinden farklılık ölçer.

KL farklılıklarını gördüğünüzde: VAE, bilgi destilasyonu, RLHF, politika gradiyenti yöntemleri.
> Aşağıdaki sahnelerde KL 散度:VAE、知识蒸、RLHF、策略梯度方法──

### Wasserstein Uzaklığı (Earth Mover's Distance)

Wasserstein mesafesinin bir olasılık dağılımını diğerine dönüştürmek için gerekli olan en az "iş" ölçüsüdür. Bu gerçek bir metriktir (simetrik, üçgen eşitsizliğini tatmin eder).
> Wasserstein  mesafe ölçüsü bir olasılık dağılımını diğerine dönüştürür en az "功"── bu gerçek ölçümdür.

### Neden farklı görevlerin farklı mesafeler olması gerekiyor?

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

### Düzenlenme ile düzenlenme ile bağlantı.

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

L1 neden kısıtlama üretir ama L2 neden üretmez: 2 boyutlu bir ağırlık alanında kısıtlama bölgesini görüntüleyin. L1 bir elmas, L2 bir daire. Kayıp fonksiyonunun konturları bir köşede elması en çok dokunabilir, burada bir ağırlık sıfırdır.
> L1  rarequidity neden oluşur ve L2                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                  

### En yakın komşu arama son komşu arama

Yaklaşık En Yakın Komşu (ANN) algoritmaları büyük hız kazanımları için küçük miktarda doğruluk ticareti:
> Yakın komşu (ANN) algoritması, az miktarda hassaslık ile büyük hızlandırma değiştirir:

```
Algorithm         Approach                      Used by
HNSW              Hierarchical navigable         FAISS, Qdrant, Weaviate
                  small-world graph
IVF               Inverted file index with       FAISS (billion-scale)
                  cluster-based search
Product quant.    Compress vectors, search       FAISS (memory-constrained)
                  in compressed space
```

HNSW, modern vektör veritabanlarında baskın algoritmadır.
> HNSW, modern döngü veritabanındaki ana algoritmadır.

## Yapın.
```figure
norm-unit-balls
```

## Yapın

### Adım 1: Tüm norm ve mesafe fonksiyonları .

Bakın .`code/distances.py`Her fonksiyon, sadece temel Python matematikini kullanarak sıfırdan inşa edilmiştir.
> 完整实现见 `code/distances.py`- Evet.

### Adım 2: Aynı veriler, farklı mesafeler, farklı komşular.

Demo ' nun varlığı .`distances.py`bir veri kümesi oluşturur, bir sorgu noktasını seçer ve uzaklık ölçüsüne bağlı olarak en yakın komşu nasıl değiştiğini gösterir.
> 演示 oluşturma veri kümesi, sorgu noktalarını seçmek, yakın komşuların mesafe ölçüsüne göre nasıl değiştiklerini göstermek

### Adım 3: Benzerlik arayışını yerleştirmek.

Kod, bir soruya en çok benzer "belgeler" bulmaya yönelik bir benzerlik arayışı içeren bir simgeyi içerir.
> 代码包含模拟嵌入式相似度搜索,余弦相似度和L2 距离寻找最相似的"文档"──

## Çerçeveyi kullanın.

En yaygın pratik kullanım: vektör veritabanında benzer öğeleri bulmak.
> En yaygın pratik kullanım:  Vektör veritabanında benzer bir yer aramak.

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

Aradığın zaman .`model.encode(text)`Ve sonra vektör veritabanını aramak, kapusun altında olan budur.
> - Ne ? - Ne ?`model.encode(text)`Sonra, kütle veritabanını aramakta, bu altta olan şey.

## Egzersizler.

1. L1, L2 ve L- sonsuzluk mesafelerini (1, 2, 3) ve (4, 0, 6) arasında hesaplayın. L-inf <= L2 <= L1 her zaman geçerli olup olmadığını kontrol edin. Bu sıralanmanın neden garanti edildiğini kanıtlayın.
   計算 (1, 2, 3) 和 (4, 0, 6)   arasındaki L1、L2 和 L-inf 距离──验证 L-inf <= L2 <= L1 始终成立──

2. Kosinus benzerliği (> 0,9) yüksek olduğu, ancak L2 mesafesi büyük (> 10) olduğu iki vektör oluşturun.
   创建两个余弦相似度高(> 0.9)

3. L1, L2, cosinus ve Mahalanobis mesafesinin altında en yakın komşunu geri alan bir fonksiyonu uygulayın.
   实现 işlevi L1、L2、余弦和马氏 mesafesinden aşağı geri dönerek yakın komşusuna ulaştırmak için dört farklı ölçüm tümüyle uyumsuz bir veri kümesi bulunmaktadır.

4. CDF yöntemi kullanarak [0,5, 0,5, 0, 0] ve [0, 0, 0, 0,5, 0,5] arasındaki Wasserstein mesafesini hesaplayın.
   CDF 方法计算 [0.5, 0.5, 0, 0] 和 [0, 0, 0.5, 0.5] 的 Wasserstein 距离──

5. Yaklaşık bir Jaccard benzerliği için MinHash uygulayın.
   实现 MinHash 近似 Jaccard 相似度──与精确 Jaccard 比较──

## Anahtar Şartlar .

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

## Daha fazla okumak

- [FAISS: A Library for Efficient Similarity Search](https://github.com/facebookresearch/faiss)- Meta'nın milyarlık ANN arama kütüphanesi
  Meta'nın milyarlarca sınıfı ANN  arama kitlesi
- [Wasserstein GAN (Arjovsky et al., 2017)](https://arxiv.org/abs/1701.07875)- Dünya Hareketçisinin GAN'larda mesafesi
  Wasserstein     GAN     GAN                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                              
- [Efficient Estimation of Word Representations (Mikolov et al., 2013)](https://arxiv.org/abs/1301.3781)- Word2Vec, burada cosine varsayılan oldu
  Word2Vec,余弦相似度 became默认选择
- [sklearn.neighbors documentation](https://scikit-learn.org/stable/modules/neighbors.html)- mesafe ölçümleri için pratik rehber
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                               
