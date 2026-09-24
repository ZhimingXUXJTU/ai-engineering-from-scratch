# La economía de la plataforma de inferencia  Fuegos artificiales, juntos, baseten, modal, replicado, en cualquier escala 推理 经济学

> El mercado de inferencias de 2026 ya no es alquiler de tiempo de GPU. Se bifurca en silicio personalizado (Groq, Cerebras, SambaNova), plataformas de GPU (Baseten, Together, Fireworks, Modal) y mercados de primer nivel de API (Replicate, DeepInfra).$1/hr per GPU on May 1, 2026, and $La valoración 4B en tokens 10T+/día indica el modelo de trabajo basado en el volumen.$300M Series E at $La regla de posicionamiento competitivo es simple: Fuegos artificiales optimiza la latencia, Juntos optimiza la amplitud del catálogo, Baseten optimiza el pulido empresarial, Modal optimiza Python-nativo DX, Replicate optimiza el alcance multimodal, Anyscale optimiza distribuido Python. Esta lección le da una matriz que puede entregar a un fundador.

> **【中文解读】**Este capítulo presenta la estructura de costes de servicios de evaluación, modelos de precios y análisis económico.
**Type:** Learn
**Languages:** Python (stdlib, toy per-call economics comparator)
**Prerequisites:** Phase 17 · 01 (Managed LLM Platforms), Phase 17 · 04 (Serving Engine Internals)
**Time:** ~60 minutes


**Type:** Learn | **类型:** 学习
**Languages:** Python (stdlib, toy per-call economics comparator) | **语言:** Python（标准库，每次调用经济性比较器）
**Prerequisites:** Phase 17 · 01 (Managed LLM Platforms), Phase 17 · 04 (vLLM Serving Internals) | **前置知识:** Phase 17 · 01（托管 LLM 平台）, Phase 17 · 04（vLLM 服务内部）

> ¿ Qué es esto ?**【前置】**學本節前 請先掌握:Fase 17·01 托管 LLM 平台) 、Fase 17·04 vLLM 内部) ⋅ 本节是 2026 推理平台选型矩阵。
> ¿ Qué es esto ?**【类比】**推理平台 = "AI 云服务商"──三类:(1) 定制芯片(Groq/Cerebras/SambaNova) = 专用 CPU;(2) GPU 平台(Baseten/Together/Fireworks/Modal)=通用云;(3) API 市场(Replicate/DeepInfra)= 应用商店──选型口:Fireworks 低延迟、Together 模型多Baseten 企业级、Modal多原生、Replicate模态广、Anyscale 分布式 Python──

## Objetivos de aprendizaje

- Nombre de los tres segmentos de mercado (sílicio personalizado, plataformas GPU, API-first) y mapa de cada proveedor a un segmento.
  China:                                                                                                                                                                                                                                                              
- Explica por qué el modelo de precios de la API "por token" se comprime hacia la curva de costos del motor de servicio, no la del hardware.
  Traducción: explica por qué "según token" API 定价模型 se comprime a la curva de costos del motor de servicio y no a los costos de hardware.
- Calcule el costo efectivo por solicitud en al menos tres proveedores y explique cuándo el precio por minuto (Baseten, Modal) supera el precio por token.
  China: 計算至少三供应商的每次请求有效成本,并解释按分钟 (Baseña, Modal)何时优于按代币 (Baseña, Modal)
- Identificar qué plataforma es la opción predeterminada para una carga de trabajo determinada (desbordador sin servidor, alta potencia constante, variantes ajustadas, multimodal).
  China: 识别哪个平台是给定工作负载的正确默认选择(无服务器突发、稳定高吞吐、微调变体、多模态)

## El problema es la introducción del problema

Usted evaluó las plataformas de hiperescalado administradas. Usted decidió que necesita un proveedor más estrecho y más rápido  Fuegos artificiales para la latencia, juntos para la amplitud, Baseten para un modelo personalizado afinado. Ahora usted tiene seis opciones reales y las páginas de precios no se alinean. Fuegos artificiales muestra $/M tokens; Baseten shows $/minuto; Muestras de moda$/second; Replicate shows $No se pueden comparar cara a cara sin modelar la carga de trabajo.

