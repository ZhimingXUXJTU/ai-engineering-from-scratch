# GANs  Generador vs Discriminador  GAN  Productor y Juez

> El truco de Goodfellow en 2014 fue saltar la densidad por completo. Dos redes. Una hace falsificaciones. Una las captura. Luchan hasta que las falsificaciones son indistinguibles de las reales. No debería funcionar. A menudo no funciona. Cuando lo hace, las muestras siguen siendo las más nítidas de la literatura para dominios estrechos.

> **【中文解读】**Goodfellow 2014 ha saltado por completo la estimación de densidad. Dos redes: una falsificación, una cripción, entre sí se pueden distinguir hasta que la falsificación de la muestra y la verdadera muestra. Teóricamente no debe funcionar, en la práctica siempre no funciona, pero una vez que se ha logrado, en la generación de un dominio estrecho sigue siendo el resultado más beneficioso de la literatura.

> **【拓展：GAN 的遗产】**StyleGAN ([[Hombre de la Facia]]) ]], CycleGAN ([[Movimiento de la Facia]]) ]], Pix2Pix ([[Images traducción ]]) ), es una aplicación clásica de GAN. Aunque el modelo de expansión se convirtió en el modelo principal después de 2022, la idea de la lucha contra la formación de GAN se sigue utilizando para mejorar la calidad de otros modelos.

**Type:** Build / 构建型
**Languages:** Python
**Prerequisites:** Phase 3 · 02 (Backprop / 反向传播), Phase 3 · 08 (Optimizers / 优化器), Phase 8 · 02 (VAE)
**Time:** ~75 minutes

## El problema es la introducción del problema

Los VAEs producen muestras borrosas porque su pérdida de decodificador MSE es Bayes-óptima para la imagen * media *  y la media de muchos dígitos plausibles es un dígito borroso. Quieres una pérdida que recompensen * plausibilidad*, no la proximidad de un objetivo en forma de píxel. No hay forma cerrada para la plausibilidad. Tienes que aprenderlo.

> VAE produce muestras confusas, ya que la pérdida de MSE 解码器对*平均值*图像是贝叶斯最优的而许多合理数字的平均值是一个模糊的数字──你需要一个奖励*逼真度*的损失,而不是接近任何目标的像素级──逼真度没有关闭式解,你必须学习它──

La idea de Goodfellow: entrenar un clasificador `D(x)`Para distinguir imágenes reales de falsas.`G(z)`para engañar .`D`. La señal de pérdida para `G`¿ Qué es lo que sea ?`D`Ahora, la señal se actualiza como`G`Mejoras, perseguir un objetivo en movimiento.`G`ha aprendido la distribución de datos sin escribirlo nunca.`log p(x)`¿ Qué ?

> La idea de un buen amigo: entrenar una clase.`D(x)`区分真假图像, entrenar un generador `G(z)`Para engañar .`D`¿Qué es eso?`G`La pérdida de señales es`D`Cuando lo que se dice "parece real" es algo...`G`La actualización y la mejora de la búsqueda de un objetivo móvil.`G`Aprendió a distribuir datos, sin necesidad de escribir.`log p(x)`¿Qué es eso?

Esto es entrenamiento adversario.

```
min_G max_D  E_real[log D(x)] + E_fake[log(1 - D(G(z)))]
```

En 2026 los GAN ya no son el generador de SOTA (la difusión y el flujo de coincidencia comieron esa corona). Pero StyleGAN 2/3 sigue siendo los modelos de cara más afilados jamás enviados, los discriminadores GAN se utilizan como *perdidas perceptuales* en el entrenamiento de difusión, y el entrenamiento adversario potencia las destilaciones rápidas de 1 paso (SDXL-Turbo, SD3-Turbo, LCM) que le permiten enviar difusión en tiempo real.

