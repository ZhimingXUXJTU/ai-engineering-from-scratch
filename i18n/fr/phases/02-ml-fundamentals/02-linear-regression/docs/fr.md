# Régrésion linéaire
# Retour en ligne


> La régression linéaire trace la meilleure ligne droite à travers vos données.

> 线性回归 线性回归 线性回归 线性回归 线性回归 线性回归 线性回归 线性回归 线性回归 线性回归 线性回归 线性回归 线性回归 线性回归 线性回归回归 线性回归回归回归回归回归回归回归回归回归回归回归回归回归回归回归回归回归回归回归回归回归回归回归回归回归回归回归回归回归回归回归回归回归回归回归回归回归回归回归回归回归回归回归回归回归回归回归回归回归回归回归回归回归回归回归回归回归回归回归回归回归回归回归回归回归回归回归回归回归回归回归回归回归回归回归回归回归回归回归回归回归回归回归回归回归回归回归回归回归回归回归回归回归回归回归回归回归回归回归回归回归回归回归回归回归回归回归回归回回回归回归回回回回回回回回回回回回回回回回回回回回回回回回回回回回回回回回回回回回回回回回回回回回回回回回回回回回回回回回回回回回回回回回回回回回回回回回回回回回回回回回回回回回回回回回回回回回回回回回回回回回回回回回回回回回回回回回回回回回回回回回回回回回回回回回回回回回回回回回回回回回回回回回回回回回回回回回回回回回回回回回回回回回回回回回回回回回回回回回回回回回回回回回回回回回回回回回回回回回回回回回回回回回回回回回

**Type:** Build | **类型：** 构建
**Languages:** Python
**Prerequisites:** Phase 1 (Linear Algebra, Calculus, Optimization), Phase 2 Lesson 1 | **前置知识：** Phase 1（线性代数、微积分、优化），Phase 2 第 1 课
**Time:** ~90 minutes | **时间：** 约 90 分钟

## Objectifs d'apprentissage

- Dériver les règles de mise à jour de la descente du gradient pour l'erreur carrée moyenne et mettre en œuvre la régression linéaire à partir de zéro
  推导平均方差的梯度下降更新规则并从零实现线性回归
- Comparer la descente des gradients et l'équation normale en termes de complexité de calcul et quand utiliser chaque
  Comparer la complexité de calcul des équations de degré de déclin et de réglementation, en déterminant quand utiliser chacun d'eux
- Construire un modèle de régression linéaire multiple avec la normalisation des caractéristiques et interpréter les poids appris
  构建带特征标准化多线性归归模型并解释学习到的权重
- Expliquez comment la régression de la Ridge (régularisation de la L2) empêche le surpassage en pénalisant les poids importants.
  Comment faire pour empêcher le passage à l'équilibre ?


> **【中文解读】**
> Le regression neural est le modèle de prédiction le plus simple avec une ligne droite ou un superplaine. Il s'agit également du réseau neuronal le plus simple: un réseau sans couche cachée, sans fonction active.

> **【拓展：线性回归在真实 AI 系统中的角色】**
> Bien que "l'apprentissage en profondeur" soit plus recherché, le retour en ligne reste l'un des modèles les plus couramment utilisés de l'industrie. Google utilise en grande partie le retour en ligne dans l'analyse de tests A/B pour estimer les effets de la reprise en ligne; Uber utilise le retour en ligne pour faire des prévisions de la demande; le modèle Fama-Français de trois facteurs dans le domaine financier est le retour en ligne en plusieurs formes.

## Le problème , l' introduction du problème

Vous avez des données: les tailles de la maison et leurs prix de vente. Vous voulez prédire le prix d'une nouvelle maison en fonction de sa taille. Vous pouvez le regarder sur un graphisme de dispersion, mais vous avez besoin d'une formule. Vous avez besoin d'une ligne qui correspond le mieux aux données afin que vous puissiez brancher dans n'importe quelle taille et obtenir une prédiction de prix.

> Vous avez des données: la surface de la maison et le prix de vente correspondant. Vous pensez que vous pouvez prévoir le prix de la nouvelle maison en fonction de la surface de la maison. Vous pouvez le faire en fonction du tableau de bord, mais vous avez besoin d'une formule.

La régression linéaire vous donne cette ligne. Plus important encore, elle introduit l'ensemble de la boucle d'entraînement ML: définir un modèle, définir une fonction de coût, optimiser les paramètres. Chaque algorithme ML suit le même schéma. Maîtrisez-le ici avec le cas le plus simple, et vous le reconnaîtrez partout.

> Le retour de ligne vous a fourni cette ligne. Plus important encore, il a introduit l'ensemble du cycle de formation de ML: définir le modèle, définir la fonction de prix, optimiser les paramètres. Chaque algorithme de ML suit le même modèle.

Il s'agit non seulement de problèmes simples, mais aussi de régressions linéaires utilisées dans les systèmes de production pour la prévision de la demande, l'analyse des tests A/B, la modélisation financière et comme base pour chaque tâche de régression.

