# Stabilité numérique , stabilité numérique .

> Le point flottant est une abstraction fuyant.
> Le nombre de points de fuite est un extrait de la fuite. Il vous mordra pendant l'entraînement, mais vous ne le verrez pas arriver.

**Type:** Build | **类型:** 动手
**Language:**Je suis un Python .**语言:**Python
**Prerequisites:** Phase 1, Lessons 01-04 | **前置知识:** Phase 1, Lessons 01-04
**Time:** ~120 minutes | **时间:** ~120 分钟

## Objectifs d'apprentissage

- Implémenter le softmax et le log-sum-exp stables numériquement en utilisant le truc de soustraction max
  Utiliser des techniques de réduction de la valeur maximale pour réaliser la valeur stable de la valeur douce max et log-sum-exp
- Identifier les débordements, les débordements et les annulations catastrophiques dans les calculs des points flottants
  Identification des débordements et des catastrophes
- Vérifiez les gradients analytiques contre les gradients numériques en utilisant des différences finites centrées
  Uzzcenter limité différence de vérification de la résolution de la échelle
- Expliquez pourquoi bfloat16 est préféré à float16 pour l'entraînement et comment l'évolutivité des pertes empêche le sous-flux de la gradiente
  Expliquer pourquoi le bfloat16 est plus adapté à l'entraînement que le float16 et comment prévenir la dégradation des températures

> **【中文解读】**
> 浮点数是漏水的抽象──训练 3 小时后损失 变 NaN 变 NaN 变 NaN 变 NaN 变 NaN 变 NaN 变 NaN 变 NaN 变 NaN 变 NaN 变 NaN 变 NaN 变 NaN 变 NaN 变 NaN 变 NaN 变 NaN 变 NaN 变 NaN 变 NaN 变 NaN 变 NaN 变 NaN 变 NaN 变 NaN 变 NaN 变 NaN 变 NaN 变 NaN 变 NaN 变 NaN 变 NaN 变 NaN 变 NaN 变 NaN 变 NaN 变 NaN 变 NaN 变 NaN 变 NaN 变 NaN 变 NaN 变 NaN 变 NaN 变 NaN 变 NaN 变 NaN 变 NaN 变 NaN 变 NaN 变 NaN 变 NaN 变 NaN 变 NaN 变 NaN 变 NaN 变 NaN 变 NaN 变 NaN 变 NaN 变 NaN 变 NaN 变 NaN 变 NaN 变 NaN 变 NaN 变 NaN 变 NaN 变 NaN 变 NaN 变 NaN 变 NaN 变 NaN 变 NaN 变 NaN 变 NaN 变 NaN 变 NaN 变 NaN 变 NaN 变 NaN 变 NaN 变 Na n 变 Na n                                                                                                                                                           

## Le problème , l' introduction du problème

> **【中文解读】**Trois types de catastrophe de stabilité numérique: 1) entraînement 3 heures après la perte 变 NaN某步计算溢出; 2) précision par rapport au résumé de 2% float16 累积舍入差吃掉准确率; 3) autodéclaration 交叉大逻辑 时返回 infsoftmax 溢出──

Vous ajoutez une déclaration d'impression. Les logits sont bons à l'étape 9.000.`inf`Par étape 9,002 chaque gradient est`nan`et l'entraînement est mort.
> Vous avez ajouté une imprimante. Les logs sont retournés à la normale.`inf`Jusqu'à la 9e étape, tous les niveaux sont`nan`L'entraînement est mort.

Ou: votre modèle est prêt à être terminé mais la précision est 2% pire que les revendications du papier. Vous vérifiez tout. L'architecture correspond. Les hyperparametres correspondent. Les données correspondent. Le problème est que le papier a utilisé float32 et que vous avez utilisé float16 sans l'échelle correcte.
> Ou: le modèle de formation est terminé mais l'exactitude du thème est de 2%. Vous avez tout vérifié.

Ou: vous mettez en œuvre la perte de l'entropie croisée à partir de zéro. Cela fonctionne sur de petits logits. Lorsque les logits dépassent 100, il revient`inf`Le softmax a débordé parce que`exp(100)`Tout système de gestion de la machine à écrire traite cela avec un truc à deux lignes.
> Ou: tu as réalisé une perte de temps.`inf`Le softmax est en train de s'écouler.`exp(100)`超越了 float32 的表示范围──

