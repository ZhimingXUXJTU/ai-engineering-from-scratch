# OpenAI Agents SDK: Transmisiones, vigilancia, rastreo

> OpenAI Agents SDK es el marco multi-agente ligero construido sobre la API de Respuestas. Cinco primitivas: Agente, Handoff, Guardrail, Sesión, Tracing.`transfer_to_<agent>`Los guardrails se bloquean en entrada o salida.

**Type:** Learn + Build | **类型:** 构建
**Languages:** Python (stdlib) | **语言:** Python (标准库)
**Prerequisites:** Phase 14 · 01 (Agent Loop), Phase 14 · 06 (Tool Use) | **前置知识:** 见原文
**Time:** ~75 minutes | **时间:** 见原文

## Objetivos de aprendizaje

- Nombre de las cinco primitivas del OpenAI Agents SDK.
- Explica las entregas: por qué se modelan como herramientas, qué forma de nombre ve el modelo y cómo se transfiere el contexto.
- Distinguir entre barandillas de entrada, barandillas de salida y barandillas de herramientas; explicar `run_in_parallel`en modo de bloqueo.
- Implementar un tiempo de ejecución de stdlib con remesas + barandillas + rastreo de estilo span.

## El problema es la introducción del problema

Los agentes que no pueden delegar limpiamente terminan llenando todo en un solo instante. Los agentes sin barandillas envían PII, salida que viola las políticas o bucle para siempre.

> 无法干净地委派任务的代理 最终将所有东西塞进一个提示词中. 无护的代理会泄露PII. 输出违反政策内容或永远循环. OpenAI SDK hará que el trabajo de varios agentes sea manejable.


> **【中文解读】**OpenAI Agents SDK(original Swarm) es el marco de desarrollo oficial de OpenAI ▌.

> **{【拓展：OpenAI Agents SDK 是 2025-2026 年最流行的轻量级 Agent 框架。其 ...】}**OpenAI Agents SDK es el marco de agentes de menor escala más popular de 2025-2026 años. Su modelo de entrega de agentes de más de un grupo de agentes de trabajo se desarrollará para la "realización" de un agente.

> ¿ Qué es esto ?**【前置】**必须先掌握:Fase 14·01(Agent Loop) y Fase 14·06(Utilización de herramientas) OpenAI Agents SDK 就是这些概念的产品化封装──还需要熟悉OpenAI Responses API(no es la vieja Chat Complement API), puesto que el SDK se basa en Respuestas API 构建的──

## El concepto central.

### Cinco primitivos

1. **Agent.**LLM + instrucciones + herramientas + entregas.
2. **Handoff.**Delegación a otro agente. Representado en el modelo como una herramienta llamada `transfer_to_<agent_name>`¿ Qué ?
3. **Guardrail.**Validación en entrada (solo el primer agente), salida (solo el último agente) o invocación de herramienta (por herramienta de función).
4. **Session.**Historial de conversaciones automático a través de los giros.
5. **Tracing.**Esparcidas para generaciones de LLM, llamadas de herramientas, entregas, barandillas.

### Las entregas como herramientas

El modelo ve .`transfer_to_billing_agent`En su lista de herramientas.

> 模型在其工具列表中看 `transfer_to_billing_agent`调用 significa que el funcionamiento necesita:

> Los agentes de OpenAI SDK 提供四种核心概念:Agentes (ADN) 带指令和工具的LLM) ‧Handoffs (Handoffs) ‧Agent 间移交) ‧Guardrails (Guardails) 输入/输出验证) ‧Tracing (Tracking) 运行追踪) ‧ Producción (LLC) 开发框架 (Regulamiento) ‧Agent 开发框架 (Regulamiento) ‧

1. Copie el contexto de la conversación (o colapse a través de `nest_handoff_history`beta).
2. Inicializa el agente objetivo con sus instrucciones.
3. Continúe la carrera con el agente objetivo.

Este es el patrón de supervisión (lección 13 / lección 28) producido.

> Éste es el modelo de supervisor de la producción posterior.

