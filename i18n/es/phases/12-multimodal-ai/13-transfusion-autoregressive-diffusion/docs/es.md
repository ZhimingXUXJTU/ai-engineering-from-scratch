# Transfusión: texto autoregreso + difusión imagen en un transformador .

> Cameleon y Emu3 apostaron todo en tokens discretos. Funcionan, pero el cuello de botella de cuantificación es visible  las mesetas de calidad de imagen debajo de los modelos de difusión en el espacio continuo. La transfusión (Meta, Zhou et al., agosto 2024) toma la apuesta opuesta: mantener las imágenes continuas, dejar caer el VQ-VAE por completo y entrenar a un transformador con dos pérdidas. Los tokens de texto obtienen la predicción de los próximos tokens. Los parches de imagen obtienen una pérdida de flujo de coincidencia / difusión. Ambos objetivos optimizan los mismos pesos. La arquitectura subyacente a la Stable Diffusion 3 (MMDiT) es una prima cercana. Esta lección lee la tesis de Transfusión, construye un entrenador de juguete de dos pérdidas y rastrea la máscara de atención que permite a un transformador hacer ambos trabajos.

> **【中文解读】**Transfusión(Meta,2024年8月) eligió el camino contrario con Chameleon/Emu3: mantener imágenes para continuar, sin necesidad de VQ-VAE, con un Transformer, simultáneamente correr dos pérdidas texto token con el siguiente token 预测, imágenes rectificadas con流匹配/扩散损失──Stable Diffusion 3 de la estructura de MMDiT es muy cerca──

> **【拓展：双损失训练的工程挑战】**El punto central de la fusión consiste en equilibrar las funciones de pérdida diferentes de dos dimensiones numéricas. La diferencia de la cantidad de pérdida de NTP y la expansión de MSE puede conducir a un entrenamiento de gestión de pérdida.

**Type:** Build  | **类型:** 构建
**Languages:** Python (stdlib, two-loss trainer on MNIST-scale toy) | **语言:** Python（标准库，MNIST 规模玩具的双损失训练器）
**Prerequisites:** Phase 12 · 11 (Chameleon), Phase 8 (Generative AI) | **前置知识:** Phase 12 · 11（Chameleon），Phase 8（生成式 AI）
**Time:** ~180 minutes | **时间:** ~180 分钟

> ¿ Qué es esto ?**【前置】**学本节前请先掌握:Fase 12·11(Chameleon 离散代币) 、Fase 12·12(Emu3 next-token 生成) 、Fase 8·01-03(扩散模型 / Flow Matching) ‧Transfusión = 两套思路的融合:文本离散 + 图像连续,一个变压器 两个损失──
> ¿ Qué es esto ?**【类比】**Transfusión = "双拼户型"──Chameleon = 一室室(todo el contenido con el mismo token);LLaVA = 联排别(视觉和文本完全分开,靠桥接连接);Transfusión = 双拼(一边文本下一个代号的损失,一边图像扩散损失,共享承重墙 = 同一个变压器 骨干)── dos pérdidas comúnmente optimizan un conjunto de参数, conservan sus propias ventajas de modelo.
> ️ **【易错点】**两个损失直接相加而不调权重 → 一个损失主导训练(usually spread MSE 数值大,文本 NTP被淹没) ――修复:Use loss weighting(如 λ_text=1.0, λ_image=0.1) o GradNorm自适应平衡──

## Objetivos de aprendizaje

- Envía un transformador que ejecuta dos pérdidas (NTP en tokens de texto, MSE de difusión en parches de imagen) en una columna vertebral.
  > Construir un transformador que pueda correr en el mismo tronco con dos pérdidas (NTP + parche de imagen  MSE)
- Explica por qué la atención bidireccional entre parches de imagen más la atención causal sobre tokens de texto es la elección correcta de máscara.
  > Explica por qué "imagen patch 双向 + 文本代币因果" es la opción de ocultamiento correcta.
