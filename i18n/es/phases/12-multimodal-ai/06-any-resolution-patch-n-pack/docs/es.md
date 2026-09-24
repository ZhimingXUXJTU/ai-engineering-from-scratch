# Visión de cualquier resolución: Parche-n'-Pack y NaFlex                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             

> Las imágenes reales no son 224x224 cuadrados. Un recibo es de 9:16, un gráfico es de 16:9, un escaneo médico puede ser de 4096x4096, una captura de pantalla móvil es de 9:19.5. La respuesta VLM pre-2024  redimensionar todo a un cuadrado fijo  arrojó la señal que hace que OCR, comprensión de documentos y análisis de escena de alta resolución trabajen. NaViT (Google, 2023) mostró que se pueden empacar parches de resolución variable en un solo lote de transformador con enmascaramiento de diagonal de bloque. El M-RoPE (2024) de Qwen2-VL dejó caer por completo las tablas de posiciones absolutas. AnyRes de LLaVA-NeXT ha convertido imágenes de alta resolución en una base + subimágenes. La variante NaFlex de SigLIP 2 (2025) es ahora el codificador predeterminado para VLM abiertos que quieren un solo punto de control para servir a cada relación de aspecto. Esta lección implementa el parche de un paquete de extremo a extremo.

> **【中文解读】**La imagen del mundo real no es de 224x224 en forma cuadrada. La recepción es de 9:16, la imagen es de 16:9, la imagen médica es posible de 4096x4096──2024 años atrás VLM 统一将图像缩缩放为固定正方形, esto perderá la comprensión OCR、文档和高分辨率场景解析的关键信息──本课讲解如何让变压器以原始分辨率处理任意宽高比的图像──

> **【拓展：金融文档场景的分辨率挑战】**En el escenario financiero, el ancho de los documentos de informes, expedientes, contratos y otros documentos es superior a los mil millones de diferencias. La reducción de la forma cuadrada fija conduce a una reducción de la precisión de los textos.

**Type:** Build  | **类型:** 构建
**Languages:** Python (stdlib, patch packer + block-diagonal mask)  | **语言:** Python（标准库，补丁打包器 + 块对角掩码）
**Prerequisites:** Phase 12 · 01 (ViT patches), Phase 12 · 05 (LLaVA)  | **前置知识:** Phase 12 · 01（ViT补丁）、Phase 12 · 05（LLaVA）
**Time:** ~120 minutes  | **时间:** ~120 分钟

> ¿ Qué es esto ?**【前置】**学本节前请先掌握:Fase 12·01(ViT 把图切成补丁);Fase 12·05(LLaVA 投影器);Fase 7·04(RoPE 位置编码,本节用2D-RoPE)
> ¿ Qué es esto ?**【类比】**NaViT's patch-n'-pack = "mover por casa"── tradicional ViT = poner todo en una caja de gran tamaño cortado(bienes cortados cortados en); NaViT = diferentes tipos de cajas de gran tamaño en forma de pacotado, un camión en un montón de cajas(bloques en la esquina es el aislamiento entre cajas, no se interrumpen)──
> ️ **【易错点】**实现 NaViT 时忘记块对角掩码 → 三张图的补丁 会相互做注意,模型训练完全失败──修复:必须构建 (N,N) 的注意矩阵,只允许注意,块外为 -inf──

## Objetivos de aprendizaje

- Envuelve los parches de un lote de imágenes de resolución variable en una secuencia y construye la máscara de atención de bloque diagonal.
  > Envasar los complementos de las imágenes de diferentes resoluciones en una secuencia, construir bloques en el rincón de la atención escondido.
- Escoge entre los azulejos AnyRes (LLaVA-NeXT), NaFlex (SigLIP 2) y M-RoPE (Qwen2-VL) para una tarea determinada.
  > Según las tareas seleccionadas AnyRes 切片(LLaVA-NeXT)、NaFlex(SigLIP 2) o M-RoPE(Qwen2-VL)。
- Computa los presupuestos de tokens para OCR, gráficos y fotografía sin cambiar de tamaño.
  > 计算无缩缩的情况下 OCR 图表和摄影的代币 预算
