# Le projet de recherche de l'architecture de la société est un projet de recherche de l'architecture de l'architecture de l'architecture.

> Une seule trajectoire de chaîne de pensée n'a pas de place pour retomber. ToT (Yao et coll., 2023) transforme le raisonnement en un arbre avec une auto-évaluation sur chaque nœud. LATS (Zhou et coll., 2024) unifie ToT avec ReAct et Réflexion dans la recherche d'arbre de Monte Carlo. Le jeu de 24 passe de 4% (CoT) à 74% (ToT); LATS atteint 92,7% pass@1 sur HumanEval.

> **【中文解读】**单条思维链没有回溯空间――ToT将推理变为带有自评树结构,Game of 24 4% 提升至74%―LATS 统一了ToT、ReAct 和 Reflection,Use蒙特卡洛树搜索实现,HumanEval 达到92.7% pass@1──

> **【拓展：ToT/LATS → OpenAI o1/o3 的推理搜索】**La "pensée profonde" de la série OpenAI o1/o3 est essentiellement la recherche dans l'espace de raisonnement pour explorer plusieurs voies, évaluer et choisir le meilleur.

>  **【前置】**本节硬核,前置必须扎实:Phase 14·01(ReAct) LATS 内部就是ReAct;Phase 14·03(Réflexion) LATS  Self-Reflector 复用 Reflexion 机制; ainsi que MCTS(蒙特卡洛树搜索)`Q(s,a) + c*sqrt(lnN/N)`Les deux éléments représentent quoi, d'abord, voir AlphaGo 论文或教程.

**Type:** Build | **类型:** 构建
**Languages:** Python (stdlib) | **语言:** Python (标准库)
**Prerequisites:** Phase 14 · 01 (Agent Loop), Phase 14 · 03 (Reflexion) | **前置知识:** Phase 14 · 01 (Agent 循环), Phase 14 · 03 (Reflexion)
**Time:** ~75 minutes | **时间:** ~75 分钟

## Objectifs d'apprentissage

- Le raisonnement de cadre comme la recherche: les nœuds sont des "pensées", les bords sont des "expansions", la valeur est "comme prometteuse".
  Le cadre de recherche est "penser", le côté est "élargir", le fond est "avoir beaucoup de perspectives".
- Implémenter une recherche sur les arbres BFS de style stdlib ToT avec un score d'auto-évaluation.
  Le code de référence est le code de référence de la langue française.
- S' étendre à une boucle de jouets LATS MCTS avec sélection / extension / simulation / backpropagate.
  Le jeu est un jeu de mots, qui est un jeu de mots.
- Décidez quand la recherche vaut le multiplicateur des jetons (jeu de 24, génération de code) et quand une seule trajectoire est suffisante (question simple et réponse).
  Je suis en train de faire une demande de référencement pour la première fois.

## Le problème , l' introduction du problème

La chaîne de pensée est une marche linéaire. Si la première étape est incorrecte, chaque étape ultérieure fonctionne sur une mauvaise prémisse.

> Si la première étape est erronée, chaque étape suivante est basée sur une erreur prémissive.

Ce qui est nécessaire au raisonnement, c'est la capacité de proposer plusieurs candidats, de les évaluer, de choisir ceux qui sont prometteurs et de revenir en arrière quand des endroits bloqués apparaissent.

> La raison est de proposer plusieurs candidatures, de les évaluer, de choisir des perspectives, de les repérer en même temps.

> **【中文解读】**Si la première étape est erronée, chaque étape ultérieure est basée sur une erreur de prémisse.

## Le concept de base.

### L'arbre des pensées (Yao et coll., NeurIPS 2023)

Chaque nœud est une étape intermédiaire cohérente ("une pensée"). Chaque nœud peut s'étendre à des pensées de K enfant. Le LLM auto-évaluent chaque nœud avec une demande de notation.

> Chaque point est un étape intermédiaire de la séquence de pensée. Chaque point peut être étendu à K 个子思考.

```
                     (root: "find 24 from 4 6 4 1")
                    /               |            \
           ("6 - 4 = 2")    ("4 + 1 = 5")    ("4 * 6 = 24")  <- Score: HIGH
              /   \              |                  |
          ...    ...          ...                finish
```

