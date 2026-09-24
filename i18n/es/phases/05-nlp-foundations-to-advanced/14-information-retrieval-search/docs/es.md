# Recuperación de información y búsqueda de información

> BM25 es preciso pero frágil. Denso lanza una red amplia pero se pierden palabras clave. Hybrid es el estándar de 2026. Todo lo demás está sintonizado.
> BM25 精确但脆弱──密检索撒大网但漏掉关键词──混合检索是2026年默认选择──其余都是调参──

> **【中文解读】**Desde el término clave de la correspondencia hasta la detección de velocidades, el detector de RAG es la aplicación de la detección de información.

**Type:** Build | **类型:** 动手
**Languages:** Python | **语言:** Python
**Prerequisites:** Phase 5 · 02 (BoW + TF-IDF), Phase 5 · 04 (GloVe, FastText, Subword) | **前置知识:** Phase 5 · 02 (BoW + TF-IDF), Phase 5 · 04 (GloVe, FastText, Subword)
**Time:** ~75 minutes | **时间:** ~75 minutes


## El problema es la introducción del problema

El usuario escribe "qué sucede si alguien miente para obtener dinero" y espera encontrar el estatuto que realmente cubre eso: "Sección 420 IPC". Una búsqueda de palabras clave se pierde por completo (no hay vocabulario compartido). Una búsqueda semántica se pierde si los embebidos no fueron entrenados en texto legal.
> Usuario ingresó "qué sucede si alguien miente para obtener dinero" y esperaba encontrar una cobertura real de este contenido de la normativa:"Sección 420 IPC"―.

> **【中文解读】**La pregunta planteada en este capítulo es: ¿cómo entender y aplicar correctamente esta tecnología en la ingeniería real? Comprender el contexto de la cuestión ayuda a comprender los puntos clave de decisión del tipo de selección técnica. En los sistemas de IA reales, el tipo de selección técnica errónea suele ser más alto que el costo de error de la realización de detalles.


IR es el tubo bajo cada sistema RAG, cada barra de búsqueda, cada búsqueda de documentos. La arquitectura 2026 que funciona en la producción no es un solo método. Es una cadena de métodos complementarios, cada uno de los cuales atrapa los fallos de la anterior.
> IR es cada sistema RAG, cada búsqueda, cada sitio de archivos, cada red de datos, cada red de archivos, cada red de archivos, cada red de archivos, cada red de archivos, cada red de archivos, cada red de archivos, cada red de archivos, cada red de archivos, cada red de archivos, cada red de archivos, cada red de archivos, cada red de archivos, cada red de archivos, cada red de archivos, cada red de archivos, cada red de archivos, cada red de archivos, cada red de archivos, cada red de archivos, cada red de archivos, cada red de archivos, cada red de archivos, cada red de archivos, cada red de archivos, cada red de archivos, cada red de archivos, cada red de archivos, cada red de archivos, cada red de archivos, cada red de archivos, cada red de archivos, cada red de archivos, cada red de archivos, cada red de archivos, cada red de archivos, cada red de archivos, cada red de archivos, y cada red de archivos, cada red de archivos, y de archivos, en el que se encuentran, en el que se encuentran en el mismo, en el que se encuentran en el mismo en el mismo en el mismo en el mismo en el mismo en el mismo en el mismo en el mismo en el mismo en el mismo en el mismo en el mismo en el mismo en el mismo en el mismo en el mismo.

Esta lección construye cada pieza y nombres que fracasan cada captura.
> Este curso construye cada parte y señala los fracasos que cada uno ha capturado.

> **【中文解读】**Este capítulo presenta los conceptos y teorías básicos. La comprensión de estos conceptos es el prerrequisito de la realización posterior de la actividad, y también el conocimiento de los puntos de alta frecuencia de la entrevista y la práctica de la ingeniería.


## El concepto central.

![Hybrid retrieval: BM25 + dense + RRF + cross-encoder rerank](../assets/retrieval.svg)
> ![混合检索：BM25 + 稠密 + RRF + 交叉编码器重排序](../assets/retrieval.svg)

