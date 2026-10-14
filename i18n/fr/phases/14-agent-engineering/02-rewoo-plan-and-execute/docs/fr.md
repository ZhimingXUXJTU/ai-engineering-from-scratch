# ReWOO et Plan-et-Exécutez: Découpe de la planification

> ReAct interpose la pensée et l'action dans un flux. ReWOO les sépare: un grand plan à l'avance, puis exécute. 5 fois moins de jetons, +4% de précision sur HotpotQA, et vous pouvez distiller le planificateur dans un modèle 7B. Plan-and-Execute l'a généralisé; Plan-and-Act l'a porté à la navigation Web.

> **【中文解读】**ReAct dans un flux de pensées et d'actions. ReWOO les séparera: d'abord, une fois, élaborer un plan complet, puis exécuter.

> **【拓展：ReWOO → 现代 Agent 架构】**Parmi les cinq modes de travail proposés par Anthropic, le modèle de planification et exécution est l'un des principaux.

>  **【前置】**精通本节前 請先掌握:Phase 14·01(Agent Loop / ReAct 循环) You must understand ReAct's "penser-action-observer" mode de remplacement, parce que ReWOO est là pour comprendre le jeton de ReAct's deuxième croissance problème; ainsi que le concept de diagramme de base (((DAG、拓排序), ne pas familier DAG 会卡在"依赖解析"那一步──

**Type:** Build | **类型:** 构建
**Languages:** Python (stdlib) | **语言:** Python (标准库)
**Prerequisites:** Phase 14 · 01 (Agent Loop) | **前置知识:** Phase 14 · 01 (Agent 循环)
**Time:** ~60 minutes | **时间:** ~60 分钟

## Objectifs d'apprentissage

- Expliquez pourquoi la fraction Planner / Worker / Solver de ReWOO économise des jetons et améliore la robustesse sur la boucle interleavée de ReAct.
  Le plan de réaction de ReWOO est plus fort que le cycle de réaction de ReAct.
- Implémenter un plan DAG, un exécuteur d'ordre dépendance et un résolveur qui compose les sorties de travail  tous stdlib.
  Le programme de réalisation DAG, dépendant de l'exécuteur et du travail de composition, est utilisé dans le cadre de la mise en œuvre de la norme.
- Décidez quand une tâche doit être exécutée en plan-et-exécution par rapport à ReAct interlevé, en utilisant le cadre "cinq modèles de flux de travail" de 2026 (Anthropic).
  Le système de gestion des ressources humaines est un système de gestion des ressources humaines.
- Reconnaître quand les données synthétiques du plan Plan-and-Act sont nécessaires pour des tâches Web ou mobiles à long terme.
  Reconnaître quand il faut un plan et un plan de travail pour traiter des tâches longues ou mobiles.

## Le problème , l' introduction du problème

La boucle de réaction-pensée-observation interdite de ReAct est simple et flexible, mais chaque appel à l'outil doit contenir le contexte précédent complet  y compris chaque pensée précédente. L'utilisation des jetons augmente quadratiquement avec la profondeur. Pire: lorsqu'un outil échoue au milieu de la boucle, le modèle doit dériver le plan entier de l'observation d'erreur.

> Le cycle de réaction de la réaction est simple et flexible, mais chaque utilisation de l'outil doit être accompagnée d'une mise en avant complète de la situation précédente.

ReWOO (Xu et coll., arXiv:2305.18323, mai 2023) a remarqué cela et a fait un pari: planifier tout à l'avance, chercher des preuves en parallèle, comporter la réponse à la fin. Un appel à la planification de LLM, N outil demande des preuves (peut être parallèle), un appel à la résolution de LLM. Le commerce est moins souple (le plan est statique) pour une efficacité de jeton beaucoup plus élevée et des modes de défaillance plus clairs.

>  **【类比】**ReWOO 像装修房子前先出施工图: designer一次性画完全部工序 (设计师一次性画完全部工序) 工人按图并行施工互不打扰 (工程器) 工人按图并行施工互不打扰 (工程器) 验收时把所有的工序结果拼拼拼在一起结算 (求解器) ⋅ React 则像边施工边设计,每个工人可以翻阅前面所有工人的笔记动手,所以10步后笔记就堆成山──

> ReWOO(Xu 等人,arXiv:2305.18323,2023 年 5 月) a noté ce point et a proposé un programme: pré-planifier l'ensemble de la tâche,并行获证,最后组合答案──一次LLM 调用规划、N 次工具调用获证 (可并行)、一次LLM 调用求解──代价是灵活性降低(计划是静态的), mais en échange de meilleurs symboles 效率和更清晰的失败模式──

## Le concept de base.

### Les trois rôles

```
Planner:  user_question -> [plan_dag]        # 规划器：将用户问题转为计划 DAG
Workers:  [plan_dag]     -> [evidence]        # 工作器：执行工具调用获取证据（可并行）
Solver:   user_question, plan_dag, evidence -> final_answer  # 求解器：组合证据生成最终答案
```

Le planificateur produit un DAG. Chaque nœud nomme un outil, ses arguments et les nœuds antérieurs dont il dépend (références comme `#E1`- Je suis là .`#E2`Les ouvriers exécutent les nœuds dans l'ordre topologique.

> 规划器 générer un DAG. Chaque nœud spécifie un outil, ses paramètres ainsi que les précédents nœuds dépendants, tels que`#E1`- Je suis là.`#E2`Étal citation) ――工作器按拓顺序执行节点──求解器将所有内容拼拼在一起──

### Pourquoi 5 fois moins de jetons

ReAct augmente la longueur de la prompt en ligne avec le nombre de étapes. À l'étape 10, la prompt contient la pensée 1 plus l'action 1 plus l'observation 1 plus la pensée 2 plus l'action 2 plus l'observation 2, etc. Chaque étape intermédiaire inclut également de manière redondante la prompt originale.

> La longueur des suggestions de réaction est augmentée au rythme de la croissance de la ligne.

ReWOO paie un prompt de planificateur (grand), N petits employés (chacun juste l'appel à l'outil, pas de chaîne), et un prompt de résolveur. sur HotpotQA, le papier mesure ~ 5 fois moins de jetons tout en obtenant une précision absolue de +4.

> ReWOO n'a besoin qu'une seule fois de planteur de suggestions, chaque fois de suggestion ne contient que des outils de mise en service, sans chaînes historiques) et une seule fois de suggestion de solution.

### Pourquoi il est plus robuste

Si le travailleur 3 échoue dans ReAct, la boucle doit raisonner à partir de l'erreur au milieu du courant. Dans ReWOO, le travailleur 3 renvoie une chaîne d'erreur; le résolveur la voit dans le contexte du plan d'origine et peut se dégrader avec grâce. La localisation de l'échec est par nœud, pas par étape.

> Si le travail 3 échoue dans ReAct, le cycle doit être défini en milieu de processus par erreur. Dans ReWOO, le travail 3 retourne une chaîne d'erreur; le solliciteur voit dans le texte ci-dessus du plan initial qu'il peut être déclassé.

### Destillation par planificateur

Le deuxième résultat du document: parce que le planificateur ne voit pas les observations, vous pouvez affiner un modèle 7B sur les sorties du planificateur d'un professeur 175B. Le petit modèle gère la planification; le grand modèle n'est pas nécessaire à l'inférence.

> Deuxième résultat du thèse: parce que le planificateur ne voit pas de résultats observés, vous pouvez modifier un modèle de travail de 175B en produisant un modèle de travail de 7B.

> **【拓展：规划器蒸馏 → 成本优化】**Parce que le planificateur n'a pas besoin d'observation, il peut faire sortir le planning du modèle de 175B à 7B 模型.

### Le plan et l'exécution (LangChain, 2023)
### Plan et exécution (2023)

L'équipe LangChain a généralisé ReWOO en août 2023 en un nom de modèle: Plan-et-Execute. Le planificateur d'avant émet une liste d'étapes, l'exécuteur exécute chaque étape, un réplanificateur optionnel peut réviser après avoir observé les résultats.

> LangChain 团队 L'article de l'août 2023 de ReWOO 泛化为一个模式名称:Plan-and-Execute。前置规划器发发出步骤列表,执行器运行每一步,可选的重新规划器可以在观察结果后修订──这比 ReWOO更接近 ReAct(重新规划器将观察带回规划),但保留了代币节省──

### Le projet de loi (Erdogan et coll., arXiv:2503.09572, ICML 2025)

Plan-and-Act étalonne le schéma à des agents Web et mobiles à long horizon. La contribution clé est les données de plan synthétiques: un générateur de trajectoire étiqueté produit des données de formation où le plan est explicite. Utilisé pour affiner les modèles de planificateur qui continuent à travailler après 3050 étapes sur des tâches similaires à WebArena où une seule trajectoire ReAct perd de la cohérence.

> Plan-and-Act étendra ce modèle à long terme à des pages Web et à des agents mobiles. Une contribution clé est la synthèse de données du plan: le générateur de traces de marque génère des données de formation, dont le plan est évident.

### Quand choisir lequel

| Pattern | When | 适用场景 |
|---------|------|----------|
| ReAct | Short tasks, unknown environment, need reactive exception handling | 短任务、未知环境、需要响应式异常处理 |
| ReWOO | Structured tasks with known tools, token-sensitive, parallelizable evidence | 结构化任务、已知工具、Token 敏感、可并行 |
| Plan-and-Execute | Like ReWOO but with replanning after partial execution | 类似 ReWOO 但支持执行后重新规划 |
| Plan-and-Act | Long-horizon (>30 steps), web/mobile/computer-use | 长程任务(>30步)、网页/移动端/计算机使用 |
| Tree of Thoughts | Search is worth paying for (Lesson 04) | 值得付出搜索成本的场景 |

Direction de décembre 2024 d'Anthropic: commencez par le plus simple. Si la tâche est un appel à outil plus un résumé, ne construisez pas ReWOO. Si la tâche est une tâche de recherche en 40 étapes, ne faites pas ReAct seul.

> 🤔 **【困惑】**Q: 既然 ReWOO 省5 倍代币还准确,为什么不全部使用 ReWOO? A: 因为 ReWOO 计划是"静态"的一发发就不再根据观察调整.

> Directives de l'Anthropic 2024: du plus simple des débuts. Si une tâche est un outil, utilisez un résumé, ne construisez pas ReWOO.

## Construisez-le et mettez-le en œuvre.

> ️ **【易错点】**实现 ReWOO 时新手最常踩的坑: oublier le plan DAG faire le cycle de contrôle.`#E1`Je suis en train de faire ça.`#E2`La première`#E2`Il dépend aussi.`#E1`, , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , ,**后果**L'exécuteur est en train de se lever ou de se déployer.**一行修复**: pour la séquence suivante, vérifier si le nombre de points de séquence est égal au nombre total de points, non égal à la mise en balance`CycleDetectedError`Il y a une autre.
```figure
rewoo-plan
```

## Faites-le

`code/main.py`met en œuvre un jouet ReWOO:

> `code/main.py`实现一个玩具 ReWOO:

- `Planner` une politique scriptée qui émet un plan DAG à partir d'un prompt.
  Le mot grec traduit par " le mot grec "`Planner` From suggestion générer plan DAG 脚本策略──
- `Worker` envoie l'appel à l'outil de chaque nœud via le registre.
  Le mot grec traduit par " le mot grec "`Worker`                                                                                                                                                                                                                                                              
- `Solver` composition écrite qui lit les preuves et produit une réponse finale.
  Le mot grec traduit par " le mot grec "`Solver`                                                                                                                                                                                                                                                              
- Résolution de la dépendance  références comme `#E1`sont remplacés par des produits de travail antérieurs.
  Suivant le résultat de la recherche`#E1`Les citations sont remplacées par les précédentes.

La démo répond à "Quelle est la population de la capitale de la France, arrondie à des millions?" en utilisant un plan en deux étapes: (1) rechercher la capitale, (2) rechercher la population, puis résoudre.

> 演示回答"La population de la capitale française est combien,四舍五入到百万?"

- Je vais le faire.

> 运行:

```
python3 code/main.py
```

La trace montre d'abord le plan complet, puis les résultats du travailleur, puis la composition du solveur.

> Le trajet montre d'abord le plan complet, puis le résultat du travail, enfin le résultat du résultat.

## Utilisez-le avec le cadre de réalisation

LangGraph envoie Plan-and-Execute comme recette (`create_react_agent`Pour ReAct, des graphiques personnalisés pour exécuter le plan). Les flux de CrewAI codent directement le schéma: vous définissez les tâches à l'avance et le DAG de Flow les exécute.

> LangGraph va planifier et exécuter comme un complément`create_react_agent`Utilisé pour ReAct, auto-défini pour planifier-exécuter) ――CrewAI's Flows  directement codé le modèle: vous pré-définissez les tâches,Flow DAG  exécuter les mêmes.

