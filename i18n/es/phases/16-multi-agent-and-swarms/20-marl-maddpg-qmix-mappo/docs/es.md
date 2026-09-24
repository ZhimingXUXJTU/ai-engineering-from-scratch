# MARL  MADDPG, QMIX, mapa MADDPG mapa MARL QMIX

> El patrimonio de aprendizaje reforzado de la coordinación multiagente, que todavía informa a los sistemas de LLM-agente en 2026. **MADDPG**(Lowe et al., NeurIPS 2017, arXiv:1706.02275) introdujo la Capacitación Centralizada, Ejecución Descentralizada (CTDE): cada crítico ve todos los estados y acciones de los agentes durante la capacitación; en el momento de la prueba solo ejecutan actores locales. Trabaja para entornos cooperativos, competitivos y mixtos. **QMIX**(Rashid et al., ICML 2018, arXiv:1803.11485) es la descomposición de valor con una red de mezcla monótona; por agente Qs se combinan en conjunto Q así `argmax`distribuye limpiamente  dominante en el StarCraft Multi-Agent Challenge (SMAC). **MAPPO**(Yu et al., NeurIPS 2022, arXiv:2103.01955) es PPO con una función de valor centralizada; "sorprendentemente eficaz" en el mundo de partículas, SMAC, Google Research Football, Hanabi con ajuste mínimo. Estas políticas sustentan las políticas de entrenamiento para equipos de agentes que deben actuar de manera descentralizada.**default 2026 cooperative-MARL baseline**Esta lección construye cada uno de ellos desde un pequeño juguete de la red y aterriza las tres ideas en la memoria muscular antes de tocar el entrenamiento de agente LLM.

> **【中文解读】**Este episodio presenta el método de acción de los agentes de la acción de la acción de la acción de la acción de la acción de la acción de la acción de la acción de la acción de la acción de la acción de la acción de la acción de la acción de la acción de la acción de la acción de la acción de la acción de la acción de la acción de la acción de la acción de la acción de la acción de la acción de la acción de la acción de la acción de la acción de la acción de la acción de la acción de la acción de la acción de la acción de la acción de la acción de la acción de la acción de la acción de la acción de la acción de la acción de la acción de la acción de la acción de la acción de la acción de la acción de la acción de la acción de la acción de la acción de la acción de la acción de la acción.

> **【拓展：marl maddpg qmix mappo→具体应用】**Más agentes 强化学习(MARL) algoritmo:(1) MADDPG cada agente tiene un actor-crítico independiente, pero el crítico puede ver todos los movimientos de los agentes;(2) QMIX集中式訓練分散式执行,通过混合网络保证单调性;(3) MAPPOPPO's Multi Agent 扩展──2026 MARL logró avances en el juego AI、机器人协作和交通控制, pero la aplicación en el agente LLM sigue siendo temprana──


**Type:** Learn | **类型:** 学习
**Languages:** Python (stdlib, small NumPy-free implementations) | **语言:** Python（标准库，无 NumPy 的小型实现）
**Prerequisites:** Phase 09 (Reinforcement Learning), Phase 16 · 09 (Parallel Swarm Networks) | **前置知识:** Phase 09（强化学习），Phase 16 · 09（并行群体网络）

> ¿ Qué es esto ?**【前置】**学本节前请先掌握:Fase 09(RL 基础 PPO/Q-learning) 、Fase 16·09(Swarm) ・MARL = 多 Agent 强化学习,CTDE(集中训练分散执行) ≠核心范式──
> ¿ Qué es esto ?**【类比】**MARL = "entrenamiento del equipo"―MADDPG = 教练看全场训练(集中评论),比赛时球员各自决策(分散演员);QMIX = Cada persona un Q 值,单调混合保证最优解可分;MAPPO = PPO多 Agent 版本──MAPPO 是 2026 合作 MARL 默认基线(" sorprendentemente eficaz"),SMAC、Google Football、Hanabi 都能少调参跑通──LLM Agent training 训练也借鉴这套范式──
**Time:** ~90 minutes | **时间:** ~90 分钟

## # El problema # # El problema #

