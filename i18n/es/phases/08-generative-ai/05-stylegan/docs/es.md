# StyleGAN  风格生成对抗网络

> La mayoría de los generadores se mueven .`z`StyleGAN lo divide en partes: primer mapa`z`a un intermediario `w`, luego * inyectar *`w`Este cambio único desentrañó el espacio latente y hizo que las caras fotorealistas fueran un problema resuelto durante siete años consecutivos.

> **【中文解读】**StyleGAN se encargará de ocultar los cambios z previamente proyectados en el espacio medio w, reincorporando AdaIN en cada nivel de resolución en w, logrando el control independiente de la generación de imágenes en diferentes niveles de grabación y características de granosidad. Este cambio abrió el espacio oculto, haciendo que la generación de caras reales se haya resuelto durante siete años.

> **【拓展：StyleGAN 的应用】**StyleGAN  amplio utilizado para la generación de personas (thispersondoesnotexist.com) 、虚拟人物创建、艺术创作──其 Style Mixing 技术可以混合不同人的脸的粗细特征──

**Type:** Build / 构建型
**Languages:** Python
**Prerequisites:** Phase 8 · 03 (GANs), Phase 4 · 08 (Normalization / 归一化), Phase 3 · 07 (CNNs)
**Time:** ~45 minutes

## El problema es la introducción del problema

Un mapa de DCGAN `z`a una imagen a través de una pila de convolucciones transpuestas.`z`controlan todo  pose, iluminación, identidad, fondo  entrelazados.`z`No se puede preguntar al modelo "la misma persona, pose diferente" porque la representación no tiene factor de esa manera.

> DCGAN                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           `z`映射为图像── el problema es:`z`Controlando todo el mundo, la forma, la luz, la identidad, el contexto, todo lo relacionado.`z`De un eje se mueve, cuatro se mueve. Tú no puedes exigir el modelo "La misma persona, diferentes posturas", porque no se descompone así.

Karras et al. (2019, NVIDIA) propuso: dejar de alimentar `z`En el interior de la superficie, el agua se coloca en una posición constante.`4×4×512`Aprenda una MLP de 8 capas que mapea `z ∈ Z → w ∈ W`Inyectar`w`en cada resolución a través de *adaptive instance normalization* (AdaIN): normaliza cada mapa de características con, luego escala y desplaza por proyecciones afines de `w`. Añadir ruido por capa para detalle estocástico (poros de piel, hebras de cabello).

> Karras 等人(2019,NVIDIA) propuso:停止将 `z`直接送入卷积层──Utilizando un número constante `4×4×512`张量作为网络输入──学习一个8层 MLP将 `z ∈ Z → w ∈ W`◊ Por medio de * autoadaptación ejemplos de la integración * * AdaIN) en cada resolución`w`◊ Añadir cada nivel de ruido de la zona se utiliza para la zona de la zona de la zona.

El resultado:`W`tiene aproximadamente ejes ortogonales para "estilo de alto nivel" (posición, identidad) vs "estilo fino" (iluminación, color).`w`para los niveles de baja resolución y las imágenes B `w`Esta edición desbloqueada, estilización de dominios cruzados y toda la línea de investigación "StyleGAN-inversión".

> 结果:`W`空间对"高级风格" (gestuación, personalidad) y "精细风格" (luz, colores)`w`Usando la capa de baja resolución de imagen B.`w`Se utiliza en niveles de alta resolución para intercambiar estilos. Esto desbloquea la edición, la configuración de los distintos dominios y la dirección de estudio de "StyleGAN Controversion".

> **【中文解读】**La clave de StyleGAN es la innovación: 1) la maquetación de la red z→w 解开纠的隐空间; 2) AdaIN en cada nivel de resolución inyecta el estilo bajo nivel de resolución control de la grosoridad de la imagen; 3) cada nivel con el ruido añadir detalles; 3) la mezcla de estilo.

> **【拓展：StyleGAN 3 的平移等变性】**StyleGAN 2 Se ha resuelto este problema a través de una serie de señales de comprensión de imágenes con "títulos de adhesión" en su posición en lugar de en la superficie del objeto. Esto es especialmente importante para la generación de video y la aplicación de 3D.

## El concepto central.

![StyleGAN: mapping network + AdaIN + per-layer noise](../assets/stylegan.svg)

**Mapping network.** `f: Z → W`, una MLP de 8 capas.`Z = N(0, I)^512`- ¿ Qué ?`W`No se ve obligado a ser gaussiano. Aprende una forma adaptada a los datos.

> **映射网络。** `f: Z → W`,8 niveles de MLP`W`No se obliga a que se aprenda a adaptarse a la forma de los datos.

**Synthesis network.**Comienza con una constante aprendida .`4×4×512`. Cada bloque de resolución: `upsample → conv → AdaIN(w_i) → noise → conv → AdaIN(w_i) → noise`Resoluciones dobles: 4, 8, 16, 32, 64, 128, 256, 512, 1024.

