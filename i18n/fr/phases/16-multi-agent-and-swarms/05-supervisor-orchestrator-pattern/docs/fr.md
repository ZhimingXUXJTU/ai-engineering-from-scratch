# Superviseur / Modèle d'orchestre-travailleur

> Un agent principal planifie et délègue; les travailleurs spécialisés exécutent dans des contextes parallèles et rapportent. C'est le modèle derrière le système de recherche d'Anthropic (Claude Opus 4 en tant que plomb, Sonnet 4 en tant que subagents), mesuré à +90,2% par rapport à l'Opus 4 à agent unique sur les évaluations internes de la recherche. Le post d'ingénierie d'Anthropic rapporte que 80% de la variance sur BrowseComp est expliquée par l'utilisation de jetons seulement  multi-agent gagne en grande partie parce que chaque sous-agent obtient une nouvelle fenêtre de contexte. Cette leçon construit le modèle de superviseur à partir des primitifs et couvre les leçons d'ingénierie de 2026 provenant des déploiements de production.

> **【中文解读】**Un agent directeur 规划并委派任务;专业化工作器在并行上下文中执行并汇报──这是人类研究系统背后的模式(Claude Opus 4.6 主管,Sonnet 4.5 子 Agent), dans l'évaluation interne de l'évaluation par rapport à un seul agent Opus 4.6 提升 90.2%──核心洞察:多 Agent 胜出主要因为每个子 Agent 获得独立的下文窗口80% de BrowseComp 方差仅由Token 使用量解释──

> **【拓展：Supervisor 模式 → Claude DevFleet】**Claude DevFleet est le superviseur de la réalisation du mode  un agent principal décompose des tâches, envoie à plusieurs arbres de travail isolés.

**Type:** Learn + Build | **类型:** 学习 + 构建
**Languages:** Python (stdlib, `threading`) | **语言:** Python (标准库, `threading`)
**Prerequisites:** Phase 16 · 04 (Primitive Model) | **前置知识:** Phase 16 · 04 (原语模型)
**Time:** ~75 minutes | **时间:** ~75 分钟

>  **【前置】**學本節前Please first master:Phase 16·04(4 个原语) 、Phase 14·01(Agent 循环) ✿Supervisor 模式 = 多 Agent
>  **【类比】**Superviseur 模式 = "projet manager + 工程师团队"──主管(Opus) décomposer tâche+examen,工作器(Sonnet)

## ♪ Problème ♪ Introduction du problème ♪

La recherche est la tâche prototypée que les systèmes à agent unique échouent. Vous demandez "qu'est-ce qui a changé dans les systèmes à agent multiple entre 2023 et 2026?" Un agent unique lit cinq documents de manière séquentielle, remplit la moitié de son contexte avec leur texte, puis doit raisonner sur tous ensemble. Il oublie le premier article au moment où il atteint le cinquième. Il ne peut pas paralléliser.

> Vous demandez "Quels changements se sont produits entre 2023 et 2026 dans le système d'agents multiples ?" Un agent unique lit cinq articles en ordre, les remplit à moitié avec le texte ci-dessous, puis doit les réfléchir ensemble.

L'échec d'un seul agent est structurel, non réalisable avec de meilleures instructions. Quelle que soit la qualité de la demande du système, la fenêtre contextuelle se remplit. Les informations nécessaires à la synthèse (les principales conclusions des cinq documents) ne correspondent pas physiquement au texte brut des documents.

> 单代理 失败是结构性的,无法用更好的提示修复──不管系统提示多好,上下文窗口都会填满──综合所需的信息(所有五篇论文的关键发现)

Le modèle de superviseur corrige ceci: un agent principal planifie la recherche, délègue chaque sous-question à un travailleur et synthétise. Chaque travailleur obtient sa propre fenêtre de 200k-token pour une question étroite. Le responsable ne voit jamais les matières premières  seulement les résumés des travailleurs.

> Le modèle du surveillant a corrigé ce problème: un agent directeur planifie la recherche, envoie chaque enfant à un outil de travail, puis complète.

Le flux d'information est la conception: les données brutes restent dans les contextes des travailleurs; seuls les résultats compressés atteignent le plomb. Le contexte du plomb est dédié à la synthèse, pas au chargement de données.

