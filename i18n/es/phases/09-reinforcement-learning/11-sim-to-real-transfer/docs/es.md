# Transporte de Sim a Real                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        

> Una política entrenada en un simulador que falla en el hardware es una política que memorizó el simulador.

> **【中文解读】**Si no puede trabajar en hardware real, explica que se "ha adaptado" a un dispositivo de imitación.

**Type:** Learn | **类型:** 学习
**Languages:** Python | **语言:** Python
**Prerequisites:** Phase 9 · 08 (PPO), Phase 2 · 10 (Bias/Variance) | **前置知识:** Phase 9 · 08 (PPO), Phase 2 · 10 (偏差/方差)
**Time:** ~45 minutes | **时间:** ~45 分钟

## El problema es la introducción del problema

El entrenamiento de un robot real es lento, peligroso y costoso. Un bipé tarda millones de episodios de entrenamiento en aprender a caminar; un bipé real que cae incluso una vez que rompe el hardware. La simulación le da reinicios ilimitados, reproducibilidad determinista, entornos paralelos y ningún daño físico.

> trenamiento real robots es lento, peligroso y caro. Un robot de dos patas necesita millones de entrenamientos para aprender a caminar. Un robot de dos patas real incluso si cae una vez puede dañar los equipos.

Los simuladores están equivocados. Los rodamientos tienen más fricción que los modelos MuJoCo. Las cámaras tienen distorsión de lente que el simulador no incluye. Los motores tienen retrasos, reacción negativa y saturación que el 99% de los modelos de sim omiten.**reality gap** La diferencia sistemática entre la distribución sim y la distribución real  es el problema central de la RL desplegada para la robótica.

> Pero los simuladores son errados. Los modelos de MuJoCo tienen más fricción que los modelos de MuJoCo. Los simuladores de los motores tienen retraso, intervalos y flujos. El 99% de los simuladores de los modelos de los motores saltan estos.**现实鸿沟**La diferencia sistémica entre la distribución real y la distribución real es el problema central de la RL de la implementación de los robots.

Necesitas una política que sea *robusta para el cambio de distribución sim-real*. Tres enfoques históricos: aleatorizar el simulador (randomizar el dominio), adaptar la política con un poco de datos reales (adaptación / ajuste fino del dominio), o identificar los parámetros del sistema real y combinarlos (identificación del sistema). En 2026 la receta dominante combina las tres con una simulación paralela masiva (Isaac Sim, Isaac Lab, Mujoco MJX en GPU).

> Usted necesita una estrategia para la simulación de la distribución real de la distribución de la distribución real de la distribución real de la distribución real de la distribución real de la distribución real de la distribución real de la distribución real de la distribución real de la distribución real de la distribución real de la distribución real de la distribución real de la distribución real de la distribución real de la distribución real de la distribución real de la distribución real de la distribución real de la distribución real de la distribución real de la distribución real de la distribución real de la distribución real de la distribución real de la distribución real de la distribución real de la distribución real de la distribución real de la distribución real de la distribución real de la distribución real de la distribución real de la distribución real de la distribución real de la distribución real de la distribución real de la distribución real de la distribución real de la distribución real de la distribución de la distribución real de la distribución real de la distribución de la distribución real de la distribución de la distribución real de la distribución de la distribución de la distribución de la distribución de la distribución de la información.

> **【中文解读】**"现实沟" es el problema central de la RL de los ordenadores. Tres grandes soluciones: 1) 域随机化在训练时随机化仿真参数让策略更鲁棒; 2) 域自适应使用少量真实数据微调; 3) 系统识别测量真实参数修改仿真机── 2026 principales soluciones son la combinación de tres personas+ GPU de gran escala y hacerse imitar.

> **【拓展：域随机化→大模型泛化】**La idea de la distribución de la formación de dominio en el LLM también se basa en la "disposición de datos" para mejorar la generalización de la capacidad de la formación de estudiantes.

## El concepto central.

![Three sim-to-real regimes: domain randomization, adaptation, system identification](../assets/sim-to-real.svg)

