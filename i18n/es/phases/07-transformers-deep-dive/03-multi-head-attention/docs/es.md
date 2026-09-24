# Atención de varias cabezas
# Mucho de atención

> Una cabeza de atención aprende una relación a la vez ocho cabezas aprenden ocho cabezas son libres toma más de ellas

> Una atención primera vez aprender una relación.

> **【中文解读】**Muchos cabezas de atención hacen que el modelo se concentre al mismo tiempo en diferentes tipos de relaciones: lenguaje, lenguaje, posición, etc.

**Type:** Build | **类型:** 动手
**Language:**¿ Qué pasa ?**语言:**Python
**Prerequisites:** Phase 7 · 02 (Self-Attention from Scratch) | **前置知识:** 阶段 7 · 02（从零实现自注意力）
**Time:** ~75 minutes | **时间:** ~75 分钟

## El problema es la introducción del problema

Una sola cabeza de autoatención calcula una matriz de atención. Esa matriz captura un tipo de relación  generalmente la que minimiza la pérdida en cualquier señal de entrenamiento. Si sus datos tienen acuerdo entre sujeto y verbo, co-referencia, discurso de largo alcance y fragmentos sintácticos enredados juntos, una sola cabeza los desprende en una sola distribución de máxima suave y pierde la mitad de la señal.

> 单个自注意头计算一个注意矩阵――这个矩阵捕获一种关系通常是最小化训练信号损失的一种――如果你的数据中的主题一致、共指消解、长程语篇和句法分块纠在一起,单个头会模糊它们成单软max 分布,丢失半信号――

La solución del artículo Vaswani de 2017: ejecuta varias funciones de atención en paralelo, cada una con sus propias proyecciones Q, K, V, y concatenar las salidas.`d_model / n_heads`Los parámetros totales permanecen iguales.

> El proyecto de revisión de Vaswani 论文 2017:并行运行多个注意力函数, cada uno tiene su propio Q、K、V 投影, luego拼接输出──每个头在维度为`d_model / n_heads`La cantidad de elementos no cambia, la capacidad de expresión aumenta.

La atención multi-cabeza es el predeterminado de cada transformador en los barcos de 2026. El único argumento es sobre *cuántas cabezas* y si las claves y valores comparten proyecciones (Attención de consulta grupada, Atención de consulta múltiple, Atención latente de múltiples cabezas).

