# Optimisation des politiques proximales (PPO)

> A2C jette chaque déploiement après une mise à jour. PPO enveloppe le gradient de politique dans un ratio d'importance réduit afin que vous puissiez faire 10+ époques sur les mêmes données sans que la politique explose. Schulman et al. (2017).

> **【中文解读】**Le PPO utilise le taux de tactile de taille pour emballer les mêmes données, ce qui permet de faire 10 ou plus de renouvellements et les stratégies ne explosent pas.

> **【拓展：PPO 与 ChatGPT】**Le PPO est l'algorithme central de l'entraînement de ChatGPT RLHF. InstructionGPT(2022) Utilisez le PPO pour faire des préférences humaines à la GPT-3, c'est la technologie derrière le ChatGPT. La stabilité et la simplicité du PPO en font la première option de l'industrie.

**Type:** Build | **类型:** 动手
**Languages:** Python | **语言:** Python
**Prerequisites:** Phase 9 · 06 (REINFORCE), Phase 9 · 07 (Actor-Critic) | **前置知识:** Phase 9 · 06 (REINFORCE), Phase 9 · 07 (Actor-Critic)
**Time:** ~75 minutes | **时间:** ~75 分钟

## Le problème , l' introduction du problème

A2C (leçon 07) est sur la politique: le gradient `E_{π_θ}[A · ∇ log π_θ]`nécessite des données prélevées à partir du * courant* `π_θ`- Prenez une mise à jour, et `π_θ`Les données que vous avez utilisées sont désormais hors politique.

> A2C (Létion 07) est en ligne`E_{π_θ}[A · ∇ log π_θ]`要求从*当前* `π_θ`Une fois de plus.`π_θ`改变; vous avez utilisé des données qui sont devenues des stratégies ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙                                                                                                                                                                                                                                                                                                                                                           

Les déploiements sont chers. Sur Atari, un déploiement sur 8 envs × 128 étapes = 1024 transitions et une douzaine de secondes de temps environnemental. Jeter cela après un pas de gradient est gaspillé.

> Le déploiement est très coûteux. Sur Atari, 8 environments × 128 étapes = 1024 fois de transfert et 10 secondes de temps environnementaux.

L'optimisation des politiques de la région de confiance (TRPO, Schulman 2015) a été la première solution: restreindre chaque mise à jour afin que la divergence KL entre les anciennes et les nouvelles politiques reste inférieure `δ`- En théorie propre, mais nécessite une solution de gradient conjugué par mise à jour.

> La première révision de la loi de 2015 sur les droits de l'homme est la révision de la loi de 2015 sur les droits de l'homme.`δ`En théorie, il est beau, mais chaque mise à jour nécessite une demande de résolution commune.

PPO (Schulman et coll. 2017) remplace la contrainte de la région de confiance avec un objectif simple coupé. Une ligne de code supplémentaire. Dix époques par déploiement. Pas de gradients conjugués.

> PPO(Schulman 等人 2017) utilise un simple objectif de coupe pour remplacer le hard-trust domain.

> **【中文解读】**Le taux de réussite de la PPO est de 0,0 à 0,0 fois plus élevé que le taux de réussite de la PPO. Le taux de réussite de la PPO est de 0,0 à 0,0 fois plus élevé que le taux de réussite de la PPO.

> **【拓展：PPO 之外的选择——DPO 与 GRPO】**Bien que le PPO soit encore une option par défaut en 2026, le programme de remplacement est en train de se développer.

## Le concept de base.

![PPO clipped surrogate objective: ratio clipping at 1 ± ε](../assets/ppo.svg)

**The importance ratio.**

`r_t(θ) = π_θ(a_t | s_t) / π_{θ_old}(a_t | s_t)`

Il s'agit du ratio de probabilité entre la nouvelle politique et la politique qui a recueilli les données. `r_t = 1`Ça ne change rien.`r_t = 2`Cela signifie que la nouvelle politique est deux fois plus susceptible de prendre`a_t`comme les anciens.

