# Scientifique de l'IA v2  Atelier de recherche autonome de niveau  Scientifique de l'IA v2  Studio de classe de recherche autonome

> L'AI Scientist de Sakana v2 (Yamada et coll., arXiv:2504.08066) gère la boucle de recherche complète: hypothèse, code, expériences, chiffres, écriture, soumission. Il s'agit du premier système à avoir une revue par les pairs de la réussite papier générée lors d'un atelier ICLR 2025. Une évaluation indépendante (Beel et coll.) a révélé que 42% des expériences avaient échoué à cause d'erreurs de codage et que l'examen de la littérature étiquetage souvent mal les concepts établis comme nouveaux. Les docteurs de Sakana ont mis en garde que la base de code exécute le code écrit par LLM et recommandent l'isolement de Docker. Les deux parties de cette image sont le point.

> **【中文解读】**L'étude complète de Sakana s'est déroulée en deux cycles: hypothèse, codage, expérience, diagramme, rédaction, soumission. C'est le premier ouvrage à avoir été produit par le biais du système d'évaluation de co-rédaction de l'ICLR 2025 工作坊.

> **【拓展：开放式研究的代价】**AlphaEvolve et DGM ont tous un "évaluateur à inspecter par machine" unité de test ou de base. Les études ne sont pas: théssifs évalués par le rédacteur, mais non par unité de test.

**Type:** Learn | **类型:** 学习
**Languages:** Python (stdlib, research-loop state-machine toy) | **语言:** Python（标准库，研究循环状态机玩具）
**Prerequisites:** Phase 15 · 03 (AlphaEvolve), Phase 15 · 04 (DGM) | **前置知识:** Phase 15 · 03（AlphaEvolve），Phase 15 · 04（DGM）
**Time:** ~60 minutes | **时间:** ~60 分钟

>  **【前置】**Les résultats de l'étude ont été obtenus en 1er janvier 2009 et ont été évalués par le comité de recherche de l'AI.
>  **【类比】**L'AI Scientist = "AI 博士生"──AlphaEvolve/DGM = 工程师(评估器=单元测试,强信号);AI Scientist = 博士生(评估器=审稿人,弱信号)──同样跑实验-评估-代循环,但弱信号评估让 Agent 容易欺骗自己42% 的实验代码有错误,文献综述把已知概念当新发现──修复:(1) Docker 隔离(必须执行 LLM 代码沙盒);(2) 人类复核(披露 AI 生成);(3) 引入强信号检查(如复现实测试) 

## Le problème , l' introduction du problème

La recherche est une tâche sans fin.

> L'étude est une mission ouverte.

Contrairement à la recherche algorithmique d'AlphaEvolve ou à l'auto-modification limitée par référence de DGM, un résultat de recherche n'a pas de critère de précision vérifiable par machine. Un article est jugé par les examinateurs, pas par les tests unitaires. Cela rend la boucle plus difficile à fermer  et plus précieuse si elle est fermée, car la recherche est le lieu où vit le progrès de la composition.

> Contrairement aux algorithmes de recherche d'AlphaEvolve ou de DGM, les résultats de l'étude ne sont pas vérifiables par un appareil.

AI Scientist v1 (Sakana, 2024) a fermé la boucle en partant des modèles écrits par l'homme. Le LLM a rempli des expériences dans un échafaudage fixe. AI Scientist v2 (Yamada et coll., 2025) supprime l'exigence de modèle en utilisant la recherche d'arbre agent avec une boucle de critique de modèle en langage de vision. Le système génère des idées, implémentera des expériences, produira des chiffres, écrira un article et réitérera les commentaires des critiques.

> L'AI Scientist v1(Sakana,2024) a commencé à se fermer en utilisant des modèles de rédaction humaine. L'AI Scientist v2(Yamada et autres,2025) a utilisé le cycle d'évaluation du modèle de langage avec des modèles de rédaction visuels.

