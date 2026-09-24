# Entrega y rutina Orquestación sin estatus

> OpenAI's Swarm (octubre 2024) destilado multi-agente orquestación a dos primitivos: **routines**(instrucciones + herramientas como un mensaje de sistema) y **handoffs**(una herramienta que devuelve a otro agente). No hay máquina estatal, no hay ramas de DSL  las rutas de LLM llamando a la herramienta de entrega correcta. El SDK OpenAI Agents (marzo 2025) es el sucesor de producción. El mismo cúmulo sigue siendo la referencia conceptual más limpia  su fuente entera encaja en unos cientos de líneas. El patrón es viral porque la superficie de la API es aproximadamente "agente = prompt + herramientas; entrega = agente de devolución de funciones". Limitación: sin estado, por lo que la memoria es el problema del llamador.

> **【中文解读】**Este capítulo presenta los procesos y procedimientos estándar de control de tareas de transmisión entre agentes.

> **【拓展：handoffs and routines→具体应用】**交接(Handoffs) es el concepto central de OpenAI Agents SDKAgent A transferirá el control a Agent B。 clave decisión de diseño:(1) 上下文传递B 收到多少 A 的历史?(2) 恢复机制B 完成后控制权回到 A 还是交给 C?(3) 超时处理B 如果卡住怎么办?


**Type:** Learn + Build | **类型:** 学习 + 构建
**Languages:** Python (stdlib) | **语言:** Python (标准库)
**Prerequisites:** Phase 16 · 04 (Primitive Model) | **前置知识:** Phase 16 · 04 (原语模型)
**Time:** ~60 minutes | **时间:** ~60 分钟

> ¿ Qué es esto ?**【前置】**学本节前请先掌握:Fase 16·04(原语模型)、Fase 14·07(工具调用)。OpenAI Swarm 把多 Agent 简化为2 原语:routine(系统提示+工具)+handoff(返回另一个代理的工具)。
> ¿ Qué es esto ?**【类比】**Handoff = "客服转接"──用户问技术问题→客服 A 接听→判断需要技术支持→转接给技术专员 B。Swarm 的天才之处:handoff 就是一个普通工具调用(返回代理),LLM 自动路由──无状态机、无 DSL,几百行代码搞定──OpenAI Agents SDK 是生产版本──

## # El problema # # El problema #

Cada marco multi-agente quiere que aprendas su DSL: nodos y bordes de LangGraph, equipos y tareas de CrewAI, AutoGen GroupChat y gerentes.

> Cada multi-agente  framework quiere hacerte aprender sus DSL:Notes y bordes de LongGraph Equipo y tareas de CrewAI  Grupo de AutoGen  Chat y administrador  DSL es un verdadero abstracto, pero hacen que las cosas se sientan más pesadas que las necesidades reales 

Los sistemas de bloqueo DSL son los sistemas de bloqueo multiagente. Cada DSL tiene sus propios conceptos, sus propias herramientas de descomposición, su propia comunidad. Una vez que se compromete, la migración es costosa.

> DSL 锁定是多代理 框架税── cada DSL tiene su propio concepto、 su propio instrumento de调试、 su propia comunidad── una vez que usted se compromete, se migra caro── Swarm's 注: completamente saltó DSL, usando los modelos existentes para utilizar los instrumentos de调用──

El grupo empuja en la dirección opuesta: utiliza la capacidad de llamada de herramientas que el modelo ya tiene. Las entregas se convierten en llamadas de herramientas. El orquestrador es el agente que actualmente sostiene la conversación. La máquina de estado está implícita en las instrucciones del sistema de los agentes.

> Swarm 推向相反的方向: utilizar el modelo de herramientas ya existentes capacidad de调用――交接变成工具调用――编排器就是当前持有对话的代理――状态机隐含在代理的系统提示中.

La visión es profunda: no se necesita una DSL de orquestación porque los LLM ya son orquestación.

> 洞察深: 你不需要编排 DSL,因为 LLM 已经是编排器──每次LLM 调用根据上下文决定下一步做什么──交接只是将该决策暴露为模型可调用工具──

