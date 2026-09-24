# Producciones estructuradas y decodificación restringida                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                  

> En la producción, "la mayoría" es el problema. La decodificación restringida se convierte en "la mayoría" en "siempre" mediante la edición de los logits antes de la muestreo.
> 让LLM 输出 JSON──大多数时候能得到 JSON──在生产中,"大多数"就是问题──约束解码通过在采样前编辑逻辑将"大多数"变成"总是"──

> **【中文解读】**让LLM 输出结构化数据如JSON、SQL──

**Type:** Learn | **类型:** 学习
**Languages:** Python | **语言:** Python
**Prerequisites:** Phase 5 · 19 (Subword Tokenization) | **前置知识:** Phase 5 · 19（子词分词）
**Time:** ~60 minutes | **时间:** ~60 分钟

## El problema es la introducción del problema

La generación de formularios libres no es un contrato. Es una sugerencia. Si pides JSON, obtienes una cadena en forma de JSON con una coma posterior, un backtick adicional o una clave llamada en alemán. Cada parser descendente se rompe. Si pides una consulta SQL, obtienes una con un nombre de columna alucinado. En la producción, estos fallos no son errores  son incidentes.

> La generación de formato libre no es un acuerdo, es una recomendación. Usted solicita JSON, obtendrá una contagia de tiempo, un número de respuestas de tiempo o un número de respuestas de tiempo en alemán. Cada un de los dispositivos de resolución se derrumbará. Usted solicita una consulta de SQL, obtendrá una lista de datos.

> **【中文解读】**La pregunta planteada en este capítulo es: ¿cómo entender y aplicar correctamente esta tecnología en la ingeniería real? Comprender el contexto de la cuestión ayuda a comprender los puntos clave de decisión del tipo de selección técnica. En los sistemas de IA reales, el tipo de selección técnica errónea suele ser más alto que el costo de error de la realización de detalles.

Tres capas existen en 2026.

> En 2026 existe un esquema de tres niveles.

1. **Prompting.**Pregunte bien. "Retorn sólo el objeto JSON". Funciona entre el 85 y el 95% del tiempo. Fallece en casos de borde, salidas largas e entradas adversarias. / **提示。**Buena buena solicitud―" sólo devuelve JSON a los objetos―" aproximadamente 85-95% del tiempo válido― en la situación fronteriza、 largo salida y resistencia a la entrada―
2. **Constrained decoding.**Enmascarar logits de next-token inválidos en cada paso de generación para que la salida siempre se ajuste a un esquema (esquema JSON, regex, gramática libre de contexto). Funciona 100%.**约束解码。**En cada paso de generación, bloquear los logitos de los siguientes tokens, haciendo que el output siempre cumpla con el modelo.
3. **Tool/function calling.**La salida estructurada a través de la interfaz de llamada de herramienta nativa del modelo. El modelo emite un objeto JSON directamente, no como texto. La mejor latencia, mejor confiabilidad, pero específico para el modelo. / **工具/函数调用。**通过模型原生工具调用接口的结构化输出──最佳延迟,最佳可靠性,但模型特定──

## El concepto central.

> **【中文解读】**Este capítulo presenta los conceptos y teorías básicos. La comprensión de estos conceptos es el prerrequisito de la realización posterior de la actividad, y también el conocimiento de los puntos de alta frecuencia de la entrevista y la práctica de la ingeniería.

**Logit masking.**En cada paso de generación, el modelo produce una distribución de probabilidades sobre el vocabulario. La decodificación restringida calcula el conjunto de tokens válidos siguientes (dado el esquema y lo que se ha generado hasta ahora) y establece todas las demás logits a -inf antes de softmax.

> **Logit 屏蔽。**En cada paso de generación, el modelo en la lista de palabras genera una probabilidad de distribución.

**JSON schema constraints.**Para la salida de JSON, la restricción se aplica: los brackets de apertura coinciden con los braces de cierre, las claves se citan cadenas, los valores coinciden con sus tipos declarados, los campos requeridos están presentes, no hay campos adicionales más allá del esquema. Esta es una restricción gramatical sin contexto, calculada incrementalmente.

> **JSON 模式约束。** Para JSON 输出,约束强制:开闭括号匹配、键是带引号字符串、值匹配声明类型、必填字段存在、无模式外额外字段── es un 上下文无关语法约束,增量计算──

> **【拓展：大语言模型的工程实践】**Desde GPT hasta ChatGPT, el campo de NLP ha experimentado un cambio de paradigma de "cada tarea entrenar un modelo" a "un modelo resolver todas las tareas". En el proyecto real, la implementación de LLM necesita considerar los problemas de token 限制,延迟,成本, seguridad etc.

> **【拓展：RAG 与企业知识库】**检索增强生成(RAG) es la estructura más popular de las aplicaciones de IA de las empresas actuales: la consulta de usuarios primero se consulta los documentos relacionados, luego se vuelve a buscar los resultados como respuesta a la pregunta de LLM.

> **【拓展：NLP 的多语言挑战】**En todo el mundo hay más de 7000 idiomas, pero los estudios de PNL se centran principalmente en inglés y en una minoría de idiomas.

## Construye y realiza.
```figure
constrained-decoder
```

## Construye el mismo

> **【中文解读】**Este capítulo a través del código de la implementación de algoritmos centrales de cero. Este método "desde cero" puede ayudar a entender el principio detrás del marco, no se encuentra en la caja negra cuando se encuentran problemas.

### Paso 1: mascaramiento de la lógica simple

