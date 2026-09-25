# Les gens dans le cercle: proposition-commission

> Le consensus de 2026 sur le HITL est spécifique. Il ne s'agit pas de "l'agent demande, l'utilisateur clique sur Approuver". Il s'agit de proposer-et-engager: l'action proposée est maintenue dans un magasin durable avec une clé d'idempotence; apparaît à un examinateur avec intention, lignée de données, autorisations touchées, rayon d'explosion et plan de rétroaction; n'est engagée qu'après une reconnaissance positive; vérifiée après exécution pour confirmer l'effet secondaire qui s'est effectivement produit. Le LangGraph `interrupt()`Plus le point de contrôle PostgreSQL, le Microsoft Agent Framework `RequestInfoEvent`, et Cloudflare's `waitForApproval()`La méthode de défaillance canonique est l'approbation du timbre en caoutchouc: "Approuver?" est cliqué sans examen.

> **【中文解读】**2026 année HITL 共识是具体的──不是"Agent 问, user点击 Approve"──是提出-then-commit:提议动作以等键持久化到持久存储;向审查员呈现意图、数据谱系、触及权限、爆炸半径、回滚计划;仅在正面确认后提交;执行后验证确认副作用实际发生──`interrupt()`Ajouter PostgreSQL 检查点、Microsoft Agent Framework `RequestInfoEvent`Les éclairs de nuage`waitForApproval()`Il est vrai que les résultats obtenus sont les mêmes.

> **【拓展：四个状态机步骤】**Propose-then-commit is four step state机:(1) 提议Agent 产生动作,以等键持久化带意图/数据谱系/触及权限/爆炸半径/回滚计划;(2) 呈现审查员(人类, non agent 自审) voir所有元数据;(3) 提交正面确认,动作执行;(4) 验证执行后回读副作用确认──这是数据库`RETURNING`- Je suis désolé.`PutObject`后 `GetObject`、Stripe/AWS API 等键模式在代理 审批上的复用──

**Type:** Learn | **类型:** 学习
**Languages:** Python (stdlib, propose-then-commit state machine with idempotency) | **语言:** Python（标准库，带幂等的提议-提交状态机）
**Prerequisites:** Phase 15 · 12 (Durable execution), Phase 15 · 14 (Tripwires) | **前置知识:** Phase 15 · 12（持久执行），Phase 15 · 14（触发器）
**Time:** ~60 minutes | **时间:** ~60 分钟

>  **【前置】**Je suis en train de faire une étude sur la façon dont les données peuvent être utilisées pour la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion
>  **【类比】**Propose-then-Commit = "bank大额转账审批"――普通 LLM 调用 = 即时转账(错了找客服);Propose-then-Commit = 提交转账申请(含收款人、金额、用途、回滚预案)→ 审查员看元数据 → 批准 → 执行 → 验证到账──每一步都不能省──这是人类计算机使用、Claude Code Plan Mode、Stripe API 等的键统一模式──
> ️ **【易错点】**"Approuver?" 弹窗被用户惯性点"是" → 皮章失效──修复:(1) 多选清单(每个动作独立确认);(2) 强制延迟(3秒倒计时);(3) 关键动作双确认(输入金额数字);(4) 显示"爆炸半径"(影响 N 个文件、M 个用户) ・・・

## Le problème , l' introduction du problème

> **【中文解读】**Le modèle de "proposition-et-commission" exige que l'agent génère d'abord un programme de modification mais ne l'exécute pas immédiatement, mais qu'il le montre à l'utilisateur ou à un autre agent, et qu'il le examine, et qu'il le soumette après avoir examiné.

> **【拓展：propose then commit】**Le modèle de soumission de code est la pratique de sécurité standard de l'agent de code de 2026  Le code de Claude  utilisation par défaut de ce modèle  génération de modifications  suggestions et attendues confirmation par l'utilisateur  Le mécanisme de PR/MR de Git est également l'application de ce modèle  modification du code de premier plan, après examen  réintégration  Dans le cas d'agent  en bas, ce modèle est particulièrement important, car les erreurs de l'agent peuvent être plus destructives que les erreurs humaines 

Un agent prend une action. L'utilisateur doit décider: approuver ou non. Si la décision est instantanée, il ne s'agit probablement pas d'une révision.

> L'agent doit décider: approuver ou non approuver. Si la décision est immédiate, il ne peut pas y avoir d'examen.

