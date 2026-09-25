# Memoria: Contexto Virtual y MemGPT                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                   
# Memoria de agente  Contexto virtual y páginas de memoria

> Las ventanas de contexto son finitas. Las conversaciones, documentos y rastros de herramientas no son. La solución es la memoria virtual del sistema operativo re-estabilizada.

> **【中文解读】**La siguiente ventana es limitada, pero el diálogo, archivos y trayectoria de herramientas no es. MemGPT comparará este tipo de datos con el sistema operativo RAM, el almacenamiento externo es el disco, el agente entre ambos cambiará de página. Este es el modelo de herencia de todos los sistemas de memoria en 2026.

**Type:** Build | **类型:** 构建
**Languages:** Python (stdlib) | **语言:** Python (标准库)
**Prerequisites:** Phase 14 · 01 (Agent Loop), Phase 14 · 06 (Tool Use) | **前置知识:** Phase 14 · 01 (Agent 循环), Phase 14 · 06 (工具使用)
**Time:** ~75 minutes | **时间:** ~75 分钟

## Objetivos de aprendizaje

- Explica la analogía del sistema operativo en la que MemGPT se basa: contexto principal = RAM, contexto externo = disco, herramientas de memoria = página de entrada/salida.
  En el contexto de la memoria, el sistema operativo de memoria se basa en la memoria de memoria.
- Implemente el patrón MemGPT de dos niveles en stdlib con un buffer de contexto principal, una tienda de búsqueda externa y herramientas de entrada/salida de página.
  Con el estándar de la biblioteca se realiza dos niveles de MemGPT 模式, contiene el principal sobre la siguiente siguiente siguiente:缓冲区、外部可搜索存储和页面换进/换出工具──
- Describa cómo el agente emite "interrumpe" para consultar o modificar la memoria externa y cómo el resultado se inserta de nuevo en el siguiente aviso.
  En inglés, el nombre de la persona que se encuentra en el registro de la memoria externa es "Agent" (Agent) y se utiliza para describir cómo se ha emitido la "interrupción" para consultar o modificar la memoria externa, así como cómo se ha escrito el resultado en el siguiente mensaje.
- Identifique las opciones de diseño MemGPT que llevan a Letta (lección 08) y Mem0 (lección 09).
  El texto original de la MemGPT se traduce en inglés como MemGPT.

## El problema es la introducción del problema

Las ventanas de contexto parecen resolver la memoria. No lo hacen. Tres modos de falla se repiten en la producción:

> La primera ventana parece poder resolver el problema de la memoria, pero en realidad no puede. En el entorno de producción aparecen repetidamente tres modelos de fracaso:

1. **Overflow.**Las conversaciones de varios turnos, documentos largos o trayectorias pesadas en herramientas cruzan la ventana.
   En inglés:**溢出。**Muchos diálogos, archivos o herramientas de diálogo se han perdido en el transcurso de la ventana.
2. **Dilution.**Incluso dentro de la ventana, llenar un contexto irrelevante diluye la atención sobre lo que importa.
   En inglés:**稀释。**Incluso en la ventana, el relleno no está relacionado con el texto anterior también deja de ser el punto de partida del contenido importante.
3. **Persistence.**Una nueva sesión comienza con una ventana vacía, y los agentes sin memoria externa no pueden decir "recuerde cuando me pediste"...
   En inglés:**持久化。**Nueva conversación comenzó desde la ventana vacía. Sin memoria externa, el agente no pudo atravesar la conversación diciendo: "Recuerda que me dejaste"....

> **【中文解读】**La primera es que el proceso de producción de la producción de la producción de material se ha desarrollado de manera que el proceso de producción de la producción de material no se ha desarrollado de manera efectiva.

Los ventanas más grandes ayudan pero no arreglan esto. Mem0 2025 documento midió que las líneas de base de 128k ventanas todavía faltan los hechos de largo horizonte que un agente de 4k ventanas con memoria externa captura.

> Más ventanas grandes ayudan pero no pueden resolver este problema. MEM0 de 2025 artículo de medición de la conclusión, 128k de las ventanas de la línea de base todavía se perderá 4k de las ventanas + de la memoria externa agente 能捕获的长程事实──

> **【拓展：MemGPT → 现代 Agent 记忆系统】**MemGPT (Packer et al., 2023) va a poner en el siguiente modo de gestión de los datos en el sistema operativo: memoria virtual: RAM, memoria externa = disco, memoria = página cambiada en cambio. Este es el modelo básico de todos los sistemas de memoria de 2026 años.

