# Encriptación de posición  Sinusoidal, RoPE, ALiBi
# 位置编码  正弦、RoPE、ALiBi

> La atención es invariable en la permutación. "El gato se sentó en el tapicero" y "el gato en el sat" producen la misma salida sin señal de posición. Tres algoritmos la arreglan  cada uno con una apuesta diferente en lo que significa "posición".

> Atención es la siguiente: "El gato se sentó en el tapicero" y "el gato se sentó en el tapicero" en el lugar donde no hay señal de salida.

> **【中文解读】**Transformer 没有位置信息,需要手动注入──RoPE es el método de uso de Llama, ALiBi 支持外推到更长序列──

**Type:** Build | **类型:** 动手
**Language:**¿ Qué pasa ?**语言:**Python
**Prerequisites:** Phase 7 · 02 (Self-Attention), Phase 7 · 03 (Multi-Head Attention) | **前置知识:** 阶段 7 · 02（自注意力），阶段 7 · 03（多头注意力）
**Time:** ~45 minutes | **时间:** ~45 分钟

## El problema es la introducción del problema

La atención a escala de producto de punto es ciega al orden.`softmax(Q K^T / √d) V`Se calcula a partir de similitudes parecidas.`X`No hay nada dentro de la atención que se preocupe por la posición.

> 缩放点积注意力是顺序无关的──注意力矩阵 `softmax(Q K^T / √d) V`Por el hecho de que la similitud se calcula y viene.`X`La línea, la salida y la salida se alteran de la misma manera.

Para el lenguaje, código, audio, video  cualquier cosa donde el orden lleva un significado  es fatal.

> En el modelo de palabras esto no es un error. Pero para el lenguaje, código, audio, vídeo, cualquier orden que lleve un significado es fatal.

La solución es inyectar posición en los embeddings de alguna manera.

> El método de reparación es de alguna manera se injectará la posición en el emplazamiento.

1. **Absolute sinusoidal**(Vaswani 2017). Añadir `sin/cos`Es simple, sin aprendizaje, extrapola poco más allá de las longitudes entrenadas.
   **绝对正弦编码**(Vaswani 2017):`sin/cos`Adición a la incorporación.

2. **RoPE — Rotary Position Embeddings**(Su 2021). Rotar los vectores Q y K por un ángulo proporcional a la posición. Encodifica * posición relativa* directamente en el producto de puntos. Dominante en 2026.
   **RoPE — 旋转位置嵌入**(Su 2021) ・ en función de la posición en la posición de la posición en la posición de la posición en la posición de la posición en la posición de la posición en la posición de la posición en la posición de la posición en la posición de la posición en la posición de la posición en la posición de la posición en la posición de la posición en la posición de la posición en la posición de la posición en la posición de la posición en la posición de la posición en la posición de la posición en la posición de la posición en la posición de la posición en la posición de la posición en la posición de la posición en la posición de la posición en la posición en la posición de la posición en la posición de la posición en la posición de la posición en la posición de la posición en la posición de la posición en la posición de la posición en la posición de la posición en la posición de la posición en la posición de la posición en la posición de la posición en la posición de la posición en la posición de la posición en la posición de la posición en la posición de la posición en la posición de la posición en la posición de la posición en la posición de la posición en la posición en la posición de la posición en la posición en la posición en la posición de la posición en la posición en la posición de la posición en la posición en la posición en la posición en la posición en la posición en la posición en la posición en la posición en la posición en la posición en la posición en la posición en la posición en la posición en la posición en la posición en la posición en la posición en la posición en la posición en la posición en la posición en la posición en la posición en la posición en la posición en la posición en la posición en la posición en la posición en la posición en la posición en el que la posición en el que se eje en el que se eje en el que se eje en el que se eje en el eje en el eje en el eje en el eje en el eje en el eje en el eje en el eje en el eje en el eje en el eje en el eje en el eje en el eje en el eje en el eje en el eje en el eje eje en el eje eje eje eje eje eje eje eje eje eje eje eje eje eje eje eje eje eje eje eje eje eje eje eje eje eje eje eje eje eje eje eje eje eje eje eje eje eje eje eje eje eje eje eje eje eje eje eje eje eje eje eje eje eje eje eje eje eje eje eje eje eje eje eje eje eje eje

