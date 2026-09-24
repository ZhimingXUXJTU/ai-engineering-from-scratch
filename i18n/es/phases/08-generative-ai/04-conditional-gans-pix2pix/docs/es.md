# GAN condicional y Pix2Pix .  Condiciones GAN y Pix2Pix

> La primera gran desbloqueación de 2014-2017 fue controlar lo que hace un GAN. adjunta una etiqueta, o una imagen, o una frase. Pix2Pix hizo la versión de imagen y todavía supera todos los modelos genéricos de texto a imagen en tareas estrechas de imagen a imagen.

> **【中文解读】**El primer gran avance de 2014-2017 fue el control de GAN. Produjo: etiquetas adicionales, imágenes o textos. Pix2Pix hizo una versión de imágenes, que hasta ahora ha superado el modelo de imagen generado en texto general en tareas de traducción de imágenes de dominio estrecho.

> **【拓展：Pix2Pix 的应用】**Pix2Pix creó el modelo de "imagen a imagen traducción": dibujo, fotografía, día, noche, dibujo, dibujo de colores.

**Type:** Build / 构建型
**Languages:** Python
**Prerequisites:** Phase 8 · 03 (GANs), Phase 4 · 06 (U-Net), Phase 3 · 07 (CNNs / 卷积神经网络)
**Time:** ~75 minutes

## El problema es la introducción del problema

Un GAN incondicional muestra caras arbitrarias. Útil para una demostración, inútil en la producción. Quieres: *mapear un boceto a una foto*, *mapear un mapa a una foto aérea*, *mapear una escena diurna a la noche*, *colorizar una imagen a escala de gris*. En todas estas, se te da una imagen de entrada`x`y debe emitir`y`Hay muchas razones plausibles.`y`por`x`El error medio cuadrado los aplanará en masaje.

> 无条件 GAN 采样任意人脸──适合演示,不适合生产──你想要的是:*将素描映射为照片*、*将地图映射为航拍图*、*将白天映射为夜*、*给灰度图上色*──在所有这些场景中,给定输入图像`x`, debe emitir relaciones de significado para la respuesta.`y` Cada uno `x`Hay muchas razonabilidades.`y`                                                                                                                                                                                                                                                              

GAN condicional (Mirza & Osindero, 2014) añade una condición `c`como una entrada para ambos `G`y `D`. Pix2Pix (Isola et al., 2017) se especializó en esto: condición es una imagen de entrada completa, generador es una U-Net, discriminador es un clasificador basado en parches (PatchGAN), y pérdida es adversarial + L1.

> 条件 GAN(2014) en `G`Y `D`de entrada en condiciones adicionales`c`Pix2Pix(2017) ha especializado en esto: condiciones es la entrada completa de imágenes, generador es U-Net, divisor es PatchGAN, pérdida = contra + L1♦ Este programa en la tarea de traducción de imágenes de estrecho dominio incluso 2026 sigue siendo mejor que el modelo de imágenes de la cabeza, ya que está en el entrenamiento de datos de parentesco.

> **【中文解读】**条件 GAN's core improvement: give generator and判别器都添加条件输入 c。Pix2Pix's condition is complete input image, generator U-Net (contención de espacio detalle),判别器 PatchGAN (contención de espacio en el espacio en el espacio en el espacio) ⋅ loss = resistencia a la pérdida + L1 ⋅ loss. Este método de entrenamiento de datos de paridad sigue siendo mejor que el modelo de generación de imágenes de texto en tareas de traducción de imágenes de dominio estrecho.

> **【拓展：从 Pix2Pix 到 ControlNet 的演进】**La idea de "generación de imágenes en condiciones" de Pix2Pix fue adoptada por ControlNet (con el año 2023) y desarrollada. ControlNet incorporará las condiciones de control (con el tiempo, la profundidad, la imagen, etc.) en el modelo de difusión estable de la preparación, logrando una generalización más general de la generación de imágenes en control.

## El concepto central.

![Pix2Pix: U-Net generator, PatchGAN discriminator](../assets/pix2pix.svg)

**Conditional G.** `G(x, z) → y`En Pix2Pix,`z`se desprende dentro de G (no hay ruido de entrada  Isola encontró que el ruido explícito fue ignorado).

> **条件生成器 G。** `G(x, z) → y`En Pix2Pix,`z`Es un problema de la salud y de la salud.