> **合成网络。**Desde el aprendizaje hasta el número de constantes`4×4×512`开始──每个分辨率块:上采样→卷积→AdaIN→噪声→卷积→AdaIN→噪声──分辨率翻倍:4 到1024──

**AdaIN.**

```
AdaIN(x, y) = y_scale · (x - mean(x)) / std(x) + y_bias
```

donde`y_scale`y `y_bias`se derivan de proyecciones afines de `w`Normaliza por mapa de características, luego rediseña. "estilo" aquí es la estadística de primer y segundo orden del mapa de características.

> Entre ellos `y_scale`Y `y_bias`Desde`w`La forma de proyección es de la forma de la forma de la forma de la forma de la forma de la forma de la forma de la forma de la forma de la forma de la forma de la forma de la forma de la forma de la forma de la forma de la forma de la forma de la forma de la forma de la forma de la forma de la forma de la forma de la forma de la forma de la forma de la forma de la forma de la forma de la forma de la forma de la forma de la forma de la forma de la forma de la forma de la forma de la forma de la forma de la forma de la forma de la forma de la forma de la forma de la forma de la forma de la forma de la forma de la forma de la forma de la forma de la forma de la forma de la forma de la forma de la forma de la forma de la forma de la forma de la forma de la forma de la forma de la forma de la forma de la forma de la forma de la forma de la forma de la forma de la forma de la forma de la forma de la forma de la forma de la forma de la forma de la forma de la forma de la forma de la forma de la forma de la forma de la forma de la forma de la forma de la forma de la forma de la forma de la forma de la forma de la forma de la forma de la forma de la forma de la forma de la forma de la forma de la forma de la forma de la forma de la forma de la forma de la forma de la forma de la de la forma.

**Per-layer noise.**El ruido gaussiano de un solo canal se añade a cada mapa de características, escalado por un factor por canal aprendido.

> **每层噪声。** Un solo paso alto de ruido se añade a cada gráfico de características, por el factor de paso individual que se puede aprender se reduce―controlar los detalles de cada paso sin afectar la estructura general―.

**Truncation trick.**En la inferencia, muestra `z`, computación `w = mapping(z)`, entonces`w' = ŵ + ψ·(w - ŵ)`donde`ŵ`es la media`w`en muchas muestras. `ψ < 1`La diversidad es la ventaja de la calidad.`ψ ≈ 0.7`¿ Qué ?

> **截断技巧。**推理时, el tiempo de la`w' = ŵ + ψ·(w - ŵ)`, entre ellos `ŵ`Sí `w`En varios ejemplos, el promedio de la cantidad de`ψ < 1`EstilGAN  Muchas muestras de estilo se utilizan`ψ ≈ 0.7`¿Qué es eso?

## StyleGAN 1 → 2 → 3  StyleGAN  versión desarrollada

| Version | Year | Innovation / 创新 |
|---------|------|------------|
| StyleGAN | 2019 | Mapping network + AdaIN + noise + progressive growing. / 映射网络 + AdaIN + 噪声 + 渐进增长。 |
| StyleGAN2 | 2020 | Weight demodulation replaces AdaIN (fixes droplet artifacts); skip/residual architecture; path-length regularization. / 权重解调替代 AdaIN。 |
| StyleGAN3 | 2021 | Alias-free convolution + equivariant kernels; eliminates texture sticking to pixel grid. / 无混叠卷积，消除纹理粘附。 |
| StyleGAN-XL | 2022 | Class-conditional, 1024², ImageNet. / 类别条件，1024²。 |
| R3GAN | 2024 | Rebrands with stronger reg; closes gap to diffusion on FFHQ-1024 with 20x fewer params. / 更强正则化，20 倍更少参数。 |

En 2026 StyleGAN3 sigue siendo el estándar para (a) fotorrealismo de dominio estrecho con FPS alto, (b) adaptación de dominio de pocos disparos (tren en un nuevo conjunto de datos con 100 imágenes, c) edición basada en la inversión (encuentra el `w`que reconstruye una foto real, luego editar que `w`Para el dominio abierto de texto a imagen, no es la herramienta  difusión es.

> 2026 StyleGAN3  todavía es el siguiente escenario de la elección: a) Alta FPS 窄域照片级真感, b) Poco sample域适应, c) basado en la edición de la re-evento.

## Construye y realiza.
```figure
gx-stylegan-mapping
```

## Construye el mismo

`code/main.py`Implementa un juguete "style-GAN lite" en 1-D: una MLP de mapeo, una función de síntesis que toma un vector constante aprendido y lo modula con `w`-desde la escala/bias derivadas y el ruido por capa.`w`por medio de coincidencias de modulación afina o de latidos concatenados `z`en la entrada del generador.

