# Autoencoders y Autoencoders Variables (VAE) ✓ Autencoders y cambios

> Un autoencoder simple comprime y luego reconstruye. Memora. No genera. Añade un truco  fuerza el código para que parezca gaussiano  y obtienes un muestreo. Ese truco único, la reparameterización de `z = mu + sigma * epsilon`, es por eso que cada modelo de difusión latente y de coincidencia de flujo de imagen que utilices en 2026 tiene un VAE en la entrada.

> **【中文解读】**Normalmente, el auto-codificador se vuelve a construir, sólo re-construye memoria, no puede generarse.`z = mu + sigma * epsilon`La escala puede atravesar el proceso de entrenamiento, es la clave de la formación de VAE.

> **【拓展：VAE 是 Stable Diffusion 的基石】**2026 años Todos los modelos de expansión potencial ((Stable Diffusion、FLUX) están en funcionamiento en el espacio potencial de VAE.

**Type:** Build / 构建型
**Languages:** Python
**Prerequisites:** Phase 3 · 02 (Backprop / 反向传播), Phase 3 · 07 (CNNs / 卷积神经网络), Phase 8 · 01 (Taxonomy / 分类)
**Time:** ~75 minutes

## El problema es la introducción del problema

Comprimir un dígito MNIST de 784 píxeles a un código de 16 números, luego reconstruir. Un autoencoder simple hará la reconstrucción de MSE pero el espacio de código es un lío agudo. Elige un punto aleatorio en el espacio de código, decodifica, y obtienes ruido. No tiene muestreo. Es un modelo de compresión disfrazado.

> El MNIST de 784 像素 se acumulará en 16 números de código reconstruido.

Lo que realmente quieres es: (a) el espacio de código es una distribución limpia y suave que puedes tomar de un isotrópico gaussiano`N(0, I)`, (b) la descifrada de cualquier muestra produce un dígito plausible, y (c) el codificador y el decodificador todavía comprimen bien.

> Lo que realmente quieres es: a) Codificar espacio es limpio, plano, disponible y distribuido, como en el caso de los grupos de sexo.`N(0, I)`• b) 解码任何样本都产生合理数字; c) 编码器和码器仍压缩良好──三个目标,一个架构,一个损失──

El VAE de Kingma 2013 resuelve esto entrenando al codificador para emitir una *distribución* `q(z|x) = N(μ(x), σ(x)²)`, tirando esa distribución hacia el prior`N(0, I)`a través de una penalización KL, y luego muestreo `z`de la`q(z|x)`En el momento de la inferencia, deja caer el codificador, muestra`z ~ N(0, I)`La pena KL es lo que obliga a estructurar el espacio de código.

> Kingma 2013 años de VAE                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                       `q(z|x) = N(μ(x), σ(x)²)`Para resolver este problema, a través de KL, el castigo se distribuirá hacia el futuro.`N(0, I)`, y luego desde `q(z|x)`En el caso de la`z`Recomiendo, abandonando el codificador, desde`N(0, I)`采样                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           `z`,解码──KL 惩罚正是使编码空间结构化的关键──

En 2026 los VAEs rara vez envían de forma independiente  han sido superados por difusión por calidad de imagen en bruto  pero son el codificador de elección para cada modelo de difusión latente (SD 1/2/XL/3, Flux, AudioCraft). Aprende el VAE y aprendes la primera capa invisible de cada pipeline de imágenes que utilizas.

> En 2026 años VAE                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        

> **【中文解读】**La visión central de la VAE: hacer que el codificador salga distribuido y no estimado.`z = mu + sigma * epsilon`En el caso de las redes de distribución, el tamaño de la base de la base de datos se puede calcular en un punto de vista de la base de datos.

