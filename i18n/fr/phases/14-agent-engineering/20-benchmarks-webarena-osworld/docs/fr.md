# Les critères de référence: WebArena et OSWorld

> WebArena teste la capacité d'agent Web sur quatre applications auto-hébergées. OSWorld teste la capacité d'agent de bureau sur Ubuntu, Windows, macOS. À la sortie (20232024) les deux ont montré un grand écart entre les meilleurs agents de classe et les humains.

**Type:** Learn | **类型:** 学习
**Languages:** Python (stdlib) | **语言:** Python (标准库)
**Prerequisites:** Phase 14 · 19 (SWE-bench, GAIA) | **前置知识:** 见原文
**Time:** ~60 minutes | **时间:** 见原文

## Objectifs d'apprentissage

- Décrivez les quatre applications auto-hébergées de WebArena et pourquoi l'évaluation basée sur l'exécution est importante.
- Expliquez pourquoi OSWorld utilise des captures d'écran réelles du système d'exploitation au lieu des API d'accessibilité.
- Nombre des deux modes de défaillance OSWorld principaux: la mise à terre de l'interface graphique et les connaissances opérationnelles.
- Résumez ce que les systèmes OSWorld-G et OSWorld-Human ajoutent au niveau de référence de base.

## Le problème , l' introduction du problème

Les agents généralistes peuvent appeler des outils. Pouvent-ils faire un navigateur à 20 clics pour effectuer une vérification de magasinage? Pouvent-ils configurer une boîte Linux en utilisant uniquement le clavier et la souris?

> Général Agent peut utiliser des outils. Mais peuvent-ils faire fonctionner un navigateur pour effectuer 20 clics pour effectuer le dépôt de billets ?


> **【中文解读】**WebArena et OSWorld  évaluer l'agent dans un environnement de calcul réel  évaluer les capacités d'exploitation  WebArena  tester les opérations du navigateur  WebArena  tester les opérations du navigateur   Commercials  Forum  CMS)  OSWorld  tester les opérations du système d'exploitation  Document management  Application                                                                                                                                                                                                                                                                                                                                                                                                                                            

> **{【拓展：WebArena (CMU, 2023) 创建了真实的 Web 环境（电商、论坛、GitLab），A...】}**WebArena (CMU, 2023) 创建了真实的 Web 环境(电商、论坛、GitLab),Agent 需要像人类一样浏览和操作。2026年 SOTA 约 35% taux de réussite,人类 约 80%。OSWorld (HKU, 2024) 提供真实的 Ubuntu/Windows/macOS 桌面环境,Agent 需要操作 GUI 完成任务。

>  **【前置】**建议先过:Phase 14·19 (SWE-bench/GAIA) 本节是其姐妹篇,专门评估"GUI 操作"能力;以及Phase 14·21 (Computer Use Agents) 本节是评估那些代理的"考试题"──理解GUI 操作和工具调用区别(GUI 是像素+点击,工具调用是API+JSON) 本节是关键──

## Le concept de base.

### Le projet de développement de l'entreprise est prévu pour la période de référence.

- 812 tâches à long horizon sur quatre applications Web auto-hébergées: un site de magasinage, un forum, un outil de développement comme GitLab, un CMS d'entreprise.
- Plus des utilitaires: carte, calculatrice, scratchpad.
- L'évaluation est basée sur l'exécution via des API de gymnase  a-t-elle été passée, le problème a-t-il été fermé, la page CMS a-t-elle été mise à jour?
- À la sortie: le meilleur agent GPT-4 atteint 14,41% de succès contre 78,24% chez l'homme.

Les cadres auto-hébergés sont importants  le critère de référence n'est pas flou parce que les applications cibles sont fixées et reproduisables.

> Le cadre de l'autogestion est important: la mise en œuvre de la base ne sera pas fixe et réalisable parce que l'application de l'objectif est instable.

>  **【类比】**WebArena et OSWorld sont différents de "simulaire de conduite" et "réelle de conduite": WebArena est une application de conduite de conduite de quatre pages Web fixes (applications électroniques, forums, etc.), environnement entièrement contrôlable, comme dans le cadre de la normalisation de l'école; OSWorld est une véritable version de l'Ubuntu/Windows/macOS, chaque version de l'UIS peut être différente, aussi peut-être une fenêtre, une carte, une annonce.**关键**: WebArena 测 est "Agent 能不能使用Web", OSWorld 测 est "Agent 能不能使用电脑"后者难一个量级──

