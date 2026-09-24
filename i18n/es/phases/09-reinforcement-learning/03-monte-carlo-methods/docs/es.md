# Métodos de Monte Carlo Aprender de los episodios completos Método de Monte Carlo Aprender de los ciclos completos

> La programación dinámica necesita un modelo. Monte Carlo sólo necesita episodios. ejecuta la política, observa los rendimientos, promedio. La idea más simple en RL  y la que desbloquea todo aguas abajo.

> **【中文解读】**动态规划需要已知环境模型,蒙特卡洛 sólo necesita un ciclo completo de datos: ejecutar estrategias, observar reportajes, obtener media.

**Type:** Build | **类型:** 动手
**Languages:** Python | **语言:** Python
**Prerequisites:** Phase 9 · 01 (MDPs), Phase 9 · 02 (Dynamic Programming) | **前置知识:** Phase 9 · 01 (MDP), Phase 9 · 02 (动态规划)
**Time:** ~75 minutes | **时间:** ~75 分钟

## El problema es la introducción del problema

La programación dinámica es elegante, pero asume que puedes hacer consultas.`P(s' | s, a)`En el mundo real casi nada funciona de esa manera. Un robot no puede calcular analíticamente la distribución de los píxeles de la cámara después de un par común. Un algoritmo de precios no puede integrarse sobre cada reacción posible del cliente.

> La planificación es muy buena, pero supongamos que puedes consultar cada estado y movimiento.`P(s' | s, a)`◊ en realidad casi nada funciona así ◊ los dispositivos no pueden resolver la distribución de las imágenes de los elementos de la máquina ◊ los algoritmos de fijación de precios no pueden hacer frente a todas las reacciones de los clientes posibles ◊ Los sistemas de fijación de datos no pueden hacer referencia a los tokens ◊ los registros de todas las reacciones posibles ◊

Necesitas un método que sólo necesite la capacidad de tomar muestras del medio ambiente. ejecutar la política. obtener una trayectoria`s_0, a_0, r_1, s_1, a_1, r_2, …, s_T`Usalo para estimar los valores.

> Necesitas un método que sólo necesite un método de la toma de agua del ambiente.`s_0, a_0, r_1, s_1, a_1, r_2, …, s_T`Usándolo para calcular el valor.

El cambio de DP a MC es filosóficamente importante: pasamos de *modelo conocido + copia de seguridad exacta* a *desarrollo de muestras + retorno promedio*. La varianza salta, pero la aplicabilidad explota. Cada algoritmo RL después de esta lección  TD, Q-learning, REINFORCE, PPO, GRPO  es un estimador de Monte Carlo en el corazón, a veces con arranque en capas arriba.

> La transición del DP al MC es importante en la filosofía: nos desplazamos de los modelos conocidos+ reservas precisas* a los modelos de rollout+ rendimiento medio*──diferencia aumentada, pero el alcance de aplicación creció explosivamente── cada algoritmo RL TD、Q-learning、REINFORCE、PPO、GRPO es en esencia un calculador de montaña, a veces superpuesto por sí mismo.

> **【中文解读】**Desde el DP hasta el MC, el cambio central: desde el modelo conocido + cálculo preciso "a la "trajectoria de la muestra + el rendimiento medio" ∼ la diferencia aumentó, pero el alcance de aplicación se expandió explosivamente ∼PPO ∼RLHF son en esencia variaciones de los MC  estimadores ∼

> **【拓展：LLM中的MC】**En el entrenamiento RLHF de ChatGPT, para cada instante 采样多个答案、计算平均奖励

## El concepto central.

![Monte Carlo: rollout, compute returns, average; first-visit vs every-visit](../assets/monte-carlo.svg)

**The core idea, in one line:** `V^π(s) = E_π[G_t | s_t = s] ≈ (1/N) Σ_i G^{(i)}(s)`donde`G^{(i)}(s)`se observan resultados tras las visitas a `s`en el marco de la política `π`¿ Qué ?

