# Acteur-Critique  A2C et A3C  Actors-Commentateurs  A2C et A3C

> La force est bruyante, ajoutez un critique qui apprend.`V̂(s)`A2C le fait en synchronisation, A3C le fait en travers de fils. Les deux sont le modèle mental de chaque méthode moderne de RL profonde.

> **【中文解读】**RÉINFORCE 方差太大──加入一个"评论家"(Critique) apprendre V̂(s), en l'utilisant comme base de la construction de la fonction d'avantage A = G - V̂(s), l'attente ne change pas mais la différence est considérablement réduite──

**Type:** Build | **类型:** 动手
**Languages:** Python | **语言:** Python
**Prerequisites:** Phase 9 · 04 (TD Learning), Phase 9 · 06 (REINFORCE) | **前置知识:** Phase 9 · 04 (TD 学习), Phase 9 · 06 (REINFORCE)
**Time:** ~75 minutes | **时间:** ~75 分钟

## Le problème , l' introduction du problème

La vanille de la force de renversement fonctionne, mais sa variance est terrible.`G_t`Il peut s'élever sur un facteur de 10 entre les épisodes.`∇ log π`et la moyenne produit un estimateur de gradient qui prend des milliers d'épisodes pour déplacer la politique à la même distance que vous pourriez le déplacer avec beaucoup moins de mises à jour DQN.

> La réinforcement est efficace, mais la différence est très mauvaise.`G_t`Dans le temps, le bruit peut être multiplié par 10.`∇ log π`En revanche, les estimateurs de degrés de formation ont besoin de milliers de revirements pour pouvoir déployer des stratégies avec moins de DQN.

La variance provient de l'utilisation de rendements bruts.`b(s_t)` toute fonction d'état, y compris une valeur apprise  l'attente est inchangée et la variance diminue.`V̂(s_t)`La quantité se multiplie .`∇ log π`est l'avantage:

`A(s, a) = G - V̂(s)`

> 方差来自使用原始回报──如果减去基线 `b(s_t)` Toute fonction d'état, y compris la valeur de l'apprentissage  l'attente ne change pas mais la différence diminue                                                                                                                                                                                                                                              `V̂(s_t)`Je suis en train de le faire.`∇ log π`Le nombre est de l'avantage.

Une action est bonne si elle produit un rendement supérieur à la moyenne; mauvaise si elle est inférieure. REINFORCE avec un critique érudit est *acteur-critique*. Le critique donne à l'acteur un professeur de faible variance. C'est chaque méthode de politique profonde après 2015 (A2C, A3C, PPO, SAC, IMPALA).

> 动作好如果产生高于平均的回报;差如果低于──带学习批评的 REINFORCE 就是 *Actor-Critic*──Critic 给 Actor一个低方差的老师──这是2015年后每深度策略方法(A2C、A3C、PPO、SAC、IMPALA)──

## Le concept de base.

![Actor-critic: policy net plus value net, TD residual as advantage](../assets/actor-critic.svg)

**Two networks, one shared loss:**

> **两个网络，一个共享损失：**

- **Actor** `π_θ(a | s)`Le programme de formation est un programme de formation de base.
  **Actor** `π_θ(a | s)`Le niveau de formation est le niveau de formation.
- **Critic** `V_φ(s)`Les résultats de l'enquête ont été évalués en fonction des résultats obtenus.`(V_φ(s) - target)²`- Je suis désolé .
  **Critic** `V_φ(s)`Les résultats de l'évaluation des résultats de l'état sont attendus.`(V_φ(s) - target)²`Il y a une autre.

**The advantage.**Deux formulaires standard:

> **优势函数。**两种标准形式:

- *Avantage du MC*`A_t = G_t - V_φ(s_t)`- Inpartieux, plus varié.
  *MC 优势:* 无偏,方差较高──
- *Avantages du TD*`A_t = r_{t+1} + γ V_φ(s_{t+1}) - V_φ(s_t)`. Utilisation biaisée `V_φ`La variance est beaucoup plus faible.`δ_t`- Je suis désolé .
  *TD 优势:* 有偏差(使用 `V_φ`),方差远低──也称为 *TD残差* `δ_t`Il y a une autre.

**n-step advantage.**Interpolez les deux:

`A_t^{(n)} = r_{t+1} + γ r_{t+2} + … + γ^{n-1} r_{t+n} + γ^n V_φ(s_{t+n}) - V_φ(s_t)`

`n = 1`est une TD pure. `n = ∞`La plupart des mises en œuvre utilisent `n = 5`pour Atari, `n = 2048`Pour le PPO sur MuJoCo.

