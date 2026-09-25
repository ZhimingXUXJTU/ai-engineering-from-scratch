# Partage de mémoire et de planches noires.

> Deux approches coexistent dans les systèmes multi-agents de 2026: le **message pool**(tous voient les messages de tous, comme dans AutoGen GroupChat ou MetaGPT) et le **blackboard with subscription**Les deux sont la seule partie étatique d'un système multi-agent  ce qui signifie que les deux sont là où vivent les bugs intéressants.**memory poisoning**Un agent hallucine un " fait ", d'autres agents le traitent comme vérifié, et la précision se détériore progressivement d'une manière qui est beaucoup plus difficile à déboguer qu'un accident immédiat.

> **【中文解读】**Ce chapitre présente la base de connaissances et le mécanisme de coordination dans le système de partage de mémoires et de systèmes de cartes à puces.

> **【拓展：shared memory blackboard→具体应用】**Le modèle de blackboard est un mécanisme de coordination classique de plusieurs agents du système. Tous les agents ont écrit une base de connaissances commune. Le modèle de blackboard est issu du système de reconnaissance des sons de l'écoute-II des années 1980.


**Type:** Learn + Build | **类型:** 学习 + 构建
**Languages:** Python (stdlib, `threading`) | **语言:** Python (标准库, `threading`)
**Prerequisites:** Phase 16 · 04 (Primitive Model), Phase 16 · 09 (Parallel Swarm Networks) | **前置知识:** Phase 16 · 04 (原语模型), Phase 16 · 09 (并行群体网络)
**Time:** ~75 minutes | **时间:** ~75 分钟

>  **【前置】**Les données de base de l'équipe de formation sont les données de base de l'équipe de formation.
>  **【类比】**Communiqué de presse: Le groupe AutoGen GroupChat (en anglais) est un groupe de télécommunications qui a été créé par l'Agence AutoGen GroupChat (en anglais) pour la communication de données.

## ♪ Problème ♪ Introduction du problème ♪

Les systèmes multi-agents ont besoin d'un endroit pour les agents de partager des faits. Une option littérale est "passer tout dans les messages"  mais qui réinvente l'état partagé avec une copie supplémentaire. Un autre est "donner à tout le monde un journal global"  mais les journaux mondiaux se développent illimités et empoisonnent facilement. Un troisième est "projeter une vue par agent"  évolutif mais schéma-heavy.

> Un type de système est "transporter tout dans le message" mais c'est comme réinventer avec une copie supplémentaire de l'état de partage. Un autre est "donner à chaque individu un journal global" mais le journal global est de croissance illimitée et facile à contaminer.

Les trois options suivent un compromis classique des systèmes distribués: bon marché mais fragile (messages), simple mais non évolutif (log global), évolutif mais rigide (projections par agent). Aucune option n'est dominante.

> Les résultats de la recherche ont été obtenus en 2006 et ont été obtenus en 2006 et ont été obtenus en 2006 et 2007.

Lorsque l'un des agents hallucine et écrit l'hallucination dans un état partagé, chaque agent en aval qui lit cet état adopte l'hallucination comme un fait.

> Lorsque l'un d'eux écrit l'illusion dans un état commun, chaque passage de cet état l'accepte comme un fait. Lorsque l'homme remarque que la chaîne de raisonnement a déjà cinq étapes, la raison fondamentale est la troisième.

Un accident vous donne une trace de l'accident. Un empoisonnement de mémoire vous donne un rapport fausse.

> La première est détectable en quelques secondes, la seconde peut prendre plusieurs jours pour retrouver le récit original.

Il s'agit de l'intoxication de la mémoire. C'est la deuxième famille de défaillances la plus documentée dans la taxonomie MAST (Cemri et coll., arXiv:2503.13657) et elle est structurelle: toute conception de mémoire partagée sans provenance et un vérificateur non écrit l'exposera finalement.