Los sistemas de LLM-agentes entrenan cada vez más políticas para la coordinación entre agentes: cuándo diferir, cuándo actuar, cuál peer a llamar.

> LLM-Agent 系统越来越地训练 Agent 间协调策略:何时延迟何时行动调用哪个同伴──告诉你如何训练这些策略的文献是多 Agent 强化学习 ((MARL), fue más temprano que la ola de LLM, un grupo de algoritmos de dirección──

La lectura de los artículos MARL sin el vocabulario de patrones es dolorosa.

> 没有模式词汇表阅读 MARL 论文是痛苦的──集中训练分散执行(CTDE)、值分解和集中式评论家不是流行词它们是特定问题的特定答案:

- El RL independiente (cada agente aprende solo) no es estacionario desde la perspectiva de cada agente.
  En inglés, "RL independiente" (RL independiente) es un lenguaje que se usa para hablar de la naturaleza de la persona.
- La RL centralizada (un agente controla a todos) no escala y viola las restricciones de ejecución.
  En la traducción de inglés, "RL" se dice "RL" en inglés, "RL" en inglés, "RL" en inglés, "RL" en inglés, "RL" en inglés, "RL" en inglés, "RL" en inglés, "RL") en inglés, "RL" en inglés, "RL" en inglés, "RL" en inglés, "RL" en inglés, "RL" en inglés, "RL" en inglés, "RL" en inglés, "RL" en inglés, "RL" en inglés, "RL" en inglés, "RL" en inglés, "R" en inglés, "R" en inglés, "R" en inglés, "R" en inglés, "R" en inglés, "R" en inglés, "R" en inglés, "R" en inglés, "R" en inglés, "R" en inglés, "R" en inglés, "R" en inglés, "R" en inglés, "R" en inglés, "R" en inglés, "R" en inglés, "R" en inglés, "en" en inglés, "en" en inglés, "en" en inglés, "en" en inglés, "en" en inglés, "en inglés, "en" en inglés, "en inglés, " en inglés, "en inglés, " en inglés, " en inglés, " en inglés, " en inglés, " en inglés, " en inglés, " en inglés, " en inglés, " en inglés, " en inglés, " en inglés, " en inglés, " en inglés, " en inglés, " en inglés, " en inglés, " en inglés, " en inglés, " en inglés, " en inglés, " en inglés, " en inglés, " en inglés, " en inglés, " en inglés, " en inglés, " en inglés, " en inglés, " en inglés, " en inglés, " en inglés, " en inglés, " en inglés, " en inglés ur ur ur ur ur ur ur ur ur ur ur ur ur ur ur ur ur ur ur ur ur ur ur ur ur ur ur ur ur ur ur ur ur ur ur ur ur ur ur ur ur ur ur ur ur ur ur ur ur ur ur ur ur ur ur ur ur ur ur ur ur ur ur ur ur ur ur ur ur ur ur ur ur ur ur
- CTDE obtiene lo mejor de ambos: entrenar con información global, desplegar con políticas locales.
  China: CTDE 兼得两者之长: con el entrenamiento de información de la región, con la estrategia de la región.

## Concepto de la esencia de la concepción

### Tres entornos que utilizan los periódicos

- **Particle World (multi-agent particle env).**Física 2D simple con tareas cooperativas y competitivas.
- **StarCraft Multi-Agent Challenge (SMAC).**La micro gestión cooperativa, la observación parcial, el banco de pruebas de QMIX, acciones discretas, estados continuos.
- **Google Research Football, Hanabi, MPE.**Las líneas de base de MAPPO.

Los diferentes entornos tienen diferentes tipos de acción/observación.

### MADDPG (2017)  el patrón CTDE

Cada agente .`i`Tiene un actor.`mu_i(o_i)`El objetivo de la Comisión es que la Comisión pueda adoptar medidas de seguridad y de seguridad para garantizar que las medidas adoptadas sean eficaces.`Q_i(x, a_1, ..., a_n)`El actor se actualiza por gradiente de política frente a la evaluación del crítico.

```
actor update:    grad_theta_i J = E[grad_theta mu_i(o_i) * grad_a_i Q_i(x, a_1..n) at a_i=mu_i(o_i)]
critic update:   TD on Q_i(x, a_1..n) given next-state joint estimate
```

