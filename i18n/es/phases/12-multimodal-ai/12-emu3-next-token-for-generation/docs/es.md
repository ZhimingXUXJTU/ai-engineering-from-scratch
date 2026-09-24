# Emu3: Previsión de la próxima marca para la generación de imágenes y videos.

> El Emu3 de BAAI (Wang et al., septiembre 2024) es el resultado de 2024 que debería haber terminado el debate difusión-versus-autorregressiva. Un único transformador de decodificación solo de estilo Llama, entrenado solo en el objetivo de predicción de tokens siguientes, a través de un vocabulario unificado de tokens de texto + VQ de imagen + 3D VQ de vídeo, supera a SDXL en generación de imágenes y LLaVA-1.6 en percepción. No hay pérdida de CLIP. No hay horario de difusión. La orientación sin clasificador se utiliza para inferir la calidad, pero el objetivo principal de la formación es la predicción de la próxima señal con la fuerza del profesor. Publicado en Nature. Esta lección lee la tesis Emu3  por qué un mejor tokenizer más escala es todo lo que necesita  y contrasta con los enfoques de difusión.

> **【中文解读】**Emu3(BAAI,2024年9月) con un solo token de auto-regreso 预测目标, en unido de texto + imágenes + vídeos 预测目标, entrenamiento en la lista de palabras de la formación, en la generación de imágenes derrotó SDXL, en la comprensión visual derrotó LLaVA-1.6── sin CLIP 损失, sin la regulación de propagación, el objetivo del entrenamiento central es el siguiente token 预测── publicado en Nature 上──

> **【拓展：自回归 vs 扩散的争论】**La contribución central de Emu3 es conceptual: si el siguiente token 预测 puede ser compatible con el modelo de propagación en la generación de imágenes, entonces el camino del modelo unificado  (a)  (a)  (a)  (a)  (a)  (b)  (a)  (a)  (b)  (a)  (b)  (b)  (b)  (b)  (c)  (c)  (c)  (c)  (c)  (c)  (c)  (c)  (c)  (d)  (d)  (d)  (d)  (d)  (d)  (d)  (d)  (d)  (d)  (d)  (d)  (d)  (d)  (d)  (d)  (d)  (d)  (d)  (d)  (d)  (d)  ( ()  ()  ()  ()  ()  ()  ()  ()  () )  ()  ()  ()  ()  ()  () )  ()  ()  ()  ()  ()  ()  () )  ()  ()  ()  ()  () )  () () () ()

**Type:** Learn  | **类型:** 学习
**Languages:** Python (stdlib, 3D video tokenizer math + autoregressive sampler skeleton) | **语言:** Python（标准库，3D 视频分词器数学 + 自回归采样器骨架）
**Prerequisites:** Phase 12 · 11 (Chameleon) | **前置知识:** Phase 12 · 11（Chameleon）
**Time:** ~120 minutes | **时间:** ~120 分钟

> ¿ Qué es esto ?**【前置】**学本节前请先掌握:Fase 12·11(Chameleon 早期融合 token) 、Fase 8·01-03(扩散模型基础,对照学习) 、Fase 7(自归下代币 训练) ⋅Emu3 =Chameleon 思路 + 更好VQ 分词器 + 大规模训练──
> ¿ Qué es esto ?**【类比】**扩散模型 vs Emu3 = "画油画" vs "拼乐高"。扩散 = 从噪音开始一步精修(连续去噪), cada paso todos volver a dibujar toda la imagen;Emu3 = un token 往下拼拼(离散乐高块), según el orden de composición de la imagen。乐高看粗, pero los bloques suficientemente pequeños+种类足多时也能拼出逼真画面, y y los textos generan el mismo conjunto de mecanismos(son los siguientes tokens)。
> ¿ Qué es esto ?**【困惑】**P: 既然 Emu3 这么强,为什么稳定扩散 仍然主流? 推理成本!扩散模型 50 步去噪就能出图,Emu3 自归需要生成上千代币才能出图,慢 20 倍. 创建质量 Emu3 接近 SDXL,但推理慢,所以生产仍然偏爱扩散.

