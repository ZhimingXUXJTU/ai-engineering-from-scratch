# Comprensión de video largo en el contexto de millones de tokens.

> Un video 4K de 1 hora a 24 FPS, parcheado e incrustado, produce el orden de 60 millones de tokens. Un episodio de podcast de 2 horas transcrito es de 30.000 tokens. Una película completa de Blu-ray, incluso comprimida con un agresivamente combinado, es de cientos de miles de tokens. Gemini 1.5 de Google (marzo 2024) abrió esta era con un contexto de 10 millones de tokens, haciendo una recuperación confiable de agujas en un haystack durante videos de una hora. LWM (Liu et al., febrero 2024) mostró la trayectoria de escala de la atención anilla. LongVILA y Video- XL aumentaron aún más la ingestión. VideoAgent cambió el contexto crudo por la recuperación de agentes. Cada enfoque es un cambio diferente en la composición, el recuerdo y la complejidad de la ingeniería. Esta lección las lee lado a lado.

> **【中文解读】**1 小时 4K 视频可产生约6000.000 tokens,远超任何模型的上下文窗口──处理长视频有三条路径:(1) 暴力上下文(Gemini 1.5 的千万 token 上下文);(2) Ring Attention 跨设备分布式注意力;(3) Token 压缩(Video-XL 摘要);(4) 代码检查 代码检查 代码检查 代码检查 代码检查 代码检查 代码检查 代码检查 代码检查 代码检查 代码检查 代码检查 代码检查 代码检查 代码检查 代码检查 代码检查 代码检查 代码检查 代码检查 代码检查 代码检查 代码检查 代码检查 代码检查 代码检查 代码检查 代码检查 代码检查 代码检查 代码检查 代码检查 代码检查 代码检查 代码检查 代码检查 代码检查 代码检查 代码检查 代码检查 代码检查 代码检查 代码检查 代码检查 代码检查 代码检查 代码检查 代码检查 代码检查 代码检查 代码

**Type:** Build | **类型:** 构建
**Languages:** Python (stdlib, needle-in-haystack simulator + agentic-retrieval router) | **语言:** Python（标准库，大海捞针模拟器 + Agent 检索路由器）
**Prerequisites:** Phase 12 · 17 (video temporal tokens) | **前置知识:** Phase 12 · 17（视频时间 token）
**Time:** ~180 minutes | **时间:** ~180 分钟

> ¿ Qué es esto ?**【前置】**学本节前请先掌握:Fase 12·17(vídeo tiempo token 与采样);Fase 10·34(Anillo de atención distribuida atención);Fase 14(Agente 检索,VideoAgent思路)。本节是长视频理解的极限挑战:百万代币 上下文。
> ¿ Qué es esto ?**【类比】**长视频理解 = "看完整部电影后能回答细节"──三种策略:(1) Gemini 1.5 路线 = Colocar toda la película en el cerebro(10M token 上下文,硬件怪兽);(2) Video-XL 路线 = 看完写摘要+检索原始片段(token 压缩);(3) VideoAgent 路线 = 当数据库查,问题导向地拉取相关段段(Agent 检索) ~~第一条最优雅但最贵,第三条最便宜但最复杂──

## Objetivos de aprendizaje

- Calcule el recuento total de tokens visuales para el vídeo de formato largo a diferentes FPS y pooling.
  Traducción: calcular diferentes FPS 和池化配置 下长视频的视觉代币 总数──
- Explica las tres vías de escala: contexto bruto (Gemini 1.5), atención a anillos (LWM), compresión de tokens (LongVILA / Video-XL).
  La historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la historia de la China.
- Comparar VLMs de video de contexto crudo con VLMs de video de recuperación de agentes (VideoAgent) en precisión y latencia.
  China Translation: Comparar original on 下文视频 VLM 和 Agent 检索视频 VLM(VideoAgent) en el índice de precisión y retraso de la actuación.
- Diseñar una prueba de aguja en un manto de heno para un video de 30 minutos y medir el recuerdo en un minuto específico.
  Traducción: para 30 minutos de video diseño de gran mararraje de prueba y medida de la frecuencia de llamada de un minuto específico.

## El problema es la introducción del problema

Un solo marco de parches de tamaño Qwen2.5VL con 384 resoluciones nativas es de ~729 tokens. En 3x3 pooling eso es de 81 tokens por marco. Un clip de 30 minutos a 1 FPS = 1800 frames = 145,800 tokens.

