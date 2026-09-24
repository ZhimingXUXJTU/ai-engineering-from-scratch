# Normes et distances.

> Votre fonction de distance définit ce que signifie "semblable".
> La distance définit la signification de "sembler".

**Type:** Build | **类型:** 动手
**Language:**Je suis un Python .**语言:**Python
**Prerequisites:** Phase 1, Lessons 01 (Linear Algebra Intuition), 02 (Vectors, Matrices & Operations) | **前置知识:** Phase 1, Lessons 01-02
**Time:** ~90 minutes | **时间:** ~90 分钟

## Objectifs d'apprentissage

- Implémenter L1, L2, cosine, Mahalanobis, Jaccard, et modifier les fonctions de distance à partir de zéro
  De zéro réalisation L1、L2、余弦、马氏、Jaccard 和 éditer la fonction de distance
- Sélectionnez la mesure de distance appropriée pour une tâche de gestion de la distance donnée et expliquez pourquoi les alternatives échouent
  Pour déterminer la tâche ML choisir la distance appropriée et expliquer pourquoi d'autres choix échoueront
- Connecter les normes L1 et L2 à la régularisation LASSO et Ridge et à leurs régions de contraintes géométriques
  L1 et L2 范数  LASSO 和 Ridge  正则化及其几何束区 联系
- Démontre comment le même ensemble de données produit différents voisins proches sous différentes mesures
  演示 Le même ensemble de données génère des données proches différentes à différentes dimensions

> **【中文解读】**
> La fonction de distance définit une signification similaire. L1 à la résolution LASSO, L2 à la résolution Ridge, L2 à la résolution Ridge, L2 à la résolution Ridge, L2 à la résolution Ridge, L2 à la résolution Ridge, L2 à la résolution Ridge, L2 à la résolution Ridge, L2 à la résolution Ridge, L2 à la résolution Ridge, L2 à la résolution Ridge, L2 à la résolution Ridge, L2 à la résolution Ridge, L2 à la résolution Ridge, L2 à la résolution Ridge, L2 à la résolution Ridge, L2 à la résolution Ridge, L2 à la résolution Ridge, L2 à la résolution Ridge, L2 à la résolution Ridge, L2 à la résolution Ridge, L2 à la résolution Ridge, L2 à la résolution Ridge, L2 à la résolution Ridge, L2 à la résolution Ridge, L2 à la résolution Ridge, L2 à la résolution Ridge, L2 à la résolution Ridge, L2 à la résolution Ridge, L2 à la résolution Ridge, L2 à la résolution Ridge, L2 à la résolution Ridge, L2 à la résolution Ridge, Ridge, R2.

## Le problème , l' introduction du problème

> **【中文解读】**"Combien ces deux vecteurs sont-ils similaires?" La réponse dépend entièrement de la fonction de distance que vous choisissez. La même paire de données est proche de L2 en dessous de la distance de l'autre, peut être très loin.

## Le concept de base.

> **【拓展：范数在 AI 中的四大应用】**(1) **L2 正则化**- Le numéro de la liste:`loss + lambda * ||w||_2^2`, prévenir le poids excessif, atténuer le poids excessif;**梯度裁剪**- Le numéro de la liste:`||grad|| > max_norm`时缩放梯度,Transformer 训练的标配;(3) **余弦相似度**:RAG 检索和推系统的标准度, seulement看方向不看大小;(4) **LayerNorm**Pour chaque niveau de sortie, faire L2 归结, processus de formation stable.

Il n'y a pas de meilleure distance universelle. L2 fonctionne pour les données spatiales. La similitude cosine domine la PNL. Jaccard gère des ensembles. Modifier la distance gère les chaînes. Mahalanobis compte pour les corrélations. Wasserstein déplace la masse de probabilité. Chacun d'eux code une hypothèse différente sur ce que signifie "similar".
> 没有万能的最佳距离――L2 适合空间数据,余弦相似度主导 NLP,Jaccard 处理集合,编辑距离处理字符串,马氏距离考虑相关性,Wasserstein 移动概率质量――每个都编码了关于"相似"意义的不同假设──

