# LLM Observabilidad Stack Selección                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                     

> El mercado de observabilidad de 2026 se divide en dos categorías. Las plataformas de desarrollo (LangSmith, Langfuse, Comet Opik) incluyen monitoreo con evaluaciones, gestión de la sesión, repeticiones de sesiones. Las herramientas de acceso/instrumentación (Helicone, SigNoz, OpenLLMetry, Phoenix) se centran en la telemetría. Langfuse es un núcleo con licencia MIT con un fuerte balance OSS (50K eventos / mes en la nube gratuita). Phoenix es OpenTelemetry nativo bajo la Licencia Elastic 2.0  excelente para la visualización de deriva / RAG, no un backend de producción persistente. Arize AX utiliza la integración de Iceberg/Parquet de copia cero que afirma que es 100 veces más barato que la observabilidad monolítica. LangSmith lidera para LangChain/LangGraph, $ 39 / usuario / mes, auto-host en Enterprise sólo. Helicone es basado en proxy con configuración de 15-30 minutos, 100K req / mo libre, pero menos profundidad en las huellas del agente. Modelo de producción común: Gateway (Helicone/Portkey) + plataforma eval (Phoenix/TruLens) pegada por OpenTelemetry.

> **【中文解读】**Este capítulo presenta el MLL observable  control y regulación                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                


**Type:** Learn | **类型:** 学习
**Languages:** Python (stdlib, toy trace-sampling simulator) | **语言:** Python
**Prerequisites:** Phase 17 · 08 (Inference Metrics), Phase 14 (Agent Engineering) | **前置知识:** Phase 17 · 08 (Inference Metrics), Phase 14 (Agent Engineering)

> ¿ Qué es esto ?**【前置】**学本节前请先掌握:Fase 17·08(推理指标) 、Fase 14(Agencia 工程) ・LLM 可观测性两类工具:开发平台 + Gateway/遥测。
> ¿ Qué es esto ?**【类比】**                                                                                                                                                                                                                                                              
**Time:** ~60 minutes | **时间:** ~60 minutes

## Objetivos de aprendizaje

- Distinguir las plataformas de desarrollo (agrupadas: evals + prompts + sesiones) de las herramientas de gateway/telemetría (solo traces + métricas).
  En inglés, el nombre de la plataforma de desarrollo es "Bundunderdog".
- Mapa de seis herramientas principales (Langfuse, LangSmith, Phoenix, Arize AX, Helicone, Opik) a sus casos de licencia, precios y uso de puntos dulces.
  La versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión de la versión original de la versión de la versión de la versión de la versión original de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión
- Explica el patrón de cola de OpenTelemetry que le permite combinar una herramienta de pasarela con una plataforma de evaluación separada.
  China: OpenTelemetry 水模式, este modelo permite que usted pueda combinar herramientas de conexión a la red con un conjunto de plataformas de evaluación independiente.
- Nombre el diferenciador de costos para 2026 (enfoque de copia cero de Arize AX vs ingesta monolitica) y indique el multiplicador aproximado de 100x.
  China 翻译:说出 2026 年的成本差异化因素 (Arize AX 的零拷贝方法 vs 单体式摄入)并说明大约100倍的乘数──

## El problema es la introducción del problema

> **【中文解读】**LLM 可观测性工具分为两类:(1) 开发平台(LangSmith、Langfuse、Opik) 捆绑监控、评估、提示管理、会话回放;(2) 网关/遥测工具(Helicone、SigNoz、OpenLLMetry、Phoenix) 专注于遥测采集──选择涉及四个维度:技术(LangChain?原始SDK、?) 需求许可证(MIT only?商业可接受?)、预算、自托管──

