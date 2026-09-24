# Le calcul de l'apprentissage automatique

> Les dérivés vous indiquent la direction de la descente.

> Le nombre de directions vous dit où est le vers le bas.

**Type:** Learn | **类型:** 学习
**Language:**Je suis un Python .**语言:**Python
**Prerequisites:** Phase 1, Lessons 01-03 | **前置知识:** Phase 1, Lessons 01-03
**Time:** ~60 minutes | **时间:** ~60 分钟

## Objectifs d'apprentissage

- Compute des dérivés numériques et analytiques pour les fonctions ML communes (x^2, sigmoïde, entropie croisée)
  計算常见 ML 函数(x^2、sigmoid、交叉) de la valeur de la valeur de la valeur et de la valeur de la valeur de la valeur
- Implémenter la descente de gradient à partir de zéro pour minimiser une fonction de perte en 1D et 2D
  De la réalisation à zéro degré de baisse, dans la 1D et 2D la perte minimale de fonction
- Dériver le gradient d'un modèle de régression linéaire et le former par des mises à jour manuelles de poids
  推导线性回归模型的梯度,并通过手动权重更新进行训练
- Expliquer la matrice hessienne, les approximations de la série Taylor et leur lien avec les méthodes d'optimisation
  Expliquer Hessian 矩阵、Taylor 级数近似及其与优化方法的联系

> **【中文解读】**
> Le débit vous dit dans quelle direction aller. Le degré de baisse est le plus bas de la direction opposée du débit.

> **【拓展：微积分与神经网络】**
> - **梯度下降**Le système de formation de réseaux neuraux est basé sur la formation de réseaux neuraux.
> - **SGD/Adam**Le taux d'apprentissage de l'adaptation et de l'éducation
> - **学习率**Le niveau de la dérive est trop grand pour dépasser le niveau minimum, trop petit pour recevoir trop lentement.

## Le problème , l' introduction du problème

> **【中文解读】**Le train consiste à trouver chaque tour qui doit se déplacer. Le train consiste à trouver chaque tour qui doit se déplacer.

## Le concept de base.

> **【拓展：偏导数就是"只动一个旋钮看效果"]**La fonction de perte de la réseau de nerfs L(w1, w2, ..., wn) Il y a un million de variables. La variable de la charge ∂L/∂w_i  vous dit " seulement modifier un seul poids, la perte de la charge est de modifier combien " ̊ gradience est de mettre toutes les variables de la charge en un seul vecteur, en direction de " la direction la plus élevée ", donc le long de la gradience est le chemin la plus rapide vers le bas ̊ gradient ̊

### Qu'est-ce qu'un dérivé ?

Une dérivée mesure le taux de changement. Pour une fonction y = f(x), la dérivée f'(x) vous dit: si vous poussez x par une petite quantité, combien y change?

> Pour la fonction y = f(x), la valeur de l'échelle f'(x) vous dit: si x 微小变化, y 变化多少?

Géométriquement, la dérivée est la pente de la ligne tangente à un point.

> En géométrie, le nombre de guides est l'inclinaison d'un point de traversée.

**f(x) = x^2:**

| x | f(x) | f'(x) (slope) |
|---|------|---------------|
| 0 | 0    | 0 (flat, at the bottom) |
| 1 | 1    | 2 |
| 2 | 4    | 4 (tangent line slope at this point) |
| 3 | 9    | 6 |

Si vous déplacez x un peu à droite, y augmente d'environ 4 fois cette quantité. à x = 0, la pente est 0. Vous êtes au bas du bol.

> Dans une position x = 2, le taux d'inclinaison est de 4... si vous allez faire un mouvement x vers la droite, y augmenter environ 4 fois ce mouvement... dans une position x = 0, le taux d'inclinaison est de 0... vous êtes dans le "bas de la tasse".

La définition formelle:

```
f'(x) = lim   f(x + h) - f(x)
        h->0  -----------------
                     h
```

Dans le code, vous sautez la limite et utilisez juste une très petite h. C'est la dérivée numérique.

> Dans le code, sauter au-delà de la limite, directement avec un très petit h pour approcher.

### Dérivés partiels: une variable à la fois

Les fonctions réelles ont de nombreuses entrées. Une perte de réseau neuronal dépend de milliers de poids. Une dérivé partielle maintient toutes les variables constantes sauf une, puis prend la dérivé par rapport à celle-ci.

> La fonction de perte de réseau neural dépend de milliers de poids. La parité de la fonction ne change pas, elle ne peut être dirigée qu'à une seule variable.

```
f(x, y) = x^2 + 3xy + y^2

df/dx = 2x + 3y     (treat y as a constant)
df/dy = 3x + 2y     (treat x as a constant)
```

Chaque dérivé partiel répond: si je pousse seulement ce poids, comment la perte change-t-elle ?

> Chaque numéro de direction répond: si je ne fais que décaler ce poids, combien perdra-t-on ?

### Le gradient: vecteur de toutes les dérivées partielles