3. **ALiBi — Attention with Linear Biases**(Presiones 2022). Salta los embebidos por completo; añade una penalización lineal por cabeza a las puntuaciones de atención basadas en la distancia. Excelente extrapolación de longitud.
   **ALiBi — 带线性偏置的注意力**(Presiones 2022): ¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡

A partir de 2026, prácticamente todos los modelos abiertos fronterizos usan RoPE: Llama 2/3/4, Qwen 2/3, Mistral, Mixtral, DeepSeek-V3, Kimi. Un puñado de modelos de contexto largo usan ALiBi o sus variantes modernas.

> 截至2026年, básicamente cada modelo de primera línea de código abierto utiliza RoPE:Llama 2/3/4、Qwen 2/3、Mistral、Mixtral、DeepSeek-V3、Kimi。

> **【中文解读】**El sistema de codificación de tres posiciones representa tres épocas: 1) el código de cuerdas de la línea de cuerdas de la línea de cuerdas de la línea de cuerdas de cuerdas de cuerdas de cuerdas de cuerdas de cuerdas de cuerdas de cuerdas de cuerdas de cuerdas de cuerdas de cuerdas de cuerdas de cuerdas de cuerdas de cuerdas de cuerdas de cuerdas de cuerdas de cuerdas de cuerdas de cuerdas de cuerdas de cuerdas de cuerdas de cuerdas de cuerdas de cuerdas de cuerdas de cuerdas de cuerdas de cuerdas de cuerdas de cuerdas de cuerdas de cuerdas de cuerdas de cuerdas de cuerdas de cuerdas de cuerdas de cuerdas de cuerdas de cuerdas de cuerdas de cuerdas de cuerdas de cuerdas de cuerdas de cuerdas de cuerdas de cuerdas de cuerdas de cuerdas de cuerdas de cuerdas de cuerdas de cuerdas de cuerdas de cuerdas de cuerdas de cuerdas de cuerdas de cuerdas de cuerdas de cuerdas de cuerdas de cuerdas de cuerdas de cuerdas de cuerdas de cuerdas de cuerdas de cuerdas de cuerdas de cuerdas de cuerdas de cuerdas de cuerdas de cuerdas de cuerdas de cuerdas de cuentas de cuentas de cuerdas de cuentas de cuentas de cuentas de cuentas de cuentas de cuentas de cuentas de cuentas de cuentas de cuentas de cuentas de cuentas de cuentas de cuentas de cuentas de cuentas de cuentas de cuentas de cuentas de cuentas de cuentas de cuentas de cuentas de cuentas de cuentas de cuentas de cuentas de cuentas de cuentas de cuentas de cuentas de cuentas de cuentas de cuentas de cuentas de cuentas de cuentas de cuentas de cuentas de cuentas de cuentas de cuentas de cuentas de cuentas de cuentas de cuentas de cuentas de cuentas de cuentas de cuentas de cuentas de cuentas de cuentas de cuentas de cuentas de cuentas de cuentas de cuentas de cuentas de cuentas de cuentas de cuentas de cuentas de cuentas de cuentas de cuentas de cuentas de cuentas de cuentas de cuentas de cuentas de cuentas de cuentas de

## El concepto central.

![Sinusoidal absolute vs RoPE rotations vs ALiBi distance bias](../assets/positional-encoding.svg)

### Absoluto sinusoidal.

Precomputa una matriz fija `PE`de forma`(max_len, d_model)`¿Qué es esto ?

> 预计算一个固定矩阵 `PE`, forma `(max_len, d_model)`¿Qué es esto ?

```
PE[pos, 2i]   = sin(pos / 10000^(2i / d_model))
PE[pos, 2i+1] = cos(pos / 10000^(2i / d_model))
```

