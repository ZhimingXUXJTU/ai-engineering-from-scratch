# Resumen del texto 文本摘要

> Los sistemas extractivos te dicen lo que dice el documento, los sistemas abstractos te dicen lo que el autor quería decir, diferentes tareas, diferentes trampas.
> 抽取式系统告诉你文档说了什么――生成式系统告诉你作者意思―― diferentes tareas, diferentes trampas―

> **【中文解读】**抽取式 vs 生成式摘要──

**Type:** Build | **类型:** 动手
**Languages:** Python | **语言:** Python
**Prerequisites:** Phase 5 · 02 (BoW + TF-IDF), Phase 5 · 11 (Machine Translation) | **前置知识:** Phase 5 · 02 (BoW + TF-IDF), Phase 5 · 11 (Machine Translation)
**Time:** ~75 minutes | **时间:** ~75 minutes


## El problema es la introducción del problema

Un artículo de noticias de 2.000 palabras se encuentra en su feed. Necesitas 120 palabras que lo capturen. Puedes elegir las tres frases más importantes del artículo (extractiva) o reescribir el contenido en tus propias palabras (abstractiva). Ambos se llaman resumen. Son problemas completamente diferentes.
> Un artículo de noticias de 2000 palabras aparece en tu flujo de información. Necesitas 120 palabras para generalizarlo. Puedes escoger las tres frases más importantes del artículo, o volver a escribir el contenido con tu propia frase.

> **【中文解读】**La pregunta planteada en este capítulo es: ¿cómo entender y aplicar correctamente esta tecnología en la ingeniería real? Comprender el contexto de la cuestión ayuda a comprender los puntos clave de decisión del tipo de selección técnica. En los sistemas de IA reales, el tipo de selección técnica errónea suele ser más alto que el costo de error de la realización de detalles.


La resumen extractiva es un problema de clasificación.`k`El resultado es siempre gramatical porque se levanta literalmente.
> 抽取式摘要是一个排序问题――给每个句子打分,返回排名 `k`El riesgo de que el contenido de un artículo esté perdido se encuentra distribuido en todo el artículo.

La resumen abstractiva es un problema de generación. Un transformador produce un nuevo texto condicionado a la entrada. La salida es fluida y compresiva, pero puede alucinar hechos que no estaban en la fuente. El riesgo es la fabricación segura.
> El resumen de la producción es un problema de generación. El transformador produce un nuevo texto según la entrada.

Esta lección construye a ambos, con el modo de fracaso que cada uno posee.
> Este curso se desarrolla en dos partes, así como en los modelos de fracaso que cada una posee.

> **【中文解读】**Este capítulo presenta los conceptos y teorías básicos. La comprensión de estos conceptos es el prerrequisito de la realización posterior de la actividad, y también el conocimiento de los puntos de alta frecuencia de la entrevista y la práctica de la ingeniería.


## El concepto central.

![Extractive TextRank vs abstractive transformer](../assets/summarization.svg)
> ![抽取式 TextRank vs 生成式 Transformer](../assets/summarization.svg)

**Extractive.**Trate el artículo como un gráfico donde los nodos son oraciones y los bordes son similitudes. ejecuta PageRank (o algo parecido) sobre el gráfico para marcar oraciones por la conexión que tienen con todo lo demás.**TextRank**(Mihalcea y Tarau, 2004).
> **抽取式（Extractive）。**Cuando se trata de un artículo, el punto es un punto, el borde es una similitud.**TextRank**(Mihalcea y Tarau, 2004):