> **【拓展：LLM 可观测性市场格局】**Los principales jugadores del mercado de LLM 可观测性市场:(1) Langfuse(MIT 开源,50K eventos/mes 免费云)LangSmith 级功能但可自托管;(2) LangSmith(商业,$39/usuario/mes)LangChain 生态最佳;(3) Phoenix(Elastic License 2.0) RAG/漂移可视化优秀;(4) Arize AX(商业) 零副本冰berg/Parquet,号称比单体可观便性宜宜100x;(5) Helicone(MIT,100K req/month 免费) 代理式,15-30 分钟设测模式是:网关水 ?? 关水/key) (((((Phoenix 评估平台/Tru Telemetra 通过连接

Usted envió una función de LLM. Funciona. No tiene visibilidad en fallos rápidos, bucles de herramientas, regresiones de latencia, picos de costos o tasa de éxito de caché rápido. Usted Google "observabilidad de LLM" y obtener ocho herramientas todas afirmando que resuelven el mismo problema a tres puntos de precio diferentes.

No resuelven el mismo problema. LangSmith responde "¿Por qué esta ejecución de LangGraph falló?" Phoenix responde "¿Mi tubería RAG está driftando?" Helicone responde "¿Qué aplicación está quemando tokens?" Langfuse responde "¿Puedo auto-host todo el asunto?" diferentes herramientas, diferentes audiencias.

La selección implica cuatro ejes: pila (LangChain? SDK crudo? multivendor?), tolerancia a las licencias (sólo MIT? Elastico OK? multa comercial?), presupuesto (nive libre? $100/mo? $1000/mo?), y auto-host (debe ser agradable de tener? nunca?).

## El concepto central.

### Dos categorías

**Development platforms**Se ejecuta experimentos, ver qué prompt funcionó, regresión de un conjunto de datos, nuevo prompt contra los viejos ganadores.

**Gateway/telemetry tools**Infraestructura de la información de la información de la información de la información de la información de la información.

### Saldo de la OSS de la Langfuse

> **【拓展：LLM 可观测性工具选型决策】**2026 años LLM 可观测性工具选型的关键维度:(1) 技术LangChain/LangGraph 生态优先选 LangSmith;自研 SDK 选 Langfuse或Phoenix;(2) 许可证要求 MIT 选 Langfuse/Opik;Elastic License 2.0 可接受选 Phoenix;商业可选 LangSmith;(3) 接受自托管必须自托管选 Langfuse或Opik(Docker 部署);(4) 预算免费层 Langfuse 50K eventos/mesen, හෙලිකონ 100K req/mesen,(5) 规模>10M traces/day 选 Arize AX-zero-copy 架构.

- Licenciado por Apache / MIT; auto-host a través de Docker.
- Número gratuito en la nube: 50 mil eventos al mes.
- Evals, gestión rápida, rastreos, conjuntos de datos, cobertura razonable de las cuatro características de la plataforma de desarrollo.
- Un punto positivo: desea características de la clase LangSmith pero debe ser auto-host o permanecer con licencia OSS.

### Phoenix (Arize)  Telemetría-primero, OpenTelemetría-nativo

- Licencia Elastica 2.0; auto-host trivial.
- Excelente en RAG y visualización de deriva.
- No diseñado como backend de producción persistente  observabilidad en el tiempo de desarrollo.
- Punto positivo: desarrollo de tuberías RAG, depuración de deriva, parejas con una puerta de entrada separada para la producción.

### Arize AX  el juego de la escala

- Integración de datos de la laguna de cero copias a través de Iceberg/Parquet.
- Las matemáticas: almacena rastros en su propio Parquet en S3; Arize lee directamente.
- En el caso de los Estados miembros, el número de datos de datos de los centros de investigación y de investigación es de 10 millones.

### LangSmith  LangChain/LangGraph primero

- Comercial, 39 dólares al mes, auto-host sólo en Enterprise.
- Lo mejor de su clase para las pilas de LangChain y LangGraph.
- Un equipo comprometido con LangChain, dispuesto a pagar.

### Helicone  base de proxy mínimo viable

- 15-30 minutos de configuración al cambiar su `OPENAI_API_BASE`a la proxy de Helicone.
- Licenciado por MIT; 100 mil recetas por mes gratis, pagados $20 por mes.
- Incluye fallover, almacenamiento en caché, límites de tasas  actúa como una puerta de entrada también.
- Menos profundidad en las huellas de agente / múltiples pasos.
- Sweet spot: inicio rápido, aplicación de pila única, necesita gateway + observabilidad en uno.

### Opik (Comet)  Plataforma de desarrollo OSS

- Apache 2.0, totalmente OSS.
- Un rasgo similar a Langfuse con herencia cometa.
- Los equipos de ML ya están en Comet, quieren la observabilidad de LLM en el mismo panel.

### SigNoz  OpenTelemetry-first APM completo

- Apache 2.0 maneja APM general más LLM a través de OpenTelemetry.
- Punto dulce: observabilidad unificada entre los servicios y las llamadas de LLM.

### El pegamento: OpenTelemetry + Convenciones semánticas de GenAI

> **【中文解读】**OpenTelemetry publicó a finales de 2025 el GenAI 语义约定(`gen_ai.system`¿Qué es esto?`gen_ai.request.model`¿Qué es esto?`gen_ai.usage.input_tokens`), hacer diferentes herramientas se pueden operar entre sí. El modelo de producción de 2026 es: 1) de cada LLM 调用发发带 GenAI 约定的 OTel; 2) 路由到网关; 3) 双写到评估平台; 4) 双写到评估平台; 4) 双写到评估平台; 4) 存档到数据湖; 4) 冰berg) 通过 Arize AX o DuckDB做长期分析;;

> **【拓展：LLM 可观测性的成本控制】**En >1M peticiones/días de escala, el total de costos de mantenimiento supera el costo de LLM 调用本身──采样策略:100% 错误、100% 高成本请求、5% 成功请求──始终保留聚合数据,只对长尾保留原始追踪──Langfuse 50K eventos/月 免费层适合小团队;大规模部署建议使用OpenTelemetry Collector +自有数据湖架构,成本可降低80%+──