> Qwen2.5-VL Ҙа小的补丁 在 384 原生分辨率下每约729 token──3x3 池化后每 81 token──30 分钟片段 1 FPS = 1800  = 145,800 token,2025年开放 VLM 可处理但紧张──2 FPS 下 291,600 token只有最大上文才能容纳──

Una película de 2 horas a 1 FPS es de 583k tokens. Más allá de la mayoría de los modelos abiertos de 2026; requiere Gemini 2.5 Pro o un pooling más agresivo.

> 2 小时电影 1 FPS es un token de 583k. Más de 2026 años la mayoría de los modelos abiertos tienen capacidad; necesita Gemini 2.5 Pro o más activado de la acumulación.

Surgieron tres caminos de escala.

> Se ha desarrollado un camino de expansión.

## El concepto central.

> **【中文解读】**长视频理解(百万代币 级别) es el reto de la AI de varios modelos. ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙                                                                                                                                                                                                                                                             

> **【拓展：Gemini 1.5 Pro 的百万 token 上下文**Gemini 1.5 Pro  soporte 1M token 输入, puede procesar aproximadamente 1 hora de vídeo o 1000+ páginas de documentos。 a través de poca atención(solo se concentra en los relacionados) y el procesamiento de bloques realizados。 en la misión de QA de largo vídeo, la precisión de Gemini 1.5 Pro disminuye más lentamente con la longitud del vídeo, pero todavía hay una diferencia significativa con los humanos。


### Caminado 1: Contexto bruto (Gemini 1.5, Claude Opus)

Arrojar hardware al problema, escalar el contexto a millones de tokens, procesar todo en un solo pase hacia adelante.

> Usar hardware violencia resolver problemas.

Gemini 1.5 Pro lanzado con 1M tokens; Gemini 1.5 Ultra a 10M; Gemini 2.5 Pro en 2026 hace horas de video confiablemente. El papel (arXiv:2403.05530) documenta la recuperación de aguja en un haystack en un 99,7% hasta ~ 9,5M tokens.

> Gemini 1.5 Pro con 1M token  lanzado; Gemini 1.5 Ultra  expandido a 10M; Gemini 2.5 Pro en 2026 puede ser procesado con confianza en el número de horas de vídeo ⋅ en el artículo se registró una tasa de recuperación de 99.7% de las grandes agujas en el rango de 9.5M token ⋅ en el rango de 9.5M token ⋅ en el año 2026.

Ingeniería: una implementación de atención personalizada con jerarquía de memoria (local + global + escaso) más enrutamiento experto de MoE para la eficiencia de largo contexto. No se publicó en detalle completo. No es de código abierto.

> 工程实现: auto-definir mecanismo de atención,带有内存层次(局部+全局+稀疏),加上 MoE 专家路由提升长上下文效率──未完整公开──非开源──

### Caminado 2: Atención a los anillos (LWM, LongVILA)

La atención en el anillo distribuye largas secuencias entre dispositivos en un "anillo" donde cada dispositivo tiene un pedazo.

> **【中文解读】**Ring Attention distribuirá la larga secuencia en varios dispositivos, cada dispositivo tiene un bloque de secuencia, a través de la comunicación de circunferencia calcular la atención de la totalidad.

LWM (Liu et al., 2024) entrenó un modelo de contexto de 1M-token de esta manera.

> LWM(Liu 等人,2024) con este método entrenó 1M token 上下文模型── entrenar el cálculo de la cantidad con el aumento de la línea de abajo y no de la segunda parte de la atención se distribuye a los dispositivos de circunferencia──

LongVILA (arXiv:2408.10188) adaptó el patrón a VLMs. 1400-frame videos a 192 tokens por fotograma = 268k contexto, entrenado con la atención del anillo a través del paralelismo de 8 vías.

> LongVILA adaptará este modelo a VLM──1400 视频, por cada token 192 = 268k 上下文, a través de 8 路并行环形注意力训练──

### Camino 3: Compresión de tokens (Video-XL, LongVA)

Más barato que el contexto bruto: comprimir agresivamente antes de que el LLM vea la secuencia.

> Más barato: en el LLM se realiza la aceleración de la compresión antes de la secuencia.

Video-XL (arXiv:2409.14485) utiliza un token de resumen visual: cada clip de los cuadros N produce un solo token de "resumen" que se encuentra sobre el N. En la inferencia, el LLM ve un token de resumen por clip, reduciendo drásticamente el contexto.

> Video-XL Uso de vídeo resumen token: cada N 片段 generar un "resumen" token, hacer atención sobre el N  hacer atención en la recomendación MLL Cada fragmento sólo ve un resumen token, reducido considerablemente en la siguiente.

