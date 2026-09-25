# LangGraph: gráficos de estado y ejecución duradera
# Orquestación de gráficos estatales  Ejecución duradera y puntos de control

> El agente es una máquina de estado; los nodos son funciones; los bordes son transiciones; el estado se pone en punto de control después de cada nodo.

> **【中文解读】**LangGraph es una referencia de la organización de estados en el nivel inferior de 2026 años.

**Type:** Learn + Build | **类型:** 学习 + 构建
**Languages:** Python (stdlib) | **语言:** Python (标准库)
**Prerequisites:** Phase 14 · 01 (Agent Loop), Phase 14 · 12 (Workflow Patterns) | **前置知识:** Phase 14 · 01 (Agent 循环), Phase 14 · 12 (工作流模式)
**Time:** ~75 minutes | **时间:** ~75 分钟

## Objetivos de aprendizaje

- Describa el modelo central de LangGraph: máquina de estado con estado inmutable, nodos de función, bordes condicionales y puntos de control post-paso.
  En el lenguaje chino, el lenguaje es el lenguaje de la lengua inglesa.
- Describa el modelo principal de LangGraph: máquina de estado con estado tipado, nodos de función, bordes condicionales y puntos de control post-nodo.
- Nombren las cuatro capacidades que destacan los documentos: ejecución duradera, transmisión, humano en el bucle, memoria integral.
  China: 文档强调的四种能力:持久执行、流式传输、人回路中、全面记忆──
- Explica las tres topologías de orquestación que LangGraph admite: supervisor, peer-to-peer (crujo), jerárquico (subgrafos anidados).
  La estructura de la estructura de la estructura de la estructura de la estructura de la estructura de la estructura de la estructura de la estructura de la estructura de la estructura de la estructura de la estructura de la estructura de la estructura de la estructura de la estructura de la estructura de la estructura de la estructura de la estructura de la estructura de la estructura de la estructura de la estructura de la estructura de la estructura de la estructura de la estructura de la estructura de la estructura de la estructura de la estructura de la estructura de la estructura de la estructura de la estructura de la estructura de la estructura de la estructura de la estructura de la estructura de la estructura de la estructura de la estructura de la estructura de la estructura de la estructura de la estructura de la estructura de la estructura de la estructura de la estructura de la estructura de la estructura de la estructura de la estructura de la estructura de la estructura de la estructura de la estructura de la estructura de la estructura de la estructura de la estructura de la estructura de la estructura de la estructura de la estructura de la estructura de la estructura de la estructura de la estructura de la estructura de la estructura de la estructura de la estructura de la estructura de la estructura de la estructura de la estructura de la estructura de la estructura de la estructura de la estructura de la estructura de la estructura de la estructura de la estructura de la estructura de la estructura de la estructura de la estructura de la estructura de la estructura de la estructura de la estructura de la estructura de la estructura de la estructura de la estructura de la estructura de la estructura de la estructura de la estructura de la estructura de la estructura de la estructura de la estructura de la estructura de la estructura de la estructura de la estructura de la estructura de la estructura de la estructura de la estructura de la estructura de la estructura de la estructura de la estructura de la estructura de la estructura de la estructura de la estructura de la estructura de la estructura de la estructura de la estructura de la estructura de la estructura de la estructura de la estructura de la estructura de la estructura de la estructura de la estructura de la estructura de la estructura de la estructura de la estructura de la estructura.
- Implemente un gráfico de estado stdlib con estado inmutable, bordes condicionales y un ciclo de control/resumen.
  Traducción:Use estándar de la biblioteca para lograr un estado de incondición, condiciones y el estado del ciclo de revisión.
- Implemente un gráfico de estado stdlib con estado tipado, bordes condicionales y un ciclo de punto de control/resumen.

## El problema es la introducción del problema

Los agentes y los flujos de trabajo comparten un problema: cuando una ejecución de 40 pasos falla en el paso 38, desea reanudar desde el paso 38, no empezar de nuevo. Los modelos de estado de segunda clase dejan a los operadores pirateando retos alrededor de una biblioteca que asume nuevas ejecuciones.