> ¿ Qué es esto ?**【前置】**必须先掌握:Fase 14·01(Agent Loop) MemGPT的记忆工具是普通工具调用的扩展;Fase 14·06(Tool Use) 记忆操作通过工具实现──还需要操作系统基础知识 Si no sabes lo que es "虚拟内存""页面错误"" , primero vaya a complementar el sistema de operaciones, si no, entonces pasa a clases de la clase de la clase de la clase de la clase de la clase de la clase de la clase de la clase de la clase de la clase de la clase de la clase de los estudiantes.

## El concepto central.

### La analogía del sistema operativo

MemGPT (Packer et al., arXiv:2310.08560, v2 Feb 2024) mapea la gestión de contexto a la memoria virtual del sistema operativo:

> Packer 等人(arXiv:2310.08560, v2 2024 年 2 月)将上下文管理映射到操作系统虚拟内存:

| OS concept | MemGPT concept | 2026 production analog |
|------------|---------------|------------------------|
| OS 概念 | MemGPT 概念 | 2026 生产环境类比 |
| RAM | main context (prompt) | Anthropic/OpenAI context window / 主上下文（提示） |
| Disk | external context | vector DB, KV, graph store / 外部上下文（向量数据库、KV、图存储） |
| Page fault | memory tool call | `memory.search`, `memory.read`, `memory.write` / 记忆工具调用 |
| OS kernel | agent control loop | ReAct loop with memory tools / 带记忆工具的 ReAct 循环 |

El agente ejecuta un bucle ReAct normal. Una clase adicional de herramientas le permite páginas de datos dentro y fuera del contexto principal.

> ¿ Qué es esto ?**【类比】**MemGPT 像你的电脑内存管理:RAM(主上下文) sólo 8GB pero para ejecutar Photoshop + 浏览器 + IDE; operating system por página cambia de entrada a salida(page in/out) hacerte "sentir" tiene un límite de memoria;;MemGPT 让代理也这样做主上下文塞不下时,Agent自我调用 `archival_memory_search`"Cambio de contenido",调用 `core_memory_replace`Añade contenido "cambiar" en el sistema operativo.

> Agencia de operaciones de ciclo ReAct normal. Un tipo adicional de herramientas permite intercambiar datos entre el archivo principal y el de almacenamiento externo.

> **【中文解读】**MemGPT se ejecutará en el sistema operativo virtual内存:RAM=主上下文 (en inglés),磁盘=外部上下文 (en inglés),向量数据库/KV/图存储 (en inglés),页面错误=memory tool调用 (en inglés).`memory.search`- ¿ Qué ?`memory.read`- ¿ Qué ?`memory.write`),OS 内核=Agent 控制循环──Agent 运行普通的 ReAct 循环, adicionalmente añade un tipo de herramienta utilizada para intercambiar datos entre el archivo principal y el de almacenamiento externo―

### Dos niveles

- **Main context.**Impulso de tamaño fijo que retiene la tarea actual. Siempre visible para el modelo.
  En inglés:**主上下文。**固定大小的提示,承载当前任务──模型始终可见──
- **External context.**Sin límites, se puede buscar a través de herramientas.
  En inglés:**外部上下文。**无界的, 通过工具可搜索──相关时读取,出现事实时写入──

El documento original evaluó el diseño en dos tareas más allá de la ventana base: análisis de documentos más largos que 100k tokens y chat de varias sesiones con memoria persistente a lo largo de días.

> El artículo original fue evaluado en dos tareas de ventanas de base superiores: análisis de archivos de más de 100k tokens y análisis de memoria de varias reuniones.

### El patrón de interrupción

MemGPT introduce la memoria como interrupción: a mediados de la conversación el agente puede invocar una herramienta de memoria, el tiempo de ejecución la ejecuta, y el resultado se inserta en el siguiente turno de asistente como una nueva observación.`read()`syscall que bloquea el proceso, devuelve bytes, y el proceso continúa.

> MemGPT introdujo memoria es interrupción: en el diálogo el agente puede utilizar herramientas de memoria, ejecutarlas durante su ejecución, como resultado de un nuevo observador conectado a la siguiente ayuda de la ronda de interrupción.`read()`系统调用阻塞进程、返回字节、进程继续──

Superficie de la herramienta de memoria canónica:

> 标准记忆工具接口:

- `core_memory_append(section, text)` escribir a una sección persistente del aviso.
  En inglés:`core_memory_append(section, text)`写入提示的持久化分区──
