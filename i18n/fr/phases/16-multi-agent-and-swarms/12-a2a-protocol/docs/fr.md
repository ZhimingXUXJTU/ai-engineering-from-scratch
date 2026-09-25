# A2A  Le protocole agent-agent 

> Google a annoncé A2A en avril 2025; en avril 2026, la spécification est à https://a2a-protocol.org/latest/specification/et plus de 150 organisations le soutiennent. A2A est le complément horizontal du MCP (leçon 13): là où le MCP est vertical (agent  outils), A2A est peer-to-peer (agent  agent). Il définit les cartes d'agent (découverte), les tâches avec des artefacts (texte, données structurées, vidéo), les cycles de vie opaques des tâches et auth. Les systèmes de production associent de plus en plus MCP à A2A. Google Cloud a introduit le support A2A dans Vertex AI Agent Builder pendant les années 2025-2026.

> **【中文解读】**Google a publié le protocole A2A en avril 2025; jusqu'en avril 2026, la norme dispose déjà de plus de 150 organisations de soutien. A2A est le complément au niveau de MCP: MCP est vertical (Agent et outil), A2A est point à point (Agent et agent) ⋅ défini la carte d'agent (Agent Card) ⋅ avec des produits ⋅ tâches ⋅ non transparents ⋅ mission cycle de vie et certification ⋅ système de production ⋅ plus en plus de pays utilisent MCP et A2A ⋅ par rapport à l'utilisation ⋅

> **【拓展：A2A → Google 的 Agent 协议】**A2A est le protocole de communication standard de l'agent de Google, avec MCP de l'anthropique, le protocole de contexte modèle) complémentation.

**Type:** Learn + Build | **类型:** 学习 + 构建
**Languages:** Python (stdlib, `http.server`, `json`) | **语言:** Python (标准库, `http.server`, `json`)
**Prerequisites:** Phase 16 · 04 (Primitive Model) | **前置知识:** Phase 16 · 04 (原语模型)
**Time:** ~75 minutes | **时间:** ~75 分钟

>  **【前置】**Pour les participants, le programme est basé sur la méthode de formation de base de la formation professionnelle.
>  **【类比】**MCP + A2A = "电话黄页 + 直接通话"──MCP = 工具目录(agent 找工具用);A2A = Agent 间通话协议(agent 找 agent 协作)──2026 生产系统标配:MCP(连工具) + A2A(连其他 Agent) + Agent Card(发现)──Google 主导,150+ 组织支持──

## ♪ Problème ♪ Introduction du problème ♪

Vous pouvez exposer un point d'extrémité HTTP, définir un schéma JSON sur mesure, et espérer que l'autre côté parle. Chaque paire d'agents devient une intégration personnalisée.

> Vous pouvez dévoiler un HTTP, définir un modèle JSON personnalisé, et espérer que l'autre partie puisse le comprendre.

Le problème de l'intégration N-quadré: avec N agents, vous avez besoin de N × 1) / 2 intégrations personnalisées. Avec 10 agents, c'est 45 intégrations. Avec 100 agents, 4950. A2A s'effondre à N Agent Cards, chacun décrivant un agent.

> N 平方集成问题:N 个代理 需要 N×(N-1)/2 个定制集成──10 个代理 是 45 个集成──100 个代理 是 4950 个──A2A est réduit à N 个代理卡片, chaque description est un agent──

A2A est le protocole de communication universel pour cet appel. Découverte standard, modèle de tâche standard, transport standard, objets standard. Comme HTTP+REST mais pour les agents en tant que citoyens de première classe.

> A2A est un protocole de ligne générale à utiliser.

L'abstraction clé: les agents sont des terminaux réseau adressables et découvertables. Vous n'importez pas un agent; vous l'appellez. Cela découple le déploiement  l'agent fonctionne partout, dans n'importe quelle langue, en utilisant n'importe quel cadre, tant qu'il parle A2A.

> 关键抽象:Agent est可寻址、可发现的网络端点──你不"导入"Agent;你"调用"它──这解已部署Agent 运行在任何地方、使用任何语言、使用任何框架,只要它说 A2A──

## Concept Le concept central

### Les quatre éléments

> Quatre éléments