> Il ne s'agit pas seulement d'une simple question. Le regroupement de la ligne est utilisé dans les systèmes de production pour la prévision de la demande, l'analyse des tests A/B, la construction financière, ainsi que comme base de chaque tâche de regroupement.

> **【中文解读】**
> Le regression linéaire est non seulement une connaissance d'entrée, mais aussi une raccourciation de l'ensemble du cycle de formation de l'apprentissage de la machine: définir le modèle → définir la fonction de perte → l'optimisation des paramètres.

## Le concept de base.

### Le modèle

La régression linéaire suppose une relation linéaire entre la sortie (x) et la sortie (y):

> 线性回归假设 entre les entrées (x) et les sorties (y) existe une relation 线性:

```
y = wx + b
```

- `w`(poids/inclinaison): combien y change lorsque x augmente de 1
  `w`(权重/斜率):x 增加 1 时 y 变化多少
- `b`(bias/intercept): la valeur de y lorsque x = 0
  `b`(偏置/截距): lorsque x = 0 时 y 的值

Pour les entrées (features) multiples, cela s'étend à:

> 对于多个输入(特征), pour étendre à:

```
y = w1*x1 + w2*x2 + ... + wn*xn + b
```

Ou sous forme vectorielle: `y = w^T * x + b`

> Ou avec le mot "volume":`y = w^T * x + b`

L'objectif: trouver les valeurs de w et b qui rendent le y prévu le plus proche possible du y réel dans tous les exemples de formation.

> 目標: trouver la valeur de w 和 b, faire en sorte que tous les exercices de prédiction y 尽可能接近实际 y。

> **【中文解读】**
> Le modèle de la réintégration est très direct:`y = wx + b`,w est inclination, b est inclination, b est inclination, b est inclination, b est inclination, b est inclination, b est inclination, b est inclination, b est inclination, b est inclination, b est inclination, b est inclination, b est inclination, b est inclination, b est inclination, b est inclination, b est inclination, b est inclination, b est inclination, b est inclination, b est inclination, b est inclination, b est inclination, b est inclination, b est inclination, c est inclination, c est inclination, c est inclination, c est inclination, c est inclination, c est inclination, c est inclination, c est inclination, inclination, inclination, inclination, inclination, inclination, inclination, inclination, inclination, inclination, inclination, inclination, inclination, inclination, inclination, inclination, inclination, inclination, inclination, inclination, inclination, inclination, inclination, inclination, inclination, inclination, inclination, inclination, inclination, inclination, inclination, inclination, inclination, inclination, inclination, inclination, inclination, inclination, inclination, inclination, inclination, inclination, inclination, inclination, inclination, inclination, inclination, inclination, inclination, inclination, inclination, inclination, inclination, inclination, inclination, inclination, inclination, inclination, inclination, inclination, inclination, inclination, inclination, inclination, inclination, inclination, inclination, inclination, inclination, inclination, inclination, inclination, inclination, inclination, inclination, inclination, inclination, inclination, inclination`y = w1*x1 + w2*x2 + ... + wn*xn + b`L'objectif de l'entraînement est de trouver le meilleur w et b, afin de réduire la différence entre la valeur prévue et la valeur réelle.

### La fonction de coût (erreur moyenne carré)

Comment mesurer " le plus près possible " ? Vous avez besoin d'un seul nombre qui détecte à quel point vos prédictions sont erronées.

> Vous avez besoin d'un modèle capable de saisir une valeur unique de la mesure de l'erreur prévisible.

```
MSE = (1/n) * sum((y_predicted - y_actual)^2)
```

