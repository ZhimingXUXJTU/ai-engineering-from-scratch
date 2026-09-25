# La théorie de l'esprit et de la coordination émergente

> Li et collègues (arXiv:2310.10701) ont montré que les agents de LLM dans une exposition de jeu de texte coopérative **emergent high-order Theory of Mind**(ToM)  raisonner sur ce qu'un autre agent croit sur les croyances d'un troisième agent  mais échouer à la planification à long terme en raison de la gestion du contexte et des hallucinations. Riedl (arXiv:2510.05174) a mesuré la synergie d'ordre supérieur dans une population et a constaté que **only**La condition ToM-prompt produit une différenciation liée à l'identité et une complémentarité axée sur l'objectif; les LLM de faible capacité ne montrent que l'émergence fausse. C'est-à-dire que l'émergence de la coordination est immédiate et conditionnelle et dépend du modèle, pas gratuite. Cette leçon met en œuvre un agent minimal conscient de la MTO, exécute une tâche de coopération avec et sans l'intervention de la MTO et mesure le delta de coordination par rapport au protocole Riedl 2025.

> **【中文解读】**Ce chapitre présente le mécanisme de coordination de la théorie de l'esprit, de la compréhension et de la prédiction des autres agents.

> **【拓展：theory of mind coordination→具体应用】**La théorie du mental (心智理論) est la capacité de comprendre et de prédire l'état psychologique des autres. Dans le système multi-agent, l'agent doté de la théorie du mental peut mieux coordonner. Il sait que les autres agents savent quoi, ce qu'ils veulent, ce qu'ils vont faire. Des études réalisées en 2025-2026 montrent que l'intention d'un autre agent peut améliorer considérablement l'efficacité de la coordination, mais aussi augmenter les coûts de calcul.


**Type:** Learn + Build | **类型:** 学习 + 构建
**Languages:** Python (stdlib) | **语言:** Python（标准库）
**Prerequisites:** Phase 16 · 07 (Society of Mind and Debate), Phase 16 · 17 (Generative Agents) | **前置知识:** Phase 16 · 07（心智社会与辩论），Phase 16 · 17（生成式 Agent）

>  **【前置】**Je suis en train de faire une étude sur la nature de l'esprit.
>  **【类比】**Il est en train de se lancer dans une nouvelle série de projets de développement de l'industrie automobile, qui a été lancée en 2025.
**Time:** ~75 minutes | **时间:** ~75 分钟

## ♪ Problème ♪ Introduction du problème ♪

La coordination multi-agents semble souvent magique: les agents divisent le travail, s'anticipent les uns les autres, évitent la redondance. Généralement, cette "émergence" est un artifact de l'ingénierie rapide  quelqu'un a dit aux agents de "coordonner".

> Il est généralement dit à l'agent de "coordonner" (en anglais: "coordination"), qu'il doit "éliminer" (en anglais: "coordination").

La conclusion de Riedl en 2025 est plus stricte: dans des conditions contrôlées, la coordination ne se produit que lorsque les agents sont amenés à raisonner sur **other agents' minds**(ToM). Sans le prompt ToM, même les modèles forts montrent des modèles de coordination qui ne survivent pas aux contrôles statistiques.

> Résultats de la recherche de 2025 plus stricte: dans des conditions de contrôle, coordonnons uniquement l'agent est invité à recommander**其他 Agent 的心理**(ToM) 才涌现――没有ToM 提示, même si un modèle fort montre un modèle de coordination non existant sous contrôle statistique―― cela est important pour la production: la fonction " multi agent 协调 " de la publication de l'équipe dépend de la suggestion et est fragile――

Cette leçon traite le ToM comme une capacité spécifique (réflexion sur les croyances sur les croyances), construit un agent minimal conscient du ToM et mesure à quoi ressemble la véritable coordination par rapport à ce que ressemble le dressage rapide.

> Ce cours va voir le TOM comme une capacité spécifique à raisonner sur les croyances de la croyance, à construire un agent de perception minimal du TOM, et à mesurer la différence entre la coordination réelle et la conception de la suggestion.

## Concept Le concept central

### Ce que signifie le TOM

Psychologie du développement: un enfant de 3 ans pense que le monde intérieur de chacun correspond à celui de l'autre. Un enfant de 5 ans comprend que les autres ont des croyances différentes. Un enfant de 7 ans explique les croyances sur les croyances ("elle pense que je pense que la balle est sous la tasse ").

