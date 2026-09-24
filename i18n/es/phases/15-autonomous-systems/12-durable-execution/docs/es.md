# Agentes de fondo de larga duración: ejecución duradera.

> Los agentes de producción de largo horizonte no se ejecutan en `while True`. Cada llamada de LLM se convierte en una actividad con checkpoint, retry, y replay. La integración de OpenAI Agents SDK de Temporal fue GA marzo 2026. Claude Code Routines (Anthropic) ejecuta invocaciones programadas de Claude Code sin un proceso local persistente. Las sesiones se pausan en la entrada humana, sobreviven a los despliegues y se reanudan desde el último checkpoint teclado por`thread_id`. Detrás de la nueva ergonomía se encuentra un viejo patrón  orquestación de flujos de trabajo  con una nueva entrada: LLM llama a actividades no deterministas que deben repetirse deterministicamente en la recuperación.

> **【中文解读】**Producción de la planta`while True`En el caso de los programas de investigación, el programa de investigación de la Universidad de California, San Diego, se ha desarrollado en el marco de la investigación de la investigación de la Universidad de San Diego, en el que se han desarrollado programas de investigación y investigación de la Universidad de San Diego, en el área de la salud y la salud.

> **【拓展：LLM 调用 = 活动的精确契合】**LLM 调用完美匹配活动特征:不确定性(temperatura > 0) 昂贵(金钱和延迟) 、可能失败(速率限制、超时) 、有副作用(调用工具)  让每个 LLM 调用包装为活动即可获得指数退避重试、跨重启检查点和可重放调试追踪──这就是为什么 Temporal、LangGraph、Cloudflare Durable Objects、Claude Code Routines 全部收到相同 API 形态`thread_id`+ 后端存储 + 最近检查点恢复──

**Type:** Learn | **类型:** 学习
**Languages:** Python (stdlib, minimal durable-execution state machine) | **语言:** Python（标准库，最小持久执行状态机）
**Prerequisites:** Phase 15 · 10 (Permission modes), Phase 15 · 01 (Long-horizon agents) | **前置知识:** Phase 15 · 10（权限模式），Phase 15 · 01（长程 Agent）
**Time:** ~60 minutes | **时间:** ~60 分钟

> ¿ Qué es esto ?**【前置】**学本节前请先掌握:Fase 15·10(权限模式) Fase 15·01(长程代理) 分布式系统基础(检查点、重试、等) Durable Execution = 把代理当工作流编排──
> ¿ Qué es esto ?**【类比】**Ejecución duradera = "Punto de archivo de agente"―Agente ordinario = 玩游戏没存档(崩=重头);Durable = Cada LLM 调用后自动存档(崩=读最近的存档)―Técnicas clave: poner cada LLM 调用包装为"活动",记录输入输出到日志,崩时重放日志而不是重新调用既省钱又避免副作用重复执行(如重复转账)―
> ️ **【易错点】**副作用工具(写数据库、调外部 API) 不存缺失键 → 恢复时重复执行可能导致业务错误(用户被扣两次款) ――修复: cada efecto secundario调用必须带等键(如`idempotency-key: uuid`), posteriormente en la siguiente dirección.

## El problema es la introducción del problema

> **【中文解读】**持久执行确保 Agent 任务在故障后能恢复――传统 Agent 在内存运行,进程崩意味着从头开始――持久执行将状态保存到外部存储 (archivo externo) DATABASE、文件系统), cualquier momento puede ser recuperado−Desde el punto de control más reciente―Temporal 和 LangGraph son dos marcos principales de ejecución permanente―

> **【拓展：durable execution】**持久执行对长时间运行的代理 至关重要――Si un agente necesita funcionar 2 小时的代理 在第90 分钟崩,没有持久执行就意味着重新开始――Temporal 通过事件追溯源实现持久工作流,LangGraph 通过检查点实现持久状态图――2026年最佳实践是每一个重要步骤后自动保存检查点――

Consideremos un agente que se ejecuta durante cuatro horas, llama a tres herramientas, le pide al usuario dos veces y hace cuarenta llamadas de LLM. A mitad de camino, el anfitrión que se ejecuta se reinicia.

> 考虑一个运行四小时的代理――它调用了三个工具――提示用户两次――进行了40次LLM 调用――中途,运行的主机重新启动――

