# Video generación

> Una imagen es un tensor 2D. Un video es un 3D. La teoría es la misma; el cálculo es 10-100 veces más difícil. Sora de OpenAI (feb 2024) demostró que era posible. Para 2026 Veo 2, Kling 1.5, Runway Gen-3, Pika 2.0, y WAN 2.2 video de producción de buque desde texto a 1080p  y la pila de pesos abiertos (CogVideoX, HunyuanVideo, Mochi-1, WAN 2.2) está 12 meses atrás.

> **【中文解读】**图像是2D 张量,视频是3D 张量, teoría es la misma pero el cálculo es de 10 a 100 veces.

> **【拓展：Sora 的影响】**Sora de OpenAI (OpenAI) es un hito en la generación de vídeos, que muestra la gran capacidad de un modelo de expansión + de una estructura transformadora.

**Type:** Build / 构建型
**Languages:** Python
**Prerequisites:** Phase 8 · 07 (Latent Diffusion / 潜在扩散), Phase 7 · 09 (ViT), Phase 8 · 06 (DDPM)
**Time:** ~45 minutes

## El problema es la introducción del problema

Un video 1080p de 10 segundos a 24fps es 240 cuadros de 1920×1080×3 píxeles. Eso es aproximadamente 1,5 GB de datos crudos por clip. La difusión en el espacio de píxeles es imposible. Necesitas:

> 10 segundos 1080p 24fps  vídeo es 240  1920×1080×3 像素, aproximadamente 1.5 GB de datos primitivos―像素空间扩散不可行―你需要:

1. **Spatiotemporal compression.**Un VAE que codifica videos, no marcos, en una secuencia de parches espacio-temporales.
   **时空压缩。**将视频(而非) codificados para el tiempo espacio de parche 序列 de VAE。
2. **Temporal coherence.**Los fotogramas deben compartir contenido, iluminación e identidad de objetos en segundos.
   **时间连贯性。** entre las necesidades de compartir contenido 、luz y identidad de objetos 
3. **Compute budget.**El entrenamiento por video es 10-100 veces más caro que la imagen para el mismo tamaño del modelo.
   **计算预算。**视频训练比图像贵 10-100 veces
4. **Conditioning.**El texto, la imagen (primero fotograma), el audio o otro video.
   **条件化。**文本、图像(首)、音频或其他视频──

La arquitectura que resolvió esto es la**Diffusion Transformer (DiT)**La diferencia entre los datos de la difusión y los datos de la difusión es que se aplican a parches espaciotemporales, y se entrenan en grandes conjuntos de datos (prompt, captura, video).

>  resolver estas estructuras es**Diffusion Transformer (DiT)**应用于时空补丁, training on large-scale dataset―― con la misma pérdida de propagación que la sección 06 课──

## El concepto central.

![Video diffusion: patchify, DiT, decode](../assets/video-generation.svg)

### Enlazar

> ### Parcheado

El video se codifica con un VAE 3D (compresión espaciotemporal aprendida).`[T_latent, H_latent, W_latent, C_latent]`Se dividen en parches de tamaño .`[t_p, h_p, w_p]`Para modelos de estilo Sora,`t_p = 1`(parches por marco) o `t_p = 2`Un video 1080p de 10 segundos se comprime a unos 20.000 a 100.000 parches.

> Usando VAE 3D 编码视频── potencialmente se puede ver en forma`[T, H, W, C]`│ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │`[t_p, h_p, w_p]`Gran tamaño de parche: 10 segundos 1080p  video comprimido para aproximadamente 2-100.000 parches:

### DiT espacio-temporal

> ### 时空 DiT

Un transformador procesa la secuencia plana de parches. Cada parche tiene una inserción posicional 3D (tiempo + y + x).

> Transformador 处理展平的补丁序列──每一个补丁有3D 位置编码(时间 + y + x)──注意力通常分解为:

- **Spatial attention**dentro de los parches de cada marco.
  **空间注意力**En cada parche dentro.
- **Temporal attention**en los marcos en la misma ubicación espacial.
  **时间注意力**La misma posición espacial de la transcursión.
- **Full 3D attention**Es 16-100 veces más caro; sólo se utiliza en baja resolución o en investigación.
  **完整 3D 注意力**贵 16-100 倍; sólo en baja resolución o en el estudio.

> **【中文解读】**视频生成的核心技术:(1) 3D VAE 将视频压缩为时空潜在表示;(2) 将潜在表示切分为时空补丁;(3) DiT(Diffusion Transformer) procesar secuencias de parches, utilizando 3D 位置编码;(4) la atención se divide normalmente en espacio y tiempo atención para reducir la cantidad de cálculo.

> **【拓展：Sora 架构与 DiT 在视频中的应用】**El núcleo de Sora es la expansión de la idea de parche de ViT en el campo de los vídeos.

### Condicionamiento del texto

> ### 文本条件化 文本条件化 文本条件化 文本条件化 文本条件化 文本条件化 文本条件化 文本条件化 文本条件化 文本条件化

La atención cruzada con un codificador de texto grande (T5-XXL para Sora, CogVideoX-5B utiliza T5-XXL).

> Con un gran codificador de textos hacer un intercambio de atención.

### Formación

> ###  entrenamiento

Perdida de difusión estándar (ε o predicción v) sobre latencias espaciotemporales. Datos: vídeo web + ~ 100M clips seleccionados + capciones de texto sintéticos. Computación: 10.000+ horas de GPU para incluso una pequeña investigación; escala Sora es 100.000+.

> 时空潜在表示上的标准扩散损失──数据:网络视频 + 约1亿精选片段 + 合成文本标注──计算:小规模研究需要10,000+ GPU 小时;Sora 规模是100,000+──

## El panorama de producción de 2026

| Model / 模型 | Date | Max duration / 最长时长 | Max res / 最高分辨率 | Open weights? / 开源？ | Notable / 亮点 |
|-------|------|--------------|---------|---------------|---------|
| Sora (OpenAI) | 2024-02 | 60s | 1080p | No | First model to show world simulator properties at scale / 首个展示世界模拟器属性的模型 |
| Sora Turbo | 2024-12 | 20s | 1080p | No | Production Sora at 5x faster inference / 5 倍推理加速 |
| Veo 2 (Google) | 2024-12 | 8s | 4K | No | Highest quality + physics in 2025 / 2025 年最高质量 |
| Veo 3 | 2025 Q3 | 15s | 4K | No | Native audio and stronger camera control / 原生音频 |
| Kling 1.5 / 2.1 (Kuaishou) | 2024-2025 | 10s | 1080p | No | Best human motion in 2025 Q1 / 最佳人体运动 |
| Runway Gen-3 Alpha | 2024-06 | 10s | 768p | No | Professional video tools on top / 专业视频工具 |
| Pika 2.0 | 2024-10 | 5s | 1080p | No | Strongest character consistency / 最强角色一致性 |
| CogVideoX (THUDM) | 2024 | 10s | 720p | Yes (2B, 5B) | First open 5B-scale video / 首个开源 5B 视频 |
| HunyuanVideo (Tencent) | 2024-12 | 5s | 720p | Yes (13B) | Open SOTA late 2024 / 2024 年末开源 SOTA |
| Mochi-1 (Genmo) | 2024-10 | 5.4s | 480p | Yes (10B) | Most permissively licensed / 最宽松许可 |
| WAN 2.2 (Alibaba) | 2025-07 | 5s | 720p | Yes | Strongest open model mid-2025 / 2025 年中最强开源 |

Los pesos abiertos están cerrando la brecha más rápido que en el espacio de imágenes: HunyuanVideo + WAN 2.2 LoRA ya alimentan la mayoría de los flujos de trabajo de código abierto a mediados de 2026.

