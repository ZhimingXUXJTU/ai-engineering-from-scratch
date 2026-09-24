# GPT  Modelado de lenguaje causal  GPT  因果语言模型

> BERT ve ambos lados. GPT sólo ve el pasado. La máscara triangular es la línea de código más consecuente en la IA moderna.

> **【中文解读】**GPT es un transformador solo para decodificadores, con el factor factor de cuadro de cuadro de cuadro de cuadro de cuadro de cuadro de cuadro de cuadro de cuadro de cuadro de cuadro de cuadro de cuadro de cuadro de cuadro de cuadro de cuadro de cuadro de cuadro de cuadro de cuadro de cuadro de cuadro de cuadro de cuadro de cuadro de cuadro de cuadro de cuadro de cuadro de cuadro de cuadro de cuadro de cuadro de cuadro de cuadro de cuadro de cuadro de cuadro de cuadro de cuadro de cuadro de cuadro de cuadro de cuadro de cuadro de cuadro de cuadro de cuadro de cuadro de cuadro de cuadro de cuadro de cuadro de cuadro de cuadro de cuadro de cuadro de cuadro de cuadro de cuadro de cuadro de cuadro de cuadro de cuadro de cuadro de cuadro de cuadro de cuadro de cuadro de cuadro de cuadro de cuadro de cuadro de cuadro de cuadro de cuadro de cuadro de cuadro de cuadro de cuadro de cuadro de cuadro de cuadro de cuadro de cuadro de cuadro de cuadro de cuadro de cuadro de cuadro de cuadro de cuadro de cuadro de cuadro de cuadro de cuadro de cuadro de cuadro de cuadro de cuadro de cuadro de cuadro de cuadro de cuadro de cuadro de cuadro de cuadro de cuadro de cuadro de cuadro de cuadro de cuento de cuento de cuento de cuento de cuento de cuento de cuento de cuento de cuento de cuento de cuento de cuento de cuento de cuento de cuento de cuento de cuento de cuento de cuento de cuento de cuento de cuento de cuento de cuento de cuento de cuento de cuento de cuento de cuento de cuento de cuento de cuento de cuento de cuento de cuento de cuento de cuento de cuento de cuento de cuento de cuento de cuento de cuento de cuento de cuento de cuento de cuento de cuento de cuento de cuento de cuento de cuento de

**Type:** Hands-on | **类型:** 动手
**Language:**¿ Qué pasa ?**语言:**Python
**Prerequisites:** Phase 7 · 02 (Self-Attention), Phase 7 · 05 (Full Transformer), Phase 7 · 06 (BERT) | **前置知识:** Phase 7 · 02 (Self-Attention), Phase 7 · 05 (Full Transformer), Phase 7 · 06 (BERT)
**Time:** ~75 minutes | **时间:** ~75 分钟

## El problema es la introducción del problema

Un modelo de lenguaje responde a una pregunta: dado el primer `t-1`Tokens, ¿cuál es la distribución de probabilidades sobre token `t`Entrenar en esa señal  predicción de token siguiente  y usted obtiene un modelo que puede generar texto arbitrario un token a la vez.

> 语言模型回答一个问题:给定前 `t-1`Es un símbolo, primero.`t`¿Cuál es la probabilidad de distribución de un token? En este señal  siguiente token 预测 en el entrenamiento, puedes obtener un modelo de texto que pueda generar cada token.

Para entrenarlo de extremo a extremo en una secuencia completa en paralelo, se necesita que la predicción de cada posición dependa sólo de posiciones anteriores.

> Para entrenar en toda la secuencia de arriba a abajo, necesitas predicir cada posición sólo dependiendo de la posición anterior.

La máscara causal hace esto. Es una matriz triangular superior única de`-inf`Los valores añadidos a las puntuaciones de atención antes de softmax. Después de softmax, esas posiciones se convierten en 0. Cada posición puede atender solo a sí misma y a las posiciones anteriores. Y porque se aplica una vez a toda la secuencia, se obtienen N paralelos de pronóstico de token siguiente en un pase hacia adelante.

