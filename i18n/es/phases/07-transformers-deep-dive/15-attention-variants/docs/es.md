# Variancias de atención  Ventana deslizante, Sparse, Diferencial  Variación de atención  ventana deslizante 稀疏 差分注意力

> La atención completa es un círculo. Cada token ve cada token, y la memoria paga el precio. Cuatro variantes doblan la forma del círculo y recuperan la mitad del costo.

> **【中文解读】**标准注意力 O(n^2) 复杂度太贵;;滑动窗口注意力(Mistral) 稀疏注意力、差分注意力是降低复杂度的方法──

**Type:** Hands-on | **类型:** 动手
**Language:**¿ Qué pasa ?**语言:**Python
**Prerequisites:** Phase 7 · 02 (Self-Attention), Phase 7 · 03 (Multi-Head), Phase 7 · 12 (KV Cache / Flash Attention) | **前置知识:** Phase 7 · 02 (Self-Attention), Phase 7 · 03 (Multi-Head), Phase 7 · 12 (KV Cache / Flash Attention)
**Time:** ~60 minutes | **时间:** ~60 分钟

## El problema es la introducción del problema

Costos de atención plena `O(N²)`memoria y `O(N²)`Para un Llama 3 70B de 128K de contexto que es 16 mil millones de entradas de atención por capa, veces 80 capas.`O(N²)`memoria de activación pero no cambia el costo aritmético  cada token todavía atende a cada otro token.

> Todo el enfoque en la duración del proceso es la memoria y el costo de cálculo.`O(N²)`❖ Para 128K 上下文 ◦ Llama 3 70B, eso es cada capa 160 mil millones de notas de atención, multiplicadas por 80 niveles.`O(N²)`de activar la memoria, pero no cambia el costo de cálculo  cada token  sigue preocupado por cada otro token 

Tres clases de variantes cambian la topología de la matriz de atención misma:

> Tres tipos de variables han cambiado la estructura de la matriz de atención en sí misma:

1. **Sliding window attention (SWA).**Cada token se encuentra en una ventana fija de vecinos, no en el prefijo completo.`O(N · W)`donde`W`Gemma 2/3, las primeras capas del Mistral 7B, Phi-3-Long.
   En inglés:**滑动窗口注意力 (SWA)。**Cada token se centra sólo en el vecino de la ventana fija, y no en el anterior completo.`O(N · W)`, entre ellos `W`Es una ventana grande. Gemma 2/3 de la ventana.
2. **Sparse / block attention.**Sólo pares seleccionados `(i, j)`Los demás se ven obligados a cero peso. Longformer, BigBird, OpenAI transformador escaso.
   En inglés:**稀疏/块注意力。**只有选定的 `(i, j)`Se trata de un proyecto de investigación que se ha desarrollado en el campo de la investigación y la investigación.
3. **Differential attention.**Computa dos mapas de atención con proyecciones Q/K separadas, restar uno del otro. Mata el "sink de atención" que desangraza el peso en los primeros tokens.
   En inglés:**差分注意力。**Utiliza un Q/K independiente 投影计算两个注意力图,将一个从另一个减去―― eliminar将权重汇聚到前几个代币的"注意力汇聚"现象――Microsoft's DIFF Transformer(2024)。

Los modelos fronterizos de 2026 a menudo los mezclan: la mayoría de las capas son SWA-1024, cada quinto es atención completa global, y un puñado de cabezas diferenciales que limpian la recuperación.

> 它们 pueden coexistir. Un modelo de vanguardia de 2026 años suele utilizarse en combinación: la mayoría de las capas son SWA-1024, cada cinco capas son la atención total de la escuela, una minoría son los diferencias de la investigación de limpieza.

> **【中文解读】**Tres formas de reducir la complejidad de la atención: 1) la ventana de desplazamiento (SWA)  sólo se centra en la complejidad local, O * N * W)  complejidad; 2) la rara / bloque de atención sólo se calcula para el token seleccionado; 3) la diferencia de la atención dos grupos Q / K  Atención  reducción, eliminación de " concentración de atención" fenómeno.

## El concepto central.

### Atención a las ventanas deslizantes (SWA)

Cada consulta en posición `i`sólo asiste a posiciones en `[i - W, i]`(SWA causal) o `[i - W/2, i + W/2]`Los tokens fuera de la ventana se ponen.`-inf`en la matriz de puntaje.

