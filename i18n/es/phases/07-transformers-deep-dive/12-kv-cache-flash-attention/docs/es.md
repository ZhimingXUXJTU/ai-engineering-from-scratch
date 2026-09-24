# KV Cache, atención flash y optimización de inferencia.

> El entrenamiento es paralelo y ligado a FLOP. La inferencia es seria y ligada a la memoria. Diferentes cuellos de botella, diferentes trucos.

> **【中文解读】**KV Cache 缓存已计算的关键/值 避免重复计算,是LLM 推理加速的核心──Flash Attention 优化显存访问模式,减少显存使用──

**Type:** Hands-on | **类型:** 动手
**Language:**¿ Qué pasa ?**语言:**Python
**Prerequisites:** Phase 7 · 02 (Self-Attention), Phase 7 · 05 (Full Transformer), Phase 7 · 07 (GPT) | **前置知识:** Phase 7 · 02 (Self-Attention), Phase 7 · 05 (Full Transformer), Phase 7 · 07 (GPT)
**Time:** ~75 minutes | **时间:** ~75 分钟

## El problema es la introducción del problema

Un descifrador autoregresor ingenuo sí .`O(N²)`trabajo para generar `N`Tokens: en cada paso recalcula la atención sobre el prefijo completo. Para una respuesta de tokens 4K que es 16M operaciones de atención, la mayoría de ellos redundantes. Cada estado oculto de un token prefijo es determinista una vez calculado.

> Un simple generador de código de auto-regreso`N`个 token 需要 `O(N²)`Para la respuesta de los tokens 4K, es una operación de 16M veces de atención, la mayor parte de las cuales son redundantes. Cada estado oculto de los tokens anteriores una vez calculado es de certeza.

Además, la atención misma mueve muchos datos. La atención estándar materializa una matriz de puntaje N×N, salida de N×d softmax, salida final N×d  demasiadas lecturas y escrituras a HBM. Para N≥2K, la atención se vuelve limitada a la memoria antes de que se convierta en FLOP-bound.

> Además, la atención en sí misma debe mover una gran cantidad de datos. La atención estándar generará N×N de la matriz de la cantidad de datos. La producción de N×d de la cantidad de datos de la HBM es demasiado grande. Cuando N≥2K, la atención se convierte en una botella de memoria antes de convertirse en una botella de FLOP. La tasa de utilización de la memoria de la GPU moderna de la atención clásica es de 4 a 10 veces mayor.

Dos optimizaciones, ambas de Dao et al., empujaron la inferencia fronteriza de "lento" a "rápido":

> 两个优化 (todos provienen de Dao 等人) se desarrollará en la vanguardia de la "lento" a la "quiz":

1. **KV cache.**Almacenar los vectores K y V de cada token prefijo. la atención de cada nuevo token es una consulta contra las claves almacenadas en caché.`O(N²)`¿ Qué ?`O(N)`por cada paso de generación.
   En inglés:**KV 缓存。**存储每前代币的 K 和 V 向量──每新代币的注意是对缓存键的一个查询──推理从每步 `O(N²)`降低到 `O(N)`¿Qué es eso?
2. **Flash Attention.**El cálculo de la atención se realiza con una tela de tela para que la matriz completa de N×N nunca alcance el HBM. Todo el softmax + matmul ocurre en SRAM. 24× velocidad del reloj de pared en A100; 510× en H100 con FP8.
   En inglés:**Flash Attention。**Para calcular el cálculo de los bloques, hacer que la N×N 矩阵 completa nunca se escriba en HBM──todos los softmax + 矩阵乘法都在SRAM完成──A100 上 2-4 倍加速;H100 上 FP8 可达 5-10 倍──

Para 2026 ambos son universales. Cada pila de inferencias de producción (vLLM, TensorRT-LLM, SGLang, llama.cpp) los asume.