- Nombre de los tres modos de fracaso de la talla cuadrada: texto aplastado, contenido recortado, tokens desperdiciados en relleno.
  > 列举正方形缩放的三种失败模式:文字压缩,内容裁剪,padding 浪费, 文字压缩,内容裁剪,padding 浪费, 文字压缩,内容裁剪, padding 浪费, 文字压缩, 文字压缩, 文字压缩, 文字压缩, 文字压缩, 文字压缩, 文字压缩, 文字压缩, 文字压缩, 文字压缩, 文字压缩, 文字压缩, 文字压缩, 文字压缩, 文字压缩, 文字压缩, 文字压缩, 文字压缩, 文字压缩, 文字压缩, 文字压缩, 文字压缩, 文字压缩, 文字压缩, 文字压缩, 文字压缩, 文字压缩, 文字压缩, 文字压缩, 文字压缩, 文字压缩, 文字压缩, 文字压缩, 文字压缩, 文字压缩, 文字压缩, 文字压缩, 文字压缩, 文字, 文字压缩, 文字, 文字, 文字, 文字, 文字, 文字, 文字, 文字, 文字, 文字 文字 文字 文字 文字 文字 文字  文字   文字   文字   文字    文字   文字     文字       文字                                                                                                                                                                           

## El problema es el contexto del problema

Los transformadores esperan una secuencia. Un lote es una pila de secuencias de la misma longitud. Si sus imágenes son 224x224, obtienes 196 tokens de parches cada vez, no se requiere relleno, el trabajo hecho. Entrenamiento en 224, inferir en 224, nunca más pensar en resolución.

> Transformador 期望固定长度序列──一批就是一堆等长序列──如果图像都是224x224,每次都产生196补丁代币,无需填充,问题解决──训练和推理都用224,永远不用考虑分辨率──

El mundo no coopera. Los documentos son retratos (8,5x11 pulgadas, 2:3). Las capturas de pantalla de gráfico son paisajes (16:9). Los recibos son altos y delgados (1:3).

> 现实世界不配──文档是向的(8.5x11英寸,约 2:3)──图表截图是横向的(16:9)──收据又高又窄(1:3)──医疗影像动 2048x2048或更大──移动设备截图是1170x2532(0.46:1)──

Tres opciones previas a 2024 y por qué cada una falla:

> Tres elecciones anteriores a 2024 y sus respectivas causas de fracaso:

1. El squish distorsiona el texto y las caras. La escala baja destruye las etiquetas de gráficos y el contenido de OCR. Práctica estándar hasta LLaVA-1.5.
   > 缩放为固定正方形(224x224或 336x336) ――压缩会扭曲文字和人脸──下采样会破坏图表标签和OCR 内容──LLaVA-1.5 之前的标准做法──
2. Se tira la mayor parte de la imagen, y elegir la ubicación de la cosecha es su propio problema de visión.
   > 剪剪为固定宽高比──将丢弃大部分图像,然后选择剪剪位置本身就是一个视觉问题──
3. El pad al lado más largo. Corre la distorsión pero desperdicia más del 50% de los tokens en el relleno para imágenes de retrato.
   > 填充到最长边──修复扭曲但对屏图像浪费50%+的代币 在填充上──所有填充代币的注意成本是二次的──

> **【中文解读】**Transformer 期望固定长度的序列── real world images宽高比不同,2024年前有三种做法:(1) 缩缩为正方形文字变形、OCR 内容丢失;(2) 剪丢弃大量内容;(3) 填充屏幕图像浪费50%+的代币 在填充上,注意计算成本第二次增长──

La respuesta 2024-2025: dejar que el transformador coma parches en la resolución nativa de la imagen, y averiguar cómo empacar un lote heterogéneo en una secuencia sin perder la computación.

> Respuesta de 2024-2025: Que el transformador se haga directamente con el "comer" original de resolución, y luego se piense en cómo hacer que los diferentes grupos de paquetes en una secuencia sin perder el cálculo.

## El concepto central.

### NaViT y el paquete de parches