Le gradient collecte chaque dérivé partiel en un vecteur. Pour une fonction f ((x, y, z), le gradient est:

> 梯度把所有偏导数集合 into one向量──对函数 f ((x, y, z),梯度为:

```
grad f = [ df/dx, df/dy, df/dz ]
```

Le gradient pointe dans la direction de l'ascension la plus raide.

> 梯度指向最上升方向──要最小化函数,就沿相反方向走──

**Contour plot of f(x,y) = x^2 + y^2:**

La fonction forme une forme de bol avec des cercles concentriques comme lignes de contour.

> La fonction forme une forme de bowl, égale à la ligne haute est le même. La valeur minimale est (0, 0)

| Point | grad f | -grad f (descent direction) |
|-------|--------|----------------------------|
| (1, 1) | [2, 2] (points uphill, away from minimum) | [-2, -2] (points downhill, toward minimum) |
| (0, 0) | [0, 0] (flat, at the minimum) | [0, 0] |

> 梯度方向指向最上坡,负梯度方向指向最下坡 (即向最小值) ⋅在最小值处梯度为零──

C'est une descente de gradient dans une image.

> C'est le tableau de la dégradation du degré.

### Le lien avec l'optimisation

La formation d'un réseau neural est une optimisation. Vous avez une fonction de perte L ((w1, w2, ..., wn) qui mesure à quel point le modèle est mal. Vous voulez le minimiser.

> 训练神经网络就是优化――损失函数 L(w1,w2, ..., wn) 衡量模型有多"错", vous devez le minimiser。

```
Gradient descent update rule:

  w_new = w_old - learning_rate * dL/dw

For every weight:
  1. Compute the partial derivative of loss with respect to that weight
  2. Subtract a small multiple of it from the weight
  3. Repeat
```

> Règles de réduction de la température: nouveau poids = vieux poids - taux d'apprentissage × 梯度──重复:1) calculer le nombre de déviations de chaque poids;2) déduire le petit nombre de fois du poids;3)

Le taux d'apprentissage contrôle la taille des étapes. Trop grand et vous survoltez. Trop petit et vous rampez.

> Le taux d'apprentissage contrôle progression.

**Loss landscape (1D slice):**

La fonction de perte L ((w) forme une courbe avec des sommets et des vallées à mesure que le poids w varie.

> 损失函数 L(w) 随权重 w 变形带峰和谷的曲线──

| Feature | Description |
|---------|-------------|
| Global minimum | The lowest point on the entire curve -- the best solution |
| Local minimum | A valley that is lower than its neighbors but not the lowest overall |
| Slope | Gradient descent follows the slope downhill from any starting point |

> La valeur minimale locale est le point le plus bas de la courbe de la ligne; la valeur minimale locale est la plus basse de la région voisine mais pas la plus basse de la région; la gradience descend du point de départ suivant le versant.

La descente graduelle suit la pente en descente. Elle peut s'enfoncer dans les minima locaux, mais dans les espaces haute dimension (millions de poids) c'est rarement un problème pratique.

> La situation est très difficile à trouver dans le monde entier.

### Dérivés numériques et analytiques

Il y a deux façons de calculer un dérivé.

> Il existe deux méthodes de calcul.

Pour le calcul, il est possible de calculer le calcul par la main.

> 解析法:手动应用微积分规则──如 f(x) = x^2 的导数是 f'(x) = 2x──精确且快速──

Numérique: approximation en utilisant la définition. Comptez f ((x+h) et f ((x-h) pour un minuscule h, puis utilisez la différence.

> Pour les calculs de la valeur de l'élément de l'élément de l'élément de l'élément de l'élément de l'élément de l'élément de l'élément de l'élément de l'élément de l'élément de l'élément de l'élément de l'élément de l'élément de l'élément de l'élément de l'élément de l'élément de l'élément de l'élément de l'élément de l'élément de l'élément de l'élément de l'élément de l'élément de l'élément de l'élément de l'élément de l'élément de l'élément de l'élément de l'élément de l'élément de l'élément de l'élément de l'élément de l'élément de l'élément de l'élément de l'élément de l'élément de l'élément de l'élément de l'élément.

```
Numerical (central difference):

f'(x) ~= f(x + h) - f(x - h)
          -----------------------
                  2h

h = 0.0001 works well in practice
```

Les dérivés numériques sont plus lents mais fonctionnent pour n'importe quelle fonction. Les dérivés analytiques sont rapides mais nécessitent que vous dériviez la formule. Les cadres de réseau neuronal utilisent une troisième approche: la différenciation automatique, qui calcule les dérivés exacts mécaniquement.

> Le nombre de directions est plus lent mais il est applicable à toute fonction. Il est nécessaire de le faire rapidement.

### Dérivés à la main pour des fonctions simples

Ce sont les dérivés que vous verrez encore et encore dans ML.

> Ce sont les nombres de guides que vous verrez à plusieurs reprises dans le ML.

```
Function        Derivative       Used in
--------        ----------       -------
f(x) = x^2     f'(x) = 2x      Loss functions (MSE)
f(x) = wx + b  f'(w) = x        Linear layer (gradient w.r.t. weight)
                f'(b) = 1        Linear layer (gradient w.r.t. bias)
                f'(x) = w        Linear layer (gradient w.r.t. input)
f(x) = e^x     f'(x) = e^x     Softmax, attention
f(x) = ln(x)   f'(x) = 1/x     Cross-entropy loss
f(x) = 1/(1+e^-x)  f'(x) = f(x)(1-f(x))   Sigmoid activation
```

Pour f ((x) = x^2:

```
f(x) = x^2    f'(x) = 2x

  x    f(x)   f'(x)   meaning
  -2    4      -4      slope tilts left (decreasing)
  -1    1      -2      slope tilts left (decreasing)
   0    0       0      flat (minimum!)
   1    1       2      slope tilts right (increasing)
   2    4       4      slope tilts right (increasing)
```

> Dans x<0 时导数为负(函数递减), x=0 时导数为零(atteindre la valeur minimale), x>0 时导数为正(函数递增) ・・・

Pour f(w) = wx + b avec x=3, b=1:

```
f(w) = 3w + 1    f'(w) = 3

The derivative with respect to w is just x.
If x is big, a small change in w causes a big change in output.
```

> Pour le w, le résultat est x en soi. Si x est très grand, les petites variations de w entraînent des variations énormes dans la production.

### La règle de la chaîne

Lorsque les fonctions sont composées, la règle de la chaîne vous dit comment différencier.

> Lorsque la fonction est complète, la loi de la chaîne vous dit comment demander des instructions.

```
If y = f(g(x)), then dy/dx = f'(g(x)) * g'(x)

Example: y = (3x + 1)^2
  outer: f(u) = u^2       f'(u) = 2u
  inner: g(x) = 3x + 1    g'(x) = 3
  dy/dx = 2(3x + 1) * 3 = 6(3x + 1)
```

Les réseaux neuronaux sont des chaînes de fonctions: entrée -> linéaire -> activation -> linéaire -> activation -> perte. La répartition en arrière est la règle de chaîne appliquée à plusieurs reprises de la sortie à l'entrée.

> Le réseau de réaction est une chaîne de fonction: entre les sorties et les sorties.

### La Matrice hessienne

Le gradient indique la pente, le Hessien la courbure.

> La gradience vous dit la courbe, la Hessian la matrice vous dit la courbe.

Le hessien est la matrice des dérivés partiels de deuxième ordre. Pour une fonction f ((x1, x2, ..., xn), l'entrée (i, j) du hessien est:

> Le Hessian est la seconde phase du nombre de composants. Pour les fonctions f ((x1, x2, ..., xn), le Hessian est la seconde (i, j) 项 ∂2f/∂∂x_i ∂x_j) ⋅

```
H[i][j] = d^2f / (dx_i * dx_j)
```

Pour une fonction à 2 variables f ((x, y):

```
H = | d^2f/dx^2    d^2f/dxdy |
    | d^2f/dydx    d^2f/dy^2 |
```

**What the Hessian tells you at a critical point (where gradient = 0):**

> Hessian dans le point de référence (梯度为 0 处) vous dit: est-ce la valeur minimale de la situation, la valeur maximale de la situation ou la valeur minimale de la situation ?

| Hessian property | Meaning | Example surface |
|-----------------|---------|-----------------|
| Positive definite (all eigenvalues > 0) | Local minimum | Bowl pointing up |
| Negative definite (all eigenvalues < 0) | Local maximum | Bowl pointing down |
| Indefinite (mixed eigenvalues) | Saddle point | Horse saddle shape |

> La valeur maximale de la valeur maximale de la valeur maximale de la valeur maximale de la valeur maximale de la valeur maximale de la valeur maximale de la valeur maximale de la valeur maximale de la valeur maximale de la valeur maximale de la valeur maximale de la valeur maximale de la valeur maximale de la valeur maximale de la valeur maximale de la valeur maximale de la valeur maximale de la valeur maximale de la valeur maximale de la valeur maximale de la valeur maximale de la valeur maximale de la valeur maximale de la valeur maximale de la valeur maximale de la valeur maximale de la valeur maximale de la valeur maximale de la valeur maximale de la valeur maximale de la valeur maximale de la valeur maximale de la valeur maximale de la valeur maximale de la valeur maximale de la valeur maximale de la valeur maximale de la valeur maximale de la valeur maximale de la valeur maximale de la valeur maximale de la valeur maximale de la valeur maximale de la valeur maximale de la valeur maximale de la valeur maximale de la valeur maximale de la valeur maximale de la valeur maximale de la valeur maximale de la valeur maximale de la valeur maximale de la valeur maximale de la valeur de la valeur maximale de la valeur maximale de la valeur de la valeur maximale de la valeur de la valeur maximale de la valeur de la valeur maximale de la valeur maximale de la valeur de la valeur maximale de la valeur de la valeur maximale de la valeur de la valeur maximale de la valeur de la valeur maximale de la valeur de la valeur de la valeur maximale de la valeur de la valeur maximale de la valeur de la valeur de la valeur maximale de la valeur de la valeur maximale de la valeur de la valeur de la valeur de la valeur de la valeur maximale de la valeur de la valeur de la valeur de la valeur maximale de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur maximale de la valeur de la valeur est est est est est est est est est est est est est est est est est est est est est est est est est est est est est est.

**Example:**f(x, y) = x^2 - y^2 (une fonction de selle)

```
df/dx = 2x       df/dy = -2y
d^2f/dx^2 = 2    d^2f/dy^2 = -2    d^2f/dxdy = 0

H = | 2   0 |
    | 0  -2 |

Eigenvalues: 2 and -2 (one positive, one negative)
--> Saddle point at (0, 0)
```

Comparer avec f ((x, y) = x^2 + y^2 (un bol):

```
H = | 2  0 |
    | 0  2 |

Eigenvalues: 2 and 2 (both positive)
--> Local minimum at (0, 0)
```

**Why the Hessian matters in ML:**

> Hessian dans ML: Newton a utilisé Hessian 修梯度方向, faire 方向走小步、平坦方向走大步, afin de比梯度下降更快收──

La méthode de Newton utilise le Hessian pour prendre de meilleures étapes d'optimisation que la descente de gradient.

```
Newton's update:    w_new = w_old - H^(-1) * gradient
Gradient descent:   w_new = w_old - lr * gradient
```

> Newton 更新:w_new = w_old - H−1 × gradient。 il utilise le taux de courbure pour redécouvrir la gradience。

La méthode de Newton converge plus rapidement parce que les "rescales" hessiennes du gradient - les directions raides obtiennent des pas plus petits, les directions plates obtiennent des pas plus grands.

> Newton a reçu plus vite, parce que le Hessian "réconcerté" gradient direction direction direction petit pas, plan direction direction grande pas.

Le problème: pour un réseau neural avec N paramètres, le Hessian est N x N. Un modèle avec 1 million de paramètres aurait besoin d'une matrice d'entrée de 1 trillion.

> Le problème réside dans: Le réseau de N 个参数, Hessian est N×N。 millions de modèles paramétraux nécessitent des millions de matrices de taille c'est pourquoi nous utilisons des approximations comme Adam、L-BFGS)。

| Method | What it uses | Cost | Convergence |
|--------|-------------|------|-------------|
| Gradient descent | First derivatives only | O(N) per step | Slow (linear) |
| Newton's method | Full Hessian | O(N^3) per step | Fast (quadratic) |
| L-BFGS | Approximate Hessian from gradient history | O(N) per step | Medium (superlinear) |
| Adam | Per-parameter adaptive rates (diagonal Hessian approx) | O(N) per step | Medium |
| Natural gradient | Fisher information matrix (statistical Hessian) | O(N^2) per step | Fast |

> Il s'agit d'un système de calcul de la fréquence de la fréquence de la fréquence de la fréquence de la fréquence de la fréquence de la fréquence de la fréquence de la fréquence de la fréquence de la fréquence de la fréquence de la fréquence de la fréquence de la fréquence de la fréquence de la fréquence de la fréquence de la fréquence de la fréquence de la fréquence de la fréquence de la fréquence de la fréquence de la fréquence de la fréquence de la fréquence de la fréquence de la fréquence de la fréquence de la fréquence de la fréquence de la fréquence de la fréquence de la fréquence de la fréquence de la fréquence de la fréquence de la fréquence de la fréquence de la fréquence de la fréquence de la fréquence de la fréquence de la fréquence de la fréquence de la fréquence de la fréquence de la fréquence de la fréquence de la fréquence de la fréquence de la fréquence de la fréquence de la fréquence de la fréquence de la fréquence de la fréquence de la fréquence de la fréquence de la fréquence de la fréquence de la fréquence de la fréquence de la fréquence de la fréquence de la fréquence de la fréquence de la fréquence de la fréquence de la fréquence de la fréquence de la fréquence de la fréquence de la fréquence de la fréquence de la fréquence de la fréquence de la fréquence de la fréquence de la fréquence de la fréquence de la fréquence de la fréquence de la fréquence de la fréquence de la fréquence de la fréquence de la fréquence de la fréquence de la fréquence de la fréquence de la fréquence de la fréquence de la fréquence de la fréquence de la fréquence de la fréquence de la fréquence de la fréquence de la fréquence de la fréquence de la fréquence de la fréquence de la fréquence de la fréquence de la fréquence de la fréquence de la fréquence de la fréquence de la fréquence de la fréquence de la fréquence de la fréquence de la fréquence de la fréquence de la fréquence de la fréquence de la fréquence de la fréquence de la fréquence de la fréquence de la fréquence de la fréquence de la fréquence

Dans la pratique, Adam est l'optimisateur par défaut pour l'apprentissage profond. Il approximate les informations de deuxième ordre à moindre coût en suivant la moyenne en cours et la variance des gradients par paramètre.

> En fait, Adam est un optimisateur par défaut d'apprentissage profond. Il suit la moyenne et la différence de chaque élément de la échelle, à un prix peu proche de la seconde étape.

### Approximation de la série Taylor

Toute fonction lisse peut être approximée localement par un polynôme:

> Toute fonction plane peut être approximative en plusieurs positions.

```
f(x + h) = f(x) + f'(x)*h + (1/2)*f''(x)*h^2 + (1/6)*f'''(x)*h^3 + ...
```

Plus vous en incluez, mieux sera l'approximation, mais seulement près du point x.

> 包含的项越多,近似越好但只有效在x 附近──一阶泰勒 = 梯度下降,二阶泰勒 = Newton 法──

**Why Taylor series matter for ML:**

- **First-order Taylor = gradient descent.**Lorsque vous utilisez f(x + h) ~ f(x) + f'(x) *h, vous faites une approximation linéaire.

- **Second-order Taylor = Newton's method.**En utilisant f(x + h) ~ f(x) + f'(x) *h + (1/2) *f'(x) *h^2, vous obtenez un modèle quadratique.

- **Loss function design.**Les émissions de MSE et de l'entropie croisée sont lisses, ce qui signifie que leurs élargissements Taylor sont bien comportés.

> Taylor = approximation de ligne = diminution de la gradience; second Taylor = second approximation = Newton 法; MSE 和交叉 de la flatteness n'est pas un hasard  flatteness de la perte faire l'optimisation prévisible。

```
Approximation order    What it captures    Optimization method
-------------------    -----------------   -------------------
0th order (constant)   Just the value      Random search
1st order (linear)     Slope               Gradient descent
2nd order (quadratic)  Curvature           Newton's method
Higher orders          Finer structure     Rarely used in ML
```

> Préparation de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la

L'idée principale: toute optimisation basée sur le gradient consiste à approximer la fonction de perte localement et à atteindre le minimum de cette approximation.

> 关键洞见: Toutes les améliorations basées sur la gradience sont en nature dans la fonction de perte proche locale, puis se dirigent vers ce point de faible valeur proche.

### Intégrales dans le ML

Les dérivés vous indiquent les taux de changement.

> 导数 vous dit le taux de variation,积分计算累积(曲线下面积)

En ML, vous comptez rarement les intégrales à la main, mais le concept est partout:

> Dans le ML, vous avez peu de calculs, mais le concept de calcul n'existe pas:

**Probability.**Pour une variable aléatoire continue avec une densité p ((x):
```
P(a < X < b) = integral from a to b of p(x) dx
```
La surface sous la courbe de densité de probabilité entre a et b est la probabilité d'atterrissage dans cette plage.

> **概率**: pour la continuité des variations, la fonction de densité p(x) dans [a, b] 区间 积分就是落在此区间的概率──

**Expected value.**Le résultat moyen pondéré par probabilité:
```
E[f(X)] = integral of f(x) * p(x) dx
```
La perte attendue sur une distribution de données est une partie intégrante.

> **期望**:加权平均―― l'attente de perte de la distribution de données est un积分, entraînement minimiser son expérience approximatif―

**KL divergence.**Mesure la différence entre deux répartitions:
```
KL(p || q) = integral of p(x) * log(p(x) / q(x)) dx
```
Utilisé dans les VAE, la distillation du savoir et l'inférence bayésienne.

> **KL 散度**: mesurer les différences de deux distributions.

**Normalization constants.**Dans l' inférence bayésienne:
```
p(w | data) = p(data | w) * p(w) / integral of p(data | w) * p(w) dw
```
Le dénominateur est une intégrale sur toutes les valeurs de paramètres possibles. Il est souvent intractable, c'est pourquoi nous utilisons des approximations comme MCMC et l'inférence variationnelle.

> **归一化常数**Dans la théorie de Bayes, la fraction est le résultat de toutes les valeurs de paramètres possibles, généralement incapable de résoudre.

| Integral concept | Where it appears in ML |
|-----------------|----------------------|
| Area under curve | Probability from density functions |
| Expected value | Loss functions, risk minimization |
| KL divergence | VAEs, policy optimization, distillation |
| Normalization | Bayesian posteriors, softmax denominator |
| Marginal likelihood | Model comparison, evidence lower bound (ELBO) |

> Le concept de "réparation" est un concept de "réparation" qui est un concept de "réparation" qui est un concept de "réparation" qui est un concept de "réparation".

### Règle de chaîne multivariée dans un graphique de calcul

La règle de la chaîne ne s'applique pas seulement aux fonctions scalaires dans une ligne. Dans un réseau neuronal, les variables se dilatent et se fusionnent. Voici comment les dérivés circulent à travers un simple passage vers l'avant:

> La loi du chaînage de plusieurs variables ne s'applique pas seulement aux fonctions de la quantité de ligne. Dans le réseau neuronal, les variables se divisent et se combinent.

```mermaid
graph LR
    x["x (input)"] -->|"*w"| z1["z1 = w*x"]
    z1 -->|"+b"| z2["z2 = w*x + b"]
    z2 -->|"sigmoid"| a["a = sigmoid(z2)"]
    a -->|"loss fn"| L["L = -(y*log(a) + (1-y)*log(1-a))"]
```

Le passage en arrière compute les gradients de droite à gauche:

```mermaid
graph RL
    dL["dL/dL = 1"] -->|"dL/da"| da["dL/da = -y/a + (1-y)/(1-a)"]
    da -->|"da/dz2 = a(1-a)"| dz2["dL/dz2 = dL/da * a(1-a)"]
    dz2 -->|"dz2/dw = x"| dw["dL/dw = dL/dz2 * x"]
    dz2 -->|"dz2/db = 1"| db["dL/db = dL/dz2 * 1"]
```

Chaque flèche se multiplie par la dérivé locale. Le gradient pour un paramètre est le produit de toutes les dérivées locales le long du chemin de la perte à ce paramètre. Lorsque les chemins se ramifient et se fusionnent, vous additionnez les contributions (règle de la chaîne multivariée).

> Chaque arrow est multiplié par le nombre de lignes de chaque paramètre = le nombre de lignes de chaque paramètre, de la perte à la liaison de chaque paramètre.

C'est tout la répartition en arrière: la règle de la chaîne appliquée systématiquement à travers un graphique de calcul, de la sortie aux entrées.

> Tout ce qui est inversé est: dans le diagramme de calcul, de la sortie à l'entrée est systématisé par la loi de l'application de la chaîne.

### La matrice jacobie

Lorsqu'une fonction cartographiant un vecteur à un vecteur (comme une couche de réseau neuronal), sa dérivé est une matrice.

> Lorsque la fonction trace le flux vers le flux, comme la couche du réseau de neurones, son flux est un flux Jacobien contenant chaque sortie vers chaque entrée.

Pour f: R^n -> R^m, le Jacobien J est une matrice m x n:

> Pour f: R^n → R^m, Jacobian J est un m × n 矩阵:

| | x1 | x2 | ... | xn |
|---|---|---|---|---|
| f1 | df1/dx1 | df1/dx2 | ... | df1/dxn |
| f2 | df2/dx1 | df2/dx2 | ... | df2/dxn |
| ... | ... | ... | ... | ... |
| fm | dfm/dx1 | dfm/dx2 | ... | dfm/dxn |

Vous ne pouvez pas calculer les Jacobiens à la main pour les réseaux neuraux. PyTorch le gère. Mais sachant qu'il existe vous aide à comprendre les formes en rétroviseur: si une couche repère R^n à R^m, son Jacobian est m x n. Le gradient coule vers l'arrière à travers la transposition de cette matrice.

> Vous ne serez pas en mesure de calculer le JacobianPyTorch du réseau de neurones. Mais sachez que son existence peut vous aider à comprendre la forme de propagation inverse: si le niveau de R^n est mappé à R^m, son Jacobian est m×n, la gradience passe par son transfert vers le flux inverse.

### Pourquoi cela importe pour les réseaux neuronaux

Chaque poids dans un réseau neuronal obtient un gradient. Le gradient vous indique comment ajuster ce poids pour réduire la perte.

> Chaque poids du réseau neural a une échelle, qui vous indique comment régler ce poids pour réduire les pertes.

```mermaid
graph LR
    subgraph Forward["Forward Pass"]
        I["input"] --> W1["W1"] --> R["relu"] --> W2["W2"] --> S["softmax"] --> L["loss"]
    end
```

```mermaid
graph RL
    subgraph Backward["Backward Pass"]
        dL["dL/dloss"] --> dW2["dL/dW2"] --> d2["..."] --> dW1["dL/dW1"]
    end
```

Chaque mise à jour de poids:
- `W1 = W1 - lr * dL/dW1`
- `W2 = W2 - lr * dL/dW2`

> Chaque élément de poids est modifié par le calcul de la charge de chaque élément de poids.

Le passage avant calcule la prédiction et la perte. Le passage arrière calcule le gradient de la perte par rapport à chaque poids. Ensuite, chaque poids fait un petit pas en descente. Répétez pour des millions de pas. C'est l'apprentissage profond.

> Avant de se propager calcul prédiction et perte, contre de se propager calcul de chaque poids de la échelle, puis chaque poids à la échelle de la échelle de la échelle de la échelle de la échelle de la échelle de la échelle de la échelle de la échelle de la échelle de la échelle de la échelle de la échelle de la échelle de la échelle de la échelle de la échelle de la échelle de la échelle de la échelle de la échelle de la échelle de la échelle de la échelle de la échelle de la échelle de la échelle de la échelle de la échelle de la échelle de la échelle de la échelle de la échelle de la échelle de la échelle de la échelle de la échelle de la échelle de la échelle de la échelle de la échelle de la échelle de la échelle de la échelle de la échelle de la échelle de la échelle de la échelle de la échelle de la échelle de la échelle de la échelle de la échelle de la échelle de la échelle de la échelle de la échelle de la échelle de la échelle de la échelle de la échelle de la échelle.

## Construisez-le et mettez-le en œuvre.
```figure
derivative-tangent
```

## Faites-le

### Étape 1: Dérivé numérique à partir de zéro

```python
def numerical_derivative(f, x, h=1e-7):
    return (f(x + h) - f(x - h)) / (2 * h)

def f(x):
    return x ** 2

for x in [-2, -1, 0, 1, 2]:
    numerical = numerical_derivative(f, x)
    analytical = 2 * x
    print(f"x={x:2d}  f'(x) numerical={numerical:.6f}  analytical={analytical:.1f}")
```

> Utilisation de la différence de centre pour réaliser la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de

La dérivée numérique correspond à celle analytique à plusieurs décimales.

> La coïncidence entre la valeur de la valeur et la valeur de la résolution sur plusieurs points après la petite différence confirme la validité de la formule de la différence centrale.

### Étape 2: Dérivés et gradients partiels

```python
def numerical_gradient(f, point, h=1e-7):
    gradient = []
    for i in range(len(point)):
        point_plus = list(point)
        point_minus = list(point)
        point_plus[i] += h
        point_minus[i] -= h
        partial = (f(point_plus) - f(point_minus)) / (2 * h)
        gradient.append(partial)
    return gradient

def f_multi(point):
    x, y = point
    return x**2 + 3*x*y + y**2

grad = numerical_gradient(f_multi, [1.0, 2.0])
print(f"Numerical gradient at (1,2): {[f'{g:.4f}' for g in grad]}")
print(f"Analytical gradient at (1,2): [2*1+3*2, 3*1+2*2] = [{2*1+3*2}, {3*1+2*2}]")
```

> Pour chaque dimension indépendante, le centre de différence est à la recherche de la direction, la composition est à la recherche de la dimension.

### Étape 3: Descente graduelle pour trouver le minimum de f ((x) = x^2

```python
x = 5.0
lr = 0.1
for step in range(20):
    grad = 2 * x
    x = x - lr * grad
    print(f"step {step:2d}  x={x:8.4f}  f(x)={x**2:10.6f}")
```

À partir de x=5, chaque étape se rapproche de x=0 (le minimum).

> De x = 5 sort, chaque pas est plus proche de x = 0 ((minimum value) ⋅ taux d'apprentissage 0,1 ⋅ faire x ⋅ petit à petit jusqu'à 0 ⋅

### Étape 4: Déclin gradient sur une fonction 2D

```python
def f_2d(point):
    x, y = point
    return x**2 + y**2

point = [4.0, 3.0]
lr = 0.1
for step in range(30):
    grad = numerical_gradient(f_2d, point)
    point = [p - lr * g for p, g in zip(point, grad)]
    loss = f_2d(point)
    if step % 5 == 0 or step == 29:
        print(f"step {step:2d}  point=({point[0]:7.4f}, {point[1]:7.4f})  f={loss:.6f}")
```

> 2D 梯度下降: de (4, 3) 出发, chaque étape du point de mise à jour -= lr × grad, progressivement recevoir jusqu'à (0, 0) ⋅

### Étape 5: Comparer les dérivés numériques et analytiques

```python
import math

test_functions = [
    ("x^2",      lambda x: x**2,          lambda x: 2*x),
    ("x^3",      lambda x: x**3,          lambda x: 3*x**2),
    ("sin(x)",   lambda x: math.sin(x),   lambda x: math.cos(x)),
    ("e^x",      lambda x: math.exp(x),   lambda x: math.exp(x)),
    ("1/x",      lambda x: 1/x,           lambda x: -1/x**2),
]

x = 2.0
print(f"{'Function':<12} {'Numerical':>12} {'Analytical':>12} {'Error':>12}")
print("-" * 50)
for name, f, df in test_functions:
    num = numerical_derivative(f, x)
    ana = df(x)
    err = abs(num - ana)
    print(f"{name:<12} {num:12.6f} {ana:12.6f} {err:12.2e}")
```

> Pour comparer 5 types de fonctions courantes à x = 2 en fonction de la valeur de l'indice et de la valeur de la solution: x2、x3、sin(x)、e^x、1/x。, l'erreur est généralement de 1e à 10 degrés, la validation de la méthode de valeur de l'indice est correcte.

### Étape 6: Calculer le hessien numériquement

```python
def hessian_2d(f, x, y, h=1e-5):
    fxx = (f(x + h, y) - 2 * f(x, y) + f(x - h, y)) / (h ** 2)
    fyy = (f(x, y + h) - 2 * f(x, y) + f(x, y - h)) / (h ** 2)
    fxy = (f(x + h, y + h) - f(x + h, y - h) - f(x - h, y + h) + f(x - h, y - h)) / (4 * h ** 2)
    return [[fxx, fxy], [fxy, fyy]]

def saddle(x, y):
    return x ** 2 - y ** 2

def bowl(x, y):
    return x ** 2 + y ** 2

H_saddle = hessian_2d(saddle, 0.0, 0.0)
H_bowl = hessian_2d(bowl, 0.0, 0.0)
print(f"Saddle Hessian: {H_saddle}")  # [[2, 0], [0, -2]] -- mixed signs
print(f"Bowl Hessian:   {H_bowl}")    # [[2, 0], [0, 2]]  -- both positive
```

> Le nombre de points de calcul de la fonction hessienne est [2,0], [0,-2]] (un vrai égal = 点), la forme de la boîte x2+y2 est [2,0], [0,2]] (un vrai égal = la valeur minimale) (en anglais).

Le Hessian de la fonction de selle a des valeurs propres 2 et -2 (signes mixtes, confirmant un point de selle).

> La valeur de la fonction hessienne est 2 和 -2 ((一正一负, identifier点); la valeur de la fonction hessienne est 2 ((均正, identifier la valeur minimale) ⋅

### Étape 7: Approximation de Taylor en action

```python
import math

def taylor_approx(f, f_prime, f_double_prime, x0, h, order=2):
    result = f(x0)
    if order >= 1:
        result += f_prime(x0) * h
    if order >= 2:
        result += 0.5 * f_double_prime(x0) * h ** 2
    return result

x0 = 0.0
for h in [0.1, 0.5, 1.0, 2.0]:
    true_val = math.sin(h)
    t1 = taylor_approx(math.sin, math.cos, lambda x: -math.sin(x), x0, h, order=1)
    t2 = taylor_approx(math.sin, math.cos, lambda x: -math.sin(x), x0, h, order=2)
    print(f"h={h:.1f}  sin(h)={true_val:.4f}  order1={t1:.4f}  order2={t2:.4f}")
```

> Taylor 近似实战:在 x0=0 处用一阶和二阶 Taylor 近似 sin(h) ・h=0.1 时近似精度极高,h=2 时偏差很大──这是梯度下降需要小学习率的数学根源──

Près de x0 = 0, sin(x) ~ x (Taylor de premier ordre). L'approximation est excellente pour les petites h mais se décompose pour les grandes h. C'est pourquoi la descente de gradient fonctionne mieux avec de petits taux d'apprentissage - chaque étape suppose que l'approximation linéaire est exacte.

> Dans le même temps, les taux de formation sont plus élevés que les taux de formation.

### Étape 8: Pourquoi cela est important pour un réseau neuronal

```python
import random

random.seed(42)

w = random.gauss(0, 1)
b = random.gauss(0, 1)
lr = 0.01

xs = [1.0, 2.0, 3.0, 4.0, 5.0]
ys = [3.0, 5.0, 7.0, 9.0, 11.0]

for epoch in range(200):
    total_loss = 0
    dw = 0
    db = 0
    for x, y in zip(xs, ys):
        pred = w * x + b
        error = pred - y
        total_loss += error ** 2
        dw += 2 * error * x
        db += 2 * error
    dw /= len(xs)
    db /= len(xs)
    total_loss /= len(xs)
    w -= lr * dw
    b -= lr * db
    if epoch % 40 == 0 or epoch == 199:
        print(f"epoch {epoch:3d}  w={w:.4f}  b={b:.4f}  loss={total_loss:.6f}")

print(f"\nLearned: y = {w:.2f}x + {b:.2f}")
print(f"Actual:  y = 2x + 1")
```

> 完整的线性回归训练循环: de l'accélération du poids w、b 发发, calculer la prédiction, l'erreur, la gradience dw 和 db de chaque échantillon, puis mettre à jour les paramètres.

Chaque boucle d'entraînement basée sur des gradients suit ce modèle: prédiction, perte de calcul, gradients de calcul, poids de mise à jour.

> Chaque cycle d'entraînement basé sur des échelles suit ce modèle: prédiction → 计算损失 → 计算梯度 → 更新权重―― cette formation a permis de réaliser un retour linéaire y=2x+1 −

## Utilisez-le avec le cadre de réalisation

Avec NumPy, les mêmes opérations sont plus rapides et plus concises:

> Utiliser NumPy 重写: le même calcul est plus simple, plus rapide, et éviter le cycle Python, rendant le calcul plus efficace.

```python
import numpy as np

x = np.array([1, 2, 3, 4, 5], dtype=float)
y = np.array([3, 5, 7, 9, 11], dtype=float)

w, b = np.random.randn(), np.random.randn()
lr = 0.01

for epoch in range(200):
    pred = w * x + b
    error = pred - y
    loss = np.mean(error ** 2)
    dw = np.mean(2 * error * x)
    db = np.mean(2 * error)
    w -= lr * dw
    b -= lr * db

print(f"Learned: y = {w:.2f}x + {b:.2f}")
```

> NumPy 向量化版本:用 `np.mean`替代Python 循环求平均,更快更简洁──矢量化 est une technique d'optimisation centrale du calcul numérique──

PyTorch automatique le calcul des gradients, mais la boucle de mise à jour est identique.

> Vous avez tout juste réalisé la baisse de la échelle depuis le zéro. PyTorch a automatisé le calcul de la échelle, mais le cycle actualisé est complètement le même.`w -= lr * dw`Cette ligne ne changera jamais.

## Les exercices

1. Mise en œuvre `numerical_second_derivative(f, x)`en utilisant `numerical_derivative`Vérifiez que la deuxième dérivée de x^3 à x=2 est 12.
    réaliser `numerical_second_derivative(f, x)`,调用两次 `numerical_derivative` L'essai x^3 dans x=2 est de 12
2. Utilisez la descente de gradient pour trouver le minimum de f ((x, y) = (x - 3) ^ 2 + (y + 1) ^ 2. Commencez à partir de (0, 0). La réponse devrait converger à (3, -1).
   Uzd梯度下降找 f(x, y) = (x - 3)2 + (y + 1)2 de la valeur minimale, de (0, 0) à (0, 0)
3. Ajouter de l'élan à la boucle de descente des gradients: maintenir un vecteur de vitesse qui accumule des gradients passés.
   给梯度下降循环加动量: maintenir une accumulation de la vitesse du passage du gradient △ comparer avec une vitesse de réception de la hauteur x = x4 - 3x2 △

## Les termes clés

| Term | What people say | What it actually means |
|------|----------------|----------------------|
| Derivative | "The slope" | The rate of change of a function at a point. Tells you how much the output changes per unit change in input. |
| Partial derivative | "Derivative of one variable" | The derivative with respect to one variable while all others are held constant. |
| Gradient | "Direction of steepest ascent" | A vector of all partial derivatives. Points in the direction that increases the function fastest. |
| Gradient descent | "Go downhill" | Subtract the gradient (times a learning rate) from the parameters to reduce the loss. The core of neural network training. |
| Learning rate | "Step size" | A scalar that controls how big each gradient descent step is. Too large: diverge. Too small: converge slowly. |
| Chain rule | "Multiply the derivatives" | The rule for differentiating composed functions: df/dx = df/dg * dg/dx. The mathematical basis of backpropagation. |
| Jacobian | "Matrix of derivatives" | When a function maps vectors to vectors, the Jacobian is the matrix of all partial derivatives of outputs with respect to inputs. |
| Numerical derivative | "Finite differences" | Approximating a derivative by evaluating the function at two nearby points and computing the slope between them. |
| Backpropagation | "Reverse-mode autodiff" | Computing gradients layer by layer from output to input using the chain rule. How neural networks learn. |
| Hessian | "Matrix of second derivatives" | The matrix of all second-order partial derivatives. Describes the curvature of a function. Positive definite Hessian at a critical point means local minimum. |
| Taylor series | "Polynomial approximation" | Approximating a function near a point using its derivatives: f(x+h) ~ f(x) + f'(x)h + (1/2)f''(x)h^2 + ... The basis for understanding why gradient descent and Newton's method work. |
| Integral | "Area under the curve" | The accumulation of a quantity over a range. In ML, integrals define probabilities, expected values, and KL divergence. |

> 术语速查:Dérivé (导数/斜率) ‧Dérivé partiel (导数, fixe autres variables) ‧Gradient (梯度), tous les dérivés constitués de la trajectoire, orientés vers le plus direction de hausse) ‧Dérivé déclin (梯度下降,沿梯度负方向更新) ‧Taylor série ‧Taylor série ‧Taylor série ‧Taylor série ‧Taylor série ‧Taylor série ‧Taylor série ‧Taylor série ‧Taylor série ‧Taylor série ‧Taylor série ‧Taylor série ‧Taylor série ‧Taylor série ‧Taylor série ‧Taylor série ‧Taylor série ‧Taylor série ‧Taylor série ‧Taylor série ‧Taylor série ‧Taylor série ‧Taylor série ‧Taylor série ‧Taylor série ‧Taylor série ‧Taylor ‧Taylor ‧Taylor ‧Taylor ‧Taylor ‧Taylor ‧Taylor ‧R ‧Taylor ‧Taylor ‧Taylor ‧Tor ‧Taylor ‧Tor ‧Taylor ‧T ‧or ‧or ‧Taylor ‧or ‧T                                                                                          

## Encore une lecture

- [3Blue1Brown: Essence of Calculus](https://www.3blue1brown.com/topics/calculus)- intuition visuelle pour les dérivés, les intégrales et la règle de la chaîne
- [Stanford CS231n: Backpropagation](https://cs231n.github.io/optimization-2/)- comment les gradients circulent à travers les couches du réseau neuronal
