# Bloques de memoria y tiempo de sueño (Letta) 記憶块与休眠計算 (Letta)
# Bloques de memoria y cálculo del tiempo de sueño

> Un modelo puede editar directamente un bloqueo de memoria funcional discreto, y un agente del tiempo de sueño que consolida la memoria sincrónicamente mientras el agente principal está inactivo.

> **【中文解读】**MemGPT en 2024 se convirtió en Letta. El desarrollo de 2026 aumentó dos ideas: el modelo puede editar directamente los bloques de memoria de funciones descentralizadas, y el agente de sueño de la memoria en el agente principal 空时异步合并记忆.

**Type:** Build | **类型:** 构建
**Languages:** Python (stdlib) | **语言:** Python (标准库)
**Prerequisites:** Phase 14 · 07 (MemGPT) | **前置知识:** Phase 14 · 07 (MemGPT)
**Time:** ~75 minutes | **时间:** ~75 分钟

## Objetivos de aprendizaje

- Nombre de los tres niveles de memoria que utiliza Letta (núcleo, recuerdo, archivo) y el papel de cada uno.
  La lengua inglesa se utiliza para el uso de la lengua inglesa.
- Explica el patrón de bloqueo de memoria: bloque humano, bloque Persona y bloques definidos por el usuario como objetos de primera clase.
  China: 藏语: 藏语: 藏语: 藏语: 藏语: 藏语: 藏语: 藏语: 藏语: 藏语: 藏语: 藏语: 藏语: 藏语: 藏语: 藏语: 藏语: 藏语: 藏语: 藏语: 藏语: 藏语: 藏语: 藏语: 藏语: 藏语: 藏语: 藏语: 藏语: 藏语: 藏语: 藏语: 藏语: 藏语: 藏语: 藏语: 藏语: 藏语: 藏语: 藏语: 藏语: 藏语: 藏语: 藏语: 藏语: 藏语: 藏语: 藏语: 藏语: 藏语: 藏语: 藏语: 藏语: 藏语: 藏语: 藏语: 藏语: 藏语: 藏语: 藏语: 藏语: 藏语: 藏语: 藏语: 藏语: 藏语: 藏语: 藏语: 藏语: 藏语: 藏语: 藏语: 藏语: 藏语: 藏语: 藏语: 藏语: 藏语: 藏语: 藏语: 藏语: 藏语: 藏语: 藏语: 藏语: 藏语: 藏语: 藏语: 藏语: 藏语: 藏语: 藏
- Describa lo que es la computación del tiempo de sueño, por qué se encuentra fuera del camino crítico y por qué puede ejecutar un modelo más fuerte que el agente principal.
  China Translation: describe休眠計算是什么,为什么它在关键路径之外,为什么它可以运行比主代理更强的模型.
- Implemente un bucle de dos agentes scripted donde un agente principal sirve respuestas y un agente de tiempo de sueño consolida bloques entre turnos.
  Traducción: "Aumentar un ciclo de dos agentes guionados, agente principal, agente de respuesta, agente de descanso en la rotación".

## El problema es la introducción del problema

MemGPT (lección 07) resolvió el flujo de control de memoria virtual. Surgieron tres problemas de producción:

> MemGPT (第 7 课) resolvió el flujo de control de la memoria virtual. Surgieron tres problemas de producción:

1. **Latency.**Cada operación de memoria se encuentra en el camino crítico. Si el agente tiene que recortar, resumir o reconciliar mientras el usuario espera, la latencia de cola explotará.
   En inglés:**延迟。**Cada operación de memoria está en un camino clave. Si el agente tiene que cortar un resumen o coordinarlo mientras el usuario espera, el final se retrasa.
2. **Memory rot.**Los escritos se acumulan, los hechos contradictorios permanecen, la recuperación se ahoga en el contenido obsoleto.
   En inglés:**记忆腐化。**写入积累――矛盾的事实保留――检索被过时内容淹没―― y el contenido de la investigación fue inundado en el pasado.
