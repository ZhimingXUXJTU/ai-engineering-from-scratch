# Inferencia de lenguaje natural  Entención textual   文本含

> "t implica h" significa que una lectura humana t concluiría que h es verdad. NLI es la tarea de predecir implicación / contradicción / neutral.
> "t 含 h" significa que el hombre leído 后会推断 h 为真──NLI es el pre测 含/矛盾/中性的任务──表面无聊,生产中承重──

> **【中文解读】**NLI 判断两个句子之间的逻辑关系: 含、矛盾、中性──

**Type:** Learn | **类型:** 学习
**Languages:** Python | **语言:** Python
**Prerequisites:** Phase 5 · 05 (Sentiment Analysis), Phase 5 · 10 (Attention) | **前置知识:** Phase 5 · 05（情感分析），Phase 5 · 10（注意力机制）
**Time:** ~45 minutes | **时间:** ~45 分钟

## El problema es la introducción del problema

¿Cómo sabes que el "sí" está respaldado por la evidencia? Necesitas clasificar 10.000 artículos de noticias por tema. Tienes 50 ejemplos etiquetados. Lo conviertes en NLI: "este artículo es sobre {tema}"  implicación o contradicción? Necesitas comprobar si un resumen generado es fiel a la fuente. NLI otra vez.

> Usted ha construido un chatbot. Usted ha respondido "sí" y ha dicho "sí" y ha dicho "sí" y ha dicho "sí" y ha dicho "sí" y ha dicho "sí" y ha dicho "sí" y ha dicho "sí" y ha dicho "sí" y ha dicho "sí" y ha dicho "sí" y ha dicho "sí" y ha dicho "sí" y ha dicho "sí" y ha dicho "sí" y ha dicho "sí" y ha dicho "sí" y ha dicho "sí" y ha dicho "sí" y ha dicho "sí" y ha dicho "sí" y ha dicho "sí" y ha dicho "sí" y ha dicho "sí" y ha dicho "sí" y ha dicho "sí" y ha dicho "sí" y ha dicho "sí" y ha dicho "sí" y ha dicho "sí" y ha dicho "sí" y ha dicho "sí" y ha dicho "sí" y ha dicho "sí" y ha dicho "sí" y ha dicho "sí" y "sí" y "sí" y "sí" y "sí" y "sí" y "sí" y "sí" y " sí" y "sí" y " sí" y " sí" y " sí" y " sí" en sí " sí" y " sí" en sí " sí" y " sí " sí" en sí " sí" y " sí " sí" en sí " sí" en sí " sí " sí" en sí " sí " sí" en sí " sí" en sí " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " "

> **【中文解读】**La pregunta planteada en este capítulo es: ¿cómo entender y aplicar correctamente esta tecnología en la ingeniería real? Comprender el contexto de la cuestión ayuda a comprender los puntos clave de decisión del tipo de selección técnica. En los sistemas de IA reales, el tipo de selección técnica errónea suele ser más alto que el costo de error de la realización de detalles.

Los tres problemas se reducen a la inferencia del lenguaje natural. NLI es la tarea de columna vertebral que admite la verificación de hechos, la clasificación de tiro cero, la evaluación de resumen y la verificación de recuperación.

> Estos tres problemas se reducen a la teoría del lenguaje natural. Los NLI son las tareas básicas de la investigación de hechos, la evaluación de muestras y la investigación de ensayos.

## El concepto central.

> **【中文解读】**Este capítulo presenta los conceptos y teorías básicos. La comprensión de estos conceptos es el prerrequisito de la realización posterior de la actividad, y también el conocimiento de los puntos de alta frecuencia de la entrevista y la práctica de la ingeniería.

**The task.**Dado el supuesto `t`y la hipótesis.`h`, clasificar su relación como una de: Entraño (t implica h), Contradición (t contradice h), Neutral (ninguno de los dos).