## Objetivos de aprendizaje

- Explica por qué el objetivo de tokens de una sola pérdida de Emu3 funciona a pesar de la suposición de hace mucho tiempo de que la difusión es necesaria para la calidad de la imagen.
  >  Explicar por qué Emu3 单一损失的下一代币 目标在长期假设"图像生成必须扩散"的情况下 sigue siendo válido.
- Describa el tokenizer de vídeo 3D: cómo se ve un libro de código VQ espacial-temporal, por qué los parches duran tiempo.
  > 描述 3D 视频分词器:时空 VQ 码本长什么样、为什么补丁 要跨时间维度──
- Comparar Emu3 vs. Estable Diffusion XL en (computación de entrenamiento, costo de inferencia, límite de calidad).
  > Comparar Emu3 con la Difusión Estable XL en la diferencia en la capacidad de cálculo de entrenamiento, el costo de cálculo y la calidad en la línea superior.
- Nombre de los tres roles que el mismo modelo Emu3 juega: Emu3-Gen (gen de imagen), Emu3-Chat (percepción), Emu3-Stage2 (gen de vídeo).
  > 列举同一 Emu3 模型扮演的三种角色:Emu3-Gen(图像生成)、Emu3-Chat(感知)、Emu3-Stage2(视频生成)。

## El problema es el contexto del problema

La sabiduría convencional hasta 2024: la generación de imágenes necesita difusión. El argumento: los tokens de imagen discretos pierden demasiada información para reconstruir detalles, y el muestreo autoregresista acumula error en miles de tokens. Estable Diffusion, DALL- E 3, Imagen, Midjourney todos utilizan alguna forma de difusión. Chameleon (Lección 12.11) refutó parcialmente esto a pequeña escala, pero no coincidió con SDXL en calidad.

> El punto final es: separarse de los tokens de imágenes  perder demasiada información no puede reconstruirse detalles, auto-regreso de la muestra en miles de tokens                                                                                                                                                                                                                                                                                                                                                                                                                                                                                         

Emu3 atacó el argumento de frente. La afirmación: mejor tokenizer visual + escala suficiente + pérdida de token siguiente = generación de imagen de difusión en el mismo modelo que también hace percepción.

> Emu3 está enfrentando este argumento. afirma: mejor visual分词器 + 足够的规模 + 下一代币 损失 = generación de imágenes que se extienden más allá del mismo modelo, al mismo tiempo que se puede hacer percepción.

La apuesta fue controvertida cuando se publicó. Dos años después, la familia de generación unificada de código abierto (Emu3, Show-o, Janus-Pro, Transfusion) es el camino predeterminado para la investigación; los modelos de producción fronteriza parecen usar alguna variante.

> Este año, el estudio de la investigación de la producción de modelos de vanguardia también parece utilizar algún tipo de variación.

## El concepto central.

> **【中文解读】**EMU3 utiliza puramente auto-regreso siguiente token  predicción unificó multimodelo comprensión y generación。 imágenes se desprenden en token 序列, modelo como predicción texto como predicción siguiente token visual。

> **【拓展：自回归图像生成的挑战】**El método de auto-regreso puro de EMU3 sigue retrasado en la generación de imágenes en el modelo de expansión, ya que la longitud de los tokens visuales depende de texto más difícil de aprender. Pero la ventaja de la estructura unificada es que el mismo modelo comprende y genera imágenes/texto simultáneamente.


### El tokenizador Emu3

El ingrediente clave es el tokenizer visual. Emu3 entrena un tokenizer personalizado de clase IBQ (Quantizer de cuello de botella inverso, familia SBER-MoVQGAN) a 8x8 de reducción de resolución por token. Una imagen de 512x512 se convierte en 64x64 = 4096 tokens en el tamaño del libro de código 32768.