> **【中文解读】**AI Scientist v2 (Sakana, 2025) 运行完整的研究循环:假设,编码,实验,图表,论文撰写和提交――它是通过ICLR 2025 工作坊同行评审的系统的第一个有生成论文的系统――但独立评估发现 42% des expériences en raison de l'erreur de codage échouent, la littérature complète est souvent désignée comme nouvelle − − − − − − − − − − − − − − − − − − − − − − − − − − − − − − − − − − − − − − − − − − − − − − − − − − − − − − − − − − − − − − − − − − − − − − − − − − − − − − − − − − − − − − − − − − − − − − − − − − − − − − − − − − − − − − − − − − − − − − − − − − − − − − − − − − − − − − − − − − − − − − − − − − − − − − − − − − − − − − − − − − − − − − − − − − − − − − − − − − − − − − − − − − − − − − − − − − − − − − − − − − − − − − − − − − − − − − − − − − − − − − − − − − − − − − − − − − − − − − − − − − − − − − − − − − − − − − − − − − − − − − − − − − − − − − − − − − − − − − − − − − − − − − − − − − − − − − − − − − − − − − − − − − − − − − − − − − − − − − − − − − − − − − − − − − − − − − − − − − − − − − − − − − − − − − − − − − − − − − − − − − − − − − − − − − − − − − − − − − − − − − − − − − − − − − − − − − − − − − − − − − − − − − − − − −

Résumé: un article généré par v2 a été accepté lors d'un atelier ICLR 2025 (avec révélation). Résumé: le système est loin d'être fiable.

> Le rapport de l'Institut de recherche et développement (ICLR) a été publié en juin 2015 à l'occasion de la réunion de la Commission européenne des technologies de l'information et de l'information (CICR) en juin 2015.

## Le concept de base.

### L'architecture et l'architecture

1. **Idea generation.**Le LLM propose des idées de recherche conditionnées sur un sujet et la littérature antérieure. v1 utilise des modèles; v2 utilise une recherche agentique sur un espace d'hypothèses.
   Le mot grec traduit par " le mot grec "**想法生成。**Le programme de maîtrise en sciences de l'université est basé sur des thèmes et des publications antérieures qui proposent des idées de recherche.
2. **Novelty check.**Une étape de récupération de la littérature vérifie si l'idée a été publiée.
   Le mot grec traduit par " le mot grec "**新颖性检查。**文献检查步骤检查想法是否已发表──这是 Beel 等人评估发现错误标记的步骤已建立的方法频繁被分类为新──
3. **Experiment plan.**L'agent rédige un protocole expérimental et écrit du code.
   Le mot grec traduit par " le mot grec "**实验计划。**Agent 起草实验协议并编写代码──
4. **Execution.**Le code est exécuté dans une boîte à sable. Les défaillances sont renvoyées dans une boucle de réessayer. Dans les mesures de Beel et al., 42% des expériences ont échoué à cause d'erreurs de codage à ce stade.
   Le mot grec traduit par " le mot grec "**执行。**Dans les tests effectués par Beel et d'autres personnes, 42% des expériences ont été effectuées à ce stade en raison d'une erreur de codage.
5. **Figure generation.**Un modèle de langage visuel lit les chiffres générés et les réécrit pour la clarté.
   Le mot grec traduit par " le mot grec "**图表生成。**视觉语言模型读取生成图表并为清晰性重写它们──这是 v2 关键技术添加──
6. **Writeup.**Le LLM rédige un article, il y a un réviseur interne.
   Le mot grec traduit par " le mot grec "**撰写。**LLM 起草论文, avec le rédacteur en chef interne
7. **Optional: submission.**Le document est soumis à un lieu.
   Le mot grec traduit par " le mot grec "**可选：提交。**论文提交到会议──

### Que signifie le résultat d'acceptation de l'atelier ?

Un article généré par v2 a passé l'examen par les pairs lors d'un atelier ICLR 2025. Les auteurs ont révélé l'origine du papier au comité du programme.

