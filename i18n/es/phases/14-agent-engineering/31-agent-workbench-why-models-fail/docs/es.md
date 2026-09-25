# ¿Por qué los modelos capaces siguen fracasando ?

> Un modelo capaz no es suficiente. Los agentes confiables necesitan un banco de trabajo: instrucciones, estado, alcance, retroalimentación, verificación, revisión y entrega.

**Type:** Learn + Build | **类型:** 构建
**Languages:** Python (stdlib) | **语言:** Python (标准库)
**Prerequisites:** Phase 14 · 01 (Agent Loop), Phase 14 · 26 (Failure Modes) | **前置知识:** 见原文
**Time:** ~45 minutes | **时间:** 见原文

> ¿ Qué es esto ?**【前置】**学本节前请先掌握:Fase 14·01(Fase 14·26(Modos de fracaso)。本节是后续Fase 14·32-42(Workbench 系列 7 节) de entrada,讲为什么"光有好模型不够"。

> ¿ Qué es esto ?**【类比】**En el caso de los cocineros, el trabajo de los trabajadores de la cocina es de un tipo muy diferente. El trabajo de los cocineros es de un tipo muy similar.

## Objetivos de aprendizaje

- Capacidad de modelo separada de la fiabilidad de ejecución.
- Nombre las siete superficies de trabajo que deciden si un agente navega.
- Compare una carrera de solo tiempo con una carrera guiada por un banco de trabajo en una pequeña tarea de repo.
- Produce un informe de modo de falla que mapee cada superficie perdida con el síntoma que causó.

## El problema es la introducción del problema

Se deja un modelo fronterizo en un repo real y se le pide que añada validación de entrada. Se abren cuatro archivos, se escribe código plausible, se declara el éxito y se detiene. Se ejecutan las pruebas. Dos fallan. Se toca un tercer archivo que no tenía nada que ver con la validación. No hay registro de lo que el agente asumió, lo que intentó primero, o lo que queda para hacer.

> Usted pone un modelo de vanguardia en el almacén de código real, deja que añada un certificado de entrada. Abre cuatro archivos, escribe un código que parezca razonable, declara éxito, luego se detiene. Usted ejecuta un test. Dos fracasos. El tercer archivo es mencionado, pero no tiene relación con el certificado.

El modelo no estaba equivocado acerca de Python, estaba equivocado acerca del trabajo, no tenía idea de lo que se contaba como hecho, dónde se le permitía escribir, qué pruebas eran autorizadas, o cómo se suponía que la próxima sesión se retomaría.

> 模型在 Python 上没有错误. 模型在工作上没有错误. 模型在 Python 上没有错误. 模型在工作上错误. 模型在 Python 上没有错误. 模型在 Python 上没有错误. 模型在工作上没有错误. 模型在 Python 上没有错误. 模型在 Python 上没有错误. 模型在 Python 上没有错误. 模型在 Python 上没有错误. 模型在 Python 上没有错误. 模型在 Python 上没有错误. 模型在 Python 上没有错误. 模型在 Python 上没有错误. 模型在 Python 上没有错误. 模型在 Python 上没有错误. 模型在 Python 上没有错误. 模型在 Python 上没有错误. 模型在 Python 上没有错误. 模型在 Python 上没有错误. 模型在 Python 上没有错误. 模型在 Python 上没有错误. 模型在 Python 上没有错误. 模型在 Python 上没有错误. 模型在 Python 上没有错误. 模型在 Python 上没有错误.


> **【中文解读】**En el caso de los agentes en el almacén real, el análisis de las causas de la falla es: 1) la instrucción de seguir el fracaso  ignorar la limitación o la capacidad de elaborar la inexistencia; 2) la cantidad de datos que se consumen en la ventana anterior y posteriormente en la ventana superior, que causan la pérdida de información clave; 3) el error acumulado  pequeños errores en la ejecución de varios pasos en el proceso de deslizamiento; 4) la falta de memoria del proyecto  desconocer la configuración y la estructura de la base de código.

No es un error de modelo, es un error de escritorio, la superficie alrededor del agente carece de las piezas que conviertan una generación de un solo disparo en ingeniería fiable y reutilizable.

