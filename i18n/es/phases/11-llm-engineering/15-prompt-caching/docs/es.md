# Caché de texto y contexto de caché de texto

> Su sistema de solicitud de inicio es de 4.000 tokens. Su contexto RAG es de 20.000 tokens. Se envían ambos con cada solicitud. También se paga por ambos  cada vez. El caché de inicio permite al proveedor mantener ese prefijo caliente en su lado y facturarle el 10% de la tasa normal en la reutilización. Se utiliza correctamente, reduce el costo de inferencia en 5090% y la latencia de la primera señal en 4085%.

> **【中文解读】**系统提示4000代币 + RAG 上下文20000代币, por solicitud debe pagar. 提示缓存让供应商保留前,重用时只收取10%费用.

> **【拓展：提示缓存→RAG生产优化】**La respuesta en caché de la Antropic Prompte Caching y OpenAI es la clave de los sistemas de producción RAG para reducir el costo, especialmente con la tendencia de sistemas fijos y una gran cantidad de búsquedas en el escenario siguiente.

> ¿ Qué es esto ?**【前置】**学本节前请先掌握:Fase 11·01(Integrado rápido)、Fase 11·05(Ingeniería de contexto)、Fase 11·11(Cost de almacenamiento)。本节是其延伸,讲供应商层(Antropic cache_control、OpenAI自动缓存、Gemini CachedContent)。

**Type:** Build | **类型:** 构建
**Languages:** Python | **语言:** Python
**Prerequisites:** Phase 11 · 01 (Prompt Engineering), Phase 11 · 05 (Context Engineering), Phase 11 · 11 (Caching and Cost) | **前置知识:** Phase 11 · 01 (提示工程)、05 (上下文工程)、11 (缓存与成本)
**Time:** ~60 minutes | **时间:** ~60 分钟

## El problema es la introducción del problema

Un agente de codificación envía el mismo aviso de sistema de 15,000 tokens a Claude en cada giro de una conversación.$3/M input tokens is $El costo de entrada solo es de 0,90 antes de cualquier mensaje real del usuario. Multiplica por 10,000 conversaciones diarias y la factura alcanza $9,000 / día por texto que nunca cambia.

> Un agente programador en cada ronda de conversación envía los mismos 15.000 tokens de instrucciones de sistema a Claude.$3/M 输入 token，仅输入成本就是 $0.90 también no incluye las noticias reales del usuario.

No se puede reducir el aviso sin perjudicar la calidad. No se puede evitar enviarlo  el modelo lo necesita en cada turno. El único movimiento es dejar de pagar el precio completo por un prefijo que el proveedor ya ha visto.

> No puedes reducir la oferta sin dañar la calidad. No puedes evitar enviarla. El único modo de evitar el pago total del precio previo que el proveedor ya ha visto.

> ¿ Qué es esto ?**【类比】**Caché rápido 像"快递公司记住你的常用地址"第一次发货要详细说明"北京市朝阳区...",后每次发货只需说"老地方",快递公司自动调出地址──技术上:供应商把前的 KV缓存存在自己的服务器,下次请求来时直接复用,不需要重新计算注意的 K/V矩阵──对用户透明你只需在API调用加个`cache_control`标记──

> ️ **【易错点】**Caching rápido de 3 个坑:(1) **prefix 顺序敏感**cache 命中要求 prefijo 完全相同(incluye空格、换行), sistema de inmediato 末尾多一个空格就错过;务必把可变部分(usuary输入)放最后。(2) **cache TTL 5 分钟**Antropic 默认 5 分钟过期,没流量时 cache 失效; con TTL extendido(1 小时)保住冷启动场景──(3) **没监控命中率** no sabemos la tasa de éxito  no podemos juzgar los beneficios `cache_creation_input_tokens`Y `cache_read_input_tokens`, el registro hasta el control de la tabla.

La aplicación fue lanzada en agosto de 2024 por Anthropic (con una variante de 1 hora de TTL extendida en 2025), OpenAI la automatizó más tarde ese año, Google lanzó la caché de contexto explícito junto con Gemini 1.5, y los tres ahora la ofrecen como una característica de primera clase en sus modelos fronterizos.

> Este método es para sugerir el almacenamiento. En agosto de 2024, Anthropic lanzó el mismo sistema. En 2025, OpenAI lo automatizó más tarde en el año, Google introdujo el mismo sistema en Gemini 1.5 junto a Google.


> **【中文解读】**El valor de la caché rápida depende del sistema de caché rápido (normalmente mucho tiempo) y en todas las solicitudes no cambia.


## El concepto central.

