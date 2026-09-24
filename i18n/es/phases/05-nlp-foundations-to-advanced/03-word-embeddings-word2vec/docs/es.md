# Word Embeddings  Word2Vec desde cero  Word2Vec desde cero

> Una palabra es la compañía que mantiene, y si se ejerce una red superficial sobre esa idea, la geometría se cae.
> Una palabra depende de la empresa que mantiene en la que se entrena una red de nivel bajo, algo que surge naturalmente.

> **【中文解读】**Word2Vec Colocar el término que se proyecta en el espacio de velocidad, similar a un término que se aproxima en el espacio de velocidad.

**Type:** Build | **类型:** 动手
**Languages:** Python | **语言:** Python
**Prerequisites:** Phase 5 · 02 (BoW + TF-IDF), Phase 3 · 03 (Backpropagation from Scratch) | **前置知识:** Phase 5 · 02（BoW + TF-IDF），Phase 3 · 03（反向传播从零实现）
**Time:** ~75 minutes | **时间:** ~75 分钟

## El problema es la introducción del problema

TF-IDF sabe `dog`y `puppy`No se sabe que significan casi lo mismo.`dog`no puede generalizarse a una revisión sobre `puppy`Puedes revisar esto listando sinónimos, pero eso falla en términos raros, jerga de dominio y en cada lengua que no anticipaste.

> TF-IDF                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                          `dog`Y `puppy`Es un término diferente. No sabe que significan casi lo mismo.`dog`Las clases de entrenamiento no pueden ampliarse a la`puppy`Puede remediarse con la lista de sinónimos, pero esto es raro en términos y en cada idioma que no se espera que falle.

¿ Quieres una representación donde ?`dog`y `puppy`Tierra cerca de uno en el espacio.`king - man + woman`tierras cercanas`queen`- Un modelo entrenado en`dog`Transfiere alguna señal a `puppy`- Por gratis.

> Tú quieres un modo de decir,让 `dog`Y `puppy`En el espacio cerca.`king - man + woman`¿ Qué pasa ?`queen`附近──让在 `dog`Modelo de entrenamiento gratis hacia `puppy`传递 algunos señales.

Word2Vec nos dio ese espacio. Dos capas de red neuronal, trillones de tokens de entrenamiento, publicados en 2013. La arquitectura es casi vergonzosamente simple. Los resultados remodelaron la PNL durante una década.

> Word2Vec nos ha dado un espacio así. Dos niveles de redes neuronales, millones de tokens de entrenamiento en marcha, publicado en 2013.

## El concepto central.

> **【中文解读】**Este capítulo presenta los conceptos y teorías básicos. La comprensión de estos conceptos es el prerrequisito de la realización posterior de la actividad, y también el conocimiento de los puntos de alta frecuencia de la entrevista y la práctica de la ingeniería.

**Distributional hypothesis**(Primero, 1957): "Conocerás una palabra por la compañía que mantiene". Si dos palabras aparecen en contextos similares, probablemente significan cosas similares.

> **分布假设（Distributional Hypothesis）**(Primero, 1957):"Tu vas a conocerlo a través de una palabra que mantiene en la empresa. "Si dos palabras aparecen similares en la siguiente, pueden significar cosas similares.

Word2Vec viene en dos sabores, ambos explotando esa idea.

> Word2Vec tiene dos variantes, todos usamos esta idea.

- **Skip-gram.**Dado una palabra central, predica las palabras circundantes.`cat -> (the, sat, on)`con el tamaño de la ventana 2.
  **Skip-gram（跳字模型）。**给定中心词,预测周围的词──`cat -> (the, sat, on)`, ventana grande para 2
- **CBOW (continuous bag of words).**Dadas las palabras circundantes, predica el centro.`(the, sat, on) -> cat`¿ Qué ?
  **CBOW（连续词袋模型）。**给定周围的词,预测中心词──`(the, sat, on) -> cat`¿Qué es eso?

El Skip-gram es más lento para entrenar pero maneja mejor las palabras raras.

> El programa de Skip-gram  entrenamiento más lento pero mejor para tratar raramente los términos .

