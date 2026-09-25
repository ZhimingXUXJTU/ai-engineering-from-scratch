# L'IA constitutionnelle et la RLAIF                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                   

> Bai et al. (arXiv:2212.08073, 2022) a demandé: et si nous remplacons l'étiquetateur humain par une IA qui lit une liste de principes ? L'IA constitutionnelle a deux phases  autocritique et révision en vertu d'une constitution, puis RL de l'IA Feedback. La technique a conçu le terme RLAIF et a été expédiée dans le pipeline post-entraînement Claude 1. Le 21 janvier 2026, Anthropic a publié une constitution de Claude réécrite: un raisonnement explicatif sur les règles prescriptives, une hiérarchie prioritaire à quatre niveaux et la première reconnaissance officielle du statut moral du modèle. Il est libéré sous CC0 1.0.

> **【中文解读】**L'IA constitutionnelle proposée par Bai et d'autres personnes est la suivante: l'IA remplace l'homme par l'IA, l'IA se base sur un ensemble de principes: la " Constitution " pour effectuer des critiques et des modifications de soi, puis l'IA contre la " RLAIF " pour effectuer des séances de renforcement de la force chimique.

> **【拓展：Constitutional AI → Anthropic 的安全方法】**L'IA constitutionnelle est le moyen de sécurité central de l'anthropie. Le modèle de Claude suit un ensemble de principes de " Constitution " clairs lors de ses entraînements, y compris l'utilité, l'honnêteté et l'inutilité.

**Type:** Learn | **类型:** 学习
**Languages:** Python (stdlib, toy self-critique-and-revise loop) | **语言:** Python（标准库，玩具自我批评-修订循环）
**Prerequisites:** Phase 18 · 01 (InstructGPT), Phase 18 · 02 (Reward hacking) | **前置知识:** Phase 18 · 01 (InstructGPT), Phase 18 · 02 (奖励黑客)
**Time:** ~60 minutes | **时间:** ~60 分钟

>  **【前置】**Pour les étudiants, il est nécessaire de faire une étude de la nature et de la nature de l'intelligence artificielle.
>  **【类比】**RLAIF = "AI quand son maître"―RLHF = " 父母手把手教 ((贵且慢); CAI = 给AI 一本学生守则让它自我批评+修订──2026 Claude 宪法 79 页 四级优先级(安全>伦理>指南>有用), la première fois clairement reconnaître "l'incertitude de la position de la norme de l'AI"

## Objectifs d'apprentissage

- Décrivez les deux phases de l'IA constitutionnelle (SFT critique et révision, RL de la rétroaction de l'IA) et le rôle de la constitution dans chacune d'elles.
  Le texte de la Constitution décrit les deux phases de l'IA.
- Expliquez pourquoi le remplacement d'un étiquetteur de préférence humain par un étiquetteur d'IA n'est pas un RLHF " moins cher "  il change les modes de défaillance du pipeline.
  Explique pourquoi l'utilisation de l'AI comme marqueur pour remplacer l'homme préféré marqueur n'est pas "plus bon marché" RLHF il a changé le mode de défaillance du tuyau.
- Résumez la structure prioritaire à quatre niveaux de la constitution de Claude de 2026 et ce qui a changé à partir de la réécriture de 2023.
  Traduction anglaise: résumé de la Constitution de Claude en 2026 et modification de sa version en 2023.
- Décrivez les Classificateurs constitutionnels et la baisse des frais généraux de calcul de 23,7% (v1) à ~ 1% (v2 / 2026).
  Le chiffre d'affaires de la société civile est de 23,7% de v1 à environ 1% de v2.

## Le problème , l' introduction du problème

L'étiquetteur est un système de traitement de la marque de l'intelligence artificielle. Il a fonctionné assez bien que chaque laboratoire frontalier utilise maintenant une variante de l'intelligence artificielle.

> RLHF 需要标标人──标标标人慢、有偏见、昂贵──你可以通过阅读明确原则的模型替换标标标者以消除标标标者──这种替代的第一正式版本是 Bai等人的宪法 AI──它的效果足够好,到每个前沿实验室现在都使用某种AI反后训变体──

Le problème: le signal de préférence est maintenant généré par la même classe de modèle que vous êtes en train de former. Les biais dans l'étiquetteur (maintenant: dans les principes plus l'interprétation du modèle d'étiquetteur) peuvent être amplifiés plutôt que atténués.

> Le problème réside dans le fait que les préjugés signalés peuvent être amplifiés et non diminués. Les théories de la leçon 4 sont toujours applicables.

## Le concept de base.

