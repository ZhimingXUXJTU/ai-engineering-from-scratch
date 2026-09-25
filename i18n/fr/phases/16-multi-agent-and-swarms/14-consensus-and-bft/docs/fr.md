# Consensus et tolérance byzantine à la faute pour les agents

> Les systèmes classiques distribués BFT répondent aux LLM stochastiques.**CP-WBFT**(arXiv:2511.10400) pèse chaque vote par une enquête de confiance; **DecentLLMs**(arXiv:2507.14928) est sans leader avec des propositions parallèles de travailleurs et une aggregation géométrique-médiane; **WBFT**(arXiv:2505.05103) combine le vote pondéré avec le regroupement de structures hiérarchiques pour diviser les nœuds Core et Edge. Le résultat empirique honnête de "Peut-être les agents de l'IA sont d'accord?" (arXiv:2603.01213) est que même l'accord scalaire est fragile aujourd'hui  un seul agent trompeur peut compromettre un mélange d'agents. Le BFT est nécessaire mais pas suffisant. Cette leçon construit un protocole BFT minimal, injecte trois attaques spécifiques à l'agent (menton byzantin, conformité sycophantique, monoculture d'erreur corrélative) et mesure comment chaque variante de consensus fait face.

> **【中文解读】**Ce chapitre présente le consensus et la manière de s'entendre sur le fait qu'un agent peut avoir des défaillances ou des comportements malveillants.

> **【拓展：consensus and bft→具体应用】**拜占庭容错 (BFT) 在多 Agent 系统中的应用:当部分 Agent可能故障或被攻击时,如何确保系统整体正确? 经典 BFT 算法 (PBFT) 需要3f+1 个节点容忍 f 个故障节点――在 LLM Agent 上下文中,'故障'可以是幻觉、注入或拒执行――实践中使用多数投票作为简化 BFT──


**Type:** Learn + Build | **类型:** 学习 + 构建
**Languages:** Python (stdlib) | **语言:** Python（标准库）
**Prerequisites:** Phase 16 · 07 (Society of Mind and Debate), Phase 16 · 13 (Shared Memory) | **前置知识:** Phase 16 · 07（心智社会与辩论），Phase 16 · 13（共享内存）

>  **【前置】**Pour les autres, il est nécessaire de se préparer à la phase 16 de la formation.
>  **【类比】**BFT = "Jury vote mais doit se protéger de l'esprit"― classique BFT = tolérer 1/3 节点说谎(PBFT 3f+1);LLM 版 = 加权投票(按置信度)+ 几何中位数聚合 + 层级聚类──三类攻击:拜占庭说谎、附和、相关错误(同一基模型 全错)──结论:BFT: BFT: BFT: BFT: BFT: BFT: BFT: BFT: BFT: BFT: BFT: BFT: BFT: BFT: BFT: BFT: BFT: BFT: BFT: BFT: BFT: BFT: BFT: BFT: BFT: BFT: BFT: BFT: BFT: BFT: BFT: BFT: BFT: BFT: BFT: BFT: BFT: BFT: BFT: BFT: BFT: BFT: BFT: BFT: BFT: BFT: BFT: BFT: BFT: BFT: BFT: BFT: BFT: BFT: BFT: BFT: BFT: BFT: BFT: BFT: BFT: BFT: BFT: BFT: BFT: BFT: BFT: BFT: BFT: BFT: BFT: BFT: BFT: BFT: BFT: BFT: BFT: BFT: BFT: BFT: BFT: BFT: BFT: BFT: BFT: BFT: BFT: BFT: BFT: BFT: BFT: BFT: BFT: BFT: BFT: BFT: BFT: BFT: BFT: BFT: BFT: BFT: BFT: BFT: BFT: BFT: BFT: BFT: BFT: BFT: BFT: BFT: BFT: BFT: BFT: BFT: BFT: BFT: BFT: BFT: BFT: BFT: BFT: BFT: BFT: BFT: BFT: BFT: BFT: BFT: BFT: BFT: BFT: BFT: BFT: BFT: BFT: BFT
**Time:** ~75 minutes | **时间:** ~75 分钟

## ♪ Problème ♪ Introduction du problème ♪

Vous avez N LLM agents qui produisent chacun une réponse. Ils ne sont pas d'accord. La majorité vote le mauvais parce que deux agents sont corrélés (le même modèle de base, les mêmes données de formation, les mêmes modes d'échec). Un troisième agent se trouve être faux d'une manière nouvelle  donc la majorité est une fausse majorité.

