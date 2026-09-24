# Modelos de lenguaje de vídeo: Tokens temporales y Grounding.

> El video no es una pila de fotos. Un clip de 5 segundos tiene orden causal, verbos de acción y tiempo de evento que un modelo de imagen no puede representar. Video-LLaMA (Zhang et al., junio 2023) envió el primer video-LLM abierto con tierra audiovisual. VideoChat y Video-LLaVA escalaron el patrón. Para 2025, el TMRoPE de Qwen2.5-VL cerró la brecha con los modelos patentados fronterizos. Cada sistema resolvió tokens temporales de manera diferente  Q-former por clip, concat-pool por frame, TMRoPE por token. Esta lección lee los patrones, construye un muestreo de marco uniforme frente a dinámico y evalúa las tareas de tierra temporal.

> **【中文解读】**视频不是 una pila de fotos. 视频 contenía información de tiempo de los eventos, es un modelo de imágenes que no puede expresar. 视频不是一堆照片的堆积. 视频的短视频包含因果序列,动作动词和事件时间信息. 视频的短视频包含因果序列,动作动词和事件时间信息. 视频的短视频的短视频包含因果序列,动作动词和事件时间信息. 视频的短视频的短视频, 视频的短视频, 视频的短视频, 视频的短视频, 视频的短视频, 视频的短视频, 视频的短视频, 视频的短视频, 视频的短视频, 视频的短视频, 视频的短视频, 视频的短视频, 视频的短视频, 视频的短视频, 视频的短视频, 视频的短视频, 视频的短视频, 视频的短视频, 视频的短视频, 视频的短视频, 视频, 视频的短视频, 视频, 视频, 视频, 视频, 视频, 视频, 视频, 视频, 视频, 视频, 视频, 视, 视, 视, 视, 视, 视, 视, 视, 视, 视, 视, 视, 视, 视, 视, 视, 视, 视, 视, 视, 视, 视, 视, 视, 视, 视, 视, 视, 视, 视, 视, 视, 视, 视, 视, 视, 视, 视, 视, 视, 视, 视, 视, 视, 视, 视, 视, 视, 视, 视, 视, 视, 视, 视, 视, 视, 视, 视, 视

**Type:** Build
**Languages:** Python (stdlib, frame sampler + temporal-grounding evaluator)
**Prerequisites:** Phase 12 · 08 (LLaVA-OneVision)
**Time:** ~180 minutes

> ¿ Qué es esto ?**【前置】**学本节前请先掌握:Fase 12·08(LLaVA-OneVision 统一视觉代币 预算) 、Fase 7·04(RoPE 旋转位置编码,本节升级为TMRoPE 三轴) ⋅视频 VLM 的核心挑战:代币 爆炸(1 分钟视频 = 35万代币) + 时间维度建模──
> ¿ Qué es esto ?**【类比】**视频 VLM 处理时间维度 = "看足球比赛回放"──均采样 = 每10秒截一(错过进球瞬间);事件驱动采样 = 进球时密集采样+其他时间稀疏(捕捉关键时刻);动态 FPS = 根据画面变化自动调度──TMRoPE 让模型能理解"4.2秒发生进球"而不是"第15 ", esto es el producto de la categoría de vídeo entender la clave──

## Objetivos de aprendizaje

- Explicar por qué la codificación posicional temporal cambia el rendimiento de VLM de vídeo independientemente del codificador de visión.
  Traducción:explicar por qué el tiempo de la posición de la codificación es independiente del vídeo de la codificación de vídeo VLM  rendimiento。
- Comparar muestreo de fotogramas uniforme, dinámico-FPS, y impulsado por eventos en tokens-por-segundo vs precisión de tierra.
  China 翻译:比较均、动态 FPS 和事件驱动采样在每秒代币 数与定位准确率上的表现──
