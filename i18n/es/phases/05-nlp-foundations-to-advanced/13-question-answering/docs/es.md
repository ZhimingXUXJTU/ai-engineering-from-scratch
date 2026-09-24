# Sistema de respuestas a preguntas.

> Tres sistemas formaron la inteligencia artificial moderna. Extractiva encontró extensiones. Recuperar aumentó la tierra en documentos. Generativo produjo respuestas. Cada asistente de IA moderno es una mezcla de los tres.
> Tres sistemas han formado la respuesta moderna. Tráger de la respuesta a la pregunta.

> **【中文解读】**Desde la búsqueda de información hasta la generación de preguntas y respuestas.

**Type:** Build | **类型:** 动手
**Languages:** Python | **语言:** Python
**Prerequisites:** Phase 5 · 11 (Machine Translation), Phase 5 · 10 (Attention Mechanism) | **前置知识:** Phase 5 · 11 (Machine Translation), Phase 5 · 10 (Attention Mechanism)
**Time:** ~75 minutes | **时间:** ~75 minutes


## El problema es la introducción del problema

Un usuario escribe "¿Cuándo lanzó el primer iPhone?" y espera "29 de junio de 2007". No "La historia de Apple es larga y variada". No "2007" sentado aislado sin oración. Una respuesta directa, basada y correcta.
> Usuario ingresar "Cuándo se lanzó el primer iPhone?" y esperar obtener "29 de junio de 2007."― no "La historia de Apple es larga y variada".― no aislada "2007" 没有句子上下文──一个直接、有据可依、正确的答案──

> **【中文解读】**La pregunta planteada en este capítulo es: ¿cómo entender y aplicar correctamente esta tecnología en la ingeniería real? Comprender el contexto de la cuestión ayuda a comprender los puntos clave de decisión del tipo de selección técnica. En los sistemas de IA reales, el tipo de selección técnica errónea suele ser más alto que el costo de error de la realización de detalles.


Tres arquitecturas han dominado la QA en la última década.
> En la década pasada, tres estructuras han dominado la pregunta y la respuesta.

- **Extractive QA.**Dado una pregunta y un pasaje que se sabe que contiene la respuesta, encontrar los índices de inicio y final del intervalo de respuesta en el pasaje.
- **Open-domain QA.**El pasaje no se da. Recupera el pasaje relevante primero, luego extrae o genera una respuesta. Esta es la base de cada oleoducto RAG hoy en día.
- **Generative / Closed-book QA.**Un modelo de lenguaje grande responde desde su memoria parámétrica, sin recuperación, más rápido en la inferencia, menos confiable en los hechos.
> - **抽取式问答（Extractive QA）。**给定一个问题和已知含答案的段落, encontrar la respuesta en el inicio y final del段落.
- **开放域问答（Open-domain QA）。**段落未给定──先检查相关段落,然后抽取或生成答案── es la piedra angular de cada RAG 流水线 de hoy──
- **生成式/闭卷问答（Generative / Closed-book QA）。**El modelo de la lengua se basa en la memoria de los parámetros.

La tendencia en 2026 es híbrida: recuperar los mejores pasajes, luego pedir un modelo generativo para responder en esos pasajes. Eso es RAG, y la lección 14 cubre la mitad de la recuperación en profundidad. Esta lección construye la mitad de la QA.
> La tendencia del año 2026 es mezcla: buscar los mejores fragmentos, y luego presentar los modelos generados en base a estos fragmentos.

## El concepto central.

> **【中文解读】**Este capítulo presenta los conceptos y teorías básicos. La comprensión de estos conceptos es el prerrequisito de la realización posterior de la actividad, y también el conocimiento de los puntos de alta frecuencia de la entrevista y la práctica de la ingeniería.


![QA architectures: extractive, retrieval-augmented, generative](../assets/qa.svg)
> ![问答架构：抽取式、检索增强、生成式](../assets/qa.svg)

