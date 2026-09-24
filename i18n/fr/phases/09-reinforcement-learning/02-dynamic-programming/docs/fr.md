# Programming dynamique  Iteration de politique et Iteration de valeur  动态规划  策略代与价值代

> La programmation dynamique est RL avec tricherie. Vous connaissez déjà les fonctions de transition et de récompense; vous faites simplement l'équation Bellman jusqu'à ce que`V`ou `π`Il s'agit de la référence à laquelle chaque méthode basée sur l'échantillonnage tente de s'approcher.

> **【中文解读】**Le programme est une fonction de "transaction et de récompense" de l'environnement connu, il suffit de répéter l'équation Bellman jusqu'à la réception.

**Type:** Build | **类型:** 动手
**Languages:** Python | **语言:** Python
**Prerequisites:** Phase 9 · 01 (MDPs) | **前置知识:** Phase 9 · 01 (MDP)
**Time:** ~75 minutes | **时间:** ~75 分钟

## Le problème , l' introduction du problème

Vous avez un MDP avec un modèle connu: vous pouvez demander `P(s' | s, a)`et `R(s, a, s')`Un gestionnaire d'inventaire connaît la distribution de la demande. un jeu de société a des transitions déterministes. un monde de grille est quatre lignes de Python. vous avez un * modèle *.