**Domain Randomization (DR).**Tobin y otros. 2017, Peng y otros. En el 2018. Durante el entrenamiento, aleatoriza todos los parámetros de simulación que puedan diferir en el robot real: masas, coeficientes de fricción, ganancias de PD del motor, ruido del sensor, posición de la cámara, iluminación, texturas, modelos de contacto. La política aprende una distribución condicional sobre "en qué sim se encuentra hoy" y generaliza en todo el período. Si el robot real cae dentro del paquete de entrenamiento, la política funciona.

> **域随机化（DR）。**Durante el entrenamiento, cada simulación puede ser diferente a la de un robot real: el tamaño, el número de fricciones, el aumento de los efectos de los motores, el ruido de los sensores, la posición de los fotores, las luces, las texturas, los modelos de contacto.

- **Upside:**No se necesitan datos reales. Una receta, muchos robots.
  **优点：**No necesita datos reales.
- **Downside:**El programa de formación sobre aleatorización produce una política "universal" pero demasiado cautelosa.
  **缺点：** Exceso de formación de casualidad genera una estrategia "general" pero demasiado conservadora―  Demasiado ruido≈ Demasiado normalización―

**System Identification (SI).**Si puedes medir la fricción entre los brazos y las articulaciones del robot real, conecta eso al simulador. Luego entrenar una política que espera esos valores. Necesita acceso al sistema real pero reduce directamente la brecha de realidad.

> **系统辨识（SI）。**訓練前將仿真器参数拟合到真世界数据──需要接触真实系统但直接缩小现实沟──

**Domain Adaptation.**Entrenamiento en sim, ajuste fino con una pequeña cantidad de datos reales.

> **域自适应。**En el simulacro, se usan dos variantes:

- **Real2Sim2Real:**Aprender un simulador residual `f(s, a, z) - f_sim(s, a)`usando implementaciones reales, entrenar en el simulador corregido.
  **Real2Sim2Real：**Con un verdadero despliegue, aprender a hacer las imitaciones, en el proceso de imitación de las modificaciones posteriores.
- **Observation adaptation:**entrenar una política que mapea los obsos reales → sim-like obs a través de un extractor de características aprendido (por ejemplo, GAN píxel a píxel).
  **观测自适应：**訓練將真實觀測映射为仿真式觀測的策略──

**Privileged learning / teacher-student.**Miki et al. 2022 (ANYmal quadruped). Entrenar a un *enseñador* en la simulación que tiene acceso a información privilegiada (frito de la verdad del suelo, altura del terreno, deriva IMU). Distilla a un *estudiante* que sólo ve observaciones de sensores reales. El estudiante aprende a inferir características privilegiadas de la historia, sólidas a través de parámetros físicos.

> **特权学习/教师-学生。**En la simulación en el entrenamiento tienen derecho a acceder a la información privilegiada de los profesores.

**Massively parallel simulation.**20242026. Isaac Lab, Mujoco MJX, Brax ejecutan miles de robots paralelos en una sola GPU. PPO con 4.096 humanoides paralelos recopila años de experiencia en horas. La "brecha de realidad" se reduce a medida que la distribución del entrenamiento se amplía; DR se vuelve casi libre cuando cada uno de esos 4.096 envs tiene diferentes parámetros aleatorios.

> **大规模并行仿真。**2024-2026 años。Isaac Lab、Mujoco MJX、Brax en una sola GPU para operar miles de paralelos de máquinas。PPO                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            

**The real-world 2026 recipe (quadruped walking example):**

1. Simulación masiva paralela con gravedad aleatoria de dominio, fricción, ganancias motoras, carga útil.
2. Política de maestros capacitados con información privilegiada (mapa de terreno, velocidad del cuerpo, verdad del suelo).
3. Política de estudiantes destilada del profesor utilizando sólo la propriocepción (códigos de articulaciones de piernas).
4. Adaptación opcional de observación mediante autoencoder en una UMI real.
5. Despliegue, disparar cero en 10 ambientes, si falla, haga minutos de ajuste real con PPO restringido por seguridad.