**Extractive.**Encode la pregunta y el pasaje junto con un transformador (familia BERT). Entrenar dos cabezas que predicen los índices de inicio y final de los tokens de la respuesta. La pérdida es entropía cruzada sobre posiciones válidas. La salida es un espacio de tiempo del pasaje. Nunca alucina (por construcción), nunca maneja preguntas que el pasaje no puede responder (por construcción).
> **抽取式。**Usador (en inglés) DATA (en inglés) DATA (en inglés) DATA (en inglés) DATA (en inglés) DATA (en inglés) DATA (en inglés) DATA (en inglés) DATA (en inglés) DATA (en inglés) DATA (en inglés) DATA (en inglés) DATA (en inglés) DATA (en inglés) DATA (en inglés) DATA (en inglés) DATA (en inglés) DATA (en inglés) DATA (en inglés) DATA (en inglés) DATA (en inglés) DATA (en inglés) DATA (en inglés) DATA (en inglés) DATA (en inglés) DATA (en inglés) DATA (en inglés) DATA (en inglés) DATA (en inglés) DATA (en inglés) DATA (en inglés) DATA (en inglés) DATA (en inglés) DATA (en inglés) DATA (en inglés) DATA (en inglés) DATA (en inglés) DATA (en inglés) DATA (en inglés) DATA (en inglés) DATA (en inglés) DATA (en inglés) DATA (en inglés) DATA (en inglés) DATA (en inglés) DATA (en inglés) DATA (en inglés) DATA (en inglés) DATA (en inglés) DATA (en inglés) DATA (en inglés) DATA (en inglés) DATA (en inglés) DATA (en inglés) DATA (en inglés) DATA (en inglés) DATA (en inglés) DATA (en inglés) DATA (en inglés)

**Retrieval-augmented (RAG).**Dos etapas. Primero, un retriever encuentra la parte superior...`k`En segundo lugar, un lector (extractivo o generativo) produce la respuesta utilizando esos pasajes. La división retriever-lector permite que cada uno sea entrenado y evaluado de forma independiente.
> **检索增强（RAG）。**Dos fases. Primero, el buscador en la biblioteca de palabras encuentra la parte superior.`k`段落──二,阅读器(抽取式或生成式) utiliza estos fragmentos para generar respuestas──检索器-阅读器分离允许 su propio entrenamiento y evaluación independientes──现代RAG normalmente añade una redimensionante entre ambos──

**Generative.**Un LLM solo para decodificadores (GPT, Claude, Llama) responde a partir de pesas aprendidas. No hay paso de recuperación. Excelente en el conocimiento común, catastrófico en hechos raros o recientes. La tasa de alucinación está inversamente correlacionada con la frecuencia de hechos en los datos de preparación.
> **生成式。**仅解码器的 LLM(GPT、Claude、Llama) de aprender a responder en el peso de la respuesta.

> **【拓展：大语言模型的工程实践】**Desde GPT hasta ChatGPT, el campo de NLP ha experimentado un cambio de paradigma de "cada tarea entrenar un modelo" a "un modelo resolver todas las tareas". En el proyecto real, la implementación de LLM necesita considerar los problemas de token 限制,延迟,成本, seguridad etc.

> **【拓展：RAG 与企业知识库】**检索增强生成(RAG) es la estructura más popular de las aplicaciones de IA de las empresas actuales: la consulta de usuarios primero se consulta los documentos relacionados, luego se vuelve a buscar los resultados como respuesta a la pregunta de LLM.

> **【拓展：NLP 的多语言挑战】**En todo el mundo hay más de 7000 idiomas, pero los estudios de PNL se centran principalmente en inglés y en una minoría de idiomas.


## Construye y realiza.

> **【中文解读】**Este capítulo a través del código de la implementación de algoritmos centrales de cero. Este método "desde cero" puede ayudar a entender el principio detrás del marco, no se encuentra en la caja negra cuando se encuentran problemas.

```figure
qa-span
```

## Construye el mismo

### Paso 1: A.Q. extractiva con un modelo pre-entrenado
> `deepset/roberta-base-squad2`En el entrenamiento SQuAD 2.0, contiene preguntas que no pueden ser contestadas.`question-answering`流水线返回最高分分的片段, incluso el número de vuelos del modelo vence 它不自动返回空答案── para obtener un comportamiento "no contestado" evidente, 流水线调用中传进 `handle_impossible_answer=True`:Refluentes sólo en el espacio por encima de todos los fragmentos por encima del tiempo de regreso en el espacio por respuesta.`score`¿Qué es eso?