¿Qué pasa?

> ¿Qué pasa?

- En un ingenuo .`while True`Lo que se hace es que el usuario se reincorpora en las llamadas de la aplicación de la aplicación de la aplicación de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de los usuarios de los usuarios de los usuarios de los usuarios de los mismos.
  En la lengua inglesa, el idioma se traduce en inglés como:`while True`循环中:一切丢失──运行从头头重新启动──三工具调用(带真实副作用) nuevamente ejecutar──用户再次被提示已批准的事──40 个 LLM 调用重新计费──
- Con ejecución duradera: la ejecución se reanuda desde el punto de control más reciente. Las actividades ya completadas no se re-executa; sus resultados se reproducen desde el registro duradero. El usuario no reaproba cosas que ya aprobaron. Las llamadas LLM ya hechas no se refacturan.
  China:有持久执行时:运行从最近检查点恢复──已完成活动不重新执行; 其结果从持久日志重放──用户不重新批准已批准的事──已做的LLM 调用不重新计费──

Este es el mismo patrón que los motores de flujo de trabajo han enviado durante una década (Temporal, Cadence, Cherami de Uber). Lo nuevo es que las llamadas de LLM son ahora una especie de actividad  no determinista, cara, con efectos secundarios  y encajan en este patrón limpiamente.

