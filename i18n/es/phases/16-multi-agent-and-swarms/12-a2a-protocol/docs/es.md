# El protocolo de agente a agente.

> Google anunció A2A en abril de 2025; para abril de 2026 la especificación está en https://a2a-protocol.org/latest/specification/y más de 150 organizaciones lo respaldan. A2A es el complemento horizontal del MCP (lección 13): donde el MCP es vertical (agente  herramientas), A2A es peer-to-peer (agente  agente). Define las tarjetas de agentes (descubrimiento), tareas con artefactos (texto, datos estructurados, video), ciclos de vida opacos de tareas y auth. Los sistemas de producción emparejan cada vez más el MCP con el A2A. Google Cloud lanzó soporte A2A en Vertex AI Agent Builder durante 2025-2026.

> **【中文解读】**Google lanzó el protocolo A2A en abril de 2025; hasta abril de 2026, la normativa ya tiene más de 150  organizaciones apoyadas. A2A es el complemento horizontal de MCP: MCP es vertical.

> **【拓展：A2A → Google 的 Agent 协议】**A2A es el protocolo de Agente 间通信标准协议, dirigido por Google, con el MCP de Anthropic (Modelio de Protocolo de Contexto) de intercambio.

**Type:** Learn + Build | **类型:** 学习 + 构建
**Languages:** Python (stdlib, `http.server`, `json`) | **语言:** Python (标准库, `http.server`, `json`)
**Prerequisites:** Phase 16 · 04 (Primitive Model) | **前置知识:** Phase 16 · 04 (原语模型)
**Time:** ~75 minutes | **时间:** ~75 分钟

> ¿ Qué es esto ?**【前置】**学本节前请先掌握:Fase 13·15-20(MCP 协议套件) 、Fase 16·04(原语) ・・・A2A es el nivel de MCP:MCP=Agent 调工具(垂直),A2A=Agent 找 Agent(横向) ・・・
> ¿ Qué es esto ?**【类比】**MCP + A2A = "电话黄页 + 直接通话"──MCP = 工具目录(agent 找工具用);A2A = Agent 间通话协议(agent 找 agent 协作)──2026 生产系统标配:MCP(连工具) + A2A(连其他 Agent) + Agent Card(发现)──Google 主导,150+ 组织支持──

## # El problema # # El problema #

El agente debe llamar a otro agente en otro sistema. ¿Cómo? Puedes exponer un punto final HTTP, definir un esquema JSON a medida, y esperar que el otro lado lo hable. Cada par de agentes se convierte en una integración personalizada.

> ¿Cómo hacer? ¿Puedes exponer un punto final HTTP, definir un modelo JSON personalizado, y esperar que el otro lado pueda entenderlo.

El problema de integración N-cuadrado: con N agentes, necesitas N × 1) / 2 integraciones personalizadas. con 10 agentes, eso es 45 integraciones. con 100 agentes, 4950. A2A desmorona esto a N Agente Cards, cada describiendo un agente.

> N 平方集成问题:N 个代理 需要 N×(N-1)/2 个定制集成──10 个代理 是 45 个集成──100 个代理 是 4950 个──A2A se acumulará en N 个代理卡片, cada una describirá a un agente──

A2A es el protocolo universal para esa llamada. Descubrimiento estándar, modelo de tarea estándar, transporte estándar, artefactos estándar.

> A2A es el protocolo de línea general que debe ser utilizado.

La abstracción clave: los agentes son endpoints de red direccionables y descubrables. No "importas" un agente; lo "llamas". Esto desacopla la implementación  el agente se ejecuta dondequiera, en cualquier idioma, utilizando cualquier marco, siempre y cuando habla A2A.

> 关键抽象:Agent es可寻址、可发现的网络端点──你不"导入"Agent;你"调用"它──这解已部署Agent 运行在任何地方、使用任何语言、使用任何框架,只要它说 A2A──

## Concepto de la esencia de la concepción

### Los cuatro elementos

> Cuatro elementos

**Agent Card.**Un documento JSON en `/.well-known/agent.json`Describir al agente: nombre, habilidades, puntos finales, modalidades compatibles, requisitos de autor.