La red tiene una capa oculta sin ninguna no linealidad. La entrada es un vector de una sola calidez sobre el vocabulario. La salida es una suave máxima sobre el vocabulario. Después del entrenamiento, se tira la capa de salida. Los pesos de la capa oculta son los embebidos.

> 网络有一个不带非线性激活函数的隐藏层――输入是单词表上的一个热向量――输出是单词表上的软max――训练后,你丢弃输出层――隐藏层的权重就是嵌入――

```
one-hot(center) ── W ──▶ hidden (d-dim) ── W' ──▶ softmax(vocab)
                          ^
                          this is the embedding
```

El truco: la máxima de más de 100 mil palabras es prohibitivamente cara.**negative sampling**Para convertirlo en una tarea de clasificación binaria. Prevé "¿apareció esta palabra de contexto cerca de esta palabra central, sí o no". Muestre un puñado de palabras negativas (no coincidentes) por par de entrenamiento en lugar de calcular softmax sobre todo el vocabulario.

> : para 100.000 palabras hacer suavemax 代价太高──Word2Vec 使用**负采样（Negative Sampling）**Se puede traducir en dos clases de tareas. Prevé " este subastavo se encuentra en este centro de palabras, es o no" (en inglés).

> **【拓展：大语言模型的工程实践】**Desde GPT hasta ChatGPT, el campo de NLP ha experimentado un cambio de paradigma de "cada tarea entrenar un modelo" a "un modelo resolver todas las tareas". En el proyecto real, la implementación de LLM necesita considerar los problemas de token 限制,延迟,成本, seguridad etc.

> **【拓展：RAG 与企业知识库】**检索增强生成(RAG) es la estructura más popular de las aplicaciones de IA de las empresas actuales: la consulta de usuarios primero se consulta los documentos relacionados, luego se vuelve a buscar los resultados como respuesta a la pregunta de LLM.

> **【拓展：NLP 的多语言挑战】**En todo el mundo hay más de 7000 idiomas, pero los estudios de PNL se centran principalmente en inglés y en una minoría de idiomas.

## Construye y realiza.

> **【中文解读】**Este capítulo a través del código de la implementación de algoritmos centrales de cero. Este método "desde cero" puede ayudar a entender el principio detrás del marco, no se encuentra en la caja negra cuando se encuentran problemas.
```figure
word-vector-arithmetic
```

## Construye el mismo

### Paso 1: entrenamiento de pares desde un corpus

```python
def skipgram_pairs(docs, window=2):
    pairs = []
    for doc in docs:
        for i, center in enumerate(doc):
            for j in range(max(0, i - window), min(len(doc), i + window + 1)):
                if i == j:
                    continue
                pairs.append((center, doc[j]))
    return pairs
```

```python
>>> skipgram_pairs([["the", "cat", "sat", "on", "mat"]], window=2)
[('the', 'cat'), ('the', 'sat'),
 ('cat', 'the'), ('cat', 'sat'), ('cat', 'on'),
 ('sat', 'the'), ('sat', 'cat'), ('sat', 'on'), ('sat', 'mat'),
 ...]
```

Cada par (centro, contexto) en una ventana es un ejemplo positivo de entrenamiento.

> Cada palabra central en la ventana, es un ejemplo de entrenamiento.

### Paso 2: incrustación de tablas

Dos matrices.`W`es la tabla de inserción de palabras centrales (la que mantiene). `W'`es la tabla de palabras contextuales (a menudo descartadas, a veces mediadas con `W`¿Qué es lo que se hace?

> Dos cuadradas.`W`Es el centro de palabras que me han dejado.`W'`Es un lenguaje que se deja solos.`W`取平均) ⋅

```python
import numpy as np


def init_embeddings(vocab_size, dim, seed=0):
    rng = np.random.default_rng(seed)
    W = rng.normal(0, 0.1, size=(vocab_size, dim))
    W_prime = rng.normal(0, 0.1, size=(vocab_size, dim))
    return W, W_prime
```

El tamaño de la vocab 10k y dim 100 es realista; para la enseñanza, 50 vocab x 16 dim es suficiente para ver la geometría.

> La forma de aprender a usar 50 palabras x 16 dimensiones es suficiente para ver los resultados.

### Paso 3: objetivo negativo de muestreo