## Concepto de la esencia de la concepción

### Dos primitivos

**Routine.**Un sistema de instrucciones que define el papel de un agente y las herramientas disponibles. Piense en ello como un conjunto de instrucciones con un alcance: "es un agente de triaje; si el usuario pregunta sobre reembolsos, entregue a la agente de reembolso".

> **例程。**definición de agente 角色和可用工具的系统提示──把它想象成一组范围化的命令:" eres un agente de diagnóstico; si el usuario pregunta por el reembolso, entre en contacto con el agente de reembolso──"

**Handoff.**Una herramienta que el agente puede llamar que devuelve un nuevo objeto de agente.

> **交接。**Agente puede ser utilizado como herramienta, devolver un nuevo Agente a un objeto.

Esa es toda la abstracción.

> Es todo un abstracto.

```
def transfer_to_refunds():
    return refund_agent  # Swarm sees Agent return → switch active agent

triage_agent = Agent(
    name="triage",
    instructions="Route the user to the right specialist.",
    functions=[transfer_to_refunds, transfer_to_sales, transfer_to_support],
)
```

El sistema de la solicitud del agente de triaje le hace elegir la entrega correcta en función del mensaje del usuario.

> El sistema de instrucciones del agente de diagnóstico lo hace según la información del usuario seleccionar correctamente la comunicación.

Este es el movimiento elegante: reutilizar la infraestructura de llamadas de herramientas existente del modelo para la orquestación. No hay nuevo DSL, editor de gráficos, máquina de estado. El modelo ya sabe cómo elegir la herramienta correcta; las entregas son solo herramientas que devuelven agentes.

> Es una iniciativa de Ulia: volver a utilizar los instrumentos existentes del modelo para organizar la infraestructura. No hay nuevos DSLs, no hay editores de gráficos, no hay máquinas de estado. El modelo ya sabe cómo elegir los instrumentos correctos.

### Por qué es viral

- **Small API.**Dos conceptos que aprender.
  En inglés:**小型 API。**Sólo necesito aprender dos conceptos.
- **Uses what the model already does.**La llamada a herramientas ya es de producción entre los proveedores.
  En inglés:**使用模型已有的能力。**工具调用已在各供应商中是生产级.
- **No state-machine burden.**No describirás el gráfico, las instrucciones de los agentes describen a quiénes entregan.
  En inglés:**无状态机负担。**Usted no describe el mapa; los consejos del agente describen los que entregan a quien.

### El comercio sin estado

Swarm es explícitamente sin estado entre las ejecuciones. El marco mantiene un historial de mensajes durante una ejecución, pero no persiste nada. Memoria, continuidad, tareas de larga duración  todo el problema del llamador.

> El marco de mantenimiento de la información durante el funcionamiento, pero no perdurar nada.

El diseño sin estado es intencional: hace que el marco sea trivialmente reiniciable, escalable horizontalmente y descompone (cada ejecución es independiente).

> 无状态设计是有意的: hace que el marco pueda reiniciarse fácilmente, ampliar y regularse fácilmente, cada vez que se ejecuta independientemente, el costo es que el trabajo que se ejecuta por mucho tiempo requiere un manejo externo del estado, la base de datos, las cotaciones, los puntos de control.

En la producción (OpenAI Agents SDK, marzo 2025) esto fue una de las principales cosas que cambiaron: el SDK añade gestión de sesiones integrada, barandillas y seguimiento mientras mantiene la entrega primitiva.

> En producción ambiente (OpenAI Agents SDK, 2025 3 月), es uno de los principales cambios:SDK añadió la gestión de conversaciones en el interior, la protección y el seguimiento, mientras que se mantuvo el contacto original.

### Cuando el grupo de manadas se ajuste

- **Triage patterns.**El agente de primera línea envía al usuario a un especialista.
  En inglés:**分诊模式。**El agente de primera línea se dirigirá al usuario hacia el profesional.
- **Skill-based handoffs.**"Si la tarea necesita código, llame al codificador; si necesita investigación, llame al investigador".
  En inglés:**基于技能的交接。**"Si las tareas necesitan codificación, utilizar el codificador; si necesitan investigación, usar el investigador"".