- Describa los diseños Q-ex-per-clip (Video-LLaMA) vs. pooled-per-frame (Video-LLaVA) vs. M-RoPE-per-token (Qwen2.5-VL).
  En el caso de los modelos de la serie de la serie, el modelo de la serie de la serie de la serie de la serie de la serie de la serie de la serie de la serie de la serie de la serie de la serie de la serie de la serie de la serie de la serie de la serie de la serie de la serie de la serie de la serie de la serie de la serie de la serie de la serie de la serie de la serie de la serie de la serie de la serie de la serie de la serie de la serie de la serie de la serie de la serie de la serie de la serie de la serie de la serie de la serie de la serie de la serie de la serie de la serie de la serie de la serie de la serie de la serie de la serie de la serie de la serie de la serie de la serie de la serie de la serie de la serie de la serie de la serie de la serie de la serie de la serie de la serie de la serie de la serie de la serie de la serie de la serie de la serie de la serie de la serie de la serie de la serie de la serie de la serie de la serie de la serie de la serie de la serie de la serie de la serie de la serie de la serie de la serie de la serie de la serie de la serie de la serie de la serie de la serie de la serie de la serie de la serie de la serie de la serie de la serie de la serie de la serie de la serie de la serie de la serie de la serie de la serie de la serie de la serie de serie de serie de serie de serie de serie de serie de serie de serie de serie de serie de serie de serie de serie de serie de serie de serie de serie de serie de serie de serie de serie de serie de serie de serie de serie de serie de serie de serie de serie de serie de serie de serie de serie de serie de serie de serie de serie de serie de serie de serie de serie de serie de serie de serie de serie de serie de serie de serie de serie de serie de serie de serie de serie de serie de serie de serie de serie de serie de serie de serie de serie de serie de serie de serie de serie de serie de serie de serie de serie de serie de serie de serie de serie de serie de serie de serie de serie de serie de serie de serie de serie de serie de serie de serie de serie de serie de serie de serie de serie de serie de serie de
- Nombre de los cuatro puntos de referencia de vídeo: VideoMME, TempCompass, EgoSchema, Video-MMMU.
  En el contexto de la actualidad, el programa de trabajo de la empresa de la industria de la información es un proyecto de investigación de la industria de la información.

## El problema es la introducción del problema

Un video de 1 minuto a 30 FPS es de 1800 cuadros. A 196 tokens visuales por cuadro (ViT-B a 224), es decir, 352k tokens  más grandes que cualquier contexto LLM de la era de 2024.

> 1 minuto 30 FPS de vídeo tiene 1800 ── en cada  196 视觉代币(ViT-B en 224 分辨率下) calcula, total 352k de los tokens  superó la longitud de cualquier LLM de 2024 

> **【中文解读】**1 minuto 30FPS tiene 1800 , 196  tokens de vídeo, un total de 352k tokens lejos más de 2024 años LLM                                                                                                                                                                                                                                              

Existen tres estrategias de reducción:

> Tres estrategias de compresión:

1. Envases de submuestras (1-8 FPS dependiendo del contenido).
   En el caso de los niños, el contenido de la película es de 1 a 8 FPS.
2. Agrupar las fichas de cada marco de forma agresiva (3x3 o 4x4 pool bilinear).
   China 翻译:对每的补丁代币 进行激进池化(3x3 或4x4 双线性池化) ⋅
3. Compresar a través de un Q-former que toma un clip de 16 cuadros y saque 64 tokens.
   Por medio de Q-former 压缩,将 16 片段映射为 64 个代币──

Cada cambio es diferente. la submuestreo pierde detalles temporales. el pooling pierde detalles espaciales. el Q-former pierde tanto un poco pero ahorra tokens.

> Cada peso es diferente. Los dos se pierden un punto, pero se ahorran un token.

La codificación de la posición temporal es el otro eje: ¿cómo sabe el modelo que el marco 5 vino antes que el marco 6? Las opciones incluyen simple RoPE temporal 1D (Video-LLaMA), incorporaciones temporales aprendidas (Video-LLaVA) y TMRoPE (Qwen2.5-VL, 3D completo).

> 时间位置编码是另一个维度:模型怎么知道第5 在第6 之前?选项包括简单的 1D 时间 RoPE(Video-LLaMA)、可学习时间嵌入(Video-LLaVA) y TMRoPE(Qwen2.5-VL, completo 3D)。

## El concepto central.

> **【中文解读】**视频语言时序定位(Temporal Grounding) es el trabajo de encontrar con precisión en el vídeo el tiempo que se debe de tiempo.

> **【拓展：时序定位的应用场景】**时序定位在视频搜索、自动剪辑、体育分析、安防监控等场景有广泛应用──技术上分为时刻检索(定位单个片段) 和亮点检测(定位高光时刻)── Actualmente el mejor modelo alcanza aproximadamente el 60% de los millones de dólares en el conjunto de datos de Charades-STA──


### Video-LLaMA: Q-former por clip + rama de audio

Video-LLaMA (2023) fue el primer video-LLM abierto.

> Video-LLaMA(2023) es el primer LLM en video abierto.

- Clip de 16 cuadros a 2 FPS (de ahí 8 segundos).
  En el caso de los niños, el tiempo de trabajo es de 8 segundos.
