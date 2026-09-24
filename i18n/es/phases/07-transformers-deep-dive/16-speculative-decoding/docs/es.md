# Descodación especulativa  Proyecto, Verificación, Repetición                                                                                                                                                                                                                                                      

> El decodificación autoregressiva es serie. Cada token espera al anterior. El decodificación especulativa rompe la cadena: un modelo barato elabora N tokens, el modelo caro verifica todos los N en un solo pase hacia adelante. Cuando el borrador está correcto pagaste un gran adelanto para N generaciones.

> **【中文解读】**Utiliza el pequeño modelo rápido generar el token de candidato, el gran modelo de verificación de la cantidad. Puede acelerar la racionalización 2-3 veces sin disminuir la calidad.

**Type:** Hands-on | **类型:** 动手
**Language:**¿ Qué pasa ?**语言:**Python
**Prerequisites:** Phase 7 · 07 (GPT Causal LM), Phase 7 · 12 (KV Cache & Flash Attention) | **前置知识:** Phase 7 · 07 (GPT Causal LM), Phase 7 · 12 (KV Cache & Flash Attention)
**Time:** ~60 minutes | **时间:** ~60 分钟

## El problema es la introducción del problema

Un 70B LLM muestreo de un token toma ~30 ms en un H100. Un modelo de borrador 3B toma ~3 ms. Si dejamos que el borrador 3B 5 tokens adelante, entonces ejecutar el 70B *una vez* para verificar todos los 5, el total es `5×3 + 30 = 45 ms`para hasta 5 tokens aceptados  versus `5×30 = 150 ms`Es el campo de la descodificación especulativa: intercambiar una pequeña cantidad de memoria extra de la GPU (modelo de borrador) por 24× menor latencia de decodificación.

> Un modelo de proyecto de H100 necesita alrededor de 30 ms. Un modelo de proyecto de H100 necesita alrededor de 3 ms. Si hacemos que 3B previamente genere 5 tokens, entonces se ejecuta 70B * una vez * validación de todos los 5 , total tiempo para `5×3 + 30 = 45 ms`El máximo obtenido 5 tokens aceptados y generado directamente necesita`5×30 = 150 ms`─Ese es el punto de venta total del proyecto: con una pequeña cantidad adicional de GPUs en el modelo del proyecto, se cambiará por 2-4 veces más bajo de la tarda del proyecto.

El truco tiene que preservar la distribución. La muestreo especulativa, introducida por Leviathan et al. (2023) y por Chen et al. simultáneamente, garantiza que la secuencia de salida es **identically distributed**No hay compromiso de calidad, sólo más rápido.