> El resultado es que se ha logrado esto.`-inf`值), adicionado a softmax 之前的注意分数上──softmax 后, estas posiciones cambian a 0── cada posición sólo puede centrarse en sí misma y en la posición anterior──因为 sólo se aplica una vez a toda la secuencia, así que una vez hacia adelante se puede propagar en obtener N 个并行的下一个代币 预测──

GPT-1 (2018), GPT-2 (2019), GPT-3 (2020), GPT-4 (2023), GPT-5 (2024), Claude, Llama, Qwen, Mistral, DeepSeek, Kimi  son todos transformadores causales solo para decodificadores con el mismo bucle central.
GPT-1 (2018), GPT-2 (2019), GPT-3 (2020), GPT-4 (2023), GPT-5 (2025), Claude, Llama, Qwen, Mistral, DeepSeek, Kimi  son todos transformadores causales solo para decodificadores con el mismo bucle central. Lo que los separa son la calidad de los datos, la escala y los refinamientos arquitectónicos, y el post-entrenamiento (SFT, RLHF, DPO y sus sucesores).

> GPT-1(2018)、GPT-2(2019)、GPT-3(2020)、GPT-4(2023)、GPT-5(2024)、Claude、Llama、Qwen、Mistral、DeepSeek、Kimi

> **【中文解读】**El factor de ocultación es la línea de código más importante de la IA moderna. Una matriz de tres esquinas (en inglés: upper-triangle matrix, inf 值), más la cantidad de atención, a través de la softmax, se oculta en 0. Cada posición puede concentrarse en sí misma y en los tokens anteriores.

## El concepto central.

![Causal mask creates a triangular attention matrix](../assets/causal-attention.svg)

### La máscara

Dado una secuencia de longitud `N`, construir un`N × N`matriz:

> 给定长度为 `N`de la serie, construir una.`N × N`¿Qué es eso?

```
M[i, j] = 0       if j <= i
M[i, j] = -inf    if j > i
```

Añadir`M`a las puntuaciones de atención antes de softmax. `exp(-inf) = 0`Cada fila de la matriz de atención es una distribución de probabilidades sobre posiciones anteriores.

> ¿ Qué ?`M`Adición a la máxima de la concentración inicial anterior.`exp(-inf) = 0`, por lo que el peso de la posición oculta es de cero. Cada línea de la matriz de atención es sólo la distribución de probabilidades en la posición anterior.

Costo de ejecución: uno `torch.tril()`Llamadas, tiempo de cálculo, nanosegundos, impacto en el campo, todo.

> 实现成本:一行 `torch.tril()`调用──计算时间:纳秒级── sobre el impacto de todo el campo:
### De donde viene el triángulo

La máscara se presenta generalmente como un parche enlazado en la atención. ejecuta la derivación en la otra dirección y deja de ser misteriosa: la atención es el tercer refinamiento de un promedio prefijo, y el triángulo es los límites de bucle de ese promedio, escrito como una matriz.

**Stage 1 — prefix average.**El resumen causal más estúpido de una secuencia: posición .`i`se convierte en el promedio de posiciones `0…i`Como un bucle, eso es`out[i] = X[:i+1].mean(0)`El mismo cálculo es una matriz multiplicar. Tomar una matriz triangular inferior de uno, dividir cada fila por su conteo, multiplicar:

```python
import numpy as np

A = np.tril(np.ones((n, n)))
A = A / A.sum(axis=1, keepdims=True)
out = A @ X
```

Redacción`i`de `A`¿ Es verdad ?`[1/(i+1), …, 1/(i+1), 0, …, 0]`Los ceros por encima de la diagonal son la causalidad. Nada sobre el futuro fue ocultado; el futuro nunca fue en la suma.

**Stage 2 — learned weights.**Un promedio uniforme trata cada token pasado como igualmente relevante.`S`Ahora las filas ya no suman a uno por construcción, así que normaliza cada fila con softmax en lugar de dividir por el recuento. Softmax nunca saca un cero exacto, lo que rompe la causalidad  a menos que las puntuaciones futuras entren como `-inf`, porque`exp(-inf) = 0`¿Qué es esto ?

```python
def softmax(x, axis):
    e = np.exp(x - np.max(x, axis=axis, keepdims=True))
    return e / e.sum(axis=axis, keepdims=True)

S = S + np.triu(np.full((n, n), -np.inf), k=1)
A = softmax(S, axis=1)
out = A @ X
```