Cuatro capas, escoge las que necesites.
> Cuatro niveles. Elige lo que necesitas.

1. **Sparse retrieval (BM25).**Rápido, preciso en las coincidencias exactas, terrible en la semántica, ejecuta un índice invertido, sub-10ms por consulta en millones de documentos, te da referencias de estatuto, códigos de producto, mensajes de error, entidades nombradas correctamente.
2. **Dense retrieval.**Encode la consulta y los documentos en vectores. búsqueda de vecino más cercano. Captura parafrases y similitud semántica. Se pierden coincidencias exactas de palabras clave que difieren por un carácter. 50-200 ms por consulta con FAISS o un vector DB.
3. **Fusion.**Combine las listas clasificadas de escasas y densas. La fusión de rango recíproco (RRF) es el estándar fácil porque ignora las puntuaciones en bruto (que viven en diferentes escalas) y solo utiliza posiciones de rango. La fusión ponderada es una opción cuando sabes que una señal domina para tu dominio.
4. **Cross-encoder rerank.**Tome el top-30 de la fusión. ejecuta un codificador cruzado (queriendo + documento juntos, anotando cada par). Mantenga el top-5. Los codificadores cruzados son más lentos por par que los bi-coders pero mucho más precisos.
> 1. **稀疏检索（BM25）。**快速、精确匹配准确、语义上糟糕──在倒排索引上运行──百万档次上每查询亚 10毫秒──正确处理法规引用、产品代码、错误消息、命名实体──
2. **稠密检索。**La información de la información de la base de datos de la base de datos de datos de la base de datos de datos de la base de datos de datos de la base de datos de datos de la base de datos de la base de datos de datos de la base de datos de datos de la base de datos de datos de la base de datos de datos de la base de datos de la base de datos de datos de la base de datos de datos de la base de datos de datos de la base de datos de datos de la base de datos de datos de la base de datos de datos de la base de datos de datos de la base de datos de datos de la base de datos de datos de datos de la base de datos de datos de la base de datos de datos de datos de la base de datos de datos de datos de la base de datos de datos de datos de la base de datos de datos de datos de datos de la base de datos de datos de datos de datos de la base de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos
3. **融合。**合并稀疏和密的排列列表──倒数排名融合(Reciprocal Rank Fusion, RRF) es una opción por defecto simple, ya que ignora los números primitivos (existen en diferentes dimensiones) solo utiliza la posición de clasificación── Cuando sabes que una señal en tu área domina, la fusión de potencia es una opción──
4. **交叉编码器重排序。**Desde la integración se obtiene el top-30──运行交叉编码器(查询 + 文档一起,对每对打分)──保留前-5──交叉编码器每对双编码器慢但准确得多──你只在前-30 上运行来摊销成本──

La recuperación de tres vías (BM25 + denso + espacio aprendido como SPLADE) supera a dos vías en los índices de referencia de 2026, pero necesita infraestructura para los índices de espacio aprendido.
> 三路检索 (BM25 + 密 + 学习稀疏如 SPLADE) en 2026 es mejor que las dos vías, pero necesita aprender la infraestructura de la índice de稀疏. Para la mayoría de los equipos, la reorganización de las dos vías es el mejor punto de equilibrio.

> **【拓展：大语言模型的工程实践】**Desde GPT hasta ChatGPT, el campo de NLP ha experimentado un cambio de paradigma de "cada tarea entrenar un modelo" a "un modelo resolver todas las tareas". En el proyecto real, la implementación de LLM necesita considerar los problemas de token 限制,延迟,成本, seguridad etc.

> **【拓展：RAG 与企业知识库】**检索增强生成(RAG) es la estructura más popular de las aplicaciones de IA de las empresas actuales: la consulta de usuarios primero se consulta los documentos relacionados, luego se vuelve a buscar los resultados como respuesta a la pregunta de LLM.

> **【拓展：NLP 的多语言挑战】**En todo el mundo hay más de 7000 idiomas, pero los estudios de PNL se centran principalmente en inglés y en una minoría de idiomas.


## Construye y realiza.