> Esto no es un error de modelo. Esto es un error de trabajo. La falta de superficie de los agentes alrededor de la obra se transformará de una vez en otra en una parte de la obra confiable y recuperable.

> El modelo de fracaso principal incluye: instrucciones para seguir el fracaso, herramientas para usar errores, perdidas de texto y la ruptura de la cadena de cálculo.

## El concepto central.

Un escritorio es el entorno operativo que envuelve el modelo durante una tarea.

> El modelo de fracaso principal incluye: instrucciones para seguir el fracaso, herramientas para usar errores, perdidas de texto y la ruptura de la cadena de cálculo.

| Surface | What it carries | Failure when missing |
|---------|-----------------|----------------------|
| Instructions | Startup rules, forbidden actions, definition of done | Agent guesses what shipping means |
| State | Current task, touched files, blockers, next action | Each session restarts from zero |
| Scope | Allowed files, forbidden files, acceptance criteria | Edits leak into unrelated code |
| Feedback | Real command output captured into the loop | Agent declares success on a 400 |
| Verification | Tests, lint, smoke run, scope check | "Looks good" reaches main |
| Review | A second pass with a different role | Builder marks own homework |
| Handoff | What changed, why, what is left | Next session re-discovers everything |


> **【中文解读】**En el caso de los agentes en el almacén real, el análisis de las causas de la falla es: 1) la instrucción de seguir el fracaso  ignorar la limitación o la capacidad de elaborar la inexistencia; 2) la cantidad de datos que se consumen en la ventana anterior y posteriormente en la ventana superior, que causan la pérdida de información clave; 3) el error acumulado  pequeños errores en la ejecución de varios pasos en el proceso de deslizamiento; 4) la falta de memoria del proyecto  desconocer la configuración y la estructura de la base de código.

El banco de trabajo es independiente del modelo. Puedes cambiar el modelo y mantener las superficies. No puedes cambiar las superficies y mantener la fiabilidad.

> 工作台独立于模型── puedes sustituir el modelo y conservar la superficie── no puedes sustituir la superficie y conservar la fiabilidad──

> El modelo de fracaso principal incluye: instrucciones para seguir el fracaso, herramientas para usar errores, perdidas de texto y la ruptura de la cadena de cálculo.

```mermaid
flowchart LR
  Task[Task] --> Scope[Scope Contract]
  Scope --> State[Repo Memory]
  State --> Agent[Agent Loop]
  Agent --> Feedback[Runtime Feedback]
  Feedback --> Verify[Verification Gate]
  Verify --> Review[Reviewer]
  Review --> Handoff[Handoff]
  Handoff --> State
```

El bucle se cierra en el archivo de estado, no en el historial de chat.

> El ciclo se cierra en los archivos de estado, en lugar de en la historia del chat.

> El modelo de fracaso principal incluye: instrucciones para seguir el fracaso, herramientas para usar errores, perdidas de texto y la ruptura de la cadena de cálculo.

### En el trabajo de la mesa de trabajo frente a la ingeniería rápida

El impulso le dice al modelo lo que desea en este turno. Un escritorio le dice al modelo cómo hacer el trabajo a través de los turnos y a través de las sesiones. La mayoría de las historias de fallas de agentes son fallos en el escritorio usando ropa de ingeniería de impulso.

> 提示告诉模型这个轮你想要什么――工作台告诉模型如何跨轮次和跨会话做工作―― La mayoría de las historias de fracaso de un agente son de un proyecto de trabajo en el que el modelo no tiene éxito―

> El modelo de fracaso principal incluye: instrucciones para seguir el fracaso, herramientas para usar errores, perdidas de texto y la ruptura de la cadena de cálculo.

### En el marco de trabajo

Un framework le da un tiempo de ejecución (LangGraph, AutoGen, Agents SDK). Un banco de trabajo le da al agente un lugar para trabajar dentro de ese tiempo de ejecución. Necesitas ambos. Esta mini-track es sobre el segundo.

