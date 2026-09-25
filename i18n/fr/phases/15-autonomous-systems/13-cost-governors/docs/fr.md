# Budget d'action, plafonds d'itération et gouvernementaux des coûts

> Le coût mensuel de la formation en droit d'un agent de commerce électronique de taille moyenne a augmenté de $1,200 to $L'agent a trouvé une nouvelle boucle et a continué à dépenser à l'intérieur. Microsoft's Agent Governance Toolkit (April 2, 2026) codifie la défense contre cette classe: par demande `max_tokens`Les commandes de téléphonie mobile, les commandes de téléphonie mobile, les commandes de téléphonie mobile, les commandes de téléphonie mobile, les commandes de téléphonie mobile, les commandes de téléphonie mobile, les commandes de téléphonie mobile, les commandes de téléphonie mobile, les commandes de téléphonie mobile, les commandes téléphoniques, les commandes téléphoniques, les commandes téléphoniques, les commandes téléphoniques, les commandes téléphoniques, les commandes téléphoniques, les commandes téléphoniques, les commandes téléphoniques, les téléphonies, les téléphones portables, les téléphonies, les téléphones portables, les téléphones portables, les téléphones portables, les téléphones portables, les téléphones portables, les téléphones portables, les téléphones portables, les téléphones portables, les téléphones portables, les téléphones portables, les téléphones portables, les téléphones portables, les téléphonies portables, les téléphonies et les téléphonies.

> **【中文解读】**L'équipe de formation de l'agent de commerce électronique de l'entreprise a commencé à utiliser les compétences de suivi des commandes.$1,200 跳到 $4,800── ce n'est pas un bug de fixation de prix── c'est un agent qui trouve un nouveau cycle et continue à y dépenser── Microsoft's Agent Governance Toolkit (WEB`max_tokens`、 chaque tâche de jeton 和美元预算、每日/月上限、代上限、分层模型路由、提示缓存、上下文窗口、昂贵动作上 HITL 检查点、预算违反时的终止开关。Anthropic's Claude Code Agent SDK 以不同名称出货相同原语──金融速度限制例如10分钟内 >$50 切断访问比月度上限更快捕获循环──

> **【拓展：单一上限不够 → 分层栈】**失败模式和时间尺度需要应对:5 秒重试的失控循环 (détention de la température limitée)  2x de la tâche 工作的缓慢泄漏 (détention de la température limitée)  5x de la nouvelle version  5x de la mauvaise diffusion                                                                                                                                                                                                                         

**Type:** Learn | **类型:** 学习
**Languages:** Python (stdlib, layered cost-governor simulator) | **语言:** Python（标准库，分层成本治理器模拟器）
**Prerequisites:** Phase 15 · 10 (Permission modes), Phase 15 · 12 (Durable execution) | **前置知识:** Phase 15 · 10（权限模式），Phase 15 · 12（持久执行）
**Time:** ~60 minutes | **时间:** ~60 分钟

>  **【前置】**Les coûts de gestion des coûts de gestion des coûts de gestion des coûts de gestion des coûts de gestion des coûts de gestion des coûts de gestion des coûts de gestion des coûts de gestion des coûts de gestion des coûts de gestion des coûts de gestion des coûts de gestion des coûts de gestion des coûts de gestion des coûts de gestion des coûts de gestion des coûts de gestion des coûts de gestion des coûts de gestion des coûts de gestion des coûts de gestion des coûts de gestion des coûts de gestion des coûts de gestion des coûts de gestion des coûts de gestion des coûts de gestion des coûts de gestion des coûts de gestion des coûts de gestion des coûts de gestion des coûts de gestion des coûts de gestion des coûts de gestion des coûts de gestion des coûts de gestion des coûts de gestion des coûts de gestion des coûts de gestion des coûts de gestion des coûts de gestion des coûts de gestion des coûts de gestion des coûts de gestion des coûts de gestion des coûts de gestion des coûts de gestion des coûts de gestion des coûts de gestion des coûts de gestion des coûts de gestion des coûts de gestion des coûts de gestion des coûts de gestion des coûts de gestion des coûts de gestion des coûts de gestion des coûts de gestion des coûts de gestion des coûts de gestion des coûts de gestion des coûts de gestion des ressources de gestion des ressources de gestion des ressources de gestion des ressources de gestion des ressources de gestion des ressources de l'État.
>  **【类比】**Coût Gouverneur = "Agent's Credit Card额度"。普通 LLM 调用 = 刷卡(每次小钱);Agent 进入死循环 = 盗刷(一夜烧光)。防御分层:(1) 速度限制10分钟 >$50 切断（防失控）；(2) 每日上限——$200/天(防慢泄漏);$3000/月（防坏发布）；(4) 单任务上限——$5/ tâche (de l'ordre de l'explosion)
> ️ **【易错点】**Il faut avoir une limite de vitesse de courte période + une limite de jour de moyenne période + une limite de longue période de mois + trois niveaux, plus le temps est court, plus le temps est long, plus le temps est long.

## Le problème , l' introduction du problème

> **【中文解读】**Les contrôles de coûts (Gouverneurs de coûts) contrôlent et limitent la consommation de ressources de l'agent principalement l'API 调用费用和代币使用量 没有成本控制器的代理可能在循环或低效执行中产生巨额账单──三种控制策略:(1) 预算上限硬性代币/费用限制;(2) 速度限制每分钟/每小时调用上限;(3) 效率门控 成本/收益比恶化时暂停

> **【拓展：cost governors】**Le contrôle de la valeur est le principal défi de la déploiement de produits d'agents pour les années 2025-2026. Exemple: plusieurs utilisateurs déclarent que l'agence génère des coûts d'API de plusieurs milliers de dollars après avoir été pris au piège du cycle de réparation. Les solutions comprennent: 1) limiter les tokens maximaux de sortie d'OpenAI; 2) suivre l'utilisation de l'API anthropique; 3) contrôler les coûts d'outils tiers tels que Helicone et Braintrust.

