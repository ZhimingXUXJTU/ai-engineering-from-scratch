# Los métodos de muestreo

> La muestreo es la forma en que la IA explora el espacio de posibilidades.
> 采样是AI 探索可能性空间的方式──

**Type:** Build | **类型:** 动手
**Language:**¿ Qué pasa ?**语言:**Python
**Prerequisites:** Phase 1, Lessons 06-07 (Probability, Bayes' Theorem) | **前置知识:** Phase 1, 第 06-07 课（概率、贝叶斯定理）
**Time:** ~120 minutes | **时间:** ~120 分钟

## Objetivos de aprendizaje

- Implementar muestreo inverso de CDF, rechazo e importancia desde cero utilizando solo números aleatorios uniformes
  Utilizaciones de datos y datos de datos de la empresa (incluidas las de la empresa)
- Construir muestreo de temperatura, top-k y top-p (núcleo) para la generación de tokens de modelos de lenguaje
  构建用于语言模型代币 生成的温度、top-k 和 top-p(nucleus)采样
- Explica el truco de reparameterización y por qué permite la retropropagación mediante muestreo en VAEs
  解释重参数化技巧(Reparameterization Trick) y por qué puede hacer que la operación de la toma de datos en el VAE apoye la transmisión de datos
- ejecuta el MCMC de Metropolis-Hastings para tomar muestras de una distribución objetivo no normalizada
  运行 Metropolis-Hastings MCMC Desde la dispersión de objetivos de la integración


> **【中文解读】**
> 采样是 AI 探索可能性的方法──LLM 控制文本生成多样性──VAE 采样是 AI 探索可能性的方法──LLM 控制文本生成多样性──VAE 采样是 AI 探索可能性的方法──LLM 控制文本生成多样性──VAE 采样是 AI 探索可能性的方法──LLM 采样是温度/top-k/top-p 控制文本生成多样性──VAE 采样是重参数化技巧让采样可微──扩散模型的前向过程是采样,反向过程是去噪 (生成) △

## El problema es la introducción del problema

Un modelo de lenguaje termina de procesar su solicitud y produce un vector de 50.000 logitos, uno para cada token en su vocabulario. Ahora tiene que elegir uno. ¿Cómo?

> Después de procesar su sugerencia, generará un volumen de 50.000 logitos, para cada token en la lista de palabras. Ahora necesita seleccionar uno. ¿Cómo elegir?

Si siempre elige el token de mayor probabilidad, cada respuesta es idéntica. Determinista. Aburrida. Si elige uniformemente al azar, la salida es vagañosa. La respuesta vive en algún lugar entre estos extremos, y que en algún lugar está controlada por muestreo.

> Si cada vez se elige el token de probabilidad más alto, cada vez se responde con la misma certeza, sin charlas. Si cada vez se elige con la misma probabilidad, la salida es entre dos extremos.

La toma de muestras no se limita a la generación de textos. El aprendizaje de refuerzo estima los gradientes de las políticas mediante trayectorias de muestreo. Los VAEs aprenden representaciones latentes tomando muestras de las distribuciones aprendidas y propagándose hacia atrás a través de la aleatoriedad. Los modelos de difusión generan imágenes mediante muestreo de ruido y denociación iterativa. Los métodos de Monte Carlo estiman integrales que no tienen solución de forma cerrada. Los algoritmos MCMC exploran distribuciones posteriores de alta dimensión que son imposibles de enumerar.

> 采样不仅限于文本生成──强化学习通过采样轨迹(轨迹) 來估计策略梯度──VAE 通过从学习到分布中采样并反向传播来学习隐表示──扩散模型通过采样噪声并代去噪声来生成图像──蒙特卡洛方法估算没有解析的积分──MCMC 算法探索无法枚举的高维后验分布──

Cada sistema de IA generativo es un sistema de muestreo. La estrategia de muestreo determina la calidad, diversidad y controlabilidad de la salida. Esta lección construye todos los métodos principales de muestreo desde cero, comenzando con números aleatorios uniformes y terminando con las técnicas que impulsan los LLM y modelos generativos modernos.

> Cada sistema de IA generado es en esencia un sistema de toma de decisiones. La estrategia de toma de decisiones determina la calidad, la diversidad y la capacidad de control de la producción.

## El concepto central.

> **【中文解读】**
> 采样问题无处不在: 语言模型需要从50,000代币中选一个,VAE需要从隐空间采样,扩散模型需要从噪声逐步到噪声.

### Por qué es importante tomar muestras

La muestreo aparece en cuatro roles fundamentales en IA y aprendizaje automático:

> 采样 en la IA y el aprendizaje automático desempeña cuatro papeles básicos:

**Generation.**Los modelos de lenguaje, modelos de difusión y GAN producen resultados mediante muestreo. El algoritmo de muestreo controla directamente la creatividad, la coherencia y la diversidad. La temperatura, la top-k y el muestreo de núcleo son los botones que los ingenieros hacen diariamente.

> **生成。**语言模型、扩散模型和 GAN都通过采样产生输出──采样算法直接控制创造力、连贯性和多样性──温度、top-k 和核采样是工程师每天调节的"旋"",

**Training.**Muestras de descenso de gradiente estocástico mini-partidos. Muestras de descenso de neuronas para desactivar. Muestras de aumento de datos muestran transformaciones aleatorias. Muestras de importancia reponderan muestras para reducir la variación de gradiente en el aprendizaje de refuerzo (PPO, TRPO).

> **训练。**随机梯度下降(SGD) 采样 mini-batch──Dropout 采样要禁用神经元──数据增强采样随机变换──重要性采样重新加权样样以后降强化学习──PPO、TRPO) 采样方差中的梯度方差──