>  posición `i`Cada consulta sólo se preocupa`[i - W, i]`(因果 SWA) o `[i - W/2, i + W/2]`(双向) posición dentro del rango.`-inf`¿Qué es eso?

```
full causal:           sliding window (W=4):
positions 0-7          positions 0-7, W=4
    0 1 2 3 4 5 6 7        0 1 2 3 4 5 6 7
0 | x                0 |  x
1 | x x              1 |  x x
2 | x x x            2 |  x x x
3 | x x x x          3 |  x x x x
4 | x x x x x        4 |    x x x x
5 | x x x x x x      5 |      x x x x
6 | x x x x x x x    6 |        x x x x
7 | x x x x x x x x  7 |          x x x x
```

Para`N = 8192`y `W = 1024`, la matriz de puntaje tiene 1024 × 8192 filas no cero en la expectativa  una reducción de 8 ×.

>  para `N = 8192`Y `W = 1024`, el número de matrices de la expectativa de 1024 × 8192 ′ ′ ′ ′ ′ ′ ′ ′ ′ ′ ′ ′ ′ ′ ′ ′ ′ ′ ′ ′ ′ ′ ′ ′ ′ ′ ′ ′ ′ ′ ′ ′ ′ ′ ′ ′ ′ ′ ′ ′ ′ ′ ′ ′ ′ ′ ′ ′ ′ ′ ′ ′ ′ ′ ′ ′ ′ ′ ′ ′ ′ ′ ′ ′ ′ ′ ′ ′ ′ ′ ′ ′ ′ ′ ′ ′ ′ ′ ′ ′ ′ ′ ′ ′ ′ ′ ′ ′ ′ ′ ′ ′ ′ ′ ′ ′ ′ ′ ′ ′ ′ ′ ′ ′ ′ ′ ′ ′ ′ ′ ′ ′ ′ ′ ′ ′ ′ ′ ′ ′ ′ ′ ′ ′ ′ ′ ′ ′ ′ ′ ′ ′ ′ ′ ′ ′ ′ ′ ′ ′ ′ ′ ′ ′ ′ ′ ′ ′ ′ ′ ′ ′ ′ ′ ′ ′ ′ ′ ′ ′ ′ ′ ′ ′ ′     ′                                                                                                                                                             

**KV cache shrinks with SWA.**Sólo el último .`W`Los tokens de K y V deben mantenerse por capa. Para una configuración Gemma-3-ish (1024 ventanas, contexto 128K), la caché KV cae 128x.

> **KV 缓存随 SWA 缩小。**Cada nivel sólo tiene que mantener el final de K y V.`W`个 token──对于类 Gemma-3 的配置(1024 窗口,128K 上下文),KV 缓存减少 128 倍──

**Quality cost.**Los transformadores solo SWA luchan con la recuperación a largo alcance. La solución: intercalar capas SWA con capas de atención completa. Gemma 3 utiliza 5:1 SWA:global. Mistral 7B utilizó una pila de SWA causal donde la información "fluye hacia adelante" a través de ventanas superpuestas  cada capa extiende el campo receptivo efectivo por `W`, y después `L`las capas que el modelo puede asistir `L × W`los tokens de vuelta.

> **质量代价。**純 SWA Transformer 在长距离检索上表现不佳──修复方案:将 SWA 层与全注意层交换使用──Gemma 3 使用 5:1 的 SWA:全局比例──Mistral 7B 使用因果 SWA 堆,信息通过重叠窗口"向前流动"每层将有效感受野扩展`W`¿ Qué ?`L`层后模型 se puede rastrear `L × W`Es un símbolo.

### Atención de escasez / bloqueo

Escoge una .`N × N`El patrón de esparcia anticipado.

> 预先选择   en el que se encuentra el`N × N`La forma rara es la de la forma clásica.

- **Local + strided (OpenAI sparse transformer).**Atender a la última .`W`fichas más cada `stride`-Todo el tiempo, capturando tanto a largo alcance como local.`O(N · sqrt(N))`¿Qué es eso?
  En inglés:**局部 + 步进（OpenAI 稀疏 Transformer）。**关注最后 `W`个 token 加上之前每隔 `stride`个 token.`O(N · sqrt(N))`La cantidad de datos calculada a la vez captura información local y de larga distancia.
