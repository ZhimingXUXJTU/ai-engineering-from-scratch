# Actor-Critico  A2C y A3C 演员-评论家  A2C y A3C

> ReINFORCE es ruidoso.`V̂(s)`, restar de la vuelta, y usted obtiene una ventaja que tiene la misma expectativa pero mucho menor varianza. Eso es actor-crítica. A2C lo ejecuta sincrónicamente; A3C lo ejecuta a través de hilos. Ambos son el modelo mental para cada método moderno de RL profundo.

> **【中文解读】**REINFORCE 方差太大──加入一个"评论家"(Critical)学习 V̂(s), usarlo como base de la construcción de la función de ventaja A = G - V̂(s), la expectativa no cambia pero la diferencia disminuye considerablemente──

**Type:** Build | **类型:** 动手
**Languages:** Python | **语言:** Python
**Prerequisites:** Phase 9 · 04 (TD Learning), Phase 9 · 06 (REINFORCE) | **前置知识:** Phase 9 · 04 (TD 学习), Phase 9 · 06 (REINFORCE)
**Time:** ~75 minutes | **时间:** ~75 分钟

## El problema es la introducción del problema

Vanilla ReINFORCE funciona, pero su variación es terrible.`G_t`puede oscilar sobre un factor de 10 entre episodios.`∇ log π`y la media produce un estimador de gradientes que toma miles de episodios para mover la póliza a la misma distancia que podrías moverla con muchas menos actualizaciones de DQN.

> El primer refuerzo es efectivo, pero la diferencia es muy mala.`G_t`En el tiempo puede ocurrir 10 veces el ruido.`∇ log π`En el caso de los sistemas de evaluación de gradientes, el nivel de escala es el nivel de escala de la escala de escala.

La variación proviene del uso de resultados crudos. Si restas una línea de base `b(s_t)` cualquier función de estado, incluyendo un valor aprendido  la expectativa es inmutable y la varianza disminuye.`V̂(s_t)`Ahora la cantidad multiplicándose`∇ log π`es la * ventaja*:

`A(s, a) = G - V̂(s)`

> 方差来自使用原始回报──如果减去基线 `b(s_t)` Cualquier función de estado, incluyendo el valor del aprendizaje  la expectativa no cambia pero el diferencial disminuye                                                                                                                                                                                                                                                  `V̂(s_t)`Ahora me voy a llevar.`∇ log π`La cantidad es la ventaja.

Una acción es buena si produjo un rendimiento superior al promedio; mala si está por debajo. REINFORCE con un crítico aprendido es *actor-crítico*. El crítico le da al actor un maestro de baja variación. Este es cada método de política profunda después de 2015 (A2C, A3C, PPO, SAC, IMPALA).

> 动作好如果产生高于平均的回报;差如果低于──带学习批评的 REINFORCE就是 *Actor-Critic*──Critic 给 Actor一个低方差的老师──这是2015年后每深度策略方法(A2C、A3C、PPO、SAC、IMPALA)──

## El concepto central.

![Actor-critic: policy net plus value net, TD residual as advantage](../assets/actor-critic.svg)

**Two networks, one shared loss:**

> **两个网络，一个共享损失：**

- **Actor** `π_θ(a | s)`La política. Muestras para actuar.
  **Actor** `π_θ(a | s)`El método de acción es el método de formación de la estrategia.
- **Critic** `V_φ(s)`Estimativas de retorno esperado del estado.`(V_φ(s) - target)²`¿ Qué ?
  **Critic** `V_φ(s)`El resultado de la evaluación de la situación se reduce al mínimo.`(V_φ(s) - target)²`¿Qué es eso?

**The advantage.**Dos formularios estándar:

> **优势函数。**两种标准形式:

- *Vantaje de la MC:* `A_t = G_t - V_φ(s_t)`- Inparcial, mayor variación.
  *MC 优势:* 无偏,方差较高──