> **【拓展：beta-VAE 与解耦表示学习】**beta-VAE(2017) a través de la regulación de beta parámetros control reconstrucción con el peso de KL;;beta<1 时重建更清晰但潜在空间不规整;beta>1 时潜在空间更规整但图像更模糊;; Cuando beta 足够大时,VAE puede aprender a "descombrar" el indicio de cada dimensión codificando factores de significado independientes (((como color, forma, tamaño) ⋅ Esto inspiró el modelo de expansión posterior para hacer una generación controlable en el espacio potencial;;

## El concepto central.

![Autoencoder vs VAE: the reparameterization trick](../assets/vae.svg)

**Autoencoder.** `z = encoder(x)`¿ Qué ?`x̂ = decoder(z)`, pérdida = `||x - x̂||²`- El espacio de código no está estructurado.

> **自编码器。** `z = encoder(x)`¿ Qué ?`x̂ = decoder(z)`, pérdida = `||x - x̂||²`◊编码空间无结构──

**VAE encoder.**Salidas de dos vectores: `μ(x)`y `log σ²(x)`- Estos definen .`q(z|x) = N(μ, diag(σ²))`¿ Qué ?

> **VAE 编码器。**输出 dos emportos:`μ(x)`Y `log σ²(x)` Ellos definen `q(z|x) = N(μ, diag(σ²))`¿Qué es eso?

**Reparameterization trick.**Muestreo de `q(z|x)`No es diferenciable.`z = μ + σ·ε`donde`ε ~ N(0, I)`Ahora .`z`es una función determinista de `(μ, σ)`más un ruido no parámetro  flujo de gradientes `μ`y `σ`¿ Qué ?

> **重参数化技巧。**Desde`q(z|x)`采样不可微──将采样重写为 `z = μ + σ·ε`, entre ellos `ε ~ N(0, I)`Ahora mismo.`z`Sí `(μ, σ)`La función de determinación más el ruido no-parámetro se puede pasar.`μ`Y `σ`En contra de la transmisión.

**Loss.**Evidencia Bando inferior (ELBO), dos términos:

```
loss = reconstruction + β · KL[q(z|x) || N(0, I)]
     = ||x - x̂||²  + β · Σ_i ( σ_i² + μ_i² - log σ_i² - 1 ) / 2
```

La reconstrucción impulsa`x̂`hacia`x`KL empuja .`q(z|x)`El primer tipo de muestras de desintegración de los átomos de la base de datos de la base de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos

> Posibilidad de reconstrucción`x̂`趋近 `x` Capacidad de trabajo`q(z|x)`趋近先验──两者相互权衡──β 小(<1)= 更利的样本,编码空间不太高斯──β 大(>1)= 更干净的编码空间,更模糊的样本──β-VAE(2017) hace que este giro se conozca, y abre el conocimiento表示学习研究──

**Sampling.**En la inferencia: dibujar `z ~ N(0, I)`Una pasada hacia adelante, sin muestreo iterativo como la difusión.

> **采样。**推理时: desde `N(0, I)`抽取                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           `z`, envía en el módulo de despliegue de la información.

> **【中文解读】**El ELBO 损失的两个组成部分分工:重建损失确保解码质量,KL 散度确保潜在空间的规整性――推理时完全不需要编码器直接从N(0,I) 采样 z 送进解码器――VAE 生成速度快(单次前向传播), pero la calidad de la imagen suele estar más confusa que la de un modelo de difusión, ya que se optimiza en ELBO 下界而非精确似──

> **【拓展：Stable Diffusion 中的 VAE】**Estabilidad de difusión Utiliza el VAE de pre-entrenamiento que se comprimirá 512x512 imágenes hasta el potencial de 64x64 de espacio (8).

## Construye y realiza.
```figure
vae-latent-grid
```

## Construye el mismo

`code/main.py`Implementa una pequeña VAE sin numpy o antorcha. La entrada es un dato sintético de 8 dimensiones extraído de una mezcla gaussiana de 2 componentes en 8D. El codificador y el decodificador son MLPs de capa oculta única. Implementamos activación tanh, pase hacia adelante, pérdida y un pase hacia atrás escrito a mano. No la producción  pedagogía.

> `code/main.py`∞: ∞: ∞: ∞: ∞: ∞: ∞: ∞: ∞: ∞: ∞: ∞: ∞: ∞: ∞: ∞: ∞: ∞: ∞: ∞: ∞: ∞: ∞: ∞: ∞: ∞: ∞: ∞: ∞: ∞: ∞: ∞: ∞: ∞: ∞: ∞: ∞: ∞: ∞: ∞: ∞: ∞: ∞: ∞: ∞: ∞: ∞: ∞: ∞: ∞: ∞: ∞: ∞: ∞: ∞: ∞: ∞: ∞: ∞: ∞: ∞: ∞: ∞: ∞: ∞: ∞: ∞: ∞: ∞: ∞: ∞: ∞: ∞: ∞: ∞: ∞: ∞: ∞: ∞: ∞: ∞: ∞: ∞: ∞: ∞: ∞: ∞: ∞: ∞: ∞: ∞: ∞: ∞: ∞: ∞: ∞: ∞: ∞: ∞: ∞: ∞: ∞: ∞: ∞: ∞: ∞: ∞: ∞: ∞: ∞: ∞: ∞: ∞: ∞: ∞: ∞: ∞: ∞: ∞: ∞: ∞: ∞: ∞: ∞: ∞: ∞: ∞: ∞: ∞: ∞: ∞: ∞: ∞: ∞: ∞: ∞: ∞: ∞: ∞: ∞: ∞: ∞: ∞: ∞: ∞: ∞: ∞: ∞: ∞: ∞: ∞: ∞: ∞: ∞: ∞: ∞: ∞: ∞: ∞: ∞: ∞: ∞: ∞: ∞: ∞: ∞: ∞: ∞: ∞: ∞:

### Paso 1: codificador hacia adelante

```python
def encode(x, enc):
    h = tanh(add(matmul(enc["W1"], x), enc["b1"]))
    mu = add(matmul(enc["W_mu"], h), enc["b_mu"])
    log_sigma2 = add(matmul(enc["W_sig"], h), enc["b_sig"])
    return mu, log_sigma2
```

`log σ²`en lugar de`σ`Así que la salida de la red no está limitada (softplus de σ es una trampa  los gradientes mueren en σ ≈ 0).

> Uso `log σ²`Y no`σ`Para que la salida de la red no esté restringida, el softplus es un trampa en el que la escala desaparecerá.

### Paso 2: reparametrizar y decodificar

```python
def reparameterize(mu, log_sigma2, rng):
    eps = [rng.gauss(0, 1) for _ in mu]
    sigma = [math.exp(0.5 * lv) for lv in log_sigma2]
    return [m + s * e for m, s, e in zip(mu, sigma, eps)]

def decode(z, dec):
    h = tanh(add(matmul(dec["W1"], z), dec["b1"]))
    return add(matmul(dec["W_out"], h), dec["b_out"])
```

### Paso 3: El ELBO

```python
def elbo(x, x_hat, mu, log_sigma2, beta=1.0):
    recon = sum((a - b) ** 2 for a, b in zip(x, x_hat))
    kl = 0.5 * sum(math.exp(lv) + m * m - lv - 1 for m, lv in zip(mu, log_sigma2))
    return recon + beta * kl, recon, kl
```

La gente todavía envía código con las estimaciones de Monte-Carlo KL en 2026  es 3 veces más lento sin razón.

> 精确的闭式 KL,因为两个分布都是高斯的──不要数值积分──2026年还有人发布蒙特卡洛 KL 估计代码无端慢了3倍──

### Paso 4: generar

```python
def sample(dec, z_dim, rng):
    z = [rng.gauss(0, 1) for _ in range(z_dim)]
    return decode(z, dec)
```

Es el modelo generativo. Cinco líneas.

> Esto es generar un modelo.

## Enlaces.

- **Posterior collapse.**Dispositivos de término KL `q(z|x) → N(0, I)`tan agresivamente que`z`No lleva información sobre `x`. Corrección: β-annealing (inicio β=0, rampa a 1), bits libres, o saltar el KL en dimensiones inactivas.
  **后验坍塌。**KL 项如此强强地将 `q(z|x)`拉向    hacia el`N(0, I)`, que conduce`z`No llevo acerca de`x`La información es que el tiempo de la información es de 0, pero no es de 0, y el tiempo de la información es de 0, pero es de 0, y el tiempo de la información es de 0, y el tiempo de la información es de 0, y el tiempo de la información es de 0, y el tiempo de la información es de 0, y el tiempo de la información es de 0, y el tiempo de la información es de 0, y el tiempo de la información es de 0, y el tiempo de la información es de 0, y el tiempo de la información es de 0, y el tiempo de la información es de 0, y el tiempo de la información es de 0, y el tiempo de la información es de 0, y el tiempo de la información es de 0, y el tiempo de la información es de 0, y el tiempo de la información es de 0, y el tiempo de la información es de 0, y el tiempo de la información es de 0, y el tiempo de la es de la información es de 0, y el tiempo de la es de la es.
- **Blurry samples.**La probabilidad del decodificador gaussiano implica la reconstrucción de MSE, que es Bayes-óptima para L2 (la media)  la media de un conjunto de dígitos plausibles es un dígito borroso.
  **模糊样本。**高斯解码器似然意味着MSE 重建一组合理数字的平均值是一个模糊的数字──修复:离散解码器(VQ-VAE、NVAE), o simplemente utilizar VAE como codificador, superpuesto en el potencial espacio sobre el modelo de expansión──
- **β too large, too early.**Ver colapso posterior. Comienza en β≈0.01 y rampa.
  **β 太大太早。**见后验塌──从 β≈0.01 开始并逐渐增加──
- **Latent dim too small.**16-D funciona para MNIST, 256-D para ImageNet 2562, 2048-D para ImageNet 10242. La VAE de la difusión estable comprime 512×512×3 → 64×64×4 (32x factor de muestra baja en área espacial, 32x en canales).
  **潜在维度太小。**MNIST con 16 dimensiones,ImageNet 2562 con 256 dimensiones.

## Usalo con el marco de ejecución

La pila de VAE 2026:

> 2026 años de la UE 技术:

| Situation / 场景 | Pick / 选择 |
|-----------|------|
| Image-latent encoder for diffusion / 图像潜在编码器 | Stable Diffusion VAE (`sd-vae-ft-ema`) or Flux VAE |
| Audio-latent encoder / 音频潜在编码器 | Encodec (Meta), SoundStream, or DAC (Descript) |
| Video latents / 视频潜在表示 | Sora's spatiotemporal patches, Latte VAE, WAN VAE |
| Disentangled representation learning / 解耦表示学习 | β-VAE, FactorVAE, TCVAE |
| Discrete latents (for transformer modelling) / 离散潜在表示 | VQ-VAE, RVQ (ResidualVQ) |
| Continuous latents for generation / 连续潜在生成 | Plain VAE, then condition a flow/diffusion model in that latent space |

Un modelo de difusión latente es un modelo de difusión que vive entre un codificador y un decodificador. El modelo de difusión hace la compresión gruesa, el modelo de difusión hace el levantamiento pesado.

> 潜在扩散模型就是编码器和编码器之间加入了扩散模型的 VAE──VAE做粗压缩,扩散模型做重活──视频(VAE + 视频 DiT) 和音频(Encodec + MusicGen transformador) 同理──

## Envíe el producto .

Salva .`outputs/skill-vae-trainer.md`¿ Qué ?

> 保存 `outputs/skill-vae-trainer.md`¿Qué es eso?

Tome habilidades: perfil de conjunto de datos + objetivo latente-dim + uso en aguas subterráneas (reconstrucción, muestreo o entrada de difusión latente) y resultados: elección de arquitectura (plan/β/VQ/RVQ), programa β, latente dim, probabilidad de decodificación (Gaussian vs categorical), y plan de evaluación (recon MSE, KL por dim, distancia Fréchet entre `q(z|x)`y `N(0, I)`¿Qué es lo que se hace?

> Habilidad  recepción: datos conjunto概况 + 潜在维度目标 + 下游用途(重建、采样或潜在扩散输入),输出:架构选择(plain/β/VQ/RVQ) 、β 调度、潜在维度、解码器似然(高斯 vs 类别) y evaluación plan。

## Los ejercicios.

1. **Easy / 简单.**Cambiar`β`En el`code/main.py`¿ Qué ?`0.01`¿ Qué ?`0.1`¿ Qué ?`1.0`¿ Qué ?`5.0`. Graba la reconstrucción final de MSE y KL. ¿Cuál β es mejor para sus datos sintéticos?
   En el`code/main.py`El jefe`β`改为     cambió por`0.01`¿Qué es esto?`0.1`¿Qué es esto?`1.0`¿Qué es esto?`5.0`¿Cuál de los dos está mejor en tu conjunto de datos?
2. **Medium / 中等.**Reemplazar la probabilidad de descodificación gaussiana con una probabilidad de Bernoulli (pérdida de entropía cruzada). Comparar la calidad de la muestra en una versión binaria de los mismos datos sintéticos.
   Se trata de un sistema de análisis de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de
3. **Hard / 困难.**Extenderse`code/main.py`en un mini VQ-VAE: sustituir el continuo `z`Comparar la reconstrucción de MSE y informar cuántas entradas de código se utilizan (el colapso del código es real).
   ¿ Qué ?`code/main.py`扩展为迷你 VQ-VAE: Usando K=32 的码本近邻查找替换连续 `z`◊ Comparar la reconstrucción de la EMS y el informe utilizó muchos códigos en este artículo.

## Términos clave .

| Term / 术语 | What people say / 俗称 | What it actually means / 实际含义 |
|------|-----------------|-----------------------|
| Autoencoder | Encode-decode network / 编码-解码网络 | `x → z → x̂`, learn MSE. Not generative. / `x → z → x̂`，学习 MSE。不是生成模型。 |
| VAE | AE with a sampler / 带采样器的 AE | Encoder outputs a distribution, KL penalty shapes code space. / 编码器输出分布，KL 惩罚塑造编码空间。 |
| ELBO | Evidence lower bound / 证据下界 | `log p(x) ≥ recon - KL[q(z\|x) \|\| p(z)]`; tight when `q = p(z\|x)`. |
| Reparameterization | `z = μ + σ·ε` | Rewrites stochastic node as deterministic + pure noise. Enables backprop through sampling. / 将随机节点重写为确定性 + 纯噪声。使采样可反向传播。 |
| Prior | `p(z)` | Target distribution for the latent, typically `N(0, I)`. / 潜在变量的目标分布，通常是 `N(0, I)`。 |
| Posterior collapse | "KL term wins" / "KL 项赢了" | Encoder ignores `x`, outputs the prior; decoder must hallucinate. / 编码器忽略 `x`，输出先验；解码器只能幻觉。 |
| β-VAE | Tunable KL weight / 可调 KL 权重 | `loss = recon + β·KL`. Higher β = more disentangled but blurrier. / β 越高越解耦但越模糊。 |
| VQ-VAE | Discrete latent / 离散潜在变量 | Replace continuous `z` with nearest codebook vector; enables transformer modelling. / 用最近码本向量替换连续 `z`。 |

## Nota de producción: el VAE es el camino más caliente en un servidor de difusión.

En una línea de flujo / flujo / SD3 estable, el VAE se llama dos veces por solicitud  una vez para codificar (si se hace img2img / inpainting) y una vez para decodificar. En 10242 el pase de decodificador es a menudo el pico de memoria de activación más grande en toda la línea porque muestra`128×128×16`Los latentes de vuelta a `1024×1024×3`Dos consecuencias prácticas:

> En la línea de flujo / flujo / SD3 流水中,VAE cada vez se utiliza dos veces una vez codificar(img2img/inpainting) una vez resolver. En 10242 bajo resolución, el descifrador suele ser la parte más grande de la línea de flujo de agua entera en la que se activa el máximo valor de memoria. Dos resultados reales:

- **Slice or tile the decode.** `diffusers`expone `pipe.vae.enable_slicing()`y `pipe.vae.enable_tiling()`. Tiling comercializa un pequeño artefacto de costura para`O(tile²)`memoria en lugar de `O(H·W)`Es esencial para 10242+ en GPUs de consumo.
  **切片或分块解码。** `diffusers`                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             `enable_slicing()`Y `enable_tiling()`分块以轻微接伪影换取 `O(tile²)`¿Qué es eso?
- **bf16 decoder, fp32 numerics for the final resize.**El SD 1.x VAE fue lanzado en fp32 y *produce silenciosamente NaNs* cuando se lanza a fp16 en 10242+. buques SDXL `madebyollin/sdxl-vae-fp16-fix` siempre prefiere la variante fp16-fix o utilizar bf16.
  **bf16 解码器，fp32 用于最终 resize。**SD 1.x VAE 在 fp16 下 10242+ 会静默产生 NaN──始终使用 fp16-fix 变体或 bf16──

## Más Leer más Leer más

- [Kingma & Welling (2013). Auto-Encoding Variational Bayes](https://arxiv.org/abs/1312.6114) el documento de la AEV.
- [Higgins et al. (2017). β-VAE: Learning Basic Visual Concepts with a Constrained Variational Framework](https://openreview.net/forum?id=Sy2fzU9gl) desentrañada β-VAE.
- [van den Oord et al. (2017). Neural Discrete Representation Learning](https://arxiv.org/abs/1711.00937) VQ-VAE.
- [Vahdat & Kautz (2021). NVAE: A Deep Hierarchical Variational Autoencoder](https://arxiv.org/abs/2007.03898) Imagen de última generación de VAE.
- [Rombach et al. (2022). High-Resolution Image Synthesis with Latent Diffusion Models](https://arxiv.org/abs/2112.10752) Difusión estable; VAE como codificador.
- [Défossez et al. (2022). High Fidelity Neural Audio Compression](https://arxiv.org/abs/2210.13438) Encodec, el estándar de audio VAE.
