# Red de Q profundo (DQN)

> 2013: Mnih entrenó una red de aprendizaje Q en píxeles crudos, venció a todos los agentes RL clásicos en siete juegos Atari. 2015: ampliado a 49 juegos, publicado en Nature, desató la era de la RL profunda. DQN es Q-learning más tres trucos que hacen que la aproximación de funciones sea estable.

> **【中文解读】**DQN = Q-learning + Neural Network + Tres habilidades de estabilización (experience re-back, goal network, reward cut) ―2013-2015 años en Atari 游戏击败了所有经典RL 方法,开启了深度RL 时代―.

**Type:** Build | **类型:** 动手
**Languages:** Python | **语言:** Python
**Prerequisites:** Phase 3 · 03 (Backpropagation), Phase 9 · 04 (Q-learning, SARSA) | **前置知识:** Phase 3 · 03 (反向传播), Phase 9 · 04 (Q-learning, SARSA)
**Time:** ~75 minutes | **时间:** ~75 分钟

## El problema es la introducción del problema

El aprendizaje de Q tabulare necesita un valor Q separado para cada par (estado, acción). Una tabla de ajedrez tiene ~1043 estados. Un marco Atari es 210×160×3 = 100,800 características.

> 表格 Q-learning 需要为每一个状态,动作) para un solo almacenamiento un valor Q. En un juego de Equipo de Equipo de Equipo de Equipo de Equipo de Equipo de Equipo de Equipo de Equipo de Equipo de Equipo de Equipo de Equipo de Equipo de Equipo de Equipo de Equipo de Equipo de Equipo de Equipo de Equipo de Equipo de Equipo de Equipo de Equipo de Equipo de Equipo de Equipo de Equipo de Equipo de Equipo de Equipo de Equipo de Equipo de Equipo de Equipo de Equipo de Equipo de Equipo de Equipo de Equipo de Equipo de Equipo de Equipo de Equipo de Equipo de Equipo de Equipo de Equipo de Equipo de Equipo de Equipo de Equipo de Equipo de Equipo de Equipo de Equipo de Equipo de Equipo de Equipo de Equipo de Equipo de Equipo de Equipo de Equipo de Equipo de Equipo de Equipo de Equipo de Equipo de Equipo de Equipo de Equipo de Equipo de Equipo de Equipo de Equipo de Equipo de Equipo de Equipo de Equipo de Equipo de Equipo de Equipo de Equipo de Equipo de Equipo de Equipo de Equipo de Equipo de Equipo de Equipo de Equipo de Equipo de Equipo de Equipo de Equipo de Equipo de Equipo de Equipo de Equipo de Equipo de Equipo de Equipo de Equipo de Equipo de Equipo de Equipo de Equipo de Equipo de Equipo de Equipo de Equipo de Equipo de Equipo de Equipo de Equipo de Equipo de Equipo de Equipo de

La solución es obvia en retrospectiva: reemplazar la tabla Q por una red neuronal.`Q(s, a; θ)`Pero la aproximación de funciones ingenuas con el aprendizaje Q diverge bajo la "triada mortal"  aproximación de funciones + bootstrapping + aprendizaje fuera de la política. Mnih et al. (2013, 2015) identificaron tres trucos de ingeniería que estabilizan el aprendizaje:

> La solución es simple: con la red neuronal.`Q(s, a; θ)`替换 Q 表――但这个"简单"花了几十年――简单的函数近似与Q-learning 在"致命三要素"下会发散函数近似 +自举 + 离策略学习――Mnih 等人(2013、2015) ha definido tres técnicas de ingeniería de aprendizaje estable:

1. **Experience replay**Descorrelar las transiciones.
   **经验回放**打破转移的时间相关性.
2. **Target network**congelará el objetivo de arranque.
   **目标网络**结自举目标──
3. **Reward clipping**normaliza las magnitudes de gradiente.
   **奖励裁剪**归一化梯度级级──