NaViT (Dehghani et al., 2023) fue el documento que mostró que esto funciona a escala.

> NaViT ((Dehghani 等人,2023) demostró este tipo de pensamiento en gran escala.

1. Para cada imagen del lote, calcular su cuadrícula de parches nativos en un tamaño de parche elegido (digamos 14).
   > Para cada imagen en lote, para especificar el tamaño de la pieza de corrección (por ejemplo, 14) calcular el tamaño de la pieza de corrección original.
2. Aplanar los parches de cada imagen en su propia secuencia de longitud variable.
   > Para cada imagen, los complementos se plantean en su secuencia de longitud variable.
3. Concaten todos los parches de las imágenes en una larga secuencia para el lote.
   > Se compondrá todos los ajustes de las imágenes en una larga secuencia como lote.
4. Construye una máscara de atención de diagonal de bloque para que los parches de la imagen A sólo estén presentes dentro de la imagen A.
   > Construir bloques en el rincón de la pantalla, haciendo que los ajustes de la imagen A sólo se hagan en la imagen A.
5. Tenga en cuenta la información de posición por parche (2D RoPE o inserciones de posición fraccionaria).
   > Para cada complemento lleve información de posición (ROPE 2D o porcentaje de ubicaciones)

Un lote de tres imágenes en 336x336 (576 tokens), 224x224 (256 tokens) y 448x336 (768 tokens) se convierte en una secuencia de 1600 tokens con una máscara de diagonal de bloques 1600x1600.

> Tres cintas diferentes de resolución imagen(336x336=576 tokens、224x224=256 tokens、448x336=768 tokens) de los lotes se convierten en una secuencia de 1600 tokens, con 1600x1600 bloques en la esquina de la cubierta.

NaViT también introdujo la caída de parches fraccionadas durante el entrenamiento  caída de 50% de parches al azar en todo el lote  que regulariza y acelera el entrenamiento. SigLIP 2 heredó esto.

> NaViT también introdujo el entrenamiento en el tiempo de la cantidad de complementos desechados en la entrega de los mismos 50% de los complementos, ya sea normalización y aceleración de los entrenamientos.

> **【中文解读】**NaViT: 3张不同分辨率的图像(576 + 256 + 768 = 1600 个代币) se empaquetó en una secuencia, con bloques en los que se oculta para evitar el paso de la imagen.

### ¿Qué es eso?

La alternativa más práctica es AnyRes de LLaVA-NeXT. Dado una imagen de alta resolución y un codificador fijo (CLIP o SigLIP en 336), la imagen se conforma con un mosaico:

1. Seleccione un diseño de cuadrícula de un conjunto predefinido  (1x1), (1x2), (2x1), (1x3), (3x1), (2x2), etc.  que mejor se adapte a la relación de aspecto de la imagen.
2. Tela la imagen completa en la cuadrícula; cada mosaico se convierte en un recorte de 336x336.
3. También produce una miniatura: toda la imagen se ha redimensionado a 336x336 como un token de contexto global.
4. Encifre cada mosaico a través del codificador congelado 336. Concaten los tokens de mosaico + tokens de miniatura.

Para una imagen 672x672 en una cuadrícula 2x2 más miniatura: 4 * 576 + 576 = 2880 tokens visuales.

AnyRes es la ruta de elección cuando su codificador está congelado y sólo admite una resolución. Explosa el recuento de tokens para imágenes grandes (una imagen de 1344x1344 en una cuadrícula 4x4 es de 9216 + 576 ≈ 9800 tokens, que llena la mayor parte de un contexto de LLM de 8k).

> **【中文解读】**AnyRes  Aplicable para el codificador se bloquea y sólo apoya la situación de una sola resolución.

### M-RoPE (Qwen2-VL)  M-RoPE

Qwen2-VL introdujo el embebimiento de posición rotativa multimodal. En lugar de las posiciones fraccionarias de NaViT o el mosaico y miniatura de AnyRes, cada parche tiene una posición 3D (temporal, altura, ancho).

M-RoPE envía una resolución dinámica nativa sin reentrenamiento. En la inferencia de que se alimenta cualquier imagen HxW, el embebedador de parches produce tokens H/14 x W/14, cada token obtiene su posición (t=0, r=row, c=col), RoPE gira la atención con las frecuencias correctas, hecho. Qwen2.5-VL y Qwen3-VL continúan esto.

A diferencia de AnyRes, M-RoPE es O(H x W / P^2) tokens en resolución nativa  sin gastos generales multiplicativos de las baldosas. A diferencia de NaViT, todavía espera una sola imagen por adelante.

> **【中文解读】**M-RoPE para cada complemento otorga tres dimensiones de posición (tempo, altura, ancho), con la posición de giro codificada para procesar cualquier H、W y longitud del tiempo.

### NaFlex (SigLIP 2) NaFlex  resolución flexible

NaFlex es el modo nativo de la señal de control SigLIP 2. Un modelo único sirve a múltiples longitudes de secuencia (256, 729, 1024 tokens) en la inferencia. Internamente utiliza parches de estilo NaViT durante el entrenamiento y posiciones fraccionarias absolutas por parche.

Para una tarea semántica (clasificación, recuperación), 256 tokens. Para OCR o comprensión de gráficos, 1024 tokens. No hay reentrenamiento.

> **【中文解读】**NaFlex: un punto de control, recomendación en función de la tarea seleccionar el token 预算──语义任务使用256 token,OCR或图表理解使用1024 token,无需重训──这是非常适合构建成本敏感的多模态服务按需分配代币 预算──

### La máscara de empaque

La máscara de diagonal de bloque es donde la mayoría de las implementaciones tropiezan.`N_total`que cubren las imágenes `i=0..B-1`con longitud `n_i`, la máscara`M`de forma`(N_total, N_total)`es 1 si ambos índices caen en el mismo bloque de la imagen, o 0.

```
offsets = [0, n_0, n_0+n_1, ..., N_total]                         # 累积偏移量
M[i, j] = 1 iff there exists b where offsets[b] <= i < offsets[b+1] # 同一图像块内为1
                        and offsets[b] <= j < offsets[b+1]
```

Esta es una línea en PyTorch con `torch.block_diag`El camino de longitud variable de FlashAttention (`cu_seqlens`) se salta de la máscara por completo y se realiza en secuencias utilizando el tensor de longitud acumulada directamente  ~ 10 veces más rápido que una máscara densa para lotes típicos.

> **【中文解读】**Bloque contra corna ocultar asegurar que cada pieza de la imagen sólo se concentra en sí misma, no "ver" con los otros lotes de piezas de la imagen.`cu_seqlens`) directamente con la longitud acumulada, la cantidad de hacer la atención, saltó sobre el escondido intenso, velocidad de aproximadamente 10 veces.

