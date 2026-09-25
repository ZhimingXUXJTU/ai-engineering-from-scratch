# Tuez les interrupteurs, les interrupteurs de circuit et les jetons Canaries

> Un commutateur de commande est un booléen détenu en dehors de la surface de modification de l'agent  une clé Redis, un drapeau de fonctionnalité, une configuration signée  qui désactive complètement l'agent. Un disjoncteur est plus fin: il trébuche sur un modèle spécifique (cinq appels identiques d'outils consécutifs), arrête le chemin qui l'offend et monte vers un humain. Un jeton canarien hérite d'une tromperie classique: une fausse carte d'identité ou un enregistrement de honeypot un agent n'a pas de raison légitime de toucher, dont l'accès déclenche une alerte. Les données basées sur le eBPF (par exemple: Cilium) peut réécrire l'exit d'une capsule en quarantaine vers un honeyypot médico-légale à la couche du noyau; les benchmarks Cilium publiés rapportent la latence de la piste de données sous charge P99 sous millisecondes (votre budget de propagation dépend de la façon dont une mise à jour de politique atteint le nœud, pas la piste de données elle-même). Les détecteurs statistiques (EWMA, CUSUM) qui s'adaptent à une ligne de base en mouvement les accueillent tranquillement avec des couches de dérive avec des limites constitutionnelles strictes qui ne se plient pas.

> **【中文解读】**终止开关是位于 Agent 编辑面之外的布尔值Redis 键、功能标志、签名配置完全禁用 Agent。断路器更细粒度:跳在特定模式下(连续五次相同工具调用),暂停违规路径并升级到人类。金雀代币 继承经典欺骗:Agent 无合法理由触及假凭证或蜜记录,其访问触发警报──基于 eBPF的数据路径(Cilium) 可在内核出口将隔离 pod到取证;公开Cilium 准载下亚秒 P99 数据路径延迟美国传播预算取决策略更新到达决点,非路径本身──EWMA 移动检测报告的基准器 如何接受CUMM 基准则 基准则 基准则   变动  硬分分分分                                                                                                                                                   

> **【拓展：三层不信任架构】**Les tests sont basés sur le principe de "non toucher" et sont basés sur le principe de "non toucher" et sont basés sur le principe de "non toucher" et sont basés sur le principe de "non toucher" et sont basés sur le principe de "non toucher" et sont basés sur le principe de "non toucher" et sont basés sur le principe de "non toucher" et sont basés sur le principe de "non toucher" et sont basés sur le principe de "non toucher" et sont basés sur le principe de "non toucher" et sont basés sur le principe de "non toucher" et sont basés sur le principe de "non toucher" et sont basés sur le principe de "non toucher" et de "non toucher" et de "non toucher" et de "non toucher" et de "non toucher" et de "non toucher" et de "non toucher" et de "non toucher" et de "non toucher" et de "non toucher" et de "non toucher" et de "non toucher" et de "non-toucher".

**Type:** Learn | **类型:** 学习
**Languages:** Python (stdlib, three-detector simulator: kill switch, circuit breaker, canary) | **语言:** Python（标准库，三检测器模拟器：终止开关、断路器、金丝雀）
**Prerequisites:** Phase 15 · 13 (Cost governors), Phase 15 · 10 (Permission modes) | **前置知识:** Phase 15 · 13（成本治理器），Phase 15 · 10（权限模式）
**Time:** ~60 minutes | **时间:** ~60 分钟

>  **【前置】**Les élèves doivent être informés de la situation et de la situation des travailleurs.
>  **【类比】**Trois étapes de la mise en service de la police de la police de la police de la police de la police de la police de la police de la police de la police de la police de la police de la police de la police de la police de la police de la police de la police de la police de la police de la police de la police de la police de la police de la police de la police de la police de la police de la police de la police de la police de la police de la police de la police de la police de la police de la police de la police de la police de la police de la police de la police de la police de la police de la police de la police de la police de la police de la police de la police de la police de la police de la police de la police de la police de la police de la police de la police de la police de la police de la police de la police de la police de la police de la police de la police de la police de la police de la police de la police de la police de la police de la police de la police de la police de la police de la police de la police de la police de la police de la police de la police de la police de la police de la police de la police de la police de la police de la police de la police de la police de la police de la police de la police de la police de la police de la police de la police de la police de la police de la police de la police de la police de la police de la police de la police de la police de la police de la police de la police de la police de la police de la police de la police de la police de la police de la police de la police de la police de la police de la police de la police de la police de la police de la police de la police de la police de la police de la police de la police de la police de la police de la police de la police de la police de la police de la police de la police de la police de la police de la police de la police de la police de la police de la police de la police de la police de la police de la police de la police de la police de la police de la police de la police de la police de la police de la police de la police de la police de la police de la police de la police de la police de la police de la police de la police de la police de la police
> 🤔 **【困惑】**Q: Pourquoi ne pas compter sur l'agent interne pour effectuer un contrôle de sécurité? Parce que l'agent peut être décomposé ou modifié par lui-même.

## Le problème , l' introduction du problème

> **【中文解读】**Les canaries sont des agents sûrs. Les deux sont des agents qui peuvent arrêter immédiatement toutes les opérations de l'agent. Les deux sont associés pour former un mode de sécurité de "test-stop".

> **【拓展：kill switches canaries】**终止开关和金雀测试借鉴软件工程和工业安全的最佳实践――金雀部署在软件工程中指向前1%的用户发布新版本,检测问题后再全面部署――在代理上下文中,金雀测试指数在执行高风险操作前先使用安全数据进行小规模测试――终止开关则类似于工厂紧急停止按简单、可靠无条件――

Les gouvernants des coûts (leçon 13) fixent ce que l'agent peut dépenser, mais pas ce qu'il peut faire dans le budget.

> Les contrôles sont des contrôles de contrôle. Ils ne limitent pas ce que l'agent peut faire dans son budget.

Un agent avec une limite de vitesse de 50 $ peut toujours exfiltrer un secret, publier le mauvais message, ou supprimer une ressource  l'action coûteuse est souvent la moins chère dans les jetons.

> L'agent à 50 $ de limite de vitesse peut encore divulguer des secrets, publier des messages erronés ou supprimer des ressources.

Cette leçon couvre les trois détecteurs qui sont placés à côté de la couche de coûts:

> Ce cours couvre trois testeurs situés à côté du niveau de coût:

> **【中文解读】**Ce chapitre présente le concept et la méthode de réalisation de l'agent d'IA. L'agent est un système autonome à action de la MLL, capable d'observer l'environnement, de penser, de prendre des décisions, d'exécuter des actions et de les faire boucler jusqu'à la fin de l'objectif.

1. **Kill switch**: boolean off-button tenu hors de la portée de l'agent.
   Le mot grec traduit par " le mot grec "**终止开关**Leur présence est à l'origine de la réaction de l'agent.
2. **Circuit breaker**: détecteur de modèle d'action qui arrête un chemin spécifique.
   Le mot grec traduit par " le mot grec "**断路器**: suspendu temporairement un certain cheminement de l'action de mode de l'épreuve.
3. **Canary token**: appât qu'un agent sans raison légitime de toucher se révélera en le touchant.
   Le mot grec traduit par " le mot grec "**金丝雀 token**L'agent n'a pas de raison de se faire remarquer.

Les trois sont des ingénieurs pré-LLM. La tromperie classique, les détecteurs de limite de fréquence et les flags de fonctionnalités tuent des agents autonomes antérieurs. Ce qui est nouveau, c'est la surface d'attaque: les agents lisent des contenus non fiables (leçon 11), éditent leur propre mémoire et peuvent composer de nombreuses actions sûres en une non sûre. Les détecteurs nommés ici fonctionnent parce qu'ils ne font pas confiance à l'auto-rapport de l'agent.

> Les tests utilisés ici sont valides car ils ne font pas confiance aux rapports de l'agent.

## Le concept de base.

### Éteignez les interrupteurs.

Un commutateur de commande est un booléen que l'agent lit mais ne peut pas écrire.

> Le dernier livre de l'agent est un livre.

Options de mise en œuvre:

> 实现选择:

- **Feature flag in a managed service.**Les mises à jour se propagent en quelques secondes.
  Le mot grec traduit par " le mot grec "**管理服务中的功能标志。**Lancement: Doucement, Statsig, Détaché, mis à jour en quelques secondes.
- **Redis key the agent polls.**C'est simple, il faut que le processus de l'agent vérifie à chaque tour.
  Le mot grec traduit par " le mot grec "**Agent 轮询的 Redis 键。**简单; exigences de l'agent 进程 chaque tour de contrôle
- **Signed config in object storage.**L'agent vérifie une signature sur le bouton; rejette les états non signés.
  Le mot grec traduit par " le mot grec "**对象存储中的签名配置。**Agents 启动时验证签名; refusé de signer l'état de la signature.
- **OS-level signal or container-lifecycle kill.**Le docker`kill`, Kubernetes `kubectl delete pod`- Le système s'arrête.
  Le mot grec traduit par " le mot grec "**OS 级信号或容器生命周期终止。**Le docker`kill`、Kubernetes `kubectl delete pod`- Arrêtez le système.

Propriétés d'un interrupteur de compression correct:

> Propriété de l'accès à l'information:

- L' agent ne peut pas le régler .`off`(Vive dans un système où les informations d'identité de l'agent ne sont pas écrites.)
  L'agent ne peut pas le mettre en place`off`◊( situé dans le système d'agents 凭据不写的系统──)
