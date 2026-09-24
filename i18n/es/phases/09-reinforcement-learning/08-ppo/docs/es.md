# Optimización de políticas proximas (PPO) 

> A2C arroja cada implementación después de una actualización. PPO envuelve el gradiente de política en una relación de importancia reducida para que pueda hacer 10+ épocas en los mismos datos sin que la política explode. Schulman et al. (2017).

> **【中文解读】**PPO utiliza el porcentaje de importancia de corte en la estrategia de recorte, para que el mismo grupo de datos pueda hacer más de 10 radas de actualización y la estrategia no explotará.

> **【拓展：PPO 与 ChatGPT】**PPO es el algoritmo central de la capacitación de ChatGPT RLHF. Instruir GPT(2022) Usar PPO para realizar preferencias humanas a GPT-3 es la técnica detrás de ChatGPT. La estabilidad y simplicidad de PPO lo hacen la primera opción en la industria.

**Type:** Build | **类型:** 动手
**Languages:** Python | **语言:** Python
**Prerequisites:** Phase 9 · 06 (REINFORCE), Phase 9 · 07 (Actor-Critic) | **前置知识:** Phase 9 · 06 (REINFORCE), Phase 9 · 07 (Actor-Critic)
**Time:** ~75 minutes | **时间:** ~75 分钟

## El problema es la introducción del problema

A2C (lección 07) es sobre la política: el gradiente `E_{π_θ}[A · ∇ log π_θ]`Requiere datos recogidos de la *current* `π_θ`. Toma una actualización, y `π_θ`los cambios; los datos que usaste ahora están fuera de política.