Pourquoi le carré? Deux raisons. Premièrement, il pénalise les erreurs importantes plus que les erreurs mineures (une erreur de 10 est 100 fois pire qu'une erreur de 1, pas 10x). Deuxièmement, la fonction carré est lisse et différenciable partout, ce qui facilite l'optimisation.

> Pourquoi utiliser le carré ? Deux raisons. D'abord, il pèse plus lourd sur les grandes erreurs que sur les petites erreurs.

La fonction de coût crée une surface. Pour un seul poids w et un biais b, la surface de l'ESM ressemble à un bol (un paraboloïde convexe).

> Pour un seul poids et une seule position b, le MSE le poids du bowl ressemble à un bowl.

### Descent graduel

La descente graduelle trouve le fond du bol en faisant des pas en descente.

> La descente est à la descente pour trouver le fond de la cuve.

```mermaid
flowchart TD
    A[Initialize w and b randomly] --> B[Compute predictions: y_hat = wx + b]
    B --> C[Compute cost: MSE]
    C --> D[Compute gradients: dMSE/dw, dMSE/db]
    D --> E[Update parameters]
    E --> F{Cost low enough?}
    F -->|No| B
    F -->|Yes| G[Done: optimal w and b found]
```

Les gradients vous disent deux choses: quelle direction déplacer chaque paramètre, et combien de déplacer.

> Le gradient vous dit deux choses: chaque paramètre devrait se déplacer dans quelle direction, ainsi que combien.

Pour les émissions de masse de masse avec y_hat = wx + b:

> 对于 MSE 且 y_hat = wx + b:

```
dMSE/dw = (2/n) * sum((y_hat - y) * x)
dMSE/db = (2/n) * sum(y_hat - y)
```

La règle de mise à jour:

> 更新规则:

```
w = w - learning_rate * dMSE/dw
b = b - learning_rate * dMSE/db
```

Le taux d'apprentissage contrôle la taille des étapes. Trop grand: vous dépassez le minimum et divergez. Trop petit: la formation prend toujours.

> Le taux d'apprentissage est très élevé: vous sautez au-delà de la valeur minimale et vous êtes très faible.

> **【中文解读】**
> Le degré de baisse est l'algorithme d'optimisation le plus central de l'apprentissage automatique. Son intuition est simple: se tenir sur une colline, aller vers le plus bas de la colline, aller un pas de plus en plus loin.

> **【拓展：梯度下降在现代 AI 中的演进】**
> Le GPT-4 est un système d'entraînement de haute variante de la température descendante. Le taux d'apprentissage commence à 0 avant la température de pointe, puis revient à la température descendante.

### L'équation normale (solution en forme fermée)

Pour la régression linéaire spécifiquement, il existe une formule directe qui donne les poids optimaux sans aucune itération:

> ), une formule directe qui peut donner le plus de poids:

```
w = (X^T * X)^(-1) * X^T * y
```

Il est préférable de faire une descente de gradient, car l'inversion de la matrice est O (n^3) dans le nombre de caractéristiques.

> Ceci est très efficace pour les petits ensembles de données. Pour les grands ensembles de données, le degré de baisse est plus élevé, car le nombre de caractéristiques est O (n^3)

> **【拓展：正规方程 vs 梯度下降的选择】**
> La complexité temporelle d'un équilibre normal est O (n^3) (n) (l) (n) (n) (n) (n) (n) (n) (n) (n) (n) (n) (n) (n) (n) (n) (n) (n) (n) (n) (n) (n) (n) (n) (n) (n) (n) (n) (n) (n) (n) (n) (n) (n) (n) (n) (n) (n) (n) (n) (n) (n) (n) (n) (n) (n) (n) (n) (n) (n) (n) (n) (n) (n) (n) (n) (n) (n) (n) (n) (n) (n) (n) (n) (n) (n) (n) (n) (n) (n) (n) (n) (n) (n) (n) (n) (n) (n) (n) (n) (n) (n) (n) (n) (n) (n) (n) (n) (n) (n) (n) (n) (n) (n) (n) (n) (n) (n) (n) (n) (n) (n) (n) (n) (n) (n) (n) (n) (n) (n) (n) (n) (n) (n) (n) (n) (n) (n) (n) (n) (n) (n) (n) (n) (n) (n) (n) (n) (n) (n) (n) (n) (n) (n) (n) (n) (n) (n) (n) (n) (n) (n) (n) (n) (n) (n) (n) (n) (n) (n) (n) (n) (n) (n) (n) (n) (n) (n) (n) (n) (n) (n) (n) (n)

### Régrésion linéaire multiple

Avec plusieurs caractéristiques, le modèle devient:

> Il y a plusieurs caractéristiques, le modèle change:

```
y = w1*x1 + w2*x2 + ... + wn*xn + b
```

Tout fonctionne de la même manière: MSE est la fonction de coût, la descente de gradient met à jour tous les poids simultanément.

> Tout est le même principe: le MSE est une fonction de prix, la gradience descend en même temps que le changement de tout le poids. La seule différence est que vous êtes en train de vous adapter à un super-plan et non à une ligne droite.

Si une caractéristique varie de 0 à 1 et une autre de 0 à 1 000 000, la baisse de gradient aura du mal à se faire parce que la surface des coûts devient allongée.

> Si une caractéristique est de 0 à 1, une autre est de 0 à 1,000,000, la baisse du degré devient difficile, car le prix est prolongé.

> **【中文解读】**
> Dans le processus de régression multiforme, la réduction des caractéristiques est essentielle. Si les différences de niveau de caractéristiques sont importantes, comme la taille de la pièce 500-3000 contre le nombre de chambres 1-5), la réduction des pertes de la fonction de régression de la taille est considérablement augmentée, ce qui entraîne une réduction de la réception, voire une incapacité de réception.

### Régrésion polynomielle

Et si la relation n'est pas linéaire ? Vous pouvez toujours utiliser la régression linéaire en créant des caractéristiques polynomielles:

> Si la relation n'est pas linéaire, vous pouvez continuer à utiliser la relation linéaire en créant plusieurs caractéristiques:

```
y = w1*x + w2*x^2 + w3*x^3 + b
```

C'est toujours une régression "linéaire" parce que le modèle est linéaire dans les poids (w1, w2, w3).