La stabilité numérique n'est pas une préoccupation théorique. C'est la différence entre une course d'entraînement qui réussit et une course qui échoue silencieusement.
> La stabilité numérique n'est pas une question théorique. Elle est la différence entre le succès de l'entraînement et le défaut de la silence.

## Le concept de base.

> **【拓展：Softmax 的数值稳定技巧是面试必考题】**Pour les produits de la production de la fibre de verre`softmax(x) = exp(x) / sum(exp(x))`, quand x est en moyenne avec une grande valeur , exp 溢出――解法: diminution de la valeur maximale `softmax(x) = exp(x - max(x)) / sum(exp(x - max(x)))`Le résultat mathématique est constant mais la valeur est stable.`F.cross_entropy`L'utilisation interne de log-softmax et non séparée de calcul, c'est la raison.

### IEEE 754: Comment les ordinateurs stockent les nombres réels

Les ordinateurs stockent les nombres réels en tant que valeurs de point flottant selon la norme IEEE 754.
> 计算机根据 IEEE 754 标准将实数存储为浮点值──浮点数有三部分:符号位、指数和尾数──

```
Float32 layout (32 bits total):
[1 sign] [8 exponent] [23 mantissa]

Value = (-1)^sign * 2^(exponent - 127) * 1.mantissa
```

La mantissa détermine la précision (combien de chiffres significatifs).
> 尾数决定精度 (numéro de nombre) 尾数决定精度 (numéro de nombre) 尾数决定精度 (numéro de nombre) 尾数决定精度 (numéro de nombre) 尾数决定精度 (numéro de nombre) 尾数决定精度 (numéro de nombre) 尾数决定精度 (numéro de nombre) 尾数决定精度 (numéro de nombre) 尾数决定精度 (numéro de nombre) 尾数决定精度 (numéro de nombre) 尾数决定精度 (numéro de nombre) 尾数决定精度 (numéro de nombre) 尾数可以多大多多多多多多多多多多多多小) △

```
Format     Bits   Exponent  Mantissa  Decimal digits  Range (approx)
float64    64     11        52        ~15-16          +/- 1.8e308
float32    32     8         23        ~7-8            +/- 3.4e38
float16    16     5         10        ~3-4            +/- 65,504
bfloat16   16     8         7         ~2-3            +/- 3.4e38
```

float32 vous donne environ 7 chiffres décimaux de précision. float16 vous donne environ 3 chiffres. bfloat16 est la réponse de Google au problème de portée de float16 - le même exponent de 8 bits que float32 mais seulement 7 bits mantissa. Pour l'entraînement des réseaux neuronaux, la portée compte plus que la précision, donc bfloat16 gagne généralement.
> float32  vous donne environ 7 places 进制精度──float16 约 3 places──bfloat16 est la réponse de Google à la question float16 范围 avec un indice de 8 places similaire à float32 mais seulement 7 places 尾数── entraînement

### Pourquoi 0,1 + 0,2 ! = 0,3 . Pourquoi 0,1 + 0,2 ! = 0,3

Le nombre 0,1 ne peut pas être représenté exactement dans le point flottant binaire.
> 0.1 En effet, dans le système de floatation, il est impossible de préciser le nombre de float32 en fonction du cycle.

```
In Python:
>>> 0.1 + 0.2
0.30000000000000004

>>> 0.1 + 0.2 == 0.3
False
```

Ceci est important pour ML parce que: (1) Les comparaisons de pertes comme `if loss < threshold`Les tests de vérification et de reproductibilité échouent si vous comparez les floats avec les autres.`==`La solution: ne comparez jamais les flottants avec`==`- Utilisez`abs(a - b) < epsilon`ou `math.isclose()`- Je suis désolé .
> Ceci est important pour ML: 1) la perte de comparaison peut être une erreur.`==`Comparer avec le nombre de points de l'épreuve et de l'essai va échouer.`==`Comparé au nombre de points.

### L' annulation catastrophique est annulée.

Lorsque vous soustraisez deux nombres de points flottants presque égaux, les chiffres significatifs s'annulent et vous êtes laissé avec le bruit arrondissant promu à des chiffres de premier plan.
> Lorsque vous diminuez le nombre de points de décalage de deux phases proches, le nombre valide de chiffres est négligé, le nombre de places de bruit est élevé à un nombre de chiffres de décalage.