DQN en Atari fue la primera vez que una única arquitectura con un solo conjunto de hiperparámetros resolvió docenas de problemas de control a partir de píxeles crudos. Todo "deep-RL" construido desde DDQN, Rainbow, Dueling, Distribucional, R2D2, Agent57  está apilado en la parte superior de esta base de tres trucos.

> La DQN de Atari es la primera vez que utiliza un único conjunto de estructuras y un único superparámetros para resolver decenas de problemas de control desde el primer plano.

> **【中文解读】**"Tres elementos mortales": función aproximación + auto-elevación + 离策略 → 训练不稳定甚至发散──DQN tres técnicas resuelven este problema: 1) experiencia re-la-breaking time correlativity; 2) 目标网络结自举目标; 3) 奖励裁剪归一化梯度──所有后续深度 RL 算法都建立在这些三个技巧之上──

> **【拓展：经验回放→RLHF】**La idea de la experiencia de repetición de la experiencia está inexistente en el entrenamiento de la LLM: el buffer de la formación de la OPP, los datos preferidos en el RLHF, los datos de la OPP son en esencia "hacer un corte de datos, la conexión de datos, la reutilización de la experiencia".

## El concepto central.

![DQN training loop: env, replay buffer, online net, target net, Bellman TD loss](../assets/dqn.svg)

**The objective.**DQN minimiza la pérdida de TD en un paso en una función Q neuronal:

`L(θ) = E_{(s,a,r,s')~D} [ (r + γ max_{a'} Q(s', a'; θ^-) - Q(s, a; θ))² ]`

`θ`= red en línea, actualizado cada paso por descenso de gradiente. `θ^-`= red objetivo, copiada periódicamente desde `θ`(cada ~ 10.000 pasos). `D`= Buffer de reproducción de las transiciones pasadas.

> **目标。**DQN 损失 损失 损失 损失 损失 损失 损失 损失 损失 损失 损失 损失 损失 损失 损失 损失 损失 损失 损失 损失 损失 损失 损失 损失 损失 损失 损失 损失 损失 损失 损失 损失 损失 损失 损失 损失 损失 损失 损失 损失 损失 损失 损失 损失 损失 损失 损失 损失 损失 损失 损失 损失 损失 损失 损失 损失 损失 损失 损失 损失 损失 损失 损失 损失 损失 损失 损失 损失`θ`= En línea, cada paso a través de la escala baja actualización.`θ^-`= 目标网络, periodicamente desde `θ`复制(约每10,000 步)`D`= 过去转移的回放缓冲区──

**The three tricks, in order of importance:**

> **三个技巧，按重要性排序：**

**Experience replay.**Un amortiguador de anillos de `~10⁶`Cada paso de entrenamiento muestra un minibatch uniformemente al azar. Esto rompe la correlación temporal (los marcos sucesivos son casi idénticos), permite a la red aprender de raras transiciones gratificantes muchas veces y descorrela actualizaciones de gradiente consecutivas.

> **经验回放。**Una zona de aceleración de la formación de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red

**Target network.**Usando la misma red `Q(·; θ)`En ambos lados de la ecuación Bellman hace que el objetivo se mueva cada actualización  "perseguir su propia cola". La solución: mantener una segunda red `Q(·; θ^-)`con pesos congelados.`C`pasos, copia `θ → θ^-`Esto estabiliza el objetivo de regresión para miles de pasos de gradiente a la vez.`θ^- ← τ θ + (1-τ) θ^-`(utilizado en DDPG, SAC) son una variante más suave.

> **目标网络。**En Bellman 方程 ambos lados de la misma red se hace el objetivo de cada actualización está en movimiento " perseguir su propio尾巴".`C`步复制                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                          `θ → θ^-`◊ soft update(DDPG、SAC en uso) es un cambio más suave.

**Reward clipping.**Las magnitudes de la recompensa de Atari varían de 1 a 1000+.`{-1, 0, +1}`No es correcto cuando la magnitud de la recompensa importa, pero bueno para Atari cuando sólo importa la firma.