L'auto-évaluation est la pièce à porter.`sure / likely / impossible`classification `1..10`Les trois ont battu CoT de façon substantielle sur le jeu de 24 (4% -> 74% avec GPT-4).

>  **【类比】**Pour chaque étape, calculer 3-5 changements dans le cerveau, vous pouvez évaluer quel changement est plus avantageux, vous pouvez éliminer les changements nettement moins favorables, vous pouvez également évaluer les changements négatifs.

> L'évaluation est une partie de la charge centrale.`sure / likely / impossible`Classe`1..10`Numéro de la valeur de l'évaluation et du vote des candidats.

### LATS (Zhou et coll., ICML 2024)

LATS unit le TOT, le ReAct et la Réflexion sous MCTS.

> LATS dans MCTS a été créé pour la TOT, la réaction et la réflexion.

- **Policy**: proposer des actions candidates suivantes (react).
  Le mot grec traduit par " le mot grec "**策略**: proposer candidature: action
- **Value function**: score une trajectoire partielle (auto-évalue à la ToT).
  Le mot grec traduit par " le mot grec "**价值函数**Le programme de formation est basé sur la formation professionnelle.
- **Self-reflector**: en cas d'échec, écrivez une réflexion en langage naturel (à la Réflexion) et utilisez-la pour revoir les déploiements futurs.
  Le mot grec traduit par " le mot grec "**自我反思器**Réflexion 风格), utilisé pour re-élaborer des projets de développement.

Les résultats en temps papier: HumanEval pass@1 92,7% avec GPT-4 (SOTA), WebShop moyenne 75,9 avec GPT-3.5 (approche de l'ajustement basé sur le gradient).

> 环境反(观察) Mix into value function, make search by real tool results rather than merely model view drive。论文发表时的结果:GPT-4 上 HumanEval pass@1 92.7%(SOTA),GPT-3.5 上 WebShop 平均 75.9(接近基于梯度的微调)。

### MCTS, au minimum

Quatre phases par itération:

> Chaque étape:

1. **Select** passer de la racine à la feuille en utilisant la TCC (confiance supérieure liée aux arbres).
   Le mot grec traduit par " le mot grec "**选择**Utiliser UCT                                                                                                                                                                                                                                                            
2. **Expand** générer des enfants K par l'intermédiaire de la politique.
   Le mot grec traduit par " le mot grec "**扩展**Utiliser des stratégies pour générer des K 个子节点。
3. **Simulate** déploiement d'un enfant utilisant la politique, score la feuille avec la fonction de valeur (ou la récompense environnementale).
   Le mot grec traduit par " le mot grec "**模拟**从子节点用策略展开,用价值函数 (从子节点用策略展开,用价值函数,或环境奖励) 评分叶节点──
4. **Backpropagate** les comptes de visites et les estimations de valeur actualisés sur le parcours.
   Le mot grec traduit par " le mot grec "**反向传播** En cours de route, les nouvelles statistiques de visite et les estimations de valeur.

Formule de l' UCT: `Q(s, a) + c * sqrt(ln N(s) / N(s, a))`Le premier terme est l'exploitation, le second est l'exploration.`c`par tâche.

> La formule UCT:`Q(s, a) + c * sqrt(ln N(s) / N(s, a))` La première est l'utilisation; la seconde est l'exploration  le réglage des tâches `c`Il y a une autre.

### La réalité des coûts

La recherche explose des jetons. ToT sur Game of 24 utilise 1001000x les jetons de CoT. LATS est similaire.

> ️ **【易错点】**Voir TOT dans le jeu de 24 上 +70 个点就以为是"银弹",套到所有任务上.**后果**En réponse à une simple question, le jeton est dépensé 1000 fois en échange de 0% de la hausse, le compte est explosé.**一行修复**Le premier est de 10 échantillons par rapport à la COT par rapport à la COT, et le deuxième est de 5 points pour la recherche de la COT.

> 搜索会爆炸代币――ToT 在 24 上消耗 CoT 100-1000 倍代币――LATS 类似――

- Les tâches dans lesquelles une seule trajectoire est démontrativement insuffisante (jeu de 24, code complexe).
  Le jeu de 24 复杂代码)
- Les tâches où l'horloge murale est moins importante que la précision.
  Traduction anglaise: correctité est une tâche plus importante que le temps.
