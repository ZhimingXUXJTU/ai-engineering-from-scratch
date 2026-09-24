# Caching rápido y Caching semántico economía

> **Pricing snapshot dated 2026-04.**Las afirmaciones numéricas a continuación reflejan las tarjetas de tarifas de los proveedores capturadas en la publicación de esta lección; verifique con los documentos vinculados antes de cotizarlos en aguas subyacentes.

> **【中文解读】**Este capítulo presenta la respuesta de la sugerencia a través de la similaridad de la respuesta a la sugerencia para reducir el costo de la hipótesis.


> El caché de instrucciones de L2 (nivel de proveedor) reutiliza la atención KV para los prefijos repetidos  Los documentos de caché de instrucciones de Anthropic anuncian hasta una reducción de costes del 90% y una reducción de latencia del 85% en instrucciones largas; para Claude 3.5 Sonnet se leen en caché $0.30/M vs $3,00/M fresco con un TTL de 5 minutos y una prima de escritura de 2 veces para la opción de TTL de 1 hora (docs.anthropic.com, 2026-04). La caché de instancias OpenAI se aplica automáticamente para las instancias ≥1024 tokens y precios entradas cachées a aproximadamente un descuento del 90% frente a frescos (platform.openai.com, 2026-04); la tasa exacta caché por modelo depende de la tarjeta de tasa en vivo. El L1 (nivel de aplicación) de almacenamiento en caché semántico omite el LLM en su totalidad en la incorporación de hits de similitud. Vendedor "95% de exactitud" se refiere a la corrección de coincidencia, no la tasa de impacto  las tasas de impacto de producción reportadas van desde el 10% (chat abierto) hasta el 70% (FAQ estructurado); ninguno de los proveedores publica una línea de base oficial, por lo que trata esto como telemetría comunitaria en lugar de garantías. Los obstáculos de producción: la paralelalización mata el caché (las solicitudes paralelas emitidas antes de que la primera caché escriba pueden inflar el gasto varias veces), y el contenido dinámico dentro del prefijo evita que el caché golpee por completo. ProjectDiscovery informó que se movió de 7% a 74% de la tasa de hits (2025-11) moviendo el texto dinámico fuera del prefijo cachéable.

**Type:** Learn | **类型:** 学习
**Languages:** Python (stdlib, toy two-layer cache simulator) | **语言:** Python
**Prerequisites:** Phase 17 · 04 (vLLM Serving Internals), Phase 17 · 06 (SGLang RadixAttention) | **前置知识:** Phase 17 · 04 (vLLM Serving Internals), Phase 17 · 06 (SGLang RadixAttention)
**Time:** ~60 minutes | **时间:** ~60 minutes
**Type:** Learn
**Languages:** Python (stdlib, toy two-layer cache simulator)
**Prerequisites:** Phase 17 · 04 (Serving Engine Internals), Phase 17 · 06 (SGLang RadixAttention)
**Time:** ~60 minutes

> ¿ Qué es esto ?**【前置】**学本节前请先掌握:Fase 17·04(vLLM)、Fase 17·06(RadixAttention)、Fase 11·04(Embedidos 用于语义缓存)。两层缓存:L2 提供商级 + L1 应用级。
> ¿ Qué es esto ?**【类比】**缓存 = "翻历史聊天记录"──L2 提示缓存(Antropic/OpenAI) = 服务商帮你存存(90% 成本降,85%延迟降);L1 语义缓存 = 自己用嵌入 找相似问题直接返回──陷:并行请求会破坏缓存、前里塞动态内容(时间) = 永远命中不了──ProjectDiscovery 把动态文本挪出可存前后,命中 7%率→74%──
> ️ **【易错点】**厂商宣传 "95% 准确率" se refiere a la tasa de coincidencia correcta y no de éxito.

## Objetivos de aprendizaje

- Distinguir entre el caché de prompto/prefijo L2 (reutilización de KV en el proveedor) y el caché semántico L1 (eliminación de LLM en prompts similares).
  La lengua inglesa se traduce en inglés como "L2 提示/前缓存") y "L1 语义缓存")
- Explica el trabajo de Anthropic `cache_control`marcado explícito y las dos opciones TTL (5 minutos vs. 1 hora) con sus multiplicadores de precios.
  Traducción:Antropic de la interpretación`cache_control`显式标记和两种 TTL 选项(5 分钟 vs 1 小时) y su precio multiplicado
- Calcule los ahorros mensuales esperados dados el índice de éxito, la mezcla de respuesta/prompto y los precios de los tokens.
  Traducción:                                                                                                                                                                                                                                                              
- Nombre el patrón anti-paralelalización que infla las facturas en 5-10 veces y el patrón anti-contenido dinámico que colapsar tasa de impacto.
  China Translation: decir que la inflación de la cuenta se ha multiplicado de 5 a 10 veces por la convergencia de los tipos de cambio y que ha provocado el colapso de los tipos de cambio.

