# Les points de contrôle et les roulements de retour.

> Chaque transition de l'état graphique persiste. Quand un travailleur se blesse, son contrat de location expire et un autre travailleur prend la voiture au dernier point de contrôle. Les objets durables Cloudflare conservent l'état pendant des heures ou des semaines. Propose-then-commit (leçon 15) définit un plan de réaction par action. La vérification post-action ferme la boucle. L'article 14 de la Loi sur l'IA de l'UE impose une surveillance humaine efficace pour les systèmes à haut risque  en pratique, cela signifie que les points de contrôle doivent être vérifiables, que les retours doivent être répétés et que le parcours d'audit doit survivre à un déploiement. Le mode défaillance aiguë: sans clés d'idempotence et vérifications des préconditions, une nouvelle tentative après une défaillance transitoire peut dupliquer une action déjà approuvée. La vérification après l'action est ce qui le prend.

> **【中文解读】**Chaque diagramme change d'état de pérennisation. Le travailleur  s'effondre lors de l'expiration de son contrat de location, un autre travailleur  s'éteint  sur le dernier point de contrôle  sur le point de récupération.  Objets durables  sur plusieurs heures ou plusieurs semaines  sur le point de détenir un état de possession.  Propose-then-commitment (article 15) pour chaque action définit un plan de réouverture. sur les opérations  sur les opérations  sur les opérations  sur les opérations  sur les opérations  sur les opérations  sur les opérations  sur les opérations  sur les opérations  sur les opérations  sur les opérations  sur les opérations  sur les opérations  sur les opérations  sur les opérations  sur les opérations  sur les opérations  sur les opérations  sur les opérations  sur les opérations  sur les opérations  sur les opérations  sur les opérations  sur les opérations  sur les opérations  sur les opérations  sur les opérations  sur les opérations  sur les opérations  sur les opérations  sur les opérations  sur les opérations  sur les opérations  sur les opérations  sur les opérations  sur les opérations  sur les opérations  sur les opérations  sur les opérations  sur les opérations  sur les opérations  sur les opérations  sur les opérations  sur les opérations  sur les opérations  sur les opérations  sur les opérations  sur les opérations  sur les opérations  sur les opérations  sur les opérations  sur les opérations  sur les opérations  sur les opérations  sur les opérations  sur les opérations  sur les opérations  sur les opérations  sur les opérations  sur les opérations  sur les opérations  sur les opérations  sur les opérations  sur les opérations  sur les opérations  sur les opérations  sur les opérations  sur les opérations  sur les opérations  sur les opérations  sur les opérations  sur les opérations  sur les opérations  sur les opérations  sur les opérations  sur les opérations  sur les opérations  sur les opérations 

> **【拓展：幂等+前置条件+验证+回滚四件套】**仅等不够: considérer "当余额" > $1000 时从 A 转 $100 à B" de l'opération de réception. Après la réception, seulement les autres contrôles seront passés, mais si A  surplus dans la réforme et la réforme entre une autre opération de réforme et des 500 $, les conditions de réception ne réussiront pas  sans elle sur le déploiement.

**Type:** Learn | **类型:** 学习
**Languages:** Python (stdlib, checkpoint and rollback state machine) | **语言:** Python（标准库，检查点和回滚状态机）
**Prerequisites:** Phase 15 · 12 (Durable execution), Phase 15 · 15 (Propose-then-commit) | **前置知识:** Phase 15 · 12（持久执行），Phase 15 · 15（propose-then-commit）
**Time:** ~60 minutes | **时间:** ~60 分钟

>  **【前置】**Les projets de développement de la société civile et de l'économie de marché sont en cours de réalisation.
>  **【类比】**检查点回滚 = "archive du jeu et读档"――检查点 = "自动存档") = "auto-archive du jeu" (en anglais: "game archives et read档") = "auto-archive du jeu" (en anglais: "game archives et read档") = "auto-archive du jeu" (en anglais: "game archives et read档").
> ️ **【易错点】**只有等键没有前置条件检查 → 重启时余额已被其他流程改了仍执行 → 透支──修复:

## Le problème , l' introduction du problème

> **【中文解读】**Le mécanisme de contrôle et de roulement permet à l'agent de conserver un état rapide pendant le processus d'exécution, de sortir à l'erreur et de se rétablir à un bon état antérieur. Ceci est similaire à la gestion des données de base de données et de la version de Git. Le contrôle de contrôle maintient des nœuds clés, comme avant la modification du fichier.

