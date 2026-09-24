# Sistemas lineales

> Resolver Ax = b es el problema más antiguo en matemáticas que aún maneja tu red neuronal.
> 解 Ax=b es el problema más antiguo de las matemáticas, que todavía está impulsando tu red neuronal.

**Type:** Build | **类型:** 动手
**Language:**¿ Qué pasa ?**语言:**Python
**Prerequisites:** Phase 1, Lessons 01 (Linear Algebra Intuition), 02 (Vectors & Matrices), 03 (Matrix Transformations) | **前置知识:** Phase 1, 第 01 课（线性代数直觉）、第 02 课（向量与矩阵）、第 03 课（矩阵变换）
**Time:** ~120 minutes | **时间:** ~120 分钟

## Objetivos de aprendizaje

- Resolver Ax = b utilizando la eliminación de Gaussian con la sustitución parcial y la sustitución de atrás
  Utiliza con la parte principal de la elección de la parte de la parte de la parte de la parte de la parte de la parte de la parte de la parte de la parte de la parte de la parte de la parte de la parte de la parte de la parte de la parte de la parte de la parte de la parte de la parte de la parte de la parte de la parte de la parte de la parte de la parte de la parte de la parte de la parte de la parte de la parte de la parte de la parte de la parte de la parte de la parte de la parte de la parte de la parte de la parte de la parte de la parte de la parte de la parte de la parte de la parte de la parte de la parte de la parte de la parte de la parte de la parte de la parte de la parte de la parte de la parte de la parte de la parte de la parte de la parte de la parte de la parte de la parte de la parte de la parte de la parte de la parte de la parte de la parte de la parte de la parte de la parte de la parte de la parte de la parte de la parte de la parte de la parte de la parte de la parte de la parte de la parte de la parte de la parte de la parte de la parte de la parte de la parte de la parte de la parte de la parte de la parte de la parte de la parte de la parte de la parte de la parte de la parte de la parte de la parte de la parte de la parte de la parte de la parte de la parte de la parte de la parte de la parte de la parte de la parte de la parte de la parte de la parte de la parte de la parte de la parte de la parte de la parte de la parte de la parte de la parte de la parte de la parte de la parte de la parte de la parte de la parte de la parte de la parte de la parte de la parte de la parte de la parte de la parte de la parte de la parte de la parte de la parte de la parte de la parte de la parte de la parte de la parte de la parte de la parte de la parte de la parte de la parte de la parte de la parte de la parte de la parte de la parte de la parte de la parte de la parte de la parte de la parte de la parte de la parte de la parte de la parte de la parte de la parte de la parte de la parte de la parte
- Matrices de factores con descomposiciones LU, QR y Cholesky y explicar cuándo cada una es apropiada
  Utiliza LU、QR 和 Cholesky 分解(Decomposition) descomposición de la matriz,并 explicar los escenarios de cada método
- Derivar las ecuaciones normales para los cuadrados mínimos y conectarlos a regresión lineal y de cresta
  推导最小二乘法正规方程(Equivalencias normales),并将其与线性归归和归归联系起来
- Diagnóstico de sistemas mal condicionados utilizando el número de condición y aplicar regularización para estabilizarlos
  Uso de condiciones Numero de condición) diagnóstico de enfermedad,并应用正则化


> **【中文解读】**
> 解 Ax=b es el problema más antiguo de la matemática. La regulación de la regulación de la regulación de la regulación de la regulación de la regulación de la regulación de la regulación de la regulación de la regulación de la regulación de la regulación de la regulación de la regulación de la regulación de la regulación de la regulación de la regulación de la regulación de la regulación de la regulación de la regulación de la regulación de la regulación de la regulación de la regulación de la regulación de la regulación de la regulación de la regulación de la regulación de la regulación de la regulación de la regulación de la regulación de la regulación de la regulación de la regulación de la regulación de la regulación de la regulación de la regulación de la regulación de la regulación de la regulación de la regulación de la regulación de la regulación de la regulación de la regulación de la regulación de la regulación de la regulación de la regulación de la regulación de la regulación de la regulación de la regulación de la regulación de la regulación de la regulación de la regulación de la regulación de la regulación de la regulación de la regulación de la regulación de la regulación de la regulación de la regulación de la regulación de la regulación de la regulación de la regulación de la regulación de la regulación de la regulación de la regulación de la regulación de la regulación de la regulación de la regulación de la regulación de la regulación de la regulación de la regulación de la regulación de la regulación de la regulación de la regulación de la regulación de la regulación de la regulación de la regulación de la regulación de la regulación de la regulación de la regulación de la regulación de la regulación de la regulación de la regulación de la regulación de la regulación de la regulación de la regulación de la regulación de la regulación de la regulación de la regulación de la regulación de la regulación de la regulación de la regulación de la regulación de la regulación de la regulación de la regulación de la regulación de la regulación de la regulación de la regulación de la regulación de la regula

## El problema es la introducción del problema

Cada vez que entrenas una regresión lineal, resuelves un sistema lineal. Cada vez que computes un ajuste de mínimos cuadrados, resuelves un sistema lineal. Cada vez que una capa de red neuronal computa.`y = Wx + b`Cuando se añade regularización, se modifica el sistema. Cuando se utiliza procesos de Gaussian, se hace una matriz. Cuando se invierte una matriz de covarianza para la distancia de Mahalanobis, se resuelve un sistema lineal.

> Cada entrenamiento de regreso lineal, estás en un sistema lineal. Cada cálculo mínimo de dos veces se adapta, estás en un sistema lineal. Cada cálculo de nivel de red neuronal.`y = Wx + b`, está en el lado de evaluar el sistema lineal. Cuando se añade la normalización, se modifica el sistema. Cuando se utiliza el proceso de Gaussian, se descompone el rectángulo.

La ecuación Ax = b aparece en todas partes. A es una matriz de coeficientes conocidos. b es un vector de resultados conocidos. x es el vector de los desconocidos que desea encontrar. En regresión lineal, A es su matriz de datos, b es su vector objetivo y x es el vector de peso. Todo el modelo se reduce a: encontrar x de tal manera que Ax esté lo más cerca posible de b.

