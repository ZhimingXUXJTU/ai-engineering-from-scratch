# Qwen-VL Familia y Dinámica-FPS Video  Qwen-VL  Serie con movimiento 率视频

> La familia Qwen-VL  Qwen-VL (2023), Qwen2-VL (2024), Qwen2.5-VL (2025), Qwen3-VL (2025)  es el linaje de modelos de lenguaje de visión abierta más influyente en 2026. Cada generación hizo una apuesta arquitectónica única decisiva que el resto del ecosistema abierto copió en doce meses: resolución dinámica nativa a través de M-RoPE, muestreo dinámico-FPS con alineación de tiempo absoluta, atención de ventana en el ViT y formatos de salida de agente estructurados. Por Qwen3-VL, la receta se había estabilizado: un codificador 2D-RoPE-ViT con entradas nativas de relación de aspecto, un proyector MLP en una gran base de lenguaje Qwen3, y etapas de entrenamiento que enfatizaron el comportamiento de OCR, la tierra y el agente como objetivos de primera clase. Esta lección lee la familia cronológicamente para que entiendas por qué cada botón está donde está.

> **【中文解读】**Qwen-VL 系列 es la familia de modelos de lenguaje de 2026 más influyente. Cada generación ha tomado una decisión de estructura clave, adoptada por la comunidad de código abierto en 12 meses.

> **【拓展：Qwen-VL 的产业生态位】**En el contexto financiero, el Qwen2.5VL puede ser utilizado para comprender los informes financieros en chino, los Emisos OCR, así como el control de vídeo análisis. Su estructuración JSON  Emission permite integrarlo directamente en el flujo de trabajo del agente.

**Type:** Learn  | **类型：学习**
**Languages:** Python (stdlib, M-RoPE encoder + dynamic-FPS sampler)  | **语言：Python（标准库，M-RoPE 编码器 + 动态帧率采样器）**
**Prerequisites:** Phase 12 · 06 (patch-n'-pack)  | **前置：阶段12第06课（补丁打包）**
**Time:** ~120 minutes  | **时长：约120分钟**

> ¿ Qué es esto ?**【前置】**学本节前请先掌握:Fase 12·06(parch-n'-pack 任意分辨率);Fase 7·04(RoPE 旋转位置编码,本节升级为 3D M-RoPE);Fase 14·04(Agent 工具调用,本节讲解 VLM 如何输出 JSON)
> ¿ Qué es esto ?**【类比】**Qwen-VL 系列 = "中文 VLM 旗舰"──和 LLaVA 系列的区别:LLaVA 主打英文 + 简单架构;Qwen-VL 主打中英双语 + 高分辨率 + 结构化输出── Si haces en chino场景(财报、合同、票据),Qwen-VL es la opción de preferencia──
> ️ **【易错点】**Qwen-VL 输出边界框坐标时混"绝对像素 vs相对比例"不同代次使用不同约定──Qwen2-VL 用绝对像素(0-1000 范围),Qwen2.5-VL 改用归一化比例(0-1)──修复:使用前查文档,按代次正确解析坐标──

## Objetivos de aprendizaje

- Compute las tres rotaciones de M-RoPE (temporal, altura, ancho) y explique por qué se necesitan las tres.
- Elija una estrategia de muestreo dinámico-FPS para un video y razonar sobre las fichas-por-segundo vs la precisión de detección de eventos.
- Nombren las cuatro mejoras generacionales de Qwen-VL en orden y lo que cada una habilitado.
- Envía un formato de salida de agente JSON de estilo Qwen2.5VL y analiza las llamadas de herramientas estructuradas de una respuesta VLM.

## El problema es el contexto del problema

Qwen-VL fue lanzado en agosto de 2023 como respuesta directa a LLaVA-1.5 y BLIP-2. La brecha que el equipo de Qwen se centró en fue triple: resolución, vídeo y salida estructurada.

Resolución: LLaVA-1.5 funcionó a 336x336. Muy bien para fotos, inútil para una factura en chino o una pantalla de hoja de cálculo densa. La primera innovación de Qwen-VL fue 448x448 y la salida de la caja de límite de tierra, dejando que el modelo apunte a las cosas.

Video: Video-LLaMA apilaron codificadores por marco y los alimentaron al LLM. Funcionó para clips cortos, no para videos de varios minutos donde el eje temporal es la señal.

Producción estructurada: LLaVA emitió texto de forma libre. Un agente necesita JSON. Qwen-VL entrenado en formatos de salida JSON explícitos, incluidas las coordenadas de la caja de límite como texto.

Cada generación de Qwen-VL extiende uno de estos tres ejes.

> **【中文解读】**Qwen-VL  en contra de LLaVA-1.5  Tres grandes deficiencias lanzar desafíos: 1) Resolución 336x336  Incapaz de procesar en chino 发票或密集表格截图; 2) 视频Video-LLaMA 只有能处理短片段; 3) 结构化输出LLaVA 输出自由文本,代理需要 JSON──每一代 Qwen-VL 都在三个轴上延伸──

