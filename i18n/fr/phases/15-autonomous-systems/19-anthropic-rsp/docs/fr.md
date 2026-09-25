# Politique d'échelle responsable de l'anthropie v3.0

> RSP v3.0 est entré en vigueur le 24 février 2026, remplaçant la politique de 2023. L'atténuation à deux niveaux: ce que fera unilatéralement Anthropic par rapport à ce qui est formulé comme une recommandation à l'échelle de l'industrie (y compris les normes de sécurité RAND SL-4). Ajout de feuilles de route de sécurité frontalière et de rapports de risque en tant que documents permanents plutôt que de livrables ponctuels. Il abandonne l'engagement de la pause de 2023. Introduit le seuil de R&D-4 de l'IA: une fois franchi, Anthropic doit publier un cas affirmatif identifiant les risques et les atténuations de désalignement. Claude Opus 4.6 ne le traverse pas. Anthropic déclare dans l'annonce de la version 3.0 que " exclure avec confiance cela devient difficile. " SaferAI a classé le RSP 2023 à 2,2; ils ont rebaptisé la version 3.0 à 1,9, plaçant Anthropic dans la catégorie RSP " faible " aux côtés d'OpenAI et DeepMind. Les seuils qualitatifs ont remplacé les engagements quantitatifs de 2023; la suppression de la clause de pause est la régression la plus marquée.

> **【中文解读】**RSP v3.0 于 2026 年 2 月 24 日生效,替代 2023 政策。两层缓解:Anthropic 单边做什么 vs 行业范围建议(incluant RAND SL-4 安全标准) ・添加边界安全路线图和风险报告 作为常设文档而非一次性交付物品──删除 2023 暂停承诺──引入AI R&D-4 齐值:一旦跨越,Anthropic 必须发布识别不对风险和缓解的肯定案例──Claude Opus 4.6 未跨越它──Anthropic 在 v3.0 公告中声明"自信地排除这变得困难"──Safer 评价 2023 RSP 为 2.2;降级 v3.0 至 1.9,将将Anthropic 和 DeepMind 起一"进入AI 强风险和缓解的肯定案例──Claude Opus 4.6 未跨越它──Anthropic 在 v3.0 公告中声明"自信地排除这变得困难"──Safer 评价 2023 RSP 为 2.2;将降级 v3.0 和 DeepMind 起一"进入RSP 类别的弱点 关键 项; 暂停 项 项 暂停 项 项 项 项 项 项 项 项 项 项 项 项 项 项 项 项 项 项 项 项 项 项 项 项 项 项 项 项 项 项 项 项 项 项 项 项 项 项 项 项 项 项 项 项 项 项 项 项 项 项 项 项 项 项 项 项 项 项 项 项 项 项 项 项 项 项 项 项 项 项 项 项 项 项 项 项 项 项 项 项 项 项 项 项 项 项 项 项 项 项 项 项 项 项 项 项 项 项 项 项 项 项 项 项 项 项 项 项 项 项 项 

> **【拓展：v3.0 的核心改动】**Trois modifications clés: 1) ajouter un plan de sécurité de la première ligne, présenter un rapport de risque, présenter des mesures de sécurité, et non des mesures spécifiques, présenter un mécanisme de contrôle, un comité consultatif de sécurité et un contrôle indépendant.

**Type:** Learn | **类型:** 学习
**Languages:** Python (stdlib, RSP threshold decision engine) | **语言:** Python（标准库，RSP 阈值决策引擎）
**Prerequisites:** Phase 15 · 06 (AAR), Phase 15 · 07 (RSI) | **前置知识:** Phase 15 · 06（AAR），Phase 15 · 07（RSI）
**Time:** ~45 minutes | **时间:** ~45 分钟

>  **【前置】**Les résultats de la recherche ont été obtenus en 1er janvier 2015 et ont été publiés en 2e janvier 2015.
>  **【类比】**RSP = "AI 公司的安全宪法"──2023 版 = 严格(定量值+暂停承诺);v3.0 = 灵活(定性值+删除暂停)──SaferAI 评分 2.2 降至 1.9("弱"类别)──新增AI R&D-4 值 = Une fois que l'IA 能自动化AI 研发达到某水平, il faut forcer la divulgation
> 🤔 **【困惑】**Q: Pourquoi avoir supprimé le délai de mise en œuvre ? 商业压力──暂停 = 竞争对手超越你──OpenAI、Google 都没暂停,Anthropic 单方面暂停=自杀──修复:行业协调(RAND SL-4 标准) + 监管干预(EU AI Act) afin d'éviter les prisonniers en difficulté──

