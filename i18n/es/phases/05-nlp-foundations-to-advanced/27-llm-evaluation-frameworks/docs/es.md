# LLM Evaluación  RAGAS, DeepEval, G-Eval  LLM  evaluación  RAGAS DeepEval

> La comparación exacta y la F1 no tienen equivalencia semántica. La revisión humana no escala. LLM-as-judge es la respuesta de producción  con suficiente calibración para confiar en el número.
> 精确匹配和 F1 捕捉不到语义等价――la revisión artificial no se puede ampliar―LLM 作为评审是生产答案经过足够的校准可以信任这个数字―

> **【中文解读】**evaluación de la calidad de la formación en LLM, incluidos los resultados de RAG  efectos.

**Type:** Learn | **类型:** 学习
**Languages:** Python | **语言:** Python
**Prerequisites:** Phase 5 · 23 (Chunking), Phase 5 · 14 (IR & Search) | **前置知识:** Phase 5 · 23（分块），Phase 5 · 14（信息检索）
**Time:** ~60 minutes | **时间:** ~60 分钟

## El problema es la introducción del problema

Su sistema RAG responde: "29 de junio de 2007". La respuesta de referencia dice: "29 de junio de 2007". La coincidencia exacta dice incorrecta. BLEU dice parcial. Un humano dice correcto. Necesitas una métrica que coincida con los humanos, se expanda a miles de resultados, y cuesta menos que la anotación humana.

> Su RAG 系统 responde:"29 de junio de 2007"."" 参考答案是:"29 de junio de 2007。" 精确匹配说错了。BLEU 说部分对──人类说正确──你需要一个与人类一致的量度,可扩展到数千输出,且成本低于人工标签──

> **【中文解读】**La pregunta planteada en este capítulo es: ¿cómo entender y aplicar correctamente esta técnica en el proyecto real?

Ahora multiplica por 10.000 casos de prueba. Multiplica de nuevo por cada actualización de modelo que quieras enviar. La evaluación humana no se escala. Necesitas métricas automatizadas que se correlacionen con el juicio humano en r ≥ 0,85.

> Ahora se multiplican con 10.000 casos de prueba. Se multiplican con cada modelo que se espera que se publique.

## El concepto central.

> **【中文解读】**Este artículo presenta la base de los conceptos y teorías centrales.

2026 tiene tres marcos que poseen este problema.

> En 2026 habrá tres marcos que orientarán este problema.

**RAGAS.**Evaluación de RAG. Evalúa la recuperación + generación conjuntamente. Métricas: fidelidad, relevancia de la respuesta, precisión de contexto, recuerdo de contexto. El estándar para la evaluación de RAG.

> **RAGAS。**RAG  evaluación. 联合评估检索和生成. 标志:忠诚度,答案相关性,上下文精确率,上下文召回率,RAG 评估标准,

**DeepEval.**Marco de pruebas unitarias para resultados de LLM. Metricas: relevancia de las respuestas, fidelidad, sesgo, toxicidad.

> **DeepEval。**La aplicación de la ley de la ley de la educación superior en los Estados Unidos es una forma de hacer que los estudiantes de la universidad puedan aprender a aprender a aprender a aprender a aprender a aprender a aprender a aprender a aprender a aprender a aprender a aprender a aprender a aprender a aprender a aprender a aprender a aprender a aprender a aprender a aprender a aprender a aprender a aprender a aprender a aprender a aprender a aprender a aprender a aprender a aprender a aprender a aprender a aprender a aprender a aprender a aprender a aprender a aprender a aprender a aprender a aprender a aprender a aprender a aprender a aprender a aprender a aprender a aprender a aprender a aprender a aprender a aprender a aprender a aprender a aprender a aprender a aprender a aprender a aprender a aprender a aprender a aprender a aprender a aprender a aprender a aprender a aprender a aprender a aprender a hacer más.
```figure
n5-judge-gauge
```