Por qué CTDE: en el tiempo de entrenamiento, conocemos las acciones de todos; lo utilizamos para reducir la variación en cada crítico.`o_i`y llamadas .`mu_i(o_i)`¿ Qué ?

Modo de falla: los críticos crecen con N agentes (la entrada incluye todas las acciones). No se escala más allá de ~ 10 agentes sin aproximaciones.

### QMIX (2018)  Descomposición de valor

La recompensa global es la suma de una función monótona de valores Q por agente:

```
Q_tot(tau, a) = f(Q_1(tau_1, a_1), ..., Q_n(tau_n, a_n)),   df/dQ_i >= 0
```

La monotonía garantiza `argmax_a Q_tot`puede ser calculado por cada agente que elija`argmax_{a_i} Q_i`¿Qué es lo que se dice?**exactly the decentralized execution property**En el tiempo de entrenamiento, una red de mezcla produce`Q_tot`de los Qs por agente.

Por qué QMIX gana en SMAC: la micro gestión cooperativa StarCraft tiene agentes homogéneos, obs local, recompensa global  perfecto para la descomposición de valor.

Modo de falla: la restricción de monotonicidad es restrictiva; algunas tareas tienen estructuras de recompensa que no son monótonas descomponibles (un agente sacrificando para el equipo).

### MAPPO (2022)  el incumplimiento no observado

PPO multi-agente: PPO con una función de valor centralizada. Cada agente tiene su propia política; todos los agentes comparten (o tienen por agente) funciones de valor que ven el estado completo. Yu et al. 2022 compararon MAPPO con MADDPG, QMIX y sus extensiones en cinco puntos de referencia y encontraron:

- MAPPO coincide o supera los métodos MARL fuera de la política en el mundo de partículas, SMAC, Google Research Football, Hanabi, MPE.
- Se requiere un ajuste mínimo de los hiperparámetros.
- Formación estable; reproducible entre semillas.

La comunidad subestimó la política MARL hasta este documento. En 2026, MAPPO es la línea de base predeterminada para la MARL cooperativa; cualquier nuevo método debe vencerlo.

### ¿Por qué los ingenieros de LLM deben preocuparse

Tres usos directos:

1. **Router training.**Un meta-agente elige qué sub-agente maneja una tarea. Este es un problema MARL con N sub-agentes descentralizados y un router centralizado.
2. **Role emergence.**En las simulaciones de agentes generativos, los agentes de formación para adoptar roles complementarios con el tiempo es un problema MARL disfrazado.
3. **Multi-agent tool use.**Cuando los agentes comparten herramientas y compiten por el presupuesto, la formación de ellos a través de CTDE produce políticas locales desplegables que respetan las restricciones de recursos.

En el año 2026, la mayoría de los sistemas de agentes de LLM de producción impulsan sus políticas en lugar de entrenarlos. MARL entra cuando usted tiene (a) muchos datos de interacción, (b) una señal clara de recompensa y (c) la voluntad de invertir en infraestructura de capacitación.

### CTDE como patrón de diseño más allá de RL

Incluso sin formación, CTDE es un patrón arquitectónico útil:

- Durante el diseño, asuma la visibilidad del equipo.
- En *runtime*, ejecutar la ejecución descentralizada: cada agente sólo ve `o_i`¿ Qué ?

El patrón te obliga a mantener el estado por agente explícito y a pensar en la observabilidad parcial de antemano.

### El problema de la no estacionalidad

Cuando varios agentes aprenden simultáneamente, el entorno de cada agente (que incluye las políticas de otros) es no estacionario. Las pruebas clásicas de RL de un solo agente se rompen.

- MADDPG: el crítico global ve todas las acciones, por lo que su estimación de valor es estacionaria.
- QMIX: la descomposición de valores traslada el aprendizaje a un espacio de Q conjunta donde la óptimalidad está bien definida.
- MAPPO: la función de valor centralizado disminuye la variación de los cambios de política de otros.