> A2C ((Ley 07) está en línea estrategia de:梯度 `E_{π_θ}[A · ∇ log π_θ]`要求从*当前* `π_θ`采样数据── Una vez más `π_θ` modificar; los datos que utilizas se convierten en estrategias ∙ Reutilizarlo en la escala tiene una diferencia ∙

En Atari, un despliegue en 8 envs × 128 pasos = 1024 transiciones y una docena de segundos de tiempo ambiental.

> El despliegue es muy caro. En Atari, 8 ambientes × 128 pasos = 1024 veces de transferencia y 10 segundos de tiempo ambiental.

La optimización de las políticas de la región de confianza (TRPO, Schulman 2015) fue la primera solución: restringir cada actualización para que la divergencia entre las políticas antiguas y nuevas de KL se mantenga por debajo `δ`Teóricamente limpio, pero requiere una solución de gradiente conjugado por actualización.

> Crear un nuevo sistema de control de la seguridad social en el mundo.`δ`En teoría, esto es bueno, pero cada actualización necesita un nivel de resolución.

PPO (Schulman et al. 2017) reemplaza la restricción de la región de confianza dura con un objetivo simple recortado. Una línea extra de código. Diez épocas por implementación. No hay gradientes conjugados.

> PPO(Schulman 等人 2017) con un simple corte de objetivos sustituir el dominio de la confianza en el trabajo.

> **【中文解读】**La innovación central de PPO: utilizar el objetivo de corte para reemplazar a TRPO. La tasa de importancia de R_t(theta) = pi_theta / pi_old 被剪到 [1-epsilon, 1+epsilon] 范围内. Cuando el beneficio A_t>0 时, no va a ser muy buena la probabilidad de movimiento se propone demasiado alto; cuando A_t<0 时, no va a ser mala la probabilidad de movimiento se reduce demasiado bajo.

> **【拓展：PPO 之外的选择——DPO 与 GRPO】**Aunque el PPO sigue siendo una opción predeterminada para 2026, el esquema de sustitución está surgiendo.

## El concepto central.

![PPO clipped surrogate objective: ratio clipping at 1 ± ε](../assets/ppo.svg)

**The importance ratio.**

`r_t(θ) = π_θ(a_t | s_t) / π_{θ_old}(a_t | s_t)`

Esta es la proporción de probabilidad de la nueva política frente a la política que recopiló los datos. `r_t = 1`significa que no hay cambio.`r_t = 2`significa que la nueva política tiene el doble de probabilidades de tomar`a_t`como el viejo.

> **重要性比率。**La nueva estrategia se compara con la estrategia de recopilación de datos.`r_t = 1`Se muestra sin cambios.`r_t = 2`Indicar nuevas estrategias para adoptar`a_t`La probabilidad es el doble de la estrategia anterior.

**The clipped surrogate.**

`L^{CLIP}(θ) = E_t [ min( r_t(θ) A_t, clip(r_t(θ), 1-ε, 1+ε) A_t ) ]`

Dos términos:

- Si la ventaja es`A_t > 0`y la proporción trata de crecer más allá `1 + ε`, el clip aplanar el gradiente  no empujar una buena acción más allá de `+ε`por encima de la antigua probabilidad.
- Si la ventaja es`A_t < 0`y la proporción trata de crecer más allá `1 - ε`(lo que significa que haríamos una mala acción más probable en comparación con su reducción recortada), el clip tapa el gradiente  no empujar una mala acción por debajo `-ε`¿ Qué ?

El `min`maneja la otra dirección: si la relación se ha movido en la dirección *beneficial* , todavía obtiene el gradiente (no hay recorte en el lado que le perjudique).

Típico`ε = 0.2`. Describir el objetivo como función de `r_t`: una función lineal de pieza con un techo plano en el "lado bueno" y un piso plano en el "lado malo".

> **裁剪代理。**两项: si el beneficio es positivo y el porcentaje excede `1 + ε`No hagas que el buen movimiento sea más alto que la probabilidad anterior.`+ε`更多── si la ventaja es negativa y la tasa es inferior a `1 - ε`No hay que reducir el nivel de los malos movimientos.`-ε`更多── típico `ε = 0.2`¿Qué es eso?

> **【中文解读】**Intucción del mecanismo de corte de PPO:epsilon=0.2 significa que la estrategia cambia al máximo un 20% por actualización. Si un movimiento es bueno, la probabilidad aumenta al 20%; si un movimiento es malo, la probabilidad disminuye al 20%. Esto evita que el "olvido catastrófico" no cambie demasiado.

**The full PPO loss.**

`L(θ, φ) = L^{CLIP}(θ) - c_v · (V_φ(s_t) - V_t^{target})² + c_e · H(π_θ(·|s_t))`

La misma estructura actor-crítica que A2C. Tres coeficientes, por lo general `c_v = 0.5`¿ Qué ?`c_e = 0.01`¿ Qué ?`ε = 0.2`¿ Qué ?

> **完整的 PPO 损失。**Con A2C comparable Actor-Critic 结构──三个系数, normalmente `c_v = 0.5`¿Qué es esto?`c_e = 0.01`¿Qué es esto?`ε = 0.2`¿Qué es eso?

**The training loop.**

1. Recolectar`N × T`transiciones en el transcurso de la`N`Envistas paralelas para `T`cada uno de los pasos.
2. Computa ventajas (GAE), congelarlas como constantes.
3. Se congela .`π_{θ_old}`como una instantánea de la corriente `π_θ`¿ Qué ?
4. Para`K`La Comisión ha adoptado una directiva relativa a la protección de los animales en el sector de la pesca.`(s, a, A, V_target, log π_old(a|s))`¿Qué es esto ?
   - Computación`r_t(θ) = exp(log π_θ(a|s) - log π_old(a|s))`¿ Qué ?
   - Aplicar`L^{CLIP}`+ pérdida de valor + entropía.
   - Un paso gradual.
5. Desecha el despliegue y vuelve al paso 1.

`K = 10`El PPO es robusto: los números exactos rara vez importan dentro de ±50%.

> **训练循环。**收集 → 计算 GAE 优势 → 结旧策略 → K 轮更新 → 丢弃数据──`K = 10`Y 64 de los pequeños lotes son los estándar superparámetros.

**KL-penalty variant.**El documento original propuso una alternativa mediante una penalidad KL adaptativa: `L = L^{PG} - β · KL(π_θ || π_old)`con`β`La versión de recorte se convirtió en dominante; la variante KL sobrevive en RLHF (donde KL a la política de referencia es una restricción separada que siempre quieres de todos modos).

> **KL 惩罚变体。**El original artículo propuso una alternativa al uso de autoadaptación KL 惩罚.

## Construye y realiza.
```figure
ppo-clip
```

## Construye el mismo

### Paso 1: captura `log π_old(a | s)`en el momento del despliegue

```python
for step in range(T):
    probs = softmax(logits(theta, state_features(s)))
    a = sample(probs, rng)
    s_next, r, done = env.step(s, a)
    buffer.append({
        "s": s, "a": a, "r": r, "done": done,
        "v_old": value(w, state_features(s)),
        "log_pi_old": log(probs[a] + 1e-12),
    })
    s = s_next
```

La instantánea se toma una vez, en el momento del lanzamiento.

> 快照在推出时拍摄一次──在更新时代 期间不变──

### Paso 2: calcular las ventajas de la AEG (lección 07)

Igual que el A2C. Normaliza en todo el lote.

> Con A2C, comparación entre los grupos de producción.

### Paso 3: actualización de sustituta recortada

```python
for _ in range(K_EPOCHS):
    for mb in minibatches(buffer, size=64):
        for rec in mb:
            x = state_features(rec["s"])
            probs = softmax(logits(theta, x))
            logp = log(probs[rec["a"]] + 1e-12)
            ratio = exp(logp - rec["log_pi_old"])
            adv = rec["advantage"]
            surrogate = min(
                ratio * adv,
                clamp(ratio, 1 - EPS, 1 + EPS) * adv,
            )
            # backprop -surrogate, add value loss, subtract entropy
            grad_logpi = onehot(rec["a"]) - probs
            if (adv > 0 and ratio >= 1 + EPS) or (adv < 0 and ratio <= 1 - EPS):
                pg_grad = 0.0  # clipped
            else:
                pg_grad = ratio * adv
            for i in range(N_ACTIONS):
                for j in range(N_FEAT):
                    theta[i][j] += LR * pg_grad * grad_logpi[i] * x[j]
```

El patrón de "gradiente reducido → cero" es el corazón de la PPO. Si la nueva política ya ha desviado demasiado en la dirección beneficiosa, la actualización se detiene.

> El modelo de "corte → 零梯度" es el núcleo de la PPO. Si la nueva estrategia se ha desviado demasiado en dirección favorable, la actualización se detiene.

### Paso 4: valor y entropía

Añadir MSE estándar al objetivo crítico y una bonificación de entropía en el actor, igual que A2C.

> Para críticos  objetivos añadir criterios MSE, para actores                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                

### Paso 5: diagnóstico

Tres cosas para ver en cada actualización:

> Cada actualización tiene tres cosas que controlar:

- **Mean KL** `E[log π_old - log π_θ]`Debería quedarse .`[0, 0.02]`Si pasa por ahí`0.1`, reducir `K_EPOCHS`o `LR`¿ Qué ?
  **平均 KL。**应保持在 `[0, 0.02]`Si excede`0.1`, reducido `K_EPOCHS`O `LR`¿Qué es eso?
- **Clip fraction** la fracción de muestras cuya proporción se encuentra fuera `[1-ε, 1+ε]`- Deberían ser .`~0.1-0.3`Si ...`~0`, el clip nunca activa → aumento `LR`o `K_EPOCHS`Si ...`~0.5+`, estás sobre-ajustando el despliegue → bajarlos.
  **裁剪比例。**Porcentaje de excedencia`[1-ε, 1+ε]`Por lo tanto, el porcentaje de los ingresos de la empresa es de aproximadamente un millón.`~0.1-0.3`¿Qué es eso?
- **Explained variance** `1 - Var(V_target - V_pred) / Var(V_target)`- Metrica de calidad crítica. Debería subir hacia 1 a medida que el crítico aprende.
  **解释方差。**Critical Quality Index. debe seguir el critico de aprendizaje.

## Las trampas

- **Clip coefficient mistuned.** `ε = 0.2`Es el estándar de facto.`0.1`hace que las actualizaciones sean demasiado tímidas; `0.3+`Invita a la inestabilidad.
  **裁剪系数调错。** `ε = 0.2`Es un hecho.`0.1`太保守;`0.3+`导致不稳定──
- **Too many epochs.** `K > 20`La política de la UE se desestabiliza de forma rutinaria porque la política se deriva lejos de la`π_old`- Epocas de límite, especialmente para las redes grandes.
  **太多 epoch。** `K > 20`常常不稳定,因为 las estrategias se alejan `π_old`太远──限制时代, especialmente la gran red──
- **No reward normalization.**Las grandes escalas de recompensa se incorporan al rango de los clip. Normaliza las recompensas (con std) antes de las ventajas de la computación.
  **没有奖励归一化。**La medida de la recompensa se reduce a la medida de la medida de la recompensa.
- **Forgetting advantage normalization.**La normalización de la media cero/unidad-std por lote es estándar.
  **忘记优势归一化。**Cada lote de valores mínimos/unidades estándares de diferenciación es estándar.
- **Learning rate not decayed.**La PPO se beneficia de la decadencia de la LR lineal a cero.
  **学习率未衰减。**PPO de LR lineal  disminución a zero                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                   
- **Importance ratio math errors.**Siempre .`exp(log_new - log_old)`para la estabilidad numérica, no `new / old`¿ Qué ?
  **重要性比率数学错误。**始终使用 `exp(log_new - log_old)`Garantizar la estabilidad de los valores, y no `new / old`¿Qué es eso?
- **Wrong gradient sign.**Maximizar la madre sustitua = *minimizar* `-L^{CLIP}`Un letrero invertido es el virus más común.
  **梯度符号错误。**Máximación de agentes = * minimizar* `-L^{CLIP}`◊ 符号反转为 PPO 最常见 bug──

## Usalo con el marco de ejecución

PPO es el algoritmo RL predeterminado de 2026 en un sorprendente número de dominios:

> PPO es un algoritmo de RL de 2026 en muchos campos:

| Use case | PPO variant |
|----------|-------------|
| Use case / 用例 | PPO variant / PPO 变体 |
| MuJoCo / robotics control / MuJoCo/机器人控制 | PPO with Gaussian policy, GAE(0.95) / 高斯策略的 PPO，GAE(0.95) |
| Atari / discrete games / Atari/离散游戏 | PPO with categorical policy, rolling 128-step rollouts / 分类策略的 PPO |
| RLHF for LLMs / LLM 的 RLHF | PPO with KL penalty to reference model, reward from RM at end of response / 带 KL 惩罚的 PPO |
| Large-scale game agents / 大规模游戏 Agent | IMPALA + PPO (AlphaStar, OpenAI Five) |
| Reasoning LLMs / 推理 LLM | GRPO (Lesson 12) — PPO variant without critic / 无 Critic 的 PPO 变体 |
| Preference-only data / 仅偏好数据 | DPO — closed-form collapsing of PPO+KL, no online sampling / 闭式 PPO+KL 折叠 |

La forma de PPO *perdida*  recortado sustituto + valor + entropía  es el andamio para DPO, GRPO y casi todos los oleoductos RLHF.

> El PPO de forma* de pérdida* cortar el agente + 值 + 是 DPO、GRPO 和几乎所有RLHF 流水线的脚手架──

## Envíe el producto .

Salvo como`outputs/skill-ppo-trainer.md`¿Qué es esto ?

```markdown
---
name: ppo-trainer
description: Produce a PPO training config and a diagnostic plan for a given environment.
version: 1.0.0
phase: 9
lesson: 8
tags: [rl, ppo, policy-gradient]
---

Given an environment and training budget, output:

1. Rollout size. `N` envs × `T` steps.
2. Update schedule. `K` epochs, minibatch size, LR schedule.
3. Surrogate params. `ε` (clip), `c_v`, `c_e`, advantage normalization on.
4. Advantage. GAE(`λ`) with explicit `γ` and `λ`.
5. Diagnostics plan. KL, clip fraction, explained variance thresholds with alerts.

Refuse `K > 30` or `ε > 0.3` (unsafe trust region). Refuse any PPO run without advantage normalization or KL/clip monitoring. Flag clip fraction sustained above 0.4 as drift.
```

## Los ejercicios.

1. **Easy.**Ejecutar PPO en 4×4 GridWorld con `ε=0.2, K=4`. Comparar la eficiencia de la muestra con A2C (una época por lanzamiento) en etapas de entorno iguales.
2. **Medium.**Especialización`K ∈ {1, 4, 10, 30}`. Retorno de la trama vs. pasos env y seguimiento de media KL por actualización.`K`¿KL explotará en esta tarea?
3. **Hard.**En el caso de las personas que no tengan derecho a la prestación de servicios, el importe de la prestación de servicios de servicios de servicios de servicios de servicios de servicios de servicios de servicios de servicios de servicios de servicios de servicios de servicios de servicios de servicios de servicios de servicios de servicios de servicios de servicios de servicios de servicios de servicios de servicios de servicios de servicios de servicios de servicios de servicios de servicios de servicios de servicios de servicios de servicios de servicios de servicios de servicios de servicios de servicios de servicios de servicios de servicios de servicios de servicios de servicios de servicios de servicios de servicios de servicios de servicios de servicios de servicios de servicios de servicios de servicios de servicios de servicios de servicios de servicios de servicios de servicios de servicios de servicios de servicios de servicios de servicios de servicios de servicios de servicios de servicios de servicios de servicios de servicios de servicios de servicios de servicios de servicios de servicios de servicios de servicios de servicios de servicios de servicios de servicios de servicios de servicios de servicios de servicios de servicios de servicios de servicios de servicios de servicios de servicios de servicios de servicios de servicios de servicios de servicios de servicios de servicios de servicios de servicios de servicios de servicios de servicios de servicios de servicios de servicios de servicios de servicios de servicios de servicios de servicios de servicios de servicios de servicios de servicios de servicios de servicios de servicios de servicios de servicios de servicios de servicios de servicios de servicios de servicios de servicios de servicios de servicios de servicios de servicios de servicios de servicios de servicios de servicios de servicios de servicios de servicios de servicios de servicios de servicios de servicios de servicios de servicios de servicios de servicios de servicios de servicios de servicios de servicios de servicios de servicios de servicios de servicios de servicios de servicios de servicios de servicios de servicios de servicios de servicios de servicios de servicios de servicios de servicios de servicios de servicios de servicios de servicios de servicios de servicios de servicios de servicios de servicios de servicios de servicios de servicios de servicios de servicios de servicios de servicios de servicios de servicios de servicios de servicios de servicios de servicios de servicios de servicios de servicios de servicios de servicios de servicios de servicios de servicios de servicios de servicios de servicios de servicios de servicios de servicios de servicios de servicios de servicios de la Unión.`β`duplicado si `KL > 2·target`, se redujeron a la mitad si `KL < target/2`) Compare el rendimiento final, la estabilidad y la libre de clip.