> **Agent 卡片。** en el`/.well-known/agent.json`El documento JSON 文档,描述 Agent:名称、技能、端点、支持的模态、认证要求──通过读取卡片进行发现──

La conocida convención de URL refleja los estándares web (`/.well-known/`es el mismo camino utilizado para `robots.txt`Cualquier agente compatible con A2A puede ser descubierto obteniendo esa URL.

> Conocimiento URL 约定镜像 Web 标准(`/.well-known/`Es utilizado`robots.txt`、ACME 挑战、OIDC 发现的相同路径) ∼ Cualquier agente A2A 兼容 △ puede acceder a la URL 发现── no necesita registro、agente o catálogo central──

**Task.**Una unidad de trabajo, un objeto sincronizado, con un ciclo de vida:`submitted -> working -> completed / failed / canceled`Un cliente envía una tarea, encuestas o suscribe actualizaciones.

> **任务。**工作单元── objetos de estado diferente del ciclo de vida:`submitted -> working -> completed / failed / canceled` Envío de tareas, consultas o actualizaciones de sus clientes.

**Artifact.**El tipo de resultado producido por una tarea. texto, JSON estructurado, imagen, video, audio.

> **工件。**任务产生的结果类型──文本、结构化 JSON、图像、视频、音频──工件是有类型的,因此不同模态是平等公民──

**Opaque lifecycle.**A2A no prescribe *cómo* el agente remoto resuelve la tarea.El cliente ve las transiciones de estado y los artefactos; la implementación es libre de usar cualquier marco.

> **不透明生命周期。**A2A 不规定远程代理 *如何* 解决任务──客户端看状态转换和工件;实现可以自由使用任何框架──

Esta opacidad es por diseño. Un agente remoto construido en LangGraph, CrewAI o un script Python personalizado se ve idéntico al cliente A2A. La interoperabilidad proviene de acordar el formato de cable, no los internos.

> Esta forma de transparencia es el diseño así. A partir de LangGraph, CrewAI o Python, un agente remoto construido por un guión de Python se ve en el cliente A2A. La interoperabilidad proviene de un formato de línea acordado, no de la interior.

### La división MCP/A2A

- **MCP**(Lección 13): herramienta de agente <->. El agente lee/escribe a través de JSON-RPC a un servidor de herramientas.
  En inglés:**MCP**(Lección 13):Agencia <-> 工具──Agencia 通过 JSON-RPC 读写工具服务器──默认无状态──
- **A2A**El protocolo de pares; ambas partes son agentes con su propio razonamiento.
  En inglés:**A2A**Agente: Agente: contratación de los demás; ambas partes tienen sus propios agentes.

Los sistemas de producción multi-agentes utilizan ambos. Un A2A peer llama a herramientas MCP de su lado. La división mantiene las dos preocupaciones limpias.

> Producción de múltiples agentes  sistemas  ambos utilizan A2A para los demás en su extremo de la MCP  herramienta                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                 

Un patrón común: un "agente de investigación" A2A en la empresa A llama a un servidor de herramienta de búsqueda MCP internamente, luego devuelve sus hallazgos a un "agente de análisis" A2A en la empresa B. La comunicación transorg es A2A; el uso de herramientas internas es MCP. Cada protocolo hace lo que mejor es.

> 常见模式: A2A "Agencia de investigación" de la compañía A utiliza internamente el MCP 搜索工具服务器, y luego se encuentra de vuelta a A2A "Agencia de analistas" de la compañía B.

O con transmisión: suscripción de SSE a `/tasks/{id}/events`para actualizaciones de empuje.

> O usar el código: SSE 订阅 `/tasks/{id}/events`获取推送更新── y ahora mismo.

### Autor

A2A admite tres patrones comunes:

> A2A 支持三种常见模式:

Los tres patrones cubren el espectro de "Confío en mi proveedor de identidad" (portador de OAuth2) a "nos verificamos mutuamente" (mTLS) a "no confiamos en ningún tercero" (firmación HMAC).

> Tres modalidades abarcan desde "我信任我的身份提供商" (OAuth2 portador) hasta "我们互相验证彼此" (MTLS) hasta "我们不信任任何第三方" (HMAC  firma) del alcance.

- **Bearer token** OAuth2 o opaco.
  En inglés:**Bearer token** OAuth2 或不透明令牌。
- **mTLS** TLS mutuo; las organizaciones se prueban la identidad.
  En inglés:**mTLS** 双向 TLS; organización mutuamente demostrando su identidad.
- **Signed requests** HMAC sobre la carga útil.
  En inglés:**签名请求** para el HMAC de carga efectiva

El autor se declara en la tarjeta de agente; los clientes descubren y cumplen.

> 认证在代理卡片中声明;客户端发现并遵守──

### 150+ organizaciones para abril de 2026

La adopción de la empresa impulsó la escala A2A. El título: A2A se convirtió en la forma en que los sistemas de agentes empresariales cruzaron las fronteras de confianza. Google Cloud envió soporte A2A para Vertex AI Agent Builder; Microsoft Agent Framework lo soporta; la mayoría de los principales marcos (LangGraph, CrewAI, AutoGen) envían adaptadores A2A.

> 企业采用推动了A2A的规模化――标题:A2A 成为企业代理 系统跨越信任边界的方式――Google Cloud 提供 Vertex AI Agent Builder A2A 支持;Microsoft Agent Framework 支持它;大多数主要框架(LangGraph、CrewAI、AutoGen)提供 A2A 适配器──

La razón por la que A2A ganó la adopción empresarial donde FIPA-ACL falló: A2A es nativo de JSON, utiliza la infraestructura web existente (HTTP, SSE, OAuth), y no requiere ontologías compartidas.

> A2A es la causa del fracaso de FIPA-ACL en la adopción empresarial: A2A es la fuente de JSON, utiliza la infraestructura web existente, HTTP, SSE, OAuth, no necesita compartir el contenido.

### Donde gana A2A

- **Cross-organization calls.**Agente de la compañía A llama a agente de la compañía B. Sin A2A, cada par es un contrato a medida.
  En inglés:**跨组织调用。**Company A's Agent 调用Company B's Agent ⋅ no hay A2A, cada uno es un contrato de fabricación ⋅
- **Heterogeneous frameworks.**El agente LangGraph llama al agente CrewAI llama al agente Python personalizado.
  En inglés:**异构框架。**LangGraph Agent 调用 CrewAI Agent 调用自定义 Python Agent──A2A 标准化──
- **Typed artifacts.**Resultado de vídeo, JSON estructurado, audio  todos de primera clase.
  En inglés:**类型化工件。**视频结果、结构化 JSON、音频都是一等公民──
- **Long-running tasks.**El ciclo de vida opaco + las encuestas hacen que las tareas de horas sean sencillas.
  En inglés:**长时间运行的任务。**La vida de los niños y niñas en el mundo de la investigación y la investigación se vuelve más fácil.

### Donde A2A lucha

- **Latency-sensitive micro-calls.**El ciclo de vida de A2A es asincronizado.
  En inglés:**延迟敏感的微调用。**El ciclo de vida de A2A es diferente.
- **Tight-coupled in-process agents.**Si ambos agentes se ejecutan en el mismo proceso Python, A2A HTTP ida y vuelta es exagerado.
  En inglés:**紧耦合的进程内 Agent。**Si dos agentes se ejecutan en el mismo proceso Python, A2A HTTP regresa es un exceso de diseño.
- **Small teams.**Las tarifas generales de las especificaciones son reales; los agentes internos pueden no necesitar la formalidad.
  En inglés:**小团队。**La normativa de venta es real; sólo el agente interno puede no necesitar esta formalidad.

### A2A vs ACP, ANP, NLIP

Varias especificaciones relacionadas surgieron en 2024-2026:

> Entre 2024 y 2026, surgieron varias normas relacionadas:

- **ACP**(IBM/Linux Foundation)  predecesor de A2A, alcance más estrecho.
  En inglés:**ACP**(IBM/Linux Foundation)  A2A's anterior, alcance más estrecho.
- **ANP**(Protocolo de red de agentes)  Peer-discovery-heavy, descentralizado-first.
  En inglés:**ANP**(Protocolo de red de agentes)  重对等发现,去中心化优先
- **NLIP**(Protocolo de Interacción de Lenguaje Natural de ECMA, estandarizado diciembre 2025)  Tipo de contenido en lenguaje natural.
  En inglés:**NLIP**(Ecma Naturaleza Language交互协议,2025 年 12 月标准化)  Naturaleza lenguaje contenido tipo。

A2A es el protocolo de pares más adoptado a partir de abril de 2026. Ver arXiv:2505.02279 (Liu et al., "Una encuesta de protocolos de interoperabilidad de agentes") para la comparación.

> 截至 2026 年 4 月,A2A es el más amplio de los contratos de comparación.

El panorama del protocolo 2026 se ha estabilizado: A2A para la colaboración con agentes, MCP para herramientas, ACP absorbido en A2A para la registro de trayectorias, ANP para la identidad transorg. NLIP sigue siendo un nicho.

> El marco del acuerdo de 2026 ya está estable: A2A para el agente 协作, MCP para los instrumentos, ACP para la absorción de A2A para el轨迹日志, ANP para la transorganización de la organización.

## Construye y realiza.
```figure
sw-agent-card-discovery
```

## Construye el mismo

`code/main.py`Implementa un servidor y cliente A2A mínimo utilizando `http.server`El servidor:

> `code/main.py`Uso `http.server`Y JSON  implementar A2A 最小服务器和客户端──服务器:

- expone `/.well-known/agent.json`¿ Qué ?
  En español: exposit`/.well-known/agent.json`¿ Qué ?
- acepta`POST /tasks`¿ Qué ?
  En inglés: acepta`POST /tasks`¿ Qué ?
- gestiona el estado de tarea,
  En inglés, el nombre de la empresa es "Special Operations Manager".
- devuelve los artefactos en `GET /tasks/{id}`¿ Qué ?
  En español: en`GET /tasks/{id}`Sobre el trabajo de vuelta.

El cliente:

> 客户端:

- Trae la tarjeta de agente,
  En el caso de los agentes, el agente de la policía es el agente de la policía.
- presentar una tarea,
  Traducción:comprometir tareas,
- encuestas hasta su finalización,
  La pregunta hasta que se acabe,
- Leía el artefacto.
  En inglés, el nombre de la obra es "Creación".

El script inicia el servidor en un hilo de fondo, luego ejecuta el cliente contra él.

> 脚本在后台线程中启动服务器,然后运行客户端──你看完整流程:发现,提交,轮询,工件──

## Usalo con el marco de ejecución

`outputs/skill-a2a-integrator.md`Diseña una integración A2A: contenido de la tarjeta de agente, esquemas de tareas, elección de autor, transmisión versus encuestas.

> `outputs/skill-a2a-integrator.md`设计 A2A 集成:Agente 卡片内容、任务模式、认证选择、流式 vs 轮询──

## Envíe el producto .

Lista de control:

> 检查清单:

- **Pin the spec version.**A2A todavía está evolucionando; la tarjeta de agente debe declarar la versión del protocolo.
  En inglés:**固定规范版本。**A2A  sigue en desarrollo;
- **Idempotent task creation.**Las presentaciones duplicadas (retemplazos en red) deben producir una tarea.
  En inglés:**幂等任务创建。**Se debe producir una tarea.
- **Artifact schemas.**Declarar qué formas devuelve el agente; los consumidores deben validar.
  En inglés:**工件模式。**声明 Agente 返回什么形状; consumidor应验证。
- **Rate limits + auth.**A2A es público; aplica seguridad web estándar.
  En inglés:**速率限制 + 认证。**A2A 面向公众; aplicación estándar de seguridad web
- **Dead-letter for failed tasks.**Inspeccionar los patrones a lo largo del tiempo para detectar tipos de fallas recurrentes.
  En inglés:**失败任务死信。**随着时间检查模式 为了发现反复出现的失败类型──

## Los ejercicios.

1. - ¿ Qué ?`code/main.py`Confirme que el cliente descubre el servidor y recibe el artefacto correcto.
   Traducción:运行`code/main.py` Confirmar que el cliente encuentra que el servidor no ha recibido las obras correctas.
2. Añadir una segunda habilidad al servidor (por ejemplo, "resumir"). Actualizar la Tarjeta de agente. Escribir un cliente que seleccione la habilidad en función del tipo de tarea.
   China: 翻译:向服务器添加第二个技能 (en inglés: 函数) 编写根据任务类型选择技能的客户端 (en inglés: 函数) 编写
3. Implementar un punto final de transmisión de SSE: `/tasks/{id}/events`¿Qué necesita el cliente para hacer de manera diferente?
   Se trata de un proyecto de la Comisión Europea.`/tasks/{id}/events`¿Qué cosas diferentes necesita hacer el cliente?
4. Lea la especificación A2A. Identifique tres cosas que la especificación manda que esta demostración no implementa.
   China: A2A 规范──识别规范要求的三个演示未实现的东西──
5. Compare A2A (descubrimiento de tarjetas de agente) con MCP (lista de capacidades del lado del servidor a través de `listTools`¿Cuál es la diferencia entre los agentes que se describen a sí mismos y los que prueban sus capacidades?
   En español: Comparar A2A (Agencia 卡片发现) con MCP (MCP)`listTools`¿Cuál es el equilibrio entre el agente y la capacidad de investigación?

## Términos clave .

| Term | What people say | What it actually means |
|------|----------------|------------------------|
| A2A | "Agent-to-agent" / "Agent 对 Agent" | Peer protocol for agents to call other agents across systems. Google 2025. / Agent 跨系统调用其他 Agent 的对等协议。Google 2025。 |
| Agent Card / Agent 卡片 | "The agent's business card" / "Agent 的名片" | JSON at `/.well-known/agent.json` describing skills, endpoints, auth. / 描述技能、端点、认证的 JSON。 |
| Task / 任务 | "The unit of work" / "工作单元" | Async stateful object with a lifecycle; artifacts produced on completion. / 具有生命周期的异步有状态对象；完成时产生工件。 |
| Artifact / 工件 | "The result" / "结果" | Typed output: text, structured JSON, image, video, audio. First-class media. / 类型化输出：文本、结构化 JSON、图像、视频、音频。一等媒体。 |
| Opaque lifecycle / 不透明生命周期 | "How it's solved is the agent's business" / "如何解决是 Agent 的事" | Client sees state transitions; server is free to choose framework/tools. / 客户端看到状态转换；服务器自由选择框架/工具。 |
| Discovery / 发现 | "Finding the agent" / "找到 Agent" | `GET /.well-known/agent.json` returns the card. / 返回卡片的 GET 请求。 |
| MCP vs A2A | "Tools vs peers" / "工具 vs 对等" | MCP: vertical agent <-> tool. A2A: horizontal agent <-> agent. / MCP：垂直 Agent <-> 工具。A2A：水平 Agent <-> Agent。 |
| ACP / ANP / NLIP | "Sibling protocols" / "兄弟协议" | Adjacent specs; A2A is the most-adopted 2026. / 相邻规范；A2A 是 2026 年采用最广泛的。 |

## Más Leer más Leer más

- [A2A specification](https://a2a-protocol.org/latest/specification/) la especificación canónica
  中文翻译:A2A 规范  权威规范
- [Google Developers Blog — A2A announcement](https://developers.googleblog.com/en/a2a-a-new-era-of-agent-interoperability/) Abril 2025 puesta en marcha
  中文翻译:Google 开发者博客  A2A 公告  2025 年 4 月发布文章
- [A2A GitHub repo](https://github.com/a2aproject/A2A) Implementaciones de referencia y KDD
  中文翻译:A2A GitHub 仓库  参考实现和 SDK
- [Liu et al. — A Survey of Agent Interoperability Protocols](https://arxiv.org/html/2505.02279v1) Comparación entre MCP, ACP, A2A y ANP
  En inglés, el nombre de la compañía es "MCP", y en inglés, el nombre de la compañía es "MCP".
