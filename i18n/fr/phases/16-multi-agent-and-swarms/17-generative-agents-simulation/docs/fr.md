# Agents génératifs et simulation émergente

> Parque et coll. 2023 (UIST '23, arXiv:2304.03442) peuplée **Smallville**, une boîte à sable de 25 agents, avec une architecture en trois parties: **memory stream**(Log de la langue naturelle), **reflection**(synthèses de niveau supérieur que l'agent génère sur son propre flux), et **plan**(comportement au niveau du jour, puis sous-plans). Le résultat historique a été l'émergence d'une fête de la Saint-Valentin: un agent a semé avec " veut organiser une fête de la Saint-Valentin ", sans plus de scénarios, a produit des invitations réparties dans la population, des dates coordonnées, et la fête s'est déroulée  de 24 agents qui ont commencé sans le savoir. Les ablations montrent que les trois composants sont nécessaires pour la crédibilité. Les défaillances documentées sont des erreurs de la norme spatiale (entrées dans des magasins fermés, partage des salles de bains individuelles). C'est l'architecture de référence pour les simulations d'agents et l'évaluation sociale multi-agents en 2026.

> **【中文解读】**Cet épisode présente l'expérience d'un agent d'IA de Stanford, 25 agents d'IA dans une communauté virtuelle.

> **【拓展：generative agents simulation→具体应用】**L'initiative de Stanford est de créer un réseau de 25 agents d'IA dans une petite ville virtuelle. Il a créé 25 agents d'IA dans une petite ville virtuelle. Il a créé 25 agents d'IA dans une petite ville virtuelle.


**Type:** Learn + Build | **类型:** 学习 + 构建
**Languages:** Python (stdlib) | **语言:** Python（标准库）
**Prerequisites:** Phase 16 · 04 (Primitive Model), Phase 16 · 13 (Shared Memory) | **前置知识:** Phase 16 · 04（原语模型），Phase 16 · 13（共享内存）

>  **【前置】**Les élèves doivent être informés de la façon dont ils ont été informés et de la façon dont ils ont été informés.
>  **【类比】**Smallville = "AI 版模拟人生"──25 个 AI 居民各有生活、记忆、计划──情人节派对奇迹: un agent 想办派对→邀请传开→其他人调整日程→派对真发生全是涌现,无脚本──三件套:memory stream(经历日志) + réflexion(自我总结) + plan(日计划)──三者缺一不可, 删除任一 Agent 行为变得不可信──
**Time:** ~75 minutes | **时间:** ~75 分钟

## ♪ Problème ♪ Introduction du problème ♪

La plupart des systèmes multi-agents sont des équipes étroitement scriptées: plans de planificateurs, codes de code, critiques de réviseurs. Cela fonctionne pour des tâches bien définies. Il ne capture pas le comportement émergent et non scripté qui se produit lorsque les agents ont une mémoire, des priorités et un monde ouvert. La recherche, la simulation de la société et de plus en plus l'IA de jeu ont besoin de ce second type.

> La plupart des systèmes d'agents sont une équipe de scripts étroits: planificateurs, éditeurs, éditeurs, réviseurs, évaluateurs. Ceci est valable pour définir les tâches précises. Mais il ne peut pas comprendre que l'agent possède des mémoires, des priorités et des comportements non scripts émergents dans le monde ouvert.

L'architecture de Smallville est la référence pour cela. Jusqu'à Park 2023, les meilleures simulations d'agents étaient des scripts superficiels; après cela, le modèle est le modèle par défaut pour les agents génératifs dans les mondes ouverts. Si vous construisez une simulation d'agents en 2026, vous utilisez soit les trois composants de Smallville ou justifiez explicitement pourquoi vous ne le faites pas.

> L'architecture de Smallville est la base de ce type. Avant Park 2023, le meilleur agent est le modèle de l'écriture de basse couche; après, ce modèle devient la norme de l'agent généré dans le monde ouvert. Si vous construisez un agent en 2026, vous devez utiliser les trois composants de Smallville, expliquez clairement pourquoi vous ne l'utilisez pas.