Entonces ...`X' = X + PE[:N]`Cada dimensión es un sinusoide con una frecuencia diferente. El modelo aprende a leer la posición del patrón de fase.`max_len`: nada le dijo al modelo lo que pasaba en la posición 2048 cuando sólo veía posiciones 02047.

> Entonces en la atención`X' = X + PE[:N]`◊ cada dimensión es de diferentes frecuencias de los movimientos de la cuerda.`max_len`Out of Effect: el modelo sólo ha visto la posición 0-2047 时, nada le dice lo que va a suceder en la posición 2048 

### RoPE gira en su posición

Gira los vectores Q y K (no embeddings). Para un par de dimensiones `(2i, 2i+1)`¿Qué es esto ?

> 旋转 Q 和 K 向量(no está enmembrado)`(2i, 2i+1)`¿Qué es esto ?

```
[q'_2i    ]   [ cos(pos·θ_i)  -sin(pos·θ_i) ] [q_2i   ]
[q'_2i+1  ] = [ sin(pos·θ_i)   cos(pos·θ_i) ] [q_2i+1 ]

θ_i = base^(-2i / d_head),  base = 10000 by default
```

Aplicar la misma rotación a las teclas con posición `pos_k`. El producto de puntos `q'_m · k'_n`se convierte en una función de `(m - n)`Sólo.**the attention score depends only on the relative distance**, aunque la rotación estaba bloqueada en posiciones absolutas.

> Para la aplicación de la clave`pos_k`De la misma rotación.`q'_m · k'_n` convirtiéndose sólo `(m - n)`La función es:**注意力分数只取决于相对距离**Incluso si el giro se basa en la posición absoluta...

> **【中文解读】**La raciocina del RoPE: aunque el ángulo de rotación se basa en la posición absoluta, el punto de Q·K depende solo de la distancia relativa (m-n) ―― esto significa que el modelo natural se encuentra en relación con la posición.

> **【拓展：RoPE 在 Llama 3 中的长上下文扩展】**Llama 3 通过 YaRN(Y otro método de extensión RoPEN) se extenderá de 8K a 128K. El pensamiento central es ajustar la frecuencia básica de RoPE, haciendo que la alta frecuencia mantenga la resolución original, la baja frecuencia mantenga el valor de inserción. Esta estrategia de "partición de la dimensión" mantiene la percepción de la posición exacta de la distancia corta, y también expande la capacidad de extracción de la distancia larga.

Extender el RoPE: `base`El Llama 3 se extendió de 8K a 128K de esta manera.

> 扩展 RoPE:`base`Se puede acortar a la siguiente siguiente instrucción (en el caso de la Llama 3 es así desde la 8K hasta la 128K).

### ¡Alibí! ¡Toma la atención con desviación lineal!

Salta el truco de incrustación.

> 跳过嵌入技巧──直接偏置注意力分数:

```
attn_score[i, j] = (q_i · k_j) / √d  -  m_h · |i - j|
```