> Agente 和工作流共享一个问题: Cuando 40 pasos funcionan en el 38o paso falla, usted quiere recuperar desde el 38o paso en lugar de comenzar desde el principio.

La respuesta de diseño de LangGraph: el estado es un objeto tipado de primera clase, las mutaciones son explícitas y los puntos de control persisten después de cada nodo.`load_state(session_id)`¿Qué pasa?

> El estado es un objeto de tipo de banda de ciudadanos iguales, el cambio de operación es evidente, el punto de control se perdurará después de cada nodo.`load_state(session_id)`¿Qué es eso?

> **【中文解读】**Agente y flujo de trabajo Compartir un problema: Cuando 40 pasos se ejecutan en el 38o paso fallado, usted quiere recuperar desde el 38o paso en lugar de comenzar desde el principio.`load_state(session_id)`¿Qué es eso?

> **【拓展：LangGraph → 状态图编排】**LangGraph es una referencia de la organización de estados en el nivel inferior de 2026 y se implementará en el marco de la estructura central del ecosistema de LangChain, ampliamente utilizada en la producción de los niveles de organización de agentes.

> ¿ Qué es esto ?**【前置】**必须先掌握:Fase 14·01(Agent Loop) y Fase 14·12(Antropic Workflow Patterns) Langgraph es la "versión permanente" del modelo de trabajo.

## El concepto central.

### El gráfico

Un gráfico se define por: Un dictado tipado (o modelo Pydantic) que cada nodo lee y muta.

> 图由以下定义:一个每个节点都读写的带类型 dict (图由以下定义:一个每个节点都读写的带类型 dict) 或 Pydantic 模型) 

- **Nodes.**Funciones puras`(state) -> state_update`Las actualizaciones se fusionan en estado después de regresar.
  En inglés:**节点。**纯函数 `(state) -> state_update`◊ actualización en el estado de regreso ◊
- **Edges.**Transiciones condicionales o directas entre nodos.
  En inglés:**边。**节点之间的条件或直接转换──
- **Entry and exit.** `START`y `END`Los nodos de la centinela marcan el límite.
  En inglés:**入口和出口。** `START`Y `END`哨兵节点标记边界──

> **【中文解读】**El gráfico de LangGraph está formado por tres elementos definidos: 1) Tipo de estado  Cada punto de lectura `(state) -> state_update`, regresar el valor de la combinación al estado; 3) 边节点之间的条件或直接转换──

Ejemplo: un agente con `classify`¿ Qué ?`refund`¿ Qué ?`bug`¿ Qué ?`sales`¿ Qué ?`done`los nodos  un flujo de trabajo de enrutamiento como un gráfico.

> Ejemplo: una contiene `classify`¿Qué es esto?`refund`¿Qué es esto?`bug`¿Qué es esto?`sales`¿Qué es esto?`done`节点的代理路由工作流作为图──

### Ejecución duradera

Después de que cada nodo regrese, el tiempo de ejecución serializa el estado y lo escribe a un punto de control (SQLite, Postgres, Redis, personalizado).`resume(session_id)`y recoger desde el paso N + 1 con estado exacto.

> Cada nodo regresa después, el estado de secuenciación del ejecutivo y se escribe en el punto de control del ejecutivo.`resume(session_id)`No se sigue en el paso N+1 con el estado exacto.

Los documentos de LangGraph destacan explícitamente a los usuarios de producción donde esto importa: Klarna, Uber, JP Morgan. La afirmación no es la forma del gráfico; es que la forma del gráfico más el punto de control hace que la recuperación sea barata.

