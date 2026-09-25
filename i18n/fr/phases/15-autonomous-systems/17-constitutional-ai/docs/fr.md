# L' IA constitutionnelle et les règles sont annulées.

> Le 22 janvier 2026, Claude Constitution de Anthropic a 79 pages et est CC0. Il passe de l'alignement fondé sur les règles à l'alignement fondé sur la raison et établit une hiérarchie prioritaire de quatre niveaux: (1) sécurité et soutien à la surveillance humaine, (2) éthique, (3) lignes directrices anthropologiques, (4) utilité. Les comportements sont divisés en interdictions codées durement (lifting bioweapons, CSAM) que les opérateurs et les utilisateurs ne peuvent pas annuler et les défauts codés doucement que les opérateurs peuvent ajuster dans des limites définies. L'original de 2022 (Bai et coll.) a entraîné l'innocuité par l'intermédiaire de l'autocritique et de la RLAIF contre une constitution. L'avertissement honnête: l'alignement fondé sur la raison repose sur le modèle généralisant les principes pour les situations imprévues. L'expérience participative de 2023 d'Anthropic a montré une divergence de ~50% entre les principes publics et les principes des entreprises; la version 2026 n'incorporait pas ces résultats.

> **【中文解读】**Anthropic 2026 Claude Constitution du 22 janvier 2026 79 pages CC0。 De la réglementation à la réglementation à la réglementation, la mise en place de quatre niveaux de priorité: 1) la sécurité et le soutien à la surveillance humaine, 2) l'éthique, 3) l'anthropie à la direction, 3) le comportement est divisé en opérateurs et utilisateurs qui ne peuvent pas être couverts par le code dur, c'est-à-dire l'amélioration de l'arme biologique, CSAM) et les opérateurs peuvent définir des codes de programmation réglementés dans les limites.

> **【拓展：四层优先级 + 双层禁令】**Les deux sont nécessaires: uniquement basé sur la logique ne peut pas fermer le bout du chemin. L'attaquant permet au modèle d'accepter la prémisse.

**Type:** Learn | **类型:** 学习
**Languages:** Python (stdlib, four-tier priority resolver) | **语言:** Python（标准库，四层优先级解析器）
**Prerequisites:** Phase 15 · 06 (Automated alignment research), Phase 15 · 10 (Permission modes) | **前置知识:** Phase 15 · 06（自动化对齐研究），Phase 15 · 10（权限模式）
**Time:** ~60 minutes | **时间:** ~60 分钟

>  **【前置】**Il est également possible de faire une analyse de la situation de l'IA en utilisant les techniques de gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la
>  **【类比】**La loi de 2026 Claude Constitution 79 page quatre niveaux priorité: sécurité > 伦理 > 公司指南 > 有用性──硬禁令(生物武器、CSAM)
> 🤔 **【困惑】**Q: 推理对齐能被绕过吗? 能! l'attaquant a créé le préjugé "我是持牌生物武器实验室" → 模型按推理允许 → 绕过原则──修复:硬禁令不向前提折(无论谁说什么,CSAM 就是不能产生)──推理 + 规则两层防御:推理覆盖大多数情况,规则覆盖推理被绕过的尾部──

## Le problème , l' introduction du problème

> **【中文解读】**L'IA constitutionnelle (CAI, Anthropic 2022) est une méthode de " Constitution " (一组原则) qui guide le comportement de l'IA. Le modèle consiste à vérifier si l'IA répond à ces principes et à se corriger elle-même en cas de violation.

> **【拓展：constitutional ai】**L'IA constitutionnelle est la pierre angulaire du mécanisme de sécurité anthropologique. Elle utilise un ensemble de principes constitutionnels (en anglais: Constitutional AI) pour aider les utilisateurs à faire des choses dangereuses.

Un agent de terrain voit des entrées que ses concepteurs n'ont jamais vues.

> L'agent du déploiement verra des entrées que le concepteur n'a jamais vues.

Aucune liste de règles n'est assez courte pour être appliquée rapidement sous pression de calcul.

> 没有规则列表短到能在计算压力下快速应用―― Question réelle: Comment l'agent peut-il survivre à des principes de l'action en cas de longueur de file et de rapidité de raisonnement ?