> **奖励裁剪。**Atari  Grado de premios de 1 a 1000+ no etc. `{-1, 0, +1}` evitar cualquier nivel de control de juego individual

**Double DQN.**Hasselt (2016) corrige el sesgo de maximización: utiliza la red en línea para * seleccionar* la acción, la red objetivo para * evaluarla.

`target = r + γ Q(s', argmax_{a'} Q(s', a'; θ); θ^-)`

El reemplazo de entrega es consistentemente mejor.

> **双重 DQN。**Hasselt (2016) 修复最大化偏差:用在线网络*选择*动作,用目标网络*评估*它──直接替换,始终更好──默认使用──

**Other improvements (Rainbow, 2017):**repetición priorizada (muestra de transiciones de alto TD-error más), arquitectura de duelo (separado `V(s)`El sistema de redes de acceso a Internet (C51/QR-DQN), las redes ruidosas (exploración aprendida), los retornos de n pasos, la distribución de Q (C51/QR-DQN), el arranque de múltiples pasos.

> **其他改进（Rainbow, 2017）：**优先回放、决斗架构、噪声网络、n 步回报、分布式 Q、多步自举── cada mejoría contribuye con varios cientos de puntos;收益大致可叠加──

> **【拓展：Rainbow DQN 与集成改进】**Rainbow DQN(2017) se integrarán 6 tipos de DQN  mejoras juntas: prioridad de experiencia re-lación Dueling 架构、 noise network exploration、n 步回报、 distribuido Q 学习、多步自举── cada tipo de mejoras contribuye a varios cientos de puntos de mejora de rendimiento, el resultado de la combinación es notable── este tipo de "integración de volumen" también se ha manifestado en el entrenamiento de LLM DATA QUALITY、 TRAINING STRATICS、 efectos de mejoras de la estructura son generalmente superpuestos.

## Construye y realiza.
```figure
f3-dqn-stability
```

## Construye el mismo

El código aquí es stdlib-solo numpy-free  usamos un MLP de capa oculta única rodada a mano en un pequeño GridWorld continuo, por lo que cada paso de entrenamiento se ejecuta en microsecondas. El algoritmo es idéntico a Atari DQN en escala.

> El código de este sitio sólo se utiliza en una biblioteca estándar en un micro tipo de continuidad GridWorld. El algoritmo de escritura en mano de una sola capa oculta de MLP es completamente el mismo que el de Atari DQN de gran tamaño.

### Paso 1: Puente de reproducción

```python
class ReplayBuffer:
    def __init__(self, capacity):
        self.buf = []
        self.capacity = capacity
    def push(self, s, a, r, s_next, done):
        if len(self.buf) == self.capacity:
            self.buf.pop(0)
        self.buf.append((s, a, r, s_next, done))
    def sample(self, batch, rng):
        return rng.sample(self.buf, batch)
```

~ 50.000 capacidad para Atari; 5.000 es suficiente para nuestro entorno de juguetes.

> Atari necesita alrededor de 50.000 capacidades; nuestro entorno de juegos 5.000 es suficiente.

### Paso 2: una pequeña red Q (MLP manual)

```python
class QNet:
    def __init__(self, n_in, n_hidden, n_actions, rng):
        self.W1 = [[rng.gauss(0, 0.3) for _ in range(n_in)] for _ in range(n_hidden)]
        self.b1 = [0.0] * n_hidden
        self.W2 = [[rng.gauss(0, 0.3) for _ in range(n_hidden)] for _ in range(n_actions)]
        self.b2 = [0.0] * n_actions
    def forward(self, x):
        h = [max(0.0, sum(w * xi for w, xi in zip(row, x)) + b) for row, b in zip(self.W1, self.b1)]
        q = [sum(w * hi for w, hi in zip(row, h)) + b for row, b in zip(self.W2, self.b2)]
        return q, h
```

Pasado hacia adelante: lineal → ReLU → lineal. Esa es toda la red.

> Antes de la transmisión: 线性 → ReLU → 线性── ése es todo el red──

### Paso 3: actualización del DQN

```python
def train_step(online, target, batch, gamma, lr):
    grads = zeros_like(online)
    for s, a, r, s_next, done in batch:
        q, h = online.forward(s)
        if done:
            y = r
        else:
            q_next, _ = target.forward(s_next)
            y = r + gamma * max(q_next)
        td_error = q[a] - y
        accumulate_grads(grads, online, s, h, a, td_error)
    apply_sgd(online, grads, lr / len(batch))
```

La forma es Q-apprenticio de la lección 04 con dos diferencias: (a) nos retroacomponemos a través de un diferenciable `Q(·; θ)`En lugar de indexar una tabla, (b) los usos objetivo `Q(·; θ^-)`¿ Qué ?

> 形式 y el aprendizaje Q de la lección 04 es similar, pero tiene dos diferencias:`Q(·; θ)`Contrarrelación y no indicación de la información, b) objetivus `Q(·; θ^-)`¿Qué es eso?