> 2026 año GAN no es más el generador más avanzado de modelos de expansión y flujo de combinación  se ha conquistado 冠) ⋅ pero StyleGAN 2/3  sigue siendo el modelo de rostro más rentable de la historia, GAN 判斷器 fue utilizado como el * Perdida de percepción en el entrenamiento de expansión*, contra entrenamiento impulsado por un rápido 1 步蒸 ⋅SDXL-Turbo、SD3-Turbo、LCM) ⋅

> **【中文解读】**GAN 尝试生成逼真图像,判别器 D(x) 尝试区分真假──两者在最小x 博中共同进化──VAE  MSE 损失导致模糊(因为它最优化是平均值图像),而GAN 抗损失奖励"逼真度"──GAN 生成速度快(单次前向传播),但训练不稳定──

> **【拓展：GAN 在扩散模型蒸馏中的新角色】**Aunque el GAN no es más un método de generación convencional, el anti-entrenamiento del pensamiento se desarrolla en el modelo de difusión. El modelo de rápida generación de los cambios de velocidad de la GAN se desarrolla en un proceso de 1 a 4 pasos, para lograr la generación en tiempo real.

## El concepto central.

![GAN training: generator and discriminator in minimax](../assets/gan.svg)

**Generator `G(z)`.**Mapas de un vector de ruido `z ~ N(0, I)`a una muestra `x̂`Una red en forma de decodificador (contenido o transpuesto).

> **生成器 `G(z)`。**Se puede ver el ruido.`z ~ N(0, I)`映射为样本                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        `x̂`△ Una red de forma de un descifrador △

**Discriminator `D(x)`.**Mapas de una muestra a una probabilidad escalar (o puntaje). Real → 1, falso → 0.

> **判别器 `D(x)`。**将样本映射为标量概率 (或分数) ⋅ verdad → 1, falsificación → 0⋅

**Loss.**Dos actualizaciones alternativas:

- **Train `D`:** `loss_D = -[ log D(x) + log(1 - D(G(z))) ]`Entropia binaria cruzada en real=1, falso=0.
- **Train `G`:** `loss_G = -log D(G(z))`Esta es la forma no saturante utilizada por Goodfellow (original)`log(1 - D(G(z)))`saturado y mata los gradientes cuando `D`es seguro).

> **损失。**两个交替更新: entrenamiento D 用二元交叉(真实=1,伪造=0); entrenamiento G 用非和形式 `-log D(G(z))`(original forma en D 自信时梯度 desaparecer)

**Training loop.**Un paso de `D`, un paso de `G`Repito.

> **训练循环。**Un paso D, un paso G, un cambio de curso.

**Why it works.**Si ...`G`Se ajusta perfectamente .`p_data`, entonces`D`No puede hacer mejor que el azar y las salidas 0.5 en todas partes; `G`No tiene más gradiente.

> **为什么有效。**Si es que`G`完美匹配 `p_data`, entonces`D`No puedo imaginar mejor que 0.5, en cualquier lugar.`G`No puedo conseguir la escala.

