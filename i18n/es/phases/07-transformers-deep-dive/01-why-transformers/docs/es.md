# Por qué los transformadores  Los problemas con las RNN
# ¿Por qué es el problema de Transformer  RNN

> RNNs procesan tokens uno a la vez. Transformers procesan todos los tokens a la vez. Esa sola apuesta arquitectónica cambió cada curva de escala en el aprendizaje profundo después de 2017.

> RNN 个别处理代币――Transformer 一次性处理所有代币―― Esta estructura 注注 cambió cada una de las curvas de expansión del aprendizaje profundo después de 2017.

> **【中文解读】**RNN tiene tres problemas mortales: no puede caminar, el largo de la escala desaparece, el largo de la longitud fija se encuentra en el transformer.

**Type:** Learn | **类型:** 学习
**Language:**¿ Qué pasa ?**语言:**Python
**Prerequisites:** Phase 3 (Deep Learning Core), Phase 5 · 09 (Sequence-to-Sequence), Phase 5 · 10 (Attention Mechanism) | **前置知识:** 阶段 3（深度学习基础），阶段 5 · 09（序列到序列），阶段 5 · 10（注意力机制）
**Time:** ~45 minutes | **时间:** ~45 分钟

## Objetivos de aprendizaje

- Comprender las tres debilidades fatales de las redes neuronales recurrentes (RNN)
  En el sentido de entender los tres puntos débiles de la red de los nervios
- Explica por qué la profundidad de serie, no el número de operaciones, determina el tiempo de entrenamiento de la GPU
   Explicar por qué la profundidad de la serie (y no la cantidad de operaciones) determinó el tiempo de entrenamiento de la GPU
- Comparación de la complejidad de RNN vs Transformer en las tareas de modelado de secuencias
  Comparar RNN con Transformer en la complejidad de la tarea de construcción de secuencias
- Identificar escenarios en los que aún se puedan preferir los RNN o los modelos del espacio estatal
  识别 RNN o estado del modelo espacial sigue siendo mejor escenario
- Reconocer el cambio de sesgo inductivo de la localidad a la atención global
  認識從局部性到全局注意力归纳偏好轉移 認識

## El problema es la introducción del problema

Antes de 2017, cada modelo de secuencia de última generación en el planeta  lenguaje, traducción, habla  era una red neuronal recurrente. LSTMs y GRU ganaron puntos de referencia de traducción equivalentes a ImageNet durante media década. Fueron la única herramienta que alguien tenía.

> Antes de 2017, cada uno de los modelos de secuencia más avanzados del mundo eran una red de nervios circulares. Los sistemas de traducción y de análisis de base de datos de la red de imágenes de la red de Internet se han convertido en un sistema de análisis de base de traducción de cinco años.

El cálculo secuencial significaba que no se podía paralelalizar a lo largo del eje del tiempo:`t+1`Necesita el estado oculto de la señal .`t`Una secuencia de 1.024 tokens significaba 1.024 pasos en serie en una GPU que puede hacer 1.000.000 operaciones de puntos flotantes por ciclo.

> Tienen tres puntos débiles.`t+1` necesita de un token `t`El estado oculto de una secuencia de 1,024 tokens significa que en cada ciclo se puede ejecutar 1,000,000 veces el cálculo de puntos de flotación de la GPU para ejecutar 1,024 pasos en secuencia. En hardware diseñado para la paralelidad, el tiempo de entrenamiento aumenta con la longitud de la secuencia.

> **【中文解读】**El primer punto débil mortal: la secuencia de cálculo. RNN  debe procesar cada token de manera ordenada, completamente incapaz de utilizar la capacidad de cálculo de la secuencia de GPU.  El tiempo de entrenamiento y el crecimiento de la longitud de la secuencia son enormes gastos en la era de la GPU.

Los gradientes desaparecientes significaban que la información 50 tokens atrás ya estaba comprimida a través de 50 no linealidades. Las unidades recurrentes de gated (LSTM, GRU) suavizaron la aplastamiento pero nunca lo eliminaron. Las dependencias de largo alcance  "el libro que leí el verano pasado en un avión a Kioto fue..."  rotineamente fracasó.

> 梯度消失 significa 50 tokens                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                      

> **【中文解读】**El segundo punto débil mortal: la desaparición de la escala. Tras 50 niveles de transformación no lineal, la información de la zona es casi completamente perdida.

Los estados ocultos de ancho fijo significaban que el codificador comprimió toda la secuencia de fuente en un solo vector antes de que el decodificador viera algo.

