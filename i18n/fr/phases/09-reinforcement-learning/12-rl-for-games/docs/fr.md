# RL pour les jeux  AlphaZero, MuZero, et l'ère du raisonnement LLM  game中的强化学习  AlphaZero、 MuZero et LLM 推理时代

> 1992: TD-Gammon bat les champions humains au backgammon avec une pure TD. 2016: AlphaGo bat Lee Sedol. 2017: AlphaZero domine les échecs, les shogi et le Go à partir de zéro. 2024: DeepSeek-R1 prouve la même recette, avec GRPO remplaçant PPO, fonctionne sur le raisonnement.

> **【中文解读】**游戏是 RL 突破的试验场:TD-Gammon (1992) → AlphaGo (2016) → AlphaZero (2017) → DeepSeek-R1 (2025)。DeepSeek-R1 证明了 AlphaZero's"self-blowing+search+strategy improvement" cycle peut être directement utilisé pour le grand modèle de la théorie mathématique token 就是动作,验证器就是"win/输"信号。

**Type:** Build | **类型:** 动手
**Languages:** Python | **语言:** Python
**Prerequisites:** Phase 9 · 05 (DQN), Phase 9 · 08 (PPO), Phase 9 · 09 (RLHF), Phase 9 · 10 (MARL) | **前置知识:** Phase 9 · 05 (DQN), Phase 9 · 08 (PPO), Phase 9 · 09 (RLHF), Phase 9 · 10 (多智能体 RL)
**Time:** ~120 minutes | **时间:** ~120 分钟

## Le problème , l' introduction du problème

Les jeux ont tout ce que RL veut. Récompense propre (gagnant/perte). Épisodes infinies (auto-jeu réinitialisé). Simulation parfaite (le jeu *est* le simulateur). espaces d'action discrets ou petits en continu. Structure multi-agent qui force la robustesse des adversaires.

> Le jeu possède tout ce dont il a besoin. Il est très facile de se faire une idée de ce que l'on peut faire.

Et les jeux sont la façon dont chaque grande percée RL a été testée. Le projet de loi sur les droits de l'homme (TD-Gammon, 1992) Le projet de loi de 2013 sur les droits de l'homme Le projet de loi de 2006 Le groupe AlphaZero (2017). Le projet de loi de l'Union européenne sur les droits de l'homme (DOT 2, 2019) AlphaStar (StarCraft II, 2019). MuZero (modèle apprenant, 2019). AlphaTensor (multiplication de matrice, 2022). AlphaDev (algorithmes de tri, 2023). DeepSeek-R1 (réasonnement mathématique, 2025)  la dernière démonstration que les techniques de jeu-RL fonctionnent sur le texte.

> Le jeu est pour chaque RL 重大突破的试验场──TD-Gammon(西洋双陆棋,1992)、Atari-DQN(2013)、AlphaGo(2016)、AlphaZero(2017)、OpenAI Five(Dota 2,2019)、AlphaStar(星际争 II,2019)、MuZero(学习模型,2019)、AlphaTensor(矩阵乘法,2022)、AlphaDev(排序算法,2023)、DeepSeek-R1(数学推理,2025)最新证明: le jeu RL 技术可用于文本──

Cette pierre angulaire surveille les trois architectures marquantes  AlphaZero, MuZero et GRPO  à travers un seul objectif unificateur: **self-play + search + policy improvement**. Chacun généralise le précédent; GRPO en particulier est la recette d'AlphaZero appliquée au raisonnement LLM, avec des jetons comme actions et une vérification mathématique comme signal gagnant.

> Cette résolution est prise à travers un seul point de vue**自我博弈+搜索+策略改进**审视三个里程碑架构:AlphaZero、MuZero 和 GRPO──每个都是前一个的推广;GRPO 特别是将 AlphaZero配方应用于LLM 推理,token是动作,数学验证是胜信号──

## Le concept de base.