> Ceci est la contamination du stockage. Il s'agit du deuxième plus grand enregistrement de la gestion du stockage de stockage de stockage de stockage de stockage de stockage de stockage de stockage de stockage de stockage de stockage de stockage de stockage de stockage de stockage de stockage de stockage de stockage de stockage de stockage de stockage de stockage de stockage de stockage de stockage de stockage de stockage de stockage de stockage de stockage de stockage de stockage de stockage de stockage de stockage de stockage de stockage de stockage de stockage de stockage de stockage de stockage de stockage de stockage de stockage de stockage de stockage de stockage de stockage de stockage de stockage de stockage de stockage de stockage de stockage de stockage de stockage de stockage de stockage de stockage de stockage de stockage de stockage de stockage de stockage de stockage de stockage de stockage de stockage de stockage de stockage de stockage de stockage de stockage de stockage de stockage de stockage de stockage de stockage de stockage de stockage de stockage de stockage de stockage de stockage de stockage de stockage de stockage de stockage de stockage de stockage de stockage de stockage de stockage de stockage de stockage de stockage de stockage de stockage de stockage de stockage de stockage de stockage de stockage de stockage de stockage de stockage de stockage de stockage de stockage de stockage de stockage de stockage de stockage de stockage de stockage de stockage de stockage de stockage de stockage de stockage de stockage de stockage de stockage de stockage de stockage de stockage de stockage de stockage de stockage de stockage de stockage de stockage de stockage de stockage de stockage de stockage de stockage de stockage de stockage de stockage de stockage de stockage de stockage de stockage de stockage de stockage de stockage de stockage de stockage de stockage de stockage de stockage de stockage de stockage de stockage de stockage de stockage de stockage de stockage de stockage de stockage de stock

## Concept Le concept central

### Les deux principales topologies

**Full message pool.**Chaque agent lit chaque message. AutoGen GroupChat et MetaGPT utilisent ceci. Simple, transparent, inspectable, mais ne dépasse pas ~ 10 agents parce que le contexte de chaque agent se remplit avec le travail des autres agents.

> **完整消息池。**Chaque agent 读取每条消息──AutoGen GroupChat 和 MetaGPT Utilisez cette méthode──简单,透明,可检查,但不能扩展到约10 agents以上,因为每个代理的上下文会填满其他代理的工作──

**Blackboard with subscription.**Les agents déclarent leur intérêt pour les sujets; les routes du substrat ne fournissent que des messages pertinents. CA-MCP (arXiv:2601.11595) et le cadre décentralisé de la Matrice (arXiv:2511.21686) utilisent cela.

> **带订阅的黑板。**L'agent  déclaration d'intérêt pour le sujet; bas niveau seulement par le biais de messages pertinents. CA-MCP(arXiv:2601.11595) et Matrix 去中心化框架(arXiv:2511.21686) utilise ce mode.

### Quand chacun gagne

- **Full pool**Les arguments sur la question de savoir qui a dit ce qui est trivial quand tout le monde voit tout.
  Le mot grec traduit par " le mot grec "**完整池**Quand tout le monde voit tout, le raisonnement de qui dit ce qui est simple.
- **Blackboard**Les résultats obtenus par les agents sont nombreux, homogènes dans le rôle mais nombreux dans l'exemple (swarms), et la conversation est longue.
  Le mot grec traduit par " le mot grec "**黑板**Dans le cadre de la mise en œuvre de la politique de sécurité, les entreprises doivent être soumises à des mesures de protection des données et des mesures de protection des données.

Les systèmes de production se mélangent souvent: une petite piscine complète en haut (couche de planification), des planches noires en bas (couche de travailleurs).

> Système de production est généralement utilisé en combinaison: top part a un petit groupe complet, le plan est basé sur un planche noire.

Ce hybride est ce que fait le système de recherche d'Anthropic: un superviseur (un pool complet entre quelques agents principaux) délègue aux subagents (chacun son propre contexte de portée, isolé des frères et sœurs).