> **任务。**                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             `t`Y las hipótesis`h`,将它们的关系分类为: 含含 h) 矛盾t 矛盾 h) 中性都不是) ∼三分类──

**Cross-encoder approach.**Concatenate t y h, alimenta a través de un transformador, clasifica. Se utiliza para aplicaciones críticas de precisión. Lento porque ejecutas el modelo completo para cada par.

> **交叉编码器方法。**拼接 t 和 h,通过 Transformer,分类──用于准确率关键的应用──慢因为每对运行完整模型──

**Bi-encoder approach.**Encodizar t y h por separado, comparar los embebidos (similaridad de cosinos).

> **双编码器方法。**Se trata de un sistema de control de la velocidad de un eje de un eje de un eje de un eje de un eje de un eje de un eje de un eje de un eje de un eje de un eje de un eje de un eje de un eje de un eje de un eje de un eje de un eje de un eje de un eje de un eje de un eje de un eje de un eje de un eje de un eje de un eje de un eje de un eje de un eje de un eje de un eje de un eje de un eje de un eje de un eje de un eje de un eje de un eje de un eje de un eje de un eje de un eje de un eje de un eje de un eje de un eje de un eje de un eje de un eje de un eje de un eje de un eje de un eje de un eje de un eje de un eje de un eje de un eje de un eje de un eje de un eje de un eje de un eje de un eje de un eje de un eje de un eje de un eje de un eje de un eje de un eje de un eje de un eje de un eje de un eje de un eje de un eje de un eje de un eje de un eje de un eje de un eje de un eje de un eje de un eje de un eje de un eje de un eje de un eje de un eje de un eje de un eje de un eje de un eje de un eje de un eje de un eje de un eje de un eje de un eje de un eje de un eje de un eje de un eje de un eje de un eje de un eje de un eje de un eje de un eje de un eje de un eje de un eje de un eje de un eje de un eje de un eje de un eje de un eje de un eje de un eje de un eje de un eje de un eje de un eje de un eje de un eje de un eje de un eje de un eje de un eje de un eje de un eje de un eje de un eje de un eje de un eje de un eje de un eje de un eje de un eje de un eje de un eje de un eje de un eje de un eje de un eje de un eje de un eje de un eje de un eje de un eje de un eje de un eje de un eje de un eje de un eje de un eje de un eje de un eje de un eje de un eje de un eje de un eje de un eje de

> **【拓展：大语言模型的工程实践】**Desde GPT hasta ChatGPT, el campo de NLP ha experimentado un cambio de paradigma de "cada tarea entrenar un modelo" a "un modelo resolver todas las tareas". En el proyecto real, la implementación de LLM necesita considerar los problemas de token 限制,延迟,成本, seguridad etc.

> **【拓展：RAG 与企业知识库】**检索增强生成(RAG) es la estructura más popular de las aplicaciones de IA de las empresas actuales: la consulta de usuarios primero se consulta los documentos relacionados, luego se vuelve a buscar los resultados como respuesta a la pregunta de LLM.
```figure
nli-router
```

## Construye el mismo

> **【拓展：NLP 的多语言挑战】**En todo el mundo hay más de 7000 idiomas, pero los estudios de PNL se centran principalmente en inglés y en una minoría de idiomas.

## Construye y realiza.

> **【中文解读】**Este capítulo a través del código de la implementación de algoritmos centrales de cero. Este método "desde cero" puede ayudar a entender el principio detrás del marco, no se encuentra en la caja negra cuando se encuentran problemas.

### Paso 1: Clasificación de disparos cero a través de NLI

```python
from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch

tok = AutoTokenizer.from_pretrained("roberta-large-mnli")
model = AutoModelForSequenceClassification.from_pretrained("roberta-large-mnli")

def nli_classify(premise, hypothesis):
    inputs = tok(premise, hypothesis, return_tensors="pt", truncation=True)
    with torch.no_grad():
        logits = model(**inputs).logits[0]
    # 0=contradiction, 1=neutral, 2=entailment
    probs = torch.softmax(logits, dim=-1)
    labels = ["contradiction", "neutral", "entailment"]
    return {labels[i]: probs[i].item() for i in range(3)}

print(nli_classify("A man is playing guitar.", "Someone is making music."))
```

