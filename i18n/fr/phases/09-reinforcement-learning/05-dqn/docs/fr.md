# Réseaux de Q profondeur

> 2013: Mnih entraîne un réseau d'apprentissage Q sur des pixels bruts, bat tous les agents RL classiques sur sept jeux Atari. 2015: étendu à 49 jeux, publié dans Nature, déclenche l'ère de la profondeur RL. DQN est Q-apprentissage plus trois astuces qui rendent l'approximation de fonction stable.

> **【中文解读】**DQN = Q-learning + réseau neuronal + trois techniques de stabilisation (expérimentation de réaction, objectif réseau, coupure de récompense) ⋅ 2013-2015 sur Atari 游戏击败了所有经典RL 方法,开启了深度RL 时代──

**Type:** Build | **类型:** 动手
**Languages:** Python | **语言:** Python
**Prerequisites:** Phase 3 · 03 (Backpropagation), Phase 9 · 04 (Q-learning, SARSA) | **前置知识:** Phase 3 · 03 (反向传播), Phase 9 · 04 (Q-learning, SARSA)
**Time:** ~75 minutes | **时间:** ~75 分钟

## Le problème , l' introduction du problème

L'apprentissage de Q tabulaire nécessite une valeur Q distincte pour chaque paire (état, action). Une planche d'échecs a ~1043 états. Un cadre Atari est 210 × 160 × 3 = 100 800 caractéristiques.

> Le tableau Q-learning  nécessite pour chaque état,动作) pour un stock unique une valeur Q。 un jeu de chess international a environ 1043 états。 un Atari  a 210×160×3 = 100,800 états。 le tableau RL dans des milliers d'états est déjà en panne, plus sans dire des milliards 。

La solution est évidente en arrière-plan: remplacer la table Q par un réseau neural,`Q(s, a; θ)`. Mais l'approximation des fonctions naïves avec l'apprentissage Q diverge sous la " triade mortelle "  approximation des fonctions + démarrage + apprentissage hors politique. Mnih et al. (2013, 2015) ont identifié trois astuces d'ingénierie qui stabilisent l'apprentissage:

> La solution est simple: utiliser le réseau neuronal.`Q(s, a; θ)`替换 Q 表――但这个"简单"花了几十年――简单的函数近似与Q-learning 在"致命三要素"下会发散函数近似 +自举 +离策略学习――Mnih 等人(2013、2015) a déterminé trois techniques d'ingénierie de l'apprentissage stable:

1. **Experience replay**déco-corrélate les transitions.
   **经验回放**打破转移的时间相关性──
2. **Target network**gelant la cible du démarrage.
   **目标网络**结自举目标──
3. **Reward clipping**normalizes les magnitudes de gradient.
   **奖励裁剪**归一化梯度级级──

DQN sur Atari est la première fois qu'une seule architecture avec un seul ensemble d'hyperparamètres a résolu des dizaines de problèmes de contrôle à partir de pixels bruts. Tout ce qui est "deep-RL" construit depuis DDQN, Rainbow, Dueling, Distribution, R2D2, Agent57  est empilé sur cette base de trois tours.

> Le DQN d'Atari est le premier à utiliser une seule architecture et un seul superparamètres ensemble pour résoudre des dizaines de problèmes de contrôle à partir de la première image.

> **【中文解读】**"Trois éléments mortels": fonction proche + auto-élever + 离策略 → 训练不稳定甚至发散──DQN trois techniques ont résolu ce problème:

> **【拓展：经验回放→RLHF】**L'idée de l'expérience de retour (Expérience Replay) est présente dans les formations de LLM: le buffer de l'entraînement PPO, les données préférées du RLHF, les données de l'offre de DPO sont en fait "détruire la connectivité des données, refaire usage de l'expérience".

## Le concept de base.

![DQN training loop: env, replay buffer, online net, target net, Bellman TD loss](../assets/dqn.svg)

**The objective.**Le DQN réduit au minimum la perte de TD en une étape sur une fonction Q neuronale:

