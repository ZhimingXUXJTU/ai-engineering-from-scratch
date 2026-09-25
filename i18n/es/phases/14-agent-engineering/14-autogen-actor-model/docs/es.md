# AutoGen v0.4: Modelo de actor y marco de agente
# El modelo de actor para agentes  Mensajes sincronizados y tiempos de ejecución de tipo

> Agentes como actores: intercambio de mensajes asíncronos, manipuladores de eventos, aislamiento de fallos, concurrencia natural. AutoGen v0.4 (Microsoft Research, enero 2025) rediseñó la orquestación de agentes alrededor de este modelo; el marco está ahora en modo de mantenimiento, con Microsoft Agent Framework (previsión pública de octubre 2025) como su sucesor de producción.

> **【中文解读】**AutoGen v0.4 (Microsoft Research Center, enero de 2025) Redesignó el modelo de Actor en torno a Agent 编排, eventos impulsores, agentes, fallas, aislamientos, naturales, y otros factores.

**Type:** Learn + Build | **类型:** 学习 + 构建
**Languages:** Python (stdlib) | **语言:** Python (标准库)
**Prerequisites:** Phase 14 · 01 (Agent Loop), Phase 14 · 12 (Workflow Patterns) | **前置知识:** Phase 14 · 01 (Agent 循环), Phase 14 · 12 (工作流模式)
**Time:** ~75 minutes | **时间:** ~75 分钟

## Objetivos de aprendizaje

- Describa el modelo de actores: agentes como actores, mensajes como el único IPC, aislamiento de fracasos por actor.
  En el texto original, el actor es el único actor en el mundo.
- Nombre de las tres capas de API de AutoGen v0.4  Core, AgentChat, Extensions  y para qué es cada uno.
  China Translation: decir fuera de las tres API de AutoGen v0.4 Core、AgentChat、Extensiones及 su uso propio
- Explica por qué la desacoplamiento de la transmisión de mensajes de la manipulación da aislamiento de fallas y concurrencia natural.
  Traducción:Explanar por qué el mensaje de transmisión con el entendimiento puede traer fallas aislamiento y el desarrollo natural.
- Implemente un tiempo de ejecución de actor stdlib en Python y puesta un flujo de revisión de código de dos agentes en él.
  En español: Python 标准库实现 Actor 运行时并将双 Agent 代码审查流程移植到其上──

## El problema es la introducción del problema

La mayoría de los marcos de agentes son sincrónicos: un agente produce, un agente consume, en una pila de llamadas. Los fallos chocan la pila. La concurrencia está activada. La distribución requiere reescribir.

> La mayoría de los agentes  marco es sincronizado: un agente produce, un agente consume, en el tiempo de uso , el fracaso hace que  colaps, el desarrollo es posterior , la necesidad de reescribir distribuida .

AutoGen v0.4 respuesta: el modelo de actor. Cada agente es un actor con una bandeja de entrada privada. Los mensajes son la única interacción. El tiempo de ejecución desacopla la entrega del manejo. Los fracasos se aislan a un actor. La competencia es nativa. La distribución es sólo un transporte diferente.

> AutoGen v0.4 respuesta:Actor 模型── cada agente es un actor con caja de recepción privada──消息是唯一交互方式──运行时将交付与处理解──失败隔离到一个 Actor──并发是原生──分布式只是不同的传输方式──

> **【中文解读】**AutoGen v0.4  Adopta Actor 模型 Cada agente es un actor independiente, a través de mensajes de transmisión. Esto es diferente del modelo gráfico de LangGraph o el modelo de papel de CrewAI.

> **【拓展：AutoGen 的演进】**AutoGen fue desarrollado por Microsoft Research Institute, v0.4 (2025) fue una de las principales redes construcciones. De la versión 0.3 del modelo de diálogo se transfiere al modelo de actores, inspirado en el modelo de aparición de Erlang/Akka. El concepto central es que cada agente es un actor, tiene un estado y una línea de mensajes independientes, a través de un proceso de transmisión de mensajes. Esto hace que AutoGen sea especialmente adecuado para múltiples agentes en la distribución de escenarios.