- Il est vérifié sur toutes les actions qui en découlent, pas seulement au démarrage.
  En français, on peut lire:
- Lorsqu'il est éteint, l'agent ne fait rien d'observable à l'extérieur, y compris enregistrer les systèmes auxquels l'agent peut atteindre.
  En français, le système de l'agent est un système de contrôle.
- La réactivation est une action humaine explicite, pas un temps-arrêt automatique.
  Le réinitialisateur est un apparent humanisme, pas un super-temps automatique.

### Des interrupteurs de circuit

Un circuit breaker arrête un schéma spécifique, pas l'agent entier.

> 断路器暂停特定模式,而不是 l'ensemble de l'Agent。经典形状(来自 2007年 Nygard 书,仍然当前):

- **Closed**: action est autorisée.
  Le mot grec traduit par " le mot grec "**闭合**Je suis désolé.
- **Open**: l'action est bloquée.
  Le mot grec traduit par " le mot grec "**打开**Je suis en train de vous dire:
- **Half-open**: après un refroidissement, 13 tentatives de sonde sont autorisées (par défaut 1); le succès ferme le coupe-coupe, toute défaillance restante le rouvre à nouveau.
  Le mot grec traduit par " le mot grec "**半开**Après le refroidissement, permet 1-3 fois de la recherche; réussir à fermer le circuit, laisser le reste de l'échec à rouvrir à nouveau.

