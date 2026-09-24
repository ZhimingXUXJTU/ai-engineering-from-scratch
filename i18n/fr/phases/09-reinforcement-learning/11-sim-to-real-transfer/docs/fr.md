# Sim-to-Real transfert  imitation à la réalité de la migration

> Une politique formée dans un simulateur qui échoue sur le matériel est une politique qui mémorise le simulateur.

> **【中文解读】**Si la stratégie de formation dans un simulateur ne peut pas fonctionner sur un matériel réel, il est indiqué qu'elle est " sur-adaptée " à un simulateur.

**Type:** Learn | **类型:** 学习
**Languages:** Python | **语言:** Python
**Prerequisites:** Phase 9 · 08 (PPO), Phase 2 · 10 (Bias/Variance) | **前置知识:** Phase 9 · 08 (PPO), Phase 2 · 10 (偏差/方差)
**Time:** ~45 minutes | **时间:** ~45 分钟

## Le problème , l' introduction du problème

Un vrai robot est lent, dangereux et coûteux. Un bipède a besoin de millions d'épisodes d'entraînement pour apprendre à marcher; un bipède qui tombe même une fois qu'il casse le matériel.

> entraînement Un véritable robot est lent, dangereux et coûteux. Un véritable robot a besoin de millions de trainings pour apprendre à marcher. Un véritable robot peut même tomber une seule fois et endommager des pièces.

Les simulateurs ont des effets négatifs, mais les simulateurs ont tort. Les roulements ont plus de friction que les modèles MuJoCo. Les caméras ont des distorsions de lentilles que le simulateur n'inclut pas. Les moteurs ont des retards, des réactions négatives et une saturation que 99% des modèles sim sautent. Le vent, la poussière et l'éclairage variable sabotent une politique formée sur le rendu stérile.**reality gap** La différence systématique entre la distribution sim et la distribution réelle  est le problème central de la RL déployée pour la robotique.

> Mais les simulateurs sont fausses. Les axes ont plus de frottement que les modèles de MuJoCo. Les simulateurs ne comprennent pas les changements de l'objectif. Les simulateurs ont des retards, des intervalles et des écarts. 99% des simulateurs ont surpassé ces objectifs.**现实鸿沟**La différence systémique entre la répartition simulée et la répartition réelle est le problème central de la RL de la déploiement des machines.

Vous avez besoin d'une politique qui soit *robuste pour le sim-to-real distribution shift*. Trois approches historiques: randomiser le simulateur (randomisation de domaine), adapter la politique avec un peu de données réelles (adaptation / ajustement du domaine), ou identifier les paramètres du système réel et les correspondre (identification du système). En 2026, la recette dominante combine les trois avec une simulation parallèle massive (Isaac Sim, Isaac Lab, Mujoco MJX sur GPU).

> Vous avez besoin d'une stratégie pour imiter la répartition de la répartition de la répartition de la répartition de la répartition de la répartition de la répartition de la répartition de la répartition de la répartition de la répartition de la répartition de la répartition de la répartition de la répartition de la répartition de la répartition de la répartition de la répartition de la répartition de la répartition de la répartition de la répartition de la répartition de la répartition de la répartition de la répartition de la répartition de la répartition de la répartition de la répartition de la répartition de la répartition de la répartition de la répartition de la répartition de la répartition de la répartition de la répartition de la répartition de la répartition de la répartition de la répartition de la répartition de la répartition de la répartition de la répartition de la répartition de la répartition de la répartition de la répartition de la répartition de la répartition de la répartition de la répartition de la répartition de la répartition de la répartition de la répartition de la répartition de la répartition de la répartition de la répartition de la répartition de la répartition de la répartition de la répartition de la répartition de la répartition de la répartition de la répartition de la répartition de la répartition de la répartition de la répartition de la répartition de la répartition de la répartition de la répartition de la répartition de la répartition de la répartition de la répartition de la répartition de la répartition de la répartition de la répartition de la répartition de la répartition de la répartition de la répartition de la répartition de la répartition de la répartition de la répartition de la répartition de la répartition de répartition de la répartition de la répartition de la