> Vous avez un modèle connu de MDP: vous pouvez demander à tout état-motion de l'action`P(s' | s, a)`et `R(s, a, s')` Le gestionnaire de stockage sait la demande de distribution  Le jeu de cartes a une certaine transition  Le réseau mondial c'est le four de Python  Vous avez un modèle 

La RL sans modèle (Q-learning, PPO, REINFORCE) a été inventée pour le cas où vous n'avez pas de modèle  vous pouvez seulement échantillonner de l'environnement. Mais quand vous en avez un, il y a des méthodes plus rapides et meilleures: la programmation dynamique. Bellman les a conçues en 1957.

> 无模型 RL(Q-learning、PPO、REINFORCE) est une situation inventée pour le manque de modèle  vous ne pouvez que le prendre de l'environnement. Mais quand vous avez un modèle, il y a des méthodes plus rapides et meilleures:

> **【中文解读】**Lorsque vous connaissez le modèle environnemental (la probabilité de transfert et la fonction de récompense), le plan d'action peut être précisé pour trouver la meilleure stratégie.

> **【拓展：AlphaZero/MCTS】**La recherche de l'arbre de charbon (MCTS) d'AlphaZero est en fait une version différente de la réserve Bellman.

Vous en avez besoin en 2026 pour trois raisons. Premièrement, chaque environnement tabulaire dans la recherche RL (GridWorld, FrozenLake, CliffWalking) est résolu avec DP pour produire la politique standard en or. Deuxièmement, les valeurs exactes vous permettent de déboguer les méthodes d'échantillonnage: si l'estimation de Q-learning pour `V*(s_0)`Troisièmement, les méthodes modernes de RL hors ligne et de planification (MCTS, recherche d'AlphaZero, RL basée sur le modèle dans la phase 9 · 10) répéteront toutes une sauvegarde Bellman sur un modèle appris ou donné.

> Vous en avez besoin en 2026: une raison: une première, une première, une seconde, une autre, une autre.`V*(s_0)`Les résultats de l'étude de la RL sont en train de se dérouler en moyenne.

## Le concept de base.

![Policy iteration and value iteration, side by side](../assets/dp.svg)

**Two algorithms, both fixed-point iteration on Bellman.**

> **两种算法，都是对 Bellman 方程做不动点迭代。**

> **【中文解读】**两种算法都是对贝尔曼方程做不动点代――策略代:交替执行"策略评估"和"策略改进"直到策略不变; 价值代:将两者合并为一步,直接取 max――两者最终收到同一个优值函数 V*――

**Policy iteration.**Alterne deux étapes jusqu'à ce que la politique cesse de changer.

> **策略迭代。**交替执行两个步骤直到策略不再改变──

1. *Évaluation:* politique donnée `π`, calcul`V^π`en appliquant à plusieurs reprises `V(s) ← Σ_a π(a|s) Σ_{s',r} P(s',r|s,a) [r + γ V(s')]`jusqu'à ce qu'il converge.
   * évaluer:* 给定策略 `π`, Répondre à Bellman jusqu' à`V^π`Je suis là.
2. * Amélioration: * accordée `V^π`, faire`π`L' avide W.R.T.`V^π`Le numéro de la liste:`π(s) ← argmax_a Σ_{s',r} P(s',r|s,a) [r + γ V(s')]`- Je suis désolé .
   *改进:* 给定 `V^π`Je vous en prie .`π`Pour le`V^π`Je suis désolé.

La convergence est garantie parce que: a) chaque étape d'amélioration ou conserve `π`la même ou une augmentation stricte `V^π`Pour certains états, (b) l'espace des politiques déterministes est fini. converge habituellement en ~520 itérations extérieures même pour de grands espaces d'état.

> La réception est garantie, parce que chaque fois que l'amélioration est maintenue.`π`Il faut que ce soit strictement augmenté.`V^π`,(b) L'espace de stratégie de détermination est limité.

**Value iteration.**L'évaluation et l'amélioration se fondent en une seule analyse.

`V(s) ← max_a Σ_{s',r} P(s',r|s,a) [r + γ V(s')]`

Répétez jusqu' à `max_s |V_{new}(s) - V(s)| < ε`. Extraire la politique à la fin en prenant l'action avide. Rigoureusement plus rapide par itération  pas de boucle d'évaluation interne  mais généralement besoin de plus d'itérations pour converger.

> **值迭代。**L'évaluation et l'amélioration seront combinées pour une seule analyse. Appliquer le procédé Bellman * le plus optimal*                                                                                                                                                                                                                                                 

**Generalized policy iteration (GPI).**La mise en forme unifiante. La fonction de valeur et la politique sont verrouillées dans une boucle d'amélioration bidirectionnelle; toute méthode qui conduit les deux vers la cohérence mutuelle (itération de valeur asynchrone, itération de politique modifiée, Q-apprentissage, acteur-critique, PPO) est une instance de GPI.

> **【拓展：GPI→PPO/RLHF】**广义策略代 (GPI) est un cadre unifié: Q-learning、Actor-Critic、PPO sont en fait tous des exemples de GPI。 Comprendre le GPI de DP, vous avez déjà compris le cycle de formation RLHF Répondre à ChatGPT Répondre à RLHF Répondre à la conception philosophie。

**Why `γ < 1` matters.**L' opérateur Bellman est un `γ`- contraction dans la norme supérieure: `||T V - T V'||_∞ ≤ γ ||V - V'||_∞`La contraction implique un point fixe unique et une convergence géométrique.`γ < 1`et vous perdez la garantie  vous avez besoin d'un horizon fini ou d'un état terminal d'absorption.

> **为什么 `γ < 1` 很重要。**Bellman est en train de faire des calculs .`γ`- comprimé-mapping. Compression signifie unique inmobilier et la réception.`γ < 1`On a perdu la garantie que vous avez besoin d'un état de confinement.

## Construisez-le et mettez-le en œuvre.
```figure
value-iteration-gamma
```

## Faites-le

### Étape 1: construire le modèle MDP GridWorld

Utilisez le même 4x4 GridWorld de la leçon 01. Nous ajoutons une variante stochastique: avec probabilité `0.1`l'agent glisse dans une direction perpendiculaire aléatoire.

> Utiliser la même 4×4 GridWorld dans le cours 01...`0.1`智能体会滑向随机垂直方向──

```python
SLIP = 0.1

def transitions(state, action):
    if state == TERMINAL:
        return [(state, 0.0, 1.0)]
    outcomes = []
    for direction, prob in action_probs(action):
        outcomes.append((apply_move(state, direction), -1.0, prob))
    return outcomes
```

`transitions(s, a)`renvoie une liste de `(s', r, p)`C'est le modèle entier.

> `transitions(s, a)`Retour`(s', r, p)`C'est le modèle tout entier.

### Étape 2: évaluation des politiques

En raison d' une politique `π(s) = {action: prob}`, répéter l' équation Bellman jusqu' à `V`Arrête de bouger:

> 给定策略 `π(s) = {action: prob}`Il est toujours là.`V`Il est également utilisé pour la fabrication de produits de haute qualité.

```python
def policy_evaluation(policy, gamma=0.99, tol=1e-6):
    V = {s: 0.0 for s in states()}
    while True:
        delta = 0.0
        for s in states():
            v = sum(pi_a * sum(p * (r + gamma * V[s_prime])
                              for s_prime, r, p in transitions(s, a))
                   for a, pi_a in policy(s).items())
            delta = max(delta, abs(v - V[s]))
            V[s] = v
        if delta < tol:
            return V
```

### Étape 3: Amélioration des politiques

Remplacez`π`avec la politique avide W.R.T.`V`Si vous ...`π`Nous sommes au maximum.

> Il va`π`替换为对 `V`La stratégie du cœur.`π`Il n'y a pas de changement, retour.

```python
def policy_improvement(V, gamma=0.99):
    new_policy = {}
    for s in states():
        best_a = max(
            ACTIONS,
            key=lambda a: sum(p * (r + gamma * V[s_prime])
                              for s_prime, r, p in transitions(s, a)),
        )
        new_policy[s] = best_a
    return new_policy
```

### Étape 4: les couture ensemble

```python
def policy_iteration(gamma=0.99):
    policy = {s: "up" for s in states()}   # arbitrary start
    for _ in range(100):
        V = policy_evaluation(lambda s: {policy[s]: 1.0}, gamma)
        new_policy = policy_improvement(V, gamma)
        if new_policy == policy:
            return V, policy
        policy = new_policy
```

Convergence typique sur 4×4: 46 Iterations extérieures.`V*(0,0) ≈ -6`et une politique qui réduit strictement le nombre d'étapes.

> 4x4 上的典型收:4-6 次外层代──输出 `V*(0,0) ≈ -6`Et une stratégie de réduction stricte du nombre de pas.

### Étape 5: Iteration de valeur (version en boucle unique)

```python
def value_iteration(gamma=0.99, tol=1e-6):
    V = {s: 0.0 for s in states()}
    while True:
        delta = 0.0
        for s in states():
            v = max(sum(p * (r + gamma * V[s_prime])
                       for s_prime, r, p in transitions(s, a))
                   for a in ACTIONS)
            delta = max(delta, abs(v - V[s]))
            V[s] = v
        if delta < tol:
            break
    policy = policy_improvement(V, gamma)
    return V, policy
```

Le même point fixe, moins de lignes de code.

> Parallèlement à l'inaction, moins de code.

## Les pièges

- **Forgetting to handle terminals.**Si vous appliquez Bellman à un état d'absorption, il prend toujours une "meilleure action" qui ne change rien.`if s == terminal: V[s] = 0`- Je suis désolé .
  **忘记处理终止状态。**Si Bellman s'intéresse à l'état d'absorption, il choisirait toujours un "meilleur mouvement", mais rien ne changera.`if s == terminal: V[s] = 0`La protection
- **Sup-norm vs L2 convergence.**Utilisation `max |V_new - V|`La garantie théorique est sur la sup-norme.
  **Sup 范数 vs L2 收敛。**Utilisation `max |V_new - V|`La valeur moyenne est la valeur de la valeur de la valeur de la valeur.
- **In-place vs synchronous updates.**Mise à jour `V[s]`La convergence en place (Gauss-Seidel) est plus rapide qu'une convergence séparée.`V_new`Le code de production utilise le code de production.
  **原地更新 vs 同步更新。**Origins et nouveautés `V[s]`(Gauss-Seidel) Comparé à un seul.`V_new`字典(Jacob)收更快──生产代码使用原地更新──
- **Policy ties.**Si deux actions ont la même valeur Q,`argmax`Les deux types de corrections peuvent être modifiés de manière différente à chaque itération, ce qui provoque une oscillation du contrôle "stable de la politique".
  **策略平局。**Si deux mouvements de Q                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        `argmax`Chaque fois, il est possible de briser la plage de manière différente, ce qui entraîne une "stratégie stable" de la réflexion.
- **State-space explosion.**Le DP est `O(|S| · |A|)`Il fonctionne jusqu'à ~ 107 états. Au-delà de cela, vous avez besoin d'approximation de fonction (phase 9 · 05 et plus).
  **状态空间爆炸。**Le DP est à chaque analyse.`O(|S| · |A|)`◊ s'applique à environ 107 个状态──超出这个范围需要函数近似(Phase 9 · 05 起)

## Utilisez-le avec le cadre de réalisation

En 2026, DP est la ligne de base de la précision et la boucle interne des planificateurs:

> En 2026, le DP est le cycle intérieur de la ligne de base et du planificateur:

| Use case | Method |
|----------|--------|
| Use case / 用例 | Method / 方法 |
| Solve a small tabular MDP exactly / 精确求解小型表格 MDP | Value iteration (simpler) or policy iteration (fewer outer steps) / 值迭代（更简单）或策略迭代（更少外层步数） |
| Verify a Q-learning / PPO implementation / 验证 Q-learning/PPO 实现 | Compare to DP-optimal V* on a toy environment / 在玩具环境上与 DP 最优 V* 比较 |
| Model-based RL (Phase 9 · 10) / 基于模型的 RL | Bellman backup on a learned transition model / 在学习的转移模型上做 Bellman 备份 |
| Planning in AlphaZero / MuZero / AlphaZero/MuZero 中的规划 | Monte Carlo Tree Search = async Bellman backup / MCTS = 异步 Bellman 备份 |
| Offline RL (CQL, IQL) / 离线 RL | Conservative Q-iteration — DP with a penalty on OOD actions / 保守 Q 迭代——对 OOD 动作加惩罚的 DP |

Chaque fois que quelqu'un dit "la fonction de valeur optimale", il veut dire "le point fixe DP".`V*`ou `Q*`Dans un journal, imaginez cette boucle.

> Chaque fois que quelqu'un dit " la fonction de valeur optimale ", ils font référence à " DP non mouvement " .`V*`Ou `Q*`Alors, imaginez ce cycle.

## Envoyez-le . Produit .

- Je ne sais pas .`outputs/skill-dp-solver.md`- Le numéro de la liste:

```markdown
---
name: dp-solver
description: Solve a small tabular MDP exactly via policy iteration or value iteration. Report convergence behavior.
version: 1.0.0
phase: 9
lesson: 2
tags: [rl, dynamic-programming, bellman]
---

Given an MDP with a known model, output:

1. Choice. Policy iteration vs value iteration. Reason tied to |S|, |A|, γ.
2. Initialization. V_0, starting policy. Convergence sensitivity.
3. Stopping. Sup-norm tolerance ε. Expected number of sweeps.
4. Verification. V*(s_0) computed exactly. Greedy policy extracted.
5. Use. How this baseline will be used to debug/evaluate sampling-based methods.

Refuse to run DP on state spaces > 10⁷. Refuse to claim convergence without a sup-norm check. Flag any γ ≥ 1 on an infinite-horizon task as a guarantee violation.
```

## Les exercices

1. **Easy.**Exécuter l' itération de la valeur sur le 4×4 GridWorld avec `γ ∈ {0.9, 0.99}`Combien de balais jusqu' à`max |ΔV| < 1e-6`- Imprimé`V*`comme une grille 4x4.
   > **练习1：**Utilisez différents facteurs de réduction pour voir comment la vitesse de réception change.
2. **Medium.**Comparez l'itération de la politique par rapport à l'itération de la valeur sur le GridWorld (probabilité de glissement `0.1`Le nombre: balayage, heure du mur, finale `V*(0,0)`Qui converge plus vite en itérations ?
   > **练习2：**Comparer le nombre de fois et le temps de fonctionnement de la société.
3. **Hard.**Construire une itération de politique modifiée: dans l'étape d'évaluation, exécuter uniquement `k`- Il s'agit d'un plan de recherche.`V*(0,0)`erreur vs `k`pour `k ∈ {1, 2, 5, 10, 50}`Que vous dit la courbe sur l'offre d'évaluation/amélioration ?
   > **练习3：**                                                                                                                                                                                                                                                              

## Les termes clés

| Term | What people say | What it actually means |
|------|-----------------|-----------------------|
| Policy iteration | "DP algorithm" / 策略迭代 | Alternating evaluation (`V^π`) and improvement (greedy `π` w.r.t. `V^π`) until the policy stops changing. |
| Value iteration | "Faster DP" / 值迭代 | Bellman optimality backup applied in one sweep; converges to `V*` geometrically. |
| Bellman operator | "The recursion" / Bellman 算子 | `(T V)(s) = max_a Σ P (r + γ V(s'))`; a `γ`-contraction in sup-norm. |
| Contraction | "Why DP converges" / 压缩映射 | Any operator `T` with `\|\|T x - T y\|\| ≤ γ \|\|x - y\|\|` has a unique fixed point. |
| GPI | "Everything is DP" / 广义策略迭代 | Generalized Policy Iteration: any method driving `V` and `π` to mutual consistency. |
| Synchronous update | "Jacobi-style" / 同步更新 | Use old `V` throughout a sweep; cleanly analyzable but slower. |
| In-place update | "Gauss-Seidel-style" / 原地更新 | Use `V` as it's being updated; converges faster in practice. |

## Encore une lecture

- [Sutton & Barto (2018). Ch. 4 — Dynamic Programming](http://incompleteideas.net/book/RLbook2020.pdf) la présentation canonique de l'itération de la politique et de l'itération de la valeur.
- [Bertsekas (2019). Reinforcement Learning and Optimal Control](http://www.athenasc.com/rlbook.html) traitement rigoureux des arguments de cartographie de contraction.
- [Puterman (2005). Markov Decision Processes](https://onlinelibrary.wiley.com/doi/book/10.1002/9780470316887) l'itération de la politique modifiée et son analyse de convergence.
- [Howard (1960). Dynamic Programming and Markov Processes](https://mitpress.mit.edu/9780262582300/dynamic-programming-and-markov-processes/) le document d'itération de la politique originale.
- [Bertsekas & Tsitsiklis (1996). Neuro-Dynamic Programming](http://www.athenasc.com/ndpbook.html) le pont du DP à l'approximation du DP / RL profond utilisé dans chaque cours ultérieur.
