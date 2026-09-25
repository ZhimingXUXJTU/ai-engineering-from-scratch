# Surveillance évolutive et généralisation faible à forte

> Burns et al. (OpenAI Superalignment, " Généralisation faible à forte ", 2023) a proposé un proxy pour le problème de la superalignement: affiner un modèle fort en utilisant des étiquettes produites par un modèle plus faible. Si le modèle fort généralise correctement à partir d'une supervision faible imparfaite, les méthodes d'alignement à l'échelle humaine actuelles peuvent s'étendre aux systèmes surhumains. La surveillance évolutive et le W2SG sont complémentaires. La surveillance évolutive (débat, modélisation récursive de la récompense, décomposition des tâches) augmente la capacité efficace du surveillant afin qu'il puisse suivre le modèle sous surveillance. Le W2SG assure que le modèle solide généralise correctement toute supervision imparfaite que le surveillant fournit. Le groupe W2SG (arXiv:2501.13124, janvier 2025) les combine.

> **【中文解读】**Ce chapitre présente le contrôle étendu possible de la faiblesse à la forte IA méthode d'évaluation de la sécurité. Burns  et d'autres  OpenAI  Superacord, 2023) propose un agent de la supercord: les étiquettes produites par des modèles faibles sont des modèles de contrôle étendues. Si le modèle fort est correctement généralisé dans la surveillance parfaite, les méthodes de contrôle de la taille humaine actuelle peuvent se développer à des systèmes superhumains.

> **【拓展：弱到强泛化 → 超级对齐路径】**PGR(Performance Gap Recovered) = (微调后-弱) /(上限-弱) ――PGR 为 1.0 signifie faible surveillance complètement comblé le déficit;PGR 为 0 signifie faible surveillance sans aide。Burns 等人 a constaté que PGR dans NLP、国际象棋题和奖励建模任务上一致为正的(约20%-80%),强模型利用预训先验"理解"的意图任务,超越了弱监督者的错误。

**Type:** Learn | **类型:** 学习
**Languages:** Python (stdlib, W2SG gap simulator) | **语言:** Python（标准库，W2SG 差距模拟器）
**Prerequisites:** Phase 18 · 01 (instruction-following), Phase 18 · 10 (AI Control), Phase 09 (RL foundations) | **前置知识:** Phase 18 · 01 (指令遵循), Phase 18 · 10 (AI 控制), Phase 09 (RL 基础)
**Time:** ~60 minutes | **时间:** ~60 分钟

>  **【前置】**Pour les étudiants, la formation est une formation de base.
>  **【类比】**W2SG = "小学生教中学生"──如果中学生能从小学老师那里正确学到,说明对齐方法可扩展到超人 AI──PGR指标(Performance Gap Recovered) = faible surveillance弥合差距比例──Burns 2023 测出PGR 约20-80%强模型能"理解"意图超越弱监督者的错误──
> 🤔 可扩展监督(debate/递归奖励建模) + W2SG 互补:前者提升监督者能力,后者确保强模型从不完美监督中泛化──

## Objectifs d'apprentissage

- Définir la surveillance évolutive et la généralisation faible à forte et expliquer comment elles sont complémentaires.

> 定义可扩展监督和弱到强泛化,并解释它们如何互补──

- Décrire la configuration expérimentale de Burns et coll. 2023: réglage fin de GPT-4 à l'aide d'étiquettes de GPT-2.

> 描述 Burns 等人 2023 年的实验设置:使用GPT-2 产生的标签微调GPT-4──

- Expliquer la mesure de l'écart de performance récupéré (PGR) et ce qu'elle mesure.

> 解释性能差距恢复 (PGR) indicateur et son contenu de mesure

- Indiquez les trois principaux mécanismes de surveillance évolutifs (débat, modélisation récursive de la récompense, décomposition des tâches) et une force de chacun.

> 列出三种主要可扩展监督机制 (voir tableau) 辩论,递归奖励建设模,任务分解) 及各自的优点──

## Le problème , l' introduction du problème