**Conditional D.** `D(x, y) → [0, 1]`. La entrada es el *pair* (condición, salida). Esta es la diferencia clave: D debe juzgar si `y`es consistente con `x`, no sólo si`y`Parece real.

> **条件判别器 D。** `D(x, y) → [0, 1]`◊输入是*配对*(条件,输出) ー关键区别:D 必须判断 `y`¿Cómo se puede`x`Un致, no sólo es`y`Sí, parece que es verdad.

**U-Net generator.**Encoder-decodificador con conexiones de salto a través del cuello de botella. Es crítico para tareas donde la entrada y salida comparten una estructura de bajo nivel (bordañas, silueta). Sin los saltos, los detalles de alta frecuencia desaparecen.

> **U-Net 生成器。**带有跳跃连接的编码器-解码器―― para la entrada, salida y distribución de la estructura de bajo nivel ([[边缘、轮]]) es esencial la tarea de la

**PatchGAN discriminator.**En lugar de emitir una única puntuación real/falsa, D emitirá una`N×N`La red de la red donde cada célula juzga un campo receptivo de ~70×70 píxeles. promedio. Esta es una suposición de campo aleatorio de Markov: el realismo es local.

> **PatchGAN 判别器。**D 输出 `N×N`网格而不是 un solo verdadero/falso分数, cada unidad juzgará aproximadamente 70×70 像素的感受野──这是马尔可夫随机场假设:真实感是局部的──训练更快,参数更少,输出更利──

**Loss.**

```
loss_G = -log D(x, G(x)) + λ · ||y - G(x)||_1
loss_D = -log D(x, y) - log (1 - D(x, G(x)))
```

El término L1 estabiliza el entrenamiento y empuja a G hacia el objetivo conocido.`λ = 100`fue el default de Pix2Pix.

> El entrenamiento de estabilidad de L1 项并推动 G 趋向已知目标──L1比L2 产生更利的边缘(中位数 vs 平均值)──`λ = 100`Es el valor predeterminado de Pix2Pix.

## CycleGAN  cuando no tienes pares  CycleGAN   no tiene par de datos 

Pix2Pix necesita emparejados `(x, y)`Los datos. CycleGAN (Zhu et al., 2017) reduce este requisito al costo de una pérdida adicional: la pérdida de *consistencia del ciclo* .`G: X → Y`y `F: Y → X`Entrenadlos así .`F(G(x)) ≈ x`y `G(F(y)) ≈ y`Esto te permite traducir caballos a cebras, verano a invierno, sin ejemplos emparejados.

> Pix2Pix 需要配对 `(x, y)`Datos: CycleGAN (en 2017) abandonó este requisito, el precio es una pérdida de coherencia de ciclo extra.`G: X → Y`Y `F: Y → X`, entrenamiento`F(G(x)) ≈ x`Y `G(F(y)) ≈ y` Esto te hace sin necesidad de par par de muestras para poder convertir el caballo en zebra, el verano en invierno

En 2026, la imagen a imagen sin pareja se realiza principalmente a través de la difusión (ControlNet, IP-Adapter) en lugar de CycleGAN, pero la idea de coherencia de ciclo sobrevive en casi todos los papeles de adaptación de dominio sin pareja.

> En 2026 años, la idea de coherencia de circuitos se desarrolla principalmente a través de modelos de distribución (ControlNet、IP-Adapter) y no CycleGAN 完成, pero casi existe en cada artículo de adaptación de dominio de circuitos.

## Construye y realiza.
```figure
gx-patchgan
```

## Construye el mismo

`code/main.py`Implementa una pequeña GAN condicional en los datos 1D.`c`es una etiqueta de clase (0 o 1). La tarea: producir una muestra de la distribución condicional para la clase dada.

> `code/main.py`En una dimensión de datos se realiza una condición de micro tipo GAN.`c`Es decir, el tipo de trabajo que se realiza en el campo de la información.

### Paso 1: añadir la condición a las entradas G y D

```python
def G(z, c, params):
    return mlp(concat([z, one_hot(c)]), params)

def D(x, c, params):
    return mlp(concat([x, one_hot(c)]), params)
```

El codificación de un solo punto es la forma más simple. Los modelos más grandes utilizan embebedidos aprendidos, modulación FiLM o atención cruzada.

> El codificación de un solo tipo es la forma más simple.

### Paso 2: tren condicional