**Why it breaks.**Collapso de modo (`G`encuentra un modo `D`No puedo clasificarlo y lo acuñar para siempre), desvanecimiento de gradiente (`D`Aprende demasiado rápido y `log D`El programa de formación de los jóvenes de edad avanzada (SET) se ha desarrollado en el ámbito de la formación.

> **为什么会失败。**模式塌(`G`找到 `D`无法分类 一种模式并永远产生它) 梯度消失(`D`Aprendió demasiado rápido.`log D`和) 、 entrenamiento no está estable                                                                                                                                                                                                                                                          

## Las variantes que hicieron que GAN funcionara hicieron que GAN tuviera éxito

| Year / 年份 | Innovation / 创新 | Fix / 解决的问题 |
|------|------------|-----|
| 2015 | DCGAN | Conv/deconv, batch norm, LeakyReLU — the first stable architecture. / 首个稳定架构。 |
| 2017 | WGAN, WGAN-GP | Replace BCE with Wasserstein distance + gradient penalty. Fixes vanishing gradient. / 用 Wasserstein 距离替换 BCE，修复梯度消失。 |
| 2017 | Spectral normalization | Lipschitz-bound the discriminator. Still used in 2026 discriminators. / 约束判别器 Lipschitz 常数。 |
| 2018 | Progressive GAN | Train low-res first, add layers. First megapixel results. / 先训练低分辨率，再加层。 |
| 2019 | StyleGAN / StyleGAN2 | Mapping network + adaptive instance norm. State of the art for fixed-domain photorealism. / 映射网络 + AdaIN。 |
| 2021 | StyleGAN3 | Alias-free, translation-equivariant — still the face gold standard in 2026. / 无混叠，平移等变。 |
| 2022 | StyleGAN-XL | Conditional, class-aware, larger scale. / 条件生成，类别感知。 |
| 2024 | R3GAN | Rebrands with stronger regularization; works on 1024² without tricks. / 更强的正则化。 |

## Construye y realiza.
```figure
gan-minimax
```

## Construye el mismo

`code/main.py`El generador y el discriminador son MLP de capa única oculta. Implementamos el bucle hacia adelante, hacia atrás y el bucle minimax a mano. El objetivo es ver los dos modos de falla clave (collaps de modo + gradiente de desaparición) a medida que suceden.

> `code/main.py`En una dimensión de datos entrenar un pequeño GAN: doble cumbre de alto mezcla. Generadores y jueces son una sola esfera de MLP.

### Paso 1: pérdida no saturante

La pérdida de la vainilla Goodfellow .`log(1 - D(G(z)))`se eleva a 0 cuando D clasifica el falso de G como falso con alta confianza. En ese punto el gradiente para G es básicamente cero  G no puede mejorar.`-log D(G(z))`tiene la asintoto opuesta: explota cuando D está seguro, dando a G una señal fuerte.

> El buen amigo                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           `log(1 - D(G(z)))`En D alta confianza grado se va a G de la falsificación de la clasificación por falso tiempo tendrán cerca de 0, en este momento la gradiencia de G de la forma básica es de cero.`-log D(G(z))`Hay un comportamiento contrario: en el momento de la explosión de la confianza, dar a G un fuerte señal.

```python
def g_loss(d_fake):
    # maximize log D(G(z))  <=>  minimize -log D(G(z))
    return -sum(math.log(max(p, 1e-8)) for p in d_fake) / len(d_fake)
```

### Paso 2: un paso discriminador por paso generador

```python
for step in range(steps):
    # train D
    real_batch = sample_real(batch_size)
    fake_batch = [G(z) for z in sample_noise(batch_size)]
    update_D(real_batch, fake_batch)

    # train G
    fake_batch = [G(z) for z in sample_noise(batch_size)]  # fresh fakes
    update_G(fake_batch)
```

Falsas frescas para G, de lo contrario los gradientes son obsoletos.

> Para generar nuevas muestras falsas, o si no está pasando el tiempo.

### Paso 3: vigila el colapso del modo

```python
if step % 200 == 0:
    samples = [G(z) for z in sample_noise(500)]
    mode_a = sum(1 for s in samples if s < 0)
    mode_b = 500 - mode_a
    if min(mode_a, mode_b) < 50:
        print("  [!] mode collapse: one mode is starved")
```

El síntoma canónico: uno de los dos modos reales deja de generarse. El discriminador deja de corregirlo porque nunca se ve como falso.

> 典型症状: Uno de los dos modelos reales ya no se produce.

## Enlaces.

- **Discriminator too strong.**Reducir la velocidad de aprendizaje de D en 2-5 veces, o añadir ruido de instancia/camada. Si D alcanza una precisión del 95%, G está muerto.
  **判别器太强。**La tasa de aprendizaje de D se reduce 2-5 veces, o se añade el ejemplo/ruido de nivel. Si la tasa de precisión de D supera el 95%, G morirá.
- **Generator memorizes a mode.**Añadir ruido a las entradas D, utilizar una capa de miniparcelación o cambiar a WGAN-GP.
  **生成器记住了一种模式。**给 D 输入添加噪声,使用小批量判辨器层,或切换到WGAN-GP──
- **Batch norm leaking statistics.**Los datos de la serie de datos de la serie de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos
  **批归一化泄漏统计量。**Los grupos reales y falsificados se mezclan en la misma BN.
- **Inception-score gaming.**FID y IS son ruidosos en el recuento de muestras bajo.
  **Inception Score 作弊。**FID 和 IS en bajo volumen de muestras en el tiempo de ruido.
- **One-shot sampling is a lie for conditional tasks.**Todavía necesitas escalas CFG, trucos de truncado y re-muestreo para obtener resultados útiles.
  **条件任务中"单次采样"是个谎言。**Aún necesitas técnicas de reducción y recorte de CFG para obtener una salida disponible.

## Usalo con el marco de ejecución

La pila de GAN 2026:

> 2026 años GAN 技术:

| Situation / 场景 | Pick / 选择 |
|-----------|------|
| Photoreal human faces, fixed pose / 照片级人脸，固定姿势 | StyleGAN3 (sharpest, smallest) |
| Anime / stylized faces / 动漫/风格化人脸 | StyleGAN-XL or Stable Diffusion LoRA |
| Image-to-image translation / 图像翻译 | Pix2Pix / CycleGAN (Phase 8 · 04) or ControlNet (Phase 8 · 08) |
| Fast 1-step text-to-image / 快速单步文生图 | Adversarial distillation of diffusion (SDXL-Turbo, SD3-Turbo) |
| Perceptual loss inside a diffusion trainer / 扩散训练中的感知损失 | Small GAN discriminator on image crops |
| Anything multi-modal, open-ended / 多模态开放域 | Don't — use diffusion or flow matching / 不要用 GAN——用扩散或 Flow Matching |

Las GAN son agudas pero estrechas. Una vez que su dominio se abre  fotos, se le solicita texto arbitrario, el video  cambia a difusión.

> GAN 利但狭域──一旦领域开放照片、任意文本提示、视频就就换到扩散模型──对抗技巧作为组件存活(感知损失、蒸),而不是 independiente generador──

## Envíe el producto .

Salva .`outputs/skill-gan-debugger.md`. Skill toma una ejecución GAN fallida (curvas de pérdida, red de muestra, tamaño del conjunto de datos) y produce una lista clasificada de causas probables, correcciones de una línea y un protocolo de repetición.

> 保存 `outputs/skill-gan-debugger.md`◊Habilidad  recepción de una GAN 运行 损失曲线、样本网格、数据集大小),输出可能原因排序列、一行修复和重跑方案──

