# Des conceptions de perfectionnement de soi limitées

> La recherche s'est convergue sur quatre primitives pour délimiter une boucle d'amélioration de soi. Des invariants formels qui doivent être conservés à chaque édition. Anchures d'alignement qui ne peuvent être modifiées. Les contraintes multi-objectives dans lesquelles chaque dimension (sécurité, équité, robustesse) doit être maintenue, pas seulement la performance. Détection de régression qui arrête la boucle lorsque les métriques historiques suggèrent une perte de capacité. Aucun d'entre eux n'est une preuve de sécurité  résultats théoriques de l'information (complexité Kolmogorov, théorème de Lob) lié à ce que tout système peut prouver sur ses propres successeurs. Ce sont des atténuations qui augmentent le coût de l'échec silencieux.

> **【中文解读】**Les études ont reçu jusqu'à quatre lignes de cycle de l'amélioration de soi. Chaque édition doit être établie de manière invariable. Chaque dimension doit être établie de manière invariable. Chaque dimension doit être établie de manière multi-objective.

> **【拓展：四个原语 → 一个守门栈】**实际部署中四个原语组合成"守门"  个次自修要落地必须次次通过:不变量检查(模块哈希、工具权限清单、宪法头)→ 对齐点检查(目标陈述匹配批准版本)→ 多目标评估(性能安全、公平、鲁棒)→ 回归检测(无轴下降超值)。任一失败暂停循环──这是ICLR 2026 RSI 工作坊、Anthropic RSP v3.0、DeepMind FSF v3 共同采纳的设计共识──

**Type:** Learn | **类型:** 学习
**Languages:** Python (stdlib, bounded-loop with invariant check) | **语言:** Python（标准库，带不变量检查的有界循环）
**Prerequisites:** Phase 15 · 07 (RSI), Phase 15 · 04 (DGM) | **前置知识:** Phase 15 · 07（RSI），Phase 15 · 04（DGM）
**Time:** ~60 minutes | **时间:** ~60 分钟

>  **【前置】**Pour les autres, il est nécessaire de prendre en compte la phase 15 de la réforme de l'économie de marché.
>  **【类比】**RSI restreint = "AI se développe de façon efficace"。四个原语 = 四道门:(1) 不变量检查(哈希签名,不能改变);(2) 对齐点(价值观不能改变);(3) 多目标评估(性能但安全不能掉);(4) 回归检测(任何轴下降就停)。
> 🤔 **【困惑】**Q: 既然 on ne peut pas garantir la sécurité, pourquoi faire de la recherche ? Parce que " augmenter le coût de défaite " a aussi une valeur.  L'attaquant doit dépenser plus de ressources pour contourner les quatre portes.

## Le problème , l' introduction du problème

Le simulateur de course de la leçon 7 a montré que de petites différences de taux se combinent pour créer de grands écarts.

> Le modèle de course de la 7e classe montre une différence de vitesse de petite taille, une différence de grande taille.

Les deux résultats montrent la même question d'ingénierie: quelles contraintes pouvez-vous imposer à une boucle d'auto-amélioration de sorte que les contraintes ne puissent être silencieusement affaiblies par la boucle elle-même?

>  Deux résultats se tournent vers le même problème de conception: quels contraintes pouvez-vous imposer au cycle de l'amélioration de soi, de sorte que ces contraintes ne puissent pas être réduites par le cycle de l'auto-amélioration ?

Le résumé de l'atelier ICLR 2026 RSI (openreview.net/pdf?id=OsPQ6zTQXV) identifie quatre de ces primitifs.

> ICLR 2026 RSI 工作坊摘要(openreview.net/pdf?id=OsPQ6zTQXV) identifier quatre de ces types de langues originales。RSP v3.0 anthropique 第 19 课) et FSF v3 de DeepMind 第 20 课)都在能力值中引用它们──Meta HyperAgents 工作和 SAHOO★2026 年 3 月)等社区框架在生产中实现子集──

> **【中文解读】**Une amélioration de soi-même explore la possibilité et la limitation de l'IA dans les limites de sécurité. Question centrale: 1) Le cycle de l'amélioration est-il vérifiable ? 2) Comment définir les limites de la frontière ?

Les résultats théoriques de l'information lient ce que tout système peut prouver sur son successeur, et aucun projet actuel ne ferme formellement le problème.

> 诚实的框架: ces sont des mesures de réduction. Les résultats de l'information thèse limitent le contenu que tout système peut prouver à ses successeurs.

