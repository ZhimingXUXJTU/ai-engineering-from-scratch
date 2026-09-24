# RL multi-agente , más inteligentes en la química .

> El RL de agente único supone que el entorno está estacionario. Colocar dos agentes de aprendizaje en el mismo mundo y esa suposición se rompe: cada agente es parte del entorno del otro, y ambos están cambiando.

> **【中文解读】**单智能体 RL 假设环境是平稳的──但放入两个同时学习的智能体后, cada智能体都成为对方环境的一部分环境不再平稳,马尔可夫假设被打破──多智能体 RL就是处理"todos están en cambio"的收收问题──

**Type:** Build | **类型:** 动手
**Languages:** Python | **语言:** Python
**Prerequisites:** Phase 9 · 04 (Q-learning), Phase 9 · 06 (REINFORCE), Phase 9 · 07 (Actor-Critic) | **前置知识:** Phase 9 · 04 (Q-learning), Phase 9 · 06 (REINFORCE), Phase 9 · 07 (Actor-Critic)
**Time:** ~45 minutes | **时间:** ~45 分钟

## El problema es la introducción del problema

Un robot que aprende a navegar por una habitación es un problema de RL de un solo agente. Un equipo de fútbol no lo es. Los oponentes de AlphaStar vs StarCraft no lo son. Un mercado de agentes de licitación no lo es. Dos coches negociando una parada de cuatro vías no lo son. Muchos problemas en el mundo real no lo son.

> 机器人学习在房间中导航是单智能体 RL 问题──足球队不是──AlphaStar对StarCraft对手不是──竞价代理的市场不是──两辆车协商四路停车不是──多对多现实世界问题都不是──

En cada entorno multi-agente, desde la perspectiva de cualquier agente, los otros agentes son parte del medio ambiente. A medida que aprenden y cambian su comportamiento, el entorno se vuelve no estacionario. La propiedad de Markov  "el próximo estado depende sólo del estado actual y mi acción"  se viola porque el siguiente estado también depende de lo que los otros agentes eligieron, y sus políticas son objetivos móviles.

> En cada entorno multi-inteligente, desde el punto de vista de cada uno de ellos, los otros inteligentes son parte del entorno. Cuando aprenden y cambian de comportamiento, el entorno se vuelve poco estable. La capacidad de adaptación se viola, ya que el estado siguiente también depende de la elección de otros inteligentes, y su estrategia es la meta móvil.

Esto rompe las pruebas de convergencia tabular (la garantía de Q-learning asume un entorno estacionario). También rompe la RL profunda ingenuo: los agentes se persiguen unos a otros en bucles, nunca convergen a una política estable. Se necesitan técnicas específicas de múltiples agentes: entrenamiento centralizado / ejecución descentralizada, líneas de base contrafactuales, juego de liga, auto-juego.

> Esto destruyó el modelo de aprendizaje de Q-learning (Q-learning) ⋅ también destruyó el simple profundo ciclo de persecución entre los cuerpos inteligentes, siempre sin alcanzar una estrategia de estabilidad ⋅ necesitas más cuerpos inteligentes ⋅ tecnología especial: concentración de entrenamiento/ distribución de ejecución ⋅ contrasistencias ⋅ coalición de entrenamiento ⋅ auto-exploración ⋅

Aplicaciones 2026: enjambres de robots, enrutamiento de tráfico, flotas de vehículos autónomos, simuladores de mercado, sistemas LLM multiagente (fase 16) y cualquier juego con más de un jugador inteligente.

> Aplicación 2026 años: máquina de trabajo, transporte, conducción automática, mercado de modelos, sistema de gestión de empresas de múltiples inteligencias, fase 16), así como cualquier juego con varios jugadores inteligentes.

> **【中文解读】**El reto central de un grupo de RL es la de no tener equilibrio en el aprendizaje. El grupo de RL tiene cuatro modalidades principales: aprendizaje independiente.