> Vous avez N'agent LLM, chacun produit une réponse. Ils ne sont pas d'accord. La majorité des votes choisit la mauvaise réponse, car deux agents sont liés. Les mêmes modèles de base, les mêmes données d'entraînement, les mêmes défauts.

Maintenant, ajoutez un agent trompeur: il est intentionnellement. Ou un agent sycophantique: il est d'accord avec qui a parlé le dernier. Dans la BFT classique, l'hypothèse est que les nœuds byzantins sont une fraction.`f < n/3`La réalité de 2026 est que les nœuds LLM sont stochastiques même quand ils sont honnêtes, corrélés entre les modèles et influencés par les résultats de l'autre.

> 现在加入一个欺骗性代理:它故意撒谎――或一个性代理:它同意最后一位发言人的意见―― Dans le classique BFT, il est supposé que le nombre de parties prenantes`f < n/3`并且行为任意──2026年现实是,LLM 节点即使诚实也随机,跨模型相关,并受影响彼此输出──你不能将它们视为独立的伯努利选民──

Le BFT classique (PBFT, 1999) n'est pas faux  il est incomplet. Il traite des détournements de bits arbitraires. Il ne traite pas "trois agents honnêtes partagent une hallucination parce qu'ils partagent des données de formation".

> Il traite des modifications volontaires, mais il ne traite pas "trois agents honnêtes" parce que le partage des données d'entraînement génère la même illusion.

## Concept Le concept central

### Ce que le BFT classique vous donne

La tolérance pratique à la faute byzantine (Castro et Liskov, OSDI 1999) tolère `f < n/3`Les nœuds byzantins. Le protocole a trois phases (préparation, préparation, engagement) et deux primitives (messages signés, certificats de quorum).`n >= 3f + 1`des nœuds honnêtes ou malveillants.

> 实用拜占庭容错(Castro et Liskov, OSDI 1999) tolérance `f < n/3`Le protocole a trois phases (preparation, préparation, soumission) et deux langues originales (signature, information, procès-verbal).`n >= 3f + 1`个诚意或恶意节点之间, une seule valeur est conclue.

Les garanties sont solides mais supposent:

> Ces garanties sont très fortes, mais supposons:

1. **Independent faults.**Les Byzantins ne se coordonnent pas.
   Le mot grec traduit par " le mot grec "**独立故障。**Le groupe de travail est en train de se dérouler.
2. **Honest nodes are truly honest.**La précision des résultats honnêtes n'est pas un problème; le protocole ne fait que régler les désaccords.
   Le mot grec traduit par " le mot grec "**诚实节点真正诚实。**L'équité de l'émission n'est pas un problème; le protocole ne traite que les différences.
3. **The question has a ground-truth answer.**Un consensus sur un fait erroné est toujours un consensus.
   Le mot grec traduit par " le mot grec "**问题有标准答案。**Le consensus sur les erreurs est toujours consensus.

Les agents de la LLM violent les trois. Deux agents qui utilisent le même modèle de base partagent des défauts. Un LLM "honnête" hallucine toujours. Et sur des questions ambiguës, la "vérité" est ce que les agents décident  il n'y a pas d'oracle externe.

> L'agent de la LLM                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                       

### Les trois attaques spécifiques à la LLM

**Byzantine lie.**Un agent donne une réponse délibérément fausse.`f < n/3`- Je suis désolé .

> **拜占庭撒谎。**Un agent a fourni des réponses délibérées et erronées.`f < n/3`, classique BFT peut être traité.

**Sycophantic conformity.**Un agent lit les réponses des autres avant de voter et s'aligne avec celui qui a parlé le dernier.