Cette leçon construit chaque fonction principale de distance à partir de zéro, vous montre quand chacun est l'outil approprié, et montre comment les mêmes données produisent des voisins proches complètement différents selon la métrique que vous utilisez.
> Ce cours commence par la construction de zéro de chaque fonction principale de distance, montre quand utiliser laquelle, et montre la même donnée produite à des niveaux différents.

### Normes: mesure de la magnitude vectorielle 范数: mesure de la taille

La norme mesure la " taille " d'un vecteur. Chaque fonction de distance entre deux vecteurs peut être écrite comme la norme de leur différence: d(a, b) = a - b)
> La fonction de distance entre deux vecteurs peut être écrite comme la différence entre eux.

### Je suis en train de faire une petite histoire.

La norme L1 résume les valeurs absolues de tous les composants.
> L1 范数将所有分量的绝对值相加.

```
||x||_1 = |x_1| + |x_2| + ... + |x_n|
```

On l'appelle la distance de Manhattan parce qu'elle mesure la distance par laquelle on marche sur une grille de ville où on ne peut se déplacer que sur des axes.
> On appelle Manhattan distance parce qu'il mesure la distance qui se déplace sur le réseau urbain, ne peut pas aller en direction des angles.

Lorsque l'on utilise L1: données rares de haute dimension, robustesse à des valeurs hors normes, problèmes de sélection des caractéristiques (régularisation de L1 favorise la rareté).
> Quel est le temps d'utiliser L1: haute taille rareur data ⋅ sur la rareté des valeurs anormales ⋅ problème de sélection des caractéristiques ⋅

Connexion à L1 régularisation: ajoutant à la fonction de perte de l'élément (Lasso) 1 pousse les petits poids à zéro exactement, effectuant la sélection automatique des caractéristiques.
> L1 惩罚创建形约束区域,角点在轴上──

### L2 Norma (distance euclidienne)

La norme L2 est la distance en ligne droite.
> L2 范数 est une distance directe entre la base et la base.

```
||x||_2 = sqrt(x_1^2 + x_2^2 + ... + x_n^2)
```

C'est la distance que vous avez apprise en classe de géométrie.
> C'est la distance par rapport à la distance par rapport à la dimension.

Connexion à L2 régulation: l'ajout de l'unw'out2 à votre fonction de perte pénalise les poids importants. Comme L1, il ne pousse pas les poids à zéro.
> En effet, le poids de l'élément L2 ne sera pas dépassé par le poids de l'élément L2 et il ne sera pas dépassé par le poids de l'élément L2 et ne sera pas dépassé par le poids de l'élément L2 et ne sera pas dépassé par le poids de l'élément L2 et ne sera pas dépassé par le poids de l'élément L2 et ne sera pas dépassé par le poids de l'élément L2 et ne sera pas dépassé par le poids de l'élément L2 et ne sera pas dépassé par le poids de l'élément L2 et ne sera pas dépassé par le poids de l'élément L2 et ne sera pas dépassé par le poids de l'élément L2 et ne sera pas dépassé par le poids de l'élément L2 et ne sera pas dépassé par le poids de l'élément L2 et ne sera pas dépassé par le poids de l'élément L2

```
MAE (L1 loss):  |y - y_hat|         Linear penalty. Robust to outliers. / 线性惩罚，对异常值鲁棒。
MSE (L2 loss):  (y - y_hat)^2       Quadratic penalty. Sensitive to outliers. / 二次惩罚，对异常值敏感。
```

### Les normes de lp: la famille générale

L1 et L2 sont des cas particuliers de la norme Lp:
> L1 et L2 sont des exemples de Lp 范数:

```
||x||_p = (|x_1|^p + |x_2|^p + ... + |x_n|^p)^(1/p)

p=1:    Diamond shape / 菱形
p=2:    Circle/sphere / 圆/球
p=inf:  Square/hypercube / 正方形/超立方体
```

### La similitude cosine et la distance cosine.

La similitude cosine mesure l'angle entre deux vecteurs, en ignorant leurs magnitudes.
> 余弦相似度 mesure les angles entre deux émetteurs, ignorer la taille.

```
cos_sim(a, b) = (a . b) / (||a||_2 * ||b||_2)
```

