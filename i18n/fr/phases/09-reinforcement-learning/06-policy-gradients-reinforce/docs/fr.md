# Politique Gradient  RENFORCE à partir de zéro   stratège                                                                                                                                                                                                                                                     

> Arrêtez d'estimer la valeur. Paramétrez directement la politique, calculez le gradient du rendement attendu, faites des pas en haut. Williams (1992) l'a écrit dans un théorème. C'est pourquoi PPO, GRPO et chaque boucle LLM RL existent.

> **【中文解读】**La fonction de réévaluation, une stratégie de réévaluation directe π_θ(a des états), calculant l'attente de récompense de la tendance ou de la tendance à la hausse.`∇J(θ) = E[G · ∇log π_θ(a|s)]` C'est la raison pour laquelle le PPO, le GRPO et tous les grands modèles de formation RL existent.

**Type:** Build | **类型:** 动手
**Languages:** Python | **语言:** Python
**Prerequisites:** Phase 3 · 03 (Backpropagation), Phase 9 · 03 (Monte Carlo), Phase 9 · 04 (TD Learning) | **前置知识:** Phase 3 · 03 (反向传播), Phase 9 · 03 (蒙特卡洛), Phase 9 · 04 (TD 学习)
**Time:** ~75 minutes | **时间:** ~75 分钟

## Le problème , l' introduction du problème

Q-learning et DQN paramétrisent la fonction *value*.`argmax Q`Il est bon pour les actions discrètes et les états discrets.`argmax`sur un couple à 10 dimensions?) ou lorsque vous voulez une politique stochastique (`argmax`est déterministe par construction).

> Q-apprentissage et DQN 参数化*value*`argmax Q`选择动作── ceci est un problème pour les mouvements séparés et les mouvements séparés.`argmax`• ou besoin de stratégie`argmax`Bien sûr, c'est certain, on est en train de s'effondrer.

Les gradients de politique paramétrisent plutôt la politique. `π_θ(a | s)`Le taux de rendement attendu est calculé par rapport à la valeur de l'échantillon.`θ`- Passer le mont.`argmax`Pas de récursion Bellman, juste une ascension de gradient.`J(θ) = E_{π_θ}[G]`- Je suis désolé .

> 策略梯度改为参数化*策略*:`π_θ(a | s)`Il s'agit d'un réseau de distribution de débit de données.`θ`Il n'y a pas besoin de la même chose.`argmax`Il n'y a pas besoin de Bellman.`J(θ) = E_{π_θ}[G]`Il y a une augmentation de la taille.

Le théorème de la REINFORCE (Williams 1992) vous dit que ce gradient est calculé: `∇J(θ) = E_π[ G · ∇_θ log π_θ(a | s) ]`- Exécutez un épisode, comptez le rendement, multipliez par`∇ log π_θ(a | s)`Je suis en moyenne, à chaque étape, à chaque grade.

> RENFORCE DATA (Williams 1992) nous dit que ce degré est calculé:`∇J(θ) = E_π[ G · ∇_θ log π_θ(a | s) ]`◊运行一个回合――计算回报――每步乘以 `∇ log π_θ(a | s)`◊取平均──梯度上升──完成──

Chaque algorithme LLM-RL en 2026  PPO, DPO, GRPO  est un raffinement de REINFORCE.

> En 2026, chaque LLM-RL 算法 PPO、DPO、GRPO sont toutes des éliminations de REINFORCE.

> **【中文解读】** idéologie centrale de la gradience de stratégie: optimiser directement les paramètres de stratégie θ, faire augmenter la probabilité de démarrage de l'action de haut rendement  diminuer la probabilité de démarrage de l'action de bas rendement `∇log π`C'est le "directionnement de la stratégie", multiplié par le "report" G'est le "courir dans la bonne direction".

> **【拓展：PPO→ChatGPT对齐】**Le RLHF de ChatGPT est un algorithme de PPO, en fait c'est REINFORCE + Critic 基线 + 信赖域剪.`loss = -advantage * log_prob`Cette ligne de code, apparaissant actuellement dans presque tous les grands modèles RL de 2026  entraînement de script.