> 框架给你一个运行时(LangGraph、AutoGen、Agents SDK) ⋅工作台给 Agent 在那运行时内一个工作的地方──两者都需要──这个小专题是关于第二个的──

> El modelo de fracaso principal incluye: instrucciones para seguir el fracaso, herramientas para usar errores, perdidas de texto y la ruptura de la cadena de cálculo.

### Razonamiento de las primitivas, no de las taxonomias de los vendedores

Hay mucho escrito sobre "ingeniería de arnés" ahora mismo. Addy Osmani, OpenAI, Anthropic, LangChain, Martin Fowler, MongoDB, HumanLayer, Augment Code, Thoughtworks, la lista impresionante de walkinglabs, y un ritmo constante de Medium y Hacker News, todo lo están llevando. No están de acuerdo en los límites de lo que es un arnés, lo que está en el alcance, y qué vocabulario usar. No necesitamos escoger un lado. Las siete superficies son una capa de UX; debajo de cada banco de trabajo hay el mismo conjunto de sistemas distribuidos primitivos que sostienen cualquier backend confiable.

> El modelo de fracaso principal incluye: instrucciones para seguir el fracaso, herramientas para usar errores, perdidas de texto y la ruptura de la cadena de cálculo.

Deshacerse de la etiqueta del agente por un momento. Un ejecutor de agente es un cálculo que cruza el tiempo, los procesos y las máquinas. Para hacer que sea confiable se necesitan los mismos primitivos que cualquier sistema de producción necesita.

> 暂时删除代理标签――un agente 运行是跨越时间、进程和机器的计算―― para hacerlo fiable, necesitas el mismo idioma original que cualquier sistema de producción necesita―

> El modelo de fracaso principal incluye: instrucciones para seguir el fracaso, herramientas para usar errores, perdidas de texto y la ruptura de la cadena de cálculo.

| Primitive | What it is | What it carries for an agent |
|-----------|------------|------------------------------|
| Function | Typed handler. Pure where possible. Owns its inputs and outputs. | A tool call, a rule check, a verification step, a model invocation |
| Worker | Long-lived process that owns one or more functions and a lifecycle | The builder, the reviewer, the verifier, an MCP server |
| Trigger | Event source that invokes a function | Agent loop tick, HTTP request, queue message, cron, file change, hook |
| Runtime | The boundary that decides what runs where, with what timeouts and resources | Claude Code's process, LangGraph's runtime, a worker container |
| HTTP / RPC | The wire between caller and worker | Tool-call protocol, MCP request, model API |
| Queue | Durable buffer between trigger and worker; back-pressure, retry, idempotency | The task board, the feedback log, the review inbox |
| Session persistence | State that survives crashes, restarts, model swaps | `agent_state.json`, checkpoints, KV stores, the repo itself |
| Authorization policy | Who can call what function with which scope | Allowed/forbidden files, approval boundaries, MCP capability lists |

Ahora, mapear las siete superficies de escritorio en esas primitivas.

> El modelo de fracaso principal incluye: instrucciones para seguir el fracaso, herramientas para usar errores, perdidas de texto y la ruptura de la cadena de cálculo.

- **Instructions** política + metadatos de función. reglas son controles (funciones).`AGENTS.md`) es la política vinculada al inicio del tiempo de ejecución.
- **State** Persistencia de sesión. Un almacén con teclado lee el tiempo de ejecución en cada paso. archivo, KV o DB; la semántica de persistencia importa, el backend de almacenamiento no.
- **Scope** Política de autorización por tarea. los globos permitidos/prohibidos son un ACL. Las aprobaciones requeridas son una red de permisos.
- **Feedback** registro de invocación escrito en una cola. Cada llamada de shell es un registro, duradero, reproducible.
- **Verification** una función. Determinista sobre entradas.
- **Review** un trabajador separado con derecho de lectura únicamente de los artefactos de construcción y de escritura únicamente de los informes de revisión.
- **Handoff** un registro duradero emitido por un gatillo de final de sesión.

El bucle de agente en sí mismo es un trabajador que consume eventos (mensaje del usuario, resultado de la herramienta, marca el tiempo), llama a funciones (el modelo, luego las herramientas que el modelo elige), escribe registros (estado, retroalimentación) y emite disparadores (verificación, revisión, entrega).