```python
for step in range(steps):
    x, c = sample_real_conditional()
    noise = sample_noise()
    update_D(x_real=x, x_fake=G(noise, c), c=c)
    update_G(noise, c)
```

El generador debe coincidir con la distribución real *de la condición dada*, no con la marginal.

> Los componentes deben coincidir con la distribución real bajo determinadas condiciones, y no con la distribución marginal.

### Paso 3: verificar la salida por clase

```python
for c in [0, 1]:
    samples = [G(noise, c) for noise in batch]
    mean_c = mean(samples)
    assert_near(mean_c, real_mean_for_class_c)
```

## Enlaces.

- **Condition ignored.**G aprende a marginar, D nunca penaliza porque la señal de condición es débil.
  **条件被忽略。**G aprendería a margenizar, D de no castigar porque las condiciones se debilitaron.
- **L1 weight too low.**G se deriva a resultados reales arbitrarios, no fieles.
  **L1 权重太低。**G 偏移到任意看起来真实输出──Pix2Pix 任务从 λ≈100 开始──
- **L1 weight too high.**G produce resultados borrosos porque L1 sigue siendo una norma de L_p.
  **L1 权重太高。**G  产生模糊输出── entrenamiento estabilizado después gradualmente disminuir──
- **Ground-truth leakage in D.**Concatenato `(x, y)`como entrada D, no sólo `y`Sin este D no se puede comprobar la consistencia.
  **D 中的真值泄漏。**¿ Qué ?`(x, y)`拼接为 D 的输入,而非仅仅 `y`¿Qué es eso?
- **Mode collapse per class.**Cada clase puede colapsar de forma independiente.
  **每类模式坍塌。**Cada categoría puede ser separada de la otra.

## Usalo con el marco de ejecución

2026 estado de las tareas de imagen a imagen:

> 2026 año de imágenes a imágenes estado de la misión:

| Task / 任务 | Best approach / 最佳方案 |
|------|---------------|
| Sketch → photo, same domain, paired data / 素描→照片，配对数据 | Pix2Pix / Pix2PixHD (still fast, still sharp) |
| Sketch → photo, unpaired / 素描→照片，非配对 | ControlNet with a Scribble conditioning model |
| Semantic seg → photo / 语义分割→照片 | SPADE / GauGAN2 or SD + ControlNet-Seg |
| Style transfer / 风格迁移 | Diffusion with IP-Adapter or LoRA; GAN methods are legacy |
| Depth → photo / 深度→照片 | ControlNet-Depth over Stable Diffusion |
| Super-resolution / 超分辨率 | Real-ESRGAN (GAN), ESRGAN-Plus, or SD-Upscale (diffusion) |
| Colorization / 上色 | ColTran, diffusion-based colorizers, or Pix2Pix-color |
| Daytime → nighttime, seasons, weather / 白天→夜晚 | CycleGAN or ControlNet-based |

Pix2Pix sigue siendo la herramienta correcta cuando (a) tienes miles de ejemplos emparejados, (b) la tarea es estrecha y repetible, y (c) necesitas una inferencia rápida. En tareas genéricas de dominio abierto, la difusión gana.

> Pix2Pix en la siguiente situación sigue siendo un instrumento correcto: a) Hay miles de ejemplos de parámetros, b) tareas estrechas y replicables, c) necesita una rápida evaluación.

## Envíe el producto .

Salva .`outputs/skill-img2img-chooser.md`. La habilidad toma una descripción de tarea, la disponibilidad de datos (pareados vs. sin parejas, muestras N) y el presupuesto de latencia/calidad, luego las salidas: enfoque (Pix2Pix, CycleGAN, variante de ControlNet, SDXL + IP-Adapter), requisitos de datos de capacitación, costo de inferencia y protocolo de evaluación (LPIPS, FID, específico de tarea).

> 保存 `outputs/skill-img2img-chooser.md` Descripción de tareas de recepción de habilidades, disponibilidad de datos y presupuesto de retraso/calidad, programa de salida, formación de la demanda de datos, acuerdo de cálculo de costes y evaluación.

## Los ejercicios.

1. **Easy / 简单.**Modificar`code/main.py`Confirmar G todavía maps el ruido de cada clase al modo correcto.
   修改                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           `code/main.py`Añadir tercer tipo de ruido: confirmar que cada tipo de ruido se reflejará en el modo correcto.
