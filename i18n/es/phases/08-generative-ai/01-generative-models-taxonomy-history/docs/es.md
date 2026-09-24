# Modelos generales  Taxonomía e historia  生成模型  类与历史

> Cada modelo de imagen, modelo de texto, modelo de video y modelo 3D encaja en uno de los cinco baldes. Elige el balde equivocado y lucharás las matemáticas durante semanas. Elige el correcto y los últimos doce años de progreso del campo se apilarán limpio en tu cabeza.

> **【中文解读】**Todas las imágenes, textos, vídeos y modelos de producción en 3D se pueden clasificar en cinco categorías: VAE, GAN, modelo de expansión, modelo de flujo y modelo de auto-regreso.

> **【拓展：生成式 AI 的五大路线】**(1) VAE变分自编码器,Stable Diffusion的编码器;(2) GAN生成对抗网络,StyleGAN的核心;(3) 扩散模型DDPM/DDIM,当前图像生成主流;(4) 流模型Flow Matching,SD3/FLUX的新方向;(5) 自归GPT 模式,VAR 应用于图像──

**Type:** Learn / 学习型
**Languages:** Python
**Prerequisites:** Phase 2 (ML Fundamentals / 机器学习基础), Phase 3 (Deep Learning Core / 深度学习核心), Phase 7 · 14 (Transformers / Transformer)
**Time:** ~45 minutes

## El problema es la introducción del problema

Un modelo generativo hace un trabajo: muestra de formación dada extraída de una distribución desconocida `p_data(x)`Las caras, las frases, los archivos MIDI, las estructuras de proteínas, todo el mismo problema si miras con los ojos.

> El modelo de producción sólo hace una cosa: se determina de una distribución desconocida.`p_data(x)`En el extrato de la muestra de entrenamiento, la salida parece venir de la misma distribución de la nueva muestra.

El problema es que ...`p_data`Si el modelo de un modelo generativo es un modelo generativo, es un compromiso que cambia un problema difícil por otro ligeramente menos difícil.

>  El problema está en `p_data`Existe en un espacio de varios millones de dimensiones ([[1张 512x512 RGB 图像约78.6万维)) , el modelo solo ocupa una tenue forma de flujo en ese espacio, mientras que es posible que solo tenga un millón de muestras. La densidad de la calculación de violencia es desesperada.

Cinco familias han sobrevivido en los últimos doce años. Saber qué compromiso hace cada familia nos dice por qué gana en algunas tareas y se derrumba en otras.

> En los últimos 12 años, cinco familias modelo han sobrevivido. Conocer lo que cada familia ha hecho es comprobar por qué ha triunfado en ciertas tareas y se ha desmoronado en otras.

> **【中文解读】**El trabajo central del modelo de producción es aprender la distribución desconocida de datos p_data (x) en el modelo de entrenamiento, para luego generar nuevos datos de la misma distribución. El reto es que el modelo de producción de datos es de gran tamaño.

> **【拓展：从扩散模型到 Flow Matching 的范式转移】**La tendencia más importante del 2024-2026 es la de la difusión del modelo (DDPM) hacia el flujo de coincidencia (Flow Matching) 流匹配 (Flow Matching) 流匹配 (Flow Matching) 训练更简单 (No necesita ruido) 采样路径更直 (更少步数) 速度提升 4-10 倍 (倍) △Stable Diffusion 3、FLUX、AudioCraft 2 已 adoptado el flujo de coincidencia (Flow Matching)).

## El concepto central.

![Five families of generative models — taxonomy by what they model](../assets/taxonomy.svg)

**1. Explicit density, tractable.**Escriba .`log p(x)`Los modelos autoregresivos (PixelCNN, WaveNet, GPT) factorizan`p(x) = ∏ p(x_i | x_<i)`. Normalización de los flujos (RealNVP, Glow)`p(x)`Pro: probabilidad exacta, pérdida de entrenamiento limpia. Con: inferencia autorregresista es secuencial (lento para secuencias largas), los flujos necesitan arquitecturas invertibles (arquitectónicamente restrictivas).

> **1. 显式密度，可处理。**¿ Qué ?`log p(x)`写成可以实际求值的求和──自归归模型(PixelCNN、WaveNet、GPT) se dividirá en la distribución conjunta dividida en la distribución de la multiplicidad de la condición──标准化流(RealNVP、Glow) a través de la distribución simple de la transformación de la estructura`p(x)`△优点:精确似然,训练损失清晰──缺点:自归推理是顺序的(长序列慢),流需要可逆架构(架构受限)。

