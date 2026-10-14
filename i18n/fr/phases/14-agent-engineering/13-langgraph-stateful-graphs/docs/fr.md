# LangGraph: Graphiques d'état et exécution durable
# Orchestration de graphes d'état  Exécution durable et points de contrôle

> L'agent est une machine d'état; les nœuds sont des fonctions; les bords sont des transitions; l'état est placé en checkpoint après chaque nœud. Résumez à partir de toute défaillance au dernier point de contrôle réussi. LangGraph est la référence 2026 pour ce modèle d'orchestration d'état à bas niveau.

> **【中文解读】**LangGraph est une référence à l'élaboration de l'élaboration de l'état de base de 2026 . L'agent est un état de fonctionnement; le point est une fonction; le côté est un transfert; l'état est immuable et chaque étape après le point de contrôle est conservé.

**Type:** Learn + Build | **类型:** 学习 + 构建
**Languages:** Python (stdlib) | **语言:** Python (标准库)
**Prerequisites:** Phase 14 · 01 (Agent Loop), Phase 14 · 12 (Workflow Patterns) | **前置知识:** Phase 14 · 01 (Agent 循环), Phase 14 · 12 (工作流模式)
**Time:** ~75 minutes | **时间:** ~75 分钟

## Objectifs d'apprentissage

- Décrivez le modèle de base de LangGraph: machine d'état avec état immuable, nœuds de fonction, bords conditionnels et points de contrôle post-étape.
  Le modèle central de LangGraph est le modèle de l'état de la fonction.
- Décrivez le modèle de base de LangGraph: machine d'état avec état typé, nœuds de fonction, bords conditionnels et points de contrôle post-nœud.
- Nombre des quatre capacités que les documents mettent en évidence: exécution durable, streaming, humain-in-the-loop, mémoire complète.
  Le récit de la première partie de la Bible est le récit de la première partie de la Bible.
- Expliquez les trois topologies d'orchestration que LangGraph prend en charge: superviseur, peer-to-peer (swarm), hiérarchique (subgraphes nidifiés).
  Le langgraphe est un schéma de programmation de l'ensemble des groupes.
- Implémenter un graphique d'état stdlib avec un état immuable, des bords conditionnels et un cycle de contrôle/résumé.
  Le tableau de l'état du cycle de rétablissement est utilisé pour réaliser un état indéfectible.
- Implémenter un graphique d'état stdlib avec l'état typé, les bords conditionnels et un cycle de contrôle/résumé.

## Le problème , l' introduction du problème

Les agents et les flux de travail partagent un problème: lorsqu'une mise en œuvre de 40 étapes échoue à l'étape 38, vous voulez reprendre à partir de l'étape 38, et non recommencer.

> Agent 和工作流共享一个问题: Lorsque 40 étapes de fonctionnement dans la 38e étape échouent, vous voulez récupérer de la 38e étape plutôt que de commencer.

La réponse de conception de LangGraph: l'état est un objet de première classe, les mutations sont explicites et les points de contrôle persistent après chaque nœud.`load_state(session_id)`Je vous appelle.

> Réponse de conception de LangGraph: l'état est un objet de type civil égal, les changements sont évidents, les points de contrôle sont maintenus après chaque nœud.`load_state(session_id)`Il y a une autre.

> **【中文解读】**L'agent et le flux de travail partagent un problème: lorsque 40 étapes de fonctionnement échouent à la 38e étape, vous voulez récupérer à partir de la 38e étape plutôt que de commencer à partir de zéro.`load_state(session_id)`Il y a une autre.

