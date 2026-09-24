# MDPs, Estados, Acciones y Recompensas

> Un proceso de decisión de Markov es de cinco cosas: estados, acciones, transiciones, recompensas, un descuento. Todo en RL  Q-learning, PPO, DPO, GRPO  optimiza sobre esta forma. Aprenda una vez, lea el resto del aprendizaje de refuerzo de forma gratuita.

> **【中文解读】**El proceso de decisión de Marco Polo (MDP) contiene cinco elementos: estado, movimiento, transferencia, probabilidad de cambio, función de recompensa, factor de descuento, etc. Todo lo que contiene en el RL se optimiza en este marco.

> **【拓展：MDP 是 AI 对齐的基础】**El entrenamiento RLHF de ChatGPT es también un MDP en esencia: estado= diálogo sobre la siguiente página,动作=generación de tokens, premio= humanos preferencias, evaluación;.

**Type:** Learn | **类型:** 学习
**Languages:** Python | **语言:** Python
**Prerequisites:** Phase 1 · 06 (Probability & Distributions), Phase 2 · 01 (ML Taxonomy) | **前置知识:** Phase 1 · 06 (概率与分布), Phase 2 · 01 (ML 分类)
**Time:** ~45 minutes | **时间:** ~45 分钟

## El problema es la introducción del problema

Es un bot de ajedrez, un planificador de inventario, un agente de comercio, o un ciclo de PPO que entrena un modelo de razonamiento, cuatro dominios diferentes, un hecho sorprendente: los cuatro se desmoronan en el mismo objeto matemático.

> Estás escribiendo un ordenador de ajedrez o un agente de operaciones o un ciclo de PPO de un modelo de juego. En cuatro campos diferentes, un hecho sorprendente es que todos ellos se pueden resumir en el mismo objeto matemático.

El aprendizaje supervisado te da `(x, y)`¿El aprendizaje de refuerzo no le da etiquetas, sólo un flujo de estados, las acciones que tomó y una recompensa escalar? ¿Ganó el juego el movimiento? ¿La decisión de reabastecimiento ahorró dinero? ¿Ha hecho un beneficio el comercio? ¿El token que acaba de producir el LLM llevó a una recompensa mayor del juez?

> 监督学习给你  ¿ Qué es lo que haces ?`(x, y)`Sí, te ha preparado para una función. ¿El aprendizaje de la química no te da etiqueta? ¿Sólo el flujo de estado? ¿Las acciones que tomas y una recompensa de escala? ¿Ha ganado ese paso? ¿Ha gastado dinero en la decisión de suplemento? ¿Ha gastado dinero? ¿El token que acaba de generarse de LLM ha recibido una recompensa mayor de los jueces?

No puedes aprender de esta corriente hasta que no la formalizes. "Lo que vi", "lo que hice", "lo que pasó después", "qué tan bueno fue"  cada uno tiene que convertirse en un objeto sobre el que puedes razonar. Esa formalización es un Proceso de Decisión Markov. Cada algoritmo RL en esta fase, incluidos los bucles RLHF y GRPO al final, optimiza sobre esta forma.

> Usted no puede aprender de este flujo de datos hasta que lo forme. "Viste lo que""",He hecho lo que""",qué pasó después""",esto tiene que ser bueno" Cada uno de ellos debe ser un objeto razonable.

## El concepto central.

![Markov decision process: states, actions, transitions, rewards, discount](../assets/mdp.svg)

**The five objects.**- ¿ Qué ?**五个核心要素。**

- **States** `S`Todo lo que el agente necesita decidir en el GridWorld, la célula, en el ajedrez, la tabla, en un LLM, la ventana de contexto más cualquier memoria.
  **状态** `S` Todos los datos necesarios para la toma de decisiones en el sistema de inteligencia.
- **Actions** `A`Las opciones, subir/bajar/izquierda/derecha, jugar un movimiento, emitir un token.
  **动作** `A`△可选的操作──上/下/左/右移动──下一步棋──生成一个代币──