> **【中文解读】**"现实沟" est le problème central de la RL des machines. Trois grandes solutions: 1) la régulation du domaine au cours de l'entraînement; 2) la régulation du domaine à lui-même avec une petite quantité de données réelles; 3) la reconnaissance du système.

> **【拓展：域随机化→大模型泛化】**L'idée de l'accumulation de données dans les formations de LLM est également liée à la "répartition d'accumulation de données" dans le cadre de la RLHF.

## Le concept de base.

![Three sim-to-real regimes: domain randomization, adaptation, system identification](../assets/sim-to-real.svg)

**Domain Randomization (DR).**Tobin et al. En 2017, Peng et al. En 2018, il y a eu une récession. Pendant l'entraînement, randomiser tous les paramètres sim qui pourraient différer sur le robot réel: masses, coefficients de friction, gains de PD du moteur, bruit du capteur, position de la caméra, éclairage, textures, modèles de contact. La politique apprend une distribution conditionnelle sur "quel sim est aujourd'hui" et généralise à travers toute la durée. Si le vrai robot est dans le cadre de la formation, la politique fonctionne.

> **域随机化（DR）。**Pendant l'entraînement, chaque simulateur peut être différent de l'ordinateur réel: la qualité, le facteur de friction, l'augmentation du volume des émetteurs de lumière, la position de la position de l'appareil photo, les textures, les modèles de contact.

- **Upside:**Il n'y a pas besoin de données réelles.
  **优点：**Il n'y a pas besoin de données réelles.
- **Downside:**La formation sur randomisée produit une politique "universelle" mais trop prudente.
  **缺点：**L'entraînement excessif à l'accélération produit des stratégies "générales" mais trop conservatrices.

**System Identification (SI).**Si vous pouvez mesurer l'affrontement entre les bras et les articulations sur le robot réel, branchez-le sur le simulateur. Ensuite, entraînez une politique qui s'attend à ces valeurs.

> **系统辨识（SI）。**訓練前将仿真器参数适应到真世界数据──需要接触真实系统但直接缩小现实沟──

**Domain Adaptation.**En train en sim, en réglage avec une petite quantité de données réelles.

> **域自适应。**En simulation, vous pouvez utiliser une petite quantité de données réelles.

- **Real2Sim2Real:**Apprendre un simulateur résiduel `f(s, a, z) - f_sim(s, a)`En utilisant des déploiements réels, entraînons dans le sim correct.
  **Real2Sim2Real：**Avec un véritable déploiement, apprendre à imiter les restes, en train de faire des imitations après les modifications.
- **Observation adaptation:**entraîner une politique qui cartographient un véritable obs → sim-like obs via un extracteur de fonctionnalités appris (par exemple, GAN pixel-à-pixel).
  **观测自适应：**訓練将真实观测映射为仿真式观测的策略──

**Privileged learning / teacher-student.**Miki et coll. 2022 (Annimal quadruped). Formez un *professeur* dans une simulation qui a accès à des informations privilégiées (truth friction au sol, altitude du terrain, dérive IMU). Dédistribuez un *étudiant* qui ne voit que des observations à capteur réel. L'étudiant apprend à déduire des caractéristiques privilégiées de l'histoire, robustes sur les paramètres physiques.

> **特权学习/教师-学生。**Dans le simulaire entraînement ayant le droit de voir les informations privilégiées des * enseignants*──蒸 one only see the true sensors observations de * étudiant*── étudiant de l'histoire

**Massively parallel simulation.**Isaac Lab, Mujoco MJX, Brax exécutent tous des milliers de robots parallèles sur un seul GPU. PPO avec 4 096 humanoïdes parallèles recueille des années d'expérience en quelques heures.