```python
from transformers import pipeline

qa = pipeline("question-answering", model="deepset/roberta-base-squad2")

passage = (
    "Apple Inc. released the first iPhone on June 29, 2007. "
    "The device was announced by Steve Jobs at Macworld in January 2007."
)
question = "When was the first iPhone released?"

answer = qa(question=question, context=passage)
print(answer)
```

```python
{'score': 0.98, 'start': 57, 'end': 70, 'answer': 'June 29, 2007'}
```

`deepset/roberta-base-squad2`El programa de formación de la Comisión de Educación y Ciencias de la Humanidad (SquAD 2.0) incluye preguntas sin respuesta.`question-answering`pipeline devuelve el lapso de puntaje más alto incluso cuando el puntaje nulo del modelo gana  no * no * automáticamente devuelve una respuesta vacía. Para obtener el comportamiento explícito "no respuesta", pasa `handle_impossible_answer=True`a la llamada de la línea de tubería: la línea de tubería devuelve una respuesta vacía sólo cuando el puntaje nulo excede cada puntaje de la línea de espera.`score`campo de cualquier manera.
> 两段流水线──密检索器(Sentence-BERT) a través de la similitud de palabras encontrar los pasajes relacionados──抽取式阅读器(RoBERTa-SquAD) de la combinación de los pasajes superiores 提取答案片段── se aplica a la pequeña biblioteca de palabras── para los millones de tipos de documentos, con el uso de FAISS o de la biblioteca de datos de la masa──

### Paso 2: una tubería aumentada para la recuperación (bozo)
> 提示模式很重要──显式告诉模型基于上下文答复和上下文不足时回复"No sé",相比简单提示将幻觉率降低40-60%.──更精细的模式添加引用、信任分数和结构化抽取──

```python
from sentence_transformers import SentenceTransformer
import numpy as np

encoder = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")

corpus = [
    "Apple Inc. released the first iPhone on June 29, 2007.",
    "Macworld 2007 featured the iPhone announcement by Steve Jobs.",
    "Android launched in 2008 as Google's mobile operating system.",
    "The first iPod was released in 2001.",
]
corpus_embeddings = encoder.encode(corpus, normalize_embeddings=True)


def retrieve(question, top_k=2):
    q_emb = encoder.encode([question], normalize_embeddings=True)
    sims = (corpus_embeddings @ q_emb.T).squeeze()
    order = np.argsort(-sims)[:top_k]
    return [corpus[i] for i in order]


def answer(question):
    passages = retrieve(question, top_k=2)
    combined = " ".join(passages)
    return qa(question=question, context=combined)


print(answer("When was the first iPhone released?"))
```

El sistema de recopilación densa (Sentence-BERT) encuentra pasajes relevantes por similitud semántica. El lector extractivo (RoBERTa-SQuAD) extrae el intervalo de respuesta de los pasajes superiores combinados. Trabaja en corporales pequeños. Para un corpus de un millón de documentos, utilice FAISS o una base de datos vectorial.
> SQUAD Uso**精确匹配（Exact Match, EM）**Y **token 级 F1**◦ EM es una combinación de puntos de eliminación y de eliminación de coronas (por ejemplo, la combinación de puntos de eliminación y de eliminación de coronas) ◦ Previsión o la combinación precisa, por ejemplo, 0♦ F1 en el token de previsión y referencia 重叠上计算,给部分分──两都低估释义:"29 de junio de 2007" vs "29 de junio de 2007" normalmente 0 EM (por ejemplo, la combinación de números de destrucción de la combinación) pero todavía se obtiene una notable F1♦

### Paso 3: generativo con RAG
> 对于生产问答:

```python
def rag_generate(question, llm):
    passages = retrieve(question, top_k=3)
    prompt = f"""Context:
{chr(10).join('- ' + p for p in passages)}

Question: {question}

Answer using only the context above. If the context does not contain the answer, say "I don't know."
"""
    return llm(prompt)
```