```
a = 1.0000001    (stored as 1.00000011920929 in float32)
b = 1.0000000    (stored as 1.00000000000000 in float32)

True difference:  0.0000001
Computed:         0.00000011920929

Relative error: 19.2%
```

La solution: réorganiser les formules pour éviter de soustraire de grands nombres presque égaux. Pour la variance, utilisez l'algorithme Welford ou centrez les données en premier.
> 修复: Réarrangement des formules pour éviter de réduire le nombre de grandes approximations ⋅ calculer la différence en utilisant l'algorithme Welford ⋅ données centralisées préalables ⋅

### Les débordements et les débordements

Le surcoulant se produit lorsqu'un résultat est trop grand pour être représenté.
> Le résultat est trop grand pour être exprimé, le résultat est trop petit.

```
Float32 boundaries:
  Maximum:  3.4028235e+38
  Overflow:  anything > 3.4e38 becomes inf
  Underflow: anything < 1.4e-45 becomes 0.0

exp(88.7)  = 3.40e+38   (barely fits in float32)
exp(89.0)  = inf         (overflow)
```

En ML, `exp()`apparaît dans les calculs softmax, sigmoid et probabilité. `log()`apparaît dans les cas de croisée entropie, de probabilités de logement et de divergence KL.
> Dans le milieu de la ML,`exp()`Il est présent dans le calcul de la température de la température de la température de l'air.`log()`Il est présent dans le milieu de la distribution.

### Le truc de l'expérience log-sum-exp

L' informatique `log(sum(exp(x_i)))`Le truc: soustraire la valeur maximale avant d'exposer.
> 直接计算 `log(sum(exp(x_i)))`Résultats de la recherche:

```
log(sum(exp(x_i))) = max(x) + log(sum(exp(x_i - max(x))))
```

Pourquoi cela fonctionne-t-il: après soustraction `max(x)`, le plus grand exponent est `exp(0) = 1`- Aucun débordement n'est possible. Au moins un terme de la somme est 1, donc la somme est au moins 1, et`log(1) = 0`- Pas de sous-couleurs .`-inf`C'est possible.
> Pourquoi ?`max(x)`后, le plus grand nombre est `exp(0) = 1` Impossible de dépasser                                                                                                                                                                                                                                                           `log(1) = 0`Il est impossible de tomber dessus.`-inf`Il y a une autre.

Ce truc apparaît partout dans ML: normalisation de la douceur maximale, perte de l'entropie croisée, somme de probabilité logistique, mélange de Gaussiens, inférence variationnelle.
> Cette technique est présente dans le ML:softmax 归化、交叉损失、对数概率求和、高斯混合、变分推断──

### Pourquoi Softmax a besoin de la technique de soustraction maximale ?

Sans le truc, les logites de [100, 101, 102] provoquent un débordement.
> Il y a des problèmes de logement, des logements [100, 101, 102], des logements [100, 102], des logements [100, 101, 102], des logements [100, 102], des logements [100, 102], des logements [100, 102], des logements [100, 102], des logements [100, 102], des logements [100, 102], 102], 102, 102, 102], 102, 102, 102, 102, 102, 102, 102, 102, 102, 102, 102, 102, 102, 102, 102, 102, 102, 102, 102, 102, 102, 102, 102, 102, 102, 102, 102, 102, 102, 102, 102, 102, 102, 102, 102, 102, 102, 102, 102, 102, 102, 102, 102, 102, 102, 103, 103, 103, 103, 103, 103, 103, 103, 103, 103, 103, 103, 103, 103, 103, 103, 103, 103, 103, 103, 103, 103, 103, 103, 103, 103, 103, 103, 103, 103, 103, 103, 103, 103, 103, 103, 103, 103, 103, 103, 103, 103, 103, 103, 103, 103, 103, 103, 103, 103, 103, 103, 103, 103, 103, 103, 103, 103, 103, 103, 103, 103, 103, 103, 103, 103, 103, 103, 103, 103, 103, 103, 103, 103, 103, 103, 103, 103, 103, 103, 103, 103, 103, 103, 103, 103, 103, 103, 103, 103, 103, 103, 103, 103, 103, 103, 103, 103, 103, 103, 103, 103, 103, 103, 103, 103, 103, 103, 103, 103, 103, 103, 103, 103, 103, 103, 103, 103, 103, 103, 103, 103, 103, 103, 103, 103, 103, 103, 103, 103, 103, 103, 103, 103, 103, 103, 103, 103, 103, 103, 103, 103, 103, 103, 103, 103, 103, 103, 103, 103, 103, 103, 103, 103, 103, 103, 103, 103,

