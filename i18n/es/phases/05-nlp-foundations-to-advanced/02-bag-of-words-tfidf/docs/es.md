# Bolsa de palabras, TF-IDF, y la representación de texto.

> TF-IDF todavía supera las incorporaciones en tareas bien definidas en 2026.
> En el marco de una misión definida, el FDI-TF hasta 2026 todavía ha logrado integrarse.

> **【中文解读】**词袋模型忽略词序只统计词频,TF-IDF 通过惩罚常见词突出关键词―― es el método de expresión más básico del texto―

**Type:** Build | **类型:** 动手
**Languages:** Python | **语言:** Python
**Prerequisites:** Phase 5 · 01 (Text Processing), Phase 2 · 02 (Linear Regression from Scratch) | **前置知识:** Phase 5 · 01（文本处理），Phase 2 · 02（线性回归从零实现）
**Time:** ~75 minutes | **时间:** ~75 分钟

## Objetivos de aprendizaje

- Construir representaciones de bolsas de palabras y TF-IDF desde cero
  Desde零构建词袋模型 y TF-IDF indicar
- Comprender vectores escasos, frecuencia de términos y frecuencia inversa de documentos
  Comprender la frecuencia de la expresión y la frecuencia de la traducción
- Utilice el CountVectorizer y el TfidfVectorizer de scikit-learn en la producción
  En la producción se utiliza un calculador de vectorizador y un calculador de vectorizador de tfidf
- Conocer cuándo TF-IDF gana sobre las incorporaciones y cuándo falla
  ¿Cuándo ha ganado, cuándo ha fracasado?

## El problema es la introducción del problema

El modelo necesita números.

> El modelo necesita números.

Cada línea de NLP tiene que responder a la misma pregunta. ¿Cómo convertir un flujo de tokens de longitud variable en un vector de tamaño fijo que un clasificador puede consumir? La primera respuesta que el campo aterrizó fue la más tonta que funciona. Cuente las palabras. Haga un vector.

> Cada línea de flujo de agua de la PNL debe responder a la misma pregunta: ¿cómo se va a transformar el tamaño de los tokens en un tamaño fijo de velocidad, para que los clasificadores puedan consumir? La primera respuesta dada en este campo es el método más utilizado.

Ese vector ha llevado más NLP de producción que cualquier modelo de incorporación. Filtros de spam, clasificadores de temas, detección de anomalías de registro, clasificación de búsqueda (antes de BM25), la primera ola de análisis de sentimientos, la primera década de benchmarks académicos de PNL. 2026 los profesionales todavía lo alcanzan primero en tareas de clasificación estrechas. Es rápido, interpretable y a menudo indistinguible de un modelo de incorporación de parámetros de 400M en tareas donde la presencia de palabras es lo que importa.

> Esta producción de NLP  aplicación de vector lleva más que cualquier modelo de emplazamiento 垃圾邮件过器, 类器, 日志异常检查, 搜索排序 (BM25 出现之前) 首波情感分析,学术 NLP 基准测试的第一十年. En 2026 los profesionales en tareas de clasificación estrecha todavía lo utilizarán primero.

Esta lección construye una bolsa de palabras, luego TF-IDF, desde cero. Luego muestra a scikit-learn haciendo lo mismo en tres líneas. Luego nombra el modo de fracaso que te hace llegar a las incorporaciones.

> Este curso se inicia en el modelo de la bolsa de palabras de construcción, luego se construye el TF-IDF, luego se muestra cómo aprender con el código de código de forma rápida.

## El concepto central.

> **【中文解读】**Este capítulo presenta los conceptos y teorías básicos. La comprensión de estos conceptos es el prerrequisito de la realización posterior de la actividad, y también el conocimiento de los puntos de alta frecuencia de la entrevista y la práctica de la ingeniería.

**Bag of Words (BoW)**Para cada documento, cuenta cuántas veces aparece cada palabra del vocabulario.`i`es el conteo de palabras `i`¿ Qué ?

> **词袋模型（Bag of Words, BoW）**抛弃顺序──对每文档,统计每词表词出现的次数──向量长度是词表大小──位置 `i`Sí es palabra`i`El número de personas.

**TF-IDF**Una palabra que aparece en cada documento es poco informativa, así que redujelo. Una palabra rara en todo el corpus pero frecuente en un solo documento es señal, así que redujelo.

> **TF-IDF**Para BoW, el peso de la palabra en cada documento no tiene una cantidad de información, por lo que reduce su peso.

