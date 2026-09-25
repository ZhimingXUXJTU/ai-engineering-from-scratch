# Normas e Distâncias.

> A função de distância define o que significa "semelhante".
> A função distância define o significado de "semelhante".

**Type:** Build | **类型:** 动手
**Language:**O Python .**语言:**Python
**Prerequisites:** Phase 1, Lessons 01 (Linear Algebra Intuition), 02 (Vectors, Matrices & Operations) | **前置知识:** Phase 1, Lessons 01-02
**Time:** ~90 minutes | **时间:** ~90 分钟

## Objetivos de aprendizagem

- Implementar L1, L2, cosino, Mahalanobis, Jaccard e editar funções de distância a partir do zero
  Desde zero realização L1、L2、余弦、马氏、Jaccard 和编辑距离函数
- Selecionar a métrica de distância adequada para uma determinada tarefa de ML e explicar por que as alternativas falham
  Para determinar a tarefa de seleção da distância adequada e explicar por que outras escolhas falham.
- Conectar as normas L1 e L2 à regularização LASSO e Ridge e às suas regiões de restrições geométricas
  L1 e L2 范数  LASSO 和 Ridge 正规化及其几何束区
- Demonstrar como o mesmo conjunto de dados produz diferentes vizinhos mais próximos sob diferentes métricas
  Demonstração do mesmo conjunto de dados em diferentes dimensões

> **【中文解读】**
> 距离函数 define significados similares. L1 对应 LASSO(特征选择), L2 对应 Ridge(防止过拟合),余弦距离适合词嵌入,编辑距离适合字符串──梯度剪剪 L2 范数限制梯度大小──

## O problema é o problema da introdução

> **【中文解读】**"Estes dois vectores têm alguma semelhança?" A resposta depende completamente da função de distância que você escolher.

## O conceito central.

> **【拓展：范数在 AI 中的四大应用】**(1) **L2 正则化**- Não .`loss + lambda * ||w||_2^2`, prevenir o peso excessiva, aliviar o peso;**梯度裁剪**- Não .`||grad|| > max_norm`时缩放梯度,Transformador 训练的标配;(3) **余弦相似度**:RAG 检索和推系统的标准度,只看方向不看大小;(4) **LayerNorm**Para cada nível de saída fazer L2 归结,稳定训练过程―― compreender范数就是理解正则化和归结的数学基础――

Não há melhor distância universal. L2 funciona para dados espaciais. A semelhança cosínica domina a PNL. Jaccard lida com conjuntos. Edit distance manipula cordas. Mahalanobis conta para correlações. Wasserstein move probabilidade massa. Cada um codifica uma suposição diferente sobre o que "semelhante" significa.
> 没有万能的最佳距离――L2 适合空间数据,余弦相似度主导 NLP,Jaccard 处理集合,编辑距离处理字符串,马氏距离考虑相关性,Wasserstein 移动概率质量──每个都编码了关于"相似"意义的不同假设──

Esta lição construi todas as principais funções de distância a partir do zero, mostra-lhe quando cada uma é a ferramenta certa, e demonstra como os mesmos dados produzem vizinhos mais próximos completamente diferentes dependendo de qual métrica você usa.
> Este curso consiste em construir cada função de distância principal a partir de zero, demonstrar quando usar qual, e demonstrar que os mesmos dados são gerados em diferentes dimensões.

### Normas: medição de magnitude de vetor .

Norma mede o " tamanho " de um vetor. Cada função de distância entre dois vetores pode ser escrita como a norma de sua diferença: d  a, b) = a - b                                                                                                                                                                                                                                         
> 范数 mide "大小" (grande dimensão) de um átomo. A função de distância entre dois átomos pode ser escrita como um范数 (quantidade de diferença entre eles).

### L1 Norm (distância de Manhattan)

A norma L1 soma os valores absolutos de todos os componentes.
> L1 范数将所有分量的绝对值相加.