```python
import json
import re


def mask_logits(logits, valid_token_ids):
    """Set invalid token logits to -inf."""
    mask = torch.full_like(logits, float('-inf'))
    mask[valid_token_ids] = logits[valid_token_ids]
    return mask
```

La idea principal: en cada paso, solo un subconjunto de tokens es válido.

> 核心洞察: en cada paso, sólo el token 子集是有效的──高效计算该子集是工程挑战──

### Paso 2: Validación de esquema JSON durante la generación

```python
import jsonschema

schema = {
    "type": "object",
    "properties": {
        "name": {"type": "string"},
        "age": {"type": "integer", "minimum": 0},
    },
    "required": ["name", "age"],
}

def validate_json_output(text, schema):
    try:
        data = json.loads(text)
        jsonschema.validate(data, schema)
        return True, data
    except (json.JSONDecodeError, jsonschema.ValidationError) as e:
        return False, str(e)
```

### Paso 3: utilizando el ejecutor de formato LM

```python
from lmformatenforcer import JsonSchemaParser, generate_enforced

parser = JsonSchemaParser(schema)
# Use with any Hugging Face model's generate method
# result = generate_enforced(model, tokenizer, parser, prompt)
```

> **【中文解读】**Este capítulo muestra cómo utilizar un marco de desarrollo rápido para aplicar esta tecnología.

> **【拓展：Prompt Engineering 与 LLM 应用】**La ingeniería rápida se ha convertido en la habilidad central de los ingenieros de PNL. Desde la Cero-Shot hasta la Few-Shot, desde la Cadena de Pensamiento hasta la Reacción, diferentes estrategias de sugerencias se aplican a diferentes escenarios.

## Usalo con el marco de ejecución

> **【中文解读】**Este capítulo se centra en cómo se puede implementar el modelo como producto disponible. Desde el modelo original hasta el sistema de producción, se deben considerar múltiples dimensiones de optimización de rendimiento, tratamiento de errores, control, etc.

Las opciones de producción para 2026:

> Producción de la producción de 2026:

| Approach / 方案 | Reliability / 可靠性 | Latency cost / 延迟成本 | Best for / 最适合 |
|---------|------------|-------------|---------|
| Prompting / 提示 | ~85-95% / 约 85-95% | None / 无 | Prototypes, non-critical paths / 原型、非关键路径 |
| Constrained decoding / 约束解码 | 100% / 100% | +10-30% / 加 10-30% | Production APIs / 生产 API |
| Tool calling / 工具调用 | ~99.9% / 约 99.9% | Lowest / 最低 | Model-native workflows / 模型原生工作流 |

## Envíe el producto .

Salvo como`outputs/prompt-structured-output.md`¿Qué es esto ?

> 保存为                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           `outputs/prompt-structured-output.md`¿Qué es esto ?

```markdown
Given an LLM output that must be structured (JSON, SQL, etc.), pick the right approach and implement it.
1. Schema definition. JSON Schema, regex, or grammar.
2. Enforcement method. Prompting, constrained decoding, or tool calling.
3. Fallback plan. What happens when the output still fails validation.
```

> **【中文解读】**Practice los temas de fácil/medio/duro  3 difficulty to pass in  Recomenda al menos completar los temas de grado medio  Grado duro  para la preparación de la entrevista

## Los ejercicios.

1. **Easy.**Construir un extractor JSON de sólo la hora. Medir la tasa de éxito en 100 llamadas LLM. / **简单。**构建纯提示的 JSON 提取器──测量 100 次 LLM 调用成功率──
2. **Medium.**Implemente la decodificación limitada para un esquema JSON simple utilizando el enmascaramiento de logit. / **中等。**Utiliza logit 屏蔽为简单 JSON 模式实现约束解码──
3. **Hard.**Comparar la decodificación limitada con la herramienta que requiere una carga de trabajo de producción.**困难。**En la producción de trabajo, comparación entre la capacidad de desbloqueo y la utilización de herramientas.

> **【中文解读】**En el lenguaje de los términos "Lo que la gente dice" vs "Lo que realmente significa" se distingue entre el lenguaje diario y la definición técnica de significado.

## Términos clave .

| Term / 术语 | What people say / 人们常说的 | What it actually means / 实际含义 |
|------|-----------------|-----------------------|
| Constrained decoding（约束解码） | Force valid output / 强制有效输出 | Mask invalid logits at each step. / 每步屏蔽无效 logits。 |
| Logit masking（Logit 屏蔽） | Block bad tokens / 阻止坏 token | Set invalid token logits to -inf before softmax. / softmax 前将无效 token logits 设为 -inf。 |
| JSON Schema | JSON validation rules / JSON 验证规则 | Declarative schema for validating JSON structure and types. / 验证 JSON 结构和类型的声明式模式。 |
| Tool calling（工具调用） | Function calling / 函数调用 | Model emits structured arguments directly via native interface. / 模型通过原生接口直接发出结构化参数。 |

> **【中文解读】**延伸阅读 proporciona un alto nivel de recursos para el aprendizaje profundo. Estos artículos y cursos son los referentes clásicos en el campo, adecuados para los lectores que necesitan una comprensión profunda.

## Más Leer más Leer más

- [LM Format Enforcer](https://github.com/noamgat/lm-format-enforcer) la producción limitada de la biblioteca de decodificación. / 生产级约束解码库。
- [Outlines](https://github.com/dottxt-ai/outlines) generación estructurada con regex/JSON/CFG. / 带 regex/JSON/CFG 的结构化生成──
- [JSON Schema specification](https://json-schema.org/) el estándar para la validación JSON. / JSON 验证标准。