- **Longformer / BigBird.**Ventana local + un pequeño conjunto de tokens globales (por ejemplo `[CLS]`En el contexto empírico, el contexto 2x es de calidad igualitaria.
  En inglés:**Longformer / BigBird。**局部窗口 + 少量全局 token (en inglés)`[CLS]`) con todos los tokens 双向关注 + 随机稀疏连接―― la experiencia muestra que la siguiente se expandió 2 veces bajo la misma calidad―
- **Native Sparse Attention (DeepSeek, 2025).**Aprenda qué bloques de `(Q, K)`El bloqueo de cero en el núcleo es compatible con FlashAttention.
  En inglés:**原生稀疏注意力（DeepSeek，2025）。**¿Qué aprender?`(Q, K)`块重要;在内核级别跳过零块──与 FlashAttention 兼容──

La matemática es simple (mascarar la matriz de puntaje); la victoria proviene de no cargar nunca las entradas cero en SRAM. FlashAttention-3 y la API 2026 FlexAttention hacen patrones de puntaje personalizados en PyTorch.

> 稀疏注意力 (en inglés: Rare Attention) es una historia de ingeniería nuclear. La matemática es muy simple.

> **【拓展：滑动窗口的信息传递机制】**滑窗注意力看似只能捕获局部信息,但通过多层堆积,信息可以"透透"到更远的位置──W 窗户的L层注意力,有效感受野为L×W──例如W=1024、L=32的模型有效感受野为32K代币──Mistral 7B正是利用这个特性在保持O(N*W) 计算复杂性同时实现长上下文建模──

### El objetivo de la evaluación es garantizar la eficacia de la evaluación de los resultados de la evaluación.

La atención regular tiene un problema de "senqueo de atención": softmax obliga a cada fila a sumar a 1, por lo que los tokens que no quieren atender a nada en particular se desprenden del peso en el primer token (o los primeros pocos).

> 标准注意力有"注意力汇聚"问题:softmax 强制每行总和为1,所以不想关注任何特定内容的代币会重量倾倾倒到第一代币(或前几个) ;; Esto robó la capacidad de contenido real que se debería usar en el caso de que fuese un token.

La atención diferencial corrige esto mediante la computación **two**mapas de atención y restantes:

> 差分注意力 差分注意力 差分注意力 差分注意力 差分注意力 差分注意力 差分注意力 差分注意力 差分注意力 差分注意力 差分注意力 差分注意力 差分注意力 差分注意力 差分注意力 差分注意力 差分注意力 差分 差分 差分 差分 差分 差分 差分 差分 差分 差分 差分 差分 差分 差分 差分 差分 差分 差分 差分 差分 差分 差分 差分 差分 差分 差分 差分 差分 差分 差分 差分 差分 差分 差分 差分 差分 差分 差分 差分 差分 差分 差分 差分 差分 差分 差分 差分 差分 差分 差分 差 差 差 差 差 差 差 差 差 差 差 差 差 差 差 差 差 差 差 差 差 差 差 差 差 差 差 差 差 差 差 差 差 差 差 差 差 差 差 差 差 差 差 差 差 差 差 差 差 差 差 差 差 差 差 差 差 差 差 差 差 差 差 差 差 差 差 差 差 差 差 差 差 差 差 差 差 差 差 差 差 差 差 差 差 差 差 差 差 差 差 差 差 差 差 差 差 差 差 差 差 差 差 差 差 差 差 差 差 差 差 差 差 差 差 差 差 差 差 差 差 差 差 差 差 差 差 差 差 差 差 差 差 差 差 差 差 **两个**Nota: El problema se encuentra en el punto de partida.

```
A1 = softmax(Q1 K1^T / √d)
A2 = softmax(Q2 K2^T / √d)
DiffAttn = (A1 - λ · A2) V
```

donde`λ`Es un escalar aprendido (típicamente 0.50.8). A1 captura los pesos reales del contenido; A2 capta el fregadero.

> Entre ellos `λ`Es un aprendizaje de la cantidad de datos que se puede obtener de la información.

Resultados reportados (Microsoft 2024): 510% menos perplejidad, contexto efectivo 1,52× más largo en la misma longitud entrenada, recuperación de aguja en haystack más nítida.