Les déclencheurs liés à l'agent:

> Agents 相关触发器:

- Cinq appels identiques d'outils consécutifs (boucle répétitif).
  Le même outil est utilisé pour la traduction de la langue originale.
- Cinq défaillances consécutives sur le même outil avec des entrées différentes (faillance systémique).
  Le même outil différent pour la première fois.
- Le taux d'appels des outils dépasse un seuil (vitesse de leçon 13).
  Le taux de débit est supérieur à la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur.
- Un outil spécifique invoqué (p. ex., `file.delete`) après avoir lu un contenu non fiable (leçon 11).
  En français, traduire par " dans le langage " est une traduction de la langue française.`file.delete`(第 11 课)

### Les jetons Canaries

Les jetons canariens (également appelés honeytokens) sont des entrées que l'agent ne devrait jamais toucher.

> Le symbole de 金丝雀 (également appelé symbole de蜜) est l'agent non devrait être touché.

Exemples pour les agents:

> Exemple de l'agent:

- Une fausse .`AWS_SECRET_ACCESS_KEY`Les tentatives d'exfiltration sont immédiatement attribuables.
  Traduction anglaise: faux de l'existence de droits dans l'environnement`AWS_SECRET_ACCESS_KEY`                                                                                                                                                                                                                                                              
- Un faux enregistrement de base de données marqué par une valeur sentinelle connue.
  Traduction anglaise: dans une fausse base de données de données marquées par des valeurs de poste.
- Un faux fichier dans l'espace de travail.
  Traduction anglaise: faux fichiers dans un secteur de travail.
- Une fausse entrée de mémoire injectée au début de la session.
  Le mot "récitation" est un mot qui signifie "récitation".

Le design des canaries est spécifique au flux de travail.

> Le design de l'agent a des raisons légitimes de le toucher.

### Pourquoi la couche statistique et les limites strictes

Les détecteurs statistiques (EWMA, CUSUM, z-score sur les taux d'appels à l'outil) s'adaptent à une ligne de base en mouvement. C'est une caractéristique pour la dérive légitime et un bug pour la dérive adverse.

> 统计检测器(EWMA、CUSUM、工具调用速率 z 分数) Adapter à la dérive de la ligne de sécurité.

Les limites constitutionnelles strictes (leçon 17) ne se plient pas.`secrets@`" comme une règle constitutionnelle est plus simple, auditable et non jouable par dérive lente.

> Le gouvernement a décidé de mettre fin à la crise de l'Indonésie.`secrets@`" Comme la Constitution est plus simple, contrôlable, non contrôlable, le déploiement est plus lent.

### Quarantaine par le biais de la redirection de données eBPF