> **【中文解读】**Este capítulo muestra cómo utilizar un marco de desarrollo rápido para aplicar esta tecnología.

> **【拓展：Prompt Engineering 与 LLM 应用】**La ingeniería rápida se ha convertido en la habilidad central de los ingenieros de PNL. Desde la Cero-Shot hasta la Few-Shot, desde la Cadena de Pensamiento hasta la Reacción, diferentes estrategias de sugerencias se aplican a diferentes escenarios.

## Usalo con el marco de ejecución

> **【中文解读】**Este capítulo se centra en cómo se puede implementar el modelo como producto disponible. Desde el modelo original hasta el sistema de producción, se deben considerar múltiples dimensiones de optimización de rendimiento, tratamiento de errores, control, etc.

La pila de NLI de producción:

> Producción de PNL 技术:

- **Zero-shot classification:**Modelos de NLI (DeBERTa-v3-grande-mnli).
- **Fact verification:**NLI de codificación cruzada en reclamación contra evidencia.
- **Summary faithfulness:**Revisa cada frase resumida en relación con la fuente. / 摘要忠实度:检查每个摘要句子与源。
- **RAG grounding:**Verify el contexto recuperado admite la respuesta. / RAG 定:验证检索上下文支持答案──

## Envíe el producto .

Salvo como`outputs/skill-nli-applications.md`¿Qué es esto ?

> 保存为                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           `outputs/skill-nli-applications.md`¿Qué es esto ?

```markdown
Given a production need (fact-checking, zero-shot classification, summary evaluation), design the NLI pipeline.
1. Model choice. Cross-encoder (accuracy) or bi-encoder (speed).
2. Input format. Premise-hypothesis pairs.
3. Evaluation. Accuracy on labeled NLI datasets.
```

> **【中文解读】**练习题按照易/中级/难三度递进;;建议至少完成中级题;;

## Los ejercicios.

1. **Easy.**Usar`roberta-large-mnli`para la clasificación de temas de tiro cero en 20 frases. / **简单。**Uso `roberta-large-mnli`Para 20 frases hacer zumbido de temas de la clase.
2. **Medium.**Construir un comprobador de fidelidad de resumen utilizando NLI. Evalúa en CNN/DailyMail. / **中等。**Utilizando NLI 构建摘要忠诚度检查器──在 CNN/DailyMail 上评估──
3. **Hard.**Comparar el cross-encoder con el bi-encoder NLI para la verificación de respuestas RAG.**困难。**Comparar el codificador de intercambio con el codificador de doble NLI para RAG  respuesta de verificación.

## Términos clave .

| Term / 术语 | What people say / 人们常说的 | What it actually means / 实际含义 |
|------|-----------------|-----------------------|
| NLI（自然语言推理） | Entailment task / 蕴含任务 | Classify premise-hypothesis pairs as entailment/contradiction/neutral. / 将前提-假设对分类为蕴含/矛盾/中性。 |
| Cross-encoder（交叉编码器） | Joint encoding / 联合编码 | Encode both texts together through the full model. / 通过完整模型联合编码两个文本。 |
| Bi-encoder（双编码器） | Separate encoding / 分离编码 | Encode each text independently, compare embeddings. / 独立编码每个文本，比较嵌入。 |

## Más Leer más Leer más

- [Bowman et al. (2015). SNLI](https://nlp.stanford.edu/pubs/snli_paper.pdf) el conjunto de datos de Stanford NLI. / Stanford NLI 数据集──
- [He et al. (2021). DeBERTa v3](https://arxiv.org/abs/2111.09543) Modelo de NLI de última generación. / 先进 NLI 模型。
