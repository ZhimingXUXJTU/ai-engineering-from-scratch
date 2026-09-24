# ControlNet, LoRA y Condicionamiento  ControlNet, LoRA y condiciones control

> El texto solo es una señal de control torpe. ControlNet le permite clonar un modelo de difusión preentrenado y dirigirlo con un mapa de profundidad, esqueleto de pose, escrutinio o imagen de borde. LoRA le permite ajustar un modelo de parámetro 2B mediante el entrenamiento de 10 millones de parámetros. Juntos convirtieron a la difusión estable de un juguete en la tubería de imágenes 2026 que se envía a cada agencia.

> **【中文解读】**纯文本控制太粗──ControlNet utiliza profundidad gráfico, postura esqueleto,涂 o bordes gráfico de producción de control preciso; LoRA sólo entrenar 1000 millones de parámetros en el modo de minimizar 20 mil millones de parámetros de modelos── ambas combinaciones permiten una difusión estable de los juguetes a través de las líneas de flujo de imágenes de cada empresa de diseño en 2026─

> **【拓展：LoRA 是大模型时代的微调标准】**LoRA (Low Range Adaptation) no sólo se utiliza en la generación de imágenes, sino que también se utiliza ampliamente en la LLM 微调 (LMA-LoRA) ⋅ sólo se necesita entrenar un parámetro del 0.1% para adaptarse a nuevas tareas/novos estilos, lo que reduce considerablemente el costo de la personalización de la IA.

**Type:** Build / 构建型
**Languages:** Python
**Prerequisites:** Phase 8 · 07 (Latent Diffusion / 潜在扩散), Phase 10 (LLMs from Scratch — for LoRA foundation / LoRA 基础)
**Time:** ~75 minutes

## El problema es la introducción del problema

Un mensaje como "una mujer con un vestido rojo caminando con un perro en una calle concurrida" no le da al modelo información sobre *dónde* está el perro, *qué postura* está la mujer en, o *la perspectiva* de la calle.

>  Como "una mujer en rojo está en una calle ocupada con un perro" este tipo de sugerencias no dicen a los modelos en la que están los perros, la mujer es una mujer de la calle, el aspecto de la calle, el aspecto de la calle, el texto sólo puede determinar el 10% de la información de la imagen.

El entrenamiento de un nuevo modelo condicional desde cero para cada señal (posición, profundidad, ingenioso, segmentación) es prohibitivo.

