# Flujo de coincidencia y flujos rectificados.

> Los modelos de difusión toman pasos de muestreo de 20-50 porque recorren un camino curvo desde el ruido hasta los datos. La coincidencia de flujo (Lipman et al., 2023) y el flujo rectificado (Liu et al., 2022) entrenaron caminos rectos.

> **【中文解读】**El modelo de propagación requiere de 20 a 50 pasos, ya que el camino es un camino de movimiento.

> **【拓展：Flow Matching 是 2024-2026 的趋势】**El flujo de coincidencia está reemplazando la tradicional regulación de propagación como estándar de modelos de generación nueva. Es matemáticamente más elegante, experimentalmente más eficaz. La mejora de la calidad de SD3 y FLUX se debe en gran medida a esta mejora.

**Type:** Build / 构建型 | **类型:** 构建
**Languages:** Python | **语言:** Python
**Prerequisites:** Phase 8 · 06 (DDPM), Phase 1 · Calculus / 微积分 | **前置知识:** 阶段 8 · 06（DDPM），阶段 1 · 微积分
**Time:** ~45 minutes | **预计用时:** ~45 分钟

## El problema es la introducción del problema

El proceso inverso de DDPM es un paseo estocástico de 1000 pasos desde `N(0, I)`El bloqueador es que el ODE que resuelve el proceso inverso es rígido; el camino es curvo.

> El proceso de reversación del DDPM es de`N(0, I)`Volver a 1000 pasos de distribución de datos con el tiempo. DDIM se comprime a 20-50 pasos.

Si pudieras entrenar el modelo de tal manera que el camino del ruido a los datos fuera una *línea recta*, un solo paso de Euler de `t=1`¿ Qué ?`t=0`La combinación de flujos construye esto directamente: definir una interpolación en línea recta desde`x_1 ∼ N(0, I)`¿ Qué ?`x_0 ∼ data`, entrenar un campo vectorial `v_θ(x, t)`para coincidir con su derivada del tiempo, integrar en la inferencia.

> Si el modelo de entrenamiento puede hacer ruido a datos el camino es *direct*, paso Euler desde `t=1`¿ Qué ?`t=0`Ya está suficiente. Correspondiente de flujo.`x_1 ∼ N(0, I)`¿ Qué ?`x_0 ∼ data`de la línea directa, entrenamiento de la línea de escala `v_θ(x, t)`匹配时间导数──

El flujo rectificado (Liu 2022) va más allá: endereza iterativamente los caminos con un procedimiento de reflujo que produce un ODE progresivamente más cercano a lineal. Después de dos iteraciones de reflujo, un muestrador de 2 pasos coincide con la calidad de DDPM de 50 pasos.

> Flow rectificado (REC) 2022: más adelante: a través del proceso de reflujo (REC) 代拉直路径──两次 reflow 代后,2 步采样器匹配 50 步 DDPM质量──

> **【中文解读】**El flujo de datos de la combinación de datos es un proceso de composición de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de

> **【拓展：FLUX.1 的 Flow Matching 实现】**FLUX.1 de Black Forest Labs (estable diffusion) utiliza el flujo de combinación  sustituir a la tradicional distribución de la configuración, junto con MMDiT (多模态 DiT) arquitectura, en calidad de imagen y velocidad de generación son significativamente mejores que SDXL。 FLUX.1-schnell  versión sólo necesita 4 pasos de la muestra para generar imágenes de alta calidad, comprobó los beneficios reales de la combinación de flujo。

## El concepto central.

![Flow matching: straight-line interpolation between noise and data](../assets/flow-matching.svg)

### Flujo en línea recta.

Definición:

>  definición:

```
x_t = t · x_1 + (1 - t) · x_0,   t ∈ [0, 1]
```

donde`x_0 ~ data`y `x_1 ~ N(0, I)`La derivada temporal a lo largo de esta línea recta es constante:

> Entre ellos `x_0 ~ data`¿ Qué ?`x_1 ~ N(0, I)`  El número de direcciones de tiempo de esta línea recta es constante:

```
dx_t / dt = x_1 - x_0
```

Define un campo vectorial neuronal `v_θ(x_t, t)`y entrenarlo para que coincida con esta derivada:

> 定义神经向量场                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                       `v_θ(x_t, t)`, entrenarlo para que se ajuste a este número:

```
L = E_{x_0, x_1, t} || v_θ(x_t, t) - (x_1 - x_0) ||²
```

Esto es el**conditional flow matching**El programa de formación de la ODE no se puede deshacer nunca.`(x_0, x_1, t)`y el regreso.

