# Les méthodes de Monte Carlo  Apprendre des épisodes complets  Les méthodes de Monte Carlo  Apprendre du cycle complet

> La programmation dynamique a besoin d'un modèle. Monte Carlo n'a besoin que d'épisodes. Exécutez la politique, regardez les rendements, les moyenniez. L'idée la plus simple dans RL  et celle qui déverrouille tout en aval.

> **【中文解读】**Le projet de RL nécessite un modèle environnemental connu, le RL nécessite seulement un cycle complet de données: stratégie d'exécution, observation, répertoire, moyenne.

**Type:** Build | **类型:** 动手
**Languages:** Python | **语言:** Python
**Prerequisites:** Phase 9 · 01 (MDPs), Phase 9 · 02 (Dynamic Programming) | **前置知识:** Phase 9 · 01 (MDP), Phase 9 · 02 (动态规划)
**Time:** ~75 minutes | **时间:** ~75 分钟

## Le problème , l' introduction du problème

La programmation dynamique est élégante, mais elle suppose que vous pouvez demander `P(s' | s, a)`Un robot ne peut pas calculer analytiquement la distribution sur les pixels de la caméra après un couple commun. Un algorithme de prix ne peut pas s'intégrer sur chaque réaction possible du client. Un LLM ne peut pas énumérer toutes les continuations possibles après un jeton.

> La planification est très agréable, mais supposons que vous puissiez consulter chaque état et chaque mouvement.`P(s' | s, a)`◊ en réalité, presque rien ne fonctionne de cette façon. ◊ Les machines ne peuvent pas résoudre la distribution des images de la phase de la phase de la phase de la phase de la phase de la phase de la phase de la phase de la phase de la phase de la phase de la phase de la phase de la phase de la phase de la phase de la phase de la phase de la phase de la phase de la phase de la phase de la phase de la phase de la phase de la phase de la phase de la phase de la phase de la phase de la phase de la phase de la phase de la phase de la phase de la phase de la phase de la phase de la phase de la phase de la phase de la phase de la phase de la phase de la phase de la phase de la phase de la phase de la phase de phase de la phase de phase de phase de phase de phase de phase de phase de phase.

Vous avez besoin d'une méthode qui ne nécessite que la capacité de *prendre des échantillons* de l'environnement.`s_0, a_0, r_1, s_1, a_1, r_2, …, s_T`- Utilisez-le pour estimer les valeurs.

> Vous avez besoin d'une méthode qui vient du milieu.`s_0, a_0, r_1, s_1, a_1, r_2, …, s_T`C'est le Mont-Carlo.

Le changement de DP à MC est philosophiquement important: nous passons de * modèle connu + sauvegarde exacte * à * déploiements échantillonnés + retour moyen*. La variance augmente, mais l'applicabilité explose. Chaque algorithme RL après cette leçon  TD, Q-learning, REINFORCE, PPO, GRPO  est un estimateur de Monte Carlo au cœur, parfois avec le démarrage en couches en haut.

> Le changement de DP à MC est important en philosophie: nous sommes allés de * modèle connu + réserves précises * à * déploiement de échantillons + revenu moyen *: le décalage a augmenté, mais la portée de l'application a explosément augmenté.

> **【中文解读】**Le changement de cœur du DP au MC: du modèle connu + calcul précis à la trajectoire de la formation + rapport moyen.

> **【拓展：LLM中的MC】**Dans le cadre de l'entraînement RLHF de ChatGPT, le GRPO de DeepSeek-R1 est également basé sur des estimations MC de type "group-in-consultation"

## Le concept de base.

![Monte Carlo: rollout, compute returns, average; first-visit vs every-visit](../assets/monte-carlo.svg)

**The core idea, in one line:** `V^π(s) = E_π[G_t | s_t = s] ≈ (1/N) Σ_i G^{(i)}(s)`où `G^{(i)}(s)`Les résultats observés sont les suivants:`s`dans le cadre de la politique `π`- Je suis désolé .

> **核心思想，一行概括：** `V^π(s) = E_π[G_t | s_t = s] ≈ (1/N) Σ_i G^{(i)}(s)`, parmi lesquels `G^{(i)}(s)`C'est dans la stratégie.`π`Suivre `s`时观测到的回报──

