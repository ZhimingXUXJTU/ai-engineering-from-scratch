# El modelo primitivo multi-agente.

> Cuatro primitivas, nada más  el agente, la entrega, el estado compartido, el orquestrador  abarcan un espacio de diseño en cuatro dimensiones, y los principales marcos multi-agentes que se enviarán en 2026 (AutoGen, LangGraph, CrewAI, OpenAI Agents SDK, Microsoft Agent Framework) son puntos en él. Esta lección los construye desde cero, ejecuta un sistema de juguetes en los cuatro, luego mapea cada marco principal en los mismos ejes para que pueda leer cualquier nueva versión en un párrafo.

> **【中文解读】**Este capítulo presenta los elementos básicos de la estructura del sistema de agentes y de la interacción original.

> **【拓展：primitive model→具体应用】**多 Agent 系统的最小原语模型定义了 Agent 之间基本交互模式:(1) 消息传递Agent 通过发送消息通信;(2) 共享状态Agent 通过阅读写共享存储协调;(3) 事件通知Agent 订阅感兴趣的事件──AutoGen 用消息传递,LangGraph 用共享状态,黑板系统用事件通知──大多数实际系统混合使用多种原语──


**Type:** Learn | **类型:** 学习
**Languages:** Python (stdlib) | **语言:** Python (标准库)
**Prerequisites:** Phase 14 (Agent Engineering), Phase 16 · 01 (Why Multi-Agent) | **前置知识:** Phase 14 (Agent 工程), Phase 16 · 01 (为什么需要多 Agent)
**Time:** ~60 minutes | **时间:** ~60 分钟

> ¿ Qué es esto ?**【前置】**学本节前请先掌握:Fase 14(Agent 工程) 、Fase 16·01(多 Agent 动机) 。本节是Fase 16 的核心4个原语(agent/handoff/shared-state/orchestrator) define所有框架的设计空间。
> ¿ Qué es esto ?**【类比】**4 原语 = "音乐四件套":agente(乐手)、handoff(独奏接力)、shared state(总谱)、orquestrator(指挥)。AutoGen 偏消息传递、LangGraph 偏共享状态、CrewAI 偏角色分工

## # El problema # # El problema #

Cada seis meses un nuevo marco multi-agente se lanza. AutoGen en 2023. CrewAI en 2024. LangGraph y OpenAI Swarm en 2024. Google ADK en abril de 2025. Microsoft Agent Framework RC en febrero de 2026. Cada comunicado de prensa afirma ser "la abstracción correcta".

> Cada seis meses se publicará un nuevo marco multi-agente ⋅ AutoGen del año 2023 ⋅ CrewAI del año 2024 ⋅ LangGraph y OpenAI Swarm del año 2024 ⋅ Google ADK del 4 de abril del año 2025 ⋅ Microsoft Agent Framework RC del 2 de febrero del año 2026 ⋅ Cada editorial se afirma como "un verdadero abstracto".

El cambio de marcas es real pero las primitivas subyacentes no cambian. Lo que parece que la innovación es a menudo rebranding: los mismos cuatro botones (agente, entrega, estado compartido, orquesta) con diferentes valores predeterminados y sintaxis. Una vez que ves las primitivas, el marketing se desvanece.

>  cambio es real pero el lenguaje original de base no cambia.  parece que las cosas nuevas son a menudo rebrandingadas: los mismos cuatro círculos  (agente, comunicación, estado de compartir, ordenador) tienen diferentes valores y lenguaje. Una vez que ves el lenguaje original, la comercialización desaparece.

Si tratas de aprenderlos uno a la vez, se agotará. Las API se ven diferentes. Los documentos no están de acuerdo sobre lo que es un "agente". Un marco llama su memoria compartida un "tablero de control", otro lo llama un "poll de mensajes", un tercero lo llama un "StateGraph".

> Si intentas uno a uno aprenderlos, te cansará de todo. Apí se ve diferente.

No es. Bajo el marketing, las cuatro primitivas son estables. Apréndelos una vez, lea cada nuevo marco en un párrafo.