> **【拓展：多智能体→LLM Agent系统】**La aplicación más popular de MARL en 2026 es multi-inteligente LLM: multi-modelo Agent 协作完成复杂任务――Modeo multi-agent 模式、AutoGen、CrewAI, etc. En esencia, son las extensiones de la idea MARL en el campo de la lengua Agent―.

## El concepto central.

![Four MARL regimes: indep, centralized critic, self-play, league](../assets/marl.svg)

**Formalism: Markov Game.**Una generalización de la MDP: estados `S`, una acción conjunta `a = (a_1, …, a_n)`, transición `P(s' | s, a)`, y recompensas por agente `R_i(s, a, s')`Cada agente .`i`maximiza su propio rendimiento bajo su propia política `π_i`Si las recompensas son idénticas, es**fully cooperative**Si es suma cero, es**adversarial**Si se mezcla, es**general-sum**¿ Qué ?

> **形式化：马尔可夫博弈。**MDP 的推广: estado `S`、 unidos `a = (a_1, …, a_n)`、 traslado `P(s'|s,a)`、 recompensas para cada cuerpo inteligente `R_i`Si la recompensa es igual,**全合作**Si es 0和, es**对抗**Si se mezcla, es**一般和**¿Qué es eso?

**Core challenges:**

- **Non-stationarity.** `P(s' | s, a_i)`de un agente .`i`La visión depende de`π_{-i}`, que está cambiando.
  **非平稳性。**Desde el cuerpo inteligente`i`La transformación depende de la estrategia de otros cuerpos inteligentes que están cambiando.
- **Credit assignment.**Con una recompensa compartida, ¿qué agente la causó?
  **信用分配。**¿Cuál es el resultado de la recompensa compartida?
- **Exploration coordination.**Los agentes deben explorar estrategias complementarias, no explorar redundantemente el mismo estado.
  **探索协调。**El cuerpo inteligente debe explorar estrategias complementarias, no explorar el mismo estado.
- **Scalability.**El espacio de acción conjunta crece exponencialmente en `n`¿ Qué ?
  **可扩展性。**联合动作空间随                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        `n`El número de personas en el país
- **Partial observability.**Cada agente sólo ve su propia observación; el estado global está oculto.
  **部分可观察性。**Cada cuerpo inteligente sólo ve su propia observación; el estado de la situación está oculto.

**Four dominant regimes:**

> **四种主导范式：**

**1. Independent Q-learning / independent PPO (IQL, IPPO).**Cada agente aprende su propia Q o política, tratando a los demás como parte del entorno. Simple, a veces funciona (especialmente con la repetición de la experiencia que actúa como un truco de modelado de agente suavizante). Convergencia teórica: ninguno.

> **1. 独立 Q-learning / 独立 PPO。**Cada cuerpo inteligente aprende su propio Q o estrategia, y el otro cuerpo inteligente es considerado como parte del medio ambiente.

**2. Centralized training, decentralized execution (CTDE).**El paradigma moderno más común.`π_i`que las condiciones de la observación local `o_i` ejecución descentralizada estándar en el despliegue.`Q(s, a_1, …, a_n)`condiciones sobre el estado global completo y la acción conjunta.
- **MADDPG**(Lowe et al. 2017): DDPG con un crítico centralizado por agente.
- **COMA**(Foerster et al. 2017): base contrafactual  preguntar "cuál habría sido mi recompensa si hubiera tomado medidas `a'`¿En cambio?"  aisla mi contribución.
- **MAPPO**- ¿ Qué ?**IPPO**con crítico compartido (Yu et al. 2022): PPO con función de valor centralizada.
- **QMIX**(Rashid et al. 2018): descomposición del valor  `Q_tot(s, a) = f(Q_1(s, a_1), …, Q_n(s, a_n))`con mezcla monótona.

> **2. 集中训练，分布执行（CTDE）。**La última norma moderna es que cada cuerpo inteligente tiene su propia estrategia, sólo depende de la localidad de observación.