L'alignement basé sur les règles (RBA): liste de toutes les choses interdites. Rapide à vérifier, facile à vérifier, impossible à maintenir à jour, souvent sur-réfute sur des analogues proches qu'il n'a pas anticipé. L'alignement basé sur la raison (la Constitution Claude de 2026): encodez les principes, laissez le modèle raisonner. Écailles dans les cas invisibles, plus difficile à vérifier, mode échec est une mauvaise application des principes plutôt que de manquer la règle.

> 基于规则对齐(RBA): énumérer chaque chose interdite―检查快、审计易、不可能保持当前、常对未预期近似物过度拒绝―基于推理对齐(2026 Claude Constitution):编码原则让模型推理―跨未见案例扩展、更难审计、失败模式是原则误用而非遗漏规则―

> **【中文解读】**Ce chapitre présente le concept et la méthode de réalisation de l'agent d'IA. L'agent est un système autonome à action de la MLL, capable d'observer l'environnement, de penser, de prendre des décisions, d'exécuter des actions et de les faire boucler jusqu'à la fin de l'objectif.

La Constitution de 2026 prend une position centrale explicite.

> La Constitution de 2026 adopte un point de vue clair.

Tout le reste est fondé sur la raison dans une hiérarchie de quatre niveaux: la sécurité et le soutien à la surveillance humaine d'abord; l'éthique en second lieu; les directives déclarées par Anthropic en troisième lieu; l'utilité en dernier lieu.

> Tout le reste est basé sur quatre niveaux: sécurité et soutien à la surveillance humaine prioritaire; éthique suivante; guide de la déclaration anthropique; utilité finale.

## Le concept de base.

### La hiérarchie des priorités de quatre niveaux.

1. **Safety and supporting human oversight.**Le modèle donne la priorité à ne pas saper la capacité des humains et de l'Anthropic à superviser et à corriger l'IA.
   Le mot grec traduit par " le mot grec "**安全和支持人类监督。**Le modèle prioritaire ne détruit pas les capacités de l'IA en matière de surveillance et de réparation humaine et anthropologique.
2. **Ethics.**L'honnêteté, éviter de nuire à des personnes, ne pas tromper, ne pas manipuler.
   Le mot grec traduit par " le mot grec "**伦理。**诚实、避免对人伤害、不欺骗、不操纵──冲突时取代人类指南──
3. **Anthropic guidelines.**Les normes opérationnelles Anthropic a décidé la question: la portée du produit, les modèles d'interaction, quels outils utiliser quand.
   Le mot grec traduit par " le mot grec "**Anthropic 指南。**Les produits sont utilisés pour la production de produits, les produits sont utilisés pour la production de produits, les produits sont utilisés pour la production de produits, les produits sont utilisés pour la production de produits, les produits sont utilisés pour la production de produits, les produits sont utilisés pour la production de produits et les produits sont utilisés pour la production de produits.
4. **Helpfulness.**Soyez aussi utile que possible dans les priorités supérieures.
   Le mot grec traduit par " le mot grec "**有用性。**Le plus bas. Dans la plus haute priorité.

Lorsque les niveaux sont en conflit, les gains sont plus élevés. C'est la même forme que les priorités Unix ou la QoS réseau  le cadre est destiné à produire une résolution prévisible, pas nécessairement le meilleur comportement sur un seul axe.

> Le système de sécurité est un système de sécurité qui est en train de se développer.

### Les interdictions de code dur par rapport aux défauts de code doux .

**Hardcoded:**

> **硬编码：**

- Le renforcement des armes biologiques / RBCN
  Le référencement à la radio
- CSAM
  Le terme "détention sexuelle" désigne la personne qui a été victime de détention sexuelle.
- Attaques contre des infrastructures critiques
  Néo-latin: attaques contre les infrastructures clés
- L'erreur des utilisateurs concernant l'identité du modèle lorsqu'ils sont directement interrogés
  Traduction anglaise: été directement interrogé

L'opérateur ne peut pas les annuler. L'utilisateur ne peut pas les annuler. Ils sont appliqués au niveau des poids de modèle lorsque cela est possible (entraînement RLHF / IA constitutionnelle) et à la couche d'inférence lorsque cela n'est pas le cas.

> Les utilisateurs ne peuvent pas les couvrir. Ils sont en phase de formation de l'IA constitutionnelle et ne peuvent pas être en phase de formation.

**Soft-coded defaults (operator-adjustable):**

> **软编码默认（操作员可调）：**

