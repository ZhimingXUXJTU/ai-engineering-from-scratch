# Repo Memoria y estado duradero  permanente  memoria  estado  almacén

> El historial de chat es volátil. El repo es duradero. El banco de trabajo almacenan el estado del agente en archivos versionados para que la próxima sesión, el siguiente agente y el siguiente revisor lean todas de la misma fuente de verdad.

**Type:** Build | **类型:** 构建
**Languages:** Python (stdlib + `jsonschema` optional) | **语言:** Python (标准库)
**Prerequisites:** Phase 14 · 32 (Minimal Workbench) | **前置知识:** 见原文
**Time:** ~60 minutes | **时间:** 见原文

> ¿ Qué es esto ?**【前置】**学本节前Permanecer la fase 14·32 (Minimal Workbench) ――本节讲如何使用仓库本身 ((不是聊天历史)作为代理的"长期记忆"――
> ¿ Qué es esto ?**【类比】**Historial de chat = 短期记忆(睡觉就忘),Repo memoria = 笔记本(写下来长期保留) ・・・ Agente 完成长任务时不能依赖短期记忆上下文窗口会满,需要把关键信息写到 repo 里(如`STATE.md`¿Qué es esto?`DECISIONS.md`), siguiente inicio en el momento de leer estos documentos.

## Objetivos de aprendizaje

- Defina lo que pertenece a la memoria de repo y lo que pertenece al historial de chat.
- Autor de JSON Schemas para `agent_state.json`y `task_board.json`¿ Qué ?
- Construir un administrador de estado que cargue, valida, muta y persiste estado de forma atómica.
- Utilice el esquema para rechazar las malas escrituras antes de que corrompan el escritorio.

## El problema es la introducción del problema

El agente termina una sesión. El chat se cierra. La siguiente sesión se abre y pregunta dónde empezar. El modelo dice "dejenme revisar los archivos", lee notas obsoletas y vuelve a hacer el trabajo que ya estaba terminado. O peor, vuelve a escribir un archivo terminado porque nadie le dijo que el archivo estaba terminado.

> Agente 完成一会话──聊天关闭──下一个会话打开并问从哪里开始──模型说"让我检查文件",读取过时的笔记,重新做已完成的工作──或更糟糕的是,它重写了已完成的文件,因为没有人告诉它文件已完成──

El banco de trabajo es la memoria de repo: el estado vive en los archivos JSON en el repo, escrito bajo un esquema, persistió de forma atómica, diferente en la revisión de código.

> 工作台的修复是仓库记忆: el estado existe en el archivo JSON de la bodega, en el esquema abajo escrito, atomizado perpetuado, en el código revisado amigo diferencial.


> **【中文解读】**仓库记忆与状态管理让代理维护对代码库的理解──两种记忆: 1) 结构性记忆文件树、依赖关系、API 接口; 2) 语义性记忆代码意图、设计决策、变更历史──状态管理确保代理在多轮交互中保持一致的代码库理解──

## El concepto central.

```mermaid
flowchart LR
  Agent[Agent Loop] --> Manager[StateManager]
  Manager --> Schema[agent_state.schema.json]
  Schema --> Validate{valid?}
  Validate -- yes --> Write[agent_state.json]
  Validate -- no --> Reject[refuse + raise]
  Write --> Manager
```


> **【中文解读】**仓库记忆与状态管理让代理维护对代码库的理解──两种记忆: 1) 结构性记忆文件树、依赖关系、API 接口; 2) 语义性记忆代码意图、设计决策、变更历史──状态管理确保代理在多轮交互中保持一致的代码库理解──

### Lo que pertenece a la memoria repo

| Belongs | Does not belong |
|---------|-----------------|
| Active task id | Raw chat transcripts |
| Touched files this session | Token-level reasoning traces |
| Assumptions the agent made | "The user seemed frustrated" |
| Open blockers | Sampled completions |
| Next action | Vendor-specific model ids |

La prueba es la durabilidad: ¿sería útil en tres meses en una repetición de CI? si sí, repo. si no, telemetría.

>  almacenamiento de memoria y estado de gestión de la decisión Agente en la base de código almacenamiento de la siguiente cuestión de perduradación ∞ incluyendo la indicación de documentos ∞ cambios de seguimiento ∞ dependencia ∞ mantenimiento ∞

### Estado del primer esquema

Sin él, cada agente inventa nuevos campos, cada revisor aprende una nueva forma, y cada script de CI tiene que hacer caso especial a versiones anteriores.

>  almacenamiento de memoria y estado de gestión de la decisión Agente en la base de código almacenamiento de la siguiente cuestión de perduradación ∞ incluyendo la indicación de documentos ∞ cambios de seguimiento ∞ dependencia ∞ mantenimiento ∞

El esquema incluye:

- Necesitas llaves.
- Se permite`status`los valores.
- Valores prohibidos (por ejemplo `null`para matrices).
- Constrangimientos de patrón (identificación de tareas coincide `T-\d{3,}`¿Qué es lo que se hace?
- Campo de versión para migraciones.

### Atomic escribe

El archivo del estado es la fuente de la verdad; un archivo medio escrito es peor que ningún archivo.

>  almacenamiento de memoria y estado de gestión de la decisión Agente en la base de código almacenamiento de la siguiente cuestión de perduradación ∞ incluyendo la indicación de documentos ∞ cambios de seguimiento ∞ dependencia ∞ mantenimiento ∞

### Migraciones

Cuando el esquema cambie, envíe un script de migración junto al golpe de esquema.`schema_version`campo; el administrador se niega a cargar un archivo desde una versión que no puede migrar.

>  almacenamiento de memoria y estado de gestión de la decisión Agente en la base de código almacenamiento de la siguiente cuestión de perduradación ∞ incluyendo la indicación de documentos ∞ cambios de seguimiento ∞ dependencia ∞ mantenimiento ∞

## Construye y realiza.
```figure
wb-state-persist
```

## Construye el mismo

`code/main.py`los instrumentos:

- `agent_state.schema.json`y `task_board.schema.json`¿ Qué ?
- Un validador de sólo stdlib (subconjunto de JSON Schema: requerido, tipo, enum, patrón, elementos).
- `StateManager.load`¿ Qué ?`StateManager.update`¿ Qué ?`StateManager.commit`con el tiempo atómico y el renombre escribe.
- Una demostración que muta el estado, persiste, se recarga y prueba el viaje de ida y vuelta.

- ¿Qué quieres decir ?

```
python3 code/main.py
```

El guión dice:`workdir/agent_state.json`y `workdir/task_board.json`, los muta en dos vueltas, e imprime el estado validado en cada paso.

>  almacenamiento de memoria y estado de gestión de la decisión Agente en la base de código almacenamiento de la siguiente cuestión de perduradación ∞ incluyendo la indicación de documentos ∞ cambios de seguimiento ∞ dependencia ∞ mantenimiento ∞

## Modelos de producción en la naturaleza

Cuatro patrones convierten el mínimo de la lección en algo que un monorepo multi-agente puede sobrevivir.

>  almacenamiento de memoria y estado de gestión de la decisión Agente en la base de código almacenamiento de la siguiente cuestión de perduradación ∞ incluyendo la indicación de documentos ∞ cambios de seguimiento ∞ dependencia ∞ mantenimiento ∞

**Atomic temp-and-rename is not optional.**Un informe de errores del proyecto Hive de marzo de 2026 documenta el modo de falla de manera limpia: `state.json`fue escrito a través de `write_text()`Partial escribe a la izquierda sesiones que se reanudan contra el estado corrupto sin señal.`tempfile.mkstemp`en el mismo directorio que el objetivo, escriba, `fsync`¿ Qué ?`os.replace`Esta lección es una de las mejores de las que podemos aprender.`atomic_write`hace exactamente eso.

**Idempotency keys on every non-idempotent tool call.**Si un agente se estrella después de llamar a una herramienta pero antes de marcar el resultado, la recuperación vuelve a intentar la llamada a la herramienta. Seguro para las lecturas; peligroso para correos electrónicos, inserciones de DB, cargas de archivos. El patrón: registrar cada ID de llamada de la herramienta antes de la ejecución en un `pending_calls.jsonl`En el nuevo intento, compruebe la identificación; si está presente, omita la llamada y utiliza el resultado almacenado en caché. Anthropic y LangChain lo llaman en la guía de 2026; el puntero de control de LangGraph persiste en espera de escritos por la misma razón.

**Separate large artifacts from state.**No almacenes CSV, transcripciones largas o archivos generados en `agent_state.json`. Guarde el artefacto como un archivo separado (o cargue al almacenamiento de objetos) y mantenga solo el camino en estado. Los puntos de control se mantienen pequeños y rápidos; los artefactos crecen de forma independiente.

**Event sourcing for audit, snapshots for resume.**Aplicar a un registro de eventos (`state.events.jsonl`) en cada mutación; de forma periódica, una instantánea de `state.json`Resume lee el instantáneo, luego reproduce cualquier evento después de la timestamp de la instantánea. Esto cuesta más disco pero le permite reproducir las decisiones del agente literalmente  esencial cuando se deparan ejecuciones de horizonte largo. La misma forma que utiliza Postgres internamente para WAL.

**Schema migrations or refuse to load.**El `schema_version`Cuando el administrador carga un archivo en una versión desconocida, se niega a leer. Envía un script de migración junto al golpe de esquema; `tools/migrate_state.py`funciona de forma idempotente en cada startup.

## Usalo con el marco de ejecución

En producción:

- **LangGraph checkpointers.**El punto de control persiste en el estado del gráfico a SQLite, Postgres o un backend personalizado. El esquema que enseña esta lección es lo que se alcanza cuando el punto de control muere y se necesita leer el estado a mano.
- **Letta memory blocks.**Bloques persistentes con esquemas estructurados (fase 14 · 08).
- **OpenAI Agents SDK session store.**El archivo de estado en esta lección es el archivo de fondo local.

## Envíe el producto .

`outputs/skill-state-schema.md`genera un par de esquemas JSON específicos para el proyecto (estado + tablero), un Python `StateManager`cableado a escrituras atómicas, y un andamio de migración para que el siguiente golpe de esquema no rompa el escritorio.

>  almacenamiento de memoria y estado de gestión de la decisión Agente en la base de código almacenamiento de la siguiente cuestión de perduradación ∞ incluyendo la indicación de documentos ∞ cambios de seguimiento ∞ dependencia ∞ mantenimiento ∞

## Los ejercicios.

1. Añadir un`last_human_touch`Rechazar cualquier agente escribir dentro de cinco segundos de una edición humana.
  En inglés, "pensar y practicar" significa "pensar y practicar".
2. Extensión del validador para soportar `oneOf`Así que una tarea puede ser una tarea de construcción o una tarea de revisión con diferentes campos requeridos.
  En inglés, "pensar y practicar" significa "pensar y practicar".
3. Añadir un`schema_version`campo y escribir la migración de v1 a v2 (renombrar `blockers`¿ Qué ?`risks`¿Qué es lo que se hace?
  En inglés, "pensar y practicar" significa "pensar y practicar".
4. Mover el backend de almacenamiento de un archivo local a SQLite.`StateManager`La API es idéntica.
  En inglés, "pensar y practicar" significa "pensar y practicar".
5. ¿Qué pasa y cómo te salva el cambio de nombre atómico?
  En inglés, "pensar y practicar" significa "pensar y practicar".

## Términos clave .

| Term | What people say | What it actually means |
|------|----------------|------------------------|---|
| Repo memory | "Notes file" | State stored in tracked files in the repo, under schema |  |
| Schema-first | "Validate inputs" | Define the contract before the writer, refuse drift |  |
| Atomic write | "Just rename" | Write to temp, fsync, rename, so partial failures cannot corrupt |  |
| Migration | "Schema bump" | A script that turns vN state into v(N+1) state |  |
| System of record | "Source of truth" | The artifact the workbench treats as authoritative |  |

## Más Leer más Leer más

- [JSON Schema specification](https://json-schema.org/specification.html)
  En el caso de los niños, el nombre de la persona que se encuentra en el lugar de residencia es el de la persona que se encuentra en el lugar de residencia.
- [LangGraph checkpointers](https://langchain-ai.github.io/langgraph/concepts/persistence/)
  En el caso de los niños, el nombre de la persona que se encuentra en el lugar de residencia es el de la persona que se encuentra en el lugar de residencia.
- [Letta memory blocks](https://docs.letta.com/concepts/memory)
  En el caso de los niños, el nombre de la persona que se encuentra en el lugar de residencia es el de la persona que se encuentra en el lugar de residencia.
- [Fast.io, AI Agent State Checkpointing: A Practical Guide](https://fast.io/resources/ai-agent-state-checkpointing/) Control de esquemas con idempotencia
  En el caso de los niños, el nombre de la persona que se encuentra en el lugar de residencia es el de la persona que se encuentra en el lugar de residencia.
- [Fast.io, AI Agent Workflow State Persistence: Best Practices 2026](https://fast.io/resources/ai-agent-workflow-state-persistence/) control de concurrencia, TTL, abastecimiento de eventos
  En el caso de los niños, el nombre de la persona que se encuentra en el lugar de residencia es el de la persona que se encuentra en el lugar de residencia.
- [Hive Issue #6263 — non-atomic state.json writes silently ignored](https://github.com/aden-hive/hive/issues/6263) el modo de fallo en un proyecto real
  En el caso de los niños, el nombre de la persona que se encuentra en el lugar de residencia es el de la persona que se encuentra en el lugar de residencia.
- [eunomia, Checkpoint/Restore Systems: Evolution, Techniques, Applications](https://eunomia.dev/blog/2025/05/11/checkpointrestore-systems-evolution-techniques-and-applications-in-ai-agents/) Primitivas de CR de la historia del sistema operativo aplicadas a agentes
  En el caso de los niños, el nombre de la persona que se encuentra en el lugar de residencia es el de la persona que se encuentra en el lugar de residencia.
- [Indium, 7 State Persistence Strategies for Long-Running AI Agents in 2026](https://www.indium.tech/blog/7-state-persistence-strategies-ai-agents-2026/)
  En el caso de los niños, el nombre de la persona que se encuentra en el lugar de residencia es el de la persona que se encuentra en el lugar de residencia.
- [Microsoft Agent Framework, Compaction](https://learn.microsoft.com/en-us/agent-framework/agents/conversations/compaction) Gerente de los puntos de control del vendedor
  En el caso de los niños, el nombre de la persona que se encuentra en el lugar de residencia es el de la persona que se encuentra en el lugar de residencia.
- Fase 14 · 08  Bloques de memoria y cálculo del tiempo de sueño
- Fase 14 · 32  el mínimo de tres archivos esta lección esquema
- Fase 14 · 40  paquetes de entrega leídos desde el mismo esquema