> **n 步优势。**Entre les deux, il y a une valeur de mise en valeur.`n = 1`C'est une pure TD.`n = ∞`Oui, la plupart des utilisateurs utilisent Atari.`n = 5`Je suis en train de faire une petite histoire.`n = 2048`Il y a une autre.

**Generalized Advantage Estimation (GAE).**Schulman et coll. (2016) ont proposé une moyenne pondérée exponentielle sur tous les avantages de l'étape n:

`A_t^{GAE} = Σ_{l=0}^{∞} (γλ)^l δ_{t+l}`

avec `λ ∈ [0, 1]`- Je suis là .`λ = 0`est TD (faible variance, haut biais). `λ = 1`est MC (haute variance, impartiale). `λ = 0.95`est la tonne  par défaut 2026 jusqu'à ce que le cadran biais/variance soit là où vous le voulez.

> **【中文解读】**GAE(广义优势估算) est une amélioration clé de l'acteur-critique: par indexation de la valeur moyenne de tous les niveaux de l'avantage, on trouve le meilleur équilibre entre les différences et les différences.

> **【拓展：GAE 在 RLHF 中的应用】**Le programme de formation de PPO de ChatGPT utilise la fonction de l'avantage de calcul GAE. Dans le cadre de l'LLM, "état" est la séquence de jetons générée, "动作" est le prochain jeton, "récompenses" proviennent du modèle de récompense.

**A2C: synchronous advantage actor-critic.**Rassembler`T`pas à travers `N`Environments parallèles, calculer les avantages pour chaque étape, mettre à jour l'acteur et le critique sur le lot combiné, répète, le frère plus simple et plus évolutif d'A3C.

> **A2C：同步优势 Actor-Critic。**Dans le`N`个并行环境中收集                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                       `T`步──计算每步优势──在合并批次上更新 Actor 和 Critic──重复──A3C's 更多简单,更多可扩展的兄弟──

**A3C: asynchronous advantage actor-critic.**Mnih et coll. (2016). Spawn `N`Chaque travailleur calcule les gradients localement sur son propre déploiement, puis les applique de manière asynchrone à un serveur de paramètres partagé. Aucun tampon de répétition n'est nécessaire  les travailleurs se décorèrent en exécutant différentes trajectoires. A3C a prouvé que vous pouviez vous entraîner sur des processeurs à grande échelle. En 2026, A2C basé sur des processeurs parallèles en série (environnements parallèles en série) domine parce que les processeurs veulent de grands lots.

> **A3C：异步优势 Actor-Critic。**Mnih 等人 (2016) ⋅ lancement `N`个工作线程,每个运行一个环境――每个工作线程在本地计算梯度,然后分步应用到共享参数服务器――不需要回放缓冲区工作线程通过运行不同轨迹来相关――2026年, A2C basé sur GPU 占主导地位,因为 GPU 需要大批量――

**The combined loss.**

`L(θ, φ) = -E[ A_t · log π_θ(a_t | s_t) ]  +  c_v · E[(V_φ(s_t) - G_t)²]  -  c_e · E[H(π_θ(·|s_t))]`

Trois termes: perte de la politique, régression de la valeur, bonus d'entropie. `c_v ~ 0.5`- Je suis là .`c_e ~ 0.01`sont des points de départ canoniques.

> **组合损失。**Trois éléments: stratégie de dégradation, de retour à la valeur, de récompense.`c_v ~ 0.5`- Je suis là.`c_e ~ 0.01`C'est une valeur de départ typique.

> **【中文解读】**L'acteur-critique est un compositeur de la stratégie.

> **【拓展：GAE→PPO→RLHF】**L'AEG (Grande valeur de l'avantage estimation) est le composant central de la PPO, tandis que la PPO est l'algorithme standard de l'entraînement ChatGPT RLHF ⋅λ=0.95 est la valeur par défaut de 2026 pour obtenir un équilibre entre les différences et les différences.

## Construisez-le et mettez-le en œuvre.
```figure
actor-critic
```

## Faites-le

### Étape 1: un critique

Le critique linéaire `V_φ(s) = w · features(s)`mis à jour avec MSE:

```python
def critic_update(w, x, target, lr):
    v_hat = dot(w, x)
    err = target - v_hat
    for j in range(len(w)):
        w[j] += lr * err * x[j]
    return v_hat
```

Sur une enveloppe tabulaire, le critique converge en quelques centaines d'épisodes. sur Atari, remplacer le critique linéaire par une tête de valeur CNN partagée.

> 线性批评  rédaction`V_φ(s) = w · features(s)`Utilisation de la mise à jour de la MSE.