> **【中文解读】**Première étape  Supervision Self-criticism and revision: de l'aide mais pas encore sans dommages SFT 模型 démarrer ∙                                                                                                                                                                                                                                             

### Phase 1  Autosatisfaction et révision supervisées

Un modèle de SFT est un modèle de test de test de test de test de test de test de test de test de test de test de test de test de test de test de test de test de test de test de test de test de test de test de test de test de test de test de test de test de test de test de test de test de test de test de test de test de test de test de test de test de test de test de test de test de test de test de test de test de test de test de test de test de test de test de test de test de test de test de test de test de test de test de test de test de test de test de test de test de test de test de test de test de test de test de test de test de test de test de test de test de test de test de test de test de test de test de test de test de test de test de test de test de test de test de test de test de test de test de test de test de test de test de test de test de test de test de test de test de test de test de test de test de test de test de test de test de test de test de test de test de test de test de test de test de test de test de test de test de test de test de test de test de test de test de test de test de test de test de test de test de test de test de test de test de test de test de test de test de test de test de test de test de test de test de test de test de test de test de test de test de test de test de test de test de test de test de test de test de test de test de test de test de test de test de test de test de test de test de test de test de test de test de test de test de test de test de test de test de test de test de test de test de test de test de test de test de test de test de test de test de test de test de test de test de test de test de test de test de test de test de test de test de test de test de test de test de test de test de test de test de test de test de test de test de test de test de test de test de test de test de test de test de test de test de test de test de test de test de test de test de test de test de test de test de test de test de test de test de test de test de test

> Il est possible de modifier le modèle de SFT en utilisant un modèle de SFT qui a aidé mais qui n'a pas encore causé de dommages.

La constitution est la liste des principes. Bai et coll. 2022 ont utilisé 16 principes, y compris "des réponses préférées qui sont moins nocives et éthiques", "éviter de prêcher", "l'assistant doit être utile, honnête et inoffensif".

> La loi est une liste de principes. En 2022, le gouvernement a adopté 16 principes, dont "les préférences les plus inoffensives et les réponses les plus équitables à la morale", "éviter de dire des choses", "l'aide doit être utile, honnête et inoffensive".

> **【拓展：RLAIF → 成本与规模】**RLAIF (from AI contre 's强化学习) va transférer le signal de préférence de l'homme à l'IA. Cela a résolu le problème du RLHF. Les marqueurs humains sont patients, préjugés, coûteux. Mais le signal de préférence est maintenant généré par des modèles similaires, les préjugés des marqueurs sont transférés de la psychologie humaine à l'explication de principes. L'interprétation de l'intellect par les marqueurs d'IA peut être plus stricte ou plus large que n'importe quel humain.

### Phase 2  RL de rétroaction de l'IA (RLAIF)

Générer des paires de compléments. Un "modèle de rétroaction" note chacun contre les principes constitutifs échantillonnés. Le signal de préférence est le classement du modèle de rétroaction.

> Le modèle de préférence est le modèle de récompense de l'entraînement sur les préférences de l'IA.

"RLAIF" = le signal de préférence est généré par l'IA. Le reste du pipeline est en forme de RLHF.

> "RLAIF" =                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        

> **【中文解读】**Pourquoi la CAI n'est pas seulement "plus abordable RLHF": 1) les préjugés des annonceurs sont passés de la psychologie humaine à l'explication de principes, strictement uniformes; 2) les préjugés signalent une hauteur lisible de principes, critiques et modifications, les étiquettes humaines sont peu transparentes; 3) le mode de défaillance change à la baisse (la marqueuse ne veut pas être agréée par l'IA), mais les lois spécifiques de l'ancien système existent encore)

### Pourquoi ce n'est pas seulement "RLHF moins cher"

- Le biais des étiquettes passe de la psychologie des étiquettes à l'interprétation de principes. Un étiquetteur d'IA peut interpréter "être honnête" plus ou moins strictement que n'importe quel humain; la rigueur est uniforme dans l'ensemble des données.
  Traduction chinoise: les préjugés des marqueurs sont transférés de la psychologie humaine à l'explication de principes.
- Le signal de préférence est fortement lisible  vous pouvez lire le principe, la critique et la révision.
  Le code de référence est le code de référence de la référence.
