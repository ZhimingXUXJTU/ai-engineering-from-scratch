# Modelos de difusión  DDPM desde cero  Modelo de difusión  Implementación de DDPM desde cero

> Ho, Jain, Abbeel (2020) dio al campo una receta que no podía dejar de hacer. Destruye los datos con ruido en mil pequeños pasos. Entrenar una red neuronal para predecir el ruido. Invertir el proceso a la inferencia. Hoy en día cada imagen, video, 3D y modelo musical corriente en este bucle, posiblemente con flujo de coincidencia o trucos de consistencia en la parte superior.

> **【中文解读】**El proceso central de DDPM: con 1000 pasos a paso para dar datos adicionales a ruido, destruir datos, entrenar un ruido de previsión de red neuronal, sugerir el tiempo de eliminación de ruido en sentido contrario.

> **【拓展：扩散模型是当前 AI 生成的核心】**Estabilidad de difusión DALL-E 3 Midjourney Sora todo basado en el modelo de difusión DDPM prueba un simple objetivo de desinfección de ruido puede producir una capacidad de generación sorprendente

**Type:** Build / 构建型
**Languages:** Python
**Prerequisites:** Phase 3 · 02 (Backprop / 反向传播), Phase 8 · 02 (VAE)
**Time:** ~75 minutes

## El problema es la introducción del problema

¿ Quieres una muestra para ?`p_data(x)`Los GAN juegan un juego de mínimas que a menudo divergen. Los VAEs producen muestras borrosas de un decodificador gaussiano. Lo que realmente se quiere es un objetivo de entrenamiento que es (a) una sola pérdida estable (sin punto de sella, sin mínimas), (b) un límite inferior en `log p(x)`(por lo que tiene probabilidades), y (c) muestras que coinciden con la calidad de SOTA.

> ¿ Qué quieres ?`p_data(x)`La cantidad de datos que se pueden obtener en el proceso de compra de un producto es de aproximadamente un millón de dólares.`log p(x)`La calidad de la producción de la planta de la planta de la planta de la planta de la planta de la planta de la planta de la planta de la planta de la planta de la planta de la planta de la planta de la planta de la planta de la planta de la planta de la planta de la planta de la planta de la planta de la planta de la planta de la planta de la planta de la planta de la planta de la planta de la planta de la planta de la planta de la planta de la planta de la planta de la planta de la planta de la planta de la planta de la planta de la planta de la planta de la planta de la planta de la planta de la planta de la planta de la planta de la planta de la planta de la planta de la planta de la planta de la planta de la planta de la planta de la planta de la planta de la planta de la planta de la planta de la planta de la planta de la planta de la planta de la planta de la planta de la planta de la planta de la planta de la planta de la planta de la planta de la planta de la planta de la planta de la planta de la planta de la planta de la planta de la planta de la planta de la planta de la planta de la planta de la planta de la planta de la planta de la planta de la planta de la planta de la planta de la planta de la planta de la planta de la planta de la planta de la planta de la planta de la planta de la planta de la planta de la planta de la planta de la planta de la planta de la planta de la planta de la planta de la planta de la planta de la planta de la planta de la planta de la planta de la planta de la planta de la planta de la planta de la planta de la planta de la planta de la planta de la planta de la planta de la planta de la planta de la planta de la planta de la planta de la planta de la planta de la planta de la planta de la planta de la planta de la planta de la planta de la planta de la planta de la planta de la planta de la planta de la planta de la planta de la planta de la planta de la planta de la planta de la planta de la planta de la planta de la planta de la planta de la planta de la planta de la planta de la planta de la planta de la planta de la planta de la planta de la planta de la planta de la planta de la planta de la planta de la planta de la planta de

Sohl-Dickstein et al. (2015) tenía una respuesta teórica: definir una cadena de Markov `q(x_t | x_{t-1})`que gradualmente añade ruido Gaussian, y entrenar una cadena inversa`p_θ(x_{t-1} | x_t)`En el año 2020 se produjo muestras de última generación. En 2022 se convirtió en la difusión estable. En 2026 es el sustrato.

