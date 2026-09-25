# Héritage de la FIPA-ACL et des lois sur le discours

> Avant MCP, avant A2A, il y avait FIPA-ACL. En 2000, la Fondation IEEE pour les agents physiques intelligents a ratifié un langage de communication d'agent avec vingt performatifs, deux langages de contenu et un ensemble de protocoles d'interaction  contrat net, abonnement/notification, demande-quand. Il a disparu de l'industrie parce que les coûts généraux ontologiques étaient trop lourds pour le Web, mais le réveil LLM des systèmes multi-agents réimplemente tranquillement les mêmes idées sans la sémantique formelle: les contrats JSON représentent les performatifs, le langage naturel représente les ontologies. Cette leçon prend au sérieux la FIPA-ACL pour que vous puissiez voir quelles décisions du protocole 2026 sont réinventées, quelles sont les nouveautés, et où la vague actuelle va redécouvrir les problèmes déjà résolus dans les années 2000.

> **【中文解读】**Le protocole de communication de l'agence et du système de communication de l'ACL est un protocole de communication et de communication de contenu, qui a été réélaboré en 2026 par les MCP/A2A/ACP.

> **【拓展：FIPA ACL 遗产→具体应用】**FIPA ACL (Fondation pour la communication avec les agents physiques intelligents) est un standard de communication de l'agent de plusieurs années 1990-2000 . Bien que l'organisation de FIPA ait disparu en 2013, son idée centrale est la communication standardisée.

