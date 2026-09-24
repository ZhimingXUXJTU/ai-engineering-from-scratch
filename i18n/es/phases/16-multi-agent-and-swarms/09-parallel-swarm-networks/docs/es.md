# Paralelas / Arquitecturas en red

> Contraste con el supervisor: no hay un factor central de decisión. Los agentes leen un bus de eventos compartidos, recogen el trabajo sincrónicamente, escriben los resultados. LangGraph admite explícitamente "Arquitectura de la Enredada" para entornos dinámicos y descentralizados. Matrix (arXiv:2511.21686) representa tanto el control como el flujo de datos como mensajes serializados que pasan a través de colas distribuidas para eliminar el cuello de botella del orquestrador. La compensación es explícita: determinismo y trazabilidad para la escalabilidad. El conjunto se adapta a las tareas con muchos subproblemas independientes; no se adapta a las tareas que requieren un solo plan coherente.

> **【中文解读】**Este capítulo presenta el modelo de organización de la red de grupos de ejecuciones  un gran número de agentes  a través del estado compartido  de trabajo 

> **【拓展：parallel swarm networks→具体应用】**Y se realiza una red de grupos que permite que un gran número de agentes se encarguen de procesar y luego se agrupen los resultados.


**Type:** Learn | **类型:** 学习
**Languages:** Python | **语言:** Python
**Prerequisites:** Phase 16 · 05 (Supervisor Pattern), Phase 16 · 04 (Primitive Model) | **前置知识:** Phase 16 · 05 (Supervisor Pattern), Phase 16 · 04 (Primitive Model)
**Time:** ~75 minutes | **时间:** ~75 分钟

> ¿ Qué es esto ?**【前置】**学本节前请先掌握:Fase 16·04-05(原语+Supervisor)。本节是Supervisor's反面无中心协调器的群体网络。
> ¿ Qué es esto ?**【类比】**Swarm vs Supervisor = "decentralización" vs "niveles de nivel"──Supervisor = 公司(CEO 调度);Swarm = 开源社区(每人看问题 板自己领取)──Swarm 适合独立子任务(多文件编辑、多源查询),不适合需要单一计划的任务──5-10 个代理是最优太多会聚聚时打架──

## # El problema # # El problema #

El supervisor se limita a unos pocos trabajadores. ¿Qué pasa con cientos? El supervisor mismo se convierte en el cuello de botella: cada decisión sobre quién hace qué canaliza a través de un agente. Un paso lento del plan impide todo el sistema.

> El supervisor puede extenderse a varios equipos de trabajo. El supervisor en sí mismo se convierte en un botellón: cada decisión sobre quién y qué hacer pasa por un agente.

El supervisor es en sí mismo una llamada de LLM. En cientos de trabajadores, el supervisor hace cientos de llamadas de LLM sólo para enviar. Cada llamada es de segundos; el despacho de gastos dominan.

> En cientos de máquinas de trabajo, el supervisor sólo se regula en realizar cientos de veces el LLM 调用── cada una de ellas se regula en unos segundos; la regulación se realiza en el grupo de supervisores.

Las arquitecturas de conjuntos cambian el diseño. En lugar de un planificador central que despachará el trabajo, los trabajadores eligen el trabajo de una cola compartida. La "coordinación" se incubó en la semántica del bus de eventos.

> La estructura del grupo ha cambiado de diseño. No es un planificador central que distribuye el trabajo, sino que el trabajo se obtiene de la línea compartida.

La inversión arquitectónica es significativa: el cuello de botella pasa de "el LLM que decide qué hacer" a "el corredor de mensajes que las rutas funcionan".

> La estructura reversa transformación importante: el grupo de agentes que cambian el modelo de LLM casi siempre gana.

## Concepto de la esencia de la concepción

### La forma

```
                ┌──── shared queue ────┐
                │                      │
       ┌────────┼────────┐  ◄──────┬───┘
       ▼        ▼        ▼         │
     Worker  Worker  Worker   Worker
      A       B       C        D
       │        │        │         │
       └────────┴────────┴─────────┘
                 │
                 ▼
            results pool
```

No hay orquesta. Cada trabajador repite: tirar una tarea, procesar, escribir el resultado (y opcionalmente hacer seguimientos).

> 没有编排器.每个工作器重复:拉取任务、处理、写入结果.