## Envoyez-le . Produit .

`outputs/skill-rewoo-planner.md`génère un plan DAG ReWOO à partir d'une demande d'utilisateur, donné un catalogue d'outils. Il valide le plan (acyclique, chaque référence résolue, chaque outil existe) avant de le remettre à un exécuteur.

> `outputs/skill-rewoo-planner.md`根据用户请求和工具目录生成 ReWOO 计划 DAG──它在转交给执行器之前验证计划(无环、每个引用已解析、每个工具存在)──

## Les exercices

1. L'exécution parallèle des travailleurs pour les nœuds de plan indépendants.
   Quel est le bénéfice d'une mise en œuvre de deux groupes de travail en même temps sur 6 points ?
2. Ajouter un nœud de réaménagement qui s'allume si un travailleur renvoie une erreur. Quelle est la plus petite modification à ReWOO qui le rend Plan-et-Execute ?
   Quel est le minimum de changement de plan et d'exécution ?
3. Remplacez`Planner`avec un petit modèle (classe 7B) et garder `Solver`Comparer la qualité de bout en bout  où la fraction échoue-t-elle ?
   Le modèle de la première ligne est un modèle de la première ligne.
4. Lisez la section 4 du document ReWOO sur la distillation des planificateurs.
   Le projet de réforme de l'équipe de formation de l'équipe de révision de l'équipe de révision de l'équipe de révision de l'équipe de révision de l'équipe de révision de révision de l'équipe de révision de révision de l'équipe de révision de révision de l'équipe de révision de révision de révision de l'équipe de révision de révision de révision de révision de révision de révision de révision de révision de révision de révision de révision de révision de révision de révision de révision de révision de révision de révision de révision de révision de révision de révision de révision de révision de révision de révision de révision de révision de révision de révision de révision de révision de révision de révision de révision de révision de révision de révision de révision de révision de révision de révision de révision de révision de révision de révision de révision de révision de révision de révision de révision de révision de révision de révision de révision de révision de révision de révision de révision de révision de révision de révision de révision de révision de révision de révision de révision de révision de révision de révision de révision de révision de révision de révision de révision de révision de révision de révision de révision de révision de révision de révision de révision de révision de révision de révision de révision de révision de révision de révision de révision de révision de révision de révision de révision de révision de révision de révision de révision de révision de révision de révision de révision de révision de révision de révision de révision de révision de révision de révision de révision de révision de révision de révision de révision de révision de révision de révision de révision de révision de révision de révision de révision de révision de révision de révision de révision de révision de ré ré ré ré révision de révision de ré ré ré ré ré ré ré ré ré ré ré ré ré ré ré ré ré ré ré
