# Optimisation de l'équipe pour les LLM (PSO, ACO) 优化群体 PSO ACO LLM

> L'optimisation bio-inspirée fait un retour à la maîtrise de la loi. **LMPSO**(arXiv:2504.09247) utilise PSO où la vitesse de chaque particule est un prompt et le LLM génère le candidat suivant; fonctionne bien sur les sorties de séquences structurées (expressions mathématiques, programmes). **Model Swarms**(arXiv:2410.11163) traite chaque expert LLM comme une particule PSO sur un modèle-poids variété et rapports **13.3% average gain**plus de 12 lignes de base sur 9 ensembles de données avec seulement 200 instances. **SwarmPrompt**(ICAART 2025) hybride PSO + Grey Wolf pour une optimisation rapide. **AMRO-S**(arXiv:2603.12933) est un spécialiste des phéromones inspiré par l'ACO pour le parcours LLM multi-agent  **4.7x speedup**Cette leçon met en œuvre le PSO sur l'espace paramétrique rapide et le ACO sur l'itinérance des agents, mesure pourquoi ces algorithmes classiques correspondent à l'ère du LLM et quand ils ne le font pas.

> **【中文解读】**Ce chapitre présente les algorithmes d'optimisation de groupes PSO particulaires group) et ACO group) et les applications de la bioinitiation de l'optimisation dans plusieurs agents 

> **【拓展：swarm optimization pso aco→具体应用】**群体优化算法在多代理中的应用:(1) 粒子群优化(PSO) Agent 根据自身最佳位置和全局最佳位置调整搜索方向;(2) 群群优化(ACO) Agent 通过信息素标记好的路径,后者倾向于跟随强信息素路径──这些算法适应大规模搜索空间中的优化问题,如 Agent 任务分配和路径规划──


**Type:** Learn + Build | **类型:** 学习 + 构建
**Languages:** Python (stdlib) | **语言:** Python（标准库）
**Prerequisites:** Phase 16 · 09 (Parallel Swarm Networks), Phase 16 · 14 (Consensus and BFT) | **前置知识:** Phase 16 · 09（并行群体网络），Phase 16 · 14（共识与 BFT）

>  **【前置】**Les techniques de gestion de la biodiversité sont les plus utilisées dans les domaines de l'éducation et de la santé.
>  **【类比】**LLM + PSO/ACO = "群找最佳 prompt"──PSO = Chaque agent est une particule, la vitesse=prompte, vers la totalité de la région;ACO = Agent dans le prompt 空间留下信息素,后者跟随强信息素──LMPSO 适合结构化输出(mathematical expression、代码);Model Swarms Place chaque LLM 专家当粒子,比12个基线平均高13.3%;AMRO-S avec ACO faire agent 路由,4.7 倍加速──
**Time:** ~75 minutes | **时间:** ~75 分钟

## ♪ Problème ♪ Introduction du problème ♪

Vous avez un prompt qui marque 62% sur votre évaluation de tâche. Vous voulez l'améliorer. Le mouvement naïf est le tweaking manuel sans gradient, qui évolue mal. L'apprentissage du renforcement a besoin de signaux de récompense et de déploiements suffisants pour s'entraîner. Backprop à travers les prompt n'est pas vraiment possible  le prompt est une chaîne discrète, pas un paramètre différenciable.

> Vous avez une suggestion dans l'évaluation des tâches qui a obtenu 62% de points. Vous souhaitez l'améliorer. Une méthode simple est la réglage manuelle sans degré, la différence de dilatation.

L'optimisation classique bio-inspirée  PSO pour les espaces de recherche continus, ACO pour la sélection de chemin  a été conçue exactement pour ce régime: sans gradient, basé sur la population, bon marché par évaluation.

> L'optimisation biologique classique est utilisée pour l'espace de recherche continue, l'ACO est utilisé pour la sélection de routes qui sont conçues pour ce scénario: sans gradient, basé sur le groupe de personnes, à faible coût de chaque évaluation.

Les mêmes schémas s'appliquent au routage des agents dans les systèmes multi-agents. Un phéromone de type ACO enregistre la piste de l'agent qui a travaillé le mieux sur quel type de tâche, permet au routeur d'exploiter la piste et décompose les phéromones afin que les routes puissent être redécouvertes.

