# Transformadores de visión y el primitivo de parches-tokens.

> Antes de cualquier cosa multimodal, una imagen tiene que convertirse en una secuencia de tokens que un transformador puede comer. El documento ViT 2020 respondió a esto con parches de 16x16 píxeles, una proyección lineal y una inserción de posición. Cinco años después cada modelo fronterizo de 2026 (Claude Opus 4.7 en 2576px nativo, Gemini 3.1 Pro, Qwen3.5-Omni) todavía comienza de esta manera  el codificador cambió de ViT a DINOv2 a SigLIP 2, se agregaron fichas de registro, el esquema posicional se convirtió en 2D-RoPE, pero el primitivo se mantuvo. Esta lección lee la línea de tokens de parches de extremo a extremo y lo construye en stdlib Python para que el resto de la Fase 12 tenga un modelo mental concreto para "tokens visuales".

> **【中文解读】**Antes de entrar en multimodus, las imágenes deben convertirse primero en un secuencia de tokens de procesamiento de Transformer. ViT utilizó bloques de imágenes 16x16 + proyección lineal + código de posición para lograr esta transformación, que es la base de todos los modelos de vanguardia hasta el día de hoy.

> **【拓展：ViT Patch→多模态基础】**El Patch-Token es la base de todos los modelos de lenguaje visual, ya sea en el código de vídeo de CLIP, o en el modelo de comprensión de archivos de LLaVA.

> ¿ Qué es esto ?**【前置】**Para aprender el proceso de desarrollo de la tecnología, el usuario debe tener en cuenta que el proceso de desarrollo de la tecnología de la tecnología de la tecnología de la tecnología de la tecnología de la tecnología de la tecnología de la tecnología de la tecnología de la tecnología de la tecnología de la tecnología de la tecnología de la tecnología de la tecnología de la tecnología de la tecnología de la tecnología de la tecnología de la tecnología de la tecnología de la tecnología de la tecnología de la tecnología de la tecnología de la tecnología de la tecnología de la tecnología de la tecnología de la tecnología de la tecnología de la tecnología de la tecnología de la tecnología de la tecnología de la tecnología de la tecnología de la tecnología de la tecnología de la tecnología de la tecnología de la tecnología de la tecnología de la tecnología de la tecnología de la tecnología de la tecnología de la tecnología de la tecnología de la tecnología de la tecnología de la tecnología de la tecnología de la tecnología de la tecnología de la tecnología de la tecnología de la tecnología de la tecnología de la tecnología de la tecnología de la tecnología de la tecnología de la tecnología de la tecnología de la tecnología de la tecnología de la tecnología de la tecnología de la tecnología de la tecnología de la tecnología de la tecnología de la tecnología de la tecnología de la tecnología de la tecnología de la tecnología de la tecnología de la tecnología de la tecnología de la tecnología de la tecnología de la tecnología de la tecnología de la tecnología de la tecnología de la tecnología de la tecnología de la tecnología de la tecnología de la tecnología de la tecnología de la tecnología de la tecnología de la tecnología de la tecnología de la tecnología de la tecnología de la tecnología de la tecnología de la tecnología de la tecnología de la tecnología de la tecnología de la tecnología de la tecnología de la tecnología de la tecnología de la tecnología de la tecnología de la tecnología de la tecnología de la tecnología de la tecnología de la tecnología de la tecnología de la tecnología de la tecnología de la tecnología de la tecnología de la tecnología de la tecnología de la tecnología de la tecnología de la tecnología de la tecnología de la tecnología de la tecnología de la tecnología de la tecnología de la tecnología de la tecnología de la tecnología de la tecnología de la tecnología de la tecnología de la tecnología de la tecnología de la tecnología de la tecnología de la tecnología de la tecnología de la tecnología de la tecnología de la tecnología de la tecnología de la tecnología de la tecnología de la tecnología de la tecnología de la tecnología de la tecnología de la tecnología de la tecnología de la tecnología de la tecnología de la tecnología de la tecnología de la tecnología de la tecnología de la tecnología de la tecnología

