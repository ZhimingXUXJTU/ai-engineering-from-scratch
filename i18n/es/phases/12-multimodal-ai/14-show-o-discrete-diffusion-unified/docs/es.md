# Show-o y Discreto-Difusión Modelos Unificados .

> La transfusión mezcla representaciones continuas y discretas. Show-o (Xie et al., agosto 2024) va en el otro sentido: los tokens de texto utilizan la predicción causal del siguiente token, los tokens de imagen utilizan la difusión discreta enmascarada en el espíritu de MaskGIT. Ambos se sientan dentro de un transformador con una máscara híbrida de atención. El resultado unifica VQA, texto a imagen, inpainting y generación de modalidad mixta en una columna vertebral, un tokenizer por modalidad, una formulación de pérdida (se extiende el siguiente token a la predicción enmascarada). Esta lección recorre el diseño Show-o  por qué la difusión discreta enmascarada es un generador de imágenes paralelo y de pocos pasos  y contrasta con Transfusión y Emu3.

> **【中文解读】**Show-o(2024年8月)走另一条路:文本代币 用因果下一代币 预测,图像代币 用掩码离散散散散散(MaskGIT风格) ・・・ ambos comparten un transformador, usar mezcla de atención掩码── resultado de un punto de control 同时支持 VQA、文本生成图像和图像修复──

> **【拓展：并行解码的速度优势】**Show-o produce imágenes que sólo necesitan alrededor de 16 pasos, mientras que el Camelio/Emu3 necesita 1024-4096 pasos, por token de regreso. Esto hace que Show-o sea el modelo más rápido de su vida, pero la calidad de la imagen está limitada a la reconstrucción del token VQ.

**Type:** Learn  | **类型:** 学习
**Languages:** Python (stdlib, masked-discrete-diffusion sampler) | **语言:** Python（标准库，掩码离散扩散采样器）
**Prerequisites:** Phase 12 · 13 (Transfusion) | **前置知识:** Phase 12 · 13（Transfusion）
**Time:** ~120 minutes | **时间:** ~120 分钟

> ¿ Qué es esto ?**【前置】**學本節前请先掌握:Fase 12·13(Transfusión 双损失) ‧Fase 12·11-12(Chameleon/Emu3 离散代币) ‧Fase 8(MaskGIT 离散扩散概念) ‧Show-o = 全离散 + 图像使用MaskGIT 风格并行解码,速度比Emu3 快 60 倍──
> ¿ Qué es esto ?**【类比】**Show-o = "并行开锁"──Emu3 = una把钥匙开 1024 把锁(自归单代币);Show-o = 16 步内同时尝试所有锁(掩码扩散并行解码)──代价:图像质量略差(VQ 量化损失), pero la razón es rápida──

## Objetivos de aprendizaje

- Explica la difusión discreta enmascarada: el calendario que enmascara los tokens de forma uniforme luego pide al transformador que los recupere.
  > Explicar el esquizofrenia: el token de esquizofrenia en forma uniforme y luego dejar que el transformador recupere su regulación.
- Compare la descodificación de imágenes paralelas (Show-o, MaskGIT) con la descodificación de imágenes autoregresivas (Chameleon, Emu3) en velocidad y calidad.
  > Comparación y comparación de imágenes de desactivado (Show-o、MaskGIT) con imágenes de desactivado de desactivado (Chameleon、Emu3) en velocidad y calidad.
- Nombre de las tres tareas que se realizan en un solo punto de control: T2I, VQA, pintura de imagen.
  > 列举 Show-o en un puesto de control en el centro de apoyo de tres tareas: T2I、VQA、 retrato
- Seleccione un calendario de enmascaramiento (cosino, lineal, truncado) y razone su efecto sobre la calidad de la muestra.
  > 选择掩码调度 (余弦、线性、截断) y analizar su impacto en la calidad de la muestra.

## El problema es el contexto del problema

La pérdida de difusión continua vive en una escala numérica diferente a la pérdida discreta de NTP.