> Eso es todo.**条件 Flow Matching**损失(Lipman 2023) ―― entrenamiento es sin simulación 的:你永远不需要展开 ODE──只需采样`(x_0, x_1, t)`Y hacer regreso es posible.

### Muestras de muestras

En la inferencia, integra el campo vectorial aprendido *retroceder* en el tiempo:

> 推理时,将学到的量场沿时间*反向*积分:

```
x_{t-Δt} = x_t - Δt · v_θ(x_t, t)
```

Comience en`x_1 ~ N(0, I)`, Euler-paso hacia abajo a `t=0`¿ Qué ?

> Desde`x_1 ~ N(0, I)`Comienza, con Euler.`t=0`¿Qué es eso?

### El flujo rectificado (Liu 2022) 整流流(Liu 2022)

El flujo en línea recta funciona pero los caminos aprendidos no son *realmente rectos*  se curvan porque muchos `x_0`s puede mapear a la misma `x_1`. Paso de reflujo del flujo rectificado:

> Aunque es efectivo, el camino de aprendizaje en realidad no es realmente directo.`x_0`Se puede proyectar a la misma.`x_1`,路径会曲──Reflow de flujo rectificado 步骤:

1. Modelo de flujo de tren v_1 con emparejamientos aleatorios.
   Usas el tiempo para entrenar Flow 模型 v_1──
2. Muestra N pares `(x_1, x_0)`integrando v_1 de `x_1`hasta su aterrizaje `x_0`¿ Qué ?
   通过将 v_1 从 `x_1`积分到落点 `x_0`采样 N 对 `(x_1, x_0)`¿Qué es eso?
3. Como los pares ahora están "pareados con ODE", el interpolante en línea recta entre ellos es realmente más plano.
   En estos ejemplos de parámetros, el parámetro actual es "parámetro ODE", y la línea de inserción entre ellos es más plana.
4. Repito, ¿qué quieres?
   ¿Qué es eso?

En la práctica, las iteraciones de reflow 2 te llevan a una aproximación lineal, permitiendo inferir en 2-4 pasos. SDXL-Turbo, SD3-Turbo, LCM son todos modelos destilados de flujo.

> En la práctica, 2 veces reflow 代就能使路径接近线性,从而支持 2-4 步推理──SDXL-Turbo、SD3-Turbo、LCM 都是基于流相匹配 蒸出来的模型──

### ¿Por qué esto ganó para las imágenes en 2024 ?

Tres razones:

> Tres razones:

1. **Simulation-free training** no se despliegan ODE durante la formación, trivial para su implementación.
   **无需仿真的训练** entrenamiento  no necesita desarrollar ODE, la realización es muy simple.
2. **Better loss geometry** Los caminos rectos tienen una señal-ruido consistente, mientras que la pérdida ε-DDPM tiene una negativa SNR en los bordes del horario.
   **更优的损失几何**直线路径信噪比一致, mientras que la ε-lucha de DDPM está en la red de la SNR 较差.
3. **Faster inference** 4-8 pasos con calidad SDXL-Turbo; 1 paso con destilación de consistencia.
   **更快的推理**4-8 步即可达到 SDXL-Turbo 质量; 配合一致性蒸可一步生成──

## Corresponde flujo vs DDPM  la conexión exacta  Corresponde flujo vs DDPM  精确联系

El flujo que coincide con una trayectoria condicional de Gauss es la difusión *con un horario de ruido específico*.`x_t = α(t) x_0 + σ(t) x_1`el tiempo y el flujo coinciden con la recuperación de la difusión reformulada de Stratonovich con `v = α'·x_0 - σ'·x_1`Los dos son algebraicamente equivalentes para las rutas de Gaussian.