> Cette combinaison est réalisée par le système de recherche anthropologique: superviseurs (en anglais seulement) et agents (en anglais seulement) et agents (en anglais seulement).

### Envenenement de la mémoire, dans un scénario

Trois agents travaillent sur une tâche de recherche, l'agent A est un agent de récupération, l'agent B est un résumé, l'agent C est un analyste.

> Trois agents 处理一个研究任务──Agent A est un agent de recherche──Agent B est un extracteur──Agent C est un analyste──

1. Un a récupéré une page et a écrit un message à l'état partagé: "L'étude rapporte une amélioration de la précision de 42%".
   Une étude a révélé une augmentation de 42% du taux d'exactitude.
2. La page qu'on a récupérée disait "4,2% d'amélioration". Un halluciné décimal.
   La page de l'accueil est en fait "4,2% 提升──" Une illusion d'un petit nombre de points──.
3. B, en lisant l'état partagé, écrit: "Un grand gain de précision de 42% a été rapporté (source: A). "
   Le taux de participation des entreprises dans le secteur de la construction a augmenté de 42% en moyenne.
4. C, en lisant l'état partagé, écrit: " Recommander l'adoption  42% de levage est transformateur. "
   Le taux de participation est de 42% et la croissance est de 42% et la croissance est de 45%.
5. Le rapport final cite un nombre de 42% qui n'a jamais existé.
   Le rapport final cite un nombre de 42% qui n'a jamais existé.

Aucun agent n'a été blessé, aucun test n'a échoué, le système a fonctionné, l'hallucination est passée du contexte d'un agent à celui de chaque agent en aval via l'état partagé.

> 没有 Agent 崩──没有测试失败──系统"工作"了──幻觉通过共享状态从一个代理的上下文进入了每个下游代理的推理──

C'est pourquoi l'intoxication de la mémoire est insidieuse: il n'y a pas de crash, pas d'erreur, pas d'avertissement. Le système produit un rapport sans doute erroné.

> C'est pourquoi le risque de contamination de l'inventaire: pas de dégradation, pas d'erreur, pas d'avertissement. Le système génère des erreurs de confiance. Le seul moyen de le vérifier est de rediriger chaque fait de la source originale.

### Pourquoi est-ce structurel

Sans état partagé, l'hallucination de l'agent A reste dans le contexte de l'agent A. Les agents en aval récupèrent ou dérivent et peuvent attraper l'erreur. Avec l'état partagé naïf, le contexte de l'agent A devient le contexte de tous, et l'hallucination est blanchie en fait.

> 没有共享状态,Agent A's illusion se trouve dans la suite de A's下文中. 下游 Agent 会重新获取或重新推导并可能捕获错误.

Le problème n'est pas l'état partagé en soi  c'est l'état partagé **without provenance and without an independent verifier**Trois mesures d'atténuation s' y rapportent:

> 问题不是共享状态本身而是**没有来源追溯和没有独立验证器**Les trois mesures de réduction permettent de résoudre ce problème:

Chaque atténuation cible un mode d'échec différent. La provenance vous permet de repérer les erreurs. La version conserve la piste d'audit. Le vérificateur non écrit fournit un contrôle indépendant. Ensemble, ils forment une défense profonde contre l'empoisonnement.

> Chaque type de mesure de réduction de la pollution est une mesure de réduction de la pollution, qui peut être utilisée pour réduire les risques de pollution.

1. **Attribute provenance on every write.**Chaque entrée dans les dossiers d'État partagés qui l'a écrite, quand, sous quel prompt, et (le cas échéant) quelle source l'agent a cité.
   Le mot grec traduit par " le mot grec "**每次写入时归属来源。**Chaque article dans l'état de partage est enregistré par qui a écrit 、何時、在什么提示下、以及((si applicable) L'agent 引用什么来源──下游 L'agent 根据来源以怀疑态度阅读──
