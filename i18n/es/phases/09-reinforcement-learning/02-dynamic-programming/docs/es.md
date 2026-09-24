# Programación dinámica Iteración de políticas y iteración de valores 动态规划 策略代与价值代

> La programación dinámica es RL con el engaño. Ya sabes las funciones de transición y recompensa; sólo se repite la ecuación de Bellman hasta que`V`o `π`El método de referencia es el que todos los métodos basados en muestreo intentan abordar.

> **【中文解读】**动态规划是强化学习的"作弊版"你已知环境的转移概率和奖励函数, sólo necesita repetir el método Bellman hasta el recibo.

**Type:** Build | **类型:** 动手
**Languages:** Python | **语言:** Python
**Prerequisites:** Phase 9 · 01 (MDPs) | **前置知识:** Phase 9 · 01 (MDP)
**Time:** ~75 minutes | **时间:** ~75 分钟

## El problema es la introducción del problema

Tiene un MDP con un modelo conocido: puede consultar `P(s' | s, a)`y `R(s, a, s')`Un gerente de inventario conoce la distribución de la demanda. un juego de mesa tiene transiciones deterministas. un mundo de cuadrícula es cuatro líneas de Python. tienes un *modelo*.

> Tienes un modelo conocido de MDP: puedes consultar cualquier estado-moción para el `P(s' | s, a)`Y `R(s, a, s')` El administrador de almacenes sabe la distribución de la demanda  El juego de tablero tiene una transferencia determinada  El mundo de la red es una cadena de Python  Tienes un modelo 

La RL libre de modelos (Q-learning, PPO, REINFORCE) fue inventada para el caso en el que no tienes un modelo  solo puedes tomar muestras del entorno. Pero cuando lo tienes, hay métodos más rápidos y mejores: programación dinámica. Bellman las diseñó en 1957.

> 无模型 RL(Q-learning、PPO、REINFORCE) es un concepto inventado para la situación de no tener modelos. You can only sample from the environment.  Pero cuando tienes modelos, hay métodos más rápidos y mejores:

> **【中文解读】**Cuando usted conoce el modelo ambiental ([[transfer probabilidad y función de recompensa]]), el plan de desarrollo puede ser preciso para obtener la mejor estrategia.

> **【拓展：AlphaZero/MCTS】**La búsqueda de la plataforma de búsqueda de árboles de AlphaZero (MCTS) es en esencia una versión diferente de la reserva de Bellman.

Los datos de la investigación de RL (GridWorld, FrozenLake, CliffWalking) se resuelven con DP para producir la política estándar de oro.`V*(s_0)`En tercer lugar, los métodos modernos de RL y planificación fuera de línea (MCTS, búsqueda de AlphaZero, RL basado en el modelo en la Fase 9 · 10) reiteran todos una copia de seguridad Bellman sobre un modelo aprendido o dado.

> Usted en 2026 años necesitan de ellos, por razones hay tres. Primero,RL en cada uno de los estudios de cada tipo de ambiente (GridWorld, FrozenLake, CliffWalking) todos usan DP para buscar soluciones para generar estrategias de oro estándar.`V*(s_0)`La evaluación con la respuesta DP es de 30%, tu aprendizaje Q tiene un error.

## El concepto central.

![Policy iteration and value iteration, side by side](../assets/dp.svg)

**Two algorithms, both fixed-point iteration on Bellman.**

> **两种算法，都是对 Bellman 方程做不动点迭代。**

> **【中文解读】**两种算法都是对贝尔曼方程做不动点代――策略代:交替执行"策略评估"和"策略改进"直到策略不变;值代:将两者合并为一步,直接取 max――两者最终收到同一个优值函数 V*──

**Policy iteration.**Alterna dos pasos hasta que la política deje de cambiar.

> **策略迭代。**交替执行两个步骤直到 la estrategia no cambie.

1. *Evaluación:* política dada `π`, computación `V^π`mediante la aplicación repetida `V(s) ← Σ_a π(a|s) Σ_{s',r} P(s',r|s,a) [r + γ V(s')]`hasta que converge.
   * evaluación:* 给定策略 `π`, Repeat Apply Bellman 方程 hasta `V^π`¿Qué es eso?
2. *Mejora: * dada `V^π`, hacer`π`codicioso W.R.T.`V^π`¿ Qué es esto ?`π(s) ← argmax_a Σ_{s',r} P(s',r|s,a) [r + γ V(s')]`¿ Qué ?
   *改进:* 给定 `V^π`, hacer `π`¿ Qué ?`V^π`贪心── es una especie de amor.