> Sohl-Dickstein (2015)  dio la respuesta teórica: definir la cadena de marcos de aumento gradual del ruido, entrenar contra la cadena hacia el ruido. Ho 等人 (2020) va a simplificar la pérdida a una línea de ruido de predicción.

> **【中文解读】**El proceso de tres pasos de DDPM: 1) proceso de avance  gradual aumento del ruido hasta que los datos se vuelven ruido puro; 2) entrenamiento aprender a predicir una red cada paso de ruido adicional; 3) proceso de avance  de ruido puro a ruido, para recuperar datos reales.

> **【拓展：从 DDPM 到实用扩散模型】**DDPM original论文在像素空间操作,速度慢(需要1000步去噪音) ;;三个关键改进使它成为实用工具:(1) DDIM(2020) se adoptará el número de pasos de 1000 降至20-50;(2) 潜在扩散(2021,Rombach) en VAE 潜在空间操作,大幅降低计算量;(3) CFG(Classifier-Free Guidance,2022) 通过条件/无条件预测的差提升生成质量;;

## El concepto central.

![DDPM: forward noise, reverse denoise](../assets/ddpm.svg)

**Forward process `q`.**Añadir el ruido Gaussian `T`La forma cerrada  la razón por la que la matemática es tratable  es que el paso acumulativo es también gaussiano:

> **前向过程 `q`。**En el`T`Los pasos pequeños en el que se añade el ruido son los siguientes:

```
q(x_t | x_0) = N( sqrt(α̅_t) · x_0,  (1 - α̅_t) · I )
```

donde`α̅_t = ∏_{s=1..t} (1 - β_s)`para un calendario de `β_t`- Escoge .`β_t`de 1e-4 a 0,02 linealmente en T=1000 pasos y `x_T`es aproximadamente `N(0, I)`¿ Qué ?

> Entre ellos `α̅_t = ∏_{s=1..t} (1 - β_s)`¿Qué es esto?`β_t`Desde 1e-4 hasta 0,02 线性排列 T=1000 步,`x_T`Como si fuera`N(0, I)`¿Qué es eso?

**Reverse process `p_θ`.**Aprenda una red neuronal .`ε_θ(x_t, t)`que predice el ruido que se agregó.`x_t`, se denota por:

> **反向过程 `p_θ`。**Aprender una red neuronal`ε_θ(x_t, t)`预测添加的噪音──给定 `x_t`, de modo ruidoso:

```
x_{t-1} = (1 / sqrt(α_t)) · ( x_t - (β_t / sqrt(1 - α̅_t)) · ε_θ(x_t, t) )  +  σ_t · z
```

donde`σ_t`es cualquiera `sqrt(β_t)`La expresión es fea pero es sólo álgebra  resolver para `x_{t-1}`dado el posterior `q(x_{t-1} | x_t, x_0)`y sustituyendo `x_0`con su estimación de ruido prevista.

> Entre ellos `σ_t`Sí `sqrt(β_t)`O aprender a hacer diferencias. La expresión parece complicada, pero es sólo un número.`q(x_{t-1} | x_t, x_0)`求解   ¿ Qué es esto ?`x_{t-1}`¿Qué es eso?

**Training loss.**

```
L_simple = E_{x_0, t, ε} [ || ε - ε_θ( sqrt(α̅_t) · x_0 + sqrt(1 - α̅_t) · ε,  t ) ||² ]
```

Muestra `x_0`de los datos, elige un aleatorio `t`, muestra `ε ~ N(0, I)`, calcular el ruido .`x_t`En un tiro a través de la forma cerrada, y regresar al ruido.

> Desde datos`x_0`, con su elección`t`, así .`ε ~ N(0, I)`, a través de un cierre de un cálculo con ruido`x_t`, para el ruido hacer regreso. un perjuicio, sin mínimo, sin KL, sin técnicas de parámetros pesados.

**Sampling.**Comienza .`x_T ~ N(0, I)`. Iterar el paso inverso de `t = T`¿ Qué ?`1`- Ya lo he hecho.

