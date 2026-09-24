# Etiquetado de POS y Parsado sintáctico.

> La gramática estaba fuera de moda por un tiempo, luego cada LLM necesitaba validar la extracción estructurada, y volvió.
> 语法 alguna vez no fue popular. Más tarde cada LLM 流水线都需要验证结构化抽取, se volvió a hacer.

> **【中文解读】**给每一个词标注词性, analizar la estructura de los idiomas de los idiomas.

**Type:** Build | **类型:** 动手
**Languages:** Python | **语言:** Python
**Prerequisites:** Phase 5 · 01 (Text Processing), Phase 2 · 14 (Naive Bayes) | **前置知识:** Phase 5 · 01（文本处理），Phase 2 · 14（朴素贝叶斯）
**Time:** ~45 minutes | **时间:** ~45 分钟

## El problema es la introducción del problema

La lección 01 prometió que la lemmatización necesita una etiqueta de parte del discurso.`running`Es un verbo, un lemmatizer no puede reducirlo a `run`Sin saberlo .`better`Es un adjetivo, no puede reducirse a `good`¿ Qué ?

> Se trata de un proyecto de ley que se ha desarrollado en el ámbito de la educación y la educación.`running`Sí, sí, sí, sí.`run`✿ no sé ✿`better`Es un término que no puede ser recuperado.`good`¿Qué es eso?

La etiquetación de parte del discurso asigna categorías gramaticales. El análisis sintáctico recupera la estructura de árbol de la oración: qué palabra modifica cuál, qué verbo gobierna cuáles argumentos. La PNL clásica pasó veinte años refinando ambos. Luego el aprendizaje profundo los convirtió en una tarea de clasificación de tokens en la parte superior de un transformador preentrenado, y la comunidad de investigación siguió adelante.

> El compromiso detrás de la promesa es un conjunto de áreas. Entonces, el aprendizaje profundo se dobla para transformar las tareas de la clase.

No la comunidad aplicada. Cada tubería de extracción estructurada todavía utiliza árboles POS y de dependencia bajo el capó. JSON generado por LLM se valida contra restricciones gramaticales.

> 应用界没有──每一个结构化抽取流水线仍在底层使用POS 和依赖树──LLM 生成的JSON 会根据语法约束进行验证──问答系统使用依赖分析来分解查询──机器翻译质量评估器检查分析树的对齐──

Esta lección presenta los tagets, las líneas de base y el punto en el que dejas de implementar desde cero y llamas spaCy.

> 值得了解──本课介绍标签集、基线以及你停止从零实现转而调用空间的节点──

## El concepto central.

> **【中文解读】**Este capítulo presenta los conceptos y teorías básicos. La comprensión de estos conceptos es el prerrequisito de la realización posterior de la actividad, y también el conocimiento de los puntos de alta frecuencia de la entrevista y la práctica de la ingeniería.

**POS tagging**El código de identidad de los símbolos de identidad de los símbolos de identidad de los símbolos de identidad de los símbolos de identidad de identidad de los símbolos de identidad de identidad de los símbolos de identidad de identidad de los símbolos de identidad de identidad de identidad de los símbolos de identidad de identidad de identidad de identidad de identidad de los símbolos de identidad de identidad de identidad de identidad de identidad de identidad de identidad de identidad de identidad de identidad de identidad de identidad de identidad de identidad de identidad de identidad de identidad de identidad de identidad de identidad de identidad de identidad de identidad de identidad de identidad de identidad de identidad de identidad de identidad de identidad de identidad de identidad de identidad de identidad de identidad de identidad de identidad de identidad de identidad de identidad de identidad de identidad de identidad de identidad de identidad de identidad de identidad de identidad de identidad de identidad de identidad de identidad de identidad de identidad de identidad de identidad de identidad de identidad de identidad de identidad de identidad de identidad de identidad de identidad de identidad.**Penn Treebank (PTB)**Tagset es el inglés predeterminado. 36 etiquetas con distinciones el lector casual encuentra inquieto: `NN`nombre singular, `NNS`nombre plural, `NNP`nombre propio singular, `VBD`Verbo pasado tiempo, `VBZ`El verbo 3rd person singular presente, y así sucesivamente.**Universal Dependencies (UD)**Tagset es más grueso (17 etiquetas) y lenguaje-agnóstico; se convirtió en el estándar para el trabajo translingual.

