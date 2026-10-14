# Planification avec HTN et Evolutionary Search .

> La planification symbolique traite les cas où le plan est prouvablement correct. La recherche de code évolutionnaire traite les cas où la fonction de fitness est vérifiable par machine. ChatHTN (2025) et AlphaEvolve (2025) montrent ce que chacun déverrouille lorsqu'il est associé à un LLM.

> **【中文解读】**Le programme de traitement des codes de programmation peut être prouvé correctement dans un scénario.

**Type:** Build | **类型:** 构建
**Languages:** Python (stdlib) | **语言:** Python (标准库)
**Prerequisites:** Phase 14 · 02 (ReWOO and Plan-and-Execute) | **前置知识:** Phase 14 · 02 (ReWOO 与计划-执行)
**Time:** ~75 minutes | **时间:** ~75 分钟

## Objectifs d'apprentissage

- Expliquer les réseaux de tâches hiérarchiques: tâches, méthodes, opérateurs, pré-conditions, effets.
  Le mot "définition" est traduit par "définition".
- Décrivez la recherche symbolique  en boucle hybride de ChatHTN avec décomposition de la chute de LLM.
  Le mot "château" est un mot qui signifie "câteau" ou "câteau".
- Expliquez la boucle évolutionnaire d'AlphaEvolve et pourquoi elle ne fonctionne qu'avec un évaluateur programmatique.
  Expliquer le cycle d'évolution d'AlphaEvolve et pourquoi il n'est efficace que dans les évaluateurs procéduraux.
- Mettre en œuvre un planificateur de jouets HTN plus une recherche évolutionnaire de jouets dans Stdlib.
  Le jeu est un jeu de société.

## Le problème , l' introduction du problème

ReWOO (leçon 02), Plan-et-Execute et ReAct couvrent la plupart des projets d'agents.

> ReWOO(第 2 课) 、Plan-and-Execute 和 ReAct 覆盖了大多数 经纪规划──两种它们不能很好覆盖的情况:

1. **Plans with provable correctness.**Le plan doit être solide par construction.Un plan de LLM fluide qui parfois hallucine une étape est inacceptable.
   Le mot grec traduit par " le mot grec "**可证明正确性的计划。**Le plan de planification de la navigation doit être fiable dans la construction.
2. **Optimizations with a machine-checkable fitness function.**La multiplication de matrice, l'heuristique de planification, le compilateur passe  l'objectif n'est pas "un plan correct" mais "le meilleur plan".
   Le mot grec traduit par " le mot grec "**有机器可检查适应度函数的优化。**Le but de la réussite n'est pas "un plan correct", mais "le meilleur plan".

> **【中文解读】**Les deux principaux types de planification d'agents: réseau de tâches de niveau séparé (HTN) et planification évolutive.

HTN Planning et AlphaEvolve résolvent les deux problèmes différents.

> HTN 规划和 AlphaEvolve 解决两个不同的问题──都将LLM用作放大器而非替代品──

> **【拓展：2026 年 Agent 规划的前沿】**AlphaEvolve et Darwin-Godel Machine vont développer des algorithmes appliqués à l'optimisation de la stratégie de l'agent non seulement en planifiant les tâches, mais aussi en planifiant et en optimisant le processus de planification lui-même.

>  **【前置】**必須先通過Fase 14·02 (ReWOO/Plan-and-Execute) HTN est sa version "strict formalization"; ainsi que les connaissances de planification de l'IA classique fondamentales (status、前置条件、效果) ── Si vous n'avez pas écouté les STRIPS ou le PDDL, suggérez de commencer à compléter les deux sections du "Classical符号 AI"

## Le concept de base.

### Réseaux hiérarchiques de tâches

Un HTN est:

> HTN est:

- **Tasks** composé (à décomposer) et primitif (exécutable directement).
  Le mot grec traduit par " le mot grec "**任务**复合(待分解)和原始(直接可执行)
- **Methods** des moyens de décomposer une tâche composée en sous-tâches, avec des conditions préalables.
  Le mot grec traduit par " le mot grec "**方法**将复合任务分解为子任务的方式,带前置条件──
- **Operators** actions primitives avec des conditions préalables et des effets.
  Le mot grec traduit par " le mot grec "**操作符**带前置条件和效果的原始动作──
- **State** un ensemble de faits.
  Le mot grec traduit par " le mot grec "**状态**Il y a une série de faits.

Planification: compte tenu d'une tâche cible et d'un état initial, trouver une décomposition en opérateurs primitifs dont les conditions préalables sont satisfaites en séquence.

> 规划: donner un objectif déterminé à l'opérateur et un état initial, trouver un schéma de décomposition en fonction de l'opérateur initial, et satisfaire ses conditions de mise en avant.

Le HTN est plus ancien que les LLM et constitue toujours la référence pour des plans prouvablement corrects.

