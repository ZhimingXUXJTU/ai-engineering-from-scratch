# Janus-Pro: Desacoplados codificadores para modelos multimodal unificados

> Los modelos multimodal unificados tienen una tensión inevitable. La comprensión necesita características semánticas  SigLIP o DINOv2 vectores de salida ricos en información de nivel de concepto. La generación quiere códigos amigables con la reconstrucción. Tokens VQ que componen de nuevo en píxeles nítidos. Los dos objetivos no son compatibles en un solo codificador. Janus (DeepSeek, octubre 2024) y Janus-Pro (DeepSeek, enero 2025) argumentan que la solución es dejar de intentar: desacoplar los dos codificadores. Comparte el cuerpo del transformador entre las tareas, pero la comprensión de ruta a través de SigLIP y generación a través de un tokenizer VQ. En 7B, Janus-Pro vence a DALL-E 3 en GenEval mientras que coincide con LLaVA en MMMU. Esta lección explica por qué dos codificadores funcionan cuando uno falla.

> **【中文解读】**Janus-Pro(DeepSeek,2025年1月) resolver una contradicción fundamental: comprender tareas necesita语义特征(SigLIP), generar tareas necesita reconstruir un buen código(VQ token)。 dos de ellos no pueden ser compatibles con un único codificador。

> **【拓展：解耦编码器的产业影响】**解编码器思想 se ha convertido en la estructura por defecto del modelo de 2026 统一.

**Type:** Build  | **类型:** 构建
**Languages:** Python (stdlib, dual-encoder routing + shared-body signal) | **语言:** Python（标准库，双编码器路由 + 共享体信号）
**Prerequisites:** Phase 12 · 13 (Transfusion), Phase 12 · 14 (Show-o) | **前置知识:** Phase 12 · 13（Transfusion），Phase 12 · 14（Show-o）
**Time:** ~120 minutes | **时间:** ~120 分钟

> ¿ Qué es esto ?**【前置】**学本节前请先掌握:Fase 12·02(SigLIP 语义编码器) Fase 12·13-14(Transfusión/Show-o 统一模型) Fase 8(VQ-VAE 重建编码器) Janus-Pro = "Entiender vs 生成的编码器分离"是Fase 12 多模态生成模型的最终答案之一──
> ¿ Qué es esto ?**【类比】**Janus-Pro = "esquerra izquierda"―esquerra izquierda = SigLIP(语义理解,认识"猫"的概念); right brain = VQ-VAE(像素重建,能画出猫的细节)―其他统一模型 = 强迫一个脑区同时做两件事,两边都不极致;Janus-Pro = 接受左右脑分工,共享脑干(Transformer 主体) 做高层推理──就像人类视觉皮层理解这个() 和运动皮层(绘画) 本来就在不同脑区.

## Objetivos de aprendizaje

- Explica por qué un único codificador compartido compromete la comprensión o la calidad de generación.
  > Explicar por qué un único codificador compartido puede dañar la comprensión o generar calidad.
- Describa el enrutamiento de Janus-Pro: SigLIP funciona en el lado de entrada para la comprensión, tokens VQ tanto en entrada como en salida para la generación.
  > Descripción de las rutas de Janus-Pro: entender rutas de entrada con siglip características, generar rutas de entrada y salida con tokens VQ。
- Traza la escalación de mezcla de datos que hace que Janus-Pro tenga éxito donde Janus no lo hizo.
  > 追溯让Janus-Pro éxito y Janus 失败的数据混合扩展──
- Comparar las arquitecturas desacopladas (Janus-Pro), acopladas continuas (Transfusión) y acopladas discretas (Show-o).
  > Conforme el artículo anterior, el artículo se refiere a la "capacidad de trabajo de los trabajadores" y "la capacidad de trabajo de los trabajadores".

## El problema es el contexto del problema

Los modelos unificados comparten un cuerpo transformador a través de la comprensión y la generación. Los intentos anteriores (Chameleon, Show-o, Transfusion) todos usan un tokenizer visual para ambas direcciones.

> 统一模型在理解和生成之间共享 Transformer 主体──之前的尝试(Chameleon、Show-o、Transfusion)都使用一个视觉分词器处理两个方向──分词器是妥协:

- Optimizado para la reconstrucción (generación): VQ-VAE captura detalles de píxeles de granos finos pero produce tokens con débil coherencia semántica.
  La forma en que se desarrolla la estructura de la estructura es la forma en que se desarrolla la estructura de la estructura.