> **词性标注（POS Tagging）**Para cada símbolo 标注语法类别──**Penn Treebank (PTB)**标签集是英语的默认选择──36标签, con el que el lector general considera que hay una diferencia demasiado detallada:`NN`单数名词、`NNS`复数名词, también conocido como`NNP`专名词单数、`VBD`动词过去时,`VBZ`动词第三人称单数现在时等等等──**通用依存（Universal Dependencies, UD）**Se ha convertido en una opción de trabajo translingüístico.

```
The/DET cats/NOUN were/AUX running/VERB at/ADP 3pm/NOUN ./PUNCT
```

**Syntactic parsing**produce un árbol. Dos estilos principales:

> **句法分析（Syntactic Parsing）**产生一棵树──两种主要风格:

- **Constituency parsing.**Las frases de sustantivo, las frases de verbo, las frases prepositivas anidan entre sí.
  **成分分析（Constituency Parsing）。**Nombre de la palabra "n" en el que se encuentra el nombre de la palabra "n" en el que se encuentra el nombre de la palabra "n" en el que se encuentra el nombre de la palabra "n" en el que se encuentra el nombre de la palabra "n" en el que se encuentra el nombre de la palabra "n" en el que se encuentra el nombre de la palabra "n" en el que se encuentra el nombre de la palabra "n" en el que se encuentra el nombre de la palabra "n" en el que se encuentra el nombre de la palabra "n" en el que se encuentra el nombre de la palabra "n" en el que se encuentra el nombre de la palabra "n" en el que se encuentra el nombre de la palabra "n" en el que se encuentra el nombre de la palabra "n" en el que se encuentra el nombre de la palabra "n" en el que se encuentra el nombre de la palabra "n" en el que se encuentra el nombre de la palabra "n" en el que se encuentra el nombre de la palabra "n" en el que se encuentra el nombre de la palabra "n" en el nombre de la palabra "n" en el que se encuentra el nombre de "n" en el nombre de la palabra "n" en el nombre de la palabra "n" en el que se puede añadrar en el nombre de "n" en el nombre de "n" en el nombre de "n" en el nombre de "n" en el nombre de "n" en el nombre de "n" en el nombre de "n" en el nombre de "n" en el nombre de "n" en el nombre de "n" en el nombre de "n" en el nombre de "n" en el nombre de "n "n" en el nombre de "n "n" en el nombre de "n" en el nombre de "n" en el nombre de "n" en el nombre de "n "n "n" en el nombre de "n" en el que se "n" en el nombre de "n" en el nombre de "n "n "n "n" en el "en "en "en "en "en" en el "en" en el que se "en" en el que se puede añadado en el "en "en "en "en" en el "en" en el "en "
- **Dependency parsing.**Cada palabra tiene una sola palabra de cabeza de la que depende, etiquetada con una relación gramatical.
  **依存分析（Dependency Parsing）。**Cada palabra tiene un centro de su dominio, se nota la relación.

La dependencia de análisis ganó en la década de 2010 porque generaliza limpiamente a través de los idiomas, especialmente los de orden de palabras libre.

> 依存分析在2010年代胜出, pues se transpuso a través de la lengua en general, especialmente la lengua en general.

```
running is ROOT
cats is nsubj of running
were is aux of running
at is prep of running
3pm is pobj of at
```

> **【拓展：大语言模型的工程实践】**Desde GPT hasta ChatGPT, el campo de NLP ha experimentado un cambio de paradigma de "cada tarea entrenar un modelo" a "un modelo resolver todas las tareas". En el proyecto real, la implementación de LLM necesita considerar los problemas de token 限制,延迟,成本, seguridad etc.

> **【拓展：RAG 与企业知识库】**检索增强生成(RAG) es la estructura más popular de las aplicaciones de IA de las empresas actuales: la consulta de usuarios primero se consulta los documentos relacionados, luego se vuelve a buscar los resultados como respuesta a la pregunta de LLM.

> **【拓展：NLP 的多语言挑战】**En todo el mundo hay más de 7000 idiomas, pero los estudios de PNL se centran principalmente en inglés y en una minoría de idiomas.

## Construye y realiza.

> **【中文解读】**Este capítulo a través del código de la implementación de algoritmos centrales de cero. Este método "desde cero" puede ayudar a entender el principio detrás del marco, no se encuentra en la caja negra cuando se encuentran problemas.
```figure
pos-tagger
```