> 发展心理学: un enfant de 3 ans pense que tout le monde est dans son cœur et qu'il est le même que lui-même. Un enfant de 5 ans comprend que les autres ont des croyances différentes. Un enfant de 7 ans pense que la foi est une croyance.

Pour les agents de LLM, ToM commande une carte à:

> Pour les agents de la LLM, vous devez:

- **Zeroth-order:**L'agent agit uniquement sur ses propres observations.
  Le mot grec traduit par " le mot grec "**零阶：**Il n'y a pas de modèle pour les autres.
- **First-order:**"Alice croit à X".
  Le mot grec traduit par " le mot grec "**一阶：**L'agent a une croyance pour chaque autre agent.
- **Second-order:**"Alice croit que Bob croit à X".
  Le mot grec traduit par " le mot grec "**二阶：**"Alice a dit à Bob qu'elle avait fait confiance à X".

Li et collègues 2023 ont constaté que les ToM de premier et de deuxième ordre émergent dans les agents de LLM dans les jeux coopératifs, mais se dégradent avec un long horizon et une communication peu fiable.

> Li et autres ont découvert en 2023 que le premier et deuxième étapes de la formation en droit de l'homme sont en plein essor dans le jeu de coopération, mais ont été réduites à un niveau de communication indéfectible et de longue durée.

### Le test Sally-Anne, en bref

Un test de fausse croyance de 1985: Sally met un marbre dans le panier A, quitte. Anne le déplace dans le panier B. Où va Sally regarder quand elle revient?

> Il y a eu une autre épreuve de foi dans le monde de l'éducation.

Les LLM de l'ère GPT-4 passent des tests de style Sally-Anne lorsqu'ils sont posés clairement. Ils échouent lorsque le récit est long, la scène change plusieurs fois ou que la question est formulée indirectement.

> Le programme de l'équipe de gestion de la gestion des ressources humaines (LLC) de GPT-4 est un programme de gestion de ressources humaines qui a été mis en œuvre par le gouvernement de l'État de l'État de l'État de l'État de l'État de l'État de l'État de l'État de l'État de l'État de l'État de l'État de l'État de l'État de l'État de l'État de l'État de l'État de l'État de l'État de l'État de l'État de l'État de l'État de l'État de l'État de l'État de l'État de l'État de l'État de l'État de l'État de l'État de l'État de l'État de l'État de l'État de l'État de l'État de l'État de l'État de l'État de l'État de l'État de l'État de l'État de l'État de l'État de l'État de l'État de l'État de l'État de l'État de l'État de l'État de l'État de l'État de l'État de l'État de l'État de l'État de l'État de l'État de l'État de l'État de l'État de l'État de l'État de l'État de l'État de l'État de l'État de l'État de l'État de l'État de l'État de l'État de l'État de l'État de l'État de l'État de l'État de l'État de l'État de l'État de l'État de l'État de l'État de l'État de l'État de l'État de l'État de l'État de l'État de l'État de l'État de l'État de l'État de l'État de l'État de l'État de l'État de l'État de l'État de l'État de l'État de l'État de l'État de l'État de l'État de l'État de l'État de l'État de l'État de l'État de l'État de l'État

### Mesure de coordination de Riedl

Riedl (arXiv:2510.05174) a construit un test à l'échelle de la population: N agents, objectif de coopération, conditions de prompt variable.

> Riedl(arXiv:2510.05174) a construit un groupe de taille:

1. **Identity-linked differentiation.**Les agents développent-ils des différences de rôles stables au fil du temps?
   Le mot grec traduit par " le mot grec "**身份关联分化。**L'agent a-t-il un rôle à jouer ?
2. **Goal-directed complementarity.**Les actions des agents se complètent-elles mutuellement (sous-tâches différentes) plutôt que de se dupliquer?
   Le mot grec traduit par " le mot grec "**目标导向互补性。**Le comportement de l'agent est-il complémentaire à celui des autres tâches ?
3. **Higher-order synergy.**Une mesure statistique de la réussite d'un groupe par rapport à un sous-ensemble.
   Le mot grec traduit par " le mot grec "**高阶协同。**Les groupes ont-ils atteint des statistiques que aucun groupe n'a pu atteindre ?

Résultat: seulement dans la condition de prompt ToM les trois indicateurs produisent un signal au-dessus de la ligne de base. Sans prompt ToM, les indicateurs hover près de chance pour les modèles de capacité modérée.

