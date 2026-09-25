# Le protocole de contexte (MCP)

> MCP donne à un hôte d'IA un protocole pour découvrir et invoquer des outils, des ressources et des invites. La révision 2026-07-28 rend ce protocole stéréotique: la capacité et le contexte de version voyagent avec chaque demande, pas dans une poignée de main liée à la connexion.

> **【中文解读】**MCP  donne à l'IA hôte un ensemble de protocoles unifiés pour trouver et utiliser des outils, des ressources et des suggestions modèles.

> **【拓展：MCP→Phase 13 深入路线】**Ce cours est le premier contact systémique de MCP: donner un modèle de protocole et un minimum de réalisation.

>  **【前置】**Pour les résultats de la phase 11, il est nécessaire de définir les résultats de la phase 2.`initialize`La main et le bras`Mcp-Session-Id`L'idée de la nouvelle version a été supprimée. Si vous avez appris l'ancienne version, effacez d'abord ces souvenirs.

**Type:** Build | **类型:** 构建
**Languages:** Python | **语言:** Python
**Prerequisites:** Phase 11 · 09 (Function Calling), Phase 11 · 03 (Structured Outputs) | **前置知识:** Phase 11 · 09（函数调用）、Phase 11 · 03（结构化输出）
**Time:** ~75 minutes | **时间:** 约 75 分钟

## Objectifs d'apprentissage

- Distinguer un hôte, client, serveur, transport et serveur primitif de MCP.
  Le service est un service de communication et de communication.
- Construire une demande JSON-RPC avec les métadonnées requises par MCP 2026-07-28.
  Le projet de loi de 2026-07-28 doit être intégré dans le JSON-RPC.
- Utilisation `server/discover`pour inspecter les versions, l'identité et les capacités.
  Le mot " usage " est traduit par " usage "`server/discover`探测服务器的版本、身份与能力──
- Retournez les résultats typés et conscients du cache à partir d'outils, de ressources et de demandes.
  Traduction anglaise: de l'outil, des ressources et des suggestions avec les résultats des types de marque et de la mise en cache de suggestions.
- Expliquez comment le MCP sans État moderne interagit avec les serveurs de l'ère des poignées de main.
  Traduction anglaise: expliquer moderne sans état MCP 如何与握手时代的旧服务器互操作──
- Choisissez l'état sécurisé, le transport et les limites d'approbation pour un serveur.
  Pour le serveur choisir l'état de sécurité, la transmission et l'approbation.

## Le problème , l' introduction du problème

Votre application a besoin d'une requête de base de données, d'une opération de calendrier et d'un lecteur de fichiers. Sans un protocole partagé, chaque hôte d'IA a besoin de découverte personnalisée, d'invocation, d'erreurs, de transport et de colle d'autorisation pour ces mêmes capacités.

> Votre application nécessite des requêtes de base de données, des opérations de calendrier et des documents de lecture.

Le MCP réduit cette matrice d'intégration. Un serveur publie une surface JSON-RPC standard. Un client conforme peut découvrir la surface, la présenter à un modèle ou à un utilisateur, l'invoquer et interpréter le résultat sans adaptateur spécifique au serveur.

> MCP a réduit cette matrice intégrée. Le serveur publie une interface standard JSON-RPC.

Le MCP standardise la communication. Il ne décide pas à quel outil le modèle doit appeler, rendre le contenu non fiable sûr ou transformer une demande sans statut en un état d'application durable. Votre hôte et votre serveur possèdent toujours ces décisions.

> Un facteur clé facilement négligeable: le MCP ne fait que normaliser la communication. Il ne décide pas du modèle à utiliser, ne fera pas de contenu incroyable une sécurité, ne fera pas de requête de non-état un état d'application durable. Ces décisions restent à votre hôte et serveur.