> Después de evaluar la plataforma de administración, decidiste que necesitas un proveedor más especializado, más rápido, que busque retrasos, juntos, que busque amplitud, que busque modelos de auto-definición, ahora tienes seis opciones reales, pero la página de precios no puede compararse directamente.$/M tokens；Baseten 显示 $/分钟; Modal 显示 $/秒；Replicate 显示 $/预测──不建模工作负载就无法直接比较──

Peor aún, el modelo de negocio detrás de cada página de precios es diferente. Los fuegos artificiales ejecutan su propio motor personalizado (FireAttention) en GPU compartidas; la tasa por token refleja su curva de utilización. Baseten le da GPUs dedicadas Truss +; por minuto refleja exclusividad. Modal es verdadero Python sin servidor  por segundo de facturación con subsegundo comienzos en frío. La misma salida (una respuesta de LLM), tres funciones de coste diferentes.

> Lo peor es que cada página de fijación tiene un modelo de negocio diferente. Fireworks en GPU compartida opera en su propio motor de desarrollo. FireAttention.

Esta lección muestra a los seis y te dice cuándo ganan cada uno.

> Este curso tiene seis plataformas, te digo cada uno en qué momento se gana.

> **【中文解读】**推理平台市场的核心难题是定价模型不统一――按代币 计费(Fireworks/Together) 按分钟计费(Baseten) 按秒计费(Modal) 按预测计费(Replicate)  响应,背后是完全不同的成本函数──不能只看单价,必须根据工作负载特征建模才能做出正确的选择──