Para cada par positivo `(center, context)`, muestra `k`Entrenando el modelo para que el producto punto`W[center] · W'[context]`es alto para los positivos y bajo para los negativos.

> Para cada muestra correcta`(center, context)`, de la palabra表中采样 `k`个随机词作为负例──训练模型使正例的点积 `W[center] · W'[context]`高,负例的低──

```python
def sigmoid(x):
    return 1.0 / (1.0 + np.exp(-np.clip(x, -20, 20)))


def train_pair(W, W_prime, center_idx, context_idx, negative_indices, lr):
    v_c = W[center_idx]
    u_pos = W_prime[context_idx]
    u_negs = W_prime[negative_indices]

    pos_score = sigmoid(v_c @ u_pos)
    neg_scores = sigmoid(u_negs @ v_c)

    grad_center = (pos_score - 1) * u_pos
    for i, u in enumerate(u_negs):
        grad_center += neg_scores[i] * u

    W[context_idx] = W[context_idx]
    W_prime[context_idx] -= lr * (pos_score - 1) * v_c
    for i, neg_idx in enumerate(negative_indices):
        W_prime[neg_idx] -= lr * neg_scores[i] * v_c
    W[center_idx] -= lr * grad_center
```

La fórmula mágica: pérdida logística en el par positivo (queremos sigmoide cerca de 1) más pérdida logística en pares negativos (queremos sigmoide cerca de 0). Los gradientes fluyen hacia ambas tablas. La derivación completa está en el papel original; pase a través de él una vez con lápiz y papel si desea que se adhiera.

> La fórmula de 神奇:正例對上論理損失 (正例對上論理損失) 希望 sigmoid 接近 1)加上负例對上論理損失 (加上负例對上論理損失) 希望 sigmoid 接近 0) ・・・梯度流向两个表──完整推导见原始文; si quieres que se entienda más profundamente, usa papel y lápiz de caminar una y otra vez──

### Paso 4: entrenar en un cuerpo de juguete

```python
def train(docs, dim=16, window=2, k_neg=5, epochs=100, lr=0.05, seed=0):
    vocab = build_vocab(docs)
    vocab_size = len(vocab)
    rng = np.random.default_rng(seed)
    W, W_prime = init_embeddings(vocab_size, dim, seed=seed)
    pairs = skipgram_pairs(docs, window=window)

    for epoch in range(epochs):
        rng.shuffle(pairs)
        for center, context in pairs:
            c_idx = vocab[center]
            ctx_idx = vocab[context]
            negs = rng.integers(0, vocab_size, size=k_neg)
            negs = [n for n in negs if n != ctx_idx and n != c_idx]
            train_pair(W, W_prime, c_idx, ctx_idx, negs, lr)
    return vocab, W
```

Después de suficientes épocas en un gran corpus, las palabras que comparten contextos tienen un centro similar. En un corpus de juguete, se ve el efecto débilmente. En miles de millones de tokens, se ve dramáticamente.

> Después de pasar por suficientes ramas de tiempo en el lenguaje de los juegos, el uso compartido de los siguientes términos tiene un similar contenido central.

### Paso 5: el truco de analogía

```python
def nearest(vocab, W, target_vec, topk=5, exclude=None):
    exclude = exclude or set()
    inv_vocab = {i: w for w, i in vocab.items()}
    norms = np.linalg.norm(W, axis=1, keepdims=True) + 1e-9
    W_norm = W / norms
    target = target_vec / (np.linalg.norm(target_vec) + 1e-9)
    sims = W_norm @ target
    order = np.argsort(-sims)
    out = []
    for i in order:
        if i in exclude:
            continue
        out.append((inv_vocab[i], float(sims[i])))
        if len(out) == topk:
            break
    return out


def analogy(vocab, W, a, b, c, topk=5):
    v = W[vocab[b]] - W[vocab[a]] + W[vocab[c]]
    return nearest(vocab, W, v, topk=topk, exclude={vocab[a], vocab[b], vocab[c]})
```

En vectores de noticias de Google 300d pre-entrenados:

```python
>>> analogy(vocab, W, "man", "king", "woman")
[('queen', 0.71), ('monarch', 0.62), ('princess', 0.59), ...]
```