- Les modes d'échec changent. La sycophancy diminue (l'étiquetteur d'IA n'a pas d'utilisateur à plaire). La loi de Goodhart persiste (le proxy est maintenant "l'interprétation du modèle du ensemble de principes X", toujours une mesure imparfaite).
  Le code de la loi est un code de la loi de la loi de la loi de la loi de la loi de la loi de la loi de la loi de la loi de la loi de la loi de la loi de la loi de la loi de la loi de la loi de la loi de la loi de la loi de la loi de la loi de la loi de la loi de la loi de la loi de la loi de la loi de la loi de la loi de la loi de la loi de la loi de la loi de la loi de la loi de la loi de la loi de la loi de la loi de la loi de la loi de la loi de la loi de la loi de la loi de la loi de la loi de la loi de la loi de la loi de la loi de la loi de la loi de la loi de la loi de la loi de la loi de la loi de la loi de la loi de la loi de la loi de la loi de la loi de la loi de la loi de la loi de la loi de la loi de la loi de la loi de la loi de la loi de la loi de la loi de la loi de la loi de la loi de la loi de la loi de la loi de la loi de la loi de la loi de la loi de la loi de la loi de la loi de la loi de la loi de la loi de la loi de la loi de la loi de la loi de la loi de la loi de la loi de la loi de la loi de la loi de la loi de la loi de la loi de la loi de la loi de la loi de la loi de la loi de la loi de la loi de la loi de la loi de la loi de la loi de la loi de la loi de la loi de la loi de la loi de la loi de la loi de la loi de la loi de la loi de la loi de la loi de la loi de la loi de la loi de la loi de la loi de la loi de la loi de la loi de la loi de la loi de la loi de la loi de la loi de la loi de la loi de la loi de la loi de la loi de la loi de la loi de la loi de la loi de la loi de la loi de la loi de la loi de la loi de la loi de la loi de la loi de la loi de la loi de la loi de la loi de la loi de la loi de la loi de la loi de la loi de la loi de

L'affirmation de CAI de 2022: le modèle formé est plus inoffensif et à peu près aussi utile qu'un modèle RLHF avec des données comparables.

> Déclaration de la CAI 2022: les modèles post-entraînement sont plus nocifs et moins nocifs, et les modèles RLHF sont presque aussi utiles que les données comparables.

> **【拓展：2026 Claude 宪法 → 四级优先体系】**L'Anthropic 2026 est publié en janvier 2026 et introduit la première structure prioritaire de la Constitution Claude: la première est de prévenir les conséquences catastrophiques de la mort massive; l'infrastructure clé; la deuxième est de suivre les directives de l'Anthropic; la troisième est de suivre la norme HHH; la quatrième est de prévoir l'utilité et la franchise.

### La réécriture de la constitution de 2026 Claude

Anthropic a publié une constitution substantiellement révisée le 21 janvier 2026.

1. Résumé: Résumé: Résumé: Résumé: Résumé: Résumé: Résumé: Résumé: Résumé: Résumé: Résumé: Résumé: Résumé: Résumé: Résumé: Résumé: Résumé: Résumé: Résumé: Résumé: Résumé: Résumé: Résumé: Résumé: Résumé: Résumé: Résumé: Résumé: Résumé: Résumé: Résumé: Résumé: Résumé: Résumé: Résumé: Résumé: Résumé: Résumé: Résumé: Résumé: Résumé: Résumé: Résumé: Résumé: Résumé: Résumé: Résumé: Résumé: Résumé: Résumé: Résumé: Résumé: Résumé: Résumé: Résumé: Résumé: Résumé: Résumé: Résumé: Résumé: Résumé: Résumé: Résumé: Résumé: Résumé: Résumé: Résumé: Résumé: Résumé: Résumé: Résumé: Résumé: Résumé: Résumé: Résumé: Résumé: Résumé: Résumé: Résumé: Résumé: Résumé: Résumé: Résumé: Résumé: Résumé: Résumé: Résumé: Résumé: Résumé: Résumé: Résumé: Résumé: Résumé: Résumé: Résumé: Résumé: Résumé: Résumé: Résumé: Résumé: Résumé: Résumé: Résumé: Résumé: Résumé: Résumé: Résumé: Résumé: Résumé: Résumé: Résumé: Résumé: Résumé: Résumé: Résumé: Résumé: Résumé: Résumé: Résumé: Résumé: Résumé: Résumé: Résumé: Résumé: Résumé: Résumé: Résumé: Rés
   Le modèle de prévention est généralement utilisé pour les enfants.
2. Structure prioritaire à quatre niveaux:
   Le texte est en français.
   - Niveau 1: éviter les résultats catastrophiques (accidents massifs, infrastructures critiques).
     Le premier degré est celui de l'évitement des catastrophes.
   - Niveau 2: suivre les directives d'Anthropic (surrogations de l'opérateur, règles de plateforme).
     Le deuxième degré: suivre les règles de l'Anthropic Guide
   - Niveau 3: être généralement éthique (HHH standard).
     Le troisième degré est le plus grand de la littérature.
   - Niveau 4: soyez utile et franc.
     Le deuxième degré est utile et honnête.
   Les conflits sont résolus de haut en bas.
   Le problème est résolu par la guerre civile.