**Estimation.**Muchas cantidades en ML no tienen solución de forma cerrada. La pérdida esperada sobre una distribución de datos, la función de partición de un modelo basado en energía, la evidencia en la inferencia bayesiana. La estimación de Monte Carlo aproxima todas estas cosas mediante una media sobre muestras.

> **估计。**Muchas de las cantidades de ML no se resuelven. Las expectativas de pérdida en la distribución de datos, las funciones de distribución basadas en el modelo de energía, los datos de la hipótesis de Bayes, la evidencia de la existencia de una base de datos, la evidencia de la existencia de una base de datos, la evidencia de la existencia de una base de datos, la evidencia de la existencia de una base de datos, la evidencia de la existencia de una base de datos, la evidencia de la existencia de una base de datos, la información de la base de datos, la información de la base de datos, la información de la base de datos, la información de la base de datos, la información de la base de datos, la información de la base de datos, la información de datos, la información de la base de datos, la información de datos, la información de la base de datos, la información de datos, etc.

**Exploration.**Los algoritmos MCMC exploran las distribuciones posteriores en la inferencia bayesiana.

> **探索。**El MCMC álgoritmo en el teorema de Bayesian explora posterior experiencia distribución  estrategia de evolución  estrategias evolutivas                                                                                                                                                                                                                                               

El reto principal: sólo se puede tomar muestras directamente de distribuciones simples (uniforme, normal).

> 核心挑战:你只能直接从简单分布 (简单分布) 均分布、正态分布) 中采样.

> **【拓展：LLM 采样策略的工程实践】**
> GPT-4 等模型推理时,temperatura normalmente se establece en 0.0-1.0,top-p 设为 0.9-1.0。OpenAI API 默认温度=1.0、top_p=1.0。研究表明 top-p (núcleo) 采样在大多数任务上优于 top-k,因为它能根据模型置信度自适应调整候选集大小──对于代码生成,temperatura=0.2 + top_p=0.95 是常见配置──

### Muestreo aleatorio uniforme

Cada método de muestreo comienza aquí. Un generador de números aleatorios uniforme produce valores en [0, 1) donde cada subintervalo de igual longitud tiene la misma probabilidad.

> Todos los métodos de selección se inician desde aquí. Los generadores de números producen el valor medio [0, 1) entre los cuales la probabilidad de que los subzonos de longitud tengan la misma probabilidad.

```
U ~ Uniform(0, 1)

P(a <= U <= b) = b - a    for 0 <= a <= b <= 1

Properties:
  E[U] = 0.5
  Var(U) = 1/12
```