El patrón de prompt importa. Decir explícitamente al modelo que se encuentre en el contexto y regresar "no sé" cuando el contexto es insuficiente reduce las tasas de alucinación en un 40-60% en comparación con el prompting ingenuo.
> - **答案准确率**(LLM 评判或人工评判,因为指标不捕获语义等价)
- **引用准确率。**¿Es el texto de la cita realmente compatible con la respuesta?
- **拒绝校准。**Cuando la respuesta no está en el segmento de la investigación, ¿el sistema dice correctamente "no sé"?
- **检索召回率。**Antes de evaluar el lector, el detector de medición si se va a colocar correctamente en la parte superior...`k`❖ Reader cannot repair missing paragraphs──

### Paso 4: evaluación que refleje el mundo real
> `RAGAS`专为RAG 系统构建,是2026年发布默认选择――它在没有黄金参考的情况下从四维度评分:

Uso de la SQuAD **Exact Match (EM)**y **token-level F1**¿ Qué ? EM es una coincidencia estricta después de la normalización (carácter menor, puntuación de la tira, eliminación de artículos)  o bien la predicción coincide exactamente o obtiene un puntaje de 0. F1 se calcula sobre la superposición de tokens entre predicción y referencia y da crédito parcial. Ambas parafrazas de bajo crédito: "29 de junio de 2007" vs "29 de junio de 2007" generalmente obtiene 0 EM (la normalización de los descansos ordinarios) pero aún gana una F1 sustancial de tokens superpuestos.
> - **忠实度（Faithfulness）。**¿Todas las declaraciones en la respuesta provienen de la siguiente información?
- **答案相关性。**¿La respuesta ha respondido a la pregunta? Mediante la respuesta generando hipótesis de la pregunta y comparando con la verdadera pregunta para medir.
- **上下文精确率。**En el bloque de la búsqueda, ¿cuánto de hecho está relacionado?
- **上下文召回率。**¿Contiene el recopilado toda la información necesaria?

Para la producción de QA:
>  evaluación sin referencia  evaluación en tiempo real sobre el flujo de producción  evaluación en tiempo real  evaluación en tiempo real  evaluación en tiempo real  evaluación en tiempo real  evaluación en tiempo real  evaluación en tiempo real  evaluación en tiempo real  evaluación en tiempo real  evaluación en tiempo real  evaluación en tiempo real  evaluación en tiempo real  evaluación en tiempo real  evaluación en tiempo real  evaluación en tiempo real  evaluación en tiempo real  evaluación en tiempo real  evaluación en tiempo real  evaluación en tiempo real  evaluación en tiempo real  evaluación en tiempo real  evaluación en tiempo real  evaluación en tiempo real  evaluación en tiempo real  evaluación en tiempo real  evaluación en tiempo real  evaluación en tiempo real  evaluación en tiempo real  evaluación en tiempo real  evaluación en tiempo real  evaluación en tiempo real  evaluación en tiempo real  evaluación en tiempo real  evaluación en tiempo real  evaluación en tiempo real  evaluación  evaluación  evaluación en tiempo real  evaluación  evaluación  evaluación  evaluación                                                                                                                                     

- **Answer accuracy**(Judicado por la LLM o por el hombre, ya que las métricas no capturan equivalencia semántica).
- **Citation accuracy.**¿El pasaje citado realmente respalda la respuesta?
- **Refusal calibration.**Cuando la respuesta no está en los pasajes recuperados, ¿dice correctamente el sistema "No sé"?
- **Retrieval recall.**Antes de evaluar al lector, mide si el retriever obtiene el pasaje correcto en la parte superior...`k`Un lector no puede arreglar un pasaje perdido.
> `pip install ragas`◊ Enlace tu inspector + lector ◊ cada consulta obtiene cuatro ejemplos ◊ regreso ⋅ notificación ⋅

### RAGAS: el marco de evaluación de la producción de 2026

`RAGAS`Es especialmente diseñado para sistemas RAG y es el envío por defecto en 2026.

- **Faithfulness.**¿Todas las afirmaciones en la respuesta provienen del contexto recuperado? Medido por la implicación basada en NLI.
- **Answer relevance.**Se mide generando preguntas hipotéticas de la respuesta y comparando con la pregunta real.
- **Context precision.**De los trozos recuperados, ¿cuál fracción era realmente relevante?
- **Context recall.**¿El conjunto recuperado contiene toda la información necesaria?