> Utilizaciones de alta condiciones de la ruta de flujo de la combinación de la corriente de flujo de la corriente de corriente de corriente de corriente de corriente de corriente de corriente de corriente de corriente de corriente de corriente de corriente de corriente de corriente de corriente de corriente de corriente de corriente de corriente de corriente de corriente de corriente de corriente de corriente de corriente de corriente de corriente de corriente de corriente de corriente de corriente de corriente de corriente de corriente de corriente de corriente de corriente de corriente de corriente de corriente de corriente de corriente de corriente de corriente de corriente de corriente de corriente de corriente de corriente de corriente de corriente de corriente de corriente de corriente de corriente de corriente de corriente de corriente de corriente de corriente de corriente de corriente de corriente de corriente de corriente de corriente de corriente de corriente de corriente de corriente de corriente de corriente de corriente de corriente de corriente de corriente de corriente de corriente de corriente de corriente de corriente de corriente de corriente de corriente de corriente de corriente de corriente de corriente de corriente de corriente de corriente de corriente de corriente de corriente de corriente de corriente de corriente de corriente de corriente de corriente de corriente de corriente de corriente de corriente de corriente de corriente de corriente de corriente de corriente de corriente de corriente de corriente de corriente de corriente de corriente de corriente de corriente de corriente de corriente de corriente de corriente de corriente de corriente de corriente de corriente de corriente de corriente de corriente de corriente de corriente de corriente de corriente de corriente de corriente de corriente de corriente de corriente de corriente de corriente de corriente de corriente de corriente de corriente de corriente de corriente de corriente de corriente de corriente de corriente de corriente de corriente de corriente de corriente de corriente de corriente de corriente de corriente de corriente de corriente de corriente de corriente de corriente`x_t = α(t) x_0 + σ(t) x_1`调度后,Flow Matching también se originó en forma de reescritura de Stratonovich, entre ellos `v = α'·x_0 - σ'·x_1` para los caminos altos, ambos en el precio igual en el factor

Lo que se añadió a la coincidencia de flujo: la *claridad* del objetivo (una velocidad plana), una pérdida más limpia y la licencia para experimentar con interpolantes no gaussianos.

> La verdadera contribución de la combinación de flujos es: la claridad de la meta, la pérdida de velocidad normal, la libertad de intentar no añadir un alto valor.

## Construye y realiza.
```figure
normalizing-flow
```

## Construye el mismo

`code/main.py`Implementa la coincidencia de flujo 1D en una mezcla gaussiana de dos modos.`v_θ(x, t)`En la inferencia, integra 1, 2, 4 y 20 pasos de Euler y compara la calidad de la muestra.

> `code/main.py`En la distribución de doble cumbre de altitud mixta se logra el acoplamiento de flujo en 1D.`v_θ(x, t)`Es un MLP de tipo pequeño, que utiliza la formación de objetivos directos.

### Paso 1: pérdida de entrenamiento Paso 1: pérdida de entrenamiento

```python
def train_step(x0, net, rng, lr):
    x1 = rng.gauss(0, 1)
    t = rng.random()
    x_t = t * x1 + (1 - t) * x0
    target = x1 - x0
    pred = net_forward(x_t, t)
    loss = (pred - target) ** 2
    # backprop + update
```

>                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                              `x1`Y el tiempo `t`, construcción de valores`x_t`, objetivo para`x1 - x0`, hacer el regreso cuadrado.

### Paso 2: Inferencia de varios pasos Paso 2: más pasos

```python
def sample(net, num_steps):
    x = rng.gauss(0, 1)
    for i in range(num_steps):
        t = 1.0 - i / num_steps
        dt = 1.0 / num_steps
        x -= dt * net_forward(x, t)
    return x
```

> Más pasos: desde el alto el ruido sale, según el largo y el largo de la línea de la línea de la línea de la línea de la línea de la línea de la línea de la línea de la línea de la línea de la línea de la línea de la línea de la línea de la línea de la línea de la línea de la línea de la línea de la línea de la línea de la línea de la línea de la línea de la línea de la línea de la línea de la línea de la línea de la línea de la línea de la línea de la línea de la línea de la línea de la línea de la línea de la línea de la línea de la línea de la línea de la línea de la línea de la línea de la línea de la línea de la línea de la línea de la línea de la línea de la línea de la línea de la línea de la línea de la línea de la línea de la línea de la línea de la línea de la línea de la línea de la línea de la línea de la línea de la línea de la línea de la línea de la línea de la línea de la línea de la línea de la línea de la línea de la línea de la línea de la línea de la línea de la línea de la línea de la línea de la línea de la línea de la línea de la línea de la línea de la línea de la línea de la línea de la línea de la línea de la línea de la línea de la línea de la línea de la línea de la línea de la línea de la línea de la línea de la línea de la línea de la línea de la línea de la línea de la línea de la línea de la línea de la línea de la línea de la línea de la línea de la línea de la línea de la línea de la línea de la línea de la línea de la línea de la línea de la línea de la línea de la línea de la línea de la línea de la línea de la línea de la línea de la línea de la línea de la línea de la línea de la línea de la línea de la línea de la línea de la línea de la línea de la línea de la línea de la línea de la línea de la línea de la línea de la línea de la línea de la línea de la línea de la línea de la línea de la línea de la línea de la línea de la línea de la línea de la línea de la línea de la línea de la línea de la línea de la línea de la línea de la línea de la línea de la línea de

