# La société de l'esprit et le débat multi-agents

> La prémisse de Minsky de 1986  intelligence est une société de spécialistes  est redécouverte chaque décennie. En 2023, Du et al. l'ont transformé en un algorithme concret: plusieurs instances de LLM proposent des réponses, lisent les réponses, critiquent et mettent à jour les unes les autres. Au cours de N tours, ils convergent sur un consensus qui bat la CoT à zéro coup et la réflexion sur six tâches de raisonnement et de factualité. Deux résultats sont importants: les deux **multiple agents**et **multiple rounds**La société est plus forte qu'un monologue à un seul agent, l'échange à plusieurs tours est plus fort qu'un vote à un seul coup.

> **【中文解读】**Ce chapitre présente le débat social sur le mental.

> **【拓展：society of mind debate→具体应用】**Marvin Minsky 心智社会 (en 1986) propose que le savoir soit le produit de nombreuses collaborations simples de l'esprit. Cette idée permet de réaliser  plusieurs agents dans le système de débat multi-agent de 2026 à travers différents points de vue.


**Type:** Learn | **类型:** 学习
**Languages:** Python (stdlib) | **语言:** Python (标准库)
**Prerequisites:** Phase 16 · 04 (Primitive Model) | **前置知识:** Phase 16 · 04 (Primitive Model)
**Time:** ~60 minutes | **时间:** ~60 分钟

>  **【前置】**Je suis en train de faire une étude de la théorie de l'intelligence et de la société.
>  **【类比】**Du agent 辩论 = "学术同行评审"――单 agent = 一个作者写论文(容易自但片面); du agent 辩论 = 多位审稿人 + 作者多轮回应,最终共识更稳健―― Du et al. 2023 证明: du agent + 多轮独立贡献提升不是简单加法,是协同效应──3-5 个代理 最优(多多了反而成一团)

## ♪ Problème ♪ Introduction du problème ♪

L'auto-consistance  échantillonnez un modèle plusieurs fois et prenez la réponse majoritaire  est l'amélioration de raisonnement la moins chère que vous pouvez suivre. Elle fonctionne, mais elle se saturera rapidement. Vous pouvez doubler vos échantillons et ne pas voir un autre saut significatif.

> La conformité à un modèle à plusieurs reprises et à la majorité des réponses est la meilleure approche de la réflexion à ajouter.

La saturation provient d'erreurs corrélatives: le même modèle tend à échouer de la même manière.

>  et provenant d'erreurs associées: le même modèle tend à échouer de la même manière. Si chaque échantillon partage le même point de vue, plus de échantillons n'aident pas. Débat par agent forcé 面对分歧打破相关性.

Le débat brise la saturation. Au lieu de N échantillons indépendants d'un modèle, N agents lisent les raisonnements et réviser les uns des autres. La corrélation entre les échantillons diminue (ils ne sont plus i.i.d.), et le point de convergence est souvent correct où le vote i.i.d était en toute confiance erroné.

> Le débat a brisé 和── non pas en obtenant N 个独立样本从一个模型, mais en permettant à N 个代理阅读彼此的推理并修改── les liens entre les échantillons diminuent, elles ne sont plus indépendantes et distribuées, les points de réception sont généralement corrects, tandis que les votes indépendants et distribués font confiance à l'erreur──

La relation décorelle est le mécanisme.Lorsque les agents voient le raisonnement d'autres agents, ils ne peuvent s'empêcher de s'y engager  soit pour défendre leur position, soit pour la mettre à jour.Cette participation forcée produit des informations qu'aucun échantillonnage d'i.i.d. ne peut.

> Lorsque l'agent voit la réflexion d'un autre agent, il doit participer soit à la défense de sa position, soit à la mise à jour. Cette participation forcée ne peut produire de quantités indépendantes et de distribution de données.

## Concept Le concept central

### L'algorithme du Du et al. 2023

Le rapport de référence est le résultat de l'analyse de l'impact de l'exploitation sur les ressources humaines.

> Le rapport de référence est le cas pour les produits de l'industrie de l'électricité.

L'algorithme est intentionnellement simple: pas de rôles spéciaux, pas de juge, pas de modérateur. Chaque agent est symétrique. La seule asymétrie est l'ordre de qui parle en premier, et même cela se dissipe sur plusieurs tours.