> Para el año 2026, ambos han sido populares. Cada producción de las ideas de la tecnología de la tecnología de la tecnología de la tecnología de la tecnología de la tecnología de la tecnología de la tecnología de la tecnología de la tecnología de la tecnología de la tecnología de la tecnología de la tecnología de la tecnología de la tecnología de la tecnología de la tecnología de la tecnología de la tecnología de la tecnología de la tecnología de la tecnología de la tecnología de la tecnología de la tecnología de la tecnología de la tecnología de la tecnología de la tecnología de la tecnología de la tecnología de la tecnología de la tecnología de la tecnología de la tecnología de la tecnología de la tecnología de la tecnología de la tecnología de la tecnología de la tecnología de la tecnología de la tecnología de la tecnología de la tecnología de la tecnología de la tecnología de la tecnología de la tecnología de la tecnología de la tecnología de la tecnología de la tecnología de la tecnología de la tecnología de la tecnología de la tecnología de la tecnología de la tecnología de la tecnología de la tecnología de la tecnología de la tecnología de la tecnología de la tecnología de la tecnología de la tecnología de la tecnología de la tecnología de la tecnología de la tecnología de la tecnología de la tecnología de la tecnología de la tecnología de la tecnología de la tecnología de la tecnología de la tecnología de la tecnología de la tecnología de la tecnología de la tecnología de la tecnología de la tecnología de la tecnología de la tecnología de la tecnología de la tecnología de la tecnología de la tecnología de la tecnología de la tecnología de la tecnología de la tecnología de la tecnología de la tecnología de la tecnología de la tecnología de la tecnología de la tecnología de la tecnología de la tecnología de la tecnología de la tecnología de la tecnología de la tecnología de la tecnología de la tecnología de la tecnología de la tecnología de la tecnología de la tecnología de la tecnología de la tecnología de la tecnología de la tecnología de la tecnología de la tecnología de la tecnología de la tecnología de la tecnología de la tecnología de la tecnología de la tecnología de la tecnología de la tecnología de la tecnología de la tecnología de la tecnología de la tecnología de la tecnología de la tecnología de la tecnología de la tecnología de la tecnología de la tecnología de la tecnología de la tecnología de la tecnología de la tecnología de la tecnología de la tecnología de la tecnología de la tecnología de la tecnología de la tecnología de la tecnología de la tecnología de la tecnología de la tecnología de la tecnología de la tecnología de la tecnología de la tecnología de la tecnología de la tecnología de la tecnología de la tecnología de la tecnología de la tecnología de la tecnología de la tecnología de la tecnología

> **【中文解读】**推理优化两大核心技术:KV Cache 存储已计算的钥匙/值向量,避免重复计算,将每步推理从O(N^2) 降至O(N);Flash Attention 通过分块计算避免N×N矩阵写入HBM,完成所有计算在SRAM,速度提升2-10倍――

## El concepto central.

![KV cache growth and Flash Attention tiling](../assets/kv-cache-flash-attn.svg)

### Matemáticas de caché de KV

Por capa de decodificación, por token, por cabeza:

> Cada nivel de código, cada token, cada cabeza:

```
bytes_per_token_per_layer = 2 * d_head * dtype_size
                          ^
                          K and V
```

Para un modelo 7B con 32 capas, 32 cabezas, d_head=128, fp16:

> 对于7B 模型(32 层、32 头、d_head=128、fp16):

```
per token per layer = 2 * 128 * 2 = 512 bytes
per token (32 layers) = 16 KB
per 32K context = 512 MB
```

> **【拓展：GQA 对 KV 缓存的影响】**GQA(Grouped-Query Attention) reducirá el KV 头从n_heads 减少到n_kv_heads,直接等比例缩小 KV 缓存.

Para Llama 3 70B (80 capas, d_head=128, GQA con 8 capas de KV):