Il va de -1 (directions opposées) à +1 (même direction).
> 范围 from -1(相反方向) to +1 ((同方向) ――余弦距离 = 1 - 余弦相似度──

Pourquoi le cosine domine la PNL et les emblèmes: dans le texte, la longueur du document ne devrait pas affecter la similitude. Un document sur les chats qui est deux fois plus long devrait toujours être "semblable".
> Pourquoi le reste du filet est-il "semblant" ?

### La distance de Mahalanobis à la distance de Maître

La distance euclidienne traite toutes les dimensions de la même manière.
> 欧氏距离对所有维度一视同仁――马氏距离考虑数据的协同差结构――

```
d_M(x, y) = sqrt((x - y)^T * S^(-1) * (x - y))
```

Intuitivement: la distance de Mahalanobis décorrelate et normalise d'abord les données (blanchiment), puis calcule la distance L2 dans cet espace transformé.
> L'équilibre de l'espace est calculé en L2 dans l'espace de l'espace.

### Jeccard est similaire (pour les ensembles)

Les mesures de similitude de Jaccard se chevauchent entre deux ensembles.
> Jaccard a mesuré la similitude entre deux ensembles.

```
J(A, B) = |A intersect B| / |A union B|
```

Quand utiliser Jaccard: comparer des ensembles de balises, la similitude des documents, la détection de doublons proches, l'évaluation des modèles de segmentation (IoU = Jaccard).
> Quelques années plus tard, le groupe a été créé pour la première fois en France.

### Modifier Distance (Levenshtein Distance)

La distance de modification compte le nombre minimum d'opérations à caractères simples nécessaires pour transformer une chaîne en une autre.
> 编辑距离计算将一个字符串转换为另一个所需的最小单字符操作数――使用动态规划计算――

```
"kitten" -> "sitting"
kitten -> sitten  (substitute k -> s)
sitten -> sittin  (substitute e -> i)
sittin -> sitting (insert g)

Edit distance = 3
```

### KL Divergence (pas une distance, mais utilisé comme un)

La différence KL mesure la différence entre une distribution de probabilités et une autre.
> KL 散度 mesure une probabilité de distribution par rapport à une différence de l'autre.

Lorsque vous voyez la divergence KL: VAEs, distillation des connaissances, RLHF, méthodes de gradient politique.
> Dans les scénarios suivants, voir KL 散度:VAE、知识蒸、RLHF、策略梯度方法──

### La distance de Wasserstein (distance du Mover Terre)

La distance de Wasserstein mesure le minimum de "travail" nécessaire pour transformer une distribution de probabilité en une autre. C'est une métrique vraie (symétrique, satisfait l'inégalité triangulaire). Elle fournit des gradients même lorsque les distributions ne se chevauchent pas (la divergence KL va à l'infini). Cette propriété en a fait le centre des WGAN.
> Wasserstein  distance mesure transformera une distribution de probabilité en une autre "功" minimale nécessaire. C'est une mesure réelle.

### Pourquoi différentes tâches ont besoin de distances différentes

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

### Le lien avec la normalisation et la normalisation.

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

Pourquoi L1 produit une rareté mais L2 ne le fait pas: imaginez la région de contrainte dans un espace de poids 2D. L1 est un diamant, L2 est un cercle. Les contours de la fonction de perte sont plus susceptibles de toucher le diamant à un coin, où un poids est zéro. Ils touchent le cercle à un point lisse, où les deux poids ne sont pas zéro.
> Pourquoi L1  produit rarogérance alors que L2 ne se produit pas: imaginez la zone de confinement 2D  en espace de poids. L1 est forme, L2 est ronde. L'équivalent de la fonction de perte de poids est le plus probable sur le contact sur le coin de la forme, où un poids est à zéro.

### Recherche de voisinage le plus proche

Les algorithmes Approximate Nearest Neighbor (ANN) échangent une petite précision pour des gains massifs de vitesse:
> Apparemment, l'algorithme de proximité (ANN) utilise une petite précision pour remplacer une accélération importante:

```
Algorithm         Approach                      Used by
HNSW              Hierarchical navigable         FAISS, Qdrant, Weaviate
                  small-world graph
IVF               Inverted file index with       FAISS (billion-scale)
                  cluster-based search
Product quant.    Compress vectors, search       FAISS (memory-constrained)
                  in compressed space
```

HNSW est l'algorithme dominant dans les bases de données vectorielles modernes.
> HNSW est le principal algorithme de la base de données moderne.

## Construisez-le et mettez-le en œuvre.
```figure
norm-unit-balls
```

## Faites-le

### Étape 1: Toutes les fonctions de norme et de distance.

Regardez !`code/distances.py`Chaque fonction est construite à partir de zéro en utilisant uniquement les mathématiques de base Python.
> 完整实现见 `code/distances.py`Il y a une autre.

### Étape 2: Les mêmes données, différentes distances, différents voisins.

La démo en .`distances.py`crée un ensemble de données, choisit un point de requête et montre comment le voisin le plus proche change en fonction de la métrique de distance.
> 演示 Créer un ensemble de données, sélectionner des points de recherche, montrer comment le voisinage proche change en fonction de la distance.

### Étape 3: Embedding de recherche de similitude.

Le code comprend une recherche simulée intégrant des similitudes qui trouve les "documents" les plus similaires à une requête en utilisant la similitude cosine par rapport à la distance L2.
> Le code contient une recherche de similitude, une recherche de similitude et une recherche de "document" le plus similaire.

## Utilisez-le avec le cadre de réalisation

L'utilisation pratique la plus courante: trouver des éléments similaires dans une base de données vectorielle.
> Utilisation réelle la plus courante: recherche d'éléments similaires dans la base de données de volumes.

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

Quand vous appelez`model.encode(text)`et ensuite rechercher une base de données vectorielle, c'est ce qui se passe sous le capot.
> Quand tu t' en fais`model.encode(text)`Puis, quand on recherche dans la base de données, c'est ce qui se passe au fond.

## Les exercices

1. Comptez les distances L1, L2 et L-infini entre (1, 2, 3) et (4, 0, 6). Vérifiez que L-inf <= L2 <= L1 est toujours valable.
   計算 (1, 2, 3) 和 (4, 0, 6) 之间 L1、L2 和 L-inf 距离──验证 L-inf <= L2 <= L1 始终成立──

2. Créer deux vecteurs où la similitude cosine est élevée (> 0,9) mais la distance L2 est grande (> 10). Expliquer géométriquement.
   创建两个余弦相似度高(> 0.9) Mais L2 距离大(> 10) 的向量──几何解释──

3. Implémenter une fonction qui renvoie le voisin le plus proche sous L1, L2, cosine et distance Mahalanobis.
   实现 une fonction à distance de L1、L2、余弦和马氏 en revenir à la proximité la plus proche.

4. Comptez la distance de Wasserstein entre [0,5, 0,5, 0,0] et [0, 0, 0, 0,5, 0,5] en utilisant la méthode CDF.
   Utilisez le CDF 方法计算 [0,5, 0,5, 0, 0] 和 [0, 0, 0,5, 0.5] de la distance de Wasserstein 距离──

5. Mettez MinHash en place pour une similitude approximative avec Jaccard.
   实现 MinHash 近似 Jaccard 相似度──与精确 Jaccard 比较──

## Les termes clés

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

## Encore une lecture

- [FAISS: A Library for Efficient Similarity Search](https://github.com/facebookresearch/faiss)- La bibliothèque de Meta pour la recherche à l'échelle de milliards d'annes
  Meta de la classe des milliards ANN 搜索库
- [Wasserstein GAN (Arjovsky et al., 2017)](https://arxiv.org/abs/1701.07875)- La distance du Mover Terre en GAN
  Wasserstein  Distance dans GAN
- [Efficient Estimation of Word Representations (Mikolov et al., 2013)](https://arxiv.org/abs/1301.3781)- Word2Vec, où cosine est devenu le code par défaut
  Word2Vec,余弦相似度 devenir un choix par défaut
- [sklearn.neighbors documentation](https://scikit-learn.org/stable/modules/neighbors.html)- guide pratique des mesures de distance
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                               
