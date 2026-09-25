# Los patrones de flujo de trabajo de Anthropic: Simple Over Complex Anthropic 工作流模式:简单优于复杂

> Schluntz y Zhang (Anthropic, Dec 2024) distinguen los flujos de trabajo (caminos predefinidos) de los agentes (uso de herramientas dinámicas).

> **【中文解读】**Anthropic en un artículo de diciembre de 2024 distinguió entre el trabajo (predefinición de un camino) y el uso de un agente (Agencia) 五种工作流模式覆盖大多数场景──从直接API调用开始──只有在步骤无法预测时才添加 Agent──

**Type:** Learn + Build | **类型:** 学习 + 构建
**Languages:** Python (stdlib) | **语言:** Python (标准库)
**Prerequisites:** Phase 14 · 01 (Agent Loop) | **前置知识:** Phase 14 · 01 (Agent 循环)
**Time:** ~60 minutes | **时间:** ~60 分钟

## Objetivos de aprendizaje

- Nombre de los cinco patrones de flujo de trabajo de Anthropic: cadena de respuesta, enrutamiento, paralelalización, orquesta-trabajadores, evaluador-optimizador.
  China: Traducción:                                                                                                                                                                                                                                                             
- Explica la distinción entre el flujo de trabajo y el costo de ingeniería de cada uno.
  Traducción:Explanar Diferencias entre el agente y el flujo de trabajo y sus propios costos de construcción.
- Identificar cuándo elegir un flujo de trabajo en lugar de un agente (y viceversa).
  En inglés, "Agencia" significa "agente" (en inglés, "agente").
- Implementar los cinco patrones en el STDlib contra un LLM con guión.
  La traducción de la lengua inglesa en inglés es:

## El problema es la introducción del problema

Los equipos buscan marcos multiagentes para problemas que requieren una sola llamada de función. El costo es real: los marcos añaden capas que oscurecen las instrucciones, ocultan el flujo de control e invitan a la complejidad prematura.

> 团队为只需要一次函数调用的问题选择多 机构框架――代价是真实的:框架增加模糊提示、隐藏控制流、引入过早复杂性的层――Schluntz 和 Zhang de diciembre de 2024 es el artículo más citado de la industria reflexión: desde el principio simple, sólo en la complejidad vale su costo cuando se añade――

> **【中文解读】**Antropic en el diciembre de 2024 publicado en Building Effective Agents define cuatro tipos de procesos: 1) Enlace rápido, 2) Routing, 3) Parallelización, 4) Orquesta y Trabajadores, ordenadores y distribuidores de tareas. Estos modelos son la construcción de la producción de agentes, la construcción de los bloques de base del sistema.

> **【拓展：Anthropic 的工作流模式分类已成为 Agent 工程的事实标准】**LangGraph utiliza el estado de imagen para implementar estos modelos, OpenAI Agents SDK utiliza las manos para implementar el routing y la organización, CrewAI utiliza los equipos para implementar la combinación de acciones.

> ¿ Qué es esto ?**【前置】**必須先通過Fase 14·01 (Agent Loop) 本節就是它的"模式提炼"──還需要看Fase 14·02 (ReWOO) ‧Fase 14·05 (Self-Refine) ‧Fase 14·10 (Skills) 五種工作流模式都對应前面學過的具体技術,没基础会感觉空洞──

## El concepto central.

### Flujos de trabajo contra agentes

- **Workflow.**Los LLM y las herramientas orquestadas a través de caminos de código predefinidos.
  En inglés:**工作流。**通过预定义代码路径编排的 LLM 和工具──工程师拥有图──
- **Agent.**Los LLM dirigen dinámicamente sus propias herramientas y toman sus propios pasos.
  En inglés:**Agent。**LLM 动态 guía sus propios instrumentos y pasos.

Los agentes desbloquean problemas sin fin, pero hacen que los modos de falla sean más difíciles de razonar.

> ¿ Qué es esto ?**【类比】**Flujo de trabajo vs agente 像地铁 vs 自驾:地铁(flujo de trabajo) ruta fija,便宜,可靠, pero sólo puedes ir a un puesto de trabajo; auto驾驶(agent)灵活,能去任何地方, pero可能迷路,烧油,出车祸;;日常通勤选地铁(workflow),探索未知地区选自驾(agent);; el error más común de los nuevos es "todas las tareas están realizadas por sí mismos"