```
TF-IDF(w, d) = TF(w, d) * IDF(w)
             = count(w in d) / |d| * log(N / df(w))
```

¿ Dónde ?`TF`es la frecuencia de los términos en el documento, `df`es la frecuencia del documento (cuántos documentos contienen la palabra), `N`Es el total de documentos.`log`mantiene el peso limitado para las palabras omnipresentes.

> Entre ellos `TF`Es un lenguaje de la literatura.`df`Es el número de documentos que contienen este término.`N`Es el número total de archivos.`log`El derecho de mantener el peso de las palabras de la inexistencia tiene límites.

Propiedad clave: ambos producen vectores escasos con ejes interpretables. Puedes mirar los pesos de un clasificador entrenado y leer qué palabras empujan un documento hacia cada clase. No puedes hacer esto con una incorporación BERT de 768 dimensiones.

> Casilidad clave: ambos producen una rara tendencia de eje explicable. Puedes ver el peso de un buen clasificador entrenado, leer qué palabras llevarán el archivo a cada clase.

> **【拓展：大语言模型的工程实践】**Desde GPT hasta ChatGPT, el campo de NLP ha experimentado un cambio de paradigma de "cada tarea entrenar un modelo" a "un modelo resolver todas las tareas". En el proyecto real, la implementación de LLM necesita considerar los problemas de token 限制,延迟,成本, seguridad etc.

> **【拓展：RAG 与企业知识库】**检索增强生成(RAG) es la estructura más popular de las aplicaciones de IA de las empresas actuales: la consulta de usuarios primero se consulta los documentos relacionados, luego se vuelve a buscar los resultados como respuesta a la pregunta de LLM.

> **【拓展：NLP 的多语言挑战】**En todo el mundo hay más de 7000 idiomas, pero los estudios de PNL se centran principalmente en inglés y en una minoría de idiomas.

## Construye y realiza.

> **【中文解读】**Este capítulo a través del código de la implementación de algoritmos centrales de cero. Este método "desde cero" puede ayudar a entender el principio detrás del marco, no se encuentra en la caja negra cuando se encuentran problemas.
```figure
bow-tfidf
```

## Construye el mismo

### Paso 1: construir el vocabulario

```python
def build_vocab(docs):
    vocab = {}
    for doc in docs:
        for token in doc:
            if token not in vocab:
                vocab[token] = len(vocab)
    return vocab
```

Entrada: lista de documentos tokenizados (se hará cualquier tokenizer de nivel de palabra; el `code/main.py`En esta lección se utiliza una variante simplificada en letras pequeñas).`{word: index}`Dict. orden de inserción estable significa que el índice de palabras 0 es la primera palabra que se ve en el primer documento.

> 输入:token 化的文档列表( cualquier palabra clase分词器都可以;本课的 `code/main.py`Uso simplificado ign略大小写变体) ⋅输出:`{word: index}`字典──稳定的插入顺序 significa 字符索引 0 es el primer palabra que se ve en el primer archivo──惯例各不相同;scikit-learn 按字母排序──

### Paso 2: bolsa de palabras

```python
def bag_of_words(docs, vocab):
    matrix = [[0] * len(vocab) for _ in docs]
    for i, doc in enumerate(docs):
        for token in doc:
            if token in vocab:
                matrix[i][vocab[token]] += 1
    return matrix
```

```python
>>> docs = [["cat", "sat", "on", "mat"], ["cat", "cat", "ran"]]
>>> vocab = build_vocab(docs)
>>> bag_of_words(docs, vocab)
[[1, 1, 1, 1, 0], [2, 0, 0, 0, 1]]
```

Las filas son documentos, las columnas son índices de vocabulario.`[i][j]`es "cuántas veces palabra `j`aparece en el documento `i`." Doc 1 tiene `cat`Dos veces porque lo hizo.`ran`cero veces porque no lo hizo.

> 行是文档──列是词表索引──条目 `[i][j]`Es un " palabra "`j`En el archivo`i`En el medio aparecieron muchas veces.`cat`, porque realmente apareció dos veces.`ran`, porque no apareció.

### Paso 3: frecuencia de los términos y frecuencia de los documentos

```python
import math


def term_frequency(doc_bow, doc_length):
    return [c / doc_length if doc_length else 0 for c in doc_bow]


def document_frequency(bow_matrix):
    df = [0] * len(bow_matrix[0])
    for row in bow_matrix:
        for j, count in enumerate(row):
            if count > 0:
                df[j] += 1
    return df


def inverse_document_frequency(df, n_docs):
    return [math.log((n_docs + 1) / (d + 1)) + 1 for d in df]
```