> 報告結果(Microsoft 2024):困惑度降低 5-10%,同训长度下有效上下文长度增加1.5-2 veces,agullas en haystack 检索更精确──

> **【中文解读】**差分注意力创新之处: 标准注意力因软max 归归化导致"注意力汇聚" (en inglés) 不相关的代币 放重重集中在序列开头的代币 上。差分注意力计算两组注意力并相减, A1 捕获真内容权重, A2 捕获汇聚噪音,相减后消除汇聚现象──困惑度降低 5-10%──

> **【拓展：Gemma 3 的混合注意力策略】**Google Gemma 3 utiliza 5:1 de la relación de la ventana de desplazamiento con la atención general de la región  por 5 niveles de atención general de la región  después de 1 nivel de atención general de la región . Esto mantiene la capacidad de construcción de la región ................................................................................................................................................................................................................................

### Comparación de variantes

| Variant | Compute | KV cache | Quality vs full | Production use |
|---------|---------|----------|-----------------|----------------|
| 变体 | 计算量 | KV 缓存 | 相对全注意力的质量 | 生产使用 |
| Full attention | O(N²) | O(N) per layer | baseline | every model's default layer |
| 全注意力 | O(N²) | 每层 O(N) | 基线 | 每个模型的默认层 |
| SWA (window 1024) | O(N·W) | O(W) per layer | -0.1 ppl, good with global layers | Gemma 2/3, Phi-3-Long |
| 滑动窗口 (窗口 1024) | O(N·W) | 每层 O(W) | -0.1 ppl，配合全局层效果好 | Gemma 2/3, Phi-3-Long |
| Local + strided sparse | O(N·√N) | mixed | similar to SWA | OpenAI sparse transformer, Longformer |
| 局部+步进稀疏 | O(N·√N) | 混合 | 类似 SWA | OpenAI 稀疏 Transformer, Longformer |
| BigBird (local + global + random) | O(N) approx | mixed | matches full at 2× context | early long-context BERT |
| BigBird (局部+全局+随机) | O(N) 近似 | 混合 | 2 倍上下文下匹配全注意力 | 早期长上下文 BERT |
| Native Sparse (DeepSeek-V3.2) | O(N · active fraction) | O(N) | within 0.05 ppl | DeepSeek-V3.2, 2025 |
| 原生稀疏 (DeepSeek-V3.2) | O(N · 活跃比例) | O(N) | 0.05 ppl 以内 | DeepSeek-V3.2, 2025 |
| Differential | O(2·N²) | O(2N) | -5 to -10% ppl | DIFF Transformer, early 2026 models |
| 差分 | O(2·N²) | O(2N) | 困惑度降低 5-10% | DIFF Transformer, 2026 早期模型 |

## Construye y realiza.
```figure
gqa-kv-sharing
```

## Construye el mismo

¿ Qué ?`code/main.py`Implementamos un comparador de máscaras causales que muestra la atención completa, SWA, local+strided y diferencial lado a lado en una secuencia de juguetes.

> 参见 `code/main.py` Hemos implementado un comparador de ocultación de factores, que muestra la atención total en la secuencia de juguetes, SWA, local + progreso y diferenciación de atención

### Paso 1: máscara causal completa (línea de base)

```python
def causal_mask(n):
    return [[0.0 if j <= i else float("-inf") for j in range(n)] for i in range(n)]
```

Línea de base de la lección 07. Triangular inferior; peso cero por encima de la diagonal.

> Sección 07 课的基线──下三角;对角线上权重为零──

### Paso 2: máscara causal de ventana deslizante

```python
def swa_mask(n, window):
    M = [[float("-inf")] * n for _ in range(n)]
    for i in range(n):
        lo = max(0, i - window + 1)
        for j in range(lo, i + 1):
            M[i][j] = 0.0
    return M
```

Un parámetro  `window`- Para .`window >= n`, se recupera la atención causal completa.`window = 1`, cada token se atende sólo a sí mismo.

> Un parámetro`window`¿Qué es esto?`window >= n`时, recuperar para todo el efecto atención.`window = 1`时, cada token sólo se preocupa por sí mismo.

### Paso 3: local + máscara escasa de paso