> **核心思想，一行概括：** `V^π(s) = E_π[G_t | s_t = s] ≈ (1/N) Σ_i G^{(i)}(s)`, entre ellos `G^{(i)}(s)`Es en estrategia.`π`Siguiente visita`s`时观测到的回报──

> **【中文解读】**MC  evaluación de núcleo: estado = valor medio de los comentarios realizados durante el estado.`V_new = V_old + α(target - V_old)`Es el puente de todos los algoritmos modernos de RL.

**First-visit vs every-visit MC.**Dado un episodio que visita el estado `s`En el caso de las primeras visitas, el MC cuenta solo el retorno de la primera visita; en cada visita, el MC cuenta todas las visitas. Ambas son imparciales en el límite.

> **首次访问 vs 每次访问 MC。**                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             `s`El primer visitante de MC sólo calcula el primer visitante de MC sólo calcula el primer visitante de MC.

**Incremental mean.**En lugar de almacenar todos los resultados, actualice el promedio de ejecución:

`V_n(s) = V_{n-1}(s) + (1/n) [G_n - V_{n-1}(s)]`

Reorganizar: `V_new = V_old + α · (target - V_old)`con`α = 1/n`- Cambiar .`1/n`para un tamaño de paso constante `α ∈ (0, 1)`y obtienes un estimador de MC no estacionario que rastrea los cambios en`π`Ese movimiento es el salto completo de MC a TD a todos los algoritmos modernos de RL.

> **增量均值。**No se almacena todo el rendimiento, sino que se actualiza el valor medio de la operación.`1/n`替换为常数步长                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                      `α ∈ (0, 1)`¡Tengo un seguimiento!`π`                                                                                                                                                                                                                                                              

**Exploration is now a problem.**DP tocó a todos los estados por el recuento. MC sólo ve los estados las visitas de política.`π`Es determinista, regiones enteras del espacio del estado nunca se muestran, y sus estimaciones de valor permanecen en cero para siempre.

> **探索现在成了问题。**DP 通过枚举触及每个状态──MC sólo puede ver el estado de la estrategia 访问──如果`π`Es cierto que la totalidad del espacio de estado nunca será tomada, su valor se estima en siempre para cero.

> **【中文解读】**探索问题:DP 能遍历所有状态,MC sólo puede ver los estrategios visitados estado.

1. **Exploring starts.**Comience cada episodio desde un par aleatorio (s, a). Garantiza la cobertura; poco realista en la práctica (no se puede "resetar" un robot a un estado arbitrario).
   **探索起点。**Cada recorrido desde el momento en que se inicia, se asegura que se cubre; en realidad, no se puede "reponer" el aparato en cualquier estado.
2. **ε-greedy.**Actúa codicioso en el actual Q, pero con probabilidad.`ε`Todos los pares de estados de acción se muestran de manera asimptotica.
   **ε-贪心。**A la actualidad, la tasa de pérdida de ingresos es de 1,5% en el año.`ε`随机选动作── Todos los estados-动作 se han adoptado gradualmente──
3. **Off-policy MC.**Recoger datos bajo una política de comportamiento `μ`, aprender sobre la política de objetivo `π`La varianza es alta, pero es el puente a los métodos de repetición como DQN.
   **离策略 MC。**En estrategias de comportamiento`μ`Recolección de datos, a través de la importancia de la estrategia de objetivos de aprendizaje`π` Alta distancia, pero es el camino hacia DQN 等回放缓冲方法的桥梁。

**Monte Carlo Control.**Evaluar → mejorar → evaluar, al igual que la iteración de políticas, pero la evaluación se basa en muestras:

1. - ¿ Qué ?`π`, conseguir un episodio.
2. Actualización `Q(s, a)`de los resultados observados.
3. ¿ Qué haces ?`π`¡ ¡ ¡ ¡ ¡ ¡ ¡ El hombre codicioso !`Q`¿ Qué ?
4. Repito, ¿qué quieres?