>  **【前置】**Pour les étudiants, il est nécessaire de se préparer à la phase 16 du programme de formation (Phase 16·01 ((pourquoi besoin de plus d'agents) Phase 13 ((MCP/instrument protocole)  Le cours est un cours d'histoire  Comprendre le protocole de formation en matière de formation en matière de formation en matière de formation en matière de formation en matière de formation en matière de formation en matière de formation en matière de formation en matière de formation en matière de formation en matière de formation en matière de formation en matière de formation en matière de formation en matière de formation en matière de formation en matière de formation en matière de formation en matière de formation en matière de formation en matière de formation en matière de formation en matière de formation en matière de formation en matière de formation en matière de formation en matière de formation en matière de formation en matière de formation en matière de formation en matière de formation en matière de formation en matière de formation en matière de formation en matière de formation en matière de formation en matière de formation en matière de formation en matière de formation en matière de formation en matière de formation en matière de formation en matière de formation en matière de formation en éducation en éducation en éducation en éducation en éducation en éducation en éducation en éducation en éducation en éducation en éducation en éducation en éducation en éducation en éducation en éducation en éducation en éducation en éducation en éducation en éducation en éducation en éducation en éducation en éducation en éducation en éducation en éducation en éducation en éducation en éducation en éducation en éducation en éducation en éducation en éducation en éducation en éducation en éducation en éducation en éducation en éducation en éducation en éducation en éducation en éducation en éducation en éducation en éducation en éducation en éducation en éducation en éducation en éducation en éducation en éducation en éducation en éducation en éducation en éducation en éducation en éducation en éducation en éducation en éducation en éducation en éducation en éducation en éducation en éducation en éducation en éducation en éducation en éducation en éducation en éducation en éducation en éducation en éducation en éducation en éducation en éducation en éducation en éducation en éducation en éducation en éducation en éducation

>  **【类比】**FIPA-ACL = "AI 界的拉丁语"── 2000 年的标准,2026 年的协议(MCP/A2A) 大量继承其思想──区别:FIPA 用形式化本体(重)、现代协议用 JSON+自然语言(轻)──学历史的价值:避免重复覆FIPA 因为"本体太重"而死,现代协议要保持轻量──

**Type:** Learn | **类型:** 学习
**Languages:** Python (stdlib) | **语言:** Python（标准库）
**Prerequisites:** Phase 16 · 01 (Why Multi-Agent) | **前置知识:** Phase 16 · 01（为什么需要多 Agent）
**Time:** ~60 minutes | **时间:** 约 60 分钟

## ♪ Problème ♪ Introduction du problème ♪

> **【中文解读】**Le protocole d'agence de 2026 semble être en train de se développer.

Le paysage du protocole d'agent 2026 est occupé: MCP pour les outils, A2A pour les agents, ACP pour l'audit des entreprises, ANP pour la confiance décentralisée, NLIP pour le contenu en langage naturel, plus CA-MCP et deux douzaines de propositions de recherche.

> Le domaine du protocole Agent de 2026 est très populaire: MCP utilise des outils, A2A utilise des agents, ACP utilise des audits d'entreprise, ANP utilise des décentralisations de confiance, NLIP utilise des contenus de langage naturel, ainsi que CA-MCP et plus de vingt propositions de recherche. Chaque norme se déclare fondée.

La lecture honnête est que la plupart d'entre eux redécouvrent un arbre de décision très spécifique de vingt ans. La théorie des actes de discours d'Austin (1962) et de Searle (1969) nous a donné " les déclarations sont des actions. " KQML (1993) a transformé cela en un protocole de câble. FIPA-ACL (ratifié en 2000) a produit la normalisation de référence: vingt performatives, langages de contenu SL0/SL1, protocoles d'interaction pour le réseau de contrat et les abonnés-notifiants. JADE et JACK étaient les plateformes de référence Java. L'effort s'est évanoui vers 2010 parce que les coûts ontologiques étaient trop lourds et que le web gagnait.

> La plupart d'entre elles sont en train de redécouvrir un arbre de décision très spécifique de vingt ans. La théorie du comportement des mots de Austin (1962) et Searle (1969) nous dit que " la parole est un acte " (KQML) (1993) va être transformée en un accord de ligne (FIPA-ACL) 2000 approuvée) a donné lieu à une normalisation de référence: vingt actions de construction (SL0/SL1) pour le marché des liens entre le réseau et les abonnements.

Quand vous regardez MCP `tools/call`En effet, les données de référence de la FIPA sont les données de référence de la CA-MCP, et elles sont les données de référence de la CA-MCP.

> Quand vous examinez MCP `tools/call`、Le cycle de vie des missions d'A2A ou le stockage de la CA-MCP, vous voyez une récitation plus souple de la décision de FIPA 、 JSON originaire.

## Concept Le concept central

> **【中文解读】**Le programme de communication est basé sur la communication de données et de données, et il est également possible de les utiliser pour les informations et les informations nécessaires.

### Actes de discours, en un paragraphe

> **【中文解读】**Une phrase de la théorie est basée sur la phrase: certaines phrases ne sont pas dans la description du monde, mais dans le changement du monde. Searle les a divisées en cinq catégories.

Austin a remarqué que certaines phrases ne décrivent pas le monde, mais le changent. "Je promets. " "Je demande. " "Je déclare". Il appelait ces déclarations performatives. Searle a formalisé cinq catégories: affirmative, directive, commissaire, expressive et déclarative. KQML (Finin et coll., 1993) a rendu cela opérationnel pour les agents logiciels: un message est un performatif (l'action) plus un contenu (de quoi l'action parle). FIPA-ACL a nettoyé les lacunes de KQML et standardisé environ vingt performatives.

> Austin note que certaines phrases ne décrivent pas le monde elles changent le monde""My promise"",My request"",I announce", il appelle ces phrases pour construire des choses

### Les vingt performances de la FIPA (liste partielle)

| Performative | Intent |
|---|---|
| `inform` | "I tell you P is true" |
| `request` | "I ask you to do X" |
| `query-if` | "Is P true?" |
| `query-ref` | "What is the value of X?" |
| `propose` | "I propose we do X" |
| `accept-proposal` | "I accept the proposal" |
| `reject-proposal` | "I reject the proposal" |
| `agree` | "I agree to do X" |
| `refuse` | "I refuse to do X" |
| `confirm` | "I confirm P is true" |
| `disconfirm` | "I deny P" |
| `not-understood` | "Your message did not parse" |
| `cancel` | "Cancel the ongoing X" |
| `cfp` | "Call for proposals on X" |
| `subscribe` | "Notify me when X changes" |
| `failure` | "I tried X and failed" |

La liste complète est disponible `fipa00037.pdf`Le point est que chacun d'eux correspond à un protocole primitif qu'un LLM ajoute finalement.

> 完整列表在 `fipa00037.pdf`(FIPA ACL 消息结构) 中── l'accent n'est pas mis sur la mémoire mais sur chacun de nous qui s'attache à un accord LLM 最终会重新添加的原语──

### Message canonique FIPA-ACL

> **【中文解读】**Il n' y a que sept étiquettes.`content`Je suis en train de vous dire:`conversation-id`et `reply-with`Les requêtes-réponse sont des requêtes qui sont toujours réinventées dans le système moderne; sans elles, il est impossible de transformer plusieurs cycles en échange.

```
(inform
  :sender       agent1@platform
  :receiver     agent2@platform
  :content      "((price IBM 83))"
  :language     SL0
  :ontology     finance
  :protocol     fipa-request
  :conversation-id   conv-42
  :reply-with   msg-17
)
```

Sept champs contiennent l'enveloppe du protocole; un champ (`content`Le reste des champs sont exactement ce que vous réinventez chaque fois que vous renforcez les essais, le fillage et l'ontologie sur un protocole JSON.

> 七个字段承载协议信封; un seul épisode`content`Le reste des sections est exactement ce que vous allez réessayer chaque fois, les lignes et le corps ajoutés au protocole JSON sont réinventés.

### Les deux plates-formes héritées

**JADE**(Java Agent DEvelopment framework, 19992020s) était le temps d'exécution le plus utilisé conforme à la FIPA. Les agents ont étendu une classe de base, échangé des messages ACL, exécuté à l'intérieur des conteneurs et coordonné en utilisant des "comportements".

> **JADE**(Java Agent 开发框架, 1999-2020 年代) est le plus courant FIPA 兼容运行时.

**JACK**(Software orienté vers les agents, commercial) a mis l'accent sur le raisonnement BDI (Crédition-Desei-Intention) en plus des messages FIPA.

> **JACK**(Software orienté aux agents, produits commerciaux) souligne que les investissements en investissement (BDI) sont basés sur les informations de la FIPA (confiance- volonté-intention)

Les deux ont diminué une fois que la pile Web a mangé des cas d'utilisation multi-agents.

> Une fois que le Web 技术 absorbé plusieurs agents utilisateurs, par exemple, les deux ont décliné.

### Pourquoi la FIPA a disparu

- **Ontology overhead.**La FIPA a exigé une ontologie partagée pour analyser `content`L'accord sur les ontologies est un processus de normes de plusieurs années.
  Le mot grec traduit par " le mot grec "**本体开销。**FIPA  besoin de partager cette résolution `content` On a réalisé un consensus sur le Web en utilisant HTTP + JSON
- **Formal semantics nobody used.**SL (langue sémantique) a donné des conditions de vérité rigoureuses, mais la plupart des systèmes de production utilisaient du contenu sous forme libre et ignoraient le formalisme.
  Le mot grec traduit par " le mot grec "**没人用的形式语义。**SL (语义语言) offre des conditions de vraie valeur strictes, mais la plupart des systèmes de production utilisent le contenu du format libre et ignorent le formalisme.
- **Tooling lock-in.**JADE était uniquement en Java, Jack était commercial.
  Le mot grec traduit par " le mot grec "**工具锁定。**JADE 仅支持Java;JACK 是商业的多语言团队绕过了两者──
- **The internet won the stack.**REST, puis JSON-RPC, puis gRPC a remplacé le transport de l'ACL.
  Le mot grec traduit par " le mot grec "**互联网赢得了技术栈。**REST, puis JSON-RPC, puis gRPC remplacé la transmission ACL.

### Le renouveau de la LLM est FIPA-lite

> **【中文解读】**Pour le FIPA `request`et MCP `tools/call`Il s'agit d'une série de programmes de recherche et de développement de programmes de recherche et de développement de l'information, qui sont en cours de développement et qui sont en cours de développement.

Comparer une FIPA `request`à un PCM `tools/call`- Le numéro de la liste:

> La FIPA `request`Avec MCP `tools/call` pour faire la comparaison:

```
(request                                {
  :sender  agent1                         "jsonrpc": "2.0",
  :receiver tool-server                   "method":  "tools/call",
  :content "(lookup stock IBM)"           "params":  {"name":"lookup_stock",
  :ontology finance                                   "arguments":{"symbol":"IBM"}},
  :conversation-id c42                    "id": 42
)                                        }
```

La même enveloppe, syntaxe différente. Les deux portent: qui, qui, intention, charge utile, identité de corrélation.

> Les deux sont liés par un même code de mots: qui, qui, qui, qui, qui, qui, qui, qui, qui, qui, qui, qui, qui, qui, qui, qui, qui, qui, qui, qui, qui, qui, qui, qui, qui, qui, qui, qui, qui, qui, qui, qui, qui, qui, qui, qui, qui, qui, qui, qui, qui, qui, qui, qui, qui, qui, qui, qui, qui, qui, qui, qui, qui, qui, qui, qui, qui, qui, qui, qui, qui, qui, qui, qui, qui, qui, qui, qui, qui, qui, qui, qui, qui, qui, qui, qui, qui, qui, qui, qui, qui, qui, qui, qui, qui, qui, qui, qui, qui, qui, qui, qui, qui, qui, qui, qui, qui, qui, qui, qui, qui, qui, qui, qui, qui, qui, qui, qui, qui, qui, qui, qui, qui, qui, qui, qui, qui, qui, qui, qui, qui, qui, qui, qui, qui, qui, qui, qui, qui, qui, qui, qui, qui, qui, qui, qui, qui, qui, qui, qui, qui, qui, qui, qui, qui, qui, qui est, qui, qui, qui, qui, qui est, qui, qui, qui, qui, qui, qui est, qui, qui est, qui, qui est, qui, qui, qui, qui est, qui, qui est, qui, qui, qui, qui, qui, qui est, qui est, qui, qui est, qui est, qui est, qui, qui est, qui, qui, qui est, qui est, qui est, qui, qui, qui est, qui est, qui est, qui est, qui est, qui, qui, qui est, qui est, qui, qui, qui est, qui est, qui est, qui, qui est, qui est, qui est, qui est, qui est, qui est, qui est, qui est, qui est, qui est, qui est, qui est, qui est, qui est, qui est, qui est, qui est, qui est, qui est, qui est, qui est, qui est,

L'enquête de 2025 de Liu et coll. ("A Survey of Agent Interoperability Protocols: MCP, ACP, A2A, ANP", arXiv:2505.02279) rend cette lignée explicite: MCP correspond aux actes de parole utilisés par les outils, A2A aux actes de parole par les agents, ACP aux actes de parole auditifs, ANP aux extensions d'identité décentralisée.

> Liu et d'autres personnes ont souligné clairement ce schéma: MCP à l'aide d'outils de traitement pour l'utilisation des mots, A2A à l'aide d'agents de traitement pour les autres mots, ACP à l'aide de trajets de traitement des mots, ANP à l'aide d'identités décentralisées.

### Le compromis, clairement déclaré

> **【中文解读】**权衡要明说:FIPA 给形式语义(可证明) 规范施事行为目录(不用重辩) 带正确性保证的交互协议模式;现代规范给 JSON 原生载荷、自然语言内容、Web 传输、能力发现──交换的就是"更松散的意图语义换更容易实现"──

**What FIPA gave you and modern specs drop:**

> **FIPA 给你的而现代规范丢弃的：**

- La sémantique formelle, vous pouvez la prouver.`inform`implique que l'expéditeur croit au contenu.
  Vous pouvez prouver`inform`Cela signifie que l'expéditeur doit croire ce contenu.
- Un catalogue canonique des performatifs  vous n'avez pas à réaffirmer "nous devrions avoir un `cancel`Je suis là.
  Le récit de la loi est un récit de la loi.`cancel`Vous êtes là ?
- Décennie de modèles d'interaction-protocole  contract-net, abonnez-notifiez, proposez-acceptez  avec des propriétés de précision connues.
  Le modèle de protocole de communication de décennies 合同网、订阅-通知、提议-接受具有已知正确性属性──

**What modern specs give you and FIPA did not:**

> **现代规范给你的而 FIPA 没有的：**

- Charges utiles natives JSON compatibles avec tous les outils modernes.
  Le texte original de la traduction chinoise est JSON.
- Contenu en langage naturel que les LLM peuvent interpréter sans ontologie codée à la main.
  L'enseignement de la langue étrangère peut être interprété sans code manuel.
- Le transport par pile Web (HTTP, SSE, WebSocket).
  Le site Web est un réseau de téléphonie mobile.
- Découverte des capacités via MCP en direct `server/discover`et les cartes d'agent A2A.
  Le MCP est en train de se développer.`server/discover`Avec une carte d'agent A2A, vous pouvez effectuer une recherche.

Une sémantique plus flexible pour une mise en œuvre plus facile.

> En plus de la réflexion, il est plus facile de réaliser.

### Protocoles d'interaction qui valent la peine d'être portés

> **【中文解读】**FIPA 约15 交互协议里,三个值搬进 LLM 多 Agent 系统:合同网,应应Fase 16·16 协商) 订阅/通知 ((每个事件总线) 请求-当(持久工作流引擎的延迟任务,应Fase 16·22) 它们都能干净映射到现代消息队列、HTTP + 轮询或SSE 流──

FIPA a envoyé ~ 15 protocoles d'interaction.

> La FIPA a publié environ 15 accords de coopération.

1. **Contract Net Protocol (CNP).**Problèmes de gestion `cfp`(appel à propositions); les soumissionnaires répondent par `propose`Le processus de négociation est le plus souvent utilisé pour les négociations.
   Le mot grec traduit par " le mot grec "**合同网协议 (CNP)。**管理者发布 `cfp`(征求提案);投标者使用 `propose`响应;管理者接受/拒绝──这是典型任务市场模式(Phase 16 · 16 协商)──
2. **Subscribe/Notify.**L' abonné envoie `subscribe`; l' éditeur envoie `inform`C'est chaque bus d'événements en 2026.
   Le mot grec traduit par " le mot grec "**订阅/通知。**订阅者发送 `subscribe`; éditeur en changement de thème `inform`C'est la ligne de chaque événement de l'année 2026.
3. **Request-When.**"Faire X lorsque la condition Y est valide". Action retardée avec des préconditions.
   Le mot grec traduit par " le mot grec "**请求-当。**" lorsque les conditions Y 成立时执行 X── " avec la préposition des conditions de retardation.

Chaque carte est propre sur les files d'attente de messages modernes, les sondages HTTP + ou le streaming SSE.

> Chaque message peut être clairement cartographié à la file d'attente moderne, HTTP + 轮询 ou SSE 流.

### Ce qui se brise quand on laisse tomber l'ontologie

> **【中文解读】**Le prix de la perte de corps est**语义漂移**Deux agents ont des concepts très différents pour le même mot "client" et le receveur accepte les mêmes concepts selon les erreurs de compréhension.`content`S'ajouter à JSON Schema 类型化工件  A2A  信封里

Sans ontologie partagée, les agents déduisent le sens du contenu du langage naturel.**semantic drift**: deux agents utilisent le même mot (`"customer"`En effet, les données de l'analyse de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur

> 没有共享本体,Agent du contenu de la langue naturelle 记录在案的2026年失败模式是**语义漂移**Deux agents pour le même mot`"customer"`Il existe des concepts très différents, l'agent de réception est basé sur une mauvaise compréhension de l'action, aucun modèle de vérificateur ne peut le capturer.

L'atténuation sans avoir recours à l'ontologie complète:

> Les mesures de soulagement non entièrement utilisées:

- Schéma JSON sur `content` rejette les erreurs structurelles du fil.
  Pour le premier jour de l'année`content`Utilisation de schéma JSON dans le niveau de transmission rejeter l'erreur structurelle.
- Les objets de type (A2A)  rejettent la mauvaise modalité.
  Le type de matériel de construction est le type de matériel de construction.
- Le performatif explicite dans l'enveloppe  rend l'intention sans ambiguïté même lorsque le contenu est un langage naturel.
  Le contenu est aussi clair.

### Les spécifications 2026 correspondant au patrimoine de l'acte de la parole

| Modern spec | FIPA analog | What it keeps | What it drops |
|---|---|---|---|
| MCP `tools/call` | `request` | explicit intent, correlation id | formal semantics, ontology |
| MCP `resources/read` | `query-ref` | explicit intent, correlation id | formal semantics |
| A2A Task lifecycle | contract-net + request-when | async lifecycle, state transitions | formal completeness guarantees |
| A2A streaming events | subscribe/notify | async push | typed-predicate subscription |
| CA-MCP shared context | blackboard (Hayes-Roth 1985) | multi-writer shared memory | logical consistency model |
| NLIP | natural-language content | LLM-native | schema |

En lisant le tableau de haut en bas, le modèle est: conservez la structure primitive, abandonnez le formalisme, laissez les LLM traiter l'ambiguïté.

> De haut en bas, le modèle est: conserver la structure originale, abandonner le formalisme, faire LLM 弥补模糊性.

> **【中文解读】**Une phrase总结全表:2026 规范保留的是结构性原语(显式意图、关联 id、异步生命周期), abandonné est形式主义(形式语义、本体、逻辑一致性), avec la capacité d'explication de LLM pour remplir les歧义── c'est un échange explicite de "l'efficacité de démonstration de l'interaction à bas prix"―

```figure
sw-contract-net
```

## Construisez-le et mettez-le en œuvre.

> **【中文解读】**Le code de l'exemple est une base de données FIPA-ACL 翻译器:把五条 MCP/A2A 风格消息编码成 FIPA-ACL 再解码回来,并跑一个"一个管理员 + 三投标者"玩具合同网协商――输出并排显示相同消息的2026 JSON 形态和FIPA-ACL 形态和一些协议原语在往返中存活,只有语法不同――

`code/main.py`Il décode et décode l'enveloppe ACL canonique et montre comment chaque forme de message MCP / A2A se réduit aux mêmes sept champs.

> `code/main.py`实现 un pur standard library FIPA-ACL 翻译器──它编解码标准ACL 信封,并展示每个MCP / A2A 消息形状如何简化为相同的七段──演示内容:

- Encode cinq messages de type MCP et A2A en FIPA-ACL.
  Le code de l'information est FIPA-ACL.
- Décode FIPA-ACL à l'équivalent moderne.
  Le texte de la loi est le texte de la loi de l'Union européenne.
- Fonctionne dans un contrat de jouet négociation net entre un gestionnaire et trois soumissionnaires en utilisant `cfp`- Je suis là .`propose`- Je suis là .`accept-proposal`- Je suis là .`reject-proposal`- Je suis désolé .
  Le mot " usage " est traduit par " usage "`cfp`- Je suis là.`propose`- Je suis là.`accept-proposal`- Je suis là.`reject-proposal`Un accord de négociation entre un gestionnaire et trois soumissionnaires est mis en place.

Je vais courir .

```
python3 code/main.py
```

La sortie est une trace côte à côte montrant chaque message moderne dans sa forme JSON 2026 et sa forme FIPA-ACL, puis un aller-retour d'une offre de réseau de contrat.

> 输出是一个并排追踪, afficher chaque 条现代消息的 2026 JSON 形式和FIPA-ACL 形式, puis être le retour du contract.

## Utilisez-le avec le cadre de réalisation

`outputs/skill-fipa-mapper.md`Il est également possible de lire les spécifications du protocole d'agent et de produire le cartographie FIPA-ACL.`inform`avec la syntaxe JSON ? "

> `outputs/skill-fipa-mapper.md`C'est une compétence, lire n'importe quel agent  protocole de réglementation et générer FIPA-ACL 映射── utiliser avant l'adoption du nouveau protocole pour répondre: "C'est vraiment nouveau, ou avec JSON 语法 `inform`Je suis là.

## Envoyez-le . Produit .

> **【中文解读】**Ne pas ressusciter la FIPA-ACL, ne pas la réviser:

Ne ramenez pas la FIPA-ACL, ramenez sa liste de contrôle:

> Ne ramène pas le FIPA-ACL.

- Quelle est l'intention primitive (performative) de chaque message?
  Le mot "je suis" est traduit en français par "je suis".
- Y a-t-il une identification de corrélation pour la réponse à la demande et l'annulation ?
  Est-ce qu'il existe un identifiant associé utilisé pour la demande-réponse et l'annulation ?
- Y a-t-il un langage de contenu explicite (JSON-RPC, texte simple, artifact de type structuré)?
  Il existe des versions de contenu en ligne, en ligne, en ligne, en ligne, en ligne, en ligne, en ligne, en ligne, en ligne, en ligne, en ligne, en ligne, en ligne, en ligne, en ligne, en ligne, en ligne, en ligne, en ligne, en ligne, en ligne, en ligne, en ligne, en ligne, en ligne, en ligne, en ligne, en ligne, en ligne, en ligne, en ligne, en ligne, en ligne, en ligne, en ligne, en ligne, en ligne, en ligne, en ligne, en ligne, en ligne, en ligne, en ligne, en ligne, en ligne, en ligne, en ligne, en ligne, en ligne, en ligne, en ligne, en ligne, en ligne, en ligne, en ligne, en ligne, en ligne, en ligne, en ligne, en ligne, en ligne, en ligne, en ligne, en ligne, en ligne, en ligne, en ligne, en ligne, en ligne, en ligne, en ligne, en ligne, en ligne, en ligne, en ligne, en ligne, en ligne, en ligne, en ligne, en ligne, en ligne, en ligne, en ligne, en ligne, en ligne, en ligne, en ligne, en ligne, en ligne, en ligne, en ligne, en ligne, en ligne, en ligne, en ligne, en ligne, en ligne, en ligne, en ligne, en ligne, en ligne, en ligne, en ligne, en ligne, en ligne, en ligne, en ligne, en ligne, en ligne, en ligne, en ligne, en ligne, en ligne, en ligne, en ligne, en ligne, en ligne, en ligne, en ligne, en ligne, en ligne, en ligne, en ligne, en ligne, en ligne, en ligne, en ligne, en ligne, en ligne, en ligne, et en ligne, en ligne, en ligne, en ligne, en anglais, en anglais, en anglais, en anglais, en anglais, en anglais, en anglais, " " " " " " " " " " " " " " " " " " " " " " "
- Les protocoles d'interaction sont-ils de première classe, ou vous réimplémenterez le réseau de contrat à partir de zéro ?
  Le protocole de coopération est-il un accord de citoyens égaux ou êtes-vous en train de rétablir le contrat ?
- Que se passe-t-il lorsque deux agents ne sont pas d'accord sur la signification du contenu (drift sémantique)?
  Qu'est-ce qui se passe quand deux agents se séparent pour le contenu ?

Documentez ces cinq questions pour tout nouveau protocole avant de le mettre en production.

> Avant de publier un nouveau protocole sur l'environnement de production, écrivez ces cinq questions:

## Les exercices

1. On court .`code/main.py`- Observer le codage aller-retour. Identifier le performatif FIPA correspondant à `tools/call`- Je suis là .`resources/read`, et la création de tâches A2A.
   Le mot " l' économie " est traduit par " l' économie ".`code/main.py` observer 往返编码  identifier quelles sont les pratiques de l'IFPA 施事对应 `tools/call`- Je suis là.`resources/read`Et les A2A ont des tâches à accomplir.
2. Extension de la démo du réseau de contrat avec un `cancel`Le système de gestion de l'entreprise est un système performatif qui permet au gestionnaire de retirer la tâche à mi-chemin.`cancel`Vous ne résolvez pas ça par vous-même ?
   Le mot " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " "`cancel`施事行为扩展合同网演示, permettre au gestionnaire de retirer les tâches au cours de la soumission.`cancel`- C'est une erreur que vous ne pouvez pas résoudre ?
3. Lire la structure des messages ACL de la FIPA (http://www.fipa.org/specs/fipa00037/) sections 4.14.3. Choisissez un performatif non couvert dans cette leçon et décrivez son analogique JSON-RPC moderne.
   Le texte de la loi est le texte de la loi.http://www.fipa.org/specs/fipa00037/）第4.1-4.3 节──选择本课未涵盖的一个施事行为并描述其现代 JSON-RPC类比──
4. Lisez Liu et coll., arXiv:2505.02279. Pour chacune des MCP, A2A, ACP, ANP, énumérez les familles performatives FIPA qu'elles conservent et déposent.
   Pour chaque membre de la MCP, A2A, ACP, ANP, il est indiqué que les actions de la FIPA sont conservées et abandonnées.
5. Conceptez un schéma JSON minimal pour le `content`champ d' un `request`Ce schéma vous donne quoi que le langage naturel pur ne donne pas, et combien ça coûte ?
   Pour toi dans ton propre système`request`施事行为 `content`字段设计一个最小的JSON-Schema. Ce modèle vous offre un langage pur naturel sans quoi, quel est le prix ?

## Les termes clés

| Term | What people say | What it actually means | 中文术语 |
|------|----------------|------------------------|----------|
| Speech act | "An utterance that does something" | Austin/Searle: utterances as actions. The theoretical parent of ACL. | 言语行为 |
| FIPA | "That old XML thing" | IEEE Foundation for Intelligent Physical Agents. Standardized ACL in 2000. | FIPA 基金会 |
| ACL | "Agent Communication Language" | FIPA's envelope format: performative + content + metadata. | Agent 通信语言 |
| Performative | "The verb" | The intent class of a message: `inform`, `request`, `propose`, `cfp`, etc. | 施事行为 |
| KQML | "FIPA's predecessor" | Knowledge Query and Manipulation Language (1993). Simpler, narrower. | KQML |
| Ontology | "Shared vocabulary" | A formal definition of the concepts the content language talks about. | 本体 |
| SL0 / SL1 | "FIPA content languages" | Semantic Language levels 0 and 1 — the formal content language family. | SL 内容语言 |
| Contract Net | "Task market" | Manager issues cfp; bidders propose; manager accepts. The canonical interaction protocol. | 合同网 |
| Interaction protocol | "Pattern of messages" | A sequence of performatives with known correctness: request-when, subscribe-notify, etc. | 交互协议 |

## Encore une lecture

- [Liu et al. — A Survey of Agent Interoperability Protocols: MCP, ACP, A2A, ANP](https://arxiv.org/html/2505.02279v1) l'enquête canonique de 2025 reliant les spécifications modernes au patrimoine de la FIPA
  Le code de conduite de l'entreprise est le code de conduite de l'entreprise.
- [FIPA ACL Message Structure Specification (fipa00037)](http://www.fipa.org/specs/fipa00037/) le format de l'enveloppe 2000 ratifié
  Traduction anglaise:FIPA ACL 消息结构规范2000年批准的信封格式
- [FIPA Communicative Act Library Specification (fipa00037)](http://www.fipa.org/specs/fipa00037/) le catalogue performatif complet
  Traduction anglaise:FIPA 通信行为库规范完整的施事行为目录
- [MCP specification 2026-07-28](https://modelcontextprotocol.io/specification/2026-07-28) l'équivalent actuel d'utilisation des outils sans état de `request`- Je suis là.`query-ref`
  Le code de conduite de la société civile`request`- Je suis là.`query-ref`d'utilisation et de l'effet
- [A2A specification](https://a2a-protocol.org/latest/specification/) l'équivalent moderne de l'agent-peer de la réseau de contrat et de l'abonnement-notification
  En anglais, le terme " agent moderne " est traduit par " agent moderne " en anglais.