```
exp(100 - 102) = exp(-2) = 0.135
exp(101 - 102) = exp(-1) = 0.368
exp(102 - 102) = exp(0)  = 1.000
sum = 1.503

softmax = [0.090, 0.245, 0.665]
```

Les probabilités sont identiques, le calcul est sûr, ce n'est pas une optimisation, c'est une exigence de précision.
> La probabilité est la même.

### NaN et Inf: détection et prévention

`nan`et `inf`se propage viralement par le calcul.`nan`dans une mise à jour de gradient fait le poids `nan`, qui produit toutes les sorties ultérieures `nan`L'entraînement est mort en une seule étape.
> `nan`et `inf`通过计算病毒式传播――梯度更新中的一个 `nan`Pour faire le changement`nan`, faire le changement de toutes les sorties`nan`- Une étape de formation est morte.

Comment ?`nan`apparaît: `0.0 / 0.0`- Je suis là .`inf - inf`- Je suis là .`inf * 0`- Je suis là .`sqrt()`de négatif, `log()`La prévention: les entrées de clampage à`exp()`, ajouter de l'epsilon aux dénominateurs, utiliser des implémentations stables, couper le gradient.
> `nan`如何出现:`0.0/0.0`- Je suis là.`inf-inf`- Je suis là.`inf*0`、 négatif `sqrt()`、 négatif `log()` prévention: limite`exp()`输入、给分母加 epsilon、使用稳定实现、梯度剪

### Vérifie le degré numérique de la valeur numérique

Les gradients analytiques (de la propagation en arrière) peuvent avoir des bugs.
> 解析梯度 (from the opposite direction of propagation) peut avoir un bug.

```
df/dx ~= (f(x + h) - f(x - h)) / (2h)
```

Règles générales: relative_error < 1e-7: parfait; < 1e-5: acceptable; > 1e-3: quelque chose ne va pas; > 1: complètement faux.
> 经验法则:相对错误 < 1e-7:完美; < 1e-5:可接受;> 1e-3:有问题;> 1:完全错误──

### Une formation de précision mixte.

Les GPU modernes ont des cœurs tensors qui calculent les multiplication de la matrice float16 2 à 8 fois plus rapidement que float32.
> Le GPU moderne a un noyau de tension, float16 矩阵乘法比 float32 快 2-8 倍──混合精度训练利用这一点──

```
1. Maintain float32 master copy of weights
2. Forward pass in float16 (fast)
3. Compute loss in float32 (prevents overflow)
4. Backward pass in float16 (fast)
5. Scale gradients to float32
6. Update float32 master weights
```

La solution pour le sous-flow float16 est l'échelle des pertes: multiplier la perte par un facteur à grande échelle, passer en arrière compute des gradients plus grands, diviser par échelle avant de mettre à jour les poids.
> La réparation de float16 est une réduction de perte: la réduction de perte est multipliée par un facteur de réduction de la charge, la réduction de la charge est multipliée par un facteur de réduction de la charge, la réduction de la charge est augmentée par un facteur de réduction de la charge.

### Pourquoi bfloat16 contre float16: Pourquoi bfloat16 gagne pour l'entraînement

Le float16 a une précision plus élevée (10 bits de mantissa) mais une portée limitée (max. ~65,504). le float16 a une précision moins élevée mais une portée plus élevée que le float32 (max. ~3.4e38).
> Le nombre de floats est limité, mais le nombre de floats est limité.

### - Je suis en train de faire une coupe.

Les gradients explosants se produisent lorsque les gradients augmentent de façon exponentielle. Deux types de clips: clip par valeur (clamper chaque élément) et clip par norme (échelle de vecteur entier de sorte que sa norme ne dépasse pas un seuil).`torch.nn.utils.clip_grad_norm_()`- Il le fait.
> 梯度爆炸 occurs dans la croissance de l'indice de gradience.                                                                                                                                                                                                                                                      

