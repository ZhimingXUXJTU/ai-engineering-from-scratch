# Probabilidad y distribución  概率 y distribución

> La probabilidad es el lenguaje que utiliza la IA para expresar la incertidumbre.
> 概率 es el lenguaje de la IA de la expresión de la incertidumbre.

**Type:** Learn | **类型:** 学习
**Language:**¿ Qué pasa ?**语言:**Python
**Prerequisites:** Phase 1, Lessons 01-04 | **前置知识:** Phase 1, Lessons 01-04
**Time:** ~75 minutes | **时间:** ~75 分钟

## Objetivos de aprendizaje

- Implementar los PMF y los PDF desde cero para las distribuciones Bernoulli, categórica, Poisson, uniforme y normal
- Computa el valor esperado, la varianza y usa el Teorema del límite central para explicar por qué los gaussianos dominan
- Construir las funciones softmax y log-softmax con el truco de estabilidad numérica (sustraer logit máximo)
- Calcular la pérdida de entropía cruzada de logits y conectarla a la probabilidad de log negativo

> **【中文解读】**
> 概率 es una IA que expresa lenguaje incierto. 分类器输出概率分布, lenguaje modelo de 50.000 palabras candidatas según probabilidad de la muestra, modelo de propagación de la distribución de la generación de imágenes de la aprendizaje a la distribución.

> **【拓展：概率在 AI 中的位置】**
> - **Softmax**: Convertir la salida de la red neuronal en distribución de probabilidad es el último paso de todos los modelos de categorías.
> - **交叉熵损失**Función de pérdida estándar de las tareas, igual a negativo en número similar.
> - **高斯分布**: Enfoque en la comprensión de por qué el alto está tan comúnmente distribuido entre la naturaleza y la IA.

## El problema es la introducción del problema

> **【中文解读】**                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             `[0.03, 0.91, 0.06]`El modelo de lenguaje se escoge de entre 50.000 palabras candidatas, el modelo de propagación se genera de la distribución de las imágenes aprendidas.

## El concepto central.

> **【拓展：概率分布是 AI 生成模型的基础】**El núcleo de los modelos de producción (VAE, GAN, expansión) es la distribución de probabilidades: aprender a una distribución de datos p (x), luego generar nuevos datos de la muestra.

Cada predicción que hace un modelo es una distribución de probabilidades. Cada función de pérdida mide cuán lejos está la distribución prevista de la verdadera. Cada paso de entrenamiento ajusta los parámetros para que una distribución se vea más parecida a otra. Sin probabilidad, no puedes leer un solo documento de ML, deshacerte de un solo modelo o entender por qué tu pérdida de entrenamiento es NaN.

>  Cada predicción del modelo es una distribución de probabilidad Cada función de pérdida mide la diferencia entre la distribución de probabilidad y la distribución real Cada paso de entrenamiento está en el parámetro de ajuste para que una distribución se acerque más a la otra  No entiendo la probabilidad, no puedes leer el artículo  Modificar el modelo o entender por qué la pérdida de entrenamiento es NaN

## El concepto central.

### Eventos, espacios de muestra y probabilidad

El espacio de muestra S es el conjunto de todos los resultados posibles. Un evento es un subconjunto del espacio de muestra.

> 样本空间 S es el conjunto de todos los posibles resultados. Eventos son subconjuntos del espacio de muestra.

```
Coin flip:
  S = {H, T}
  P(H) = 0.5,  P(T) = 0.5

Single die roll:
  S = {1, 2, 3, 4, 5, 6}
  P(even) = P({2, 4, 6}) = 3/6 = 0.5
```

Tres axiomas definen toda la probabilidad:
1. P(A) >= 0 para cualquier evento A
2. P(S) = 1 (algo siempre sucede)
3. P(A o B) = P(A) + P(B) cuando A y B no pueden ocurrir ambas