> 方程 Ax = b 无处不在──A es la matriz de los números de datos conocidos, b es la matriz de los números de datos conocidos, x es la matriz de los datos que se requiere, b es la matriz de datos, x es la matriz de los datos, x es la matriz de los valores de los valores de los valores de los datos, b es la matriz de los datos, x es la matriz de los valores de los valores de los valores de los valores de los valores de los valores de los valores de los valores de los valores de los valores de los valores de los valores de los valores de los valores de los valores de los valores de los valores de los valores de los valores de los valores de los valores de los valores de los valores de los valores de los valores de los valores de los valores de los valores de los valores de los valores de los valores de los valores de los valores de los valores de los valores de los valores de los valores de los valores de los valores de los valores de los valores de los valores de los valores de los valores de la matriz de la matriz de la matriz de la matriz de la matriz de la matriz de la matriz de la matriz de la matriz de la matriz de la matriz de la matriz de la matriz de la matriz de la matriz de la matriz de la matriz de la matriz de la matriz de la matriz de la matriz de la matriz de la matriz de la matriz de la matriz de la matriz de la matriz de la matriz de la matriz de la matriz de la matriz de la matriz de la matriz de la matriz de la matriz de la matriz de la matriz de la matriz de la matriz de la matriz de la matriz de la matriz de la matriz de la matriz de la matriz de la matriz de la matriz de la matriz de la matriz de la matriz de la matriz de la matriz de la matriz de la matriz de la matriz de la matriz de la matriz de la matriz de la matriz de la matriz de la matriz de la matriz de la matriz de la matriz de la matriz de la matriz de la matriz de la matriz de la matriz de la

Esta lección construye todos los métodos principales para resolver esa ecuación desde cero. Comprenderá por qué algunos métodos son rápidos y otros estables, por qué algunos funcionan solo para sistemas cuadrados y otros manejan los excesivamente determinados, y por qué el número de condición de su matriz determina si su respuesta significa algo en absoluto.

> En esta clase, se busca resolver todos los métodos principales de la ecuación desde cero. Usted entenderá por qué algunos métodos son rápidos y algunos estables, por qué algunos sólo se aplican a sistemas de cuadros y otros pueden tratar superconstantes, y por qué el número de condiciones de la matriz determina si su respuesta es significativa.

## El concepto central.

> **【中文解读】**
> Para el sistema superestable, no existe una solución exacta, el mínimo de dos veces puede encontrar el "mejor acercamiento" del mínimo de residuos.

> **【拓展：线性系统在推荐系统中的规模】**
> En la competencia del Premio Netflix, el problema de la matriz de descomposición involucró a 480.000 usuarios y 17.770 películas. Este problema de matriz de aproximadamente 500.000 x 17.770 requirió algoritmos de descomposición de matriz de alta eficiencia. El gran concurso de Netflix impulsó el desarrollo de algoritmos de descomposición de matriz a gran escala (SVD, ALS), que hoy en día siguen siendo el núcleo del sistema de recomendación.

### Lo que Ax = b significa geométricamente

Un sistema de ecuaciones lineales tiene una interpretación geométrica. Cada ecuación define un hiperplano. La solución es el punto (o conjunto de puntos) donde todos los hiperplanos se cruzan.

> 线性方程组有几何解释── cada cuadro define un superplano (超平面)──解是所有超平面的交点 (交点) ──

```
2x + y = 5          Two lines in 2D.
x - y  = 1          They intersect at x=2, y=1.
```

```mermaid
graph LR
    A["2x + y = 5"] --- S["Solution: (2, 1)"]
    B["x - y = 1"] --- S
```

Tres cosas pueden suceder:

```mermaid
graph TD
    subgraph "One Solution"
        A1["Lines intersect at a single point"]
    end
    subgraph "No Solution"
        A2["Lines are parallel — no intersection"]
    end
    subgraph "Infinite Solutions"
        A3["Lines are identical — every point is a solution"]
    end
```

En forma de matriz, "una solución" significa que A es invertible. "Ninguna solución" significa que el sistema es inconsistente. "Soluciones infinitas" significa que A tiene un espacio nulo. La mayoría de los problemas de ML caen en la categoría "no solución exacta" porque tienes más ecuaciones (puntos de datos) que desconocidos (parámetros). Es ahí donde entra el menor número de cuadrados.

> Usando el lenguaje de la matriz, "un解" significa A 可逆──"无解" significa sistemas no coinciden──"无穷多解" significa A 有零空间(Null Space)── la mayoría de los problemas de ML pertenecen a la categoría de "无精确解", ya que el cuadro de números (nombre de puntos) es mayor que el número desconocido (参数)──.

### Imagen de columna vs imagen de fila

Hay dos maneras de leer Ax = b.

> Hay dos formas de hacerlo.

**Row picture.**Cada fila de A define una ecuación. Cada ecuación es un hiperplano. La solución es donde se cruzan todas.

> **行视角。**Cada línea de un define un cuadrado. Cada cuadrado es un superplano.

**Column picture.**Cada columna de A es un vector. La pregunta es: ¿qué combinación lineal de las columnas de A produce b?

> **列视角。**Cada una de las líneas de A es un eje. ¿Puede producir b?

```
A = | 2  1 |    b = | 5 |
    | 1 -1 |        | 1 |

Row picture: solve 2x + y = 5 and x - y = 1 simultaneously.

Column picture: find x1, x2 such that:
  x1 * [2, 1] + x2 * [1, -1] = [5, 1]
  2 * [2, 1] + 1 * [1, -1] = [4+1, 2-1] = [5, 1]   check.
```

Si b se encuentra en el espacio de columna de A, el sistema tiene una solución. Si b no lo hace, se encuentra el punto más cercano en el espacio de columna. Ese punto más cercano es la solución de cuadrados mínimos.

> 列视角更根本──如果 b {\displaystyle b} en A {\displaystyle A} {\displaystyle A} {\displaystyle A} {\displaystyle A} {\displaystyle A} {\displaystyle B} {\displaystyle B} {\displaystyle B} {\displaystyle B} {\displaystyle B} {\displaystyle B} {\displaystyle B} {\displaystyle B} {\displaystyle B} {\displaystyle B} {\displaystyle B} {\displaystyle B} {\displaystyle B} {\displaystyle B} {\displaystyle B} {\displaystyle B} {\displaystyle B} {\displaystyle B} {\displaystyle B} {\displaystyle B} {\displaystyle B} {\displaystyle B} {\displaystyle B} {\displaystyle B} {\displaystyle B} }

