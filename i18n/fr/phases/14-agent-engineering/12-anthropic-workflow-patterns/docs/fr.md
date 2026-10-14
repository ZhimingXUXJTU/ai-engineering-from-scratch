# Les modèles de flux de travail de l'anthropique: simple sur complexe

> Schluntz et Zhang (Anthropic, Déc 2024) distinguent les flux de travail (pistes prédéfinies) des agents (utilisation dynamique des outils).

> **【中文解读】**Anthropic a distingué entre les flux de travail (en anglais) et les modes d'utilisation des outils mobiles (en anglais) en décembre 2024.

**Type:** Learn + Build | **类型:** 学习 + 构建
**Languages:** Python (stdlib) | **语言:** Python (标准库)
**Prerequisites:** Phase 14 · 01 (Agent Loop) | **前置知识:** Phase 14 · 01 (Agent 循环)
**Time:** ~60 minutes | **时间:** ~60 分钟

## Objectifs d'apprentissage

- Nommez les cinq modèles de flux de travail d'Anthropic: chaîne rapide, routage, parallélisation, orchestrateur-travailleur, évaluateur-optimisateur.
  Le modèle de travail de l'anthropie est le suivant:
- Expliquez la différence entre les agents et les flux de travail et le coût de l'ingénierie de chacun.
  Expliquer les différences entre l'agent et le flux de travail et leurs coûts de construction.
- Identifier le moment où choisir un flux de travail au lieu d'un agent (et vice versa).
  Le nom de l'agent est traduit en français par "agent" ou "agent".
- Implémenter les cinq modèles dans le stdlib contre un LLM scénarisé.
  Le texte de la loi est écrit en français.

## Le problème , l' introduction du problème

Les équipes recherchent des cadres multi-agents pour les problèmes qui nécessitent un appel à une seule fonction. Le coût est réel: les cadres ajoutent des couches qui obscurcissent les demandes, cachent le flux de contrôle et invitent la complexité prématurée.

> Le prix est réel: le cadre ajoute une idée floue, un flux de contrôle caché, une couche de complexité précoce.

> **【中文解读】**Anthropic a publié en décembre 2024  Construction Effective Agents définit quatre modes de travail: 1) Chaîne rapide 串行步骤链; 2) Routing 条件分支; 3) Parallélisation 并行扇出扇入; 4) Orchestrator-Workers 编排器分配子任务──

> **【拓展：Anthropic 的工作流模式分类已成为 Agent 工程的事实标准】**LangGraph utilise l'état-image pour réaliser ces modèles, OpenAI Agents SDK utilise les mains pour réaliser le routage et l'édition, CrewAI utilise les équipes pour réaliser l'équipage.

>  **【前置】**Il faut d'abord passer la phase 14·01 (Agent Loop) 本节就是它的"模式提炼"──还需要看过阶段 14·02 (ReWOO) ‧阶段 14·05 (Self-Refine) ‧阶段 14·10 (Skills) 五种工作流模式都对应前面学过的具体技术,没基础会感觉空洞──

## Le concept de base.

### Flux de travail par rapport aux agents

- **Workflow.**Les LLM et les outils sont orchestrés par des chemins de code prédéfinis.
  Le mot grec traduit par " le mot grec "**工作流。**通過预定义代码路径编排的 LLM 和工具──工程师拥有图──
- **Agent.**Les LLM dirigent dynamiquement leurs propres outils et font leurs propres pas.
  Le mot grec traduit par " le mot grec "**Agent。**Le programme de formation en sciences de l'enseignement supérieur est un outil de formation en sciences de l'enseignement supérieur.

Les deux ont leur place. Les flux de travail sont moins chers, plus rapides et plus faciles à déboguer. Les agents débloquent des problèmes sans fin, mais rendent les modes d'échec plus difficiles à raisonner.

>  **【类比】**Workflow vs Agent 像地铁 vs 自驾:地铁(workflow) route fixe、便宜、可靠, mais tu peux seulement aller à la station;自驾(agent)灵活、能去任何地方, mais可能迷路、烧油、出车祸──日常通勤选地铁(workflow),探索未知地区选自驾(agent)──新手最常见的错误是"所有任务都自驾"其实80% des tâches de production sont réalisées par le métro.