> ¿ Qué es esto ?**【类比】**Handoff 像医院的分诊转诊:分诊台(triage agent) Escucha la descripción del paciente después de decir "tu vas al corazón"`transfer_to_cardiology_agent` pacientes (del departamento de clínicas a la de clínicas de clínicas de clínicas de clínicas de clínicas de clínicas de clínicas de clínicas de clínicas de clínicas de clínicas de clínicas de clínicas de clínicas de clínicas de clínicas de clínicas de clínicas de clínicas de clínicas de clínicas de clínicas de clínicas de clínicas de clínicas de clínicas de clínicas de clínicas de clínicas de clínicas de clínicas de clínicas de clínicas de clínicas de clínicas de clínicas de clínicas de clínicas de clínicas de clínicas de clínicas de clínicas de clínicas de clínicas de clínicas de clínicas de clínicas de clínicas de clínicas de clínicas de clínicas de clínicas de clínicas de clínicas de clínicas de clínicas de clínicas de clínicas de clínicas de clínicas de clínicas de clínicas de clínicas de clínicas de clínicas de clínicas de clínicas de clínicas de clínicas de clínicas de clínicas de clínicas de clínicas de clínicas de clínicas de clínicas de clínicas de clínicas de clínicas de clínicas de clínicas de clínicas de clínicas de clínicas de clínicas de clínicas de clínicas de clínicas de clínicas de clínicas de clínicas de clínicas de clínicas de clínicas de clínicas de clínicas de clínicas de clínicas de clínicas de clínicas de clínicas de clínicas de clínicas de clínicas de clínicas de clínicas de clínicas de clínicas de clínicas de clínicas de clínicas de clínicas de clínicas de clínicas de clínicas de clínicas de clínicas de clínicas de clínicas de clínicas de clínicas de clínicas de clínicas de clínicas de clínicas de clínicas de clínicas de clínicas de clínicas de clínicas de clínicas de clínicas de clínicas de clínicas de clínicas de clínicas de clínicas de clínicas de clínicas de clínicas de clínicas de clínicas de clínicas de clínicas de clínicas de clínicas de clínicas de clínicas de clínicas de clínicas de clínicas de clínicas de clínicas de clínicas de clínicas de clínicas de clínicas de clínicas de clínicas de clínicas de clínicas de clínicas de clínicas de clínicas de clínicas de clínicas de**关键**El control es un solo proceso, el control es totalmente transferido, el agente original no participa más.

> Los agentes de OpenAI SDK 提供四种核心概念:Agentes (ADN) 带指令和工具的LLM) ‧Handoffs (Handoffs) ‧Agent 间移交) ‧Guardrails (Guardails) 输入/输出验证) ‧Tracing (Tracking) 运行追踪) ‧ Producción (LLC) 开发框架 (Regulamiento) ‧Agent 开发框架 (Regulamiento) ‧

### Barras de seguridad

Tres sabores:

> Tres tipos:

- **Input guardrails.**Rechazar las solicitudes inseguras o fuera de alcance antes de cualquier llamada de LLM.
- **Output guardrails.**Busca la salida del último agente, detecta filtraciones de PII, violaciones de políticas, respuestas malformadas.
- **Tool guardrails.**Ejecutar por herramienta de función, validar argumentos, verificar permisos, ejecutar auditorías.

Modo de trabajo:

> 模式:

- **Parallel**(por defecto). Guardrail LLM se ejecuta junto con el LLM principal.
- **Blocking**(El artículo`run_in_parallel=False`Guardrail LLM se ejecuta primero. si se tropieza, no se desperdician fichas en la llamada principal.

Los trifiles se elevan .`InputGuardrailTripwireTriggered`- ¿ Qué ?`OutputGuardrailTripwireTriggered`¿ Qué ?

> 触发器会抛出 `InputGuardrailTripwireTriggered`- ¿ Qué ?`OutputGuardrailTripwireTriggered`异常── es muy raro.

> Los agentes de OpenAI SDK 提供四种核心概念:Agentes (ADN) 带指令和工具的LLM) ‧Handoffs (Handoffs) ‧Agent 间移交) ‧Guardrails (Guardails) 输入/输出验证) ‧Tracing (Tracking) 运行追踪) ‧ Producción (LLC) 开发框架 (Regulamiento) ‧Agent 开发框架 (Regulamiento) ‧

### Trazación

Cada generación de LLM, llamada de herramientas, entrega y baranda emite un tiempo.`OPENAI_AGENTS_DISABLE_TRACING=1`Opta por salir.`add_trace_processor(processor)`Los fans se extienden a su propio backend junto con OpenAI.

> 默认开启── cada LLM 生成、工具调用、交接和护都发出一个跨度──`OPENAI_AGENTS_DISABLE_TRACING=1`Puede elegir salir.`add_trace_processor(processor)`Puede ser enviado al mismo tiempo que envía a su propio extremo y al extremo posterior de OpenAI.

