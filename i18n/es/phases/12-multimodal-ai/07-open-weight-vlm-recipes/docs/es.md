# Recetas de VLM de peso abierto: lo que realmente importa

> La literatura VLM de peso abierto 2024-2026 es un bosque de tablas de ablación. El MM1 de Apple probó 13 combinaciones de codificador de imágenes, conector y mezcla de datos. El Molmo de Allen AI demostró que los títulos humanos detallados superan la destilación GPT-4V. Cambrian-1 ejecutó 20+ comparaciones de codificadores. Idefics2 formalizó el espacio de diseño de cinco ejes. Los VLM prismáticos compararon 27 recetas de entrenamiento en un índice de referencia controlado. De todo ese ruido, un pequeño conjunto de resultados se mantiene en el papel: el codificador de imágenes importa más que la arquitectura del conector, la mezcla de datos importa más que ambas, y los títulos humanos detallados superan a los datos sintéticos destilados. Esta lección lee esas tablas para que no tengas que hacerlo.

> **【中文解读】**El estudio de la tecnología de la información (MEM) se desarrolló en el período de 2024-2026 y se desarrolló en el período de 20 a 20 años.

> **【拓展：VLM 工程的实践指南】**Cuando descubras que el rendimiento de VLM no alcanza el nivel de clasificación, debes hacer lo siguiente: 1) ¿El número de tokens de vídeo es suficiente? 2) ¿El número de los ordenadores de código es suficiente? 2) ¿El número de datos es suficiente? 3) ¿El número de datos es suficiente? 4) ¿El número de datos es suficiente? 4) El número de dispositivos de conexión es casi inalterable?

**Type:** Learn + lab  | **类型：学习 + 实验**
**Languages:** Python (stdlib, ablation table parser + recipe picker)  | **语言：Python（标准库，消融表解析器 + 配方选择器）**
**Prerequisites:** Phase 12 · 05 (LLaVA baseline)  | **前置：阶段12第05课（LLaVA基线）**
**Time:** ~180 minutes  | **时长：约180分钟**

> ¿ Qué es esto ?**【前置】**学本节前请先掌握:Fase 12·02-06(CLIP/BLIP-2/Flamingo/LLaVA/NaFlex 全套);Fase 11·08(Instrucción de sintonía)。本节是Fase 12 前半段的总结:所有架构都学过了,现在看哪些选择真正重要──
> ¿ Qué es esto ?**【类比】**开源 VLM 五轴选择 = "买车选配置"──编码器 = 发动机(перфективность差 5-7 分);连接器 = 中控台界面(几乎不影响驾驶);LLM = 车身大小;数据 = 油品(差油再好的发动机也跑不快);分辨率 = 轮胎(决定能跑什么地形)──纠结界面(连接器) es una nueva trampa, el viejo司机 priorita en la dirección de los motores y el aceite。

## Objetivos de aprendizaje

- Nombre del espacio de diseño de VLM de cinco ejes: codificador de imagen, conector, LLM, mezcla de datos, cronograma de resolución.
- Lea una tabla de ablación MM1 / Idefics2 / Cambrian-1 y pronostica qué botón mueve un punto de referencia dado.
- Elija una receta (encoder, conector, datos, resolución) para un nuevo VLM dado un presupuesto computacional y una mezcla de tareas.
- Explica por qué los títulos humanos detallados superan a la destilación GPT-4V en el mismo recuento de tokens.

## El problema es el contexto del problema

Hay cientos de VLM de peso abierto. La mayor parte de la brecha entre "bueno" y "estado de la técnica" no es arquitectura. Son datos, horario de resolución y elección de codificador. Saber qué botón girar primero cuando su modelo no funciona bien te ahorra un error de 5 millones de GPU-hora.

La ola de 2023 (LLaVA-1.5, InstructBLIP, MiniGPT-4) se realizó en el entrenamiento previo a la pareja de captura + LLaVA-Instruct-150k.

La ola de 2024 (MM1, Idefics2, Molmo, Cambrian-1, Prismatic VLMs) realizó ablaciones exhaustivas.

> **【中文解读】**En cientos de VLM de código abierto, la diferencia entre "bueno" y "mejor" no es principalmente la estructura, sino el dato, la resolución de la regulación y la selección de los codificadores.

## El concepto central.

### El espacio de diseño de cinco ejes.