> 信息流是设计: les données originales restent sur les machines de travail dans le contexte; seulement les découvertes compressées atteignent le maître de travail.

Le système de recherche de production d'Anthropic rapporte +90,2% sur les évaluations internes de recherche par rapport à un seul Opus 4.

> Le rapport de production de l'Anthropic Research System a été évalué à +90,2% par rapport à un seul Opus 4 en interne.

Le nombre de 80% est la conclusion principale: le choix du modèle, l'ingénierie rapide et l'outillage ensemble expliquent seulement 20% de la variance. Si vous voulez une meilleure performance de l'agent de recherche, dépensez plus de jetons (plus de sous-gents, de contextes plus grands) avant de modifier les instructions.

> 80% de ce chiffre est un chiffre de référence: le modèle sélectionnement, l'ingénierie et les outils ajoutés ne expliquent que 20% de la différence. Si vous voulez mieux étudier les performances de l'agent, dépensez plus de jetons avant de modifier l'ingénierie.

## Concept Le concept central

### Le modèle

```
                 ┌──────────────┐
                 │   Lead       │  plans, decomposes,
                 │  (Opus 4)    │  synthesizes
                 └──┬────┬───┬──┘
                    │    │   │
            ┌───────┘    │   └───────┐
            ▼            ▼           ▼
      ┌─────────┐  ┌─────────┐  ┌─────────┐
      │ Worker1 │  │ Worker2 │  │ Worker3 │
      │(Sonnet) │  │(Sonnet) │  │(Sonnet) │
      └─────────┘  └─────────┘  └─────────┘
         fresh       fresh        fresh
         context     context      context
```

Le plomb ne lit jamais les matières premières, les ouvriers ne voient jamais le travail de l'autre avant que le plomb ne se synthétise.

> Le maître ne se voit jamais le travail de l'autre jusqu'à ce que le maître ne se compose pas. Chaque arbre est un ensemble de pièces de travail étroitement liées.

Cette isolation de l'information est le choix de conception principal. La fenêtre contextuelle du plomb reste axée sur la planification et la synthèse  jamais polluée par 200 000 jetons de résultats de recherche bruts.

> Cette sorte d'isolement est la principale conception de sélection. La fenêtre du directeur se concentre sur la planification et le complément.

### Pourquoi il gagne ?

Trois mécanismes:

> Trois mécanismes:

1. **Fresh context per subagent.**Un travailleur qui explore le "patrimoine de l'ACL-FIPA" ne porte pas les 40 000 jetons dépensés pour planifier.
   Le mot grec traduit par " le mot grec "**每个子 Agent 的清新上下文。**探索"FIPA-ACL 遗产" un "projet de travail non porté par un guide utilisé pour planifier des jetons de 40 000 $.
2. **Specialization via prompt.**Le conseil du chef est " décomposer et synthétiser ", pas " rechercher. " Le conseil de chaque travailleur est étroit: " trouver ce qui a changé dans X. " Les instructions ciblées produisent des résultats ciblés.
   Le mot grec traduit par " le mot grec "**通过提示专业化。**La proposition du directeur principal est "décomposer et compléter", et non "étudier"[6]. La proposition de chaque appareil est étroite:" trouver ce qui a changé X[6]. " La proposition du focus produit une output de focus[6].
3. **Parallelism.**Les ouvriers travaillent simultanément.`max(worker_times) + plan + synthesis`- Je ne sais pas .`sum(worker_times)`- Je suis désolé .
   Le mot grec traduit par " le mot grec "**并行性。**工作器并发运行──挂钟时间大约是 `max(worker_times) + plan + synthesis`, au lieu de `sum(worker_times)`Il y a une autre.

### Les cours d'ingénierie (Anthropic 2025)

Le post Anthropic énumère plusieurs leçons de production qui sont encore pertinentes pour 2026:

> Anthropic's article énumère quelques articles qui s'appliquent encore à l'expérience de production de 2026:

- **Scale effort to query complexity.**Des requêtes simples: un agent, 3 à 10 appels à l'outil. Des requêtes complexes: 10+ agents.
  Le mot grec traduit par " le mot grec "**按查询复杂度缩放工作量。**简单查询: un agent, 3-10 fois tool调用──复杂查询:10+ 个代理── le directeur doit estimer ce point, et non le调用者──
