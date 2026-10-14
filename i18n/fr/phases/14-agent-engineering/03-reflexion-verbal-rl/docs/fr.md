# Réflexion: Apprentissage par le renforcement verbal

> La RL basée sur les gradients a besoin de milliers d'essais et d'un graphiteur pour corriger un mode défaillance. Reflexion (Shinn et coll., NeurIPS 2023) le fait en langage naturel: après chaque essai raté, l'agent écrit une réflexion, la stocke dans la mémoire épisodique et conditionne le prochain essai sur cette mémoire. C'est le modèle derrière le calcul du temps de sommeil de Letta, les apprentissages de Claude Code sur CLAUDE.md et la règle d'apprentissage pro-flux de travail.

> **【中文解读】**基于梯度的RL 需要数千次试验和GPU集群──Réflexion avec le langage naturel pour réaliser l'auto-amélioration: chaque fois que l'agent échoue, il écrit un passage de réflexion dans la mémoire de l'événement, la prochaine fois qu'il essaie de se référer à ces mémoires── c'est exactement ce qui est derrière le calcul du sommeil de Letta、Claude Code de CLAUDE.md mécanisme d'apprentissage──

> **【拓展：Reflexion → Claude Code 的自我学习】**Le mécanisme de Claude Code CLAUDE.md est en fait une variante de Réflexion.

>  **【前置】**本节依赖:Phase 14·01(Agent Loop)你必须已经能跑通一个 ReAct 循环,因为 Reflexion's Actor 内部就是一个 ReAct loop;以及Phase 14·02(ReWOO)理解"试验/轨迹"的概念──如果你分不清"一次试验"和"一个步骤",先回去补补 ReAct──

**Type:** Build | **类型:** 构建
**Languages:** Python (stdlib) | **语言:** Python (标准库)
**Prerequisites:** Phase 14 · 01 (Agent Loop), Phase 14 · 02 (ReWOO) | **前置知识:** Phase 14 · 01 (Agent 循环), Phase 14 · 02 (ReWOO)
**Time:** ~60 minutes | **时间:** ~60 分钟

## Objectifs d'apprentissage

- Nombre des trois composantes de Réflexion (Acteur, Évaluateur, Autoreflex) et le rôle de la mémoire épisodique.
  Le rôle de l'acteur, de l'évaluateur et du réflecteur personnel
- Implémenter une boucle de réflexion stdlib avec évaluateur binaire, tampon de réflexion et nouvelles tentatives de réécriture.
  Le cycle de réflexion, contenant un évaluateur à deux niveaux, est utilisé pour réaliser la réflexion.
- Choisissez entre des sources de rétroaction scalaires, heuristiques et auto-évaluées pour une tâche donnée.
  Pour une tâche déterminée, choisir un échantillon, ou se faire évaluer.
- Expliquez pourquoi le renforcement verbal capture des erreurs que la RL basée sur le gradient aurait besoin de milliers d'essais pour corriger.
  Expliquer pourquoi la langue forte peut capturer des RL basées sur des échelles. Il faut des milliers d'essais pour corriger les erreurs.

## Le problème , l' introduction du problème

Un agent échoue à une tâche. Dans la RL standard, vous pourriez effectuer des milliers d'essais supplémentaires, calculer des gradients, mettre à jour des poids.

> L'agent a échoué à une tâche. Dans la norme RL, vous devez effectuer des milliers de fois plus d'essais, de calcul de la échelle, de mise à jour du poids, de coût, de lenteur, et la plupart des agents de production n'ont pas de budget d'entraînement pour chaque échec.

La réflexion (Shinn et coll., arXiv:2303.11366) pose une autre question: et si l'agent pensait simplement à pourquoi il a échoué et essayait à nouveau avec cette pensée dans son prompt? Pas de mises à jour de poids. Pas de gradient.