La falta de un decider central es la característica definitorio. Los trabajadores no esperan instrucciones; se autoorganizan alrededor de la cola. Este es el modelo de actor aplicado a los LLM.

> 缺乏 central decision maker  工作器不等待指令; elles se organizan en la línea de trabajo  工作器是响应消息的独立演员

### Cuando el enjambre se ajusta

- **Many independent tasks.**Descargar, transformar, clasificar, las tareas no dependen de las otras.
  En inglés:**许多独立任务。**抓取、转换、分类── tareas entre no dependen entre sí.
- **Variable-duration work.**Si algunas tareas tardan 100 ms y otras 10s, un enjambre balancea la carga automáticamente  rápidos trabajadores tiran los próximos trabajos.
  En inglés:**可变持续时间的工作。**Si algunas tareas requieren 100 ms y otras 10s, el grupo se balanceará automáticamente la carga.
- **Throughput over determinism.**Te importa el tiempo total de finalización, no el ordenamiento estricto.
  En inglés:**吞吐量优先于确定性。**Tu preocupación es el tiempo de realización, no la rigurosa orden.

### Cuando el enjambre falla

- **Ordered workflows.**Si el paso 3 necesita la salida del paso 2, un enjambre corre el riesgo de disparar el paso 3 antes de que se complete el paso 2.
  En inglés:**有序工作流。**Si el paso 3 necesita el paso 2 de salida, el grupo tiene el paso 3 en el paso 2  completado antes de que el paso 2 触发风险──
- **Global-plan tasks.**Las preguntas de investigación complejas se benefician de un planificador.
  En inglés:**全局计划任务。** Problemas de investigación complejos beneficiados por los planificadores un grupo de investigadores produce hechos independientes, en lugar de un informe coherente
- **Debugging.**Sin registro central y trabajo asincrónico, reproducir un error es caro.
  En inglés:**调试。**没有中央日志和异步工作, el costo de la recuperación de errores es muy alto.

### Matriz (arXiv:2511.21686)

Matrix es el documento de 2025 que lleva a swarm a su conclusión natural: tanto el flujo de control como el flujo de datos son mensajes serializados en colas distribuidas. No hay coordinador central. La tolerancia a fallos proviene de la durabilidad del mensaje. La escalabilidad es el problema del corredor de mensajes, no del sistema.

> Matrix es un trabajo que propone que los grupos de 2025 lleguen a la conclusión natural: el flujo de control y el flujo de datos son mensajes de secuenciación en la cola distribuida. No hay coordinador central.

Al hacer del corredor (Kafka, Redis Streams, NATS) el cuello de botella de escala, Matrix evita el cuello de botella de LLM como orquesta.

> 通过使代理(Kafka、Redis Streams、NATS) se convirtió en un amplificador, Matrix 完全避开LLM 作为编排器的瓶──如果代理可以,系统可以扩展到数千代理;LLM es puramente un trabajo, nunca es un coordinador──

Contribución: un modelo de programación en el que la coordinación multi-agente es "qué tema de mensaje se suscribe este agente?" en lugar de "qué agente elige el supervisor después?" Esto hace que el sistema parezca una malla de eventos pub/sub.

> 贡献: un modelo de programación, multi-agente 协调 es "este agente 订阅什么消息主题?" en lugar de "监督者下一个选择哪个代理?" que hace que el sistema parezca una publicación/subscrición de eventos 网格──

### La arquitectura de los enjambres de LangGraph
### Un montón en los marcos gráficos

Los documentos de LangGraph 2025 describen explícitamente "Arquitectura de la Enredada" como uno de los patrones de múltiples agentes: los agentes son nodos, pero los bordes forman un gráfico dirigido con ciclos y cualquier nodo puede ser activado desde el grupo.

> LangGraph 2025 文档明确将"群体架构" describir como un modelo de múltiples agentes: Agente es un punto, pero al borde de la formación de un círculo tiene un dibujo, cualquier punto puede ser activado en el grupo.

La contribución de LangGraph: el mismo modelo mental basado en gráficos ahora apoya la dinámica de enjambre. nodos que se activaban basándose en condiciones en lugar de bordes fijos. Esto une el gráfico estático y los mundos de enjambre puro.

> Contribuciones de LangGraph: el mismo modelo mental basado en gráficos ahora apoya la movilidad del grupo.