> Ceci est toujours "linéaire" car le modèle est en poids (w1, w2, w3) et est linéaire.

Les polynômes de degré supérieur peuvent s'adapter à des courbes plus complexes mais risquent de se surpasser. Un polynôme de degré 10 traversera tous les points d'un ensemble de données de 10 points mais prédira mal les nouvelles données.

> Un multijoint de 10 fois peut traverser 10 points de chaque ensemble de données, mais les prévisions sur les nouvelles données sont très médiocres.

### R-quadrés

Le MSE vous dit à quel point vous vous trompez, mais le nombre dépend de l'échelle de y. R-quadré (R^2) donne une mesure indépendante de l'échelle:

> Le MSE vous dit combien vous avez fait de erreurs, mais ce chiffre dépend de la taille de y. R-quadré (R^2) donne une taille qui n'est pas liée à la taille:

```
R^2 = 1 - (sum of squared residuals) / (sum of squared deviations from mean)
    = 1 - SS_res / SS_tot
```

- R^2 = 1,0: prédictions parfaites
  R^2 = 1,0:完美预测
- R^2 = 0,0: le modèle n'est pas meilleur que de prédire la moyenne à chaque fois
  R^2 = 0,0: modèle n'est pas comparable à la moyenne de prévision
- R^2 < 0,0: le modèle est pire que de prédire la moyenne
  R^2 < 0,0: modèle par rapport à la moyenne prévue

### Révision préliminaire de la régulation (régrésion de la vallée)

Lorsque vous avez de nombreuses caractéristiques, le modèle peut surpasser en attribuant de grands poids.

> Lorsque vous avez beaucoup de caractéristiques, le modèle peut être attribué un grand pouvoir pour être adapté.

```
Cost = MSE + lambda * sum(w_i^2)
```

Le terme de pénalité décourage les poids importants. L'hyperparamètre lambda contrôle le compromis: un lambda plus élevé signifie des poids plus petits et plus de régularisation.

> 惩罚项阻止权重过大──超参数 lambda 控制权衡:lambda 越大意味着权重越小、正则化越强── ceci sera discuté en profondeur dans le cours suivant── maintenant il suffit de comprendre son existence et son effet──

> **【中文解读】**
> Ridge Retour à la Ridge (Ridge Retour à la Ridge) L2 L2 L2 L2 L2 L2 L2 L2 L2 L2 L2 L2 L2 L2 L2 L2 L2 L2 L2 L2 L2 L2 L2 L2 L2 L2 L2 L2 L2 L2 L2 L2 L2 L2 L2 L2 L2 L2 L2 L2 L2 L2 L2 L2 L2 L2 L2 L2 L2 L2 L2 L2 L2 L2 L2 L2 L2 L2 L2 L2 L2 L2 L2 L2 L2 L2 L2 L2 L2 L2 L2 L2 L2 L2 L2 L2 L2 L2 L2 L2 L2 L2 L2 L2 L2 L2 L2 L2 L2 L2 L2 L2 L2 L2 L2 L2 L2 L2 L2 L2 L2 L2 L2 L2 L2 L2 L2 L2 L2 L2 L2 L2 L2 L2 L2 L2 L2 L2 L2 L2 L2 L2 L2 L2 L2 L2 L2 L2 L2 L2 L2 L2 L2 L2 L2 L2 L2 L2 L2 L2 L2 L2 L2 L2 L2 L2 L2 L2 L2 L2 L2 L2 L2 L2 L2 L2 L2 L2 L2 L2 L2 L2 L2 L2 L2 L2 L2 L2 L2 L2 L2 L2 L2 L2 L2 L2 L2 L2 L2 L2 L2 L2 L2 L2 L2 L2 L2 L2 L2 L2 L2 L2 L2 L2 L2 L2 L2 L2 L2 L2 L2 L2 L2 L2 L2 L2 L2 L2 L2 L2 L2 L2 L2 L2 L2 L2 L2 L2 L2 L2 L2 L2 L2 L2 L2 L2 L2 L2 L2 L2 L2 L2 L2 L2 L2 L2 L2 L2 L2 L2 L2 L2 L2 L2 L2

## Construisez-le et mettez-le en œuvre.
```figure
linear-regression-fit
```

## Faites-le

### Étape 1: Générer des données d'échantillon

```python
import random
import math

random.seed(42)  # 设置随机种子以确保结果可复现

TRUE_W = 3.0  # 真实斜率（权重）
TRUE_B = 7.0  # 真实截距（偏置）
N_SAMPLES = 100  # 样本数量

X = [random.uniform(0, 10) for _ in range(N_SAMPLES)]  # 生成 0-10 之间的随机特征值
y = [TRUE_W * x + TRUE_B + random.gauss(0, 2.0) for x in X]  # 真实关系 + 高斯噪声

print(f"Generated {N_SAMPLES} samples")
print(f"True relationship: y = {TRUE_W}x + {TRUE_B} (+ noise)")
print(f"First 5 points: {[(round(X[i], 2), round(y[i], 2)) for i in range(5)]}")
```