> Un v2 生成的论文在ICLR 2025 工作坊通过同行评审――作者向程序委员会披露论文的来源――接受是一个数据点;不是声称系统"做研究"的许可――

Un rapport de travail de l'équipe de recherche de l'Université de Londres (Université de Londres) a été publié en juin, et il a été publié en juin, en juin, en juin, par le journal Nature.

> 重要背景:工作坊论文的门低于主会议论文──同行评审有噪音;任何一天都有一小部分提交被接受──一次成功是概念证明,不是可靠性声明──Nature 2026 论文记录端到端循环,本身由人类研究人员共同撰写;不是"系统写了一篇自然论文"──

### Ce que l' évaluation indépendante a trouvé

Beel et coll. (arXiv:2502.14297) ont mené une évaluation externe.

> Le projet de loi de l'Union européenne sur les droits de l'homme (CEPA) a été adopté par le Conseil européen des droits de l'homme (CEPA) en décembre 2003.

- **Experiment failures.**42% des expériences ont échoué en raison d'erreurs de codage (mauvaises importations, défaillances de forme, variables non définies).
  Le mot grec traduit par " le mot grec "**实验失败。**42% des expériences ont été mal conçues, mais pas entièrement.
- **Novelty mislabeling.**La recherche de la littérature et de la récupération ont souvent marqué les concepts établis comme nouveaux.
  Le mot grec traduit par " le mot grec "**新颖性错误标记。**Les concepts déjà établis seront identifiés comme nouveaux.
- **Presentation-quality gap.**La critique des figures du langage de vision a produit des visuels de qualité de publication, masquant les faiblesses expérimentales sous-jacentes.
  Le mot grec traduit par " le mot grec "**呈现质量差距。**L'évaluation des graphiques de langage visuel produit des effets visuels de qualité de publication, couvrant les faiblesses de l'expérience de base.

La dernière conclusion est importante pour cette phase: un système qui produit des résultats convaincants sans faire de recherches convaincantes est plus dangereux, pas plus sûr, que celui qui échoue évidemment.

> La dernière découverte est importante pour cette phase: un système qui produit des résultats convaincants mais qui n'a pas été étudié de manière convaincante est plus dangereux et moins sûr que celui qui échoue manifestement.

L'évaluation doit atteindre les revendications sous-jacentes et non s'arrêter au chiffre.

> L'évaluation doit être réalisée en fonction de la déclaration de base, et non en fonction de la table.

### La peur de la fuite de la boîte à sable.

Le propre référentiel de Sakana README prévient:

> Sakana  propre entrepôt README  warning:

> En raison de la nature de ce logiciel, qui exécute le code généré par LLM, nous ne pouvons pas garantir la sécurité. Il y a des risques de paquets dangereux, accès non contrôlé au web et de reproduction de processus non intentionnés. Utilisez à vos risques et considérez l'isolement Docker.

> En raison de l'exécution du code de développement de ce logiciel, nous ne pouvons pas garantir la sécurité. Il existe un risque de accès à Internet incontrôlé et de processus incroyables.

Il s'agit de la forme opérationnelle de l'autonomie dans un domaine non vérifié. Le LLM écrit du code; le code fonctionne; le code peut faire tout ce que le processus est autorisé à faire. Sans une boîte à sable qui limite durement le système de fichiers, le réseau et les actions de processus, tout agent de recherche autodirectionné peut exfiltrer les données, brûler le calcul ou se réécrire.

> C'est une forme d'opération autonome dans le domaine non vérifié. L'écriture de code; code de fonctionnement; code peut faire tout ce qui est autorisé.

L'histoire de la boîte à sable d'AlphaEvolve est plus facile parce que son évaluateur est serré. La boucle d'AI Scientist v2 exécute du code ouvert avec des objectifs ouverts. C'est pourquoi elle a besoin d'un isolement plus fort (Docker minimum; seccomp / gVisor préféré) et d'un examen manuel de chaque soumission avant de quitter le système.