La convergencia está garantizada porque a) cada paso de mejora mantiene o`π`el mismo o aumentan estrictamente `V^π`Para algunos estados, (b) el espacio de las políticas deterministas es finito. generalmente converge en ~ 520 iteraciones externas incluso para grandes espacios de estados.

> La recepción es garantizada, porque (a) cada vez que se mejora o se mantiene`π`No cambia, o se debe aumentar de manera severa un estado.`V^π`,(b) El espacio de estrategia de determinación es limitado. Incluso para el espacio de estado grande, normalmente sólo se requieren ~5-20 veces la capa exterior.

**Value iteration.**Se desmorona la evaluación y la mejora en un solo barrido. Aplique la ecuación Bellman *optimalidad*:

`V(s) ← max_a Σ_{s',r} P(s',r|s,a) [r + γ V(s')]`

Repita hasta que`max_s |V_{new}(s) - V(s)| < ε`. Extraer la política al final tomando la acción codiciosa. Estrictamente más rápido por iteración  no hay bucle de evaluación interna  pero normalmente necesita más iteraciones para converger.

> **值迭代。**La evaluación y la mejora se combinan para una sola exploración. Aplicar el método Bellman * optimista*                                                                                                                                                                                                                                                   

**Generalized policy iteration (GPI).**La estructura unificadora. La función de valor y la política están bloqueadas en un bucle de mejora bidireccional; cualquier método que impulse ambos hacia la consistencia mutua (iteración de valores sincronizados, iteración de políticas modificadas, Q-learning, actor-critico, PPO) es una instancia de GPI.

> **【拓展：GPI→PPO/RLHF】**广义策略代 (GPI) es un marco de trabajo: Q-learning、Actor-Critic、PPO es en esencia un ejemplo de GPI, entiendo el GPI de DP, ya entiendes el ciclo de entrenamiento de RLHF 

**Why `γ < 1` matters.**El operador Bellman es un`γ`- contracción en la norma de sup: `||T V - T V'||_∞ ≤ γ ||V - V'||_∞`La contracción implica un punto fijo único y una convergencia geométrica.`γ < 1`y pierdes la garantía necesitas un horizonte finito o un estado terminal de absorción.

> **为什么 `γ < 1` 很重要。**Bellman está en su sub-fánculatura.`γ`- compresión de mapas. compresión significa único inactividad y geometría.`γ < 1`Por lo tanto, no hay ninguna garantía de que necesites un estado de visión o absorción limitada.

## Construye y realiza.
```figure
value-iteration-gamma
```

## Construye el mismo

### Paso 1: construir el modelo de MDP de GridWorld

Usamos el mismo 4x4 GridWorld de la Lección 01. Añadimos una variante estocástica: con probabilidad `0.1`El agente se desliza hacia una dirección perpendicular aleatoria.

> Usamos la misma 4×4 GridWorld en la lección 01... y añadimos una variable al azar: en probabilidad.`0.1`智能体会滑向随机垂直方向──

```python
SLIP = 0.1

def transitions(state, action):
    if state == TERMINAL:
        return [(state, 0.0, 1.0)]
    outcomes = []
    for direction, prob in action_probs(action):
        outcomes.append((apply_move(state, direction), -1.0, prob))
    return outcomes
```

`transitions(s, a)`devuelve una lista de `(s', r, p)`Este es todo el modelo.

> `transitions(s, a)` regresar `(s', r, p)`列表── ése es todo el modelo──

### Paso 2: Evaluación de las políticas

Dado que hay una política `π(s) = {action: prob}`, repite la ecuación de Bellman hasta que `V`Se detiene:

> 给定策略                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                         `π(s) = {action: prob}`, 代 Bellman 方程直到 `V`No se puede cambiar.

```python
def policy_evaluation(policy, gamma=0.99, tol=1e-6):
    V = {s: 0.0 for s in states()}
    while True:
        delta = 0.0
        for s in states():
            v = sum(pi_a * sum(p * (r + gamma * V[s_prime])
                              for s_prime, r, p in transitions(s, a))
                   for a, pi_a in policy(s).items())
            delta = max(delta, abs(v - V[s]))
            V[s] = v
        if delta < tol:
            return V
```

### Paso 3: Mejora de las políticas

Reemplazar`π`con la política codiciosa W.R.T.`V`Si ...`π`No cambió, regreso  estamos en el óptimo.

> ¿ Qué ?`π`替换为对 `V`贪心的策略──如果 `π`No cambió, regresamos. Hemos alcanzado el máximo.