> El entrenamiento de doble pérdida de transfusión es posible pero el movimiento es más complejo  pérdida de propagación continua y pérdida de NTP separada  pérdida en la escala numérica es diferente                                                                                                                                                                                                                                        

La respuesta de Show-o: mantener ambas modalidades discretas (como Chameleon), pero generar imágenes en paralelo a través de difusión discreta enmascarada en lugar de secuencialmente.

> Respuesta: mantener dos modalidades son dispersas, pero a través de ocultar dispersas se genera una imagen, no una secuencia de generación.

## El concepto central.

> **【中文解读】**Show-o 统一多模态理解和生成, utilizar los procesos de descentralización de la generación de datos en lugar de los procesos de descentralización de datos en el contexto de la generación de datos.

> **【拓展：离散扩散的统一优势】**离散扩散将文本生成和图像生成统一到同一个数学框架 (图像生成统一到同一个数学框架) 掩码代币 预测), lo que hace que el entrenamiento conjunto de múltiples modelos sea más sencillo.


### Difusión discreta enmascarada (MaskGIT)

El truco original de Chang et al. (2022) MaskGIT es elegante.`<MASK>`En cada paso, predecir todos los tokens enmascarados en paralelo, luego mantener las predicciones más seguras de K y volver a enmascarar el resto. Después de ~ 8-16 iteraciones, todos los tokens se llenan.

> El original Chang 等人(2022) El arte de MaskGIT es muy bonito.`<MASK>`ID) ―― por cada paso se hace la predicción de todos los tokens ocultos, luego se mantiene el top-K 最有信心的预测并重新掩盖其余的──

La formación es simple: muestra una proporción de enmascaramiento uniformemente desde [0, 1], aplica a los tokens VQ de la imagen, entrena al transformador para recuperar los enmascarados.

> 训练很简单: desde [0, 1] 均采样掩码比例, aplicado a la imagen de VQ token, entrenamiento Transformer 恢复被掩码的 token──就是BERT对文本做,扩展到图像生成──

### Show-o: un transformador, máscara híbrida

El show-o pone MaskGIT dentro de un transformador de modelo de lenguaje causal.

> Show-o va a poner en el modelo de lenguaje de la transformación.

- Los tokens de texto: causal (MLL estándar).
  En inglés, el título de la LLM es "LLLM Standard".
- Tokens de imagen: bidireccionales completos dentro del bloque de imagen (para que los tokens enmascarados puedan ver todos los otros tokens de imagen durante la predicción).
  Se puede ver en el pronóstico todos los demás símbolos de imagen)。
- Texto a imagen: el texto se ajusta a las imágenes anteriores, la imagen se ajusta al texto anterior.
  En la actualidad, el texto es un texto de la historia de la historia.

Los cursos de formación alternativos entre:
1. NTP estándar en secuencias de texto.
   NTP estándar en el texto.
2. Muestras de T2I: texto → imagen con tokens de imagen enmascarados, pérdida de predicción de tokens enmascarados.
   En el caso de los ejemplos de la imagen, el símbolo de la imagen es el símbolo de la imagen.
3. Muestras de VQA: imagen → texto con tokens de texto enmascarados (en realidad sólo NTP).
   En el caso de los ejemplos de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de

La pérdida unificada es la entropía cruzada en `<MASK>`tokens, que cubre tanto el NTP de texto (solo el último token está "mascarado") como la difusión de imágenes enmascarada (un subconjunto aleatorio está enmascarado).

> 统一损失是                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        `<MASK>`El símbolo de la conexión es el símbolo de la conexión de la conexión.

### Muestreo paralelo

Show-o genera una imagen en ~16 pasos en lugar de ~1000 (autoregresivas por token) o ~20 (difusión).

> Show-o en aproximadamente 16 pasos dentro de la generación de imágenes, y no alrededor de 1000 pasos (por símbolo) o alrededor de 20 pasos (por símbolo) de expansión (por símbolo);

