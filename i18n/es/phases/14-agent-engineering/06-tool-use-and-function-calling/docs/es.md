# Uso de herramientas y funciones llamadas 工具使用与函调用

> Toolformer (Schick et al., 2023) comenzó la anotación de herramientas auto supervisada. Berkeley Function Calling Leaderboard V4 (Patil et al., 2025) establece la barra de 2026: 40% agente, 30% multi-turn, 10% en vivo, 10% no en vivo, 10% alucinación. Se resuelve el giro único.

> **【中文解读】**Toolformer  abre autocontrol tool tag.  Berkeley Function Calling Leaderboard V4 define el estándar de evaluación para 2026: 40% 智能体、30% 多轮、10% 实时、10% 非实时、10% 幻觉检测.  Función de un solo ciclo de trabajo 已解决, memoria、动态决策和长链工具编排仍是开放问题.

**Type:** Build | **类型:** 构建
**Languages:** Python (stdlib) | **语言:** Python (标准库)
**Prerequisites:** Phase 14 · 01 (Agent Loop), Phase 13 · 01 (Function Calling Deep Dive) | **前置知识:** Phase 14 · 01 (Agent 循环), Phase 13 · 01 (函数调用深入)
**Time:** ~60 minutes | **时间:** ~60 分钟

## Objetivos de aprendizaje

- Explica la señal de entrenamiento auto supervisada de Toolformer: mantenga las anotaciones de la herramienta solo cuando la ejecución reduzca la pérdida de los siguientes tokens.
  Traducción:Explanar Toolformer's autocontrol training signal: sólo en ejecución reduciendo un token 损失时保留工具标注。
- Nombre de las cinco categorías de evaluación de BFCL V4 y qué medidas cada una.
  China:                                                                                                                                                                                                                                                              
- Implementar un registro de herramientas stdlib con validación de esquemas, coerción de argumentos y sandboxing de ejecución.
  En la actualidad, el sistema de registro de instrumentos de ejecución de la caja de instrumentos de la caja de cambios y de ejecución de los parámetros está en funcionamiento.
- Diagnóstico de los tres problemas abiertos 2026: cadena de herramientas de horizonte largo, toma de decisiones dinámicas y memoria.
  China: diagnóstico tres 2026 años de apertura

## El problema es la introducción del problema

El uso temprano de herramientas se preguntó: ¿puede el modelo predecir una llamada de función correcta?

> El problema del uso de herramientas tempranas es: ¿podrá el modelo predecir correctamente la función de la redundancia? ¿podrá el modelo utilizar herramientas en 40 pasos en cadena, tener memoria, procesar partes observables, recuperarse de la falla de las herramientas y no tener la sensación de que no existen?

El modelo de evaluación de las herramientas de la empresa de evaluación de la calidad de la calidad de la calidad de la calidad de la calidad de la calidad de la calidad de la calidad de la calidad de la calidad de la calidad de la calidad de la calidad de la calidad de la calidad de la calidad de la calidad de la calidad de la calidad de la calidad de la calidad de la calidad de la calidad de la calidad de la calidad de la calidad de la calidad de la calidad de la calidad de la calidad de la calidad de la calidad de la calidad de la calidad de la calidad de la calidad de la calidad de la calidad de la calidad de la calidad de la calidad de la calidad de la calidad de la calidad de la calidad de la calidad de la calidad de la calidad de la calidad de la calidad de la calidad de la calidad de la calidad de la calidad de la calidad de la calidad de la calidad de la calidad de la calidad de la calidad de la calidad de la calidad de la calidad de la calidad de la calidad de la calidad de la calidad de la calidad de la calidad de la calidad de la calidad de la calidad de la calidad de la calidad de la calidad de la calidad de la calidad de la calidad de la calidad de la calidad de la calidad de la calidad de la calidad de la calidad de la calidad de la calidad de la calidad de la calidad de la calidad de la calidad de la calidad de la calidad de la calidad de la calidad de la calidad de la calidad de la calidad de la calidad de la calidad de la calidad de la calidad de la calidad de la calidad de la calidad de la calidad de la calidad de la calidad de la calidad de la calidad de la calidad de la calidad de la calidad de la calidad de la calidad de la calidad de la calidad de la calidad de la calidad de la calidad de la calidad de la calidad de la calidad de la calidad de la calidad de la calidad de la calidad de la calidad de la calidad de la calidad de la calidad de la calidad de la calidad de la calidad de la calidad de la calidad de la calidad de la calidad de la calidad de la calidad de la calidad de la calidad de la calidad de la calidad de la calidad de la calidad de la calidad de la calidad de la calidad de la calidad de la calidad de la calidad de la calidad de la calidad de la calidad de la calidad de la calidad de la calidad de la calidad de la calidad de la calidad de la calidad de la calidad de la calidad de la calidad de la calidad de