> El estado oculto de la amplitud fija significa que antes de que el codificador vea cualquier contenido, el procesador comprimirá toda la secuencia de origen en un eje.

> **【中文解读】**El tercer punto débil mortal: botella de anchura fija. El codificador debe comprimir toda la secuencia de origen a un volumen de longitud fija.

El artículo de 2017 "Attención es todo lo que necesitas" propuso algo radical: dejar de recurrir por completo. Dejar que cada posición atenda a cada otra posición en paralelo. Entrenar en una gran matriz multiplicación en lugar de 1.024 secuenciales.

> El artículo de 2017 "La atención es todo lo que necesitas" propuso un esquema de acción: abandonar completamente el ciclo.

El resultado domina todas las modalidades para 2026. lenguaje (GPT-5, Claude 4, Llama 4), visión (ViT, DINOv2, SAM 3), audio (Whisper), biología (AlphaFold 3), robótica (RT-2).

> Hasta 2026 años, sus resultados dominan cada tipo de modèles.

## El concepto central.

![RNN sequential compute vs Transformer parallel attention](../assets/rnn-vs-transformer.svg)

**Recurrence as a bottleneck.**Un RNN computa `h_t = f(h_{t-1}, x_t)`Cada paso depende del anterior. No puedes calcular.`h_5`antes de`h_4`En las GPU modernas con más de 10.000 núcleos paralelos, esto desperdicia el 99% del silicio en una larga secuencia.

> **循环即瓶颈。**RNN 计算 `h_t = f(h_{t-1}, x_t)`Cada paso depende del paso anterior.`h_4`之前计算 `h_5`❖ En tener más de 10,000 y ejecutar el núcleo de la GPU moderna, esto desperdicia el 99% de la capacidad de cálculo de los chips de la serie larga.

> **【中文解读】**El ciclo es la esencia de la botella: cada paso de tiempo del cálculo depende de los resultados del paso anterior. La GPU es excelente en miles de millas de operaciones simultáneas, mientras que la cadena de RNN depende de que sólo pueda utilizarse en una pequeña parte de la capacidad de cálculo de la GPU. El transformador, a través de su propia atención, procesará la secuencia de O(N) 串行深度降至O(1), liberando completamente la capacidad de la GPU de simultánea.

**Attention as a broadcast.**Cuentas de autoatención `output_i = sum_j(a_ij * v_j)`para cada par `(i, j)`La matriz de atención N×N completa un matmul en lote. Ningún paso depende de otro.

> **注意力即广播。**Yo me he puesto en el mismo lugar.`(i, j)`计算 `output_i = sum_j(a_ij * v_j)`◊ Toda la N×N Atención de la matriz está llena en una matriz de multiplicidad de un solo lote.

**The speedup is not a constant.**Es la diferencia entre `O(N)`profundidad en serie y `O(1)`En la práctica, los transformadores se entrenan 510x más rápido por época en hardware coincidente a N=512, y la brecha se amplía con la longitud de la secuencia hasta que se golpea el `O(N²)`pared de memoria de la atención (que Flash Attention posteriormente arregló  ver Lección 12).

> **加速不是常数。**Es un buen trabajo .`O(N)`串行深度与                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        `O(1)`En la práctica, en el hardware de la combinación N=512 时, Transformer Cada época de la formación velocidad rápida 5-10 veces, y el espacio aumenta con la longitud de la secuencia hasta que te encuentras con la atención.`O(N²)`Interior del muro (Flash Attention)

**What transformers cost.**Escales de memoria de atención como `O(N²)`Para el contexto de 2K, bien. Para el contexto de 128K, necesitas ventanas correderas, extrapolación RoPE, mosaico de atención flash, o variantes de atención lineal.`O(N)`en tiempo y memoria; los transformadores intercambian tiempo por memoria y luego ganan el tiempo de vuelta a través del paralelismo.

> **Transformer 的代价。**                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             `O(N²)`增长──对于2K上下文,没有问题──对于128K上下文,你需要滑窗,RoPE外推,Flash Attention 分块计算或线性注意力变体──循环在时间和内存都是`O(N)`Transformador con tiempo de memoria, luego pasa por el tiempo de ganar.

**The inductive bias shift.**Los transformadores no asumen nada.  cada par es un candidato a la atención. Es por eso que los transformadores necesitan más datos para entrenar bien, pero escalar más una vez que lo tengan. Chinchilla (2022) formalizó esto: dado suficientes tokens, un transformador siempre supera un RNN de igual número de parámetros.