Comparar:
- Cameleón / Emu3 (autoregresividad sobre tokens): N_tokens pasa hacia adelante, típicamente 1024-4096 por imagen.
  En el caso de los ejemplos de la imagen, el nombre de la señal es "Chameleon" (en inglés: Chameleon) o "Emu3 (en inglés: Emu3 (en inglés: Chameleon) " (en inglés: Emu3 (en inglés: Chameleon) ), que significa "token de la señal de la señal de la señal de la señal de la señal de la señal de la señal de la señal de la señal de la señal de la señal de la señal de la señal de la señal de la señal de la señal de la señal de la señal de la señal de la señal de la señal de la señal de la señal de la señal de la señal de la señal de la señal de la señal de la señal de la señal de señal de la señal de señal de señal de señal de señal de señal de señal de señal de señal de señal de señal de señal de señal de señal de señal de señal de señal de señal de señal de señal de señal de señal de señal de señal de señal de señal de señal de señal de señal de señal de señal de señal de señal de señal de señal de señal de señal de señal de señal de señal de señal de señal de señal de señal de señal de señal de señal de señal de señal de señal de señal de señal de señal de señal de señal de señal de señal de señal de señal de señal de señal de señal de señal de señal de señal de señal de señal de señal de señal de señal de señal de señal de señal de señal de señal de señal de señal de señal de señal de señal de señal de señal de señal de señal de señal de señal de señal de señal de señal de señal de señal de señal de señal de señal de señal de señal de señal de señal de señal de señal de señal de señal de señal de señal de señal de señal de señal de señal de señal de señal de señal de señal de señal de señal de señal de señal de señal de señal de señal de señal de señal de señal de señal de señal de señal de señal de señal de señal de señal de señal de señal de señal de señal de señal de señal de señal de señal de señal de señal de señal de señal de señal de señal de señal de señal de señal de señal de señal de señal de señal de señal de señal de señal de señal de señal de señal de señal de señal de que se de señal de señal de señal de señal de señal de que se de que se de que se que se ha
- Transfusión (difusión continua): ~20 pasos, cada uno con un transformer completo.
  Transfusión: aproximadamente 20 pasos, cada paso una vez completo Transformer 传播。
- Show-o (difusión discreta enmascarada): ~16 pasos, cada uno con un transformer completo.
  En el caso de los transformas, el transformer puede ser un transformer completo.

Show-o es más rápido que el Chameleon en modelos de escala similar, coincide aproximadamente con el recuento de pasos de Transfusión con un menor costo por paso (logitas de vocabulario discreta vs pérdida continua de MSE).

> Show-o en comparación de tamaño modelo en comparación con el camaleón más rápido, el número de pasos de gran tamaño para la transfusión, pero el costo de cada paso es más bajo.

### tareas en un solo puesto de control

Show-o admite cuatro tareas en la inferencia, seleccionadas por formato de respuesta rápida:

> Show-o en el tiempo de la propuesta apoyar cuatro tareas, a través de sugerencias de forma de selección:

- Generación de texto: salida de texto autoregresista estándar.
  El texto original de la traducción de la traducción de la lengua inglesa de la lengua inglesa de inglés de la lengua inglesa de inglés de inglés de inglés de inglés de inglés de inglés de inglés de inglés de inglés de inglés de inglés de inglés de inglés de inglés de inglés de inglés de inglés de inglés de inglés de inglés de inglés de inglés de inglés de inglés de inglés de inglés de inglés de inglés de inglés de inglés de inglés de inglés de inglés de inglés de inglés de inglés de inglés de inglés de inglés de inglés de inglés de inglés de inglés de inglés de inglés de inglés de inglés de inglés de inglés de inglés de inglés de inglés de inglés de inglés de inglés de inglés de inglés de inglés de inglés de inglés de inglés de inglés de inglés de inglés de inglés de inglés de inglés de inglés de inglés de inglés de inglés de inglés de inglés de inglés de inglés de inglés de inglés de inglés de inglés de inglés de inglés de inglés de inglés de inglés de inglés de inglés de inglés de inglés de inglés de inglés de inglés de inglés de inglés de inglés de inglés de inglés de inglés de inglés de inglés de inglés de inglés de inglés de inglés de inglés de inglés de inglés de inglés de inglés de inglés de inglés de inglés de inglés de inglés de inglés de inglés de inglés de inglés de inglés de inglés de inglés de inglés de inglés de inglés de inglés de inglés de inglés de inglés de inglés de inglés de inglés de inglés de inglés de inglés de inglés de inglés de inglés de inglés de inglés de inglés de inglés de inglés de inglés de inglés de inglés de inglés de inglés de inglés de inglés de inglés de inglés de inglés de inglés de inglés de inglés de inglés de inglés de inglés de inglés de inglés de inglés de inglés de inglés de inglés de inglés de inglés de inglés de inglés de inglés de inglés de inglés de inglés de inglés de inglés de inglés de inglés de inglés de inglés de inglés de inglés de inglés de inglés de inglés de inglés de inglés de inglés de inglés de inglés de inglés de English de English de English de English de English de English de English de English de English de English de English de English de English de English de English de English de English de English de English de English de English de English de English de English de English de English de English de English de English de English de English de English de English de English de English de English de English de English de German de English de English de German de German de English de English de German de German de English de German de German de English de German de German de German de
- VQA: imagen en, mensaje de texto.
  En el texto original, el texto se traduce en "VQA".
- T2I: entrada de texto, salida de imagen a través de difusión discreta enmascarada.
  En el texto original, el texto se encuentra en el texto original.
- Inpintado: imagen con algunos tokens enmascarados, rellenar.
  China: 图像修复:带部分掩码 token 的图像,填充缺失部分──

La capacidad de pintura viene de forma gratuita de la formación de predicción enmascarada. Enmascarar una región de la cuadrícula de tokens VQ, alimentar el resto más un mensaje de texto, predecir los tokens enmascarados.

> 图像修复能力从掩码预测训练中免费获得──掩码 VQ token 网格的一个区域,进入其余部分加上文本提示,预测被掩码的代币──

### Programa de enmascaramiento

El calendario de cuántos tokens desmascarar por paso forma la calidad.

> Cada paso de la secuencia de un símbolo de la secuencia de un símbolo de un símbolo de un símbolo de la secuencia de un símbolo de un símbolo de la secuencia de un símbolo de un símbolo de la secuencia de un símbolo de un símbolo de la secuencia de un símbolo de un símbolo de la secuencia de un símbolo de la secuencia de un símbolo de la secuencia de un símbolo de la secuencia de un símbolo de la secuencia de un símbolo de la secuencia de un símbolo de un símbolo de la secuencia de un símbolo de la secuencia de un símbolo de un símbolo de la secuencia de un símbolo de un símbolo de la secuencia de un símbolo de un símbolo de la secuencia de un símbolo de un símbolo de la secuencia de un símbolo de la secuencia de un símbolo de un símbolo de la secuencia de un símbolo de un símbolo de la secuencia de un símbolo de un símbolo de la secuencia de un símbolo de un símbolo de la secuencia de un símbolo de un símbolo de un símbolo de un símbolo de la secuencia de un símbolo de un símbolo de un símbolo de un símbolo de un símbolo de un símbolo de un símbolo de un símbolo de un símbolo de un símbolo de un símbolo de un símbolo de un símbolo de un símbolo de un símbolo de un símbolo de un símbolo de un símbolo.

```
mask_ratio(t) = cos(pi * t / (2 * T))   # t = 0..T
```

En el paso 0, todos los tokens están enmascarados (ratio 1.0). en el paso T, ninguno está enmascarado. Cosino concentra la masa en proporciones de medio rango donde la predicción es más informativa.

> Se trata de un proceso de formación de la estructura de la estructura de la estructura de la estructura.

### El programa de trabajo

Show-o2 (2025 seguimiento, arXiv 2506.15564) escalas Show-o: mayor base de LLM, mejor tokenizer, mejor cronograma de máscara.

### Donde se sienta Show-o

En la taxonomía de 2026:

> En 2026 años de las categorías:

- Tokens discretos + NTP: camaleón, Emu3.
  En inglés, el nombre de la palabra "Chameleon" se traduce en "Chameleon".
- Tokens discretos + difusión enmascarada: Show-o, MaskGIT, LlamaGen, Muse. Muestreo paralelo, todavía perdida por el tokenizer.
  En el caso de los ejemplos de la lengua inglesa, el nombre de la lengua inglesa es "MaskGIT".
- Transfusión continua + difusión: Transfusión, MMDiT, DiT. La formación de mayor calidad y más compleja.
  En el caso de la transfusión, el proceso de formación es más complejo.
- Aparición continua + flujo en un VLM: JanusFlow, InternVL-U. Más reciente.
  En el caso de los viajeros, el número de viajeros es de aproximadamente un millón de personas.

Seleccionar por tarea: Show-o cuando se quiere T2I + inpainting + VQA en un modelo abierto con una velocidad razonable; Transfusión cuando la calidad es primordial y se puede pagar la plomería de dos pérdidas.

> 按任务选择: necesita un modelo abierto al mismo tiempo hacer T2I + 修复 + VQA 且速度合理时选 Show-o;质量至上且能承担双损失复杂性时选转


> **【拓展：Show-o 的离散扩散方法】**Se puede ver el número de ejemplos de la función de la función de la función de la función de la función de la función de la función de la función de la función de la función de la función de la función de la función de la función de la función de la función de la función de la función de la función de la función de la función de la función de la función de la función de la función de la función de la función de la función de la función de la función de la función de la función de la función de la función de la función de la función de la función de la función de la función de la función de la función de la función de la función de la función de la función de la función de la función de la función de la función de la función de la función de la función de la función de la función de la función de la función de la función de la función de la función de la función de la función de la función de la función de la función de la función de la función de la función de la función de la función de la función de la función de la función de la función de la función de la función de la función de la función de la función de la función de la función de la función de la función de la función de la función de la función de la función de la función de la función de la función de la función de la función de la función de la función de la función de la función de la función de la función de la función de la función de la función de la función de la función de la función de la función de la función de la función de la función de la función de la función de la función de la función de la función de la función de la función de la función de la función de la función de la función de la función de la función de la función de la función de la función de la función de la función de la función de la cuta de la cuento.


## Usalo en práctica.
```figure
masked-diffusion-unmask
```

## Usalo

`code/main.py`simula la muestreo de muestra:

> `code/main.py`模拟 Show-o 采样:

- Una cuadrícula de juguetes de 16 tokens VQ.
  Un 16 VQ token de juguete red.
- Un falso "transformador" que predice logits basándose en un prompt y los tokens actualmente desmascarados.
  Un modelo de "transformador", basado en la señal de la señal de la señal de la señal de la señal de la señal de la señal de la señal de la señal de la señal de la señal de la señal de la señal de la señal de la señal de la señal de la señal de la señal de la señal de la señal de la señal de la señal de la señal de la señal de la señal de la señal de la señal de la señal de la señal de la señal de la señal de la señal de la señal de la señal de la señal de la señal de la señal de la señal de la señal de la señal de la señal de la señal de la señal de la señal de la señal de la señal de la señal de la señal de la señal de la señal de la señal de señal de la señal de señal de la señal.
- Muestreo enmascarado paralelo en 8 pasos con horario cosino.
  En el texto original, el texto se traduce como "el amor de Dios".
- Imprime los estados intermedios (evolución de patrones de máscara) y los tokens finales.
  En el caso de los ejemplos de la lengua inglesa, el nombre de la lengua inglesa es "Middle State".

Echa un vistazo a la máscara disolverse paso a paso.

> ¿Qué es eso?

## Envíalo .

Esta lección produce`outputs/skill-unified-gen-model-picker.md`. Dado un producto que necesita tanto comprensión (VQA, subtítulos) como generación (T2I, inpainting) con una restricción de peso abierto, escoge entre la familia Show-o, la familia Transfusion/MMDiT y la familia Emu3/Chameleon con compensaciones concretas.

