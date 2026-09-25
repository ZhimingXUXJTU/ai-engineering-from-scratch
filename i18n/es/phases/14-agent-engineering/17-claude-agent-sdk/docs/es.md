# Subagents y la tienda de sesiones
# El arnés como biblioteca  Subbagents y tienda de sesiones

> Un arnés que puede importar: herramientas incorporadas, subagentes para aislamiento de contexto, ganchos, propagación de rastros W3C, persistencia de sesión. El SDK de agente Claude es el ejemplo de referencia  la forma de biblioteca del arnés de código Claude  y Claude Managed Agents es la alternativa alojada para el trabajo de sincronización de larga duración.

**Type:** Learn + Build | **类型:** 构建
**Languages:** Python (stdlib) | **语言:** Python (标准库)
**Prerequisites:** Phase 14 · 01 (Agent Loop), Phase 14 · 10 (Skill Libraries) | **前置知识:** 见原文
**Time:** ~75 minutes | **时间:** 见原文

## Objetivos de aprendizaje

- Explique la diferencia entre el SDK del cliente antropico (API prima) y el SDK del agente Claude (forma de arnés).
- Describa los subgentes  paralelación y aislamiento de contexto  y cuándo alcanzarlos.
- Nombre de la superficie de almacenamiento de sesión del SDK Python (`append`¿ Qué ?`load`¿ Qué ?`list_sessions`¿ Qué ?`delete`¿ Qué ?`list_subkeys`) y el papel de `--session-mirror`¿ Qué ?
- Implemente un arnés stdlib con herramientas incorporadas, desove subagente con contexto aislado, ganchos de ciclo de vida y una tienda de sesiones.

## El problema es la introducción del problema

Una API de LLM crudo te da un viaje de ida y vuelta. Un agente de producción necesita ejecución de herramientas, servidores MCP, ganchos de ciclo de vida, desove subagente, persistencia de sesión, propagación de huellas. Claude Agent SDK envía esta forma como una biblioteca  el mismo arnés que Claude Code utiliza, expuesto para agentes personalizados.

> El primer programa de LLM en el mundo de la tecnología de la información, el primer programa de la tecnología de la información, el primer programa de la tecnología de la información, el segundo programa de la tecnología de la información, el segundo programa de la tecnología de la información, el segundo programa de la tecnología de la información, el segundo programa de la tecnología de la información, el segundo programa de la tecnología de la información, el segundo programa de la tecnología de la información, el segundo programa de la tecnología de la información, el segundo programa de la tecnología de la información, el segundo programa de la tecnología de la información, el segundo programa de la tecnología de la información, el segundo programa de la tecnología de la información, el segundo programa de la tecnología de la información, el segundo programa de la tecnología de la información, el segundo programa de la tecnología de la información, el segundo programa de la tecnología de la información, el segundo programa de la tecnología de la información, el segundo programa de la tecnología de la tecnología de la información, el segundo programa de la tecnología de la tecnología de la información, el segundo programa de la tecnología de la tecnología de la tecnología de la información, el segundo programa de la tecnología de la tecnología de la tecnología de la tecnología de la tecnología, el segundo programa de la tecnología de la tecnología de la tecnología de la tecnología de la tecnología de la tecnología, el segundo de la tecnología de la tecnología de la tecnología de la tecnología de la tecnología de la tecnología de la tecnología de la tecnología de la tecnología de la tecnología de la tecnología de la tecnología de la tecnología de la tecnología de la tecnología de la tecnología de la tecnología de la tecnología de la tecnología de la tecnología de la tecnología de la tecnología de la tecnología de la tecnología de la tecnología de la tecnología de la tecnología de la tecnología de la tecnología de la tecnología de la tecnología de la tecnología de la tecnología de la tecnología de la tecnología de la tecnología de la tecnología de la tecnología de la tecnología de la tecnología de la tecnología de la tecnología de la tecnología de la tecnología de la tecnología de la tecnología de la tecnología de la tecnología de la tecnología de la tecnología de la tecnología de la tecnología de la tecnología de la tecnología de la tecnología de la tecnología de la tecnología de la tecnología de la tecnología de la tecnología de la tecnología de la tecnología de la tecnología de la tecnología de la tecnología de la tecnología de la tecnología de la tecnología de la tecnología de la tecnología de la tecnología de la tecnología de la tecnología de la tecnología de la tecnología de la tecnología de


> **【中文解读】**Claude Agent SDK es un sistema de desarrollo de agentes 官方的 开发框架──核心特性:(1) 内置工具(文件读写、代码执行等);(2) 子 Agent 支持Agent 可以生成子 Agent 处理子任务;(3) 生命周期子在 Agent 执行的关键节点插入自定义逻辑──SDK 深度集成 Claude 的扩展思维能力──