> La description de la boîte de références d'AlphaEvolve est plus facile, car son évaluateur est strict.

### Là où v2 se trouve dans la pile de frontière v2 est positionné en avant

| System | Target | Output kind | Evaluator | Known failure |
|---|---|---|---|---|
| 系统 | 目标 | 输出类型 | 评估器 | 已知失败 |
| AlphaEvolve | algorithms | code | unit + benchmark | bounded by evaluator rigor |
| AlphaEvolve | 算法 | 代码 | 单元 + 基准 | 受评估器严谨性约束 |
| DGM | agent scaffolding | code | SWE-bench | reward hacking |
| DGM | Agent 脚手架 | 代码 | SWE-bench | 奖励篡改 |
| AI Scientist v2 | research papers | text + code + figures | peer review (weak) | experiment failures, mislabeling, polish masking weakness |
| AI Scientist v2 | 研究论文 | 文本 + 代码 + 图表 | 同行评审（弱） | 实验失败、错误标记、修饰掩盖弱点 |

V2 a l'évaluateur automatique le plus faible des trois, la surface de sortie la plus large et le chemin le plus court vers les artefacts publics.

> v2 Les trois ont les plus faibles évaluateurs automatiques, les plus larges sorties et les plus courtes voies de production publique.

Les contrôles opérationnels (sandbox, examen, divulgation) effectuent la majeure partie des travaux de sécurité.

> L'exploitation de contrôle (SABox, Censure, Déclaration) a assumé la majeure partie du travail de sécurité.

## Utilisez-le avec le cadre de réalisation
```figure
mx-research-loop
```

## Utilisez-le

`code/main.py`Simulation de la boucle v2 en tant que machine d'état: idée → vérification de la nouveauté → expérience → figure → écriture → révision → acceptation-ou-iteration. Chaque état a une probabilité de défaillance configurable tirée des résultats de Beel et al. Exécutez le simulateur pour N boucles et comptez:

> `code/main.py`Pour chaque état, il y a une probabilité de défaillance de configuration à prélever de Beel et d'autres personnes.

- Combien d'idées sont soumises.
  En français, il est écrit:
- Combien de soumissions auraient une faille critique expérimentale que le papier poli cache.
  En anglais, le nombre de soumissions est de 5 à 6 ans.
- Comment les budgets de réessayer échanger qualité contre rendement.
  Traduction anglaise: Comment réessayer le budget entre la qualité et la production

## Envoyez-le . Produit .

`outputs/skill-ai-scientist-sandbox-review.md`est une liste de contrôle de deux portes pour tout ce produit par un agent de cycle de recherche avant qu'il ne quitte la boîte à sable.

> `outputs/skill-ai-scientist-sandbox-review.md`Il est nécessaire de vérifier la quantité de produits produits produits par l'agent.

## Les exercices

1. On court .`code/main.py`Quelle fraction de circuits produit un papier " propre " ? Quelle fraction produit un papier avec une faille d'expérience-échec la figure critique poli ?
   Le mot " usage " est traduit par " usage " .`code/main.py`Quelle est la proportion de cycles qui produisent des essais " propres " ? Quelle est la proportion de essais qui ont subi des échecs expérimentaux ?

2. Les défauts utilisent déjà les 42% / 25% de Beel et al.`--experiment-failure 0.20 --novelty-mislabel 0.10`et puis avec `--experiment-failure 0.60 --novelty-mislabel 0.40`Comment se déplace la part polissée mais défectueuse entre les deux courses ?
   Le nombre de personnes qui utilisent Beel et d'autres personnes est de 42% / 25% .`--experiment-failure 0.20 --novelty-mislabel 0.10`Je vais courir, puis je vais utiliser.`--experiment-failure 0.60 --novelty-mislabel 0.40`◊ Comment le rapport de modification mais de défaut entre deux opérations change-t-il ?