> Toolformer  ha establecido la base: el modelo puede aprender a usar los instrumentos mediante su propio control. BFCL V4 define el objetivo de evaluación de 2026 años. La diferencia entre ambos es el espacio de existencia de un agente de producción.

> **【中文解读】**El problema de los primeros instrumentos de uso es: ¿qué modelo puede predecir la correcta función de uso? ¿Qué modelo puede predecir la función de uso? ¿Qué modelo puede utilizar los instrumentos de uso en cadena en 40 pasos? ¿qué memoria tiene? ¿qué parte puede ser observada? ¿qué puede recuperar de un fracaso de los instrumentos y no parece que no existe? ¿Qué función de ciclo único se ha cercado a resolver, pero la memoria, las decisiones y la gestión de la cadena larga siguen siendo un problema abierto para el año 2026?

> **【拓展：BFCL V4 评估体系的演进】**Berkeley Function Calling Leaderboard V4 es un estándar de evaluación de hecho de 2026 años. V3 introdujo una evaluación basada en el estado. V4 añadió la Web.

> ¿ Qué es esto ?**【前置】**Necesidad de lectura:Fase 13·01(Función llamada Deep Dive) 本节假设你已经能写JSON Schema并理解人类的 `input_schema`vs OpenAI de `function.parameters`区别;Fase 14·01(Agencia Loop)  herramienta de la manipulación se produce en el ciclo del agente, deja el ciclo solo para ver herramienta de la manipulación se pierde en el siguiente.

## El concepto central.

### El equipo de herramientas (Schick et al., NeurIPS 2023)

Idea: dejar que el modelo anote su propio corpus de preentrenamiento con llamadas de API de candidatos. Para cada candidato, ejecutarlo. Mantenga la anotación solo si la inclusión del resultado de la herramienta reduce la pérdida en el siguiente token.

> 核心思想:让模型使用自己的预训语料标签候选人API调调. 调. 调. 调. 调. 调. 调. 调. 调. 调. 调. 调. 调. 调. 调. 调. 调. 调. 调. 调. 调. 调. 调. 调. 调. 调. 调. 调. 调. 调. 调. 调. 调. 调. 调. 调. 调. 调. 调. 调. 调. 调. 调. 调. 调. 调. 调. 调. 调. 调. 调. 调. 调. 调. 调. 调. 调. 调. 调. 调. 调. 调. 调. 调. 调. 调. 调. 调. 调. 调. 调. 调. 调. 调. 调. 调. 调. 调. 调. 调. 调. 调. 调. 调. 调. 调. 调. 调. 调. 调. 调. 调. 调. 调. 调. 调.

Las herramientas cubiertas: calculadora, sistema de calificación, motores de búsqueda, traductor, calendario. La señal de autocontrol se refiere puramente a si la herramienta ayuda a predecir el texto  no etiquetas humanas.

> 覆盖的工具:计算器、QA 系统、搜索引擎、翻译器、日历──自监督信号纯粹关于工具是否帮助预测文本不需要人工标签──