- Comparar el estilo Transfusión (imágenes continuas, pérdida de difusión) con el estilo Chameleon (imágenes discretas, NTP) en computación, calidad y complejidad de código.
  > Comparado con el modelo de transfusión 风格 (连续图像、扩散损失) y el modelo de camaleón 风格 (离散图像、NTP) en la capacidad de cálculo, calidad y complejidad de código.
- Nombre de la contribución de MMDiT: pesas específicas de modalidad en cada bloque, atención conjunta en el flujo residual.
  > 列举 MMDiT's contributions: Modelo de cada bloque de un determinado peso, diferencia y unidad de atención.

## El problema es el contexto del problema

El debate entre los tokens de imagen discretos y continuos es más antiguo que los LLM. Las representaciones continuas (pixeles crudos, VAE latente) conservan el detalle.

> 离散与连续图像代币的争论比 LLM 更早──连续表示(原始像素、VAE 潜变量)保留细节──离散代币(VQ索引) se ajusta al transformer's original词汇表, pero en la medida en que los pasos perdidos detalle──

Caméleo / Emu3 fue discreto: una pérdida, una arquitectura, pero la fidelidad de la imagen se limitó por la calidad del tokenizer.

> Caméleo / Emu3 选择离散: una pérdida, una estructura, pero la seguridad de imágenes está limitada a la calidad de los componentes.

Los modelos de difusión fueron continuos: calidad de imagen excepcional, pero un modelo separado del LLM, ingeniería compleja de horarios de ruido y ninguna integración limpia con la generación de texto.

> 扩散模型选择连续:卓越的图像质量, pero con LLM es un modelo independiente, requiere un complejo diseño de ajuste de ruido, no puede generar un contenido de texto en forma integrada.

La transfusión pregunta: ¿podemos tener ambas? Mantener las imágenes continuas, seguir entrenando un modelo, usar dos pérdidas cosidas en un paso de gradiente.

> ¿Podría hacerse con dos? Mantener imágenes continuas, todavía entrenar un modelo, con dos pérdidas en un paso de escala.

## El concepto central.

> **【中文解读】**Transfusion(Meta) se volverá a regar en el texto generar y difundir modelos de imágenes generar fusión en el mismo Transformer En: texto token Uso de la siguiente señal de predicción pérdida, imágenes token Uso de pérdida de difundir.

> **【拓展：多模态训练目标的融合】**Transfusión  prueba de auto-regulación y expansión puede existir en el mismo modelo y  compartición                                                                                                                                                                                                                                                   


### La arquitectura de dos pérdidas

Un único transformador de decodificación sólo procesa una secuencia que contiene:

> 单一解码器 Transformer 处理 contiene el siguiente contenido de la serie:

- Tokens de texto (discreto, de la vocabla BPE).
  En el caso de los ejemplos de la lengua inglesa, el nombre de la lengua inglesa es "B.P.E".
- Parches de imagen (continua, bloques de píxeles 16x16 proyectados en oscuridad oculta a través de la incorporación lineal  igual que la entrada de un codificador ViT).
  En el caso de los parches de imágenes, el bloque de imágenes de 16x16 es el mismo que el de las imágenes de las imágenes de las imágenes de las imágenes.
- `<image>`y `</image>`etiquetas que marcan donde viven los parches continuos.
  En inglés:`<image>`Y `</image>`标签标记连续补丁的位置──

El pase delantero se ejecuta una vez. La pérdida elige una de dos cabezas por token:

> Antes de la difusión, una vez, perdemos por cada token.

- Para los tokens de texto: entropía cruzada estándar en la cabeza de los logitos de vocabulario.
  En el texto de la traducción de la palabra "simbolismo" se escribe el texto "simbolismo" en el texto de la palabra "simbolismo".