Converge a `Q*`y `π*`con probabilidad 1 en condiciones suaves (cada par visitado con infinidad de frecuencia, `α`satisface a Robbins-Monro).

> **蒙特卡洛控制。**评估 → 改进 → 评估,就像策略代, pero evaluar basándose en la adopción.`α`满足 Robbins-Monro), en la probabilidad 1 收到 `Q*`Y `π*`¿Qué es eso?

## Construye y realiza.
```figure
epsilon-greedy
```

## Construye el mismo

### Paso 1: despliegue → lista de (s, a, r)

```python
def rollout(env, policy, max_steps=200):
    trajectory = []
    s = env.reset()
    for _ in range(max_steps):
        a = policy(s)
        s_next, r, done = env.step(s, a)
        trajectory.append((s, a, r))
        s = s_next
        if done:
            break
    return trajectory
```

No hay modelo, sólo `env.reset()`y `env.step(s, a)`La misma interfaz que un entorno de gimnasio pero despojado.

> No necesito un modelo, sólo necesito.`env.reset()`Y `env.step(s, a)`                                                                                                                                                                                                                                                              

### Paso 2: Regresos de cálculo (varrilamiento inverso)

```python
def returns_from(trajectory, gamma):
    returns = []
    G = 0.0
    for _, _, r in reversed(trajectory):
        G = r + gamma * G
        returns.append(G)
    return list(reversed(returns))
```

Un pase,`O(T)`La recurrencia hacia atrás .`G_t = r_{t+1} + γ G_{t+1}`evita la re-suma.

> Una vez más,`O(T)` Reversa hacia el`G_t = r_{t+1} + γ G_{t+1}`避免了重复求和──

### Paso 3: Evaluación de la primera visita de MC

```python
def mc_policy_evaluation(env, policy, episodes, gamma=0.99):
    V = defaultdict(float)
    counts = defaultdict(int)
    for _ in range(episodes):
        trajectory = rollout(env, policy)
        returns = returns_from(trajectory, gamma)
        seen = set()
        for t, ((s, _, _), G) in enumerate(zip(trajectory, returns)):
            if s in seen:
                continue
            seen.add(s)
            counts[s] += 1
            V[s] += (G - V[s]) / counts[s]
    return V
```

Tres líneas hacen el trabajo: marcar el estado visto en la primera visita, el recuento de incrementos, la media de actualización en ejecución.

> Tres行代码完成工作: marcar el estado de la primera visita, aumentar el número de contactos, actualizar el promedio de operaciones.

### Paso 4: control de MC codicioso (en política)

```python
def mc_control(env, episodes, gamma=0.99, epsilon=0.1):
    Q = defaultdict(lambda: {a: 0.0 for a in ACTIONS})
    counts = defaultdict(lambda: {a: 0 for a in ACTIONS})

    def policy(s):
        if random() < epsilon:
            return choice(ACTIONS)
        return max(Q[s], key=Q[s].get)

    for _ in range(episodes):
        trajectory = rollout(env, policy)
        returns = returns_from(trajectory, gamma)
        seen = set()
        for (s, a, _), G in zip(trajectory, returns):
            if (s, a) in seen:
                continue
            seen.add((s, a))
            counts[s][a] += 1
            Q[s][a] += (G - Q[s][a]) / counts[s][a]
    return Q, policy
```

### Paso 5: comparación con el estándar de oro DP

Su estimativa de MC de `V^π`En la práctica: 50.000 episodios en 4×4 GridWorld te lleva dentro de `~0.1`de la respuesta del DP.

> ¿ Qué ?`V^π`El resultado del estudio de la lección 02 es conforme a la evaluación de la MC en el número de recopilaciones → ∞ 时应 y el resultado del estudio 02 △ en la práctica:`~0.1`En el interior.

## Las trampas