- *Vantaje de la TD:* `A_t = r_{t+1} + γ V_φ(s_{t+1}) - V_φ(s_t)`. Prejuicios (usados `V_φ`), una varianza mucho menor.`δ_t`¿ Qué ?
  *TD 优势:* 有偏差(使用 `V_φ`),方差远低── también llamado *TD残差* `δ_t`¿Qué es eso?

**n-step advantage.**Interpolar entre los dos:

`A_t^{(n)} = r_{t+1} + γ r_{t+2} + … + γ^{n-1} r_{t+n} + γ^n V_φ(s_{t+n}) - V_φ(s_t)`

`n = 1`es TD puro. `n = ∞`La mayoría de las implementaciones utilizan `n = 5`para Atari, `n = 2048`para el PPO en MuJoCo.

> **n 步优势。**Entre ambos se interpone el valor.`n = 1`Es pura TD.`n = ∞`Es el MC. La mayoría de los ejecutantes de Atari usan`n = 5`, MuJoCo de PPO de arriba Usando`n = 2048`¿Qué es eso?

**Generalized Advantage Estimation (GAE).**Schulman et al. (2016) propuso una media ponderada exponencialmente sobre todas las ventajas de n-pasos:

`A_t^{GAE} = Σ_{l=0}^{∞} (γλ)^l δ_{t+l}`

con`λ ∈ [0, 1]`- ¿ Qué ?`λ = 0`es TD (baja varianza, alto sesgo). `λ = 1`es MC (alta varianza, imparcial). `λ = 0.95`es el 2026 de la tune  por defecto hasta que la dial de sesgo / variación es donde lo desea.

> **【中文解读】**GAE(广义优势估计) es una mejora clave de Actor-Critic: a través de índices de aumento de la media de los beneficios, se encuentra el mejor equilibrio entre los diferenciales y los diferenciales.

> **【拓展：GAE 在 RLHF 中的应用】**En el caso de los programas de LLM, el "estado" es la secuencia de tokens generados, el "movimiento" es el siguiente token, el "recompensa" proviene del modelo de recompensa.

**A2C: synchronous advantage actor-critic.**Recolectar`T`pasos de la otra parte `N`En el juego de juego, el juego de juego es un juego de juego paralelo.

> **A2C：同步优势 Actor-Critic。**En el`N`个并行环境中收集                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                       `T`步──计算每步优势──在合并批次上更新 Actor 和 Critic──重复──A3C's más sencillo、 más extendido hermano──

**A3C: asynchronous advantage actor-critic.**Mnih et al. (2016). Spawn `N`Cada trabajador calcula los gradientes localmente en su propio despliegue, luego los aplica sincrónicamente a un servidor de parámetros compartido. No se necesita buffer de repetición  los trabajadores se descorregan ejecutando diferentes trayectorias. A3C demostró que se puede entrenar en CPUs a escala. En 2026, A2C basado en GPU (envases paralelos en lote) domina porque las GPUs quieren lotes grandes.

> **A3C：异步优势 Actor-Critic。**Mnih 等人 (2016)。 iniciación `N`个工作线程, cada una de ellas ejecuta un ambiente. Cada una de ellas se aplica a un servidor de parámetros compartidos.

**The combined loss.**

`L(θ, φ) = -E[ A_t · log π_θ(a_t | s_t) ]  +  c_v · E[(V_φ(s_t) - G_t)²]  -  c_e · E[H(π_θ(·|s_t))]`

Tres términos: pérdida de la política, regresión de valor, bonificación de entropía. `c_v ~ 0.5`¿ Qué ?`c_e ~ 0.01`son puntos de partida canónicos.