> **【中文解读】**El caché rápido utiliza las características del LLM 推理 Si varias solicitudes comparten el mismo prompt anterior, se puede cazar el KV-cache anterior 计算结果, evitar repetir el cálculo.

> **【拓展：Prompt Caching 的成本节省】**La caché rápida de Anthropic va a repetir la entrada anterior, el coste se reducirá en un 90% o más.$0.50/M tokens（原价 $5)。 para sistemas de instantánea de 5K tokens + 平均10 veces reutilización de escenarios,月成本可降低约75%──


![Prompt caching: write once, read cheap](../assets/prompt-caching.svg)

**The mechanic.**Cuando el prefijo de una solicitud coincide con uno de una solicitud reciente, el proveedor sirve el caché KV de la ejecución anterior en lugar de volver a codificar los tokens.

> **机制。**Cuando el pre de la solicitud coincide con el pre de la solicitud reciente, el proveedor ofrece KV-cache desde la operación anterior, en lugar de volver a codificar el token―: Usted paga por primera vez una pequeña cantidad de pre de inscripción, luego se disfruta de un descuento masivo en cada lectura―:

**Three provider flavors in 2026.**

| Provider | API style | Hit discount | Write premium | Default TTL | Min cacheable |
|---------|-----------|--------------|---------------|-------------|---------------|
| Anthropic | Explicit `cache_control` markers on content blocks | 90% off input | 25% surcharge | 5 min (extendable to 1 hour) | 1,024 tokens (Sonnet/Opus), 2,048 (Haiku) |
| OpenAI | Automatic prefix detection | 50% off input | none | Up to 1 hour (best-effort) | 1,024 tokens |
| Google (Gemini) | Explicit `CachedContent` API | Storage-billed; read at ~25% of normal | Storage fee per token·hour | User-set (default 1 hour) | 4,096 tokens (Flash), 32,768 (Pro) |

**The invariant.**Si algún token difiere entre las solicitudes, todo después del primer token diferente es un error. Coloque las partes *estables* en la parte superior, las partes *variables* en la parte inferior.

> **不变量。**Tres personas solo se mantienen en el caché. Si hay algún token entre las solicitudes, el primer token es diferente. Después de todo, todo lo que contiene está en el caché.

### El diseño de la caché

```
[system prompt]          <-- cache this
[tool definitions]       <-- cache this
[few-shot examples]      <-- cache this
[retrieved documents]    <-- cache if reused, else don't
[conversation history]   <-- cache up to last turn
[current user message]   <-- never cache (different every time)
```

Viola el orden  poner el mensaje del usuario por encima del aviso del sistema, intercalar las recuperaciones dinámicas entre unas pocas tomas  y el caché nunca golpea.

>  Contrario al orden  El mensaje del usuario se coloca sobre el sistema de sugerencias, entre pocos ejemplos entre entre entre entre entre entre

### El cálculo del equilibrio

El 25% de la prima de escritura de Anthropic significa que un bloque almacenado en caché debe leerse al menos dos veces para ahorrar dinero neto. 1 escribir + 1 leer promedio de 0.675x costo por solicitud (ahorra 32%); 1 escribir + 10 leer promedio de 0.205x (ahorra 80%). regla general: almacenar en caché cualquier cosa que espera reutilizar al menos 3 veces dentro del TTL.

> El 25% de la antropeza 写入溢价 significa que los bloques de almacenamiento deben ser leídos al menos dos veces para poder conservar el dinero 经验法则:

## Construye y realiza.
```figure
prompt-cache-hit
```

## Construye el mismo

### Paso 1: Caching de la llamada antropópica con marcadores explícitos

```python
import anthropic

client = anthropic.Anthropic()

SYSTEM = [
    {
        "type": "text",
        "text": "You are a senior Python reviewer. Follow the rubric exactly.\n\n" + RUBRIC_15K_TOKENS,
        "cache_control": {"type": "ephemeral"},
    }
]

def review(code: str):
    return client.messages.create(
        model="claude-opus-4-7",
        max_tokens=1024,
        system=SYSTEM,
        messages=[{"role": "user", "content": code}],
    )
```

El `cache_control`el marcador le dice a Anthropic que almacene el bloque durante 5 minutos.

> `cache_control`标记告诉人类将该块存储 5 分钟. 标记告诉人类将该块存储 5 分钟.

**Response usage fields:**

```python
response = review(code_a)
response.usage
# InputTokensUsage(
#     input_tokens=120,
#     cache_creation_input_tokens=15023,   # paid at 1.25x
#     cache_read_input_tokens=0,
#     output_tokens=340,
# )

response_b = review(code_b)
response_b.usage
# cache_creation_input_tokens=0
# cache_read_input_tokens=15023           # paid at 0.1x
```