En los sistemas de agentes LLM, la no estacionariedad se manifiesta como "mi agente trabajó el mes pasado, ahora que otro agente en el río arriba cambió, la mina se comporta mal". El entrenamiento MARL con CTDE es la solución de principio; las correcciones de nivel inmediato son más rápidas pero menos duraderas.

### Lo que esta lección NO abarca

El entrenamiento de las redes reales es un tema de la Fase 09 . Esta lección construye versiones de políticas scriptadas que demuestran los patrones de CTDE, de descomposición de valor y de valor centralizado sin actualizaciones de gradientes. El objetivo es internalizar los patrones antes de recoger una biblioteca MARL completa (PyMARL, MARLlib, RLlib multi-agente).

## Construye con movimiento.
```figure
sw-ctde
```

## Construye el mismo

`code/main.py`Implementa tres demostraciones de patrones, todas en un pequeño mundo de red cooperativa de 2 agentes:

- Medio ambiente: 2 agentes en una cuadrícula 4x4, una pelleta de recompensa.
  En el contexto de la investigación, el equipo de investigación de la Universidad de Chicago (U.S.) ha realizado un estudio de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de los resultados de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de los resultados de la investigación de la investigación de la investigación de la investigación de la investigación de la investigación de la cucienca.
- `IndependentAgents` cada agente trata a los demás como el medio ambiente.
  En inglés:`IndependentAgents` Cada agente será otro agente 视为环境――基线――
- `MADDPGStyle` El crítico centralizado calcula un valor común; las políticas de los actores se actualizan a partir de él.
  En inglés:`MADDPGStyle` 集中式评论家计算联合值;Actor 策略从中更新──脚本化策略改进──
- `QMIXStyle` Descomposición de valor con un mezclador monótono.
  En inglés:`QMIXStyle` 带单调混合器的值分解──
- `MAPPOStyle` función de valor centralizada; actualización de las políticas en relación con la línea de base compartida.
  En inglés:`MAPPOStyle` 集中式值函数;策略对共享基线更新──

Las cuatro versiones de CTDE convergen a caminos más cortos que la línea de base independiente.

> Todos los cuatro ejecutivos de la misma recorrido y reportan un número de pasos promedio para alcanzar el objetivo.

- ¿Qué quieres decir ?

```
python3 code/main.py
```

Resultados esperados: los agentes independientes toman ~ 6 pasos en promedio; las variantes CTDE convergen hacia ~ 3.5 pasos (el óptimo para la cuadrícula 4x4 es 3). La diferencia de patrón aparece a pesar de las políticas scriptadas.

## Usalo.

`outputs/skill-marl-picker.md`es una habilidad que elige un algoritmo MARL para una tarea multi-agente dada: cooperativa vs competitiva, homogénea vs heterogénea, tipo de espacio de acción, escala, señal de recompensa.

## Envíalo .

El MARL en producción es raro.

- **Start with MAPPO.**El documento de 2022 estableció esto como la línea de base; reproducirlo primero ahorra semanas de perseguir métodos más sofisticados.
  En inglés:**从 MAPPO 开始。**El artículo de 2022 se establecerá como base; antes de repetir, se puede ahorrar varias semanas para perseguir métodos más sofisticados.
- **Log every agent's observation and action stream.**Desarmar el MARL sin rastro de agente es inútil.
  En inglés:**记录每个 Agent 的观察和动作流。**No hay ningún agente que pueda hacer el trabajo de MARL.
- **Separate training code from execution code.**El CTDE es una disciplina; deja que el camino de ejecución realmente sólo vea `o_i`¿ Qué ?
  En inglés:**分离训练代码和执行代码。**CTDE es una forma de hacer que el camino de ejecución sea realmente visto.`o_i`¿Qué es eso?
- **Reward shaping warning.**MARL es muy sensible al diseño de recompensas. un error de coordinación en la configuración y los agentes aprenden a explotarlo. ejecutar pruebas adversarias.
  En inglés:**奖励塑形警告。**MARL para el diseño de premios es muy sensible. Un error de coordinación en la forma de plástico deja que el agente aprenda a utilizarlo.
- **For LLM agents**En primer lugar, considere las políticas de nivel inmediato.Invertir en la formación MARL sólo cuando los datos de interacción + señal de recompensa + infraestructura están todos presentes.
  En inglés:**对于 LLM Agent**, primero considerar las estrategias de nivel de información. Sólo en datos de interacción +  recompensa +  infraestructura están preparados para invertir en MARL  formación.