## Le problème , l' introduction du problème

Les laboratoires frontaliers publient des politiques d'échelle qui sont en partie des documents techniques, en partie des documents de gouvernance et en partie des signaux aux régulateurs.

> La politique d'expansion publiée par le premier côté du laboratoire est une partie du dossier technique, une partie du dossier administratif, une partie du dossier est un signal à l'autorité de surveillance.

RSP v3.0 est le document actuel de l'Anthropic. Lire attentivement n'est pas important parce que le respect de celui-ci est obligatoire (il n'est pas), mais parce que le cadre forme la façon dont un laboratoire conçoit le risque catastrophique et comment il communique les compromis au public.

> RSP v3.0 est un document anthropologique actuel. Il est important de lire ceci non pas parce que la norme est en vigueur, mais parce que le cadre de formation des laboratoires est un modèle de façon à concevoir les risques de catastrophe et à les transmettre au public.

La différence entre la version 3.0 et la version 2.0 est l'unité utile. Ce qui a été ajouté: cartes routières de sécurité frontalière, rapports de risques, le seuil de R&D-4 de l'IA. Ce qui a été supprimé: l'engagement de pause de 2023.

> Les différences entre la version 3.0 et la version 2.0 sont utiles.

Ce qui a été refait: un calendrier d'atténuation à deux niveaux divisé entre Anthropic-unilatérale et recommandation de l'industrie.

> Révision: répartition en deux niveaux de temps de réduction de la proposition de l'industrie et de l'Anthropologie. Externe Review.

> **【中文解读】**Le RSP, Politique de mise à l'échelle responsable de l'Anthropic) définit un cadre pour maintenir la sécurité dans la croissance de la capacité de l'IA.

## Le concept de base.

### Le calendrier de réduction à deux niveaux.

- **Anthropic unilateral actions**Les programmes de formation sont basés sur des objectifs spécifiques, des mesures de sécurité spécifiques, des portes de déploiement spécifiques.
  Le mot grec traduit par " le mot grec "**Anthropic 单边动作**Il est également possible de faire des tests en toute sécurité.
- **Industry-wide recommendations**Les normes de sécurité RAND SL-4 sont incluses. Ce ne sont pas des engagements de la part d'Anthropic; ce sont des politiques de défense.
  Le mot grec traduit par " le mot grec "**行业范围建议**Les mesures de protection des données sont les suivantes:

La structure à deux niveaux n'était pas dans v2. Cela signifie qu'un lecteur doit regarder dans quelle colonne chaque engagement vit. Une mesure de sécurité dans la colonne "récommandation à l'échelle de l'industrie" n'est pas la promesse d'Anthropic; c'est l'espoir d'Anthropic.

> Il n'y a pas de structure à deux niveaux dans v2. Cela signifie que le lecteur doit regarder chaque engagement dans lequel il y a. Les mesures de sécurité de l'industrie suggèrent que les engagements ne sont pas des engagements anthropologiques; ce sont des espoirs anthropologiques.

### Le seuil de R&D-4 de l'IA

C'est le niveau de capacité que RSP v3.0 nomme comme le prochain seuil important. Plus précisément: un modèle qui pourrait automatiser une fraction substantielle de la recherche sur l'IA à un coût compétitif. Une fois qu'Anthropic croit qu'un modèle le franchit, il doit publier un cas affirmatif identifiant les risques de désalignement et les atténuations avant de continuer à l'échelle.

> C'est le RSP v3.0 qui a été nommé comme un important niveau de capacité de valeur. Concrètement, l'automatisation des coûts de concurrence est une partie importante du modèle de recherche de l'IA.

Claude Opus 4.6 ne le franchit pas selon l'annonce de la version 3.0. " Il devient difficile de ne pas en parler avec certitude. " Cette phrase est importante; elle admet que le seuil est assez proche pour être une préoccupation vivante, pas une limite spéculative.

> Claude Opus 4.6 根据 v3.0 公告未跨越它──文档添加:"Confiance地排除 this became困难──" Cette phrase est importante; elle reconnaît que la valeur est assez proche de l'état actuel, pas de la limitation de la hypothèse──