Les agents autonomes dépensent de l'argent à chaque tour.

> L'agent autonome en fait de l'argent.

Le mauvais résultat d'un chatbot est une mauvaise réponse; la mauvaise boucle d'un agent est une facture. Le terme documenté par l'industrie pour le mode de défaillance est "Denial of Wallet"  l'agent continue de raisonner, continue d'appeler des outils, continue de facturer, et rien ne l'arrête parce que rien n'a été conçu pour.

> 聊天机器人错误输出是一条错误回复;Agent's errore cycle is a bill. 行业记录的失败模式术语是"Denial of Wallet"Agent 持续推理、持续调用工具、持续计费,没有什么阻止它,因为没有什么被设计制阻止──

La solution n'est pas un seul nombre, mais une pile de limites à différentes échelles de temps et granularités: par demande, par tâche, par heure, par jour, par mois. Une pile bien conçue capture une boucle en cours de route en quelques minutes, une fuite lente en quelques heures et une mauvaise libération en une journée. La même pile maintient un budget quand l'agent est à long horizon et autonome.

> La réparation n'est pas un chiffre. Elle est une limite de mesure et de grille de temps différentes: par requête, par tâche, par heure, par jour, par mois.

> **【中文解读】**Ce chapitre présente le concept et la méthode de réalisation de l'agent d'IA. L'agent est un système autonome à action de la MLL, capable d'observer l'environnement, de penser, de prendre des décisions, d'exécuter des actions et de les faire boucler jusqu'à la fin de l'objectif.

C'est une leçon d'ingénierie: les mathématiques sont triviales, la discipline est où les équipes échouent. La liste des limites ci-dessous est nommée soit dans le Kit d'outils de gouvernance des agents Microsoft ou dans les documents SDK des agents de code Claude Anthropic.

> C'est un cours d'ingénierie: mathématiques ordinaires, le code est un défaut de l'équipe.

## Le concept de base.

### Le coût-gouverneur de la pile.

1. **`max_tokens` per request.**Simple, empêche un appel d'émettre une finition illimitée.
   Le mot grec traduit par " le mot grec "**每请求 `max_tokens`。**简单―― empêcher la seule fois de faire un complément complet
2. **Per-task token budget.**Dans toute la course, ne dépassez pas N. Arrêtez à la limite.
   Le mot grec traduit par " le mot grec "**每任务 token 预算。**L'ensemble du processus ne dépasse pas N 个代币.