> **【中文解读】**Este capítulo a través del código de la implementación de algoritmos centrales de cero. Este método "desde cero" puede ayudar a entender el principio detrás del marco, no se encuentra en la caja negra cuando se encuentran problemas.

```figure
gx-hybrid-retrieval
```

## Construye el mismo

### Paso 1: BM25 desde cero
> Dos parámetros que hay que entender.`k1=1.5`控制词频和;更高 significa más peso de la palabra repetida.`b=0.75`控制长度归纳化;0 忽略文档长度,1 完全归纳化──默认值是罗伯茨森 原始论文中的推值,很少需要调整──

```python
import math
import re
from collections import Counter

TOKEN_RE = re.compile(r"[a-z0-9]+")


def tokenize(text):
    return TOKEN_RE.findall(text.lower())


class BM25:
    def __init__(self, corpus, k1=1.5, b=0.75):
        if not corpus:
            raise ValueError("corpus must not be empty")
        self.corpus = [tokenize(d) for d in corpus]
        self.k1 = k1
        self.b = b
        self.n_docs = len(self.corpus)
        self.avg_dl = sum(len(d) for d in self.corpus) / self.n_docs
        self.df = Counter()
        for doc in self.corpus:
            for term in set(doc):
                self.df[term] += 1

    def idf(self, term):
        n = self.df.get(term, 0)
        return math.log(1 + (self.n_docs - n + 0.5) / (n + 0.5))

    def score(self, query, doc_idx):
        q_tokens = tokenize(query)
        doc = self.corpus[doc_idx]
        dl = len(doc)
        freq = Counter(doc)
        score = 0.0
        for term in q_tokens:
            f = freq.get(term, 0)
            if f == 0:
                continue
            numerator = f * (self.k1 + 1)
            denominator = f + self.k1 * (1 - self.b + self.b * dl / self.avg_dl)
            score += self.idf(term) * numerator / denominator
        return score

    def rank(self, query, top_k=10):
        scored = [(self.score(query, i), i) for i in range(self.n_docs)]
        scored.sort(reverse=True)
        return scored[:top_k]
```

Dos parámetros que vale la pena conocer.`k1=1.5`control de saturación de la frecuencia de término; mayor significa más peso en la repetición de término. `b=0.75`El número 0 ignora la longitud del documento, el número 1 normaliza completamente.
> L2 归一化嵌入使点积等于余弦──`all-MiniLM-L6-v2`Es un idioma que se utiliza en la mayoría de los idiomas.`paraphrase-multilingual-MiniLM-L12-v2` La mayor tasa de precisión de uso `bge-large-en-v1.5`O `e5-large-v2`¿Qué es eso?

### Paso 2: Recuperación densa con un bi-encodor
> `k=60`常数来自原始RRF论文──更高的 `k`En la actualidad, el número de empresas en el sector de la industria de la información se ha reducido a un nivel de 1.`k`Usado por el grupo de la lista de los 60 que ya se publicó, muy poco necesita ser ajustado.

```python
from sentence_transformers import SentenceTransformer
import numpy as np


def build_dense_index(corpus, model_id="sentence-transformers/all-MiniLM-L6-v2"):
    encoder = SentenceTransformer(model_id)
    embeddings = encoder.encode(corpus, normalize_embeddings=True)
    return encoder, embeddings


def dense_search(encoder, embeddings, query, top_k=10):
    q_emb = encoder.encode([query], normalize_embeddings=True)
    sims = (embeddings @ q_emb.T).flatten()
    order = np.argsort(-sims)[:top_k]
    return [(float(sims[i]), int(i)) for i in order]
```

L2-normalizar las incorporaciones de modo que el producto punto es igual a cosino. `all-MiniLM-L6-v2`Es 384 dimensiones, rápido y lo suficientemente fuerte para la mayoría de los retiros en inglés.`paraphrase-multilingual-MiniLM-L12-v2`Para la máxima precisión,`bge-large-en-v1.5`o `e5-large-v2`¿ Qué ?
> Tres fases 组合──BM25 找到词汇匹配──密找到语义匹配──RRF 合并两个排名不需要分数校准──交叉编码器使用查询-文档对重新对 top-30 打分,捕获双编码器遗漏的细粒度相关性──保留 top-5──