Dos trucos de suavizamiento que vale la pena nombrar.`(n+1)/(d+1)`evita`log(x/0)`- El trasero .`+1`El sistema de instrucción de base de datos de base de datos de base de datos de base de datos de base de datos de base de datos de base de datos de base de datos de base de datos de base de datos de base de datos de base de datos de base de datos de base de datos de base de datos de base de datos de base de datos de base de datos de base de datos de base de datos de base de datos de base de datos de base de datos de base de datos de base de datos de base de datos de base de datos de base de datos de base de datos de base de datos de base de datos de base de datos de base de datos de base de datos de base de datos de base de datos de base de datos de base de datos de base de datos de base de datos de base de datos de base de datos de base de datos de base de datos de base de datos de base de datos de base de datos de base de datos de base de datos de base de datos de base de datos de base de datos de base de datos de base de datos de base de datos de base de datos de base de datos de base de datos de base de datos de base de datos de base de datos de base de datos de base de datos de base de datos de base de datos de base de base de datos de base de datos de base de datos de base de base de datos de datos de base de base de datos de base de datos de base de base de datos de base de datos de base de datos de base de datos de base de datos de base de datos de base de datos de base de base de datos de datos de base de base de datos de base de base de datos de datos de base de base de datos de base de base de datos de base de base de datos de base de base de datos de datos de base de base de datos de base de base de datos de base de base de datos de base de base de datos de base de base de base de datos de base de base de datos de base de base de base de base de base de base de base de base de base de base de base de base de base de base de base de base de base de base de base de base de base de base de base de base de base de base de base de base de base de base de base de base de base de base de base de base de base de base de base de base de base de base de base de base de base de base de base de base de`log(N/df)`Ambos funcionan, la versión suave es más amigable.

> Dos técnicas de planeación que vale la pena notar.`(n+1)/(d+1)` evitar `log(x/0)`ᅳ尾部的 ᅳ`+1` asegurar que la IDF                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                       `log(N/df)`两种都有效;平滑版本更友好

### Paso 4: TF-IDF

```python
def tfidf(bow_matrix):
    n_docs = len(bow_matrix)
    df = document_frequency(bow_matrix)
    idf = inverse_document_frequency(df, n_docs)
    out = []
    for row in bow_matrix:
        length = sum(row)
        tf = term_frequency(row, length)
        out.append([tf_j * idf_j for tf_j, idf_j in zip(tf, idf)])
    return out
```

```python
>>> docs = [
...     ["the", "cat", "sat"],
...     ["the", "dog", "sat"],
...     ["the", "cat", "ran"],
... ]
>>> vocab = build_vocab(docs)
>>> bow = bag_of_words(docs, vocab)
>>> tfidf(bow)
```

Tres documentos, cinco palabras vocabularias (`the`¿ Qué ?`cat`¿ Qué ?`sat`¿ Qué ?`dog`¿ Qué ?`ran`¿ Qué es esto ?`the`aparece en los tres, así que su IDF es baja. `dog`Los vectores son escasos (la mayoría de las entradas son pequeñas) y las palabras discriminatorias pop.

> Tres documentos, cinco palabras`the`¿Qué es esto?`cat`¿Qué es esto?`sat`¿Qué es esto?`dog`¿Qué es esto?`ran`)。`the`En todos los tres archivos aparecen, así que su IDF es muy baja.`dog`Sólo aparece en un archivo, por lo que su IDF 很高──向量是稀疏的 (la mayoría de los artículos son pequeños),区分性强的词突出──

### Paso 5: Normaliza las filas L2

```python
def l2_normalize(matrix):
    out = []
    for row in matrix:
        norm = math.sqrt(sum(x * x for x in row))
        out.append([x / norm if norm else 0 for x in row])
    return out
```

> **【中文解读】**Este capítulo muestra cómo utilizar un marco maduro (como PyTorch、HuggingFace, etc.) para aplicar rápidamente esta tecnología. En los proyectos reales, se realiza con prioridad el uso de un marco experimentado, se pueden reducir errores y mejorar la eficiencia de desarrollo.

Sin normalización, un documento más largo obtiene un vector más grande y domina las puntuaciones de similitud. La normalización L2 pone cada documento en la hiperesfera unitaria. La similitud cosínica entre filas es ahora solo un producto de puntos.