> **{【拓展：Claude Agent SDK 是 2026 年 Claude 生态的核心开发工具。与 OpenA...】}**Claude Agent SDK es un instrumento de desarrollo central de Claude en el contexto de 2026 . En comparación con OpenAI Agents SDK, se centra más en la integración profunda de las capacidades únicas de Claude (como el pensamiento extendido, uso de computadoras).

> ¿ Qué es esto ?**【前置】**必须先掌握:Phase 14·01(Agent Loop) yPhase 14·10(Skill Libraries) Claude Agent SDK 内置了技能 系统作为子 Agent的标准模式── Si no has usado el código Claude CLI, recomienda fuertemente que primero uses unos días本 SDK, es decir, la forma de código Claude, para entender el modelo de comportamiento del CLI para aprender el SDK.

## El concepto central.

### SDK del cliente vs SDK del agente

- **Client SDK (`anthropic`).**Eres dueño del bucle, de las herramientas, del estado.
- **Agent SDK (`claude-agent-sdk`).**Ejecución de herramientas integradas, conexiones MCP, ganchos, desove subagente, almacenamiento de sesiones.

> **Client SDK（`anthropic`）。**El código de código de las redes sociales de los usuarios es el código de código de las redes sociales.
> **Agent SDK（`claude-agent-sdk`）。**Introducción de la información sobre el código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de

### Herramientas incorporadas

El SDK envía más de 10 herramientas de la caja: lectura/escritura de archivos, shell, grep, glob, web fetch, etc. Herramientas personalizadas se registran a través de la interfaz estándar de esquema de herramientas.

> SDK 开箱提供 10+ 工具:文件读写、shell、grep、glob、网页抓取等──自定义工具通过标准工具-schema 接口注册──

> Claude Agent SDK es el agente oficial de Anthropic 框架──核心概念:Agent: 带系统提示和工具的 LLM) ‧Tools: 可调用函数: ‧Subbagents: 子代理委派: ‧Session Store: 会话持久化: ‧

### Sub-cargas

Dos propósitos documentados por Anthropic:

> El Antropic 文档 registró dos usos:

1. **Parallelization.**Realizar trabajo independiente simultáneamente. "Encuentra el archivo de prueba para cada uno de estos 20 módulos" es 20 tareas paralelas de subagente.
2. **Context isolation.**Los subjugadores utilizan su propia ventana de contexto; sólo los resultados regresan al orquestrador.

Python SDK recientes adiciones: `list_subagents()`¿ Qué ?`get_subagent_messages()`para leer las transcripciones de subagento.

> Python SDK recientes nuevas funciones:`list_subagents()`¿Qué es esto?`get_subagent_messages()`Para leer el registro de conversaciones del agente.

> ¿ Qué es esto ?**【类比】**Los agentes de la empresa tienen una "junta de proyectos" independiente.**关键收益是上下文隔离**Si "调研竞品" de este tipo de trabajo se leían 100 artículos llenos de abajo, el agente principal se hizo en su propio lugar y se inundaría; entregado a su hijo agente, hijo agente de 100 artículos lectura no contaminará el punto de vista del agente principal, sólo regresar a " 3 conclusiones del análisis de la oferta " .

> Claude Agent SDK es el agente oficial de Anthropic 框架──核心概念:Agent: 带系统提示和工具的 LLM) ‧Tools: 可调用函数: ‧Subbagents: 子代理委派: ‧Session Store: 会话持久化: ‧

### Tienda de sesiones

Paridad de protocolo con TypeScript:

> Con el tipo de versión de tipo de texto:

- `append(session_id, message)` añadir un giro.
- `load(session_id)` restaurar la conversación.
- `list_sessions()` enumerar.
- `delete(session_id)` con sesiones en cascada a subagentes.
- `list_subkeys(session_id)` lista de las claves de subagente.

`--session-mirror`(Bandereta CLI) refleja la transcripción a un archivo externo mientras fluye, para depurar.

> `--session-mirror`(CLI 标志) Durante la transmisión en curso, el diálogo se registrará en un archivo externo, para su uso en la prueba.

> Claude Agent SDK es el agente oficial de Anthropic 框架──核心概念:Agent: 带系统提示和工具的 LLM) ‧Tools: 可调用函数: ‧Subbagents: 子代理委派: ‧Session Store: 会话持久化: ‧

### Los ganchos

Los ganchos de ciclo de vida que se pueden registrar:

> Registro de ciclo de vida:

- `PreToolUse`¿ Qué ?`PostToolUse` llamadas de puerta o de herramienta de auditoría.
- `SessionStart`¿ Qué ?`SessionEnd`- Construir y derribar.
- `UserPromptSubmit` actuar sobre la entrada del usuario antes de que el modelo la vea.
- `PreCompact` ejecutarse antes de la compactación del contexto.
- `Stop` limpieza en la salida del agente.
- `Notification` Alertas de canales laterales.

Los ganchos son la forma en que los flujos de trabajo (referencia del currículo de la Fase 14) y sistemas similares añaden comportamiento transversal.

> 子是专业工作流 (Fase 14 课程参考) y similar sistemas añadir métodos de conducta transversal.

> Claude Agent SDK es el agente oficial de Anthropic 框架──核心概念:Agent: 带系统提示和工具的 LLM) ‧Tools: 可调用函数: ‧Subbagents: 子代理委派: ‧Session Store: 会话持久化: ‧

### Contexto de la traza W3C

Las extensiones de OTel activas en el llamador se propagan al subproceso CLI a través de los encabezados de contexto de rastreo W3C.

> 调用方上活跃的OTel span 通过W3C 追踪上下文头传播到CLI 子进程──整个多进程追踪在你的后端显示为一个追踪──

> Claude Agent SDK es el agente oficial de Anthropic 框架──核心概念:Agent: 带系统提示和工具的 LLM) ‧Tools: 可调用函数: ‧Subbagents: 子代理委派: ‧Session Store: 会话持久化: ‧

### Claude manejaba a los agentes

La alternativa alojada (título beta `managed-agents-2026-04-01`La gestión de la información en el mercado de la información y la información en el mercado de la información.

> 托管替方案  头`managed-agents-2026-04-01`•■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■

> Claude Agent SDK es el agente oficial de Anthropic 框架──核心概念:Agent: 带系统提示和工具的 LLM) ‧Tools: 可调用函数: ‧Subbagents: 子代理委派: ‧Session Store: 会话持久化: ‧

### Cuando este patrón va mal

> ️ **【易错点】**El desastre más común es que 100 pequeñas tareas generan 100 agentes.**后果**Cada agente tiene su propio sistema de respuesta + 工具注册 + 上下文初始化,开销 30-60 秒/个,100 个就是 1 小时;并发又有限制(Antropic cada minuto token 限制),最终任务跑一晚上──**一行修复**En el caso de los equipos de investigación, el equipo de investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de los resultados de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de los resultados de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de los resultados de la

- **Subagent over-spawn.**Desprender 100 subagentes para 100 tareas pequeñas.
- **Hook creep.**Cada equipo añade ganchos, globos de tiempo de inicio, revisa ganchos trimestralmente.
- **Session bloat.**Las sesiones se acumulan, el tamaño crece.`list_sessions`+ Política de vencimiento.

> ¿ Qué es esto ?**【困惑】**P: ¿Qué es lo que realmente se diferencia? ¿Por qué usar SDK?**内置工具开箱即用**(文件、shell、grep 等 10+ 工具, yo mismo escribir al menos dos días);(2) **Session 持久化协议**(incluido:子 Agent 会话级联删除);(3) **Hook 生命周期**(PreToolUse、PostCompact etc 7 个子点) ⋅ Si tu agente 只是简单问答, utiliza SDK antropico就足; si tienes que escribir Claude Code 那种生产级 Agent,SDK 省你几周工程时间──

> **子 Agent 过度生成。**Para 100 个小任务生成 100 个子代理――开销占主导――改为批量处理――
> **钩子膨胀。**Cada equipo añade tiempo; el tiempo de inicio se expande.
> **会话膨胀。**El uso de la palabra "casa" se hace en el idioma español.`list_sessions`+ 过期策略──

## Construye y realiza.
```figure
ae-subagent-isolation
```

## Construye el mismo

`code/main.py`Implementa la forma SDK en stdlib:

> `code/main.py`Utilizando el estándar de la biblioteca se ha realizado la forma de SDK:

> Claude Agent SDK es el agente oficial de Anthropic 框架──核心概念:Agent: 带系统提示和工具的 LLM) ‧Tools: 可调用函数: ‧Subbagents: 子代理委派: ‧Session Store: 会话持久化: ‧

- `Tool`¿ Qué ?`ToolRegistry`con incorporado `read_file`¿ Qué ?`write_file`¿ Qué ?`list_dir`¿ Qué ?
- `Subagent` contexto privado, ejecución aislada, resultados devueltos.
- `SessionStore` añadir, cargar, listar, borrar, list_subkey.
- `Hooks`¿ Qué es esto ?`pre_tool_use`¿ Qué ?`post_tool_use`¿ Qué ?`session_start`¿ Qué ?`session_end`¿ Qué ?
- Una demostración: el agente principal genera 3 subpagentes en paralelo (cada uno aislado), agrega los resultados, persiste la sesión.