> La apertura de la fuente de energía está reduciendo la diferencia más rápidamente que en el campo de la imagen.

## Construye y realiza.
```figure
video-diffusion-denoise
```

## Construye el mismo

`code/main.py`Simula la idea principal de la DiT espacial-temporal: parchear un pequeño video sintético, agregar una inserción de posición por parche y denotar toda la secuencia con una atención de estilo transformador sobre parches. No numpy; Python puro. Mostramos que la coherencia temporal emerge incluso en 1-D cuando parches de marco adyacente comparten un denotador y posiciones de inserción.

### Paso 1: parchear un "vídeo" sintético 1D

```python
def make_video(T_frames=8, rng=None):
    # a "video" is a sequence of 1-D values following a smooth trajectory
    base = rng.gauss(0, 1)
    return [base + 0.3 * t + rng.gauss(0, 0.1) for t in range(T_frames)]
```

### Paso 2: Emblazo de posición por marco

```python
def pos_embed(t, dim):
    return sinusoidal(t, dim)
```

### Paso 3: el desinfectador ve toda la secuencia

En lugar de denotar cada marco de forma independiente, nuestra pequeña red concatenará todos los valores del marco + sus embebedidos de posición y predice el ruido para todos los cuadros conjuntamente.

### Paso 4: Prueba de coherencia temporal

Después del entrenamiento, muestre un video. Mide el delta de marco a marco. Si el modelo ha aprendido la estructura temporal, los deltas permanecen más pequeños que muestrar cada marco de forma independiente.

## Enlaces.

- **Independent per-frame sampling = flicker.**Si ejecutas la difusión de imágenes en cada fotograma por separado, las salidas de salida parpadean porque el ruido de cada fotograma es independiente.
- **Naive 3D attention = OOM.**La atención 3D completa en una latencia de 10 segundos de 1080p es cientos de miles de millones de operaciones.
- **Data captioning matters more than size.**La principal actualización de Sora respecto a los trabajos anteriores fue la capacitación en cintas de texto 10 veces más detalladas (clips reetiquetados GPT-4).
- **First-frame conditioning.**La mayoría de los modelos de producción también aceptan una imagen como primer marco.
- **Physics drift.**Los clips largos (> 10 s) acumulan sutiles inconsistencias.

## Usalo con el marco de ejecución

| Use case / 用途 | 2026 pick / 2026 选择 |
|----------|-----------|
| Highest-quality text-to-video, hosted / 最高质量托管 | Veo 3 or Sora |
| Camera-controlled cinematic / 相机控制电影感 | Runway Gen-3 with motion brushes |
| Character consistency across clips / 跨片段角色一致 | Pika 2.0 or Kling 2.1 |
| Open weights, fast fine-tune / 开源快速微调 | WAN 2.2 + LoRA |
| Image-to-video / 图生视频 | WAN 2.2-I2V, Kling 2.1 I2V, or Runway |
| Audio-to-video lip sync / 音频对口型 | Veo 3 (native audio) or a dedicated lip-sync model |
| Video editing / 视频编辑 | Runway Act-Two, Kling Motion Brush, Flux-Kontext (still-frame) |

El costo por segundo de vídeo a la paridad de calidad ha caído 20 veces entre 2024 y 2026.

> 质量平价下视频成本每秒在2024-2026 años se redujo 20 veces.

## Envíe el producto .

Salva .`outputs/skill-video-brief.md`. Skill toma un resumen de vídeo (duración, relación de aspecto, estilo, plan de cámara, consistencia del tema, audio) y las salidas: modelo + alojamiento, plantilla rápida (lenguaje de cámara, descripción del tema, descriptores de movimiento), protocolo de semilla + reproductibilidad y una lista de verificación de calidad a nivel de marco.

## Los ejercicios.

