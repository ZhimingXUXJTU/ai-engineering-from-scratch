# Modelaje de recompensas y RLHF.

> Los humanos no pueden escribir una función de recompensa para "buena respuesta de asistente", pero pueden comparar dos respuestas y elegir la mejor. Ajuste un modelo de recompensa a esas comparaciones, luego RL el modelo de lenguaje en contra de ella. Cristiano 2017.

> **【中文解读】**La gente no puede escribir una función de recompensa para "buen ayudante de respuesta", pero puede comparar dos veces mejor.

> **【拓展：RLHF 是大模型对齐的关键】**RLHF(basado en humanos反的强化学习) 是ChatGPT成功的核心技术──三步流程:(1) 监督微调 SFT;(2) 训练奖励模型 RM;(3) 用PPO 优化 LM──DPO 简化第2-3步,但本质相同──

**Type:** Build | **类型:** 动手
**Languages:** Python | **语言:** Python
**Prerequisites:** Phase 5 · 05 (Sentiment), Phase 9 · 08 (PPO) | **前置知识:** Phase 5 · 05 (情感分析), Phase 9 · 08 (PPO)
**Time:** ~45 minutes | **时间:** ~45 分钟

## El problema es la introducción del problema

Usted entrenó un modelo de lenguaje en el objetivo de predicción de tokens. Escribe inglés gramatical. También miente, vagabundea y se niega a rechazar. No se puede arreglar esto con más preentrenamiento.

> Usted ha entrenado un modelo de lenguaje en el siguiente token 预测目标. Escribió un lenguaje correcto en inglés. Pero también mentirá, correrá, rechazará, rechazará.

Si quieres una recompensa *escalar* que diga "respuesta A es mejor que respuesta B para instrucción X". Es imposible escribir esa función de recompensa a mano. "Helpfulness" no es una expresión de forma cerrada sobre tokens. Pero los humanos pueden comparar dos salidas y marcar una preferencia. Eso es barato para recoger en escala.

> Usted quiere una* recompensa de la marca*, indicando" para la instrucción X, responder A a B mejor"―Escribe esta función de recompensa es imposible―"utilidad" no es un símbolo de expresión cerrada de arriba―pero el ser humano puede comparar dos salidas y marcar preferencias―esto puede ser un bajo costo de la recopilación masiva―

RLHF (Christiano et al. 2017; Ouyang et al. 2022) convierte las preferencias en un modelo de recompensa, luego optimiza el LM a través de PPO en contra de esa recompensa. En tres pasos: SFT → RM → PPO. Es la receta que envió ChatGPT, Claude, Gemini y todos los demás LLM alineados en 20232025.

> RLHF se convertirá preferentemente en un modelo de recompensa, y luego se optimizará a través de PPO para LM.

En 2026 el paso PPO se sustituye principalmente por DPO (Fase 10 · 08) porque es más barato y casi tan bueno para la sintonización de alineamientos. Pero la pieza de modelo de recompensa sigue siendo la base de cada muestreo Best-of-N, cada RL-from-verifiable-rewards pipeline, y cada modelo de razonamiento que utiliza un modelo de recompensa de proceso.

> En 2026 los pasos de la PPO fueron sustituidos por los DPO, ya que son más económicos y tienen casi el mismo efecto. Pero el modelo de recompensas sigue siendo el mejor de los modelos de recompensas de la RL.

> **【中文解读】**RLHF 三阶段流程:(1) SFT supervisa los pequeños modelos básicos en datos de demostraciones humanas;(2) RM utiliza la preferencia humana por el entrenamiento Bradley-Terry 奖励模型;(3) PPO utiliza el modelo de recompensa para optimizar el lenguaje de los signos, al mismo tiempo que KL 惩罚防止偏离 SFT 太远── Aunque en 2026 muchos pasos de la PPO 已 ser reemplazados por DPO, el modelo de recompensa sigue siendo el mejor de los modelos de N 采样、可验证奖励 RL、 proceso de recompensa modelo en uso amplio en escenarios como este.

> **【拓展：DPO 与 RLHF 的对比】**DPO(Optimización de Preferencias Directas) combinará RM+PPO de RLHF 两步合并为一步 directamente desde la preferencia hacia la estrategia de entrenamiento, sin necesidad de un modelo de recompensa de entrenamiento manifiesto. Matemáticamente, el DPO es equivalente a la estrategia de optimización bajo el modelo Bradley-Terry.