2. **Medium / 中等.**Reemplazar L1 con una pérdida de estilo perceptivo en el entorno 1-D (por ejemplo, un pequeño D congelado que actúa como extractor de características). ¿Cambia la nitidez de la distribución condicional?
   ¿En la configuración 1D se sustituye la pérdida de percepción por la L1? ¿Cambió la distribución de las condiciones?
3. **Hard / 困难.**Esbozar un CycleGAN en la configuración 1-D: dos distribuciones, dos generadores, pérdida de ciclo. Muestre que aprende a mapear entre ellos sin datos emparejados.
   En la configuración 1D  desencargar en CycleGAN: dos distribuciones ∆ dos generadores ∆ ciclo de pérdida  prueba que no necesita de par par de datos para aprender a mapear 

## Términos clave .

| Term / 术语 | What people say / 俗称 | What it actually means / 实际含义 |
|------|-----------------|-----------------------|
| Conditional GAN | "GAN with labels" / "带标签的 GAN" | G(z, c), D(x, c). Both networks see the condition. / 两个网络都看到条件。 |
| Pix2Pix | "Image-to-image GAN" / "图像到图像 GAN" | Paired cGAN with U-Net G and PatchGAN D + L1 loss. / 配对 cGAN + U-Net + PatchGAN + L1。 |
| U-Net | "Encoder-decoder with skips" / "带跳跃的编解码器" | Symmetric conv network; skips preserve high-freq. / 对称卷积网络；跳跃连接保留高频。 |
| PatchGAN | "Local-realism classifier" / "局部真实分类器" | D outputs per-patch score instead of global score. / D 输出逐块分数。 |
| CycleGAN | "Unpaired image translation" / "非配对图像翻译" | Two G's + cycle-consistency loss; no paired data. / 两个 G + 循环一致性损失。 |
| SPADE | "GauGAN" | Normalizes intermediate activations with the semantic map; segmentation-to-image. / 用语义图归一化中间激活。 |
| FiLM | "Feature-wise linear modulation" / "特征级线性调制" | Per-feature affine transform from the condition; cheap conditioning. / 廉价的条件化方式。 |

## Nota de producción: Pix2Pix como una línea de base limitada a la latencia

Cuando se ha emparejado datos y una tarea estrecha (bozo → renderizado, mapa semántico → foto, día → noche), la inferencia de una sola toma de Pix2Pix supera la difusión por un orden de magnitud en la latencia.

> Cuando tienes una relación entre datos y tareas de dominio estrecho, la única hipótesis de Pix2Pix es que el modelo de expansión es rápido en un nivel cuantitativo.

| Path / 方案 | Steps / 步数 | Typical latency at 512² on a single L4 / 典型延迟 |
|------|-------|----------------------------------------|
| Pix2Pix (U-Net forward) | 1 | ~30 ms |
| SD-Inpaint or SD-Img2Img | 20 | ~1.2 s |
| SDXL-Turbo Img2Img | 1-4 | ~0.15-0.35 s |
| ControlNet + SDXL base | 20-30 | ~3-5 s |

Pix2Pix gana en el rendimiento en lotes estáticos (cada solicitud es la misma FLOPs). La difusión gana en la calidad y generalización.

> Pix2Pix en estado de estado de producción en volumen de producción. Cada solicitud FLOPs similar) ◊ modelo de distribución en calidad y generalización ◊ la práctica moderna es generalmente para la distribución de tareas de área estrecha Pix2Pix 风格蒸模型, para la entrada final proporcionar la distribución y el regreso ◊

## Más Leer más Leer más

- [Mirza & Osindero (2014). Conditional Generative Adversarial Nets](https://arxiv.org/abs/1411.1784) el documento de la CGAN.
- [Isola et al. (2017). Image-to-Image Translation with Conditional Adversarial Networks](https://arxiv.org/abs/1611.07004) Pix2Pix.
- [Zhu et al. (2017). Unpaired Image-to-Image Translation using Cycle-Consistent Adversarial Networks](https://arxiv.org/abs/1703.10593) CycleGAN.
- [Wang et al. (2018). High-Resolution Image Synthesis with Conditional GANs](https://arxiv.org/abs/1711.11585) Pix2PixHD.
- [Park et al. (2019). Semantic Image Synthesis with Spatially-Adaptive Normalization](https://arxiv.org/abs/1903.07291) SPADE / Gaugan.
- [Miyato & Koyama (2018). cGANs with Projection Discriminator](https://arxiv.org/abs/1802.05637) la proyección D.