```python
def policy_improvement(V, gamma=0.99):
    new_policy = {}
    for s in states():
        best_a = max(
            ACTIONS,
            key=lambda a: sum(p * (r + gamma * V[s_prime])
                              for s_prime, r, p in transitions(s, a)),
        )
        new_policy[s] = best_a
    return new_policy
```

### Paso 4: Conectadlos

```python
def policy_iteration(gamma=0.99):
    policy = {s: "up" for s in states()}   # arbitrary start
    for _ in range(100):
        V = policy_evaluation(lambda s: {policy[s]: 1.0}, gamma)
        new_policy = policy_improvement(V, gamma)
        if new_policy == policy:
            return V, policy
        policy = new_policy
```

Convergencia típica en 4×4: 46 iteraciones externas.`V*(0,0) ≈ -6`y una política que reduce estrictamente el número de pasos.

> 4×4 上的典型收:4-6 次外层代──输出 `V*(0,0) ≈ -6`Y una estrategia de reducción de pasos estrictamente.

### Paso 5: Iteración de valor (versión de un bucle)

```python
def value_iteration(gamma=0.99, tol=1e-6):
    V = {s: 0.0 for s in states()}
    while True:
        delta = 0.0
        for s in states():
            v = max(sum(p * (r + gamma * V[s_prime])
                       for s_prime, r, p in transitions(s, a))
                   for a in ACTIONS)
            delta = max(delta, abs(v - V[s]))
            V[s] = v
        if delta < tol:
            break
    policy = policy_improvement(V, gamma)
    return V, policy
```

El mismo punto fijo, menos líneas de código.

> Igual de inactividad, menor de código de la línea de números.

## Las trampas

- **Forgetting to handle terminals.**Si aplicas Bellman a un estado de absorción, sigue recogiendo una "mejor acción" que no cambia nada.`if s == terminal: V[s] = 0`¿ Qué ?
  **忘记处理终止状态。**Si se aplica el estado de absorción Bellman, todavía elegirá un "mejor movimiento" pero nada cambiará.`if s == terminal: V[s] = 0`保护。
- **Sup-norm vs L2 convergence.**Usar`max |V_new - V|`La garantía teórica está en la sup-norma.
  **Sup 范数 vs L2 收敛。**Uso `max |V_new - V|`, y no el valor medio.
- **In-place vs synchronous updates.**Actualización `V[s]`En el lugar (Gauss-Seidel) converge más rápido que en un lugar separado `V_new`El código de producción utiliza en el lugar.
  **原地更新 vs 同步更新。**Originalmente actualizada`V[s]`(Gauss-Seidel) Comparado con el aislado`V_new`字典(Jacobi)收更快──生产代码使用原地更新──
- **Policy ties.**Si dos acciones tienen el mismo valor Q,`argmax`El sistema de correlación puede romper los vínculos de manera diferente en cada iteración, causando que el control de "estabilidad de política" oscile.
  **策略平局。**Si dos movimientos de Q                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        `argmax`Cada vez puede romper la tabla de manera diferente, lo que conduce a la "strategia estabil" de la revisión de la balanza.
- **State-space explosion.**DP es`O(|S| · |A|)`Para el análisis de la función, el valor de la función se calcula en un punto de referencia.
  **状态空间爆炸。**DP cada vez que se hace la exploración es`O(|S| · |A|)`△ se aplica a aproximadamente 107 estados ∞.

## Usalo con el marco de ejecución

En 2026, DP es la línea de base de corrección y el bucle interno de los planificadores:

> En el año 2026, el DP es el ciclo interno de la línea y el planificador de base:

| Use case | Method |
|----------|--------|
| Use case / 用例 | Method / 方法 |
| Solve a small tabular MDP exactly / 精确求解小型表格 MDP | Value iteration (simpler) or policy iteration (fewer outer steps) / 值迭代（更简单）或策略迭代（更少外层步数） |
| Verify a Q-learning / PPO implementation / 验证 Q-learning/PPO 实现 | Compare to DP-optimal V* on a toy environment / 在玩具环境上与 DP 最优 V* 比较 |
| Model-based RL (Phase 9 · 10) / 基于模型的 RL | Bellman backup on a learned transition model / 在学习的转移模型上做 Bellman 备份 |
| Planning in AlphaZero / MuZero / AlphaZero/MuZero 中的规划 | Monte Carlo Tree Search = async Bellman backup / MCTS = 异步 Bellman 备份 |
| Offline RL (CQL, IQL) / 离线 RL | Conservative Q-iteration — DP with a penalty on OOD actions / 保守 Q 迭代——对 OOD 动作加惩罚的 DP |

Cada vez que alguien dice "la función de valor óptimo", se refiere a "el punto fijo DP".`V*`o `Q*`en un periódico, imagínate este bucle.