> **谄媚从众。**Un agent, en lisant la réponse de l'autre agent avant le vote, est en accord avec le dernier intervenant. Il n'est pas mal intentionné, mais il est lié au plus grand bruit.

**Correlated-error monoculture.**Trois agents partagent un modèle de base. Ils hallucinent la même réponse fausse. La majorité est fausse.

> **相关错误单一文化。**Trois agents partagent un modèle de base. Ils produisent le même faux-semblant. La plupart sont faux.

### Les réponses de 2025 à 2026

**CP-WBFT**(arXiv:2511.10400)  BFT pondéré à la confiance. Chaque électeur attache une sonde de confiance à sa réponse (une probabilité auto-déclarée ou une prédiction de modèle d'étalonnage séparé).

> **CP-WBFT**(arXiv:2511.10400)  confiance en confiance recherche augmentation de pouvoir BFT。 chaque électeur pour sa réponse ajouter une confiance en soi recherche, probabilité de rapport, ou prédiction du modèle de calibration unique)。 le droit de vote est réduit avec la confiance en soi。 le rapport a enregistré sur la carte complète une amélioration de +85.71% de la confiance en soi BFT。 contre les mesures de réduction du public  de l'Agent populaire  tend à avoir moins de confiance dans les positions proposées volontairement par lui-même)。

**DecentLLMs**Les agents de travail proposent en parallèle, les agents d'évaluation notent les propositions, la réponse finale est la médiane géométrique des positions notées.`f < n/2`- L'atténuation de: mensonge byzantin et erreurs corrélatives (la médiane géométrique est robuste à des valeurs étrangères et s'avance vers le grappillage dense, et non vers la moyenne modélisée).

> **DecentLLMs**(arXiv:2507.14928)  sans leader                                                                                                                                                                                                                                                        `f < n/2`时稳健.  contre les mensonges et les erreurs associées.

**WBFT**(arXiv:2505.05103)  Pise BFT avec Clustering structure hiérarchique. Les poids des votes sont attribués par la qualité de réponse plus un score de confiance appris de l'histoire. Les agents de cluster dans le noyau et l'extrémité; les agents de noyau doivent obtenir le consensus d'abord, les agents de l'extrémité suivent. Atténuation pour: évolutivité (le consensus du noyau est petit et rapide) et partiellement pour la monoculture (le noyau peut être choisi pour la diversité).

> **WBFT**Le pouvoir de vote est attribué par la qualité de réponse et par la répartition du nombre de fidèles qui ont été apprises dans l'histoire. Le pouvoir de vote est attribué par le pouvoir de vote.

### En empirie: " Les agents de l'IA peuvent-ils être d'accord ? "

Le document mesure l'accord scalaire (agents LLM se mettant d'accord sur une seule valeur numérique) sur plusieurs modèles frontaliers.

> Le document a mesuré la cohérence des échantillons sur plusieurs modèles de première ligne.

- Même sans adversaires, les agents de LLM ne sont pas d'accord sur les questions scalaires à des taux supérieurs à 30% sur de nombreux critères de référence.
  Même sans contre-joueur, le taux d'incohérence des questions de l'échantillon sur de nombreux tests de base dépasse 30%[1].
- Un agent qui adopte une personnalité trompeuse peut retirer le consensus de mélange d'agents de 40 points de pourcentage de la ligne de base honnête.
  En français, l'agent peut être mélangé avec un agent différent de l'agent différent.