**Abstractive.**La combinación de un transformer encoder-decoder (BART, T5, Pegasus) en pares de resumen de documentos.
> **生成式（Abstractive）。**En el caso de los modelos de la serie de modelos de modelos de modelos de modelos de modelos de modelos de modelos de modelos de modelos de modelos de modelos de modelos de modelos de modelos de modelos de modelos de modelos de modelos de modelos de modelos de modelos de modelos de modelos de modelos de modelos de modelos de modelos de modelos de modelos de modelos de modelos de modelos de modelos de modelos de modelos de modelos de modelos de modelos de modelos de modelos de modelos de modelos de modelos de modelos de modelos de modelos de modelos de modelos de modelos de modelos de modelos de modelos de modelos de modelos de modelos de modelos de modelos de modelos de modelos de modelos de modelos de modelos de modelos de modelos de modelos de modelos de modelos de modelos de modelos de modelos de modelos de modelos de modelos de modelos de modelos de modelos de modelos de modelos de modelos de modelos de modelos de modelos de modelos de modelos de modelos de modelos de modelos de modelos de modelos de modelos de modelos de modelos de modelos de modelos de modelos de modelos de modelos de modelos de modelos de modelos de modelos de modelos de modelos de modelos de modelos de modelos de modelos de modelos de modelos de modelos de modelos de modelos de modelos de modelos de modelos de modelos de modelos de modelos de modelos de modelos de modelos de modelos de modelos de modelos de modelos de modelos de modelos de modelos de modelos de modelos de modelos de modelos de modelos de modelos de modelos de modelos de modelos de modelos de modelos de modelos de modelos de modelos de modelos de modelos de modelos de modelos de modelos de modelos de modelos de modelos de modelos de modelos de modelos de modelos de modelos de modelos de modelos de modelos de modelos de modelos de modelos de modelos de modelos de modelos de modelos de modelos de modelos de modelos de modelos de modelos de modelos de modelos de modelos de modelos de modelos de modelos de modelos de modelos de modelos de modelos de modelos de modelos de modelos de modelos de modelos de modelos de modelos de modelos de modelos de modelos de modelos de modelos de modelos de modelos de modelos de modelos de modelos de modelos de modelos de modelos de modelos de modelos de modelos de modelos de modelos de modelos de modelos de modelos de modelos de modelos de modelos de modelos de modelos de modelos de modelos de modelos de modelos de modelos de modelos de modelos de modelos de modelos de modelos de modelos de modelos de modelos de modelos de modelos de modelos de modelos de modelos de modelos de modelos de modelos de modelos de modelos de modelos de modelos de modelos de modelos de modelos de modelos de modelos de modelos de modelos de modelos de modelos de modelos de modelos de modelos de

Evaluación con **ROUGE**(Recall-Oriented Understudy for Gisting Evaluation). ROUGE-1 y ROUGE-2 puntajes unigram y bigram superpone. ROUGE-L puntajes más largo subsecuencia común. Más alto es mejor, pero 40 ROUGE-L es "bueno" y 50 es "excepcional".`rouge-score`el paquete.
> Uso **ROUGE**(Recall-Oriented Understudy for Gisting Evaluation) evaluación──ROUGE-1 和 ROUGE-2 评分一元组和二元组重叠──ROUGE-L 评分最长公共子序列──越高越好,但40 ROUGE-L是"好",50是"出色"──每篇论文都报告全部三个──使用`rouge-score`¿Qué es eso?

> **【拓展：大语言模型的工程实践】**Desde GPT hasta ChatGPT, el campo de NLP ha experimentado un cambio de paradigma de "cada tarea entrenar un modelo" a "un modelo resolver todas las tareas". En el proyecto real, la implementación de LLM necesita considerar los problemas de token 限制,延迟,成本, seguridad etc.

> **【拓展：RAG 与企业知识库】**检索增强生成(RAG) es la estructura más popular de las aplicaciones de IA de las empresas actuales: la consulta de usuarios primero se consulta los documentos relacionados, luego se vuelve a buscar los resultados como respuesta a la pregunta de LLM.

> **【拓展：NLP 的多语言挑战】**En todo el mundo hay más de 7000 idiomas, pero los estudios de PNL se centran principalmente en inglés y en una minoría de idiomas.


## Construye y realiza.

> **【中文解读】**Este capítulo a través del código de la implementación de algoritmos centrales de cero. Este método "desde cero" puede ayudar a entender el principio detrás del marco, no se encuentra en la caja negra cuando se encuentran problemas.

```figure
summarize-collapse
```

## Construye el mismo