> Los agentes de OpenAI SDK 提供四种核心概念:Agentes (ADN) 带指令和工具的LLM) ‧Handoffs (Handoffs) ‧Agent 间移交) ‧Guardrails (Guardails) 输入/输出验证) ‧Tracing (Tracking) 运行追踪) ‧ Producción (LLC) 开发框架 (Regulamiento) ‧Agent 开发框架 (Regulamiento) ‧

### Sesiones

`Session`almacena el historial de conversaciones en un backend (SQLite, Redis, personalizado). `Runner.run(agent, input, session=session)`cargas automáticas y apéndices.

> `Session`En el último momento, el equipo de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de la organización de las redes de las redes de las redes de las redes de las redes de las redes de las redes de las redes de las redes de las redes de las redes de las redes de las redes de las redes de las redes de las redes de las redes de las redes de las redes de las redes de las redes de las redes de las redes de las redes de las redes de las redes de las redes de las redes de las redes de las redes de las redes de las redes de las redes de las redes de las redes de las redes de las redes de las redes.`Runner.run(agent, input, session=session)`Autocarga y adición.

> Los agentes de OpenAI SDK 提供四种核心概念:Agentes (ADN) 带指令和工具的LLM) ‧Handoffs (Handoffs) ‧Agent 间移交) ‧Guardrails (Guardails) 输入/输出验证) ‧Tracing (Tracking) 运行追踪) ‧ Producción (LLC) 开发框架 (Regulamiento) ‧Agent 开发框架 (Regulamiento) ‧

### Cuando este patrón va mal

> ️ **【易错点】**Drift de entrega: Agente A 移交给 B,B 又移交给 A,A 再移交给 B... token de ciclo de quemadura ilimitado。**后果**¡Cuánto tiempo hay en el mundo!**一行修复**: en el corredor 里加跳 counter`max_handoffs=5`), más que la`HandoffBudgetExceeded`异常──OpenAI SDK 默认没有这个保护,必须自己加──

- **Handoff drift.**Agente A se entrega al Agente B que se entrega al Agente A. Añade un contador de saltos.
- **Guardrail bypass.**Las barandillas de herramientas solo disparan a herramientas de función; las herramientas incorporadas (lector de archivos, recoger web) necesitan una política separada.
- **Over-tracing.**Contenido sensible en intervalos. empareja con las reglas de captura de contenido de OTel GenAI (lección 23)  almacenaje externo, referencia por ID.

> ¿ Qué es esto ?**【困惑】**P: Paralelo de guardrail y bloqueo 模式怎么选? look parallel 总是更快── A: 不一定──Parallel es "primero guardrail 和 guardrail LLM 同时跑"快但浪费代币(guardrail 触发时时主 LLM 已经在运行,代币 已经花了)──Bloqueo es "primer guardrail,过了再主 LLM"慢但省钱──**选择规则**Si el barranco de seguridad 触发率高 (por ejemplo, >20%), utiliza el bloqueo de 省钱; si el índice de触发率 es bajo (por ejemplo, <5%), utiliza el paralelos 省延迟。

> **交接漂移。**Agente A 交交给Agente B,Agente B también交交回Agente A 添加跳数计器
> **护栏绕过。**工具护 只有在函数工具上触发;内置工具(文件读取器、网页抓取) requiere estrategias individuales。
> **过度追踪。**Espacio de contenido sensible. 配合 OTel GenAI 内容捕获规则 (第 23 课) 使用外部存储,按ID 引用──

## Construye y realiza.
```figure
ae-agent-handoff
```

## Construye el mismo

`code/main.py`Implementa la forma SDK en stdlib:

> `code/main.py`Utilizando el estándar de la biblioteca se ha realizado la forma de SDK:

> Los agentes de OpenAI SDK 提供四种核心概念:Agentes (ADN) 带指令和工具的LLM) ‧Handoffs (Handoffs) ‧Agent 间移交) ‧Guardrails (Guardails) 输入/输出验证) ‧Tracing (Tracking) 运行追踪) ‧ Producción (LLC) 开发框架 (Regulamiento) ‧Agent 开发框架 (Regulamiento) ‧

- `Agent`¿ Qué ?`FunctionTool`¿ Qué ?`Handoff`(como herramienta de función con semántica de transferencia).
- `Runner`con barandillas de entrada/salida/herramienta, despacho de entrega y contador de salto.
- Un simple emisor de espacio para mostrar la forma de la huella.
- Un agente de triaje que entrega a la facturación o soporte basado en la consulta del usuario; viajes de baranda de seguridad en una entrada.

- ¿Qué quieres decir ?

```
python3 code/main.py
```

El rastro muestra dos entregas exitosas, un viaje de entrada en el barranco de seguridad y un árbol de espalda que refleja lo que emite el SDK real.