> `code/main.py`En 1D se realizó una "StyleGAN lite": mapeo MLP, función sintética y cada nivel de ruido.`w`Con el`z`拼接到输入相比效果相当或更好──

### Paso 1: red de mapeo

```python
def mapping(z, M):
    h = z
    for i in range(num_layers):
        h = leaky_relu(add(matmul(M[f"W{i}"], h), M[f"b{i}"]))
    return h
```

### Paso 2: Normalización de instancia adaptativa

```python
def adain(x, w_scale, w_bias):
    mu = mean(x)
    sd = std(x)
    x_norm = [(xi - mu) / (sd + 1e-8) for xi in x]
    return [w_scale * xi + w_bias for xi in x_norm]
```

La escala y el sesgo de las características del mapa provienen de `w`por medio de la proyección lineal.

>                                                                                                                                                                                                                                                               `w`La línea de proyección.

### Paso 3: ruido por capa

```python
def add_noise(x, sigma, rng):
    return [xi + sigma * rng.gauss(0, 1) for xi in x]
```

Sigma por canal es aprendizaje.

> Cada paso de sigma es algo que se puede aprender.

## Enlaces.

- **Droplet artifacts.**StyleGAN 1 produjo una gota de manchas en los mapas de características porque AdaIN eliminó el promedio.
  **液滴伪影。**StyleGAN 1  因 AdaIN 归零均值产生液滴──StyleGAN 2 的权重解调通过缩放卷积权重修复──
- **Texture sticking.**Las texturas de StyleGAN 1 y 2 siguieron las coordenadas de píxel, no las coordenadas de objeto (visibles cuando se interpola).
  **纹理粘附。**La estructura de StyleGAN 1/2 sigue a la imagen de un eje, y no a la de un objeto.
- **Mode coverage.**Truncado `ψ < 0.7`se ve limpio pero muestras de un cono estrecho; uso `ψ = 1.0`Si necesitas diversidad.
  **模式覆盖。**截断 `ψ < 0.7`Parece limpio pero de una forma muy estrecha.`ψ = 1.0`¿Qué es eso?
- **Inversion is lossy.**Invertir una foto real en`W`Se realiza generalmente a través de la optimización o un codificador (e4e, ReStyle, HyperStyle).
  **反演有损。**Voy a hacer una foto real.`W`Normalmente se realiza mediante optimización o codificador, el resultado se desplaza en varias generaciones posteriores.

## Usalo con el marco de ejecución

| Use case / 用途 | Approach / 方案 |
|----------|----------|
| Photoreal human faces (anime, product, narrow) / 照片级人脸 | StyleGAN3 FFHQ / custom fine-tune |
| Face editing from a photo / 从照片编辑人脸 | e4e inversion + StyleSpace / InterFaceGAN directions |
| Face swap / reenactment / 换脸/重演 | StyleGAN + encoder + blending |
| Avatar pipelines / 虚拟形象 | StyleGAN3 w/ ADA for low-data fine-tune |
| Domain adaptation from a few images / 少样本域适应 | Freeze mapping network, fine-tune synthesis |
| Multi-modal or text-conditioned generation / 多模态生成 | Don't — use diffusion / 不要用——用扩散模型 |

Para las demostraciones de calidad de producto donde la respuesta es "foto de la cara de una persona", StyleGAN supera la difusión en el costo de inferencia (pasado a la derecha, <10 ms en un 4090) y la nitidez para la misma barra de calidad.

> 对于"人物面部照片"级别的产品演示,StyleGAN在推理成本(单次前向传播,4090 上 <10ms) 和同质下度上胜过扩散模型──

## Envíe el producto .

Salva .`outputs/skill-stylegan-inversion.md`. Skill toma una foto real y las salidas: método de inversión (e4e / ReStyle / HyperStyle), pérdida latente esperada, presupuesto de edición (cuánto tiempo en `W`se puede mover antes de los artefactos), y una lista de conocidas buenas direcciones de edición (edad, expresión, postura).

> 保存 `outputs/skill-stylegan-inversion.md`◊Habilidad para recibir fotos reales, hacer cambios en los métodos de producción, anticipar pérdidas potenciales, editar el presupuesto y el rumbo de edición conocido.

## Los ejercicios.

1. **Easy / 简单.**- ¿ Qué ?`code/main.py`con`adain_on=True`y `adain_on=False`Comparar la dispersión de las salidas de un latente fijo con el latente perturbado.
   Por lo demás .`adain_on=True`Y `adain_on=False`运行―― Comparar la distribución de las emisiones de los cambios fijos y los cambios perturbadores―
2. **Medium / 中等.**Implementar la regularización de mezcla: para un lote de formación, calcular `w_a`¿ Qué ?`w_b`, y se aplican `w_a`para la primera mitad de la síntesis y `w_b`¿El decodificador aprende estilos desentrañados?
   ¿Ha aprendido a resolver el estilo?
