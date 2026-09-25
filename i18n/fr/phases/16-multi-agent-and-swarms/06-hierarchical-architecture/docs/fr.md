# L'architecture hiérarchique et son mode d'échec

> La hiérarchie est le superviseur enraciné, les agents de direction sur les sous-gérants sur les travailleurs.`Process.hierarchical`est la version du manuel: a `manager_llm`La fonction de déléguer dynamiquement les tâches et de valider les sorties.`create_supervisor(create_supervisor(...))`. C'est le modèle naturel lorsque la tâche est un vrai tableau d'org. C'est aussi le modèle le plus susceptible de s'effondrer dans un boucle de gestion  les agents de gestion attribuent mal le travail, interprètent mal les sous-produits ou ne parviennent pas à un consensus.

> **【中文解读】**Ce chapitre présente la structure de l'organisation de l'architecture de plusieurs niveaux, adaptée à la répartition des tâches complexes.

> **【拓展：hierarchical architecture→具体应用】**La structure de niveau distribué va revenir au modèle des superviseurs à la mise en place du système de gestion de niveau supérieur, qui sera réparti au niveau moyen, et au niveau moyen, qui sera réparti au niveau inférieur.


**Type:** Learn + Build | **类型:** 学习 + 构建
**Languages:** Python (stdlib) | **语言:** Python (标准库)
**Prerequisites:** Phase 16 · 05 (Supervisor Pattern) | **前置知识:** Phase 16 · 05 (监督者模式)
**Time:** ~60 minutes | **时间:** ~60 分钟

>  **【前置】**• Les élèves doivent être informés de la situation de la société.
>  **【类比】**Le niveau de gestion est le plus élevé de la société. Le niveau de gestion est le plus élevé de la société.
> ️ **【易错点】**看到"任务复杂"就加层级 → 管理开销压系统──修复:先用序列或监督者单层跑,确认不够再分层;2-3层是上限──

## ♪ Problème ♪ Introduction du problème ♪

Une fois que le modèle de superviseur est cliqué, la prochaine étape naturelle est "et si les travailleurs sont eux-mêmes superviseurs?" Les équipes ont des sous-équipes; les entreprises ont des départements de départements.

> Une fois que le modèle de superviseur est compris, la prochaine étape de la nature est " si le travail lui-même est également un superviseur ? "