Resultado de escala: el uso de herramientas surge a escala. Los modelos más pequeños se ven perjudicados por las anotaciones de herramientas; los modelos más grandes ganan. Esta es la razón por la cual los modelos fronterizos 2026 tienen un fuerte uso de herramientas incorporados, mientras que la mayoría de los modelos 7B necesitan una ajuste de uso de herramientas explícito para ser confiables.

> 规模效应: herramientas utilizadas en el modelo grande surge. 小模型反而被工具标注损害; 大模型则受益.

> **【中文解读】**El concepto central del Toolformer es: hacer que el modelo utilice su propio pre-training en el lenguaje de etiquetado de candidato API 调用. Para cada candidato, ejecutarlo. Sólo cuando el resultado de la herramienta puede reducir la pérdida de un siguiente token, se puede conservar el etiquetado. Luego, en el material de la herramienta posterior se puede reducir. El efecto de escala es notable: el uso de herramientas en el modelo grande surge, el pequeño modelo en cambio es el uso de herramientas de etiquetado de daño.

### El nivel de clasificación de las funciones de Berkeley V4 (Patil et al., ICML 2025)

BFCL es la evaluación de facto de 2026.

> El BFCL es el estándar de evaluación de hechos de 2026 años.

- **Agentic (40%)** trayectorias de agentes completos: memoria, decisiones de varios turnos y dinámicas.
  En inglés:**智能体 (40%)** Completo agente 轨迹: memori¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬
- **Multi-Turn (30%)** conversaciones interactivas con cadenas de herramientas.
  En inglés:**多轮 (30%)**带工具链的交互式对话── también se puede decir que el diálogo es una forma de comunicación.
- **Live (10%)** Invitaciones reales presentadas por el usuario (distribución más dura).
  En inglés:**实时 (10%)** usuario de envío de la verdadera sugerencia 更难的分布)
- **Non-Live (10%)** casos de ensayo sintéticos.
  En inglés:**非实时 (10%)**合成测试用例──
- **Hallucination (10%)** detectar cuando no se debe llamar a ninguna herramienta.
  En inglés:**幻觉 (10%)**检测何时不应调用工具──

V3 introdujo la evaluación basada en el estado: después de una secuencia de herramientas, compruebe el estado real de la API (por ejemplo, "¿se ha creado el archivo?") en lugar de coincidir con el AST de las llamadas de la herramienta. V4 agregó categorías de búsqueda web, memoria y sensibilidad al formato.

> V3 introdujo una evaluación basada en el estado: después de ejecutar la secuencia de herramientas, revisar el estado real de la API (por ejemplo: "¿ha sido creado el archivo?") en lugar de utilizar las herramientas de consulta AST。V4 añadió la Web  búsqueda、 memoria y la clase de sensibilidad al formato。

En el 2026 se encontró que la llamada de la función de giro único está casi resuelta. Las fallas se concentran en la memoria (cargar con el contexto a través de los turnos), la toma de decisiones dinámicas (escoler herramientas basadas en resultados previos), cadenas de horizonte largo (drift después de más de 20 pasos) y la detección de alucinaciones (rechazar llamar cuando ninguna herramienta encaja).

> Descubrimiento clave del año 2026: la función de rodaje de rodaje único ya se acerca a la solución.

### Esquema de herramienta

Cada proveedor tiene un esquema. difieren en detalles pero comparten la misma forma:

> Cada proveedor tiene su propio modelo.

```
name: string
description: string (what it does, when to use it)
input_schema: JSON Schema (properties, required, types, enums)
```

Utilizaciones antropológicas `input_schema`Directamente. OpenAI utiliza`function.parameters`. Ambos aceptan JSON Schema. Las descripciones son cargadoras  el modelo las lee para elegir la herramienta correcta. Las descripciones de herramientas malas son la causa principal de fallos de herramientas seleccionadas incorrectamente.