El mismo triángulo, la misma matriz de filasestocásticas, la misma matmul.`-inf`La máscara no es una nueva maquinaria.

**Stage 3 — content-dependent weights.**En la etapa 2, `S`La posición 7 siempre pesa la misma posición 3, sea cual sea el significado de los tokens.`S = Q @ K.T / sqrt(d_k)`No hay nada más que cambie.

Tres etapas, una invariante: una matriz de fila-estocástica triangular inferior por la secuencia. promedio uniforme, pesos estáticos aprendidos, pesos dependientes del contenido. La máscara nunca se añadió a la atención.

```figure
mask-derivation
```

### Formación paralela, inferencia en serie

Formación: adelantar todo `(N, d_model)`Se calcula N pérdidas de entropía cruzada (una por posición), suma, backprop. Paralelas a lo largo de la secuencia.

> Entrenamiento: para todo`(N, d_model)`序列做一次前向传播,计算 N 个交叉损失(每个位置一个),求和,反向传播──沿序列并行──这就是GPT 训练可扩展的原因一次GPU通行就能处理批量中的1M 个代币──

Inferencia: generas token por token.`[t1, t2, t3]`¿ Qué ?`t4`- Alimentación .`[t1, t2, t3, t4]`¿ Qué ?`t5`- Alimentación .`[t1, t2, t3, t4, t5]`¿ Qué ?`t6`El caché KV (lección 12) guarda los estados ocultos de `t1…tn`Así que no los recompite cada paso. Pero la profundidad en serie en la inferencia = longitud de salida. Ese es el impuesto autoregresivista y por qué la descifrado es el cuello de botella de latencia de cada LLM.

> 推理: por token 生成──输入 `[t1, t2, t3]`, lo conseguí`t4` Entrar`[t1, t2, t3, t4]`, lo conseguí`t5` Entrar`[t1, t2, t3, t4, t5]`, lo conseguí`t6`;;KV 缓存(第 12 课) guardado `t1…tn`El estado oculto, evitar cada paso de nuevo cálculo. Pero la profundidad de la cadena en el momento de la recomendación es la longitud de salida.

### La pérdida  cambio por uno

Se le dan tokens `[t1, t2, t3, t4]`¿Qué es esto ?

>                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                              `[t1, t2, t3, t4]`¿Qué es esto ?

- Entrada: `[t1, t2, t3]`
  En inglés:`[t1, t2, t3]`
- Objetivos: `[t2, t3, t4]`
  En inglés, el nombre de la persona que se encuentra en el sitio web es:`[t2, t3, t4]`

Para cada posición .`i`, computación `-log P(target_i | inputs[:i+1])`Esta es la entropía cruzada de toda la secuencia.

> Para cada posición`i`, calcular `-log P(target_i | inputs[:i+1])`求和── ése es el cruce de toda la secuencia──

Cada transformador LM que hayas oído hablar de trenes en esta pérdida. Pre-entrenamiento, ajuste fino, SFT  misma pérdida, datos diferentes.

> Cada modelo de lenguaje de transformador que has oído hablar está en este proceso de entrenamiento.

> **【拓展：Teacher Forcing 与暴露偏差】**GPT entrenamiento de uso del maestro forzando cada paso de entrada en la verdadera anterior a un token, y no el propio modelo de pronóstico. Esto conduce a "exposición de prejuicios" (exposición de prejuicios): entrenamiento cuando el modelo nunca ha visto su propio error de salida, la hipótesis debe continuar generando de su propio salida.

### Estrategias de decodificación

Después de la formación, las opciones de muestreo son más importantes de lo que la gente piensa.

> Después de la formación, la elección de estrategias de toma es más importante que lo que la gente imagina.

