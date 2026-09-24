# Teoría del gráfico para el aprendizaje automático 图论与机器学习

> Los gráficos son la estructura de datos de las relaciones. Si sus datos tienen conexiones, necesitas teoría de gráficos.
> 图是关系的数据结构―― Si tus datos están conectados, necesitas un gráfico―

**Type:** Build | **类型:** 动手
**Language:**¿ Qué pasa ?**语言:**Python
**Prerequisites:** Phase 1, Lessons 01-03 (linear algebra, matrices) | **前置知识:** Phase 1, 第 01-03 课（线性代数、矩阵）
**Time:** ~90 minutes | **时间:** ~90 分钟

## Objetivos de aprendizaje

- Construir una clase de gráfico con representaciones de matriz/lista adyacentes e implementar BFS y DFS.
  construir con una matriz/lista de cuadros de indicación de vecinos, implementar BFS y DFS 
- Computa el gráfico Laplacian y utiliza sus valores propios para detectar componentes conectados y nodos de grupo
  计算图拉普拉斯矩阵(Graph Laplacian) y utiliza su característica de análisis de la distribución y la concentración de puntos
- Implementar una ronda de mensaje de estilo GNN que pasa como una matriz de adyacencia multiplicada normalizada
  实现 una ronda de GNN 风格的消息传递归归归归归归归归归邻矩阵乘法
- Aplicar agrupamiento espectral para particionar un gráfico utilizando el vector Fiedler
  应用谱聚类(Spectral Clustering) usando Fiedler 向量划分图


> **【中文解读】**
> La red social, la estructura molecular, el mapa de conocimiento son imágenes. La transmisión de mensajes del GN es en esencia una matriz vecina multiplicada. El mapa de datos se utiliza para la matriz de la estructura de la matriz, más adecuado a los datos no esféricos que los K-Mans.

## El problema es la introducción del problema

Las redes sociales, las moléculas, las bases de conocimiento, las redes de citas, los mapas de carreteras, todo son gráficos. La ML tradicional trata los datos como tablas planas. Cada fila es independiente. Cada característica es una columna. Pero cuando la estructura de las conexiones importa, las tablas fallan.

> 社交网络、分子、知識库、引文网络、道路图都是图图图图图图图图图图图图图图图图图图图图图图图图图图图图图图图图图图图图图图图图图图图图图图图图图图图图图图图图图图图图图图图图图图图图图图图图图图图图图图图图图图图图图图图图图图图图图图图图图图图图图图图图图图图图图图图图图图图图图图图图图图图图图图图图图图图图图图图图图图图图图图图图图图图图图图图图图图图图图图图图图图图图图图图图图图图图图图图图图图图图图图图图图图图图图图图图图图图图图图图图图图图图图图图图图图图图图图图图图图图图图图图图图图图图图图图图图图图图图图图图图图图图图图图

Consideremos una red social. Quieres predecir qué producto comprará un usuario. Su historial de compras importa. Pero el historial de compras de sus amigos importa más. Las conexiones llevan señal.

> 考虑社交网络――你想预测用户会买什么产品―― su historia de compra es importante―― pero la historia de compra de los amigos es más importante――

O considerar una molécula. Quieres predecir si se une a una proteína. Los átomos son importantes, pero lo que realmente importa es cómo los átomos se unen entre sí. La estructura es los datos.

> O pensar en la molécula. Usted piensa en predecir si se une a la proteína. El átomo es importante, pero lo que realmente importa es cómo se une entre los átomos.

Las redes neuronales gráficas (GNN) son el área de aprendizaje profundo que más rápido crece. impulsan el descubrimiento de drogas, la recomendación social, la detección de fraude y el razonamiento gráfico del conocimiento.

> 图神经网络 (GNN) es el campo de crecimiento más rápido del aprendizaje profundo.

Necesitas cuatro cosas:
1. Una forma de representar gráficos como matrices (para que pueda multiplicarlos)
   将图表示为矩阵的方法 (), así se puede hacer矩阵乘法)
2. Algorithms de travesía para explorar la estructura del gráfico
   探索图结构的遍历算法
