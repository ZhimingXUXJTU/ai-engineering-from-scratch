# RL multi-agent, plus d'intelligence pour apprendre à renforcer la chimique.

> L'agent unique RL suppose que l'environnement est stationnaire. Mettre deux agents d'apprentissage dans le même monde et cette hypothèse est cassée: chaque agent fait partie de l'environnement de l'autre, et les deux changent.

> **【中文解读】**L'environnement est déstabilisé. L'hypothèse de l'environnement est brisée. Mais après avoir été introduit dans deux systèmes intelligents qui apprennent simultanément, chaque système intelligent devient une partie de l'environnement de l'autre.

**Type:** Build | **类型:** 动手
**Languages:** Python | **语言:** Python
**Prerequisites:** Phase 9 · 04 (Q-learning), Phase 9 · 06 (REINFORCE), Phase 9 · 07 (Actor-Critic) | **前置知识:** Phase 9 · 04 (Q-learning), Phase 9 · 06 (REINFORCE), Phase 9 · 07 (Actor-Critic)
**Time:** ~45 minutes | **时间:** ~45 分钟

## Le problème , l' introduction du problème

Un robot apprenant à naviguer dans une pièce est un problème de RL d'agent unique. Une équipe de football n'est pas. Les adversaires AlphaStar vs StarCraft ne le sont pas. Un marché d'agents d'appel d'offres n'est pas. Deux voitures négociant un arrêt à quatre voies ne le sont pas. Beaucoup de problèmes sur beaucoup dans le monde réel ne le sont pas.

> L'équipe de football n'est pas un problème. L'équipe de football n'est pas un problème. L'équipe de football n'est pas un problème.

Dans chaque contexte multi-agents, du point de vue d'un agent, les autres agents font partie de l'environnement. Au fur et à mesure qu'ils apprennent et changent de comportement, l'environnement devient non-stagnant. La propriété Markov  "l'état suivant dépend uniquement de l'état actuel et de mon action"  est violée parce que l'état suivant dépend également de ce que les *autres* agents ont choisi, et leurs politiques sont des cibles en mouvement.

> Dans chaque milieu multi-intelligent, du point de vue de chaque organisme intelligent, les autres sont une partie de l'environnement. Lorsqu'ils apprennent et changent leur comportement, l'environnement devient instable. La flexibilité est violée, car l'état d'origine dépend également du choix des autres, et leur stratégie est celle d'un objectif mobile.

Cela casse les preuves de convergence tabulaire (la garantie de Q-learning suppose un environnement stationnaire). Il casse également la RL profonde naïve: les agents se poursuivent dans des boucles, ne convergent jamais vers une politique stable.

> Cela a détruit le modèle de réception de la preuve de Q-learning. Il a également détruit la profondeur simple de RL: les êtres intelligents se poursuivent mutuellement, ne jamais obtenir de stratégie de rétablissement.

2026 applications: essaims de robots, routage de la circulation, flottes de véhicules autonomes, simulateurs de marché, systèmes de gestion de la gestion des risques multi-agents (phase 16), et tout jeu avec plus d'un joueur intelligent.

> Application 2026: groupe de personnes, chemin de fer, équipe de conduite autonome, marché simulateur, système de gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion des ressources et de gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion des projets.

> **【中文解读】**Le défi central de la RL est de ne pas avoir de stabilité dans l'apprentissage, de ne pas avoir de répartition de crédit, de ne pas avoir de répartition de crédit, de ne pas avoir de répartition de crédit, de ne pas avoir de répartition de crédit, de ne pas avoir de répartition de crédit, de ne pas avoir de répartition de crédit, de ne pas avoir de répartition de crédit, de ne pas avoir de répartition de crédit, de ne pas avoir de répartition de crédit, de ne pas avoir de répartition de crédit, de ne pas avoir de répartition de crédit, de ne pas avoir de répartition de crédit, de ne pas avoir de répartition de crédit, de ne pas avoir de répartition de crédit, de ne pas avoir de répartition de répartition de répartition de répartition, de ne pas avoir de répartition de répartition, de ne pas avoir de répartition de répartition, de ne pas avoir de répartition de répartition, de ne pas avoir de répartition de répartition, de ne pas avoir de répartition de répartition.