> Para cada señal (~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

También quieres enseñar al modelo nuevos conceptos (tu rostro, tu producto, tu estilo) sin volver a entrenar al modelo completo. Quieres un delta 100 veces más pequeño.

> También quieres enseñar un nuevo concepto de modelo (tu rostro, tu producto, tu estilo) sin volver a entrenar todo el modelo. Necesitas un aumento de 100 veces menor.

ControlNet + LoRA + texto = el kit de herramientas del profesional 2026 La mayoría de las tuberías de imágenes de producción tienen 2-5 LoRA, 1-3 ControlNets y un adaptador IP encima de una base SDXL / SD3 / Flux.

> ControlNet + LoRA + texto = 2026 años de practicantes. La mayoría de la producción de imágenes fluyen en línea en SDXL/SD3/Flux  Base sobrepuesta 2-5 个 LoRA、1-3 个 ControlNet y un IP-Adaptor.

## El concepto central.

![ControlNet clones the encoder; LoRA adds low-rank deltas](../assets/controlnet-lora.svg)

### ControlNet (Zhang et al., 2023)

*Clon* la mitad de codificador de la U-Net. Congela el original. Entren el clon para aceptar una entrada de condicionamiento adicional (borda, profundidad, pose). Conecte al clon de nuevo al decodificador de la mitad del original con *convolución cero* conexiones saltadas (1×1 convs inicializados a cero  comienzan como no-op, aprende un delta).

```
SD U-Net decoder:   ... ← orig_enc_features + zero_conv(controlnet_enc(condition))
```

El tren en 1M (prompto, condición, imagen) se triplica con la pérdida de difusión estándar.

ControlNets por modalidad se envían como modelos secundarios pequeños (~ 360 M para SDXL, ~ 70 M para SD 1.5).

```
features += weight_a * control_a(depth) + weight_b * control_b(pose)
```

### Los Estados miembros pueden adoptar medidas de seguridad en el marco de la aplicación de la presente Directiva.

Para cualquier capa lineal `W ∈ R^{d×d}`en el modelo, congelación `W`y añadir un delta de bajo rango:

```
W' = W + ΔW,  ΔW = B @ A,  A ∈ R^{r×d},  B ∈ R^{d×r}
```

con`r << d`.Rango 4-16 es estándar para la atención, rango 64-128 para las tonas finas pesadas.`2 · d · r`en lugar de`d²`. para la atención de SDXL con `d=640`¿ Qué ?`r=16`Por ejemplo, el modelo de la base de 5GB es de 20-200 MB.

En la inferencia se puede escalar la LoRA: `W' = W + α · B @ A`- ¿ Qué ?`α = 0.5-1.5`Los LRA múltiples se apilan de forma aditiva (con la advertencia habitual de que interactúan de manera no lineal).

### Adaptador IP (Ye et al., 2023)

Un pequeño adaptador que acepta una *imagen* como condicionamiento (junto con texto). Utiliza el codificador de imagen CLIP para producir tokens de imagen, inyectándolos en atención cruzada junto con tokens de texto. ~ 20 MB por modelo base. Permite "generar una imagen en el estilo de esta referencia" sin un LoRA.

## Matriz de composibilidad .

| Tool / 工具 | What it controls / 控制内容 | Size / 大小 | When to use / 使用时机 |
|------|------------------|------|-------------|
| ControlNet | Spatial structure (pose, depth, edges) / 空间结构 | 70-360MB | Exact layout, composition / 精确布局 |
| LoRA | Style, subject, concept / 风格、主题、概念 | 20-200MB | Personalization, style / 个性化、风格 |
| IP-Adapter | Style or subject from reference image / 参考图像风格 | 20MB | No text can describe the look / 文字无法描述 |
| Textual Inversion | Single concept as a new token / 单概念新 token | 10KB | Legacy, mostly replaced by LoRA / 旧方案 |
| DreamBooth | Full fine-tune on a subject / 完整微调 | 2-5GB | Strong identity, high compute / 强身份 |
| T2I-Adapter | Lighter ControlNet alternative / 轻量 ControlNet | 70MB | Edge devices, inference budget / 边缘设备 |

ControlNet es espacial, LoRA es semántico, usa ambas cosas.

> ControlNet ≈ 空间控制──LoRA ≈ 语义控制──两者配合使用──

> **【中文解读】**Mecanismo central de ControlNet: Klon SD U-Net 编码器,结原始部分,训练克隆部分接受额外条件输入(边缘、深度、姿态)。零卷积(零卷积) inicialización asegurar el entrenamiento comienza ControlNet no afecta al modelo original。LoRA En línea en la capa de la línea añadir a la red B@A, sólo entrenar muy poca cantidad de参数(20-200MB vs 基础模型 5GB)。

> **【拓展：ControlNet + LoRA 的组合控制】**实际生产中,ControlNet(空间控制) y LoRA(风格/主题控制) suelen ser combinados en diferentes conjuntos. Por ejemplo:ControlNet 控制人物姿态,LoRA 注入特定艺术风格,文本提示 描述场景内容── este mecanismo de control de tres niveles es el estándar de configuración de los servicios de imagen de la IA comercial de 2026──IP-Adapter 则提供"con imágenes para controlar imágenes" en la cuarta dimensión.

## Construye y realiza.
```figure
v4-controlnet-zero
```

## Construye el mismo

`code/main.py`simula los dos mecanismos en 1-D:

1. **LoRA.**Una capa lineal preentrenada .`W`- Congelarlo. Entrenar a un bajo rango.`B @ A`Es así .`W + BA`coincide con una capa lineal objetivo. Muestre que`r = 1`es suficiente para aprender una corrección de rango 1 perfectamente.

2. **ControlNet-lite.**Un predictor de "base congelada" y una "red lateral" que lee una señal adicional. La salida de la red lateral está bloqueada por un escalar aprendizaje inicializado a cero (nuestra versión de cero-conv). Entren y vigila la rampa de la puerta hacia arriba.

### Paso 1: Matemáticas de la LORA

```python
def lora(W, A, B, x, alpha=1.0):
    # W is frozen; A, B are the trainable low-rank factors.
    return [W[i][j] * x[j] for i, j in ...] + alpha * (B @ (A @ x))
```

### Paso 2: red lateral de inicio cero

```python
side_out = control_net(x, condition)
gated = gate * side_out  # gate initialized to 0
h = base(x) + gated
```

En el paso 0 la salida es idéntica a la base.`gate`lentamente, sin una deriva catastrófica.

> En el primer paso, la salida es exactamente igual a la base del modelo.`gate`更新缓慢没有灾难性偏移──

## Enlaces.

- **Over-scaling LoRAs.** `α = 2`o `α = 3`es un hack común "hacerlo más fuerte" que produce resultados demasiado estilizados / rotos.`α ≤ 1.5`¿ Qué ?
  **LoRA 过度缩放。** `α = 2`O `α = 3`Es habitual que la "intensificación" de la producción se produzca en exceso.`α ≤ 1.5`¿Qué es eso?
- **ControlNet weight conflict.**Usar una Pose ControlNet con peso 1.0 y una Depth ControlNet con peso 1.0 generalmente se sobrepone.
  **ControlNet 权重冲突。**权重之和 ≈ 1.0 es el valor predeterminado de seguridad.
- **LoRA on the wrong base.**Los SDXL LoRA no se operan en silencio en SD 1.5 porque las dimensiones de atención no coinciden.
  **LoRA 用错基础模型。**SDXL LoRA en SD 1.5 arriba se encuentra en silencio ineffectivo.
- **Textual Inversion drift.**Los tokens entrenados en un puesto de control se desplazan mal en otro.
  **Textual Inversion 漂移。**En un punto de control, el entrenamiento se mueve gravemente en otro.
- **LoRA weight-merging and storage.**Puedes hornear un LoRA en los pesos del modelo base para inferir más rápido (sin adición de tiempo de ejecución), pero pierdes la capacidad de escalar `α`Mantenga ambas versiones.
  **LoRA 权重合并。**Se puede acelerar la reflexión en el modelo básico, pero perder el tiempo de funcionamiento.`α`De la capacidad.

## Usalo con el marco de ejecución

| Goal / 目标 | 2026 pipeline / 方案 |
|------|---------------|
| Reproduce a brand's art style / 复刻品牌艺术风格 | LoRA trained on ~30 curated images at rank 32 |
| Put my face in a generated image / 把我的脸放入生成图像 | DreamBooth or LoRA + IP-Adapter-FaceID |
| Specific pose + prompt / 特定姿态+提示 | ControlNet-Openpose + SDXL + text |
| Depth-aware composition / 深度感知构图 | ControlNet-Depth + SD3 |
| Reference + prompt / 参考+提示 | IP-Adapter + text |
| Exact layout / 精确布局 | ControlNet-Scribble or ControlNet-Canny |
| Background replace / 背景替换 | ControlNet-Seg + Inpainting (Lesson 09) |
| Fast 1-step style / 快速单步风格 | LCM-LoRA on SDXL-Turbo |

## Envíe el producto .

Salva .`outputs/skill-sd-toolkit-composer.md`. La habilidad toma una tarea (activos de entrada: instantáneo, imagen de referencia opcional, pose opcional, profundidad opcional, escríbalo opcional) y saca la pila de herramientas, pesos y un protocolo de semilla reproducible.

## Los ejercicios.

1. **Easy / 简单.**En el`code/main.py`, varían el rango de la LoRA `r`¿En qué rango el LoRA coincide exactamente con un delta objetivo de rango 2?
   En el`code/main.py`El jefe de la policía`r`¿En qué orden se ajusta el LRA a los objetivos?
2. **Medium / 中等.**Entrenar dos LoRAs separadas en dos transformaciones de objetivo. cargarlos juntos y mostrar su interacción aditiva. ¿Cuándo la interacción rompe la linealidad?
   En dos objetivos de cambio, ¿cuándo romper la línea?
3. **Hard / 困难.**Utilice difusores para apilar: SDXL-base + Canny-ControlNet (peso 0.8) + un estilo LoRA (α 0.8) + IP-Adaptador (peso 0.6).
   Usar difusores 堆叠组合, medir FID y rápidamente 遵循的权衡──

## Términos clave .

| Term / 术语 | What people say / 俗称 | What it actually means / 实际含义 |
|------|-----------------|-----------------------|
| ControlNet | "Spatial control" / "空间控制" | Cloned encoder + zero-conv skips; reads a conditioning image. / 克隆编码器 + 零卷积跳跃。 |
| Zero convolution | "Starts as identity" / "起始为恒等" | 1×1 conv initialized to zero; ControlNet starts as no-op. / 1×1 卷积初始化为零。 |
| LoRA | "Low-rank adapter" / "低秩适配器" | `W + B @ A`, `r << d`; 100x fewer params than a full fine-tune. / 比完整微调少 100 倍参数。 |
| rank r | "The knob" / "那个旋钮" | LoRA compression; 4-16 typical, 64+ for heavy personalization. / LoRA 压缩；典型 4-16。 |
| α | "LoRA strength" / "LoRA 强度" | Runtime scaling of the LoRA delta. / LoRA 增量的运行时缩放。 |
| IP-Adapter | "Reference image" / "参考图像" | Small image-conditioning adapter via CLIP-image tokens. / 通过 CLIP 图像 token 的小型适配器。 |
| DreamBooth | "Full subject fine-tune" / "完整主题微调" | Train the full model on ~30 images of a subject. / 在约 30 张主题图像上训练完整模型。 |
| Textual Inversion | "New token" / "新 token" | Learn a new word embedding only; legacy, mostly replaced. / 仅学习新词嵌入；旧方案。 |

## Nota de producción: LoRA swaps, ControlNet carriles, servicio para varios inquilinos.

Un SaaS de texto a imagen real sirve a cientos de LoRA y una docena de ControlNets en el mismo punto de control base. El problema de servicio se parece mucho a la LLM multi-tenancy (la literatura de producción cubre el caso de LLM bajo lotes continuos y LoRAX / S-LoRA):

- **Hot-swap LoRAs, do not merge.**Fusión`W' = W + α·B·A`en la base da ~ 3-5% más rápido por paso de inferencia pero se congela `α`Mantenga los LRA calientes en VRAM como deltas de rango; los difusores exponen`pipe.load_lora_weights()`¿ Qué es eso ?`pipe.set_adapters([...], adapter_weights=[...])`El costo de cambio es el `2 · d · r · num_layers`Peso  en escala de MB, subsegundo.
- **ControlNet as a second attention lane.**El codificador clonado funciona en paralelo con la base. Dos ControlNets con peso 1.0 cada uno = dos pases adicionales hacia adelante por paso, no un pasado fusionado. El tamaño del batch se reduce cuadráticamente. Presupuesto para ~ 1.5 × costo de paso por ControlNet activo.
- **Quantized LoRAs too.**Si cuantificó la base (ver Lección 07, Flux en 8GB), el delta LoRA también cuantifica limpiamente a 8 bits o 4 bits.

Flux-specific: la notebook de Niels Flux-on-8GB cuantifica la base a 4 bits; apilar un estilo LoRA (`pipe.load_lora_weights("user/style-lora")`) en esa base cuantificada en `weight_name="pytorch_lora_weights.safetensors"`Esta es la receta que la mayoría de las agencias SaaS envían en 2026.

## Más Leer más Leer más

- [Zhang, Rao, Agrawala (2023). Adding Conditional Control to Text-to-Image Diffusion Models](https://arxiv.org/abs/2302.05543) ControlNet.
- [Hu et al. (2021). LoRA: Low-Rank Adaptation of Large Language Models](https://arxiv.org/abs/2106.09685) LoRA (originalmente para LLM; puertos de difusión).
- [Ye et al. (2023). IP-Adapter: Text Compatible Image Prompt Adapter](https://arxiv.org/abs/2308.06721) Adaptador IP.
- [Mou et al. (2023). T2I-Adapter: Learning Adapters to Dig Out More Controllable Ability](https://arxiv.org/abs/2302.08453) alternativa más ligera a ControlNet.
- [Ruiz et al. (2023). DreamBooth: Fine Tuning Text-to-Image Diffusion Models for Subject-Driven Generation](https://arxiv.org/abs/2208.12242) DreamBooth.
- [HuggingFace Diffusers — ControlNet / LoRA / IP-Adapter docs](https://huggingface.co/docs/diffusers/training/controlnet) tuberías de referencia.