Verifique ambos campos en CI  si `cache_read_input_tokens`se mantiene en cero en todas las solicitudes, sus claves de caché están a la deriva.

> En el CI, revise estos dos segmentos si`cache_read_input_tokens`En varias veces de la solicitud mantener para cero, su caché de la clave está flotando.

### Paso 2: TTL extendido por una hora

Para los trabajos de larga duración, el plazo de 5 minutos de incumplimiento expira entre los trabajos.`ttl`¿Qué es esto ?

```python
{"type": "text", "text": RUBRIC, "cache_control": {"type": "ephemeral", "ttl": "1h"}}
```

El TTL de una hora cuesta el doble de la prima de escritura (50% sobre el límite de referencia en lugar de 25%) pero se devuelve rápidamente en cualquier lote que reutilice el prefijo más de 5 veces.

> El precio de entrada de 1 小时 TTL es 2 veces el 50% de la base y no el 25%), pero se vuelve muy rápido en cualquier uso anterior a 5 veces de la carga.

### Paso 3: Caché automático de OpenAI

OpenAI no le da nada para configurar. Cualquier prefijo de más de 1.024 tokens que coincida con una solicitud reciente obtiene un descuento del 50% automáticamente.

```python
from openai import OpenAI
client = OpenAI()

resp = client.chat.completions.create(
    model="gpt-5",
    messages=[
        {"role": "system", "content": SYSTEM_PROMPT},   # long and stable
        {"role": "user", "content": user_msg},
    ],
)
resp.usage.prompt_tokens_details.cached_tokens  # the discounted portion
```

La misma regla de diseño amigable con la caché se aplica. Dos cosas matan la caché de OpenAI que no matan la de Anthropic: cambiar la `user`campo (utilizado como componente de clave de caché) y herramientas de reordenamiento.

> También se aplican las reglas de la estructura de la caché. Dos cosas matarán la caché de OpenAI y no matarán a la antropic.`user`字段和重新排序工具── también se puede utilizar para la clasificación de los productos.

### Paso 4: Gemini caché de contexto explícito

Gemini trata el caché como un objeto de primera clase que se crea y nombra:

```python
from google import genai
from google.genai import types

client = genai.Client()

cache = client.caches.create(
    model="gemini-3-pro",
    config=types.CreateCachedContentConfig(
        display_name="rubric-v3",
        system_instruction=RUBRIC,
        contents=[FEW_SHOT_EXAMPLES],
        ttl="3600s",
    ),
)

resp = client.models.generate_content(
    model="gemini-3-pro",
    contents=["Review this code:\n" + code],
    config=types.GenerateContentConfig(cached_content=cache.name),
)
```

Gemini carga almacenamiento por token·hora durante el tiempo que la caché vive, y se lee a ~25% de la tasa de entrada normal. Esta es la forma correcta cuando se reutiliza el mismo prompt gigante en muchas sesiones durante días.

> Gemini 按缓存存活期间每令牌·小时收取存储费,读取费率约为正常输入的25%──当你在多次会议中跨天重复使用相同的大型提示时,这是正确的选择──

### Paso 5: medición de la tasa de impacto en la producción

¿ Qué ?`code/main.py`para un contador simulado de tres proveedores que rastrea el conteo de escritura/lectura/falta y calcula el costo combinado por 1K solicitudes.

> ¿ Qué ?`code/main.py`获取模拟的三供应商会计师,跟踪写入/读取/未命中计数并计算每千请求的混合成本──按目标命中率门控部署多数生产 预热后应见在预热设置 >80% 读取比例──

## Las trampas que todavía se envían en 2026

> El año 2026 sigue en la trampa:

- **Dynamic timestamps at the top.** `"Current time: 2026-04-22 15:30:02"`En la parte superior del sistema de la llamada. cada solicitud se pierde. Mover las marcas de tiempo por debajo del punto de ruptura de caché.
  **顶部的动态时间戳。**系统提示顶部放                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        `"Current time: 2026-04-22 15:30:02"`                                                                                                                                                                                                                                                              
- **Tool reordering.**Serializa las herramientas en un orden estable  un reajuste dictado entre los despliegues rompe cada golpe.
  **工具重排序。**Es un instrumento de ordenamiento estable y de ordenamiento.
- **Free-text near-duplicates.**"Eres útil". vs "Eres un asistente útil".  una diferencia de un byte = falta total.
  **自由文本近似重复。**"Eres útil". vs "Eres un ayudante útil".