>  ambos tienen su uso en el campo de batalla                                                                                                                                                                                                                                                         

### El LLM aumentado

Fundamento para los cinco patrones: un LLM con tres capacidades conectadas en  búsqueda (recuperar), herramientas (acciones), memoria (persistencia).

> Todas las aplicaciones de la aplicación de la aplicación de la aplicación de la aplicación de la aplicación de la aplicación de la aplicación de la aplicación de la aplicación de la aplicación de la aplicación de la aplicación de la aplicación de la aplicación de la aplicación de la aplicación de la aplicación de la aplicación de la aplicación de la aplicación de la aplicación de la aplicación de la aplicación de la aplicación de la aplicación de la aplicación de la aplicación de la aplicación de la aplicación de la aplicación de la aplicación de la aplicación de la aplicación de la aplicación de la aplicación de la aplicación de la aplicación de la aplicación de la aplicación de la aplicación de la aplicación de la aplicación de la aplicación de la aplicación de la aplicación de la aplicación de la aplicación de la aplicación de la aplicación de la aplicación de la aplicación de la aplicación de la aplicación de la aplicación de la aplicación de la aplicación de la aplicación de la aplicación de la aplicación de la aplicación de la aplicación de la aplicación de la aplicación de la aplicación de la aplicación de la aplicación de la aplicación de la aplicación de la aplicación de la aplicación de la aplicación de la aplicación de la aplicación de la aplicación de la aplicación de la aplicación de la aplicación de la aplicación de la aplicación de la aplicación de la aplicación de la aplicación de la ley.

### Los cinco patrones

1. **Prompt chaining.**La salida de llamada 1 es la entrada a llamada 2. Se utiliza cuando una tarea tiene una descomposición lineal limpia. Puertas programáticas opcionales entre pasos.
   En inglés:**提示链。**调用 1 的输出是调用 2 的输入. Cuando la tarea tiene una clara descomposición de la línea, se utiliza un proceso de programación.
2. **Routing.**Un LLM clasificador elige qué LLM o herramienta a invocar.
   En inglés:**路由。**选择调用哪个下游 LLM或工具── cuando las diferentes clases de entradas necesitan diferentes procesos de uso──
3. **Parallelization.**Se ejecutan N LLM llamadas simultáneamente, resultados agregados. Dos formas: sección (parcelaciones diferentes) y votación (el mismo prompt, N ejecutan, mayoría/síntesis).
   En inglés:**并行化。**Y发运行 N 个 LLM 调用,聚合结果──两种形式:分段(不同块) 和投票(同提示,N 次运行,多数/综合)
4. **Orchestrator-workers.**Un LLM orquestador decide dinámicamente qué trabajadores (también LLM) ejecutar y sintetiza su producción.
   En inglés:**编排器-工作者。**编排器 LLM 动态决定运行哪些工作者(también LLM)并综合其输出── similar a un ciclo de agentes, pero el编排器 no tendrá un ciclo ilimitado──
5. **Evaluator-optimizer.**Un LLM propone una respuesta, otro LLM la evalúa. Iterar hasta que el evaluador pasa. Esto es auto-refinado (lección 05) generalizado.
   En inglés:**评估器-优化器。**Una LLM  planteó una respuesta, otra LLM  evaluarla―代直到评估器通过―.

### Donde los flujos de trabajo vencen a los agentes

> 工作流优于 Agente de la escena:

- **Predictable tasks.**Si puedes enumerar los pasos, deberías.
  En inglés:**可预测任务。**Si puedes levantar pasos, deberías hacerlo.
- **Cost-bound tasks.**Los flujos de trabajo tienen un número limitado de pasos; los agentes pueden espiral.
  En inglés:**成本受限任务。**工作流有有限步数; Agente puede estar fuera de control.
- **Compliance-bound tasks.**Los auditores quieren leer el gráfico, no deducirlo a partir de las trayectorias.
  En inglés:**合规受限任务。**El auditor quiere leer el cuadro, en lugar de deducirlo de su trayectoria.

### Donde los agentes superan los flujos de trabajo

> Agente 优于工作流的场景:

- **Open-ended research.**Cuándo el siguiente paso depende de lo que el último paso regresó.
  En inglés:**开放式研究。**Cuando el siguiente paso depende de lo que el siguiente paso regresó.