- **Transitions** `P(s' | s, a)`- Dado el estado .`s`y la acción `a`Determinista en ajedrez, estocástico en inventario, casi determinista en decodificación LLM.
  **转移概率** `P(s' | s, a)` Estado determinado`s`Y movimiento`a`, Distribución del siguiente estado, en el mundo del juego de chess, la certeza, en el manejo de inventarios, la certeza, en el sistema de gestión de inventarios, la certeza, en el sistema de gestión de inventarios, la certeza, en el sistema de gestión de inventarios, en el sistema de gestión de inventarios, en el sistema de gestión de inventarios, en el sistema de gestión de inventarios, en el sistema de gestión de inventarios, en el sistema de gestión de inventarios, en el sistema de gestión de inventarios, en el sistema de gestión de inventarios, en el sistema de inventarios, en el sistema de inventarios, en el sistema de inventarios, en el sistema de inventarios, en el sistema de inventarios, en el sistema de inventarios, en el sistema de inventarios, en el sistema de inventarios, en el sistema de inventarios, en el sistema de inventarios, en el sistema de inventarios, en el sistema de inventarios, en el sistema de inventarios, en el sistema de inventarios, en el sistema de inventarios, en el sistema de inventarios, en el sistema de inventarios, en el sistema de datos, en el cual se puede ver más.
- **Rewards** `R(s, a, s')`La señal escalar. ganancia = +1, pérdida = -1. ingresos menos costo. El término de la relación log-probabilidad en GRPO.
  **奖励** `R(s, a, s')`                                                                                                                                                                                                                                                              
- **Discount** `γ ∈ [0, 1)`¿Cuánto cuentan las recompensas futuras frente al presente?`γ = 0.99`compra un horizonte de ~ 100 pasos; `γ = 0.9`Comprará ~10.
  **折扣因子** `γ ∈ [0, 1)`■ Las recompensas futuras en relación con el peso de las recompensas actuales■`γ = 0.99`Para la visión efectiva de aproximadamente 100 pasos;`γ = 0.9`Para la respuesta de aproximadamente 10 pasos.

**The Markov property** `P(s_{t+1} | s_t, a_t) = P(s_{t+1} | s_0, a_0, …, s_t, a_t)`El futuro depende sólo del estado presente. Si no lo hace, la representación del estado es incompleta.

> **马尔可夫性质**El futuro sólo depende del estado actual. Si no existe, el estado significa que no está completo.

**Policies and returns.**Una política`π(a | s)`Los estados de mapas a las distribuciones de acción.`G_t = r_t + γ r_{t+1} + γ² r_{t+2} + …`Es la suma descuentada de las recompensas futuras.`V^π(s) = E[G_t | s_t = s]`es el rendimiento esperado a partir de `s`en el marco de la política `π`El valor Q`Q^π(s, a) = E[G_t | s_t = s, a_t = a]`El algoritmo RL estima uno de estos dos, y luego mejora `π`En consecuencia.

> **策略与回报。** estrategia `π(a|s)`将状态映射到动作分布──回报 `G_t`Es un descuento y un valor de la recompensa futura.`V^π(s)`Es de estado.`s`                                                                                                                                                                                                                                                              `Q^π(s,a)`Es decir, cada algoritmo de RL es uno de los dos valores que se evalúan y luego se mejora la estrategia.

**The Bellman equations.**Las ecuaciones de punto fijo que todo en esta fase utiliza:

`V^π(s) = Σ_a π(a|s) Σ_{s', r} P(s', r | s, a) [r + γ V^π(s')]`

> **【中文解读】**La ecuación Bellman es la relación de transmisión central de RL: el valor del estado actual = recompensa inmediata + valor del estado siguiente de descuento posterior. Es la base común del planeamiento de la actividad, el aprendizaje Q, el aprendizaje TD. En el entrenamiento RLHF de la LLM, esto se corresponde a "contribución de los tokens actuales = porcentaje de preferencias de la gente + contribución esperada de los tokens futuros".

> **【拓展：从 MDP 到 POMDP】**现实中很多问题不满足马尔可夫性 (la situación actual no puede determinar completamente el futuro), necesita usar POMDP (MDP) 建模.
`Q^π(s, a) = Σ_{s', r} P(s', r | s, a) [r + γ Σ_{a'} π(a'|s') Q^π(s', a')]`

Estos divididos esperados regresan a "la recompensa de este paso" más "valor descuento de donde aterrizas". Recursivo. Cada algoritmo en la Fase 9 o bien repite esta ecuación a convergencia (programación dinámica), muestras de ella (Monte Carlo), o arranca un paso (diferencia temporal).

> Estos métodos se espera que el retorno se descompone en "recompensación de los pasos actuales" + "valor de descuento de alcanzar el estado"―.