## El concepto central.

![Three-stage RLHF: SFT, RM training on pairwise prefs, PPO with KL penalty](../assets/rlhf.svg)

**Stage 1: Supervised Fine-Tuning (SFT).**Comienza con un modelo base pre-entrenado. Enfine las demostraciones escritas por el hombre del comportamiento objetivo (respuestas que siguen instrucciones, respuestas útiles, etc.). Resultado: un modelo `π_SFT`que es *preciado hacia el buen comportamiento* pero todavía tiene un espacio de acción ilimitado.

> **阶段 1：监督微调（SFT）。**Desde el modelo básico de pre-entrenamiento comienza. En la muestra de comportamiento objetivo de la redacción humana se modifica. Resultado: un modelo de comportamiento favorable, pero todavía tiene un espacio de movimiento ilimitado.`π_SFT`¿Qué es eso?

**Stage 2: Reward Model training.**

- Recoger pares de respuestas `(y_+, y_-)`a las instrucciones `x`, etiquetado por los seres humanos como "y_+ es preferido sobre y_-."
- Entrenar un modelo de recompensa`R_φ(x, y)`para asignar puntuaciones más altas a `y_+`¿ Qué ?
- Las pérdidas:**Bradley-Terry pairwise logistic**¿Qué es esto ?

  `L(φ) = -E[ log σ(R_φ(x, y_+) - R_φ(x, y_-)) ]`

  La diferencia en la recompensa implica una probabilidad de log de preferencia. BT ha sido el estándar desde 1952 (Bradley-Terry) y es la opción dominante en la moderna RLHF.

- `R_φ`El modelo de transformer de la base de la base de la base de la base de la base de la base de la base de la base de la base de la base de la base de la base de la base de la base de la base de la base de la base de la base de la base de la base de la base de la base de la base de la base de la base de la base de la base de la base de la base de la base de la base de la base de la base de la base de la base de la base de la base de la base de la base de la base de la base de la base de la base de la base de la base de la base de la base de la base de la base de la base de la base de la base de la base de la base de la base de la base de la base de la base de la base de la base de la base de la base de la base de la base de la base de la base de la base de la base de la base de la base de la base de la base de datos.

> **阶段 2：奖励模型训练。** recoger las preferencias de los marcos humanos `(y_+, y_-)`, entrenamiento de recompensas modelo dar`y_+`Más alto... la pérdida es Bradley-Terry... y regreso lógico.`R_φ`Normalmente desde SFT 模型初始化, añadir una muestra de salida.

**Stage 3: PPO against the RM with KL penalty.**

- Iniciar la política de capacitación `π_θ`de la`π_SFT`Mantenga una referencia congelada.`π_ref = π_SFT`¿ Qué ?
- Recompensa al final de una respuesta `y`¿Qué es esto ?

  `r_total(x, y) = R_φ(x, y) - β · KL(π_θ(·|x) || π_ref(·|x))`

  La penalidad de KL impide`π_θ`de la deriva arbitraria de `π_SFT` es un *regularizador*, no una región de confianza difícil. `β`Por lo general`0.01`- ¿ Qué ?`0.05`¿ Qué ?
- ejecuta PPO (Ley 08) con esta recompensa. Las ventajas se calculan en la trayectoria de nivel de token, pero el RM marca solo la respuesta completa.

> **阶段 3：对 RM 做 PPO + KL 惩罚。**Desde`π_SFT`Iniciación de estrategias de entrenamiento. Recompensa = RM 分数 - β × KL 到参考策略.

**Why the KL?**Sin él, PPO encontrará estrategias de hackeo de recompensas  el RM sólo fue entrenado en completos en distribución. Una respuesta fuera de distribución podría tener un puntaje más alto que cualquier otro escrito por humanos.`π_θ`Es el nodo más importante en el RLHF.

> **为什么需要 KL？** Sin ella, la OPPO encontrará estrategias de recompensa RM sólo en la formación en datos distribuidos                                                                                                                                                                                                                                                 `π_θ`保持在 RM 训练的流形附近──这是 el giro más importante en RLHF──

**2026 status:**