OpenTelemetry publicó las convenciones semánticas de GenAI a finales de 2025 (`gen_ai.system`¿ Qué ?`gen_ai.request.model`¿ Qué ?`gen_ai.usage.input_tokens`Las herramientas que consumen OTel pueden interactuar.

1. Emite OTel con convenciones de GenAI de cada llamada de LLM.
2. Ruta a puerta de entrada (Helicone / Portkey) para el día a día.
3. Plataforma de evaluación de doble nave (Phoenix / Langfuse) para regresiones.
4. Archivo en el lago de datos (Iceberg) para análisis a largo plazo a través de Arize AX o DuckDB.

### La trampa: el instrumento en la capa equivocada

> **【中文解读】**埋点层级的选择:在 Agent 框架内埋点 (如添加 LangSmith traces) 会合到这个框架;在 HTTP/OpenAI-SDK 层埋点 (通过 OpenLLMetry或网关)则可移植──2026 最佳实践是协议层埋点无论底层使用什么框架,都通过OpenTelemetry + GenAI 语义约定统一采集──

La instrumentación dentro de su marco de agentes (por ejemplo, añadiendo rastros LangSmith) lo une a ese marco. La instrumentación en la capa HTTP/OpenAI-SDK (a través de OpenLLMetry o su puerta de enlace) es portátil.

### Muestras  no se puede guardar todo

En el caso de las solicitudes de más de 1 millón de personas/día, la retención de datos completos cuesta más que las solicitudes de LLM. Muestra por regla: 100% de errores, 100% de alto costo, 5% de éxito.

### Números que debes recordar

- Nube libre de Langfuse: 50K eventos/mes.
- LangSmith: 39 dólares al usuario por mes.
- Helicona libre: 100K reacutivos al mes.
- Arize AX reclama: ~ 100 veces más barato que el monolito a escala.
- Convenciones de OpenTelemetry GenAI: 2025 transporte marítimo, 2026 ampliamente adoptado.

## Usalo con el marco de ejecución
```figure
i4-otel-glue
```

## Usalo

`code/main.py`simula un día de 1M de seguimiento en todas las estrategias de retención (100% ingesta, muestreo, muestreo + errores).

> `code/main.py`simula un día de 1M de seguimiento en todas las estrategias de retención (100% ingesta, muestreo, muestreo + errores).

> `code/main.py`simula un día de 1M de seguimiento en todas las estrategias de retención (100% ingesta, muestreo, muestreo + errores).

## Envíe el producto .

Esta lección produce`outputs/skill-observability-stack.md`. Dado el tamaño, la escala, el presupuesto, la postura de la licencia, elige la herramienta (s).

> 本课产 出  `outputs/skill-observability-stack.md`. Dado el tamaño, la escala, el presupuesto, la postura de la licencia, elige la herramienta (s).

## Los ejercicios.

1. Su equipo en LangChain quiere la observabilidad de OSS, elija Langfuse o Opik y justifica.
   Su equipo utiliza LangChain, quiere abrirse a la administración de la información.
2. Con 5M traces/día con Datadog cotiza 150K$/mes, computa equilibración para Arize AX.
   En 5M rastros / día  bajo la escala, Datadog 报价$ 150K/月,计算 Arize AX 零拷贝方案的亏平衡点──
3. Diseñar un atributo de OpenTelemetry GenAI establecido por la guía de su organización debe exigir en cada llamada de LLM.
   China 调用包含的OpenTelemetry GenAI 属性集──
4. ¿Debemos discutir si Phoenix es suficiente para la producción?
   El Phoenix 单独使用是否足以满足生产需求──¿En qué circunstancias no es suficiente?
5. Helicone es 20 ms de carga por proxy. ¿A P99 TTFT 300 ms, es aceptable? ¿Qué pasa si SLA es 100 ms?

## Términos clave .

| Term | What people say | What it actually means |
|------|----------------|------------------------|
| OpenLLMetry | "OTel for LLMs" | Open-source OpenTelemetry instrumentation for LLMs |
| GenAI conventions | "OTel attributes" | Standard OTel attribute names for LLM calls |
| LangSmith | "LangChain observability" | Commercial platform bundled with LangChain ecosystem |
| Langfuse | "OSS LangSmith" | MIT OSS with similar feature set |
| Phoenix | "Arize dev tool" | OpenTelemetry-native dev/eval platform |
| Arize AX | "scale observability" | Commercial zero-copy Iceberg/Parquet observability |
| Helicone | "proxy observability" | HTTP proxy collecting LLM telemetry + gateway features |
| Opik | "Comet LLM" | Apache 2.0 OSS dev platform from Comet |
| Session replay | "trace rerun" | Replay a full agent session with tool calls |
| Eval | "offline test" | Running candidate model/prompt over labeled dataset |

## Más Leer más Leer más

- [SigNoz — Top LLM Observability Tools 2026](https://signoz.io/comparisons/llm-observability-tools/)
- [Langfuse — Arize AX Alternative analysis](https://langfuse.com/faq/all/best-phoenix-arize-alternatives)
- [PremAI — Setting Up Langfuse, LangSmith, Helicone, Phoenix](https://blog.premai.io/llm-observability-setting-up-langfuse-langsmith-helicone-phoenix/)
- [OpenTelemetry GenAI Semantic Conventions](https://opentelemetry.io/docs/specs/semconv/gen-ai/)
- [Arize Phoenix docs](https://docs.arize.com/phoenix)
- [Helicone docs](https://docs.helicone.ai/)
