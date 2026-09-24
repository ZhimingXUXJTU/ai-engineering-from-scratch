# Calculo para el aprendizaje automático

> Los derivados te dicen hacia abajo, eso es todo lo que una red neuronal necesita aprender.

> El número de instrucciones te dice dónde está la dirección de la red nerviosa.

**Type:** Learn | **类型:** 学习
**Language:**¿ Qué pasa ?**语言:**Python
**Prerequisites:** Phase 1, Lessons 01-03 | **前置知识:** Phase 1, Lessons 01-03
**Time:** ~60 minutes | **时间:** ~60 分钟

## Objetivos de aprendizaje

- Computación de derivados numéricos y analíticos para las funciones ML comunes (x^2, sigmoide, entropía cruzada)
  计算常见 ML 函数(x^2、sigmoid、交叉) de los números de valores y de los números de datos
- Implementar la descenso de gradiente desde cero para minimizar una función de pérdida en 1D y 2D
  Desde el nivel de reducción de la realidad, en 1D y 2D la función de pérdida mínima
- Derivar el gradiente de un modelo de regresión lineal y entrenarlo mediante actualizaciones manuales de peso
  推导线性回归模型的梯度, y mediante el manual de actualización de peso realizar entrenamiento
- Explicar la matriz hessiana, las aproximaciones de la serie Taylor y su conexión con los métodos de optimización
   Explicar Hessian 矩阵、Taylor 级数近似 y su relación con el método de optimización

> **【中文解读】**
> Los números directivos te dicen "a qué dirección debe ir" y pueden hacer que el error sea pequeño. La red neuronal tiene millones de parámetros, cada parámetro es un "torno", los parámetros directivos te dicen en qué dirección debe ir.

> **【拓展：微积分与神经网络】**
> - **梯度下降**El algoritmo central del entrenamiento de la red neuronal se actualiza en la dirección contraria de la escala.
> - **SGD/Adam**El estudio de la evolución de la evolución de la evolución de la evolución de la evolución de la evolución de la evolución de la evolución de la evolución de la evolución de la evolución de la evolución de la evolución de la evolución de la evolución de la evolución de la evolución de la evolución de la evolución de la evolución de la evolución de la evolución de la evolución de la evolución de la evolución de la evolución de la evolución de la evolución de la evolución de la evolución de la evolución de la evolución de la evolución de la evolución de la evolución de la evolución de la evolución de la evolución de la evolución de la evolución de la evolución de la evolución de la evolución de la evolución de la evolución de la evolución de la evolución de la evolución de la evolución de la evolución de la evolución de la evolución de la evolución de la evolución de la evolución de la evolución de la evolución de la evolución de la evolución de la evolución de la evolución de la evolución de la evolución de la evolución de la evolución de la evolución de la evolución de la evolución de la evolución de la evolución de la evolución de la evolución de la evolución de la evolución de la evolución de la evolución de la evolución de la evolución de la evolución de la evolución de la evolución de la evolución de la evolución de la evolución de la evolución de la evolución de la evolución de la evolución de la evolución de la evolución de la evolución de la evolución de la evolución de la evolución de la evolución de la evolución de la evolución de la evolución de la evolución de la evolución de la evolución de la evolución de la evolución de la evolución de la evolución de la evolución de la evolución de la evolución de la evolución de la evolución de la evolución de la evolución de la evolución de la evolución de la evolución de la evolución de la evolución de la evolución de la evolución de la evolución de la evolución de la evolución de la evolución de la evolución de la evolución de la evolución de la evolución de la evolución de la evolución de la evolución de la evolución de la evolución de la evolución de la evolución de la evolución de la evolución de la evolución de la evolución de la evolución de la evolución de la evolución de la evolución de la evolución de la evolución de la evolución de la evolución de la evolución de la evolución de la evolución de la evolución de la evolución de la evolución de la evolución de la evolución de la evolución de la evolución de la evolución de la humanidad.
> - **学习率**梯度下降的步长──太大则跳过最小值,太小则收太慢──

## El problema es la introducción del problema

> **【中文解读】**La formación consiste en encontrar cada giro que debe ir hacia dónde. La formación consiste en encontrar cada giro que debe ir hacia dónde.

## El concepto central.

> **【拓展：偏导数就是"只动一个旋钮看效果"]**La función de pérdida de la red nerviosa L(w1, w2, ..., wn) tiene millones de variaciones. La función de pérdida de la red nerviosa ∂L/∂w_i                                                                                                                                                                                                                                                                                                                                                                                                                                                                                   