La puntuación sin referencias le permite evaluar el tráfico en directo sin respuestas de oro seleccionadas.

`pip install ragas`Conecta tu retriever + lector, consigue cuatro escalares por consulta, alerta de regresión.

> **【中文解读】**Este capítulo muestra cómo utilizar un marco maduro (como PyTorch、HuggingFace, etc.) para aplicar rápidamente esta tecnología. En los proyectos reales, se realiza con prioridad el uso de un marco experimentado, se pueden reducir errores y mejorar la eficiencia de desarrollo.


> **【拓展：Prompt Engineering 与 LLM 应用】**La ingeniería rápida se ha convertido en la habilidad central de los ingenieros de PNL. Desde la Cero-Shot hasta la Few-Shot, desde la Cadena de Pensamiento hasta la Reacción, diferentes estrategias de sugerencias se aplican a diferentes escenarios.

## Usalo con el marco de ejecución

La pila de 2026.
> 2026 años de tecnología

| Use case | Recommended |
|---------|-------------|
| Given passage, find answer span | `deepset/roberta-base-squad2` |
| Over a fixed corpus, closed-book not acceptable | RAG: dense retriever + LLM reader |
| Real-time over a document store | RAG with hybrid (BM25 + dense) retriever + reranker (lesson 14) |
| Conversational QA (follow-up questions) | LLM with conversation history + RAG on each turn |
| Highly factual, regulated domains | Extractive over an authoritative corpus; never generative alone |
> # Usar la escena #
|---------|------|
| 给定段落，找答案片段 | `deepset/roberta-base-squad2` |
| 固定语料上，闭卷不可接受 | RAG：稠密检索器 + LLM 阅读器 |
| 实时文档存储 | RAG 配混合（BM25 + 稠密）检索器 + 重排序器（第 14 课） |
| 对话式问答（追问） | 带对话历史的 LLM + 每轮 RAG |
| 高度事实性、受监管领域 | 在权威语料上的抽取式；永远不要单独用生成式 |

> **【中文解读】**Este capítulo se centra en cómo se puede implementar el modelo como producto disponible. Desde el modelo original hasta el sistema de producción, se deben considerar múltiples dimensiones de optimización de rendimiento, tratamiento de errores, control, etc.


La AQ extractiva es de moda en 2026 porque RAG con LLM maneja más casos.
> La extracción de preguntas y respuestas en 2026 no ha sido popular, ya que el RAG de LLM ha tratado más situaciones.


## Envíe el producto .

Salvo como`outputs/skill-qa-architect.md`¿Qué es esto ?
> 保存为                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           `outputs/skill-qa-architect.md`¿Qué es esto ?

```markdown
---
name: qa-architect
description: Choose QA architecture, retrieval strategy, and evaluation plan.
version: 1.0.0
phase: 5
lesson: 13
tags: [nlp, qa, rag]
---

Given requirements (corpus size, question type, factuality constraint, latency budget), output:

1. Architecture. Extractive, RAG with extractive reader, RAG with generative reader, or closed-book LLM. One-sentence reason.
2. Retriever. None, BM25, dense (name the encoder), or hybrid.
3. Reader. SQuAD-tuned model, LLM by name, or "domain-fine-tuned DistilBERT."
4. Evaluation. EM + F1 for extractive benchmarks; answer accuracy + citation accuracy + refusal calibration for production. Name what you are measuring and how you are measuring it.

Refuse closed-book LLM answers for regulatory or compliance-sensitive questions. Refuse any QA system without a retrieval-recall baseline (you cannot evaluate the reader without knowing the retriever surfaced the right passage). Flag questions that require multi-hop reasoning as needing specialized multi-hop retrievers like HotpotQA-trained systems.
```

> **【中文解读】**Practice los temas de fácil/medio/duro  3 difficulty to pass in  Recomenda al menos completar los temas de grado medio  Grado duro  para la preparación de la entrevista


## Los ejercicios.