> Para Llama 3 70B ((80 层、d_head=128、GQA 8 个 KV 头):

```
per token per layer = 2 * 8 * 128 * 2 = 4096 bytes (4 KB)
per 32K context = 10.4 GB
```

Ese 10 GB es por lo que Llama 3 70B en 128K contexto necesita la mayoría de un 40 GB A100 sólo para KV caché en el tamaño de lote 1.

> Este 10 GB es por qué Llama 3 70B en 128K arriba abajo sólo KV 缓存(tamaño de lote 1) necesita la mayor parte de 40 GB A100 显存――

**GQA is the KV-cache win.**MHA con 64 cabezas sería de 32 GB. MLA comprime aún más.

> **GQA 是 KV 缓存的胜利。**64 cabezas de MHA  necesitan 32 GB―MLA  comprimirse más adelante―
Arraste las dimensiones y observa el tamaño de la caché. Empuje la longitud de la secuencia o lote hacia arriba y vea qué tan rápido se desvanece más allá de una sola GPU:

```figure
kv-cache-sizer
```

### La atención de flash  el truco de la balsa

Atención estándar:

> 标准注意力:

```
S = Q @ K^T          (HBM read, N×N, HBM write)
P = softmax(S)       (HBM read, HBM write)
O = P @ V            (HBM read, HBM write)
```

Tres viajes de ida y vuelta de HBM. En H100, el ancho de banda de HBM es de 3 TB/s; SRAM es de 30 TB/s. Cada viaje de HBM es un factor de 10 de desaceleración frente a mantener todo en el chip.

> Tres veces HBM 往返── en H100, HBM 带宽是3TB/s;SRAM es 30TB/s── en cada HBM 访问比在片保持所有数据慢10倍──

Atención instantánea:

```
for each block of Q (tile size ~128 × 128):
    load Q_tile into SRAM
    for each block of K, V:
        load K_tile, V_tile into SRAM
        compute S_tile = Q_tile @ K_tile^T     (SRAM)
        running softmax aggregation             (SRAM)
        accumulate into O_tile                  (SRAM)
    write O_tile to HBM
```

Un viaje de HBM por baldosas.`O(N²)`¿ Qué ?`O(N)`. El pase hacia atrás recalcula algunos valores del pase hacia adelante en lugar de almacenarlos  otra ganancia de memoria.

> Cada mosaico una vez HBM                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                       `O(N²)`降到 `O(N)` Contrastre propagando de la anterior hacia la propagando recalcula ciertos valores en lugar de almacenarlos otro beneficio de la memoria

**Numerical trick.**El funcionamiento de softmax se mantiene `(max, sum)`La atención flash calcula la salida idéntica a la atención estándar (modulo fp16 no asociativa).

> **数值技巧。**运行时 softmax 跨 维护 `(max, sum)`Para asegurar que la integración final es precisa. No es similar.

> **【中文解读】**Las técnicas centrales de atención flash: calcular la atención en bloques de cálculo, realizar la softa máxima y la matriz multiplicada en la GPU de SRAM rápido, evitar escribir la matriz media de N×N en HBM lenta.

> **【拓展：vLLM 的 PagedAttention】**PagedAttention(vLLM) organizará KV 缓存为固定大小的"页", similar a los sistemas operativos de memoria virtual. Esto eliminó el problema de los fragmentos de memoria, permitiendo que varias peticiones de desarrollo puedan ser compartidas de manera alta con GPU 显存──配合连续批处理(continuous batching),vLLM aumentará el volumen de datos de LLM 推理 2-4 veces, convirtiéndose en el marco de análisis más popular de 2024-2026.

**Version evolution:**

| Version | Year | Key change | Speedup on reference hardware |
|---------|------|-----------|-------------------------------|
| 版本 | 年份 | 关键变化 | 参考硬件上的加速 |
| Flash 1 | 2022 | Tiled SRAM kernel | 2× on A100 |
| Flash 2 | 2023 | Better parallelism, causal-first ordering | 3× on A100 |
| Flash 3 | 2024 | Hopper asynchrony, FP8 | 1.5–2× on H100 (~740 TFLOPs FP16) |
| Flash 4 | 2026 | Blackwell 5-stage pipeline, software exp2 | Inference-first (forward only initially) |

Flash 4 es solo avanzado al lanzamiento. El entrenamiento todavía utiliza Flash 3.

> Flash 4 发布时仅支持前向传播;; entrenamiento todavía utiliza Flash 3;; GQA y cambios de apoyo de Flash 4 esperan(2026年中)。

### Descodación especulativa  la otra latencia gana

El modelo barato propone N tokens. El modelo grande verifica todos los N en paralelo. Si la verificación acepta k tokens, pagó 1 pase adelante de modelo grande para k generaciones.

> 廉价模型提出N 个代币――大模型并行验证所有N 个―― Si la验证 acepta k 个代币, usted obtiene k 个生成――代码和散文的典型 k=3-5―― con un gran modelo de pre-propagación.

2026 incumplimientos:
- **EAGLE 2 / Medusa.**Tías de proyección integradas que comparten los estados ocultos del verificador. 23x aceleración sin pérdida de calidad.
  En inglés:**EAGLE 2 / Medusa。**集成草案头, compartido estado oculto del verificador ∼2-3 veces acelerado, sin pérdida de calidad ∼
- **Speculative decoding with draft model.**2×4 veces más rápido en el hardware de consumo.
  En inglés:**带草案模型的推测解码。**El consumo de hardware se acelera de 2 a 4 veces.
- **Lookahead decoding.**Iteración Jacobi, no se necesita un modelo de borrador. Nicho pero gratis.
  En inglés:**前瞻解码。**Jacobi 代;不需要草案模型──小众但免费──

### Participación continua

Inferencia clásica de lote: esperar a que termine la secuencia más lenta, luego iniciar un nuevo lote.

> 经典批量推理: esperar a que se complete el más lento de los procesos, y luego comenzar a realizar nuevos grupos.

Batchamiento continuo (en Orca, ahora en vLLM, TensorRT-LLM, SGLang): intercambiar nuevas solicitudes en el lote tan pronto como terminen las viejas.

> 连续批处理(首次在Orca中发布,现在在vLLM、TensorRT-LLM、SGLang 中): la antigua solicitud se completa inmediatamente después de la nueva solicitud cambiará en la serie.

### PagedAttention  KV caché como memoria virtual

La función principal de vLLM. El caché KV se asigna en bloques de 16 tokens; una tabla de página mapea las posiciones lógicas de los bloques físicos. Permite compartir KV a través de muestras paralelas (busca de haces, muestreo paralelo), prefijos de intercambio caliente para el caché rápido y memoria de desfragmentación. Mejora de rendimiento 4x sobre asignación contiguosa ingenua.

> La base de datos de la aplicación es el código de acceso de la página web de la empresa.

## Construye y realiza.
```figure
flash-attention-memory
```

## Construye el mismo

¿ Qué ?`code/main.py`Implementamos:

> 参见 `code/main.py`❖ Nosotros realizamos:

1. Un ingenuo .`O(N²)`decodificador incremental.
   Un simple y simple.`O(N²)`增量解码器── también se puede ver en el video.
2. ¿ Qué es esto ?`O(N)`Descriptor de caché KV.
   Un hombre de la familia de los niños.`O(N)`KV 缓存解码器──
3. Una softmax de tejas que simula el algoritmo de ejecución máxima de Flash Attention.
   Un modelo de Flash Attention 运行时最大值的分块软max──

### Paso 1: Caché de KV

```python
class KVCache:
    def __init__(self, n_layers, n_heads, d_head):
        self.K = [[[] for _ in range(n_heads)] for _ in range(n_layers)]
        self.V = [[[] for _ in range(n_heads)] for _ in range(n_layers)]

    def append(self, layer, head, k, v):
        self.K[layer][head].append(k)
        self.V[layer][head].append(v)

    def read(self, layer, head):
        return self.K[layer][head], self.V[layer][head]
```

Sencillo: sigue creciendo por token K, V vectores en por capa, por lista de cabeza.

> 简单: en la lista de cada uno de los niveles                                                                                                                                                                                                                                                         

### Paso 2: softmax de azulejos

```python
def tiled_softmax_dot(q, K, V, tile=4):
    """Flash-attention-style softmax(qK^T)V with running max/sum."""
    m = float("-inf")
    s = 0.0
    out = [0.0] * len(V[0])
    for start in range(0, len(K), tile):
        k_block = K[start:start + tile]
        v_block = V[start:start + tile]
        scores = [sum(qi * ki for qi, ki in zip(q, k)) for k in k_block]
        new_m = max(m, *scores)
        exp_old = math.exp(m - new_m) if m != float("-inf") else 0.0
        exp_new = [math.exp(sc - new_m) for sc in scores]
        s = s * exp_old + sum(exp_new)
        for j in range(len(out)):
            out[j] = out[j] * exp_old + sum(e * v[j] for e, v in zip(exp_new, v_block))
        m = new_m
    return [o / s for o in out]
```

Una salida idéntica a bit `softmax(qK) V`en un solo disparo, pero en cualquier momento el juego de trabajo es un `tile × d_head`Bloqueo, no el completo `N × d_head`¿ Qué ?

> Con una sola vez`softmax(qK) V`Primero y después de todo, todo es igual.`tile × d_head`块, y no completo `N × d_head`¿Qué es eso?

### Paso 3: Comparar la descifrado ingenuo vs caché en la generación de 100 tokens

Cuenta las operaciones de atención.`O(N²)`= 5050. En caché: `O(N)`El código imprime ambas cosas.

> 計算注意力操作次数──朴素:`O(N²)`= 5050──缓存:`O(N)`= 100¬代码会打印两者¬

## Usalo con el marco de ejecución

```python
# HuggingFace transformers auto-enables KV cache on decoder-only generate().
from transformers import AutoModelForCausalLM
model = AutoModelForCausalLM.from_pretrained(
    "meta-llama/Llama-3.2-3B",
    attn_implementation="flash_attention_2",  # use FA3 if Hopper
    torch_dtype="bfloat16",
)
# generate() uses KV cache automatically
```

Producción de VLLM:

> VLLM 生产部署:

```bash
pip install vllm
vllm serve meta-llama/Llama-3.1-70B-Instruct \
    --tensor-parallel-size 4 \
    --max-model-len 32768 \
    --enable-prefix-caching \
    --kv-cache-dtype fp8
```

El caché de prefijos en las solicitudes es un gran éxito para 2026  el mismo sistema de instrucciones, ejemplos de pocos disparos o documento de contexto largo reutiliza KV en las llamadas. Para las cargas de trabajo de agentes con instrucciones de herramientas repetidas, el caché de prefijos es rutinariamente 5x ganancia de rendimiento.

> 跨请求的前缓存是2026年的重大胜利相同系统提示、少样本示例或长上下文文档在调用间重复使用 KV── para el carga de trabajo de los representantes de las提示的重复工具, el pre缓存 generalmente trae un aumento de 5 veces de la potenciación──

## Envíe el producto .

¿ Qué ?`outputs/skill-inference-optimizer.md`La habilidad selecciona la implementación de la atención, la estrategia de caché KV, la cuantificación y la descifrado especulativo para una nueva implementación de inferencias.

> 参见 `outputs/skill-inference-optimizer.md` Esta habilidad se aplica a la nueva estrategia de evaluación de la situación de la población, la evaluación de la situación de la población y la evaluación de la situación de la población.

## Los ejercicios.

1. **Easy.**- ¿ Qué ?`code/main.py`- Confirmar que los descifradores ingenuos y almacenados en caché producen la misma salida; nota la diferencia de op-count.
   Traducción:运行`code/main.py` Confirmar que la simple y el caché de código producen la misma salida;
2. **Medium.**Implementar el caché de prefijos: dado un prompt P y varias completas, ejecuta un pase hacia adelante sobre P para llenar el caché KV, luego ramifica por completado.
   Traducción: implementar pre缓存:给定提示 P 和多个补充,对 P 运行一次前向传播填充 KV 缓存,然后每个补充分支――测量与每次重编码 P 相比的速度提升――
3. **Hard.**Implementar un juguete PagedAttention: KV cache en bloques fijos de 16 tokens con una lista libre. Cuando una secuencia termine, devuelva sus bloques a la piscina. Simula 1.000 terminaciones de chat con diferentes longitudes. Compara fragmentación de memoria con asignación contiguosa.
   China: 实现玩具版 PagedAttention: KV 缓存使用固定 16 token 块加空列表──序列完成时归归块──模拟 1,000 个变长聊天补全──比较连续分配的内存碎片化差异──

## Términos clave .

| Term | What people say | What it actually means |
|------|-----------------|-----------------------|
| 术语 | 通俗说法 | 实际含义 |
| KV cache | "The trick that makes decoding fast" | Stored K and V from every prefix token; new queries attend to them instead of recomputing. |
| KV 缓存 | "让解码变快的技巧" | 存储每个前缀 token 的 K 和 V；新查询对它们做注意力而非重新计算。 |
| HBM | "GPU main memory" | High Bandwidth Memory; 80 GB on H100, 192 GB on B200. ~3 TB/s bandwidth. |
| HBM | "GPU 主内存" | 高带宽内存；H100 上 80 GB，B200 上 192 GB。约 3 TB/s 带宽。 |
| SRAM | "On-chip memory" | Per-SM fast memory, ~256 KB per SM on H100. ~30 TB/s bandwidth. |
| SRAM | "片上内存" | 每 SM 的快速内存，H100 上每 SM 约 256 KB。约 30 TB/s 带宽。 |
| Flash Attention | "Tiled attention kernel" | Computes attention without materializing N×N in HBM. |
| Flash Attention | "分块注意力内核" | 不在 HBM 中生成 N×N 矩阵即完成注意力计算。 |
| Continuous batching | "No-wait batching" | Swap finished sequences out, new ones in, without draining the batch. |
| 连续批处理 | "无等待批处理" | 完成的序列换出，新的换入，无需排空批次。 |
| PagedAttention | "vLLM's headline" | KV cache allocated in fixed blocks with a page table; eliminates fragmentation. |
| PagedAttention | "vLLM 的核心特性" | KV 缓存以固定块分配加页表；消除碎片化。 |
| Prefix caching | "Reuse long prompts" | Cache KV for a shared prefix across requests; major cost cut for agents. |
| 前缀缓存 | "复用长提示" | 跨请求缓存共享前缀的 KV；代理场景大幅降低成本。 |
| Speculative decoding | "Draft + verify" | Cheap draft model proposes tokens; big model verifies k in one pass. |
| 推测解码 | "草案 + 验证" | 廉价草案模型提出 token；大模型一次验证 k 个。 |

## Más Leer más Leer más

- [Dao et al. (2022). FlashAttention: Fast and Memory-Efficient Exact Attention with IO-Awareness](https://arxiv.org/abs/2205.14135) Flash 1.
  En inglés: Flash Attention 1
- [Dao (2023). FlashAttention-2: Faster Attention with Better Parallelism and Work Partitioning](https://arxiv.org/abs/2307.08691) Flash 2.
  En el caso de los niños, el problema es que no hay nada que hacer.
- [Shah et al. (2024). FlashAttention-3: Fast and Accurate Attention with Asynchrony and Low-precision](https://arxiv.org/abs/2407.08608) Flash 3.
  En el caso de los niños, el problema es que no hay nada que hacer.
- [FlashAttention-4 release notes (Dao-AILab, 2026)](https://github.com/Dao-AILab/flash-attention) Blackwell 5 etapas de tubería y el truco de software-exp2; lea el repo README para las advertencias de lanzamiento sólo hacia adelante que menciona esta lección.
  En inglés, el nombre de la compañía es "Blackwell 5".
- [Kwon et al. (2023). Efficient Memory Management for Large Language Model Serving with PagedAttention](https://arxiv.org/abs/2309.06180) Papel de la VLLM.
  En el caso de los niños, el problema es que el niño tiene que ser un niño.
- [Leviathan et al. (2023). Fast Inference from Transformers via Speculative Decoding](https://arxiv.org/abs/2211.17192) Descripción de especificaciones.
  Traducción:Tú测解码论文.
- [Li et al. (2024). EAGLE: Speculative Sampling Requires Rethinking Feature Uncertainty](https://arxiv.org/abs/2401.15077) Documento de EAGLE-1/2 para el enfoque de proyecto integrado que cita la lección.
  El proyecto de ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la
- [Cai et al. (2024). Medusa: Simple LLM Inference Acceleration Framework with Multiple Decoding Heads](https://arxiv.org/abs/2401.10774) el enfoque Medusa mencionado junto con EAGLE.
  En el caso de la Medusa, el método de la Medusa es el método de la Medusa.
- [vLLM docs — PagedAttention](https://docs.vllm.ai/en/latest/design/kernel/paged_attention.html) el profundo inmersión canónica en el bloque de 16 tokens y diseño de tabla de páginas.
  En el caso de los ejemplos de la página web, el usuario puede utilizar el código de acceso de la página web.