> **采样。**Desde`x_T ~ N(0, I)`开始, desde `t = T`¿ Qué ?`1`代反向步骤──完成──

## ¿Por qué funciona ?

Tres intuiciones:

> Tres cosas directas:

1. **Denoising is easy; generating is hard.**En el`t=T`La red tiene que resolver un problema trivial.`t=0`La red sólo tiene que limpiar unos pocos píxeles.`t`, el problema es difícil pero la red tiene muchos gradientes que fluyen a través de los mismos pesos de cada nivel de ruido.
   **去噪容易，生成难。**En el`t=T`时, datos son ruidos puros 网络只需要解决简单的问题.`t=0`时, la red sólo necesita limpiar una pequeña cantidad de imágenes.

2. **Score matching in disguise.**Vincent (2011) demostró que predecir el ruido es equivalente a estimar `∇_x log q(x_t | x_0)`, el * puntaje*. El SDE inverso utiliza este puntaje para subir el gradiente de densidad  un paseo aleatorio guiado hacia regiones de alta probabilidad.
   **伪装的分数匹配。**预测 ruido igual al precio de la función de la estimación`∇_x log q(x_t | x_0)`❖ En contraposición a la SDE, utilizar este porcentaje a lo largo de la escala de densidad de aumento.

3. **The ELBO reduces to simple MSE.**El límite inferior de variación completa tiene un término KL por paso de tiempo. Con la parámetriz de DDPM, esos términos KL se simplifican a MSE en predicción del ruido con coeficientes específicos; Ho redujo los coeficientes (llamándolo pérdida "simplificada") y la calidad *mejorada*.
   **ELBO 简化为简单 MSE。**完整的变分下界 每个时间步都有 KL 项──Ho 丢弃系数后质量反而*提升*了──

## Construye y realiza.
```figure
diffusion-denoise
```

## Construye el mismo

`code/main.py`La red es una pequeña MLP que toma un`(x_t, t)`El entrenamiento es la pérdida de una línea.

> `code/main.py`实现 una dimensión DDPM. DATA es doble cumbre mixto. 网络 es un micro tipo de MLP, recepción `(x_t, t)`输出预测噪声──训练就是那一行损失──采样代反向链──

### Paso 1: el calendario anticipado (formulario cerrado)

```python
betas = [1e-4 + (0.02 - 1e-4) * t / (T - 1) for t in range(T)]
alphas = [1 - b for b in betas]
alpha_bars = []
cum = 1.0
for a in alphas:
    cum *= a
    alpha_bars.append(cum)
```

### Paso 2: muestra `x_t`en un solo disparo

```python
def forward_sample(x0, t, alpha_bars, rng):
    a_bar = alpha_bars[t]
    eps = rng.gauss(0, 1)
    x_t = math.sqrt(a_bar) * x0 + math.sqrt(1 - a_bar) * eps
    return x_t, eps
```

### Paso 3: un paso de entrenamiento

```python
def train_step(x0, model, alpha_bars, rng):
    t = rng.randrange(T)
    x_t, eps = forward_sample(x0, t, alpha_bars, rng)
    eps_hat = model_forward(model, x_t, t)
    loss = (eps - eps_hat) ** 2
    return loss, gradient_step(model, ...)
```

### Paso 4: muestreo inverso

```python
def sample(model, alpha_bars, T, rng):
    x = rng.gauss(0, 1)
    for t in range(T - 1, -1, -1):
        eps_hat = model_forward(model, x, t)
        beta_t = 1 - alphas[t]
        x = (x - beta_t / math.sqrt(1 - alpha_bars[t]) * eps_hat) / math.sqrt(alphas[t])
        if t > 0:
            x += math.sqrt(beta_t) * rng.gauss(0, 1)
    return x
```

Para un problema 1-D con 40 pasos de tiempo y una MLP de 24 unidades, esto aprende la mezcla de dos modos en ~200 épocas.

> 对于40 时间步和24 单元 MLP的一维问题,约200轮即可学会双峰混合──

## El tiempo está condicionado .