## Concept Le concept central

### Les trois composantes

**Memory stream.**Un journal d'observations, d'actions, de réflexions et de plans, uniquement en annexe. Chaque entrée a un timestamp, un type, une description (langue naturelle) et des métadonnées dérivées: **recency**- Je suis là .**importance**(auto-évalué 1 à 10 par l'agent), et **relevance**(semblance de cousin avec la requête actuelle).

> **记忆流。**Un seul extrait de l'observation, de l'action, de l'examen et du plan de jour.**时效性**- Je suis là.**重要性**(Agent 自评 1-10) et**相关性**(par rapport à la comparaison avec les autres questions)

```
[2026-02-14 09:12:03] observation: Isabella Rodriguez asked me if I like jazz
[2026-02-14 09:14:22] reflection:   I enjoy long conversations about music
[2026-02-14 10:05:00] plan:         Attend Isabella's Valentine's Day party tonight
```

La récupération de mémoire combine les trois scores: `score = w_recency * e^(-decay * age) + w_importance * importance + w_relevance * cos_sim`Les entrées de haut de K entrent dans la requête actuelle.

**Reflection.**Il est également possible de récupérer des informations sur les données de base de la mémoire de l'architecture, en utilisant des données de base de données.

> **反思。**定期(每 N 条记忆或在重要事件时),Agent génère un ensemble de haute échelle dans la mémoire récente.

**Plan.**Décomposition en haut et en bas. D'abord, un plan de jour en grandes lignes (" aller travailler, dîner avec Klaus "). Ensuite des plans à l'heure.

> **计划。**Il s'agit d'un plan de travail qui est modifiable: lorsqu'il est observé et contredit avec le plan, l'agent reprend son programme.

### Pourquoi les trois choses comptent (ablation)

Park et al. ont réalisé des ablations en abandonnant chacune de l'observation, de la réflexion et du plan.

> Parks et autres ont mené des expériences de désintégration, séparément en éliminant l'observation, les réflexions et les plans.

- Sans**observation**L'agent manque de contexte et agit sur des croyances périmées.
  Il n'y a pas de problème**观察**,Agent 缺失上下文, basé sur l'action de conviction passée.
- Sans**reflection**l'agent ne peut pas former des croyances de plus haut ordre; les interactions restent superficielles.
  Il n'y a pas de problème**反思**,Agent ne peut pas former de croyances de haut niveau;
- Sans**plan**Le comportement devient un bruit réactif; les objectifs se dissipent.
  Il n'y a pas de problème**计划**Le comportement devient un bruit réactif; objectif:

Les scores de crédibilité des évaluateurs humains sont les plus élevés avec les trois; la chute de n'importe lequel produit une régression mesurable.

> Le taux de crédibilité des évaluateurs est le plus élevé de tous les temps; éliminer toute déformation produisant une mesure.

### L'émergence de la Saint-Valentin

Une agent, Isabella Rodriguez, est semée avec le but " veut organiser une fête de la Saint-Valentin au Hobbs Cafe le 14 février à 17h. " Les 24 autres agents ne reçoivent pas de telles semences.

> Une agent, Isabella Rodriguez, a été implantée dans le but de " organiser un festin d'amour à Hobbs Café à 5 heures du matin le 14 février. "

1. Le plan d'Isabella inclut d'inviter les gens.
   Le plan d'Isabella était d'inviter les gens.
2. Chaque invitation devient une observation dans le flux de mémoire d'un voisin.
   Chaque invitation est une observation dans le flux de mémoire du voisin.
3. Cette réflexion de la voisine suscite des croyances: " Isabella organise une fête. "
   Le récit de l'époque de Isabelle est un récit de la vie de Isabelle.
4. Le plan du voisin inclut "assister à une fête le 14 février".
   Le 14 janvier, le président de la République de Suisse a déclaré: "Je suis un citoyen de la République de Suisse.
5. Les voisins disent aux autres voisins, l'invitation se répand sans coordination centrale.
   Les voisins se disent les uns aux autres.
6. À 17 h le 14 février, plusieurs agents se sont rassemblés au café Hobbs.
   Deux jours après le début de la guerre, plusieurs agents se sont rassemblés dans le café Hobbs.

Il s'agit d'une émergence au sens technique: le comportement au niveau du système (un parti) est issu d'interactions locales (invitations bilatérales + planification individuelle) sans orchestrateur central.

> C'est une tendance à l'échelle technique: les comportements systémiques (particules) sont générés par des interactions locales (invitations à deux côtés + planification individuelle) sans éditeur central.

### Les modes de défaillance documentés

Parque et coll. documentent explicitement:

> Park et d'autres ont écrit:

- **Spatial norm errors.**Les agents entrent dans des magasins fermés. Les agents essaient d'utiliser la même salle de bain individuelle. Les agents mangent dans des salles non destinées à manger. Le modèle ne déduit pas les normes socio-physiques de l'environnement seulement.
  Le mot grec traduit par " le mot grec "**空间规范错误。**L'agent entre dans un magasin fermé. L'agent essaie d'utiliser la même salle de bain. L'agent dans une salle de bain non utilisée. Le modèle ne peut être défini uniquement par l'environnement.
- **Memory overflow.**Les opérations de simulation profonde entraînent une augmentation des coûts de récupération de mémoire.
  Le mot grec traduit par " le mot grec "**记忆溢出。**La profondeur des opérations de modélisation entraîne une augmentation des coûts de recherche de mémoire.
- **Reflection hallucination.**Les réflexions peuvent inventer des relations qui n'existent pas dans le flux de mémoire.
  Le mot grec traduit par " le mot grec "**反思幻觉。**Réflexion peut évoquer des relations inexistantes dans le flux de mémoire.

Ce sont des modes de défaillance liés à la production: toute simulation d'agent 2026 les hérite.

> Ce sont des défauts liés à la production: tout agent de 2026 est censé les hériter.

### Règles de mise en œuvre en trois éléments

1. **Memory is append-only.**Ne changez jamais une entrée de mémoire.
   Le mot grec traduit par " le mot grec "**记忆只追加。**永遠不修改記憶条目──更正是新条目──
2. **Importance scores are cheap.**Appelle le Master pour évaluer l'importance de 1 à 10 au moment de la rédaction.
   Le mot grec traduit par " le mot grec "**重要性分数是廉价的。**写入时调用 LLM 评分 1-10──缓存分数──
3. **Retrieval is ranked, not filtered.**Top-k par score combiné; n'utilisez pas de filtres durs (qui perdent de leur contexte).
   Le mot grec traduit par " le mot grec "**检索是排序的，不是过滤的。**按综合分数取 top-k; ne pas utiliser le hard过(会丢失上下文)
4. **Reflection runs periodically.**Trigger lorsque la somme de l'importance des souvenirs non traités dépasse un seuil (par exemple, 150).
   Le mot grec traduit par " le mot grec "**反思定期运行。**Lorsque l'importance de la mémoire non traitée dépasse la valeur totale (par exemple 150)
5. **Plans are revisable.**Lorsqu'une nouvelle observation contredit un plan, régénérez seulement le segment affecté, pas l'ensemble du plan.
   Le mot grec traduit par " le mot grec "**计划可修订。**Lorsque les nouvelles observations sont en contradiction avec les plans, seuls les éléments affectés sont reproduits, et non l'ensemble du plan.

### Agents génératifs au-delà de Smallville

La littérature de suivi 2024-2026 étend l'architecture:

> La littérature ultérieure des années 2024-2026 étend cette structure:

- **Multi-agent social simulation for policy / market research.**Les populations de Smallville simulent le comportement des utilisateurs en réponse aux caractéristiques.
  Le mot grec traduit par " le mot grec "**用于政策/市场研究的多 Agent 社会模拟。**类似Smalville 的人群模拟用户对功能的响应──比A/B 测试更快;准确性有争议──
- **NPC AI for games.**Les jeux de rôle avec des agents de Smallville produisent des histoires émergentes au lieu de quêtes scriptées.
  Le mot grec traduit par " le mot grec "**游戏 NPC AI。**Avec le rôle d'agent de smallville, il y a un rôle de narrateur plutôt que de scénariste.
- **Generative-agent evaluation benchmarks.**Plutôt que de préciser les tâches, la métrique devient crédibilité + cohérence du comportement sur de longues périodes.
  Le mot grec traduit par " le mot grec "**生成式 Agent 评估基准。**En effet, les résultats de la recherche ont été très positifs.

L'architecture est la référence. Les extensions échanger des composants (stockage vectoriel pour la mémoire, récupération augmentée de la réflexion, plan neurosymbolique) mais garder la structure en trois parties.

> Cette structure est une référence. Elle est une extension de la structure.

### Pourquoi cela importe pour l'ingénierie multi-agents

Smallville est la preuve du concept que l'émergence de multi-agents est bon marché lorsque les composants sont corrects. L'architecture a maintenant été reproduite sur les modèles open source (les LLM plus petits perdent la crédibilité avec gracie, pas fortement).**emergent social behavior**Tout système qui a besoin de**tight task execution**utilise les modèles de superviseurs / rôles / primitives de plus tôt dans cette phase.

> Smallville est un concept de test, indiquant que lorsque le composant est correct, le multi-agent est émergé est bon marché.**涌现社会行为**Tout le monde utilise cette forme.**紧密任务执行**Le système est utilisé à cette phase par les superviseurs/personnes/modèles de langage original.

## Construisez-le en main
```figure
a5-memory-reflection
```

## Faites-le

`code/main.py`Il implique les trois composants dans stdlib Python avec des politiques d'agent scripté (pas de véritable LLM).

- `MemoryStream` Appendice de journaux uniquement avec récupération de récente/importance/relevance.
  Le mot grec traduit par " le mot grec "`MemoryStream` 带时效性/重要性/相关性检索的仅额日志──
- `reflect(stream)`Réflexion sur les récents souvenirs d'une grande importance.
  Le mot grec traduit par " le mot grec "`reflect` Réflexion sur les souvenirs d'importance récente
- `plan(agent_state)` des plans au niveau journalier et horaire basés sur les croyances actuelles.
  Le mot grec traduit par " le mot grec "`plan`  basé sur les croyances actuelles de jour et heure de plan.
- Scenario: 5 agents. L'agent 1 commence par "fête à 17h". Au cours des tiques simulées, l'invitation se répand et les agents convergent.
  En français, le temps de la rédaction est de 5 heures.

Je vais courir .

```
python3 code/main.py
```

Les résultats attendus: trace de tirage par tirage. Au dernier tirage, au moins 3 des 5 agents montrent le parti dans leur plan, et ils convergent à l'emplacement du parti.

> 预期输出: suivi par étape. Dans le dernier temps, 5 agents ont montré au moins 3 parties dans le plan, elles se sont rassemblées au lieu de la fête.

## Utilisez-le.

`outputs/skill-simulation-designer.md`Il conçoit une simulation générative-agent: nombre d'agents, schéma de mémoire, cadence de réflexion, horizon de plan et métrique d'évaluation.

> `outputs/skill-simulation-designer.md`Design a generé un agent 模拟:Agent numéros, modes de mémoire, réflexion, fréquence de planification et indicateur d'évaluation.

## Envoyez-le en ligne .

Règles pour les simulations de production:

- **Memory is the database.**Choisissez un magasin réel (vecteur DB, Postgres) à l'échelle.
  Le mot grec traduit par " le mot grec "**记忆是数据库。**Dans la sélection de la taille du stockage réel, le stockage standard est utilisé uniquement pour le type original.
- **Log the retrieval trace.**Pour chaque action, enregistrez les souvenirs qui l'ont conduite.
  Le mot grec traduit par " le mot grec "**记录检索轨迹。**Pour chaque mouvement, le record le pousse à se souvenir de son top-k. C'est votre capacité de réécriture.
- **Budget per-agent tokens.**Le plan de chaque agent pour récupérer + refléter + par tic est O(k) LLM. N agents × T ticks × appels-par-tick peuvent envahir votre budget.
  Le mot grec traduit par " le mot grec "**预算每 Agent token。**Chaque agent Chaque étape de temps de recherche + réflexion + plan est O(k) fois LLM 调用──N 个代理 × T 个时间步 × 每时间步调用数可能让你的预算相形见──
- **Compact memory periodically.**Résumé et séquence des entrées de faible importance.
  Le mot grec traduit par " le mot grec "**定期压缩记忆。**Résumé et modification de l'importance de l'article.
- **Detect spatial / social norm violations**L'architecture ne les apprend pas.
  Le mot grec traduit par " le mot grec "**显式检测空间/社会规范违规。**Les architectures ne les apprendront pas.

## Les exercices

1. On court .`code/main.py`Confirmez que 3 agents sont convergents à la fête.
   Le mot " l' économie " est traduit par " l' économie ".`code/main.py`Confirmer que 3 agents ou plus sont rassemblés pour la fête.
2. Le comportement est-il le même ?
   Le comportement se présente-t-il comme un phénomène ?
3. Introduisez un objectif en compétition (" Klaus veut donner une conférence de recherche à 17h ").
   Le groupe de travail est un groupe de travail qui a été créé pour la première fois en 2008 et qui a été créé pour la première fois en 2011.
4. Ajouter des contraintes spatiales: Hobbs Cafe peut contenir au plus 4 agents. La manche de simulation déborde-t-elle avec élégance, ou frappe-t-elle le modèle de défaillance de la salle de bain à une seule personne?
   Le café Hobbs a-t-il le plus de capacité pour 4 agents ?
5. Par exemple, la section 6 (expériences de comportement émergentes) identifie un comportement non reproduisable dans votre miniature.
   Le code de la vie est un code de vie qui est utilisé pour la vie privée.

## Les termes clés

| Term | What people say | What it actually means |
|------|----------------|------------------------|
| Memory stream / 记忆流 | "The agent's diary" / "Agent 的日记" | Append-only log of observations, actions, reflections, plans. / 观察、行动、反思、计划的只追加日志。 |
| Recency / 时效性 | "How new is the memory" / "记忆有多新" | Exponential-decay score by age. / 按年龄的指数衰减分数。 |
| Importance / 重要性 | "How much does the agent care" / "Agent 有多在意" | Self-rated 1-10 at write time. Cached. / 写入时自评 1-10。已缓存。 |
| Relevance / 相关性 | "How related to the current query" / "与当前查询有多相关" | Cosine similarity (embedding-based). / 余弦相似度（基于嵌入）。 |
| Reflection / 反思 | "Higher-order belief" / "高阶信念" | Synthesis generated from recent memories, re-ingested as a new memory. / 从最近记忆生成的综合，作为新记忆重新摄入。 |
| Plan / 计划 | "Day/hour/action decomposition" / "日/小时/动作分解" | Top-down plan tree. Revisable when observations contradict. / 自顶向下计划树。观察矛盾时可修订。 |
| Smallville / 小镇 | "Park 2023's sandbox" / "Park 2023 的沙盒" | 25-agent simulation that produced the Valentine's Day emergence. / 25 个 Agent 的模拟，产生了情人节涌现。 |
| Believability / 可信度 | "The quality metric" / "质量指标" | Human-rater score for whether behavior seems like a plausible agent. / 人类评分者对行为是否像合理 Agent 的评分。 |

## Encore une lecture

- [Park et al. — Generative Agents: Interactive Simulacra of Human Behavior](https://arxiv.org/abs/2304.03442) l'architecture de référence
- [UIST '23 paper page](https://dl.acm.org/doi/10.1145/3586183.3606763) lieu de publication
- [Smallville code release](https://github.com/joonspk-research/generative_agents) mise en œuvre de référence Python
- [Hayes-Roth 1985 — A Blackboard Architecture for Control](https://www.sciencedirect.com/science/article/abs/pii/0004370285900639) l'art antérieur des agents de mémoire structurée