Para tomar muestras uniformes de un conjunto discreto de n elementos, generar U y devolver piso(n * U. Para tomar muestras de un rango continuo [a, b], calcular a + (b - a) * U.

> Para obtener un resultado de la separación de los elementos, generar U y volver al suelo,

La clave: un solo número aleatorio uniforme contiene exactamente la cantidad adecuada de aleatoriedad para producir una muestra de cualquier distribución.

> 关键洞察: el número de azar individuales medio contiene una aleatoriedad suficiente para generar una muestra de cualquier distribución.

> **【中文解读】**
> 均分布是所有采样基石── en el ordenador se produce un falso generador de números con frecuencia (como Mersenne Twister) es el resultado de la distribución de la distribución de la distribución de los datos de la base.

### Método inverso de CDF (muestreo de transformación inversa)

La función de distribución acumulada (CDF) asigna los valores a probabilidades:

```
F(x) = P(X <= x)

Properties:
  F is non-decreasing
  F(-inf) = 0
  F(+inf) = 1
  F maps the real line to [0, 1]
```

El CDF inverso mapea las probabilidades de vuelta a valores. Si U ~ Uniform(0, 1), entonces X = F_inverse(U) sigue la distribución objetivo.

> 逆 CDF 将概率映射回值──如果 U ~ Uniform(0, 1), entonces X = F_inverse(U) 服从目标分布──

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

Esto funciona perfectamente cuando se puede escribir F_inverse en forma cerrada. Para la distribución normal, no hay CDF inverso de forma cerrada, por lo que usamos otros métodos (Box-Muller, o aproximación numérica).

> Cuando puedes escribir una expresión de resolución de F_inverse, este método es perfecto para el funcionamiento. Para la distribución de estado correcto, no hay forma de resolución en contra de CDF, por lo que usamos otros métodos.

**Discrete version:**Para las distribuciones discretas, construye el CDF como una suma acumulada, genera U y encuentra el primer índice donde la suma acumulada exceda a U. Así es como `sample_categorical`trabaja en la Lección 06.

> **离散版本：**对于离散分布,将CDF 构建为累积和,生成 U,找到累积和首次超过 U 的索引──这是第06 课中`sample_categorical`El trabajo de la empresa.

> **【中文解读】**
> 逆 CDF 方法的核心思想:CDF 函数 F(x) Colocar el valor de la variable de manera constante a la probabilidad de [0,1], mientras que su función inversa F_inverse está bien reversa. Colocar [0,1] de forma constante a la función de manera constante a la función de distribución de la meta. Este método es preciso, pero es muy eficaz.

### Muestras de rechazo

Cuando no se puede invertir el CDF pero puede evaluar el PDF objetivo hasta una constante, el muestreo de rechazo funciona.

> Cuando no puedes pedir contra CDF, pero puedes calcular objetivos PDF (todo lo que sea un factor constante)

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

En las dimensiones bajas (1-3), el muestreo de rechazo funciona bien. En las dimensiones altas, la tasa de aceptación disminuye exponencialmente porque la mayor parte del volumen de la propuesta es rechazada. Esta es la maldición de dimensionalidad para el muestreo de rechazo.

> En el espacio de alto nivel, la tasa de aceptación en el índice de índice de baja, ya que la mayor parte de las propuestas de volumen fueron rechazadas.

**Example: sampling from a truncated normal.**Utilice una propuesta uniforme en el rango truncado. El sobre M es el máximo del PDF normal en ese rango.

> **示例：从截断正态分布采样。**En el ámbito de la interceptación de uso de la distribución de la oferta.

**Example: sampling from a semicircle.**Propón uniformemente en el rectángulo de borde. Acepta si el punto cae dentro del semicírculo. Así calcula Monte Carlo pi: la tasa de aceptación es igual a la proporción de área pi/4.

> **示例：从半圆采样。**En el rectángulo exterior, la tasa de aceptación es igual a la superficie de pi por cuarto.

> **【拓展：拒绝采样在粒子滤波中的应用】**
> 粒子波(Particle Filter) es un algoritmo central de seguimiento de objetivos y de posicionamiento de los órganos. En esencia es un método de rechazo de la muestreo con un conjunto de "partículas" de distribución de probabilidad, según los resultados de la observación sobre la muestreo de partículas.

### Muestreo de importancia

A veces no se necesitan muestras de la distribución objetivo p(x). Se necesita estimar una expectativa bajo p(x), y se tienen muestras de una distribución diferente q(x.

> Algunas veces no necesitas un modelo de distribución de p(x) en el centro, sino que necesitas un modelo de distribución de p(x) en el centro, y tienes que calcular un modelo de distribución de q(x) en el centro.

```
Goal: estimate E_p[f(x)] = integral of f(x) * p(x) dx

Rewrite:
  E_p[f(x)] = integral of f(x) * (p(x)/q(x)) * q(x) dx
            = E_q[f(x) * w(x)]

where w(x) = p(x) / q(x)  are the importance weights.

Estimator:
  E_p[f(x)] ~ (1/N) * sum(f(x_i) * w(x_i))    where x_i ~ q(x)
```

Esto es fundamental en el aprendizaje de refuerzo. En PPO (Proximal Policy Optimization), recopilas trayectorias bajo una vieja política pi_old pero quieres optimizar una nueva política pi_new. El peso de importancia es pi_new ̇a ̇a ̇a ̇a ̇a ̇a ̇a ̇a ̇a ̇a ̇a ̇a ̇a ̇a ̇a ̇a ̇a ̇a ̇a ̇a ̇a ̇a ̇a ̇a ̇a ̇a ̇a ̇a ̇a ̇a ̇a ̇a ̇a ̇a ̇a ̇a ̇a ̇a ̇a ̇a ̇a ̇a ̇a ̇a ̇a ̇a ̇a ̇a ̇a ̇a ̇a ̇a ̇a ̇a ̇a ̇a ̇a ̇a ̇a ̇a ̇a ̇a ̇a ̇a ̇a ̇a ̇a ̇a ̇a ̇a ̇a ̇a ̇a ̇a ̇a ̇a ̇a ̇a ̇a ̇a ̇a ̇a ̇a ̇a ̇a ̇a ̇a ̇a ̇a ̇a ̇a ̇a ̇a ̇a ̇a ̇a ̇a ̇a ̇a ̇a ̇a ̇a ̇a ̇a ̇a ̇a ̇a ̇a ̇a ̇a ̇a ̇a ̇a ̇a    ̇a ̇a  ̇a ̇a  ̇a    ̇a    ̇a     ̇a      ̇      ̇                                                         

> Esto es esencial en la formación de la fuerza. En la optimización de la política próxima (PPO) usted está en la estrategia antigua.

> **【拓展：PPO 中的重要性采样】**
> PPO es el algoritmo central de la capacitación de ChatGPT RLHF. Su importancia es la de modificar la diferencia de distribución entre las nuevas estrategias antiguas.

La variación del estimador de muestreo de importancia depende de cuan similar q es a p. Si q es muy diferente de p, algunas muestras obtienen enormes pesos y dominan la estimación.

> La diferencia de importancia del estimador de muestras depende de la similitud entre q y p. Si q y p difieren mucho, un pequeño número de muestras obtendrán un gran peso y se orientarán en la estimación.

```
E_p[f(x)] ~ sum(w_i * f(x_i)) / sum(w_i)
```

### Estimación de Monte Carlo

La estimación de Monte Carlo aproxima las integrales mediante la media de muestras aleatorias.

> La estimación de Monte Carlo a través de la media de muestras de tiempo para obtener un tamaño aproximado.

```
Goal: estimate I = integral of g(x) dx over domain D

Method:
  1. Sample x_1, ..., x_N uniformly from D
  2. I ~ (Volume of D / N) * sum(g(x_i))

Error: O(1 / sqrt(N))   regardless of dimension
```

La tasa de error es independiente de las dimensiones, por lo que los métodos de Monte Carlo dominan en dimensiones altas donde la integración basada en la red es imposible.

> La tasa de error no tiene relación con la dimensión. Por eso el método Monte Carlo ocupa el lugar dominante en el espacio de gran tamaño.

> **【中文解读】**
> El esmero del método de Monte Carlo: se utiliza el valor medio de la muestra de tiempo para obtener una aproximación de la expectativa. La gran cantidad de teorías garantiza la recepción, y la tasa de error O(1/sqrt(N)) no tiene relación con la dimensión. Esto es muy importante en el problema de alto tamaño.

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

### La cadena Markov Monte Carlo (MCMC): Metrópolis-Hastings

MCMC construye una cadena de Markov cuya distribución estacionaria es la distribución objetivo p(x). Después de suficientes pasos, las muestras de la cadena son (aproximadamente) muestras de p(x.

> MCMC construir una cadena de Markov ), su distribución estacionaria ), es la distribución objetivo x (x) .

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

Para las propuestas simétricas (q(x' (x) = q(x (x) = x)), la relación se simplifica a p(x') / p(x. Este es el algoritmo Metropolis original.

> 对于对称提议 (q) = q) ),比率简化为 p (x) /p (x) .

**Why it works.**La regla de aceptación asegura el equilibrio detallado: la probabilidad de estar en x y moverse a x' es igual a la probabilidad de estar en x' y moverse a x. El equilibrio detallado implica que p(x) es la distribución estacionaria de la cadena.

> **为什么有效。**                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             

> **【拓展：MCMC 在贝叶斯深度学习中的应用】**
> PyMC、NumPyro 等 Bayesian 推理框架的核心就是MCMC──NUTS (No-U-Turn Sampler) es el MCMC 变体最先进, se regula automáticamente el tamaño y la dirección. En el descubrimiento de medicamentos, los investigadores utilizaron MCMC 采样分子构造的后验分布, procesar miles de dimensiones de espacio.

**Practical considerations:**
- Incendio: descartar las muestras tempranas antes de que la cadena alcance el equilibrio
  预热期(Burn-in): dejar la cadena para alcanzar el equilibrio previo de la muestra temprana
- El adelgazamiento: mantener cada k-a muestra para reducir la autocorrelación
  稀释(Tinning): cada separado de muestras se conserva una para reducir
- Escala de las propuestas: demasiado pequeña y la cadena se mueve lentamente (alta aceptación, lenta exploración); demasiado grande y la mayoría de las propuestas son rechazadas (baja aceptación, en su lugar)
  提议尺度(Proposal Scale): 太小则链移动缓慢(acceptation rate high but explore slow); 太大则大多数提议被拒绝(acceptation rate low,原地不动)
- La tasa óptima de aceptación de una propuesta gaussiana en grandes dimensiones es de aproximadamente 0,234
  La tasa de aceptación óptima de la alta propuesta en el espacio es de aproximadamente 0,234.

### Muestras de Gibbs

El muestreo de Gibbs es un caso especial de MCMC para distribuciones multivariadas. En lugar de proponer un movimiento en todas las dimensiones a la vez, actualiza una variable a la vez de su distribución condicional.

> Gibbs 采样 es un ejemplo de MCMC en la distribución de múltiples variables. No se mueve simultáneamente en todas las dimensiones, sino que se actualiza una variación cada vez que se encuentra en la distribución de condiciones.

```
Target: p(x_1, x_2, ..., x_d)

Algorithm:
  For each iteration t:
    Sample x_1^{t+1} ~ p(x_1 | x_2^t, x_3^t, ..., x_d^t)
    Sample x_2^{t+1} ~ p(x_2 | x_1^{t+1}, x_3^t, ..., x_d^t)
    ...
    Sample x_d^{t+1} ~ p(x_d | x_1^{t+1}, x_2^{t+1}, ..., x_{d-1}^{t+1})
```

El muestreo de Gibbs requiere que puedas muestrar de cada distribución condicional p ((x_i ∈ x_{-i}). Esto es sencillo para muchos modelos:
- Redes bayesianas: los condicionals siguen de la estructura del gráfico
  贝叶斯网络: condiciones distribuidas por la estructura determinada
- Mezclas gaussianas: los condicionantes son gaussianas
  Modelo de alta mezcla: las condiciones de distribución son altas
- Modelos de aislamiento: la condicional de cada giro depende sólo de sus vecinos
  Especialización: cada una de las condiciones de la distribución depende de sus vecinos

La tasa de aceptación es siempre de 1 (se acepta cada propuesta) porque la muestreo de la condición exacta satisface automáticamente el equilibrio detallado.

>  tasa de aceptación siempre es 1 cada propuesta es aceptada), pues de la distribución de condiciones precisas se toma automáticamente la satisfacción de condiciones de equilibrio.

**Limitation.**Cuando las variables están altamente correlacionadas, la muestreo de Gibbs se mezcla lentamente porque actualizar una variable a la vez no puede hacer grandes movimientos diagonales a través de la distribución.

> **局限性。**Cuando las variaciones están muy relacionadas, el modelo de Gibbs se mezcla lentamente, ya que cada vez que se actualiza una sola variación no se puede hacer un gran movimiento de la distribución en contra de los ángulos.

> **【中文解读】**
> El modelo de Gibbs es un ejemplo particular del MCMC: cada vez sólo actualiza una variable, de la distribución de condiciones.

### Muestreo de temperatura (utilizado en LLM)

Los modelos de lenguaje producen logits z_1, ..., z_V para cada token en el vocabulario. Softmax convierte estos en probabilidades.

> 语言模型为词汇表中的每个代币 输出 logits z_1, ..., z_V──Softmax将将转换为概率──Temperatura(温度) 在软max 之前对 logits 进行缩放:

```
p_i = exp(z_i / T) / sum(exp(z_j / T))

T = 1.0: standard softmax (original distribution)
T -> 0:  argmax (deterministic, always picks highest logit)
T -> inf: uniform (all tokens equally likely)
T < 1.0: sharpens the distribution (more confident, less diverse)
T > 1.0: flattens the distribution (less confident, more diverse)
```

**Why it works.**Dividir los logitos por T < 1 amplifica las diferencias entre los logitos. Si z_1 = 2 y z_2 = 1, dividir por T = 0.5 da z_1/T = 4 y z_2/T = 2, haciendo que la brecha sea mayor. Después de softmax, el token de logito más alto obtiene una participación mucho mayor.

> **为什么有效。**Se puede calcular la diferencia entre los logitos de T < 1 ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅                                                                                                                                                                                                       

**In practice:**
- T = 0,0: codificación codificada, mejor para preguntas y respuestas de hecho
  贪心解码, más adecuado a la realidad
- T = 0,3-0,7: ligeramente creativo, bueno para la generación de código
  略有创意, adaptarse a la generación de código
- T = 0,7-1,0: equilibrado, bueno para la conversación general
  均衡,适合一般对话
- T = 1.0-1.5: escritura creativa, lluvia de ideas
  创意写作、头脑风暴
- T > 1,5: cada vez más aleatorios, raramente útiles
  越来越随时, muy poco útil

La temperatura no cambia qué tokens son posibles, sino la masa de probabilidad asignada a cada token.

> La temperatura no cambia qué símbolo puede ser seleccionado.

> **【中文解读】**
> La temperatura es LLM 输出多样性的"旋"──T < 1 让分布更尖(更像贪心),T > 1 让分布更平坦(更随机)──T → 0 退化为 argmax,T → ∞ 退化为均分布──T=0.7 es el punto de equilibrio más habitual en el medio de la práctica──T: la temperatura no cambia en los tokens que hay, sólo cambia la distribución de probabilidad──

### Muestreo de la parte superior

El muestreo de top-k restringe el conjunto candidato a los tokens k con las mayores probabilidades, luego renormaliza y muestra de ese conjunto restringido.

> El top-k 采样将限制选集为概率最高的 k 个代币, luego volver a regroup并从该受限集合中采样.

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

El top-k impide que el modelo seleccione fijos extremadamente improbables (tipos, tonterías) que existen en la larga cola de la distribución del vocabulario. El problema: k se fija independientemente del contexto. Cuando el modelo es seguro (un token tiene probabilidad del 95%), k = 40 todavía permite 39 alternativas. Cuando el modelo es incierto (la probabilidad se distribuye a través de 1000 tokens), k = 40 corta las opciones plausibles.

> El problema es que: k es fijo, no conlleva cambios en el texto siguiente. Cuando el modelo tiene mucha confianza en que un token ocupa el 95% de la probabilidad), k = 40 todavía permite 39 opciones alternativas.