> 关键成分是视觉分词器──Emu3 训练了自定义 IBQ 类分词器(逆瓶量化器,SBER-MoVQGAN 家族), cada token 8x8 分辨率缩减──一张 512x512 图像变成64x64 = 4096 代币,码本大小 32768──

Esto es más grande que los 1024 tokens de Chameleon por 512x512 en K=8192 pero más barato por token (buscas más pequeñas de códigos, códec más simple).

> Este es más grande que el de Chameleon (en inglés) pero cada uno es más barato.

Para el vídeo: un tokenizer VQ 3D codifica un parche espacio-temporal (4x4x4 píxeles) a un número entero. Un clip 4s a 8 FPS tiene 32 cuadros; en 256x256 con 4x reducción espacial y 4x temporal, el recuento de tokens es (256/4) * (256/4) * (32/4) = 64 * 64 * 8 = 32.768 tokens.

> 对于视频:3D VQ 分词器将时空补丁(4x4x4 像素)编码为整数──4秒片段在 8 FPS 下有 32 ;256x256 分辨率下 4x 空间和 4x 时间缩减,代码数字为 32768──

La calidad del tokenizer es el techo. La contribución de Emu3 es en parte "entrenamos a un muy buen tokenizer".

> La calidad de los lenguajes es superior. La contribución de Emu3 se basa en "Hemos entrenado un lenguaje muy bueno".

### Formación de pérdida única

Emu3 utiliza un objetivo: predicción de tokens siguientes en un vocabulario compartido entre tokens de texto, tokens de imagen 2D y tokens de video 3D. Los pesos se multiplican por factores específicos de la modalidad durante el entrenamiento para equilibrar la contribución, pero la función de pérdida es idéntica.

> Emu3 utiliza un objetivo: en el compartido palabra汇表下一代币 预测, abarcan el texto token、2D 图像 token 和 3D 视频 token。 entrenamiento tiempo de peso multiplicado por un modelo de factores específicos para equilibrar la contribución, pero la función de pérdida es la misma。

El tren en una mezcla de:
- Género de imagen: `<text caption> <image> image_tokens </image>`
  En inglés: image generation
- Percepción de imagen: `<image> image_tokens </image> <question> text_tokens`
  Traducción:Images de la percepción
- Gen de vídeo: `<text caption> <video> video_tokens </video>`
  Traducción:video
- Percepción de vídeo: análogo.
  En inglés, el idioma de la lengua china es el idioma de la lengua china.
- Sólo texto: NTP estándar.
  En español, el nombre de la persona que se encuentra en el lugar de la persona que se encuentra en el lugar de la persona que se encuentra en el lugar de la persona que se encuentra en el lugar de la persona que se encuentra en el lugar de la persona que se encuentra en el lugar de la persona que se encuentra en el lugar de la persona que se encuentra en el lugar de la persona que se encuentra en el lugar de la persona que se encuentra en el lugar de la persona que se encuentra en el lugar de la persona que se encuentra en el lugar de la persona que se encuentra en el lugar de la persona que se encuentra en el lugar de la persona que se encuentra en el lugar de la persona que se encuentra en el lugar de la persona.

El modelo aprende cuándo emitir tokens de imagen frente a tokens de texto a partir de la distribución de datos.`<image>`- ¿Qué?

> 模型从数据分布中学习何时输出图像代币与文本代币―― capacidad de generación de los modelos en `<image>`标签后预测 símbolo de imagen

### Orientación y temperatura sin clasificador

La generación de imágenes autoregresivas mejora mucho con la orientación sin clasificador (CFG) en la inferencia. Emu3 la utiliza: genera dos veces, una vez con la leyenda completa, una vez con una leyenda vacía, mezcla los logits con un peso de la guía (típico 3.0-7.0).

> Emu3 Utiliza: genera dos veces, una vez con descripción completa, una vez con descripción en el espacio, con el peso de dirección (tipo de valor 3.0-7.0) logits mixtos.

