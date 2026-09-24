# Tema Modelado  LDA y BERTopic  Tema de construcción  LDA y BERTopic

> LDA: documentos son mezclas de temas, temas son distribuciones sobre palabras. BERTopic: documentos en grupo en el espacio de incorporación, grupos son temas.
> LDA: el documento es una mezcla de temas, el tema es la distribución de palabras.

> **【中文解读】**LDA utiliza el modelo de probabilidad para encontrar el tema, BERTopic utiliza BERT 嵌入──

**Type:** Learn | **类型:** 学习
**Languages:** Python | **语言:** Python
**Prerequisites:** Phase 5 · 02 (BoW + TF-IDF), Phase 5 · 03 (Word2Vec) | **前置知识:** Phase 5 · 02 (BoW + TF-IDF), Phase 5 · 03 (Word2Vec)
**Time:** ~45 minutes | **时间:** ~45 分钟


## El problema es la introducción del problema

Tienes 10.000 boletos de atención al cliente, 50.000 artículos de noticias o 200.000 tweets. Necesitas saber de qué se trata la colección sin leerla. No tienes etiquetadas categorías. Ni siquiera sabes cuántas categorías existen.
> Tienes 10.000 张客户支持工单,50.000 篇新闻文章或200.000 条推文── necesitas entender el tema de este conjunto sin leer── no tienes categorías marcadas── ni siquiera sabes cuántas categorías existen──

> **【中文解读】**La pregunta planteada en este capítulo es: ¿cómo entender y aplicar correctamente esta tecnología en la ingeniería real? Comprender el contexto de la cuestión ayuda a comprender los puntos clave de decisión del tipo de selección técnica. En los sistemas de IA reales, el tipo de selección técnica errónea suele ser más alto que el costo de error de la realización de detalles.


El modelo de temas responde sin supervisión. Dale un corpus, retorna un pequeño conjunto de temas coherentes y, para cada documento, una distribución sobre esos temas.
> Tema construcción en caso de no supervisión responder a esta pregunta.

El LDA (2003) trata cada documento como una mezcla de temas latentes y cada tema como una distribución sobre palabras. La inferencia es bayesiana. Todavía se envía en producción donde se necesitan asignaciones de temas de miembros mixtos y distribuciones de probabilidad explicables a nivel de palabras.
> 两个 algoritmos dominan la posición. LDA  2003  2003                                                                                                                                                                                                                                                       

BERTopic (2020) codifica documentos con BERT, reduce la dimensionalidad con UMAP, agrupa con HDBSCAN y extrae palabras de temas a través de TF-IDF basado en clase. Se gana en texto corto, redes sociales y cualquier cosa donde la similitud semántica importa más que la superposición de palabras. Un documento obtiene un tema, que es una limitación para el contenido de forma larga.
> BERTopic(2020) con el documento de codificación BERT, con UMAP 降维, con HDBSCAN 聚类, a través de la base de tipos TF-IDF 提取主题词──它在短文本、社交媒体和语义相似性比词重叠更重要的内容上胜出──一篇文档获得一个主题, esto es una limitación para el contenido de la historia.

Esta lección construye la intuición para ambos y los nombres que uno debe elegir para un cuerpo dado.
> Este curso se centra en la creación de una percepción directa y señala el material de texto que debe elegirse.

> **【中文解读】**Este capítulo presenta los conceptos y teorías básicos. La comprensión de estos conceptos es el prerrequisito de la realización posterior de la actividad, y también el conocimiento de los puntos de alta frecuencia de la entrevista y la práctica de la ingeniería.


## El concepto central.

![LDA mixture model vs BERTopic clustering](../assets/topic-modeling.svg)
> ![LDA 混合模型 vs BERTopic 聚类](../assets/topic-modeling.svg)