### Muestreo de la parte superior (núcleo)

El muestreo top-p ajusta dinámicamente el tamaño del conjunto candidato. En lugar de mantener un número fijo de tokens, se guarda el conjunto más pequeño de tokens cuya probabilidad acumulada excede de p.

> No retiene un número fijo de tokens, sino que mantiene la probabilidad acumulada superior a la colección mínima de tokens.

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

Cuando el modelo es seguro, la muestreo de núcleo mantiene pocos tokens (tal vez 2-3). Cuando el modelo es incierto, mantiene muchos (tal vez 200). Este comportamiento adaptativo es por lo que la muestreo de núcleo generalmente produce un texto mejor que el top-k.

> Cuando el modelo tiene confianza, el núcleo 采样只保留少量代币(可能2-3个) ;; cuando el modelo no está seguro, se conserva mucho(可能200个);; Este comportamiento de autoadaptación es el núcleo 采样通常比 top-k 产生更好的文本的原因──

**Common combinations:**
- Temperatura 0,7 + p superior 0,9: buena configuración de uso general
  Bien el ajuste general
- Temperatura 0.0 (compulsiva): mejor para tareas deterministas
  Lo más adecuado para la determinación de las tareas
- Temperatura 1.0 + top-k 50: Fan et al. (2018) configuración original de papel
  Fan 等人 (2018) 原论文设置