> **大规模并行仿真。**2024-2026 année。Isaac Lab、Mujoco MJX、Brax sur un seul GPU fonctionne sur des milliers de mécanismes de parcours。PPO  associé à 4 096 mécanismes de parcours humains  personnalisé  personnalisé  personnalisé  personnalisé  personnalisé  personnalisé  personnalisé  personnalisé  personnalisé  personnalisé  personnalisé  personnalisé  personnalisé  personnalisé  personnalisé  personnalisé  personnalisé  personnalisé  personnalisé  personnalisé  personnalisé  personnalisé  personnalisé  personnalisé  personnalisé  personnalisé  personnalisé  personnalisé  personnalisé  personnalisé  personnalisé  personnalisé  personnalisé  personnalisé  personnalisé  personnalisé  personnalisé  personn

**The real-world 2026 recipe (quadruped walking example):**

1. Simulation parallèle avec gravité randomisée, friction, gain moteur, charge utile.
2. Politique des enseignants formés avec des informations privilégiées (carte du terrain, vérité sur la vitesse du corps au sol).
3. Les politiques étudiantes distillées de l'enseignant en utilisant uniquement la proprioception (encodateurs des articulations des jambes).
4. Adaptation optionnelle de l'observation par autoencodeur sur l'UIM réel.
5. Déployer, ne pas tirer sur plus de 10 environnements, et si ça ne marche pas, faire quelques minutes de réglage réel avec PPO.

> **真实世界 2026 年方案（四足行走示例）：**Les résultats de la formation sont les suivants:

## Construisez-le et mettez-le en œuvre.
```figure
f3-reality-gap
```

## Faites-le

Le code de cette leçon est une petite démonstration de la randomisation de domaine sur un GridWorld avec des transitions * bruyantes *. Nous entraînons une politique qui expérimente des probabilités de glissement randomisées dans "sim" et évalue sur "réel" avec un niveau de glissement qu'il n'a jamais vu lors de la formation.

> Le code de ce cours est une petite démonstration de l'arrangement des zones de GridWorld avec des mouvements de bruit. Nous avons pratiqué une stratégie de probabilité d'arrangement des mouvements dans une "imitable" expérience et évalué "vraiment" le niveau de roulement jamais vu dans l'entraînement. Cette structure est directement mappée à MuJoCo jusqu'à la migration du matériel.

### Étape 1: sim paramétrifié

```python
def step(state, action, slip):
    if rng.random() < slip:
        action = random_perpendicular(action)
    ...
```

`slip`En robotique réelle, il pourrait s'agir de friction, de masse, de gain moteur, tout ce qui se déplace entre sim et réel.

> `slip`Il peut y avoir des effets de friction, de qualité, de gain électronique, de variation entre la réalité et la réalité.

### Étape 2: entraînement avec DR

Au début de chaque épisode, échantillon `slip ~ Uniform[0.0, 0.4]`- Prenez le PPO, l'apprentissage Q, tout.

> Chaque fois que tu commences, tu fais comme ça.`slip ~ Uniform[0.0, 0.4]` entraînement PPO/Q-learning/ tout algorithme

### Étape 3: évaluer les tirages zéro sur les feuilles "réelles"

Évaluer `slip ∈ {0.0, 0.1, 0.2, 0.3, 0.5, 0.7}`- les quatre premiers sont placés dans le cadre d'un soutien à la formation; `0.5`et `0.7`Une politique de formation en DR devrait rester presque optimale à l'intérieur du support et dégrader gracieusement à l'extérieur.

> Dans le`slip ∈ {0.0, 0.1, 0.2, 0.3, 0.5, 0.7}`上评估──前四在训练支内;`0.5`et `0.7`La stratégie de formation en DR doit être maintenue à l'intérieur de la branche, à l'extérieur de la formation en DR doit être maintenue à l'extérieur.

### Étape 4: comparer à une formation étroite

Formez une deuxième politique avec `slip = 0.0`- Je ne peux pas le faire.`slip`Vous devriez voir une chute catastrophique dès que le glissement réel > 0.