## El problema es la introducción del problema

> **【中文解读】**提示缓存有两个常见失败模式:(1) 并行化反模式Agent 发发出10 并行工具调用, todas las solicitudes se escriben en la primera caché 完成前到达,10 次写入、0 次读取, cuenta se expansión 5-10x;(2) 动态内容反模式系统提示中包含当前时间、请求 ID等动态内容,每个请求都唯一,缓存中率 0%──修复方法:将静态内容放缓存前,动态内容放缓边界后──

> **【拓展：提示缓存的经济价值】**提示缓存是LLM 成本优化中最直接的杆──Antropic 的缓存 仅读 仅读$0.30/M（Claude 3.5 Sonnet），比 fresh input $3.00/M 便宜 10x──OpenAI para caché automático de sugerencias de ≥1024 tokens, caché de entrada de caché de aproximadamente el 10% del precio de las nuevas entradas──En la producción RAG 系统, la tasa de caché de sugerencias de sistema compartido puede alcanzar el 60-80%, por mes puede ahorrar varios millones de dólares──语义缓存(L1) en estructuradas FAQ 场景可达 40-70% la tasa de vida──

Si usted añade la caché de instrucciones a su servicio RAG. La factura se mantiene plana. mide la tasa de hits; es 7%. Sus instrucciones se ven estáticas pero no lo son.

> **【中文解读】**
> 提示缓存分两层:L2(fourmer级) 重用重复前的 KV cacheAnthropic 声称缓存读取成本降低90%、延迟降低85%;L1(应用级)语义缓存存在嵌入相似度命中时直接跳过LLM。 pero dos反模式会破坏缓存效果:(1) prompt 中的动态内容(时间、请求 ID)阻止缓存命中;(2) 并行请求在第一个缓存写入前全部到达,导致N 次取写入次次读零──

Separadamente, su agente ejecuta diez llamadas paralelas de herramientas por pregunta de usuario. Todas las diez llegan al proveedor antes de que finalice la primera escritura en caché. Diez escribe, cero lee. Su factura es 5-10 veces lo que "con caché" se suponía que costaría.

El caché es un protocolo, no una bandera.

## El concepto central.

### L2  almacenamiento en caché de los servicios de proveedores

> **【中文解读】**L2 层(提供商级)提示缓存复用重复前的注意力 KV──Antropic 使用显式 `cache_control`标记,TTL 选项有5分钟(写入成本 1.25x)和1 小时(2x),读取成本仅为新鲜输入的1/10──OpenAI对 ≥1024 token提示自动缓存,无需标记──Google Gemini 通过显式 API 提供语境缓存──自部署方案使用vLLM预写缓存或SGLang RadixAttention──

El proveedor almacena el KV de atención para un prefijo cachéable y lo reutiliza en la siguiente solicitud que coincide con el prefijo.

**Anthropic (Claude 3.5 / 3.7 / 4 series)**: explícito `cache_control`TTL: 5 minutos (costos de escritura 1.25x base) o 1 hora (costos de escritura 2x base).$0.30/M on Claude 3.5 Sonnet vs $3,00/M fresco  10 veces más barato (docs.anthropic.com, a partir de 2026-04). Las tarifas difieren por modelo (Opus/Haiku publicado por separado); siempre compruebe la página de precios en vivo.

**OpenAI**El sistema de almacenamiento en caché automático para las instrucciones ≥1024 tokens (platform.openai.com, 2026-04). No hay bandera explícita. La entrada en caché es aproximadamente 10 veces más barata que la nueva en las tarjetas de tasa gpt-4o/gpt-5. Ni los documentos ni las notas de liberación publican una línea de base oficial de la tasa de éxito; los informes comunitarios se agrupan alrededor de 3060% con un diseño de solicitud cuidadoso.`usage.cached_tokens`para medir la suya.

**Google (Gemini)**: caching de contexto a través de API explícita; 1M-token context significa que el caching paga aún más.

**Self-hosted (vLLM, SGLang)**: Fase 17 · 06 cubre el mismo patrón en su propio cálculo.

### L1  Caching semántico a nivel de aplicación

> **【中文解读】**L1 层(应用级)语义缓存在调用 LLM 之前,对提示做哈希和嵌入查找. Si se encuentra una similitud superior a值 (normalmente 0.95+) de la solicitud de缓存, directamente regresar a la solicitud de缓存响应.

Antes de llamar al LLM, hash el prompt, embebegue y busque una solicitud similar almacenada en caché (similaridad de cosinos por encima del umbral, típicamente 0.95+).

Fuente abierta: Redis Vector Similarity, GPTCache, Qdrant. Comercial: Portkey Cache, Helicone Cache.