### Paso 3: Comparar el número de pasos.

Esperar que el muestreo de 4 pasos ya coincida con la calidad de 20 pasos  un gran problema para la latencia.

> 4 步采采器应已匹配 20 步质量 esto es una mejora importante en el retraso.

## Enlaces.

- **Time parameterization.**Utilizaciones de coincidencia de flujo `t ∈ [0, 1]`con`t=0`en los datos, `t=1`en el ruido.`t ∈ [0, T]`con`t=0`en los datos, `t=T`El mismo rumor, la misma dirección, en diferentes escalas.
  时间参数化: Flujo de coincidencia Usado `t ∈ [0, 1]`¿ Qué ?`t=0`En el último momento,`t=1`En el ruido; DDPM Usado `t ∈ [0, T]`, la misma dirección pero diferentes dimensiones.
- **Schedule choice.**La línea recta del flujo rectificado es "el" calendario de coincidencia de flujo, pero se puede utilizar el muestreo de t-normal cosino o logit (SD3 hace esto) para una mejor cobertura a escala.
  调度选择:La línea recta del flujo rectificado es "standard" del flujo de coincidencia 调度, pero se puede usar el cosino o el t 采样的 logit-normal (SD3就是这样做) para obtener una mejor medida de cobertura。
- **Reflow cost.**Generar el conjunto de datos emparejado para reflujo es un paso de inferencia completo por muestra. Sólo recaiga cuando realmente necesita inferencia de 1-2 pasos.
  Reflujo: generación de reflujo 配对数据集需要每样本一次完整推理──只有真正需要1-2步推理时才做reflow──
- **Classifier-free guidance still applies.**Sólo intercambiar ε por v en la combinación lineal: `v_cfg = (1+w) v_cond - w v_uncond`¿ Qué ?
  Guía libre de clasificadores  sigue siendo aplicable: sólo necesita poner en el conjunto de la línea`v_cfg = (1+w) v_cond - w v_uncond`¿Qué es eso?

## Usalo con el marco de ejecución

| Use case / 用途 | 2026 stack / 2026 技术栈 |
|----------|-----------|
| Text-to-image, best quality / 最佳质量文生图 | Flow matching: SD3, Flux.1-dev |
| Text-to-image, 1-4 steps / 1-4 步文生图 | Distilled flow matching: Flux.1-schnell, SD3-Turbo, SDXL-Turbo |
| Real-time inference / 实时推理 | Consistency distillation from a flow-matched base (LCM, PCM) |
| Audio generation / 音频生成 | Flow matching: Stable Audio 2.5, AudioCraft 2 |
| Video generation / 视频生成 | Flow matching mixed with diffusion (Sora, Veo, Stable Video) |
| Science / physics / 科学/物理 | Flow matching + equivariant vector field |

Cada vez que un documento dice "más rápido que la difusión" en 2025-2026, casi siempre es el flujo de coincidencia + destilación.

> Cuando el artículo dice "Bísi se expande más rápido", casi siempre es Flujo de coincidencia + 蒸。

## Envíe el producto .

Salva .`outputs/skill-fm-tuner.md`. Skill toma una especificación de modelo de estilo de difusión y la convierte en una configuración de entrenamiento de flujo: elección de horario, distribución de muestreo de tiempo (uniforme / logit-normal), optimizador, plan de reflujo, recuento de pasos objetivo, protocolo de evaluación.

> 保存为                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           `outputs/skill-fm-tuner.md` Esta habilidad recibe una especificación de modelo de propagación, se transformará en Flow Matching  entrenamiento de configuración:调度选择、时间采样分布(uniforme / logit-normal) ✓ optimizadores、reflow 计划、目标步数、评估协议。

## Los ejercicios.

1. **Easy.**- ¿ Qué ?`code/main.py`y comparar la MSE de 1 paso vs 20 pasos vs la distribución de datos real.
   **简单。**运行                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           `code/main.py`, comparar 1 paso y 20 pasos en relación con la distribución real de datos MSE¬
2. **Medium.**Cambiar de uniforme`t`El análisis de muestras se reduce a logit-normal (concentra el análisis de muestras a mediados de t).
   **中等。**                         `t`采样切换为 logit-normal (), ¿se ha incrementado el volumen de la muestra?
