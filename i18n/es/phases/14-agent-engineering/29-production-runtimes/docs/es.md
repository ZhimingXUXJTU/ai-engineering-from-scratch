# Tiempos de ejecución de la producción: Cuadra, evento, cron  producción  funcionamiento  Unión Europea

> Los agentes de producción funcionan en seis formas de tiempo de ejecución: solicitud-respuesta, transmisión, ejecución duradera, fondo basado en cola, impulsado por eventos y programado. Elige la forma antes de elegir el marco.

**Type:** Learn | **类型:** 学习
**Languages:** Python (stdlib) | **语言:** Python (标准库)
**Prerequisites:** Phase 14 · 13 (LangGraph), Phase 14 · 22 (Voice) | **前置知识:** 见原文
**Time:** ~60 minutes | **时间:** 见原文

> ¿ Qué es esto ?**【前置】**学本节前请先掌握:Fase 14·13(LangGraph) 状态图基础;Fase 17(Infraestructura y producción) 本节是其前置概念,深入生产部署看Fase 17 全部。

## Objetivos de aprendizaje

- Nombre las seis formas de ejecución de producción y coincide cada una con un patrón de marco / producto.
- Explique por qué la ejecución duradera (LangGraph) es importante para las tareas de largo horizonte.
- Describa el tiempo de ejecución basado en el evento y cuándo encaja Claude Managed Agents.
- Explicar la afirmación de observabilidad como carga de carga para los agentes de múltiples pasos.

## El problema es la introducción del problema

Los agentes de producción fallan de manera que un portátil de Jupyter no aparece: los tiempos de red en el paso 37, el usuario cuelga la llamada de voz, el trabajo cron se muere en la reiniciación de la máquina, el trabajador de fondo se queda sin memoria. La forma de tiempo de ejecución determina qué fallos son supervivientes.

> El método de fracaso de un agente de producción es Jupitero  notas de la red no puede ser demostrado: 37 paso de la red superhora, el usuario está en medio de la conversación en voz, la tarea está suspendida en el tiempo de muerte en el reinicio de la máquina, la falta de memoria en la última etapa del trabajo, la forma de funcionamiento determina qué fallas pueden ser recuperadas.


> **【中文解读】**Medio ambiente de producción Agente  Cuando se ejecuta necesita tratar problemas de desarrollo medio ambiente  Cuando se ejecuta: estado de perdurada                                                                                                                                                                                                                                                

> ¿ Qué es esto ?**【类比】**6 种运行时 = 6 种交通工具:(1) **request-response**=出租车(一次一结,最简单);(2) **streaming**=高铁(边走边看风景,token 流式);(3) **durable execution**=房车(sleeping awake to continue open,LangGraph checkpoint);(4) **queue-based**=Logistics company(任务排队,Celery/RQ);(5) **event-driven**= Plataforma de venta externa (事件触发,Claude Managed Agents);**scheduled**=钟(定时执行,cron) ――task多长多复杂决定选择哪个──

> ️ **【易错点】**运行时选错的 3 个坑:(1) **长任务用 request-response**3 小时任务挂 HTTP 请求,nginx 60s 超时切断; con ejecución duradera(LangGraph) + 后台轮询──(2) **observability 当可选**上线后发现"不知道为失败"; desde el primer día en contacto Langfuse/LangSmith, cada herramienta调用都追踪──(3) **没做 graceful shutdown** servicio reinicio cuando se ejecuta la tarea directamente muerto; usar SIGTERM 子 para guardar el puesto de control, reinicio después de que el puesto de control continúe funcionando.

> **{【拓展：2026年生产 Agent 运行时的选择：(1) LangGraph Cloud——LangGrap...】}**2026 años de producción Agente 运行时的选择:(1) LangGraph CloudLangGraph's托管服务,内置状态检查点和重放;(2) Temporal通用工作流引擎,配合AI SDK可构建持久化 Agent;(3) Autoconstrucción 基于Redis/Kafka的消息队列 +自定义 Agent 循环──关键决策因素是是否需要持久化执行如果Agente可能运行数小时甚至数天,Temporal或 LangGraph是更安全的选择──
## El concepto central.

### Requisito y respuesta

- HTTP sincrónico. El usuario espera la finalización.
- Solo viable para tareas cortas (< 30 años).
- Las pilas: Agno (Python + FastAPI), Mastra (TypeScript + Express/Hono/Fastify/Koa).
- Observabilidad: registros de acceso HTTP estándar + extensiones de OTel.