3. **Hard / 困难.**Tome un modelo de FFHQ (ffhq-1024.pkl) de StyleGAN3 pre-entrenado.`w`Dirección que controla la "smile" mediante la formación de un SVM en muestras etiquetadas; informe hasta dónde puede avanzar antes de que la identidad se desvíe.
   Utiliza Pre-entrenamiento StyleGAN3 FFHQ 模型, a través de SVM 找到控制"微笑"的 `w`Dirección:

## Términos clave .

| Term / 术语 | What people say / 俗称 | What it actually means / 实际含义 |
|------|-----------------|-----------------------|
| Mapping network | "The MLP" / "那个 MLP" | `f: Z → W`, 8 layers, decouples latent geometry from data statistics. / 解耦隐变量几何与数据统计。 |
| W space | "The style space" / "风格空间" | Output of the mapping network; roughly disentangled. / 映射网络的输出；大致解耦。 |
| AdaIN | "Adaptive instance norm" / "自适应实例归一化" | Normalize feature map, then scale + shift by `w`-projection. / 归一化后用 `w` 投影缩放偏移。 |
| Truncation trick | "Psi" | `w = mean + ψ·(w - mean)`, ψ<1 trades diversity for quality. / ψ<1 以多样性换质量。 |
| Path-length regularization | "PL reg" | Penalizes large changes in image per unit change in `w`; makes `W` smoother. / 惩罚 `w` 单位变化引起的大图像变化。 |
| Weight demodulation | "The StyleGAN2 fix" / "StyleGAN2 修复" | Normalize conv weights instead of activations; kills droplet artifacts. / 归一化卷积权重而非激活。 |
| Alias-free | "StyleGAN3's trick" / "StyleGAN3 技巧" | Windowed sinc filters; eliminates texture sticking to the pixel grid. / 窗口 sinc 滤波器消除纹理粘附。 |
| Inversion | "Find w for a real image" / "找 w" | Optimize or encode `x → w` so `G(w) ≈ x`. / 优化或编码使 `G(w) ≈ x`。 |

## Nota de producción: por qué StyleGAN todavía se envían en 2026

StyleGAN3 en una 4090 genera una cara de 10242 FFHQ en menos de 10 ms  `num_steps = 1`En términos de producción esta es la latencia de suelo para cualquier generador de imagen. Un tubo de decodificación SDXL + VAE de 50 pasos con la misma resolución es de ~ 3 segundos.**300× gap**, y para productos de dominio estrecho (servicios de avatares, tuberías de documentos de identificación, generación de caras de stock) gana en TCO.

> StyleGAN3 en 4090 arriba no hasta 10ms 生成 10242 人脸`num_steps = 1`, sin VAE 解码, sin交叉注意力──50 步 SDXL en la misma resolución de aproximadamente 3 segundos── esto es **300 倍差距**, en el producto de un área estrecha.

Dos consecuencias operativas:

> 两个运营后果:

- **No scheduler, no batcher.**El lote estático en la ocupación objetivo es óptimo. El lote continuo (esencial para los LLM y la difusión) proporciona cero beneficio porque cada solicitud tiene los mismos FLOPs.
  **无需调度器或批处理器。**静态批量最优──连续批处理(对 LLM 和扩散模型至关重要)零收益──
- **Truncation `ψ` is the safety knob.** `ψ < 0.7`En el caso de las muestras de una zona de distribución de la red de mapeo, el nivel de distribución de la muestra es el más bajo.`ψ`en la carga máxima, elevarla para usuarios premium.
  **截断 `ψ` 是安全旋钮。** `ψ < 0.7`Desde el mapa de la red de la gama estrecha 采样―― es el único 杆──高峰负载时降低 `ψ`, usuarios superiores en mejoras.

## Más Leer más Leer más

- [Karras et al. (2019). A Style-Based Generator Architecture for GANs](https://arxiv.org/abs/1812.04948) StyleGAN.
- [Karras et al. (2020). Analyzing and Improving the Image Quality of StyleGAN](https://arxiv.org/abs/1912.04958) StyleGAN2.
- [Karras et al. (2021). Alias-Free Generative Adversarial Networks](https://arxiv.org/abs/2106.12423) StyleGAN3.
- [Tov et al. (2021). Designing an Encoder for StyleGAN Image Manipulation](https://arxiv.org/abs/2102.02766) inversión e4e.
- [Sauer et al. (2022). StyleGAN-XL: Scaling StyleGAN to Large Diverse Datasets](https://arxiv.org/abs/2202.00273) StyleGAN-XL.
- [Huang et al. (2024). R3GAN: The GAN is dead; long live the GAN!](https://arxiv.org/abs/2501.05441) receta moderna de GAN mínimo.