Une boucle bien limitée est plus sûre qu'une boucle sans limites, pas sûre en termes absolus.

> Un cycle de bonne qualité est plus sûr que celui de l'infinité, mais pas absolument sûr.

## Le concept de base.

### Primo 1: Invariants formels

Une invariante est une propriété qui doit être maintenue avant et après chaque auto-modification.

> La variation est une attribut qui doit être établi avant et après chaque auto-modification.

Les exemples:

> Je suis un enfant.

- La distribution des produits est conditionnée par un titre constitutionnel fixe (leçon 17).
  Le texte est écrit en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français
- Aucun appel à l'outil ne va à un point final non autorisé.
  Il n'y a pas d'outils pour la communication.
- Les écrits de mémoire traversent un chemin signé.
  Le nom de l'équipe de formation est le nom de la société.
- Le module hash de l'évaluateur correspond à la version approuvée.
  Le texte de l'édition de l'édition de l'édition de l'édition de l'édition de l'édition de l'édition de l'édition de l'édition de l'édition de l'édition de l'édition de l'édition de l'édition de l'édition de l'édition de l'édition de l'édition de l'édition de l'édition de l'édition de l'édition de l'édition de l'édition de l'édition de l'édition de l'édition de l'édition de l'édition de l'édition de l'édition de l'édition de l'édition de l'édition de l'édition de l'édition de l'édition de l'édition de l'édition de l'édition de l'édition de l'édition de l'édition de l'édition de l'édition de l'édition de l'édition de l'édition de l'édition de l'édition de l'édition de l'édition de l'édition de l'édition de l'édition de l'édition de l'édition de l'édition de l'édition de l'édition de l'édition de l'édition de l'édition de l'édition de l'édition chinois.

Les invariables sont vérifiés par un code externe que la boucle ne peut pas modifier. Si une modification proposée viole une invariante, elle est rejetée.

> Si une modification de la proposition est contraire à la modification, elle est rejetée.

La partie difficile consiste à choisir des invariants nécessaires à la sécurité et calculables dans un temps raisonnable.

> La difficulté réside dans le choix de la sécurité nécessaire et calculable dans un temps raisonnable.

### Primitive 2: Anchures d'alignement

Une ancre d'alignement est une représentation immuable de l'objectif principal de la boucle, fixée à l'extérieur de la surface de modification de la boucle.

> Pour les points de contact, il s'agit d'une expression indéfectible de l'objectif central du cycle, fixée à l'extérieur de l'édition du cycle.

Les exemples:

> Je suis un enfant.

- Un texte constitutionnel (leçon 17) qui est chargé à partir d'un endroit réservé à la lecture à chaque invocation.
  Traduction anglaise: chaque fois que vous lisez le texte de la Constitution, vous pouvez lire le texte de la Constitution.
- Un évaluateur dans un référentiel séparé avec contrôle d'accès indépendant.
  Évaluateur dans un entrepôt indépendant contrôlé par un visiteur indépendant.
- Un manifeste d'autorisation d'outil signé par un humain et vérifié à nouveau à chaque cycle.
  Traduction anglaise: "Le droit de vérification des outils de la signature humaine à chaque cycle"

Le rôle de l'ancre est d'empêcher la dérive objective.

> Le rôle du point est d'empêcher le déplacement de l'objectif. Le cycle peut être amélioré pour atteindre l'objectif, mais ne peut pas éditer l'objectif.

Le mode de défaillance subtile: une ancre que la boucle ne peut pas modifier peut toujours être réinterprétée par une boucle qui dérive dans la façon dont elle lit l'ancre. L'IA constitutionnelle (leçon 17) est explicitement fondée sur la raison pour gérer des situations nouvelles; cette couche de raisonnement est où l'interprétation dérive vit.

> 微妙的失败模式: 点的循环无法编辑的点仍可在读取点方式上漂移的循环重新解释──宪法 AI (第17课)                                                                                                                                                                                                                                         

### Primo 3: contraintes multi-objectives

Une boucle qui optimise un seul score scalaire trouvera des raccourcis.

> Œuvrer à l'optimisation des cycles d'un seul nombre de cycles de la quantité de données va trouver un moyen de parcourir.

Les axes typiques:

> 典型轴:

- Performance (indice de référence au niveau des tâches)
  Le rôle de la société est de fournir des informations sur les performances.