> **组合损失。**Tres: estrategia de pérdida de la magnitud de la pérdida de la calidad, de la rentabilidad, de la rentabilidad, de la rentabilidad, de la rentabilidad, de la rentabilidad, de la rentabilidad, de la rentabilidad, de la rentabilidad, de la rentabilidad, de la rentabilidad, de la rentabilidad, de la rentabilidad, de la rentabilidad, de la rentabilidad, de la rentabilidad, de la rentabilidad, de la rentabilidad, de la rentabilidad, de la rentabilidad, de la rentabilidad, de la rentabilidad, de la rentabilidad, de la rentabilidad, de la rentabilidad, de la rentabilidad, de la rentabilidad, de la rentabilidad, de la rentabilidad, de la rentabilidad, de la rentabilidad, de la rentabilidad y de la rentabilidad.`c_v ~ 0.5`¿Qué es esto?`c_e ~ 0.01`Es el típico valor inicial.

> **【中文解读】**El grupo de actores-criticos se encuentra en una posición de equilibrio entre el grupo de actores y el grupo de actores.

> **【拓展：GAE→PPO→RLHF】**GAE (广义优势估算) es el componente central de PPO, mientras que PPO es el algoritmo estándar de entrenamiento ChatGPT RLHF ∙∙λ=0.95 es el valor predeterminado para 2026, para lograr un equilibrio entre los diferenciales y los diferenciales ∙ Comprender GAE es comprender el método de estimación de ventajas más clave en el gran modelo de entrenamiento ∙

## Construye y realiza.
```figure
actor-critic
```

## Construye el mismo

### Paso 1: un crítico

Crítico lineal `V_φ(s) = w · features(s)`actualizada con MSE:

```python
def critic_update(w, x, target, lr):
    v_hat = dot(w, x)
    err = target - v_hat
    for j in range(len(w)):
        w[j] += lr * err * x[j]
    return v_hat
```

En un entorno tabular el crítico converge en unos cientos de episodios. En Atari, reemplaza al crítico lineal con un compartimento de CNN trunk + valor cabeza.

> 线性批评 `V_φ(s) = w · features(s)`Usar MSE 更新──在表格环境中几百回合就收──在 Atari 上, sustituido por compartir CNN 主干 + 值头──

### Paso 2: ventaja de n-paso

Dado el rollout de longitud `T`y una final sin salida .`V(s_T)`¿Qué es esto ?

```python
def compute_advantages(rewards, values, gamma=0.99, lam=0.95, last_value=0.0):
    advantages = [0.0] * len(rewards)
    gae = 0.0
    for t in reversed(range(len(rewards))):
        next_v = values[t + 1] if t + 1 < len(values) else last_value
        delta = rewards[t] + gamma * next_v - values[t]
        gae = delta + gamma * lam * gae
        advantages[t] = gae
    returns = [a + v for a, v in zip(advantages, values)]
    return advantages, returns
```

`returns`es el objetivo crítico. `advantages`es lo que se multiplica `∇ log π`¿ Qué ?

> `returns`Es un objetivo crítico.`advantages`Es un viaje .`∇ log π`La cantidad de...

### Paso 3: actualización combinada

```python
for step_i, (x, a, _r, probs) in enumerate(traj):
    adv = advantages[step_i]
    target_v = returns[step_i]

    # critic
    critic_update(w, x, target_v, lr_v)

    # actor
    for i in range(N_ACTIONS):
        grad_logpi = (1.0 if i == a else 0.0) - probs[i]
        for j in range(N_FEAT):
            theta[i][j] += lr_a * adv * grad_logpi * x[j]
```

En política, una implementación por actualización, tasas de aprendizaje separadas para actores y críticos.

> En línea estrategia, cada vez más un rollout, Actor y Crítico utiliza diferentes tasas de aprendizaje.

### Paso 4: paralelación (A3C vs. A2C)