**Type:** Learn | **类型:** 学习
**Languages:** Python (stdlib, patch tokenizer + geometry calculator) | **语言:** Python（标准库，patch tokenizer + 几何计算器）
**Prerequisites:** Phase 7 (Transformers), Phase 4 (Computer Vision) | **前置知识:** Phase 7（Transformer），Phase 4（计算机视觉）
**Time:** ~120 minutes | **时间:** ~120 分钟

## Objetivos de aprendizaje

- Convierta una imagen HxWx3 en una secuencia de tokens de parches con codificación posicional correcta.
  China Translation:将 HxWx3 图像转换为带有正确位置编码的补丁代币序列──
- Calcule la longitud de la secuencia, el conteo de parámetros y los FLOP para un ViT de un dato (tamaño de parche, resolución, oscuridad oculta, profundidad).
  En inglés, el nombre de la secuencia de parches de la VT es el nombre de la secuencia de parches de la VT.
- Nombre de las tres actualizaciones que llevaron ViT de la investigación de 2020 a la producción de 2026: pre-entrenamiento auto supervisado (DINO / MAE), tokens de registro y embalaje de resolución nativa.
  China: 列举将 ViT From 2020研究推向 2026 年生产环境的三大升级:自监督预训练(DINO / MAE) 、registro token 和原生分辨率打包──
- Elija entre la agrupación CLS, la agrupación media, y registrar tokens para una tarea en el flujo posterior.
  China:                                                                                                                                                                                                                                                              

## El problema es la introducción del problema

Los transformadores operan en secuencias de vectores. El texto ya es una secuencia (bytes o tokens). Una imagen es una cuadrícula 2D de píxeles con tres canales de color  no una secuencia. Si se aplanan cada píxel, una imagen RGB 224x224 se convierte en 150.528 tokens, y la autoatención a esa longitud es un no iniciante (cuadrático en longitud de secuencia).

> El transformador obra es un secuencia de velocidades. El texto en sí mismo es un secuencia de caracteres, pero la imagen es una secuencia de tres colores. Si se extiende a cada secuencia, una imagen RGB de 224x224 se convierte en 150.528 símbolos, mientras que la auto-atención en esta longitud es imposible.

Los enfoques anteriores a 2020 empujaron un extractor de características de CNN en el frente: ResNet produce un mapa de características 7x7 de vectores de 2048 dimensiones, alimenta esos 49 tokens a un transformador. Esto funciona pero hereda los sesgos de CNN (equivalencia de traducción, campos receptivos locales) y pierde el apetito del transformador por la escala.

> El método anterior a 2020 fue el siguiente en el extremo anterior de un extractor de características de CNN: ResNet produjo un gráfico de características de dimensiones de 2048 de 7x7, que daría a los 49 tokens a Transformer. Esto era posible, pero heredó la inclusión de la CNN en la distribución de la variabilidad, y perdió el apetito de Transformer para expandir su tamaño.

Dosovitskiy y otros. (2020) hizo la pregunta directa: ¿qué pasa si saltamos la CNN? Dividir la imagen en parches de tamaño fijo (digamos 16x16 píxeles), proyectar linealmente cada parche en un vector, agregar una incorporación posicional y alimentar la secuencia a un transformador de vainilla. En ese momento esto era una visión hereje sin convulsiones. Con suficientes datos (JFT-300M, luego LAION) venció a ResNet en ImageNet y siguió mejorando.

> Dosovitskiy  et al. (2020) planteó un problema directo: si saltamos CNN, ¿se dividirá la imagen en parches de tamaño fijo (por ejemplo, 16x16), proyecta lineal cada parche en un vector, añade código de posición, y luego entrega la secuencia a Transformer estándar?

Para 2026, el ViT primitivo es la base indiscutible. la torre de visión de cada VLM de peso abierto es algún descendiente (DINOv2, SigLIP 2, CLIP, EVA, InternViT). La pregunta ya no es "¿deberíamos usar parches?" sino "qué tamaño de parche, qué horario de resolución, qué objetivo de preentrenamiento, qué codificación posicional".

> Para 2026, el ViT original ha sido indiscutible. Cada VLM de la plataforma de control de potencia abierta es su siguiente generación. La cuestión ya no es "¿¿no debería usar el parche?" sino "¿Qué parche? ¿Qué resolución de resolución? ¿Qué objetivos de entrenamiento? ¿Qué posición de codificación?"