> **【中文解读】**MC évaluation de la base: état = valeur moyenne des retours de plusieurs fois passé par cet état ⋅ moyenne des retours de l'observation ⋅ moyenne de la première visite ⋅ moyenne de chaque visite ⋅ moyenne de chaque visite ⋅ moyenne de chaque visite ⋅ moyenne de chaque visite ⋅ moyenne de chaque visite ⋅ moyenne de chaque visite ⋅ moyenne de chaque visite ⋅ moyenne de chaque visite ⋅ moyenne de chaque visite ⋅ moyenne de chaque visite ⋅ moyenne de chaque visite ⋅ moyenne de chaque visite ⋅ moyenne de chaque visite ⋅ moyenne de chaque visite ⋅ moyenne de chaque visite ⋅ moyenne de chaque visite ⋅ moyenne de chaque visite ⋅ moyenne de chaque visite ⋅ moyenne de chaque visite ⋅ moyenne de chaque visite ⋅ moyenne de chaque visite ⋅ moyenne de chaque visite ⋅ moyenne de chaque visite ⋅ moyenne de chaque visite ⋅ moyenne de chaque visite ⋅ moyenne de chaque visite ⋅ moyenne de chaque visite ⋅ moyenne ⋅ moyenne de chaque visite ⋅ moyenne ⋅ moyenne de chaque visite ⋅ moyenne ⋅ moyenne ⋅ moyenne de chaque visite ⋅ moyenne ⋅ moyenne ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅                                                                                                                                                                                                                                               `V_new = V_old + α(target - V_old)`Il est le pont de l'algorithme de RL moderne.

**First-visit vs every-visit MC.**Vu un épisode qui visite l' état `s`Les premières visites sont plus simples à analyser (échantillons d'iid). Chaque visite utilise plus de données par épisode et converge généralement plus rapidement dans la pratique.

> **首次访问 vs 每次访问 MC。** donner un état de plusieurs visites `s`Les deux sont sans préjugé en dessous de la limite. Les deux sont plus faciles à analyser.

**Incremental mean.**Au lieu de stocker tous les retours, mettre à jour la moyenne courante:

`V_n(s) = V_{n-1}(s) + (1/n) [G_n - V_{n-1}(s)]`

Réorganiser: `V_new = V_old + α · (target - V_old)`avec `α = 1/n`- Échangez .`1/n`pour une taille de marge constante `α ∈ (0, 1)`et vous obtenez un estimateur MC non-stationnaire qui suit les changements dans `π`Ce mouvement est le saut de MC à TD à tous les algorithmes RL modernes.

> **增量均值。**Il est possible de détecter les données de la société.`1/n`替换为常数步长 `α ∈ (0, 1)`On a une piste.`π`L'équipe de calcul de la RL est en train de réaliser un saut de MC à TD à tous les algorithmes modernes de RL.

**Exploration is now a problem.**Le DP a touché chaque État par l'enregistrement.`π`Les données de l'espace de l'état ne sont jamais échantillonnées et leurs estimations de valeur restent à zéro pour toujours.

> **探索现在成了问题。**DP 通过枚举触及每个状态──MC 只有看到策略访问的状态──如果`π`Il est certain que l'ensemble de la zone de l'espace d'état ne sera jamais prise en compte, sa valeur estimée sera toujours à zéro.

> **【中文解读】**探索问题:DP 能遍历所有状态,MC 能看到策略访问过的状态――如果策略是确定性的,大量状态永远不会被访问──三种解决方案:探索起点 (不实) ̇ε-贪心 (最常用) ̇离策略MC ̇通过重要性采样从行为策略学习目标策略)

1. **Exploring starts.**Commencez chaque épisode à partir d'une paire aléatoire (s, a). Garantit la couverture; irréaliste dans la pratique (vous ne pouvez pas "réinitialiser" un robot dans un état arbitraire).
   **探索起点。**Chaque cycle est à partir de l'instant (s) à commencer.
2. **ε-greedy.**Agissez avide avec le courant Q, mais avec la probabilité `ε`Toutes les paires d'actions d'état sont échantillonnées de manière asymptotique.
   **ε-贪心。**Pour les actions de Q 贪心, mais en probabilité `ε`随机选动作── Tous les états-motions sont progressivement adoptés──
3. **Off-policy MC.**Rassembler des données dans le cadre d' une politique de comportement `μ`, apprendre sur la politique cible `π`La variance est élevée, mais c'est le pont vers des méthodes de tampon de répétition comme DQN.
   **离策略 MC。**Dans les stratégies de comportement`μ`La collecte de données, par l'importance de la stratégie de l'objectif d'apprentissage`π`高方差, mais il est passé par DQN 等回放缓冲方法的桥梁

**Monte Carlo Control.**Évaluer → améliorer → évaluer, tout comme l'itération de la politique, mais l'évaluation est basée sur l'échantillonnage:

1. On court .`π`- Je vais vous faire un épisode.
2. Mise à jour `Q(s, a)`à partir des résultats observés.
3. Faites-le`π`É-coupard de l'argent.`Q`- Je suis désolé .
4. Je répète.

Converge à `Q*`et `π*`avec probabilité 1 dans des conditions douces (toutes les paires ont été visitées de façon infinie,`α`Il est satisfait de Robbins-Monro.

> **蒙特卡洛控制。**评估 → 改进 → 评估,就像策略代, mais évaluer sur la base de la mise en œuvre.`α`满足 Robbins-Monro), à une probabilité de 1 收到 `Q*`et `π*`Il y a une autre.

## Construisez-le et mettez-le en œuvre.
```figure
epsilon-greedy
```

## Faites-le

### Étape 1: déploiement → liste de (s, a, r)

```python
def rollout(env, policy, max_steps=200):
    trajectory = []
    s = env.reset()
    for _ in range(max_steps):
        a = policy(s)
        s_next, r, done = env.step(s, a)
        trajectory.append((s, a, r))
        s = s_next
        if done:
            break
    return trajectory
```

Pas de modèle, seulement.`env.reset()`et `env.step(s, a)`- La même interface qu'un environnement de gym, mais dépouillée.

> Il n'y a pas besoin de modèle, il y a besoin.`env.reset()`et `env.step(s, a)`                                                                                                                                                                                                                                                              

### Étape 2: retour de calcul (soufflement inverse)

```python
def returns_from(trajectory, gamma):
    returns = []
    G = 0.0
    for _, _, r in reversed(trajectory):
        G = r + gamma * G
        returns.append(G)
    return list(reversed(returns))
```

Une passe,`O(T)`La récurrence en arrière .`G_t = r_{t+1} + γ G_{t+1}`évitent de recommencer à la somme.

> Une fois par jour,`O(T)` Retour vers le passé`G_t = r_{t+1} + γ G_{t+1}`避免了重复求和──

### Étape 3: évaluation du MC lors de la première visite

```python
def mc_policy_evaluation(env, policy, episodes, gamma=0.99):
    V = defaultdict(float)
    counts = defaultdict(int)
    for _ in range(episodes):
        trajectory = rollout(env, policy)
        returns = returns_from(trajectory, gamma)
        seen = set()
        for t, ((s, _, _), G) in enumerate(zip(trajectory, returns)):
            if s in seen:
                continue
            seen.add(s)
            counts[s] += 1
            V[s] += (G - V[s]) / counts[s]
    return V
```

Trois lignes font le travail: marquer l'état vu lors de la première visite, le nombre de points, la moyenne de mise à jour.

> 三行代码完成工作: 标记首次访问的状态,增加计数,更新运行平均值──

### Étape 4: contrôle de MC avide (sur la politique)

```python
def mc_control(env, episodes, gamma=0.99, epsilon=0.1):
    Q = defaultdict(lambda: {a: 0.0 for a in ACTIONS})
    counts = defaultdict(lambda: {a: 0 for a in ACTIONS})

    def policy(s):
        if random() < epsilon:
            return choice(ACTIONS)
        return max(Q[s], key=Q[s].get)

    for _ in range(episodes):
        trajectory = rollout(env, policy)
        returns = returns_from(trajectory, gamma)
        seen = set()
        for (s, a, _), G in zip(trajectory, returns):
            if (s, a) in seen:
                continue
            seen.add((s, a))
            counts[s][a] += 1
            Q[s][a] += (G - Q[s][a]) / counts[s][a]
    return Q, policy
```

### Étape 5: comparer avec le standard d'or DP

Votre estimation du MC de `V^π`En pratique, 50 000 épisodes sur 4×4 GridWorld vous permettent de vous intégrer dans la série.`~0.1`de la réponse du DP.

