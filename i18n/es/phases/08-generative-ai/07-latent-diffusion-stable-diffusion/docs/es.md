# La difusión latente y la difusión estable.

> La difusión del espacio-pixel en imágenes de 512x512 es un crimen de guerra computacional. Rombach et al. (2022) notó que no se necesitan todas las dimensiones de 786k para generar una imagen  se necesita suficiente para capturar la estructura semántica, y un decodificador separado para el resto. ejecutar difusión dentro del espacio latente de un VAE. Esa idea es la difusión estable.

> **【中文解读】**En 512x512 像素空间做扩散是计算灾难──Rombach 等人发现不需要全部78.6万维度只需捕获语义结构,剩余用解码器补充──在 VAE's潜在空间中运行扩散,这个想法就是稳定扩散──

> **【拓展：Stable Diffusion 的革命】**La difusión estable llevará a cabo el proceso de expansión desde el espacio de imágenes hasta el espacio potencial, reduciendo la cantidad de cálculo decenas de veces, haciendo que la GPU de nivel de consumo pueda funcionar.

**Type:** Build / 构建型
**Languages:** Python
**Prerequisites:** Phase 8 · 02 (VAE), Phase 8 · 06 (DDPM), Phase 7 · 09 (ViT)
**Time:** ~75 minutes

## El problema es la introducción del problema

La difusión del espacio-pixel en 5122 significa que la U-Net funciona en tensores de forma .`[B, 3, 512, 512]`Cada paso de muestreo es de ~100 GFLOPS para una U-Net de 500M. Cincuenta pasos son 5 TFLOPS por imagen.

> 5122 像素空间扩散 significa U-Net en `[B, 3, 512, 512]`张量上运行──每采样步约100 GFLOPS──50 步就是5 TFLOPS──在十亿图像上训练计算成本荒谬──

La mayoría de esos FLOPs van a empujar detalles perceptualmente no importantes a través de la red  la textura de alta frecuencia que un VAE perdedor podría comprimir. La idea de Rombach: entrenar un VAE una vez (la * primera etapa*), congelarlo y ejecutar la difusión enteramente en el espacio latente de 4 canales 64×64 (la * segunda etapa*).

> La gran parte de los FLOPs se utiliza para transmitir la percepción sobre detalles no importantes. La idea de Rombach es: entrenar una vez en VAE (la primera etapa), y terminarlo, completamente en 4 vias 64×64  potencial espacio de operación se expande (la segunda etapa) ⋅ la misma U-Net⋅1/16 像素── aproximadamente 64 veces menos FLOPs。

Esta es la receta de la difusión estable. SD 1.x / 2.x usó una U-Net de 860M sobre `64×64×4`Las redes de acceso a Internet de SDXL utilizan una red de acceso a Internet de 2.6B.`128×128×4`, SD3 cambió la U-Net por un Transformador de Difusión (DiT) con flujo de coincidencia. Flux.1-dev (Black Forest Labs, 2024) envía un DiT-MMDiT de 12B-parámetro. Todos funcionan en el mismo sustrato de dos etapas.

> Esta es la combinación de la difusión estable. SD 1.x/2.x usando 860M U-Net en 64×64×4 arriba, SDXL usando 2.6B U-Net en 128×128×4 arriba, SD3 usando DiT + Flow Matching sustituir U-Net──Flux.1-dev usando 12B MMDiT──todos funcionan en las mismas dos etapas de base.

> **【中文解读】**La estructura central de la difusión estable es de dos fases: 1) Primera fase VAE 编码器将512x512 图像压缩到64x64x4 潜在空间(16 倍压缩); 2) Segunda fase 运行在潜在空间中运行扩散过程――U-Net 在 64x64 张量上运行,计算量降低约64 倍――Desde SD 1.x hasta SD3 desarrollo:U-Net → DiT(Diffusion Transformer), DDPM → Flow Matching――