>  sin regeneración, los archivos más largos obtendrán un mayor volumen y dominarán la similaridad de la puntuación. L2  Regeneración colocará cada archivo en unidad sobre la superficie de la bola.

> **【拓展：Prompt Engineering 与 LLM 应用】**La ingeniería rápida se ha convertido en la habilidad central de los ingenieros de PNL. Desde la Cero-Shot hasta la Few-Shot, desde la Cadena de Pensamiento hasta la Reacción, diferentes estrategias de sugerencias se aplican a diferentes escenarios.

## Usalo con el marco de ejecución

Scikit-Learn envía la versión de producción.

> Scikit-learn  proporcionó una versión de producción.

```python
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer

docs = ["the cat sat on the mat", "the dog sat on the mat", "the cat ran"]

bow_vectorizer = CountVectorizer()
bow = bow_vectorizer.fit_transform(docs)
print(bow_vectorizer.get_feature_names_out())
print(bow.toarray())

tfidf_vectorizer = TfidfVectorizer()
tfidf = tfidf_vectorizer.fit_transform(docs)
print(tfidf.toarray().round(3))
```

`CountVectorizer`hace tokenización, vocabulario y BoW en una sola llamada. `TfidfVectorizer`Para 100k documentos, la versión densa no encaja en la memoria; permanezca escasa hasta que el clasificador exija densa.

> `CountVectorizer`En una ocasión调用中完成分词、构建词表和 BoW。`TfidfVectorizer`增加 IDF 加权和 L2 归结化──都回归稀疏矩阵──对10万篇文档,密集版本放不进内存;在分类器要求密集之前保持稀疏──

Los nudos que cambian todo:

>  modificar todo   modificar todo   modificar todo   modificar todo  modificar todo  modificar todo  modificar todo  modificar todo  modificar todo  modificar todo  modificar todo  modificar todo  modificar todo  modificar todo  modificar todo  modificar todo  modificar todo  modificar todo  modificar todo  modificar todo  modificar todo  modificar todo  modificar todo  modificar todo  modificar todo  modificar todo  modificar todo  modificar todo  modificar todo  modificar todo  modificar todo  modificar todo  modificar todo  modificar todo  modificar todo  modificar todo  modificar todo  modificar todo  modificar todo  modificar  modificar todo  modificar  modificar todo  modificar  modificar  modificar  modificar  modificar  modificar  modificar  modificar  modificar  modificar  modificar  modificar  modificar  modificar  modificar  modificar  modificar  modificar  modificar   modificar  modificar   modificar   modificar   modificar    modificar   modificar    modificar     modificar                                                                                                                                                                                                                                                                                                                        

| Arg | Effect | 参数 | 效果 |
|-----|--------|------|------|
| `ngram_range=(1, 2)` | Include bigrams. Usually boosts classification. | `ngram_range=(1, 2)` | 包含二元组。通常提升分类效果。 |
| `min_df=2` | Drop words in fewer than 2 docs. Trims vocabulary on noisy data. | `min_df=2` | 丢弃出现在少于 2 个文档中的词。在噪声数据上修剪词表。 |
| `max_df=0.95` | Drop words in more than 95% of docs. Approximates stopword removal without a hardcoded list. | `max_df=0.95` | 丢弃出现在超过 95% 文档中的词。近似停用词去除，无需硬编码列表。 |
| `stop_words="english"` | scikit-learn's builtin stopword list. Task-dependent — sentiment analysis should *not* drop negations. | `stop_words="english"` | scikit-learn 内置停用词列表。因任务而异——情感分析不应去除否定词。 |
| `sublinear_tf=True` | Use `1 + log(tf)` instead of raw `tf`. Helps when a term repeats many times in one doc. | `sublinear_tf=True` | 使用 `1 + log(tf)` 代替原始 `tf`。当一个词在一个文档中重复多次时有帮助。 |

### Cuando TF-IDF todavía gane (a partir de 2026)

- La detección de spam, etiquetado de temas, marcado de anomalías de registro.
  垃圾邮件检测、主题标签、日志异常标签──la existencia o no de un término es clave; la diferencia en el significado es importante.
- Los regímenes de datos bajos (cientos de ejemplos etiquetados) TF-IDF más regresión logística no tienen coste previo a la formación.
  低数据场景(cientos ejemplos de marcas) ――TF-IDF 加逻辑回归没有预训成本──
- TF-IDF más un modelo lineal responde en microsecondas.
  任何延迟敏感场景──TF-IDF 加线性模型的响应时间是微秒级──通过变压器 嵌入一个文档需要10-100毫秒──