### Paso 4: el bucle exterior

Para cada episodio, actúa en un acto de codicia.`Q(·; θ)`, empujar las transiciones en el amortiguador, muestran un minibatch, hacen un paso gradiente, sincronizan periódicamente`θ^- ← θ`El patrón:

```python
for episode in range(N):
    s = env.reset()
    while not done:
        a = epsilon_greedy(online, s, epsilon)
        s_next, r, done = env.step(s, a)
        buffer.push(s, a, r, s_next, done)
        if len(buffer) >= batch:
            train_step(online, target, buffer.sample(batch), gamma, lr)
        if steps % sync_every == 0:
            target = copy(online)
        s = s_next
```

En nuestro pequeño GridWorld con un estado de 16 dimensiones, el agente aprende una política casi óptima en aproximadamente 500 episodios.

> En nuestro uso de 16 dimensiones de un estado de calor en el microtipo GridWorld, el cuerpo inteligente está en unos 500 recolecciones para aprender a acercarse a la estrategia más óptima. En Atari, se expandió a 2 mil millones de dólares y añadió el extractor de características de CNN.

## Las trampas

- **Deadly triad.**La aproximación de la función + fuera de la política + arranque puede divergir. DQN mitigó con red objetivo + repetición; no eliminar ninguno.
  **致命三要素。**函数近似+离策略+自举可能发散──DQN 通过目标网络+回放缓解; don't remove any one──
- **Exploration.**El sistema de detección de la red Q-net se descompone en el primer 10% del entrenamiento.
  **探索。**ε 必须衰减, normalmente de 1.0 a 0.01, cubrir aproximadamente el 10% de la formación previa.
- **Overestimation.** `max`El uso de doble DQN en la producción siempre es de carácter ascendente.
  **过估计。**Para el ruido`max`Se utiliza el doble de DQN en la producción.
- **Reward scale.**Clip o normalizar recompensas; la magnitud del gradiente es proporcional a la magnitud de la recompensa.
  **奖励尺度。** reducción o reducción de la remuneración; grado de graduación en relación con el grado de remuneración
