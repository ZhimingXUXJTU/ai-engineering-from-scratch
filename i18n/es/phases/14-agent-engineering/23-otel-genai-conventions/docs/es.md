# OpenTelemetry GenAI Semántica Convenciones 约定 GenAI METR

> El SIG GenAI de OpenTelemetry (lanzado en abril de 2024) define el esquema estándar para la telemetría de agentes. Los nombres de espacios, atributos y reglas de captura de contenido convergen entre los proveedores, por lo que los rastros de agentes significan lo mismo en Datadog, Grafana, Jaeger y Honeycomb.

**Type:** Learn + Build | **类型:** 构建
**Languages:** Python (stdlib) | **语言:** Python (标准库)
**Prerequisites:** Phase 14 · 13 (LangGraph), Phase 14 · 24 (Observability Platforms) | **前置知识:** 见原文
**Time:** ~60 minutes | **时间:** 见原文

## Objetivos de aprendizaje

- Nombre de las categorías de género de genAI: modelo/cliente, agente, herramienta.
- Distinguir`invoke_agent`CLIENT vs INTERNAL y cuando cada uno se aplica.
- Enumera los atributos de nivel superior de GenAI: nombre del proveedor, modelo de solicitud, ID de fuente de datos.
- Explica el contrato de captura de contenido: optar por participar, `OTEL_SEMCONV_STABILITY_OPT_IN`, recomendación de referencia externa.

## El problema es la introducción del problema

> **【中文解读】**Cada proveedor ha inventado su propio nombre de extensión, y el equipo de transporte necesita finalmente construir un instrumento independiente para cada marco.

Cada proveedor inventa sus propios nombres de espacio. los equipos de operaciones terminan construyendo paneles de control por marco. el SIG GenAI de OpenTelemetry corrige esto definiendo un estándar para todos los objetivos del ecosistema.

> Cada proveedor ha inventado su propio rango de distribución. El equipo de transporte necesita finalmente construir un instrumento independiente para cada marco.

> **【拓展：OTel GenAI 规范的跨平台统一】**OpenTelemetry GenAI 语义约定 (2024年4月启动) 定义 Agent 遥测的标准方案:span 名称、属性和内容捕获规则跨供应商统一,使 Agent 追踪在 Datadog、Grafana、Jaeger 和 Honeycomb 中具有相同语义──一次埋点,多后端通用──

> ¿ Qué es esto ?**【前置】**学本节前 請先掌握:Fase 14·01(Agent Loop) 你需要先有 Agent 才能给它埋点;Fase 14·13(LangGraph) 理解状态图,因为 span 的父子层级就是图遍历的镜像──如果完全没有接触过OpenTelemetry(不知道什么是 span、trace、text propagation),先看OTel 官方 Python 快速进入本节只讲 GenAI 专属约定,不重讲 OT基础 ⋅

## El concepto central.

### Categorías de extensión

> ¿ Qué es esto ?**【类比】**Los tres tipos de OTel GenAI tienen un rango similar a los registros de clínicas de los hospitales:**Model span**Es la prueba más baja, el registro "extrajo mucha sangre"", con qué instrumentos"", resultados cuánto" a la señal de la respuesta números"",nombre de modelo"",tarte);**Agent span**Es el proceso completo de la enfermedad desde el número de la que se encuentra hasta la salida, que incluye varias experiencias.**Tool span**Es un proyecto de control. Cada vez son un solo proceso.`parent_span_id`链回父记录这样 Datadog 里你能展开看: Todo el agente 调用 → 5 veces herramienta调用 → Cada vez herramienta调用里 2 veces LLM 调用──

1. **Model / client spans.**Cubre las llamadas de LLM crudas. Emitidas por los SDKs (Antropic, OpenAI, Bedrock) y adaptadores de modelos de marco.
2. **Agent spans.** `create_agent`(cuando se construye el agente) y `invoke_agent`(cuando se ejecuta).
3. **Tool spans.**Una por invocación de herramienta; conectada a la franja de agentes por relación padre-hijo.

### Nombramiento del agente span

- Nombre español: `invoke_agent {gen_ai.agent.name}`si se nombra; regreso a `invoke_agent`¿ Qué ?
- Tipo de espán:
  - **CLIENT** para los servicios de agentes remotos (OpenAI Assistants API, Bedrock Agents).
  - **INTERNAL** para los marcos de agentes en proceso (LangChain, CrewAI, local ReAct).

### Los atributos clave

- `gen_ai.provider.name`¿ Qué es esto ?`anthropic`¿ Qué ?`openai`¿ Qué ?`aws.bedrock`¿ Qué ?`google.vertex`¿ Qué ?
- `gen_ai.request.model` el modelo de identificación.
- `gen_ai.response.model` el modelo resuelto (puede diferir de la solicitud debido al enrutamiento).
- `gen_ai.agent.name`Identificación del agente.
- `gen_ai.operation.name`¿ Qué es esto ?`chat`¿ Qué ?`completion`¿ Qué ?`invoke_agent`¿ Qué ?`tool_call`¿ Qué ?
- `gen_ai.data_source.id` para RAG: qué cuerpo o almacén se consultó.