2. **Version writes; treat them as append-only.**Une correction est une nouvelle entrée qui remplace l'ancienne, pas une mise à jour en place.
   Le mot grec traduit par " le mot grec "**版本化写入；视为仅追加。**修正是一个取代旧条目的新条条条,不是原地更新──审计跟踪被保留──
3. **Keep at least one agent that cannot write to shared state.**Un agent de vérification à lecture seule prélève des échantillons, récupère les sources et détecte les incohérences.
   Le mot grec traduit par " le mot grec "**保留至少一个不能写入共享状态的 Agent。**Il ne peut pas être contaminé par la pile.

### Précedent de plaque noire (Hayes-Roth, 1985)

Le modèle de tableau noir précède les agents de LLM de quatre décennies. Hayes-Roth (1985, "A Blackboard Architecture for Control") a décrit des sources de connaissances spécialisées qui observent une planche noire mondiale, contribuent à des solutions partielles et déclenchent d'autres sources. Le tableau noir 2026 (CA-MCP, Matrix) est le même modèle avec les agents LLM comme les sources de connaissances et les taches JSON comme solutions partielles. L'ancienne littérature a documenté des solutions pour écrire la controverse, le contrôle opportuniste et la cohérence que les systèmes modernes redécouvrent.

> Le modèle de Blackboard comparé à LLM Agent il y a quatre décennies. Hayes-Roth (en 1985) décrit la solution de Blackboard et de la contribution de la partie à observer à l'échelle mondiale. Le modèle de Blackboard et de la MCP est identique à celui de l'agent LLM.

La leçon de Hearsay-II (le tableau de bord de la reconnaissance vocale des années 1970): le contrôle opportuniste  permettant à toute Source de connaissances de déclencher une action lorsque sa condition de déclenchement correspond  produit une résolution de problèmes émergente.

> Le système de gestion des données est un système de gestion de données qui permet de contrôler les informations et de les mettre en œuvre.

### Projection par rapport à vue complète

