# Évaluation et coordonnées Benchmarks  координа基准 评估

> Cinq critères de référence 2025-2026 couvrent l'espace d'évaluation multi-agents. **MultiAgentBench / MARBLE**(ACL 2025, arXiv:2503.01935) évalue les topologies étoile/chaîne/arbre/graphe avec des indicateurs clés; **graph is best for research**, la planification cognitive ajoute à ~ 3% des réalisations clés. **COMMA**L'évaluation de la coordination multimodal asymétrique-information; les modèles de pointe, y compris le GPT-4o, luttent pour surmonter une ligne de base aléatoire. **MedAgentBoard**(arXiv:2505.12371) couvre quatre catégories de tâches médicales et trouve souvent que le multi-agent ne domine pas le single-LLM. **AgentArch**(arXiv:2509.10769) références des architectures d'agents d'entreprise combinant l'utilisation d'outils + mémoire + orchestration. **SWE-bench Pro**(le secteur de l'énergie)[arXiv:2509.16941](https://arxiv.org/abs/2509.16941)Il existe des problèmes de protection des données dans 41 repossissants couvrant des applications commerciales, des services B2B et des outils de développement; les modèles frontaliers obtiennent un score de ~23% sur Pro vs 70%+ sur Verified  un contrôle de la réalité sur la contamination.**64.3%**sur Pro avec une coordination explicite des équipes d'agents (aucune source primaire anthropic n'a encore été publiée  traiter comme préliminaire); Verdent (échafaudage d'agents) frappe **76.1% pass@1**sur vérifié ([Verdent technical report](https://www.verdent.ai/blog/swe-bench-verified-technical-report)**AAAI 2026 Bridge Program WMAC**(le secteur de l'énergie)https://multiagents.org/2026/Cette leçon s'appuie sur les mesures de MARBLE, effectue un balayage topologique contre métrique et fixe la règle " juste passer la banque SWE Verified n'est pas une preuve de généralisation ".

> **【中文解读】**Ce chapitre présente les méthodes d'évaluation des capacités de coordination des systèmes pour mesurer les capacités de coordination de plusieurs agents.

> **【拓展：evaluation coordination benchmarks→具体应用】**│ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │                                  


**Type:** Learn | **类型:** 学习
**Languages:** Python (stdlib) | **语言:** Python（标准库）
**Prerequisites:** Phase 16 · 15 (Voting and Debate Topology), Phase 16 · 23 (Failure Modes) | **前置知识:** Phase 16 · 15（投票与辩论拓扑），Phase 16 · 23（失败模式）

>  **【前置】**Les résultats de la formation sont les suivants:
>  **【类比】**基准 = "AI 团队的标准化考试"――MARBLE 测拓(图最佳做研究);COMMA 测多模态不对称信息协调(GPT-4o 都难超随机基线);MedAgentBoard 测医疗(多 Agent 常不胜单 LLM);SWE-bench Pro 测真码(1865 题/41 仓库,前沿模型仅23%,对比 验证70%+,揭露污染问题) ―Claude Opus 4.7 多 Agent 协调达 64.3%──
**Time:** ~75 minutes | **时间:** ~75 分钟

## ♪ Problème ♪ Introduction du problème ♪

Lorsque un article affirme que "notre système multi-agents est meilleur", la question est: mieux que quoi, sur quoi, mesuré comment? L'ère 2023-2024 de l'évaluation multi-agents a été un chaos  chacun a choisi ses propres mesures, ses propres lignes de base et ses propres ensembles de tâches.

> Lorsque l'article affirme que " notre multi agent  système meilleur ", la question est: par rapport à quoi mieux, sur quoi mieux, avec quoi mesurer ?

Sans benchmarks partagés, vous ne pouvez pas comparer deux systèmes multi-agents de manière significative. Pire, sans benchmarks de détention, les modèles frontaliers peuvent contaminer. SWE-bench Verified est partiellement contaminé dans les corps de formation à la mi-2025; les scores frontaliers ont gonflé; Pro a été conçu comme un contrôle de la réalité non contaminé.

>  sans base de données partagée, vous ne pouvez pas comparer significativement deux agents 系统── pire, sans base de données conservée, le modèle avant-coût peut être contaminé──SWE-bench Verified in mid-term 2025 contamination partie de la formation;

Cette leçon énumère les cinq critères de référence canoniques de 2026, nomme ce que chaque mesure, et vous apprend à lire les affirmations de référence de manière sceptique.

> Ce cours présente cinq règles de l'épreuve de base de 2026, nommée pour chaque mesure de quoi, et vous apprend à avoir un état d'esprit douteux.

## Concept Le concept central

### Le groupe de travail de la Commission

ArXiv:2503.01935. Évalue quatre topologies de coordination (étoile, chaîne, arbre, graphique) sur les tâches de recherche, de codage et de planification.

Résultats mesurés:

- **Graph**La meilleure topologie pour les scénarios de recherche; prend en charge toute critique.
- **Chain**le mieux adapté à la codage de raffinage progressif.
- **Star**la meilleure solution pour une consolidation rapide.
- **Coordination tax**apparaît après ~ 4 agents sur le graphique.
- **Cognitive planning**ajoute à ~3% de réalisation de milestones dans les topologies.

Utilisez lorsque vous souhaitez comparer les topologies de coordination pommes à pommes.https://github.com/ulab-uiuc/MARBLE) est fourni par l'évaluateur.

### COMMA  Informations asymétriques multimodelles

Il couvre des tâches dans lesquelles les agents ont des modalités d'observation différentes et doivent se coordonner sans partager pleinement les informations.**random baseline**La Commission a également décidé de mettre en place un programme de coopération de coopération entre les agents dans le cadre de la COMMA.

Utilisez lorsque: votre système dispose d'une coordination multimodal ou asymétrique-information.

### Test de stress de domaine MedAgentBoard 

ArXiv: 2505.12371. Quatre catégories de tâches médicales: diagnostic, planification du traitement, génération de rapports, communication avec les patients. Compares systèmes basés sur des règles conventionnelles avec des systèmes multi-agent et un seul LLM.

Résultats: le multi-agent N'est PAS le principal facteur de la LLM dans la plupart des catégories. L'avantage du multi-agent est étroit.

Utilisez quand: votre domaine a des lignes de base claires pour un seul LLM. Si la leçon de MedAgentBoard généralise, de nombreux systèmes multi-agents proposés sont sur-ingénieurs.

### AgentArch  architectures d'entreprise

Les paramètres d'entreprise avec l'utilisation des outils, la mémoire et l'orchestration couchés ensemble.

Utilisez-le lorsque vous conçoitz une pile d'agents d'entreprise et que vous devez justifier chaque couche. AgentArch aide à éviter d'acheter des fonctionnalités dont vous ne pouvez pas mesurer la valeur.

### SWE-bench Pro  la vérification de la réalité

1865 problèmes dans 41 référentiels couvrant des applications commerciales, des services B2B et des outils de développement.**uncontaminated**Les modèles Frontier obtiennent un score de 23% sur Pro contre 70%+ sur Verified.

Points du mois d'avril 2026:
- Claude Opus 4.7 sur Pro: **64.3%**(reporté avec une coordination explicite entre les équipes d'agents; aucune source primaire Anthropic n'a encore été publiée  traité comme préliminaire).
- Verdent (échafaudage d' agent) sur vérifié: **76.1% pass@1**(le secteur de l'énergie)[technical report](https://www.verdent.ai/blog/swe-bench-verified-technical-report))
- Scores de base frontaliers sur Pro sans échafaudage d'agent: ~23-35% ([SWE-bench Pro paper](https://arxiv.org/abs/2509.16941))

Le résultat: " nous avons battu le banc SWE-Verified " n'est plus une preuve de capacité. Pro est le test de mise en place actuel. L'échafaudage agent-équipe produit des gains mesurables sur Pro (~ 30-40 points delta), ce qui est l'un des arguments empiriques les plus forts pour la coordination multi-agent en 2026.

### AAAI 2026 WMAC

Le programme de ponts 2026 de l'AAAI  Atelier sur la coordination multi-agents (https://multiagents.org/2026/Les documents acceptés et les ateliers sont le lieu canonique d'évaluation des nouvelles méthodes; renoncer aux revendications acceptées par le WMAC sur les prépriintes arXiv pour les décisions de production.

### Lire les revendications de référence de manière sceptique  la liste de contrôle de 2026

Quand quelqu'un prétend un résultat multi-agent:

1. **Which benchmark, which split?**Le SWE-bench Verified vs Pro compte beaucoup, un nombre rapporté sur la mauvaise fraction est inutile.
   Le mot grec traduit par " le mot grec "**哪个基准，哪个分割？**La différence entre les chiffres vérifiés et les chiffres de la banque SWE est très grande.
2. **Contamination check.**Le modèle a- t- il été mis en valeur après sa formation ?
   Le mot grec traduit par " le mot grec "**污染检查。**基准是否 publié après la date limite de l'entraînement du modèle ?
3. **Baseline comparison.**Contrairement à la base de l'unité de licence, contre le hasard, contre le travail de plusieurs agents antérieurs.
   Le mot grec traduit par " le mot grec "**基线比较。**Comparé à un seul programme de formation professionnelle, il n'est pas "une version inédite du même système".
4. **Statistical significance.**N essais, p-value, intervalle de confiance. les modèles frontaliers sont à forte variance; les courses simples induisent en erreur.
   Le mot grec traduit par " le mot grec "**统计显著性。**N 次试验、p 值、置信区间──前沿模型是高方差的;单次运行误导──
5. **Task diversity.**Une tâche ou plusieurs?
   Le mot grec traduit par " le mot grec "**任务多样性。**Une tâche ou plusieurs ?
6. **Cost disclosure.**Une solution à 90% à 20 fois le coût est une décision commerciale, pas une revendication de capacité.
   Le mot grec traduit par " le mot grec "**成本披露。**Pour chaque tâche, le temps de la tâche est de 20 à 90% du coût.

### Ce que aucune des valeurs de référence ne mesure bien

- **Long-horizon coordination.**Des jours d'interaction avec les cloches murales.
- **Adversarial resilience.**Que se passe-t-il quand un agent est malveillant ou compromis ?
- **Drift under deployment.**Les points de référence sont statiques; les distributions de production changent.
- **Cost-normalized performance.**La plupart des indicateurs de référence rapportent une précision brute, pas une précision par dollar.

Construire votre propre référence interne pour l'axe qui vous intéresse est souvent la bonne décision.

## Construisez-le en main
```figure
a5-bench-gap
```

## Faites-le

`code/main.py`est une marche non interactive:

- Simule 3 systèmes multi-agents sur une tâche de jouet.
- Compute les mesures marquées de style MARBLE pour chacune.
- Effectue un contrôle de contamination en détournant des tâches d'un ensemble de "formation".
- Comparé à une base aléatoire explicitement.
- Imprime une carte de référence des revendications.

Je vais courir .

```bash
python3 code/main.py
```

Expérience attendue: carte de score du système avec précision brute, réalisation de l'étape importante, coût par tâche, delta de la ligne de base par rapport au hasard et note de contrôle de la contamination.

## Utilisez-le.

`outputs/skill-benchmark-reader.md`L'évaluation de la qualité des produits de base est effectuée en fonction des critères de référence de l'entreprise.

## Envoyez-le en ligne .

Discipline de l'évaluation de la production:

- **Build an internal benchmark**Les critères de référence publics sont des informations, mais ne sont pas des remplacements.
  Le mot grec traduit par " le mot grec "**构建内部基准**reflecter votre réelle distribution de production ∙ 公共基准提供信息但不能替代──
- **Include a random baseline**Si vous ne pouvez pas battre le hasard par une grande marge sur une tâche de coordination, la tâche peut être mal posée.
  Le mot grec traduit par " le mot grec "**在每个比较中包含随机基线。**Si vous ne pouvez pas dépasser considérablement le temps dans la coordination des tâches, les tâches peuvent être définies.
- **Report cost alongside accuracy.**Les équipes d'opération ont besoin des deux.
  Le mot grec traduit par " le mot grec "**同时报告成本和准确率。**Les symboles sont nécessaires.
- **Rebuild the benchmark quarterly.**Les changements de distribution de la production; les critères de référence obsolètes induisent en erreur.
  Le mot grec traduit par " le mot grec "**每季度重建基准。**La distribution des produits est déplacée; les bases de la production sont erronées.
- **Avoid published-benchmark overfitting.**Si votre équipe optimise spécifiquement pour les numéros SWE-bench Pro, vous régresserez sur la production.
  Le mot grec traduit par " le mot grec "**避免公开基准过拟合。**Si votre équipe s'est spécialisée dans l'optimisation des chiffres Pro, vous serez en production.

## Les exercices

1. On court .`code/main.py`- Identifier lequel des trois systèmes simulés a le meilleur coût par étape.
2. Lisez MultiAgentBench (arXiv:2503.01935). Pour votre propre domaine de tâches, décidez laquelle des quatre topologies que MARBLE recommanderait.
3. Lisez le papier SWE-bench Pro. Qu'est-ce qui le rend spécifiquement résistant à la contamination?
4. Lisez les conclusions de COMMA sur la coordination multimodal. Développez une tâche de coordination multimodal simple que vous pourriez ajouter à votre référence interne.
5. Appliquez la liste de contrôle des revendications de référence au résultat de l'article de presse récent.

## Les termes clés

| Term | What people say | What it actually means |
|------|----------------|------------------------|
| MARBLE | "MultiAgentBench" / "多 Agent 基准" | ACL 2025; star/chain/tree/graph topologies with milestone KPIs. / ACL 2025；星形/链形/树形/图形拓扑，带里程碑 KPI。 |
| COMMA | "Multimodal benchmark" / "多模态基准" | Multimodal asymmetric-info coordination; frontier models struggle vs random. / 多模态不对称信息协调；前沿模型难以超越随机基线。 |
| MedAgentBoard | "Domain stress test" / "领域压力测试" | Four medical categories; often finds multi-agent does not dominate single-LLM. / 四个医疗类别；常发现多 Agent 不优于单 LLM。 |
| AgentArch | "Enterprise benchmark" / "企业基准" | Tools + memory + orchestration layered. / 工具 + 记忆 + 编排分层。 |
| SWE-bench Pro | "Contamination-resistant" / "抗污染" | 1865 problems, 41 repos; ~23% vs 70%+ on Verified (the contamination signal). / 1865 个问题，41 个仓库；~23% vs Verified 上 70%+（污染信号）。 |
| Milestone achievement / 里程碑达成 | "Partial credit" / "部分积分" | Benchmarks that reward progress, not only final success. / 奖励进展而非仅最终成功的基准。 |
| Contamination / 污染 | "Benchmark leaked into training" / "基准泄露到训练" | Post-release, benchmarks drift into training corpora; scores inflate. / 发布后，基准渗入训练语料；分数膨胀。 |
| WMAC | "AAAI 2026 Bridge Program" / "AAAI 2026 桥接项目" | Workshop on Multi-Agent Coordination; community focal point. / 多 Agent 协调研讨会；社区焦点。 |

## Encore une lecture

- [MultiAgentBench / MARBLE](https://arxiv.org/abs/2503.01935) référence de topologie avec des indicateurs clés clés
- [MARBLE repository](https://github.com/ulab-uiuc/MARBLE) mise en œuvre de référence
- [MedAgentBoard](https://arxiv.org/abs/2505.12371) test de stress de domaine; souvent, le multi-agent ne domine pas
- [AgentArch](https://arxiv.org/abs/2509.10769) architectures d'agents d'entreprise
- [SWE-bench leaderboards](https://www.swebench.com/) Scores vérifiés et pro pour les modèles frontaliers
- [AAAI 2026 WMAC](https://multiagents.org/2026/) le point focal communautaire de 2026