- **Variable-length tasks.**Minutos a horas de trabajo donde el número de pasos es desconocido.
  En inglés:**可变长度任务。**几分钟到几小时的工作, pasos desconocidos.
- **Novel domains.**Cuando aún no conozcas el flujo de trabajo correcto, primero explora, codifica después.
  En inglés:**新领域。**Cuando todavía no sabes el verdadero flujo de trabajo, primero explora, después redacta.

### El acompañante de ingeniería de contexto

"Ingeniería de contexto eficaz para agentes de IA" (Anthropic 2025) formaliza la disciplina adyacente: la ventana 200k es un presupuesto, no un contenedor. Qué incluir, cuándo compactar, cuándo dejar crecer el contexto.

> "AI Agent's有效上下文工程" (Antropic 2025) formalizó las áreas de estudio de la siguiente manera:

## Construye con movimiento.

> ️ **【易错点】**团队 más habitual en el cratera: ver Antropic 五种模式就直接全部上 LangGraph/CrewAI 框架──**后果**En el caso de las redes de datos, el número de redes de datos de las redes de datos de las redes de datos de las redes de datos de las redes de datos de las redes de datos de las redes de datos de las redes de datos de las redes de datos de las redes de datos de las redes de datos de las redes de datos de las redes de datos de las redes de datos de las redes de datos de las redes de datos de las redes de datos de las redes de datos de las redes de datos de las redes de datos de las redes de datos de las redes de datos de las redes de datos de las redes de datos de las redes de datos de las redes de datos de las redes de datos de las redes de datos de las redes de datos de las redes de datos de las redes de Internet de Internet de Internet de Internet de Internet de Internet de Internet de Internet de Internet de Internet de Internet de Internet de Internet de Internet de Internet de Internet de Internet de Internet de Internet de Internet de Internet de Internet de Internet de Internet de Internet de Internet de Internet de Internet de Internet de Internet de Internet de Internet de Internet de Internet de Internet de Internet de Internet de Internet de Internet de Internet de Internet de Internet de Internet de Internet de Internet de Internet de Internet de Internet de Internet de Internet de Internet de Internet de Internet de Internet de Internet de Internet de Internet de Internet de Internet de Internet de Internet de Internet de Internet de Internet de Internet de Internet de Internet de Internet de Internet de Internet de Internet de Internet de Internet de Internet de Internet de Internet de Internet de Internet de Internet de Internet de Internet de Internet de Internet de Internet de Internet de Internet de Internet de Internet de Internet de Internet de Internet de Internet de Internet de Internet de Internet de Internet de Internet de Internet de Internet de Internet de Internet de Internet de Internet de Internet de Internet de Internet de Internet de Internet de Internet de Internet de Internet de Internet de Internet de Internet de Internet de Internet de Internet de Internet de Internet de Internet de Internet de Internet de Internet de Internet de Internet de Internet de Internet de Internet de Internet de Internet de Internet de Internet de Internet de Internet de Internet de Internet de Internet de Internet de Internet de Internet de Internet de Internet de Internet de Internet de Internet de Internet de Internet de Internet de Internet de Internet de Internet de Internet de Internet de Internet de Internet de Internet de Internet de Internet de Internet de Internet de Internet de Internet de Internet de Internet de Internet de Internet de Internet de Internet de Internet de Internet de Internet de Internet de Internet de**先直接 API 调用，加复杂度只为换取能力**" Una cadena de comandos con una función Python ordinaria está lista, no necesita ningún marco".""**一行修复**El objetivo es evaluar si cada tarea puede ser realizada con un marco diferente.
```figure
workflow-chain
```

## Construye el mismo

`code/main.py`Implementa los cinco patrones de flujo de trabajo en contra de un `ScriptedLLM`¿Qué es esto ?

> `code/main.py` en el sentido `ScriptedLLM` Realizar todos los cinco modos de trabajo:

- `prompt_chain(input, steps)` secuencial.
- `route(input, classifier, handlers)` Clasificación + expedición.
- `parallel_vote(prompt, n, aggregator)` N carreras, agregado.
- `orchestrator_workers(task, workers)` Orquestación elige trabajadores.
- `evaluator_optimizer(task, proposer, evaluator, max_iter)` bucle hasta el paso.