> ¿ Qué es esto ?**【类比】**El control de LangGraph es como el "archivo automático" del juego: cada uno de los tramos de control de control de control de control de control de control de control de control de control de control de control de control de control de control de control de control de control de control de control de control de control de control de control de control de control de control de control de control de control de control de control de control de control de control de control de control de control de control de control de control de control de control de control de control de control de control de control de control de control de control de control de control de control de control de control de control de control de control de control de control de control de control de control de control de control de control de control de control de control de control de control de control de control de control de control de control de control de control de control de control de control de control de control de control de control de control de control de control de control de control de control de control de control de control de control de control de control de control de control de control de control de control de control de control de control de control de control de control de control de control de control de control de control de control de control de control de control de control de control de control de control de control de control de control de control de control de control de control de control de control de control de control de control de control de control de control de control de control de control de control de control de control de control de control de control de control de control de control de control de control de control de control de control de control de control de control de control de control de control de control de control de control de control de control de control de control de control de control de control de control de control de control de control de control de control de control de control de control de control de control de control de control de control de control de control de control de control de control de control de control de control de control de control de control de control de control de control de control de control de control de control de control de control de control de control de control de control de control de control de control de control de control de control de control de control de control de control de control de control de control de control de control de control de control de control de control de control de control de control de control de control de control de control de control de control de control de control de control de control de control de control de control de`resume(session_id)`¿Qué pasa?

> LangGraph 文档明确强调这一点的生产用户:Klarna、Uber、J.P. Morgan──声明不是图形的形状;而是图形的形状加上检查点使恢复成本很低──

### En streaming

Cada nodo puede producir una salida parcial. El gráfico transmite eventos por nodo-delta al llamador para que las UI se actualicen a medida que se ejecuta el gráfico.

> Cada nodo puede generar una parte de la salida.

### Hombre en el ciclo

Inspeccionar y modificar el estado entre los nodos. Implementaciones: pausa antes de un nodo crítico, estado de superficie a un humano, acepta modificaciones, reanuda. El checkpointer hace esto fácil porque el estado ya está serializado.

> En el punto entre el estado de control y modificación. Método de realización: en el punto clave, el estado de demostración se detenga en el momento de la presentación.

### La memoria

A corto plazo (dentro de una ejecución  historial de conversaciones en estado) y a largo plazo (a través de las carreras  persistente a través del checkpointer más una tienda a largo plazo separada). LangGraph se integra con sistemas de memoria externa (Mem0, personalizado) a través de herramientas.

> 短期 (一次运行内状态中的对话历史) 和长期 (长期) 跨运行 (长期) 通过检查点器加独立长期储存持久化) 长图 通过工具与外部记忆系统 (memoría) 长图 (también conocido como memoria) 长图 (también conocido como memoria) 长图 (también conocido como memoria) 长期 (también conocido como memoria) 长期 (también conocido como memoria) 长期 (también conocido como memoria) 长期 (también conocido como memoria) 长期 (también conocido como memoria) 长期 (también conocido como memoria) 长期 (también conocido como memoria) 长期 (también conocido como memoria) 长期 (también conocido como memoria) 长期 (también conocido como memoria) 长期 (también conocido como memoria) 长期 (también conocido como memoria) 长期 (también conocido como memoria) 长期) 长期 (también conocido como memoria) 长期 (también conocido como memoria) 长期) 长期 (también conocido como memoria) 长期) 长期 (también conocido como 长期)

### Tres topologías

1. **Supervisor.**El router central LLM envía a los sub-agentes especializados. `create_supervisor()`En el`langgraph-supervisor`(aunque el equipo de LangChain en 2026 recomienda hacer esto a través de herramientas que piden directamente más control de contexto).
   En inglés:**监督者。**Centro de la Dirección General de Maestría en Ciencias Científicas
2. **Swarm / peer-to-peer.**Los agentes se entregan directamente a través de una superficie compartida de herramientas.
   En inglés:**群体/点对点。**Agente 通過共享工具接口直接移交──无中央路由──
3. **Hierarchical.**Supervisores que gestionan subsupervisores, implementados como subgrafos en niedo.
   En inglés:**层次化。**监督者管理子监督者, ejecutado para嵌套子图──

### Cuando este patrón va mal

> ️ **【易错点】**El fracaso más común es el punto de partida.`datetime.now()`O con el número, estos valores cambiarán al recuperarse.**后果**Desde el punto de control, el punto se ejecuta de nuevo con resultados diferentes a los de la operación original, y todo el estado entra en un caos.**一行修复**Todos los elementos de la API deben ser capturados en el estado, en el estado de la función de punto de lectura y no en el estado de la función de regulación directa.`datetime.now()`¿Qué es eso?

- **Checkpoints too small.**Sólo el punto de control de conversación gira deja el estado de la herramienta y la memoria escribe irrecuperable.
  En inglés:**检查点太小。**                                                                                                                                                                                                                                                              