La red necesita saber qué paso de tiempo está denonizando.

> La red necesita saber en qué paso del tiempo está haciendo ruido.

- **Sinusoidal embedding.**Como el codificación de posición de Transformer.`embed(t) = [sin(t/ω_0), cos(t/ω_0), sin(t/ω_1), ...]`Pasar por una MLP, transmitir a la red.
  **正弦嵌入。**类似变压器 位置编码──
- **Film / group-norm conditioning.**El proyecto de incorporación a escala/bias por canal (FiLM) en cada bloque.
  **FiLM / 组归一化条件化。**Se incorporará proyección para cada canal de reducción/disminución.

Nuestro código de juguete usa sinusoidal → concat.

> Nuestro juego está en el cine.

## Enlaces.

- **Schedule matters a lot.**Lineal `β`Es el DDPM predeterminado pero el cronograma cosino (Nichol & Dhariwal, 2021) da una mejor FID para el mismo cálculo.
  **调度很重要。**线性   línea `β`Es DDPM 默认但余弦调度在相同计算量下 FID 更好──
- **Timestep embedding is fragile.**Pasando en bruto`t`como un flotador funciona para juguete 1-D pero no para imágenes; siempre use una incorporación adecuada.
  **时间步嵌入脆弱。**Originario`t`浮点数在玩具 1D可用但图像不行──
- **V-prediction vs ε-prediction.**Para regímenes estrechos (t muy pequeños o muy grandes), `ε`El sistema de predicción de V (`v = α·ε - σ·x`) es más estable; SDXL, SD3 y Flux lo utilizan.
  **V 预测 vs ε 预测。**En el extremo del tiempo, V 预测更稳定;SDXL、SD3、Flux usarlo―
- **Classifier-free guidance.**En la inferencia, calcular tanto condicional como incondicional `ε`, entonces`ε_cfg = (1 + w) · ε_cond - w · ε_uncond`con`w ≈ 3-7`- Se trata de la Lección 8.
  **无分类器引导。**推理时计算条件和无条件预测的差值──第 08 课详述──
