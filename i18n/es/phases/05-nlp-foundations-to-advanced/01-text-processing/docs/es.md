# Procesamiento de texto  Tokenization, Stemming, Lemmatization  文本处理  分词、词干提取、词形還原

> El lenguaje es continuo, los modelos son discretos, el preprocesamiento es el puente.
> El lenguaje es continuo. El modelo es dispersado.

> **【中文解读】**La primera etapa de la PNL es la de la PNL: la de la PNL.

**Type:** Build | **类型:** 动手
**Languages:** Python | **语言:** Python
**Prerequisites:** Phase 2 · 14 (Naive Bayes) | **前置知识:** Phase 2 · 14（朴素贝叶斯）
**Time:** ~45 minutes | **时间:** ~45 分钟

## Objetivos de aprendizaje

- Comprender la tokenización, el derivado y la lemmatización como operaciones de preprocesamiento distintas
  Comprender分词、词干提取和词形还原 como diferentes operaciones de pre-procesamiento
- Construir un tokenizer regex, un paso de Porter votadores, y un lemmatizer basado en búsqueda desde cero
  Desde零 construcción de la norma de la palabra separador, el portavoz de la palabra, el proceso de la palabra extracción y el proceso de la palabra en el orden de la letra
- Comparar NLTK y spaCy para las tuberías de preprocesamiento de producción
  Comparado con NLTK y espaCy en la producción preprocesamiento flujo de agua
- Reconocer las dos fallas de producción más comunes: la deriva de reproducibilidad y la discrepancia entre tren e interferencia
  Identificación de dos tipos de fallas de producción más comunes:

## El problema es la introducción del problema

Un modelo no puede leer "Los gatos corrían".

> 模型不能直接读取 "Los gatos corrían".

Cada sistema de PNL se abre con las mismas tres preguntas. ¿Dónde comienza una palabra? ¿Cuál es la raíz de la palabra? ¿Cómo tratamos "correr", "correr", "correr" como lo mismo cuando ayuda, y como cosas diferentes cuando no lo hace?

> Cada sistema de PNL debe responder a las mismas tres preguntas: ¿de dónde comienza un palabra? ¿Cuál es la raíz de este palabra? ¿cómo vamos a "corrir" cuando se necesita, "corrir" cuando se necesita, "corrir" cuando se ve como la misma cosa, y cuando no se necesita otra diferencia de trato?

Si se equivoca en la tokenización, el modelo aprende de la basura.`don't`Como una señal , pero`do n't`Si el voto se derrumba, el equipo de entrenamiento se divide.`organization`y `organ`Si su lemmatizer necesita un contexto de parte del habla pero no lo pasa, los verbos se tratan como sustantivos.

> Se ha hecho un error, el modelo se aprende de la basura de datos.`don't`Como un símbolo, pero lo haces.`do n't`Cuando se hace dos, la formación se divide. Si tu palabra se hace extractor.`organization`Y `organ`结为同一个词干,主题建模就会失效──如果你的词形还原器需要词性上下文但你没有传入,动词就会被当作名词处理──

Esta lección construye los tres pasos de preprocesamiento desde cero, luego muestra cómo NLTK y spaCy hacen el mismo trabajo para que pueda ver las compensaciones.

> Este curso se desarrolla desde cero en estos tres pasos de preprocesamiento, y luego muestra cómo hacer el mismo trabajo en NLTK y espaCy, dejándote ver el peso de ellos.

## El concepto central.

> **【中文解读】**Este capítulo presenta los conceptos y teorías básicos. La comprensión de estos conceptos es el prerrequisito de la realización posterior de la actividad, y también el conocimiento de los puntos de alta frecuencia de la entrevista y la práctica de la ingeniería.

Tres operaciones, cada una tiene un trabajo y un modo de falla.

> Tres operaciones, cada uno tiene su propio deber y su propio modelo de fracaso.

**Tokenization**"Token" es deliberadamente vago porque la granularidad correcta depende de la tarea. nivel de palabra para la PNL clásica. Subpalabra para transformadores. carácter para idiomas sin espacio en blanco.

> **分词（Tokenization）**La palabra "Token" es un término que tiene la intención de mantenerse confuso, ya que la granosidad de la adaptación depende de la tarea específica.

**Stemming**Las cortes son sufijos con reglas, rápidas, agresivas, estúpidas.`running -> run`- ¿ Qué ?`organization -> organ`El segundo es el modo de falla.

> **词干提取（Stemming）**Uso de la norma de corte después de la corte.`running -> run`¿Qué es eso?`organization -> organ`. Segundo ejemplo es su modelo de fracaso.