- Para parches de imagen: pérdida de difusión en parches continuos  predecir el ruido que se añadió a cada parche.
  Traducción:Imagen patch:连续 patch 上的扩散损失预测 Cada parche 添加的噪音──

El gradiente fluye a través del cuerpo del transformador compartido. Ambas pérdidas mejoran los pesos compartidos simultáneamente.

> 梯度通过共享的变压器 体回流―― dos pérdidas al mismo tiempo que mejorar el derecho de compartir

### Máscara de atención: texto causal + imagen bidireccional

Los tokens de texto deben ser causales  no se puede dejar que un token de texto atenda a un texto futuro, o que el profesor obligue a los descansos.

> 文本代币 必須是因果的不能让文本代币 关注未来文本,否则教师强制会失败――但图像补丁代表一个快照; deben estar en el mismo bloque de imágenes, ambos se centran el uno en el otro――

La máscara:

> 掩码:

```
M[i, j] = 1 if:
  (i is text and j is text and j <= i)   # causal for text
  OR (i is image and j is image and same_image_block(i, j))   # bidirectional within image
  OR (i is text and j is image and j < i_image_end)   # text attends to previous images
  OR (i is image and j is text and j < i_image_start)   # image attends to preceding text
```

Implementado como una máscara triangular en el entrenamiento y la inferencia.

> En el entrenamiento y la reflexión, se realiza para el bloque.

### Perdida de difusión dentro del transformador

La pérdida de difusión es estándar: añadir ruido a un parche de imagen, pedir al modelo que predica el ruido (o el parche limpio, equivalentemente).

> 扩散损失是标准的: 给图像补丁 添加噪音,让模型预测噪音(或等价地预测干净补丁) ――Transfusión 版本使用流匹配预测从噪音到干净的速度场──

Durante la formación:
1. Para cada parche de imagen x0, muestra un paso de tiempo aleatorio t.
   Por ejemplo, el tiempo que pasa en el tiempo es el tiempo que pasa en el tiempo.
2. Muestra de ruido ε, calcular xt = (1-t) * x0 + t * ε (interpolación lineal para la coincidencia de flujo).
   En el caso de los sistemas de control de la información, el sistema de control de la información puede ser utilizado para determinar el valor de la información.
3. El transformador predice v_theta(xt, t); pérdida = MSE(v_theta(xt, t), ε - x0).
   En el texto original, el texto se basa en el texto de la traducción de la traducción de la traducción de la traducción de la traducción de la traducción de la traducción de la traducción de la traducción de la traducción de la traducción de la traducción de la traducción de la traducción de la traducción de la traducción de la traducción de la traducción de la traducción de la traducción de la traducción de la traducción de la traducción de la traducción de la traducción de la traducción de la traducción de la traducción de la traducción de la traducción de la traducción de la traducción de la traducción de la traducción de la traducción de la traducción de la traducción de la traducción de la traducción de la traducción de la traducción de la traducción de la traducción de la traducción de la traducción de la traducción de la traducción de la traducción de la traducción de la traducción de la traducción de la traducción de la traducción de la traducción de la traducción de la traducción de la traducción de la traducción de la traducción de la traducción de la traducción de la traducción de la traducción de la lengua inglesa.
4. La retroprop junto con el texto NTP pérdidas de la misma secuencia.
   Sinopsis: El texto de la serie se transmite en el sentido contrario.

En la inferencia, la generación es:
- Tokens de texto: muestreo autorregresor estándar.
  En el caso de los ejemplos de la lengua inglesa, el nombre de la lengua inglesa es "Categoría de la lengua inglesa".
- Parches de imagen: bucle de muestreo de difusión (10-30 pasos típicos) condicionado a los tokens de texto anteriores.
  En la actualidad, el sistema de parche de imágenes es un sistema de parche de imágenes.

### MMDiT: Variante de la difusión estable 3

Estable Diffusion 3 (Esser et al., marzo 2024) envió MMDiT (Transformador de Diffusión Multimodal) aproximadamente al mismo tiempo que Transfusión.