> En el mercado, cuatro idiomas originales son estables.

## Concepto de la esencia de la concepción

### Los cuatro primitivos

1. **Agent** un prompt de sistema más una lista de herramientas. Estatal; cada ejecución comienza desde su prompt de sistema y el historial de mensajes actual.
   En inglés:**Agent** Un sistema de sugerencias añadido a una lista de herramientas.
2. **Handoff** una transferencia estructurada de control de un agente a otro. Mecánica, una llamada de herramienta que devuelve un nuevo agente o un borde de gráfico que sigue una condición.
   En inglés:**交接** Transferencia de control estructural de un agente a otro agente. Mecanicamente, un nuevo agente de regreso utiliza o sigue los instrumentos de la obra.
3. **Shared state** cualquier estructura de datos que más de un agente pueda leer (a veces escribir).
   En inglés:**共享状态** Más agentes pueden leer (sometimes write in) cualquier estructura de datos.
4. **Orchestrator** quien decida quién habla después. Opciones: un gráfico explícito (determinista), un selector de altavoces de LLM (suave), la llamada de entrega del último orador (OpenAI Swarm), o un programador sobre una cola (arquitectura de conjuntos).
   En inglés:**编排器** decide quién sigue un discurso de la voz.

Todo el espacio de diseño. Cada marco elige los valores predeterminados para cada eje; el resto es la sintaxis de superficie.

> Esto es todo el espacio de diseño. Cada marco tiene un valor de elección de cada eje.

La implicación: no hay un marco multiagente "mejor". Sólo hay "mejor para las preferencias de eje de su tarea". Un marco que orquesta la orquestación para las tuberías deterministas (LangGraph) es incorrecto para conversaciones emergentes (use AutoGen). Conozca sus ejes, luego elija.

> 含义: no hay un marco multi-agente 框架── sólo un marco que se adapte más a tu objetivo 轴偏好的── en la definición de flujo de agua en el marco de la organización.

### Cómo cada marco 2026 se asigna a él

| Framework | Agent | Handoff | Shared state | Orchestrator |
|-----------|-------|---------|--------------|--------------|
| OpenAI Swarm / Agents SDK | `Agent(instructions, tools)` | tool returns Agent | caller's problem | the LLM's next handoff call |
| AutoGen v0.4 / AG2 | `ConversableAgent` | speaker-selector on GroupChat | message pool | selector function (LLM or round-robin) |
| CrewAI | `Agent(role, goal, backstory)` | `Process.Sequential / Hierarchical` | Task outputs chained | manager LLM or static order |
| LangGraph | node function | graph edge + condition | `StateGraph` reducer | the graph, deterministic |
| Microsoft Agent Framework | agent + orchestration patterns | pattern-specific | thread / context | pattern-specific |
| Google ADK | agent + A2A card | A2A task | A2A artifacts | host decides |