![AlphaZero ↔ MuZero ↔ GRPO: same loop, different environments](../assets/rl-games.svg)

**The unifying loop.**

```
while True:
    trajectory = self_play(current_policy, search)     # play game against self
    policy_target = search.improved_policy(trajectory) # search improves raw policy
    policy_net.update(policy_target, value_target)     # supervised on search output
```

**AlphaZero (2017).**Silver et al. Un jeu (échecs, shogi, Go) avec des règles connues:

- Réseau de valeur politique: une tour `f_θ(s) → (p, v)`- Je suis là .`p`est un précurseur sur les mouvements juridiques. `v`est le résultat attendu du jeu.
- Monte Carlo Tree Search (MCTS): à chaque mouvement, élargir un arbre de possibilités de continuation.`(p, v)`comme le précédent + la bande de démarrage. Sélectionnez les nœuds par UCB (PUCT): `a* = argmax Q(s, a) + c · p(a|s) · √N(s) / (1 + N(s, a))`- Je suis désolé .
- Jouer à soi-même: jouer à des jeux agent-agent.`t`, la distribution des visites du MCTS `π_t`Il est également possible de faire des efforts pour améliorer la qualité de la formation.
- Perte:`L = (v - z)² - π · log p + c · ||θ||²`- Je suis là .`z`est le résultat du jeu (+1 / 0 / -1).

Zéro connaissance humaine, zéro heuristique artisanale, une recette unique qui maîtrisait les échecs, le shogi et le go après quelques dizaines de millions de jeux d'auto-jouer chacun.

> 零人类知识──零手工启发式── un mécanisme de maîtrise de l'international de l'échec, du jeu de cartes et du jeu de cartes après des milliers de millions de livres de lecture.

**MuZero (2019).**Schrittwieser et al. Supprime l'exigence de connaître les règles.

- Au lieu d'un environnement fixe, apprenez un modèle de dynamique latente.`(h, g, f)`- Le numéro de la liste:
  - `h(s)`: encodez l'observation à un état latent.
  - `g(s_latent, a)`: prédire le prochain état latent + récompense.
  - `f(s_latent)`: prévoir la politique prioritaire + valeur.
- MCTS fonctionne dans l'espace latent appris.
- Fonctionne sur Go, échecs, shogi et Atari, un algorithme, aucune connaissance des règles.

> Dans le jeu de cartes, le jeu de cartes, le jeu de cartes et Atari, il n'y a pas besoin de connaître les règles.

> **【中文解读】**AlphaZero et MuZero ont éliminé cette restriction grâce à l'apprentissage du modèle de mobilité spatiale cachée. Ce cycle de "auto-exploration+ recherche+ stratégie d'amélioration" a directement lancé l'entraînement de la démarche de DeepSeek-R1 avec des récompenses vérifiables pour remplacer le signal de victoire négatif du jeu.

> **【拓展：DeepSeek-R1 与 AlphaZero 范式】**DeepSeek-R1(2025) va appliquer le paradigme d'AlphaZero à la LLM 推理:token就是动作,推理过程就是"游戏",验证器(mathematics题对错、代码是否通过测试)就是"胜负信号"──GRPO 替代PPO,组内采样替代自我博──

**Stochastic MuZero (2022).**Ajout de dynamique stochastique et de nœuds de chance; s'étend aux jeux de classe backgammon.

> **随机 MuZero (2022)。**添加随机动力学和机会节点; étendre à du jeu de cartes bi-terre

**Muesli, Gumbel MuZero (2022-2024).**Amélioration de l'efficacité de l'échantillon et de la recherche déterministe.

> **Muesli、Gumbel MuZero (2022-2024)。**L'amélioration de l'efficacité et de la détermination des recherches de l'échantillon

**GRPO (2024-2025).**La même boucle en forme d'AlphaZero, appliquée au raisonnement du modèle de langage:

- "Jeu": répondre à un problème mathématique / de codage / de raisonnement. "Vincre" = vérificateur (test case passes, correspondances numériques de réponse) renvoie 1.
- Politique: le LLM. Actions: jetons. État: prompt + réponse-jusqu'à présent.
- Aucun critique (PPO-style V_φ). Au lieu de cela, pour chaque prompt, échantillon `G`Les résultats de la politique sont complétés.**group-relative advantage** `A_i = (r_i - mean_r) / std_r`comme signal de mise à jour de style REINFORCE.
- KL pénalité à la politique de référence pour prévenir la dérive (comme RLHF).
- Perte totale:

  `L_GRPO(θ) = -E_{q, {o_i}} [ (1/G) Σ_i A_i · log π_θ(o_i | q) ] + β · KL(π_θ || π_ref)`

Aucun modèle de récompense, aucun critique, aucun MCTS. La base relative au groupe remplace les trois.

> **GRPO (2024-2025)。**Le même cycle de forme AlphaZero, appliqué à des modèles linguistiques, ne nécessite pas de modèle de récompense, critique ou MCTS, le groupe relatif à la ligne de base a remplacé les trois.

> **【中文解读】**GRPO est la nouveauté centrale de DeepSeek-R1: non besoin de critique 网络(省一半内存), utilise la valeur moyenne et la différence de construction en groupe. Pour chaque question, G 个回答, correct answer的优势为正确(增强概率),错误的负面为降低概率 ().

> **【拓展：GRPO→DeepSeek-R1→开源推理革命】**Le processus de formation en quatre étapes de DeepSeek-R1: SFT à froideur → 推理导向 GRPO → 拒绝采样+SFT → 全谱 GRPO──R1-Zero(纯GRPO 无SFT) a prouvé que le LLM peut être réalisé à partir de la théorie de l'école, mais avec des différences de lecture disponibles── expérience de vapeur montre: utiliser la trajectoire de la théorie des enseignants de RL fort pour faire des SFT, par rapport à un petit modèle de RL 效果更好──

**The R1 recipe in full.**DeepSeek-R1 (DeepSeek 2025) est constitué de deux modèles dans un seul document:

> **R1 完整配方。**DeepSeek-R1 est un des deux modèles du thème:

- **R1-Zero.**Commencez par le modèle de base DeepSeek-V3. Pas de SFT. Appliquez GRPO directement avec deux composants de récompense: *récompense de précision* (basée sur des règles  a-t-il analysé la réponse finale au bon nombre / le code a-t-il passé les tests d'unité) et *récompense de format* (a-t-il enveloppé sa chaîne de pensée en `<think>…</think>`Les résultats de la recherche de la méthode de calcul de la méthode de calcul de la méthode de calcul de la méthode de calcul de la méthode de calcul de la méthode de calcul de la méthode de calcul de la méthode de calcul de calcul de la méthode de calcul de calcul de la méthode de calcul de la méthode de calcul de la méthode de calcul de la méthode de calcul de la méthode de calcul de la méthode de calcul de la méthode de calcul de la méthode de calcul de la méthode de calcul de la méthode de calcul de la méthode de calcul de la méthode de calcul de la méthode de calcul de la méthode de calcul de la méthode de calcul de la méthode de calcul de la méthode de calcul de la méthode de calcul de la méthode de calcul de la méthode de calcul de la méthode de calcul de la méthode de calcul de la méthode de calcul de la méthode de calcul de la méthode de calcul de la méthode de calcul de la méthode de calcul de la méthode de calcul de la méthode de calcul de la méthode de calcul de la méthode de calcul de la méthode de calcul de la méthode de calcul de la méthode de calcul de la méthode de calcul de la méthode de calcul de la méthode de calcul de la méthode de calcul de la méthode de calcul de la méthode de calcul de la méthode de calcul de la méthode de calcul de la méthode de calcul de la méthode de calcul de la méthode de calcul de la méthode de calcul de la méthode de calcul de la méthode de calcul de la méthode de calcul de la méthode de calcul de la méthode de calcul de la méthode de calcul de calcul de la méthode de calcul de la méthode de calcul de la méthode de calcul de la méthode de calcul de calcul de la méthode de calcul de la méthode de calcul de la méthode de calcul de la méthode de calcul de la méthode de calcul de calcul de la méthode de calcul de la méthode de calcul de la méthode de la méthode de calcul de la méthode de calcul de calcul de la méthode de calcul de la méthode de calcul de la méthode de calcul de calcul de la méthode de calcul de la méthode de calcul de la méthode de calcul de la méthode de calcul de
- **R1.**Réparer les problèmes de lisibilité de R1-Zero avec un pipeline en quatre étapes:
  1. **Cold-start SFT.**Rassemblez quelques milliers de démonstrations longues de CoT avec un formatage propre.
  2. **Reasoning-oriented GRPO.**Appliquer GRPO avec les récompenses de précision + format plus une récompense de cohérence de langage pour éviter le changement de code.
  3. **Rejection sampling + SFT round 2.**Prenez des trajectories de raisonnement de 600 000 à partir du point de contrôle RL, conservez seulement celles avec des réponses finales correctes et une CoT lisible, et combinez avec 200 000 exemples de SFT non raisonnables (écriture, QA, auto-cognition).
  4. **Full-spectrum GRPO.**Une nouvelle ronde de RL couvrant à la fois le raisonnement (récompenses basées sur les règles) et l'alignement général (récompenses basées sur les préférences d'utilité/impérience).