### Paso 1: TextRank (extractivo)
> 两件事值得注意──相似度函数使用对数归结的词重叠, esto es el original Variante de TextRank──TF-IDF 向量的余弦相似度也行──阻尼因子 0.85 和代次数是PageRank's默认值──

```python
import math
import re
from collections import Counter


def sentence_split(text):
    return re.split(r"(?<=[.!?])\s+", text.strip())


def similarity(s1, s2):
    w1 = Counter(s1.lower().split())
    w2 = Counter(s2.lower().split())
    intersection = sum((w1 & w2).values())
    denom = math.log(len(w1) + 1) + math.log(len(w2) + 1)
    if denom == 0:
        return 0.0
    return intersection / denom


def textrank(text, top_k=3, damping=0.85, iterations=50, epsilon=1e-4):
    sentences = sentence_split(text)
    n = len(sentences)
    if n <= top_k:
        return sentences

    sim = [[0.0] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            if i != j:
                sim[i][j] = similarity(sentences[i], sentences[j])

    scores = [1.0] * n
    for _ in range(iterations):
        new_scores = [1 - damping] * n
        for i in range(n):
            total_out = sum(sim[i]) or 1e-9
            for j in range(n):
                if sim[i][j] > 0:
                    new_scores[j] += damping * sim[i][j] / total_out * scores[i]
        if max(abs(s - ns) for s, ns in zip(scores, new_scores)) < epsilon:
            scores = new_scores
            break
        scores = new_scores

    ranked = sorted(range(n), key=lambda k: scores[k], reverse=True)[:top_k]
    ranked.sort()
    return [sentences[i] for i in ranked]
```

La función de similitud utiliza una superposición de palabras normalizadas de registro, que es la variante original de TextRank.
> BART-large-CNN en CNN/DailyMail 语料上微调──开箱即即用产生新闻风格摘要── para otros campos, utilizar Pegasus 检查点应对或在目标数据上微调──

### Paso 2: abstracto con BART
> 始终使用词干提取──没有它, "running" 和 "run" 被视为不同的词,ROUGE 会低估──

```python
from transformers import pipeline

summarizer = pipeline("summarization", model="facebook/bart-large-cnn")

article = """(long news article text)"""

summary = summarizer(article, max_length=120, min_length=60, do_sample=False)
print(summary[0]["summary_text"])
```

BART-large-CNN está ajustado al corpus de CNN/DailyMail. Produce resúmenes de estilo de noticias fuera de la caja. Para otros dominios (artículos científicos, diálogo, legal), utilice el correspondiente punto de control Pegasus o ajuste a sus datos objetivo.
> ROUGE ha sido el principal indicador de resumen durante 20 años, pero en 2026 ya no basta con ello.

### Paso 3: Evaluación ROUGE
> - **BERTScore**(上下文嵌入相似度) en 2023 se ha visto más afectado, ahora la mayoría de los artículos de resumen están relacionados con ROUGE un primer informe.
- **BARTScore**Se evaluará la perspectiva de la producción: a través del entrenamiento previo BART                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            
- **MoverScore**(sobre la siguiente página) alcanza el máximo en el 2025 del resumen de base, ya que es mejor que ROUGE para capturar la traducción de la palabra.
- **FactCC**Y**基于 QA 的事实性检查**En 2021-2023 años muy común, ahora normalmente se **G-Eval**(una especie de GPT-4 提示链, con una cadena de pensamiento de la evaluación de la coherencia, la coherencia, la fluidez y la correlación)
- **G-Eval**Y similar LLM  evaluación método en el evaluación estándares diseñados bien cuando el juicio humano es aproximadamente 80% de la misma.

```python
from rouge_score import rouge_scorer

scorer = rouge_scorer.RougeScorer(["rouge1", "rouge2", "rougeL"], use_stemmer=True)
scores = scorer.score(reference_summary, generated_summary)
print({k: round(v.fmeasure, 3) for k, v in scores.items()})
```