## El concepto central.

> **【中文解读】**El Transformador de visión (ViT) dividirá la imagen en un parche de tamaño fijo (como 16x16 像素), cada parche 展平后通过线性投影变成一个代币,然后像NLP中的Transformer一样处理── esto será transformador 架构引入计算机视觉的奠基性工作,取代了CNN 成为视觉的脊柱──

> **【拓展：ViT 的影响】**Dosovitskiy  et al. Propuso en 2020 ViT prueba de transformador en la clasificación de imágenes puede superar CNN;. ViT-L/14 en la imagenNet alcanza el 88.5% de la tasa de precisión 1 ∞. ViT es la base de codificador de vídeo de CLIP, GPT-4V, Gemini, etc. Modelo de múltiples modelos.


> **【拓展：ViT 对 CNN 的优势】**La totalidad de ViT se auto-atención en la cantidad de datos suficiente tiempo (como JFT-300M o LAION-5B) significativamente mejor que la sensación local de CNN.


### Los parches como tokens

Dado una imagen `x`de forma`(H, W, 3)`y un tamaño de parche `P`, usted tallar la imagen en una cuadrícula de`(H/P) x (W/P)`Los parches no se superponen.`P x P x 3`Cubo de píxeles. Aplanar cada cubo a un`3 P^2`Aplicar una proyección lineal compartida `W_E`de forma`(3 P^2, D)`para mapear cada parche en la dimensión oculta del modelo `D`¿ Qué ?

> 给定形为 `(H, W, 3)`De imágenes `x`Y el parche`P`, se cortará la imagen para`(H/P) x (W/P)`个不重叠的补丁 网格── cada parche es uno `P x P x 3`de cuadros cuadrados.`3 P^2`维向量── aplicación forma为 `(3 P^2, D)`                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             `W_E`, cada parche se proyecta en la dimensión oculta del modelo`D`¿Qué es eso?

Para la configuración canónica de ViT-B/16:
- Resolución 224, tamaño de parche 16 → cuadrícula 14x14 → 196 tokens de parche.
  中文翻译:分辨率 224, parche 网格 14x14 → 196 个 parche token。
- Cada parche es`16 x 16 x 3 = 768`valores de píxeles, proyectados a `D = 768`¿ Qué ?
  中文翻译: cada parche 包含 `16 x 16 x 3 = 768`个像素值, proyección hasta `D = 768`¿Qué es eso?
- Añadir un aprendizaje `[CLS]`token → longitud de secuencia 197.
  China                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             `[CLS]`símbolo → 序列长度 197。

La proyección de parche es matemáticamente idéntica a una convolución 2D con tamaño del núcleo `P`, paso .`P`, y `D`Así es como el código de producción lo implementa realmente`nn.Conv2d(3, D, kernel_size=P, stride=P)`. El marco de la proyección lineal es conceptual; el marco del núcleo es eficiente.

> Patch  proyección en matemáticas es igual a la de la gran parte de la energía nuclear`P`、步长为 `P`、Exportación y transporte`D`La producción de código es así lo que se realiza.`nn.Conv2d(3, D, kernel_size=P, stride=P)`La "proyección lineal" es conceptual; la realización de la secuencia nuclear es altamente eficaz.

### Embedings de posición

Los parches no tienen orden inherente  el transformador los ve como una bolsa. los primeros viTs añadieron una incorporación posicional 1D aprendizable (un vector de 768 dimensiones por posición, 197 de ellos). Funciona, pero vincula el modelo a la resolución de entrenamiento: en la inferencia tienes que interpolar la tabla de posición si cambias la cuadrícula.

> El parche  no tiene orden fijo El transformador los considera como un conjunto sin orden  Los primeros viT  añadieron un código de posición 1D de aprendizaje  Cada posición un 768 维向量,共 197 个)  (código de parche 没有固定的顺序)  (código de posición)  (código de posición) )  (código de parche 没有固定的顺序)  (código de posición)  (código de posición) )  (código de posición)  (código de posición) )  (código de posición)  (código de posición)  (código de posición)  (código de posición)  (código de posición)  (código de posición)  (código de posición)  (código de posición)  (código de posición)  (código de posición)  (código de posición)  (código de posición)  (código de posición)  (código de posición)  ()  ()  ()  ()  ( ()  ()  ()  ()  ()  ()  ()  ()  ()  ()  () )  ()  ()  ()  ()  () )  ()  ()  ()  ()  ()  ()  () ) ()  ()  () ) ()  () () () () () () () () () () () () () () () ()