| Method | What it does | When to use |
|--------|--------------|-------------|
| 方法 | 功能 | 适用场景 |
| Greedy | Argmax every step | Deterministic tasks, code completion |
| 贪心 | 每步取最大值 | 确定性任务、代码补全 |
| Temperature | Divide logits by T, sample | Creative tasks, higher T = more diversity |
| 温度 | 将 logits 除以 T 后采样 | 创意任务，T 越高多样性越大 |
| Top-k | Sample from top-k tokens only | Kills low-probability tails |
| Top-k | 只从概率最高的 k 个 token 采样 | 消除低概率尾部 |
| Top-p (nucleus) | Sample from smallest set with cumulative prob ≥ p | 2020+ default; adapts to distribution shape |
| Top-p（核采样） | 从累积概率 ≥ p 的最小集合中采样 | 2020+ 默认策略；自适应分布形状 |
| Min-p | Keep tokens with `p > min_p * max_p` | 2024+; better at rejecting long tails than top-p |
| Min-p | 保留 `p > min_p * max_p` 的 token | 2024+；比 top-p 更好地拒绝长尾 |
| Speculative decoding | Draft model proposes N tokens, big model verifies | 2–3× latency reduction at same quality |
| 推测解码 | 草案模型提出 N 个 token，大模型验证 | 相同质量下延迟降低 2-3 倍 |

En 2026, min-p + temperatura 0,7 es un defecto razonable para los modelos de pesos abiertos.

> En 2026 la temperatura min-p + 0,7 es la configuración razonable del modelo de código abierto.

> **【中文解读】**解码策略的选择直接影响生成质量──贪心搜索(argmax) Adapting to determination task, temperaturas采样增加多样性,top-p/min-p 截断低概率尾部──2026 年的推默认:min-p + temperature 0.7,比传统的top-p 能更好地处理分布的度变化──

> **【拓展：从 GPT-2 到 GPT-4 的规模跳跃】**GPT-2(1.5B 参数)→ GPT-3(175B)→ GPT-4(estima que en el salto de escala de 1.8T MoE), la estructura cambia muy poco, pero la mejora de los métodos de datos y entrenamiento es enorme―GPT-4 utiliza la estructura de datos de MoE(mixta especialidad) y la mayor calidad, además de RLHF para el entrenamiento de preparación― esto confirma la hipótesis de "tamaño es todo", pero también muestra que la calidad de datos y el entrenamiento posterior son igualmente importantes―

### ¿Qué hizo que funcionara la "recepta de GPT"

1. **Decoder-only.**No hay codificador en la carga.
   En inglés:**解码器专用。**没有编码器开销──每层一次注意力 + FFN 通行──
2. **Scaling.**124M → 1.5B → 175B → billones. Las leyes de escala de Chinchilla (lección 13) te dicen cómo gastar computación.
   En inglés:**规模扩展。**Desde 124M hasta 1.5B hasta 175B, y hasta los mil millones de parametros.
3. **In-context learning.**Surgió alrededor de 6B13B. El modelo puede seguir algunos ejemplos de disparos sin ajuste fino.
   En inglés:**上下文学习。**约在 6B-13B 参数时涌现――模型无需微调就能遵循少样本示例――
4. **RLHF.**La formación posterior sobre las preferencias humanas convirtió el texto crudo pre-entrenado en asistentes de chat.
   En inglés:**RLHF。**En el caso de los entrenamientos realizados en la prefixión humana, el texto original del entrenamiento previo se traducirá en asistente de diálogo.
5. **Pre-norm + RoPE + SwiGLU.**Entrenamiento estable a escala.
   En inglés:**Pre-norm + RoPE + SwiGLU。**Entrenamiento de estabilidad a gran escala.

La arquitectura central no ha cambiado mucho desde el GPT-2. Todo lo interesante ha sucedido en datos, escala y post-entrenamiento.

> Desde el GPT-2, la estructura central no ha cambiado mucho. Todas las cosas interesantes ocurren en el aspecto de la escala y el entrenamiento posterior.

> **【中文解读】**Elemento de éxito de GPT:Simple de la estructura de sólo decodificador, escala de ampliación de la estructura de la GPT a partir de 124M hasta millones de parámetros)  Up下文学习能力 (~6B 参数开始涌现) RLHF 后训练 (将预训文将转化为对话助手) 以及现代块设计 (Pre-norm + RoPE + SwiGLU) 

> **【拓展：自回归生成的推理瓶颈】**La contradicción central de GPT es: entrenar y calcular toda la secuencia, y tener un tiempo de trabajo en el que se puede calcular el tiempo de trabajo.