>  Marco  Agente  Contacto  Compartir estado  Editor 
> Se trata de un proyecto de ley que se ha desarrollado en el campo de la salud.
> ♪ OpenAI Swarm / Agentes SDK ♪`Agent(instructions, tools)` Herramientas de regreso a la pregunta del agente                                                                                                                                                                                                                                                         
> ♬ AutoGen v0.4 / AG2 ♬`ConversableAgent`♬ Grupo de chat ♬ Ejecutor de la lista ♬ ♬ ♬ ♬ ♬ ♬ ♬ ♬ ♬ ♬ ♬ ♬ ♬ ♬ ♬ ♬ ♬ ♬ ♬ ♬ ♬ ♬ ♬ ♬ ♬ ♬ ♬ ♬ ♬ ♬ ♬ ♬ ♬ ♬ ♬ ♬ ♬ ♬ ♬ ♬ ♬ ♬ ♬ ♬ ♬ ♬ ♬ ♬ ♬ ♬ ♬ ♬ ♬ ♬ ♬ ♬ ♬ ♬ ♬ ♬ ♬ ♬ ♬ ♬ ♬ ♬ ♬ ♬ ♬ ♬ ♬ ♬ ♬ ♬ ♬ ♬ ♬ ♬ ♬ ♬ ♬ ♬ ♬ ♬ ♬ ♬ ♬ ♬ ♬ ♬ ♬ ♬ ♬ ♬ ♬ ♬ ♬ ♬ ♬ ♬ ♬ ♬ ♬ ♬ ♬ ♬ ♬ ♬ ♬ ♬ ♬ ♬ ♬ ♬ ♬  ♬  ♬   ♬ ♬     ♬     ♬       ♬                                                                                                                                                                                                                                          
> # El equipo de la tripulación #`Agent(role, goal, backstory)`¿ Qué es eso ?`Process.Sequential / Hierarchical`♬ tareas de producción en cadena ♬ gerente LLM o orden estático ♬
> # LangGraph # Función de punto #`StateGraph`¿Qué es eso?
> ♬ Microsoft Agent Framework ♬ agente ♬ + modelo de edición ♬ modelo específico ♬ ♬ ♬ ♬ ♬ ♬ ♬ ♬ ♬ ♬ ♬ ♬ ♬ ♬ ♬ ♬ ♬ ♬ ♬ ♬ ♬ ♬ ♬ ♬ ♬ ♬ ♬ ♬ ♬ ♬ ♬ ♬ ♬ ♬ ♬ ♬ ♬ ♬ ♬ ♬ ♬ ♬ ♬ ♬ ♬ ♬ ♬ ♬ ♬ ♬ ♬ ♬ ♬ ♬ ♬ ♬ ♬ ♬ ♬ ♬ ♬ ♬ ♬ ♬ ♬ ♬ ♬ ♬ ♬ ♬ ♬ ♬ ♬ ♬ ♬ ♬ ♬ ♬ ♬ ♬ ♬ ♬ ♬  ♬   ♬   ♬                                                                                                                                                                                                                                                                                                                           
>  Google ADK  agente + tarjeta A2A  A2A misión  A2A trabajo 

Las diferencias superficiales son enormes, debajo de ellos, los mismos cuatro botones.

> La diferencia de superficie parece muy grande.

### ¿Por qué esto importa?

Una vez que veas las primitivas, la comparación de marcos se convierte en una lista de verificación corta:

> Una vez que ves el lenguaje original, el marco comparativo se convierte en una lista de verificación breve:

- ¿Confia el orquestrador en que el LLM en el enrutamiento (Swarm) o en que el enrutamiento se enmarque en código (LangGraph)?
  ¿Es el programa de la LLM en el que se encuentra el programa de la LLM?
- ¿Es el estado compartido de historia completa (GroupChat) o proyectado (Reductor de gráfico de estado)?
  China: ¿Estado compartido es historia completa? ¿Grupo de chat o proyección?
- ¿Pueden los agentes modificar las instrucciones de los demás (administrador de CrewAI) o sólo entregar (Swarm)?
  En inglés, "Agentas pueden cambiar las ideas de los demás" (CrewAI) o "Swarm"?

Estas tres preguntas responden al 80% de cuál marco se adapta a un problema dado. Dejas de comprar "el mejor marco multi-agente" y empiezas a diseñar para el eje que realmente te importa.

> Estas tres preguntas respondieron al 80% de cuál marco se adapta a un determinado problema.

Cuando un nuevo marco se lance en 2027, ejecuta las tres preguntas en él. Si sus respuestas coinciden con un marco que ya usa, omita la migración. Si difieren en un eje que te importa, evalúa. La mayoría de los nuevos marcos son reempaquetado, no innovación.

> Cuando se publique el nuevo marco de 2027 , se plantean estos tres problemas para su funcionamiento. Si la respuesta coincide con el marco que ya usaste, salta a la migración. Si no se componen en el eje que te preocupa, evalúa. La mayoría de los nuevos frameworks son reempaquetados, no innovadores.

### El insight sin estado