Las espinas de visión modernas utilizan 2D-RoPE (M-RoPE de Qwen2-VL, por defecto de SigLIP 2) o posiciones 2D factorizadas. 2D-RoPE gira la consulta y los vectores clave basados en el índice del parche (fila, columna), por lo que el modelo infere la posición 2D relativa desde el ángulo de rotación. No hay tabla de posición. El modelo maneja tamaños de cuadrícula arbitrarios a la inferencia.

> 现代视觉主干网络使用2D-RoPE(Qwen2-VL de M-RoPE、SigLIP 2 的默认方案) o descompuesto 2D 位置编码──2D-RoPE De acuerdo con el parche de la ↓ 行列) Indicación de la consulta de rotación 和 clave向量, por lo que el modelo de la posición de rotación de la hipótesis en relación con la posición 2D──无需位置表──模型在推理时可以处理任意网格大小──

### Tokens CLS, salida conjunta y registros

¿Qué es la representación a nivel de imagen? Tres opciones coexisten:

> ¿Qué es la imagen?

1. `[CLS]`token. prepárate un vector de aprendizaje a la secuencia de parches. Después de todos los bloques transformadores, el estado oculto del token CLS es la representación de imagen. heredada de BERT. utilizada por ViT original, CLIP.
   En inglés:`[CLS]`token── en parche 序列前拼接一个可学习向量── después de todos los bloques de transformador, el estado oculto del token CLS es el de la imagen.
2. Media de los estados ocultos de salida de los tokens de parche, utilizado por SigLIP, DINOv2, la mayoría de los VLM modernos.
   China Translation:均值池化──对所有补丁代币的输出隐藏状态取平均──SigLIP、DINOv2 和大多数现代VLM使用──
3. Las señales de registro. Darcet et al. (2023) observaron que las VTs entrenadas sin un token de fregadero explícito desarrollan parches de "artefactos" de alta norma que secuestran la autoatención.
   China Translation:Register token──Darcet 等人(2023) observado, sin un token de汇聚显式的ViT 会产生高范数"伪影"patch,劫持自注意力──添加4-16个可学习的注册代币可以吸收这种负载,提高密集预测质量(分分、深度)──DINOv2 和 SigLIP 2 都带有注册──

La elección importa para las tareas en el flujo posterior. CLS es bueno para la clasificación. Para VLMs que alimentan tokens de parches en un LLM, se omite la puesta en común por completo  cada parche se convierte en un token de entrada de LLM. Los registros se desechan antes de la entrega (son andamios, no contenido).

> 选择对下游任务很重要──CLS 适合分类──对于将补丁代币进入LLM的VLM,完全跳过池化每个补丁都成为LLM的输入代币──Register在交接前被丢弃(它们是脚手架,不是内容)──

### Preentrenamiento: supervisado, contrastivo, enmascarado, auto-destilado

El ViT 2020 fue preentrenado con clasificación supervisada en JFT-300M. Rápidamente sustituido por:

> El año 2020 de ViT en JFT-300M 上用监督分类进行预训――很快被以下方法取代:

- CLIP (2021): texto de imagen contrastable en 400M pares. Lección 12.02.
  China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China:
- MAE (2021, He et al.): enmascarar el 75% de los parches, reconstruir los píxeles. Auto supervisado, trabaja en imágenes puras.
  En el caso de los modelos de imagen, el modelo de imagen de la imagen es el modelo de imagen de la imagen de la imagen.
- DINO (2021) / DINOv2 (2023): auto-distillación con estudiante-maestro, sin etiquetas, sin encabezados. La DINOv2 ViT-g/14 2023 es la columna vertebral puramente visual más fuerte y el estándar para los casos de uso de "características densas".
  En el año 2023, DINOv2 ViT-g/14 es la red principal de pure visión más fuerte, también es "tratuete intenso" de uso de ejemplos de la elección de la forma de la imagen.