>  **【类比】**MCP 像"电源插座国标"──没有国标时,每台电器配种插头,出一次国家要买一次转接头;有国标,一个插座通吃所有电器──但国标不关心你插插的是风机还是电钻电安全(审批、鉴定权)

## Le concept de base.

![MCP host, stateless request, and server primitives](../assets/mcp-architecture.svg)

### Les trois serveurs primitifs

1. **Tools**Chaque outil a un nom, une description, une entrée de schéma JSON et un gestionnaire.
2. **Resources**sont nommés, contenu adressé à l'URI qu'un client peut lire.
3. **Prompts**sont des modèles réutilisables qu'un hôte peut exposer à un utilisateur.

L'hôte est l'application d'IA. Un client MCP à l'intérieur de cet hôte parle à un serveur. Le transport transporte des messages JSON-RPC entre eux.

> L'hôte est l'application de l'IA elle-même; un clientèle MCP à l'intérieur de l'hôte ne peut interagir qu'avec un serveur; le niveau de transmission entre les deux est le déplacement de JSON-RPC 消息── note: clientèle: serveur = 1:1" nécessite plusieurs serveurs lorsqu'il est connecté à plusieurs clients──

### Les demandes de stateless remplacent la poignée de main

> **【中文解读】**Cette section est le plus grand changement de la nouvelle version de la norme:`initialize`La main dans la main,`notifications/initialized`Et le processus de mise en place de l'accord est de mettre en place des procédures de mise en œuvre des mesures de mise en œuvre des mesures de mise en œuvre des mesures de mise en œuvre de la politique de sécurité.`params._meta`(accord version ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙`_meta`、缺必填字段或类型不对 → `-32602`; version format legal mais le serveur n' est pas pris en charge → `-32022`Il y a une autre.

Le MCP 2026-07-28 est retiré `initialize`et `notifications/initialized`Il supprime également les sessions au niveau du protocole.`params._meta`- Le numéro de la liste:

```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "method": "tools/list",
  "params": {
    "_meta": {
      "io.modelcontextprotocol/protocolVersion": "2026-07-28",
      "io.modelcontextprotocol/clientCapabilities": {},
      "io.modelcontextprotocol/clientInfo": {
        "name": "lesson-client",
        "version": "1.0.0"
      }
    }
  }
}
```