- Las funciones de ViT por marco -> Video Q-former que atende cruzando a través de los 16 cuadros -> 32 consultas aprendidas -> LLM.
  En inglés, el programa de estudios de la Universidad de Chicago es el más popular de los estudios de la Universidad de Chicago.
- Ramo de audio paralelo: forma de onda -> Encoder de audio ImageBind -> Audio Q-former -> 32 consultas -> LLM.
  China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China

Fuerza: razonamiento conjunto audiovisual. debilidad: longitud fija del clip, sin tierra de tiempo arbitrario.

> 优势:音视频联合推理――劣势: fijación de un segmento de longitud, no se puede hacer cualquier tiempo de tiempo.

### VideoChat y Video-LLaVA

VideoChat mantuvo la idea de Video-LLaMA, pero dejó caer el audio y simplificó. Video-LLaVA (Lin et al., 2023) entrenó un único codificador visual en ambas imágenes y marcos de video ("alineamiento antes de la proyección"), dando una representación unificada.

> VideoChat guardó la idea de Video-LLaMA pero eliminó el audio y simplificó.

Ninguno de ellos maneja videos largos.

> 两者都不能处理长视频──都是 8-16 系统──

### Qwen2.5-VL y TMRoPE

Qwen2.5-VL introdujo TMRoPE  Embedding de posición rotaria de modalidad temporal. Cada token de parche lleva una posición (t, h, w) donde t es el sello de tiempo real (no el índice de marco).

> Qwen2.5-VL  introdujo TMRoPE tiempo-模态旋转位置编码── cada parche de token 携带 (t, h, w) 位置, de los cuales t es el tiempo real(非索引)──

Diferencias clave de la simple incorporación temporal:

> Diferencias clave entre simple tiempo de inserción:

- El modelo ve "a 4.2 segundos" no "a marco 15".
  La versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión de la versión original de la versión de la versión original de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la
- Cada token visual gira de forma independiente por su sello de tiempo.
  China: 转而非逐片段. 按时间独立旋转.
- Si muestra a 2 FPS aquí y 4 FPS allí, TMRoPE maneja el espaciamiento desigual de forma nativa.
  Si en algún lugar 2 FPS 采样、另一处 4 FPS 采样,TMRoPE 原生处理不均间隔──

TMRoPE permite las consultas "¿a qué segundo salta el gato?" El modelo puede emitir "a 4.2 segundos". Video-LLaMA sólo podría decir "a principios en el clip".

> TMRoPE 支持"Cat in few seconds jumps?" este tipo de consultas.

> **【中文解读】**TMRoPE es la innovación clave de Qwen2.5 - VL: cada token de visión porta (t, h, w) información de posición, de la cual t es tiempo real  y no  índice. Esto significa que el modelo ve es "4,2 segundos" en lugar de "15 ", y puede procesar naturalmente el tiempo de intervalos de tiempo bajo un índice desigual .

> **【拓展：TMRoPE 在金融视频分析中的应用】**La capacidad absoluta de posicionamiento en el tiempo de TMRoPE es crucial para el escenario financiero: en el análisis de los informes financieros, se puede determinar con precisión el lugar "CEO cuándo menciona el crecimiento de ingresos"; en el análisis de la vigilancia de operaciones, se puede marcar los puntos de tiempo de eventos extraordinarios.

### Estrategias de muestreo de marco

Uniforme: muestra N marcos uniformemente a lo largo de la duración.

> 均采样: 在时长内均采样 N ──简单,但丢失运动峰值──

FPS dinámico: muestra adaptativamente basada en la intensidad del movimiento. flujo óptico o diferenciación de marco elige segmentos de alta movimiento para muestreo más denso.

> 动态 FPS: Basado en el movimiento de la intensidad de autoadaptación de la muestra.

Event-driven: ejecuta un detector ligero, muestra más donde ocurre la acción.

> 事件驱动:运行轻量级检测器, 在动作发生处密集采样;;VideoAgent 使用;;

Cuadro de teclado + contexto: muestra en los límites de la toma + algunos cuadros adyacentes.

> 关键 + 上下文: 在镜头边界采样 + 少量相邻──用于电影内容──

> **【中文解读】**Cuatro estrategias de toma de decisiones: mediación de la toma de decisiones (en términos de movimiento)  mejor práctica para el año 2026 es la toma de decisiones en función de la intensidad de la toma de decisiones (en términos de movimiento)  mejor práctica para el año 2026 es la toma de decisiones en función de la intensidad de la toma de decisiones (en términos de movimiento).