- **Non-deterministic nodes.**Resume asume que las entradas de nodos producen la misma actualización de estado. Se deben capturar semillas aleatorias, relojes de pared, API externas.
  En inglés:**非确定性节点。**恢复假设节点输入产生相同状态更新──随机种子、挂钟时间、外部 API 必须被捕──
- **Over-use of conditional edges.**Un gráfico con cada borde condicional es una máquina de estado que no se puede razonar. Prefiere cadenas lineales con ramas ocasionales.
  En inglés:**过度使用条件边。**Cada línea es un estado de condiciones de un estado inexplicable.

> ¿ Qué es esto ?**【困惑】**P: 三种拓(supervisor、swarm、hierárquico) ¿qué es lo que hay que elegir?**任务可分解为独立角色**(如客服/退款/技术) seleccionar a un supervisor;**Agent 之间是协作关系而非派发关系**(如辩、相互 review) Seleccionar el enjambre;**任务有天然层次结构**(por ejemplo, "product line A 下分 5 个团队") seleccionar jerárquico。LangChain 团队 2026 年建议:能直接用工具调用解决就别上监督直接工具调用上下文控制更精细──

## Construye con movimiento.
```figure
langgraph-state
```

## Construye el mismo

`code/main.py`Implementa un gráfico de estados de stdlib:

> `code/main.py`Utilizando la base de datos se ha logrado un estado gráfico:

- `State` un dictado escrito con `messages`¿ Qué ?`step`¿ Qué ?`route`¿ Qué ?`output`¿ Qué ?`human_approval`¿ Qué ?
  En inglés:`State`包含 `messages`¿Qué es esto?`step`¿Qué es esto?`route`¿Qué es esto?`output`¿Qué es esto?`human_approval`De la clase de dictado.
- `Node` Callable tomando estado y devolviendo un dictado de actualización.
  En inglés:`Node` acepta el estado y vuelve a actualizar el dictado de objetos ajustables。
- `StateGraph` nodos + bordes + bordes condicionales + ejecutar + reanudar.
  En inglés:`StateGraph`节点 + 边 + 条件边 + 运行 + 恢复。
- `SQLiteCheckpointer`(falsas en memoria)  serializa estado después de cada nodo; `load(session_id)`- ¿Qué es eso?
  En inglés:`SQLiteCheckpointer`(内存模拟)  estado de secuenciación de cada punto posterior;`load(session_id)` Recuperación
- Un gráfico de demostración: clasificar -> rama(reembolso / error / ventas) -> puerta humana -> enviar.
  En el caso de las empresas de la industria de la información, el sistema de información de la empresa es un sistema de información de la empresa.

- ¿Qué quieres decir ?

> 运行:

```
python3 code/main.py
```

El rastro muestra la primera carrera fallando en la puerta humana, persistencia, luego reanudar la producción final.

> El trayecto muestra que la primera operación en el control humano ha fracasado, se ha perpetuado y luego se ha recuperado para producir la salida final.

## Usalo con el marco de ejecución

- **LangGraph** el referente, listo para producción.`create_react_agent`¿ Qué ?`create_supervisor`, o construir su propio gráfico.
  En inglés:**LangGraph**参考实现,生产就绪──使用 `create_react_agent`¿Qué es esto?`create_supervisor`O construir su propio dibujo.
- **AutoGen v0.4**(Lección 14)  Modelo alternativo de actores para escenarios de alta competencia.
  En inglés:**AutoGen v0.4**(第 14 课) 高并发场景的 actor 模型替代方案──
- **Claude Agent SDK**(Lección 17)  Arnes administrado con tienda de sesiones integrada.
  En inglés:**Claude Agent SDK**(第 17 课) 带内置会话存储的托管框架──
- **Custom** cuando necesite un control exacto sobre la forma del estado o el backend del checkpointer.
  En inglés:**自定义** Cuando necesite un control preciso de la forma del estado o de la terminal del punto de inspección.

## Envíe el producto .

`outputs/skill-state-graph.md`genera un gráfico de estado en forma de LangGraph en cualquier tiempo de ejecución objetivo con control y resumen conectado.