### Eliminación gaussiana

La eliminación de Gaussian transforma Ax = b en un sistema triangular superior Ux = c que se resuelve mediante la sustitución posterior. Es el método más directo.

> 高斯消元法将 Ax = b 转化为上三角系统 Ux = c,然后通过回代法求解――这是最直接的方法――

El algoritmo:

```
1. For each column k (the pivot column):
   a. Find the largest entry in column k at or below row k (partial pivoting).
   b. Swap that row with row k.
   c. For each row i below k:
      - Compute multiplier m = A[i][k] / A[k][k]
      - Subtract m times row k from row i.
2. Back substitute: solve from the last equation upward.
```

Ejemplo:

```
Original:
| 2  1  1 | 8 |       R2 = R2 - (2)R1     | 2  1   1 |  8 |
| 4  3  3 |20 |  -->  R3 = R3 - (1)R1 --> | 0  1   1 |  4 |
| 2  3  1 |12 |                            | 0  2   0 |  4 |

                       R3 = R3 - (2)R2     | 2  1   1 |  8 |
                                       --> | 0  1   1 |  4 |
                                           | 0  0  -2 | -4 |

Back substitute:
  -2 * x3 = -4    -->  x3 = 2
  x2 + 2  = 4     -->  x2 = 2
  2*x1 + 2 + 2 = 8 --> x1 = 2
```

