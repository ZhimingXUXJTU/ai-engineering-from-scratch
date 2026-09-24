# Différence temporelle  Q-Learning & SARSA  时序差分  Q学习 et SARSA

> Monte Carlo attend la fin de l'épisode. TD met à jour après chaque étape en démarrant la prochaine estimation de valeur. Q-learning est hors politique et optimiste; SARSA est sur politique et prudent. Les deux sont une ligne de code. Les deux sont à la base de chaque méthode de RL profonde dans cette phase.

> **【中文解读】**MC doit attendre le cycle pour se mettre à jour, TD`r + γ V(s')` comme objectif de guider les évaluations actuelles Q-apprentissage est l'un des meilleurs stratégies de formation, SARSA est l'un des meilleurs stratégies en ligne de formation `max`Mais c'est la base de toutes les profondeurs de RL.

**Type:** Build | **类型:** 动手
**Languages:** Python | **语言:** Python
**Prerequisites:** Phase 9 · 01 (MDPs), Phase 9 · 02 (Dynamic Programming), Phase 9 · 03 (Monte Carlo) | **前置知识:** Phase 9 · 01 (MDP), Phase 9 · 02 (动态规划), Phase 9 · 03 (蒙特卡洛)
**Time:** ~75 minutes | **时间:** ~75 分钟

## Le problème , l' introduction du problème

Monte Carlo fonctionne mais il a deux exigences coûteuses. Il a besoin d'épisodes qui se terminent, et il ne se met à jour que lorsque le retour final est arrivé. Si votre épisode est de 1000 étapes, MC attend 1000 étapes pour mettre à jour quoi que ce soit. C'est de haute variance, faible partialité, et lent en pratique.

> Le mont Carlo est efficace mais il y a deux exigences coûteuses. Il doit mettre fin au cycle, et ne doit être mis à jour qu'après le retour final. Si le cycle a 1000 étapes, il faut attendre 1000 étapes pour mettre à jour quoi que ce soit.

La programmation dynamique a le profil opposé  sauvegardes à zéro variance  mais nécessite un modèle connu.

> La planification dynamique a des caractéristiques opposées à la différence de caractère, mais nécessite un modèle connu.

