# Les processus stochastiques

> Le mathématicien derrière les promenades aléatoires, les chaînes de Markov et les modèles de diffusion.
> Il y a une structure de l'accident.

**Type:** Learn | **类型:** 学习
**Language:**Je suis un Python .**语言:**Python
**Prerequisites:** Phase 1, Lessons 06-07 (probability, Bayes) | **前置知识:** Phase 1, 第 06-07 课（概率、贝叶斯）
**Time:** ~75 minutes | **时间:** ~75 分钟

## Objectifs d'apprentissage

- Simuler des promenades aléatoires 1D et 2D et vérifier l'échelle de déplacement
  模拟一维和二维随机游走,验证位移的 √n 缩放规律
- Construire un simulateur de chaîne Markov et calculer sa distribution stationnaire via une propre composition
  Construire un modèle de chaîne de calcul par caractéristique de décomposition
- Implementer la dynamique MCMC et Langevin de Metropolis-Hastings pour le prélèvement d'échantillons à partir de distributions cibles
  实现 Metropolis-Hastings MCMC 和 Langevin 动力学, du point de vue de la distribution dans le modèle
- Connectez le processus de diffusion avant au mouvement Brownien et expliquez comment le processus inverse génère des données
  En lien avec le mouvement de Browning, expliquer comment le processus de diffusion de l'avant est généré


> **【中文解读】**
> Le processus de diffusion est le processus de génération de bruit. Le processus de diffusion est le processus de génération de bruit.

## Le problème , l' introduction du problème

Beaucoup de systèmes d'IA impliquent le hasard qui évolue au fil du temps, pas le hasard statique, le hasard structuré et séquentiel où chaque étape dépend de ce qui est arrivé avant.

> De nombreux systèmes d'IA sont liés au hasard évoluant au fil du temps.

Les modèles de langage génèrent des jetons un à la fois. Chaque jeton dépend du contexte précédent. Le modèle produit une distribution de probabilité, des échantillons à partir de lui, et passe à autre chose. C'est un processus stochastique.

> 语言模型逐个生成代币――每个代币取决于之前的上下文――模型输出一个概率分布,从中采样,然后继续――这是随机过程――

Les modèles de diffusion ajoutent du bruit à une image étape par étape jusqu'à ce qu'elle devienne pure statique. Ils inversent ensuite le processus, dénonçant étape par étape jusqu'à ce qu'une nouvelle image émerge.

> Le modèle de propagation est progressivement orienté vers l'image, ajoutant du bruit jusqu'à ce qu'il devienne purement statique.

Les agents d'apprentissage de renforcement prennent des actions dans un environnement. Chaque action conduit à un nouvel état avec une certaine probabilité. L'agent suit une politique aléatoire dans un monde aléatoire.

> 强化学习智能体在环境中执行动作──每动作以一定概率导致新状态──智能体在随机世界中遵循随机策略──整个系统是马尔可夫的决策过程──MDP

L'échantillonnage MCMC - la colonne vertébrale de l'inférence bayésienne - construit une chaîne de Markov dont la distribution stationnaire est la partie postérieure dont vous voulez échantillonner.

> Le MCMC est un modèle de base de la théorie de la construction d'une chaîne de marque, dont la répartition est stable et que vous souhaitez utiliser dans la répartition des expériences suivantes.

Tout cela repose sur quatre idées fondamentales:
1. Les promenades aléatoires -- le processus stochastique le plus simple
2. Chaînes de Markov -- structurée au hasard avec une matrice de transition
3. Dynamique de Langevin - descente de gradient avec le bruit
4. Metropolis-Hastings - prélèvement d'échantillons à partir de toute distribution

> Toutes ces choses sont basées sur quatre concepts de base: 1. le plus simple processus de déplacement; 2. la structure de la chaîne de Markov avec la matrice de déplacement; 3. la diminution du niveau de bruit de la dynamique de Langovine; 4. la métropole-Hastings avec la distribution arbitraire.

## Le concept de base.

### Des promenades aléatoires

Commencez à la position 0. À chaque étape, lancez une pièce équitable.

> De la position 0 开始── chaque étape de la mise en place d'une égale pièce de monnaie──正面:向右 (+1)──反面:向左 (-1)──

Après n étapes, votre position est la somme de n valeurs aléatoires +/-1. La position attendue est 0 (la marche est impartiale). Mais la distance attendue de l'origine augmente en sqrt(n).

> n 步后, votre position est n 个随机 ±1 值的求和――期望位置为 0(游走无偏), mais la distance de l'expectation du point d'origine est augmentée √n 

C'est contre-intuitif. La marche est juste - pas de dérive dans les deux sens. Mais avec le temps, il va de plus en plus loin de l'endroit où il a commencé. L'écart standard après n étapes est sqrt(n.

> Il y a un point de décalage entre les deux directions, mais avec le temps, il s'écarte de la position de départ et s'éloigne de la position de départ.

```
Step 0:  Position = 0
Step 1:  Position = +1 or -1
Step 2:  Position = +2, 0, or -2
...
Step 100: Expected distance from origin ~ 10 (sqrt(100))
Step 10000: Expected distance from origin ~ 100 (sqrt(10000))
```

**In 2D**La même échelle s'applique à la distance de l'origine. Le chemin trace un motif fractale.