## Construye el mismo

**G-Eval.**La cadena de pensamiento que nos lleva a generar criterios de evaluación, luego a obtener resultados.

> **G-Eval。**Usar ideas para generar criterios de evaluación, luego evaluar y emitir evaluaciones.

> **【拓展：大语言模型的工程实践】**Desde el GPT hasta el ChatGPT, el campo de la NLP ha experimentado un cambio de paradigma.

> **【拓展：RAG 与企业知识库】**检索增强生成(RAG) es la arquitectura más popular de la aplicación de IA en las empresas actuales.

> **【拓展：NLP 的多语言挑战】**En todo el mundo hay más de 7000 idiomas, pero los estudios de PNL se centran principalmente en inglés y en una minoría de idiomas.

## Construye y realiza.

> **【中文解读】**Este capítulo pasa por el código desde el núcleo de algoritmos de implementación de cero.

```python
from ragas import evaluate
from ragas.metrics import faithfulness, answer_relevancy, context_precision

# Evaluate RAG pipeline
results = evaluate(
    dataset=rag_dataset,
    metrics=[faithfulness, answer_relevancy, context_precision],
    llm=judge_llm,
    embeddings=embed_model,
)
print(results)
```

```python
from deepeval import assert_test
from deepeval.metrics import FaithfulnessMetric

metric = FaithfulnessMetric(threshold=0.7, model="gpt-4")
assert_test(test_case, [metric])
```

> **【中文解读】**Este capítulo muestra cómo utilizar un marco maduro para aplicar rápidamente esta tecnología.

> **【拓展：Prompt Engineering 与 LLM 应用】**La ingeniería rápida se ha convertido en la habilidad central de los ingenieros de PNL.

## Usalo con el marco de ejecución

> **【中文解读】**Este apartado se centra en cómo el modelo se desplegará en productos disponibles.

| Framework / 框架 | Focus / 重点 | Best for / 最适合 |
|---------|--------|---------|
| RAGAS | RAG evaluation / RAG 评估 | Retrieval + generation / 检索 + 生成 |
| DeepEval | Unit testing / 单元测试 | CI/CD integration / CI/CD 集成 |
| G-Eval | Research / 研究 | Custom metrics / 自定义指标 |

## Envíe el producto .

Salvo como`outputs/skill-llm-eval.md`¿Qué es esto ?

> 保存为                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           `outputs/skill-llm-eval.md`¿Qué es esto ?

```markdown
Given an LLM application (chatbot, RAG, agent), design evaluation pipeline.
1. Framework (RAGAS, DeepEval, G-Eval).
2. Metrics to track.
3. Calibration against human labels.
```

## Los ejercicios.

1. **Easy.**Evaluar una simple tubería de RAG con RAGAS. / **简单。**Usar RAGAS  evaluación simple RAG 流水线──
2. **Medium.**Construir una suite de pruebas DeepEval para un chatbot.**中等。**Por qué no se trata de un proyecto de investigación?
3. **Hard.**Calibra la LLM como juez contra 200 etiquetas humanas.**困难。**Con 200 personas en el programa de evaluación de la LLM.

## Términos clave .

| Term / 术语 | What it means / 含义 |
|------|-----------------------|
| RAGAS | RAG evaluation framework. / RAG 评估框架。 |
| Faithfulness（忠实度） | Answer is supported by context. / 答案有上下文支持。 |
| LLM-as-judge | LLM evaluates other LLM outputs. / LLM 评估其他 LLM 输出。 |

## Más Leer más Leer más

- [RAGAS](https://docs.ragas.io/) Marco de evaluación de los RAG. / RAG  evaluación marco。
- [DeepEval](https://docs.confident-ai.com/) Prueba de unidad de LLM. / LLM 单元测试。
- [G-Eval](https://arxiv.org/abs/2303.16634) evaluación de la cadena de pensamiento. / 思维链评估。