L'apprentissage par différence temporelle (TD) divise la différence.`(s, a, r, s')`, pour former une cible en un seul pas `r + γ V(s')`et de pousser`V(s)`Aucun modèle, aucun épisode complet, aucun biais d'utilisation d'une approximation.`V`sur le RHS, mais une variance nettement inférieure à celle du MC et des mises à jour en ligne à partir de l'étape 1.

> 时序差分(TD) learning折中了两者──从单次转移 `(s, a, r, s')` Construire un seul objectif `r + γ V(s')`,将 `V(s)`Pour le côté droit, l'utilisation de l'approximation est plus courte.`V`Il y a des différences, mais les différences sont bien inférieures à MC, et dès la première étape, elles peuvent être mises à jour en ligne.

C'est le pivot sur lequel se tournent toutes les RL  DQN, A2C, PPO, SAC  modernes. Le reste de la phase 9 est des couches d'approximation des fonctions et des astuces construites en haut de la mise à jour TD en une étape que vous écrirez dans cette leçon.

> C'est le reste de la phase 9 qui se compose de la fonction approximative et technique de la phase 9 que vous écrivez dans ce cours.

> **【中文解读】**Le TD apprend à être DP et MC en un seul pas.`(s,a,r,s')`                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             `r + γV(s')`Il n'y a pas besoin de modèle, ni de cycle complet. Il y a des préjugés, car on utilise des approches V, mais les différences sont bien inférieures à MC, et peuvent être mises à jour en ligne.

> **【拓展：游戏AI→LLM对齐】**L'apprentissage Q est le cœur de l'Atari DQN de 2013, qui a lancé la période de RL en profondeur.

## Le concept de base.

![Q-learning vs SARSA: off-policy max vs on-policy Q(s', a')](../assets/td.svg)

**The TD(0) update for V:**

`V(s) ← V(s) + α [r + γ V(s') - V(s)]`

La quantité en parenthèses est l' erreur TD `δ = r + γ V(s') - V(s)`Il s'agit de l' analogue en ligne de `G_t - V(s_t)`dans le MC. La convergence exige `α`- le rapport de l'entreprise`Σ α = ∞`- Je suis là .`Σ α² < ∞`Il y a eu des visites de nombreux États.

> **V 的 TD(0) 更新：**La quantité dans le parenthétique est TD 误差 `δ = r + γ V(s') - V(s)`C'est dans le MC.`G_t - V(s_t)`Les résultats de la recherche ont été obtenus.`α`满足 Robbins-Monro 条件且所有状态被无限次访问──

**Q-learning.**Une méthode de contrôle TD hors politique:

`Q(s, a) ← Q(s, a) + α [r + γ max_{a'} Q(s', a') - Q(s, a)]`

Le `max`Il est donc important de prendre en compte les mesures prises en vue de la mise en œuvre de la politique de l'avidité.`s'`Ce découplage fait que l'apprentissage Q apprend.`Q*`Mnih et al. (2015) ont converti cela en profondeur d'apprentissage Q sur Atari (Léction 05).

> **Q-learning。**Une méthode de contrôle.`max`假设从 `s'`开始将遵循*贪心*策略, peu importe ce que le corps intelligent prend réellement en action.`Q*` Mnih 等人 (2015) va se transformer en Atari 上的深度 Q-learning (leçon 05):

**SARSA.**Une méthode de démarrage de la politique:

`Q(s, a) ← Q(s, a) + α [r + γ Q(s', a') - Q(s, a)]`

Le nom est le tuple .`(s, a, r, s', a')`La SARSA utilise l' action.`a'`L'agent prend le prochain, pas l'avid`argmax`- Converge à`Q^π`Pour quoi que ce soit de cupide .`π`est en cours d'exécution, qui dans la limite `ε → 0`devient `Q*`- Je suis désolé .

> **SARSA。**Une stratégie en ligne TD 方法──名称是元组 `(s, a, r, s', a')`◊ SARSA Utiliser le corps intelligent* réel* de l'action suivante `a'`et non pas avide .`argmax`◊ Recevoir jusqu'à présent ε-贪心 `π``Q^π`, dans le`ε → 0`De la limite sous le changement`Q*`Il y a une autre.

**The cliff-walking difference.**Dans la tâche classique de marche sur le falais (coupe-de-cliff = récompense -100), l'apprentissage Q apprend le chemin optimal le long du bord du falais mais prend parfois la pénalité lors de l'exploration. SARSA apprend un chemin plus sûr à un pas de l'exploration car il fait partie de la valeur Q du bruit d'exploration.`ε → 0`En pratique, il importe: lorsque l'exploration se déroule réellement au déploiement, le comportement de la SARSA est plus conservateur.

> **【中文解读】**L'expérience classique de la marche sur le cliff révèle les différences clés entre Q-learning et SARSA: Q-learning apprend à se tenir sur le cliff mais s'évanouit lorsque l'exploration se produit), SARSA apprend à se tenir loin du cliff et à se protéger de son impact (car il considère le bruit de l'exploration)  Dans les déploiements de recherche, SARSA est plus sûr de maintenir

**Expected SARSA.**Remplacez`Q(s', a')`avec sa valeur attendue inférieure à `π`- Le numéro de la liste:

`Q(s, a) ← Q(s, a) + α [r + γ Σ_{a'} π(a'|s') Q(s', a') - Q(s, a)]`