¿ Dónde ?`m_h`es una pendiente específica de la cabeza (por ejemplo `1 / 2^(8·h/H)`Los tokens más cercanos se incrementan; los tokens más lejanos se penalizan. No hay costo de tiempo de entrenamiento. El documento muestra que la extrapolación de longitud supera sinusoidal y coincide con el RoPE en su longitud entrenada original.

> Entre ellos `m_h`Es un tipo específico de inclinación de la cabeza.`1 / 2^(8·h/H)`Los ejemplos de la serie de ensayos de la serie de ensayos de la serie de ensayos de la serie de ensayos de la serie de ensayos de la serie de ensayos de la serie de ensayos de la serie de ensayos de la serie de ensayos de la serie de ensayos de la serie de ensayos de la serie de ensayos de la serie de ensayos de la serie de ensayos de la serie de ensayos de la serie de ensayos de la serie de ensayos de la serie de ensayos de la serie de ensayos de la serie de ensayos de la serie de ensayos de la serie de ensayos de la serie de ensayos de la serie de ensayos de la serie de ensayos de la serie de ensayos de la serie de ensayos de la serie de ensayos de la serie de ensayos de ensayos de la serie de ensayos de la serie de ensayos de ensayos de la serie de ensayos de ensayos de la serie de ensayos de ensayos de la serie de ensayos de ensayos de ensayos de la serie de ensayos de ensayos de ensayos de ensayos de ensayos de ensayos de ensayos de ensayos de ensayos de ensayos de ensayos de ensayos de ensayos de ensayos de ensayos de ensayos de ensayos de ensayos de ensayos de ensayos de ensayos de ensayos de ensayos de ensayos de ensayos de ensayos de ensayos de ensayos de ensayos de ensayos de ensayos de ensayos de ensayos de ensayos de ensayos de ensayos de ensayos de ensayos de ensayos de ensayos de ensayos de ensayos de ensayos de ensayos de ensayos de ensayos de ensayos de ensayos de ensayos de ensayos de ensayos de ensayos de ensayos de ensayos de ensayos de ensayos de ensayos de ensayos de ensayos de ensayos de ensayos de ensayos de ensayos de ensayos de ensayos de ensayos de ensayos de ensayos de ensayos de ensayos de ensayos de ensayos de ensayos de ensayos de ensayos de ensayos de que no ensayos de ensayos de ensayos de ensayos de ensayos de ensayos de ensayos de que no ensayos de que no ensayos de que no ensayos de que no se cumplidos en ensayos de que no sean más .

### ¿Qué elegir en 2026?

| Variant / 变体 | Extrapolation / 外推能力 | Training cost / 训练成本 | Used by / 使用者 |
|---------|---------------|---------------|---------|
| Absolute sinusoidal / 绝对正弦编码 | poor / 差 | free / 免费 | original transformer, early BERT |
| Learned absolute / 学习式绝对编码 | none / 无 | tiny / 微小 | GPT-2, GPT-3 |
| RoPE | good with scaling / 良好（带缩放） | free / 免费 | Llama 2/3/4, Qwen 2/3, Mistral, DeepSeek-V3, Kimi |
| RoPE + YaRN | excellent / 优秀 | fine-tune stage / 微调阶段 | Qwen2-1M, Llama 3.1 128K |
| ALiBi | excellent / 优秀 | free / 免费 | BLOOM, MPT, Baichuan |

RoPE ganó porque atrajo la atención sin cambiar la arquitectura, codifica la posición relativa y su`base`El hiperparámetro da un botón limpio para ajustar el contexto largo.

> RoPE 胜出 es porque no necesita cambiar la estructura, es decir, puede insertar atención, codificar en la posición relativa, y su`base`La superparámetro por el tiempo de la siguiente pequeña modificación proporciona una clara regulación de la rotación.

> **【中文解读】**La elección de la codificación de la posición 2026 es muy clara: el nuevo proyecto es un RoPE por defecto. No cambia la estructura, la codificación en relación con la posición, y a través de la base, los parámetros proporcionan un camino claro de la codificación de la posición. Sólo en el extremo extremo de la situación se puede considerar la ALiBi.

> **【拓展：位置编码对长上下文 RAG 的影响】**En el sistema RAG, el código de posición afecta directamente a la capacidad de procesamiento de archivos. RoPE + YaRN permite que Llama 3 pueda procesar los tokens de 128K en su subyacente, lo que significa que puede procesar una sola vez unos 300 páginas de documentos. La elección del programa de codificación de posición determina si el sistema RAG necesita estrategias de bloques complejas.
```figure
rope-explorer
```

## Construye el mismo

## Construye y realiza.

### Paso 1: codificación sinusoidal. Paso 1: codificación de la cuerda.

¿ Qué ?`code/main.py`Un cálculo de 4 líneas:

> 参见 `code/main.py`△4 行计算:

```python
def sinusoidal(N, d):
    pe = [[0.0] * d for _ in range(N)]
    for pos in range(N):
        for i in range(d // 2):
            theta = pos / (10000 ** (2 * i / d))
            pe[pos][2 * i]     = math.sin(theta)
            pe[pos][2 * i + 1] = math.cos(theta)
    return pe
```

Añadir esto a la matriz de incorporación antes de la primera capa de atención.

> En la primera capa de atención se añadirá a la matriz de inserción.

### Paso 2: RoPE aplicado a Q, K. Paso 2: RoPE  aplicado a Q ̊K

RoPE opera en el lugar en Q y K. Para cada par de dimmers:

> RoPE para Q y K operaciones de tierra originarias.

```python
def apply_rope(x, pos, base=10000):
    d = len(x)
    out = list(x)
    for i in range(d // 2):
        theta = pos / (base ** (2 * i / d))
        c, s = math.cos(theta), math.sin(theta)
        a, b = x[2 * i], x[2 * i + 1]
        out[2 * i]     = a * c - b * s
        out[2 * i + 1] = a * s + b * c
    return out
```

Crucial: aplicar la misma función a Q en posición `m`y K en posición `n`Su producto de puntos recoge un`cos((m-n)·θ_i)`La atención aprende la posición relativa de forma gratuita.

> 关键: por la posición `m`de Q y posición `n`Los puntos de cada posicionamiento se acumulan en la misma función.`cos((m-n)·θ_i)`Porque... la atención libre ha aprendido a la posición relativa...

> **【中文解读】**El núcleo de realización de la RoPE: hacer la rotación en relación con la posición de cada uno de las dimensiones de Q y K (2i, 2i+1) ⋅ angular de rotación en relación con la posición, por lo que los puntos de Q_m · K_n aparecen en los conjuntos cosm (m-n) ⋅theta, naturalmente codificados en relación a la distancia―

### Paso 3: AlíBi pendientes y sesgos  Paso 3: AlíBi  inclinado y desviado

```python
def alibi_bias(n_heads, seq_len):
    # slope_h = 2 ** (-8 * h / n_heads) for h = 1..n_heads
    slopes = [2 ** (-8 * (h + 1) / n_heads) for h in range(n_heads)]
    bias = []
    for m in slopes:
        row = [[-m * abs(i - j) for j in range(seq_len)] for i in range(seq_len)]
        bias.append(row)
    return bias  # add to attention scores before softmax
```

Añadir`bias[h]`a la `(seq_len, seq_len)`Matriz de puntaje de atención de la cabeza `h`, luego softmax.

> ¿ Qué ?`bias[h]`¡ ¡ ¡ ¡ ¡ ¡ ¡ ¡ ¡ ¡ ¡ ¡ ¡ ¡ ¡ ¡ ¡ ¡ ¡ ¡ ¡ ¡ ¡ ¡ ¡ ¡ ¡ ¡ ¡ ¡ ¡ ¡ ¡ ¡ ¡ ¡ ¡ ¡ ¡ ¡ ¡ ¡ ¡ ¡ ¡ ¡ ¡ ¡ ¡ ¡ ¡ ¡ ¡ ¡ ¡ ¡ ¡ ¡ ¡ ¡ ¡ ¡ ¡ ¡ ¡ ¡ ¡ ¡ ¡ ¡ ¡ ¡ ¡ ¡ ¡ ¡ ¡ ¡ ¡ ¡ ¡ ¡ ¡ ¡ ¡ ¡ ¡ ¡ ¡ ¡ ¡ ¡ ¡ ¡ ¡ ¡ ¡ ¡ ¡ ¡ ¡ ¡ ¡ ¡ ¡ ¡ ¡ ¡ ¡ ¡ ¡ ¡ ¡ ¡ ¡ ¡ ¡ ¡ ¡ ¡ ¡ ¡ ¡ ¡ ¡ ¡ ¡ ¡ ¡ ¡ ¡ ¡ ¡ ¡ ¡ ¡ ¡ ¡ ¡ ¡ ¡ ¡ ¡ ¡ ¡ ¡ ¡ ¡ ¡ ¡ ¡ ¡ ¡ ¡ ¡ ¡ ¡ ¡ ¡ ¡ ¡ ¡ ¡ ¡ ¡ ¡ ¡ ¡ ¡ ¡ ¡ ¡ ¡ ¡ ¡ ¡ ¡ ¡ ¡ ¡ ¡ ¡ ¡ ¡ ¡ ¡ ¡ ¡ ¡ ¡ ¡ ¡ ¡ ¡ ¡ ¡ ¡ ¡ ¡ ¡ ¡ ¡ ¡ ¡ ¡ ¡ ¡ ¡ ¡ ¡ ¡ ¡ ¡ ¡ ¡ ¡ ¡ ¡ ¡ ¡ ¡ ¡ ¡ ¡ ¡ ¡ ¡ ¡ ¡ ¡ ¡ ¡ ¡ ¡ ¡ ¡ ¡ ¡ ¡ ¡ ¡ ¡ ¡ ¡ ¡ ¡ ¡ ¡ ¡ ¡ ¡ ¡ ¡ ¡ ¡ ¡ ¡ ¡ ¡ ¡ ¡ ¡ ¡ ¡ ¡ ¡ ¡ ¡ ¡ ¡ ¡ ¡ ¡ ¡ ¡ ¡ ¡ ¡ ¡ ¡ ¡ ¡ ¡ ¡ ¡ ¡ ¡ ¡ ¡ ¡ ¡ ¡ ¡ ¡ ¡ ¡ ¡ ¡ ¡ ¡ ¡ ¡ ¡ ¡ ¡ ¡ ¡ ¡ ¡ ¡ ¡ ¡ ¡ ¡ ¡ ¡ ¡ ¡ ¡ ¡ ¡ ¡ ¡ ¡ ¡ ¡ ¡ ¡ ¡ ¡ ¡ ¡ ¡ ¡ ¡ ¡ ¡ ¡ ¡ ¡ ¡ ¡ ¡ ¡ ¡ ¡ ¡ ¡ ¡ ¡ ¡ ¡ ¡ ¡ ¡ ¡ ¡ ¡ ¡ ¡ ¡ ¡ ¡ ¡ ¡ ¡ ¡ ¡ ¡ ¡ ¡ ¡ ¡ ¡ ¡ ¡ ¡ ¡ ¡ ¡ ¡ ¡ ¡ ¡ ¡ ¡ ¡ ¡ ¡ ¡ ¡ ¡ ¡ ¡ ¡ ¡ ¡ ¡ ¡ ¡ ¡ ¡ ¡ ¡ ¡ ¡ ¡ ¡ ¡ ¡ ¡ ¡ ¡ ¡ ¡ ¡ ¡ ¡ ¡ ¡ ¡ ¡ ¡ ¡ ¡ ¡ ¡ ¡ ¡ ¡ ¡ ¡ ¡ ¡ ¡ ¡ ¡ ¡ ¡ ¡ ¡ ¡ ¡ ¡ ¡ ¡ ¡ ¡ ¡ ¡ ¡ ¡ ¡ ¡ ¡ ¡ ¡ ¡ ¡ ¡ ¡ ¡ ¡ ¡ ¡ ¡ ¡ ¡ ¡ ¡ ¡ ¡ ¡ ¡ ¡ ¡ ¡ ¡ ¡ ¡ ¡ ¡ ¡ ¡ ¡ ¡ ¡ ¡ ¡ ¡ ¡ ¡ ¡ ¡ ¡ ¡ ¡ ¡ ¡ ¡ ¡ ¡ ¡ ¡ ¡ ¡ ¡ ¡ ¡ ¡`h`de la `(seq_len, seq_len)`Atención a la matriz, luego suave.

### Paso 4: Verificar la propiedad de distancia relativa de RoPE. Paso 4: Verificar la propiedad de distancia relativa de RoPE.

Escoge dos vectores aleatorios .`a, b`- Gira por el .`(pos_a, pos_b)`Entonces por`(pos_a + k, pos_b + k)`. ambos productos de puntos deben coincidir dentro del error de punto flotante. Esa propiedad es el punto entero de RoPE  es invariante al desvio absoluto, sólo la brecha relativa importa.

> 选择两个随机向量 `a, b`。 Usado `(pos_a, pos_b)`Luego lo usamos.`(pos_a + k, pos_b + k)`旋转── dos puntos deben coincidir en el rango de los puntos de error. Esta característica es el significado total de RoPE.

> **【拓展：位置编码的历史演进】**Desde Vaswani, el código de la línea justa absoluta de 2017 hasta GPT-2/3 de la posición de aprendizaje, y hasta RoPE, el 2021 y el ALiBi, el 2022), el código de posición ha experimentado un cambio de paradigma de "posición justa" a "posición relativa". El éxito del RoPE es que no cambia la estructura de atención, directamente en la posición relativa del código en Q/K, al mismo tiempo que proporciona una ruta clara para la expansión de la siguiente secuencia.

