# Le vote, la cohérence et la topologie du débat

> L'agrégation la moins chère: échantillon N d'agents indépendants, majorité-vot. Wang et coll. 2022 auto-consistance a fait cela avec un modèle échantillonné N fois.**heterogeneous**Les agents pour échapper à la monoculture  différents modèles, différents signaux, différentes températures, différents contextes. Au-delà du vote majoritaire, le débat sur la topologie est important: MultiAgentBench (arXiv:2503.01935, ACL 2025) a évalué la coordination étoile / chaîne / arbre / graphique et a trouvé **graph best for research**AgentVerse (ICLR 2024) documente deux modèles émergents  comportements volontaires et comportements de conformité  et la conformité est à la fois une caractéristique (trouver un consensus) et un risque (pensée de groupe, leçon 24).

> **【中文解读】**Cette section présente la structure organisationnelle du vote et du débat pour prendre des décisions par l'intermédiaire de plusieurs agents.

> **【拓展：voting debate topology→具体应用】**投票和辩論拓 形形 形 形 形 形 形 形 形 形 形 形 形 形 形 形 形 形 形 形 形 形 形 形 形 形 形 形 形 形 形 形 形 形 形 形 形 形 形 形 形 形 形 形 形 形 形 形 形 形 形 形 形 形 形 形 形 形 形 形 形 形 形 形 形 形 形 形 形 形 形 形 形 形 形 形 形 形 形 形 形 形 形 形 形 形 形 形 形 形 形 形 形 形 形 形 形 形 形 形 形 形 形 形 形 形 形 形 形 形 形 形 形 形 形 形 形 形 形 形 形 形 形 形 形 形 形 形 形 形 形 形 形 形 形 形 形 形 形 形 形 形 形 形 形 形 形 形 形 形 形 形 形 形 形 形 形 形 形 形 形 形 形 形 形 形 形 形 形 形 形 形 形 形 形 形 形 形 形 形 形 形 形 形 形 形 形 形 形 形 形   形     形 形       形   形       形                  形                                                                       


**Type:** Learn + Build | **类型:** 学习 + 构建
**Languages:** Python (stdlib) | **语言:** Python（标准库）
**Prerequisites:** Phase 16 · 07 (Society of Mind and Debate), Phase 16 · 14 (Consensus and BFT) | **前置知识:** Phase 16 · 07（心智社会与辩论），Phase 16 · 14（共识与 BFT）

>  **【前置】**Les résultats de la recherche ont été obtenus en vue de la réalisation de la phase 16 du projet.
>  **【类比】**投票拓 = "conférence table de mise en place"──星形 = 圆桌投票(独立);链形 = 接力修改(前面 Agent 的输出传给下一个);图形 = 圆桌讨论(多轮交互)──MultiAgentBench 结论:图形适合研究任务但有"协调税"──>4 个 Agent 性价比下降)──异质性是关键不同模型/温度/快速 防单一文化错误──
**Time:** ~75 minutes | **时间:** ~75 分钟

## ♪ Problème ♪ Introduction du problème ♪

Le débat peut améliorer la précision (Du et al., arXiv:2305.14325). Il peut également la dégrader.

> Le débat peut améliorer la précision, il peut également diminuer la précision.

1. Qui parle à qui (topologie).
   Qui et qui sont ceux qui parlent ?
2. Combien de tours (Du 2023: les tours et les agents comptent indépendamment).
   Le nombre de fois où l'on peut se rendre à la maison est de 20%.
3. Si les agents sont hétérogènes (les différents modèles de base brisent la monoculture).
   Le modèle de base est un modèle de base.
4. Si une voix d'adversaire est présente (stain-manning vs. paille-manning).
   Le problème est que le système de contrôle de la nature est un système de contrôle de la nature.

Les équipes qui "exécuter 5 agents et voter" sur une tâche sont souvent régressés par rapport à un seul agent. Les échecs ne sont pas aléatoires. Ils suivent la topologie et l'hétérogénéité. Cette leçon est la carte topologique.

