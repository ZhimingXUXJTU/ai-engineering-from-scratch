# Porteras de IA  LiteLLM, Portkey, Kong AI Gateway, Bifrost 网关 LLM

> Una puerta de entrada se encuentra entre sus aplicaciones y los proveedores de modelos. Las características principales son el enrutamiento del proveedor, retroceso, retemplajes, limitación de tarifas, referencias secretas, observabilidad, barandillas.**LiteLLM**es MIT OSS con más de 100 proveedores, compatible con OpenAI, pero se descompone alrededor de ~ 2000 RPS (8 GB de memoria, fallas en cascada en benchmarks publicados); mejor para Python, <500 RPS, desarrollo / prototipo. **Portkey**está en el plano de control (garderas, redacción de PII, detección de jailbreak, pistas de auditoría), fue Apache 2.0 de código abierto marzo de 2026, 20-40 ms de latencia por encima, $49/mo production tier. **Kong AI Gateway** built on Kong Gateway — Kong's own benchmark on same 12 CPUs: 228% faster than Portkey, 859% faster than LiteLLM; $Precio de 100/modelo/mes (máximo 5 en nivel Plus); adecuado para empresas si ya está en Kong. **Bifrost**(Maxim AI)  retemplajes automáticos con configurable backkoff, regreso a Anthropic en OpenAI 429. **Cloudflare / Vercel AI Gateways** administrado, operaciones cero, retraso básico. Residencia de datos impulsa la decisión de auto-host; Portkey y Kong se sientan en el medio con OSS + administrado opcional.

> **【中文解读】**Este capítulo presenta la IA 网关LLM Pedidos de ruta, equilibrio de carga y seguridad 网关.


**Type:** Learn | **类型:** 学习
**Languages:** Python (stdlib, toy gateway-routing simulator) | **语言:** Python
**Prerequisites:** Phase 17 · 01 (Managed LLM Platforms), Phase 17 · 16 (Model Routing) | **前置知识:** Phase 17 · 01 (Managed LLM Platforms), Phase 17 · 16 (Model Routing)