>  Tous deux ont leur place de travail                                                                                                                                                                                                                                                          

### Le LLM complémentaire

Fondation pour les cinq modèles: un LLM avec trois capacités câblées en  recherche (reprise), outils (actions), mémoire (persistance).

> Une licence de licence comporte trois compétences: recherche, recherche, outils, actions, mémoire, et tout autre type d'API.

### Les cinq modèles

1. **Prompt chaining.**La sortie de l'appel 1 est l'entrée de l'appel 2. Utilisez-la lorsqu'une tâche a une décomposition linéaire propre. Ports programmatiques optionnels entre les étapes.
   Le mot grec traduit par " le mot grec "**提示链。**调用 1 的输出是调用 2 的输入.
2. **Routing.**Un classifiateur LLM choisit le LLM ou l'outil en aval à invoquer. Utilisez lorsque des entrées catégoriquement différentes nécessitent une manipulation différente (support de niveau 1 vs remboursement vs bug vs ventes).
   Le mot grec traduit par " le mot grec "**路由。**Les différents types d'entrées doivent être traités différemment.
3. **Parallelization.**Exécuter N LLM appels simultanément, résultats agrégés. Deux formes: sectionnement (couches différentes) et vote (même prompt, N coure, majorité/synthèse).
   Le mot grec traduit par " le mot grec "**并行化。**Il s'agit d'une série de projets de recherche et de développement qui ont été réalisés par des chercheurs en sciences de l'information et de l'information.
4. **Orchestrator-workers.**Un LLM orchestrateur décide dynamiquement quels travailleurs (également LLM) exécuter et synthétise leur production.
   Le mot grec traduit par " le mot grec "**编排器-工作者。**L'équipe de gestion de la gestion de la gestion des ressources humaines (LPC) décide de la gestion des ressources humaines (LPC) et de la gestion des ressources humaines (LPC).
5. **Evaluator-optimizer.**Un LLM propose une réponse, un autre LLM l'évalue. Iterer jusqu'à ce que l'évaluateur passe.
   Le mot grec traduit par " le mot grec "**评估器-优化器。**Une LLM  propose une réponse, une autre LLM  évaluer la.

### Où les flux de travail battent les agents

> 工作流优于 Agent's scène:

- **Predictable tasks.**Si vous pouvez énumérer les étapes, vous devriez.
  Le mot grec traduit par " le mot grec "**可预测任务。**Si tu peux faire des étapes, tu devrais faire des étapes.
- **Cost-bound tasks.**Les flux de travail ont un nombre limité d'étapes; les agents peuvent être en spirale.
  Le mot grec traduit par " le mot grec "**成本受限任务。**Le flux de travail est limité; l'agent peut être en panne de contrôle.
- **Compliance-bound tasks.**Les auditeurs veulent lire le graphique, pas le déduire des trajectoires.
  Le mot grec traduit par " le mot grec "**合规受限任务。**L'auditeur veut lire le tableau, plutôt que le trajet.

### Où les agents battent les flux de travail

> Agents 优于工作流的场景:

- **Open-ended research.**Quand la prochaine étape dépend de ce que la dernière étape a rendu.
  Le mot grec traduit par " le mot grec "**开放式研究。**Quand la prochaine étape détermine ce que la prochaine étape a rendu.
- **Variable-length tasks.**Minutes à heures de travail où le nombre d'étapes est inconnu.
  Le mot grec traduit par " le mot grec "**可变长度任务。**Quelques minutes à quelques heures de travail, nombre d'étapes inconnues.
- **Novel domains.**Si vous ne connaissez pas encore le bon flux de travail, explorez d'abord, codifiez plus tard.
  Le mot grec traduit par " le mot grec "**新领域。**Quand tu ne sais pas ce que tu veux faire, tu dois commencer par explorer.

### Le compagnon de l'ingénierie contextuelle

" Ingénierie contextuelle efficace pour les agents d'IA " (Anthropic 2025) formalite la discipline adjacente: la fenêtre 200k est un budget, pas un conteneur. Qu'est-ce qu'il faut inclure, quand compacter, quand laisser le contexte croître.