3. **Structure loss.**Una tienda de archivos plana no puede expresar "el bloque humano siempre está en el prompt; el bloque Persona siempre está en el prompt; el bloque de tareas cambia por sesión".
   En inglés:**结构丢失。**平的归档存储不能表达"Human 块始终在提示中;Persona 块始终在提示中;Task 块按会话交换――"

Letta (letta.com) es el nombre de la plataforma el proyecto MemGPT original adoptado en 2024  el patrón del papel mantiene el nombre MemGPT  y la reescritura de 2026 Letta V1 es un paso posterior y separado.

> Letta (en inglés) es una nueva versión de 2026: un bloque de memorias hace que la estructura se manifieste.

> **【中文解读】**记忆块 (memoria bloques) y休眠计算 (Huy-Time Computing) son dos estrategias de optimización de MemGPT/Letta. 记忆块 es un segmento de texto de gran tamaño fijo, similar a la página de memoria, utilizado para controlar con precisión la proporción de todo tipo de información en la ventana de texto. 休眠计算指指在用户不活跃时预处理和压缩记忆,减少下次会话的延迟.

> **【拓展：Letta 的演进】**Letta (en inglés: Letta, original MemGPT) introdujo en la evolución de 2024-2025 dos conceptos clave de memoria y de cálculo de descanso.

> ¿ Qué es esto ?**【前置】**必須先通過Fase 14·07 (MemGPT) 本節是它的直接延續──如果你不理解 MemGPT's"主上下文 vs 外部上下文"的二层模型,那么 Letta's三层 (core/recall/archival) 扩展会把你搞──

## El concepto central.

### Tres niveles

| Tier | Scope | Where it lives | Written by |
|------|-------|----------------|------------|
| 层级 | 范围 | 存储位置 | 写入者 |
| Core | Always visible | Inside the main prompt | Agent tool call + sleep-time rewrites / Agent 工具调用 + 休眠重写 |
| Recall | Conversation history | Retrievable | Automatic turn logging / 自动轮次日志 |
| Archival | Arbitrary facts | Vector + KV + graph | Agent tool call + sleep-time ingest / Agent 工具调用 + 休眠摄取 |

El núcleo es el núcleo MemGPT. Recuerda es el amortiguador de conversación con su cola desalojada.

> El núcleo es el núcleo de MemGPT. Recuerdo es el diálogo de la parte posterior de la expulsado. Arquivo es el almacenamiento externo. Este despliegue ha resuelto la sobrecarga de MemGPT de dos niveles.

### Bloques de memoria

Un bloque es una sección tipada, persistente y editable del nivel principal.

> El bloque es la tipificación de la capa central, la perdurada, la editable.

- **Human block** hechos sobre el usuario (nombre, función, preferencias, objetivos).
  En inglés:**Human 块** Sobre el hecho de usuario (姓名,角色,偏好,目标)
- **Persona block** el concepto de sí mismo del agente (identidad, tono, restricciones).
  En inglés:**Persona 块**Agent's ego concept (se-o-o-o-o-o-o-o-o-o-o-o) 身份、语气、约束) 

Letta generaliza a bloques definidos por el usuario: a `Task`bloque para el objetivo actual, un `Project`bloque de datos de base de código, una `Safety`bloque para restricciones duras. Cada bloque tiene un`id`¿ Qué ?`label`¿ Qué ?`value`¿ Qué ?`limit`(capítulo de carácter), `description`(para que el modelo sepa cuándo editarlo).

> Letta 泛化为任意用户定义块:用于当前目标的 `Task`块、 para usar los hechos de la código `Project`块、 para usar en el duro`Safety`块── cada uno tiene `id`¿Qué es esto?`label`¿Qué es esto?`value`¿Qué es esto?`limit`(字符上限)`description`(让模型知道何时编辑它)

Los bloques se pueden editar a través de la superficie de la herramienta:

> 块通过工具接口可编辑:

- `block_append(label, text)`
  En inglés:`block_append(label, text)`向块追加文本──
- `block_replace(label, old, new)`
  En inglés:`block_replace(label, old, new)`替换块中的文本──