> **真实世界 2026 年方案（四足行走示例）：**La aplicación de la aplicación de la aplicación de la aplicación de la aplicación de la aplicación de la aplicación de la aplicación de la aplicación de la aplicación de la aplicación de la aplicación de la aplicación de la aplicación de la aplicación de la aplicación de la aplicación de la aplicación de la aplicación de la aplicación de la aplicación de la aplicación de la aplicación de la aplicación de la aplicación de la aplicación de la aplicación de la aplicación de la aplicación de la aplicación de la aplicación de la aplicación de la aplicación de la aplicación de la aplicación de la aplicación de la aplicación de la aplicación de la aplicación de la aplicación de la aplicación de la aplicación de la aplicación de la aplicación de la aplicación de la aplicación de la aplicación de la aplicación de la aplicación de la aplicación de la aplicación de la aplicación de la aplicación de la aplicación de la aplicación de la aplicación de la aplicación de la aplicación de la aplicación de la aplicación de la aplicación de la aplicación de la aplicación de la aplicación de la aplicación de la aplicación de la aplicación de la aplicación de la aplicación de la aplicación de la aplicación de la aplicación de la aplicación de la aplicación de la aplicación de la aplicación de la aplicación de la aplicación de la aplicación de la aplicación de la aplicación de la aplicación de la aplicación de la aplicación de la aplicación de la aplicación de la aplicación de la aplicación de la aplicación de la aplicación de la aplicación de la aplicación de la aplicación de la aplicación de la aplicación de la aplicación de la aplicación de la aplicación de la aplicación de la aplicación de la aplicación de la aplicación de la aplicación de la aplicación de la aplicación de la aplicación de la aplicación de la aplicación de la aplicación de la aplicación de la aplicación de la aplicación de la aplicación de la aplicación de la aplicación de la aplicación de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de 30 de 30 de 30 de julio de julio de julio de julio de julio de julio de de de de de de de de de de de de de de de de de de de de de de de de de de de de julio de de de de de de julio de de de de de de julio de de de de de de de de de de de de de de de de de de de de de de de de de de de de de de de de de de de de de de de de de de de de de de de de de de de de de de de de de de de de de de de de de de de de de de de de de de de

## Construye y realiza.
```figure
f3-reality-gap
```

## Construye el mismo

El código de esta lección es una pequeña demostración de la aleatorización de dominios en un GridWorld con transiciones *ruidosas*.

> El código de esta clase es una pequeña demostración de la randomization de la región de GridWorld con un ruido transferido.

### Paso 1: Sim parámetrizado

```python
def step(state, action, slip):
    if rng.random() < slip:
        action = random_perpendicular(action)
    ...
```

`slip`En la robótica real podría ser fricción, masa, ganancia motora cualquier cosa que se desplace entre sim y real.

> `slip`Es el parámetro de exposición de los simuladores. En los simuladores reales puede ser el fricción, la calidad, el aumento de la potencia.

### Paso 2: entrenar con DR

Al comienzo de cada episodio, muestra `slip ~ Uniform[0.0, 0.4]`Entrenar PPO / Q-learning / cualquier cosa.

> Cada vuelta comienza, por ejemplo.`slip ~ Uniform[0.0, 0.4]` Entrenamiento PPO/Q-learning/ cualquier algoritmo

### Paso 3: evaluar el tiro cero en los boletines "reales"

Evaluar el `slip ∈ {0.0, 0.1, 0.2, 0.3, 0.5, 0.7}`. Los cuatro primeros están en el marco de la formación; `0.5`y `0.7`La política de formación en DR debe mantenerse casi óptima dentro del soporte y degradarse con gracia fuera.

> En el`slip ∈ {0.0, 0.1, 0.2, 0.3, 0.5, 0.7}`上评估──前四在训练支内;`0.5`Y `0.7`En el exterior, la estrategia de entrenamiento de la RD debe mantenerse cerca de la máxima calidad dentro de la rama, en el exterior, la de la reducción de la calidad.

### Paso 4: compara con el entrenamiento estrecho