Sin él, "correr" y "correr" cuentan como palabras diferentes y ROUGE cuentan como subcuentas.
> Producción de recomendaciones: informe ROUGE-L Usado para el legado comparativo, BERTScore Usado para el significado sobrepeso, G-Eval Usado para la coherencia y la realidad.

### Más allá de ROUGE (2026 evaluación de resumen)
> Los extractos de producción son muy fáciles de extraer, ya que el resultado es extraído de la fuente por letra, aunque si las frases de origen se descansan de la siguiente, pueden ser confundidas. Es la principal razón por la que el sistema de producción sigue prefiriendo el método extracto en el contenido de la normativa.

ROUGE ha sido la métrica de resumen dominante durante veinte años y no es suficiente por sí sola en 2026.
> 需要命名的幻觉类型:

- **BERTScore**(similaridad de inserción contextual) ganó terreno hasta 2023 y ahora se informa junto con ROUGE en la mayoría de los documentos de resumen.
- **BARTScore**El análisis de la evaluación se realiza en función de la probabilidad de que un BART previamente entrenado lo asigne a la fuente.
- **MoverScore**(Distancia de Earth Mover sobre embebidos contextuales) alcanzó el primer lugar en 2025 en los puntos de referencia de resumen porque capta la superposición semántica mejor que ROUGE.
- **FactCC**y **QA-based faithfulness**Las nuevas tecnologías de la información son comunes en 2021-2023, ahora a menudo reemplazadas por **G-Eval**(una cadena de respuesta GPT-4 que califica la coherencia, la consistencia, la fluidez, la relevancia con el razonamiento de la cadena de pensamiento).
- **G-Eval**y enfoques similares de LLM-juzgados coinciden con el juicio humano ~ 80% del tiempo cuando las rúbricas están bien diseñadas.
> - **实体替换。**源说 "John Smith"―摘要说 "John Brown"―
- **数字漂移。**源说 "25,000"―摘要说"25 millones"―
- **极性翻转。**源说 "rechazó la oferta"―摘要说 "aceptó la oferta"―
- **事实编造。**源没有提到CEO──摘要说CEO 批准了──

Recomendación de producción: informe ROUGE-L para comparación de la herencia, BERTScore para superposición semántica, G-Eval para coherencia y factualidad. Calibrado en función de 50-100 resúmenes etiquetados por humanos.
> Método de evaluación eficaz:

### Paso 4: el problema de la realidad
> - **FactCC。**En la base de la frase y la frase resumen se ha entrenado en la relación entre la realidad y la realidad.
- **基于 QA 的事实性检查。**Para QA 模型问源有答题──如果摘要支持不同的答案,标记──
- **实体级 F1。**Comparado con el origen y el nombre de la entidad en el resumen.

Los resúmenes abstractos son propensos a la alucinación. Los resúmenes extractivos tienen un riesgo de alucinación mucho menor porque la salida se levanta literalmente de la fuente, aunque aún pueden engañar si las oraciones de la fuente se descontéxtúan, quedan obsoletas o se citan fuera de orden. Esta es la única razón más grande por la que los sistemas de producción todavía prefieren métodos extractivos para el contenido adyacente al cumplimiento.
>  para el contenido de usuario que es importante en la realidad (información, medicina, ley, finanzas), la extracción es una opción predeterminada más segura.

Tipos de alucinaciones para nombrar:

- **Entity swap.**La fuente dice "John Smith". El resumen dice "John Brown".
- **Number drift.**La fuente dice "25.000". El resumen dice "25 millones".
- **Polarity flip.**La fuente dice "rechazó la oferta". El resumen dice "aceptó la oferta".
- **Fact invention.**La fuente no menciona al CEO.

La evaluación se aproxima a ese trabajo:

- **FactCC.**Un clasificador binario entrenado en la relación entre la frase fuente y la frase resumida. Predece hechos/no hechos.
- **QA-based factuality.**Si el resumen respalda respuestas diferentes, señale.
- **Entity-level F1.**Comparar las entidades nombradas en la fuente con el resumen.

Para cualquier cosa que se enfrente al usuario donde la factualidad importa (noticias, médicos, legales, financieros), la extractiva es el default más seguro.

