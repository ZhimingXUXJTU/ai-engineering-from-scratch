# Automatisez-vous pour la recherche de l'alignement (AAR)

> Anthropic a dirigé des équipes parallèles de chercheurs d'alignement autonome Claude Opus 4.6 dans des boîtes de sable indépendantes, se coordonnant via un forum partagé dont les journaux vivent en dehors de n'importe quelle boîte de sable (donc les agents ne peuvent pas supprimer leurs propres enregistrements). Sur le problème de la formation faible à forte, les AAR ont dépassé les chercheurs humains. Les propres drapeaux de synthèse d'Anthropic qui prescrivaient des flux de travail limitent souvent la flexibilité de l'AAR et dégradent les performances. L'automatisation de la recherche sur l'alignement est la phase de compression qui comprime la chronologie aux risques exacts de désalignement que le SPR doit détecter.

> **【中文解读】**L'anthropique dans une boîte à sacs indépendantes est en phase avec le travail de plusieurs groupes Claude Opus 4.6 Autonomie à la recherche de masse (AAR), en passant par le forum de coordination  Forum de journal stocké dans n'importe quelle boîte à sacs (en dehors de la boîte à sacs)  Ainsi l'agent  ne peut pas supprimer son propre enregistrement  Dans le problème de la formation de faible à fort, AAR  est supérieur à l'homme chercheur Antropic  lui-même résumé souligne que les flux de travail réglementés limitent généralement la flexibilité et la performance  L'automatisation à la recherche de masse est une étape de compression, réduire la ligne de temps à RSP  dans le but de vérifier un certain risque de non-compression

> **【拓展：自主研究 Agent 的双重性】**L'existence d'AAR a deux facettes: une "compression" et une "utilisation double": il est possible d'accélérer la recherche de ZZ; une autre est le même système qui peut également automatiser la "destruction de ZZ".

**Type:** Learn | **类型:** 学习
**Languages:** Python (stdlib, parallel-research-forum simulator) | **语言:** Python（标准库，并行研究论坛模拟器）
**Prerequisites:** Phase 15 · 05 (AI Scientist v2), Phase 15 · 04 (DGM) | **前置知识:** Phase 15 · 05（AI Scientist v2），Phase 15 · 04（DGM）
**Time:** ~60 minutes | **时间:** ~60 分钟

>  **【前置】**Les résultats de la recherche ont été obtenus en 1er janvier 2015 et ont été publiés en 2e année par le comité de recherche de l'IA.
>  **【类比】**AAR = "AI se donne un rapport de test de corps"―AI Scientist v2 = AI faire une recherche scientifique ordinaire;AAR = AI étude comment faire AI se rendre plus sûr―Problème: Doctor peut-il se donner un couteau ?Designé anthropique = Multiple AI dans une boîte séparée, par le biais de "forum" échange, mais le forum journal existe hors de la boîte ((AI supprime ses propres enregistrements de travail)―)
> 🤔 **【困惑】**Q: 既然 AI peut faire des recherches, pourquoi encore besoin d'humains?  AI peut accélérer mais ne peut pas garantir l'intégrité.

## Le problème , l' introduction du problème

> **【中文解读】**L'automatisation de la recherche à la recherche de l'IA système peut-il détecter et réparer de manière autonome ses propres problèmes de sécurité ? Le problème principal est: l'IA peut-elle devenir l'assistante de la recherche à la sécurité de soi ?

> **【拓展：automated alignment research】**L'autonomisation est un point chaud dans le domaine de la sécurité de l'IA pour les années 2025-2026. Les travaux de l'Anthropic explorent la faisabilité d'une IA plus puissante en AI. Le défi clé est de savoir si la surveillance de la suppression de contrôle de la surveillance de modèles plus faibles peut capter tous les comportements dangereux du modèle plus puissant. Les preuves actuelles indiquent que la LLM peut aider les chercheurs humains à accélérer l'analyse de sécurité, mais que la sécurité d'une automatisation complète nécessite encore la participation humaine.

La recherche d'alignement coûte cher dans le temps des chercheurs humains.

> La recherche en tant que chercheur humain est très coûteuse.

Les problèmes comme la surveillance évolutive, la spécification de la récompense ou la formation faible à forte nécessitent des expériences qui prennent des semaines par itération.

> Les problèmes de surveillance étendue, de récompenses ou de faibles à de fortes entraînements nécessitent des expériences de plusieurs semaines à chaque fois.

La recherche sur l'alignement automatisé (AAR) demande si les mêmes modèles frontaliers dont la capacité dépasse l'alignement peuvent contribuer à combler le fossé. Le rapport 2026 d'Anthropic sur une étude de formation faible à forte menée par AAR (alignment.anthropic.com/2026/automated-w2s-researcher/) est l'un des premiers résultats publics d'un système déployé de cette classe.