> - Je veux le faire .`slip = 0.0`trainement de deuxième stratégie  dans la même gamme de mouvement  évaluation  lorsque le mouvement réel > 0  devrait voir la catastrophe décroître

## Les pièges

- **Too much randomization.**Le train est en marche .`slip ∈ [0, 0.9]`et votre politique est si averse au risque qu'elle n'essaie jamais de suivre le chemin optimal.
  **过度随机化。**Dans le`slip ∈ [0, 0.9]`La formation, la stratégie est trop préventive et ne tente pas de trouver le meilleur chemin.
- **Too little randomization.**Traînez sur une tranche mince et la politique ne peut pas être généralisée du tout. Utilisez un programme adaptatif (Randomisation automatique de domaine) qui élargit la distribution à mesure que la politique s'améliore.
  **过少随机化。**En ce qui concerne les techniques de formation, la stratégie est totalement impossible à généraliser.
- **Misidentified parameter space.**Remplissez le mauvais truc (tune de la caméra quand le vrai écart est le retard moteur) et DR n'aide pas.
  **错误识别参数空间。**Il y a des erreurs dans la réaction.
- **Privileged info leakage.**Un enseignant qui utilise l'état global pour des actions, pas seulement des observations, peut produire un élève qui ne peut pas le rattraper.
  **特权信息泄漏。**Les enseignants qui font des mouvements en utilisant l'état de l'ensemble peuvent avoir des étudiants incapables de les suivre.
- **Sim-to-sim transfer failure.**Si votre politique n'est pas robuste à une variante sim plus difficile, elle ne sera pas robuste au monde réel non plus.
  **仿真到仿真迁移失败。**Si la stratégie de mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise de la mise en œuvre de la mise en œuvre de la mise de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en en en en.
- **No real-world safety envelope.**Une politique qui fonctionne en sim et "fonctionne en réalité" sans un bouclier de sécurité de faible niveau peut toujours briser le matériel.
  **无真实世界安全包络。**Il n'y a pas de stratégie de protection de sécurité de faible niveau qui puisse encore endommager le matériel.

## Utilisez-le avec le cadre de réalisation

La série sim-to-real de 2026:

> 2026: La technologie de l'information est mise à jour

| Domain | Stack |
|--------|-------|
| Domain / 领域 | Stack / 技术栈 |
| Legged locomotion (ANYmal, Spot, humanoid) / 腿式运动 | Isaac Lab + DR + privileged teacher / student |
| Manipulation (dexterous hands, pick-and-place) / 操作 | Isaac Lab + DR + DR-GAN for vision |
| Autonomous driving / 自动驾驶 | CARLA / NVIDIA DRIVE Sim + DR + real fine-tune |
| Drone racing / 无人机竞速 | RotorS / Flightmare + DR + online adaptation |
| Finger/in-hand manipulation / 手指/手内操作 | OpenAI Dactyl (DR at unprecedented scale) |
| Industrial arms / 工业机械臂 | MuJoCo-Warp + SI + small real fine-tune |

Pour le contrôle à toutes les échelles, le flux de travail est cohérent: adapter le sim le mieux possible, randomiser ce que vous ne pouvez pas adapter, entraîner des politiques énormes, distiller, déployer avec un bouclier de sécurité.

> Pour tous les contrôles de taille, le flux de travail est conforme: autant que possible pour s'adapter à la réalité, autant que possible pour s'adapter à la réalité, autant que possible pour s'adapter à la réalité,

## Envoyez-le . Produit .

- Je ne sais pas .`outputs/skill-sim2real-planner.md`- Le numéro de la liste:

```markdown
---
name: sim2real-planner
description: Plan a sim-to-real transfer pipeline for a given robot + task, covering DR, SI, and safety.
version: 1.0.0
phase: 9
lesson: 11
tags: [rl, sim2real, robotics, domain-randomization]
---

Given a robot platform, a task, and access to real hardware time, output:

1. Reality gap inventory. Suspected sources ranked by expected impact (contact, sensing, actuation delay, vision).
2. DR parameters. Exact list, ranges, distribution. Justify each range against real measurements.
3. SI steps. Which parameters to measure; measurement method.
4. Teacher/student split. What privileged info the teacher uses; what obs the student uses.
5. Safety envelope. Low-level limits, emergency stops, backup controller.

Refuse to deploy without (a) a zero-shot sim-variant test, (b) a safety shield, (c) a rollback plan. Flag any DR range wider than 3× measured real variability as likely over-randomized.
```

## Les exercices

1. **Easy.**Formez un agent Q-apprentissage sur le GridWorld à glissement fixe (slip=0.0).
2. **Medium.**Formation d' un agent d' apprentissage DR Q`slip ~ Uniform[0, 0.3]`- Combien DR achète à slip=0,5 (en dehors de la distribution)?
3. **Hard.**Mettre en œuvre un programme: commencer par slip=0,0, élargir la plage DR chaque fois que la politique atteint 90% de l'optimal. Mesurer les étapes de l'environnement totale pour atteindre slip=0,3 nul-shot par rapport à une plage de base DR fixe.

## Les termes clés

| Term | What people say | What it actually means |
|------|-----------------|-----------------------|
| Reality gap | "Sim-to-real difference" / 现实鸿沟 | Distribution shift between training and deployment physics/sensing. |
| Domain randomization (DR) | "Train across random sims" / 域随机化 | Randomize sim parameters during training so policy generalizes. |
| System identification (SI) | "Measure real and fit sim" / 系统辨识 | Estimate real physical parameters; set sim to match. |
| Domain adaptation | "Fine-tune on real data" / 域自适应 | Small real-world fine-tune after sim training; may adapt obs or dynamics. |
| Privileged info | "Ground truth for teacher" / 特权信息 | Information only the sim has; student must infer it from obs history. |
| Teacher/student | "Distill privileged -> observable" / 教师-学生蒸馏 | Teacher trained with shortcuts; student learns to mimic without them. |
| ADR | "Automatic Domain Randomization" / 自动域随机化 | Curriculum that widens DR ranges as the policy improves. |
| Real2Sim | "Close the gap with real data" / 现实到仿真 | Learn a residual to make the sim mimic real rollouts. |

## Encore une lecture

- [Tobin et al. (2017). Domain Randomization for Transferring Deep Neural Networks from Simulation to the Real World](https://arxiv.org/abs/1703.06907) le document original de DR (vision pour la robotique).
- [Peng et al. (2018). Sim-to-Real Transfer of Robotic Control with Dynamics Randomization](https://arxiv.org/abs/1710.06537) DR pour la dynamique, la locomotion quadruple.
- [OpenAI et al. (2019). Solving Rubik's Cube with a Robot Hand](https://arxiv.org/abs/1910.07113) Dactyl, ADR à l'échelle.
- [Miki et al. (2022). Learning robust perceptive locomotion for quadrupedal robots in the wild](https://www.science.org/doi/10.1126/scirobotics.abk2822) enseignant-étudiant pour ANYmal.
- [Makoviychuk et al. (2021). Isaac Gym: High Performance GPU Based Physics Simulation for Robot Learning](https://arxiv.org/abs/2108.10470) la simulation massiquement parallèle qui conduit les déploiements 2025-2026.
- [Akkaya et al. (2019). Automatic Domain Randomization](https://arxiv.org/abs/1910.07113) Métode du programme d'ADR.
- [Sutton & Barto (2018). Ch. 8 — Planning and Learning with Tabular Methods](http://incompleteideas.net/book/RLbook2020.pdf) le cadrage Dyna (utiliser un modèle pour la planification + les déploiements) qui sous-tend les pipelines sim-to-real modernes.
- [Zhao, Queralta & Westerlund (2020). Sim-to-Real Transfer in Deep Reinforcement Learning for Robotics: a Survey](https://arxiv.org/abs/2009.13303) taxonomie des méthodes sim-to-real avec des résultats de référence.