### Los presupuestos de los tokens

Elige tu estrategia por tarea:

- OCR / documentos: 1024-4096 tokens. SigLIP 2 NaFlex en 1024, o AnyRes 3x3 + miniatura.
- Gráficos y UI: 729-1024 tokens en 384-448 nativo. Resolución dinámica Qwen2.5VL con límite máximo de píxeles.
- Las fotos naturales: 256-576 tokens está bien. El LLM en el río abajo ve suficiente. Pague por tokens donde la densidad de contenido es alta.
- Video: 64-128 tokens por fotograma después de la agrupación espacial, 2-8 FPS. La lección 12.17 cubre esto.

La regla de producción 2026: escoger una tapa de pixel máximo por tarea, codificar en proporción de aspecto nativa hasta esa tapa, empacar el lote y saltar relleno.`min_pixels`y `max_pixels`para exactamente este botón.

> **【拓展：Token 预算与成本优化】**En el entorno de producción, los tokens  presupuesto afectan directamente a la API  成本和延迟── para las tareas de OCR 分配1024+ tokens es necesario, pero la fotografía natural con 256 tokens es suficiente.

> ¿ Qué es esto ?**【困惑】**Estudiando este capítulo también se preguntará:1) ¿Por qué no se utiliza directamente 2k×2k? token Segunda explosión,长文档一张图就吃掉整个LLM 上下文。3) NaFlex vs AnyRes 哪个更通用? NaFlex(SigLIP 2) Más moderno, un solo punto de control 适配所有分辨率;AnyRes 是过渡方案。