`L(θ) = E_{(s,a,r,s')~D} [ (r + γ max_{a'} Q(s', a'; θ^-) - Q(s, a; θ))² ]`

`θ`= réseau en ligne, mis à jour à chaque étape par déclin de gradient. `θ^-`= réseau cible, copié périodiquement à partir de `θ`(à chaque 10 000 pas). `D`= tampon de répétition des transitions passées.

> **目标。**DQN, la perte de la TD sur la fonction Q.`θ`= On se retrouve sur le net, chaque étape passe par la progression.`θ^-`= 目标网络, périodiquement depuis `θ`Il est aussi possible de faire une commande de la même manière.`D`= 过去转移的回放缓冲区──

**The three tricks, in order of importance:**

> **三个技巧，按重要性排序：**

**Experience replay.**Un tampon de bague de `~10⁶`Les transitions de formation sont effectuées par des équipes de formation qui ont des échantillons de type mini par lots aléatoires.

> **经验回放。**Une zone de réparation de l'environnement est déployée à 106 reprises. Chaque étape de formation est déployée à un petit nombre de reprises.

**Target network.**En utilisant le même réseau `Q(·; θ)`Les deux côtés de l'équation Bellman font que la cible se déplace à chaque mise à jour  " chasse à sa propre queue. " La solution: garder un deuxième réseau `Q(·; θ^-)`avec des poids gelés.`C`Pas, copie `θ → θ^-`Cela stabilise la cible de régression pour des milliers d'étapes de gradient à la fois.`θ^- ← τ θ + (1-τ) θ^-`(utilisés dans le DDPG, SAC) sont une variante plus lisse.

> **目标网络。**Dans l'équation Bellman, les deux parties utilisent le même réseau pour que chaque mise à jour soit en mouvement.`C`步复制 `θ → θ^-`◊ soft update(DDPG、SAC 中使用) est un type de variante plus simple.

**Reward clipping.**Les magnitudes de récompense Atari varient de 1 à 1000+.`{-1, 0, +1}`Faut quand la récompense importe, c'est bien pour Atari quand il ne s'agit que de signes.

> **奖励裁剪。**Atari  Prix de la catégorie de 1 à 1000+ pas etc.`{-1, 0, +1}` empêcher toute éventuelle évolution du jeu.

**Double DQN.**Hasselt (2016) corrige le biais de maximisation: utilisez le net en ligne pour * sélectionner* l'action, le net cible pour * l'évaluer*.

`target = r + γ Q(s', argmax_{a'} Q(s', a'; θ); θ^-)`

Le remplacement est toujours mieux.

> **双重 DQN。**Hasselt (2016) 修复最大化偏差:用在线网络*选择*动作,用目标网络*评估*它──直接替换,始终更好──默认使用──

