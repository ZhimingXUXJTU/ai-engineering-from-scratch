# RL para juegos  AlphaZero, MuZero, y la era del LLM-Razonamiento  游戏中的强化学习  AlphaZero、 MuZero y LLM 推理时代

> 1992: TD-Gammon venció a los campeones humanos en backgammon con TD puro. 2016: AlphaGo venció a Lee Sedol. 2017: AlphaZero dominó el ajedrez, shogi y Go desde cero. 2024: DeepSeek-R1 demostró la misma receta, con GRPO reemplazando a PPO, trabaja en el razonamiento.

> **【中文解读】**游戏是 RL 突破的试验场:TD-Gammon (1992) → AlphaGo (2016) → AlphaZero (2017) → DeepSeek-R1 (2025)。DeepSeek-R1 证明了 AlphaZero's"self-blowing+search+strategy improvement" cycle can be directly used for large model's mathematical reasoningtoken 就是动作,验证器就是"赢/输"信号──

**Type:** Build | **类型:** 动手
**Languages:** Python | **语言:** Python
**Prerequisites:** Phase 9 · 05 (DQN), Phase 9 · 08 (PPO), Phase 9 · 09 (RLHF), Phase 9 · 10 (MARL) | **前置知识:** Phase 9 · 05 (DQN), Phase 9 · 08 (PPO), Phase 9 · 09 (RLHF), Phase 9 · 10 (多智能体 RL)
**Time:** ~120 minutes | **时间:** ~120 分钟

## El problema es la introducción del problema

Los juegos tienen todo lo que RL quiere. recompensa limpia (ganas/perdidas). episodios infinitos (reiniciados de autojuego). Simulación perfecta (el juego *es* el simulador). Espacios de acción discretos o pequeños y continuos. estructura multi-agente que fuerza la robustez adversaria.

> 游戏拥有RL所需的一切──清晰的奖励(赢/输)──无限回合(自我博重置)──完美仿真(游戏*就是*仿真器)──离散或小型连续动作空间──迫使对抗鲁棒性的多智能体结构──

Y los juegos son la forma en que cada gran avance de RL fue probado. TD-Gammon (backgammon, 1992). El objetivo de la investigación es mejorar la calidad de la información y la calidad de la información. El objetivo de la investigación es mejorar la calidad de la información. El objetivo de la investigación es mejorar la calidad de la información. OpenAI Five (Dota 2, 2019). AlphaStar (StarCraft II, 2019). MuZero (modelo aprendido, 2019). AlfaTensor (multiplicación de matriz, 2022). AlphaDev (algoritmos de clasificación, 2023). DeepSeek-R1 (razón matemático, 2025)  la última demostración de que las técnicas de juego-RL funcionan en texto.

> 游戏是每个 RL 重大突破的试验场。TD-Gammon(西洋双陆棋,1992)、Atari-DQN(2013)、AlphaGo(2016)、AlphaZero(2017)、OpenAI Five(Dota 2,2019)、AlphaStar(星际争 II,2019)、MuZero(学习模型,2019)、AlphaTensor(矩阵乘法,2022)、AlphaDev(排序算法,2023)、DeepSeek-R1(数学推理,2025)最新证据:游戏RL 技术可用于文本──

Esta piedra angular examina las tres arquitecturas emblemáticas  AlphaZero, MuZero y GRPO  a través de un solo objetivo unificador: **self-play + search + policy improvement**Cada uno generaliza lo anterior; GRPO en particular es la receta de AlphaZero aplicada al razonamiento de LLM, con tokens como acciones y verificación matemática como señal de victoria.

> Esto se termina por un solo punto de vista**自我博弈+搜索+策略改进**审视三个里程碑架构:AlphaZero、MuZero 和 GRPO── cada uno es el anterior de la promoción; GRPO 特别是将 AlphaZero配方应用于 LLM 推理,代币是动作,数学验证是胜信号──

## El concepto central.

![AlphaZero ↔ MuZero ↔ GRPO: same loop, different environments](../assets/rl-games.svg)

**The unifying loop.**