```python
def strided_mask(n, window, stride):
    M = [[float("-inf")] * n for _ in range(n)]
    for i in range(n):
        lo = max(0, i - window + 1)
        for j in range(lo, i + 1):
            M[i][j] = 0.0
        for j in range(0, i + 1, stride):
            M[i][j] = 0.0
    return M
```

La ventana local es densa más cada uno .`stride`El campo receptor crece en etapas de registro con capas adicionales.

> La ventana de la sección de la sección de la sección de la sección de la sección de la sección de la sección de la sección de la sección de la sección de la sección de la sección de la sección de la sección de la sección de la sección de la sección de la sección de la sección de la sección de la sección de la sección de la sección de la sección de la sección de la sección de la sección de la sección de la sección de la sección de la sección de la sección de la sección de la sección de la sección de la sección de la sección de la sección de la sección de la sección de la sección de la sección de la sección de la sección de la sección de la sección de la sección de la sección de la sección de la sección de la sección de la sección de la sección de la sección de la sección de la sección de la sección de la sección de la sección de la sección de la sección de la sección de la sección de la sección de la sección de la sección de la sección de la sección de la sección de la sección de la sección de la sección de la sección de la sección de la sección de la sección de la sección de la sección de la sección de la sección de la sección de la sección de la sección de la sección de la sección de la sección de la sección de la sección de la sección de la sección de la sección de la sección de la sección de la sección de la sección de la sección de la sección de la sección de la sección de la sección de la sección de la sección de la sección de la sección de la sección de la sección de la sección de la sección de la sección de la sección de la sección de la sección de la sección de la sección de la sección de la sección de la sección de la sección de la sección de la sección de la sección de la sección de la sección de la sección de la sección de la sección de la sección de la sección de la sección de la sección de la sección de la sección de la sección de la sección de la sección de la sección de la sección de la sección de la sección de la sección de la sección de la sección de la sección de la sección de la sección de la sección de la sección de la sección de la sección de la sección de la sección de la sección de la sección de la sección de la sección de la sección de la sección de la sección de la sección de la sección de la sección de la sección de la sección de la sección de la sección de la sección de la sección de los departamentos de la`stride`个标志──感受野随着数层以对数步长的增长──

### Paso 4: Atención diferenciada

```python
def diff_attention(Q1, K1, Q2, K2, V, lam):
    A1 = softmax_causal(Q1 @ K1.T / sqrt_d)
    A2 = softmax_causal(Q2 @ K2.T / sqrt_d)
    return (A1 - lam * A2) @ V
```

En el código comparamos el mapa de calor de la concentración de la concentración de la concentración de la concentración de la concentración de la concentración de la concentración de la concentración de la concentración de la concentración de la concentración de la concentración de la concentración de la concentración de la concentración de la concentración de la concentración de la concentración de la concentración de la concentración de la concentración de la concentración de la concentración de la concentración de la concentración de la concentración de la concentración de la concentración de la concentración de la concentración de la concentración de la concentración de la concentración de la concentración de la concentración de la concentración de la concentración de la concentración de la concentración de la concentración de la concentración de la concentración de la concentración de la concentración de la concentración de la concentración de la concentración de la concentración de la concentración de la concentración de la concentración de la concentración de la concentración de la concentración de la concentración de la concentración de la concentración de la concentración de la concentración de la concentración de la concentración de la concentración de la concentración de la concentración de la concentración de la concentración de la concentración de la concentración de la concentración de la concentración de la concentración de la concentración de la concentración de la concentración de la concentración de la concentración de la concentración de la concentración de la concentración de la concentración de la concentración de la concentración de la concentración de la concentración de la concentración de la concentración de la concentración de la concentración de la concentración de la concentración de la concentración de la concentración de la concentración de la concentración de la concentración de la concentración de la concentración de la concentración de la concentración de la concentración de la concentración de la concentración de la concentración de la concentración de la concentración de la concentración de la concentración de la concentración de la concentración de la concentración de la concentración de la concentración de la concentración de la concentración de la concentración de la concentración de la concentración de la concentración de la concentración de la concentración de la concentración de la concentración de la concentración de la concentración de la concentración de la concentración de la concentración de la concentración de la concentración de la concentración de la concentración de la concentración de la concentración de la concentración de la concentración de la concentración de la concentración de la concentración de la concentración de la concentración de la concentración de la concentración de la cubo en el descienda de la cubo.