### Étape 2: Regression linéaire à partir de zéro avec descente de gradient

```python
class LinearRegression:
    def __init__(self, learning_rate=0.01):
        self.w = 0.0  # 权重初始化为 0
        self.b = 0.0  # 偏置初始化为 0
        self.lr = learning_rate  # 学习率控制梯度下降步长
        self.cost_history = []  # 记录每轮的损失值

    def predict(self, X):
        return [self.w * x + self.b for x in X]  # y_hat = wx + b

    def compute_cost(self, X, y):
        predictions = self.predict(X)
        n = len(y)
        # 计算 MSE：均方误差
        cost = sum((pred - actual) ** 2 for pred, actual in zip(predictions, y)) / n
        return cost

    def compute_gradients(self, X, y):
        predictions = self.predict(X)
        n = len(y)
        # 对 w 的偏导数
        dw = (2 / n) * sum((pred - actual) * x for pred, actual, x in zip(predictions, y, X))
        # 对 b 的偏导数
        db = (2 / n) * sum(pred - actual for pred, actual in zip(predictions, y))
        return dw, db

    def fit(self, X, y, epochs=1000, print_every=200):
        for epoch in range(epochs):
            dw, db = self.compute_gradients(X, y)  # 计算梯度
            self.w -= self.lr * dw  # 沿梯度反方向更新权重
            self.b -= self.lr * db  # 沿梯度反方向更新偏置
            cost = self.compute_cost(X, y)
            self.cost_history.append(cost)
            if epoch % print_every == 0:
                print(f"  Epoch {epoch:4d} | Cost: {cost:.4f} | w: {self.w:.4f} | b: {self.b:.4f}")
        return self

    def r_squared(self, X, y):
        predictions = self.predict(X)
        y_mean = sum(y) / len(y)
        ss_res = sum((actual - pred) ** 2 for actual, pred in zip(y, predictions))  # 残差平方和
        ss_tot = sum((actual - y_mean) ** 2 for actual in y)  # 总变差
        return 1 - (ss_res / ss_tot)  # R² = 1 - SS_res/SS_tot


print("=== Training Linear Regression (Gradient Descent) ===")
model = LinearRegression(learning_rate=0.005)
model.fit(X, y, epochs=1000, print_every=200)
print(f"\nLearned: y = {model.w:.4f}x + {model.b:.4f}")
print(f"True:    y = {TRUE_W}x + {TRUE_B}")
print(f"R-squared: {model.r_squared(X, y):.4f}")
```

### Étape 3: équation normale (solution en forme fermée)

```python
class LinearRegressionNormal:
    def __init__(self):
        self.w = 0.0  # 斜率
        self.b = 0.0  # 截距

    def fit(self, X, y):
        n = len(X)
        x_mean = sum(X) / n  # 计算 x 的均值
        y_mean = sum(y) / n  # 计算 y 的均值
        # 协方差 / 方差 = 最优斜率
        numerator = sum((X[i] - x_mean) * (y[i] - y_mean) for i in range(n))
        denominator = sum((X[i] - x_mean) ** 2 for i in range(n))
        self.w = numerator / denominator
        # 截距 = y 均值 - 斜率 * x 均值
        self.b = y_mean - self.w * x_mean
        return self

    def predict(self, X):
        return [self.w * x + self.b for x in X]

    def r_squared(self, X, y):
        predictions = self.predict(X)
        y_mean = sum(y) / len(y)
        ss_res = sum((actual - pred) ** 2 for actual, pred in zip(y, predictions))
        ss_tot = sum((actual - y_mean) ** 2 for actual in y)
        return 1 - (ss_res / ss_tot)


print("\n=== Normal Equation (Closed-Form) ===")
model_normal = LinearRegressionNormal()
model_normal.fit(X, y)
print(f"Learned: y = {model_normal.w:.4f}x + {model_normal.b:.4f}")
print(f"R-squared: {model_normal.r_squared(X, y):.4f}")
```

### Étape 4: Régrésion linéaire multiple