```
while True:
    trajectory = self_play(current_policy, search)     # play game against self
    policy_target = search.improved_policy(trajectory) # search improves raw policy
    policy_net.update(policy_target, value_target)     # supervised on search output
```

**AlphaZero (2017).**Silver et al. Dado un juego (ajedrez, shogi, Go) con reglas conocidas:

- Red de valor político: una torre `f_θ(s) → (p, v)`- ¿ Qué ?`p`Es un precursor de los movimientos legales.`v`es el resultado esperado del juego.
- Buscar árboles de Monte Carlo (MCTS): con cada movimiento, expanda un árbol de posibles continuas.`(p, v)`Seleccione los nodos por UCB (PUCT): `a* = argmax Q(s, a) + c · p(a|s) · √N(s) / (1 + N(s, a))`¿ Qué ?
- Juego de persona: juego de agente contra agente.`t`, la distribución de las visitas del MCTS `π_t`La formación política se convierte en el objetivo.
- Perdida:`L = (v - z)² - π · log p + c · ||θ||²`- ¿ Qué ?`z`es el resultado del juego (+1 / 0 / -1).

Cero conocimiento humano, cero heurísticas hechas a mano, una sola receta que dominaba el ajedrez, el shogi y el go después de unas decenas de millones de juegos de autojuego cada uno.

> 零人类知识――零手工启发式―― una fórmula que después de miles de millones de auto-logos se hizo familiar con el International Chess, el ejemplar y el béisbol―

**MuZero (2019).**Schrittwieser et al. Elimina el requisito de que las reglas sean conocidas.

- En lugar de un entorno fijo, aprenda un modelo de dinámica latente.`(h, g, f)`¿Qué es esto ?
  - `h(s)`: codificar la observación en estado latente.
  - `g(s_latent, a)`: predecir el próximo estado latente + recompensa.
  - `f(s_latent)`El valor de la política previo + valor.
- El MCTS se ejecuta en el *espacio latente aprendido*.
- Funciona en Go, ajedrez, shogi y Atari un algoritmo, sin conocimiento de reglas.

> En el juego de cartas, el juego de cartas, el juego de cartas y el juego de cartas, el juego de cartas y el juego de cartas, el juego de cartas y el juego de cartas, el juego de cartas y el juego de cartas, el juego de cartas y el juego de cartas, el juego de cartas y el juego de cartas, el juego de cartas y el juego de cartas, el juego de cartas y el juego de cartas, el juego de cartas y el juego de cartas, el juego de cartas y el juego de cartas, el juego de cartas y el juego de cartas, el juego de cartas y el juego de cartas, el juego de cartas y el juego de cartas, el juego de cartas y el juego de cartas, el juego de cartas y el juego de cartas, el juego de cartas y el juego de cartas, el juego de cartas y el juego de cartas, el juego de cartas y el juego de cartas, el juego de cartas y el juego de cartas, el juego de cartas y el juego de cartas, el juego de las cartas y el juego de cartas, el juego de las cartas, el juego de las cartas y el juego de cartas, el juego de las cartas y el juego de cartas, el juego de las cartas, el juego de las cartas y el juego de las cartas, el juego de las cartas, el juego de las cartas, el juego de las cartas y el juego de las cartas, el juego de las cartas, el juego de la cual todos los demás.

> **【中文解读】**AlphaZero y MuZero: AutoBlog+ Search+ Strategy Improvement: MCTS  Search Improvement Strategy → 监督学习更新网络──AlphaZero 需要已知游戏规则,MuZero 通过学习隐空间动力学模型消除了这个限制──这个"autoBlog+搜索+策略改进"循环直接启动了DeepSeek-R1的推理训练使用可验证奖励替代游戏胜负信号──

> **【拓展：DeepSeek-R1 与 AlphaZero 范式】**DeepSeek-R1(2025) aplicará el paradigma de AlphaZero a la LLM 推理:token就是动作,推理过程就是"游戏",验证器(数学题对错、代码是否通过测试)就是"胜负信号"──GRPO 替代PPO,组内采样替代自我博──

**Stochastic MuZero (2022).**Agrega dinámicas estocásticas y nodos de azar; se extiende a juegos de clase de backgammon.