**2. Explicit density, approximate.**Enlazado`log p(x)`Los modelos de difusión (DDPM, Ho 2020) entrenan un denoizador que optimiza implícitamente un ELBO ponderado. La difusión es la columna vertebral dominante de la imagen, el video y la 3D en 2026.

> **2. 显式密度，近似。**Desde abajo`log p(x)`El modelo de expansión es el modelo de 2026 de imágenes, vídeos y 3D.

**3. Implicit density.**Salta la densidad por completo; aprende un generador `G(z)`que produce muestras y un discriminador `D(x)`GANs (Goodfellow 2014). Rápido en la inferencia (un pase hacia adelante) pero notoriamente inestable durante el entrenamiento. StyleGAN 1/2/3 sigue siendo el estado de la técnica para el fotorrealismo de dominio fijo (caras, dormitorios) incluso en 2026.

> **3. 隐式密度。** completamente saltar por encima de la estimación de densidad; aprender un generador `G(z)` producirse muestras, un juez `D(x)`区分真假──GAN 推理快(单次前向传播), pero el entrenamiento es muy inestable──StyleGAN 1/2/3 incluso en 2026 sigue siendo el modelo más avanzado de la realidad del nivel de la fotografía de un dominio fijo──

**4. Score-based / continuous-time.**Aprenda el gradiente de la densidad de troncos `∇_x log p(x)`Song & Ermon (2019) mostró que la coincidencia de puntajes generaliza la difusión a una SDE. La coincidencia de flujo (Lipman 2023) es la calidez 2024-2026: entrenamiento sin simulación, caminos más recta, muestreo 4-10 veces más rápido que DDPM.

> **4. 基于分数/连续时间。**直接学习对数密度的梯度 (分数函数) ――Song & Ermon (2019) 证明分数匹配将扩散推广到 SDE──Flow Matching(2023) es el curso de 2024-2026 en el que se desarrollará un entrenamiento de flujo, más directo que el DDPM 快 4-10 倍──Stable Diffusion 3、Flux、AudioCraft 2 都使用Flow Matching──

> **【中文解读】**La combinación de números y flujos es la generalización y mejora del modelo de difusión. La combinación de números y flujos simplificó aún más el proceso de entrenamiento.

**5. Token-based autoregressive over discrete codes.**Compresar datos de alto tamaño con un VQ-VAE o cuantificador residual en una secuencia corta de tokens discretos, luego usar un transformador para modelar la secuencia de tokens. Parti, MuseNet, AudioLM, VALL-E, el tokenizer de parches de Sora todos usan esto. Este es balde 1 más un tokenizer aprendido.

> **5. 基于离散 token 的自回归。**Usando VQ-VAE o residuoquizador se comprimirán datos de alto nivel en una serie corta de tokens despartidos, y luego se utilizarán los tokens de parche de los tokens de los tokens de parche de los tokens de parche de parte, museNet, audioLM, val-e, sora.

## Una breve historia.

| Year / 年份 | Model / 模型 | Why it mattered / 重要意义 |
|------|-------|-----------------|
| 2013 | VAE (Kingma) | First deep generative model with a usable training loss. / 首个具有可用训练损失的深度生成模型。 |
| 2014 | GAN (Goodfellow) | Implicit density, no likelihood — shockingly sharp samples. / 隐式密度，无需似然——惊人的锐利样本。 |
| 2015 | DRAW, PixelCNN | Sequential image generation. / 顺序图像生成。 |
| 2017 | Glow, RealNVP | Invertible flows; exact likelihood with depth. / 可逆流；深度带来精确似然。 |
| 2017 | Progressive GAN | First megapixel faces. / 首个百万像素人脸。 |
| 2019 | StyleGAN / StyleGAN2 | Photorealistic faces still hard to beat for that one domain. / 照片级真实人脸，该领域至今难以超越。 |
| 2020 | DDPM (Ho) | Diffusion becomes practical. / 扩散模型变得实用。 |
| 2021 | CLIP, DALL-E 1, VQGAN | Text-to-image goes mainstream. / 文本生成图像走向主流。 |
| 2022 | Imagen, Stable Diffusion 1, DALL-E 2 | Latent diffusion + text conditioning = commodity. / 潜在扩散 + 文本条件 = 大众化。 |
| 2022 | ControlNet, LoRA | Fine control over pretrained diffusion. / 对预训练扩散模型的精细控制。 |
| 2023 | SDXL, Midjourney v5, Flow matching | Scale + better training dynamics. / 规模化 + 更好的训练动态。 |
| 2024 | Sora, Stable Diffusion 3, Flux.1 | Video diffusion; flow matching wins. / 视频扩散；Flow Matching 胜出。 |
| 2025 | Veo 2, Kling 1.5, Runway Gen-3, Nano Banana | Production-grade video. / 生产级视频。 |
| 2026 | Consistency + Rectified Flow | One-step sampling from diffusion backbones. / 从扩散骨干实现单步采样。 |