- **Replay buffer coldstart.**No entrenes hasta que el amortiguador tenga unos miles de transiciones.
  **回放缓冲区冷启动。**缓冲区 缓冲区 缓冲区 缓冲区 缓冲区 缓冲区 缓冲区 缓冲区 缓冲区 缓冲区 缓冲区 缓冲区 缓冲区 缓冲区 缓冲区 缓冲区 缓冲区 缓冲区 缓冲区 缓冲区 缓冲区 缓冲区 缓冲区 缓冲区 缓冲区 缓冲区 缓冲区 缓冲区 缓冲区 缓冲区 缓冲区 缓冲区 缓冲区 缓冲区 缓冲区 缓冲区 缓冲 缓冲 缓冲 缓冲 缓冲 缓冲 缓冲 缓冲 缓冲 缓冲 缓冲 缓冲 缓冲 缓冲 缓冲 缓冲 缓冲 缓冲 缓冲 缓冲 缓冲 缓冲 缓冲 缓冲 缓冲 缓冲 缓冲 缓冲 缓冲 缓冲 缓 缓 缓 缓 缓 缓 缓 缓 缓 缓 缓 缓 缓 缓 缓 缓 缓 缓 缓 缓 缓 缓 缓 缓 缓 缓 缓 缓 缓 缓 缓 缓 缓 缓 缓 缓 缓 缓 缓 缓 缓 缓 缓 缓 缓 缓 缓 缓 缓 缓 缓 缓 缓 缓 缓 缓 缓 缓 缓 缓 缓 缓 缓 缓 缓 缓 缓 缓 缓 缓 缓 缓 缓 缓 缓 缓 缓 缓 缓 缓 缓 缓 缓 缓 缓 缓 缓 缓 缓 缓 缓 缓 缓 缓 缓 缓 缓 缓 缓 缓 缓 缓 缓 缓 缓 缓 缓 缓 缓 缓 缓 缓 缓 缓 缓 缓 缓 缓 缓 缓 缓 缓 缓 缓 缓 缓 缓 缓 缓 缓 缓 缓 缓 缓 缓 缓 缓 缓
- **Target sync frequency.**El sistema de control de velocidad de la navegación de Atari utiliza 10.000 pasos env.
  **目标同步频率。**太频繁≈没有目标网络;太不频繁≈过时目标――experience law: 每约1/100 训练视野同步一次――
- **Observation preprocessing.**Atari DQN apila 4 cuadros para hacer estado Markov. Cualquier entorno con información de velocidad necesita estado de cuadros o recurrente.
  **观测预处理。**Atari DQN 堆叠 4 使状态满足马尔可夫性── cualquier ambiente con velocidad de información necesita 堆叠或循环状态──

## Usalo con el marco de ejecución

En 2026, DQN rara vez es de última generación, pero sigue siendo el algoritmo de referencia fuera de la política:

> En 2026 el DQN                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                       

| Task | Method of choice | Why not DQN? |
|------|------------------|--------------|
| Task / 任务 | Method of choice / 首选方法 | Why not DQN? / 为什么不用 DQN？ |
| Discrete-action Atari-like / 离散动作类 Atari | Rainbow DQN or Muesli | Same framework, more tricks. / 相同框架，更多技巧。 |
| Continuous control / 连续控制 | SAC / TD3 (Phase 9 · 07) | DQN has no policy network. / DQN 没有策略网络。 |
| On-policy / high-throughput / 在线策略/高吞吐 | PPO (Phase 9 · 08) | No replay buffer; easier to scale. / 无回放缓冲区；更易扩展。 |
| Offline RL / 离线 RL | CQL / IQL / Decision Transformer | Conservative Q targets, no bootstrapping blowups. / 保守 Q 目标，无自举爆炸。 |
| Large discrete action spaces (recommender) / 大离散动作空间（推荐） | DQN with action embedding, or IMPALA | Fine; decoration matters. / 可行；细节很重要。 |
| LLM RL / LLM RL | PPO / GRPO | Sequence-level, not step-level; different loss. / 序列级而非步级；不同损失。 |

Las lecciones siguen viajando. Replay y redes de destino aparecen en SAC, TD3, DDPG, SAC-X, el amortiguador de auto-juego de AlphaZero y todos los métodos de RL fuera de línea.

> Estas experiencias siguen siendo válidas. La red de repuestos y objetivos se encuentra en SAC, TD3, DDPG, SAC-X, AlphaZero, en su propia zona de amortización y en cada método de RL de salida.

## Envíe el producto .

Salvo como`outputs/skill-dqn-trainer.md`¿Qué es esto ?

