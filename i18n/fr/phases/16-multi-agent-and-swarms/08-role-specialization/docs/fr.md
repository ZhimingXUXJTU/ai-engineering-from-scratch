# Rôle spécialisation  Planificateur, critique, exécuteur, vérificateur  spécialisation  critiqueur  planificateur  rôle

> La décomposition multi-agent la plus courante en 2026: un agent planifie, un exécute, un critique ou vérifie. MetaGPT (arXiv:2308.00352) formalite cela en tant que SOP codés en instructions de rôle  Product Manager, Architect, Project Manager, Engineer, QA Engineer  suivant `Code = SOP(Team)`- Je suis désolé . ChatDev (arXiv:2307.07924) renferme le concepteur, le programmeur, l'examen, le testeur à travers une "chaîne de chat" avec "déhallucination communicative" (les agents demandent explicitement des détails manquants). Le vérificateur est porteur de charge: Cemri et al. (MAST, arXiv:2503.13657) montre que chaque défaillance multi-agent peut être tracée à la vérification manquante ou cassée. PwC a rapporté un gain de précision de 7 fois (10% → 70%) à partir de boucles de validation structurées dans CrewAI.

> **【中文解读】**Ce chapitre présente la spécialisation des rôles pour chaque agent, la répartition des rôles et des compétences spécifiques, l'amélioration de l'efficacité de l'équipe dans son ensemble.

> **【拓展：role specialization→具体应用】**La spécialisation des rôles est le concept central de l'Agence de l'Agence de l'Agence de l'Agence de l'Agence de l'Agence de l'Agence de l'Agence de l'Agence de l'Agence de l'Agence de l'Agence de l'Agence de l'Agence de l'Agence de l'Agence de l'Agence de l'Agence de l'Agence de l'Agence de l'Agence de l'Agence de l'Agence de l'Agence de l'Agence de l'Agence de l'Agence de l'Agence de l'Agence de l'Agence de l'Agence de l'Agence de l'Agence de l'Agence de l'Agence de l'Agence de l'Agence de l'Agence de l'Agence de l'Agence de l'Agence de l'Agence de l'Agence de l'Agence de l'Agence de l'Agence de l'Agence de l'Agence de l'Agence de l'Agence de l'Agence de l'Agence de l'Agence de l'Agence de l'Agence de l'Agence de l'Agence de l'Agence de l'Agence de l'Agence de l'Agence de l'Agence de l'Agence de l'Agence de l'Agence de l'Agence de l'Agence de l'Agence de l'Agence de l'Agence de l'Agence de l'Agence de l'Agence de l'Agence de l'Agence de l'Agence de l'Agence de l'Agence de l'Agence de l'Agence de l'Agence de l'Agence de l'Agence de l'Agence de l'Agence de l'Agence de l'Agence de l'Agence de l'Agence de l'Agence de l'Agence de l'Agence de l'Agence de l'Agence de l'Agence de l'Agence de l'Agence de l'Agence de l'Agence de l'Agence


**Type:** Learn | **类型:** 学习
**Languages:** Python (stdlib) | **语言:** Python (标准库)
**Prerequisites:** Phase 16 · 04 (Primitive Model), Phase 16 · 05 (Supervisor) | **前置知识:** Phase 16 · 04 (Primitive Model), Phase 16 · 05 (Supervisor)
**Time:** ~60 minutes | **时间:** ~60 分钟

>  **【前置】**學本節前Please first master:Phase 16·04-05(原语+Supervisor)。本节是2026 最常见的多代理 分解模式:Planner + Critic + Executioner + Verifier。
>  **【类比】**角色专业化 = "film制作团队"──Planner = 编剧(定方向)、Executor = 演员(执行)、Critic = 内审、Verifier = 质检员──MetaGPT、ChatDev、CrewAI 都用这种角色分解──Cemri 等人 MAST论文:所有多 Agent 失败都可追溯到"缺少或破损的验证人"验证是承重墙──PwC 案例:加验证人 让准确率从10% 到70% 7倍)──

