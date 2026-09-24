# Política Gradiente  REINFORCE desde cero   estrategia   desde cero realizarREINFORCE

> Dejar de estimar el valor. Parametrizar la política directamente, calcular el gradiente de la rentabilidad esperada, paso hacia arriba. Williams (1992) lo escribió en un teorema. Es por eso que existen PPO, GRPO y cada bucle LLM RL.

> **【中文解读】**La función de reevaluación, estrategia de parametrización directa π_θ(a de la información), calcula la expectativa de reporte de la escala y la escala de aumento.`∇J(θ) = E[G · ∇log π_θ(a|s)]` Esta es la razón por la que existen los ciclos de entrenamiento de PPO, GRPO y todos los grandes modelos de RL.

**Type:** Build | **类型:** 动手
**Languages:** Python | **语言:** Python
**Prerequisites:** Phase 3 · 03 (Backpropagation), Phase 9 · 03 (Monte Carlo), Phase 9 · 04 (TD Learning) | **前置知识:** Phase 3 · 03 (反向传播), Phase 9 · 03 (蒙特卡洛), Phase 9 · 04 (TD 学习)
**Time:** ~75 minutes | **时间:** ~75 分钟

## El problema es la introducción del problema

El aprendizaje Q y DQN paramétrean la función de *valor*.`argmax Q`Se rompe cuando las acciones son continuas (que son`argmax`¿O cuando se quiere una política estocástica (`argmax`es determinista por construcción).

> Q-aprendizaje y DQN 参数化*值*函数──通过 `argmax Q`选择动作── esto no es un problema para el movimiento y el estado de separación── pero cuando el movimiento se mantiene 10 维力矩上取哪个 `argmax`¿) o necesita un estrategia`argmax`Es cierto, ya se ha desmoronado.

Los gradientes de política paramétrean la política en su lugar. `π_θ(a | s)`Es una red neuronal que produce una distribución sobre acciones.`θ`- Un paso hacia arriba.`argmax`No hay recursión de Bellman, sólo ascenso de gradiente en`J(θ) = E_{π_θ}[G]`¿ Qué ?

> 策略梯度改为参数化*策略*`π_θ(a | s)`Es una red de distribución de movimientos de salida de la neurona.`θ`La escalera es de la misma manera que la de la escalera.`argmax`No necesito a Bellman.`J(θ) = E_{π_θ}[G]`La escala de arriba...

El teorema de la REINFORCE (Williams 1992) dice que este gradiente es computable: `∇J(θ) = E_π[ G · ∇_θ log π_θ(a | s) ]`Ejecutar un episodio, calcular el rendimiento, multiplicar por`∇ log π_θ(a | s)`En promedio, en escala, terminado.

> ReINFORCE                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                          `∇J(θ) = E_π[ G · ∇_θ log π_θ(a | s) ]`◊运行一个回合――计算回报―― cada paso multiplicado `∇ log π_θ(a | s)`◊取平均──梯度上升──完成──

Cada algoritmo LLM-RL en 2026  PPO, DPO, GRPO  es un refinamiento de REINFORCE.

> Cada LLM-RL de 2026 算法PPO、DPO、GRPO  son la refinamiento de REINFORCE.

> **【中文解读】** idea central de la gradación estratégica: direct optimización de los parámetros estratégicos θ, hacer que la probabilidad de movimiento de altos retornos aumente `∇log π`Es decir, "la dirección de la estrategia", multiplicado por el reporte G es "la dirección correcta".

> **【拓展：PPO→ChatGPT对齐】**El algoritmo de PPO  entrenamiento de ChatGPT  RLHF  utilizando, en esencia es REINFORCE + crítico 基线 + 信赖域剪──`loss = -advantage * log_prob`Esta línea de código, aparece en casi todos los grandes modelos RL de 2026 años en el guión de entrenamiento.

## El concepto central.

![Policy gradient: softmax policy, log-π gradient, return-weighted update](../assets/policy-gradient.svg)

**The policy gradient theorem.**Para cualquier política`π_θ`parametrizado por `θ`¿Qué es esto ?

`∇J(θ) = E_{τ ~ π_θ}[ Σ_{t=0}^{T} G_t · ∇_θ log π_θ(a_t | s_t) ]`

donde`G_t = Σ_{k=t}^{T} γ^{k-t} r_{k+1}`es el retorno descuento de paso `t`La expectativa está sobre las trayectorias completas .`τ`muestras de `π_θ`¿ Qué ?

> **策略梯度定理。**Para cualquier cosa`θ`                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             `π_θ`, la expectativa de retorno es igual a: el descuento de retorno y la expectativa de retorno multiplicada por la expectativa de la expectativa de retorno de estrategia numérica.`π_θ`采样完整轨迹上取── y también el mismo.