> 算法有意简单: pas de rôle particulier, pas de juge, pas de présentateur. Chaque agent est le premier à parler.

1. Chacun des N agents produit une réponse initiale à la question.
   En français, le premier mot de la réponse est " agent ".
2. Pour la ronde r = 2..R: chaque agent est montré les réponses de r-1 des autres agents et demandé "en tenant compte de ces, donnez votre réponse mise à jour".
   Pour la première r = 2..R: chaque agent  voir les autres agents
3. Après les ronde R, votez à la majorité les réponses finales.
   Après le R 轮, la majorité des votes est votée pour l'opinion finale.

Les tests papier sur MMLU, GSM8K, biographies, MATH et références factuelles.

> Le débat se poursuit au-delà du CoT et du réflexe personnel.

La suite de référence couvre à la fois le raisonnement (MATH, GSM8K  problèmes avec des réponses correctes vérifiables) et la réalité (biographies  revendications vérifiables contre Wikipedia).

> 基准套件涵盖推理(MATH、GSM8K有可验证正确答案问题) 和事实性(传记可对照维基百科 检查的声明) ∼ Factutaire augmentation est le résultat du titre: Débat est la méthode la plus bon marché connue pour réduire les problèmes de réalité ∼

### Deux boutons indépendants

Ablations du même document:

> Comme un article de l'expérience de désintégration:

- **Agent count alone**Le nombre de personnes qui ont été affectées par les travaux de la Commission est de 0,5% en fonction des besoins de la Commission.
  Le mot grec traduit par " le mot grec "**仅 Agent 数量**(1 round, N's majority vote) Sur la plupart des tâches, il est meilleur que le seul agent, mais atteint la plateforme.
- **Round count alone**1 agent qui voit son propre raisonnement préalable) aide à peine à la faiblesse connue de la réflexion.
  Le mot grec traduit par " le mot grec "**仅轮数**(1 agent voir soi-même précédemment) peu d'aide.
- **Both together**L'échange multi-rounds entre plusieurs agents conduit au gain.
  Le mot grec traduit par " le mot grec "**两者结合** une augmentation significative.  des échanges de plusieurs agents ont entraîné des bénéfices.

### Pourquoi ça marche ?

Deux mécanismes:

> Œuvre de la Commission

Les deux mécanismes sont composés: l'exposition aux désaccords fournit de nouvelles informations; les erreurs décorrélées empêchent la moyenne des nouvelles informations de se traduire par une mauvaise réponse.

> ∆ Deux mécanismes sont complexes: exposer à des différences fournissant de nouvelles informations; ∆er correcter des erreurs empêchant de nouvelles informations d'être moyennées à des erreurs dans les réponses.

1. **Exposure to disagreement.**Lorsqu'un agent voit la chaîne de raisonnement d'un autre agent avec une conclusion différente, il doit soit justifier ou mettre à jour.
   Le mot grec traduit par " le mot grec "**暴露于分歧。**Lorsqu'un agent voit un autre agent avec une chaîne de délibération différente, il doit soit prouver soit mettre à jour.
2. **Correlated error reduction.**En auto-cohérence, tous les échantillons proviennent du même modèle, de sorte que les erreurs corrélent  vous moyenne dans une réponse en toute confiance.
   Le mot grec traduit par " le mot grec "**相关错误减少。**Dans l'auto-cohérence, tous les échantillons proviennent du même modèle, donc l'erreur est liée à la moyenne.

### Débat hétérogène

A-HMAD et les suivis connexes utilisent *modèles de base différents* pour différents agents. Le débat Llama + Claude + GPT réduit l'effondrement de la monoculture (leçon 26) parce que les erreurs corrélatives d'une famille de modèles ne sont pas partagées par les autres.

> A-HMAD 和相关后续工作为不同 Agent 使用*不同的基础模型*──Llama + Claude + GPT 辩论减少单一文化崩(Lesson 26),因为一个模型族的相关错误不被其他模型族共享──

L'argument d'erreur-décorrélation est le même derrière les méthodes ensemble dans la ML classique: les modèles divers échouent différemment, donc le vote est plus fiable.

