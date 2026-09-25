# L'agent de codage autonome paysage (2026)

> Le taux de vérification de la banque SWE est passé de 4% à 80,9% en moins de trois ans. Le même Claude Sonnet 4.5 a obtenu 43,2% sur SWE-agent v1 et 59,8% sur Cline autonome  l'échafaudage autour du modèle compte maintenant autant que le modèle lui-même. OpenHands (anciennement OpenDevin) est la plateforme la plus active sous licence MIT et sa boucle CodeAct exécute des actions Python directement dans une boîte à sable au lieu d'appels à l'outil JSON. Les numéros de titre cachent un problème méthodologique: 161 des 500 tâches vérifiées SWE-bench nécessitent seulement un changement de ligne 12, et SWE-bench Pro (10 tâches de ligne +) se situe à 2359% pour les mêmes modèles frontaliers.

> **【中文解读】**SWE-bench Verified est la plateforme de licence MIT la plus active, dont le cycle CodeAct est d'exécuter directement dans la boîte Python 动作而不是 JSON 工具调调用.

> **【拓展：脚手架 > 模型】**La courbe de 2022-2026 indique que la capacité de l'agent à coder augmente à trois sources complexes: meilleur modèle de base, meilleur scripture (CodeAct, Réflexion, Cycle de vérificateur)  meilleur scripture (Verified, Débarrasse de bruit)  Les mêmes modèles diffèrent en nombre de points de base 16.6  Le modèle de base est composé, le cycle est le produit ‒ c'est pourquoi l'agent n'a pas la capacité de voir uniquement le classement des modèles ‒

**Type:** Learn | **类型:** 学习
**Languages:** Python (stdlib, CodeAct vs JSON tool-call comparison) | **语言:** Python（标准库，CodeAct vs JSON 工具调用对比）
**Prerequisites:** Phase 14 · 07 (Tool use), Phase 15 · 01 (Long-horizon agents) | **前置知识:** Phase 14 · 07（工具使用），Phase 15 · 01（长程 Agent）
**Time:** ~45 minutes | **时间:** ~45 分钟

>  **【前置】**Je vous invite à apprendre la première partie de la série: phase 14·07 (outils de préparation)  phase 14·30 (outils de préparation)  phase 15·01 (outils de préparation)  phase 15·01 (outils de préparation)  phase 15 (outils de préparation)  phase 14·07 (outils de préparation)  phase 14·30 (outils de préparation)  phase 15·01 (outils de préparation)  phase 15·01 (outils de préparation)  phase 15 (outils de préparation)  phase 14·07 (outils de préparation)  phase 14·30 (outils de préparation)  phase 14·30 (outils de préparation)  phase 15·01 (outils de préparation)  phase 15 (outils de préparation)  phase 15 (outils de préparation)  phase 14 (outils de préparation)  phase 14 (outils de préparation)  phase 14 (outils de préparation)  phase 14 (ouvrage)  phase 14 (ouvrage)  phase 14 (ouvrage) 
>  **【类比】**选编码 Agent = "选车" plutôt que "选发动机"。同一发动机(Claude Sonnet 4.5) installé sur différents véhicules(SWE-agent vs Cline) Speed Difference 16 个百分点。脚手架(检索层、规划器、沙箱、编辑-verify 循环) 才是产品,模型只是组件。所以不要只看模型排行榜,看"我的任务+我的脚手架"的端到端可靠性。
> ️ **【易错点】**Regarde le SWE-bench Verifié 分数选 Agent = 被基准骗了──500 个任务里 161 个只需要1-2 行修改(容易),看 SWE-bench Pro(10+ 行真实任务) 分数才有参考价值──修复:选 Agent 前用自己代码库的真实问题 测试,而不是看营销基准──

## Le problème , l' introduction du problème

> **【中文解读】**Le domaine de l'IA est l'un des domaines d'application les plus rapides de l'IA en 2025-2026 . Les principaux acteurs sont Claude Code, Cursor, GitHub Copilot, Devine, Windsurf, etc.

> **【拓展：coding agent landscape】**2026年编码 代理的竞争格局:(1) Claude CodeAnthropic's Autonomous Coding Agent, supporting 开发、Git 操作和终端命令执行;(2) Cursor基于 VS Code的 AI 编辑器,强调人机协作;(3) DevinCognition AI's Full Autonomous Coding Agent,可以独立完成开发任务;(4) Windsurf(原 Codeium) AI 优先 IDE──SWE-bench 上的表现是主要竞争指标──