Existen convenciones específicas de tecnología para Anthropic, Azure AI Inference, AWS Bedrock, OpenAI.

> OpenTelemetry GenAI 语义约定 define los estándares de observabilidad de LLM y de Agente.`gen_ai.request.model`¿Qué es esto?`gen_ai.usage.input_tokens`¿Qué es esto?`gen_ai.agent.name`Y así.

### Captura de contenido

> ️ **【易错点】**场景: desarrollador `invoke_agent`span 里把完整提示(含用户 PII、API key、客户合同条款) como atributo 直接塞进去 → 后果:运维在Jaeger 网页里点开就能看到所有的明文,Datadog también hará un índice de hacer un buscador de texto completo, igual que poner en práctica el riesgo de extenderse a toda la cadena de observación → 修复:默认关闭内容 capture,需要时只在 span 里存指针 ID(`gen_ai.input.message_id=row42`), original落到带带 ACL's对象存储 S3 里,运维要查时通过 ID 跳转授权访问──这是本节反复强调的"recomendación de referencia externa"──

La regla predeterminada: las instrumentaciones NO DEVEN capturar entradas/salidas por defecto.

> OpenTelemetry GenAI 语义约定 define los estándares de observabilidad de LLM y de Agente.`gen_ai.request.model`¿Qué es esto?`gen_ai.usage.input_tokens`¿Qué es esto?`gen_ai.agent.name`Y así.

- `gen_ai.system_instructions`
- `gen_ai.input.messages`
- `gen_ai.output.messages`

El patrón de producción recomendado: almacenar contenido externamente (S3, su registro de almacenamiento), registrar referencias en intervalos (ID de puntero, no en prosa). Esta es la Lección 27 de la defensa contra la intoxicación de contenido cableada en observabilidad.

> 的生产模式:将内容外部存储(S3、你的日志存储),在 span 上记录引用(指针 ID,不是原文) .

> OpenTelemetry GenAI 语义约定 define los estándares de observabilidad de LLM y de Agente.`gen_ai.request.model`¿Qué es esto?`gen_ai.usage.input_tokens`¿Qué es esto?`gen_ai.agent.name`Y así.

### Estabilidad

La mayoría de las convenciones son experimentales a partir de marzo de 2026.

> OpenTelemetry GenAI 语义约定 define los estándares de observabilidad de LLM y de Agente.`gen_ai.request.model`¿Qué es esto?`gen_ai.usage.input_tokens`¿Qué es esto?`gen_ai.agent.name`Y así.

```
OTEL_SEMCONV_STABILITY_OPT_IN=gen_ai_latest_experimental
```

Datadog v1.37+ mapas GenAI atribuye nativamente a su esquema de observabilidad LLM. Otros fondos (Grafana, Honeycomb, Jaeger) apoyan los atributos crudos.

> ¿ Qué es esto ?**【困惑】**P: `invoke_agent`A: 看被调用的代理不是"另一个进程/服务"──如果直接在Python 进程中导入 LangChain 运行一个 ReAct,这是 INTERNAL你的自己代码内的子调用──如果调调 OpenAI Asistentes API o AWS Bedrock Agents,那就是远程HTTP调用,标点客户端──CLIENT span也会自动带 RPC 相关属性如(`rpc.system`¿Qué es esto?`rpc.service`), la facilidad y la tradición de seguimiento de los servicios

> Datadog v1.37+ 原生将 GenAI 属性映射到其LLM Observability schema──其他后端(Grafana、Honeycomb、Jaeger)支持原始属性──

> OpenTelemetry GenAI 语义约定 define los estándares de observabilidad de LLM y de Agente.`gen_ai.request.model`¿Qué es esto?`gen_ai.usage.input_tokens`¿Qué es esto?`gen_ai.agent.name`Y así.

### Cuando este patrón va mal

- **Capturing full prompts in spans.**Información personal, secretos, datos de clientes en rastros que las operaciones pueden leer.
- **No `gen_ai.provider.name`.**Los tableros de múltiples proveedores se rompen cuando falta la atribución.
- **Spans without parent links.**Las herramientas huérfanas se extienden, siempre propagan el contexto.
- **Not setting stability opt-in.**Sus atributos pueden ser renombrados en la actualización de backend.

> **在 span 中捕获完整提示。**运维可以读取的追踪包含PII、密钥、客户数据──外部存储──
> **缺少 `gen_ai.provider.name`。**缺少归属时,多供应商仪表盘会出错.
> **没有父链接的 span。**孤立的工具 span──始终传播上下文──
> **不设置稳定性选择加入。**Su propiedad podría ser renombrada en el último nivel.

## Construye y realiza.
```figure
ae-genai-span-tree
```

## Construye el mismo

`code/main.py`Implementa un emisor de espacio de duración stdlib que coincida con las convenciones de GenAI:

> OpenTelemetry GenAI 语义约定 define los estándares de observabilidad de LLM y de Agente.`gen_ai.request.model`¿Qué es esto?`gen_ai.usage.input_tokens`¿Qué es esto?`gen_ai.agent.name`Y así.