> **【拓展：多智能体→LLM Agent系统】**L'application MARL la plus populaire de 2026 est le système LLM multi-intelligents: plusieurs grands modèles d'agents collaborant à accomplir des tâches complexes.

## Le concept de base.

![Four MARL regimes: indep, centralized critic, self-play, league](../assets/marl.svg)

**Formalism: Markov Game.**Une généralisation du MDP: États `S`, une action commune `a = (a_1, …, a_n)`, transition `P(s' | s, a)`, et récompenses par agent `R_i(s, a, s')`- Chaque agent .`i`maximiser son propre rendement dans le cadre de sa propre politique `π_i`Si les récompenses sont identiques, c'est le cas.**fully cooperative**Si c'est une somme nulle, c'est ça.**adversarial**Si elle est mélangée, elle est.**general-sum**- Je suis désolé .

> **形式化：马尔可夫博弈。**MDP 的推广: état `S`、 unité de travail `a = (a_1, …, a_n)`、 transfert `P(s'|s,a)`Récompenses pour chaque être intelligent`R_i`Si les récompenses sont les mêmes,**全合作**Si c'est le zéro et le zéro,**对抗**Si on est mélangé,**一般和**Il y a une autre.

**Core challenges:**

- **Non-stationarity.** `P(s' | s, a_i)`de l' agent `i`La vue dépend de `π_{-i}`, ce qui change.
  **非平稳性。**De l' esprit`i`Le transfert dépend de la stratégie des autres êtres intelligents en train de changer.
- **Credit assignment.**Avec une récompense partagée, quel agent l'a causé ?
  **信用分配。**Quand on partage des récompenses, quel est le corps intelligent qui a conduit ?
- **Exploration coordination.**Les agents doivent explorer des stratégies complémentaires, pas redondamment explorer le même état.
  **探索协调。**Le "intelligent" doit explorer des stratégies de complément, et non une exploration exagérée du même état.
- **Scalability.**L' espace d' action commune augmente de façon exponentielle en `n`- Je suis désolé .
  **可扩展性。**联合动作空间随 `n`Le nombre de personnes qui ont été tuées
- **Partial observability.**Chaque agent ne voit que sa propre observation; l'état mondial est caché.
  **部分可观察性。**Chaque corps intelligent ne voit que ses propres observations; l'état de l'ensemble est caché.

**Four dominant regimes:**

> **四种主导范式：**

**1. Independent Q-learning / independent PPO (IQL, IPPO).**Chaque agent apprend sa propre Q ou politique, traitant les autres comme faisant partie de l'environnement. Simple, parfois cela fonctionne (surtout avec une répétition de l'expérience agissant comme un truc de modélisation d'agent de lissage). Convergence théorique: aucune.

> **1. 独立 Q-learning / 独立 PPO。**Chaque organe intelligent apprend son propre Q ou stratégie, considérant l'autre être un élément de son environnement.

**2. Centralized training, decentralized execution (CTDE).**Le paradigme moderne le plus courant.`π_i`que les conditions de l' observation locale `o_i` exécution standard décentralisée au déploiement.`Q(s, a_1, …, a_n)`Les conditions relatives à l'état global complet et à l'action commune.
- **MADDPG**(Lowe et coll. 2017): DDPG avec un critique centralisé par agent.
- **COMA**(Foerster et coll. 2017): base contrefactuelle  demandez " quelle aurait été ma récompense si j'avais pris des mesures `a'`"  isole ma contribution.
- **MAPPO**- Je suis là .**IPPO**avec critique partagée (Yu et coll. 2022): PPO avec une fonction de valeur centralisée.
- **QMIX**(Rashid et coll. 2018): décomposition de la valeur  `Q_tot(s, a) = f(Q_1(s, a_1), …, Q_n(s, a_n))`avec un mélange monotone.

> **2. 集中训练，分布执行（CTDE）。**Le modèle moderne le plus courant est le modèle de la stratégie de chaque organe intelligent, qui dépend uniquement de l'observation locale.

**3. Self-play.**Deux copies du même agent se jouent. La politique de l'adversaire *est* ma politique d'un instantané passé. AlphaGo / AlphaZero / MuZero. OpenAI Five. Fonctionne mieux pour les jeux à somme nulle; le signal d'entraînement est symétrique.