```python
class MultipleLinearRegression:
    def __init__(self, n_features, learning_rate=0.01):
        self.weights = [0.0] * n_features
        self.bias = 0.0
        self.lr = learning_rate
        self.cost_history = []

    def predict_single(self, x):
        return sum(w * xi for w, xi in zip(self.weights, x)) + self.bias

    def predict(self, X):
        return [self.predict_single(x) for x in X]

    def compute_cost(self, X, y):
        predictions = self.predict(X)
        n = len(y)
        return sum((pred - actual) ** 2 for pred, actual in zip(predictions, y)) / n

    def fit(self, X, y, epochs=1000, print_every=200):
        n = len(y)
        n_features = len(X[0])
        for epoch in range(epochs):
            predictions = self.predict(X)
            errors = [pred - actual for pred, actual in zip(predictions, y)]
            for j in range(n_features):
                grad = (2 / n) * sum(errors[i] * X[i][j] for i in range(n))
                self.weights[j] -= self.lr * grad
            grad_b = (2 / n) * sum(errors)
            self.bias -= self.lr * grad_b
            cost = self.compute_cost(X, y)
            self.cost_history.append(cost)
            if epoch % print_every == 0:
                print(f"  Epoch {epoch:4d} | Cost: {cost:.4f}")
        return self

    def r_squared(self, X, y):
        predictions = self.predict(X)
        y_mean = sum(y) / len(y)
        ss_res = sum((actual - pred) ** 2 for actual, pred in zip(y, predictions))
        ss_tot = sum((actual - y_mean) ** 2 for actual in y)
        return 1 - (ss_res / ss_tot)


random.seed(42)
N = 100
X_multi = []
y_multi = []
for _ in range(N):
    size = random.uniform(500, 3000)
    bedrooms = random.randint(1, 5)
    age = random.uniform(0, 50)
    price = 50 * size + 10000 * bedrooms - 1000 * age + 50000 + random.gauss(0, 20000)
    X_multi.append([size, bedrooms, age])
    y_multi.append(price)


def standardize(X):
    n_features = len(X[0])
    means = [sum(X[i][j] for i in range(len(X))) / len(X) for j in range(n_features)]
    stds = []
    for j in range(n_features):
        variance = sum((X[i][j] - means[j]) ** 2 for i in range(len(X))) / len(X)
        stds.append(variance ** 0.5)
    X_scaled = []
    for i in range(len(X)):
        row = [(X[i][j] - means[j]) / stds[j] if stds[j] > 0 else 0 for j in range(n_features)]
        X_scaled.append(row)
    return X_scaled, means, stds


y_mean_val = sum(y_multi) / len(y_multi)
y_std_val = (sum((yi - y_mean_val) ** 2 for yi in y_multi) / len(y_multi)) ** 0.5
y_scaled = [(yi - y_mean_val) / y_std_val for yi in y_multi]

X_scaled, x_means, x_stds = standardize(X_multi)

print("\n=== Multiple Linear Regression (3 features) ===")
print("Features: house size, bedrooms, age")
multi_model = MultipleLinearRegression(n_features=3, learning_rate=0.01)
multi_model.fit(X_scaled, y_scaled, epochs=1000, print_every=200)

print(f"\nWeights (standardized): {[round(w, 4) for w in multi_model.weights]}")
print(f"Bias (standardized): {multi_model.bias:.4f}")
print(f"R-squared: {multi_model.r_squared(X_scaled, y_scaled):.4f}")
```

### Étape 5: Regression polynomielle

```python
class PolynomialRegression:
    def __init__(self, degree, learning_rate=0.01):
        self.degree = degree
        self.weights = [0.0] * degree
        self.bias = 0.0
        self.lr = learning_rate

    def make_features(self, X):
        return [[x ** (d + 1) for d in range(self.degree)] for x in X]

    def predict(self, X):
        features = self.make_features(X)
        return [sum(w * f for w, f in zip(self.weights, row)) + self.bias for row in features]

    def fit(self, X, y, epochs=1000, print_every=200):
        features = self.make_features(X)
        n = len(y)
        for epoch in range(epochs):
            predictions = [sum(w * f for w, f in zip(self.weights, row)) + self.bias for row in features]
            errors = [pred - actual for pred, actual in zip(predictions, y)]
            for j in range(self.degree):
                grad = (2 / n) * sum(errors[i] * features[i][j] for i in range(n))
                self.weights[j] -= self.lr * grad
            grad_b = (2 / n) * sum(errors)
            self.bias -= self.lr * grad_b
            if epoch % print_every == 0:
                cost = sum(e ** 2 for e in errors) / n
                print(f"  Epoch {epoch:4d} | Cost: {cost:.6f}")
        return self

    def r_squared(self, X, y):
        predictions = self.predict(X)
        y_mean = sum(y) / len(y)
        ss_res = sum((actual - pred) ** 2 for actual, pred in zip(y, predictions))
        ss_tot = sum((actual - y_mean) ** 2 for actual in y)
        return 1 - (ss_res / ss_tot)


random.seed(42)
X_poly = [x / 10.0 for x in range(0, 50)]
y_poly = [0.5 * x ** 2 - 2 * x + 3 + random.gauss(0, 1.0) for x in X_poly]

x_max = max(abs(x) for x in X_poly)
X_poly_norm = [x / x_max for x in X_poly]
y_poly_mean = sum(y_poly) / len(y_poly)
y_poly_std = (sum((yi - y_poly_mean) ** 2 for yi in y_poly) / len(y_poly)) ** 0.5
y_poly_norm = [(yi - y_poly_mean) / y_poly_std for yi in y_poly]

print("\n=== Polynomial Regression (degree 2 vs degree 5) ===")
print("True relationship: y = 0.5x^2 - 2x + 3")

print("\nDegree 2:")
poly2 = PolynomialRegression(degree=2, learning_rate=0.1)
poly2.fit(X_poly_norm, y_poly_norm, epochs=2000, print_every=500)
print(f"  R-squared: {poly2.r_squared(X_poly_norm, y_poly_norm):.4f}")

print("\nDegree 5:")
poly5 = PolynomialRegression(degree=5, learning_rate=0.1)
poly5.fit(X_poly_norm, y_poly_norm, epochs=2000, print_every=500)
print(f"  R-squared: {poly5.r_squared(X_poly_norm, y_poly_norm):.4f}")

print("\nDegree 2 fits the true curve well. Degree 5 fits training data slightly better")
print("but risks overfitting on new data.")
```

