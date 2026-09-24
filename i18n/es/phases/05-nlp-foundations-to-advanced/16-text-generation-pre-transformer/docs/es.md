# Géneración de texto antes de transformadores  N-gram Modelos de lenguaje  Transformer                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        

> Si una palabra es sorprendente, el modelo es malo. La perplejidad hace que la sorpresa sea un número.
> Si una palabra es sorprendente, el modelo es malo. La confusión la convierte en un número.

> **【中文解读】**N-gram 统计词频预测 下一个词──GPT 就是更强大的语言模型──

**Type:** Build | **类型:** 动手
**Languages:** Python | **语言:** Python
**Prerequisites:** Phase 5 · 01 (Text Processing), Phase 2 · 14 (Naive Bayes) | **前置知识:** Phase 5 · 01（文本处理），Phase 2 · 14（朴素贝叶斯）
**Time:** ~45 minutes | **时间:** ~45 分钟

## El problema es la introducción del problema

Antes de los transformadores, antes de las RNN, antes de las incorporaciones de palabras, un modelo de lenguaje predijo la siguiente palabra contando la frecuencia con la que siguió a la anterior `n-1`Cuenta "el gato" → "sentarse" 47 veces, "el gato" → "salto" 12 veces, "el gato" → "frigerador" 0 veces. Normaliza para obtener una distribución de probabilidades.

> En el transformer  antes, en el RNN  antes, en el word embedded antes, lenguaje modelo                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    `n-1`个词后面跟着当前词的频率来预测下一个词──统计 "el gato" → "sat" 出现 47 次, "el gato" → "jumped" 出现 12 次, "el gato" → "frigerador" 出现 0 次──归结得到概率分布──

> **【中文解读】**La pregunta planteada en este capítulo es: ¿cómo entender y aplicar correctamente esta tecnología en la ingeniería real? Comprender el contexto de la cuestión ayuda a comprender los puntos clave de decisión del tipo de selección técnica. En los sistemas de IA reales, el tipo de selección técnica errónea suele ser más alto que el costo de error de la realización de detalles.

Ese es un modelo de lenguaje n-gram. Ejecutó todos los reconocedores de voz, todos los verificadores de ortografía y todos los sistemas de traducción automática basados en frases desde 1980 hasta 2015.

> Este es el n-gram 语言模型. Desde 1980 hasta 2015, se ejecutó en cada identificador de voz, cada revisor de escritura y cada sistema de traducción automática basado en palabras cortas. Cuando se necesita un dispositivo barato para construir un lenguaje, sigue funcionando.

El problema interesante es qué hacer con los n-gramos no vistos. Un modelo basado en el conteo crudo asigna probabilidad cero a cualquier cosa que no ha visto, lo cual es catastrófico porque las oraciones son largas y casi todas las oraciones largas contienen al menos una secuencia invisible. Cincuenta años de investigación de suavizamiento lo arreglaron.

> La pregunta interesante es: cómo tratar los n-gramos no vistos. El modelo primitivo basado en la cuenta distribuye la probabilidad de cero de cualquier cosa no vista, que es catastrófica, porque las oraciones son largas, casi todas las oraciones largas contienen al menos una secuencia no vista.

## El concepto central.

> **【中文解读】**Este capítulo presenta los conceptos y teorías básicos. La comprensión de estos conceptos es el prerrequisito de la realización posterior de la actividad, y también el conocimiento de los puntos de alta frecuencia de la entrevista y la práctica de la ingeniería.

![N-gram model: count, smooth, generate](../assets/ngram.svg)

### El juego de predicción

Antes de que existiera alguna de estas máquinas, un experimento definió lo que es un modelo de lenguaje. Cubre la siguiente letra de una frase inglesa. Pídale a alguien que adivine, una adivina a la vez, hasta que lo haga bien. Anote el recuento de adivinaciones. Repita por unos cientos de letras.

Los números de adivinanzas no son triviales. Son una recodificación sin pérdidas del texto: entregue la secuencia de recuento a un segundo adivinador idéntico y pueden reconstruir cada letra, porque en cada posición saben exactamente qué adivinan primero. Un mensaje que se puede recodificar en menos símbolos lleva menos información por símbolo, por lo que las estadísticas de adivinanzas ponen un límite a la entropía del inglés.