3. El Laplacio - la matriz más importante en la teoría de gráficos espectrales
   La matriz de Laplace es la matriz más importante de la teoría de la secuencia
4. Transmisiones de mensajes - la operación que hace que GNNs funcionen
   消息传递使 GNN 工作的操作

## El concepto central.

> **【中文解读】**
> 图是关系的数据结构──社交网络中人是节点、关注是边; moléculas atom are节点、化学键是边; conocimientos gráficos en el que el objeto es un punto、关系是边──图神经网络 (GNN) 信息传递本质是邻属矩阵乘法──谱聚类使用图拉普拉斯矩阵的特征向量聚类──

> **【拓展：图神经网络在药物发现中的突破】**
> AlphaFold2 (2020) de DeepMind utiliza gráficos de la red neuronal de predicción de la proteína 3D estructura, resuelve el problema de la doble de proteínas de la comunidad biológica de 50 años.

### Gráficos: nodos y bordes

Un gráfico G = (V, E) consiste en vértices (nodos) V y bordes E. Cada borde conecta dos nodos.

> 图 G = (V, E) 由顶点(节点) V 和边 E 组成──每条边连接两个节点──

**Directed vs undirected.**En un gráfico no dirigido, el borde (u, v) significa que u se conecta a v Y v se conecta a u. En un gráfico dirigido (digrafo), el borde (u, v) significa que u apunta a v, pero no necesariamente al revés.

> **有向与无向。**En el plano de la dirección,边 (u, v) significa u 连接 v 且 v 连接 u── en el plano de la dirección,边 (u, v) significa u 指向 v, pero en reverso no es necesario establecer──

**Weighted vs unweighted.**En un gráfico sin peso, los bordes o bien existen o no. En un gráfico ponderado, cada borde tiene un peso numérico: una distancia, un costo, una fuerza.

> **加权与无权。**En la gráfica sin derechos, el borde debe existir o no existir. En la gráfica de derechos adicionales, cada lado tiene un valor de peso numérico: distancia, costo, fuerza.

| Graph type | Example |
|-----------|---------|
| Undirected, unweighted | Facebook friendship network |
| Directed, unweighted | Twitter follow network |
| Undirected, weighted | Road map (distances) |
| Directed, weighted | Web page links (PageRank scores) |

### La matriz de la proximidad

La matriz de adyacencia A es la representación del núcleo. Para un gráfico con n nodos:

> 邻接矩阵(Adjacency Matrix) A es el núcleo de la muestra.

```
A[i][j] = 1    if there is an edge from node i to node j
A[i][j] = 0    otherwise
```

Para los gráficos no dirigidos, A es simétrico: A[i][j] = A[j][i]. Para los gráficos ponderados, A[i][j] = peso del borde (i, j).

> 对于无向图,A 是对称的:A[i][j] = A[j][i]。对加权图,A[i][j] = 边 (i, j) 的权重──

**Example -- a triangle:**

```
Nodes: 0, 1, 2
Edges: (0,1), (1,2), (0,2)

A = [[0, 1, 1],
     [1, 0, 1],
     [1, 1, 0]]
```

La matriz de adyacencia es la entrada de cada GNN. Las operaciones de la matriz en A corresponden a las operaciones en el gráfico.

> 邻矩阵是每个 GNN 的输入――对 A 的矩阵运算对应于图上的操作――

> **【中文解读】**
> 邻近矩阵是图的"数字化表示"──A[i][j]=1 表示节点 i 和 j 之间有边缘──奇之处:A^2 的元素A^2[i][j]恰好等于从 i到 j 长度为 2 的路径数──GNN de mensajes de transmisión es en esencia A 乘以特征矩阵每个节点聚邻近的信息──

### Grado

El grado de un nodo es el número de bordes conectados a él. Para los gráficos dirigidos, tienes en grado (edges entering) y en grado (edges going out).

> 节点的度(Degree) es conectado a su borde número。 para con el dibujo, con la entrada (in-degree, entry) y la salida (out-degree, out-eng) ◦

La matriz de grados D es diagonal:

> La matriz de grado es la matriz de la dirección.

```
D[i][i] = degree of node i
D[i][j] = 0    for i != j
```