## Usalo en práctica.
```figure
mm-patch-n-pack
```

## Usalo

`code/main.py`Implementa el paquete de parches para un lote heterogéneo de imágenes con coordenadas de píxeles enteros.

> `code/main.py`Utilizando un conjunto de imágenes, se logró un paquete de parches de imágenes de diferentes conjuntos.

- Toma una lista de tamaños de imagen (H, W).
  > 接收 (H, W) 图像尺寸列表──
- Computa la longitud de la secuencia de parches de cada imagen en el tamaño de parche 14.
  > 计算每张图像在补丁大小 14 下的序列长度──
- Los empaque en una secuencia de longitud total .`sum(n_i)`¿ Qué ?
  > 打包为总长度                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                       `sum(n_i)`De una sola secuencia.
- Construye la máscara de atención de bloque diagonal (densa, para mayor claridad).
  > 构建块对角注意力掩码 (construcción de bloques en la esquina)
- Compara el coste de empaquetado con el tamaño cuadrado y el mosaico de AnyRes.
  > En comparación con el coste de la carga frente a la reducción de la forma de cuadro y la reducción de la forma de cuadro.
- Imprime una tabla de presupuesto simbólica para un lote mixto (recibo, gráfico, captura de pantalla, foto).
  > 打印混合批次(收据、图表、截图、照片) de los símbolos  presupuestos 预算表。

Los números que se caen son la razón por la que cada VLM abierto 2026 usa parches.

> 运行它──印出的数字就是每2026 开源VLM都使用补丁包的原因──

## Envíalo .

Esta lección produce`outputs/skill-resolution-budget-planner.md`. Dado una carga de trabajo de relación de aspecto mixta (OCR, gráficos, fotos, fotogramas de video) y un presupuesto total de tokens, elige la estrategia correcta (NaFlex, AnyRes, M-RoPE o cuadrado fijo) y emite una configuración por solicitud.

> 本课产 出  `outputs/skill-resolution-budget-planner.md` Dado un mix mixto de largo y largo trabajo de carga (OCR, gráficos, fotos, vídeos) y un total de tokens  presupuesto, se elige la estrategia correcta  NaFlex, AnyRes, M-RoPE o forma cuadrada fija) y se genera según la configuración de la solicitud  Usar esta habilidad para la selección de productos  Es posible evitar  retrasar el presupuesto  10 veces más de los tokens  Explosión 

> **【中文解读】**Este curso se desarrolla en el marco de la investigación y desarrollo de la tecnología de la información y de la información sobre la información y la información sobre la información y la información sobre la información y la información sobre la información y la información sobre la información y la información sobre la información y la información sobre la información y la información sobre la información y la información sobre la información y la información sobre la información y la información sobre la información y la información sobre la información y la información sobre la información y la información sobre la información y la información sobre la información y la información sobre la información y la información sobre la información y la información sobre la información y la información sobre la información y la información sobre la información y la información sobre la información y la información sobre la información y la información sobre la información y la información sobre la información.

## Los ejercicios.

1. Un recibo es 600x1500 (1:2.5). En el tamaño de parche 14, ¿cuántos tokens de resolución nativa? ¿Cuántos después de cuadrar a 336? ¿Cuál pierde más precisión OCR en la práctica?
   | 一张收据 600x1500（1:2.5）。补丁大小14下，原始分辨率多少 token？缩放到336正方形后多少？实际中哪种 OCR 精度损失更大？

2. Construye la máscara de diagonal de bloque para un lote de cuatro imágenes con longitudes 256, 576, 729, 1024.`256^2 + 576^2 + 729^2 + 1024^2`entradas no cero.
   | 为四张长度分别为 256、576、729、1024 的图像构建块对角掩码。验证注意力矩阵为 2585x2585 且非零元素数精确为 `256^2 + 576^2 + 729^2 + 1024^2`。