- `block_read(label)`
  En inglés:`block_read(label)`读取块内容──
- `block_summarize(label)` condensa un bloque que está cerca de su límite.
  En inglés:`block_summarize(label)` comprimir cerca de la límite de bloques

### Computación del tiempo de sueño

La adición 2025 Letta: ejecutar un segundo agente en el fondo, fuera de la ruta crítica.`learned_context`en bloques compartidos, y consolidar o invalidar los registros de archivo.

> 2025 Letta's new addition function: en el segundo funcionamiento en el segundo ejecutivo, no en el camino clave.`learned_context`写入共享块,并合并或使归档记录失效──

Propiedades que se desprenden:

> 随之产生的 características:

- **No latency cost.**Las respuestas primarias no esperan a las operaciones de memoria.
  En inglés:**无延迟成本。**主响应不等待记忆操作──
- **Stronger model allowed.**El agente de tiempo de sueño puede ser un modelo más caro y más lento porque no tiene limitaciones de latencia.
  En inglés:**允许更强的模型。**El agente de sueño puede ser un modelo más caro, más lento, porque no se limita a retrasos.
- **Natural consolidation window.**Dedup, resumir, invalidar hechos contradictorios cuando el usuario no está esperando.
  En inglés:**天然的合并窗口。**En el momento en que el usuario no espera, el resumen se vuelve a hacer imposible.

La forma coincide con cómo trabajan los humanos: haces la tarea, duermes en ella, la memoria a largo plazo se calma durante la noche.

> ¿ Qué es esto ?**【类比】**Computación del tiempo de sueño 像夜晚的清洁工:白天你(主代理) ocupado en responder a los clientes, oficinas(主上下文)堆满今天的会议记录、文件、咖啡杯;晚晚清洁工(睡眠时间代理)进来擦桌子、归档文件、把"明天要跟进的事"贴到便利贴上(写入人/任务块) ・・・第二天你来上班,看整洁待的桌面和清晰的办理清单──**关键**: limpieza puede ser lenta, lo más caro puede ser con un modelo más fuerte, porque el cliente no está esperando.

> Esta forma de trabajo es compatible con el trabajo humano: tu haces tareas, tu duermes, el recuerdo de larga duración en la noche.

### Letta V1 y el razonamiento nativo
### Razonamiento nativo

Letta V1 (`letta_v1_agent`, 2026) se desactiva `send_message`/bate del corazón y en línea `Thought:`Las aplicaciones de respuesta y mensajes (OpenAI) emiten el razonamiento en un canal separado, pasando por turnos (cifrados entre los proveedores en producción). El bucle de control es todavía ReAct.

> Letta V1`letta_v1_agent`,2026) se ha abandonado.`send_message`/ corazón saltar y dentro `Thought:`En el contexto de la producción, el ciclo de control sigue siendo un proceso de reacción.

### Cuando este patrón va mal

> ️ **【易错点】**"静默漂移" es el error más peligroso de Letta 部署: el agente del sueño en el segundo plano ha cambiado el personaje 块 (por ejemplo, "始终使用中文回复"改成"中英文混用"), pero el agente principal no sabe.**后果**: el usuario encuentra que el comportamiento del agente cambia pero no encuentra una causa porque el diario de conversación sólo registra las salidas del agente principal.**一行修复**: Cada vez que duerme, escribe y bloquea el contenido, y en la siguiente ronda del agente principal, le pide que se introduzca un bloque que cambia desde la última vez:

- **Block bloat.**Infinito .`block_append`Si el bloque llega al límite, debe enviar un resumen de bloque antes de escribir.
  En inglés:**块膨胀。** Infinito `block_append` rápidamente alcanzar el límite superior                                                                                                                                                                                                                                                            
- **Silent drift.**El agente del sueño reescribe un bloque y el agente principal nunca se da cuenta.
  En inglés:**静默漂移。**Agente de descanso Reescribir bloques pero el principal Agente de no se ha dado cuenta.
- **Poisoned consolidation.**El agente del sueño procesa el contenido accesible al atacante en el núcleo.
  En inglés:**投毒合并。**El agente de sueño procesará el contenido del atacante en el núcleo.