> **随机 MuZero (2022)。**添加随机动力学和机会节点; expansión a juego de azar y azar.

**Muesli, Gumbel MuZero (2022-2024).**Mejora de la eficiencia de la muestra y de la búsqueda determinista.

> **Muesli、Gumbel MuZero (2022-2024)。** Mejorar la eficiencia y la determinación de la búsqueda de muestras.

**GRPO (2024-2025).**La misma bucle en forma de AlphaZero, aplicada al razonamiento del modelo de lenguaje:

- "Juego": responder a un problema de matemáticas / codificación / razonamiento. "Gan" = verificador (pasos de prueba, coincidencias numéricas de respuesta) devuelve 1.
- Política: el LLM. Acciones: tokens. Estado: rápido + respuesta-hasta ahora.
- No hay crítico (V_φ estilo PPO).`G`El precio de la póliza es el precio de la póliza.**group-relative advantage** `A_i = (r_i - mean_r) / std_r`como señal para la actualización de tipo REINFORCE.
- KL penalización a la política de referencia para evitar la deriva (como RLHF).
- Perdida total:

  `L_GRPO(θ) = -E_{q, {o_i}} [ (1/G) Σ_i A_i · log π_θ(o_i | q) ] + β · KL(π_θ || π_ref)`

No hay modelo de recompensa, no hay crítico, no hay MCTS. La línea de base relativa al grupo reemplaza a las tres.

> **GRPO (2024-2025)。**DeepSeek-R1 配方── igual AlphaZero 形状循环, aplicado en modelos de lenguaje 推理:不需要奖励模型、Critic 或 MCTS──组相对基线替代了三者──在推理基准上匹配或超越 PPO-RLHF 质量,计算量仅为一小部分──

> **【中文解读】**GRPO es la innovación central de DeepSeek-R1: no necesita crítico 网络(provincia mitad内存), utiliza el valor medio dentro del grupo y el estándar de diferencia de construcción de ventajas. G 个回答, correct answer的优势为正正的 (增强概率), err err err err err err err的 (负的) 降低概率 (降低概率) ⋅ es "no hay crítico PPO", es el algoritmo más importante del entrenamiento de la raciocínio de grandes modelos de 2025 ⋅

> **【拓展：GRPO→DeepSeek-R1→开源推理革命】**El proceso de entrenamiento de cuatro fases de DeepSeek-R1: frío inicio de SFT → 推理导向 GRPO → 拒采样+SFT → 全谱 GRPO──R1-Zero(puro GRPO 无 SFT) demostró que el LLM puede hacerse desde la teoría de la ciencia, pero con un rendimiento de diferencia de lectura── la experiencia de la burbuja muestra que el método de cálculo de un profesor de RL fuerte es mejor para hacer SFT, que un modelo pequeño para hacer RL 效果更好──

**The R1 recipe in full.**DeepSeek-R1 (DeepSeek 2025) es dos modelos en un documento:

> **R1 完整配方。**DeepSeek-R1 es uno de los dos modelos del artículo:

- **R1-Zero.**Comience con el modelo base DeepSeek-V3. No hay SFT. Aplique GRPO directamente con dos componentes de recompensa: * recompensa de precisión* (basado en reglas  ¿ha analizado la respuesta final al número correcto / el código ha aprobado las pruebas de unidad) y * recompensa de formato* (ha completado su cadena de pensamiento en `<think>…</think>`En el caso de los modelos de la imagen, el modelo de la imagen de la imagen de la imagen de la imagen de la imagen de la imagen de la imagen de la imagen de la imagen de la imagen de la imagen de la imagen de la imagen de la imagen de la imagen de la imagen de la imagen de la imagen de la imagen de la imagen de la imagen de la imagen de la imagen de la imagen de la imagen de la imagen de la imagen de la imagen de la imagen de la imagen de la imagen de la imagen de la imagen de la imagen de la imagen de la imagen de la imagen de la imagen de la imagen de la imagen de la imagen de la imagen de la imagen de la imagen de la imagen de la imagen de la imagen de la imagen de la imagen de la imagen de la imagen de la imagen de la imagen de la imagen de la imagen de la imagen de la imagen de la imagen de la imagen de la imagen de la imagen de la imagen de la imagen de la imagen de la imagen de la imagen de la imagen de la imagen de la imagen de la imagen de la imagen de la imagen de la imagen de la imagen de la imagen de la imagen de la imagen de la imagen de la imagen de la imagen de la imagen de la imagen de la imagen de la imagen de la imagen de la imagen de la imagen de la imagen de la imagen de la imagen de la imagen de la imagen de la imagen de la imagen de la imagen de la imagen de la imagen de la imagen de la imagen de la imagen de la imagen de la imagen de la imagen de la imagen de la imagen de la imagen de la imagen de la imagen de la imagen de la imagen de la imagen de la imagen de la imagen de la imagen de la imagen de la imagen de la imagen de la imagen de la imagen de la imagen de la imagen de la imagen de la imagen de la imagen de
- **R1.**Solucionar los problemas de legibilidad de R1-Zero con una tubería de cuatro etapas:
  1. **Cold-start SFT.**Recoge unos pocos miles de demostraciones de CoT con formato limpio, supervisa y perfeccionas el modelo base en ellos. Esto da un punto de partida legible.
  2. **Reasoning-oriented GRPO.**Aplicar GRPO con las recompensas de precisión+formato más una recompensa de coherencia de lenguaje para evitar el cambio de código.
  3. **Rejection sampling + SFT round 2.**Muestre trajectorias de razonamiento de ~600K desde el punto de control RL, mantenga solo las que tengan respuestas finales correctas y CoT legible, y combine con ~200K ejemplos de SFT no razonantes (escritura, QA, autoconocimiento).
  4. **Full-spectrum GRPO.**Una ronda de RL más que cubrirá tanto el razonamiento (recompensas basadas en reglas) como la alineación general (recompensas basadas en preferencias de utilidad/inharmonía).

El resultado coincide con el o1 en AIME y MATH-500 en pesos abiertos, y es lo suficientemente pequeño como para destilar. El mismo documento también libera seis modelos densos destilados (Qwen-1.5B a través de Llama-70B) mediante la SFT'ing en rastros de razonamiento de R1  no RL en el estudiante. La destilación de un maestro de RL fuerte siempre supera a RL desde cero en la escala del estudiante.

> 结果在 AIME 和 MATH-500 上匹配 o1,且足够小可以蒸──蒸强 RL El trayecto de la investigación del profesor siempre es superior a la escala del estudiante desde el RL.

**Why GRPO instead of PPO for reasoning.**Tres razones en el artículo de DeepSeekMath (feb 2024): (1) no hay red de valor para entrenar, reduciendo la memoria a la mitad; (2) la línea de base del grupo maneja naturalmente la recompensa de final de trayectoria que producen las tareas de razonamiento; (3) la normalización por instante hace que las ventajas sean comparables en problemas de dificultad muy diferente, lo que el único crítico de PPO no puede.

> **为什么推理用 GRPO 而非 PPO。**Tres razones: 1) 无需训练值网络,内存减半; 2) 组基线自然处理推理任务产生的稀疏回合末奖励; 3) Cada proposición de regeneración hace que el beneficio en la dificultad sea grande entre los problemas entre comparación:

**Search-free vs search-based.**Los juegos se han ramificado:

> **Search-free vs search-based.**

- * Juegos de información perfecta con horizontes largos* (Go, ajedrez): todavía basados en búsquedas.
- * Razón LLM*: aún no hay MCTS en producción; GRPO en implementaciones completas, mejor de N para la computación de inferencias.

## Construye y realiza.
```figure
f3-selfplay-ladder
```

## Construye el mismo

El código en `code/main.py`ejecutar **GRPO in miniature** un bandido con múltiples grupos de muestras. El algoritmo es el mismo que en un LLM; sólo la política y el entorno son más simples. Enseña la *perda* y la *beneficio relativo al grupo*, que es la innovación de 2025.

> `code/main.py`Se ha logrado el código medio**微型 GRPO** un algoritmo con múltiples grupos de ejemplos 博机―― es igual al LLM; simplemente la estrategia y el ambiente son más simples― es un profesor* pérdida* y* grupo en relación a las ventajas*, es la innovación del año 2025―

