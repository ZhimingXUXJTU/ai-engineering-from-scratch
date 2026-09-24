# Optimización convexa 凸优化

> Los problemas convexos tienen un valle, las redes neuronales tienen millones, saber la diferencia importa.
> 凸问题只有一个谷底――神经网络有数百万――理解差异至关重要―― es importante que el problema de la conexión sea un problema de la conexión.

**Type:** Build | **类型:** 动手
**Language:**¿ Qué pasa ?**语言:**Python
**Prerequisites:** Phase 1, Lessons 04 (Calculus for ML), 08 (Optimization) | **前置知识:** Phase 1, 第 04 课（微积分）、第 08 课（优化）
**Time:** ~90 minutes | **时间:** ~90 分钟

## Objetivos de aprendizaje

- Prueba si una función es convexa utilizando la definición, la segunda derivada y los criterios de Hessian
  Utiliza definición、二阶导数和 Hessian 判据测试函数 ¿Es que la función de la prueba es un segundo
- Implemente el método de Newton y compare su convergencia cuadrática con el descenso de gradiente
  实现牛顿法 (Método de Newton)并比较其二次收与梯度下降
- Resolver problemas de optimización restringidos utilizando multiplicadores de Lagrange e interpretar las condiciones de KKT
  Utilizaciones de la aplicación de la aplicación de la aplicación de la aplicación de la aplicación de la aplicación de la aplicación de la aplicación de la aplicación de la aplicación de la aplicación de la aplicación de la aplicación de la aplicación de la aplicación de la aplicación de la aplicación de la aplicación de la aplicación de la aplicación de la aplicación de la aplicación de la aplicación de la aplicación de la aplicación de la aplicación de la aplicación de la aplicación de la aplicación de la aplicación de la aplicación de la aplicación de la aplicación de la aplicación de la aplicación de la aplicación de la aplicación de la aplicación de la aplicación de la aplicación de la aplicación de la aplicación de la aplicación de la aplicación de la aplicación de la aplicación de la aplicación de la aplicación de la aplicación de la aplicación de la aplicación de la aplicación de la aplicación de la aplicación de la aplicación de la aplicación de la aplicación de la aplicación de la aplicación de la aplicación de la aplicación de la aplicación de la aplicación de la ley
- Explica por qué los paisajes de pérdida de redes neuronales no son convexos pero SGD todavía encuentra buenas soluciones
  Explica por qué la pérdida de la red neuronal no es tan grave, pero la SGD todavía puede encontrar una buena solución.


> **【中文解读】**
> 凸函数 sólo tiene un valle (→ 凸函数) 凸的, 凸的, 凸的, 凸的, 凸的, 凸的, 凸的, 凸的, 凸的, 凸的, 凸的, 凸的, 凸的, 凸的, 凸的, 凸的, 凸的, 凸的, 凸的, 凸的, 凸的, 凸的, 凸的, 凸的, 凸的, 凸的, 凸的, 凸的, 凸的, 凸的, 凸的, 凸的, 凸的, 凸的, 凸的, 凸的, 凸的, 凸的, 凸的, 凸的, 凸的, 凸的, 凸的, 凸的, 凸的, 凸的, 凸的, 凸的, 凸的, 凸的, 凸的, 凸的, 凸的, 凸的, 凸的, 凸的, 凸的, 凸的, 凸的, 凸的, 凸的, 凸的, 凸的, 凸的, 凸的, 凸的, 凸的, 凸的, 凸的, 凸的, 凸的, 凸的, 凸的, 凸的, 凸的, 凸的, 凸的, 凸的, 凸的, 凸的, 凸的, 凸的, 凸的, 凸, 凸的, 凸, 凸, 凸的, 凸, 凸, 凸, 凸的, 凸, 凸, 凸, 凸, 凸, 凸, 凸, 凸, 凸, 凸, 凸, 凸, 凸, 凸, 凸, 凸, 凸, 凸, 凸, 的, 凸, 凸, 凸, 凸, 凸, 且 且 且 且 且 且 且 且 且 且 且 且 且 且 且 且 且 且 且 且 且 且 且 且 且 且 且 且 且

## El problema es la introducción del problema

La lección 08 te enseñó la descenda de gradiente, el impulso y Adam. Esos optimizadores caminan por la ladera en cualquier superficie. Pero no tienen garantías. La descenda de gradiente en un paisaje no convexo puede aterrizar en un mínimo local malo, quedarse atascado en un punto de silla o oscilar para siempre. Lo usaste de todos modos porque las redes neuronales no son convexas y no hay alternativa.

> En la primera parte del capítulo, el profesor de la Universidad de Chicago, en el que se trata de la educación de la educación en la educación, el profesor de la Universidad de Chicago, el profesor de la Universidad de Chicago, el profesor de la Universidad de Chicago, el profesor de la Universidad de Chicago, el profesor de la Universidad de Chicago, el profesor de la Universidad de Chicago, el profesor de la Universidad de Chicago, y el profesor de la Universidad de Chicago, el profesor de la Universidad de Chicago, el profesor de la Universidad de Chicago, el profesor de la Universidad de Chicago, el profesor de la Universidad de Chicago, el profesor de la Universidad de Chicago, el profesor de la Universidad de Chicago, el profesor de la Universidad de Chicago, el profesor de la Universidad de Chicago, el profesor de la Universidad de Chicago, el profesor de la Universidad de Chicago, el profesor de la Universidad de Chicago, el profesor de la Universidad de Chicago, el profesor de la Universidad de Chicago, el profesor de la Universidad de Chicago, el profesor de la Universidad de Chicago, el profesor de la Universidad de Chicago, el profesor de la Universidad de Chicago, el profesor de la Universidad de Chicago, se encuentra en una universidad.

Pero muchos problemas en el aprendizaje automático son convexos. Regresión lineal, regresión logística, SVMs, LASSO, regresión de cresta. Para estos, existe algo más fuerte: optimización con garantías matemáticas. Un problema convexo tiene exactamente un valle. Cualquier algoritmo que camine descendente alcanzará el mínimo global. No se necesita reinicio. No hay horarios de tasa de aprendizaje. No hay oración.

> Pero muchos problemas en el aprendizaje automático son de la conmoción. La conmoción de la conmoción de la conmoción de la conmoción de la conmoción de la conmoción de la conmoción de la conmoción de la conmoción de la conmoción de la conmoción.