3. **Hard.**Implemente una iteración de reflow: genera pareadas (x_0, x_1) integrando el primer modelo, entrena un segundo modelo en los pares y compara la calidad de la muestra en 1 paso.
   **困难。**实现 una vez reflow 代: mediante el primer modelo积分生成配对 (x_0, x_1), en el segundo modelo entrenamiento en el配对,并比较 1 步采样质量──

## Términos clave .

| Term | What people say | What it actually means |
|------|-----------------|-----------------------|
| Flow matching | "Straight-line diffusion" | Train `v_θ(x, t)` to match `x_1 - x_0` along an interpolant. |
| Rectified flow | "Reflow" | Iterative procedure that straightens learned flows. |
| Velocity field | "v_θ" | Output of the model — the direction to move `x_t`. |
| Straight-line interpolant | "The path" | `x_t = (1-t)·x_0 + t·x_1`; trivial target derivative. |
| Euler sampler | "1st order ODE solver" | Simplest integrator; works well when paths are straight. |
| Logit-normal t | "SD3 sampling" | Concentrate `t` sampling toward mid-values where gradients are strongest. |
| Consistency distillation | "1-step sampler" | Train a student to map any `x_t` directly to `x_0`. |
| CFG with velocity | "v-CFG" | `v_cfg = (1+w) v_cond - w v_uncond`; same trick, new variable. |

## Nota de producción: Flux.1-schnell es el flujo de coincidencia a su más rápido.

La victoria de producción de flujo de coincidencia es Flux.1-schnell  un flujo-combinación DiT destilado a 1-4 pasos de inferencia manteniendo la calidad de grado Flux-dev. Niels "Run Flux en una máquina de 8GB" notebook es la receta de implementación de referencia: T5 + CLIP código, cuantizado MMDiT denoise (en 4 pasos para rápido vs 50 para dev), VAE decodificación. La contabilidad de costos:

> Flux.1-schnell un蒸到1-4 步推理、 mantener el flujo-dev 级质量Flow-Matched DiT。Niels de "Flux running on 8GB 机器上流动" cuaderno es referencia de la implementación de esquema:T5 + CLIP 编码、量化 MMDiT 去噪(schnell 4 步 vs dev 50 步)、VAE 解码──成本核算:

| Variant | Steps | Latency at 1024² on L4 | Total FLOPs (relative) |
|---------|-------|------------------------|------------------------|
| Flux.1-dev (raw) | 50 | ~15 s | 1.0× |
| Flux.1-schnell | 4 | ~1.2 s | 0.08× (12× faster) |
| SDXL-base | 30 | ~4 s | 0.25× |
| SDXL-Lightning 2-step | 2 | ~0.3 s | 0.03× |

La regla de producción: **flow-matched base + distillation = the 2026 default for fast text-to-image.**Todos los principales proveedores envían esta combinación: SD3-Turbo (SD3 + flujo + destilación), Flux-schnell (Flux-dev + rectificado-flujo de enderezamiento), CogView-4-Flash.

> Reglas de producción:**Flow-Matched 基座 + 蒸馏 = 2026 年快速文生图的默认方案。**Cada fabricante principal ha lanzado este tipo de combinación:SD3-Turbo(SD3 + flujo + 蒸)、Flux-schnell(Flux-dev + Flujo rectificado 拉直)、CogView-4-Flash──纯扩散基座只为遗留检查点保留──

## Más Leer más Leer más

- [Liu, Gong, Liu (2022). Flow Straight and Fast: Learning to Generate and Transfer Data with Rectified Flow](https://arxiv.org/abs/2209.03003) flujo rectificado.
- [Lipman et al. (2023). Flow Matching for Generative Modeling](https://arxiv.org/abs/2210.02747) coincidencia de flujo.
- [Esser et al. (2024). Scaling Rectified Flow Transformers for High-Resolution Image Synthesis](https://arxiv.org/abs/2403.03206) SD3, flujo rectificado a escala.
- [Albergo, Vanden-Eijnden (2023). Stochastic Interpolants](https://arxiv.org/abs/2303.08797) marco general que cubre la difusión FM +.
- [Song et al. (2023). Consistency Models](https://arxiv.org/abs/2303.01469) Destillación en 1 paso de difusión/flujo.
- [Sauer et al. (2023). Adversarial Diffusion Distillation (SDXL-Turbo)](https://arxiv.org/abs/2311.17042) Variante turbo.
- [Black Forest Labs (2024). Flux.1 models](https://blackforestlabs.ai/announcing-black-forest-labs/) flujo de coincidencia en la producción.