Shannon hizo esto en 1951 y obtuvo un número que todavía gobierna el campo. Un alfabeto de 27 símbolos (26 letras más espacio) podría llevar`log2(27) ≈ 4.75`Los adivinadores humanos con 100 letras de contexto aterrizaron entre 0,6 y 1,3 bits por letra. el inglés es aproximadamente tres cuartas partes de movimientos forzados. La estructura que un modelo debe aprender se midió antes de que cualquier modelo pudiera aprenderlo.

Cada modelo de lenguaje desde entonces es un jugador mecánico de este juego, y cada número de evaluación en esta lección es el juego anotado:

- **Cross-entropy loss**El entrenamiento de un LM es literalmente minimizar su puntaje en el juego de adivinar.
- **Perplexity**¿ Es verdad ?`2^bits`(o `e^nats`): el factor de ramificación que aún enfrenta el modelo después de su adivinación.
- **Context length is the player's memory.**Un modelo de trigramas juega con dos tokens de memoria. Un transformador juega el mismo juego con 100K tokens. Las reglas nunca cambiaron; el jugador mejoró.

Un cambio de unidad a la pista: los puntajes del juego por letra en bits (`log2`), mientras que las fórmulas n-gramas de abajo ponen por símbolo de palabra en nats (log natural)  y desde la perplejidad `e^H`en nats iguales `2^H`en bits, las dos vistas son la misma medida en diferentes unidades.

```figure
prediction-game
```

**N-gram probability:** `P(w_i | w_{i-n+1}, ..., w_{i-1})`- ¿ Qué ?`n`(normalmente 3 para trigramas, 4 para 4 gramos).

> **N-gram 概率：** `P(w_i | w_{i-n+1}, ..., w_{i-1})`❖ Fija`n`(三元组 normalmente es 3,四元组 es 4)

```text
P(w | context) = count(context, w) / count(context)
```

**The zero-count problem.**Cualquier n-gramo no visto en el entrenamiento obtiene probabilidad cero. Un estudio de 2007 sobre el corpus de Brown encontró que incluso un modelo de 4 gramos tenía el 30% de 4 gramos no vistos en el entrenamiento.

> **零计数问题。** Los n-gramos que no se vieron en cualquier entrenamiento obtuvieron una probabilidad de 0                                                                                                                                                                                                                                                   

**Smoothing approaches, in order of sophistication:**

> **平滑方法，按复杂度排序：**

1. **Laplace (add-one).**Añade 1 a cada cuenta.
   **拉普拉斯（加一）。**Demos a cada cuenta más 1― sencillo, pero en casos raros el efecto es muy malo―
2. **Good-Turing.**Reasignar la masa de probabilidad de eventos de mayor frecuencia a los invisibles basados en la frecuencia de las frecuencias.
   **Good-Turing。**Basado en la frecuencia de la frecuencia, se redistribuirá la calidad de la probabilidad de los eventos de alta frecuencia a los eventos no vistos.
3. **Interpolation.**Combine n-gram, (n-1)-gram, etc., estimaciones con pesos ajustables.
   **插值。**Usado para la evaluación de la cantidad de gramos.
4. **Backoff.**Si n-gram tiene el conteo cero, regresa a (n-1)-gram.
   **回退。**Si n-gram 计数为零, regresa a (n-1)-gram。Katz regresará a su regreso 归化。
5. **Absolute discounting.**Subtraer un descuento fijo `D`de todos los números, redistribuir a lo invisible.
   **绝对折扣。**De todos los contactos deducción de descuentos fijos`D`, reassignar a los hechos no vistos.