Idefics2 (Laurençon et al., 2024) nombró los ejes:

1. Encodrador de imágenes / 图像编码器. CLIP ViT-L/14, SigLIP SO400m/14, DINOv2 ViT-g/14, InternViT-6B. Los codificadores difieren en el tamaño del parche, la resolución y el objetivo de pretraining / 编码器在补丁大小、分辨率和预训目标上各不相同.
2. Conector / 连接器. MLP (2-4 capas), Q-Former (32 consultas + cross-attn), Perceptor Resampler (64 consultas), C-Abstractor (convolucional + bilinear pooling) / MLP(2-4 niveles)、Q-Former(32 consulta+交叉注意力)、Perceptor 重采样器(64 consulta)、C-Abstractor(卷积+双线性池化).
3. Modelo de lenguaje / 语言模型. Llama-3 8B / 70B, Mistral 7B, Phi-3, Gemma-2, Qwen2.5.
4. Datos de entrenamiento / 训练数据. pares de capciones (CC3M, LAION), entrelazados (OBELICS, MMC4), instrucción (LLaVA-Instruct, ShareGPT4V, PixMo, Cauldron) / 描述对、交错数据、指令数据.
5. Calendario de resolución / resolución de resolución. Fijo 224/336/448, AnyRes, dinámica nativa. Rampado durante el entrenamiento o constante / 固定分辨率、AnyRes、原生动态分辨率── entrenamiento en el proceso de crecimiento o恒定.

Cada VLM de producción hace una elección en cada eje. La mayoría de las variaciones en las puntuaciones de MMMU se explican por los ejes 1, 4 y 5  no por qué conector elegiste.

> **【中文解读】**Cada VLM se hace una selección en cinco ejes. La mayor parte de la diferencia de la cantidad de MMMU es por el eje1 (editor) 轴4 (data) y el eje5 (resolución) explica en lugar de que elijas el conector. Esto significa: gastar dinero en un mejor codeador y en mejores datos, tiene más valor que la estructura de conectores enlazados.

### Eje 1: codificador > conector

MM1 Sección 3.2 mostró: el intercambio de CLIP ViT-L/14 a SigLIP SO400m/14 añadió 3 puntos MMMU. el intercambio del conector de MLP a Perceptor Resampler añadió menos de 1 punto.

Cambrian-1 "Cambrian Vision Encoders Match-Up" (Tong et al., 2024) ejecutó 20+ codificadores en un punto de referencia centrado en la visión (CV-Bench). La parte superior del tablero de clasificación es una mezcla de DINOv2 y SigLIP; CLIP está en el medio del paquete; ImageBind y ViT-MAE son más bajos. La brecha entre CLIP ViT-L y DINOv2 ViT-g/14 es de ~ 5-7 puntos en CV-Bench.

El codificador predeterminado 2026 para VLM abiertos es SigLIP 2 SO400m/14 para características semánticas + densas, a veces concatenado con DINOv2 ViT-g/14 características (Cambrian "Aggregador de visión espacial" hace esto).

> **【中文解读】**换编码器(CLIP→SigLIP)加3+ 分 MMMU,换连接器(MLP→Perceptor)加不到1分──2026年开源 VLM 的默认编码器是SigLIP 2 SO400m/14,有时与DINOv2 ViT-g/14 拼接(Cambrian 的"空间视觉聚合器"就是这样做的)──

> ️ **【易错点】**El nuevo usuario se ha caído en la trampa de "调连接器架构" pensando que Q-Former era mejor que vale la pena estudiar.

### Eje 2: el diseño del conector es un lavado.

MM1, Idefics2, Prismatic y MM-Interleaved llegaron a la misma conclusión: en un conteo fijo de tokens visuales, la arquitectura del conector apenas importa.

Lo que importa es el número de tokens. Más tokens visuales = más computación LLM = mejor rendimiento hasta un punto, luego disminuye los rendimientos. 64 tokens por imagen es demasiado poco para OCR. 576-1024 tokens es el punto dulce para la mayoría de VLM abiertos. 2048+ ayuda solo para documentos y gráficos.

Q-Former vs MLP es una cuestión de costo, no una cuestión de calidad: Q-Former limita los tokens a 32-64 independientemente de la resolución de la imagen; MLP emite todos los tokens de parche. Para entradas de alta resolución, Q-Former guarda el contexto LLM; para bajas respuestas, la diferencia es el ruido.