Cada primitivo excepto el estado compartido es estatal. El agente es una función de (prompto, herramientas).**The only stateful thing in the system is shared state.**Ahí viven todos los interesantes errores: envenenamiento de la memoria (lección 15), ordenamiento de mensajes, versioning, discusión de escritura.

> Además del estado compartido, cada idioma original es inestatal.**系统中唯一有状态的东西是共享状态。**Aquí está todo el problema interesante que se encuentra: la contaminación de la memoria.

Esta visión impulsa la estrategia de depuración: cuando un sistema multiagente se comporta mal, primero vea el estado compartido. ¿Está el grupo de mensajes envenenado? ¿Están los escritos ordenados correctamente? ¿Se respeta el esquema?

> Esta estrategia de control es: Cuando muchos agentes del sistema se comportan de manera inusual, primero revise el estado de distribución.

Los marcos que ocultan el estado compartido (Swarm) empujan el problema al llamador.

> 藏藏共享状态的框架(Swarm) hará que el problema se presente al usuario.

### Anatomía de una sola primitiva

#### Agente , ¿ qué ?

```
Agent = (system_prompt, tools, model, optional_name)
```

No hay memoria, no hay estado, dos agentes con el mismo sistema de instrucción y herramientas son intercambiables, todo lo que parece un estado de agente es en realidad en estado compartido o el protocolo de transmisión.

> 没有记忆――没有状态――具有相同系统提示和工具的两个代理是可互换的――看起来就像每个代理状态的一切实际上都在共享状态或交互协议中――

Esto es contrario a la intuición pero poderoso: los agentes apátridas son triviales paralelables, reiniciables y intercambiables. Puedes hacer 100 copias del mismo agente y todos se comportan de manera idéntica.

> Esto es contrario a la intuición pero fuerte: Agente sin estado puede fácilmente ser combinado, reiniciado y sustituido. Puedes iniciar 100 copias del mismo Agente, y su comportamiento es completamente el mismo.

#### Entrega de dinero

```
Handoff = (from_agent, to_agent, reason, payload)
```

Las tres implementaciones son dominantes:

> Tres tipos de logros:

- **Function return** la herramienta devuelve el siguiente agente. Este es el patrón de OpenAI Swarm. Los agentes llevan el enrutamiento en sus esquemas de herramientas.
  En inglés:**函数返回** 工具返回下一个 Agent──这是 OpenAI Swarm's model──Agent lleva el camino en su modelo de herramientas──
- **Graph edge** LangGraph. Los bordes son declarativos. El LLM produce un valor; una condición selecciona el siguiente nodo.
  En inglés:**图边** LangGraph──边是声明式的──LLM 产生一个值;条件选择下一个节点──
- **Speaker selection**Una función selectora (a veces en sí misma una llamada de LLM) lee el grupo y elige quién habla después.
  En inglés:**发言者选择** AutoGen GroupChat。 seleccionador de funciones

#### Estado compartido

```
SharedState = { messages: [], artifacts: {}, context: {} }
```

A menudo más: artefactos estructurados (salidas de tareas de CrewAI), contexto tipado (reducidores de LangGraph), memoria externa (MCP, vector DB).

> Al menos una lista de mensajes. Usualmente más: estructural de la obra.

La forma del estado compartido determina qué tipos de coordinación son posibles. Una lista plana de mensajes hace que la transmisión sea fácil pero el filtrado específico de función sea difícil. Un esquema tipado hace que el filtrado sea trivial pero requiere un diseño previo. No hay almuerzo gratis.

> La forma del estado compartido determina qué tipo de coordinación es posible. La lista de mensajes en línea hace que la difusión sea fácil pero el papel es difícil.

Dos topologías: **full pool**(todo agente ve cada mensaje) y **projected**Los grupos completos son simples y escalar mal. los grupos proyectados escalar pero requieren un diseño de esquema anticipado.

> 两种拓:**完整池**(cada agente 看到每条消息) y**投影**(Agencia ver la visión del alcance del papel) ◊ Completa cuadro simple pero amplificador diferencias ◊ proyección cuadro ampliable pero necesita modelo de diseño previo ◊

#### Orquestación

