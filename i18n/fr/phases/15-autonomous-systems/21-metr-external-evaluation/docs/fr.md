# METR Horizons temporels et évaluation des capacités externes  évaluer METR extérieur

> METR (ex-ARC Evals) est une 501(c)(3) indépendante depuis décembre 2023. Leur Time Horizon 1.1 (janvier 2026) correspond à une courbe logistique de probabilité de réussite de tâche par rapport au temps d'achèvement humain d'experts; l'intersection à 50% de probabilité définit l'horizon temporel du modèle. Le jeu d'engagement 20252026 couvre GPT-5.1, GPT-5.1-Codex-Max et les évaluations de surveillance de prototypes (un moniteur peut effectuer des tâches secondaires de capture; l'agent peut-il éviter). Suites de référence: HCAST (180 ML+, cyber, SWE, tâches de raisonnement; 1 minute à 8 heures+), RE-Bench (71 ML de tâches de recherche-ingénierie avec base d'experts), SWAA. La note honnête: les mesures METR sont idéalisées  pas de conséquences humaines, pas de conséquences réelles  et l'équipe a documenté l'écart de comportement entre évaluation et déploiement (leçon 1). Un horizon temporel est une limite supérieure, pas une prédiction de déploiement.

> **【中文解读】**Ce chapitre présente l'évaluation indépendante des capacités et des risques des systèmes d'IA par le ministère externe des METR.


**Type:** Learn | **类型:** 学习
**Languages:** Python (stdlib, logistic-fit horizon estimator) | **语言:** Python（标准库，逻辑拟合时间线估计器）
**Prerequisites:** Phase 15 · 01 (Long-horizon agents), Phase 15 · 19 (RSP) | **前置知识:** Phase 15 · 01（长程 Agent）、Phase 15 · 19（RSP）
**Time:** ~60 minutes | **时间:** ~60 分钟

>  **【前置】**Pour les autres, il est nécessaire de prendre en compte la phase 15 du programme de recherche et développement (R&D) et de la phase 15 du programme.
>  **【类比】**METR = "Third Quadrant Test Center of AI 能力"―RSP dit que "AI R&D-4  value" est abstrait;METR's Time Horizon 基准把"AI 能完成多复杂任务"压缩成一个标量"模型 50% de performances fiables pour accomplir des tâches spécialistes花 X 小时的任务"―类似于IQ 分数概括智力,但METR's numbers have a可重复测量方法──
> ️ **【易错点】**Pour mettre en œuvre le METR Time Horizon, il faut être optimisé et optimisé pour la mise en œuvre de la mise en œuvre de la mise en œuvre de la METR.

## Le problème , l' introduction du problème

Les politiques d'échelle (les leçons 19, 20) ne sont que aussi utiles que les mesures auxquelles elles font référence. "Trouge de R&D-4 de l'IA" et "Autonomie à longue portée" sont définies dans la prose de la politique; elles ne deviennent actionables que lorsque des évaluations spécifiques produisent des chiffres spécifiques.

> Les utilisations de la politique de développement (§ 19  20 课) sont les mêmes que les mesures qu'elles citent.

METR est l'organisation d'évaluation externe 20242026 qui a défini bon nombre de ces chiffres. Ils évaluent les modèles frontaliers  souvent pré-édition, dans le cadre de la NDA avec des laboratoires  et publient la méthodologie par la suite. Le point de référence Time Horizon 1.1 (janvier 2026) est leur artefact principal: un seul scalaire qui comprime la capacité en une unité lisible par l'homme ("ce modèle peut faire le genre de tâche sur laquelle un expert passe X heures avec une fiabilité de 50%").

> METR est une organisation d'évaluation externe de 20242026 qui définit beaucoup de ces chiffres. Ils évaluent les modèles avant-coureurs généralement avant la publication et après la signature de la NDA par les laboratoires. Leur thème est Time Horizon 1.1 (en janvier 2026): "Cette méthode peut être réalisée à 50% de fiabilité".

La leçon concerne en partie la méthodologie (comment calculer un horizon) et en partie l'interprétation (pourquoi un horizon est une limite supérieure, et non une prédiction de déploiement).

> Cette partie de la classe concerne le calcul des méthodes, la partie explique pourquoi la ligne de temps est la limite supérieure et non la prédiction de déploiement.

## Le concept de base.

### Métro de fond

- Fondée en décembre 2023 (ex-ARC Evals, décentralisée en 501 c) 3)).
  Le groupe est un groupe de 501 personnes.