`king - man + woman = queen`No porque el modelo sepa lo que es la realeza, porque el vector`(king - man)`captura algo como "real", y añadiéndolo a `woman`tierras cerca de la región de las mujeres reales.

> `king - man + woman = queen`No es porque el modelo sepa lo que es la casa, sino porque el volumen.`(king - man)`Captura algo parecido a "Royal House", lo agregará.`woman`Está en la zona de las mujeres de la casa de los reyes.

> **【中文解读】**Este capítulo muestra cómo utilizar un marco maduro (como PyTorch、HuggingFace, etc.) para aplicar rápidamente esta tecnología. En los proyectos reales, se realiza con prioridad el uso de un marco experimentado, se pueden reducir errores y mejorar la eficiencia de desarrollo.

> **【拓展：Prompt Engineering 与 LLM 应用】**La ingeniería rápida se ha convertido en la habilidad central de los ingenieros de PNL. Desde la Cero-Shot hasta la Few-Shot, desde la Cadena de Pensamiento hasta la Reacción, diferentes estrategias de sugerencias se aplican a diferentes escenarios.

## Usalo con el marco de ejecución

Escribir Word2Vec desde cero es enseñar.`gensim`¿ Qué ?

> Desde el principio de la escritura Word2Vec es para la enseñanza.`gensim`¿Qué es eso?

```python
from gensim.models import Word2Vec

sentences = [
    ["the", "cat", "sat", "on", "the", "mat"],
    ["the", "dog", "ran", "across", "the", "room"],
]

model = Word2Vec(
    sentences,
    vector_size=100,
    window=5,
    min_count=1,
    sg=1,
    negative=5,
    workers=4,
    epochs=30,
)

print(model.wv["cat"])
print(model.wv.most_similar("cat", topn=3))
```

Para el trabajo real, casi nunca entrenas Word2Vec tú mismo.

> 实际工作中,你几乎从不自练 Word2Vec──你下载预训向量──

- **GloVe** El enfoque de factorizamiento de la matriz de cooccurrencia de Stanford. 50d, 100d, 200d, 300d puntos de control. Buena cobertura general. La lección 04 cubre específicamente GloVe.
  **GloVe** Estánfu's Common Current Matrix Decomposition Method―50 维、100 维、200 维、300 维的检查点―通用覆盖良好―第04 课专讲解 GloVe―
- **fastText** La extensión Word2Vec de Facebook que incorpora n-gramas de caracteres.
  **fastText** Word2Vec 扩展,嵌入字符 n-gram──通过组合子词处理词表外词──第 04 课──
- **Pretrained Word2Vec on Google News** 300d, vocabulario de palabras 3M, publicado 2013. Todavía descargado diariamente.
  **Google News 预训练 Word2Vec** 300 维,300 millones de palabras表, 2013 años de publicación.

### Cuando Word2Vec todavía gane en 2026

- Entrenamiento en resúmenes médicos en una hora en una computadora portátil, obtener vectores especializados sin capturas de modelos generales.
  En el libro de notas, se utiliza una hora de entrenamiento en resumen médico, para obtener un modelo general de la capacidad de captura de un espectro especial.
- Ingeniería de características de estilo analógico. `gender_vector = mean(man - woman pairs)`...desde otras palabras para obtener un eje neutral de género.
  类比式特征工程──`gender_vector = mean(man - woman pairs)`                                                                                                                                                                                                                                                              
- Interpretabilidad. 100d es lo suficientemente pequeño como para trazar a través de PCA o t-SNE y ver realmente forma de grupos.
  可解释性──100 维足够小, puede ser visto mediante PCA o t-SNE 图并实际见聚类形成──
- En cualquier lugar la inferencia tiene que ejecutarse en el dispositivo sin GPU.
  任何需要在没有GPU的设备上运行推理的场景──Word2Vec 查找就是单行获取──

### Donde Word2Vec falla

La pared de la polisemia.`bank`tiene un vector. `river bank`y `financial bank`Comparte con nosotros.`table`Un clasificador aguas abajo no puede distinguir los sentidos del vector.

> Muchos términos de barreras.`bank`Sólo hay un solo movimiento.`river bank`Y `financial bank`Compartirlo.`table`(electrónica en el formato de la tabla) Compartirlo.