> **【中文解读】**En el número de tokens de visión fija, la arquitectura de los dispositivos de conexión casi no afecta el rendimiento. La diferencia entre los 2 niveles de MLP y los 32 queries de Q-Former se encuentra en 1 minuto.

### Eje 3: El tamaño de la LLM establece el techo.

El doble del LLM de 7B a 13B añade confiablemente 2-4 puntos en MMMU en cada documento de VLM. En 70B se saturan la mayoría de los puntos de referencia.

Es por eso que Qwen2.5VL-72B y Claude Opus 4.7 aplastan MMMU-Pro y ScreenSpot-Pro: el cerebro del lenguaje es enorme. Un VLM 7B no puede sustituir a un VLM 70B a través del diseño inteligente de conectores.

> **【中文解读】**LLM 翻倍(7B→13B) Estabilidad aumentar 2-4 分 MMMU──70B 时大多数基准和──VLM 的多模态推理天花板就是LLM 的文本推理天花板视觉编码器只能""数据,不能取代推理──这就是为什么72B 参数的VLM 能压7B 的语言大脑的规模不可替代的原因──

### Eje 4: datos  detallado de los títulos humanos superan la destilación DATA: descripción artificial

Molmo + PixMo (Deitke et al., 2024) es el resultado 2024 que todos deberían leer. Allen AI tenía anotadores humanos que describieron imágenes en 1-3 minutos de pasajes densos de habla a texto, dando 712K imágenes con subtítulos densos.

Molmo-72B superó a Llama-3.2-90B-Vision en 11 de los 11 puntos de referencia. El delta no es arquitectura  es calidad de leyenda.

ShareGPT4V (Chen et al., 2023) y Cauldron (Idefics2) siguieron el mismo manual con títulos humanos + GPT-4V mixtos. La tendencia es clara: para la frontera de 2026, la densidad de títulos > cantidad de títulos > conveniencia de destilación.

> **【中文解读】**El descubrimiento central de Molmo: hacer que los marcadores humanos utilizaran 1-3 minutos de imágenes de descripción de voz, obteniendo 712K de imágenes de marcas de alta calidad, completamente sin usar GPT-4V 蒸── Molmo-72B derrotó a Llama-3.2-90B-Visión en el 11/11 基准. La diferencia no es estructura es la descripción de calidad── detalle de la descripción artificial de la información de cada imagen es de 5-10 veces la descripción de la red corta, y es real, no es como GPT-4V DATA会"继承蒸幻──

> **【拓展：数据质量的投资回报】**Este hallazgo es importante para la construcción vertical de VLM: con el gasto de gran cantidad de capacidad de cálculo para modificar la estructura, no se invierten recursos para obtener datos de alta calidad en el campo. En el escenario financiero, los resultados de los informes de envío de boletos y de las imágenes de contratos con los profesionales son mucho mejores que con GPT-4V.

### Eje 5: resolución y su horario, resolución y su regulación.

Las ablaciones de Idefics2: 384 -> 448 añade 1-2 puntos. 448 -> 980 con división de imágenes (AnyRes) añade otros 3-5 en los puntos de referencia OCR. Planas de entrenamiento de resolución plana a una precisión media; ramping de resolución (inicio 224, final 448 o nativo) trenes más rápido y termina más alto.

Cambrian-1 realizó un trade-off de resolución vs. tokens: en el cálculo fijo, puede tener más tokens con menor resolución o menos tokens con mayor resolución.

La receta de producción 2026: tren etapa 1 en 384 fijos, etapa 2 con resolución dinámica hasta 1280 para tareas pesadas de OCR.

> **【中文解读】**Resolución aumentada de 384 升级 a 448 加 1-2 分,448 加 980 加 AnyRes) en OCR 基准再加 3-5 分── resolución creciente调调度(de 224 开始,到 448 或原生分辨率结束) entrenamiento más rápido、 resultados mejores── bajo presupuesto de cálculo fijo: alta resolución en OCR, baja resolución+ más token 利于一般场景理解──

### La comparación controlada de Prismatic  control frente a la experiencia

Prismatic VLMs (Karamcheti et al., 2024) es el documento que controlaba todos los ejes.

- El número de tokens visuales por imagen explica ~60% de la variación.
- La elección del codificador explica ~20%.
- La arquitectura de conectores explica ~5%.
- Todo lo demás (mix de datos, cronista, LR) el 15% restante.