Le résultat correspond à l'o1 sur l'AIME et MATH-500 à poids ouverts, et est assez petit pour distiller. Le même document libère également six modèles denses distillés (Qwen-1.5B à Llama-70B) en SFT'ing sur les traces de raisonnement de R1  pas de RL chez l'étudiant.

> Le résultat est que les résultats sont en phase avec les résultats de la formation et que les résultats sont en phase avec les résultats de la formation.

**Why GRPO instead of PPO for reasoning.**Trois raisons dans le document DeepSeekMath (février 2024): (1) aucun réseau de valeur à former, réduisant de moitié la mémoire; (2) la ligne de base du groupe gère naturellement la récompense rare de fin de trajectoire que produisent les tâches de raisonnement; (3) la normalisation par prompt rend les avantages comparables sur des problèmes de difficulté très différente, ce que le seul critique de PPO ne peut pas faire.

> **为什么推理用 GRPO 而非 PPO。**Trois raisons: 1) la valeur de formation nécessaire est réduite de moitié; 2) la récompense du rares échanges de données sur les tâches de traitement naturel; 3) chaque proposition de réintégration permet de comparer les avantages dans les grandes difficultés.

**Search-free vs search-based.**Les jeux se sont succédé:

> **Search-free vs search-based.**

- *Jeux d'information parfaits avec de longs horizons* (Go, échecs): toujours basés sur la recherche. AlphaZero / MuZero dominent.
- *Réconciliation LLM*: aucun MCTS n'est encore en production; GRPO sur des déploiements complets, meilleur de N pour le calcul des inférences.

## Construisez-le et mettez-le en œuvre.
```figure
f3-selfplay-ladder
```

## Faites-le

Le code dans `code/main.py`les implémentations **GRPO in miniature**L'algorithme est le même qu'un LLM; seulement la politique et l'environnement sont plus simples. Il enseigne la *perte* et l'avantage relatif au groupe*, qui est l'innovation de 2025.

> `code/main.py`Le code intermédiaire est réalisé**微型 GRPO** un algorithme avec un échantillon de plusieurs groupes 博机── le même que LLM; simplement la stratégie et l'environnement plus simple── il professe* les pertes* et* les avantages par rapport au groupe*, c'est l'innovation de l'année 2025──