3. **Per-task dollar budget.**Comme les jetons, mais en monnaie.`max_budget_usd`dans le code Claude.
   Le mot grec traduit par " le mot grec "**每任务美元预算。**Comparable à la monnaie, mais en devises.`max_budget_usd`Il y a une autre.
4. **Per-tool call cap.**Pas plus de N `WebFetch`Les appels, N `shell_exec`les appels, etc.
   Le mot grec traduit par " le mot grec "**每工具调用上限。**N' excède pas N 个 `WebFetch`Je suis en train de faire une petite histoire.`shell_exec`Il est aussi utilisé.
5. **Iteration cap (`max_turns`).**Iterations de boucle d'agent totale; empêche les boucles de raisonnement infinies.
   Le mot grec traduit par " le mot grec "**迭代上限（`max_turns`）。**总 Agent 循环 代数; empêcher le cycle de la proposition illimitée.
6. **Per-minute / per-hour / per-day / per-month cap.**Des fenêtres en roulement, des fuites à différentes échelles temporelles.
   Le mot grec traduit par " le mot grec "**每分/时/日/月上限。**滚动窗口──在不同时间尺度捕获泄漏──
7. **Financial velocity limit.**Par exemple, "si les dépenses dépassent 50 $ en 10 minutes, coupez l'accès".
   Le mot grec traduit par " le mot grec "**金融速度限制。**Par exemple, "si 10 minutes dans le temps coûtent plus de 50 dollars, coupez la visite"
8. **Tiered model routing.**Par défaut, un modèle plus petit; escalade vers un modèle plus grand seulement lorsqu'un classificateur juge que la tâche le justifie.
   Le mot grec traduit par " le mot grec "**分层模型路由。**默认小模型; seulement lorsque la tâche de jugement des classes est évaluée à un modèle plus grand.
9. **Prompt caching.**Context prompt et stable du système stocké dans le cache du fournisseur; le coût des jetons de réenvoi est proche de zéro.
   Le mot grec traduit par " le mot grec "**提示缓存。**系统提示和稳定上下文存储在供应商缓存; réémission des jetons
10. **Context windowing.**Compaction / résumé pour maintenir le contexte actif en dessous d'un seuil; réduction directe des coûts des jetons.
    Le mot grec traduit par " le mot grec "**上下文窗口。**压缩/摘要 值低于值; direct token 成本降低──