La question correcte est: sur une répartition des tâches qui correspond à mon travail, avec l'échafaudage que je vais exécuter en production, quelle fiabilité de bout en bout obtiens-je?

> La question vraie est la suivante: dans la distribution des tâches correspondant à mon travail, en utilisant les cadres de code que je vais utiliser dans la production, que puis-je obtenir de la fiabilité de bout en bout ?

Entre 2022 et 2026, le champ a appris que l'échafaudage  la couche de récupération, le planificateur, la boîte à sable, la boucle de vérification de la modification, le format de rétroaction  est porteur de charge. Claude Sonnet 4.5 sur SWE-agent v1 a obtenu 43,2% sur SWE-bench Verified; le même modèle à l'intérieur de l'échafaudage autonome de Cline a obtenu 59,8%. 16.6 points de différence absolus, les mêmes poids. Le modèle de base est un composant; la boucle est le produit.

> En 2022, à 2026, le domaine de l'apprentissage des scripts a été testé à la fois par des planificateurs et des boîtes de sacs, et le cycle de vérification des éditions et des éditions a été réalisé à la fois par des experts et des experts.

> **【中文解读】**Ce chapitre présente le concept et la méthode de réalisation de l'agent d'IA. L'agent est un système autonome à action de la MLL, capable d'observer l'environnement, de penser, de prendre des décisions, d'exécuter des actions et de les faire boucler jusqu'à la fin de l'objectif.

Le problème du complément est que la saturation de référence cache les régressions.

> Le problème est le retour à la base et le retour à la cachette.

SWE-bench Verified est proche de saturation, et la queue facile à effectuer (161 des 500 tâches nécessitant ≤ 2 lignes) augmente les meilleurs scores. La qualité du monde réel est mieux mesurée sur des distributions comme SWE-bench Pro (10 + changements de lignes), où les mêmes leaders sont toujours assis à 2359%.

> SWE-bench Verifié 接近和,简单任务尾部(500 个任务中 161 个需要 ≤2 行) 拉高顶级分数──现实世界质量在SWE-bench Pro(10+ 行变更)等分布上测量更好,同领先者仍然只有23-59%──

## Le concept de base.

### SWE-bench, un paragraphe

SWE-bench (Jimenez et coll.) prend de vrais problèmes GitHub avec des correctifs de base et demande à un agent de produire un correctif qui permet de passer la suite de tests. SWE-bench Verified (OpenAI, 2024) est un sous-ensemble de 500 tâches géré par l'homme avec les tâches ambiguës et brisées supprimées. SWE-bench Pro est le successeur plus difficile  tâches nécessitant plus de 10 lignes de changement, où les agents frontaliers actuels sont à 2359%.

> SWE-bench (Jimenez et autres) a apporté des correctifs réels à la question GitHub, exigeant que l'agent  produise des correctifs qui permettent de faire passer des tests.

### Ce que la courbe 2022 → 2026 montre réellement

- **2022**: modèles de recherche à ~4% sur le banc SWE brut.
  Le mot grec traduit par " le mot grec "**2022**Le modèle de recherche est basé sur la banque SWE.
- **2024**: GPT-4 + échafaudage de style Devin à ~ 14%; agent SWE à ~ 12%.
  Le mot grec traduit par " le mot grec "**2024**:GPT-4 + Devin 式脚手架约 14%;SWE-agent 约 12%──
- **2025**: Claude 3.5/3.7 Sonnet à l'intérieur de Aider et agent SWE poussent dans la plage de 4055%.
  Le mot grec traduit par " le mot grec "**2025**Le sonnet en Aider et en SWE est de 40 à 55%.
- **2026**Le tableau de classement de l'Epoch AI suit en direct ce qui suit: Claude Sonnet 4.5 et les concurrents frontaliers à 7080%+ sur le banc SWE-Verified.
  Le mot grec traduit par " le mot grec "**2026**:Claude Sonnet 4.5 和前沿竞争者在SWE-bench Verified 上 70-80%+──Epoch AI's排名实时跟踪──

La pente provient de trois sources de composition: de meilleurs modèles de base, d'un meilleur échafaudage (CodeAct, réflexion, boucles de vérification) et de meilleures valeurs de référence (élimination du bruit vérifiée).