- **A3C:**¡ ¡ ¡ ¡ ¡ ¡ ¡ ¡ ¡ ¡ ¡ ¡ ¡ ¡ ¡ ¡ ¡ ¡ ¡ ¡ ¡ Qué bien !`N`Cada uno ejecuta su propio env y su propio pase hacia adelante. Periódicamente empuje actualizaciones de gradiente a un maestro compartido. No hay cerraduras en el maestro  carreras están bien, sólo añaden ruido.
- **A2C:**¿ Qué ?`N`Env instancias en un solo proceso, apilar las observaciones en un `[N, obs_dim]`Batch, batch forward pass, batch backward pass. mayor utilización de GPU, determinista, más fácil de razonar.

Nuestro código de juguete es un hilo único para la claridad; reescribir a lotes de A2C es tres líneas de numpy.

> Nuestro código de juguetes es de un solo tramo para mantener la claridad; reescribir para el lote A2C sólo necesita tres líneas de numpy.

## Las trampas

- **Critic bias before actor gradient.**Si el crítico es aleatorio, su línea de base no es informativa y usted está entrenando en ruido puro. Calentar al crítico durante unos cientos de pasos antes de activar el gradiente de política, o utilizar una tasa de aprendizaje de actores lenta.
  **Actor 梯度之前的 Critic 偏差。**Si el crítico es casual, sin información, te entrenas en ruido puro.
- **Advantage normalization.**Normaliza las ventajas a cero promedio/unidad-std por lote. Estabiliza el entrenamiento masivamente a un costo cercano a cero.
  **优势归一化。**Cada lote se va a reducir a un valor medio/unidad de diferencia.
- **Shared trunk.**Utilice un extractor de características compartidas para actores y críticos en entradas de imagen. cabezas separadas. Las características compartidas son de viaje libre en ambas pérdidas.
  **共享主干。**图像输入时使用共享特征提取器──分开的头──共享特征同时从两个损失中获益──
- **On-policy contract.**A2C reutiliza datos para exactamente una actualización. Más y su gradiente es sesgado (corrección de muestreo de importancia es lo que agrega PPO).
  **在线策略约束。**A2C 恰好用数据做一次更新.
- **Entropy collapse.**Sin ...`c_e > 0`La política se vuelve casi determinista en unos cientos de actualizaciones y deja de explorar.
  **熵坍缩。**No hay .`c_e > 0`, la estrategia se ha vuelto cercana a la certeza y ha dejado de explorar después de cientos de actualizaciones.
- **Reward scale.**Las magnitudes de ventaja dependen de la escala de recompensa. Normaliza las recompensas (por ejemplo, la división de run-std) para magnitudes de gradiente consistentes en las tareas.
  **奖励尺度。** La calificación de la ventaja depende de la calificación de la recompensa

## Usalo con el marco de ejecución

A2C/A3C rara vez son la elección final en 2026 pero son la arquitectura que todo más tarde refinará:

> A2C/A3C en 2026 son muy pocas las opciones finales, pero son más tarde una estructura que refinará todos los métodos:

| Method | Relation to A2C |
|--------|----------------|
| Method / 方法 | Relation to A2C / 与 A2C 的关系 |
| PPO | A2C + clipped importance ratio for multi-epoch updates / A2C + 裁剪重要性比率用于多轮更新 |
| IMPALA | A3C + V-trace off-policy correction / A3C + V-trace 离策略修正 |
| SAC (Phase 9 · 07) | Off-policy A2C with a soft-value critic (next lesson) / 离策略 A2C + 软值 Critic |
| GRPO (Phase 9 · 12) | A2C without the critic — group-relative advantage / 无 Critic 的 A2C——组相对优势 |
| DPO | A2C collapsed into a preference-ranking loss, no sampling / 折叠为偏好排名损失的 A2C |
| AlphaStar / OpenAI Five | A2C with league training + imitation pre-training / A2C + 联盟训练 + 模仿预训练 |

Si ves "vantaj" en un artículo de 2026, piensa en actor-crítica.

> Si en el artículo de 2026 ves "Unecesidades", piensa en el Actor-Crítico.

## Envíe el producto .

Salvo como`outputs/skill-actor-critic-trainer.md`¿Qué es esto ?