La eliminación de Gaussian cuesta operaciones O ((n^3). para un sistema 1000x1000, eso es aproximadamente mil millones de operaciones de puntos flotantes.

> La cantidad de cálculo de la ley de los valores de valor es de O (n^3) ⋅ para sistemas de 1000x1000, aproximadamente se necesita un billón de veces de cálculo de puntos de cálculo ⋅ muy rápido, pero si se necesita resolver varios sistemas para el mismo A, hay mejores métodos ⋅

> **【中文解读】**
> La idea de la ley de los valores es muy simple: a través de una línea de cambios, la matriz se transforma en un formato de tres esquinas, y luego desde la última línea de "reciencia" se busca una solución.

### La rotación parcial: por qué importa

Sin pivotar, la eliminación gaussiana puede fallar o producir basura. Si un elemento pivot es cero, se divide por cero. Si es pequeño, se amplifican los errores de redondeo.

>  sin la principal moneda, la ley de los altos consumos puede fracasar o producir resultados basura Si la principal moneda es cero, se dividirá en cero Si la principal moneda es pequeña, se ampliará el error

```
Bad pivot:                       With partial pivoting:
| 0.001  1 | 1.001 |            Swap rows first:
| 1      1 | 2     |            | 1      1 | 2     |
                                 | 0.001  1 | 1.001 |
m = 1/0.001 = 1000              m = 0.001/1 = 0.001
R2 = R2 - 1000*R1               R2 = R2 - 0.001*R1
| 0.001  1     | 1.001   |      | 1      1     | 2     |
| 0     -999   | -999.0  |      | 0      0.999 | 0.999 |

x2 = 1.000 (correct)            x2 = 1.000 (correct)
x1 = (1.001 - 1)/0.001          x1 = (2 - 1)/1 = 1.000 (correct)
   = 0.001/0.001 = 1.000        Stable because the multiplier is small.
```

En la aritmética de puntos flotantes con precisión limitada, la versión sin pivot puede perder cifras significativas.

> En el cálculo de puntos de flotación de precisión limitada, la versión sin factor principal puede perder un número válido.

### Descomposición de las LU

La matriz de descomposición de LU A en una matriz triangular inferior L y una matriz triangular superior U: A = LU. La matriz L almacena los multiplicadores de la eliminación de Gaussian.

> LU 分解将 A 分解为一个下三角矩阵 L 和一个上三角矩阵 U:A = LU。L 矩阵存储高斯消元中的乘数──U 矩阵是消元的结果──

```
A = L @ U

| 2  1  1 |   | 1  0  0 |   | 2  1   1 |
| 4  3  3 | = | 2  1  0 | @ | 0  1   1 |
| 2  3  1 |   | 1  2  1 |   | 0  0  -2 |
```

¿Por qué factor en lugar de simplemente eliminar? Porque una vez que tienes L y U, resolver Ax = b para cualquier nueva b cuesta sólo O ((n^2):

> ¿Por qué se descompone y no se descompone directamente? Porque una vez que se tiene L y U, para cualquier nuevo b se necesita solucionar Ax = b sólo O (n^2):

```
Ax = b
LUx = b
Let y = Ux:
  Ly = b    (forward substitution, O(n^2))
  Ux = y    (back substitution, O(n^2))
```

El costo de O ((n^3) se paga una vez durante la factorization. cada solución posterior es O ((n^2). Si necesitas resolver 1000 sistemas con los mismos A pero diferentes b vectores, LU ahorra un factor de 1000/3 en el trabajo total.

> Si se necesita un mismo A pero diferente b para un sistema de 1000, se ahorrará 1000/3 veces en el total de trabajo.

Con la pivoting parcial, obtienes PA = LU donde P es una matriz de permutación que registra los swaps de fila.

> Utiliza parte principal de la matriz de sustitución, obtenida PA = LU, de la cual P es la matriz de sustitución de la matriz de permutation)

> **【拓展：LU 分解在大规模科学计算中的角色】**
> En el análisis de la estructura física, la rigidez de la matriz es generalmente de millones de fases raras. SuperLU y MUMPS se dividen en sistemas de resolución de problemas.

### Descomposición de las QR

Los factores de descomposición QR A en una matriz ortogonal Q y una matriz triangular superior R: A = QR.

> QR 分解将 A 分解为一个正交矩阵(Matriz ortogonal) Q 和一个上三角矩阵 R:A = QR。

Una matriz ortogonal tiene la propiedad Q^T Q = I. Sus columnas son vectores ortónormales.

> La línea de equilibrio tiene una naturaleza Q^T Q = I. Suele ser el estándar de equilibrio.

```
A = Q @ R

Q has orthonormal columns: Q^T Q = I
R is upper triangular

To solve Ax = b:
  QRx = b
  Rx = Q^T b    (just multiply by Q^T, no inversion needed)
  Back substitute to get x.
```

QR es numéricamente más estable que LU para resolver problemas de mínimos cuadrados.

> QR en la búsqueda de resolver el problema mínimo de la segunda multiplicidad en el tiempo de la cantidad de valores en comparación con LU más estable.

```
Given columns a1, a2, ... of A:

q1 = a1 / ||a1||

q2 = a2 - (a2 . q1) * q1        (subtract projection onto q1)
q2 = q2 / ||q2||                (normalize)

q3 = a3 - (a3 . q1) * q1 - (a3 . q2) * q2
q3 = q3 / ||q3||

R[i][j] = qi . aj    for i <= j
```

Cada paso elimina el componente a lo largo de todos los vectores q anteriores, dejando sólo la nueva dirección ortogonala.

> Cada paso se mueve a lo largo de todas las direcciones anteriores, sólo se deja una nueva dirección correcta.

### Descomposición de Cholesky

Cuando A es simétrico (A = A^T) y positivo definido (todos los valores propios positivos), se puede factorizar como A = L L^T donde L es triangular inferior. Esta es la descomposición de Cholesky.

> Cuando A es对称的(A = A^T)且正定(todos los rasgos son valores正), puedes desglosarlos en A = L L^T, de los cuales L es la rectangular de la rectangular de la cuenca.

```
A = L @ L^T

| 4  2 |   | 2  0 |   | 2  1 |
| 2  5 | = | 1  2 | @ | 0  2 |

L[i][i] = sqrt(A[i][i] - sum(L[i][k]^2 for k < i))
L[i][j] = (A[i][j] - sum(L[i][k]*L[j][k] for k < j)) / L[j][j]    for i > j
```

Cholesky es dos veces más rápido que LU y requiere la mitad del almacenamiento.

> Cholesky es casi dos veces más grande que LU, sólo necesita la mitad del espacio de almacenamiento.

- Las matrices de covarianza son semidefinidas positivas simétricas (definidas positivas con regularización).
  协方差矩阵是对称半正定的 (加正则化后正定)
- La matriz del núcleo en los procesos de Gaussian es simétrica positiva definida.
  La matriz nuclear en el proceso de elevación es la correcta.
- El Hessiano de una función convexa en un mínimo es simétrico positivo definido.
  La función de la rectangular de Hessian 矩阵 es la de la rectangular de la rectangular de la rectangular de la rectangular de la rectangular de la rectangular de la rectangular de la rectangular de la rectangular de la rectangular de la rectangular de la rectangular de la rectangular de la rectangular de la rectangular de la rectangular de la rectangular de la rectangular de la rectangular de la rectangular de la rectangular de la rectangular de la rectangular de la rectangular de la rectangular de la rectangular de la rectangular de la rectangular de la rectangular de la rectangular de la rectangular de la rectangular de la rectangular de la rectangular de la rectangular de la rectangular de la rectangular de la rectangular de la rectangular de la rectangular de la rectangular de la rectangular de la rectangular de la rectangular de la rectangular de la rectangular de la rectangular de la rectangular de la rectangular de la rectangular de la rectangular de la rectangular de la rectangular de la rectangular.
- A^T A es siempre semidefinido positivo simétrico.
  A^T A 总是对称半正确的──

En los procesos de Gaussian, se hace la matriz del núcleo K con Cholesky, luego se resuelve K alfa = y para obtener la media predictiva. El factor Cholesky también le da el determinante de registro para la probabilidad marginal: log det(K) = 2 * suma(log(diag(L))).

> En el proceso de elevación, se utiliza Cholesky para resolver la matriz K, y luego se busca la solución K alfa = y  obtener el valor promedio de pronóstico.

> **【中文解读】**
> Cholesky 分解是 LU 分解的" especial ventaja" sólo se aplica a la llamada矩阵正定, pero la velocidad es dos veces la de LU. La buena noticia es que en ML todos los tipos de matrices正定:协方差矩阵、核矩阵、X^T X、Hessian 矩阵──GPTQ etc.

### Cuadrados mínimos: cuando Ax = b no tiene solución exacta

Si A es m x n con m > n (más ecuaciones que desconocidas), el sistema está sobredeterminado. No hay solución exacta.

> Si A es m x n y m > n (n) el número de cuadrados es más que desconocido), el sistema es super determinado (Overdeterminado) (No hay una solución precisa).

```
minimize ||Ax - b||^2

This is the sum of squared residuals:
  sum((A[i,:] @ x - b[i])^2 for i in range(m))
```

El minimizador satisface las ecuaciones normales:

```
A^T A x = A^T b
```

Derivación: expandirex - b b b b b b b b 2 = (Ax - b) ^ T (Ax - b) = x^T A^T A x - 2 x^T A^T b + b^T b. Tomar el gradiente con respecto a x, establecerlo a cero: 2 A^T A x - 2 A^T b = 0.

> 推导:展开Axarx - b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b

```
Original system (overdetermined, 4 equations, 2 unknowns):
| 1  1 |         | 3 |
| 1  2 | x     = | 5 |       No exact x satisfies all 4 equations.
| 1  3 |         | 6 |
| 1  4 |         | 8 |

Normal equations:
A^T A = | 4  10 |    A^T b = | 22 |
        | 10 30 |            | 63 |

Solve: x = [1.5, 1.7]

This is linear regression. x[0] is the intercept, x[1] is the slope.
```

### Equaciones normales = regresión lineal

La conexión es exacta. En regresión lineal, su matriz de datos X tiene una fila por muestra y una columna por característica. Su vector objetivo y tiene una entrada por muestra. El vector de peso w satisface:

> Esta relación es precisa. En la retracción en línea, la matriz de datos X cada línea de un modelo, cada línea de un rasgo, cada tipo de un rasgo, cada tipo de un modelo y cada tipo de un artículo, cada tipo de un modelo, cada tipo de un tipo de un tipo de un tipo de un tipo de un tipo de un tipo de un tipo de un tipo de un tipo de un tipo de un tipo de un tipo de un tipo de un tipo de un tipo de un tipo de un tipo de un tipo de un tipo de un tipo de un tipo de un tipo de un tipo de un tipo de un tipo de un tipo de un tipo de un tipo de un tipo de tipo de un tipo de un tipo de tipo de un tipo de tipo de un tipo de tipo de un tipo de tipo de un tipo de tipo de tipo de un tipo de tipo de tipo de un tipo de tipo de tipo de tipo de un tipo de tipo de tipo de tipo de tipo de un tipo de tipo de tipo de tipo de tipo de tipo de un tipo de tipo de tipo de tipo de tipo de tipo de tipo de tipo de un tipo de tipo de tipo de tipo de tipo de tipo de tipo de tipo de tipo de tipo de tipo de tipo de tipo de tipo de tipo de tipo de tipo de tipo de tipo de tipo de tipo de tipo de tipo de tipo de tipo de tipo de tipo de tipo de tipo de tipo de tipo de tipo de tipo de tipo de tipo de tipo de tipo de tipo de tipo de tipo de tipo de tipo de tipo de tipo de tipo de tipo de tipo de tipo de tipo de tipo de tipo de tipo de tipo de tipo de tipo de tipo de tipo de tipo de tipo de tipo de tipo de tipo de tipo de tipo de tipo de tipo de tipo de tipo de tipo de tipo de tipo de tipo de tipo de tipo de tipo de tipo de tipo de tipo de tipo de tipo de tipo de tipo de tipo de tipo de tipo de tipo de tipo de tipo de tipo de tipo de tipo de tipo de tipo de tipo de tipo de tipo de tipo de tipo de tipo de tipo de tipo de tipo de tipo de tipo de tipo de tipo de tipo de tipo de tipo de tipo de tipo de tipo de tipo de tipo de tipo de tipo de tipo de tipo de tipo de tipo de tipo de tipo de tipo de tipo de tipo de tipo de tipo de tipo de tipo de tipo de tipo de tipo de tipo de tipo de tipo de tipo de tipo

```
X^T X w = X^T y
w = (X^T X)^(-1) X^T y
```

Esta es la solución de forma cerrada a la regresión lineal.`sklearn.linear_model.LinearRegression.fit()`calcula esto (o un equivalente a través de QR o SVD).

> Es la solución de la regresión.`sklearn.linear_model.LinearRegression.fit()`Todo esto se calcula en forma de QR o SVD.

Agregue un término de regularización lambda * I a la matriz y obtendrá regresión de cresta:

> En la rectangularidad añadido el programa de reglamentación lambda * I get  regreso  Ridge Regression):

```
(X^T X + lambda * I) w = X^T y
w = (X^T X + lambda * I)^(-1) X^T y
```

La regularización hace que la matriz esté mejor condicionada (más fácil de invertir con precisión) y evita el sobreajuste reduciendo los pesos hacia cero. La matriz X^T X + lambda * I es siempre positiva simétrica definida cuando lambda > 0, por lo que se puede usar Cholesky para resolverla.

> Cuando la lógica de la lógica de la lógica de la lógica de la lógica de la lógica de la lógica de la lógica de la lógica de la lógica de la lógica de la lógica de la lógica de la lógica de la lógica de la lógica de la lógica de la lógica de la lógica de la lógica de la lógica de la lógica de la lógica de la lógica de la lógica de la lógica de la lógica de la lógica de la lógica de la lógica de la lógica de la lógica de la lógica de la lógica de la lógica de la lógica de la lógica de la lógica de la lógica de la lógica de la lógica de la lógica de la lógica de la lógica de lógica de lógica de lógica de lógica de lógica de lógica de lógica de lógica de lógica de lógica de lógica de lógica de lógica de lógica de lógica de lógica de lógica de lógica de lógica de lógica de lógica de lógica de lógica de lógica de lógica de lógica de lógica de lógica de lógica de lógica de lógica de lógica de lógica de lógica de lógica de lógica de lógica de lógica de lógica de lógica de lógica de lógica de lógica de lógica de lógica de lógica de lógica de lógica de lógica de lógica de lógica de lógica de lógica de lógica de lógica de lógica de lógica de lógica de lógica de lógica de lógica de lógica de lógica de lógica de lógica de lógica de lógica de lógica de lógica de lógica de lógica de lógica de lógica de lógica de lógica de lógica de lógica de lógica de lógica de lógica de lógica de lógica de lógica de lógica de lógica de lógica de lógica de lógica de lógica de lógica de lógica de lógica de lógica de lógica de lógica de lógica de lógica de lógica de lógica de lógica de lógica de lógica de lógica de lógica de lógica de lógica de lógica de lógica de lógica de lógica de lógica de

> **【拓展：条件数与深度学习训练稳定性】**
> El problema de la escala explosión/desaparición en el entrenamiento del transformador está estrechamente relacionado con el número de condiciones. La relación entre residuos y la regeneración de niveles es que la norma de las capas mejora la cantidad de condiciones de cada nivel.

### Pseudoinverso (Moore-Penrose)

El pseudoinverso A+ generaliza la inversión de la matriz a matrices no cuadradas y singulares.

> 伪逆(Pseudoinverse) A+ 将矩阵求逆推广到非方阵和奇异矩阵── para cualquier矩阵 A:

```
x = A+ b

where A+ = V Sigma+ U^T    (computed via SVD)
```

Sigma+ se forma tomando la recíproca de cada valor singular no cero y transponendo el resultado.

> Sigma+ por cada valor diferente que no es un valor de un número de sigma y se transforma en un número de sigma. Si A = U Sigma V^T, entonces A+ = V Sigma+ U^T。

```
A = U Sigma V^T        (SVD)

Sigma = | 5  0 |       Sigma+ = | 1/5  0  0 |
        | 0  2 |                | 0  1/2  0 |
        | 0  0 |

A+ = V Sigma+ U^T
```

El pseudoinverso da la solución de mínimos mínimos cuadrados normales.
- Una solución: A + b lo da.
  Una solución: A+ b                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        
- Ninguna solución: A + b da la solución de cuadrados mínimos.
  无解:A+b 给出最小二乘解──
- Soluciones infinitas: A+ b da a la que tiene el menor número de puntos.
  无穷多解:A+b 给出范数最小的一个.

NumPy's `np.linalg.lstsq`y `np.linalg.pinv`ambos utilizan el SVD internamente.

> NumPy de `np.linalg.lstsq`Y `np.linalg.pinv`内部都使用 SVD。

### Número de condición

El número de condición mide la sensibilidad de la solución a pequeños cambios en la entrada.

> 条件数(Conditions Number) mide la sensibilidad a los cambios de entrada y de pequeño tamaño.

```
kappa(A) = ||A|| * ||A^(-1)|| = sigma_max / sigma_min
```

donde sigma_max y sigma_min son los valores singulares más grandes y más pequeños.

```
Well-conditioned (kappa ~ 1):        Ill-conditioned (kappa ~ 10^15):
Small change in b -->                Small change in b -->
small change in x                    huge change in x

| 2  0 |   kappa = 2/1 = 2          | 1   1          |   kappa ~ 10^15
| 0  1 |   safe to solve            | 1   1+10^(-15) |   solution is garbage
```

Reglas de los pulgares:
- Kappa < 100: seguro, la solución es precisa.
  Seguridad, la solución es precisa.
- Kappa ~ 10 k: se pierde aproximadamente k dígitos de precisión de su aritmética de puntos flotantes.
  Perderás la precisión de los puntos de vuelo.
- Kappa ~ 10^16 (para float64): la solución no tiene sentido.
  La matriz en realidad es extraña.

En ML, la mala condición ocurre cuando las características son casi colinearias. La regularización (agregando lambda * I) mejora el número de condición de sigma_max / sigma_min a (sigma_max + lambda) / (sigma_min + lambda).

> En el ML, cuando se caracterizan por la proximidad de la línea de trabajo (Collinear) se producen condiciones de enfermedad (Collinear) cuando se producen condiciones de trabajo (Collinear) se producen condiciones de trabajo (Collinear) cuando se producen condiciones de trabajo (Collinear) se producen condiciones de trabajo (Collinear) cuando se producen condiciones de trabajo (Collinear) se producen condiciones de trabajo (Collinear) cuando se producen condiciones de trabajo (Collinear) se producen condiciones de trabajo (Collinear) cuando se producen condiciones de trabajo (Collinear) cuando se producen condiciones de trabajo (Collinear) cuando se producen condiciones de trabajo (Collinear) se producen condiciones de trabajo (Collinear) cuando se producen condiciones de trabajo (Collinear) (Collinear) cuando se producen condiciones (Collinear) (Collinear) (Collinear) (Collinear) (Collinear) (Collinear) (Collinear) (Collinear) (Collinear) (Collinear) (Collinear) (Collinear) (Collinear) (Collinear) (Collinear) (Collinear) (Collinear) (Collinear) (Collinear) (Collinear) (Collinear) (Collinear) (Collinear) (Collinear) (Collinear))) (Collinear) (Collinear) (Collinear) (C) (C) (C))) (C) (C) (C) (C))) (C) (C) (C))))) (C) (C) (C) (C) (C) (C) (C) (C))))))))))))))))))))))))) (C) (C) (C) (C) (C) (C) (C) (C) (C) (C) (C) (C) (C) (C) (C) (C) (C) (C) (C) (C) (

### Métodos iterativos: gradiente conjugado

Para sistemas muy grandes y escasos (millones de desconocidos), los métodos directos como LU o Cholesky son demasiado caros. Los métodos iterativos se acercan a la solución mejorando una suposición en muchas iteraciones.

> Para sistemas muy grandes, los métodos directos son demasiado caros.

El gradiente conjugado (CG) resuelve Ax = b cuando A es simétrico positivo definido. Encuentra la solución exacta en al menos n iteraciones (en aritmética exacta), pero normalmente converge mucho más rápido si los valores propios de A se agrupan.

> 共梯度法 (Conjugate Gradient, CG) en A es un nombre que se denomina a tiempo determinado (A = b。 es el más frecuente en la generación actual en que se puede encontrar una solución precisa (), pero si el valor de las características de A se agrupa, normalmente se recibe más rápido。

```
Algorithm sketch:
  x0 = initial guess (often zero)
  r0 = b - A x0           (residual)
  p0 = r0                 (search direction)

  For k = 0, 1, 2, ...:
    alpha = (rk . rk) / (pk . A pk)
    x_{k+1} = xk + alpha * pk
    r_{k+1} = rk - alpha * A pk
    beta = (r_{k+1} . r_{k+1}) / (rk . rk)
    p_{k+1} = r_{k+1} + beta * pk
    if ||r_{k+1}|| < tolerance: stop
```

CG se utiliza en:
- Optimización a gran escala (método Newton-CG)
  La mayor cantidad de la gente que se encuentra en el área de la ciudad
- Resolución de las discretizas de la EIP
  Solucionar la separación de la diferenciación de la diferenciación
- Métodos del núcleo donde la matriz del núcleo es demasiado grande para factorizar
  Cuadro nuclear demasiado grande para descomponer
- Precondicionamiento para otros solventes iterativos
  其他代求解器的预处理

La tasa de convergencia depende del número de condiciones. Los sistemas mejor condicionados convergen más rápido, lo que es otra razón por la que la regularización ayuda.

>  Rate de recepción depende de la cantidad de condiciones                                                                                                                                                                                                                                                        

> **【中文解读】**
> Comparado con el tiempo, el tiempo es un tiempo de carga de la red de la red nerviosa. En la red nerviosa, el tiempo es un tiempo de carga de la red nerviosa.

### El cuadro completo: qué método cuando

| Method | Requirements | Cost | Use case |
|--------|-------------|------|----------|
| Gaussian elimination | Square, nonsingular A | O(n^3) | One-off solve of a square system |
| LU decomposition | Square, nonsingular A | O(n^3) factor + O(n^2) solve | Multiple solves with the same A |
| QR decomposition | Any A (m >= n) | O(mn^2) | Least squares, numerically stable |
| Cholesky | Symmetric positive definite A | O(n^3/3) | Covariance matrices, Gaussian processes, ridge regression |
| Normal equations | Overdetermined (m > n) | O(mn^2 + n^3) | Linear regression (small n) |
| SVD / pseudoinverse | Any A | O(mn^2) | Rank-deficient systems, minimum-norm solutions |
| Conjugate gradient | Symmetric positive definite, sparse A | O(n * k * nnz) | Large sparse systems, k = iterations |

### Conexión a ML

Cada método de esta lección aparece en ML de producción:

> Cada método de esta clase se encuentra en la producción de ML:

**Linear regression.**La solución de forma cerrada resuelve las ecuaciones normales X^T X w = X^T y. Esto se hace a través de Cholesky (si n es pequeño) o QR (si la estabilidad numérica importa) o SVD (si la matriz podría ser deficiente en rango).

> **线性回归。**解析解求解正规方程 X^T X w = X^T y。通过Cholesky(n 较小时) o QR((需要数值稳定性时) o SVD(矩阵可能不满秩时)完成。

**Ridge regression.**Añade lambda * I a X^T X. El sistema regularizado (X^T X + lambda * I) w = X^T y es siempre soluble a través de Cholesky porque X^T X + lambda * I es simétrico positivo definido para lambda > 0.

> **岭回归。**En X^T X 上加 lambda * I。正则化系统 (X^T X + lambda * I) w = X^T y 总是可以通过Cholesky 求解,因为当 lambda > 0 时 X^T X + lambda * I 是对称正定的。

**Gaussian processes.**La media predictiva requiere resolver K alfa = y donde K es la matriz del núcleo. La factorization de Cholesky de K es el enfoque estándar. La probabilidad marginal de registro utiliza log det(K) = 2 suma(log(diag(L))).

> **高斯过程。**预测 promedio de valor necesita buscar la solución K alfa = y, de los cuales K es la matriz nuclear。Cholesky 分解 K es el método estándar。对数边际似然使用 log det(K) = 2 sumas(log(diag(L)))。

**Neural network initialization.**La inicialización ortogonal utiliza la descomposición QR para crear matrices de peso cuyas columnas son ortónormales. Esto evita el colapso de la señal en redes profundas.

> **神经网络初始化。**Se inicializó el uso de QR para crear una matriz de peso de la norma de interacción. Esto impidió la reducción de los señales en la red profunda.

**Preconditioning.**Los optimizadores a gran escala utilizan Cholesky incompleto o LU incompleto como precondiciones para los solventes de gradientes conjugados.

> **预处理。**Uso de optimizadores de gran escala no completo Cholesky o no completo LU como condición de pre-procesamiento de los sistemas de búsqueda de escalas comunes.

**Feature engineering.**El número de condición de X^T X le dice si sus características son colinearias. Si kappa es grande, deje de caracteres o añada regularización.

> **特征工程。**El número de condiciones de X^T X le dice si el rasgo es común. Si la kappa es grande, elimina el rasgo o añade la normalización.

## Construye y realiza.
```figure
linear-system-conditioning
```

## Construye el mismo

### Paso 1: Eliminación gaussiana con giro parcial

```python
import numpy as np

def gaussian_elimination(A, b):
    n = len(b)
    Ab = np.hstack([A.astype(float), b.reshape(-1, 1).astype(float)])

    for k in range(n):
        max_row = k + np.argmax(np.abs(Ab[k:, k]))  # 部分主元选取：找列中绝对值最大的行
        Ab[[k, max_row]] = Ab[[max_row, k]]           # 交换行使最大元素到主元位置

        if abs(Ab[k, k]) < 1e-12:                     # 检查主元是否接近零（矩阵奇异）
            raise ValueError(f"Matrix is singular or nearly singular at pivot {k}")

        for i in range(k + 1, n):
            m = Ab[i, k] / Ab[k, k]                   # 计算消元乘数
            Ab[i, k:] -= m * Ab[k, k:]                # 消元：将第 k 列第 i 行以下变为零

    x = np.zeros(n)
    for i in range(n - 1, -1, -1):
        x[i] = (Ab[i, -1] - Ab[i, i+1:n] @ x[i+1:n]) / Ab[i, i]  # 回代求解

    return x
```

### Paso 2: Descomposición de la LU

```python
def lu_decompose(A):
    n = A.shape[0]
    L = np.eye(n)
    U = A.astype(float).copy()
    P = np.eye(n)

    for k in range(n):
        max_row = k + np.argmax(np.abs(U[k:, k]))
        if max_row != k:
            U[[k, max_row]] = U[[max_row, k]]
            P[[k, max_row]] = P[[max_row, k]]
            if k > 0:
                L[[k, max_row], :k] = L[[max_row, k], :k]

        for i in range(k + 1, n):
            L[i, k] = U[i, k] / U[k, k]
            U[i, k:] -= L[i, k] * U[k, k:]

    return P, L, U

def lu_solve(P, L, U, b):
    n = len(b)
    Pb = P @ b.astype(float)

    y = np.zeros(n)
    for i in range(n):
        y[i] = Pb[i] - L[i, :i] @ y[:i]

    x = np.zeros(n)
    for i in range(n - 1, -1, -1):
        x[i] = (y[i] - U[i, i+1:] @ x[i+1:]) / U[i, i]

    return x
```

### Paso 3: Descomposición de Cholesky

```python
def cholesky(A):
    n = A.shape[0]
    L = np.zeros_like(A, dtype=float)

    for i in range(n):
        for j in range(i + 1):
            s = A[i, j] - L[i, :j] @ L[j, :j]       # 减去已计算部分的贡献
            if i == j:
                if s <= 0:                             # 对角线元素必须为正（正定条件）
                    raise ValueError("Matrix is not positive definite")
                L[i, j] = np.sqrt(s)                  # 对角线元素 = sqrt(剩余值)
            else:
                L[i, j] = s / L[j, j]                 # 非对角线元素除以对应对角线值

    return L
```

### Paso 4: Cuadrados mínimos a través de ecuaciones normales

```python
def least_squares_normal(A, b):
    AtA = A.T @ A
    Atb = A.T @ b
    return gaussian_elimination(AtA, Atb)

def ridge_regression(A, b, lam):
    n = A.shape[1]
    AtA = A.T @ A + lam * np.eye(n)
    Atb = A.T @ b
    L = cholesky(AtA)
    y = np.zeros(n)
    for i in range(n):
        y[i] = (Atb[i] - L[i, :i] @ y[:i]) / L[i, i]
    x = np.zeros(n)
    for i in range(n - 1, -1, -1):
        x[i] = (y[i] - L.T[i, i+1:] @ x[i+1:]) / L.T[i, i]
    return x
```

### Paso 5: Número de condición

```python
def condition_number(A):
    U, S, Vt = np.linalg.svd(A)
    return S[0] / S[-1]
```

## Usalo con el marco de ejecución

Colocando las piezas juntas para la regresión lineal y la regresión de la cresta en datos reales:

> Para combinar estas partes, realizar una regresión y una regresión en datos reales:

```python
np.random.seed(42)
X_raw = np.random.randn(100, 3)
w_true = np.array([2.0, -1.0, 0.5])
y = X_raw @ w_true + np.random.randn(100) * 0.1

X = np.column_stack([np.ones(100), X_raw])

w_ols = least_squares_normal(X, y)
print(f"OLS weights (ours):    {w_ols}")

w_np = np.linalg.lstsq(X, y, rcond=None)[0]
print(f"OLS weights (numpy):   {w_np}")
print(f"Max difference: {np.max(np.abs(w_ols - w_np)):.2e}")

w_ridge = ridge_regression(X, y, lam=1.0)
print(f"Ridge weights (ours):  {w_ridge}")

from sklearn.linear_model import Ridge
ridge_sk = Ridge(alpha=1.0, fit_intercept=False)
ridge_sk.fit(X, y)
print(f"Ridge weights (sklearn): {ridge_sk.coef_}")
```

## Envíe el producto .

Esta lección produce:
- `code/linear_systems.py`que contiene implementaciones desde cero de la eliminación de Gaussian, la descomposición de LU, la descomposición de Cholesky, los mínimos cuadrados y la regresión de la cresta
  包含高斯消元法、LU 分解、Cholesky 分解、最小二乘法和回归的从零实现
- Una demostración de trabajo de que las ecuaciones normales y la Regressión Lineal de sklearn producen los mismos pesos
  Regressión lineal de la forma y el método de cálculo

## Los ejercicios.

1. Resolver el sistema `[[1,2,3],[4,5,6],[7,8,10]] x = [6, 15, 27]`usando su eliminación Gaussian, su solvente de LU, y `np.linalg.solve`Verifique que los tres dan la misma respuesta dentro de la tolerancia de puntos flotantes.

2. Generar una matriz aleatoria 50x5 X y objetivo y = X @ w_true + ruido. Resolver para w utilizando ecuaciones normales, QR (via `np.linalg.qr`), SVD (a través de `np.linalg.svd`), y `np.linalg.lstsq`Comparar las cuatro soluciones. Medir el número de condición de X^T X y explicar cómo afecta a qué método confía.

3. Crea una matriz casi singular haciendo que dos columnas sean casi idénticas (por ejemplo, columna 2 = columna 1 + 1e-10 * ruido).

4. Implemente el algoritmo de gradiente conjugado para una matriz definida positiva simétrica aleatoria 100x100. Cuente cuántas iteraciones se necesitan para converger a la tolerancia 1e-8.

5. Tiempo de su solvente Cholesky vs su solvente LU vs `np.linalg.solve`En las matrices definidas positivas simétricas de tamaño 10, 50, 200, 500.

## Términos clave .

| Term | What people say | What it actually means |
|------|----------------|----------------------|
| Linear system | "Solve for x" | A set of linear equations Ax = b. Finding x means finding the input that produces output b under transformation A. |
| Gaussian elimination | "Row reduce" | Systematically zero out entries below the diagonal using row operations, producing an upper triangular system solvable by back substitution. O(n^3). |
| Partial pivoting | "Swap rows for stability" | Before eliminating in column k, swap the row with the largest absolute value in that column to the pivot position. Prevents division by small numbers. |
| LU decomposition | "Factor into triangles" | Write A = LU where L is lower triangular (stores multipliers) and U is upper triangular (the eliminated matrix). Amortizes the O(n^3) cost over multiple solves. |
| QR decomposition | "Orthogonal factorization" | Write A = QR where Q has orthonormal columns and R is upper triangular. More stable than LU for least squares. |
| Cholesky decomposition | "Square root of a matrix" | For symmetric positive definite A, write A = LL^T. Half the cost of LU. Used for covariance matrices, kernel matrices, and ridge regression. |
| Least squares | "Best fit when exact is impossible" | Minimize the sum of squared residuals ||Ax - b||^2 when the system is overdetermined (more equations than unknowns). |
| Normal equations | "The calculus shortcut" | A^T A x = A^T b. Setting the gradient of ||Ax - b||^2 to zero. This IS the closed-form solution to linear regression. |
| Pseudoinverse | "Inversion for non-square matrices" | A+ = V Sigma+ U^T via SVD. Gives the minimum-norm least-squares solution for any matrix, square or rectangular, singular or not. |
| Condition number | "How trustworthy is this answer" | kappa = sigma_max / sigma_min. Measures sensitivity to input perturbations. Lose about log10(kappa) digits of precision. |
| Ridge regression | "Regularized least squares" | Solve (X^T X + lambda I) w = X^T y. Adding lambda I improves conditioning and shrinks weights toward zero. Prevents overfitting. |
| Conjugate gradient | "Iterative Ax=b for big matrices" | An iterative solver for symmetric positive definite systems. Converges in at most n steps. Practical for large sparse systems where factorization is too expensive. |
| Overdetermined system | "More data than parameters" | m > n in an m-by-n system. No exact solution exists. Least squares finds the best approximation. This is every regression problem. |
| Back substitution | "Solve from the bottom up" | Given an upper triangular system, solve the last equation first, then substitute backward. O(n^2). |
| Forward substitution | "Solve from the top down" | Given a lower triangular system, solve the first equation first, then substitute forward. O(n^2). Used in the L step of LU solves. |

## Más Leer más Leer más

- [MIT 18.06: Linear Algebra](https://ocw.mit.edu/courses/18-06-linear-algebra-spring-2010/)(Gilbert Strang) -- el curso definitivo sobre sistemas lineales y factorizations de matriz
- [Numerical Linear Algebra](https://people.maths.ox.ac.uk/trefethen/text.html)(Trefethen & Bau) -- la referencia estándar para entender la estabilidad numérica, el condicionamiento, y por qué los algoritmos fallan
- [Matrix Computations](https://www.cs.cornell.edu/cv/GolubVanLoan4/golubandvanloan.htm)(Golub & Van Loan) -- la referencia enciclopédica para cada algoritmo de matriz
- [3Blue1Brown: Inverse Matrices](https://www.3blue1brown.com/lessons/inverse-matrices)-- intuición visual para lo que resolver Ax = b significa geométricamente