### Paso 1: un pequeño entorno de verificación

```python
QUESTIONS = [
    {"prompt": "q1", "correct": 3},
    {"prompt": "q2", "correct": 1},
]

def verify(prompt_idx, answer_token):
    return 1.0 if answer_token == QUESTIONS[prompt_idx]["correct"] else 0.0
```

En GRPO real el verificador ejecuta pruebas unitarias o verifica la igualdad matemática.

> Verdaderos GRPO en el laboratorio de pruebas de matemáticas y demás.

### Paso 2: política: softmax sobre K de los tokens de respuesta por solicitud

```python
def policy_probs(theta, p_idx):
    return softmax(theta[p_idx])
```

Es equivalente a la salida final de una LLM condicionada a un prompt.

> Para el LLM, el precio de la salida es de la última capa.

### Paso 3: Muestreo en grupo y ventaja en relación con el grupo

```python
def grpo_step(theta, p_idx, G=8, beta=0.01, lr=0.1, rng=None):
    probs = policy_probs(theta, p_idx)
    samples = [sample(probs, rng) for _ in range(G)]
    rewards = [verify(p_idx, s) for s in samples]
    mean_r = sum(rewards) / G
    std_r = stddev(rewards) + 1e-8
    advs = [(r - mean_r) / std_r for r in rewards]

    for a, A in zip(samples, advs):
        grad = onehot(a) - probs
        for i in range(len(probs)):
            theta[p_idx][i] += lr * A * grad[i]
    # KL penalty: pull theta toward reference
    for i in range(len(probs)):
        theta[p_idx][i] -= beta * (theta[p_idx][i] - reference[p_idx][i])
```

La ventaja en relación con el grupo es el truco de DeepSeek 2024. No se necesita crítico.

> 组相对优势是2024年DeepSeek的技巧──无需批评──"基线"是组平均值,归结使用组标准差──

### Paso 4: comparación con el límite de referencia de REINFORCE (sin valor)

La misma configuración, el mismo cálculo, la REINFORCE simple.

> Igual configuración, igual cálculo, pura REINFORCE.

### Paso 5: Observa la entropía y KL

Los mismos diagnósticos que el RLHF: KL medio para referencia, entropía política, recompensa sobre tiempo. Una vez estabilizadas, se termina el entrenamiento.

> Diagnosis similar a la RLHF: KL promedio a la referencia estrategia, estrategia, recompensa con el tiempo cambia.

## Las trampas

- **Reward hacking via verifier gaming.**GRPO hereda el riesgo de RLHF: si el verificador es erróneo o explotable, la MLL encontrará el exploit.
  **通过验证器博弈的奖励黑客。**GRPO  heredó el riesgo de RLHF: si el verificador está equivocado o utilizable, LLM encontrará la falla.
- **Group size too small.**La variación de la línea de base del grupo es de `1/√G`- Por debajo .`G = 4`, la señal de ventaja es ruidosa; la elección estándar es `G = 8`¿ Qué ?`64`¿ Qué ?
  **组大小太小。**组基线的方差与 `1/√G`Es verdad.`G = 4`Se trata de un ejemplo de la presencia de ruido.`G = 8`¿ Qué ?`64`¿Qué es eso?
- **Length bias.**Las terminaciones de LLM de diferentes longitudes tienen diferentes probabilidades de registro. Normaliza por cuenta de tokens, o usa el log-prob de nivel de secuencia, o truncate a la longitud máxima.
  **长度偏差。**LLM de diferentes dimensiones  finalización con diferentes probabilidades de contracción ⋅ por token ⋅ reducción o recorte a la mayor longitud ⋅
- **Pure self-play cycles.**El entrenamiento al estilo AlphaZero puede quedar atrapado en los bucles de dominio en los juegos de suma general.
  **纯自我博弈循环。**El entrenamiento de AlphaZero puede caer en el ciclo de control de los sistemas de control de las células.
