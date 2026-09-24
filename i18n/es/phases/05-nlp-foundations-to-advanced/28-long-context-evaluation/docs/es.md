# Evaluar el contexto largo  NIAH, RULER, LongBench, MRCR 长上下文评估  NIAH、RULER

> Gemini 3 Pro anuncia 10M tokens de contexto. En 1M tokens, el MRCR de 8 agujas cae a 26.3%. Publicado ≠ utilizable.
> Gemini 3 Pro 宣称10M token 上下文──在1M token 时,8-agullas MRCR 降至26.3%──宣称的 ≠可用──长上下文评估告诉你你正在部署模型的实际能力──

> **【中文解读】** evaluación de la actuación real en la ventana de LLM

**Type:** Learn | **类型:** 学习
**Languages:** Python | **语言:** Python
**Prerequisites:** Phase 5 · 27 (LLM Evaluation) | **前置知识:** Phase 5 · 27（LLM 评估）
**Time:** ~45 minutes | **时间:** ~45 分钟

## El problema es la introducción del problema

Esta es la brecha de capacidad de contexto de 2026. Las hojas de especificaciones dicen 1M tokens. Los puntos de referencia dicen: en 100K tokens, la precisión de recuperación disminuye 15-40%. en 500K, disminuye 40-70%. El modelo no "ve" todo en su ventana de contexto de la misma manera.

> Es la diferencia de capacidad de los modelos de 2026 años. La configuración dice 1M de tokens.

> **【中文解读】**La pregunta planteada en este capítulo es: ¿cómo entender y aplicar correctamente esta técnica en el proyecto real?

La evaluación de largo contexto mide estos ejes: precisión de recuperación en diferentes profundidades, razonamiento multi-hop entre documentos y agregación sobre información distribuida.

> 长上下文评估测量: las diferentes profundidades de la búsqueda de precisión, la multiplantación de los archivos, así como la acumulación de información distribuida.

## El concepto central.

> **【中文解读】**Este artículo presenta la base de los conceptos y teorías centrales.

**NIAH (Needle in a Haystack).**Insertar un hecho específico en un documento largo en varias posiciones. Pídale al modelo que lo recupere. Medidas: ¿puede el modelo encontrar una aguja a la profundidad X en un pajar de heno con símbolo Y?

> **NIAH（大海捞针）。**En cada posición del archivo largo, se insertan hechos específicos. ¿Puede el modelo encontrar una aguja en la profundidad X del token Y?

**RULER.**Extiende la NIAH con tareas de múltiples agujas, distancia variable y agregación.

> **RULER。**Extensión de la NIAH  Añadir múltiples puntos                                                                                                                                                                                                                                                        

**LongBench.**Las tareas de contexto largo del mundo real: resumen, calificación, recuperación, código. Más representativas que los puntos de referencia sintéticos.

> **LongBench。**En el caso de los grupos de trabajo, el trabajo de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de las organizaciones de las organizaciones de la organización de las organizaciones de las organizaciones de la organización de las organizaciones de la organización de las organizaciones de la organización de las organizaciones de la organización de las organizaciones de la organización de las organizaciones de las organizaciones de las organizaciones de las organizaciones de los grupos de los grupos de los grupos de los grupos de los grupos de los grupos de los grupos de los grupos de los grupos de los grupos de organizaciones de los grupos de organizaciones de organizaciones de los grupos de organizaciones de organizaciones de organizaciones de organizaciones de organizaciones de los grupos de organizaciones de organizaciones de organizaciones de organizaciones de organizaciones de organizaciones de organizaciones de organizaciones de organizaciones de organizaciones de organizaciones de organizaciones de organizaciones de organizaciones de organizaciones de organizaciones de organizaciones de organizaciones de organizaciones de organizaciones de organizaciones

**MRCR (Multi-hop Reasoning over Context).**Reasonamiento que requiere conectar información a través de múltiples documentos.

> **MRCR（上下文多跳推理）。**需要跨多文档连接信息的推理──最难的长上下文测试──

> **【拓展：大语言模型的工程实践】**Desde el GPT hasta el ChatGPT, el campo de la NLP ha experimentado un cambio de paradigma.
```figure
gx-niah-decay
```

## Construye el mismo

> **【拓展：RAG 与企业知识库】**检索增强生成(RAG) es la arquitectura más popular de la aplicación de IA en las empresas actuales.

> **【拓展：NLP 的多语言挑战】**En todo el mundo hay más de 7000 idiomas, pero los estudios de PNL se centran principalmente en inglés y en una minoría de idiomas.

## Construye y realiza.

> **【中文解读】**Este capítulo pasa por el código desde el núcleo de algoritmos de implementación de cero.

### Paso 1: prueba simple de NIAH

```python
def needle_in_haystack(model, context_length, needle, needle_position):
    """Insert needle at position in a long document and test retrieval."""
    haystack = generate_irrelevant_text(context_length)
    full_text = haystack[:needle_position] + f"\n{needle}\n" + haystack[needle_position:]
    question = f"What is the secret fact hidden in the text?"
    response = model(full_text + "\n\n" + question)
    return needle.lower() in response.lower()
```

> **【中文解读】**Este capítulo muestra cómo utilizar un marco maduro para aplicar rápidamente esta tecnología.

> **【拓展：Prompt Engineering 与 LLM 应用】**La ingeniería rápida se ha convertido en la habilidad central de los ingenieros de PNL.

## Usalo con el marco de ejecución

> **【中文解读】**Este apartado se centra en cómo el modelo se desplegará en productos disponibles.

| Benchmark / 基准 | Type / 类型 | Measures / 测量 |
|---------|------|---------|
| NIAH | Synthetic / 合成 | Single-fact retrieval at depth. / 深度单事实检索。 |
| RULER | Synthetic / 合成 | Multi-needle + aggregation. / 多针 + 聚合。 |
| LongBench | Real / 真实 | Practical long-context tasks. / 实用长上下文任务。 |
| MRCR | Synthetic / 合成 | Multi-hop reasoning. / 多跳推理。 |

## Envíe el producto .

Salvo como`outputs/skill-long-context-eval.md`¿Qué es esto ?

> 保存为                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           `outputs/skill-long-context-eval.md`¿Qué es esto ?

```markdown
Given a model claiming long-context support, verify actual performance.
1. Context length to test.
2. Benchmarks to run (NIAH, RULER, LongBench).
3. Minimum acceptable accuracy at target length.
```

## Los ejercicios.

1. **Easy.**Ejecutar NIAH en un modelo a 10K y 50K tokens.**简单。**En 10K y 50K tokens arriba funcionan NIAH♪
2. **Medium.**Construir una prueba con múltiples agujas.**中等。**构建多针测试──
3. **Hard.**Comparar 3 modelos en LongBench.**困难。**En LongBench 上比较 3 个模型──

## Términos clave .

| Term / 术语 | What it means / 含义 |
|------|-----------------------|
| NIAH（大海捞针） | Insert fact in long text, test retrieval. / 在长文本中插入事实，测试检索。 |
| Context window（上下文窗口） | Maximum input length a model can process. / 模型能处理的最大输入长度。 |
| Multi-hop reasoning（多跳推理） | Connect info across multiple documents. / 跨文档连接信息。 |

## Más Leer más Leer más

- [NIAH original](https://arxiv.org/abs/2404.05460)Una aguja en un pajar.
- [RULER](https://arxiv.org/abs/2404.02372) referencia extendida de largo contexto. / 扩展长上下文基准──
- [LongBench](https://arxiv.org/abs/2308.14508) tareas de contexto largo en el mundo real.
