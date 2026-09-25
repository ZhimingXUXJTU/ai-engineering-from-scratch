# LangGraph  Machines d'État pour les agents  LangGraph: état de l'agent
# Machines de l'État agencées  Graphes, nœuds, points de contrôle

> Une boucle ReAct écrite à la main est une `while True`La même boucle écrite comme un graphique explicite est quelque chose que vous pouvez contrôler, interrompre, brancher, et voyager dans le temps.

> **【中文解读】**Le cycle de réaction est un.`while True` Le cycle de réaction écrit avec LangGraph est un diagramme que l'on peut examiner à la place de la conservation, de la interruption, de la fraction de l'écoulement, du temps de voyage.

> **【拓展：LangGraph→Agent工程】**LangGraph est actuellement le cadre d'agence le plus mature, l'agent le plus performant, le plus efficace et le plus efficace.

>  **【前置】**Pour les autres, il est nécessaire de prendre en compte les caractéristiques de la fonctionnalité de la fonctionnalité.`langgraph`- Je suis là.`langchain-core`Il y a une autre.

**Type:** Build | **类型:** 构建
**Languages:** Python | **语言:** Python
**Prerequisites:** Phase 11 · 09 (Function Calling), Phase 11 · 14 (Model Context Protocol) | **前置知识:** Phase 11 · 09 (函数调用)、14 (模型上下文协议)
**Time:** ~75 minutes | **时间:** ~75 分钟

## Le problème , l' introduction du problème

Vous envoyez un agent qui appelle à la fonction. Il fonctionne pendant trois tours, puis quelque chose ne va pas: le modèle essaie un outil qui rend 500, l'utilisateur change d'avis au milieu de la tâche, ou l'agent décide de rembourser une commande sans qu'un humain signe.`while True:`Vous ne pouvez pas le faire pauser, vous ne pouvez pas le faire retourner, et vous ne pouvez pas brancher en "et si le modèle avait choisi l'autre outil".

> Vous publiez une fonction pour appeler l'agent. Elle a travaillé trois fois, puis il y a un problème: le modèle tente un retour 500 outils, l'utilisateur change d'avis ou l'agent décide de rembourser sans signature artificielle.`while True:`Vous ne pouvez pas le suspendre, le revenir, ou le brancher à "Si le modèle choisit un autre outil, comment ça va se passer ?" Une fois que vous publiez une démo de ce genre, l'agent devient une boîte noire.

La prochaine étape est évidente une fois que vous la voyez. L'agent est déjà une machine d'état  système prompt plus l'historique des messages plus les appels d'outil en attente plus l'action suivante. Faites expliciter la machine d'état: les nœuds pour "le modèle pense", "un outil fonctionne", "un humain approuve", et les bords pour les transitions conditionnelles entre eux. Une fois le graphique explicite, le harnais obtient quatre choses gratuitement: le point de contrôle (état de sauvegarde entre les étapes), les interruptions (pause pour un humain), le streaming (tokens de flux et événements intermédiaires) et le voyage dans le temps (retour à un état précédent et essayez une branche différente).

> Une fois que vous avez vu, l'étape suivante est évidente. L'agent lui-même est un état de machine.

LangGraph est la bibliothèque qui envoie cette abstraction. Ce n'est pas un cadre d'agent au sens de LangChain (" ici il y a un AgentExecutor, bonne chance "). C'est un graphique de temps d'exécution avec état de première classe, persistance de première classe et interruptions de première classe.
La mise en œuvre de référence de cette abstraction est LangGraph. Ce n'est pas un cadre d'agent au sens de LangChain (" ici il y a un AgentExecutor, bonne chance "). C'est un graphe runtime avec état de première classe, persistance de première classe et interruptions de première classe. La boucle d'agent est quelque chose que vous dessinez, pas quelque chose que vous écrivez à la main.

> LangGraph est une base de données abstraite. Il n'est pas un cadre d'agent au sens de LangChain. Il est un cadre de statut civil égal, de stabilité citoyenne égale et de interruption citoyenne égale.