- **Broad then narrow.**Décomposer en sous-questions larges d'abord, puis engendrer plus de travailleurs par sous-question si la réponse justifie la profondeur.
  Le mot grec traduit par " le mot grec "**先宽后窄。**Pour chaque question, il faut former plus de machines à travailler.
- **Rainbow deployments.**Les agents sont longs et étroits. Le vert bleu traditionnel ne fonctionne pas. L'anthropique utilise l'arc-en-ciel: déploiement progressif de nouvelles versions tandis que les anciennes se déchargent.
  Le mot grec traduit par " le mot grec "**彩虹部署。**L'agent est un agent de longue durée en cours de fonctionnement et en état de fonctionnement.
- **Token usage dominates.**Multi-agent est ~ 15x les jetons de single-agent. Exécutez-le seulement lorsque la valeur de la tâche justifie le coût.
  Le mot grec traduit par " le mot grec "**Token 使用量占主导。**Il y a environ 15 fois plus de symboles d'un seul agent que d'un seul agent.

### Le tour de la graphie

LangGraph a envoyé une `langgraph-supervisor`bibliothèque de haut niveau `create_supervisor`En 2025, LangChain a déménagé la recommandation de mettre en œuvre le modèle de superviseur via l'appel à l'outil directement, car les appels à l'outil donnent plus de contrôle sur ce que le superviseur voit* (ingénierie contextuelle).

> LangGraph a d'abord publié un avec un haut niveau .`create_supervisor`- Je suis un assistant .`langgraph-supervisor`库──2025年 LangChain va proposer de se transformer en outil pour mettre en œuvre directement le mode de surveillance, car les outils de surveillance fournissent plus de contrôle.

Le changement reflète une vision de 2025-2026: l'ingénierie contextuelle compte plus que l'ingénierie orchestration. Ce que le superviseur voit détermine ce qu'il peut planifier.

> Ce changement reflète l'idée de 2025-2026: le développement de l'ingénierie sous-jacente est plus important que le développement de l'élaboration.

### Les modes d'échec

- **Lead hallucinates the plan.**Si le plomb génère des sous-questions qui ne décomposent pas la vraie question, les travailleurs effectuent des recherches précises sur la mauvaise cible.
  Le mot grec traduit par " le mot grec "**主导者幻觉计划。**Si le problème généré par le maître ne résoud pas le problème réel, le travail effectue une étude précise sur l'objectif de l'erreur.
- **Workers over-explore.**Sans limites de portée explicites, les travailleurs dépassent leur sous-question assignée et polluent l'étape de synthèse.
  Le mot grec traduit par " le mot grec "**工作器过度探索。** sans limites de portée, le travail se déplace au-delà de son domaine de distribution et de la pollution 
- **Synthesis conflicts.**Deux travailleurs rapportent des faits contradictoires. Le prospect doit soit réinterroger (ajouter une ronde) ou noter explicitement le désaccord.
  Le mot grec traduit par " le mot grec "**综合冲突。**两个工作器回复矛盾的事实――主导者必须重新询问(增加一轮) 或明确记录分歧――静默选择一方是最糟糕的失败:用户永远不知道发生分歧――

### Quand le superviseur a tort

- **Sequential tasks.**Si l'étape 2 a besoin de la sortie de l'étape 1, le parallélisme n'achète rien.
  Le mot grec traduit par " le mot grec "**顺序任务。**Si le pas 2 a vraiment besoin de la sortie du pas 1, la marche n'a pas d'aide.
- **Simple queries.**L'agent unique les traite plus vite et moins cher.
  Le mot grec traduit par " le mot grec "**简单查询。**单代理更快更便宜地处理它们―― utiliser le contrôleur de "réduction du travail" avant de créer un outil de travail―
- **Strict determinism.**Le superviseur utilise une délégation sélectionnée par le LLM. Les graphiques statiques sont meilleurs lorsque l'audit/réplique est plus important que l'adaptabilité.
  Le mot grec traduit par " le mot grec "**严格确定性。**监督者使用 LLM 选择的委派──当审计/回放比适应性更重要时,静态图更好──

## Construisez-le et mettez-le en œuvre.
```figure
supervisor-hierarchy
```

## Faites-le

`code/main.py`Il met en œuvre un superviseur de trois travailleurs parallèles en utilisant `threading`. Le plomb décompose une requête en sous-questions, les travailleurs s'exécutent simultanément sur chaque sous-question et le plomb est synthétisé.