## El concepto central.

### Qwen-VL (agosto 2023)

La primera generación: OpenCLIP ViT-bigG/14 como codificador (2.5B parámetros), Q-Former compatible con LLama (1 paso con 256 consultas), base Qwen-7B. Contribuciones:

- Resolución 448x448 (entonces SOTA para un VLM abierto).
- "El gato está en <box> 112, 204, (280, 344)</box>".
- Entrenamiento multilingüe chino + inglés desde el principio.

En la época, los puntos de referencia eran competitivos con el GPT-4V en inglés, dominantes en chino.

> **【中文解读】**La primera generación de Qwen-VL fue desarrollada en el año 2000 con un rendimiento de 448x448 puntos de resolución.

### Qwen2-VL (septiembre 2024)  M-RoPE y resolución nativa  Qwen2-VL: M-RoPE con resolución de origen

Qwen2-VL reemplazó la pila de resolución fija + Q-Former con un codificador ViT de resolución dinámica nativo.

- Resolución dinámica nativa / 原生动态分辨率. El ViT acepta cualquier HxW divisible por 28 (parche 14 con 2x fusión espacial). Una imagen en 1120x672 (40x24 parches fusionados) produce 960 tokens visuales.
- M-RoPE (RoPE multimodal) / 多模态旋转位置编码. Cada token lleva una posición 3D (t, h, w) en lugar de 1D. Para imágenes t = 0, para video t = frame_index. RoPE gira los vectores de consulta / clave por una frecuencia por eje. No hay tabla de embebido posicional.
- MLP proyector / MLP 投影器. Deja el Q-Former; usa un MLP de 2 capas en los tokens de parches fusionados.
- Video con FPS dinámico / 动态率视频. Video muestran en 1-2 FPS por defecto, pero el modelo acepta recuentos de cuadros arbitrarios.

Resultado: Qwen2-VL-7B coincidió con GPT-4o en varios puntos de referencia multimodal y lo superó en DocVQA (94.5 vs 88.4).

> **【中文解读】**La estructura central de Qwen2-VL cambia: elimina la resolución fija + Q-Former, cambia a la resolución de vida original ViT + M-RoPE + MLP  proyectores。M-RoPE para cada token  otorga una posición 3D                                                                                                                                                                                                                                   

### Qwen2.5VL (febrero 2025)  FPS dinámico + tiempo absoluto  Qwen2.5VL: 动态率 + 绝对时间

El cambio principal de Qwen2.5VL fue el video.