- **Search-policy mismatch.**AlphaZero entrena la política para imitar el resultado de búsqueda. Si la red de políticas es demasiado pequeña para representar la distribución de la búsqueda, la capacitación se detiene.
  **搜索-策略不匹配。**AlphaZero trenamiento estrategia imitación de búsqueda de salida. Si la estrategia de red demasiado pequeño no puede mostrar la distribución de búsqueda, el entrenamiento se detiene.
- **Compute floor.**MuZero / AlphaZero necesita computación masiva. Una sola ablación a menudo es de cientos de horas de GPU. Existen demos en miniatura (por ejemplo, AlphaZero en Connect Four) para el aprendizaje.
  **计算下限。**MuZero/AlphaZero  necesita un gran número de cálculos ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙     ∙ ∙     ∙                                                                                                                                                                                                                                                                                                                                    
- **Verifier coverage.**Las pruebas de unidad que aprueban una solución de error refuerzan el error.
  **验证器覆盖。**通过有bug 解决方案的单元测试会强化 bug;; diseño capaz de capturar la situación marginal de un verificador;;

## Usalo con el marco de ejecución

El panorama del juego-RL 2026 por dominio:

> 2026 年游戏 RL 版图, según el campo:

| Domain | Dominant method |
|--------|-----------------|
| Domain / 领域 | Dominant method / 主导方法 |
| Two-player zero-sum board games (Go, chess, shogi) / 双人零和棋类 | AlphaZero / MuZero / KataGo |
| Imperfect info card games (poker) / 不完全信息纸牌 | CFR + deep learning (DeepStack, Libratus, Pluribus) / CFR + 深度学习 |
| Atari / pixel games / Atari/像素游戏 | Muesli / MuZero / IMPALA-PPO |
| Large multiplayer strategy (Dota, StarCraft) / 大型多人策略 | PPO + self-play + league (OpenAI Five, AlphaStar) |
| LLM math/code reasoning / LLM 数学/代码推理 | GRPO (DeepSeek-R1, Qwen-RL, open replications) |
| LLM alignment / LLM 对齐 | DPO / RLHF-PPO (not GRPO; verifier is preference not verifiable) / DPO/RLHF-PPO |
| Robotics / 机器人 | PPO + DR (not game-RL, but uses same policy-gradient tools) / PPO+DR |
| Combinatorial problems / 组合问题 | AlphaZero variants (AlphaTensor, AlphaDev) / AlphaZero 变体 |

La *recepta*  auto-juego, mejoras aumentadas por búsqueda, destilación de políticas  abarca texto, píxeles y control físico. GRPO es la instancia más joven; más están por venir.

> Esta * forma* auto-exploración  búsqueda de mejoras  estrategia  de control físico 

## Envíe el producto .

Salvo como`outputs/skill-game-rl-designer.md`¿Qué es esto ?

```markdown
---
name: game-rl-designer
description: Design a game-RL or reasoning-RL training pipeline (AlphaZero / MuZero / GRPO) for a given domain.
version: 1.0.0
phase: 9
lesson: 12
tags: [rl, alphazero, muzero, grpo, self-play]
---

Given a target (perfect-info game / imperfect-info / Atari / LLM reasoning / combinatorial), output:

1. Environment fit. Known rules? Markov? Stochastic? Multi-agent? Informs AlphaZero vs MuZero vs GRPO.
2. Search strategy. MCTS (PUCT with learned prior), Gumbel-sampled, best-of-N, or none.
3. Self-play plan. Symmetric self-play / league / offline data / verifier-generated.
4. Target signal. Game outcome / verifier reward / preference / learned model. Include robustness plan.
5. Diagnostics. Win rate vs baseline, ELO curve, verifier pass rate, KL to reference.

Refuse AlphaZero on imperfect-info games (route to CFR). Refuse GRPO without a trusted verifier. Refuse any game-RL pipeline without a fixed baseline opponent set (self-play ELO is uncalibrated otherwise).
```

## Los ejercicios.