Vérités typiques: `max_norm=1.0`pour les transformateurs, `max_norm=0.5`pour RL, `max_norm=5.0`pour des réseaux plus simples.
> 典型值: transformateur UZ `max_norm=1.0`, RL utilisez `max_norm=0.5`, simple utilisation du réseau `max_norm=5.0`Il y a une autre.

### Les bugs numériques ML sont courants

**Bug: Loss is NaN after a few epochs.**Cause: les logits trop grands, le softmax débordé.
> **Bug: 几个 epoch 后 loss 变 NaN。**原因:logits 太大,softmax 溢出──修复:使用稳定softmax,降低学习率,添加梯度剪──

**Bug: Validation accuracy is lower by 1-3%.**Cause: précision mixte sans mise à l'échelle de perte correcte.
> **Bug: 验证精度低 1-3%。**原因:混合精度没有正确的损失缩放──修复: activation动态损失缩放, ou changement à bfloat16──

**Bug: `exp()` returns `inf` in loss computation.**Réparation: utilisation `torch.nn.functional.log_softmax()`qui implémentent log-sum-exp en interne.
> **Bug: 损失计算中 `exp()` 返回 `inf`。**修复: utiliser `torch.nn.functional.log_softmax()`Il y a une autre.

## Construisez-le et mettez-le en œuvre.

### Étape 1: Démontre les limites de précision des points flottants
**Bug: Validation accuracy is lower than expected by 1-3%.**
Cause: précision mixte sans mise à l'échelle des pertes.
Réparation: activer l'évolutivité dynamique des pertes ou passer à bfloat16.

**Bug: Gradient norms are 0.0 for some layers.**
Cause: neurones morts de ReLU (toutes les entrées négatives) ou sous-flux float16.
Réparation: utiliser LeakyReLU ou GELU, utiliser l'échelle des gradients, vérifier l'initialisation du poids.

**Bug: Model works on one GPU but gives different results on another.**
Cause: ordre d'accumulation de points flottants non déterministe. Les réductions parallèles de la GPU sont la somme de différents ordres sur différents matériels, et l'ajout de points flottants n'est pas associatif.
Fix: accepter les petites différences (1e-6), ou définir `torch.use_deterministic_algorithms(True)`et acceptez la pénalité de vitesse.

**Bug: `exp()` returns `inf` in loss computation.**
Cause: les logits bruts sont passés à `exp()`sans le truc de soustraction maximale.
Réparation: utilisation `torch.nn.functional.log_softmax()`qui implémentent log-sum-exp en interne.

**Bug: Training diverges after switching from float32 to float16.**
Cause: float16 ne peut pas représenter des magnitudes de gradient inférieures à 6e-8 ou des activations supérieures à 65,504.
Réparation: utiliser une précision mixte avec une mise à l'échelle des pertes (AMP) ou utiliser bfloat16 à la place.

```figure
logsumexp-stability
```

## Faites-le

### Étape 1: démontrer les limites de précision des points flottants

```python
print("=== Floating Point Precision ===")
print(f"0.1 + 0.2 = {0.1 + 0.2}")
print(f"0.1 + 0.2 == 0.3? {0.1 + 0.2 == 0.3}")
print(f"Difference: {(0.1 + 0.2) - 0.3:.2e}")
```

### Étape 2: Implémenter naïf contre stable softmax.

```python
import math

def softmax_naive(logits):
    exps = [math.exp(z) for z in logits]
    total = sum(exps)
    return [e / total for e in exps]

def softmax_stable(logits):
    max_logit = max(logits)
    exps = [math.exp(z - max_logit) for z in logits]
    total = sum(exps)
    return [e / total for e in exps]

safe_logits = [2.0, 1.0, 0.1]
print(f"Naive:  {softmax_naive(safe_logits)}")
print(f"Stable: {softmax_stable(safe_logits)}")

dangerous_logits = [100.0, 101.0, 102.0]
print(f"Stable: {softmax_stable(dangerous_logits)}")
# softmax_naive(dangerous_logits) would return [nan, nan, nan]
```

### Étape 3: Implémenter une log-sum-exp stable