> `code/main.py`Utilisation `threading` réaliser un supervisor de trois outils de travail.  Le supervisor va décomposer la requête en un problème, le travail sera décomposé sur chaque problème, le supervisor sera complété.

Structure clé:

> 关键结构:

- `Lead.plan(query)`une requête est divisée en 3 sous-questions.
  Le mot grec traduit par " le mot grec "`Lead.plan(query)`La question sera divisée en trois questions.
- `Worker.run(sub_q)`renvoie un faux résumé (peut être un agent utilisant des outils dans la production).
  Le mot grec traduit par " le mot grec "`Worker.run(sub_q)`返回一个假摘要(可以在生产中是任何工具的代理)
- `Lead.run(query)`Il dégage les travailleurs en fils, en joints et en synthétise.
  Le mot grec traduit par " le mot grec "`Lead.run(query)`En cours de route, démarrer le travail, attendre, puis compléter.

Je vais courir .

```
python3 code/main.py
```

La sortie montre le plan, les traces de l'ouvrier parallèle avec des timestamps de début/fin et la synthèse finale.

> 输出显示计划、带有开始/结束时间的并行工作器跟踪和最终综合―― vous pouvez voir le temps de fonctionnement de l'appareil fonctionne en 0,35 secondes plutôt que 0,9 secondes.

## Utilisez-le avec le cadre de réalisation

`outputs/skill-supervisor-designer.md`Il prend une requête utilisateur et produit une conception de modèle de superviseur: prompt du système de conduite, rôles de travailleurs, règles de décomposition des sous-questions et modèle de synthèse.

> `outputs/skill-supervisor-designer.md`Recevoir des requêtes utilisateur et générer des modèles de surveillance: principal système de suggestions 工作器角色、子问题分解规则和综合模板──在构建新的研究风格 系统之前使用──

## Envoyez-le . Produit .

Liste de contrôle avant de déployer un modèle de surveillance:

> Liste des contrôles effectués par le ministère de la Santé:

- **Model pairing.**Le plomb sur un modèle de niveau de raisonnement (classe Opus, `o3`Les travailleurs travaillent sur un modèle plus rapide et moins cher (Sonnet, `o4-mini`)
  Le mot grec traduit par " le mot grec "**模型配对。**Le modèle de l'équipe de formation est le modèle de formation de l'équipe de formation.`o3`类) ・工作器使用更快、更便宜的模型(Sonnet、`o4-mini`)。
- **Worker timeout.**Tout travailleur qui dépasse 2 fois la durée moyenne de fonctionnement est tué; le plomb se réorganise avec une portée plus étroite ou se déplace sans elle.
  Le mot grec traduit par " le mot grec "**工作器超时。** Tout appareil de plus de 2 fois le temps de fonctionnement est arrêté; le conducteur doit soit se reproduire dans une gamme plus étroite, soit ne pas continuer à l'utiliser.
