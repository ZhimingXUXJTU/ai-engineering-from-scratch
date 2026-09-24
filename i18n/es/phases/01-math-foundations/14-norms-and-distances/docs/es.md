# Normas y distancias.

> Su función de distancia define lo que significa "similar".
> La distancia de la función define el significado de "parecido".

**Type:** Build | **类型:** 动手
**Language:**¿ Qué pasa ?**语言:**Python
**Prerequisites:** Phase 1, Lessons 01 (Linear Algebra Intuition), 02 (Vectors, Matrices & Operations) | **前置知识:** Phase 1, Lessons 01-02
**Time:** ~90 minutes | **时间:** ~90 分钟

## Objetivos de aprendizaje

- Implemente L1, L2, cosino, Mahalanobis, Jaccard, y edite las funciones de distancia desde cero
  Desde el 0 realizar L1、L2、余弦、马氏、Jaccard 和 editar la función de distancia
- Seleccione la métrica de distancia apropiada para una tarea de ML dada y explique por qué las alternativas fallan
  Para determinar las tareas de ML, seleccionar la distancia adecuada y explicar por qué otras opciones fracasarán.
- Conectar las normas L1 y L2 a la regularización LASSO y Ridge y sus regiones de restricción geométrica
  Enlace las L1 y L2 范数 con LASSO 和 Ridge  正则化及其几何束区
- Demostrar cómo el mismo conjunto de datos produce diferentes vecinos más cercanos bajo diferentes métricas
  演示 El mismo conjunto de datos se produce en diferentes dimensiones en diferentes proximidades

> **【中文解读】**
> 距离函数 define similar signification──L1对应 LASSO(特征选择),L2对应 Ridge(防止过拟合),余弦距离适合词嵌入,编辑距离适合字符串──梯度剪剪 L2 范数限制梯度大小──

## El problema es la introducción del problema

> **【中文解读】**"¿Qué similitud tienen estos dos vectores?" la respuesta depende completamente de qué función de distancia elijas. La misma par de datos en L2 es la vecindad más cercana, en el cuadro de distancia de cuerda puede ser muy lejos.

## El concepto central.

> **【拓展：范数在 AI 中的四大应用】**(1) **L2 正则化**¿Qué es esto ?`loss + lambda * ||w||_2^2`, prevenir el peso excesivo, aliviar el exceso de capacidad;**梯度裁剪**¿Qué es esto ?`||grad|| > max_norm`时缩放梯度,Transformer 训练的标配;(3) **余弦相似度**:RAG 检索和推系统的标准度量, sólo看方向不看大小;(4) **LayerNorm**Para cada nivel de salida hacer L2 归结,稳定训练过程―― comprensión de la variante es la base matemática de la comprensión de la normalización y la归结――

No hay una distancia universal mejor. L2 funciona para datos espaciales. La similitud cosínica domina la PNL. Jaccard maneja conjuntos. Editar distancia maneja cuerdas. Mahalanobis cuenta por correlaciones. Wasserstein mueve masa de probabilidad. Cada uno codifica una suposición diferente sobre lo que significa "similar".
> 没有万能的最佳距离――L2 适合空间数据,余弦相似度主导 NLP,Jaccard 处理集合,编辑距离处理字符串,马氏距离考虑相关性,Wasserstein 移动概率质量―― cada uno codificó sobre las diferentes hipótesis del significado de "相似"――

Esta lección construye todas las funciones de distancia importantes desde cero, muestra cuándo cada una es la herramienta correcta, y demuestra cómo los mismos datos producen vecinos más cercanos completamente diferentes dependiendo de qué métrica se utiliza.
> Este curso se desarrolla desde cero construyendo cada función de distancia principal, mostrando cuándo usar cuál, y mostrando que los mismos datos se producen en diferentes dimensiones en un vecindario completamente diferente.

### Normas: medición de magnitud de vector 范数: medir tamaño de

norma mide el "tamaño" de un vector. Cada función de distancia entre dos vectores se puede escribir como la norma de su diferencia: d(a, b) = a - b)
> 范数 mide la "grandeza" de un espectro. La función de distancia entre dos espectros puede ser escrita como un范数 de diferencia entre ellos.

### L1 Norm (Distancia de Manhattan)  L1 范数(Distancia de Manhattan)

La norma L1 suma los valores absolutos de todos los componentes.
> L1 范数将所有分量的绝对值相加.

