# Modelos de orquestación: Supervisor, grupo, jerárquico 编排 分层 主管 模式 群体

> Cuatro patrones de orquestación se repiten en los marcos 2026: supervisor-trabajador, enjambre / peer-to-peer, jerárquico, debate. La guía de Anthropic: "Se trata de construir el sistema adecuado para sus necesidades".

**Type:** Learn + Build | **类型:** 构建
**Languages:** Python (stdlib) | **语言:** Python (标准库)
**Prerequisites:** Phase 14 · 12 (Workflow Patterns), Phase 14 · 25 (Multi-Agent Debate) | **前置知识:** 见原文
**Time:** ~60 minutes | **时间:** 见原文

> ¿ Qué es esto ?**【前置】**学本节前请先掌握:Fase 14·01(Curso de agentes) Un solo agente 基础;Fase 14·12(Putros de flujo de trabajo) Antropic's 5 种工作流模式;Fase 14·25(Debate multi-agente) 多 Agent 协作基础。**重要原则**Primero con un solo agente + 工作流, no hay tiempo suficiente para volver a subir más agentes 拓──

## Objetivos de aprendizaje

- Nombre los cuatro patrones de orquestación recurrentes y cuándo cada uno encaja.
- Describa la recomendación de LangChain 2026: supervisión basada en herramientas y bibliotecas supervisoras.
- Explica la regla de "construir el sistema correcto" de Anthropic y cómo se aborda la elección de topología.
- Implementar los cuatro en un estudio contra un LLM con guión común.

## El problema es la introducción del problema

Los equipos buscan "multi-agente" antes de necesitarlo. Cuatro patrones se repiten en los marcos; una vez que se puede nombrarlos, se puede elegir el correcto  o saltar la topología por completo.

> El equipo utiliza "Multi-Agent" en los momentos innecesarios. Cuatro patrones aparecen repetidamente en el marco; una vez que puedes nombrarlos, puedes elegir uno correcto o saltar completamente sobre ellos.


> **【中文解读】**El modelo de organización de agentes define la distribución y coordinación de tareas en un sistema de múltiples agentes. Cuatro tipos de modelos centrales: 1) la orden de las tareas entre agentes; 2) la distribución de múltiples agentes y el tratamiento de diferentes tareas; 3) el nivel de los administradores; 3) el reparto de tareas entre agentes y trabajadores; 4) la igualdad entre agentes.

> ¿ Qué es esto ?**【类比】**4 种编排模式 = 4 种公司组织:(1) **Supervisor-Worker**= 老板分活给员工 (la mayoría de los empleados de LangGraph)**Swarm/P2P**= 同事相互协作(适合讨论类任务,AutoGen GroupChat);(3) **Hierarchical**= 多层老板(CEO→总监→员工,超复杂任务);(4) **Debate**= 委员会投票 (comisión de votación)

> ️ **【易错点】**编排选错的 3 个坑:(1) **简单任务用多 Agent**Un agente único + 5 工具能解决 80% 需求, demasiado pronto con un supervisor, en cambio aumenta la complejidad;**Supervisor 成瓶颈** todas las tareas que ha hecho el supervisor 转发,单点延迟 + 单点失败;让工人间直接通信(仅必要时报 supervisor)**没设 worker 超时**lora labor 卡住整个流程; cada trabajador 调用 debe establecer tiempo fuera,超时返回降级结果──

> **{【拓展：Agent 编排是 2026 年生产 Agent 系统的核心挑战。Anthropic 的模式分类（P...】}**El sistema de distribución de agentes es un reto central de la producción de sistemas de agentes en 2026: el modelo antropico de cadenas de cadenas, enrutamiento, paralelación y trabajadores de orquestación se ha convertido en un estándar. En la aplicación real, la mayoría de los sistemas de distribución de sistemas utilizan varios modelos, como los primeros en utilizar los modelos de los clientes, y el uso de los modelos de distribución de niveles de los agentes.
## El concepto central.

### Trabajadores supervisores

- Un LLM de enrutamiento central envía a agentes especializados.
- Decide: volver a sí mismo, entregar a un especialista, terminar.
- Los especialistas no se hablan entre sí; todo el enrutamiento pasa por el supervisor.

Cuadro: LangGraph `create_supervisor`, trabajadores de la Orquesta Antropical, Proceso Jerárquico de la CrewAI.

> 编排模式描述多 系统的组织方式──主要模式包括:监督者(中央路由)、群体(点对点移交)、层次化(嵌套监督)、管道(顺序处理)──