> **3. 自我博弈。**Les deux copies du même corps intelligent sont les mêmes. Les deux techniques sont les mêmes.

**4. League play.**Une extension du jeu à des environnements généraux / adversitaires: conserver une population de politiques passées et actuelles, échantillonner un adversaire de la ligue, s'entraîner contre eux. Ajout d'exploitants (spécialisés dans la battre le meilleur actuel) et d'exploitants principaux (spécialisés dans la battre des exploitants). AlphaStar (StarCraft II). Nécessaire lorsque le jeu admet des cycles de stratégie "rock-paper-scissors".

> **4. 联盟训练。**L'expansion de la société: maintenir le passé et le présent, en se battant contre les autres.

**Communication.**Permettez aux agents d' envoyer des messages apprentis .`m_i`Foerster et coll. (2016) ont montré que la communication interagent différenciable peut être formée de bout en bout. Les systèmes multi-agents basés sur le LLM d'aujourd'hui (phase 16) communiquent essentiellement en langage naturel.

> **通信。**Le programme de formation en langue étrangère est un programme de formation en langue étrangère.

## Construisez-le et mettez-le en œuvre.
```figure
f3-marl-orbit
```

## Faites-le

Cette leçon utilise un 6×6 GridWorld avec deux agents coopératifs. Ils commencent dans des coins opposés et doivent atteindre un objectif commun. Récompense partagée:`-1`par étape pendant que l'un des agents est toujours en mouvement,`+10`Quand ils arriveront tous les deux.`code/main.py`- Je suis désolé .

> Ce cours utilise un 6×6 GridWorld et deux collaborateurs intelligents. Ils doivent sortir de l'angle opposé, ils doivent atteindre un objectif commun.

### Étape 1: l'environnement multi-agent

```python
class CoopGridWorld:
    def __init__(self):
        self.size = 6
        self.goal = (5, 5)

    def reset(self):
        return ((0, 0), (5, 0))  # two agents

    def step(self, state, actions):
        a1, a2 = state
        new1 = move(a1, actions[0])
        new2 = move(a2, actions[1])
        done = (new1 == self.goal) and (new2 == self.goal)
        reward = 10.0 if done else -1.0
        return (new1, new2), reward, done
```

L'espace d'action commun est `|A|² = 16`L'état mondial est de deux positions.

> * unité * un espace d'action`|A|² = 16`L'état de l'ensemble est de deux positions.

### Étape 2: apprentissage Q indépendant

Chaque agent exécute sa propre table Q sur l'état commun. À chaque étape: choisir les actions ε-avides, collecter la transition commune, chaque mise à jour de son propre Q avec la récompense partagée.

```python
def independent_q(env, episodes, alpha, gamma, epsilon):
    Q1, Q2 = defaultdict(default_q), defaultdict(default_q)
    for _ in range(episodes):
        s = env.reset()
        while not done:
            a1 = epsilon_greedy(Q1, s, epsilon)
            a2 = epsilon_greedy(Q2, s, epsilon)
            s_next, r, done = env.step(s, (a1, a2))
            target1 = r + gamma * max(Q1[s_next].values())
            target2 = r + gamma * max(Q2[s_next].values())
            Q1[s][a1] += alpha * (target1 - Q1[s][a1])
            Q2[s][a2] += alpha * (target2 - Q2[s][a2])
            s = s_next
```

Il travaille sur cette tâche parce que les récompenses sont denses et alignées.

> Il est efficace dans cette tâche, car les récompenses sont intenses et étroites.

### Étape 3: Q centralisé avec mise à jour de la valeur décomposée

Utilisez un Q au lieu d' actions conjointes `Q(s, a_1, a_2)`- Mise à jour à partir de la récompense partagée. Décentraliser à l'exécution en marginalisant:`π_i(s) = argmax_{a_i} max_{a_{-i}} Q(s, a_1, a_2)`. Échange d'espace d'action commun exponentiel pour une vision globale *correcte*

> Utilisation d'un espace de travail commun à partir d'un prix de partage

### Étape 4: simple jeu d'auto (agent adversaire 2)