> Cada vez que alguien dice "la función de valor óptimo", se refiere a "DP no se mueve"― cuando ves en el artículo`V*`O `Q*`时, imagina este ciclo.

## Envíe el producto .

Salvo como`outputs/skill-dp-solver.md`¿Qué es esto ?

```markdown
---
name: dp-solver
description: Solve a small tabular MDP exactly via policy iteration or value iteration. Report convergence behavior.
version: 1.0.0
phase: 9
lesson: 2
tags: [rl, dynamic-programming, bellman]
---

Given an MDP with a known model, output:

1. Choice. Policy iteration vs value iteration. Reason tied to |S|, |A|, γ.
2. Initialization. V_0, starting policy. Convergence sensitivity.
3. Stopping. Sup-norm tolerance ε. Expected number of sweeps.
4. Verification. V*(s_0) computed exactly. Greedy policy extracted.
5. Use. How this baseline will be used to debug/evaluate sampling-based methods.

Refuse to run DP on state spaces > 10⁷. Refuse to claim convergence without a sup-norm check. Flag any γ ≥ 1 on an infinite-horizon task as a guarantee violation.
```

## Los ejercicios.

1. **Easy.**Ejecutar la iteración de valor en la 4×4 GridWorld con `γ ∈ {0.9, 0.99}`¿ Cuántas barradas hasta ?`max |ΔV| < 1e-6`¿ Impresión ?`V*`como una cuadrícula 4×4.
   > **练习1：**Usando diferentes factores de descuento, observa cómo cambia la velocidad de recepción.
2. **Medium.**Comparación de la iteración de la política vs iteración de valor en la *estocástica* GridWorld (probabilidad de deslizamiento `0.1`Contar: barridos, tiempo del reloj de la pared, final `V*(0,0)`¿Cuál converge más rápido en iteraciones?
   > **练习2：**Comparar estrategias 代和值 代在随机网格世界中的收速度 ((代次数和运行时间) 代的速度
3. **Hard.**Construir una iteración de política modificada: en la etapa de evaluación, ejecutar sólo `k`Se desliza en lugar de convergir.`V*(0,0)`error vs `k`por`k ∈ {1, 2, 5, 10, 50}`¿Qué le dice la curva sobre la compensación entre evaluación y mejora?
   > **练习3：**                                                                                                                                                                                                                                                              

## Términos clave .

| Term | What people say | What it actually means |
|------|-----------------|-----------------------|
| Policy iteration | "DP algorithm" / 策略迭代 | Alternating evaluation (`V^π`) and improvement (greedy `π` w.r.t. `V^π`) until the policy stops changing. |
| Value iteration | "Faster DP" / 值迭代 | Bellman optimality backup applied in one sweep; converges to `V*` geometrically. |
| Bellman operator | "The recursion" / Bellman 算子 | `(T V)(s) = max_a Σ P (r + γ V(s'))`; a `γ`-contraction in sup-norm. |
| Contraction | "Why DP converges" / 压缩映射 | Any operator `T` with `\|\|T x - T y\|\| ≤ γ \|\|x - y\|\|` has a unique fixed point. |
| GPI | "Everything is DP" / 广义策略迭代 | Generalized Policy Iteration: any method driving `V` and `π` to mutual consistency. |
| Synchronous update | "Jacobi-style" / 同步更新 | Use old `V` throughout a sweep; cleanly analyzable but slower. |
| In-place update | "Gauss-Seidel-style" / 原地更新 | Use `V` as it's being updated; converges faster in practice. |

## Más Leer más Leer más

- [Sutton & Barto (2018). Ch. 4 — Dynamic Programming](http://incompleteideas.net/book/RLbook2020.pdf) la presentación canónica de la iteración de políticas y la iteración de valores.
- [Bertsekas (2019). Reinforcement Learning and Optimal Control](http://www.athenasc.com/rlbook.html) tratamiento riguroso de los argumentos de cartografía de contracción.
- [Puterman (2005). Markov Decision Processes](https://onlinelibrary.wiley.com/doi/book/10.1002/9780470316887) la iteración de las políticas modificadas y su análisis de convergencia.
- [Howard (1960). Dynamic Programming and Markov Processes](https://mitpress.mit.edu/9780262582300/dynamic-programming-and-markov-processes/) el documento original de iteración de la política.
- [Bertsekas & Tsitsiklis (1996). Neuro-Dynamic Programming](http://www.athenasc.com/ndpbook.html) el puente desde el DP hasta el aproximado-DP / RL profundo utilizado en cada lección posterior.