>  2 veces la atención calculada, utilizando la combinación de factores de la reducción aprendida. En el código comparamos la concentración de la atención individual con la diferenciación de la atención, observando la eliminación del fenómeno de la concentración.

### Paso 5: Tamaños de caché de KV

Imprima el tamaño de la caché por capa en `N = 131072`Las variantes SWA y raras caen en 10 100 ×. Dobles diferenciales.

> 打印 `N = 131072`时每种变体每层缓存大小──SWA 和稀疏变体减少10-100 倍──差分变体翻倍──应有意识地管理你的内存开销──

## Usalo con el marco de ejecución

Modelos de producción para 2026:

> Modelo de producción de 2026:

```python
from transformers import AutoModelForCausalLM
# Gemma 3 mixes SWA (window=1024) and global layers at 5:1.
model = AutoModelForCausalLM.from_pretrained("google/gemma-3-27b-it")
# print(model.config.sliding_window, model.config.layer_types)
```

FlexAttention en PyTorch 2.5+ acepta una función de máscara:

> PyTorch 2.5+ 中的 FlexAttention  acepta la función de ocultamiento:

```python
from torch.nn.attention.flex_attention import flex_attention, create_block_mask

def swa_pattern(b, h, q_idx, kv_idx):
    return (q_idx - kv_idx < 1024) & (q_idx >= kv_idx)

mask = create_block_mask(swa_pattern, B=batch, H=heads, Q_LEN=n, KV_LEN=n)
out = flex_attention(q, k, v, block_mask=mask)
```

Esto se compiló a un núcleo Triton personalizado. dentro del 10% de la velocidad de FlashAttention-3 para patrones comunes, y la función de máscara es una llamada Python.

> Esto se traducirá en Triton 内核. Para el modo habitual, la velocidad está en el 10% de FlashAttention-3, y la función de ocultamiento es un objeto de Python que se puede ajustar.

**When to pick each:**

> **何时选择每种变体：**

- **Pure full attention** cada capa hasta ~ 16K contexto, o cuando la calidad de recuperación es primordial.
  En inglés:**纯全注意力** Cada nivel se utiliza hasta aproximadamente 16K en la siguiente, o en un escenario de gran importancia.
- **SWA + global mix** contexto largo (> 32K), formación y inferencia limitada a la memoria.
  En inglés:**SWA + 全局混合** 长上下文(>32K), entrenamiento y la evaluación de la memoria
- **Sparse block attention** kernel personalizado, patrón personalizado. Reservado para cargas de trabajo especializadas (recuperación, audio).
  En inglés:**稀疏块注意力** 自定义内核,自定义模式──专用于特殊工作负载(检索、音频)──
- **Differential attention** cualquier carga de trabajo en la que la contaminación por sumido de atención sea perjudicial (RAG de largo contexto, aguja en el manto de heno).
  En inglés:**差分注意力** Atención 汇聚污染有害的任何工作负载(长上下文 RAG、agul-en-haystack)

## Envíe el producto .

¿ Qué ?`outputs/skill-attention-variant-picker.md`. La habilidad selecciona una topología de atención para un nuevo modelo dada la longitud del contexto objetivo, las demandas de recuperación y el perfil de computación de formación/inferencia.

> 参见 `outputs/skill-attention-variant-picker.md` Esta habilidad  basándose en el objetivo  la longitud de la siguiente descripción  la demanda y la formación / la orientación de la configuración de cálculo, para seleccionar el nuevo modelo  la orientación y la orientación de la información.

## Los ejercicios.

1. **Easy.**- ¿ Qué ?`code/main.py`Verifique el SWA en`window=4`cero todo fuera de los últimos 4 tokens por fila.`window=n`reproducen la atención causal completa de forma bit-identica.
   Traducción:运行`code/main.py` Prueba`window=4`El SWA pondrá todo lo que hay fuera de los últimos 4 tokens de cada línea.`window=n`能逐位复现全因果注意力──
2. **Medium.**Implementar la SWA causal con `window=1024`¿Cuánto disminuye la pérdida de val vs. plena atención? ¿Cuánto disminuye la memoria máxima?
   En la lengua china , el programa de formación de estudiantes es un proyecto de formación de estudiantes .`window=1024`¿Cuánto es el resultado de la SWA? ¿Cuánto es el valor máximo de la memoria?