```markdown
---
name: dqn-trainer
description: Produce a DQN training config (buffer, target sync, ε schedule, reward clipping) for a discrete-action RL task.
version: 1.0.0
phase: 9
lesson: 5
tags: [rl, dqn, deep-rl]
---

Given a discrete-action environment (observation shape, action count, horizon, reward scale), output:

1. Network. Architecture (MLP / CNN / Transformer), feature dim, depth.
2. Replay buffer. Capacity, minibatch size, warmup size.
3. Target network. Sync strategy (hard every C steps or soft τ).
4. Exploration. ε start / end / schedule length.
5. Loss. Huber vs MSE, gradient clip value, reward clipping rule.
6. Double DQN. On by default unless explicit reason to disable.

Refuse to ship a DQN with no target network, no replay buffer, or ε held at 1. Refuse continuous-action tasks (route to SAC / TD3). Flag any reward range > 10× per-step mean as needing clipping or scale normalization.
```

## Los ejercicios.

1. **Easy.**- ¿ Qué ?`code/main.py`¿Cuántos episodios hasta que la media de ejecución exceda de -10?
2. **Medium.**Deshabilitar la red de destino (utilizar la red en línea para ambos lados del objetivo de Bellman).
3. **Hard.**Añadir DQN doble: utilizar la red en línea para seleccionar `argmax a'`, la red de objetivo para evaluar.`Q(s_0, best_a)`contra verdadero`V*(s_0)`Después de 1.000 episodios con vs sin Double DQN en un grido de recompensas GridWorld.

## Términos clave .

| Term | What people say | What it actually means |
|------|-----------------|-----------------------|
| DQN | "Deep Q-learning" / 深度Q网络 | Q-learning with a neural Q-function, replay buffer, and target network. |
| Experience replay | "Shuffled transitions" / 经验回放 | Ring buffer sampled uniformly each gradient step; decorrelates data. |
| Target network | "Frozen bootstrap" / 目标网络 | Periodic copy of Q used in the Bellman target; stabilizes training. |
| Deadly triad | "Why RL diverges" / 致命三要素 | Function approximation + bootstrapping + off-policy = no convergence guarantee. |
| Double DQN | "Fix for maximization bias" / 双重DQN | Online net selects action, target net evaluates it. |
| Dueling DQN | "V and A heads" / 决斗DQN | Decompose Q = V + A - mean(A); same output, better gradient flow. |
| Rainbow | "All the tricks" / Rainbow | DDQN + PER + dueling + n-step + noisy + distributional in one. |
| PER | "Prioritized Replay" / 优先经验回放 | Sample transitions proportional to TD-error magnitude. |

## Más Leer más Leer más

- [Mnih et al. (2013). Playing Atari with Deep Reinforcement Learning](https://arxiv.org/abs/1312.5602) el trabajo del taller de 2013 de NeurIPS que dio inicio a la RL profunda.
- [Mnih et al. (2015). Human-level control through deep reinforcement learning](https://www.nature.com/articles/nature14236) el artículo Nature, 49 juegos de DQN.
- [Hasselt, Guez, Silver (2016). Deep Reinforcement Learning with Double Q-learning](https://arxiv.org/abs/1509.06461) DDQN.
- [Wang et al. (2016). Dueling Network Architectures](https://arxiv.org/abs/1511.06581) Duelo de DQN.
- [Hessel et al. (2018). Rainbow: Combining Improvements in Deep RL](https://arxiv.org/abs/1710.02298) el papel de trucos apilados.
- [OpenAI Spinning Up — DQN](https://spinningup.openai.com/en/latest/algorithms/dqn.html) Exposición moderna clara.
- [Sutton & Barto (2018). Ch. 9 — On-policy Prediction with Approximation](http://incompleteideas.net/book/RLbook2020.pdf) el tratamiento en libros de texto de la "triada mortal" (aproximado de la función + arranque + fuera de la política) que la red objetivo y el buffer de reproducción de DQN están diseñados para domesticar.
- [CleanRL DQN implementation](https://docs.cleanrl.dev/rl-algorithms/dqn/) DQN de referencia de archivo único utilizado en estudios de ablación; bueno para leer junto con la versión de la lección desde cero.