```
||x||_1 = |x_1| + |x_2| + ... + |x_n|
```

Se llama distancia de Manhattan porque mide la distancia que caminas en una red de la ciudad donde solo puedes moverte a lo largo de ejes.
> Se llama Manhattan Distance porque mide la distancia que se mueve en la red urbana, no puede ir en contra de las esquinas.

Cuando utilizar L1: datos escasos de alta dimensión, robustez a valores extremos, problemas de selección de características (la regularización de L1 promueve la escasez).
> ¿Cuándo utilizar L1: Alta dimensión de datos raros  Rústicidad de los valores anormales  Problemas de selección de características 

Conexión a L1 regularization: añadiendo a la función de pérdida (Lasso) 1 a la función de pérdida empuja los pesos pequeños a exactamente cero, realizando la selección automática de características. La penalidad L1 crea regiones de restricción en forma de diamante, y las esquinas se encuentran en ejes donde algunos pesos son cero.
> En el caso de las funciones de L1 (Lasso), el ejecutor puede ejecutar la función de L1 (Lasso) en el caso de la función de L1 (Lasso):

### L2 Norma (distancia euclidiana)

La norma L2 es la distancia en línea recta.
> L2 范数 ∈ L2 ∈ L2 ∈ L2 ∈ L2 ∈ L2 ∈ L2 ∈ L2 ∈ L2 ∈ L2 ∈ L2 ∈ L2 ∈ L2 ∈ L2 ∈ L2 ∈ L2 ∈ L2 ∈ L2 ∈ L2 ∈ L2 ∈ L2 ∈ L2 ∈ L2 ∈ L2 ∈ L2 ∈ L2 ∈ L2 ∈ L2 ∈ L2 ∈ L2 ∈ L2 ∈ L2 ∈ L2 ∈ L2 ∈ L2 ∈ L2 ∈ L2 ∈ L2 ∈ L2 ∈ L2 ∈ L2 ∈ L2 ∈ L2 ∈ L2 ∈ L2 ∈ L2 ∈ L2 ∈ L2 ∈ L2 ∈ L2 ∈ L2 ∈ L2 ∈ L2 ∈ L2 ∈ L2 ∈ L2 ∈ L2 ∈ L2 ∈ L2 ∈ L2 ∈ L2 ∈ L2 ∈ L2 ∈ L2 ∈ L2 ∈ L2 ∈ L2 ∈ L2 ∈ L2 ∈ L2 ∈ L2 ∈ L2 ∈ L2 ∈ L2 ∈ L2 

```
||x||_2 = sqrt(x_1^2 + x_2^2 + ... + x_n^2)
```

Esta es la distancia que aprendiste en la clase de geometría.
> Es la teoría de la distancia entre las clases de geometría.

Conexión a L2 regularization: añadir un 2^2 a la función de pérdida penaliza pesos grandes. al igual que L1, no empuja pesos a cero. La penalización L2 crea regiones de restricción circulares, por lo que no hay esquinas en ejes.
> En el caso de la función de pérdida de L2 ∞, el peso de la carga no será de igual peso que el de L1 ∞, el peso no será de 0 ∞.

```
MAE (L1 loss):  |y - y_hat|         Linear penalty. Robust to outliers. / 线性惩罚，对异常值鲁棒。
MSE (L2 loss):  (y - y_hat)^2       Quadratic penalty. Sensitive to outliers. / 二次惩罚，对异常值敏感。
```

### Las normas de la familia general.

L1 y L2 son casos especiales de la norma Lp:
> L1 y L2 son ejemplos de Lp 范数:

```
||x||_p = (|x_1|^p + |x_2|^p + ... + |x_n|^p)^(1/p)

p=1:    Diamond shape / 菱形
p=2:    Circle/sphere / 圆/球
p=inf:  Square/hypercube / 正方形/超立方体
```

### Similaridad cosínica y distancia cosínica.

La similitud cosínica mide el ángulo entre dos vectores, ignorando sus magnitudes.
> 余弦相似度 mide el ángulo entre dos vectores, ignorar el tamaño.

```
cos_sim(a, b) = (a . b) / (||a||_2 * ||b||_2)
```