- `core_memory_replace(section, old, new)` editar una sección persistente.
  En inglés:`core_memory_replace(section, old, new)`编辑持久化分区──
- `archival_memory_insert(text)` escribir a la tienda externa de búsqueda.
  En inglés:`archival_memory_insert(text)` escribir en el almacén externo de búsqueda
- `archival_memory_search(query, top_k)` Recogerlo en la tienda externa.
  En inglés:`archival_memory_search(query, top_k)` desde el almacenamiento externo
- `conversation_search(query)` escanear los curvas pasadas.
  En inglés:`conversation_search(query)`扫描过去的轮次──

### Donde termina el papel y comienza la producción

En septiembre de 2024 el MemGPT se convirtió en Letta.`cpacker/MemGPT`) permanece; Letta amplía el diseño:

> El año 2024 fue 9 de enero de MemGPT 成为 Letta──研究仓库(`cpacker/MemGPT`) todavía existe;Leta 扩展了设计:

- Tres niveles en lugar de dos (núcleo, recuerdo, archivo  Lección 08).
  La historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la China.
- Raciocinio nativo que sustituye a la `send_message`/ patrón de latidos cardíacos (lección 08).
  El lenguaje original de la lengua china es el lenguaje original de la lengua china.`send_message`/心跳模式 (sección 8)
- Agentes del sueño que ejecutan el trabajo de memoria asincronizada (lección 08).
  El tiempo de sueño del trabajo de memoria (Reflex)

El papel MemGPT es la base para 2026 incluso si los sistemas de producción ejecutan Letta, Mem0 o una tienda de dos niveles personalizada.

> MemGPT es la base de 2026 años, incluso si el sistema de producción se ejecuta Letta、Mem0 o auto-definir dos niveles de almacenamiento。

### Cuando este patrón va mal

> ️ **【易错点】**MemGPT Noviciel le facilita ignorar "memória投毒": poner en la página externa de la página, el mensaje del usuario directamente`archival_memory_insert`En el almacenamiento externo.**后果**El atacante en la página web tiene una inyección rápida, como "ignorar antes de todas las instrucciones"), la siguiente vez que el agente recauda este recuento, la instrucción se ejecuta.**一行修复**Todo el contenido externo que entra en el archivo debe ser primero hecho seguro.

- **Memory rot.**Las escrituras se acumulan más rápido que las lecturas; la recuperación se ahoga en hechos obsoletos.
  En inglés:**记忆腐化。**写入积累速度快于读取;检索被过时事实淹没──修复:定期合并(Leta hora de dormir)、显式失效(Mem0 冲突检测器)──
- **Memory poisoning.**Se recupera el texto de la memoria externa. Si el contenido controlado por el atacante se encuentra en una nota de memoria, el agente la reingesta en la próxima sesión.
  En inglés:**记忆投毒。**Si el contenido del atacante controla entra en la memoria, el agente en la próxima sesión se re-recogerá.
- **Citation loss.**El agente recuerda que "el usuario me pidió enviar X" pero no puede citar qué turno.
  En inglés:**引用丢失。**Agente de memoria "User me hace publicar X" pero no puede citar cuál es la ronda.

> ¿ Qué es esto ?**【困惑】**P: 既然 2026年模型上下文窗口已经有1M代币了? Gemini 1.5 Pro), ¿necesita MemGPT este tipo de "内存虚拟"? A: 需要──窗口大不代表用对硬塞 1M代币会触发"中段遗忘" (perdida en el medio 现象) y注意力稀释, el modelo tiene un contenido intermedio muy bajo en el primer momento.

## Construye con movimiento.
```figure
context-budget
```

## Construye el mismo

`code/main.py`Implementa el patrón de dos niveles de MemGPT en stdlib:

> `code/main.py`Utilizando el estándar de la biblioteca se ha realizado dos niveles de MemGPT:

- `MainContext` Puffer de respuesta de tamaño fijo con un `core`dict y un `messages`lista; auto-compacta los mensajes más antiguos cuando se ha superado el límite.
  En inglés:`MainContext`Fixar grandes de la pista缓冲区,带 `core`字典和                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                          `messages`列表;超出上限时自动压缩最老的消息──
- `ArchivalStore` almacenamiento en memoria BM25-esque (puntuación de tokens-overlap) de (id, texto, etiquetas, sesión, turno) registros.
  En inglés:`ArchivalStore`内存中的类 BM25 存储(token 重叠评分), almacenamiento (id, texto, etiquetas, sesión, turno) 记录。