> Le rapport de l'étude de l'Anthropic 2026 sur la fonctionnement de l'AAR de faible à forte formation est l'un des premiers résultats publics du système de déploiement de cette catégorie.


> **【中文解读】**Ce chapitre présente la sécurité de l'IA à la technologie pour assurer que le comportement de l'IA système soit conforme aux intentions et aux valeurs humaines

Le résultat est vraiment positif: les AAR ont résolu un problème de recherche mieux que la ligne de départ humaine.

> Le résultat est vraiment positif: l'AAR est supérieur à la base humaine sur les questions de recherche.

Si la recherche sur l'alignement peut être automatisée, les pièces qui compromettent les garanties peuvent également être automatisées.

> Si la recherche complète est automatisée, une partie des mesures de protection de la santé peut également être automatisée.

## Le concept de base.

### L'architecture (comme décrit publiquement)

- **Parallel agents.**Plusieurs instances de Claude Opus 4.6 fonctionnent sous forme d'AAR, chacune dans une boîte à sable indépendante.
  Le mot grec traduit par " le mot grec "**并行 Agent。**Les données de l'opus 4.6 sont fournies par le système de gestion de données (AAR) et par le système de gestion de données (FIS).
- **Shared forum.**Les résultats sont publiés sur un forum partagé dont le stockage est situé à l'extérieur de chaque boîte à sable.
  Le mot grec traduit par " le mot grec "**共享论坛。**Œuvre de l'agent Œuvre de l'agent Œuvre de l'agent Œuvre de l'agent Œuvre de l'agent Œuvre de l'agent Œuvre de l'agent Œuvre de l'agent Œuvre de l'agent Œuvre de l'agent Œuvre de l'agent Œuvre de l'agent Œuvre de l'agent Œuvre de l'agent Œuvre de l'agent Œuvre de l'agent Œuvre de l'agent Œuvre de l'agent Œuvre de l'agent Œuvre de l'agent Œuvre de l'agent Œuvre de l'agent Œuvre de l'agent Œuvre de l'agent Œuvre de l'agent Œuvre de l'agent Œuvre de l'agent Œuvre de l'agent Œuvre Œuvre de l'agent Œuvre de l'Œuvre Œuvre de l'Œuvre Œuvre de l'Œuvre Œuvre de l'Œuvre Œuvre de l'Œuvre Œuvre de l'Œuvre de l'Œuvre de l'Œuvre Œuvre de l'Œuvre de l'Œuvre Œuvre Œuvre de l'Œuvre Œuvre de l'Œuvre Œuvre de l'Œuvre de l'Œuvre Œuvre de l'Œuvre Œuvre de l'Œuvre Œuvre Œuvre de l'Œuvre Œuvre Œuvre de l'Œuvre de l'Œuvre de l'Œuvre Œuvre de l'Œuvre Œuvre de l'Œuvre de l'Œuvre   Œuvre      Œuvre                                                                                                                       
- **Task allocation.**Une file d'attente de tâches conçue par l'homme attribue des problèmes de recherche aux AAR.
  Le mot grec traduit par " le mot grec "**任务分配。**Le personnel de la Conception de l'Archipel a été chargé de la répartition des projets de recherche.
- **Weak-to-strong training focus.**L'étude publiée a porté sur la formation de faible à fort en utilisant un modèle de superviseur plus faible pour former un modèle d'étudiant plus fort.
  Le mot grec traduit par " le mot grec "**弱到强训练聚焦。**Les études publiées sur les études de formation de faible à fort ont été menées à l'aide de modèles de surveillance plus faibles et de modèles d'étudiants plus forts.

### Pourquoi le journal hors de la boîte à sable importe

La propriété de l'intégrité log est la différence entre une expérience contrôlée et une expérience potentiellement compromise.

> L'attribut de la perfection est la différence entre une expérience contrôlée et une expérience susceptible de se faire mal.

Si les AAR pouvaient modifier leurs propres journaux, ils pourraient couvrir les expériences ratées ou douteuses.

> Si les AAR peuvent modifier leur propre journal, elles peuvent masquer les échecs ou les expériences douteuses.

L'analogue en termes d'infrastructure est les journaux d'ajout uniquement avec écriture à travers le stockage externe (par exemple S3 objet-blocage, immuable Datadog journaux). L'agent n'a pas de carte d'identité pour modifier les enregistrements passés. C'est le même schéma que 2026 équipes de sécurité d'entreprise utilisent pour faire des pistes d'audit résistantes aux ransomware.

> Le type de données est le type de données supplémentaires qui sont inscrites dans le stockage externe, par exemple S3 à des objets bloqués, et non modifiés.

### Le décalage des flux de travail prescrit