> `outputs/skill-state-graph.md`En cualquier objetivo de ejecución generar gráfico de estado de forma LangGraph, punto de control interno y recuperación.

## Los ejercicios.

1. Añadir un borde condicional de `classify`¿ Qué ?`end`Cuando la confianza de clasificación está por debajo de un umbral, reanuda la carrera después de un conjunto humano.`route`manualmente.
   Cuando la confianza en la clase baja es de valor cuando se añade `classify`¿ Qué ?`end`La situación es muy difícil.`route`后恢复运行──
2. Cambiar el falso de SQLite por un verdadero punto de control SQLite.
   En inglés, el método de cálculo de la cantidad de datos de un SQLite es el método de cálculo de un SQLite.
3. Implementar bordes paralelos: dos nodos se ejecutan simultáneamente, se fusionan por un reducidor personalizado. ¿Qué compra el estado inmutable aquí?
   En inglés, "realizar y ejecutar": dos nodos que se ejecutan con un reducidor de auto-definición 合并──.
4. Leer .`langgraph-supervisor`- ¿Qué es lo que se hace?`create_supervisor`Comparar las formas de las huellas.
   En inglés:`langgraph-supervisor`参考──将玩具移植为 `create_supervisor`◊ Comparar el trayecto
5. Añadir streaming: cada nodo produce estado parcial mientras se ejecuta. Imprimir los deltas a su llegada.
   Traducción:Additional flow: cada punto del proceso produce un estado parcial.

## Términos clave .

| Term | What people say | What it actually means |
|------|-----------------|-----------------------|
| 术语 | 通俗说法 | 实际含义 |
| State graph | "Agent as state machine" / "Agent 即状态机" | Typed state + nodes + edges + reducers / 带类型状态 + 节点 + 边 + reducer |
| Checkpointer | "Persistence backend" / "持久化后端" | Serializes state after every node; enables resume / 每个节点后序列化状态；支持恢复 |
| Reducer | "State merger" / "状态合并器" | Function that combines current state with a node's update / 将当前状态与节点更新合并的函数 |
| Conditional edge | "Branch" / "分支" | Edge chosen by a function of state / 由状态函数选择的边 |
| Subgraph | "Nested graph" / "嵌套图" | A graph used as a node inside another graph / 作为另一个图内节点使用的图 |
| Durable execution | "Resume from failure" / "从失败恢复" | Restart at the last successful node with exact state / 在最后成功节点处用精确状态重启 |
| Supervisor | "Router LLM" / "路由 LLM" | Central dispatcher for specialist subagents / 专家子 Agent 的中央分派器 |
| Swarm | "P2P agents" / "P2P Agent" | Agents hand off via shared tools; no central router / Agent 通过共享工具移交；无中央路由 |

## Más Leer más Leer más

- [LangGraph overview](https://docs.langchain.com/oss/python/langgraph/overview) los documentos de referencia
  En el caso de los países de la región de la Unión Soviética, el nombre de la región de la Unión Soviética es el de la República Popular China.
- [langgraph-supervisor reference](https://reference.langchain.com/python/langgraph/supervisor/) API de patrón de supervisión
  La información de la empresa se encuentra en el archivo de la empresa.
- [AutoGen v0.4, Microsoft Research](https://www.microsoft.com/en-us/research/articles/autogen-v0-4-reimagining-the-foundation-of-agentic-ai-for-scale-extensibility-and-robustness/) Alternativa de actor-modelo
  En inglés, el nombre de la versión de AutoGen es "AutoGen v0.4".
- [Claude Agent SDK overview](https://platform.claude.com/docs/en/agent-sdk/overview) Tienda de sesiones y subagentes
  En inglés, el nombre de la persona que representa a la persona que representa a la persona que representa a la persona que representa a la persona que representa a la persona que representa a la persona que representa a la persona que representa a la persona que representa a la persona que representa a la persona que representa a la persona que representa a la persona que representa a la persona que representa a la persona que representa a la persona que representa a la persona que representa a la persona que representa a la persona que representa a la persona que representa a la persona que representa a la persona que representa a la persona que representa a la persona que representa a la persona que representa a la persona en la persona.