> Résultat: Seulement dans les conditions de la tendance à la tendance à la tendance à la tendance à la tendance à la tendance à la tendance à la tendance à la tendance à la tendance à la tendance à la tendance à la tendance à la tendance à la tendance à la tendance à la tendance à la tendance à la tendance à la tendance à la tendance à la tendance à la tendance à la tendance à la tendance à la tendance à la tendance à la tendance à la tendance à la tendance à la tendance à la tendance à la tendance à la tendance à la tendance à la tendance à la tendance à la tendance à la tendance à la tendance à la tendance à la tendance à la tendance à la tendance à la tendance à la tendance à la tendance à la tendance à la tendance à la tendance à la tendance à la tendance à la tendance à la tendance à la tendance à la tendance à la tendance à la tendance à la tendance à la tendance à la tendance à la tendance à la tendance à la tendance à la tendance à la tendance à la tendance à la tendance à la tendance à la tendance à la tendance à la tendance à la tendance à la tendance à la tendance à la tendance à la tendance à la tendance à la tendance à la tendance à la tendance à la tendance à la tendance à la tendance à la tendance à la tendance à la tendance à la tendance à la tendance à la tendance à la tendance à la tendance à la tendance à la tendance à la tendance à la tendance à la tendance à la tendance à la tendance à la tendance à la tendance à la tendance à la tendance à la tendance à la tendance à la tendance à la tendance à la tendance à la tendance à la tendance à la tendance à la tendance à la tendance à la tendance à la tendance à la tendance à la tendance à la tendance à la tendance à la tendance à la tendance à la tendance à la tendance à la tendance à la tendance à

### L'illusion de coordination

Sans contrôle statistique, la "coordination d'urgence" dans les démos reflète souvent:

> 没有统计控制, dans les démonstrations, la "涌现协调" est généralement représentée par:

- L'ingénierie rapide qui fonctionne en coordination (l'intervention du système qui dit "travailler ensemble").
  Le système de travail est un système de travail.
- Préjugé observateur (nous voyons des modèles que nous attendons).
  Le modèle de l'observateur est le modèle de l'observateur.
- Sélection post-hoc des courses réussies.
  Le succès de la carrière

Les systèmes de production qui commercialisent une "coordination d'urgence" sans signal mesurable doivent être traités comme une commercialisation.

>  aucun signal mesurable sur la propagande du système de production "survenue coordonnée" devrait être considéré comme un marketing―Pré-méthore réaffirmant―

### Un agent minimal conscient de la TOM

La structure:

```
agent state:
  own_beliefs:    {facts the agent believes}
  other_models:   {other_agent_id -> {beliefs_the_agent_attributes_to_them}}
  actions_last_N: [history of others' actions]

observation update:
  - update own_beliefs from direct observation
  - update other_models[agent_id] from their action + prior beliefs

action selection:
  - enumerate candidate actions
  - for each, predict what each other agent will do next given their modeled beliefs
  - pick action that maximizes joint outcome under those predictions
```

Le `other_models`L'attribut est l'état ToM. Le premier ordre ToM ne conserve qu'un seul niveau.`other_models[i][other_models_of_j]`Ce que je pense que l'agent J croit.

### Pourquoi le long horizon fait mal

Les limites de contexte font oublier aux agents quelle croyance appartient à qui. Les hallucinations ajoutent de fausses croyances aux modèles d'autres agents.

Les mesures d'atténuation documentées dans le document et les suivis en 2024-2026:

- **Explicit ToM state in the prompt.**Format structuré: `{agent_id: belief_list}`- La récupération des forces pour préserver la liaison entre la croyance et l'identité.
- **Shorter reasoning chains.**Moins de mises à jour de ToM par tour réduisent les hallucinations composées.
- **External ToM store.**Garder le modèle hors du contexte du MLL; injecter uniquement des pièces pertinentes par tour.

### Lorsque le ToM échoue dans la production