6. **Kneser-Ney.**Desconto absoluto más una elección inteligente para el modelo de orden inferior: utilizar *probabilidad de continuación* (cuántos contextos aparece una palabra) en lugar de frecuencia bruta.
   **Kneser-Ney。**绝对折扣加上低阶模型的巧妙选择:使用*续接概率*((un word appears多少上下文中) en lugar de la frecuencia original。

La visión de Kneser-Ney es profunda. "San Francisco" es un gran gramo común. Unigramas "Francisco" aparece principalmente después de "San. " Naive descuento absoluto da "Francisco" alta unicramas probabilidad (porque el conteo es alto). Kneser-Ney observa que "Francisco" aparece en un solo contexto y reduce en consecuencia su probabilidad de continuación. Resultado: un gran gramo que termina en "Francisco" obtiene la probabilidad adecuada.

> Kneser-Ney tiene una visión muy profunda. "San Francisco" es un grupo de dos grupos de la mayoría de los que se encuentran en el mundo.

**Evaluation: perplexity.**El exponente de la probabilidad de registro negativo promedio por palabra en un conjunto de pruebas prolongadas. Más bajo es mejor. Una perplejidad de 100 significa que el modelo es tan confuso como elegiría uniformemente entre 100 palabras.

> **评估：困惑度。**留出测试集 上每字平均负对数似然的指数──越低越好──困惑度 100 significa que el grado de confusión del modelo es equivalente a la media de la selección entre 100 palabras──

```text
perplexity = exp(- (1/N) * Σ log P(w_i | context_i))
```

> **【中文解读】**Este capítulo a través del código de la implementación de algoritmos centrales de cero. Este método "desde cero" puede ayudar a entender el principio detrás del marco, no se encuentra en la caja negra cuando se encuentran problemas.

> **【拓展：大语言模型的工程实践】**Desde GPT hasta ChatGPT, el campo de NLP ha experimentado un cambio de paradigma de "cada tarea entrenar un modelo" a "un modelo resolver todas las tareas". En el proyecto real, la implementación de LLM necesita considerar los problemas de token 限制,延迟,成本, seguridad etc.

> **【拓展：RAG 与企业知识库】**检索增强生成(RAG) es la estructura más popular de las aplicaciones de IA de las empresas actuales: la consulta de usuarios primero se consulta los documentos relacionados, luego se vuelve a buscar los resultados como respuesta a la pregunta de LLM.

> **【拓展：NLP 的多语言挑战】**En todo el mundo hay más de 7000 idiomas, pero los estudios de PNL se centran principalmente en inglés y en una minoría de idiomas.

## Construye y realiza.

> **【中文解读】**Este capítulo a través del código de la implementación de algoritmos centrales de cero. Este método "desde cero" puede ayudar a entender el principio detrás del marco, no se encuentra en la caja negra cuando se encuentran problemas.
```figure
ngram-backoff
```

## Construye el mismo

### Paso 1: cuenta el trigrama

```python
from collections import Counter, defaultdict


def train_ngram(corpus_tokens, n=3):
    ngrams = Counter()
    contexts = Counter()
    for sentence in corpus_tokens:
        padded = ["<s>"] * (n - 1) + sentence + ["</s>"]
        for i in range(len(padded) - n + 1):
            ctx = tuple(padded[i:i + n - 1])
            word = padded[i + n - 1]
            ngrams[ctx + (word,)] += 1
            contexts[ctx] += 1
    return ngrams, contexts


def raw_probability(ngrams, contexts, context, word):
    ctx = tuple(context)
    if contexts.get(ctx, 0) == 0:
        return 0.0
    return ngrams.get(ctx + (word,), 0) / contexts[ctx]
```

La entrada es una lista de oraciones tokenizadas. La salida es n-grama y contextualización contextualizada. `<s>`y `</s>`son límites de oraciones.

> 输入是分词后的句子列表──输出是n-gram 计数和上下文计数──`<s>`Y `</s>`Es el límite de la frase.

### Paso 2: Limpiación de la zona

```python
def laplace_probability(ngrams, contexts, vocab_size, context, word):
    ctx = tuple(context)
    numerator = ngrams.get(ctx + (word,), 0) + 1
    denominator = contexts.get(ctx, 0) + vocab_size
    return numerator / denominator
```

Añade 1 a cada cuenta, pero asigna masa a eventos invisibles, perjudicando también a eventos raros conocidos.

> 给每一个计数加1──平滑但过分分配质量给未见事件,也伤害已知罕见事件──

### Paso 3: Kneser-Ney (bigrama, interpolado)

```python
def kneser_ney_bigram_model(corpus_tokens, discount=0.75):
    unigrams = Counter()
    bigrams = Counter()
    unigram_contexts = defaultdict(set)

    for sentence in corpus_tokens:
        padded = ["<s>"] + sentence + ["</s>"]
        for i, w in enumerate(padded):
            unigrams[w] += 1
            if i > 0:
                prev = padded[i - 1]
                bigrams[(prev, w)] += 1
                unigram_contexts[w].add(prev)

    total_unique_bigrams = sum(len(ctx_set) for ctx_set in unigram_contexts.values())
    continuation_prob = {
        w: len(ctx_set) / total_unique_bigrams for w, ctx_set in unigram_contexts.items()
    }

    context_totals = Counter()
    for (prev, w), count in bigrams.items():
        context_totals[prev] += count

    unique_follow = defaultdict(set)
    for (prev, w) in bigrams:
        unique_follow[prev].add(w)

    def prob(prev, w):
        count = bigrams.get((prev, w), 0)
        denom = context_totals.get(prev, 0)
        if denom == 0:
            return continuation_prob.get(w, 1e-9)
        first_term = max(count - discount, 0) / denom
        lambda_prev = discount * len(unique_follow[prev]) / denom
        return first_term + lambda_prev * continuation_prob.get(w, 1e-9)

    return prob
```

Tres partes móviles.`continuation_prob`La innovación de Kneser-Ney es una de las principales razones de la innovación.`lambda_prev`La probabilidad final es el término principal descuento más el término de continuación ponderado.

> Tres partes de movimiento:`continuation_prob`¿Cómo se puede decir que el nombre de la palabra "Kneser-Ney" es diferente de "Kneser-Ney" en el idioma inglés?`lambda_prev`Es la calidad de la liberación de descuento, para la devolución de los derechos de venta.

### Paso 4: generar texto con muestreo

```python
import random


def generate(prob_fn, vocab, prefix, max_len=30, seed=0):
    rng = random.Random(seed)
    tokens = list(prefix)
    for _ in range(max_len):
        candidates = [(w, prob_fn(tokens[-1], w)) for w in vocab]
        total = sum(p for _, p in candidates)
        r = rng.random() * total
        acc = 0.0
        for w, p in candidates:
            acc += p
            if r <= acc:
                tokens.append(w)
                break
        if tokens[-1] == "</s>":
            break
    return tokens
```

Muestreo proporcional a la probabilidad. Siempre da una salida diferente por semilla. Para la salida similar a la búsqueda de haces, seleccione el argmax en cada paso (compulsivo) y agregue un pequeño botón de aleatoriedad (temperatura).

> 按概率比例采样. △ cada semilla siempre es dado a diferentes sortidos. △ Para similar束搜索的输出, cada paso toma argmax. △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △                                                                                                                       

### Paso 5: perplejidad

```python
import math


def perplexity(prob_fn, sentences):
    total_log_prob = 0.0
    total_tokens = 0
    for sentence in sentences:
        padded = ["<s>"] + sentence + ["</s>"]
        for i in range(1, len(padded)):
            p = prob_fn(padded[i - 1], padded[i])
            total_log_prob += math.log(max(p, 1e-12))
            total_tokens += 1
    return math.exp(-total_log_prob / total_tokens)
```

Para el cuerpo de Brown, un modelo KN de 4 gramos bien ajustado alcanza la perplejidad alrededor de 140. Un transformador LM alcanza 15-30 en el mismo conjunto de prueba. La brecha es de aproximadamente 10 veces. Esa brecha es por lo que el campo se movió.

> 越低越好── Para Brown 语料库, una concentración de cuatro grupos de KN 模型困惑度约140──Transformer 语言模型在同一测试集上达到15-30──差距约10倍──这个差距就是这个领域转向的原因──

> **【中文解读】**Este capítulo muestra cómo utilizar un marco maduro (como PyTorch、HuggingFace, etc.) para aplicar rápidamente esta tecnología. En los proyectos reales, se realiza con prioridad el uso de un marco experimentado, se pueden reducir errores y mejorar la eficiencia de desarrollo.

> **【拓展：Prompt Engineering 与 LLM 应用】**La ingeniería rápida se ha convertido en la habilidad central de los ingenieros de PNL. Desde la Cero-Shot hasta la Few-Shot, desde la Cadena de Pensamiento hasta la Reacción, diferentes estrategias de sugerencias se aplican a diferentes escenarios.

## Usalo con el marco de ejecución

- **Classical NLP teaching.**La exposición más clara a la suavidad, MLE, y la perplejidad que puedes tener.
  **经典 NLP 教学。**La mejor experiencia de la vida que puedas tener.
- **KenLM.**Producción n-gram biblioteca. Se utiliza como un rescensor en el habla y sistemas MT donde baja latencia importa.
  **KenLM。**Clasificación de producción n-gramo 库── Us作低延迟语音和MT 系统的重评分器──
- **On-device autocomplete.**Modelos de trigramas en teclados.
  **设备端自动补全。**Modelo de tres grupos en el teclado.
- **Baselines.**Siempre calcular una perplejidad de LM de n gramos antes de declarar que su LM neuronal es bueno.
  **基线。**En la declaración de tu modelo de lenguaje nervioso bueno, siempre cuentas n gramos de LM 困惑度── Si tu Transformer  no gana en gran medida KN, entonces hay problemas──

> **【中文解读】**Este capítulo se centra en cómo se puede implementar el modelo como producto disponible. Desde el modelo original hasta el sistema de producción, se deben considerar múltiples dimensiones de optimización de rendimiento, tratamiento de errores, control, etc.

## Envíe el producto .

Salvo como`outputs/prompt-lm-baseline.md`¿Qué es esto ?

> 保存为                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           `outputs/prompt-lm-baseline.md`¿Qué es esto ?

```markdown
---
name: lm-baseline
description: Build a reproducible n-gram language model baseline before training a neural LM.
phase: 5
lesson: 16
---

Given a corpus and target use (next-word prediction, rescoring, perplexity baseline), output:

1. N-gram order. Trigram for general English, 4-gram if corpus is large, 5-gram for speech rescoring.
2. Smoothing. Modified Kneser-Ney is the default; Laplace only for teaching.
3. Library. `kenlm` for production, `nltk.lm` for teaching, roll your own only to learn.
4. Evaluation. Held-out perplexity with consistent tokenization between train and test sets.

Refuse to report perplexity computed with different tokenization between systems being compared — perplexity numbers are comparable only under identical tokenization. Flag OOV rate in test set; KN handles OOV poorly unless you reserve a special <UNK> token during training.
```

> **【中文解读】**Practice los temas de fácil/medio/duro  3 difficulty to pass in  Recomenda al menos completar los temas de grado medio  Grado duro  para la preparación de la entrevista

## Los ejercicios.

1. **Easy.**Entrenar un trigramas LM en un corpus de Shakespeare de 1.000 frases. Generar 20 frases. Serán plausibles localmente pero globalmente incoherentes. Esta es la demostración canónica.
   **简单。**En 1000 frases de Shakespeare, el lenguaje de la forma en que se ha escrito el libro es un lenguaje de la forma en que se ha escrito el libro.
2. **Medium.**Implemente la perplejidad para su modelo KN en una división de Shakespeare prolongada. Comparar con Laplace. Usted debería ver la perplejidad KN menor en 30-50%.
   **中等。**En las categorías de Shakespeare que se han dejado, se reduce la confusión entre los 30 y 50% de la población.
3. **Hard.**Construir un corrector de ortografía de trigramas: dada una palabra mal escrita y su contexto, generar correcciones y clasificar por probabilidad de contexto bajo el LM. Evalúa en el corpus de ortografía de Birkbeck (público).
   **困难。**构建三元组拼写纠错器:给定一个拼写错误的词及其上下文,生成纠正并按 LM 下的上下文概率排序──在 Birkbeck 拼写语料库(公开) 上评估──

> **【中文解读】**En el lenguaje de los términos "Lo que la gente dice" vs "Lo que realmente significa" se distingue entre el lenguaje diario y la definición técnica de significado.

## Términos clave .

| Term / 术语 | What people say / 人们常说的 | What it actually means / 实际含义 |
|------|-----------------|-----------------------|
| N-gram | Word sequence / 词序列 | Sequence of `n` consecutive tokens. / `n` 个连续 token 的序列。 |
| Smoothing（平滑） | Avoiding zeros / 避免零 | Reallocating probability mass so unseen events get non-zero probability. / 重新分配概率质量使未见事件获得非零概率。 |
| Perplexity（困惑度） | LM quality metric / LM 质量指标 | `exp(-average log-prob)` on held-out data. Lower is better. / 留出数据上的 `exp(-平均对数概率)`。越低越好。 |
| Backoff（回退） | Fallback to shorter context / 回退到更短上下文 | If trigram count is zero, use bigram. Katz backoff formalizes this. / 如果三元组计数为零，使用二元组。Katz 回退将其形式化。 |
| Kneser-Ney | Best smoothing for n-grams / 最佳 n-gram 平滑 | Absolute discounting + continuation probability for the lower-order model. / 绝对折扣 + 低阶模型的续接概率。 |
| Continuation probability（续接概率） | KN-specific / KN 特有 | `P(w)` weighted by number of contexts `w` appears in, not by raw count. / `P(w)` 按 `w` 出现的上下文数量加权，而非原始计数。 |

> **【中文解读】**延伸阅读 proporciona un alto nivel de recursos para el aprendizaje profundo. Estos artículos y cursos son los referentes clásicos en el campo, adecuados para los lectores que necesitan una comprensión profunda.

## Más Leer más Leer más

- [Jurafsky and Martin — Speech and Language Processing, Chapter 3 (2026 draft)](https://web.stanford.edu/~jurafsky/slp3/3.pdf) el tratamiento canónico de las LM n-gram y el suavización. / n-gram 语言模型和平滑的经典教材──
- [Chen and Goodman (1998). An Empirical Study of Smoothing Techniques for Language Modeling](https://dash.harvard.edu/handle/1/25104739) el papel que estableció Kneser-Ney como el mejor n-gram más suave. / 确定 Kneser-Ney 为最佳 n-gram 平滑器的论文──
- [Kneser and Ney (1995). Improved Backing-off for M-gram Language Modeling](https://ieeexplore.ieee.org/document/479394) el papel KN original. / 原始 KN 论文。
- [KenLM](https://kheafield.com/code/kenlm/) producción rápida n-gram LM, todavía utilizada en 2026 para aplicaciones sensibles a la latencia. / 快速生产级 n-gram 语言模型,2026年仍用于延迟敏感应用──
| N-gram | Word sequence | Sequence of `n` consecutive tokens. |
| Smoothing | Avoiding zeros | Reallocating probability mass so unseen events get non-zero probability. |
| Perplexity | LM quality metric | `exp(-average log-prob)` on held-out data. Lower is better. |
| Backoff | Fallback to shorter context | If trigram count is zero, use bigram. Katz backoff formalizes this. |
| Kneser-Ney | Best smoothing for n-grams | Absolute discounting + continuation probability for the lower-order model. |
| Continuation probability | KN-specific | `P(w)` weighted by number of contexts `w` appears in, not by raw count. |
| Entropy of text | Information per symbol | Average bits needed to encode the next symbol given the context. Shannon's 1951 estimate for printed English with up to 100 letters of context: 0.6-1.3 bits/letter, measured before any model existed. |

## Leer más

- [Shannon (1951). Prediction and Entropy of Printed English](https://www.princeton.edu/~wbialek/rome/refs/shannon_51.pdf) el experimento de juego de adivinación que definió el objetivo que cada modelo de lenguaje todavía optimiza.
- [Jurafsky and Martin — Speech and Language Processing, Chapter 3 (2026 draft)](https://web.stanford.edu/~jurafsky/slp3/3.pdf) el tratamiento canónico de las LM de n gramos y el suavización.
- [Chen and Goodman (1998). An Empirical Study of Smoothing Techniques for Language Modeling](https://dash.harvard.edu/handle/1/25104739) el papel que estableció Kneser-Ney como el mejor n-gramo más suave.
- [Kneser and Ney (1995). Improved Backing-off for M-gram Language Modeling](https://ieeexplore.ieee.org/document/479394) el papel KN original.
- [KenLM](https://kheafield.com/code/kenlm/) LM de producción rápida n-gramos, todavía utilizado en 2026 para aplicaciones sensibles a la latencia.