> ¿ Qué es esto ?**【前置】**La fase 17 de la plataforma (Fase 17 de la plataforma)  Fase 17 de la plataforma (Fase 16 de la plataforma)  Fase 17 de la plataforma (Fase 17 de la plataforma)  Fase 17 de la plataforma (Fase 17 de la plataforma)  Fase 17 de la plataforma (Fase 17 de la plataforma)  Fase 17 de la plataforma (Fase 17 de la plataforma)  Fase 17 de la plataforma (Fase 17 de la plataforma)  Fase 17 de la plataforma (Fase 17 de la plataforma)  Fase 17 de la plataforma (Fase 17 de la plataforma)  Fase 17 de la plataforma (Fase 17 de la plataforma)  Fase 17 de la plataforma (Fase 17 de la plataforma)  Fase 17 de la plataforma (Fase 17 de la plataforma)  Fase 17 de la plataforma (Fase 17 de la plataforma)  Fase 17 de la plataforma (Fase 17 de la plataforma)  Fase 17 de la plataforma (Fase 17 de la plataforma)  Fase 17 de la plataforma (Fase 17 de la plataforma)  Fase 17 de la plataforma (Fase 17 de la plataforma)  Fase 17 de la plataforma (Fase 17 de la plataforma)  Fase 17 de la plataforma (Fase 17 de la plataforma)  Fase 17 de la plataforma)  Fase 17 de la plataforma (Fase 17 de la plataforma)  Fase 17 de la plataforma (Fase 17 de la plataforma)  Fase 17 de la plataforma (Fase 17 de la plataforma)  Fase 17 de la plataforma (Fase 17 de la plataforma)  Fase 17 de la plataforma)  Fase 17 de la plataforma (Fase 17 de la plataforma)  Fase 17 de la plataforma (Fase 17 de la plataforma)  Fase 17 de la plataforma (Fase 17 de la plataforma)  Fase 17 de la Fase 17 de la Fase 17 de la Fase 17 de la Fase 17 de la Fase 17 de Fase 17 de Fase 17 de Fase 17 de Fase 17 de Fase 17 de Fase 17 de Fase 17 de Fase 17 de Fase (Fase 17 de Fase 17 de Fase de F
> ¿ Qué es esto ?**【类比】**Por ejemplo, en el caso de las empresas de la industria de la información, el número de usuarios de las redes de Internet es de aproximadamente un millón de dólares.
**Time:** ~60 minutes | **时间:** ~60 minutes

## Objetivos de aprendizaje

- Enumera las seis características principales de la puerta de enlace (routing, fallback, retemptadas, límites de velocidad, secretos, observabilidad, barandillas).
  En el caso de los sistemas de control de la red, el sistema de control de la red central tiene una función de control de la red central.
- Mapa de cuatro puertas de acceso 2026 (LiteLLM, Portkey, Kong AI, Bifrost) para escalar los techos y casos de uso.
  La versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión de la versión original de la versión original de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de 2026 de la versión de la versión de la versión de la versión de la versión de la versión de la versión de 2026 de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de 20 de la versión de la versión de 20 de la versión de la versión de 20 de la versión de la versión de la versión de 20 de la versión de la versión de la versión de 20 de la versión de la versión de la versión de la versión de 20 de la versión de 20 de la versión de la versión de la versión de la versión de la versión de 20 de la versión de la versión de la versión de la versión de la versión de la versión de la versión de 20 de la versión de la versión de la versión de la versión de la versión de la versión de la versión de 20 de la versión de la versión de la versión de la versión de la versión de la versión de 20 de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de
- Cita el índice de referencia Kong (228% vs Portkey, 859% vs LiteLLM) y explica por qué importa para > 500 RPS.
  China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China:
- Elija auto-hosted vs administrado dado el presupuesto de residencia de datos y operaciones.
  Traducción:给定数据驻留和运维预算,选择自托管 vs.托管──

## El problema es la introducción del problema

> **【中文解读】**El problema central de la solución de la red de conexión se encuentra entre la aplicación y el proveedor de modelos. Los productos utilizan al mismo tiempo OpenAI, un sistema de gestión de datos antropológico y autotrópico, cada proveedor tiene diferentes SDK, modelos errados, restricciones de velocidad y programas de certificación. La red de conexión de conexión de conexión de conexión de conexión de conexión de conexión de conexión de conexión de conexión de conexión de conexión de conexión de conexión de conexión de conexión de conexión de conexión de conexión de conexión de conexión de conexión de conexión de conexión de conexión de conexión de conexión de conexión de conexión de conexión de conexión de conexión de conexión de conexión de conexión de conexión de conexión de conexión de conexión de conexión de conexión de conexión de conexión de conexión de conexión de conexión de conexión de conexión de conexión de conexión de conexión de conexión de conexión de conexión de conexión de conexión de conexión de conexión de conexión de conexión de conexión de conexión de conexión de conexión de conexión de conexión de conexión de conexión de conexión de conexión de conexión de conexión de conexión de conexión de conexión de conexión de conexión de conexión de conexión de conexión de conexión de conexión de conexión de conexión de conexión de conexión de conexión de conexión de conexión de conexión de conexión de conexión de conexión de conexión de conexión de conexión de conexión de conexión de conexión de conexión de conexión de conexión de conexión de conexión de conexión de conexión de conexión de conexión de conexión de conexión de conexión de conexión de conexión de conexión de conexión de conexión de conexión de conexión de conexión de conexión de conexión de conexión de conexión de conexión de conexión de conexión de conexión de conexión de conexión de conexión de conexión de conexión de conexión de conexión de conexión de conexión de conexión de conexión de conexión de conexión de conexión de conexión de conexión de conexión de conexión de

> **【拓展：2026 年 AI 网关市场】**Los cuatro principales jugadores del mercado de la red de inteligencia artificial en 2026: 1) LiteLLMMIT 开源,100+ proveedores, pero en ~2000 RPS 时崩(8GB内存); 2) Portkey2026 3月开源 Apache 2.0,控制面定位(garderrails、PII 脱敏、越狱检测、审计追踪),20-40ms 延迟开销; 3) Kong AI Gateway 基于成熟的 API 网关产品,Kong 基准测试显示比自己的 Portkey 快 228%、比 LiteLLM 快 859%; 4) Cloudflare/Vercel AI Gateway 托管、零运维、边缘部署.

Su producto llama OpenAI, Anthropic y un Llama auto-hosted. Cada proveedor tiene un SDK diferente, modelo de error, límite de tarifa y esquema de auth.

Reinventando esto en la capa de aplicación, se combina cada servicio con cada proveedor. Una capa de puerta de enlace lo consolida en un proceso con una API (generalmente compatible con OpenAI) que se distribuye a los proveedores.

## El concepto central.

### Seis características centrales

1. **Provider routing** OpenAI, Anthropic, Gemini, auto-hosted, etc. detrás de una API.
2. **Fallback** en 429, 5xx, o fallas de calidad, vuelva a intentarlo en otro lugar.
3. **Retries** retroceso exponencial, intentos limitados.
4. **Rate limits** por inquilino, por llave, por modelo.
5. **Secret references** sacar las credenciales de la bóveda en el tiempo de ejecución (nunca en la aplicación).
6. **Observability** ATRITUDOS OTEL + GenAI (fase 17 · 13) + atribución de costes.
7. **Guardrails** Reducción de PII, detección de jailbreak, filtros de temas permitidos.