- **DPO**(Rafailov 2023): el álgebra de forma cerrada se desploma en la etapa 2 + 3 en una sola pérdida supervisada sobre los datos de preferencia. No RM, no PPO. La misma calidad en los puntos de referencia de alineación para una fracción del cálculo.
- **GRPO**(DeepSeek 20242025): PPO con un baseline relativo al grupo en lugar de un crítico, recompensa de un *verificador* (codificación / correspondencias matemáticas) en lugar de un RM entrenado por el hombre.
- **Process reward models (PRMs):**soluciones parciales de puntaje (cada paso de razonamiento), utilizadas tanto en las variantes RLHF como en las GRPO para el razonamiento.
- **Constitutional AI / RLAIF:**El programa de investigación de la Comisión de Investigación y Desarrollo de la Investigación de la Investigación de la Investigación de la Investigación de la Investigación de la Investigación de la Investigación de la Investigación de la Investigación de la Investigación de la Investigación de la Investigación de la Investigación de la Investigación de la Investigación de la Investigación de la Investigación de la Investigación de la Investigación de la Investigación de la Investigación de la Investigación de la Investigación de la Investigación de la Investigación de la Investigación de la Investigación de la Investigación de la Investigación de la Investigación de la Investigación de la Investigación de la Investigación de la Investigación de la Investigación de la Investigación de la Investigación de la Investigación de la Investigación de la Investigación de la Investigación de la Investigación de la Investigación de la Investigación de la Investigación de la Investigación de la Investigación de la Investigación de la Investigación de la Investigación de la Investigación de la Investigación de la Investigación de la Investigación de la Investigación de la Investigación de la Investigación de la Investigación de la Investigación de la Investigación de la Investigación de la Investigación de la Investigación de la Investigación de la Investigación de la Investigación de la Investigación de la Investigación de la Investigación de la Investigación de la Investigación de la Investigación de la Investigación de la Investigación de la Investigación de la Investigación de la Investigación de la Investigación de la Investigación de la Investigación de la Investigación de la Investigación de la Investigación de la Investigación de la Investigación de la Investigación de la Investigación de la Investigación de la Investigación de la Investigación de la Investigación de la Investigación de la Investigación de la Investigación de la Investigación de la Investigación de la Investigación de la Investigación de la Investigación de la Investigación de la Investigación de la Investigación de la Investigación de la Investigación de la Investigación de la Investigación de la Investigación de la Investigación de la Investigación de la Investigación de la Investigación de la Investigación de la Investigación de la Investigación de la Investigación de la Investigación de la Investigación de la Investigación de la Investigación de la Investigación de la Investigación de la Investigación de la Investigación de la Investigación

> **2026 年状态：**DPO 将阶段 2+3 折叠为单一监督损失──GRPO 用组相对基线替代评论,用验证器替代人类训练的 RM──PRM 评分部分解决方案──Constitutional AI / RLAIF 用对齐的 LLM 生成偏好──

## Construye y realiza.
```figure
reward-model
```

## Construye el mismo

Esta lección utiliza pequeñas "invitaciones" y "respuestas" sintéticas representadas como cuerdas. El RM es un punteador lineal sobre una representación de bolsa de fichas.`code/main.py`¿ Qué ?

> Este curso utiliza sintetizados pequeños "pues" y "recap" caracteres. RM es un evaluador de la línea de la expresión de la palabra en bolsa.

### Paso 1: Datos de preferencias sintéticas

```python
PROMPTS = ["help me", "answer me", "explain this"]
GOOD_WORDS = {"clear", "specific", "kind", "thorough"}
BAD_WORDS = {"vague", "rude", "wrong", "short"}

def make_pair(rng):
    x = rng.choice(PROMPTS)
    y_good = rng.choice(list(GOOD_WORDS)) + " " + rng.choice(list(GOOD_WORDS))
    y_bad = rng.choice(list(BAD_WORDS)) + " " + rng.choice(list(BAD_WORDS))
    return (x, y_good, y_bad)
```

En el RLHF real, esto es reemplazado por etiquetadores humanos.`(prompt, preferred_response, rejected_response)` es idéntico.

> Verdaderos RLHF 中由人类标注者替代──形状`(提示, 偏好回复, 拒绝回复)` Totalmente igual.

### Paso 2: modelo de recompensa Bradley-Terry

Punto lineal: `R(x, y) = w · bag(y)`. Entrenamiento para minimizar la pérdida de registro de BT en parejas:

```python
def rm_train_step(w, x, y_pos, y_neg, lr):
    r_pos = dot(w, bag(y_pos))
    r_neg = dot(w, bag(y_neg))
    p = sigmoid(r_pos - r_neg)
    for tok, cnt in bag(y_pos).items():
        w[tok] += lr * (1 - p) * cnt
    for tok, cnt in bag(y_neg).items():
        w[tok] -= lr * (1 - p) * cnt
```