> ¿ Qué es esto ?**【类比】**工具描述就像给实习生写的"使用说明书"―― el modelo nunca ha visto tu herramienta, lo único que puede depender es la descripción― si escribe`name: get_user, description: "gets user"`, el modelo no sabe si es por identificación o por correo, regresar es el objeto completo o sólo el nombre.**好描述包含三要素**:做什么 + 何时用 + 输入输出语义──

> ️ **【易错点】**El modelo de confianza regresa de los parámetros tipo.`"5"`(字符串) Regresar a la expectativa`int`El esquema...**后果**: tu herramienta de la función `TypeError` Crash, todo el ciclo de agentes  中断**一行修复**: en el instrumento de ejecución de la entrada de la información`pydantic.BaseModel.parse_obj`O similar a la experiencia, la experiencia fracasa cuando regresa errores estructurales, como`{"error": "expected int, got str"}`¡Que vuelva a intentarlo!

> Antropic 直接使用 `input_schema`❖ OpenAI                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                          `function.parameters`◊ ambos aceptan el esquema JSON. La descripción es el modelo de carga central.

### Validación de los argumentos

No confía en ninguna llamada de herramienta.

> No hay ningún tipo de prueba.

1. **Type coercion.**El modelo puede devolver una cadena "5" donde el esquema dice int. Forzar si no es ambigua; rechazar si no.
   En inglés:**类型强制转换。**模型可能返回字符串 "5" Pero el modelo requiere int.
2. **Enum validation.**Si el esquema dice `status in {"open", "closed"}`y las emisiones de modelo `"in_progress"`, rechazar con un error descriptivo.
   En inglés:**枚举验证。**Si mode determinado `status in {"open", "closed"}`Y el modelo de salida`"in_progress"`, con el error descriptivo rechazo.
3. **Required fields.**Falta el campo requerido -> observación de error inmediato de vuelta al modelo, no un accidente.
   En inglés:**必填字段。**缺少必填字段 -> 立即回归错误观察给模型, y no el colapso.
4. **Format validation.**Datos, correos electrónicos, URLs  validar con parseres de concreto, no regex.
   En inglés:**格式验证。**El número de páginas de la página web se utiliza para la información de la página web.

Cada falla de validación debe devolver una observación estructurada para que el modelo pueda volver a intentar con la forma correcta.

> Cada prueba que falla debe volver a observar estructuralmente, para que el modelo pueda volver a probar en el formato correcto.

### Llamadas paralelas de herramientas

Los proveedores modernos admiten llamadas paralelas de herramientas en un solo turno de asistente.

> 现代提供商支持在一个助手轮次中并行调用工具──循环:

1. El modelo emite 3 llamadas de herramientas con distinción `tool_use_id`S.
   Traducción:Modelo发出 3 个带有不同 `tool_use_id`De los instrumentos de la práctica.
2. El tiempo de ejecución los ejecuta (en paralelo si es independiente).
   Se trata de un sistema de operaciones de la compañía.
3. Cada resultado se remonta a como un`tool_result`bloque correlacionado por `tool_use_id`¿ Qué ?
   En inglés, "Cada resultado como resultado"`tool_result`块返回, por el `tool_use_id`¿Qué pasa?

Regla de ingeniería: tratar las identificaciones de correlación como carga, cambiarlas y obtener la ruta de herramienta a resultado equivocado.

> ¿ Qué es esto ?**【困惑】**P: El 40% de BFCL V4 es agente, ¿no es que el ciclo único ya no es importante? A: No es. El 40% es agente para reflejar la producción real, pero el ciclo único de precisión sigue siendo fundamental.

> 工程规则:将关联 ID 视为核心承载──交换它们会导致错误的工具-结果路由──

### El sandboxing

La ejecución de herramientas es el límite de la caja de arena. Véase la lección 09 para detalles. versión corta: cada herramienta debe especificar la superficie de lectura/escritura, acceso a la red, tiempo de espera, límite de memoria.`run_shell(cmd)`es una bandera roja; específico `git_status()`Es más seguro.