Les études de l'alignement automatisé (Automated Alignment Research) et de l'auto-amélioration récursive (Lecture 7) sont directement liées à ce seuil.

> Le programme de recherche sur l'IA est un outil de recherche qui permet de réaliser des recherches sur l'IA et de développer des techniques de recherche.

### Carte de route de sécurité frontalière et rapport de risque

V3.0 élève deux types d'artefacts à des documents permanents:

> v3.0 va mettre à jour deux catégories de produits pour un fichier permanent:

- **Frontier Safety Roadmap**: document prospectif décrivant les travaux de sécurité planifiés, les attentes de capacité et la recherche sur l'atténuation.
  Le mot grec traduit par " le mot grec "**前沿安全路线图**Définition du projet de recherche et de recherche sur la sécurité, la capacité d'expérience et la capacité de lutte contre la maladie
- **Risk Report**: document rétrospectif sur des modèles spécifiques après la mise en vente, décrivant la capacité observée et le risque résiduel.
  Le mot grec traduit par " le mot grec "**风险报告**: publié après un modèle spécifique, décrit la capacité d'observation et le résidu des risques.

Les deux sont publiques. Les deux sont mises à jour à une cadence déclarée. L'utilité est que le lecteur peut suivre comment ce qu'Anthropic a dit qu'ils feraient dans une feuille de route se compare à ce qu'ils rapportent dans un rapport de risque.

> 两者公开──两者按声明节奏更新──效果: lecteur可追踪 Anthropic 在路线图中说会做与在风险报告中报告的如何对比──

### La clause de pause est supprimée.

Le RSP 2023 comprenait un engagement explicite de pause: si un modèle franchissait les seuils de capacité spécifiques, la formation se serait arrêtée jusqu'à ce que les atténuations soient en place. V3.0 remplace la pause explicite par une formulation plus douce (publier un cas affirmatif, procéder si les atténuations sont adéquates). SaferAI et d'autres analystes ont qualifié cela directement de la régression la plus forte du nouveau document.

> 2023 RSP 包含显式暂停承诺: si le modèle franchit une capacité spécifique 值, l'entraînement sera suspendu jusqu'à ce que le缓解就位──v3.0 用更软表述(发布肯定案例,如缓解充分则继续)

L'argument politique pour le changement: les seuils quantitatifs en 2023 se sont avérés inaccessibles par les critères de référence de capacité de l'ère 2026 parce que les critères de référence eux-mêmes ont été rééchelonnés.

> 变更的政策论文:2023 时代能力基准 定量值 时代能力基准 2026 时代能力基准 时代能力基准 2026 时代能力基准 2026 时代能力基准 2026 时代能力基准 2026 时代能力基准 2026 时代能力基准 2026 时代能力基准 2026 时代能力基准 2026 时代能力基准 2026 时代能力基准 2026 时代能力基准 2026 时代能力基准 2026 时代能力基准 2026 时代能力基准 2026 时代能力基准 2026 时代能力基准 2026 时代能力基准 2026 时代能力基准 2026 时代能力基准 2026 时代能力基准 2026 时代能力基准 2026 时代能力基准 2026 时代能力基准 2026 时代能力 时代能力基准 2026 时代能力 时代能力 时代能力 时代能力 时代基准 2026 时代 时代 时代 时代 时代 时代 时代 时代 时代 时代 时代 时代 时代 时代 时代 时代 时代 时代 时代 时代 时代 时代 时代 时代 时代 时代 时代 时代 时代 时代 时代 时代 时代 时代 时代 时代 时代 时代 时代 时代 时代 时代 时代 时代 时代 时代 时代 时代 时代 时代 时代 时代 时代 时代 时代 时时时时时时时 时 时 时 时 时 时 时 时 时 时 时 时 时 时 时 时 时 时 时 时 时 时 时 时 时 时 时 时 时 时 时 时 时 时 时 时 时 时 时 时 时 时

### La dégradation de SaferAI