Chaque technique d'alignement jusqu'à présent dans la phase 18 suppose que le superviseur peut évaluer le comportement du modèle. Lorsque le modèle est surhumain, le superviseur est le maillon faible. La question de l'alignement supérieur: un superviseur plus faible peut-il produire de manière fiable un modèle plus fort et aligné?

> La phase 18 est la première à ce jour, et chaque type de technologie est supposée être capable d'évaluer le comportement du modèle.

Burns et al. réduisent cela à une configuration empirique opérationnelle: superviser fort avec faible, mesurer combien de la capacité du modèle fort survit à la supervision faible.

> Burns  et autres ont simplifié la mise en place de la pratique de l'opération: avec un faible contrôle, la capacité de mesurer un modèle fort a beaucoup de survivre sous un faible contrôle.

## Le concept de base.

> **【中文解读】**Burns  et autres expériences de mise en place: faible modèle GPT-2 级别,强模型 GPT-4 级别, objectif est强模型在金标签上上限──流程:获取弱模型零样本预测 → 在弱标签上微调强模型 → 测量强微调模型准确率──差距指标 PGR = (微调-弱) /(上限-弱),1.0 = 弱监督完全弥合差距,0 = 弱监督没有帮助──

### W2SG: la configuration de Burns et al.

- Modèle faible: classe GPT-2.
- Modèle fort: classe GPT-4.
- Objectif: un plafond GPT-4 solide pour la tâche.

Procédure:
1. Obtenez les prédictions zéro-shot du modèle faible sur une tâche.
2. Réglez le modèle fort sur des données faibles.
3. Mesurer la précision du modèle fort et bien ajusté.

> 流程:1. 获取弱模型在任务上的零样本预测――2. 在弱标签数据上的微调强模型――3. 测量强微调模型的准确率――

Les lignes de base: précision faible du modèle lui-même, plafond supervisé du modèle fort sur les étiquettes en or.

> 基线: faible modèle lui-même de précision, modèle fort sur le label d'or

Metrique de la faille: Faille de performance récupérée (PGR) = (finement réglée - faible) / (plafond - faible).