- SigLIP / SigLIP 2 (2023, 2025): CLIP con pérdida sigmoide y NaFlex para la relación de aspecto nativa. La torre de visión dominante en 2026 VLM abiertos (Qwen, Idefics2, LLaVA-OneVision).
  China: SigLIP / SigLIP 2(2023,2025): uso sigmoide 损失和 NaFlex 原生宽高比的 CLIP──2026年开放 VLM(Qwen、Idefics2、LLaVA-OneVision) 主导视觉塔──

Su elección de la preparación determina para qué es buena la columna vertebral: CLIP/SigLIP para la combinación semántica con el texto, DINOv2 para características visuales densas, MAE como punto de partida para la regulación de la línea baja.

> 预训练方式决定主干网络擅长什么:CLIP/SigLIP se utiliza para adaptarse al texto,DINOv2 se utiliza para el contenido de la imagen,MAE se utiliza como punto de partida de la subyacción de la configuración.

### Leyes de escala

La escalación de ViT (Zhai et al. 2022) estableció que la calidad de un ViT obedece a leyes predecibles en tamaño de modelo, tamaño de datos y computación.

> ViT 缩放定律(Zhai 等人,2022) estableció la calidad de ViT siguiendo sobre el modelo de tamaño, tamaño de datos y la regla de cálculo predecible de la cantidad de:

- Un modelo más grande + más datos → mejor calidad.
  Más grandes modelos + más datos → mejor calidad。
- El tamaño del parche es un palanca en la longitud de la secuencia frente a la fidelidad. El parche 14 (típico de DINOv2/SigLIP SO400m) da más tokens por imagen que el parche 16; mejor para las tareas OCR y densas, peor para la velocidad.
  Patch:PATCH 大小是序列长度与保真度之间的杆──Patch 14(DINOv2/SigLIP SO400m 的典型配置) Más de 16 parches cada uno de los cuadros generan más tokens; más adecuado para OCR y tareas densas, pero la velocidad es más lenta──
- La resolución es la otra gran palanca. Ir de 224 a 384 a 512 casi siempre ayuda, a un costo cuadrático en FLOPs.
  La resolución es otro importante eje. Desde 224 se eleva a 384 y hasta 512 casi siempre ayuda, pero los FLOP se producen en un segundo aumento.

ViT-g/14 (1B params, parche 14, resolución 224 → 256 tokens) y SigLIP SO400m/14 (400M params, parche 14) son los dos codificadores de trabajo para 2026 VLM abiertos.

> ViT-g/14(10 mil millones de parámetros, parche 14, resolución 224 → 256 tokens) y SigLIP SO400m/14(4 mil millones de parámetros, parche 14) son los dos principales codificadores de VLM abiertos para el año 2026―

### El número de parámetros para un ViT

El cálculo completo se realiza en`code/main.py`Para ViT-B/16 en el 224:

> 完整计算见 `code/main.py`❖ Para ViT-B/16 en 224 resolución:

```
patch_embed = 3 * 16 * 16 * 768 + 768  =  591k
cls + pos    = 768 + 197 * 768          =  152k
block        = 4 * 768^2 (QKVO) + 2 * 4 * 768^2 (MLP) + 2 * 2*768 (LN)
             = 12 * 768^2 + 3k          =  7.1M
12 blocks    = 85M
final LN    = 1.5k
total       ≈ 86M
```

Estajando cada VT de esta manera antes de cargar el punto de control.

> Antes de la carga de un punto de control, se utiliza este método para calcular cada VT.

### Configuración de producción 2026

El codificador más abierto que VLMs envían en 2026 es SigLIP 2 SO400m/14 en resolución nativa (NaFlex).

> La mayoría de los editores de VLM 搭载 2026 años son originales en resolución de NaFlex (siglip 2 SO400m/14).

- Parámetros de 400M.
  En el caso de los niños, el número de niños en edad avanzada es de aproximadamente 5 millones.
- Tamaño de parche 14, resolución predeterminada 384 → 729 parches de tokens por imagen.
  Patch                                                                                                                                                                                                                                                              