> El modelo de fracaso principal incluye: instrucciones para seguir el fracaso, herramientas para usar errores, perdidas de texto y la ruptura de la cadena de cálculo.

### Modelos en circulación, traducidos a primitivos

Cada patrón popular de arnés se reduce a los ocho primitivos.

> El modelo de fracaso principal incluye: instrucciones para seguir el fracaso, herramientas para usar errores, perdidas de texto y la ruptura de la cadena de cálculo.

| Vendor or community pattern | What it actually is |
|------------------------------|--------------------|
| Ralph Loop (Claude Code, Codex, agentic_harness book) — re-inject original intent into a fresh context window when the agent tries to stop early | A trigger that re-enqueues a task with a clean context; session persistence carries the goal forward |
| Plan / Execute / Verify (PEV) | Three workers, one per role, communicating via state and a queue between phases |
| Harness-compute separation (OpenAI Agents SDK, April 2026) — split control plane from execution plane | Restating control-plane / data-plane. Predates the agent label by decades |
| Open Agent Passport (OAP, March 2026) — sign and audit every tool call against a declarative policy before execution | An authorization policy enforced by a pre-action worker, with a signed audit queue |
| Guides and Sensors (Birgitta Böckeler / Thoughtworks) — feedforward rules + feedback observability | Authorization policy + verification functions + observability traces |
| Progressive compaction, 5-stage (Claude Code reverse engineering, April 2026) | A state-management worker that runs cron-like over session persistence to keep it within a budget |
| Hooks / middleware (LangChain, Claude Code) — intercept model and tool calls | Triggers + functions wrapped around the runtime's invocation path |
| Skills as Markdown with progressive disclosure (Anthropic, Flue) | A function registry where the function metadata is loaded into context just-in-time |
| Sandbox agents (Codex, Sandcastle, Vercel Sandbox) | The compute plane: a runtime with isolated filesystem, network, and lifecycle |
| MCP servers | Workers exposing functions over a stable RPC, with capability lists as authorization |

Cada entrada en esa tabla es la comunidad de agentes llegando a un primitivo que ya tenía un nombre en sistemas distribuidos y dándole uno nuevo. Etiquetas útiles para el marketing; no útiles como vocabulario de ingeniería.

> El modelo de fracaso principal incluye: instrucciones para seguir el fracaso, herramientas para usar errores, perdidas de texto y la ruptura de la cadena de cálculo.

### Lo que dicen los recibos

La afirmación de que el modelo es más inteligente tiene números detrás de él ahora.

> El modelo de fracaso principal incluye: instrucciones para seguir el fracaso, herramientas para usar errores, perdidas de texto y la ruptura de la cadena de cálculo.

- Terminal Bench 2.0  el mismo modelo, cambio de arnés movió a un agente codificador de fuera de los 30 primeros a la posición cinco (LangChain, *Anatomía de un agente Arnés*).
- Vercel  eliminó el 80% de las herramientas de su agente; la tasa de éxito aumentó del 80% al 100% (MongoDB).
- Harvey  agentes legales más que duplicaron la precisión solo a través de la optimización del arnés (MongoDB).
- El 88% de los proyectos de agentes de IA de empresas no llegan a la producción. Los fallos se agrupan en torno al tiempo de ejecución, no en el razonamiento (preprints.org, *Harness Engineering for Language Agents*, marzo 2026).
- Un estudio de referencia de 2025 en tres marcos de código abierto populares informó de ~50% de finalización de tareas; WebAgent de contexto largo se desplomó del 40-50% a menos del 10% en condiciones de contexto largo, principalmente por bucles infinitos y pérdida de metas (cubrió ampliamente en las escrituras de 2026).

El resultado no es que el arnés gane para siempre. Los modelos absorben los trucos de arnés con el tiempo. El resultado es que hoy en día, la ingeniería de carga se centra en torno al modelo, no en su interior, y los primitivos que llevan esa carga son los que cada sistema de producción siempre ha necesitado.