Para el ejemplo del triángulo: D = diag(2, 2, 2) porque cada nodo se conecta a otros dos.

El grado le dice sobre la importancia de los nodos. El grado alto = nodo de centro. La distribución de grado de una red revela su estructura. Las redes sociales siguen las leyes de potencia (pocos centros, muchos nodos de hoja).

> 库告诉你节点重要性──高度 = 枢纽节点──网络的度分布揭示其结构──社交网络遵循律──少数枢纽,大量叶节点)──随机图的度服从泊松分布──

### BFS y DFS

Los dos algoritmos fundamentales de travesía de gráficos.

> 两种基本图遍历算法──两种都需要──

**Breadth-First Search (BFS):**Explora primero todos los vecinos, luego los vecinos de los vecinos.

> **广度优先搜索（BFS）：**Primero explorar todos los vecinos, luego es el vecino de los vecinos.

```
BFS from node 0:
  Visit 0
  Queue: [1, 2]        (neighbors of 0)
  Visit 1
  Queue: [2, 3]        (add neighbors of 1)
  Visit 2
  Queue: [3]           (neighbors of 2 already visited)
  Visit 3
  Queue: []            (done)
```

BFS encuentra los caminos más cortos en gráficos sin ponderación. La distancia desde el inicio hasta cualquier nodo es igual al nivel BFS en el que ese nodo es descubierto por primera vez. Esta es la razón por la que BFS se utiliza para las distancias de recuento de espera en las redes sociales.

> BFS encuentra el camino más corto en la gráfica sin derechos. La distancia desde el punto de partida hasta cualquier nodo es igual al nivel BFS en el momento en que el nodo fue descubierto por primera vez.

**Depth-First Search (DFS):**Ir lo más profundo posible antes de retroceder.

> **深度优先搜索（DFS）：**尽可能深入再回溯──使用(后进先出) o regreso──

```
DFS from node 0:
  Visit 0
  Stack: [1, 2]        (neighbors of 0)
  Visit 2               (pop from stack)
  Stack: [1, 3]         (add neighbors of 2)
  Visit 3               (pop from stack)
  Stack: [1]
  Visit 1               (pop from stack)
  Stack: []             (done)
```

DFS es útil para:
- Encontrar componentes conectados (ejecutar DFS desde nodos no visitados)
  寻找连通分量(从未访问节点运行 DFS)
- Detección de ciclos (borda trasera en árbol DFS)
  环检测(DFS 树中的后向边)
- Sortado topológico (orden de finalización inverso de DFS)
  拓排序(DFS 完成顺序的逆序)

| Algorithm | Data structure | Finds | Use case |
|-----------|---------------|-------|----------|
| BFS | Queue | Shortest paths | Social network distance, knowledge graph traversal |
| DFS | Stack | Components, cycles | Connectivity, topological sort |

### El gráfico laplaciano

L = D - A. La matriz más importante en la teoría de gráficos espectrales.

> L = D - A。 La matriz más importante en la teoría de la secuencia de datos―

Para el triángulo:

```
D = [[2, 0, 0],    A = [[0, 1, 1],    L = [[2, -1, -1],
     [0, 2, 0],         [1, 0, 1],         [-1, 2, -1],
     [0, 0, 2]]         [1, 1, 0]]         [-1, -1,  2]]
```

El laplacio tiene propiedades notables:

> La matriz de raplas tiene una naturaleza extraordinaria:

1. **L is positive semi-definite.**Todos los valores propios son >= 0.

> 1. **L 是半正定的。**Todos los valores de las características >= 0

2. **The number of zero eigenvalues equals the number of connected components.**Un gráfico conectado tiene exactamente un valor propio cero. Un gráfico con 3 componentes desconectados tiene tres valores propios cero.

> 2. **零特征值的个数等于连通分量的个数。**连通图恰好有一个零特征值──有3 没有连通分量的图有3零特征值──

3. **The smallest non-zero eigenvalue (Fiedler value) measures connectivity.**Un gran valor Fiedler significa que el gráfico está bien conectado. Un pequeño valor Fiedler significa que el gráfico tiene un punto débil - un cuello de botella.