- Les tâches avec une fonction de valeur bon marché et fiable (tests unitaires pour le code, cible explicite pour les mathématiques).
  Traduction anglaise: il existe une fonction de valeur de valeur de qualité (en anglais: cód.

Si votre tâche a une seule bonne réponse et un évaluateur bruyant, la recherche rend souvent les choses pires  elle trouve une mauvaise réponse " bonne note ".

> 🤔 **【困惑】**Q: LATS mettre à jour / Réagir / Réflexion 三個都"統一"了,那不是学了 LATS就足了吗 A:不足──LATS est une "重型武器"一次完整搜索要展开上百节点,单任务代币 成本可达百万级──生产环境的95% 任务用 React + 简单 Reflexion 已足──LATS est seulement dans " valeurs de fonctionnalités peu fiables "comme le test des unités de code tasks)

> Si votre tâche ne comporte qu'une seule réponse correcte mais que l'évaluateur est bruyant, la recherche rend souvent la situation pire.

> **【中文解读】**搜尋会爆炸 TokenToT 在 24 上消耗 CoT 100-1000倍. 搜尋:单轨迹明显不足、正确性比速度重要、有廉价可靠的价值函数──如果评估器有噪音,搜索可能找到"高分但错误"的答案──

### 2026 positionnement

La plupart des agents de production n'exécutent pas de LATS. Ils exécutent ReAct avec une vérification basée sur des outils (CRITIC, leçon 05).

> La plupart des producteurs de produits ne travaillent pas dans des laboratoires de traitement des données.

- Les agents de codage qui exécutent des tests en tant que fonction de valeur (au style HumanEval).
  Le code de la fonction de valeur est l'agent de la fonction de valeur.
- Des agents de recherche approfondie qui explorent plusieurs chemins de requête.
  En français, le terme "agent de recherche" est traduit par "agent de recherche".
- Des flux de travail lourds à planifier à l'intérieur des sous-graphes LangGraph.
  Le langage de la planète est le langage de la planète.

AlphaEvolve (Léction 11) est l'extrême de 2025: recherche évolutionnaire sur le code, aptitude vérifiable par machine, gains frontaliers (première amélioration de la matmul 4x4 en 56 ans).

> AlphaEvolve (n° 11) est un exemple extrême de 2025: recherche d'évolution du code, adaptation des machines à vérifier, avant-coût de la course.

## Construisez-le et mettez-le en œuvre.
```figure
tree-of-thoughts
```

## Faites-le

`code/main.py`les implémentations:

> `code/main.py`实现:

- Un petit BFS sur une tâche stylisée "opération de sélection d'arithmétique".
  Le mot "BFS" est traduit par "BFS".
- Un jeu LATS MCTS en boucle sur la même tâche (Sélection / Expansion / Simulation / Backpropagate) avec la sélection UCT.
  Le jeu de l'équipe de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation.
- Une fonction de valeur qui compose un score symbolique plus un score auto-équivalent.
  Une valeur de la fonction de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur est est est est est est est est est est est est est est est est est est est est est est.

- Je vais le faire.

> 运行:

```
python3 code/main.py
```

La trace montre que ToT élargit trois candidats par nœud avec BFS, comparativement à LATS convergeant sur le meilleur déploiement via MCTS.

> 轨迹显示 ToT Using BFS 每节扩展三个候选人,与LATS 通过MCTS 收到最佳展开对比──两者都印印了标记计数──

## Utilisez-le avec le cadre de réalisation

LangGraph envoie l'exploration de style ToT comme modèles de sous-graphes; le blog de l'équipe LangChain sur LATS (mai 2024) est le tutoriel de référence. LlamaIndex envoie un `TreeOfThoughts`Pour la plupart des agents de production de 2026 ce modèle vit derrière une`if task_complexity > threshold: use_search()` voir le modèle d'évaluation-optimisation dans la leçon 05.

> LangGraph va explorer le style de la LATS en tant que modèle de dessin; LangChain 团队关于 LATS 的博客(2024 年 5 月) est un cours de référence.`TreeOfThoughts`Pour la plupart des agents de production de 2026, ce modèle existe en`if task_complexity > threshold: use_search()`门控后参见第 5 课的评估器-优化器模式──