- Los símbolos de tiempo absoluto / 绝对时间 token. En lugar de índices de posición (marco 0, 1, 2...), utilice sellos de tiempo reales. "A las 0:04, el gato salta". El modelo ve `<time>0.04</time>`Los tokens se entrelazan con los tokens de marco.
- FPS dinámico / 动态率. Muestra a 1 FPS para imágenes lentas, 4+ FPS para la acción. El usuario o entrenador elige; M-RoPE se adapta.
- La atención espacial se hace en ventanas (local dentro de los bloques) para el rendimiento; la atención global cada pocas capas.
- Formato de salida JSON explícito / 显式 JSON 输出格式. Entrenado en datos de llamadas de herramienta: `{"tool": "click", "coords": [380, 220]}`. Agente listo fuera de la caja. ✓ ✓ ✓ ✓ ✓ ✓ ✓ ✓ ✓ ✓ ✓ ✓ ✓ ✓ ✓ ✓ ✓ ✓ ✓ ✓ ✓ ✓ ✓ ✓ ✓ ✓ ✓ ✓ ✓ ✓ ✓ ✓ ✓ ✓ ✓ ✓ ✓ ✓ ✓ ✓ ✓ ✓ ✓ ✓ ✓ ✓ ✓ ✓ ✓ ✓ ✓ ✓ ✓ ✓ ✓ ✓ ✓ ✓ ✓ ✓ ✓ ✓ ✓ ✓ ✓ ✓ ✓ ✓ ✓ ✓ ✓ ✓ ✓ ✓ ✓ ✓ ✓ ✓ ✓ ✓ ✓ ✓ ✓ ✓ ✓ ✓ ✓ ✓ ✓ ✓ ✓ ✓ ✓ ✓ ✓ ✓ ✓ ✓ ✓ ✓ ✓ ✓ ✓ ✓ ✓ ✓ ✓ ✓ ✓ ✓ ✓ ✓ ✓ ✓ ✓ ✓ ✓ ✓ ✓ ✓ ✓ ✓ ✓ ✓ ✓ ✓ ✓ ✓ ✓ ✓ ✓ ✓ ✓ ✓ ✓ ✓ ✓ ✓ ✓ ✓ ✓ ✓ ✓ ✓ ✓ ✓ ✓ ✓ ✓ ✓ ✓ ✓ ✓ ✓ ✓ ✓ ✓ ✓ ✓ ✓ ✓ ✓ ✓ ✓ ✓ ✓ ✓ ✓ ✓ ✓ ✓ ✓ ✓ ✓ ✓ ✓ ✓ ✓ ✓ ✓ ✓ ✓ ✓ ✓ ✓ ✓ ✓ ✓ ✓ ✓ ✓ ✓ ✓ ✓ ✓ ✓ ✓ ✓ ✓ ✓ ✓ ✓ ✓ ✓ ✓ ✓ ✓ ✓ ✓ ✓ ✓ ✓ ✓ ✓ ✓ ✓ ✓ ✓ ✓ ✓ ✓ ✓ ✓ ✓ ✓ ✓ ✓ ✓ ✓ ✓ ✓ ✓ ✓ ✓ ✓ ✓ ✓ ✓ ✓ ✓ ✓ ✓ ✓ ✓ ✓ ✓ ✓ ✓ ✓ ✓ 
- MRoPE-v2 escala / MRoPE-v2 缩放. Posiciones escala con el tamaño máximo de entrada para que un video de 10 minutos no se agota del rango de frecuencia.

Compartidos: Qwen2.5-VL-72B supera a GPT-4o en la mayoría de los puntos de referencia de vídeo, coincide con Gemini 2.0 en documentos y establece el modelo abierto SOTA para la conexión a tierra de la interfaz gráfica (ScreenSpot: 84% de precisión frente a 38% para GPT-4o).

> **【中文解读】**La ruptura de Qwen2.5VL está en el entendimiento de vídeo: absolutamente tiempo token 让模型知道"第4秒猫跳了",动态率让模型在动作密集时自动提高采采样率,窗口注意力提升 ViT 吞吐量──72B 版本在视频基准上超越GPT-4o,GUI 定位精度(ScreenSpot 84%)远超GPT-4o(38%)──

> **【拓展：结构化输出对 Agent 工程的意义】**En el ámbito financiero, esto significa que VLM puede emitir estructurados "click sit-down" o "提取的字段", directamente consumidos por el sistema de down游系统, sin necesidad de expresar la resolución.

### Qwen3-VL (novembre 2025)

Qwen3-VL es una actualización incremental que consolida en lugar de reinventar: la columna vertebral de LLM más grande (Qwen3-72B), los datos de capacitación ampliados, la OCR mejorada, un razonamiento más fuerte a través del "modo de pensamiento" de Qwen3.

El resultado de la línea: para 2025 la arquitectura Qwen-VL se había estabilizado.

> **【中文解读】**Qwen3-VL es un aumento de la mejora de la cantidad y no un reinvenimiento: más grandes LLM 骨干、 más entrenamiento datos、 mejor OCR、 más fuerte de la hipótesis(Qwen3 "pensamiento")。ViT 和 M-RoPE 保持不变──En 2025, la estructura de Qwen-VL ya está estable, la versión posterior se actualizará principalmente a través de la ampliación y optimización de datos─

### M-RoPE matemáticamente.

El RoPE clásico gira una consulta `q`de dimensiones `d`por posición `m`utilizando coordenadas emparejadas:

```
q_rot[2i]   = q[2i]   * cos(m * theta_i) - q[2i+1] * sin(m * theta_i)   # 经典 RoPE 旋转
q_rot[2i+1] = q[2i]   * sin(m * theta_i) + q[2i+1] * cos(m * theta_i)
theta_i     = 10000^(-2i/d)                                                 # 频率基
```