> 3. **最小非零特征值（Fiedler 值）衡量连通性。**Fiedler 值大 significa que está bien conectado. Fiedler 值小 significa que tiene puntos débiles.

4. **The eigenvector of the Fiedler value (Fiedler vector) reveals the best split.**Los nodos con valores positivos van en un grupo, los nodos con valores negativos van en el otro.

> 4. **Fiedler 值对应的特征向量（Fiedler 向量）揭示最佳划分。**Los nodos de valor normal se encuentran en un grupo, los nodos de valor negativo en otro grupo.

> **【中文解读】**
> 图拉普拉斯 L = D - A es la matriz más importante en la teoría del gráfico de espectros. Tiene cuatro características clave: 1) 半正定; 2) 零特征值个数 = 连通分量个数; 3) 最小非零特征值; 3) Fiedler 值) mide la conectividad越大越紧; 4) Fiedler 量正负号将图自动分成两──这是谱聚类的数学基础.

```mermaid
graph TD
    subgraph "Graph to Matrices"
        G["Graph G"] --> A["Adjacency Matrix A"]
        G --> D["Degree Matrix D"]
        A --> L["Laplacian L = D - A"]
        D --> L
    end
    subgraph "Spectral Analysis"
        L --> E["Eigenvalues of L"]
        L --> V["Eigenvectors of L"]
        E --> C["Connected components (zeros)"]
        E --> F["Connectivity (Fiedler value)"]
        V --> S["Spectral clustering"]
    end
```

### Propiedades espectral

Los valores propios de la matriz adyacente y el laplaciano revelan propiedades estructurales sin ningún cruce.

> La estructura de la matriz de los vecinos y la de los rotadores no necesita ser explorada para revelar su naturaleza estructural.

**Spectral clustering**funciona así:
1. Cuenta el Laplacio L
   计算拉普拉斯矩阵 L
2. Encuentra los k vectores propios más pequeños de L (salta el primero, que es todos-ones para los gráficos conectados)
   找到 L's k 个最小特征向量(跳过第一个,连通图中它是全1向量)
3. Utilice esos propios vectores como nuevas coordenadas para cada nodo
   Utilice estas características de velocidad como nuevo punto de referencia de cada nodo
4. Ejecutar k-medias en esas coordenadas
   En estos lugares se ejecuta k-means

Los propios vectores de L codifican las funciones "más suaves" en el gráfico. Los nodos que están bien conectados obtienen valores propios similares. Los nodos separados por un cuello de botella obtienen valores diferentes. Los propios vectores naturalmente separan grupos.

> Por qué es efectivo?El eje de características de L codifica la función "más lisa" en el gráfico. Un buen nodo de conexión obtiene un eje de características similares.

**Random walk connection.**El laplaciano normalizado se relaciona con caminatas aleatorias en el gráfico. La distribución estacionaria de un paseo aleatorio es proporcional al grado de nodo. El tiempo de mezcla (cuán rápido converge el paseo) depende de la brecha espectral.

> **随机游走联系。**                                                                                                                                                                                                                                                              

### El mensaje se pasa

El núcleo de operaciones de las redes neuronales gráficas. Cada nodo recoge mensajes de sus vecinos, los agrega y actualiza su propio estado.

> 图神经网络的核心操作── cada nodo recoge información del vecino, las agrupa, y actualiza su propio estado──

```
h_v^(k+1) = UPDATE(h_v^(k), AGGREGATE({h_u^(k) : u in neighbors(v)}))
```

En la forma más simple, AGGREGATE = media y UPDATE = transformación lineal + activación:

```
h_v^(k+1) = sigma(W * mean({h_u^(k) : u in neighbors(v)}))
```

Esto es la multiplicación de matriz disfrazada. Si H es la matriz de todas las características del nodo y A es la matriz de adyacencia:

```
H^(k+1) = sigma(A_norm * H^(k) * W)
```

donde A_norm es la matriz de adyacencia normalizada (cada fila suma a 1).

Una ronda de mensajes que pasa permite a cada nodo "ver" a sus vecinos inmediatos. Dos rondas le permiten ver vecinos de vecinos.