> Le taux de rebond provient de trois sources complexes: meilleur modèle de base, meilleur scripture, meilleur codeact, meilleur base de référence, meilleur bas de page, meilleur bas de page, meilleur bas de page, meilleur résultat, meilleur résultat, meilleur résultat, meilleur résultat, meilleur résultat, meilleur résultat, meilleur résultat, meilleur résultat, meilleur résultat, meilleur résultat, meilleur résultat, meilleur résultat, meilleur résultat, meilleur résultat, meilleur résultat, meilleur résultat, meilleur résultat, meilleur résultat, meilleur résultat, meilleur résultat, meilleur résultat, meilleur résultat, meilleur résultat, meilleur résultat, meilleur résultat, meilleur résultat, meilleur résultat, meilleur résultat, plus de résultat, plus de résultat.

### CodeAct contre JSON outil appelle .

OpenHands (All-Hands-AI, arXiv:2407.16741, anciennement OpenDevin) a pris un pari architectural spécifique: au lieu du modèle émettant des appels d'outil JSON que l'hôte décode et exécute, le modèle émet du code Python et un noyau de style Jupyter le gère dans une boîte à sable.

> OpenHands(All-Hands-AI,arXiv:2407.16741,前 OpenDevin) sous une architecture spécifique注: le modèle ne sort plus par le JSON 工具调用, mais par Python 代码, par Jupiter 风格内核在沙箱中运行──Agent peut être dans un mouvement dans un cycle de fichiers、chaîné de outils、 capturer ses propres anomalies──

Le compromis:

> 权衡:

- **JSON tool calls**: chaque action est une seule fois; facile à vérifier; compositionalité limitée; sûre par défaut car chaque appel passe par un validateur explicite.
  Le mot grec traduit par " le mot grec "**JSON 工具调用**: chaque opération est simple, facile à vérifier, la composition est limitée, la sécurité est définie par défaut, car chaque utilisation est effectuée par un vérificateur explicite.
- **CodeAct**: une action peut être un programme entier; composition; nécessite une boîte à sable durcie (OpenHands utilise l'isolement Docker); les modes de défaillance incluent tout ce que le temps de fonctionnement de la boîte à sable permet.
  Le mot grec traduit par " le mot grec "**CodeAct**Un mouvement peut être l'ensemble du processus; peut être assemblé; doit être renforcé dans la boîte à outils;

Les deux architectures sont en production. CodeAct est dominant dans les plateformes ouvertes (OpenHands, smolagents). Les appels à l'outil JSON restent dominants dans les services gérés (Agentes gérés par l'anthropie, Assistants OpenAI) où le fournisseur contrôle l'exécuteur.

> 两种架构都在生产中.CodeAct 在开放平台(OpenHands、smolagents) 主导.

### Des échafaudages dans le paysage de 2026

| Scaffold | License | Execution model | Notable property |
|---|---|---|---|
| 脚手架 | 许可 | 执行模型 | 显著属性 |
| OpenHands (OpenDevin) | MIT | CodeAct in Docker | Most active open platform; event-stream replayable |
| OpenHands（OpenDevin） | MIT | Docker 中 CodeAct | 最活跃开放平台；事件流可重放 |
| SWE-agent | MIT | Agent-Computer Interface (ACI) | First end-to-end SWE-bench scaffold |
| SWE-agent | MIT | Agent-计算机接口（ACI） | 首个端到端 SWE-bench 脚手架 |
| Aider | Apache-2 | edit-via-diff in local repo | Minimal scaffold, strong regression stability |
| Aider | Apache-2 | 本地仓库 edit-via-diff | 最小脚手架，强回归稳定性 |
| Cline | Apache-2 | VS Code agent with tool policy | Highest-scoring open scaffold on Sonnet 4.5 |
| Cline | Apache-2 | 带工具策略的 VS Code Agent | Sonnet 4.5 上得分最高的开放脚手架 |
| Devin (Cognition) | Proprietary | Managed VM + planner | First "AI software engineer" product category |
| Devin（Cognition） | 专有 | 管理 VM + 规划器 | 首个"AI 软件工程师"产品类别 |
| Claude Code | Proprietary | Permission modes + routines | Lesson 10 covers the agent loop in detail |
| Claude Code | 专有 | 权限模式 + 例程 | 第 10 课详细介绍 Agent 循环 |