Las afirmaciones de precisión del proveedor se refieren a la frecuencia con la que la respuesta devuelta en caché fue semánticamente apropiada  no a la frecuencia con la que se golpeó.

- Convite de tiempo libre: 10-15%.
- Preguntas frecuentes / apoyo estructurados: 40-70%.
- Las preguntas de código: 20-30% (variantes pequeñas matan los hits).
- Agentes de voz que repiten las instrucciones: 50-80% (conjunto fijo de normalización de voz).

### El patrón antiparallelización

> **【拓展：并行化反模式的真实案例】**Y linealización contra el modo en la producción:Agent hacia Antropic  Emite 10 herramientas de la misma manera de convocar, compartir con un 4K-token  system tip. Antropic cache escribir en aproximadamente 300ms   finalizado, pero la solicitud 2-10 en la misma milisegundos ventana llega, cada uno ve caché perdido. Resultado::10 veces escribir en溢价、0 veces leer en descuento.

Su agente hace 10 llamadas de herramientas en paralelo. Todas las 10 tienen el mismo mensaje de sistema de 4K-token. Las escrituras de caché antropópica son por solicitud; la primera escritura de caché se completa alrededor de 300 ms después de que el proveedor vea el mensaje. Las solicitudes de 2-10 llegan en la misma ventana de milisegundos y cada uno ve caché perdido. Pagas 10 primas de escritura, 0 descuentos de lectura.

Corrección: lote con secuencia-primero  hacer la solicitud 1 solo, luego disparar 2-10 una vez que la caché de 1 se ha llenado. Agrega 300 ms a la primera llamada de herramienta; ahorra 5-10 veces la factura.

### El antipatrón de contenido dinámico

Su mensaje del sistema se parece a:

```
You are a helpful assistant. The current time is 14:32:17.
User ID: abc123. Today is Tuesday...
```

Cada solicitud es única, cada solicitud escribe, cero hits.

Corrección: mover todo lo realmente estático al prefijo cachéable; agregar contenido dinámico después del límite de caché:

```
[cacheable]
You are a helpful assistant. [rules, examples, instructions]
[/cacheable]
[dynamic, not cached]
Current time: 14:32:17. User: abc123.
```

ProjectDiscovery pasó de 7% a 74% de la tasa de caché de esta manera y publicó la anatomía.

### Batch de pila + caché para cargas de trabajo nocturnas

Las API de lote (fase 17 · 15) ofrecen un descuento del 50% a las 24 horas de cambio. La entrada almacenada en caché en la parte superior te da ~ 10 veces más. Las cargas de trabajo de clasificación, etiquetado y generación de informes de la noche a la mañana pueden caer a ~ 10% del costo sincrónico sin caje mediante la pila.

### Números que debes recordar

Los puntos de precios se capturan 2026-04 de los documentos de los vendedores vinculados y se desvían cada pocos meses  volver a comprobar antes de depender de ellos.

- Anthropic se lee en caché: $0.30/M en Claude 3.5 Sonnet, aproximadamente 10 veces más barato que la entrada reciente (docs.anthropic.com).
- Premia de escritura de caché antropico: 1.25x (5 min TTL) o 2x (1 hora TTL).
- OpenAI auto-cache: se aplica a las instrucciones ≥1024 tokens; entradas almacenadas en caché a un precio de aproximadamente el 10% de las entradas nuevas en las tarjetas de tasa corriente (platform.openai.com).
- Taxa de hits de caché semántico (reportado por la comunidad): ~10% de chat abierto; hasta ~70% de preguntas frecuentes estructuradas. No es una línea de base documentada por el proveedor.
- ProjectDiscovery: 7% → 74% de tasa de éxito al mover dinámica fuera del prefijo (blog de proyecto, 2025-11).
- Anti-patrón de paralelalización: informes típicos de inflación de facturas 510x cuando N solicitudes paralelas omiten la primera caché de escritura.

## Usalo con el marco de ejecución

> **【中文解读】**
> La mejor práctica es la de hacer un seguimiento de la información de la información de la información de la información.`cache_control`标记静态前──实测案例:把动态内容移出缓存前,命中率从7% 跳到74%──对于RAG 系统,静态系统提示 + 检索到的文档属于缓存范围,用户问题不属于──

> **【拓展：提示缓存→成本优化】**提示缓存是 LLM 成本优化最直接的手段──Anthropic Claude 的缓存读取价格为$0.30/M token，不到新鲜输入 $Una de las diez de 3.00/M. OpenAI para 1024+ tokens de caché automático rápido, caché de entrada precio de caché de aproximadamente 90%. Para el sistema RAG de procesamiento diario de millones de solicitudes, caché de sugerencias puede reducir la cantidad de cuentas API de cientos de miles de dólares a cientos de miles de dólares.
```figure
semantic-cache-hit
```