### En streaming

- SSE o WebSocket para salida progresiva.
- LiveKit extiende esto a WebRTC para voz/vídeo (lección 22).
- Stacks: cualquier marco con soporte de transmisión + una frontend que maneje SSE/WS.
- Observabilidad: tiempo por pieza, latencia de primer token, latencia de cola.

### Ejecución duradera

- El estado de control después de cada paso; auto-resumen en caso de fallo.
- El modelo de actores de AutoGen v0.4 aisla las fallas a un agente (lección 14).
- El diferenciador central de LangGraph (lección 13).
- Es esencial cuando el número de pasos es desconocido y el costo de recuperación es alto.

### Basado en la cola / fondo

- El trabajo entra en cola, los trabajadores se recogen, los resultados fluyen a través de webhooks o pub/sub.
- Esencial para agentes de largo horizonte (decenas a cientos de pasos por tarea, por anuncio de uso de computadora de Anthropic).
- Las pilas: Celery (Python), BullMQ (Node), SQS + Lambda (AWS), personalizado.
- Observabilidad: profundidad de cola, distribución de latencia por trabajo, tamaño de DLQ.

### El desarrollo de la actividad

- Los agentes se suscriben a los gatillos: nuevo correo electrónico, PR abierto, cron fire.
- Claude Managed Agents cubre esto fuera de la caja (lección 17).
- Los flujos de CrewAI (lección 15) estructuran flujos de trabajo deterministas basados en eventos.
- Observabilidad: fuente de activación, latencia de inicio de evento, latencia de agente.

### Programación

- Agentes en forma de Cron que se ejecutan periódicamente.
- Combina con una ejecución duradera para que una carrera nocturna fallida se reanude la próxima vez.
- Stacks: Kubernetes CronJob + un marco duradero; alojado (Render cron, Vercel cron).

### Modelos de despliegue para 2026

- **CrewAI Flows**para la producción basada en eventos.
- **Agno**FastAPI sin estado para microservicios Python.
- **Mastra**Adaptadores de servidores (Express, Hono, Fastify, Koa) para su incorporación.
- **Pipecat Cloud / LiveKit Cloud**para la voz gestionada (lección 22).
- **Claude Managed Agents**para asíncrono de larga duración alojado.

### La observabilidad es de carga

Sin OpenTelemetry GenAI (lección 23) más un backend Langfuse/Phoenix/Opik (lección 24), no se puede deshacer un agente de múltiples pasos que falló en el paso 40. Esto no es opcional para la producción. Es la diferencia entre "deshacemos deshacer rápidamente" y "replayamos desde cero con más registro".

> 没有 OpenTelemetry GenAI span(第 23 课)加上Langfuse/Phoenix/Opik 后端(第 24 课),you cannot调试在第 40 步失败的多步代理── esto no es opcional para el entorno de producción── esto es la diferencia entre "rápido调试" y "从头重放并添加更多日志".

> La implementación, expansión y fiabilidad de los agentes en el proceso de producción, incluyen: gestión de estado, recuperación de errores, limitaciones, gestión de filas y control de costes.

### Cuando los tiempos de ejecución de la producción no funcionen

- **Wrong shape choice.**Elegir la respuesta a las solicitudes para una tarea de 5 minutos.
- **No DLQ.**Trabajadores en cola sin letra muerta.
- **Opaque background work.**El agente de fondo se ejecuta sin rastro de exportación. Los fallos son invisibles hasta que el usuario los informa.
- **Skipping durable state.**Cualquier ejecución > 30 segundos donde no se puede permitir reiniciar necesita ejecución duradera.

> **错误的形态选择。**Por 5 minutos tareas seleccionar petición- respuesta.
> **没有 DLQ。**队列工作器没有死信队列──失败的任务消失──
> **不透明的后台工作。**后台 Agente 运行没有追踪导出――失败不可见直到用户报告――
> **跳过持久化状态。**Cualquier operación que exceda los 30 segundos y sea insoportable en el reinicio requiere una ejecución permanente.

## Construye y realiza.
```figure
wb-runtime-shapes
```

## Construye el mismo

`code/main.py`es una demostración multi-forma de stdlib:

- Punto final de solicitud y respuesta (función simple).
- El controlador de transmisión (generador).
- Trabajadora en cola con DLQ.
- Registro de activadores de eventos.
- Programación en forma de cron.

- ¿Qué quieres decir ?