>                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                              

> Los agentes de OpenAI SDK 提供四种核心概念:Agentes (ADN) 带指令和工具的LLM) ‧Handoffs (Handoffs) ‧Agent 间移交) ‧Guardrails (Guardails) 输入/输出验证) ‧Tracing (Tracking) 运行追踪) ‧ Producción (LLC) 开发框架 (Regulamiento) ‧Agent 开发框架 (Regulamiento) ‧

## Usalo con el marco de ejecución

- **OpenAI Agents SDK**para los productos OpenAI-first.
- **Claude Agent SDK**(Ley 17) para los productos de primera clase.
- **LangGraph**(Lección 13) cuando quieres un estado explícito y un currículum duradero.
- **Custom**cuando se necesita un control exacto (voz, multi-proveedor, implementaciones federadas).

## Envíe el producto .

`outputs/skill-agents-sdk-scaffold.md`plancha una aplicación de Agents SDK con un agente de triaje, manchas, barandillas de entrada/salida/herramienta, almacenamiento de sesiones y un procesador de rastreo.

> `outputs/skill-agents-sdk-scaffold.md`construir un SDK de agentes  aplicación, que incluye un procesador de almacenamiento y seguimiento de agentes 交接、输入/输出/工具护、会话存储和追踪处理器──

> Los agentes de OpenAI SDK 提供四种核心概念:Agentes (ADN) 带指令和工具的LLM) ‧Handoffs (Handoffs) ‧Agent 间移交) ‧Guardrails (Guardails) 输入/输出验证) ‧Tracing (Tracking) 运行追踪) ‧ Producción (LLC) 开发框架 (Regulamiento) ‧Agent 开发框架 (Regulamiento) ‧

## Los ejercicios.

1. Añadir un contador de saltos de entrega: rechazar después de N transferencias.
  En inglés, "pensar y practicar" significa "pensar y practicar".
2. Implementación `nest_handoff_history`como opción  desglosar los mensajes anteriores en un resumen antes de transferirlos.
  En inglés, "pensar y practicar" significa "pensar y practicar".
3. Escribe un barranco de salida bloqueador. Compara la latencia en las instrucciones que lo tropezarían con las que pasan.
  En inglés, "pensar y practicar" significa "pensar y practicar".
4. El cable`add_trace_processor`¿Qué forma emite por período?
  En inglés, "pensar y practicar" significa "pensar y practicar".
5. Lea los documentos del SDK y porta su juguete a SDK.`openai-agents-python`¿Qué modelo mal ha dado?
  En inglés, "pensar y practicar" significa "pensar y practicar".

## Términos clave .

| Term | What people say | What it actually means |
|------|----------------|------------------------|---|
| Agent | "LLM + instructions" | Agent type in the SDK; owns tools and handoffs |  |
| Handoff | "Transfer" | Tool the model calls to delegate to another agent |  |
| Guardrail | "Policy check" | Validation on input / output / tool invocation |  |
| Tripwire | "Guardrail trip" | Exception raised when guardrail rejects |  |
| Session | "History store" | Conversation memory persisted between runs |  |
| Tracing | "Spans" | Built-in observability over LLM + tool + handoff + guardrail |  |
| Blocking guardrail | "Sequential check" | Guardrail runs first; no token waste on trip |  |
| Parallel guardrail | "Concurrent check" | Guardrail runs alongside; lower latency, wastes tokens on trip |  |

## Más Leer más Leer más

- [OpenAI Agents SDK docs](https://openai.github.io/openai-agents-python/) primitivos, entregas, barandillas, rastreo
  En el caso de los niños, el nombre de la persona que se encuentra en el lugar de residencia es el de la persona que se encuentra en el lugar de residencia.
- [Claude Agent SDK overview](https://platform.claude.com/docs/en/agent-sdk/overview) Colega con sabor a claudio
  En el caso de los niños, el nombre de la persona que se encuentra en el lugar de residencia es el de la persona que se encuentra en el lugar de residencia.
- [Anthropic, Building Effective Agents](https://www.anthropic.com/research/building-effective-agents) Cuando se llegan a las ofertas
  En el caso de los niños, el nombre de la persona que se encuentra en el lugar de residencia es el de la persona que se encuentra en el lugar de residencia.
- [OpenTelemetry GenAI semantic conventions](https://opentelemetry.io/docs/specs/semconv/gen-ai/) el SDK estándar de Agents abarca el mapa a
  En el caso de los niños, el nombre de la persona que se encuentra en el lugar de residencia es el de la persona que se encuentra en el lugar de residencia.