Se extiende desde -1 (direcciones opuestas) hasta +1 (la misma dirección).
> 范围 from -1(相反方向) to +1 ((同方向) ――余弦距离 = 1 - 余弦相似度──

Por qué el cosino domina la PNL y las incorporaciones: en el texto, la longitud del documento no debe afectar a la similitud. Un documento sobre gatos que es el doble de largo debe seguir siendo "similar".
> Por qué el tiempo de la película se reduce a un tiempo de trabajo de la película? ¿Por qué el tiempo de la película se reduce a un tiempo de trabajo de la película?

### Distancia Mahalanobis Distancia de Mace

La distancia euclidiana trata todas las dimensiones de manera igual.
> 欧氏距离对所有维度一视同仁――马氏距离考虑数据的协方差结构――

```
d_M(x, y) = sqrt((x - y)^T * S^(-1) * (x - y))
```

Intuitivamente: la distancia de Mahalanobis primero descorrela y normaliza los datos (blanqueamiento), luego calcula la distancia L2 en ese espacio transformado.
> Intuition: Mace distancia primero se relaciona y se vuelve unidad de datos (), luego se calcula L2 distancia en el espacio después de la transformación.

### Jaccard Similaridad (para conjuntos)

Las medidas de similitud de Jaccard se superponen entre dos conjuntos.
> Jaccard comparabilidad mide la superposición de dos conjuntos.

```
J(A, B) = |A intersect B| / |A union B|
```

Cuando utilizar Jaccard: comparar conjuntos de etiquetas, similitud de documentos, detección de casi duplicados, evaluación de modelos de segmentación (IoU = Jaccard).
> ¿Cuándo usar Jaccard: Comparar el conjunto de etiquetas, la similitud de los archivos, la similitud de los archivos, la similitud de los archivos, la similitud de los archivos, la similitud de los archivos, la similitud de los archivos, la similitud de los archivos, la similitud de los archivos, la similitud de los archivos, la similitud de los archivos, la similitud de los archivos, la similitud de los archivos, la similitud de los archivos, la similitud de los archivos, la similitud de los archivos, la similitud de los archivos, la similitud de los archivos, la similitud de los archivos, etc.

### Edit Distancia (Distancia Levenshtein) 编辑距离(Levenshtein 距离)

La distancia de edición cuenta el número mínimo de operaciones de un solo carácter necesarias para transformar una cadena en otra.
> 编辑距离计算将一个字符串转换为另一个所需的最小单字符操作数――使用动态规划计算――

```
"kitten" -> "sitting"
kitten -> sitten  (substitute k -> s)
sitten -> sittin  (substitute e -> i)
sittin -> sitting (insert g)

Edit distance = 3
```

### KL Divergencia (no una distancia, pero se utiliza como uno)

La diferencia KL mide la diferencia entre una distribución de probabilidades y otra. Propiedad crítica: NO simétrica. D_KL(P
> KL 散度 mide una distribución de probabilidad con la diferencia de otro.

Cuando se ve la divergencia KL: VAEs, destilación del conocimiento, RLHF, métodos de gradiente de política.
> En los siguientes escenarios ver KL 散度:VAE、知识蒸、RLHF、策略梯度方法──

### La distancia de Wasserstein (Distancia del Mover de la Tierra)

La distancia de Wasserstein mide el "trabajo" mínimo necesario para transformar una distribución de probabilidades en otra. Es una métrica verdadera (simétrica, satisface la desigualdad del triángulo). Proporciona gradientes incluso cuando las distribuciones no se superponen (la divergencia de KL va al infinito). Esta propiedad la hizo central para WGANs.
> Wasserstein  distancia de medida transformará una distribución de probabilidad en otra "功" mínima necesaria. Es una medida real.

### ¿Por qué las diferentes tareas necesitan distancias diferentes?

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

### Conexión con la regularización y la normalización.

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

Por qué L1 produce escasez pero L2 no: imagen la región de restricción en el espacio de peso 2D. L1 es un diamante, L2 es un círculo. Los contornos de la función de pérdida son más propensos a tocar el diamante en una esquina, donde un peso es cero. Tocan el círculo en un punto liso, donde ambos pesos no son cero.
> Por qué L1  produce rarequidad y L2 no: imagina 2D  área de confinamiento en el espacio de peso. L1 es forma, L2 es redonda.

### Buscar vecino más cercano Buscar vecino más reciente

Los algoritmos de vecino más cercano (ANN) intercambian una pequeña cantidad de precisión para obtener grandes ganancias de velocidad:
> Algorithms de proximidad (ANN) con poca precisión cambian a una aceleración considerable:

```
Algorithm         Approach                      Used by
HNSW              Hierarchical navigable         FAISS, Qdrant, Weaviate
                  small-world graph
IVF               Inverted file index with       FAISS (billion-scale)
                  cluster-based search
Product quant.    Compress vectors, search       FAISS (memory-constrained)
                  in compressed space
```

HNSW es el algoritmo dominante en las bases de datos vectoriales modernas.
> HNSW es el principal algoritmo de la base de datos de movimiento moderno.

## Construye y realiza.
```figure
norm-unit-balls
```

## Construye el mismo

### Paso 1: Todas las funciones normales y de distancia.

¿ Qué ?`code/distances.py`Cada función se construye desde cero utilizando sólo matemáticas básicas de Python.
> 完整实现见 `code/distances.py`¿Qué es eso?

### Paso 2: Los mismos datos, distancias diferentes, vecinos diferentes.

La demostración en `distances.py`crea un conjunto de datos, elige un punto de consulta y muestra cómo cambia el vecino más cercano dependiendo de la métrica de distancia.
> 演示 Crea un conjunto de datos, selecciona puntos de consulta, muestra cómo el vecino más cercano cambia con la distancia de medida.

### Paso 3: Incorporar búsqueda de similitud.

El código incluye una búsqueda de similitud simulada que encuentra los "documentos" más similares a una consulta utilizando similitud cosina vs distancia L2.
> 代码包含模拟嵌入相似度搜索, 余弦相似度和 L2 距离寻找最相似的"文档"──

## Usalo con el marco de ejecución

El uso práctico más común: encontrar elementos similares en una base de datos vectorial.
> Uso real más común: en la base de datos de velocidades buscar elementos similares.

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

Cuando llames .`model.encode(text)`y luego buscar una base de datos vectorial, esto es lo que sucede debajo de la capucha.
> Cuando tú调用 `model.encode(text)`Entonces, cuando buscas en la base de datos de velocidades, eso es lo que pasa en el fondo.

## Los ejercicios.

1. Calcule las distancias L1, L2 y L-infinidad entre (1, 2, 3) y (4, 0, 6). Verifique que L-inf <= L2 <= L1 siempre se mantiene.
   計算 (1, 2, 3) 和 (4, 0, 6) 之间 L1、L2 和 L-inf 距离──验证 L-inf <= L2 <= L1 始终成立──

2. Crear dos vectores donde la similitud cosinosa es alta (> 0,9) pero la distancia L2 es grande (> 10).
   创建两个余弦相似度高(> 0.9) pero L2 距离大(> 10) de la magnitud.

3. Implemente una función que devuelve al vecino más cercano bajo la distancia L1, L2, cosino y Mahalanobis.
   实现 la función en L1、L2、余弦和马氏 distancia abajo regresa a la vecindad más cercana. Encontrar cuatro tipos de medidas totalmente incompatibles.

4. Calcule la distancia de Wasserstein entre [0,5, 0,5, 0,0] y [0, 0, 0, 0,5, 0,5] utilizando el método CDF.
   Us CDF 方法计算 [0,5, 0,5, 0, 0] y [0, 0, 0,5, 0.5] de Wasserstein 距离──

5. Implemente MinHash para obtener una similitud aproximada con Jaccard.
   实现 MinHash 近似 Jaccard 相似度──与精确 Jaccard 比较──

## Términos clave .

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

## Más Leer más Leer más

- [FAISS: A Library for Efficient Similarity Search](https://github.com/facebookresearch/faiss)- La biblioteca de Meta para la búsqueda de ANN a escala de miles de millones
  Meta de la categoría de miles de millones de ANN  búsqueda
- [Wasserstein GAN (Arjovsky et al., 2017)](https://arxiv.org/abs/1701.07875)- La distancia del Mover de la Tierra en GAN
  Wasserstein  Distancia en GAN
- [Efficient Estimation of Word Representations (Mikolov et al., 2013)](https://arxiv.org/abs/1301.3781)- Word2Vec, donde cosino se convirtió en el predeterminado
  Word2Vec,余弦相似度 se convirtió en la opción de preferencia
- [sklearn.neighbors documentation](https://scikit-learn.org/stable/modules/neighbors.html)- Guía práctica de las métricas de distancias
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                               