## Términos clave .

| Term | What people say | What it actually means |
|------|-----------------|-----------------------|
| Importance ratio | "r_t(θ)" | `π_θ(a\|s) / π_old(a\|s)`; deviation from the policy that collected the data. |
| Clipped surrogate | "PPO's main trick" | `min(r·A, clip(r, 1-ε, 1+ε)·A)`; flat gradient past the clip on beneficial side. |
| Trust region | "TRPO / PPO intent" | Limit each update's KL to guarantee monotone improvement. |
| KL penalty | "Soft trust region" | Alternative PPO: `L - β · KL(π_θ \|\| π_old)`. Adaptive `β`. |
| Clip fraction | "How often clipping triggers" | Diagnostic — should be 0.1-0.3; outside means mistuned. |
| Multi-epoch training | "Data reuse" | K epochs on each rollout; variance cost traded for sample efficiency. |
| On-policy-ish | "Mostly on-policy" | PPO is nominally on-policy but K>1 epochs uses slightly-off-policy data safely. |
| PPO-KL | "The other PPO" | KL-penalty variant; used in RLHF where KL-to-reference is already a constraint. |

## Más Leer más Leer más

- [Schulman et al. (2017). Proximal Policy Optimization Algorithms](https://arxiv.org/abs/1707.06347)- El periódico.
- [Schulman et al. (2015). Trust Region Policy Optimization](https://arxiv.org/abs/1502.05477) TRPO, el predecesor de PPO.
- [Andrychowicz et al. (2021). What Matters In On-Policy RL? A Large-Scale Empirical Study](https://arxiv.org/abs/2006.05990) todos los hiperparámetros de PPO eliminados.
- [Ouyang et al. (2022). Training language models to follow instructions with human feedback](https://arxiv.org/abs/2203.02155) InstructGPT; la receta de PPO en RLHF.
- [OpenAI Spinning Up — PPO](https://spinningup.openai.com/en/latest/algorithms/ppo.html) limpia exposición moderna con PyTorch.
- [CleanRL PPO implementation](https://github.com/vwxyzjn/cleanrl) PPO de referencia de archivo único utilizado por muchos documentos.
- [Hugging Face TRL — PPOTrainer](https://huggingface.co/docs/trl/main/en/ppo_trainer) la receta de producción de PPO en modelos de lenguaje; leer junto con la Lección 09 (RLHF).
- [Engstrom et al. (2020). Implementation Matters in Deep Policy Gradients](https://arxiv.org/abs/2005.12729) el documento "37 optimizaciones de nivel de código"; cuáles son los trucos de PPO que son cargadores y cuáles son el folclore.
