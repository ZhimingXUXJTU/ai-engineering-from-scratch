#  LangGraph vs CrewAI vs AutoGen vs Agno  Agent 框架对比: LangGraph vs CrewAI vs AutoGen vs Agno
# Negocios de marco de agentes  Gráfico, papel y orquestación de actores

> Cada marco vende la misma demostración (el agente de investigación construye un informe) y oculta el mismo error (el esquema de estado lucha con la capa de orquestación).

> **【中文解读】**Cada marco muestra la misma demostración, todos ocultan el mismo error, los esquemas de estado y los conflictos de orden.

> **【拓展：框架选择→Agent工程实践】**LangGraph  adaptado a la necesidad de un flujo de trabajo de estado de control preciso; CrewAI  adaptado a múltiples papeles; AutoGen  adaptado a múltiples agentes de conversación; Selection error framework es la principal causa del fracaso del proyecto de agente.

> ¿ Qué es esto ?**【前置】**学本节前请先掌握:Fase 11·09(Function Calling)、Fase 11·16(LangGraph)。本节是Fase 11的最后一节,对比 4 个主流框架(LangGraph、CrewAI、AutoGen、Agno) 的优劣──最好已经分别使用过其中2个个──

**Type:** Learn | **类型:** 学习
**Languages:** Python | **语言:** Python
**Prerequisites:** Phase 11 · 09 (Function Calling), Phase 11 · 16 (LangGraph) | **前置知识:** Phase 11 · 09 (函数调用)、16 (LangGraph)
**Time:** ~45 minutes | **时间:** ~45 分钟

## El problema es la introducción del problema

Puede ser un flujo de trabajo de investigación (planar, buscar, resumir, citar). Puede ser un flujo de revisión de código (parse diff, criticar, parchear, validar). Puede ser un asistente de múltiples turnos que hace libros de vuelos, escribe correos electrónicos y archivará informes de gastos.

> Tienes una tarea que necesita varias veces para el LLM. Quizás es el estudio de la labor. Quizás es un marco.

Tres días después, descubres la fuga de abstracciones del marco. CrewAI te da roles pero te pelea cuando el "investigador" necesita entregar un plan estructurado al "escrito". AutoGen te da chat entre agentes pero no tiene estado de primera clase así que tu punto de control es un picante de un registro de conversaciones. LangGraph te da un gráfico de estado pero te obliga a nombrar cada transición antes de saber lo que hará el agente. Agno te da una abstracción de un solo agente que grita cuando intentas extenderte a tres trabajadores simultáneos.

> Tres días después, descubres que el marco de abstracción se va a filtrar. La tripulación te da un papel, pero cuando el "investigador" necesita un plan estructurado para entregarle al "autor" surge un problema. AutoGen te da un agente, pero no tiene un estado civil.

La solución no es "elija el mejor marco". Es para coincidir con la abstracción del núcleo del marco a la forma de su problema.

> El método de reparación no es "escollir el mejor marco" sino que el abstracto central del marco se ajusta a la forma de tu problema.


> **【中文解读】**Agente 框架选型的三个维度:(1) 任务复杂度简单 RAG 用LlamaIndex,复杂 Agent 用LangGraph;(2) 团队经验新手用LangChain 模板,专家用原生API;(3) 生产要求需要LangSmith 集成选LangChain 生态──

> ¿ Qué es esto ?**【类比】**选 Agent 框架像选交通工具短途买菜用自行车(stdlib + función llamando),跨城出差用车(LangGraph 状态机),多人旅行用面包车(CrewAI 角色),即时通讯用电话(AutoGen 对话) ⋅ Cada tipo de trabajo tiene escenario adecuado, "cuál es el mejor" es un problema de error, "cuál es la forma de problema que se ajusta a ti" es sólo──

> ️ **【易错点】**框架选错的 3 个常见原因:(1) **跟风最热门**AutoGen 火就上 AutoGen, resultados de la búsqueda de tareas son sólo un agente único + 工具,过度工程;先评估任务复杂度再选框架――(2) **被 demo 误导**Demo de "Researchers+Autors" de CrewAI parece muy bueno, pero en realidad el papel en la tarea es muy confuso, el papel de CrewAI es abstracto y retrasado; primero, hacer un PoC 验证抽象匹配──(3) **低估迁移成本** Comience con Agno 简单,后期要增加 Agent 时发现Agno不支持,重写到 LangGraph 花两周;选框架时看 6 个月后的需求──


