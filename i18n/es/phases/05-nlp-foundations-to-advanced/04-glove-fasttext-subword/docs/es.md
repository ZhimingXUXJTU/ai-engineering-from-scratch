# GloVe, FastText y Subword Embeddings.

> Word2Vec entrenó una incorporación por palabra. GloVe factorizó la matriz de cooccurrencia. FastText incorporó las piezas. BPE se conectó a transformadores.
> Word2Vec 为每个词训练一个嵌入──GloVe 分解共现矩阵──FastText 嵌入词的组成部分──BPE 桥接到变压器──

> **【中文解读】**El mundo utiliza la información de la actualidad, el texto rápido, el proceso de resolución de problemas.

**Type:** Build | **类型:** 动手
**Languages:** Python | **语言:** Python
**Prerequisites:** Phase 5 · 03 (Word2Vec from Scratch) | **前置知识:** Phase 5 · 03（Word2Vec 从零实现）
**Time:** ~45 minutes | **时间:** ~45 分钟

## El problema es la introducción del problema

Word2Vec dejó dos preguntas abiertas.

> Word2Vec deja dos preguntas abiertas.

Primero, hubo una línea paralela de investigación que factorizó la matriz de cooccurrencia directamente (LSA, HAL) en lugar de hacer actualizaciones de skip-gram en línea. ¿Fue el enfoque iterativo de Word2Vec fundamentalmente mejor, o fue la diferencia un artefacto de cómo los dos métodos se manejan cuenta? **GloVe**La respuesta es que: factorization de matriz con una pérdida elegida cuidadosamente coincide o supera Word2Vec, y cuesta menos entrenar.

> Primero, existe una ruta de investigación de línea, directamente desglosando la matriz actual (LSA、HAL), en lugar de hacer saltos en línea 更新──. ¿El método de generación de Word2Vec es mejor en sí mismo, o es que la diferencia es sólo un resultado humano de dos métodos de procesamiento de cuentas?**GloVe**回答了:配合精心选择的损失函数矩阵分解匹配或超过 Word2Vec, y el costo de entrenamiento es más bajo.

En segundo lugar, ninguno de los métodos tenía una historia para las palabras que nunca había visto.`Zoomer-approved`¿ Qué ?`dogecoin`, cualquier sustantivo propio acuñado la semana pasada, cada forma inflecta de una raíz rara.**FastText**Esto se arregla incorporando caracteres n-gramas: una palabra es la suma de sus partes, incluyendo morfemas, así que incluso las palabras fuera del vocabulario obtienen un vector sensible.

> Segundo, dos métodos no tienen solución a las palabras nunca vistas.`Zoomer-approved`¿Qué es esto?`dogecoin`、 、 、 、 、 、 、 、 、 、 、 、 、 、 、 、 、 、 、 、 、 、 、 、 、 、 、 、 、 、 、 、 、 、 、 、 、 、 、 、 、 、 、 、 、 、 、 、 、 、 、 、 、 、 、 、 、 、 、 、 、 、 、 、 、 、 、 、 、 、 、 、 、 、 、 、 、 、 、 、 、 、 、 、 、 、 、 、 、 、 、 、 、 、 、 、 、 、 、 、 、 、 、 、 、 、 、 、 、 、 、 、 、 、 、 **FastText**通过嵌入字符n-gram 修复了这个问题: un palabra es de sus partes, incluyendo los elementos de la palabra, por lo que incluso los términos fuera de la expresión pueden obtener un volumen razonable.

En tercer lugar, una vez que llegaron los transformadores, la pregunta cambió de nuevo.**Byte-pair encoding (BPE)**Y sus parientes resolvieron esto aprendiendo un vocabulario de unidades de subpalabra frecuentes que cubre todo.

> En tercer lugar, cuando el Transformer llega, el problema vuelve a cambiar.**字节对编码（Byte-Pair Encoding, BPE）** y sus variaciones a través del aprendizaje de todo                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                  

Esta lección recorre a los tres, y luego explica cuál alcanzar para cuándo.

> Esta clase explica cada uno de estos tres, y luego explica cuándo usar cuál.

## El concepto central.

> **【中文解读】**Este capítulo presenta los conceptos y teorías básicos. La comprensión de estos conceptos es el prerrequisito de la realización posterior de la actividad, y también el conocimiento de los puntos de alta frecuencia de la entrevista y la práctica de la ingeniería.

**GloVe (Global Vectors).**Construye la matriz de coocurrencia palabra-palabras `X`donde`X[i][j]`es la frecuencia de la palabra `j`aparece en el contexto de la palabra `i`. Traen vectores tales que`v_i · v_j + b_i + b_j ≈ log(X[i][j])`- Peso la pérdida de parejas tan frecuentes no dominan.