### Étape 2: avantage de n-étape

Compte tenu de la longueur de la déploiement `T`et une finale à la traîne`V(s_T)`- Le numéro de la liste:

```python
def compute_advantages(rewards, values, gamma=0.99, lam=0.95, last_value=0.0):
    advantages = [0.0] * len(rewards)
    gae = 0.0
    for t in reversed(range(len(rewards))):
        next_v = values[t + 1] if t + 1 < len(values) else last_value
        delta = rewards[t] + gamma * next_v - values[t]
        gae = delta + gamma * lam * gae
        advantages[t] = gae
    returns = [a + v for a, v in zip(advantages, values)]
    return advantages, returns
```

`returns`est la cible critique. `advantages`est ce qui se multiplie `∇ log π`- Je suis désolé .

> `returns`C'est un objectif critique.`advantages`Oui, c'est le cas.`∇ log π`La quantité de

### Étape 3: mise à jour combinée

```python
for step_i, (x, a, _r, probs) in enumerate(traj):
    adv = advantages[step_i]
    target_v = returns[step_i]

    # critic
    critic_update(w, x, target_v, lr_v)

    # actor
    for i in range(N_ACTIONS):
        grad_logpi = (1.0 if i == a else 0.0) - probs[i]
        for j in range(N_FEAT):
            theta[i][j] += lr_a * adv * grad_logpi * x[j]
```

On-policy, un déploiement par mise à jour, taux d'apprentissage séparés pour acteur et critique.

> Chaque année, les acteurs et les critiques utilisent différents taux d'apprentissage.

### Étape 4: parallélisation (A3C contre A2C)

- **A3C:**tourner vers le haut `N`Chaque course est en mode environnemental et en mode avant.
- **A2C:**courir`N`Env instances dans un seul processus, enchaînement des observations en un `[N, obs_dim]`Les données de l'échantillon sont plus précises, plus précises, plus faciles à raisonner.

Notre code de jouet est un seul fil pour la clarté; réécrire à A2C en lots est trois lignes de numpy.

> Notre code de jouets est simple pour garder la clarté; réécrire pour la quantité A2C ne nécessite que trois lignes de numpy.

## Les pièges

- **Critic bias before actor gradient.**Si le critique est aléatoire, sa ligne de départ est non informative et vous vous entraînez sur le bruit pur. Réchauffez le critique pendant quelques centaines d'étapes avant d'activer le gradient de politique, ou utilisez un taux d'apprentissage lent des acteurs.
  **Actor 梯度之前的 Critic 偏差。**Si le critique est aléatoire, il n'y a pas de quantité d'information, vous vous entraînez sur le bruit pur.
- **Advantage normalization.**Normalement, les avantages sont réduits à zéro moyenne/unit-std par lot.
  **优势归一化。**Chaque lot sera unifié en valeurs moyennes/unités standard de différence.
- **Shared trunk.**Utilisez un extracteur de fonctionnalités partagées pour les acteurs et les critiques sur les entrées d'image.
  **共享主干。**图像输入时使用共享特征提取器──分开的头──共享特征同时从两个损失中获益──