> **重要性比率。**La nouvelle stratégie et la collecte de données sont similaires.`r_t = 1`Indique pas de changement.`r_t = 2`Indiquer une nouvelle stratégie`a_t`La probabilité est deux fois supérieure à l'ancienne stratégie.

**The clipped surrogate.**

`L^{CLIP}(θ) = E_t [ min( r_t(θ) A_t, clip(r_t(θ), 1-ε, 1+ε) A_t ) ]`

Deux termes:

- Si l' avantage `A_t > 0`et le ratio essaie de passer `1 + ε`, le clip aplatit le gradient  ne pousse pas une bonne action plus loin que `+ε`au-dessus de la vieille probabilité.
- Si l' avantage `A_t < 0`et le ratio essaie de passer `1 - ε`(ce qui signifie que nous rendrions une mauvaise action plus probable par rapport à sa réduction coupée), le clip coupe le gradient  ne poussent pas une mauvaise action en dessous `-ε`- Je suis désolé .

Le `min`Il s'agit de la direction opposée: si le ratio a déménagé dans la direction * bénéfique*, vous obtenez toujours le gradient (pas de coupure sur le côté qui vous ferait mal).

Typique`ε = 0.2`. Tracer l'objectif en fonction de `r_t`: une fonction linéaire en morceaux avec un toit plat sur le "bon côté" et un plancher plat sur le "mauvais côté".

> **裁剪代理。**两项: si les avantages sont positifs et le taux dépasse `1 + ε`Ne pas faire de bonnes actions plus fort que les probabilités .`+ε`更多── si les avantages sont négatifs et le taux est inférieur à `1 - ε`Ne réduisez pas les mauvaises actions.`-ε`更多──typical `ε = 0.2`Il y a une autre.

> **【中文解读】**L'intuition du mécanisme de coupe de la PPO:epsilon=0.2 signifie que la stratégie change au plus 20% par mise à jour. Si un mouvement est bon, la probabilité augmente au plus de 20%; si un mouvement est mauvais, la probabilité diminue au plus de 20%. Cela empêche l'oubli catastrophique.

**The full PPO loss.**

`L(θ, φ) = L^{CLIP}(θ) - c_v · (V_φ(s_t) - V_t^{target})² + c_e · H(π_θ(·|s_t))`

La même structure acteur-critique que l'A2C. Trois coefficients, généralement `c_v = 0.5`- Je suis là .`c_e = 0.01`- Je suis là .`ε = 0.2`- Je suis désolé .

> **完整的 PPO 损失。**A2C comparable à Actor-Critic structure ∼ trois系数, généralement `c_v = 0.5`- Je suis là.`c_e = 0.01`- Je suis là.`ε = 0.2`Il y a une autre.

**The training loop.**

1. Rassembler`N × T`transitions à travers `N`environnements parallèles pour `T`chaque étape.
2. Comptez les avantages (GAE), congélez-les comme constantes.
3. Le gel`π_{θ_old}`comme une capture d'écran de courant `π_θ`- Je suis désolé .
4. Pour `K`Les épisodes de la première série de l'époque sont les suivants:`(s, a, A, V_target, log π_old(a|s))`- Le numéro de la liste:
   - Compte `r_t(θ) = exp(log π_θ(a|s) - log π_old(a|s))`- Je suis désolé .
   - Appliquer `L^{CLIP}`+ perte de valeur + entropie.
   - Un pas de plus.
5. Jetez le déploiement et retournez à l'étape 1.

`K = 10`Les données de l'analyse de la quantité de données de l'indice de référence sont très précises, et les mini-parts de 64 sont un ensemble standard d'hyperparamètres.

> **训练循环。**收集 → 计算 GAE 优势 → 结旧策略 → K 轮更新 → 丢弃数据──`K = 10`Et 64 de petits lots sont des superparametres standard.