## ♪ Problème ♪ Introduction du problème ♪

Les systèmes multi-agents génériques produisent des sorties génériques. Trois codeurs dans un chat de groupe écrivent trois saveurs du même code médiocre. Vous pouvez ajouter plus d'agents, ajouter plus de tours, et toujours ne pas franchir le seuil de qualité.

> Les trois éditeurs du groupe de discussion écrivent trois codes de même type de goût. Vous pouvez ajouter plus d'agent, plus de fois, mais vous ne pouvez toujours pas franchir la porte de qualité.

Le problème n'est pas la quantité mais l'uniformité. Trois agents identiques donnés la même tâche produira trois réponses erronées similaires. Ils partagent les mêmes points aveugles parce qu'ils partagent le même prompt et le même modèle.

>                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                              

La solution n'est pas plus d'agents  c'est * différents * agents. Assignez des rôles distincts. Donnez aux outils critiques que le planificateur n'a pas. Donnez au vérificateur une suite de tests objective. Maintenant, le système a un désaccord interne avec la correction à la terre, pas seulement des devinettes parallèles.

> La méthode de réparation n'est pas plus agent mais * différent* agent. Distribuer différents rôles. Donner aux critiques planificateurs sans outils. Donner aux vérificateurs un ensemble de tests objectif.

Le changement clé: de "plus d'agents faisant la même chose" à "agents différents faisant des choses différentes". Le parallélisme sans spécialisation est juste une spéculation coûteuse.

> 关键转变: de "Plus d'agents font la même chose" à "divers agents font des choses différentes"― pas de conjonction spécialisée est simplement une spéculation coûteuse― la spécialisation crée un système qui capture ses erreurs d'incompatibilité―

## Concept Le concept central

### Les quatre rôles canoniques

**Planner.**Lire l'objectif, produire une liste d'étapes ou une spécification.

> **规划者。**读取目标,产生步骤列表或规范──工具:知识检索、文档──输出: structuration plan──

**Executor.**Lire un plan étape par étape, produire l'artefact. outils: les outils de travail réels (compilateur de code, shell, client API).

> **执行者。**Chaque fois que vous lisez un plan, vous pouvez créer un outil.

**Critic.**Lire l'exécution de l'exécuteur contre l'intention du planificateur. outils: accès uniquement en lecture à l'artefact, analyse statique.

> **批评者。**根据规划者意图阅读执行者输出──工具:对工件的只读访问、静态分析──输出:接受/拒绝及原因──

**Verifier.**Lire l'artefact et effectuer un contrôle déterministe. outils: test runner, type checker, validateur de schéma. sortie: passer/échouer avec des preuves.

> **验证者。**读取工件并运行确定性检查──工具:测试运行器、类型检查器、模式验证器──输出:通过/失败及证据──

Le critique est subjectif, opinionné, souvent basé sur le LLM. Le vérificateur est objectif, déterministe, souvent basé sur le code.

> Les critiques sont subjectives, généralement basées sur le LLM, les vérificateurs sont objectifs, généralement basés sur le code, ils ne sont pas le même rôle.

Les systèmes de vérification de code sont les plus courants, mais les résultats sont les plus mauvais.

> Les confondre en une seule est la plus commune à plusieurs agents  conception de erreurs  Les systèmes de systèmes de seulement les critiques  LLM  reviseurs  obtiennent des sorties similaires  mais non erronées  Les systèmes de seulement les vérifiants  code inspection  obtiennent des sorties correctes  mais mauvaises  Les deux nécessitent: les critiques sont responsables du goût, les vérifiants sont responsables de la justesse

### Le modèle de traitement des méta-gPT

MetaGPT (arXiv:2308.00352) code les SOP de l'ingénierie logicielle comme des instructions de rôle:

> MetaGPT(arXiv:2308.00352)将软件工程 SOP 编码为角色提示:

Le cadre "SOP" est emprunté aux organisations humaines: les procédures opérationnelles standard transforment le travail ad hoc en processus répétable. MetaGPT l'applique aux LLM.

> Le cadre "SOP" s'appuie sur l'organisation humaine: le processus d'exploitation standard se transforme en processus récurrents.

- **Product Manager**écrit le PRD.
  Le mot grec traduit par " le mot grec "**产品经理**编写 PRD。
- **Architect**produit la conception du système.
  Le mot grec traduit par " le mot grec "**架构师**产生系统设计── voir aussi
- **Project Manager**- Il partage les tâches.
  Le mot grec traduit par " le mot grec "**项目经理**Je suis en train de démêler les tâches.
- **Engineer**les outils.
  Le mot grec traduit par " le mot grec "**工程师** réaliser 
- **QA Engineer**Il fait des tests.
  Le mot grec traduit par " le mot grec "**QA 工程师**Je suis en train de faire une expérience.

Chaque rôle a un schéma d'entrée/sortie strict.`Code = SOP(Team)`Les SOP déterministes transforment une équipe de LLM en un pipeline prévisible.

> Chaque rôle a un mode d'entrée/sortie strict.`Code = SOP(Team)`公式确定性 SOP transformera une équipe LLM en une ligne de flux prévisible.

Le point de vue clé: encoder le flux de travail de l'équipe comme code, pas comme conversation. Chaque rôle de LLM est un nœud dans un graphique déterministe; la structure du graphique est écrite par l'homme. Les LLM font le travail local; les humains possèdent le flux de travail mondial.

> 关键洞察:将团队工作流编码为代码,而不是对话――每个LLM 角色是确定性图中的节点;图结构由人类编写――LLM做局部工作;人类拥有全局工作流――

### La déhallucination communicative de ChatDev

ChatDev ajoute un mouvement clé: lorsqu'un exécuteur a besoin d'un détail spécifique qui n'était pas dans le plan, il demande explicitement au concepteur avant de continuer.

> ChatDev a ajouté une initiative clé: lorsque l'exécuteur a besoin de détails spécifiques dans un plan, il demande clairement au concepteur avant de continuer.

Le modèle capture les hallucinations à leur source. Au lieu de détecter des détails fabriqués après le fait (difficile), il empêche la fabrication en obligeant l'exécuteur à demander avant de supposer.

> Le modèle est à l'origine de la capture de l'illusion. Il ne s'agit pas de vérifier les faits après les faits, mais de demander à l'exécuteur de pré-interroger l'hypothèse pour prévenir la falsification.

Mise en œuvre: le prompt de rôle comprend "lorsque vous avez besoin d'informations spécifiques qui ne vous ont pas été données, demandez le rôle pertinent par son nom avant de produire une sortie".

> 实现: rôle提示包括"When you need you not provided specific information, ask relevant role"

### Pourquoi le vérificateur est le plus important

Cemri et al. (MAST) ont suivi 1642 échecs d'exécution multi-agent. 21,3% étaient des lacunes de vérification  le système a envoyé une réponse que personne n'avait vérifiée. Les 79% restants remontent souvent à "il y avait un contrôle qui a échoué silencieusement ou n'a jamais été exécuté. " La vérification est le rôle porteur de charge.

> Cemri 等人(MAST) a suivi 1642 多 代理 执行失败──21.3% 验证缺口系统发布没有人检查过的答案──其余79% généralement remontent à "un seul contrôle a été silencieusement échoué ou jamais fonctionné"──验证是承担重角色──

Le nombre de 21,3% est la statistique la plus citée en 2026 en ingénierie multi-agents. Il dit: si vous ajoutez un seul rôle à votre système, faites-en un vérificateur. Pas un critique, pas un planificateur  un vérificateur déterministe avec des contrôles au niveau du code.

> 21,3% Cette figure est la statistique la plus citée dans l'agence 工程 de 2026 ⋅ ans. Elle dit: si vous ajoutez un seul rôle au système, faites-le devenir un vérificateur.