- **Adversarial settings.**Les agents avec une bonne ToM sont plus faciles à manipuler (vous pouvez modéliser ce qu'ils modélisent de vous, puis exploiter).
- **Heterogeneous teams.**Lorsque les modèles sont différents, le modèle ToM qui fonctionne pour un adversaire ne généralise pas.
- **Ground-truth-dependent tasks.**Le TOM concerne les croyances; si la justesse dépend des faits, le TOM peut être une distraction.

### La coordination que vous pouvez vraiment mesurer

Trois signes pratiques indiquent que la coordination d'une équipe est réelle plutôt que rapide:

1. **Complementarity over time.**Sur une tâche multi-tours, les actions des agents couvrent-elles des sous-tâches disjointes ?
2. **Anticipation.**L'action de l'agent A au tour T+1 dépend-elle d'une prédiction sur l'action de B à T+2 qui s'est avérée correcte?
3. **Correction.**Lorsque A ne comprend pas correctement la croyance de B au virage T, A corrige-t-il le virage T+2?

Ces données sont mesurables dans un système multi-agents enregistré.

## Construisez-le en main
```figure
sw-theory-of-mind
```

## Faites-le

`code/main.py`les implémentations:

- `ToMAgent` trace ses propres croyances et les modèles de croyances par rapport à d'autres agents.
  Le mot grec traduit par " le mot grec "`ToMAgent`Suivez vos propres croyances et celles de tous les autres agents.
- Une tâche de coopération: trois agents doivent collecter trois jetons de trois boîtes; chaque boîte peut contenir un jeton.
  Les trois agents doivent collecter trois jetons de trois boîtes; chaque boîte ne peut placer qu'un jeton.
- Deux configurations: `zeroth_order`(pas de TOM) et `first_order`(ToM avec modèle de croyance à un niveau).
  Deux types de configuration:`zeroth_order`(sans détour)`first_order`(avec une couche de modèle de conviction)
- Mesure sur 200 essais randomisés: taux de réalisation, taux de duplication (deux agents ciblant la même boîte), moyenne de la finition.
  La mesure de l'essai est de la taille de l'échantillon.

Je vais courir .

```
python3 code/main.py
```

Expérience attendue: les agents de l'ordre zéro dupliquent l'effort à un taux de ~35% et terminent ~60% des essais en 10 tours.

> 预期输出: 0-stage Agent équivaut à environ 35% de taux de répétition du travail et à environ 60% de résultats en 10 rounds de l'essai.

## Utilisez-le.

`outputs/skill-tom-auditor.md`est une compétence qui vérifie la revendication d'un système multi-agents de "coordination d'urgence".

> `outputs/skill-tom-auditor.md`Il est un agent de contrôle multi-système "émergence coordination" de la déclaration de compétence.

## Envoyez-le en ligne .

Liste de contrôle des demandes de coordination:

- **Control condition.**Une version de votre système sans la commande de coordination.
  Le mot grec traduit par " le mot grec "**对照条件。**没有协调提示的系统版本──两者都测量──
- **Statistical test.**La différence entre le système et le contrôle est-elle significative à `p < 0.05`sur votre métrique ?
  Le mot grec traduit par " le mot grec "**统计测试。**La différence entre le système et le reflet est-elle sur votre indicateur ?`p < 0.05`- Il est important ?
- **Complementarity measure.**Des désaccords au fil du temps, pas seulement un succès final.
  Le mot grec traduit par " le mot grec "**互补性测量。**Avec le temps, les mouvements ne se combinent pas, mais ils réussissent.
- **Failure-case log.**Quand les agents se trompent, à quoi ressemble l'état de la MTO ?
  Le mot grec traduit par " le mot grec "**失败案例日志。**Quand l'agent a échoué, comment était votre état ?
- **Model-capacity disclosure.**Si l'effet disparaît sur les modèles plus petits, dites-le.
  Le mot grec traduit par " le mot grec "**模型能力披露。**Si l'effet disparaît sur le modèle plus petit, expliquez ceci.

## Les exercices

1. On court .`code/main.py`Confirmer que le premier ordre de ToM réduit le taux de duplication de 7 fois.
   Le mot " l' économie " est traduit par " l' économie ".`code/main.py` Confirmer que la première phase de la RTE va réduire le taux de répétition d'environ 7 fois.
2. La mise en œuvre de la deuxième classe de ToM (l'agent A modélise ce que B pense de C).
   En français, l'action est une transformation de la situation.
3. Injecter une**hallucination**Dans l'état de ToM, on renverse au hasard une croyance par tour.
   À l'intérieur de l'État**幻觉**: chaque tour change d'avis.
4. Lisez Li et coll. (arXiv:2310.10701). Répétez la découverte de la " dégradation à long horizon ": à mesure que les tours passent de 10 à 30, comment votre performance de premier ordre ToM change-t-elle ?
   Le nombre de fois où le nombre de personnes atteintes de la maladie est réduit, le nombre de fois où les personnes atteintes de la maladie sont réduites est réduit à 10%.
5. Lisez Riedl 2025 (arXiv:2510.05174). Implémenter les statistiques de synergie de plus haut ordre sur vos journaux de simulation.
   Le projet de loi de la loi de la loi de la loi de la loi de la loi de la loi de la loi de la loi de la loi de la loi de la loi de la loi de la loi de la loi de la loi de la loi de la loi de la loi de la loi de la loi de la loi de la loi de la loi de la loi de la loi de la loi de la loi de la loi de la loi de la loi de la loi de la loi de la loi de la loi de la loi de la loi de la loi de la loi de la loi de la loi de la loi de la loi de la loi de la loi de la loi de la loi de la loi de la loi de la loi de la loi de la loi de la loi de la loi de la loi de la loi de la loi de la loi de la loi de la loi de la loi de la loi de la loi de la loi de la loi de la loi de la loi de la loi de la loi de la loi de la loi de la loi de la loi de la loi de la loi de la loi de la loi de la loi de la loi de la loi de la loi de la loi de la loi de la loi de la loi de la loi de la loi de la loi de la loi de la loi de la loi de la loi de la loi de la loi de la loi de la loi de la loi de la loi de la loi de la loi de la loi de la loi de la loi de la loi de la loi de la loi de la loi de la loi de la loi de la loi de la loi de la loi de la loi de la loi de la loi de la loi de la loi de la loi de la loi de la loi de la loi de la loi de la loi de la loi de la loi de la loi de la loi de la loi de la loi de la loi de la loi de la loi de la loi de la loi de la loi de la loi de la loi de la loi de la loi de la loi de la loi de la loi de la loi de la loi de la loi de la loi de la loi de la loi de la loi de la loi de la loi de la loi de la loi de la loi de la loi de la loi de la loi de la loi de la loi de la loi de la loi de la loi de la loi de la loi de la loi de la loi de la loi de la loi de la loi de la

## Les termes clés

| Term | What people say | What it actually means |
|------|----------------|------------------------|
| Theory of Mind / 心智理论 | "Understanding others' minds" / "理解他人的心理" | The capacity to model another agent's beliefs. Graded by order (0, 1, 2+). / 建模另一个 Agent 信念的能力。按阶次分级（0, 1, 2+）。 |
| Sally-Anne test / Sally-Anne 测试 | "The false-belief test" / "错误信念测试" | 1985 developmental psychology; LLMs pass plain versions, fail complex ones. / 1985 年发展心理学；LLM 通过简单版本，复杂版本失败。 |
| First-order ToM / 一阶 ToM | "A believes X" / "A 相信 X" | Modeling one other's beliefs about facts. / 建模另一个关于事实的信念。 |
| Second-order ToM / 二阶 ToM | "A believes B believes X" / "A 相信 B 相信 X" | Recursive modeling one level deeper. / 递归建模更深一层。 |
| Identity-linked differentiation / 身份关联分化 | "Stable roles over time" / "稳定的角色" | Riedl's metric: roles persist, not random. / Riedl 的指标：角色持续而非随机。 |
| Goal-directed complementarity / 目标导向互补性 | "Disjoint actions" / "不交动作" | Agents target different subtasks, not the same one. / Agent 瞄准不同子任务，不是同一个。 |
| Higher-order synergy / 高阶协同 | "Group exceeds any subset" / "群体超越任何子集" | Riedl's statistical measure for real coordination. / Riedl 对真正协调的统计度量。 |
| Coordination illusion / 协调幻觉 | "It looks coordinated" / "看起来协调" | Prompt-dressed appearance of coordination without measurable signal. / 没有可测量信号的提示装饰的协调外观。 |

## Encore une lecture

- [Li et al. — Theory of Mind for Multi-Agent Collaboration via Large Language Models](https://arxiv.org/abs/2310.10701) la gestion des risques émergente dans les jeux de coopération; modes de défaillance à long horizon
- [Riedl — Emergent Coordination in Multi-Agent Language Models](https://arxiv.org/abs/2510.05174) Mesure à l'échelle de la population; la pression à la charge est la condition de support
- [Premack & Woodruff — Does the chimpanzee have a theory of mind?](https://www.cambridge.org/core/journals/behavioral-and-brain-sciences/article/does-the-chimpanzee-have-a-theory-of-mind/1E96B02CD9850E69AF20F81FA7EB3595) l'origine de la notion de TOM en 1978
- [Baron-Cohen, Leslie, Frith — Does the autistic child have a theory of mind?](https://doi.org/10.1016/0010-0277(85)90022-8)  le document Sally-Anne (1985)