Las incorporaciones contextuales (ELMo, BERT, cada transformador desde entonces) resolvieron esto produciendo un vector diferente para cada ocurrencia de la palabra en función del contexto circundante.

> 上下文嵌入(ELMo、BERT 以及后的所有变体former) a través de la aparición de diferentes velocidades para cada palabra en función de la siguiente palabra en torno a la cual se ha resuelto este problema.

El problema de la falta de vocabulario es el otro fracaso.`Zoomer-approved`Si no se trata de datos de formación, no hay retroceso. fastText corrige esto con la composición de las palabras (lección 04).

> 词表外(Fuera del vocabulario) el problema es otro fracaso―si `Zoomer-approved`En el entrenamiento de datos, Word2Vec 就從未见过它──没有后备方案──fastText 通過子词组合修复了这个问题 (→                                                                                                                                                                                                                                            

> **【中文解读】**Este capítulo se centra en cómo se puede implementar el modelo como producto disponible. Desde el modelo original hasta el sistema de producción, se deben considerar múltiples dimensiones de optimización de rendimiento, tratamiento de errores, control, etc.

## Envíe el producto .

Salvo como`outputs/skill-embedding-probe.md`¿Qué es esto ?

```markdown
---
name: embedding-probe
description: Inspect a word2vec model. Run analogies, find neighbors, diagnose quality.
version: 1.0.0
phase: 5
lesson: 03
tags: [nlp, embeddings, debugging]
---

You probe trained word embeddings to verify they are working. Given a `gensim.models.KeyedVectors` object and a vocabulary, you run:

1. Three canonical analogy tests. `king : man :: queen : woman`. `paris : france :: tokyo : japan`. `walking : walked :: swimming : ?`. Report the top-1 result and its cosine.
2. Five nearest-neighbor tests on domain-specific words the user supplies. Print top-5 neighbors with cosines.
3. One symmetry check. `similarity(a, b) == similarity(b, a)` to within float precision.
4. One degenerate check. If any embedding has a norm below 0.01 or above 100, the model has a training bug. Flag it.

> **【中文解读】** 练习题按照 Easy/Medium/Hard 三个难度递进。建议至少完成 Medium 级别的题目，Hard 级别适合深入研究或面试准备。

Refuse to declare a model good on analogy accuracy alone. Analogy benchmarks are gameable and do not transfer to downstream tasks. Recommend intrinsic + downstream evaluation together.
```

## Los ejercicios.

1. **Easy.**Realice el ciclo de entrenamiento en un pequeño corpus (20 frases sobre gatos y perros).`nearest(vocab, W, W[vocab["cat"]])`retorno `dog`En caso contrario, aumenta las épocas o el vocabulario.
   **简单。**En un pequeño lenguaje en el ciclo de entrenamiento de la práctica de la práctica de la práctica de la práctica de la práctica de la práctica de la práctica de la práctica de la práctica de la práctica de la práctica de la práctica de la práctica de la práctica de la práctica de la práctica de la práctica de la práctica de la práctica de la práctica de la práctica de la práctica de la práctica de la práctica de la práctica de la práctica de la práctica de la práctica de la práctica de la práctica de la práctica de la práctica de la práctica de la práctica de la práctica de la práctica de la práctica de la práctica de la práctica de la práctica de la práctica de la práctica de la práctica de la práctica de la práctica de la práctica de la práctica de la práctica de la práctica de la práctica de la práctica de la práctica de la práctica de la práctica de la práctica de la práctica de la práctica de la práctica de la práctica de la práctica de la práctica de la práctica de la práctica de la práctica de la práctica de la práctica de la práctica de la práctica de la práctica de la práctica de la práctica de la práctica de la práctica de la práctica de la práctica de la práctica de la práctica de la práctica de la práctica de la práctica de la práctica de la práctica de la práctica de la práctica de la práctica de la práctica de la práctica de la práctica de la práctica de la práctica de la práctica de la práctica de la práctica de la práctica de la práctica de la práctica de la práctica de la práctica de la práctica de la práctica de la práctica de la práctica de la práctica de la práctica de la práctica de la práctica de la práctica de la práctica de la práctica de la práctica de la práctica de la práctica de la práctica de la práctica de la práctica de la práctica de la práctica de la práctica de la práctica de la práctica de la práctica de la práctica de la práctica de la práctica de la práctica de la práctica de la práctica de la práctica de la práctica de la práctica de la práctica de la práctica de la práctica de la práctica de la práctica de la práctica de la práctica de la práctica de la práctica de la práctica de la práctica de la práctica de la práctica de la práctica de la práctica de la práctica de la práctica de la práctica de la práctica de la práctica de la práctica de la práctica de la práctica de la práctica de la práctica de la práctica de la práctica de la práctica de la práctica de la práctica de la práctica de la práctica de la práctica de la práctica de la práctica de la práctica de`nearest(vocab, W, W[vocab["cat"]])`返回的前3中包含 `dog`Si no, aumenta la ronda o la palabra.
2. **Medium.**Añadir submuestras de palabras frecuentes.`10^-5`Se evaluarán los resultados de las pruebas de formación en pares de formación con probabilidad proporcional a su frecuencia.
   **中等。**添加高频词子采样──频率高于 `10^-5`La probabilidad de que las palabras sean correctas en relación con su frecuencia es de entrenamiento a medio desechado.
3. **Hard.**Entrenar un modelo en el corpus de 20 Newsgroups.`he - she`y `doctor - nurse`. Proyecto de palabras de ocupación en ambos ejes. informe cuáles ocupaciones tienen la mayor brecha de sesgo. este es el tipo de investigación de equidad de la sonda que usan los investigadores.
   **困难。**En 20 grupos de noticias 语料上训练模型――计算两个偏见轴:`he - she`Y `doctor - nurse`将职业词投投投两轴上 报告哪些职业有最大偏见差                                                                                                                                                                                                                                                   

> **【中文解读】**Practice los temas de fácil/medio/duro  3 difficulty to pass in  Recomenda al menos completar los temas de grado medio  Grado duro  para la preparación de la entrevista

## Términos clave .

| Term | What people say | What it actually means | 术语 | 人们常说的 | 实际含义 |
|------|-----------------|-----------------------|------|-----------|---------|
| Word embedding | Word as a vector | A dense, low-dim (typically 100-300) representation learned from context. | 词嵌入 | 词向量 | 从上下文学习的稠密、低维（通常 100-300）表示。 |
| Skip-gram | Word2Vec trick | Predict context words from center word. Slower than CBOW, better for rare words. | Skip-gram | Word2Vec 技巧 | 从中心词预测上下文词。比 CBOW 慢，对罕见词更好。 |
| Negative sampling | Training shortcut | Replace softmax over full vocab with binary classification against `k` random words. | 负采样 | 训练捷径 | 用对 `k` 个随机词的二分类替换对整个词表的 softmax。 |
| Static embedding | One vector per word | Same vector regardless of context. Fails on polysemy. | 静态嵌入 | 每个词一个向量 | 无论上下文如何都是同一个向量。在多义词上失败。 |
| Contextual embedding | Context-sensitive vector | Different vector for each occurrence based on surrounding words. What transformers produce. | 上下文嵌入 | 上下文敏感向量 | 根据周围词，每次出现都是不同的向量。Transformer 产生的。 |
| OOV | Out of vocabulary | Word not seen in training. Word2Vec cannot produce a vector for these. | OOV（词表外） | 词表外 | 训练中未见过的词。Word2Vec 无法为这些词产生向量。 |

> **【中文解读】**En el lenguaje de los términos "Lo que la gente dice" vs "Lo que realmente significa" se distingue entre el lenguaje diario y la definición técnica de significado.

## Más Leer más Leer más

- [Mikolov et al. (2013). Distributed Representations of Words and Phrases and their Compositionality](https://arxiv.org/abs/1310.4546) el papel de muestreo negativo. Corto y legible. / 负采样论文。短小易读。
- [Rong, X. (2014). word2vec Parameter Learning Explained](https://arxiv.org/abs/1411.2738) la derivación más clara de los gradientes, si la matemática del papel original se siente densa. / 最清晰的梯度推导, si usted siente que la matemática de los gráficos es demasiado intenso.
- [gensim Word2Vec tutorial](https://radimrehurek.com/gensim/models/word2vec.html) configuración de entrenamiento de producción que realmente funcione. / 真正有效的生产训练设置──