> Réflexion ((Shinn et d'autres, arXiv:2303.11366) pose une question différente: si l'agent  pense simplement aux causes de l'échec, puis rejoint cette idée dans la prochaine tentative de suggestion?

Le résultat: sur ALFWorld, il bat ReAct et d'autres lignes de base non finement réglées. sur HotpotQA, il s'améliore par rapport à ReAct. sur la génération de code (HumanEval / MBPP) il met à jour l'état de l'art à l'époque. Tout cela sans un seul pas de gradient.

> 结果: dans ALFWorld 上它击败了 ReAct 和其他非微调基线. Dans HotpotQA 上它超越了 ReAct. Dans la génération de codes (HumanEval/MBPP) 上它达到当时的最佳水平.

## Le concept de base.

### Les trois composantes

```
Actor         : generates a trajectory (ReAct-style loop)     # 执行器：生成行动轨迹
Evaluator     : scores the trajectory — binary, heuristic, or self-eval  # 评估器：评分
Self-Reflector: writes a natural-language reflection on the failure      # 自我反思器：写反思
```

Plus une structure de données:

```
Episodic memory: list of prior reflections, prepended to the next trial's prompt  # 情景记忆
```

Un essai est effectué par l'Acteur. L'évaluateur le note. Si le score est faible, l'Auto-Reflecteur produit une réflexion ("J'ai choisi l'outil incorrect parce que j'ai mal lu la question comme posant une question sur X quand il demandait sur Y"). La réflexion entre dans la mémoire épisodique.

>  **【类比】**Réflexion 像考试做错题后的"错题本"机制:你做错一道题(Actor 失败)→ 拿到对错信号(Evaluator 评分)→ 写下"我为什么错了"(Self-Reflector 写反思)→ 下次考前翻错题本(情景记忆前置到提示)。 下次重复同类题,错的概率就低了──关键是错题本(反思用自然语言写,不需要重训模型权──

> Une fois, un élève a été interrogé sur un sujet qui lui a été donné par un élève. Il a été interrogé sur un sujet qui lui a été donné par un élève.

### Trois types d'évaluateurs

1. **Scalar** un signal binaire externe. ALFWorld réussit ou échoue. Tests HumanEval réussissent ou échouent.
   Le mot grec traduit par " le mot grec "**标量** Externe secondaire signal。 ALFWorld succès ou défaite。HumanEval 测试通过或不通过──最简单,信号最强──
2. **Heuristic** signatures de défaillance prédéfinies. "Si l'agent a produit la même action deux fois de suite, marquez comme coincé". "Si la trajectoire dépasse 50 étapes, marquez comme inefficace".
   Le mot grec traduit par " le mot grec "**启发式**预定义的失败签名──"si l'agent 连续两次产生相同行动,标记为卡住──""si la trajectoire dépasse 50 étapes,标记为低效──"
3. **Self-evaluated** le LLM marque sa propre trajectoire. nécessaire lorsqu'aucune vérité fondée n'est disponible. signal plus faible; bien associé à la vérification fondée sur des outils (leçon 05  CRITIC).
   Le mot grec traduit par " le mot grec "**自评估**LLM à son propre parcours 

Le modèle par défaut de 2026 est un mélange: scalaire quand il est disponible, auto-égale quand il n'est pas, heuristique comme rails de sécurité.

> ️ **【易错点】**Trois types d'évaluateurs sont en train de se poser un gros problème: dans la création de rédactions de " sans réponse standard " sur les tâches de l'évaluateur à échelle dure, il continuera à générer des " signaux de défaillance "→ Agent 拼命反思 → Mais l'esprit lui-même n'a pas de sens → 浪费 token jusqu'à ce qu'il ait épuisé son budget。**后果**: cycle de transformation de l'argent**一行修复**Il est également possible de détecter les défaillances de l'équipe de formation de la formation professionnelle.

> La pratique standard de 2026 est l'utilisation mixte: avec des étiquettes, avec des étiquettes, sans étiquettes, avec des étiquettes.

### Pourquoi cela généralise-t-il

La réflexion n'est pas un nouvel algorithme mais un modèle nommé.

> La réflexion est plutôt un nouveau algorithme, pas comme un modèle de nommage.

- Letta's sleep-time computation (leçon 08): un agent séparé réfléchit sur les conversations passées et écrit aux blocs de mémoire.
  Letta's sleep-time computation (Lecture 8) est un agent indépendant qui réfléchit à son passé et écrit dans son cœur.
- Le code de Claude `CLAUDE.md`/ "sauvage de la mémoire": réflexions capturées en tant qu'apprentissage, pré-pendées pour les futures séances.
  Le code de Claude`CLAUDE.md`/"conserver les souvenirs" mode: le réflexion est capturée pour l'expérience d'apprentissage, préposée à la réunion future.
- Les flux de travail pro`/learn-rule`commandes: corrections prises en tant que règles explicites.
  Le travail de la société`/learn-rule`命令: recti正被捕为显式规则──
- Les nœuds de réflexion de LangGraph: un nœud qui note la sortie et les routes pour les affiner si nécessaire.
  Le langgraphe de l'écriture est un langgraphe de l'écriture de l'écriture.

Tout cela découle du même point de vue: le langage naturel est un moyen suffisamment riche pour transporter "ce que j'ai appris de l'échec" entre les deux sessions.

> Elles sont toutes issues du même concept: le langage naturel est un moyen suffisamment riche pour transmettre "ce que j'ai appris de l'échec" entre les deux.

> **【拓展：Reflexion → 生产环境的自我修复】**几乎所有生产环境的"自我修复"Agent 都使用 Reflexion 变体:Letta's sleep-time computation 异步反思、Claude Code的CLAUDE.md 存储学习经验、Langgraph的反思节点──核心洞察相同:自然语言足够承载"从失败中学到了什么"──

### Quand ça marche et quand ça ne marche pas

La réflexion fonctionne lorsque:

> Réflexion sur les situations suivantes:

- Il y a un signal de défaillance clair (faillance des tests, erreur de l'outil, mauvaise réponse).
  Il est également connu pour avoir été un échec de test.
- La classe de tâches est reproduisable (le même type de question peut être posé à nouveau).
  Le même type de question peut être posé à nouveau.
- La réflexion a de la place pour améliorer la trajectoire (budget d'action suffisant).
  Le projet de loi de la Commission européenne sur les droits de l'homme (CEDEAO) a été adopté par le Conseil européen de l'environnement (CEDEAO) en juin 2014.

La réflexion ne peut pas aider si:

> Réflexion dans les situations suivantes:

- L'agent réussit déjà à la première tentative.
  Le premier succès est le succès.
- L'échec est externe (réseau en panne, outil cassé)  la réflexion sur "réseau était en panne" n'aide pas les futurs exécutions.
  Le succès est une rupture de réseau extérieure.
- La réflexion se transforme en superstition  en stockant un récit sur une course à pied unique.
  Le récit d'une relation qui a été violée par une relation instable.

2026: dépôt: pourriture de la mémoire. Les réflexions s'accumulent; certaines sont obsolètes ou fausses; les ré-exécutions deviennent plus lentes à mesure que le tampon épisodique augmente.

> 🤔 **【困惑】**Q: Réflexion 真的能" équivaut à "RL 吗?RL 改是模型权重,Reflexion 改只快,机制完全不同。 A: 不能等价──论文标题"Verbal RL"是修辞而非数学等价──Reflexion 优势是**样本效率极高**Il faut 3 à 5 fois réfléchir pour réparer un défaut, et RL nécessite des milliers de renouvellements.**反思不会持久**Pour le modèle, chaque nouvelle réunion est un sujet de réflexion.

> La réaction de la population à la réaction de la population à la réaction de la population à la réaction de la population à la réaction de la population à la réaction de la réaction de la population à la réaction de la réaction de la population à la réaction de la réaction de la population à la réaction de la réaction de la population à la réaction de la réaction de la population à la réaction de la réaction de la population à la réaction de la réaction de la population à la réaction de la réaction de la réaction de la population à la réaction de la réaction de la réaction de la population à la réaction de la réaction de la réaction de la population à la réaction de la réaction de la réaction de la réaction de la population à la réaction de la réaction de la réaction de la réaction de la réaction de la réaction de la réaction de la réaction de la réaction de la réaction de la réaction de la réaction de la réaction de la réaction de la réaction de la réaction de la réaction de la réaction de la réaction de la réaction de la réaction de la réaction de la réaction de la réaction de la réaction de la réaction de la réaction de la réaction de la réaction de la réaction de la réaction de la réaction de la réaction de la réaction de la réaction de la réaction de la réaction de la réaction de la réaction de la réaction de la réaction de la réaction de la réaction de la réaction de la réaction de la réaction de la réaction de la réaction de la réaction de la réaction de la réaction de la réaction de la réaction de la réaction de la réaction de la réaction de la réaction de la réaction de la réaction de la réaction de la réaction de la réaction de la réaction de la réaction de la réaction de la réaction de la réaction de la réaction de la réaction de la réaction de la réaction de la réaction de la réaction de la réaction de la réaction de la réaction de la réaction de la réaction de la réaction de la réaction de la réaction de la réaction de la réaction de la ré

## Construisez-le et mettez-le en œuvre.
```figure
react-trace
```

## Faites-le

`code/main.py`Il met en œuvre Reflexion sur un puzzle de jouet: produire une liste de 3 éléments qui s'ajoute à une cible. L'acteur émet des listes de candidats; l'évaluateur vérifie la somme; l'auto-réflecteur écrit une ligne sur ce qui est mal passé. La réflexion va dans la mémoire épisodique pour le prochain essai.

> `code/main.py`Réflexion: générer une liste de 3 éléments et de valeur cible. Acteur: émettre une liste de candidats. Évaluateur: examiner le résumé. Autoreflecteur: écrire une ligne sur le diagnostic de ce qui a été émis. Réflexion: générer une liste de 3 éléments et de la valeur cible.

Components:

> 组件:

- `Actor` une politique écrite qui s'améliore lorsqu'elle voit des réflexions.
  Le mot grec traduit par " le mot grec "`Actor` voir le réflexe                                                                                                                                                                                                                                                            
- `Evaluator.binary()` Passer ou échouer sur la somme cible.
  Le mot grec traduit par " le mot grec "`Evaluator.binary()` à travers le succès de la décision de l'objectif total.
- `SelfReflector` génère un diagnostic à une seule ligne de l'échec.
  Le mot grec traduit par " le mot grec "`SelfReflector`生成一行失败诊断──
- `EpisodicMemory` une liste limitée avec la sémantique TTL.
  Le mot grec traduit par " le mot grec "`EpisodicMemory`带 TTL 语义的有界列表──

- Je vais le faire.

> 运行:

```
python3 code/main.py
```

La trace montre trois essais. L'essai 1 échoue, une réflexion est stockée, l'essai 2 voit le reflet et s'améliore mais échoue toujours, l'essai 3 réussit.

> 轨迹显示三次试验──试验1 失败,储反思,试验2 看到反思并改进但仍失败,试验3 成功──与基线运行(无反思) par rapport à它停留在试验1的答案──

## Utilisez-le avec le cadre de réalisation

LangGraph envoie la réflexion comme un modèle de nœud.`/memory`Les commandes et les flux de travail pro`/learn-rule`Letta's compute de temps de sommeil exécute l'auto-réflecteur en temps d'arrêt afin que l'agent principal reste lié à la latence. OpenAI Agents SDK ne délivre pas directement la réflexion; vous le construisez avec une garde personnalisée qui rejette les trajectoires par score et une mémoire`Session`qui survit à travers les courants.

> LangGraph va réfléchir comme un modèle de point de fourniture de Claude Code `/memory`命令和 pro-workflow `/learn-rule`L'équipe de gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion`Session`Pour le construire.

## Envoyez-le . Produit .

`outputs/skill-reflexion-buffer.md`crée et maintient un tampon épisodique avec capture de réflexion, TTL et déduplication.

> `outputs/skill-reflexion-buffer.md`创建并维护带反思捕获、TTL 和去重的情景缓冲区──给定任务类别和失败, elle génère un passage qui contribue réellement à la réflexion de l'expérience suivante, et non pas un "tout petit cœur")──

## Les exercices

1. Passer de l'évaluation binaire à l'évaluation scalaire qui renvoie une mesure de distance (à quelle distance de la cible).
   Le système d'évaluation de la quantité de données est-il plus rapide ?
2. Ajoutez à la réflexion un TTL de 10 essais.
   En français, la réflexion est plus ou moins bénéfique.
3. Appliquez l'évaluation heuristique: marquez l'essai comme bloqué si la même action se répète.
   Comment cela interagit-il avec le réflexeur-auto ?
4. Exécutez Reflexion avec un Acteur adversaire qui ignore les réflexions.
   Le moins nécessaire est de savoir comment faire pour forcer l'acteur à prendre conscience de la réaction.
5. Lisez la section 4 du document Reflexion sur AlfWorld.
   Le réflexe de l'article 4 sur le contenu d'AlfWorld.

## Les termes clés

| Term | What people say | What it actually means |
|------|-----------------|-----------------------|
| 术语 | 通俗说法 | 实际含义 |
| Reflexion | "Self-correction" / "自我纠错" | Shinn et al. 2023 — Actor, Evaluator, Self-Reflector plus episodic memory / Shinn 等人 2023——Actor、Evaluator、Self-Reflector 加情景记忆 |
| Verbal reinforcement | "Learning without gradients" / "无梯度学习" | Natural-language reflection prepended to the next trial's prompt / 自然语言反思前置到下一次试验的提示 |
| Episodic memory | "Per-task reflections" / "按任务的反思" | Bounded buffer of prior reflections for one task class / 一个任务类别的先前反思有界缓冲区 |
| Scalar evaluator | "Binary success signal" / "二元成功信号" | Pass/fail or numeric score from ground truth / 来自真值的通过/失败或数值评分 |
| Heuristic evaluator | "Pattern-based detector" / "基于模式的检测器" | Predefined failure signatures (e.g. stuck-loop, too-many-steps) / 预定义的失败签名（如卡住循环、步数过多） |
| Self-evaluator | "LLM-as-judge on own trace" / "LLM 评价自身轨迹" | Lower-signal fallback when no ground truth — pair with tool-grounded verification / 无真值时的低信号后备——与工具锚定验证配合 |
| Memory rot | "Stale reflections" / "过时反思" | Episodic buffer fills with obsolete entries; fix with compaction/TTL / 情景缓冲区填满过时条目；用压缩/TTL 修复 |
| Sleep-time reflection | "Async self-reflection" / "异步自我反思" | Run Self-Reflector off the hot path so primary agent stays fast / 在非关键路径上运行 Self-Reflector 使主 Agent 保持快速 |

## Encore une lecture

- [Shinn et al., Reflexion: Language Agents with Verbal Reinforcement Learning (arXiv:2303.11366)](https://arxiv.org/abs/2303.11366) le papier canonique
  Le réflexe est un élément clé de la réflexion.
- [Letta, Sleep-time Compute](https://www.letta.com/blog/sleep-time-compute) Réflexion asynchrone dans la production
  Letta 关于生产环境中异步反思的博客文章.
- [Anthropic, Effective context engineering for AI agents](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents) gérer le tampon épisodique dans le cadre du contexte
  Article suivant: "L'état de l'environnement dans le secteur de l'intelligence artificielle"
- [LangGraph overview](https://docs.langchain.com/oss/python/langgraph/overview) modèle de nœud de réflexion
  Le langage de la page est le langage de la page.