**Lemmatization**La definición de un término es más rápida y precisa, pero necesita una tabla de búsqueda o un analizador morfológico.`ran -> run`(necesita saber que "run" es pasado de tiempo de "run").`better -> good`(necesita conocer formas comparativas).

> **词形还原（Lemmatization）**Utilizando el conocimiento de los idiomas, los idiomas se vuelven a utilizar en forma de idiomas.`ran -> run`(Necesita saber que "corrido" es "corrido" del pasado)`better -> good`(Necesita saber la forma de comparación)

Regla de pulgar. Semeja cuando la velocidad es importante y puedes tolerar el ruido (indexación de búsqueda, clasificación aproximada). Lemmatiza cuando el significado es importante (respuesta a preguntas, búsqueda semántica, cualquier cosa que el usuario lea).

> 经验法则: Cuando la velocidad es importante y puede tolerar el ruido, utiliza el término "search" (en inglés) 

> **【拓展：大语言模型的工程实践】**Desde GPT hasta ChatGPT, el campo de NLP ha experimentado un cambio de paradigma de "cada tarea entrenar un modelo" a "un modelo resolver todas las tareas". En el proyecto real, la implementación de LLM necesita considerar los problemas de token 限制,延迟,成本, seguridad etc.

> **【拓展：RAG 与企业知识库】**检索增强生成(RAG) es la estructura más popular de las aplicaciones de IA de las empresas actuales: la consulta de usuarios primero se consulta los documentos relacionados, luego se vuelve a buscar los resultados como respuesta a la pregunta de LLM.

> **【拓展：NLP 的多语言挑战】**En todo el mundo hay más de 7000 idiomas, pero los estudios de PNL se centran principalmente en inglés y en una minoría de idiomas.

## Construye y realiza.

> **【中文解读】**Este capítulo a través del código de la implementación de algoritmos centrales de cero. Este método "desde cero" puede ayudar a entender el principio detrás del marco, no se encuentra en la caja negra cuando se encuentran problemas.
```figure
edit-distance
```

## Construye el mismo

### Paso 1: un tokenizer de palabras regex

El tokenizer más simple y útil se divide en caracteres no alfanuméricos, manteniendo la puntuación como sus propios tokens.

> El más simple es que el código se puede usar en forma independiente.

```python
import re

def tokenize(text):
    return re.findall(r"[A-Za-z]+(?:'[A-Za-z]+)?|[0-9]+|[^\sA-Za-z0-9]", text)
```

Tres patrones en orden de precedencia.`don't`¿ Qué ?`it's`Cualquier carácter no alfanumérico que no sea blanco como símbolo independiente (puntuación).

> Tres palabras en la lista de prioridades`don't`¿Qué es esto?`it's`)。Purón número。 Cualquier único símbolo numérico no blanco como símbolo independiente (标点符号)。

```python
>>> tokenize("The cats weren't running at 3pm.")
['The', 'cats', "weren't", 'running', 'at', '3', 'pm', '.']
```

Modo de falla para detectar. `3pm`Se divide en `['3', 'pm']`porque alteramos entre las cartas y las cifras. Lo suficiente para la mayoría de las tareas. URL, correos electrónicos, hashtags se rompen. Para la producción, añadir patrones antes de los generales.

> 需要注意的失败模式──`3pm`Fue desprendido.`['3', 'pm']`, porque hemos hecho el intercambio entre la secuencia de letras y la secuencia de números. Para la mayoría de las tareas es suficiente.

### Paso 2: un Porter stemmer (solo el paso 1a)

El algoritmo completo de Porter tiene cinco fases de reglas. El paso 1a solo cubre los sufijos ingleses más frecuentes y enseña el patrón.

> El algoritmo completo de Porter tiene cinco etapas de reglas. Sólo el paso 1a cubre el más común de los idiomas ingleses, y muestra el modelo de reglas.

```python
def stem_step_1a(word):
    if word.endswith("sses"):
        return word[:-2]
    if word.endswith("ies"):
        return word[:-2]
    if word.endswith("ss"):
        return word
    if word.endswith("s") and len(word) > 1:
        return word[:-1]
    return word
```

```python
>>> [stem_step_1a(w) for w in ["caresses", "ponies", "caress", "cats"]]
['caress', 'poni', 'caress', 'cat']
```

Lea las reglas de arriba hacia abajo.`ies -> i`La regla es por qué .`ponies -> poni`No , no .`pony`El verdadero Porter tiene el paso 1B que lo arreglaría las reglas compiten las reglas anteriores ganan el orden importa más que cualquier regla