## Los ejercicios.

1. - ¿ Qué ?`code/main.py`. Medir la brecha de pasos a objetivos entre agentes independientes y de tipo MAPPO. ¿La brecha crece o se reduce en una rejilla de 6x6?
2. Implementar una variante competitiva: dos agentes, una pelleta, sólo el primero en alcanzar recibe una recompensa. ¿Qué patrón maneja la competencia limpio?
3. Lea MADDPG (arXiv:1706.02275) Sección 3. Implemente simbólicamente la regla de actualización crítica exacta en pseudocodo en sus propias palabras.
4. ¿Por qué los autores argumentan que el valor centralizado + PPO supera a MARL fuera de la política en sus puntos de referencia?
5. Aplicar CTDE como patrón de diseño a un sistema hipotético de agentes de LLM (por ejemplo, agente de investigación + resumidor + codificador). ¿Cuál es la información conjunta disponible en el momento del diseño que no está disponible en el tiempo de ejecución?

## Términos clave .

| Term | What people say | What it actually means |
|------|----------------|------------------------|
| MARL / 多 Agent 强化学习 | "Multi-Agent RL" / "多 Agent 强化学习" | Reinforcement learning for multi-agent systems. / 多 Agent 系统的强化学习。 |
| CTDE / 集中训练分散执行 | "Centralized Training, Decentralized Execution" / "集中训练分散执行" | Train with global info; deploy with local policies. / 用全局信息训练；用局部策略部署。 |
| MADDPG | "Multi-Agent DDPG" / "多 Agent DDPG" | CTDE with per-agent critic seeing all observations + actions. / CTDE，每个 Agent 的评论家看到所有观察 + 动作。 |
| QMIX / 值分解 | "Value decomposition" / "值分解" | Monotonic mixing of per-agent Qs. Cooperative. / 每 Agent Q 的单调混合。协作型。 |
| MAPPO / 多 Agent PPO | "Multi-Agent PPO" / "多 Agent PPO" | PPO with centralized value function. 2026 default baseline. / 带集中式值函数的 PPO。2026 默认基线。 |
| Value decomposition / 值分解 | "Sum of individual Qs" / "个体 Q 之和" | Joint Q represented as a monotone function of per-agent Qs. / 联合 Q 表示为每 Agent Q 的单调函数。 |
| Non-stationarity / 非平稳性 | "Moving targets" / "移动目标" | Each agent's env changes as others learn. The core MARL problem. / 每个 Agent 的环境随着其他 Agent 学习而变化。核心 MARL 问题。 |
| On-policy / off-policy / 同策略/离策略 | "Learn from current / replay" / "从当前/回放学习" | PPO is on-policy (MAPPO); DDPG and Q-learning are off-policy. / PPO 是同策略（MAPPO）；DDPG 和 Q-learning 是离策略。 |
| SMAC / 星际争霸多 Agent 挑战 | "StarCraft Multi-Agent Challenge" / "星际争霸多 Agent 挑战" | Cooperative micromanagement benchmark; QMIX's homegrown ground. / 协作微操基准；QMIX 的主战场。 |

## Más Leer más Leer más

- [Lowe et al. — Multi-Agent Actor-Critic for Mixed Cooperative-Competitive Environments](https://arxiv.org/abs/1706.02275) MADDPG; NeurIPS 2017
- [Rashid et al. — QMIX: Monotonic Value Function Factorisation for Deep Multi-Agent Reinforcement Learning](https://arxiv.org/abs/1803.11485) QMIX; ICML 2018
- [Yu et al. — The Surprising Effectiveness of PPO in Cooperative Multi-Agent Games](https://arxiv.org/abs/2103.01955) MAPPO; NeurIPS 2022
- [BAIR blog post on MAPPO](https://bair.berkeley.edu/blog/2021/07/14/mappo/) Enmarcado legible del resultado de la MAPPO
- [SMAC repository](https://github.com/oxwhirl/smac) StarCraft Multi-Agent Challenge