### LiteLLM  MIT OSS, Python

- 100+ proveedores, compatibles con OpenAI, configuración del router, retroceso, observabilidad básica.
- Se rompe alrededor de 2000 RPS en el punto de referencia de Kong; 8 GB de memoria, fallas en cascada bajo carga sostenida.
- Mejor ajuste: aplicación Python, < 500 RPS, puertas de acceso de desarrollo/estagiado, enrutamiento experimental.
- Costo: $0 para OSS; existe un nivel libre de nube.

### Portkey  posicionamiento del plano de control

- Apache 2.0 OSS a partir de marzo de 2026. Rastreos de seguridad, redacción de PII, detección de jailbreak, rastro de auditoría.
- 20-40 ms por solicitud de latencia general.
- $49 / mes para el nivel de producción con retención + SLA.
- Mejor adaptación: industrias reguladas que necesitan barandillas + observabilidad en conjunto.

### Kong AI Gateway  el juego de la escala

- Construido en Kong Gateway (producto de API maduro, lua+OpenResty).
- El propio índice de referencia de Kong en el equivalente de 12 CPU: 228% más rápido que Portkey, 859% más rápido que LiteLLM.
- Precio: $ 100 / modelo / mes, máximo 5 en el nivel Plus.
- Mejor ajuste: ya en Kong; > 1000 RPS; dispuesto a licenciar.

### Bifrost (Maxim AI)

- Pruebas automáticas con retroceso configurable.
- Fallback a Anthropic en OpenAI 429 es una receta canónica.
- Nuevo participante, comercial.

### Puerta de entrada de IA de Cloudflare / Puerta de entrada de IA de Vercel

- Gestionado, operaciones cero, retoma y observabilidad básica.
- Mejor ajuste: aplicaciones JavaScript de Edge en Cloudflare/Vercel.
- Limitado en comparación con Kong/Portkey en barandillas y límites de velocidad.

### Auto-hosted vs administrado

> **【中文解读】**El sistema de gestión de datos de la empresa es el más amplio de los sistemas de gestión de datos de la compañía. El sistema de gestión de datos de la empresa es el más amplio de los sistemas de gestión de datos de la compañía.

> **【拓展：网关 + 可观测性 + 路由的组合】**Fase 17·13(可观测性) + 16(模型路由) + 19(网关) está en producción es la misma capa.

La residencia de datos es la función de forzamiento. Cuidado de salud y finanzas auto-hosting por defecto (LiteLLM o Portkey OSS o Kong). Productos de consumo administrados por defecto (Cloudflare AI Gateway) o de nivel medio (Portkey administrado).

### Presupuesto de la latencia

> **【拓展：AI 网关延迟预算分析】**AI 网关延迟直接影响TTFT,是选型的关键因素. (1) LiteLLM 5-15msPython 实现,简单但高并发下不稳定;[2] Portkey 20-40ms功能最全面但延迟最高;[3] Kong 3-8msGo + OpenResty,延迟最低且高并发稳定;[4] Cloudflare/Vercel 1-3ms边缘部署优势.

- LiteLLM: 5-15 ms de carga aérea típico.
- Portero: 20-40 ms por encima.
- 3 a 8 ms por encima.
- Cloudflare/Vercel: 1-3 ms de gastos generales (avantage de borde).

La latencia de la puerta de enlace se agrega directamente a TTFT. Para TTFT P99 < 100 ms SLA, Kong o Cloudflare. Para P99 < 500 ms, cualquier.

### Materia de semántica de límite de tasas

El token-bucket simple funciona hasta una escala moderada. Multi-tenant requiere una ventana deslizante + franquicia de explosión + tiering por tenente. LiteLLM navega token-bucket; Kong navega ventana deslizante; Portkey navega en niveles.

### Puerta de entrada + observabilidad + enrutamiento componer

La fase 17 · 13 (observabilidad) + 16 (routing de modelo) + 19 (gateways) son la misma capa en producción. Elija una herramienta que cubra las tres o cableálas cuidadosamente: la mayoría de las implementaciones de 2026 combinan Helicone (observabilidad) o Portkey (garderrails) con Kong (escala) para funciones divididas.

### Números que debes recordar

- LiteLLM: rompe a ~ 2000 RPS, memoria de 8 GB.
- Portkey: 20-40 ms por encima; Apache 2.0 desde marzo de 2026.
- Kong: 228% más rápido que Portkey, 859% más rápido que LiteLLM.
- Precio de Kong: $ 100 / modelo / mes, 5 max en el nivel Plus.
- Cloudflare/Vercel: 1-3 ms de carga en el borde.