> 差距指标: performance difference recovery (PGR) = ((微调后 - 弱) / ((上限 - 弱) ・PGR 为表示弱监督完全弥合差距;PGR 为 0 表示弱监督没有帮助。

### Résultats empiriques de Burns et coll.

Dans les tâches de PNL, de puzzle d'échecs et de modélisation de récompenses, le PGR était toujours positif: le modèle fort se généralisait au-delà des erreurs du superviseur faible.

> Dans les tâches de construction de conception et de récompense de la PNL, le PGR s'est concentré sur la généralisation du modèle fort dépassant les erreurs des surveillants faibles.

Limitations Burns et al. note:
- Le modèle faible est aligné; un modèle vraiment surhumain pourrait être aligné par un humain, mais avec un écart de capacité beaucoup plus grand.

> La différence entre faible et fort est la capacité, et non la capacité.

- La généralisation du modèle fort peut être plus liée aux antécédents de tâches que à la récupération de l'intention de vérité de base.

> La généralisation du modèle fort peut être plus liée à l'expérience des tâches, que à la restauration de l'intention réelle.

- L'obtention de la connaissance latente du modèle fort est le vrai problème; la RGP mesure une opérationnalisation spécifique.

> Le potentiel de connaissance du modèle est le seul problème; la RPG mesure une opération spécifique.

> **【拓展：三种可扩展监督机制 → 辩论/递归奖励建模/任务分解】**辩论(Irving 等人 2018): deux U 实例争论相反立场,弱评判者决定──归归奖励建模(Leike 等人 2018):U 帮助人类训练 U+1 的奖励模型,监督者的有效能力随模型增长──任务分解(Christiano 等人 2018):将硬任务分解成人类可检查的子任务,归归执行──每种机制都假设关于任务结构或中间组件对齐的某些东西──

### Surveillance évolutive: trois mécanismes

- **Debate (Irving et al. 2018).**Deux exemples de U débattent des côtés opposés; le juge faible décide. L'hypothèse: trouver une vraie réponse convaincante est plus facile que de trouver une fausse réponse convaincante.

> **辩论（Irving 等人 2018）。**Deux exemples de U débattent contre position; faibles juges décident. Supposons: trouver une vraie réponse convaincante est plus facile que de trouver une fausse réponse convaincante. Les dernières études de 2024-2025 montrent que le débat a parfois de l'efficacité, parfois de l'inefficacité, dépend de la structure de la tâche.

- **Recursive Reward Modeling (Leike et al. 2018).**U aide l'humain à former le modèle de récompense pour U+1.

> **递归奖励建模（Leike 等人 2018）。**U 帮助人类训练 U+1 的奖励模型──监督者的有效能力随模型增长──

- **Task Decomposition (Christiano, Shlegeris, Amodei 2018).**Décomposer une tâche difficile en sous-tâches que l'homme peut vérifier, récursivement.

> **任务分解（Christiano, Shlegeris, Amodei 2018）。**La résolution des tâches difficiles est décomposée en sous-tasques de contrôle humain.

Chaque mécanisme suppose quelque chose sur la structure de la tâche ou l'alignement des composants intermédiaires.

> Chaque mécanisme suppose quelque chose qui concerne la structure de la tâche ou le composant intermédiaire.

### Pourquoi la surveillance évolutive et le W2SG sont complémentaires

Une surveillance à grande échelle améliore la qualité du signal efficace du surveillant.
Le W2SG comble le fossé de tout signal imparfait que le surveillant peut fournir.

> 可扩展监督提高监督人有效信号质量──弱到强泛化── de la capacité du contrôleur à fournir des signaux imparfaits.

Lang et coll.  Débat aide la généralisation faible à forte (arXiv:2501.13124) les combine: un protocole de débat fournit de meilleures étiquettes faibles, et le modèle fort est formé sur ces étiquettes.

> Lang et d'autres contribuent à la renforcement de la force de l'étiquette.

> **【中文解读】**组织戏剧:OpenAI's super super对齐团队 en 2024 Jan Leike 离职加入人类 后解散――但研究议程(可扩展监督、弱到强泛化、自动化对齐研究) 在人类 和学术实验室继续MATS(Léction 28)、Redwood(Léction 10)、Apollo(Léction 8)、METR(Léction 28)。 L'organisation a changé, les problèmes de recherche ne sont pas différents。

### Le drame organisationnel

L'équipe Superalignment d'OpenAI a été dissoute en mai 2024 après le départ de Jan Leike à Anthropic. L'agenda (surveillance scalable, W2SG, recherche d'alignement automatisée) a continué à Anthropic et dans les laboratoires académiques  MATS (leçon 28), Redwood (leçon 10), Apollo (leçon 8), METR (leçon 28). La structure organisationnelle a changé; les questions de recherche ne l'ont pas fait.

> Le groupe de super-équipe de l'OpenAI a rejoint Anthropic en 2024 en mai Jan Leike 离职加入 Anthropic 后解散──研究议程(可扩展监督、弱到强泛化、自动化对齐研究) a poursuivi à l'intérieur de l'Anthropic 和学术实验室MATS、Redwood、Apollo、METR── la structure de l'organisation a changé; les problèmes de recherche ne sont pas changés──

### Là où cela s'inscrit dans la phase 18

Les leçons 6-10 décrivent la menace et le paradigme défensif sous l'hypothèse que U est peu fiable. La leçon 11 est le paradigme offensif: rendre le surveillant assez fort pour vérifier l'alignement de U. Les leçons 12-16 se tournent ensuite vers l'outillage pratique de l'évaluation adversitaire.

> Les leçons 6-10 Décrivent les menaces et les hypothèses de défense de l'U. Incrédulité. Les leçons 11 sont des leçons positives: rendre le surveillant assez fort pour vérifier la présence de l'U. Les leçons 12-16 se tournent vers des outils pratiques d'évaluation de l'U.

> **【拓展：辩论帮助弱到强泛化 → 2025 组合】**Lang 等人(arXiv:2501.13124, janvier 2025) va étendre la surveillance et la faiblesse à la forte généralisation combinée: le protocole de débat fournit de meilleurs étiquettes faibles, un modèle fort est formé sur ces étiquettes.

## Utilisez-le avec le cadre de réalisation
```figure
scalable-oversight
```

## Utilisez-le

`code/main.py`Simulation de l'étiquetage W2SG sur une tâche synthétique. un étiquetage faible a une précision de 70% avec des erreurs structurées; un modèle fort a un plafond de 95% sur des étiquettes en or. Vous étiquettez le modèle fort sur des étiquettes faibles, mesurez le PGR et comparez avec le modèle fort sur l'or et le modèle faible seul.

> `code/main.py`Dans les tâches de synthèse, il est possible de simuler W2SG 微调── faible marqueur de 70% 带有结构性错误;强模型在金标上上限为95%──你在弱标上微调强模型,测量PGR,并与强模型在金标和弱模型单独结果比较──

## Envoyez-le . Produit .

Cette leçon produit `outputs/skill-w2sg-pgr.md`. En raison d'une description de la configuration de la surveillance, elle identifie le responsable de surveillance faible, le modèle fort, la qualité de la surveillance et compute (ou demande) la RGP. Elle marque si l'affirmation est "faible peut superviser fort" ou "faible + mécanisme de surveillance peut superviser fort".

> 本课产 出 `outputs/skill-w2sg-pgr.md` donner des instructions de surveillance définition description, identifier les faibles surveillants, modèle fort, qualité de surveillance,并计算, ou requête)