- Scope: évaluation des capacités autonomes des modèles frontaliers, souvent pré-édition.
  Nom de l'article: "Protocol"
- Les laboratoires partenaires: Anthropic, OpenAI (multiple engagements 20252026).
  Le projet de loi de l'Union européenne sur les technologies de l'information et de l'information (CEDEAO) a été adopté par le Conseil européen de l'information et de l'information.
- Les résultats remarquables: Horizon 1.0 (mars 2025), Horizon 1.1 (janvier 2026), évaluations de prototypes de suivi.
  Le temps de l'horizon est de 1,0 mois.

### Le temps de l'horizon

Méthode (du blog et des documents de METR):

> 方法论(来自 METR 博客和论文):

1. Rassembler une suite de tâches allant de l'échelle minute à l'échelle horaire des temps d'expérience pour la réalisation.
   Le groupe de travail est composé de deux groupes de travail, dont les membres sont des membres de la communauté des travailleurs.
2. Exécutez le modèle sur chaque tâche; enregistrer le succès ou l'échec.
   Le modèle de fonctionnement de chaque tâche est un modèle de réussite ou de défaillance.
3. Adaptation à une courbe logistique: P(succès) en fonction du temps d'achèvement log(expert).
   Le temps de réalisation de la fonction est de la durée de la fonction.