- Optimizado para la semántica (entendimiento): SigLIP incorpora imágenes de "gato" cerca de tokens de "gato", pero no permite una buena reconstrucción.
  China:                                                                                                                                                                                                                                                              

En el caso de los proyectos de tecnología de la Unión Europea, la Comisión ha puesto en marcha un programa de investigación de la Unión Europea, que se desarrolla en el ámbito de la tecnología de la información y de la información.

> Show-o y Transfusión para esto pagaron un impuesto de calidad visible.

## El concepto central.

> **【中文解读】**Janus-Pro(DeepSeek) utilizando el mismo código de vídeo: un para entender tareas(CLIP 编码器), un para generar tareas(VQ 编码器)── dos codificadores comparten la misma espina dorsal del LLM, cada uno de ellos se enfoca en optimizar diferentes representaciones de vídeo──

> **【拓展：解耦编码器的动机】**Comprender las tareas requiere de características de lenguaje de alto nivel, generar las tareas requiere de características de detalle de nivel inferior. Un único programador es difícil de hacer bien a la vez.


### Código visual descoplado

La arquitectura de Janus-Pro separa los dos codificadores:

> La estructura de Janus-Pro se dividirá en dos codificadores:

- Comprensión de la ruta. Imagen de entrada → SigLIP-SO400m → Cuerpo de transformador de 2 capas MLP.
  En inglés, el método de traducción de la lengua inglesa para la traducción de la lengua inglesa se utiliza en la traducción de la lengua inglesa para la traducción de la lengua inglesa.
- Camino de generación. Imagen de entrada (si se condiciona en una imagen existente) → Tokenizer VQ → IDs de token → cuerpo del transformador.
  En inglés, el nombre de la fuente de datos de la fuente de datos de la red de datos de la red de datos de la red de datos de la red de datos de la red de datos de la red de datos de la red de datos de la red de datos de la red de datos de la red de datos de la red de datos de la red de datos de la red de datos de la red de datos de la red de datos de la red de datos de la red de datos de la red de datos de la red de datos de la red de datos de la red de datos de la red de datos de la red de datos de la red de datos de la red de datos de la red.
- Generación de salida. Tokens de imagen predicho por el transformador → decodificador VQ → píxeles.
  En inglés, el nombre de la fuente de la información es "VQ".

El cuerpo del transformador es compartido. Todo arriba y abajo del cuerpo es específico de la tarea.

> El transformador principal es compartido. Todo lo que contiene el transformador es un objetivo específico.

Las entradas se desambiguan por formato de respuesta: a `<understand>`Etiquetas de rutas a través de SigLIP; `<generate>`o la ruta es implícita de la tarea.

> 输入通过提示格式消歧:`<understand>`标签路由到SigLIP;`<generate>`路由到VQ── o 路由从任务隐式确定──

### ¿Por qué funciona esto?

La pérdida de comprensión obtiene características SigLIP, que el preentrenamiento de estilo CLIP ha ajustado para la similitud semántica.

> Comprender la pérdida de obtener características SigLIP, el entrenamiento previo del estilo CLIP ha mejorado estas características para la semejantía de palabras.

La pérdida de generación obtiene tokens VQ, que un tokenizer ha sintonizado para la reconstrucción. La calidad de la imagen mejora en comparación con Show-o porque los códigos VQ se componen de nuevo a píxeles de forma limpia.

> Los resultados de la investigación han sido muy positivos, ya que el número de imágenes de VQ se ha vuelto a aumentar.

El cuerpo del transformador compartido ve dos distribuciones de entrada (SigLIP y VQ) y aprende a trabajar con ambos.

> Comunicado de Transformer 主体 see两种输入分布(SigLIP 和 VQ),学会与两者一起工作──声称:足够的数据 +足够的参数, 主体能吸收切换──

### Escalado de datos  Janus vs Janus-Pro

Janus (original, arXiv 2410.13848) introdujo el desacoplamiento pero a pequeña escala (1.3B parámetros, datos limitados).