```figure
dependency-arcs
```

## Construye el mismo

### Paso 1: línea de base de etiquetas más frecuentes

El etiquetador más estúpido que funciona, para cada palabra, predice la etiqueta que tenía más a menudo en el entrenamiento.

> Por cada palabra, predicción que es la etiqueta más habitual en el entrenamiento.

```python
from collections import Counter, defaultdict


def train_mft(train_examples):
    word_tag_counts = defaultdict(Counter)
    all_tags = Counter()
    for tokens, tags in train_examples:
        for token, tag in zip(tokens, tags):
            word_tag_counts[token.lower()][tag] += 1
            all_tags[tag] += 1
    word_best = {w: c.most_common(1)[0][0] for w, c in word_tag_counts.items()}
    default_tag = all_tags.most_common(1)[0][0]
    return word_best, default_tag


def predict_mft(tokens, word_best, default_tag):
    return [word_best.get(t.lower(), default_tag) for t in tokens]
```

En el corpus de Brown, esta línea de base alcanza una precisión del 85%.

> En la biblioteca de lenguaje de color marrón, esta línea de base alcanza una tasa de precisión de aproximadamente 85%.

### Paso 2: etiqueta de HMM de gran tamaño

Modela la probabilidad conjunta de la secuencia:

> 建模序列的联合概率:

```
P(tags, words) = prod P(tag_i | tag_{i-1}) * P(word_i | tag_i)
```

Dos tablas: probabilidades de transición (tag dada la etiqueta anterior), probabilidades de emisión (tag dada la palabra). Estima ambas desde los recuentos con el suavización de Laplace.

> 两个表:转移概率 (),发射概率 (),发射概率 (),发射概率 (),发射概率 (),发射概率 (),发射概率 (),发射概率 (),发射概率 (),发射概率 (),发射概率 (),发射概率 (),发射概率 (),发射概率 (),发射概率 (),发射概率 (),发射概率 (),发射概率 (),发射概率 (),发射概率 (),发射概率 (),发射概率 (),发射概率 (),发射概率 (),发射概率 (),发射概率 (),发射概率 (),发射概率 (),发射概率 (),发射概率 (),发射概率 (),发射概率 (),发射概率 (),发射概率 (),发射概率 (),发射概率),发射概率 (),发射概率 (),发射) 概率 (),发射概率 (),发射) 概率 (),发射 (),发射) 概率 (),发射) 概率 (),发射 (),发射) 概率 (),发射) 概率 (),发射) 概率 (),发射 (),发射) 概率 (),发射) 概率 (),发射) 概率 (),发射 (),发射) 发射 (),发射) 发射 (),发射) 发射 (),发射) 发射 (发射) 发射) 发射 (),发射) 发射 (发射) 发射 (),发射 (),发射) 发射 (),发射) 发射) 发射 (),发射)

```python
import math


def train_hmm(train_examples, alpha=0.01):
    transitions = defaultdict(Counter)
    emissions = defaultdict(Counter)
    tags = set()
    vocab = set()

    for tokens, ts in train_examples:
        prev = "<BOS>"
        for token, tag in zip(tokens, ts):
            transitions[prev][tag] += 1
            emissions[tag][token.lower()] += 1
            tags.add(tag)
            vocab.add(token.lower())
            prev = tag
        transitions[prev]["<EOS>"] += 1

    return transitions, emissions, tags, vocab


def log_prob(table, given, key, smooth_denom, alpha):
    return math.log((table[given].get(key, 0) + alpha) / smooth_denom)


def viterbi(tokens, transitions, emissions, tags, vocab, alpha=0.01):
    tags_list = list(tags)
    n = len(tokens)
    V = [[0.0] * len(tags_list) for _ in range(n)]
    back = [[0] * len(tags_list) for _ in range(n)]

    for j, tag in enumerate(tags_list):
        em_denom = sum(emissions[tag].values()) + alpha * (len(vocab) + 1)
        tr_denom = sum(transitions["<BOS>"].values()) + alpha * (len(tags_list) + 1)
        tr = log_prob(transitions, "<BOS>", tag, tr_denom, alpha)
        em = log_prob(emissions, tag, tokens[0].lower(), em_denom, alpha)
        V[0][j] = tr + em
        back[0][j] = 0

    for i in range(1, n):
        for j, tag in enumerate(tags_list):
            em_denom = sum(emissions[tag].values()) + alpha * (len(vocab) + 1)
            em = log_prob(emissions, tag, tokens[i].lower(), em_denom, alpha)
            best_prev = 0
            best_score = -1e30
            for k, prev_tag in enumerate(tags_list):
                tr_denom = sum(transitions[prev_tag].values()) + alpha * (len(tags_list) + 1)
                tr = log_prob(transitions, prev_tag, tag, tr_denom, alpha)
                score = V[i - 1][k] + tr + em
                if score > best_score:
                    best_score = score
                    best_prev = k
            V[i][j] = best_score
            back[i][j] = best_prev

    last_best = max(range(len(tags_list)), key=lambda j: V[n - 1][j])
    path = [last_best]
    for i in range(n - 1, 0, -1):
        path.append(back[i][path[-1]])
    return [tags_list[j] for j in reversed(path)]
```