## Usalo con el marco de ejecución

PyTorch 2.5+ envía a los servicios públicos de RoPE en `torch.nn.functional`La mayoría de los códigos de producción usan`flash_attn`o `xformers`en el que se aplique RoPE dentro del núcleo de atención.

> PyTorch 2.5+ en`torch.nn.functional`Encluso RoPE 工具──la mayoría de la producción utiliza código `flash_attn`O `xformers`, en el que el RoPE en la aplicación interna de la atención intèrna.

```python
from transformers import AutoModel
model = AutoModel.from_pretrained("meta-llama/Llama-3.2-3B")
# model.config.rope_scaling → {"type": "yarn", "factor": 32.0, "original_max_position_embeddings": 8192}
```

**Long-context tricks in 2026:**

> **2026 年的长上下文技巧：**

- **NTK-aware interpolation.**Reescalado`base`¿ Qué ?`base * (scale_factor)^(d/(d-2))`cuando se extiende de 4K a 16K+.
  **NTK-aware 插值。**Cuando se expanda de 4K a 16K +, se`base`重新缩放为 `base * (scale_factor)^(d/(d-2))`¿Qué es eso?
- **YaRN.**Interpolación más inteligente que preserva la entropía de la atención en contextos largos.
  **YaRN。**Más inteligencia, mantener la atención en el texto siguiente.