> **【拓展：LangGraph → 状态图编排】**LangGraph est une référence de l'élaboration de l'élaboration de l'état de base de 2026 . Il va être utilisé à grande échelle dans la production de l'élaboration de l'élaboration de l'élaboration de l'élaboration de l'élaboration de l'élaboration de l'élaboration de l'élaboration de l'élaboration de l'élaboration de l'élaboration de l'élaboration de l'élaboration de l'élaboration de l'élaboration de l'élaboration de l'élaboration de l'élaboration de l'élaboration de l'élaboration de l'élaboration de l'élaboration de l'élaboration de l'élaboration de l'élaboration de l'élaboration de l'élaboration de l'élaboration de l'élaboration de l'élaboration de l'élaboration de l'élaboration de l'élaboration de l'élaboration de l'élaboration de l'élaboration de l'élaboration de l'élaboration de l'élaboration de l'élaboration de l'élaboration de l'élaboration de l'élaboration de l'élaboration de l'élaboration de l'élaboration de l'élaboration de l'élaboration de l'élaboration de l'élaboration de l'élaboration de l'élaboration de l'élaboration de l'élaboration de l'élaboration de l'élaboration de l'élaboration de l'élaboration de l'élaboration de l'élaboration de l'élaboration de l'élaboration de l'élaboration de l'élaboration de l'élaboration de l'élaboration de l'élaboration de l'élaboration de l'élaboration de l'élaboration de l'élaboration de l'élaboration de l'élaboration de l'élaboration de l'élaboration de l'élaboration de l'élaboration de l'élaboration de l

>  **【前置】**Il faut d'abord comprendre:Phase 14·01 (Agent Loop) et Phase 14·12 (Anthropic Workflow Patterns) Langgraph c'est la "version durable" du mode de travail.

## Le concept de base.

### Le graphique

Un graphique est défini par: Un dicté typé (ou modèle Pydantic) que chaque nœud lit et mutent.

> 图由以下定义:一个每个节点都读写的带类型 dict (图由以下定义:一个每个节点都读写的带类型 dict) 

- **Nodes.**Des fonctions pures`(state) -> state_update`Les mises à jour sont fusionnées dans l'état après leur retour.
  Le mot grec traduit par " le mot grec "**节点。**纯函数 `(state) -> state_update`◊ Actualisation dans le retour après la fusion dans l'état.
- **Edges.**Transitions conditionnelles ou directes entre les nœuds.
  Le mot grec traduit par " le mot grec "**边。**节点之间的条件或直接转换──
- **Entry and exit.** `START`et `END`Les nœuds de sentinelle marquent la frontière.
  Le mot grec traduit par " le mot grec "**入口和出口。** `START`et `END`Le poste de garde a été marqué.

> **【中文解读】**Le diagramme de LangGraph est défini par trois éléments: 1) type d'état chaque section de lecture de la carte 模型; 2) 节点 pure fonction `(state) -> state_update`, retourner la valeur à l'état; 3) conditions entre les points de bord ou transfert direct

Exemple: un agent avec `classify`- Je suis là .`refund`- Je suis là .`bug`- Je suis là .`sales`- Je suis là .`done`les nœuds  un flux de travail de routage en tant que graphique.

> Example: une contenu `classify`- Je suis là.`refund`- Je suis là.`bug`- Je suis là.`sales`- Je suis là.`done`节点的代理路由工作流作为图──

### Exécution durable

Après chaque nœud retourne, le runtime sérialise l'état et l'écrit à un point de contrôle (SQLite, Postgres, Redis, personnalisé).`resume(session_id)`et reprendre à partir de l'étape N + 1 avec l'état exact.

> Chaque nœud retourne après, fonctionnement en état de séquence et écrit dans le point de contrôle de l'appareil.`resume(session_id)`Il n'y a pas de phase N+1 avec l'état précis continu.

Les documents LangGraph mettent explicitement en évidence les utilisateurs de production où cela compte: Klarna, Uber, JP Morgan.

>  **【类比】**Le point de contrôle de LangGraph est comme le jeu de "auto-archivage": chaque tranche de connexion est automatiquement enregistrée une fois. Le chef de la branche 38 est suspendu, vous n'avez pas besoin de passer du premier tranche de connexion à la branche 37 pour continuer à passer.`resume(session_id)`Je suis en train de faire ça.

> LangGraph 文档 文档 文档 文档 文档 文档 文档 文档 文档 文档 文档 文档 文档 文档 文档 文档 文档 文档 文档 文档 文档 文档 文档 文档 文档 文档 文档 文档 文档 文档 文档 文档 文档 文档 文档 文档 文档 文档 文档 文档 文档 文档 文档 文档 文档 文档 文档 文档 文档 文档 文档 文档 文档 文档 文档 文档 文档 文档 文档 文档 文档 文档 文档 文档 文档 文档 文档 文档 文档 文档 文档 文档 文档 文档 文档 文档 文档 文档 文档 文档 文档 文档 文档 文文档 文文文文档 文文文文文文文文文文文文文文文文文文文文文文文文文文文文文文文文文文文文文文文文文文文文文文文文文文文文文文文文文文文文文文文文文文文文文文文文文文文文文文文文文文文文文文文文文文文文文文文文文文文文文文文文文文文文文文文文文文文文文文文文文文文文文文文文文文文文文文文文文文文文文文文文文文文文文文文文文文文文文文文文文文文文文文文文文文文文文文文文文文文文文文文文文文文文文文文文文文文文文文文文文文文文文文文文文文文文文文文文文文文文文文文文文文文文文文文文文文文文文文文文文文文文文文文

