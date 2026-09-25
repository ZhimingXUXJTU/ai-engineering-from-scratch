# Les modes d'échec  MAST, groupe de pensée, monoculture, erreurs en cascade 失败模式 群体思维 MAST

> La taxonomie de référence pour 2026 est **MAST**(Cemri et coll., NeurIPS 2025, arXiv:2503.13657), dérivé de 1642 traces d'exécution sur 7 MAS open source à la pointe de la technologie montrant **41–86.7% failure rate**. Trois catégories racines: **Specification Problems**(41,77%)  ambiguïté de rôle, définition de tâches peu claire; **Coordination Failures**(36,94%)  défaillances de communication, désynchronisation de l'état; **Verification Gaps**(21,30%)  manque de validation, absence de vérifications de qualité.**Groupthink**La famille (arXiv:2508.05687) ajoute: effondrement de la monoculture (même modèle de base → défaillances corrélatives), biais de conformité (les agents renforcent les erreurs de l'autre), théorie déficiente de l'esprit, dynamique de motifs mixtes, défaillances de fiabilité en cascade. Exemple en cascade: tempêtes de retrait où une défaillance de paiement déclenche des retraités de commandes, qui déclenchent des retraités d'inventaire, qui submergent le service d'inventaire (10 fois la charge en secondes  nécessite des interrupteurs). Poison de mémoire: l'hallucination d'un agent entre dans la mémoire partagée, les agents en aval la traitent comme un fait; la précision se détériore progressivement, rendant douloureux le diagnostic de la cause racine.**STRATUS**(NeurIPS 2025) rapporte une amélioration de 1,5 fois de la réussite de l'atténuation par l'intermédiaire d'agents spécialisés de détection / diagnostic / validation.

> **【中文解读】**Ce chapitre présente le mode de défaillance de plusieurs agents et le mode de défaillance du groupe de pensées d'agents différents.

> **【拓展：failure modes mast groupthink→具体应用】**L'agent est un agent qui ne peut pas se poursuivre. L'agent ne peut pas changer de stratégie mais ne peut pas accepter.


**Type:** Learn | **类型:** 学习
**Languages:** Python (stdlib) | **语言:** Python（标准库）
**Prerequisites:** Phase 16 · 13 (Shared Memory), Phase 16 · 14 (Consensus and BFT), Phase 16 · 15 (Voting and Debate Topology) | **前置知识:** Phase 16 · 13（共享内存），Phase 16 · 14（共识与 BFT），Phase 16 · 15（投票与辩论拓扑）

>  **【前置】**Les élèves doivent être informés de la situation actuelle et de la situation actuelle.
>  **【类比】**MAST 失败分类 = "hôpital urgent诊分诊"──三类根因:规格问题(42%角色不清)、协调失败(37%通信失灵)、验证缺失(21%无质检)──MAST 1642 条 痕迹 显示 41-87% 失败率多 代理 不是银弹──Groupthink 家族:单一文化崩(同基模型 全错)、群体盲从级付联错支(修失触发重试风暴,10 秒 10 倍负载)──复:异见代理 + 随机化发言顺序 + 断路器──
**Time:** ~75 minutes | **时间:** ~75 分钟

## ♪ Problème ♪ Introduction du problème ♪

Les systèmes multi-agents échouent 41 à 86,7% du temps sur des tâches réelles (Cemri et coll. 2025 ont mesuré cela sur 7 MAS open-source). Cela ne peut pas être débogable par " juste ajouter plus d'agents. " Les défaillances ont des causes structurelles. La taxonomie MAST vous donne les catégories. Cette leçon cartographique chaque catégorie à un modèle de détection, de diagnostic et d'atténuation concret afin que les chiffres cessent d'être arbitraires.

> Les tests de dépistage de l'agent sont effectués en fonction de la capacité de l'agent à effectuer des tests. Il y a des raisons structurelles à l'échec.

La pratique de production 2026 consiste à traiter les modes d'échec comme des entrées de conception.

> La pratique de production de 2026 est un modèle de conception qui va échouer. Votre architecture n'est pas "assez bonne" jusqu'à ce que vous puissiez vous diriger vers chaque classe MAST et dire que vous déployez des mesures de réduction.

## Concept Le concept central

### Catégories MAST

**Specification Problems (41.77% of failures).**La tâche de l'agent n'a pas été définie assez étroitement.

> **规范问题（41.77% 的失败）。**Les tâches de l'agent sont définies de manière insuffisante.

- Ambigüité de rôle: deux agents pensent tous deux qu'ils sont le critique.
  Deux agents se considèrent comme des réviseurs.
- La tâche a été sous-déclarée: "récapituler ceci" lorsque l'utilisateur voulait un angle spécifique.
  Le problème est que les utilisateurs veulent un angle spécifique.
- Critères de réussite implicites: l'agent ne peut pas dire si elle a réussi.
  Le succès est un phénomène qui se produit à travers les différentes formes de communication.

Les atténuations:

> 缓解措施:

- Écrivez des contrats explicites de rôle.
  Traduction anglaise: édition de la lettre de rôle de chaque agent
- Avant de commencer, définissez "fait ressemble à X".
  Le terme "completé" est défini par X.
- Vérifie des spécifications avant vol: un agent séparé examine la définition de la tâche avant l'expédition.
  Traduction anglaise: pré-inspection pré-inspection: agent unique dans le cadre de la mission de révision définie.

**Coordination Failures (36.94%).**Les communications ou les échecs d'état.

> **协调失败（36.94%）。**通信或状态故障──

Les exemples:

> Je suis un enfant.

- Deux agents mettent à jour l'état partagé sans synchronisation.
  Deux agents différents de la région et de la région.
- Message perdu entre les agents (failure de file d'attente, délai de résiliation).
  Le groupe de travail est en train de se déchaîner.
- Départ de l'état: l'agent A pense que la tâche est terminée; l'agent B est toujours en train d'exécuter.
  À l'origine, le système de gestion de la tâche était en train de se dérouler.

Les atténuations:

> 缓解措施:

- L'état partagé de version avec une synchronisation optimiste.
  Le texte de la première édition de la série est en français.
- Reconnaissance explicite des messages critiques (retrait jusqu'à ce qu'ils soient accrus).
  Le récit de la première partie de la Bible est écrit dans le livre de Jérémie.
- Les points de contrôle de synchronisation d'état sont périodiques. Détecter la dérive tôt.
  Le premier est le premier, le deuxième, le deuxième, le troisième, le troisième, le troisième, le troisième, le troisième, le troisième, le troisième, le troisième, le troisième, le troisième, le troisième, le troisième, le troisième, le troisième, le troisième, le troisième, le troisième, le troisième, le troisième, le troisième, le troisième, le troisième, le troisième, le troisième, le troisième, le troisième, le troisième, le troisième, le troisième, le troisième, le troisième, le troisième, le troisième, le troisième, le troisième et le troisième.

**Verification Gaps (21.30%).**Aucune vérification indépendante des sorties.

> **验证缺口（21.30%）。**没有对输出独立检查──

Les exemples:

> Je suis un enfant.

- Un agent prétend réussir, personne ne le confirme.
  Le succès de l'agent est une réelle réussite.
- Chaque chaîne d'agents fait confiance à la production du précurseur.
  En français, le mot " agent " est traduit par " agent " en français par " agent " en français par " agent " en français par " agent " en français par " agent " en français par " agent " en français par " agent " en français par " agent " en français par " agent " en français par " agent " en français par " agent " en français par " agent " en français par " agent " en français par " agent " en français par " agent " en français par " agent " en français par " agent " en français par " agent " en français par " agent " en français par " agent " en français par " agent " en français par " agent " en français par " agent " en français par " agent " en français par " en français par " agent " en français par " agent " en français par " en français par " agent " en français par " en français par " agent " en français par " en français par " agent " en français par " en français par " en français par " en français par " en français " en français " en français par " en français " en français " en français " en français " en français " en français " en français " en français " en français " en français " en français " en français " en français " en français " en français " en français " en français " en français " en français " en français " en français " en français " en français " en français " en français en français " en français en français " en français " en français " en français " en français en français en français " en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en
- Des tests manquant sur le comportement composé émergent.
  Le nombre de personnes qui ont été affectées par la maladie est de 6,7%.

Les atténuations:

> 缓解措施:

- Agents de vérification indépendants (leçon 13).
  Le texte de la loi est le texte de la loi.
- Contract explicite de remise: "La sortie d'A doit passer le contrôleur C avant que B ne démarre".
  Le texte de la lettre de référence est le suivant:
- L'enregistrement des résultats pour l'analyse post-hoc.
  Le résultat est utilisé pour l'analyse des faits.

### La famille de la pensée de groupe (arXiv:2508.05687)

Cinq défaillances liées lorsque les agents homogénéisent ou s'imitent:

**Monoculture collapse.**Les mêmes données de base ou de formation → erreurs corrélatives.

**Conformity bias.**Les agents s'adaptent au plus fort ou le plus confiant de leurs pairs, même quand ils se trompent.

**Deficient ToM.**Les agents ne peuvent pas modéliser les croyances de l'autre; la coordination tombe en panne (leçon 18).

**Mixed-motive dynamics.**Les agents avec des incitations partiellement alignées dérivent vers le compromis, ce qui ne satisfait personne.

**Cascading reliability failures.**Le modèle d'erreur d'un composant déclenche des modèles d'erreur dans les composants dépendants.

### Exemple en cascade  la tempête de réessayer

Un modèle classique d'incidents de 2026:

```
payment service fails 10% of requests
   ↓
order agent retries payment (exponential backoff but naive)
   ↓
each retry is a new order-inventory check
   ↓
inventory service sees 2x normal load
   ↓
inventory service starts timing out
   ↓
every order retries inventory check
   ↓
inventory service sees 10x normal load
   ↓
cluster goes down
```

La solution est classique:**circuit breakers**- lorsque le taux d'erreur en aval dépasse le seuil, courts-circuits avec des résultats en cache ou par défaut.

Les interrupteurs de circuit sont l'une des rares mesures d'atténuation des défaillances multi-agents que vous empruntez directement à des systèmes distribués sans modification.

### Poison de mémoire (revisé)

La leçon 13 est que l'hallucination d'un agent devient un fait de mémoire partagée, les agents en aval raisonnent sur le fait empoisonné.

Le symptôme est une dégradation progressive de la précision.

L'atténuation: journal de l'annexe, provenance, vérificateur non rédigé.

### STRATUS  agents spécialisés pour la détection des défaillances

STRATUS (NeurIPS 2025) rapporte une amélioration de 1,5 fois du succès de l'atténuation lorsque vous déployez:

- **Detection agent.**Observation des symptômes (contradiction élevée, augmentation des tentatives, dérive de précision).
- **Diagnosis agent.**Compte tenu des symptômes, il est probable qu'il en résulte une cause profonde de la taxonomie MAST.
- **Validation agent.**Après l'atténuation, vérifiez si les symptômes disparaissent.

C'est une réponse à des incidents de style SRE, appliquée aux systèmes d'agents.

### L'audit en mode défaillance

Une meilleure pratique pour 2026 est un audit annuel (ou par version majeure) en mode défaillance:

1. **Trace sample.**Ramassez 1000 traces d'exécution réelles.
2. **Categorize.**Pour chaque défaillance de la trace, carte des catégories MAST + Groupthink.
3. **Compute failure-by-category rate.**Quelles catégories dominent votre système ?
4. **Rank mitigations.**Quel remède éliminerait le plus de défaillances ?
5. **Pick 2-3 mitigations.**Mise en œuvre; réaudit au trimestre prochain.

La discipline est plus importante que les choix spécifiques. Sans audits, les échecs se mélangent au bruit et ne sont jamais traités de manière systématique.

### Quand les systèmes échouent silencieusement

La catégorie de défaillance la plus dangereuse est la catégorie de défaillance de la correction silencieuse. Un système qui échoue fortement (crash, exception, alerte) peut être surveillé. Un système qui produit des sorties plausibles mais erronées ne peut pas être détecté par les journaux d'exception. C'est pourquoi les lacunes de vérification sont la catégorie la plus chère par défaillance même si elles ne sont que 21,30% par compte.

Investir dans:
- Révision humaine basée sur des échantillons.
- Des tests de régression de l'ensemble de données doré.
- Contrôle croisé entre agents sur des résultats importants.

### Échec par rapport à échec lent

Certains échecs sont immédiats; certains sont lents. Les échecs immédiats (délais de mise en œuvre, désaccord de schéma, erreur d'auteur) sont peu coûteux à détecter.

Le mouvement d'ingénierie de 2026: les proxies de défaillance lente de l'instrument afin que vous puissiez attraper la dérive avant qu'elle ne devienne une erreur visible.

## Construisez-le en main
```figure
a5-retry-cascade
```

## Faites-le

`code/main.py`les implémentations:

- `FailureTaxonomy` classe les incidents simulés en catégories MAST + Groupthink.
- `CircuitBreaker` modèle classique; s'ouvre lorsque le taux d'erreur dépasse le seuil.
- `RetryStormSimulator` montre la défaillance en cascade; allume/éteint le disjoncteur.
- `DetectionAgent` matcheur de symptômes de style STRATUS.

Je vais courir .

```
python3 code/main.py
```

Résultats attendus:
- tempête de reprise sans interrupteur: les erreurs d'inventaire explosent (simulées).
- avec interrupteur: plaquette au seuil; réponse en mode dégradé fournie.
- l'agent de détection marque le motif et nomme la catégorie MAST.

## Utilisez-le.

`outputs/skill-mast-auditor.md`effectue un audit de mode défaillance de type MAST sur un système multi-agents.

## Envoyez-le en ligne .

Discipline en mode défaillance dans la production:

- **MAST audit per quarter.**Les catégories changent à mesure que votre système grandit.
  Le mot grec traduit par " le mot grec "**每季度 MAST 审计。**Il n'y a pas de changement annuel.
- **Circuit breakers everywhere.**Chaque appel sortant vers un service dépendant.
  Le mot grec traduit par " le mot grec "**到处都是熔断器。**Chaque station de départ de service dépendant est utilisée à un taux d'erreur de 5 à 10%
- **Golden datasets.**Petit, de haute qualité, vérifié à la main, test de régression contre eux chaque semaine.
  Le mot grec traduit par " le mot grec "**黄金数据集。**Les tests de retour sont effectués chaque semaine.
- **STRATUS trio.**Les agents de détection + diagnostic + validation surveillent la production. Commencez par le seul agent de détection; ajoutez le diagnostic lorsque les symptômes sont bruyants.
  Le mot grec traduit par " le mot grec "**STRATUS 三重奏。**检测 + 诊断 + 验证代理 监控生产――从检测代理 开始;当症状杂时添加诊断――
- **Failure budget.**Expliquer explicitement le taux de défaillance par catégorie.
  Le mot grec traduit par " le mot grec "**失败预算。**Le taux de défaillance de la classe est évident SLO.

## Les exercices

1. On court .`code/main.py`Confirmez que le circuit est coupé, que la tempête est réinitialisée, modifiez le seuil de défaillance et observez le compromis.
2. La mise en œuvre d'une **slow-failure proxy**Le taux d'accords entre trois agents parallèles. Lorsqu'il baisse fortement, déclenchez une alerte. Simuler une dérive de monocultures en corréla­tion progressive des sorties d'agents.
3. Lisez Cemri et collègues (arXiv:2503.13657). Choisissez l'un de leurs 7 systèmes MAS et cartez ses 3 principales catégories de défaillance.
4. Lisez le document Groupthink (arXiv:2508.05687). Identifiez lequel des cinq modèles est le plus difficile à détecter dans la production.
5. Conceptez un trio de détection-diagnostic-validation de style STRATUS pour un système multi-agents spécifique que vous connaissez. Quels symptômes la détection surveille-t-elle? Quelles atténuations le diagnostic recommande-t-il? Comment la validation confirme-t-elle qu'ils fonctionnent?

## Les termes clés

| Term | What people say | What it actually means |
|------|----------------|------------------------|
| MAST / MAST 分类法 | "The 2026 taxonomy" / "2026 年分类法" | Cemri 2025; 3 root categories + 14 sub-types of failures. / Cemri 2025；3 个根类别 + 14 个失败子类型。 |
| Specification Problem / 规范问题 | "Role ambiguity" / "角色模糊" | Task or role under-defined; agents do not know what to do. / 任务或角色定义不足；Agent 不知道做什么。 |
| Coordination Failure / 协调失败 | "State drift" / "状态漂移" | Communication or sync breakdown between agents. / Agent 之间的通信或同步故障。 |
| Verification Gap / 验证缺口 | "No one checked" / "没人检查" | Outputs accepted without independent validation. / 输出未经独立验证即接受。 |
| Groupthink family / 群体思维族 | "Homogeneity failures" / "同质性失败" | Monoculture, conformity, deficient ToM, mixed-motive, cascading. / 单一文化、从众、ToM 不足、混合动机、级联。 |
| Monoculture collapse / 单一文化崩溃 | "Same model, same hallucinations" / "相同模型，相同幻觉" | Correlated errors from shared base model or training data. / 共享基础模型或训练数据的相关错误。 |
| Retry storm / 重试风暴 | "Cascading error amplification" / "级联错误放大" | One failure triggers retries which amplify load downstream. / 一次失败触发重试，放大下游负载。 |
| Circuit breaker / 熔断器 | "Fail fast on error rate" / "错误率快速失败" | Open when error rate exceeds threshold; short-circuit with default. / 错误率超阈值时断开；用默认值短路。 |
| STRATUS | "Incident response trio" / "事件响应三重奏" | Detection + diagnosis + validation agents. 1.5x mitigation success. / 检测 + 诊断 + 验证 Agent。1.5 倍缓解成功。 |
| Memory poisoning / 记忆投毒 | "Hallucinations propagate" / "幻觉传播" | Shared-memory fact tainted; downstream agents reason on poison. / 共享记忆事实被污染；下游 Agent 在毒化数据上推理。 |

## Encore une lecture

- [Cemri et al. — Why Do Multi-Agent LLM Systems Fail?](https://arxiv.org/abs/2503.13657) Taxonomie MAST, NeurIPS 2025
- [Groupthink failures in multi-agent LLMs](https://arxiv.org/abs/2508.05687) monoculture, conformité et taxonomie des cinq familles
- [STRATUS — specialized agents for MAS incident response](https://neurips.cc/) Entrée dans la procédure NeurIPS 2025 (détection + diagnostic + validation)
- [Release It! — stability patterns (Nygard)](https://pragprog.com/titles/mnee2/release-it-second-edition/) la référence canonique du disjoncteur
- [Anthropic — Multi-agent research system](https://www.anthropic.com/engineering/multi-agent-research-system) Notes de défaillance de la production