> 错误去相关论点与经典ML中的集成方法背后的相同: la diversité des modèles échoue de différentes manières, de sorte que le vote est plus fiable.

L'inconvénient: un modèle faible participant à un débat peut entraîner le consensus vers sa mauvaise réponse (voir " Devrions-nous devenir fous ? ", arXiv:2311.17371).

> 缺点: un modèle faible du débat participant peut faire le concours de la réaction à l'erreur.

Un modèle faible (par exemple, un paramètre Llama 7B) peut dépasser un modèle fort (GPT-4) si le modèle fort se met trop agressivement à jour vers les réponses erronées confiantes du modèle faible. Calibrez les modèles qui participent.

> 异构辩论不是免费多样性──弱模型(如7B 参数 Llama) 可以否决强模型(GPT-4),如果强模型过激进地向弱模型的自信错答案更新──校准哪些模型参与──

### NLSOM  l'extension 129-agent

Zhuge et al. ("Mindstorms in Natural Language-Based Societies of Mind", arXiv:2305.17066) ont étendu cette idée à 129 sociétés membres.

> Zhuge 等人(" Basée sur le langage naturel, la réflexion dans le cœur de la société ", arXiv:2305.17066) va étendre cette idée à 129 membres de la société.

Le résultat de l'échelle est frappant: après ~ 50 agents, les rôles individuels commencent à se spécialiser sans être informés. Certains deviennent des "chercheurs", "autres" critiques, "autres" synthétiseurs. " C'est une différenciation de rôle émergente  le même phénomène observé dans les organisations humaines, qui se produit maintenant dans les sociétés de LLM.

> Les résultats de l'expansion sont remarquables: après plus de 50 agents, les rôles individuels commencent à se spécialiser dans des situations non reconnues. Certains deviennent des " chercheurs "、 d'autres " critiques "、 d'autres " complèteurs ".

### Mode d'échec

- **Sycophancy cascade.**Tous les agents se délaissent à ce qui semble le plus confiant. Le débat s'effondre à la voix la plus forte.
  Le mot grec traduit par " le mot grec "**谄媚级联。**Tout agent se soumet à l'agent le plus confiant qui puisse paraître.
- **Topic drift.**Les débats sur plusieurs tours dérivent de la question initiale.
  Le mot grec traduit par " le mot grec "**主题漂移。**Débat de plusieurs rounds sur la question originale: mesures de réinsertion
- **Compute blowup.**N agents x R rounds = N*R LLM appels, chacun avec un contexte qui croît. Un débat de 5 agents, 5 rounds est de 25 appels dans un contexte croissant. Le coût par question peut dépasser 10 fois un appel CoT unique.
  Le mot grec traduit par " le mot grec "**计算爆炸。**N 个代理 x R 轮 = N*R 次 LLM 调用,每次的上下文都在增长──5 个代理、5 轮的辩论是25 次调用,上下文不断增长──每一个问题的成本可能超过单次CoT 调用的10倍──

## Construisez-le et mettez-le en œuvre.
```figure
multi-agent-debate
```

## Faites-le

`code/main.py`Il y a un débat de 3 agents x 3 rondes sur une question mathématique où chaque agent commence par une réponse différente (peut-être fausse).

> `code/main.py`Dans une question mathématique, 3 agents x 3 débats, chaque agent commence par une réponse différente.

La démo montre deux effets clés:

> La présentation a montré deux effets clés:

- Une seule ronde d'échange rapproche les agents de la bonne réponse.
  En français, le mot "agent" est traduit par "agent".
- Les tours supplémentaires après le second tour montrent des rendements diminuant (matches du plateau de Du et al.).
  Le nombre de roues supplémentaires de la deuxième ronde dépasse le chiffre de revenu de la deuxième ronde.

Je vais courir .

```
python3 code/main.py
```

## Utilisez-le avec le cadre de réalisation

`outputs/skill-debate-configurator.md`Il configure un débat pour une nouvelle tâche: nombre d'agents, nombre de tours, hétérogénéité (modèle même contre mixte), attribution de rôle (symétrique contre un adversaire).