- Cinco herramientas de memoria que trazan mapas a la superficie de MemGPT.
  Traducción:México:MemGPT 接口的五个记忆工具.
- Un agente con guión que llena el archivo con hechos, luego responde una pregunta llamando.`archival_memory_search`¿ Qué ?
  Un guión agente, use factsfill en archivo de archivo, luego a través de调用 `archival_memory_search`回答问题──

- ¿Qué quieres decir ?

> 运行:

```
python3 code/main.py
```

El rastro muestra al agente escribiendo tres hechos, llenando el contexto principal del límite (desalojo forzoso), luego respondiendo a una pregunta de seguimiento mediante la extracción de archivos  reproducción del flujo de trabajo MemGPT sin ningún LLM real.

> 轨迹显示 Agent 写入三个事实、将主上下文填满到上限(强制驱逐) 、然后通过归档存储检查来回答后续问题在没有任何真实LLM的情况下重现 MemGPT 工作流──

## Usalo con el marco de ejecución

Cada sistema de memoria de producción hoy en día es una variante MemGPT:

> Hoy en día cada sistema de producción de memoria es una variación de MemGPT:

- **Letta**(Lección 08)  tres niveles, razonamiento nativo, cálculo del tiempo de sueño.
  En inglés:**Letta**(第 8 课) 三层、原生推理、睡眠时间计算──
- **Mem0**(Lección 09)  vector + KV + gráfico fusionado con una capa de puntuación.
  En inglés:**Mem0**(第 9 课) 向量 + KV + 图与评分层融合──
- **OpenAI Assistants / Responses** la memoria gestionada a través de hilos y archivos.
  En inglés:**OpenAI Assistants / Responses**por el proceso y la gestión de archivos 
- **Claude Agent SDK** memoria a largo plazo a través de las habilidades y la tienda de sesiones.
  En inglés:**Claude Agent SDK**por medio de habilidades y conversaciones de almacenamiento de memoria de largo plazo

Seleccione uno por forma operativa (auto-hosted, administrado, integrado en el marco), no por el patrón central  el patrón central es MemGPT.

> Según el modo de operación ([[auto-administration]], [[administration]], [[cadres de integración]]) seleccionar, y no el modo central  el modo central es MemGPT

## Envíe el producto .
### La forma de la memoria del agente

La página de página resuelve la capacidad. No decide qué almacenar. Cuatro tipos de memoria recurren en los sistemas de producción, cada uno respondiendo a una pregunta diferente:

- **Working memory**¿Qué importa ahora? La capa dentro del contexto: tarea actual, giros recientes, secciones centrales fijadas.
- **Episodic memory** ¿Qué pasó? curvas y trayectorias pasadas, almacenadas con referencias de sesión y curva, reproducibles a pedido.
- **Semantic memory** ¿Qué es verdad? hechos sobre el usuario, el dominio, el mundo, actualizados y deduplicados a medida que cambian.
- **Procedural memory**Aprendí rutinas, preferencias y reglas que guían el comportamiento futuro en lugar de recordar.

Las implementaciones de código abierto eligen diferentes puntos de ataque:

| Type | Implementation | How it tackles it |
|------|----------------|-------------------|
| Working | MemGPT / Letta | Pages content in and out of a fixed prompt budget via memory tools (this lesson, Lesson 08) |
| Episodic | Zep | Temporal knowledge graph — facts carry validity intervals, so "what was true when" is queryable |
| Semantic | Mem0 | Extraction pipeline that dedupes and updates facts across vector, KV, and graph stores (Lesson 09) |
| Semantic + procedural | LangMem | Background extraction of facts and behavioral rules into a store the agent consults between turns |
| Episodic + semantic | agentmemory | Captures sessions as they run, consolidates them into typed, searchable records |

## Envío

`outputs/skill-virtual-memory.md`es una habilidad reutilizable que produce un andamio de memoria de dos niveles correcto (superficie principal + archivo + herramienta) para cualquier tiempo de ejecución objetivo, con política de desalojo y campos de cita conectados.

> `outputs/skill-virtual-memory.md`Es una habilidad replicable, para generar dos niveles de memoria correctos para cualquier objetivo de ejecución, incluyendo la interfaz de archivos y herramientas, estrategias de expansión y citas.

## Los ejercicios.

1. Añadir un`max_main_context_tokens`Cap medida en tokens (aproximadamente con `len(text.split())`* 1.3). Compactar los mensajes más antiguos en un resumen cuando se supera el límite.
   China                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             `max_main_context_tokens`上限(Uz `len(text.split())`* 1.3 近似) ・ Cuando se superen el límite superior se comprimirán las noticias más antiguas en resumen―