> **【拓展：checkpoints rollback】**检查点-回滚是可靠的代理 系统的基础设施――实现选择:(1) 文件系统级使用 Git或快照保存文件状态;(2) 数据库级使用事务保证数据一致性;(3) 应用级Agent自我管理检查点(如LangGraph)──关键权衡是检查点粒度太细会增加开销,太粗会丢失更多工作──

L'exécution durable (leçon 12) rend un agent accidenté réalisable.

> 持久执行 (第 12 课) 使崩 Agent 可恢复──Propose-then-commit

Cette leçon les rejoint: que se passe- t- il lorsqu'une action approuvée s'exécute partiellement, s'écrase et reprend?

> Le cours les relie à: quand la ratification de la partie d'exécution, de l'effondrement, de la reprise se produit-il ?

Les systèmes réels le font différemment:

> Le système de connexion est différent:

> **【中文解读】**Ce chapitre présente le concept et la méthode de réalisation de l'agent d'IA. L'agent est un système autonome à action de la MLL, capable d'observer l'environnement, de penser, de prendre des décisions, d'exécuter des actions et de les faire boucler jusqu'à la fin de l'objectif.

- **LangGraph**Les points de contrôle de chaque transition de l'état graphique vers PostgreSQL.`interrupt()`, qui lui-même persiste.
  Le mot grec traduit par " le mot grec "**LangGraph**Pour chaque tableau, le point de contrôle est transféré à PostgreSQL.`interrupt()`Il est en train de se faire sentir.
- **Cloudflare Durable Objects**maintenir l'état par clé pendant des heures ou des semaines. Co-location du calcul avec le stockage pour l'action approuvée.
  Le mot grec traduit par " le mot grec "**Cloudflare Durable Objects**跨数小时或数周持有每键状态――将计算与已批准的存储同址――
- **Microsoft Agent Framework**exposés `Checkpoint`les primitifs dans l'API de flux de travail; la répétition plus l'idempotence couvre les répétitions.
  Le mot grec traduit par " le mot grec "**Microsoft Agent Framework**Dans le flux de travail API exposé`Checkpoint`Orig语;重放加等覆盖重试──

Dans tous les cas, la combinaison qui fonctionne réellement est: clé d'idempotence + vérification des préconditions + vérification post-action + réinitialisation de la vérification-échec.

> Dans chaque cas, la composition effective est: 等键 + 前置条件检查 + 动作后验证 + 验证失败时回滚──

## Le concept de base.

### Chaque transition persiste. Chaque transition est durable.

Une transition graphique-état est toute étape qui déplace le flux de travail d'un état nommé à un autre. Les implémentations naïves persistent uniquement à des points de mise en œuvre spécifiques; les implémentations de production persistent à chaque transition. Le coût (quelques écritures supplémentaires) est faible par rapport au gain de fiabilité (la répétition se déplace n'importe où, la récupération de location est précise).

> 图状态转换是将工作流从一个命名状态转移到另一个命名状态的任何步骤──简单实现只在特定提交点持久化;生产实现持久化每转换──成本几次额外写)

### Le bail est récupéré.

Lorsqu'un travailleur se trouve en panne, le flux de travail n'est pas perdu; le bail (une affirmation de courte durée selon laquelle ce travailleur exécute cette course) expire simplement. Un autre travailleur prend le dernier point de contrôle et reprend. Le mécanisme de bail est ce qui permet aux systèmes de production de survivre aux déploiements en roulement sans perdre de travail en vol.