## Envoyez-le . Produit .

`outputs/skill-search-policy.md`choisit entre ReAct linéaire, ToT, LATS et recherche évolutionnaire compte tenu de la forme de la tâche, du budget et de la fidélité de l'évaluateur.

> `outputs/skill-search-policy.md`∆en fonction de la forme de la tâche, du budget et de l'évaluation, la réaction en ligne, le TOT, le LATS et la recherche d'évolution entre les choix.

## Les exercices

1. Exécutez le jouet LATS avec UCT c=0,1 vs c=2,0.
   Le système de calcul de la distance de trajet est différent.
2. Le MCTS trouve-t-il toujours la meilleure feuille ? quelle est la limite minimale de signal-à-bruit qu'il tolère ?
   Le MCTS peut-il encore trouver le meilleur niveau de la valeur ? Quelle est la proportion de bruit minimale qu'il peut tolérer ?
3. Mettre en œuvre des ToT de recherche de faisceaux (maintient le top-k à chaque niveau) et comparer avec BFS.
   Le code de la ligne de référence est le code de la ligne de référence.
4. Lire la section 5.1.Réproduire le nombre de trajectories HumanEval: combien de déploiements faut-il pour atteindre le passage@1 signalé?
   Le nombre de trajets de l'Eval humain: atteindre le rapport de passage@1 需要多少次展开?
5. Lisez la discussion du document LATS sur "quand le LATS aide moins". Écrivez une règle de décision en un paragraphe pour cartographier la forme de la tâche pour la stratégie de recherche.
   Le texte de la lettre de référence est le texte de la lettre de référence de la lettre de référence de la lettre de référence.

## Les termes clés

| Term | What people say | What it actually means |
|------|-----------------|-----------------------|
| 术语 | 通俗说法 | 实际含义 |
| Tree of Thoughts | "Branching CoT" / "分支思维链" | Yao et al. — tree of thought nodes with self-evaluation / Yao 等人——带自评估的思维节点树 |
| LATS | "MCTS for LLMs" / "LLM 的 MCTS" | Zhou et al. — unifies ToT + ReAct + Reflexion under MCTS / Zhou 等人——在 MCTS 下统一 ToT+ReAct+Reflexion |
| UCT | "Upper confidence bound" / "上置信界" | Select formula balancing exploitation (Q) and exploration (ln N / n) / 平衡利用(Q)和探索(ln N/n)的选择公式 |
| Value function | "How good is this state" / "状态有多好" | Prompted LLM score or environment reward; feeds backprop / 提示的 LLM 评分或环境奖励；驱动反向传播 |
| Policy | "Action proposer" / "行动提议器" | ReAct-style generator; emits candidate next thoughts/actions / ReAct 风格生成器；发出候选下一步思考/行动 |
| Rollout | "Simulated trajectory" / "模拟轨迹" | Walk from a node to a leaf using policy, score with value / 用策略从节点走到叶节点，用价值函数评分 |
| Backpropagate | "Update ancestors" / "更新祖先" | Push the leaf's reward up the path, updating visit counts and Q / 将叶节点的奖励沿路径上推，更新访问计数和 Q 值 |
| Search cost | "Token explosion" / "Token 爆炸" | 100-1000x CoT on Game of 24; budget before you adopt / Game of 24 上是 CoT 的 100-1000 倍；采用前先做预算 |

## Encore une lecture

- [Yao et al., Tree of Thoughts (arXiv:2305.10601)](https://arxiv.org/abs/2305.10601) le papier canonique
  Le thème de la rédaction de l'article est:
- [Zhou et al., LATS (arXiv:2310.04406)](https://arxiv.org/abs/2310.04406) MCTS avec rétroaction Réflexion
  Le mot "réflexion" est traduit par "réflexion".
- [LangGraph overview](https://docs.langchain.com/oss/python/langgraph/overview) modèles de sous-graphe pour la recherche
  Le langage est le langage de la langue.
- [AlphaEvolve (arXiv:2506.13131)](https://arxiv.org/abs/2506.13131) recherche évolutionnaire avec des évaluateurs programmatiques
  Le programme de recherche de l'AlphaEvolve est un outil de recherche de l'AlphaEvolve.