**The proof is short.**Diferenciar`J(θ) = Σ_τ P(τ; θ) G(τ)`El uso de la información`∇P(τ; θ) = P(τ; θ) ∇ log P(τ; θ)`(el truco de la derivación de registro).`log P(τ; θ) = Σ log π_θ(a_t | s_t) + environment terms that do not depend on θ`Los términos de entorno desaparecen. Dos líneas de álgebra te dan el teorema.

> **证明很短。**En espera de que`J(θ)`求导――使用对数导数技巧──将 `log P(τ; θ)`Se ha definido el número de elementos en las dos líneas.

**Variance reduction tricks.**Vanilla ReINFORCE tiene una varianza asesina  los retornos son ruidosos, `∇ log π`es ruidoso, su producto es muy ruidoso. Dos soluciones estándar:

> **方差降低技巧。**El primer reinicio tiene un gran impacto.`∇ log π`Hay ruido, su volumen es mayor.

1. **Baseline subtraction.**Reemplazar`G_t`con`G_t - b(s_t)`para cualquier línea de base `b(s_t)`que no depende de `a_t`No es imparcial porque`E[b(s_t) · ∇ log π(a_t | s_t)] = 0`. Escoge típico: `b(s_t) = V̂(s_t)`Aprendió un crítico → actor-crítico (Lesión 07).
   **基线减法。**¿ Qué ?`G_t - b(s_t)` sustitución `G_t`❖ típico seleccion:`b(s_t) = V̂(s_t)`Por el crítico 学习 → Actor-Crítico (LECCIÓN 07)
2. **Reward-to-go.**Reemplazar`Σ_t G_t · ∇ log π_θ(a_t | s_t)`con`Σ_t G_t^{from t} · ∇ log π_θ(a_t | s_t)`. Sólo los retornos futuros son importantes para una acción dada  Las recompensas pasadas contribuyen con ruido cero-medio.
   **未来回报。** Sólo el retorno futuro a una determinada actividad tiene sentido contribución de la recompensa del pasado  0 promedio de ruido

Combinado, obtienes:

`∇J ≈ (1/N) Σ_{i=1}^{N} Σ_{t=0}^{T_i} [ G_t^{(i)} - V̂(s_t^{(i)}) ] · ∇_θ log π_θ(a_t^{(i)} | s_t^{(i)})`

que es REINFORCE con un valor de referencia  el antepasado directo de A2C (lección 07) y PPO (lección 08).

**Softmax policy parameterization.**Para las acciones discretas, la opción estándar:

`π_θ(a | s) = exp(f_θ(s, a)) / Σ_{a'} exp(f_θ(s, a'))`

donde`f_θ`es cualquier red neuronal que emite un puntaje por acción. El gradiente tiene una forma limpia:

`∇_θ log π_θ(a | s) = ∇_θ f_θ(s, a) - Σ_{a'} π_θ(a' | s) ∇_θ f_θ(s, a')`

Es decir, el puntaje de la acción tomada menos su valor esperado en el marco de la póliza.

> **Softmax 策略参数化。**Para la separación de movimientos, la forma de gradiente es simple: el porcentaje de movimientos realizados se reduce al valor esperado de la estrategia de eliminación.

**Gaussian policy for continuous actions.** `π_θ(a | s) = N(μ_θ(s), σ_θ(s))`- ¿ Qué ?`∇ log N(a; μ, σ)`El proyecto de investigación de la Comisión de Agricultura y Desarrollo de la Agricultura, la Agricultura y la Agricultura tiene un formulario cerrado.

> **连续动作的高斯策略。** `∇ log N(a; μ, σ)`Hay una solución cerrada. Esto es todo lo que se necesita para la Fase 9 · 07 del SAC.

## Construye y realiza.
```figure
policy-gradient-landscape
```

## Construye el mismo

### Paso 1: red de políticas softmax

```python
def policy_logits(theta, state_features):
    return [dot(theta[a], state_features) for a in range(N_ACTIONS)]

def softmax(logits):
    m = max(logits)
    exps = [exp(l - m) for l in logits]
    Z = sum(exps)
    return [e / Z for e in exps]
```

Utilice una política lineal (un vector de peso por acción) para un entorno tabular. Para Atari, intercambiar en una CNN y mantener la cabeza de softmax.

> Cada movimiento tiene un peso de carga.

### Paso 2: muestreo y probabilidad de registro

```python
def sample_action(probs, rng):
    x = rng.random()
    cum = 0
    for a, p in enumerate(probs):
        cum += p
        if x <= cum:
            return a
    return len(probs) - 1

def log_prob(probs, a):
    return log(probs[a] + 1e-12)
```

### Paso 3: despliegue con log-probes capturados

