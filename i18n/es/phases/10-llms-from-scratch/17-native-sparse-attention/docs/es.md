# Native Sparse Attention (DepSeek NSA)

> En los tokens 64k, la atención consume 70-80% de la latencia de decodificación. Cada laboratorio abierto tiene un plan para arreglarlo. La NSA de DeepSeek (el mejor documento de ACL 2025) es la que se quedó pegada: tres ramas de atención paralelas  tokens de grano grueso comprimidos, tokens de grano fino retenidos selectivamente, y ventanas deslizantes para el contexto local  combinadas a través de una puerta de entrada aprendida. Es alineado con hardware (friendly-kernel), nativamente entrenable (trabaja en pre-entrenamiento, no se enciende en la inferencia), y en 64k decodifica se ejecuta más rápido que FlashAttention mientras que coincide o supera la calidad de atención completa. Esta lección construye las tres ramas de extremo a extremo y muestra por qué la escasez es diferenciable de extremo a extremo.

> **【中文解读】**64K token 时注意力消耗 70-80%解码延迟──DeepSeek NSA(ACL 2025 最佳论文) con tres artículos y seguimiento Atención分支解决: comprimir token grueso de gramación、 seleccionar para conservar token de granosidad、滑窗局部上下文, pasando por un módulo de control de la puerta, mediante un módulo de aprendizaje, mediante un módulo de hardware amigable、 un entrenamiento previo, más rápido que FlashAttention.

> **【拓展：稀疏注意力→长上下文】**长上下文(64K-128K token) es la capacidad central del gran modelo de 2025-2026 años;;NSA、MHA、GQA son todos los programas de reducción de la complejidad de cálculo de la atención;;DeepSeek es una innovación en la rareza de la terminal de la terminal de la micro, puede ser utilizado directamente en la fase de entrenamiento previo;;

> ¿ Qué es esto ?**【前置】**学本节前请先掌握:Fase 10·16(差分注意力);FlashAttention 概念;softmax 门控机制──本节是注意力优化进阶──
> ¿ Qué es esto ?**【类比】**NSA = 看长文档的三种策略同时进行:**压缩分支**= 看目录摘要(粗粒度);(2) **选择分支**= 重点看自己感兴趣的章节(细粒度);(3) **滑动窗口**= 当前页前后 5 页仔细看(局部上下文) ――门控(gate) = decidir qué estrategia debe utilizarse en cada posición, aprender automáticamente el mejor conjunto。

**Type:** Build
**Languages:** Python (stdlib)
**Prerequisites:** Phase 7 · 12 (KV cache, flash-attention), Phase 7 · 15 (attention variants), Phase 10 · 16 (differential attention)
**Time:** ~60 minutes

## Objetivos de aprendizaje

- Cuéntanos las tres ramas de atención de la NSA y lo que captura cada una.
  Explicando las tres ramas de atención de la NSA y su captura de información
- Explica por qué la NSA es "naturalmente entrenable" cuando los métodos previos de atención escasa eran sólo inferenciales.
  Explica por qué la NSA es "prácticamente entrenada", mientras que los métodos anteriores de atención rara sólo pueden ser utilizados para la hipótesis.
- Computa los ahorros de atención de la NSA frente a la atención completa en el contexto de 64k como función del tamaño del bloque de compresión y la selección de top-k.
  计算在 64K 上下文中 NSA相对全注意的计算节省量(como función de compresión de un bloque de tamaño y selección de la parte superior de k)
- Implemente la combinación de tres ramas en stdlib Python en una secuencia sintética corta y verifique el comportamiento de los pesos de gating.
  Usando Python en secuencias de sintetizado cortas, realizar tres componentes, verificar el control de peso

## El problema es la introducción del problema

Atención total en la longitud de secuencia N costos `O(N^2)`tiempo y `O(N)`El caché KV por capa. En los tokens 64k, los números de ancho de banda de computación y memoria son catastróficos. Estimado teóricamente desde el documento de la NSA: la atención representa el 70-80% de la latencia total de decodificación en 64k. Todo a la baja  TTFT, tokens/sec, costo por millón de tokens  está dominado por el costo de la atención.

> 序列长度 N                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        `O(N^2)`时间和每层 `O(N)`KV 缓存── en los tokens de 64k, el cálculo y el número de tokens de 64k 显存带宽 时的数字是灾难性的──NSA 论文的测量理论估计:64k 时的注意力占据总解码延迟的70-80%──所有下游指标TTFT、tokens/sec、每百万 token 成本都由注意力成本主导──