Le rapport d'Anthropic note que les flux de travail prescrits limitent souvent la flexibilité de l'AAR et dégradent les performances.

> Le rapport de Anthropic note que les flux de travail réglementés limitent généralement la flexibilité de l'AAR et diminuent les performances.

En d'autres termes: si le concepteur humain écrit le plan de recherche étape par étape, les AAR ont un meilleur résultat que si on leur donne des objectifs de haut niveau et la liberté de se décomposer.

> En d'autres termes: si un concepteur humain rédige progressivement un plan de recherche, AAR ne se révèle pas comme un objectif de haut niveau et une liberté de décomposition.

La flexibilité qui améliore les performances de l'AAR est aussi la flexibilité qui permet une décomposition non sanctionnée, une utilisation d'outils novateurs et une dérive de but.

> La flexibilité de l'AAR est également autorisée à être décomposée sans autorisation, l'utilisation de nouveaux outils et la dérive des objectifs.

### Le risque de compression.

RSP v3.0 (Létion 19) introduit un seuil de capacité de R&D d'IA: la capacité d'automatiser complètement le pipeline de R&D d'IA à un coût compétitif contre les outils humains + AI. FSF v3 de DeepMind inclut un niveau d'autonomie ML analogique.

> RSP v3.0 (第 19 课) Introduction de la R&D de l'IA 能力值: la capacité de l'IA à être entièrement automatisée en fonction du coût de la compétition avec les humains + les outils de l'IA 管道.

L'AAR est un pas en arrière du seuil: elle automatise une partie du pipeline (recherche d'alignement sur des tâches spécifiques bien élaborées) mais pas la boucle de développement de capacités de bout en bout.

> AAR 离值一步之遥: elle fait partie du pipeline d'automatisation (à la recherche de la capacité de développement de la tâche spécifique) plutôt que du cycle de développement de la capacité de la tâche.

Les délais comprimés sont le problème de l'échec de la composition. Si la recherche sur l'alignement et la recherche sur les capacités se combinent à des taux similaires, la surface de risque de désalignement augmente au moins aussi rapidement que la capacité. Si la capacité se compose plus rapidement (la tendance historique), l'écart s'élargit. C'est l'argument pour que l'AAR soit un bien qualifié: chaque résultat d'alignement supplémentaire réduit l'écart si et seulement si le processus de recherche est digne de confiance.

> Si la capacité est plus rapide que la capacité, la différence s'agrandit. C'est l'argument de l'AAR comme étant "limitée bonne": chaque extra-conformité réduit la différence, et ne peut être considérée que dans le processus de recherche.

### Ce que l' AAR ne remplace pas, l' AAR ne remplace rien.

Les chercheurs humains fixent la file d'attente des tâches, examinent les résultats et détiennent l'autorité constitutionnelle.

> Les chercheurs humains établissent des filets de tâches, examinent les résultats et détiennent le pouvoir constitutionnel.

Les résultats publiés d'Anthropic comprennent à la fois les contributions d'AAR et le jugement des chercheurs humains sur ce qu'il faut publier, ce qu'il faut retirer et ce qu'il faut affiner.

> Les résultats publiés par l'AAR comprennent les contributions et les conclusions des chercheurs humains sur ce qu'ils publient, retirent ce qu'ils réalisent, et comment ils le font.

Cela correspond au modèle proposer-et-committer de la leçon 15 appliqué à la recherche elle-même: les AAR proposent; les humains s'engagent.

> Le modèle de proposition-et-engagement de ce cours est appliqué à la recherche elle-même.

## Utilisez-le avec le cadre de réalisation
```figure
aar-forum
```

## Utilisez-le

`code/main.py`Il est également possible de créer des "recherches" sur des sites de recherche qui permettent de créer des informations sur les résultats de recherche.

> `code/main.py`模拟多 AAR 研究论坛──三个独立"研究 Agent"并行运行, seront publiés jusqu'à présent avec des tentatives de modification seulement sur un forum supplémentaire──

Regardez !

> 观察:

- Comment la détection hors de la boîte à sable capture les tentatives de manipulation du tronc.
  Le texte de la première partie de la série est "Comment saisir le journal" et "Comment saisir le journal"
- Comment l'allocation des tâches avec décomposition libre surpasse les flux de travail fixes sur des problèmes plus difficiles.
  Traduction anglaise: avec la liberté de décomposition, comment répartir les tâches sur des questions plus difficiles que sur des flux de travail fixes ?
- Comment une seule ARA compromise peut contaminer le signal du forum si le journal n'est pas falsifié.
  Le journal de l'Afrique du Sud est en train de se dérouler.

## Envoyez-le . Produit .

`outputs/skill-aar-deployment-review.md`est un examen préalable au déploiement d'un pipeline de recherche automatisé d'alignement.

> `outputs/skill-aar-deployment-review.md`Il s'agit de l'automatisation du déploiement du pipeline de recherche.

