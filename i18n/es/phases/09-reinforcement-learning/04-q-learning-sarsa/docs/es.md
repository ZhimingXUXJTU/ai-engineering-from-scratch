# Diferencia temporal  Q-Learning y SARSA  时序差分  Q学习 y SARSA

> Monte Carlo espera hasta que termine el episodio. TD actualiza después de cada paso al iniciar la siguiente estimación de valor. Q-learning es fuera de política y optimista; SARSA es en política y cauteloso. Ambos son una línea de código. Ambos sustentan cada método de RL profundo en esta fase.

> **【中文解读】**MC tiene que esperar hasta que el ciclo termine para actualizarse, TD((`r + γ V(s')`作为目标来引导当前估计;;Q-learning is离策略的(学习最佳策略),SARSA es en línea策略的(学习当前行为策略);; dos de ellos son sólo diferentes`max`Pero es la base de toda la profundidad de la RL.

**Type:** Build | **类型:** 动手
**Languages:** Python | **语言:** Python
**Prerequisites:** Phase 9 · 01 (MDPs), Phase 9 · 02 (Dynamic Programming), Phase 9 · 03 (Monte Carlo) | **前置知识:** Phase 9 · 01 (MDP), Phase 9 · 02 (动态规划), Phase 9 · 03 (蒙特卡洛)
**Time:** ~75 minutes | **时间:** ~75 分钟

## El problema es la introducción del problema

Monte Carlo funciona pero tiene dos demandas caras. Necesita episodios que terminen, y sólo se actualiza después de que el regreso final está en. Si tu episodio es de 1.000 pasos, MC espera 1.000 pasos para actualizar cualquier cosa. Es de alta variación, baja prejuicio, y lento en la práctica.

> El Monte Carlo es válido pero tiene dos requisitos caros. Requiere que el ciclo termine, y sólo se actualice después de que el regreso final sale. Si el ciclo tiene 1.000 pasos, MC debe esperar 1.000 pasos para actualizar cualquier cosa.

La programación dinámica tiene el perfil opuesto  copias de seguridad de boot de varianza cero  pero requiere un modelo conocido.

> 动态规划有相反的特点零方差的自举备份但需要已知模型

El aprendizaje de la diferencia temporal (TD) divide la diferencia.`(s, a, r, s')`, formar un objetivo de un paso .`r + γ V(s')`y empujar .`V(s)`No hay modelo, no hay episodios completos, ni sesgo de usar una aproximación.`V`en el RHS, pero con una variación dramáticamente menor que MC y actualizaciones en línea desde el primer paso.

> 时序差分(TD) aprendizaje de los dos.`(s, a, r, s')` Construir un solo objetivo `r + γ V(s')`,将 `V(s)`A su lado, no se necesita un modelo.`V`Hay diferencias, pero las diferencias son mucho más bajas que las MC, y desde el primer paso se puede actualizar en línea.

Este es el pivote en el que se giran todas las modernas RL  DQN, A2C, PPO, SAC . El resto de la Fase 9 son capas de aproximación de funciones y trucos construidos sobre la actualización TD de un paso que escribirás en esta lección.

> Es el núcleo de todos los RLDQN¬A2C¬PPO¬SAC¬¬. El resto de la fase 9 se encuentra en el nivel de aproximación y técnicas de las funciones construidas sobre las únicas etapas de la actualización de la TD que escribirás en este curso.

> **【中文解读】**TD aprendiz es DP y MC: con un solo paso de transferencia`(s,a,r,s')`                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             `r + γV(s')`, no necesita modelo, ni requiere un ciclo completo. Hay un parámetro (porque se utiliza un parámetro similar a V), pero el parámetro es mucho menor que el MC, y puede actualizarse en línea.

> **【拓展：游戏AI→LLM对齐】**El aprendizaje Q es el núcleo de Atari DQN de 2013, que abrió la fase de RL en profundidad.

## El concepto central.

![Q-learning vs SARSA: off-policy max vs on-policy Q(s', a')](../assets/td.svg)

**The TD(0) update for V:**

`V(s) ← V(s) + α [r + γ V(s') - V(s)]`

La cantidad entre paréntesis es el error TD `δ = r + γ V(s') - V(s)`Es el análogo en línea de `G_t - V(s_t)`en MC. La convergencia requiere`α`satisfacer a Robbins-Monro (`Σ α = ∞`¿ Qué ?`Σ α² < ∞`) y todos los estados visitados con infinita frecuencia.

> **V 的 TD(0) 更新：**括号中的量是 TD 误差 `δ = r + γ V(s') - V(s)`Es el MC.`G_t - V(s_t)`La respuesta es que la respuesta es una respuesta.`α`满足 Robbins-Monro 条件且所有状态被无限次访问──

**Q-learning.**Un método de control TD fuera de la política:

`Q(s, a) ← Q(s, a) + α [r + γ max_{a'} Q(s', a') - Q(s, a)]`

El `max`La política de la "compromisora" se seguirá desde`s'`El desacoplamiento hace que el aprendizaje Q aprenda.`Q*`Mnih et al. (2015) convirtió esto en aprendizaje profundo de Q en Atari (Ley 05).

> **Q-learning。**Un método de control de la TD.`max`假设从                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                          `s'`开始将遵循*贪心*策略, independientemente de lo que el cuerpo inteligente practique.  Este método permite que el aprendizaje Q se desarrolle a través de la exploración de la inteligencia.`Q*`Mnih 等人 (2015) se convertirá en Atari 上的深度 Q-learning (Leyón 05) 

**SARSA.**Un método de TD en política:

`Q(s, a) ← Q(s, a) + α [r + γ Q(s', a') - Q(s, a)]`

El nombre es el tuple`(s, a, r, s', a')`. SARSA utiliza la acción `a'`El agente toma el siguiente, no el codicioso.`argmax`- Converge a`Q^π`Por lo que sea que sea avaro.`π`está funcionando, que en el límite `ε → 0`Se convierte en`Q*`¿ Qué ?

> **SARSA。**Un tipo de estrategia en línea TD 方法──名称是元组 `(s, a, r, s', a')`◊ SARSA 使用智能体*实际*采取的下一个动作 `a'`, y no de la avaricia .`argmax`◊ Recibir hasta ahora ε-贪心 `π`de la `Q^π`, en el`ε → 0`De la máxima baja de cambio`Q*`¿Qué es eso?

**The cliff-walking difference.**En la tarea clásica de caminar por acantilados (caída-descance-acantilado = recompensa -100), el aprendizaje Q aprende el camino óptimo a lo largo del borde del acantilado, pero ocasionalmente toma la penalidad durante la exploración. SARSA aprende un camino más seguro a un paso del acantilado porque tiene en cuenta el ruido de exploración en su valor Q.`ε → 0`En la práctica importa: cuando la exploración se realiza en realidad en el despliegue, el comportamiento de SARSA es más conservador.

> **【中文解读】**Clásico experimento de caminata en la colina revela la diferencia clave entre Q-learning y SARSA: Q-learning aprender a seguir el mejor camino de la colina, pero explorar cuando cae), SARSA aprender a seguir el camino de seguridad lejos de la colina, ya que considera el ruido explorado.

**Expected SARSA.**Reemplazar`Q(s', a')`con su valor esperado inferior a `π`¿Qué es esto ?

`Q(s, a) ← Q(s, a) + α [r + γ Σ_{a'} π(a'|s') Q(s', a') - Q(s, a)]`

Varianza menor que la SARSA (no hay muestra de `a'`), el mismo objetivo en materia de política.

> **期望 SARSA。**¿ Qué ?`π` 下的期望值替换 `Q(s', a')`◊ Más bajo que SARSA 方差更低`a'`), el mismo en línea estrategia objetivo.