Un tableau noir pur donne à chaque abonné la même projection (à l'échelle du sujet).**per-agent projection**Les réducteurs d'état de LangGraph sont la mise en œuvre canonique 2026  la fonction de réduction plie l'état global en une tranche spécifique au rôle.

> Le tableau noir donne à chaque abonné la même projection.**每个 Agent 投影**: chaque agent obtient un statut de jeu en fonction de son rôle. L'état du jeu est un élément typique de la réalisation de la fonction de jeu en 2026 qui va se plier dans un morceau de jeu spécifique.

La projection par agent s'élargit mais a besoin d'un schéma.

> Chaque agent est plus efficace, mais il faut un modèle.

### Modèles de contenu écrit

La rédaction simultanément de plusieurs agents est un problème de simultanés, pas seulement un problème de LLM.

> Plusieurs agents sont inscrits en même temps est un problème, pas seulement LLM  problèmes.

- **Sequential writer (single producer).**Toutes les écritures passent par un agent de coordination qui sérialise.
  Le mot grec traduit par " le mot grec "**顺序写入者（单一生产者）。**Toutes les écritures sont réalisées par un agent coordonné.
- **Optimistic concurrency with versioning.**Chaque entrée a une version; les écrivains échouent à la version de déséquilibre et à la réessayer.
  Le mot grec traduit par " le mot grec "**带版本控制的乐观并发。**Chaque article a une version; l'auteur a échoué et réessaye une version incohérente.
- **Topic partitioning.**Les différents agents possèdent des sujets différents, pas de différends entre sujets, il faut des limites de partition.
  Le mot grec traduit par " le mot grec "**主题分区。**Il n'y a pas de conflit entre les différents thèmes.

La plupart des frameworks 2026 sont par défaut écrits par écrit parce que les appels LLM sont assez lents pour que la dispute soit rare et que le goulot d'étranglement ne fasse pas de mal.

> La majorité des élèves de 2026 utilisent le cadre de la formation, parce que le programme de formation professionnelle est assez lent, les conflits sont très rares, les problèmes ne sont pas affectés.

Lorsque vous faites une contestation (envahisseur de haute puissance, agents de recherche parallèles écrivant des résultats), la partition des sujets est généralement la solution la moins chère.

> Lorsque vous rencontrez réellement un conflit, les zones de thèmes sont généralement les plus bon marché.

### Le vérificateur non écrit

L'atténuation la plus efficace est le vérificateur à lecture seule.

> La plus importante mesure de réduction est la mise en œuvre des règles suivantes:

- Le vérificateur partage l'état avec l'équipe (lire le tableau noir ou la balance).
  Le groupe de travail est un groupe de travail.
- Le vérificateur n'a pas de manche d'écriture pour partager l'état  uniquement sur un canal de vérification séparé.
  En français, le testateur n'a pas d'écriture commune à l'état de l'établissement.
- Le vérificateur récupère indépendamment les sources citées dans les écrits.
  Le texte de la loi de l'État de Hongrie est traduit en français par " la loi de Hongrie ".
- Les résultats du vérificateur sont envoyés à un humain ou à un agent de décision séparé, jamais remis dans la piscine.
  Traduction anglaise: l'épreuveur lui-même est un agent de décision, jamais retourné dans la poche.

Sans cette séparation, les sorties du vérificateur deviennent de nouvelles entrées dans la piscine, ce qui signifie qu'une piscine empoisonnée empoisonne le vérificateur, ce qui empoisonne ses vérifications.

> Sans cette séparation, les sorties du vérificateur deviennent les nouvelles entrées de la piscine, ce qui signifie que la piscine contaminée a contaminé le vérificateur, et ainsi contaminé son vérification.

Le principe de l'audit est le suivant: le vérificateur doit être lu uniquement par rapport au système audité.

> C'est un principe indéfectible de vérificateur: l'auditeur doit lire uniquement le système de vérification.

## Construisez-le et mettez-le en œuvre.
```figure
swarm-blackboard
```

## Faites-le

`code/main.py`Il implique les deux topologies dans Stdlib Python plus une attaque d'empoisonnement de jouet et les trois atténuations.

> `code/main.py`Avec Python, deux types de déploiements ont été réalisés, ainsi qu'une attaque contre la pollution des jouets et trois mesures de réduction.

- `MessagePool` Enregistrement de l'appendice sans fil avec lecture complète.
  Le mot grec traduit par " le mot grec "`MessagePool` 线程安全的仅额日志,支持完整读取──
- `Blackboard` pub/sub à clé de thème avec abonnements par agent.
  Le mot grec traduit par " le mot grec "`Blackboard`                                                                                                                                                                                                                                                              
- `ProvenanceEntry` tous les enregistrements d'écriture (écrivain, timestamp, prompt_hash, source_uri).
  Le mot grec traduit par " le mot grec "`ProvenanceEntry` Chaque fois que vous écrivez, vous écrivez, vous faites des recherches.
- `PoisoningScenario` effectue une tâche de recherche à trois agents où l'agent A hallucine un décimal.
  Le mot grec traduit par " le mot grec "`PoisoningScenario` 运行三 Agent 研究任务, dont l'agent A 幻觉一个小数点――印印最终报告――
- `Verifier` un agent à lecture seule qui récupère les sources et détecte les incohérences.
  Le mot grec traduit par " le mot grec "`Verifier` Un agent de recouvrement et de marquage non conformes  fonctionne dans le même scénario en présence d'un vérificateur

Résultats attendus:
- Retour 1 (pas de vérificateur): les 42% hallucinés se propagent au rapport final.
  Le nombre de manifestations de l'hypothèse est de 42%.
- Exécution 2 (avec vérificateur): le vérificateur détecte l'incohérence, le pool est marqué "déglabré", le rapport final comprend une rétraction.
  Le rapport final comprend le retrait.

## Utilisez-le avec le cadre de réalisation

`outputs/skill-memory-auditor.md`est une compétence qui vérifie la conception de la mémoire partagée de tout système multi-agent pour la provenance, la versionisation et la séparation des vérificateurs.

> `outputs/skill-memory-auditor.md`C'est une compétence, auditeur de toute structure de système de gestion de l'agent, de la gestion de la version et de la vérification de l'identité.

## Envoyez-le . Produit .

Pour toute conception de mémoire partagée:

>  Pour tout design de partage:

- Enregistrer la provenance de chaque écriture: `(writer, timestamp, prompt_hash, tool_calls_cited, source_uri)`- Je suis désolé .
  Traduction anglaise: chaque fois que vous écrivez, vous êtes en train de lire:`(写入者, 时间戳, prompt_hash, 引用的工具调用, source_uri)`Il y a une autre.
- Les corrections sont de nouvelles entrées qui font référence à la liste de remplacement.
  Le texte est remplacé par le texte suivant:
- Déployer au moins un agent de vérification à lecture seule avec accès source indépendant.
  En français, le nom de l'agent de l'équipe de défense est traduit en français par " agent de défense ".
- Export du vérificateur de route vers un canal séparé, et non vers le pool partagé.
  Le testateur sort par un chemin unique, plutôt que par un chemin commun.
- L'enregistrement du rapport des écritures qui sont des supersessions  un rapport croissant est une preuve précoce des modèles d'hallucination.
  Traduction anglaise: le taux de couverture des enregistrements est une preuve précoce du mode illusoire.

## Les exercices

1. On court .`code/main.py`Confirmer que la première fois propage l'hallucination et la seconde la prend.
   Le mot " l' économie " est traduit par " l' économie ".`code/main.py`❖ Confirmer le lancement 1 ❖ diffuser le phénomène et le lancement 2 ❖ le capturer
2. Ajouter une deuxième hallucination: l'agent B invente une taille de jeu de données. Le vérificateur doit capturer les deux sans être à la main pour l'un ou l'autre.
   En français, le test doit être effectué sans avoir à s'attaquer à un seul ou plusieurs éléments.
3. Transférer la totalité de la piscine à un tableau avec des partitions de thème (`prices`- Je suis là .`summaries`- Je suis là .`analyses`Quels scénarios d'empoisonnement rendent la partition des thèmes plus difficile à réaliser, et quels ne l'aideront pas?
   Le tableau de bord est remplacé par le tableau de bord.`prices`- Je suis là.`summaries`- Je suis là.`analyses`• ■ Les zones de thème qui rendent les situations de toxicomanie plus difficiles à mettre en œuvre, celles qui ne les aident pas ?
4. Lisez Hayes-Roth (1985, "A Blackboard Architecture for Control"). Identifiez deux modèles de contrôle du document qui ne sont pas discutés dans cette leçon et dont les systèmes 2026 pourraient bénéficier.
   Le projet de loi de 2026 sur la gestion des systèmes de gestion de l'information et de l'information (en anglais: ISO/IEC) est un projet de loi de 2026 sur l'information et la communication.
5. Lisez CA-MCP (arXiv:2601.11595). Mettez son magasin de contexte partagé dans la classe MessagePool ou Blackboard en `code/main.py`Quels primitifs CA-MCP ajoute-t-il au dessus ?
   Le projet de loi de la République de Chine sur le stockage de données (CA-MCP) est en cours de mise en œuvre.`code/main.py`Quels sont les langages originaux ajoutés à la classe CA-MCP ?

## Les termes clés

| Term | What people say | What it actually means |
|------|----------------|------------------------|
| Message pool / 消息池 | "Shared chat history" / "共享聊天历史" | Append-only log that every agent reads. Full transparency, poor scaling. / 每个 Agent 读取的仅追加日志。完全透明，扩展性差。 |
| Blackboard / 黑板 | "Shared workspace" / "共享工作区" | Topic-keyed pub/sub. Agents subscribe to relevant topics. Scales farther. / 基于主题的发布/订阅。Agent 订阅相关主题。扩展性更好。 |
| Provenance / 来源追溯 | "Who wrote what" / "谁写了什么" | Metadata on each write: writer, timestamp, prompt, sources. / 每次写入的元数据：写入者、时间戳、提示、来源。 |
| Memory poisoning / 内存污染 | "Hallucinations spreading" / "幻觉传播" | One agent's error enters shared state, downstream agents adopt it as fact. / 一个 Agent 的错误进入共享状态，下游 Agent 将其作为事实采纳。 |
| Append-only / 仅追加 | "No in-place updates" / "无原地更新" | Corrections are new entries that supersede. Preserves audit trail. / 修正项是取代旧条目的新条目。保留审计跟踪。 |
| Unwritable verifier / 不可写验证者 | "Independent auditor" / "独立审计者" | Read-only agent that re-fetches sources and flags inconsistencies. / 重新获取来源并标记不一致的只读 Agent。 |
| Projection / 投影 | "Scoped view" / "范围视图" | Per-agent view computed from global state. LangGraph reducers are the canonical case. / 从全局状态计算的每个 Agent 视图。LangGraph 归约器是典型实现。 |
| Knowledge Source / 知识源 | "Specialist agent" / "专家 Agent" | Hayes-Roth's 1985 term for a blackboard participant. / Hayes-Roth 1985 年对黑板参与者的称呼。 |

## Encore une lecture

- [Cemri et al. — Why Do Multi-Agent LLM Systems Fail?](https://arxiv.org/abs/2503.13657) Taxonomie MAST; l'empoisonnement par la mémoire est une sous-famille de défaillances de coordination
  Pourquoi plusieurs agents LLM 系统会失败?  MAST 分类法;内存污染是协调失败子家族
- [CA-MCP — Context-Aware Multi-Server MCP](https://arxiv.org/abs/2601.11595) Stockage de contexte partagé pour les serveurs MCP coordonnés
  Le code de gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la
- [Matrix — decentralized multi-agent framework](https://arxiv.org/abs/2511.21686) tableau noir basé sur la file d'attente de messages sans orchestrateur central
  Le code de la carte est un code de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de
- [LangGraph state and reducers](https://docs.langchain.com/oss/python/langgraph/workflows-agents) le modèle de projection par agent dans la production
  L' émetteur de l' émetteur de l' émetteur de l' émetteur de l' émetteur de l' émetteur de l' émetteur de l' émetteur de l' émetteur de l' émetteur de l' émetteur de l' émetteur de l' émetteur de l' émetteur de l' émetteur de l' émetteur de l' émetteur de l' émetteur de l' émetteur de l' émetteur de l' émetteur de l' émetteur de l' émetteur de l' émetteur de l' émetteur de l' émetteur de l émetteur de l' émetteur de l émetteur de l émetteur de l émetteur de l émetteur de l émetteur de l émetteur de l émetteur de l émetteur de l émetteur de l émetteur de l émetteur de l émetteur de l émetteur de l émetteur de l émetteur de l émetteur de l émetteur de l émetteur de l émetteur de l émetteur de l émetteur de l émetteur de l émetteur de l émetteur de l émetteur de l émetteur de l émetteur de l émetteur de l émetteur de l émetteur de l émetteur de l émetteur de l émetteur de émetteur
- [Anthropic — How we built our multi-agent research system](https://www.anthropic.com/engineering/multi-agent-research-system) Notes de provenance et de vérification d'un déploiement de production
  Traduction anglaise:Anthropic  Comment construire plusieurs agents  Système de recherche  provenant de la production des déploiements 