**Other improvements (Rainbow, 2017):**réplique prioritaire (échantillons de transitions à forte TD-erreur plus), architecture duel (separé `V(s)`Les résultats obtenus sont: les réseaux bruyants (exploration apprise), les retours en n étapes, la distribution Q (C51/QR-DQN), le démarrage en plusieurs étapes.

> **其他改进（Rainbow, 2017）：**优先回放、决斗架构、噪声网络、n 步回报、分布式 Q、多步自举── chaque amélioration contribue à plusieurs centaines de points;收益大致可叠加──

> **【拓展：Rainbow DQN 与集成改进】**Rainbow DQN(2017) va intégrer ensemble 6 types de DQN: priorité expérience recharge, dueling architecture, noise network exploration, n'étape de réception, Q apprentissage distribué, plusieurs étapes de réception. Chaque type de modification contribue à améliorer les performances de plusieurs centaines de points, le résultat de la combinaison est notable.

## Construisez-le et mettez-le en œuvre.
```figure
f3-dqn-stability
```

## Faites-le

Le code ici est stdlib-only numpy-free  nous utilisons un MLP à couche cachée roulée à la main sur un petit continu GridWorld, donc chaque étape d'entraînement se déroule en microsecondes. L'algorithme est identique à Atari DQN à l'échelle.

> Le code ici est uniquement utilisé dans une base de données standard dans un micro réseau GridWorld.

### Étape 1: tampon de répétition

```python
class ReplayBuffer:
    def __init__(self, capacity):
        self.buf = []
        self.capacity = capacity
    def push(self, s, a, r, s_next, done):
        if len(self.buf) == self.capacity:
            self.buf.pop(0)
        self.buf.append((s, a, r, s_next, done))
    def sample(self, batch, rng):
        return rng.sample(self.buf, batch)
```

~ 50 000 de capacité pour Atari; 5 000 suffisent pour notre environnement de jouets.

> Atari a besoin de 50 000 places, notre environnement de jeu est suffisant pour 5 000.

### Étape 2: un petit réseau Q (MLP manuel)

```python
class QNet:
    def __init__(self, n_in, n_hidden, n_actions, rng):
        self.W1 = [[rng.gauss(0, 0.3) for _ in range(n_in)] for _ in range(n_hidden)]
        self.b1 = [0.0] * n_hidden
        self.W2 = [[rng.gauss(0, 0.3) for _ in range(n_hidden)] for _ in range(n_actions)]
        self.b2 = [0.0] * n_actions
    def forward(self, x):
        h = [max(0.0, sum(w * xi for w, xi in zip(row, x)) + b) for row, b in zip(self.W1, self.b1)]
        q = [sum(w * hi for w, hi in zip(row, h)) + b for row, b in zip(self.W2, self.b2)]
        return q, h
```

Pass avant: linéaire → ReLU → linéaire.

> Il est également connu pour être le plus grand de la série.

### Étape 3: mise à jour du DQN

```python
def train_step(online, target, batch, gamma, lr):
    grads = zeros_like(online)
    for s, a, r, s_next, done in batch:
        q, h = online.forward(s)
        if done:
            y = r
        else:
            q_next, _ = target.forward(s_next)
            y = r + gamma * max(q_next)
        td_error = q[a] - y
        accumulate_grads(grads, online, s, h, a, td_error)
    apply_sgd(online, grads, lr / len(batch))
```

La forme est Q-apprentissage de la leçon 04 avec deux différences: a) nous nous rapprochons par un différenciable `Q(·; θ)`au lieu d'indiquer un tableau, b) les utilisations cibles `Q(·; θ^-)`- Je suis désolé .

> 形式 et le Q-learning de la leçon 04 sont similaires, mais il y a deux différences:`Q(·; θ)`Controverses et non-indications`Q(·; θ^-)`Il y a une autre.

### Étape 4: boucle extérieure

Pour chaque épisode, agissez avec avidité.`Q(·; θ)`, poussez les transitions dans le tampon, prenez un échantillon d'un minibatch, faites un pas de gradient, synchronisez périodiquement`θ^- ← θ`Le modèle:

```python
for episode in range(N):
    s = env.reset()
    while not done:
        a = epsilon_greedy(online, s, epsilon)
        s_next, r, done = env.step(s, a)
        buffer.push(s, a, r, s_next, done)
        if len(buffer) >= batch:
            train_step(online, target, buffer.sample(batch), gamma, lr)
        if steps % sync_every == 0:
            target = copy(online)
        s = s_next
```

Sur notre petit GridWorld avec un état unique de 16 dimensions, l'agent apprend une politique presque optimale en environ 500 épisodes. sur Atari, élargir à 200M cadres et ajouter un extracteur de fonctionnalités CNN.

> Dans notre réseau réseau à 16 dimensions, le système intelligent est à environ 500 reprises et apprend à se rapprocher des stratégies les plus efficaces.

## Les pièges

- **Deadly triad.**L'approximation des fonctions + hors politique + démarrage peut diverger. DQN atténue avec la mise en réseau cible + répétition; ne supprimez pas les deux.
  **致命三要素。**函数近似+离策略+自举可能发散──DQN 通过目标网络+回放缓解; ne pas déplacer aucun one──