Se pueden combinar top-k y top-p. Aplique top-k primero, luego top-p en el conjunto restante.

> Top-k y top-p pueden ser combinados en uso.

### Tricuación de reparameterización (utilizada en VAEs)

Los autoencodadores variacionales (VAE) aprenden codificando entradas en una distribución en espacio latente, tomando muestras de esa distribución y descifrando la muestra de nuevo.

> 变分自编码器(VAE) mediante la entrada de código para la distribución en el espacio oculto 、 desde la distribución de la muestra 、 luego la muestra de código descifrado volver a aprender ;; el problema es: no se puede realizar la transmisión reversa mediante la operación de la muestra ;;

```
Standard sampling (not differentiable):
  z ~ N(mu, sigma^2)

  The randomness blocks gradient flow.
  d/d_mu [sample from N(mu, sigma^2)] = ???
```

El truco de reparameterización separa la aleatoriedad de los parámetros:

> Las técnicas de la parámetriz se dejarán al azar y parámetros por separado:

```
Reparameterized sampling:
  epsilon ~ N(0, 1)          (fixed random noise, no parameters)
  z = mu + sigma * epsilon   (deterministic function of parameters)

  Now z is a deterministic, differentiable function of mu and sigma.
  d(z)/d(mu) = 1
  d(z)/d(sigma) = epsilon

  Gradients flow through mu and sigma.
```

Esto funciona porque N(mu, sigma^2) tiene la misma distribución que mu + sigma * N(0, 1). La clave: mover la aleatoriedad a una fuente libre de parámetros (epsilon), luego expresar la muestra como una transformación diferenciable de los parámetros.