- **LongRoPE.**El método 2024 de Microsoft que utiliza la búsqueda evolutiva para seleccionar factores de escala por dimensión.
  **LongRoPE。**Microsoft 2024 años de método, usando la búsqueda de evolución seleccionar por dimensión reducido factor.
- **Position interpolation + fine-tuning.**Sólo reducir las posiciones por el factor de extensión y ajustar a 15B tokens. Sorprendentemente eficaz.
  **位置插值 + 微调。**Sólo se necesita en función de la expansión de la posición reducida y la reducción de 1-5B de los tokens.

## Envíe el producto .

¿ Qué ?`outputs/skill-positional-encoding-picker.md`. La habilidad elige una estrategia de codificación para un nuevo modelo dada la longitud del contexto objetivo, las necesidades de extrapolación y el presupuesto de formación.

> 参见 `outputs/skill-positional-encoding-picker.md` Esta habilidad se utiliza para seleccionar estrategias de codificación de nuevos modelos, para determinar la longitud de la siguiente definición, la necesidad de desarrollo y el presupuesto de entrenamiento.

## Los ejercicios.

1. **Easy / 简单。**Traza el senoideal .`PE`matriz como mapa de calor para `max_len=512, d=128`Confirmar el patrón de "las franjas se amplían a medida que crece el índice de dimensiones".
   ¿Qué es eso ?`PE`矩阵绘制为 `max_len=512, d=128`La tendencia de la industria de la información es la de la industria de la información.