> 结论不是"harness 永远赢"──模型确实会随时间吸收 harness 技巧──结论是今天,承载工程重量是模型周围的部分,而不是模型内部的,承载这个重量的原语是每个生产系统一直需要的──

> El modelo de fracaso principal incluye: instrucciones para seguir el fracaso, herramientas para usar errores, perdidas de texto y la ruptura de la cadena de cálculo.

### Donde las escrituras de los vendedores se detienen

Esta es la parte en la que no necesitas ser educado.

> El modelo de fracaso principal incluye: instrucciones para seguir el fracaso, herramientas para usar errores, perdidas de texto y la ruptura de la cadena de cálculo.

- LangChain *Anatomy of an Agent Harness* enumera once componentes  instrucciones, herramientas, ganchos, cajas de arena, orquestación, memoria, habilidades, sub-subgencios y un "bucle tonto" de tiempo de ejecución. No nombra filas, trabajadores como unidad de implementación, semántica de activación, persistencia de sesión como una preocupación separada o política de autorización. Trata al arnés como un objeto que configuras, no como un sistema que despliegas.
- Addy Osmani's *Agent Harness Engineering* aterriza el marco `Agent = Model + Harness`y el patrón de ratchet, pero no dice de qué se construye un arnés.
- Anthropic y OpenAI van más profundo en las superficies pero permanecen dentro de sus propios tiempos de ejecución. El anuncio de "separación de arnés-computación" en el APRIL 2026 Agents SDK es la primera pieza de proveedor que respalda explícitamente la división de control-plano / plano de datos. Esa es una idea primitiva, no una nueva.
- El libro de arneses agentes trata el arneses como un objeto de configuración (Jaymin West *Agentic Engineering*, capítulo 6) y la línea más fuerte en él es "el arneses es el límite de seguridad primario en un sistema agente". Eso es sólo política de autorización, reiterado.
- Los hilos de Hacker News siguen llegando al mismo lugar. El hilo de abril de 2026 *El arnés del agente pertenece fuera de la caja de arena* sostiene que el arnés debe estar "más como un hipervisor que se sienta fuera de todo y autoriza el acceso basado en el contexto y el usuario".

No es necesario estar en desacuerdo con ninguno de estos elementos para notar la brecha. Están escribiendo descripciones de UX de un sistema que ya existe. Estamos escribiendo el sistema. Cuando el sistema se construye correctamente, las siete superficies caen de las primitivas. Cuando se construye mal, no hay cantidad de `AGENTS.md`Polish arregla la cola que falta.

> El modelo de fracaso principal incluye: instrucciones para seguir el fracaso, herramientas para usar errores, perdidas de texto y la ruptura de la cadena de cálculo.

Así que cuando escuches "ingeniería de arnés" en otro lugar, traduce a primitivos. Las instrucciones y las reglas son políticas y funciones. El andamio es el tiempo de ejecución. Las barandillas son la autorización + verificación. Los ganchos son los gatilladores. La memoria es la persistencia de la sesión. El Ralph Loop está en orden. Los subagentes son trabajadores. Las cajas de arena son aviones de computación. El vocabulario cambia; la ingeniería no. El banco de trabajo es la UX de cara a un agente; el arnés, en el sentido que sobrevive al siguiente reframe del proveedor, es funciones, trabajadores, disparadores, tiempos de ejecución, colas, persistencia y política conectadas correctamente.

> El modelo de fracaso principal incluye: instrucciones para seguir el fracaso, herramientas para usar errores, perdidas de texto y la ruptura de la cadena de cálculo.

## Construye y realiza.
```figure
wb-seven-surfaces
```

## Construye el mismo

`code/main.py`El guión cuenta qué superficies faltan en la ejecución fallida y imprime un informe de modo de falla.

> El modelo de fracaso principal incluye: instrucciones para seguir el fracaso, herramientas para usar errores, perdidas de texto y la ruptura de la cadena de cálculo.

La tarea de repo es pequeña a propósito: añadir validación de entrada a un procesador de estilo FastAPI de un archivo y escribir una prueba de aprobación.