> **归纳偏好的转变。**RNN 假设局部性和邻近性──Transformer no hace ninguna hipótesis Cada par es candidato de atención── es por eso que Transformer 需要更多数据来训练好, pero una vez que tenga suficiente datos, podrá expandirse más lejos──Chinchilla(2022) formalizó este punto: dado suficiente token, Transformer 总是击败同等参数的 RNN──

> **【中文解读】**La transferencia de preferencias de regulación es la clave del éxito del transformador. RNN 隐式假设"近处的符号更重要", mientras que el transformador no hace ninguna hipótesis  entre cualquier posición puede establecer una conexión directa.

> **【拓展：Chinchilla 缩放定律】**El artículo de Chinchilla de DeepMind 文章(2022) demuestra que el tamaño de los modelos y la cantidad de datos de entrenamiento se han incrementado en proporciones. Esto explica por qué los modelos Llama 、 GPT-4  necesitan millones de tokens de datos de entrenamiento  debilidad de inclusión  necesitan una gran cantidad de datos para "compensarse".

## Construye y realiza.
```figure
rnn-vs-parallel
```

## Construye el mismo

No hay red neuronal aquí Simulado el cuello de botella del núcleo numéricamente para que sienta la brecha en su portátil.

> Aquí no hay una red neuronal. Usamos un núcleo de valores para hacerte sentir la diferencia en el ordenador.

> **【中文解读】**Esta sección utiliza un modelo de valor numérico puro para hacerte sentir de cerca la diferencia de rendimiento de la cadena versus la cadena. La clave es que la profundidad de la cadena depende de la profundidad de la cadena para N, mientras que la profundidad de la cadena para la redondeza es sólo de O(1) o O(log N) ;; esta es la razón fundamental de la transformación de RNN 快.

### Paso 1: Medir la profundidad de serie.

¿ Qué ?`code/main.py`Construimos dos funciones: una codifica una secuencia como una cadena de adiciones (serial, como un RNN). otra lo codifica como una reducción paralela (broadcast, como la atención).

> 参见 `code/main.py`△ Nosotros construimos dos funciones― una se codificará la serie para la cadena de adición △串行, similar a RNN)― una se codificará para la并行归约 △广播, similar a atención △ la misma matemática, diferentes dependencias △

```python
def rnn_style(xs):
    h = 0.0
    for x in xs:
        h = 0.9 * h + x   # can't parallelize: h depends on previous h
    return h

def attention_style(xs):
    return sum(xs) / len(xs)  # every x is independent
```

Los datos de la secuencia de la CPU son de un solo tipo, pero la secuencia de la CPU es de un solo tipo.`sum()`se implementa en C y se repite sin gastos generales de intérprete por paso.

> Se calcula la secuencia de hasta 100.000 elementos. La versión RNN es una sola CPU de O(N) 流水线. Incluso en Python puro, el estilo de atención 归约在长度 ≥ 1,000 时也能胜出, ya que Python `sum()`Es un proceso de desarrollo de la lengua, sin explicación de la lengua.

### Paso 2: Cuenta las operaciones teóricas . Paso 2: calcular las operaciones teóricas .

Los algoritmos añaden N. La diferencia es *profundidad de dependencia*: cuántas operaciones deben ocurrir secuencialmente antes de que pueda comenzar el siguiente. RNN profundidad = N. Profundidad de atención = log(N) con una reducción de árbol, o 1 con un escaneo paralelo.

> 两种算法都做N 次加法──区别在* dependiente de la profundidad*: en el siguiente operación, antes de comenzar, debe ordenarse realizar cuántas operaciones。RNN profundidad = N。

### Paso 3: Escalación empírica en secuencias largas.

Impresamos una tabla de tiempo que hace que la brecha O(N) sea visible. En un portátil Mac 2026, las secuencias de menos de 1.000 elementos son demasiado rápidas para medir. Las secuencias de 100.000 muestran un escaneo lineal limpio. Escala eso a un transformador de 16.384 tokens con un equivalente LSTM de 12 capas y ves por qué el entrenamiento de relojes murales fue un bloqueador en 2016.

> En el cuaderno de Mac de 2026 , la secuencia de menos de 1.000 elementos es demasiado rápida e incalculable. En el cuaderno de 100 000 elementos se muestra un claro análisis lineal. Se extiende a un transformador de 16,384 tokens con 12 niveles LSTM, y se entenderá por qué el tiempo de entrenamiento de 2016 es un botella.