## Construye y realiza.
```figure
discount-horizon
```

## Construye el mismo

### Paso 1: un pequeño MDP determinista

Un 4x4 GridWorld. El agente comienza en la parte superior izquierda, la terminal en la parte inferior derecha, recompensa de -1 por paso, acciones.`{up, down, left, right}`- ¿ Qué ?`code/main.py`¿ Qué ?

> Un 4×4 de la red de mundo. El cuerpo inteligente de la esquina superior izquierda, el estado final en la esquina inferior derecha, cada paso recompensa -1, se activa como `{上, 下, 左, 右}`¿Qué es eso?

```python
GRID = 4
TERMINAL = (3, 3)
ACTIONS = {"up": (-1, 0), "down": (1, 0), "left": (0, -1), "right": (0, 1)}

def step(state, action):
    if state == TERMINAL:
        return state, 0.0, True
    dr, dc = ACTIONS[action]
    r, c = state
    nr = min(max(r + dr, 0), GRID - 1)
    nc = min(max(c + dc, 0), GRID - 1)
    return (nr, nc), -1.0, (nr, nc) == TERMINAL
```

Cinco líneas, todo el entorno, transiciones deterministas, penas de paso constantes, estado terminal de absorción.

> 五行代码── ése es todo el ambiente── determinación de la transferencia、恒定步惩罚、 absorción de la terminación del estado──

### Paso 2: elaborar una política

Una política es una función de la distribución del estado a la acción.

> 策略是从状态到动作分布的函数──最简单的:均随机── es la función de distribución de la estrategia desde estado hasta movimiento.

```python
def uniform_policy(state):
    return {a: 0.25 for a in ACTIONS}

def rollout(policy, max_steps=200):
    s, total, steps = (0, 0), 0.0, 0
    for _ in range(max_steps):
        a = sample(policy(s))
        s, r, done = step(s, a)
        total += r
        steps += 1
        if done:
            break
    return total, steps
```

ejecuta la política aleatoria 1000 veces. el retorno promedio es de alrededor de -60 a -80 para esta tabla 4×4. el retorno óptimo es -6 (camino de línea recta hacia abajo a la derecha). cerrar esa brecha es todo en la Fase 9.

> 运行随机策略 1000 次── este 4×4 棋盘 平均回报约为 -60到 -80──最优回报是 -6(直线路径向右下方)──缩小这个差距就是9期的全部目标──

### Paso 3: computación `V^π`exactamente a través de la ecuación de Bellman

Para MDPs pequeños la ecuación de Bellman es un sistema lineal. Enumera estados, aplica la expectativa, itera hasta que los valores dejan de cambiar.

> Para el MDP pequeño, la ecuación Bellman es un sistema lineal.

```python
def policy_evaluation(policy, gamma=0.99, tol=1e-6):
    V = {s: 0.0 for s in all_states()}
    while True:
        delta = 0.0
        for s in all_states():
            if s == TERMINAL:
                continue
            v = 0.0
            for a, pi_a in policy(s).items():
                s_next, r, _ = step(s, a)
                v += pi_a * (r + gamma * V[s_next])
            delta = max(delta, abs(v - V[s]))
            V[s] = v
        if delta < tol:
            return V
```

Este es el primer algoritmo en Sutton & Barto y la base teórica de cada método RL que sigue.

> Es el primer algoritmo en el libro de Sutton & Barto, y es la base teórica de todos los métodos de RL posteriores.

### Paso 4:`γ`es un hiperparámetro con significado físico

El horizonte efectivo es aproximadamente `1 / (1 - γ)`- ¿ Qué ?`γ = 0.9`→ 10 pasos. `γ = 0.99`→ 100 pasos. `γ = 0.999`→ 1000 pasos.

> Tiene efectos visuales.`1 / (1 - γ)`¿Qué es eso?`γ = 0.9`Por lo que se trata de 10 pasos.`γ = 0.99`Por lo que se trata de 100 pasos.`γ = 0.999`Por lo que 1000 pasos.

El agente actúa de manera miope y la asignación de créditos se vuelve ruidosa, ya que muchos pasos iniciales comparten la responsabilidad de la recompensa de un futuro lejano.`γ = 1`Los controles de las tareas de control utilizan`0.95–0.99`Los juegos de estrategia de largo horizonte usan`0.999`¿ Qué ?