> **【拓展：消息传递与 GNN 架构演进】**
> GCN (Kipf & Welling, 2017) es el mensaje más simple GNN: cada nivel hace una vez la integración de vecinos en la matriz multiplicada + 线性变换. GAT (Veličković et al., 2018)  introduce un mecanismo de atención para hacer que los puntos de aprendizaje del vecino tengan un peso importante. GraphSAGE (Hamilton et al., 2017) 支持采样邻居以处理大规模图片.

```mermaid
graph LR
    subgraph "Round 0"
        A0["Node A: [1,0]"]
        B0["Node B: [0,1]"]
        C0["Node C: [1,1]"]
    end
    subgraph "Round 1 (aggregate neighbors)"
        A1["Node A: avg(B,C) = [0.5, 1.0]"]
        B1["Node B: avg(A,C) = [1.0, 0.5]"]
        C1["Node C: avg(A,B) = [0.5, 0.5]"]
    end
    A0 --> A1
    B0 --> A1
    C0 --> A1
    A0 --> B1
    C0 --> B1
    A0 --> C1
    B0 --> C1
```

### Conceptos y aplicaciones de ML

| Concept | ML Application |
|---------|---------------|
| Adjacency matrix | GNN input representation |
| Graph Laplacian | Spectral clustering, community detection |
| BFS/DFS | Knowledge graph traversal, path finding |
| Degree distribution | Node importance, feature engineering |
| Message passing | GNN layers (GCN, GAT, GraphSAGE) |
| Eigenvalues of L | Community detection, graph partitioning |
| Spectral clustering | Unsupervised node grouping |
| PageRank | Node importance, web search |

> 概念与 ML 应用对照:邻接矩阵(GNN 输入表示) 图拉普拉斯(谱聚类、社区检测) 、BFS/DFS(知识图谱遍历、路径查找) 度分布(节点重要性、特征工程) 、消息传递(GNN 层 GCN/GAT/GraphSAGE) 、L 的特征值(社区检测聚图、划分) 、谱类(无监督节点分组) 、PageRank(节点重要性、Web 搜索) ⋅

## Construye y realiza.
```figure
graph-degree-distribution
```

## Construye el mismo

### Paso 1: Clase de gráfico desde cero

```python
class Graph:
    def __init__(self, n_nodes, directed=False):
        self.n = n_nodes
        self.directed = directed
        self.adj = {i: {} for i in range(n_nodes)}

    def add_edge(self, u, v, weight=1.0):
        self.adj[u][v] = weight
        if not self.directed:
            self.adj[v][u] = weight

    def neighbors(self, node):
        return list(self.adj[node].keys())

    def degree(self, node):
        return len(self.adj[node])

    def adjacency_matrix(self):
        import numpy as np
        A = np.zeros((self.n, self.n))
        for u in range(self.n):
            for v, w in self.adj[u].items():
                A[u][v] = w
        return A

    def degree_matrix(self):
        import numpy as np
        D = np.zeros((self.n, self.n))
        for i in range(self.n):
            D[i][i] = self.degree(i)
        return D

    def laplacian(self):
        return self.degree_matrix() - self.adjacency_matrix()
```

La lista de adyacentes (`self.adj`La conversión de matriz de adyacencia utiliza numpy porque todas las operaciones espectral lo necesitan.

> 邻接表`self.adj`) Alto Eficiencia de Almacenamiento Vecinal.

### Paso 2: BFS y DFS

```python
from collections import deque

def bfs(graph, start):
    visited = set()
    order = []
    distances = {}
    queue = deque([(start, 0)])                     # BFS 用队列：先进先出
    visited.add(start)
    while queue:
        node, dist = queue.popleft()                # 取出队列头部的节点
        order.append(node)
        distances[node] = dist                      # 距离 = BFS 层级（最短路径）
        for neighbor in graph.neighbors(node):
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append((neighbor, dist + 1))  # 邻居距离 +1
    return order, distances


def dfs(graph, start):
    visited = set()
    order = []
    stack = [start]
    while stack:
        node = stack.pop()
        if node in visited:
            continue
        visited.add(node)
        order.append(node)
        for neighbor in reversed(graph.neighbors(node)):
            if neighbor not in visited:
                stack.append(neighbor)
    return order
```

