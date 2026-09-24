# Relación extracción y conocimiento gráfico construcción de relaciones extracción y gráficos de conocimiento construcción

> NER encontró las entidades. la entidad que une las ancla. la extracción de relaciones encuentra los bordes entre ellos. un gráfico de conocimiento es la suma de nodos, bordes y su procedencia.
> NER 找到了实体──实体链接定了它们──关系抽取找到它们之间的边──知识图谱是节点、边及其来源的总和──

> **【中文解读】**Desde el texto extraer relaciones entre los cuerpos, construir un panorama de conocimiento.

**Type:** Learn | **类型:** 学习
**Languages:** Python | **语言:** Python
**Prerequisites:** Phase 5 · 06 (NER), Phase 5 · 25 (Entity Linking) | **前置知识:** Phase 5 · 06（NER），Phase 5 · 25（实体链接）
**Time:** ~60 minutes | **时间:** ~60 分钟

## El problema es la introducción del problema

Relación Extracción (RE) convierte el texto libre en triples estructurados: (sujeto, relación, objeto). "Apple fue fundada por Steve Jobs" → (Apple, fundado_por Steve Jobs). El conocimiento gráfica sistemas de recomendación de potencia, respuesta a preguntas, descubrimiento de medicamentos y monitoreo de cumplimiento.

> 关系抽取(RE)将自由文本转化为结构化三元组:(主语, 关系, 宾语) ・・・"Apple fue fundada por Steve Jobs" → (Apple, fundada_por Steve Jobs) ・・・知识图驱动推系统、问答、药物发现和合规监控。

> **【中文解读】**La pregunta planteada en este capítulo es: ¿cómo entender y aplicar correctamente esta técnica en el proyecto real?

El problema de 2026: los LLM extraen relaciones con entusiasmo pero alucinan bordes que no existen en el texto fuente.

> En la construcción de los gráficos de conocimiento de producción, la precisión es más importante que la tasa de recuperación.

## El concepto central.

> **【中文解读】**Este artículo presenta la base de los conceptos y teorías centrales.

**Supervised RE.**Entrenamiento de un clasificador en ejemplos de relaciones etiquetadas. Entrada: oración + par de entidades. salida: tipo de relación. Requiere datos etiquetados.

> **有监督 RE。**En el ejemplar de etiquetado de relaciones entrenamiento en los grupos de datos.

**Distant supervision.**Alinear el texto con los triples KB existentes. Si (A, born_in, B) existe en el KB, cualquier oración que mencione tanto A como B es un ejemplo positivo.

> **远程监督。**Cuando el texto se encuentra en el conocimiento existente, cualquier frase que se mencione en el mismo tiempo en el mismo es normal.

**LLM-based RE.**Promueve el LLM para extraer relaciones.

> **基于 LLM 的 RE。**提示 LLM 抽取关系──高召回率,精确率不稳定──需要验证──

> **【拓展：大语言模型的工程实践】**Desde el GPT hasta el ChatGPT, el campo de la NLP ha experimentado un cambio de paradigma.

> **【拓展：RAG 与企业知识库】**检索增强生成(RAG) es la arquitectura más popular de la aplicación de IA en las empresas actuales.
```figure
relation-triples
```

## Construye el mismo

> **【拓展：NLP 的多语言挑战】**En todo el mundo hay más de 7000 idiomas, pero los estudios de PNL se centran principalmente en inglés y en una minoría de idiomas.

## Construye y realiza.

> **【中文解读】**Este capítulo pasa por el código desde el núcleo de algoritmos de implementación de cero.

```python
def extract_relations(text, entities, llm):
    prompt = f"""Extract all relations between entities from this text.
Text: {text}
Entities: {entities}
Output as JSON list of {{"subject": "...", "relation": "...", "object": "..."}}."""
    return llm(prompt)
```

> **【中文解读】**Este capítulo muestra cómo utilizar un marco maduro para aplicar rápidamente esta tecnología.

> **【拓展：Prompt Engineering 与 LLM 应用】**La ingeniería rápida se ha convertido en la habilidad central de los ingenieros de PNL.

## Usalo con el marco de ejecución

> **【中文解读】**Este apartado se centra en cómo el modelo se desplegará en productos disponibles.

- **spaCy + RE models.**El proyecto de producción de RE. / spaCy + RE 模型──生产 RE 流水线──
- **Hugging Face RE models.**BERT afinado para la clasificación de las relaciones. / Embracing Face RE 模型。
- **LLM + verification.**Extraer con LLM, verificar en relación con la fuente. / LLM + 验证。
- **Neo4j.**Almacenar y consultar los gráficos de conocimiento. / Neo4j── almacenamiento y consulta

## Envíe el producto .

Salvo como`outputs/skill-re-kg-builder.md`¿Qué es esto ?

> 保存为                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           `outputs/skill-re-kg-builder.md`¿Qué es esto ?

```markdown
Given a corpus and entity types, build a knowledge graph.
1. RE approach (supervised, distant supervision, LLM).
2. Verification strategy (precision vs recall).
3. KG storage (Neo4j, RDF, property graph).
```

## Los ejercicios.

1. **Easy.**Extraer relaciones de 10 frases usando patrones de regex. / **简单。**Usando el modelo correcto de 10 frases de extracción de relaciones.
2. **Medium.**La clasificación de las relaciones en TACRED debe ajustarse a un modelo BERT. / **中等。**En TACRED 上微调 BERT 关系分类模型──
3. **Hard.**Construir un oleoducto completo de KG: NER → EL → RE → Neo4j. / **困难。**Construir un KG completo de agua.

## Términos clave .

| Term / 术语 | What it means / 含义 |
|------|-----------------------|
| Relation extraction（关系抽取） | Extract (subject, relation, object) triples from text. / 从文本提取三元组。 |
| Knowledge graph（知识图谱） | Structured graph of entities and relations. / 实体和关系的结构化图。 |
| Distant supervision（远程监督） | Auto-label using existing KB. / 用现有知识库自动标注。 |

## Más Leer más Leer más

- [TACRED](https://nlp.stanford.edu/pubs/tacred17.pdf) Relación de extracción de conjunto de datos. / 关系抽取数据集──
- [Neo4j](https://neo4j.com/) base de datos gráfica. / 图数据库。