- Pozo medio para tareas de nivel de imagen; todos los 729 parches fluyen al LLM para VQA.
  Traducción:Imagen Clasificación de tareas de uso de la media de valor; todos los 729 parches 流入 LLM 进行视觉问答。
- 4 fichas de registro, desechadas antes de la entrega de LLM.
  En el caso de los estudiantes de la Universidad de Nueva York, el registro de los estudiantes de la Universidad de Nueva York es el siguiente:
- 2D-RoPE con escalación a nivel de imagen para la relación de aspecto nativa.
  Traducción:D-RoPE, con cuadros reducidos para apoyar el tamaño de la vida original.

Cada decisión en ese archivo remonta a un periódico que puedes leer.

> Cada decisión de la configuración se puede remontar a los artículos que puedes leer.

## Usalo con el marco de ejecución
```figure
image-patch-tokens
```

## Usalo

`code/main.py`Es un tokenizador de parches y calculadora de geometría. toma (imagen H, W, parche P, oculto D, profundidad L) y informa:

> `code/main.py`Es un tokenizador de parche 和几何计算器──它接收(图像 H, W, parche P, 隐藏维度 D, 深度 L)并报告:

- Forma de la rejilla y longitud de la secuencia después de la corrección.
  En la página de la página de la página de la página de la página de la página de la página de la página de la página de la página de la página de la página de la página de la página de la página de la página de la página de la página de la página de la página de la página de la página de la página de la página de la página de la página de la página de la página de la página de la página de la página de la página de la página de la página de la página de la página de la página de la página de la página de la página de la página de la página de la página de la página de la página de la página de la página de la página de la página de la página de la página de la página de la página de la página de la página de la página de la página de la página de la página de la página de la página de la página de la página de la página de la página de la página de la página de la página de la página de la página de la página de la página de la página de la página de la página de la página de la página de la página de la página de la página de la página de la página de la página de la página de la página de la página de la página de la página de la página de la página de la página de la página de la página de la página de la página de la página de la página de la página de la página de la página de la página de la página de la página de la página de la página de la página de la página de la página de la página de la página de la página de la página de la página de la página de la página de la página de la página de la página de la página de la página de la página de la página de la página de la página de la página de la página de la página de la página de la página de la página de la página de la página de la página de la página de la página de la página de la página de la página de la página de la página de la página de la página de la página de la página de la página de la página de la página de la página de la página de la página de la página de la página de la página de la página de la de la página de la página de la página de la página de la de la página de la de la de la de la de la de la de la de la de la de la de la de la de la de la de
- Secuencia de fichas para una imagen de juguete sintética de 8x8 píxeles (caminar por la ruta plana + proyecto).
  Sinopsis: Sinopsis 8x8 像素玩具图像的代币序列 遍历展平 + 投影路径)
- El recuento de parámetros se desglosó por inserción de parche, inserción de posición, bloques de transformador y cabeza.
  Traducción:en función de parche 嵌入、位置编码、Transformer 块和头分解的参数──
- Los FLOP por paso hacia adelante en la resolución objetivo.
  La información de la información se puede obtener en el sitio web de la empresa.
- Una tabla de comparación en ViT-B/16 @ 224, ViT-L/14 @ 336, DINOv2 ViT-g/14 @ 224, SigLIP SO400m/14 @ 384.
  En el texto original, el texto se traduce en inglés como "Vit-B/16 @ 224、ViT-L/14 @ 336、DINOv2 ViT-g/14 @ 224、SigLIP SO400m/14 @ 384 的对比表──

Ejecutar. Combinar el parámetro cuenta con los números publicados. Jugar con el tamaño del parche y la resolución para sentir el costo de cuenta de tokens.

> 运行它――将参数与发布数据对比――调整补丁大小和分辨率来感受代币数量成本――

## Envíe el producto .

Esta lección produce`outputs/skill-patch-geometry-reader.md`. Dado una configuración ViT (tamaño de parche, resolución, oscuridad oculta, profundidad), produce un recuento de tokens, recuento de parámetros y estimación VRAM con justificaciones.