**3. Self-play.**Dos copias del mismo agente se juegan entre sí. La política del oponente es mi política de un instante pasado. AlphaGo / AlphaZero / MuZero. OpenAI Five. Funciona mejor para juegos de suma cero; la señal de entrenamiento es simétrica.

> **3. 自我博弈。**Las dos copias del mismo cuerpo inteligente son las de la misma manera.

**4. League play.**Una extensión del juego propio a entornos de suma general / adversarial: mantener una población de políticas pasadas y actuales, probar un oponente de la liga, entrenar contra ellos. Agrega explotadores (especializados en vencer a los mejores actuales) y explotadores principales (especializados en vencer a explotadores). AlphaStar (StarCraft II). Necesitado cuando el juego admite ciclos de estrategia "rock-paper-scissors".

> **4. 联盟训练。**La expansión de la plataforma de juego de la plataforma de juego de la plataforma de juego de la plataforma de juego de la plataforma de juego de la plataforma de juego de la plataforma de juego de la plataforma de juego de la plataforma de juego de la plataforma de juego de la plataforma de juego de la plataforma de juego de la plataforma de juego de la plataforma de juego de la plataforma de juego de la plataforma de juego de la plataforma de juego de la plataforma de juego de la plataforma de juego de la plataforma de juego de la plataforma de juego de la plataforma de juego de la plataforma de juego de la plataforma de juego de la plataforma de juego de la plataforma de juego de la plataforma de juego de la plataforma de juego de la plataforma de juego de la plataforma de juego de la plataforma de juego de la plataforma de juego de la plataforma de juego de la plataforma de juego de la plataforma de juego de la plataforma de juego de la plataforma de juego de la plataforma de juego de la plataforma de juego de la plataforma de juego de la plataforma de juego de la plataforma de juego de la plataforma de juego de la plataforma de juego de juego de la plataforma de juego de juego de la plataforma de juego de juego de la plataforma de juego de juego de la plataforma de juego de juego de juego de la plataforma de juego de juego de juego de la plataforma de juego de juego de juego de juego de la plataforma de juego de juego de juego de juego de la plataforma de juego de juego de juego de juego de juego de juego de la plataforma de juego de juego de juego de juego de juego de juego de juego de juego de juego de juego de juego de juego de juego de juego de juego de juego de juego de juego de juego de juego de juego de juego de juego de juego de juego de juego de juego de juego de juego de juego de juego de juego de juego de juego de juego de juego de juego de juego de juego de juego de juego de juego de juego de juego de juego de juego de juego de juego de juego de juego de juego de juego de juego de juego de juego de juego de juego de juego de juego de juego de juego de juego de juego de juego de juego de juego de juego de juego de juego de juego de juego de juego de juego de juego de juego de juego de juego de juego de juego de juego de juego de juego de juego de juego de juego de juego de juego de juego de juego de juego de juego de juego de juego de juego de juego de juego de juego de juego de juego de juego de juego de juego de

**Communication.**Permita a los agentes enviar mensajes aprendidos .`m_i`Foerster et al. (2016) mostró que la comunicación inter-agente diferenciable se puede entrenar de extremo a extremo.

> **通信。**允许智能体相互发送学习的消息――有效在合作环境中―― hoy en día, el sistema de LLM 多智能体系统 básicamente utiliza la comunicación en lenguaje natural―

## Construye y realiza.
```figure
f3-marl-orbit
```

## Construye el mismo

Esta lección utiliza un GridWorld 6×6 con dos agentes cooperativos. Comienzan en esquinas opuestas y deben alcanzar un objetivo compartido.`-1`por paso mientras cualquiera de los agentes está todavía en movimiento,`+10`Cuando ambos lleguen.`code/main.py`¿ Qué ?

> Este curso utiliza un 6×6 GridWorld y dos equipos inteligentes de cooperación. Ellos salen de la esquina, deben alcanzar el objetivo compartido.

### Paso 1: el entorno multiagente