```
Orchestrator = ({state, last_speaker}) -> next_agent
```

Cuatro sabores:

> Cuatro tipos:

- **Static** el gráfico se fija en el tiempo de construcción (determinista de LangGraph, secuencial CrewAI).
  En inglés:**静态** 图在构建时固定(Langgraph 确定性、CrewAI Sequencia)
- **LLM-selected** un LLM lee la piscina y elige al siguiente orador (AutoGen, CrewAI Hierarquial).
  En inglés:**LLM 选择** LLM 读取池并选择下一个发言人(AutoGen、CrewAI Jerárquico) 』
- **Handoff-driven** el agente actual decide llamando a una herramienta de entrega (Swarm).
  En inglés:**交接驱动** 当前 Agente 通过调用交接工具决定(Carajo) ⋅
- **Queue-driven** los trabajadores se tiran de una cola compartida; no hay altavoz siguiente explícito (arquitecturas de enjambres, Matrix).
  En inglés:**队列驱动** 工作器 de la línea de trabajo compartida; no está claro

### ¿Qué cambios se producen entre los marcos

Una vez que las primitivas se fijan, las decisiones de diseño restantes son:

> Una vez que el lenguaje original se fija, el resto de decisiones de diseño son:

- **Memory strategy** Control efímero frente a control duradero (checkpointer LangGraph).
  En inglés:**内存策略** 临时 vs 持久检查点 (punto de control de la longitud del gráfico)
- **Safety boundary** que puede aprobar una entrega (humano en el circuito).
  En inglés:**安全边界** 谁可以批准交接 (¿Quién puede ratificar un contacto?)
- **Cost accounting** Presupuestos de tokens por agente.
  En inglés:**成本核算** El presupuesto de cada agente.
- **Observability** rastrear las entregas, persistir en el estado para repetición.
  En inglés:**可观测性** Seguir en contacto  Perpetuado estado para devolver

Todos implementados en la parte superior de los primitivos. ninguno de ellos son nuevos primitivos.

> Todo puede realizarse en el original.

Cuando un framework anuncia una característica "nueva" (humano en el circuito, retraye, presupuesto de tokens), compruebe si realmente introduce una nueva primitiva o simplemente compone las cuatro. Casi siempre la última. Las cuatro primitivas son estables; todo lo demás es composición.

> Cuando el marco propaga la función "nueva" (la persona lo hace en ciclo, reutiliza, toma el presupuesto), comprueba si realmente introdujo o simplemente ha combinado estos cuatro idiomas.

## Construye y realiza.
```figure
a5-primitive-radar
```

## Construye el mismo

`code/main.py`Implementa las cuatro primitivas en ~ 150 líneas de stdlib Python.

> `code/main.py`Con aproximadamente 150 páginas de Python                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                       

El expediente exporta:

> 文件导出:

- `Agent` una clase de datos de nombre, orden del sistema, herramientas, función de política.
  En inglés:`Agent` 名称、系统提示、工具、策略函数的数据类──
- `Handoff` una función que devuelve un nuevo agente.
  En inglés:`Handoff` 返回新代理的函数──
- `SharedState` un grupo de mensajes seguro de hilo.
  En inglés:`SharedState` 线程安全的消息池──
- `Orchestrator` tres variantes: `StaticOrchestrator`¿ Qué ?`HandoffOrchestrator`¿ Qué ?`LLMSelectorOrchestrator`(simulado).
  En inglés:`Orchestrator` 三种变体:`StaticOrchestrator`¿Qué es esto?`HandoffOrchestrator`¿Qué es esto?`LLMSelectorOrchestrator`(模拟)

La demostración ejecuta la misma línea de tres agentes (investigación -> escritura -> revisión) a través de los tres tipos de orquesta y imprime el conjunto de mensajes al final.

> 演示通过所有三种编排器类型运行相同三 Agent 流水线(研究 -> 编写 -> 审阅), y finalmente imprimir消息池── puedes ver la salida sólo en* quién seleccionó el siguiente* en diferentes;Agent 和共享状态在所有运行中是相同──