1. **Easy.**En el`code/main.py`, comparar el delta de marco a marco para (a) muestreo independiente por marco, (b) muestreo de secuencia conjunta.
2. **Medium.**Añadir una condición de primer marco: marco de pin 0 a un valor dado y muestre el resto. Medir cómo se propaga el valor fijado.
3. **Hard.**Utilice los difusores HuggingFace para ejecutar CogVideoX-2B en una GPU local. La hora 20 de la inferencia se hace a 720p para un clip de 6 segundos. Profilar la atención espacio-temporal para identificar el cuello de botella.

## Términos clave .

| Term | What people say | What it actually means |
|------|-----------------|-----------------------|
| Video VAE | "3-D VAE" | Encoder that compresses `(T, H, W, C)` → spatiotemporal latent. |
| Patches | "The tokens" | Fixed-size 3-D blocks of the latent; input to the DiT. |
| Factorized attention | "Spatial + temporal" | Run attention over space, then over time; skip full 3-D attention. |
| Image-to-video (I2V) | "Animate this photo" | Model takes an image + text, outputs a video that starts from it. |
| Keyframe conditioning | "Anchor frames" | Pin specific frames to control the video's arc. |
| Motion brush | "Directional hint" | UI input where the user paints motion vectors onto the image. |
| Re-captioning | "Dense captions" | Using an LLM to re-label training clips with detailed prompts. |
| Flicker | "Temporal artifact" | Frame-to-frame inconsistency; fixed with coupled denoising. |

## Nota de producción: los videos latente son un problema de ancho de banda de memoria.

Un clip 1080p de 10 segundos a 24 fps es de 240 cuadros × 1920 × 1080 × 3 ≈ 1,5 GB de píxeles crudos.`2 × spatial × 2 × temporal`El tiempo de transcursión es de aproximadamente 100 MB por solicitud. ejecutar esto a través de un DiT espacio-temporal durante 30 pasos en el lote 1 y se está moviendo ~3 GB/paso a través de HBM  ancho de banda de memoria, no FLOPs, es el cuello de botella.

Tres botones de producción, todos directamente de la producción-inferencia literatura capítulo de inferencia:

- **TP across the DiT.**Los modelos de texto a video son rutinariamente ≥10B parámetros. TP = 4 en 4 H100s es estándar; PP = 2 × TP = 2 para los modelos de clase 405B. La latencia por paso disminuye aproximadamente linealmente con TP hasta la pared de reducción total.
- **Frame batching = continuous batching.**En el momento de la generación, el video es conceptualmente un lote de cuadros unidos por la atención.`t+1`mientras que el marco `t-1`se devuelve, si la arquitectura del modelo permite la generación de ventanas deslizantes.
- **Clip-level prefill cache.**Para la imagen a video, el condicionamiento de primer marco es análogo al preenrollo de LLM: computa una vez, reutiliza a través de los pases del decodificador temporal.

## Más Leer más Leer más

- [Brooks et al. (2024). Video generation models as world simulators](https://openai.com/index/video-generation-models-as-world-simulators/) Informe técnico de Sora.
- [Yang et al. (2024). CogVideoX: Text-to-Video Diffusion Models with An Expert Transformer](https://arxiv.org/abs/2408.06072) CogVideoX.
- [Kong et al. (2024). HunyuanVideo: A Systematic Framework for Large Video Generative Models](https://arxiv.org/abs/2412.03603) HunyuanVideo.
- [Genmo (2024). Mochi-1 Technical Report](https://www.genmo.ai/blog/mochi) Mochi-1.
- [Alibaba (2025). WAN 2.2](https://wanvideo.io/) abrir SOTA a mediados de 2025.
- [Ho, Salimans, Gritsenko et al. (2022). Video Diffusion Models](https://arxiv.org/abs/2204.03458) el papel de difusión de vídeo seminal.
- [Blattmann et al. (2023). Align your Latents (Video LDM)](https://arxiv.org/abs/2304.08818) El ancestro de la difusión de vídeo estable.