- Los sistemas que deben explicar sus predicciones, inspeccionar los coeficientes del clasificador, las palabras positivas más altas son la razón.
  需要解释预测结果的系统──检查分类器的系数──排名最高正权重词就是原因──

### Cuando el TF-IDF falla

El fracaso de la ceguera semántica.

> 语义盲点──考虑以下两个文档:

- "La película no fue buena en absoluto".
- "La película fue excelente".

Uno es una revisión negativa, otro es positivo, su superposición entre TF e IDF es exactamente`{the, movie, was}`Un clasificador de bolsas de palabras tiene que memorizar esa palabra .`not`cerca .`good`Puede aprender esto con suficiente datos, pero nunca tan graciosamente como un modelo que entiende la sintaxis.

> Una es la evaluación negativa, otra es la evaluación positiva.`{the, movie, was}`词袋分类器 debe recordar `good` cerca `not`Se puede aprender esto en datos suficientes, pero nunca será tan bonito como un modelo de comprensión de la gramática.

El otro fracaso: palabras fuera del vocabulario en la inferencia.`Zoomer-approved`Si el token no apareció en el entrenamiento, las incorporaciones de subpalabra (lección 04) manejan esto.

> 另一个失败:推理时的词表外(Fuera del vocabulario, OOV)词──在 IMDb 评论上训练的 BoW 模型不知道如何处理 `Zoomer-approved`, Si este token no aparece en el entrenamiento.

### El valor de la carga de carga de la aeronave se calcula en el punto de partida 1 del anexo I.

El estándar pragmático para 2026 para la clasificación de datos medios: utilizar pesas TF-IDF como atención sobre las incorporaciones de palabras.

> Programa de referencia de uso práctico de la información de la clase media 2026: uso de TF-IDF 权重作为词嵌的注意力──

```python
def tfidf_weighted_embedding(doc, tfidf_scores, embedding_table, dim):
    vec = [0.0] * dim
    total_weight = 0.0
    for token in doc:
        if token not in embedding_table or token not in tfidf_scores:
            continue
        weight = tfidf_scores[token]
        emb = embedding_table[token]
        for i in range(dim):
            vec[i] += weight * emb[i]
        total_weight += weight
    if total_weight == 0:
        return vec
    return [v / total_weight for v in vec]
```

> **【中文解读】**Este capítulo se centra en cómo se puede implementar el modelo como producto disponible. Desde el modelo original hasta el sistema de producción, se deben considerar múltiples dimensiones de optimización de rendimiento, tratamiento de errores, control, etc.

Obtienes capacidad semántica de las incorporaciones, y énfasis en palabras raras de TF-IDF. El clasificador se forma en el vector combinado. Esto supera por sí solo para la clasificación de sentimiento, tema y intención por debajo de unos 50k ejemplos etiquetados.

> Se obtiene la capacidad de semanía de las incorporaciones, de las TF-IDF  obtiene rarísima palabra enfatizada ∙∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙  ∙     ∙                                                                                                                                                                                                                                                                

## Envíe el producto .

Salvo como`outputs/prompt-vectorization-picker.md`¿Qué es esto ?

```markdown
---
name: vectorization-picker
description: Given a text-classification task, recommend BoW, TF-IDF, embeddings, or a hybrid.
phase: 5
lesson: 02
---

You recommend a text-vectorization strategy. Given a task description, output:

1. Representation (BoW, TF-IDF, transformer embeddings, or a hybrid). Explain why in one sentence.
2. Specific vectorizer configuration. Name the library. Quote the arguments (`ngram_range`, `min_df`, `max_df`, `sublinear_tf`, `stop_words`).
3. One failure mode to test before shipping.

Refuse to recommend embeddings when the user has under 500 labeled examples unless they show evidence of semantic failure in a TF-IDF baseline. Refuse to remove stopwords for sentiment analysis (negations carry signal). Flag class imbalance as needing more than a vectorizer change.

Example input: "Classifying 30k customer support tickets into 12 categories. Most tickets are 2-3 sentences. English only. Need explainability for audit logs."

Example output:

- Representation: TF-IDF. 30k examples is not small; explainability requirement rules out dense embeddings.
- Config: `TfidfVectorizer(ngram_range=(1, 2), min_df=3, max_df=0.95, sublinear_tf=True, stop_words=None)`. Keep stopwords because category keywords sometimes are stopwords ("not working" vs "working").
- Failure to test: verify `min_df=3` does not drop rare category keywords. Run `get_feature_names_out` filtered by class and eyeball.
```