La escasa atención es la respuesta obvia. Los intentos anteriores se dividen en dos cubo. La esparcia de patrones fijos (ventana deslizante, paso a paso, bloque local) arroja la información y falla en las tareas de recuerdo a largo alcance. La esparcia de tiempo de inferencia (KV cache pruning, H2O, StreamingLLM) se aplica a un modelo pre-entrenado en atención densa y recupera solo una fracción del potencial aceleramiento porque nunca se le pidió al modelo que enrutara la información a través del patrón esparcido.

> 稀疏注意力 (en inglés: Rarura de atención) es una respuesta evidente. Se ha dividido en dos tipos los intentos anteriores.

Native Sparse Attention (Yuan et al., DeepSeek + PKU + UW, ACL 2025 mejor documento, arXiv:2502.11089) hace ambas cosas: un patrón de esparcia que el modelo aprende durante el pre-entrenamiento, implementado como un algoritmo alineado con el núcleo que realmente entrega los ahorros de computación a la inferencia.

> Originarios de la teoría de la teoría de la teoría de la teoría de la teoría de la teoría de la teoría de la teoría de la teoría de la teoría de la teoría de la teoría de la teoría de la teoría de la teoría de la teoría de la teoría de la teoría de la teoría de la teoría de la teoría de la teoría de la teoría de la teoría de la teoría de la teoría de la teoría de la teoría de la teoría de la teoría de la teoría de la teoría de la teoría de la teoría de la teoría de la teoría de la teoría de la teoría de la teoría de la teoría de la teoría de la teoría de la teoría de la teoría de la teoría de la teoría de la teoría de la teoría de la teoría de la teoría de la teoría de la teoría de la teoría de la teoría de la teoría de la teoría de la teoría de la teoría de la teoría de la teoría de la teoría de la teoría de la teoría de la teoría de la teoría de la teoría de la teoría de la teoría de la teoría de la teoría de la teoría de la teoría de la teoría de la teoría de la teoría de la teoría de la teoría de la teoría de la teoría de la teoría de la teoría de la teoría de la teoría de la teoría de la teoría de la teoría de la teoría de la teoría de la teoría de la teoría de la teoría de la teoría de la teoría de la teoría de la teoría de la teoría de la teoría de la teoría de la teoría de la teoría de la teoría de la teoría de la teoría de los cuentas de la teoría de la teoría de la teoría de los cuentas de la teoría de los cuentas de la teoría de los cuentas de los cuentas de los cuentas de cuentas de cuentas de cuentas de cuentas de cuentas de cuentas de cuentas de cuentas de cuentas de cuentas de cuentas de cuentas de cuentas de cuentas de cuentas de cuentas de cuentas de cuentas de cuentas de cuentas de cuentas de cuentas de cuentas de cuentas de cuentas de cuentas de cuentas de cuentas de cuentas de cuentas de cuentas de cuentas de cuentas de cuentas de cuentas de cuentas de cuentas de cuentas de cuentas de cuentas de cuentas de cuentas de cuentas de cuentas de cuentas de cuentas de cuentas de cuentas de cuentas de cuentas de cuentas de cuentas de cuentas de

## El concepto central.

> **【中文解读】**La atención es una forma de hacer que el modelo se ponga en contacto con la información que se le ofrece.