```python
def rollout(theta, env, rng, gamma):
    trajectory = []
    s = env.reset()
    while not done:
        logits = policy_logits(theta, s)
        probs = softmax(logits)
        a = sample_action(probs, rng)
        s_next, r, done = env.step(s, a)
        trajectory.append((s, a, r, probs))
        s = s_next
    return trajectory
```

### Paso 4: actualización de la REINFORCE

```python
def reinforce_step(theta, trajectory, gamma, lr, baseline=0.0):
    returns = compute_returns(trajectory, gamma)
    for (s, a, _, probs), G in zip(trajectory, returns):
        advantage = G - baseline
        grad_log_pi_a = [-p for p in probs]
        grad_log_pi_a[a] += 1.0
        for i in range(N_ACTIONS):
            for j in range(len(s)):
                theta[i][j] += lr * advantage * grad_log_pi_a[i] * s[j]
```

El gradiente `∇ log π(a|s) = e_a - π(·|s)`(en el caso de `a`- probabilidades) es el corazón de los gradientes de política de softmax.

> 梯度 `∇ log π(a|s) = e_a - π(·|s)`(El artículo`a`El índice de probabilidad de eliminación de un solo calor (un-hot) es el núcleo de la tendencia de la estrategia de la softa máxima.

### Paso 5: líneas de base

Un medio corriente de `G`En los últimos episodios, la reducción de varianza es suficiente para que un GridWorld 4×4 funcione; se necesitan ~ 500 episodios para converger.`V̂(s)`y tienes crítico de actores.

> Recientemente .`G`El valor medio de la operación es suficiente para permitir que 4×4 GridWorld trabaje; aproximadamente 500 回合收──将基线升级为学习的`V̂(s)`Se lo recibieron de la crítica.

## Las trampas

- **Exploding gradients.**Las devoluciones pueden ser enormes.`G`¿ Qué ?`~N(0, 1)`en el lote antes de multiplicarse por `∇ log π`¿ Qué ?
  **梯度爆炸。**El reporte puede ser muy grande.`∇ log π`Antes siempre y siempre`G`归一化到                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                         `~N(0, 1)`¿Qué es eso?
- **Entropy collapse.**La política converge a una acción casi determinista demasiado pronto, deja de explorar, se queda atascada.`β · H(π(·|s))`al objetivo.
  **熵坍缩。**策略过早收到近确定性动作,停止探索,陷入困境──修复:向目标添加奖励 `β · H(π(·|s))`¿Qué es eso?
- **High variance.**Vanilla REINFORCE necesita miles de episodios. Una línea de base crítica (lección 07) o la región de confianza de TRPO/PPO (lección 08) es la solución estándar.
  **高方差。**El principio de la reinserción en la sociedad civil es el principio de la reinserción en la sociedad civil.
- **Sample inefficiency.**En política significa que se descarta cada transición después de una actualización. Las correcciones fuera de política a través de muestreo de importancia traen datos, a costa de la variación (la proporción de la OPP es un peso de IS recortado).
  **样本效率低。**La estrategia en línea significa que se abandona todo el cambio después de cada actualización.
- **Non-stationary gradients.**El mismo gradiente de hace 100 episodios usa el antiguo .`π`Los métodos en política se actualizan cada pocos lanzamientos por esta razón.
  **非平稳梯度。**100 回合前的梯度使用旧的 `π`                                                                                                                                                                                                                                                              
- **Credit assignment.**Sin recompensas, las recompensas pasadas contribuyen al ruido.
  **信用分配。**没有未来回报,过去的奖励贡献噪声──始终使用未来回报──

## Usalo con el marco de ejecución

En 2026, REINFORCE rara vez se ejecuta directamente, pero su fórmula de gradiente está en todas partes:

> En 2026 años, la fuerza de la fuerza  muy pocos directamente operar, pero su gradiente fórmula no está presente:

| Use case | Derived method |
|----------|---------------|
| Use case / 用例 | Derived method / 派生方法 |
| Continuous control / 连续控制 | PPO / SAC with Gaussian policy / 高斯策略的 PPO/SAC |
| LLM RLHF / LLM RLHF | PPO with KL penalty, running on token-level policy / 带 KL 惩罚的 PPO，token 级策略 |
| LLM reasoning (DeepSeek) / LLM 推理 | GRPO — REINFORCE with group-relative baseline, no critic / 组相对基线的 REINFORCE，无 critic |
| Multi-agent / 多智能体 | Centralized-critic REINFORCE (MADDPG, COMA) / 集中 critic 的 REINFORCE |
| Discrete action robotics / 离散动作机器人 | A2C, A3C, PPO |
| Preference-only settings / 仅偏好设置 | DPO — REINFORCE rewritten as a preference-likelihood loss, no sampling / 重写为偏好似然损失的 REINFORCE |

Cuando usted lee`loss = -advantage * log_prob`En un guión de formación de 2026, es decir, REINFORCE con una línea de base.

> Cuando estés en el guión de entrenamiento de 2026`loss = -advantage * log_prob`, ahí es la REINFORCE de la linea de base. Todo lo que está en esta línea de código es un desciframiento de la diferencia.

## Envíe el producto .

Salvo como`outputs/skill-policy-gradient-trainer.md`¿Qué es esto ?

```markdown
---
name: policy-gradient-trainer
description: Produce a REINFORCE / actor-critic / PPO training config for a given task and diagnose variance issues.
version: 1.0.0
phase: 9
lesson: 6
tags: [rl, policy-gradient, reinforce]
---

Given an environment (discrete / continuous actions, horizon, reward stats), output:

1. Policy head. Softmax (discrete) or Gaussian (continuous) with parameter counts.
2. Baseline. None (vanilla), running mean, learned `V̂(s)`, or A2C critic.
3. Variance controls. Reward-to-go on by default, return normalization, gradient clip value.
4. Entropy bonus. Coefficient β and decay schedule.
5. Batch size. Episodes per update; on-policy data freshness contract.

Refuse REINFORCE-no-baseline on horizons > 500 steps. Refuse continuous-action control with a softmax head. Flag any run with `β = 0` and observed policy entropy < 0.1 as entropy-collapsed.
```

## Los ejercicios.

1. **Easy.**Implemente REINFORCE en 4×4 GridWorld con una política de softmax lineal. Entrenar durante 1.000 episodios sin una línea de base. Trazar la curva de aprendizaje; medir la variación (std de rendimientos).
2. **Medium.**Añadir una línea de base de la media de ejecución. Entrenar de nuevo. Comparar la eficiencia de la muestra y la variación con la carrera de vainilla. ¿En qué medida la línea de base reduce los pasos a la convergencia?
3. **Hard.**Añadir una bonificación de entropía `β · H(π)`- Específico .`β ∈ {0, 0.01, 0.1, 1.0}`¿Dónde está el punto de interés de esta tarea?

## Términos clave .

| Term | What people say | What it actually means |
|------|-----------------|-----------------------|
| Policy gradient | "Train the policy directly" / 策略梯度 | `∇J(θ) = E[G · ∇ log π_θ(a\|s)]`; derived from the log-derivative trick. |
| REINFORCE | "The original PG algorithm" / REINFORCE算法 | Williams (1992); Monte Carlo returns multiplied by log-policy gradient. |
| Log-derivative trick | "Score function estimator" / 对数导数技巧 | `∇P(τ;θ) = P(τ;θ) · ∇ log P(τ;θ)`; makes gradients of expectations tractable. |
| Baseline | "Variance reduction" / 基线 | Any `b(s)` subtracted from `G`; unbiased because `E[b · ∇ log π] = 0`. |
| Reward-to-go | "Only future returns count" / 未来回报 | `G_t^{from t}` instead of the full `G_0`; correct and lower-variance. |
| Entropy bonus | "Encourage exploration" / 熵正则化 | `+β · H(π(·\|s))` term keeps the policy from collapsing. |
| On-policy | "Train on what you just saw" / 在线策略 | Gradient expectation is w.r.t. the current policy — cannot reuse old data directly. |
| Advantage | "How much better than average" / 优势函数 | `A(s, a) = G(s, a) - V(s)`; the signed quantity REINFORCE-with-baseline multiplies. |

## Más Leer más Leer más

- [Williams (1992). Simple Statistical Gradient-Following Algorithms for Connectionist Reinforcement Learning](https://link.springer.com/article/10.1007/BF00992696) el papel original de REINFORCE.
- [Sutton et al. (2000). Policy Gradient Methods for Reinforcement Learning with Function Approximation](https://papers.nips.cc/paper_files/paper/1999/hash/464d828b85b0bed98e80ade0a5c43b0f-Abstract.html) el teorema moderno de la política-gradiente con aproximación de funciones.
- [Sutton & Barto (2018). Ch. 13 — Policy Gradient Methods](http://incompleteideas.net/book/RLbook2020.pdf) Presentación de libros de texto.
- [OpenAI Spinning Up — VPG / REINFORCE](https://spinningup.openai.com/en/latest/algorithms/vpg.html) Exposición pedagógica clara con código PyTorch.
- [Peters & Schaal (2008). Reinforcement Learning of Motor Skills with Policy Gradients](https://homes.cs.washington.edu/~todorov/courses/amath579/reading/PolicyGradient.pdf) Reducción de la varianza y la visión natural-gradiente que conecta REINFORCE a la familia de la región de confianza (TRPO, PPO).