### Modo de falla: hambre y puntos calientes

Si todos los trabajadores hacen la tarea más rápida disponible, las tareas de larga duración nunca se seleccionan hasta que no queden las únicas.

> Si todos los equipos de trabajo se llevan a las tareas más rápidas disponibles, las tareas de largo tiempo no se seleccionarán nunca hasta que se conviertan en las únicas que quedan.

El hambre es el modo de falla de la firma del enjambre. Sin envejecimiento explícito (la prioridad aumenta con el tiempo de espera) o trabajadores especializados de tareas largas, una tarea de 10 segundos espera para siempre detrás de un flujo de tareas de 100 ms.

>  Hunger es el modelo de fracaso de los grupos ⋅ no hay un evidente envejecimiento ⋅ prioridad con el tiempo de espera aumentado ⋅ o especialización ⋅ Long Task Worker ⋅ 10 segundos                                                                                                                                                                                                                                                                                                                                                                                                                                                                               

Mitigación:
- Colas de prioridad con envejecimiento explícito (aumentar la prioridad con el tiempo de espera).
  China: 带显式老化优先队列 (随着等待时间增加优先级)
- Especialización de los trabajadores: algunos trabajadores solo realizan tareas "longas".
  Algunos equipos de trabajo sólo aceptan tareas de "长"
- Presión de retroceso: limita la cantidad de tareas rápidas que entran en la cola.
  En inglés, el nombre de la misión es "Limiting how many fast tasks into the line".

### El enlace de enrutamiento basado en el contenido

Los pares de conjuntos se realizan naturalmente con el enrutamiento basado en contenido (lección 22). En lugar de una cola genérica, tienen una cola por tipo de mensaje. Los trabajadores especializados se suscriben solo a su tipo. Esta es la base de las arquitecturas de bus de mensajes que se escalan a miles de agentes.

> 群体与内容基础的路由 (LECCIÓN 22) El parámetro natural no es una línea general, sino una línea para cada tipo de mensaje.

El enrutamiento basado en contenido más el enjambre le da la malla de eventos pub/sub: un sustrato donde cualquier agente puede publicar cualquier tipo de mensaje, y solo los agentes interesados lo reciben. Esta es la base de Matrix, CA-MCP y la mayoría de los sistemas multi-agentes de producción 2026 .

> 基于内容的路由加群体给你发布/订阅事件网格: un agente puede publicar cualquier tipo de mensaje y sólo el agente que esté interesado recibe su base.

## Construye y realiza.
```figure
sw-work-stealing
```

## Construye el mismo

`code/main.py`Implementa un enjambre de 4 hilos de trabajadores tirando de un compartido `queue.Queue`Las tareas tienen duradas variables (algunas rápidas, otras lentas).

> `code/main.py`                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             `queue.Queue`拉取工作线程──任务有可变持续时间(algunos rápidos, algunos lentos)──演示对比:

La comparación de tres vías es el valor educativo: las mismas tareas, los mismos trabajadores, sólo cambia la estrategia de envío. Secuencial = lento. Fijo = gastoso. Envase = óptimo. Los números del reloj de la pared hacen el caso empíricamente.

> Tres partes contra la comparación es el valor de la educación: la misma tarea, el mismo trabajo, sólo la modificación de la estrategia.

- **Sequential baseline:**un trabajador procesa todas las tareas en serie.
  En inglés:**顺序基线：**Una máquina de trabajo que maneja todas las tareas.
- **Fixed assignment:**cada tarea previamente asignada a un trabajador específico (estilo de supervisor).
  En inglés:**固定分配：**Cada tarea se asigna previamente a un determinado trabajo.
- **Swarm:**Los trabajadores se hacen cola compartida.
  En inglés:**群体：**工作器 de la línea de trabajo compartida

Las balanzas de un montón se cargan automáticamente; la asignación fija deja a los trabajadores rápidos inactivos cuando su tarea asignada es lenta.

> 群体自动平衡负载; fijación de la asignación de tareas lenta en el tiempo que hace que el rápido trabajo del equipo esté en el espacio

La distribución "inequitativa pero óptima" es la firma del enjambre. Un trabajador que termina su tarea en 50 ms tira tres más mientras un trabajador en una tarea de 2 segundos todavía está en su primera. El reloj de pared total está limitado por la tarea individual más lenta, no la suma.