> Le HTN est plus ancien que le LLM, mais il est encore un référentiel à la planification.

### Le projet de loi de l'Union européenne sur les droits de l'homme (CATHN)

ChatHTN (arXiv:2505.11814) interpose le HTN symbolique avec les requêtes de LLM:

> Le programme de formation est basé sur le programme de formation de formation professionnelle.

1. Essayez de décomposer la tâche complète actuelle avec les méthodes existantes.
   Traduction anglaise: essayer d'utiliser des méthodes existantes pour résoudre des tâches complexes.
2. Si aucune méthode n'est appliquée, demandez au LLM: "comment décomposeriez-vous `task`dans l' État `s`Je suis là.
   Si vous n'avez pas de méthode, demandez à l'LLM:`s`Comment allez-vous décomposer ?`task`Je suis là.
3. Transformer la réponse du LLM en sous-tâches candidates.
   Le programme de formation en droit est une formation de premier cycle.
4. Valider contre le schéma de l'opérateur; rejeter les décompositions invalides.
   Le modèle d'essai de l'opérateur est le même que celui de l'opérateur.
5. - Il faut recourir.
   Le mot "réciproque" est traduit par "réciproque".

L'affirmation centrale du document: chaque plan produit est prouvablement solide car les suggestions de LLM ne sont introduites que sous forme de décompositions candidates, jamais sous forme de modifications directes du plan.

