# Des méthodes d'échantillonnage

> L'échantillonnage est la façon dont l'IA explore l'espace des possibilités.
> La recherche de l'espace est une façon d'explorer l'espace.

**Type:** Build | **类型:** 动手
**Language:**Je suis un Python .**语言:**Python
**Prerequisites:** Phase 1, Lessons 06-07 (Probability, Bayes' Theorem) | **前置知识:** Phase 1, 第 06-07 课（概率、贝叶斯定理）
**Time:** ~120 minutes | **时间:** ~120 分钟

## Objectifs d'apprentissage

- Implémenter à partir de zéro l'échantillonnage inverse de CDF, de rejet et d'importance en utilisant uniquement des nombres aléatoires uniformes
  Utilisation moyenne avec nombre de réalisations à l'inverse du CDF
- Construire des échantillonnages de température, de top-k et de top-p (nucle) pour la génération de jetons de modèle de langage
  构建用于语言模型代币 生成的温度、top-k 和 top-p(nucleus)采样
- Expliquez la réparamétrisation et pourquoi elle permet la répartition par l'échantillonnage dans les VAE
  解释重参数化技巧(Reparametrization Trick) ainsi que pourquoi il peut permettre à l'opération de la VAE de prendre en charge la propagation de l'opération
- Exécuter le MCMC de Metropolis-Hastings pour échantillonner une distribution cible non normalisée
  运行 Metropolis-Hastings MCMC  从未归纳化的目标分布中采样


> **【中文解读】**
> 采样是 AI 探索可能性的方法──LLM 控制文本生成多样性──VAE 采样是 AI 探索可能性的方法──LLM 控制文本生成多样性──VAE 采样是 AI 探索可能性的方法──LLM 控制文本生成多样性──VAE 采样是 AI 探索可能性的方法──LLM 采样是高温的方法──LLM 控制文本生成多样性──VAE 采样是 AI 探索可能性的方法──VAE 采样是 AI 探索的方法──VAE 采样是 AI 探索可能性的方法──LLM 采样是高温的方法──LLM 控制温度/top-k/top-p 控制文本生成多样性──VAE 采样是重参数化技巧让采样可微的.

## Le problème , l' introduction du problème

Un modèle de langage finit de traiter votre demande et produit un vecteur de 50 000 logits, un pour chaque jeton dans son vocabulaire.

> Une fois votre suggestion traitée, vous générez un volume de 50 000 logites, pour chaque jeton dans le tableau de mots.

Si elle choisit toujours le jeton de plus grande probabilité, chaque réponse est identique. Déterministique. ennuyeux. Si elle choisit uniformément au hasard, la sortie est grimaçante. La réponse vit quelque part entre ces extrêmes, et que quelque part est contrôlée par l'échantillonnage.

> Si chaque fois on choisit le plus haut de probabilité, chaque fois on répond à la même certitude, sans discussion. Si chaque fois on choisit le plus haut de probabilité, le résultat est entre les deux extrémités, et le résultat est le contrôle de la stratégie.

Le prélèvement d'échantillons ne se limite pas à la génération de texte. L'apprentissage par renforcement évalue les gradients de la politique en prenant des échantillons. Les VAE apprennent des représentations latentes en prélèvant des échantillons à partir de distributions apprises et en se propagant à travers le hasard. Les modèles de diffusion génèrent des images en prélèvant des échantillons de bruit et en dénonçant de manière itérative. Les méthodes de Monte Carlo estiment les intégrales qui n'ont pas de solution de forme fermée. Les algorithmes MCMC explorent des distributions postérieures de haute dimension qui sont impossibles à énumérer.

> 采样不仅限于文本生成――强化学习通过采样轨迹(轨迹) 来估计策略梯度――VAE 通过从学习到分布中采样并反向传播来学习隐表示――扩散模型通过采样噪声并代去噪声来生成图像――蒙特卡洛方法估算没有解析的积分――MCMC 算法探索无法枚举的高维后验分布――

Chaque système génératif d'IA est un système d'échantillonnage. La stratégie d'échantillonnage détermine la qualité, la diversité et la contrôlabilité de la sortie. Cette leçon construit chaque méthode d'échantillonnage majeure à partir de zéro, à partir de nombres aléatoires uniformes et se terminant par les techniques qui alimentent les LLM modernes et les modèles génératifs.

> Chaque système généré par l'IA est essentiellement un système de prélèvement. La stratégie de prélèvement détermine la qualité, la diversité et la maîtrise des sorties.

## Le concept de base.

> **【中文解读】**
> 采样问题无处不在: 语言模型 语言模型 语言模型 语言模型 语言模型 语言模型 语言模型 语言模型 语言模型 语言模型 语言模型 语言模型 语言模型 语言模型 语言模型 语言模型 语言模型 语言模型 语言 语言 语言 语言 语言 语言 语言 语言 语言 语言 语言 语言 语言 语言 语言 语言 语言 语言 语言 语言 语言 语言 语言 语言 语言 语言 语言 语言 语言 语言 语言 语言 语言 语言 语言 语言 语言 语言 语言 语言 语言 语言 语言 语言 语言 语言 语言 语言 语言 语言 语言 语言 语言 语言 语言 语言 语言 语言 语言 语言 语言 语言 语言 语言 语言 语言 语言 语言 语言 语言 语言 语言 语言 语言 语言 语言 语言 语言 语言 语言 语言 语言 语言 语言 语言 语言 语言 语言 语言 语言 语言 语言 语言 语言 语言 语言 语言 语言 语言 语言 语言 语言 语言 语言 语言 语言 语言 语言 语言 语言 语言 语言 语言 语言 语言 语言 语言 语言 语言 语言 语言 语言 语言 语言 语言 语言 语言 语言 语言 语言 语言 语言 语言 语言 语言 语言 语言 语言 语言 语言 语言 语言 语言 语言 语言 语言 语言 语言 语言 语言 语言 语言 语言 语言 语言 语言 语言 语言 语言 语言 语言 语言 语言 语言 语言 语言 语言 语言 语言 语言 语言 语言 语言 语言 语言 语言 语言 语言 语言 语言 语言 语言 语言 语言 语言 语言 语言 语言 语言 语言 语言 语言 语言 语言 语言 语言 语言 语言 语言 语言 语言 语言 语言 语言 语言 语言 语言 语言 语言 语言 语言 语言 语言 语言 语言 语言 语言 语言 语言 语言 语言 语言 语言 语言

### Pourquoi la prise d'échantillons est importante

L'échantillonnage apparaît dans quatre rôles fondamentaux dans l'IA et l'apprentissage automatique:

> 采样 dans l'IA et l'apprentissage automatique joue quatre rôles fondamentaux:

**Generation.**Les modèles linguistiques, les modèles de diffusion et les GAN produisent tous des résultats par échantillonnage. L'algorithme de prélèvement contrôle directement la créativité, la cohérence et la diversité.

> **生成。**Le modèle de langage, le modèle de diffusion et le GAN sont utilisés pour produire des sorties.

**Training.**Les échantillons de dégradation du gradient stochastique sont des mini-parties. Les échantillons de décapage des neurones pour les désactiver. Les échantillons d'augmentation des données sont des transformations aléatoires.

> **训练。**随机梯度下降(SGD) 采样 mini-batch──Dropout 采样要禁用神经元──数据增强采样随机变换──重要性采样重新加权样样以后降强化学习──PPO、TRPO) 采样方差