```python
class CoopGridWorld:
    def __init__(self):
        self.size = 6
        self.goal = (5, 5)

    def reset(self):
        return ((0, 0), (5, 0))  # two agents

    def step(self, state, actions):
        a1, a2 = state
        new1 = move(a1, actions[0])
        new2 = move(a2, actions[1])
        done = (new1 == self.goal) and (new2 == self.goal)
        reward = 10.0 if done else -1.0
        return (new1, new2), reward, done
```

El espacio de acción *joint* es `|A|² = 16`El estado global es de dos posiciones.

> * Unidos* movimiento espacio es `|A|² = 16`Todo el mundo está en dos posiciones.

### Paso 2: aprendizaje Q independiente

Cada agente ejecuta su propia tabla Q con teclado en estado conjunto. En cada paso: ambos eligen acciones ε-avidas, recogen transición conjunta, cada uno actualiza su propio Q con la recompensa compartida.

```python
def independent_q(env, episodes, alpha, gamma, epsilon):
    Q1, Q2 = defaultdict(default_q), defaultdict(default_q)
    for _ in range(episodes):
        s = env.reset()
        while not done:
            a1 = epsilon_greedy(Q1, s, epsilon)
            a2 = epsilon_greedy(Q2, s, epsilon)
            s_next, r, done = env.step(s, (a1, a2))
            target1 = r + gamma * max(Q1[s_next].values())
            target2 = r + gamma * max(Q2[s_next].values())
            Q1[s][a1] += alpha * (target1 - Q1[s][a1])
            Q2[s][a2] += alpha * (target2 - Q2[s][a2])
            s = s_next
```

Trabaja en esta tarea porque las recompensas son densas y alineadas. No logra tareas estrechamente vinculadas (por ejemplo, donde un agente tiene que *esperar* al otro).

> En este trabajo es válido, porque la recompensa es intensa y en conjunto. En el trabajo de estrecha colaboración, el fracaso es un fracaso.

### Paso 3: Q centralizado con actualización de valor descompuesto

Utilice un Q en las acciones conjuntas `Q(s, a_1, a_2)`Actualización de la recompensa compartida. Descentraliza en la ejecución marginalizando: `π_i(s) = argmax_{a_i} max_{a_{-i}} Q(s, a_1, a_2)`. Trades espacio de acción conjunto exponencial para una visión global *correcta*

> Utiliza un Q. en el conjunto de movimientos. Desde el compartimiento de premios hasta la actualización.

### Paso 4: juego propio simple (adversario 2-agente)

El mismo agente, dos papeles.`K`Los episodios, copiar los pesos de A en B. Entrenamiento simétrico, progreso constante.

> Como un cuerpo inteligente, dos papeles. Entrenamiento A contra B.`K` 回合后将 A's权重复复制到B──对称训练,持续进步──AlphaZero 配方的缩影──

## Las trampas

- **Non-stationary replay.**La experiencia de repetición con agentes independientes es peor que la de un solo agente porque las viejas transiciones fueron generadas por oponentes ahora obsoletos.
  **非平稳回放。**La experiencia de un cuerpo inteligente independiente es peor que la de un solo cuerpo inteligente, ya que la transferencia antigua es generada por los oponentes del pasado.
- **Credit assignment ambiguity.**Recompensa compartida después de un largo episodio; no hay manera clara de decir qué agente contribuyó.
  **信用分配模糊。**长回合后的共享奖励; no se puede determinar qué contribuyó el cuerpo inteligente.
- **Policy drift / chasing.**Las mejores respuestas de cada agente cambian con la actualización de los demás.
  **策略漂移/追逐。**El mejor respuesta de cada cuerpo inteligente es la actualización y cambio de los demás cuerpos inteligentes.
- **Reward hacking via coordination.**Los agentes encuentran exploits coordinados que el diseñador no anticipó. Los agentes de subastas convergen a la oferta cero.
  **协调奖励黑客。**智能体发现设计者未预料的协调漏洞──修复:仔细的奖励设计、行为约束──