### Paso 3: Fusión recíproca de rango
> # El signo significa #
|------|------|
| Recall@k | 存在正确文档的查询中，正确文档在 top-k 中的比例 |
| MRR（平均倒数排名） | 第一个相关文档的 1/rank 的平均值 |
| nDCG@k | 考虑相关性分级，而非仅仅是二元的 相关/不相关 |

```python
def reciprocal_rank_fusion(rankings, k=60):
    scores = {}
    for ranking in rankings:
        for rank, (_, doc_idx) in enumerate(ranking):
            scores[doc_idx] = scores.get(doc_idx, 0.0) + 1.0 / (k + rank + 1)
    fused = sorted(scores.items(), key=lambda x: x[1], reverse=True)
    return [(score, doc_idx) for doc_idx, score in fused]
```

El `k=60`La constante proviene del papel original de RRF.`k`Aporta la contribución de las diferencias de rango;`k`60 es el estándar publicado y rara vez necesita ajuste.
> ), en particular, en el caso de los RAG,**Recall@k**Si el pasaje correcto no se concentra en la búsqueda, el lector no puede responder.

### Paso 4: búsqueda híbrida + re-ranqueo
> 调试技巧:对于失败的查询,对稀疏和密排名──如果一个找到正确文档而另一个没有,你有词汇不匹配(修复:添加缺失的一半) 或语义歧义(修复:更好的嵌入或重排器)──

```python
from sentence_transformers import CrossEncoder

reranker = CrossEncoder("cross-encoder/ms-marco-MiniLM-L-6-v2")


def hybrid_search(query, bm25, encoder, dense_embeddings, corpus, top_k=5, pool_size=30, reranker=reranker):
    sparse_ranking = bm25.rank(query, top_k=pool_size)
    dense_ranking = dense_search(encoder, dense_embeddings, query, top_k=pool_size)
    fused = reciprocal_rank_fusion([sparse_ranking, dense_ranking])[:pool_size]

    pairs = [(query, corpus[doc_idx]) for _, doc_idx in fused]
    scores = reranker.predict(pairs)
    reranked = sorted(zip(scores, [doc_idx for _, doc_idx in fused]), reverse=True)
    return reranked[:top_k]
```

BM25 encuentra coincidencias léxicas. Denso encuentra coincidencias semánticas. RRF fusiona las dos clasificaciones sin necesidad de calibración de puntaje. Cross-encoder vuelve a marcar el top-30 usando pares de documentos de consulta juntos, lo que capta la relevancia de granos finos que el bi-encoder no logró. Mantenga el top-5.

### Paso 5: evaluación

| Metric | Meaning |
|--------|---------|
| Recall@k | Of queries where the correct document exists, how often is it in the top-k? |
| MRR (Mean Reciprocal Rank) | Average of 1/rank of first relevant document. |
| nDCG@k | Accounts for relevance gradations, not just binary relevant/not. |

Para RAG específicamente, **Recall@k**El lector no puede responder si el pasaje correcto no está en el conjunto recuperado.

Tip de desarreglamiento: para las consultas fallidas, diferir las clasificaciones escasas y densas. Si uno encuentra el documento correcto y el otro no, usted tiene un desajuste de vocabulario (corrección: agregar la mitad que falta) o una ambigüedad semántica (corrección: mejores embebedidos o un re-ranqueador).


> **【拓展：Prompt Engineering 与 LLM 应用】**La ingeniería rápida se ha convertido en la habilidad central de los ingenieros de PNL. Desde la Cero-Shot hasta la Few-Shot, desde la Cadena de Pensamiento hasta la Reacción, diferentes estrategias de sugerencias se aplican a diferentes escenarios.

## Usalo con el marco de ejecución

> **【中文解读】**Este capítulo muestra cómo utilizar un marco maduro (como PyTorch、HuggingFace, etc.) para aplicar rápidamente esta tecnología. En los proyectos reales, se realiza con prioridad el uso de un marco experimentado, se pueden reducir errores y mejorar la eficiencia de desarrollo.


La pila de 2026:
> 2026 años de tecnología:

| Scale | Stack |
|-------|-------|
| 1k-100k docs | In-memory BM25 + `all-MiniLM-L6-v2` embeddings + RRF. No separate DB. |
| 100k-10M docs | FAISS or pgvector for dense + Elasticsearch / OpenSearch for BM25. Run in parallel. |
| 10M+ docs | Qdrant / Weaviate / Vespa / Milvus with hybrid support. Cross-encoder rerank on top-30. |
| Best-quality frontier | Three-way (BM25 + dense + SPLADE) + ColBERT late-interaction reranking |
> La escala y la tecnología.
|------|--------|
| 1k-100k 文档 | 内存中 BM25 + `all-MiniLM-L6-v2` 嵌入 + RRF。无需独立数据库。 |
| 100k-10M 文档 | FAISS 或 pgvector 做稠密 + Elasticsearch / OpenSearch 做 BM25。并行运行。 |
| 10M+ 文档 | Qdrant / Weaviate / Vespa / Milvus 配混合支持。交叉编码器重排序 top-30。 |
| 最高质量前沿 | 三路（BM25 + 稠密 + SPLADE）+ ColBERT 后期交互重排序 |

Cualquiera que sea el presupuesto para la evaluación. Recall de recuperación de benchmark antes de comparar la exactitud de RAG de extremo a extremo. Un lector no puede arreglar lo que el recuperador perdió.
> Lo que sea que elija, debe evaluarse en el presupuesto.

### Las lecciones duramente aprendidas de la producción RAG 2026
> - **80% 的 RAG 失败追溯到摄取和分块，而不是模型。**El equipo pasó varias semanas intercambiando LLM y sugerencias, mientras que la investigación cada tres veces la consulta sobre la paz de regreso de errores de arriba abajo.
- **分块策略比分块大小更重要。**固定大小分割会破坏表格、代码和嵌套标题──句子感知是默认选择;语义或基于LLM的分块在技术文档和产品手册有回报──
- **父文档模式。**检索小的"子"块以获得精度──当同一节的多子块出现时,换进父块以保留下文──这持续提升答案质量而无需重新训练──
- **k_rerank=3 通常最优。**Cada aumento de un bloque que supere este número aumentará el token de la producción y el retraso de generación sin aumentar la calidad de la respuesta. Si k=8 sigue siendo k=3, bueno, se indica que el redireccionador no funciona bien.
- **HyDE / 查询扩展。**Desde la consulta se genera una hipótesis de respuesta, se inserta en ella, se recomienda la explicación de la diferencia entre el problema y el archivo largo.
- **上下文预算控制在 8K token 以下。**En este límite, la vida continua significa reorganizar el valor.
- **版本化一切。**提示、分块规则、嵌入模型、重排序器── cualquier desplazamiento silenciosamente dañará la respuesta质量──忠诚度、上下文精确率和未回答问题率 关控在用户看到之前阻止回归──
- **三路检索（BM25 + 稠密 + 学习稀疏如 SPLADE）在 2026 年基准上优于两路**, especialmente en la búsqueda de palabras y palabras mixtas.

- **80% of RAG failures trace to ingestion and chunking, not the model.**Los equipos pasan semanas intercambiando LLM y sintonizando las instrucciones mientras que la recuperación devuelve silenciosamente el contexto equivocado cada tercera consulta.
- **Chunking strategy matters more than chunk size.**El tamaño fijo se divide en tablas, código y encabezados anidados.
- **Parent-doc pattern.**Recoger pequeños trozos de "niño" para obtener precisión. Cuando aparecen varios niños de la misma sección de padres, intercambiar en el bloque de padres para preservar el contexto. Esto aumenta constantemente la calidad de las respuestas sin necesidad de reentrenamiento.
- **k_rerank=3 is usually optimal.**Cada pieza extra que añade el costo de token y la latencia de generación sin elevar la calidad de la respuesta. Si k=8 es aún mejor que k=3 para usted, el re-ranqueador está haciendo mal.
- **HyDE / query expansion.**Generar una respuesta hipotética de la consulta, incrustar, recuperar. Cubriendo la brecha de fraseo entre preguntas cortas y documentos largos.
- **Context budget under 8K tokens.**Los golpes constantes en ese límite significan que el umbral de re-ranqueador es demasiado suelto.
- **Version everything.**Las instrucciones, las reglas de fragmentación, el modelo de incorporación, el reranker. Cualquier deriva rompe silenciosamente la calidad de la respuesta. Las puertas de CI sobre fidelidad, precisión de contexto y tasa de preguntas sin respuesta bloquean las regresiones antes de que los usuarios las vean.
- **Three-way retrieval (BM25 + dense + learned-sparse like SPLADE) outperforms two-way**Envía cuando la infraestructura admita los índices SPLADE.
> Según las mediciones del sector de 2026, el diseño de la inspección correcta reduce el 70-90% de las apariencias. La mayoría de los RAG mejoran su rendimiento por una inspección mejor, y no por un modelo de reducción.