> La distribución "no uniforme pero óptima" es la característica del grupo. 50 ms. El equipo de trabajo que termina la tarea en 2 segundos sigue ocupando tres tareas más en la primera tarea.

La salida muestra el número de tareas por trabajador (el grupo se distribuye de manera desigual pero óptima) y los tiempos del reloj de pared.

> 输出显示每个工作器的任务计数(群体分布不均但优优) y 挂钟时间──

## Usalo con el marco de ejecución

`outputs/skill-swarm-fit.md`evalúa si una tarea debe utilizar enjambre vs supervisor. Ingresos: independencia de tarea, variación de duración, requisitos de orden, necesidades de descomposición.

> `outputs/skill-swarm-fit.md`评估任务应使用群体还是监督者──输入: independencia de tareas、持续时间差、排序要求、可调试性需求──

## Envíe el producto .

Lista de control:

> 检查清单:

- **Priority queue with aging.**Prevenir el hambre de tareas largas.
  En inglés:**带老化的优先队列。**防止长任务饥饿──
- **Worker idempotency.**La tarea puede ser realizada más de una vez si un trabajador se estrella en medio de la carrera.
  En inglés:**工作器幂等性。**Si el trabajo se desploma, las tareas pueden ser retrasadas varias veces.
- **Durable queue.**Utilice Kafka, Redis Streams o una cola respaldada por una base de datos para la producción. `queue.Queue`Es sólo en memoria.
  En inglés:**持久队列。**Productos de la producción y el uso de Kafka, Redis Streams o bases de datos de apoyo de la línea.`queue.Queue`Sólo en la memoria.
- **Observability per task.**Cada tarea tiene un identificador de rastreo; cada trabajador registra el inicio y el final con él.
  En inglés:**每个任务的可观测性。**Cada tarea tiene un ID de seguimiento; cada trabajo con el que se registra comienza/acaba.
- **Back-pressure.**Si la cola crece más rápido que los trabajadores la drenan, ralentiza al productor.
  En inglés:**背压。**Si la línea de trabajo crece rápidamente en la velocidad de trabajo, disminuye el rendimiento de los productores.

## Los ejercicios.

1. - ¿ Qué ?`code/main.py`¿Cuánto más rápido es el enjambre que el secuencial en la carga de trabajo de duración variable?
   Traducción:运行`code/main.py`¿Cuánto más rápido que el grupo en la carga de trabajo en el tiempo de duración variable?