- ¿Qué quieres decir ?

> 运行:

```
python3 code/main.py
```

Cada patrón imprime su rastro. El total de líneas de código por patrón es de ~10-15; el costo de un marco se mide en miles.

> Cada modelo imprime su trayectoria. Cada modelo tiene un número de líneas de código de aproximadamente 10-15 líneas.

> ¿ Qué es esto ?**【困惑】**P: 既然"workflow 优先"那么明确,为什么LangGraph、CrewAI estos frameworks还如此火?**持久化、可观测性、人在回路、监控**Estas funciones de "运维级"── utilizas 30 行 stdlib 写的提示链 运挂了, tienes que pensar en cómo recuperarte desde el 17 步步; utilizas LangGraph 写的,框架免费给你检查点── por lo tanto, la conclusión es "el primer paso con stdlib, la fase de producción evalúa si se encuentra en el marco" en lugar de ser sin cerebro o sin cerebro no arriba──

## Usalo con el marco de ejecución

- La API directa requiere la mayoría de las tareas.
  La mayoría de las tareas utilizan API directa 调用。
- Marco sólo cuando el patrón realmente necesita estado duradero (LangGraph), concurrencia actor-modelo (AutoGen v0.4), o plantilla de rol (CrewAI).
  En inglés, el nombre de la persona que se ha convertido en el nombre de la persona que se ha convertido en el nombre de la persona que se ha convertido en el nombre de la persona que se ha convertido en el nombre de la persona que se ha convertido en el nombre de la persona que se ha convertido en el nombre de la persona que se ha convertido en el nombre de la persona que se ha convertido en el nombre de la persona que se ha convertido en el nombre de la persona que se ha convertido en el nombre de la persona que se ha convertido en el nombre de la persona que se ha convertido en el nombre de la persona que se ha convertido en el nombre de la persona que se ha convertido en el nombre de la persona que se ha convertido en el nombre de la persona que se ha convertido en el nombre de la persona.
- Busca el SDK de Claude Agent cuando quieras la forma del arnés de código Claude sin reconstruirlo.
  Cuando quieres Claude Code 框架形态而不重建时选择Claude Agent SDK──

## Envíe el producto .

`outputs/skill-workflow-picker.md`elige el patrón adecuado para una descripción de tarea dada, incluida la razón de decisión y el camino de refactor hacia un agente si los flujos de trabajo no son suficientes.

> `outputs/skill-workflow-picker.md`Para determinar la tarea, describir el modelo correcto de elección, incluyendo las razones de la decisión y la forma de reconstruir el proceso de trabajo del agente cuando el flujo de trabajo es insuficiente.

## Los ejercicios.

1. Implementar el enrutamiento con un umbral de confianza. Por debajo del umbral -> escala a humano. ¿Dónde aterriza el umbral para un caso de uso de soporte de nivel 1?
   En la actualidad, el valor de la empresa es más bajo que el valor de la empresa.
2. Añadir un tiempo de descanso a `parallel_vote`¿Qué pasa cuando se hace una llamada? ¿Cómo se agrega con los votos faltantes?
   En inglés:`parallel_vote`¿Cómo se hace cuando se coloca una llamada? ¿Cómo se agrupa la votación de la falta?
3. - ¿ Qué ?`evaluator_optimizer`en un bandido: mantener las salidas de 2 en las iteraciones para que un resultado bueno tardío no sea superado por uno malo tardío.
   En inglés:`evaluator_optimizer`变成 bandit:跨代保留 top-2 输出, evitar后期好结果被后期坏结果覆盖──
4. Combine la cadena de prompto con el enrutamiento: un router elige una de las tres cadenas. Medir el costo de los tokens frente a una sola alternativa de gran prompto.
   En la actualidad, el sistema de distribución de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de
