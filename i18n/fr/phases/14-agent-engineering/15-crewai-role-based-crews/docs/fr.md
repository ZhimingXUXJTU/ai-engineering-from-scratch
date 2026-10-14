# CrewAI: équipes et flux basés sur le rôle
# Équipes d'agents basées sur le rôle  Roles, tâches, processus

> Quatre primitives: Agent, tâche, équipage, processus. Deux formes de haut niveau: équipages (collaboration autonome, basée sur le rôle) et flux (événement-driven, déterministe). CrewAI est la mise en œuvre de référence 2026 et ses documents sont simples: "pour toute application prête à la production, commencer par un flux".

**Type:** Learn + Build | **类型:** 构建
**Languages:** Python (stdlib) | **语言:** Python (标准库)
**Prerequisites:** Phase 14 · 12 (Workflow Patterns), Phase 14 · 14 (Actor Model) | **前置知识:** 见原文
**Time:** ~75 minutes | **时间:** 见原文

## Objectifs d'apprentissage

- Nommer les quatre primitifs de CrewAI (Agent, tâche, équipage, processus) et ce que chacun possède.
- Distinguer le processus de consensus séquentiel, hiérarchique et prévu; choisir un par charge de travail.
- Distinguer les équipes (basées sur des rôles autonomes) des flux (déterministique axée sur les événements) et expliquer la recommandation de production des docteurs.
- Les outils en fil avec la`@tool`décorateur et `BaseTool`sous-classe; raison sur les sorties structurées par rapport au texte libre.
- Nommez les quatre types de mémoire CrewAI et quand chacun se dépense.
- Mettre en œuvre un équipage de trois agents (chercheur, écrivain, rédacteur en chef) qui produit un résumé.
- Détectez les trois modes de défaillance de CrewAI: le gonflement rapide, l'impôt sur le gestionnaire et les transferts fragiles.

## Le problème , l' introduction du problème

Les équipes qui adoptent des cadres multi-agents sont dans le même mur. " Collaboration autonome " sonne bien dans une démo. Ensuite, un client dépose un bug et vous avez besoin de répétition déterministe.

> Le personnel de l'équipe de plusieurs agents se retrouve sur le même mur. Le "co-laboration autonome" semble excellent dans la présentation. Le client fait alors une erreur, il faut une réinitialisation.

Les équipes de formation libre ne répondent pas à ces questions, mais perdent la forme exploratoire dont un agent de brainstorming a besoin.

> La formation de la formation en droit de l'homme ne peut répondre à ces questions de manière claire.


> **【中文解读】**L'Agence de l'équipe utilise un modèle de rôle pour chaque agent ayant un rôle (rôle) 目标 (objectif) 及背景故事 (Histoire)  L'Agence de l'équipe 协作完成任务 (e)  L'unité unique de l'Agence de l'équipe est de définir la théorie de gestion de l'organisation (rôle définition 团队协作)  L'Agence est mise en œuvre dans le design, de sorte que les utilisateurs non techniques puissent également définir l'Agence 团队。

> **{【拓展：CrewAI 是 2024-2025 年增长最快的 Agent 框架之一（GitHub 20k+ s...】}**CrewAI est l'un des cadres d'agents les plus rapides de 2024-2025 (GitHub 20k+ stars) ⋅ Son point de vente central est un agent de faible code ⋅ collaboration ⋅ via YAML  configurer un agent  rôle et un flux de tâches ⋅ CrewAI ⋅ support deux types de modes: Crew ⋅ pré définition de rôle ⋅ équipe ⋅ Flow ⋅ activité ⋅ flux ⋅ employeur d'entreprise ⋅ en particulier les non techniciens ⋅ façon de définir son rôle ⋅
La division de CrewAI est honnête sur le commerce. équipes pour le travail collaboratif, axé sur les rôles, exploratoire. flux pour la production axée sur les événements, propriété de code, auditable. même cadre, deux formes, choisir par surface.

> La division de l'IAC repose sur ce poids. L'équipe utilise la collaboration, la recherche de rôles. Le flux est utilisé pour la conduite des événements, le contrôle des codes, l'environnement de production vérifiable.