El diseño adecuado de recuperación reduce las alucinaciones en un 70-90% de acuerdo con las mediciones de la industria de 2026. La mayoría de los beneficios de rendimiento de RAG provienen de una mejor recuperación, no de ajuste fino del modelo.

> **【中文解读】**Este capítulo se centra en cómo se puede implementar el modelo como producto disponible. Desde el modelo original hasta el sistema de producción, se deben considerar múltiples dimensiones de optimización de rendimiento, tratamiento de errores, control, etc.


## Envíe el producto .

Salvo como`outputs/skill-retrieval-picker.md`¿Qué es esto ?
> 保存为                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           `outputs/skill-retrieval-picker.md`¿Qué es esto ?

```markdown
---
name: retrieval-picker
description: Pick a retrieval stack for a given corpus and query pattern.
version: 1.0.0
phase: 5
lesson: 14
tags: [nlp, retrieval, rag, search]
---

Given requirements (corpus size, query pattern, latency budget, quality bar, infra constraints), output:

1. Stack. BM25 only, dense only, hybrid (BM25 + dense + RRF), hybrid + cross-encoder rerank, or three-way (BM25 + dense + learned-sparse).
2. Dense encoder. Name the specific model. Match to language(s), domain, and context length.
3. Reranker. Name the specific cross-encoder model if used. Flag that rerank adds 30-100ms latency on top-30.
4. Evaluation plan. Recall@10 is the primary retriever metric. MRR for multi-answer. Baseline first, incremental improvements measured against it.

Refuse to recommend dense-only for corpora with named entities, error codes, or product SKUs unless the user has evidence dense handles exact matches. Refuse to skip reranking for high-stakes retrieval (legal, medical) where the final top-5 decides the user's answer.
```

> **【中文解读】**Practice los temas de fácil/medio/duro  3 difficulty to pass in  Recomenda al menos completar los temas de grado medio  Grado duro  para la preparación de la entrevista


## Los ejercicios.

1. **Easy.**Implementación `hybrid_search`En el caso de los datos de la serie de datos, el número de datos de los datos de la serie de datos de la serie de datos de la serie de datos de la serie de datos de la serie de datos de la serie de datos de la serie de datos de la serie de datos de la serie de datos de la serie de datos de la serie de datos de la serie de datos de la serie de datos de la serie de datos de la serie de datos de la serie de datos de la serie de datos de la serie de datos de la serie de datos de la serie de datos de la serie de datos de la serie de datos de datos de la serie de datos de datos de la serie de datos de datos de la serie de datos de datos de la serie de datos de datos de la serie de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos
2. **Medium.**Añadir el cálculo de MRR. Para cada consulta de prueba con un documento correcto conocido, encontrar el rango del documento correcto en BM25, clasificaciones densas e híbridas. Informar el MRR para cada uno.
3. **Hard.**Afinar un codificador denso en su dominio utilizando MultipleNegativesRankingLoss (Transformadores de Sentencia). Construir un conjunto de entrenamiento de 500 pares de documentos de consulta. Comparar el pre y post-afinado de recuerdos.
> 1. **简单。**En 500                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            `hybrid_search`△测试 20 个查询──比较 BM25-only、density-only 和混合的回忆@5──
2. **中等。**Añadir MRR  calcular. Para cada consulta de prueba de documentos correctos conocidos, encontrar los documentos correctos en la posición en BM25 密和混合排名.
3. **困难。**Utiliza MultipleNegativesRankingLoss (RankingLoss) (Sentences Transformers) en su área de trabajo.