> ¿ Qué es esto ?**【困惑】**P: ¿Por qué es más costoso usar un modelo más fuerte en el sueño? ¿Por qué es más costoso ahorrar dinero en lugar de quemarlo? A:**避开了关键路径的高价** Agente principal  debe utilizar streaming + alta prioridad, el precio único es de 2-3 veces el lote.

## Construye con movimiento.
```figure
memory-blocks
```

## Construye el mismo

`code/main.py`los instrumentos:

> `code/main.py`实现:

- `Block` identificación, etiqueta, valor, límite, descripción.
  En inglés:`Block`id、etiqueta、valor、limitamento、descripción。
- `BlockStore` CRUD + `near_limit(label)`¿Qué es eso?
  En inglés:`BlockStore`CRUD + `near_limit(label)`辅助方法── también
- Dos agentes con guión  `PrimaryAgent`sirve un turno, `SleepTimeAgent`se consolida entre los turnos.
  Traducción:Dos guiones Agente`PrimaryAgent`提供轮次,`SleepTimeAgent`En la siguiente ronda.
- Un rastro que muestra una conversación de tres vueltas con el bloque escribe, más un pase de tiempo de sueño que resume un bloque e invalida un hecho anticuado.
  China: exhibición de tres rondas de diálogo con bloques de escritura, además de bloques de compresión y el tratamiento de los hechos del pasado en forma inadecuada.

- ¿Qué quieres decir ?

> 运行:

```
python3 code/main.py
```

La transcripción muestra la división: los giros primarios son rápidos y producen escritos crudos; el paso del sueño se compacta y limpia.

> 转录记录显示分工:主轮次快速产生原始写入;休眠处理压缩和清理──

## Usalo con el marco de ejecución

- **Letta**(letta.com) para la implementación de referencia.
  En inglés:**Letta**(letta.com) Referir a la realización.
- **Claude Agent SDK skills**como conocimiento en forma de bloque  una habilidad es un bloque de instrucciones nombrado, versionado y recuperable que el agente carga a pedido.
  En inglés:**Claude Agent SDK skills**Como bloque de conocimiento habilidad es denominado  versionamiento  instrucciones de bloque de control, agente 按需加载
- **Custom builds**Para los equipos que quieren controlar el backend de almacenamiento, utilice el contrato de Letta API para poder migrar más tarde.
  En inglés:**自定义构建** Adaptado para controlar el almacenamiento posterior del equipo.

## Envíe el producto .

`outputs/skill-memory-blocks.md`genera un sistema de bloque en forma de Letta con ganchos de hora de dormir para cualquier tiempo de ejecución, incluidas las reglas de seguridad y el cableado de citación.

> `outputs/skill-memory-blocks.md`Para cualquier operación, se genera un sistema de bloques de forma Letta, con reglas de seguridad y conexión de referencia.

## Los ejercicios.

1. Añadir un`block_summarize`herramienta que sustituye el valor de bloque por un resumen generado por el modelo cuando `near_limit`¿Cuál umbral de activación minimiza tanto las llamadas de resumen como el desbordamiento de bloque?
   En inglés:`block_summarize`工具, en `near_limit`返回 true 时使用模型生成的摘要替换块值──哪个触发值最小化摘要调用和块溢出? 返回 true 时使用模型生成的摘要替换块值. 什么触发值最小化摘要调用和块溢出?
