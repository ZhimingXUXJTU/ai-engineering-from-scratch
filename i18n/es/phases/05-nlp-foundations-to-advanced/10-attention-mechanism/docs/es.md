# Mecanismo de atención La ruptura de la máquina de atención La ruptura central del transformador

> El decodificador deja de mirar a un resumen comprimido y comienza a mirar toda la fuente.
> El descifrador deja de mirar el resumen, comienza a mirar hacia todo el origen.

> **【中文解读】**El mecanismo de atención hace que el modelo se preocupe en la entrada de los componentes relacionados.

**Type:** Build | **类型:** 动手
**Languages:** Python | **语言:** Python
**Prerequisites:** Phase 5 · 09 (Sequence-to-Sequence Models) | **前置知识:** Phase 5 · 09（序列到序列模型）
**Time:** ~45 minutes | **时间:** ~45 分钟

## El problema es la introducción del problema

La lección 09 terminó con un fallo medido. Un codificador-decodificador GRU entrenado en una tarea de copia de juguete va desde una precisión del 89% en longitud 5 a casi la probabilidad en longitud 80. La razón es estructural, no un error de entrenamiento: cada bit de información que el codificador recolecta tiene que encajar en un estado oculto de tamaño fijo, y el decodificador nunca ve nada más.

> Sección 09  Clasificación final con un fracaso de una medida. GRU codificador-descifrador entrenado en tareas de copia de juguetes en longitud 5  89%  precisión, en longitud 80  cerca de la oportunidad. La razón es estructural, no un error de entrenamiento: cada punto de información de la recopilación del codificador debe ser introducido en un estado oculto de tamaño fijo, el descifrador no ve nada más.

Bahdanau, Cho y Bengio publicaron una solución de tres líneas en 2014. En lugar de darle al decodificador solo el estado final del codificador, mantenga cada estado del codificador.`i`Ese promedio ponderado es el contexto, y cambia cada paso del decodificador.

> Bahdanau、Cho 和 Bengio publicó en 2014 una tercera edición. No solo le dio al descifrador el estado final del codificador, sino que mantuvo el estado de cada codificador.`i`"Este aumento de la media es en el texto siguiente, cambia en cada paso del decodificador.

Esa es la idea. Los transformadores la extendieron. La autoatención la aplicó a una sola secuencia. La atención multi-cabeza la corrió en paralelo. Pero la versión de 2014 ya rompió el cuello de botella, y una vez que la tienes, el eje central de los transformadores es la ingeniería, no conceptual.

> Esa es la idea completa. Transformer la ha ampliado. La propia atención la aplicará a un solo proceso.

## El concepto central.

> **【中文解读】**Este capítulo presenta los conceptos y teorías básicos. La comprensión de estos conceptos es el prerrequisito de la realización posterior de la actividad, y también el conocimiento de los puntos de alta frecuencia de la entrevista y la práctica de la ingeniería.

![Bahdanau attention: decoder queries all encoder states](../assets/attention.svg)

En cada paso del decodificador `t`¿Qué es esto ?

> En cada paso de la codificación`t`¿Qué es esto ?

1. Utilice el estado oculto del decodificador anterior `s_{t-1}`como un **query**¿ Qué ?
2. Escóralo contra cada estado oculto del codificador .`h_1, ..., h_T`Un escalar por posición de codificador.
3. Softaxe las puntuaciones para obtener pesas de atención `α_{t,1}, ..., α_{t,T}`que la suma es de 1.
4. Vector de contexto `c_t = Σ α_{t,i} * h_i`- Media ponderada de estados de codificación.
5. El descifrador toma `c_t`más el token de salida anterior, produce el siguiente token.
   1. Usar un descifrador estado oculto`s_{t-1}` Como**查询（Query）**¿Qué es eso?
   2. Lo ocultará con cada codificador.`h_1, ..., h_T`打分── cada codificador ubica una etiqueta──
   3. Para el porcentaje hacer suave max  obtener el peso de la atención `α_{t,1}, ..., α_{t,T}`, en general para 1
   4. 上下文向量   en el que se encuentra el`c_t = Σ α_{t,i} * h_i`◊ el estado del codificador aumenta su promedio.
   5. ¿ Qué es eso ?`c_t`Además de un token de salida anterior, generar el siguiente token.