> **【拓展：从 U-Net 到 DiT 的架构变迁】**SD 1.x/2.x Uso de U-Net  como red de deslumbro. SD3(2024) y FLUX 转向 DiT(Diffusion Transformer)  uso de Transformer 替代 U-Net。

## El concepto central.

![Latent diffusion: VAE compression + diffusion in latent space](../assets/latent-diffusion.svg)

**Two stages, separately trained.**

> **两个阶段，分别训练。**

1. **Stage 1 — VAE.**Encodificador`E(x) → z`, decodificador`D(z) → x`. Compresión objetivo: 8 veces muestra descendente en cada eje espacial + ajustar canales para que el tamaño latente total sea ~1/16 de la cantidad de píxeles. pérdida = reconstrucción (L1 + LPIPS perceptual) + KL (pequeño peso así `z`No es demasiado Gaussian, porque no necesitamos muestras exactas de`z`A menudo entrenados con una derrota adversaria, las imágenes descifradas son agudas.

   **阶段 1 — VAE。**编码器   codificador  codificador`E(x) → z`, descifrador `D(z) → x`△ objetivo compresión: cada espacio eje 8 倍下采样──损失 = 重建(L1 + LPIPS) + KL(小权重)。

2. **Stage 2 — diffusion on `z`.**Tratar`z = E(x_real)`En el caso de las redes de Internet, el sistema de comunicación de Internet (U-Net) puede ser utilizado para denegar la información.`z_t`En la inferencia: muestra`z_0`por difusión, entonces `x = D(z_0)`¿ Qué ?

   **阶段 2 — 在 `z` 上扩散。**¿ Qué ?`z = E(x_real)`视为数据──训练 U-Net(或 DiT) 去噪──推理时:采样 `z_0`, entonces`x = D(z_0)`¿Qué es eso?

**Text conditioning.**Dos componentes adicionales: un codificador de texto congelado (CLIP-L para SD 1.x, CLIP-L+OpenCLIP-G para SD 2/XL, T5-XXL para SD3 y Flux).`[Q = image features, K = V = text tokens]`Los tokens son la única forma en que el texto influye en la imagen.

> **文本条件化。**结的文本编码器和交叉注意注入── cada uno de los bloques de la red U-Net `[Q = 图像特征, K = V = 文本 token]`hacerse un paso por el otro.

**The loss function is identical to Lesson 06.**El mismo DDPM / flujo de MSE coincide con el ruido.

> **损失函数与第 06 课完全相同。**Sólo intercambiamos datos.

## Las variantes de arquitectura

| Model / 模型 | Year | Backbone / 骨干 | Latent shape / 潜在形状 | Text encoder / 文本编码器 | Params / 参数量 |
|-------|------|----------|--------------|--------------|--------|
| SD 1.5 | 2022 | U-Net | 64×64×4 | CLIP-L (77 tokens) | 860M |
| SD 2.1 | 2022 | U-Net | 64×64×4 | OpenCLIP-H | 865M |
| SDXL | 2023 | U-Net + refiner | 128×128×4 | CLIP-L + OpenCLIP-G | 2.6B + 6.6B |
| SDXL-Turbo | 2023 | Distilled | 128×128×4 | same | 1-4 step sampling / 1-4 步采样 |
| SD3 | 2024 | MMDiT (multimodal DiT) | 128×128×16 | T5-XXL + CLIP-L + CLIP-G | 2B / 8B |
| Flux.1-dev | 2024 | MMDiT | 128×128×16 | T5-XXL + CLIP-L | 12B |
| Flux.1-schnell | 2024 | MMDiT distilled | 128×128×16 | T5-XXL + CLIP-L | 12B, 1-4 step |

La tendencia: reemplazar U-Net por DiT (transformador sobre parches latente), escalar el codificador de texto (T5 supera CLIP para la adhesión rápida), aumentar los canales latente (4 → 16 da más espacio de detalle).

> 趋势: utilizar DiT 替代 U-Net, ampliar文本编码器(T5 在快速遵循上优于CLIP), aumentar las posibles vías de comunicación(4→16 给更多细节余量)

## Construye y realiza.
```figure
noise-schedule
```

## Construye el mismo

`code/main.py`Esta prueba muestra que la misma pérdida de difusión funciona si se ejecuta con valores 1D o en valores codificados  la información clave.

> `code/main.py`En la clase 06 de DDPM se superpuso un juguete 1D "VAE" y se añadió un guión de clase condicionada de clase.

### Paso 1: codificador/decodificador

```python
def encode(x):    return x * 0.5          # toy "compression" to smaller scale
def decode(z):    return z * 2.0
```

Para la pedagogía, este mapa lineal es suficiente para mostrar que la difusión opera en`z`sin importar el espacio de datos original.

> En la enseñanza, este lineal de mapeo es suficiente para mostrar la difusión en la`z`La operación no se preocupa por el espacio de datos original.

### Paso 2: difusión en `z`- el espacio

El mismo DDPM que la Lección 06.`z = E(x)`Después de tomar muestras`z_0`, decodificar con `D(z_0)`¿ Qué ?

> Los datos que se ven en la red son los mismos que los datos de la DDPM de la clase 06  `z = E(x)` 采样 `z_0`后用 `D(z_0)`¿Qué pasa?

### Paso 3: Guía sin clasificador

Durante el entrenamiento, deje de escribir la etiqueta de clase el 10% de las veces (reemplaza con un token nulo).`ε_cond`y `ε_uncond`, entonces:

```python
eps_cfg = (1 + w) * eps_cond - w * eps_uncond
```

`w = 0`= no hay orientación (plena diversidad), `w = 3`= por defecto, `w = 7+`= saturado / demasiado nítido.

> `w = 0`= 无引导(完全多样性),`w = 3`- ¿Qué es eso?`w = 7+`= 和/过度利。

### Paso 4: Condicionamiento de texto (concepto, no código)

Reemplazar la etiqueta de clase con una salida de codificador de texto congelado. Alimenta el texto integrado a la U-Net a través de la atención cruzada:

> Utiliza el código de texto para emitir un código de texto en la red.

```python
h = h + CrossAttention(Q=h, K=text_embed, V=text_embed)
```

Esta es la única diferencia sustancial entre un modelo de difusión con condiciones de clase y la difusión estable.

> Esta es la única diferencia sustancial entre el modelo de expansión y la difusión estable.

## Enlaces.

- **VAE-scale mismatch.**SD 1.x VAEs tienen una constante de escala (`scaling_factor ≈ 0.18215`El sistema de control de la red de U-Net se encuentra en latencia con una variación muy equivocada.
  **VAE 尺度不匹配。**SD 1.x VAE  codificación después de tener un número constante reducido ⋅ olvidar que permitirá que U-Net entrenar en el espacio potencial de la diferencia de error ⋅
- **Text encoder silently wrong.**SD3 necesita T5-XXL con >=128 tokens, y el regreso a CLIP-solo es pérdida.`use_t5=True`o cráteres de fidelidad rápidos.
  **文本编码器静默错误。**SD3  necesita T5-XXL 且 >=128 tokens。
- **Mixing latent spaces.**SDXL, SD3, Flux todos usan diferentes VAEs. Un LoRA entrenado en SDXL latente no funcionará en SD3.
  **混合潜在空间。**SDXL、SD3、Flux utiliza diferentes VAE──SDXL de LoRA no puede utilizarse en SD3 arriba──
- **CFG too high.** `w > 10`La idea de la Comisión es que la Comisión debe tener en cuenta que el mercado de la información en el mercado interior es un mercado único.`w = 3-7`¿ Qué ?
  **CFG 太高。** `w > 10`Producir imágenes de la película.
- **Negative prompts leaking.**El mensaje negativo vacío se convierte en el token nulo; un mensaje negativo lleno se convierte en el `ε_uncond`No son lo mismo; algunas tuberías silenciosamente se ponen en nulo.
  **负向 prompt 泄漏。**空负向 prompt 变为零代币; llenar de cambios `ε_uncond`Dos cosas diferentes.

## Usalo con el marco de ejecución

Estatuas de producción en 2026:

> 2026 años de producción tecnológica:

| Target / 目标 | Recommended backbone / 推荐骨干 |
|--------|----------------------|
| Narrow domain, paired data, from scratch / 窄域配对从零训练 | SDXL fine-tune (LoRA / full) — fastest to ship |
| Open-domain text-to-image, open weights / 开放域开放权重 | Flux.1-dev (12B, Apache / non-commercial) or SD3.5-Large |
| Fastest inference, open weights / 最快推理开放权重 | Flux.1-schnell (1-4 step, Apache) or SDXL-Lightning |
| Best prompt adherence, hosted / 最佳 prompt 遵循，托管 | GPT-Image / DALL-E 3, Midjourney v7, Imagen 4 |
| Edit workflows / 编辑工作流 | Flux.1-Kontext (Dec 2024) — natively accepts image + text |
| Research, baseline / 研究基线 | SD 1.5 — ancient but well-studied |

## Envíe el producto .

Salva .`outputs/skill-sd-prompter.md`. Skill toma un texto de respuesta + estilo objetivo y las salidas: modelo + punto de control, escala CFG, muestra, respuesta negativa, resolución, combinación opcional de ControlNet/IP-Adapter, y una lista de verificación de calidad por paso.

> 保存 `outputs/skill-sd-prompter.md` Habilidad de recibir texto + objetivo风格,输出模型 +检查点, CFG,采样器,负向提示等──

## Los ejercicios.

1. **Easy / 简单.**- ¿ Qué ?`code/main.py`con una guía`w ∈ {0, 1, 3, 7, 15}`- Registran la muestra media por clase.`w`¿Las clases de medios divergen más allá de los medios de datos reales?
   ¿ Qué ?`w ∈ {0, 1, 3, 7, 15}`¿Qué pasa?`w`¿El valor medio de la categoría del valor medio de los datos reales?
2. **Medium / 中等.**Cambiar el codificador lineal del juguete por un par de codificador/decodificador tanh-MLP con pérdida de reconstrucción. Retrain difusión en los nuevos latentes. ¿Cambia la calidad de la muestra?
   ¿Ha cambiado la calidad de la herramienta en el nuevo espacio potencial?
3. **Hard / 困难.**Configurar una verdadera inferencia de difusión estable con difusores: carga `sdxl-base`, ejecutar 30 pasos de Euler con CFG=7, tiempo. Ahora cambia a`sdxl-turbo`El mismo tema, diferente calidad  describir lo que cambió y por qué.
   Utiliza difusores 搭建真实SD 推理, comparar SDXL-base y SDXL-Turbo

## Términos clave .

| Term / 术语 | What people say / 俗称 | What it actually means / 实际含义 |
|------|-----------------|-----------------------|
| First stage | "The VAE" | Trained encoder/decoder pair; compresses 512² to 64². / 训练好的编码/解码器对；将 512² 压缩到 64²。 |
| Second stage | "The U-Net" | Diffusion model over the latent space. / 潜在空间上的扩散模型。 |
| CFG | "Guidance scale" / "引导缩放" | `(1+w)·ε_cond - w·ε_uncond`; tunes conditioning strength. / 调节条件化强度。 |
| Null token | "Empty prompt embed" / "空 prompt 嵌入" | Unconditional embed used for `ε_uncond`. / 用于无条件预测的嵌入。 |
| Cross-attention | "How text gets in" / "文本如何进入" | Each U-Net block attends to text tokens as K and V. / 每个 U-Net 块对文本 token 做注意力。 |
| DiT | "Diffusion Transformer" | Replace U-Net with a transformer over latent patches; scales better. / 用 Transformer 替代 U-Net。 |
| MMDiT | "Multi-modal DiT" / "多模态 DiT" | SD3's architecture: text and image streams with joint attention. / SD3 架构：文本和图像流的联合注意力。 |
| VAE scaling factor | "Magic number" / "魔数" | Divides latents by ~5.4 so diffusion operates in unit-variance space. / 除以约 5.4 使扩散在单位方差空间操作。 |

## Nota de producción: ejecutar Flux-12B en una GPU de consumo de 8 GB .

La integración de Flux de referencia es la receta canónica "Tengo una GPU de consumo, ¿puedo enviar esto?" El truco es el mismo de tres botones de receta de producción de la literatura de inferencia listas aplicadas a una difusión DiT:

> 参考流流集是经典的"Me sólo consume GPU, ¿puede desplegar?"方案──三旋方案:

1. **Staggered loading.**Flux tiene tres redes que nunca necesitan coexistir en VRAM: T5-XXL codificador de texto (~ 10 GB en fp32), CLIP-L (pequeño), el 12B MMDiT, y el VAE. Encode el prompt primero, *borrar* los codificadores, cargar el DiT, denoise, *borrar* el DiT, cargar el VAE, decodificar.
   **交错加载。**Flux tiene tres no necesitan permanecer simultáneamente en la red de VRAM.
2. **4-bit quantization via bitsandbytes.** `BitsAndBytesConfig(load_in_4bit=True, bnb_4bit_compute_dtype=torch.bfloat16)`En el codificador T5 y en el DiT. Cortando la memoria 8×, la caída de calidad es imperceptible para el texto a la imagen por los puntos de referencia de Aritra (enlazados en el cuaderno).
   **4 位量化。**El T5 y DiT se cuantifican a 4 bits, la memoria baja 8 veces, la pérdida de calidad es mínima.
3. **CPU offload.** `pipe.enable_model_cpu_offload()`automáticamente cambia los módulos entre la CPU y la GPU a medida que cada paso avanzado avanza. Agrega 10-20% de latencia pero hace que la tubería funcione en absoluto.
   **CPU 卸载。**Automático intercambio entre CPU y GPU. Aumenta el 10-20% de retraso, pero hace que el flujo de la línea pueda funcionar.

La contabilidad de la memoria es: `10 GB T5 / 8 = 1.25 GB`cuantificado,`12 B params × 0.5 bytes = ~6 GB`En términos de stas00 este es el extremo de la inferencia TP=1  sin paralelismo de modelo, cuantización máxima. Para la producción se ejecutaría TP=2 o TP=4 en H100s; para un solo portátil de desarrollo, esta es la receta.

## Más Leer más Leer más

- [Rombach et al. (2022). High-Resolution Image Synthesis with Latent Diffusion Models](https://arxiv.org/abs/2112.10752) Difusión estable.
- [Podell et al. (2023). SDXL: Improving Latent Diffusion Models for High-Resolution Image Synthesis](https://arxiv.org/abs/2307.01952) SDXL.
- [Peebles & Xie (2023). Scalable Diffusion Models with Transformers (DiT)](https://arxiv.org/abs/2212.09748)¿Qué es esto?
- [Esser et al. (2024). Scaling Rectified Flow Transformers for High-Resolution Image Synthesis](https://arxiv.org/abs/2403.03206) SD3, MMDiT.
- [Ho & Salimans (2022). Classifier-Free Diffusion Guidance](https://arxiv.org/abs/2207.12598) CFG.
- [Labs (2024). Flux.1 — Black Forest Labs announcement](https://blackforestlabs.ai/announcing-black-forest-labs/) Familia Flux1.
- [Hugging Face Diffusers docs](https://huggingface.co/docs/diffusers/index) aplicación de referencia para cada punto de control anterior.