- **Exploration redundancy.**Ambos agentes exploran los mismos pares de acciones de estado.
  **探索冗余。**两个 inteligentes exploran el mismo estado-actividad para ⋅ Re: ⋅ Re: ⋅ Re: ⋅ Re: ⋅ Re: ⋅ Re: ⋅ Re: ⋅ Re: ⋅ Re: ⋅ Re: ⋅ Re: ⋅ Re: ⋅ Re: ⋅ Re: ⋅ Re: ⋅ Re: ⋅ Re: ⋅ Re: ⋅ Re: ⋅ Re: ⋅ Re: ⋅ Re: ⋅ Re: ⋅ Re: ⋅ Re: ⋅ Re: ⋅ Re: ⋅ Re: ⋅ Re: ⋅ Re: ⋅ Re: ⋅ Re: ⋅ Re: ⋅ Re: ⋅ Re: ⋅ Re: ⋅ Re: ⋅ Re: ⋅ Re: ⋅ Re: ⋅ Re: ⋅ Re: ⋅ Re: ⋅ Re: ⋅ Re: ⋅ Re: ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅                                                                                                                                                                                                                                   
- **League cycles.**El juego puro puede quedar atrapado en un ciclo de dominación.
  **联盟循环。**純自我博可能陷入支配循环──修复:多样化对手的联盟训练──
- **Sample explosion.** `n`Los agentes × espacio de estado × acciones conjuntas. Aproximado con aproximación de funciones; espacios de acción factorizados (una cabeza de salida de política por agente).
  **样本爆炸。**n 个智能体 × 状态空间 × 联合动作──用函数近似解决;因子化动作空间──

## Usalo con el marco de ejecución

El mapa de aplicaciones MARL 2026:

> 2026 años MARL 应用地图:

| Domain | Method | Notes |
|--------|--------|-------|
| Domain / 领域 | Method / 方法 | Notes / 备注 |
| Cooperative navigation / manipulation / 合作导航/操作 | MAPPO / QMIX | CTDE; shared critic + decentralized actors. / CTDE；共享 Critic + 分布式 Actor。 |
| Two-player games (chess, Go, poker) / 双人游戏 | Self-play with MCTS (AlphaZero) | Zero-sum; symmetric training. / 零和；对称训练。 |
| Complex multiplayer (Dota, StarCraft) / 复杂多人游戏 | League play + imitation pretraining | OpenAI Five, AlphaStar. |
| Autonomous-vehicle fleets / 自动驾驶车队 | CTDE MAPPO / PPO with attention | Partial obs; variable team sizes. / 部分可观察；可变团队大小。 |
| Auction markets / 拍卖市场 | Game-theoretic equilibrium + RL | Mean-field RL when `n` → ∞. / n→∞ 时用平均场 RL。 |
| LLM multi-agent systems (Phase 16) / LLM 多智能体系统 | Natural-language comm + role conditioning | RL loop at the agent-planning layer. / Agent 规划层的 RL 循环。 |

En 2026, el área de crecimiento más grande de MARL es la base de LLM: enjambres de agentes del modelo de lenguaje que negocian, debaten, construyen software.

> El mayor crecimiento del MARL en 2026 se basará en el área de LLM: lenguaje modelo inteligente grupo de negociación, debate, construcción de software, RL aparece en la forma de la optimización de los resultados, y no en la forma de los tokens.

## Envíe el producto .

Salvo como`outputs/skill-marl-architect.md`¿Qué es esto ?

```markdown
---
name: marl-architect
description: Pick the right multi-agent RL regime (IPPO, CTDE, self-play, league) for a given task.
version: 1.0.0
phase: 9
lesson: 10
tags: [rl, multi-agent, marl, self-play]
---

Given a task with `n` agents, output:

1. Regime classification. Cooperative / adversarial / general-sum. Justify.
2. Algorithm. IPPO / MAPPO / QMIX / self-play / league. Reason tied to coupling tightness and reward structure.
3. Information access. Centralized training (what global info goes to the critic)? Decentralized execution?
4. Credit assignment. Counterfactual baseline, value decomposition, or reward shaping.
5. Exploration plan. Per-agent entropy, population-based training, or league.

Refuse independent Q-learning on tightly-coupled cooperative tasks. Refuse to recommend self-play for general-sum with cycle risks. Flag any MARL pipeline without a fixed-opponent eval (cherry-picked self-play numbers are common).
```