Bigram HMM en Brown alcanza ~93% de precisión. El salto del 85% al 93% es principalmente probabilidades de transición  el modelo aprende `DET NOUN`es común y `NOUN DET`Es raro.

> En el brown 语料库上二元组 HMM  alcanzó aproximadamente el 93% de la precisión de la tasa.`DET NOUN`Es habitual y`NOUN DET`Es raro.

### Paso 3: por qué los taggers modernos superan esto

Las probabilidades de transición + emisiones son locales.`saw`es un sustantivo en "compré una sierra" pero un verbo en "vi la película". Un CRF con características arbitrarias (sufijo, forma de palabra, palabra antes y después, palabra misma) alcanza ~97%. Un BiLSTM-CRF o transformador alcanza ~98%+.

> 转移 + 发射概率是局部的──它们 no pueden captar `saw`En "compré una sierra" entre es el nombre de palabra pero en "Vi la película" entre es el movimiento de palabra.

El límite de esta tarea se establece por el desacuerdo de los anotadores.

> El plan de este trabajo fue decidido por los marcadores. Los marcadores humanos en Penn Treebank alcanzaron un acuerdo en aproximadamente el 97% del tiempo.

### Paso 4: boceto de análisis de dependencias

La dependencia completa del análisis desde cero está fuera de alcance; el tratamiento de los libros de texto canónicos está en Jurafsky y Martin.

> Desde el principio de la realización completa de la dependencia de análisis, el análisis de la dependencia de la comprensión de la comprensión de la comprensión de la comprensión de la comprensión de la comprensión de la comprensión de la comprensión de la comprensión de la comprensión de la comprensión de la comprensión de la comprensión de la comprensión de la comprensión de la comprensión de la comprensión de la comprensión de la comprensión de la comprensión de la comprensión de la comprensión de la comprensión de la comprensión de la comprensión de la comprensión de la comprensión de la comprensión de la comprensión de la comprensión de la comprensión de la comprensión de la comprensión de la comprensión de la comprensión de la comprensión de la comprensión de la comprensión de la comprensión de la comprensión de la comprensión de la comprensión de la comprensión de la comprensión de la comprensión de la comprensión de la comprensión de la comprensión de la comprensión de la comprensión de la comprensión de la comprensión de la comprensión de la comprensión de la comprensión de la comprensión de la comprensión de la comprensión de la comprensión de la comprensión de la comprensión de la comprensión de la comprensión de la comprensión de la comprensión de la comprensión de la comprensión de la comprensión de la comprensión de la comprensión de la comprensión de la comprensión de la comprensión de la comprensión de la comprensión de la comprensión de la comprensión de la comprensión de la comprensión de la comprensión de la comprensión de la comprensión de la comprensión de la comprensión de la comprensión de la comprensión de la comprensión de la comprensión de la comprensión de la comprensión de la comprensión de la comprensión de la comprensión de la comprensión.