- Les taux de désaccord sont corrélés à la diversité des modèles  les ensembles hétérogènes sont plus en désaccord que les ensembles homogènes (bien: erreurs non corrélatives) mais dérivent aussi plus lentement (mauvais: plus de temps pour l'accord).
  Le taux d'incohérence avec le modèle de diversité est différent de celui de l'intégration.

Le résultat: BFT vous donne un dispositif pour aligner les sorties, mais il ne vous indique pas si la sortie alignée est correcte.

> 结论:BFT 提供出口对齐的机制, mais ne vous dit pas si la sortie对齐的输出是正确的吗.

### Le protocole de base, dépouillé

Un tour BFT minimal pour les agents de LLM:

```
1. task arrives; each agent i produces answer a_i
2. each agent attaches confidence probe c_i in [0, 1]
3. aggregator collects (a_i, c_i) from all n agents
4. aggregator groups by semantic cluster (equivalent answers)
5. aggregator computes weight for each cluster C:
     w(C) = sum_{i in C} c_i
6. winner = cluster with max weight, if max > threshold * sum(c_i)
   else: retry or escalate
7. minority clusters logged with provenance for post-hoc audit
```

La phase de clustering sémantique est la tournure spécifique du LLM. Deux réponses "les rapports d'étude 4,2%" et "l'amélioration de 4,2%" sont le même cluster.

> Les deux réponses "Recherche rapport 4,2%" et "4,2% d'amélioration" sont les mêmes ── simple en strings phases etc.

### Régularisation des seuils

Le `threshold`Paramètre décide quand accepter et quand réessayer. trop bas: vous acceptez les faibles majorités. trop haut: vous n'acceptez jamais rien.`n=5-7`Les agents, plus élevés pour les plus petits `n`En dessous d'un seuil, escaladez vers un humain ou un ensemble d'agents différents.

> `threshold`参数决定何时接受、何时重试──太低: accepter faible majorité──太高:永远不接受任何东西──`n=5-7`个 Agent 时为0.5-0.67,较小的 `n`时更高──低于值时, amélioration de la valeur humaine ou de l'agent différent 集合──

### Lorsque le consensus ne contribue pas

- **Ambiguous questions.**Si la question n'a pas de vérité fondamentale, le consensus est une opinion.
  Le mot grec traduit par " le mot grec "**模糊问题。**Si le problème n'a pas de réponse standard, le consensus est l'opinion.
- **Compound questions.**"Écrivez un code et expliquez-le"  deux réponses.
  Le mot grec traduit par " le mot grec "**复合问题。**"编写代码并解释"两个答案──分别独立投票──
- **Adversarial multi-round.**Si les agents peuvent observer les tours précédents et imiter (débat du 2023), ils commencent à s'entendre les uns avec les autres indépendamment de la vérité.
  Le mot grec traduit par " le mot grec "**对抗性多轮。**Si l'agent peut observer les précédents débats, ils seront en accord entre eux.

## Construisez-le en main
```figure
swarm-consensus-wave
```

## Faites-le

`code/main.py`les implémentations:

- `AgentVoter` une politique écrite avec (réponse, confiance).
  Le mot grec traduit par " le mot grec "`AgentVoter` 带有(答案,置信度) du scénario
- `MajorityVote` pluralité classique.
  Le mot grec traduit par " le mot grec "`MajorityVote` 经典多数投票──
- `CPWBFT` vote pondéré par la confiance avec regroupement sémantique.
  Le mot grec traduit par " le mot grec "`CPWBFT` 带语义聚类的信任度加权投票──
- `DecentLLMs` Aggrégation géométrique-médiane des propositions obtenues.
  Le mot grec traduit par " le mot grec "`DecentLLMs` 评分 评价 评价 评价 评价 评价 评价 评价 评价 评价 评价 评价 评价 评价 评价 评价 评价 评价 评价 评价 评价 评价 评价 评价 评价 评价 评价 评价 评价 评价 评价 评价 评价 评价 评价 评价 评价 评价 评价 评价 评价 评价 评价 评价 评价 评价 评价 评价 评价 评价 评价 评价 评价 评价 评价 评价 评价 评价 评价 评价 评价 评价 评价 评价 评价 评价 评价 评价 评价 评价 评价 评价 评价 评价 评价 评价 评价 评价 评价 评价 评价 评价 评价 评价 评价 评价 评价 评价 评价 评价 评价 评价 评价 评价 评价 评价 评价 评价 评价 评价 评价 评价 评价 评价 评价 评价 评 评 评 评 评 评 评 评 评 评 评 评 评 评 评 评      评   评 评                               评                                 评                                                                               
- `Scenario` exploite chaque agrégateur sous trois modèles d'attaque.
  Le mot grec traduit par " le mot grec "`Scenario` Dans trois modes d'attaque fonctionnent chaque polymère.

Modèles d'attaque mis en œuvre:

> 实现的攻击模式:

1. `byzantine`Un agent ment avec une grande confiance.
   Le mot grec traduit par " le mot grec "`byzantine`Un agent qui est très convaincu de mentir.
2. `sycophancy`Un agent copie la première réponse qu'il voit, avec la même confiance.
   Le mot grec traduit par " le mot grec "`sycophancy`Un agent a copié la première réponse qu'il a vue, en toute confiance.
3. `monoculture`: trois agents partagent une réponse erronée (erreur corrélative) avec confiance modérée.
   Le mot grec traduit par " le mot grec "`monoculture`Il y a trois agents qui partagent une erreur de réponse, une erreur de confiance, etc.

Je vais courir .

```
python3 code/main.py
```

Les résultats attendus: une table de (attaque, agrégateur) -> réponse finale, avec la réponse correcte mise en évidence. La pluralité échoue dans le cas de la monoculture. La pondération de confiance du CPWBFT atténue la sycophancy.

> 预期输出:一张(攻击,聚合器) -> Le formulaire du dernier résultat, correct answer 高亮显示── la majorité des voix ont échoué dans un cas de culture unique── la confiance accrue du CPWBFT a diminué── lorsque la culture unique ne dépasse pas la moitié de l'heure, le nombre de décent LLMs est tendu vers l'intégrité──

## Utilisez-le.

`outputs/skill-consensus-designer.md`conçoit un protocole de consensus pour un ensemble multi-agents: méthode de regroupement, pondération, seuil et politique d'escalade pour les tours sous-seuils.

> `outputs/skill-consensus-designer.md`Pour plusieurs agents, le protocole de consensus de conception collective: méthode de regroupement, de poids, de valeur, ainsi que des stratégies de mise à niveau inférieures à la valeur de la série.

## Envoyez-le en ligne .

Avant l'expédition de tout mécanisme de consensus:

- **Attack-test with at least the three patterns**Votre protocole devrait échouer de façon prévisible, pas silencieuse.
  Le mot grec traduit par " le mot grec "**至少用上述三种模式进行攻击测试。**Votre accord devrait être un échec prévisible, et non un échec silencieux.
- **Log every minority cluster**Les groupes minoritaires sont votre système d'alerte précoce pour les erreurs corrélatives.
  Le mot grec traduit par " le mot grec "**记录每个少数派簇** et son origine ∼ minorité ∼ sont votre correction des erreurs du système pré-alerte précoce ∼
- **Enforce bounded rounds.**Pas de "continuer à débattre jusqu'à un accord" qui récompense la sycophancy.
  Le mot grec traduit par " le mot grec "**强制限制轮次。**Ne débattez pas jusqu'à ce que vous soyez d'accord.
- **Separate agreement from correctness.**La sortie de consensus est envoyée à un vérificateur; le vérificateur est indépendant de l'ensemble.
  Le mot grec traduit par " le mot grec "**分离一致性和正确性。**共识输出交给验证器;验证器 indépendante du groupe.
- **Monitor the agreement rate.**Une hausse rapide signifie un biais de conformité; une chute rapide signifie une dérive du modèle.
  Le mot grec traduit par " le mot grec "**监控一致率。**Une hausse rapide signifie une déviation du public; une baisse rapide signifie un déménagement du modèle.

## Les exercices

1. On court .`code/main.py`- Confirmer la pluralité échoue à l'attaque des monocultures, mais le CPWBFT l'atténue partiellement lorsque la confiance des monocultures est inférieure à 0,7.
   Le mot " l' économie " est traduit par " l' économie ".`code/main.py` Confirmer que la majorité des voix ont échoué dans les attaques contre la culture unique, mais que lorsque la confiance en la culture unique était inférieure à 0,7 heures, la CPWBFT a partiellement atténué le problème.
2. Ajoutez un quatrième modèle d' attaque:**silent abstention** un agent refuse de répondre ("Je ne sais pas"). Comment chaque agrégateur doit-il traiter les abstentions?
   Le deuxième type de défense est le "Castor"**静默弃权** Un agent  refuse de répondre  "je ne sais pas")  Comment chaque polymère devrait-il traiter l'absence?