> Estable Diffusion 3 (Esser 等人,2024 年 3 月) publicó MMDiT (多模态扩散变压器), con Transfusion 差不多同时──两者架构是兄弟──

Las diferencias clave del MMDiT:

> Los siguientes son los principales factores de la MMDiT:

- Peso específico de modalidad por bloque. Cada bloque de transformador tiene pesos separados Q, K, V y MLP para tokens de texto frente a parches de imagen.
  China Translation: cada bloque tiene un peso específico. Cada bloque de transformador tiene un peso específico.
- Una variante específica de flujo de coincidencia con muestreo conocido y matemáticas más simples que DDPM.
  En la actualidad, el sistema de matemáticas es más simple que el DDPM.
- Escala. MMDiT es la columna vertebral de SD3 (2B y 8B variantes param).
  La dimensión de la MDDT es la principal de la SD3 (en inglés: SMDT) y la dimensión de la MDDT es de los 20 mil millones y los 80 mil millones de cambios en los números.

Ambos convergen en la misma idea central: un transformador ejecuta NTP en texto y difusión en representaciones continuas de imágenes.

> 两者收到同一核心理念: un transformador en el texto en funcionamiento NTP, en la imagen en continuidad en el funcionamiento en expansión.

### ¿Por qué esto es mejor que el estilo del camaleón?

La brecha de calidad entre la difusión continua y la NTP discreta en la generación de imágenes es medible.

>  Continuous diffusion and dispersed NTP en la generación de imágenes es calibrable.

- En parámetros 7B, supera un modelo de estilo camaleón del mismo tamaño en FID en 3-5 puntos.
  China: 70 mil millones de dólares bajo la base de la FID.
- No se requiere entrenamiento de tokenizer  el codificador de imagen es más simple (proyección lineal a oculta, igual que la capa de entrada de un ViT).
  Traducción:No necesita un entrenamiento de los elementos de la imagen.
- La inferencia puede paralelalizar la denotación de parches de imagen, a diferencia de los tokens de imagen autoregresivos.
  Traducción:Tú理可以并行化图像补丁 去噪, diferente a los símbolos de la imagen auto-regreso.

Desventaja: La transfusión es un modelo de doble pérdida, lo que hace que la dinámica de entrenamiento sea más complicada. Los pesos de pérdida necesitan ajuste.

> 缺点:Transfusión es un modelo de doble pérdida, el entrenamiento de los movimientos es más complejo.

### Lo que se encuentra río abajo

Janus-Pro (lección 12.15) perfecciona la idea de Transfusion descoplando el codificador de visión para la comprensión y generación  SigLIP para uno, VQ para el otro  mientras comparte el cuerpo del transformador. Show-o (lección 12.14) cambia la difusión por difusión discreta (predicción enmascarada).

> Janus-Pro (Janu­s-Pro) (n.o 12.15) mediante la resolución de la visión codificador mejoró la idea de la Transfusión (SigLIP) para entender, VQ para generar y compartir a la vez Transformer 主体──Show-o (n.o 12) (n.o 12.14) se difundirá en lugar de difundir en lugar de difundir en lugar de difundir en lugar de difundir en lugar de difundir (n.o.o.o.o.)

Los VLM de producción 2026 que emiten imágenes  Gemini 3 Pro, GPT-5, Claude Opus 4.7's imagen generation path  casi seguramente utilizan algún descendiente de esta familia.

> 2026 años de producción de imágenes VLMGemini 3 Pro、GPT-5、Claude Opus 4.7 de la producción de imágenes de la ruta  casi se puede determinar que se utilizó algún tipo de posterior generación de esta familia .


> **【拓展：TransFusion 的推理过程】**Transfusión  Título clave de la idea: el token de texto se vuelve a generar, se encuentra con una imagen comienza a marcar cuando cambia a un modelo de difusión ⋅ el proceso de difusión se lleva a cabo en el espacio de token ⋅ en lugar de en el espacio de imagen, compartiendo con el generador de texto el mismo modelo parametros ⋅