> Es el mismo modelo que el de la década de la producción de motores de trabajo (Temporal, Cadence, Uber's Cherami) ⋅ Lo nuevo es que el LLM 调用现在是一种 actividad不确定性,昂贵,有副作用它们干净地契合于这个模式──

> **【中文解读】**持久化执行解决长程 经纪人的可靠性问题:四小时运行中主机重启时,朴素循环丢失一切( herramientas re-execution、用户重新审批、LLM 重新计费), mientras que 持久化执行从最近检查点恢复,已完成的活动从持久日志重放而不是重执行──Temporal OpenAI Agents SDK 集成于2026年3月 GA──核心洞察:LLM调用是一种不确定性、昂贵、有副作用活动,完美适应工作流引擎的模式──

El tema de la lección: la fiabilidad de largo horizonte se desacelera (METR observa una "degradación de 35 minutos"  la tasa de éxito disminuye aproximadamente cuadráticamente con el horizonte).

> El tema de este curso es: "Desacuación de la fiabilidad de los archivos de la Metr" (METR)  Observación de "35 minutos de decadencia"  tasa de éxito con la línea de tiempo                                                                                                                                                                                                                                     

## El concepto central.

### Actividades, flujos de trabajo y reproducción.

- **Workflow**El código de orquestación determinista define la secuencia de actividades, las ramas, las esperas. Debe ser determinista para que pueda reproducirse del registro de eventos sin divergencias sorprendentes.
  En inglés:**工作流**La definición de la secuencia de actividades, las secciones, las expectativas, las diferencias, las diferencias y las diferencias de los eventos.
- **Activity**Un programa de trabajo de la empresa de gestión de datos (LLC) es una unidad de trabajo no determinista, potencialmente fallida. llamada de LLM, llamada de herramienta, escritura de archivos, solicitud HTTP. Cada actividad se registra con sus entradas y (una vez completada) sus salidas.
  En inglés:**活动**:Incertidity、可能失败的工作单元──LLM 调用、工具调用、文件写、HTTP 请求── cada actividad registra su entrada y
- **Event log**Cada actividad se inicia, completa, falla, vuelve a intentar y se registra cada decisión del flujo de trabajo.
  En inglés:**事件日志**Cada actividad comienza, termina, fracasa, vuelve a intentarse y cada decisión del proceso de trabajo se registra.
- **Replay**En el proceso de recuperación, el código del flujo de trabajo se ejecuta de nuevo desde el principio; cada actividad que ya se haya completado devuelve su resultado registrado sin volver a ejecutarse.
  En inglés:**重放**Cuando se recupera, el código de trabajo se vuelve a ejecutar; cada actividad finalizada regresa a su registro y no se vuelve a ejecutar.

Esta es la misma forma que React que se vuelve a renderizar contra un DOM virtual, o Git reconstruyendo un árbol de trabajo a partir de commits.

> Esto es similar a React  en relación con la DOM re-renovación virtual o Git desde la forma del árbol de trabajo de re-construcción de la presentación                                                                                                                                                                                                                                            

### ¿Por qué LLM llamadas encajan en el patrón por qué LLM                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             

Las convocatorias de LLM son:

> LLM 调用是:

- No determinista (temperatura > 0; incluso la temperatura 0 fluye entre las versiones del modelo).
  La temperatura del agua se desplaza a un nivel de temperatura de 0 a 0 °C.
- Es caro (dinero y latencia).
  El dinero y la demora.
- Potencialmente fallido (limites de tasas, tiempo de espera).
  En inglés, el número de personas que han perdido la oportunidad de ganar la oportunidad de ganar la oportunidad de ganar la oportunidad de ganar la oportunidad de ganar la oportunidad de ganar la oportunidad de ganar la oportunidad de ganar la oportunidad de ganar la oportunidad de ganar la oportunidad de ganar la oportunidad de ganar la oportunidad de ganar la oportunidad de ganar la oportunidad de ganar la oportunidad de ganar la oportunidad de ganar la victoria.
- Efecto secundario (si invocan herramientas).
  En inglés, "se puede usar un instrumento de control".

Esta es exactamente la actividad del perfil. Envuelva cada llamada LLM como una actividad le da volver a intentar con retroceso exponencial, control de puntos a través de reinicios, y un rastro replayable para el desarreglamiento.

> Este es el archivo de actividades. Cada LLM  modificar el envase para actividades para darte un índice de retorno de pruebas 跨重启检查点和可重放调试追踪.

### Puntos de control seleccionados por `thread_id`¿ Qué es esto ?`thread_id`Por el punto de control clave

LangGraph, Microsoft Agent Framework, Cloudflare Durable Objects y Claude Code Routines convergieron en la misma forma de API: un `thread_id`(o equivalente) identifica la sesión; cada transición de estado persiste a un backend (postgreSQL predeterminado, SQLite para dev, Redis para caché); el currículum lee el último punto de control.

> LangGraph, Microsoft Agent Framework, Cloudflare Durable Objects y Claude Code Routines recibieron el mismo formato de API:`thread_id`(o igual precio) Identificación de conversaciones; cada estado se transforma en el último de los últimos puntos de control;

La elección del final es importante:

> 后端选择重要:

- **PostgreSQL**Es duradero, consultable, sobrevive a los despliegues.
  En inglés:**PostgreSQL**El programa de investigación de la ONU sobre la seguridad y la seguridad de los trabajadores en el sector de la salud
- **SQLite**: solo local-dev; pierde datos en todos los hosts.
  En inglés:**SQLite**: sólo en el desarrollo; transversales de los datos.
- **Redis**: rápido pero efímero, a menos que se configure AOF/snapshot.
  En inglés:**Redis**:快但临时, excepto la configuración AOF/快照。
- **Cloudflare Durable Objects**: distribuido de forma transparente; escalzado por una llave única; sobrevive durante horas o semanas.
  En inglés:**Cloudflare Durable Objects**: transparente distribuido; en un único rango de clave; sobrevivientes de un número de horas a un número de semanas.

### La entrada humana como un estado de primera clase.

Proponer y luego comprometerse (lección 15) requiere un estado duradero de "espera a los humanos". El flujo de trabajo se detiene, la cola externa sostiene la solicitud pendiente y la aprobación se reanuda exactamente desde ese punto.

> Proponer-entonces-comprometerse (第 15 课) necesita mantenerse en el estado de "esperar a la humanidad" . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .

### La degradación de 35 minutos 35 minutos disminución.

METR observó que cada clase de agentes medida muestra una degradación de fiabilidad más allá de ~ 35 minutos de operación continua.

> METR  Observación de cada medida  Clasificación de agentes en aproximadamente 35 minutos de funcionamiento continuado mostró una disminución de la fiabilidad 

El doble de duración de la tarea aproximadamente cuadruplica la tasa de fallas. La ejecución duradera no corrige esto; le permite correr más tiempo de lo que soporta el perfil de fiabilidad. El patrón seguro es combinar la durabilidad con los puntos de control que requieren HITL fresco en la reentrada, y con interruptores de eliminación de presupuesto (lección 13) que limitan el cálculo total independientemente del tiempo del reloj de pared.

> El tiempo de tarea duplica aproximadamente el porcentaje de fracaso de cuatro veces. El tiempo de ejecución de una tarea no se repite por más tiempo. El modo de seguridad es unirse a la durabilidad y a la reingreso de nuevos HITL.

### Cuando la ejecución duradera es la respuesta equivocada.

- Las carreras son más cortas que unos minutos sin intervención humana.
  China: 短于几分钟无人输入的运行──开销 > 收益──
- Recuperación de información estrictamente de lectura.
  En inglés, "Creo que el lenguaje es un lenguaje que se utiliza para la lectura de información".
- tareas en las que la corrección requiere de un extremo a otro dentro de una ventana de contexto (algunas tareas de razonamiento; algunas generaciones de una sola toma).
  China Translation: correctamente es necesario realizar una tarea dentro de una ventana de la siguiente página:

## Usalo con el marco de ejecución
```figure
memory-consolidation
```

## Usalo

`code/main.py`Implementa un motor de ejecución duradera mínima en stdlib Python.

> `code/main.py`Utiliza la base de Python 实现 el motor de ejecución de duración mínima.

- `@activity`decorador que registra entradas y salidas en un registro de eventos JSON.
  En inglés:`@activity`装饰器将输入输出记录到 JSON 事件日志。
- Una función de flujo de trabajo que secuencia las actividades.
  La función de trabajo de la organización de actividades.
- ¿ Qué es esto ?`run_or_replay(workflow, event_log)`Función que reproduce las actividades completadas sin volver a ejecutarlas.
  En inglés:`run_or_replay(workflow, event_log)`函数重放已完成活动而不重新执行──

El conductor simula un flujo de trabajo de tres actividades, se estrella a mitad de camino, y muestra (a) un ingenuo retiro re-executivo de todo frente a (b) una repetición que ejecuta sólo la actividad que falta.

> 驱动器模拟三活动工作流,中途崩,展示 (a) 朴素重试重新执行一切 vs (b) 重放只运行缺失活动──

## Envíe el producto .

`outputs/skill-durable-execution-review.md`revisa el despliegue de agentes de larga duración propuesto para determinar la forma correcta de ejecución duradera: actividades, determinismo, backend de los puntos de control, estado de entrada humana y política de HITL-on-resume.

> `outputs/skill-durable-execution-review.md`审查提议长时运行 署的正确持久执行形状: actividad, determinación, punto de control y posterior final, estado de entrada y recuperación humana  HITL estrategia

## Los ejercicios.

1. - ¿ Qué ?`code/main.py`Observe la diferencia en el recuento de actividad-execución entre la repetición y la repetición ingenuas. Cambia el punto de choque y muestra los cambios en el recuento de repetición en consecuencia.
   Traducción:运行`code/main.py`◊ observar la simple comprobación y la reapertura de actividades de ejecución de la comprobación de cambios.

2. Convierta el motor de juguete para usarlo `thread_id`Simula dos sesiones simultáneas compartiendo el motor y confirma que sus registros de eventos no chocan.
   China:将玩具引擎转为显式使用`thread_id`◊ 模拟共享引擎的两个并发会话并确认其事件日志不冲突──

3. Tomar una actividad en el motor de juguete. Introducir un no-determinismo (un sello de tiempo de un reloj de pared dentro de una decisión de flujo de trabajo). Demostrar la divergencia en la repetición. Explicar cómo los motores reales manejan esto (registro de efectos secundarios, `Workflow.now()`Las API).
   En español, el nombre de la máquina de jugar es "Introduce un movimiento": "Introduce un movimiento": "Introduce un movimiento": "Introduce un movimiento": "Introduce un movimiento": "Introduce un movimiento": "Introduce un movimiento": "Introduce un movimiento": "Introduce un movimiento": "Introduce un movimiento": "Introduce un movimiento": "Introduce un movimiento": "Introduce un movimiento": "Introduce un movimiento": "Introduce un movimiento": "Introduce un movimiento": "Introduce un movimiento": "Introduce un movimiento": "Introduce un movimiento": "Introduce un movimiento": "Introduce un movimiento": "Introduce un movimiento": "Introduce un movimiento": "Introduce un movimiento": "Introduce un movimiento": "Introduce un movimiento": "Introduce un movimiento": "Introduce un movimiento": "Introduce un movimiento": "Introduce un movimiento": "Introduce" ("Introduce" significa que significa que significa que significa que "Introduceeds" significa que significa que significa que significa que "Introduceeds un movimiento" ("Introduceeds into un movimiento" significa que significa que significa que significa que significa que significa que significa que significa que significa que significa que significa que significa que significa que significa que significa que significa que significa que significa que significa que significa que significa que significa que significa que significa que significa que significa que significa que significa que significa que significa que significa que significa que significa que significa que significa que significa que significa que significa que significa que significa que significa que significa que significa que significa que significa que significa que significa que significa que significa que significa que "es que significa que significa que "es que significa que "es que es que "es que es que es que es que es que es que es que es que es que es que es que es que es que es que es que es que es que es que es que es que es que es que es que es que es que es que es que es`Workflow.now()`API) 

4. Lea el post de LangChain "Runtime behind production deep agents" en el que se enumera cada estado en el que persiste el tiempo de ejecución y se nombra el modo de falla que cubre cada uno.
   La cadena de producción de los agentes profundos de la producción de LangChain fue lanzada en el año pasado.

5. Diseñar una política de punto de control para una tarea de codificación autónoma de 6 horas. ¿Dónde se hace el punto de control? ¿Cómo se ve el resumen en desfase? ¿Qué requiere HITL fresco?
   Por qué no se ha hecho un nuevo HITL?

## Términos clave .

| Term | What people say | What it actually means |
|---|---|---|
| 术语 | 通俗说法 | 实际含义 |
| Workflow | "Agent's script" | Deterministic orchestration code; replayable from event log |
| 工作流 | "Agent 的脚本" | 确定性编排代码；可从事件日志重放 |
| Activity | "A step" | Non-deterministic unit (LLM call, tool call); logged before and after |
| 活动 | "一步" | 非确定性单元（LLM 调用、工具调用）；前后记录 |
| Event log | "The backing store" | Durable record of every state transition |
| 事件日志 | "后端存储" | 每个状态转换的持久记录 |
| Replay | "Resume" | Re-run workflow; completed activities return logged results without re-execution |
| 重放 | "恢复" | 重跑工作流；已完成活动返回记录结果而不重新执行 |
| Checkpoint | "Save point" | Persisted state keyed by thread_id; latest-wins on resume |
| 检查点 | "保存点" | 以 thread_id 为键的持久状态；恢复时最新优先 |
| thread_id | "Session key" | Identifier that scopes durable state |
| thread_id | "会话键" | 范围化持久状态的标识符 |
| 35-minute degradation | "Reliability decay" | METR: success rate drops ~quadratically with horizon |
| 35 分钟衰减 | "可靠性衰减" | METR：成功率与时间线大致平方反比下降 |
| Non-determinism | "Drift on replay" | Wall clock, random, LLM output; must be registered as side effect |
| 非确定性 | "重放漂移" | 墙钟、随机、LLM 输出；必须注册为副作用 |

## Más Leer más Leer más

- [Anthropic — Claude Code Agent SDK: agent loop](https://code.claude.com/docs/en/agent-sdk/agent-loop) presupuesto, giros y semántica de reanudación.
  Traducción: presupuesto, ciclo y recuperación
- [Microsoft — Agent Framework: human-in-the-loop and checkpointing](https://learn.microsoft.com/en-us/agent-framework/workflows/human-in-the-loop) Forma de solicitud de información.
  En el caso de los niños, el número de niños en edad avanzada es de aproximadamente un millón.
- [LangChain — The Runtime Behind Production Deep Agents](https://www.langchain.com/conceptual-guides/runtime-behind-production-deep-agents) requisitos concretos de tiempo de ejecución.
  En español, "condicionado" significa "condicionado".
- [OpenAI Agents SDK + Temporal integration (Trigger.dev announcement)](https://trigger.dev) Forma de actividad para las convocatorias de LLM.
  En el caso de los estudiantes de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de los los los los los
- [Anthropic — Measuring agent autonomy in practice](https://www.anthropic.com/research/measuring-agent-autonomy) la referencia de degradación de 35 minutos.
  En el caso de los niños, el tiempo de vida es de aproximadamente un año.