## Le concept de base.

![Policy gradient: softmax policy, log-π gradient, return-weighted update](../assets/policy-gradient.svg)

**The policy gradient theorem.**Pour toute politique `π_θ`paramétrisé par `θ`- Le numéro de la liste:

`∇J(θ) = E_{τ ~ π_θ}[ Σ_{t=0}^{T} G_t · ∇_θ log π_θ(a_t | s_t) ]`

où `G_t = Σ_{k=t}^{T} γ^{k-t} r_{k+1}`est le rendement réduit de la étape `t`L' attente est au-delà des trajectories complètes .`τ`échantillonnés à partir de `π_θ`- Je suis désolé .

> **策略梯度定理。**Pour tout ce qui`θ` Stratégie de numérisation `π_θ`, la échelle de retour de l'espérance est égale à: la réduction du retour et la multiplication de l'espérance de la échelle de la stratégie numérique.`π_θ`Il y a une bonne partie de la route.

**The proof is short.**Différencier `J(θ) = Σ_τ P(τ; θ) G(τ)`- Je suis un peu déçu.`∇P(τ; θ) = P(τ; θ) ∇ log P(τ; θ)`Facteur `log P(τ; θ) = Σ log π_θ(a_t | s_t) + environment terms that do not depend on θ`Les termes de l'environnement disparaissent.

> **证明很短。**Dans l'attente de la`J(θ)`求导―― utiliser pour les techniques de la conduite numérique――将 `log P(τ; θ)`Les deux phases sont déterminées.

**Variance reduction tricks.**La vanille de la force a une variance meurtrière. Les retours sont bruyants.`∇ log π`Le produit est très bruyant.

> **方差降低技巧。**La réinfortation initiale est très bruyante.`∇ log π`Il y a du bruit, leur nombre est plus grand.

1. **Baseline subtraction.**Remplacez`G_t`avec `G_t - b(s_t)`pour toute ligne de base `b(s_t)`qui ne dépend pas de `a_t`- Je suis impartial parce que ...`E[b(s_t) · ∇ log π(a_t | s_t)] = 0`. Choix typique: `b(s_t) = V̂(s_t)`apprise par un critique → acteur-critique (Lément 07).
   **基线减法。**- Je veux le faire .`G_t - b(s_t)` remplacement `G_t`❖ typical choix:`b(s_t) = V̂(s_t)`Il est également un acteur-critique.
2. **Reward-to-go.**Remplacez`Σ_t G_t · ∇ log π_θ(a_t | s_t)`avec `Σ_t G_t^{from t} · ∇ log π_θ(a_t | s_t)`. Seuls les rendements futurs sont importants pour une action donnée  Les récompenses passées contribuent au bruit nul moyen.
   **未来回报。** Seuls les retours futurs à des actions déterminées ont un sens Contribution des récompenses passées à la bruit de valeur moyenne zéro

Combiné, vous obtenez:

`∇J ≈ (1/N) Σ_{i=1}^{N} Σ_{t=0}^{T_i} [ G_t^{(i)} - V̂(s_t^{(i)}) ] · ∇_θ log π_θ(a_t^{(i)} | s_t^{(i)})`

qui est REINFORCE avec une ligne de base  l'ancêtre direct de l'A2C (leçon 07) et du PPO (leçon 08).

**Softmax policy parameterization.**Pour les actions discrètes, le choix standard:

`π_θ(a | s) = exp(f_θ(s, a)) / Σ_{a'} exp(f_θ(s, a'))`

où `f_θ`est un réseau neural qui donne un score par action.

`∇_θ log π_θ(a | s) = ∇_θ f_θ(s, a) - Σ_{a'} π_θ(a' | s) ∇_θ f_θ(s, a')`

c'est-à-dire le score de l'action prise moins sa valeur attendue dans le cadre de la police.

> **Softmax 策略参数化。**Pour les actions décentralisées, la forme de gradiente est simple: le nombre de actions prises diminue la valeur attendue de la stratégie de décentralisation.