> 工具执行是沙箱边界──详见第 9 课――简短版: Cada instrumento debe especificarse en el alcance de la lectura, en el acceso a la red, en el tiempo y en la memoria.`run_shell(cmd)`Es una bandera roja.`git_status()`Más seguro.

## Construye con movimiento.
```figure
tool-routing
```

## Construye el mismo

`code/main.py`Implemente un registro de herramientas de forma de producción:

> `code/main.py`实现 un registro de herramientas de producción:

- Validador de subconjunto de JSON Schema (sólo stdlib).
  En inglés, el nombre de la base de datos de la base de datos es JSON.
- Registro de herramienta con descripción, esquema de entrada, tiempo de espera y ejecutor.
  China: 带描述、输入模式、超时和执行器的工具注册── también conocido como 带描述,输入模式,超时和执行器的工具注册, también conocido como 带描述,输入模式,超时和执行器的工具注册, también conocido como 超时和执行器的工具注册.
- La coerción de argumentos y la validación enum.
  En la actualidad, el número de personas que han recibido la información de la información de la empresa es de aproximadamente un millón de personas.
- Envío paralelo de herramientas con identificadores de correlación.
  La información de la información de la página web de la página web de la página web de la página web de la página web de la página web de la página web de la página web de la página web de la página web de la página web de la página web de la página web de la página web de la página web de la página web de la página web de la página web de la página web de la página web de la página web de la página web de la página web de la página web de la página web de la página web de la página web de la página web de la página web de la página web de la página web de la página web de la página web de la página web de la página web de la página web de la página web de la página web de la página web de la página web de la página web de la página web de la página web de la página web de la página web.
- Observaciones de errores como cadenas estructuradas.
  En inglés, el error observado como un símbolo estructurado.

- ¿Qué quieres decir ?

> 运行:

```
python3 code/main.py
```

El rastro muestra a un mini agente llamando a tres herramientas en un turno, con una llamada deliberadamente malformada que es rechazada con un error descriptivo en el que el modelo puede actuar.

> 轨迹显示一个迷你代理在一轮中调用三个工具, una de ellas es un error de forma intencional.

## Usalo con el marco de ejecución

Cada proveedor tiene su propio esquema de herramientas  Antropic, OpenAI, Gemini, Bedrock. Utilice una capa de traducción (OpenAI Agents SDK, Vercel AI SDK, LangChain Tool Adapter) si necesita multi-proveedor. BFCL es el punto de referencia  ejecutarlo contra su agente antes de enviar si el uso de herramientas es central para el producto.

> Cada proveedor tiene su propio modelo de herramientas: Antropico, OpenAI, Gemini, Bedrock, si necesita más proveedores, utiliza la versión de la versión de la versión de los SDK de los agentes de OpenAI, Vercel, LongChain, etc.

## Envíe el producto .

`outputs/skill-tool-registry.md`genera un catálogo de herramientas, esquema y registro para un dominio de tarea determinado. Incluye controles de calidad de descripción (¿dice la descripción de cada herramienta al modelo cuándo usarla?).

> `outputs/skill-tool-registry.md`Para un determinado campo de tareas, el registro de herramientas se genera en el catálogo de herramientas, modelos y registros.

## Los ejercicios.

1. Añadir una herramienta "no-op" que permite al modelo rechazar explícitamente el uso de cualquier otra herramienta.
   China: añadir un instrumento "sin operación", hacer que el modelo rechace expresamente el uso de cualquier otro instrumento.
2. Implemente la coerción de argumentos para int-as-string y float-as-string. ¿Dónde comienza la coerción a ocultar insectos reales?
   En español, el nombre de la persona que ha sido enviada a la red se puede ver en el código de la red.
3. Añadir un tiempo de espera por herramienta y un interruptor de circuito (rechazar la herramienta durante 60 años después de 3 fallos consecutivos). ¿Qué cambia esto en la forma en que el modelo se recupera?
   China Translation: Añadir cada herramienta de super tiempo y interruptor (continuous 3 times failure after rejecting tool 60 seconds)