> 本课产 出  `outputs/skill-unified-gen-model-picker.md`△给定需要理解(VQA、描述) 和生成(T2I、修复) y está restringido a la libre distribución de productos, en Show-o、Transfusion/MMDiT 和 Emu3/Chameleon

## Los ejercicios.

1. ¿Por qué no 1? ¿Qué se rompe si desmascaras todo en el paso 0?
   En el primer paso, ¿qué ocurre si se desvanece todo el token?

2. La pintura es libre con difusión enmascarada. Propón un caso de uso del producto (real o hipotético) en el que la pintura de Show-o supera a un modelo especializado.
   China 翻译:掩码扩散的图像修复是免费的―― propone un ejemplo de la capacidad de la muestra de la reparación de los modelos de productos de la industria.

3. Calendario cosino vs calendario lineal: rastrear el número de tokens desmascarados por paso para T=8. ¿Cuál es más equilibrado?
   China 翻译:余弦调度 vs 线性调度: 追踪 T=8 时每步解掩码的符号 数―― ¿Cuál es el mejor equilibrio?

4. Una imagen de 512x512 Show-o es de 1024 tokens. En la vocab K=16384, el modelo emite 1024 * log2(16384) = 14.336 bits (~1.75 KiB) de datos.
   En el caso de los modelos de la imagen, el tamaño de la imagen es de 1.75 Kb.

5. ¿En qué se diferencia el modelo de imagen autorregresista con condiciones de clase de LlamaGen del enfoque enmascarado de Show-o?
   En la actualidad, el sistema de ocultamiento de los imágenes es un sistema de ocultamiento de los imágenes.

## Términos clave .

| Term | What people say | What it actually means | 中文含义 | 中文释义 |
|------|-----------------|------------------------|---------|
| Masked discrete diffusion | "MaskGIT-style" | Training to predict masked tokens; at inference, iteratively unmask the most-confident predictions | 训练预测掩码 token；推理时迭代解掩码最有信心的预测 |
| Cosine schedule | "Unmask schedule" | Decay of mask ratio over inference steps; concentrates confidence growth at mid-range | 推理步骤中掩码比例的衰减；将信心增长集中在中程 |
| Parallel decoding | "All tokens at once" | Every step predicts the full sequence of masked tokens in one forward pass, then commits top-K | 每步在一次前向传播中预测所有掩码 token，然后提交 top-K |
| Hybrid attention | "Causal + bidirectional" | Mask that is causal over text tokens and bidirectional within image blocks | 文本 token 因果、图像块内双向的掩码 |
| Inpainting | "Fill-in generation" | Condition on an image with some tokens masked, predict the missing ones; free from the training objective | 以部分掩码图像为条件，预测缺失 token；从训练目标免费获得 |
| Commitment rate | "Top-K per step" | How many tokens are declared "done" per iteration; controls inference vs quality trade-off | 每次迭代声明"完成"的 token 数；控制推理与质量的权衡 |

## Más Leer más Leer más

- [Xie et al. — Show-o (arXiv:2408.12528)](https://arxiv.org/abs/2408.12528)
  En el caso de los niños, el problema es que no hay nada que hacer.
- [Show-o2 (arXiv:2506.15564)](https://arxiv.org/abs/2506.15564)
  En el caso de los que se encuentran en el centro de la ciudad, el número de personas que se encuentran en el centro de la ciudad es el número de personas que se encuentran en el centro de la ciudad.
- [Chang et al. — MaskGIT (arXiv:2202.04200)](https://arxiv.org/abs/2202.04200)
  En el caso de los trabajadores de la empresa, el trabajo inicial de la empresa es de la misma naturaleza.
- [Sun et al. — LlamaGen (arXiv:2406.06525)](https://arxiv.org/abs/2406.06525)
  La lengua árabe se traduce en lengua árabe como "la lengua árabe".
- [Chang et al. — Muse (arXiv:2301.00704)](https://arxiv.org/abs/2301.00704)
  Muz 掩码图像生成── también conocido como Muz 掩码.