## El concepto central.

> **【中文解读】**La selección de un agente es un proceso de diseño:LangChain 生态最完整但复杂度高,LlamaIndex 专注RAG,CrewAI 适合多代理 协作,LangGraph 适合状态机控制流,直接使用API最灵活但要自己写更多代码──

> **【拓展：Agent 框架的选型指南】**选型维度:(1) 任务复杂度(简单 RAG 用 LlamaIndex,复杂 Agent 用 LangGraph);(2) 团队经验(新手用 LangChain 模板,专家用原生API);(3) 生产要求(LangSmith 集成选 LangChain 生态) ――2025年趋势是框架轻量化──


![Agent framework matrix: core abstraction vs problem shape](../assets/framework-matrix.svg)

Cuatro marcos dominan el paisaje de 2026. Sus abstracciones centrales no son las mismas.

> Cuatro marcos dominaron la estructura del año 2026: sus estrategias centrales son diferentes.

| Framework | Core abstraction | Best fit | Worst fit |
|-----------|------------------|----------|-----------|
| **LangGraph** | `StateGraph` — typed state, nodes, conditional edges, checkpointer. | Workflows with explicit state and human-in-the-loop interrupts; production agents needing time-travel debugging. | Loose, role-driven brainstorming where the topology is unknown. |
| **CrewAI** | `Crew` — roles (goal, backstory), tasks, process (sequential or hierarchical). | Role-playing or persona-driven workflows with a short linear/hierarchical plan. | Anything stateful beyond the crew's turn history; complex branching. |
| **AutoGen** | `ConversableAgent` pair — two or more agents that speak in turns until an exit condition. | Multi-agent *dialogue* (teacher-student, proposer-critic, actor-reviewer) where the thinking emerges from the chat. | Deterministic workflows with a known DAG; anything needing durable state across restarts. |
| **Agno** | `Agent` — a single LLM + tools + memory, composable into teams. | Fast-to-build single agents and lightweight teams; strong multi-modality and built-in storage drivers. | Deep, explicitly-branched graphs with custom reducers. |

### ¿Qué significa realmente "abstracción"?

La abstracción central de un marco es lo que dibujas en la pizarra cuando presentas la arquitectura.

> El abstracto central del marco es lo que se pinta en una tabla blanca cuando se vende la arquitectura.

- **LangGraph**Los nodos son pasos, los bordes son transiciones, y el objeto de estado en cada punto se escribe.
  Tu dibujas una imagen. El punto es un paso, el borde es un cambio.
- **CrewAI**→ se dibuja un organograma. cada rol tiene una descripción de trabajo y un gerente rutas tareas. el modelo mental es un pequeño equipo de especialistas.
  Usted dibuja una organización. Cada papel tiene una descripción de las responsabilidades, el gerente distribuye las tareas.
- **AutoGen**Dos agentes se envían mensajes; un tercero se une si necesitas un moderador. El modelo mental es el chat.
  Tú dibujas un Slack 私信. Dos agentes.
- **Agno**→ dibujas una sola caja con herramientas colgando de ella. Pones cajas juntas para un equipo. El modelo mental es "agente con baterías incluidas".
  Te dibujas un cuadro de herramienta en el que te cuelgas.

### La cuestión del Estado

El Estado es donde la mayoría de las opciones de marco se desmoronan en la producción.

> 状态是大多数框架选择在生产中出问题的地方──

- **LangGraph.**Estado de tipo (`TypedDict`El modelo Pydantic, por campo reducidores, punto de control de primera clase (SQLite/Postgres/Redis).
  **LangGraph。**类型化状态`TypedDict`O Pydantic 模型) 、每字段 reducer、一等公民检查点器(SQLite/Postgres/Redis) ⋅恢复、中断和时间旅行免费──(见 Fase 11 · 16──)
- **CrewAI.**Los flujos de estado como cadenas entre las tareas a través de la `context`campo, o estructurados a través de `output_pydantic`No hay una tienda duradera por tripulación fuera de la caja, se puede salir por su cuenta si la tripulación debe sobrevivir a un reinicio.
  **CrewAI。**status como un enlace en tarea entre paso `context`字段流动, o por `output_pydantic`strukturización.                                                                                                                                                                                                                                                             