> Desde arriba hasta abajo...`ies -> i`规则是 `ponies -> poni`En vez de`pony`La verdadera teoría de Porter tiene un paso 1b para solucionar este problema. Las reglas compiten entre sí, las reglas vencen en la primera línea.

### Paso 3: un lemmatizer basado en búsqueda

La limmatización adecuada necesita morfología. Una versión de enseñanza manejable utiliza una pequeña tabla de lemma y un fallback.

> Una versión práctica de la enseñanza utiliza un pequeño vocabulario y estrategia de preparación.

```python
LEMMA_TABLE = {
    ("running", "VERB"): "run",
    ("ran", "VERB"): "run",
    ("runs", "VERB"): "run",
    ("better", "ADJ"): "good",
    ("best", "ADJ"): "good",
    ("cats", "NOUN"): "cat",
    ("cat", "NOUN"): "cat",
    ("were", "VERB"): "be",
    ("was", "VERB"): "be",
    ("is", "VERB"): "be",
}

def lemmatize(word, pos):
    key = (word.lower(), pos)
    if key in LEMMA_TABLE:
        return LEMMA_TABLE[key]
    if pos == "VERB" and word.endswith("ing"):
        return word[:-3]
    if pos == "NOUN" and word.endswith("s"):
        return word[:-1]
    return word.lower()
```

```python
>>> lemmatize("running", "VERB")
'run'
>>> lemmatize("cats", "NOUN")
'cat'
>>> lemmatize("better", "ADJ")
'good'
>>> lemmatize("watched", "VERB")
'watched'
```