M-RoPE divide el oscuro escondido en tres bandas.`d = 96`. Asesinar 32 puntos de menor tamaño a la altura, 32 a la anchura. Cada banda gira por su propia posición en el eje.`R_t(5)`¿ Qué ?`R_h(10)`¿ Qué ?`R_w(20)`se aplica a sus tres bandas.

Uso de tokens de texto `t = text_index, h = 0, w = 0`(o una opción normalizada), manteniendo la compatibilidad.`t = frame_time, h = row, w = col`. Uso de imágenes únicas `t = 0`¿ Qué ?

El beneficio: una codificación de posición maneja texto, imagen y video sin código ramificado o tablas de posición diferentes.

> **【中文解读】**M-RoPE va a dividir la dimensión oculta en tres frecuencias: tiempo, altura, ancho, cada uno de los segmentos de la serie de datos de la serie de datos de la serie de datos de la serie de datos de la serie de datos de la serie de datos de la serie de datos de la serie de datos de la serie de datos de la serie de datos de la serie de datos de la serie de datos de la serie de datos de la serie de datos de la serie de datos de la serie de datos de la serie de datos de la serie de datos de la serie de datos de la serie de datos de la serie de datos de la serie de datos de la serie de datos de la serie de datos de la serie de datos de la serie de datos de datos de la serie de datos de datos de la serie de datos de datos de la serie de datos de datos de la serie de datos de datos de la serie de datos de datos de la serie de datos de datos de la serie de datos de datos de datos de la serie de datos de datos de datos de la serie de datos de datos de datos de datos de la serie de datos de datos de datos de datos de datos de datos de la serie de datos de datos de datos de datos de datos de datos de datos de datos de la serie de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de

### Dinámica de muestreo de FPS lógica 动态 率采样逻辑

Dado un video de duración `T`segundos y un presupuesto de tokens objetivo `B`¿Qué es esto ?

1. Calcule el máximo de FPS que pueda permitirse: `fps_max = B / (T * tokens_per_frame)`.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             
2. Elige un FPS objetivo de `{1, 2, 4, 8}`que satisface `fps <= fps_max`De la tasa de selección de candidatos.
3. Si el movimiento es alto (heurística de flujo óptico o solicitud explícita del usuario), elija FPS más alto. Si el movimiento es bajo, elija más bajo.
4. Muestra uniforme en el FPS elegido; insertar `<time>t</time>`Los tokens entre los marcos.

Qwen2.5-VL entrena esta lógica implícitamente; en la inferencia el usuario controla a través de `fps`Parámetro: Una secuencia de acción de 60 segundos a 4 FPS con 81 tokens por fotograma = 19440 tokens, manejable en un contexto de 32k.

> **【中文解读】**动态率的核心思想:根据视频时长、代币 预算和运动量,自动选择最佳率──60秒动作场景在4FPS下产生19440代币,可在32k上下文中处理──

### Agencia estructurada salida .

La formación de agentes de Qwen2.5VL se dirige explícitamente a las llamadas de herramientas estructuradas:

```
{
  "tool": "mouse_click",          # 工具名称
  "coords": [1024, 512],          # 点击坐标
  "button": "left",               # 鼠标按钮
  "modifier": null                # 修饰键
}
```

El parse es determinista: JSON.parse sobre la salida del modelo. Comparar con el formulario libre "clic en (1024, 512) " que requirió el manejo de regex y ambigüedad. El cambio es por lo que las puntuaciones de ScreenSpot de Qwen2.5-VL saltaron del 55% a 84% de Qwen2-VL.

> **【中文解读】** Structured output permite que VLM pueda enviar directamente herramientas de resolución de modo que se puedan utilizar, como click 坐标), no necesita un modo de expresar.
```figure
mm-mrope-axes
```

## Usalo

## Usalo en práctica.

`code/main.py`los instrumentos:

- M-RoPE de la posición de cálculo para una secuencia de mezcla de texto, parches de imagen, y los marcos de vídeo.
- Muestra dinámica-FPS: dado (tiempo, presupuesto, movimiento_nivel), elegir FPS y emitir marcas de tiempo de marco.
- Un parser de salida de JSON Qwen2.5VL que maneja las respuestas de las llamadas de herramientas con campos de coordenadas.

## Envíalo .

Esta lección produce`outputs/skill-qwen-vl-pipeline-designer.md`. Dado una tarea de vídeo (monitoreo, agente, reconocimiento de acción, accesibilidad), emite la configuración Qwen2.5VL (orden de cuadro, estrategia FPS, bandera de atención de ventana, modo de salida de agente) y una estimación de latencia.