- **AutoGen.**Estado es el historial de chat y cualquier usuario definido `context`Las transcripciones de conversación persisten; el estado de flujo de trabajo arbitrario no lo hace a menos que escriba adaptadores.
  **AutoGen。** estado es historia de chat y cualquier usuario definido `context` Registro de diálogo persistente; estado de flujo de trabajo arbitrario no persistente, excepto en el caso de los escritos adaptados.
- **Agno.**Impulsores de almacenamiento incorporados (SQLite, Postgres, Mongo, Redis, DynamoDB) conectados a un `Agent`por medio de`storage=` las sesiones de conversación y los recuerdos del usuario persisten automáticamente.
  **Agno。**Introducción de la información en el archivo de datos`storage=`                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             `Agent`La memoria del usuario se perdurará automáticamente.

- **LangGraph.**Estado de tipo (`TypedDict`El modelo Pydantic, por campo reducidores, punto de control de primera clase (SQLite/Postgres/Redis).
- **CrewAI.**Los flujos de estado como cadenas entre las tareas a través de la `context`campo, o estructurados a través de `output_pydantic`No hay una tienda duradera por tripulación fuera de la caja, se puede salir por su cuenta si la tripulación debe sobrevivir a un reinicio.
- **AutoGen.**Estado es el historial de chat y cualquier usuario definido `context`Las transcripciones de conversación persisten; el estado de flujo de trabajo arbitrario no lo hace a menos que escriba adaptadores.
- **Agno.**Impulsores de almacenamiento incorporados (SQLite, Postgres, Mongo, Redis, DynamoDB) conectados a un `Agent`por medio de`storage=` las sesiones de conversación y los recuerdos del usuario persisten automáticamente.

### La cuestión de las ramas

Todos los agentes no triviales se suceden, quien decide las cosas.

> Cada agente extraordinario tiene su propia división.

- **LangGraph** decide, a través de bordes condicionales. El enrutamiento es una función de Python con ramas nombradas. Las ramas son de primera clase en el gráfico compilado; el checkpointer registra qué rama se tomó.
  **LangGraph**你决定,通过条件边──路由是带命名分支的 Python 函数──分支是编译图中的一等公民;检查点器记录走哪条──
- **CrewAI** el administrador decide en modo jerárquico; en modo secuencial usted decide en el tiempo de construcción. El enrutamiento está implícito en la lista de tareas; no hay "si" de primera clase fuera del prompt del administrador.
  **CrewAI**分层模式由经理决定;顺序模式你在构建时决定──路由隐含在任务列表中;经理提示外无一等公民"if"──
- **AutoGen** los agentes deciden por chat.`GroupChatManager`selecciona el próximo orador; puede escribir a mano un `speaker_selection_method`pero el defecto es impulsado por el LLM.
  **AutoGen**Agent 通過聊天決定──分支從誰下一個說話中涌现──`GroupChatManager`选下一个发言人;可手写 `speaker_selection_method`Pero el LLM es un proceso de aprendizaje.
- **Agno** el agente decide con qué herramienta llamar a continuación. los equipos tienen un modo coordinador/router/colaborador; la ramificación más allá de eso es responsabilidad del desarrollador.
  **Agno**Agent 通过下一个调用哪个工具决定──团队有协调员/路由器/合作者模式;

- **LangGraph** decide, a través de bordes condicionales. El enrutamiento es una función de Python con ramas nombradas. Las ramas son de primera clase en el gráfico compilado; el checkpointer registra qué rama se tomó.
- **CrewAI** el administrador decide en modo jerárquico; en modo secuencial usted decide en el tiempo de construcción. El enrutamiento está implícito en la lista de tareas; no hay "si" de primera clase fuera del prompt del administrador.
- **AutoGen** los agentes deciden por chat.`GroupChatManager`selecciona el próximo orador; puede escribir a mano un `speaker_selection_method`pero el defecto es impulsado por el LLM.
- **Agno** el agente decide con qué herramienta llamar a continuación. los equipos tienen un modo coordinador/router/colaborador; la ramificación más allá de eso es responsabilidad del desarrollador.

### La cuestión de la observabilidad

> ¿Qué es lo que se puede hacer?

- **LangGraph** OpenTelemetry a través de LangSmith o cualquier exportador de OTel. Cada transición de nodo es un lapso de rastreo; los puntos de control se duplican como rastros reproducibles. LangSmith es la opción de primera parte; Langfuse / Phoenix también tiene adaptadores.
  **LangGraph**A través de LangSmith o cualquier OTel 导出器的 OpenTelemetry── cada punto de transformación es un espacio de rastreo; inspección y seguimiento de nuevo.
- **CrewAI** OpenTelemetry de primera clase desde finales de 2025; integraciones con Langfuse, Phoenix, Opik, AgentOps.
  **CrewAI**2025 年末起一等公民OpenTelemetry;集成 Langfuse、Phoenix、Opik、AgentOps。
- **AutoGen** Integrar la Telemetría abierta a través de `autogen-core`AgentOps y Opik tienen conectores.
  **AutoGen** Por el `autogen-core`La capacidad de seguimiento es de cada agente, no de cada punto.
- **Agno** incorporado `monitoring=True`bandera más exportadores OpenTelemetry; estrecha integración con Langfuse para las pistas de sesiones.
  **Agno**内置                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                          `monitoring=True`标志加 OpenTelemetry 导出器;与 Langfuse 紧密集成会话追踪──

### Costo y latencia

Los cuatro frameworks añaden gastos generales por llamada (lógica de marco, validación, serialización). Orden aproximada de aumento de gastos generales: Agno ≈ LangGraph < CrewAI ≈ AutoGen. La diferencia está dominada por la cantidad de enrutamiento adicional de LLM que hace el framework.`GroupChatManager`LangGraph sólo gasta tokens donde escribe.`llm.invoke`El camino de Agno es delgado.

> Cuatro marcos aumentarán en cada período de trabajo.

Cuando el costo por carrera es importante, prefiere el enrutamiento explícito (LangGraph edges, AutoGen `speaker_selection_method`) sobre el itinerario seleccionado por el LLM.

> Cuando el coste de cada operación es importante, se debe priorizar el uso de rutas de forma explícita y no de rutas de LLM.

### Interoperabilidad

> 互操作性 互操作性 互操作性 互操作性 互操作性 互操作性 互操作性 互操作性 互操作性 互操作性 互操作性 互操作性

- **LangGraph**¿ Qué es esto ?**LangChain**herramientas, retrievers, LLM. Adaptador MCP de primera clase (herramientas importadas como servidores MCP).
  **LangGraph**¿ Qué es esto ?**LangChain**工具、检索器、LLM──一等公民 MCP 适配器(工具作为 MCP 服务器导入)
- **CrewAI** herencias heredadas de herramientas `BaseTool`Las herramientas de LangChain, LlamaIndex y MCP se adaptan a la experiencia de la tripulación.`allow_delegation=True`¿ Qué ?
  **CrewAI** 工具继承自                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                       `BaseTool`• LongChain 工具、LlamaIndex 工具、MCP 工具都适配进来──crew-to-crew 委派通过 `allow_delegation=True`¿Qué es eso?
- **AutoGen**¿ Qué es esto ?`FunctionTool`Envuelve cualquier Python de llamadas; adaptador MCP disponible.
  **AutoGen**¿ Qué es esto ?`FunctionTool`Packing cualquier Python puede ser utilizado; MCP 适配器可用──与 AG2 生态紧密合用于代理 间模式──
- **Agno**¿ Qué es esto ?`@tool`decorador o subclase BaseTool; adaptador MCP; las herramientas pueden ser compartidas entre agentes y equipos.
  **Agno**¿ Qué es esto ?`@tool`装饰器或 BaseTool 子类;MCP 适配器;工具可跨 Agent 和团队共享──

## La habilidad

> Puedes explicar, en una frase, por qué un marco dado es adecuado para un problema de agente dado.
> Puedes usar una frase para explicar por qué un marco se adapta a un problema de un agente.

Lista de verificación de preconstrucción:

> 构建前检查清单:

1. **Draw the shape.**¿Es un gráfico (estado tipado, transiciones nombradas)? ¿Un juego de rol (especialistas abandonan el trabajo)? ¿Un chat (agentes hablan hasta que terminan)? ¿Un agente único con herramientas?
   **画出形状。**¿Es un dibujo, un papel, una charla o un agente solo con herramientas?
2. **Decide who branches.**Desarrollo decidido por el desarrollador → LangGraph. Gerente-agente decidido → CrewAI jerárquico. Chat emergente → AutoGen. Herramienta-llamada decidida → Agno.
   **决定谁分支。**开发者决定 → LangGraph──经理 Agente decide → CrewAI──聊天涌现 → AutoGen──工具调用决定 → Agno──
3. **Check the state budget.**¿Necesitas un currículum desde el punto de control? Viajes en el tiempo? Interrumpe el ser humano a mitad de carrera? Si es así, LangGraph es el predeterminado; sesiones Agno cubren el estado de conversación.
   **检查状态预算。**¿Necesitas recuperarte de la inspección? ¿Tiempo de viaje? ¿Cancelar en interrupción artificial?
4. **Check the cost budget.**El enrutamiento seleccionado por LLM cuesta tokens adicionales por turno.
   **检查成本预算。**El proceso de selección de LLM se realiza por cada ronda de los tokens de consumo adicional.
5. **Budget the framework overhead.**Cada marco es otra dependencia. Si la tarea es dos llamadas de LLM y una herramienta, escriba 30 líneas de Python simple; ningún marco es más barato que ningún marco.
   **预算框架开销。**Cada marco es otro dependiente. Si la tarea es sólo dos veces LLM 调用一个工具, escribir 30 行纯Python.

Rechazarse a buscar un marco antes de poder dibujar el gráfico, el organograma, el chat o la caja de agentes.

> Antes de que puedas dibujar, organizar, charlar o el marco de agente, no te estires el marco. No elijas algo que te obligue a luchar por su modelo de estado.

## La matriz de decisiones

| Problem shape | Preferred framework | Why |
|---------------|---------------------|-----|
| Workflow DAG with typed state, human approvals, long-running | LangGraph | First-class state, checkpointer, interrupts, time-travel. |
| Research / writing pipeline with distinct roles | CrewAI (sequential) or LangGraph subgraphs | Role-per-task is cheap to express in CrewAI; scale up with LangGraph when branching gets complex. |
| Proposer-critic or teacher-student dialogue | AutoGen | Two-agent chat is its native shape. |
| Single agent with tools, sessions, memory | Agno | Thinnest setup, built-in storage and memory. |
| Thousands of parallel fanouts with reducers | LangGraph + `Send` | The only one with a first-class parallel-dispatch API. |
| Quick prototype, no framework commitment | Plain Python + provider SDK | No framework is the fastest framework. |

| 问题形状 | 推荐框架 | 原因 |
|---------|---------|------|
| 类型化状态的工作流 DAG、人工审批、长期运行 | LangGraph | 一等公民状态、检查点、中断、时间旅行 |
| 研究写作流水线带不同角色 | CrewAI（顺序）或 LangGraph 子图 | CrewAI 表达每任务角色便宜；分支复杂时用 LangGraph |
| 提议者-评论者或师生对话 | AutoGen | 双 Agent 聊天是其原生形状 |
| 单 Agent 带工具、会话、记忆 | Agno | 最薄设置，内置存储和记忆 |
| 数千并行扇出带 reducer | LangGraph + `Send` | 唯一带一等公民并行分派 API 的 |
| 快速原型、不绑定框架 | 纯 Python + 提供商 SDK | 无框架是最快的框架 |

## Los ejercicios.
```figure
l5-framework-fit
```

## Los ejercicios

1. **Easy.**Tome la misma tarea  "investigar la sede de Anthropic, escribir un breve de 200 palabras, citar fuentes"  y implementarlo en LangGraph (cuatro nodos: planear, buscar, escribir, citar) y en CrewAI (tres roles: investigador, escritor, editor).
   Utilizando la misma tarea en LangGraph y CrewAI, reportar el número de tokens, componentes y código ejecutados en cada operación.
2. **Medium.**Construir la misma tarea en AutoGen (investigador  escritor chat, editor se une a través `GroupChat`) y Agno (un solo agente con `search_tools`y `write_tools`Las cuatro implementaciones se clasifican en: a) costo por carrera, b) capacidad de reanudar después de un accidente, c) capacidad de inyectar una aprobación humana antes del paso de escritura.
   En AutoGen y Agno se realiza la misma tarea, según el costo, la capacidad de recuperación, la capacidad de aprobación artificial e inyección de la clasificación.