2. Implementar deducción del tiempo de sueño sobre el archivo: dos registros cuyo texto tiene un superposición simbólica de > 90% se derrumban a uno.
   En el archivo de archivos, se realiza el repositorio de repositorios de repositorios de repositorios de repositorios de repositorios de repositorios de repositorios de repositorios de repositorios de repositorios de repositorios de repositorios de repositorios de repositorios de repositorios de repositorios de repositorios de repositorios de repositorios de repositorios de repositorios de repositorios de repositorios de repositorios de repositorios de repositorios de repositorios de repositorios de repositorios de repositorios de repositorios de repositorios de repositorios de repositorios de repositorios de repositorios de repositorios de repositorios de repositorios de repositorios de repositorios de repositorios de repositorios de repositorios de repositorios de repositorios de repositorios de repositorios de repositorios de repositorios de repositorios de repositorios de repositorios de repositorios de repositorios de repositorios de repositorios de repositorios de repositorios de repositorios de repositorios de repositorios de repositorios de repositorios de repositorios de repositorios de repositorios de repositorios de repositorios de repositorios de repositorios de repositorios de repositorios repositorios de repositorios de repositorios repositorios de repositorios repositorios de repositorios de repositorios de repositorios repositorios de repositorios en repositorios repositorios de repositorios repositorios repositorios de repositorios de repositorios en repositorios de repositorios repositorios de repositorios en repositorios en repositorios repositorios repositorios.
3. Bloques de versiones. En cada registro de escritura el valor antiguo y una diferencia. Exponer `block_history(label)`Así que los operadores pueden deshacerse de "por qué el agente olvidó X".
   Traducción:Version化块── Cada vez que escribe un registro de valores y diferencias──exposición `block_history(label)`¿Por qué el agente se olvidó de X?
4. Trate a los agentes de horas de sueño como escritores no confiables. Cuando toquen el bloque Persona o Seguridad, requieren una revisión de segundo agente antes de comprometerse.
   Cuando los agentes tocan a la persona o el bloque de seguridad, se debe presentar un segundo informe.
5. Portar el ejemplo para utilizar la API Letta (`letta_v1_agent`¿Qué cambios hay en el esquema de bloques, y cómo el razonamiento nativo altera la forma de las huellas?
   La versión de Letta se puede utilizar en el caso de Letta API.`letta_v1_agent`¿Qué cambios han ocurrido en el modelo de bloques? ¿Cómo ha cambiado el modelo de trayectoria?

## Términos clave .

| Term | What people say | What it actually means |
|------|-----------------|-----------------------|
| 术语 | 通俗说法 | 实际含义 |
| Memory block | "Editable prompt section" / "可编辑提示分区" | Typed, persistent, LLM-editable segment of core memory / 类型化、持久化、LLM 可编辑的核心记忆段 |
| Human block | "User memory" / "用户记忆" | Facts about the user, pinned in core / 关于用户的事实，固定在 core 中 |
| Persona block | "Agent identity" / "Agent 身份" | Self-concept, tone, constraints, pinned in core / 自我概念、语气、约束，固定在 core 中 |
| Sleep-time compute | "Async memory work" / "异步记忆工作" | Second agent doing consolidation off the critical path / 第二个 Agent 在关键路径之外做合并 |
| Core / Recall / Archival | "Tiers" / "层级" | Three-layer memory split: always-visible / conversation / external / 三层记忆拆分：始终可见 / 对话 / 外部 |
| Block limit | "Cap" / "上限" | Character limit per block; forces summarization / 每个块的字符限制；强制摘要 |
| Native reasoning | "Thinking channel" / "思考通道" | Provider-level reasoning output, not prompt-level `Thought:` / 提供商级推理输出，非提示级 `Thought:` |
| Learned context | "Sleep output" / "休眠输出" | Facts the sleep-time agent writes into shared blocks / 休眠 Agent 写入共享块的事实 |

## Más Leer más Leer más

- [Letta, Memory Blocks blog](https://www.letta.com/blog/memory-blocks) el patrón de bloque
  La versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de
- [Letta, Sleep-time Compute blog](https://www.letta.com/blog/sleep-time-compute) Consolidación sin sincronizada
  La traducción del inglés en inglés es: Letta 休眠计算博客异步合并──
- [Letta, Rearchitecting the Agent Loop](https://www.letta.com/blog/letta-v1-agent) Reescribir el razonamiento nativo
  Traducción:Letta 重建 Agent 循环博客原生推理重写。
- [Packer et al., MemGPT (arXiv:2310.08560)](https://arxiv.org/abs/2310.08560) el origen
  En el contexto de la historia de la historia, el mundo se ha convertido en un mundo de la ciencia.