### Étape 6: régression de la montée (régularisation de la L2)

```python
class RidgeRegression:
    def __init__(self, n_features, learning_rate=0.01, alpha=1.0):
        self.weights = [0.0] * n_features
        self.bias = 0.0
        self.lr = learning_rate
        self.alpha = alpha

    def predict_single(self, x):
        return sum(w * xi for w, xi in zip(self.weights, x)) + self.bias

    def predict(self, X):
        return [self.predict_single(x) for x in X]

    def fit(self, X, y, epochs=1000, print_every=200):
        n = len(y)
        n_features = len(X[0])
        for epoch in range(epochs):
            predictions = self.predict(X)
            errors = [pred - actual for pred, actual in zip(predictions, y)]
            mse = sum(e ** 2 for e in errors) / n
            reg_term = self.alpha * sum(w ** 2 for w in self.weights)
            cost = mse + reg_term
            for j in range(n_features):
                grad = (2 / n) * sum(errors[i] * X[i][j] for i in range(n))
                grad += 2 * self.alpha * self.weights[j]
                self.weights[j] -= self.lr * grad
            grad_b = (2 / n) * sum(errors)
            self.bias -= self.lr * grad_b
            if epoch % print_every == 0:
                print(f"  Epoch {epoch:4d} | Cost: {cost:.4f} | L2 penalty: {reg_term:.4f}")
        return self


print("\n=== Ridge Regression (L2 Regularization) ===")
print("Same data as multiple regression, with alpha=0.1")
ridge = RidgeRegression(n_features=3, learning_rate=0.01, alpha=0.1)
ridge.fit(X_scaled, y_scaled, epochs=1000, print_every=200)
print(f"\nRidge weights: {[round(w, 4) for w in ridge.weights]}")
print(f"Plain weights: {[round(w, 4) for w in multi_model.weights]}")
print("Ridge weights are smaller (shrunk toward zero) due to the L2 penalty.")
```

## Utilisez-le avec le cadre de réalisation

Il en va de même avec le scikit-learn, que vous allez utiliser dans la production.

> Maintenant, avec un petit apprentissage, vous pouvez réaliser la même fonction, c'est l'outil que vous utilisez en production.

```python
from sklearn.linear_model import LinearRegression as SklearnLR
from sklearn.linear_model import Ridge
from sklearn.preprocessing import PolynomialFeatures, StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score
import numpy as np

# 生成与从零实现相同的数据
np.random.seed(42)
X_sk = np.random.uniform(0, 10, (100, 1))
y_sk = 3.0 * X_sk.squeeze() + 7.0 + np.random.normal(0, 2.0, 100)

# 划分训练集和测试集（80/20）
X_train, X_test, y_train, y_test = train_test_split(X_sk, y_sk, test_size=0.2, random_state=42)

# 线性回归
lr = SklearnLR()
lr.fit(X_train, y_train)
y_pred = lr.predict(X_test)

print("=== Scikit-learn Linear Regression ===")
print(f"Coefficient (w): {lr.coef_[0]:.4f}")
print(f"Intercept (b): {lr.intercept_:.4f}")
print(f"R-squared (test): {r2_score(y_test, y_pred):.4f}")
print(f"MSE (test): {mean_squared_error(y_test, y_pred):.4f}")

# 多项式回归（degree=2）
poly = PolynomialFeatures(degree=2, include_bias=False)
X_poly_sk = poly.fit_transform(X_train)  # 生成 x, x² 特征
X_poly_test = poly.transform(X_test)

lr_poly = SklearnLR()
lr_poly.fit(X_poly_sk, y_train)
print(f"\nPolynomial degree 2 R-squared: {r2_score(y_test, lr_poly.predict(X_poly_test)):.4f}")

# 标准化后使用 Ridge 回归
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)  # 在训练集上拟合并转换
X_test_scaled = scaler.transform(X_test)  # 在测试集上只转换

ridge = Ridge(alpha=1.0)  # alpha 即正则化强度 lambda
ridge.fit(X_train_scaled, y_train)
print(f"Ridge R-squared: {r2_score(y_test, ridge.predict(X_test_scaled)):.4f}")
print(f"Ridge coefficient: {ridge.coef_[0]:.4f}")
```