> **【拓展：LLM 推理成本构成】**El coste de la LLM 推理主要由GPU 租(H100 约 $2-3/hr）、电力（约 $La tasa de interés total de la plataforma de recomendación suele estar en el 20-40% (a16z 2025  Infraestructura de Inteligencia Artificial)  La clave para optimizar el costo de la recomendación es mejorar la tasa de utilización de la GPU y el lote de gran tamaño vLLM de lotes continuos.

## El concepto central.

> **【中文解读】**推理平台市场分为三大细分:(1) 自研芯片(Groq LPU、Cerebras WSE、SambaNova RDU) 以 5-10x 解码速度取胜但单价更高;(2) GPU 平台(Baseten、Together、Fireworks、Modal) 运行NVIDIA GPU,介于原始 GPU 租和超级级托管服务之间;(3) API 优先市场(Replicate、DeepInfra、OpenRouter) 强调快速手和广度──

> **【拓展：自研推理芯片竞赛】**Groq's LPU(Language Processing Unit) en Llama 70B puede realizar 300+ tokens/s, es 10x de GPU 推理的. Cerebras' CS-3 晶圆级引擎可达 2000+ tokens/s. Pero la debilidad de estos chips es que la flexibilidad es baja  sólo puede funcionar en modelos de estructura específica.

### Los tres segmentos

**Custom silicon** Groq (LPU), Cerebras (WSE), SambaNova (RDU). Típicamente 5-10 veces más rápido que un cluster basado en GPU en el mismo modelo. Precio por token más alto (Groq fue ~ $ 0.99 / M en Llama-70B a finales de 2025) pero inmejorable para casos de uso sensibles a la latencia. Groq es la elección de producción para agentes de voz y traducción en tiempo real.

> **自研芯片** Groq(LPU)、Cerebras(WSE)、SambaNova(RDU)。 Normalmente comparable al modelo de GPU 集群解码速度快 5-10 倍──按代币 价格更高(Groq 2025 年末在 Llama-70B 上约 $0.99/M), pero en el caso de la capacidad de uso sensible a la demora no hay rivalidad──Groq es el representante de la producción y la selección de la traducción real.

**GPU platforms** Baseten, Together, Fireworks, Modal, Anyscale. Se ejecuta en NVIDIA (H100, H200, B200 en 2026) o a veces AMD. La capa económica entre "arrendamiento de GPU crudo" (RunPod, Lambda) y "servicio administrado hipercaler" (Bedrock).

> **GPU 平台** Baseten、Together、Fireworks、Modal、Anyscale──运行在 NVIDIA(2026 años H100、H200、B200) o有时是 AMD 上──"original GPU 租"(RunPod、Lambda) y"云托管服务"(Bedrock) entre la economía层──

**API-first marketplaces** Replicar, DeepInfra, OpenRouter, Fal. Catálogo amplio, pago por predicción o pago por segundo, enfatizar el tiempo de la primera llamada.

> **API 优先市场** Replicar 、DeepInfra、OpenRouter、Fal。 amplio catálogo, según el pronóstico o según el segundo, enfatizar la velocidad de la primera modificación。

### Fuegos artificiales  plataforma de GPU optimizada para la latencia

- Motor FireAttention (custom); comercializado como 4 veces menor latencia que vLLM en configuraciones equivalentes.
  China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China:
- Lugar de lote en ~50% de tasa sin servidor para cargas de trabajo no interactivas.
  China: por lo que se refiere a las tasas de carga de carga de carga de carga de carga de carga de carga de carga de carga de carga de carga de carga de carga de carga de carga de carga de carga de carga de carga de carga de carga de carga de carga de carga de carga de carga de carga de carga de carga de carga de carga de carga de carga de carga de carga de carga de carga de carga de carga de carga de carga de carga de carga de carga de carga de carga de carga de carga de carga de carga de carga de carga de carga de carga de carga de carga de carga de carga de carga de carga de carga de carga de carga de carga de carga de carga de carga de carga de carga de carga de carga de carga de carga de carga de carga de carga de carga de carga de carga de carga de carga de carga de carga de carga de carga de carga de carga de carga de carga de carga de carga de carga de carga de carga de carga de carga de carga de carga de carga de carga de carga de carga de carga de carga de carga de carga de carga de carga de carga de carga de carga de carga de carga de carga de carga de carga de carga de carga de carga de carga de carga de carga de carga de carga de carga de carga de carga de carga de carga de carga de carga de carga de carga de carga de carga de carga de carga de carga de carga de carga de carga de carga de carga de carga de carga de carga de carga de carga de carga de carga de carga de carga de carga de carga de carga de carga de carga de carga de carga de carga de carga de carga de carga de carga de carga de carga de carga de carga de carga de carga de carga de carga de carga de carga de carga de carga de carga de carga de carga de carga de carga de carga de carga de carga de carga de carga de carga de carga de carga de carga de carga de carga de carga de carga de carga de carga de carga de carga de carga de carga de carga de carga de carga de carga de carga de carga de carga de carga de carga de carga de carga de carga de carga de carga de carga de carga de carga de carga de carga de carga de carga de carga de carga de carga de carga de carga de carga de carga de carga de carga de carga de carga de carga de carga de carga de carga de carga de carga de carga de carga de carga de carga de carga de carga de carga de carga de carga de carga de carga de
- El modelo ajustado sirve al mismo ritmo que el modelo base  un diferenciador real frente a los proveedores que cobran una prima por su LoRA.
  La diferenciación real entre los modelos de base y los proveedores que cobran los prefijos de la LORA es el factor de diferenciación.
- Mediados de 2026: aumento del alquiler de GPU bajo demanda de $1/hora a partir del 1 de mayo de 2026.
  China 翻译:2026 年中:自 5 月 1 日起按量 GPU 租价 $1/小时──大批量价格可协商──
- Señal financiero: valoración de $ 4B, 10T + tokens / día manejados.
  China: $4B 估值,每日处理 10T+ token──

### Juntos  amplitud optimizada

- 200+ modelos, incluidos los lanzamientos de código abierto dentro de los días siguientes a la publicación en línea.
  中文翻译:200+ 模型, incluida la versión abierta de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión.
- 50-70% más barato que Replicate en modelos LLM equivalentes  el posicionamiento de "AI Native Cloud" es volumen y catálogo.
  En el modelo de LLM, el modelo de RPL es de un costo de 50 a 70%.
- Inferencia + ajuste fino + capacitación en una API.
  Traducción:Tú理 + 微调 + 训练在一个API 中。

### Baseten  optimizado para empresas

- Marco de la Truss: envases de modelos con dependencias, secretos, servidores config en un manifiesto.
  En inglés, el código de confianza es el código de código de confianza.
- GPU de T4 a B200. facturación por minuto con una mitigación razonable de arranque en frío.
  China  GPU  Rango de T4 a B200 ⋅ por minuto ⋅ cuota de tiempo, hay razonable de frío de inicio de la reducción ⋅
- SOC 2 Tipo II, HIPAA-pronto.
  El gobierno de la República de China ha aprobado la ley de salud de la República de China.
- $5B valuation, January 2026 Series E ($300 millones de dólares de CapitalG, IVP, NVIDIA).
  En inglés:$5B 估值，2026 年 1 月 E 轮融资（来自 CapitalG、IVP、NVIDIA 的 $300M) ⋅