- ¿Qué quieres decir ?

```
python3 code/main.py
```

El rastro muestra el aislamiento de contexto subagente (el tamaño del contexto del orquestrador se mantiene limitado), la ejecución del gancho y la persistencia de la sesión.

> 追踪显示子 Agent的上下文隔离(编排者上下文大小保持有界) 子执行和会话持久化──

> Claude Agent SDK es el agente oficial de Anthropic 框架──核心概念:Agent: 带系统提示和工具的 LLM) ‧Tools: 可调用函数: ‧Subbagents: 子代理委派: ‧Session Store: 会话持久化: ‧

## Usalo con el marco de ejecución

- **Claude Agent SDK**para productos de Claude-first que quieren la forma de arnés de código Claude.
- **Claude Managed Agents**para el trabajo de asíncrono de larga duración alojado.
- **OpenAI Agents SDK**(Ley 16) para las contrapartes de OpenAI-primero.
- **LangGraph + custom tools**Si quieres la máquina de estado en forma de gráfico en su lugar.

## Envíe el producto .

`outputs/skill-claude-agent-scaffold.md`plantillas de una aplicación de Claude Agent SDK con subagents, ganchos, almacenamiento de sesiones, servidor MCP adjunto, y W3C de la propagación de rastros.

> `outputs/skill-claude-agent-scaffold.md`construir un SDK de Agente Claude  aplicación, contenido en Agente 子、会话存储、MCP 服务器连接和 W3C 追踪传播──

> Claude Agent SDK es el agente oficial de Anthropic 框架──核心概念:Agent: 带系统提示和工具的 LLM) ‧Tools: 可调用函数: ‧Subbagents: 子代理委派: ‧Session Store: 会话持久化: ‧

## Los ejercicios.

1. Añadir un deslizador de subbagentes que agrupa 20 tareas en grupos de 5 subbagentes paralelos. Medir el tamaño del contexto del orquestrador frente a uno por tarea.
  En inglés, "pensar y practicar" significa "pensar y practicar".
2. Implementar una `PreToolUse`Cuelga ese límite de tarifas `write_file`Las llamadas (5 minutos por sesión).
  En inglés, "pensar y practicar" significa "pensar y practicar".
3. El cable`list_subkeys`¿Cómo es el anidamiento profundo?
  En inglés, "pensar y practicar" significa "pensar y practicar".
4. Llevar el juguete al real `claude-agent-sdk`¿Qué cambios hay en el registro de herramientas?
  En inglés, "pensar y practicar" significa "pensar y practicar".
5. ¿Cuándo pasarías de auto-host a administrado?
  En inglés, "pensar y practicar" significa "pensar y practicar".

## Términos clave .

| Term | What people say | What it actually means |
|------|----------------|------------------------|---|
| Agent SDK | "Claude Code as a library" | Harness shape: tools, MCP, hooks, subagents, session store |  |
| Subagent | "Child agent" | Separate context, own budget; results bubble up |  |
| Session store | "Conversation DB" | Persist, load, list, delete turns with subagent cascade |  |
| Hook | "Lifecycle callback" | Pre/post tool, session, prompt submit, compact, stop |  |
| W3C trace context | "Cross-process trace" | Parent span propagates into CLI subprocess |  |
| Managed Agents | "Hosted harness" | Anthropic-hosted long-running async work |  |
| `--session-mirror` | "Transcript mirror" | Writes session turns to an external file as they stream |  |
| MCP server | "Tool surface" | External tool/resource source attached to the agent |  |

## Más Leer más Leer más

- [Claude Agent SDK overview](https://platform.claude.com/docs/en/agent-sdk/overview) la forma de biblioteca de Claude Code
  En el caso de los niños, el nombre de la persona que se encuentra en el lugar de residencia es el de la persona que se encuentra en el lugar de residencia.
- [Anthropic, Building agents with the Claude Agent SDK](https://www.anthropic.com/engineering/building-agents-with-the-claude-agent-sdk) patrones de producción
  En el caso de los niños, el nombre de la persona que se encuentra en el lugar de residencia es el de la persona que se encuentra en el lugar de residencia.
- [Claude Managed Agents overview](https://platform.claude.com/docs/en/managed-agents/overview) alternativa alojada
  En el caso de los niños, el nombre de la persona que se encuentra en el lugar de residencia es el de la persona que se encuentra en el lugar de residencia.
- [OpenAI Agents SDK](https://openai.github.io/openai-agents-python/) contraparte
  En el caso de los niños, el nombre de la persona que se encuentra en el lugar de residencia es el de la persona que se encuentra en el lugar de residencia.