> Esto es porque es válido, es porque N ∈ Mu, sigma^2) con mu + sigma * N ∈ 0, 1) ∈ N tiene la misma distribución.

**In the VAE training loop:**
1. Encuentra las salidas mu y log(sigma^2) para cada entrada
2. Muestra de epsilon ~ N(0, 1)
3. Computa z = mu + sigma * epsilon
4. Decodificar z para reconstruir la entrada
5. Propagación hacia atrás a través de los pasos 4, 3, 2, 1 (posible porque el paso 3 es diferenciable)

Sin el truco de reparameterización, las VAEs no pueden ser entrenadas con la retropropagación estándar.

>  sin técnicas de pesimismo, la VAE no puede utilizar el entrenamiento estándar contra la transmisión 

> **【拓展：重参数化技巧的广泛应用】**
> La técnica de la gravitacion no se limita a la VAE. La diferencia de la diferencia entre las variables de la velocidad y la velocidad de la velocidad de la velocidad de la velocidad de la velocidad de la velocidad de la velocidad de la velocidad de la velocidad de la velocidad de la velocidad de la velocidad de la velocidad.

### Gumbel-Softmax (Muestreo categórico diferenciable)

El truco de reparameterización funciona para distribuciones continuas (Gaussian). Para distribuciones categoricas discretas, necesitamos un enfoque diferente. Gumbel-Softmax proporciona una aproximación diferenciable a la muestreo categórico.

> Las técnicas de la gravitacion se aplican a la distribución continua. Para la distribución de las clases separadas, se necesitan diferentes métodos.

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

Gumbel-Softmax produce una relajación continua de una muestra discreta. La salida es un vector de probabilidad (blando un-hot) en lugar de un duro un-hot. Los gradientes fluyen a través del softmax. Durante el pase hacia adelante en el entrenamiento, se puede usar el estimador "directo a través": utilizar el argmax duro para el pase hacia adelante pero los gradientes blandos de Gumbel-Softmax para el pase hacia atrás.

> Gumbel-Softmax 产生离散样本的连续松(Continuous Relaxation) ――输出是一个概率向量(软一热) 而不是硬一热――梯度可以流过软max──在训练的前向传播中,你可以使用"直通估计器"(Straight-Through Estimator):前向传播使用硬 argmax,反向传播使用软 Gumbel-Softmax 梯度──

**Applications:**
- Variables latentes discretas en las VAEs
  Variación de la dispersión en el VAE
- Buscar arquitectura neuronal (escoler operaciones discretas)
  神经架构搜索 (sección de operaciones)
- Mecanismos de atención dura
  硬注意力机制 硬注意力机制 硬注意力机制 硬注意力机制 硬注意力机制 硬注意力机制 硬注意力机制 硬注意力机制 硬注意力机制 硬注意力机制 硬注意力机制
- Aprendizaje reforzado con acciones discretas
  离散动作强化学习 离散动作强化学习 离散动作强化学习 离散动作强化学习 离散动作强化学习 离散动作强化学习强化学习强化学习强化学习强化学习强化学习强化学习强化学习强化学习强化学习强化学习强化学习强化学习强化学习强化学习强化学习强化学习强化学习强化学习强化学习强化学习强化学习强化学习强化学习强化学习强化学习强化学习强化学习强化学习强化学习强化学习强化学习强化学习强化学习强化学强化学强化学强化学强强强强强强强强强强强强强强强强强强强强强强强强强强强强强强强强强强强强强强强强强强强强强强强强强强强强强强强强强强强强强强强强强强强强强强强强强强强强强强强强强强强强强强强强强强强强强强强强强强强强强强强强强强强强强强强强强强强强强强强强强强强强强强强强强强强强强强强强强强强强强强强强强强强强强强强强强强强强强强强强强强强强强强强强强强强强强强强强强强强强强强强强强强强强强强强强强强强强强强强强强强强强强强强强强强强强强强强强强强强强强强强强强强强强强强强强强强强强强强强强强强强强强强强强强强强强强强强强强强强强强强强强强强强强强强强强强强强强强强强强强强强强强强强强强强强强强强强强强强强强强强强强强强强强强强强强强强强强强强强强强强强强强强强强强强强强强强强强强强强强强强强强强强强强强强强强强强强

### Muestreo estratificado

El muestreo estándar de Monte Carlo puede dejar vacíos en el espacio de muestreo por casualidad.

> 标准蒙特卡洛采样可能会偶然留下空隙在样本空间中──分层采样──Stratified Sampling) mediante la división del espacio en niveles (Strata)并从每层中采样中来强制均覆盖──

```
Standard Monte Carlo:
  Sample N points uniformly from [0, 1]
  Some regions may have clusters, others gaps

Stratified sampling:
  Divide [0, 1] into N equal strata: [0, 1/N), [1/N, 2/N), ..., [(N-1)/N, 1)
  Sample one point uniformly within each stratum
  x_i = (i + u_i) / N   where u_i ~ Uniform(0, 1),  i = 0, ..., N-1
```

El muestreo estratificado siempre tiene una variación inferior o igual en comparación con el Monte Carlo estándar:

> La diferencia de la forma de la cuadrícula es siempre inferior o igual al estándar de la categoría:

```
Var(stratified) <= Var(standard Monte Carlo)

The improvement is largest when f(x) varies smoothly.
For piecewise-constant functions, stratified sampling is exact.
```

**Applications:**
- Integración numérica (quasi-Monte Carlo)
  Número de puntos de venta