**Agent Card.**Un document JSON à `/.well-known/agent.json`Les informations sur les différents types de données sont fournies par le service de recherche.

> **Agent 卡片。**      `/.well-known/agent.json`Les données de référence sont fournies par le service de recherche et de recherche.

La convention URL bien connue reflète les normes web (`/.well-known/`est le même chemin utilisé pour `robots.txt`Tout agent compatible avec A2A peut être découvert en obtenant cette URL.

> Il est un site web très populaire.`/.well-known/`est utilisé `robots.txt`、ACME 挑战、OIDC 发现的相同路径) ∼ Tout agent A2A 兼容 △ peuvent obtenir cette URL 发现──不需要注册表、代理或中央目录──

**Task.**Un objet asynchrone, étalé avec un cycle de vie:`submitted -> working -> completed / failed / canceled`Un client envoie une tâche, des sondages ou s'abonne aux mises à jour.

> **任务。**工作单元── Objets ayant des cycles de vie différents:`submitted -> working -> completed / failed / canceled` Les tâches de transmission, de consultation ou de mise à jour des clients.

**Artifact.**Le type de résultat produit par une tâche. texte, JSON structuré, image, vidéo, audio.

> **工件。**Les tâches de production sont de type, donc les différents modèles sont des citoyens égaux.

**Opaque lifecycle.**A2A ne précise pas *comment* l'agent à distance résout la tâche.Le client voit les transitions d'état et les artefacts; la mise en œuvre est libre d'utiliser n'importe quel cadre.

> **不透明生命周期。**A2A 不规范远程代理 *如何* 解决任务──客户端看状态转换和工件;实现可以自由使用任何框架──

Cette opacité est par conception. Un agent à distance construit sur LangGraph, CrewAI ou un script Python personnalisé semble identique au client A2A. L'interopérabilité vient de l'accord sur le format de fil, pas les internes.

> Cette opacité est la conception de manière à ce que l'agent à distance construit sur la base de LangGraph, CrewAI ou Python  script de définition personnalisée  A2A  clientèle semble identique  Interopérationnalité provient du format de ligne convenu, et non de l'intérieur 

### Le MCP/A2A est divisé

- **MCP**(Léction 13): outil agent <->. L'agent lit/écrit via JSON-RPC sur un serveur outil.
  Le mot grec traduit par " le mot grec "**MCP**(Létion 13):Agent <-> 工具──Agent 通过 JSON-RPC 读写工具服务器──默认无状态──
- **A2A**Le protocole de parité; les deux parties sont des agents avec leur propre raisonnement.
  Le mot grec traduit par " le mot grec "**A2A**Les deux parties sont des agents qui ont leur propre opinion.

Les systèmes de production multi-agents utilisent les deux. un paire A2A appelle les outils MCP de son côté. La division garde les deux problèmes propres.

> Les deux systèmes utilisent tous les deux les deux.

Un schéma commun: un "agent de recherche" A2A de la société A appelle un serveur d'outil de recherche MCP en interne, puis renvoie ses résultats à un "agent d'analyse" A2A de la société B. La communication transnationale est A2A; l'utilisation interne des outils est MCP. Chaque protocole fait ce qu'il est le mieux à faire.

> 常见模式: A2A "Agent de recherche" de la société A utilise MCP 搜索工具服务器, puis retrouve le retour à A2A "Agent d'analyse" de la société B.

Ou avec streaming: abonnement SSE à `/tasks/{id}/events`pour les mises à jour.

> Ou utiliser: SSE 订阅 `/tasks/{id}/events`获取推送更新── Je suis en train de faire une nouvelle expérience.

### Autre

A2A prend en charge trois modèles communs:

> A2A 支持三种常见模式:

Les trois modèles couvrent le spectre de "Je fais confiance à mon fournisseur d'identité" (porteur OAuth2) à "nous nous vérifions mutuellement" (mTLS) à "nous ne faisons confiance à aucun tiers" (signe HMAC). Choisissez le plus léger qui répond à vos exigences de sécurité.

> Les trois modes couvrent la gamme de "我信任我的身份提供商" (OAuth2 porteur) à "我们互相验证彼此" (MTLS) à "我们不信任任何第三方" (HMAC signing).