- **1000 steps is a lot.**La producción utiliza DDIM (20-50 pasos), DPM-Solver (10-20 pasos) o destilación (1-4 pasos).
  **1000 步太多了。**Produción con DDIM ((20-50 步) 、DPM-Solver ((10-20 步) o蒸(1-4 步) ✿

## Usalo con el marco de ejecución

| Role / 角色 | Typical stack in 2026 / 2026 典型技术栈 |
|------|-----------------------|
| Image pixel-space diffusion (small, toy) / 像素空间扩散 | DDPM + U-Net |
| Image latent diffusion / 潜在扩散 | VAE encoder + U-Net or DiT (Lesson 07) |
| Video latent diffusion / 视频潜在扩散 | Spatiotemporal DiT (Sora, Veo, WAN) |
| Audio latent diffusion / 音频潜在扩散 | Encodec + diffusion transformer |
| Science (molecules, proteins, physics) / 科学 | Equivariant diffusion (EDM, RFdiffusion, AlphaFold3) |

La difusión es la columna vertebral generativa universal. La coincidencia de flujo (lección 13) es el competidor 2024-2026 que generalmente gana en velocidad de inferencia por la misma calidad.

> 扩散是通用生成骨干;;Flow Matching (第 13 课) es el competidor de 2024-2026, generalmente con la misma calidad.

## Envíe el producto .

Salva .`outputs/skill-diffusion-trainer.md`. La habilidad toma un conjunto de datos + presupuesto y resultados de cálculo: horario (lineal/cosino/sigmoide), objetivo de predicción (ε/v/x), número de pasos, escala de orientación, familia de muestras y un protocolo de evaluación.

> 保存 `outputs/skill-diffusion-trainer.md`Habilidad para recibir datos + presupuesto de cálculo, producción de datos, objetivos de previsión, pasos, reducción de datos, grupos de datos y protocolo de evaluación.

## Los ejercicios.

1. **Easy / 简单.**Cambiar T de 40 a 10 en `code/main.py`¿Cómo se degrada la calidad de la muestra (histograma visual de las salidas)?
   ¿Cómo se degrada la calidad de la muestra? ¿En qué estructura se derrumbe la estructura de las dos cimas?
2. **Medium / 中等.**Cambiar de la predicción ε a la predicción v. Retomar el paso inverso. Comparar la calidad final de la muestra.
   Desde ε 预测切换到v 预测──重新推导反向步骤──比较最终样本质量──
3. **Hard / 困难.**Añadir una guía sin clasificador. Condición en una etiqueta de clase `c ∈ {0, 1}`, bajar el 10% del tiempo durante el entrenamiento y en el tiempo de muestreo de uso `ε = (1+w)·ε_cond - w·ε_uncond`. Medir la tasa de impacto en el modo condicional en `w = 0, 1, 3, 7`¿ Qué ?
   添加无分类器引导──测量 `w = 0, 1, 3, 7`时的条件模式命中率──

## Términos clave .

| Term / 术语 | What people say / 俗称 | What it actually means / 实际含义 |
|------|-----------------|-----------------------|
| Forward process | "Adding noise" / "加噪" | Fixed Markov chain `q(x_t \| x_{t-1})` that destroys the data. / 破坏数据的固定马尔可夫链。 |
| Reverse process | "Denoising" / "去噪" | Learned chain `p_θ(x_{t-1} \| x_t)` that reconstructs the data. / 重建数据的学习链。 |
| β schedule | "The noise ladder" / "噪声阶梯" | Per-step variance; linear, cosine, or sigmoid. / 每步方差；线性、余弦或 S 形。 |
| α̅ | "Alpha bar" | Cumulative product `∏(1 - β)`; gives closed-form `x_t` from `x_0`. / 累积乘积，给出闭式 `x_t`。 |
| Simple loss | "MSE on noise" / "噪声 MSE" | `\|\|ε - ε_θ(x_t, t)\|\|²`; all variational derivations collapse to this. / 所有变分推导最终坍塌为此。 |
| ε-prediction | "Predict noise" / "预测噪声" | Output is the noise added; standard DDPM. / 输出是添加的噪声。 |
| V-prediction | "Predict velocity" / "预测速度" | Output is `α·ε - σ·x`; better conditioning across t. / 跨时间步条件化更好。 |
| DDPM | "The paper" / "那篇论文" | Ho et al. 2020; linear β, 1000 steps, U-Net. |
| DDIM | "Deterministic sampler" / "确定性采样器" | Non-Markov sampler, 20-50 steps, same training objective. / 非马尔可夫采样器。 |
| Classifier-free guidance | "CFG" | Mix conditional and unconditional noise predictions to amplify conditioning. / 混合条件和无条件预测以放大条件化。 |

## Nota de producción: la inferencia de difusión es un problema de recuento de pasos.

El documento DDPM ejecuta T=1000 pasos invertidos. Nadie envía eso en producción. Cada pila de inferencias real elige una de tres estrategias  y cada mapa limpio a la producción de enmarcado de "de dónde viene la latencia":

> DDPM 论文 T=1000 反向步──生产中没有人这样做──每种策略对应生产中"延迟来自哪里":

1. **Faster sampler, same model.**DDIM (20-50 pasos), DPM-Solver++ (10-20), UniPC (8-16).`ε_θ`Los pesos están intactos, reduce la latencia 20 a 50 veces.
   **更快的采样器，相同模型。**DDIM、DPM-Solver++、UniPC──即插即用替换反向循环,降低延迟 20-50 倍──
2. **Distillation.**Entrenar a un estudiante a coincidir con el maestro en menos pasos: Distillación progresiva (2 → 1), Modelos de consistencia (arbitrario → 1-4), LCM, SDXL-Turbo, SD3-Turbo.
   **蒸馏。**訓練学生模型在更少步数匹配教师──再降延迟 5-10 倍,需要重训──
3. **Caching and compilation.** `torch.compile(unet, mode="reduce-overhead")`, los retrocesos de difusión de TensorRT-LLM,`xformers`/SDPA atención, bf16 pesos. Cortes por paso latencia ~ 2×.
   **缓存和编译。**Torch.compile、TensorRT、xformers、bf16──降低每步延迟约2倍──

Para un servidor de difusión de producción la conversación presupuestaria es la misma que la literatura de producción describe para LLM: la latencia es `num_steps × step_cost + VAE_decode`, el rendimiento es `batch_size × (num_steps × step_cost)^-1`. TTFT es pequeño (un paso); TPOT-equivalente es el tiempo de respuesta completo porque la generación de imágenes es "todo a la vez" desde la perspectiva del usuario.

> El presupuesto de la empresa de servicios de producción y de expansión de servicios de servicios de producción y de distribución de productos en el mercado de la empresa de servicios de producción y de distribución de productos en el mercado de la empresa de servicios de producción y de distribución de productos en el mercado de la empresa de servicios de producción y de distribución de productos en el mercado de la empresa de servicios de producción y de distribución de productos en el mercado de la empresa de servicios de producción y de distribución de productos en el mercado de la empresa de servicios de producción y de producción en el mercado de servicios de producción y de producción en el mercado de servicios de producción en el mercado de servicios de producción y de producción en el mercado de la empresa de servicios de servicios de producción en el mercado de la empresa de servicios de producción en el mercado de la empresa de servicios de producción en el mercado de la empresa de servicios de producción de servicios de producción en el mercado de la empresa de la empresa de la empresa de la empresa de la empresa de producción de la empresa de la empresa de la empresa de la empresa de la empresa de la empresa de la empresa de la empresa de la empresa de la empresa de la empresa de la empresa de la empresa de la empresa de la empresa de la empresa de la empresa de la empresa de la empresa de la empresa de la empresa de la empresa de la empresa de la empresa de la empresa de la empresa de la empresa de la empresa de la empresa de la empresa de la empresa de la empresa de la empresa de la empresa de la empresa de la empresa de la empresa de la empresa de la empresa de la empresa de la empresa de la empresa de la empresa de la empresa de la empresa de la empresa de la empresa de la empresa de la empresa de la empresa de la empresa de la empresa de la empresa de la empresa de la empresa de la empresa de la empresa de la empresa de la empresa de la empresa de la empresa de la empresa de la empresa de la empresa de la empresa de la empresa de la empresa de la empresa de la empresa de la empresa de la empresa de la empresa de la empresa de la empresa de la empresa de la empresa de la empresa de la empresa de la empresa de la empresa de la empresa de la empresa de la empresa de la marca de la marca de la marca de la marca de la marca de la marca de la marca de la marca de la marca de la marca de la marca de la marca de la marca de la marca de la marca de la marca de la marca de la marca de`num_steps × step_cost + VAE_decode`△TTFT 很小(一步);TPOT 等价物是完整响应时间──

## Más Leer más Leer más

- [Sohl-Dickstein et al. (2015). Deep Unsupervised Learning using Nonequilibrium Thermodynamics](https://arxiv.org/abs/1503.03585) el papel de difusión, antes de su tiempo.
- [Ho, Jain, Abbeel (2020). Denoising Diffusion Probabilistic Models](https://arxiv.org/abs/2006.11239) DDPM.
- [Song, Meng, Ermon (2021). Denoising Diffusion Implicit Models](https://arxiv.org/abs/2010.02502) DDIM, menos pasos.
- [Nichol & Dhariwal (2021). Improved DDPM](https://arxiv.org/abs/2102.09672) horario cosino, variación aprendida.
- [Dhariwal & Nichol (2021). Diffusion Models Beat GANs on Image Synthesis](https://arxiv.org/abs/2105.05233) Orientación del clasificador.
- [Ho & Salimans (2022). Classifier-Free Diffusion Guidance](https://arxiv.org/abs/2207.12598) CFG.
- [Karras et al. (2022). Elucidating the Design Space of Diffusion-Based Generative Models (EDM)](https://arxiv.org/abs/2206.00364) Notas unificadas, receta más limpia.