- **Infinite episodes.**MC requiere que los episodios se terminen. Si su política puede circular para siempre, cap.`max_steps`GridWorld con una política aleatoria rotineamente veces fuera  que es normal, sólo asegúrese de contarlo correctamente.
  **无限回合。**MC 要求回合*终止*──如果策略可能永远循环,设置 `max_steps`La limitación será vista como un fracaso oculto.
- **Variance.**MC utiliza devoluciones completas. En episodios largos, la variación es enorme  una recompensa desafortunada en los turnos finales `V(s_0)`El método TD (lección 04) reduce esto mediante bootstrapping.
  **方差。**MC utiliza el reporte completo.`V(s_0)`◊TD 方法(Ley 04) a través de la propia acción para reducir la diferencia.
- **State coverage.**El MC codicioso en un Q fresco con corbatas sólo intentará una acción.
  **状态覆盖。**Nuevo Q 上的贪心 MC sólo intentará un movimiento. Tú* tienes que* explorar.
- **Non-stationary policies.**Si ...`π`En el caso de los controles de MC, los resultados anteriores son de una política diferente.
  **非平稳策略。**Si es que`π`变化(如 MC 控制中),旧回报来自不同策略──常数 α MC 处理此问题;样本平均 MC 不能──
- **Off-policy importance sampling.**Los pesos .`π(a|s)/μ(a|s)`La variación explotará con el horizonte, el límite con la IS ponderada por decisión o el cambio a TD.
  **离策略重要性采样。**权重         `π(a|s)/μ(a|s)`En el trayecto acumulación de fases multiplicadas. Diferencias con el campo de explosiones.

## Usalo con el marco de ejecución

El papel de los métodos de Monte Carlo para 2026:

> 2026 años de Montcarlo método de papel:

| Use case | Why MC |
|----------|--------|
| Use case / 用例 | Why MC / 为什么用 MC |
| Short-horizon games (blackjack, poker) / 短视野游戏（二十一点、扑克） | Episodes terminate naturally; returns are clean. / 回合自然终止；回报干净。 |
| Offline evaluation of a logged policy / 离线评估已记录的策略 | Average discounted returns over stored trajectories. / 对存储轨迹取折扣回报平均。 |
| Monte Carlo Tree Search (AlphaZero) / 蒙特卡洛树搜索 | MC rollouts from tree leaves guide selection. / 树叶的 MC rollout 指导选择。 |
| LLM RL evaluation / LLM RL 评估 | Compute average reward over sampled completions for a given policy. / 对给定策略的采样完成计算平均奖励。 |
| Baseline estimation in PPO / PPO 中的基线估计 | The advantage target `A_t = G_t - V(s_t)` uses an MC `G_t`. / 优势目标使用 MC 的 `G_t`。 |
| Teaching RL / 教学 RL | Simplest algorithm that actually works — strip bootstrapping to see the core. / 最简单且有效的算法——去掉自举看核心。 |

Los algoritmos modernos de RL profundo (PPO, SAC) interpolan entre MC puro (retorno completo) y TD puro (bootstrap de un paso) a través de `n`Los dos puntos finales son ejemplos del mismo estimador.

> 现代深度 RL 算法 PPO、SAC) por el que`n`步回报或 GAE 在纯 MC (M) 完全回报) 和纯 TD (TD) 单步自举) 之间插值──两个端点都是同样估计器的实例──

## Envíe el producto .

Salvo como`outputs/skill-mc-evaluator.md`¿Qué es esto ?

```markdown
---
name: mc-evaluator
description: Evaluate a policy via Monte Carlo rollouts and produce a convergence report with DP-comparison if available.
version: 1.0.0
phase: 9
lesson: 3
tags: [rl, monte-carlo, evaluation]
---

Given an environment (episodic, with reset+step API) and a policy, output:

1. Method. First-visit vs every-visit MC. Reason.
2. Episode budget. Target number, variance diagnostic, expected standard error.
3. Exploration plan. ε schedule (if needed) or exploring starts.
4. Gold-standard comparison. DP-optimal V* if tabular; otherwise a bound from a Q-learning / PPO baseline.
5. Termination check. Max-step cap, timeouts, handling of non-terminating trajectories.

Refuse to run MC on non-episodic tasks without a finite horizon cap. Refuse to report V^π estimates from fewer than 100 episodes per state for tabular tasks. Flag any policy with zero-variance actions as an exploration risk.
```