Comprender la convexidad hace tres cosas. Primero, le dice cuándo su problema es fácil (convexa) versus duro (no convexa). Segundo, le da herramientas más rápidas como el método de Newton para problemas convexos. Tercero, explica conceptos que aparecen en todo ML: regularización como una restricción, dualidad en SVMs, y por qué el aprendizaje profundo funciona a pesar de violar cada propiedad agradable que le da la convexidad.

> En primer lugar, le dice a usted el problema de cuándo es fácil (conforme) o difícil (sin conforme). En segundo lugar, proporciona herramientas más rápidas para el problema de conformación, como la ley de Newton. En tercer lugar, explica el concepto de ML: la normalización como un vínculo, la paridad en la SVM, y por qué el aprendizaje profundo sigue siendo válido en caso de que se infrinja todas las cualidades de la conformación.

## El concepto central.

> **【中文解读】**
> La forma de la función de la conformación es como una taza, pero la SGD en la práctica todavía puede encontrar una buena solución.

> **【拓展：凸优化在工业中的实际规模】**
> El sistema de clasificación de anuncios de Google utiliza la lógica de regreso a gran escala (concentrado en la optimización), procesando miles de millones de solicitudes diarias.

### conjuntos convexos

Un conjunto S es convexo si para cualquier dos puntos en S, el segmento de línea entre ellos también se encuentra enteramente en S.

> Si el conjunto S está en el centro de cualquier línea entre dos puntos completamente ubicado en S dentro, entonces S es un conjunto de puntos convexos.

| Convex sets | Not convex |
|---|---|
| **Rectangle**: any two points inside can be connected by a line segment that stays inside | **Star/crescent shape**: a line between two interior points can pass outside the set |
| **Triangle**: same property holds for all interior points | **Donut/annulus**: the hole means some line segments leave the set |
| The line segment between any two points stays within the set | The line segment between some pairs of points exits the set |

Prueba formal: para cualquier punto x, y en S y cualquier t en [0, 1], el punto tx + (1-t) y también está en S.

> 形式化测试: para S en el medio de cualquier punto x、y 和 [0, 1] en el medio de cualquier t, punto tx + (1-t) y también en el medio de S。

Ejemplos de conjuntos convexos:
- Una línea, un plano, todo R^n
  Una línea recta, una plana, toda la R^n
- Una bola (círculo, esfera, hiperesfera)
  Una bola (en inglés)
- Un medio espacio: {x: a^T x <= b}
  半空间: {x: a^T x <= b}
- La intersección de cualquier número de conjuntos convexos
  任意数凸集的交交集 任意数凸集的交交集 交集 交集 交集 交集 交集 交集 交集 交集 交集 交集 交集 交集 交集 交集 交集 交集 交集 交集 交集 交集 交集 交集 交集 交集 交集 交集 交集 交集 交集 交集 交集 交集 交集 交集 交集 交集 交集 交集 交集 交集 交集 交集 交集 交集 交集 交集 交集 交集 交集 交集 交集 交集 交集 交集 交集 交集 交集 交集 交集 交集 交集 交集 交集 交集 交集 交集 交集 交集 交集 交集 交集 交集 交集 交集 交集 交集 交集 交集 交集 交集 交集 交集 交集 交集 交集 交集 交集 交集 交集 交集 交集 交集 交集 交集 交集 交集 交集 交集 交集 交集 交集 交

Ejemplos de conjuntos no convexos:
- Un donut (annulo)
  环面(lugar)
- La unión de dos círculos desarticulados
  两个不相交圆的并集
- Cualquier conjunto con un "dent" o "agujero"
   cualquier colección de "陷" o "洞"

### Funciones convexas

Una función f es convexa si su dominio es un conjunto convexo y para cualquier dos puntos x, y en su dominio y cualquier t en [0, 1]:

> Si la función f define un dominio de forma gráfica, y para el dominio definido, cualquier dos puntos x、y y [0, 1] de cualquier t:

```
f(tx + (1-t)y) <= t*f(x) + (1-t)*f(y)
```

Geométricamente: el segmento de línea entre cualquier dos puntos del gráfico se encuentra por encima o en el gráfico.

> 几何上: el intervalo entre cualquier punto del cuadro se encuentra en la parte superior o en la parte superior del cuadro.

| Property | Convex function | Non-convex function |
|---|---|---|
| **Line segment test** | The line between any two points on the graph lies **above or on** the curve | The line between some points on the graph dips **below** the curve |
| **Shape** | Single bowl/valley curving upward | Multiple peaks and valleys with mixed curvature |
| **Local minima** | Every local minimum is the global minimum | Multiple local minima may exist at different heights |

Funciones convexas comunes:
- f(x) = x^2 (parabola)
  抛物线
- f(x) = ↓ x (valor absoluto)
   Valor absoluto
- f(x) = e^x (exponencial)
  Funcciones de la
- f(x) = max(0, x) (ReLU, aunque lineal en forma de pieza)
  ReLU(aunque分段线性)
- f(x) = -log(x) para x > 0 (log negativo)
  负对数 (nombre negativo)