- **Bearer token** OAuth2 ou opaque.
  Le mot grec traduit par " le mot grec "**Bearer token** OAuth2 ou non transparente
- **mTLS** TLS mutuel; les organisations se prouvent l'identité.
  Le mot grec traduit par " le mot grec "**mTLS** 双向 TLS; Organisation mutuelle de preuve de identité
- **Signed requests** HMAC sur la charge utile.
  Le mot grec traduit par " le mot grec "**签名请求** à la charge HMAC

L'auteur est déclaré dans la carte d'agent; les clients découvrent et se conforment.

> 认证在代理卡片中声明;客户端发现并遵守──

### 150 organisations d'ici à avril 2026

L'adoption par l'entreprise a conduit à l'échelle A2A. Le titre: A2A est devenu la façon dont les systèmes d'agents d'entreprise traversent les frontières de la confiance. Google Cloud a livré le support Vertex AI Agent Builder A2A; Microsoft Agent Framework le prend en charge; la plupart des principaux frameworks (LangGraph, CrewAI, AutoGen) expédient des adaptateurs A2A.

> L'adoption par les entreprises a favorisé la taille de l'A2A. Le processus d'adoption par les entreprises a permis de développer le système d'agents d'entreprise. Google Cloud a fourni le Vertex AI Agent Builder A2A.

La raison pour laquelle A2A a gagné l'adoption d'entreprise où FIPA-ACL a échoué: A2A est natif de JSON, utilise l'infrastructure Web existante (HTTP, SSE, OAuth) et ne nécessite pas d'ontologies partagées.

> A2A est le JSON original, il utilise les infrastructures Web existantes, il n'a pas besoin de partager son propre contenu.

### Où A2A gagne

- **Cross-organization calls.**L'agent de la compagnie A appelle l'agent de la compagnie B. Sans A2A, chaque paire est un contrat sur mesure.
  Le mot grec traduit par " le mot grec "**跨组织调用。**Company A's Agent 调用Company B's Agent ⋅ pas de A2A, chaque partie est un contrat de fabrication ⋅
- **Heterogeneous frameworks.**L'agent LangGraph appelle l'agent CrewAI appelle l'agent Python personnalisé.
  Le mot grec traduit par " le mot grec "**异构框架。**LangGraph Agent 调用 CrewAI Agent 调用自定义 Python Agent。A2A 标准化。
- **Typed artifacts.**Résultat vidéo, JSON structuré, audio  tout premier niveau.
  Le mot grec traduit par " le mot grec "**类型化工件。**视频结果、结构化 JSON、音频都是一等公民──
- **Long-running tasks.**Le cycle de vie opaque + les sondages simplifient les tâches d'une durée d'une heure.
  Le mot grec traduit par " le mot grec "**长时间运行的任务。**Le cycle de vie + la rotation rendent les tâches de classe de petit temps plus simples.

### Où A2A lutte

- **Latency-sensitive micro-calls.**Le cycle de vie de l'A2A est asynchrone.
  Le mot grec traduit par " le mot grec "**延迟敏感的微调用。**Le cycle de vie d'A2A est différent.
- **Tight-coupled in-process agents.**Si les deux agents fonctionnent dans le même processus Python, le retour HTTP d'A2A est exagéré.
  Le mot grec traduit par " le mot grec "**紧耦合的进程内 Agent。**Si deux agents fonctionnent dans le même processus Python, le retour HTTP d'A2A est un surdépôt.
- **Small teams.**Les frais généraux sont réels; les agents internes ne peuvent avoir besoin de la formalité.
  Le mot grec traduit par " le mot grec "**小团队。**La réglementation de vente est réelle; seul l'agent interne peut ne pas avoir besoin de cette formalité.

### A2A contre ACP, ANP, NLIP

Plusieurs spécifications connexes ont été émises en 2024-2026:

> Entre 2024 et 2026, plusieurs règles connexes ont été élaborées:

- **ACP**(IBM/Linux Foundation)  Prédécesseur à A2A, portée plus étroite.
  Le mot grec traduit par " le mot grec "**ACP**(IBM/Linux Foundation)  A2A's avant-goût, champ de champ plus étroit