BFS utiliza un deque (cuadra doble) para O(1) popleft. DFS utiliza una lista como una pila. Ambos visitan cada nodo exactamente una vez - O(V + E) tiempo.

> BFS utiliza deque(双端队列) ejecutar O(1) popleft;DFS utiliza lista 当──两者都恰好访问每个节点一次时间复杂度 O(V+E)。

### Paso 3: Componentes conectados y valores propios laplacios

```python
def connected_components(graph):
    visited = set()
    components = []
    for node in range(graph.n):
        if node not in visited:
            order, _ = bfs(graph, node)
            visited.update(order)
            components.append(order)
    return components


def laplacian_eigenvalues(graph):
    import numpy as np
    L = graph.laplacian()
    eigenvalues = np.linalg.eigvalsh(L)
    return eigenvalues
```

`eigvalsh`Es para matrices simétricas - el Laplacian es siempre simétrico para gráficos no dirigidos. devuelve valores propios en orden ascendente. Cuenta los ceros para encontrar el número de componentes conectados.

> `eigvalsh`La matriz de raplas de la matriz de la imagen de la imagen de la matriz de la matriz de la matriz de la matriz de la matriz de la matriz de la matriz de la matriz de la matriz de la matriz de la matriz de la matriz de la matriz de la matriz de la matriz de la matriz de la matriz de la matriz de la matriz de la matriz de la matriz de la matriz de la matriz de la matriz de la matriz de la matriz de la matriz de la matriz de la matriz de la matriz de la matriz de la matriz de la matriz de la matriz de la matriz de la matriz de la matriz de la matriz de la matriz de la matriz de la matriz de la matriz de la matriz de la matriz de la matriz de la matriz de la matriz de la matriz de la matriz de la matriz de la matriz de la matriz de la matriz de la matriz de la matriz de la matriz de la matriz de la matriz de la matriz de la matriz de la matriz de la matriz de la matriz de la matriz de la matriz de la matriz de la matriz de la matriz de la matriz de la matriz de la matriz de la matriz de la matriz de la matriz de la matriz de la matriz de la matriz de la matriz de la matriz de la matriz de la matriz de la matriz de la matriz de la matriz de la matriz de la matriz de la matriz de la matriz de la matriz de la matriz de la matriz de la matriz de la matriz de la matriz de la matriz de la matriz de la matriz de la matriz de la matriz de la matriz de la matriz de la matriz de la matriz de la matriz de la matriz de la matriz de la matriz de la matriz de la matriz de la matriz de la matriz de la matriz de la matriz de la matriz de la matriz de la matriz de la matriz de la matriz de la matriz de la matriz de la matriz de la matriz de la matriz

### Paso 4: Clustering espectral

```python
def spectral_clustering(graph, k=2):
    import numpy as np
    L = graph.laplacian()                           # 计算图拉普拉斯矩阵 L = D - A
    eigenvalues, eigenvectors = np.linalg.eigh(L)   # 特征分解（对称矩阵用 eigh）
    features = eigenvectors[:, 1:k+1]               # 取第 2 到 k+1 个特征向量（跳过第一个全 1 向量）

    labels = np.zeros(graph.n, dtype=int)
    for i in range(graph.n):
        if features[i, 0] >= 0:                     # Fiedler 向量 >= 0 → 簇 A
            labels[i] = 0
        else:                                       # Fiedler 向量 < 0 → 簇 B
            labels[i] = 1
    return labels
```

Para k=2, el signo del vector de Fiedler divide el gráfico en dos grupos. para k>2, ejecutarías k-medias en los primeros k vectores propios (excluyendo el trivial vector propio de todos los únicos).

> k=2 时,Fiedler 向量的符号把图分成两──k>2 时,在前 k 个特征向量上跑 k-means(跳过平凡的全1特征向量) ⋅

### Paso 5: Transmisión del mensaje

```python
def message_passing(graph, features, weight_matrix):
    import numpy as np
    A = graph.adjacency_matrix()
    row_sums = A.sum(axis=1, keepdims=True)
    row_sums[row_sums == 0] = 1
    A_norm = A / row_sums
    aggregated = A_norm @ features
    output = aggregated @ weight_matrix
    return output
```