> 折扣因子太低,智能体会目光短浅──太高,信用分配会变杂,因为 muchos pasos tempranos juntos asumen la responsabilidad de las recompensas a largo plazo──LLM RLHF usualmente se utiliza `γ = 1`, , porque el tiempo es corto y tiene límites.`0.95-0.99`△长视野策略 juego `0.999`¿Qué es eso?

## Las trampas

- **Non-Markovian state.**Si necesita las últimas tres observaciones para decidir, el "estado" no es solo la observación actual.
  **非马尔可夫状态。**Si necesitas las últimas tres observaciones para tomar una decisión, "estado" no es sólo la actual observación.
- **Sparse rewards.**Las recompensas sólo para ganar hacen que el aprendizaje sea casi imposible en grandes espacios de estado.
  **稀疏奖励。**                                                                                                                                                                                                                                                              
- **Reward hacking.**Optimizar una recompensa por proxy a menudo produce comportamiento patológico. El agente de carreras de barcos de OpenAI gira en círculos recogiendo powerups para siempre en lugar de terminar la carrera. Siempre define la recompensa por el resultado objetivo, no por el proxy.
  **奖励黑客。**优化代理奖励常产生病态行为――OpenAI's赛船代理原地转圈收集道具,永远不完成比赛――始终从目标结果定义奖励,而不是代理――
- **Discount mis-spec.** `γ = 1`En una tarea de horizonte infinito hace que cada valor sea infinito.`γ < 1`¿ Qué ?
  **折扣因子设定错误。**无限视野任务上                                              `γ = 1`¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡`γ < 1`¡Vamos a la reunión!
- **Reward scale.**Las recompensas de {+100, -100} vs {+1, -1} dan políticas óptimas idénticas pero magnitudes de gradiente muy diferentes.`[-1, 1]`- antes de conectarse a PPO/DQN.
  **奖励尺度。**Los premios de {+100, -100} y {+1, -1} dan la misma estrategia óptima, pero la gradiencia de la escala es enorme.`[-1, 1]`¿Qué es esto?

## Usalo con el marco de ejecución

La pila 2026 reduce cada tubería RL a un MDP antes de tocar el código:

> Antes de escribir el código, se reducirá cada RL 流水线 a un MDP:

| Situation | State | Action | Reward | γ |
|-----------|-------|--------|--------|---|
| Situation / 场景 | State / 状态 | Action / 动作 | Reward / 奖励 | γ |
| Control (locomotion, manipulation) / 控制（运动、操作） | Joint angles + velocities / 关节角度+速度 | Continuous torques / 连续力矩 | Task-specific shaped / 任务特定塑形 | 0.99 |
| Games (chess, Go, poker) / 游戏（象棋、围棋、扑克） | Board + history / 棋盘+历史 | Legal move / 合法走法 | Win=+1 / loss=-1 / 胜=+1/负=-1 | 1.0 (finite) |
| Inventory / pricing / 库存/定价 | Stock + demand / 库存+需求 | Order qty / 订购量 | Revenue - cost / 收入-成本 | 0.95 |
| RLHF for LLMs / LLM 的 RLHF | Context tokens / 上下文 token | Next token / 下一个 token | Reward-model score at end / 末尾奖励模型分数 | 1.0 (episode ~200 tokens) |
| GRPO for reasoning / 推理的 GRPO | Prompt + partial response / 提示+部分回复 | Next token / 下一个 token | Verifier 0/1 at end / 末尾验证器 0/1 | 1.0 |

Escriba los cinco tuples antes de escribir cualquier bucle de entrenamiento. La mayoría de los informes de errores "RL no funciona" se remontan a una formulación MDP que se rompió en papel.

> Antes de escribir cualquier ciclo de entrenamiento, debe escribirse un buen grupo de cinco. La mayoría de los informes de errores de "RL no funciona" se remontan a la definición de MDP en papel.

## Envíe el producto .

Salvo como`outputs/skill-mdp-modeler.md`¿Qué es esto ?