Formar una segunda política con `slip = 0.0`Sólo. Evaluar en el mismo.`slip`Deberías ver una caída catastrófica tan pronto como el deslizamiento real > 0.

> ¿ Qué ?`slip = 0.0` entrenar la segunda estrategia― evaluar en el mismo rango de desplazamiento― evaluar cuando el rango de desplazamiento real > 0 时应看到灾难性下降―

## Las trampas

- **Too much randomization.**El tren en marcha .`slip ∈ [0, 0.9]`Y su política es tan ajeno al riesgo que nunca intenta el camino óptimo.
  **过度随机化。**En el`slip ∈ [0, 0.9]`La estrategia es demasiado regular y no se trata de la mejor manera de lograr la distribución del mundo real.
- **Too little randomization.**Entrenamiento en una pequeña rebanada y la política no puede generalizar en absoluto. Utilice un currículo adaptativo (Randomization Automatic Domain) que amplía la distribución a medida que la política mejora.
  **过少随机化。**En el entrenamiento en la sección de la capacitación, la estrategia es totalmente impensable.
- **Misidentified parameter space.**Al aleatorizar la cosa equivocada (tín de cámara cuando la diferencia real es el retraso motor) y DR no ayuda.
  **错误识别参数空间。**随机化错误的东西,DR 无效――先分析真实机器人――
- **Privileged info leakage.**Un profesor que utiliza el estado global para acciones, no sólo observaciones, puede producir un estudiante que no puede ponerse al día.
  **特权信息泄漏。**El profesor que hace movimientos en el estado de la organización puede producir estudiantes que no pueden alcanzar.
- **Sim-to-sim transfer failure.**Si su política no es robusta para una variante de sim más difícil, tampoco será robusta para el mundo real.
  **仿真到仿真迁移失败。**Si la estrategia para hacer más difícil las simulaciones no es fácil, para el mundo real tampoco será fácil.
- **No real-world safety envelope.**Una política que funciona en simulación y "funciona en realidad" sin un escudo de seguridad de bajo nivel puede romper el hardware.
  **无真实世界安全包络。** sin estrategias de protección de seguridad de bajo nivel todavía puede dañar el hardware― en controladores no aprendices                                                                                                                                                                                                                                                  

## Usalo con el marco de ejecución

La pila de simulación real de 2026:

> 2026 años de la verdad a la verdad:

| Domain | Stack |
|--------|-------|
| Domain / 领域 | Stack / 技术栈 |
| Legged locomotion (ANYmal, Spot, humanoid) / 腿式运动 | Isaac Lab + DR + privileged teacher / student |
| Manipulation (dexterous hands, pick-and-place) / 操作 | Isaac Lab + DR + DR-GAN for vision |
| Autonomous driving / 自动驾驶 | CARLA / NVIDIA DRIVE Sim + DR + real fine-tune |
| Drone racing / 无人机竞速 | RotorS / Flightmare + DR + online adaptation |
| Finger/in-hand manipulation / 手指/手内操作 | OpenAI Dactyl (DR at unprecedented scale) |
| Industrial arms / 工业机械臂 | MuJoCo-Warp + SI + small real fine-tune |

Para el control en todas las escalas, el flujo de trabajo es consistente: ajusta el simulador lo mejor que puedas, aleatoriza lo que no puedes ajustar, entrena enormes políticas, destila, despliega con un escudo de seguridad.

> Para todo el control, el flujo de trabajo: todo lo posible para adaptarse a la realidad, todo lo imposible para adaptarse a la realidad, entrenar estrategias enormes,

## Envíe el producto .

Salvo como`outputs/skill-sim2real-planner.md`¿Qué es esto ?