El promedio ponderado es el punto. Cuando el decodificador necesita traducir "Je" a "I", pesa el estado del codificador sobre "Je" alto y los otros bajo. Cuando necesita "no", pesa "pas" alto. El vector de contexto remodela cada paso.

> Cuando el desmantelador necesita "Je" 翻译为"I" 时,它对"Je"上的编码器状态权重高,其他低──当需要"not" 时,它对"pas"权重高──上下文向量在每步重塑──

> **【拓展：大语言模型的工程实践】**Desde GPT hasta ChatGPT, el campo de NLP ha experimentado un cambio de paradigma de "cada tarea entrenar un modelo" a "un modelo resolver todas las tareas". En el proyecto real, la implementación de LLM necesita considerar los problemas de token 限制,延迟,成本, seguridad etc.

> **【拓展：RAG 与企业知识库】**检索增强生成(RAG) es la estructura más popular de las aplicaciones de IA de las empresas actuales: la consulta de usuarios primero se consulta los documentos relacionados, luego se vuelve a buscar los resultados como respuesta a la pregunta de LLM.

> **【拓展：NLP 的多语言挑战】**En todo el mundo hay más de 7000 idiomas, pero los estudios de PNL se centran principalmente en inglés y en una minoría de idiomas.

## Las formas (la cosa que muerde a todos)

Aquí es donde cada aplicación de atención va mal la primera vez.

> Es el primer lugar donde cada uno de nosotros hace un esfuerzo por lograr el primer error.

| Thing / 对象 | Shape / 形状 | Notes / 说明 |
|-------|-------|-------|
| Encoder hidden states `H` / 编码器隐藏状态 `H` | `(T_enc, d_h)` | If BiLSTM, `d_h = 2 * d_hidden` / 如果是 BiLSTM，`d_h = 2 * d_hidden` |
| Decoder hidden state `s_{t-1}` / 解码器隐藏状态 | `(d_s,)` | One vector / 一个向量 |
| Attention score `e_{t,i}` / 注意力分数 | scalar / 标量 | One per encoder position / 每个编码器位置一个 |
| Attention weight `α_{t,i}` / 注意力权重 | scalar / 标量 | After softmax over all `i` / 对所有 `i` 做 softmax 后 |
| Context vector `c_t` / 上下文向量 | `(d_h,)` | Same shape as an encoder state / 与编码器状态相同形状 |

**Bahdanau (additive) score.** `e_{t,i} = v_α^T * tanh(W_a * s_{t-1} + U_a * h_i)`¿ Qué ?

> **Bahdanau（加性）分数。** `e_{t,i} = v_α^T * tanh(W_a * s_{t-1} + U_a * h_i)`¿Qué es eso?

- `s_{t-1}`tiene forma`(d_s,)`¿ Qué ?`h_i`tiene forma`(d_h,)`¿ Qué ?
- `W_a`tiene forma`(d_attn, d_s)`- ¿ Qué ?`U_a`tiene forma`(d_attn, d_h)`¿ Qué ?
- Su suma dentro del tanh tiene forma .`(d_attn,)`¿ Qué ?
- `v_α`tiene forma`(d_attn,)`. El producto interno con `v_α`Se derrumba hasta una escala.**This is what `v_α` does.**No es magia, es la proyección que convierte un vector de atención-dim en una puntuación escalar.
  - `s_{t-1}`形状为            `(d_s,)`¿ Qué ?`h_i`形状为            `(d_h,)`¿Qué es eso?
  - `W_a`形状为            `(d_attn, d_s)`¿Qué es eso?`U_a`形状为            `(d_attn, d_h)`¿Qué es eso?
  - tanh 内部的和形为 `(d_attn,)`¿Qué es eso?
  - `v_α`形状为            `(d_attn,)` con`v_α`De la cantidad de contenido en el interior.**这就是 `v_α` 的作用。**No es magia. Es proyección de la dimensión de la energía de la luz.