```
||x||_1 = |x_1| + |x_2| + ... + |x_n|
```

Chama-se distância de Manhattan porque mede a distância que percorre numa rede de cidades onde só pode mover-se ao longo de eixos.
> Chamamos Manhattan Distância porque mede a distância que se move ao longo do eixo na rede urbana, não pode ir em direção a um canto.

Quando utilizar L1: dados escassos de alta dimensão, robustez para valores fora do limite, problemas de selecção de características (a regularização de L1 promove a escassez).
> Qual é o tempo de utilização de L1: alta dimensão de dados raros, sobre a robustez de valores anormais, sobre a seleção de características, sobre o problema de

Conexão a L1 regularização: adicionando a sua função de perda (Lasso) 1 empurra pequenos pesos para exatamente zero, realizando seleção automática de características. A penalidade L1 cria regiões de restrição em forma de diamante, e as curvas estão em eixos onde alguns pesos são zero.
> Em relação ao L1 (Lasso): em função de perda, o limite de peso é de 0, e o limite de peso é de 0, e o limite de peso é de 0, e o limite de peso é de 0, e o limite de peso é de 0, e o limite de peso é de 0, e o limite de peso é de 0, e o limite de peso é de 0, e o limite de peso é de 0, e o limite de peso é de 0, e o limite de peso é de 0, e o limite de peso é de 0, e o limite de peso é de 0, e o limite de peso é de 0, e o limite de peso é de 0, e o limite de peso é de 0, e o limite de peso é de 0, e o limite de peso é de 0, e o limite de peso é de 0, e o limite de peso é de 0, e o limite de peso é de 0, e o limite de peso é de 0, e o valor é de 0, respectivamente.

### L2 Norma (distância euclidiana)

A norma L2 é a distância de linha reta.
> L2 范数是直线距离──分量平方和的平方根──

```
||x||_2 = sqrt(x_1^2 + x_2^2 + ... + x_n^2)
```

Esta é a distância que aprendeste na aula de geometria.
> É a geometria da distância entre as classes.

Conexão a L2 regularização: adicionando a Unww Descreve a sua função de perda penaliza grandes pesos.Como L1, não empurra pesos para zero. A penalidade L2 cria regiões de restrição circular, por isso não há cantos nos eixos.
> Em relação ao L2 (L2): em relação ao L1, não se pode atribuir o peso a zero.

```
MAE (L1 loss):  |y - y_hat|         Linear penalty. Robust to outliers. / 线性惩罚，对异常值鲁棒。
MSE (L2 loss):  (y - y_hat)^2       Quadratic penalty. Sensitive to outliers. / 二次惩罚，对异常值敏感。
```

### Lp Normas: a família geral .

L1 e L2 são casos especiais da norma Lp:
> L1 e L2 são exemplos de Lp 范数:

```
||x||_p = (|x_1|^p + |x_2|^p + ... + |x_n|^p)^(1/p)

p=1:    Diamond shape / 菱形
p=2:    Circle/sphere / 圆/球
p=inf:  Square/hypercube / 正方形/超立方体
```

### Semelhança cosínica e distância cosínica.

A semelhança cosínica mede o ângulo entre dois vetores, ignorando suas magnitudes.
> O 余弦相似度 mede o ângulo entre dois vectores, ignorar o tamanho.

```
cos_sim(a, b) = (a . b) / (||a||_2 * ||b||_2)
```