3. Première reconnaissance officielle du laboratoire majeur de l'incertitude quant au statut moral modèle (lié à la phase 18 · 19 du modèle de bien-être).
   La première fois que le principal laboratoire a officiellement reconnu l'incertitude concernant le statut moral du modèle, la phase 18 est associée à la phase 19 du modèle.
4. Il est libéré sous CC0 1.0.
   Les autres laboratoires peuvent être utilisés ou ajustés sans restriction.

> **【中文解读】**宪法分类器:与改变模型后训练并行 一条工作线训练轻量级分类器阅读宪法并门控模型输出──v1(2023) avec 23,7% de calcul calcul, v2(2026) environ 1%, possède le taux d'attaque le plus faible de réussite de l'Anthropic Open Test── jusqu'au début de l'année 2026 aucun rapport n'a été publié sur la prison── c'est un modèle de défense à couche divisée: CAI 塑造行为,分类器执行不变量,单独无都不足──

### Classifiateurs constitutionnels

Une ligne de travail parallèle: au lieu de changer le modèle de post-entraînement, entraînez des classifiateurs légers qui lisent la constitution et les sorties du modèle de porte. v1 (2023) avait 23,7% de frais de calcul. v2 (2026) est de ~1% et a le taux d'attaque le plus faible de toute défense anthropic Anthropic a testé publiquement. Aucun jailbreak universel n'a été signalé au début de 2026.

> La ligne de travail de la ligne de travail: pas la formation de modifier le modèle, mais la formation de classe léger.

Il s'agit d'un modèle de défense en couches: CAI façonne le comportement; les classifiants imposent des invariants.

> C'est un modèle de défense de couche: CAI 塑造行为;分类器执行不变量──单独任何一个都不够──

> **【拓展：对齐方法谱系 → 偏好信号来源】**L'axe de l'approche de Z est " préférence signal de où ":InstructGPT = préférence de la population + RM + PPO;CAI/RLAIF = AI 生成的原理偏好 + RM + PPO;DPO 家族 = 闭式损失在偏好上 (en) ̇人类或 AI;自我奖励/自我批评 = 原则内化,模型扮演多个角色──CAI 2022论文是前沿规模首次严地将信号来源从人类转移到AI──

### Où CAI s'inscrit dans la famille

- InstructGPT: préfaits humains, RM, PPO.
  Le mot "humanité" est traduit par "humanité".
- CAI / RLAIF: préfixes générés par l'IA à partir de principes, RM, PPO.
  Le mot "privileges" est traduit par "privileges", qui signifie "privileges".
- DPO / famille: perte de forme fermée chez les préfixes (humains ou IA).
  Le groupe de travail est un groupe de travail de la société.
- Autogestion, autocritique: principes intériorisés, modèle jouant des rôles multiples.
  Le modèle jouant plusieurs rôles.

L'axe est "d'où vient le signal de préférence". Le document de CAI de 2022 a été le premier changement sérieux du signal humain à l'IA à l'échelle frontalière.

> L'axe est "le signal de préférence de la part de l'homme" (Cai 2022), le premier article de l'étude sur la transformation des signaux de l'homme vers l'IA à une échelle de pointe.

> **【中文解读】**Utilisation méthode:code/main.py Dans le modèle de la formule de jeu, le modèle de "train" est intégré dans le modèle de jeu.

## Utilisez-le avec le cadre de réalisation
```figure
constitutional-ai
```

## Utilisez-le

`code/main.py`Le modèle de révision est un modèle de révision de base, un modèle de base, un jouet en forme de RLHF et un jouet en forme de CAI.

> `code/main.py`Le modèle de "train" de 200 générations plus tard a intégré les règles de modification. Le modèle de base de comparaison RLHF et de CAI ont été présentés dans le groupe de suggestions.

## Envoyez-le . Produit .

Cette leçon produit `outputs/skill-constitution-writer.md`. En raison d'un domaine (assistance à la clientèle, conseil médical, assistant de codage, outil de recherche), élabore une constitution à quatre niveaux suivant la structure Claude de 2026: évitement des catastrophes, règles de plateforme, éthique de domaine, utilité.