>  **【前置】** doit d'abord comprendre:Phase 14·12Anthropic Workflow PatternsCrewAI's Flow is these modes of implementation,Crew is"autonomes versions"工作流; ainsi que Phase 14·14Actor Model)Crew 内部 Agent 协作本质上是消息传递──还需要理解Pydantic结构化输出验证),因为Task `output_pydantic`C'est le cœur de la convention.

## Le concept de base.

### Quatre primitifs

La surface de l'Equipage est petite, mémorisez ceci et le reste est configuré.

> L'interface de l'équipage est très petite.

> CrewAI 将多 Agent 协作建模为角色团队(Crew) 和事件驱动流程(Flow)两种模式──四种原语:Agent(角色+目标+背景故事)、Task(任务)、Crew(团队容器)、Process(执行策略)──

- **Agent.** `role + goal + backstory + tools + (optional) llm`L'équipe de recherche a été créée pour la première fois en 1999 et a été créée en 1999 par le groupe de recherche de l'équipe de recherche de recherche de l'équipe de recherche de recherche de l'équipe de recherche de recherche de l'équipe de recherche de recherche de l'équipe de recherche de recherche de l'équipe de recherche de recherche de l'équipe de recherche de recherche de l'équipe de recherche de recherche de l'équipe de recherche de recherche de l'équipe de recherche de recherche de l'équipe de recherche de recherche de l'équipe de recherche de recherche de l'équipe de recherche de recherche de l'équipe de recherche de recherche de l'équipe de recherche de recherche de l'équipe de recherche de recherche de recherche de l'équipe de recherche de recherche de recherche de recherche de l'équipe de recherche de recherche de recherche de recherche de recherche de recherche de recherche de recherche de recherche de recherche de recherche de recherche de recherche de recherche de recherche de recherche de recherche de recherche de recherche de recherche de recherche de recherche de recherche de recherche de recherche de recherche de recherche de recherche de recherche de recherche de recherche de recherche de recherche de recherche de recherche de recherche de recherche de recherche de recherche de recherche de recherche de recherche de recherche de recherche de recherche de recherche de recherche de recherche de recherche de recherche de recherche de recherche de recherche de recherche de recherche de recherche de recherche de recherche de recherche de recherche de recherche de recherche de recherche de recherche de recherche de recherche de recherche de recherche de recherche de recherche de recherche de recherche de recherche de recherche de recherche de recherche de recherche de recherche de recherche de recherche de recherche de recherche de recherche de recherche de recherche de recherche de recherche de recherche de recherche de recherche de recherche de recherche de recherche de recherche de recherche de recherche de recherche de recherche de recherche de recherche de recherche de recherche de recherche de recherche de recherche de recherche de recherche de recherche de recherche de recherche de recherche de recherche de recherche de recherche de recherche de recherche de recherche de recherche de recherche de recherche de recherche de recherche de recherche de recherche de recherche de recherche de recherche de recherche de recherche de recherche de recherche de recherche de recherche de recherche de recherche de recherche de recherche de recherche de recherche de recherche de recherche de recherche de recherche de recherche de recherche de recherche de recherche de recherche de recherche de recherche de recherche de recherche de recherche de recherche de recherche de recherche de recherche de recherche de recherche

>  **【类比】**L'agent de CrewAI est défini comme un agent de recrutement JD (en anglais seulement) (en anglais seulement) (en anglais seulement) (en anglais seulement) (en anglais seulement) (en anglais seulement) (en anglais seulement) (en anglais seulement) (en anglais seulement) (en anglais seulement) (en anglais seulement) (en anglais seulement) (en anglais seulement) (en anglais seulement) (en anglais seulement) (en anglais seulement) (en anglais seulement) (en anglais seulement) (en anglais seulement) (en anglais seulement) (en anglais seulement) (en anglais seulement) (en anglais seulement) (en anglais seulement) (en anglais seulement) (en anglais seulement) (en anglais seulement) (en anglais seulement) (en anglais seulement) (en anglais seulement) (en anglais seulement) (en anglais seulement) (en anglais seulement) (en anglais seulement) (en anglais seulement) (en anglais seulement) (en anglais seulement) (en anglais seulement) (en anglais seulement) (en anglais) (en anglais) (en anglais) (en anglais) (en anglais) (en anglais) (en anglais) (en anglais) (en anglais) (en anglais) (en anglais) (en anglais) (en anglais) (en anglais) (en anglais) (en anglais) (en anglais) (en anglais) (en anglais) (en anglais) (en anglais)) (en anglais) (en anglais)) (en anglais) (en anglais) (en anglais) (en anglais)) (en anglais)) (en anglais) (en anglais)) (en anglais) (en anglais) (en anglais)) (en anglais) (en anglais)) (en anglais)) (en anglais)) (en anglais) (en anglais) (en anglais) (anglais) (ing) (ing) (ing) (ing) (ing) (ing) (ing) (ing)**关键洞察**Le fond de l'histoire n'est pas décoré, cela affectera vraiment le style de jugement de la LLM.
- **Task.** `description + expected_output + agent + (optional) context + (optional) output_pydantic`- Unité de travail réutilisable.`expected_output`C'est le contrat.`context`Liste des tâches en amont dont les résultats sont transmis. `output_pydantic`une forme structurée.
- **Crew.**Container, possède la liste des`agents`, la liste des `tasks`, le `process`, et facultatif `memory`+ `verbose`+ `manager_llm`réglages.
- **Process.**Stratégie d'exécution: séquentielle, hiérarchique, consensus (planifié).