3. Lisez le repo README de Sakana sur les exigences de la boîte à sable.
   Le nom de l'équipe de recherche est le nom de l'équipe de recherche de recherche de l'équipe de recherche de recherche.

4. Lisez la section 4 sur l'écart de qualité de présentation.
   Le projet de conception d'un extra-évaluateur de l'expérience ayant des défauts de modification mais de modification.

5. Proposez un protocole d'examen humain pour les résultats des agents de recherche qui équivaut mieux à "un doctorant lit chaque article". Identifiez le goulet d'étranglement et la conception autour de celui-ci.
   Pour la recherche, l'agent de recherche a été élaboré pour la recherche et la recherche.

## Les termes clés

| Term | What people say | What it actually means |
|---|---|---|
| 术语 | 通俗说法 | 实际含义 |
| AI Scientist v1 | "Sakana's templated research agent" | Filled experiments into a fixed scaffold |
| AI Scientist v1 | "Sakana 的模板研究 Agent" | 在固定脚手架中填充实验 |
| AI Scientist v2 | "Template-free research agent" | Agentic tree search with VLM figure critique |
| AI Scientist v2 | "无模板研究 Agent" | 带有 VLM 图表评审的 Agent 式树搜索 |
| Agentic tree search | "Branching research agent" | Expands multiple experiment plans in parallel; prunes by internal critic |
| Agent 式树搜索 | "分支研究 Agent" | 并行展开多个实验计划；由内部评论者修剪 |
| Vision-language critique | "VLM polish on figures" | Multimodal model reads figures and rewrites them for clarity |
| 视觉语言评审 | "VLM 修饰图表" | 多模态模型读取图表并为清晰性重写 |
| Literature retrieval | "Novelty check" | Searches prior work to confirm idea novelty — documented to mislabel |
| 文献检索 | "新颖性检查" | 搜索先前工作以确认想法新颖性——文档记录会错误标记 |
| Polish masking | "Pretty paper, broken research" | Presentation quality exceeds experimental quality; hides weaknesses |
| 修饰掩盖 | "漂亮论文，破碎研究" | 呈现质量超过实验质量；隐藏弱点 |
| Sandbox escape | "LLM code breaks out" | Agent-executed code does things the loop designer did not intend |
| 沙箱逃逸 | "LLM 代码逃逸" | Agent 执行的代码做循环设计者未预期的事 |

## Encore une lecture

- [Yamada et al. (2025). The AI Scientist-v2](https://arxiv.org/abs/2504.08066)- Le papier.
  Le texte est en français.
- [Sakana blog on the Nature 2026 publication](https://sakana.ai/ai-scientist-nature/) résumé des fournisseurs avec contexte d'examen par les pairs.
  Le texte de la lettre de la première lettre est le texte de la lettre de la première lettre.
- [Beel et al. (2025). Independent evaluation of The AI Scientist](https://arxiv.org/abs/2502.14297) numéros d'évaluation externe.
  Nom de l'auteur:
- [Sakana AI Scientist v1 paper](https://arxiv.org/abs/2408.06292) le prédécesseur templé.
  Le nom de la ville est le nom de la ville de la ville de la ville de la ville de la ville de la ville de la ville de la ville de la ville de la ville de la ville de la ville de la ville de la ville de la ville de la ville de la ville de la ville de la ville de la ville de la ville de la ville de la ville de la ville de la ville de la ville de la ville de la ville de la ville de la ville de la ville de la ville de la ville de la ville de la ville de la ville de la ville de la ville de la ville de la ville de la ville de la ville de la ville de la ville de la ville de la ville de la ville de la ville de la ville de la ville de la ville de la ville de la ville de la ville de la ville.
- [Anthropic — Measuring AI agent autonomy](https://www.anthropic.com/research/measuring-agent-autonomy) un cadre plus large des agents de recherche à terme.
  Le plus large cadre de l'agent de recherche ouvert.