### Pourquoi l'échafaudage domine ? Pourquoi le scandale ?

Une course de codage est une trajectoire à long horizon (leçon 1).

> 编码运行是长程轨迹 (第 1 课) ⋅可靠性跨步骤复合 (编码运行是长程轨迹) ⋅可靠性跨步骤复合 (编码运行是长程轨迹) ⋅可靠性跨步步步复合 (编码运行是长程轨迹) ⋅可靠性跨步步步复合 (编码运行是长程轨迹) ⋅可靠性跨步步步复合 (编码运行是长程轨迹) ⋅可靠性跨步步步复合 (编码运行是长程轨迹) ⋅可靠性跨步步步复合 (编码架买入分数) ⋅可靠性跨步步复合 (编码架买入分数) ⋅可靠性

1. **Retrieval**L'ACI de l'agent SWE, l'index de fichiers OpenHands et la carte référencée d'Aider attaquent tout cela.
   Le mot grec traduit par " le mot grec "**检索**Le référencement de l'agent de la SWE, l'index des fichiers OpenHands, la carte de référencement de l'aide, ont attaqué ce point.
2. **Verifier loop**: exécuter des tests, lire les traces de pile et réessayer est un delta de plus de 10 points sur le banc SWE.
   Le mot grec traduit par " le mot grec "**验证器循环**Le nombre de points de croissance est de 10 points.
3. **Failure containment**Le même modèle avec et sans boucle de vérification ressemble à deux produits différents.
   Le mot grec traduit par " le mot grec "**失败遏制**Le même modèle a et ne produit pas de cycle de vérification.

### La saturation de référence et la réelle distribution.

Les auteurs d'OpenHands et Epoch AI indiquent tous deux que SWE-bench Verified a une queue facile: 161 des 500 tâches nécessitent seulement 12 lignes de changement. Les scores élevés sont en partie motivés par cette queue. SWE-bench Pro se limite à plus de 10 changements de ligne et rend des scores dans la plage de 2359% même pour les systèmes frontaliers.

> Les ouvertures des mains auteurs et l'époque de l'IA ont marqué SWE-bench Verified 有简单尾部:500 个任务中161 个 个只需要1-2 行变更──高分部分由该尾部驱动──SWE-bench Pro 限制10+ 行变更,即使前沿系统也返回23-59% 范围──你的生产分布几乎肯定更接近Pro而非 Verified──

Implication pour choisir un agent: exécuter un sous-ensemble Pro-like de votre propre backlog de bug. Le score qui compte est le score sur les tâches représentatives de ce que vous expédez.

> 选择 Agent 的含义: dans votre propre bug 积压上运行 Pro 类子集── 重要分数是代表你发布任务的分数──

## Utilisez-le avec le cadre de réalisation
```figure
a5-scaffold-delta
```

## Utilisez-le

`code/main.py`compare deux échafaudages de jouets à l'aide d'un agent sur une distribution fixe de mini-tasks:

> `code/main.py`Comparer les deux jouets dans la distribution de tâches mini-fixées:

1. Une .**JSON tool-call**un échafaudage qui prend une action par tour.
   Le mot grec traduit par " le mot grec "**JSON 工具调用**- Je suis en train de faire un tour.
2. Une .**CodeAct**un échafaudage qui peut émettre un petit extrait Python par action.
   Le mot grec traduit par " le mot grec "**CodeAct**Chaque mouvement peut être émis avec un petit code Python.

Les deux utilisent un " modèle " de stub (règles déterministes) afin que la comparaison isola l'échafaudage de la qualité du modèle.

> 两者使用存根模型 (Règles de détermination) pour comparer les cadres de travail avec les cadres de travail de qualité séparés.

## Envoyez-le . Produit .

`outputs/skill-scaffold-audit.md`aide à vérifier un échafaudage proposé d'agent de codage avant son adoption: qualité de récupération, présence du vérificateur, isolement des boîtes à sable et conformité des points de référence à la distribution.

> `outputs/skill-scaffold-audit.md` aider à la mise en œuvre de la proposition de code de l'Audit pré-acquisition Agent 脚手架:检索质量、验证器存在、沙箱隔离、基准到分布契合──

## Les exercices