>  **【类比】**ChatHTN 像严格的审计员 (严格的审计员) 符号层) + 创意实习生 (创意实习生) LLM (实习生提建议:"Je pense que cet objectif peut être décomposé de cette façon..."**结果**Tous les plans de mise en œuvre finale ont été vérifiés, leur fiabilité est garantie.

> 论文的核心主张: chaque plan de développement peut être prouvé comme fiable, car les recommandations de l'LLM ne sont pas des éditeurs de projets directs, mais seulement des candidats à l'entrée en vigueur.

Apprentissage en ligne des méthodes (OpenReview `gwYEDY9j2x`Le programme de suivi de la formation (en 2025) ajoute un apprenant qui généralise les décompositions produites par le LLM par régression  réduisant la fréquence de requête du LLM à 75%.

> En 2025, les études de premier cycle ont été menées à des études de premier cycle et des études de troisième cycle ont été menées à des études de premier cycle.

### AlphaEvolve (Novikov et coll., 2025)

AlphaEvolve (arXiv:2506.13131, DeepMind, juin 2025) est une bête différente: recherche de code évolutif orchestrée par un ensemble de Gémeaux 2.0 Flash/Pro.

> AlphaEvolve (arXiv:2506.13131, DeepMind,2025 年 6 月) est une autre existence:

- Le boucle:

> 循环:

1. Commencez par un programme de semence + un évaluateur programme (retourne un score de fitness).
   Le récit de la rédaction de la Bible est le récit de la rédaction de la Bible.
2. L'ensemble des LLM propose des mutations.
   Le groupe de formation a proposé des changements.
3. Faites passer les mutations par l'évaluateur.
   Le mot "réalité" est traduit par "réalité".
4. Gardez le meilleur, muter à nouveau.
   Le meilleur est conservé, le meilleur est changé.

Les gains publiés:

>  résultats publiés:

- Première amélioration par rapport à Strassen pour la multiplication de matrice complexe 4x4 en 56 ans (48 multiplication scalaire).
  Le système de calcul de la fréquence de la fréquence est le système de calcul de la fréquence de la fréquence de la fréquence.
- 0,7% ont récupéré le calcul de Google via une heuristique de planification Borg.
  Le nombre de personnes qui ont été incluses dans le programme de recherche de Google est de 0,7% .
- 32% de vitesse de FlashAttention sur une charge de travail frontalière.
  En anglais, le nombre de personnes qui ont été vaccinées est de 32%.

La contrainte dure: la fonction de fitness doit être vérifiable par machine.

> ️ **【易错点】**Pour que le programme d'écriture de l'AlphaEvolve soit optimisé, il faut utiliser les algorithmes de rédaction de la petite histoire, en utilisant les notes de l'écriture de l'alphaEvolve comme un moyen de réussir.**后果**Le nombre de points de réussite est de 30% à 30% en fonction de la fonction de fitness.**一行修复**: seulement pour les " tâches de programmation ayant un indicateur objectif " avec AlphaEvolve ((code performance, taux de test de couverture, efficacité de régulation), créativité

> 硬约束: la fonction de l'adaptation doit être machine à vérifier ⋅ pour les réponses au texte de recherche évoluée ne recevra ⋅

### Quand utiliser quel

| Problem class | Use | Why |
|---------------|-----|-----|
| 问题类别 | 使用 | 原因 |
| Scheduling with hard constraints | HTN + ChatHTN | Provable soundness / 可证明的可靠性 |
| Compiler optimization | AlphaEvolve | Machine-checkable fitness / 机器可检查的适应度 |
| Multi-step task execution | ReAct / ReWOO | LLM in the loop, no formal guarantees / LLM 在循环中，无形式化保证 |
| Code improvement with tests | AlphaEvolve | Tests are the evaluator / 测试即评估器 |
| Policy-bound automation | HTN | Preconditions encode policy / 前置条件编码策略 |

### Où ce modèle va mal

- **HTN without operators.**Sans précondictions/ schémas d'effet, l'affirmation de solidité s'effondre.
  Le mot grec traduit par " le mot grec "**没有操作符的 HTN。**无前置条件/效果模式, fiabilité déclaration est désintégrée.
- **AlphaEvolve without a real evaluator.**" Demandez au LLM si le code est meilleur " n'est pas une fonction de fitness.
  Le mot grec traduit par " le mot grec "**没有真正评估器的 AlphaEvolve。**"Question LLM 代码是否更好" n'est pas une fonction d'adaptation.
- **Over-engineering.**La plupart des tâches d'agent n'en ont pas besoin.
  Le mot grec traduit par " le mot grec "**过度工程。**La plupart des agents ne nécessitent aucun.

> 🤔 **【困惑】**Q: ChatHTN 论文说"LLM 只是提建议不直接进计划"这跟LangChain Agent 调用工具不是一回事吗? A: 不一样.

## Construisez-le en main
```figure
htn-tree-expand
```

## Faites-le

`code/main.py`Il met en œuvre deux jouets:

> `code/main.py`Il y a deux jouets:

- Un planificateur de réseau de téléphonie électronique avec opérateurs, méthodes, préconitions, effets et un`LLMFallback`Le "LLM" est un décomposateur scripté, donc le planificateur fonctionne hors ligne.
  Un système de programmation de fonctionnement de la fonction d'un système de programmation de fonctionnement de fonctionnement de fonctionnement de fonctionnement de fonctionnement de fonctionnement de fonctionnement de fonctionnement de fonctionnement de fonctionnement de fonctionnement de fonctionnement de fonctionnement de fonctionnement de fonctionnement de fonctionnement de fonctionnement de fonctionnement de fonctionnement de fonctionnement de fonctionnement de fonctionnement de fonctionnement de fonctionnement de fonctionnement de fonctionnement de fonctionnement de fonctionnement de fonctionnement de fonctionnement de fonctionnement de fonctionnement de fonctionnement de fonctionnement de fonctionnement de fonctionnement de fonctionnement de fonctionnement de fonctionnement de fonctionnement de fonctionnement de fonctionnement de fonctionnement de fonctionnement de fonctionnement de fonctionnement de fonctionnement de fonctionnement de fonctionnement de fonctionnement de fonctionnement de fonctionnement de fonctionnement de fonctionnement de fonctionnement de fonctionnement de fonctionnement de fonctionnement de fonctionnement de fonctionnement de fonctionnement de fonctionnement de fonctionnement de la fonctionnement de la fonctionnement de l'un système de fonctionnement de fonctionnement de fonctionnement de fonctionnement de fonctionnement de la fonctionnement de la fonctionnement de la fonction de la fonction de la fonction de la fonction de la fonction de la fonction.`LLMFallback` "LLM" est un scénario décodeur, planificateur à utiliser en ligne
- Une recherche évolutive stdlib sur les programmes arithmétiques: développer des expressions dont la production est minimisée `|f(x) - target|`L'évaluation est déterministe.
  Traduction anglaise: un standard de recherche, dans le processus de calcul:`|f(x) - target|`Dans le test de l'ensemble, la plus petite expression est déterminante.

- Je vais le faire.

> 运行:

```
python3 code/main.py
```

La trace montre le planificateur HTN décomposant une tâche composée (avec un retrait de LLM au milieu du plan) et la boucle évolutionnaire convergeant sur une expression cible.

> 轨迹显示 HTN 规划器分解复合任务(带中途 LLM 回退)

## Utilisez-le avec le cadre de réalisation

- **HTN planners** `pyhop`- Je suis là .`SHOP3`, ou construire votre propre pour l'application de la politique spécifique à un domaine.
  Le mot grec traduit par " le mot grec "**HTN 规划器** Le`pyhop`- Je suis là.`SHOP3`, ou pour mettre en œuvre des stratégies spécifiques dans le domaine de la construction de soi-même.
- **ChatHTN** code de recherche; le modèle (symbolique + LLM fallback) est porté de manière propre à tout planificateur HTN.
  Le mot grec traduit par " le mot grec "**ChatHTN**研究代码;模式(符号 + LLM 回退)可干净地移植到任何HTN 规划器──
- **AlphaEvolve** Paper DeepMind; le modèle (ensemble + évaluateur) est reproduisable. OpenEvolve et autres fourches open source similaires sont en train d'émerger.
  Le mot grec traduit par " le mot grec "**AlphaEvolve**DeepMind 论文;模式(集群 + 评估器)可复现──OpenEvolve 和类似开源分支正在涌现──
- **Agent frameworks** aucun navire de première classe HTN ou AlphaEvolve encore.
  Le mot grec traduit par " le mot grec "**Agent 框架** Actuellement, il n'existe pas de HTN ou d'AlphaEvolve intégré.

## Envoyez-le . Produit .

`outputs/skill-hybrid-planner.md`génère un échafaudage de planificateurs hybrides (HTN ou évolutionnaire) avec un rôle de MLL explicitement défini.

> `outputs/skill-hybrid-planner.md`Il est également possible de faire des recherches sur les différents types de produits.

## Les exercices

1. Prendre le plan de la ligne de transmission en mode rétro-traçage: lorsque le post-conditionnement d'un opérateur échoue à l'heure de fonctionnement, faire demi-tour et essayer la méthode suivante.
   Pour HTN 规划器添加回溯: lorsque les conditions de mise à jour de l'opérateur ont échoué lors de la mise en service, re滚并尝试下一个方法──
2. Ajouter un cache de méthode LLM à ChatHTN: lorsque le LLM décompose la tâche `T`dans le modèle de l'état `P`Retournez à la bibliothèque de méthodes à l'appel suivant.
   Pour le chatHTN 添加 LLM 方法缓存:当 LLM 在状态模式 `P`中分解任务 `T`时, stockage résultat──下次调用时先重新检查方法库──
3. Évoluer l'évaluateur de recherche évolutionnaire vers une suite de tests réelle. Évoluer une fonction de tri qui passe 20 cas de test; rapporter des générations à la convergence.
   Le système de recherche est un système de recherche qui est utilisé pour évaluer les résultats de tests.
4. Lisez les notes de conception de l'évaluateur d'AlphaEvolve. Concevez un évaluateur pour un domaine qui vous intéresse (optimisation de requête SQL, minimisation de la suite de tests, déploiement YAML).
   Pour les personnes intéressées, le projet de conception d'un évaluateur est un projet de conception de l'analyse de données.
5. Combiner: utiliser HTN pour décomposer une tâche composée en sous-tâches, puis utiliser la recherche évolutionnaire sur l'opérateur primitif de chaque sous-tâche. Où brille-t-il, où est-il sur-ingénierie?
   Le système de recherche est basé sur le système de recherche de l'opérateur de chaque tâche.

## Les termes clés

| Term | What people say | What it actually means |
|------|-----------------|-----------------------|
| 术语 | 通俗说法 | 实际含义 |
| HTN | "Hierarchical planner" / "分层规划器" | Task decomposition with operators, preconditions, effects / 带操作符、前置条件、效果的任务分解 |
| Method | "Decomposition rule" / "分解规则" | Way to break a compound task into subtasks / 将复合任务分解为子任务的方式 |
| Operator | "Primitive action" / "原始动作" | Concrete step with precondition and effect / 带前置条件和效果的具体步骤 |
| ChatHTN | "LLM + HTN" / "LLM + HTN" | Symbolic planner asks LLM when no method matches / 符号规划器在没有方法匹配时询问 LLM |
| AlphaEvolve | "Evolutionary code search" / "进化代码搜索" | Ensemble LLMs mutate code; deterministic evaluator selects / LLM 集群变异代码；确定性评估器选择 |
| Fitness function | "Evaluator" / "评估器" | Deterministic, machine-checkable score over outputs / 输出上的确定性、机器可检查分数 |
| Online method learning | "Cached LLM decomposition" / "缓存的 LLM 分解" | Store + generalize LLM plans to cut query cost / 存储并泛化 LLM 计划以降低查询成本 |

## Encore une lecture

- [Gopalakrishnan et al., ChatHTN (arXiv:2505.11814)](https://arxiv.org/abs/2505.11814) symbolique + planificateur hybride LLM
  Le texte de la lettre de l'auteur est écrit en français.
- [Novikov et al., AlphaEvolve (arXiv:2506.13131)](https://arxiv.org/abs/2506.13131) recherche de code évolutif avec des mutations de LLM
  Le thème de l'éducation à la langue française est "AlphaEvolve" et "AlphaEvolve" est "AlphaEvolve" et "AlphaEvolve" est "AlphaEvolve" et "AlphaEvolve" sont "AlphaEvolve" et "AlphaEvolve" sont des thèmes de l'éducation à la langue française.
- [Anthropic, Building Effective Agents](https://www.anthropic.com/research/building-effective-agents) quand trouver un planificateur par rapport à une boucle simple
  Traduction anglaise:Anthropique                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                     