> **【中文解读】**Este capítulo muestra cómo utilizar un marco maduro (como PyTorch、HuggingFace, etc.) para aplicar rápidamente esta tecnología. En los proyectos reales, se realiza con prioridad el uso de un marco experimentado, se pueden reducir errores y mejorar la eficiencia de desarrollo.


> **【拓展：Prompt Engineering 与 LLM 应用】**La ingeniería rápida se ha convertido en la habilidad central de los ingenieros de PNL. Desde la Cero-Shot hasta la Few-Shot, desde la Cadena de Pensamiento hasta la Reacción, diferentes estrategias de sugerencias se aplican a diferentes escenarios.

## Usalo con el marco de ejecución

La pila de 2026:
> 2026 años de tecnología:

| Use case | Recommended |
|---------|-------------|
| News, 3-5 sentence summary, English | `facebook/bart-large-cnn` |
| Scientific papers | `google/pegasus-pubmed` or a tuned T5 |
| Multi-document, long-form | Any LLM with 32k+ context, prompted |
| Dialog summarization | `philschmid/bart-large-cnn-samsum` |
| Extractive, low hallucination risk by construction | TextRank or `sumy`'s LSA / LexRank |
> # Usar la escena #
|---------|------|
| 新闻，3-5 句摘要，英语 | `facebook/bart-large-cnn` |
| 科学论文 | `google/pegasus-pubmed` 或微调的 T5 |
| 多文档，长文 | 任何 32k+ 上下文的 LLM，提示 |
| 对话摘要 | `philschmid/bart-large-cnn-samsum` |
| 抽取式，结构性低幻觉风险 | TextRank 或 `sumy` 的 LSA / LexRank |

> **【中文解读】**Este capítulo se centra en cómo se puede implementar el modelo como producto disponible. Desde el modelo original hasta el sistema de producción, se deben considerar múltiples dimensiones de optimización de rendimiento, tratamiento de errores, control, etc.


Los LLM con contexto largo a menudo superan a los modelos especializados en 2026 cuando la computación no es una limitación.
> En el año 2026 en el cálculo no se limita, el LLM normalmente supera los modelos específicos.


## Envíe el producto .

Salvo como`outputs/skill-summary-picker.md`¿Qué es esto ?
> 保存为                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           `outputs/skill-summary-picker.md`¿Qué es esto ?

```markdown
---
name: summary-picker
description: Pick extractive or abstractive, named library, factuality check.
version: 1.0.0
phase: 5
lesson: 12
tags: [nlp, summarization]
---

Given a task (document type, compliance requirement, length, compute budget), output:

1. Approach. Extractive or abstractive. Explain in one sentence why.
2. Starting model / library. Name it. `sumy.TextRankSummarizer`, `facebook/bart-large-cnn`, `google/pegasus-pubmed`, or an LLM prompt.
3. Evaluation plan. ROUGE-1, ROUGE-2, ROUGE-L (use rouge-score with stemming). Plus factuality check if abstractive.
4. One failure mode to probe. Entity swap is the most common in abstractive news summarization; flag samples where source entities do not appear in summary.

> **【中文解读】** 练习题按照 Easy/Medium/Hard 三个难度递进。建议至少完成 Medium 级别的题目，Hard 级别适合深入研究或面试准备。


Refuse abstractive summarization for medical, legal, financial, or regulated content without a factuality gate. Flag input over the model's context window as needing chunked map-reduce summarization (not just truncation).
```

## Los ejercicios.