## Usalo con el marco de ejecución
```figure
mx-gateway-fallback
```

## Usalo

`code/main.py`Simula el enrutamiento de la puerta de enlace con fallback en 3 proveedores bajo la inyección 429/5xx. Informes latencia, tasa de retiro y tasa de impacto de fallback.

> `code/main.py`Simula el enrutamiento de la puerta de enlace con fallback en 3 proveedores bajo la inyección 429/5xx. Informes latencia, tasa de retiro y tasa de impacto de fallback.

> `code/main.py`Simula el enrutamiento de la puerta de enlace con fallback en 3 proveedores bajo la inyección 429/5xx. Informes latencia, tasa de retiro y tasa de impacto de fallback.

## Envíe el producto .

Esta lección produce`outputs/skill-gateway-picker.md`Dada la escala, la postura de las operaciones, el cumplimiento, el presupuesto de latencia, elige una puerta de entrada.

> 本课产 出  `outputs/skill-gateway-picker.md`Dada la escala, la postura de las operaciones, el cumplimiento, el presupuesto de latencia, elige una puerta de entrada.

## Los ejercicios.

1. - ¿ Qué ?`code/main.py`. Configurar fallback desde OpenAI→Anthropic→auto-hosted. ¿Cuál es la tasa de impacto esperada con una tasa de error del proveedor del 5%?
   Traducción:运行`code/main.py` Configurar OpenAI -> Antropic -> Autotúmenes de regreso. ¿Cuál es la condición de desarrollo más razonable?
2. Su SLA es TTFT P99 < 200 ms en una línea de base de 300 ms. ¿Qué pasarelas se mantienen dentro del presupuesto?
   Sinopsis: ¿Cuál es la línea de acceso de la red de Internet de la red de Internet de la red de Internet de la red de Internet de la red de Internet de la red de Internet de la red de Internet de la red de Internet de la red de Internet de la red de Internet de la red de Internet de la red de Internet de la red de Internet de la red de Internet de la red de Internet de la red de Internet de la red de Internet de la red de Internet de la red de Internet de la red de Internet de la red de Internet de la red de Internet de la red de Internet de la red de Internet de la red de Internet de la red de Internet de la red de Internet de la red de Internet de la red de Internet de la red de Internet de la red de Internet de la red de Internet de la red de Internet de la red de Internet de la red de Internet de la red de Internet de China?
3. Un cliente de atención médica requiere auto-hosting + redacción de PII + auditoría.
   Un cliente de salud necesita autosuficiencia + PII 脱敏 + 审计――选择 Portkey OSS 或 Kong――
4. Comparar LiteLLM vs Kong: ¿a qué límite RPS debe migrar un equipo?
   Comparación LiteLLM vs Kong: ¿Qué equipo en RPS arriba límite debe mudarse?
5. Diseñar una política de límite de tarifas para un SaaS multi-arrendatario: nivel gratuito, nivel de prueba, nivel pagado.

## Términos clave .

| Term | What people say | What it actually means |
|------|----------------|------------------------|
| Gateway | "API broker" | Process sitting between apps and providers |
| LiteLLM | "the MIT one" | Python OSS, 100+ providers, breaks at 2K RPS |
| Portkey | "guardrails gateway" | Control plane + observability, Apache 2.0 |
| Kong AI Gateway | "the scale one" | Built on Kong Gateway, benchmark leader |
| Bifrost | "Maxim's gateway" | Retries + Anthropic fallback recipe |
| Cloudflare AI Gateway | "edge managed" | Edge-deployed managed gateway, zero-ops |
| PII redaction | "data scrub" | Regex + NER mask before sending to model |
| Jailbreak detection | "prompt injection guard" | Classifier on user input |
| Audit trail | "regulated log" | Immutable record of every LLM call |
| Token-bucket | "simple rate limit" | Refill-based rate limiter |
| Sliding-window | "precise rate limit" | Time-windowed rate limiter; better fairness |

## Más Leer más Leer más

- [Kong AI Gateway Benchmark](https://konghq.com/blog/engineering/ai-gateway-benchmark-kong-ai-gateway-portkey-litellm)
- [TrueFoundry — AI Gateways 2026 Comparison](https://www.truefoundry.com/blog/a-definitive-guide-to-ai-gateways-in-2026-competitive-landscape-comparison)
- [Techsy — Top LLM Gateway Tools 2026](https://techsy.io/en/blog/best-llm-gateway-tools)
- [LiteLLM GitHub](https://github.com/BerriAI/litellm)
- [Portkey GitHub](https://github.com/Portkey-AI/gateway)
- [Kong AI Gateway docs](https://docs.konghq.com/gateway/latest/ai-gateway/)