1. **Easy.**Configure la línea extractiva SQuAD arriba en 10 pasajes de Wikipedia. 10 preguntas artesanales. Medir la frecuencia con la que la respuesta es correcta. Usted debe ver 7-9 correctas si los pasajes y las preguntas son limpios.
2. **Medium.**Añadir un clasificador de rechazo. Cuando el puntaje de recuperación superior está por debajo de un umbral (digamos 0,3 cosinos), devuelva "no sé" en lugar de llamar al lector.
3. **Hard.**Construye un oleoducto RAG sobre un corpus de 10.000 documentos de su elección. Implemente la recuperación híbrida (BM25 + densa) con fusión RRF (ver lección 14).
> 1. **简单。**En 10 篇维基百科段落设置上述 SQuAD 抽取式流线――手工设计 10 问题――测量答案正确率――如果段落和问题干净,你应该看到7-9 个正确――
2. **中等。**Cuando el máximo de búsquedas es inferior al 值 (por ejemplo, 0.3 余弦), devuelve "no sé" en lugar de usar un lector.
3. **困难。**En tu elección, 10.000 文档语料构建RAG 流水线――实现混合检索(BM25 + 密)加RRF 融合(见第 14 课)――测量有没有混合步骤的答案准确率──记录哪些问题类型受益最大──

> **【中文解读】**En el lenguaje de los términos "Lo que la gente dice" vs "Lo que realmente significa" se distingue entre el lenguaje diario y la definición técnica de significado.


## Términos clave .

| Term | What people say | What it actually means |
|------|-----------------|-----------------------|
| Extractive QA | Find the answer span | Predict start and end indices of the answer within a given passage. |
| Open-domain QA | QA over a corpus | No given passage; must retrieve then answer. |
| RAG | Retrieve then generate | Retrieval-augmented generation. Retriever + reader pipeline. |
| SQuAD | Canonical benchmark | Stanford Question Answering Dataset. EM + F1 metrics. |
| Hallucination | Made-up answer | Reader output not supported by retrieved context. |
| Refusal calibration | Know when to shut up | System correctly says "I don't know" when unable to answer. |
> # Los términos # # que la gente dice # # tienen un significado real #
|------|-----------|---------|
| 抽取式问答 | 找答案片段 | 预测给定段落中答案的起始和结束索引。 |
| 开放域问答 | 语料上的问答 | 无给定段落；必须先检索再回答。 |
| RAG | 检索再生成 | 检索增强生成。检索器 + 阅读器流水线。 |
| SQuAD | 经典基准 | 斯坦福问答数据集。EM + F1 指标。 |
| 幻觉 | 编造答案 | 阅读器输出不被检索上下文支持。 |
| 拒绝校准 | 知道何时闭嘴 | 系统在无法回答时正确地说 "I don't know"。 |

> **【中文解读】**延伸阅读 proporciona un alto nivel de recursos para el aprendizaje profundo. Estos artículos y cursos son los referentes clásicos en el campo, adecuados para los lectores que necesitan una comprensión profunda.


## Más Leer más Leer más

- [Rajpurkar et al. (2016). SQuAD: 100,000+ Questions for Machine Comprehension of Text](https://arxiv.org/abs/1606.05250) el documento de referencia.
- [Karpukhin et al. (2020). Dense Passage Retrieval for Open-Domain QA](https://arxiv.org/abs/2004.04906) DPR, el retriever canónico denso para QA.
- [Lewis et al. (2020). Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks](https://arxiv.org/abs/2005.11401) el periódico que nombró RAG.
- [Gao et al. (2023). Retrieval-Augmented Generation for Large Language Models: A Survey](https://arxiv.org/abs/2312.10997) encuesta exhaustiva del RAG.
> - [Rajpurkar et al. (2016). SQuAD: 100,000+ Questions for Machine Comprehension of Text](https://arxiv.org/abs/1606.05250) 基准论文──
- [Karpukhin et al. (2020). Dense Passage Retrieval for Open-Domain QA](https://arxiv.org/abs/2004.04906) DPR, 问答的经典密检索器──
- [Lewis et al. (2020). Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks](https://arxiv.org/abs/2005.11401) 命名 RAG 的论文──
- [Gao et al. (2023). Retrieval-Augmented Generation for Large Language Models: A Survey](https://arxiv.org/abs/2312.10997) 综合 RAG 综述。