> 本课产 出  `outputs/skill-patch-geometry-reader.md` Dado el ViT  configuración  parche  tamaño  resolución  escondido  profundidad  profundidad), genera tokens  cantidad  parametros y  estimación de la memoria y su base  cada vez que se utiliza esta habilidad para VLM                                                                                                                                                                                                                                                                                                                                                                                                                                                          

## Los ejercicios.

1. Calcule la longitud de la secuencia de tokens de parche para Qwen2.5-VL en entrada nativa 1280x720 con tamaño de parche 14. ¿Cómo se compara eso con una representación solo CLS?
   En inglés, el nombre de la marca de la marca de marca de marca de marca de marca de marca de marca de marca de marca de marca de marca de marca de marca de marca de marca de marca de marca de marca de marca de marca de marca de marca de marca de marca de marca de marca de marca de marca de marca de marca de marca de marca de marca de marca de marca de marca de marca de marca de marca de marca de marca de marca de marca de marca de marca de marca de marca de marca de marca de marca de marca de marca de marca de marca de marca de marca de marca de marca de marca de marca de marca de marca de marca de marca de marca de marca de marca de marca de marca de marca de marca de marca de marca de marca de marca de marca de marca de marca de marca de marca de marca de marca de marca de marca de marca de marca de marca de marca de marca de marca de marca de marca de marca de marca de marca de marca de marca de marca de marca de marca de marca de marca de marca de marca de marca de marca de marca de marca de marca de marca de marca de marca de marca de marca de marca de marca de marca de marca de marca de marca de marca de marca de marca de marca de marca de marca de marca de marca de marca de marca de marca de marca de marca de marca de marca de marca de marca de marca de marca de marca de marca de marca de marca de marca de marca de marca de marca de marca de marca de marca de marca de marca de marca de marca de marca de marca de marca de marca de marca de marca de marca de marca de marca de marca de marca de marca de marca de marca de marca de marca de marca de marca de marca de marca de marca de marca de marca de marca de marca de marca de marca de marca de marca de marca de marca de marca de marca de marca de marca de marca de marca de marca de marca de marca de marca de marca de marca de marca de marca de marca de marca de marca de marca de marca de marca de marca de marca de marca de marca de marca de marca de marca de marca de marca de marca de marca de marca de marca de marca de marca de marca de marca de marca de marca de marca de marca de marca de marca de marca de marca de marca de marca de marca de marca de marca de marca de marca de marca de marca de marca de marca de marca de marca de marca de marca de marca de marca de marca de marca de marca de

2. ¿Cuántos tokens producen un fotograma 1080p (1920x1080) en el parche 14? ¿A 30 FPS en un video de 5 minutos, cuántos tokens visuales totales? ¿Cuál es el costo más ahorrado: pooling, muestreo de fotogramas o fusión de tokens?
   China 翻译:一 1080p 图像(1920x1080) ¿Cuántos tokens se producen en el parche 14? ¿Con 30 FPS 播放 5 分钟视频,总共多少视觉 token? ¿Qué método ahorra más el costo:池化、采样还是 token 合并?

3. Implementar el pool medio sobre tokens de parches en Python puro. Verifique que el pool medio sobre 196 tokens de una salida DINOv2 coincide con lo que el modelo `forward`regresa cuando usted pide una incorporación conjunta.
   China 翻译:用纯Python 实现补丁代币的平均值池化――验证对 DINOv2 输出的196代币做平均值池化是否与模型 `forward`                                                                                                                                                                                                                                                              

4. Lea la sección 3 de "Los transformadores de visión necesitan registros" (arXiv:2309.16588). Describa en dos frases qué artefacto absorben los registros y por qué es importante para la predicción densa aguas abajo.
   La versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión de la versión original de la versión de la versión de la versión original de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de 2010 de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de 2010 de la versión de la versión de la versión de la versión de la versión de la versión de 2010 de la versión de la versión de la versión de la versión de la versión de la versión de 2010 de la versión de la versión de la versión de la versión de la versión de 2010 de la versión de la versión de la versión de la versión de la versión de la versión de 2010 de la versión de la versión de la versión de 2010 de la versión de la versión de 2010 de la versión de la versión de la versión de la versión de la versión