### Modal  Python nativo optimizado

- Infraestructura como código en Python puro. Decorar una función con `@modal.function(gpu="A100")`y desplegar con un solo comando.
  La infraestructura de Python es el código.`@modal.function(gpu="A100")`装饰函数,一条命令部署。
- El frío comienza en 2-4 segundos con precalentamiento; < 1s para modelos pequeños.
  En español: por segundo. Pre-calor.
- $87M Series B at $1.1B valoración (2025). La mejor puntuación de experiencia de los desarrolladores en encuestas independientes.
  La economía de la región se ha convertido en una economía de mercado.$87M，估值 $1.1B(2025)。 independent survey中开发者体验评分最高。

### Replicación  ancho multimodal

- Pagos por predicción. La plataforma predeterminada para modelos de imágenes, video y audio.
  Traducción:Página de acuerdo con el modelo de imágenes, vídeos y sonidos.
- Ecosistema de integración (Zapier, Vercel, plugins CMS).
  En el contexto de la actualidad, el sistema de gestión de datos de la empresa es un sistema de gestión de datos de datos de la empresa.
- Menos competitivo en las tasas de LLM por token, pero gana en la variedad multimodal.
  La competencia de los LLM es más baja, pero se gana en la diversidad de los modelos.

### En cualquier escala  Radial nativo

- Construido en Ray; RayTurbo es el motor de inferencia patentado de Anyscale (competir con vLLM).
  La versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión de la versión original de la versión original de la versión de la versión original de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión
- Lo mejor para cargas de trabajo distribuidas de Python donde el paso de inferencia es un nodo en un gráfico más grande.
  China 工作负载: Piython 工作负载 工作负载 工作负载
- Gestionó los racimos de Ray; integración estrecha con Ray AIR y Ray Serve.
  Traducción:Total de Rays; Rápido y Rápido

### Por token versus por minuto  cuando cada uno gana

Per-token tiene sentido cuando la carga de trabajo es insensible a la latencia y estallar  sólo paga por lo que usa. Por minuto tiene sentido cuando la utilización es alta y predecible  se supera por-token una vez que está saturando la GPU.

> Cuando la carga de trabajo es poco sensible a la demora y se produce, el costo de la señal es más razonable. Cuando la tasa de utilización es alta y predecible, el costo de la señal es más razonable.

Regla dura: para cargas de trabajo superiores al 30% de utilización sostenida de una GPU dedicada, por minuto (Baseten, Modal) comienza a superar por token (Fireworks, Together).

> 粗略规则: Para la GPU especial 持续利用率 超过约30%的工作负载,按分钟(Baseten、Modal)开始优于按代币(Fireworks、Together) ∼低于此价值时,按代币 获胜,因为避免为空付费──

> **【中文解读】**El núcleo de la selección de modelos de precio fijo es la tasa de utilización. Por token el costo de la operación se adapta a la situación de alta carga y el precio de la operación se adapta a la situación de alta carga continua.

> **【拓展：推理经济学趋势】**El costo de la evaluación de los modelos de nivel 4 de la GPT a partir de 2023 se redujo en un 90% en el período 2024-2026$30/M tokens 降到 2025 年的 $Los tokens de 3/M, las tendencias que impulsan la evolución de la tecnología son: modelos de cuantificación, int8/int4  mejor lote, la regulación, la competencia de los chips y la apertura de los motores de cálculo, vLLM/SGLang)  la madurez de los modelos.

### El motor personalizado es el verdadero foso

Cada plataforma que se encuentra por encima de vLLM y SGLang reclama un motor personalizado. FireAttention, RayTurbo, la pila de inferencias de Baseten.