Les agents ne se voient pas directement, les tâches sont des agents de référence, l'équipage séquence les tâches, le processus décide qui choisit la prochaine tâche, c'est tout le modèle mental.

> L'agent 间不直接见彼此──Task 引用 Agent──Crew 排列任务序──Processus décide qui exécute la prochaine tâche──Tant est le modèle mental complet──

> **Validated against**CrewAI 0.86 (2026-05). Les versions plus récentes peuvent renommer ou fusionner les types de processus; vérifiez le [CrewAI Processes docs](https://docs.crewai.com/concepts/processes)avant de s'appuyer sur une forme spécifique.

### Sequence et hiérarchie

- **Sequential.**Les tâches sont exécutées par ordre de déclaration.`context`Le coût le plus bas, le plus prévisible, utilisez-le lorsque l'ordre est fixé.
- **Hierarchical.**Un agent de gestion (appel séparé de LLM) parcourt les itinéraires entre les spécialistes.`manager_llm`le gestionnaire choisit la tâche suivante à chaque tour et peut refuser ou rediriger. Utilisez lorsque vous avez quatre spécialistes ou plus et que la commande dépend vraiment de la sortie préalable.
- **Consensus.**Les docs réservent le nom pour un futur processus basé sur le vote.

La hiérarchie ajoute un appel LLM par round (le gestionnaire) en plus de chaque appel spécialisé. Le coût des jetons peut tripler sur une course en cinq étapes.

> ️ **【易错点】**Voir les exemples de documents de l'Equipage d'Activité (CrewAI) avec un modèle hiérarchique.**后果**Chaque tour de la gestion de l'équipe de gestion de l'équipe de gestion de gestion de l'équipe de gestion de gestion de l'équipe de gestion de gestion de l'équipe de gestion de gestion de l'équipe de gestion de gestion de l'équipe de gestion de gestion de l'équipe de gestion de gestion de l'équipe de gestion de gestion de l'équipe de gestion de gestion de l'équipe de gestion de gestion de l'équipe de gestion de gestion de gestion de l'équipe de gestion de gestion de gestion de l'équipe de gestion de gestion de gestion de l'équipe de gestion de gestion de gestion de l'équipe de gestion de gestion de l'équipe de gestion de gestion de l'équipe de gestion de gestion de l'équipe de gestion de gestion de l'équipe de gestion de gestion de gestion de l'équipe de gestion de gestion de gestion de l'équipe de gestion de gestion de gestion de l'équipe de gestion de gestion de gestion de gestion de l'équipe de gestion de gestion de gestion de gestion de gestion de l'équipe de gestion de gestion de gestion de gestion de gestion de gestion de l'équipe de gestion de gestion de gestion de gestion de gestion de l'équipe de gestion de gestion de gestion de gestion de gestion de l'équipe de gestion de gestion de gestion de gestion de gestion de l'équipe de gestion de gestion de gestion de l'équipe de gestion de gestion de gestion de l'équipe de gestion de gestion de gestion de l'équipe de gestion de gestion de l'équipe de gestion de gestion de l'équipe de gestion de gestion de gestion de l'équipe de gestion de gestion de l'équipe de gestion de l'équipe de gestion de l'équipe de gestion de l'équipe de l'équipe de gestion de l'équipe de gestion de l'équipe de gestion de l'équipe de gestion de l'équipe de gestion de l'équipe de l'équipe de l'équipe de l'équipe de l'équipe de l'équipe de l'équipe de l'équipe de l'équipe de l'équipe de l'équipe de l'équipe de l'équipe de l'équipe de l**一行修复**:默认使用序列 (成本最低、最可预测),只有任务顺序真的依赖前一步输出 (如客服分流)才升级到等级级 (如客服分流)

> Le modèle de niveau augmente le nombre de cours de LLM à chaque session de formation professionnelle.

> CrewAI 将多 Agent 协作建模为角色团队(Crew) 和事件驱动流程(Flow)两种模式──四种原语:Agent(角色+目标+背景故事)、Task(任务)、Crew(团队容器)、Process(执行策略)──

### Équipes contre flux

C'est le cadre avec lequel les docteurs vont en 2026.

> C'est le cadre le plus central du dossier de 2026.

- **Crew.**Autonomie basée sur le LLM. Le cadre choisit la forme à l'heure de l'exécution. Bon pour: recherche, brainstorming, premiers plans, partout où le chemin fait partie de la réponse. Difficile à reproduire. Difficile à tester. Cheap à prototype.
- **Flow.**Graphique d'événements que vous possédez.`@start`marque l'entrée. `@listen(topic)`Chaque étape est Python simple (peut appeler un équipage en interne).

Les docteurs recommandent de produire en 2026: commencer par un flux.`Crew.kickoff()`Le flux vous donne le sentier d'audit, l'équipage vous donne l'exploration.

> 文档 2026 年的生产建议:从流开始――当自主性值其成本时,将船员作为`Crew.kickoff()`调用嵌入 Flow 步骤中──Flow 提供审计追踪,Crew 提供探索能力──组合使用,不要二选一──

> CrewAI 将多 Agent 协作建模为角色团队(Crew) 和事件驱动流程(Flow)两种模式──四种原语:Agent(角色+目标+背景故事)、Task(任务)、Crew(团队容器)、Process(执行策略)──

### Intégration des outils

Trois façons de donner un outil à un agent.

> Il y a trois façons de donner à l'agent un outil. Choisissez le plus simple.

> CrewAI 将多 Agent 协作建模为角色团队(Crew) 和事件驱动流程(Flow)两种模式──四种原语:Agent(角色+目标+背景故事)、Task(任务)、Crew(团队容器)、Process(执行策略)──

1. **`@tool` decorator.**Les fonctions pures deviennent des outils. La signature est le schéma; la documentation est la description que le LLM voit.

   ```python
   from crewai.tools import tool

   @tool("Search the web")
   def search(query: str) -> str:
       """Return top results for the query."""
       return run_search(query)
   ```

2. **`BaseTool` subclass.**Utilisation lorsque l'outil a un état (client, cache) ou a besoin d'args structurés.

   ```python
   from crewai.tools import BaseTool
   from pydantic import BaseModel

   class SearchArgs(BaseModel):
       query: str
       limit: int = 10

   class SearchTool(BaseTool):
       name = "web_search"
       description = "Search the web and return top results."
       args_schema = SearchArgs

       def _run(self, query: str, limit: int = 10) -> str:
           return self.client.search(query, limit=limit)
   ```

3. **Built-in toolkits.**CrewAI expédie des adaptateurs de première partie: `SerperDevTool`- Je suis là .`FileReadTool`- Je suis là .`DirectoryReadTool`- Je suis là .`CodeInterpreterTool`- Je suis là .`RagTool`- Je suis là .`WebsiteSearchTool`- Un câble avec une importation.

Les sorties structurées utilisent Pydantic.`output_pydantic=MyModel`La réponse de la MLL est validée par CrewAI contre le modèle et est soit forcée soit réessayée.`expected_output`Les sorties de texte libre sont bonnes pour les projets; les sorties structurées sont ce que les flux en aval peuvent consommer.

> 结构化输出使用Pydantic──在Task 上传入 `output_pydantic=MyModel` Les équipes d'essai en ligne, selon le modèle de l'expérience LLM, ne correspondent pas à un transfert obligatoire ou à un nouveau test.`expected_output`字符串使用──自由文本输出适合草稿; structuralisée输出才是下游 Flow 可以消费的──

> CrewAI 将多 Agent 协作建模为角色团队(Crew) 和事件驱动流程(Flow)两种模式──四种原语:Agent(角色+目标+背景故事)、Task(任务)、Crew(团队容器)、Process(执行策略)──

### Les crochets de mémoire

CrewAI envoie quatre types de mémoire hors de la boîte.

> La CrewAI 开箱提供四种记忆类型──它们可以组合使用:一个 Crew可以同时启动全部四种──

> **Validated against**CrewAI 0.86 (2026-05). Les dernières versions tout parcourent un système unifié `Memory`Le modèle conceptuel ci-dessous est toujours valable, mais la surface de la classe publique peut s'effondrer en une seule`Memory`point d'entrée dans les versions plus récentes; vérifier [CrewAI memory docs](https://docs.crewai.com/concepts/memory)pour l'API actuelle.

- **Short-term.**Bouffer de conversation à la fin d'une seule course.
- **Long-term.**Persistant sur les circuits. Stocké dans un vecteur DB (Chroma par défaut, swappable). Retrievé par similitude avec la tâche actuelle.
- **Entity.**"Client X est dans le plan d'entreprise". Clé par entité, pas par similitude.
- **Contextual.**Récupération en temps d'assemblage, extrait la mémoire pertinente au moment où l'agent en a besoin, pas prélèvée.

Activer l' équipage avec `memory=True`La mémoire est l'un des endroits où CrewAI gagne sa place contre les cadres plus fins; LangGraph pur exige que vous câbliez chacun d'entre eux vous-même.

> Dans l' équipage`memory=True`Ou selon le type de configuration pour activer. Les emblèmes que vous avez configurés  fournisseur de support                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                   

> CrewAI 将多 Agent 协作建模为角色团队(Crew) 和事件驱动流程(Flow)两种模式──四种原语:Agent(角色+目标+背景故事)、Task(任务)、Crew(团队容器)、Process(执行策略)──

### Lorsque CrewAI est adapté
### Lorsque les équipes basées sur les rôles s'adaptent

- Trois à six agents avec des rôles nommés et un flux de travail collaboratif.
- Le routage où le jugement de la LLM sur l'étape suivante fait partie de la valeur (hiérarchique).
- Où que l' équipe soit plus heureuse de lire .`role + goal + backstory`que de lire une définition graphique.

### Quand ils ne le font pas

- Les DAG déterministes avec un ordre strict. Utilisez LangGraph (leçon 13).
- Les budgets de latence sous-seconde. Hiérarchique ajoute aller-retour. Même Sequential sérialise les demandes qui incluent des histoires de fond et des sorties précédentes.
- Les boucles à agent unique. Sautez le cadre; une boucle à agent (leçon 1) plus un registre d'outils est plus court.

La leçon 17 (Agent Framework Tradeoffs) explique cela dans une matrice.

> Le travail de l'agent est une technique de travail qui consiste à faire des recherches et à faire des recherches.

> 🤔 **【困惑】**Q: CrewAI 文档说"生产环境从流动开始",但我看YouTube教程全是 Crew 例子,到底该信谁? A: 信文档。YouTube教程偏向演示 效果(Crew autonomous协作看起来更酷),但生产环境是什么?**可重放、可审计、可监控** Ces seulement Flow 能给──建议路径: Using Crew做原型验证思想(一两小时搞定),稳定后用 Flow 重写为生产版本──Crew 不是不能用,而是不能直接上生产──

> CrewAI 将多 Agent 协作建模为角色团队(Crew) 和事件驱动流程(Flow)两种模式──四种原语:Agent(角色+目标+背景故事)、Task(任务)、Crew(团队容器)、Process(执行策略)──

### Forme de dépendance

Indépendante de LangChain. Python 3.10 à 3.13. Utilisations `uv`Le nombre d' étoiles: voir[crewAIInc/crewAI](https://github.com/crewAIInc/crewAI)L'intégration AWS Bedrock est documentée; les benchmarks des fournisseurs rapportent une vitesse significative par rapport à LangGraph sur les charges de travail de QA, mais la méthodologie (ensemble de données, matériel, métrique d'évaluation) n'est pas publiée, alors traitez les numéros du fournisseur-cadre comme directionnels uniquement.

> Non dépend de LangChain. Soutenir Python 3.10 à 3.13.`uv`包管理──AWS Bedrock 集成已有文件; fournisseur基准测试报告称在QA 工作负载上有显著加速,但方法论(数据集、硬件、评估指标) est non publié, de sorte que les données du fournisseur-cadre seront uniquement utilisées comme référence──

> CrewAI 将多 Agent 协作建模为角色团队(Crew) 和事件驱动流程(Flow)两种模式──四种原语:Agent(角色+目标+背景故事)、Task(任务)、Crew(团队容器)、Process(执行策略)──

### Où ce modèle va mal

- **Prompt-bloat from backstories.**Un récit de 2000 mots par agent et un équipage de cinq agents brûle le budget contextuel avant le premier appel d'outil. Gardez les récit de 200 mots.

> **背景故事导致的提示膨胀。**Chaque contextuel de chaque agent 2000 mots, ainsi que cinq équipes d'agents, est déjà épuisé avant la première utilisation des outils.
- **Manager-LLM token tax.**Le processus hiérarchique ajoute un appel de gestion LLM avant chaque appel spécialisé. Sur une équipe de cinq tâches qui est six appels de gestion LLM au lieu de cinq, et l'appel de gestion porte la liste complète des tâches plus les sorties précédentes.

> **管理者 LLM 的 Token 税。**Le modèle de niveau augmente une fois avant la mise en place de la mise en place de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion
- **Brittle handoffs.**La tâche N's `expected_output`est "un schéma". La tâche N+1 la lit comme `context`Le LLM a produit quatre, les agents en aval, les annonces.`output_pydantic`sur la tâche N, la tâche N+1 lit un objet typé, pas du texte libre.

> **脆弱的交接。** tâche N  `expected_output`Il s'agit d'un "grand plan" de tâches N+1 qui seront définies comme `context`读取并尝试解析三个部分──LLM 生成四个──下游 Agent 即兴发挥──用 `output_pydantic`修复任务 N,让任务 N+1 读取类型化对象而非自由文本。
- **Crew-as-prod.**La production de l'équipage libre est effectuée sans enveloppe de flux. La variabilité de sortie est élevée; la répétition est impossible; le coup de feu sur appel ne peut pas différencier une mauvaise course contre une bonne.

> **Crew 直接上生产。**没有包装成流就将自由形式 Crew 发布到生产环境――输出变异性高;无法重放;值班人员无法对抗好坏运行――使用流 包装――

## Construisez-le et mettez-le en œuvre.
```figure
ae-crew-vs-flow
```

## Faites-le

`code/main.py`Il implémentera des versions STDlib des deux formes plus un équipage de trois agents.

> `code/main.py`Il a réalisé deux formes et un groupe de trois agents.

> CrewAI 将多 Agent 协作建模为角色团队(Crew) 和事件驱动流程(Flow)两种模式──四种原语:Agent(角色+目标+背景故事)、Task(任务)、Crew(团队容器)、Process(执行策略)──

La forme:

- `Agent`- Je suis là .`Task`les classes de données correspondant à la surface de l'Equipage d'exploration.
- `SequentialCrew.kickoff(inputs)`Les tâches sont effectuées en ordre de déclaration, en répartissant les sorties en`context`- Je suis désolé .
- `HierarchicalCrew.kickoff(topic)`Un agent de direction choisit le prochain spécialiste à chaque tour, s'arrête à "fin".
- `Flow`avec `@start`et `@listen(topic)`Des décorateurs, une petite boucle d'événements et une trace.
- `tool(name)`Le décorateur reflète les équipes de l'Aéroport de la Croix.`@tool`la forme.
- `Memory`avec `short_term`- Je suis là .`long_term`- Je suis là .`entity`Les magasins; la similitude ridicule utilise des numpy.
- Les réponses de faux LLM sont des chaînes hardcodées déconnectées de rôle plus préfixe d'entrée.

Démo concrète: chercheur, écrivain, équipe d'éditeur produisant un bref sur "ingénierie des agents 2026 ".

> 具体演示:研究员、作者、编辑组成团队,生成一篇关于"agent engineering 2026"的简报──研究员获取(模拟的)来源──作者起草──编辑精炼──同一个团队通过流动 运行以展示确定性形态──

> CrewAI 将多 Agent 协作建模为角色团队(Crew) 和事件驱动流程(Flow)两种模式──四种原语:Agent(角色+目标+背景故事)、Task(任务)、Crew(团队容器)、Process(执行策略)──

- Je vais le faire.

```bash
python3 code/main.py
```

Couvertures de traces: sorties de filetage d' équipage séquentielles à travers `context`, équipe hiérarchique avec choix de gestionnaires (chercheur, écrivain, rédacteur en chef, puis "fait"), flux en cours de cours les mêmes trois étapes avec des sujets explicites (`researched`- Je suis là .`drafted`- Je suis là .`edited`), les appels à l' outil sont parcourus `@tool`, et la mémoire à long terme survivant à deux coups de pied.

> CrewAI 将多 Agent 协作建模为角色团队(Crew) 和事件驱动流程(Flow)两种模式──四种原语:Agent(角色+目标+背景故事)、Task(任务)、Crew(团队容器)、Process(执行策略)──

La trace de l'équipage est fluide, le gestionnaire pourrait en principe réordonner la trace de flux est fixe.

> Le suivi de l'équipage est fluide; le directeur peut en principe se réorganiser.

> CrewAI 将多 Agent 协作建模为角色团队(Crew) 和事件驱动流程(Flow)两种模式──四种原语:Agent(角色+目标+背景故事)、Task(任务)、Crew(团队容器)、Process(执行策略)──

## Utilisez-le avec le cadre de réalisation

- **CrewAI Flow**Même si le flux est une étape qui appelle`Crew.kickoff()`Le flux donne la limite de vérification.
- **CrewAI Crew (Sequential)**pour des travaux de collaboration clairs, en particulier les premiers projets et les boucles d'examen.
- **CrewAI Crew (Hierarchical)**lorsque le routage dépend de la sortie et que vous avez quatre spécialistes ou plus.
- **LangGraph**(Létion 13) pour les machines d'état explicites, résumé durable, ordre strict.
- **AutoGen v0.4**(Létion 14) pour la synchronisation du modèle acteur et l'isolement des failles.
- **OpenAI Agents SDK**(Létion 16) pour les produits OpenAI-first avec des roulements et des barreaux.
- **Claude Agent SDK**(Létion 17) pour les produits Claude-first avec sous-boîtiers et magasin de séances.

## Envoyez-le . Produit .

`outputs/skill-crew-or-flow.md`Choisissez Crew vs Flow pour une tâche et échauffe la mise en œuvre minimale. Hard rejette sur les sujets Crew-without-backstory, Flow-without-explicite, Hiérarchique avec moins de trois spécialistes.

> `outputs/skill-crew-or-flow.md`Pour une mission, choisir un équipage ou un flux, et construire un minimum de réalisation.

> CrewAI 将多 Agent 协作建模为角色团队(Crew) 和事件驱动流程(Flow)两种模式──四种原语:Agent(角色+目标+背景故事)、Task(任务)、Crew(团队容器)、Process(执行策略)──

## Les pièges sont des pièges.

- **Backstory as flavor.**Il forme les sorties, teste trois variantes par agent, la variance est réelle, choisissez une, congélez-la.

> **把背景故事当装饰。**Il a en fait formé la sortie. Chaque agent test trois variables; la différence est réelle.
- **Skipping `expected_output`.**Sans contrat par tâche, les tâches en aval reprennent ce que le LLM a produit.

> **跳过 `expected_output`。**没有每个任务的契约,下游任务会接收LLM 生成的任何内容──Crew 运行通过;审计失败──
- **Memory always-on.**Le long terme écrit chaque course. Le vecteur DB augmente. La récupération devient bruyante. La portée écrit aux tâches où le fait est persistant.

> **记忆始终开启。**La rédaction de la base de données de données de longue durée est limitée aux tâches de persévérance nécessaires.
- **Manager prompt drift.**Si le routage devient bizarre, jetez-le en mode verbe et lisez.

> **管理者提示漂移。**Le modèle de niveau est un modèle de mise en cache.
- **Tool side effects in Crews.**Un équipage peut appeler un outil plus de fois que prévu.

> **Crew 中的工具副作用。**L'équipage pourrait utiliser plus d'outils que prévu. Les opérations de POST, DELETE, PAI et autres doivent être placées dans les étapes de flux, sans jamais être placées dans les outils de l'équipage.

## Les exercices

1. Convertir l'équipage de la séquence en flux, compter les points de contact où la variabilité diminue, noter où la lisibilité diminue.
  Le mot "exercer" est traduit par "exercer".
2. Ajouter la mémoire de l'entité à l'équipage: les faits sur un client persistent au cours des coupes.
  Le mot "exercer" est traduit par "exercer".
3. Implémenter un processus hiérarchique où le gestionnaire refuse de se diriger vers l'éditeur jusqu'à ce que la sortie de l'écrivain ait au moins trois paragraphes.
  Le mot "exercer" est traduit par "exercer".
4. - Le câble`BaseTool`Comparer la forme de la trace par rapport à la `@tool`une version décorative.
  Le mot "exercer" est traduit par "exercer".
5. Ajouter `output_pydantic=Brief`à la tâche de rédacteur en chef, où `Brief`Il a`title`- Je suis là .`summary`- Je suis là .`sections`. Faites une fois que la sortie de la tâche de rédacteur a malformé JSON; vérifiez le comportement de réessayer CrewAI dans la trace.
  Le mot "exercer" est traduit par "exercer".
6. Lisez l'introduction des documents de CrewAI.`crewai`Quelles garanties la version stdlib a-t-elle raté ?
  Le mot "exercer" est traduit par "exercer".
7. Tu as oublié quelles traces dans la version stdlib ?
  Le mot "exercer" est traduit par "exercer".

## Les termes clés

| Term | What people say | What it actually means |
|------|----------------|------------------------|---|
| Agent | "Persona" | Role + goal + backstory + tools |  |
| Task | "Unit of work" | Description + expected output + assignee + optional structured output |  |
| Crew | "Agent team" | Container for Agents + Tasks + Process |  |
| Process | "Execution strategy" | Sequential / Hierarchical / Consensus (planned) |  |
| Flow | "Deterministic workflow" | Event-driven, code-owned, testable |  |
| Backstory | "Persona prompt" | Tone and judgment shaper for the Agent |  |
| `@tool` | "Function tool" | Decorator that turns a function into a tool the Agent can call |  |
| `BaseTool` | "Class tool" | Class-based tool with args schema, retries, async support |  |
| Entity memory | "Per-entity facts" | Memory scoped to a customer / account / issue |  |
| Long-term memory | "Cross-run memory" | Vector-backed memory that survives between kickoffs |  |
| Contextual memory | "Just-in-time retrieval" | Memory pulled at the moment the Agent needs it |  |
| Manager LLM | "Router agent" | Extra LLM in Hierarchical process that picks the next task |  |
| `expected_output` | "Task contract" | String that tells the Agent (and audit) what shape to return |  |

## Encore une lecture

- [CrewAI docs introduction](https://docs.crewai.com/en/introduction): concepts et voie de production recommandée
  Le mot "réfléchisseur" est traduit par "réfléchisseur".
- [CrewAI Flows guide](https://docs.crewai.com/en/concepts/flows): forme axée sur l'événement, `@start`- Je suis là .`@listen`
  Le mot "réfléchisseur" est traduit par "réfléchisseur".
- [CrewAI tools reference](https://docs.crewai.com/en/concepts/tools)Le numéro de la liste:`@tool`- Je suis là .`BaseTool`, kits d'outils intégrés
  Le mot "réfléchisseur" est traduit par "réfléchisseur".
- [CrewAI memory](https://docs.crewai.com/en/concepts/memory): à court terme, à long terme, entité, contextuel
  Le mot "réfléchisseur" est traduit par "réfléchisseur".
- [Anthropic, Building Effective Agents](https://www.anthropic.com/research/building-effective-agents): quand le multi-agent aide et quand il ne le fait pas
  Le mot "réfléchisseur" est traduit par "réfléchisseur".
- [LangGraph overview](https://docs.langchain.com/oss/python/langgraph/overview): l'alternative de la machine d'État
  Le mot "réfléchisseur" est traduit par "réfléchisseur".