Esta es una ronda de transmisión de mensajes GNN. Las nuevas características de cada nodo son el promedio ponderado de las características de sus vecinos, transformado por la matriz de peso.

> Es una ronda de transmisión de noticias de GNN. Cada nodo tiene una nueva característica.

## Usalo con el marco de ejecución

Con networkx y numpy, las mismas operaciones son de una línea:

> Usando redx y numpy, el mismo operativo es una línea de código:

```python
import networkx as nx
import numpy as np

G = nx.karate_club_graph()

A = nx.adjacency_matrix(G).toarray()
L = nx.laplacian_matrix(G).toarray()

eigenvalues = np.linalg.eigvalsh(L.astype(float))
print(f"Smallest eigenvalues: {eigenvalues[:5]}")
print(f"Connected components: {nx.number_connected_components(G)}")

communities = nx.community.greedy_modularity_communities(G)
print(f"Communities found: {len(communities)}")

pr = nx.pagerank(G)
top_nodes = sorted(pr.items(), key=lambda x: x[1], reverse=True)[:5]
print(f"Top 5 PageRank nodes: {top_nodes}")
```

networkx maneja gráficos de cualquier tamaño con backends optimizados en C. Utilice en la producción. Utilice su implementación desde cero para entender lo que hace.

> redx utiliza el C 后端 optimizado para procesar cualquier tamaño de la imagen.

### análisis espectral de la nudidad

```python
import numpy as np

A = np.array([
    [0, 1, 1, 0, 0],
    [1, 0, 1, 0, 0],
    [1, 1, 0, 1, 0],
    [0, 0, 1, 0, 1],
    [0, 0, 0, 1, 0]
])

D = np.diag(A.sum(axis=1))
L = D - A

eigenvalues, eigenvectors = np.linalg.eigh(L)
print(f"Eigenvalues: {np.round(eigenvalues, 4)}")
print(f"Fiedler value: {eigenvalues[1]:.4f}")
print(f"Fiedler vector: {np.round(eigenvectors[:, 1], 4)}")

fiedler = eigenvectors[:, 1]
group_a = np.where(fiedler >= 0)[0]
group_b = np.where(fiedler < 0)[0]
print(f"Cluster A: {group_a}")
print(f"Cluster B: {group_b}")
```

El vector Fiedler hace la tarea pesada. entradas positivas en un grupo, negativas en el otro. No se necesita optimización iterativa, sólo una propia composición.

## Envíe el producto .

Esta lección produce:
- `outputs/skill-graph-analysis.md`-- una referencia de habilidades para analizar datos estructurados en gráficos

## Conexiones conceptos relacionados mapa

| Concept | Where it shows up |
|---------|------------------|
| Adjacency matrix | GCN, GAT, GraphSAGE input |
| Laplacian | Spectral clustering, ChebNet filters |
| BFS | Knowledge graph traversal, shortest path queries |
| Message passing | Every GNN layer, neural message passing |
| Spectral gap | Graph connectivity, mixing time of random walks |
| Degree distribution | Power-law networks, node feature engineering |
| Connected components | Preprocessing, handling disconnected graphs |
| PageRank | Node importance ranking, attention initialization |

Las GNN merecen mención especial. La operación de convolución de gráfico en GCN (Kipf & Welling, 2017) utiliza la matriz de adyacencia con los bucles automáticos añadidos, A_hat = A + I:

```text
H^(l+1) = sigma(D_hat^(-1/2) * A_hat * D_hat^(-1/2) * H^(l) * W^(l))
```

donde A_hat = A + I (adyacencia más auto-bucles) y D_hat es la matriz de grados de A_hat. Los circuitos automáticos aseguran que cada nodo incluya sus propias características durante la agregación. Este es exactamente el mensaje que pasa con normalización simétrica. D_hat^(-1/2) * A_hat * D_hat^(-1/2) es la matriz de adyacencia normalizada. El Laplaciano aparece porque esta normalización está relacionada con L_sym = I - D^(-1/2) * A * D^(-1/2). Comprender el Laplacio significa entender por qué funcionan las GCN.