**LDA generative story.**Cada tema es una distribución sobre palabras. Cada documento es una mezcla de temas. Para generar una palabra en un documento, muestre un tema de la mezcla del documento, luego muestre una palabra de la distribución de ese tema. La inferencia invierte esto: dada las palabras observadas, inferir la distribución de temas por documento y la distribución de palabras por tema.
> **LDA 生成故事。**Cada tema es la distribución de palabras. Cada documento es la mezcla de temas. Debe generarse una palabra en el documento, tomarse una palabra de la mezcla de documentos, y luego tomar una palabra de la distribución de ese tema.

Fuente de salida de LDA clave:
> 关键 LDA 输出:

- `doc_topic`: matriz `(n_docs, n_topics)`, cada fila suma a 1 (mezcla de temas del documento).
- `topic_word`: matriz `(n_topics, vocab_size)`, cada fila suma a 1 (distribución de palabras del tema).
> - `doc_topic`:矩阵 `(n_docs, n_topics)`, por ciento y por ciento (documentation)
- `topic_word`:矩阵 `(n_topics, vocab_size)`, por línea total y por 1 ((subject's word distribution) ⋅

**BERTopic pipeline.**
> **BERTopic 流水线。**

1. Encodizar cada documento con un transformador de oraciones (por ejemplo, `all-MiniLM-L6-v2`Los vectores de 384 dimensiones.
2. Reducir la dimensionalidad con UMAP a ~5 dimensiones.
3. Cluster con HDBSCAN. basado en la densidad, produce grupos de tamaño variable y una etiqueta "outlier".
4. Para cada grupo, computa TF-IDF basado en la clase sobre los documentos del grupo para extraer las palabras principales.
> 1. Usó la palabra Transformer`all-MiniLM-L6-v2`)编码每篇文档──384 维向量──
2. Utiliza UMAP 降维到大约5维度.
3. Utilizando HDBSCAN 聚类── basado en la densidad, se producen cambios en la gran cantidad de 聚类 y "离群值" 标签──
4. Para cada grupo, se calcula en los archivos de la colección basándose en el TF-IDF para extraer las palabras de primer nivel.

La salida es un tema por documento (más una etiqueta de -1 fuera).
> 输出是每篇文档一个主题 (加上 -1 离群值标签) ⋅可选地, mediante el HDBSCAN de la probabilidad de obtener el derecho de miembro de la programación ⋅

> **【中文解读】**Este capítulo a través del código de la implementación de algoritmos centrales de cero. Este método "desde cero" puede ayudar a entender el principio detrás del marco, no se encuentra en la caja negra cuando se encuentran problemas.

> **【拓展：大语言模型的工程实践】**Desde GPT hasta ChatGPT, el campo de NLP ha experimentado un cambio de paradigma de "cada tarea entrenar un modelo" a "un modelo resolver todas las tareas". En el proyecto real, la implementación de LLM necesita considerar los problemas de token 限制,延迟,成本, seguridad etc.

> **【拓展：RAG 与企业知识库】**检索增强生成(RAG) es la estructura más popular de las aplicaciones de IA de las empresas actuales: la consulta de usuarios primero se consulta los documentos relacionados, luego se vuelve a buscar los resultados como respuesta a la pregunta de LLM.

> **【拓展：NLP 的多语言挑战】**En todo el mundo hay más de 7000 idiomas, pero los estudios de PNL se centran principalmente en inglés y en una minoría de idiomas.


## Construye y realiza.
```figure
topic-drift
```

## Construye el mismo

### Paso 1: LDA a través de scikit-learn
> Nota: se ha eliminado el uso de palabras de uso interrumpido, min_df 和 max_df 过罕见和无处不在的词, se utiliza CountVectorizer (no TfidfVectorizer), ya que LDA 期望原始计数──

```python
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.decomposition import LatentDirichletAllocation
import numpy as np


def fit_lda(documents, n_topics=5, max_features=1000):
    cv = CountVectorizer(
        max_features=max_features,
        stop_words="english",
        min_df=2,
        max_df=0.9,
    )
    X = cv.fit_transform(documents)
    lda = LatentDirichletAllocation(
        n_components=n_topics,
        random_state=42,
        max_iter=50,
        learning_method="online",
    )
    doc_topic = lda.fit_transform(X)
    feature_names = cv.get_feature_names_out()
    return lda, cv, doc_topic, feature_names


def print_top_words(lda, feature_names, n_top=10):
    for idx, topic in enumerate(lda.components_):
        top_idx = np.argsort(-topic)[:n_top]
        words = [feature_names[i] for i in top_idx]
        print(f"topic {idx}: {' '.join(words)}")
```

Nota: se han eliminado las palabras de parada, min_df y max_df filtran términos raros y ubicuos, CountVectorizer (no TfidfVectorizer) porque LDA espera contagens crudas.
> `Topic != -1`La información de la plataforma se ha desviado de la plataforma de BERTopic.`min_topic_size` control HDBSCAN BERTopic 库默认为 10──本例为课程的规模显然设为15──对于超过10,000 文档语料,增加到50或100──

### Paso 2: BERTopic (producción)
> 两种方法都输出主题词――问题是这些词是否连贯―― ¿Qué es lo que se dice en el texto?

```python
from bertopic import BERTopic

topic_model = BERTopic(
    embedding_model="sentence-transformers/all-MiniLM-L6-v2",
    min_topic_size=15,
    verbose=True,
)

topics, probs = topic_model.fit_transform(documents)
info = topic_model.get_topic_info()
print(info.head(20))
valid_topics = info[info["Topic"] != -1]["Topic"].tolist()
for topic_id in valid_topics[:5]:
    print(f"topic {topic_id}: {topic_model.get_topic(topic_id)[:10]}")
```

El filtro está encendido .`Topic != -1`Se elimina el cubo de pérdida de BERTopic (documentos que HDBSCAN no pudo agrupar). `min_topic_size`El tamaño mínimo de los clusters de HDBSCAN se controla; el estándar de biblioteca de BERTopic es 10.
> - **主题连贯度（c_v）。**结合滑动窗口上下文中顶级词对的 NPMI (en inglés: NPMI) 归一化点逐点互信息), se agrupará en el eje de la secuencia, a través de la similaridad de los cuerpos comparando estos eje de la secuencia.`gensim.models.CoherenceModel`配 `coherence="c_v"`¿Qué es eso?
- **主题多样性。**Todas las palabras en el top de la categoría son las únicas en la proporción.
- **定性检查。**¿Son ellos el nombre de una cosa real?

### Paso 3: evaluación

Ambos métodos producen palabras de tema. La pregunta es si esas palabras coinciden.

- **Topic coherence (c_v).**Combina NPMI (información mutua normalizada de punto) de pares de palabras principales en contextos de ventana deslizante, agrega las puntuaciones en vectores de tema y compara esos vectores a través de similitud cosínica.`gensim.models.CoherenceModel`con`coherence="c_v"`¿ Qué ?
- **Topic diversity.**Fracción de palabras únicas en todas las palabras principales de los temas.
- **Qualitative inspection.**¿Es verdad que el juicio humano es la última línea de defensa?


> **【拓展：Prompt Engineering 与 LLM 应用】**La ingeniería rápida se ha convertido en la habilidad central de los ingenieros de PNL. Desde la Cero-Shot hasta la Few-Shot, desde la Cadena de Pensamiento hasta la Reacción, diferentes estrategias de sugerencias se aplican a diferentes escenarios.

## ¿Cuándo elegir cuál

| Situation | Pick |
|-----------|------|
| Short text (tweets, reviews, headlines) | BERTopic |
| Long documents with topic mixtures | LDA |
| No GPU / limited compute | LDA or NMF |
| Need document-level multi-topic distributions | LDA |
| LLM integration for topic labeling | BERTopic (direct support) |
| Resource-constrained edge deployment | LDA |
| Max semantic coherence | BERTopic |

La mayor consideración práctica es la longitud del documento. las incorporaciones BERT truncan; LDA cuenta el trabajo en cualquier longitud. Para documentos más largos que el contexto del modelo de incorporación, ya sea pieza + agregado o use LDA.

> **【中文解读】**Este capítulo muestra cómo utilizar un marco maduro (como PyTorch、HuggingFace, etc.) para aplicar rápidamente esta tecnología. En los proyectos reales, se realiza con prioridad el uso de un marco experimentado, se pueden reducir errores y mejorar la eficiencia de desarrollo.


## Usalo con el marco de ejecución

La pila de 2026:
> 2026 años de tecnología:

- **BERTopic.**Default para texto corto y cualquier cosa donde la semántica importa.
- **`gensim.models.LdaModel`.**LDA clásico para producción, maduro, probado en batalla.
- **`sklearn.decomposition.LatentDirichletAllocation`.**LDA fácil para experimentos.
- **NMF.**Factorizamiento de matriz no negativo, alternativa rápida a la LDA, calidad comparable en texto corto.
- **Top2Vec.**Diseño similar al de BERTopic, comunidad más pequeña pero buena en algunos puntos de referencia.
- **FASTopic.**Más nuevo, más rápido que BERTopic en corpora muy grandes.
- **LLM-based labeling.**Ejecutar cualquier agrupación, luego pedir un modelo para nombrar cada agrupación.
> - **BERTopic。**短文本和语义重要的场景的默认选择──
- **`gensim.models.LdaModel`。**Clasificación de producción clásica LDA, maduro, cuya experiencia es larga.
- **`sklearn.decomposition.LatentDirichletAllocation`。**实验用简单 LDA──
- **NMF。**La velocidad de la LDA es de un tamaño de 1,00 m.
- **Top2Vec。**类似BERTopic的设计──社区较小但在某些基准上表现良好──
- **FASTopic。**更新,在超大语料上比BERTopic 快──
- **基于 LLM 的标注。**¿Qué es eso? ¿Qué es eso?

> **【中文解读】**Este capítulo se centra en cómo se puede implementar el modelo como producto disponible. Desde el modelo original hasta el sistema de producción, se deben considerar múltiples dimensiones de optimización de rendimiento, tratamiento de errores, control, etc.


## Envíe el producto .

Salvo como`outputs/skill-topic-picker.md`¿Qué es esto ?
> 保存为                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           `outputs/skill-topic-picker.md`¿Qué es esto ?

```markdown
---
name: topic-picker
description: Pick LDA or BERTopic for a corpus. Specify library, knobs, evaluation.
version: 1.0.0
phase: 5
lesson: 15
tags: [nlp, topic-modeling]
---

Given a corpus description (document count, avg length, domain, language, compute budget), output:

1. Algorithm. LDA / NMF / BERTopic / Top2Vec / FASTopic. One-sentence reason.
2. Configuration. Number of topics: `recommended = max(5, round(sqrt(n_docs)))`, clamped to 200 for corpora under 40,000 docs; permit >200 only when the corpus is genuinely large (>40k) and note the increased compute cost. `min_df` / `max_df` filters and embedding model for neural approaches also belong here.
3. Evaluation. Topic coherence (c_v) via `gensim.models.CoherenceModel`, topic diversity, and a 20-sample human read.
4. Failure mode to probe. For LDA, "junk topics" absorbing stopwords and frequent terms. For BERTopic, the -1 outlier cluster swallowing ambiguous documents.

Refuse BERTopic on documents longer than the embedding model's context window without a chunking strategy. Refuse LDA on very short text (tweets, reviews under 10 tokens) as coherence collapses. Flag any n_topics choice below 5 as likely wrong; flag >200 on corpora under 40k docs as likely over-splitting.
```

> **【中文解读】**Practice los temas de fácil/medio/duro  3 difficulty to pass in  Recomenda al menos completar los temas de grado medio  Grado duro  para la preparación de la entrevista


## Los ejercicios.

1. **Easy.**Aplica LDA con 5 temas en el conjunto de datos de 20 Newsgroups. Imprima las 10 palabras principales por tema. Etiqueta cada tema a mano. ¿El algoritmo encontró las categorías reales?
2. **Medium.**En la actualidad, el grupo de noticias de la región de LDA es el más importante de los grupos de noticias de la región de LDA.
3. **Hard.**Compute la coherencia c_v tanto para LDA como para BERTopic en su corpus. ejecuta cada uno con 5, 10, 20, 50 temas. Conserva la coherencia frente al conteo de temas. Reporte qué método es más estable en los conteos de temas.
> 1. **简单。**En 20 grupos de noticias, los datos se componen con 5 temas que se ajustan a la LDA. ¿Imprimir las 10 mejores palabras de cada tema? ¿El algoritmo ha encontrado una clase real?
2. **中等。**En el mismo 20 Newsgroups 子集上适合BERTopic── Compare encontrar el número de temas, las palabras de primer nivel y la conectividad de la determinación con la comparación de LDA── ¿Cuál es la clase más claramente presentada?
3. **困难。**En tu lenguaje, calcular la continuidad de los LDA y BERTopic.

> **【中文解读】**En el lenguaje de los términos "Lo que la gente dice" vs "Lo que realmente significa" se distingue entre el lenguaje diario y la definición técnica de significado.


## Términos clave .

| Term | What people say | What it actually means |
|------|-----------------|-----------------------|
| Topic | A thing the corpus is about | A probability distribution over words (LDA) or a cluster of similar documents (BERTopic). |
| Mixed membership | Doc is multiple topics | LDA assigns each document a distribution over all topics. |
| UMAP | Dimensionality reduction | Manifold learning that preserves local structure; used in BERTopic. |
| HDBSCAN | Density clustering | Finds variable-size clusters; produces "noise" label (-1) for outliers. |
| c_v coherence | Topic quality metric | Average pointwise mutual information of top topic words within sliding windows. |
> # Los términos # # que la gente dice # # tienen un significado real #
|------|-----------|---------|
| 主题 | 语料关于的东西 | 词的概率分布（LDA）或相似文档的聚类（BERTopic）。 |
| 混合成员资格 | 文档是多个主题 | LDA 为每篇文档分配所有主题上的分布。 |
| UMAP | 降维 | 保留局部结构的流形学习；BERTopic 中使用。 |
| HDBSCAN | 密度聚类 | 找到变大小聚类；为离群值产生 "噪声" 标签（-1）。 |
| c_v 连贯度 | 主题质量指标 | 滑动窗口内顶级主题词的平均逐点互信息。 |

> **【中文解读】**延伸阅读 proporciona un alto nivel de recursos para el aprendizaje profundo. Estos artículos y cursos son los referentes clásicos en el campo, adecuados para los lectores que necesitan una comprensión profunda.


## Más Leer más Leer más

- [Blei, Ng, Jordan (2003). Latent Dirichlet Allocation](https://www.jmlr.org/papers/volume3/blei03a/blei03a.pdf) el documento de la LDA.
- [Grootendorst (2022). BERTopic: Neural topic modeling with a class-based TF-IDF procedure](https://arxiv.org/abs/2203.05794) el periódico BERTopic.
- [Röder, Both, Hinneburg (2015). Exploring the Space of Topic Coherence Measures](https://svn.aksw.org/papers/2015/WSDM_Topic_Evaluation/public.pdf) el periódico que introdujo a C_V y amigos.
- [BERTopic documentation](https://maartengr.github.io/BERTopic/) la referencia de producción.
> - [Blei, Ng, Jordan (2003). Latent Dirichlet Allocation](https://www.jmlr.org/papers/volume3/blei03a/blei03a.pdf) LDA 论文──
- [Grootendorst (2022). BERTopic: Neural topic modeling with a class-based TF-IDF procedure](https://arxiv.org/abs/2203.05794) BERTópico 论文──
- [Röder, Both, Hinneburg (2015). Exploring the Space of Topic Coherence Measures](https://svn.aksw.org/papers/2015/WSDM_Topic_Evaluation/public.pdf) 引入 c_v 及相关标标的论文──
- [BERTopic documentation](https://maartengr.github.io/BERTopic/) 生产参考──优秀示例──