Le même agent, deux rôles.`K`Les épisodes, copier les poids d'A en B. Formation symétrique, progression constante.

> Avec un esprit, deux rôles.`K`Récapitulation du pouvoir d'entraînement de l'A à la B.

## Les pièges

- **Non-stationary replay.**La répétition de l'expérience avec des agents indépendants est pire que le simple agent parce que les anciennes transitions ont été générées par des adversaires désormais obsolètes.
  **非平稳回放。**L'expérience de l'intelligence indépendante est plus mauvaise que celle d'un seul intelligent, car l'ancien transfert est généré par des adversaires du passé.
- **Credit assignment ambiguity.**Récompense partagée après un long épisode; aucun moyen clair de dire quel agent a contribué.
  **信用分配模糊。**长回合后的共享奖励; impossible de déterminer quelles personnes ont contribué à quoi.
- **Policy drift / chasing.**La meilleure réponse de chaque agent change avec la mise à jour de l'autre.
  **策略漂移/追逐。**Le meilleur réactif de chaque organe intelligent est de modifier et de modifier les autres organes intelligents.
- **Reward hacking via coordination.**Les agents trouvent des exploits coordonnés que le concepteur n'a pas anticipés. Les agents d'enchères convergent pour offrir zéro.
  **协调奖励黑客。**智能体发现设计者未预料的协调漏洞──修复:仔细的奖励设计、行为约束──
- **Exploration redundancy.**Les deux agents explorent les mêmes paires d'actions d'état.
  **探索冗余。**两个智能体探索相同状态动作对──修复: 两个智能体探索相同状态动作对──
- **League cycles.**Le jeu pur peut se retrouver dans un cycle de domination.
  **联盟循环。**L'éducation à la culture de l'homme est une forme de formation de l'homme.
- **Sample explosion.** `n`Les agents × espace d'état × actions conjointes. Approximation avec approximation de fonction; espaces d'action facteurés (un chef de sortie de politique par agent).
  **样本爆炸。**n 个智能体 × 状态空间 × 联合动作──用函数近似解决;因子化动作空间──

## Utilisez-le avec le cadre de réalisation

La carte des demandes MARL 2026:

> 2026 années MARL 应用地图:

| Domain | Method | Notes |
|--------|--------|-------|
| Domain / 领域 | Method / 方法 | Notes / 备注 |
| Cooperative navigation / manipulation / 合作导航/操作 | MAPPO / QMIX | CTDE; shared critic + decentralized actors. / CTDE；共享 Critic + 分布式 Actor。 |
| Two-player games (chess, Go, poker) / 双人游戏 | Self-play with MCTS (AlphaZero) | Zero-sum; symmetric training. / 零和；对称训练。 |
| Complex multiplayer (Dota, StarCraft) / 复杂多人游戏 | League play + imitation pretraining | OpenAI Five, AlphaStar. |
| Autonomous-vehicle fleets / 自动驾驶车队 | CTDE MAPPO / PPO with attention | Partial obs; variable team sizes. / 部分可观察；可变团队大小。 |
| Auction markets / 拍卖市场 | Game-theoretic equilibrium + RL | Mean-field RL when `n` → ∞. / n→∞ 时用平均场 RL。 |
| LLM multi-agent systems (Phase 16) / LLM 多智能体系统 | Natural-language comm + role conditioning | RL loop at the agent-planning layer. / Agent 规划层的 RL 循环。 |

En 2026, le domaine de croissance le plus important de MARL est basé sur le MLL: des essaims d'agents de modèle linguistique négociant, débattant, construisant des logiciels.

> Le domaine de la MARL le plus grand développement de 2026 est basé sur le LLM: langage modèle intelligents groupes de discussion, débat, construction de logiciels, RL apparaît sur le niveau de la voie de l'optimisation des préférences de sortie, et non sur le niveau de la marque.

## Envoyez-le . Produit .

- Je ne sais pas .`outputs/skill-marl-architect.md`- Le numéro de la liste:

```markdown
---
name: marl-architect
description: Pick the right multi-agent RL regime (IPPO, CTDE, self-play, league) for a given task.
version: 1.0.0
phase: 9
lesson: 10
tags: [rl, multi-agent, marl, self-play]
---

Given a task with `n` agents, output:

1. Regime classification. Cooperative / adversarial / general-sum. Justify.
2. Algorithm. IPPO / MAPPO / QMIX / self-play / league. Reason tied to coupling tightness and reward structure.
3. Information access. Centralized training (what global info goes to the critic)? Decentralized execution?
4. Credit assignment. Counterfactual baseline, value decomposition, or reward shaping.
5. Exploration plan. Per-agent entropy, population-based training, or league.

Refuse independent Q-learning on tightly-coupled cooperative tasks. Refuse to recommend self-play for general-sum with cycle risks. Flag any MARL pipeline without a fixed-opponent eval (cherry-picked self-play numbers are common).
```

## Les exercices

1. **Easy.**Prenez l'apprentissage indépendant de Q sur la coopérative GridWorld. Combien d'épisodes jusqu'à ce que le retour moyen > 0?
2. **Medium.**Ajouter une tâche de "coordination": l'objectif n'est atteint que lorsque les deux agents y arrivent sur le même virage.
3. **Hard.**Mettre en œuvre un critère centralisé pour la formation de type MAPPO et comparer la vitesse de convergence à la vitesse de PPO indépendante sur la tâche de coordination.

## Les termes clés

| Term | What people say | What it actually means |
|------|-----------------|-----------------------|
| Markov game | "Multi-agent MDP" / 马尔可夫博弈 | `(S, A_1, …, A_n, P, R_1, …, R_n)`; each agent has its own reward. |
| CTDE | "Centralized training, decentralized execution" / 集中训练分布执行 | Joint critic at training time; each agent's policy uses only local obs. |
| IPPO | "Independent PPO" / 独立 PPO | Each agent runs PPO separately. Simple baseline; often underrated. |
| MAPPO | "Multi-agent PPO" / 多智能体 PPO | PPO with a centralized value function conditioned on global state. |
| QMIX | "Monotonic value decomposition" / 单调值分解 | `Q_tot = f_monotone(Q_1, …, Q_n)` allows decentralized argmax. |
| COMA | "Counterfactual multi-agent" / 反事实多智能体 | Advantage = my Q minus expected Q marginalizing over my action. |
| Self-play | "Agent vs past self" / 自我博弈 | Single agent, two roles; standard for zero-sum games. |
| League play | "Population training" / 联盟训练 | Cache past policies, sample opponents from the pool; handles strategy cycles. |

## Encore une lecture

- [Lowe et al. (2017). Multi-Agent Actor-Critic for Mixed Cooperative-Competitive Environments (MADDPG)](https://arxiv.org/abs/1706.02275) CTDE avec un critique centralisé.
- [Foerster et al. (2017). Counterfactual Multi-Agent Policy Gradients (COMA)](https://arxiv.org/abs/1705.08926) contrefactuelles de base pour l'attribution de crédit.
- [Rashid et al. (2018). QMIX: Monotonic Value Function Factorisation](https://arxiv.org/abs/1803.11485) décomposition de la valeur avec monotonie.
- [Yu et al. (2022). The Surprising Effectiveness of PPO in Cooperative Multi-Agent Games (MAPPO)](https://arxiv.org/abs/2103.01955)La PPO est étonnamment forte pour MARL.
- [Vinyals et al. (2019). Grandmaster level in StarCraft II using multi-agent reinforcement learning (AlphaStar)](https://www.nature.com/articles/s41586-019-1724-z) jeu de ligue à l'échelle.
- [Silver et al. (2017). Mastering the game of Go without human knowledge (AlphaGo Zero)](https://www.nature.com/articles/nature24270) pure jeu d'auto dans les jeux à somme nulle.
- [Sutton & Barto (2018). Ch. 15 — Neuroscience & Ch. 17 — Frontiers](http://incompleteideas.net/book/RLbook2020.pdf) comprend le traitement court du manuel des paramètres multi-agents et le problème de non-stationarité que le CTDE est conçu pour résoudre.
- [Zhang, Yang & Başar (2021). Multi-Agent Reinforcement Learning: A Selective Overview](https://arxiv.org/abs/1911.10635) enquête portant sur les LMR coopératives, compétitives et mixtes avec des résultats de convergence.