1. **Easy.**Ejecutar TextRank en 5 artículos de noticias. Comparar las tres frases principales con un resumen de referencia. Medir ROUGE-L. Usted debe ver 30-45 ROUGE-L en artículos de estilo CNN / DailyMail.
2. **Medium.**Implementar la realidad a nivel de entidad: extraer las entidades nombradas de la fuente y el resumen (spaCy), recordar las entidades fuentes en resumen y recoger con precisión las entidades sumarias en relación con la fuente.
3. **Hard.**Comparar BART-grand-CNN con un LLM (Claude o GPT-4) en 50 artículos de CNN/DailyMail.
> 1. **简单。**En 5 篇新闻文章上运行 TextRank. 将 top-3 句子与参考摘要比较. 测量 ROUGE-L.  在 CNN/DailyMail 风格文章上你应该看到 30-45 ROUGE-L.
2. **中等。**实现实体级事实性: de origen y resumen entre提取命名实体(spaCy), de origen de cálculo entre la tasa de recolección en resumen y la tasa de precisión de origen de origen de origen de origen de origen de resumen.
3. **困难。**En 50 篇 CNN/DailyMail 文章上比较 BART-big-CNN与LLM(Claude或GPT-4) ――报告 ROUGE-L、事实性(按实体F1) y cada resumen de costes──记录各自的胜场景──

> **【中文解读】**En el lenguaje de los términos "Lo que la gente dice" vs "Lo que realmente significa" se distingue entre el lenguaje diario y la definición técnica de significado.


## Términos clave .

| Term | What people say | What it actually means |
|------|-----------------|-----------------------|
| Extractive | Pick sentences | Return sentences verbatim from the source. Never hallucinates. |
| Abstractive | Rewrite | Generate new text conditioned on source. Can hallucinate. |
| ROUGE | Summary metric | N-gram / LCS overlap between system output and reference. |
| TextRank | Graph-based extractive | PageRank over sentence similarity graph. |
| Factuality | Is it right | Whether summary claims are supported by the source. |
| Hallucination | Made-up content | Content in the summary that the source does not support. |
> # Los términos # # que la gente dice # # tienen un significado real #
|------|-----------|---------|
| 抽取式 | 选取句子 | 从源中逐字返回句子。不会幻觉。 |
| 生成式 | 重写 | 根据源生成新文本。可能幻觉。 |
| ROUGE | 摘要指标 | 系统输出与参考之间的 n-gram / LCS 重叠。 |
| TextRank | 基于图的抽取式 | 句子相似度图上的 PageRank。 |
| 事实性 | 对不对 | 摘要声明是否被源支持。 |
| 幻觉 | 编造内容 | 摘要中源不支持的内容。 |

> **【中文解读】**延伸阅读 proporciona un alto nivel de recursos para el aprendizaje profundo. Estos artículos y cursos son los referentes clásicos en el campo, adecuados para los lectores que necesitan una comprensión profunda.


## Más Leer más Leer más

- [Mihalcea and Tarau (2004). TextRank: Bringing Order into Texts](https://aclanthology.org/W04-3252/) el papel canónico extractivo.
- [Lewis et al. (2019). BART: Denoising Sequence-to-Sequence Pre-training](https://arxiv.org/abs/1910.13461) el papel BART.
- [Zhang et al. (2019). PEGASUS: Pre-training with Extracted Gap-sentences](https://arxiv.org/abs/1912.08777) Pegasus y el objetivo de la frase de la brecha.
- [Lin (2004). ROUGE: A Package for Automatic Evaluation of Summaries](https://aclanthology.org/W04-1013/) papel rojo.
- [Maynez et al. (2020). On Faithfulness and Factuality in Abstractive Summarization](https://arxiv.org/abs/2005.00661) el documento de paisaje de la realidad.
> - [Mihalcea and Tarau (2004). TextRank: Bringing Order into Texts](https://aclanthology.org/W04-3252/) 抽取式经典论文── y también el libro de la literatura clásica.
- [Lewis et al. (2019). BART: Denoising Sequence-to-Sequence Pre-training](https://arxiv.org/abs/1910.13461) BART 论文。
- [Zhang et al. (2019). PEGASUS: Pre-training with Extracted Gap-sentences](https://arxiv.org/abs/1912.08777) Pegasus 和间隔句子目标──
- [Lin (2004). ROUGE: A Package for Automatic Evaluation of Summaries](https://aclanthology.org/W04-1013/) ROUGE 论文──
- [Maynez et al. (2020). On Faithfulness and Factuality in Abstractive Summarization](https://arxiv.org/abs/2005.00661) Fakt性全景论文──