**n-step TD and TD(λ).**Interpolar entre TD(0) y MC esperando `n`pasos antes de arrancar. `n=1`es TD, `n=∞`es MC. TD(λ) promedios sobre todos `n`con pesos geométricos `(1-λ)λ^{n-1}`La mayoría de los usos de RL profundos`n`entre 3 y 20.

> **n 步 TD 和 TD(λ)。**En TD(0) y MC  entre el valor de entrada, espera `n`步再自举──`n=1`Sí, TD,`n=∞`Es el MC.TD.`n`取平均──大多数深度 RL 使用 `n`Entre 3 y 20 años.

> **【拓展：TD 误差在 LLM RLHF 中的对应】**TD 误差 δ = r + γV(s') - V(s) en el entrenamiento RLHF de LLM                                                                                                                                                                                                                                                 

## Construye y realiza.
```figure
qlearning-gridworld
```

## Construye el mismo

### Paso 1: SARSA sobre la política de avaricia

```python
def sarsa(env, episodes, alpha=0.1, gamma=0.99, epsilon=0.1):
    Q = defaultdict(lambda: {a: 0.0 for a in ACTIONS})

    def choose(s):
        if random() < epsilon:
            return choice(ACTIONS)
        return max(Q[s], key=Q[s].get)

    for _ in range(episodes):
        s = env.reset()
        a = choose(s)
        while True:
            s_next, r, done = env.step(s, a)
            a_next = choose(s_next) if not done else None
            target = r + (gamma * Q[s_next][a_next] if not done else 0.0)
            Q[s][a] += alpha * (target - Q[s][a])
            if done:
                break
            s, a = s_next, a_next
    return Q
```

La única diferencia con el aprendizaje Q es la línea de objetivo.

> La única diferencia entre el aprendizaje de Q y el objetivo de Q.

### Paso 2: Aprendizaje de Q

```python
def q_learning(env, episodes, alpha=0.1, gamma=0.99, epsilon=0.1):
    Q = defaultdict(lambda: {a: 0.0 for a in ACTIONS})
    for _ in range(episodes):
        s = env.reset()
        while True:
            a = choose(s, Q, epsilon)
            s_next, r, done = env.step(s, a)
            target = r + (gamma * max(Q[s_next].values()) if not done else 0.0)
            Q[s][a] += alpha * (target - Q[s][a])
            if done:
                break
            s = s_next
    return Q
```

El `max`El símbolo es la diferencia entre la política y la política.

> `max`La definición de objetivos y comportamientos es la diferencia entre estrategias en línea y estrategias fuera de línea.

### Paso 3: Curvas de aprendizaje

El estudio de la C.A.R.S.A. se ha desarrollado en el campo de la C.A.R.S.A. en el campo de la C.A.R.S.A.R.S.A. en el campo de la C.A.R.S.A.R.S.A. en el campo de la C.A.R.S.A.R.S.A. en el campo de la C.A.R.S.A.R.S.A.R.S.A. en el campo de la C.A.R.S.A.R.S.A. en el campo de la C.A.R.S.A.R.S.A. en el campo de la C.A.R.S.A.R.S.A. en el campo de la C.A.R.S.A.R.S.A.R.S.A. en el campo de la C.A.R.S.R.S.A.R.S.R.S.A.R.R.S.R.S.R.R.S.R.R.R.R.S.R.R.R.R.R.R.R.R.R.R.R.R.R.R.R.R.R.R.R.R.R.R.R.R.R.R.R.R.R.R.R.R.R.R.R.R.R.R.R.R.R.R.R.R.R.R.R.R.R.R.R.R.R.R.R.R.R.R.R.R.R.R.R.R.R.R.R.R.R.R.R.R.R.R.R.R.R.R.R.R.R.R.R.R.R.R.R.R.R.R.R.R.R.R.R.R.R.R.R.R.R.R.R.R.R.R.R.R.R.R.R.R.R.R.R.R.R.R.R.R.R`code/main.py`, ambos son casi óptimos después de ~ 2.000 episodios con `α=0.1, ε=0.1`¿ Qué ?

> Seguir cada 100 veces el recorrido promedio. Q-learning en la simple determinación GridWorld 上收快; SARSA en la escalera de la ruta más conservada.`code/main.py`El 4×4 GridWorld arriba, dos en `α=0.1, ε=0.1`Cerca de 2.000 veces más cerca de lo mejor.

### Paso 4: comparación con la verdad de DP

Ejecutar la iteración del valor (lección 02) para obtener `Q*`- ¿ Qué ?`max_{s,a} |Q_learned(s,a) - Q*(s,a)|`Un agente TD saludable tabulear aterriza dentro de la`~0.5`en el 4×4 GridWorld después de 10.000 episodios.

> 运行值代(Leyón 02) obtener `Q*` Inspección`max_{s,a} |Q_learned(s,a) - Q*(s,a)|`◊ Una buena imagen TD  inteligentes en 10.000 veces después en 4×4 GridWorld `~0.5`En el interior.

## Las trampas

- **Initial Q values matter.**Inicialmente optimista (`Q = 0`El principio pesimista puede atrapar una política codiciosa para siempre.
  **初始 Q 值很重要。**乐观初始化 负奖励任务中                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                  `Q = 0`En el caso de los países de la Unión Europea, el desarrollo de la economía de la Unión Europea es un factor importante.
- **α schedule.**Constantemente .`α`Es bueno para problemas no estacionarios.`α_n = 1/n`da convergencia en teoría pero es demasiado lento en la práctica  pin `α`En el`[0.05, 0.3]`y monitorear la curva de aprendizaje.
  **α 调度。**                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             `α`                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             `α_n = 1/n`                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             `α` Fija en `[0.05, 0.3]`Y controlar el aprendizaje de la línea.
- **ε schedule.**Comienza con alto (`ε=1.0`), la descomposición a `ε=0.05`. "GLIE" (compulsivo en el límite con una exploración infinita) es la condición de convergencia.
  **ε 调度。**Desde el alto de la cantidad de dinero`ε=1.0`), disminución hasta `ε=0.05`La "GLIE" (极极贪心且无限探索) es una condición.
- **Max bias in Q-learning.**El `max`el operador está sesgado hacia arriba cuando `Q`El doble aprendizaje Q de Hasselt (utilizado por DDQN en la Lección 05) corrige esto con dos tablas de Q.
  **Q-learning 的最大化偏差。** `max`算子在                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                          `Q`Hay ruido cuando se hace un alto y se hace un alto y se hace un alto y se hace un alto y se hace un alto y se hace un alto y se hace un alto y se hace un alto y se hace un alto y se hace un alto y se hace un alto y se hace un alto y se hace un alto y se hace un alto y se hace un alto y se hace un alto y se hace un alto y se hace un alto y se hace un alto y se hace un alto y se hace un alto y se hace un alto y se hace un alto y se hace un alto y se hace un alto y se hace un alto y se hace un alto y se hace un alto y se hace un alto.
- **Non-terminating episodes.**TD puede aprender sin terminales, pero debe captar los pasos o manejar correctamente la banda de arranque en la banda.
  **非终止回合。**TD puede aprender en un estado sin fin, pero necesita establecer un número de pasos por encima del límite o correctamente tratar el límite de la actividad.
- **State hashing.**Si los estados son tuples/tensores, utilice una clave hashable (tuplo, no lista; tuple de flotantes redondeados, no crudo).
  **状态哈希。**Si el estado es un grupo de unidades/cuantidad de unidades, utiliza la clave de la base de datos de un grupo de unidades (con la base de datos de un grupo de unidades) y no la base de datos de un grupo de unidades.

## Usalo con el marco de ejecución

El panorama de la TD para 2026:

> Edición de la edición de la edición de 2026 del año TD:

| Task | Method | Reason |
|------|--------|--------|
| Task / 任务 | Method / 方法 | Reason / 原因 |
| Small tabular environments / 小型表格环境 | Q-learning | Learns optimal policy directly. / 直接学习最优策略。 |
| On-policy safety-critical / 在线策略安全关键 | SARSA / Expected SARSA | Conservative during exploration. / 探索期间保守。 |
| High-dimensional state / 高维状态 | DQN (Phase 9 · 05) | Neural-net Q-function with replay and target net. / 神经网络 Q 函数+回放+目标网络。 |
| Continuous actions / 连续动作 | SAC / TD3 (Phase 9 · 07) | TD update on a Q-network; policy net emits actions. / Q 网络上的 TD 更新；策略网络输出动作。 |
| LLM RL (reward-model-based) / LLM RL（基于奖励模型） | PPO / GRPO (Phase 9 · 08, 12) | Actor-critic with TD-style advantage via GAE. / Actor-Critic + GAE 的 TD 式优势。 |
| Offline RL / 离线 RL | CQL / IQL (Phase 9 · 08) | Q-learning with conservative regularization. / 带保守正则化的 Q-learning。 |

El 90% de la "RL" que se lee en los artículos 2026 es una elaboración de Q-learning o SARSA.

> En el artículo 2026 años, el "RL" que has leído, el 90% es una variante de Q-learning o SARSA. Antes de leer en profundidad, primero actualice el perfil para que aprenda la memoria muscular.

## Envíe el producto .

Salvo como`outputs/skill-td-agent.md`¿Qué es esto ?

```markdown
---
name: td-agent
description: Pick between Q-learning, SARSA, Expected SARSA for a tabular or small-feature RL task.
version: 1.0.0
phase: 9
lesson: 4
tags: [rl, td-learning, q-learning, sarsa]
---

Given a tabular or small-feature environment, output:

1. Algorithm. Q-learning / SARSA / Expected SARSA / n-step variant. One-sentence reason tied to on-policy vs off-policy and variance.
2. Hyperparameters. α, γ, ε, decay schedule.
3. Initialization. Q_0 value (optimistic vs zero) and justification.
4. Convergence diagnostic. Target learning curve, `|Q - Q*|` check if DP is possible.
5. Deployment caveat. How will exploration behave at inference? Is SARSA's conservatism needed?

Refuse to apply tabular TD to state spaces > 10⁶. Refuse to ship a Q-learning agent without a max-bias caveat. Flag any agent trained with ε held at 1.0 throughout (no exploitation phase).
```

## Los ejercicios.

1. **Easy.**Implemente Q-learning y SARSA en el GridWorld 4×4. Plot de curvas de aprendizaje (retorno medio por 100 episodios) para 2.000 episodios. ¿Quién converge más rápido?
   > **练习1：**En GridWorld, la línea de aprendizaje de Q-learning y SARSA se compara con la de RRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRR
2. **Medium.**Construir un entorno de caminar en acantilados (4×12, la última fila es el acantilado con recompensa -100 y restablecer para comenzar). Comparar las políticas finales de Q-learning y SARSA.
   > **练习2：** realzar el clima, observar las diferencias de estrategia de Q-learning                                                                                                                                                                                                                                                      
3. **Hard.**Implementar doble aprendizaje Q. En un GridWorld de recompensas ruidosas (ruido gaussiano σ=5 añadido a la recompensa por paso), muestra sobrevaloraciones de Q-learning `V*(0,0)`En el caso de los estudiantes de doble Q, el aprendizaje no es un aprendizaje de doble Q.
   > **练习3：**¢¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿

## Términos clave .

| Term | What people say | What it actually means |
|------|-----------------|-----------------------|
| TD error | "The update signal" / TD 误差 | `δ = r + γ V(s') - V(s)`, the bootstrapped residual. |
| TD(0) | "One-step TD" / 单步 TD | Update after every transition using only the next state's estimate. |
| Q-learning | "Off-policy RL 101" / Q 学习 | TD update with `max` over next-state actions; learns `Q*` regardless of behavior policy. |
| SARSA | "On-policy Q-learning" / SARSA | TD update using the actual next action; learns `Q^π` for current ε-greedy π. |
| Expected SARSA | "The low-variance SARSA" / 期望 SARSA | Replace sampled `a'` with its expectation under π. |
| GLIE | "Correct exploration schedule" / 无限探索极限贪心 | Greedy in the Limit with Infinite Exploration; needed for Q-learning convergence. |
| Bootstrapping | "Using current estimate in the target" / 自举 | What distinguishes TD from MC. Source of bias but massive variance reduction. |
| Maximization bias | "Q-learning overestimates" / 最大化偏差 | `max` over noisy estimates is upward-biased; fixed by Double Q-learning. |

## Más Leer más Leer más

- [Watkins & Dayan (1992). Q-learning](https://link.springer.com/article/10.1007/BF00992698) el papel original y la prueba de convergencia.
- [Sutton & Barto (2018). Ch. 6 — Temporal-Difference Learning](http://incompleteideas.net/book/RLbook2020.pdf) TD(0), SARSA, aprendizaje Q, SARSA esperada.
- [Hasselt (2010). Double Q-learning](https://papers.nips.cc/paper_files/paper/2010/hash/091d584fced301b442654dd8c23b3fc9-Abstract.html) fijar el sesgo de maximización.
- [Seijen, Hasselt, Whiteson, Wiering (2009). A Theoretical and Empirical Analysis of Expected SARSA](https://ieeexplore.ieee.org/document/4927542) la motivación esperada por SARSA.
- [Rummery & Niranjan (1994). On-line Q-learning using connectionist systems](https://www.researchgate.net/publication/2500611_On-Line_Q-Learning_Using_Connectionist_Systems) el documento que acuñó SARSA (entonces llamado "aprendizaje Q-conexionista modificado").
- [Sutton & Barto (2018). Ch. 7 — n-step Bootstrapping](http://incompleteideas.net/book/RLbook2020.pdf) generaliza TD(0) a TD(n), el camino desde el aprendizaje Q hasta los rastros de elegibilidad y, más tarde, GAE en PPO.