- División de datos de formación (segurando el equilibrio de clases en cada pliegue)
  训练数据划分( asegurar cada giro de la clase balance)
- Muestreo de importancia con estratificación (combinación de ambas técnicas)
  结合分层的重要性采样
- NeRF (Neural Radiance Fields) utiliza muestreo estratificado a lo largo de los rayos de la cámara
  NeRF( campo de radiación neurológica) a lo largo de la fase de la luz de uso de las capas de la

### Conexión a modelos de difusión

Los modelos de difusión generan imágenes a través de un proceso de muestreo. El proceso avanzado agrega ruido gaussiano a una imagen en T pasos hasta que se convierte en ruido puro. El proceso inverso aprende a denotar, recuperando la imagen original paso a paso.

> 扩散模型通过采样过程生成图像──前向过程在T 步内逐步向图像增加高的噪音,直到变成纯噪声──反向过程学习去噪音,逐步恢复原始图像──

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

La conexión con los métodos en esta lección:
- Cada paso de desinfección utiliza el truco de reparameterización (ruido de muestra, aplicar la transformación determinista)
  Cada paso de ruido se utiliza técnicas de reparámetros (también se usan técnicas de reparámetros)
- El horario de ruido {alpha_t} controla una forma de anulación de temperatura
  噪声调度 {alpha_t} 控制一种形式的温度退火(Temperatura Anealing)
- El entrenamiento utiliza la estimación de Monte Carlo para aproximar el ELBO (evidencia límite inferior)
   entrenamiento usando la estimación de Monte Carlo para acercarse a ELBO(Evidencia Bajo límite, evidencia abajo)
- El muestreo ancestral en modelos de difusión es una cadena de Markov (cada paso depende solo del estado actual)
  扩散模型中的祖先采样 (Ancestral Sampling) es una cadena de ancestros (cada paso depende sólo del estado actual)

Todo el proceso de generación de imágenes es muestreo iterativo: comience desde el ruido y, en cada paso, muestre una versión ligeramente menos ruidosa condicionada al modelo de denotación aprendido.

> Todo el proceso de creación de imágenes es de tipo: desde el ruido, en cada paso, se basa en el aprendizaje de un modelo de ruido, de una versión un poco diferente.

## Construye y realiza.
```figure
monte-carlo-pi
```

## Construye el mismo

### Paso 1: Muestreo uniforme y inverso de CDF

```python
import math
import random

def sample_uniform(a, b):
    return a + (b - a) * random.random()  # 线性变换：把 [0,1) 映射到 [a,b)

def sample_exponential_inverse_cdf(lam):
    u = random.random()                   # 生成均匀随机数
    return -math.log(u) / lam             # 逆 CDF：x = -ln(u) / lambda
```

Generar 10.000 muestras exponenciales y verificar que la media es 1/lambda.

> Produce 10.000 muestras de distribución de índices, ¿es el valor medio de la prueba 1/lambda?

### Paso 2: Muestreo de rechazo

```python
def rejection_sample(target_pdf, proposal_sample, proposal_pdf, M):
    while True:                           # 持续采样直到被接受
        x = proposal_sample()             # 从提议分布采样
        u = random.random()               # 均匀随机数用于决定接受/拒绝
        if u < target_pdf(x) / (M * proposal_pdf(x)):  # 接受条件
            return x
```

Utilice muestras de rechazo para extraer de una distribución normal truncada.

> Utilización de muestras de recortes en la distribución de estado correcto.

### Paso 3: Muestreo de importancia

```python
def importance_sampling_estimate(f, target_pdf, proposal_pdf, proposal_sample, n):
    total = 0
    for _ in range(n):
        x = proposal_sample()
        w = target_pdf(x) / proposal_pdf(x)
        total += f(x) * w
    return total / n
```

Estimar E[X^2] bajo una distribución normal utilizando una propuesta uniforme.

> Utiliza均提议分布估计正态分布下 E[X^2]──与已知答案 (mu^2 + sigma^2) 比较──

### Paso 4: Estimación de Monte Carlo de pi

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

### Paso 5: MCMC de Metropolis-Hastings

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

Muestra de una distribución bimodal (mezcla de dos Gaussianos). Visualiza la trayectoria de la cadena.

> Desde la distribución de dos picos (de dos altos) entre la adopción.

### Paso 6: Muestreo de Gibbs

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

### Paso 7: Muestreo de temperatura

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

Muestre cómo la temperatura cambia la distribución de salida para un conjunto de logits de token.

> 展示温度如何改变一组代币日志的输出分布──

### Paso 8: Muestreo de la parte superior y de la parte superior

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

### Paso 9: Truco de reparameterización

```python
def reparam_sample(mu, sigma):
    epsilon = random.gauss(0, 1)          # 标准正态噪声，不含可学习参数
    return mu + sigma * epsilon            # 确定性变换，梯度可流过

def reparam_gradient(mu, sigma, epsilon):
    dz_dmu = 1.0                          # z 对 mu 的梯度恒为 1
    dz_dsigma = epsilon                   # z 对 sigma 的梯度是 epsilon
    return dz_dmu, dz_dsigma
```

Demostrar que los gradientes fluyen a través de la muestra reparametrizada pero no a través de la muestreo directa.

> La escala de demostración puede fluir por encima de la muestra de parámetros pesados, pero no puede fluir directamente por la muestra.

### Paso 10: Gumbel-Softmax