Si la décision est structurée, elle est lente mais fiable.

> Si la décision est structurée, elle est lente mais crédible. La question de l'ingénierie est de savoir comment faire de la révision structurée le moyen le plus simple d'opposition.

Le modèle HITL de l'ère 2023 était une demande synchrone: " L'agent veut envoyer un courriel à X avec le corps Y  approuver ? " L'utilisateur clique sur Approuver. Tout le monde sent que le système est sûr.

> 2023 时代 HITL 模式是同步提示:"Agent doit envoyer un courrier à X,正文 Y批准?" utilisateur cliquez sur Approuver。 Tout le monde se sent système de sécurité。

> **【中文解读】**Ce chapitre présente le concept et la méthode de réalisation de l'agent d'IA. L'agent est un système autonome à action de la MLL, capable d'observer l'environnement, de penser, de prendre des décisions, d'exécuter des actions et de les faire boucler jusqu'à la fin de l'objectif.

Le modèle 2026 propose-et-commet déplace HITL sur un substrat durable, attache des métadonnées structurées et nécessite un engagement positif.

> En 2026, le modèle proposé-et-commité HITL  sera transféré à la base de données persistante, ajoutée structurée, exige une soumission directe

Chaque SDK géré par un agent envoie une version: LangGraph `interrupt()`, Microsoft Agent Framework `RequestInfoEvent`, Cloudflare `waitForApproval()`Les noms des API diffèrent, mais pas la forme.

> Chaque agent de surveillance SDK est envoyé.`interrupt()`、Microsoft Agent Framework `RequestInfoEvent`Cloudflare`waitForApproval()`◊API 名称不同;形态不。

## Le concept de base.

### La machine de proposer puis de faire