## Les exercices

1. On court .`code/main.py`. Rapporte le PGR pour la faiblesse de précision = 0,60, 0,70, 0,80. Expliquez la forme de la courbe du PGR.

2. Modifier l'étiquetateur faible pour qu'il ait une erreur structurée (par exemple, toujours incorrecte sur une classe d'entrée spécifique).

3. Lisez Burns et coll. 2023 Section 4.3 (Tâches de PNL). Reproduire l'intuition de "perte de confiance auxiliaire": lorsque le modèle fort est plus confiant que les étiquettes faibles, qui gagne?

4. Conceptez un protocole de surveillance évolutif qui combine le débat et la décomposition des tâches pour une tâche de génie logiciel. Nommez un mode d'échec de chaque composant et expliquez comment la combinaison s'adresse ou ne s'y parvient pas.

5. Expliquez ce qui pourrait falsifier l'affirmation selon laquelle "la généralisation faible à forte est une voie viable vers la suralignement".

## Les termes clés

| Term | What people say | What it actually means |
|------|-----------------|------------------------|
| Scalable oversight | "making the overseer stronger" | Mechanisms that increase an overseer's ability to evaluate a more-capable model |
| W2SG | "weak supervises strong" | Fine-tuning a strong model on weak labels and measuring the capability recovered |
| PGR | "performance gap recovered" | (fine-tuned - weak) / (ceiling - weak); 1.0 = fully closed, 0 = no help |
| Debate | "two U instances argue" | Scalable oversight mechanism where a weak judge picks between two U defenders |
| RRM | "recursive reward modeling" | U helps train the reward model for U+1; overseer capability tracks U |
| Task decomposition | "sub-tasks the human checks" | Break a hard task into sub-tasks the human can verify, recursively |
| Superalignment | "aligning superhuman AI" | The research agenda concerned with aligning models the human cannot directly evaluate |

## Encore une lecture

- [Burns et al. — Weak-to-Strong Generalization (OpenAI 2023)](https://openai.com/index/weak-to-strong-generalization/) le papier W2SG
- [Irving, Christiano, Amodei — AI safety via debate (arXiv:1805.00899)](https://arxiv.org/abs/1805.00899) le mécanisme de débat
- [Leike et al. — Scalable agent alignment via reward modeling (arXiv:1811.07871)](https://arxiv.org/abs/1811.07871) Modélisation récursive de la récompense
- [Khan et al. — Debating with More Persuasive LLMs Leads to More Truthful Answers (arXiv:2402.06782)](https://arxiv.org/abs/2402.06782) 2024 étude empirique du débat avec des débatteurs plus forts
- [Lang et al. — Debate Helps Weak-to-Strong Generalization (arXiv:2501.13124)](https://arxiv.org/abs/2501.13124) 2025 combinaison de débats + W2SG