## Usalo con el marco de ejecución

¿Cuándo elegir un RNN en 2026?

> 2026 年何时仍应选择 RNN:

> **【中文解读】**Aunque el Transformer ha logrado ganar en la mayoría de los escenarios, pero no ha logrado hacerlo.

> **【拓展：Mamba 与状态空间模型】**Mamba(2023) A través del mecanismo de selección de barrido ha logrado la construcción de secuencias de complejidad O(N), al mismo tiempo que apoya el entrenamiento de la misma manera.

| Situation | Pick / 场景 | 选择 |
|-----------|-------------|------|
| Streaming inference, one token at a time, constant memory | RNN or state-space model (Mamba, RWKV) |
| Very long sequences (>1M tokens) where attention memory explodes | Linear attention, Mamba 2, Hyena |
| Edge device with no matmul accelerator | Depthwise-separable RNN still wins on FLOPs/watt |
| Anything else (training, batched inference, context up to 128K) | Transformer |

Los modelos de espacio estatal (SSM) como Mamba son esencialmente RNNs con parametrización estructurada que les da lo mejor de ambos: `O(N)`La mayoría de los laboratorios fronterizos entrenan modelos híbridos de transformadores SSM+ (por ejemplo, Jamba, Samba)  la recurrencia no está muerta, es un componente.

> 状态空间模型 (SSM) como Mamba es en su naturaleza RNN estructurado, y tiene ventajas de ambos:`O(N)`扫描内存, 通过选择性扫描实现并行训练――它们 recuperaron la calidad del Transformer 90% , al mismo tiempo con una mejor长上下文扩展性―― 2026 La mayoría de los laboratorios de la vanguardia de la década de 2026 entrenan mezclado SSM+Transformer 模型(como Jamba、Samba)  ciclo no ha desaparecido, es un componente―

## Envíe el producto .

¿ Qué ?`outputs/skill-architecture-picker.md`La habilidad elige una arquitectura para un nuevo problema de secuencia dada la longitud, el rendimiento y las limitaciones del presupuesto de entrenamiento.

> 参见 `outputs/skill-architecture-picker.md` Esta habilidad para la nueva secuencia de problemas de selección de estructura, dado la longitud, la capacidad y el presupuesto de entrenamiento.

> **【拓展：架构选择决策树】**En el proyecto real, la selección de arquitectura necesita considerar varias dimensiones: longitud de la serie, retraso de la solicitud, presupuesto de memoria, cantidad de datos de entrenamiento, implementación de hardware. Para la mayoría de las tareas de NLP, el Transformer solo para decodificadores es una opción de tipo de elección; para la secuencia de superluz, considerar Mamba o arquitectura mixta; para la implementación de bordes, RNN/SSM cuantificada puede ser más adecuada.

## Los ejercicios.

1. **Easy / 简单。**¿ Qué ?`rnn_style`de la`code/main.py`y reemplazar el estado oculto escalar con un vector de longitud-64 de estados ocultos.
   取 `code/main.py`En el centro`rnn_style`, ¿se sustituirá la dimensión del estado oculto por la longitud 64 de la dimensión del estado oculto.

2. **Medium / 中等。**Implemente una suma de prefijos paralelas (escaneo de Hillis-Steele) en Python puro. Verifique que produce la misma salida numérica que un escaneo en serie en longitud 1024. Cuente la profundidad.
   Utiliza pure Python                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                          

3. **Hard / 困难。**Portar la reducción de estilo de atención a PyTorch en la GPU. tiempo tanto como varía la longitud de la secuencia de 64 a 65.536.
   La velocidad de la velocidad de la velocidad de la velocidad de la velocidad de la velocidad de la velocidad de la velocidad de la velocidad de la velocidad de la velocidad de la velocidad de la velocidad de la velocidad de la velocidad de la velocidad de la velocidad de la velocidad de la velocidad de la velocidad de la velocidad de la velocidad de la velocidad de la velocidad de la velocidad de la velocidad de la velocidad de la velocidad de la velocidad de la velocidad de la velocidad de la velocidad de la velocidad de la velocidad de la velocidad de la velocidad de la velocidad de la velocidad de la velocidad de la velocidad de la velocidad de la velocidad de la velocidad de la velocidad de la velocidad de la velocidad de la velocidad de la velocidad de la velocidad de la velocidad de la velocidad de la velocidad de la velocidad de la velocidad de la velocidad de la velocidad de la velocidad de la velocidad de la velocidad de la velocidad de la velocidad de la velocidad de la velocidad de la velocidad de la velocidad de la velocidad de la velocidad de la velocidad de la velocidad de la velocidad de la velocidad de la velocidad de la velocidad de la velocidad de la velocidad de la velocidad de la velocidad de la velocidad de la velocidad de la velocidad de la velocidad de la velocidad de la velocidad de la velocidad de la velocidad de la velocidad de la velocidad de la velocidad de la velocidad de la velocidad de la velocidad de la velocidad de la velocidad de la velocidad de la velocidad de la velocidad de la velocidad de la velocidad de la velocidad de la velocidad de la velocidad de la velocidad de la velocidad de la velocidad de la velocidad de la velocidad de la velocidad de la velocidad de la velocidad de la velocidad de la velocidad de la velocidad de la velocidad de la velocidad de la velocidad de la velocidad de la velocidad de la velocidad de la velocidad de la velocidad de la velocidad de la velocidad de la velocidad de la velocidad de la velocidad de la velocidad de la velocidad de la veloc