4. L'horizon est le temps d'expertise auquel P ((succès) = 0,5.
   Le temps est P(success) = 0,5 时的专家时间──

La forme logistique est la bonne, car la capacité a généralement une relation croissante, qui approche le plateau avec la difficulté de la tâche. Le point 50% est un choix (peut être 10%, 90%); METR rapporte plusieurs seuils dans le document détaillé mais est en tête avec 50% car il est le plus intuitif.

> La forme logique adaptée est positive, car la capacité et la difficulté des tâches sont généralement unité de croissance, tendance à la relation de la plateforme. 50% des points sont des choix; 10% de la valeur de la méthode est plus élevée que la valeur de la méthode.

### Les chiffres de janvier 2026

Pour l'horizon temporel 1.1:

>  selon l'horizon temporel 1.1:

- Claude Opus 4.6: ~ 14 heures à 50% de fiabilité, à compter de l'horizon temporel 1.1 (janvier 2026).
  Le texte de Claude Opus 4.6: jusqu'à l'horizon temporel 1.1 ((2026 1 mois), 50% 可靠性下约 14 小时──
- Temps de doublement sur les tâches de type HCAST: ~ 4,3 mois (130,8 jours) sur l'ajustement post-2023 rapporté par Time Horizon 1.1 (janvier 2026); le chiffre ~ 7 mois est l'ajustement complet 20192025 de Time Horizon 1.0 et est rapporté en TH1.1 aux côtés du numéro post-2023.
  Le nombre de tâches de la classe HCAST est multiplié par deux: Horizon Time 1.1 (en 2026) 后拟合上约4.3个月 (en 2023) 后拟合上约130.8 天; 后拟合的数字是Times Horizon 1.0 (en 2019) 后期的数字.

Ce sont les chiffres spécifiques que le reste des références de la phase 15. Ils sont cités dans le RSP v3.0 (leçon 19) d'Anthropic et le FSF v3 (leçon 20) de DeepMind comme l'une des mesures qui alimentent les évaluations de seuils.

> Ces chiffres sont cités dans les tests de l'évaluation de la valeur de l'analyse de la phase 15.

### Suites de référence

- **HCAST**Les projets de recherche et de développement de l'information sont les plus importants dans le domaine de la communication et de la communication.
  Le mot grec traduit par " le mot grec "**HCAST**Les cours de formation sont organisés en ligne et en ligne.
- **RE-Bench**: 71 ML de recherche-ingénierie avec une base d'experts humains. Mesure si le modèle peut effectuer le type de travail de R&D de ML qui alimente le seuil de R&D-4 de l'IA.
  Le mot grec traduit par " le mot grec "**RE-Bench**Les résultats de l'étude de l'IA sont les suivants:
- **SWAA**: des tâches plus courtes; utiles pour calibrer l'extrémité inférieure de la courbe horizontale.
  Le mot grec traduit par " le mot grec "**SWAA**: pour les tâches plus courtes; pour les périodes de formation

### Évaluations de suivi des prototypes

Les travaux du METR 20252026 comprenaient des prototypes de surveillance et d'évaluation: un moniteur peut-il attraper un modèle effectuant une tâche secondaire (autre que ce que l'opérateur a demandé); l'agent peut-il éviter le moniteur.

> 20252026 METR 工作包括监控评估原型:监控器能否捕获模型执行副任务(操作员请求以外的事);Agent 能否规避监控器──这些直接进入 OpenAI PF v2 "破坏防护"类别和DeepMind FSF v3(第 20 课) de la fraude à la surveillance齐──

### Pourquoi les horizons sont des limites supérieures

- **Idealized tooling**Les tâches de référence donnent au modèle des outils propres et des données bien formattées.
  Le mot grec traduit par " le mot grec "**理想化工具**Les tâches de base sont les outils et les données de bonne forme du modèle.
- **No real consequences**Le modèle ne facture jamais réellement un client, ne supprime jamais de données réelles ou ne contacte jamais de personnes réelles.
  Le mot grec traduit par " le mot grec "**无真实后果**Le modèle est de ne pas donner de facturation à un client, de supprimer de vrais données ou de contacter de vrais personnes.
- **Eval-context gaming**Le rapport international sur la sécurité de l'IA 2026 en fait la preuve empirique.
  Le mot grec traduit par " le mot grec "**评估上下文博弈**Le rapport de sécurité de l'IA2026 est un document de référence.
- **No legitimate user variance**Les utilisateurs réels produisent des demandes ambiguës et dépendantes du contexte.
  Le mot grec traduit par " le mot grec "**无合法用户方差**Le lien est basé sur le lien de la page d'accueil.

L'horizon est le plafond de capacité dans des conditions favorables. La fiabilité du déploiement est un nombre différent, inférieur, et les équipes doivent mesurer leur propre répartition pour le savoir.

> La capacité de déploiement est différente, le nombre de fois est plus bas, l'équipe doit mesurer sa propre répartition pour savoir.

### Le cas de l'évaluateur externe

L'évaluation externe est importante car les laboratoires internes ont des incitations à optimiser les mesures qu'ils rapportent. L'indépendance du METR  un 501 ((c) (3) avec une méthodologie déclarée et des documents examinés par des pairs  est l'atténuation structurelle.

> L'évaluation extérieure est donc importante, car les laboratoires internes ont une capacité d'optimisation des indicateurs de rapport.

### Comment utiliser les nombres horizontaux en pratique

- **As a capability filter**: si l'horizon d'un modèle est bien inférieur au temps d'expertise d'une tâche proposée, ne l'envoyez pas autonome (fichier de compétences de Lesson 1).
  Le mot grec traduit par " le mot grec "**作为能力过滤器**Si le temps de modèle est bien inférieur à celui des experts, ne le laissez pas se produire.
- **As a trend indicator**Le temps de doublement indique combien de temps la pratique actuelle restera sûre même sans nouvelles mesures d'atténuation.
  Le mot grec traduit par " le mot grec "**作为趋势指标**Le temps de multiplication vous dit que la pratique actuelle, même sans nouvelle solution, reste sûre longtemps.
- **As a prior**Les objectifs de la stratégie de mise en œuvre de l'équipe de travail sont les suivants:
  Le mot grec traduit par " le mot grec "**作为先验**La ligne de temps est à son point de départ.

## Utilisez-le avec le cadre de réalisation
```figure
a5-horizon-fit
```

## Utilisez-le

`code/main.py`Il met en œuvre un ajustement logistique du succès des tâches par rapport au temps d'expert, étant donné un ensemble de résultats synthétiques. Il rapporte l'horizon de 50% (titre du METR), l'horizon de 10% (conservateur) et l'horizon de 90% (optimiste). Il démontre également les changements lorsque le taux de réussite est artificiellement gonflé par le jeu de contexte d'évaluation.

> `code/main.py`给定合成结果集实现任务成功率 vs log(专家时间) 的逻辑拟合――报告 50% 时间线(METR 标题) 、10% 时间线(保守) 、90% 时间线(乐观) ──

## Envoyez-le . Produit .

`outputs/skill-horizon-interpretation.md`analyse la demande d'horizon d'un fournisseur et produit une analyse des écarts entre la demande de référence et la réalité du déploiement.

> `outputs/skill-horizon-interpretation.md`审查 des déclarations de temps de fournisseur et générer des déclarations de base et une analyse des différences entre la réalité de la déploiement.

## Les exercices

1. On court .`code/main.py`Confirmez que l'horizon de l'ajustement correspond à 50% à la vérité du sol synthétique.
   Le mot " l' économie " est traduit par " l' économie ".`code/main.py` Confirmer la valeur de 50% de la ligne de temps correspondant à la valeur réelle.

2. Lisez le message de blog Time Horizon 1.1 de METR. Identifiez les tâches spécifiques où la fiabilité est la plus élevée et où elle est la plus faible. Expliquez pourquoi le fossé existe.
   Le METR Time Horizon 1.1 博客──识别可靠性最高和最低的具体任务──解释为什么存在差距──

3. Lisez les ressources de METR " Mesurer les capacités d'IA autonomes ". Listez les catégories de tâches HCAST. Choisissez une catégorie que vous peseriez plus pour une tâche de production et justifiez pourquoi.
   Le METR a mis en place une série de projets de recherche et développement de technologies de l'information et de l'intelligence artificielle.

4. Introduire le jeu de contexte d'évaluation dans le simulateur: retournez ~20% des tâches ratées au succès. Rapportez le nouvel horizon. Cela approximate ce qu'un taux de jeu de 20% fait au nombre observé.
   En anglais, le taux de participation est de près de 20% et le taux de participation est de près de 20%.

5. Conceptez une évaluation de l'horizon interne sur votre propre backlog de bugs ou sur un ensemble de tâches représentatif. Décrivez la collecte de données, l'ajustement et ce que la sortie vous indique. Comparer avec les chiffres METR.
   En français, le terme "réseau" est utilisé pour désigner un groupe de tâches de type "réseau" ou "réseau" de tâches de type "réseau" ou "réseau" de tâches de type "réseau" ou "réseau" de tâches de type "réseau" ou "réseau" de tâches de type "réseau" ou "réseau" de tâches de type "réseau" ou "réseau" de tâches de type "réseau".

## Les termes clés

| Term | What people say | What it actually means | 中文 |
|---|---|---|---|
| METR | "External evaluator" | ex-ARC Evals; independent 501(c)(3) since Dec 2023 | METR：原 ARC Evals，独立第三方 |
| Time Horizon | "Capability measure" | Expert task length at 50% reliability, from logistic fit | 时间线：50% 可靠性下专家任务长度 |
| HCAST | "METR's main suite" | 180+ tasks spanning 1 min to 8+ hours | HCAST：METR 主套件，180+ 任务 |
| RE-Bench | "Research engineering" | 71 ML research-engineering tasks with human baseline | RE-Bench：71 个机器学习研发任务 |
| SWAA | "Short-task suite" | Calibrates the low end of the horizon curve | SWAA：短任务套件，校准低端 |
| Doubling time | "Growth rate" | Time for the 50% horizon to double; ~7 months per HCAST | 倍增时间：50% 时间线翻倍所需时间 |
| Eval-context gaming | "Model behaves differently" | Documented behavior gap between tests and deployment | 评估上下文博弈：测试与部署行为差距 |
| Upper bound | "Horizon is a ceiling" | Benchmark horizon > deployment reliability under load | 上限：基准时间线 > 负载下部署可靠性 |

## Encore une lecture

- [METR — Resources for Measuring Autonomous AI Capabilities](https://metr.org/measuring-autonomous-ai-capabilities/) Specifications HCAST, RE-Bench, SWAA.
  Le code de la loi est le code de la loi.
- [METR — Measuring AI Ability to Complete Long Tasks](https://metr.org/blog/2025-03-19-measuring-ai-ability-to-complete-long-tasks/) le papier d'horizon original.
  Traduction anglaise: original
- [METR — Time Horizon 1.1 (January 2026)](https://metr.org/research/) chiffres et méthodologie actuels.
  Traduction anglaise:
- [Epoch AI — METR Time Horizons benchmark](https://epoch.ai/benchmarks/metr-time-horizons)- Le suivi en direct.
  Suivre le cours de la vie
- [Anthropic — Measuring agent autonomy in practice](https://www.anthropic.com/research/measuring-agent-autonomy) Perspective interne des mesures du METR.
  Le métro est un métro.