## Los ejercicios.

1. **Easy.**Entrenamiento independiente de aprendizaje Q en la cooperativa de 2 agentes GridWorld. ¿Cuántos episodios hasta que el retorno medio > 0?
2. **Medium.**Añadir una tarea de "coordinación": el objetivo se alcanza sólo cuando ambos agentes se acercan a él en el mismo giro. ¿Q independiente todavía converge? ¿Qué se rompe?
3. **Hard.**Implementar un critico centralizado para la formación al estilo MAPPO y comparar la velocidad de convergencia con la PPO independiente en la tarea de coordinación.

## Términos clave .

| Term | What people say | What it actually means |
|------|-----------------|-----------------------|
| Markov game | "Multi-agent MDP" / 马尔可夫博弈 | `(S, A_1, …, A_n, P, R_1, …, R_n)`; each agent has its own reward. |
| CTDE | "Centralized training, decentralized execution" / 集中训练分布执行 | Joint critic at training time; each agent's policy uses only local obs. |
| IPPO | "Independent PPO" / 独立 PPO | Each agent runs PPO separately. Simple baseline; often underrated. |
| MAPPO | "Multi-agent PPO" / 多智能体 PPO | PPO with a centralized value function conditioned on global state. |
| QMIX | "Monotonic value decomposition" / 单调值分解 | `Q_tot = f_monotone(Q_1, …, Q_n)` allows decentralized argmax. |
| COMA | "Counterfactual multi-agent" / 反事实多智能体 | Advantage = my Q minus expected Q marginalizing over my action. |
| Self-play | "Agent vs past self" / 自我博弈 | Single agent, two roles; standard for zero-sum games. |
| League play | "Population training" / 联盟训练 | Cache past policies, sample opponents from the pool; handles strategy cycles. |

## Más Leer más Leer más

- [Lowe et al. (2017). Multi-Agent Actor-Critic for Mixed Cooperative-Competitive Environments (MADDPG)](https://arxiv.org/abs/1706.02275) CTDE con un crítico centralizado.
- [Foerster et al. (2017). Counterfactual Multi-Agent Policy Gradients (COMA)](https://arxiv.org/abs/1705.08926) líneas de base contrafactuales para la asignación de créditos.
- [Rashid et al. (2018). QMIX: Monotonic Value Function Factorisation](https://arxiv.org/abs/1803.11485) Descomposición de valores con monotonía.
- [Yu et al. (2022). The Surprising Effectiveness of PPO in Cooperative Multi-Agent Games (MAPPO)](https://arxiv.org/abs/2103.01955) La PPO es sorprendentemente fuerte para MARL.
- [Vinyals et al. (2019). Grandmaster level in StarCraft II using multi-agent reinforcement learning (AlphaStar)](https://www.nature.com/articles/s41586-019-1724-z) juego de liga en escala.
- [Silver et al. (2017). Mastering the game of Go without human knowledge (AlphaGo Zero)](https://www.nature.com/articles/nature24270) juego puro en juegos de suma cero.
- [Sutton & Barto (2018). Ch. 15 — Neuroscience & Ch. 17 — Frontiers](http://incompleteideas.net/book/RLbook2020.pdf) incluye el tratamiento corto del manual de configuraciones de múltiples agentes y el problema de no estacionalidad que CTDE está diseñado para resolver.
- [Zhang, Yang & Başar (2021). Multi-Agent Reinforcement Learning: A Selective Overview](https://arxiv.org/abs/1911.10635) encuesta que abarca las LMA cooperativas, competitivas y mixtas con resultados de convergencia.