## Usalo

`code/main.py`Simula la caché L1 + L2 en cargas de trabajo mixtas.

> `code/main.py`Simula la caché L1 + L2 en cargas de trabajo mixtas.

> `code/main.py`Simula la caché L1 + L2 en cargas de trabajo mixtas.

## Envíe el producto .

> **【拓展：缓存 + 批处理叠加优化】**缓存与批处理 API(Fase 17·15) 叠加效果:批处理 API 50% 折扣 + 缓存输入 ~10x 折扣 = aproximadamente 10% de los costes de sincronización sin缓存.

Esta lección produce`outputs/skill-cache-auditor.md`. Dado el modelo y el tráfico inmediato, las auditorías de caché y recomienda la reestructuración.

> 本课产 出  `outputs/skill-cache-auditor.md`. Dado el modelo y el tráfico inmediato, las auditorías de caché y recomienda la reestructuración.

## Los ejercicios.

1. - ¿ Qué ?`code/main.py`- ¿Cuánto cambia la cuenta?
   Traducción:运行`code/main.py`¿Cuánto se ha incrementado el volumen de la cuenta?
2. Su solicitud del sistema tiene una fecha. Mueva. Muéstren antes / después de golpear la tasa matemática.
   En inglés, el sistema de matemáticas de la matemática de la matemática de la matemática de la matemática de la matemática de la matemática de la matemática de la matemática de la matemática de la matemática.
3. Calcule el equilibrio de 1 hora TTL (2x escribir) vs 5 minutos TTL (1.25x escribir) dada la tasa de llegada de su solicitud.
   China: 1 小时 TTL (en inglés) 写入成本 (en inglés) 2x 写入成本 (en inglés) vs 5 分钟 TTL (en inglés) 1.25x 写入成本 (en inglés) 写入成本 (en inglés) 写入成本 (en inglés) 写入成本 (en inglés) 写入成本 (en inglés) 写入成本 (en inglés) 写入成本 (en inglés) 写入成本 (en inglés) 写入成本 (en inglés) 写入成本 (en inglés) 写入成本 (en inglés) 写入成本 (en inglés) 写入成本 (en inglés) 写入成本 (en inglés) 写入成本 (en inglés) 写入成本) 写入成本 (en inglés) 写入成本 (en inglés) 写入成本 (en inglés) 写入成本) 写入成本 (en inglés) 写入成本 (en inglés) 写入成本) 写入成本 (en inglés) 写入成本) 写入成本 (en inglés) 写入成本) 写入成本 (en inglés) 写入成本) 写入成本 (en inglés) 写入成本) 写入成本 (en inglés) 写入成本) 写入成本 (en inglés) 写入成本)
4. El caché semántico en el umbral de 0.95 alcanza el 20%. en 0.85 alcanza el 50% pero ve respuestas almacenadas en caché incorrectas.
   China 译文:语义缓存值 0.95 时命中率 20%──0.85 时命中率 50% Pero ¿verás fantasía──值设多少?
5. Se hacen 10 subcuestiones paralelas por pregunta de usuario.

## Términos clave .

| Term | What people say | What it actually means |
|------|----------------|------------------------|
| L2 prompt cache | "prefix cache" | Provider stores KV for repeated prefix |
| `cache_control` | "Anthropic cache marker" | Explicit attribute marking cacheable blocks |
| Cache write premium | "write tax" | Extra cost for first miss-to-cache (1.25x or 2x) |
| L1 semantic cache | "embedding cache" | App-level hash-and-embed before calling LLM |
| GPTCache | "LLM caching lib" | Popular OSS L1 cache library |
| Cache hit rate | "hits / total" | Fraction of requests served from cache |
| Parallelization anti-pattern | "the N-write trap" | N parallel requests miss cache N times |
| Dynamic content trap | "the time-in-prompt trap" | Dynamic bytes in prefix kill hit rate |
| RadixAttention | "intra-replica cache" | SGLang's prefix-cache implementation |

## Más Leer más Leer más

- [Anthropic Prompt Caching](https://docs.anthropic.com/en/docs/build-with-claude/prompt-caching) oficial `cache_control`la semántica y los TTL.
- [OpenAI Prompt Caching](https://platform.openai.com/docs/guides/prompt-caching) comportamiento de almacenamiento automático en caché y elegibilidad.
- [TianPan — Semantic Caching for LLMs Production](https://tianpan.co/blog/2026-04-10-semantic-caching-llm-production)
- [ProjectDiscovery — Cut LLM Costs 59% With Prompt Caching](https://projectdiscovery.io/blog/how-we-cut-llm-cost-with-prompt-caching)
- [DigitalOcean / Anthropic — Prompt Caching](https://www.digitalocean.com/blog/prompt-caching-with-digital-ocean)