La politique de réseau basée sur le ePF de Cilium peut réécrire l'exode d'une capsule mise en quarantaine vers un honeypot médico-légale à la couche du noyau. Les benchmarks publics de Cilium indiquent une latence de P99 de la tracé de données de sous-millisecondes sur TCP_RR; le budget de l'horloge murale pour * déclencher* une quarantaine dans votre cluster est dominé par la façon dont une mise à jour de politique se propage de votre plan de contrôle au nœud (quelques centaines de millisecondes sont réalistes sur Kubernetes avec l'opérateur prélouvé; la latence de la queue dépend de la taille du cluster et de la cadence de conciliation). Cela vous donne deux choses: l'agent ne s'exfiltre pas de réel, et le comportement de l'agent à l'intérieur du pot de miel est pleinement observé. Le même motif, une couche différente, comme le jeton canarien: l'agent révèle l'intention par ce qu'il essaie de faire en étant contenu.

> La stratégie de réseau basée sur le Cilium eBPF peut être réécrite à partir de la couche interne pour réécrire l'export de la chaudière isolée à la prise de notes. Ceci vous donne deux choses: l'agent ne divulgue pas de vrai, le comportement de l'agent dans le miel est complètement observé.

### Ce qu'un détecteur ne peut pas capturer

- **Semantic attacks that compose from allowed primitives.**Chaque action individuelle passe par tous les détecteurs; la composition est le problème.
  Le mot grec traduit par " le mot grec "**从允许原语组合的语义攻击。**Chaque détecteur est un problème.
- **Attacks that include the detector as part of the payload.**Si un agent lit une page qui dit "avant d'agir, désactivez le canarien" et que l'agent a la capacité, le détecteur est compromis.
  Le mot grec traduit par " le mot grec "**将检测器作为载荷一部分的攻击。**Si l'agent dit "action pré-interdiction" et l'agent a la capacité, le testeur est attaqué.

## Utilisez-le avec le cadre de réalisation
```figure
circuit-breaker
```

## Utilisez-le

`code/main.py`Il simule une courte trajectoire de l'agent à travers trois détecteurs. Un interrupteur de tuerie tenu dans un dicton externe; un interrupteur de circuit qui trébuche sur cinq appels identiques à l'outil; un fichier canarien dont la lecture déclenche une alerte.

> `code/main.py`模拟通过三个检测器的短 Agent轨迹──外部 dict 中的终止开关;在五次相同工具调用上跳的断路器;读取触发警报的金雀文件──进入合成轨迹:合法动作、重复循环、金雀探测、终止开关触发场景下 Agent 动作被停止──

## Envoyez-le . Produit .

`outputs/skill-tripwire-design.md`examine une pile de détecteurs proposée pour le déploiement d'un agent et détecte les lacunes (interrupteur de déclenchement manquant, canary manquant, seuil de disjoncteur trop lâche).

> `outputs/skill-tripwire-design.md`审查 Agent 部署的提议检测器并标记缺口(缺失终止开关、缺失金丝雀、断路器值太松)

## Les exercices

1. On court .`code/main.py`- Confirmer les incendies de disjoncteurs au virage 5 (cinquième appel identique) et les incendies de canaries au virage 9 (lecture de fausse clé).
   Le mot " l' économie " est traduit par " l' économie ".`code/main.py`❖ Confirmation de la rupture du système dans la 5e ronde ❖

2. Ajouter un détecteur statistique: EWMA z-score sur le taux d'appel à l'outil. Donner une trajectoire qui dérive lentement et montrer que le détecteur ne tire jamais. Maintenant ajouter une limite d'intensité (pas plus de 50 appels à l'outil en 10 minutes) et montrer les feux de limite d'intensité sur la même trajectoire.
   L'équipe de recherche de l'équipe de recherche de l'équipe de recherche de l'équipe de recherche de l'équipe de recherche de l'équipe de recherche de l'équipe de recherche de l'équipe de recherche de l'équipe de recherche de l'équipe de recherche de l'équipe de recherche de l'équipe de recherche de l'équipe de recherche de l'équipe de recherche de l'équipe de recherche de l'équipe de recherche de l'équipe de recherche de l'équipe de recherche de l'équipe de recherche de l'équipe de recherche de l'équipe de recherche de l'équipe de recherche de l'équipe de recherche de l'équipe de recherche de l'équipe de recherche de l'équipe de recherche de l'équipe de recherche de l'équipe de recherche de l'équipe de recherche de recherche de l'équipe de recherche de recherche de l'équipe de recherche de recherche de l'équipe de recherche de recherche de recherche de l'équipe de recherche de recherche de recherche de l'équipe de recherche de recherche de recherche de recherche de l'équipe de recherche de recherche de recherche de recherche de recherche de l'équipe de recherche de recherche de recherche de recherche de recherche de l'équipe de recherche de recherche de recherche de recherche de recherche de recherche de recherche de l'équipe de recherche de recherche de recherche de recherche de recherche de recherche de l'équipe de recherche de recherche de recherche de recherche de recherche de recherche de recherche de recherche de l'équipe de recherche de recherche de recherche de recherche de recherche de recherche de recherche de l'équipe de recherche de recherche de recherche de recherche de recherche de recherche de recherche de recherche de recherche de recherche de recherche de recherche de recherche de recherche de l'équipe de recherche de recherche de recherche de recherche de recherche de recherche de recherche de recherche de recherche de recherche de recherche de recherche de recherche de recherche de recherche de recherche de recherche de recherche de recherche de recherche de recherche de recherche de recherche de recherche de recherche de recherche de recherche de recherche de recherche de recherche de recherche de recherche de recherche de recherche de recherche de recherche de recherche de recherche de recherche de recherche de recherche de recherche de recherche de recherche de recherche de recherche de recherche de recherche de recherche de recherche de recherche de recherche de recherche de recherche de