> La única disputa es sobre * cuantos* títulos y si el clave y el valor son de compartir proyecciones (¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡

> **【中文解读】**个头的注意力只能学习一种关系模式, pero en el lenguaje natural existen varias relaciones. 个头的注意力的核心思想: con múltiples cabezas de atención independientes, cada cabeza aprende diferentes relaciones en diferentes espacios, finalmente拼接混合──参数不变,表达能力大幅提升──

## El concepto central.

![Multi-head attention splits, attends, concatenates](../assets/multi-head-attention.svg)

**Split.**¿ Qué ?`X`de forma`(N, d_model)`Proyecto a Q, K, V de cada forma `(N, d_model)`- Reconfigurar para`(N, n_heads, d_head)`donde`d_head = d_model / n_heads`. Transponer a`(n_heads, N, d_head)`¿ Qué ?

> **拆分。**取形为 `(N, d_model)`de la `X`◊ proyección hasta la forma`(N, d_model)`de Q、K、V──重塑为 `(N, n_heads, d_head)`, entre ellos `d_head = d_model / n_heads`                                                                                                                                                                                                                                                              `(n_heads, N, d_head)`¿Qué es eso?

**Attend in parallel.**ejecutar escalado producto de puntos de atención dentro de cada cabeza.`(N, d_head)`Las cabezas operan en diferentes subespacios de la incorporación y nunca hablan durante el cálculo de la atención.

> **并行计算注意力。**En cada cabeza se ejecuta un reducido punto de concentración.`(N, d_head)`头在嵌入的不同子空间上操作,在注意计算本身期间互不通信──

**Concatenate and project.**Las cabezas de pila vuelven a la`(N, d_model)`y multiplicar por una matriz de salida aprendida `W_o`de forma`(d_model, d_model)`- ¿ Qué ?`W_o`Es donde las cabezas se mezclan.

> **拼接并投影。**Se volverá a reponer para`(N, d_model)`Y multiplicando la matriz de salida de aprendizaje`W_o`, forma `(d_model, d_model)`¿Qué es eso?`W_o`Es un lugar mezclado.

**Why it works.**Cada cabeza puede especializarse sin competir con los demás para el presupuesto representativo. Los estudios de sondeo de 20192024 muestran diferentes roles de cabeza: cabezas posicionales, cabeza que atiende al token anterior, cabezas de copia, cabezas de entidades nombradas, cabezas de inducción (que son la base del aprendizaje en contexto).

> **为什么有效。**Cada uno de los títulos puede especializarse sin competir con otros títulos para representar el presupuesto. Un estudio de investigación de 2019-2024 muestra diferentes papeles de los títulos: posición de los títulos, atención a los títulos de un token anterior, copia de los títulos, nombre de los títulos, regeneración de los títulos.

> **【中文解读】**Tres pasos: Split(divide dividido a varios niños espacios)→ Asistir(cada uno de ellos hacerse atentamente)→ Concat+Proyecto(拼接并通过W_o 混合)。

> **【拓展：GQA 在 Llama 3 中的实际应用】**Llama 3 70B utiliza 64 cabezas de consulta pero sólo 8 cabezas de KV, el KV 缓存压缩了8倍―― esto ahorra en el tiempo de la investigación una gran cantidad de almacenamiento, al mismo tiempo que casi no pierde la calidad del modelo―GQA 已 se ha convertido en el patrón del modelo de código abierto de 2024-2026―DeepSeek-V2  MLA 则进一步,将 KV 压缩到低排隐空间―

**The 2026 lineage of variations:**

> **2026 年的变体谱系：**

| Variant | Q heads / Q 头数 | K/V heads / K/V 头数 | Used by / 使用者 |
|---------|---------|-----------|---------|
| Multi-head (MHA) / 多头 | N | N | GPT-2, BERT, T5 |
| Multi-query (MQA) / 多查询 | N | 1 | PaLM, Falcon |
| Grouped-query (GQA) / 分组查询 | N | G (e.g. N/8) | Llama 2 70B, Llama 3+, Qwen 2+, Mistral |
| Multi-head latent (MLA) / 多头潜在 | N | compressed to low-rank / 压缩为低秩 | DeepSeek-V2, V3 |

GQA es el estándar moderno porque reduce la memoria de caché KV en un factor de `N/G`MLA va más allá comprimiendo K/V en un espacio latente, luego proyectando de nuevo en tiempo de cálculo  cuesta FLOPs, ahorra mucho más memoria.

> GQA es una opción moderna, ya que reducirá la KV 缓存内存 `N/G`倍, al mismo tiempo que mantiene casi la calidad completa. MLA 通過將 K/V 壓縮到隱藏空間更进一步,然后在計算時投影回來花費 FLOP,節省更多內存.

## Construye y realiza.
```figure
multihead-split
```

## Construye el mismo

### Paso 1: Separar las cabezas de la atención de cabeza única que ya tenemos. Paso 1: Desglosar la atención de cabeza única existente.

Toma el .`SelfAttention`En el caso de las clases de la segunda clase, el resultado de la prueba es el resultado de la prueba de la segunda clase.`code/main.py`para una implementación numpy; la lógica es:

> 取第 02 课的                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                       `SelfAttention`, Usando la división /拼接对包装它──参见 `code/main.py`En el caso de la aplicación de la ley, el código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de no se puede utilizar en el siguiente modo:

```python
def split_heads(X, n_heads):
    n, d = X.shape
    d_head = d // n_heads
    return X.reshape(n, n_heads, d_head).transpose(1, 0, 2)  # (heads, n, d_head)

def combine_heads(H):
    h, n, d_head = H.shape
    return H.transpose(1, 0, 2).reshape(n, h * d_head)
```

Uno se remodela y otro se transponen.`nn.MultiheadAttention`¿ Qué ?

> Una vez se vuelve a formar y una vez se transpone.`nn.MultiheadAttention`Lo que hace el nivel inferior.

> **【中文解读】** `split_heads`Y `combine_heads`                                                                                                                                                                                                                                                              

### Paso 2: ejecutar escalado punto-producto atención por cabeza Paso 2: cada cabeza se reduce en punto acumulación de atención

Cada cabeza recibe su propia rebanada de Q, K, V. La atención se convierte en un matmul en lote:

> Cada cabeza obtiene su propio Q、K、V 切片── la atención se convierte en la matriz de masa multiplicada:

```python
def mha_forward(X, W_q, W_k, W_v, W_o, n_heads):
    Q = X @ W_q
    K = X @ W_k
    V = X @ W_v
    Qh = split_heads(Q, n_heads)         # (heads, n, d_head)
    Kh = split_heads(K, n_heads)
    Vh = split_heads(V, n_heads)
    scores = Qh @ Kh.transpose(0, 2, 1) / np.sqrt(Qh.shape[-1])
    weights = softmax(scores, axis=-1)
    out = weights @ Vh                    # (heads, n, d_head)
    concat = combine_heads(out)
    return concat @ W_o, weights
```

En hardware real .`Qh @ Kh.transpose(...)`Es uno .`bmm`La GPU ve un solo parche de forma .`(heads, N, d_head) × (heads, d_head, N) -> (heads, N, N)`Añadir cabezas es gratis.

> En el hardware real,`Qh @ Kh.transpose(...)`Es una vez.`bmm`◊GPU 看到的是形状为 `(heads, N, d_head) × (heads, d_head, N) -> (heads, N, N)`El aumento de la cantidad de la matriz es gratuito.

### Paso 3: Variante de atención de la pregunta agrupada 步骤 3:分组查询注意力变体

Sólo las proyecciones de clave y valor cambian.`n_heads`los grupos; K y V obtendrán`n_kv_heads < n_heads`grupos y se repiten para coincidir:

> Sólo la proyección de la clave y el valor cambia.`n_heads`个组; K 和 V 有 `n_kv_heads < n_heads`个组,并被重复以匹配:

```python
def gqa_project(X, W, n_kv_heads, n_heads):
    kv = split_heads(X @ W, n_kv_heads)       # (kv_heads, n, d_head)
    repeat = n_heads // n_kv_heads
    return np.repeat(kv, repeat, axis=0)      # (n_heads, n, d_head)
```

En la inferencia esto ahorra memoria porque sólo`n_kv_heads`Las copias viven en el caché KV, no `n_heads`Llama 3 70B utiliza 64 cabezas de consulta con 8 cabezas de KV  un 8x cache contractor.

> En el momento de la investigación, esto ahorra memoria, porque sólo`n_kv_heads`份副本 existe en KV 缓存中, en lugar de `n_heads`份──Llama 3 70B Utiliza 64 cabezas de consulta y 8 cabezas de KV 8 倍的缓存缩减──

> **【拓展：MQA/GQA 在推理中的内存节约】**KV 缓存大小与 KV 缓存数成正比──Llama 3 70B utiliza 64 查询头, pero sólo 8 KV 头, KV 缓存压缩了8倍──对于128K 上下文,这意味着节省数 GB 显存──这是大模型长上下文推理的关键优化GQA 几乎不损质量,但显著降低推理成本──

### Paso 4: Probe lo que cada cabeza ha aprendido. Paso 4: Explora lo que cada cabeza ha aprendido.

Ejecutar MHA en una frase corta con 4 cabezas.`(N, N)`Verá diferentes cabezas seleccionar diferentes estructuras incluso con inicialización aleatoria que es en parte señal, en parte simetría de rotación en los subespacios.

> En pocas palabras, utiliza 4 cabezas para ejecutar MHA.`(N, N)`Nota: Se puede ver que incluso con la inicialización de la forma de la forma, diferentes cabezas también escogen diferentes estructuras.

## Usalo con el marco de ejecución

En PyTorch, la versión de una línea:

> PyTorch 中,一行版本:

```python
import torch.nn as nn

mha = nn.MultiheadAttention(embed_dim=512, num_heads=8, batch_first=True)
```

GQA a partir de PyTorch 2.5+:

> GQA(PyTorch 2.5+):

```python
from torch.nn.functional import scaled_dot_product_attention

# scaled_dot_product_attention auto-dispatches Flash Attention on CUDA.
# For GQA, pass Q of shape (B, n_heads, N, d_head) and K,V of shape
# (B, n_kv_heads, N, d_head). PyTorch handles the repeat.
out = scaled_dot_product_attention(q, k, v, is_causal=True, enable_gqa=True)
```

**How many heads?**Reglas generales de los modelos de producción en 2026:

> **多少个头？**Ley de experiencia de producción modelo 2026:

| Model size / 模型大小 | d_model | n_heads | d_head |
|------------|---------|---------|--------|
| Small (~125M) / 小型 | 768 | 12 | 64 |
| Base (~350M) / 基础 | 1024 | 16 | 64 |
| Large (~1B) / 大型 | 2048 | 16 | 128 |
| Frontier (~70B) / 前沿 | 8192 | 64 | 128 |

`d_head`casi siempre aterriza en 64 o 128. Es la unidad de cuánto una cabeza puede "ver". Baja por debajo de 32 y las cabezas comienzan a luchar contra el factor de escala.`sqrt(d_head)`Si se superan los 256 y se pierde el beneficio de "muchos especialistas pequeños".

> `d_head`几乎总是64或128──它是一个头能"见"多少的量单位──低于32时,头开始与缩小因子 `sqrt(d_head)`冲突; más de 256 时, has perdido los beneficios de "many小专家"

## Envíe el producto .

¿ Qué ?`outputs/skill-mha-configurator.md`. La habilidad recomienda el recuento de cabezas, el recuento de cabezas kv y la estrategia de proyección para un nuevo transformador dado el presupuesto de parámetros, la longitud de la secuencia y el objetivo de despliegue.

> 参见 `outputs/skill-mha-configurator.md` Esta habilidad se aplica a los nuevos transformadores                                                                                                                                                                                                                                                         

## Los ejercicios.

1. **Easy / 简单。**Tome el MHA de `code/main.py`y el cambio`n_heads`de 1 a 16 con `d_model=64`¿Ayuda más cabezas, plato o daño?
   取 `code/main.py`En el centro de MHA, en el`d_model=64`En determinadas circunstancias se`n_heads`¿Es más útil alcanzar el período de plataforma o perjudicial?

2. **Medium / 中等。**Implemente MQA (una cabeza de KV compartida entre todas las cabezas de consulta). Medir cuánto parámetro cuenta caídas frente a MHA completa. Compute cuánto se reduce el tamaño de la caché de KV a la inferencia para N = 2048.
   实现 MQA(un KV 头在所有查询头间共享) ⋅测量与完整MHA相比参数下降多少──计算在 N=2048的推理时 KV 缓存大小缩减多少──

3. **Hard / 困难。**Implemente una versión pequeña de Multi-head Latent Attention: comprime K, V a un rango de`r`Se puede almacenar en el caché KV, descomprimir en el tiempo de atención.`r`¿La memoria de caché pasa por debajo de 1/8 de la MHA completa mientras que la calidad permanece dentro de 1 bit de la validación ppl?
   实现迷你版的 Multi-head Latent Attention:将 K,V 压缩为秩 `r`El valor de la información en el archivo de KV                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                  `r`值下缓存内存降到完整MHA的1/8以下, mientras que la calidad se mantiene en el proceso de comprobación de 1 bit desde dentro?

## Términos clave .

| Term | What people say / 人们怎么说 | What it actually means / 实际含义 |
|------|------------------------------|----------------------------------|
| Head / 头 | "A single attention circuit" / "一个注意力电路" | One Q/K/V projection of dimension `d_head = d_model / n_heads` with its own attention matrix. 维度为 `d_head = d_model / n_heads` 的一个 Q/K/V 投影，有自己的注意力矩阵。 |
| d_head | "Head dimension" / "头维度" | Per-head hidden width; almost always 64 or 128 in production. 每个头的隐藏宽度；生产中几乎总是 64 或 128。 |
| Split / combine / 拆分/合并 | "Reshape tricks" / "reshape 技巧" | `(N, d_model) ↔ (n_heads, N, d_head)` reshape+transpose around attention. 围绕注意力的 `(N, d_model) ↔ (n_heads, N, d_head)` reshape+transpose。 |
| W_o | "Output projection" / "输出投影" | `(d_model, d_model)` matrix applied after concatenating heads; where heads mix. 拼接头后应用的 `(d_model, d_model)` 矩阵；头混合的地方。 |
| MQA | "One KV head" / "一个 KV 头" | Multi-Query Attention: single shared K/V projection. Smallest KV cache, some quality loss. 多查询注意力：单个共享的 K/V 投影。最小 KV 缓存，有一些质量损失。 |
| GQA | "The default since Llama 2" / "Llama 2 之后的默认" | Grouped-Query Attention with `n_kv_heads < n_heads`; repeats to match Q. 分组查询注意力，`n_kv_heads < n_heads`；重复以匹配 Q。 |
| MLA | "DeepSeek's trick" / "DeepSeek 的技巧" | Multi-head Latent Attention: K,V compressed to low-rank latent, decompressed at attend time. 多头潜在注意力：K,V 压缩为低秩隐向量，在注意力计算时解压。 |
| Induction head / 归纳头 | "The circuit behind in-context learning" / "上下文学习背后的电路" | A pair of heads that detect previous occurrences and copy what followed them. 一对检测先前出现模式并复制后续内容的头。 |

## Más Leer más Leer más

- [Vaswani et al. (2017). Attention Is All You Need §3.2.2](https://arxiv.org/abs/1706.03762) la especificación original de múltiples cabezas.
  Vaswani 等人(2017)  原始多头规范──

- [Shazeer (2019). Fast Transformer Decoding: One Write-Head is All You Need](https://arxiv.org/abs/1911.02150) el documento de la MQA.
  Shazeer(2019)  MQA 论文。

- [Ainslie et al. (2023). GQA: Training Generalized Multi-Query Transformer Models from Multi-Head Checkpoints](https://arxiv.org/abs/2305.13245) cómo convertir la MHA en GQA después de la formación.
  Ainslie 等人(2023)  训练后如何将 MHA 转换为 GQA。

- [DeepSeek-AI (2024). DeepSeek-V2 Technical Report](https://arxiv.org/abs/2405.04434) MLA y por qué supera a MHA/GQA en memoria caché.
  DeepSeek-AI (MLA) 2024 及为何在缓存内存上击败 MHA/GQA

- [Olsson et al. (2022). In-context Learning and Induction Heads](https://transformer-circuits.pub/2022/in-context-learning-and-induction-heads/index.html) Mecanicistas mira lo que las cabezas realmente hacen.
  Olsson 等人 (2022)  análisis del mecanismo de las funciones reales de la cabeza.

> **【拓展：Induction Heads 与上下文学习】**El estudio antropológico encontró que la capacidad de aprendizaje literario superior de Transformer (en contexto) se realiza principalmente por un tipo de cabeza de atención llamada "cabeza de inducción". Esto explica por qué el gran modelo puede "aprender de ejemplos" y no necesita actualizar el poder de pesar.