1. **Propose.**L'agent produit une action proposée. Persiste à un stock durable (PostgreSQL, Redis, Object Durable).
   Le mot grec traduit par " le mot grec "**提议。**L'agent 产生提议动作──持久化到持久存储(PostgreSQL、Redis、Durable Object) ── comprend:
   - intention (pourquoi l'agent fait-il cela)
     L'agent pour quoi faire ça ?
   - lignée des données (quelle source a conduit à cette proposition)
     Le texte de la loi est le texte de la loi.
   - permissions touchées (quels champs / fichiers / points d'extrémité)
     Le mot "références" est traduit par "références".
   - rayon d'explosion (qui est le pire cas)
     Le pire des cas est quoi ?
   - plan de réouverture (si engagé, comment le faire annuler)
     Le projet de loi est en cours de révision.
   - clé d'idempotence (unique par proposition; la réintroduction renvoie le même enregistrement)
     Le texte est écrit en français.
2. **Surface.**Le réviseur voit la proposition avec toutes les métadonnées.
   Le mot grec traduit par " le mot grec "**呈现。**Le contrôleur voit avec tout le données de la proposition.
3. **Commit.**L'action est exécutée.
   Le mot grec traduit par " le mot grec "**提交。**Il est en train de s'exécuter.
4. **Verify.**Après l'exécution, l'effet secondaire est lu et confirmé. Si l'étape de vérification échoue, le système est dans un mauvais état connu et l'alerte s'engage.
   Le mot grec traduit par " le mot grec "**验证。** Après exécution des effets secondaires sont reconnus  Si les étapes de vérification échouent, le système est dans un état de malformation connu et lance un alerte

### La clé de l'indépendance

Sans clé d'idempotence, une nouvelle tentative après une défaillance transitoire peut dupliquer une action approuvée.

> 等键, reessais de la situation après l'échec possible double exécution déjà approuvé 

Exemple concret: l'utilisateur approuve le "transfert de 100 $ de A à B. " Blip réseau. Workflow retries. L'utilisateur a approuvé une fois mais le transfert est exécuté deux fois. La clé d'idempotence lie l'approbation à un seul effet secondaire unique; la deuxième exécution est un no-op.

> 具体例:用户批准"从A 转 $100到B"──网络闪断──工作流重试──用户批准一次但转账执行两次──等键将批准绑定到单一唯一副作用;第二次执行是无-op──

C'est le même schéma d'idempotence que Stripe et AWS utilisent.

> C'est le même modèle utilisé par Stripe et AWS API.

### Durabilité: pourquoi les approbations surpassent les processus ?

La salle d'attente d'approbation est un état qui ne appartient pas à l'agent. Le flux de travail est arrêté (leçon 12).`interrupt()`avec PostgreSQL checkpointing et pas seulement l'état de mémoire  une approbation deux jours plus tard trouve toujours le flux de travail intact.

> 批准等候室是代理 不拥有一片状态――工作流暂停――第 12 课)――批准到达时,工作流从该精确点恢复――这就是为什么LangGraph将`interrupt()`L'accord de mise en œuvre de PostgreSQL est toujours en cours et ne se limite pas à l'état de l'inventaire.

### Les approbations de la marque de caoutchouc et l'atténuation des défis et des réponses

L'interface utilisateur par défaut pour HITL ("Approuver" / "Réjecter") produit des approbations rapides sans révision authentique.

> HITL 默认 UI("Approuver"/"Réjecter" 按)产生快速批准无真审查──已记录缓解:在 Approuver 按启动前要求对特定问题正面回答的挑战-响应清单──具体形状:

- "Vous comprenez quelle ressource cela touche ?
  Vous savez ce que c'est que cette histoire ?
- "Avez-vous vérifié que le rayon de l'explosion est acceptable ?
  Le mot "explosion" est traduit par "explosion".
- "Avez-vous un plan de reprise si cela échoue ?
  Le mot "si tu as perdu, tu as un plan de retour ?"

La fonction de contrôle de l'HITL est une méthode de contrôle de l'agence de sécurité Anthropic citant explicitement le HITL comme une atténuation des modèles d'approbation des timbres de caoutchouc.

> Il est nécessaire de faire en sorte que les données soient disponibles et que les données soient disponibles à des utilisateurs qui ont besoin de l'information.

### Ce qui compte comme conséquent, c'est ce qui compte.

Toutes les actions ne nécessitent pas de propos puis d'engagement.

> Il faut proposer et ensuite s'engager.

- **Consequential actions**(souvent HITL): écritures irréversibles, transactions financières, communication en sortie, modifications de base de données de production, opérations destructives du système de fichiers.
  Le mot grec traduit par " le mot grec "**后果性动作**(总 HITL): non-réversible, opérations financières, échanges de données, production de bases de données, changements de données, opérations de systèmes de documents.
- **Reversible actions**(parfois HITL): modification des fichiers locaux, changements de mise en scène env, écriture réversible avec un retour en arrière clair.
  Le mot grec traduit par " le mot grec "**可逆动作**(Quelques fois HITL): 本地文件编辑、舞台化 环境变更、带清晰回滚的可逆写──
- **Reads and inspections**(ne jamais HITL): lire un fichier, énumérer des ressources, appeler une API à lecture seule.
  Le mot grec traduit par " le mot grec "**读和检查**(de l'origine: le texte de l'article)

### La vérification après l'action

"L'exécution de commit" n'est pas la même que "l'effet secondaire est arrivé". Les conditions de partition réseau et de course peuvent produire un flux de travail qui pense avoir réussi alors que le backend n'a pas persisté.`RETURNING`clauses ou AWS `GetObject`après `PutObject`- Je suis désolé .

> " La mise en œuvre de la soumission " n'est pas égale à " l'apparition de effets secondaires ".`RETURNING`                                                                                                                                                                                                                                                              `PutObject`后 `GetObject`Les modèles AWS sont similaires.

### Article 14 de la loi sur l'IA de l'UE

L'article 14 impose une surveillance humaine efficace des systèmes d'IA à haut risque dans l'UE. "Efficace" n'est pas décoratif. Le langage réglementaire exclut spécifiquement les modèles de timbre en caoutchouc.

> La mise en œuvre de la politique de surveillance des données est une priorité pour la gestion des données et la gestion des données.

## Utilisez-le avec le cadre de réalisation
```figure
mx-propose-then-commit
```

## Utilisez-le

`code/main.py`Le pilote simule trois cas: un flux d'approbation propre, une réessaye après un échec transitoire (qui ne doit pas être exécuté à double exécution) et un tampon en caoutchouc par défaut par rapport à un flux de défi et de réponse.

> `code/main.py`Il est également possible de modifier le code de base de Python pour une mise à jour de la base de données.

## Envoyez-le . Produit .

`outputs/skill-hitl-design.md`examine un flux de travail proposé de l'HITL pour proposer la forme et les indicateurs de la méta-données manquantes, des couches d'idempotence, de vérification ou de défi-réponse.

> `outputs/skill-hitl-design.md`审查提议 HITL 工作流的建议-然后-承诺 形态并标记缺失的元数据、等、验证或挑战-响应层──

## Les exercices

1. On court .`code/main.py`- Confirmer que la nouvelle tentative d'une proposition approuvée utilise le dossier durable et ne réexécute pas.
   Le mot " l' économie " est traduit par " l' économie ".`code/main.py` confirmer que la proposition a été approuvée et qu'elle a été utilisée à nouveau pour une durée de durée indéterminée et non réélevée.

2. Extension du dossier de proposition par un `rollback`Simuler une exécution dont la étape de vérification échoue.
   Le mot " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " "`rollback`字段扩展提议记录──模拟验证步骤失败的执行──展示回滚自动触发──

3. Lisez le cadre d'agents de Microsoft `RequestInfoEvent`Identifiez un champ de métadonnées l'API inclut que le moteur de jouet manque. Ajoutez-le et expliquez de quoi il protège.
   Le code de la société Microsoft Agent Framework`RequestInfoEvent`文档──识别 API 包含而玩具引擎缺失的一个元数据字段──添加它并解释它防止什么──

4. Conceptez une liste de défis et réponses pour une action spécifique (par exemple, "poster sur un compte Twitter public").
   Pour répondre à ces trois questions, le réviseur doit répondre à quelles ?

5. Choisissez un cas où une requête synchrone " Approuver " serait suffisante (aucun magasin durable n'est nécessaire). Expliquez pourquoi et nommez la classe de risque que vous acceptez.
   Le mot "approuver" est un mot qui signifie "approuver".

## Les termes clés

| Term | What people say | What it actually means |
|---|---|---|
| 术语 | 通俗说法 | 实际含义 |
| Propose-then-commit | "Two-phase approval" | Persisted proposal + positive commit + verify |
| Propose-then-commit | "两阶段批准" | 持久提议 + 正面提交 + 验证 |
| Idempotency key | "Retry-safe token" | Unique per proposal; second execution no-ops |
| 幂等键 | "重试安全 token" | 每提议唯一；第二次执行 no-op |
| Data lineage | "Where it came from" | The specific source content that led to the proposal |
| 数据谱系 | "它从哪来" | 导致提议的特定源内容 |
| Blast radius | "Worst case" | Scope of effect if the action goes wrong |
| 爆炸半径 | "最坏情况" | 动作出错时的影响范围 |
| Rubber-stamp | "Fast approval" | "Approve" clicked without genuine review |
| 橡皮章 | "快速批准" | 无真实审查地点击"Approve" |
| Challenge-and-response | "Forcing checklist" | Reviewer must positively acknowledge specific questions |
| 挑战-响应 | "强制清单" | 审查者必须正面确认特定问题 |
| RequestInfoEvent | "MS Agent Framework primitive" | Durable HITL request with structured metadata |
| RequestInfoEvent | "MS Agent Framework 原语" | 带结构化元数据的持久 HITL 请求 |
| `interrupt()` / `waitForApproval()` | "Framework primitives" | LangGraph / Cloudflare equivalents of the same shape |
| `interrupt()` / `waitForApproval()` | "框架原语" | 相同形态的 LangGraph / Cloudflare 等价物 |

## Encore une lecture

- [Microsoft Agent Framework — Human in the loop](https://learn.microsoft.com/en-us/agent-framework/workflows/human-in-the-loop) `RequestInfoEvent`, approbations durables.
  Le mot grec traduit par " le mot grec "`RequestInfoEvent`Il est toujours approuvé.
- [Cloudflare Agents — Human in the loop](https://developers.cloudflare.com/agents/concepts/human-in-the-loop/) `waitForApproval()`et objets durables.
  Le mot grec traduit par " le mot grec "`waitForApproval()`Et les objets durables
- [Anthropic — Measuring agent autonomy in practice](https://www.anthropic.com/research/measuring-agent-autonomy) HITL comme atténuation du risque à long terme.
  En français, le mot "HITL" est traduit par "HITL".
- [EU AI Act — Article 14: Human oversight](https://artificialintelligenceact.eu/article/14/) base réglementaire pour les systèmes à haut risque.
  Traduction anglaise: 高风险系统的监管基线──
- [Anthropic — Claude's Constitution (January 2026)](https://www.anthropic.com/news/claudes-constitution) le cadre constitutionnel en ce qui concerne la surveillance.
  Le texte de la loi est le texte de la loi.