**Estimation.**De nombreuses quantités dans ML n'ont pas de solution de forme fermée. La perte attendue sur une distribution de données, la fonction de partition d'un modèle basé sur l'énergie, les preuves de l'inférence bayésienne.

> **估计。**Beaucoup de quantités de ML ne sont pas résolues. Les pertes attendues sur la distribution de données, les fonctions de distribution du modèle d'énergie, les preuves de la hypothèse de Bayes, les estimations de Monte Carlo, en utilisant des échantillons, sont en moyenne approximatives à toutes ces quantités.

**Exploration.**Les algorithmes MCMC explorent les distributions postérieures dans l'inférence bayésienne.

> **探索。**Le MCMC 算法 dans le développement de la recherche 后验分布在贝叶斯推断中.

Le défi principal: vous ne pouvez échantillonner directement que des distributions simples (uniforme, normale). Pour tout le reste, vous avez besoin d'une méthode pour convertir des échantillons simples en échantillons de votre distribution cible.

> 核心挑战: tu peux seulement directement partir de la simple distribution 均分布、正态分布) 中采样. Pour tout autre distribution, tu as besoin d'une méthode qui transformera le simple échantillon en échantillon de la distribution cible.

> **【拓展：LLM 采样策略的工程实践】**
> La température de l'API OpenAI est généralement de 0,0-1,0, le top-p est de 0,9-1,0[6]. La recherche montre que le top-p (nucleus) est supérieur au top-k dans la plupart des tâches, car il peut se adapter à la configuration du code généré par le modèle.

### Prise de l'échantillon aléatoire uniforme

Chaque méthode d'échantillonnage commence ici. Un générateur de nombres aléatoires uniforme produit des valeurs dans [0, 1) où chaque sous-intervalle de longueur égale a la même probabilité.

> Toutes les méthodes de saisie sont à partir de là. Le générateur de nombres moyen génère [0, 1) la valeur moyenne, dont la probabilité que les subzones de longueur aient des similitudes.

```
U ~ Uniform(0, 1)

P(a <= U <= b) = b - a    for 0 <= a <= b <= 1

Properties:
  E[U] = 0.5
  Var(U) = 1/12
```