### Étape 1: un petit environnement de vérification

```python
QUESTIONS = [
    {"prompt": "q1", "correct": 3},
    {"prompt": "q2", "correct": 1},
]

def verify(prompt_idx, answer_token):
    return 1.0 if answer_token == QUESTIONS[prompt_idx]["correct"] else 0.0
```

Dans le GRPO réel, le vérificateur effectue des tests unitaires ou vérifie l'égalité mathématique.

> Réel GRPO 中验证器运行单元测试或检查数学等式──

### Étape 2: politique: softmax sur K des jetons de réponse par prompt

```python
def policy_probs(theta, p_idx):
    return softmax(theta[p_idx])
```

Équivalent à la production finale d'un LLM conditionné à un prompt.

> L'émission de la dernière étape de la formation est en cours.

### Étape 3: Prélèvement par groupe et avantage par groupe

```python
def grpo_step(theta, p_idx, G=8, beta=0.01, lr=0.1, rng=None):
    probs = policy_probs(theta, p_idx)
    samples = [sample(probs, rng) for _ in range(G)]
    rewards = [verify(p_idx, s) for s in samples]
    mean_r = sum(rewards) / G
    std_r = stddev(rewards) + 1e-8
    advs = [(r - mean_r) / std_r for r in rewards]

    for a, A in zip(samples, advs):
        grad = onehot(a) - probs
        for i in range(len(probs)):
            theta[p_idx][i] += lr * A * grad[i]
    # KL penalty: pull theta toward reference
    for i in range(len(probs)):
        theta[p_idx][i] -= beta * (theta[p_idx][i] - reference[p_idx][i])
```

L'avantage relatif au groupe est le truc DeepSeek 2024. Aucun critique n'est nécessaire.

> 组相对优势是2024年DeepSeek的技巧──无需批判──"基线"是组平均值,归结使用组标准差──

### Étape 4: comparer avec la ligne de base de REINFORCE (sans valeur)

La même configuration, le même calcul, la même force de réaction.

> La même configuration, la même quantité de calcul, la seule force de réaction.

### Étape 5: observez l'entropie et KL

Les mêmes diagnostics que la RLHF: moyenne KL à référence, entropie politique, récompense au-delà du temps.

> Le diagnostic est similaire à celui de la RLHF: moyenne KL à la stratégie de référence, stratégie, récompense au fil du temps.

## Les pièges

- **Reward hacking via verifier gaming.**Le GRPO hérite du risque de la RLHF: si le vérificateur est erroné ou exploitable, le MLL trouvera l'exploit.
  **通过验证器博弈的奖励黑客。**GRPO                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            
- **Group size too small.**La variance de la ligne de base du groupe est la suivante:`1/√G`- Ci-dessous .`G = 4`, le signal d' avantage est bruyant; choix standard est `G = 8`à `64`- Je suis désolé .
  **组大小太小。**Différence de la ligne de base`1/√G`C'est vrai.`G = 4`Les signes de sonorités suivants sont:`G = 8`À la`64`Il y a une autre.
- **Length bias.**Les résultats de LLM de différentes longueurs ont des probabilités de logs différentes.
  **长度偏差。**Les MLL de différentes longitudes ont des probabilités de résultat différentes.
- **Pure self-play cycles.**L'entraînement de style AlphaZero peut être bloqué dans des boucles de domination sur les jeux de somme générale.
  **纯自我博弈循环。**L'entraînement AlphaZero peut être entraîné dans un cycle de contrôle.
- **Search-policy mismatch.**AlphaZero entraîne la politique pour imiter les résultats de recherche. Si le réseau de politique est trop petit pour représenter la distribution de la recherche, la formation est suspendue.
  **搜索-策略不匹配。**AlphaZero trainage 策略模仿搜索输出──如果策略网络太小不能表示搜索分布,训练停滞──