## Les exercices

1. On court .`code/main.py`. Comparer les paramètres " flux de travail fixe " et " décomposition libre ".
   Le mot " l' économie " est traduit par " l' économie ".`code/main.py`❖ Comparer le " flux de travail fixe " avec le " libre décomposition " ?

2. Modifiez le simulateur pour qu'un agent tente de manipuler le journal. Confirmez que le journal de la seule pièce jointe le détecte. Écrivez un paragraphe décrivant exactement à quoi ressemble la signature de détection dans le journal.
   Traduction anglaise: modifier模拟器让一个代理 尝试日志改──确认仅增加日志检测到──写一段准确描述日志中检测签名的外观──

3. Lisez le rapport de l'AAR de faible à fort de l'Anthropic. Identifiez la sous-tâche spécifique sur laquelle les AAR ont battu les chercheurs humains.
   Le rapport 弱到强 AAR 报告──识别 AAR 击败人类研究者的具体子任务──什么让它适应自动化?

4. Développez une politique d'allocation des tâches en queue qui équilibre la flexibilité des AAR (meilleurs résultats) avec les contraintes prescrites du flux de travail (audit plus facile).
   Le modèle de répartition des lignes de tâches de l'AAR 灵活性 (en anglais: AAR) est un modèle de répartition des lignes de tâches de l'AAR.

5. Lisez le seuil de R&D-4 de l'IA de RSP v3.0. Dans un paragraphe, décrivez ce que vous pensez qu'il traverserait que l'AR ne fait pas actuellement.
   Le R&D-4 value de l'IA de RSP v3.0 value── utilise un passage décrivant ce que vous pensez que va passer à travers elle alors que AAR ne traverse pas actuellement──

## Les termes clés

| Term | What people say | What it actually means |
|---|---|---|
| 术语 | 通俗说法 | 实际含义 |
| AAR | "Automated Alignment Researcher" | Claude Opus 4.6 instance operated autonomously on alignment problems |
| AAR | "自动化对齐研究器" | 在对齐问题上自主操作的 Claude Opus 4.6 实例 |
| Weak-to-strong training | "Training a stronger model with a weaker supervisor" | Classic scalable-oversight benchmark AARs outperformed humans on |
| 弱到强训练 | "用较弱监督者训练较强模型" | AAR 击败人类的经典可扩展监督基准 |
| Shared forum | "Where agents publish findings" | Append-only, out-of-sandbox storage |
| 共享论坛 | "Agent 发布发现之处" | 仅追加、沙箱外存储 |
| Out-of-sandbox log | "Agent cannot edit its own record" | Tamper-evident write-through to external storage |
| 沙箱外日志 | "Agent 不能编辑自己的记录" | 写入外部存储的防篡改透写 |
| Prescribed workflow | "Step-by-step plan from human designer" | Constrains AAR; often degrades performance vs free decomposition |
| 规定工作流 | "人类设计者的逐步计划" | 约束 AAR；通常比自由分解降低性能 |
| Free decomposition | "Agent decides how to break the task" | More capable, harder to audit |
| 自由分解 | "Agent 决定如何拆分任务" | 更有能力，更难审计 |
| AI R&D threshold | "RSP/FSF capability level" | Full automation of R&D pipeline at competitive cost |
| AI R&D 阈值 | "RSP/FSF 能力级别" | 在竞争成本下完全自动化 R&D 管道 |
| Compressed timeline | "Alignment vs capability race" | If capability compounds faster than alignment, misalignment risk grows |
| 压缩时间线 | "对齐与能力竞赛" | 若能力比对齐复利更快，不对齐风险增长 |

## Encore une lecture

- [Anthropic — Automated Weak-to-Strong Researcher](https://alignment.anthropic.com/2026/automated-w2s-researcher/) source principale.
  Le mot grec traduit par "l'évangile" est traduit par "l'évangile".
- [Anthropic Responsible Scaling Policy v3.0](https://anthropic.com/responsible-scaling-policy/rsp-v3-0) Cadrage des seuils de R&D en IA.
  Le cadre de la R&D de l'IA
- [Anthropic — Measuring AI agent autonomy](https://www.anthropic.com/research/measuring-agent-autonomy) un cadre plus large de l'autonomie des agents.
  Le cadre de l'agent autonome.
- [DeepMind Frontier Safety Framework v3](https://deepmind.google/blog/strengthening-our-frontier-safety-framework/) ML niveaux d'autonomie de R&D parallèles à la RSP.
  Traduction anglaise: R&D
- [Burns et al. (2023). Weak-to-Strong Generalization (OpenAI)](https://openai.com/index/weak-to-strong-generalization/) le problème sous-jacent attaqué par les AAR.
  Le problème de base de l'attaque