> Le même modèle s'applique à l'agent dans le système multi-agent * route*。ACO 风格的信息素轨迹记录哪个代理在哪个任务类型上表现最好,让路由器利用轨迹,并减弱信息素以便重新发现路径。

## Concept Le concept central

### Récupération de l'OPS (Kennedy & Eberhart 1995)

Optimisation de l'accumulation de particules: population de particules dans un espace de recherche continu.`x_i`et la vitesse `v_i`- Chaque itération:

```
v_i <- w * v_i + c1 * r1 * (p_best_i - x_i) + c2 * r2 * (g_best - x_i)
x_i <- x_i + v_i
evaluate fitness(x_i)
update p_best_i if improved
update g_best if global best
```

Où ?`p_best`est le meilleur de la particule,`g_best`est le meilleur de swarm, `w, c1, c2`sont l'inertie + les poids cognitifs + les poids sociaux, `r1, r2`sont des facteurs aléatoires.

### PSO sur les résultats de la LLM  LMPSO

Le programme d'exécution de la vitesse est un programme de détection de la vitesse de détection de la vitesse. le programme d'exécution de la vitesse est un programme de détection de la vitesse de détection de la vitesse.

Cela fonctionne bien lorsque:
- La sortie est structurée (perçable, évaluable).
  Le texte est écrit en français.
- La condition physique est automatique (expérience, évaluation arithmétique).
  Le nombre de tests effectués est de 1,00 à 1,00 par jour.
- La population est petite (~10-30 particules) et les appels LLM totaux restent gérables.
  Le nombre de particules est de 10 à 30 particules.

Il ne fonctionne pas bien lorsque la forme physique a besoin d'un examen humain  le coût de la réitération devient prohibitif.

> Lorsque l'adaptation nécessite une inspection artificielle, l'effet est mauvais.

### Des essaims modèles

Le nombre de particules est de 12 lignes de base sur 9 ensembles de données, avec seulement 200 instances par itération.

L'idée clé est que les modèles experts de la LLM sont déjà proches dans un variété de paramètres partagés (poids d'adaptateur, delta de LoRA).

### Récupération de l'ACO (Dorigo 1992)

Optimisation de la colonie de fourmis: les fourmis traversent un graphique; chaque chemin a une trace de phéromones. Les fourmis déplacent les probabilités de poids par la force des phéromones. Les fourmis qui terminent la tâche déposent des phéromones proportionnellement à la qualité de la solution. Les phéromones se décomposent avec le temps.

### AMRO-S  ACO pour le routage des agents

Le phéromone est un phéromone qui renforce les routes qui produisent de bons résultats.

- **Interpretable routing evidence.**La force des phéromones est un signal lisible par l'homme.
  Le mot grec traduit par " le mot grec "**可解释的路由证据。**La force de l'information est un signal lisible par l'homme.
- **Quality-gated asynchronous update.**Les phéromones ne se mettent à jour qu'après la réussite des contrôles de qualité, déconnectant les inférences de l'apprentissage.
  Le mot grec traduit par " le mot grec "**质量门控异步更新。**L'information ne sera mise à jour qu'après examen de qualité, et sera considérée comme une solution d'apprentissage.
- **4.7x speedup**sur le point de référence de routage multi-agents.
  En français, traduit par " dans le monde "**4.7 倍加速**Il y a une autre.

La qualité est importante: sans elle, les agents rapides mais mal conçus accumulent des phéromones, et le système s'enferme sur de mauvaises voies.

> La qualité est importante: sans elle, l'agent rapide mais erroné accumule des informations, le système est bloqué sur un mauvais chemin.

### Quand utiliser le PSO / ACO pour les LLM

**Use PSO when:**
- L'espace de recherche est continu ou des cartes à des paramètres continu (embeddings de prompt, poids LoRA, paramètres de génération numérique).
  Le nombre de paramètres générés est de 0,9 à 0,9 par rapport à la taille de la structure.
- Le fitness est bon marché et automatique.
  Traduction anglaise:适应度评估廉价且自动──
- La population peut être petite (10-30).
  Le groupe peut être très petit.