2. **Medium / 中等。**Implemente una escalación de RoPE consciente de NTK. Entrenar un pequeño LM en secuencias de longitud 256, luego probar en longitud 1024 con y sin escalación. Medir la perplejidad.
   实现 NTK-consciente RoPE 缩放── en la longitud 256 entrenar una LM de tipo pequeño en la secuencia, luego en el caso de tener una reducción y sin reducción, probar la longitud 1024── medir la confusión─

3. **Hard / 困难。**Implemente ALiBi y RoPE en el mismo módulo de atención. Entrenar un transformador de 4 capas en una tarea de copia con secuencias de longitud 512. Extrapolar a 2048 en el momento de la prueba. Comparar degradación.
   En el mismo módulo de atención se realiza ALiBi y RoPE. En la secuencia de longitud 512 se entrena a una misión de replicación de un transformador de 4 niveles.

## Términos clave .

| Term | What people say / 人们怎么说 | What it actually means / 实际含义 |
|------|------------------------------|----------------------------------|
| Positional encoding / 位置编码 | "Tells attention about order" / "告诉注意力顺序" | Any signal added to embeddings or attention that encodes position. 添加到嵌入或注意力中编码位置的任何信号。 |
| Sinusoidal / 正弦编码 | "The original one" / "原始的那种" | `sin/cos` at geometric frequencies added to embeddings; doesn't extrapolate. 以几何频率加到嵌入上的 `sin/cos`；不能外推。 |
| RoPE | "Rotary embeddings" / "旋转嵌入" | Rotate Q, K by position-dependent angle; dot product encodes relative distance. 按位置相关角度旋转 Q、K；点积编码相对距离。 |
| ALiBi | "Linear bias trick" / "线性偏置技巧" | Add `-m·|i-j|` to attention scores; no embedding needed, great extrapolation. 向注意力分数添加 `-m·|i-j|`；无需嵌入，出色的外推。 |
| base | "RoPE's knob" / "RoPE 的旋钮" | The frequency scaler in RoPE; increase to extend context at inference. RoPE 中的频率缩放器；增大以在推理时扩展上下文。 |
| NTK-aware | "A RoPE scaling trick" / "RoPE 缩放技巧" | Rescale `base` so high-frequency dims aren't squeezed when context expands. 重新缩放 `base` 使高频维度在上下文扩展时不被挤压。 |
| YaRN | "The fancy one" / "高级的那种" | Per-dimension interpolation+extrapolation that preserves attention entropy. 保留注意力熵的每维度插值+外推。 |
| Extrapolation / 外推 | "Works beyond trained length" / "超过训练长度还能用" | Can the position scheme serve correct output past `max_len` seen in training? 位置方案能否在训练中见过的 `max_len` 之后提供正确的输出？ |