> GNN 值得特别说明──GCN(Kipf & Welling, 2017) 图卷积用加了自环的邻属矩阵 A_hat = A + I:H^(l+1) = σ(D_hat^(-1/2) A_hat D_hat^(-1/2) H^(l) W^(l))──自环让每个节点聚合时包含自身特征──这就是对称归结的消息传递──理解拉普拉斯阵阵 =理解GCN 为何有效──

## Los ejercicios.

1. **Implement PageRank from scratch.**Comience con puntuaciones uniformes. En cada paso: puntuación(v) = (1-d) /n + d * suma(puntuación(u) /out_degree(u)) para todos los u que apuntan a v. Utilice d=0.85.

2. **Find communities using spectral clustering.**Crear un gráfico con dos grupos claramente separados (por ejemplo, dos cliques conectados por un solo borde). ejecutar el agrupamiento espectral y verificar que encuentra la división correcta. ¿Qué sucede cuando se añaden más bordes cruzados de grupo?

3. **Implement Dijkstra's algorithm**Comparar los resultados con BFS en el mismo gráfico con pesos uniformes.

4. **Build a 2-layer message passing network.**Aplicar el mensaje que pasa dos veces con diferentes matrices de peso. Muestre que después de 2 rondas, cada nodo tiene información de su vecindario de 2 pasos.

5. **Analyze a real-world graph.**Utilice el gráfico del Club de Karate (34 nodos, 78 bordes). Computa la distribución de grados, los valores propios de Laplacia y el agrupamiento espectral. Compara el resultado del agrupamiento espectral con la división de verdad de tierra conocida.

## Términos clave .

| Term | What people say | What it actually means |
|------|----------------|----------------------|
| Graph | "Nodes and edges" | A mathematical structure G=(V,E) encoding pairwise relationships |
| Adjacency matrix | "The connection table" | An n x n matrix where A[i][j] = 1 if nodes i and j are connected |
| Degree | "How connected a node is" | The number of edges touching a node |
| Laplacian | "D minus A" | L = D - A, the matrix whose eigenvalues reveal graph structure |
| Fiedler value | "The algebraic connectivity" | The smallest non-zero eigenvalue of L, measuring how well-connected the graph is |
| BFS | "Level-by-level search" | Traversal that visits all neighbors before going deeper, finds shortest paths |
| DFS | "Go deep first" | Traversal that follows one path to its end before backtracking |
| Message passing | "Nodes talk to neighbors" | Each node aggregates information from its neighbors, the core of GNNs |
| Spectral clustering | "Cluster by eigenvectors" | Partition a graph using eigenvectors of its Laplacian |
| Connected component | "A separate piece" | A maximal subgraph where every node can reach every other node |

> 术语速查:Graph(图 G=(V,E))、Adjacency matrix(邻接矩阵 A[i][j]=1 表示 i、j 连接)、Degree(度,节点连接的边数)、Laplacian(拉普拉斯 L=D-A)、Fiedler value(最小非零特征值,代数连通性)、BFS(广度优先,按层遍历)、DFS深度优先,走到底再回溯)、Message passing(消息传递,GNN 核心)、Spectral clustering using拉普拉斯特征向量聚类)、Connected component(连通量)、

## Más Leer más Leer más

- **Kipf & Welling (2017)**-- "Clasificación semisupervisada con redes convolutivas de gráficos". El documento que lanzó las GNNs modernas. Muestra que las convoluciones de gráficos espectrales simplifican el pasaje de mensajes.
- **Spielman (2012)**-- "Teoría del gráfico espectral" notas de conferencia. La introducción definitiva a los laplacios, las lagunas espectral, y la partición del gráfico.
- **Hamilton (2020)**-- "Aprendizaje de representación gráfica". Libro que abarca las GNN desde los fundamentos hasta las aplicaciones.
- **Bronstein et al. (2021)**-- "Depth Learning Geometric: Grids, Groups, Graphs, Geodesics, and Gauges". El documento marco unificador.
- **Veličković et al. (2018)**-- "Graph Attention Networks". Ampliará el mensaje que pasa con mecanismos de atención.