**2026 LangChain recommendation:**hacer supervisión a través de llamadas directas a herramientas en lugar de `create_supervisor`. Da un control de ingeniería de contexto más preciso  decides exactamente lo que ve cada especialista.

> **2026 年 LangChain 建议：**通过直接工具调用而不是 `create_supervisor`Para lograr la supervisión, proporcionar un control de ingeniería más detallado, puedes decidir con precisión qué verá cada experto.

### En el caso de los productos de la industria de la industria de la producción, el precio de la producción se calcula en el caso de los productos de la industria de la industria de la industria de la producción.

- Los agentes se entregan directamente a través de una superficie compartida de herramientas.
- No hay router central.
- Menos latencia que la de supervisor (menos saltos).
- Más difícil de razonar sobre (ningún punto de control único).

Marco: Topología de enjambre LangGraph, entrega de SDK de OpenAI Agents (cuando todos los agentes pueden entregar a todos los demás).

> 编排模式描述多 系统的组织方式──主要模式包括:监督者(中央路由)、群体(点对点移交)、层次化(嵌套监督)、管道(顺序处理)──

### Los niveles de orden

- Supervisores que gestionan subsupervisores que gestionan trabajadores.
- Implementados como subgrafos anidados en LangGraph; tripulaciones anidadas en CrewAI.
- Escala a grandes poblaciones de agentes a costa de la complejidad operativa.

Cuando lo necesite: cuando el presupuesto contextual de un solo supervisor no puede contener descripciones de todos los especialistas.

> ¿qué tiempo necesita: cuando el presupuesto de un supervisor individual no puede contener la descripción de todos los especialistas

> 编排模式描述多 系统的组织方式──主要模式包括:监督者(中央路由)、群体(点对点移交)、层次化(嵌套监督)、管道(顺序处理)──

### Debate sobre el tema

- Proponentes paralelos + crítica cruzada iterativa (lección 25).
- No es realmente orquestación  más verificación  pero aparece como una opción de topología en los marcos.

### Los equipos autónomos vs flujos deterministas

CrewAI formaliza dos modos de despliegue:

- **Flow**para la automatización determinista basada en eventos (punto de partida recomendado para la producción).
- **Crew**para la colaboración autónoma basada en el papel.

Esto es ortogonal a los cuatro patrones anteriores, pero los mapas a la topología: Flow es típicamente supervisor o jerárquico; Crew es típicamente supervisor con un router LLM.

> 编排模式描述多 系统的组织方式──主要模式包括:监督者(中央路由)、群体(点对点移交)、层次化(嵌套监督)、管道(顺序处理)──

### La guía de Anthropic

"El éxito en el área de LLM no se trata de construir el sistema más sofisticado, sino de construir el sistema adecuado para tus necesidades".

> 编排模式描述多 系统的组织方式──主要模式包括:监督者(中央路由)、群体(点对点移交)、层次化(嵌套监督)、管道(顺序处理)──

Orden de decisión:

1. Un agente único + patrones de flujo de trabajo (lección 12)  comienzan aquí.
2. Trabajo supervisor  cuando usted tiene 2-4 especialistas.
3. Swarm  cuando la latencia importa más que la claridad del razonamiento.
4. Hierarquico  sólo cuando el presupuesto de contexto de supervisión falla.
5. Debate  cuando la precisión es más importante que el costo.

### Cuando este patrón va mal

- **Topology-first thinking.**"Necesitamos multi-agente" antes de identificar qué problema multi-agente resuelve.
- **Bouncing handoffs in swarm.**A -> B -> A -> B. Utilice contadores de salpicaduras.
- **Fake hierarchy.**Tres capas porque "empresa"; dos equipos reales.

> **拓扑优先思维。**En determinar qué más agentes resolver el problema antes de decir "necesitamos más agentes".
> **群体中弹跳交接。**A -> B -> A -> B。 Usar un salto de cuentas
> **虚假层级。**Porque el "clasificado empresarial" tiene tres niveles; en realidad sólo hay dos equipos.

## Construye y realiza.
```figure
orchestration-pattern
```

## Construye el mismo

`code/main.py`Implementa los cuatro patrones en stdlib contra un LLM con guión:

> 编排模式描述多 系统的组织方式──主要模式包括:监督者(中央路由)、群体(点对点移交)、层次化(嵌套监督)、管道(顺序处理)──