- `Span`con el esquema de atributos GenAI.
- `Tracer`con`start_span`, contextos anidados.
- Un agente guionado que emite:`create_agent`¿ Qué ?`invoke_agent`(INTERNAL), extensiones por herramienta, `chat`Las llamadas de LLM.
- Un modo de captura de contenido que almacena las instrucciones externamente y registra las identidades en los intervalos.

- ¿Qué quieres decir ?

```
python3 code/main.py
```

Resultado: un árbol de extensión con todos los atributos GenAI requeridos y una "tienda externa" que muestra las referencias de contenido de opción.

> 输出: un contenedor de todos los elementos genAI 属性的 span 树, así como un mostrador de seleccionar los "extraños de almacenamiento" de los "content reference" (en inglés).

> OpenTelemetry GenAI 语义约定 define los estándares de observabilidad de LLM y de Agente.`gen_ai.request.model`¿Qué es esto?`gen_ai.usage.input_tokens`¿Qué es esto?`gen_ai.agent.name`Y así.

## Usalo con el marco de ejecución

- **Datadog LLM Observability**(v1.37+) los atributos de mapas nativos.
- **Langfuse / Phoenix / Opik**(Lección 24)  auto-instrumentos del ecosistema.
- **Jaeger / Honeycomb / Grafana Tempo** rastros OTel crudos; construir tablas de control a partir de los atributos GenAI.
- **Self-hosted** ejecutar el Colector OTel con un procesador GenAI.

## Envíe el producto .

`outputs/skill-otel-genai.md`los cables OTel GenAI se extienden a un agente existente con capturas de contenido por defecto y almacenamiento de referencias externos.

> `outputs/skill-otel-genai.md`Se puede utilizar para la captura de valores predefinidos y almacenamiento de referencia externa.

> OpenTelemetry GenAI 语义约定 define los estándares de observabilidad de LLM y de Agente.`gen_ai.request.model`¿Qué es esto?`gen_ai.usage.input_tokens`¿Qué es esto?`gen_ai.agent.name`Y así.

## Los ejercicios.

1. Instrumenta su Lección 01 Reacta el bucle con `invoke_agent`Envía a una instancia Jaeger.
  En inglés, "pensar y practicar" significa "pensar y practicar".
2. Añadir captura de contenido en modo "sólo referencias": las instrucciones a SQLite, los atributos span solo llevan ID de fila.
  En inglés, "pensar y practicar" significa "pensar y practicar".
3. Lea la especificación para `gen_ai.data_source.id`Envíala a tu búsqueda de Memorías de la Lección 09
  En inglés, "pensar y practicar" significa "pensar y practicar".
4. Se ha establecido`OTEL_SEMCONV_STABILITY_OPT_IN=gen_ai_latest_experimental`y verificar que sus atributos no sean renombrados por el coleccionista.
  En inglés, "pensar y practicar" significa "pensar y practicar".
5. Construir un tablero de control: "qué errores de herramienta se correlacionan con qué modelos" de los atributos de GenAI solamente.
  En inglés, "pensar y practicar" significa "pensar y practicar".

## Términos clave .

| Term | What people say | What it actually means |
|------|----------------|------------------------|---|
| GenAI SIG | "OpenTelemetry GenAI group" | OTel working group defining the schema |  |
| invoke_agent | "Agent span" | Name of the span representing an agent run |  |
| CLIENT span | "Remote call" | Span for a call to a remote agent service |  |
| INTERNAL span | "In-process" | Span for an in-process agent run |  |
| gen_ai.provider.name | "Provider" | anthropic / openai / aws.bedrock / google.vertex |  |
| gen_ai.data_source.id | "RAG source" | Which corpus/store a retrieval hit |  |
| Content capture | "Prompt logging" | Opt-in capture of messages; store externally in prod |  |
| Stability opt-in | "Preview mode" | Env var to pin experimental conventions |  |

## Más Leer más Leer más

- [OpenTelemetry GenAI semantic conventions](https://opentelemetry.io/docs/specs/semconv/gen-ai/) la especificación
  En el caso de los niños, el nombre de la persona que se encuentra en el lugar de residencia es el de la persona que se encuentra en el lugar de residencia.
- [OpenAI Agents SDK](https://openai.github.io/openai-agents-python/) GenAI se extiende por defecto
  En el caso de los niños, el nombre de la persona que se encuentra en el lugar de residencia es el de la persona que se encuentra en el lugar de residencia.
- [AutoGen v0.4 (Microsoft Research)](https://www.microsoft.com/en-us/research/articles/autogen-v0-4-reimagining-the-foundation-of-agentic-ai-for-scale-extensibility-and-robustness/) Espacios de OTel incorporados
  En el caso de los niños, el nombre de la persona que se encuentra en el lugar de residencia es el de la persona que se encuentra en el lugar de residencia.
- [Claude Agent SDK](https://platform.claude.com/docs/en/agent-sdk/overview) Profundización del contexto de las huellas de W3C
  En el caso de los niños, el nombre de la persona que se encuentra en el lugar de residencia es el de la persona que se encuentra en el lugar de residencia.