- **Transition-based**Los parser (arc-eager, arc-standard) actúan como un parser de reducción de cambios: leen tokens, los desplazan a una pila y aplican acciones de reducción que crean arcos. La codificación codificada es rápida. La implementación clásica es MaltParser.
  **基于转移的**解析器(arc-eager、arc-standard) Como el movimiento hacia el movimiento hacia el movimiento hacia el movimiento hacia el movimiento hacia el movimiento hacia el movimiento hacia el movimiento hacia el movimiento hacia el movimiento hacia el movimiento hacia el movimiento hacia el movimiento hacia el movimiento hacia el movimiento hacia el movimiento hacia el movimiento hacia el movimiento hacia el movimiento hacia el movimiento hacia el movimiento hacia el movimiento hacia el movimiento hacia el movimiento hacia el movimiento hacia el movimiento hacia el movimiento hacia el movimiento hacia el movimiento hacia el movimiento hacia el movimiento hacia el movimiento hacia el movimiento hacia el movimiento hacia el movimiento hacia el movimiento hacia el movimiento hacia el movimiento hacia el movimiento hacia el movimiento hacia el movimiento hacia el movimiento hacia el movimiento hacia el movimiento hacia el movimiento hacia el movimiento hacia el movimiento hacia el movimiento hacia el movimiento hacia el movimiento hacia el movimiento hacia el movimiento hacia el movimiento hacia el movimiento hacia el movimiento hacia el movimiento hacia el movimiento hacia el movimiento hacia el movimiento hacia el movimiento hacia el movimiento hacia el movimiento hacia el movimiento hacia el movimiento hacia el movimiento hacia el movimiento hacia el movimiento hacia el movimiento hacia el movimiento hacia el movimiento hacia el movimiento hacia el movimiento hacia el movimiento hacia el movimiento hacia el movimiento hacia el movimiento hacia el movimiento hacia el movimiento hacia el movimiento hacia el movimiento hacia el movimiento hacia el movimiento hacia el movimiento hacia el movimiento hacia el movimiento hacia el movimiento hacia el movimiento hacia el movimiento hacia el movimiento hacia el movimiento hacia el movimiento hacia el movimiento hacia el movimiento hacia el movimiento hacia hacia hacia el movimiento hacia el movimiento hacia el movimiento hacia el movimiento hacia hacia hacia el movimiento hacia el movimiento hacia el movimiento hacia hacia hacia hacia el movimiento hacia hacia hacia hacia el movimiento hacia hacia hacia hacia el movimiento hacia hacia el movimiento hacia hacia el movimiento hacia hacia hacia hacia el movimiento hacia el movimiento hacia hacia hacia hacia hacia el movimiento hacia hacia hacia hacia hacia hacia el movimiento hacia hacia hacia hacia hacia hacia el movimiento hacia hacia hacia hacia hacia el más hacia el más hacia el más hacia el más hacia el más hacia el
- **Graph-based**Los parseres (algorithmo de Eisner, Dozat-Manning biafina) anotan todos los bordes posibles dependientes de la cabeza y eligen el árbol de mayor extensión.
  **基于图的**解析器(Eisner 算法、Dozat-Manning 双仿射) a cada posible de cabeza dependiente 边打分, seleccionar el máximo generar árbol。

Para la mayoría de los trabajos aplicados, llame a espaCy:

>  Para la mayoría de las aplicaciones, se utiliza espaci:

```python
import spacy

nlp = spacy.load("en_core_web_sm")
doc = nlp("The cats were running at 3pm.")
for token in doc:
    print(f"{token.text:10s} tag={token.tag_:5s} pos={token.pos_:6s} dep={token.dep_:10s} head={token.head.text}")
```

```
The        tag=DT    pos=DET    dep=det        head=cats
cats       tag=NNS   pos=NOUN   dep=nsubj      head=running
were       tag=VBD   pos=AUX    dep=aux        head=running
running    tag=VBG   pos=VERB   dep=ROOT       head=running
at         tag=IN    pos=ADP    dep=prep       head=running
3pm        tag=NN    pos=NOUN   dep=pobj       head=at
.          tag=.     pos=PUNCT  dep=punct      head=running
```

Lea el `dep`columna de abajo a arriba y la estructura gramatical de la oración cae.

> Desde abajo hacia arriba`dep`列,句子的语法结构就自然呈现了──

> **【中文解读】**Este capítulo muestra cómo utilizar un marco maduro (como PyTorch、HuggingFace, etc.) para aplicar rápidamente esta tecnología. En los proyectos reales, se realiza con prioridad el uso de un marco experimentado, se pueden reducir errores y mejorar la eficiencia de desarrollo.

> **【拓展：Prompt Engineering 与 LLM 应用】**La ingeniería rápida se ha convertido en la habilidad central de los ingenieros de PNL. Desde la Cero-Shot hasta la Few-Shot, desde la Cadena de Pensamiento hasta la Reacción, diferentes estrategias de sugerencias se aplican a diferentes escenarios.