- **Compute floor.**MuZero / AlphaZero nécessite un calcul massif. Une seule ablation est souvent de centaines d'heures de GPU. Des démos miniatures existent (par exemple, AlphaZero sur Connect Four) pour l'apprentissage.
  **计算下限。**MuZero/AlphaZero  nécessite une grande quantité de calcul.
- **Verifier coverage.**Les tests unitaires qui réussissent pour une solution de buggy renforcent le bug.
  **验证器覆盖。**通过有bug 解决方案的单元测试会强化 bug;; conçu pour capturer les conditions de bord de l'épreuve de la situation;.

## Utilisez-le avec le cadre de réalisation

Le paysage du jeu-RL 2026 par domaine:

> 2026 年游戏 RL 版图, selon le domaine:

| Domain | Dominant method |
|--------|-----------------|
| Domain / 领域 | Dominant method / 主导方法 |
| Two-player zero-sum board games (Go, chess, shogi) / 双人零和棋类 | AlphaZero / MuZero / KataGo |
| Imperfect info card games (poker) / 不完全信息纸牌 | CFR + deep learning (DeepStack, Libratus, Pluribus) / CFR + 深度学习 |
| Atari / pixel games / Atari/像素游戏 | Muesli / MuZero / IMPALA-PPO |
| Large multiplayer strategy (Dota, StarCraft) / 大型多人策略 | PPO + self-play + league (OpenAI Five, AlphaStar) |
| LLM math/code reasoning / LLM 数学/代码推理 | GRPO (DeepSeek-R1, Qwen-RL, open replications) |
| LLM alignment / LLM 对齐 | DPO / RLHF-PPO (not GRPO; verifier is preference not verifiable) / DPO/RLHF-PPO |
| Robotics / 机器人 | PPO + DR (not game-RL, but uses same policy-gradient tools) / PPO+DR |
| Combinatorial problems / 组合问题 | AlphaZero variants (AlphaTensor, AlphaDev) / AlphaZero 变体 |

La recette *recipe*  auto-joue, amélioration augmentée par la recherche, distillation de politique  couvre le texte, les pixels et le contrôle physique.

> Cette méthode est le dernier exemple de l'évolution de la technologie.

## Envoyez-le . Produit .

- Je ne sais pas .`outputs/skill-game-rl-designer.md`- Le numéro de la liste:

```markdown
---
name: game-rl-designer
description: Design a game-RL or reasoning-RL training pipeline (AlphaZero / MuZero / GRPO) for a given domain.
version: 1.0.0
phase: 9
lesson: 12
tags: [rl, alphazero, muzero, grpo, self-play]
---

Given a target (perfect-info game / imperfect-info / Atari / LLM reasoning / combinatorial), output:

1. Environment fit. Known rules? Markov? Stochastic? Multi-agent? Informs AlphaZero vs MuZero vs GRPO.
2. Search strategy. MCTS (PUCT with learned prior), Gumbel-sampled, best-of-N, or none.
3. Self-play plan. Symmetric self-play / league / offline data / verifier-generated.
4. Target signal. Game outcome / verifier reward / preference / learned model. Include robustness plan.
5. Diagnostics. Win rate vs baseline, ELO curve, verifier pass rate, KL to reference.

Refuse AlphaZero on imperfect-info games (route to CFR). Refuse GRPO without a trusted verifier. Refuse any game-RL pipeline without a fixed baseline opponent set (self-play ELO is uncalibrated otherwise).
```

## Les exercices