Después de unos cientos de actualizaciones,`w`asigna pesos positivos a los tokens de buenas palabras y negativos a los malos.

> Después de un par de actualizaciones,`w`给好词 token 分配正权重,坏词 分配负权重──

### Paso 3: Política similar a la PPO en la parte superior de RM

Nuestra política de juguetes produce un solo token de un vocabulario.`log π_θ(token | prompt)`, añadir una penalidad KL-a-referencia, y aplicar el recortado PPO sustituta.

> Nuestra estrategia de juguete genera un solo token de una palabra.`log π_θ(token | prompt)`, añadir KL a la punción de la estrategia de referencia, y aplicar el corte de PPO 代理

```python
def rlhf_step(theta, ref, w, prompt, rng, eps=0.2, beta=0.1, lr=0.05):
    logits_theta = policy_logits(theta, prompt)
    probs = softmax(logits_theta)
    token = sample(probs, rng)
    logits_ref = policy_logits(ref, prompt)
    probs_ref = softmax(logits_ref)
    reward = dot(w, bag([token])) - beta * kl(probs, probs_ref)
    # ppo-style update on theta, treating reward as the return
    ...
```

> 关键:奖励 = RM 分数 - β × KL(π_θ 1920 π_ref) ――β es control estrategia漂移程度的关键超参数太大策略几乎不变,太小则奖励黑客开始──

### Paso 4: Monitorear el KL

Mediano de pista`KL(π_θ || π_ref)`Cada actualización. Si se hace pasar.`~5-10`La política ha desviado mucho de la`π_SFT` más bajo `β`Este es el diagnóstico más alto en la verdadera RLHF.

> Cada actualización sigue el promedio`KL(π_θ || π_ref)`Si excede`~5-10`, estrategia ha ido lejos`π_SFT`可能 β 正在降低或奖励黑客正在开始──... es la verdadera RLHF más importante diagnóstico──

### Paso 5: receta de producción con TRL