```python
def gumbel_sample():
    u = random.random()
    return -math.log(-math.log(u))

def gumbel_softmax(logits, temperature):
    gumbels = [math.log(p) + gumbel_sample() for p in logits]
    return softmax([g / temperature for g in gumbels])
```

Muestre cómo la disminución de la temperatura hace que la salida se acerque a un vector de un solo calor.

>  demostrando cómo reducir la temperatura hace que la salida se acerque a un extremo caliente ⋅

Las implementaciones completas con todas las visualizaciones están en `code/sampling.py`¿ Qué ?

> La realización completa de todas las visibilidades`code/sampling.py`En el medio.

## Usalo con el marco de ejecución

> **【拓展：扩散模型中的采样工程】**
> Desde la publicación de 2022 años, el método de toma de datos se desarrolla desde 1000 pasos de DDPM hasta DDIM、DPM-Solver++ etc. sólo se necesita un método de 20-50 pasos.

Con NumPy y SciPy, las versiones de producción:

> Utiliza NumPy y SciPy de la versión de producción:

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

Para el MCMC a escala, utilice bibliotecas dedicadas:
- PyMC: modelado bayesiano completo con NUTS (HMC adaptativo)
  完整的贝叶斯建模, usando NUTS(自适应 HMC)
- Emcee: ensamblador de muestras MCMC
  集成 MCMC 采样器 集成 MCMC 采样器 采样器 集成 MCMC 采样器 采样器 采样器 采样器 采样器 采样器 采样器 采样器 采样器 采样器 采样器 采样器 采样器 采样器 采样器 采样器 采样器 采样器 采样器 采样器 采样器 采样器 采样器 采样器 采样器 采样器 采样器 采样器 采样器 采样器 采样器 采样器 采样器 采样器 采样器 采样器 采样器
- NumPyro/JAX: MCMC acelerado por GPU
  GPU acelerado de MCMC

Construiste esto desde cero, ahora sabes lo que hacen las llamadas de la biblioteca.

> Has construido estos métodos desde cero. Ahora sabes lo que hace la función de la biblioteca.

## Los ejercicios.

1. Implemente muestreo inverso de CDF para la distribución de Cauchy. El CDF es F(x) = 0.5 + arctan(x) / pi. Generar 10.000 muestras y trazar el histograma contra el PDF real. Observe las colas pesadas (valores extremos lejos del centro).
   实现柯西分布(Cauchy Distribution) de CDF 采样──CDF 为 F(x) = 0.5 + arctan(x) /pi── generar 10.000 个样本并绘制直方图与真实 PDF 对比──注意重尾(远离中心极端值)。

2. Utilice el muestreo de rechazo para generar muestras de una distribución Beta(2, 5) utilizando una propuesta Uniform(0, 1).
   Utiliza rechazar la muestra de Beta(2, 5) 分布中生成样本,提议分布使用Uniform(0, 1)─绘制接受样本与真实Beta PDF的比图──理论接受率是多少?

3. Estima la integral de sin ((x) de 0 a pi usando Monte Carlo con 1,000, 10,000 y 100,000 muestras. Compara el error en cada nivel. Verifique que la escala de error sea O(1/sqrt(N)).
   Utiliza el método de cálculo de los errores de la base de datos de la base de datos de la base de datos de la base de datos de la base de datos de la base de datos de la base de datos de la base de datos de la base de datos de la base de datos de la base de datos de la base de datos de la base de datos de la base de datos de la base de datos de la base de datos de la base de datos de datos de la base de datos de la base de datos de datos de la base de datos de datos de la base de datos de datos de la base de datos de datos de la base de datos de datos de datos de la base de datos de datos de la base de datos de datos de datos de la base de datos de datos de datos de la base de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de

4. Implementar Metropolis-Hastings para muestrar de una distribución 2D p ((x, y) proporcional a exp ((-(x^2 * y^2 + x^2 + y^2 - 8*x - 8*y) / 2).
   实现 Metropolis-Hastings Desde 2D 分布 p(x, y) ~ exp(-(x^2*y^2 + x^2 + y^2 - 8x - 8y) /2) 中采样──绘制样本和链的轨迹──尝试不同的提议标准差──

5. Construir una demostración completa de generación de texto: dado un vocabulario de 10 palabras con logits, generar secuencias de 20 tokens utilizando (a) codicioso, (b) temperatura = 0,7, (c) top-k = 3, (d) top-p = 0,9. Comparar la diversidad de las salidas en 5 carreras.
   构建一个完整的文本生成演示:给定 10 个词的词汇表和logits,使用 (a) 贪心、(b) temperatura=0.7、(c) top-k=3、((d) top-p=0.9 生成 20 个代币的序列──比较 5 次运行的输出多样性──

## Términos clave .

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

## Más Leer más Leer más

- [Holbrook (2023): The Metropolis-Hastings Algorithm](https://arxiv.org/abs/2304.07010)- un tutorial detallado sobre los fundamentos del MCMC
- [Jang, Gu, Poole (2017): Categorical Reparameterization with Gumbel-Softmax](https://arxiv.org/abs/1611.01144)- papel original Gumbel-Softmax
- [Holtzman et al. (2020): The Curious Case of Neural Text Degeneration](https://arxiv.org/abs/1904.09751)- papel de muestreo de núcleo (top-p)
- [Kingma & Welling (2014): Auto-Encoding Variational Bayes](https://arxiv.org/abs/1312.6114)- Papel de la AEV que introduce el truco de reparameterización
- [Ho, Jain, Abbeel (2020): Denoising Diffusion Probabilistic Models](https://arxiv.org/abs/2006.11239)- DDPM conecta el muestreo a la generación de imágenes