## Construye y realiza.
```figure
causal-mask
```

## Construye el mismo

### Paso 1: la máscara causal

¿ Qué ?`code/main.py`Un solo en línea:

> 参见 `code/main.py`一行代码:

```python
def causal_mask(n):
    return [[0.0 if j <= i else float("-inf") for j in range(n)] for i in range(n)]
```

Añade a las puntuaciones de atención antes de la máxima.

> Para que se haga más suave, se debe aumentar la cantidad de atención que se había hecho antes.

### Paso 2: un modelo de GPT de dos capas

Coloque dos bloques de decodificación (autoatención enmascarada + FFN, sin atención cruzada). Agregue una incorporación de token, una codificación posicional y una desincorporación (atado a la matriz de incorporación de token  un truco estándar desde GPT-2).

> 堆叠两个解码器块(掩码自注意力 + FFN,无交叉注意力) ・・・ Añadir el token 嵌入、位置编码和反嵌入(与代币 嵌入矩阵绑定GPT-2 以来的标准技巧) ・・・

### Paso 3: Previsión de la próxima señal, de extremo a extremo

En una vocabulario de juguete de 20 tokens, produzca logits en cada posición. Calcule la pérdida de entropía cruzada contra el objetivo de cambio por uno.

> En el tablero de 20 tokens de juguetes, en cada posición se generan logitos.

### Paso 4: muestreo

Implemente codiciosas, temperatura, top-k, top-p, min-p. ejecuta cada una en un prompt fijo y compara las salidas. Una función de muestreo es de 10 líneas.

> 实现贪心、温度、top-k、top-p、min-p 采样──在固定提示上分别运行并比较输出──一采样函数只需要10 行代码──

## Usalo con el marco de ejecución

PyTorch, 2026 Idioma:

> PyTorch, 2026 años de uso habitual

```python
from transformers import AutoModelForCausalLM, AutoTokenizer
model = AutoModelForCausalLM.from_pretrained("meta-llama/Llama-3.2-3B-Instruct")
tok = AutoTokenizer.from_pretrained("meta-llama/Llama-3.2-3B-Instruct")

prompt = "Attention is all you need because"
inputs = tok(prompt, return_tensors="pt")
out = model.generate(
    **inputs,
    max_new_tokens=64,
    temperature=0.7,
    top_p=0.9,
    do_sample=True,
)
print(tok.decode(out[0]))
```

Bajo la capucha,`generate()`ejecuta el pase hacia adelante, tira de los logits de posición final, muestra el siguiente token, lo añade y repite. Cada pila de inferencias LLM de producción (vLLM, TensorRT-LLM, llama.cpp, Ollama, MLX) implementa el mismo bucle con gran optimización  preempleo en lote, batch continuo, paging de caché KV, descodificación especulativa.

> En el fondo,`generate()`运行前向传播,取出最后位置的logits,采样下一个代币,添加到序列中,重复──每一个生产 LLM 推理(vLLM、TensorRT-LLM、llama.cpp、Ollama、MLX) se utilizan grandes cantidades de optimización para lograr el mismo ciclo批量预填充、连续批处理、KV 缓存分页、推测解码──

**GPT vs BERT, one line each:**Las predicciones del GPT `P(x_t | x_{<t})`- BERT predice .`P(x_masked | x_unmasked)`La pérdida determina si el modelo puede generar.

> **GPT 与 BERT 各一句话：**GPT 预测 `P(x_t | x_{<t})`│BERT 预测 │`P(x_masked | x_unmasked)` La función de pérdida determina si el modelo puede generarse

## Envíe el producto .

¿ Qué ?`outputs/skill-sampling-tuner.md`La habilidad selecciona parámetros de muestreo para una tarea de nueva generación y señala cuando se requiere una decodificación determinista.

> 参见 `outputs/skill-sampling-tuner.md` Esta habilidad para la nueva generación de tareas seleccionar parámetros,并标记何时需要确定性解码──

## Los ejercicios.

1. **Easy.**- ¿ Qué ?`code/main.py`y comprobar que la matriz de atención causal es triangular inferior después de softmax.
   Traducción:运行`code/main.py`, la prueba de la razón de la matriz de atención en la suavemax 后是下三角的──抽查:
2. **Medium.**Compare la perplejidad de la viga 4 con la codicia en 10 preguntas cortas. ¿La viga siempre gana? (sugerencia: generalmente para la traducción, no para el chat abierto).
   En 10 pocas palabras, la búsqueda de la búsqueda de la búsqueda de la búsqueda de la búsqueda de la búsqueda de la búsqueda de la búsqueda de la búsqueda de la búsqueda de la búsqueda de la búsqueda de la búsqueda de la búsqueda de la búsqueda de la búsqueda de la búsqueda de la búsqueda de la búsqueda de la búsqueda de la búsqueda de la búsqueda de la búsqueda de la búsqueda de la búsqueda de la búsqueda de la búsqueda de la búsqueda de la búsqueda de la búsqueda de la búsqueda de la búsqueda de la búsqueda de la búsqueda de la búsqueda de la búsqueda de la búsqueda de la búsqueda de la búsqueda de la búsqueda de la búsqueda de la búsqueda de la búsqueda de la búsqueda de la búsqueda de la búsqueda de la búsqueda de la búsqueda de la búsqueda de la búsqueda de la búsqueda de la búsqueda de la búsqueda de la búsqueda de la búsqueda de la búsqueda de la búsqueda de la búsqueda de la búsqueda de la búsqueda de la búsqueda de la búsqueda de la búsqueda de la búsqueda de la búsqueda de la búsqueda de la búsqueda de la búsqueda de la búsqueda de la búsqueda de la búsqueda de la búsqueda de la búsqueda de la búsqueda de la búsqueda de la búsqueda de la búsqueda de la búsqueda de la búsqueda de la búsqueda de la búsqueda de la búsqueda de la búsqueda de la búsqueda de la búsqueda de la búsqueda de la búsqueda de la búsqueda de la búsqueda de la búsqueda de la búsqueda de la búsqueda de la búsqueda de la búsqueda de la búsqueda de la búsqueda de la búsqueda de la búsqueda de la búsqueda de un puedas de un puedas de un
3. **Hard.**Implemente una descifrado especulativo: utilice un modelo de 2 capas pequeño como el borrador y un modelo de 6 capas como el verificador.
   En el texto chino, el método de cálculo de la velocidad de la velocidad de la velocidad de la velocidad de la velocidad de la velocidad de la velocidad de la velocidad de la velocidad de la velocidad de la velocidad de la velocidad de la velocidad de la velocidad de la velocidad de la velocidad de la velocidad de la velocidad de la velocidad de la velocidad de la velocidad de la velocidad de la velocidad de la velocidad de la velocidad de la velocidad de la velocidad de la velocidad de la velocidad de la velocidad de la velocidad de la velocidad de la velocidad de la velocidad de la velocidad de la velocidad de la velocidad de la velocidad de la velocidad de la velocidad de la velocidad de la velocidad de la velocidad de la velocidad de la velocidad de la velocidad de la velocidad de la velocidad de la velocidad de la velocidad de la velocidad de la velocidad de la velocidad de la velocidad de la velocidad de la velocidad de la velocidad de la velocidad de la velocidad de la velocidad de la velocidad de la velocidad de la velocidad de la velocidad de la velocidad de la velocidad de la velocidad de la velocidad de la velocidad de la velocidad de la velocidad de la velocidad de la velocidad de la velocidad de la velocidad de la velocidad de la velocidad de la velocidad de la velocidad de la velocidad de la velocidad de la velocidad de la velocidad de la velocidad de la velocidad de la velocidad de la velocidad de la velocidad de la velocidad de la velocidad de la velocidad de la velocidad de la velocidad de la velocidad de la velocidad de la velocidad de la velocidad de la velocidad de la velocidad de la velocidad de la velocidad de la velocidad de la velocidad de la velocidad de la velocidad de la velocidad de la velocidad de la velocidad de la velocidad de la velocidad de la velocidad de la velocidad de la velocidad de la velocidad de la velocidad de la velocidad de la velocidad de la velocidad de la velocidad de la velocidad de la velocidad de la velocidad de la velocidad de la velocidad de la velocidad de

## Términos clave .