> **二维情况下**, y'a lieu de voir la probabilité de mouvement à la droite, à la gauche, à la droite, à la droite, à la gauche, à la gauche, à la droite, à la droite, à la gauche, à la gauche, à la gauche, à la gauche, à la gauche, à la gauche, à la gauche, à la gauche, à la gauche, à la gauche, à la droite, à la gauche, à la gauche, à la gauche, à la gauche, à la droite, à la gauche, à la gauche, à la droite, à la gauche, à la gauche, à la droite, à la gauche, à la gauche, à la droite, à la droite, à la gauche, à la gauche, à la droite, à la gauche, à la gauche, à la droite, à la gauche, à la droite, à la gauche, à la droite, à la gauche, à la droite, à la droite, à la gauche, à la gauche, à la droite, à la gauche, à la gauche, à la droite, à la droite, à la droite, à la droite, à la droite, à la droite, et à la gauche.

**Why sqrt(n)?**Chaque étape est +1 ou -1 avec une probabilité égale. Après n étapes, la position S_n = X_1 + X_2 + ... + X_n où chaque X_i est +/-1. La variance de chaque étape est 1, et les étapes sont indépendantes, donc Var(S_n) = n. Déviation standard = sqrt(n.

> **为什么是 √n？**Chaque étape est différente de 1, de sorte que Var(S_n) = n, standard差 = √n。由中心极限定理,S_n/√n 收到标准正态分布。

Cette échelle de n est présente partout dans ML. SGD évalue le bruit comme 1/sqrt(batch_size).

> √n 缩放放在 ML 中无处不在──SGD 噪音按1/√(batch_size) 缩放,嵌入维度按√d 缩放──平方根是独立随机叠加的标志──

**Connection to Brownian motion.**Prenez une marche aléatoire avec la taille des étapes 1/sqrt(n) et n étapes par unité de temps.

> **与布朗运动的联系。**取步长 1/√n、每单位时间 n 步的随机游走──当 n → ∞ 时,游走收到布朗运动 B(t) 一个连续时间过程,B(t) ~ N(0, t) ⋅

Le mouvement brownien est la base mathématique de la diffusion. Il modélise le vibration aléatoire des particules dans un fluide, les fluctuations des prix des actions et - crucialement - le processus sonore dans les modèles de diffusion.

> Le mouvement de Brown est la base mathématique du modèle de propagation. Il décrit le mouvement de la partition dans le corps, les fluctuations du prix des actions, ainsi que le processus de bruit dans le modèle de propagation.

**Gambler's ruin.**Un marcheur aléatoire commençant à la position k, avec des barrières d'absorption à 0 et N. Quelle est la probabilité d'atteindre N avant 0? Pour une marche équitable: P(atteindre N) = k/N. C'est étonnamment simple et élégant. Il se connecte à la théorie des martingales - la marche aléatoire équitable est un martingale (valeur future attendue = valeur actuelle).

> **赌徒破产问题。**La probabilité de l'arrivée de l'équilibre est de 0, et non de 0, et le taux de l'arrivée de l'équilibre est de 0, et le taux de l'arrivée de l'équilibre est de 0, et le taux de l'arrivée de l'équilibre est de 0, et le taux de l'arrivée de l'équilibre est de 0, et le taux de l'arrivée de l'équilibre est de 0, et le taux de l'arrivée de l'équilibre est de 0, et le taux de l'arrivée de l'équilibre est de 0, et le taux de l'arrivée de l'équilibre est de 0, et le taux de l'arrivée de l'équilibre est de 0, et le taux de l'arrivée de l'équilibre est de 0, et le taux de l'arrivée de l'équilibre est de 0, et le taux de l'arrivée de l'arrivée de l'équilibre est de 0, et le taux de l'arrivée de l'arrivée de l'arrivée de l'arrivée de l'arrivée de l'arrivée de l'arrivée de l'arrivée de l'arrivée de l'arrivée de l'arrivée est de 0 est de 0, et de 0, et le taux de l'arrivée est de 0, et de l'arrivée est de 0, et de l'arrivée est de 0, et de 0, et de la moyenne est de 0, et de 0, et de la moyenne est de 0, et de 0, et de la moyenne de la moyenne de 0, et de la moyenne de la moyenne de 0, et de la moyenne de la moyenne de 0, et de la moyenne de la moyenne de la moyenne de la moyenne de 0, et de la moyenne de la moyenne de la moyenne de la moyenne de la moyenne de la moyenne de la moyenne de la moyenne de la moyenne de la moyenne de la moyenne de la moyenne de la moyenne de la moyenne de la moyenne de la moyenne de la moyenne de la moyenne de la moyenne de la moyenne de la moyenne de la moyenne de la moyenne de la moyenne de la moyenne de la moyenne de la moyenne de la moyenne de la moyenne de la moyenne de la moyenne de la moyenne de la moyenne de la moyenne de la moyenne de la moyenne de la moyenne de la moyenne de la moyenne de

### Chaînes de Markov

Une chaîne de Markov est un système qui transite entre les états selon des probabilités fixes.

> La chaîne de Markov est un système de transfert entre les états en fonction de la probabilité fixe. La nature centrale: l'état suivant ne dépend que de l'état actuel, sans lien avec l'histoire.

```
P(X_{t+1} = j | X_t = i, X_{t-1} = ...) = P(X_{t+1} = j | X_t = i)
```

C'est la propriété de Markov. Cela signifie que vous pouvez décrire toute la dynamique avec une matrice de transition P:

> C'est la nature de Markov. Cela signifie que vous pouvez utiliser la matrice de déplacement P pour décrire l'ensemble du mouvement.

```
P[i][j] = probability of going from state i to state j
```

Chaque rangée de P est une somme de 1 (vous devez aller quelque part).

> Tu dois aller quelque part.

**Example -- Weather:**

> **示例——天气：**

```
States: Sunny (0), Rainy (1), Cloudy (2)

P = [[0.7, 0.1, 0.2],    (if sunny: 70% sunny, 10% rainy, 20% cloudy)
     [0.3, 0.4, 0.3],    (if rainy: 30% sunny, 40% rainy, 30% cloudy)
     [0.4, 0.2, 0.4]]    (if cloudy: 40% sunny, 20% rainy, 40% cloudy)
```

Commencez dans n'importe quel état. Après de nombreuses transitions, la distribution des états converge à la distribution stationnaire pi, où pi * P = pi. C'est le propre vecteur gauche de P avec la valeur propre 1.

> Après un changement suffisant, la distribution de l'état est réceptionnée par une distribution stable de π, satisfaisant π·P = π── c'est la valeur de la caractéristique de P à 1 de la valeur de la caractéristique gauche.

Pour la chaîne météorologique, la répartition stationnaire pourrait être [0,53, 0,18, 0,29] -- à long terme, il est ensoleillé 53% du temps, quel que soit l'état de départ.
Pour la chaîne météorologique, la répartition stationnaire est [0,55, 0,18, 0,27] -- à long terme, il est ensoleillé 55% du temps, quel que soit l'état de départ.

> Pour la chaîne météorologique, la répartition stable est [0,53, 0,18, 0,29]  longue durée pour voir 53% du temps clair, sans lien avec l'état de départ.

```mermaid
graph LR
    S["Sunny"] -->|0.7| S
    S -->|0.1| R["Rainy"]
    S -->|0.2| C["Cloudy"]
    R -->|0.3| S
    R -->|0.4| R
    R -->|0.3| C
    C -->|0.4| S
    C -->|0.2| R
    C -->|0.4| C
```

**Computing the stationary distribution.**Il existe deux approches:

1. **Power method**: multipliez une distribution initiale par P à plusieurs reprises.
2. **Eigenvalue method**: trouver le propre vecteur gauche de P avec la valeur propre 1.

> **计算平稳分布。**- Je suis en train de vous dire.**幂法**: Répondre à la distribution initiale par P, suffisamment de fois après la réception.**特征值法**: Demandez la valeur de la caractéristique de P à 1 de la caractéristique gauche de P^T à 1 de la caractéristique droite de P^T)