### Reunión por marco

A 1 FPS y 576 tokens por fotograma, un clip de 5 minutos es de 172.800 tokens.

> 1 FPS ⋅ 576 tokens ⋅ 5 分钟片段 ⋅ 172.800 ⋅ tokens ⋅ Qwen2.5-VL-72B ⋅ 128k ⋅ 上下文 可处理,但成本高──

3x3 bilinear pool se reduce a 64 tokens por marco -> 19.200 tokens durante 5 minutos.

> 3x3 双线性池化降至每 64 tokens → 5 分钟 19,200 tokens── la mayoría de las tareas─

Reúne de manera más agresiva (6x6 -> 16 tokens por fotograma) para flujos de trabajo de agentes donde el detalle espacial importa menos.

> Más activamente en el área de trabajo.

### Los cuatro puntos de referencia de vídeo

- VideoMME: comprensión completa de vídeo, corto + medio + largo.
  VideoMME:综合视频理解,短+中+长。
- TempCompass: razonamiento temporal de gran tamaño, preguntas "antes" / "después".
  En el contexto de la historia de la historia, el tiempo se ha convertido en un tiempo de transición.
- EgoSchema: video en primera persona de largo horizonte.
  En español, el nombre de la persona que se encuentra en el video es "EgoSchema".
- Video-MMMU: preguntas de vídeo multimodales multidisciplinares.
  El video-MMMU:多模态多学科视频问题──

Una evaluación completa de video-VLM alcanza a los cuatro. Enfatizan diferentes ejes  TempCompass se trata de pedir, EgoSchema es de aproximadamente 3+ minutos de razonamiento, VideoMME abarca duradas.

> 完整的视频 VLM 评估需要覆盖全部四基准──它们测试不同维度TempCompass 关注时序,EgoSchema 关注 3分钟以上的推理,VideoMME 跨越不同时长──

### Formatos de salida de tierra

Formatos de salida para la tierra temporal:

> 时序定位的输出格式:

- Texto libre: "El gato salta alrededor de la marca de 4 segundos".
  El gato está saltando en 4 segundos o más.
- JSON estructurado: `{"event": "jump", "start": 4.1, "end": 4.3}`El Qwen2.5VL está equipado con esto.
  En inglés, el nombre de la fuente de la información es JSON.`{"event": "jump", "start": 4.1, "end": 4.3}`◊ Qwen2.5VL  entrenamiento en este formato―
- Basado en tokens: especial `<time>4.1</time>`Los tokens se entrelazaron con la respuesta.
  Traducción:basado en símbolo: especial`<time>4.1</time>`El símbolo y la respuesta se encuentran en el formato interno de Qwen2.5-VL.

El formato de salida JSON de Qwen2.5VL analiza directamente.

> 基于代币的格式在下游使用中最准确──Qwen2.5-VL 输出格式可直接解析──

### 2026 mejores prácticas

Para VLMs de vídeo en 2026:

> 2026 años de video VLM:

- Encodrador: SigLIP 2 con M-RoPE o TMRoPE (Qwen2.5-VL).
  La versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión de la versión original de la versión de la versión original de la versión de la versión de la versión original de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de
- Muestreo de fotogramas: FPS dinámico (1-4 dependiendo del movimiento) con tapa máxima de fotograma.
  Según el movimiento 1-4), hay un máximo de límites.
- El conjunto por marco: 3x3 bilinear.
  Traducción: por la mano: 3x3 双线性.
- Resultado: JSON estructurado con campos de tiempo + evento.
  China: 输出:带时间和事件字段的结构化 JSON。
- Indicadores de referencia: VideoMME + TempCompass para el general; EgoSchema para el largo horizonte.
  El programa de trabajo de la empresa es el de la empresa de la empresa de la empresa de la empresa de la empresa de la empresa de la empresa de la empresa de la empresa de la empresa de la empresa de la empresa de la empresa de la empresa de la empresa de la empresa de la empresa de la empresa de la empresa de la empresa de la empresa de la empresa de la empresa de la empresa de la empresa de la empresa de la empresa de la empresa de la empresa de la empresa de la empresa de la empresa de la empresa de la empresa de la empresa de la empresa de la empresa de la empresa de la empresa de la empresa de la empresa de la empresa de la empresa de la empresa de la empresa de la empresa de la empresa de la empresa de la empresa de la empresa de la empresa de la empresa de la empresa de la empresa de la empresa de la empresa de la empresa de la empresa de la empresa de la empresa de la empresa de la empresa de la empresa de la empresa de la empresa de la empresa de la empresa de la empresa de la empresa de la empresa.