**Luong (multiplicative) score.**Tres variantes:

> **Luong（乘性）分数。**Tres cambios:

- `dot`¿ Qué es esto ?`e_{t,i} = s_t^T * h_i`- Requiere .`d_s == d_h`- No se puede hacer nada si el codificador es bidireccional.
  `dot`¿Qué es esto ?`e_{t,i} = s_t^T * h_i` Requerimiento`d_s == d_h`Si el codificador es doble de la forma de saltar.
- `general`¿ Qué es esto ?`e_{t,i} = s_t^T * W * h_i`con`W`forma`(d_s, d_h)`Elimina la restricción de igual oscuridad.
  `general`¿Qué es esto ?`e_{t,i} = s_t^T * W * h_i`¿ Qué ?`W`形状为            `(d_s, d_h)`❖ Movimiento y control
- `concat`Es raro utilizarlo ya que los dos primeros son más baratos.
  `concat`La forma Bahdanau es de naturaleza más barato, muy poco utilizado.

**One Bahdanau / Luong gotcha worth naming.**Bahdanau utiliza `s_{t-1}`(el estado del decodificador * antes de * generar la palabra actual). Luong utiliza `s_t`(el estado * después *). mezclarlos produce gradientes sutiles y incorrectos que son extremadamente difíciles de deshacer.