La tentation est forte parce que les organisations humaines fonctionnent de cette façon. Mais les hiérarchies LLM héritent de toutes les pathologies des hiérarchies humaines (perte d'information, mauvaise communication, itération lente) sans les effets stabilisateurs des relations humaines et de la culture partagée.

> La tentation est forte, car les organisations humaines travaillent de cette façon. Mais le niveau de LLM a hérité de tous les maux du niveau humain, sans aucun effet stable sur les relations humaines et la culture de partage.

Le problème: les gestionnaires de LLM ne sont pas les mêmes que les gestionnaires humains. Un gestionnaire humain a des antécédents stables sur ce que savent ses rapports. Un gestionnaire de LLM redécouvre l'org à chaque tournant de ce qui est dans son contexte.

> Le problème réside dans: les gestionnaires de l'LLM sont différents des gestionnaires humains. Les gestionnaires humains savent ce qu'ils ont de précoce et de stable.

C'est le mode de défaillance de base des systèmes hiérarchiques de MLL: chaque niveau de gestionnaire amplifie les erreurs du niveau précédent.

> C'est le modèle de défaillance de base du système LLM: chaque niveau de gestion augmente les erreurs de niveau supérieur.

## Concept Le concept central

### La forme

```
                 Manager
                 ┌─────┐
                 └──┬──┘
           ┌────────┴────────┐
           ▼                 ▼
       Sub-Mgr A         Sub-Mgr B
       ┌─────┐           ┌─────┐
       └──┬──┘           └──┬──┘
         ┌┴──┬──┐          ┌┴──┐
         ▼   ▼  ▼          ▼   ▼
       W1  W2  W3         W4  W5
```

Chaque nœud interne planifie, délègue et synthétise.

> Chaque élément interne est planifié, chargé et intégré.

Ce tableau reflète un tableau des organes humains, qui est à la fois sa force (modèle mental familier) et sa faiblesse (les organes humains ont des antécédents stables dont les LLM manquent).

> Ceci reflète la structure de l'organisation humaine, ce qui est à la fois son avantage et son faiblesse.

### Là où il brille

- **Clear org mapping.**Si la tâche réelle est départementale ("révision juridique du document, révision financière du document, révision technique du document, puis résumé pour l'exécutif"), la hiérarchie est explicite.
  Le mot grec traduit par " le mot grec "**清晰的组织映射。**Si la tâche réelle est de type départemental, la structure de niveau est claire.
- **Local summarization.**Chaque sous-gérant synthétise la production de son équipe avant que le chef de file ne la voie.
  Le mot grec traduit par " le mot grec "**局部摘要。**Chaque administrateur de premier niveau voit les résultats de son équipe avant de les compléter.

### Où il se brise

Trois modes de défaillance les post-mortem de 2026 continuent de trouver:

> L'analyse des événements de 2026 constate trois types de défaites:

Cemri et coll. (MAST, arXiv:2503.13657) les documentent comme des sous-familles de "failure de spécification" et de "disinformation interpersonnelle".

> Ces problèmes sont plus faciles à résoudre que les systèmes de niveau, car chaque niveau est ajouté à des étapes de réinterprétation.

1. **Task assignment error.**Le gestionnaire lit l'objectif, hallucine une décomposition et délègue à un sous-gestionnaire incorrect. Parce que le sous-gestionnaire travaille obéissamment sur ce qui lui a été donné, l'erreur ne surgit qu'à la synthèse supérieure  un niveau enlevée d'où un humain aurait pu l'avoir attrapé.
   Le mot grec traduit par " le mot grec "**任务分配错误。**管理者读取目标,幻觉出分解,并委派给错误的子管理者──因为子管理者服从处理给定的任务, l'erreur ne se révèle qu'à un niveau supérieur à celui qu'un être humain aurait pu capturer lorsqu'il est complété.
2. **Output misinterpretation.**Le sous-gérant renvoie " incapable de vérifier la réclamation X. " Le supérieur gérant résume comme " la réclamation X n'a pas été confirmée. " La signification dérive à tous les niveaux.
   Le mot grec traduit par " le mot grec "**输出误解。** "  "  "  "  "  "  "  "  "  "  "  "  "  "  "  "  "  "  "  "  "  "  "  "  "  "  "  "  "  "  "  "  "  "  "  "  "  "  "  "  "  "  "  "  "  "  "  "  "  "  "  "  "  "  "  "  "  "  "  "  "  "  "  "  "  "  "  "  " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " "
3. **Consensus loops.**Deux sous-gérants ne sont pas d'accord; le chef de file leur demande de se réconcilier; ils déléguent à nouveau; les travailleurs se réorganisent; les sous-gérants répondent légèrement différemment; boucle.`Process.hierarchical`Il y a des limites de niveau, mais la limite elle-même est maintenant un hyperparamètre.
   Le mot grec traduit par " le mot grec "**共识循环。**两个子管理员不一致; 顶层管理员要求他们协调; 它们向下重新委派;工作器重新运行; 子管理员回归略有不同的答案; 循环──CrewAI 的`Process.hierarchical`通过步骤限制来保护, mais la limitation elle-même est maintenant un superparamètre.

### La question décisive

Sequentiel (pipeline linéaire) vs hiérarchique: votre tâche a-t-elle réellement des sous-équipes indépendantes, ou est-ce qu'il s'agit d'un flux linéaire prétendant être un arbre?

> 顺序(线性流水线) vs 分层: votre tâche a vraiment une sous-équipe indépendante, c'est aussi un processus de ligne de bois ?

C'est le test que la plupart des équipes sautent. Ils atteignent la hiérarchie parce que cela semble sophistiqué, puis passent des semaines à déboguer la décomposition.

> C'est le test que la plupart des équipes ont passé. Ils ont choisi de se diviser en couches parce qu'ils semblent hauts, puis ils ont passé quelques semaines à se diviser et à se déplacer.

### Mise en œuvre de CrewAI
### Mise en œuvre du cadre de rôle

Les équipages de l'AIA `Process.hierarchical`Le directeur:

> `Process.hierarchical`Dans le cadre de la formation professionnelle, il est possible de créer un réseau de formation professionnelle.

Le gestionnaire LLM est lui-même un agent complet avec son propre contexte, son prompt et ses propres outils. Il n'est pas un dispatcher déterministe  il fait des appels de jugement sur la délégation, ce qui signifie qu'il peut faire de mauvais appels de jugement.

>  Manager LLM est lui-même un agent complet de soi-même sur la mise en page                                                                                                                                                                                                                                                     

- reçoit la tâche de premier niveau,
  Le premier est le premier.
- attribue des sous-tâches aux équipages,
  Le rôle de l'équipe est à la tête de l'équipe.
- évalue les résultats de l'équipage,
  Le groupe d'évaluation,
- décide de l'acceptation, de la rédélégation ou de l'itération.
  La décision est acceptée, réélue ou déléguée.

Documents: https://docs.crewai.com/en/introduction(voir "Processus hiérarchiques" dans les concepts de base).

> 文档:https://docs.crewai.com/en/introduction（在核心概念中查找"HierarchicalProcédure")

### La mise en œuvre de LangGraph
### Implementation du cadre graphique

LangGraph utilise des nids `create_supervisor`Le superviseur interne a son propre graphique; le superviseur externe traite le graphique interne comme un nœud opaque. C'est plus propre que CrewAI pour débogage (vous pouvez passer par chaque graphique séparément), mais plus difficile à exprimer la remodelage dynamique de l'arbre.

> LangGraph utilise le schéma `create_supervisor`调用──内部监督人有自己的图; externe监督人将内部图视为不透明节点──这在调试方面比 CrewAI更清晰(你可以分别步进每个图),但更难表达树的动态重塑──

La victoire en débogage est réelle: lorsque quelque chose ne va pas dans une hiérarchie LangGraph à 3 niveaux, vous pouvez isoler quel niveau a échoué en passant par chaque graphique de manière indépendante.

> 调试优势真实: lorsque trois niveaux de LangGraph échouent, vous pouvez passer par des étapes indépendantes dans chaque tableau pour séparer les niveaux qui ont échoué.

Référence: https://reference.langchain.com/python/langgraph-supervisor.

>  référence:https://reference.langchain.com/python/langgraph-supervisor。

## Construisez-le et mettez-le en œuvre.
```figure
swarm-hierarchy-token
```

## Faites-le

`code/main.py`Il dispose d'une hiérarchie de 3 niveaux:

> `code/main.py`运行一个3层层级:

- Directeur principal: divise une tâche en branches "ingénierie" et "juridique",
  Le gouvernement a décidé de démanteler la structure de la société.
- sous-gérant de l'ingénierie: divisé en travailleurs "frontend" et "backend",
  Le système de gestion de l'entreprise est divisé en deux types:
- sous-directeur juridique: un travailleur.
  Le gouvernement de la République de Chine a créé un système de gestion de l'entreprise.

La démo contraste avec le chemin heureux (tous sont d'accord) contre un **perturbed path**Lorsque la décomposition du directeur supérieur étiquette mal "legal" comme "financial" et observe la cascade d'erreurs  le sous-directeur effectue obéissamment les travaux financiers, le synthétiseur supérieur rapporte les résultats financiers, la question juridique initiale reste sans réponse.

> 演示对比了正常路径 (所有人一致) avec**扰动路径**, dont la division des gestionnaires de haut niveau sera " juridique " erronée comme " financière "并观察错误级联子管理员服从地做财务工作, toplevel综合者报告财务发现,原始法务问题没有得到答应;;

Le chemin perturbé est l'avertissement: les systèmes hiérarchiques amplifient les erreurs en silence. Le sous-gérant ne repousse pas ("vous avez dit finance, mais la tâche a dit légal "). Il suppose que le gérant sait mieux.

>  perturbation route est un avertissement: séparation de niveau système silencieux accroissement de l'erreur.

Je vais courir .

```
python3 code/main.py
```

La sortie montre les deux chemins avec un côté-à-côté clair de "ce qui a été demandé" vs "ce qui a été livré".

> 输出显示两条路径的清晰并排对比:" exigent quoi "与" livré quoi "

## Utilisez-le avec le cadre de réalisation

`outputs/skill-hierarchy-fitness.md`Les données de référence sont les données de référence de la structure de l'organisation, de la structure des organes, du budget de réconciliation, de la production, de la recommandation de modèle avec les modes d'échec spécifiques à prévenir.

> `outputs/skill-hierarchy-fitness.md` évaluer les tâches déterminées doit être utilisé par des niveaux, des séquences ou des superviseurs. 输入: description des tâches, organisation, structure, budget. 输出: mode de recommandations et de besoins de protection.

## Envoyez-le . Produit .

Si vous envoyez des hiérarchiques:

> Si vous déployez une structure de niveau:

- **Cap tree depth at 2.**Trois niveaux cachent déjà la plupart des erreurs de l'observabilité.
  Le mot grec traduit par " le mot grec "**将树深度限制在 2。**Les trois niveaux ont déjà caché la plupart des erreurs en dehors de la perception.
- **Explicit reconciliation budget.**Mettez au maximum des tirs avant que le chef de l'équipe ne s'engage.
  Le mot grec traduit par " le mot grec "**明确的协调预算。**Le gestionnaire de haut niveau doit soumettre le nombre maximal de roues.
- **Provenance on every synthesis.**Le résumé de chaque nœud doit indiquer les sorties de feuilles qui l'ont produit.
  Le mot grec traduit par " le mot grec "**每次综合的来源追溯。**Le résumé de chaque point doit être cité pour produire sa feuille de sortie.
- **Alert on decomposition drift.**Enregistrez la décomposition du gestionnaire par étape; diffère par rapport à la requête utilisateur. Si la décomposition ne couvre plus la requête, activez une alerte.
  Le mot grec traduit par " le mot grec "**分解漂移告警。**记录管理者每步的分解;与用户查询对比.

## Les exercices

1. On court .`code/main.py`Combien de niveaux de gestion de la remise avant que la sortie de haut dévient complètement de la question de l'utilisateur?
   Le mot " l' économie " est traduit par " l' économie ".`code/main.py`Comparer les routes normales aux routes perturbantes. Combien de niveaux de gestion sont nécessaires pour que les niveaux supérieurs de sortie soient complètement déconnectés des problèmes utilisateurs ?
2. Ajoutez un troisième niveau (supérieur -> sous -> sous-sous -> travailleur). Mesurez la fréquence à laquelle le chemin perturbé se corrige et diverge complètement à mesure que la profondeur augmente.
   La mesure avec l'augmentation de la profondeur, perturbe la voie de la rectification de soi et la fréquence de l'écart complet。
3. Mettre en œuvre un "canary" employé à chaque sous-administrateur qui est toujours posé la question initiale de l'utilisateur inchangé. Utilisez la réponse canarienne pour détecter la décomposition dérive. Comment le gestionnaire devrait-il réagir lorsque le canary ne convient pas à la réponse synthétisée?
   Traduction chinoise: Dans chaque enfant administrateur, une machine de travail "Kinshe" est mise en place, toujours posée à l'utilisateur original.
4. Lisez le journal de CrewAI `Process.hierarchical`Identifier une barrière de protection concrète appliquée par CrewAI (limite de pas, contrainte manager_llm) et décrire le mode de défaillance visé.
   Le groupe de travail de l'équipage`Process.hierarchical`文档──识别 CrewAI 应用一个具体防护措施(步骤限制、manager_llm 约束)并描述它针对的失败模式──
5. Comparer les superviseurs LangGraph à la hiérarchie CrewAI.
   Comparer LangGraph 监督者与 CrewAI 分层── qui facilite le dépistage du cycle de coordination ?

## Les termes clés

| Term | What people say | What it actually means |
|------|----------------|------------------------|
| Hierarchical / 分层 | "Org chart pattern" / "组织架构模式" | Supervisors over supervisors; only leaves do work. / 监督者之上还有监督者；只有叶子节点做实际工作。 |
| Manager LLM / 管理者 LLM | "The boss" / "老板" | The LLM that decomposes, assigns, and validates at an internal node. / 在内部节点进行分解、分配和验证的 LLM。 |
| Decomposition drift / 分解漂移 | "The boss lost the plot" / "老板偏离了主题" | Top manager's split no longer covers the original question. / 顶层管理者的拆分不再覆盖原始问题。 |
| Reconciliation loop / 协调循环 | "Endless meetings" / "无尽会议" | Sub-managers disagree; top re-delegates; workers re-run; loop until budget exhausted. / 子管理者不一致；顶层重新委派；工作器重新运行；循环直到预算耗尽。 |
| Depth-2 ceiling / 深度-2 上限 | "Don't go deeper than 2 levels" / "不要超过 2 层" | Empirical guardrail: 3+ levels collapses observability. / 经验防护：3+ 层使可观测性崩溃。 |
| Canary question / 金丝雀问题 | "Ground truth at every level" / "每层的基准真相" | A worker that is always asked the original query unchanged, to detect drift. / 一个总是被问及原始查询不变的工作器，用于检测漂移。 |
| Provenance chain / 来源链 | "Who said what" / "谁说了什么" | Trace from each synthesis back to the leaf outputs that produced it. / 从每个综合追溯到产生它的叶子输出。 |

## Encore une lecture

- [CrewAI introduction — Process.hierarchical](https://docs.crewai.com/en/introduction) manuel hiérarchique avec un directeur LLM
  Le processus.hiérarchique 带管理者 LLM 的教科书式分层
- [LangGraph supervisor reference](https://reference.langchain.com/python/langgraph-supervisor) superviseur en nid via `create_supervisor`
  Le langgraphe est un langage de la langue française.`create_supervisor`Le directeur de la rédaction
- [Anthropic engineering — Research system](https://www.anthropic.com/engineering/multi-agent-research-system)Pourquoi Anthropic a délibérément choisi un superviseur plat plutôt que hiérarchique
  Le langage de l'anthropie est le langage de l'anthropie.
- [Cemri et al. — Why Do Multi-Agent LLM Systems Fail?](https://arxiv.org/abs/2503.13657) Taxonomie MAST; section sur les défaillances de coordination documents décomposition dérive
  Pourquoi plusieurs agents LLM 系统会失败?  MAST 分类法;协调失败部分记录了分解漂移