- **Short, bounded conversations.**Soporte al cliente, preguntas frecuentes, flujos de trabajo simples.
  En inglés:**短、有界对话。**客户支持、FAQ 到工单、简单工作流──

### Cuando el enjambre lucha

- **Long sessions with shared memory.**Las transferencias restablecen el estado de conversación al nuevo agente de la cuenta de espera más el historial.
  En inglés:**需要共享内存的长会话。**交接将对话状态重置为新代理的提示加历史―― no hay memoria de gestión de调用者, no hay estado permanente de trans-agente――
- **Parallel execution.**El cambio de mano es uno a la vez  los interruptores del agente activo. Paralelamente, el llamador requiere orquestar múltiples carreras de Swarm.
  En inglés:**并行执行。**交接是逐一的活动 交换――并行性需要调用者编排多个 Swarm 运行――
- **Audit and replay.**Las carreras sin estatus son difíciles de reproducir exactamente; la elección de entrega del LLM no es determinista.
  En inglés:**审计和回放。**无状态运行难以精确回放; La elección de los enlaces de LLM no es definitiva.

### El objetivo de la evaluación es mejorar la calidad de la información y la calidad de la información.

El sucesor de producción añade:

> El productor de producción añadió:

- **Session state.**Un hilo persistente a través de las carreras.
  En inglés:**会话状态。**跨运行的持久线程──
- **Guardrails.**Los ganchos de validación de entrada/salida.
  En inglés:**防护栏。**输入/输出验证子──
- **Tracing.**Todas las llamadas y entregas de herramientas están registradas.
  En inglés:**追踪。**Cada vez que se usan herramientas y se registra la comunicación.
- **Handoff filters.**Controlar qué contexto se transfiere en la entrega.
  En inglés:**交接过滤器。**Control de comunicación, transmisión y transmisión.

El primitivo de entrega sobrevive; la ergonomía de producción se agrega a su alrededor.

> 交接原语存活下来; producción de ingeniería humana alrededor de ella añadir

Esta es la progresión estándar para las abstracciones virales: primero los barcos primitivos simples (Swarm), la producción se refiere a la capa superior (Agents SDK).

> Este es el estándar progreso de virus式抽象:先发布简单原语(Swarm), producir preocupaciones en su nivel superior(Agentes SDK)

### Swarm vs. grupo chat

Ambos utilizan el enrutamiento impulsado por el LLM, pero difieren en**who picks next**¿Qué es esto ?

>  ambos utilizan el LLM  impulsado por el camino, pero en**谁选择下一个**上不同:

- GrupoChat: un selector (función o LLM) elige al próximo orador desde fuera.
  La lengua de la lengua se traduce en inglés como "el lenguaje de la lengua".
- El agente actual elige a su sucesor llamando a una herramienta de entrega.
  En español: "Swarm" (en inglés: Swarm)

Swarm es "el agente decide lo que viene después"; GroupChat es "el gerente decide lo que viene después". La decisión de Swarm vive en la llamada de herramientas del agente activo; la vida de GroupChat en el `GroupChatManager`¿ Qué ?

> Swarm es "El agente decide el siguiente paso"; GroupChat es "El administrador decide el siguiente paso"。La decisión del grupo se basa en el instrumento del agente de actividad; GroupChat se basa en el`GroupChatManager`En el medio.

Implicación práctica: Swarm es más fácil de deshacerse (siguiendo las llamadas de herramientas del agente activo) pero más difícil de restringir (cualquier agente puede entregarlo en cualquier lugar). GroupChat es lo contrario: fácil de restringir (la función del selector es un lugar para agregar reglas), más difícil de deshacerse (la lógica del selector puede ser opaca).