Esta es una descomposición dura, pero es la respuesta más limpia a "qué debo ablar primero" en la literatura.

> **【中文解读】**Los VLM prismáticos son los más puros en el control de experimentos  el mismo 13B LLM  el mismo instrucción DATA  la misma evaluación, cada vez sólo cambia un eje  Conclusión:

### Un selector para 2026 2026 años de recopilación

Dadas las pruebas, la receta de VLM abierta por defecto para un nuevo proyecto en 2026:

- Encoder / 编码器: SigLIP 2 SO400m/14 en resolución nativa con NaFlex, concatena con DINOv2 ViT-g/14 para características densas si necesita segmentación / tierra / 如需分割/定位则拼接 DINOv2.
- Conector / 连接器: MLP de 2 capas en tokens de parche. Salta Q-Former a menos que esté limitado por token / 除非 token 受限否则跳过 Q-Former.
- LLM / 语言模型: Qwen2.5 / Llama-3.1 / Gemma 2, 7B para el costo / 成本优先选7B, 70B para la calidad / 质量优先选70B, elegido por latencia objetivo / 按延迟目标选择.
- Datos / datos: PixMo + ShareGPT4V + Calderón, completado con datos de instrucciones específicas de tareas / 补充任务特定指令数据.
- Resolución / 分辨率: dinámico (min 256, max 1280 píxeles por lado largo) / 动态(minimum256,最大1280像素每长边).
- Programación / 调度: Alineación de la etapa 1 (proyector-sólo / 仅投影器), etapa 2 de ajuste fino completo / 全参数微调, etapa 3 de ajuste fino específico de tarea / 任务特定微调.

Cada uno de esos valores por defecto se remonta a una ablación medida en los documentos citados al final de esta lección.

> **【中文解读】**Por encima de cada una de las opciones por defecto se remonta a los resultados de los experimentos de eliminación en el artículo citado en este curso. Este es el mejor punto de partida para la construcción de un nuevo proyecto de VLM en 2026.

## Usalo en práctica.
```figure
l5-vlm-recipe-knobs
```

## Usalo

`code/main.py`Es un analizador de tablas de ablación y receta. codifica las tablas de ablación MM1 e Idefics2 (condensado) y le permite hacer consultas:

- "Dado el presupuesto X y la tarea Y, ¿qué receta gana?"
- "Si cambio SigLIP por CLIP en un 7B Llama, ¿cuál es el delta esperado de MMMU?"
- "¿Qué eje debo ablar primero para una respuesta de 80% de confianza?"

La salida es una lista de recetas clasificadas con los deltas de referencia esperados y una recomendación de "ablate first".

## Envíalo .

Esta lección produce`outputs/skill-vlm-recipe-picker.md`. Dado un mix de tareas objetivo, un presupuesto de cálculo y un objetivo de latencia, emite una receta completa (encodor, conector, LLM, mix de datos, cronograma de resolución) con citas a la ablación que justifica cada elección.

> **【中文解读】**Este curso se desarrolla en VLM  Formación de selección de herramientas ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞

## Los ejercicios.

1. ¿Qué código gana en el programa de estudios de la Universidad de California en el Reino Unido? ¿La respuesta se invertiría en el programa de estudios de la Universidad de California en el Reino Unido?
   | 阅读 MM1 第 3.2 节。在固定 2B LLM 和 50M 图像预算下，哪个编码器最优？在 13B LLM 时答案会翻转吗？为什么？

2. Cambrian-1 encuentra que la concatenada DINOv2 + SigLIP supera a sí sola en los puntos de referencia centrados en la visión, pero no añade ninguna señal en MMMU.
   | Cambrian-1 发现 DINOv2+SigLIP 拼接在视觉中心基准上优于单独使用，但在 MMMU 上无增益。预测哪些基准提升、哪些持平。

3. Su objetivo es un agente de interfaz móvil en un 2B LLM. Seleccione un codificador, conector, resolución y mezcla de datos. Justifique cada elección con una tabla de ablación específica.
   | 目标是在 2B LLM 上构建移动端 UI 代理。选择编码器、连接器、分辨率和数据混合，用具体消融表论证每个选择。