> **【中文解读】**Este curso se desarrolla en el campo de la tecnología de la información y de la información.

## Los ejercicios.

1. Calcule las rotaciones de M-RoPE para un parche en (t=3, h=5, w=7) con 48 ocultos (16 por banda, base theta 10000). Muestre los ángulos de rotación de los primeros tres pares en cada banda.
   | 计算 (t=3, h=5, w=7) 补丁的 M-RoPE 旋转，隐藏维度48（每频段16），基数10000。展示每频段前三对的旋转角度。

2. ¿Cuántos cuadros producen una cámara de seguridad de 10 minutos a 1 FPS? ¿A 384 de resolución con 3x pool, cuántos tokens totales? ¿El contexto predeterminado de Qwen2.5VL de 32k lo maneja?
   | 10分钟安防摄像头录像在 1FPS 下产生多少帧？384分辨率+3x池化后多少 token？Qwen2.5-VL 默认 32k 上下文能处理吗？

3. Elige FPS para un rally de tenis de 30 segundos vs. una demostración de receta de 30 segundos vs. una grabación de agente de interfaz de 30 segundos.
   | 为 30 秒网球比赛、30 秒食谱演示、30 秒 UI 代理录像选择帧率。用动态帧率逻辑论证每个选择。

4. Qwen2.5VL deja de funcionar el Q-Former por completo. ¿Por qué un MLP simple funciona en 2025 pero no en 2023?
   | Qwen2.5-VL 完全去掉了 Q-Former。为什么 MLP 在 2025 年可行但 2023 年不行？（提示：数据规模和编码器质量。）

5. Parsear tres Qwen2.5-VL JSON herramienta de llamadas de salida en Python dicts. ¿Qué falla en JSON malformado y qué estrategia de recuperación recomienda el libro de cocina Qwen?
   | 将三个 Qwen2.5-VL JSON 工具调用输出解析为 Python 字典。畸形 JSON 会出什么问题？Qwen 食谱推荐的恢复策略是什么？

## Términos clave .

| Term | What people say | What it actually means | 中文含义 | 中文释义 |
|------|-----------------|------------------------|----------|---------|
| M-RoPE | "Multimodal RoPE" | 3D rotary position embedding with temporal, height, and width bands in the hidden dim | 三维旋转位置编码，隐藏维度分时间、高度、宽度三个频段 | |
| Dynamic FPS | "Smart sampling" | Frame sampling rate chosen per video based on motion, duration, and token budget | 根据运动量、时长和 token 预算动态选择帧率 | |
| Absolute time token | "Timestamp token" | `<time>t</time>` interleaved in the sequence so the model sees actual seconds not frame index | 在序列中插入真实时间戳 token | |
| Window attention | "Local attention" | Spatial self-attention restricted to small windows for speed; global attention added periodically | 空间自注意力限制在小窗口内加速，周期性加入全局注意力 | |
| Structured agent output | "JSON mode" | Training data supervision teaching the VLM to emit parseable JSON with coords and tool names | 训练 VLM 输出可解析的 JSON（含坐标和工具名） | |
| min_pixels / max_pixels | "Resolution bounds" | Per-request Qwen2.5-VL controls bounding total pixel count and therefore token count | 按请求控制最小/最大像素数从而控制 token 数 | |
| Grounding | "Point-at-it" | Outputting bounding-box coordinates as text tokens; used since Qwen-VL v1 | 输出边界框坐标作为文本 token，从 Qwen-VL v1 开始支持 | |

## Más Leer más Leer más

- [Bai et al. — Qwen-VL (arXiv:2308.12966)](https://arxiv.org/abs/2308.12966)♬ Qwen-VL Primera generación
- [Wang et al. — Qwen2-VL (arXiv:2409.12191)](https://arxiv.org/abs/2409.12191)♬ Qwen2-VL M-RoPE
- [Qwen Team — Qwen2.5-VL Technical Report (arXiv:2502.13923)](https://arxiv.org/abs/2502.13923) Qwen2.5VL  Rate de movimiento 
- [Qwen Team — Qwen3-VL (arXiv:2511.21631)](https://arxiv.org/abs/2511.21631) Qwen3-VL                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                       
- [Zhu et al. — InternVL3 (arXiv:2504.10479)](https://arxiv.org/abs/2504.10479)¿Por qué no me gusta el trabajo?