> "AI Agent's有效上下文工程" (Anthropic 2025) a formalisé la science adjacente: la fenêtre est un budget et non un récipient.

## Construisez-le en main

> ️ **【易错点】**Le plus souvent, les gens se mettent à la recherche de l'intelligence.**后果**Le programme de programmation est un programme de programmation de programmation de programmation de programmation de programmation de programmation de programmation de programmation de programmation de programmation de programmation de programmation de programmation de programmation de programmation de programmation de programmation de programmation de programmation de programmation de programmation de programmation de programmation de programmation de programmation de programmation de programmation de programmation de programmation de programmation de programmation de programmation de programmation de programmation de programmation de programmation de programmation de programmation de programmation de programmation de programmation de programmation de programmation de programmation de programmation de programmation de programmation de programmation de programmation de programmation de programmation de programmation de programmation de programmation de programmation de programmation de programmation de programmation de programmation de programmation de programmation de programmation de programmation de programmation de programmation de programmation de programmation de programmation de programmation de programmation de programmation de programmation de programmation de programmation de programmation de programmation de programmation de programmation de programmation de programmation de programmation de programmation de programmation de programmation de programmation de programmation de programmation de programmation de programmation de programmation de programmation de programmation de programmation de programmation de programmation de programmation de programmation de programmation de programmation de programmation de programmation de programmation de programmation de programmation de programmation de programmation de programmation de programmation de programmation de programmation de programmation de programmation de programmation de programmation de programmation de programmation de programmation de programmation de programmation de programmation de programmation de programmation de programmation de programmation de programmation de programmation de programmation de programmation de programmation de programmation de programmation de programmation de programmation de programmation de programmation de programmation de programmation de programmation de programmation de programmation de programmation de programmation de programmation de programmation de programmation de programmation de programmation de programmation de programmation de programmation de programmation de programmation de programmation de programmation de programmation de programmation de programmation de programmation de programmation de programmation de programmation de programmation de programmation de programmation de programmation de programmation de programmation de**先直接 API 调用，加复杂度只为换取能力**" Une chaîne de prompt avec une fonction Python ordinaire est suffisante, pas besoin de cadre".""**一行修复**: évaluer si chaque tâche peut être réalisée avec un cadre différent.
```figure
workflow-chain
```

## Faites-le

`code/main.py`Il met en œuvre les cinq modèles de flux de travail par rapport à un `ScriptedLLM`- Le numéro de la liste:

> `code/main.py` à l' égard `ScriptedLLM`¢ réalisé tous les cinq modes de travail:

- `prompt_chain(input, steps)` séquentielle.
- `route(input, classifier, handlers)` classification + expédition.
- `parallel_vote(prompt, n, aggregator)` N couronne, agrégée.
- `orchestrator_workers(task, workers)`L'orchestre choisit les ouvriers.
- `evaluator_optimizer(task, proposer, evaluator, max_iter)` boucle jusqu'à la passée.

- Je vais le faire.

> 运行:

```
python3 code/main.py
```

Chaque modèle imprime sa trace. Le total des lignes de code par modèle est de ~10-15; le coût d'un cadre est mesuré en milliers.

> Chaque modèle imprime ses traces. Chaque modèle a environ 10 à 15 lignes de code.

> 🤔 **【困惑】**Q: 既然 "workflow  priorit" est alors clair, pourquoi LangGraph、CrewAI ces cadres sont aussi brûlés ?**持久化、可观测性、人在回路、监控**Ces "运维级" fonctionnement. Vous utilisez 30 行 stdlib 写的提示链 运挂了, vous avez vous-même pensé comment récupérer du 17ème étape; vous utilisez LangGraph 写的,框架免费给您检查点.

## Utilisez-le avec le cadre de réalisation

- L'API directe appelle pour la plupart des tâches.
  La plupart des tâches utilisent une API directe.
- Framework seulement lorsque le modèle a vraiment besoin d'un état durable (LangGraph), de la concurrence acteur-modèle (AutoGen v0.4), ou de la modélisation de rôle (CrewAI).
  Le modèle est utilisé pour la création de nouveaux modèles.