4. Molmo vende modelos 4B y 72B. El 4B es competitivo con los VLM cerrados 7B; el 72B supera a Llama-3.2-90B-Vision en 11/11 puntos de referencia. ¿Qué le dice eso sobre la hipótesis de plato del tamaño de LLM?
   | Molmo 的 4B 模型与闭源 7B VLM 竞争力相当；72B 在 11/11 基准上击败 Llama-3.2-90B-Vision。这对 LLM 规模饱和假说意味着什么？

5. Diseñar una tabla de ablación para aislar la calidad de la mezcla de datos de la calidad del codificador en un VLM 7B. ¿Cuántas carreras de entrenamiento mínimo? Propón las cuatro configuraciones de eje.
   | 设计消融实验表，在 7B VLM 上隔离数据混合质量和编码器质量。最少需要多少次训练？提出四组轴设置。

## Términos clave .

| Term | What people say | What it actually means | 中文含义 | 中文释义 |
|------|-----------------|------------------------|----------|---------|
| Ablation | "Turning one knob" | Training multiple runs that differ in exactly one design-space axis, holding everything else constant | 消融实验：只改变一个设计轴、保持其他不变的多组训练 | |
| Connector | "Bridge" / "projector" | Trainable module that maps vision encoder output into the LLM's token space (MLP, Q-Former, Perceiver) | 连接器：将视觉编码器输出映射到 LLM token 空间的可训练模块 | |
| Detailed human caption | "Dense caption" | A multi-sentence human-written description (typically 80-300 tokens) richer than a web alt text | 详细人工描述：人类编写的多句描述（通常80-300 token） | |
| Distillation | "GPT-4V captions" | Training data generated by a stronger proprietary VLM; convenient but prone to inherited hallucination | 蒸馏：用更强的专有 VLM 生成训练数据；方便但会继承幻觉 | |
| AnyRes / dynamic res | "High-res path" | Strategy to feed images larger than the encoder's native resolution via tiling or M-RoPE | AnyRes/动态分辨率：通过切片或 M-RoPE 处理超过编码器原生分辨率的图像 | |
| Resolution ramp | "Curriculum" | Training schedule that starts low-resolution and increases, speeding alignment learning | 分辨率递增：从低分辨率开始逐步增加的训练调度 | |
| Vision-centric bench | "CV-Bench / BLINK" | Evaluation that stresses fine-grained visual perception rather than language-heavy reasoning | 视觉中心基准：测试精细视觉感知能力而非语言推理 | |
| PixMo | "Molmo's data" | Allen AI's 712K densely-captioned image dataset; human speech transcribed into dense captions | Allen AI 的 712K 密集标注图像数据集；人工语音转录为密集描述 | |

## Más Leer más Leer más

- [McKinzie et al. — MM1 (arXiv:2403.09611)](https://arxiv.org/abs/2403.09611) Apple MM1                                                                                                                                                                                                                                                             
- [Laurençon et al. — Idefics2 / What matters building VLMs (arXiv:2405.02246)](https://arxiv.org/abs/2405.02246) Los factores clave para construir VLM
- [Deitke et al. — Molmo and PixMo (arXiv:2409.17146)](https://arxiv.org/abs/2409.17146)♬ Molmo y PixMo ♬ ♬ ♬ ♬ ♬ ♬ ♬ ♬ ♬ ♬ ♬ ♬ ♬ ♬ ♬ ♬ ♬ ♬ ♬ ♬ ♬ ♬ ♬ ♬ ♬ ♬ ♬ ♬ ♬ ♬ ♬ ♬ ♬ ♬ ♬ ♬ ♬ ♬ ♬ ♬ ♬ ♬ ♬ ♬ ♬ ♬ ♬ ♬ ♬ ♬ ♬ ♬ ♬ ♬ ♬ ♬ ♬ ♬ ♬ ♬ ♬ ♬ ♬ ♬ ♬ ♬ ♬ ♬ ♬ ♬ ♬ ♬ ♬ ♬ ♬ ♬ ♬ ♬ ♬  ♬   ♬     ♬      ♬                                                                                                                                                                                                                                                                                                                                     
- [Tong et al. — Cambrian-1 (arXiv:2406.16860)](https://arxiv.org/abs/2406.16860)∙ Cambrian-1 en el código
- [Karamcheti et al. — Prismatic VLMs (arXiv:2402.07865)](https://arxiv.org/abs/2402.07865)                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             