- Cualquier función lineal f ((x) = a^T x + b (tanto convexa como cóncava)
  任何线性函数 ((既是凸的也是的)

### Pruebas de convexidad

Tres pruebas prácticas, desde las más fáciles hasta las más rigurosas.

> Tres tipos de pruebas prácticas, desde las más simples hasta las más estrictas.

**Test 1: Second derivative test (1D).**Si f'(x) >= 0 para todos los x, entonces f es convexa.

> **测试 1：二阶导数测试（一维）。**Si para todos los x hay f'(x) >= 0, entonces f es de simbología.

- f''(x) = x^2: f''(x) = 2 >= 0.
- f''(x) = x^3: f''(x) = 6x. negativo para x < 0. No es convexa.
- F''(x) = e^x: f''(x) = e^x > 0.

**Test 2: Hessian test (multivariate).**Si la matriz hessiana H(x) es semidefinita positiva para todas las x, entonces f es convexa.

> **测试 2：Hessian 测试（多变量）。**Si Hessian 矩阵 H(x) para todos los x ∈ X es medio correcto, entonces f ∈ H ∈ H ∈ H ∈ H ∈ H ∈ H ∈ H ∈ H ∈ H ∈ H ∈ H ∈ H ∈ H ∈ H ∈ H ∈ H ∈ H ∈ H ∈ H ∈ H ∈ H ∈ H ∈ H ∈ H ∈ H ∈ H ∈ H ∈ H ∈ H ∈ H ∈ H ∈ H ∈ H ∈ H ∈ H ∈ H ∈ H ∈ H ∈ H ∈ H ∈ H ∈ H ∈ H ∈ H ∈ H ∈ H ∈ H ∈ H ∈ H ∈ H ∈ H ∈ H ∈ H ∈ H ∈ H ∈ H ∈ H ∈ H ∈ H ∈ H ∈ H ∈ H ∈ H ∈ H ∈ H ∈ H ∈ H ∈ H ∈ H    ∈ H                                                                                                                                                                                                                                                                                 

**Test 3: Definition test.**Verifique la desigualdad f(tx + (1-t) y) <= t*f(x) + (1-t) *f(y) directamente.

> **测试 3：定义测试。**直接检查不等式 f(tx + (1-t) y) <= t*f(x) + (1-t) *f(y)。适用于导数难以计算的函数。

### Por qué es importante la convexidad

El teorema central de la optimización convexa:

**For a convex function, every local minimum is a global minimum.**

> **对于凸函数，每个局部最小值都是全局最小值。**

Esto significa que el descenso de gradiente no puede quedar atrapado. Cualquier camino descendente conduce a la misma respuesta. El algoritmo está garantizado para converger a la solución óptima.

> Esto significa que la baja de la escala no se quedará atrapada.

> **【中文解读】**
> Es la teoría central de la optimización de la campa: el valor mínimo de cada ubicación de la función de campa es el valor mínimo de la totalidad. Esto significa que la reducción de la gradiencia nunca estará en la mejor parte de la "variedad".

```mermaid
graph LR
    subgraph "Convex: ONE answer"
        direction TB
        C1["Loss surface has a single valley"] --> C2["Gradient descent ALWAYS finds the global minimum"]
    end
    subgraph "Non-convex: MANY traps"
        direction TB
        N1["Loss surface has multiple valleys and peaks"] --> N2["Gradient descent may get stuck in a local minimum"]
        N2 --> N3["Global minimum might be missed"]
    end
```

Consecuencias:
- No hay necesidad de reiniciar al azar
  No necesita reiniciar
- No se necesitan programas de aprendizaje sofisticados
  No necesita una complejidad de la tasa de aprendizaje
- Las pruebas de convergencia son posibles (la tasa depende de las propiedades de la función)
  Puede probar la recepción (la velocidad depende de la naturaleza de la función)
- La solución es única (hasta regiones planas)
  解是唯一的(excepto la región plana)

### Conveja vs no conveja en ML

| Problem | Convex? | Why |
|---------|---------|-----|
| Linear regression (MSE) | Yes | Loss is quadratic in weights |
| Logistic regression | Yes | Log-loss is convex in weights |
| SVM (hinge loss) | Yes | Maximum of linear functions |
| LASSO (L1 regression) | Yes | Sum of convex functions is convex |
| Ridge regression (L2) | Yes | Quadratic + quadratic = convex |
| Neural network (any loss) | No | Nonlinear activations create non-convex landscape |
| k-means clustering | No | Discrete assignment step |
| Matrix factorization | No | Product of unknowns |

Los modelos lineales con pérdidas convexas son convexas. En el momento en que se añaden capas ocultas con activaciones no lineales, se rompe la convexidad.

>  Con pérdida de consonancia, el modelo lineal es consonancia. Una vez que se añade con la activación no lineal de la capa oculta, la consonancia se rompe.

### La matriz hesiana

La Hesiana de una función f: R^n -> R es la matriz n x n de derivados parciales segundos.

> 函数 f: R^n -> R de Hessian 矩阵 H es n x n de la segunda etapa de la dirección de la matriz。

```
H[i][j] = d^2 f / (dx_i dx_j)
```

Para f ((x, y) = x^2 + 3xy + y^2:

```
df/dx = 2x + 3y       d^2f/dx^2 = 2      d^2f/dxdy = 3
df/dy = 3x + 2y       d^2f/dydx = 3      d^2f/dy^2 = 2

H = [ 2  3 ]
    [ 3  2 ]
```

El Hessiano te dice acerca de la curvatura:
- Valores propios todos positivos: la función se curva hacia arriba en todas las direcciones (convexa en ese punto)
  Términos de la función: La función está en cada dirección
- Valores propios todos negativos: curvas hacia abajo en todas las direcciones (concavo, una máxima local)
  Títulos de la serie: El valor máximo de la serie es el valor máximo de la serie.
- Signos mixtos: punto de silla (curvas hacia arriba en algunas direcciones, hacia abajo en otras)
  混合符号: 点( ciertas direcciones hacia arriba, otras direcciones hacia abajo)
- Valor propio cero: plano en esa dirección (degenerado)
  零特征值:该方向平坦(退化)

Para la convexidad, el hesiano debe ser semidefinido positivo (todos los valores propios >= 0) en todas partes, no solo en un punto.

> Para la consonancia, el Hessian tiene que estar en cualquier lugar y todo su valor es medio correcto, no sólo en un punto.

### El método de Newton

El descenso de gradiente utiliza información de primer orden (el gradiente). El método de Newton utiliza información de segundo orden (el Hessiano).

> 梯度下降使用一阶信息(梯度) ――牛顿法使用二阶信息(Hessian) ・・・ se adapta a una segunda aproximación en el punto actual, y luego se junta directamente al valor mínimo de la función segunda。

```
Update rule:
  x_new = x - H^(-1) * gradient

Compare to gradient descent:
  x_new = x - lr * gradient
```

El método de Newton reemplaza la tasa de aprendizaje escalar por el Hessiano inverso. Esto ajusta automáticamente el tamaño y la dirección del paso en función de la curvatura local.

> 牛顿法用逆 Hessian 替代标标量学习率── esto se basa en la local de la curvatura de la manera automática de ajustar el progreso y la dirección──

> **【拓展：牛顿法在现代 ML 中的实际使用】**
> Aunque el método de Newton no es práctico en el aprendizaje profundo, pero sigue siendo el principal en el ML clásico. XGBoost y LightGBM en la construcción de cada árbol, se desarrolla en segundo plano la función de pérdida.

```mermaid
graph TD
    subgraph "Gradient Descent"
        GD1["Start"] --> GD2["Step 1"]
        GD2 --> GD3["Step 2"]
        GD3 --> GD4["..."]
        GD4 --> GD5["Step ~500: Converged"]
        GD_note["Follows gradient blindly — many small steps"]
    end
    subgraph "Newton's Method"
        NM1["Start"] --> NM2["Step 1"]
        NM2 --> NM3["..."]
        NM3 --> NM4["Step ~5: Converged"]
        NM_note["Uses curvature for optimal steps"]
    end
```

Las ventajas:
- Convergencia cuadrática cerca del mínimo (cuadrados de errores en cada paso)
  En el segundo recibo de la mínima de la cantidad (en el segundo recibo de la cantidad de la cantidad de la cantidad de la cantidad de la cantidad de la cantidad de la cantidad de la cantidad de la cantidad de la cantidad de la cantidad de la cantidad de la cantidad de la cantidad de la cantidad de la cantidad de la cantidad de la cantidad de la cantidad de la cantidad de la cantidad de la cantidad de la cantidad de la cantidad de la cantidad de la cantidad de la cantidad de la cantidad de la cantidad de la cantidad de la cantidad de la cantidad de la cantidad de la cantidad de la cantidad de la cantidad de la cantidad de la cantidad de la cantidad de la cantidad de la cantidad de la cantidad de la cantidad de la cantidad de la cantidad de la cantidad de la cantidad de la cantidad de la cantidad de la cantidad de la cantidad de la cantidad de la cantidad de la cantidad de la cantidad de la cantidad de la cantidad de la cantidad de la cantidad de la cantidad de la cantidad de la cantidad de la cantidad de la cantidad de la cantidad de la cantidad de la cantidad de la cantidad de la cantidad de la cantidad de la cantidad de la cantidad de la cantidad de la cantidad de la cantidad de la cantidad de la cantidad de la cantidad de la cantidad de la cantidad de la cantidad de la cantidad de la cantidad de la cantidad de la cantidad de la cantidad de la cantidad de la cantidad de la cantidad de la cantidad de la cantidad de la cantidad de la cantidad de la cantidad de la cantidad de la cantidad de la cantidad de la cantidad de la cantidad de la cantidad de la cantidad de la cantidad de la cantidad de la cantidad de la cantidad de la cantidad de la cantidad de la cantidad de la cantidad de la cantidad de la cantidad de la cantidad de la cantidad de la cantidad de la cantidad de la cantidad de la cantidad de la cantidad de la cantidad de la cantidad de la cantidad de la cantidad de la cantidad de la cantidad de la cantidad de la cantidad de la cantidad de la cantidad de la cantidad de la cantidad de la cantidad de la cantidad de la cantidad de la cantidad de la cantidad de la cantidad de la cantidad de la cantidad de la cantidad de la cantidad de la cantidad de la cantidad de la cantidad de la cantidad de la cantidad de la cantidad de la cantidad de la cantidad de la cantidad de la cantidad de la cantidad de la cantidad de la cantidad de la cantidad de la cantidad de la cantidad de la cantidad de la cantidad de la cantidad de la cantidad de la cantidad de la cantidad de la cantidad de la cantidad de
- No hay ritmo de aprendizaje para sintonizar
  无需调节 aprendizaje
- Invariante de escala (funciona independientemente de cómo parametrice el problema)
  尺度不变 (cualquiera que sea el problema de la estadística)

Desventajas:
- El cálculo de los costes de Hessian O  n ^ 2) memoria y O  n ^ 3) para invertir
  计算 Hessian 需要 O(n^2) 内存和 O(n^3) 求逆
- Para una red neuronal con 1 millón de pesos, es decir, 10^12 entradas y 10^18 operaciones
  Para un millón de pesos de la red neuronal, eso es 10^12 elementos y 10^18 veces el cálculo.
- No es práctico para el aprendizaje profundo
  No es adecuado para el aprendizaje profundo

### Optimización limitada

Optimización sin restricciones: minimizar f ((x) sobre todos los x.
Optimización limitada: minimizar f ((x) sujeto a restricciones.

> 无约束优化: 在所有 x 上最小化 f(x)。约束优化: 在约束条件下最小化 f(x)。

Los problemas reales tienen limitaciones. Quiere reducir el costo pero su presupuesto es limitado. Quiere reducir al mínimo el error pero su complejidad del modelo es limitada.

> El verdadero problema tiene un límite. Quieres minimizar el costo pero el presupuesto es limitado.

```mermaid
graph LR
    subgraph "Unconstrained"
        U1["Loss function"] --> U2["Free minimum: lowest point of the loss surface"]
    end
    subgraph "Constrained"
        C1["Loss function"] --> C2["Constrained minimum: lowest point within the feasible region"]
        C3["Constraint boundary limits the search space"]
    end
```

### Multiplicadores de laranja

El método de los multiplicadores de Lagrange convierte un problema limitado en uno sin restricciones.

> La ley de la libertad se transformará en la libertad.

Problema: minimizar f(x) sujeto a g(x) = 0.

Solución: introducir una nueva variable (la lambda del multiplicador de Lagrange) y resolver el problema sin restricciones:

```
L(x, lambda) = f(x) + lambda * g(x)
```

En la solución, el gradiente de L es cero:

```
dL/dx = df/dx + lambda * dg/dx = 0
dL/dlambda = g(x) = 0
```

Intuición geométrica: en el mínimo restringido, el gradiente de f debe ser paralelo al gradiente de la restricción g. Si no eran paralelas, se podría mover a lo largo de la superficie de la restricción y reducir f más.

> 几何直觉: en el punto de menor valor del grupo, la gradiencia de f debe ser igual a la gradiencia de g del grupo. Si no es igual, puede moverse en la línea del grupo y reducir aún más f.

```mermaid
graph LR
    A["Contours of f(x,y): concentric ellipses"] --- S["Solution point"]
    B["Constraint curve g(x,y) = 0"] --- S
    S --- C["At the solution, gradient of f is parallel to gradient of g"]
```

Ejemplo: minimizar f ((x,y) = x^2 + y^2 sujeto a x + y = 1.

```
L = x^2 + y^2 + lambda(x + y - 1)

dL/dx = 2x + lambda = 0  =>  x = -lambda/2
dL/dy = 2y + lambda = 0  =>  y = -lambda/2
dL/dlambda = x + y - 1 = 0

From first two: x = y
Substituting: 2x = 1, so x = y = 0.5, lambda = -1
```

El punto más cercano de la línea x + y = 1 al origen es (0,5, 0,5).

> Linea directa x + y = 1 arriba del punto de origen punto más cercano es (0,5, 0,5)。

### Condiciones de la TCC

Las condiciones de Karush-Kuhn-Tucker amplían los multiplicadores de Lagrange a las restricciones de desigualdad.

> KKT 条件(Karush-Kuhn-Tucker Conditions) será拉格朗日乘子推广到不等式约束──

El problema: minimizar f  x) sujeto a g  i  x) <= 0 para i = 1, ..., m.

Las condiciones de KKT (necesarias para la óptimalidad):

```
1. Stationarity:    df/dx + sum(lambda_i * dg_i/dx) = 0
2. Primal feasibility:  g_i(x) <= 0  for all i
3. Dual feasibility:    lambda_i >= 0  for all i
4. Complementary slackness:  lambda_i * g_i(x) = 0  for all i
```

La flexibilidad complementaria es la clave: o bien la restricción es activa (g_i = 0, la solución se encuentra en el límite) o el multiplicador es cero (la restricción no importa).

> 互补松性(Complementary Slackness) 是关键洞察: 要么约束是活跃的(g_i = 0,解在边界上), 要么乘子为零(约束不重要) 不影响解的约束其 lambda = 0。

Las condiciones de KKT son centrales para los SVM. Los vectores de apoyo son los puntos de datos en los que la restricción está activa (lambda > 0).

> KKT 条件是 SVM's核心──支持向量──Support Vectors)就是约束活跃的那些数据点──lambda > 0)──所有其他数据点的 lambda = 0,不影响决策边界──

> **【中文解读】**
> La condición de KKT es la versión más popular de la secuencia de pasajes, el tratamiento de la secuencia de pasajes. La interacción de pasajes es la más exquisita: para cada secuencia, o bien es "activa" (sólo se puede tocar la frontera), o bien es una secuencia de pasajes sin efectos.

### Regularización como optimización limitada

La regularización de L1 y L2 no son trucos arbitrarios, son problemas de optimización limitada disfrazados.

> La normalización L1 y L2 no son técnicas arbitrarias. Son problemas de optimización de la limitación de las falsas formas.

**L2 regularization (Ridge):**

```
minimize  Loss(w)  subject to  ||w||^2 <= t

Equivalent unconstrained form:
minimize  Loss(w) + lambda * ||w||^2
```

La restricción de la pérdida en la pérdida de la pérdida de la pérdida de la pérdida de la pérdida de la pérdida de la pérdida de la pérdida de la pérdida de la pérdida de la pérdida de la pérdida de la pérdida de la pérdida de la pérdida de la pérdida de la pérdida de la pérdida de la pérdida de la pérdida de la pérdida de la pérdida de la pérdida de la pérdida de la pérdida de la pérdida de la pérdida de la pérdida de la pérdida de la pérdida de la pérdida de la pérdida de la pérdida de la pérdida de la pérdida de la pérdida de la pérdida de la pérdida de la pérdida de la pérdida de la pérdida de la pérdida de la pérdida de la pérdida de la pérdida de la pérdida de la pérdida de la pérdida de la pérdida de la pérdida de la pérdida de la pérdida de la pérdida de la pérdida de la pérdida de la pérdida de la pérdida de la pérdida de la pérdida de la pérdida de la pérdida de la pérdida de la pérdida de la pérdida de la pérdida de la pérdida de la pérdida de la pérdida de la pérdida de la pérdida de la pérdida de la pérdida de la pérdida de la pérdida de la pérdida de la pérdida de la pérdida de la pérdida de la pérdida de la pérdida de la pérdida de la pérdida de la pérdida de la pérdida de la pérdida de la pérdida de la pérdida de la pérdida de la pérdida de la pérdida de la pérdida de la pérdida de la pérdida de la pérdida de la pérdida de la pérdida de la pérdida de la pérdida de la pérdida de la pérdida de la pérdida de la pérdida de la pérdida de la pérdida de la pérdida de la pérdida de la pérdida de la pérdida de la pérdida de la pérdida.

> 约束 约束 约束 约束 约束 约束 约束 约束 约束 约束 约束 约束 约束 约束 约束 约束 约束 约束 约束 约束 约束 约束 约束 约束 约束 约束 约束 约束 约束 约束 约束 约束 约束 约束 约束 约束 约束 约束 约束 约束 约束 约束 约束 约束 约束 约束 约束 约束 约束 约束 约束 约束 约束 约束 约束 约束 约束 约束 约束 约束 约束 约 约 约 约 约 约 约 约 约 约 约 约 约 约 约 约 约 约 约 约 约 约 约 约 约 约 约 约 约 约 约 约 约 约 约 约 约 约                                                                                                                                                                                                                                                           

**L1 regularization (LASSO):**

```
minimize  Loss(w)  subject to  ||w||_1 <= t

Equivalent unconstrained form:
minimize  Loss(w) + lambda * ||w||_1
```

La restricción de la cantidad de diamantes definida en 2D (cuadrado rotado).

> 约束 约束 约束 约束 约束 约束 约束 约束 约束 约束 约束 约束 约束 约束 约束 约束 约束 约束 约束 约束 约束 约束 约束 约束 约束 约束 约束 约束 约束 约束 约束 约束 约束 约束 约束 约束 约束 约束 约束 约束 约束 约束 约束 约束 约束 约束 约束 约束 约束 约束 约束 约束 约束 约束 约束 约束 约束 约束 约束 约束 约束 约束 约束 约束 约束 约束 约束 约束 约束 约束 约束 约束 约束 约束 约束 约束 约束 约束 约束 约 约 约 约 约 约 约 约 约 约 约 约 约 约 约 约 约 约 约 约 约 约 约 约 约 约 约 约 约 约 约 约 约 约 约 约 约 约 约 约 约 约 约 约 约 约 约 约 约 约 约 约 约 约 约 约 约 约 约 约 约 约 约 约 约 约 约 约 约 约 约 约 约 约 约    

| Property | L2 constraint (circle) | L1 constraint (diamond) |
|---|---|---|
| **Constraint shape** | Circle (sphere in higher dims) | Diamond (rotated square in 2D) |
| **Where loss contour touches** | Smooth boundary — any point on the circle | Corner — aligned with an axis |
| **Solution behavior** | Weights are small but nonzero | Some weights are exactly zero (sparse) |
| **Result** | Weight shrinkage | Feature selection |

Esto explica por qué L1 produce modelos escasos (selección de características) mientras que L2 solo reduce los pesos. El diamante tiene esquinas alineadas con ejes.

> Esto explica por qué L1 produce un modelo raro (títulos seleccionados) y L2 sólo se reduce en peso.

> **【拓展：L1 正则化与 L2 正则化的几何直觉】**
> La forma del enlace L1 es de forma cuadrada, en 2D es de forma rotativa, en 2D es de forma cuadrada, en L2 es de forma redonda. La forma del enlace L1 es de forma cuadrada. La forma del enlace L1 es de forma cuadrada. La forma del enlace L1 es de forma cuadrada. La forma del enlace L1 es de forma cuadrada. La forma del enlace L1 es de forma cuadrada. La forma del enlace L1 es de forma cuadrada. La forma del enlace L1 es de forma cuadrada. La forma del enlace L1 es de forma cuadrada. La forma del enlace L1 es de forma cuadrada. La forma del enlace L1 es de forma cuadrada. La forma del enlace L1 es de forma cuadrada. La forma del enlace L1 es de forma cuadrada. La forma del enlace L1 es de forma cuadrada. La forma del enlace L1 es de forma cuadrada. La forma del en 2D es de forma cuadrada. La forma del en 2D es de forma cuadrada. La forma de en 2D es de forma cuadrada es de la forma cuadrada. La forma de la forma de la enla enlace L2 es de la forma de la forma de la enlace L2 es de la forma de la forma de la enlace L2 es de la forma de la enla enla enlaza es de la es en el enlaza es en el eje de la esfera de la esfera de la esfera de la esfera de la esfera de la esfera de la esfera de la esfera de la esfera de la esfera de la esfera de la esfera de la esfera de la esfera de la esfera de la esfera de la esfera de la esfera de la esfera de la esfera de la esfera de la esfera de la esfera de la esfera. Enlace L2 esfera de la esfera de la esfera de la esfera de la esfera de la esfera de la esfera de la esfera de la esfera de la esfera de la esfera de la esfera de la esfera de la esfera de la esfera de la esfera de la esfera de la esfera de la esfera de la esfera de la

### La dualidad

Cada problema de optimización limitada (el primario) tiene un problema compañero (el dual). Para los problemas convexos, el primario y el dual tienen el mismo valor óptimo. Esta es una fuerte dualidad.

> Cada problema de optimización de la estructura (problema original) tiene un problema asociado (problema de par) ⋅ para el problema de la estructura, el problema original y el problema de par tienen el mismo valor óptimo ⋅ esto es la fuerte paridad (problema original) ⋅ fuerte dualidad (problema de par) ⋅

La función dual de Lagrangian:

```
Primal: minimize f(x) subject to g(x) <= 0
Lagrangian: L(x, lambda) = f(x) + lambda * g(x)
Dual function: d(lambda) = min_x L(x, lambda)
Dual problem: maximize d(lambda) subject to lambda >= 0
```

Por qué la dualidad es importante:
- El problema dual es a veces más fácil de resolver que el primordial
  Para los problemas de la pareja a veces es más fácil resolver que el problema original
- Los SVM se resuelven en su forma dual, donde el problema depende de productos de puntos entre los puntos de datos (habilitando el truco del núcleo)
  SVM en forma de búsqueda de solución, el problema depende sólo de los puntos entre los puntos de datos (para poder utilizar técnicas nucleares)
- El doble proporciona un límite inferior en el óptimo primario, útil para comprobar la calidad de la solución
  Para el par para el valor óptimo original, proporcionar un límite inferior, para la calidad de la prueba de resolución

Para los SVM específicamente:

```
Primal: find w, b that maximize the margin 2/||w|| subject to
        y_i(w^T x_i + b) >= 1 for all i

Dual:   maximize sum(alpha_i) - 0.5 * sum_ij(alpha_i * alpha_j * y_i * y_j * x_i^T x_j)
        subject to alpha_i >= 0 and sum(alpha_i * y_i) = 0

The dual only involves dot products x_i^T x_j.
Replace x_i^T x_j with K(x_i, x_j) to get the kernel trick.
```

### Por qué el aprendizaje profundo funciona a pesar de la no convexidad

Las funciones de pérdida de red neuronal son muy no convexas. Por todas las medidas clásicas, la optimización de ellas debería fallar. Sin embargo, el descenso de gradiente estocástico encuentra buenas soluciones confiablemente. Varios factores explican esto.

> La función de pérdida de redes neuronales es extremadamente inexplicable. Según la teoría clásica, la optimización de ellas debería fracasar.

**Most local minima are good enough.**En los espacios de alta dimensión, los puntos críticos aleatorios (donde el gradiente es cero) son en su mayoría puntos de sella, no mínimos locales. Los pocos mínimos locales que existen tienden a tener valores de pérdida cercanos al mínimo global.

> **大多数局部最小值都足够好。**En el espacio alto, los puntos de límite de los elementos de la dimensión (grado a cero) son en la mayoría de los puntos, y no en el valor mínimo local. La pérdida de los valores mínimos locales de una minoría de elementos de la dimensión local suele acercarse al valor mínimo de la dimensión total.

**Saddle points, not local minima, are the real obstacle.**En una función con n parámetros, un punto de sillón tiene una mezcla de direcciones de curvatura positiva y negativa. Para un punto crítico aleatorio en dimensiones altas, la probabilidad de que todos los n valores propios sean positivos (mínimo local) es aproximadamente 2 ^ - n. Casi todos los puntos críticos son puntos de sillón.

> **鞍点而非局部最小值才是真正的障碍。**En las funciones de n 个参数, 点具有正负曲率方向的混合──对于高维中的随机临界点, todas las n 个特征值都为正的 (n 个局部最小值) 的概率为2^(-n)──几乎所有的临界点都是点──SGD的噪音帮助逃离它们──

**Overparameterization smooths the landscape.**Las redes con más parámetros que los ejemplos de entrenamiento tienen superficies de pérdida más suaves y conectadas. Las redes más amplias tienen menos mínimos locales negativos. Esto es contrario a la intuición pero empíricamente consistente.

> **过参数化（Overparameterization）使损失面更平滑。**参数 más que el entrenamiento de la muestra de red tiene una superficie de pérdida más plana, más conectada.  Red más amplia tiene un valor mínimo de mal localización menor.

**Loss landscape structure:**

| Property | Low-dimensional space | High-dimensional space |
|---|---|---|
| **Landscape** | Many isolated peaks and valleys | Smoothly connected valleys |
| **Minima** | Many isolated local minima | Few bad local minima; most are near-optimal |
| **Navigation** | Hard to find global minimum | Many paths lead to good solutions |
| **Critical points** | Mix of local minima and saddle points | Overwhelmingly saddle points, not local minima |

**Stochastic noise acts as implicit regularization.**El SGD de mini lote añade ruido que evita que se establezca en mínimos nítidos. mínimos nítidos se sobreajustan; mínimos planos se generalizan. El ruido favorece la optimización hacia regiones planas del paisaje de pérdidas.

> **随机噪声充当隐式正则化。**Los pequeños grupos de SGD añaden el ruido para evitar que se caiga en el extremo menor de la superficie.

> **【中文解读】**
> El éxito del aprendizaje profundo parece infringir la teoría de la optimización de la conformación: las funciones no conformaciones deberían ser muy difíciles de optimizar, pero SGD funciona muy bien. Hay tres razones: primero, casi todos los puntos críticos en el espacio alto son valores mínimos de puntos y no locales; segundo, la overparametrización hace que la pérdida de superficie sea más plana; tercero, el ruido de SGD se carga con una normalización oculta, ayuda a escapar de los valores extremos más pequeños, encuentra una mejor solución a la generalización más plana.

### Métodos de segundo orden en la práctica

El método de Newton puro es poco práctico para modelos grandes. Varias aproximaciones hacen que la información de segundo orden sea utilizable.

> La pura ley de Newton sobre el gran modelo no es práctica.

**L-BFGS (Limited-memory BFGS):**Se aproxima al Hessiano inverso utilizando las últimas diferencias de gradiente m. Requiere memoria O(mn en lugar de O(n^2). Funciona bien para problemas con hasta ~ 10.000 parámetros. Se utiliza en ML clásico (regressión logística, CRFs) pero no en aprendizaje profundo.

> **L-BFGS：**Utiliza m 个梯度差近似逆 Hessian──需要 O(mn) 内存而不是 O(n^2)── se aplica a la mayoría de las preguntas de aproximadamente 10.000 个参数── se utiliza en el clásico ML(lógico regreso、CRF) pero no se utiliza en profundidad de aprendizaje──

**Natural gradient:**Utiliza la matriz de información de Fisher (Hessian esperado de la probabilidad de registro) en lugar del Hessian estándar. Esto explica la geometría de las distribuciones de probabilidad. K-FAC (Curvatura aproximada con factores de Cronécker) se aproxima a la matriz de Fisher como un producto de Cronécker, lo que la hace práctica para las redes neuronales.

> **自然梯度（Natural Gradient）：**Utiliza Fisher 信息矩阵 (Hessian) para el número similar a la expectativa Hessian) sustitución estándar Hessian。 esto tiene en cuenta la probabilidad de distribución de la estructura geográfica。 K-FAC pondrá Fisher 矩阵 de manera similar a Kronecker 乘积, lo que lo hace disponible en la red neuronal。

**Hessian-free optimization:**Utiliza gradiente conjugado para resolver Hx = g sin formar nunca H. Solo requiere productos de vector hessiano, que se pueden calcular en tiempo O ((n) a través de diferenciación automática.

> **无 Hessian 优化：**Utiliza la contagia de la escala para resolver Hx = g y no necesita formar H. Sólo se necesita Hessian-向量乘积, se puede calcular automáticamente en O (n) 时间内.

**Diagonal approximations:**El segundo momento de Adam es una aproximación diagonal de la diagonal de Hessian. AdaHessian lo extiende utilizando elementos diagonales de Hessian reales a través del estimador de Hutchinson.

> **对角近似：**La segunda etapa de Adam es la aproximación de Hessian a la línea de la esquina. AdaHessian   Hutchinson  estimador                                                                                                                                                                                                                                              

| Method | Memory | Per-step cost | When to use |
|--------|--------|--------------|-------------|
| Gradient descent | O(n) | O(n) | Baseline, large models |
| Newton's method | O(n^2) | O(n^3) | Small convex problems |
| L-BFGS | O(mn) | O(mn) | Medium convex problems |
| Adam | O(n) | O(n) | Deep learning default |
| K-FAC | O(n) | O(n) per layer | Research, large-batch training |

## Construye y realiza.
```figure
convex-vs-nonconvex
```

## Construye el mismo

### Paso 1: Verificación de convexidad

Construir una función que prueba la convexidad empíricamente mediante muestreo de puntos y comprobar la definición.

> Construir una función, a través de la toma de puntos y la revisión de la definición para experimentar la prueba de la cualidad.

```python
import random
import math

def check_convexity(f, dim, bounds=(-5, 5), samples=1000):
    violations = 0
    for _ in range(samples):
        x = [random.uniform(*bounds) for _ in range(dim)]  # 随机采样点 x
        y = [random.uniform(*bounds) for _ in range(dim)]  # 随机采样点 y
        t = random.uniform(0, 1)                            # 随机混合系数
        mid = [t * xi + (1 - t) * yi for xi, yi in zip(x, y)]  # 凸组合 tx + (1-t)y
        lhs = f(mid)                                        # f(凸组合)
        rhs = t * f(x) + (1 - t) * f(y)                    # tf(x) + (1-t)f(y)
        if lhs > rhs + 1e-10:                               # 违反凸性不等式
            violations += 1
    return violations == 0, violations
```

### Paso 2: El método de Newton para 2D

Implemente el método de Newton usando un Hessiano explícito. Compara la velocidad de convergencia con el descenso de gradiente.

> Utilización de la teoría de Newton en Hessian.

```python
def newtons_method(f, grad_f, hessian_f, x0, steps=50, tol=1e-12):
    x = list(x0)
    history = [x[:]]
    for _ in range(steps):
        g = grad_f(x)
        H = hessian_f(x)
        det = H[0][0] * H[1][1] - H[0][1] * H[1][0]
        if abs(det) < 1e-15:
            break
        H_inv = [
            [H[1][1] / det, -H[0][1] / det],
            [-H[1][0] / det, H[0][0] / det],
        ]
        dx = [
            H_inv[0][0] * g[0] + H_inv[0][1] * g[1],
            H_inv[1][0] * g[0] + H_inv[1][1] * g[1],
        ]
        x = [x[0] - dx[0], x[1] - dx[1]]
        history.append(x[:])
        if sum(gi ** 2 for gi in g) < tol:
            break
    return history
```

### Paso 3: Solvente del multiplicador de laranja

Resolver la optimización limitada utilizando el descenso de gradiente en el Lagrangiano.

> Utiliza la gradiente de la función de la longitud baja en la búsqueda de la optimización de la función de la longitud.

```python
def lagrange_solve(f_grad, g_val, g_grad, x0, lr=0.01,
                   lr_lambda=0.01, steps=5000):
    x = list(x0)
    lam = 0.0
    history = []
    for _ in range(steps):
        fg = f_grad(x)
        gv = g_val(x)
        gg = g_grad(x)
        x = [
            xi - lr * (fgi + lam * ggi)
            for xi, fgi, ggi in zip(x, fg, gg)
        ]
        lam = lam + lr_lambda * gv
        history.append((x[:], lam, gv))
    return history
```

### Paso 4: Comparar el primer orden con el segundo orden

Ejecutar la descenda de gradiente y el método de Newton en la misma función cuadrática.

```python
def quadratic(x):
    return 5 * x[0] ** 2 + x[1] ** 2

def quadratic_grad(x):
    return [10 * x[0], 2 * x[1]]

def quadratic_hessian(x):
    return [[10, 0], [0, 2]]
```

El método de Newton convergerá en 1 paso (es exacto para la cuadrática).

> La ley de Newton se aplicará en 1 paso a la función secundaria (la siguiente es precisa) ⋅ la disminución del gradiente requiere de cientos de pasos, ya que la diferencia entre los valores de las características del Hessian es 5 veces mayor, formando un valle de gran longitud.

## Usalo con el marco de ejecución

El análisis de convexidad se aplica directamente a la hora de elegir modelos y solventes ML.

> 凸性分析在选择ML模型和求解器时直接适用──

Para los problemas convexos (regressión logística, SVM, LASSO):
- Utilice solventes dedicados (liblinear, CVXPY, scipy.optimize.minimize con método='L-BFGS-B')
  Utilización de búsqueda de soluciones
- Esperar una solución global única
  期望唯一的全局解 期望唯一的全局解
- Los métodos de segundo orden son prácticos y rápidos
  2o paso método práctico y rápido

Para los problemas no convexos (redes neuronales):
- Utilice métodos de primer orden (SGD, Adam)
  Utiliza un método de primera clase
- Aceptar que la solución depende de la inicialización y la aleatoriedad
  Acceptar la solución depende de la iniciación y la casualidad
- Utilice los horarios de sobreparametrización, ruido y tasa de aprendizaje como regularización implícita
  Usar la regulación de los parámetros, ruido y la tasa de aprendizaje como forma de regularización
- No pierdas tiempo buscando el mínimo global.
  No pierdas tiempo buscando el mínimo de la zona.

```python
from scipy.optimize import minimize

result = minimize(
    fun=lambda w: sum((y - X @ w) ** 2) + 0.1 * sum(w ** 2),
    x0=np.zeros(d),
    method='L-BFGS-B',
    jac=lambda w: -2 * X.T @ (y - X @ w) + 0.2 * w,
)
```

Para los SVM, la fórmula dual permite usar el truco del núcleo:

> Para SVM, para forma ocasional, puedes usar el trucos nucleares:

```python
from sklearn.svm import SVC

svm = SVC(kernel='rbf', C=1.0)
svm.fit(X_train, y_train)
print(f"Support vectors: {svm.n_support_}")
```

## Los ejercicios.

1. **Convexity gallery.**Prueba estas funciones para la convexidad utilizando el comprobador: f(x) = x^4, f(x) = sin(x), f(x,y) = x^2 + y^2, f(x,y) = x*y, f(x) = max(x, 0). Explique por qué cada resultado tiene sentido.

2. **Newton vs gradient descent race.**¿Cuántos pasos necesita cada uno para alcanzar la pérdida < 1e-10? ¿Qué sucede con el descenso de gradiente cuando el número de condición (ratio de mayor a menor valor propio hessiano) aumenta?

3. **Lagrange multiplier geometry.**Minimizar f ((x,y) = (x-3) ^ 2 + (y-3) ^ 2 sujeto a x + 2y = 4. Verificar la solución comprobando que el gradiente de f es paralelo al gradiente de g en la solución.

4. **Regularization constraint.**Implemente la optimización con restricción L1: minimizar (x-3) ^ 2 + (y-2) ^ 2 sujeto a ∙x                                                                                                                                                                                                                                                

5. **Hessian eigenvalue analysis.**Compute el Hessian de la función Rosenbrock en (1,1) y en (-1,1). Compute los valores propios en ambos puntos. ¿Qué le dicen los valores propios sobre la curvatura en el mínimo versus lejos de él?

## Términos clave .

| Term | What it means |
|------|---------------|
| Convex set | A set where the line segment between any two points in the set stays inside the set |
| Convex function | A function where the line between any two points on its graph lies above or on the graph. Equivalently, Hessian is positive semidefinite everywhere |
| Local minimum | A point lower than all nearby points. For convex functions, every local minimum is the global minimum |
| Global minimum | The lowest point of a function over its entire domain |
| Hessian matrix | The matrix of all second partial derivatives. Encodes curvature information |
| Positive semidefinite | A matrix whose eigenvalues are all non-negative. The multidimensional analogue of "second derivative >= 0" |
| Condition number | Ratio of largest to smallest eigenvalue of the Hessian. High condition number means elongated valleys and slow gradient descent |
| Newton's method | Second-order optimizer that uses the inverse Hessian to determine step direction and size. Quadratic convergence near the minimum |
| Lagrange multiplier | A variable introduced to convert a constrained optimization problem into an unconstrained one |
| KKT conditions | Necessary conditions for optimality with inequality constraints. Generalize Lagrange multipliers |
| Complementary slackness | At the solution, either a constraint is active or its multiplier is zero. Never both nonzero |
| Duality | Every constrained problem has a companion dual problem. For convex problems, both have the same optimal value |
| Strong duality | Primal and dual optimal values are equal. Holds for convex problems satisfying Slater's condition |
| L-BFGS | Approximate second-order method that stores the last m gradient differences instead of the full Hessian |
| Saddle point | A point where the gradient is zero but it is a minimum in some directions and a maximum in others |
| Overparameterization | Using more parameters than training examples. Smooths the loss landscape and reduces bad local minima |

## Más Leer más Leer más

- [Boyd & Vandenberghe: Convex Optimization](https://web.stanford.edu/~boyd/cvxbook/)- el libro de texto estándar, disponible gratuitamente en línea
- [Bottou, Curtis, Nocedal: Optimization Methods for Large-Scale Machine Learning (2018)](https://arxiv.org/abs/1606.04838)- puentes de teoría de la optimización convexa y práctica de aprendizaje profundo
- [Choromanska et al.: The Loss Surfaces of Multilayer Networks (2015)](https://arxiv.org/abs/1412.0233)- por qué los paisajes de las redes neuronales no convexas no son tan malos como parecen
- [Nocedal & Wright: Numerical Optimization](https://link.springer.com/book/10.1007/978-0-387-40065-5)- referencia completa del método de Newton, L-BFGS, y optimización limitada