- ¿Qué quieres decir ?

```
python3 code/main.py
```

La ejecución dirigida por la entrega llega a menos agentes si el investigador decide que se hace temprano  que es el tradeoff de enrutamiento LLM en miniatura.

> 预期输出: tres veces editador de operaciones, cada modelo una vez.  Cada edición de la información final.  Si el investigador decide previamente completar, el funcionamiento de la comunicación se refiere a menos agentes.

## Usalo con el marco de ejecución

`outputs/skill-primitive-mapper.md`es una habilidad que lee cualquier base de código multi-agente o documento marco y devuelve el mapeo de cuatro primitivos. ejecutarlo en una nueva versión de marco para obtener una comprensión de un párrafo antes de leer documentos en profundidad.

> `outputs/skill-primitive-mapper.md`Es una habilidad, leer cualquier otro código de agente o archivo de marco y volver a cuatro lenguajes originales.

## Envíe el producto .

Antes de adoptar un nuevo marco, escriba el mapa primitivo para él. Si no puede, los documentos son incompletos o el marco está inventando un quinto primitivo (que se verifique raramente  para un sabor de estado compartido que no ha visto).

> Antes de adoptar un nuevo marco, escriba un mapa de lenguaje original. Si no lo hace, indique que el archivo no está completo o que el marco está desarrollando un quinto marco de lenguaje original.

Enfilar el mapeo en su documento de arquitectura. Cuando un nuevo miembro del equipo se une, envíe el mapeo antes de los documentos de la API. Cuando las versiones del marco cambian, difir el mapeo, no el registro de cambios.

> Cuando un miembro del equipo nuevo se une, envía una asignación antes de la API. Cuando la versión del marco cambia, compara la asignación, en lugar de cambiar el día.

## Los ejercicios.

1. - ¿ Qué ?`code/main.py`Observe cómo el orquestaje cambia la elección de los agentes.
   En español: con diferentes agentes`code/main.py`Tres veces. Observar cómo el editor selecciona cómo cambia el funcionamiento del agente.
2. Implemente un cuarto tipo de orquesta: uno dirigido por fila donde los agentes encuestan el estado compartido para el trabajo. ¿Qué estancamiento puede ocurrir, y cómo lo detecta?
   En inglés, el programa de trabajo de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de las organizaciones de la organización de las organizaciones de las organizaciones de las organizaciones de las organizaciones de las organizaciones de las organizaciones de las organizaciones de organizaciones de organizaciones de organizaciones de organizaciones de organizaciones de organizaciones de organizaciones de organizaciones de organizaciones de organizaciones de organizaciones de organizaciones de organizaciones de organizaciones de organizaciones de organizaciones de organizaciones de organizaciones de organizaciones
3. Tomemos el inicio rápido de LangGraph y lo reescribimos como las cuatro primitivas. ¿Cuál de los mapas de abstracciones de LangGraph 1:1 y cuáles son los envoltorios de conveniencia?
   ¿Qué es el lenguaje original de LangGraph? ¿Qué es el lenguaje original de LangGraph?
4. Lea el libro de cocina OpenAI Swarm. Identifique cuál de las cuatro primitivas Swarm hace más ergonómico, y cuál empuja al que llama.
   En la lengua inglesa, el nombre de la palabra "swarm" se refiere a un grupo de palabras que se utiliza en la lengua inglesa.
5. Encuentra un marco en esta tabla que oculte el estado compartido por completo y explique qué se rompe cuando los agentes necesitan coordinar entre las entregas sin volver a leer el historial.
   Traducción:En el cuadro se encuentra un marco de estado compartido completamente oculto. Explicación: ¿Qué problemas surgen cuando un agente necesita coordinarse en un contexto de no re-lectura de la historia?

## Términos clave .