Ele varia de -1 (direções opostas) a +1 (a mesma direção).
> 范围 from -1(相反方向) to +1 ((同方向) ――余弦距离 = 1 - 余弦相似度──

Por que o cosino domina a PNL e as incorporações: no texto, o comprimento do documento não deve afetar a semelhança. Um documento sobre gatos que seja duas vezes mais longo deve ainda ser "semelhante".
> Porquê o longo de um arquivo de gato ainda deve ser "semelhante" ?

### Distância Mahalanobis Distância Mace

A distância euclidiana trata todas as dimensões de forma igual.
> 欧氏距离对所有维度一视同仁――马氏距离考虑数据的协同差结构――

```
d_M(x, y) = sqrt((x - y)^T * S^(-1) * (x - y))
```

Intuitivamente: a distância de Mahalanobis primeiro descorrela e normaliza os dados (branquização), depois calcula a distância L2 nesse espaço transformado.
> Intuition: Mace's distance first goes related and integrated data (), then calculates L2 distance in space in the transformation of the after.

### Jaccard Similarity (para conjuntos)

As medidas de similaridade de Jaccard se sobrepõem entre dois conjuntos.
> Jaccard comparabilidade mede a sobreposição de dois conjuntos.

```
J(A, B) = |A intersect B| / |A union B|
```

Quando utilizar o Jaccard: comparação de conjuntos de etiquetas, semelhança de documentos, detecção de duplicados quase, avaliação de modelos de segmentação (IoU = Jaccard).
> 何時使用 Jaccard:比较标签集、文档相似度、近似重复检测、评估分割模型(IoU = Jaccard) 』

### Edit Distância (Levenshtein Distância) 編集距離(Levenshtein 距離)

A distância de edição conta o número mínimo de operações de um único caracteres necessárias para transformar uma cadeia em outra.
> 编辑距离计算将一个字符串转换为另一个最小单字符操作数――使用动态规划计算――

```
"kitten" -> "sitting"
kitten -> sitten  (substitute k -> s)
sitten -> sittin  (substitute e -> i)
sittin -> sitting (insert g)

Edit distance = 3
```

### KL Divergência (não uma distância, mas usado como um)

A diferença KL mede como uma distribuição de probabilidade difere de outra. Propriedade crítica: NÃO simétrica. D_KL(P  Q) != D_KL(Q  P). É uma divergência, não uma distância.
> KL 散度 mede a diferença entre uma distribuição de probabilidade e outra.

Quando se vê a divergência KL: VAEs, destilação do conhecimento, RLHF, métodos de gradiente de política.
> Em cenários seguintes, veja KL 散度:VAE、知识蒸、RLHF、策略梯度方法──

### A distância de Wasserstein.

A distância de Wasserstein mede o mínimo de "trabalho" necessário para transformar uma distribuição de probabilidade em outra. É uma métrica verdadeira (simétrica, satisfaz a desigualdade triangular). Ele fornece gradientes mesmo quando as distribuições não se sobrepõem (a divergência KL vai para o infinito). Esta propriedade tornou-o central para WGANs.
> Wasserstein  Distância de medida irá transformar uma distribuição de probabilidade em outra "função" mínima necessária. É uma medida real.

### Porque diferentes tarefas precisam de diferentes distâncias?

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

### Conexão com a Regularização e a regularização.

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

Por que L1 produz escassez, mas L2 não: imagine a região de restrição em espaço de peso 2D. L1 é um diamante, L2 é um círculo. Os contornos da função de perda são mais propensos a tocar o diamante em um canto, onde um peso é zero. Eles tocam o círculo em um ponto liso, onde ambos os pesos não são zero.
> Por que L1  produz rarefacção e L2 não: imagina 2D  área de restrição no espaço de peso. L1 é form, L2 é circular. Línia de perda da função é mais possível em contacto em canto de form, onde um peso é zero.

### Busca de vizinho mais próximo Busca de vizinho mais recente

Algoritmos de Vezinho Mais Próximo (ANN) aproximados trocam uma pequena quantidade de precisão para ganhos de velocidade maciços:
> Algoritmos de proximidade (ANN) com menor precisão para trocar aceleração:

```
Algorithm         Approach                      Used by
HNSW              Hierarchical navigable         FAISS, Qdrant, Weaviate
                  small-world graph
IVF               Inverted file index with       FAISS (billion-scale)
                  cluster-based search
Product quant.    Compress vectors, search       FAISS (memory-constrained)
                  in compressed space
```

O HNSW é o algoritmo dominante em bancos de dados vetoriais modernos.
> HNSW é o principal algoritmo de dados em modelos modernos.

## Construí-lo e realizei-o.
```figure
norm-unit-balls
```

## Construí-lo

### Passo 1: Todas as funções normais e de distância.

Veja .`code/distances.py`Cada função é construída a partir do zero usando apenas matemática básica Python.
> 完整实现见 `code/distances.py`- Não.

### Passo 2: Os mesmos dados, distâncias diferentes, vizinhos diferentes.

A demonstração em`distances.py`cria um conjunto de dados, escolhe um ponto de consulta e mostra como o vizinho mais próximo muda dependendo da métrica de distância.
> 演示 criar conjuntos de dados, selecionar pontos de consulta, mostrar como os vizinhos próximos variam com a distância.

### Passo 3: Embedando a pesquisa de semelhança.

O código inclui uma busca de semelhança simulada que encontra os "documentos" mais semelhantes a uma consulta usando semelhança cosínea vs distância L2.
> O código contém análises embutidas em busca de similaridade, usando o restante de similaridade e L2 a distância de encontrar o "documento" mais similar.

## Use-o com o framework implementado.

O uso prático mais comum: encontrar itens semelhantes em um banco de dados vetorial.
> Utilização real mais comum: procurar em base de dados de volumes em busca de elementos semelhantes.

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

Quando ligares .`model.encode(text)`e depois pesquisar uma base de dados vetorial, é o que acontece sob o capô.
> Quando você está a usar`model.encode(text)`Então, quando pesquisas em base de dados de volumes, é o que acontece no fundo.

## Exercícios.

1. Calcule as distâncias L1, L2 e L-infinito entre (1, 2, 3) e (4, 0, 6). Verifique se L-inf <= L2 <= L1 sempre é válido.
   計算 (1, 2, 3) 和 (4, 0, 6) 之间 L1、L2 和 L-inf 距离──验证 L-inf <= L2 <= L1 始终成立──

2. Criar dois vetores onde a semelhança cosínica é elevada (> 0,9) mas a distância L2 é grande (> 10). Explique geometricamente.
   创建两个余弦相似度高(> 0.9) 但L2 距离大(> 10) 的向量──几何解释──

3. Implementar uma função que retorna o vizinho mais próximo sob L1, L2, cosino e distância de Mahalanobis.
   实现 função em L1、L2、余弦和马氏 distância abaixo de volta próxima vizinhança;; encontrar quatro tipos de medidas totalmente incompatíveis com o conjunto de dados;;

4. Calcule a distância de Wasserstein entre [0,5, 0,5, 0,0] e [0, 0, 0, 0,5, 0,5] usando o método CDF.
   Use CDF 方法计算 [0,5, 0,5, 0, 0] 和 [0, 0, 0,5, 0.5] 的 Wasserstein 距离──

5. Implementar MinHash para a semelhança aproximada com Jaccard.
   实现 MinHash 近似 Jaccard 相似度──与精确 Jaccard 比较──

## Termos-chave .

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

## Mais leitura 延伸阅读

- [FAISS: A Library for Efficient Similarity Search](https://github.com/facebookresearch/faiss)- Biblioteca da Meta para pesquisas em ANN em escala de bilhões
  Meta de um bilhão de anos de ANN
- [Wasserstein GAN (Arjovsky et al., 2017)](https://arxiv.org/abs/1701.07875)- Distância do Mover da Terra em GANs
  Wasserstein  Distância em GAN
- [Efficient Estimation of Word Representations (Mikolov et al., 2013)](https://arxiv.org/abs/1301.3781)- Word2Vec, onde cosino se tornou o padrão
  Word2Vec,余弦相似度 tornar-se默认选择
- [sklearn.neighbors documentation](https://scikit-learn.org/stable/modules/neighbors.html)- guia prático para as métricas de distâncias
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                               