## Los ejercicios.

1. **Easy.**Implementación `cosine_similarity(doc_vec_a, doc_vec_b)`Verificar que los documentos idénticos obtienen un puntaje de 1.0 y los documentos de vocabulario desarticulado un puntaje de 0.0.
   **简单。**En L2                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           `cosine_similarity(doc_vec_a, doc_vec_b)` Prueba de que el mismo documento tiene un puntaje de 1.0, palabra表完全不相交的文档的分分为0.0♦
2. **Medium.**Añadir`n-gram`apoyo a `bag_of_words`Parámetro .`n`produce recuentos sobre `n`- Prueba eso.`n=2`En el`["the", "cat", "sat"]`produce un gran número de números de gramos para`["the cat", "cat sat"]`¿ Qué ?
   **中等。**Por lo tanto ,`bag_of_words`添加                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           `n-gram`支持──参数 `n` producirse `n`-gramas de cuentas.`n=2`时    tiempo`["the", "cat", "sat"]`产生二元组 `["the cat", "cat sat"]`El número de personas.
3. **Hard.**Construir el híbrido de incorporación ponderada TF-IDF arriba utilizando vectores GloVe 100d (descargar una vez, caché). Comparar la precisión de clasificación con la TF-IDF y las incorporaciones medias comunes en el conjunto de datos de 20 Newsgroups.
   **困难。**Utiliza GloVe 100 维向量(download一次并缓存) Construir la mencionada TF-IDF加权嵌混合方案── en 20 Newsgroups datos en conjunto comparación de la tasa de precisión, en comparación con la pura TF-IDF y la pura media de valor en la pila de emplazamiento── informe que está en donde se ha ganado──

> **【中文解读】**Practice los temas de fácil/medio/duro  3 difficulty to pass in  Recomenda al menos completar los temas de grado medio  Grado duro  para la preparación de la entrevista

## Términos clave .

| Term | What people say | What it actually means | 术语 | 人们常说的 | 实际含义 |
|------|-----------------|-----------------------|------|-----------|---------|
| BoW | Word frequency vector | Counts of vocabulary words in one document. Throws away order. | BoW（词袋模型） | 词频向量 | 一个文档中词表词的计数。抛弃顺序。 |
| TF | Term frequency | Count of a word in a document, optionally normalized by document length. | TF（词频） | 词频 | 一个词在文档中的计数，可选按文档长度归一化。 |
| DF | Document frequency | Count of documents containing the word at least once. | DF（文档频率） | 文档频率 | 至少包含该词一次的文档计数。 |
| IDF | Inverse document frequency | `log(N / df)` smoothed. Downweights words that appear everywhere. | IDF（逆文档频率） | 逆文档频率 | 经平滑的 `log(N / df)`。降低到处出现的词的权重。 |
| Sparse vector | Mostly zeros | Vocabulary is typically 10k-100k words; most are absent from any given document. | 稀疏向量 | 大部分为零 | 词表通常有 1 万到 10 万个词；大多数在任何给定文档中都不出现。 |
| Cosine similarity | Vector angle | Dot product of L2-normalized vectors. 1 is identical, 0 is orthogonal. | 余弦相似度 | 向量夹角 | L2 归一化向量的点积。1 表示相同，0 表示正交。 |

> **【中文解读】**En el lenguaje de los términos "Lo que la gente dice" vs "Lo que realmente significa" se distingue entre el lenguaje diario y la definición técnica de significado.

## Más Leer más Leer más

- [scikit-learn — feature extraction from text](https://scikit-learn.org/stable/modules/feature_extraction.html#text-feature-extraction) la referencia canónica de la API, más notas en cada botón. / 权威 API 参考,以及每个参数的说明──
- [Salton, G., & Buckley, C. (1988). Term-weighting approaches in automatic text retrieval](https://www.sciencedirect.com/science/article/pii/0306457388900210) el documento que hizo del TF-IDF el default durante una década. / 使 TF-IDF 成为十年默认方案的论文──
- ["Why TF-IDF Still Beats Embeddings" — Ashfaque Thonikkadavan (Medium)](https://medium.com/@cmtwskb/why-tf-idf-still-beats-embeddings-ad85c123e1b2) 2026 tomar cuando el viejo método gana y por qué. / 2026 年对旧方法何时胜出以及为什么的观点──