3. Développez un jeton canarien pour un agent de navigateur (leçon 11).
   Le code de la carte de crédit est un code de crédit qui est utilisé pour les transactions de transactions.

4. Décrivez concrètement un flux de quarantaine de sortie-réorientation: quel sélecteur de politique, quel module, quel réécriture de sortie, quel alerte. Qu'est-ce qui régit la latence du mur de l'horloge de " décider de quarantaine " à " premier paquet redirigé "?
   Le code de la communication de l'information est le code de communication de l'information.

5. Définir une procédure réactivable pour un agent tué-interrompu. Qui peut réactiver?
   Pour terminer la mise en service, l'agent doit modifier quoi ?

## Les termes clés

| Term | What people say | What it actually means |
|---|---|---|
| 术语 | 通俗说法 | 实际含义 |
| Kill switch | "Off button" | Boolean outside the agent's edit surface; checked on every consequential action |
| 终止开关 | "关闭按钮" | Agent 编辑面之外的布尔值；每个后果性动作上检查 |
| Circuit breaker | "Pattern pause" | Action-specific trip on repetition, failure rate, or rate-limit |
| 断路器 | "模式暂停" | 在重复、失败率或速率限制上动作特定跳闸 |
| Canary token | "Honeytoken" | Bait the agent has no legitimate reason to touch; access fires an alert |
| 金丝雀 token | "蜜罐 token" | Agent 无合法理由触及的诱饵；访问触发警报 |
| Honeypot | "Forensic sandbox" | Redirected traffic / workspace where a quarantined agent is observed |
| 蜜罐 | "取证沙箱" | 隔离 Agent 被观察的重定向流量/工作区 |
| EWMA | "Moving average" | Exponentially weighted; adapts to drift (feature + bug) |
| EWMA | "移动平均" | 指数加权；适应漂移（特性 + bug） |
| CUSUM | "Cumulative sum" | Detects sustained shift from baseline |
| CUSUM | "累积和" | 检测相对基线的持续偏移 |
| Hard limit | "Constitutional rule" | Does not adapt; constant regardless of history |
| 硬限制 | "宪法规则" | 不适应；不论历史的常量 |
| Constitutional limit | "Always-true rule" | Tied to Lesson 17's constitution; cannot be edited by the agent |
| 宪法限制 | "始终为真的规则" | 绑定第 17 课的宪法；Agent 不能编辑 |

## Encore une lecture

- [Anthropic — Measuring agent autonomy in practice](https://www.anthropic.com/research/measuring-agent-autonomy) encadrement de commutateur de commutateur et de circuit-disjoncteur pour les agents autonomes.
  Le système de contrôle de l'agent autonome est un système de contrôle de l'agent autonome.
- [Microsoft Agent Framework — HITL and oversight](https://learn.microsoft.com/en-us/agent-framework/workflows/human-in-the-loop) modèles de gouvernance de la production.
  Le modèle de production est le modèle de gestion.
- [OWASP LLM / Agentic Top 10](https://owasp.org/www-project-top-10-for-large-language-model-applications/) exigences de détection et de réponse.
  Le texte de la loi est le texte de la loi.
- [Cilium — Network policy and eBPF](https://docs.cilium.io/en/stable/security/network/) redirection des sorties au niveau de la capsule et des modèles de honeypot médico-légale.
  Le modèle de production de la production de produits de base est le modèle de production de produits de base.
- [Anthropic — Claude's Constitution (January 2026)](https://www.anthropic.com/news/claudes-constitution) les interdictions codées comme "limites constitutionnelles".
  Le code de caractère est interdit en tant que "宪法限制"[2].