La différence: scikit-learn gère les cas de bord, la stabilité numérique et les optimisations de performance. Utilisez la bibliothèque pour la production. Utilisez la version de scratch pour comprendre ce qui se passe.

> La différence réside dans le fait que le processus de réalisation et de démarrage de l'apprentissage produit les mêmes résultats.

## Envoyez-le . Produit .

Cette leçon donne:
- `outputs/skill-regression.md`- une aptitude à choisir la bonne approche de régression en fonction du problème

> Le programme de formation
> - `outputs/skill-regression.md`- une compétence de choix de méthode de retour

## Les exercices

1. Appliquez la baisse de gradient de lot, la baisse de gradient stochastique (SGD) et la baisse de gradient de mini lot. Comparer la vitesse de convergence sur le même ensemble de données.
   1. 实现批量梯度下降,随机梯度下降 (SGD) 和小批量梯度下降.                                                                                                                                                                                                                                                 
2. Générer des données à partir d'une fonction cubique (y = ax^3 + bx^2 + cx + d + bruit).
   2. De trois fonctions (y = ax^3 + bx^2 + cx + d + bruit) 生成数据──拟合 1、3 和 10 次多项式──比较训练 R^2 和测试 R^2──几次多项式时过拟合变得明显吗?
3. Implémenter la régression Lasso (régularisation L1: pénalité * alpha *( sur le direw_i i i i i)). Trainer les données de logement multi-factores. Comparer les poids qui vont à zéro par rapport à Ridge. Pourquoi L1 produit des solutions rares alors que L2 ne le fait pas?
   3. 实现 Lasso 回归(L1 正则化:penalty * alpha sum *(((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((

## Les termes clés

| Term | What people say | What it actually means |
|------|----------------|----------------------|
| Linear regression | "Draw a line through data" | Find weight w and bias b that minimize the sum of squared differences between wx+b and actual y values |
| Cost function | "How bad the model is" | A function that maps model parameters to a single number measuring prediction error, which optimization minimizes |
| Mean squared error | "Average of squared errors" | (1/n) * sum of (predicted - actual)^2, penalizing large errors disproportionately |
| Gradient descent | "Walk downhill" | Iteratively adjust parameters in the direction that reduces the cost function, using partial derivatives |
| Learning rate | "Step size" | A scalar that controls how much parameters change per gradient descent step |
| Normal equation | "Solve it directly" | The closed-form solution w = (X^T X)^-1 X^T y that gives optimal weights without iteration |
| R-squared | "How good the fit is" | The fraction of variance in y explained by the model, ranging from negative infinity to 1.0 |
| Feature scaling | "Make features comparable" | Transforming features to similar ranges (e.g., zero mean, unit variance) so gradient descent converges faster |
| Regularization | "Penalize complexity" | Adding a term to the cost function that shrinks weights, preventing overfitting |
| Ridge regression | "L2 regularization" | Linear regression with a penalty of lambda * sum(w_i^2) added to MSE |
| Polynomial regression | "Fitting curves with linear math" | Linear regression on polynomial features (x, x^2, x^3, ...), still linear in the weights |
| Overfitting | "Memorizing training data" | Using a model so complex that it fits noise in training data and fails on new data |

## Encore une lecture

- [An Introduction to Statistical Learning (ISLR)](https://www.statlearning.com/)-- PDF gratuit, les chapitres 3 et 6 couvrent la régression linéaire et la régularisation avec des exemples pratiques de R
  [An Introduction to Statistical Learning (ISLR)](https://www.statlearning.com/)-- 免费教材, Chapitre 3 et Chapitre 6 avec des exemples réels de R couvrant la régénération et la normalisation
- [The Elements of Statistical Learning (ESL)](https://hastie.su.domains/ElemStatLearn/)-- PDF gratuit, le compagnon plus mathématique de l'IRL avec un traitement plus profond de la crête et du lasso
  [The Elements of Statistical Learning (ESL)](https://hastie.su.domains/ElemStatLearn/)-- 免费教材,ISLR's maths version, pour la crête et les lasso il y a un traitement plus approfondi
- [Stanford CS229 Lecture Notes on Linear Regression](https://cs229.stanford.edu/main_notes.pdf)-- Les notes d'Andrew Ng déduisant l'équation normale et la descente des gradients à partir des premiers principes
  [Stanford CS229 Lecture Notes on Linear Regression](https://cs229.stanford.edu/main_notes.pdf)-- Andrew Ng's notes de la première nature du principe de la régularité et de la dégradation des degrés
- [scikit-learn LinearRegression documentation](https://scikit-learn.org/stable/modules/linear_model.html)-- référence pratique pour LinearRegression, Ridge, Lasso et ElasticNet avec des exemples de code
  [scikit-learn LinearRegression documentation](https://scikit-learn.org/stable/modules/linear_model.html)-- L'exemple de référence et de code pratique de LinearRegression、Ridge、Lasso 和 ElasticNet