> `outputs/skill-debate-configurator.md`Pour le nouveau débat de configure des tâches:Agent numéros, cycles, différences de structure, même modèle contre mélange, répartition de rôles, même modèle contre un opposant.

## Envoyez-le . Produit .

Si vous envoyez le débat:

> Si vous déployez le système de débat:

- **Cap rounds at 3.**Du et al. montrent 3 tours capture la plupart du gain. Plus est le coût, pas la qualité.
  Le mot grec traduit par " le mot grec "**将轮数限制在 3。**Les trois routes ont réalisé la majeure partie des bénéfices.
- **Cap agents at 5.**Au-delà de 5, le contexte et les coûts dominent.
  Le mot grec traduit par " le mot grec "**将 Agent 限制在 5。** Plus de 5 ,  inflation et coût dominant
- **Heterogeneous by default.**Au moins deux modèles de base différents dans la piscine.
  Le mot grec traduit par " le mot grec "**默认异构。**Il y a au moins deux modèles de base différents dans la piscine.
- **Adversarial slot.**Un agent a été incité à discuter, c'est une rupture de la sycophancy.
  Le mot grec traduit par " le mot grec "**对抗角色。**Un agent est invité à résister à tout.
- **Log every round.**Les systèmes de débat qui cachent des tours intermédiaires ne peuvent être débogages ou vérifiés.
  Le mot grec traduit par " le mot grec "**记录每轮。**Le système de débat caché au milieu des séries ne peut être vérifié ou vérifié.

## Les exercices

1. On court .`code/main.py`La convergence supplémentaire s'arrête à quelle ronde ?
   Le mot " l' économie " est traduit par " l' économie ".`code/main.py`Le nombre de tours sera alors fixé à 5 et les bénéfices seront réduits.
2. Ajouter un quatrième agent avec un rôle adversaire: toujours en désaccord avec la majorité actuelle.
   En français, le rôle de l'agent est de se battre contre les autres.
3. Le score de l'accord par round (fraction des agents sur la réponse majoritaire) atteint-il 1,0, et est-ce équivalent à "correct"?
   En français, le nombre de fois où l'on peut écrire est de 1,0.
4. Lisez les ablations du chapitre 4 et répliquez le résultat "agent seulement" contre "ronde seulement" contre "both" en utilisant ce code.
   Le code de réaction est utilisé pour résoudre les problèmes de réaction.
5. Lisez " Devrions-nous devenir fous ? " (arXiv:2311.17371) et énumérez deux variantes de débat au-delà du round-robin  par exemple, dirigées par un juge, en chaîne de débat, adversarielles.
   Le texte de la première partie de la première partie de la première partie de la première partie de la première partie de la deuxième partie de la deuxième partie de la deuxième partie de la deuxième partie de la deuxième partie de la deuxième partie de la deuxième partie de la deuxième partie de la deuxième partie de la deuxième partie de la deuxième partie de la deuxième partie de la deuxième partie de la deuxième partie de la deuxième partie de la deuxième partie de la deuxième partie de la deuxième partie de la deuxième partie de la deuxième partie de la deuxième partie de la deuxième partie de la deuxième partie de la deuxième partie de la deuxième partie de la deuxième partie de la deuxième partie de la deuxième partie de la deuxième partie de la deuxième partie de la deuxième partie de la deuxième partie de la deuxième partie de la deuxième partie de la deuxième partie de la deuxième partie de la deuxième partie de la deuxième partie de la deuxième partie de la deuxième partie de la deuxième partie de la deuxième partie de la deuxième partie de la deuxième partie de la deuxième partie de la deuxième partie de la deuxième partie de la deuxième partie de la deuxième partie de la deuxième partie de la deuxième partie de la deuxième partie de la deuxième partie de la deuxième partie de la deuxième partie de la deuxième partie de la deuxième partie de la deuxième partie de la deuxième partie de la deuxième partie de la deuxième partie de la deuxième partie de la deuxième partie de la deuxième partie de la deuxième partie de la deuxième partie de la deuxième partie de la deuxième partie de la deuxième partie de la deuxième partie de la deuxième partie de la deuxième partie de la deuxième partie de la deuxième partie de la deuxième partie de la deuxième partie de la deuxième partie de la deuxième partie de la deuxième partie de la deuxième partie de la deuxième partie de la deuxième partie de la deuxième partie de la partie de la deuxième partie de la partie de la deuxième partie de la partie de la deuxième partie de la partie de la partie de la deuxième partie de la partie de la partie de la partie de la partie de la deuxième partie de la partie de la partie de la partie de la partie de la partie de la partie de la partie de la partie de la deuxième de la partie de la partie de la partie de la partie de la partie de la partie de la partie de la partie de la partie de la partie de la partie de la partie de la partie de la partie de la partie de la partie de la partie de la partie de la partie de la partie de la partie de la partie de la partie de la partie de la partie de la partie de la partie de