## El proceso de clasificación de cinco preguntas.

Cuando se produzca un nuevo modelo generativo, responda a estas cinco preguntas antes de leer la sección de métodos.

> Cuando se publique un nuevo trabajo sobre el modelo de generación, primero responda a estas cinco preguntas antes de leer la sección de métodos.

1. **What is being modeled?**¿Pixels, latences, tokens discretos, Gaussians 3D, redes, formas de onda?
   **正在建模什么？**¿Cómo se puede decir que se puede decir que se puede decir que se puede decir que se puede decir que se puede decir que se puede decir que se puede decir que se puede decir que se puede decir que se puede decir que se puede decir que se puede decir que se puede decir que se puede decir que se puede decir que se puede decir que se puede decir que se puede decir que se puede decir que se puede decir que se puede decir que se puede decir que se puede decir que se puede decir que se puede decir que se puede decir que se puede decir que se puede decir que se puede decir que se puede que se puede decir que se puede que se puede decir que se puede que se puede que se puede que se puede que sea que se puede que se puede que sea que sea que sea que sea que sea que sea que sea que sea que sea que sea que sea que sea que sea que sea que sea que sea?
2. **Is the density explicit or implicit?**¿ Se escriben ?`log p(x)`¿ Qué ?
   **密度是显式还是隐式的？**¿Eran los que escribieron?`log p(x)`¿ Qué ?
3. **Sampling: one-shot or iterative?**Iterativo significa inferencia más lenta; un tiro generalmente significa adversario o destilado.
   **采样：单次还是迭代？**代 significa pensar más lento;单次 normalmente significa oposición o disti──
4. **Conditioning: unconditional, class, text, image, pose?**Esto determina la pérdida y el andamio de la arquitectura.
   **条件：无条件、类别、文本、图像、姿态？**Esto determina la función de pérdida y el marco de la estructura.
5. **Evaluation: FID, CLIP score, IS, human preference, task accuracy?**Cada uno tiene modos de fallo conocidos (véase la Lección 14).
   **评估：FID、CLIP Score、IS、人类偏好、任务准确率？**Cada uno tiene un modelo de fallo de eficacia conocido (véase la sección 14)

Responda a estas cinco preguntas para cada lección en esta fase.

> En cada sección de esta etapa, responderás de nuevo a estas cinco preguntas. Al final, se convertirán en tu instinto.

> **【中文解读】**Estas cinco preguntas (construcción de objetos de modelado, densidad de manifiesto/impreso, tipo de modelo, tipo de condiciones, indicador de evaluación) son un marco general para analizar cualquier modelo generado. Respondiendo repetidamente a estas cinco preguntas en cada sección posterior, puede ayudarle a comprender rápidamente la contribución y la selección técnica del nuevo trabajo.

## Construye y realiza.
```figure
autoencoder-bottleneck
```

## Construye el mismo

El código para esta lección es una visualización ligera: ajusta una mezcla de Gaussis de 1D de muestras utilizando tres enfoques de juguete (densidad del núcleo, histograma discreto y generador de "GAN-ish" de la muestra más cercana) para que puedas ver la diferencia entre la densidad explícita vs implícita en un problema que puedes imprimir en una pantalla.

> El código de esta clase es una visualización de nivel ligero: utiliza tres métodos simples:                                                                                                                                                                                                                                                     

- ¿ Qué ?`code/main.py`Se extraen 2000 muestras de una mezcla gaussiana de dos modos, y luego se imprimen:

> 运行                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           `code/main.py`❖ Extrajo 2000 muestras de la mezcla de dos picos y luego imprimió:

```
explicit density (histogram): p(x in [-0.5, 0.5]) ≈ 0.38
approximate density (KDE):     p(x in [-0.5, 0.5]) ≈ 0.41
implicit (nearest-sample gen): 20 new samples printed, no p(x)
```

Nota: las dos primeras te permiten preguntar "¿qué probabilidades tiene este punto?" La tercera no puede. Esta es la distinción *explicita vs implícita* que será importante para cada lección futura.

> Nota: los dos primeros métodos pueden responder "¿qué probabilidad tiene este punto?" el tercer no puede.

## Usalo con el marco de ejecución

¿Qué familia, para qué tarea, en 2026?

> 2026 años, ¿qué familia se adapte a qué tarea?

| Task / 任务 | Best family / 最佳家族 | Why / 原因 |
|------|-------------|-----|
| Photoreal faces, narrow domain / 照片级人脸，窄域 | StyleGAN 2/3 | Still sharpest, fastest inference. / 仍然最锐利，推理最快。 |
| General text-to-image / 通用文本生成图像 | Latent diffusion + flow matching | SD3, Flux.1, DALL-E 3. |
| Fast text-to-image / 快速文本生成图像 | Rectified flow + distillation | SDXL-Turbo, SD3-Turbo, LCM. |
| Text-to-video / 文本生成视频 | Diffusion Transformer + flow matching | Sora, Veo 2, Kling. |
| Speech + music / 语音+音乐 | Token-based AR (AudioLM, VALL-E, MusicGen) or flow matching (AudioCraft 2) | Discrete tokens scale cheaply. / 离散 token 扩展成本低。 |
| 3D scenes / 3D 场景 | Gaussian Splatting fit, diffusion prior | 3D-GS for reconstruction, diffusion for novel-view. / 3D-GS 用于重建，扩散用于新视角。 |
| Density estimation (no sampling) / 密度估计（不采样） | Flows | Only family with exact `log p(x)`. / 唯一有精确 `log p(x)` 的家族。 |
| Simulation / physics / 模拟/物理 | Flow matching, score SDE | Straight-line paths, smooth vector fields. / 直线路径，平滑向量场。 |

## Envíe el producto .

Salvo como`outputs/skill-model-chooser.md`¿ Qué ?

> 保存为                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           `outputs/skill-model-chooser.md`¿Qué es eso?

La habilidad toma una descripción de tarea y resultados: (1) qué familia utilizar, (2) una lista clasificada de tres opciones abiertas y tres alojadas, (3) el modo probable de fracaso que debe mirar, y (4) un presupuesto de cálculo/tiempo.

> La habilidad  recepción  tarea descripción,输出: 1) 应使用哪个家族, 2) 三个开源和三个托管选项的排序列表, 3) 应注意的可能失效模式, 4) 计算/时间预算.

## Los ejercicios.

1. **Easy / 简单.**Para cada uno de estos cinco productos, identifique la familia y la columna vertebral: imagen ChatGPT, Midjourney v7, Sora, Runway Gen-3, ElevenLabs.
   对于这五个产品,识别其家族和骨干:ChatGPT image、Midjourney v7、Sora、Runway Gen-3、ElevenLabs──证据应来自公开技术报告──
2. **Medium / 中等.**El artículo que vas a leer mañana recomienda una muestreo 100 veces más rápida que la difusión.
   Tu mañana leer el artículo afirma que se expande 100 veces más rápido que el ejemplar. Escriba los siguientes tres problemas para comprobar si la aceleración sigue existiendo bajo condiciones de generación y alta resolución.
3. **Hard / 困难.**Tome un dominio que le importe (por ejemplo, estructura de proteínas, CAD, moléculas, trayectorias). Responde al triaje de cinco preguntas para el modelo SOTA actual en ese dominio y esboce qué cambiaría un modelo mejor.
   选择一个你关心的领域 (如蛋白质结构,CAD,分子轨迹) ⋅ En este campo, el modelo actual de SOTA responde a cinco preguntas y dibuja un modelo mejor que pueda cambiar lo que sea.

## Términos clave .