3. **Hard.**Implemente una mezcla de capas de 5:1 de estilo Gemma-3 (5 SWA, 1 global) en el modelo de piedra angular. Compara la calidad de pérdida, memoria y generación con las líneas de base de SWA pura y global pura en parámetros iguales.
   En el modelo de proyectos de educación, se realiza la combinación de los niveles 5: 1 de Gemma-3 (5, SWA,1 nivel) en la combinación de los niveles SWA y SWA y los niveles de base de la producción.
4. **Hard.**Implementar la atención diferencial con un aprendiz `λ`En el caso de los equipos de detección de datos, el equipo de detección de datos de detección de datos de datos de detección de datos de datos de detección de datos de datos de detección de datos de datos de detección de datos de datos de detección de datos de detección de datos de detección de datos de datos de detección de datos de detección de datos de detección de datos de detección de datos de detección de datos de detección de datos de detección de datos de detección de datos de detección de datos de detección de datos de detección de datos de detección de datos de detección de datos de detección de datos de detección de datos de detección de datos de detección de datos de detección de datos de detección de datos de detección de datos de detección de datos de detección de datos de detección de datos de detección de datos de detección de datos de detección de datos de detección de datos de detección de datos de detección de datos de detección de datos de detección de datos de detección de datos de datos de detección de datos de datos de datos de detección de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de cuyo de cuyo de cuyo de cuyo cuyo cuyo cuyo cuyo cuyo cuyo cuyo cuyo cuyo cuyo cuyo cu
   En español: " Realizar cada uno tiene aprendizaje "`λ`La diferencia de atención en la tarea de detección de síntomas (en la que se ha realizado un ensayo de detección de interferencias) se ha desarrollado en la base de datos de detección de interferencias.

## Términos clave .

| Term | What people say | What it actually means |
|------|-----------------|-----------------------|
| 术语 | 通俗说法 | 实际含义 |
| Sliding window attention (SWA) | "Local attention" | Each query attends to its last `W` tokens; KV cache shrinks to `O(W)`. |
| 滑动窗口注意力 (SWA) | "局部注意力" | 每个查询关注其最后 `W` 个 token；KV 缓存缩小到 `O(W)`。 |
| Effective receptive field | "How far back the model sees" | In an `L`-layer SWA stack with window `W`, up to `L × W` tokens. |
| 有效感受野 | "模型能看多远" | 在 `L` 层 SWA 堆栈中，窗口 `W`，最多 `L × W` 个 token。 |
| Longformer / BigBird | "Local + global + random" | Sparse patterns with a few always-attending global tokens; early long-context approach. |
| Longformer / BigBird | "局部+全局+随机" | 带少量始终关注的全局 token 的稀疏模式；早期长上下文方案。 |
| Native Sparse Attention | "DeepSeek's kernel trick" | Learn block-level sparsity; skip zero blocks at the kernel level while keeping quality. |
| 原生稀疏注意力 | "DeepSeek 的内核技巧" | 学习块级稀疏性；在内核级别跳过零块同时保持质量。 |
| Differential attention | "Two maps, one subtracts" | DIFF Transformer: subtract a learned `λ` times a second attention map from the first to cancel attention sinks. |
| 差分注意力 | "两个图，一个相减" | DIFF Transformer：用第一个注意力图减去学习 `λ` 倍的第二个注意力图，消除注意力汇聚。 |
| Attention sink | "Weight bleeds to token 0" | Softmax normalization forces rows to sum to 1; uninformative queries dump weight on position 0. |
| 注意力汇聚 | "权重流向 token 0" | Softmax 归一化迫使每行总和为 1；无信息查询将权重倾倒到位置 0。 |
| FlexAttention | "Mask-as-Python" | PyTorch 2.5+ API that compiles arbitrary mask functions into FlashAttention-shape kernels. |
| FlexAttention | "掩码即 Python" | PyTorch 2.5+ API，将任意掩码函数编译为 FlashAttention 形式的内核。 |
| Layer type mix | "5:1 SWA-to-global" | Interleave sparse and full attention layers in a stack to keep quality at lower memory. |
| 层类型混合 | "5:1 SWA 与全局" | 在堆栈中交替使用稀疏和全注意力层，以较低内存保持质量。 |