5. Modificar`code/main.py`Para soportar el parche-n'-pack: dada una lista de imágenes de diferentes resoluciones, produzca una sola secuencia de paquetes y la máscara de atención de diagonal de bloque.
   Traducción:Mudificación`code/main.py`Es compatible con el parche-n'-pack: dado un conjunto de imágenes de diferentes resoluciones, generar una serie de pacotes y bloques para cubrir la atención en los rincones.

## Términos clave .

| Term | What people say | What it actually means | 中文释义 |
|------|----------------|------------------------|---------|
| 术语 | 通俗说法 | 实际含义 | |
| Patch | "16x16 pixel square" | A fixed-size non-overlapping region of the input image; becomes one token | 固定大小的非重叠图像区域；成为一个 token |
| Patch embedding | "Linear projection" | A shared learned matrix (or Conv2d with stride=P) mapping flattened patch pixels to D-dim vectors | 共享的学习矩阵（或步长为 P 的 Conv2d），将展平的 patch 像素映射为 D 维向量 |
| CLS token | "Class token" | Prepended learnable vector whose final hidden state represents the whole image; optional in 2026 | 前置可学习向量，其最终隐藏状态代表整张图像；2026 年可选 |
| Register token | "Sink token" | Extra learnable tokens that absorb the high-norm attention artifacts ViTs develop during pretraining | 额外可学习 token，吸收 ViT 预训练中产生的高范数注意力伪影 |
| Position embedding | "Positional info" | Per-position vector or rotation making the sequence-order-aware; 2D-RoPE is the modern default | 每个位置的向量或旋转，使序列具有顺序感知；2D-RoPE 是现代默认方案 |
| Grid | "Patch grid" | The (H/P) x (W/P) 2D array of patches for a given resolution and patch size | 给定分辨率和 patch 大小下的 (H/P) x (W/P) 2D patch 数组 |
| NaFlex | "Native flexible resolution" | SigLIP 2 feature: single model serves multiple aspect ratios and resolutions without retraining | SigLIP 2 特性：单一模型服务多种宽高比和分辨率，无需重新训练 |
| Backbone | "Vision tower" | The pretrained image encoder whose patch-token outputs feed the LLM in a VLM | 预训练的图像编码器，其 patch-token 输出喂入 VLM 中的 LLM |
| Pooling | "Image-level summary" | Strategy to turn patch tokens into one vector: CLS, mean, attention pool, or register-based | 将 patch token 转为一个向量的策略：CLS、均值、注意力池化或基于 register |
| Patch 14 vs 16 | "Finer vs coarser grid" | Patch 14 produces more tokens per image, better fidelity for OCR, slower; patch 16 is the classic default | Patch 14 每张图产生更多 token，OCR 保真度更高但更慢；patch 16 是经典默认值 |

## Más Leer más Leer más

- [Dosovitskiy et al. — An Image is Worth 16x16 Words (arXiv:2010.11929)](https://arxiv.org/abs/2010.11929) ViT original.
  El texto original de la traducción de la lengua china es "Vídeo".
- [He et al. — Masked Autoencoders Are Scalable Vision Learners (arXiv:2111.06377)](https://arxiv.org/abs/2111.06377) MAE, auto-supervisión de la preparación.
  En inglés, "Má" es el nombre de la lengua inglesa.
- [Oquab et al. — DINOv2 (arXiv:2304.07193)](https://arxiv.org/abs/2304.07193) Auto-destilación a escala, sin etiquetas.
  La lengua inglesa se traduce en inglés como "la lengua de la lengua" (en inglés: "la lengua de la lengua")
- [Darcet et al. — Vision Transformers Need Registers (arXiv:2309.16588)](https://arxiv.org/abs/2309.16588) registro de tokens y análisis de artefactos.
  Sinopsis: El nombre de la persona que se encuentra en el registro de la ciudad.
- [Tschannen et al. — SigLIP 2 (arXiv:2502.14786)](https://arxiv.org/abs/2502.14786) la torre de visión predeterminada de 2026.
  Traducción:El año de la muerte de Jesús en el siglo XX.
- [Zhai et al. — Scaling Vision Transformers (arXiv:2106.04560)](https://arxiv.org/abs/2106.04560) leyes empíricas de escala.
  En español: experiencia en la práctica.