> L'équipe "travaille 5 agents et vote" dur sur les tâches, souvent moins que l'agent seul. Les défaites ne sont pas aléatoires.

## Concept Le concept central

### Autosatisfaction, ligne de base pour un modèle unique

Wang et coll. 2022 (" L'auto-cohérence améliore la chaîne de raisonnement de la pensée ") ont échantillonné le même modèle N fois à une température > 0 et voté majoritairement sur les réponses de la voie de raisonnement. Le résultat sur GSM8K: des gains substantiels avec N = 40 échantillons sur un seul décode avide. L'auto-cohérence est le précurseur de l'agent unique au vote multi-agent.

> Wang 等人 2022年 (("auto-cohérence amélioration de la réflexion") dans des conditions de température > 0 N fois, et pour la plupart des votes sur la réponse du chemin de la réflexion N fois, et pour la réponse du processus de réflexion N fois.

Limit: l'auto-cohérence utilise un modèle de base. Les erreurs sont corrélatives par construction. Si le modèle a un biais systématique, tous les échantillons N le partagent.

> Limitation: la conformité à l'aide d'un modèle de base  Évolution de la structure est correcte Si le modèle a des préjugés systémiques, tous les échantillons le partagent

### Le vote multi-agents, l'extension hétérogène

Remplacez les échantillons N par des agents N * différents * différents. Modèles de base différents (Claude, GPT, Llama), différentes instructions, accès à des outils différents. L'avantage: erreurs non corrélatives. Coût: différents agents coûtent des montants différents; leur coordination ajoute des frais généraux.

> Pour les différents types d'actifs, les coûts de production sont différents, les coûts de production sont différents, les coûts de production sont différents, les coûts de production sont différents, les coûts de production sont différents.

Le nom canonique de 2026 pour le débat hétérogène est **A-HMAD** Débat hétérogène multi-agent adversaire. Pas universellement adopté, mais les articles utilisent le terme pour "débat sur différents modèles, ce qui réduit les erreurs corrélatives de l'effondrement de la monoculture".

> Le règlement de la mise en place de la politique de l'Union européenne en 2026**A-HMAD** opposant à l'antitype 辩论──并非普遍采用, mais les travaux utilisent le terme " différent modèle de débat, réduire les erreurs liées à la seule culture de l'effondrement "──

### Les quatre topologies

```
star                chain               tree                graph

    ┌─A─┐           A─B─C─D         ┌──A──┐              A───B
    │   │                           │     │              │ × │
    B   C                           B     C              D───C
    │   │                          / \   / \
    D   E                         D   E F   G           (fully connected)
```

Une étoile: un hub, les autres ne parlent qu'à un hub.
Chaîne: linéaire, chaque agent voit la sortie de l'autre.
Arbre: hiérarchique, utilisé par les systèmes d'agents hiérarchiques (leçon 06).
Graphique: tout à tout. Inclut une clique entièrement connectée et des DAG arbitraires.

> 星形: un centre, tous les autres agents seulement avec le centre dialogue.
> Chaque agent voit le produit de l'agent précédent.
> 树形: niveaux, utilisés pour niveaux Agent 系统 (第 06 课)
> 图形: arbitrary to arbitrary──incluant pleinement connecté du groupe et arbitrary DAG──

### La taxe de coordination (Bénéfice multi-agent)

MultiAgentBench (MARBLE, ACL 2025, arXiv:2503.01935) a comparé l'étoile, la chaîne, l'arbre, le graphique sur une suite de tâches comprenant la recherche, le codage et la planification.

> MultiAgentBench ((MARBLE,ACL 2025,arXiv:2503.01935) a réalisé un test de base sur la forme de l'étoile, la forme de la chaîne, la forme du bois et le dessin, dans des ensembles de tâches comprenant la recherche, le codage et la planification:

- **Graph**La topologie gagne sur les tâches de recherche.
  Le mot grec traduit par " le mot grec "**图形**拓在研究任务中获胜;信息随意流动;Agent peuvent se critiquer mutuellement.
- **Star**Les résultats obtenus par les tests de recherche sont les suivants:
  Le mot grec traduit par " le mot grec "**星形**En réponse rapide à la tâche factuelle, la victoire est centrée sur la coordination et l'intégration.
- **Chain**les gains sur les pipelines étape par étape (réfinition progressive).
  Le mot grec traduit par " le mot grec "**链形**Dans le même temps, il y a aussi des changements dans la vie.
- **Coordination tax**Le coût des montres et des jetons augmente plus vite que la qualité.
  Le mot grec traduit par " le mot grec "**协调税**Dans le tableau, il y a environ 4 agents qui apparaissent.

Le plafond de 4 agents est empirique, pas fondamental. Il reflète la capacité de contexte du LLM 2026: le contexte de chaque agent se remplit de résultats de pairs, et la valeur marginale de l'agent N + 1 additionnel diminue une fois que tout le monde peut voir tout le monde.

> 4 L'agent de haut niveau est expérimental, pas fondamental. Il reflète la capacité de 2026 LLM: chaque agent de haut niveau est rempli de ses produits de base, une fois que chacun peut voir chacun, ajouter N + 1  la valeur marginale de l'agent est en baisse.

### Stratégies de débat multi-agents (" Devrions-nous devenir fous ? ")

ArXiv:2311.17371 est l'enquête de 2023 sur les stratégies MAD. Les principales conclusions reproduites par d'autres: les variantes MAD qui sont * structurellement similaires* à l'auto-cohérence (échantillonnage indépendant + aggregation) ont souvent un rendement inférieur à l'auto-cohérence lors de l'utilisation du même budget.

> arXiv:2311.17371 est un résumé de stratégie MAD de 2023[6]. La découverte clé a été répétrée par d'autres: des variations MAD similaires à l'autodiscipline dans la structure, des échantillons indépendants + des polygones, qui ne sont pas toujours conformes à l'autodiscipline dans le même budget[6].

### Les modèles émergents

Le projet de loi de l'Union européenne sur les droits de l'hommehttps://proceedings.iclr.cc/paper_files/paper/2024/file/578e65cdee35d00c708d4c64bce32971-Paper-Conference.pdf) documentent deux comportements qui émergent du débat multi-agents même sans conception explicite:

- **Volunteer.**Un agent offre de l'aide ("Je peux faire la prochaine étape") sans être prévenu.
  Le mot grec traduit par " le mot grec "**自愿者。**L'agent principal fournit de l'aide.
- **Conformity.**Un agent ajuste sa position pour s'adapter à un critique, même si le critique a tort.
  Le mot grec traduit par " le mot grec "**从众。**L'agent 调整立场以匹配批评者, même si le critiqueur est erroris­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­

La conformité est la raison pour laquelle le débat jusqu'à l'accord récompense les intimidateurs.

> De nombreuses personnes ont été récompensées pour avoir "débattu à l'accord" avec les plus forts.

### Hétérogénéité: le bouton réel qui déplace la précision

Un schéma 2024-2026 dans la littérature pratique: échanger un de vos agents N pour un modèle de base différent donne une augmentation de précision plus grande que d'augmenter N par 1. L'intuition est monoculture  chaque nouvelle source d'erreur indépendante vaut plus qu'un échantillon corrélateur supplémentaire.

> Un modèle dans la littérature pratique de 2024-2026: remplacer un modèle de base différent par un modèle de base différent par rapport à l'augmentation de N+1 agents  apporter un taux de précision plus élevé  augmenter le sentiment que chaque culture  chaque nouvelle source d'erreur indépendante  plus de valeur que les échantillons associés supplémentaires  augmenter le taux de précision  augmenter le taux de précision  augmenter le taux de précision  augmenter le taux de précision  augmenter le taux de précision  augmenter le taux de précision  augmenter le taux de précision  augmenter le taux de précision  augmenter le taux de précision  augmenter le taux de précision  augmenter le taux de précision  augmenter le taux de précision  augmenter le taux de précision  augmenter le taux de déficit  augmenter le taux de déficit  augmenter le taux de déficit  augmenter le taux de déficit  augmenter le taux de déficit  augmenter le taux de déficit  augmenter le taux de déficit de déficit  augmenter le taux de déficit de déficit  augmentation de déficit 

Dans la limite, l'hétérogénéité bat la numerité.

> Dans les cas limités, la différence de structure est supérieure au nombre. Dans la plupart des cas, trois modèles différents sont supérieurs à cinq copies du même modèle.

### Méthodes du jury

Le cadre Sibyl (cité dans la littérature Minsky-LLM) formalite un " jury "  un petit ensemble d'agents spécialisés qui affinent les réponses en votant à chaque étape. Contrairement au vote à la majorité ordinaire, un jury a des rôles: un agent interroge, un fournit le contexte, un marque la plausibilité. Les méthodes du jury sont un point intermédiaire entre le vote ordinaire (bon marché, enclin à la monoculture) et le MAD complet (bon marché, enclin à la conformité).

> Sibyl framework (en citation dans la littérature Minsky-LLM) a formalisé le "jury"一小组 专业化 Agent 通过每阶段投票来改进答案──与简单多数投票不同, le jury a un rôle: un agent 交叉质询, un fournir sur la base, un évaluation rationnelle── un jury method介介于简单投票(便宜,易单一文化) 和完整 MAD(昂贵,易从众) 之间──

### Lorsque le vote avec débat domine

- La question a une vérité fondamentale (facts, mathématiques, comportement de code).
  Le vote est un vote qui a un sens.
- Les agents peuvent accéder à différentes sources ou outils (l'hétérogénéité est disponible).
  L'agent peut accéder à différentes sources ou outils (en anglais: Agent)
- Les tours sont délimités (2-3 typiquement) et il y a un juge ou un vérificateur séparé.
  Traduction anglaise:轮次有界 (généralement 2-3 rounds), avec un comité ou un éditeur indépendant.
- Le budget permet de 3 à 5 agents. Au-delà de 5 à 7 sur la topologie graphique, l'impôt de coordination domine.
  Le budget permet de travailler avec 3 à 5 agents.

### Quand le vote avec le débat fait mal

- Les agents convergent pour trouver la réponse la plus sûre, pas la plus correcte.
  Le problème est le type d'opinion. L'agent a reçu la réponse la plus sûre, mais pas la plus exacte.
- Tous les agents partagent un modèle de base.
  Tous les agents communément utilisés sont des acteurs de la culture.
- Les tours sont illimités, la conformité gagne à chaque fois.
  Le nombre de victoires est de 7 à 7 fois.
- La tâche est simple: un agent unique avec une cohérence à N = 5 est moins cher et aussi précis.
  Traduction anglaise: tâche simple. Un seul agent en N = 5 时的自一致性更便宜且同样准确.

## Construisez-le en main
```figure
sw-debate-topology
```

## Faites-le

`code/main.py`les implémentations:

- `run_star(agents, hub, question)` Les sondages de chaque travailleur, les agrégats.
  Le mot grec traduit par " le mot grec "`run_star` Centre de formation pour chaque employé
- `run_chain(agents, question)` raffinement séquentiel.
  Le mot grec traduit par " le mot grec "`run_chain` 顺序改进──
- `run_tree(root, children, question)` hiérarchique avec aggregation de profondeur-2.
  Le mot grec traduit par " le mot grec "`run_tree` 层次化, profondité 2 聚合──
- `run_graph(agents, question, rounds)`- Débat général, coups limités.
  Le mot grec traduit par " le mot grec "`run_graph`                                                                                                                                                                                                                                                              
- Un cadran d' hétérogénéité scripté: chaque agent a un `error_bias`indiquant son erreur systématique.
  Chaque agent a un seul.`error_bias`Indiquer son système d'erreur.
- Une corde de mesure qui exécute chaque topologie à N=3, 5, 7 et rapporte (exactitude, total_tokens, wallclock_simulated).
  Le nombre de jours de travail effectués par les opérateurs est de 0,7%.

Je vais courir .

```
python3 code/main.py
```

Expérience attendue: table de topologie × N → (exactitude, jetons, latence). Graphique gagne à N=3-5 sur les tâches de recherche; étoile gagne sur les tâches factuelles rapides; graphique à N=7 montre la taxe de coordination (la latence gonfle plus vite que la précision).

> 预期输出:拓 × N →(准确率,token,延迟)表格──图形在 N=3-5 的研究风格任务上获胜;星形在快速事实性任务上获胜;图形在 N=7 时显示协调税(延迟膨胀快于准确率)

## Utilisez-le.

`outputs/skill-topology-picker.md`est une compétence qui lit une description de tâche et recommande une topologie (étoile / chaîne / arbre / graphique), un N (nombre d'agents), un profil d'hétérogénéité (modèles de base à utiliser) et une ligne ronde.

> `outputs/skill-topology-picker.md`Il est un outil de formation, une formation, une formation, une formation, une formation, une formation, une formation, une formation, une formation, une formation, une formation, une formation, une formation, une formation, une formation, une formation, une formation, une formation, une formation, une formation, une formation, une formation, une formation, une formation, une formation, une formation, une formation, une formation, une formation, une formation, une formation, une formation, une formation, une formation, une formation, une formation, une formation, une formation, une formation, une formation, une formation, une formation, une formation, une formation, une formation, une formation, une formation, une formation, une formation, une formation, une formation, une formation, une formation, une formation, une formation, une formation, une formation, une formation, une formation, une formation, une formation, une formation, une formation, une formation, une formation, une formation, une formation, une formation, une formation, une formation, une formation, une formation, une formation, une formation, une formation, une formation, une formation, une formation, une formation, une formation, une formation, une formation, une formation, une formation, une formation, une formation, une formation, une formation, une formation, une formation, une formation, une formation, une formation, une formation, une formation, une formation, une formation, une formation, une formation, une formation, une formation, une formation, une formation, une formation, une formation, une formation, une formation, une formation, une formation, une formation, une formation, une formation, une formation, une formation, une formation, une formation, une formation, une formation, une formation, une formation, une formation, une formation, une formation, une formation, une formation, une formation, une formation, une formation, une formation, une formation, unité, unité, unité, unité, unité, unité, unité, unité, unité, unité, unité, unité, unité, unité, unité, unité, unité, unité, unité, unité, unité, unité, unité, unité, unité, unité, unité, unité, unité, unité, unité, unité, unité, unité, unité, unité, unité, unité, un

## Envoyez-le en ligne .

Pour tout ensemble:

- Commencez par **self-consistency at N=5**Il est le modèle de base bon marché.
  Le modèle de base est fort.**N=5 自一致性**C'est une ligne bon marché.
- Mettre à jour à **heterogeneous voting at N=3**Si la précision est importante, mesurez le delta.
  Si le taux de précision est important, le niveau est élevé.**N=3 异构投票**◊ Mesure de la quantité de nourriture
- Ne pas passer à **debate topology**si la tâche est structurée (recherche, plusieurs étapes) et que des tours limités sont faisables.
  Traduction anglaise: seulement dans les tâches ont une structure (étude, plusieurs étapes) et des périodes de mise à niveau (grader à la mise à niveau)**辩论拓扑**Il y a une autre.
- Si une minorité a toujours raison, vous avez un signal de diversité.
  Le nombre de personnes qui ont été victimes de la violence et de la violence est de plus en plus élevé.
- "Mieux précis à 10 fois le coût" est une décision commerciale.
  Le taux de précision de 10 fois le coût est un taux de précision commercial.

## Les exercices

1. On court .`code/main.py`. Tracer la courbe de coordination-taxe pour la topologie du graphique: précision vs N, jetons vs N. À quel N la courbe s'inflecte?
   Le mot " l' économie " est traduit par " l' économie ".`code/main.py`◊ Le tableau de bord est le plus précis.
2. Comment la base de préjugés identique se compare-t-elle à la base de préjugés de l'attaque de monoculture de la leçon 14 ?
   Comment comparer l'A-HMAD à l'attaque de la culture unique de la 14e classe ?
3. Ajouter un rôle de "juger" à la topologie du graphique qui ne vote pas, mais marque seulement le consensus final.
   En français, le rôle de "commissaire" est d'ajouter un rôle de "commissaire" dans le tableau, non de voter seulement pour évaluer le consensus final.
4. Lisez le document AgentVerse (ICLR 2024). Identifiez quel comportement émergent votre mise en œuvre présente le plus fortement. Pouvez-vous attirer le comportement opposé par un changement rapide?
   Le texte de l'article suivant est le plus ancien de tous les textes de la Bible.
5. Lisez MultiAgentBench (arXiv:2503.01935) Section 4 (expériences topologiques).
   Le résultat de la recherche est le résultat de la recherche.

## Les termes clés

| Term | What people say | What it actually means |
|------|----------------|------------------------|
| Self-consistency / 自一致性 | "Sample N times, vote" / "采样 N 次，投票" | Wang 2022. Single model, N temperature>0 samples, majority vote on reasoning paths. / Wang 2022。单模型，N 次 temperature>0 采样，推理路径多数投票。 |
| Heterogeneity / 异构性 | "Different models" / "不同模型" | Ensemble of different base models or prompt families. Breaks monoculture. / 不同基础模型或提示族的集成。打破单一文化。 |
| MAD / 多 Agent 辩论 | "Multi-agent debate" / "多 Agent 辩论" | Generic term for agents exchanging critiques over rounds. See Du 2023. / Agent 跨轮次交换批评的通用术语。见 Du 2023。 |
| A-HMAD / 对抗性异构 MAD | "Adversarial Heterogeneous MAD" / "对抗性异构 MAD" | MAD variant emphasizing different models + adversarial structure. / 强调不同模型 + 对抗结构的 MAD 变体。 |
| Topology / 拓扑 | "Who talks to whom" / "谁和谁对话" | Star, chain, tree, graph. Determines information flow. / 星形、链形、树形、图形。决定信息流。 |
| Coordination tax / 协调税 | "Diminishing returns" / "边际收益递减" | Above ~4 agents on graph, cost grows faster than quality. / 图形拓扑约 4 个 Agent 后，成本增长快于质量。 |
| Volunteer behavior / 自愿者行为 | "Unprompted help" / "主动帮助" | AgentVerse emergent pattern: an agent offers to take a step. / AgentVerse 涌现模式：Agent 主动提出执行步骤。 |
| Conformity behavior / 从众行为 | "Agreement under pressure" / "压力下的同意" | AgentVerse emergent pattern: an agent aligns with a critic. / AgentVerse 涌现模式：Agent 与批评者对齐。 |
| Jury / 陪审团 | "Small specialized panel" / "小型专业小组" | Sibyl-style ensemble with roles (examiner, context, scorer). / Sibyl 风格的带角色集成（质询者、上下文、评分者）。 |

## Encore une lecture

- [Wang et al. — Self-Consistency Improves Chain of Thought Reasoning](https://arxiv.org/abs/2203.11171) L'indice de base pour un modèle unique
- [Du et al. — Improving Factuality and Reasoning via Multiagent Debate](https://arxiv.org/abs/2305.14325) Les deux agents et les tours sont indépendants
- [MultiAgentBench / MARBLE](https://arxiv.org/abs/2503.01935) référence de topologie montrant le graphique le mieux adapté à la recherche, chaîne pour les pipelines
- [Should we be going MAD?](https://arxiv.org/abs/2311.17371) Enquête sur la stratégie MAD; découvre que la MAD perd souvent à cause de l'auto-cohérence à un budget égal
- [AgentVerse (ICLR 2024)](https://proceedings.iclr.cc/paper_files/paper/2024/file/578e65cdee35d00c708d4c64bce32971-Paper-Conference.pdf) modèles émergents de volontariat et de conformité
- [MARBLE repo](https://github.com/ulab-uiuc/MARBLE) mise en œuvre des indices de référence