5. Le jouet est porté à la forme de la trajectoire du Plan-et-Act: le plan est une séquence, pas un DAG.
   Le plan est un processus plutôt que le DAG. Quels sont les changements qui ont eu lieu ?

## Les termes clés

| Term | What people say | What it actually means |
|------|-----------------|-----------------------|
| 术语 | 通俗说法 | 实际含义 |
| ReWOO | "Reasoning without observations" / "无观察推理" | Plan, then fetch evidence in parallel, then solve — no observations in the planning prompt / 先规划，再并行获取证据，最后求解——规划提示中不包含观察 |
| Plan-and-Execute | "LangChain's plan-execute pattern" / "LangChain 的计划-执行模式" | ReWOO with an optional replanner node after execution / 带可选重新规划节点的 ReWOO |
| Plan-and-Act | "Scaled plan-execute" / "扩展版计划-执行" | Explicit planner/executor split with synthetic plan training data for long-horizon tasks / 使用合成计划训练数据的长程任务显式规划器/执行器分离 |
| Evidence reference | "#E1, #E2, ..." / "证据引用" | Plan-node placeholder substituted with prior worker output at dispatch time / 计划节点占位符，在分派时替换为工作器输出 |
| Planner distillation | "Small planner, big executor" / "小规划器，大执行器" | Fine-tune a small model on planner traces from a large teacher / 用大模型的规划轨迹微调小模型 |
| Token efficiency | "Fewer round trips" / "更少往返" | 5x fewer tokens on HotpotQA vs ReAct in the paper / 论文中 HotpotQA 上比 ReAct 减少 5 倍 token |
| DAG executor | "Topological dispatcher" / "拓扑分派器" | Runs plan nodes in dependency order; parallel at each level / 按依赖顺序运行计划节点；每层可并行 |

## Encore une lecture

- [Xu et al., ReWOO: Decoupling Reasoning from Observations (arXiv:2305.18323)](https://arxiv.org/abs/2305.18323) le papier canonique
  Le récit de la rédaction de la Bible est un récit de la rédaction de la Bible.
- [Erdogan et al., Plan-and-Act (arXiv:2503.09572)](https://arxiv.org/abs/2503.09572) planificateur-exécuteur à l'échelle avec des plans synthétiques
  Plan et acte  usage synthé plan of élargissement édition规划器-执行器──
- [LangGraph Plan-and-Execute tutorial](https://docs.langchain.com/oss/python/langgraph/overview) la recette de base
  Le plan de long-graphe et l'exécution
- [Anthropic, Building Effective Agents](https://www.anthropic.com/research/building-effective-agents) Choisissez le modèle le plus simple qui fonctionne
  Traduction anglaise: Guide de l'anthropologue sur la construction d'un agent efficace pour choisir le mode de fonctionnement le plus simple.