La version du protocole et les capacités du client sont nécessaires.`_meta`, un champ requis manquant ou un champ requis avec le type incorrect est malformé et renvoie des paramètres invalides (`-32602`                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             `UnsupportedProtocolVersionError`(le secteur de l'énergie)`-32022`Un serveur peut traiter une demande valide sans récupérer un dossier de négociation antérieur.

L'état de l'application n'est pas maintenu par un programme de connexion, mais il est possible de le faire en fonction de la connexion de l'application.`Mcp-Session-Id`Si un flux de travail a besoin de continuité, le serveur met une poignée opaque et le client passe cette poignée comme argument d'outil ordinaire lors d'appels ultérieurs.

> "Inconnu" n'est pas une application qui ne peut pas avoir d'état, mais un état qui ne peut pas être caché dans un MCP  connexion  ou `Mcp-Session-Id`后面──工作流需要连续性时,由服务器发发发一个不透明句柄 (handled),客户端在后调中把它当普通工具参数传回──鉴权仍然必须逐请求检查──

> ️ **【易错点】**Le code ancien met les données client dans un objet connecté, en envoyant une seule fois à la main.`_meta`Chaque demande doit être reconstruite.

### Découverte et sélection de version

> **【中文解读】** `server/discover`C'est une option obligatoire pour la nouvelle version du serveur: retourner la version prise en charge, capacités et identité du serveur, et avec`ttlMs`- Je suis là.`cacheScope`缓存提示──双时代客户端在studio 上先用 `server/discover`探测: recevoir les résultats de la découverte ou identifier les erreurs modernes`-32022`) explique que le serveur moderne; rencontrer des erreurs indétectables ou des surtemps permet de revenir à 2025-11-25 `initialize`Le vieux processus est un code de compatibilité, pas un code moderne.

Chaque serveur moderne implémentera `server/discover`. Le résultat annonce les versions, les capacités et l'identité du serveur pris en charge:

```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "result": {
    "resultType": "complete",
    "supportedVersions": ["2026-07-28"],
    "capabilities": {
      "tools": {},
      "resources": {},
      "prompts": {}
    },
    "ttlMs": 3600000,
    "cacheScope": "public",
    "_meta": {
      "io.modelcontextprotocol/serverInfo": {
        "name": "demo-server",
        "version": "1.0.0"
      }
    }
  }
}
```

Un client peut appeler une autre méthode directement et gérer une erreur de version, mais la découverte rend explicite l'affichage des capacités et la sélection de version. Une version non prise en charge retourne `UnsupportedProtocolVersionError`avec code `-32022`Les données de ce rapport contiennent:`supported`, une série de révisions de serveur, et `requested`, la révision rejetée.

En studio, un client de double époque sonde avec`server/discover`Un résultat de découverte ou une erreur moderne reconnue comme`UnsupportedProtocolVersionError`Toute erreur ou délai qui n'est pas reconnu comme moderne permet de revenir à 2025-11-25`initialize`Le comportement hérité est le code de compatibilité, pas le code par défaut moderne.

### Les résultats sont explicites.

> **【中文解读】**Chaque résultat central est à portée de main.`resultType`- Le numéro de la liste:`complete`(操作完成) ou `input_required`(il faut que le client revienne et retourne selon le mode MRTR; le serveur central ne permet que de`tools/call`- Je suis là.`resources/read`- Je suis là.`prompts/get`Il est en train de se faire remarquer.`resultType`Les résultats doivent être conformes`complete`处理──列表/读取结果还带 `ttlMs`Avec `cacheScope` définitivité référencement + nouvelle tendance à faire en sorte que le client puisse enregistrer en toute sécurité,并提升快速缓存命中率──

Chaque résultat de base 2026-07-28 a`resultType`- Le numéro de la liste:

- `complete`signifie que l'opération est terminée.
- `input_required`signifie que le serveur a besoin d'un autre voyage aller-retour à travers le modèle de demandes de plusieurs voyages aller-retour.`tools/call`- Je suis là .`resources/read`ou `prompts/get`- Je suis désolé .

Les clients doivent traiter un résultat hérité qui omet `resultType`comme complète.

Les serveurs doivent inclure `io.modelcontextprotocol/serverInfo`dans chaque résultat `_meta`Cette identité est auto-déclarée et est destinée à l'affichage, à l'enregistrement et au débogage, et non à des décisions de sécurité.

Liste et résultats de lecture aussi porter `ttlMs`et `cacheScope`- Une déterministe .`tools/list`ordre plus un indice de fraîcheur permet aux clients de mettre en cache la découverte en toute sécurité et améliore la stabilité du cache rapide. `cacheScope: public`autorise la mise en cache partagée; `private`Il est possible de les réutiliser dans le contexte de l'appel.

### Le format de fil et le transport.

> **【中文解读】**线格式仍是JSON-RPC 2.0。现代 Streamable HTTP 唯暴露一个接受 POST的端点,每条 JSON-RPC 消息独立一个 POST; request POST 的响应是一个 JSON对象或一条请求级 SSE 流;通知 POST 被接受时返回 HTTP 202 空响应体──2026-07-28 里没有独立 GET 流、没有 DELETE 会话端点、没有`Mcp-Session-Id`Il n'y a pas de`Last-Event-ID`Révision des modifications de la politique de l'emploi`subscriptions/listen`POST( Répondre à la demande de réception

MCP utilise JSON-RPC 2.0 sur stdio ou HTTP par flux.

- Une demande a été faite `jsonrpc`- Je suis là .`id`- Je suis là .`method`, et `params`- Je suis désolé .
- Une réponse a la correspondance `id`et soit `result`ou `error`- Je suis désolé .
- Une notification n' a pas été faite `id`et ne s'attend à aucune réponse.

Une requête POST reçoit soit un objet JSON, soit un flux d'événements Server-Sent qui se termine avec la réponse finale. Une notification acceptée POST reçoit HTTP 202 sans corps de réponse; cette révision de base ne définit aucune notification client-serveur sur Streamable HTTP.

Il n'y a pas de flux GET de MCP indépendant, de point d'extrémité de session DELETE, `Mcp-Session-Id`ou `Last-Event-ID`Les notifications de changement de longue durée utilisent une`subscriptions/listen`POST dont la réponse reste ouverte comme un flux SSE.

### Entrée du client sans requêtes initiées par le serveur. Aucun serveur n'a activé la requête client entrée

> **【中文解读】**旧规范允许服务器反向发请求(`sampling/createMessage`- Je suis là.`roots/list`- Je suis là.`elicitation/create`);现行协议改用 MRTR(Multiple demandes de retour): tool调用返回 `resultType: input_required`Il y a aussi`inputRequests`- Je suis là.`requestState`, clientèle collect input après utilisation**新的 JSON-RPC ID**重试原方法并携带 `inputResponses`, comme ça ,`requestState` Roots/Sampling/Logging  encore disponible mais abandonné  nouvelle réalisation ne pas refaire usage, priorité avec des fichiers/répertoires explicites 、 ressources URI 和直连模型供应商──

Les versions antérieures permettent à un serveur d' envoyer des requêtes telles que `sampling/createMessage`- Je suis là .`roots/list`ou `elicitation/create`Le protocole actuel utilise des demandes de plusieurs voyages ronds à la place.`resultType: input_required`avec au moins un des`inputRequests`ou `requestState`. Le client recueille toute entrée demandée, réessaye la méthode d'origine avec un nouvel ID JSON-RPC et le correspondant `inputResponses`, et fait écho à l' exact`requestState`Si vous n'avez pas été fourni`inputRequests`Si vous étiez présent, la nouvelle tentative est omise.`inputResponses`- Je suis désolé .

Les racines, l'échantillonnage et l'enregistrement restent fonctionnels mais sont dépassés, de sorte que les nouvelles mises en œuvre ne devraient pas les adopter.`inputRequests`, jamais comme requêtes JSON-RPC indépendantes du serveur au client. préférer des paramètres de fichier ou de répertoire explicites, des URIs de ressources, la configuration du serveur et l'intégration directe du fournisseur de modèles.

```figure
mcp-nxm-collapse
```

## Construisez-le en main

> **【中文解读】**五步构建:(1) 注册服务器接口面(工具/资源/提示);(2) 给每个请求附加 `_meta`Il n'y a pas de connexion entre les données.`server/discover`- Je ne sais pas .`tools/list`;(4) HTTP   远程调用时带上与请求体镜像的路由头`MCP-Protocol-Version`- Je suis là.`Mcp-Method`- Je suis là.`Mcp-Name`),头体不一致 → HTTP 400 + `-32020`;(5) Placez la sécurité à l'extérieur de l'état de l'accordpour chaque demande de reconnaissance de droitl'hôte local 绑定 + Origine 校验`destructiveHint`标记破坏性工具并要求宿主审批──

### Étape 1: enregistrer une surface serveur. Étape 1: enregistrer l'interface serveur.

L'enregistrement reste simple même si le contrat de demande a été modifié:

```python
server = MCPServer("demo-server")

@server.tool(
    "add",
    "Add two integers.",
    {
        "type": "object",
        "properties": {
            "a": {"type": "integer"},
            "b": {"type": "integer"}
        },
        "required": ["a", "b"]
    }
)
def add(a: int, b: int) -> dict:
    return {"sum": a + b}
```

La mise en œuvre expédiée en `code/main.py`Il utilise délibérément la bibliothèque standard pour que vous puissiez voir chaque enveloppe plutôt que de déléguer le protocole à un SDK.

### Étape 2: joindre des métadonnées à chaque demande.

```python
def request(method, params=None):
    body_params = dict(params or {})
    body_params["_meta"] = {
        "io.modelcontextprotocol/protocolVersion": "2026-07-28",
        "io.modelcontextprotocol/clientCapabilities": {},
        "io.modelcontextprotocol/clientInfo": {
            "name": "demo-client",
            "version": "1.0.0"
        }
    }
    return {
        "jsonrpc": "2.0",
        "id": 1,
        "method": method,
        "params": body_params
    }
```

Ne mettez pas ces métadonnées en cache uniquement dans un objet de connexion. Le serveur les valide à chaque demande.

### Étape 3: Découvrez optionnellement avant de la liste.

Appel`server/discover`, choisissez une version prise en charge, puis appelez `tools/list`- Une direct .`tools/list`est également valable si vous connaissez déjà la version et que vous pouvez gérer `-32022`- Je suis désolé .

La démo renvoie les listes d' outils en ordre de noms et les attache `ttlMs`- Je suis là .`cacheScope`- Je suis là .`resultType`Un appel d'outil renvoie un résultat complet, non caché parce que sa sortie peut dépendre de l'état actuel.

### Étape 4: Mettre la même requête en HTTP.

Une télécommande .`tools/call`POST comprend des en-têtes qui reflètent le corps JSON-RPC:

```http
POST /mcp HTTP/1.1
Content-Type: application/json
Accept: application/json, text/event-stream
MCP-Protocol-Version: 2026-07-28
Mcp-Method: tools/call
Mcp-Name: add
```

Le `MCP-Protocol-Version`l' en-tête doit correspondre à la version de `_meta`- Je suis là .`Mcp-Method`est requis pour chaque demande JSON-RPC et doit correspondre `method`- Je suis là .`Mcp-Name`est nécessaire uniquement pour `tools/call`- Je suis là .`resources/read`, et `prompts/get`, où il doit correspondre au nom de l'outil, à l'URI de ressource ou au nom de la requête.`HeaderMismatch`code `-32020`- Je suis désolé .

### Étape 5: Faire respecter la sécurité en dehors du protocole.

- Valider l'autorisation et le public sur chaque requête HTTP.
- Lier les serveurs locaux à localhost et valider `Origin`sur le HTTP par flux.
- Marquez les outils mutants avec `destructiveHint: true`et nécessitent l'approbation de l'hôte.
- Passer le répertoire et la portée du fichier explicitement au lieu de dépendre des racines dépassées.
- Traiter les ressources et les résultats des outils comme des données non fiables.
- Garder la stdout réservée à JSON-RPC sous stdio; écrire des diagnostics à stderr.

## Utilisez-le pour la vérification .

Exécutez la leçon de son répertoire:

```bash
python3 code/main.py
cd code
python3 -m unittest discover tests -v
```

La première ligne devrait indiquer la découverte de `demo-server`au protocole `2026-07-28`- Alors inspectez .`MCPClient.request`: il reconstruit `_meta`supprimer les métadonnées d'une demande et observer le serveur la rejeter.

## Envoyez-le .

`outputs/skill-mcp-server-designer.md`Il est nécessaire de trouver un résultat de découverte, une politique de métadonnées par requête, des listes déterministes de cache-conscients, des manipulations explicites de l'état, des en-têtes de transport, des règles d'autorisation et d'approbation.

## Continuez à plonger profondément dans le MCP

Cette leçon vous donne le modèle de protocole.

1. [MCP Tool Contracts and Content](../../../13-tools-and-protocols/28-mcp-tool-contracts-and-content/docs/en.md)couvre les schémas d'entrée fermés, le contenu structuré, les métadonnées de routage, la pagination opaque, l'autorisation de termination et la différence entre les erreurs de protocole et de domaine d'outil.
2. [MCP Reliability, Cancellation, and Flow Control](../../../13-tools-and-protocols/29-mcp-reliability-cancellation-and-flow-control/docs/en.md)couvre l'annulation de la demande, l'annulation durable de la tâche, les délais, l'idempotence, la contre-pression, le tampon de proxy et le comportement de reconnexion.
3. [MCP Registry Supply Chain, Admission, Drift, and Rollback](../../../13-tools-and-protocols/30-mcp-registry-supply-chain-and-drift/docs/en.md)couvre la preuve de l'espace de noms, l'origine des artefacts, les broches immuables, le dérivé en direct, l'état du registre, les preuves d'admission et le retour en arrière.
4. [MCP Conformance Engineering](../../../13-tools-and-protocols/31-mcp-conformance-versioning-and-operations/docs/en.md)couvre les transcriptions de fil dorées et négatives, les âges de version stricts, les différentiels SDK, les preuves par procuration, la rédaction, les portes de santé et le retour de sortie.

Suivez-les dans l'ordre où le serveur franchira une frontière d'équipe ou de confiance. Ensemble, ils passent de la méthode fonctionne à le contrat reste sécurisé et diagnostique par déploiement.

## Des exercices.

1. Ajouter un `subtract`outil et confirmer `tools/list`reste dans l'ordre alphabétique.
2. Retirez la clé de version du protocole et vérifiez les paramètres invalides (`-32602`Envoyez alors la version bien formée mais non soutenue `2025-11-25`, vérifier `-32022`, confirme`requested`Il est possible de choisir entre les deux.`supported`- Je suis désolé .
3. Ajouter un serveur-minté `draftId`Expliquez pourquoi c'est l'état de l'application plutôt qu'une session de protocole.
4. Retour `input_required`En cas de besoin de confirmation par l'utilisateur, essayez à nouveau l'appel original avec un nouvel identifiant, un `inputResponses`l'entrée, et l'excès `requestState`au lieu d'inventer une demande JSON-RPC serveur-client.
5. Décrire un client de studio à deux époques. Traiter un résultat ou une erreur reconnue moderne comme moderne, et permettre le retour à l'erreur.`initialize`uniquement pour une erreur ou un délai non reconnu.

## Les termes clés

| Term | What people say | What it actually means |
|------|-----------------|------------------------|
| MCP | "Tool protocol for LLMs" | JSON-RPC protocol for server discovery, tools, resources, prompts, and extensions |
| Host | "The AI app" | Owns the model and UI and mounts one or more MCP clients |
| Client | "The connector" | Speaks MCP to one server on behalf of a host |
| Stateless MCP | "No session" | Every request carries version and capabilities; no protocol state is keyed by a connection |
| `server/discover` | "Capability probe" | Required server method advertising versions, capabilities, and identity |
| `resultType` | "Result state" | Marks a result as `complete` or `input_required` |
| State handle | "Workflow id" | Server-minted application identifier passed as an ordinary argument |
| Streamable HTTP | "Remote transport" | One POST endpoint with JSON or request-scoped SSE responses |
| MRTR | "Ask and retry" | Input request embedded in a result, followed by a retry of the original operation |

## Encore une lecture

- [MCP 2026-07-28 key changes](https://modelcontextprotocol.io/specification/2026-07-28/changelog)
- [MCP server discovery](https://modelcontextprotocol.io/specification/2026-07-28/server/discover)
- [MCP Streamable HTTP](https://modelcontextprotocol.io/specification/2026-07-28/basic/transports/streamable-http)
- [MCP Multi Round-Trip Requests](https://modelcontextprotocol.io/specification/2026-07-28/basic/patterns/mrtr)
- [MCP deprecated features](https://modelcontextprotocol.io/specification/2026-07-28/deprecated)