| Term | What people say | What it actually means |
|------|----------------|------------------------|
| Agent | "An LLM with tools" / "带工具的 LLM" | A `(system_prompt, tools, model)` triple. Stateless. / 一个 `(system_prompt, tools, model)` 三元组。无状态。 |
| Handoff / 交接 | "Transfer of control" / "控制转移" | A structured call that names the next agent and optional payload. Three implementations: function return, graph edge, speaker selection. / 命名下一个 Agent 和可选有效载荷的结构化调用。三种实现：函数返回、图边、发言者选择。 |
| Shared state / 共享状态 | "Memory" / "context" / "内存" / "上下文" | The only stateful part of a multi-agent system. Message pool or blackboard. / 多 Agent 系统中唯一有状态的部分。消息池或黑板。 |
| Orchestrator / 编排器 | "Coordinator" / "协调器" | Whoever decides who runs next. Static graph, LLM selector, handoff-driven, or queue-driven. / 决定谁下一个运行的角色。静态图、LLM 选择器、交接驱动或队列驱动。 |
| Primitive / 原语 | "Abstraction" / "抽象" | One of the four axes every framework parameterizes. Not a framework feature. / 每个框架参数化的四个轴之一。不是框架特性。 |
| Message pool / 消息池 | "Shared chat history" / "共享聊天历史" | Full-history shared state. Easy to reason about, scales badly. / 完整历史共享状态。易于推理，扩展性差。 |
| Projected state / 投影状态 | "Scoped view" / "范围视图" | Role-specific view into shared state. Scales, requires schema design. / 角色特定的共享状态视图。可扩展，需要模式设计。 |
| Speaker selection / 发言者选择 | "Who talks next" / "谁下一个说话" | Orchestrator pattern where a function (often an LLM) picks the next agent from a group. / 编排器模式，函数（通常是 LLM）从组中选择下一个 Agent。 |

## Más Leer más Leer más

- [OpenAI cookbook: Orchestrating Agents — Routines and Handoffs](https://developers.openai.com/cookbook/examples/orchestrating_agents) la articulación más clara de la orquestación impulsada por la entrega
   Ejemplo y relación  交接驱动编排的最清晰阐述
- [AutoGen stable docs](https://microsoft.github.io/autogen/stable/) GroupChat + selección de oradores es la referencia para la orquestación seleccionada por el LLM
  中文翻译:AutoGen 稳定文档  GroupChat + 发言人选择是 LLM 选择编排的参考
- [LangGraph workflows and agents](https://docs.langchain.com/oss/python/langgraph/workflows-agents) Orquestación de borde gráfico y estado compartido basado en reducidor
   图边编排和基于归约器的共享状态 中文翻译:LangGraph 工作流和 Agent  图边编排和基于归约器的共享状态
- [CrewAI introduction](https://docs.crewai.com/en/introduction) agentes de rol-objetivo-historia de fondo, procesos secuenciales / jerárquicos
  Centro de trabajo de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de las organizaciones de las organizaciones de las organizaciones de las organizaciones de organizaciones de las organizaciones de organizaciones de organizaciones de organizaciones de organizaciones de organizaciones de organizaciones de organizaciones de organizaciones de organizaciones de organizaciones de organizaciones de organizaciones de organizaciones de organizaciones de organizaciones de organizaciones de organizaciones de organizaciones de organizaciones de organizaciones de organizaciones de organizaciones de organizaciones de organizaciones de organizaciones de organizaciones de organizaciones de organizaciones de organizaciones de organizaciones de organizaciones de organizaciones de organizaciones de organizaciones de organizaciones de organizaciones de organizaciones de organizaciones de organizaciones de organizaciones de organizaciones de organizaciones de organizaciones de organizaciones de organizaciones de organizaciones de organizaciones de organizaciones de organizaciones de organizaciones de organizaciones de organizaciones de organizaciones de organizaciones de organizaciones de organizaciones de organizaciones de organizaciones de organizaciones de organizaciones de organizaciones de organizaciones de organizaciones de organizaciones de organizaciones de organizaciones de
- [AG2 (community AutoGen continuation)](https://github.com/ag2ai/ag2) la línea de AutoGen v0.2 en vivo después de que Microsoft moviera v0.4 en mantenimiento
  En inglés, el nombre de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de Microsoft.