```markdown
---
name: sim2real-planner
description: Plan a sim-to-real transfer pipeline for a given robot + task, covering DR, SI, and safety.
version: 1.0.0
phase: 9
lesson: 11
tags: [rl, sim2real, robotics, domain-randomization]
---

Given a robot platform, a task, and access to real hardware time, output:

1. Reality gap inventory. Suspected sources ranked by expected impact (contact, sensing, actuation delay, vision).
2. DR parameters. Exact list, ranges, distribution. Justify each range against real measurements.
3. SI steps. Which parameters to measure; measurement method.
4. Teacher/student split. What privileged info the teacher uses; what obs the student uses.
5. Safety envelope. Low-level limits, emergency stops, backup controller.

Refuse to deploy without (a) a zero-shot sim-variant test, (b) a safety shield, (c) a rollback plan. Flag any DR range wider than 3× measured real variability as likely over-randomized.
```

## Los ejercicios.

1. **Easy.**Entrenar a un agente de aprendizaje Q en el GridWorld de deslizamiento fijo (slip=0.0). Evalúa en deslizamiento ∈ {0.0, 0.1, 0.3, 0.5}.
2. **Medium.**Entrenar un agente de aprendizaje DR Q muestreo `slip ~ Uniform[0, 0.3]`¿Cuánto compra DR a un slip=0.5 (fuera de distribución)?
3. **Hard.**Implementar un plan de estudios: empezar con slip=0.0, ampliar el rango de DR cada vez que la política alcanza el 90% de la óptima. Medir los pasos totales del entorno para alcanzar slip=0.3 de tiro cero frente a un baseline de DR fijo.

## Términos clave .

| Term | What people say | What it actually means |
|------|-----------------|-----------------------|
| Reality gap | "Sim-to-real difference" / 现实鸿沟 | Distribution shift between training and deployment physics/sensing. |
| Domain randomization (DR) | "Train across random sims" / 域随机化 | Randomize sim parameters during training so policy generalizes. |
| System identification (SI) | "Measure real and fit sim" / 系统辨识 | Estimate real physical parameters; set sim to match. |
| Domain adaptation | "Fine-tune on real data" / 域自适应 | Small real-world fine-tune after sim training; may adapt obs or dynamics. |
| Privileged info | "Ground truth for teacher" / 特权信息 | Information only the sim has; student must infer it from obs history. |
| Teacher/student | "Distill privileged -> observable" / 教师-学生蒸馏 | Teacher trained with shortcuts; student learns to mimic without them. |
| ADR | "Automatic Domain Randomization" / 自动域随机化 | Curriculum that widens DR ranges as the policy improves. |
| Real2Sim | "Close the gap with real data" / 现实到仿真 | Learn a residual to make the sim mimic real rollouts. |

## Más Leer más Leer más

- [Tobin et al. (2017). Domain Randomization for Transferring Deep Neural Networks from Simulation to the Real World](https://arxiv.org/abs/1703.06907) el documento original de DR (visión para la robótica).
- [Peng et al. (2018). Sim-to-Real Transfer of Robotic Control with Dynamics Randomization](https://arxiv.org/abs/1710.06537) DR para la dinámica, la locomoción cuadruplicada.
- [OpenAI et al. (2019). Solving Rubik's Cube with a Robot Hand](https://arxiv.org/abs/1910.07113) Dactyl, ADR en escala.
- [Miki et al. (2022). Learning robust perceptive locomotion for quadrupedal robots in the wild](https://www.science.org/doi/10.1126/scirobotics.abk2822) Maestro-alumno para ANYmal.
- [Makoviychuk et al. (2021). Isaac Gym: High Performance GPU Based Physics Simulation for Robot Learning](https://arxiv.org/abs/2108.10470) el simulador masivo paralelo que impulsa los despliegues 2025-2026.
- [Akkaya et al. (2019). Automatic Domain Randomization](https://arxiv.org/abs/1910.07113) Método de programación de estudios de ADR.
- [Sutton & Barto (2018). Ch. 8 — Planning and Learning with Tabular Methods](http://incompleteideas.net/book/RLbook2020.pdf) el marco Dyna (utilizar un modelo para la planificación + implementaciones) que sustenta las modernas tuberías sim-to-real.
- [Zhao, Queralta & Westerlund (2020). Sim-to-Real Transfer in Deep Reinforcement Learning for Robotics: a Survey](https://arxiv.org/abs/2009.13303) taxonomía de los métodos sim-to-real con resultados de referencia.