> Janus ([[original: original: [[Janu-Janu-Janu-Janu-Janu-Janu-Janu-Janu-Janu-Janu-Janu-Janu-Janu-Janu-Janu-Janu-Janu-Janu-Janu-Janu-Janu-Janu-Janu-Janu-Janu-Janu-Janu-Janu-Janu-Janu-Janu-Janu-Janu-Janu-Janu-Janu-Janu-Janu-Janu-Janu-Janu-Janu-Janu-Janu-Janu-Janu-Janu-Janu-Janu-Janu-Janu-Janu-Janu-Janu-Janu-Janu-Janu-Janu-Janu-Janu-Janu-Janu-Janu-Janu-Janu-Janu-Janu-Janu-Janu-Janu-Janu-Janu-Janu-Janu-Janu-Janu-Janu-Janu-Janu-Janu-Janu-Janu-Janu-Janu-Janu-Janu-Janu-Janu-Janu-Janu-Janu-Janu-Janu-Janu-Janu-Janu-Janu-Janu-Janu-Janu-Janu-Janu-Janu-Janu-Janu-Janu-Janu-Janu-Janu-Janu-Janu-Janu-Janu-Janu-Janu-Janu-Janu-Janu-Janu-Janu-Janu-Janu-Janu-Janu-Janu-Janu-Janu-Janu-Janu-Janu-Janu-Janu-Janu-Janu-Janu-Janu-Janu-Janu-Janu-Janu-Janu-Janu-Janu-Janu-Janu-Janu-Janu-Janu-Janu-Janu-Janu-Janu-Janu-Janu-Janu-Janu-Janu-Janu-Janu-Janu-Janu-Janu-Janu-Janu-Janu-Janu-Janu

- 7B parámetros (vs 1.3B).
  En el caso de los países de la región de la región de la República Popular China, el número de habitantes de la región es de 770 millones.
- 90M pares de imágenes y texto para la etapa 1 (alignamiento) desde 72M.
  China: 90.000 millones de dólares para la primera fase, desde 7200 millones de dólares para la segunda fase.
- 72M para la etapa 2 (unificada) desde 26M.
  El número de personas que han recibido el premio de la Academia de Ciencias del Medio Ambiente en el año pasado fue de 22 millones de personas.
- Se añadieron 200 mil muestras de instrucciones de generación de imágenes para la etapa 3.
  China: para la tercera fase se incrementaron 200.000 imágenes de producción de instrucciones de muestras.

El resultado: Janus-Pro-7B coincide con LLaVA en MMMU (60.3 vs ~58) y supera a DALL-E 3 en GenEval (0.80 vs 0.67). Un modelo abierto, competitivo en ambos lados del espectro unificado.

> 结果:Janus-Pro-7B en MMMU 上匹配 LLaVA(60.3 vs ~58), en GenEval 上击败 DALL-E 3(0.80 vs 0.67)。 un modelo abierto, en ambos extremos del conjunto de la matriz tienen competencia。

### JanusFlow  la variante de flujo rectificada

JanusFlow (arXiv 2411.07975) cambia el camino de generación de VQ por un camino de generación de flujo rectificado (continuo). La división se convierte en SigLIP-para-entendimiento + rectificado-flujo-para-generación. Los techos de calidad se elevan aún más. La arquitectura sigue siendo decoupling-encoders-shared-body.

> JanusFlow(arXiv 2411.07975) sustituirá el VQ 生成路径 para ser el completo流生成路径(连续) ――分离成 SigLIP Usado para entender + 整流用于生成──质量上限进一步提升──架构仍然是解编码器-共享主体──

### El trabajo del cuerpo compartido

El cuerpo del transformador procesa una secuencia unificada pero con dos distribuciones de entrada.

> Transformer principal procesamiento de la serie pero tiene dos tipos de distribución de entrada. Su tarea es:

- Para entender: consumen las características de SigLIP + tokens de texto → emiten texto autoregresivamente.
  En inglés, el nombre de la marca de la marca de la marca de la marca de la marca de la marca de la marca de la marca de la marca de la marca de la marca de la marca de la marca de la marca de la marca de la marca de la marca de la marca de la marca de la marca de la marca de la marca de la marca de la marca de la marca de la marca de la marca de la marca de la marca de la marca de la marca de la marca de la marca de la marca de la marca de la marca de la marca de la marca de la marca de la marca de la marca de la marca de la marca de la marca de la marca de la marca de la marca de marca de la marca de la marca de marca de la marca de marca de la marca de marca de marca de marca de la marca de marca de marca de marca de marca de marca de marca de marca de marca de marca de marca de marca de marca de marca de marca de marca de marca de marca de marca de marca de marca de marca de marca de marca de marca de marca de marca de marca de marca de marca de marca de marca de marca de marca de marca de marca de marca de marca de marca de marca de marca de marca de marca de marca de marca de marca de marca de marca de marca de marca de marca de marca de marca de marca de marca de marca de marca de marca de marca de marca de marca de marca de marca de marca de marca de marca de marca de marca de marca de marca de marca de marca de marca de marca de marca de marca de marca de marca de marca de marca de marca de marca de marca de marca de marca de marca de marca de marca de marca de marca de marca de marca de marca de marca de marca de marca de marca de marca de marca de marca de marca de marca de marca de marca de marca de marca de marca de marca de marca de marca de marca de marca de marca de marca de marca de marca de marca de marca de marca de marca de marca de marca de marca de marca de marca de marca de marca de marca de marca de marca de marca de marca de marca de marca de marca de marca de marca de marca de marca de marca de marca de marca de marca de marca de marca de marca de marca de marca de marca de marca de marca de marca de marca de marca de marca de marca de marca de marca de marca de marca de marca de marca de marca de marca de marca de marca de marca de marca de marca de
- Para la generación: consumen tokens de texto + (tokens VQ de imagen opcionales) → emiten tokens VQ de imagen autoregresivamente.
  En inglés, el nombre de la moneda de cambio es el símbolo de la moneda de cambio.

El cuerpo no tiene pesos específicos de modalidad por bloque. Es el transformador de estilo de texto que se espera encontrar dentro de Qwen o Llama, más los dos adaptadores de entrada.

> El eje no tiene un modelo específico de peso. Es el que usted espera encontrar en el medio de Qwen o Llama.

Curiosamente, esto significa que el cuerpo de Janus-Pro podría ser iniciado desde un LLM pre-entrenado. Janus-Pro inicia desde DeepSeek-MoE-7B. Esa elección importa: el LLM contribuye a la capacidad de razonamiento que los modelos unificados puros desde cero luchan por alcanzar.

> Curiosamente, esto significa que el tema de Janus-Pro puede comenzar a trabajar desde el primer entrenamiento de LLM.

### En comparación con el InternVL-U

El curso de seguimiento de 2026 se define como el curso de seguimiento de la U (lección 12.10).

> InternVL-U (第 12.10 课) es el siguiente curso de 2026 años.

- Preentrenamiento multimodal nativo (internVL3 espina dorsal).
  El trabajo de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de
- Enrutamiento de codificador descoplado (SigLIP en, VQ + difusión se dirige hacia fuera).
  En el caso de los sistemas de codificación, el sistema de codificación de los sistemas de codificación de los sistemas de codificación de los sistemas de codificación de los sistemas de codificación de los sistemas de codificación de los sistemas de codificación de los sistemas de codificación de los sistemas de codificación de los sistemas de codificación de codificación de los sistemas de codificación de codificación de los sistemas de codificación de codificación de los sistemas de codificación de codificación de los sistemas de codificación de codificación de los sistemas de codificación de codificación de los sistemas de codificación de codificación de los sistemas de codificación de codificación de codificación de los sistemas de codificación de codificación de codificación de los sistemas de codificación de codificación de codificación de los sistemas de codificación de codificación de codificación de los sistemas de codificación de codificación de codificación de codificación de los sistemas de codificación de codificación de codificación de codificación de los sistemas de codificación de codificación de codificación de codificación de los sistemas de codificación de codificación de codificación de codificación de codificación de codificación de codificación de codificación de codificación de codificación de codificación de codificación de codificación de codificación de codificación de codificación de codificación de codificación de codificación de codificación de codificación de codificación de codificación de codificación de codificación de codificación de codificación de codificación de codificación de codificación de codificación de codificación de codificación de codificación de codificación de codificación de codificación de codificación de codificación de codificación de codificación de codificación de codificación de codificación de codificación de codificación de codificación de codificación de codificación de codificación de codificación de codificación de codificación de codificación de codificación de codificación de codificación de codificación de codificación de codificación de codificación de codificación de codificación de codificación de codificación de codificación de codificación de codificación de codificación de codificación de codificación de codificación de codificación de codificación de codificación de codificación de codificación de codificación de codificación de codificación de codificación de codificación de codificación de codificación de codificación de codificación de codificación de codificación de codificación de codificación de codificación de codificación de codificación de codificación de codificación de codificación
- Comprensión unificada + generación + edición.
  En inglés, el nombre de la lengua es "Categoría de lenguaje".

InternVL-U incorpora la elección arquitectónica de Janus-Pro en un marco más amplio.

> InternVL-U incorporó la arquitectura de Janus-Pro a un marco más amplio.

### Las limitaciones

Los codificadores descoplados agregan complejidad arquitectónica. Dos tokenizers para entrenar, dos vías de entrada para mantener, dos conjuntos de modos de falla. Para productos que no necesitan generación, Janus-Pro es sobre-ingeniero.

> 解编码器 aumentó la complejidad de la estructura. Dos分词器要训练,两条输入路要维护,两组失败模式.

Para los productos que no requieren comprensión, Janus- Pro es sobrecalificado  elige un modelo Stable Diffusion 3 / Flux.

> 对于不需要理解的产品,Janus-Pro 大材小用选择 Estable Diffusion 3 / Flux 模型──

Para los productos que necesitan ambos, Janus-Pro es ahora la arquitectura abierta de referencia.

> Para los productos que necesitan ambos, Janus-Pro ahora es una referencia de arquitectura abierta.


> **【拓展：Janus-Pro 在基准上的表现】**Janus-Pro en el modelo de comprensión de base sobre el programa de un codificador superior a un nivel de 3%, en el de generación de imágenes superior a un nivel de 10-15%.


## Usalo en práctica.
```figure
l5-janus-decouple
```

## Usalo

`code/main.py`simula el enrutamiento de Janus-Pro:

> `code/main.py`模拟 Janus-Pro 路由:

- Dos codificadores simulados: SigLIP-like (produce vectores semánticos de 256 dimensiones) y VQ-like (produce códigos enteros).
  En el caso de los sistemas de codificación de idiomas, el número de números de los idiomas de los idiomas de los idiomas de los idiomas de los idiomas de los idiomas de los idiomas de los idiomas de los idiomas de los idiomas de los idiomas de los idiomas de los idiomas de los idiomas de los idiomas de los idiomas de los idiomas de los idiomas de los idiomas de los idiomas de los idiomas de los idiomas de los idiomas de los idiomas de los idiomas de los idiomas de los idiomas de los idiomas de los idiomas de los idiomas de los idiomas de los idiomas de los idiomas de los idiomas de los idiomas de los idiomas de los idiomas de los idiomas de los idiomas de los idiomas de los idiomas de los idiomas de los idiomas de los idiomas de los idiomas de los idiomas de los idiomas de los idiomas de los idiomas de los idiomas de los idiomas de los idiomas de los idiomas de los idiomas de los idiomas de los idiomas de los idiomas de los idiomas de los idiomas de los idiomas de los idiomas de los idiomas de los idiomas de los idiomas de los idiomas de los idiomas de idiomas de los idiomas de idiomas de los idiomas de idiomas de idiomas de idiomas de idiomas de idiomas de idiomas de idiomas de idiomas de idiomas de idiomas de idiomas de idiomas de idiomas de idiomas de idiomas de idiomas de idiomas de idiomas de idiomas de idiomas de idiomas de idiomas de idiomas de idiomas de idiomas de idiomas de idiomas de idiomas de idiomas de idiomas de idiomas de idiomas de idiomas de idiomas de idiomas de idiomas de idiomas de idiomas de idiomas de idiomas de idiomas de idiomas de idiomas de idiomas de idiomas de idiomas de idiomas de idiomas de idiomas de idiomas de idiomas de idiomas de idiomas de idiomas de idiomas de idiomas de idiomas de idiomas de idiomas de idiomas de idiomas de idiomas de idiomas de idiomas de idiomas de idiomas de idiomas de idiomas de idiomas de idiomas de idiomas de idi
- Un router de instrucción que elige el codificador basado en una etiqueta de tarea.
  Traducción:basado en etiquetas de tareas seleccionar el código de instrucciones.
- Un cuerpo compartido (stand-in) que procesa secuencias de tokens independientemente de cuál codificador las haya producido.
  China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China:
- Cambiar de la etapa 1 (alignamiento) a la etapa 3 (tón de instrucción) del calendario de muestras ponderadas.
  China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China:

Imprima las rutas de ruta para 3 ejemplos: imagen QA, T2I, edición de imagen.

> Imprimir 3 ejemplos de ruta de ruta: imágenes preguntas y respuestas, T2I, imágenes editadas,

## Envíalo .

Esta lección produce`outputs/skill-decoupled-encoder-picker.md`. Dado que un producto que quiere generación unificada + comprensión a la calidad de la frontera, elige Janus-Pro, JanusFlow o InternVL-U con una recomendación concreta de escala de datos.

> 本课产 出  `outputs/skill-decoupled-encoder-picker.md` Se debe determinar la calidad de la producción en el producto, se puede elegir entre Janus-Pro、JanusFlow o InternVL-U, con una escala de datos específica sugerida.

## Los ejercicios.

1. Janus-Pro-7B supera a DALL-E 3 en GenEval. Explique por qué un modelo abierto 7B puede coincidir con un modelo patentado fronterizo en generación pero no en comprensión.
   Traducción:Janus-Pro-7B en GenEval 上击败 DALL-E 3── explica por qué 7B 开放模型能在生成上匹敌前沿专专业模型, pero在理解上不能──

2. Implementar una función de enrutador: dado texto de respuesta, clasificar como `understand`o `generate`¿Cómo manejas las preguntas ambigüas como "describir y luego dibujar"?
   La función de la ruta es una función de la ruta.`understand`O `generate`¿Cómo se trata de la idea de "describir y luego dibujar"?

3. JanusFlow reemplaza la ruta de VQ con un flujo rectificado. ¿Qué produce ahora el cuerpo del transformador, y qué cambios en la pérdida?
   En el transcurso de la transformación, el flujo de flujo de flujo se ha convertido en un flujo de flujo de flujo de flujo de flujo de flujo de flujo.

4. Proponemos una cuarta tarea que la arquitectura Janus-Pro podría manejar con un codificador más descoplado. Ejemplos: segmentación de imágenes (estilo DINO), profundidad (estilo MiDaS).
   China: la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la

5. Leer la sección 4.2 de Janus-Pro sobre la escalación de datos. ¿Qué etapa de datos contribuye más a la ganancia de calidad de T2I vs. Janus?
   China Translation: read Janus-Pro 第 4.2 节关于数据扩展―― ¿Cuál es la etapa de datos que más contribuye a la mejora de la calidad de T2I?

## Términos clave .

| Term | What people say | What it actually means | 中文含义 | 中文释义 |
|------|-----------------|------------------------|---------|
| Decoupled encoding | "Two visual encoders" | Separate tokenizer or encoder per direction: semantic for understanding, reconstruction for generation | 每个方向使用独立的分词器或编码器：理解用语义，生成用重建 |
| Shared body | "One transformer" | Single transformer processes either encoder's output; no modality-specific weights | 单一 Transformer 处理任一编码器的输出；无模态特定权重 |
| SigLIP for understanding | "Semantic features" | CLIP-family vision tower providing rich conceptual features but poor reconstruction | CLIP 家族视觉塔，提供丰富的概念特征但重建能力差 |
| VQ for generation | "Reconstruction codes" | Vector-quantized tokens that decode cleanly back to pixels | 可干净解码回像素的向量量化 token |
| JanusFlow | "Rectified-flow variant" | Janus-Pro with a continuous flow-matching generation head instead of VQ | 使用连续流匹配生成头替代 VQ 的 Janus-Pro |
| Routing tag | "Task tag" | Prompt marker (`<understand>` / `<generate>`) that picks the input encoder | 选择输入编码器的提示标记 |

## Más Leer más Leer más

- [Wu et al. — Janus (arXiv:2410.13848)](https://arxiv.org/abs/2410.13848)
  En español: Janus 论文。
- [Chen et al. — Janus-Pro (arXiv:2501.17811)](https://arxiv.org/abs/2501.17811)
  En el caso de los jóvenes, el trabajo de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela
- [Ma et al. — JanusFlow (arXiv:2411.07975)](https://arxiv.org/abs/2411.07975)
  En el caso de los jóvenes, el trabajo de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela
- [InternVL-U (arXiv:2603.09877)](https://arxiv.org/abs/2603.09877)
  En inglés, "InterVL-U" se traduce en "InterVL-U".
- [Dong et al. — DreamLLM (arXiv:2309.11499)](https://arxiv.org/abs/2309.11499)
  En el libro de la ley de los sueños, el libro de los sueños se trata de un libro de la ley de los sueños.