### ¿Qué es una derivada?

Una derivada mide la velocidad de cambio. para una función y = f(x), la derivada f'(x) le dice: si empujas x por una cantidad pequeña, ¿cuánto cambia y?

> 导数量衡变化率──对于函数 y = f(x),导数 f'(x) 告诉你: si x 微小变化, y 变化多少?

Geométricamente, la derivada es la pendiente de la línea tangente en un punto.

> 几何上, el número de direcciones es la inclinación de un punto de la línea.

**f(x) = x^2:**

| x | f(x) | f'(x) (slope) |
|---|------|---------------|
| 0 | 0    | 0 (flat, at the bottom) |
| 1 | 1    | 2 |
| 2 | 4    | 4 (tangent line slope at this point) |
| 3 | 9    | 6 |

Cuando x es igual a 2, la pendiente es 4. Si se mueve x un poco a la derecha, y aumenta aproximadamente 4 veces esa cantidad.

> En x=2 处, la inclination es 4 ⋅ si vas a x hacia la derecha mover un punto, y aproximadamente aumentar la cantidad de movimiento 4 ⋅ veces ⋅ en x=0 处, la inclination es 0 ⋅ si estás en el "bas de la taza" ⋅

La definición formal:

```
f'(x) = lim   f(x + h) - f(x)
        h->0  -----------------
                     h
```

En el código, saltamos el límite y sólo usamos una h muy pequeña. Esa es la derivada numérica.

> En código, saltar por encima de la frontera, directamente con un pequeño h para acercarse.

### Derivados parciales: una variable a la vez

Las funciones reales tienen muchas entradas. Una pérdida de red neuronal depende de miles de pesas. Una derivada parcial mantiene constantes todas las variables excepto una, luego toma la derivada con respecto a esa.

> La función de pérdida de red neuronal depende de miles de pesos. La función de pérdida de red neuronal depende de miles de pesos. La función de pérdida de red neuronal depende de miles de pesos.

```
f(x, y) = x^2 + 3xy + y^2

df/dx = 2x + 3y     (treat y as a constant)
df/dy = 3x + 2y     (treat x as a constant)
```

Cada derivada parcial responde: si empujo sólo este peso, ¿cómo cambia la pérdida?

> Cada número de parámetros responde: si sólo dialé este peso, ¿cuánto cambiaría la pérdida?

### El gradiente: vector de todas las derivadas parciales