## Usalo en práctica.
```figure
cfg-guidance-scale
```

## Usalo

`code/main.py`construye un juguete Transfusión sobre un pequeño problema similar a MNIST:

> `code/main.py`En el caso de la miniatura MNIST, la construcción de juguetes Transfusión:

- Las capciones de texto son secuencias cortas de números enteros que describen un dígito (0-9).
  La descripción de los números es la descripción de los números de 0-9) en el texto chino.
- Las imágenes son redes de 4x4 bytes.
  El ejemplar de imágenes es 4x4 字节网格.
- Un par de proyecciones lineales de peso compartido actúa como el reemplazo del transformador; pérdida de NTP en texto, pérdida de MSE en parches ruidosos.
  Un proyecto de línea como Transformer 替代;文本用NTP 损失,噪音补丁用MSE 损失──
- El bucle de entrenamiento alterna las dos pérdidas, la máscara de atención es explícita.
  En el curso de la formación, el ciclo de formación cambia a dos pérdidas, la atención es obvia.
- La generación produce una leyenda de texto y una imagen 4x4 en un pase hacia adelante.
  En el caso de la lengua china, el lenguaje original se utiliza para la traducción de la lengua china.

El transformador es un juguete, la tubería de dos pérdidas, la construcción de la máscara de atención y el bucle de inferencia son los artefactos reales.

> El transformador es un tipo de juguete.

## Envíalo .

Esta lección produce`outputs/skill-two-loss-trainer-designer.md`. Dado una nueva tarea de formación multimodal (texto + imagen, texto + audio, texto + video), diseña el calendario de dos pérdidas (peso de pérdida, forma de máscara, bloques compartidos vs. específicos de modalidad) y señala los riesgos de implementación.

> 本课产 出  `outputs/skill-two-loss-trainer-designer.md`◊ Dado un nuevo trabajo de entrenamiento de múltiples modos (文本+图像、文本+音频、文本+视频), diseñó doble pérdida de peso (输权), ocultar la forma, compartir vs. 模态特定块) y marcó la realización de riesgos.

## Los ejercicios.

1. Un modelo de estilo Transfusion entraña 70% de tokens de texto y 30% de parches de imagen. La pérdida de difusión de imagen es ~10 veces la pérdida de NTP de texto en magnitud. ¿Qué pesos de pérdida los equilibran?
   Traducción:Transfusión 风格模型训练 70% 文本代币 和 30% 图像补丁──图像扩散损失在量级上约为文本NTP 损失的10倍──什么损失权重能平衡它们?

2. Implementar la máscara triangular de bloque para una secuencia: `[T, T, <image>, P, P, P, P, </image>, T]`Marque cada entrada 0 o 1.
   En inglés, "La historia de la historia"`[T, T, <image>, P, P, P, P, </image>, T]`实现块三角掩码──标记每个条目为0或1──

3. MMDiT tiene pesos de QKV específicos para modalidad. ¿Qué parámetros cuenta por encima añade esto vs Transfusion's transformador totalmente compartido?
   China 翻译:MMDiT 有模态特定QKV权重――相比Transfusion 的全共享变压器 增加了多少参数?70亿参数下值值?

4. Generación: dado un mensaje de texto, el modelo ejecuta NTP para 50 tokens, luego golpea `<image>`, luego ejecuta difusión en 256 parches en 20 pasos denoise. ¿Cuántos pasos adelante en total?
   En el caso de los ejemplos de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de`<image>`, y luego en 256 parches, se ejecuta 20 pasos para la difusión del ruido. ¿Cuántas veces en total se transmite?

5. Leer el documento SD3 Sección 3. Describa el flujo rectificado y por qué converge en menos pasos de inferencia que el DDPM.
   La versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de