- **Too-small blocks.**Anthropic impone un piso de 1.024 tokens (2.048 para Haiku).
  **过小的块。**Antropic 强制 1,024 token 下限(Haiku 为 2,048)。更小的块静默不缓存。
- **Blind cost dashboards.**Divide "tokens de entrada" en caché vs no caché. de lo contrario una caída de tráfico se parece a una ganancia caché.
  **盲目的成本仪表板。**De esta forma, el "token de entrada" se descompone en caché vs. caché.

## Usalo con el marco de ejecución

La pila de almacenamiento en caché de 2026:

> 2026 缓存技术:

| Situation | Pick |
|-----------|------|
| Agent with stable 10k+ system prompt, many turns | Anthropic `cache_control` with 5-min TTL |
| Batch job reusing a prefix for 30+ minutes | Anthropic with `ttl: "1h"` |
| Serverless endpoints on GPT-5, no custom infra | OpenAI automatic (just make your prefix stable and long) |
| Multi-day reuse of a giant code/doc corpus | Gemini explicit `CachedContent` |
| Cross-provider fallback | Keep the cacheable prefix layout identical across providers so any hit works |

| 场景 | 选择 |
|------|------|
| Agent 有稳定 10k+ 系统提示、多轮 | Anthropic `cache_control` 配 5 分钟 TTL |
| 批处理重用前缀 30+ 分钟 | Anthropic 配 `ttl: "1h"` |
| GPT-5 上的无服务器端点、无定制基建 | OpenAI 自动（让前缀稳定且够长） |
| 多天重用大型代码/文档语料 | Gemini 显式 `CachedContent` |
| 跨提供商回退 | 跨提供商保持可缓存前缀布局一致，任何命中都工作 |

Combina con el caché semántico (fase 11 · 11) para la capa de mensaje de usuario: mantulas de caché de inmediato *utilización idéntica a los tokens*, mantulas de caché semántico *utilización idéntica a los significados*

> Conjunto para el usuario de la información:提示缓存处理*token 完全相同*的重用,语义缓存处理*语义相同*的重用──

## Envíe el producto .

Salva .`outputs/skill-prompt-caching-planner.md`¿Qué es esto ?

```markdown
---
name: prompt-caching-planner
description: Design a cache-friendly prompt layout and pick the right provider caching mode.
version: 1.0.0
phase: 11
lesson: 15
tags: [llm-engineering, caching, cost]
---

Given a prompt (system + tools + few-shot + retrieval + history + user) and a usage profile (requests per hour, TTL needed, provider), output:

1. Layout. Reordered sections with a single cache breakpoint marked; explain which sections are stable, which are volatile.
2. Provider mode. Anthropic cache_control, OpenAI automatic, or Gemini CachedContent. Justify from TTL and reuse pattern.
3. Break-even. Expected reads per write within TTL; net cost vs no-cache with math.
4. Verification plan. CI assertion that cache_read_input_tokens > 0 on the second identical request; dashboard split by cached vs uncached tokens.
5. Failure modes. List the three most likely reasons the cache will miss in this setup (dynamic timestamp, tool reorder, near-duplicate text) and how you will prevent each.

Refuse to ship a cache plan that places a dynamic field above the breakpoint. Refuse to enable 1h TTL without a reuse count that makes the 2x write premium pay back.
```

## Los ejercicios.

1. **Easy.**Haga una conversación de 10 vueltas con un sistema de 5,000 tokens contra Claude.`cache_control`y luego con. Reporte la factura de los tokens de entrada para cada uno.
   取一个10轮对话和5000代币 系统提示,不使用和使用 `cache_control`Se trata de un proyecto de investigación que se desarrolla en el sector de la energía.
2. **Medium.**Escriba un arnés de prueba que, dado una plantilla de solicitud y un registro de solicitud, compute la tasa de éxito esperada y el ahorro en dólares por proveedor (Antropic 5m, Anthropic 1h, OpenAI automático, Gemini explícito).
    redacción de herramientas de prueba, formularios de sugerencias y diarios de peticiones, cálculo de la tasa de éxito esperada y de ahorro de cada proveedor 
3. **Hard.**Construir un optimizador de diseño: se le da una respuesta y una lista de campos marcados `stable=True/False`, reescribir el prompt para poner un solo punto de ruptura de caché en la posición máxima amigable con la caché sin perder información. Verificar en un punto final real de Antropic.
   构建布局优化器:重写提示将缓存断点放在最大缓存友好位置――

## Términos clave .