> Tu es à moi .`V^π`Les résultats de l'étude de la leçon 02 sont conformes à la même estimation de la leçon 2 de la leçon 2 de la leçon 2 de la leçon 2 de la leçon 2 de la leçon 2 de la leçon 2 de la leçon 2 de la leçon 2 de la leçon 2 de la leçon 2 de la leçon 2 de la leçon 2 de la leçon 2 de la leçon 2 de la leçon 2 de la leçon 2 de la leçon 2 de la leçon 2 de la leçon 2 de la leçon 2 de la leçon 2 de la leçon 2 de la leçon 2 de la leçon 2 de la leçon 2 de la leçon 2 de la leçon 2 de la leçon 2 de la leçon 2 de la leçon 2 de la leçon 4 de la leçon 4 de la leçon 4 de la leçon 4 de la leçon 4 de la leçon 4 de la leçon 4 de la leçon 4 de la leçon 3 de la leçon 3 de la leçon 3 de la leçon 3 de la leçon 3 de la le 5 de la leçon 3 de la le 5 de la leçon 3 de la le 5 de la leçon 3 de la le 5 de la le 5 de la leçon 3 de la le 5 de la le 5 de la le 5 de la le 5 de la le 7 de la le 7 de la le 7 de la le 7 de la page de la page de la page de la page de la page de la page de la page de la page de la page de la page de la page de la page de page de la page de page de page de page de page de page de page de page de page de page de page de page de page de page de page de page de page de page de page de page de page de page de page de page de page de page de page de page de page de page de page de page de page de page de page de page de page de page de page de page de page de page de page de page de page de page de page de page de page de page de page de page de page de page de page de page de page de page de page de page de page de page de page de page de page de page de page de page de page de page de page de page de page de page de page de page de page de page de page de page`~0.1`Dans le même temps.

## Les pièges

- **Infinite episodes.**MC a besoin d'épisodes pour *cesser*. Si votre politique peut boucle pour toujours, cap `max_steps`GridWorld avec une politique aléatoire, il faut compter correctement.
  **无限回合。**MC 要求回合*终止*──如果策略可能永远循环,设置 `max_steps`La limite supérieure sera considérée comme un échec caché.
- **Variance.**MC utilise des retours complets. sur les longs épisodes, la variance est énorme  une récompense malchanceuse à la fin des tours `V(s_0)`Les méthodes TD (Lesson 04) réduisent ce nombre en le démarrant.
  **方差。**MC utilise le récit complet.`V(s_0)`◊TD 方法(L'enseignement 04) par l'intermédiaire de la mise en place et de la réduction des différences
- **State coverage.**Un MC avide sur un Q frais avec des liens n'essaie qu'une seule action.
  **状态覆盖。**Il faut que tu explores le cœur, le cœur, le cœur, le cœur.
- **Non-stationary policies.**Si vous`π`Les résultats de l'analyse de l'échantillon sont basés sur des données de référence, et les résultats de l'échantillon sont basés sur des données de référence.
  **非平稳策略。**Si `π`变化(如 MC 控制中),旧回报来自不同策略──常数 α MC 处理此问题;样本平均 MC 不能──
- **Off-policy importance sampling.**Les poids .`π(a|s)/μ(a|s)`La variance explose avec l'horizon.
  **离策略重要性采样。**权重  référencement`π(a|s)/μ(a|s)`Dans le même temps, les différences de couleur sont aussi importantes que les différences de couleur.

## Utilisez-le avec le cadre de réalisation

Le rôle des méthodes de Monte Carlo en 2026:

> 2026: Les rôles de la méthode de Montcarlo:

| Use case | Why MC |
|----------|--------|
| Use case / 用例 | Why MC / 为什么用 MC |
| Short-horizon games (blackjack, poker) / 短视野游戏（二十一点、扑克） | Episodes terminate naturally; returns are clean. / 回合自然终止；回报干净。 |
| Offline evaluation of a logged policy / 离线评估已记录的策略 | Average discounted returns over stored trajectories. / 对存储轨迹取折扣回报平均。 |
| Monte Carlo Tree Search (AlphaZero) / 蒙特卡洛树搜索 | MC rollouts from tree leaves guide selection. / 树叶的 MC rollout 指导选择。 |
| LLM RL evaluation / LLM RL 评估 | Compute average reward over sampled completions for a given policy. / 对给定策略的采样完成计算平均奖励。 |
| Baseline estimation in PPO / PPO 中的基线估计 | The advantage target `A_t = G_t - V(s_t)` uses an MC `G_t`. / 优势目标使用 MC 的 `G_t`。 |
| Teaching RL / 教学 RL | Simplest algorithm that actually works — strip bootstrapping to see the core. / 最简单且有效的算法——去掉自举看核心。 |

Les algorithmes modernes de profondeur de RL (PPO, SAC) interpolent entre MC pur (rendement complet) et TD pur (bootstrap à un pas) via `n`Les deux points de fin sont des instances du même estimateur.

> 现代深度 RL 算法 PPO、SAC) par le biais `n`步回报或 GAE 在纯 MC (完整回报) 和纯 TD (单步自举) 间插值.

## Envoyez-le . Produit .