> **GloVe（全局向量）。**构建词-词共现矩阵 `X`, entre ellos `X[i][j]`Sí es palabra`j`Aparecen en el mundo`i`Frecuencia en el texto siguiente.`v_i · v_j + b_i + b_j ≈ log(X[i][j])`◊ El derecho a la pérdida aumentada para hacer frecuentemente la falta de control ◊ completar ◊

**FastText.**Una palabra es la suma de sus caracteres n-gramos más la palabra misma. `where`Se convierte en`<wh, whe, her, ere, re>, <where>`. El vector de palabras es la suma de esos vectores componentes.`whereupon`) se componen de n-gramos conocidos.

> **FastText。**Un palabra es su carácter n-gram 之和加上词本身──`where`变成 `<wh, whe, her, ere, re>, <where>`△ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △  △    △ △       △                                                                                                                              `whereupon`) de los n-gramos 组合 y

**BPE (Byte-Pair Encoding).**Comience con un vocabulario de bytes individuales (o caracteres). Cuente cada par adyacente en el corpus. Combine el par más frecuente en un nuevo token. Repita para `k`El resultado: un vocabulario de `k + 256`los tokens donde las secuencias frecuentes (`ing`¿ Qué ?`tion`¿ Qué ?`the`Las palabras raras se rompen en piezas familiares.

> **BPE（字节对编码）。**Desde el singular en el idioma, el número de palabras en el idioma se inicia con la frecuencia de cada uno de los ejemplos de la lengua.`k`Siguiente: Resultado: uno `k + 256`个 token 的词表, entre ellos高频序列(`ing`¿Qué es esto?`tion`¿Qué es esto?`the`) es un solo token, rara palabra se descompone en fragmentos familiares. Cada frase puede ser dividida en una forma o otra.

> **【拓展：大语言模型的工程实践】**Desde GPT hasta ChatGPT, el campo de NLP ha experimentado un cambio de paradigma de "cada tarea entrenar un modelo" a "un modelo resolver todas las tareas". En el proyecto real, la implementación de LLM necesita considerar los problemas de token 限制,延迟,成本, seguridad etc.

> **【拓展：RAG 与企业知识库】**检索增强生成(RAG) es la estructura más popular de las aplicaciones de IA de las empresas actuales: la consulta de usuarios primero se consulta los documentos relacionados, luego se vuelve a buscar los resultados como respuesta a la pregunta de LLM.

> **【拓展：NLP 的多语言挑战】**En todo el mundo hay más de 7000 idiomas, pero los estudios de PNL se centran principalmente en inglés y en una minoría de idiomas.

## Construye y realiza.

> **【中文解读】**Este capítulo a través del código de la implementación de algoritmos centrales de cero. Este método "desde cero" puede ayudar a entender el principio detrás del marco, no se encuentra en la caja negra cuando se encuentran problemas.
```figure
n5-subword-merge
```

## Construye el mismo

### GloVe: factorizar la matriz de coocurrencia

```python
import numpy as np
from collections import Counter


def build_cooccurrence(docs, window=5):
    pair_counts = Counter()
    vocab = {}
    for doc in docs:
        for token in doc:
            if token not in vocab:
                vocab[token] = len(vocab)
    for doc in docs:
        indexed = [vocab[t] for t in doc]
        for i, center in enumerate(indexed):
            for j in range(max(0, i - window), min(len(indexed), i + window + 1)):
                if i != j:
                    distance = abs(i - j)
                    pair_counts[(center, indexed[j])] += 1.0 / distance
    return vocab, pair_counts


def glove_train(vocab, pair_counts, dim=16, epochs=100, lr=0.05, x_max=100, alpha=0.75, seed=0):
    n = len(vocab)
    rng = np.random.default_rng(seed)
    W = rng.normal(0, 0.1, size=(n, dim))
    W_tilde = rng.normal(0, 0.1, size=(n, dim))
    b = np.zeros(n)
    b_tilde = np.zeros(n)

    for epoch in range(epochs):
        for (i, j), x_ij in pair_counts.items():
            weight = (x_ij / x_max) ** alpha if x_ij < x_max else 1.0
            diff = W[i] @ W_tilde[j] + b[i] + b_tilde[j] - np.log(x_ij)
            coef = weight * diff

            grad_W_i = coef * W_tilde[j]
            grad_W_tilde_j = coef * W[i]
            W[i] -= lr * grad_W_i
            W_tilde[j] -= lr * grad_W_tilde_j
            b[i] -= lr * coef
            b_tilde[j] -= lr * coef

    return W + W_tilde
```

Dos piezas móviles que vale la pena nombrar.`f(x) = (x/x_max)^alpha`Peso inferior en pares muy frecuentes (como `(the, and)`La integración final es la suma de `W`(centro) y `W_tilde`Sumar ambas es un truco publicado que tiende a superar con sólo uno.

> 两个 puntos de referencia ∙                                                                                                                                                                                                                                                            `f(x) = (x/x_max)^alpha`降低非常频繁的对(如 `(the, and)`El peso del peso, que no conduce a la pérdida.`W`(centro词) y `W_tilde`(上下文词)表之和──对两者求和是一个已发表的技巧, usualmente es mejor usar sólo uno de ellos──

### FastText: incorporaciones conocedoras de las palabras

```python
def char_ngrams(word, n_min=3, n_max=6):
    wrapped = f"<{word}>"
    grams = {wrapped}
    for n in range(n_min, n_max + 1):
        for i in range(len(wrapped) - n + 1):
            grams.add(wrapped[i:i + n])
    return grams
```

```python
>>> char_ngrams("where")
{'<where>', '<wh', 'whe', 'her', 'ere', 're>', '<whe', 'wher', 'here', 'ere>', '<wher', 'where', 'here>'}
```

Cada palabra está representada por su conjunto de n-gramas (normalmente de 3 a 6 caracteres).

> Cada palabra se inserta en su n-gram 集合 (normalmente 3 a 6 caracteres) y para el entrenamiento de skip-gram, se inserta en Word2Vec utilizando una única posición de vector.

```python
def fasttext_vector(word, ngram_table):
    grams = char_ngrams(word)
    vecs = [ngram_table[g] for g in grams if g in ngram_table]
    if not vecs:
        return None
    return np.sum(vecs, axis=0)
```

Para una palabra invisible, todavía se obtiene un vector siempre y cuando algunos de sus n-gramos son conocidos. `whereupon`acciones `<wh`¿ Qué ?`her`¿ Qué ?`ere`, y `<where`con`where`, así que los dos aterrizan cerca de uno al otro.

> Para palabras no vistas, siempre y cuando su parte n-grama es conocida, todavía puedes obtener una velocidad.`whereupon`Con`where`Compartir`<wh`¿Qué es esto?`her`¿Qué es esto?`ere`Y `<where`Así que ambos están en una posición cercana.

### BPE: vocabulario de palabras subpartidas aprendidas

```python
def learn_bpe(corpus, k_merges):
    vocab = Counter()
    for word, freq in corpus.items():
        tokens = tuple(word) + ("</w>",)
        vocab[tokens] = freq

    merges = []
    for _ in range(k_merges):
        pair_freq = Counter()
        for tokens, freq in vocab.items():
            for a, b in zip(tokens, tokens[1:]):
                pair_freq[(a, b)] += freq
        if not pair_freq:
            break
        best = pair_freq.most_common(1)[0][0]
        merges.append(best)

        new_vocab = Counter()
        for tokens, freq in vocab.items():
            new_tokens = []
            i = 0
            while i < len(tokens):
                if i + 1 < len(tokens) and (tokens[i], tokens[i + 1]) == best:
                    new_tokens.append(tokens[i] + tokens[i + 1])
                    i += 2
                else:
                    new_tokens.append(tokens[i])
                    i += 1
            new_vocab[tuple(new_tokens)] = freq
        vocab = new_vocab
    return merges


def apply_bpe(word, merges):
    tokens = list(word) + ["</w>"]
    for a, b in merges:
        new_tokens = []
        i = 0
        while i < len(tokens):
            if i + 1 < len(tokens) and tokens[i] == a and tokens[i + 1] == b:
                new_tokens.append(a + b)
                i += 2
            else:
                new_tokens.append(tokens[i])
                i += 1
        tokens = new_tokens
    return tokens
```

```python
>>> corpus = Counter({"low": 5, "lower": 2, "newest": 6, "widest": 3})
>>> merges = learn_bpe(corpus, k_merges=10)
>>> apply_bpe("lowest", merges)
['low', 'est</w>']
```

La primera iteración fusiona el par adyacente más común.`low`¿ Qué ?`est`¿ Qué ?`tion`Las palabras raras se rompen de forma clara.

> La primera vez que se ha hecho el mayor número de veces que se ha hecho el mayor número de veces que se ha hecho el mayor número de veces que se ha hecho el mayor número de veces que se ha hecho el mayor número de veces que se ha hecho el mayor número de veces que se ha hecho el mayor número de veces que se ha hecho el mayor número de veces que se ha hecho el mayor número de veces que se ha hecho el mayor número de veces que se ha hecho el mayor número de veces que se ha hecho el mayor número de veces que se ha hecho el mayor número de veces que se ha hecho el mayor número de veces que se ha hecho el mayor número de veces que se ha hecho.`low`¿Qué es esto?`est`¿Qué es esto?`tion`) se convierte en un solo token, rara palabra干净地分解──

Los tokenizadores reales de GPT / BERT / T5 aprenden fusiones de 30k-100k. Resultado: cualquier texto se tokeniza en una secuencia de longitud limitada de IDs conocidas, sin OOV nunca.

> El resultado: cualquier texto está dividido en una serie de caracteres de identificación conocida, nunca habrá OOV.

> **【中文解读】**Este capítulo muestra cómo utilizar un marco maduro (como PyTorch、HuggingFace, etc.) para aplicar rápidamente esta tecnología. En los proyectos reales, se realiza con prioridad el uso de un marco experimentado, se pueden reducir errores y mejorar la eficiencia de desarrollo.

> **【拓展：Prompt Engineering 与 LLM 应用】**La ingeniería rápida se ha convertido en la habilidad central de los ingenieros de PNL. Desde la Cero-Shot hasta la Few-Shot, desde la Cadena de Pensamiento hasta la Reacción, diferentes estrategias de sugerencias se aplican a diferentes escenarios.

## Usalo con el marco de ejecución

En la práctica, rara vez entrenas uno de estos tú mismo.

> En la práctica, casi no te entrenas a ti mismo.

```python
import fasttext.util
fasttext.util.download_model("en", if_exists="ignore")
ft = fasttext.load_model("cc.en.300.bin")
print(ft.get_word_vector("whereupon").shape)
print(ft.get_word_vector("zoomerapproved").shape)
```

Para la tokenización de subpalabra de estilo BPE en la era de los transformadores:

> 对于 Transformer 时代的 BPE 风格子词分词:

```python
from transformers import AutoTokenizer

tok = AutoTokenizer.from_pretrained("gpt2")
print(tok.tokenize("unbelievably tokenized"))
```

```
['un', 'bel', 'iev', 'ably', 'Ġtoken', 'ized']
```

El `Ġ`El prefijo marca los límites de palabras (una convención GPT-2).

> `Ġ`Antes de la fecha, el nombre de la palabra "BPE" se ha convertido en el nombre de la palabra "BPE" en el nombre de la palabra "BPE".

### ¿Cuándo elegir cuál

| Situation | Pick | 场景 | 选择 |
|-----------|------|------|------|
| Pretrained general-purpose word vectors, no OOV tolerance needed | GloVe 300d | 预训练通用词向量，不需要处理 OOV | GloVe 300 维 |
| Pretrained general-purpose word vectors, must handle misspellings / neologisms / morphologically rich languages | FastText | 预训练通用词向量，必须处理拼写错误 / 新词 / 形态丰富的语言 | FastText |
| Anything going into a transformer (training or inference) | Whatever tokenizer the model shipped with. Never swap. | 输入 Transformer 的任何场景（训练或推理） | 模型自带的分词器。永远不要替换。 |
| Training your own language model from scratch | Train a BPE or SentencePiece tokenizer on your corpus first | 从零训练自己的语言模型 | 先在你的语料上训练 BPE 或 SentencePiece 分词器 |
| Production text classification with a linear model | Still TF-IDF. Lesson 02. | 使用线性模型的生产文本分类 | 仍然用 TF-IDF。第 02 课。 |

> **【中文解读】**Este capítulo se centra en cómo se puede implementar el modelo como producto disponible. Desde el modelo original hasta el sistema de producción, se deben considerar múltiples dimensiones de optimización de rendimiento, tratamiento de errores, control, etc.

## Envíe el producto .

Salvo como`outputs/skill-embeddings-picker.md`¿Qué es esto ?

```markdown
---
name: tokenizer-picker
description: Pick a tokenization approach for a new language model or text pipeline.
version: 1.0.0
phase: 5
lesson: 04
tags: [nlp, tokenization, embeddings]
---

Given a task and dataset description, you output:

1. Tokenization strategy (word-level, BPE, WordPiece, SentencePiece, byte-level). One-sentence reason.
2. Vocabulary size target (e.g., 32k for an English-only LM, 64k-100k for multilingual).
3. Library call with the exact training command. Name the library. Quote the arguments.
4. One reproducibility pitfall. Tokenizer-model mismatch is the single most common silent production bug; call out which pair must be used together.

> **【中文解读】** 练习题按照 Easy/Medium/Hard 三个难度递进。建议至少完成 Medium 级别的题目，Hard 级别适合深入研究或面试准备。

Refuse to recommend training a custom tokenizer when the user is fine-tuning a pretrained LLM. Refuse to recommend word-level tokenization for any model targeting production inference. Flag non-English / multi-script corpora as needing SentencePiece with byte fallback.
```

## Los ejercicios.

1. **Easy.**- ¿ Qué ?`char_ngrams("playing")`y `char_ngrams("played")`. Calcule la superposición de Jaccard de los dos conjuntos de n-gram.`pla`¿ Qué ?`lay`¿ Qué ?`play`), por lo que FastText transfiere bien entre variantes morfológicas.
   **简单。**运行                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           `char_ngrams("playing")`Y `char_ngrams("played")`△ calcular dos n-gramos 集合的Jaccard 重叠度── Usted debería ver un montón de compartido 片段(`pla`¿Qué es esto?`lay`¿Qué es esto?`play`), esta es la razón de que FastText en forma de cambio entre los cambios de forma buena migración.
2. **Medium.**Extenderse`learn_bpe`Para rastrear el crecimiento del vocabulario. Plot tokens-per corpus-character como función del número de fusiones. Usted debe ver una compresión rápida en un primer momento, asymptoting cerca de ~2-3 caracteres por token.
   **中等。**扩展 `learn_bpe`Es decir, el número de símbolos de cada símbolo de un idioma se puede ver en un punto de vista de la forma en que se compone el símbolo.
3. **Hard.**Entrenar un BPE de 1k de fusión en las obras completas de Shakespeare. Comparar la tokenización de palabras comunes con nombres propios raros. Medir los tokens promedio por palabra antes y después. Escribir lo que te sorprendió.
   **困难。**En el libro de Shakespeare se ha entrenado mil veces en BPE.

> **【中文解读】**Practice los temas de fácil/medio/duro  3 difficulty to pass in  Recomenda al menos completar los temas de grado medio  Grado duro  para la preparación de la entrevista

## Términos clave .

| Term | What people say | What it actually means | 术语 | 人们常说的 | 实际含义 |
|------|-----------------|-----------------------|------|-----------|---------|
| Co-occurrence matrix | Word-word frequency table | `X[i][j]` = how often word `j` appears in a window around word `i`. | 共现矩阵 | 词-词频率表 | `X[i][j]` = 词 `j` 在词 `i` 周围窗口中出现的频率。 |
| Subword | Piece of a word | A character n-gram (FastText) or learned token (BPE/WordPiece/SentencePiece). | 子词 | 词的片段 | 字符 n-gram（FastText）或学习到的 token（BPE/WordPiece/SentencePiece）。 |
| BPE | Byte-pair encoding | Iterative merging of most-frequent adjacent pairs until vocabulary hits target size. | BPE（字节对编码） | 字节对编码 | 迭代合并最频繁的相邻对，直到词表达到目标大小。 |
| OOV | Out of vocabulary | Word the model has never seen. Word2Vec/GloVe fail. FastText and BPE handle it. | OOV（词表外） | 词表外 | 模型从未见过的词。Word2Vec/GloVe 会失败。FastText 和 BPE 能处理。 |
| Byte-level BPE | BPE on raw bytes | GPT-2's scheme. Vocabulary starts with 256 bytes, so nothing is ever OOV. | 字节级 BPE | 对原始字节的 BPE | GPT-2 的方案。词表从 256 个字节开始，所以永远不会有 OOV。 |

> **【中文解读】**En el lenguaje de los términos "Lo que la gente dice" vs "Lo que realmente significa" se distingue entre el lenguaje diario y la definición técnica de significado.

## Más Leer más Leer más

- [Pennington, Socher, Manning (2014). GloVe: Global Vectors for Word Representation](https://nlp.stanford.edu/pubs/glove.pdf) el papel GloVe, siete páginas, todavía la mejor derivación de la pérdida. / GloVe 论文,七页,仍然是损失函数最好的推导──
- [Bojanowski et al. (2017). Enriching Word Vectors with Subword Information](https://arxiv.org/abs/1607.04606) FastText. / FastText 论文。
- [Sennrich, Haddow, Birch (2016). Neural Machine Translation of Rare Words with Subword Units](https://arxiv.org/abs/1508.07909) el documento que introdujo el BPE en la PNL moderna. / 将 BPE 引入现代 NLP 的论文──
- [Hugging Face tokenizer summary](https://huggingface.co/docs/transformers/tokenizer_summary) cómo BPE, WordPiece y SentencePiece realmente difieren en la práctica. / BPE、WordPiece 和 SentencePiece 在实践中的区别──