2. Añadir una variante de la cola de prioridad (uso `queue.PriorityQueue`Se debe asignar prioridad por tarea en el campo "importancia". Observe si las tareas de baja prioridad pasan hambre bajo carga continua.
   中文翻译:添加优先队列变体(使用 `queue.PriorityQueue`)■ en función de la "importancia" del trabajo, el segmento de distribución de prioridades■ observar si las tareas de baja prioridad están en carga continua de hambre■■
3. Implementar un detector de puntos calientes: registro cuando un trabajador procesa 3 veces más tareas que el trabajador más lento. ¿Qué indica esto sobre la distribución de la duración de la tarea?
   Traducción: Cuando cualquier máquina trabaja en un tiempo de trabajo más lento que en un tiempo de trabajo más lento, ¿qué características tiene esto?
4. Lea el resumen del documento de Matrix (arXiv:2511.21686) y la sección 3. Identifique una compensación específica que la Matrix acepta (ganancia de escalabilidad) y una que abandona (trazabilidad, determinismo).
   La matriz de la identidad de los usuarios es un factor de interés de la sociedad.
5. Convierta la demo del enjambre para usar un `queue.Queue`¿Qué reglas de enrutamiento tienen sentido cuando las tareas son heterogéneas?
   El grupo de trabajo de la empresa de la empresa de la empresa de la empresa de la empresa de la empresa de la empresa de la empresa de la empresa de la empresa de la empresa de la empresa de la empresa de la empresa de la empresa de la empresa de la empresa de la empresa de la empresa de la empresa de la empresa de la empresa de la empresa de la empresa de la empresa de la empresa de la empresa de la empresa de la empresa de la empresa de la empresa de la empresa de la empresa de la empresa de la marca de la marca de la marca de la marca de la marca de la marca de la marca de la marca de la marca de la marca de la marca de la marca de la marca de la marca de la marca de la marca de la marca de la marca de la marca de la marca de la marca de la marca de la marca de la marca de la marca de la marca de la marca de la marca de la marca de la marca de la marca de la marca de la marca de la marca de la marca de la marca de la marca de la marca de la marca de la marca de la marca de la marca de la marca de la marca de la marca de la marca de la marca de la marca de la marca de la marca de la marca de la marca de la marca de la marca de la marca de la marca de la marca de la marca de la marca de la marca de la marca de la marca de la marca de la marca de la marca de la marca de la marca de la marca de la marca de marca de la marca de la marca de marca de la marca de la marca de marca de marca de la marca de marca de la marca de marca de la marca de marca de marca de la marca de marca de marca de marca de marca de marca de marca de marca de marca de marca de marca de marca de marca de marca de marca de marca de marca de marca de marca de marca de marca de marca de marca de marca de marca de marca de marca de marca de marca de marca de marca de marca de marca de marca de marca de marca de marca de marca de marca de marca de marca de marca de marca de marca de marca de marca de marca de marca de marca de marca de marca de marca de marca de marca de marca de marca de marca de marca de marca de marca de marca de marca de marca de marca de marca de marca de marca de marca de marca de marca de marca de marca de marca de marca de marca de marca de marca de marca de marca de`queue.Queue`¿Cuál es la regla de ruta razonable cuando se construye una tarea?

## Términos clave .

| Term | What people say | What it actually means |
|------|----------------|------------------------|
| Swarm architecture / 群体架构 | "Decentralized agents" / "去中心化 Agent" | Workers pull from shared queue; no central orchestrator. / 工作器从共享队列拉取；没有中央编排器。 |
| Event bus / 事件总线 | "Agents subscribe to topics" / "Agent 订阅主题" | Message broker that routes tasks to workers by type or content. / 按类型或内容将任务路由到工作器的消息代理。 |
| Starvation / 饥饿 | "Task never runs" / "任务永远不运行" | Low-priority task never gets picked because higher-priority work arrives continuously. / 低优先级任务因为高优先级工作持续到达而永远不被选中。 |
| Hot-spotting / 热点 | "One worker drowns" / "一个工作器淹没" | Load imbalance where one worker gets most tasks. / 一个工作器获得大部分任务的负载不均衡。 |
| Back-pressure / 背压 | "Slow down the producer" / "减慢生产者" | Mechanism that signals upstream to stop producing when the queue fills up. / 当队列填满时向上游发出停止生产的信号机制。 |
| Idempotent worker / 幂等工作器 | "Safe to re-run" / "安全重新运行" | A task processed twice produces the same result. Required because workers may crash mid-run. / 任务处理两次产生相同结果。因为工作器可能中途崩溃所以需要。 |
| Durable queue / 持久队列 | "Survives crashes" / "崩溃后存活" | Queue backed by disk or replicated storage; tasks are not lost when a worker crashes. / 由磁盘或复制存储支持的队列；工作器崩溃时任务不丢失。 |
| Matrix framework / Matrix 框架 | "Full message-passing swarm" / "全消息传递群体" | Both data and control flow are serialized messages on distributed queues. / 数据流和控制流都是分布式队列上的序列化消息。 |

## Más Leer más Leer más

- [LangGraph workflows and agents — Swarm Architecture](https://docs.langchain.com/oss/python/langgraph/workflows-agents) apoyo explícito del enjambre
   群体架构  明确的群体支持  群体架构  群体支持  群体架构  明确的群体支持
- [Matrix — A Decentralized Framework for Multi-Agent Systems](https://arxiv.org/abs/2511.21686) Envuelo de mensajes completos
  En inglés, el lenguaje de la lengua inglesa es el lenguaje de la lengua inglesa.
- [Anthropic engineering — why supervisor not swarm in Research](https://www.anthropic.com/engineering/multi-agent-research-system) por qué un sistema de producción específico escogió explícitamente a un supervisor sobre un enjambre
  China 工程                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           
- [AutoGen v0.4 actor-model docs](https://microsoft.github.io/autogen/stable/) el actor impulsado por eventos reescribir, más cerca del enjambre que GroupChat de v0.2
  AutoGen v0.4 actor 模型文档  事件驱动 actor 重写,比 v0.2 的 GroupChat 更接近群体