- Je ne sais pas .`outputs/skill-mc-evaluator.md`- Le numéro de la liste:

```markdown
---
name: mc-evaluator
description: Evaluate a policy via Monte Carlo rollouts and produce a convergence report with DP-comparison if available.
version: 1.0.0
phase: 9
lesson: 3
tags: [rl, monte-carlo, evaluation]
---

Given an environment (episodic, with reset+step API) and a policy, output:

1. Method. First-visit vs every-visit MC. Reason.
2. Episode budget. Target number, variance diagnostic, expected standard error.
3. Exploration plan. ε schedule (if needed) or exploring starts.
4. Gold-standard comparison. DP-optimal V* if tabular; otherwise a bound from a Q-learning / PPO baseline.
5. Termination check. Max-step cap, timeouts, handling of non-terminating trajectories.

Refuse to run MC on non-episodic tasks without a finite horizon cap. Refuse to report V^π estimates from fewer than 100 episodes per state for tabular tasks. Flag any policy with zero-variance actions as an exploration risk.
```

## Les exercices

1. **Easy.**Mettre en œuvre une évaluation MC de la politique uniforme au hasard lors de la première visite sur 4×4 GridWorld.`V(0,0)`en fonction du nombre d'épisodes par rapport à la réponse du DP.
   > **练习1：**¢ réaliser MC ¢ évaluation, ¢ V ¢ 0,0) ¢ avec le nombre de recouvrements de la courbe de réception et le DP ¢基准对比──
2. **Medium.**Implémenter le contrôle de l' MC avec `ε ∈ {0.01, 0.1, 0.3}`Comparer le retour moyen après 20 000 épisodes.
   > **练习2：**Utilisation de la valeur de l'équipement de contrôle, observation explorer-utiliser le pouvoir de contrôle.
3. **Hard.**Implementer des MC "extra-politiques" avec échantillonnage d'importance: collecter des données dans le cadre d'une politique uniforme et aléatoire `μ`, estimation `V^π`pour la politique déterministe optimale `π`Comparer l'IS simple par rapport à l'IS par décision par rapport à l'IS pondéré.
   > **练习3：**实现离策略 MC 重度采样), comparer différents IS 方差的差异──

## Les termes clés

| Term | What people say | What it actually means |
|------|-----------------|-----------------------|
| Monte Carlo | "Random sampling" / 蒙特卡洛 | Estimate expectations by averaging over iid samples from the distribution. |
| Return `G_t` | "Future reward" / 回报 | Sum of discounted rewards from step `t` to episode end: `Σ_{k≥0} γ^k r_{t+k+1}`. |
| First-visit MC | "Count each state once" / 首次访问 MC | Only the first visit in an episode contributes to the value estimate. |
| Every-visit MC | "Use all visits" / 每次访问 MC | Every visit contributes; slightly biased but more sample-efficient. |
| ε-greedy | "Exploration noise" / ε-贪心 | Pick greedy action with prob `1-ε`; random action with prob `ε`. |
| Importance sampling | "Correcting for sampling from the wrong distribution" / 重要性采样 | Reweight returns by `π(a\|s)/μ(a\|s)` products to estimate `V^π` from `μ` data. |
| On-policy | "Learn from my own data" / 在线策略 | Target policy = behavior policy. Vanilla MC, PPO, SARSA. |
| Off-policy | "Learn from someone else's data" / 离线策略 | Target policy ≠ behavior policy. Importance-sampled MC, Q-learning, DQN. |

## Encore une lecture

- [Sutton & Barto (2018). Ch. 5 — Monte Carlo Methods](http://incompleteideas.net/book/RLbook2020.pdf) le traitement canonique.
- [Singh & Sutton (1996). Reinforcement Learning with Replacing Eligibility Traces](https://link.springer.com/article/10.1007/BF00114726) analyse de la première visite par rapport à chaque visite.
- [Precup, Sutton, Singh (2000). Eligibility Traces for Off-Policy Policy Evaluation](http://incompleteideas.net/papers/PSS-00.pdf) MC et contrôle des variantes hors politique.
- [Mahmood et al. (2014). Weighted Importance Sampling for Off-Policy Learning](https://arxiv.org/abs/1404.6362) estimateurs IS modernes à faible variance.
- [Tesauro (1995). TD-Gammon, A Self-Teaching Backgammon Program](https://dl.acm.org/doi/10.1145/203330.203343) la première démonstration empirique à grande échelle du jeu de MC/TD convergeant au jeu surhumain; précurseur conceptuel de chaque leçon dans la seconde moitié de cette phase.