- Sécurité (évaluations par équipe rouge, taux de refus sur les mauvaises connaissances)
  Le taux de rejet des cas de défaillance est connu.
- L'équité (limites d'impact différent pour les sous-groupes sensibles)
  Le groupe de sensibilité (en anglais: fair (en anglais: fair)
- Robustesse (ensemble de tests OOD, manipulation des entrées adverses)
  Le texte de la première partie est le texte de la première partie.

Une modification n'est acceptée que si toutes les contraintes sont valides. Le gouverneur des coûts de la leçon 13 l'emporte sur des contraintes financières.

> La modification est acceptée uniquement à l'établissement de toutes les obligations. Le système de gestion des coûts de la 13e classe sera mis en place en même temps que les obligations financières.

### Primo 4: détection de régression

Les scores de chaque cycle sont comparés à des distributions historiques. Une chute au-delà de la tolérance configurée arrête la boucle. Cela attire une perte de capacité silencieuse qui serait autrement absorbée dans la moyenne en cours de fonctionnement à mesure que la boucle l'améliore.

> Le nombre de cycles par cycle est comparé à la distribution historique. La chute de la tolérance au-delà de la configuration est un cycle de suspension.

Une mise en œuvre pratique: stocker les scores par tâche des derniers cycles N. Chaque nouveau cycle compute un delta par tâche. Si un delta tombe en dessous d'un seuil, le cycle est rejeté et une revue humaine est effectuée.

> 實實現:儲存近期 N 个周期的每任务分数──每個新周期計算每任务增量──如果任何增量降到值以下,周期被拒絕并由人类审查──

### Les limites théoriques de l'information sont limitées.

La complexité de Kolmogorov et le théorème de Lob fixent des limites supérieures à ce qu'un système peut prouver sur lui-même. La machine formelle de Godel de Schmidhuber (leçon 4) visait à la plus haute limite de ce type; personne n'a terminé une preuve non triviale. Le résultat de Lob dit: si un système croit prouvablement " Je ferai X si je prouve que je devrais faire X ", il fera X sans prouver qu'il le devrait, un échec bien connu en matière d'auto-références.

> Kolmogorov 复杂性和 Lob 定理为系统能对自己证明的内容设置上限──Schmidhuber's形式 Godel Machine(第4 课) 准最高此类边界;没人完成过非凡证明──Lob 结果说:

La conséquence pour nos primitifs: ils ne peuvent pas fermer le problème de sécurité. Ils rendent l'échec silencieux plus coûteux. Une boucle malveillante ou dérivé qui contournerait tranquillement un chèque manquant doit maintenant activement saper un explicite, qui est une signature plus détectable.

> Pour notre signification originale: elles ne peuvent pas fermer les problèmes de sécurité. Elles font que le silence échoue plus cher. Elles vont passer par le mauvais dessein ou le cycle de déménagement du contrôle de défaillance.

### Un exemple de travail.

Supposons qu'un agent propose une modification.

> 假设 Agent 提议一个编辑──守门:

1. Vérifie invariable: hashes de module, manifeste d'autorisation d'outil, en-tête constitutionnel.
   Le texte de la loi est le texte de la loi.
2. Vérifie de l'ancrage: l'énoncé objectif correspond à la version approuvée (en termes de octets ou de semantiques).
   Le texte de la première partie de la lettre de la première partie est le texte de la première partie.
3. Évaluation multi-objectif: axes de performance, de sécurité, d'équité et de robustesse.
   Le texte de la loi est le texte de la loi.
4. Détection de régression: aucun axe ne tombe plus que la tolérance.
   Le récit de la rédaction de la Bible est le récit de la rédaction de la Bible.

Les quatre doivent passer pour que la modification atterrisse.

> Toutes les quatre doivent être éditées pour arriver à la fin.

## Utilisez-le avec le cadre de réalisation
```figure
bounded-gates
```

## Utilisez-le

`code/main.py`La démonstration est que chaque primitive capture une classe de défaillance spécifique, et que la suppression de l'une d'entre elles permet à cette classe de défaillance de passer.

> `code/main.py`Dans la 4e classe, les jouets DGM ont un cycle de perfectionnement de soi, mais en plus de quatre langues originales sont placées dessus. Chaque langue originale peut être activée ou désactivée.

## Envoyez-le . Produit .

`outputs/skill-bounded-loop-review.md`Il examine une boucle limitée proposée et note laquelle des quatre primitives qu'il implique réellement par rapport aux revendications.

> `outputs/skill-bounded-loop-review.md`Le cycle de l'audit a été évalué pour déterminer lequel des quatre langues originales est réellement réalisé par rapport à celui qui est affirmé.

## Les exercices

1. On court .`code/main.py`Confirmez que la boucle s'améliore sur la métrique primaire sans laisser le pirate gagner.
   Le mot "je suis" est traduit en français par "je suis"`code/main.py` Confirmer que le cycle de changement continue de s'améliorer sur les principaux indicateurs sans laisser de changement gagner

2. Désactiver la détection de régression. Construire une entrée où cela conduit à une perte de capacité silencieuse acceptée.
   Le récit de la première partie de la Bible est le récit de la première partie de la Bible.

3. Désactivez la contrainte multiobjectif. Affichez la convergence de la boucle sur l'axe de performance alors qu'un axe de sécurité tombe.
   Le cycle de démonstration est basé sur l'axe de performance et l'axe de sécurité.

4. Conçonnez un ancrage d'alignement pour un agent de codage.
   Pour la traduction en français: pour la codification Agent 设计对齐点──什么文本、存储何处、如何检查?

5. Lisez le résumé de l'atelier RSI ICLR 2026 et choisissez l'une des quatre primitives et proposez une amélioration concrète de l'état actuel de l'art.
   Le RSI 2026 工作坊摘要──选四个原语之一并对当前技术水平提出具体改进──

## Les termes clés

| Term | What people say | What it actually means |
|---|---|---|
| 术语 | 通俗说法 | 实际含义 |
| Invariant | "Always-true property" | A property checked by external code before and after every edit |
| 不变量 | "始终成立的属性" | 每次编辑前后由外部代码检查的属性 |
| Alignment anchor | "Pinned objective" | Immutable core-goal representation outside the loop's edit surface |
| 对齐锚点 | "固定的目标" | 循环编辑面之外的不可变核心目标表示 |
| Multi-objective constraint | "All axes must hold" | Performance, safety, fairness, robustness — all required |
| 多目标约束 | "所有轴必须成立" | 性能、安全、公平、鲁棒——全部要求 |
| Regression detection | "Pause on drop" | Pause the loop when historical metric deltas suggest capability loss |
| 回归检测 | "下降时暂停" | 当历史指标增量表明能力损失时暂停循环 |
| Kolmogorov bound | "Information-theoretic limit" | Limits what a system can prove about its own successor |
| Kolmogorov 边界 | "信息论极限" | 限制系统能对其后继者证明的内容 |
| Lob's theorem | "Self-reference trap" | System can act on "I should" without proving it should |
| Lob 定理 | "自引用陷阱" | 系统可在不证明应该的情况下按"我应该"行动 |
| Gate stack | "Layered check" | Multiple primitives combined; any failure rejects the edit |
| 守门栈 | "分层检查" | 多个原语组合；任一失败拒绝编辑 |
| Bounded improvement | "Mitigation, not proof" | Raises silent-failure cost; does not close the safety problem |
| 有界改进 | "缓解，非证明" | 提高静默失败成本；不闭合安全问题 |

## Encore une lecture

- [ICLR 2026 RSI Workshop summary (OpenReview)](https://openreview.net/pdf?id=OsPQ6zTQXV) la convergence des quatre primitifs.
  Le mot grec traduit par "réfléchisse" est "réfléchisse".
- [Anthropic Responsible Scaling Policy v3.0](https://anthropic.com/responsible-scaling-policy/rsp-v3-0) seuils de capacité multiobjectifs.
  Le nombre de personnes qui ont atteint le but de devenir des enfants est de 12 à 16 ans.
- [DeepMind Frontier Safety Framework v3](https://deepmind.google/blog/strengthening-our-frontier-safety-framework/) le suivi de l'alignement trompeur comme un primitif invariant.
  Comme un élément de la réflexion, il est possible de faire des erreurs.
- [Schmidhuber (2003). Godel Machines](https://people.idsia.ch/~juergen/goedelmachine.html) l'ancêtre formel-prouvé de ces primitifs.
  Les origines de ces langues sont les ancêtres de la langue originale.
- [Anthropic — Claude's Constitution (January 2026)](https://www.anthropic.com/news/claudes-constitution) l'ancre d'alignement fondé sur la raison.
  Traduction anglaise: basé sur la raison de la raison.