**Use ACO when:**
- Vous avez un problème de routage ou de sélection de chemin.
  Vous avez un chemin ou un chemin de choix.
- Les décisions se renforcent au fil du temps (les mêmes types de tâches reviennent).
  Le même type de tâche revient).
- Vous avez besoin de preuves interprétables pour les décisions de routage.
  Vous avez besoin de preuves explicatives de la décision.

**Do not use either when:**
- La forme physique nécessite une révision humaine (trop coûteuse par itération).
  Le récit de la Bible est un récit de la vie de Jésus.
- L'espace de recherche est discrète et combinatoire de manière à ne pas être couvert par le PSO (utiliser des algorithmes génétiques à la place).
  Le système de recherche est un système de recherche qui est décentralisé.
- Les décisions en temps réel nécessitent une latence stricte (convergence PSO/ACO lentement par rapport aux heuristiques à passage unique).
  Le processus de prise de décision nécessite une grande retardation.

### Pourquoi l'inspiration biologique gagne toujours

Les méthodes basées sur les gradients ont besoin de signaux différenciables. Les résultats du LLM et les décisions de routage ne sont pas trivialement différenciables.

PSO et ACO n'ont besoin que d'une fonction d'évaluation. Si vous pouvez marquer une sortie de candidat ou une décision de routage, vous pouvez optimiser l'espace. Cela rend la barre d'applicabilité beaucoup plus faible.

### Limits pratiques

- **Population budget.**N particules × T itérations × coût par éval. Pour les évaluations LLM à ~$0.02 / call, a 20-particle PSO running 50 iterations costs ~$20 - Planifiez en conséquence.
- **Exploration vs exploitation.**Le taux de décomposition des phéromones et l'inertie de l'OPS se décompensent; décomposition trop rapide → oubli de solutions; trop lent → collé à l'optima locale précoce.
- **Catastrophic drift.**Les deux algorithmes peuvent converger et ensuite diverger si le paysage de la condition physique change (nouvelle distribution de données).

## Construisez-le en main
```figure
swarm-stigmergy
```

## Faites-le

`code/main.py`les implémentations:

- `LMPSO` PSO sur les paramètres numériques de prompt (température, poids top_k). La "génération LLM" de chaque particule est simulée comme une fonction de conditionnement scriptée.
- `AMRO_S` Routage à la mode ACO. 3 agents, 4 types de tâches, matrice phéromone, 100 tâches routées.
- Comparaison: routage aléatoire par rapport au routage ACO sur le même flux de tâches. Mesure la qualité et la latence.

Je vais courir .

```
python3 code/main.py
```

Résultats attendus:
- LMPSO: g_best fitness s'améliore de façon aléatoire à presque optimale sur 30 itérations.
- AMRO-S: la table des phéromones se stabilise sur le bon agent par type de tâche; le routage ACO bat au hasard de ~ 30 à 40% sur la qualité et réduit également la latence (moins de retries).

## Utilisez-le.

`outputs/skill-swarm-optimizer.md`aide à choisir entre les algorithmes génétiques, les algorithmes de PSO et les optimisateurs basés sur les gradients pour les problèmes d'optimisation de l'agent.

## Envoyez-le en ligne .

- **Start small.**10 à 20 particules, 20 à 50 itérations.
  Le mot grec traduit par " le mot grec "**从小开始。**10-20 particules, 20 à 50 fois, mais seulement une augmentation visible de la courbe de réception et une expansion.
- **Log pheromones or g_best per iteration.**Débarrasser les optimisateurs sans trace est douloureux.
  Le mot grec traduit par " le mot grec "**每次迭代记录信息素或 g_best。**Il n'y a pas de chemin à parcourir.
- **Quality-gate updates.**Surtout pour le routage ACO: les agents rapides et mal conçus ne doivent pas accumuler de phéromone.
  Le mot grec traduit par " le mot grec "**质量门控更新。**En particulier, l'ACO: Rapide mais erroné Agent incapable de recueillir des informations.
- **Reset decay on distribution shift.**Lorsque la distribution de votre évaluation change, les phéromones vieillissants sont stériles; réinitialisez ou doublons temporairement le taux de décomposition.
  Le mot grec traduit par " le mot grec "**分布偏移时重置衰减。**Lorsque l'évaluation des changements de distribution, le taux de déclin du vieillissement de l'information est passé; le taux de réarrangement ou de réapprovisionnement temporaire.