## Les termes clés

| Term | What people say | What it actually means |
|------|----------------|------------------------|
| Society of Mind / 心智社会 | "Minsky's idea" / "Minsky 的想法" | Intelligence as interacting specialists; 1986 framing now operationalized via LLM debate. / 智能作为交互的专家；1986 年的框架现在通过 LLM 辩论实现。 |
| Multi-agent debate / 多 Agent 辩论 | "Agents argue" / "Agent 争论" | N agents propose, critique each other, revise over R rounds, majority-vote. / N 个 Agent 提议、批评彼此、在 R 轮中修改、多数投票。 |
| Consensus / 共识 | "They agree" / "他们一致" | Not epistemic truth — just fraction-on-majority-answer. Can be confidently wrong. / 不是认识论真理——只是多数答案上的比例。可能自信地犯错。 |
| Rounds / 轮次 | "Exchange steps" / "交换步骤" | One round = each agent reads the others and updates once. / 一轮 = 每个 Agent 阅读其他 Agent 并更新一次。 |
| Heterogeneous debate / 异构辩论 | "Mix model families" / "混合模型族" | Using different base models to decorrelate errors. / 使用不同的基础模型来去相关错误。 |
| Sycophancy cascade / 谄媚级联 | "Everyone agrees with the loud one" / "每个人都同意最大声的" | Debate failure where agents defer to the most confident agent regardless of correctness. / 辩论失败，Agent 不顾正确性屈从于最自信的 Agent。 |
| NLSOM | "129-agent society" / "129 Agent 社会" | Natural-language society of mind; Zhuge et al.'s scaled version. / 自然语言心智社会；Zhuge 等人的扩展版本。 |
| Correlated error / 相关错误 | "Same model, same bug" / "相同模型，相同 bug" | Why self-consistency saturates; debate across different views decorrelates. / 自我一致性为什么饱和；不同观点的辩论去相关。 |

## Encore une lecture

- [Du et al. — Improving Factuality and Reasoning in Language Models through Multiagent Debate](https://arxiv.org/abs/2305.14325) le document de référence, ICML 2024
  Le débat sur la réforme des langues et des langues est un débat sur la réforme des langues et des langues.
- [Zhuge et al. — Mindstorms in Natural Language-Based Societies of Mind](https://arxiv.org/abs/2305.17066) 129-agent NLSOM
  Le récit de la rédaction de la Bible est le récit de la rédaction de la Bible.
- [Should we be going MAD? A Look at Multi-Agent Debate Strategies for LLMs](https://arxiv.org/abs/2311.17371) des variantes de débat sur les critères de référence
  En français, traduire par " Nous devrions aller vers la folie "
- [Debate project page](https://composable-models.github.io/llm_debate/) Le code du groupe Du et al., les démos et les détails de l'ablation
  Le débat est un projet de loi qui a été créé par le gouvernement de l'État de l'État de l'État de l'État de l'État de l'État de l'État de l'État de l'État de l'État de l'État de l'État de l'État de l'État de l'État de l'État de l'État de l'État de l'État de l'État de l'État de l'État de l'État de l'État de l'État de l'État de l'État de l'État de l'État de l'État de l'État de l'État de l'État de l'État de l'État de l'État de l'État de l'État de l'État de l'État de l'État de l'État de l'État de l'État de l'État de l'État de l'État de l'État de l'État de l'État de l'État de l'État de l'État de l'État de l'État de l'État de l'État de l'État de l'État de l'État de l'État de l'État de l'État de l'État de l'État de l'État.