## Términos clave .

| Term | What people say / 术语 | 人们怎么说 | What it actually means / 实际含义 |
|------|----------------------|-----------|----------------------------------|
| Recurrence | "RNNs are sequential" | 循环 (Recurrence) | Computation where step `t` depends on step `t-1`, forcing serial execution along the time axis. 步骤 `t` 依赖于步骤 `t-1` 的计算，强制沿时间轴串行执行。 |
| Serial depth | "How deep the graph is" | 串行深度 (Serial depth) | Longest chain of dependent ops; bounds wall-clock even on infinite hardware. 依赖操作的最长链；即使在无限硬件上也限制了时间开销。 |
| Attention | "Let tokens look at each other" | 注意力 (Attention) | Weighted sum `sum_j a_ij v_j` where `a_ij` comes from a similarity score between positions i and j. 加权求和 `sum_j a_ij v_j`，其中 `a_ij` 来自位置 i 和 j 之间的相似度得分。 |
| Context window | "How much the model sees" | 上下文窗口 (Context window) | Number of positions an attention layer can take as input; quadratic memory cost scales here. 注意力层可作为输入的位置数；二次内存开销在这里缩放。 |
| Inductive bias | "Assumptions baked into the architecture" | 归纳偏好 (Inductive bias) | Prior about what the data looks like; CNNs assume translation invariance, RNNs assume recency. 关于数据外观的先验；CNN 假设平移不变性，RNN 假设邻近性。 |
| State-space model | "RNN with algebra behind it" | 状态空间模型 (State-space model) | Recurrence parameterized for parallel training via structured state-space matrices. 通过结构化状态空间矩阵参数化以实现并行训练的循环。 |
| Quadratic bottleneck | "Why context costs so much" | 二次瓶颈 (Quadratic bottleneck) | Attention memory = `O(N²)` in sequence length; Flash Attention hides the constants, not the scaling. 注意力内存 = 序列长度的 `O(N²)`；Flash Attention 隐藏了常数，而非缩放。 |

## Más Leer más Leer más

- [Vaswani et al. (2017). Attention Is All You Need](https://arxiv.org/abs/1706.03762) el artículo que mató la recurrencia en la PNL convencional.
  Vaswani 等人(2017)  终结了主流NLP 中循环的论文──

- [Bahdanau, Cho, Bengio (2014). Neural MT by Jointly Learning to Align and Translate](https://arxiv.org/abs/1409.0473) donde nació la atención, enlazado en un RNN.
  Bahdanau, Cho, Bengio ((2014)  Atención donde nació,

- [Hochreiter, Schmidhuber (1997). Long Short-Term Memory](https://www.bioinf.jku.at/publications/older/2604.pdf) el papel original de LSTM, por escrito.
  Hochreiter, Schmidhuber(1997)  原始 LSTM 论文,留作记录。

- [Gu, Dao (2023). Mamba: Linear-Time Sequence Modeling with Selective State Spaces](https://arxiv.org/abs/2312.00752) respuesta recurrente moderna a los transformadores.
  Gu, Dao(2023)  Transformer's moderno ciclo sustitutivo方案──

> **【拓展："Attention Is All You Need" 的历史影响】**Vaswani  et al. en su artículo de 2017 no solo resolvió el problema de la integración de RNN, sino que también provocó una gran revolución. Desde BERT(2018) hasta GPT-4(2023), desde ViT(2020) hasta AlphaFold 2(2021), la estructura transformadora se ha convertido en un módulo básico de la IA moderna.