- **Token cap per worker.**Une limite dure (par exemple 10 fois plus importante que la synthèse prévue) empêche un travailleur en fuite de dépenser le budget.
  Le mot grec traduit par " le mot grec "**每个工作器的 Token 上限。**硬限制 (par exemple, 10 fois plus de l'entrée globale prévue) empêcher les machines de travail de perdre leur budget.
- **Observability.**Suivez le plan du chef, les appels à l'outil de chaque travailleur et la synthèse.
  Le mot grec traduit par " le mot grec "**可观测性。**Suivre le plan du directeur, le travail et l'ensemble des outils de chaque outil.
- **Rainbow rollout.**Les agents de longue date ont besoin d'une transition progressive, pas d'un échange.
  Le mot grec traduit par " le mot grec "**彩虹推出。**Il faut une version progressive de l'agent, pas un échange chaud.

## Les exercices

1. On court .`code/main.py`En ce qui concerne le nombre de travailleurs, le coût de production dépasse les économies parallèles dans cette démonstration.
   Le mot " l' économie " est traduit par " l' économie ".`code/main.py`, puis modifier le directeur pour produire 5 machines au lieu de 3 machines. Observer l'effet du temps de travail. Dans cette démonstration, combien de machines atteindront le nombre de fois que la production de dépenses dépassera les épargne ?
2. Mettre en œuvre un délai de travail: tuer tout travailleur qui court plus de 0,5 seconde et avoir le plomb synthétiser les résultats restants.
   L'équipe de gestion de l'exploitation de l'équipement de travail doit être interrompue.
3. Ajouter une étape de détection des conflits à la synthèse du leader: si deux travailleurs répondent à des réponses contradictoires, le leader note le désaccord plutôt que de choisir un. Comment détecter une contradiction sans appeler un LLM?
   Dans le cadre de l'ensemble du maître, ajouter des conflits de contrôle étapes: si deux machines de travail répondent à des contradictions, le maître de travail enregistrera des différences au lieu de choisir l'une de celles-ci.
4. Lisez le rapport d'ingénierie de la société Anthropic sur les systèmes de recherche.
   Le jeu est présenté en trois manières différentes.
5. Comparer avec LangGraph `create_supervisor`Pourquoi Anthropic ne passe explicitement que des sous-répondices et non pas le contexte des travailleurs brut dans la synthèse ?
   La langue officielle de la langue française est la langue officielle de la langue française.`create_supervisor`Pourquoi l'anthropique 明确只传递子答案而不是原始工作器上下文到综合中?

## Les termes clés

| Term | What people say | What it actually means |
|------|----------------|------------------------|
| Supervisor / 监督者 | "Lead agent" / "主导 Agent" | An orchestrator agent that plans, delegates, and synthesizes. Does not do the work itself. / 规划、委派和综合的编排 Agent。不做实际工作。 |
| Worker / 工作器 | "Subagent" / "子 Agent" | A focused agent invoked by the supervisor with narrow scope and its own context window. / 由监督者调用的聚焦 Agent，具有狭窄范围和自己的上下文窗口。 |
| Orchestrator-worker / 编排器-工作器 | "Supervisor pattern" / "监督者模式" | Same thing, different name. The 2026 literature uses both. / 同一事物，不同名称。2026 年文献两者都用。 |
| Fresh context / 清新上下文 | "Clean window" / "干净窗口" | A worker's context starts from its system prompt and assigned question, not the lead's history. / 工作器的上下文从其系统提示和分配的问题开始，而不是主导者的历史。 |
| Rainbow deployment / 彩虹部署 | "Gradual rollout" / "渐进推出" | Long-running stateful agents need versioned drain-and-replace, not blue-green. / 长时间运行的有状态 Agent 需要版本化的排空和替换，而不是蓝绿部署。 |
| Token dominance / Token 主导 | "Context is the variable" / "上下文是变量" | 80% of research-eval variance comes from total tokens used, not model choice, per Anthropic. / 80% 的研究评估方差来自使用的总 token，而不是模型选择，据 Anthropic。 |
| Scale effort / 缩放工作量 | "Match agent count to complexity" / "按复杂度匹配 Agent 数量" | Lead estimates query difficulty, spawns 1 vs 10+ workers accordingly. / 主导者估计查询难度，相应地生成 1 个或 10+ 个工作器。 |
| Synthesis conflict / 综合冲突 | "Workers disagree" / "工作器不一致" | Two workers return contradictory facts; the lead must surface disagreement, not silently pick one. / 两个工作器返回矛盾的事实；主导者必须揭示分歧，而不是静默选择一方。 |

## Encore une lecture

- [Anthropic engineering — How we built our multi-agent research system](https://www.anthropic.com/engineering/multi-agent-research-system) la référence de production pour le modèle de surveillance
  Traduction anglaise:Anthropic 工程  我们如何构建多 代理研究系统 监督者模式的生产参考
- [LangGraph workflows and agents](https://docs.langchain.com/oss/python/langgraph/workflows-agents) le superviseur d'appel d'outils est maintenant la forme recommandée
  L'agent  工具调用监督者现在是推的形式
- [LangGraph supervisor reference](https://reference.langchain.com/python/langgraph-supervisor) l'assistant hérité, encore utilisé en production en 2026
  Traduction anglaise: LangGraph 监督者参考  旧版助手, encore utilisé 2026年生产
- [OpenAI cookbook — Orchestrating Agents: Routines and Handoffs](https://developers.openai.com/cookbook/examples/orchestrating_agents) Variante de superviseur basée sur la remise
  En anglais, le code de la langue française est le code de la langue française.