- **ANP**(Protocole de réseau d'agents)  Peer-discovery-heavy, décentralisé-first.
  Le mot grec traduit par " le mot grec "**ANP**(Protocole de réseau d'agents) 重对等发现, décentralisation prioritaire
- **NLIP**(Protocole d'interaction linguistique naturelle ECMA, normalisé décembre 2025)  type de contenu en langue naturelle.
  Le mot grec traduit par " le mot grec "**NLIP**(Ecma Naturelanguage交互协议, 2025 12 月標準化)

A2A est le protocole de pairs le plus adopté en avril 2026. Voir arXiv:2505.02279 (Liu et coll., "Un sondage des protocoles d'interopérabilité des agents") pour la comparaison.

> 截至 2026 年 4 月, A2A est l'accord de coopération le plus étendu adopté.

Le paysage du protocole 2026 s'est stabilisé: A2A pour la collaboration avec les agents, MCP pour les outils, ACP absorbé dans A2A pour la logerie de trajectoires, ANP pour l'identité transnationale.

> Le cadre du protocole de 2026 est déjà stable: A2A utilise l'agent 协作, MCP utilise les outils, ACP  absorbe l'A2A utilise le trajectoire journal, ANP utilise l'organisation en tant que société.

## Construisez-le et mettez-le en œuvre.
```figure
sw-agent-card-discovery
```

## Faites-le

`code/main.py`met en œuvre un serveur et un client A2A minimaux en utilisant `http.server`Le serveur:

> `code/main.py`Utilisation `http.server`Et JSON  réaliser A2A 最小服务器和客户端──服务器:

- exposés `/.well-known/agent.json`- Je suis désolé .
  Le récit de la première édition de la série`/.well-known/agent.json`- Je suis désolé .
- accepte `POST /tasks`- Je suis désolé .
  Le mot " accept " est traduit par " accept "`POST /tasks`- Je suis désolé .
- gère l'état des tâches,
  Le gouvernement a décidé de mettre en place un programme de réforme de l'organisation.
- retourne des objets sur `GET /tasks/{id}`- Je suis désolé .
  Dans le texte original,`GET /tasks/{id}`Retour à l'œuvre.

Le client:

> 客户端:

- Il vient chercher la carte d'agent,
  Le nom de l'agent est le nom de l'agent.
- soumet une tâche,
  Nom de l'article
- les sondages jusqu'à leur fin,
  Le temps de la réflexion est terminé.
- Il lit l'artefact.
  Le texte de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la première de la lettre de la lettre de la lettre de la première de la lettre de la première de la lettre

Le script démarre le serveur dans un fil d'arrière-plan, puis le client contre lui. Vous voyez le flux complet: découverte, soumission, sondage, artefact.

> 脚本在后台线程中启动服务器,然后运行客户端──你看完整流程:发现、提交、轮询、工件──

## Utilisez-le avec le cadre de réalisation

`outputs/skill-a2a-integrator.md`Il propose une intégration A2A: contenu de la carte d'agent, schémas de tâches, choix d'auteur, streaming et sondage.

> `outputs/skill-a2a-integrator.md`设计 A2A 集成:Agent 卡片内容、任务模式、认证选择、流式 vs 轮询──

## Envoyez-le . Produit .

Liste de contrôle:

> 检查清单:

- **Pin the spec version.**A2A est toujours en cours d'élaboration. La carte d'agent doit déclarer la version du protocole.
  Le mot grec traduit par " le mot grec "**固定规范版本。**A2A  est toujours en cours d'élaboration                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                 
- **Idempotent task creation.**Les répétitions de soumissions (réessayes réseau) devraient produire une seule tâche.
  Le mot grec traduit par " le mot grec "**幂等任务创建。**Réponse: Il faut qu'il y ait une tâche.
- **Artifact schemas.**Déclarer les formes que le vendeur retourne; les consommateurs doivent valider.
  Le mot grec traduit par " le mot grec "**工件模式。**声明 Agent 返回什么形状;消费者应验证──
- **Rate limits + auth.**A2A est ouvert au public; appliquez la sécurité Web standard.
  Le mot grec traduit par " le mot grec "**速率限制 + 认证。**A2A 面向公众; appliquer les normes de sécurité Web
- **Dead-letter for failed tasks.**Inspecter les modèles au fil du temps pour les types de défaillances récurrentes.
  Le mot grec traduit par " le mot grec "**失败任务死信。** avec le temps de l'examen mode pour trouver les types de défaillance réapparaissant à nouveau 

## Les exercices

1. On court .`code/main.py`Confirmez que le client découvre le serveur et reçoit l'artefact correct.
   Le mot " l' économie " est traduit par " l' économie ".`code/main.py` Confirmer que le serveur du client a trouvé et reçu les tâches exactes 
2. Ajouter une deuxième compétence au serveur (par exemple, " résumer "). Mise à jour de la carte d'agent. Écrivez un client qui choisit la compétence en fonction du type de tâche.
   Le service est un service de communication qui est un service de communication.
3. Implementer un point final de diffusion SSE: `/tasks/{id}/events`Qu'est-ce que le client doit faire différemment ?
   Le mot de passe est "translation".`/tasks/{id}/events`Qu'est-ce que le client doit faire différemment ?
4. Lisez les spécifications A2A. Identifiez trois choses que les spécifications exigent que cette démo ne soit pas mise en œuvre.
   Les trois éléments de la définition de la norme sont:
5. Comparez A2A (découverte de carte d' agent) à MCP (liste de capacités côté serveur via `listTools`Quelle est la différence entre les agents qui se décrivent eux-mêmes et ceux qui testent leurs capacités?
   Le code de la carte de crédit est un code de crédit.`listTools`Quelle est la différence entre l'agent et la capacité de recherche ?

## Les termes clés

| Term | What people say | What it actually means |
|------|----------------|------------------------|
| A2A | "Agent-to-agent" / "Agent 对 Agent" | Peer protocol for agents to call other agents across systems. Google 2025. / Agent 跨系统调用其他 Agent 的对等协议。Google 2025。 |
| Agent Card / Agent 卡片 | "The agent's business card" / "Agent 的名片" | JSON at `/.well-known/agent.json` describing skills, endpoints, auth. / 描述技能、端点、认证的 JSON。 |
| Task / 任务 | "The unit of work" / "工作单元" | Async stateful object with a lifecycle; artifacts produced on completion. / 具有生命周期的异步有状态对象；完成时产生工件。 |
| Artifact / 工件 | "The result" / "结果" | Typed output: text, structured JSON, image, video, audio. First-class media. / 类型化输出：文本、结构化 JSON、图像、视频、音频。一等媒体。 |
| Opaque lifecycle / 不透明生命周期 | "How it's solved is the agent's business" / "如何解决是 Agent 的事" | Client sees state transitions; server is free to choose framework/tools. / 客户端看到状态转换；服务器自由选择框架/工具。 |
| Discovery / 发现 | "Finding the agent" / "找到 Agent" | `GET /.well-known/agent.json` returns the card. / 返回卡片的 GET 请求。 |
| MCP vs A2A | "Tools vs peers" / "工具 vs 对等" | MCP: vertical agent <-> tool. A2A: horizontal agent <-> agent. / MCP：垂直 Agent <-> 工具。A2A：水平 Agent <-> Agent。 |
| ACP / ANP / NLIP | "Sibling protocols" / "兄弟协议" | Adjacent specs; A2A is the most-adopted 2026. / 相邻规范；A2A 是 2026 年采用最广泛的。 |

## Encore une lecture

- [A2A specification](https://a2a-protocol.org/latest/specification/) la spécificité canonique
  Le mot " autorité " est traduit par " autorité ".
- [Google Developers Blog — A2A announcement](https://developers.googleblog.com/en/a2a-a-new-era-of-agent-interoperability/) Le lancement en avril 2025
  中文翻译:Google 开发者博客  A2A 公告  2025 年 4 月发布文章
- [A2A GitHub repo](https://github.com/a2aproject/A2A) Implémentations de référence et KDD
  Le code de gestion de la gestion de données est le code de gestion de données.
- [Liu et al. — A Survey of Agent Interoperability Protocols](https://arxiv.org/html/2505.02279v1) Comparaison des PAM, ACP, A2A, PAN
  Le code de conduite est un code de conduite qui est utilisé pour la gestion de la sécurité.