### Retour en continu

Chaque nœud peut produire une sortie partielle. Le graphique transmet des événements par nœud-delta à l'appelant afin que les UI soient mis à jour au fur et à mesure que le graphique fonctionne.

> Chaque nœud peut générer une partie de sortie.

### Les humains dans le cycle

Inspecter et modifier l'état entre les nœuds. Implémentations: pause avant un nœud critique, état de surface à un humain, accepter les modifications, reprendre. Le point de contrôle le rend facile parce que l'état est déjà sérialisé.

> Le système de contrôle et de révision entre les nœuds.

### La mémoire

À court terme (dans un cours  histoire de conversation dans l'état) et à long terme (à travers les cours  persistant via le point de contrôle plus un magasin à long terme séparé). LangGraph s'intègre avec des systèmes de mémoire externes (Mem0, personnalisé) via des outils.

> 短期 (→ une seule opération dans un état de dialogue) et longue durée (→ une seule opération) 跨运行 (→ une seule opération) 通过检查点器加独立长期储存持久化)  长图 通过工具与外部记忆系统 (→ un seul processus) 长期 (→ une seule opération) 长期 (→ une seule opération) 长期 (→ une seule opération) 长期 (→ une seule opération) 长期 (→ une seule opération) 长期 (→ une seule opération) 长期 (→ une seule opération) 长期 (→ une seule opération) 长期 (→ une seule opération) 长期 (→ une seule opération) 长期 (→ une seule opération) 长期 (→ une seule opération) 长期 (→ une seule opération) 长期 (→ une seule opération) 长期 (→ une seule opération) 长期 (→ une seule opération) 长期 (→ une seule opération) 长期) 长期 (→ une seule opération) 长期 (→ une seule opération) 长期) 长期 (→ une seule opération) 长期) 长期 (→ une seule opération) 长期 (→ une seule opération) 长期) 长期 (→

### Trois topologies

1. **Supervisor.**Le routeur central LLM envoie des subagents spécialisés. `create_supervisor()`dans `langgraph-supervisor`(bien que l'équipe de LangChain en 2026 recommande de le faire via des appels à l'outil directement pour plus de contrôle de contexte).
   Le mot grec traduit par " le mot grec "**监督者。**Entraîneur spécialisé en médecine
2. **Swarm / peer-to-peer.**Les agents se détachent directement via une surface d'outils partagée.
   Le mot grec traduit par " le mot grec "**群体/点对点。**L'agent 通过共享工具接口直接移交――无中央路由―― est un agent qui est un agent de communication.
3. **Hierarchical.**Superviseurs gérant des sous-superviseurs, mis en œuvre sous forme de sous-graphes encastrés.
   Le mot grec traduit par " le mot grec "**层次化。**监督者管理子监督者, réalisé pour嵌套子图──

### Où ce modèle va mal

> ️ **【易错点】**Le plus souvent, les défaites sont les suivantes:`datetime.now()`Ou au fur et à mesure, ces valeurs changent à la reprise.**后果**Après le point de contrôle, le point de réécration est effectué différemment de l'origine, l'ensemble du système entra dans le chaos.**一行修复**Toutes les sources incertaines (temps, temps, temps, API) doivent être capturées dans l'état, les fonctions de l'élément doivent être lues dans l'état et non directement modifiées.`datetime.now()`Il y a une autre.

- **Checkpoints too small.**Seule la conversation de point de contrôle tourne laissant l'état de l'outil et la mémoire écrit non récupérable.
  Le mot grec traduit par " le mot grec "**检查点太小。**                                                                                                                                                                                                                                                              
- **Non-deterministic nodes.**Le résumé suppose que les entrées de nœud produisent la même mise à jour d'état.
  Le mot grec traduit par " le mot grec "**非确定性节点。**恢复假设节点输入产生相同状态更新──随机种子、挂钟时间、外部API 必须被捕──
- **Over-use of conditional edges.**Un graphique avec chaque bord conditionnel est une machine d'état qui ne peut être raisonnable.
  Le mot grec traduit par " le mot grec "**过度使用条件边。**Chaque ligne est une chaîne de chaîne à chaîne à chaîne à chaîne à chaîne à chaîne à chaîne à chaîne à chaîne à chaîne à chaîne à chaîne à chaîne à chaîne à chaîne à chaîne.

> 🤔 **【困惑】**Q: 三种拓(superviseur、swarm、hierarchical) jusqu'où dois-je choisir lequel ?**任务可分解为独立角色**(如客服/退款/技术) - superviseur de choix;**Agent 之间是协作关系而非派发关系**(如辩、相互 review) Choisir le swarm;**任务有天然层次结构**(comme "produit line A 下分 5 个团队") sélection hiérarchique。 LongChain 团队 2026 年建议:能直接用工具调用解决就别上监督直接工具调用上下文控制更精细──

## Construisez-le en main
```figure
langgraph-state
```

## Faites-le

`code/main.py`met en œuvre un graphique d'état stdlib:

> `code/main.py`Utilisation de la base de données:

- `State` un dicton avec`messages`- Je suis là .`step`- Je suis là .`route`- Je suis là .`output`- Je suis là .`human_approval`- Je suis désolé .
  Le mot grec traduit par " le mot grec "`State`包含 `messages`- Je suis là.`step`- Je suis là.`route`- Je suis là.`output`- Je suis là.`human_approval`Le type de dicton.
- `Node` appel à l'état de prise et à la restitution d'un dicton de mise à jour.
  Le mot grec traduit par " le mot grec "`Node` accepter l'état et retourner à l'objet modifiable de la commande 
- `StateGraph` nœuds + bordes + bordes conditionnelles + exécution + CV.
  Le mot grec traduit par " le mot grec "`StateGraph`节点 + 边 + 条件边 + 运行 + 恢复。
- `SQLiteCheckpointer`(fals en mémoire)  sérialise l' état après chaque nœud; `load(session_id)`- Il est en train de restaurer.
  Le mot grec traduit par " le mot grec "`SQLiteCheckpointer`(内存模拟)  État de séquestration après chaque point;`load(session_id)`La réparation
- Un graphique de démonstration: classer -> branche(refund / bug / ventes) -> porte humaine -> envoyer.
  Le code de la page de référence est le code de la page de référence.

- Je vais le faire.

> 运行:

```
python3 code/main.py
```

La trace montre la première course échouant à la porte humaine, persistance, puis reprendre à produire la sortie finale.

> Le premier fonctionnement dans le domaine de contrôle humain a échoué, s'est perpétué, puis a repris et produit une sortie finale.

## Utilisez-le avec le cadre de réalisation

- **LangGraph** la référence, prête à la production.`create_react_agent`- Je suis là .`create_supervisor`, ou construire votre propre graphique.
  Le mot grec traduit par " le mot grec "**LangGraph**参考实现,生产就绪──使用 `create_react_agent`- Je suis là.`create_supervisor`Ou construire son propre dessin.
- **AutoGen v0.4**(Létion 14)  Modèle de l'acteur alternative pour les scénarios à forte concurrence.
  Le mot grec traduit par " le mot grec "**AutoGen v0.4**(第 14 课) 高并发场景的演员 模型替代方案──
- **Claude Agent SDK**(Léction 17)  Harness géré avec magasin de session intégré.
  Le mot grec traduit par " le mot grec "**Claude Agent SDK**(第 17 课) 带内置会话存储的托管框架──
- **Custom** lorsque vous avez besoin d'un contrôle exact sur la forme de l'état ou le backend du point de contrôle.
  Le mot grec traduit par " le mot grec "**自定义** lorsque vous avez besoin de contrôle précis de l'état de forme ou de l'examen du point de contrôle à l'arrière-plan.

## Envoyez-le . Produit .

`outputs/skill-state-graph.md`génère un graphique d'état en forme de LangGraph dans n'importe quel temps d'exécution cible avec le point de contrôle et le CV câblé.

> `outputs/skill-state-graph.md`Générer des diagrammes d'état de LangGraph en fonction de l'objectif, des points de contrôle et de récupération intégrés.

## Les exercices

1. Ajouter une limite conditionnelle à partir de `classify`à `end`Lorsque la confiance de la classification est inférieure à un seuil, reprenez la course après un ensemble humain.`route`manuellement.
   Traduction anglaise: quand la confiance est inférieure à la valeur ajoutée`classify`À la`end`Les conditions sont différentes.`route`后恢复运行──
2. Échangez le faux SQLite contre un vrai point de contrôle SQLite.
   Le code de calcul est un code de calcul qui est utilisé pour calculer les données de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur.
3. Implémenter des bords parallèles: deux nœuds fonctionnent simultanément, fusionner par un réducteur personnalisé.
   Deux nœuds et deux opérations, avec un réducteur de définition automatique 合并── état inconstant ici?
4. Lire `langgraph-supervisor`- Remplacez le jouet à`create_supervisor`- Comparer les traces.
   Le mot grec traduit par " le "`langgraph-supervisor`参考──将玩具移植为 `create_supervisor`◊ Comparer les traces de la situation
5. Ajouter le flux: chaque nœud produit un état partiel pendant son exécution.
   Chaque élément de la circulation est en train de produire un état.

## Les termes clés

| Term | What people say | What it actually means |
|------|-----------------|-----------------------|
| 术语 | 通俗说法 | 实际含义 |
| State graph | "Agent as state machine" / "Agent 即状态机" | Typed state + nodes + edges + reducers / 带类型状态 + 节点 + 边 + reducer |
| Checkpointer | "Persistence backend" / "持久化后端" | Serializes state after every node; enables resume / 每个节点后序列化状态；支持恢复 |
| Reducer | "State merger" / "状态合并器" | Function that combines current state with a node's update / 将当前状态与节点更新合并的函数 |
| Conditional edge | "Branch" / "分支" | Edge chosen by a function of state / 由状态函数选择的边 |
| Subgraph | "Nested graph" / "嵌套图" | A graph used as a node inside another graph / 作为另一个图内节点使用的图 |
| Durable execution | "Resume from failure" / "从失败恢复" | Restart at the last successful node with exact state / 在最后成功节点处用精确状态重启 |
| Supervisor | "Router LLM" / "路由 LLM" | Central dispatcher for specialist subagents / 专家子 Agent 的中央分派器 |
| Swarm | "P2P agents" / "P2P Agent" | Agents hand off via shared tools; no central router / Agent 通过共享工具移交；无中央路由 |

## Encore une lecture

- [LangGraph overview](https://docs.langchain.com/oss/python/langgraph/overview) les documents de référence
  Le langage est le langage de la langue.
- [langgraph-supervisor reference](https://reference.langchain.com/python/langgraph/supervisor/) API de modèle de surveillance
  Le langgraph-supervisor est un superviseur de l'API.
- [AutoGen v0.4, Microsoft Research](https://www.microsoft.com/en-us/research/articles/autogen-v0-4-reimagining-the-foundation-of-agentic-ai-for-scale-extensibility-and-robustness/) Modèle alternatif pour les acteurs
  Le modèle de l'équipe de développement de l'équipe de développement de l'équipe de développement de l'équipe de développement de l'équipe de développement de l'équipe de développement de l'équipe de développement de l'équipe de développement de l'équipe de développement de l'équipe de développement de développement de l'équipe de développement de l'équipe de développement de l'équipe de développement de l'équipe de développement de l'équipe de développement de développement de l'équipe de développement de l'équipe de développement de développement de l'équipe de développement de développement de l'équipe de développement de développement de l'équipe de développement de développement de l'équipe de développement de développement de l'équipe de développement de développement de développement de l'équipe de développement de développement de développement de l'équipe de développement de développement de développement de l'équipe de développement de développement de développement de développement de l'équipe de développement de développement de développement de développement de développement de l'équipe de développement de développement de développement de développement de développement de l'équipe de développement de développement de développement de développement de développement de développement de développement de développement de l'équipe de développement de développement de développement de développement de développement de développement de développement de développement.
- [Claude Agent SDK overview](https://platform.claude.com/docs/en/agent-sdk/overview) magasin de séances et sous-bagages
  Le président de la République a déclaré que la décision de la Commission européenne de la protection des données et de l'environnement avait été prise en application de la loi.