1. On court .`code/main.py`Combien de tours chaque échafaudage prend-il sur le même ensemble de tâches ?
   Le mot " l' économie " est traduit par " l' économie ".`code/main.py`Combien de roues de chaque épisode de la même série de tâches ?

2. Lisez le document OpenHands (arXiv:2407.16741). Le document soutient que CodeAct dépasse les appels d'outil JSON sur les tâches complexes.
   Le codeAct sur une tâche complexe a surmonté JSON 工具调用──识别论文承认一个失败模式并写一句该模式在生产中何时主导──

3. Choisissez une tâche de votre backlog de bug qui nécessiterait plus de 10 lignes de changement sur deux fichiers. Estimer la probabilité de succès de bout en bout pour un modèle frontalier sous (a) appels à l'outil JSON et (b) CodeAct. Justifier l'écart.
   Le codeAct est un outil de calcul qui permet de calculer les différences entre les deux types de fichiers.

4. SWE-bench Verified a 161 tâches de 12 lignes à un seul fichier.
   Suivant:SWE-bench Verified Il y a 161 个单文件 1-2 行任务──构建排除它们的分数──排行榜如何重排?

5. Lisez "Introduction de la vérification du banc SWE" (OpenAI). Expliquez la méthodologie spécifique utilisée pour supprimer les tâches ambiguës et nommez une catégorie que la curation manquerait.
   La première partie de la série est consacrée à la création de la série "Show Me" et à la création de la série "Show Me" (en anglais).

## Les termes clés

| Term | What people say | What it actually means |
|---|---|---|
| 术语 | 通俗说法 | 实际含义 |
| SWE-bench | "Coding benchmark" | Real GitHub issues with ground-truth patches and test suites |
| SWE-bench | "编码基准" | 带真实补丁和测试套件的真实 GitHub issue |
| SWE-bench Verified | "Cleaned subset" | 500 human-curated tasks, easier-tail present |
| SWE-bench Verified | "清理的子集" | 500 个手工策划任务，存在简单尾部 |
| SWE-bench Pro | "Harder subset" | 10+ line changes; frontier sits at 23–59% |
| SWE-bench Pro | "更难的子集" | 10+ 行变更；前沿在 23-59% |
| CodeAct | "Code-as-action" | Agent emits Python; Jupyter-style kernel executes in sandbox |
| CodeAct | "代码即动作" | Agent 发出 Python；Jupyter 风格内核在沙箱执行 |
| JSON tool call | "Function calling" | Each action is a structured JSON payload validated before execution |
| JSON 工具调用 | "函数调用" | 每动作是执行前验证的结构化 JSON 负载 |
| Scaffold | "Agent framework" | Retrieval + planner + executor + verifier loop around the base model |
| 脚手架 | "Agent 框架" | 围绕基础模型的检索 + 规划器 + 执行器 + 验证器循环 |
| ACI (Agent-Computer Interface) | "SWE-agent's format" | Command set designed for LLM ergonomics, not human shells |
| ACI（Agent-计算机接口） | "SWE-agent 格式" | 为 LLM 人体工程学设计的命令集，非人类 shell |
| Verifier loop | "Test-and-retry" | Run tests, read output, revise patch; biggest non-model reliability gain |
| 验证器循环 | "测试并重试" | 运行测试、读输出、修订补丁；最大非模型可靠性增益 |

## Encore une lecture

- [Jimenez et al. — SWE-bench](https://www.swebench.com/) l'indice de référence et la méthodologie originaux.
  Traduction anglaise: original基准和方法论
- [OpenAI — Introducing SWE-bench Verified](https://openai.com/index/introducing-swe-bench-verified/) comment le sous-ensemble de la sélection a été construit.
  Comment construire un ensemble ?
- [Wang et al. — OpenHands: An Open Platform for AI Software Developers](https://arxiv.org/abs/2407.16741) Architecture CodeAct et conception de flux d'événements.
  Le codeAct est un code-conception et un code-conception.
- [Epoch AI — SWE-bench leaderboard](https://epoch.ai/benchmarks)- Les scores en direct.
  En français, le nombre de personnes qui suivent le cours est de 7 à 7 ans.
- [Anthropic — Measuring agent autonomy](https://www.anthropic.com/research/measuring-agent-autonomy) cadrage de fiabilité des agents de codage à long horizon.
  Le code de l'agent est un cadre de confiance.