11. **HITL checkpoints on expensive actions.**Avant une action connue pour être coûteuse (long appel à l'outil, téléchargement important, mise à niveau coûteux du modèle), il faut un tapage humain.
    Le mot grec traduit par " le mot grec "**昂贵动作上的 HITL 检查点。**Dans un autre article, nous avons écrit: "Le plus important est de faire des efforts pour améliorer la qualité de l'appareil.
12. **Kill switch on budget breach.**La session est interrompue lorsque des chapeaux sont allumés.
    Le mot grec traduit par " le mot grec "**预算违反时终止开关。**任一上限触发时会话停止──上限被记录;需要单独重新启动路径──

### Pourquoi la pile, pas une seule plaque ? Pourquoi une seule limite ?

Un seul plafond mensuel ne capture un agent fugitif qu'après la disparition du portefeuille. Un seul plafond par demande ne capte rien au niveau de la session.

> 单一月度上限只在钱包空后抓失控代理. 单一每请求上限在会话级别什么也没抓.

- **Runaway loop**(agent coincé dans une reprise de 5 secondes): pris par la limite de vitesse.
  Le mot grec traduit par " le mot grec "**失控循环**(Agent 卡在 5 秒重试): la vitesse limite de capture
- **Slow leak**(agent effectuant ~ 2 fois le travail attendu par tâche): pris par le plafond journalier.
  Le mot grec traduit par " le mot grec "**缓慢泄漏**(Agent à chaque tâche faire environ 2x 预期工作):
- **Bad release**(nouvelle version utilise des jetons 5x): pris par le plafond hebdomadaire / mensuel.
  Le mot grec traduit par " le mot grec "**坏发布**(nouvelle version avec 5x token): chaque semaine / mois
- **Legitimate surge**(réelle demande, pas un bug): pris par le cap horaire / jour avec un journal clair.
  Le mot grec traduit par " le mot grec "**合法激增**(réellement besoin, non bug):小时/日上限带清晰日志捕获──

### La surface budgétaire de Claude Code
### Surface de budget de harnais

Le SDK Claude Code Agent expose (docs publics):

> Claude Code Agent SDK 暴露(公开文档):

- `max_turns` Cap d'itération.
  Le mot grec traduit par " le mot grec "`max_turns`Il y a une limite.
- `max_budget_usd` plafond en dollars; avortements de séance sur violation.
  Le mot grec traduit par " le mot grec "`max_budget_usd`美元上限; violate le temps de réunion suspendu.
- `allowed_tools`- Je suis là .`disallowed_tools` allouliste et denyliste d'outils.
  Le mot grec traduit par " le mot grec "`allowed_tools`- Je suis là .`disallowed_tools` outils permettant la liste et refusant la liste
- Point de crochet avant utilisation de l'outil pour la comptabilité des coûts personnalisée.
  Les coûts de production sont calculés par le système de calcul.

Combinez avec l'échelle en mode autorisation (leçon 10).`autoMode`séance sans`max_budget_usd`L'anthropique définit explicitement le mode automatique comme nécessitant des contrôles budgétaires; le classifiant est orthogonal au coût.

> Avec le pouvoir de mode de classe`max_budget_usd``autoMode`L'interface est autonome. L'interface est autonome.

### La loi sur l'IA de l'UE, les agents OWASP Top 10

Le Kit d'outils de gouvernance des agents de Microsoft couvre les exigences du Top 10 des agents OWASP et de l'article 14 de la Loi sur l'IA de l'UE (surveillance humaine).

> Le programme de gestion des agents de Microsoft couvre le Top 10 des agents OWASP et la loi sur l'IA de l'UE, article 14.

### Les observations $1,200 → $4800 cas observés$1,200 → $4 800 cas

Le cas réel dans les documents de Microsoft: un agent de commerce électronique dont le coût mensuel a triplé après l'ajout d'un nouvel outil.

> Un exemple réel dans le dossier Microsoft: un agent de commerce électronique a augmenté le coût de l'ajout d'un nouvel outil trois fois par mois.

L'outil permettait à l'agent de surveiller l'état des commandes pendant chaque session. Pas de détection de boucle. Pas de plafond par outil. Pas d'alerte sur la croissance semaine après semaine. La correction était un plafond par outil plus une alerte de croissance quotidienne. C'est un modèle: chaque nouvelle surface d'outil est une nouvelle boucle potentielle; chaque nouvel outil a besoin de son propre plafond et de son propre alerte.

> L'outil permet à l'agent de consulter l'état de l'ordre pendant chaque session. Il n'y a pas de contrôle en cycle. Il n'y a pas de limite de chaque outil.

## Utilisez-le avec le cadre de réalisation
```figure
cost-governor-stack
```

## Utilisez-le

`code/main.py`L'agent simulé dérive dans une boucle de vote après quelques tours; la pile de couches le prend dans la fenêtre de vitesse tandis qu'un seul capsule mensuelle ne tirerait que quelques jours plus tard.

> `code/main.py`模拟有和没有分层成本管理的代理运行;模拟代理在某些轮次后漂移到轮询循环;分层在速度窗口内捕获它,而单一级上限直到几天后才触发;

## Envoyez-le . Produit .

`outputs/skill-agent-budget-audit.md`l'audit de la pile de coûts du déploiement d'un agent proposé et détecte les couches manquantes.

> `outputs/skill-agent-budget-audit.md`Le dépôt des coûts de gestion de l'agent du projet de révision a été marqué par une absence de niveau.

## Les exercices

1. On court .`code/main.py`Confirmer la vitesse limite avant le plafond d'itération sur une trajectoire de cycle de sondage. Maintenant désactiver la vitesse limite et mesurer combien l'agent "spend" avant que le plafond d'itération le capture.
   Le mot " l' économie " est traduit par " l' économie ".`code/main.py` La vitesse de confirmation est limitée à la limite de la durée du cycle de la demande.

2. Conceptez un ensemble de plaques de plaques pour chaque outil pour un agent de navigateur (leçon 11). Quel outil a besoin du plaque de plaque le plus serré? Quel outil peut fonctionner sans limite sans risque?
   Pour les utilisateurs de navigateurs, il est nécessaire de créer un système de navigation qui fonctionne à la fois en fonction de la portée de l'appareil et de la portée de l'appareil.

3. Lisez les documents du kit d'outils de gouvernance des agents de Microsoft. Listez chaque type de plafond et les noms du kit d'outils. Mettez chacun dans un des modes d'échec (circuit de fuite, fuite lente, mauvaise sortie, survol).
   Le programme de gestion de l'agent de Microsoft est basé sur le système de gestion de l'agent de Microsoft.

4. Prix d'une opération non surveillée au cours de la nuit pour une tâche réaliste (par exemple, "triage 50 émissions dans un repo").`max_budget_usd`à 2x votre estimation de points.
   Pour les tâches de la société, il est nécessaire de faire des efforts pour obtenir des résultats.`max_budget_usd`Pour vous faire une estimation de 2x...

5. Le code de Claude `max_budget_usd`Des limites de vitesse complémentaires que vous appliquerez à l'extérieur.
   Le code de Claude`max_budget_usd`Dans le cadre de la mise en œuvre de la stratégie de répartition, les coûts de la mise en œuvre seront réduits.

## Les termes clés

| Term | What people say | What it actually means |
|---|---|---|
| 术语 | 通俗说法 | 实际含义 |
| Denial of Wallet | "Runaway bill" | Agent loop generating spend with no cap to stop it |
| Denial of Wallet | "失控账单" | 无上限阻止的 Agent 循环产生花费 |
| max_tokens | "Per-request cap" | Ceiling on a single completion's size |
| max_tokens | "每请求上限" | 单次补全大小上限 |
| max_turns | "Iteration cap" | Ceiling on agent loop iterations in a session |
| max_turns | "迭代上限" | 会话中 Agent 循环迭代数上限 |
| max_budget_usd | "Dollar kill switch" | Session cost cap; aborts on breach |
| max_budget_usd | "美元终止开关" | 会话成本上限；违反时中止 |
| Velocity limit | "Rate cap" | Limit on spend per short window (e.g., $50 / 10 min) |
| 速度限制 | "速率上限" | 短窗口花费限制（例如 $50/10 分钟） |
| Tiered routing | "Small model first" | Cheap model default; escalate only when classifier warrants |
| 分层路由 | "小模型优先" | 默认廉价模型；仅当分类器批准时升级 |
| Prompt caching | "Cached system prompt" | Provider-side cache reduces re-send token cost to near zero |
| 提示缓存 | "缓存系统提示" | 提供商侧缓存将重发 token 成本降至接近零 |
| HITL checkpoint | "Human approval gate" | Human tap required before expensive action |
| HITL 检查点 | "人类批准门" | 昂贵动作前需人类点击 |

## Encore une lecture

- [Anthropic Claude Code Agent SDK — agent loop and budgets](https://code.claude.com/docs/en/agent-sdk/agent-loop) `max_turns`- Je suis là .`max_budget_usd`, les outils de réparation.
  Le mot grec traduit par " le mot grec "`max_turns`- Je suis là.`max_budget_usd`、 outils permettant la liste。
- [Microsoft Agent Framework — human-in-the-loop and governance](https://learn.microsoft.com/en-us/agent-framework/workflows/human-in-the-loop) les points de contrôle des gouvernements des coûts.
  Le prix de la vente est de 0,5%
- [Anthropic — Claude Managed Agents overview](https://platform.claude.com/docs/en/managed-agents/overview) contrôle des coûts du côté du fournisseur.
  Le fournisseur est le contrôleur des coûts.
- [Anthropic — Prompt caching (Claude API docs)](https://platform.claude.com/docs/en/prompt-caching) mécanique de mise en cache.
  Le système de stockage
- [Anthropic — Prompt caching (Claude API docs)](https://platform.claude.com/docs/en/build-with-claude/prompt-caching) mécanique de mise en cache.
- [Anthropic — Measuring agent autonomy in practice](https://www.anthropic.com/research/measuring-agent-autonomy) profil des coûts pour les agents à long horizon.
  Le prix de l'agent est le plus élevé.