> Cada plataforma que supera a la VLLM y SGLang afirma tener un motor de desarrollo propio. FireAttention, RayTurbo, Baseten, .

### Números que debes recordar

- Alquiler de GPU de fuegos artificiales: $1/hora de aumento a partir del 1 de mayo de 2026.
  Fuego de trabajo GPU 租:自 2026 年 5 月 1 日起价 $1/小时。
- Reclamo de fuegos artificiales: 4 veces menor latencia que vLLM en configuraciones equivalentes.
  El fuego de la ciudad de Nueva York fue destruido por el incendio de la ciudad de Nueva York.
- En conjunto: 50-70% más barato que Replicate en LLM.
  En el caso de los estudiantes de la Universidad de San Francisco, el número de estudiantes de la Universidad de San Francisco es de 50 a 70%.
- Valoración de base: $5B (Series E, Jan 2026, $300M de ronda).
  El precio de la venta de la propiedad de la empresa es el precio de la venta de la propiedad.$5B（E 轮，2026 年 1 月，$300M 轮次)
- Valoración de los activos: $1.1B (Sería B, 2025).
  La evaluación de los modelos: $1.1B (B轮,2025)
- Los ritmos por minuto por token por encima de ~ 30% de utilización sostenida.
  China: la tasa de utilización continua supera aproximadamente el 30% 时分钟优于代币──

## Usalo con el marco de ejecución
```figure
cost-per-token
```

## Usalo

`code/main.py`Comparación de los seis proveedores en una carga de trabajo sintética en los modelos de precios.$/day and effective $- M tokens. Ejecutarlo para encontrar el equilibrio entre por token y por minuto.

> `code/main.py`En el informe, se comparó el modelo de fijación de precios de seis proveedores en la carga de trabajo sintética.$/天和等效 $/M tokens──运行它找到按代币 和按分钟的亏平点──

> **【中文解读】**實踐部分通過模拟工作負荷對比六供應商的定價模型──關鍵输出是每日成本$/day）和等效每百万 token 成本（$/M tokens), ayudarte a encontrar el punto de intersección según el token y según el minuto de cuotación.

## Envíe el producto .

Esta lección produce`outputs/skill-inference-platform-picker.md`. Dado el perfil de carga de trabajo, SLA y presupuesto, elige la plataforma de inferencia principal y nombra al segundo.

> 本课产 出  `outputs/skill-inference-platform-picker.md` asignar la carga de trabajo, la asignación de servicios y el presupuesto, seleccionar la plataforma de evaluación y la designación de los servicios.

> **【拓展：推理平台选型决策树】**选型决策路径:(1) 是否需要 < 50ms TTFT? 是 → Groq/Cerebras;(2) 是否需要自托管/合规? 是 → Baseten/Modal;(3) 是否需要最大模型广度? 是 → Together/OpenRouter;(4) 是否需要多媒体模型? 是 → Replicate/Fal;(5) 默认 → Fireworks(延迟优化) or Together(成本优化)

## Los ejercicios.

1. - ¿ Qué ?`code/main.py`¿En qué uso sostenido Baseten (por minuto) supera a Fireworks (por token) para un modelo 70B en un H100?
   Traducción:运行`code/main.py`◊ Baseten (en inglés) ⋅ por minuto) ⋅ en qué se mantiene el uso de la tecnología en el mercado de la información sobre la información sobre la información sobre la información sobre la información sobre la información sobre la información sobre la información sobre la información sobre la información sobre la información sobre la información sobre la información sobre la información sobre la información sobre la información sobre la información sobre la información sobre la información sobre la información sobre la información sobre la información sobre la información sobre la información sobre la información sobre la información sobre la información sobre la información sobre la información sobre la información sobre la información sobre la información sobre la información sobre la información sobre la información sobre la información sobre la información sobre la información sobre la información sobre la información sobre la información sobre la información sobre la información sobre la información sobre la información sobre la información sobre la información sobre la información sobre la información sobre la información sobre la información sobre la información sobre la información sobre la información sobre la información sobre la información sobre la información sobre la información sobre la información sobre la información sobre la información sobre la información sobre la información sobre la información sobre la información sobre la información sobre la información sobre la información sobre la información sobre la información sobre la información sobre la información sobre la información sobre la información sobre la información sobre la información sobre la información sobre la información sobre la información sobre la información sobre la información sobre la información sobre la información sobre la información sobre la información sobre la información sobre la información sobre la información sobre la información sobre la información sobre la información sobre la información sobre la información sobre la información sobre la información sobre la información sobre la información sobre la información sobre la información sobre la información sobre la información sobre la información sobre la información sobre la información sobre la información sobre la cuento.