## Términos clave .

| Term | What people say | What it actually means | 中文含义 | 中文释义 |
|------|-----------------|------------------------|---------|
| Two-loss training | "NTP + diffusion" | A single transformer optimizes both cross-entropy on text tokens and MSE on continuous image patches in the same gradient step | 单一 Transformer 在同一梯度步中优化文本 token 交叉熵和连续图像 patch MSE |
| Flow matching | "Rectified flow" | Diffusion variant that predicts a velocity field from noise to clean data; simpler math than DDPM | 预测从噪声到干净数据速度场的扩散变体；数学比 DDPM 更简单 |
| MMDiT | "Multimodal DiT" | Stable Diffusion 3's architecture: joint attention, modality-specific MLPs and norms | SD3 架构：联合注意力、模态特定 MLP 和归一化 |
| Block-triangular mask | "Causal text + bidirectional image" | Attention mask that is causal across text but bidirectional within image regions | 文本因果、图像区域内双向的注意力掩码 |
| Continuous image representation | "No VQ" | Image patches as real-valued vectors, not integer codebook indices | 图像 patch 为实值向量，非整数码本索引 |
| Velocity prediction | "v-parameterization" | Network output is the velocity field between noise and data, not the noise itself | 网络输出为噪声和数据之间的速度场，非噪声本身 |

## Más Leer más Leer más

- [Zhou et al. — Transfusion (arXiv:2408.11039)](https://arxiv.org/abs/2408.11039)
  La traducción de la traducción de la traducción de la traducción de la traducción de la traducción de la traducción de la traducción de la traducción de la traducción de la traducción de la traducción de la traducción de la traducción de la traducción de la traducción de la traducción de la traducción de la traducción de la traducción de la traducción de la traducción de la traducción de la traducción de la traducción de la traducción de la traducción de la traducción de la traducción de la traducción de la traducción de la traducción de la traducción de la traducción de la traducción de la traducción de la traducción de la traducción de la traducción de la traducción de la traducción de la traducción de la traducción de la traducción de la traducción de la traducción de la traducción de la traducción de la traducción de la traducción de la traducción de la traducción de la traducción de la traducción de la traducción de la traducción de la traducción de la traducción de la traducción de la traducción de la traducción de la traducción de la traducción de la traducción de la traducción de la traducción de la traducción de la traducción de la traducción de la traducción de la traducción de la traducción de la traducción de la traducción de la traducción de la traducción de la traducción de la traducción de la traducción de la traducción de la traducción de la traducción de la traducción de la traducción de la traducción de la traducción de la traducción de la traducción de la traducción de la traducción de la traducción de la traducción de la traducción de la traducción de la traducción de la traducción de la traducción de la traducción de la traducción de la traducción de la traducción de la traducción de la traducción de la traducción de la traducción de la traducción de la traducción de la traducción de la traducción de la traducción de la traducción de la traducción de la traducción de la traducción de la traducción de la traducción de la traducción de la traducción de la traducción de la traducción de la traducción de la traducción de la traducción de la traducción de la traducción de la traducción de la traducción de la lengua
- [Esser et al. — Stable Diffusion 3 / MMDiT (arXiv:2403.03206)](https://arxiv.org/abs/2403.03206)
  La difusión estable 3 / MMDiT 论文。
- [Peebles & Xie — DiT (arXiv:2212.09748)](https://arxiv.org/abs/2212.09748)
  En inglés, el nombre de la palabra "transformador" se traduce en "transformador".
- [Zhao et al. — MonoFormer (arXiv:2409.16280)](https://arxiv.org/abs/2409.16280)
  En el caso de los primeros tiempos, el nombre de la familia de los monos se ha extendido a la antigua.
- [Xie et al. — Show-o (arXiv:2408.12528)](https://arxiv.org/abs/2408.12528)
  En el caso de los niños, el problema es que no hay nada que hacer.