> Le travailleur 崩时工作流不丢失; le bail(Ce travailleur est en train d'exécuter ce travail) est simplement une période de transition.

### Idempotence plus conditions préalables

L'idempotence seule ne suffit pas.$100 from A to B when balance > $1000. " Le flux de travail est engagé, s'écrase au milieu de l'exécution et reprend. Si seulement la clé d'idempotence est vérifiée, et l'exécution reprend, le transfert se déroule une fois (correct). Mais considérez que entre l'écrase et le CV, le solde d'A tombe à 500 $ via un flux de travail différent. Le contrôle d'idempotence passe toujours; la condition préalable ne le fait pas. Sans un contrôle de condition préalable, nous expédions un dépôt.

>  等不够──考虑: 工作流被批准"当余额 > $1000 时从 A 转 $100 à B "。 le flux de travail est soumis, exécuté, rétabli. Si seulement le contrôle est exécuté, le transfert est effectué une fois, mais en considération de l'effondrement et de la récupération, le résidu de l'autre flux de travail est réduit à 500 $.

Toute action conséquente nécessite les deux éléments suivants:

> Chaque action sexuelle doit avoir deux effets:

- **Idempotency key**: empêche la double exécution.
  Le mot grec traduit par " le mot grec "**幂等键**: empêcher la double exécution
- **Precondition check**: confirme que l'État est toujours conforme à ce qui a été approuvé.
  Le mot grec traduit par " le mot grec "**前置条件检查**Le statut de confirmation est toujours conforme à la ratification.

### La vérification après l'action

"L'outil retourné 200" n'est pas une vérification.

> "Working Back 200" n'est pas une expérience.

- Mise à jour de la base de données: `UPDATE ... RETURNING *`puis affirmer l'état prévu des correspondances de rangées retournées.
  Le nouveau système de données est en cours de développement.`UPDATE ... RETURNING *`Puis il déclare qu'il revient à l'état prévu.
- Envoi par courrier électronique: vérifiez le dossier envoyé pour l'identifiant du message après sa soumission.
  Nom de fichier: "Comment est-ce que tu as fait ?"
- Écrire le fichier: lire le fichier et le faire hasher.
  Le texte est écrit en français.
- Appel à l' API: suivi `GET`sur la ressource cible.
  Suivant: À l'aide de l'API`GET`Il y a une autre.

Si la vérification échoue, le flux de travail est dans un mauvais état connu.

> Le processus de vérification de défaillance est en mauvais état.

### Les plans de retour .

Chaque action qui en résulte dans la proposition-et-commit (leçon 15) comporte un plan de réaction.

> Propose-et-commit­te (§ 15 课) 中每个后果性动作带回滚计划──:

- **In-band rollback**: inverser directement l'effet secondaire (`DELETE`après `INSERT`- Je suis là .`Send-correction-email`après l' envoi).
  Le mot grec traduit par " le mot grec "**带内回滚**: direct contre-réaction secondaire`INSERT`后 `DELETE`、 envoyer après envoyer更正邮件) ⋅
- **Compensating transaction**: une nouvelle action qui neutralise l'original (moteur SAGA standard).
  Le mot grec traduit par " le mot grec "**补偿事务**Le projet de loi de la Société des Nations unies sur les droits de l'homme (SAGA)
- **Out-of-band rollback**: alert un humain, arrête le flux de travail, laisse le mauvais état pour enquête.
  Le mot grec traduit par " le mot grec "**带外回滚**Les autorités ont décidé de mettre fin à la crise.

Les actions sans réaction nécessitent un HITL plus fort au moment de l'engagement (leçon 15 - défi et réponse).

> Il faut que le projet soit nommé dans le projet de loi.

### Article 14 Loi sur l' IA de l' UE Lire la suite

L'article 14 exige une "surveillance humaine efficace" des systèmes à haut risque.

> Article 14 de la loi sur la protection des êtres humains en matière de protection des êtres humains.

- Les points de contrôle sont vérifiables par un vérificateur.
  En français, le point de contrôle est le point de contrôle.
- Les retours sont répétés (testés de bout en bout au moins une fois).
  Le mot "test" est traduit par "test" (en français: test).
- Le suivi de l'audit survit à un déploiement (le backend du point de contrôle n'est pas éphémère).
  Le projet de loi de la Commission européenne sur les droits de l'homme (CEDEAO) est en cours de révision.
- Les vérifications ratées sont alertées, pas enregistrées en silence.
  Le récit de la guerre de l'Allemagne est un récit de la guerre de l'Allemagne.

Un flux de travail qui s'écrase au milieu de l'engagement, reprend et complète l'effet secondaire sans voie de vérification + retour ne survit pas à l'essai de l'article 14.

> 提交中崩、恢复、无验证+回滚路完成副作用工作流不通过第 14 条测试──

### Le mode de défaillance aiguë: le double exécuteur

L'incident de production le plus fréquent dans cet espace: Action approuvée, démarrage de commande, retour 200, décalage du flux de travail avant de persister dans l'état, reprendre et réexécuter.

> Le plus courant dans ce domaine est le déclenchement d'accidents de production:动作批准、提交开始、返回 200、工作流在持久化状态前崩、恢复并重新执行──

1. Action approuvée, clé d'indemptance k.
   Le mot d'ordre est "réfléchisse".
2. Commit commence, exécute, retourne 200.
   Nom de l'article:
3. Le flux de travail s'effondre avant de persister dans le statut "engagé".
   Le travail est en cours de rédaction.
4. Le flux de travail est repris; voit "approuvé mais non engagé"; est réexécuté.
   Le texte est traduit en français par "Ratification mais non soumis";
5. Les effets secondaires sont deux fois.
   Le deuxième est le deuxième.

Atténuation: persévérer une intention "en vol" avant l'exécution, exécuter avec une clé d'idempotence, puis marquer "committed" seulement après la vérification post-action réussie. Si les tirs d'action et l'écriture de statut échouent, vous savez vérifier et (le cas échéant) ré-écrire. Si l'écriture d'état réussit et l'action échoue, vous vérifiez et tirez exactement une fois via le chemin de récupération.

> 缓解: execution前持久化"in-flight"意图, avec等键执行, seulement dans l'action 后验证成功后标记"已提交"──如动作触发而状态写失败,你知道要验证(如必要) 重触发──如状态写成功而动作失败,你验证并通过恢复路径精确触发一次──

## Utilisez-le avec le cadre de réalisation
```figure
checkpoint-replay
```

## Utilisez-le

`code/main.py`Le conducteur simule quatre scénarios: une course propre, une nouvelle tentative après un accident (captures d'idempotence), un échec de précondition (abortes de flux de travail sans tir), une vérification de l'échec (incendie de roulement).

> `code/main.py`实现带等、前置条件、验证和回滚的检查点工作流──驱动器模拟四场景:干净运行、崩后重试(等捕获)、前置条件失败(工作流停止不触发)、验证失败(回滚触发)。

## Envoyez-le . Produit .

`outputs/skill-rollback-rehearsal.md`conçoit un test de répétition de l'expérience de retour pour un flux de travail proposé et vérifie la persistance du parcours d'audit du point de contrôle.

> `outputs/skill-rollback-rehearsal.md`Pour la proposition de projet de projet de projet de projet de projet de projet de projet de projet de projet de projet de projet de projet de projet de projet de projet de projet de projet de projet de projet de projet de projet de projet de projet de projet de projet de projet de projet de projet de projet de projet de projet de projet de projet de projet de projet de projet de projet de projet de projet de projet de projet de projet de projet de projet de projet de projet de projet de projet de projet de projet de projet de projet de projet de projet de projet de projet de projet de projet de projet de projet de projet de projet de projet de projet de projet de projet de projet de projet de projet de projet de projet de projet de projet de projet de projet de projet de projet de projet de projet de projet de projet de projet de projet de projet de projet de projet de projet de projet de projet de projet de projet de projet de projet de projet de projet de projet de projet de projet de projet de projet de projet de projet de projet de projet de projet de projet de projet de projet de projet de projet de projet de projet de projet de projet de projet de projet de projet de projet de projet de projet de projet de projet de projet de projet de projet de projet de projet de projet de projet de projet de projet de projet de projet de projet de projet de projet de projet de projet de projet de projet de projet de projet de projet de projet de projet de projet de projet de projet de projet de projet de projet de projet de projet de projet de projet de projet de projet de projet de projet de projet de projet de projet de projet de projet de projet de projet de projet de projet de projet de projet de projet de projet de projet de projet de projet de projet de projet de projet de projet de projet de projet de projet de projet de projet de projet de projet de projet de projet de projet de projet de projet de projet de projet de projet de projet de projet de projet de projet de projet de projet de projet de projet de projet de projet de projet de projet de projet de projet de projet de projet de projet de projet de projet de projet de projet de projet de projet de projet de projet de projet de projet de projet de projet de projet de projet de projet de projet de projet de projet de projet de projet de projet de projet de projet de projet de projet de projet de projet de projet de projet de projet de projet de projet de projet de projet de projet de projet de projet de projet de projet de projet de projet de projet de

## Les exercices

1. On court .`code/main.py`Pour le cas d'accident, confirmez les tirs d'action exactement une fois à travers les tentatives de reprise.
   Le mot " l' économie " est traduit par " l' économie ".`code/main.py` vérifier quatre scénarios. Pour le cas de l'effondrement de la procédure de soumission, confirmer l'action dans le cadre de l'essai réel.

2. Modifiez le modèle "marquer comme fait d'abord, puis le faire" afin que le statut écrive des incendies après l'action. Retournez le scénario de crash. Mesurer combien d'actions dupliquées tirent.
   Traduction anglaise: modifier le mode "Présignation completée à nouveau" mode de mise en place de l'état de l'écriture dans l'action

3. Développer un plan de réouverture pour une action de production spécifique (par exemple, "post to a Slack channel"). Classifier comme en bande, compensant ou hors bande. Justifier le choix.
   Pour une production spécifique, il est nécessaire de créer un projet de production spécifique.

4. Prenez un flux de travail que vous connaissez. Identifiez chaque transition d'état. Marquez-le avec une exigence de durabilité (persistent / ne persistent pas). Comptez ceux que vous ne persistez pas actuellement.
   Le nombre de personnes qui travaillent dans un état de travail est de 1,5% à 1,5% en moyenne.

5. Test de retour répété: concevoir un test de bout en bout qui exécute un véritable flux de travail, le casse et confirme les feux de chemin de retour.
   Le projet de réforme de la structure de l'équipe de réforme de l'équipe de réforme de l'équipe de réforme de l'équipe de réforme de l'équipe de réforme de l'équipe de réforme de l'équipe de réforme de réforme de l'équipe de réforme de réforme de l'équipe de réforme de réforme de l'équipe de réforme de réforme de l'équipe de réforme de réforme de l'équipe de réforme de réforme de l'équipe de réforme de réforme de l'équipe de réforme de réforme de l'équipe de réforme de réforme de l'équipe de réforme de réforme de l'équipe de réforme de réforme de l'équipe de réforme de réforme de réforme de l'équipe de réforme de réforme de réforme de réforme de l'équipe de réforme de réforme de réforme de réforme de réforme de réforme de réforme de réforme de réforme de réforme de réforme de réforme de réforme de réforme de réforme de réforme de réforme de réforme de réforme de réforme de réforme de réforme de réforme de réforme de réforme de réforme de réforme de réforme de réforme.

## Les termes clés

| Term | What people say | What it actually means |
|---|---|---|
| 术语 | 通俗说法 | 实际含义 |
| Checkpoint | "Save point" | Every graph-state transition persists to a durable store |
| 检查点 | "保存点" | 每个图状态转换持久化到持久存储 |
| Lease | "Worker claim" | Short-lived claim that a worker is executing a run; expires on crash |
| 租约 | "Worker 声明" | worker 正在执行运行的短暂声明；崩溃时过期 |
| Precondition | "State gate" | Assertion that the state is still consistent with the approved action |
| 前置条件 | "状态门" | 状态仍与批准动作一致的断言 |
| Post-action verify | "Re-read check" | Confirm the side effect actually happened in the target system |
| 动作后验证 | "回读检查" | 确认副作用在目标系统中实际发生 |
| In-band rollback | "Direct undo" | Reverse the side effect with the inverse operation |
| 带内回滚 | "直接撤销" | 用逆操作反转副作用 |
| Compensating transaction | "SAGA undo" | A new action that neutralizes the original |
| 补偿事务 | "SAGA 撤销" | 抵消原始动作的新动作 |
| Mark-as-done-first | "Status write order" | Persist the committed status before returning from commit |
| 先标记完成 | "状态写顺序" | 从提交返回前持久化已提交状态 |
| Article 14 | "EU AI Act human oversight" | Operational: queryable checkpoints, rehearsed rollbacks, auditable trail |
| 第 14 条 | "EU AI 法案人类监督" | 运营：可查询检查点、演练回滚、可审计追踪 |

## Encore une lecture

- [Microsoft Agent Framework — Checkpointing and HITL](https://learn.microsoft.com/en-us/agent-framework/workflows/human-in-the-loop) Primitives de points de contrôle et récupération de location.
  Le mot grec traduit par "rétablissement" est "rétablissement".
- [Cloudflare Agents — Human in the loop](https://developers.cloudflare.com/agents/concepts/human-in-the-loop/) Objets durables en tant que substrat d'état.
  Les objets durables sont classés en tant que base de données de l'état.
- [EU AI Act — Article 14: Human oversight](https://artificialintelligenceact.eu/article/14/) base réglementaire.
  Le mot "région" est traduit par "région".
- [Anthropic — Measuring agent autonomy in practice](https://www.anthropic.com/research/measuring-agent-autonomy) Cadrage fiable des flux de travail à long terme.
  Le cadre de travail de longue durée.
- [Anthropic — Claude Code Agent SDK: agent loop](https://code.claude.com/docs/en/agent-sdk/agent-loop) Forme de flux de travail pour les routines de code Claude.
  Le code de Claude est un code de Claude Claude.