```python
def logsumexp_stable(values):
    c = max(values)
    return c + math.log(sum(math.exp(v - c) for v in values))
```

### Étape 4: Implémenter une entropie croisée stable.

```python
def cross_entropy_stable(true_class, logits):
    max_logit = max(logits)
    shifted = [z - max_logit for z in logits]
    log_sum_exp = math.log(sum(math.exp(s) for s in shifted))
    log_prob = shifted[true_class] - log_sum_exp
    return -log_prob
```

### Étape 5: vérification progressive.

```python
def numerical_gradient(f, x, h=1e-5):
    grad = []
    for i in range(len(x)):
        x_plus = x[:]
        x_minus = x[:]
        x_plus[i] += h
        x_minus[i] -= h
        grad.append((f(x_plus) - f(x_minus)) / (2 * h))
    return grad

def check_gradient(analytical, numerical, tolerance=1e-5):
    for i, (a, n) in enumerate(zip(analytical, numerical)):
        denom = max(abs(a), abs(n), 1e-8)
        rel_error = abs(a - n) / denom
        status = "OK" if rel_error < tolerance else "FAIL"
        print(f"  param {i}: analytical={a:.8f} numerical={n:.8f} "
              f"rel_error={rel_error:.2e} [{status}]")
```

## Utilisez-le avec le cadre de réalisation

Regardez !`code/numerical.py`pour des mises en œuvre complètes avec toutes les situations de bord démontrées.
> 完整实现见 `code/numerical.py`Il y a une autre.

```python
# 梯度裁剪
def clip_by_norm(gradients, max_norm):
    total_norm = math.sqrt(sum(g**2 for g in gradients))
    if total_norm > max_norm:
        scale = max_norm / total_norm
        return [g * scale for g in gradients]
    return gradients

# NaN/Inf 检测
def check_tensor(name, values):
    has_nan = any(math.isnan(v) for v in values)
    has_inf = any(math.isinf(v) for v in values)
    if has_nan or has_inf:
        print(f"WARNING {name}: nan={has_nan} inf={has_inf}")
        return False
    return True
```

## Envoyez-le . Produit .

Cette leçon donne:
> Le programme de formation

- `code/numerical.py`avec une douceur stable, une log-sum-exp, une entropie croisée, une vérification des gradients et une simulation de précision mixte
  包含 stable softmax ✓ log-sum-exp ✓交叉 ✓ échelle de vérification et mélange d'excision
- `outputs/prompt-numerical-debugger.md`pour le diagnostic de la NA/INF et des problèmes numériques dans la formation
  Utilisation de la question de la valeur et de la valeur de la NaN/Inf dans la formation de diagnostic

## Les exercices

1. **Catastrophic cancellation.**Comptez la variance de [1000000.0, 1000001.0, 1000002.0] en utilisant la formule naïve `E[x^2] - E[x]^2`Comparer les erreurs avec la variance réelle (0,6667).
   **灾难性抵消。**Utilisation de la simple formule et de l'algorithme Welford pour calculer les différences de la différence de la différence de la différence de la différence de la différence de la différence de la différence de la différence de la différence de la différence de la différence de la différence de la différence de la différence de la différence de la différence de la différence de la différence de la différence de la différence de la différence de la différence de la différence de la différence de la différence de la différence de la différence de la différence de la différence de la différence de la différence de la différence.

2. **Precision hunt.**Trouvez la plus petite valeur positive float32 `x`comme ça .`1.0 + x == 1.0`- Vérifiez qu' il correspond .`numpy.finfo(numpy.float32).eps`- Je suis désolé .
   **精度搜索。**找到使 `1.0 + x == 1.0`La valeur de la float 32 est la plus faible.

3. **Log-sum-exp edge cases.**Testez votre`logsumexp_stable`fonction avec: a) toutes les valeurs égales, b) une valeur beaucoup plus grande que les autres, c) toutes les valeurs très négatives (-1000).
   **Log-sum-exp 边界情况。**测试稳定 log-sum-exp 在极端输入下表现──

4. **Gradient checking a neural network layer.**Implémenter une seule couche linéaire `y = Wx + b`et vérifier la précision d'une matrice de poids 3x2.
   **梯度检查神经网络层。**☐ la mise en œuvre de la politique de sécurité