El último caso es el momento clave de enseñanza.`watched`No está en nuestra mesa y nuestra caída sólo maneja .`ing`La lematización real cubre`ed`, verbos irregulares, adjetivos comparativos, plurales con cambios de sonido (`children -> child`Es por ello que los sistemas de producción utilizan WordNet, el morfologizador de spaCy, o un analizador morfológico completo.

> El último ejemplo es el momento clave de la enseñanza.`watched`No está en nuestra lista, pero nuestra estrategia de reserva sólo se trata.`ing`◊ verdadera palabra forma`ed`、不规则动词、比较级形容词、语音变化的复数(`children -> child`)― es por eso que el sistema de producción utiliza el analista de forma de WordNet, espaCy o el analista de forma completo―

### Paso 4: enchufarlos juntos

```python
def preprocess(text, pos_tagger=None):
    tokens = tokenize(text)
    stems = [stem_step_1a(t.lower()) for t in tokens]
    tags = pos_tagger(tokens) if pos_tagger else [(t, "NOUN") for t in tokens]
    lemmas = [lemmatize(word, pos) for word, pos in tags]
    return {"tokens": tokens, "stems": stems, "lemmas": lemmas}
```

> **【中文解读】**Este capítulo muestra cómo utilizar un marco maduro (como PyTorch、HuggingFace, etc.) para aplicar rápidamente esta tecnología. En los proyectos reales, se realiza con prioridad el uso de un marco experimentado, se pueden reducir errores y mejorar la eficiencia de desarrollo.

La pieza que falta es un etiquetador de POS. Fase 5 · 07 (POS Tagging) construye uno. Por ahora, por defecto todo a `NOUN`y reconocer la limitación.

> 缺少的部分是词性标注器──Phase 5 · 07(词性标注) se construirá una──`NOUN`, no reconoce esta limitación.

> **【拓展：Prompt Engineering 与 LLM 应用】**La ingeniería rápida se ha convertido en la habilidad central de los ingenieros de PNL. Desde la Cero-Shot hasta la Few-Shot, desde la Cadena de Pensamiento hasta la Reacción, diferentes estrategias de sugerencias se aplican a diferentes escenarios.

## Usalo con el marco de ejecución

NLTK y spaCy envían las versiones de producción.

> NLTK y spaCy ofrecieron una versión de producción de clase.

### NLTK

```python
import nltk
nltk.download("punkt_tab")
nltk.download("wordnet")
nltk.download("averaged_perceptron_tagger_eng")

from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer, WordNetLemmatizer
from nltk import pos_tag

text = "The cats were running."
tokens = word_tokenize(text)
stems = [PorterStemmer().stem(t) for t in tokens]
lemmatizer = WordNetLemmatizer()
tagged = pos_tag(tokens)


def nltk_pos_to_wordnet(tag):
    if tag.startswith("V"):
        return "v"
    if tag.startswith("J"):
        return "a"
    if tag.startswith("R"):
        return "r"
    return "n"


lemmas = [lemmatizer.lemmatize(t, nltk_pos_to_wordnet(tag)) for t, tag in tagged]
```

`word_tokenize`maneja contracciones, Unicode, casos de borde que su regex pierde.`PorterStemmer`Se ejecuta en las cinco fases.`WordNetLemmatizer`Necesita la etiqueta POS traducida del esquema Penn Treebank de NLTK al conjunto de abreviaturas de WordNet.

> `word_tokenize`处理缩写、Unicode 和你的正则表达式遗漏的边界情况──`PorterStemmer`¿Qué es esto?`WordNetLemmatizer`需要将 NLTK Penn Treebank 词性标注方案转换为 WordNet 的缩写集──以上的转换代码是大多数教程跳过的部分──

### el espacio

```python
import spacy

nlp = spacy.load("en_core_web_sm")
doc = nlp("The cats were running.")

for token in doc:
    print(token.text, token.lemma_, token.pos_)
```

```
The      the     DET
cats     cat     NOUN
were     be      AUX
running  run     VERB
.        .       PUNCT
```

spaCy esconde toda la tubería detrás.`nlp(text)`La tokenización, etiquetado de POS y lematización funcionan todos. Más rápido que NLTK en escala. Más preciso fuera de la caja. La compensación es que no se puede cambiar fácilmente componentes individuales.

> El espacio se esconde en todo el flujo de agua.`nlp(text)`背后──分词、词性标注和词形还原全部运行── en gran escala bajo NLTK, más rápido, la caja abierta es con más precisión──代价是你不能轻松替换单个组件──

### ¿Cuándo elegir cuál

| Situation | Pick | 场景 | 选择 |
|-----------|------|------|------|
| Teaching, research, swapping components | NLTK | 教学、研究、需要替换组件 | NLTK |
| Production, multi-language, speed matters | spaCy | 生产环境、多语言、速度要求高 | spaCy |
| Transformer pipeline (you'll tokenize with the model's tokenizer anyway) | Use `tokenizers` / `transformers` and skip classical preprocessing | Transformer 流水线（反正你会用模型自带的分词器） | 使用 `tokenizers` / `transformers`，跳过经典预处理 |

### Los dos modos de fracaso nadie te advierte

La mayoría de los tutoriales enseñan los algoritmos y se detienen. Dos cosas mordrán una verdadera tubería de preprocesamiento, y casi nunca se cubren.

> La mayoría de los cursos de aprendizaje de algoritmos se han detenido. Hay dos problemas que afectan al verdadero flujo de tratamiento previo, y casi nunca se mencionan.

**Reproducibility drift.**NLTK y spaCy cambian el comportamiento de tokenización y lemmatizer entre versiones.`['do', "n't"]`en spaCy 2.x puede producir `["don't"]`En 3.x, tu modelo fue entrenado en una distribución. la inferencia ahora se ejecuta en otra. la precisión se degrada silenciosamente y nadie sabe por qué.`requirements.txt`Escriba una prueba de regresión de preprocesamiento que congele la tokenización esperada de 20 frases de muestra.

> **可复现性漂移。**NLTK y spaCy en diferentes versiones se alterarán entre los diferentes términos y formas de los mismos.`['do', "n't"]`El resultado, en 3.x puede producirse.`["don't"]`◊ tu modelo se entrena en una distribución, se extiende en otra distribución ◊ la tasa de precisión ◊ de verdad baja, nadie sabe la causa ◊ en ◊`requirements.txt`En la versión fija de la biblioteca, escribió un test de tratamiento de regreso, y logró obtener resultados de 20 ejemplos de la frase.

**Training / inference mismatch.**Entrenamiento con preprocesamiento agresivo (minúsculas, eliminación de palabras de parada, stemming), desplegar en la entrada del usuario bruto, cráter de rendimiento de la vigilancia. Esta es la falla de producción NLP más común. Si preprocesas durante el entrenamiento, debes ejecutar la misma función durante la inferencia.

> **训练/推理不匹配。**                                                                                                                                                                                                                                                              

## Envíe el producto .

> **【中文解读】**Este capítulo se centra en cómo se puede implementar el modelo como producto disponible. Desde el modelo original hasta el sistema de producción, se deben considerar múltiples dimensiones de optimización de rendimiento, tratamiento de errores, control, etc.

Una solicitud reutilizable que ayuda a los ingenieros a elegir una estrategia de preprocesamiento sin leer tres libros de texto.

> Una rápida y fácilmente utilizable, ayuda al ingeniero a elegir estrategias de procesamiento preliminares sin necesidad de leer tres libros de texto.

Salvo como`outputs/prompt-preprocessing-advisor.md`¿Qué es esto ?

```markdown
---
name: preprocessing-advisor
description: Recommends a tokenization, stemming, and lemmatization setup for an NLP task.
phase: 5
lesson: 01
---

You advise on classical NLP preprocessing. Given a task description, you output:

1. Tokenization choice (regex, NLTK word_tokenize, spaCy, or transformer tokenizer). Explain why.
2. Whether to stem, lemmatize, both, or neither. Explain why.
3. Specific library calls. Name the functions. Quote the POS-tag translation if NLTK is involved.
4. One failure mode the user should test for.

> **【中文解读】** 练习题按照 Easy/Medium/Hard 三个难度递进。建议至少完成 Medium 级别的题目，Hard 级别适合深入研究或面试准备。

Refuse to recommend stemming for user-visible text. Refuse to recommend lemmatization without POS tags. Flag non-English input as needing a different pipeline.
```

## Los ejercicios.

1. **Easy.**Extenderse`tokenize`Para mantener las URLs como tokens únicos.`tokenize("Visit https://example.com today.")`debe producir un token de URL.
   **简单。**扩展 `tokenize`Para que la URL se mantenga en un solo token.`tokenize("Visit https://example.com today.")`应产生一个URL token──
2. **Medium.**Implemente el paso Porter 1b. Si una palabra contiene una vocal y termina en `ed`o `ing`, quitarlo. Manejar la regla de doble consonante (`hopping -> hop`No , no .`hopp`¿Qué es lo que se hace?
   **中等。**实现 Porter 步骤 1b.  If a word contains a vowels and a `ed`O `ing`结尾,则移除它──处理双辅音规则(`hopping -> hop`, en lugar de`hopp`)。
3. **Hard.**Construye un lemmatizer que utiliza WordNet como una tabla de búsqueda pero cae de nuevo a su Porter votes cuando WordNet no tiene entrada. Medir la precisión en un corpus etiquetado contra el simple WordNet y el simple Porter.
   **困难。**Construir un uso de WordNet  como buscador de palabras  como la lista de palabras  Cuando WordNet  sin条目时回归你的波特词干提取器── en la medición de los materiales de etiquetado en relación con la precisión de Pure WordNet 和 Pure Porter──

> **【中文解读】**En el lenguaje de los términos "Lo que la gente dice" vs "Lo que realmente significa" se distingue entre el lenguaje diario y la definición técnica de significado.

## Términos clave .

| Term | What people say | What it actually means | 术语 | 人们常说的 | 实际含义 |
|------|-----------------|-----------------------|------|-----------|---------|
| Token | A word | Whatever unit the model consumes. Can be word, subword, character, or byte. | Token（词元） | 一个词 | 模型消耗的任何单位。可以是词、子词、字符或字节。 |
| Stem | Root of a word | Result of rule-based suffix stripping. Not always a real word. | Stem（词干） | 词的词根 | 基于规则的后缀剥离结果。不一定是真正的词。 |
| Lemma | Dictionary form | The form you'd look up. Requires grammatical context to compute correctly. | Lemma（词元形式） | 词典形式 | 你会去词典中查找的形式。需要语法上下文才能正确计算。 |
| POS tag | Part of speech | Category like NOUN, VERB, ADJ. Needed to lemmatize accurately. | POS tag（词性标注） | 词性 | 如 NOUN、VERB、ADJ 等类别。准确词形还原需要它。 |
| Morphology | Word shape rules | How a word changes form based on tense, number, case. Lemmatization depends on it. | Morphology（形态学） | 词形变化规则 | 词如何根据时态、数、格变化形式。词形还原依赖它。 |

> **【中文解读】**延伸阅读 proporciona un alto nivel de recursos para el aprendizaje profundo. Estos artículos y cursos son los referentes clásicos en el campo, adecuados para los lectores que necesitan una comprensión profunda.

## Más Leer más Leer más

- [Porter, M. F. (1980). An algorithm for suffix stripping](https://tartarus.org/martin/PorterStemmer/def.txt) el papel original, cinco páginas, todavía la explicación más clara. / 原始论文,五页,至今仍然是最清晰的解释──
- [spaCy 101 — linguistic features](https://spacy.io/usage/linguistic-features)¿Cómo se conecta una tubería real?
- [NLTK book, chapter 3](https://www.nltk.org/book/ch03.html) casos de margen de tokenización que aún no has pensado. / 你还没想过分词边界情况──