La temperatura es importante: demasiado alta, artefactos; demasiado baja, colapso de modo. La temperatura recomendada de Emu3 es de 1,0 para la percepción, 0,8 para la generación de imágenes.

> 温度很重要: demasiado alto tendrá una falsa sombra; demasiado bajo causará un colapso de los modelos.

### Tres papeles, un modelo

Emu3 como tres API funcionalmente distintas pero un conjunto de pesas subyacente:

> Emu3 以三个 funciones diferentes API 发货, pero utilizar el mismo conjunto de derechos:

- Emu3 Gen. Generación de imágenes.
  En el caso de los ejemplos de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de
- Emu3-Chat. VQA y subtítulos. Imagen de entrada (tokens), texto de salida.
  En español: Emú3-Chat──视觉问答和描述──输入图像(token),输出文本──
- Emu3-Etapia2. Generación de vídeo y VQA de vídeo. Ingreso de texto o vídeo, salida de texto o vídeo.
  En español: Emu3-Stage2──videoproducción y video preguntas y respuestas──输入文本或视频,输出文本或视频──

No hay cabezas específicas de tareas, solo plantillas de instrucciones diferentes, el mismo punto de control.

> No hay un tema específico. Sólo hay diferentes puntos de control.

### Indicadores de referencia

De la publicación de Emu3 (septiembre 2024):

> Desde Emu3 论文(2024 年 9 月):

- Generación de imágenes: supera a SDXL en MJHQ-30K FID (5.4 vs 5.6), GenEval en general (0.54 vs 0.55  empate estadístico), y el compuesto de Deep-Eval en par.
  En el caso de los Estados Unidos, el número de personas que han sido víctimas de la pandemia es de 5,4 a 5,6 millones.
- Percepción de imagen: supera a LLaVA-1.6 en VQAv2 (75.1 vs 72.4) y coincide aproximadamente en MMMU.
  En el caso de los estudiantes de la universidad, el nivel de la enseñanza de la lengua se reduce a un nivel de la enseñanza de la lengua.
- Generación de vídeo: calidad de 4 segundos en FVD competitivo con modelos de la era Sora comparados públicamente.
  La competencia de los modelos de base abierta de la época Sora es equivalente.

Los números no siempre están ganando  Emu3 negocia un punto aquí por un punto allí  pero la afirmación "la predicción de la próxima ficha es todo lo que necesitas" es defendible a través de las modalidades.

> El número no siempre gana en un punto por otro, pero la afirmación de que "la predicción es todo lo que necesitas" es que en todos los modelos se puede mantener en pie.

### Costo de cálculo

Emu3 fue entrenado en ~300 mil millones de tokens multimodal con un modelo de parámetro 7B. Las horas de GPU son aproximadamente comparables al preentrenamiento Llama-2-7B (2k-4k GPU-años en silicio de clase A100).

> Emu3 en alrededor de 3000 mil millones de tokens de modalidad de forma más alta con 70 mil millones de parámetros de modelo de entrenamiento. GPU: un número de horas aproximadamente similar a Llama-2-7B  pre-entrenamiento equivalente a A100 片 sobre 2k-4k GPU años) ⋅ Estabilidad de difusión 3 etc.

En la inferencia, Emu3 es más lento que SDXL por imagen: 4096 tokens de imagen a 30 tok/s es ~2 minutos por imagen 512x512 , frente a 2-5 segundos para SDXL. La descifrado especulativo y la optimización de KV-cache estrechan la brecha pero no la cierran.

> 推理时,Emu3 Cada imagen de la SDXL 慢:4096 个图像代币 以 30 tok/s 生成,每张 512x512 图像约2分钟,而SDXL只需2-5秒――投机解码和KV 缓存优化缩小了差距但没有关闭它――自归图像生成计算密度;这是持续存在的权衡――

### Por qué importa