| Term / 术语 | What people say / 俗称 | What it actually means / 实际含义 |
|------|-----------------|-----------------------|
| Generative model | "It makes new stuff" / "它生成新东西" | Learns a sampler for `p_data(x)`, optionally exposes `log p(x)`. / 学习 `p_data(x)` 的采样器，可选暴露 `log p(x)`。 |
| Explicit density | "You can evaluate it" / "可以计算" | Model provides a closed-form or tractable `log p(x)`. / 模型提供闭式或可处理的 `log p(x)`。 |
| Implicit density | "GAN-style" / "GAN 风格" | Only a sampler — no way to evaluate `p(x)` of a given point. / 只有采样器——无法计算给定点的 `p(x)`。 |
| ELBO | "Evidence lower bound" / "证据下界" | A tractable lower bound on `log p(x)`; VAEs and diffusion optimize it. / `log p(x)` 的可处理下界；VAE 和扩散模型优化它。 |
| Score | "Gradient of log-density" / "对数密度梯度" | `∇_x log p(x)`; diffusion and SDE models learn this field. / 扩散和 SDE 模型学习这个场。 |
| Manifold hypothesis | "Data lives on a surface" / "数据在曲面上" | High-dim data concentrates on a low-dim manifold; why dimensionality reduction works. / 高维数据集中在低维流形上；降维有效的原因。 |
| Autoregressive | "Predict the next piece" / "预测下一个" | Factorize joint as product of conditionals. / 将联合分布分解为条件分布的乘积。 |
| Latent | "Compressed code" / "压缩编码" | Low-dim representation from which a decoder can reconstruct the input. / 解码器可从中重建输入的低维表示。 |

## Nota de producción: cinco familias, cinco formas de inferencia

Cada familia hace mapas a una curva de costos inferencia-servidor diferente. La literatura de producción-inferencia enmarca la inferencia LLM como preempleo + decodificación; la misma descomposición se aplica aquí:

> Cada familia se adapta a diferentes tipos de cálculo de costos de servidores.

- **Autoregressive (bucket 1 and 5).**El decodificación secuencial domina la latencia; el caché KV, el batch continuo y el decodificación especulativa se aplican directamente.
  **自回归（第 1 和 5 类）。**顺序解码主导延迟;KV 缓存、连续批处理和推测解码直接适用──
- **VAE / diffusion / flow-matching (buckets 2 and 4).**No hay decodificación en el sentido de LLM.`num_steps × step_cost`, y el `step_cost`Los botones de producción son el recuento de pasos (DDIM / DPM-Solver / destilación), el tamaño del lote y la precisión (bf16 / fp8 / int4).
  **VAE / 扩散 / Flow Matching（第 2 和 4 类）。**LLM 意义上没有解码──成本 = `num_steps × step_cost`, la producción de la regla de giro es el número de pasos, la cantidad de tamaño y la precisión.
- **GAN (bucket 3).**No hay cronograma, no hay caché KV, TTFT ≈ latencia total, por eso StyleGAN sigue ganando en el uso de dominio estrecho.
  **GAN（第 3 类）。**单次前向传播──没有调度,没有 KV 缓存──TTFT ≈ 总延迟──这是StayGAN在狭域UX上仍然胜出的原因──

Cuando vea "más rápido que la difusión" en un resumen de papel, traduzca a "menos pasos × el mismo costo del paso" o "los mismos pasos × el costo del paso más barato".

> Cuando el resumen del artículo dice "quando es más rápido que se expande", se traduce como "menos pasos × costos de comparación" o "el mismo paso × costos de pasos más baratos"―, el resto es de comercialización―.

## Más Leer más Leer más

- [Goodfellow et al. (2014). Generative Adversarial Nets](https://arxiv.org/abs/1406.2661) el papel GAN.
- [Kingma & Welling (2013). Auto-Encoding Variational Bayes](https://arxiv.org/abs/1312.6114) el documento de la AEV.
- [Ho, Jain, Abbeel (2020). Denoising Diffusion Probabilistic Models](https://arxiv.org/abs/2006.11239) el documento del DDPM.
- [Song et al. (2021). Score-Based Generative Modeling through SDEs](https://arxiv.org/abs/2011.13456) difusión como SDE.
- [Lipman et al. (2023). Flow Matching for Generative Modeling](https://arxiv.org/abs/2210.02747) el papel de correspondencia de flujo.
- [Esser et al. (2024). Scaling Rectified Flow Transformers for High-Resolution Image Synthesis](https://arxiv.org/abs/2403.03206) Difusión estable 3.