| Term | What people say | What it actually means | 中文释义 |
|------|-----------------|-----------------------|---------|
| Prompt caching | "Makes long prompts cheap" / "让长提示变便宜" | Reusing a provider-side KV-cache for matching prefixes; 50-90% discount on repeated input tokens. | 提示缓存：重用供应商端的 KV-cache，对重复输入 token 提供 50-90% 折扣 |
| `cache_control` | "The Anthropic marker" / "Anthropic 标记" | Content-block attribute that declares "everything up to here is cacheable"; `{"type": "ephemeral"}`. | cache_control：内容块属性，声明"到这里为止的内容可缓存" |
| Cache write | "Paying the premium" / "付溢价" | The first request that populates the cache; billed at ~1.25x input rate on Anthropic, free on OpenAI. | 缓存写入：第一次填充缓存的请求 |
| Cache read | "The discount" / "折扣" | Subsequent requests matching the prefix; billed at 10% (Anthropic), 50% (OpenAI), ~25% (Gemini). | 缓存读取：匹配前缀的后续请求 |
| TTL | "How long it lives" / "存活时间" | Seconds the cache stays warm; Anthropic 5m default (extendable 1h), OpenAI best-effort up to 1h, Gemini user-set. | TTL：缓存保持活跃的秒数 |
| Extended TTL | "1-hour Anthropic cache" / "1小时缓存" | `{"type": "ephemeral", "ttl": "1h"}`; 2x write premium but worth it for batch reuse. | 扩展 TTL：1 小时缓存，2 倍写入溢价 |
| Prefix match | "Why my cache missed" / "为什么缓存未命中" | Caches only hit when every token from the start up to the breakpoint is byte-identical. | 前缀匹配：缓存只在从开头到断点的每个 token 完全相同时才命中 |
| Context caching (Gemini) | "The explicit one" / "显式缓存" | Google's named, storage-billed cache object; best for multi-day reuse of large corpora. | 上下文缓存 (Gemini)：命名、按存储计费的缓存对象 |

## Más Leer más Leer más

- [Anthropic — Prompt caching](https://docs.anthropic.com/en/docs/build-with-claude/prompt-caching)¿ Qué es esto ?`cache_control`, 1 hora TTL, la mesa de equilibrio.
  Antropic 提示缓存文档 cache_control、1 小时 TTL、亏平衡表──
- [OpenAI — Prompt caching](https://platform.openai.com/docs/guides/prompt-caching) Aparición automática de prefijos.
  OpenAI 提示缓存文档 自動前匹配──
- [Google — Context caching](https://ai.google.dev/gemini-api/docs/caching)¿ Qué es esto ?`CachedContent`API y precios de almacenamiento.
  Google 上下文缓存文档CachedContent API y el precio del almacenamiento
- [Anthropic engineering — Prompt caching for long-context workloads](https://www.anthropic.com/news/prompt-caching) puesto de lanzamiento original con números de latencia.
  Antropic 工程博客长上下文工作负载的提示缓存,含延迟数据──
- Fase 11 · 05 (Ingeniería de contexto)  donde cortar el prompt para que la caché pueda aterrizar.
  Se trata de un proyecto de investigación que se desarrolla en el ámbito de la salud y de la salud.
- Fase 11 · 11 (Caching y Cost)  pareja de caché de la solicitud con una caché semántica en los mensajes del usuario.
  Se trata de un proyecto de investigación que se desarrolla en el ámbito de la seguridad y la seguridad.
- [Pope et al., "Efficiently Scaling Transformer Inference" (2022)](https://arxiv.org/abs/2211.05102) el modelo de memoria de caché KV que solicita el almacenamiento en caché expone a los usuarios; explica por qué un prefijo almacenado en caché es ~ 10 veces más barato de volver a leer que de recombutar.
  解释为什么缓存前比重算便宜约10倍的KV-cache 内存模型论文──
- [Agrawal et al., "SARATHI: Efficient LLM Inference by Piggybacking Decodes with Chunked Prefills" (2023)](https://arxiv.org/abs/2308.16369) prefill es el acorta de caché de fase de prompt; este artículo explica por qué TTFT cae dramáticamente en el caché golpeado mientras que TPOT no se ve afectado.
  Explicación de por qué la TTFT se redujo en gran medida y la TPOT no se vio afectada en el estudio.
- [Leviathan et al., "Fast Inference from Transformers via Speculative Decoding" (2023)](https://arxiv.org/abs/2211.17192) el caché rápido se encuentra junto al descifrado especulativo, Flash Attention y MQA/GQA como palancas que doblan la curva de costo de inferencia; lea esto para los otros tres.
  提示缓存与投机解码、Flash Attention 和 MQA/GQA 并列的推理成本曲线杆──