**Gaussian policy for continuous actions.** `π_θ(a | s) = N(μ_θ(s), σ_θ(s))`- Je suis là .`∇ log N(a; μ, σ)`Il est nécessaire de fournir une information complète sur les besoins de la phase 9 · 07 du SAC.

> **连续动作的高斯策略。** `∇ log N(a; μ, σ)`Il y a une solution claire. C'est tout ce qui est nécessaire à la phase 9 de la SAC.

## Construisez-le et mettez-le en œuvre.
```figure
policy-gradient-landscape
```

## Faites-le

### Étape 1: réseau de politique softmax

```python
def policy_logits(theta, state_features):
    return [dot(theta[a], state_features) for a in range(N_ACTIONS)]

def softmax(logits):
    m = max(logits)
    exps = [exp(l - m) for l in logits]
    Z = sum(exps)
    return [e / Z for e in exps]
```

Utilisez une politique linéaire (un vecteur de poids par action) pour une enveloppe tabulaire. Pour Atari, échangez dans une CNN et gardez la tête softmax.

> Pour chaque action, un pouvoir de poids est mis en place.

### Étape 2: prélèvement d'échantillons et probabilité de stockage

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

### Étape 3: déploiement avec des sondes de journaux capturées

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

### Étape 4: Mise à jour de REINFORCE

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