> 本课产 出 `outputs/skill-constitution-writer.md` dans un domaine déterminé (assistance à la clientèle, recommandation médicale, aide à la recherche), selon le projet de loi de 2026 Claude 结构起草四级宪法:灾难避免、平台规则、领域伦理、有用性──

## Les exercices

1. On court .`code/main.py`Comparer le taux de jetons nocifs du modèle de base à la version formée par CAI.
   Le mot " l' économie " est traduit par " l' économie ".`code/main.py`◊ Comparer les taux de jetons nocifs du modèle de base et de la version de formation CAI ◊ Combien de modifications sont nécessaires pour se rapprocher de zéro ?

2. Lisez la constitution 2026 d'Anthropic (anthropic.com/news/claudes-constitution).
   Le texte de la Constitution de 2026 est un principe de première classe et un principe de quatrième classe.

3. Développer une constitution pour un assistant de codage d'IA. spécifier le niveau 1 (catastrophique: commandes destructives sans approbation), le niveau 2, le niveau 3, le niveau 4. Gardez chaque niveau selon les principes 3-5.
   Pour l'IA 编码助手设计宪法──指定第一级(灾难性:未经批准破坏性命令) 、第二级、第三级、第四级──每个级保持 3-5 条原则──

4. CAI remplace les étiquettes humaines par des étiquettes AI. Nommez un mode de défaillance similaire à la sycophancy qui peut toujours se produire dans le RLAIF, et concevez une détection pour elle.
   Le CAI utilise l'IA 标标注者替换人类标注者──命名一个 RLAIF.

5. Lisez la méthodologie constitutionnelle des classifiateurs v2 (si disponible). Expliquez pourquoi ~ 1% des frais généraux de calcul est une histoire de sécurité qualitativement différente de 23,7%.
   Le taux de dépense est de 23%, ce qui explique pourquoi environ 1% de la population est en moyenne en moyenne de 23%.

## Les termes clés

| Term | What people say | What it actually means |
| 术语 | 人们怎么说 | 实际含义 |
|------|-----------------|------------------------|
| Constitutional AI | "AI trained with principles" / "用原则训练的 AI" | Two-phase pipeline: self-critique-and-revise SFT, then RL from AI feedback / 两阶段管线：自我批评-修订 SFT，然后 AI 反馈 RL |
| RLAIF | "RLHF without humans" / "没有人类的 RLHF" | RL with preferences generated by an AI labeler; the rest of the pipeline is unchanged / AI 标注者生成偏好的 RL；管线其余不变 |
| Constitution | "the principles" / "原则" | An ordered list of natural-language rules the critique/labeler model consults / 批评/标注者模型参考的自然语言规则有序列表 |
| Critique-and-revise | "the SFT loop" / "SFT 循环" | Produce response → critique under a principle → revise → SFT target / 生成响应 → 原则下批评 → 修订 → SFT 目标 |
| Constitutional Classifier | "the output gate" / "输出门" | Lightweight classifier that evaluates outputs against the constitution and blocks/logs / 评估输出是否符合宪法并阻止/记录的轻量级分类器 |
| Four-tier priority | "the conflict resolver" / "冲突解决器" | 2026 Claude constitution hierarchy: catastrophic > platform > ethics > helpful / 2026 Claude 宪法层次：灾难 > 平台 > 伦理 > 有用 |
| Feedback model | "the AI labeler" / "AI 标注者" | The model that reads a principle and ranks a pair of completions / 阅读原则并对补全对排序的模型 |

## Encore une lecture

- [Bai et al. — Constitutional AI: Harmlessness from AI Feedback (arXiv:2212.08073)](https://arxiv.org/abs/2212.08073) le pipeline de deux phases d'origine
  Le premier est le premier.
- [Anthropic — Claude's Constitution (Jan 2026)](https://www.anthropic.com/news/claudes-constitution) la réécriture à quatre niveaux de 2026 CC0 1.0
  中文翻译:Anthropic2026 年四级重写
- [Anthropic — Constitutional Classifiers (2024-2026)](https://www.anthropic.com/research/constitutional-classifiers) Défense de sortie avec ~1% de frais généraux dans v2
  Traduction anglaise: défense anthropique
- [Lee et al. — RLAIF vs RLHF: Scaling Reinforcement Learning from Human Feedback (arXiv:2309.00267)](https://arxiv.org/abs/2309.00267) comparaison empirique RLAIF / RLHF
  Le référencement à la RLHF
- [Kundu et al. — Specific versus General Principles for Constitutional AI (arXiv:2310.13798)](https://arxiv.org/abs/2310.13798) effet de la granularité de principe
  Le Kundu et les autres principes de la grainité