Variance inférieure à SARSA (pas d' échantillon de `a'`Le problème est que les échanges de données sont souvent négatifs.

> **期望 SARSA。**- Je veux le faire .`π`  下的期望值替换 `Q(s', a')`◊ Comparé à SARSA 方差更低`a'`), le même objectif en ligne.

**n-step TD and TD(λ).**Interpolez entre TD(0) et MC en attendant `n`étapes avant le démarrage. `n=1`est TD, `n=∞`est MC. TD(λ) moyennes sur tous `n`avec des poids géométriques `(1-λ)λ^{n-1}`La plupart des utilisations de RL profonde`n`entre 3 et 20.

> **n 步 TD 和 TD(λ)。**Dans le TD(0) et MC  entre les valeurs, attendre `n`Il est en train de se faire remarquer.`n=1`Oui, le TD,`n=∞`Oui, c'est le MC.`n`取平均── la plupart de la profondeur RL `n`Dans les 3 à 20...

> **【拓展：TD 误差在 LLM RLHF 中的对应】**TD 误差 δ = r + γV(s') - V(s) dans la formation RLHF de LLM: la fonction d'avantage de la PPO A = r + γV(s') - V(s) est la variante de TD 误差. Pour chaque génération de jetons, calculer les récompenses des jetons actuels (r) provient de RM) plus de critique pour l'estimation de la valeur future et la réduction de la valeur actuelle.

## Construisez-le et mettez-le en œuvre.
```figure
qlearning-gridworld
```

## Faites-le

### Étape 1: SARSA sur la politique de l'avidité

```python
def sarsa(env, episodes, alpha=0.1, gamma=0.99, epsilon=0.1):
    Q = defaultdict(lambda: {a: 0.0 for a in ACTIONS})

    def choose(s):
        if random() < epsilon:
            return choice(ACTIONS)
        return max(Q[s], key=Q[s].get)

    for _ in range(episodes):
        s = env.reset()
        a = choose(s)
        while True:
            s_next, r, done = env.step(s, a)
            a_next = choose(s_next) if not done else None
            target = r + (gamma * Q[s_next][a_next] if not done else 0.0)
            Q[s][a] += alpha * (target - Q[s][a])
            if done:
                break
            s, a = s_next, a_next
    return Q
```

La seule différence avec l'apprentissage de Q est la ligne cible.

> La seule différence entre l'apprentissage de Q et l'apprentissage de Q est l'objectif.

### Étape 2: Apprendre à Q

```python
def q_learning(env, episodes, alpha=0.1, gamma=0.99, epsilon=0.1):
    Q = defaultdict(lambda: {a: 0.0 for a in ACTIONS})
    for _ in range(episodes):
        s = env.reset()
        while True:
            a = choose(s, Q, epsilon)
            s_next, r, done = env.step(s, a)
            target = r + (gamma * max(Q[s_next].values()) if not done else 0.0)
            Q[s][a] += alpha * (target - Q[s][a])
            if done:
                break
            s = s_next
    return Q
```

Le `max`Ce symbole est la différence entre les politiques et les politiques.

> `max`Le code est la différence entre la stratégie en ligne et la stratégie de démarrage.

### Étape 3: courbes d'apprentissage

Le taux de retour moyen sur 100 épisodes. Q-learning converge plus rapidement sur le simple GridWorld déterministe; SARSA est plus conservateur sur le grillage.`code/main.py`, les deux sont presque optimaux après environ 2000 épisodes avec`α=0.1, ε=0.1`- Je suis désolé .

> Suivre chaque 100 recourts de retour moyen. Q-apprentissage en simple certitude GridWorld 上收快; SARSA sur le rocher de la falaise plus conservé.`code/main.py`Le 4x4 GridWorld est en train de se développer.`α=0.1, ε=0.1`Environ 2 000 fois plus tard.

### Étape 4: comparer avec la vérité DP

L' iteration de la valeur d' exécution (leçon 02) pour obtenir `Q*`- Vérifiez .`max_{s,a} |Q_learned(s,a) - Q*(s,a)|`Un agent de TD tablaire sain atterrit à l' intérieur de la`~0.5`sur le 4x4 GridWorld après 10 000 épisodes.

> 运行值代(L'enseignement 02) obtenir `Q*` Inspection`max_{s,a} |Q_learned(s,a) - Q*(s,a)|`◊ Un tableau sain TD 智能体 en 10.000 fois réunis en 4×4 GridWorld `~0.5`Dans le même temps.

## Les pièges

- **Initial Q values matter.**L'initiative optimiste (`Q = 0`Les résultats de l'enquête ont été très positifs, et la Commission a décidé de les mettre en œuvre.
  **初始 Q 值很重要。**乐观初始化 负奖励任务中 `Q = 0`Il est possible de trouver des solutions à la recherche de l'économie.
- **α schedule.**Constante`α`Il est bon pour les problèmes non stables.`α_n = 1/n`donne une convergence en théorie mais est trop lente en pratique  pin `α`dans `[0.05, 0.3]`et surveiller la courbe d'apprentissage.
  **α 调度。**Le nombre de`α`                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             `α_n = 1/n`Œuvre théorique mais pratique trop lente Œuvre théorique Œuvre théorique Œuvre théorique Œuvre théorique Œuvre théorique Œuvre théorique Œuvre théorique Œuvre théorique Œuvre théorique Œuvre théorique Œuvre théorique Œuvre théorique Œuvre théorique Œuvre théorique Œuvre théorique Œuvre théorique Œuvre théorique Œuvre théorique Œuvre théorique Œuvre théorique Œuvre théorique Œuvre théorique Œuvre théorique Œuvre théorique Œuvre théorique Œuvre théorique Œuvre théorique Œuvre théorique Œuvre théorique Œuvre théorique Œuvre théorique Œuvre théorique Œuvre théorique Œuvre théorique Œuvre théorique Œdique Œuvre théorique Œdique Œdique Œdique Œdique Œdique Œdique Œdique Œdique Œdique Œdique Œdique Œdique Œdique Œdique Œdique Œdique Œdique Œdique Œdique Œdique Œdique Œdique Œdique Œdique Œdique Œdique Œdique Œdique Œdique Œdique Œdique Œdique Œdique Œdique Œdique Œdique Œc Œdique Œdique Œc Œdique Œc Œdique Œc Œdique Œdique Œdique Œdique Œc`α` Fixée `[0.05, 0.3]`Il a été créé pour la première fois en 2011.
- **ε schedule.**Commencez à hauteur (`ε=1.0`), décomposition à `ε=0.05`. "GLIE" (avidité dans la limite avec exploration infinie) est la condition de convergence.
  **ε 调度。**Depuis le haut de la valeur`ε=1.0`), déclinée à `ε=0.05`La "GLIE" (极极贪心且无限探索) est une condition.
- **Max bias in Q-learning.**Le `max`l' opérateur est biaisé vers le haut lorsque `Q`Le double Q-learning de Hasselt (utilisé par DDQN dans la leçon 05) corrige cette situation avec deux tables Q.
  **Q-learning 的最大化偏差。** `max`Je suis là.`Q`Il y a un bruit lorsque l'on est en train de faire des préjugés.
- **Non-terminating episodes.**TD peut apprendre sans terminaux, mais vous devez soit enfoncer les étapes ou gérer correctement le démarrage au cap.
  **非终止回合。**La pratique standard est de considérer le niveau de niveau comme non-stop, de continuer à le suivre.
- **State hashing.**Si les états sont des tuples/tensors, utilisez une touche hachable (tuple, pas liste; tuple de flottes arrondie, pas crue).
  **状态哈希。**Si l'état est de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur

## Utilisez-le avec le cadre de réalisation

Le paysage de la TD de 2026:

> Édition de l'étude TD de 2026:

| Task | Method | Reason |
|------|--------|--------|
| Task / 任务 | Method / 方法 | Reason / 原因 |
| Small tabular environments / 小型表格环境 | Q-learning | Learns optimal policy directly. / 直接学习最优策略。 |
| On-policy safety-critical / 在线策略安全关键 | SARSA / Expected SARSA | Conservative during exploration. / 探索期间保守。 |
| High-dimensional state / 高维状态 | DQN (Phase 9 · 05) | Neural-net Q-function with replay and target net. / 神经网络 Q 函数+回放+目标网络。 |
| Continuous actions / 连续动作 | SAC / TD3 (Phase 9 · 07) | TD update on a Q-network; policy net emits actions. / Q 网络上的 TD 更新；策略网络输出动作。 |
| LLM RL (reward-model-based) / LLM RL（基于奖励模型） | PPO / GRPO (Phase 9 · 08, 12) | Actor-critic with TD-style advantage via GAE. / Actor-Critic + GAE 的 TD 式优势。 |
| Offline RL / 离线 RL | CQL / IQL (Phase 9 · 08) | Q-learning with conservative regularization. / 带保守正则化的 Q-learning。 |

90% des "RL" que vous lisez dans les articles 2026 sont une élaboration de Q-learning ou SARSA.

> Dans le 2026 année de travaux, vous avez lu "RL", 90% est une variante de Q-apprentissage ou SARSA.

## Envoyez-le . Produit .

- Je ne sais pas .`outputs/skill-td-agent.md`- Le numéro de la liste:

```markdown
---
name: td-agent
description: Pick between Q-learning, SARSA, Expected SARSA for a tabular or small-feature RL task.
version: 1.0.0
phase: 9
lesson: 4
tags: [rl, td-learning, q-learning, sarsa]
---

Given a tabular or small-feature environment, output:

1. Algorithm. Q-learning / SARSA / Expected SARSA / n-step variant. One-sentence reason tied to on-policy vs off-policy and variance.
2. Hyperparameters. α, γ, ε, decay schedule.
3. Initialization. Q_0 value (optimistic vs zero) and justification.
4. Convergence diagnostic. Target learning curve, `|Q - Q*|` check if DP is possible.
5. Deployment caveat. How will exploration behave at inference? Is SARSA's conservatism needed?

Refuse to apply tabular TD to state spaces > 10⁶. Refuse to ship a Q-learning agent without a max-bias caveat. Flag any agent trained with ε held at 1.0 throughout (no exploitation phase).
```

## Les exercices

1. **Easy.**Implémenter Q-learning et SARSA sur le 4×4 GridWorld. Plot des courbes d'apprentissage (retour moyen par 100 épisodes) pour 2000 épisodes. Qui converge plus vite?
   > **练习1：**En ce qui concerne les cours de formation de la société, les cours de formation de la société sont les suivants:
2. **Medium.**Construisez un environnement de marche sur un cliff (4x12, la dernière rangée est le cliff avec récompense -100 et réinitialisez pour commencer). Comparer les politiques finales de Q-learning et SARSA.
   > **练习2：** réaliser un climat de cliff, observer les différences de stratégie de Q-apprentissage
3. **Hard.**Dans un GridWorld avec une récompense bruyante (bruit gaussien σ=5 ajouté à la récompense par étape), affichez des surestimations de l'apprentissage de Q `V*(0,0)`Il est vrai que les deux types d'apprentissage sont différents.
   > **练习3：**¢ réaliser un double Q-learning, vérifier qu'il peut éliminer le plus grand décalage de Q-learning¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬

## Les termes clés

| Term | What people say | What it actually means |
|------|-----------------|-----------------------|
| TD error | "The update signal" / TD 误差 | `δ = r + γ V(s') - V(s)`, the bootstrapped residual. |
| TD(0) | "One-step TD" / 单步 TD | Update after every transition using only the next state's estimate. |
| Q-learning | "Off-policy RL 101" / Q 学习 | TD update with `max` over next-state actions; learns `Q*` regardless of behavior policy. |
| SARSA | "On-policy Q-learning" / SARSA | TD update using the actual next action; learns `Q^π` for current ε-greedy π. |
| Expected SARSA | "The low-variance SARSA" / 期望 SARSA | Replace sampled `a'` with its expectation under π. |
| GLIE | "Correct exploration schedule" / 无限探索极限贪心 | Greedy in the Limit with Infinite Exploration; needed for Q-learning convergence. |
| Bootstrapping | "Using current estimate in the target" / 自举 | What distinguishes TD from MC. Source of bias but massive variance reduction. |
| Maximization bias | "Q-learning overestimates" / 最大化偏差 | `max` over noisy estimates is upward-biased; fixed by Double Q-learning. |

## Encore une lecture

- [Watkins & Dayan (1992). Q-learning](https://link.springer.com/article/10.1007/BF00992698) le papier original et la preuve de convergence.
- [Sutton & Barto (2018). Ch. 6 — Temporal-Difference Learning](http://incompleteideas.net/book/RLbook2020.pdf) TD(0), SARSA, Q-apprentissage, SARSA attendue.
- [Hasselt (2010). Double Q-learning](https://papers.nips.cc/paper_files/paper/2010/hash/091d584fced301b442654dd8c23b3fc9-Abstract.html) fixer le biais de maximisation.
- [Seijen, Hasselt, Whiteson, Wiering (2009). A Theoretical and Empirical Analysis of Expected SARSA](https://ieeexplore.ieee.org/document/4927542) motivation attendue par le SARSA.
- [Rummery & Niranjan (1994). On-line Q-learning using connectionist systems](https://www.researchgate.net/publication/2500611_On-Line_Q-Learning_Using_Connectionist_Systems) le document qui a inventé SARSA (alors appelé "apprentissage Q-connexion modifié").
- [Sutton & Barto (2018). Ch. 7 — n-step Bootstrapping](http://incompleteideas.net/book/RLbook2020.pdf) généralise le TD(0) à TD(n), le chemin de l'apprentissage Q aux traces d'admissibilité et, plus tard, de l'AEG en PPO.