> WebArena et OSWorld sont des systèmes d'évaluation de l'environnement d'utilisation de l'agent.

### Extensions

- **VisualWebArena** des tâches basées sur des données visuelles où le succès dépend de l'interprétation des images (captures d'écran comme observations de première classe).
- **TheAgentCompany**(Dec 2024)  ajoute le terminal + le codage; plus comme un véritable environnement de travail à distance.

### OSWorld (Xie et coll., NeurIPS 2024)

- 369 tâches réelles sur ordinateur sur Ubuntu, Windows, macOS.
- Contrôle de clavier et de souris de form libre d'applications réelles.
- 1920×1080 captures d'écran comme observation.
- Au moment de la sortie: meilleur modèle 12,24% contre humain 72,36%.

### Mode de défaillance primaire

1. **GUI grounding.**Le modèle a du mal à localiser les éléments de l'interface utilisateur de manière fiable en 1920×1080.
2. **Operational knowledge.**Quel menu a le réglage, quel raccourci clavier, quel panneau de préférence.

> ️ **【易错点】**Utilisez l'API DOM ou d'accessibilité pour la mise en service de l'OSWorld, puis rapportez "高分"**后果**:分数虚高且无意义 OSWorld 设计目的就是测**视觉 grounding**(image à la carte des éléments), avec l'API DOM, il est possible de contourner le défi central.**一行修复**: dans OSWorld 上 seulement utiliser l'agent de capture d'écran comme entrée, sinon pas " dans OSWorld 上评估"― Si vous voulez tester un agent basé sur DOM, veuillez utiliser WebArena ou Mind2Web―

### Suivi des mesures

- **OSWorld-G** 564 échantillons de la suite de mise à terre + Jedi formation ensemble.
- **OSWorld-Human** des trajectoires d'action de l'or sélectionnées manuellement.

### Pourquoi cela importe ?

Claude utilisation de l'ordinateur, OpenAI CUA, Gemini 2.5 utilisation de l'ordinateur (leçon 21) tous entraînés sur des charges de travail façonnées par WebArena et OSWorld.

> Claude 计算机使用、OpenAI CUA、Gemini 2.5 计算机使用(第21 课) Tous les participants à la formation sur la charge de travail de la création de sites Web et OSWorld 基准是目标;生产模型是交付的答案──

> WebArena et OSWorld sont des systèmes d'évaluation de l'environnement d'utilisation de l'agent.

### Lorsque l'analyse comparative se trompe

- **Screenshot-only evals.**OSWorld est basé sur des captures d'écran; l'évaluation d'un agent qui utilise des API DOM ou d'accessibilité sur OSWorld manque le défi de mise à terre.
- **Ignoring trajectory length.**Le score de succès ne fait que rater les 1,4-2,7 fois l'inefficacité des étapes OSWorld-Human surfaces.
- **Stale self-hosted apps.**Les applications WebArena sont en version spécifique; la mise à jour sans récuration rompt la comparabilité.

> 🤔 **【困惑】**Q: Le WebArena 上 SOTA 才 35%,OSWorld 才 12%, ce n'est pas une explication que l'Agent d'utilisation informatique 现在不能用吗 A: 不能如此看;;基准测试的任务是"最难的那批"长程(20+步) 多模态、需要精确的基础;;**针对性优化**Le code Claude en ligne peut aussi être utilisé dans un environnement structuré comme celui-ci.**结论**Le test de base est " capacité de production supérieure ", " utilisation spéciale ", les deux sont interchangeables directement.

> **仅截图评估。**OSWorld est un défi de détection; l'Agent de l'évaluation de l'utilisation d'une API DOM ou sans obstacle dans OSWorld sera confronté à des défis de terrain.
> **忽略轨迹长度。**                                                                                                                                                                                                                                                              
> **过时的自托管应用。**L'application WebArena a fixé une version spécifique; ne pas re-planifier sur les mises à jour détruira la compatibilité.

## Construisez-le et mettez-le en œuvre.
```figure
ae-agent-human-gap
```

## Faites-le

`code/main.py`met en place un harnais de jouets avec agent web:

> `code/main.py`实现一个玩具 Web Agent 测试工具:

> WebArena et OSWorld sont des systèmes d'évaluation de l'environnement d'utilisation de l'agent.

- Une machine d'état "applications de magasinage" minimale: liste_articles, add_to_cart, paiement.
- Des trajectoires en or pour 3 tâches.
- Un agent avec un script qui tente chaque tâche.
- Évaluateur basé sur l'exécution (contrôle d'état) et métrique de l'efficacité de la trajectoire (étapes contre or).

- Je vais le faire.

```
python3 code/main.py
```

Résultats: taux de réussite par tâche et efficacité de la trajectoire, en suivant la méthodologie d'OSWorld-Human.

> 输出: pour chaque mission, le taux de réussite et l'efficacité de la trajectoire, reflètent le méthodologie OSWorld-Human.

> WebArena et OSWorld sont des systèmes d'évaluation de l'environnement d'utilisation de l'agent.

## Utilisez-le avec le cadre de réalisation

- **WebArena Verified**auto-hébergé sur un cluster interne pour une évaluation continue.
- **OSWorld**dans une flotte de machines virtuelles pour les agents de bureau.
- **Computer-use agents**(Léction 21) Claude, OpenAI CUA, Gémeaux sont tous formés à des tâches comme celle-ci.
- **Your own product flows** capturer des trajectoires d'or pour vos 20 principales tâches; exécuter des agents contre eux chaque semaine.

## Envoyez-le . Produit .

`outputs/skill-web-desktop-harness.md`construit un harnais d'agent web/desktop avec une évaluation et une métrique d'efficacité de trajectoire basées sur l'exécution.

> `outputs/skill-web-desktop-harness.md`Construire un outil de test d'agent Web/descendant, avec des indicateurs d'évaluation et d'efficacité de la trajectoire basés sur l'exécution.

> WebArena et OSWorld sont des systèmes d'évaluation de l'environnement d'utilisation de l'agent.

## Les exercices

1. Élargir le harnais de jouets avec une deuxième application (un forum).
  Le mot "exercer" est traduit par "exercer".
2. Ajouter des rapports d'efficacité par tâche.
  Le mot "exercer" est traduit par "exercer".
3. La méthode de l'or ne peut pas être utilisée.
  Le mot "exercer" est traduit par "exercer".
4. Comment sépareriez-vous les échecs de mise à terre des échecs de planification dans vos propres évaluations ?
  Le mot "exercer" est traduit par "exercer".
5. Qu'est-ce qui se passe quand vous mettez à jour une version de l'application enfoncée ?
  Le mot "exercer" est traduit par "exercer".

## Les termes clés

| Term | What people say | What it actually means |
|------|----------------|------------------------|---|
| WebArena | "Web agent benchmark" | 812 tasks across 4 self-hosted apps; gym-style evaluation |  |
| VisualWebArena | "Visual WebArena" | Visually grounded WebArena; screenshots are observations |  |
| OSWorld | "Desktop agent benchmark" | 369 tasks on real Ubuntu/Windows/macOS |  |
| GUI grounding | "Pixel-to-element mapping" | Model localizing UI elements in 1920x1080 |  |
| Operational knowledge | "OS know-how" | Which menu, which shortcut, which preference pane |  |
| OSWorld-G | "Grounding suite" | 564 grounding-only samples + training set |  |
| OSWorld-Human | "Gold trajectories" | Manual expert action sequences to measure efficiency |  |
| Trajectory efficiency | "Steps over gold" | Agent step count divided by human minimum |  |

## Encore une lecture

- [Zhou et al., WebArena (arXiv:2307.13854)](https://arxiv.org/abs/2307.13854) Un référentiel web de quatre applications
  Le mot "réfléchisseur" est traduit par "réfléchisseur".
- [Xie et al., OSWorld (arXiv:2404.07972)](https://arxiv.org/abs/2404.07972) référence de bureau cross-OS
  Le mot "réfléchisseur" est traduit par "réfléchisseur".
- [Anthropic, Introducing computer use](https://www.anthropic.com/news/3-5-models-and-computer-use) La capacité de Claude en forme de référence
  Le mot "réfléchisseur" est traduit par "réfléchisseur".
- [OpenAI, Computer-Using Agent](https://openai.com/index/computer-using-agent/) Numéros OSWorld et WebArena
  Le mot "réfléchisseur" est traduit par "réfléchisseur".