SaferAI est une organisation indépendante qui classe les documents de style RSP. Leur classement public: 2023 Anthropic RSP a obtenu 2.2 (d'une échelle où 4.0 est le meilleur RSP actuel et 1.0 est nominal).

> SaferAI est une organisation indépendante de RSP 式文档. Its public rating:2023 Antropic RSP 得 2.2(4.0 est le meilleur RSP actuel, 1.0 est le meilleur RSP nominale.

Les facteurs de dégradation par SAFERAI:

> Facteurs de réduction de la sécurité:

- Les seuils qualitatifs ont remplacé ceux quantitatifs.
  Le mot "définition" est traduit par "définition".
- L'engagement de pause a été retiré.
  Le gouvernement a décidé de suspendre la mise en place de l'accord.
- Les atténuations du seuil de R&D-4 de l'IA sont décrites comme "cas affirmatif" plutôt que comme des mesures spécifiques.
  La R&D-4 est une méthode de recherche de l'intelligence artificielle.
- Les mécanismes d'examen dépendent du groupe consultatif de sécurité d'Anthropic, avec une surveillance indépendante limitée.
  Le comité de révision de la loi de l'État de Hong Kong est un organisme de révision et de surveillance des données.

### Ce que cette leçon n'est pas, c'est ce que c'est.

Ce n'est pas une leçon de conformité. RSP v3.0 n'est pas une réglementation; rien ne force Anthropic à la suivre.

> Ceci n'est pas un programme conforme à la loi.

La leçon est de lire le document avec la spécificité et le scepticisme qu'il mérite. Les politiques d'échelle sont les principaux signaux publics émis par les laboratoires frontaliers sur les postures de risque catastrophique.

> Le programme est utilisé pour les spécificités et les spécificités qu'il doit résoudre. Lire les documents. La politique d'expansion est le principal signal public émis par les laboratoires de première ligne sur les postures de risque catastrophique.

## Utilisez-le avec le cadre de réalisation
```figure
a5-rsp-ladder
```

## Utilisez-le

`code/main.py`Il implique un petit moteur de décision qui reflète la forme de l'évaluation du seuil de RSP: étant donné un modèle candidat et un ensemble de mesures de capacité, retourner si le seuil de R&D-4 de l'IA est franchi, les sections requises de cas affirmatifs, et si le déploiement peut se poursuivre. C'est intentionnellement simple; l'objectif est de rendre la logique du document explicite.

> `code/main.py`实现镜像 RSP 值评估形状的小决策引擎:给定候选模型和一组能力测量,返回 AI R&D-4 值是否跨越、需要肯定案例节、部署是否可继续──它故意简单;点是让文档逻辑显式──

## Envoyez-le . Produit .

`outputs/skill-scaling-policy-review.md`révise une politique d'échelle (Anthropic, OpenAI, DeepMind ou interne) par rapport à la référence v3.0: structure à deux niveaux, seuils, engagements de pause, révision indépendante.

> `outputs/skill-scaling-policy-review.md`Pour les personnes âgées, les taux d'intérêt de l'entreprise sont les mêmes que pour les personnes âgées âgées âgées âgées âgées âgées âgées âgées âgées âgées âgées âgées âgées âgées âgées âgées âgées âgées âgées âgées âgées âgées âgées âgées âgées âgées âgées âgées âgées âgées âgées âgées âgées âgées âgées âgées âgées âgées âgées âgées âgées âgées âgées âgées âgées âgées âgées âgées âgées âgées âgées âgées âgées âgées âgées âgées âgées âgées âgées âgées âgées âgées âgées âgées âgées âgées âgées âgés âgés âgés âgés âgés âgés âgés âgés âgés âgés âgés âgés âgés âgés âgés âgés âgés âgés âgés âgés âgés âgés âgés âgés âgés âgés âgés âgés âgés âgés âgés âgés âgés âgés âgés âgés âgés âgés âgés âgés âgés âgés âgés âgés âgés âgés âgés âgés âgés âgés âgés âgés âgés âgés âgés âgés âgés âgés âgés âgés âgés âgés âgés âgés âgés âgés âgés âgés âgés âgés âgés âgés âgés âgés âgés âgés âgés âgés âgés âgés âgés âgés âgés âgés âgés âgés âgés âgés âgés âgés âgés âgés âgés âgés âgés â

## Les exercices

1. On court .`code/main.py`- fournir trois modèles synthétiques à différents niveaux de capacité. Confirmer que l'évaluateur des seuils se comporte comme prévu et produit le bon modèle de cas affirmatif.
   Le mot " l' économie " est traduit par " l' économie ".`code/main.py` dans trois niveaux de capacité différents de modèles synthétiques confirmer valeurs évaluateurs selon le comportement prévu et produire un modèle de cas d'assurance correct

2. Lisez RSP v3.0 en entier (32 pages). Identifiez chaque engagement qui se situe dans le niveau de "récommandation à l'échelle de l'industrie".
   Le projet de loi de la Commission européenne sur les droits de l'homme (CEDEAO) a été adopté par le Conseil européen de l'environnement (CEP) en décembre 2014.

3. Lisez la méthodologie de notation RSP de SaferAI. Reproduisez leur score de 1.9 pour la version 3.0 en appliquant leur rubrique au document.
   Le RSP de SaferAI est un système de référencement de la classe de référence.

4. L'engagement de pause pour 2023 a été supprimé. Proposer un engagement de remplacement qui préserve la crédibilité de la politique tout en reconnaissant le problème de rééchelle des benchmarks de 2026.
   En ce qui concerne la réforme du système de sécurité et de la sécurité sociale, le gouvernement a décidé de mettre en place un système de sécurité sociale qui permettrait de maintenir la sécurité des populations.

5. Comparez RSP v3.0 à OpenAI Preparedness Framework v2 (leçon 20). Choisissez un domaine où v3.0 est plus fort. Choisissez un domaine où le Framework de préparation est plus fort.
   Le programme de préparation de l'OpenAI est basé sur la technologie de préparation de l'OpenAI.

## Les termes clés

| Term | What people say | What it actually means |
|---|---|---|
| 术语 | 通俗说法 | 实际含义 |
| RSP | "Anthropic's scaling policy" | Responsible Scaling Policy; v3.0 effective Feb 24, 2026 |
| RSP | "Anthropic 的扩展政策" | Responsible Scaling Policy；v3.0 2026 年 2 月 24 日生效 |
| AI R&D-4 | "Research-automation threshold" | Capability to automate substantial AI research at competitive cost |
| AI R&D-4 | "研究自动化阈值" | 以竞争成本自动化相当部分 AI 研究的能力 |
| Affirmative case | "Safety justification" | Published argument that risks are identified and mitigations adequate |
| 肯定案例 | "安全证明" | 风险已识别缓解充分的已发布论证 |
| Frontier Safety Roadmap | "Forward plan" | Standing document on planned safety work and expected capabilities |
| 前沿安全路线图 | "前瞻计划" | 计划安全工作和预期能力的常设文档 |
| Risk Report | "Retrospective on a model" | Standing document on observed capability and residual risk after release |
| 风险报告 | "模型事后" | 发布后观察能力和剩余风险的常设文档 |
| Two-tier mitigation | "Unilateral vs industry" | Anthropic commitments vs industry recommendations, separated |
| 两层缓解 | "单边 vs 行业" | Anthropic 承诺 vs 行业建议，分开 |
| Pause commitment | "2023 clause" | Explicit promise to pause training; removed in v3.0 |
| 暂停承诺 | "2023 条款" | 暂停训练的显式承诺；v3.0 中移除 |
| SaferAI rating | "Independent RSP grade" | Third-party rubric; v3.0 scored 1.9 (v2 was 2.2) |
| SaferAI 评分 | "独立 RSP 评分" | 第三方量表；v3.0 得 1.9（v2 是 2.2） |

## Encore une lecture

- [Anthropic — Responsible Scaling Policy v3.0](https://anthropic.com/responsible-scaling-policy/rsp-v3-0) la politique complète de 32 pages.
  Le texte de la loi est en français.
- [Anthropic — RSP v3.0 announcement](https://www.anthropic.com/news/responsible-scaling-policy-v3) résumé des modifications de v2.
  Le texte est en français.
- [Anthropic — Frontier Safety Roadmap](https://www.anthropic.com/research/frontier-safety) document permanent lié à partir de RSP v3.0.
  Le référencement de la société est le plus connu de tous les pays.
- [Anthropic — Risk Report: Claude Opus 4.6](https://www.anthropic.com/research/risk-report-claude-opus-4-6) rétrospective du modèle frontalier actuel.
  Le modèle est un modèle de la vie.
- [Anthropic — Measuring agent autonomy in practice](https://www.anthropic.com/research/measuring-agent-autonomy) connecte l'IA R&D-4 à l'autonomie mesurée.
  Le développement de l'IA est un processus de recherche et développement.