```bash
python3 code/main.py
```

Resultado: cinco rastros que muestran el comportamiento de cada forma en la misma tarea. La misma lógica del agente, diferentes capas externas. La ejecución duradera (la sexta forma) se cubre intencionalmente en la Lección 13 con el punto de control de LangGraph.

> 输出:五种追踪显示每种形态在同一任务上的行为――相同的代理 逻辑,不同的外──持久化执行――第六种形态) 有意在第13 课中通过 LangGraph 检查点覆盖――

> La implementación, expansión y fiabilidad de los agentes en el proceso de producción, incluyen: gestión de estado, recuperación de errores, limitaciones, gestión de filas y control de costes.

## Usalo con el marco de ejecución

- **Request-response**para el estilo de chat UX.
- **Streaming**para respuestas progresivas.
- **Durable**para tareas de largo horizonte.
- **Queue**para lote / asíncrono / de larga duración.
- **Event**para la reactividad del agente.
- **Cron**para el mantenimiento de la vivienda (consolidación de memoria, evaluaciones, informes de costes).

## Envíe el producto .

`outputs/skill-runtime-shape.md`elige una forma de tiempo de ejecución para una tarea y fija los requisitos de observabilidad.

> `outputs/skill-runtime-shape.md`Para la tarea de seleccionar una forma de funcionamiento y conectar observabilidad requisitos.

> La implementación, expansión y fiabilidad de los agentes en el proceso de producción, incluyen: gestión de estado, recuperación de errores, limitaciones, gestión de filas y control de costes.

## Los ejercicios.

1. Portar su Lección 01 ReAct bucle a las seis formas en su pila. ¿Qué forma se ajusta a la superficie del producto?
  En inglés, "pensar y practicar" significa "pensar y practicar".
2. Añadir un DLQ a la demostración basada en la cola. Simula el fracaso del trabajo del 10%; tamaño de DLQ de superficie.
  En inglés, "pensar y practicar" significa "pensar y practicar".
3. Escriba un agente de evaluación cron-triggered que se ejecuta todas las noches contra sus 20 mejores rastros del día.
  En inglés, "pensar y practicar" significa "pensar y practicar".
4. Implementar el streaming con presión de contra: si el cliente es lento, detenga al agente. ¿Cómo interactúa esto con un presupuesto de turno?
  En inglés, "pensar y practicar" significa "pensar y practicar".
5. ¿Cuándo trasladaría a un agente de largo horizonte a administrar?
  En inglés, "pensar y practicar" significa "pensar y practicar".

## Términos clave .

| Term | What people say | What it actually means |
|------|----------------|------------------------|---|
| Request-response | "Synchronous" | User waits; short tasks only |  |
| Streaming | "SSE / WS" | Progressive output; better UX; latency observable per chunk |  |
| Durable execution | "Resume from failure" | Checkpointed state; restart at last step |  |
| Queue-based | "Background jobs" | Producer / worker pool / DLQ |  |
| Event-driven | "Trigger-based" | Agent reacts to external events |  |
| DLQ | "Dead-letter queue" | Parking lot for failed jobs |  |
| Claude Managed Agents | "Hosted harness" | Anthropic-hosted long-running async with caching + compaction |  |

## Más Leer más Leer más

- [LangGraph overview](https://docs.langchain.com/oss/python/langgraph/overview) Detalles de ejecución duraderos
  En el caso de los niños, el nombre de la persona que se encuentra en el lugar de residencia es el de la persona que se encuentra en el lugar de residencia.
- [Claude Managed Agents overview](https://platform.claude.com/docs/en/managed-agents/overview) acogida sin sincronización de larga duración
  En el caso de los niños, el nombre de la persona que se encuentra en el lugar de residencia es el de la persona que se encuentra en el lugar de residencia.
- [Anthropic, Introducing computer use](https://www.anthropic.com/news/3-5-models-and-computer-use) "decenas a cientos de pasos por tarea"
  En el caso de los niños, el nombre de la persona que se encuentra en el lugar de residencia es el de la persona que se encuentra en el lugar de residencia.
- [AutoGen v0.4 (Microsoft Research)](https://www.microsoft.com/en-us/research/articles/autogen-v0-4-reimagining-the-foundation-of-agentic-ai-for-scale-extensibility-and-robustness/) aislamiento de fallas del modelo actor
  En el caso de los niños, el nombre de la persona que se encuentra en el lugar de residencia es el de la persona que se encuentra en el lugar de residencia.
