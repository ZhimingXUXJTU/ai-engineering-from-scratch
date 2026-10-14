# Développement d' un agent Eval-Driven

> L'évaluation n'est pas la dernière étape, c'est la boucle extérieure qui motive tous les autres choix de la phase 14.

**Type:** Learn + Build | **类型:** 构建
**Languages:** Python (stdlib) | **语言:** Python (标准库)
**Prerequisites:** All of Phase 14. | **前置知识:** 见原文
**Time:** ~60 minutes | **时间:** 见原文

>  **【前置】**Les modes d'échec de la phase 14 sont les modes de prévention de la phase 14 et de la phase 14 et de la phase 14 et de la phase 14 et de la phase 14 et de la phase 14 et de la phase 14 et de la phase 14 et de la phase 14 et de la phase 14 et de la phase 14 et de la phase 14 et de la phase 14 et de la phase 14 et de la phase 14 et de la phase 14 et de la phase 14 et de la phase 14 et de la phase 14 et de la phase 14 et de la phase 14 et de la phase 14 et de la phase 14 et de la phase 14 et de la phase 14 et de la phase 14 et de la phase 14 et de la phase 14 et de la phase 14 et de la phase 14 et de la phase 14 et de la phase 14 et de la phase 14 et de la phase 14 et de la phase 14 et de la phase 14 et de la phase 14 et de la phase 14 sont les phases 14 et de phase 14 et de phase 14 et de phase 14 et de phase 14 et de phase 14 et de phase 14 et de phase 14 et de phase 14 sont les phases 14 et de phase 14 et de phase 14 et de phase 14 sont utilisées.

## Objectifs d'apprentissage

- Nombre des trois couches d'évaluation  référence statique, production personnalisée hors ligne, production en ligne  et à quoi sert chacune.
- Expliquez la boucle serrée de l'évaluateur-optimisateur.
- Décrire les meilleures pratiques de 2026: évaluations en direct à côté du code, exécutées en CI, relations en porte.
- Connectez chaque leçon de la phase 14 à l'évaluation qu'elle génère.

## Le problème , l' introduction du problème

Les agents passent des démos. Ils échouent dans la production de manière que les démos ne peuvent pas prévoir. Les critères de référence répondent " est-ce que ce modèle est largement capable ? " et non " est-ce que cet agent expédie les bons patchs pour mon produit ? " La réponse: évaluation à trois couches, en cours de fonctionnement continu, avec chaque garde-corps et règle apprise cartographiée à un cas d'évaluation.

>  **【类比】**L'agent eval 像给运动员做体检3 个层级:(1) **静态基准**(SWE-bench、BFCL) =国家体能测试,比平均水平;**定制离线 eval**= pour le projet de conception de votre projet (comme " taux de réussite de la modification de ce bug ") = entraînement en équipe;**在线生产 eval**= réel utilisateur contre  = A/B 测试──三层缺一不可

> ️ **【易错点】**L' agent eval de 3 个坑:**只测 happy path**eval 集全是简单查询, complexe situation n'est pas couvert;务必构建对抗性 测试(模糊指令、攻击、边界值)**eval 不进 CI** développement时手工跑一次就过,上线后没人跑;eval 必须进 GitHub Actions,PR 不过 eval 不能合并──(3) **eval 集污染**Exemple de quelques coups de vue de l'information de l'époque,

> L'agent a passé la démonstration. Ils ont échoué de manière imprévisible dans la production. Le principe de base est de répondre " ce modèle a-t-il une capacité étendue ? " plutôt que " cet agent fournit-il des suppléments corrects pour mon produit ? " La réponse est: trois niveaux d'évaluation, de fonctionnement continu, de chaque traitement et de la règle d'apprentissage sont tous mappés à un exemple d'évaluation.


> **【中文解读】**评估驱动的代理 开发(Eval-Driven Development) 将在传统软件工程中的TDD 应用于 代理:先定义评估标准,再实现 Agent──核心挑战是 代理的不确定性

> **{【拓展：Eval-Driven Agent Development 是 2025-2026 年的最佳实践。核...】}**Le développement d'agents Eval-Driven est la meilleure pratique de 2025-2026: 1) AgentOpsAgent trace et évaluation de la plateforme; 2) LangSmithLangChain; 3) BraintrustAI évaluation Framework。 Key insight:L'évaluation de l'agent doit être basée sur une trajectoire complète (la trajectoire) plutôt que sur le produit final Deux agents peuvent obtenir le même résultat, mais l'un a suivi 5 étapes, l'autre a suivi 50 étapes, la qualité et les coûts sont énormes.
## Le concept de base.