2. Su producto sirve para la generación de imágenes más chat más habla-texto.
   Su producto ofrece imágenes de generación, conversación y lenguaje de transcripción.
3. Los fuegos artificiales aumentan los precios en $1/hora en su modelo principal. Modela el impacto de costos combinados si el 40% de su tráfico se mueve a la categoría de lote (50% de descuento).
   El proyecto de incendios será el principal modelo  precio $1/小时── si el 40% del tráfico se transfiere a la categoría de la cantidad  mitad de precio, construir 
4. Un cliente regulado requiere GPUs SOC 2 Tipo II + HIPAA + dedicadas. ¿Cuáles de las tres plataformas son viables y cuál gana en FinOps?
   Un cliente bajo supervisión necesita SOC 2 Tipo II + HIPAA + GPU especial. ¿Cuál de las tres plataformas está disponible?
5. Comparar el costo por 1.000 predicciones para Llama 3.1 70B en Fireworks sin servidor, juntos a pedido, Baseten dedicado y Replicate API. ¿Cuál es más barato a 10 predicciones por día? a 10.000?
   En inglés, el uso de las aplicaciones de fireworks es más fácil y más costoso.

## Términos clave .

| Term | What people say | What it actually means | 中文释义 |
|------|----------------|------------------------|----------|
| Custom silicon | "non-GPU chips" | Groq LPU, Cerebras WSE, SambaNova RDU — optimized for decode | 自研推理芯片——Groq LPU、Cerebras WSE 等 |
| FireAttention | "Fireworks engine" | Custom attention kernel; marketed at 4x lower latency than vLLM | Fireworks 自研注意力引擎，号称比 vLLM 快 4x |
| Truss | "Baseten's format" | Model packaging manifest; dependencies + secrets + serving config | Baseten 的模型打包格式，包含依赖、密钥、服务配置 |
| Per-token | "API pricing" | Charge by tokens consumed; pay for no idle | 按 token 计费——只付实际使用量 |
| Per-minute | "dedicated pricing" | Charge by wall-clock GPU time; wins at high utilization | 按分钟计费——高利用率时更划算 |
| Per-prediction | "Replicate pricing" | Charge per model invocation; common for image/video | 按预测次数计费——常见于图像/视频模型 |
| RayTurbo | "Anyscale engine" | Proprietary inference on Ray; competes with vLLM on Ray clusters | Anyscale 基于 Ray 的自研推理引擎 |
| Batch tier | "50% off" | Non-interactive queue at reduced rate; common on Fireworks, OpenAI | 批量推理队列——半价用于非交互任务 |
| Fine-tuned at base rate | "Fireworks LoRA" | Charge LoRA-served requests at base model's rate (differentiator) | 微调模型按基础模型费率计费 |

## Más Leer más Leer más

- [Fireworks Pricing](https://fireworks.ai/pricing) Tarifas por token, nivel de lote, alquiler de GPU.
- [Baseten Pricing](https://www.baseten.co/pricing/) tasas por minuto, capacidad comprometida, niveles de empresa.
- [Modal Pricing](https://modal.com/pricing) velocidades de GPU por segundo y nivel libre.
- [Together AI Pricing](https://www.together.ai/pricing) catálogo de modelos y tarifas por token.
- [Anyscale Pricing](https://www.anyscale.com/pricing) RayTurbo y gestionó el precio de Ray.
- [Northflank — Fireworks AI Alternatives](https://northflank.com/blog/7-best-fireworks-ai-alternatives-for-inference) evaluación comparativa.
- [Infrabase — AI Inference API Providers 2026](https://infrabase.ai/blog/ai-inference-api-providers-compared) paisaje de vendedores.