Pour échantillonner uniformément à partir d'un ensemble distincte d'éléments n, générer U et retourner le sol ((n * U). Pour échantillonner à partir d'une plage continue [a, b], calculer un + (b - a) * U.

> Pour obtenir un échantillon de chaque élément de la collection dispersée, générer U et revenir au sol, il faut calculer un + (b - a) * U。

Le point de vue clé: un seul nombre aléatoire uniforme contient exactement la bonne quantité de chance pour produire un échantillon à partir d'une distribution.

> 关键洞察: un nombre unique de variables contient une probabilité suffisamment large pour produire un échantillon de n'importe quelle distribution.

> **【中文解读】**
> La distribution moyenne est le générateur de nombres à éventuelles variations de toutes sortes de bases. Le générateur de nombres à éventuelles variations de toutes sortes de bases est le générateur de nombres à éventuelles variations de [0,1], comme le fait Mersenne Twister.

### Métode de CDF inverse (échantillonnage en transformation inverse)

La fonction de distribution cumulée (CDF) trace les valeurs en probabilités:

```
F(x) = P(X <= x)

Properties:
  F is non-decreasing
  F(-inf) = 0
  F(+inf) = 1
  F maps the real line to [0, 1]
```

La CDF inverse repère les probabilités à des valeurs. Si U ~ Uniform(0, 1), alors X = F_inverse(U) suit la distribution cible.

> 逆 CDF 将概率映射回值──如果 U ~ Uniform(0, 1), alors X = F_inverse(U) 服从目标分布──

```
Algorithm:
  1. Generate u ~ Uniform(0, 1)
  2. Return F_inverse(u)

Why it works:
  P(X <= x) = P(F_inverse(U) <= x) = P(U <= F(x)) = F(x)
```

**Exponential distribution example:**

```
PDF: f(x) = lambda * exp(-lambda * x),   x >= 0
CDF: F(x) = 1 - exp(-lambda * x)

Solve F(x) = u for x:
  u = 1 - exp(-lambda * x)
  exp(-lambda * x) = 1 - u
  x = -ln(1 - u) / lambda

Since (1 - U) and U have the same distribution:
  x = -ln(u) / lambda
```

Cela fonctionne parfaitement lorsque vous pouvez écrire F_inverse sous forme fermée. Pour la distribution normale, il n'y a pas de CDF inverse de forme fermée, nous utilisons donc d'autres méthodes (Box-Muller, ou approximation numérique).

> Lorsque vous pouvez écrire une expression de résolution de F_inverse, cette méthode est parfaite. Pour la distribution normale, il n'y a pas de forme de résolution contre CDF, donc nous utilisons d'autres méthodes.

**Discrete version:**Pour les distributions discrètes, construisez le CDF comme une somme cumulée, générez U et trouvez le premier indice où la somme cumulée dépasse U.`sample_categorical`Les travaux de la leçon 06.

> **离散版本：**Pour la distribution dispersée, le CDF se construit pour accumuler et générer U, trouver accumulation et pour la première fois surpasser U.`sample_categorical`Le travail de la société

> **【中文解读】**
> 逆 CDF 方法的核心思想:CDF 函数 F(x) Placez la valeur de la variable à la probabilité de [0,1], tandis que sa fonction à la inverse F_inverse 正好反过来把 [0,1] de la moyenne à la valeur de la variable à la valeur de la distribution cible. Cette méthode est précise, mais elle est très efficace, mais elle est préexistante pour que vous puissiez écrire une expression résolue de la fonction à l'opposé.

### Prélèvement d'échantillons de rejet

Lorsque vous ne pouvez pas inverser le CDF mais pouvez évaluer le PDF cible jusqu'à une constante, le prélèvement d'échantillons de rejet fonctionne.

> Quand vous ne pouvez pas demander contre CDF, mais vous pouvez calculer l'objectif PDF (en utilisant un nombre constant de données)

```
Target distribution: p(x)  (can evaluate, possibly unnormalized)
Proposal distribution: q(x)  (can sample from)
Bound: M such that p(x) <= M * q(x) for all x

Algorithm:
  1. Sample x ~ q(x)
  2. Sample u ~ Uniform(0, 1)
  3. If u < p(x) / (M * q(x)), accept x
  4. Otherwise, reject and go to step 1

Acceptance rate = 1/M
```

Plus le M est serré, plus le taux d'acceptation est élevé. Dans les dimensions faibles (1-3), le prélèvement d'échantillons de rejet fonctionne bien. Dans les dimensions élevées, le taux d'acceptation diminue de manière exponentielle parce que la plupart du volume de proposition est rejeté.

> Dans le cadre de la réforme, le taux d'acceptation est de plus en plus élevé.

**Example: sampling from a truncated normal.**Utilisez une proposition uniforme sur la plage tronquée. L'enveloppe M est le maximum du PDF normal dans cette plage.

> **示例：从截断正态分布采样。**Dans la gamme de décomposition, la valeur maximale de la gamme de décomposition est la M.

**Example: sampling from a semicircle.**Proposez uniformément dans le rectangle de bordure. Acceptez si le point tombe à l'intérieur du demi-cercle. C'est ainsi que Monte Carlo calcule pi: le taux d'acceptation est égal au ratio de surface pi/4.

> **示例：从半圆采样。**Si le point tombe dans un demi-circle, il est accepté. C'est la méthode de calcul de pi: le taux d'acceptation est égal à la surface de pi/4[6].

> **【拓展：拒绝采样在粒子滤波中的应用】**
> Le filtre à particules est un algorithme central de suivi des objectifs et de la position des appareils. Il est en fait un moyen de rejeter le prélèvement avec un ensemble de particules.

### Prélèvement d'échantillons d'importance

Parfois, vous n'avez pas besoin d'échantillons de la distribution cible p(x). Vous devez estimer une attente sous p(x), et vous avez des échantillons d'une distribution différente q(x).

> Parfois, vous n'avez pas besoin de prendre des échantillons de la distribution cible, mais d'estimer une attente, alors que vous avez à votre disposition des échantillons d'une autre distribution.

```
Goal: estimate E_p[f(x)] = integral of f(x) * p(x) dx

Rewrite:
  E_p[f(x)] = integral of f(x) * (p(x)/q(x)) * q(x) dx
            = E_q[f(x) * w(x)]

where w(x) = p(x) / q(x)  are the importance weights.

Estimator:
  E_p[f(x)] ~ (1/N) * sum(f(x_i) * w(x_i))    where x_i ~ q(x)
```

C'est essentiel dans l'apprentissage du renforcement. Dans PPO (Proposimal Policy Optimization), vous recueillez des trajectoires dans une vieille politique pi_old mais vous voulez optimiser une nouvelle politique pi_new.

> Ceci est essentiel dans la formation de renforcement. Dans le PPO, vous êtes dans l'ancienne stratégie.

> **【拓展：PPO 中的重要性采样】**
> Le PPO est l'algorithme central de l'entraînement de ChatGPT RLHF. Il est important de modifier la différence de distribution entre les nouvelles stratégies.

La variance de l'estimatrice d'importance de l'échantillonnage dépend de la similarité de q à p. Si q est très différent de p, quelques échantillons obtiennent des poids énormes et dominent l'estimation.

> Si la différence entre q et p est grande, un petit nombre d'échantillons obtiennent un énorme poids et mènent une estimation.

```
E_p[f(x)] ~ sum(w_i * f(x_i)) / sum(w_i)
```

### Évaluation de Monte Carlo

L'estimation de Monte Carlo approximate les intégrales en moyenne des échantillons aléatoires.

> L'estimation de Monte Carlo a permis de déterminer la réception de l'échantillon en moyenne.

```
Goal: estimate I = integral of g(x) dx over domain D

Method:
  1. Sample x_1, ..., x_N uniformly from D
  2. I ~ (Volume of D / N) * sum(g(x_i))

Error: O(1 / sqrt(N))   regardless of dimension
```

Le taux d'erreur est indépendant des dimensions, c'est pourquoi les méthodes de Monte Carlo dominent dans les dimensions élevées où l'intégration basée sur le réseau est impossible.

> Le taux d'erreur n'a rien à voir avec la dimension. C'est pourquoi la méthode Monte Carlo est impossible à réaliser en fonction du réseau.

> **【中文解读】**
> L'essence de la méthode de Monte Carlo: une approximation de l'expectative de la valeur moyenne de l'échantillon au hasard. La grande quantité de lois garantit la réception, et le taux d'erreur O(1/sqrt(N)) n'a rien à voir avec la dimension.

**Estimating pi:**

```
Sample (x, y) uniformly from [-1, 1] x [-1, 1]
Count how many fall inside the unit circle: x^2 + y^2 <= 1
pi ~ 4 * (count inside) / (total count)
```

**Estimating expectations:**

```
E[f(X)] ~ (1/N) * sum(f(x_i))    where x_i ~ p(x)

The sample mean converges to the true expectation.
Variance of the estimator = Var(f(X)) / N
```

### Chaîne de Markov Monte Carlo (MCMC): Métropole-Hastings

Le MCMC construit une chaîne de Markov dont la distribution stationnaire est la distribution cible p ((x). Après suffisamment de pas, les échantillons de la chaîne sont (environ) des échantillons de p ((x).

> MCMC construire une chaîne de Markov, sa distribution stable  Distribution stationnaire  est la distribution cible                                                                                                                                                                                                                                                 

```
Target: p(x)  (known up to a normalizing constant)
Proposal: q(x'|x)  (how to propose the next state given the current state)

Metropolis-Hastings algorithm:
  1. Start at some x_0
  2. For t = 1, 2, ..., T:
     a. Propose x' ~ q(x'|x_t)
     b. Compute acceptance ratio:
        alpha = [p(x') * q(x_t|x')] / [p(x_t) * q(x'|x_t)]
     c. Accept with probability min(1, alpha):
        - If u < alpha (u ~ Uniform(0,1)): x_{t+1} = x'
        - Otherwise: x_{t+1} = x_t
  3. Discard first B samples (burn-in)
  4. Return remaining samples
```

Pour les propositions symétriques (q(x' (x) = q(x)), le rapport est simplifié à p(x')/p(x. C'est l'algorithme original de Metropolis.

> Pour le titre de la proposition, le taux de conversion est simplifié à la valeur de la proposition.

**Why it works.**La règle d'acceptation garantit un équilibre détaillé: la probabilité d'être à x et de se déplacer à x' est égale à la probabilité d'être à x' et de se déplacer à x. L'équilibre détaillé implique que p ((x) est la distribution stationnaire de la chaîne.

> **为什么有效。**                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             

> **【拓展：MCMC 在贝叶斯深度学习中的应用】**
> Le cœur du cadre de calcul bayésien est le MCMC. Les NUTS (No-U-Turn Sampler) sont les variantes MCMC les plus avancées, elles régulent automatiquement le rythme et la direction.

**Practical considerations:**
- Brûlure: rejeter les premiers échantillons avant que la chaîne n'atteigne l'équilibre
  预热期(Burn-in): abandonner la chaîne pour atteindre l'équilibre
- Édiminer: conserver chaque échantillon k-th pour réduire l'autocorrélation
  稀释(Tinnage): chaque échantillon de conserver un pour réduire sa coefficient de
- Équelles: trop petites et la chaîne se déplace lentement (accueil élevé, exploration lente); trop grandes et la plupart des propositions sont rejetées (accueil faible, collée à leur place)
  提议尺度(Proposition Scale): 太小则链移动缓慢( taux d'acceptation élevé mais explorer lent); 太大则大多数提议被拒绝( taux d'acceptation faible,原地不动)
- Le taux d'acceptation optimal pour une proposition gaussienne de grande dimension est d'environ 0,234
  Le taux d'acceptation optimal des propositions de l'établissement de l'établissement de l'établissement est d'environ 0,234

### Prise d'échantillons de Gibbs

Le prélèvement d'échantillons de Gibbs est un cas spécial du MCMC pour les distributions multivariées. Au lieu de proposer un mouvement dans toutes les dimensions à la fois, il met à jour une variable à la fois à partir de sa distribution conditionnelle.

> Le modèle de Gibbs est un exemple particulier du MCMC dans la distribution de plusieurs variables. Il ne se déplace pas simultanément sur toutes les dimensions, mais renouvelle une variable à chaque fois dans la distribution de conditions.

```
Target: p(x_1, x_2, ..., x_d)

Algorithm:
  For each iteration t:
    Sample x_1^{t+1} ~ p(x_1 | x_2^t, x_3^t, ..., x_d^t)
    Sample x_2^{t+1} ~ p(x_2 | x_1^{t+1}, x_3^t, ..., x_d^t)
    ...
    Sample x_d^{t+1} ~ p(x_d | x_1^{t+1}, x_2^{t+1}, ..., x_{d-1}^{t+1})
```

Le prélèvement Gibbs exige que vous puissiez échantillonner à partir de chaque distribution conditionnelle p ((x_i ∈ x_{-i}).
- Réseaux bayésiens: les conditionnels suivent la structure du graphique
  贝叶斯网络: conditions répartis par la structure décidée
- Les mélanges gaussiens: les conditionnels sont gaussiens
  Modèle mixte: conditions de distribution sont élevées
- Modèles d'isage: la condition de chaque tour dépend uniquement de ses voisins
  Ising 模型: chaque situation de rotation est répartie en fonction de son voisin

Le taux d'acceptation est toujours de 1 (toute proposition est acceptée) car l'échantillonnage à partir de la condition exacte satisfait automatiquement l'équilibre détaillé.

> Le taux d'acceptation est toujours de 1 (toutes les propositions sont acceptées), car les conditions de répartition sont automatiquement satisfaites par des conditions précises.

**Limitation.**Lorsque les variables sont fortement corrélées, le prélèvement d'échantillons de Gibbs se mélange lentement parce que la mise à jour d'une variable à la fois ne peut pas faire de grands mouvements diagonales à travers la distribution.

> **局限性。**Lorsque les variables sont très liées, le modèle de Gibbs se mélange très lentement, car chaque fois qu'une seule variable est mise à jour, il est impossible de faire un grand mouvement de contre-angle dans la distribution.

> **【中文解读】**
> Le modèle de Gibbs est un exemple particulier du MCMC: chaque fois, il ne renouvelle qu'une variable, à partir de la distribution des conditions. Parce que chaque échantillon provient d'une distribution des conditions précises, le taux d'acceptation est donc toujours de 100%.

### Prise d'échantillons à température (utilisés dans les LLM)

Les modèles de langage sortent des logits z_1, ..., z_V pour chaque jeton dans le vocabulaire. Softmax les convertit en probabilités.

> 语言模型为词汇表中的每个代币 输出 logits z_1, ..., z_V──Softmax 将将它们转换为概率──Temperature(温度) 在 softmax 之前对 logits 进行缩放:

```
p_i = exp(z_i / T) / sum(exp(z_j / T))

T = 1.0: standard softmax (original distribution)
T -> 0:  argmax (deterministic, always picks highest logit)
T -> inf: uniform (all tokens equally likely)
T < 1.0: sharpens the distribution (more confident, less diverse)
T > 1.0: flattens the distribution (less confident, more diverse)
```

**Why it works.**Diviser les logits par T < 1 amplifie les différences entre les logits. Si z_1 = 2 et z_2 = 1, divisant par T = 0,5 donne z_1/T = 4 et z_2/T = 2, ce qui augmente l'écart. Après softmax, le jeton de logit le plus élevé obtient une part beaucoup plus grande.

> **为什么有效。**Pour les logits, la différence entre les logits est augmentée à T < 1 ⋅ s'il y a z_1 = 2 ⋅ z_2 = 1, pour obtenir z_1/T = 0.5 ⋅ z_1/T = 4 ⋅ z_2/T = 2, la différence est plus grande ⋅ après le softmax, le logit le plus élevé ⋅ obtient une plus grande part ⋅

**In practice:**
- T = 0,0: décoding avide, le mieux pour des questions et réponses factuelles
  贪心解码, le plus adapté à la réalité
- T = 0,3-0,7: légèrement créatif, bon pour la génération de code
  略有创意, adapté à la génération de code
- T = 0,7-1,0: équilibré, bon pour une conversation générale
  均衡, adaptation à la conversation générale
- T = 1,0-1,5: écriture créative, brainstorming
  创意写作、头脑风暴
- T > 1,5: de plus en plus aléatoire, rarement utile
  Ça va être très utile.

La température ne change pas les jetons possibles, elle change la masse de probabilité allouée à chaque jeton.

> La température ne change pas quel token peut être sélectionné.

> **【中文解读】**
> La température est la " rotation " de l' LLM 输出多样性的. T < 1 让分布更尖(更像贪心), T > 1 让分布更平坦(更随机) 。 T → 0 退化为 argmax, T → ∞ 退化为均分布──实际中 T=0.7 est le point d'équilibre le plus courant.

### Prise d'échantillons

Le prélèvement d'échantillons top-k limite le jeu de candidats aux jetons k avec les probabilités les plus élevées, puis renormalise et prélève des échantillons de ce jeu restreint.

> Le top-k 采样将候选集限制为概率最高的 k 个代币, puis être rassemblé并从该受限集合中采样.

```
Algorithm:
  1. Compute softmax probabilities for all V tokens
  2. Sort tokens by probability (descending)
  3. Keep only the top k tokens
  4. Renormalize: p_i' = p_i / sum(p_j for j in top-k)
  5. Sample from the renormalized distribution

k = 1:  greedy decoding
k = V:  no filtering (standard sampling)
k = 40: typical setting, removes long tail of unlikely tokens
```

Le problème: k est fixe indépendamment du contexte. Lorsque le modèle est sûr (un jeton a 95% de probabilité), k = 40 permet encore 39 alternatives. Lorsque le modèle est incertain (la probabilité est répartie sur 1000 jetons), k = 40 coupe les options plausibles.

> Le problème réside dans le fait que le modèle est fixe, non conforme à la variation des textes suivants. Le modèle est très confiant lorsque le modèle est en mesure de choisir un seul token.

### Prélèvement d'échantillons de haut niveau (nucleus)

Le prélèvement d'échantillons top-p ajuste dynamiquement la taille du jeu de candidats. Au lieu de conserver un nombre fixe de jetons, il conserve le plus petit ensemble de jetons dont la probabilité cumulée dépasse p.

> Il ne conserve pas un nombre fixe de jetons, mais conserve une probabilité accumulée supérieure à la plus petite collection de jetons.

```
Algorithm:
  1. Compute softmax probabilities for all V tokens
  2. Sort tokens by probability (descending)
  3. Find smallest k such that sum of top-k probabilities >= p
  4. Keep only those k tokens
  5. Renormalize and sample

p = 0.9:  keeps tokens covering 90% of probability mass
p = 1.0:  no filtering
p = 0.1:  very restrictive, nearly greedy
```

Lorsque le modèle est sûr, le prélèvement de noyau conserve peu de jetons (peut-être 2-3). Lorsque le modèle est incertain, il conserve beaucoup (peut-être 200). Ce comportement adaptatif est la raison pour laquelle le prélèvement de noyau produit généralement un meilleur texte que le top-k.

> Lorsque le modèle a confiance, le noyau 采样 ne conserve que peu de jetons ️ peut 2 个) ️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️

**Common combinations:**
- Température 0,7 + p-supérieur 0,9: bonne réglage général
  Bon réglage général
- Température 0,0 (avid): optimale pour les tâches déterministes
  Le plus adapté à la tâche de détermination
- Température 1.0 + top-k 50: Fan et al. (2018) réglage original du papier
  Fan 等人 (2018) 原论文设置

On peut combiner le top-k et le top-p. Appliquez le top-k d'abord, puis le top-p sur le reste du jeu.

> Top-k 和 top-p peuvent être combinés à l'aide de la première application top-k, puis appliqué sur le reste du ensemble top-p。

### Triche de réparamétrisation (utilisée dans les VAE)

Les autoencoders variatifs (VAE) apprennent en encodant les entrées dans une distribution dans un espace latent, en prélèvant des échantillons à partir de cette distribution et en décodant l'échantillon.

> 变分自编码器(VAE) en introduisant le code pour une distribution dans l'espace caché 、 de cette distribution en utilisant le modèle, puis en le déchiffrant pour revenir à l'apprentissage.

```
Standard sampling (not differentiable):
  z ~ N(mu, sigma^2)

  The randomness blocks gradient flow.
  d/d_mu [sample from N(mu, sigma^2)] = ???
```

Le truc de réparamétrisation sépare la randomisation des paramètres:

> Les techniques de séquestration seront laissées à la fois par défaut et par paramètres:

```
Reparameterized sampling:
  epsilon ~ N(0, 1)          (fixed random noise, no parameters)
  z = mu + sigma * epsilon   (deterministic function of parameters)

  Now z is a deterministic, differentiable function of mu and sigma.
  d(z)/d(mu) = 1
  d(z)/d(sigma) = epsilon

  Gradients flow through mu and sigma.
```

Cela fonctionne parce que N(mu, sigma^2) a la même répartition que mu + sigma * N(0, 1).

> Ceci est donc valable, parce que N(mu, sigma^2) avec mu + sigma * N(0, 1) 具有相同分布──关键洞察:将随机性移移到一个无参数的源 (epsilon),然后将样本表示参数的可微变变──

**In the VAE training loop:**
1. Les sorties de l'encodeur mu et log(sigma^2) pour chaque entrée
2. Pratique de l'épsilon ~ N(0, 1)
3. Computez z = mu + sigma * epsilon
4. Décodez z pour reconstruire l'entrée
5. Propagation en arrière à travers les étapes 4, 3, 2, 1 (possible car l'étape 3 est différenciable)

Sans le truc de réparamétrisation, les VAE ne peuvent pas être formés avec la répartition standard.

>  sans techniques de réparation, la VAE ne peut pas utiliser de formation standard contre la propagation 

> **【拓展：重参数化技巧的广泛应用】**
> Le système de calcul de la répartition stable, DALL-E, est basé sur le système de calcul de la répartition stable, et il est utilisé pour la répartition de la répartition stable.

### Gumbel-Softmax (échantillonnage catégorique différenciable)

La réparamétrisation fonctionne pour les distributions continues (Gaussian). Pour les distributions catégoriques discrètes, nous avons besoin d'une approche différente.

> Les techniques de séquestration sont adaptées à la distribution continue. Pour une distribution de catégories dispersées, nous avons besoin de différentes méthodes.

**The Gumbel-Max trick (non-differentiable):**

```
To sample from a categorical distribution with log-probabilities log(p_1), ..., log(p_k):
  1. Sample g_i ~ Gumbel(0, 1) for each category
     (g = -log(-log(u)), where u ~ Uniform(0, 1))
  2. Return argmax(log(p_i) + g_i)

This produces exact categorical samples.
```

**Gumbel-Softmax (differentiable approximation):**

```
Replace the hard argmax with a soft softmax:
  y_i = exp((log(p_i) + g_i) / tau) / sum(exp((log(p_j) + g_j) / tau))

tau (temperature) controls the approximation:
  tau -> 0:  approaches a one-hot vector (hard categorical)
  tau -> inf: approaches uniform (1/k, 1/k, ..., 1/k)
  tau = 1.0: soft approximation
```

Gumbel-Softmax produit une relaxation continue d'un échantillon discret. La sortie est un vecteur de probabilité (mous one-hot) au lieu d'un hard one-hot. Les gradients circulent à travers le softmax.

> Gumbel-Softmax 产生离散样本的连续松(Continuous Relaxation)。输出是一个概率向量(软一个热) plutôt que硬一个热──梯度可以流过软max──在训练的前向传播中,你可以使用"直通估计器"(Straight-Through Estimator):前向传播使用硬 argmax,反向传播使用软 Gumbel-Softmax 梯度──

**Applications:**
- Variables latentes discrètes dans les VAE
  VAE
- Recherche d'architecture neuronale (choisir des opérations discrètes)
  神经架构搜索 (sélection d'opération)
- Mécanismes d'attention dure
  硬注意力机械
- Apprentissage renforcé par des actions discrètes
  离散动作强化学习 离散动作强化学习

### Pratification stratifiée

L'échantillonnage standard de Monte Carlo peut laisser des lacunes dans l'espace de l'échantillon par hasard.

> Le modèle de modèle peut être laissé dans l'espace de l'échantillon par hasard.

```
Standard Monte Carlo:
  Sample N points uniformly from [0, 1]
  Some regions may have clusters, others gaps

Stratified sampling:
  Divide [0, 1] into N equal strata: [0, 1/N), [1/N, 2/N), ..., [(N-1)/N, 1)
  Sample one point uniformly within each stratum
  x_i = (i + u_i) / N   where u_i ~ Uniform(0, 1),  i = 0, ..., N-1
```

L'échantillonnage stratifié a toujours une variance inférieure ou égale par rapport à la variation standard Monte Carlo:

> Les différences de couches sont généralement inférieures ou égales à celles de la norme Mont-Carlo:

```
Var(stratified) <= Var(standard Monte Carlo)

The improvement is largest when f(x) varies smoothly.
For piecewise-constant functions, stratified sampling is exact.
```

**Applications:**
- Intégration numérique (quasi-Monte Carlo)
  Numéro de valeur
- Divisions de données de formation (assurance de l'équilibre des classes dans chaque pliage)
  训练数据划分(assurer chaque fois le classement équilibré)
- Prélèvement d'importance avec stratification (combinant les deux techniques)
  结合分层的重要性采样
- NeRF (Neural Radiance Fields) utilise des échantillonnages stratifiés le long des rayons de caméra
  NeRF(réaction de la lumière à travers les phases de l'échantillon

### Connexion aux modèles de diffusion

Les modèles de diffusion génèrent des images grâce à un processus d'échantillonnage. Le processus avant ajoute le bruit gaussien à une image sur T étapes jusqu'à ce qu'elle devienne un bruit pur. Le processus inverse apprend à dénoncer, récupérant l'image d'origine étape par étape.

> Le processus de diffusion est de générer des images à travers le processus de prise de vue. Le processus de diffusion est de recréer progressivement le bruit jusqu'à ce qu'il soit devenu un bruit pur.

```
Forward process (known):
  x_t = sqrt(alpha_t) * x_{t-1} + sqrt(1 - alpha_t) * epsilon
  where epsilon ~ N(0, I)

  After T steps: x_T ~ N(0, I)  (pure noise)

Reverse process (learned):
  x_{t-1} = (1/sqrt(alpha_t)) * (x_t - (1 - alpha_t)/sqrt(1 - alpha_bar_t) * epsilon_theta(x_t, t)) + sigma_t * z
  where z ~ N(0, I)

  Each denoising step is a sampling step.
```

Le lien avec les méthodes de cette leçon:
- Chaque étape dénonciatrice utilise le procédé de réparamétrisation (bruit d'échantillon, transformation déterministe appliquée)
  Chaque étape de dégagement du bruit est utilisée avec des techniques de réparation (en utilisant des techniques de recoupement du bruit, de changement de détermination)
- Le programme de bruit {alpha_t} contrôle une forme d'anneillage de température
  噪音调度 {alpha_t} 控制一种形式的温度退火(Temperature Annealing)
- La formation utilise l'estimation de Monte Carlo pour approximer l'ELBO (la limite inférieure des preuves)
  entraînement à l'aide de l'estimation de Montcarlo pour approcher ELBO(Evidence Lower Bound, preuves
- L'échantillonnage ancestral dans les modèles de diffusion est une chaîne de Markov (chaque étape dépend uniquement de l'état actuel)
  L'échantillonnage ancestral est une chaîne de calcul (chaque étape dépend uniquement de l'état actuel).

L'ensemble du processus de génération d'images est un échantillonnage itératif: commencez par le bruit et à chaque étape, prenez un échantillon d'une version légèrement moins bruyante, conditionnée sur le modèle de dénosage appris.

> L'ensemble du processus de production d'images est de la production de sondage: à partir du bruit, à chaque étape, il est basé sur l'apprentissage du modèle de production de sondage, en une version légèrement différente.

## Construisez-le et mettez-le en œuvre.
```figure
monte-carlo-pi
```

## Faites-le

### Étape 1: Prise d'échantillons CDF uniforme et inverse

```python
import math
import random

def sample_uniform(a, b):
    return a + (b - a) * random.random()  # 线性变换：把 [0,1) 映射到 [a,b)

def sample_exponential_inverse_cdf(lam):
    u = random.random()                   # 生成均匀随机数
    return -math.log(u) / lam             # 逆 CDF：x = -ln(u) / lambda
```

Générez 10 000 échantillons exponentiels et vérifiez que la moyenne est 1/lambda.

> Produit 10 000 échantillons de distribution d'indices, la valeur moyenne de l'essai est-elle de 1/lambda ?

### Étape 2: Prélèvement d'échantillons de rejet

```python
def rejection_sample(target_pdf, proposal_sample, proposal_pdf, M):
    while True:                           # 持续采样直到被接受
        x = proposal_sample()             # 从提议分布采样
        u = random.random()               # 均匀随机数用于决定接受/拒绝
        if u < target_pdf(x) / (M * proposal_pdf(x)):  # 接受条件
            return x
```

Utilisez l'échantillonnage de rejet pour tirer d'une distribution normale tronquée.

> Utilisation de l'échantillon de la distribution de l'état de coupe.

### Étape 3: Prélèvement d'importance

```python
def importance_sampling_estimate(f, target_pdf, proposal_pdf, proposal_sample, n):
    total = 0
    for _ in range(n):
        x = proposal_sample()
        w = target_pdf(x) / proposal_pdf(x)
        total += f(x) * w
    return total / n
```

Évaluer E[X^2] sous une distribution normale en utilisant une proposition uniforme.

> Utilisation moyenne de la distribution de propositions estimation normale de la distribution E[X^2]。 comparer avec l'ensemble des réponses (mu^2 + sigma^2)

### Étape 4: Estimation de Monte Carlo de pi

```python
def monte_carlo_pi(n):
    inside = 0
    for _ in range(n):
        x = random.uniform(-1, 1)
        y = random.uniform(-1, 1)
        if x*x + y*y <= 1:
            inside += 1
    return 4 * inside / n
```

### Étape 5: MCMC de la région de Metropolis-Hastings

```python
def metropolis_hastings(target_log_pdf, proposal_sample, proposal_log_pdf, x0, n_samples, burn_in):
    samples = []
    x = x0                                # 初始状态
    for i in range(n_samples + burn_in):
        x_new = proposal_sample(x)        # 从提议分布生成新候选
        log_alpha = (target_log_pdf(x_new) + proposal_log_pdf(x, x_new)  # 计算接受比的对数
                     - target_log_pdf(x) - proposal_log_pdf(x_new, x))
        if math.log(random.random()) < log_alpha:  # 以 min(1, alpha) 的概率接受
            x = x_new
        if i >= burn_in:                  # 丢弃 burn-in 阶段的样本
            samples.append(x)
    return samples
```

Prenons un échantillon de la distribution bimodal (mixture de deux Gaussiens).

> Le détail de la distribution des deux sommets est le suivant:

### Étape 6: Prise d'échantillons par Gibbs

```python
def gibbs_sampling_2d(conditional_x_given_y, conditional_y_given_x, x0, y0, n_samples, burn_in):
    x, y = x0, y0
    samples = []
    for i in range(n_samples + burn_in):
        x = conditional_x_given_y(y)
        y = conditional_y_given_x(x)
        if i >= burn_in:
            samples.append((x, y))
    return samples
```

### Étape 7: Prise d'échantillons à température

```python
def softmax(logits):
    max_l = max(logits)
    exps = [math.exp(z - max_l) for z in logits]
    total = sum(exps)
    return [e / total for e in exps]

def temperature_sample(logits, temperature):
    scaled = [z / temperature for z in logits]  # 温度缩放：除以 T
    probs = softmax(scaled)                      # 计算缩放后的概率分布
    return sample_from_probs(probs)
```

Montrez comment la température modifie la distribution de sortie pour un ensemble de logits de jetons.

> 展示温度如何改变一组代币日志的输出分布──

### Étape 8: Prise d'échantillons en haut et en haut

```python
def top_k_sample(logits, k):
    indexed = sorted(enumerate(logits), key=lambda x: -x[1])
    top = indexed[:k]
    top_logits = [l for _, l in top]
    probs = softmax(top_logits)
    idx = sample_from_probs(probs)
    return top[idx][0]

def top_p_sample(logits, p):
    probs = softmax(logits)
    indexed = sorted(enumerate(probs), key=lambda x: -x[1])
    cumsum = 0
    selected = []
    for token_idx, prob in indexed:
        cumsum += prob
        selected.append((token_idx, prob))
        if cumsum >= p:
            break
    sel_probs = [pr for _, pr in selected]
    total = sum(sel_probs)
    sel_probs = [pr / total for pr in sel_probs]
    idx = sample_from_probs(sel_probs)
    return selected[idx][0]
```

### Étape 9: Réglage de réparamétrisation

```python
def reparam_sample(mu, sigma):
    epsilon = random.gauss(0, 1)          # 标准正态噪声，不含可学习参数
    return mu + sigma * epsilon            # 确定性变换，梯度可流过

def reparam_gradient(mu, sigma, epsilon):
    dz_dmu = 1.0                          # z 对 mu 的梯度恒为 1
    dz_dsigma = epsilon                   # z 对 sigma 的梯度是 epsilon
    return dz_dmu, dz_dsigma
```

Démontre que les gradients circulent à travers l'échantillon réparamétrié mais pas par échantillonnage direct.

> La échelle de démonstration peut être transmise par des échantillons de paramétrage, mais pas directement.

### Étape 10: Gumbel-Softmax

```python
def gumbel_sample():
    u = random.random()
    return -math.log(-math.log(u))

def gumbel_softmax(logits, temperature):
    gumbels = [math.log(p) + gumbel_sample() for p in logits]
    return softmax([g / temperature for g in gumbels])
```

Montrez comment la baisse de la température fait approcher le vecteur de sortie d'un vecteur à chaud.

> 展示降低温度如何使输出趋近一热向量──

Des mises en œuvre complètes avec toutes les visualisations sont en `code/sampling.py`- Je suis désolé .

> L'ensemble de la réalisation de l'ensemble de la visibilité`code/sampling.py`Dans le centre.

## Utilisez-le avec le cadre de réalisation

> **【拓展：扩散模型中的采样工程】**
> Depuis la publication de 2022 , la méthode de prélèvement est passée de 1000 étapes de la DDPM à DDIM、DPM-Solver++ et nécessite seulement 20 à 50 étapes de méthodes.

Avec NumPy et SciPy, les versions de production:

> Utilisation NumPy 和 SciPy de la version de production:

```python
import numpy as np

rng = np.random.default_rng(42)

exponential_samples = rng.exponential(scale=2.0, size=10000)
print(f"Exponential mean: {exponential_samples.mean():.4f} (expected 2.0)")

from scipy import stats
normal = stats.norm(loc=0, scale=1)
print(f"CDF at 1.96: {normal.cdf(1.96):.4f}")
print(f"Inverse CDF at 0.975: {normal.ppf(0.975):.4f}")

logits = np.array([2.0, 1.0, 0.5, 0.1, -1.0])
temperature = 0.7
scaled = logits / temperature
probs = np.exp(scaled - scaled.max()) / np.exp(scaled - scaled.max()).sum()
token = rng.choice(len(logits), p=probs)
print(f"Sampled token index: {token}")
```

Pour les MCMC à grande échelle, utilisez des bibliothèques dédiées:
- PyMC: modélisation bayésienne complète avec NUTS (HMC adaptatif)
  完整的贝叶斯建模, utiliser NUTS(autoadapter HMC)
- émetteur: échantillonneur MCMC ensemble
  集成 MCMC 采样器
- NumPyro/JAX: MCMC accéléré par GPU
  GPU accélération du MCMC

Vous avez construit ça à partir de zéro, maintenant vous savez ce que font les appels de la bibliothèque.

> Vous avez construit ces méthodes depuis le zéro. Maintenant vous savez ce que font les fonctions de la bibliothèque.

## Les exercices

1. Implémenter l'échantillonnage inverse CDF pour la distribution Cauchy. Le CDF est F(x) = 0,5 + arctan(x) / pi. Générer 10 000 échantillons et tracer l'histogramme contre le vrai PDF. Notez les queues lourdes (valeurs extrêmes loin du centre).
   实现柯西分布(Cauchy Distribution) de contre CDF 采样──CDF 为 F(x) = 0,5 + arctan(x) /pi── générer 10 000 个样本并绘制直方图与真实 PDF 对比──注意重尾(远离中心极端值)。

2. Utilisez l'échantillonnage de rejet pour générer des échantillons à partir d'une distribution Beta(2, 5) en utilisant une proposition Uniform(0, 1). Tracer les échantillons acceptés contre le vrai Beta PDF. Quel est le taux d'acceptation théorique?
   Utilisation de l'échantillon de production de la version bêta (Beta) 2, 5) Répartition de l'échantillon de production de la version bêta (Beta) 2, 5) Répartition de la proposition de la version bêta (Beta) 2, 1, 1, 2, 3, 4, 4, 5, 5, 6, 6, 6, 6, 6, 7, 7, 7, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 9, 9, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10,

3. Évaluer l'intégrale de sin ((x) de 0 à pi en utilisant Monte Carlo avec 1,000, 10,000 et 100,000 échantillons. Comparer l'erreur à chaque niveau. Vérifiez que l'erreur est étalée comme O(1/sqrt(N)).
   Utilisation de méthode de calcul de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de

4. Mettre en œuvre Metropolis-Hastings pour échantillonner à partir d'une distribution 2D p ((x, y) proportionnelle à exp ((-(x^2 * y^2 + x^2 + y^2 - 8*x - 8*y) / 2).
   实现 Metropolis-Hastings De 2D 分布 p(x, y) ~ exp(-(x^2*y^2 + x^2 + y^2 - 8x - 8y) /2) 中采样──绘制样本和链的轨迹──尝试不同的提议标准差──

5. Construisez une démo de génération de texte complète: compte tenu d'un vocabulaire de 10 mots avec logits, générez des séquences de 20 jetons en utilisant (a) avide, (b) température = 0,7, (c) top-k = 3, (d) top-p = 0,9.
   构建一个完整的文本生成演示:给定 10 个词的词汇表和logits,使用 (a) 贪心、(b) temperature=0.7、(c) top-k=3、((d) top-p=0.9 生成 20 个代币的序列──比较 5次运行的输出多样性──

## Les termes clés

| Term | What people say | What it actually means |
|------|----------------|----------------------|
| Sampling | "Drawing random values" | Generating values according to a probability distribution. The mechanism behind all generative AI |
| Uniform distribution | "All equally likely" | Every value in [a, b] has equal probability density 1/(b-a). The starting point for all sampling methods |
| Inverse CDF | "Probability transform" | F_inverse(U) converts a uniform sample into a sample from any distribution with known CDF. Exact and efficient |
| Rejection sampling | "Propose and accept/reject" | Generate from a simple proposal, accept with probability proportional to target/proposal ratio. Exact but wastes samples |
| Importance sampling | "Reweight samples" | Estimate expectations under p(x) using samples from q(x) by weighting each sample by p(x)/q(x). Core to PPO in RL |
| Monte Carlo | "Average random samples" | Approximate integrals as sample averages. Error O(1/sqrt(N)) regardless of dimension |
| MCMC | "Random walk that converges" | Construct a Markov chain whose stationary distribution is the target. Metropolis-Hastings is the foundational algorithm |
| Metropolis-Hastings | "Accept uphill, sometimes downhill" | Propose moves, accept based on density ratio. Detailed balance ensures convergence to target distribution |
| Gibbs sampling | "One variable at a time" | Update each variable from its conditional distribution holding others fixed. 100% acceptance rate |
| Temperature | "Confidence knob" | Divides logits by T before softmax. T<1 sharpens (more confident), T>1 flattens (more diverse) |
| Top-k sampling | "Keep the k best" | Zero out all but the k highest-probability tokens, renormalize, sample. Fixed candidate set size |
| Nucleus sampling (top-p) | "Keep the probable ones" | Keep the smallest set of tokens whose cumulative probability exceeds p. Adaptive candidate set size |
| Reparameterization trick | "Move randomness outside" | Write z = mu + sigma * epsilon where epsilon ~ N(0,1). Makes sampling differentiable. Essential for VAE training |
| Gumbel-Softmax | "Soft categorical sampling" | Differentiable approximation to categorical sampling using Gumbel noise + softmax with temperature |
| Stratified sampling | "Forced coverage" | Divide sample space into strata, sample from each. Always lower variance than naive Monte Carlo |
| Burn-in | "Warm-up period" | Initial MCMC samples discarded before the chain reaches its stationary distribution |
| Detailed balance | "Reversibility condition" | p(x) * T(x->y) = p(y) * T(y->x). Sufficient condition for p to be the stationary distribution of a Markov chain |
| Diffusion sampling | "Iterative denoising" | Generate data by starting from noise and applying learned denoising steps. Each step is a conditional sampling operation |

## Encore une lecture

- [Holbrook (2023): The Metropolis-Hastings Algorithm](https://arxiv.org/abs/2304.07010)- un tutoriel détaillé sur les fondations du MCMC
- [Jang, Gu, Poole (2017): Categorical Reparameterization with Gumbel-Softmax](https://arxiv.org/abs/1611.01144)- papier original Gumbel-Softmax
- [Holtzman et al. (2020): The Curious Case of Neural Text Degeneration](https://arxiv.org/abs/1904.09751)- papier d'échantillonnage de noyau (top-p)
- [Kingma & Welling (2014): Auto-Encoding Variational Bayes](https://arxiv.org/abs/1312.6114)- Le papier VAE introduisant le truc de réparamétrisation
- [Ho, Jain, Abbeel (2020): Denoising Diffusion Probabilistic Models](https://arxiv.org/abs/2006.11239)- Le DDPM relie l'échantillonnage à la génération d'images