Una vez que entiendes la línea de juguetes, aquí hay el mismo bucle que un usuario de biblioteca real lo escribe.[TRL](https://huggingface.co/docs/trl)es la aplicación de referencia  `RewardTrainer`para la etapa 2 y `PPOTrainer`(con un KL-to-reference incorporado) para la etapa 3.

> Una vez que comprendes la línea de flujo de agua de los juguetes, aquí es el modo en que los usuarios de la biblioteca escriben el mismo ciclo.`RewardTrainer`, Etapa 3 Usado`PPOTrainer`¿Qué es eso?

```python
# Stage 2: reward model from pairwise preferences
from trl import RewardTrainer, RewardConfig
from transformers import AutoModelForSequenceClassification, AutoTokenizer

tok = AutoTokenizer.from_pretrained("meta-llama/Llama-3.1-8B-Instruct")
rm = AutoModelForSequenceClassification.from_pretrained(
    "meta-llama/Llama-3.1-8B-Instruct", num_labels=1
)

# dataset rows: {"prompt", "chosen", "rejected"} — Bradley-Terry format
trainer = RewardTrainer(
    model=rm,
    tokenizer=tok,
    train_dataset=preference_data,
    args=RewardConfig(output_dir="./rm", num_train_epochs=1, learning_rate=1e-5),
)
trainer.train()
```

```python
# Stage 3: PPO against the RM with KL penalty to the SFT reference
from trl import PPOTrainer, PPOConfig, AutoModelForCausalLMWithValueHead

policy = AutoModelForCausalLMWithValueHead.from_pretrained("./sft-checkpoint")
ref    = AutoModelForCausalLMWithValueHead.from_pretrained("./sft-checkpoint")  # frozen

ppo = PPOTrainer(
    config=PPOConfig(learning_rate=1.41e-5, batch_size=64, init_kl_coef=0.05,
                     target_kl=6.0, adap_kl_ctrl=True),
    model=policy, ref_model=ref, tokenizer=tok,
)

for batch in dataloader:
    responses = ppo.generate(batch["query_ids"], max_new_tokens=128)
    rewards   = rm(torch.cat([batch["query_ids"], responses], dim=-1)).logits[:, 0]
    stats     = ppo.step(batch["query_ids"], responses, rewards)
    # stats includes: mean_kl, clip_frac, value_loss — the three PPO diagnostics
```

Tres cosas que la biblioteca hace por ti.`adap_kl_ctrl=True`se aplica el calendario de adaptación-β: si el KL observado excede `target_kl`El modelo de referencia está congelado por convención  no se pueden compartir accidentalmente los parámetros con `policy`Y el valor de la cabeza vive en la misma espina dorsal que la póliza (`AutoModelForCausalLMWithValueHead`se une una cabeza de MLP escalar), por lo que TRL informa `policy/kl`y `value/loss`por separado.

> Tengo tres cosas que hacer para ti.`adap_kl_ctrl=True`实现自适应 β 调度: si KL 超越目标则 β 翻倍, si inferior a la mitad则 β 减半―― referencia modelo según el acuerdo 结── valores y estrategias en el mismo ejecutivo─

## Las trampas

- **Over-optimization / reward hacking.**El RM es imperfecto .`π_θ`Los síntomas: la recompensa sube indefinidamente mientras que la evaluación humana califica plateaos o bajas.`β`, ampliar los datos de formación RM.
  **过度优化/奖励黑客。**RM 不完美;`π_θ`找到对抗性补全分高但质量差──症状: el premio continúa aumentando pero el porcentaje de evaluación humana se detiene o disminuye──修复:早停、提高 β、扩展 RM 训练数据──
- **Length hacking.**Las RM entrenadas en respuestas útiles a menudo recompensan implícitamente la longitud. La política aprende a cubrir las respuestas.
  **长度黑客。**En el curso de la formación de RM 常隐式奖励长度──策略学会填充回复──缓解: 长度归归化奖励或长度感知 RM──
- **Too-small RM.**El RM tiene que ser al menos tan grande como la póliza.
  **RM 太小。**RM al menos debe ser tan grande como la estrategia.
- **KL tuning.**El método estándar es un método de *adaptiva* β que se dirige a un KL fijo por paso.
  **KL 调优。**β 太低→漂移和奖励黑客──β 太高→ estrategia casi invariable──标准技巧是*自适应* β 目标为固定 KL──
- **Preference-data noise.**- 30% de las etiquetas humanas son ruidosas o ambigüas. Calibrar mediante la formación del RM en datos filtrados por acuerdo o utilizar una temperatura en BT.
  **偏好数据噪声。**Aproximadamente el 30% de los etiquetas humanas tienen ruido o borbullo.
- **Off-policy problems.**Los datos de PPO son ligeramente fuera de política después de la primera época.
  **离策略问题。**En la primera época, el PPO se convirtió en un pequeño grupo de estrategias de corte de la producción.

## Usalo con el marco de ejecución

El RLHF en 2026 se superponerá a capas:

> El RLHF de 2026 es de:

| Layer | Target | Method |
|-------|--------|--------|
| Layer / 层级 | Target / 目标 | Method / 方法 |
| Instruction following, helpfulness, harmlessness / 指令遵循、有用性、无害性 | Alignment / 对齐 | DPO (Phase 10 · 08) preferred over RLHF-PPO. |
| Reasoning correctness (math, code) / 推理正确性（数学、代码） | Capability / 能力 | GRPO with verifier reward (Phase 9 · 12). |
| Long-horizon multi-step tasks / 长视野多步任务 | Agentic / 代理 | PPO / GRPO with process reward models over steps. |
| Safety / refusal behavior / 安全/拒绝行为 | Safety / 安全 | RLHF-PPO with separate safety RM, or Constitutional AI. |
| Best-of-N at inference / 推理时 Best-of-N | Fast alignment / 快速对齐 | Use RM at decode time; no policy training needed. |
| Reward distillation / 奖励蒸馏 | Inference compute / 推理计算 | Train a small "reward head" on top of a frozen LM. |

El RLHF fue el método en 2022-2024. En 2026, las tuberías de alineación de producción son DPO-primero, PPO-solo para las etapas de RM-intensivas o críticas a la seguridad.

> RLHF en 2022-2024 años es* método* central.

## Envíe el producto .

Salvo como`outputs/skill-rlhf-architect.md`¿Qué es esto ?

```markdown
---
name: rlhf-architect
description: Design an RLHF / DPO / GRPO alignment pipeline for a language model, including RM, KL, and data strategy.
version: 1.0.0
phase: 9
lesson: 9
tags: [rl, rlhf, alignment, llm]
---

Given a base LM, a target behavior (alignment / reasoning / refusal / agent), and a preference or verifier budget, output:

1. Stage. SFT? RM? DPO? GRPO? With justification.
2. Preference or verifier source. Humans, AI feedback, rule-based, unit-test-pass, or reward distillation.
3. KL strategy. Fixed β, adaptive β, or DPO (implicit KL).
4. Diagnostics. Mean KL, reward stability, over-optimization guard (holdout human eval).
5. Safety gate. Red-team set, refusal rate, safety RM separate from helpfulness RM.

Refuse to ship RLHF-PPO without a KL monitor. Refuse to use an RM smaller than the target policy. Refuse length-only rewards. Flag any pipeline that does not hold back a blind human-eval set as lacking over-optimization protection.
```

## Los ejercicios.

1. **Easy.**Entrenemos el modelo de recompensa Bradley-Terry en .`code/main.py`En el caso de las piezas de la serie, el valor de la precisión de la medida es de un par de 100 pares.
2. **Medium.**Ejecutar el bucle de juguete PPO-RLHF con `β ∈ {0.0, 0.1, 1.0}`Para cada uno, compro RM puntuación vs KL-a-referencia sobre las actualizaciones. ¿Cuál ejecuta recompensa-hack?
3. **Hard.**Implemente DPO (perdida de probabilidad de preferencia en forma cerrada) en los mismos datos de preferencia y compare con el oleoducto RLHF-PPO en el cálculo utilizado y el puntaje final RM obtenido.

## Términos clave .

| Term | What people say | What it actually means |
|------|-----------------|-----------------------|
| RLHF | "Alignment RL" | Three-stage SFT + RM + PPO pipeline (Christiano 2017, Ouyang 2022). |
| Reward Model (RM) | "The scoring net" | Learned scalar function fit to pairwise preferences via Bradley-Terry. |
| Bradley-Terry | "Pairwise logistic loss" | `P(y_+ ≻ y_-) = σ(R(y_+) - R(y_-))`; the standard RM objective. |
| KL penalty | "Stay near the reference" | `β · KL(π_θ \|\| π_ref)` in the reward; the anti-reward-hacking regularizer. |
| Reward hacking | "Goodhart's law" | Policy exploits RM flaws; symptoms: reward up, human eval flat. |
| RLAIF | "AI-labeled preferences" | RLHF where labels come from another LM instead of humans. |
| PRM | "Process Reward Model" | Scores partial reasoning steps; used in reasoning pipelines. |
| Constitutional AI | "Anthropic's method" | AI-generated preferences guided by explicit rules. |

## Más Leer más Leer más

- [Christiano et al. (2017). Deep Reinforcement Learning from Human Preferences](https://arxiv.org/abs/1706.03741) el periódico que comenzó RLHF.
- [Ouyang et al. (2022). InstructGPT — Training language models to follow instructions with human feedback](https://arxiv.org/abs/2203.02155) la receta detrás de ChatGPT.
- [Stiennon et al. (2020). Learning to summarize with human feedback](https://arxiv.org/abs/2009.01325) RLHF anterior para su resumen.
- [Rafailov et al. (2023). Direct Preference Optimization](https://arxiv.org/abs/2305.18290) DPO; el incumplimiento posterior al RLHF en 2026.
- [Bai et al. (2022). Constitutional AI: Harmlessness from AI Feedback](https://arxiv.org/abs/2212.08073) RLAIF y circuito de autocrítica.
- [Anthropic RLHF paper (Bai et al. 2022). Training a Helpful and Harmless Assistant](https://arxiv.org/abs/2204.05862) el papel de HH.
- [Hugging Face TRL library](https://huggingface.co/docs/trl) producción `RewardTrainer`y `PPOTrainer`. Lea la fuente del entrenador para los detalles de KL y valor de cabeza.
- [Hugging Face — Illustrating Reinforcement Learning from Human Feedback](https://huggingface.co/blog/rlhf)por Lambert, Castricato, von Werra, Havrilla  el paseo canónico de la tubería de tres etapas con diagramas.
- [von Werra et al. (2020). TRL: Transformer Reinforcement Learning](https://github.com/huggingface/trl) la biblioteca; `examples/`tiene guiones de extremo a extremo RLHF para Llama, Mistral y Qwen.
- [Sutton & Barto (2018). Ch. 17.4 — Designing Reward Signals](http://incompleteideas.net/book/RLbook2020.pdf) la visión de la hipótesis de recompensa; condición esencial para pensar en el hacking de recompensa.