> Esta técnica debe mantenerse distribuida invariablemente. Proposición de la toma de ejemplos por Leviathan et al. (WEB 2023) y Chen et al. (WEB introducida simultáneamente, garantiza la distribución de la secuencia de salida y la generación automática del gran modelo.**完全相同**No hay pérdida de calidad, sólo más rápido.

Cuatro familias de pares de verificadores de borrador dominan la inferencia de 2026:

> Cuatro tipos de proyectos de certificación tendrán un papel dominante en la propuesta de 2026:

1. **Vanilla speculative (Leviathan 2023).**Modelo de proyecto separado (por ejemplo, Llama 3 1B) + verificador (por ejemplo, Llama 3 70B).
   En inglés:**朴素推测（Leviathan 2023）。**独立的草案模型(如 Llama 3 1B) + 验证器(如 Llama 3 70B) ⋅
2. **Medusa (Cai 2024).**Múltiples cabezas de decodificación en el verificador predicen posiciones `t+1..t+k`No hay un proyecto de modelo separado.
   En inglés:**Medusa（Cai 2024）。**En el verificador , varios terminales y posiciones de pronóstico .`t+1..t+k`无需独立草案模型──
3. **EAGLE family (Li 2024, 2025).**Draft ligero que reutiliza los estados ocultos del verificador; tasa de aceptación más cercana que la vainilla; 34× típico.
   En inglés:**EAGLE 系列（Li 2024, 2025）。**复用验证器隐藏状态的轻量草案; tasa de aceptación más alta que el simple esquema; aceleración típica de 3-4 veces:
4. **Lookahead decoding (Fu 2024).**Iteración Jacobi, no se requiere ningún modelo de proyecto, autoespeculación, nicho pero libre de dependencias.
   En inglés:**前瞻解码（Fu 2024）。**Jacobi 代; totalmente no necesita el modelo del proyecto.

Cada pila de inferencias de producción en 2026 envíe descifrado especulativo por defecto. vLLM, TensorRT-LLM, SGLang y llama.cpp todos admiten al menos vainilla + EAGLE-2.

> Cada producción de 2026 años tiene como objetivo el apoyo de la simple + EAGLE-2:

> **【中文解读】**推测解码的核心洞察:自归生成是串行瓶──用小模型(3B)快速生成 N 个候选代币,大模型(70B) una vez antes de la transmisión验证所有 N 个──总时间从 N×30ms 降至 5×3+30=45ms,加速 2-4 倍──关键:推测采样保证输出分布与大模型完全一致,无质量损失──

> **【拓展：EAGLE 与 Medusa 的自推测策略】**EAGLE(2024) Repite el estado oculto del gran modelo para generar un borrador, la tasa de aceptación es mayor que el pequeño modelo independiente, típicamente aceleración de 3-4 veces. Medusa añade varios terminales en el gran modelo, y pronostica varias posiciones futuras, sin necesidad de modelos adicionales. Estas dos estrategias de "auto-posición" evitan el mantenimiento de la venta del modelo del borrador independiente, convirtiéndose en la opción dominante de 2026.

## El concepto central.

### El algoritmo central

Dado un verificador `M_q`y un borrador más barato `M_p`¿Qué es esto ?

> 给定验器                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                         `M_q`Y más barato del modelo de proyecto `M_p`¿Qué es esto ?

1. - ¿ Qué ?`x_1..x_k`sea el prefijo ya decodificado.
   En inglés:设 `x_1..x_k`Por el código de la anterior.
2. **Draft**: uso `M_p`Proponer de forma autoregressiva `d_{k+1}, d_{k+2}, ..., d_{k+N}`con probabilidades de proyecto `p_1..p_N`¿ Qué ?
   En inglés:**草案**:用 `M_p`Propuso su regreso`d_{k+1}, d_{k+2}, ..., d_{k+N}`, , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , ,`p_1..p_N`¿Qué es eso?
3. **Verify in parallel**: correr `M_q`Una vez más .`x_1..x_k, d_{k+1}, ..., d_{k+N}`, obtener probabilidades de verificación `q_1..q_{N+1}`para posiciones `k+1..k+N+1`¿ Qué ?
   En inglés:**并行验证**Por lo tanto ,`x_1..x_k, d_{k+1}, ..., d_{k+N}`¿ Qué pasa ?`M_q`, obtener una posición`k+1..k+N+1`                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             `q_1..q_{N+1}`¿Qué es eso?
4. **Accept/reject each draft token left to right**: para cada uno `i`, acepta con probabilidad `min(1, q_i(d_i) / p_i(d_i))`¿ Qué ?
   En inglés:**从左到右接受/拒绝每个草案 token**: para cada uno `i`, en la probabilidad`min(1, q_i(d_i) / p_i(d_i))`¿Qué es esto?
5. En el primer rechazo en posición `j`: muestra `t_j`de la distribución "residual" `(q_j - p_j)_+`Todos los proyectos después de la`j`se descartan.
   En el idioma chino:`j`首次被拒绝时: de "残差" distribución `(q_j - p_j)_+`归一化后采样 `t_j`¿Qué es eso?`j`Después de todo el proyecto fue abandonado.
6. Al aceptar todo .`N`: muestra de un token extra `t_{N+1}`de la`q_{N+1}`(el token de bonificación gratuito).
   En español:`N`个都被接受时: desde `q_{N+1}`采样一个额外的标志 `t_{N+1}`(títol de premio gratis)

El truco de distribución residual es la visión matemática que mantiene la salida distribuida exactamente como si `M_q`había tomado muestras desde cero.

> Las técnicas de distribución de diferencia son mantener la distribución de la salida y la distribución de la`M_q`Desde el principio, el mismo tipo de matemáticas.

### Lo que determina la aceleración

- ¿ Qué ?`α`= tasa de aceptación esperada por proyecto de token.`c`= relación de costes entre proyectos y verificadores.

> 设 `α`= Previsión de aceptación de cada proyecto de token.`c`= costo del proyecto y el verificador por paso:

- La generación ingenua hace una llamada de modelo grande por token.
  Traducción:Pauquin genere cada símbolo 调用一次大模型──
- Especulativo hace una llamada de modelo grande por ...`(1 - α^{N+1}) / (1 - α) ≈ 1/(1-α)`fichas cuando `α`Es muy alto.
  Traducción:Tú测解码在 `α`较高时,每 `(1 - α^{N+1}) / (1 - α) ≈ 1/(1-α)`个代币 调用一次大模型──

La regla típica es que ...`α = 0.75`y `N = 5`El costo del proyecto es 5 veces más barato. El total del reloj de pared cae ~ 2,5 veces.

> `α = 0.75`Y `N = 5`时的典型经验法则: 时的典型经验法则: 时的典型调用减少3倍.

> **【中文解读】**El efecto de la aceleración depende de la tasa de aceptación alfa. Cuando alfa=0.75 ￼, aproximadamente 3 veces reducido el tamaño del modelo N=5 ￼.

**α depends on:**

> **α 取决于：**

- La información de la misma familia/del mismo entrenamiento aumenta significativamente.
  La cantidad de datos de la serie de pruebas de la prueba aumentó significativamente.
- Estrategia de decodificación: Draft codicioso contra verificador codicioso: alto α. Muestreo de temperatura: más difícil de emparejar; disminuye la aceptación.
  La situación de la economía de la región de la India se ha vuelto más difícil.
- Tipo de tarea: el código y la salida estructurada aceptan más (predictable); la escritura creativa de forma libre acepta menos.
  Traducción: tarea tipo──代码和结构化输出接受更多(可预测); libertad forma创意写作接受更少──

### Medusa  proyectos sin modelo de proyecto

Medusa sustituye el modelo de proyecto por cabezas de salida adicionales en el verificador.`t`¿Qué es esto ?

> Medusa utiliza el extra de la producción en el verificador para reemplazar el modelo.`t`¿Qué es esto ?

```
shared trunk → hidden h_t
    ├── head_0: predict token at t+1  (standard LM head)
    ├── head_1: predict token at t+2
    ├── head_2: predict token at t+3
    ├── head_3: predict token at t+4
```

Cada cabeza saca sus propias logitas. En la inferencia tomas una muestra de cada cabeza para obtener una secuencia de candidatos, luego verifica con un pase hacia adelante utilizando un esquema de atención al árbol que considera todas las continuidades de candidatos a la vez.

> Cada uno de ellos ha dado sus propias logitas. La idea es que cada uno de ellos obtenga una serie de candidatos, y luego, con el programa de atención, una vez más, considera todas las candidaturas.

Pros: no hay segundo modelo. Los inconvenientes: añade parámetros entrenables; necesita una etapa de ajuste fino supervisado (~ 1B tokens); la tasa de aceptación es un poco menor que la especulativa de vainilla con un buen borrador.

> 优点:无需第二模型──缺点:增加可训练参数;需要监督微调阶段(约1B token); aceptación比好的草案模型的朴素推测略低──

> **【拓展：推测解码在 vLLM 中的实现】**vLLM es el marco de investigación de LLM más popular del año 2026, original apoyo a la investigación de análisis de datos. Utiliza el proceso de análisis continuo de datos.

### Eagle  mejor dibujo mediante la reutilización de estados ocultos

EAGLE-1/2/3 (Li et al., 20242025) hace que el modelo de proyecto sea un pequeño transformador (típicamente de 1 capa) que ingere los estados ocultos de última capa del verificador. Debido a que el proyecto ve la representación de las características del verificador, sus predicciones se correlacionan fuertemente con la distribución de salida del verificador.

> EAGLE-1/2/3 ((Li 等人,2024-2025)) se convertirá el modelo del proyecto en un micro transformador ((generalmente 1 nivel), estado oculto de la última capa del verificador de absorción.

EAGLE-3 (2025) añadió la búsqueda de árboles sobre las continuas candidatos. vLLM y SGLang nave EAGLE-2/3 como la ruta de especificación predeterminada para Llama 3/4 y Qwen 3.

> EAGLE-3(2025) añadió a la búsqueda de árboles para el candidato de la redacción.

### El baile de caché KV

Los datos de verificación `N`Los tokens de proyecto en el verificador en un solo pase hacia adelante. Esto extiende la caché KV del verificador en `N`Si algunos borrados son rechazados, debe volver a rodar el caché a la longitud del prefijo aceptado.

> 验证在一次前向传播中将                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    `N`个草案 token 输入验证器── esto va a hacer que el KV de la prueba 缓存扩展 `N`个条目──Si algunos proyectos son rechazados, usted debe devolver el caché al tiempo que se ha aceptado.

Implementaciones de la producción (vLLM's `--speculative-model`Es un problema de la vida, pero no es difícil, pero es difícil.

> Producción de la realización de la`--speculative-model`、TensorRT-LLM's LookaheadDecoder) utiliza el KV 缓冲区 de tratamiento temporal de este problema──pre-escrito, aceptado en el momento de presentar── concepto no es difícil, pero la realización es más difícil──

## Construye y realiza.
```figure
draft-verify-tokens
```

## Construye el mismo

¿ Qué ?`code/main.py`Implementamos el algoritmo de muestreo especulativo principal (paso de rechazo + distribución residual) con:

> 参见 `code/main.py`△ Nosotros utilizamos los siguientes componentes para implementar el algoritmo de análisis de datos de base:

- Un "modelo grande" que es una determinación-softmax sobre una distribución codificada a mano (para que podamos verificar la aceptación matemática analíticamente).
  Un "grando modelo", es una determinación de la distribución de código de mano softmax (en inglés) para analizar la experiencia de la matemática.
- Un "modelo de borrador" que es una perturbación del modelo grande.
  Un "draft模型", es una versión perturbada del gran modelo.
- Un bucle de aceptación/rechazo que produce la misma distribución marginal que la muestreo directo.
  Un ciclo de aceptación/rechazo, que produce la misma distribución marginal que el tipo de uso directo.

### Paso 1: el paso de rechazo

```python
def accept_or_reject(q_prob, p_prob, draft_token, u):
    ratio = q_prob / p_prob if p_prob > 0 else float("inf")
    return u < min(1.0, ratio)
```

`u`es un número aleatorio uniforme. `q_prob`es la probabilidad del verificador para el token redactado. `p_prob`El teorema de Leviathan es que esta decisión de Bernoulli, seguida de muestreo del residual en el rechazo, conserva exactamente la distribución del verificador.

> `u`Es un número de veces.`q_prob`Es probable que el verificador haya hecho un proyecto de token.`p_prob`La teoría de Leviathan indica que esta decisión de Bernard y el rechazo de la muestra de residuos pueden asegurar la distribución del verificador.

### Paso 2: distribución residual

```python
def residual_dist(q, p):
    raw = [max(0.0, qi - pi) for qi, pi in zip(q, p)]
    s = sum(raw)
    return [r / s for r in raw]
```

Subtracción `p`de la`q`En el caso de los elementos, aplastar los valores negativos a cero, renormalizarlo.

>                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                              `q`                                                  `p`, se cortará el valor negativo a cero, se volverá a regroupir.

### Paso 3: un paso especulativo

```python
def spec_step(prefix, q_model, p_model, N, rng):
    drafts = []
    p_probs = []
    ctx = list(prefix)
    for _ in range(N):
        p_dist = p_model(ctx)
        d = sample(p_dist, rng)
        drafts.append(d)
        p_probs.append(p_dist[d])
        ctx.append(d)

    q_dists = [q_model(prefix + drafts[:i]) for i in range(N + 1)]

    for i, d in enumerate(drafts):
        u = rng.random()
        q_prob = q_dists[i][d]
        p_prob = p_probs[i]
        if u < min(1.0, q_prob / p_prob if p_prob > 0 else float("inf")):
            prefix = prefix + [d]
        else:
            res = residual_dist(q_dists[i], p_model(prefix))
            prefix = prefix + [sample(res, rng)]
            return prefix
    prefix = prefix + [sample(q_dists[N], rng)]
    return prefix
```

Cinco aceptados → un bono → seis tokens producidos en un pase de verificación.

> 五个被接受 → 一个奖励 → 一次验证器通行产生六个代币──

### Paso 4: medir la tasa de aceptación

ejecutar 10.000 pasos especulativos en diferentes niveles de calidad del borrador. tasa de aceptación de la trama vs KL divergencia entre la distribución del borrador y el verificador. Usted debe ver una relación monótona limpia.

> En diferentes niveles de calidad del proyecto se ejecutan 10.000 veces.

### Paso 5: verificar la equivalencia de distribución

Empiricamente: el histograma de tokens producido por el bucle especulativo debe coincidir con el histograma producido por muestreo directamente del verificador. Este es el teorema de Leviatán en la práctica.

> 经验上: el símbolo de un ciclo de sugerencias se corresponde directamente con el ejemplar de pruebas de la prueba.

## Usalo con el marco de ejecución

Producción:

> Producción de productos:

```bash
# vLLM with EAGLE
vllm serve meta-llama/Llama-3.1-70B-Instruct \
    --speculative-model /models/llama-3.1-eagle-70b \
    --speculative-draft-tensor-parallel-size 1 \
    --num-speculative-tokens 5

# vLLM with vanilla draft model
vllm serve meta-llama/Llama-3.1-70B-Instruct \
    --speculative-model meta-llama/Llama-3.2-1B-Instruct \
    --num-speculative-tokens 5
```

TensorRT-LLM tiene la ruta más rápida de Medusa a mediados de 2026. `faster-whisper`Envuelve la descifrado especulativo para Whisper-large con un pequeño borrador.

> TensorRT-LLM tendrá el camino más rápido de Medusa en el período medio de 2026:`faster-whisper`Para susurrar, en su mayor parte, el proyecto de ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley.

**Picking a draft:**

> **选择草案策略：**

| Strategy | When to pick | Speedup |
|----------|--------------|---------|
| 策略 | 何时选择 | 加速比 |
| Vanilla draft (1B/3B Llama family) | Fast prototype, no training | 1.8–2.3× |
| 朴素草案（1B/3B Llama 系列） | 快速原型，无需训练 | 1.8–2.3× |
| Medusa heads | You can fine-tune the verifier | 2–3× |
| Medusa 头 | 可以微调验证器 | 2–3× |
| EAGLE-2 / 3 | Production, max speed | 3–4× |
| EAGLE-2 / 3 | 生产环境，最大速度 | 3–4× |
| Lookahead | No draft, no training, no extra params | 1.3–1.6× |
| 前瞻 | 无草案，无训练，无额外参数 | 1.3–1.6× |

**When NOT to spec-decode:**

> **何时不使用推测解码：**

- Generación de secuencia única de 15 tokens.
  China: 1-5 tokens de la secuencia de generación.
- Muestreo de alta temperatura / muy creativo (caídas de α).
  En el caso de los edificios de la ciudad, el edificio de la ciudad de la capital es el edificio de la ciudad de la capital.
- Despliegues con restricciones de memoria (el modelo de proyecto añade VRAM).
  La situación de la población de la región de la región de la región de la región de la región de la región de la región de la región de la región de la región de la región de la región de la región de la región de la región de la región de la región de la región de la región de la región de la región de la región de la región de la región de la región de la región de la región de la región de la región de la región de la región de la región de la región de la región de la región de la región de la región de la región de la región de la región de la región de la región de la región de la región de la región de la región de la región de la región de la región de la región de la región de la región de la región de la región de la región de la región de la región de la región de la región de la región de la región de la región de la región de la región de la región de la región de la región de la región de la región de la región de la región de la región de la región de la región de la región de la región de la región de la región de la región de la Sudán.

## Envíe el producto .

¿ Qué ?`outputs/skill-spec-decode-picker.md`La habilidad elige una estrategia de decodificación especulativa (vanilla / Medusa / EAGLE / lookahead) y parámetros de ajuste (N, temperatura de proyecto) para una nueva carga de trabajo de inferencia.

> 参见 `outputs/skill-spec-decode-picker.md`△ Esta habilidad para nuevos propósitos                                                                                                                                                                                                                                                           

## Los ejercicios.

1. **Easy.**- ¿ Qué ?`code/main.py`. Confirmar que la distribución especulativa de tokens coincide con la distribución directa de muestras del verificador en 50.000 tokens dentro de un chi-cuadrado p > 0,05.
   Traducción:运行`code/main.py` Confirmar en 50.000 tokens, distribuir los tokens de la prueba con el verificador de la prueba de la prueba de la prueba de la prueba p > 0.05 dentro de la prueba de la prueba de la prueba de la prueba de la prueba de la prueba de la prueba de la prueba de la prueba de la prueba de la prueba de la prueba de la prueba de la prueba de la prueba de la prueba de la prueba de la prueba de la prueba de la prueba de la prueba de la prueba de la prueba de la prueba de la prueba de la prueba de la prueba de la prueba de la prueba de la prueba de la prueba de la prueba de la prueba de la prueba de la prueba de la prueba de la prueba de la prueba de la prueba de la prueba de la prueba de la prueba de la prueba de la prueba de la prueba de la prueba de la prueba de prueba de la prueba de prueba de la prueba de prueba de la prueba de prueba de la prueba de prueba de prueba de la prueba de prueba de prueba de prueba de prueba de prueba de prueba de prueba de prueba de prueba de prueba de prueba de prueba de prueba de prueba de prueba de prueba de prueba de prueba de prueba de prueba de prueba de prueba de prueba de prueba de prueba de prueba de prueba de prueba de prueba de prueba de prueba de prueba de prueba de prueba de prueba de prueba de prueba de prueba de prueba de prueba de prueba de prueba de prueba de prueba de prueba de prueba de prueba de prueba de prueba de prueba de prueba de prueba de prueba de prueba de prueba de prueba de prueba de prueba de prueba de prueba de prueba de prueba de prueba de prueba de prueba de prueba de prueba de prueba de prueba de prueba de prueba de prueba de prueba de prueba de prueba de prueba de prueba de prueba de prueba de prueba de prueba de prueba de prueba de prueba de prueba de prueba de prueba de prueba de prueba de prueba de prueba de prueba de prueba de prueba de prueba de prueba de prueba de prueba de prueba de prueba de prueba de prueba de prueba de prueba de prueba de prueba de prueba de prueba de prueba de prueba de prueba de prueba de prueba de prueba de prueba de prueba de prueba de prueba de prueba de prueba de prueba de prueba de prueba de prueba de prueba de prueba de prueba de prueba de prueba de prueba de prueba de prueba de prueba de prueba de prueba de prueba de prueba de prueba de prueba de prueba de prueba de prueba de prueba de prueba de prueba de prueba de prueba de prueba de prueba de prueba de prueba de
2. **Medium.**Aceleración de gráfico (tokens por modelo grande hacia adelante) como función de `N`por`α = 0.5, 0.7, 0.85`Identificar el óptimo`N`para cada α. (Intención: tokens esperados por llamada de verificación = `(1 - α^{N+1}) / (1 - α)`(en inglés).
   En español:`α = 0.5, 0.7, 0.85`时加速比( por cada gran modelo de símbolo de la dirección del número)`N`∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞`N`◊                                                                                                                                                                                                                                                              `(1 - α^{N+1}) / (1 - α)`◊)
3. **Hard.**Implemente una pequeña Medusa: toma la piedra angular GPT de la Lección 14, añada 3 cabezas LM adicionales que predicen las posiciones t+2, t+3, t+4. Entrenamiento en tinyshakespeare con una pérdida conjunta de múltiples cabezas. Compara las tasas de aceptación con un borrador de vainilla hecho mediante el truncado del mismo modelo.
   China 翻译:实现一个小型梅杜萨:取第14 课的 GPT毕业项目,添加 3 额外的 LM 头预测位置 t+2、t+3、t+4──用联合多头损失在小小小小小的上训──比较与截断相同模型得到的简单草案的接受率──
4. **Hard.**Implementar el rollback: comience con un prefijo KV de 10 tokens, alimenta 5 tokens de borrador, simula un rechazo en la posición 3. Verifique que sus lecturas de la caché coincidan correctamente con "prefijo + primeros 2 borradores aceptados" en la siguiente iteración.
   China:实现回滚:从10 token 的前 KV 缓存开始,输入5 个草案令牌,模拟位置3 的拒绝――验证你的缓存读取在下次代时正确匹配"前 + 前2 个已接受草案"――

## Términos clave .

| Term | What people say | What it actually means |
|------|-----------------|-----------------------|
| 术语 | 通俗说法 | 实际含义 |
| Draft model | "The cheap one" | A smaller model that proposes candidate tokens; usually 10–50× cheaper than the verifier. |
| 草案模型 | "便宜的那个" | 提出候选 token 的较小模型；通常比验证器便宜 10-50 倍。 |
| Verifier | "The big one" | The target model whose distribution we preserve; runs once per speculative step. |
| 验证器 | "大的那个" | 我们要保持其分布的目标模型；每次推测步骤运行一次。 |
| Acceptance rate (α) | "How often the draft is right" | Per-token probability that the verifier accepts the draft. 0.7–0.9 typical. |
| 接受率 (α) | "草案正确的频率" | 验证器接受草案的每 token 概率。典型值 0.7-0.9。 |
| Residual distribution | "The rejection fallback" | `(q - p)_+` normalized; sampling from this on rejection preserves the verifier's distribution. |
| 残差分布 | "拒绝时的后备方案" | `(q - p)_+` 归一化；拒绝时从中采样保持验证器的分布。 |
| Bonus token | "The free one" | When all N drafts accepted, sample one more from the verifier's next-step distribution. |
| 奖励 token | "免费的那个" | 当所有 N 个草案被接受时，从验证器的下一步分布中多采样一个。 |
| Medusa | "Draft-less speculative" | Multiple LM heads on the verifier predict positions t+1..t+k in parallel. |
| Medusa | "无草案推测" | 验证器上的多个 LM 头并行预测位置 t+1..t+k。 |
| EAGLE | "Hidden-state draft" | Tiny transformer draft conditioned on the verifier's last-layer hidden states. |
| EAGLE | "隐藏状态草案" | 以验证器最后一层隐藏状态为条件的小型 Transformer 草案。 |
| Lookahead decoding | "Jacobi iteration" | Self-speculation using a fixed-point iteration; no draft model. |
| 前瞻解码 | "Jacobi 迭代" | 使用不动点迭代的自推测；无需草案模型。 |
| Tree attention | "Verify many candidates at once" | Branching verification that considers several draft continuations simultaneously. |
| 树注意力 | "同时验证多个候选" | 同时考虑多个草案续写的分支验证。 |
| KV rollback | "Undo rejected drafts" | Scratch KV buffer; commit on acceptance, discard on reject. |
| KV 回滚 | "撤销被拒绝的草案" | 临时 KV 缓冲区；接受时提交，拒绝时丢弃。 |

## Más Leer más Leer más

- [Leviathan, Kalman, Matias (2023). Fast Inference from Transformers via Speculative Decoding](https://arxiv.org/abs/2211.17192) el algoritmo central y el teorema de equivalencia.
  Traducción:Tú测解码的核心算法和等价定理论文──
- [Chen et al. (2023). Accelerating Large Language Model Decoding with Speculative Sampling](https://arxiv.org/abs/2302.01318) introducción simultánea; prueba limpia de rechazo de Bernoulli.
  Traducción: simultáneamente publicado; traducción: traducción: traducción: traducción: traducción: traducción: traducción: traducción: traducción: traducción: traducción: traducción: traducción: traducción: traducción: traducción: traducción: traducción: traducción: traducción: traducción: traducción: traducción: traducción: traducción: traducción: traducción: traducción: traducción: traducción: traducción: traducción: traducción: traducción: traducción: traducción: traducción: traducción: traducción: traducción: traducción: traducción: traducción: traducción: traducción: traducción: traducción: traducción: traducción: traducción: traducción: traducción: traducción: traducción: traducción: traducción: traducción: traducción: traducción: traducción: traducción: traducción: traducción: traducción: traducción: traducción: traducción: traducción: traducción: traducción: traducción: traducción: traducción: traducción: traducción: traducción: traducción: traducción: traducción: traducción: traducción: traducción: traducción: traducción: traducción.
- [Cai et al. (2024). Medusa: Simple LLM Inference Acceleration Framework with Multiple Decoding Heads](https://arxiv.org/abs/2401.10774) Papel de Medusa; verificación de la atención al árbol.
  El tema es el tema de la historia de la historia de la ciencia.
- [Li et al. (2024). EAGLE: Speculative Sampling Requires Rethinking Feature Uncertainty](https://arxiv.org/abs/2401.15077) EAGLE-1; proyecto con condición de estado oculto.
  El proyecto de ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley.
- [Li et al. (2024). EAGLE-2: Faster Inference of Language Models with Dynamic Draft Trees](https://arxiv.org/abs/2406.16858) EAGLE-2; profundidad dinámica del árbol.
  El tema de la película es el tema de la película.
- [Li et al. (2025). EAGLE-3: Scaling up Inference Acceleration of Large Language Models via Training-Time Test](https://arxiv.org/abs/2503.01840)- El Águila-3.
  El ejército de los Estados Unidos ha liberado a los alemanes de la guerra.
- [Fu et al. (2024). Break the Sequential Dependency of LLM Inference Using Lookahead Decoding](https://arxiv.org/abs/2402.02057) Mirando hacia adelante, sin plan de enfoque.
  En el texto original, el texto se encuentra en el texto original.
- [vLLM docs — Speculative Decoding](https://docs.vllm.ai/en/latest/features/spec_decode.html) referencia canónica de producción con las cuatro estrategias conectadas.
  La producción de la información se desarrolla en el contexto de la investigación.
- [SafeAILab / EAGLE reference implementation](https://github.com/SafeAILab/EAGLE) el código de referencia de EAGLE-1/2/3.
  En el caso de los ejemplos de la lengua inglesa, el nombre de la lengua inglesa es "Eagle".