- **Cap the per-iteration cost.**Émettez une métrique de coût par itération. PSO qui coûte 500 $ / itération et gagne 0,5% n'est pas expédible.
  Le mot grec traduit par " le mot grec "**限制每次迭代成本。**发发出每次代成本指标──每次代花费$500 且只增加0.5% 的PSO不可发行──

## Les exercices

1. On court .`code/main.py`- Observez la convergence de l'OMPSO. La taille de la population varie 5, 10, 20, 50.
2. La fonction de fitness est modifiée après l'itération 30.`p_best`- Je peux vous aider ?
3. Ajouter une passerelle de qualité à AMRO-S: dépôt de phéromone uniquement sur les courses avec un score d'évaluation > 0,7. Comment cela change-t-il la convergence par rapport à la version non-gérée?
4. Lire LMPSO (arXiv:2504.09247). Mettez la "vitesse comme une demande" du papier à votre vitesse numérique.
5. Lisez AMRO-S (arXiv:2603.12933). Implémenter le " chemin rapide d'inférence " déconnecté avec la mise à jour phéromonique asynchrone. Comment cela change-t-il la latence du système sous charge soutenue ?

## Les termes clés

| Term | What people say | What it actually means |
|------|----------------|------------------------|
| PSO / 粒子群优化 | "Particle Swarm Optimization" / "粒子群优化" | Kennedy-Eberhart 1995. Population-based gradient-free optimizer. / Kennedy-Eberhart 1995。基于种群的无梯度优化器。 |
| ACO / 蚁群优化 | "Ant Colony Optimization" / "蚁群优化" | Dorigo 1992. Path/route optimization via pheromone trails. / Dorigo 1992。通过信息素轨迹的路径/路由优化。 |
| LMPSO / LLM 粒子群 | "PSO with LLM generation" / "LLM 生成的 PSO" | arXiv:2504.09247. Velocity is a prompt; LLM produces candidates. / arXiv:2504.09247。速度是提示；LLM 生成候选。 |
| Model Swarms / 模型群体 | "PSO on expert weights" / "专家权重的 PSO" | arXiv:2410.11163. Gradient-free update on model parameter subspace. / arXiv:2410.11163。模型参数子空间上的无梯度更新。 |
| AMRO-S / ACO Agent 路由 | "ACO for agent routing" / "Agent 路由的 ACO" | arXiv:2603.12933. Pheromone matrix over task-type × agent. / arXiv:2603.12933。任务类型 × Agent 的信息素矩阵。 |
| p_best / g_best / 个体最优/全局最优 | "Personal / global best" / "个人/全局最优" | Per-particle and swarm-wide best solutions found so far. / 每个粒子和群体目前找到的最优解。 |
| Pheromone / 信息素 | "Routing memory" / "路由记忆" | Strength on an edge; decays over time; deposits on quality. / 边上的强度；随时间衰减；按质量沉积。 |
| Quality-gated update / 质量门控更新 | "Only learn from good runs" / "只从好的运行学习" | Pheromone deposit conditioned on quality check. / 以质量检查为条件的信息素沉积。 |
| Catastrophic drift / 灾难性漂移 | "Distribution shift" / "分布偏移" | Fitness landscape changes; old p_best and pheromones become stale. / 适应度景观变化；旧的 p_best 和信息素变得过时。 |

## Encore une lecture

- [Kennedy & Eberhart — Particle Swarm Optimization](https://ieeexplore.ieee.org/document/488968) le document de l'OPS de 1995
- [Dorigo — Ant Colony Optimization](https://www.aco-metaheuristic.org/about.html) Fondations de l'ACO 1992
- [LMPSO — Language Model Particle Swarm Optimization](https://arxiv.org/abs/2504.09247) OPS pour les résultats structurés de la LLM
- [Model Swarms — gradient-free LLM expert optimization](https://arxiv.org/abs/2410.11163) PSO sur le sous-espace de poids de modèle
- [AMRO-S — ant-colony multi-agent routing](https://arxiv.org/abs/2603.12933) routage à phéromone avec passerelle de qualité