```markdown
---
name: mdp-modeler
description: Given a task description, produce a Markov Decision Process spec and flag formulation risks before training.
version: 1.0.0
phase: 9
lesson: 1
tags: [rl, mdp, modeling]
---

Given a task (control / game / recommendation / LLM fine-tuning), output:

1. State. Exact feature vector or tensor spec. Justify Markov property.
2. Action. Discrete set or continuous range. Dimensionality.
3. Transition. Deterministic, stochastic-with-known-model, or sample-only.
4. Reward. Function and source. Sparse vs shaped. Terminal vs per-step.
5. Discount. Value and horizon justification.

Refuse to ship any MDP where the state is non-Markovian without explicit mention of frame-stacking or recurrent state. Refuse any reward that was not defined in terms of the target outcome. Flag any `γ ≥ 1.0` on an infinite-horizon task. Flag any reward range >100x the typical step reward as a likely gradient-explosion source.
```

## Los ejercicios.

1. **Easy.**Implementar el 4×4 GridWorld y el despliegue de políticas aleatorias en `code/main.py`- Cancelar 10.000 episodios. Informar el promedio y el std de retorno. Comparar con el retorno óptimo (-6).
   > **练习1（简单）：**实现 4×4 GridWorld 和随机策略推广──运行 10,000 回合──报告回报的平均值和标准差,与最优回报 (-6) 比较──
2. **Medium.**- ¿ Qué ?`policy_evaluation`con`γ ∈ {0.5, 0.9, 0.99}`para la política uniforme aleatoria.`V`Explique por qué los valores de estado cerca de la terminal crecen más rápido con mayor tamaño.`γ`¿ Qué ?
   > **练习2（中等）：**¿ Qué ?`γ ∈ {0.5, 0.9, 0.99}`运行策略评估──印每 γ 的 4×4 值网格──解释为什么接近终止状态的状态值在更大的 γ 下增长更快──
3. **Hard.**Vuelve la GridWorld estocástica: cada acción se desliza hacia una dirección adyacente con probabilidad `p = 0.1`Reevaluar la política de uniforme.`V[start]`¿Mejor o peor?
   > **练习3（困难）：**Cambiar el mundo de la red a lo que sea: cada movimiento en probabilidad`p = 0.1`滑向相邻方向── reevaluación de la estrategia de la misma.`V[start]`¿Bastará bien o mal?

## Términos clave .

| Term | What people say | What it actually means |
|------|-----------------|-----------------------|
| Term / 术语 | What people say / 通俗说法 | What it actually means / 实际含义 |
| MDP | "Reinforcement learning setup" | Tuple `(S, A, P, R, γ)` satisfying the Markov property. |
| State / 状态 | "What the agent sees" / "智能体看到什么" | Sufficient statistic for future dynamics under the chosen policy class. |
| Policy / 策略 | "Agent's behavior" / "智能体的行为" | Conditional distribution `π(a \| s)` or deterministic map `s → a`. |
| Return / 回报 | "Total reward" / "总奖励" | Discounted sum `Σ γ^t r_t` from the current step. |
| Value / 值函数 | "How good a state is" / "状态有多好" | Expected return under `π` starting from `s`. |
| Q-value / Q值 | "How good an action is" / "动作有多好" | Expected return under `π` starting from `s` with first action `a`. |
| Bellman equation / Bellman方程 | "Dynamic programming recursion" / "动态规划递推" | Fixed-point decomposition of value / Q into one-step reward plus discounted successor value. |
| Discount `γ` / 折扣因子 | "Future vs present" / "未来vs当前" | Geometric weight on far-future reward; effective horizon `~1/(1-γ)`. |

## Más Leer más Leer más

- [Sutton & Barto (2018). Reinforcement Learning: An Introduction, 2nd ed.](http://incompleteideas.net/book/RLbook2020.pdf)El capítulo 3 cubre las ecuaciones de MDP y Bellman; el capítulo 1 motiva la hipótesis de recompensa que subyace en cada lección posterior.
- [Bellman (1957). Dynamic Programming](https://press.princeton.edu/books/paperback/9780691146683/dynamic-programming) el origen de la ecuación de Bellman.
- [OpenAI Spinning Up — Part 1: Key Concepts](https://spinningup.openai.com/en/latest/spinningup/rl_intro.html) Primer conciso de MDP desde un ángulo de RL profundo.
- [Puterman (2005). Markov Decision Processes](https://onlinelibrary.wiley.com/doi/book/10.1002/9780470316887) la referencia de investigación de operaciones sobre los PMP y los métodos de solución exactos.
- [Littman (1996). Algorithms for Sequential Decision Making (PhD thesis)](https://www.cs.rutgers.edu/~mlittman/papers/thesis-main.pdf) la derivación más limpia de los MDP como especialización de programación dinámica.
