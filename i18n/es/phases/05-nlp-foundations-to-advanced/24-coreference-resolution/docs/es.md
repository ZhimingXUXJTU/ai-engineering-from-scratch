# Resolución de correferencia.

> "Le llamó, no contestó, el médico estaba al almuerzo". Tres referencias a dos personas y nadie es nombrado.
> "El médico estaba al almuerzo".

> **【中文解读】**Los nombres y los nombres en el texto están enlazados a los elementos que los indican.

**Type:** Learn | **类型:** 学习
**Languages:** Python | **语言:** Python
**Prerequisites:** Phase 5 · 06 (NER), Phase 5 · 07 (POS & Parsing) | **前置知识:** Phase 5 · 06（NER），Phase 5 · 07（POS 与解析）
**Time:** ~45 minutes | **时间:** ~45 分钟

## El problema es la introducción del problema

La resolución de Coreference une todas las expresiones que se refieren a la misma entidad. "Barack Obama", "el presidente", "él", "Obama" apuntan a una persona. Sin ella, su sistema NER informa cuatro entidades en lugar de una, sus fragmentos de gráfico de conocimiento, y su resumen deja caer los temas en medio del documento.

> 共指消解将每个指向同一实体的表达链接起――"Barack Obama""",el presidente""",el""",Obama"都指向一个人──没有它,你的NER 系统报告四个实体而不是一个,知识图碎,摘要器在文档中间丢弃主语──

> **【中文解读】**La pregunta planteada en este capítulo es: ¿cómo entender y aplicar correctamente esta técnica en el proyecto real?

Por qué importa en 2026: LLM manejan la coreferencia implícitamente dentro de su ventana de contexto, pero la recuperación RAG todavía necesita resolución explícita. Si un usuario pregunta "¿qué dijo?", el recuperador necesita saber quién es "ella" antes de poder encontrar la pieza correcta.

> Por qué 2026 años: LLM en la ventana de arriba abajo tiene que resolver el problema, pero RAG 检索 todavía necesita una desintegración clara. Si el usuario pregunta "¿qué dijo?", el buscador necesita saber "quién es ella" antes de encontrar el bloque correcto.

## El concepto central.

> **【中文解读】**Este artículo presenta la base de los conceptos y teorías centrales.

**Mention detection.**Encuentra todas las frases y pronombres de sustantivos que puedan referirse a una entidad.

> **指称检测。**找到所有可能指向实体名词短语和代词──使用 POS 标签和分析树──

**Coreference clustering.**Los grupos mencionan que se refieren a la misma entidad. Clasificadores de pares de mención, modelos basados en el período de tiempo o enfoques neuronales de extremo a extremo (Lee et al., 2017).

> **共指聚类。**Se refiere a la misma entidad en el denominado grupo de grupos. Se refiere a los grupos de grupos, basados en modelos o métodos neurológicos de extremo a extremo.

> **【拓展：大语言模型的工程实践】**Desde GPT hasta ChatGPT, el campo de NLP ha experimentado un cambio de paradigma de "cada tarea entrenar un modelo" a "un modelo resolver todas las tareas".

> **【拓展：RAG 与企业知识库】**检索增强生成(RAG) es la arquitectura más popular de la aplicación de IA en las empresas actuales.

> **【拓展：NLP 的多语言挑战】**En todo el mundo hay más de 7000 idiomas, pero los estudios de PNL se centran principalmente en inglés y en una minoría de idiomas.
```figure
coref-links
```

## Construye el mismo

## Construye y realiza.

> **【中文解读】**Este capítulo pasa por el código desde el núcleo de algoritmos de implementación de cero.

```python
import spacy

nlp = spacy.load("en_core_web_sm")

def resolve_coref(text):
    doc = nlp(text)
    clusters = {}
    for token in doc:
        if token.pos_ == "PRON":
            # Simple heuristic: look for nearest preceding noun
            for t in reversed(list(doc[:token.i])):
                if t.pos_ in ("NOUN", "PROPN"):
                    clusters[token.text] = t.text
                    break
    return clusters
```

> **【中文解读】**Este capítulo muestra cómo utilizar un marco maduro para aplicar rápidamente esta tecnología.

> **【拓展：Prompt Engineering 与 LLM 应用】**La ingeniería rápida se ha convertido en la habilidad central de los ingenieros de PNL.

## Usalo con el marco de ejecución

> **【中文解读】**Este apartado se centra en cómo el modelo se desplegará en productos disponibles.

- **spaCy with coreferee.**Coreferencia de producción para inglés. / spaCy + coreferee。英语生产共指。
- **Hugging Face span-based models.**Resolución de coreferencia neuronal. / Abrazando la cara 基于跨度的模型──
- **LLM prompting.**Pida al LLM que resuelva las referencias básicas. Buena precisión, alto costo.

## Envíe el producto .

Salvo como`outputs/skill-coref-picker.md`¿Qué es esto ?

> 保存为                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           `outputs/skill-coref-picker.md`¿Qué es esto ?

```markdown
Given a text and need for entity tracking, pick coreference approach.
1. Rule-based vs neural vs LLM.
2. Language support.
3. Latency budget.
```

## Los ejercicios.

1. **Easy.**Implemente la resolución del pronombre utilizando etiquetas de POS. / **简单。**Usar POS 标签实现代词消解──
2. **Medium.**Evaluar a los participantes en el estudio en un corpus de 50 frases.**中等。**En 50 palabras, evalúa el espacio y el tema central.
3. **Hard.**Construir un preprocesador RAG que resuelva las coreferencias antes de la fragmentación. / **困难。**Construido en el segmento anterior 消解共指 de RAG 预处理器──

## Términos clave .

| Term / 术语 | What it means / 含义 |
|------|-----------------------|
| Coreference（共指） | Multiple expressions referring to the same entity. / 多个表达指向同一实体。 |
| Mention（指称） | A textual reference to an entity. / 对实体的文本引用。 |
| Anaphora（回指） | Pronoun referring to an earlier noun. / 代词指向前面的名词。 |

## Más Leer más Leer más

- [Lee et al. (2017). End-to-end Neural Coreference Resolution](https://arxiv.org/abs/1707.07045) el enfoque basado en el espacio. / 基于跨度的方法──
- [coreferee](https://github.com/explosion/coreferee) espaCy coreference plugin. / spaCy 共指插件──