3. **Hard.**Construir un guión de árbol de decisión `pick_framework.py`que toma una breve descripción del problema (JSON: `{has_typed_state, has_roles, has_dialogue, has_parallel_fanout, needs_resume}`En el caso de los casos de la Comisión, el Consejo de Ministros de la Unión Europea (CE) y el Consejo de Ministros de la Unión Europea (CE) han presentado una recomendación con una justificación de una frase.
   构建决策树脚本, en función de la descripción de los problemas, regresar al marco de recomendaciones.

## Términos clave .

| Term | What people say | What it actually means | 中文释义 |
|------|-----------------|-----------------------|---------|
| Orchestration | "How the agents coordinate" / "Agent 如何协调" | The layer that decides which node/role/agent runs next. | 编排：决定哪个节点/角色/Agent 下一步运行的层 |
| Durable state | "Resume after a restart" / "重启后恢复" | State that survives process death, attached to a checkpoint or session store. | 持久状态：在进程终止后仍存活的状态 |
| LLM-selected routing | "Let the model decide" / "让模型决定" | A planner LLM picks the next step each turn; flexible but pays tokens on every decision. | LLM 选择路由：规划 LLM 每轮选择下一步 |
| Explicit routing | "Developer decides" / "开发者决定" | A Python function or static edge picks the next step; cheap and auditable. | 显式路由：Python 函数或静态边选择下一步 |
| Crew | "A CrewAI team" / "CrewAI 团队" | Roles + tasks + process (sequential or hierarchical) bound into a single runnable. | Crew：角色+任务+流程绑定成一个可运行单元 |
| GroupChat | "AutoGen's multi-agent chat" / "AutoGen 多 Agent 聊天" | A managed conversation between N agents with a speaker selector. | GroupChat：N 个 Agent 之间的托管对话 |
| Team (Agno) | "Multi-agent Agno" / "多 Agent Agno" | Route / coordinate / collaborate mode over a set of agents. | Team (Agno)：Agent 集合上的路由/协调/协作模式 |
| StateGraph | "LangGraph's graph" / "LangGraph 图" | Typed-state, node, conditional-edge, checkpointer abstraction. | StateGraph：类型化状态、节点、条件边、检查点抽象 |

## Más Leer más Leer más

- [LangGraph documentation](https://langchain-ai.github.io/langgraph/) StateGraph, puntos de control, interrupciones, viajes en el tiempo.
  LangGraph 文档StateGraph、检查点、中断、时间旅行──
- [CrewAI documentation](https://docs.crewai.com/) Equipos, flujos, agentes, tareas, procesos.
  El equipo de trabajo 文档 Crew、Flow、Agent、Task、Proceso。
- [AutoGen documentation](https://microsoft.github.io/autogen/) ConversableAgent, GroupChat, equipos, herramientas.
  AutoGen 文档ConversableAgent、GroupChat、 equipos、herramientas。
- [Agno documentation](https://docs.agno.com/)Agente, equipo, flujo de trabajo, almacenamiento, memoria.
  Agno 文档Agent,Equipo, Flujo de trabajo, almacenamiento, memoria
- [Anthropic — Building effective agents (Dec 2024)](https://www.anthropic.com/research/building-effective-agents) biblioteca de patrones (cadena de instrucciones, enrutamiento, paralelación, orquestación-trabajadores, evaluador-optimizador) marco-agnóstico.
  Antropic  Sobre la construcción de un agente eficaz 模式库, framework无关.
- [Yao et al., "ReAct: Synergizing Reasoning and Acting" (ICLR 2023)](https://arxiv.org/abs/2210.03629) el bucle cada marco se pone de moda.
  Cada marco está en el envasado en el ciclo original de ReAct.
- [Wu et al., "AutoGen: Enabling Next-Gen LLM Applications via Multi-Agent Conversation" (2023)](https://arxiv.org/abs/2308.08155) El papel de diseño de AutoGen.
  AutoGen's diseño de la página web
- [Park et al., "Generative Agents: Interactive Simulacra of Human Behavior" (UIST 2023)](https://arxiv.org/abs/2304.03442) base de juego de rol en la que se basan las pilas de personajes de estilo CrewAI.
  La tripulación 风格角色堆所基于的角色扮演基础──
- Fase 11 · 16 (Langgraph)  el marco que esta lección comparte.
  Este es el marco de base de la clase en comparación.
- Fase 11 · 19 (Reflexión)  un patrón que se mapea limpio a LangGraph pero incómodo a CrewAI.
  Una en LangGraph, pero un modelo de mal funcionamiento en CrewAI.
- Fase 11 · 22 (Observabilidad de producción)  cómo utilizar el instrumento en función del marco que elija.
  ¿Cómo puedes elegir cualquier marco para añadir observaciones?