## Más Leer más Leer más

- [Vaswani et al. (2017). Attention Is All You Need §3.5](https://arxiv.org/abs/1706.03762) original sinusoidal.
  Vaswani 等人(2017)  原始正弦编码──

- [Su et al. (2021). RoFormer: Enhanced Transformer with Rotary Position Embedding](https://arxiv.org/abs/2104.09864) Papel de papel de papel rope.
  Su 等人(2021)  RoPE 论文。

- [Press, Smith, Lewis (2021). Train Short, Test Long: Attention with Linear Biases Enables Input Length Extrapolation](https://arxiv.org/abs/2108.12409) ALiBi.
  Prensa, Smith, Lewis... 2021... ¡Aquí está!

- [Peng et al. (2023). YaRN: Efficient Context Window Extension of Large Language Models](https://arxiv.org/abs/2309.00071) el estado de la técnica de escalado RoPE.
  Peng 等人(2023)  Ultimas avanzadas de RoPE 缩放──

- [Chen et al. (2023). Extending Context Window of Large Language Models via Positional Interpolation](https://arxiv.org/abs/2306.15595) Meta's Llama 2 papel de largo contexto.
  Chen 等人(2023)  Meta's Llama 2 长上下文论文。

- [Ding et al. (2024). LongRoPE: Extending LLM Context Window Beyond 2 Million Tokens](https://arxiv.org/abs/2402.13753) el método de Microsoft utilizado por Phi-3-Long.
  Ding 等人(2024)  Microsoft's method, fue utilizado por Phi-3-Long.

- [HuggingFace Transformers — `modeling_rope_utils.py`](https://github.com/huggingface/transformers/blob/main/src/transformers/modeling_rope_utils.py) Implementaciones de cada régimen de escalado de RoPE en el nivel de producción.
  EmbracingFace Transformers  Todos los RoPE  Encrementamiento de la producción de programas de realización.