> El modelo de fracaso principal incluye: instrucciones para seguir el fracaso, herramientas para usar errores, perdidas de texto y la ruptura de la cadena de cálculo.

- ¿Qué quieres decir ?

```
python3 code/main.py
```

Resultado: un registro de las dos carreras, un `failure_modes.json`Resumiendo la carrera de inmediato y un veredicto de una sola línea para la carrera de trabajo.

> El modelo de fracaso principal incluye: instrucciones para seguir el fracaso, herramientas para usar errores, perdidas de texto y la ruptura de la cadena de cálculo.

El agente es un pequeño recinto basado en reglas; el punto es las superficies, no el modelo.

> El modelo de fracaso principal incluye: instrucciones para seguir el fracaso, herramientas para usar errores, perdidas de texto y la ruptura de la cadena de cálculo.

## Usalo con el marco de ejecución

Tres lugares de la mesa de trabajo superficies ya existen en la naturaleza, incluso si nadie los llama así:

> El modelo de fracaso principal incluye: instrucciones para seguir el fracaso, herramientas para usar errores, perdidas de texto y la ruptura de la cadena de cálculo.

- **Claude Code, Codex, Cursor.** `AGENTS.md`y `CLAUDE.md`Las instrucciones son la superficie, los comandos son el alcance, los ganchos son la verificación.
- **LangGraph, OpenAI Agents SDK.**Los puestos de control y las tiendas de sesiones son la superficie del estado.
- **CI on a real repo.**Las pruebas, el reviso de tipo y el reviso de la letra son la verificación.

La ingeniería de trabajo es la disciplina de hacer que esas superficies sean explícitas y reutilizables, en lugar de dejar que cada equipo las redescubra.

> El modelo de fracaso principal incluye: instrucciones para seguir el fracaso, herramientas para usar errores, perdidas de texto y la ruptura de la cadena de cálculo.

## Envíe el producto .

`outputs/skill-workbench-audit.md`Es una habilidad portátil que audita un repo existente para las siete superficies de escritorio y informes que faltan, que son parciales y que son saludables.

> `outputs/skill-workbench-audit.md`Es una habilidad transponible, auditar las siete superficies de trabajo existentes en el almacén, informar qué carencias, qué partes existen, qué salud. Colocar a cualquier agente junto a la configuración; te dirá primero qué reparar.

> El modelo de fracaso principal incluye: instrucciones para seguir el fracaso, herramientas para usar errores, perdidas de texto y la ruptura de la cadena de cálculo.

## Los ejercicios.

1. Seleccione un repo donde ya esté ejecutando un agente.
  En inglés, "pensar y practicar" significa "pensar y practicar".
2. Extenderse`main.py`Así que la ejecución de inmediato también produce una falsa afirmación de "éxito".
  En inglés, "pensar y practicar" significa "pensar y practicar".
3. Añade una octava superficie para su propio producto.
  En inglés, "pensar y practicar" significa "pensar y practicar".
4. Re-exercer el guión con un agente de estub que alucina una escritura de archivo adicional. ¿Qué superficie lo capta primero?
  En inglés, "pensar y practicar" significa "pensar y practicar".
5. Mapa de los cinco modos de falla recurrentes de la industria desde la fase 14 · 26 en las siete superficies. ¿Qué modo está diseñado para absorber cada superficie?
  En inglés, "pensar y practicar" significa "pensar y practicar".

## Términos clave .

| Term | What people say | What it actually means |
|------|----------------|------------------------|---|
| Workbench | "The setup" | Engineered surfaces around the model that make work reliable |  |
| Surface | "A doc" or "a script" | A named, machine-readable input the agent reads or writes every turn |  |
| System of record | "The notes" | The file the agent treats as truth when chat history is gone |  |
| Definition of done | "Acceptance" | An objective, file-backed checklist the agent cannot fake |  |
| Workbench audit | "Repo readiness check" | A pass over the seven surfaces that flags missing pieces before work begins |  |

## Más Leer más Leer más

Las personas que se encuentran en la zona de trabajo de la empresa deben tener en cuenta que el proyecto de trabajo de la empresa es un proyecto de investigación y que el objetivo de la empresa es mejorar la calidad de vida de la empresa.