### Trois couches d'évaluation

1. **Static benchmarks** SWE-bench Verifié pour le code (leçon 19), WebArena/OSWorld pour la navigation / bureau (leçon 20), GAIA pour généraliste (leçon 19), BFCL V4 pour l'utilisation d'outils (leçon 06). Utilisation pour la comparaison entre modèles et la régression. La contamination est réelle: SWE-bench+ a trouvé 32,67% de fuite de solution.

2. **Custom offline evals** la forme de votre produit:
   - Leur rôle est de rendre des comptes à la Cour des comptes.
   - Basé sur l'exécution (exécuter le patch, vérifier les tests).
   - Basé sur la trajectoire (comparer les séquences d'action contre l'or; OSWorld-Human montre des agents supérieurs de 1,4-2,7 fois plus que l'or).

3. **Online evals** production:
   - Retours de séance (Langfuse).
   - Alertes déclenchées par la garde-ferre (leçon 16, 21).
   - Suivi des coûts / latences par étape (leçon 23 OTel couvre).

### Évaluateur-optimisateur (anthropique)

La boucle serrée:

1. Le proposateur génère la sortie.
2. Les juges évaluateurs.
3. Rétroyer jusqu'à ce que l'évaluateur passe.

Tout flux d'agent qui vous intéresse peut être intégré à un évaluateur-optimisateur pour la fiabilité.

> C'est la généralisation de l'auto-réfinition. Tout processus d'agent que vous aimez peut être utilisé avec un évaluateur-optimisateur pour améliorer la fiabilité.

> 评估驱动的代理 开发(Eval-Driven Development) sera évalué comme le cœur de l'Agent 开发──先定义评估标准,再构建 Agent,用评估轨迹指导改进──

### 2026 les meilleures pratiques

- Les Evals vivent à côté du code.
- Rendez-vous au renseignement sur chaque affaire.
- La combinaison des portes sur les scores d'évaluation (par exemple "pas de régression > 5% contre principal").
- Chaque garde-garde est une carte d'évaluation.
- Chaque règle apprise (Reflection, pro-workflow learning-rule) correspond à un cas d'échec.

### Lier la phase 14 ensemble

Chaque leçon de la phase 14 génère des cas d'évaluation:

| Lesson | Eval case it generates |
|--------|------------------------|
| 01 Agent Loop | Budget-exhausted, infinite-loop guard |
| 02 ReWOO | Planner replans correctly when a tool fails |
| 03 Reflexion | Learned reflections apply on retry |
| 05 Self-Refine/CRITIC | Judge passes refined output |
| 06 Tool Use | Argument coercion works; unknown tools rejected |
| 07-10 Memory | Retrieval citations match sources; stale facts invalidate |
| 12 Workflow Patterns | Each pattern produces correct output |
| 13 LangGraph | Resume reproduces state exactly |
| 14 AutoGen Actors | DLQ catches crashed handlers |
| 16 OpenAI Agents SDK | Guardrail trips on the right inputs |
| 17 Claude Agent SDK | Subagent results return to orchestrator |
| 19-20 Benchmarks | SWE-bench Verified score, WebArena success rate, OSWorld efficiency |
| 21 Computer Use | Per-step safety catches injected DOM |
| 23 OTel | Spans emit required attributes |
| 26 Failure Modes | Detectors tag known failures |
| 27 Prompt Injection | PVE refuses poisoned retrievals |
| 28 Orchestration | Supervisor routes to the right specialist |
| 29 Runtime Shapes | DLQ handles N% failure |

Si votre suite d'évaluation contient des cas pour chacun, vous avez couvert la phase 14.

> Si votre ensemble d'évaluation a des exemples d'utilisation de chaque cours, vous avez déjà couvert la phase 14.

> 评估驱动的代理 开发(Eval-Driven Development) sera évalué comme le cœur de l'Agent 开发──先定义评估标准,再构建 Agent,用评估轨迹指导改进──

### Lorsque le développement axé sur l'évaluation échoue

- **No baseline.**Les Evals sans le dernier bon connu sont illisibles.
- **LLM-judge without grounding.**Les juges ont également des hallucinations.
- **Over-fitting to evals.**L'optimisation pour l'évaluation est différente de l'utilité de la production.
- **Flaky evals.**Les cas non déterministes provoquent de fausses alarmes.

> **没有基线。**Aucune évaluation de l'état de stockage de l'information n'est définitivement possible.
> **LLM 评审器没有基础。**评审器也会幻觉──CRITIC 模式(第 5 课) 评审器基于外部工具──
> **过拟合评估。**Pour évaluer l'optimisation des démarches de production en usage pratique, la transformation des usages est nécessaire.
> **不稳定的评估。**Les cas d'utilisation non déterminés entraînent des erreurs de déclaration.

## Construisez-le et mettez-le en œuvre.
```figure
ae-eval-three-layers
```

## Faites-le

`code/main.py`est un harnais d'évaluation stdlib:

- Registre de cas avec catégories (marque de référence, personnalisée, en ligne).
- Un agent sous contrôle.
- Loup évaluateur-optimisateur: proposer, juger, affiner jusqu'à passer ou à la ronde maximale.
- Porte CI: taux de réussite agrégé + régression par rapport à la ligne de référence.

- Je vais le faire.

```
python3 code/main.py
```

Résultats: par cas, défaillance, flag de régression, verdict de la porte CI.

> 输出: chaque cas de défaite/faillite 归归标志 CI 门控裁定

> 评估驱动的代理 开发(Eval-Driven Development) sera évalué comme le cœur de l'Agent 开发──先定义评估标准,再构建 Agent,用评估轨迹指导改进──

## Utilisez-le avec le cadre de réalisation

- Écrivez des cas d'évaluation dans le même repo que votre code d'agent.
- Retourne sur chaque rapport public via CI.
- Faut pas construire sur la régression.
- Suivez le taux de réussite au fil du temps.
- Rattache chaque échec de production à un nouveau cas.

## Envoyez-le . Produit .

`outputs/skill-eval-suite.md`construit une suite d'évaluation en trois couches pour un produit agent avec des portes CI et un suivi de régression.

> `outputs/skill-eval-suite.md`Pour la construction de produits d'agents, trois niveaux de kits d'évaluation comprennent le suivi des activités de contrôle et de retour.

> 评估驱动的代理 开发(Eval-Driven Development) sera évalué comme le cœur de l'Agent 开发──先定义评估标准,再构建 Agent,用评估轨迹指导改进──

## Les exercices

1. Prenez une de vos erreurs de production, écrivez une évaluation qui la reproduit.
  Le mot "exercer" est traduit par "exercer".
2. Construisez une rubrique de juge de LLM pour votre domaine avec trois dimensions (factuelle, ton, portée).
  Le mot "exercer" est traduit par "exercer".
3. Faites passer la suite d'évaluation dans l'IC. Faites échouer la construction sur la régression >=5%.
  Le mot "exercer" est traduit par "exercer".
4. Ajoutez une métrique de trajectorie-efficacité: combien d'étapes l'agent a-t-il fait par rapport à une trajectoire d'or?
  Le mot "exercer" est traduit par "exercer".
5. Mettez chaque leçon de phase 14 dans une évaluation de votre suite.
  Le mot "exercer" est traduit par "exercer".

## Les termes clés

| Term | What people say | What it actually means |
|------|----------------|------------------------|---|
| Static benchmark | "Off-the-shelf eval" | SWE-bench, GAIA, AgentBench, WebArena, OSWorld |  |
| Custom offline eval | "Domain eval" | LLM-as-judge / exec / trajectory on your product shape |  |
| Online eval | "Production eval" | Session replay, guardrail alerts, cost/latency tracking |  |
| Evaluator-optimizer | "Propose-judge-refine" | Iterate until judge passes |  |
| CI gate | "Merge blocker" | Fail the build on eval regression |  |
| Baseline | "Last-known-good" | Reference score to detect regression |  |
| Trajectory efficiency | "Steps over gold" | Agent step count divided by human expert minimum |  |

## Encore une lecture

- [Anthropic, Building Effective Agents](https://www.anthropic.com/research/building-effective-agents) "débuter simple, optimiser avec les évaluations"
  Le mot "réfléchisseur" est traduit par "réfléchisseur".
- [OpenAI, SWE-bench Verified](https://openai.com/index/introducing-swe-bench-verified/) l'indice de référence sélectionné
  Le mot "réfléchisseur" est traduit par "réfléchisseur".
- [Berkeley Function Calling Leaderboard](https://gorilla.cs.berkeley.edu/leaderboard.html) référence de l'utilisation des outils
  Le mot "réfléchisseur" est traduit par "réfléchisseur".
- [Langfuse docs](https://langfuse.com/) évaluations + répétition de session en pratique
  Le mot "réfléchisseur" est traduit par "réfléchisseur".