LongVA amplía el contexto de LLM de 200 mil a 2 millones con una técnica de "transferencia de contexto largo".

> LongVA utiliza la técnica de "长上下文迁移" para LLM 上下文 de 200k 扩展到2M── en el entrenamiento en el texto de la larga, a través del intercambio de mensajes de migración a la larga.

La compresión de tokens se trata de un retiro en marcas de tiempo específicas para la escalabilidad.

> El precio de la recetación de los tokens se reduce a un precio de expansión a un precio de tiempo determinado.

### Camino 4: Recuperación de agentes (VideoAgent)

No entregue el vídeo completo al LLM. En su lugar, trate el vídeo como una base de datos y use un LLM para consultarlo.

> No lo pongas todo en el vídeo para LLM.

VideoAgent (arXiv:2403.10517):

> VideoAgent ((arXiv:2403.10517):

1. El LLM lee la pregunta.
   > LLM 读取问题──
2. El LLM pide una herramienta de recuperación de clips relevantes ("mírame segmentos con un gato").
   > LLM 调用检索工具获取相关片段("给我看有猫的片段")
3. La herramienta devuelve las marcas de tiempo de los clip.
   > 工具返回匹配的片段时间──
4. LLM lee esos clips a través de un VLM.
   > LLM 通过VLM 读取这些片段──
5. El LLM compone la respuesta o hace preguntas de seguimiento.
   > LLM: Respuesta o encuesta posterior.

Este es el patrón de LLM-as-agent aplicado a los vídeos largos.

> Es el caso de la aplicación de la LLM como agente en el largo de la serie.

### Indicadores de referencia de agujas en un manto de heno

La prueba estándar de largo contexto: insertar un marcador visual o textual único en un punto aleatorio del video, luego hacer una consulta que requiera su recuerdo.

> 标准长上下文测试: en el video, inserta un marcado único de la imagen o del texto en cualquier lugar, y luego presenta una consulta sobre la necesidad de recordar ese marcado.

Metrícula: Recall@k a través de la longitud del vídeo y la posición del marcador.

> Indicador:跨视频长度和标记位置的 Recall@k。

Gemini 2.5 Pro obtiene un puntaje de >99% de recuerdo en videos de hasta 90 minutos. Los modelos abiertos 72B (Qwen2.5-VL-72B, InternVL3-78B) obtienen un puntaje de ~85-90% a los 30 minutos y se degradan más allá de 60.

> Gemini 2.5 Pro en 90 minutos de duración Rate de retorno >99%──Open 72B 模型(Qwen2.5-VL-72B、InternVL3-78B) en 30 minutos de duración alrededor de 85-90%, 60 minutos de retorno posterior―

VideoAgent puede igualar o superar los modelos de contexto crudo en 2 horas porque la recuperación golpea la aguja si la herramienta es buena.

> VideoAgent puede ser combinado o superado en el modelo original de vídeo de más de 2 horas, ya que siempre que la herramienta sea buena, la búsqueda puede tener un objetivo.

### ¿Qué camino elegir?

Para un clip de 15 minutos con precisión fronteriza: abre 72B + contexto nativo generalmente funciona.

> 15 分片段追求前沿准确率: 开放 72B + 原生上下文通常可行──选 Qwen2.5-VL-72B──

Para el contenido de 30 minutos a 1 hora: LongVILA o Video-XL para abierto; Gemini 2.5 Pro para cerrado. La barra de calidad importa  la frontera se cierra.

> 30 minutos a 1 hora contenido: abierto con LongVILA o Video-XL; abierto con Gemini 2.5 Pro;; calidad de entrada  es importante

Para contenido de más de 2 horas: VideoAgent o patrones de recuperación similares.

> 2 小时以上内容:VideoAgent o similar en busca de modo modo.

### Modelo de producción 2026

En la práctica, las líneas de producción de video largo son híbridas:

> En la práctica, la producción de vídeos es un programa mixto:

1. ejecuta muestreo dinámico de FPS + agregación agresiva en todo el video (obtenga una representación global de 100k tokens).
   China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China:
2. Pasen a un 72B VLM para un resumen global.
   En el caso de los viajeros, el número de viajeros es de 72B.
3. Si el usuario hace preguntas detalladas, ejecuta la recuperación agencial utilizando el resumen como índice.
   Si el usuario pregunta detalles, utiliza el resumen como índice de funcionamiento del agente 检索。

Esto combina el contexto bruto para la comprensión global y la recuperación de detalles locales.

> Esto combina la capacidad de comprensión general y detalle local de la violencia en el contexto siguiente.

## Usalo con el marco de ejecución
```figure
mm-video-token-budget
```

## Usalo

`code/main.py`¿Qué es esto ?

- Computa los presupuestos de tokens para videos de 1 minuto a 3 horas en diferentes FPS + pooling.
  El tiempo de la película es de 5 minutos y el tiempo de la película es de 5 minutos.
- Simula una carrera de aguja en un montón de heno: inyecta un marcador en una marca de tiempo aleatoria, hace una pregunta, recuerda el resultado.
  En el tiempo que se desee, se puede hacer un examen de la etiqueta, la pregunta, la evaluación y la receta.
- Incluye un simulador de enrutamiento de recuperación de agentes que selecciona clips específicos para alimentar a un VLM aguas abajo.
  En inglés, el nombre de la persona que se encuentra en el sitio web de la compañía es el nombre de la persona que se encuentra en el sitio web.

Echa un vistazo a la tabla de presupuesto y siente la brecha de la escala.

> 运行预算表,感受规模差距──

## Envíe el producto .

Esta lección produce`outputs/skill-long-video-strategy-planner.md`. Dada la duración del video y la complejidad de la consulta, elige entre el contexto bruto, la compresión y la recuperación agencial, y calcula las expectativas de latencia + calidad.

> 本课产 出  `outputs/skill-long-video-strategy-planner.md` Dado el tiempo de la película y la complejidad de la consulta, se opta por la violencia en la información, la compresión y el proceso de selección de agentes, y se calcula la demora + el pronóstico de calidad.

## Los ejercicios.

1. Una conferencia de 45 minutos a 1 FPS, 81 tokens por fotograma. total de tokens? ¿Se ajusta en qué contextos de los modelos? 45 分钟讲座,1 FPS, cada 1 81 token──总代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代

2. Diseñar una prueba de aguja en un haystack: en qué minuto inyectas el marcador, y cuál es el formato exacto de la consulta?

3. Comparar el contexto bruto Qwen2.5-VL-72B (contexto 80k) con VideoAgent (Claude 3.5 + recuperación) en un video de 1 hora. ¿Qué gana en el recuerdo? ¿Qué gana en la latencia?

4. El costo de memoria de la atención de anillo se escala linealmente en longitud de secuencia y linealmente en el número de dispositivos. Explica por qué y qué falla si se deja caer la fase de rotación de anillo.

5. Leer Gemini 1.5 Sección 5 sobre aguja en un haystack. ¿Qué encontró el periódico sobre el recuerdo en el límite de token 1M vs 10M?

## Términos clave .

| Term | What people say | What it actually means | 中文释义 |
|------|-----------------|------------------------|---------|
| Brute context | "Just more tokens" 暴力上下文 | Scale LLM context to millions of tokens; process everything in one pass 将 LLM 上下文扩展到百万 token，一次前向传播处理全部内容 | |
| Ring attention | "LWM-style parallel" 环形注意力 | Distributed attention pattern where each device holds a chunk and rotates 分布式注意力模式，每个设备持有一块并在环中轮转 | |
| Token compression | "Summary tokens" 摘要 token | Reduce per-clip tokens via a learned compressor before the LLM LLM 前通过学习型压缩器减少每片段 token 数 | |
| Needle-in-haystack | "NIH test" 大海捞针测试 | Insert a unique marker at a random point, ask model to recall it at test time 在随机位置插入唯一标记，测试时要求模型回忆 | |
| Agentic retrieval | "LLM as query planner" Agent 检索 | LLM asks a retrieval tool for relevant clips, reads them via a VLM, composes answer LLM 调用检索工具获取相关片段，通过 VLM 阅读并生成回答 | |
| VideoAgent | "Retrieval pattern for video" 视频检索模式 | Canonical agentic-retrieval design: question -> tool -> clip -> answer 经典 Agent 检索设计：问题→工具→片段→回答 | |

## Más Leer más Leer más

- [Gemini Team — Gemini 1.5 (arXiv:2403.05530)](https://arxiv.org/abs/2403.05530)
- [Liu et al. — LWM / RingAttention (arXiv:2402.08268)](https://arxiv.org/abs/2402.08268)
- [Xue et al. — LongVILA (arXiv:2408.10188)](https://arxiv.org/abs/2408.10188)
- [Shu et al. — Video-XL (arXiv:2409.14485)](https://arxiv.org/abs/2409.14485)
- [Wang et al. — VideoAgent (arXiv:2403.10517)](https://arxiv.org/abs/2403.10517)