## Usalo con el marco de ejecución

Cada biblioteca de producción de PNL envía los puntos de venta y los parseres de dependencia como parte de una tubería estándar.

> Cada producción de PNL 库都把 POS 和依赖解析器 como parte de la línea de flujo de agua estándar proporcionado.

- **spaCy**(El artículo`en_core_web_sm`- ¿ Qué ?`md`- ¿ Qué ?`lg`- ¿ Qué ?`trf` Rapido, preciso, integrado con tokenization + NER + lemmatization. `token.tag_`¿ Qué es esto ?`token.pos_`(UD), `token.dep_`(relación de dependencia).
  **spaCy**(El artículo`en_core_web_sm`- ¿ Qué ?`md`- ¿ Qué ?`lg`- ¿ Qué ?`trf`)──快速、准确,与分词 + NER + 词形还原集成──`token.tag_`¿Qué es eso?`token.pos_`(UD)`token.dep_`(dependencia)
- **Stanford NLP (stanza)**. el sucesor de Stanford a CoreNLP. Estado de la técnica en más de 60 idiomas.
  **Stanford NLP (stanza)**❖ Recurrentes de Stanford CoreNLP ❖ En más de 60 idiomas alcanzaron un nivel avanzado ❖
- **trankit**- Basado en transformador, buena precisión UD.
  **trankit**❖ Basado en el Transformer, buena tasa de precisión ❖
- **NLTK**- ¿ Qué ?`pos_tag`- Útil, lento, más viejo, bueno para enseñar.
  **NLTK**¿Qué es eso?`pos_tag`△可用、慢、较旧──适合教学──

### Cuando esto todavía importa en 2026

- **Lemmatization.**La lección 01 necesita que el POS se lematice correctamente.
  **词形还原。**Se trata de un proyecto de investigación que se desarrolla en el ámbito de la salud y de la salud.
- **Structured extraction from LLM outputs.**Validar que una oración generada respete restricciones gramaticales (por ejemplo, acuerdo entre objeto y verbo, modificadores requeridos).
  **LLM 输出的结构化抽取。**验证生成的句子满足语法约束 (en inglés)
- **Aspect-based sentiment.**Los pares de dependencia te dicen qué adjetivo modifica qué sustantivo.
  **基于方面的情感分析。** depende análisis te dice cuál es el nombre de la palabra 
- **Query understanding.**"Las películas dirigidas por Wes Anderson con Bill Murray" se descomponen en restricciones estructuradas a través del análisis.
  **查询理解。**"filmes dirigidos por Wes Anderson y protagonizados por Bill Murray"
- **Cross-lingual transfer.**Las etiquetas UD y las relaciones de dependencia son agnósticas del lenguaje, lo que permite un análisis estructurado de cero disparos de nuevos idiomas.
  **跨语言迁移。**UD 标签和依赖与语言无关,支持新语言的零样本结构化分析──
- **Low-compute pipelines.**Si no puedes enviar un transformador, POS + dependencia parse + gazetteer te lleva sorprendentemente lejos.
  **低算力流水线。**Si no puedes desplegar el Transformer, POS + 依存分析 + 地名词典能让你走相当远――

> **【中文解读】**Este capítulo se centra en cómo se puede implementar el modelo como producto disponible. Desde el modelo original hasta el sistema de producción, se deben considerar múltiples dimensiones de optimización de rendimiento, tratamiento de errores, control, etc.

## Envíe el producto .

Salvo como`outputs/skill-grammar-pipeline.md`¿Qué es esto ?

> 保存为                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           `outputs/skill-grammar-pipeline.md`¿Qué es esto ?

```markdown
---
name: grammar-pipeline
description: Design a classical POS + dependency pipeline for a downstream NLP task.
version: 1.0.0
phase: 5
lesson: 07
tags: [nlp, pos, parsing]
---

Given a downstream task (information extraction, rewrite validation, query decomposition, lemmatization), you output:

1. Tagset to use. Penn Treebank for English-only legacy pipelines, Universal Dependencies for multilingual or cross-lingual.
2. Library. spaCy for most production, stanza for academic-grade multilingual, trankit for highest UD accuracy. Name the specific model ID.
3. Integration pattern. Show the 3-5 lines that call the library and consume the needed attributes (`.pos_`, `.dep_`, `.head`).
4. Failure mode to test. Noun-verb ambiguity (`saw`, `book`, `can`) and PP-attachment ambiguity are the classical traps. Sample 20 outputs and eyeball.

Refuse to recommend rolling your own parser. Building parsers from scratch is a research project, not an application task. Flag any pipeline that consumes POS tags without handling lowercase/uppercase variants as fragile.
```

> **【中文解读】**Practice los temas de fácil/medio/duro  3 difficulty to pass in  Recomenda al menos completar los temas de grado medio  Grado duro  para la preparación de la entrevista

## Los ejercicios.

1. **Easy.**Usando la línea de base de etiquetas más frecuentes en un corpus pequeño etiquetado (por ejemplo, el subconjunto Brown de NLTK), mide la precisión en las oraciones retrasadas. Verifique el resultado de ~ 85%.
   **简单。**En un pequeño material de etiquetado (como el NLTK Brown 子集) se utiliza con mayor frecuencia en el etiquetado, la medición de la precisión en las frases de la frase es de aproximadamente el 85% de los resultados.
2. **Medium.**Entrenar el HMM de gran tamaño arriba y informar la precisión / recuperación por etiqueta. ¿Qué etiquetas confunden más el HMM?
   **中等。**訓練上述二元组 HMM 并报告每标签精确率/召回率──HMM ¿Qué étiquetas son las más fáciles de confundir?
3. **Hard.**Utilice el análisis de dependencias de spaCy para extraer triples de sujeto-verbo-objeto de una muestra de 1000 frases. Evalúe en 50 triples etiquetados manualmente. Documento donde la extracción falla (a menudo pasivos, coordenadas y sujetos eliminados).
   **困难。**Utiliza la dependencia de análisis de espaCy de 1000 ejemplos de ejemplos para extraer el principal denominado de tres grupos de 50 marcas manuales.

> **【中文解读】**En el lenguaje de los términos "Lo que la gente dice" vs "Lo que realmente significa" se distingue entre el lenguaje diario y la definición técnica de significado.

## Términos clave .

| Term / 术语 | What people say / 人们常说的 | What it actually means / 实际含义 |
|------|-----------------|-----------------------|
| POS tag（词性标签） | Word's type / 词的类型 | Grammatical category. PTB has 36; UD has 17. / 语法类别。PTB 有 36 个；UD 有 17 个。 |
| Penn Treebank | Standard tagset / 标准标签集 | English-specific. Fine-grained verb tenses and noun number. / 特定于英语。细粒度的动词时态和名词数。 |
| Universal Dependencies（通用依存） | Multilingual tagset / 多语言标签集 | Coarser than PTB; language-neutral; defaults for cross-lingual work. / 比 PTB 更粗；语言无关；跨语言工作的默认选择。 |
| Dependency parse（依存分析） | Sentence tree / 句子树 | Each word has one head, each edge has a grammatical relation. / 每个词有一个中心词，每条边有一个语法关系。 |
| Viterbi（维特比算法） | Dynamic programming / 动态规划 | Finds the highest-probability tag sequence given emissions and transitions. / 给定发射和转移概率，找到最高概率的标签序列。 |

> **【中文解读】**延伸阅读 proporciona un alto nivel de recursos para el aprendizaje profundo. Estos artículos y cursos son los referentes clásicos en el campo, adecuados para los lectores que necesitan una comprensión profunda.

## Más Leer más Leer más

- [Jurafsky and Martin — Speech and Language Processing, chapters 8 and 18](https://web.stanford.edu/~jurafsky/slp3/) el tratamiento canónico de libros de texto de POS y parsing. / POS 和解析的经典教科书处理──
- [Universal Dependencies project](https://universaldependencies.org/) el conjunto de etiquetas y la colección de árboles interlingualmente utilizados por cada parser multilingüe. / 每个多语言解析器使用的跨语言标签集和树库集合。
- [spaCy linguistic features guide](https://spacy.io/usage/linguistic-features) referencia práctica para cada atributo expuesto en `Token`- ¿ Qué ?`Token`Referencia práctica de cada una de las características de la exposición anterior.
- [Chen and Manning (2014). A Fast and Accurate Dependency Parser using Neural Networks](https://nlp.stanford.edu/pubs/emnlp2014-depparser.pdf) el artículo que trajo los parseros neuronales a la corriente principal. / 将神经解析器带入主流的论文──