El gradiente reúne todas las derivadas parciales en un vector. Para una función f ((x, y, z), el gradiente es:

> 梯度把所有偏导数集合 into a向量──对函数 f ((x, y, z),梯度为:

```
grad f = [ df/dx, df/dy, df/dz ]
```

El gradiente apunta en la dirección de la ascensión más empinada.

> 梯度指向最上升方向──要最小化函数,就沿相反方向走──

**Contour plot of f(x,y) = x^2 + y^2:**

La función forma una forma de cuenco con círculos concéntricos como líneas de contorno.

> La función forma una forma de cuenco, igual que la línea alta es el círculo central. El valor mínimo es (0, 0)

| Point | grad f | -grad f (descent direction) |
|-------|--------|----------------------------|
| (1, 1) | [2, 2] (points uphill, away from minimum) | [-2, -2] (points downhill, toward minimum) |
| (0, 0) | [0, 0] (flat, at the minimum) | [0, 0] |

> 梯度方向指向最上坡,负梯度方向指向最下坡 (en inglés: 梯度方向指向最上坡,负梯度方向指向最下坡, en inglés: 梯度方向指向最下坡, 梯度方向指向最下坡, 梯度方向指向最下坡, 梯度方向指向最小值, 梯度方向指向最低值, 梯度方向指向最低值, 梯度方向指向最低值, 梯度方向指向最低值, 梯度在最小值处梯度为零点, 梯度为零点, 梯度在最小值处梯度为零点, 梯度在最小值为零点, 梯度方向指向最低值, 梯度方向指向最低值, 梯度方向指向最低值, 梯度方向指向最低值, 梯度向最低值, 梯度向最低值, 梯度向最低值, 梯度向最低值, 梯度向最低值, 梯度向最低值, 梯度向最低值, 梯度为零点, 梯度向下坡, 梯度向下坡向最低值, 梯度向下坡向最低值, 梯梯梯度为零点, 梯梯度为零点, 梯度, 梯梯梯梯梯梯梯度向向向向向向向向向向向向向下下下下下下下下下下下下下下下下下下下下下下下下下下下下下下下下下下下下下下下下下下下下下下下下下下下下下下下下下下下下下下下下下下下下下下下下下下下下下下下下下下下下下下下下下下下下下下下下下下下下下下下下下下下下下下下下下下下下下下下下下下下下下下下下下下下下下下下下下下下下下下下下下下下下下下下下下下下下下下下下下下下下下下下下下下下下下下下下下

Esto es un descenso de gradiente en una imagen.

> Éste es el gráfico de la escala baja.

### La conexión con la optimización

Entrenando una red neuronal es optimización. Tienes una función de pérdida L ((w1, w2, ..., wn) que mide lo mal que está el modelo.

> 训练神经网络就是优化――损失函数 L(w1, w2, ..., wn) 衡量模型有多"错", tienes que minimizarlo―

```
Gradient descent update rule:

  w_new = w_old - learning_rate * dL/dw

For every weight:
  1. Compute the partial derivative of loss with respect to that weight
  2. Subtract a small multiple of it from the weight
  3. Repeat
```

> 梯度下降规则: 新权重 = 旧权重 - 学习率 × 梯度──重复:1) calcular el número de parámetros de cada peso;2) deducir de peso una pequeña multiplicidad;3) 代数百万次──

La velocidad de aprendizaje controla el tamaño del paso.

> El índice de aprendizaje controló el paso.

**Loss landscape (1D slice):**

La función de pérdida L ((w) forma una curva con picos y valles a medida que el peso w varía.

> 损失函数 L(w) 随权重 w 变化形成带峰和谷的曲线──

| Feature | Description |
|---------|-------------|
| Global minimum | The lowest point on the entire curve -- the best solution |
| Local minimum | A valley that is lower than its neighbors but not the lowest overall |
| Slope | Gradient descent follows the slope downhill from any starting point |

> El mínimo local es el mínimo del valle del valle del barrio, pero no el mínimo local; la gradiencia baja desde cualquier punto de salida a lo largo de la ladera.

La descenso gradual sigue la pendiente hacia abajo. Puede quedar atrapado en mínimos locales, pero en espacios de alta dimensión (millones de pesos) esto rara vez es un problema práctico.

> 梯度下降沿坡下行──可能陷入局部最小值, pero en高维空间中 (en el espacio alto, en el peso de millones de grados), esto rara vez se convierte en un problema real──

### Derivados numéricos frente a derivados analíticos

Hay dos formas de calcular una derivada.

> 计算导数 Hay dos métodos:

Para f  x = x^2, la derivada es f  x = 2x. Exactamente. Rápido.

> 解析法:手动应用微积分规则──如 f(x) = x^2 的导数是 f'(x) = 2x──精确且快速──

Numérico: aproximar usando la definición. Calcule f ((x+h) y f ((x-h) para una pequeña h, luego use la diferencia.

> Número de valores: con definición de aproximación.

```
Numerical (central difference):

f'(x) ~= f(x + h) - f(x - h)
          -----------------------
                  2h

h = 0.0001 works well in practice
```

Las derivadas numéricas son más lentas pero funcionan para cualquier función. Las derivadas analíticas son rápidas pero requieren que se derive la fórmula.

> La dirección de valores es más lenta pero se aplica a cualquier función. La dirección de resolución es rápida pero necesita una dirección manual.

### Derivados a mano para funciones simples

Estas son las derivadas que verás una y otra vez en ML.

> Estos son los números de guías que verás repetidamente en ML.

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

Para f ((x) = x^2:

```
f(x) = x^2    f'(x) = 2x

  x    f(x)   f'(x)   meaning
  -2    4      -4      slope tilts left (decreasing)
  -1    1      -2      slope tilts left (decreasing)
   0    0       0      flat (minimum!)
   1    1       2      slope tilts right (increasing)
   2    4       4      slope tilts right (increasing)
```

> En x<0 时导数为负(函数递减), x=0 时导数为零(alcanzar el valor mínimo), x>0 时导数为正(函数递增) ・・・

Para f(w) = wx + b con x=3, b=1:

```
f(w) = 3w + 1    f'(w) = 3

The derivative with respect to w is just x.
If x is big, a small change in w causes a big change in output.
```

> Para la w  orientación el resultado es x en sí mismo. Si x  es grande, las pequeñas variaciones de w conducen a cambios enormes en la salida.

### La regla de la cadena

Cuando las funciones se componen, la regla de la cadena le dice cómo diferenciar.

> Cuando la función compleja, la ley de cadena le dice cómo buscar dirección.

```
If y = f(g(x)), then dy/dx = f'(g(x)) * g'(x)

Example: y = (3x + 1)^2
  outer: f(u) = u^2       f'(u) = 2u
  inner: g(x) = 3x + 1    g'(x) = 3
  dy/dx = 2(3x + 1) * 3 = 6(3x + 1)
```

Las redes neuronales son cadenas de funciones: entrada -> lineal -> activación -> lineal -> activación -> pérdida. La retropropagación es la regla de cadena aplicada repetidamente desde la salida a la entrada. Es el algoritmo entero.

> La red de los nervios es una cadena de funciones: entrada -> 线性 -> 激活 -> 线性 -> 激活 -> 损失──反向传播就是从输出到输入反复应用链式法则──这是整个算法──

### La Matriz Hesiana

El gradiente le dice la pendiente, el hessiano le dice la curvatura.

> La gradiente te dice la inclinada, la Hessian la matriz te dice la inclinada.

El hessiano es la matriz de derivadas parciales de segundo orden. Para una función f ((x1, x2, ..., xn), la entrada (i, j) del hessiano es:

> Hessian es la segunda etapa de la dirección de la cantidad de componentes de la matriz.

```
H[i][j] = d^2f / (dx_i * dx_j)
```

Para una función de 2 variables f ((x, y):

```
H = | d^2f/dx^2    d^2f/dxdy |
    | d^2f/dydx    d^2f/dy^2 |
```

**What the Hessian tells you at a critical point (where gradient = 0):**

> Hessian en el punto de referencia (梯度为 0 处) te dice: ¿es el valor mínimo del punto de referencia o el valor máximo del punto de referencia?

| Hessian property | Meaning | Example surface |
|-----------------|---------|-----------------|
| Positive definite (all eigenvalues > 0) | Local minimum | Bowl pointing up |
| Negative definite (all eigenvalues < 0) | Local maximum | Bowl pointing down |
| Indefinite (mixed eigenvalues) | Saddle point | Horse saddle shape |

> 正定(所有特征值 > 0) = 局部最小值;负定(所有特征值 < 0) = 局部最大值;不定(特征值有正有负) = 点。

**Example:**f(x, y) = x^2 - y^2 (función de silla)

```
df/dx = 2x       df/dy = -2y
d^2f/dx^2 = 2    d^2f/dy^2 = -2    d^2f/dxdy = 0

H = | 2   0 |
    | 0  -2 |

Eigenvalues: 2 and -2 (one positive, one negative)
--> Saddle point at (0, 0)
```

Compare con f ((x, y) = x^2 + y^2 (un tazón):

```
H = | 2  0 |
    | 0  2 |

Eigenvalues: 2 and 2 (both positive)
--> Local minimum at (0, 0)
```

**Why the Hessian matters in ML:**

> Hessian en ML ¿qué significa: Newton usó Hessian 修梯度方向, hacer que la dirección se moviera pequeños pasos 平坦方向走大步, de modo que la gradiencia se descendiera más rápido.

El método de Newton utiliza el Hessian para tomar mejores pasos de optimización que el descenso de gradiente.

```
Newton's update:    w_new = w_old - H^(-1) * gradient
Gradient descent:   w_new = w_old - lr * gradient
```

> Newton 更新:w_new = w_old - H−1 × gradiente―la utiliza con la incidencia de la incrustación de la incrustación de la incrustación―

El método de Newton converge más rápido porque el Hessian "rescales" el gradiente - direcciones empinadas consiguen pasos más pequeños, direcciones planas consiguen pasos más grandes.

> Newton se acelera más rápido, porque el hesiano "reencontrajo" la escala en dirección a un pequeño paso, en dirección plana a un gran paso.

El problema: para una red neuronal con N parámetros, el Hessian es N x N. Un modelo con 1 millón de parámetros necesitaría una matriz de 1 billón de entradas.

> El problema está en: N 个参数的网络, Hessian es N×N── millones de modelos de参数 necesitan millones de dimensiones de la matriz es por eso que utilizamos los métodos similares (como Adam、L-BFGS)──

| Method | What it uses | Cost | Convergence |
|--------|-------------|------|-------------|
| Gradient descent | First derivatives only | O(N) per step | Slow (linear) |
| Newton's method | Full Hessian | O(N^3) per step | Fast (quadratic) |
| L-BFGS | Approximate Hessian from gradient history | O(N) per step | Medium (superlinear) |
| Adam | Per-parameter adaptive rates (diagonal Hessian approx) | O(N) per step | Medium |
| Natural gradient | Fisher information matrix (statistical Hessian) | O(N^2) per step | Fast |

> Diferente de optimizador: gradiente de baja con un solo número de parámetros (O (N),慢); Newton con un Hessiano completo (O (N3), rápido pero demasiado caro); L-BFGS con gradiente histórico similar a Hessiano; Adam con gradiente Hessiano similar a cada uno de los parámetros; natural gradiente con Fisher 信息矩阵。

En la práctica, Adam es el optimizador predeterminado para el aprendizaje profundo. Aproxima información de segundo orden a bajo costo mediante el seguimiento de la media corriente y la variación de gradientes por parámetro.

> En realidad, Adam es un optimizador predeterminado de aprendizaje profundo.                                                                                                                                                                                                                                                      

### Aproximación de la serie Taylor

Cualquier función lisa puede ser aproximada localmente por un polinomio:

> Cualquier función plana puede ser localmente utilizada en múltiples aproximaciones.

```
f(x + h) = f(x) + f'(x)*h + (1/2)*f''(x)*h^2 + (1/6)*f'''(x)*h^3 + ...
```

Cuanto más términos incluya, mejor la aproximación, pero sólo cerca del punto x.

> 包含的项越多,近似越好但只在x 附近有效──一阶 Taylor = 梯度下降,二阶 Taylor = Newton法──

**Why Taylor series matter for ML:**

- **First-order Taylor = gradient descent.**Cuando se usa f(x + h) ~ f(x) + f'(x) *h, se está haciendo una aproximación lineal.

- **Second-order Taylor = Newton's method.**Usando f(x + h) ~ f(x) + f'(x) *h + (1/2) *f'(x) *h^2, obtienes un modelo cuadrático. Minimizándolo se da h = -f'(x) / f'(x) --el paso de Newton.

- **Loss function design.**El MSE y la entropía cruzada son suaves, lo que significa que sus expansiones Taylor están bien conducidas. Esto no es un accidente.

> Número de Taylor en ML en el significado: primera etapa Taylor = 线性近似 = 梯度下降; segunda etapa Taylor = 二次近似 = Newton法; MSE 和交叉的平滑性不是巧合平滑损失让优化可预测──

```
Approximation order    What it captures    Optimization method
-------------------    -----------------   -------------------
0th order (constant)   Just the value      Random search
1st order (linear)     Slope               Gradient descent
2nd order (quadratic)  Curvature           Newton's method
Higher orders          Finer structure     Rarely used in ML
```

> Aproximadamente, el número de etapas se reduce a la de la de la de la de la de la de la de la de la de la de la de la de la de la de la de la de la de la de la de la de la de la de la de la de la de la de la de la de la de la de la de la de la de la de la de la de la de la de la de la de la de la de la de la de la de la de la de la de la de la de la de la de la de la de la de la de la de la de la de la de la de la de la de la de la de la de la de la de la de la de la de la de la de la de la de la de la de la de la de la de la de la de la de la de la de la de la de la de la de la de la de la de la de la de la de la de la de la de la de la de la de la de la de la de la de la de la de la de la de la de la de la de la de la de la de la de la de la de la de la de la de la de la de la de la de la de la de la de la de la de la de la de la de la de la de la de la de la de la de la de la de la de la de la de la de la de la de la de la de la de la de la de la de la de la de la de la de la de la de la de la de la de la de la de la de la de la de la de la de la de la de la de la de la de la de la de la de la de la de la de la de la de la de la de la de la de la de la de la de la de la de la de la de la de la de la de la de la de la de la de la de la de la de la de la de la de la de la de la de la de la de la de la de la de la de la de la de la de la de la de la de la de la de la de la de la de la de la de la de la de la de la de la de la de la de la de la de la de la de la de la de la de la de la de la de la de la de la de la de

La idea clave: toda optimización basada en gradientes es realmente acerca de aproximar la función de pérdida localmente y avanzar al mínimo de esa aproximación.

> 关键洞见: todas las optimizaciones basadas en la gradiencia se realizan en la función de pérdida aproximada local, y luego se llegan a este punto de menor valor aproximado.

### Integral en ML

Las derivadas le dicen las tasas de cambio. Los integrales calculan acumulaciones - área bajo una curva.

> 导数告诉你变化率,积分计算累积(曲线下面积) ⋅

En ML, rara vez se computa integrals a mano, pero el concepto está en todas partes:

> En el ML, hay pocos números de cuentas, pero el concepto de cuentas está presente:

**Probability.**Para una variable aleatoria continua con densidad p ((x):
```
P(a < X < b) = integral from a to b of p(x) dx
```
El área bajo la curva de densidad de probabilidad entre a y b es la probabilidad de aterrizaje en ese rango.

> **概率**: a la continuidad de las variaciones, la función de densidad p(x) en [a, b] 区间积分就是落在此区间的概率──

**Expected value.**El resultado medio ponderado por probabilidad:
```
E[f(X)] = integral of f(x) * p(x) dx
```
La pérdida esperada sobre una distribución de datos es una parte integral.

> **期望**:加权平均―― la pérdida de esperanzas en la distribución de datos es una积分, entrenamiento minimiza su experiencia casi―

**KL divergence.**Medirá la diferencia entre dos distribuciones:
```
KL(p || q) = integral of p(x) * log(p(x) / q(x)) dx
```
Se utiliza en VAEs, destilación del conocimiento y inferencia bayesiana.

> **KL 散度**La diferencia entre las dos distribuciones se mide en la VAE, en el conocimiento y en la teoría de la base.

**Normalization constants.**En la inferencia bayesiana:
```
p(w | data) = p(data | w) * p(w) / integral of p(data | w) * p(w) dw
```
El denominador es una integral sobre todos los posibles valores de parámetros. a menudo es intratable, por lo que usamos aproximaciones como MCMC y inferencia variativa.

> **归一化常数**En la hipótesis de Bayes, la fracción es el cálculo de todos los valores de los parámetros posibles, por lo general no se puede resolver.

| Integral concept | Where it appears in ML |
|-----------------|----------------------|
| Area under curve | Probability from density functions |
| Expected value | Loss functions, risk minimization |
| KL divergence | VAEs, policy optimization, distillation |
| Normalization | Bayesian posteriors, softmax denominator |
| Marginal likelihood | Model comparison, evidence lower bound (ELBO) |

> 积分概念在 ML 中体现:曲线下面积(density function求概率) 期望(损失函数) 、KL 散度(VAE/蒸) 归结(贝叶斯后验/softmax 分母) 边际似然(模型比较/ELBO) ⋅

### Regla de cadena multivariable en un gráfico de cálculo

La regla de la cadena no se aplica solo a las funciones escalares en una línea. En una red neuronal, las variables se expandieron y se fusionaron.

> La ley de la cadena de múltiples variaciones no solo se aplica a las funciones de la cadena de valores de la línea. En las redes neuronales, las variaciones se dividen y se unifican.

```mermaid
graph LR
    x["x (input)"] -->|"*w"| z1["z1 = w*x"]
    z1 -->|"+b"| z2["z2 = w*x + b"]
    z2 -->|"sigmoid"| a["a = sigmoid(z2)"]
    a -->|"loss fn"| L["L = -(y*log(a) + (1-y)*log(1-a))"]
```

El paso hacia atrás calcula los gradientes de derecha a izquierda:

```mermaid
graph RL
    dL["dL/dL = 1"] -->|"dL/da"| da["dL/da = -y/a + (1-y)/(1-a)"]
    da -->|"da/dz2 = a(1-a)"| dz2["dL/dz2 = dL/da * a(1-a)"]
    dz2 -->|"dz2/dw = x"| dw["dL/dw = dL/dz2 * x"]
    dz2 -->|"dz2/db = 1"| db["dL/db = dL/dz2 * 1"]
```

Cada flecha se multiplica por la derivada local. El gradiente de cualquier parámetro es el producto de todas las derivadas locales a lo largo del camino desde la pérdida hasta ese parámetro. Cuando los caminos se ramifican y se fusionan, se suman las contribuciones (regla de cadena multivariada).

> Cada arco se multiplica por la dirección local. La escala de cualquier parámetro es la multiplicidad de todas las direcciones locales en el camino del parámetro desde la pérdida hasta el paso del parámetro. Cuando el camino se divide y se combina, se debe hacer una contribución a la demanda y a la aplicación de la ley de la cadena múltiple.

Esto es todo la retropropagación es: la regla de cadena aplicada sistemáticamente a través de un gráfico de cálculo, de salida a entradas.

> Todo lo contrario de la transmisión es: en el cálculo, desde la salida hasta la entrada se aplica la ley de la cadena sistematizada.

### La matriz jacobiana

Cuando una función mapea un vector a un vector (como una capa de red neuronal), su derivada es una matriz. El Jacobian contiene cada derivada parcial de cada salida con respecto a cada entrada.

> Cuando la función trae la velocidad de un eje hacia una velocidad, su dirección es una matriz de Jacobian que contiene cada salida a cada entrada.

Para f: R^n -> R^m, el Jacobiano J es una matriz m x n:

> 对于 f: R^n → R^m,Jacobian J es una m × n 矩阵:

| | x1 | x2 | ... | xn |
|---|---|---|---|---|
| f1 | df1/dx1 | df1/dx2 | ... | df1/dxn |
| f2 | df2/dx1 | df2/dx2 | ... | df2/dxn |
| ... | ... | ... | ... | ... |
| fm | dfm/dx1 | dfm/dx2 | ... | dfm/dxn |

No se calcularán Jacobians a mano para redes neuronales. PyTorch lo maneja. Pero saber que existe le ayuda a entender formas en la retropropagación: si una capa mapea R^n a R^m, su Jacobian es m x n. El gradiente fluye hacia atrás a través de la transposición de esta matriz.

> Usted no puede calcular la forma de la red neuronal JacobianPyTorch automáticamente. Pero saber que existe puede ayudarle a entender la forma en la transmisión inversa: si la capa de R^n n n n n r m, su Jacobian es m×n, gradiente a través de su transposición inversa n r n r r r r r r r r r r r r r r r r r r r r r r r r r rrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrr

### Por qué esto es importante para las redes neuronales

Cada peso en una red neuronal obtiene un gradiente. El gradiente le dice cómo ajustar ese peso para reducir la pérdida.

> Cada peso en la red nerviosa tiene una escala, que te dice cómo ajustar ese peso para reducir la pérdida.

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

Cada actualización de peso:
- `W1 = W1 - lr * dL/dW1`
- `W2 = W2 - lr * dL/dW2`

> Cada uno de los cambios de peso: W = W - lr × dL/dW──.

El pase hacia adelante calcula la predicción y la pérdida. El pase hacia atrás calcula el gradiente de la pérdida con respecto a cada peso. Luego cada peso toma un pequeño paso hacia abajo. Repita por millones de pasos. Eso es aprendizaje profundo.

> Antes de la transmisión calculará la previsión y pérdida, después de la transmisión calculará la escala de cada peso, y luego cada peso a lo largo de la escala de peso se dirigirá hacia un pequeño paso.

## Construye y realiza.
```figure
derivative-tangent
```

## Construye el mismo

### Paso 1: Derivada numérica desde cero

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

> Utiliza el método de diferenciación central para lograr el número de valores de la dirección.

La derivada numérica coincide con la analítica de uno a muchos decimales.

> La dirección de valores y la dirección de resolución se mantienen en la misma posición en varios puntos después de un pequeño número de puntos, lo que confirma la exactitud de la fórmula de diferencia central.

### Paso 2: Derivados y gradientes parciales

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

> Número de valores: para cada dimensión independiente de los centros de diferencia en la dirección, la composición de la escala de la escala de la escala.

### Paso 3: Descenso gradual para encontrar el mínimo de f ((x) = x^2

```python
x = 5.0
lr = 0.1
for step in range(20):
    grad = 2 * x
    x = x - lr * grad
    print(f"step {step:2d}  x={x:8.4f}  f(x)={x**2:10.6f}")
```

Comenzando en x=5, cada paso se acerca a x=0 (el mínimo).

> Desde x=5 saliendo, cada paso está más cerca de x=0 ((minimo valor) ⋅ tasa de aprendizaje 0.1 让 x 逐步缩小到接近0──

### Paso 4: Descenso gradual en una función 2D

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

> 2D 梯度下降: desde (4, 3) 出发, cada paso de actualización punto -= lr × grad, cada paso de recepción hasta (0, 0) ⋅

### Paso 5: Comparación de derivados numéricos y analíticos

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

> En comparación con 5 funciones comunes en x=2 en la dirección de valores y la dirección de resolución: x2、x3、sin(x)、e^x、1/x。, los errores suelen estar en la escala 1e-10 ̊, la exactitud del método de verificación de valores。

### Paso 6: Calcular el hessiano numéricamente

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

> Hesiano 矩阵:fxx、fyy es el segundo escalón de la orientación, fxy es la orientación de la combinación.

El Hessian de la función de sillón tiene valores propios 2 y -2 (signos mixtos, confirmando un punto de sillón).

> Punto de función de Hessian características son 2 和 -2(一正一负, identificando点);

### Paso 7: Aproximación de Taylor en acción

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

> Taylor 近似实战: 在 x0=0 处用一阶和二阶 Taylor 近似 sin(h) ・h=0.1 时近似精度极高,h=2 时偏差很大──这是梯度下降需要小学习率的数学根源──

Cerca de x0=0, sin(x) ~ x (de primer orden Taylor). La aproximación es excelente para pequeñas h pero se descompone para grandes h. Esta es la razón por la que el descenso de gradiente funciona mejor con pequeñas tasas de aprendizaje - cada paso asume que la aproximación lineal es precisa.

> En el caso de los estudiantes de secundaria, el nivel de aprendizaje es de 10 a 10 años.

### Paso 8: Por qué esto es importante para una red neuronal

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

> 完整的线性回归训练循环: desde随机权重 w、b 出发, calcular cada muestra de pronóstico、误差、梯度 dw 和 db, luego actualizar los parámetros。重复 200 轮后, el modelo se aprende automáticamente hasta y = 2x + 1── este es el prototipo de todos los ciclos de entrenamiento de aprendizaje profundo。

Cada ciclo de entrenamiento basado en gradientes sigue este patrón: predicción, pérdida de cálculo, gradientes de cálculo, pesos de actualización.

> Cada ciclo de entrenamiento basado en la escala sigue este modelo: predicción → 计算损失 → 计算梯度 → 更新权重―― esta clase logra el entrenamiento de regreso lineal y=2x+1―.

## Usalo con el marco de ejecución

Con NumPy, las mismas operaciones son más rápidas y más concisas:

> Usar NumPy 重写: similar运算更简洁更快――矢量化 evitó el ciclo de Python, hacer que la escala de cálculo sea más alta.

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

> NumPy hacia la dimensión versión:`np.mean`替代Python 循环求平均,更快更简洁──矢量化 es la técnica de optimización central del cálculo numérico──

PyTorch automatiza el cálculo de gradientes, pero el bucle de actualización es idéntico.

> Usted acaba de lograr la disminución de la escala desde cero. PyTorch automatizó la calculación de la escala, pero el ciclo de actualización es completamente el mismo.`w -= lr * dw`Esta línea nunca cambiará.

## Los ejercicios.

1. Implementación `numerical_second_derivative(f, x)`el uso de`numerical_derivative`Se llama dos veces. Verifique que la segunda derivada de x^3 en x=2 es 12.
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                `numerical_second_derivative(f, x)`,调用两次 `numerical_derivative` Prueba x^3 en x=2 处的二阶导数为12──
2. Utilice la descenda de gradiente para encontrar el mínimo de f ((x, y) = (x - 3) ^ 2 + (y + 1) ^ 2. Comience desde (0, 0). La respuesta debe converger a (3, -1).
   Us梯度下降找 f(x, y) = (x - 3)2 + (y + 1)2 de la mínima valor, desde (0, 0) 出发,应收到 (3, -1)。
3. Añadir impulso al bucle de descenso de gradiente: mantener un vector de velocidad que se acumula en los gradientes anteriores.
   给梯度下降循环加动量: mantenimiento de una acumulación de velocidad de la escala pasada △ comparar con un inactividad en f(x) = x4 - 3x2 △

## Términos clave .

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

> 术语速查:Derivado (导数/斜率) ‧Derivado parcial (偏导数, fijación de otras variaciones) ‧Gradiente (梯度), todos los derivados que forman el向量, orientados hacia el más alto y hacia el más alto) ‧Descenso (梯度下降,沿梯度负方向更新) ‧Tasa de aprendizaje (学习率,步长) ‧Regla de cadena (链式法则,反向传播的数学基础) ‧Code (导数,固定其他变量) ‧Derivado numérico (导数, all-out) ‧Backpropagation (反向传播,层次链式) ‧Hessian二阶段偏导矩阵,描述曲值,正法=最小率) ‧Taylor series ‧(((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((

## Más Leer más Leer más

- [3Blue1Brown: Essence of Calculus](https://www.3blue1brown.com/topics/calculus)- Intuición visual para derivados, integrales y la regla de la cadena
- [Stanford CS231n: Backpropagation](https://cs231n.github.io/optimization-2/)- cómo fluyen los gradientes a través de las capas de la red neuronal