| Term | What people say | What it actually means |
|------|-----------------|-----------------------|
| 术语 | 通俗说法 | 实际含义 |
| Causal mask | "The triangle" | Upper-triangular `-inf` matrix added to attention scores so position `i` only sees positions `≤ i`. |
| 因果掩码 | "三角矩阵" | 加到注意力分数上的上三角 `-inf` 矩阵，使位置 `i` 只能看到位置 `≤ i`。 |
| Next-token prediction | "The loss" | Cross-entropy of the model's distribution against the true next token at every position. |
| 下一个 token 预测 | "损失函数" | 模型分布与每个位置真实下一个 token 之间的交叉熵。 |
| Autoregressive | "Generate one at a time" | Feed output back as input; parallelism only during training, not during generation. |
| 自回归 | "逐个生成" | 将输出反馈为输入；仅在训练时并行，生成时不并行。 |
| Logits | "Pre-softmax scores" | Raw output of the LM head before softmax; sampling happens on these. |
| Logits | "softmax 前的分数" | LM 头在 softmax 之前的原始输出；采样基于这些值。 |
| Temperature | "Creativity knob" | Divide logits by T; T→0 = greedy, T→∞ = uniform. |
| 温度 | "创造力旋钮" | 将 logits 除以 T；T→0 为贪心，T→∞ 为均匀分布。 |
| Top-p | "Nucleus sampling" | Truncate distribution to smallest set summing to ≥p; sample from what remains. |
| Top-p | "核采样" | 将分布截断为累积概率 ≥ p 的最小集合；从剩余部分采样。 |
| Min-p | "Better than top-p" | Keep tokens where `p ≥ min_p × max_p`; adapts cutoff to sharpness of distribution. |
| Min-p | "比 top-p 更好" | 保留 `p ≥ min_p × max_p` 的 token；根据分布锐度自适应调整截断。 |
| Speculative decoding | "Draft + verify" | Cheap model proposes N tokens; big model verifies in parallel. |
| 推测解码 | "草案+验证" | 廉价模型提出 N 个 token；大模型并行验证。 |
| Teacher forcing | "Training trick" | During training, feed the true previous token, not the model's prediction. Standard for every seq2seq LM. |
| Teacher forcing | "训练技巧" | 训练时输入真实的前一个 token，而非模型的预测。所有 seq2seq 语言模型的标准做法。 |

## Más Leer más Leer más

- [Radford et al. (2018). Improving Language Understanding by Generative Pre-Training](https://cdn.openai.com/research-covers/language-unsupervised/language_understanding_paper.pdf) GPT-1.
  El texto original de la obra es el de la escritura.
- [Radford et al. (2019). Language Models are Unsupervised Multitask Learners](https://cdn.openai.com/better-language-models/language_models_are_unsupervised_multitask_learners.pdf) GPT-2.
  En el caso de los países de la región de la región de la región de la región de la región de la región de la región de la región de la región de la región de la región de la región de la región de la región de la región de la región de la región de la región de la región de la región de la región de la región de la región de la región de la región de la región de la región de la región de la región de la región de la región de la región de la región de la región de la región de la región de la región de la región de la región de la región de la región de la región de la región de la región de la región de la región de la región de la región de la región de la región de la región de la región de la región de la región de la región de la región de la región de la región de la región de la región de la región de la región de la región de la región de la región de la región de la región de la región de la región de la región de la región de la región de la región de la región de la región de la región de la región de la región de la región de la región de la región de la región de la región de la región de la región de la región de la región de la región de la región de la región de la región de la región de la región de la región de la región.
- [Brown et al. (2020). Language Models are Few-Shot Learners](https://arxiv.org/abs/2005.14165) GPT-3 y aprendizaje en contexto.
  El texto original de la obra es el de la escritura.
- [Leviathan, Kalman, Matias (2023). Fast Inference from Transformers via Speculative Decoding](https://arxiv.org/abs/2211.17192) Papel de decodificación de especificaciones.
  Traducción:Tú测解码论文.
- [HuggingFace `modeling_llama.py`](https://github.com/huggingface/transformers/blob/main/src/transformers/models/llama/modeling_llama.py) código de referencia causal-LM canónico.
  En español: "HuggingFace Llama"