3. Para una imagen 1792x896 en el parche 14, compare: (a) cuadrado-dimensionar a 336 y luego codificar, (b) AnyRes 2x1 + miniatura, (c) M-RoPE en nativo. ¿Cuál utiliza menos tokens? ¿Cuál conserva más detalles?
   | 对于 1792x896 的图像（补丁14），对比：(a) 缩放到336正方形，(b) AnyRes 2x1+缩略图，(c) M-RoPE 原始分辨率。哪种 token 最少？哪种保留最多细节？

4. Implemente la caída de parches fraccionados: dada una secuencia de paquetes, deje caer el 50% de los tokens de forma uniforme al azar, y actualice la máscara de diagonal de bloque en consecuencia.
   | 实现分数补丁丢弃：给定打包序列，随机均匀丢弃50%的token，更新块对角掩码，测量掩码稀疏度变化。

5. Leer la sección 3.2 del documento Qwen2-VL (arXiv:2409.12191).`min_pixels`y `max_pixels`control y por qué ambas fronteras importan.
   | 阅读 Qwen2-VL 论文第 3.2 节（arXiv:2409.12191）。用两句话描述 `min_pixels` 和 `max_pixels` 控制什么，为什么两个边界都很重要。

## Términos clave .

| Term | What people say | What it actually means | 中文含义 | 中文释义 |
|------|-----------------|------------------------|----------|---------|
| Patch-n'-pack | "NaViT-style packing" | Concatenate variable-length patch sequences from different images into one batch dimension | 将不同图像的可变长度补丁序列拼接到一个批次维度 | |
| Block-diagonal mask | "Packing mask" | Attention mask that confines each image's patches to attend only to themselves, not neighbors in the pack | 块对角掩码：限制每张图像的补丁只关注自身 | |
| AnyRes | "LLaVA-NeXT tiling" | Split a high-res image into a grid of fixed-size tiles plus a global thumbnail; encode every tile with a fixed encoder | 将高分辨率图像切分为固定大小网格+全局缩略图 | |
| NaFlex | "SigLIP 2 native-flex" | Single SigLIP 2 checkpoint that serves 256/729/1024-token budgets at inference without retraining | 单一 SigLIP 2 checkpoint 推理时支持多种 token 预算 | |
| M-RoPE | "Multimodal RoPE" | 3D rotary position encoding (time, row, column) that handles arbitrary H, W, T without position tables | 三维旋转位置编码（时间、行、列），处理任意宽高和时间长度 | |
| cu_seqlens | "FlashAttention packing" | Cumulative-length tensor the FlashAttention varlen path uses instead of a dense block-diagonal mask | FlashAttention 可变长度路径使用的累积长度张量 | |
| min_pixels / max_pixels | "Resolution bounds" | Qwen2.5-VL per-request knobs capping token count on very small or very large inputs | Qwen2.5-VL 按请求控制最小/最大像素数的参数 | |
| Visual token budget | "How many tokens per image" | Rough count of patch tokens emitted per image; sets the LLM's prompt budget and attention cost | 每张图像产生的补丁 token 数，决定 LLM 的提示预算和注意力成本 | |

## Más Leer más Leer más

- [Dehghani et al. — Patch n' Pack: NaViT (arXiv:2307.06304)](https://arxiv.org/abs/2307.06304)♬ NaViT Entrenamiento de resolución arbitraria
- [Wang et al. — Qwen2-VL (arXiv:2409.12191)](https://arxiv.org/abs/2409.12191) Qwen2-VL                                                                                                                                                                                                                                                            
- [Laurençon et al. — What matters when building vision-language models? (Idefics2, arXiv:2405.02246)](https://arxiv.org/abs/2405.02246) Los factores clave para construir VLM
- [Tschannen et al. — SigLIP 2 (arXiv:2502.14786)](https://arxiv.org/abs/2502.14786)Se le dio una vuelta a la puerta.
- [Qwen Team — Qwen2.5-VL Technical Report (arXiv:2502.13923)](https://arxiv.org/abs/2502.13923) Qwen2.5VL  informe técnico