> 实际影响:Swarm 更容易调试(跟踪活动 调用的工具) pero更难约束(cualquier agente puede comunicarse en cualquier lugar) ――GroupChat 相反:容易约束(selector función es una de las reglas de la adición),更难调试(selector's logic可能不透明)。

## Construye y realiza.
```figure
sw-handoff-routing
```

## Construye el mismo

`code/main.py`Implementa Swarm desde cero: una clase de datos de agente, un mecanismo de entrega (herramienta devuelve agente) y un bucle de ejecución que detecta los interruptores de agente.

> `code/main.py`Desde la realización de la serie:Mécanismo de comunicación, de datos y de datos de los agentes (Mécanismo de comunicación, de la información y de la información de los agentes) y de la investigación de los agentes (Mécanismo de intercambio de datos y de comunicación).

Demo: un agente de triaje viaja para reembolsar, ventas o especialistas de soporte. Cada especialista tiene sus propias herramientas.

> 演示:分诊 路由到退款、销售或支持专家── cada uno de los especialistas tiene su propio instrumento──运行循环打印每次交交交──

- ¿Qué quieres decir ?

```
python3 code/main.py
```

## Usalo con el marco de ejecución

`outputs/skill-handoff-designer.md`diseña una topología de entrega para una tarea determinada: qué agentes existen, qué entregas pueden llamar, qué contextos transfieren.

> `outputs/skill-handoff-designer.md`Para determinar el diseño de la misión: ¿Qué agentes existen?, ¿qué pueden utilizar para la transmisión?

## Envíe el producto .

Lista de control:

> 检查清单:

- **Handoff logging.**Cada entrega escribe un evento de rastreo con un instantáneo de agente a agente, contexto.
  En inglés:**交接日志。**Cada contacto que se escribe en el evento de seguimiento, incluye desde el agente hasta el agente.
- **Context transfer rules.**Decida qué se mueve en la entrega: historia completa (cargada), últimos N mensajes, o un resumen.
  En inglés:**上下文传输规则。**Decide en el momento de la transmisión: historia completa, historia de la historia, historia de la historia, historia de la historia, historia de la historia, historia de la historia, historia de la historia, historia de la historia, historia de la historia, historia de la historia, historia de la historia, historia, historia, historia, historia, historia, historia, historia, historia, historia, historia, historia, historia, historia, historia, historia, historia, historia, historia, historia, historia, historia, historia, historia, historia, historia, historia, historia, historia, historia, historia, historia, historia, historia, historia, historia, historia, historia, historia, historia, historia, historia, historia, historia, historia, historia, historia, historia, historia, historia, historia, historia, historia, historia, historia, historia, historia, historia, historia, historia, historia, historia, historia, historia, historia, historia, historia, historia, etc.
- **Guardrail on handoff.**Una entrega a un especialista con diferentes permisos de herramienta debe ser autenticada  de lo contrario, la inyección rápida puede forzar las entregas no deseadas.
  En inglés:**交接防护栏。**交接到具有不同工具权限的专家必须得到认证否则提示注入可以强制不需要交接
- **Loop detection.**Dos agentes que se entregan de un lado a otro es un fracaso común; detecta con una simple verificación de anillo de último K.
  En inglés:**循环检测。** dos agentes volver a comunicarse es un fracaso habitual; con simple reciente K siguiente ciclo de inspección de inspección 
- **Fallback agent.**Si no existe un objetivo de entrega, vuelva a un defecto seguro.
  En inglés:**后备 Agent。**Si el objetivo de conexión no existe, regresa al valor de seguridad.

## Los ejercicios.

1. - ¿ Qué ?`code/main.py`Confirme que el agente activo de la segunda vuelta es el reembolso.
   Traducción:运行`code/main.py`,分诊到退款代理──确认第二轮活动代理是退款──
2. Añadir una regla de detección de bucle: si los mismos dos agentes han entregado 3 veces seguidas, forzar una salida. Diseñar el fallback.
   Traducción: Añadir un ciclo de prueba de reglas: Si los dos mismos agentes 连续交接 3 veces,强制退出──设计后备方案──
3. Lea los documentos de OpenAI Agents SDK sobre filtros de entrega. Implemente una versión de "resumen en entrega": el agente saliente comprime el contexto a un resumen de bala antes de que el agente entrante se haga cargo.
   En la versión original, el código de acceso de los agentes de OpenAI se ha reducido a un resumen de datos.
4. Comparar la entrega de Swarm con un selector de GroupChatManager. ¿Qué patrón empeora la inyección rápida, y por qué?
   En inglés, el grupo de grupos de conversaciones es el más grande de los grupos de conversaciones.
5. Identifique una decisión de diseño explícita que Swarm toma que OpenAI Agents SDK cambió o se mantuvo.
   En el libro, el autor de la serie de novelas de la serie, el autor de la serie, el actor, el actor y el actor, el actor y el actor, el actor y el actor, el actor y el actor, el actor y el actor, el actor y el actor, el actor y el actor, el actor y el actor, el actor y el actor, el actor y el actor, el actor y el actor, el actor y el actor, el actor y el actor, el actor y el actor, el actor y el actor, el actor y el actor, el actor y el actor, el actor y el actor, el actor y el actor, el actor y el actor, el actor y el actor, el actor y el actor y el actor, el actor y el actor, el actor y el actor y el actor, el actor y el actor y el actor, el actor y el actor y el actor, el actor y el actor y el actor, el mismo, el mismo, se rejuvencuerdas.

## Términos clave .

| Term | What people say | What it actually means |
|------|----------------|------------------------|
| Routine / 例程 | "The agent prompt" / "Agent 提示" | System prompt + tool list. Defines role and available handoffs. / 系统提示 + 工具列表。定义角色和可用交接。 |
| Handoff / 交接 | "Transfer to another agent" / "转移到另一个 Agent" | A tool the active agent can call that returns a new Agent. The runtime switches active agent. / 活动 Agent 可以调用的工具，返回新 Agent。运行时切换活动 Agent。 |
| Stateless / 无状态 | "No memory between runs" / "运行间无记忆" | Swarm does not persist anything; memory is the caller's responsibility. / Swarm 不持久化任何东西；内存是调用者的责任。 |
| Active agent / 活动 Agent | "Who's speaking now" / "现在谁在说话" | The agent currently holding the conversation. Handoff changes this. / 当前持有对话的 Agent。交接改变这个。 |
| Context transfer / 上下文传输 | "What moves on handoff" / "交接时传输什么" | Policy for what history the incoming agent sees: full, last N, or summarized. / 传入 Agent 看到什么历史的策略：完整、最后 N 条或摘要。 |
| Handoff loop / 交接循环 | "Agents ping-pong" / "Agent 乒乓" | Failure mode where two agents keep handing back to each other. / 两个 Agent 持续互相交接的失败模式。 |
| OpenAI Agents SDK | "Production Swarm" / "生产 Swarm" | March 2025 successor; adds sessions, guardrails, tracing on top of the handoff primitive. / 2025 年 3 月继任者；在交接原语之上添加会话、防护栏、追踪。 |
| Handoff filter / 交接过滤器 | "Gate on transfer" / "传输门" | SDK feature to inspect and modify context at the handoff boundary. / 在交接边界检查和修改上下文的 SDK 特性。 |

## Más Leer más Leer más

- [OpenAI cookbook — Orchestrating Agents: Routines and Handoffs](https://developers.openai.com/cookbook/examples/orchestrating_agents) la articulación de referencia
  En inglés: OpenAI 手册  编排 Agent:例程和交接  参考阐述
- [OpenAI Swarm repo](https://github.com/openai/swarm) la aplicación original, conservada como referencia conceptual
  中文翻译:OpenAI Swarm 仓库  原始实现,保留为概念参考
- [OpenAI Agents SDK docs](https://openai.github.io/openai-agents-python/) sucesor de producción con sesiones y seguimiento
  China 文档 带会话和追踪的生产继任者 带会话和追踪的生产继任者 带会话和追踪的生产继任者
- [Anthropic handoff-in-Claude notes](https://docs.anthropic.com/en/docs/claude-code) cómo los subagentes de código claude utilizan un patrón similar a la entrega a través de `Task`
  En español: Antropic Claude En español: Claude Code En español: Claude Code En español: Claude Code En español: Claude Code En español: Claude`Task`Usar el mismo modo de comunicación