> **【中文解读】**L'avantage central de LangGraph est de soutenir un courant de contrôle complexe: cycle (Agent rencontre une erreur en temps de réessayer) 条件分支 (en fonction du type de tâche choisie différents outils) 人工审批 (en fonction de l'opération de type LangGraph) 高风险操作需要人工确认 (en fonction de l'opération de réessayer) 简单的 LangChain Chain 无法表达这些复杂逻辑──

>  **【类比】**Le long graphe est un schéma de processus de peinture qui est en train de disparaître. Il est possible de vérifier le point de conservation.

> ️ **【易错点】**LangGraph's 3 个坑: 1)**状态 schema 太松散**用 `dict`Quand l'état 没类型约束,运行时关键 拼错发现不了;用 `TypedDict`Ou modèle pydantique  définir l'état。(2) **条件边写得太复杂** un bord 函数里 if/other 嵌套 5 层,调试地狱; décomposer en plusieurs simples bord 函数, chaque retour en un seul节点名──(3) **checkpoint 用 SQLite 不持久化** Réclencher le service perdu; produire avec Postgres ou Redis faire un point de contrôle。


## Le concept de base.

> **【中文解读】**LangGraph va utiliser l'agent de LLM pour établir un état de machine: définir un état de l'agent de l'agent de l'agent de l'agent de l'agent de l'agent de l'agent de l'agent de l'agent de l'agent de l'agent de l'agent de l'agent de l'agent de l'agent de l'agent de l'agent de l'agent de l'agent de l'agent de l'agent de l'agent de l'agent de l'agent de l'agent de l'agent de l'agent de l'agent de l'agent de l'agent de l'agent de l'agent de l'agent de l'agent de l'agent de l'agent de l'agent de l'agent de l'agent de l'agent de l'agent de l'agent de l'agent de l'agent de l'agent de l'agent de l'agent de l'agent de l'agent de l'agent de l'agent de l'agent de l'agent de l'agent de l'agent de l'agent de l'agent de l'agent de l'agent de l'agent de l'agent de l'agent de l'agent de l'agent de l'agent de l'agent de l'agent de l'agent de l'agent de l'agent de l'agent de l'agent de l'agent de l'agent de l'agent de l'agent de l'agent de l'agent de l'agent de l'agent de l'agent de l'agent de l'agent de l'agent de l'agent de l'agent de l'agent de l'agent de l'agent de l'agent de l'agent de l'agent de l'agent de l'agent de l'agent de l'agent de l'agent de l'agent de l'agent de l'agent de l'agent de l'agent de l'agent de l'agent de l'agent de l'agent de l'agent de l'agent de l'agent de l'agent de l'agent de l'agent de l'agent de l'agent de l'agent de l'agent de l'agent de l'agent de l'agent de l'agent de l'agent de l'

> **【拓展：LangGraph 与 Agent 编排】**LangGraph est un cadre de coordination de l'équipe lancé par LangChain, supporté par:多 Agent 协作、人工介入(Human-in-the-loop) 持久化状态、时间旅行调试――与 CrewAI (Agent de rôle) et AutoGen (Agent de rôle) 多 Agent对话)


![LangGraph StateGraph: nodes, edges, and the checkpointer](../assets/langgraph-stategraph.svg)

Une .`StateGraph`Il y a trois choses.

> `StateGraph`Il y a trois choses.

1. **State.**Un dicté typé (TypedDict ou modèle Pydantic) qui circule à travers le graphique. Chaque nœud reçoit l'état complet et renvoie une mise à jour partielle, que LangGraph fusionne en utilisant un *réducteur* par champ `operator.add`pour les listes qui devraient s'accumuler, écraser par défaut.
   **状态。**流過图的类型化字典──每个节点接收完整状态并返回部分更新──
2. **Nodes.**Fonctions Python `state -> partial_state`Chacun est une étape discrète: "appeler le modèle", "exécuter des outils", "récapituler".
   **节点。**Python 函数 `state -> partial_state`                                                                                                                                                                                                                                                              
3. **Edges.**Les tranches entre les nœuds. Les bords statiques vont à un endroit. Les bords conditionnels prennent une fonction de routeur`state -> next_node_name`Donc le graphique peut se brancher sur la sortie du modèle.
   **边。**节点之间的转换──静态边去一个地方──条件边接受路由函数以在模型输出上分支──

Vous compilez le graphique. Compile lie la topologie, attache un point de contrôle (optionnel mais essentiel pour la production), et renvoie un fonctionnable. Vous l'invoquez avec un état initial et un`thread_id`Chaque étape de l' exécution est un point de contrôle à clé .`(thread_id, checkpoint_id)`- Je suis désolé .

> Vous avez utilisé un objet opérationnel et vous avez utilisé un objet opérationnel.`thread_id`Chaque étape de l'exécution sera perpétuée par un point de contrôle.

### Les quatre superpuissances

**Checkpointing.**Chaque transition de nœud écrit le nouvel état dans un magasin (en mémoire pour les tests, Postgres/Redis/SQLite pour prod).`thread_id`Le graphique reprend son parcours.

> **检查点。**Chaque nœud transfert sera écrit dans le stockage en utilisant le même.`thread_id`Re-utiliser le tableau pour récupérer.

**Interrupts.**Marquez un nœud avec `interrupt_before=["human_review"]`L'API répond à l'utilisateur avec "attendant l'approbation". Une demande ultérieure à la même `thread_id`avec `Command(resume=...)`reprend l'exécution.

> **中断。**- Je veux le faire .`interrupt_before`标记一个节点,执行在该节点运行前停止――状态被持久化――后续请求可恢复执行――

**Streaming.** `graph.stream(state, mode="updates")`Les zones de delta sont en train de se produire.`mode="messages"`Les jetons LLM sont diffusés à l'intérieur des nœuds du modèle. `mode="values"`Vous choisissez ce qui doit apparaître dans votre interface.

> **流式输出。** `graph.stream`按发生顺序产出状态增量──你选择在 UI 中显示什么──

**Time-travel.** `graph.get_state_history(thread_id)`renvoie le journal complet du point de contrôle.`checkpoint_id`à `graph.invoke`C'est un bon moyen de débogage ("et si le modèle avait choisi l'outil B à la place?") et pour les tests de régression qui reproduisent les traces de production.

> **时间旅行。**Retourner à l'ensemble du dossier.`checkpoint_id`Tu es à la recherche de la réponse.

### Les réducteurs sont le point

Chaque champ d'état a un réducteur. La plupart des paramètres sont bons  une nouvelle valeur surpasse l'ancienne. Mais les listes de messages doivent `operator.add`Les deux nœuds sont mis à jour par la même méthode.`messages`et vous avez oublié le `Annotated[list, add_messages]`Le réducteur est la seule chose subtile dans la bibliothèque; faites-le bien et le reste se compose.

> Chaque section de l'état a un réducteur.`operator.add`Pour ajouter de nouvelles nouvelles nouvelles plutôt que de les remplacer. Le réducteur est la seule chose minuscule de cette collection.

### Le graphique ReAct en quatre nœuds

Un agent ReAct de production est constitué de quatre nœuds et de deux bords:

> Un agent réactif de production est quatre éléments et deux parties:

1. `agent` appelle le LLM avec l'historique de message actuel. Retourne le message assistant (qui peut contenir tool_calls).
2. `tools` exécute tous les appels tool_calls dans le dernier message assistant, ajoute les résultats de l'outil comme messages d'outil.
3. Un bord conditionnel de `agent`qui se dirige vers `tools`si le dernier message contient des appels à outils, sinon `END`- Je suis désolé .
4. Un bord statique de `tools`Retour à `agent`- Je suis désolé .

Vous obtenez la boucle ReAct complète (Pensement → Action → Observation → Pensement → ...) avec point de contrôle, interrompt et streaming, en environ 40 lignes de code.

> C'est ainsi que tu as obtenu un cycle complet de réaction, avec un point de contrôle, une interruption et une sortie de courant, environ 40 pages de code.

### StateGraph vs Envoyer (fanout)

`Send(node_name, state)`L'agent décide de consulter trois récupérateurs à la fois.`Send`La méthode de LangGraph est de façon à exprimer le modèle orchestrateur-travailleur sans fil de primitives.

> `Send(node_name, state)`Faites un point de départ et faites un plan.`Send`生成目标节点的并行执行; leurs sorties sont effectuées par le réducteur d'état 合并──

### Les sous-graphes

Un graphique compilé peut être un nœud dans un autre graphique. Le graphique externe voit un seul nœud; le graphique interne a son propre état et ses propres points de contrôle. C'est ainsi que les équipes construisent des agents de travail supervisé: le graphique supervisé rote l'intention de l'utilisateur vers un sous-graphe de travail par domaine.

> Le tableau post-compilation peut être un nœud dans un autre tableau. Le tableau extérieur peut voir un nœud unique; le tableau intérieur a son propre état et son propre point de contrôle.

## Construisez-le et mettez-le en œuvre.
```figure
l5-state-graph-ledger
```

## Faites-le

### Étape 1: état et nœuds

> 步骤 1: état et point de départ

```python
from typing import Annotated, TypedDict
from langchain_core.messages import AnyMessage, HumanMessage, AIMessage
from langgraph.graph import StateGraph, END
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode
from langgraph.checkpoint.memory import MemorySaver

class State(TypedDict):
    messages: Annotated[list[AnyMessage], add_messages]

def agent_node(state: State) -> dict:
    response = llm.invoke(state["messages"])
    return {"messages": [response]}

def should_continue(state: State) -> str:
    last = state["messages"][-1]
    return "tools" if getattr(last, "tool_calls", None) else END

tool_node = ToolNode(tools=[search_web, read_file])

graph = StateGraph(State)
graph.add_node("agent", agent_node)
graph.add_node("tools", tool_node)
graph.set_entry_point("agent")
graph.add_conditional_edges("agent", should_continue, {"tools": "tools", END: END})
graph.add_edge("tools", "agent")

app = graph.compile(checkpointer=MemorySaver())
```

`add_messages`est le réducteur qui fait accumuler la liste de messages au lieu de la supprimer.

> `add_messages`C'est le réducteur de l'accumulation de la liste de messages et non de la couverture.

### Étape 2: courir avec un fil

> 步骤 2: Avec le train de la route

```python
config = {"configurable": {"thread_id": "user-42"}}
for event in app.stream(
    {"messages": [HumanMessage("find the Anthropic headquarters address")]},
    config,
    stream_mode="updates",
):
    print(event)
```

Chaque mise à jour est un dicton .`{node_name: state_delta}`Votre frontend peut les transmettre à l'interface utilisateur pour que les utilisateurs voient "l'agent pense... appelant search_web... a obtenu le résultat... répondant".

> Chaque mise à jour est `{node_name: state_delta}`字典──前端可流式传到 UI,让用户看到"agent 思考中... 调用 search_web... 得到结果... 回答中"──

### Étape 3: ajouter une interruption humaine en boucle

Marquez un nœud pour que l'exécution s'arrête avant son exécution.

> 步骤 3: Additional人机协作中断──标记节点使执行在运行前暂停──

```python
app = graph.compile(
    checkpointer=MemorySaver(),
    interrupt_before=["tools"],  # pause before every tool call
)

state = app.invoke({"messages": [HumanMessage("delete the production database")]}, config)
# state["__interrupt__"] is set. Inspect proposed tool calls.
# If approved:
from langgraph.types import Command
app.invoke(Command(resume=True), config)
# If denied: write a rejection message and resume
app.update_state(config, {"messages": [AIMessage("Blocked by human reviewer.")]})
```

L'état, le point de contrôle et le fil persistent tout au long de l'interruption.

> 状态、检查点和线程在中断期间全部持久化──除了执行期间, rien n'est en cache──

### Étape 4: Voyage dans le temps pour débogage

> 步骤 4: réinitialiser le temps de voyage.

```python
history = list(app.get_state_history(config))
for snapshot in history:
    print(snapshot.values["messages"][-1].content[:80], snapshot.config)

# Fork from a prior checkpoint
target = history[3].config  # three steps back
for event in app.stream(None, target, stream_mode="values"):
    pass  # replay from that point forward
```

Passer par là`None`Lorsque l'entrée se reproduit à partir du point de contrôle donné, en passant une valeur, elle est ajoutée comme une mise à jour de l'état de ce point de contrôle avant de reprendre.

> - Je suis là .`None` comme entrée de la réinstallation d'un point de contrôle donné;  comme entrée avant la récupération, elle est ajoutée à l'état du point de contrôle .

### Étape 5: échangez le point de contrôle pour la production

> 步骤 5: production environnement remplacé inspection point de

```python
from langgraph.checkpoint.postgres import PostgresSaver

with PostgresSaver.from_conn_string("postgresql://...") as checkpointer:
    checkpointer.setup()
    app = graph.compile(checkpointer=checkpointer)
```

SQLite, Redis et Postgres sont expédiés.`MemorySaver`Tout ce qui persiste à travers les redémarrages veut un vrai magasin.

> SQLite、Redis 和 Postgres 已提供──`MemorySaver`Tout ce qui a besoin de réinitialisation a besoin d'un véritable stockage.

## La compétence

> Vous construisez des agents comme des graphiques, pas comme `while True`- Les boucles.
> Vous avez construit un agent pour vous, et non pas pour vous.`while True`Le cycle

Avant de toucher LangGraph, faites une conception de 60 secondes:

> Avant d'utiliser LangGraph, faites un design de 60 secondes:

1. **Name the nodes.**Chaque décision discrète ou action secondaire est un nœud. " L'agent pense, " " l'outil fonctionne, " " l'examenateur approuve, " " les flux de réponse. " Si vous ne pouvez pas les énumérer, la tâche n'est pas encore en forme d'agent.
   **命名节点。**Chaque décision de séparation ou action secondaire est un point.
2. **Declare the state.**Type minimal avec un réducteur pour chaque champ de liste.`messages`; les champs spécifiques à la tâche de levage (un travail `plan`, une `budget`le compteur, un `retrieved_docs`Liste) au niveau supérieur.
   **声明状态。**Le plus petit typeDict, chaque section de liste a un réducteur.
3. **Draw the edges.**La fonction de routeur est statique, sauf si l'étape suivante dépend de la sortie du modèle.
   **画边。**À moins que l'étape suivante ne soit basée sur le modèle de sortie, ou utilisez le côté statique.
4. **Choose a checkpointer up front.** `MemorySaver`Pour les tests, Postgres/Redis/SQLite pour tout autre.
   **提前选择检查点器。**测试用 `MemorySaver`, autres usages Postgres/Redis/SQLite
5. **Decide interrupts before tools run, not after.**Les approbations vont sur le bord dans un nœud d'effet secondaire afin que vous puissiez annuler avant le dommage; la validation va sur le bord hors du modèle afin que vous puissiez rejeter les mauvaises appels à bas prix.
   **在工具运行之前决定中断，而不是之后。**
6. **Stream by default.** `mode="updates"`pour l'interface utilisateur, `mode="messages"`pour le streaming au niveau des jetons à l'intérieur des nœuds du modèle, `mode="values"`pour les instantanés complets pendant l'évaluation.
   **默认使用流式输出。**

Ne pas envoyer un agent LangGraph qui n'a pas de point de contrôle, ne pas envoyer un agent qui interrompt après l'effet secondaire, ne pas envoyer un agent LangGraph qui ne peut pas être utilisé.`messages`champ sans `add_messages`comme son réducteur.

>  refuse de publier aucun agent LangGraph du point de contrôle ∙ refuse de publier un agent interrompu après les effets secondaires ∙ refuse de publier aucun ∙`add_messages`作为减轻剂 的 `messages`Je suis en train de vous dire:

## Les exercices

1. **Easy.**Implémenter le graphique ReAct à quatre nœuds ci-dessus avec un outil de calculateur et un outil de recherche Web.`list(app.get_state_history(config))`retourne au moins quatre points de contrôle pour une conversation à deux tours.
   **简单。**实现上述四节点 ReAct 图,验证检查点历史记录──
2. **Medium.**Ajouter un `planner`Le nœud qui se déplace avant `agent`et écrit un article structuré `plan: list[str]`Je suis dans l'état.`agent`Marquer les étapes du plan comme faites.`plan`est perdu sur un CV du point de contrôle (réducteur incorrect).
   **中等。**J' ai une autre.`agent`之前运行的 `planner`节点, write in structured plan to state.
3. **Hard.**Construire un graphique de surveillance qui traverse trois sous-graphes (`researcher`- Je suis là .`writer`- Je suis là .`reviewer`) en utilisant `Send`Chaque sous-graphe a son propre état et son propre point de contrôle.`interrupt_before=["writer"]`Confirmer que le voyage dans le temps depuis un point de contrôle précédent ne refait que la branche fourchée.
   **困难。**Construire un superviseur 图, entre trois images `Send`Je suis là.

## Les termes clés

| Term | What people say | What it actually means | 中文释义 |
|------|-----------------|-----------------------|---------|
| StateGraph | "The LangGraph graph" / "LangGraph 图" | The builder object you add nodes and edges to before compile. | StateGraph：编译前添加节点和边的构建器对象 |
| Reducer | "How the field merges" / "字段如何合并" | A function `(old, new) -> merged` applied when a node returns an update for that field; default is overwrite, `add_messages` appends. | Reducer：节点返回更新时应用的合并函数 |
| Thread | "A conversation ID" / "对话 ID" | A `thread_id` string that scopes all checkpoints for one session. | Thread：限定一个会话所有检查点的 thread_id 字符串 |
| Checkpoint | "A paused state" / "暂停的状态" | A persisted snapshot of the full graph state after a node transition, keyed on `(thread_id, checkpoint_id)`. | Checkpoint：节点转换后持久化的完整图状态快照 |
| Interrupt | "Pause for a human" / "暂停等人工" | `interrupt_before` / `interrupt_after` stop execution at a node boundary; resume with `Command(resume=...)`. | Interrupt：在节点边界停止执行，可恢复 |
| Time-travel | "Fork from a prior step" / "从先前步骤分叉" | `graph.invoke(None, config_with_old_checkpoint_id)` replays from that checkpoint forward. | Time-travel：从先前检查点重放 |
| Send | "Parallel subgraph dispatch" / "并行子图分派" | A constructor a node can return to spawn N parallel executions of a target node. | Send：节点返回以生成 N 个并行执行的构造器 |
| Subgraph | "A compiled graph as a node" / "编译后的图作为节点" | A compiled StateGraph used as a node in another graph; preserves its own state scope. | Subgraph：作为另一个图中节点使用的编译后 StateGraph |

## Encore une lecture

- [LangGraph documentation](https://langchain-ai.github.io/langgraph/) référence canonique pour StateGraph, réducteurs, points de contrôle et interruptions.
  LangGraph 文档StateGraph、reducer、检查点器和中断的权威参考──
- [LangGraph concepts: state, reducers, checkpointers](https://langchain-ai.github.io/langgraph/concepts/low_level/) le modèle mental utilisé dans cette leçon, directement de la source.
  LangGraph 概念: état, réducteur, contrôleur
- [LangGraph Persistence and Checkpoints](https://langchain-ai.github.io/langgraph/concepts/persistence/) les détails sur les magasins Postgres/SQLite/Redis, les espaces de noms des points de contrôle et les identifiants de filets.
  LangGraph 持久化和检查点详情
- [LangGraph Human-in-the-loop](https://langchain-ai.github.io/langgraph/concepts/human_in_the_loop/) `interrupt_before`- Je suis là .`interrupt_after`- Je suis là .`Command(resume=...)`, et le modèle de modification-état.
  LangGraph 人机协作 interrupt 和 résumé 模式──
- [Yao et al., "ReAct: Synergizing Reasoning and Acting in Language Models" (ICLR 2023)](https://arxiv.org/abs/2210.03629) le modèle que chaque agent LangGraph implémentera; lisez-le pour le raisonnement de la racine.
  Chaque agent LangGraph réalise un mode de réaction.
- [Anthropic — Building effective agents (Dec 2024)](https://www.anthropic.com/research/building-effective-agents) quelles formes de graphique (chaîne, routeur, orchestrateur-travailleurs, évaluateur-optimisateur) préférer et quand.
  Anthropic  concernant le choix des formes et des directives de l'utilisation
- Phase 11 · 09 (Appel de fonction)  l'outil-appel primitif chaque nœud de l'agent LangGraph réutilise.
  第 11 阶段 · 09(函数调用) 每个 LangGraph Agent 节点重用工具调用原语。
- Phase 11 · 14 (Model Context Protocol)  Découverte d'outils externes qui se connectent à un LangGraph `ToolNode`par l'adaptateur MCP.
  第 11 阶段 · 14(MCP) 通过MCP 适配器插入 LangGraph `ToolNode`Les outils externes sont trouvés.
- Phase 11 · 17 (compromise avec le cadre des agents)  quand choisir LangGraph au lieu de CrewAI, AutoGen ou Agno.
  第 11 阶段 · 17(Agent 框架对比) 何时选择 LangGraph。