1. **Easy.**Implemente el bandido del GRPO en `code/main.py`. Entrenamiento en 2 instrucciones × 4 tokens de respuesta cada uno. Convergen en < 1.000 actualizaciones con `G=8`¿ Qué ?
2. **Medium.**Enchufe PPO (cortado) y vanilla REINFORCE. Compara la eficiencia de la muestra y la variación de la recompensa con GRPO en el mismo bandido.
3. **Hard.**Extensión a una "cadena de razonamiento" de longitud-2: el agente emite dos tokens y el verificador recompensa el par. Medir cómo GRPO maneja la asignación de crédito en dos secuencias de pasos. (Punta: ventaja del grupo de cálculo por *secuencia completa*, propagación a ambas posiciones de tokens.)

## Términos clave .

| Term | What people say | What it actually means |
|------|-----------------|-----------------------|
| MCTS | "Tree search with learned net" / 蒙特卡洛树搜索 | Monte Carlo Tree Search; UCB1/PUCT selection with learned `(p, v)` priors. |
| AlphaZero | "Self-play + MCTS" / AlphaZero | Policy-value net trained to match MCTS visits and game outcome. |
| MuZero | "Learned-model AlphaZero" / MuZero | Same loop but in latent space via learned dynamics. |
| GRPO | "Critic-free PPO" / 组相对策略优化 | Group Relative Policy Optimization; REINFORCE with group-mean baseline + KL. |
| PUCT | "AlphaZero's UCB" / PUCT 选择公式 | `Q + c · p · √N / (1 + N_a)` — balances value estimate with prior. |
| Self-play | "Agent vs past self" / 自我博弈 | Standard for zero-sum; symmetric training signal. |
| League play | "Population-based self-play" / 联盟训练 | Past + current + exploiters sampled as opponents. |
| Verifier reward | "Verifiable RL" / 验证器奖励 | Reward comes from a deterministic checker (tests pass, answer matches). |
| Process reward | "PRM" / 过程奖励模型 | Scores each reasoning step, not just the final answer. |

## Más Leer más Leer más

- [Silver et al. (2017). Mastering the game of Go without human knowledge (AlphaGo Zero)](https://www.nature.com/articles/nature24270)¿ Qué ?
- [Silver et al. (2018). A general reinforcement learning algorithm that masters chess, shogi, and Go through self-play (AlphaZero)](https://www.science.org/doi/10.1126/science.aar6404)¿ Qué ?
- [Schrittwieser et al. (2020). Mastering Atari, Go, chess and shogi by planning with a learned model (MuZero)](https://www.nature.com/articles/s41586-020-03051-4)¿ Qué ?
- [Vinyals et al. (2019). Grandmaster level in StarCraft II (AlphaStar)](https://www.nature.com/articles/s41586-019-1724-z)¿ Qué ?
- [DeepSeek-AI (2024). DeepSeekMath: Pushing the Limits of Mathematical Reasoning in Open Language Models (GRPO)](https://arxiv.org/abs/2402.03300) el documento que introdujo el GRPO y el punto de partida relativo al grupo.
- [DeepSeek-AI (2025). DeepSeek-R1: Incentivizing Reasoning Capability in LLMs via Reinforcement Learning](https://arxiv.org/abs/2501.12948) la receta completa de cuatro etapas R1 más la ablación R1-Zero.
- [Brown et al. (2019). Superhuman AI for multiplayer poker (Pluribus)](https://www.science.org/doi/10.1126/science.aay2400) CFR + aprendizaje profundo a escala.
- [Tesauro (1995). Temporal Difference Learning and TD-Gammon](https://dl.acm.org/doi/10.1145/203330.203343)El periódico que comenzó todo.
- [Hugging Face TRL — GRPOTrainer](https://huggingface.co/docs/trl/main/en/grpo_trainer) la referencia de producción para la aplicación de GRPO con funciones de recompensa personalizadas.
- [Qwen Team (2024). Qwen2.5-Math — GRPO replication](https://github.com/QwenLM/Qwen2.5-Math) replicación abierta de la receta R1 en múltiples escalas.
- [Sutton & Barto (2018). Ch. 17 — Frontiers of Reinforcement Learning](http://incompleteideas.net/book/RLbook2020.pdf) el marco del libro de texto para el juego propio, la búsqueda y la "recompensa diseñada" que R1 proporciona a escala de LLM.