Les deux approches exigent que la chaîne remplisse les conditions de convergence.

> Les deux méthodes exigent que la chaîne satisfaise les conditions de la réception.

**Convergence conditions.**Une chaîne Markov converge à une distribution stationnaire unique si elle est:
- **Irreducible**: chaque État est accessible depuis chaque autre État
- **Aperiodic**: la chaîne ne cycle pas avec une période fixe

> **收敛条件。**La chaîne de stockage doit être satisfaite à la seule distribution stable:**不可约**(chaque état peut être atteint par l'autre);**非周期**(La chaîne ne sera pas en cycle fixe)

La plupart des chaînes rencontrées dans ML satisfont aux deux conditions.

> La plupart des chaînes rencontrées dans le ML sont à la hauteur de ces deux conditions.

**Absorbing states.**Un état est absorbant si une fois que vous y entrez, vous ne quittez jamais (P[i][i] = 1).

> **吸收状态。**Une fois que vous êtes entré dans un état de non-abandon de jeu, vous avez été en mesure de créer un système de connexion.

**Mixing time.**Combien d'étapes jusqu'à ce que la chaîne soit "close" à la distribution stationnaire? Formellement, le nombre d'étapes jusqu'à ce que la distance totale de variation de la stationarité tombe en dessous d'un certain seuil.

> **混合时间。**链"接近"平稳分布需要多少步骤? 链"接近"平稳分布需要多少步骤? 链"接近"平稳分布需要多少步步? 链"接近"平稳分布需要多少步? 形式上,是与平稳分布的总变差距降低到值以下的步数──快混合 = 步数少──谱间隙(1 -第二大特征值) 控制混合时间:间隙越大,混合越快──

### Connexion avec les modèles linguistiques

La génération de jetons dans un modèle de langage est approximativement un processus de Markov.

> 语言模型的代币 生成近似是一个马尔可夫的过程――给定当前上下文,模型输出下一个代币的概率分布――温度 控制分布的尖度:

```
P(token_i) = exp(logit_i / temperature) / sum(exp(logit_j / temperature))
```

- Température = 1,0: répartition standard
- Température < 1,0: plus nette (plus déterministe)
- Température > 1,0: plus plate (plus aléatoire)
- Température -> 0: argmax (comme l'avidité)

> Température = 1.0 標準分布;<1.0 更尖(更确定性);>1.0 更平坦(更随机);→0 退化为 argmax(贪心解码)

Le prélèvement d'échantillons top-k réduit à k les jetons de plus grande probabilité. Le prélèvement d'échantillons top-p (nucleus) réduit à la plus petite série de jetons dont la probabilité cumulée dépasse p. Les deux modifient les probabilités de transition de Markov.

> Le top-k 采样 conservation probabilité maximale de k 个代币; le top-p 核采样) conservation probabilité cumulée supérieure à la plus petite de p de la sélection de dépôts ⋅ les deux modifications apportées à la probabilité de transfert de Mark ⋅

### Motion brown

La position B ((t) a trois propriétés:
1. B(0) = 0
2. B(t) - B(s) est normalement distribué avec la moyenne 0 et la variance t - s (pour t > s)
3. Les augmentations sur les intervalles non superposés sont indépendantes

> Le nombre de personnes qui ont été déplacées dans le monde entier est de 0,0 à 0,0 à 0,0 à 0,0 à 0,0 à 0,0 à 0,0 à 0,0 à 0,0 à 0,0 à 0,0 à 0,0 à 0,0 à 0,0 à 0,0 à 0,0 à 0,0 à 0,0 à 0,0 à 0,0 à 0,0 à 0,0 à 0,0 à 0,0 à 0,0 à 0,0 à 0,0 à 0,0 à 0,0 à 0,0 à 0,0 à 0,0 à 0,0 à 0,0 à 0,0 à 0,0 à 0,0 à 0,0 à 0,0 à 0,0 à 0,0 à 0,0 à 0,0 à 0,0 à 0,0 à 0,0 à 0,0 à 0,0 à 0,0 à 0,0 à 0,0 à 0,0 à 0,0 à 0,0 à 0,0 à 0,0 à 0,0 à 0,0 à 0,0 à 0,0 à 0,0 à 0,0 à 0,0 à 0,0 à 0,0 à 0,0 à 0,0 à 0,0 à 0,0 à 0,0 à 0,0 à 0,0 à 0,0 à 0,0 à 0,0 à 0, à 0,0 en moyenne moyenne moyenne moyenne moyenne moyenne moyenne moyenne moyenne moyenne moyenne moyenne moyenne moyenne moyenne moyenne moyenne moyenne moyenne moyenne moyenne moyenne moyenne moyenne moyenne moyenne moyenne moyenne moyenne moyenne moyenne moyenne moyenne moyenne moyenne moyenne moyenne moyenne moyenne moyenne moyenne moyenne moyenne moyenne moyenne moyenne moyenne moyenne moyenne moyenne moyenne moyenne moyenne moyenne moyenne moyenne moyenne moyenne moyenne moyenne moyenne moyenne moyenne moyenne moyenne moyenne moyenne moyenne moyenne moyenne moyenne moyenne moyenne moyenne moyenne moyenne moyenne moyenne moyenne moyenne moyenne moyenne moyenne moyenne moyenne moyenne moyenne moyenne moyenne moyenne moyenne moyenne moyenne moyenne moyenne moyenne moyenne moyenne moyenne moyenne moyenne moyenne moyenne moyenne moyenne moyenne moyenne moyenne moyenne moyenne moyenne moyenne moyenne moyenne moyenne moyenne moyenne moyenne moyenne moyenne moyenne moyenne moyenne moyenne moyenne moyenne moyenne moyenne moyenne moyenne moyenne moyenne moyenne moyenne moyenne moyenne moyenne moyenne moyenne moyenne moyenne moyenne moyenne moyenne moyenne moyenne moyenne moyenne moyenne moyenne moyenne moyenne moyenne moyenne moyenne moyenne moyenne moyenne moyenne moyenne moyenne moyenne moyenne moyenne moyenne moyenne moyenne moyenne moyenne moyenne moyenne moyenne moyenne moyenne moyenne moyenne moyenne moyenne moyenne moyenne moyenne moyenne moyenne moyenne moyenne moyenne moyenne moyenne moyenne moyenne moyenne moyenne moyenne moyenne moyenne moyenne moyenne moyenne moyenne moyenne moyenne moyenne moyenne moyenne moyenne moyenne moyenne moyenne moyenne moyenne moyenne moyenne moyenne moyenne moyenne moyenne moyenne moyenne moyenne moyenne moyenne moyenne moyenne moyenne moyenne moyenne moyenne moyenne moyenne moyenne moyenne moyenne moyenne moyenne moyenne moyenne moyenne moyenne moyenne moyenne moyenne moyenne moyenne moyenne moyenne moyenne moyenne moyenne moyenne moyenne moyenne moyenne moyenne moyenne moyenne moyenne moyenne moyenne moyenne moyenne moyenne moyenne moyenne moyenne

Le mouvement brownien est continu mais nulle part différenciable - il se balance à chaque échelle.

> Le mouvement de Browne est continuel mais il est indétectable. Il est en mouvement à chaque dimension.

Dans une simulation discrète, on approche le mouvement brownien par:

```
B(t + dt) = B(t) + sqrt(dt) * z,    where z ~ N(0, 1)
```

L'échelle sqrt (dt) est importante. Elle vient du théorème de limite centrale appliqué aux promenades aléatoires.

> 离散仿真中用 B(t+dt) = B(t) + √dt × z 近似布朗运动(z ~ N(0,1))

### Dynamique de Langevin

La dynamique de Langevin trouve la distribution de probabilité proportionnelle à exp ((-U ((x) / T), où U est une fonction d'énergie et T est la température.

> 梯度下降找函数最小值──Langevin 动力学找概率分布  exp(-U(x)/T), dont U est une fonction d'énergie, T est la température──

```
x_{t+1} = x_t - dt * gradient(U(x_t)) + sqrt(2 * T * dt) * z_t
```

Deux forces agissent sur la particule:
1. **Gradient force**(-dt * gradient(U)): pousse vers une faible énergie (comme la descente du gradient)
2. **Random force**(sqrt(2*T*dt) * z): pousse dans des directions aléatoires (exploration)

> 两种力作用在粒子上:1. **梯度力**推向低能量 (à une échelle de plus en plus basse); 2. **随机力**推向随机方向 (à l'exploration)

À température T = 0, c'est une descente de gradient pure. À haute température, c'est presque une marche aléatoire. À la bonne température, la particule explore le paysage énergétique et passe plus de temps dans les régions à faible énergie.

> La température T=0 时是纯梯度下降──高温时近似随机游走──合适的温度下, les particules explorent le paysage énergétique et restent plus longtemps dans la région de la faible énergie──

**Connection to diffusion models.**Le processus avancé d'un modèle de diffusion est le suivant:

```
x_t = sqrt(alpha_t) * x_{t-1} + sqrt(1 - alpha_t) * noise
```

C'est une chaîne de Markov qui mélange progressivement les données avec le bruit.

> 扩散模型的前向过程:x_t = √α_t × x_{t-1} + √(1-α_t) × noise── c'est un lien de bruit progressif, assez long après x_T 变为纯高斯噪音──

Le processus inverse - passer du bruit à la data - est aussi une chaîne de Markov, mais ses probabilités de transition sont apprises par un réseau neuronal. Le réseau apprend à prédire le bruit qui a été ajouté à chaque étape, puis le soustrait.

> Le processus inversé de retour du bruit vers les données est également une chaîne de rotation, mais la probabilité de transfert est apprise par le réseau de neurones.

```mermaid
graph LR
    subgraph "Forward Process (add noise)"
        X0["x_0 (data)"] -->|"+ noise"| X1["x_1"]
        X1 -->|"+ noise"| X2["x_2"]
        X2 -->|"..."| XT["x_T (pure noise)"]
    end
    subgraph "Reverse Process (denoise)"
        XT2["x_T (noise)"] -->|"neural net"| XR2["x_{T-1}"]
        XR2 -->|"neural net"| XR1["x_{T-2}"]
        XR1 -->|"..."| XR0["x_0 (generated data)"]
    end
```

### MCMC: Chaîne de Markov à Monte Carlo

Parfois, vous devez échantillonner à partir d'une distribution p ((x) que vous pouvez évaluer (jusqu'à une constante) mais ne peut pas échantillonner directement.

> Parfois, vous avez besoin d'un calcul possible (mais en manque de calcul) mais vous ne pouvez pas prendre directement la distribution de la taille de la taille de la taille de la taille de la taille de la taille de la taille de la taille de la taille de la taille de la taille de la taille de la taille de la taille de la taille de la taille de la taille de la taille de la taille de la taille de la taille de la taille de la taille de la taille de la taille de la taille de la taille de la taille de la taille de la taille de la taille de la taille de la taille de la taille de la taille de la taille de la taille de la taille de la taille de la taille de la taille de la taille de la taille de la taille de la taille de la taille de la taille de la taille de la taille de la taille de la taille de la taille de la taille de la taille de la taille de la taille de la taille de la taille de la taille de la taille de la taille de la taille de la taille de la taille de la taille de la taille de la taille de la taille de la taille de la taille de la taille de la taille de la taille de la taille de la taille de la taille de la taille de la taille de la taille de la taille de la taille de la taille de la taille de la taille de la taille de la taille de la taille de la taille de la taille de la taille de la taille de la taille de la taille de la taille de la taille de la taille de la taille de la taille de la taille de la taille de la taille de la taille de la taille de la taille de la taille de la taille de la taille de la taille de la taille de la taille de la taille de la taille de la taille de la taille de la taille de la taille de la taille de la taille de la taille de la taille de la taille de la taille de la taille de la taille de la taille de la taille de la taille de la taille de la taille de la taille de la taille de la taille de la taille de la taille de la taille de la taille de la taille de la taille de la taille de la taille de la taille de la taille de la taille de la taille de la taille de la taille de la taille de la taille de la taille de la taille de la taille de la taille de la taille de la taille de la taille de la taille de la taille de la taille de la taille de la taille de la taille

**Metropolis-Hastings**construit une chaîne de Markov dont la distribution stationnaire est p ((x):

1. Commencez à une position x
2. Proposer une nouvelle position x' à partir d'une distribution de proposition Q(x'
3. Ratio d'acceptation de calcul: a(x') * Q(x
4. Acceptez x' avec probabilité min ((1, a).
5. Je répète.

> **Metropolis-Hastings**构建一个平稳分布为 p(x) 的马尔可夫链:1) 从某点 x 出发;2) 从提议分布 Q(x'就是x) 提出新位置 x';3) 计算接受率 a = p(x') Q(x'就是x') /(p(x) Q(x'就是x));4) 以概率 min(1,a) 接受,否则停留;5) 重复.

Si Q est symétrique par exemple, Q(x' ( ( ( ( () ), Q(x (x) = N(x, sigma^2)), le rapport se simplifie à a = p(x') / p(x. Vous n'avez besoin que du rapport des probabilités - les constantes normalisantes annulent.

> Si Q pour les nombres ((comme高斯), le taux d'acceptation est simplifié à = p(x')/p(x) ⋅ il suffit que la probabilité de la résolution des nombres ordinaires soit automatiquement supprimée, c'est la raison pour laquelle le MCMC est si utile pour les expériences de base.

La chaîne est garantie de converger à p*x dans des conditions douces. Mais la convergence peut être lente si la proposition est trop petite (marche aléatoire) ou trop grande (rejettion élevée).

> Dans les conditions de température et de sécurité, la réception est un peu trop faible, mais la réception peut être trop lente.

**Why it works.**Le rapport d'acceptation garantit un équilibre détaillé: la probabilité d'être à x et de se déplacer à x' est égale à la probabilité d'être à x' et de se déplacer à x. L'équilibre détaillé implique que p(x) est la distribution stationnaire de la chaîne.

> **为什么有效**Le taux d'accueil assure une répartition précise de la chaîne, suffisamment de mesures pour que l'échantillon soit de la chaîne.

**Practical considerations:**
- **Burn-in**La chaîne a besoin de temps pour atteindre la distribution stationnaire à partir de son point de départ.
- **Thinning**: conserver chaque k-e échantillon pour réduire l'autocorrélation.
- **Multiple chains**Si elles convergent vers la même distribution, vous avez des preuves de convergence.
- **Acceptance rate**Pour les propositions gaussiennes en dimension d, le taux d'acceptation optimal est d'environ 23% (Roberts & Rosenthal, 2001).

> Je veux dire:**Burn-in**丢弃前 N 个样本(链需要时间到达平稳分布);**Thinning**Chaque personne a un problème de santé.**Multiple chains**Si la réception est répartie avec la même distribution, il y a des preuves de réception.**Acceptance rate**Le taux d'acceptation optimal du VKT est d'environ 23% (trop élevé = presque pas, trop faible = total rejet)

### Processus stochastiques dans l'IA

| Process | AI Application |
|---------|---------------|
| Random walk | Exploration in RL, Node2Vec embeddings |
| Markov chain | Text generation, MCMC sampling |
| Brownian motion | Diffusion models (forward process) |
| Langevin dynamics | Score-based generative models, SGLD |
| Markov decision process | Reinforcement learning |
| Metropolis-Hastings | Bayesian inference, posterior sampling |

> Le processus de développement de l'IA est le processus de développement de la technologie de l'IA.

## Construisez-le et mettez-le en œuvre.
```figure
random-walk-diffusion
```

## Faites-le

### Étape 1: Simulateur de marche aléatoire

> 第1 étape: avec le mouvement de la machine à modeler.

```python
import numpy as np

def random_walk_1d(n_steps, seed=None):
    rng = np.random.RandomState(seed)
    steps = rng.choice([-1, 1], size=n_steps)
    positions = np.concatenate([[0], np.cumsum(steps)])
    return positions


def random_walk_2d(n_steps, seed=None):
    rng = np.random.RandomState(seed)
    directions = rng.choice(4, size=n_steps)
    dx = np.zeros(n_steps)
    dy = np.zeros(n_steps)
    dx[directions == 0] = 1   # right
    dx[directions == 1] = -1  # left
    dy[directions == 2] = 1   # up
    dy[directions == 3] = -1  # down
    x = np.concatenate([[0], np.cumsum(dx)])
    y = np.concatenate([[0], np.cumsum(dy)])
    return x, y
```

La marche 1D stocke les sommes cumulatives. Chaque étape est +1 ou -1. Après n étapes, la position est la somme. La variance augmente linéairement avec n, de sorte que l'écart standard augmente en sqrt(n).

> Un niveau de croissance est le niveau de croissance de la gamme de données.

### Étape 2: Chaîne de Markov

> 第2 étape:                                                                                                                                                                                                                                                             

```python
class MarkovChain:
    def __init__(self, transition_matrix, state_names=None):
        self.P = np.array(transition_matrix, dtype=float)
        self.n_states = len(self.P)
        self.state_names = state_names or [str(i) for i in range(self.n_states)]

    def step(self, current_state, rng=None):
        if rng is None:
            rng = np.random.RandomState()
        probs = self.P[current_state]
        return rng.choice(self.n_states, p=probs)

    def simulate(self, start_state, n_steps, seed=None):
        rng = np.random.RandomState(seed)
        states = [start_state]
        current = start_state
        for _ in range(n_steps):
            current = self.step(current, rng)
            states.append(current)
        return states

    def stationary_distribution(self):
        eigenvalues, eigenvectors = np.linalg.eig(self.P.T)
        idx = np.argmin(np.abs(eigenvalues - 1.0))
        stationary = np.real(eigenvectors[:, idx])
        stationary = stationary / stationary.sum()
        return np.abs(stationary)
```

La distribution stationnaire est le propre vecteur gauche de P avec valeur propre 1. Nous le trouvons en calculant les propres vecteurs de P^T (transposant les propres vecteurs gauche en propres vecteurs droits).

> La distribution est la valeur de la trace gauche de P à 1 par rapport à la trace gauche de P^T.

### Étape 3: Dynamique de Langevin

> 第3 étape: Langevin 动力学──梯度下降 + 高斯噪音 = explorer l'énergie paysage并采样──

```python
def langevin_dynamics(grad_U, x0, dt, temperature, n_steps, seed=None):
    rng = np.random.RandomState(seed)
    x = np.array(x0, dtype=float)
    trajectory = [x.copy()]
    for _ in range(n_steps):
        noise = rng.randn(*x.shape)
        x = x - dt * grad_U(x) + np.sqrt(2 * temperature * dt) * noise
        trajectory.append(x.copy())
    return np.array(trajectory)
```

Le gradient pousse x vers une faible énergie. Le bruit empêche qu'il ne se bloque. À l'équilibre, la distribution des échantillons est proportionnelle à exp ((-U ((x) / température).

> 梯度把 x 推向低能量区, noise preventing into the local best 优──平衡时样本分布  exp(-U(x) /温度)

### Étape 4: Métropole-Hastings

> 第4 étape: MCMC de Metropolis-Hastings.

```python
def metropolis_hastings(target_log_prob, proposal_std, x0, n_samples, seed=None):
    rng = np.random.RandomState(seed)
    x = np.array(x0, dtype=float)
    samples = [x.copy()]
    accepted = 0
    for _ in range(n_samples - 1):
        x_proposed = x + rng.randn(*x.shape) * proposal_std
        log_ratio = target_log_prob(x_proposed) - target_log_prob(x)
        if np.log(rng.rand()) < log_ratio:
            x = x_proposed
            accepted += 1
        samples.append(x.copy())
    acceptance_rate = accepted / (n_samples - 1)
    return np.array(samples), acceptance_rate
```

L'algorithme propose un nouveau point, vérifie s'il a une probabilité plus élevée (ou accepte avec probabilité proportionnelle au ratio) et répète.

> 算法流程:提议新点 → 检查概率是否更高 (或按比例接受)→ 重复.

## Utilisez-le avec le cadre de réalisation

En pratique, vous utilisez des bibliothèques établies pour ces algorithmes, mais comprendre la mécanique est important pour débogage et réglage.

> En fait, vous utilisez une base de données mature pour réaliser ces algorithmes.

```python
import numpy as np

rng = np.random.RandomState(42)
walk = np.cumsum(rng.choice([-1, 1], size=10000))
print(f"Final position: {walk[-1]}")
print(f"Expected distance: {np.sqrt(10000):.1f}")
print(f"Actual distance: {abs(walk[-1])}")
```

> NumPy 实现随机游走:一行代码生成 10000 步 ±1 随机游走,验证实际距离与理论值 √10000 = 100 接近──

### numpy pour les matrices de transition

```python
import numpy as np

P = np.array([[0.7, 0.1, 0.2],
              [0.3, 0.4, 0.3],
              [0.4, 0.2, 0.4]])

distribution = np.array([1.0, 0.0, 0.0])
for _ in range(100):
    distribution = distribution @ P

print(f"Stationary distribution: {np.round(distribution, 4)}")
```

> NumPy 处理转移矩阵: de [1,0,0] 出发,反复左乘 P 100 fois, automatiquement reçu到平稳分布── voilà le cœur de PageRank et autres algorithmes──

Multipliez la distribution initiale par P à plusieurs reprises. Après suffisamment d'itérations, elle converge à la distribution stationnaire indépendamment de l'endroit où vous avez commencé. C'est la méthode de puissance pour trouver le propre vecteur gauche dominant.

> Répondre à la distribution initiale par P. suffisamment de fois après, peu importe où on commence, on reçoit jusqu'à une distribution plane.

### Connexions avec des cadres réels

- **PyTorch diffusion:**Le `DDPMScheduler`Dans une tête enveloppée .`diffusers`met en œuvre les chaînes Markov avant et arrière
- **NumPyro / PyMC:**Utiliser MCMC (échantillonneur NUTS, qui améliore sur Metropolis-Hastings) pour l'inférence bayésienne
- **Gymnasium (RL):**La fonction étape environnement définit un processus de décision Markov

> Avec le vrai cadre de la relation:`diffusers`Le programmeur du DDPMS a réalisé la chaîne de pré-/contre-orientation du modèle de diffusion; NumPyro/PyMC utilise NUTS 采样器 (en version améliorée de Metropolis-Hastings) pour faire des hypothèses; La fonction de l'étape du Gymnasium définit le processus de décision de Markoff.

### Vérification de la convergence de la chaîne de Markov

```python
import numpy as np

P = np.array([[0.9, 0.1], [0.3, 0.7]])

eigenvalues = np.linalg.eigvals(P)
spectral_gap = 1 - sorted(np.abs(eigenvalues))[-2]
print(f"Eigenvalues: {eigenvalues}")
print(f"Spectral gap: {spectral_gap:.4f}")
print(f"Approximate mixing time: {1/spectral_gap:.1f} steps")
```

L'écart spectrale vous indique à quelle vitesse la chaîne oublie son état initial. Un écart de 0,2 signifie environ 5 étapes pour mélanger. Un écart de 0,01 signifie environ 100 étapes. Vérifiez toujours cela avant d'exécuter de longues simulations - un calcul de déchets de chaîne mélange lentement.

> L'intervalle de 0,2 a besoin d'environ 5 étapes de mélange; 0,01 a besoin d'environ 100 étapes de mélange.

## Envoyez-le . Produit .

Cette leçon donne:
- `outputs/prompt-stochastic-process-advisor.md`-- une requête qui aide à identifier quel cadre de processus stochastique s'applique à un problème donné

> Le cours est ouvert à tous les étudiants.

## Les liens concept

| Concept | Where it shows up |
|---------|------------------|
| Random walk | Node2Vec graph embeddings, exploration in RL |
| Markov chain | Token generation in LLMs, MCMC sampling |
| Brownian motion | Forward diffusion process in DDPM, SDE-based models |
| Langevin dynamics | Score-based generative models, stochastic gradient Langevin dynamics (SGLD) |
| Stationary distribution | MCMC convergence target, PageRank |
| Metropolis-Hastings | Bayesian posterior sampling, simulated annealing |
| Temperature | LLM sampling, Boltzmann exploration in RL, simulated annealing |
| Mixing time | Convergence speed of MCMC, spectral gap analysis |
| Absorbing state | End-of-sequence token, terminal states in RL |
| Detailed balance | Correctness guarantee for MCMC samplers |

> 概念关联:随机游走(Node2Vec、RL 探索)、马尔可夫链(LLM token 生成、MCMC)、布朗运动)、DDPM 前向过程)、Langevin 动力学(Score-based 模型、SGLD)、平稳分布(MCMC 收目标、PageRank)、Metropolis-Hastings(贝叶斯后验、模拟退火)、Temperature(LLM 采样、Boltzmann 探索)、Mixing time(MCMC 收速度)、Absorbing state(序列结束、RL 终止状态)、Détaillé équilibre((MCMC 采样机的正确性保证)、

Les modèles de diffusion méritent une attention particulière.

```
q(x_t | x_{t-1}) = N(x_t; sqrt(1-beta_t) * x_{t-1}, beta_t * I)
```

où beta_t est un calendrier de bruit. Après T étapes, x_T est approximativement N(0, I). Le processus inverse est paramétrifié par un réseau neuronal qui prédit le bruit:

```
p_theta(x_{t-1} | x_t) = N(x_{t-1}; mu_theta(x_t, t), sigma_t^2 * I)
```

Chaque étape de la génération est une étape dans une chaîne de Markov apprise.

Le SGLD (Stochastic Gradient Langevin Dynamics) combine la descente de gradient mini-batch avec le bruit de Langevin. Au lieu de calculer le gradient complet, vous utilisez une estimation stochastique et ajoutez un bruit calibré. Alors que le taux d'apprentissage diminue, le SGLD passe de l'optimisation à l'échantillonnage -- vous obtenez des échantillons Bayésiens approximatifs gratuits. C'est l'un des moyens les plus simples d'obtenir des estimations d'incertitude à partir d'un réseau neuronal.

L'idée clé de toutes ces connexions: les processus stochastiques ne sont pas seulement des outils théoriques. Ce sont les mécanismes informatiques à l'intérieur des systèmes d'IA modernes. Quand vous ajustez la température d'un LLM, vous ajustez une chaîne Markov. Quand vous entraînez un modèle de diffusion, vous apprenez à inverser un processus de mouvement Brownian. Quand vous exécutez l'inférence bayésienne, vous construisez une chaîne qui converge vers l'arrière.

> 穿越所有这些联系的核心洞见:随机过程不仅仅是理论工具,它们是现代AI系统内部的计算机制――调整LLM的温度时,你调整马尔可夫链;训练扩散模型时,你学习反转布朗运动过程;运行贝叶斯推理时,你构建收收到后验的链――

## Les exercices

1. **Simulate 1000 random walks of 10000 steps.**Décrire la répartition des positions finales. Vérifiez qu'il est approximativement gaussien avec la moyenne 0 et l'écart standard sqrt ((10000) = 100.

2. **Build a text generator using a Markov chain.**Formez un petit corpus: pour chaque mot, comptez les transitions vers le mot suivant. Construisez la matrice de transition. Générez de nouvelles phrases en prélèvant des échantillons de la chaîne.

3. **Implement simulated annealing**En utilisant Metropolis-Hastings, commencez à haute température (acceptez presque tout) et refroidissez progressivement (acceptez seulement des améliorations).

4. **Compare Langevin dynamics at different temperatures.**Pratique de l'échantillon à partir d'un potentiel de puits double U(x) = (x^2 - 1)^2. à basse température, les échantillons se regroupent dans un puits. à haute température, ils se propagent à travers les deux.

5. **Implement the forward diffusion process.**Commencez par un signal 1D (par exemple, une onde sinusoïde). Ajoutez progressivement le bruit sur 100 étapes avec un calendrier sonore linéaire. Montrez comment le signal se dégrade en bruit pur.

## Les termes clés

| Term | What people say | What it actually means |
|------|----------------|----------------------|
| Random walk | "Coin-flip movement" | A process where position changes by random increments at each step |
| Markov property | "Memoryless" | The future depends only on the present state, not on the history |
| Transition matrix | "The probability table" | P[i][j] = probability of moving from state i to state j |
| Stationary distribution | "The long-run average" | The distribution pi where pi*P = pi -- the chain's equilibrium |
| Brownian motion | "Random jiggling" | The continuous-time limit of a random walk, B(t) ~ N(0, t) |
| Langevin dynamics | "Gradient descent with noise" | Update rule that combines deterministic gradient and random perturbation |
| MCMC | "Walking toward the target" | Constructing a Markov chain whose stationary distribution is the one you want |
| Metropolis-Hastings | "Propose and accept/reject" | MCMC algorithm that uses acceptance ratios to ensure convergence |
| Temperature | "The randomness knob" | Parameter controlling the tradeoff between exploration and exploitation |
| Diffusion process | "Noise in, noise out" | Forward: gradually add noise. Reverse: gradually remove it. Generates data. |

> 术语速查:Random walk (随机游走) ‧Markov property ((无记忆性) ‧Transition matrix (转移矩阵) ‧P[i][j]) ‧Répartition stationnaire (平稳分布) ‧P=π) ‧Brownian motion (布朗运动) ‧布朗运动 (布朗运动) ‧N (N) ‧0,t)) ‧Langevin dynamics (带噪声的梯度下降) ‧MCMC (MCMC) ‧Construction (平稳分布) ‧Construction (MCMC) ‧Metropolis-Hastings (MCM) ‧Temperatur (探索/利用平衡参数) ‧Diffusion (MC) ‧Premi-augmentation du bruit ‧反向去噪声生成数据) ‧

## Encore une lecture

- **Ho, Jain, Abbeel (2020)**- "Dénoncer les modèles probabilistiques de diffusion". Le document du DDPM qui a lancé la révolution du modèle de diffusion.
- **Song & Ermon (2019)**-- "Modélisation générative en estimant les gradients de la distribution des données". Approche basée sur le score en utilisant la dynamique de Langevin pour l'échantillonnage.
- **Roberts & Rosenthal (2004)**"Les chaînes Markov et les algorithmes MCMC". La théorie derrière quand et pourquoi MCMC fonctionne.
- **Norris (1997)**- "Markov Chains". Le manuel standard couvre la convergence, les répartitions stationnaires et les temps de frappe.
- **Welling & Teh (2011)**-- "L'apprentissage bayésien via la dynamique de Langevin au degré stochastique". Combine SGD avec la dynamique de Langevin pour une inférence bayésienne évolutive.