- Dépôts de longueur de réponse
  Réponses à la longueur et à la longueur
- Scope actuel (le modèle peut refuser des sujets en dehors du déploiement de l'opérateur)
  Le modèle peut être refusé à l'opérateur (en anglais)
- Style (formel contre occasionnel)
  Le mot " officiel " est traduit par " officiel "
- Modèles d'utilisation des outils
  Le modèle de l'utilisation

Les réglages de l'opérateur se produisent à l'intérieur d'une limite déclarée.

> L'opérateur ne peut pas passer par le renom de déménagement de l'arrêt de code strict.

### L' entraînement CAI 2022

L'IA constitutionnelle originale (Bai et al., 2022) a formé l'imharmonie:

> La formation de l'AI (AI)

1. Générer des réponses à un ensemble de demandes.
   Le mot "réponse" est traduit par "réponse".
2. Demandez au modèle de critiquer chaque réponse contre une constitution (principes explicites).
   Le texte de la loi est le texte de la loi.
3. Réviser la réponse en fonction de la critique.
   Traduction anglaise: basé sur la critique
4. RLAIF (apprentissage renforcé à partir de rétroaction de l'IA) sur les paires révisées.
   Le RLAIF est issu de l'IA (AI)

Le résultat: un modèle qui refuse les demandes nuisibles avec des explications de principe, et non des refus généraux.

> 结果: 以原则性解释而非一概拒绝拒绝有害请求的模型──2026 宪法使用此训练后代加额外对显而易见的层次训练后──

### Quels alignements fondés sur la raison attraper et manquer basé sur la raison pour saisir et perdre quoi

**Catches:**

> **捕获：**

- Combinaisons imprévues de primitifs autorisés où le principe s'applique clairement.
  Le mot grec traduit par "partie" est traduit par "partie": "partie": "partie": "partie": "partie": "partie": "partie": "partie": "partie": "partie": "partie": "partie": "partie": "partie": "partie": "partie": "partie": "partie": "partie": "partie": "partie": "partie": "partie": "partie": "partie": "partie": "partie": "partie": "partie": "partie": "partie": "partie": "partie": "partie": "partie": "partie": "partie": "partie": "partie":": "partie": "partie":": "partie":": "partie":": "partie":": "partie":":": "partie": "partie":":": "partie":":" partie": "partie": "partie":": "partie": "partie":":": "partie":": "partie":":": "partie":": "partie":": "partie":":": "partie":":": "partie":":": "partie":":": "partie":": "partie":":": "partie":":":": "partie":":":": "partie":": "partie":":":": "partie: "partie":":":":":":":": "partie: "partie: "partie: "partie":":":":":":":":":":":":":":": "partie: "partie: "partie: "partie: "partie: "partie:":":":":":":":":":":":":":":":":":":":":":":":": "partie: "partie: "partie: "partie: "partie: "partie: "partie: "partie: "partie:
- Des demandes novatrices qui sont proches de celles interdites.
  Néo-latin: forbidding request of approximate similar things 新请求──
- Des attaques d'ingénierie sociale qui reposent sur "tu n'as pas dit que X était interdit".
  Suivant: "Tu n'as pas dit X est interdit"

**Misses:**

> **遗漏：**

- Attaques qui exploitent l'ambiguïté du principe ("l'utilisateur a demandé cela de sorte que l'utilité dit oui").
  Le mot "utilisateur doit être utile" est traduit par "utiliser le principe de l'attaque".
- Scenarios où deux principes sont en conflit de manière inattendue et où l'ordre des niveaux est ambigu.
  Deux principes sont en conflit et en conflit de manière inattendue.
- Dérive lente en principe d'interprétation sur les cycles de formation (réinterprétation).
  Le principe de l'entraînement de cycle de l'entraînement de cycle de l'entraînement de cycle de l'entraînement de l'entraînement de cycle de l'entraînement de cycle de l'entraînement de cycle de l'entraînement de cycle de l'entraînement de cycle de l'entraînement de cycle de l'entraînement de cycle de l'entraînement de cycle de l'entraînement de cycle de l'entraînement de cycle de l'entraînement de cycle de l'entraînement de cycle de l'entraînement de cycle de l'entraînement de cycle de l'entraînement de cycle de l'entraînement de cycle de l'entraînement de cycle de l'entraînement de cycle de l'entraînement de la formation de cycle de la formation de cycle de la formation de cycle de la formation de cycle de la période de l'entraînement de la formation de cycle de la formation de cycle de la formation de cycle de cycle de la période de l'entraînement de la formation de cycle de la formation de cycle de cycle de la formation de cycle de cycle de l'entraînement de la période de l'entraînement de la formation de cycle de la période de l'entraînement de la période de formation de l'entraînement de la période de l'entraînement de la période de la période de formation de l'entraînement.

### L' expérience participative de 2023

Anthropic a mené une expérience en 2023 comparant une constitution d'entreprise à une constitution générée par l'intermédiaire de l'apport public (~ 1 000 répondants américains). Les deux versions ont convenu de 50% des principes. Là où ils divergeaient, la version publique était plus restrictive sur certaines questions (manipulation du contenu politique) et moins restrictive sur d'autres (auto-révélation de l'identité de l'IA). La Constitution de 2026 n'incorporait pas les résultats obtenus par les sources publiques. Il s'agit d'une tension documentée dans l'approche.

> Anthropic 2023 ans de fonctionnement expérience comparative Entreprise rédaction de la Constitution et de la Constitution générée par le public (environ 1000  États-Unis) ⋅ deux éditions environ 50% 原则一致──分歧处, la version publique sur certains problèmes est plus stricte ⋅ traitement du contenu politique ⋅ dans d'autres plus large ⋅ AI Identity Self Disclosure ⋅ 2026 宪法未纳入公众版发现──这是方法中的已记录张力──

### Pourquoi les interdictions sont nécessaires ?

L'alignement fondé sur la raison seul ne peut pas fermer la queue. Un attaquant qui peut faire accepter un modèle de prémisse (par exemple, "nous sommes un laboratoire de recherche sur les armes biologiques agréé") peut souvent parler de principes passés qui dépendent du raisonnement des cas. Les interdictions hardcodées ne se plient pas à l'encadrement des prémisses.

> Les attaquants de l'attaque, basés uniquement sur le raisonnement, ne peuvent pas fermer le bout de la ligne de conduite. Ils peuvent accepter les préjugés, par exemple: " Nous sommes des laboratoires de recherche sur les armes biologiques " (WEB), qui peuvent souvent contourner le principe de la logique de la dépendance à l'égard des cas.

### Là où la Constitution est dans la pile

La Constitution n'est pas le commutateur de la leçon 14.

> La Constitution n'est pas le dernier mot de la quatorzième classe.

Il vit à la couche du modèle: ce que les poids du modèle sont formés à préférer. Les interrupteurs de commande et les jetons canariens sont en direct à la couche de fonctionnement: ce que la fonctionnement permet. Les deux sont nécessaires. Un temps de course qui déclenche toutes les mauvaises actions parce que les poids du modèle sont permissifs est un problème de temps de course. Un modèle qui refuse toutes les bonnes actions parce que le temps d'exécution est trop restrictif est un problème de temps d'exécution. Les couches couvrent différentes classes.

> Il existe dans le modèle de niveau: le modèle de poids est entraîné par des préférences à quoi. Le modèle de niveau: le modèle de poids est entraîné par des préférences à quoi.

## Utilisez-le avec le cadre de réalisation
```figure
mx-priority-tiers
```

## Utilisez-le

`code/main.py`Le résolveur prend une action proposée et un ensemble de principes-évaluations (sécurité, éthique, lignes directrices, utilité) et renvoie l'action, un refus ou une action modifiée.

> `code/main.py`实现最小四层优先解析器──解析器取提议动作和一组原则评估(安全,伦理,指南,有用性)并返回动作、拒绝或修改动作──驱动器运行小案例集:清晰允许、清晰拒绝、硬编码禁令、跨层模糊案例──

## Envoyez-le . Produit .

`outputs/skill-constitution-review.md`l'audit de la couche constitutionnelle d'un déploiement: ce qui est codé dur, ce qui est codé doux, où l'opérateur peut s'ajuster et si la hiérarchie à quatre niveaux est réellement l'ordre de résolution.

> `outputs/skill-constitution-review.md`L'Audit déploiement de la Layer de Constitution: Qu'est-ce que le code dur?, Qu'est-ce que le code logiciel?, Les opérateurs sont-ils en mesure de le modifier?

## Les exercices

1. On court .`code/main.py`- Confirmer les feux d'interdiction d'utilisation d'un code dur même lorsque la utilité est élevée. Modifier le résolveur pour peser l'utilité au-dessus de l'éthique; observer le mode d'échec.
   Le mot " l' économie " est traduit par " l' économie ".`code/main.py` Confirmer l'utilité de l'interdiction de code dur à haute fréquence.

2. Lisez la Constitution de Claude (publique, 79 pages, CC0). Identifiez un principe que vous pensez être sous-spécifié.
   Le texte de la Constitution de Claude est un texte écrit en français.

3. Conceptez un ensemble par défaut de code doux pour un agent de support client. Que régle l'opérateur? Que peut-il ne pas toucher? Justifiez chaque limite.
   Pour le client, l'agent est un agent de conception.

4. Lisez le document CAI 2022 de Bai et coll. Décrivez un cas où la boucle de critique et de révision de l'IA constitutionnelle produirait un résultat pire qu'une règle générale.
   Le projet de loi de la loi de l'IA, qui a été adopté en 2022, décrit l'IA constitutionnelle.

5. L'expérience participative d'Anthropic en 2023 a révélé une divergence de ~50% entre les principes publics et des entreprises. Choisissez une catégorie où cela importe pour le déploiement de la production (par exemple, la neutralité politique). Proposez un design qui permet aux opérateurs d'exprimer leurs propres valeurs alors que les interdictions hardcodées restent intactes.
   En 2023, l'expérience anthropologique participative a révélé que les principes du public et des entreprises étaient à environ 50% divisés.

## Les termes clés

| Term | What people say | What it actually means |
|---|---|---|
| 术语 | 通俗说法 | 实际含义 |
| Constitutional AI | "Anthropic's alignment method" | Self-critique + RLAIF against a written constitution |
| Constitutional AI | "Anthropic 的对齐方法" | 对照书面宪法的自我批评 + RLAIF |
| Reason-based alignment | "Principles, not rules" | Model reasons over principles to handle unseen cases |
| 基于推理对齐 | "原则而非规则" | 模型对原则推理以处理未见案例 |
| Hardcoded prohibition | "Never do X" | Rule-based prohibition no operator or user can override |
| 硬编码禁令 | "永不做 X" | 操作员或用户不能覆盖的基于规则的禁令 |
| Soft-coded default | "Operator-adjustable" | Behaviour within a declared bound, operator controls |
| 软编码默认 | "操作员可调" | 声明边界内的行为，操作员控制 |
| Four-tier hierarchy | "Priority order" | safety > ethics > guidelines > helpfulness |
| 四层层次 | "优先级顺序" | 安全 > 伦理 > 指南 > 有用性 |
| RLAIF | "AI feedback RL" | RL where the reward comes from model-generated critiques |
| RLAIF | "AI 反馈 RL" | 奖励来自模型生成批评的 RL |
| Participatory constitution | "Public-sourced principles" | 2023 Anthropic experiment; ~50% divergence from corporate |
| 参与式宪法 | "公众来源原则" | 2023 Anthropic 实验；与企业约 50% 分歧 |
| Principle drift | "Interpretation slip" | Slow change in how the model reads a fixed principle text |
| 原则漂移 | "解释滑移" | 模型如何读取固定原则文本的缓慢变化 |

## Encore une lecture

- [Anthropic — Claude's Constitution (January 2026)](https://www.anthropic.com/news/claudes-constitution) le document CC0 de 79 pages.
  Le texte de la loi est en français.
- [Bai et al. — Constitutional AI: Harmlessness from AI Feedback](https://www.anthropic.com/research/constitutional-ai-harmlessness-from-ai-feedback) 2022 original.
  Traduction anglaise: version originale
- [Anthropic — Collective Constitutional AI (2023)](https://www.anthropic.com/research/collective-constitutional-ai-aligning-a-language-model-with-public-input) expérience participative.
  Le mot grec traduit par " participation à l'expérience " signifie " participation à l'expérience ".
- [Anthropic — Responsible Scaling Policy v3.0](https://anthropic.com/responsible-scaling-policy/rsp-v3-0) où la Constitution est inscrite dans la pile RSP.
  Le texte de la Constitution est en place dans le RSP.
- [Anthropic — Measuring agent autonomy in practice](https://www.anthropic.com/research/measuring-agent-autonomy) Le rôle de la Constitution dans les déploiements à long terme.
  Le rôle de la Constitution dans le long terme.