> **【拓展：长上下文的稀疏注意力方案】**稀疏注意力工程实现包括:滑动窗口(Mistral's 32K 窗口) + 全局 token([CLS]) + 选择性关注。Google's Ring Attention 和 Block-Sparse Attention 将上下文扩展到百万代币──DeepSeek's NSA(Native Sparse Attention) 在训练时直接学习稀疏模式──


### Tres ramas paralelas

Para cada consulta, la NSA ejecuta la atención tres veces, contra tres vistas diferentes de la caché KV:

1. **Compressed branch.**Los tokens se agrupan en bloques de tamaño `l`Cada bloque se comprime en un solo token de resumen a través de un pequeño MLP aprendido.

2. **Selected branch.**Usando las puntuaciones de atención de la rama comprimida, se identifican los bloques top-k más relevantes para la consulta actual. Se leen los tokens de granos finos (no comprimidos) de esos bloques y la consulta se atiende sobre todos ellos. Piense en la atención de la rama comprimida como la señal de enrutamiento para la selección.

3. **Sliding-window branch.**La consulta se ocupa de los más recientes `W`Los símbolos de la estructura de la base de datos (normalmente 512) para el contexto local. Esta rama captura los patrones de corto alcance de estructura pesada (sintaxis, coreferencia local) que los otros dos podrían perder.

Las tres salidas de la rama se combinan a través de una puerta de posición aprendida:

```
out = g_cmp * out_cmp + g_sel * out_sel + g_win * out_win
```

`g_cmp, g_sel, g_win`No tienen que sumar a 1  pueden pesar ramas de forma independiente.

### Por qué esto es "naturalmente entrenable"

El paso de selección (bloques de la parte superior de la K) es discreto. Las operaciones discretas rompen el flujo de gradiente.

La NSA evita esto: la atención de ramas comprimidas es una atención de granos gruesos diferenciables en toda la secuencia. La operación top-k sólo reutiliza las puntuaciones de atención de la rama comprimida para elegir qué bloques de granos finos cargar. Los gradientes fluyen a través de las puntuaciones de ramas comprimidas (que influyen tanto en la salida comprimida como en la lógica de selección), y la contribución de los bloques seleccionados a la salida final también es diferenciable. El no diferenciable `top_k`La operación es una no-op en el gráfico computacional de adelante  sólo controla qué bloques se cargan de la memoria.

Esta es la razón por la cual la NSA puede ser utilizada en el pre-entrenamiento de extremo a extremo. El modelo aprende a dirigir la información a través de las tres ramas conjuntamente, produciendo un patrón escaso que en inferencia realmente entrega el acelerado prometido.

### Núcleo alineado con el hardware

El kernel de la NSA está diseñado para las jerarquías de memoria GPU modernas. El kernel carga consultas por grupos GQA (bucle externo), recoge los bloques KV escasos correspondientes por grupo (bucle interno) y dirige la atención a SRAM. Debido a que cada grupo de consulta ve los mismos bloques seleccionados (la selección es por grupo de consulta, no por cabeza de consulta), las cargas KV se amortizan en todo el grupo.

El documento informa que los kernels de Triton se ejecutan 9 veces más rápido que FlashAttention en decodificadores 64k, con la relación de aceleración creciendo con la longitud de la secuencia.

### El presupuesto de cálculo

- ¿ Qué ?`N`ser longitud de secuencia, `l`el tamaño del bloque de compresión, `k`el recuento de selección de la parte superior de k, `w`la ventana deslizante, `b`el tamaño de bloque seleccionado (normalmente es igual `l`¿Qué es lo que se hace?

- Ramo comprimido: `O(N/l)`llaves por consulta, así que `O(N * N / l)`- ¿Qué?
- Se seleccionó la rama: `O(k * b)`llaves por consulta, así que `O(N * k * b)`¿ Qué ?
- Ramo deslizante: `O(w)`llaves por consulta, así que `O(N * w)`¿ Qué ?

Total: `O(N * (N/l + k*b + w))`¿ Qué ?

Con `N = 64k, l = 64, k = 16, b = 64, w = 512`: el coste por solicitud es `1000 + 1024 + 512 = 2536 keys`Toda la atención es`64000 keys`. 25 veces reducción de cálculo.

Con `N = 128k, l = 64, k = 16, b = 64, w = 512`: el coste por solicitud es `2000 + 1024 + 512 = 3536 keys`Toda la atención es`128000 keys`El beneficio aumenta con la longitud de la secuencia, que es todo el punto.

### ¿Cómo se compara

| Method | Differentiable | Real inference speedup | Long-range recall |
|--------|---------------|----------------------|-------------------|
| Sliding window only | yes | yes | fails |
| Strided / block-sparse | yes | yes | partial |
| KV pruning (H2O, StreamingLLM) | N/A (inference-time) | yes | partial |
| MoBA (Moonshot) | partial | yes | good |
| NSA | yes (natively) | yes (9x at 64k) | matches full attention |

MoBA (Moonshot, arXiv:2502.13189) fue publicado simultáneamente y adopta un enfoque similar de tres es mejor que uno, aplicando el principio de MoE a los bloques de atención. NSA y MoBA son las dos arquitecturas que se conocen para la pre-entrenamiento de contexto largo de 2026.


> **【拓展：稀疏注意力在长上下文中的应用】**密集注意力 O(n^2) 计算量使128K 上下文的预填充阶段需要约30秒──稀疏方法(如 NSA、Ring Attention) 将其降至可接受范围──Gemini 1.5 Pro 的1M代币 上下文依赖于稀疏注意力──


## Construye y realiza.
```figure
sliding-window-attention
```

## Construye el mismo

`code/main.py`Implementa las tres ramas en una secuencia sintética corta y muestra:

- La MLP de compresión (se utiliza una línea de base simple de la media para la claridad pedagógica; la NSA real utiliza una MLP aprendida).
- La selección de bloques de la parte superior de k impulsada por puntajes de ramas comprimidas.
- La atención de la ventana deslizante en el último `w`- ¿Qué es eso?
- La combinación cerrada.
- Una impresión de recuento computacional comparando la atención completa.

### Paso 1: comprimir los tokens en bloques

```python
def compress(K, l):
    n = len(K)
    n_blocks = (n + l - 1) // l
    out = []
    for b in range(n_blocks):
        start, end = b * l, min((b + 1) * l, n)
        block = K[start:end]
        summary = [sum(row[d] for row in block) / len(block) for d in range(len(K[0]))]
        out.append(summary)
    return out
```

### Paso 2: Atención a las ramas comprimidas

ejecuta la atención de la consulta en la máxima medida contra las teclas comprimidas.

### Paso 3: Selección de bloque de la parte superior

Seleccione los índices de la `k`Los bloques comprimidos con más puntuaciones cargar los tokens originales sin comprimir de esos bloques y prestar atención a ellos.

### Paso 4: Atención a las ventanas deslizantes

Toma el último .`w`las fichas y ejecutar la atención estándar contra ellos.

### Paso 5: puerta + combinación

Una pequeña MLP en la consulta produce tres pesos de puerta. La salida final es una suma ponderada de las tres salidas de rama.

### Paso 6: Cuenta de cálculo

Imprima el número de teclas consultadas por consulta para cada rama y el total.`N`En una sintética de 1024 tokens con`l = 32, k = 4, w = 128`, la NSA ve .`32 + 128 + 128 = 288`Las claves por consulta en comparación con 1024 para la atención completa  3,5 veces menos.

## Usalo con el marco de ejecución

La NSA está enviando en DeepSeek su propia línea de pre-entrenamiento de largo contexto.

- **DeepSeek internal**: pesos nativos, publicados utilizan NSA o su sucesor DSA (Deepseek Sparse Attention).
- **vLLM**: soporte experimental de la NSA en desarrollo para pesos de DeepSeek-V3.x.
- **SGLang**: Se publican los índices de referencia de la NSA; el camino de producción sigue el VLLM.
- **llama.cpp / CPU**: no se admite; el gasto general de la descomposición del núcleo no vale la pena en el rendimiento de la CPU.

Cuándo contactar a la NSA:

- Las actividades de formación previa o de formación continua dirigidas a más de 64 000 personas con un presupuesto de cálculo serio.
- La inferencia de los propios puestos de control de DeepSeek en el contexto largo.

Cuando no:

- No puedes adaptar la NSA sin entrenamiento continuo.
- El gasto general de tres ramas domina los ahorros.
- Chat interactivo de batch 1. Beneficios de decodificación sensibles a la latencia, pero sólo en contextos largos.

## Envíe el producto .

Esta lección produce`outputs/skill-nsa-integrator.md`. Dado una especificación de ejecución previa a la capacitación en largo contexto, produce un plan de integración de la NSA: tamaño de bloque de compresión, top-k, ventana deslizante, ancho de puerta MLP, elección del núcleo y las evaluaciones específicas en largo contexto que justifican el cambio de arquitectura.

> 本课产 出  `outputs/skill-nsa-integrator.md` La aplicación de las normas de entrenamiento previo de la NSA, que generó un plan de integración: compresión de bloques de tamaño, de arriba a abajo, ventanas de deslizamiento, control de puertas, MLP de amplitud, selección de núcleos y evaluación de la estructura de prueba de que sea más razonable.

## Los ejercicios.

1. - ¿ Qué ?`code/main.py`En un 1024-token sintético.`(l, k, w)`Identificar el predefinido que consigue el menor número de claves por consulta manteniendo un recuento del 95% frente a la atención total en una prueba de aguja en haystack.
   En 1024-token 合成数据上运行 `code/main.py` En tres pre-setting en la exploración `(l, k, w)`Y imprimir la cantidad de cálculo. Encontrar en el test de haystack para mantener la atención total en el 95% de la tasa de retorno al tiempo que lograr el mínimo de la previsión de cada consulta clave.

2. Reemplazar el compresor de la base media con un pequeño MLP aprendido (2 capas, oculto 32). Entrenarlo en una tarea sintética donde la señal es el promedio de un bloque. Medir la brecha de perplejidad con la línea de base de la base media en los datos retenidos.
   China Translation: Usando un pequeño aprendizaje MLP ((2 niveles, escondido 32) sustituir el compresor de la media de valor de la base de la base de la base de la base de la base de la base de la base de la base de la base de la base de la base de la base de la base de la base de la base de la base de la base de la media de valor de la base de la medida en la reserva de datos.

3. Implemente la puerta MLP. Toma la consulta como entrada y saca tres escalares. Muestre que la puerta se comporta sensatamente: ponderación casi uniforme en consultas aleatorias, peso pesado en la rama seleccionada cuando la consulta golpea un bloque de fondo.
   China Translation: implementar el control de la puerta MLP。 se utiliza para la consulta de tres dimensiones para la entrada y salida。 mostrar el control de la puerta comportamiento razonable:

4. Compute el presupuesto de memoria de caché KV para un modelo 70B habilitado por la NSA en un contexto de 128k. Las cabezas de KV son 8, la cabeza es de 128, BF16. Compara con la atención completa y con MLA (fase 10 · 14 mostró los números de MLA).
   計算 NSA 启用70B 模型在 128K 上下文 下 KV 缓存内存预算──KV 头 8 个,头维度 128,BF16──与全注意力和 MLA比较──找到 NSA 细粒度分支 KV 缓存等于全注意序列长度──

5. Lea la sección 4 del documento de la NSA (arXiv:2502.11089) y explique en tres frases por qué los puntajes de atención de la rama comprimida se reutilizan para la selección de top-k en lugar de calcular un puntaje de enrutamiento separado.
   China 翻译:阅读 NSA 论文第4节, utiliza tres frases para explicar por qué el porcentaje de atención de la división de compresión se repite en la selección superior y no en el cálculo del porcentaje de ruta individual.

## Términos clave .

| Term | What people say | What it actually means | 中文释义 |
|------|----------------|------------------------|---------|
| Compressed branch | "Coarse view" | Attention over block-averaged keys that provides global context in O(N/l) keys per query | 压缩分支，块平均键上的注意力 |
| Selected branch | "Top-k blocks" | Fine-grained attention over the `k` blocks with highest compressed-branch scores | 选择分支，对 top-k 块做细粒度注意力 |
| Sliding window | "Local context" | Attention over the last `W` tokens for short-range patterns | 滑动窗口，最近 W 个 token 的局部上下文 |
| Native trainability | "Pre-train with the sparsity on" | The sparsity pattern is learned during pre-training, not bolted on at inference | 原生可训练，预训练时就使用稀疏模式 |
| Compression block size l | "Group size for coarse view" | How many tokens get merged into one summary; 32-64 typical | 压缩块大小，每组合并多少 token |
| Top-k | "Blocks to keep" | Number of compressed blocks whose uncompressed tokens get read; 16 typical | Top-k，保留的压缩块数量 |
| Sliding window W | "Local attention radius" | Typically 512; shorter hurts local coherence, longer wastes compute | 滑动窗口大小，典型值 512 |
| Branch gate | "How to mix the three" | Per-position MLP output that weights the three branches' contributions | 分支门控，MLP 输出加权三分支贡献 |
| Hardware alignment | "Kernel-friendly sparsity" | Sparse pattern chosen so that the actual GPU kernel achieves the theoretical speedup | 硬件对齐，稀疏模式适配 GPU 核函数 |
| DSA | "NSA's successor" | Deepseek Sparse Attention, the architecture that followed NSA in DeepSeek's lineage | DSA，DeepSeek 稀疏注意力，NSA 的后继架构 |

## Más Leer más Leer más

- [Yuan et al. — Native Sparse Attention: Hardware-Aligned and Natively Trainable Sparse Attention (arXiv:2502.11089, ACL 2025 Best Paper)](https://arxiv.org/abs/2502.11089) el papel
- [DeepSeek-V3 Technical Report (arXiv:2412.19437)](https://arxiv.org/abs/2412.19437) la familia de arquitecturas de los objetivos de la NSA
- [Moonshot AI — MoBA: Mixture of Block Attention for Long-Context LLMs (arXiv:2502.13189)](https://arxiv.org/abs/2502.13189) trabajo simultáneo, atención al estilo de la MOE sobre bloques
- [Beltagy et al. — Longformer: The Long-Document Transformer (arXiv:2004.05150)](https://arxiv.org/abs/2004.05150) Origen de las ventanas deslizantes
- [Xiao et al. — StreamingLLM: Efficient Streaming Language Models with Attention Sinks (arXiv:2309.17453)](https://arxiv.org/abs/2309.17453) La línea de base de la escasez de tiempo de inferencia
- [Dao et al. — FlashAttention-2 (arXiv:2307.08691)](https://arxiv.org/abs/2307.08691) la línea de base de atención completa de los núcleos de la NSA golpeó en 64k