- Recherchez le SDK de Claude Agent quand vous voulez la forme du harnais Claude Code sans le reconstruire.
  Le code Claude est un code de code de code de Claude.

## Envoyez-le . Produit .

`outputs/skill-workflow-picker.md`choisit le bon modèle pour une description de tâche donnée, y compris la justification de la décision et le chemin du réfacteur vers un agent si les flux de travail ne sont pas suffisants.

> `outputs/skill-workflow-picker.md`Pour déterminer la tâche, décrire le mode de choix correct, y compris les raisons de la décision et la façon dont l'agent est reconstitué en cas de manque de flux de travail.

## Les exercices

1. La mise en œuvre de l'itinéraire avec un seuil de confiance. En dessous du seuil -> escalade à humain. Où se trouve le seuil pour un cas d'utilisation de support de niveau 1 ?
   En français, la valeur de l'équipement est de type étalon.
2. Ajoutez un temps de pause à `parallel_vote`Comment on fait pour compenser les voix manquantes ?
   Pour le français`parallel_vote`Comment faire quand un appel est suspendu ? Comment rassembler le vote manquant ?
3. Tournez-vous`evaluator_optimizer`En tant que bandit, conservez les deux premières sorties en plusieurs iterations afin qu'un bon résultat tardif ne soit pas écrasé par un mauvais tardif.
   Le premier est le premier.`evaluator_optimizer`变成 bandit:跨代保留 top-2 输出, éviter la bonne fin de la période suivante 被后期坏结果覆盖──
4. Combinez la chaîne de prompt avec le routage: un routeur choisit une des trois chaînes. Mesurez le coût des jetons par rapport à une seule alternative à grande demande.
   Le mot "composition de la proposition" est traduit par "composition de la proposition".
5. Choisissez une fonction de production, dessinez le graphique du flux de travail, comptez les étapes.
   Choisir une fonction de production, dessiner un travail, calculer des étapes, faire un agent, c'est mieux ?

## Les termes clés

| Term | What people say | What it actually means |
|------|-----------------|-----------------------|
| 术语 | 通俗说法 | 实际含义 |
| Workflow | "Predefined flow" / "预定义流程" | Engineer-owned graph of LLM and tool calls / 工程师拥有的 LLM 和工具调用图 |
| Agent | "Autonomous AI" / "自主 AI" | Model-owned graph; dynamic tool direction / 模型拥有的图；动态工具指导 |
| Augmented LLM | "LLM with tools" / "带工具的 LLM" | LLM + search + tools + memory; the atomic unit / LLM + 搜索 + 工具 + 记忆；原子单元 |
| Prompt chaining | "Sequential calls" / "串行调用" | Output of call N is input to call N+1 / 调用 N 的输出是调用 N+1 的输入 |
| Routing | "Classifier dispatch" / "分类分派" | Pick which chain/model handles the input / 选择哪个链/模型处理输入 |
| Parallelization | "Fan out" / "扇出" | N concurrent calls; aggregate by sectioning or voting / N 个并发调用；按分段或投票聚合 |
| Orchestrator-workers | "Dispatcher agent" / "分派 Agent" | Orchestrator LLM picks specialist LLMs dynamically / 编排器 LLM 动态选择专家 LLM |
| Evaluator-optimizer | "Proposer + judge" / "提议者 + 评判者" | Iterate until evaluator passes; Self-Refine generalized / 迭代直到评估器通过；Self-Refine 的泛化 |

## Encore une lecture

- [Anthropic, Building Effective Agents (Dec 2024)](https://www.anthropic.com/research/building-effective-agents) les cinq modèles de flux de travail
  Article suivant: "A propos de la création d'un agent efficace"
- [Anthropic, Effective context engineering for AI agents](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents) la discipline du compagnon
  En anglais, le thème de l'artisanat est "Agent d'intelligence artificielle".
- [LangGraph overview](https://docs.langchain.com/oss/python/langgraph/overview) lorsque les graphiques d'état gagnent leur coût
  Le longgraphe est un tableau de l'état du pays.
- [OpenAI Agents SDK](https://openai.github.io/openai-agents-python/) le modèle des ouvriers-orchestre, produit
  Le code de gestion de la gestion des ressources humaines est le code de gestion des ressources humaines.