5. Elige una de tus características de producción, dibuja el gráfico del flujo de trabajo, cuenta los pasos. ¿Sería mejor un agente aquí?
   China: seleccionar una de tus funciones de producción, dibujar un trabajo, hacer un trabajo, hacer un trabajo, hacer un trabajo, hacer un trabajo, hacer un trabajo, hacer un trabajo, hacer un trabajo, hacer un trabajo, hacer un trabajo, hacer un trabajo, hacer un trabajo, hacer un trabajo, hacer un trabajo, hacer un trabajo, hacer un trabajo, hacer un trabajo, hacer un trabajo, hacer un trabajo, hacer un trabajo, hacer un trabajo, hacer un trabajo, hacer un trabajo, hacer un trabajo, hacer un trabajo, hacer un trabajo, hacer un trabajo, hacer un trabajo, hacer un trabajo, hacer un trabajo, hacer un trabajo, hacer un trabajo, hacer un trabajo, hacer un trabajo, hacer un trabajo, hacer un trabajo, hacer un trabajo, hacer un trabajo, hacer un trabajo, hacer un trabajo, hacer un trabajo, hacer un trabajo, hacer un trabajo, hacer un trabajo, hacer un trabajo, hacer un trabajo, hacer un trabajo, hacer un trabajo, hacer un trabajo, hacer un trabajo, hacer un trabajo, hacer un trabajo, hacer un trabajo, hacer un trabajo, hacer un trabajo, hacer un trabajo, hacer un trabajo, hacer un trabajo, hacer un trabajo, hacer un trabajo, hacer un trabajo, hacer un trabajo, hacer un trabajo, hacer un trabajo, hacer un trabajo, hacer un trabajo, hacer un trabajo, hacer un trabajo, hacer un trabajo, hacer un trabajo, hacer un trabajo, hacer un trabajo, hacer un trabajo, hacer un trabajo, hacer un trabajo, hacer un trabajo, hacer un trabajo, hacer un trabajo, hacer un trabajo, hacer un trabajo, hacer un trabajo, hacer un trabajo, hacer un trabajo, hacer un trabajo, hacer un trabajo, hacer un trabajo, hacer un trabajo, hacer un trabajo, hacer un trabajo, hacer un trabajo, hacer un trabajo, hacer un trabajo, hacer un trabajo, hacer un trabajo, hacer un trabajo, hacer un trabajo, hacer un trabajo, hacer un trabajo, hacer un trabajo, hacer un trabajo, hacer un?

## Términos clave .

| Term | What people say | What it actually means |
|------|-----------------|-----------------------|
| 术语 | 通俗说法 | 实际含义 |
| Workflow | "Predefined flow" / "预定义流程" | Engineer-owned graph of LLM and tool calls / 工程师拥有的 LLM 和工具调用图 |
| Agent | "Autonomous AI" / "自主 AI" | Model-owned graph; dynamic tool direction / 模型拥有的图；动态工具指导 |
| Augmented LLM | "LLM with tools" / "带工具的 LLM" | LLM + search + tools + memory; the atomic unit / LLM + 搜索 + 工具 + 记忆；原子单元 |
| Prompt chaining | "Sequential calls" / "串行调用" | Output of call N is input to call N+1 / 调用 N 的输出是调用 N+1 的输入 |
| Routing | "Classifier dispatch" / "分类分派" | Pick which chain/model handles the input / 选择哪个链/模型处理输入 |
| Parallelization | "Fan out" / "扇出" | N concurrent calls; aggregate by sectioning or voting / N 个并发调用；按分段或投票聚合 |
| Orchestrator-workers | "Dispatcher agent" / "分派 Agent" | Orchestrator LLM picks specialist LLMs dynamically / 编排器 LLM 动态选择专家 LLM |
| Evaluator-optimizer | "Proposer + judge" / "提议者 + 评判者" | Iterate until evaluator passes; Self-Refine generalized / 迭代直到评估器通过；Self-Refine 的泛化 |

## Más Leer más Leer más

- [Anthropic, Building Effective Agents (Dec 2024)](https://www.anthropic.com/research/building-effective-agents) los cinco patrones de flujo de trabajo
  En inglés, el nombre de la empresa es "Agent".
- [Anthropic, Effective context engineering for AI agents](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents) la disciplina del compañero
  En inglés, el artículo de la revista "Antropic  About AI Agent 有效上下文工程的文章伴学科──
- [LangGraph overview](https://docs.langchain.com/oss/python/langgraph/overview) cuando los gráficos estatales ganan su costo
  La historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la China.
- [OpenAI Agents SDK](https://openai.github.io/openai-agents-python/) el patrón de orquesta­dor-trabajadores, producido
  China: OpenAI Agents SDK 编排器-工作者模式的产品化.