PwC a rapporté (CrewAI deployments, 2025) que l'ajout d'une boucle de validation structurée a déplacé la précision de 10% à 70%.

> Le rapport de PwC CrewAI 部署,2025) ajoute un cycle de vérification structurée qui permettra d'augmenter le taux de précision de 10% à 70%― un rôle entraînera une augmentation de 7 fois.

### Critic vs vérificateur

- Un critique est un maître d'école qui examine un artefact pour la qualité.
  Le critique est un LLM de qualité de l'objet de l'examen.
- Un vérificateur est un programme déterministe exécuté sur l'artefact. objectif. donne le passage/échec avec des preuves.
  Le testateur est un processus de détermination effectué sur le travail.

Utilisez les deux. Le critique capture les problèmes de goût que le vérificateur ne peut pas articuler. Le vérificateur capture les bugs que le critique ne peut pas voir parce qu'ils ne se montrent que pendant la mise en marche.

> Les critiques ne peuvent pas exprimer les problèmes de qualité qu'ils rencontrent. Les critiques ne peuvent pas exprimer les bugs qu'ils rencontrent en cours de fonctionnement.

Un ordre commun: vérificateur d'abord (rapide, tue évidemment le travail cassé), puis critique (légère, raffinant la qualité). Certaines équipes inversent l'ordre pour détecter les problèmes de goût avant de dépenser des calculs sur le code cassé.

> 常见顺序:先验证者(快,杀死明显破损的工作), puis critiqueur(慢,精炼质量) ・・・ certaines équipes翻转顺序以在花计算资源修复破损代码之前捕获质量问题──测试哪种适合你的任务──

### Le modèle anti-

Chaque rôle dans votre système est un LLM et chaque rôle est "il me semble bon". Mode de défaillance MAST classique. Ajoutez au moins un vérificateur dont le passage/fail est décidé par code, pas par un LLM.

> Chaque rôle dans votre système est LLM, chaque rôle est "apparemment mal" ⋅ le modèle classique MAST failure ⋅ au moins ajouter un code au lieu de LLM décide de passer/failure de l'assureur ⋅

### Cartographie du cadre

- **CrewAI** `Agent(role, goal, backstory)`est la surface de spécialisation du livre.
  Le mot grec traduit par " le mot grec "**CrewAI** `Agent(role, goal, backstory)`Il s'agit de la surface de spécialisation du cours.
- **LangGraph** les nœuds peuvent avoir des instructions spécialisées; les bords forcent le pipeline.
  Le mot grec traduit par " le mot grec "**LangGraph** 节点可以有专用提示;边强制流水线──
- **AutoGen** Agents conversables spécifiques à un rôle avec des noms d'un mot dans un chat de groupe.
  Le mot grec traduit par " le mot grec "**AutoGen** Dans le GroupeChat, un rôle spécifique est défini par un agent conversable。
- **OpenAI Agents SDK** les outils de transfert entre les agents spécialisés dans les rôles.
  Le mot grec traduit par " le mot grec "**OpenAI Agents SDK** 角色专业化 代理 之间的交接工具──

## Construisez-le et mettez-le en œuvre.
```figure
swarm-roles
```

## Faites-le

`code/main.py`met en œuvre un pipeline à 4 rôles construisant une fonction Python simple:

> `code/main.py`实现 une construction simple Python 函数 de 4 角色流水线:

- **Planner**produit une spécification.
  Le mot grec traduit par " le mot grec "**规划者**Il y a des règles.
- **Executor**génère une chaîne de code.
  Le mot grec traduit par " le mot grec "**执行者**Je suis en train de faire une petite histoire.
- **Critic**(SIMULATION de L'ALM) indique des problèmes évidents.
  Le mot grec traduit par " le mot grec "**批评者**(LLM 模拟) 标记明显问题──
- **Verifier**exécute le code généré dans une boîte à sable (`exec`) contre un cas d'essai.
  Le mot grec traduit par " le mot grec "**验证者**Dans une boîte`exec`) sont des codes générés pour des cas de test utilisés.