**KL-penalty variant.**Le document original proposait une alternative à l' utilisation d' une pénalité KL adaptative: `L = L^{PG} - β · KL(π_θ || π_old)`avec `β`La version de coupage est devenue dominante; la variante KL survit dans le RLHF (où KL à la politique de référence est une contrainte séparée que l'on veut toujours de toute façon).

> **KL 惩罚变体。**Le premier article propose une alternative à l'utilisation de l'auto-adaptation KL 惩罚.

## Construisez-le et mettez-le en œuvre.
```figure
ppo-clip
```

## Faites-le

### Étape 1: capture `log π_old(a | s)`au moment du déploiement

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

L'instantané est pris une fois, au moment du déploiement.

> 快照在推出时拍摄一次──在更新时代 期间不变──

### Étape 2: calculer les avantages de l'AEG (leçon 07)

La même chose que l'A2C. Normalize à travers le lot.

> Avec A2C parallèlement.

### Étape 3: Mise à jour de substitution coupée

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

Le modèle "gradient réduit → zéro" est au cœur de la PPO. Si la nouvelle politique a déjà dérivé trop loin dans la direction bénéfique, la mise à jour s'arrête.

> Le modèle "coupage → zéro degré" est au cœur de la PPO. Si une nouvelle stratégie s'est détournée trop loin dans une direction favorable, la mise à jour s'arrête.

### Étape 4: valeur et entropie

Ajouter des MSE standard à la cible critique et un bonus d'entropie sur l'acteur, le même que A2C.

> À la critique objectif ajouter des normes MSE, à l'acteur 添加奖励, par rapport à A2C

### Étape 5: diagnostic

Trois choses à regarder à chaque mise à jour:

> Chaque mise à jour doit être surveillée par trois choses:

- **Mean KL** `E[log π_old - log π_θ]`- Je devrais rester .`[0, 0.02]`Si ça passe ,`0.1`, réduire `K_EPOCHS`ou `LR`- Je suis désolé .
  **平均 KL。**Il faut rester là.`[0, 0.02]` Si plus `0.1`, réduit `K_EPOCHS`Ou `LR`Il y a une autre.
- **Clip fraction** la fraction des échantillons dont le ratio se trouve à l'extérieur `[1-ε, 1+ε]`- Ça devrait être .`~0.1-0.3`Si vous ...`~0`, le clip ne déclenche jamais → augmentation `LR`ou `K_EPOCHS`Si vous ...`~0.5+`Vous les faites trop bas.
  **裁剪比例。**Rate de dépassement`[1-ε, 1+ε]`Le taux de participation est de 0,5%`~0.1-0.3`Il y a une autre.
- **Explained variance** `1 - Var(V_target - V_pred) / Var(V_target)`Il devrait grimper vers 1 à mesure que le critique apprend.
  **解释方差。**Critic Quality Index: devrait suivre la tendance de la formation critique

## Les pièges

- **Clip coefficient mistuned.** `ε = 0.2`C'est la norme de fait.`0.1`rend les mises à jour trop timides; `0.3+`Il y a une instabilité.
  **裁剪系数调错。** `ε = 0.2`C'est une réalité.`0.1`太保守;`0.3+`导致不稳定──
- **Too many epochs.** `K > 20`La politique de l'Union européenne est en train de détériorer de manière régulière la stabilité de l'Union européenne.`π_old`- Époques de cap, en particulier pour les grands réseaux.
  **太多 epoch。** `K > 20`Il est toujours instable, parce que la stratégie est détournée.`π_old`Il y a beaucoup de temps, surtout de temps.
- **No reward normalization.**Les grandes échelles de récompense entrent dans la gamme des clips.
  **没有奖励归一化。**Les prix de la récompense sont les prix de la récompense.
- **Forgetting advantage normalization.**La normalisation par lot de zéro moyenne/unit-std est standard.
  **忘记优势归一化。**Chaque lot de valeur moyenne / unité standard est un standard.
- **Learning rate not decayed.**La PPO bénéficie d'une décomposition de la LR linéaire à zéro.
  **学习率未衰减。**Le PPO de LR de ligne  déclin à zéro  bénéfice ∞
- **Importance ratio math errors.**Toujours .`exp(log_new - log_old)`pour la stabilité numérique, non `new / old`- Je suis désolé .
  **重要性比率数学错误。**始终使用 `exp(log_new - log_old)`La sécurité de la valeur est stable, et non pas `new / old`Il y a une autre.
- **Wrong gradient sign.**Maximiser la mère porteuse = *minimiser* `-L^{CLIP}`Un panneau inversé est le virus le plus courant.
  **梯度符号错误。**Le maximum de représentants = * minimisation* `-L^{CLIP}`◊ 符号反转为 PPO 最常见 bug──

## Utilisez-le avec le cadre de réalisation

PPO est l'algorithme RL par défaut de 2026 sur un nombre surprenant de domaines:

> Le PPO est un algorithme de RL standard de nombreux domaines de 2026:

| Use case | PPO variant |
|----------|-------------|
| Use case / 用例 | PPO variant / PPO 变体 |
| MuJoCo / robotics control / MuJoCo/机器人控制 | PPO with Gaussian policy, GAE(0.95) / 高斯策略的 PPO，GAE(0.95) |
| Atari / discrete games / Atari/离散游戏 | PPO with categorical policy, rolling 128-step rollouts / 分类策略的 PPO |
| RLHF for LLMs / LLM 的 RLHF | PPO with KL penalty to reference model, reward from RM at end of response / 带 KL 惩罚的 PPO |
| Large-scale game agents / 大规模游戏 Agent | IMPALA + PPO (AlphaStar, OpenAI Five) |
| Reasoning LLMs / 推理 LLM | GRPO (Lesson 12) — PPO variant without critic / 无 Critic 的 PPO 变体 |
| Preference-only data / 仅偏好数据 | DPO — closed-form collapsing of PPO+KL, no online sampling / 闭式 PPO+KL 折叠 |

La forme de PPO *perte*  coupée surrogée + valeur + entropie  est l'échafaudage pour DPO, GRPO et presque tous les pipelines RLHF.

> Le PPO de la forme* perte* coupe de l'agent + 值 + 是 DPO、GRPO 和几乎所有RLHF 流水线的脚手架──

## Envoyez-le . Produit .

- Je ne sais pas .`outputs/skill-ppo-trainer.md`- Le numéro de la liste:

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

## Les exercices

1. **Easy.**Réglez le PPO sur 4×4 GridWorld avec `ε=0.2, K=4`- Comparez l'efficacité de l'échantillon à A2C (une époque par déploiement) à des étapes d'environnement correspondantes.
2. **Medium.**- Le balayage .`K ∈ {1, 4, 10, 30}`- Retour de l'intrigue vers l'env étapes et suivre la moyenne KL par mise à jour.`K`KL explose sur cette tâche ?
3. **Hard.**Le remplaçant coupé est remplacé par une pénalité KL adaptative (`β`double si `KL > 2·target`, réduit de moitié si `KL < target/2`) Comparer le rendement final, la stabilité et la non-clip.

## Les termes clés

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

## Encore une lecture

- [Schulman et al. (2017). Proximal Policy Optimization Algorithms](https://arxiv.org/abs/1707.06347)- Le journal.
- [Schulman et al. (2015). Trust Region Policy Optimization](https://arxiv.org/abs/1502.05477) TRPO, prédécesseur de PPO.
- [Andrychowicz et al. (2021). What Matters In On-Policy RL? A Large-Scale Empirical Study](https://arxiv.org/abs/2006.05990) tous les hyperparametres de PPO supprimés.
- [Ouyang et al. (2022). Training language models to follow instructions with human feedback](https://arxiv.org/abs/2203.02155) InstructGPT; la recette de PPO-in-RLHF.
- [OpenAI Spinning Up — PPO](https://spinningup.openai.com/en/latest/algorithms/ppo.html) exposition moderne propre avec PyTorch.
- [CleanRL PPO implementation](https://github.com/vwxyzjn/cleanrl) référence PPO à fichier unique utilisé par de nombreux documents.
- [Hugging Face TRL — PPOTrainer](https://huggingface.co/docs/trl/main/en/ppo_trainer) la recette de production de PPO sur les modèles linguistiques; lire à côté de la leçon 09 (RLHF).
- [Engstrom et al. (2020). Implementation Matters in Deep Policy Gradients](https://arxiv.org/abs/2005.12729) le document "37 optimisations au niveau du code"; quelles astuces PPO sont portables et quelles sont folklore.