> El modelo de fracaso principal incluye: instrucciones para seguir el fracaso, herramientas para usar errores, perdidas de texto y la ruptura de la cadena de cálculo.

Enmarcamientos de los proveedores:

- [Addy Osmani, Agent Harness Engineering](https://addyosmani.com/blog/agent-harness-engineering/)¿ Qué es esto ?`Agent = Model + Harness`y el patrón de ratchets; delgado en la infraestructura
  En el caso de los niños, el nombre de la persona que se encuentra en el lugar de residencia es el de la persona que se encuentra en el lugar de residencia.
- [LangChain, The Anatomy of an Agent Harness](https://blog.langchain.com/the-anatomy-of-an-agent-harness/) once componentes: instrucciones, herramientas, ganchos, orquestación, cajas de arena, memoria, habilidades, sub-gentes, tiempo de ejecución; omite colas, despliegue, authz
  En el caso de los niños, el nombre de la persona que se encuentra en el lugar de residencia es el de la persona que se encuentra en el lugar de residencia.
- [OpenAI, Harness engineering: leveraging Codex in an agent-first world](https://openai.com/index/harness-engineering/) La visión del equipo del Codex de las superficies alrededor de su tiempo de ejecución
  En el caso de los niños, el nombre de la persona que se encuentra en el lugar de residencia es el de la persona que se encuentra en el lugar de residencia.
- [OpenAI, Unrolling the Codex agent loop](https://openai.com/index/unrolling-the-codex-agent-loop/) el bucle de agente reducido a un `while`en llamadas de funciones
  En el caso de los niños, el nombre de la persona que se encuentra en el lugar de residencia es el de la persona que se encuentra en el lugar de residencia.
- [Anthropic, Effective harnesses for long-running agents](https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents) superficies de largo horizonte dentro de un tiempo de ejecución específico
  En el caso de los niños, el nombre de la persona que se encuentra en el lugar de residencia es el de la persona que se encuentra en el lugar de residencia.
- [Anthropic, Harness design for long-running application development](https://www.anthropic.com/engineering/harness-design-long-running-apps) notas de diseño aplicadas
  En el caso de los niños, el nombre de la persona que se encuentra en el lugar de residencia es el de la persona que se encuentra en el lugar de residencia.
- [LangChain Deep Agents harness capabilities](https://docs.langchain.com/oss/python/deepagents/harness) Superficie de configuración de tiempo de ejecución
  En el caso de los niños, el nombre de la persona que se encuentra en el lugar de residencia es el de la persona que se encuentra en el lugar de residencia.

Piezas de practicantes con detalles utilizables:

- [Martin Fowler / Birgitta Böckeler, Harness engineering for coding agent users](https://martinfowler.com/articles/harness-engineering.html) guías (feedforward) + sensores (feedback); el marco de la teoría de control más limpio
  En el caso de los niños, el nombre de la persona que se encuentra en el lugar de residencia es el de la persona que se encuentra en el lugar de residencia.
- [HumanLayer, Skill Issue: Harness Engineering for Coding Agents](https://www.humanlayer.dev/blog/skill-issue-harness-engineering-for-coding-agents)"No es un problema de modelo, es un problema de configuración"
  En el caso de los niños, el nombre de la persona que se encuentra en el lugar de residencia es el de la persona que se encuentra en el lugar de residencia.
- [MongoDB, The Agent Harness: Why the LLM Is the Smallest Part of Your Agent System](https://www.mongodb.com/company/blog/technical/agent-harness-why-llm-is-smallest-part-of-your-agent-system) recibos: Vercel del 80% al 100%, precisión Harvey 2x, Terminal Bench Top 30 al Top 5
  En el caso de los niños, el nombre de la persona que se encuentra en el lugar de residencia es el de la persona que se encuentra en el lugar de residencia.
- [Augment Code, Harness Engineering for AI Coding Agents](https://www.augmentcode.com/guides/harness-engineering-ai-coding-agents) la restricción de la primera marcha
  En el caso de los niños, el nombre de la persona que se encuentra en el lugar de residencia es el de la persona que se encuentra en el lugar de residencia.
- [Sequoia podcast, Harrison Chase on Context Engineering Long-Horizon Agents](https://sequoiacap.com/podcast/context-engineering-our-way-to-long-horizon-agents-langchains-harrison-chase/) Preocupación por el tiempo de ejecución respecto a las preocupaciones del modelo
  En el caso de los niños, el nombre de la persona que se encuentra en el lugar de residencia es el de la persona que se encuentra en el lugar de residencia.

Libros, documentos y implementaciones de referencia:

- [Jaymin West, Agentic Engineering — Chapter 6: Harnesses](https://www.jayminwest.com/agentic-engineering-book/6-harnesses) tratamiento de longitud de libro, trata el arnés como el límite de seguridad primario
  En el caso de los niños, el nombre de la persona que se encuentra en el lugar de residencia es el de la persona que se encuentra en el lugar de residencia.
- [preprints.org, Harness Engineering for Language Agents (March 2026)](https://www.preprints.org/manuscript/202603.1756) Enmarcamiento académico como control / agencia / tiempo de ejecución
  En el caso de los niños, el nombre de la persona que se encuentra en el lugar de residencia es el de la persona que se encuentra en el lugar de residencia.
- [walkinglabs/awesome-harness-engineering](https://github.com/walkinglabs/awesome-harness-engineering) Lista de lectura seleccionada en todo contexto, evaluación, observabilidad, orquestación
  En el caso de los niños, el nombre de la persona que se encuentra en el lugar de residencia es el de la persona que se encuentra en el lugar de residencia.
- [ai-boost/awesome-harness-engineering](https://github.com/ai-boost/awesome-harness-engineering) lista de selección alternativa (herramientas, evaluaciones, memoria, MCP, permisos)
  En el caso de los niños, el nombre de la persona que se encuentra en el lugar de residencia es el de la persona que se encuentra en el lugar de residencia.
- [andrewgarst/agentic_harness](https://github.com/andrewgarst/agentic_harness) Implementación de referencia lista para producción con memoria y suite de eval con respaldo de Redis
  En el caso de los niños, el nombre de la persona que se encuentra en el lugar de residencia es el de la persona que se encuentra en el lugar de residencia.
- [HKUDS/OpenHarness](https://github.com/HKUDS/OpenHarness) Arnes de agente abierto con agente personal incorporado
  En el caso de los niños, el nombre de la persona que se encuentra en el lugar de residencia es el de la persona que se encuentra en el lugar de residencia.

Hacker News vale la pena leer por los desacuerdos, no por el consenso:

> El modelo de fracaso principal incluye: instrucciones para seguir el fracaso, herramientas para usar errores, perdidas de texto y la ruptura de la cadena de cálculo.

- [HN: Effective harnesses for long-running agents](https://news.ycombinator.com/item?id=46081704)
  En el caso de los niños, el nombre de la persona que se encuentra en el lugar de residencia es el de la persona que se encuentra en el lugar de residencia.
- [HN: Improving 15 LLMs at Coding in One Afternoon. Only the Harness Changed](https://news.ycombinator.com/item?id=46988596)
  En el caso de los niños, el nombre de la persona que se encuentra en el lugar de residencia es el de la persona que se encuentra en el lugar de residencia.
- [HN: The agent harness belongs outside the sandbox](https://news.ycombinator.com/item?id=47990675) argumenta por la autorización como avión separado
  En el caso de los niños, el nombre de la persona que se encuentra en el lugar de residencia es el de la persona que se encuentra en el lugar de residencia.

Referencias cruzadas dentro de este plan de estudios:

- Fase 14 · 23  Convenciones de la GenAI de OpenTelemetry: la capa de observabilidad en la que la literatura de los sensores apunta a
- Fase 14 · 26  Catálogo de modos de falla las siete superficies están diseñadas para absorber
- Fase 14 · 27  Defensa de inyección rápida que se sitúa en la política de autorización primitiva
- Fase 14 · 29  Tiempos de ejecución de producción (cuota, evento, cron): donde los primitivos de esta lección viven en despliegue