La démo se déroule deux fois: une fois où l'exécuteur produit un code correct (critique + vérificateur tous les deux passent), une fois où l'exécuteur produit un code hors spécificité (critique manque le bug parce qu'il semble plausible, vérificateur le capture parce que le test échoue).

> 演示运行两次:一次执行者产生正确的代码(批评者 + 验证者都通过),一次执行者产生偏离规范的代码(批评者因为看起来合理而错过错误,验证者因为测试失败而捕获它) 

## Utilisez-le avec le cadre de réalisation

`outputs/skill-role-designer.md`Il prend une tâche et produit la liste de rôles (3-5 rôles), le schéma d'entrée/sortie par rôle et le contrôle du vérificateur.

> `outputs/skill-role-designer.md`接收任务并产生角色名册(3-5 个角色) 、 chaque rôle de mode d'entrée/sortie et de vérificateur de contrôle.

## Envoyez-le . Produit .

Liste de contrôle:

> 检查清单:

- **At least one deterministic verifier.**Jamais tout-LLM.
  Le mot grec traduit par " le mot grec "**至少一个确定性验证者。**Ne jamais avoir de diplôme.
- **Explicit I/O schema per role.**Le planificateur renvoie une spécification, pas de la prose; l'exécuteur lit ce schéma.
  Le mot grec traduit par " le mot grec "**每个角色有明确的 I/O 模式。**规划者返回规范,不是散文;执行者读取该模式──
- **Communicative dehallucination.**L'exécuteur doit demander à l'organisateur quand les informations manquent; ne jamais les inventer.
  Le mot grec traduit par " le mot grec "**交流去幻觉。**L'exécuteur doit demander au planificateur lorsqu'il manque de l'information; ne jamais évoquer.
- **Critic/verifier ordering.**Exécutez le critique d'abord (bon marché, il capture des problèmes de conception), le vérificateur en second (légers, il capture des bugs).
  Le mot grec traduit par " le mot grec "**批评者/验证者顺序。**Il est également possible de trouver des informations sur les différents types de produits et services de l'industrie automobile.
- **Loop budget.**Max 2 critique-exécuteur revue rounds avant d'escalader à humain.
  Le mot grec traduit par " le mot grec "**循环预算。**Le plus de 2 critiques-exécuteurs avant de passer à l'humanité

## Les exercices

1. On court .`code/main.py`et observez comment le vérificateur détecte le bug que le critique a raté.`return`En ce qui concerne les tests de fonctionnement, qu'est-ce qui est pris en compte si le test de fonctionnement est manqué ?
   Le mot " l' économie " est traduit par " l' économie ".`code/main.py`Il a été créé par le gouvernement de la République de Suède pour la première fois en 2011.`return`En tant qu'expérienceur extraordinaire, il a capturé quoi ?
2. Ajouter un cinquième rôle: "analyste des exigences" qui traduit le souhait de l'utilisateur en spécification prête à l'emploi.
   Le rôle de l'analyste de besoins est de définir les besoins des utilisateurs.
3. Lisez la section 3 de MetaGPT ("Agent"). Lisez le schéma d'entrée/sortie de chacun des 5 rôles de MetaGPT.
   Le rôle de l'agent est de 5 personnages dans chaque mode d'entrée/sortie.
4. Lisez le diagramme de la chaîne de chat de ChatDev (arXiv:2307.07924 Figure 3). Identifiez où la déhallucination communicative rompt une boucle qui serait autrement infinie.
   Le chat dev est un réseau de communication sans fin.
5. L'augmentation de la précision de 7 fois de PwC est due aux boucles de vérification.
   Le taux de précision de 7 fois de la PwC est augmenté par le cycle de vérification.

## Les termes clés

| Term | What people say | What it actually means |
|------|----------------|------------------------|
| Role specialization / 角色专业化 | "Different agents, different jobs" / "不同 Agent，不同工作" | Distinct system prompts tuned for planner/executor/critic/verifier roles. / 为规划者/执行者/批评者/验证者角色调优的独特系统提示。 |
| SOP pattern / SOP 模式 | "Encoded standard operating procedure" / "编码标准操作流程" | MetaGPT's framing: strict I/O schemas per role turn a team into a pipeline. / MetaGPT 的框架：每个角色的严格 I/O 模式将团队变成流水线。 |
| Communicative dehallucination / 交流去幻觉 | "Ask before inventing" / "先问再发明" | ChatDev pattern: executor asks planner when a detail is missing rather than making one up. / ChatDev 模式：执行者在细节缺失时询问规划者而不是编造。 |
| Critic / 批评者 | "LLM reviewer" / "LLM 审阅者" | Subjective, opinionated reviewer. Catches taste issues. Can be fooled by plausible prose. / 主观的、有观点的审阅者。捕获质量问题。可以被似是而非的散文愚弄。 |
| Verifier / 验证者 | "Deterministic check" / "确定性检查" | Code-based pass/fail. Test runner, type checker, schema validator. Cannot be fooled. / 基于代码的通过/失败。测试运行器、类型检查器、模式验证器。不能被愚弄。 |
| Verification gap / 验证缺口 | "No one checked" / "没人检查" | 21.3% of MAST failures. Answer shipped without a check that would have caught the bug. / 21.3% 的 MAST 失败。发布答案时没有会捕获 bug 的检查。 |
| Revision loop / 修订循环 | "Critic sends it back" / "批评者打回" | Critic rejection triggers executor re-run with feedback. Needs a budget. / 批评者拒绝触发带反馈的执行者重新运行。需要预算。 |
| All-LLM anti-pattern / 全 LLM 反模式 | "Looks good to me" / "看起来不错" | Every role is an LLM, no deterministic check. Classic MAST failure. / 每个角色都是 LLM，没有确定性检查。经典的 MAST 失败。 |

## Encore une lecture

- [Hong et al. — MetaGPT: Meta Programming for Multi-Agent Collaboration](https://arxiv.org/abs/2308.00352) le document de référence du PPS en tant que rôle
  Le métaGPT:多 Agent 协作的元编程  SOP 作为角色提示的参考论文
- [Qian et al. — Communicative Agents for Software Development (ChatDev)](https://arxiv.org/abs/2307.07924) Chaîne de chat + déhallucination communicative
  Le lien entre les deux parties est le lien entre les deux parties.
- [Cemri et al. — Why Do Multi-Agent LLM Systems Fail?](https://arxiv.org/abs/2503.13657) Taxonomie MAST; les lacunes de vérification représentent 21,3% des défaillances
  Pourquoi plusieurs agents LLM 系统会失败?  MAST 分类法;验证缺口占失的21.3%
- [CrewAI docs — Agent roles](https://docs.crewai.com/en/introduction) surface spécifique de rôle de production
  Le rôle de l'agent dans le rôle de l'agent dans le rôle de l'agent dans le rôle de l'agent dans le rôle de l'agent dans le rôle de l'agent dans le rôle de l'agent dans le rôle de l'agent dans le rôle de l'agent dans le rôle de l'agent dans le rôle de l'agent dans le rôle de l'agent dans le rôle de l'agent dans le rôle de l'agent dans le rôle de l'agent dans le rôle de l'agent dans le rôle de l'agent dans le rôle de l'agent dans le rôle de l'agent dans le rôle de l'agent dans le rôle de l'agent dans le rôle de l'agent dans le rôle de l'agent dans le rôle de l'agent dans le rôle de l'agent dans le rôle de l'agent dans le rôle de l'agent dans le rôle de l'agent dans le rôle de l'agent dans le rôle de l'agent dans le rôle de l'agent dans le rôle de l'agent dans le rôle de l'agent dans le rôle de l'agent dans le travail