3. S'il vous plaît modifier le clustering sémantique de la canonisation de chaîne à la simulation d'intégration (utilisez n'importe quel modèle d'intégration open source).
   Le mot "partage" est un mot qui signifie "partage" ou "partage".
4. Lire CP-WBFT (arXiv:2511.10400). Mettre en œuvre l'étape d'étalonnage de la sonde de confiance (un modèle d'étalonnage séparé vérifie la confiance déclarée par chaque agent). Mesurer le gain de précision sur le scénario de monocultures.
   Le taux de précision dans les scènes culturelles uniques augmente.
5. Lisez " Les agents de l'IA peuvent-ils être d'accord ? " (arXiv:2603.01213). Reproduire une expérience simplifiée d'accord scalaire: trois agents, une question scalaire, la requête de la personne trompeuse.
   Le problème est que les données de l'agent de l'IA peuvent être utilisées pour des tests de conformité de type "AI Agent 能达成一致吗?"

## Les termes clés

| Term | What people say | What it actually means |
|------|----------------|------------------------|
| BFT / 拜占庭容错 | "Byzantine fault tolerance" / "拜占庭容错" | Castro-Liskov 1999 protocol for consensus with `f < n/3` arbitrary faults. / Castro-Liskov 1999 协议，容忍 `f < n/3` 个任意故障节点的共识。 |
| Byzantine / 拜占庭 | "Any bad behavior" / "任何不良行为" | A node that can lie, drop messages, fail silently — anything but crash safely. / 可以撒谎、丢弃消息、静默失败的节点——除了安全崩溃外的任何行为。 |
| Confidence probe / 置信度探测 | "How sure are you?" / "你有多确定？" | Self-reported or calibrator-predicted probability attached to a vote. / 附加在投票上的自报或校准器预测的概率。 |
| Semantic clustering / 语义聚类 | "Same answer, different words" / "相同答案，不同措辞" | Grouping equivalent answers before counting votes. / 在计票前将等价答案分组。 |
| Geometric median / 几何中位数 | "Robust center" / "稳健中心" | The point minimizing sum of distances to sample points. Robust to outliers, unlike the mean. / 最小化到样本点距离之和的点。对异常值稳健，与均值不同。 |
| Monoculture / 单一文化 | "Same model, same failures" / "相同模型，相同失败" | Correlated errors when agents share training data or base model. / Agent 共享训练数据或基础模型时的相关错误。 |
| Sycophantic conformity / 谄媚从众 | "Agreeing with the loud voice" / "附和最大声的声音" | An agent's vote biases toward whoever spoke first/loudest. / Agent 的投票偏向最先/最大声发言的人。 |
| Core/Edge / 核心/边缘 | "Hierarchical BFT" / "层次化 BFT" | WBFT split: small Core consensus first, Edge nodes follow. Bounds latency. / WBFT 分割：小核心先达成共识，边缘节点跟随。限制延迟。 |

## Encore une lecture

- [Castro & Liskov — Practical Byzantine Fault Tolerance (OSDI 1999)](https://pmg.csail.mit.edu/papers/osdi99.pdf) la fondation
- [CP-WBFT — Confidence-Probe Weighted BFT](https://arxiv.org/abs/2511.10400) pondération des voix par confiance
- [DecentLLMs — leaderless multi-agent consensus](https://arxiv.org/abs/2507.14928) Aggrégation géométrique-médiane
- [WBFT — Weighted BFT with Hierarchical Structure Clustering](https://arxiv.org/abs/2505.05103) Split de base/extrémité pour une latence limitée
- [Can AI Agents Agree?](https://arxiv.org/abs/2603.01213) Fragilité des accords scalaires et attaque de personnes trompeuses