4. Lea la descripción de BFCL V4. Seleccione una categoría (por ejemplo, "multi-turn") y ejecute 10 instrucciones de ejemplo a través de su agente.
   En el caso de los agentes de la empresa, el número de clientes que pueden participar en la operación es el número de clientes que pueden participar en la operación.
5. ¿Qué fue lo que Pydantic/Zod captó que el juguete perdió?
   China:将标准库验证器移植到Pydantic或Zod──Pydantic/Zod 捕获了玩具版本遗漏的什么?

## Términos clave .

| Term | What people say | What it actually means |
|------|-----------------|-----------------------|
| 术语 | 通俗说法 | 实际含义 |
| Function calling | "Tool use" / "工具使用" | Structured-output tool invocation with validated schema / 带验证模式的结构化输出工具调用 |
| Toolformer | "Self-supervised tool annotation" / "自监督工具标注" | Schick 2023 — keep tool calls whose results reduce next-token loss / Schick 2023——保留减少下一个 token 损失的工具调用 |
| BFCL | "Berkeley Function Calling Leaderboard" / "Berkeley 函数调用排行榜" | 2026 benchmark: 40% agentic, 30% multi-turn, 10% live, 10% non-live, 10% hallucination / 2026 基准：40% 智能体、30% 多轮、10% 实时、10% 非实时、10% 幻觉 |
| Tool schema | "Function signature for the model" / "模型的函数签名" | name, description, JSON Schema of arguments / 名称、描述、参数的 JSON Schema |
| tool_use_id | "Correlation ID" / "关联 ID" | Ties a tool call to its result; essential for parallel dispatch / 将工具调用与其结果关联；并行分派必需 |
| Hallucination detection | "Know when not to call" / "知道何时不调用" | V4 category: refuse to call when no tool fits / V4 类别：无合适工具时拒绝调用 |
| Argument coercion | "String-to-int repair" / "字符串到整数的修复" | Narrow fixes for predictable schema-mismatch; reject if ambiguous / 可预测模式不匹配的窄修复；如果歧义则拒绝 |
| Sandboxing | "Tool execution boundary" / "工具执行边界" | Per-tool read/write surface, network, timeout, memory cap / 每个工具的读写范围、网络、超时、内存上限 |

## Más Leer más Leer más

- [Schick et al., Toolformer (arXiv:2302.04761)](https://arxiv.org/abs/2302.04761) Anotado de herramientas auto supervisadas
  En el libro de la obra, el autor de la obra, el autor de la obra, el autor de la obra, el autor de la obra, el autor de la obra, el autor de la obra, el autor de la obra, el autor de la obra, el autor de la obra, el autor de la obra, el autor de la obra, el autor de la obra, el autor de la obra, el autor de la obra, el autor de la obra, el autor de la obra, el autor de la obra, el autor de la obra, el autor de la obra, el autor de la obra, el autor de la obra, el autor de la obra, el autor de la obra, el autor de la obra, el autor de la obra, el autor de la obra, el autor de la obra, el autor, el autor de la obra, el autor, el autor de la obra, el autor, el autor de la obra, el autor, el autor, el autor, el autor de la obra, el libro, el libro, el libro, el libro, el libro, el libro, el libro, el libro, el libro, el libro, el libro, el libro, el.
- [Berkeley Function Calling Leaderboard (V4)](https://gorilla.cs.berkeley.edu/leaderboard.html) Valoración de referencia de 2026
  La lista de la evaluación de la base de datos de Berkeley es el siguiente:
- [Anthropic, Tool use documentation](https://platform.claude.com/docs/en/agent-sdk/overview) esquema de herramientas de producción en el SDK de Claude Agent
  En inglés, el método de producción de los instrumentos de producción de los SDK es el método de producción de los instrumentos de producción de los SDK.
- [OpenAI Agents SDK docs](https://openai.github.io/openai-agents-python/) Tipo de herramienta de función y Guardrails
  En inglés, el código de código de código de código abierto es el código de código abierto.