> 概率论由三条公理定义:
> 1. 对于任意事件 A,P(A) >= 0
> 2. P (S) = 1 (necesariamente habrá algún tipo de resultado)
> 3. Cuando A y B no pueden ocurrir simultáneamente, P(A o B) = P(A) + P(B)

Todo lo demás (teorema de Bayes, expectativas, distribuciones) se sigue de estas tres reglas.

> Todo lo demás se deriva de estas tres reglas.

### Probabilidad condicional y independencia

P ((A) B) es la probabilidad de A dada que B sucedió.

> P                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             

```
P(A|B) = P(A and B) / P(B)

Example: deck of cards
  P(King | Face card) = P(King and Face card) / P(Face card)
                      = (4/52) / (12/52)
                      = 4/12 = 1/3
```

Dos eventos son independientes cuando saber uno no te dice nada del otro:

> Dos eventos independientes significa saber que uno de ellos no te dirá nada sobre el otro:

```
Independent:   P(A|B) = P(A)
Equivalent to: P(A and B) = P(A) * P(B)
```

Los tiros de monedas son independientes, pero los tiros sin reemplazo no lo son.

> La moneda es independiente.

### Funciones de masa de probabilidad vs. funciones de densidad de probabilidad

Las variables aleatorias discretas tienen una función de masa de probabilidad (PMF). Cada resultado tiene una probabilidad específica que se puede leer directamente.

> 离散随机变量有概率质量函数 (PMF) ⋅ cada resultado tiene una probabilidad específica que se puede leer directamente ⋅

```
PMF: P(X = k)

Fair die:
  P(X = 1) = 1/6
  P(X = 2) = 1/6
  ...
  P(X = 6) = 1/6

  Sum of all probabilities = 1
```

Las variables aleatorias continuas tienen una función de densidad de probabilidad (PDF). La densidad en un solo punto no es una probabilidad.

> 连续随机变量有概率密度函数 (PDF) ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅                                                                                                                                                                                                                              

```
PDF: f(x)

P(a <= X <= b) = integral of f(x) from a to b

f(x) can be greater than 1 (density, not probability)
integral from -inf to +inf of f(x) dx = 1
```

Esta distinción es importante en ML. Las salidas de clasificación son PMF (elecciones discretas).

> Esta diferencia en ML es muy importante.

### Distribuciones comunes

**Bernoulli:**Un ensayo, dos resultados.

> **伯努利分布：**Una prueba, dos resultados.

```
P(X = 1) = p
P(X = 0) = 1 - p
Mean = p,  Variance = p(1-p)
```

**Categorical:**Los modelos de clasificación de clases múltiples (salida de la máxima suavidad).

> **分类分布：**Una vez que se realizó el ensayo, se produjo un gran número de problemas.

```
P(X = i) = p_i,  where sum of p_i = 1
Example: P(cat) = 0.7,  P(dog) = 0.2,  P(bird) = 0.1
```

**Uniform:**Todos los resultados son igualmente probables.

> **均匀分布：**Todos los resultados y probabilidades aparecen.

```
Discrete: P(X = k) = 1/n for k in {1, ..., n}
Continuous: f(x) = 1/(b-a) for x in [a, b]
```

**Normal (Gaussian):**La curva de la campana. Parameterizada por medio (mu) y varianza (sigma^2).

> **正态（高斯）分布：**钟形曲线──由均值 (mu) 和方差 (sigma^2) 参数化──

```
f(x) = (1 / sqrt(2*pi*sigma^2)) * exp(-(x - mu)^2 / (2*sigma^2))

Standard normal: mu = 0, sigma = 1
  68% of data within 1 sigma
  95% within 2 sigma
  99.7% within 3 sigma
```

**Poisson:**El número de eventos raros en un intervalo fijo.

> **泊松分布：**Cuenta de eventos raros en zonas fijas                                                                                                                                                                                                                                                          

```
P(X = k) = (lambda^k * e^(-lambda)) / k!
Mean = lambda,  Variance = lambda
```