```markdown
---
name: actor-critic-trainer
description: Produce an A2C / A3C / GAE configuration for a given environment, with advantage estimation and loss weights specified.
version: 1.0.0
phase: 9
lesson: 7
tags: [rl, actor-critic, gae]
---

Given an environment and compute budget, output:

1. Parallelism. A2C (GPU batched) vs A3C (CPU async) and the number of workers.
2. Rollout length T. Steps per env per update.
3. Advantage estimator. n-step or GAE(λ); specify λ.
4. Loss weights. `c_v` (value), `c_e` (entropy), gradient clip.
5. Learning rates. Actor and critic (separate if using).

Refuse single-worker A2C on environments with horizon > 1000 (too on-policy, too slow). Refuse to ship without advantage normalization. Flag any run with `c_e = 0` and observed entropy < 0.1 as entropy-collapsed.
```

## Los ejercicios.

1. **Easy.**Entraen actor-crítico con ventaja MC (`G_t - V(s_t)`Comparar la eficiencia de la muestra con la línea de referencia de REINFORCE con el promedio de funcionamiento de la lección 06.
2. **Medium.**Cambiar a la ventaja residual TD (`r + γ V(s') - V(s)`¿Cuánto disminuye la variación de los lotes de ventajas?
3. **Hard.**Implementar GAE(λ).`λ ∈ {0, 0.5, 0.9, 0.95, 1.0}`¿Dónde está el punto de equilibrio de la variación/previación para esta tarea?

## Términos clave .

| Term | What people say | What it actually means |
|------|-----------------|-----------------------|
| Actor | "The policy net" / 演员（策略网络） | `π_θ(a\|s)`, updated by policy gradient. |
| Critic | "The value net" / 评论家（值网络） | `V_φ(s)`, updated by MSE regression to returns / TD targets. |
| Advantage | "How much better than average" / 优势函数 | `A(s, a) = Q(s, a) - V(s)` or its estimators. Multiplier for `∇ log π`. |
| TD residual | "δ" / TD 残差 | `δ_t = r + γ V(s') - V(s)`; one-step advantage estimate. |
| GAE | "The interpolation knob" / 广义优势估计 | Exponentially weighted sum of n-step advantages, parameterized by `λ`. |
| A2C | "Synchronous actor-critic" / 同步演员-评论家 | Batched across envs; one gradient step per rollout. |
| A3C | "Async actor-critic" / 异步演员-评论家 | Worker threads push gradients to a shared param server. Original paper; less common in 2026. |
| Bootstrap | "Use V at the horizon" / 自举截断 | Truncate the rollout, add `γ^n V(s_{t+n})` to close the sum. |

## Más Leer más Leer más

- [Mnih et al. (2016). Asynchronous Methods for Deep Reinforcement Learning](https://arxiv.org/abs/1602.01783) A3C, el papel original de actores críticos sincronizados.
- [Schulman et al. (2016). High-Dimensional Continuous Control Using Generalized Advantage Estimation](https://arxiv.org/abs/1506.02438) GAE.
- [Sutton & Barto (2018). Ch. 13 — Actor-Critic Methods](http://incompleteideas.net/book/RLbook2020.pdf) fundamentos; emparejar esto con el capítulo 9 sobre aproximación de funciones cuando el crítico es una red neuronal.
- [Espeholt et al. (2018). IMPALA](https://arxiv.org/abs/1802.01561) escalable y distribuido de actores críticos con corrección fuera de la política de V-trace.
- [OpenAI Baselines / Stable-Baselines3](https://stable-baselines3.readthedocs.io/) implementaciones de producción A2C/PPO que valgan la pena leer.
- [Konda & Tsitsiklis (2000). Actor-Critic Algorithms](https://papers.nips.cc/paper/1786-actor-critic-algorithms) el resultado de convergencia fundamental para la descomposición actor-crítica en dos escalas.