> **【中文解读】**En el lenguaje de los términos "Lo que la gente dice" vs "Lo que realmente significa" se distingue entre el lenguaje diario y la definición técnica de significado.


## Términos clave .

| Term | What people say | What it actually means |
|------|-----------------|-----------------------|
| BM25 | Keyword search | Okapi BM25. Scores documents by term frequency, IDF, and length. |
| Dense retrieval | Vector search | Encode query + doc into vectors, find nearest neighbors. |
| Bi-encoder | Embedding model | Encodes query and doc independently. Fast at query time. |
| Cross-encoder | Reranker model | Encodes query + doc together. Slow but accurate. |
| RRF | Rank fusion | Combine two rankings by summing `1/(k + rank)`. |
| Recall@k | Retrieval metric | Fraction of queries where a relevant doc is in the top-k. |
> # Los términos # # que la gente dice # # tienen un significado real #
|------|-----------|---------|
| BM25 | 关键词搜索 | Okapi BM25。按词频、IDF 和长度为文档打分。 |
| 稠密检索 | 向量搜索 | 将查询 + 文档编码为向量，找最近邻。 |
| 双编码器 | 嵌入模型 | 独立编码查询和文档。查询时快速。 |
| 交叉编码器 | 重排序模型 | 一起编码查询 + 文档。慢但准确。 |
| RRF | 排名融合 | 通过对 `1/(k + rank)` 求和合并两个排名。 |
| Recall@k | 检索指标 | 相关文档在 top-k 中的查询比例。 |

> **【中文解读】**延伸阅读 proporciona un alto nivel de recursos para el aprendizaje profundo. Estos artículos y cursos son los referentes clásicos en el campo, adecuados para los lectores que necesitan una comprensión profunda.


## Más Leer más Leer más

- [Robertson and Zaragoza (2009). The Probabilistic Relevance Framework: BM25 and Beyond](https://www.staff.city.ac.uk/~sbrp622/papers/foundations_bm25_review.pdf) el tratamiento definitivo de BM25.
- [Karpukhin et al. (2020). Dense Passage Retrieval for Open-Domain QA](https://arxiv.org/abs/2004.04906) DPR, el bi-encodador canónico.
- [Formal et al. (2021). SPLADE: Sparse Lexical and Expansion Model](https://arxiv.org/abs/2107.05720) el retriever de espacios aprendidos que cierra la brecha con denso.
- [Cormack, Clarke, Büttcher (2009). Reciprocal Rank Fusion outperforms Condorcet and individual Rank Learning Methods](https://plg.uwaterloo.ca/~gvcormac/cormacksigir09-rrf.pdf) Papel de RRF.
- [Khattab and Zaharia (2020). ColBERT: Efficient and Effective Passage Search](https://arxiv.org/abs/2004.12832) Recuperación de interacción tardía.
> - [Robertson and Zaragoza (2009). The Probabilistic Relevance Framework: BM25 and Beyond](https://www.staff.city.ac.uk/~sbrp622/papers/foundations_bm25_review.pdf) 权威的BM25 处理──
- [Karpukhin et al. (2020). Dense Passage Retrieval for Open-Domain QA](https://arxiv.org/abs/2004.04906) DPR, clásico doble编码器。
- [Formal et al. (2021). SPLADE: Sparse Lexical and Expansion Model](https://arxiv.org/abs/2107.05720)                                                                                                                                                                                                                                                              
- [Cormack, Clarke, Büttcher (2009). Reciprocal Rank Fusion outperforms Condorcet and individual Rank Learning Methods](https://plg.uwaterloo.ca/~gvcormac/cormacksigir09-rrf.pdf) RRF 论文──
- [Khattab and Zaharia (2020). ColBERT: Efficient and Effective Passage Search](https://arxiv.org/abs/2004.12832) 后期交互检索──