> ¿ Qué es esto ?**【前置】**必须先掌握:Phase 14·01(Agent Loop) yPhase 14·12(Antropic Workflow Patterns) 本节是这些模式在"并发场景"下延伸──还需要"Actor 模型"的基本概念如果不知道Erlang/Akka是什么,先去补一节分布式系统课──本节硬核在"异步消息传递"而不是"LLM 调用"──

## El concepto central.

### Actores

Un actor tiene:

> Un actor tiene:

- Un estado privado (nunca tocado directamente desde fuera).
  En el caso de los países de la región de la Unión Soviética, el gobierno de la República de China no ha permitido que los países de la región de la Unión Soviética no tengan relaciones con los demás países.
- Una bandeja de entrada (cuadra de mensajes).
  En el caso de los que se encuentran en el centro de la ciudad, el número de personas que se encuentran en el centro de la ciudad es el número de personas que se encuentran en el centro de la ciudad.
- Un manipulador:`receive(message) -> effects`donde los efectos pueden ser "responda", "envía a otro actor", "españar un nuevo actor", "actualizar estado", "detenerse".
  En inglés:`receive(message) -> effects`, el efecto puede ser "回复""",enviar a otros actores"",crear un nuevo actor"",actualizar el estado""",stop yourself"

Dos actores no pueden compartir memoria, sólo pueden enviar mensajes.

> ¿ Qué es esto ?**【类比】**Actor 模型像办公室里互相见的同事: cada uno tiene su propio trabajo (privé status) y caja de correos (receive box) 消息队列) ⋅你想让同事帮忙,不能直接翻翻他的工位 (共享内存),只能发邮件 (发消息) ⋅同事处理完邮件可能回信 (回复) ⋅转发给另一个人 (发送给另一个人) ⋅招生 (招生) ⋅发新演员 (发演员) ⋅**关键**Un compañero de trabajo no afecta a los demás.

> Dos actores no pueden compartir su memoria. Sólo pueden enviar mensajes.

### Tres capas de API en AutoGen v0.4
### Tres capas de API

AutoGen v0.4 divide su superficie en tres:

1. **Core.**Marco de actores de bajo nivel. `AgentRuntime`¿ Qué ?`Agent`¿ Qué ?`Message`¿ Qué ?`Topic`- Intercambio de mensajes sincronizados, basado en eventos.
   En inglés:**Core。**底层 Actor 框架──`AgentRuntime`¿Qué es esto?`Agent`¿Qué es esto?`Message`¿Qué es esto?`Topic`◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊   ◊ ◊ ◊     ◊ ◊    ◊ ◊     ◊      ◊     ◊            ◊                                                                                                                                   
2. **AgentChat.**API de alto nivel dirigida a tareas (sustitución del ConversableAgent de v0.2). `AssistantAgent`¿ Qué ?`UserProxyAgent`¿ Qué ?`RoundRobinGroupChat`¿ Qué ?`SelectorGroupChat`¿ Qué ?
   En inglés:**AgentChat。**任务驱动的高级 API( sustituye la versión 0.2 de ConversableAgent)`AssistantAgent`¿Qué es esto?`UserProxyAgent`¿Qué es esto?`RoundRobinGroupChat`¿Qué es esto?`SelectorGroupChat`¿Qué es eso?
3. **Extensions.**Integraciones  OpenAI, Anthropic, Azure, herramientas, memoria.
   En inglés:**Extensions。**集成OpenAI、Antropic、Azure、工具、记忆──

### ¿Por qué es importante la separación?

En el modelo v0.2, llamando`agent_a.chat(agent_b)`bloquea sincrónicamente el agente_a hasta que el agente_b regrese.`send(agent_b, msg)`El tiempo de ejecución se entrega más tarde.

> En el modelo 0.2,调用 `agent_a.chat(agent_b)`En la versión 0.4, el agente de bloqueo regresa.`send(agent_b, msg)`Se puede enviar una información a la caja de recepción del agente y devolverla.

- **Fault isolation.**El agente B se estrella no se estrella el agente A  el tiempo de ejecución captura el fallo en el manipulador de B y decide qué hacer (log, retraye, letra muerta).
  En inglés:**故障隔离。**El agente B 崩 no causará que el agente A 崩运行时在B's处理器中捕获故障并决定做什么 (日志、重试、死信) ⋅
- **Natural concurrency.**Muchos mensajes en vuelo a la vez; los actores procesan su bandeja de entrada simultáneamente.
  En inglés:**天然并发。**Más noticias en el mismo tiempo; actor no ha enviado el procesamiento de ellas.
- **Distribution-ready.**La bandeja de entrada + transporte es la misma abstracción ya sea que el actor esté en proceso o en otro anfitrión.
  En inglés:**分布式就绪。**收件箱 + 传输 es el mismo abstracto, independientemente de que el actor esté en el proceso o en otra máquina.

> ️ **【易错点】**Usó el modelo del actor pero olvidó que la noticia debe ser procesada.**后果**El proceso de producción se distribuye hasta que muchos objetos no llegan a su objeto.**一行修复**Todos los mensajes deben utilizar pydantic/dataclass/JSON-schema definido, prohibido transmitiendo lambda、文件句柄、数据库连接等不可序列化对象──

### Topologías

- **RoundRobinGroupChat.**Los agentes se turnan en una rotación fija.
  En inglés:**RoundRobinGroupChat。**Agente 按固定轮换顺序轮流──
- **SelectorGroupChat.**Un agente seleccionador elige quién va a seguir en función del contexto de la conversación.
  En inglés:**SelectorGroupChat。**选择器 Agente 根据对话上下文选择下一个发言人──
- **Magentic-One.**Equipo de referencia multi-agente para navegación web, ejecución de código, manejo de archivos.
  En inglés:**Magentic-One。**Utilizado para la búsqueda de páginas web, ejecución de código, procesamiento de archivos, en referencia a más de un equipo de agentes.

### Observabilidad

Cada mensaje emite un período de tiempo; las llamadas a la herramienta llevan`gen_ai.*`Los datos de la evaluación de los datos de la evaluación de los datos de la evaluación de los datos de la evaluación de los datos de la evaluación de los datos de la evaluación de la evaluación de los datos de la evaluación de la evaluación de los datos de la evaluación de la evaluación de la evaluación de la evaluación de los datos de la evaluación de la evaluación de la evaluación de la evaluación de la evaluación de los datos de la evaluación de la evaluación de la evaluación de la evaluación de la evaluación de la evaluación de la evaluación de la evaluación de la evaluación de la evaluación de la evaluación de los datos de la evaluación de la evaluación de la evaluación de la evaluación de la evaluación de la evaluación de la evaluación de la evaluación de la evaluación de la evaluación de la evaluación de la evaluación de la evaluación de la evaluación de la evaluación de la evaluación de la evaluación de la evaluación de la evaluación de la evaluación de la evaluación de la evaluación de la evaluación de la evaluación de la evaluación de la evaluación de la evaluación de la evaluación de la evaluación de la evaluación de la evaluación de la evaluación de la evaluación de la evaluación de la evaluación de la evaluación de la evaluación de la evaluación de la evaluación de la evaluación de la evaluación de la evaluación de la evaluación de la evaluación de la evaluación de la evaluación de la evaluación de la evaluación de la evaluación de la evaluación de la evaluación de la evaluación de la evaluación de la evaluación de la evaluación de la evaluación de la evaluación de la evaluación de la evaluación de la evaluación de la evaluación de la evaluación de la evaluación de la evaluación de la evaluación de la evaluación de la evaluación de la evaluación de la evaluación de la evaluación de la evaluación de la evaluación de la evaluación de la evaluación de la evaluación de la evaluación de la evaluación de la evaluación de la evaluación de la evaluación de la evaluación de la evaluación de la evaluación de la evaluación de la evaluación de la evaluación de la evaluación de la evaluación de la evaluación de la evaluación de la evaluación de la evaluación de la evaluación de la evaluación de la evaluación de la evaluación de la evaluación de la evaluación de la evaluación de la evaluación de la evaluación de la evaluación de la evaluación de la evaluación de la evaluación de la evaluación de la evaluación de la evaluación de la evaluación de la evaluación de la evaluación de la evaluación de la evaluación de la evaluación de la evaluación de la evaluación de la cuento de la evaluación de la evaluación de la evaluación de la evaluación de la cuento de la cuento de la evaluación de la cuento de la cuento de la cuento de la evaluación de

> OpenTelemetry 支持内置──每条消息发发出一个跨度;工具调用携带 `gen_ai.*`属性, conforme a 2026 años OTel GenAI 语义约定(第 23 课)

### Estado: modo de mantenimiento

Inicio 2026: AutoGen v0.7.x es estable para la investigación y la creación de prototipos. Microsoft ha cambiado el desarrollo activo al Microsoft Agent Framework, el sucesor de producción (previsión pública 1 de octubre de 2025; 1.0 GA fue dirigido a finales del primer trimestre de 2026).

```figure
actor-mailbox
```

> ¿ Qué es esto ?**【困惑】**P: AutoGen  ha entrado en el modelo de mantenimiento, ¿qué debo aprender?**别在生产上选 AutoGen**△原因:(1) 微软 ha pasado a Microsoft Agent Framework(MAF),AutoGen no vuelve a obtener nuevas características;(2) Actor 模型 mismo es个**经久不衰的分布式设计思想**(desde el 1973 en Hewitt 论文,比 LLM 老 50年), entender que es para evaluar MAF、Erlang、Akka、Ray tienen ayuda.

> Inicio del año 2026: AutoGen v0.7.x en el aspecto de la investigación y desarrollo del modelo original está estable. Microsoft ha transferido el desarrollo activo al Microsoft Agent Framework.

## Construye con movimiento.

`code/main.py`Implementa un tiempo de ejecución de actores stdlib:

> `code/main.py`Usándándarcu realizó Actor 运行时:

- `Message` carga útil tipografada con `sender`¿ Qué ?`recipient`¿ Qué ?`topic`¿ Qué ?`body`¿ Qué ?
  En inglés:`Message`带 `sender`¿Qué es esto?`recipient`¿Qué es esto?`topic`¿Qué es esto?`body`La carga de la carga
- `Actor` abstracto con `receive(message, runtime)`¿ Qué ?
  En inglés:`Actor`带 `receive(message, runtime)`De los tipos de abstracciones.
- `Runtime` bucle de eventos con una cola compartida, entrega, aislamiento de fallas.
  En inglés:`Runtime`带共享队列、投递、故障隔离的事件循环──
- Una demostración de dos actores:`ReviewerAgent`código de revisión, `ChecklistAgent`ejecuta una lista de verificación; intercambian mensajes hasta el consenso.
  En español: actor`ReviewerAgent`审查代码,`ChecklistAgent`运行检查清单; intercambian noticias hasta alcanzar el acuerdo.

- ¿Qué quieres decir ?

> 运行:

```
python3 code/main.py
```

El rastro muestra la entrega del mensaje, un fracaso simulado en un actor que no estrella al otro, y convergencia en un veredicto compartido.

> 轨迹显示消息投递、 un fallo de un actor no conducirá a otro colapso, así como a la recepción de la decisión compartida ──

## Usalo con el marco de ejecución

- **AutoGen v0.4/v0.7**(Mantenimiento)  estable para la investigación, prototipos, patrones multi-agentes.
  En inglés:**AutoGen v0.4/v0.7**(维护中) 研究、原型、多 Agent 模式稳定──
- **Microsoft Agent Framework**(previsión pública)  el camino hacia adelante; las mismas ideas de actores-modelo en una API actualizada.
  En inglés:**Microsoft Agent Framework**(公开预览) 前进方向; en la actualización de la API en el mismo Actor 模型理念.
- **Microsoft Agent Framework** el sucesor de producción (previsión pública de octubre de 2025); las mismas ideas de actores-modelo en una API actualizada.
- **LangGraph swarm topology**(Lección 13)  patrón similar a través de las entregas de herramientas compartidas.
  En inglés:**LangGraph 群体拓扑**(第 13 课)                                                                                                                                                                                                                                                            
- **Custom actor runtime** cuando se necesita un transporte específico (NATS, RabbitMQ, gRPC).
  En inglés:**自定义 Actor 运行时** Cuando necesites un determinado transmisor (NATS, RabbitMQ, GRPC) 时

## Envíe el producto .

`outputs/skill-actor-runtime.md`genera un tiempo de ejecución mínimo de actores más una plantilla de equipo (RoundRobin o Selector) para una tarea multi-agente dada.

> `outputs/skill-actor-runtime.md`Para determinar más agentes  tareas de generación de actores 运行时加团队模板(RoundRobin o Selector) ⋅

## Los ejercicios.

1. Añadir una cola de letras muertas: cuando un manipulador levante, estacione el mensaje fallido para inspección humana. ¿Con qué frecuencia se golpea DLQ en su juguete?
   China: Add Additional Death Line: Cuando el procesador lanza una anomalía, ¿cómo es la frecuencia de que el DLQ sea detectado en tu juguete?
2. Implementación `SelectorGroupChat`: un actor selector elige quien procesa el siguiente mensaje en función del estado de conversación.
   En español:`SelectorGroupChat`: seleccionador Actor 根据对话状态选择谁处理下一条消息。
3. Añadir transporte distribuido: intercambiar la cola en proceso por un servidor JSON-over-HTTP para que los actores puedan ejecutar procesos separados.
   China: Additional Distributed Transfer: se sustituirá la línea de comandos del proceso en JSON-over-HTTP  servidor, para que el Actor pueda funcionar en un proceso independiente.
4. Envía un tiempo de OTel por mensaje (o un no-op stand-in).`gen_ai.agent.name`¿ Qué ?`gen_ai.operation.name`Por lección 23.
   Por ejemplo, el texto de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de los Estados de los Estados Unidos.`gen_ai.agent.name`¿Qué es esto?`gen_ai.operation.name`¿Qué es eso?
5. Lea el post de arquitectura de AutoGen v0.4.`autogen_core`¿Qué se ha saltado que importa en la producción?
   China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China:`autogen_core`¿Qué es lo que saltaste de lo importante en la producción?

## Términos clave .

| Term | What people say | What it actually means |
|------|-----------------|-----------------------|
| 术语 | 通俗说法 | 实际含义 |
| Actor | "Agent" / "Agent" | Private state + inbox + handler; no shared memory / 私有状态 + 收件箱 + 处理器；无共享内存 |
| Message | "Event" / "事件" | Typed payload; the only way actors interact / 带类型载荷；Actor 唯一的交互方式 |
| Inbox | "Mailbox" / "邮箱" | Per-actor queue of pending messages / 每个 Actor 的待处理消息队列 |
| Runtime | "Agent host" / "Agent 宿主" | Event loop that routes messages and isolates failures / 路由消息和隔离故障的事件循环 |
| Topic | "Channel" / "通道" | Named publish-subscribe route between actors / Actor 之间的命名发布-订阅路由 |
| Fault isolation | "Let it crash" / "让它崩溃" | One actor failing does not crash others / 一个 Actor 失败不会导致其他崩溃 |
| RoundRobinGroupChat | "Fixed-rotation team" / "固定轮换团队" | Agents take turns in order / Agent 按顺序轮流 |
| SelectorGroupChat | "Context-routed team" / "上下文路由团队" | Selector picks who goes next / 选择器选择下一个发言者 |
| Magentic-One | "Reference team" / "参考团队" | Multi-agent squad for web + code + files / 用于网页+代码+文件的多 Agent 小队 |

## Más Leer más Leer más

- [AutoGen v0.4, Microsoft Research](https://www.microsoft.com/en-us/research/articles/autogen-v0-4-reimagining-the-foundation-of-agentic-ai-for-scale-extensibility-and-robustness/) el puesto de rediseño
  En el caso de los modelos de diseño de la máquina, el diseño de la máquina de diseño de la máquina de diseño de la máquina es el mismo.
- [LangGraph overview](https://docs.langchain.com/oss/python/langgraph/overview) Alternativa en forma de gráfico
  La historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la China.
- [OpenTelemetry GenAI semantic conventions](https://opentelemetry.io/docs/specs/semconv/gen-ai/) se extiende AutoGen emite por defecto
  中文翻译:OpenTelemetry GenAI 语义约定AutoGen 默认发射跨度──