### Valor esperado y variación

El valor esperado es el resultado medio ponderado.

> El valor esperado es el resultado medio de la adición.

```
Discrete:   E[X] = sum of x_i * P(X = x_i)
Continuous: E[X] = integral of x * f(x) dx
```

Las medidas de variación se extienden alrededor de la media.

> 方差 mide el grado de dispersión del valor medio en torno a la misma.

```
Var(X) = E[(X - E[X])^2] = E[X^2] - (E[X])^2
Standard deviation = sqrt(Var(X))
```

En ML, el valor esperado aparece como la función de pérdida (pérdida promedio sobre la distribución de datos).

> En ML, el valor esperado se muestra como la función de pérdida (la pérdida media en la distribución de datos), el diferencial le dice la estabilidad del modelo.

### Distribuciones conjuntas y marginales

Una distribución conjunta P ((X, Y) describe dos variables aleatorias juntas.

> 联合分布 P(X, Y)                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                     

Ejemplo de PMF conjunta (X = clima, Y = paraguas):
联合 PMF示例(X = 天气,Y = 是否带):

| | Y=0 (no umbrella / 不带伞) | Y=1 (umbrella / 带伞) | Marginal P(X) / 边缘 P(X) |
|---|---|---|---|
| X=0 (sun / 晴天) | 0.40 | 0.10 | P(X=0) = 0.50 |
| X=1 (rain / 下雨) | 0.05 | 0.45 | P(X=1) = 0.50 |
| **Marginal P(Y) / 边缘 P(Y)** | P(Y=0) = 0.45 | P(Y=1) = 0.55 | 1.00 |

La distribución marginal suma la otra variable:

> 边缘分布通过对另一个变量求和得到:

```
P(X = x) = sum over all y of P(X = x, Y = y)
```

Los totales de filas y columnas de la tabla anterior son los márgenes.

> La distribución de las líneas y las líneas de la tabla anterior es la distribución de las líneas de la tabla anterior.

### Por qué la distribución normal aparece en todas partes

El Teorema del límite central: la suma (o promedio) de muchas variables aleatorias independientes converge a una distribución normal, independientemente de la distribución original.

> La distribución de los valores de los valores de los valores de los valores de los valores de los valores de los valores de los valores de los valores de los valores de los valores de los valores de los valores de los valores de los valores de los valores de los valores de los valores de los valores de los valores de los valores de los valores de los valores de los valores de los valores de los valores de los valores de los valores de los valores de los valores de los valores de los valores de los valores de los valores de los valores de los valores de los valores de los valores de los valores de los valores de los valores de los valores de los valores de los valores de los valores de los valores de los valores de los valores de los valores de los valores de los valores de los valores de los valores de los valores de los valores de los valores de los valores de los valores de los valores de los valores de los valores de los valores de los valores de los valores de los valores de los valores de los valores de los valores de los valores de los valores de los valores de los valores de los valores de los valores de los valores de los valores de los valores de los valores de los valores de los valores de los valores de los valores de los valores de los valores de los valores de los valores de los valores de los valores de los valores de los valores de los valores de los valores de los valores de los valores de los valores de los valores de los valores de la cuyo de los valores de los valores de los valores de los valores de los valores de la cuyo de los valores de los valores de los valores de los valores de la cuyo de los valores de los valores de la cuento de los valores de los valores de los valores de los valores de la cuento de la cuento de los valores de la cuento de los valores de la cuento de la cuento de la cuento de la cuento de la cuento de la cuento de la cuento de la cuento de la cuento de la cuento de la cuento de la cuento de la cuento de la cuento de la cuento de la cuento de la cuento de la cuento de la cuento de la cuento de la cuento de la cuento de la cuento de la cuento de la cuento de la cuento de la cuento de la cuento de la cuento de la cuenta de la cuenta de la cuenta de la cuenta de la cuenta de la

```
Roll 1 die:  uniform distribution (flat)
Average of 2 dice:  triangular (peaked)
Average of 30 dice: nearly perfect bell curve

This works for ANY starting distribution.
```

Por eso es que:
- Los errores de medición son aproximadamente normales (muchas pequeñas fuentes independientes)
  Traducción:Mejora de error casi como normal (por muchos pequeños)
- Las inicializaciones de peso en las redes neuronales utilizan distribuciones normales
  Traducción:El peso de la red de los cuerpos de los cuerpos de los cuerpos de los cuerpos de los cuerpos de los cuerpos de los cuerpos de los cuerpos de los cuerpos de los cuerpos de los cuerpos de los cuerpos de los cuerpos de los cuerpos de los cuerpos de los cuerpos de los cuerpos de los cuerpos de los cuerpos de los cuerpos de los cuerpos de los cuerpos de los cuerpos de los cuerpos de los cuerpos de los cuerpos de los cuerpos de los cuerpos de los cuerpos de los cuerpos de los cuerpos de los cuerpos de los cuerpos de los cuerpos de los cuerpos de los cuerpos de los cuerpos de los cuerpos de los cuerpos de los cuerpos de los cuerpos de los cuerpos de los cuerpos de los cuerpos de los cuerpos de los cuerpos de los cuerpos de los cuerpos de los cuerpos de los cuerpos de los cuerpos de los cuerpos de los cuerpos de los cuerpos de los cuerpos de los cuerpos de los cuerpos de los cuerpos de los cuerpos de los cuerpos de los cuerpos de los cuerpos de los cuerpos de los cuerpos de los cuerpos de los cuerpos de los cuerpos de los cuerpos de los cuerpos de los cuerpos de los cuerpos de los cuerpos de los cuerpos de los cuerpos de los cuerpos de los cuerpos de los cuerpos de los cuerpos de los cuerpos de los cuerpos de los cuerpos de los cuerpos de los cuerpos de los cuerpos de los cuerpos de los cuerpos de los cuerpos de los cuerpos de los cuerpos de los cuerpos de los cuerpos de los cuerpos de los cuerpos de los cuerpos de los cuerpos de los cuerpos de los cuerpos de los cuerpos de los cuerpos de los cuerpos de los cuerpos de los cuerpos de los cuerpos de los cuerpos de los cuerpos
- El ruido gradiente en SGD es aproximadamente normal (suma de muchos gradientes de muestra)
  China 翻译:SGD 中的梯度噪音近似正态 (en inglés)
- La distribución normal es la distribución máxima de entropía para una media y varianza dada
  Traducción:La distribución normal es la distribución máxima de un valor medio determinado y el diferencial de la cuota.

### Probabilidades de registro

Las probabilidades crudas causan problemas numéricos. Multiplicar muchas probabilidades pequeñas juntas rápidamente se subtrae a cero.

> La probabilidad inicial conducirá a problemas de valores.

```
P(sentence) = P(word1) * P(word2) * ... * P(word_n)
            = 0.01 * 0.003 * 0.02 * ...
            -> 0.0 (underflow after ~30 terms)
```

Las probabilidades de registro arreglan esto. Las multiplicaciones se convierten en adiciones.

> La probabilidad numérica ha resuelto este problema.

```
log P(sentence) = log P(word1) + log P(word2) + ... + log P(word_n)
                = -4.6 + -5.8 + -3.9 + ...
                -> finite number (no underflow)
```

Reglas:
- log(a * b) = log(a) + log(b)
- Las probabilidades de registro son siempre <= 0 (ya que 0 < P <= 1)
- Más negativo = menos probable
- La pérdida de entropía cruzada es la probabilidad de registro negativo de la clase correcta

> 规则:
> - log(a * b) = log(a) + log(b)
> - La probabilidad de la cantidad es siempre <= 0 (porque 0 < P <= 1)
> - 越负 = 越不可能
> - 交叉损失就是正确类别的负对数概率

### Softmax como distribución de probabilidad

Las redes neuronales producen puntajes en bruto (logits). Softmax los convierte en una distribución de probabilidades válida.

> 神经网络输出原始分数(logits) ――Softmax los transformará en una distribución de probabilidad efectiva―

```
softmax(z_i) = exp(z_i) / sum(exp(z_j) for all j)

Properties:
  - All outputs are in (0, 1)
  - All outputs sum to 1
  - Preserves relative ordering of inputs
  - exp() amplifies differences between logits
```

El truco de softmax: restar la máxima logit antes de exponenciar para evitar el desbordamiento.

> Softmax 技巧: en la medida en que se reduce el máximo de logit, se evita la sobreposición.

```
z = [100, 101, 102]
exp(102) = overflow

z_shifted = z - max(z) = [-2, -1, 0]
exp(0) = 1  (safe)

Same result, no overflow.
```

Log-softmax combina softmax y log para la estabilidad numérica. PyTorch utiliza esto internamente para la pérdida de entropía cruzada.

> Log-softmax se aplicará a la softmax y log 合并 en un paso para mantener la estabilidad numérica.

### Muestreo

Muestreo significa extraer valores aleatorios de una distribución.
- Dejar de tomar muestras aleatorias de qué neuronas se desprenden
  China: Desarrollo 随机采样决定哪些神经元置零
- Muestras de aumento de datos transformaciones aleatorias
  Ciencia de la información en el mundo
- Los modelos de lenguaje muestran el siguiente token de la distribución prevista
  El lenguaje de la lengua se traduce en el lenguaje de la lengua.
- Modelos de difusión muestran ruido y denotan progresivamente
  China: 翻译:扩散模型采样噪音并逐步去噪音

La muestreo de distribuciones arbitrarias requiere técnicas como muestreo de transformación inversa, muestreo de rechazo o el truco de reparameterización (utilizado en VAEs).

> Desde la distribución arbitraria de la toma de muestras se requiere inversación de la toma de muestras, rechazo de la toma de muestras o técnicas de re-parámetros (VAE) etc.

## Construye y realiza.
```figure
gaussian-pdf
```

## Construye el mismo

### Paso 1: Bases de probabilidad

```python
import math
import random

def factorial(n):
    result = 1
    for i in range(2, n + 1):
        result *= i
    return result

def combinations(n, k):
    return factorial(n) // (factorial(k) * factorial(n - k))

def conditional_probability(p_a_and_b, p_b):
    return p_a_and_b / p_b

p_king_given_face = conditional_probability(4/52, 12/52)
print(f"P(King | Face card) = {p_king_given_face:.4f}")
```

### Paso 2: PMF y PDF desde cero

```python
def bernoulli_pmf(k, p):
    return p if k == 1 else (1 - p)

def categorical_pmf(k, probs):
    return probs[k]

def poisson_pmf(k, lam):
    return (lam ** k) * math.exp(-lam) / factorial(k)

def uniform_pdf(x, a, b):
    if a <= x <= b:
        return 1.0 / (b - a)
    return 0.0

def normal_pdf(x, mu, sigma):
    coeff = 1.0 / (sigma * math.sqrt(2 * math.pi))
    exponent = -0.5 * ((x - mu) / sigma) ** 2
    return coeff * math.exp(exponent)
```

### Paso 3: Valor esperado y variación

```python
def expected_value(values, probabilities):
    return sum(v * p for v, p in zip(values, probabilities))

def variance(values, probabilities):
    mu = expected_value(values, probabilities)
    return sum(p * (v - mu) ** 2 for v, p in zip(values, probabilities))

die_values = [1, 2, 3, 4, 5, 6]
die_probs = [1/6] * 6
mu = expected_value(die_values, die_probs)
var = variance(die_values, die_probs)
print(f"Die: E[X] = {mu:.4f}, Var(X) = {var:.4f}, SD = {var**0.5:.4f}")
```

### Paso 4: Muestreo de las distribuciones

```python
def sample_bernoulli(p, n=1):
    return [1 if random.random() < p else 0 for _ in range(n)]

def sample_categorical(probs, n=1):
    cumulative = []
    total = 0
    for p in probs:
        total += p
        cumulative.append(total)
    samples = []
    for _ in range(n):
        r = random.random()
        for i, c in enumerate(cumulative):
            if r <= c:
                samples.append(i)
                break
    return samples

def sample_normal_box_muller(mu, sigma, n=1):
    samples = []
    for _ in range(n):
        u1 = random.random()
        u2 = random.random()
        z = math.sqrt(-2 * math.log(u1)) * math.cos(2 * math.pi * u2)
        samples.append(mu + sigma * z)
    return samples
```

### Paso 5: Softmax y probabilidades de registro

```python
def softmax(logits):
    max_logit = max(logits)
    shifted = [z - max_logit for z in logits]
    exps = [math.exp(z) for z in shifted]
    total = sum(exps)
    return [e / total for e in exps]

def log_softmax(logits):
    max_logit = max(logits)
    shifted = [z - max_logit for z in logits]
    log_sum_exp = max_logit + math.log(sum(math.exp(z) for z in shifted))
    return [z - log_sum_exp for z in logits]

def cross_entropy_loss(logits, target_index):
    log_probs = log_softmax(logits)
    return -log_probs[target_index]
```

### Paso 6: Teorema de límite central demostración

```python
def demonstrate_clt(dist_fn, n_samples, n_averages):
    averages = []
    for _ in range(n_averages):
        samples = [dist_fn() for _ in range(n_samples)]
        averages.append(sum(samples) / len(samples))
    return averages
```

### Paso 7: Visualización

```python
import matplotlib.pyplot as plt

xs = [mu + sigma * (i - 500) / 100 for i in range(1001)]
ys = [normal_pdf(x, mu, sigma) for x, mu, sigma in ...]
plt.plot(xs, ys)
```

Las implementaciones completas con todas las visualizaciones están en `code/probability.py`¿ Qué ?

> incluye la realización completa de todo lo que se ve`code/probability.py`¿Qué es eso?

## Usalo con el marco de ejecución

Con NumPy y SciPy, todo lo anterior es de una sola línea:

> Utiliza NumPy y SciPy, todas las funciones que se mencionan sólo necesitan una línea de código:

```python
import numpy as np
from scipy import stats

normal = stats.norm(loc=0, scale=1)
samples = normal.rvs(size=10000)
print(f"Mean: {np.mean(samples):.4f}, Std: {np.std(samples):.4f}")
print(f"P(X < 1.96) = {normal.cdf(1.96):.4f}")

logits = np.array([2.0, 1.0, 0.1])
from scipy.special import softmax, log_softmax
probs = softmax(logits)
log_probs = log_softmax(logits)
print(f"Softmax: {probs}")
print(f"Log-softmax: {log_probs}")
```

Construiste esto desde cero, ahora sabes lo que hacen las llamadas de la biblioteca.

> Has construido esto desde cero. Ahora sabes lo que hace la función de la biblioteca.

## Los ejercicios.

1. Implemente muestreo inverso de transformación para la distribución exponencial. Verifique tomando muestras de 10.000 valores y comparando el histograma con el PDF real.

2. Construye una tabla de distribución conjunta para dos dados cargados, computa las distribuciones marginales y comprueba si los dados son independientes.

3. Calcule la pérdida de entropía cruzada para un clasificador de 5 clases que emita logits `[2.0, 0.5, -1.0, 3.0, 0.1]`Cuando la clase correcta es el índice 3. Entonces verifique su respuesta con PyTorch's `nn.CrossEntropyLoss`¿ Qué ?

4. Escriba una función que tome una lista de probabilidades de registro y devuelve la secuencia más probable, la probabilidad total de registro y la probabilidad bruta equivalente. Pruébalo con una oración de 50 palabras donde cada palabra tiene probabilidad 0.01.

## Términos clave .

| Term | What people say | What it actually means |
|------|----------------|----------------------|
| Sample space | "All the possibilities" / "所有可能性" | The set S of every possible outcome of an experiment / 实验所有可能结果的集合 S |
| PMF | "The probability function" / "概率函数" | A function that gives the exact probability of each discrete outcome, summing to 1 / 给出每个离散结果精确概率的函数，总和为 1 |
| PDF | "The probability curve" / "概率曲线" | A density function for continuous variables. Integrate it over an interval to get probability / 连续变量的密度函数，在区间上积分得到概率 |
| Conditional probability | "Probability given something" / "条件概率" | P(A\|B) = P(A and B) / P(B). The foundation of Bayesian thinking and Bayes' theorem / 贝叶斯思维和贝叶斯定理的基础 |
| Independence | "They don't affect each other" / "互不影响" | P(A and B) = P(A) * P(B). Knowing one event tells you nothing about the other / 知道一个事件不影响另一个 |
| Expected value | "The average" / "平均值" | The probability-weighted sum of all outcomes. The loss function is an expected value / 所有结果的概率加权求和，损失函数就是一种期望值 |
| Variance | "How spread out" / "离散程度" | The expected squared deviation from the mean. High variance = noisy, unstable estimates / 偏离均值的平方的期望，方差大 = 噪声大、不稳定 |
| Normal distribution | "The bell curve" / "钟形曲线" | f(x) = (1/sqrt(2*pi*sigma^2)) * exp(-(x-mu)^2/(2*sigma^2)). Appears everywhere due to the CLT / 因中心极限定理而无处不在 |
| Central Limit Theorem | "Averages become normal" / "平均趋于正态" | The mean of many independent samples converges to a normal distribution regardless of the source / 许多独立样本的均值收敛到正态分布 |
| Joint distribution | "Two variables together" / "两个变量一起" | P(X, Y) describes the probability of every combination of X and Y outcomes / 描述 X 和 Y 每种组合的概率 |
| Marginal distribution | "Sum out the other variable" / "消去另一个变量" | P(X) = sum_y P(X, Y). Recovers one variable's distribution from the joint / 从联合分布中恢复单个变量的分布 |
| Log probability | "Log of the probability" / "概率的对数" | log P(x). Turns products into sums, preventing numerical underflow in long sequences / 将乘法变加法，防止长序列数值下溢 |
| Softmax | "Turn scores into probabilities" / "分数转概率" | softmax(z_i) = exp(z_i) / sum(exp(z_j)). Maps real-valued logits to a valid probability distribution / 将实数值 logits 映射为有效概率分布 |
| Cross-entropy | "The loss function" / "损失函数" | -sum(p_true * log(p_predicted)). Measures how different two distributions are. Lower is better / 衡量两个分布的差异，越小越好 |
| Logits | "Raw model outputs" / "模型原始输出" | Unnormalized scores before softmax. Named after the logistic function / softmax 之前的未归一化分数 |
| Sampling | "Drawing random values" / "随机取值" | Generating values according to a probability distribution. How models generate output / 按概率分布生成值，模型用它生成输出 |

## Más Leer más Leer más

- [3Blue1Brown: But what is the Central Limit Theorem?](https://www.youtube.com/watch?v=zeJD6dqJ5lo)- prueba visual de por qué las medias se vuelven normales
- [Stanford CS229 Probability Review](https://cs229.stanford.edu/section/cs229-prob.pdf)- una referencia concisa que cubre todo aquí y más
- [The Log-Sum-Exp Trick](https://gregorygundersen.com/blog/2020/02/09/log-sum-exp/)- por qué es importante la estabilidad numérica y cómo lograrla