Le gradient `∇ log π(a|s) = e_a - π(·|s)`(à l'intérieur de `a`Le cœur des gradients de politique softmax.

> 梯度 `∇ log π(a|s) = e_a - π(·|s)`(le secteur de l'énergie)`a`Le taux de réduction de la probabilité de la température de la température de la température de la température de la température de la température de la température de la température de la température de la température de la température de la température de la température de la température de la température de la température de la température de la température de la température de la température de la température de la température de la température de la température de la température de la température de la température de la température de la température de la température de la température de la température de la température de la température de la température de la température de la température de la température de la température de la température de la température de la température de la température de la température de la température de la température de la température de la température de la température de la température de la température de la température de la température de la température de la température de la température de la température de la température de la température de la température de la température de la température de la température de la température de la température.

### Étape 5: lignes de base

Une moyenne de `G`Les épisodes récents sont suffisants pour réduire la variance pour faire fonctionner un GridWorld 4×4; il faut environ 500 épisodes pour converger.`V̂(s)`et vous obtenez un critique d'acteur.

> Récemment`G`La moyenne de fonctionnement est suffisante pour permettre le travail de 4×4 GridWorld; environ 500 recettes de travail seront mises à niveau pour l'apprentissage.`V̂(s)`On a reçu une critique d'acteur.

## Les pièges

- **Exploding gradients.**Les retours peuvent être énormes.`G`à `~N(0, 1)`à travers le lot avant de multiplier par `∇ log π`- Je suis désolé .
  **梯度爆炸。**Le rapport est très important.`∇ log π`之前始终将 `G`Retour à la société`~N(0, 1)`Il y a une autre.
- **Entropy collapse.**La politique converge à une action quasi-deterministe trop tôt, cesse d'explorer, se retrouve coincée.`β · H(π(·|s))`à l'objectif.
  **熵坍缩。**策略过早收到近确定性动作,停止探索,陷入困境──修复:向目标添加奖励 `β · H(π(·|s))`Il y a une autre.
- **High variance.**La réaction de Vanilla REINFORCE nécessite des milliers d'épisodes.
  **高方差。**Le rétablissement des droits de l'homme est une priorité pour la réforme de la situation économique.
- **Sample inefficiency.**On-policy signifie que vous jetez chaque transition après une mise à jour.Les corrections hors-policy par l'intermédiaire d'un échantillonnage d'importance ramènent des données au coût de la variance (le ratio de l'OPP est un poids IS réduit).
  **样本效率低。**En ligne, le stratagème signifie qu'après chaque mise à jour, tout est abandonné.
- **Non-stationary gradients.**Le même gradient de 100 épisodes auparavant utilise l' ancien .`π`Les méthodes de mise en œuvre de la politique sont mises à jour à chaque déploiement.
  **非平稳梯度。**100 回合前的梯度使用旧的 `π`                                                                                                                                                                                                                                                              
- **Credit assignment.**Sans récompense, les récompenses passées contribuent au bruit.
  **信用分配。**没有未来回报, past's rewards contributions noise──始终使用未来回报──

## Utilisez-le avec le cadre de réalisation

En 2026, REINFORCE est rarement utilisé directement mais sa formule de gradient est partout:

> En 2026, la force de l'air est très peu présente, mais sa forme de force est toujours présente:

| Use case | Derived method |
|----------|---------------|
| Use case / 用例 | Derived method / 派生方法 |
| Continuous control / 连续控制 | PPO / SAC with Gaussian policy / 高斯策略的 PPO/SAC |
| LLM RLHF / LLM RLHF | PPO with KL penalty, running on token-level policy / 带 KL 惩罚的 PPO，token 级策略 |
| LLM reasoning (DeepSeek) / LLM 推理 | GRPO — REINFORCE with group-relative baseline, no critic / 组相对基线的 REINFORCE，无 critic |
| Multi-agent / 多智能体 | Centralized-critic REINFORCE (MADDPG, COMA) / 集中 critic 的 REINFORCE |
| Discrete action robotics / 离散动作机器人 | A2C, A3C, PPO |
| Preference-only settings / 仅偏好设置 | DPO — REINFORCE rewritten as a preference-likelihood loss, no sampling / 重写为偏好似然损失的 REINFORCE |

Quand vous lisez`loss = -advantage * log_prob`Les documents complets (DPO, GRPO, RLOO) sont des astuces de réduction des variantes en plus de cette ligne.

> Quand tu lis dans le script d'entraînement de l'année 2026`loss = -advantage * log_prob`, c'est le RENFORCE de la lignée de base.

## Envoyez-le . Produit .

- Je ne sais pas .`outputs/skill-policy-gradient-trainer.md`- Le numéro de la liste:

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

## Les exercices

1. **Easy.**Mettre en œuvre REINFORCE sur 4×4 GridWorld avec une politique de softmax linéaire. entraîner pour 1000 épisodes sans ligne de base. tracer la courbe d'apprentissage; mesurer la variance (std de rendements).
2. **Medium.**Ajoutez une ligne de base moyenne de course. Reentraînez. Comparer l'efficacité de l'échantillon et la variance à la course de vanille. En combien la ligne de base réduit les étapes de convergence?
3. **Hard.**Ajoutez une bonus d' entropie `β · H(π)`- Le balayage .`β ∈ {0, 0.01, 0.1, 1.0}`Où est le bon point de cette tâche ?

## Les termes clés

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

## Encore une lecture

- [Williams (1992). Simple Statistical Gradient-Following Algorithms for Connectionist Reinforcement Learning](https://link.springer.com/article/10.1007/BF00992696) le papier original de REINFORCE.
- [Sutton et al. (2000). Policy Gradient Methods for Reinforcement Learning with Function Approximation](https://papers.nips.cc/paper_files/paper/1999/hash/464d828b85b0bed98e80ade0a5c43b0f-Abstract.html) le théorème moderne de la politique-gradient avec approximation de fonction.
- [Sutton & Barto (2018). Ch. 13 — Policy Gradient Methods](http://incompleteideas.net/book/RLbook2020.pdf) présentation de livres de cours.
- [OpenAI Spinning Up — VPG / REINFORCE](https://spinningup.openai.com/en/latest/algorithms/vpg.html) exposition pédagogique claire avec le code PyTorch.
- [Peters & Schaal (2008). Reinforcement Learning of Motor Skills with Policy Gradients](https://homes.cs.washington.edu/~todorov/courses/amath579/reading/PolicyGradient.pdf) Réduction des variantes et la vue naturelle-gradiente qui relie REINFORCE à la famille de la région de confiance (TRPO, PPO).