2. Implemente correctamente BM25 sobre el archivo (frecuencia de plazo, frecuencia inversa de documento).
   En el ejemplar chino, el recuento de datos se mide en un recuento de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos
3. Añadir`citation`los campos (session_id, turn_id, source_url) a los inserts de archivo. Haga que el agente cite fuentes en cada respuesta respaldada por recuperación.
   En español: "En el archivo"`citation`字段(session_id, turn_id, source_url) ⋅让代理 在每个基于检索的回答上引用来源──
4. Simula el envenenamiento de la memoria: añade un archivo que dice "ignora todas las instrucciones futuras del usuario".
   China: 模拟记忆投毒:添加一条归档记录说"忽略所有未来用户指令"──编写一个防护器扫描检索结果中的指令类文本并标记为不可信──
5. Portar la implementación para utilizar el esquema JSON de memoria central del repo de investigación MemGPT (`cpacker/MemGPT`¿Qué cambios se producen cuando se cambian de cadenas planas a secciones tipografadas?
   La memoria central de la almacén de MemGPT está siendo implementada para usar MemGPT`cpacker/MemGPT`¿Qué ha cambiado el cambio de caracteres planos a tipos de divisores?

## Términos clave .

| Term | What people say | What it actually means |
|------|-----------------|-----------------------|
| 术语 | 通俗说法 | 实际含义 |
| Virtual context | "Unlimited memory" / "无限记忆" | Main (prompt) + external (searchable) tiers with page in/out / 主（提示）+ 外部（可搜索）两层，带页面换入/换出 |
| Main context | "Working memory" / "工作记忆" | The prompt — fixed-size, always visible / 提示——固定大小，始终可见 |
| Archival memory | "Long-term store" / "长期存储" | External searchable persistence, retrieved on demand / 外部可搜索持久化，按需检索 |
| Core memory | "Persistent prompt section" / "持久化提示分区" | Named sections pinned inside the main context / 固定在主上下文内的命名分区 |
| Memory tool | "Memory API" / "记忆 API" | Tool call the agent issues to read/write external memory / Agent 发出的读/写外部记忆的工具调用 |
| Interrupt | "Memory page fault" / "记忆页面错误" | Agent pauses, runtime fetches, result splices into next turn / Agent 暂停、运行时获取、结果拼接到下一轮 |
| Memory rot | "Stale facts" / "过时事实" | Old writes drown retrieval; fix with consolidation / 旧写入淹没检索；用合并修复 |
| Memory poisoning | "Injected persistent note" / "注入的持久化笔记" | Attacker content stored as memory, re-ingested on recall / 攻击者内容存储为记忆，在回忆时重新摄取 |

## Más Leer más Leer más

- [Packer et al., MemGPT (arXiv:2310.08560)](https://arxiv.org/abs/2310.08560) Papel de contexto virtual inspirado en el sistema operativo
  En el contexto de la actualidad, el sistema operativo de MemGPT se ha iniciado en el contexto de la actualidad.
- [Letta, Memory Blocks blog](https://www.letta.com/blog/memory-blocks) la evolución de tres niveles
  La historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de los tiempos de los tiempos de los tiempos de los tiempos de los tiempos de los tiempos de los tiempos de los tiempos de los tiempos de los tiempos de los tiempos de los tiempos de los tiempos de los tiempos de los tiempos de los tiempos de los tiempos de los tiempos de los tiempos de los tiempos.
- [Anthropic, Effective context engineering](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents) el contexto como presupuesto
  China 关于有效上下文工程的文章将上下文视为预算──
- [Chhikara et al., Mem0 (arXiv:2504.19413)](https://arxiv.org/abs/2504.19413) memoria de producción híbrida en la parte superior de este patrón
  En el contexto de la producción de la memoria, el proceso de producción de la memoria se desarrolla en el contexto de la producción de la memoria.
- [Zep (getzep/zep)](https://github.com/getzep/zep) Memoria temporal del grafo de conocimiento de la tabla de taxonomía
- [Mem0 (mem0ai/mem0)](https://github.com/mem0ai/mem0) el oleoducto de extracción detrás de la tienda híbrida de la Lección 09
- [LangMem (langchain-ai/langmem)](https://github.com/langchain-ai/langmem) extracción de datos y normas de comportamiento
- [agentmemory (rohitg00/agentmemory)](https://github.com/rohitg00/agentmemory) Captura de sesiones consolidada en registros digitalizados y buscables