## Más Leer más Leer más

- [Beltagy, Peters, Cohan (2020). Longformer: The Long-Document Transformer](https://arxiv.org/abs/2004.05150) el papel de fichaje global + ventana de deslizamiento canónica.
  Traducción:Longformer 论文, clásico de la ventana de movimiento + 方案 全局代币
- [Zaheer et al. (2020). Big Bird: Transformers for Longer Sequences](https://arxiv.org/abs/2007.14062) local + global + aleatorio.
  En inglés, el nombre de la organización se traduce en inglés como "BigBird".
- [Child et al. (2019). Generating Long Sequences with Sparse Transformers](https://arxiv.org/abs/1904.10509) El patrón local+pasado de OpenAI.
  La nueva versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión
- [Gemma Team (2024). Gemma 2: Improving Open Language Models at a Practical Size](https://arxiv.org/abs/2408.00118) la mezcla global de la SWA 1:1.
  Gemma 2 论文,1:1 SWA 与全局混合──
- [Gemma Team (2025). Gemma 3 technical report](https://arxiv.org/abs/2503.19786) la combinación 5:1 con ventana=1024 que ahora es el libro de texto predeterminado.
  El texto de la ley de la lengua inglesa, el texto de la ley de la lengua inglesa, el texto de la ley de la lengua inglesa, el texto de la ley de la lengua inglesa, el texto de la ley de la lengua inglesa, el texto de la ley de la lengua inglesa, el texto de la ley de la lengua inglesa, el texto de la ley de la lengua inglesa, el texto de la ley de la lengua inglesa, el texto de la ley de la lengua inglesa, el texto de la ley de la lengua inglesa, el texto de la ley de la lengua inglesa, el texto de la ley de la lengua inglesa, el texto de la ley de la lengua inglesa, el texto de la ley de la lengua inglesa, el texto de la ley de la lengua inglesa, el texto de la ley de la lengua inglesa, el lengua inglesa, el lengua inglesa, el lengua inglesa y el inglés, se han traducido en inglés, se han traducido en inglés en inglés en inglés en inglés en inglés en inglés en inglés en inglés en inglés en inglés en inglés en inglés en inglés en inglés en inglés en inglés en inglés en inglés en inglés en inglés en inglés en inglés en inglés en inglés en inglés en inglés en inglés en inglés en inglés en inglés en inglés en inglés en inglés en inglés en inglés en inglés en inglés en inglés en inglés en inglés en inglés en inglés en inglés en inglés en inglés en inglés en inglés en inglés en inglés en inglés en inglés en inglés en inglés en inglés en inglés en inglés en inglés en inglés en inglés en inglés en inglés en inglés en inglés en inglés en inglés en inglés en inglés en inglés en inglés en inglés en inglés en inglés en inglés en inglés en inglés en inglés en inglés en inglés en inglés en inglés en inglés en inglés en inglés en inglés en inglés en inglés en inglés en inglés en inglés en inglés en inglés en inglés en inglés en inglés en inglés en inglés en inglés en inglés en inglés en inglés en inglés en inglés en inglés en inglés en inglés en inglés en inglés en inglés en inglés en inglés en inglés en inglés en inglés en inglés en inglés en inglés en inglés en inglés en inglés en inglés en inglés en inglés en inglés en inglés en inglés en inglés en inglés en inglés en inglés en inglés en inglés en inglés en inglés en inglés en inglés en inglés en inglés en inglés en inglés en inglés en inglés.
- [Ye et al. (2024). Differential Transformer](https://arxiv.org/abs/2410.05258) papel transformador DIFF.
  El transformer de diff es un transformer de diff.
- [Yuan et al. (2025). Native Sparse Attention](https://arxiv.org/abs/2502.11089) La atención de la disparidad aprendida de DeepSeek-V3.2.
  El tema es el tema de la investigación de la investigación.
- [PyTorch — FlexAttention blog and docs](https://pytorch.org/blog/flexattention/) Referencia de API para el patrón de máscara como llamada en Use It.
  En el caso de las redes sociales, el usuario puede utilizar la aplicación de la red de datos de la red de Internet.