## Usalo con el marco de ejecución
```figure
video-temporal-patches
```

## Usalo

`code/main.py`incluye:

> `code/main.py`包含:

- Muestras de marcos de FPS uniformes y dinámicos.
  Traducción:均和动态 FPS 采样器──
- Un evaluador de la tierra temporal de juguete: dado un evento de "verdad fundamental" en el tiempo T y una salida de modelo, califique la precisión con tolerancia.
  Un juego de tiempo en el que se puede evaluar el tiempo de T de "verdadero" eventos y modelos de salida, en el rango de la capacidad de diferencia.
- Una comparación entre Video-LLaMA (16 cuadros, Q-former), Video-LLaVA (8 cuadros, MLP), Qwen2.5-VL (FPS dinámico + TMRoPE).
  En el caso de los video-LLaMA, el video-LLaVA es un video de la serie de televisión de la serie de televisión de la televisión de la televisión de la India.

## Envíe el producto .

Esta lección produce`outputs/skill-video-vlm-frame-planner.md`. Dado una tarea de vídeo (monitoreo, reconocimiento de acción, tierra temporal, resumen), elige el muestreo de fotogramas, factor de agrupación, formato de salida y nivel de precisión esperado.

> 本课产 出  `outputs/skill-video-vlm-frame-planner.md`△ dado un determinado video tarea(monitoreo 动作识别、时序定位、摘要), que selecciona 采样器、池化因子、输出格式和预期准确率等级──

## Los ejercicios.

1. Para una demostración de cocción de 3 minutos, elija uniforme vs FPS dinámico. Justifique con un recuento de tokens.

2. TMRoPE añade qué específicamente una simple tabla de embebimiento temporal no puede hacer? TMRoPE 具体添加了什么简单的时间嵌入表无法做到的功能?

3. Escriba un esquema JSON para la conexión temporal que un VLM puede aprender a emitir. Incluya casos de error.

4. Lee la sección 3 de Video-LLaVA sobre "Alignment Before Projection". ¿Por qué es mejor que entrenar codificadores de imágenes y videos separados? 阅读 Video-LLaVA 第 3 节"对齐先于投影", ¿por qué esta comparación entrenar imágenes y vídeo编码器更好?

5. Dado el ranking de VideoMME, ¿cuál es la diferencia entre el modelo abierto superior y el modelo propietario superior a partir de 2026? ¿Cuánto de esa brecha se atribuye a la codificación temporal vs. escala LLM básica?

## Términos clave .

| Term | What people say | What it actually means | 中文释义 |
|------|-----------------|------------------------|---------|
| Temporal grounding | "Time-localized answers" 时序定位 | VLM outputs a specific timestamp range for when an event happens VLM 输出事件发生的具体时间戳范围 | |
| TMRoPE | "Time-Multimodal RoPE" 时间-多模态旋转位置编码 | 3D rotary position with absolute timestamps, used by Qwen2.5-VL 带绝对时间戳的 3D 旋转位置编码 | |
| Dynamic FPS | "Motion-aware sampling" 运动感知采样 | Sample more frames in high-motion segments, fewer in static ones 高运动段密集采样，静态段稀疏采样 | |
| Frame pooling | "Spatial compress per frame" 逐帧空间压缩 | Reduce patches per frame with bilinear interpolation before the LLM LLM 前用双线性插值减少每帧 patch 数 | |
| Video Q-former | "Clip compressor" 片段压缩器 | Cross-attention bottleneck mapping N frames to K learned queries 将 N 帧映射为 K 个学习查询的交叉注意力瓶颈 | |
| VideoMME | "Video bench" 视频基准 | Comprehensive short/medium/long video benchmark, 2500+ samples 覆盖短/中/长视频的综合基准测试 | |

## Más Leer más Leer más

- [Zhang et al. — Video-LLaMA (arXiv:2306.02858)](https://arxiv.org/abs/2306.02858)
- [Li et al. — VideoChat (arXiv:2305.06355)](https://arxiv.org/abs/2305.06355)
- [Lin et al. — Video-LLaVA (arXiv:2311.10122)](https://arxiv.org/abs/2311.10122)
- [Qwen Team — Qwen2.5-VL (arXiv:2502.13923)](https://arxiv.org/abs/2502.13923)
- [Lin et al. — VILA-1.5 (arXiv:2312.07533)](https://arxiv.org/abs/2312.07533)