- **Exploration.**Le Q-net doit se décomposer, généralement de 1,0 à 0,01 au cours des premières ~10% de l'entraînement.
  **探索。**ε 必须 décliner, généralement de 1,0 à 0,01, couvrant environ 10% de l'entraînement.
- **Overestimation.** `max`Le Q bruyant est partial.
  **过估计。**Pour les questions de bruit`max`Réalisation de la production en utilisant le double DQN
- **Reward scale.**Clip ou normaliser les récompenses; la magnitude du gradient est proportionnelle à la magnitude de la récompense.
  **奖励尺度。**Récompenses de réduction ou d'intégration; degré de qualité et degré de qualité de la récompense en équivalence.
- **Replay buffer coldstart.**Ne vous entraînez pas avant que le tampon ait quelques milliers de transitions.
  **回放缓冲区冷启动。**La zone de réadaptation a été reprise par plusieurs milliers de personnes.
- **Target sync frequency.**Trop fréquent ≈ pas de filet cible; trop rare ≈ cibles obsolètes. Atari DQN utilise 10 000 étapes env. Règle générale: synchronisez chaque 1/100 de l'horizon d'entraînement.
  **目标同步频率。**太频繁≈没有目标网络;太不频繁≈过时目标――Législation de l'expérience: chaque 1/100 训练视野同步一次――
- **Observation preprocessing.**L'Atari DQN empile 4 images pour faire l'état Markov.
  **观测预处理。**Atari DQN 堆叠 4 使状态满足马尔可夫性──任何有速度信息的环境都需要堆叠或循环状态──

## Utilisez-le avec le cadre de réalisation

En 2026, DQN est rarement à la pointe de la technologie mais reste l'algorithme de référence hors politique:

> En 2026, le DQN est très peu avancé, mais reste un indicateur de l'algorithme stratégique:

| Task | Method of choice | Why not DQN? |
|------|------------------|--------------|
| Task / 任务 | Method of choice / 首选方法 | Why not DQN? / 为什么不用 DQN？ |
| Discrete-action Atari-like / 离散动作类 Atari | Rainbow DQN or Muesli | Same framework, more tricks. / 相同框架，更多技巧。 |
| Continuous control / 连续控制 | SAC / TD3 (Phase 9 · 07) | DQN has no policy network. / DQN 没有策略网络。 |
| On-policy / high-throughput / 在线策略/高吞吐 | PPO (Phase 9 · 08) | No replay buffer; easier to scale. / 无回放缓冲区；更易扩展。 |
| Offline RL / 离线 RL | CQL / IQL / Decision Transformer | Conservative Q targets, no bootstrapping blowups. / 保守 Q 目标，无自举爆炸。 |
| Large discrete action spaces (recommender) / 大离散动作空间（推荐） | DQN with action embedding, or IMPALA | Fine; decoration matters. / 可行；细节很重要。 |
| LLM RL / LLM RL | PPO / GRPO | Sequence-level, not step-level; different loss. / 序列级而非步级；不同损失。 |

Les leçons sont toujours en cours. La lecture et les réseaux cibles apparaissent dans SAC, TD3, DDPG, SAC-X, le tampon de lecture automatique d'AlphaZero et toutes les méthodes de RL hors ligne.

> Ces expériences sont toujours valides. Les retours et les objectifs du réseau sont maintenant présentés dans les méthodes de RL de SAC, TD3, DDPG, SAC-X et AlphaZero.

## Envoyez-le . Produit .

- Je ne sais pas .`outputs/skill-dqn-trainer.md`- Le numéro de la liste:

```markdown
---
name: dqn-trainer
description: Produce a DQN training config (buffer, target sync, ε schedule, reward clipping) for a discrete-action RL task.
version: 1.0.0
phase: 9
lesson: 5
tags: [rl, dqn, deep-rl]
---

Given a discrete-action environment (observation shape, action count, horizon, reward scale), output:

1. Network. Architecture (MLP / CNN / Transformer), feature dim, depth.
2. Replay buffer. Capacity, minibatch size, warmup size.
3. Target network. Sync strategy (hard every C steps or soft τ).
4. Exploration. ε start / end / schedule length.
5. Loss. Huber vs MSE, gradient clip value, reward clipping rule.
6. Double DQN. On by default unless explicit reason to disable.

Refuse to ship a DQN with no target network, no replay buffer, or ε held at 1. Refuse continuous-action tasks (route to SAC / TD3). Flag any reward range > 10× per-step mean as needing clipping or scale normalization.
```

## Les exercices

1. **Easy.**On court .`code/main.py`Combien d'épisodes avant que la moyenne de course dépasse -10 ?
2. **Medium.**Désactiver le réseau cible (utiliser le réseau en ligne pour les deux côtés de la cible Bellman). Mesurer l'instabilité de l'entraînement  est-ce que le retour oscille ou diverge?
3. **Hard.**Ajouter le double DQN: utilisez le réseau en ligne pour choisir `argmax a'`Les résultats de l'analyse de la recherche ont été évalués en fonction des résultats obtenus.`Q(s_0, best_a)`contre vrai `V*(s_0)`Après 1000 épisodes avec vs sans Double DQN sur un grille-World.

## Les termes clés

| Term | What people say | What it actually means |
|------|-----------------|-----------------------|
| DQN | "Deep Q-learning" / 深度Q网络 | Q-learning with a neural Q-function, replay buffer, and target network. |
| Experience replay | "Shuffled transitions" / 经验回放 | Ring buffer sampled uniformly each gradient step; decorrelates data. |
| Target network | "Frozen bootstrap" / 目标网络 | Periodic copy of Q used in the Bellman target; stabilizes training. |
| Deadly triad | "Why RL diverges" / 致命三要素 | Function approximation + bootstrapping + off-policy = no convergence guarantee. |
| Double DQN | "Fix for maximization bias" / 双重DQN | Online net selects action, target net evaluates it. |
| Dueling DQN | "V and A heads" / 决斗DQN | Decompose Q = V + A - mean(A); same output, better gradient flow. |
| Rainbow | "All the tricks" / Rainbow | DDQN + PER + dueling + n-step + noisy + distributional in one. |
| PER | "Prioritized Replay" / 优先经验回放 | Sample transitions proportional to TD-error magnitude. |

## Encore une lecture

- [Mnih et al. (2013). Playing Atari with Deep Reinforcement Learning](https://arxiv.org/abs/1312.5602) le document d'atelier de 2013 sur NeurIPS qui a déclenché la RL profonde.
- [Mnih et al. (2015). Human-level control through deep reinforcement learning](https://www.nature.com/articles/nature14236) le journal Nature, 49 jeux de DQN.
- [Hasselt, Guez, Silver (2016). Deep Reinforcement Learning with Double Q-learning](https://arxiv.org/abs/1509.06461) DDQN.
- [Wang et al. (2016). Dueling Network Architectures](https://arxiv.org/abs/1511.06581)- Le duel de DQN.
- [Hessel et al. (2018). Rainbow: Combining Improvements in Deep RL](https://arxiv.org/abs/1710.02298)- Le papier de trucs empilés.
- [OpenAI Spinning Up — DQN](https://spinningup.openai.com/en/latest/algorithms/dqn.html) exposition moderne claire.
- [Sutton & Barto (2018). Ch. 9 — On-policy Prediction with Approximation](http://incompleteideas.net/book/RLbook2020.pdf) le traitement manuel de la "triade mortelle" (approximation des fonctions + démarrage + hors politique) que le réseau cible et le tampon de lecture de DQN sont conçus pour dompter.
- [CleanRL DQN implementation](https://docs.cleanrl.dev/rl-algorithms/dqn/) DQN de référence à fichier unique utilisé dans les études d'ablation; bon à lire à côté de la version originale de cette leçon.