## Los ejercicios.

1. **Easy.**Implemente la evaluación de la primera visita de MC de la política uniforme al azar en 4×4 GridWorld. ejecuta 10.000 episodios.`V(0,0)`como función del recuento de episodios frente a la respuesta de DP.
   > **练习1：**实现 MC 评估,将 V(0,0) 随回合数的收曲线与 DP 基准对比──
2. **Medium.**Implementar el control de MC con `ε ∈ {0.01, 0.1, 0.3}`Comparar el retorno medio después de 20.000 episodios. ¿Cómo es la curva? ¿Dónde vive el compromiso de variación de sesgo?
   > **练习2：**Us diferén ε 值做 MC 控制, observar explorar-utilizar权衡──
3. **Hard.**Implementar *extrapolíticas* MC con muestreo de importancia: recoger datos en el marco de una política uniforme aleatoria `μ`, estimación `V^π`para la política óptima determinista `π`Comparar el IS puro vs. por decisión IS vs. IS ponderado. ¿Cuál tiene la menor variación?
   > **练习3：**实现离策略 MC 重要性采样), comparar diferentes IS 方差的差异──

## Términos clave .

| Term | What people say | What it actually means |
|------|-----------------|-----------------------|
| Monte Carlo | "Random sampling" / 蒙特卡洛 | Estimate expectations by averaging over iid samples from the distribution. |
| Return `G_t` | "Future reward" / 回报 | Sum of discounted rewards from step `t` to episode end: `Σ_{k≥0} γ^k r_{t+k+1}`. |
| First-visit MC | "Count each state once" / 首次访问 MC | Only the first visit in an episode contributes to the value estimate. |
| Every-visit MC | "Use all visits" / 每次访问 MC | Every visit contributes; slightly biased but more sample-efficient. |
| ε-greedy | "Exploration noise" / ε-贪心 | Pick greedy action with prob `1-ε`; random action with prob `ε`. |
| Importance sampling | "Correcting for sampling from the wrong distribution" / 重要性采样 | Reweight returns by `π(a\|s)/μ(a\|s)` products to estimate `V^π` from `μ` data. |
| On-policy | "Learn from my own data" / 在线策略 | Target policy = behavior policy. Vanilla MC, PPO, SARSA. |
| Off-policy | "Learn from someone else's data" / 离线策略 | Target policy ≠ behavior policy. Importance-sampled MC, Q-learning, DQN. |

## Más Leer más Leer más

- [Sutton & Barto (2018). Ch. 5 — Monte Carlo Methods](http://incompleteideas.net/book/RLbook2020.pdf) el tratamiento canónico.
- [Singh & Sutton (1996). Reinforcement Learning with Replacing Eligibility Traces](https://link.springer.com/article/10.1007/BF00114726) Análisis de primera visita frente a cada visita.
- [Precup, Sutton, Singh (2000). Eligibility Traces for Off-Policy Policy Evaluation](http://incompleteideas.net/papers/PSS-00.pdf) control de las variaciones y de las MC fuera de las políticas.
- [Mahmood et al. (2014). Weighted Importance Sampling for Off-Policy Learning](https://arxiv.org/abs/1404.6362) Estimadores modernos de IS de baja variación.
- [Tesauro (1995). TD-Gammon, A Self-Teaching Backgammon Program](https://dl.acm.org/doi/10.1145/203330.203343) la primera demostración empírica a gran escala de la auto-juego MC/TD convergiendo al juego sobrehumano; precursor conceptual de cada lección en la segunda mitad de esta fase.