## Los ejercicios.

1. **Easy / 简单.**- ¿ Qué ?`code/main.py`con las configuraciones de acciones.`D_LR = 5 * G_LR`¿A qué velocidad se derrumba la pérdida de G a una constante?
   Usado por error`code/main.py`。 Entonces se establece `D_LR = 5 * G_LR`¿Las pérdidas de peso de G son constantes?
2. **Medium / 中等.**Substituir la pérdida de Goodfellow BCE por la pérdida de WGAN: `loss_D = E[D(fake)] - E[D(real)]`¿ Qué ?`loss_G = -E[D(fake)]`, y clip de D los pesos a `[-0.01, 0.01]`¿El entrenamiento es más estable?
   Para cambiar los beneficios de la BCE por los de WGAN , cortar el peso de D`[-0.01, 0.01]`¿Hace más tiempo? ¿Qué?
3. **Hard / 困难.**Extenda el ejemplo de 1D a datos 2D (mezcla de 8 Gaussians en un anillo). Rastrear cuántos de los 8 modos que el generador captura en los pasos 1k, 5k, 10k. Implementar la discriminación de minipartidos y volver a medir.
   Para extender el ejemplo 1D a datos 2D, el generador de seguimiento capturó en 1k,5k,10k pasos, logrando un pequeño análisis y reevaluación de la cantidad.

## Términos clave .