> **一个值得注意的 Bahdanau / Luong 陷阱。**Bahdanau                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           `s_{t-1}`(生成当前词*之前*的解码器状态) ――Long 使用 `s_t`(¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡

## Construye y realiza.

> **【中文解读】**Este capítulo a través del código de la implementación de algoritmos centrales de cero. Este método "desde cero" puede ayudar a entender el principio detrás del marco, no se encuentra en la caja negra cuando se encuentran problemas.
```figure
attention-heatmap
```

## Construye el mismo

### Paso 1: atención aditiva (Bahdanau)

```python
import numpy as np


def additive_attention(decoder_state, encoder_states, W_a, U_a, v_a):
    projected_dec = W_a @ decoder_state
    projected_enc = encoder_states @ U_a.T
    combined = np.tanh(projected_enc + projected_dec)
    scores = combined @ v_a
    weights = softmax(scores)
    context = weights @ encoder_states
    return context, weights


def softmax(x):
    x = x - np.max(x)
    e = np.exp(x)
    return e / e.sum()
```

Compruebe sus formas con la tabla de arriba.`encoder_states`tiene forma`(T_enc, d_h)`- ¿ Qué ?`projected_enc`tiene forma`(T_enc, d_attn)`- ¿ Qué ?`projected_dec`tiene forma`(d_attn,)`y las emisiones. `combined`tiene forma`(T_enc, d_attn)`- ¿ Qué ?`scores`tiene forma`(T_enc,)`- ¿ Qué ?`weights`tiene forma`(T_enc,)`- ¿ Qué ?`context`tiene forma`(d_h,)`- Envíalo.

> Controlar el formulario de arriba, comprobar tu forma.`encoder_states`形状为            `(T_enc, d_h)`¿Qué es eso?`projected_enc`形状为            `(T_enc, d_attn)`¿Qué es eso?`projected_dec`形状为            `(d_attn,)`Y se ha propagado.`combined`形状为            `(T_enc, d_attn)`¿Qué es eso?`scores`形状为            `(T_enc,)`¿Qué es eso?`weights`形状为            `(T_enc,)`¿Qué es eso?`context`形状为            `(d_h,)`¡Ya lo he decidido!

### Paso 2: Luong punto y general

```python
def dot_attention(decoder_state, encoder_states):
    scores = encoder_states @ decoder_state
    weights = softmax(scores)
    return weights @ encoder_states, weights


def general_attention(decoder_state, encoder_states, W):
    projected = W.T @ decoder_state
    scores = encoder_states @ projected
    weights = softmax(scores)
    return weights @ encoder_states, weights
```

Es por eso que el papel de Luong aterrizó, la misma precisión en la mayoría de las tareas, mucho menos código.

> Cada uno de los tres líneas. Es el significado de Luong. En la mayoría de las tareas, el código es mucho menor.

### Paso 3: ejemplo numérico trabajado

Dado tres estados de codificación (aproximadamente "cat", "sat", "mat") y un estado de decodificación que se alinea más con el primero, la distribución de la atención se concentra en la posición 0.

> 给定三个编码器状态 ((大致是"cat"、"sat"、"mat") y uno con el primero más alineado con el estado del decodificador, la distribución de la atención se concentra en la posición 0。 Si el estado del decodificador se mueve a la última alineada, la atención se mueve a la posición 2。

```python
H = np.array([
    [1.0, 0.0, 0.2],
    [0.5, 0.5, 0.1],
    [0.1, 0.9, 0.3],
])

s_close_to_cat = np.array([0.9, 0.1, 0.2])
ctx, w = dot_attention(s_close_to_cat, H)
print("weights:", w.round(3))
```

```
weights: [0.464 0.305 0.231]
```

La primera fila gana. Luego mueve el estado del decodificador más cerca del tercer estado del codificador y observa el cambio de pesas. Eso es todo.

> Primera línea vence. Luego se desplaza el estado del decodificador hacia el tercer estado del codificador, observando el cambio de peso.

### Paso 4: por qué este es el puente a los transformadores

Traducir el idioma anterior a Q/K/V:

> 将上的语言翻译为:

- **Query**= estado del decodificador `s_{t-1}`
  **查询（Query）**= 解码器 estado `s_{t-1}`
- **Key**= estados de codificación (lo que anotamos en contra)
  **键（Key）**= 编码器状态(我们用来打分的对象)
- **Value**= estados del codificador (lo que pesamos y suma)
  **值（Value）**= 编码器状态(我们用来加权和的对象)

En la atención clásica, las claves y los valores son lo mismo. La autoatención los separa: se puede consultar una secuencia contra sí misma, con diferentes proyecciones aprendidas para K y V. La atención multi-cabeza la ejecuta en paralelo con diferentes proyecciones aprendidas. Los transformadores apilan la etapa entera muchas veces y dejan caer RNNs.

> En la atención clásica, el clave y el valor son la misma cosa. La atención propia los separará: se puede utilizar diferentes secuencias de proyección de aprendizaje para buscar una secuencia de proyección de aprendizaje como K y V.

Las matemáticas son las mismas, las formas son las mismas, el salto pedagógico de la atención Bahdanau a la atención escalada de producto es principalmente la notación.

> La matemática es la misma. La forma es la misma. De Bahdanau, el salto de atención a la concentración de puntos y puntos de concentración es principalmente un símbolo.

> **【中文解读】**Este capítulo muestra cómo utilizar un marco maduro (como PyTorch、HuggingFace, etc.) para aplicar rápidamente esta tecnología. En los proyectos reales, se realiza con prioridad el uso de un marco experimentado, se pueden reducir errores y mejorar la eficiencia de desarrollo.

> **【拓展：Prompt Engineering 与 LLM 应用】**La ingeniería rápida se ha convertido en la habilidad central de los ingenieros de PNL. Desde la Cero-Shot hasta la Few-Shot, desde la Cadena de Pensamiento hasta la Reacción, diferentes estrategias de sugerencias se aplican a diferentes escenarios.

## Usalo con el marco de ejecución

PyTorch y TensorFlow envían la atención directamente.

> PyTorch y TensorFlow  directamente proporcionar atención.

```python
import torch
import torch.nn as nn

mha = nn.MultiheadAttention(embed_dim=128, num_heads=8, batch_first=True)
query = torch.randn(2, 5, 128)
key = torch.randn(2, 10, 128)
value = torch.randn(2, 10, 128)

output, weights = mha(query, key, value)
print(output.shape, weights.shape)
```

```
torch.Size([2, 5, 128]) torch.Size([2, 5, 10]
```

Es una capa de atención de transformador. Batalla de consulta de 5 posiciones, batalla de clave/valor de 10 posiciones, 128-dim cada, 8 cabezas. `output`es las nuevas consultas aumentadas de contexto. `weights`es la matriz de alineación 5x10 que puedes visualizar.

> Éste es un transformador de atención.`output`Es una nueva "respuesta a la pregunta".`weights`Es una matriz de 5x10, puedes visualizarla.

### Cuando la atención clásica todavía importa

- La versión de una sola cabeza, de una sola capa, basada en RNN hace que cada concepto sea visible.
  Teaching: Un solo tema, un solo nivel, una versión basada en RNN.
- tareas de secuenciación en el dispositivo en las que los transformadores no encajan.
  Transformer 放不下设备端序列任务──
- Cualquier artículo de 2014-2017. Lo leerás mal sin conocer la convención de Bahdanau.
  Cualquier artículo de 2014-2017 años. No entiendo Bahdanau's约定你会误读它.
- Análisis de alineación de granos finos en MT. Los pesos de atención en bruto son una herramienta de interpretabilidad incluso en los modelos de transformadores, y leerlos requiere saber qué son.
  La pequeña parte de la información en la traducción de la máquina se encuentra en el análisis.

### La trampa de la atención-peso-como-explicación

Las pesas de atención parecen interpretables: son pesas que suman a uno a través de posiciones; puedes trazarlas; alta significa "mirado esto".

> El peso de la atención se puede explicar. Son el peso de un total de 1 y de 1 en una posición; puedes dibujarlos; alto significa "ver esto".

No son tan interpretables como parecen. Jain y Wallace (2019) mostraron que las distribuciones de atención pueden ser permutadas y reemplazadas por alternativas arbitrarias sin cambiar las predicciones de modelos para algunas tareas. Nunca reportes los pesos de atención como evidencia de razonamiento sin una ablación o verificación contrafactual.

> 它们 no son tan explicables como parecen. Jane y Wallace (2019) indican que la distribución de la atención puede ser sustituida y sustituida por cualquier otra, sin cambiar el modelo de predicción de ciertas tareas. Nunca debe utilizar la atención como evidencia de la hipótesis en caso de no tener una investigación de desintegración o de contrasatisfacción.

> **【中文解读】**Este capítulo se centra en cómo se puede implementar el modelo como producto disponible. Desde el modelo original hasta el sistema de producción, se deben considerar múltiples dimensiones de optimización de rendimiento, tratamiento de errores, control, etc.

## Envíe el producto .

Salvo como`outputs/prompt-attention-shapes.md`¿Qué es esto ?

> 保存为                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           `outputs/prompt-attention-shapes.md`¿Qué es esto ?

```markdown
---
name: attention-shapes
description: Debug shape bugs in attention implementations.
phase: 5
lesson: 10
---

Given a broken attention implementation, you identify the shape mismatch. Output:

1. Which matrix has the wrong shape. Name the tensor.
2. What its shape should be, derived from (d_s, d_h, d_attn, T_enc, T_dec, batch_size).
3. One-line fix. Transpose, reshape, or project.
4. A test to catch regressions. Typically: assert `output.shape == (batch, T_dec, d_h)` and `weights.shape == (batch, T_dec, T_enc)` and `weights.sum(dim=-1) close to 1`.

Refuse to recommend fixes that silently broadcast. Broadcast-hiding bugs surface later as silent accuracy degradation, the worst kind of attention bug.

For Bahdanau confusion, insist the decoder input is `s_{t-1}` (pre-step state). For Luong, `s_t` (post-step state). For dot-product, flag dimension mismatch between query and key as the most common first-time error.
```

> **【中文解读】**Practice los temas de fácil/medio/duro  3 difficulty to pass in  Recomenda al menos completar los temas de grado medio  Grado duro  para la preparación de la entrevista

## Los ejercicios.

1. **Easy.**Implementación `softmax`En el código de código se encuentran los tokens de relleno para que la atención tenga peso cero.
   **简单。**                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             `softmax`掩码, hacer que el tiempo de carga en el codificador sea de 0 ⋅ en la serie de cambios de tiempo.
2. **Medium.**Añadir atención multi-cabeza a la Luong `general`forma. dividido`d_h`en el`n_heads`Los grupos, la atención por cabeza, concatenado.
   **中等。**Por lo largo`general`Forma de añadir más atención.`d_h`Por lo que se divide`n_heads`组, cada uno de los primeros pasos de la ejecución
3. **Hard.**Entrenar un codificador-decodificador GRU con Bahdanau atención en la tarea de copia de juguete de la lección 09. Precisión de trama vs longitud de secuencia. Comparar con la línea de base de no atención. Usted debe ver la brecha se amplía a medida que crece la longitud, confirmando la atención levanta el cuello de botella.
   **困难。**En la 9a clase de tareas de reproducción de juguetes entrenamiento con Bahdanau Atención GRU  codificador-descodificador ∞ dibujar la precisión de la velocidad vs  secuencia longitud ∞ Comparado con la base de la línea sin atención ∞ Usted debe ver la diferencia creciendo y ampliándose con la longitud, confirmar la atención desactivado ∞

> **【中文解读】**En el lenguaje de los términos "Lo que la gente dice" vs "Lo que realmente significa" se distingue entre el lenguaje diario y la definición técnica de significado.

## Términos clave .

| Term / 术语 | What people say / 人们常说的 | What it actually means / 实际含义 |
|------|-----------------|-----------------------|
| Attention（注意力） | Looking at things / 看东西 | Weighted average of a value sequence, weights computed from a query-key similarity. / 值序列的加权平均，权重从查询-键相似度计算。 |
| Query, Key, Value（查询、键、值） | QKV | Three projections: Q asks, K is what to match, V is what to return. / 三个投影：Q 询问，K 是要匹配的，V 是要返回的。 |
| Additive attention（加性注意力） | Bahdanau | Feed-forward score: `v^T tanh(W q + U k)`. / 前馈分数：`v^T tanh(W q + U k)`。 |
| Multiplicative attention（乘性注意力） | Luong dot / general | Score is `q^T k` or `q^T W k`. Cheaper, same accuracy on most tasks. / 分数是 `q^T k` 或 `q^T W k`。更便宜，大多数任务上相同准确率。 |
| Alignment matrix（对齐矩阵） | The pretty picture / 那张漂亮的图 | Attention weights as a `(T_dec, T_enc)` grid. Read it to see what the model attended to. / 注意力权重作为 `(T_dec, T_enc)` 网格。阅读它看模型关注了什么。 |

> **【中文解读】**延伸阅读 proporciona un alto nivel de recursos para el aprendizaje profundo. Estos artículos y cursos son los referentes clásicos en el campo, adecuados para los lectores que necesitan una comprensión profunda.

## Más Leer más Leer más

- [Bahdanau, Cho, Bengio (2014). Neural Machine Translation by Jointly Learning to Align and Translate](https://arxiv.org/abs/1409.0473)¿Qué es eso?
- [Luong, Pham, Manning (2015). Effective Approaches to Attention-based Neural Machine Translation](https://arxiv.org/abs/1508.04025) las tres variantes de puntaje y su comparación. / 三种分数变体及其比较──
- [Jain and Wallace (2019). Attention is not Explanation](https://arxiv.org/abs/1902.10186) la advertencia de interpretación. / 可解释性警示──
- [Dive into Deep Learning — Bahdanau Attention](https://d2l.ai/chapter_attention-mechanisms-and-transformers/bahdanau-attention.html) Paseo en marcha con PyTorch. / 带 PyTorch 的可运行演练──