- `Supervisor` Router central.
- `Swarm` Peer-to-peer con entregas directas.
- `Hierarchical` Supervisores de supervisores.
- `Debate` Propososos paralelos + crítica.

Cada patrón maneja la misma tarea de tres intenciones (reembolso / error / ventas).

> 编排模式描述多 系统的组织方式──主要模式包括:监督者(中央路由)、群体(点对点移交)、层次化(嵌套监督)、管道(顺序处理)──

- ¿Qué quieres decir ?

```
python3 code/main.py
```

Resultado: rastreo por patrón + recuento de operaciones. Supervisor es más limpio; enjambre es más corto; jerárquico es más profundo; debate es más caro.

> 输出: cada modo de seguimiento + 操作数──监督者最清晰;群体最短;层级最深;辩论最昂贵──

> 编排模式描述多 系统的组织方式──主要模式包括:监督者(中央路由)、群体(点对点移交)、层次化(嵌套监督)、管道(顺序处理)──

## Usalo con el marco de ejecución

- **LangGraph**para supervisores y jerárquicos (subgrafos anidados).
- **OpenAI Agents SDK**para las entregas como herramientas (en forma de supervisor).
- **CrewAI Flow**para la determinación de la producción.
- **Custom**para el debate o cuando quieras el control exacto.

## Envíe el producto .

`outputs/skill-orchestration-picker.md`elige una topología y la implementa.

> `outputs/skill-orchestration-picker.md`选择一个拓并实现它──

> 编排模式描述多 系统的组织方式──主要模式包括:监督者(中央路由)、群体(点对点移交)、层次化(嵌套监督)、管道(顺序处理)──

## Los ejercicios.

1. Convierte a un supervisor en un enjambre quitando el router. ¿Qué se rompe? ¿Qué mejora?
  En inglés, "pensar y practicar" significa "pensar y practicar".
2. Añadir un contador de salto al enjambre: rechazar después de 3 entregas. ¿Coge A->B->A rebotando?
  En inglés, "pensar y practicar" significa "pensar y practicar".
3. ¿Cuál es el presupuesto de contexto que falla sin anidar?
  En inglés, "pensar y practicar" significa "pensar y practicar".
4. Profilar los cuatro patrones en una carga de trabajo en forma de producción. ¿Cuál gana en qué métrica (latencia, costo, precisión, descomposición)?
  En inglés, "pensar y practicar" significa "pensar y practicar".
5. Lea el post de Anthropic sobre "Construir agentes eficaces" y mapa cada uno de sus flujos de producción a uno de los cuatro. ¿Alguno que no haga un mapa limpio?
  En inglés, "pensar y practicar" significa "pensar y practicar".

## Términos clave .

| Term | What people say | What it actually means |
|------|----------------|------------------------|---|
| Supervisor-worker | "Router + specialists" | Central LLM dispatches to specialists; they don't talk to each other |  |
| Swarm | "Peer-to-peer" | Direct handoffs via shared tools; no central router |  |
| Hierarchical | "Supervisors of supervisors" | Nested subgraphs for large populations |  |
| Debate | "Proposer + critique" | Parallel proposers, cross-critique (Lesson 25) |  |
| Tool-call-based supervision | "Supervisor without a library" | Implement supervisor as direct tool calls for context control |  |
| Crew | "Autonomous team" | CrewAI's role-based collaboration mode |  |
| Flow | "Deterministic workflow" | CrewAI's event-driven production mode |  |

## Más Leer más Leer más

- [Anthropic, Building Effective Agents](https://www.anthropic.com/research/building-effective-agents) cinco patrones + agente vs flujo de trabajo
  En el caso de los niños, el nombre de la persona que se encuentra en el lugar de residencia es el de la persona que se encuentra en el lugar de residencia.
- [LangGraph overview](https://docs.langchain.com/oss/python/langgraph/overview) supervisor, enjambre, jerárquico
  En el caso de los niños, el nombre de la persona que se encuentra en el lugar de residencia es el de la persona que se encuentra en el lugar de residencia.
- [CrewAI docs](https://docs.crewai.com/en/introduction) Equipamiento vs flujo
  En el caso de los niños, el nombre de la persona que se encuentra en el lugar de residencia es el de la persona que se encuentra en el lugar de residencia.
- [Du et al., Society of Minds (arXiv:2305.14325)](https://arxiv.org/abs/2305.14325) Modelo de debate
  En el caso de los niños, el nombre de la persona que se encuentra en el lugar de residencia es el de la persona que se encuentra en el lugar de residencia.