| Term / 术语 | What people say / 俗称 | What it actually means / 实际含义 |
|------|-----------------|-----------------------|
| Generator | "G" | Noise-to-sample network, `G: z → x̂`. / 噪声到样本的网络。 |
| Discriminator | "D" | Classifier `D: x → [0, 1]`, real vs fake. / 真假分类器。 |
| Minimax | "The game" / "博弈" | `min_G max_D` of a joint objective. / 联合目标的极小极大。 |
| Non-saturating loss | "The fix" / "修复" | Use `-log D(G(z))` for G instead of `log(1 - D(G(z)))`. / 用非饱和形式替代原始损失。 |
| Mode collapse | "G memorized one thing" / "G 记住了一种" | Generator produces few distinct outputs despite diverse data. / 生成器产生少量不同输出。 |
| WGAN | "Wasserstein" | Replace BCE with Earth-Mover distance + gradient penalty; smoother gradient. / 用 Wasserstein 距离替代 BCE。 |
| Spectral norm | "Lipschitz trick" / "Lipschitz 技巧" | Constrain D's weight norms to bound its slope; stabilizes training. / 约束 D 的权重范数以稳定训练。 |
| StyleGAN | "The one that works" / "能用的那个" | Mapping network + AdaIN; best-in-class for faces, still in 2026. / 映射网络 + AdaIN，人脸最佳。 |

## Nota de producción: la inferencia de un solo disparo es la ventaja duradera de GAN.

Los GAN ya no ganan en la calidad de la muestra para la generación de dominio abierto, pero todavía ganan en el costo de inferencia.

> GAN no ha ganado más en la calidad de las muestras generadas en el área abierta, pero sigue ganando en el costo de la producción.

- **No prefill, no decode stages.**Un solo .`G(z)`TTFT ≈ latencia total.
  **无 prefill，无 decode 阶段。**单次                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           `G(z)`Antes de la difusión, el tiempo de la difusión.
- **No KV-cache pressure.**El tamaño del lote está limitado por la memoria de activación, no por el caché.
  **无 KV 缓存压力。**El único estado es el peso. El tamaño del lote se limita a la memoria activa y no a la memoria.
- **Trivial continuous batching.**Como cada solicitud requiere los mismos FLOPs fijos, un lote estático en la ocupación de destino del servidor es generalmente óptimo.
  **简单的连续批处理。**Cada solicitud consume el mismo FLOP, el volumen estático suele ser el mejor.

Esta es la razón por la que la destilación de GAN (SDXL-Turbo, SD3-Turbo, ADD, LCM) es la técnica dominante para el texto rápido a la imagen en 2026: se desmorona un tubo de difusión de 20-50 pasos en pases hacia adelante de 1-4 GAN al tiempo que se mantiene la distribución de una base de difusión.

> Es por eso que GAN 蒸(SDXL-Turbo、SD3-Turbo、LCM) es la principal tecnología de 2026: se ampliará en 2050 pasos a 1-4 veces el flujo de agua de la GAN 风格, manteniendo la distribución del modelo de propagación.

## Más Leer más Leer más

- [Goodfellow et al. (2014). Generative Adversarial Nets](https://arxiv.org/abs/1406.2661) el papel original de la GAN.
- [Radford et al. (2015). Unsupervised Representation Learning with DCGAN](https://arxiv.org/abs/1511.06434) la primera arquitectura estable.
- [Arjovsky, Chintala, Bottou (2017). Wasserstein GAN](https://arxiv.org/abs/1701.07875) WGAN.
- [Miyato et al. (2018). Spectral Normalization for GANs](https://arxiv.org/abs/1802.05957) SN.
- [Karras et al. (2020). Analyzing and Improving the Image Quality of StyleGAN](https://arxiv.org/abs/1912.04958) StyleGAN2.
- [Karras et al. (2021). Alias-Free Generative Adversarial Networks](https://arxiv.org/abs/2106.12423) StyleGAN3.
- [Sauer et al. (2023). Adversarial Diffusion Distillation](https://arxiv.org/abs/2311.17042) SDXL-Turbo.