La contribución profunda de Emu3 es conceptual. Si la predicción de los tokens siguientes se adapta a la difusión en la generación de imágenes, el camino del modelo unificado (una pérdida, una columna vertebral, cualquier modalidad) es viable. Los modelos futuros no necesitan codificadores de texto separados, cronólogos de difusión separados, VAEs separados. Un transformador, un tokenizer por modalidad, escala.

> La contribución profunda de Emu3 es conceptual. Si el siguiente token 预测能扩展到在图像生成上匹敌扩散,统一模型路径 ((un损失、一个骨干、任何模态) es realizable.

Show-o, Janus-Pro y InternVL-U se basan o desafían a esta tesis. Los laboratorios chinos (BAAI, DeepSeek) publican más agresivamente en esta dirección que los laboratorios estadounidenses hasta 2025.

> Show-o、Janus-Pro 和 InternVL-U fueron construidos en este punto de vista o lo desafiaron. China Laboratories (BAAI、DeepSeek) publicaron más activamente en este sentido antes del año 2025 que los Laboratorios de EE.UU.


> **【拓展：EMU3 的统一训练策略】**La contribución central de la EMU3 es demostrar que el método de auto-regreso puro puede hacerse a la vez comprensión y generación. En la tarea de comprensión visual se aproxima a LLaVA, en la gráfica de vida se aproxima a SDXL.


## Usalo en práctica.
```figure
l5-emu3-next-token
```

## Usalo

`code/main.py`construye dos piezas de juguete:

> `code/main.py`Construyeron dos componentes de juguete:

- Una calculadora de recuento de tokenizaje VQ 2D vs 3D: dada (resolución, parche, longitud de clip, FPS), cuenta los tokens de cálculo para imagen vs video.
  Traducción: 2D vs 3D VQ 分词器计数计算器:给定(分辨率、补丁、片段长度、FPS), calcular imágenes y vídeos de los tokens números。
- Un muestreo autoregresor de marcas de imagen con orientación sin clasificador a temperatura.
  China: 带温度和无分类器引导的自归图像代币 采样器── también conocido como 采样器, también conocido como 采样器, 采样器, 采样器, 采样器, 采样器, 采样器, 采样器, 采样器, 采样器, 采样器, 采样器, 采样器, 采样器, 采样器, 采样器, 采样器, 采样器, 采样器, 采样器, 采样器, 采样器, 采样器, 采样器, 采样器, 采样器, 采样器, 采样器, 采样器, 采样器, 采样器, 采样器, 采样器, 采样器, 采样器, 采样器, 采样器, 采样器, 采样器, 采样器, 采样器, 采样器, 采样器, 采样器, 采样器, 采样器, 采样器, 采样器, 采样器, 采样器, 采样器, 采样器, 采样器, 采样器, 采样器

La implementación del CFG coincide con la receta de Emu3  mezclar logits condicionales e incondicionales con un peso de orientación.

> CFG                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            

## Envíalo .

Esta lección produce`outputs/skill-token-gen-cost-analyzer.md`. Dado un producto de generación especificación (imagen o vídeo, resolución objetivo, nivel de calidad, presupuesto de latencia), se calcula el recuento de tokens, el costo de inferencia, y elige Emu3 familia vs difusión.

> 本课产 出  `outputs/skill-token-gen-cost-analyzer.md` Es decir, el producto se ha producido en forma de imagen o vídeo, tiene una resolución de objetivos, una calidad de calidad, un presupuesto de retraso, calcula la cantidad de productos, el costo de cálculo y decide entre la serie Emu3 y el modelo de propagación.

## Los ejercicios.

1. Emu3 produce 4096 tokens por 512x512 imagen a una reducción de 8x8.
   Emú3 en 8x8  reducción abajo por张 512x512 图像产生 4096 个代币──计算 1024x1024 和 2048x2048 的等效值──推理延迟会如何?

2. Lea la sección 3.3 de Emu3 en el tokenizer de vídeo. Describa la forma del parche VQ 3D y por qué es 4x4x4 y no 8x8x1.
   En español, el texto de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión de la versión original de la versión de la versión original de la versión de la versión de la versión de la versión de la versión de la versión de 3D.

3. Peso de orientación libre de clasificadores 5.0 vs 3.0: ¿qué efecto visual?`code/main.py`¿ Qué ?
   Sin separador de control de peso 5.0 vs 3.0: ¿Cuál es el resultado de la visión?`code/main.py`Matemáticas de medio grado.

4. Computa los FLOP de entrenamiento para Emu3-7B a 300B tokens y compara con la Diffusión Estable 3. ¿Cuál fue más caro de entrenar?
   En inglés, el método de cálculo de Emu3-7B en 300B se utiliza para calcular los FLOPs de entrenamiento de los tokens, y el método de cálculo de Emu3-7B se utiliza para calcular los FLOPs de entrenamiento de Emu3-7B en 300B.

5. Emu3 supera a SDXL en FID pero no en VQAv2 vs VLM especializados. Explique por qué el enfoque de pérdida unificada muestra diferentes fortalezas vs especialistas en diferentes puntos de referencia.
   Emú3 en FID arriba derrotar SDXL, pero en VQAv2 arriba no como VLM profesional.

## Términos clave .

| Term | What people say | What it actually means | 中文含义 | 中文释义 |
|------|-----------------|------------------------|---------|
| Next-token prediction | "NTP" | Standard autoregressive loss: predict token[i+1] given token[0..i]; works for every modality when tokenized | 标准自回归损失：给定 token[0..i] 预测 token[i+1]；分词后适用于所有模态 |
| IBQ tokenizer | "Inverse bottleneck quantizer" | A class of VQ-VAE with larger codebooks (32768+) and better reconstruction than Chameleon's | 一类更大码本（32768+）和更好重建质量的 VQ-VAE |
| 3D VQ | "Spatiotemporal quantizer" | Codebook indexed by (time, row, col); one token covers a 4x4x4 pixel cube | 按（时间、行、列）索引的码本；一个 token 覆盖 4x4x4 像素立方体 |
| Classifier-free guidance | "CFG" | Mix conditional and unconditional logits with weight gamma; boosts image quality at inference | 用权重 gamma 混合条件和无条件 logits；提升推理图像质量 |
| Unified vocabulary | "Shared tokens" | Text + image + video all draw from the same integer space; model predicts whichever modality comes next | 文本+图像+视频共享同一整数空间；模型预测下一个模态 |
| MJHQ-30K | "Image gen benchmark" | Midjourney-quality benchmark with 30k prompts; Emu3 reports FID here | 30k 提示的 Midjourney 质量基准；Emu3 报告 FID |

## Más Leer más Leer más

- [Wang et al. — Emu3: Next-Token Prediction is All You Need (arXiv:2409.18869)](https://arxiv.org/abs/2409.18869)
  En el caso de los ejemplos de la historia, el ejemplar de la historia de la historia de la historia de la historia de la historia de la historia, es el ejemplar de la historia de la historia de la historia de la historia de la historia.
- [Sun et al. — Emu: Generative Pretraining in Multimodality (arXiv:2307.05222)](https://arxiv.org/abs/2307.05222)
  En español: Emú 多模态生成预训练──
- [Liu et al. — LWM (arXiv:2402.08268)](https://arxiv.org/abs/2402.08268)
  En el caso de los niños, el trabajo de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de la escuela de los estudiantes.
- [Yu et al. — MAGVIT-v2 (arXiv:2310.05737)](https://arxiv.org/abs/2310.05737)
  En inglés, el nombre de la palabra "magvit" se refiere a la palabra "magvit".
- [Tian et al. — VAR (arXiv:2404.02905)](https://arxiv.org/abs/2404.02905)
  En el caso de los modelos de la vida, el modelo de vida es el modelo de vida.