5. **Loss scaling experiment.**Simuler l'entraînement avec float16: mesurer quelle fraction des gradients devient zéro. Appliquer ensuite l'échelle de perte et mesurer à nouveau.
   **损失缩放实验。**模拟 float16 训练, mesure gradiente change pour le ratio de zéro, puis appliquer la perte réduite à la re mesure.

## Les termes clés

| Term / 术语 | What people say | What it actually means / 实际含义 |
|------|----------------|----------------------|
| IEEE 754 | "The float standard" | International standard defining binary floating point formats. / 定义二进制浮点格式的国际标准。 |
| Machine epsilon / 机器精度 | "The precision limit" | The smallest value e such that 1.0 + e != 1.0. For float32, ~1.19e-7. / 使 1.0 + e != 1.0 的最小值。float32 约 1.19e-7。 |
| Catastrophic cancellation / 灾难性抵消 | "Precision loss from subtraction" | Significant digits cancel when subtracting nearly equal numbers. / 相减近似相等数时有效数字抵消。 |
| Overflow / 溢出 | "Number too big" | A result exceeds the maximum representable value and becomes inf. / 结果超过最大可表示值变为 inf。 |
| Underflow / 下溢 | "Number too small" | A result is closer to zero than the smallest representable positive number. / 结果比最小可表示正数更接近零。 |
| Log-sum-exp trick / Log-sum-exp 技巧 | "Subtract the max first" | Computing log(sum(exp(x))) by factoring out exp(max(x)). / 通过提取 exp(max(x)) 计算 log(sum(exp(x)))。 |
| Stable softmax / 稳定 softmax | "Softmax that does not explode" | Subtracting max(logits) before exponentiating. / 指数化前减去最大 logit。 |
| Gradient checking / 梯度检查 | "Verify your backprop" | Comparing analytical vs numerical gradients to catch bugs. / 比较解析和数值梯度以捕获 bug。 |
| Mixed precision / 混合精度 | "Float16 forward, float32 backward" | Using lower-precision for speed, higher-precision for accuracy. / 低精度加速，高精度保准确。 |
| Loss scaling / 损失缩放 | "Prevent gradient underflow" | Multiplying loss by a large constant to keep gradients in float16 range. / 将损失乘以大常数使梯度保持在 float16 范围内。 |
| bfloat16 | "Brain floating point" | Google's 16-bit format with 8 exponent bits. Preferred for training. / Google 的 16 位格式，8 位指数。训练首选。 |
| Gradient clipping / 梯度裁剪 | "Cap the gradient norm" | Scaling the gradient vector so its norm does not exceed a threshold. / 缩放梯度向量使范数不超过阈值。 |
| NaN | "Not a Number" | Special float value from undefined operations. Propagates through all arithmetic. / 未定义操作的特殊浮点值。通过所有算术传播。 |
| Inf | "Infinity" | Special float value from overflow or division by zero. / 溢出或除零产生的特殊浮点值。 |
| Numerical gradient / 数值梯度 | "Brute force derivative" | Approximating a derivative by evaluating f(x+h) and f(x-h). / 通过求 f(x+h) 和 f(x-h) 近似导数。 |

## Encore une lecture

- [What Every Computer Scientist Should Know About Floating-Point Arithmetic (Goldberg 1991)](https://docs.oracle.com/cd/E19957-01/806-3568/ncg_goldberg.html)-- la référence définitive
  浮点算术 autorité de référence
- [Mixed Precision Training (Micikevicius et al., 2018)](https://arxiv.org/abs/1710.03740)-- le document NVIDIA sur l' évolutivité des pertes
  NVIDIA 损失缩放论文
- [AMP: Automatic Mixed Precision (PyTorch docs)](https://pytorch.org/docs/stable/amp.html)-- guide pratique
  PyTorch 混合精度实践指南
- [bfloat16 format (Google Cloud TPU docs)](https://cloud.google.com/tpu/docs/bfloat16)-- pourquoi Google a choisi ce format
  Google 选择 bfloat16 的原因
- [Kahan Summation (Wikipedia)](https://en.wikipedia.org/wiki/Kahan_summation_algorithm)-- algorithme pour réduire l'erreur d'arrondissement
  Réduire les erreurs de Kahan