- **On-policy contract.**A2C réutilise les données pour une mise à jour. Plus et votre gradient est biaisé (correction d'importance-échantillonnage est ce que PPO ajoute).
  **在线策略约束。**A2C 恰好用数据做一次更新.
- **Entropy collapse.**Sans`c_e > 0`La politique devient presque déterministe dans quelques centaines de mises à jour et cesse d'explorer.
  **熵坍缩。**Il n' y a pas de`c_e > 0`La stratégie a été mise à jour plusieurs centaines de fois et a été mise à jour de manière plus précise.
- **Reward scale.**Les magnitudes d'avantage dépendent de l'échelle de récompense. Normalize les récompenses (par exemple, la division run-std) pour des magnitudes de gradient cohérentes entre les tâches.
  **奖励尺度。**Le niveau de la qualité dépend de la mesure de la récompense.

## Utilisez-le avec le cadre de réalisation

A2C/A3C sont rarement le choix final en 2026 mais ils sont l'architecture que tout raffinera plus tard:

> A2C/A3C en 2026 sont rarement les choix finaux, mais ils sont ensuite toutes des méthodes élaborées:

| Method | Relation to A2C |
|--------|----------------|
| Method / 方法 | Relation to A2C / 与 A2C 的关系 |
| PPO | A2C + clipped importance ratio for multi-epoch updates / A2C + 裁剪重要性比率用于多轮更新 |
| IMPALA | A3C + V-trace off-policy correction / A3C + V-trace 离策略修正 |
| SAC (Phase 9 · 07) | Off-policy A2C with a soft-value critic (next lesson) / 离策略 A2C + 软值 Critic |
| GRPO (Phase 9 · 12) | A2C without the critic — group-relative advantage / 无 Critic 的 A2C——组相对优势 |
| DPO | A2C collapsed into a preference-ranking loss, no sampling / 折叠为偏好排名损失的 A2C |
| AlphaStar / OpenAI Five | A2C with league training + imitation pre-training / A2C + 联盟训练 + 模仿预训练 |

Si vous voyez "avantage" dans un article de 2026, pensez à un critique acteur.

> Si vous voyez "Unexits" dans un article de 2026 , pensez à l'acteur-critique.

## Envoyez-le . Produit .

- Je ne sais pas .`outputs/skill-actor-critic-trainer.md`- Le numéro de la liste:

```markdown
---
name: actor-critic-trainer
description: Produce an A2C / A3C / GAE configuration for a given environment, with advantage estimation and loss weights specified.
version: 1.0.0
phase: 9
lesson: 7
tags: [rl, actor-critic, gae]
---

Given an environment and compute budget, output:

1. Parallelism. A2C (GPU batched) vs A3C (CPU async) and the number of workers.
2. Rollout length T. Steps per env per update.
3. Advantage estimator. n-step or GAE(λ); specify λ.
4. Loss weights. `c_v` (value), `c_e` (entropy), gradient clip.
5. Learning rates. Actor and critic (separate if using).

Refuse single-worker A2C on environments with horizon > 1000 (too on-policy, too slow). Refuse to ship without advantage normalization. Flag any run with `c_e = 0` and observed entropy < 0.1 as entropy-collapsed.
```

## Les exercices

1. **Easy.**Traîneur-critique acteur avec avantage MC (`G_t - V(s_t)`Comparer l'efficacité de l'échantillon à la base moyenne de REINFORCE avec fonctionnement de la leçon 06.
2. **Medium.**Passer à l'avantage de la TD (`r + γ V(s') - V(s)`La différence entre les lots d'avantage est mesurée.
3. **Hard.**Implémentation de l'AEA (L).`λ ∈ {0, 0.5, 0.9, 0.95, 1.0}`Où est le point de vue de la différence pour cette tâche ?

## Les termes clés

| Term | What people say | What it actually means |
|------|-----------------|-----------------------|
| Actor | "The policy net" / 演员（策略网络） | `π_θ(a\|s)`, updated by policy gradient. |
| Critic | "The value net" / 评论家（值网络） | `V_φ(s)`, updated by MSE regression to returns / TD targets. |
| Advantage | "How much better than average" / 优势函数 | `A(s, a) = Q(s, a) - V(s)` or its estimators. Multiplier for `∇ log π`. |
| TD residual | "δ" / TD 残差 | `δ_t = r + γ V(s') - V(s)`; one-step advantage estimate. |
| GAE | "The interpolation knob" / 广义优势估计 | Exponentially weighted sum of n-step advantages, parameterized by `λ`. |
| A2C | "Synchronous actor-critic" / 同步演员-评论家 | Batched across envs; one gradient step per rollout. |
| A3C | "Async actor-critic" / 异步演员-评论家 | Worker threads push gradients to a shared param server. Original paper; less common in 2026. |
| Bootstrap | "Use V at the horizon" / 自举截断 | Truncate the rollout, add `γ^n V(s_{t+n})` to close the sum. |

## Encore une lecture

- [Mnih et al. (2016). Asynchronous Methods for Deep Reinforcement Learning](https://arxiv.org/abs/1602.01783) A3C, le papier critique acteur-critique original.
- [Schulman et al. (2016). High-Dimensional Continuous Control Using Generalized Advantage Estimation](https://arxiv.org/abs/1506.02438) GAE.
- [Sutton & Barto (2018). Ch. 13 — Actor-Critic Methods](http://incompleteideas.net/book/RLbook2020.pdf) fondations; associer ceci au chapitre 9 sur l'approximation des fonctions lorsque le critique est un réseau neuronal.
- [Espeholt et al. (2018). IMPALA](https://arxiv.org/abs/1802.01561) critique distribuée d'acteurs évolutifs avec correction hors politique de V-trace.
- [OpenAI Baselines / Stable-Baselines3](https://stable-baselines3.readthedocs.io/) des mises en œuvre de production A2C/PPO qui méritent d'être lues.
- [Konda & Tsitsiklis (2000). Actor-Critic Algorithms](https://papers.nips.cc/paper/1786-actor-critic-algorithms) le résultat de convergence fondamental de la décomposition acteur-critique à deux échelles.