1. **Easy.**Mettre en œuvre le bandit GRPO en `code/main.py`. Traînez sur 2 demandes × 4 jetons de réponse chacun. Converger dans < 1000 mises à jour avec `G=8`- Je suis désolé .
2. **Medium.**Comparer l'efficacité de l'échantillon et la variance de la récompense avec la GRPO sur le même bandit.
3. **Hard.**Prendre une longueur à 2 "chaîne de raisonnement": l'agent émet deux jetons et le vérificateur récompense la paire. Mesurer comment GRPO gère l'attribution de crédit sur deux séquences de étapes. (Conseil: calculer l'avantage du groupe par *sequence complète*, propager aux deux positions de jetons.)

## Les termes clés

| Term | What people say | What it actually means |
|------|-----------------|-----------------------|
| MCTS | "Tree search with learned net" / 蒙特卡洛树搜索 | Monte Carlo Tree Search; UCB1/PUCT selection with learned `(p, v)` priors. |
| AlphaZero | "Self-play + MCTS" / AlphaZero | Policy-value net trained to match MCTS visits and game outcome. |
| MuZero | "Learned-model AlphaZero" / MuZero | Same loop but in latent space via learned dynamics. |
| GRPO | "Critic-free PPO" / 组相对策略优化 | Group Relative Policy Optimization; REINFORCE with group-mean baseline + KL. |
| PUCT | "AlphaZero's UCB" / PUCT 选择公式 | `Q + c · p · √N / (1 + N_a)` — balances value estimate with prior. |
| Self-play | "Agent vs past self" / 自我博弈 | Standard for zero-sum; symmetric training signal. |
| League play | "Population-based self-play" / 联盟训练 | Past + current + exploiters sampled as opponents. |
| Verifier reward | "Verifiable RL" / 验证器奖励 | Reward comes from a deterministic checker (tests pass, answer matches). |
| Process reward | "PRM" / 过程奖励模型 | Scores each reasoning step, not just the final answer. |

## Encore une lecture

- [Silver et al. (2017). Mastering the game of Go without human knowledge (AlphaGo Zero)](https://www.nature.com/articles/nature24270)- Je suis désolé .
- [Silver et al. (2018). A general reinforcement learning algorithm that masters chess, shogi, and Go through self-play (AlphaZero)](https://www.science.org/doi/10.1126/science.aar6404)- Je suis désolé .
- [Schrittwieser et al. (2020). Mastering Atari, Go, chess and shogi by planning with a learned model (MuZero)](https://www.nature.com/articles/s41586-020-03051-4)- Je suis désolé .
- [Vinyals et al. (2019). Grandmaster level in StarCraft II (AlphaStar)](https://www.nature.com/articles/s41586-019-1724-z)- Je suis désolé .
- [DeepSeek-AI (2024). DeepSeekMath: Pushing the Limits of Mathematical Reasoning in Open Language Models (GRPO)](https://arxiv.org/abs/2402.03300) le document qui introduit le GRPO et la référence par groupe.
- [DeepSeek-AI (2025). DeepSeek-R1: Incentivizing Reasoning Capability in LLMs via Reinforcement Learning](https://arxiv.org/abs/2501.12948) la recette R1 complète en quatre étapes plus l'ablation R1-Zero.
- [Brown et al. (2019). Superhuman AI for multiplayer poker (Pluribus)](https://www.science.org/doi/10.1126/science.aay2400) CFR + apprentissage en profondeur à l'échelle.
- [Tesauro (1995). Temporal Difference Learning and TD-Gammon](https://dl.acm.org/doi/10.1145/203330.203343)Le journal qui a tout commencé.
- [Hugging Face TRL — GRPOTrainer](https://huggingface.co/docs/trl/main/en/grpo_trainer) la référence de production pour l'application de GRPO avec des fonctions de récompense personnalisées.
- [Qwen Team (2024). Qwen2.5-Math — GRPO replication](https://github.com/QwenLM/Qwen2.5-Math) réplique ouverte de la recette R1 à plusieurs échelles.
- [Sutton & Barto (2018). Ch. 17 — Frontiers of Reinforcement Learning](http://incompleteideas.net/book/RLbook2020.pdf) le cadre du manuel de lecture pour le jeu personnel, la recherche et la "récompense conçue" que R1 instantie à l'échelle de la maîtrise en droit.
