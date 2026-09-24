# Procesos estocásticos.

> La matemática detrás de los paseos aleatorios, las cadenas de Markov y los modelos de difusión.
> Tiene una estructura de la naturaleza de la naturaleza de la naturaleza de la naturaleza de la naturaleza de la naturaleza de la naturaleza de la naturaleza de la naturaleza de la naturaleza de la naturaleza de la naturaleza de la naturaleza de la naturaleza de la naturaleza de la naturaleza de la naturaleza de la naturaleza de la naturaleza de la naturaleza de la naturaleza de la naturaleza de la naturaleza de la naturaleza de la naturaleza de la naturaleza de la naturaleza de la naturaleza de la naturaleza de la naturaleza de la naturaleza de la naturaleza de la naturaleza de la naturaleza de la naturaleza de la naturaleza de la naturaleza de la naturaleza de la naturaleza de la naturaleza de la naturaleza de la naturaleza de la naturaleza de la naturaleza de la naturaleza de la naturaleza de la naturaleza de la naturaleza de la naturaleza de la naturaleza de la naturaleza de la naturaleza de la naturaleza de la naturaleza de la naturaleza de la naturaleza de la naturaleza de la naturaleza de la naturaleza de la naturaleza de la naturaleza de la naturaleza de la naturaleza de la naturaleza de la naturaleza de la naturaleza de la naturaleza de la naturaleza de la naturaleza de la naturaleza de la naturaleza de la naturaleza de la naturaleza de la naturaleza de la naturaleza de la naturaleza de la naturaleza de la naturaleza de la naturaleza de la naturaleza de la naturaleza de la naturaleza de la naturaleza de la naturaleza.

**Type:** Learn | **类型:** 学习
**Language:**¿ Qué pasa ?**语言:**Python
**Prerequisites:** Phase 1, Lessons 06-07 (probability, Bayes) | **前置知识:** Phase 1, 第 06-07 课（概率、贝叶斯）
**Time:** ~75 minutes | **时间:** ~75 分钟

## Objetivos de aprendizaje

- Simula las caminatas aleatorias 1D y 2D y verifica la escala de desplazamiento
  模拟一维和二维随机游走,验证位移的 √n 缩放规律 √n 缩放规律
- Construir un simulador de cadena de Markov y calcular su distribución estacionaria a través de la propia composición
  Construir un modelo de cadena de marcos, mediante características de descomposición calculada distribución plana
- Implementar la dinámica MCMC y Langevin de Metropolis-Hastings para la toma de muestras de las distribuciones objetivo
  实现 Metropolis-Hastings MCMC 和 Langevin 动力学, desde el objetivo de distribución en la
- Conecte el proceso de difusión hacia adelante al movimiento de Brownian y explique cómo el proceso inverso genera datos
  Relacionar el proceso de expansión hacia adelante con el movimiento de Browning, explicar cómo el proceso hacia atrás genera datos


> **【中文解读】**
> 随机过程是有结构的随机性――马尔可夫链(el estado actual depende sólo del paso anterior) es la base de PageRank。 el proceso anterior del modelo de propagación es el movimiento de browning(加噪), el proceso contrario es la generación de ruido。MCMC es la piedra angular de la estadística de abejas。

## El problema es la introducción del problema

Muchos sistemas de IA implican aleatoriedad que evoluciona con el tiempo, no aleatoriedad estática, aleatoriedad estructurada y secuencial donde cada paso depende de lo que pasó antes.

> Muchos sistemas de IA están involucrados en la casualidad de la evolución a lo largo del tiempo. No son casuales estáticos, sino que tienen una estructura, una secuencia de casualidad.

Los modelos de lenguaje generan tokens uno a la vez. Cada token depende del contexto anterior. El modelo saca una distribución de probabilidad, muestras de ella, y se mueve. Ese es un proceso estocástico.

> 语言模型逐个生成代币――每个代币取决于之前的上下文――模型输出一个概率分布,从中采样,然后继续――这是随机过程――

Los modelos de difusión añaden ruido a una imagen paso a paso hasta que se convierte en pura estática. Luego revertir el proceso, denonizando paso a paso hasta que surja una nueva imagen. El proceso hacia adelante es una cadena de Markov. El proceso inverso es una cadena de Markov aprendida que corre hacia atrás.

> El modelo de expansión es incrementar el ruido hasta que se vuelve puro estado estático. Luego, el proceso de reversión es incrementar el ruido hasta que surja una nueva imagen.

Los agentes de aprendizaje de refuerzo toman acciones en un entorno. Cada acción conduce a un nuevo estado con cierta probabilidad. El agente sigue una política aleatoria en un mundo aleatorio. Todo es un proceso de decisión de Markov.

> 强化学习智能体在环境中执行动作── cada movimiento con cierta probabilidad conduce a un nuevo estado──智能体在随机世界中遵循随机策略──整个系统是马尔可夫的决策过程──MDP)──

El muestreo MCMC - la columna vertebral de la inferencia bayesiana - construye una cadena de Markov cuya distribución estacionaria es la posterior de la que quieres tomar muestras.

> El MCMC 采采贝叶斯推理的基石 构建一个马尔可夫链, su distribución es la tasa estable que se espera de la distribución de la misma.

Todo esto se basa en cuatro ideas fundamentales:
1. Paseos aleatorios - el proceso estocástico más simple
2. Cadenas de Markov -- aleatoriedad estructurada con una matriz de transición
3. Dinámica de Langevin - Descenso de gradiente con ruido
4. Metropolis-Hastings -- muestreo de cualquier distribución

> Todos estos se basan en cuatro conceptos básicos: 1. 随机游走最简单随机过程; 2. 马尔可夫链带转移矩阵的结构化随机性; 3. 长文动力学带噪声梯度下降; 4.

## El concepto central.

### Paseos aleatorios

Comience en la posición 0. En cada paso, lanza una moneda justa. cabezas: mueve a la derecha (+1).

> Desde la posición 0 开始── cada paso lanzar una枚公平硬币──正面:向右 (+1)──反面:向左 (-1)──

Después de n pasos, su posición es la suma de n valores aleatorios +/-1. La posición esperada es 0 (el paseo es imparcial). Pero la distancia esperada del origen crece como sqrt(n).

> En el n 步后, tu posición es n 个随机 ±1 值的求和――期望位置为 0(游走无偏), pero la distancia de la espera del punto de partida es de √n 增长――

Esto es contrario a la intuición. La caminata es justa - no se deriva en ninguna dirección. Pero con el tiempo, vaga más y más lejos de donde comenzó. La desviación estándar después de n pasos es sqrt(n).

> Este tiene un punto contrario a la intuición. El camino es justo.

```
Step 0:  Position = 0
Step 1:  Position = +1 or -1
Step 2:  Position = +2, 0, or -2
...
Step 100: Expected distance from origin ~ 10 (sqrt(100))
Step 10000: Expected distance from origin ~ 100 (sqrt(10000))
```

**In 2D**La misma escala de cuadrados se aplica a la distancia desde el origen. La ruta rastrea un patrón similar a un fractal.

> **二维情况下**, y se desplaza a la misma probabilidad de movimiento ascendente, descendente, izquierdo, derecho, etc.

**Why sqrt(n)?**Cada paso es +1 o -1 con igual probabilidad. Después de n pasos, la posición S_n = X_1 + X_2 + ... + X_n donde cada X_i es +/-1. La varianza de cada paso es 1, y los pasos son independientes, por lo que Var(S_n) = n. Desviación estándar = sqrt(n).

> **为什么是 √n？**Cada paso de diferencia es 1, paso y paso independiente, por lo que Var(S_n) = n, estándar diferencial = √n。 por el centro de la limitación, S_n/√n 收到标准正态分布。

Esta escala de cuadrados se muestra en todas partes en ML. SGD escala el ruido como 1/sqrt(batch_size).

> √n 缩放在 ML 中无处不在──SGD 噪音按1/√(batch_size) 缩放,嵌入维度按√d 缩放──平方根是独立随机叠加的标志──

**Connection to Brownian motion.**Tomar un paseo aleatorio con el tamaño del paso 1/sqrt(n) y n pasos por unidad de tiempo. A medida que n va al infinito, el paseo converge al movimiento browniano B(t) - un proceso continuo en el tiempo donde B(t) se distribuye normalmente con la media 0 y la varianza t.

> **与布朗运动的联系。**取步长 1/√n、每单位时间 n 步的随机游走──当 n → ∞ 时,游走收到布朗运动 B(t) 一个连续时间过程,B(t) ~ N(0, t) ⋅

El movimiento browniano es la base matemática de la difusión. Modela el sacudimiento aleatorio de partículas en un fluido, las fluctuaciones de los precios de las acciones y, lo que es crucial, el proceso de ruido en los modelos de difusión.

> El movimiento de Brown es la base matemática del modelo de propagación. Describe el flujo de movimientos de partículas en el cuerpo, la variación del precio de las acciones, así como el proceso de ruido en el modelo de propagación.

**Gambler's ruin.**Un caminante aleatorio que comienza en la posición k, con barreras de absorción en 0 y N. ¿Cuál es la probabilidad de llegar a N antes de 0? Para un paseo justo: P(llegar a N) = k/N. Esto es sorprendentemente simple y elegante. Se conecta con la teoría de los martingales - el paseo aleatorio justo es un martingale (valor futuro esperado = valor actual).

> **赌徒破产问题。**Desde la posición k, en 0 y N, hay una absorción de la corriente.

### Las cadenas de Markov

Una cadena de Markov es un sistema que transiciona entre estados de acuerdo a probabilidades fijas. La propiedad clave: el siguiente estado depende sólo del estado actual, no de la historia.

> La cadena de Marco es un sistema de transferencia de probabilidad fija entre estados. La naturaleza central del siguiente estado depende únicamente del estado actual, sin relación con la historia.

```
P(X_{t+1} = j | X_t = i, X_{t-1} = ...) = P(X_{t+1} = j | X_t = i)
```

Esto es la propiedad de Markov. Significa que se puede describir toda la dinámica con una matriz de transición P:

> Esto es la naturaleza de la marmotalidad. Significa que puedes usar la matriz de movimiento P para describir todo el movimiento.

```
P[i][j] = probability of going from state i to state j
```

Cada fila de P suma a 1 (debes ir a algún lado).

> P de cada línea y para 1 (((tienes que ir a algún lugar)

**Example -- Weather:**

> **示例——天气：**

```
States: Sunny (0), Rainy (1), Cloudy (2)

P = [[0.7, 0.1, 0.2],    (if sunny: 70% sunny, 10% rainy, 20% cloudy)
     [0.3, 0.4, 0.3],    (if rainy: 30% sunny, 40% rainy, 30% cloudy)
     [0.4, 0.2, 0.4]]    (if cloudy: 40% sunny, 20% rainy, 40% cloudy)
```

Comienza en cualquier estado. Después de muchas transiciones, la distribución de estados converge a la distribución estacionaria pi, donde pi * P = pi. Este es el vector propio izquierdo de P con valor propio 1.

> Desde el estado arbitrario, después de haberse trasladado lo suficiente, la distribución de estado recibe a la distribución plana y estable de π, satisfizo π·P = π── es el valor de la característica de P para 1 de la característica de la velocidad de la velocidad.

Para la cadena meteorológica, la distribución estacionaria podría ser [0,53, 0,18, 0,29] -- a largo plazo, es soleado el 53% del tiempo independientemente del estado de inicio.
Para la cadena meteorológica, la distribución estacionaria es [0,55, 0,18, 0,27] -- a largo plazo, es soleado el 55% del tiempo independientemente del estado de inicio.

> Para la cadena meteorológica, la distribución estable es posible [0.53, 0.18, 0.29]La larga duración en vista del 53% del tiempo de la estación, sin relación con el estado de inicio.

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

**Computing the stationary distribution.**Hay dos enfoques:

1. **Power method**: multiplicar cualquier distribución inicial por P repetidamente. Después de suficientes iteraciones, converge.
2. **Eigenvalue method**: encontrar el vector propio izquierdo de P con valor propio 1. Este es el vector propio de P^T con valor propio 1.

> **计算平稳分布。**两种方法:1. **幂法**:反复用任意初始分布乘P,足足多次后收──2. **特征值法**: Buscar P de la característica de 1 de la característica izquierda de la velocidad de velocidad (es decir, P^T de la característica de la característica de 1 de la característica derecha de la velocidad de velocidad) ⋅

Ambos enfoques requieren que la cadena cumpla con las condiciones de convergencia.

> 两种方法都要求链满足收条件――

**Convergence conditions.**Una cadena de Markov converge a una distribución estacionaria única si es:
- **Irreducible**: cada estado es accesible desde cualquier otro estado
- **Aperiodic**: la cadena no se ejecuta con un período fijo

> **收敛条件。**La cadena de intercambio de datos de la red de datos de la red de intercambio de datos de la red de intercambio de datos de la red de intercambio de datos de la red de intercambio de datos de la red de intercambio de datos de la red de intercambio de datos de la red de intercambio de datos de la red de intercambio de datos de la red de intercambio de datos de la red de intercambio de datos de la red de intercambio de datos de la red de intercambio de datos de la red de intercambio de datos de intercambio de datos de la red de intercambio de datos de intercambio de datos de intercambio de datos de intercambio de datos de datos de la red de intercambio de datos de datos de intercambio de datos de datos de intercambio de datos de datos de datos de intercambio de datos de datos de datos de datos de la red de datos de intercambio de datos de datos de datos de datos de la red de datos de datos de datos de la red de datos de datos de datos de la red de datos de datos de datos de la red de datos de datos de datos de la red de datos de datos de datos de la red de datos de datos de datos de la red de datos de datos de datos de la red de datos de datos de datos de datos de la red de datos de datos de datos de datos de la red de datos de datos de datos de la red de datos de datos de datos de datos de datos de la red de datos de datos de datos de datos de la red de datos de datos de datos de la red de datos de datos de datos de Internet de Internet de Internet de Internet de Internet de Internet de Internet de Internet de Internet de Internet de Internet de Internet de Internet de de Internet de Internet de Internet de de de de Internet de Internet de de de de Internet de Internet de de de de Internet de es de Internet de Internet de de Internet de de Internet de de de de de de Internet de es de Internet de es de Internet de Internet de es de Internet de Internet de Internet de es de Internet de Internet de es de Internet de es es es.**不可约**(cada estado puede llegar desde otro estado);**非周期**(La cadena no se fijará en un ciclo de ciclo)

La mayoría de las cadenas que encuentras en ML cumplen ambas condiciones.

> La mayoría de las cadenas que encuentras en ML cumplen con estas dos condiciones.

**Absorbing states.**Un estado es absorbente si una vez que lo ingresas, nunca sales (P[i][i] = 1). Absorber cadenas de Markov modelos de procesos con estados terminales - un juego que termina, un cliente que se agita, una secuencia de tokens que golpea el token final del texto.

> **吸收状态。**Una vez que entra en un estado de incesante abandono, P[i][i]=1)── absorber el proceso de construcción de un sistema de marcos de marcos de marcos de marcos de marcos de marcos de marcos de marcos de marcos de marcos de marcos de marcos de marcos de marcos de marcos de marcos de marcos de marcos de marcos de marcos de marcos de marcos de marcos de marcos de marcos de marcos de marcos de marcos de marcos de marcos de marcos de marcos de marcos de marcos de marcos de marcos de marcos de marcos de marcos de marcos de marcos de marcos de marcos de marcos de marcos de marcos de marcos de marcos de marcos de marcos de marcos de marcos de marcos de marcos de marcos de marcos de marcos de marcos de marcos de marcos de marcos de marcos de marcos de marcos de marcos de marcos de marcos de marcos de marcos de marcos de marcos de marcos de marcos de marcos de marcos de marcos de marcos de marcos de marcos de marcos de marcos de marcos de marcos de marcos de marcos de marcos de marcos de marcos de marcos de marcos de marcos de marcos de marcos de marcos de marcos de marcos de marcos de marcos de marcos de marcos de marcos de marcos de marcos de marcos de marcos de marcos de marcos de marcos de marcos de marcos de marcos de marcos de marcos de marcos de marcos de marcos de marcos de marcos de marcos de marcos de marcos de marcos de marcos de marcos de marcos de marcos de marcos de marcos de marcos de marcos de marcos de marcos de marcos de marcos de marcos de marcos de marcos de marcos de marcos de marcos de marcos de marcos de marcos de marcos de marcos de marcos de marcos de marcos de marcos de marcos de marcos de marcos de marcos de marcos de marcos de marcos de marcos de marcos de marcos de

**Mixing time.**¿Cuántos pasos hasta que la cadena esté "cerca" de la distribución estacionaria? formalmente, el número de pasos hasta que la distancia total de variación de la estacionariedad caiga por debajo de algún umbral. mezcla rápida = pocos pasos necesarios. La brecha espectral de P (1 menos el segundo valor propio más grande) controla el tiempo de mezcla.

> **混合时间。**En forma, es la diferencia total de variación de la distribución plana que se reduce a los pasos siguientes a la valor.

### Conexión con modelos de idiomas

La generación de tokens en un modelo de lenguaje es aproximadamente un proceso de Markov. Dado el contexto actual, el modelo produce una distribución sobre el siguiente token.

> 语言模型的代币 生成近似是一个马尔可夫过程――给定当前上下文,模型输出下一个代币的概率分布――温度 控制分布的尖度:

```
P(token_i) = exp(logit_i / temperature) / sum(exp(logit_j / temperature))
```

- Temperatura = 1,0: distribución estándar
- Temperatura < 1,0: más nítida (más determinista)
- Temperatura > 1,0: más plana (más aleatoria)
- Temperatura -> 0: argmax (compulsivo)

> Temperatura=1.0 标准分布;<1.0 更尖(更确定性);>1.0 更平坦(更随机);→0 退化为 argmax(贪心解码)

El muestreo de top-k se reduce a los tokens de mayor probabilidad k. El muestreo de top-p (núcleo) se reduce al conjunto más pequeño de tokens cuya probabilidad acumulada excede p. Ambos modifican las probabilidades de transición de Markov.

> Top-k 采样保留概率最高的 k 个代币;Top-p(核采样) conservar acumulación概率超过 p 的最小代币集合──都修改了马可夫转移概率──

### Movimiento browniano

El límite de tiempo continuo de la marcha aleatoria. La posición B(t) tiene tres propiedades:
1. B(0) = 0
2. B(t) - B(s) se distribuye normalmente con la media 0 y la varianza t - s (para t > s)
3. Los incrementos en los intervalos no superpuestos son independientes

> 布朗运动是随机游走的连续时间极限──B(t) 有三条性质:B(0)=0;B(t) -B(s) ~ N(0, t-s);

El movimiento browniano es continuo pero en ninguna parte diferenciable, se tambalea en todas las escalas.

> El movimiento de Brown continúa pero en el mismo lugar es indíguo.

En simulación discreta, se aproxima el movimiento browniano por:

```
B(t + dt) = B(t) + sqrt(dt) * z,    where z ~ N(0, 1)
```

La escala de sqrt(dt) es importante. proviene del teorema de límite central aplicado a los paseos aleatorios.

> 离散仿真中中用 B(t+dt) = B(t) + √dt × z 近似布朗运动(z ~ N(0,1)) √dt 缩放很关键,源自随机游走的中心极限定理。

### Dinámica de Langevin

La dinámica de Langevin encuentra la distribución de probabilidades proporcional a exp(-U(x) /T), donde U es una función de energía y T es temperatura.

> 梯度下降找函数最小值──Langevin 动力学找概率分布  exp(-U(x) /T), entre los cuales U es la función de energía, T es temperatura──

```
x_{t+1} = x_t - dt * gradient(U(x_t)) + sqrt(2 * T * dt) * z_t
```

Dos fuerzas actúan sobre la partícula:
1. **Gradient force**(-dt * gradiente(U)): empuja hacia la baja energía (como la descensía de gradiente)
2. **Random force**(sqrt(2*T*dt) * z): empuja en direcciones aleatorias (exploración)

> 两种力作用在粒子上:1. **梯度力**推向低能量 (se parece a una baja energía); 2. **随机力**推向随机方向 (en español)

A temperatura T = 0, esto es un descenso de gradiente puro. A temperatura alta, es casi un paseo aleatorio. A la temperatura adecuada, la partícula explora el paisaje energético y pasa más tiempo en regiones de baja energía.

> La temperatura T=0 时是纯梯度下降──高温时近似随机游走──合适的温度下, las partículas exploran el paisaje energético y permanecen en la región de baja energía por más tiempo──

**Connection to diffusion models.**El proceso avanzado de un modelo de difusión es:

```
x_t = sqrt(alpha_t) * x_{t-1} + sqrt(1 - alpha_t) * noise
```

Esta es una cadena de Markov que mezcla gradualmente los datos con el ruido.

> 扩散模型的前向过程:x_t = √α_t × x_{t-1} + √(1-α_t) × ruido。 es una cadena de ruido de marcó que se mezcla gradualmente, suficiente paso después de x_T 变为纯高斯噪声。

El proceso inverso, pasar del ruido de vuelta a los datos, es también una cadena de Markov, pero sus probabilidades de transición son aprendidas por una red neuronal. La red aprende a predecir el ruido que se agregó en cada paso, y luego lo restará.

> El proceso inverso del ruido hacia el dato es también una cadena de marcos, pero la probabilidad de transferencia es determinada por el aprendizaje de la red neuronal.

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

### MCMC: Cadena de Markov Monte Carlo

A veces se necesita tomar una muestra de una distribución p ((x) que se puede evaluar (hasta una constante) pero no puede tomar una muestra directamente. los posteriores bayesianos son el ejemplo clásico - usted sabe la probabilidad veces el anterior, pero la constante normalizadora es intratable.

> Algunas veces necesitas una distribución que se puede calcular, pero la falta de la normalización no puede ser calculada directamente.

**Metropolis-Hastings**construye una cadena de Markov cuya distribución estacionaria es p(x):

1. Comience en alguna posición x
2. Proponer una nueva posición x' de una distribución de propuesta Q(x'
3. Ratio de aceptación de cálculo: a(x') * Q(x (x) = (x) = (x) * (x) * (x)
4. Acepta x' con probabilidad min ((1, a). de lo contrario permanezca en x.
5. Repito, ¿qué quieres?

> **Metropolis-Hastings**构建一个平稳分布为 p(x) 的马尔可夫链:1) 从某点 x 出发;2) 从提议分布 Q(x'就是x) 提出新位置 x';3) 计算接受率 a = p(x') Q(x'就是x') /((p(x) Q(x'就是x));4) 以概率 min(1,a) 接受,否则停留;5) 重复.

Si Q es simétrico, por ejemplo, Q(x' ( ( ( ( () ), = Q(x (x) ), la relación se simplifica a a = p(x') / p(x. Solo se necesita la relación de probabilidades - las constantes normalizadoras se cancelan.

> Si Q se abrevió a la norma (p) y la tasa de aceptación se simplificó a la norma (p) y la probabilidad se eliminó automáticamente, esto es la razón por la cual el MCMC es tan útil para la experiencia posterior de Bayesian.

La cadena está garantizada para converger a px en condiciones suaves. Pero la convergencia puede ser lenta si la propuesta es demasiado pequeña (caminar al azar) o demasiado grande (alto rechazo).

> En condiciones de temperatura bajo la cadena de garantía de la recepción de p  x) . Pero la recepción puede ser lenta                                                                                                                                                                                                                                                

**Why it works.**El coeficiente de aceptación garantiza el equilibrio detallado: la probabilidad de estar en x y moverse a x' es igual a la probabilidad de estar en x' y moverse a x. El equilibrio detallado implica que p(x) es la distribución estacionaria de la cadena.

> **为什么有效**La probabilidad de equilibrio de x a x es igual a la probabilidad de x a x. La probabilidad de equilibrio de x a x es igual a la probabilidad de x a x.

**Practical considerations:**
- **Burn-in**La cadena necesita tiempo para llegar a la distribución estacionaria desde su punto de partida.
- **Thinning**: mantener cada k-ta muestra para reducir la autocorrelación.
- **Multiple chains**Si convergen en la misma distribución, se tiene evidencia de convergencia.
- **Acceptance rate**En el caso de las propuestas gaussianas en dimensiones d, la tasa óptima de aceptación es de alrededor del 23% (Roberts & Rosenthal, 2001).

> ¿Qué es eso?**Burn-in**丢弃前 N 个样本(链需要时间到达平稳分布);**Thinning**Cada k 个样本取一个(降低自相关);**Multiple chains**Desde diferentes puntos de marcha de varias cadenas (si se recibe hasta la misma distribución, entonces hay pruebas de recepción);**Acceptance rate**La tasa de aceptación óptima de la propuesta de la Comisión de Asuntos Exteriores es de aproximadamente el 23%.

### Procesos estocásticos en IA

| Process | AI Application |
|---------|---------------|
| Random walk | Exploration in RL, Node2Vec embeddings |
| Markov chain | Text generation, MCMC sampling |
| Brownian motion | Diffusion models (forward process) |
| Langevin dynamics | Score-based generative models, SGLD |
| Markov decision process | Reinforcement learning |
| Metropolis-Hastings | Bayesian inference, posterior sampling |

> 随机过程在 AI 中的应用:随机游走:RL 探索、Node2Vec 嵌入) 、马尔可夫链 、文本生成、MCMC) 、布朗运动 、扩散模型前向) 、Langevin 动力学 、Score-based 模型、SGLD) 、马尔可夫决策过程 、强化学习) 、Metropolis-Hastings 、贝叶斯推理、后验采样) 、

## Construye y realiza.
```figure
random-walk-diffusion
```

## Construye el mismo

### Paso 1: Simulador de caminar aleatorio

> Paso 1: Con el movimiento de la máquina de simulación.

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

El paseo 1D almacena sumas acumuladas. Cada paso es +1 o -1. Después de n pasos, la posición es la suma. La varianza crece linealmente con n, por lo que la desviación estándar crece como sqrt(n).

> Un paso a paso en el proceso de almacenamiento de la información. Cada paso es +1 o -1.

### Paso 2: cadena de Markov

> Sección 2:                                                                                                                                                                                                                                                              

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

La distribución estacionaria es el propio vector izquierdo de P con valor propio 1. Lo encontramos mediante el cálculo de los propios vectores de P^T (transponer los propios vectores izquierdo en propios vectores derechosos).

> La distribución plana es el valor de la característica de P en 1 de la característica de P. Por medio de P^T se obtiene la característica de P.

### Paso 3: Dinámica de Langevin

> Paso 3: Langevin 动力学──梯度下降 + 高斯噪声 = explorar energía paisajística并采样──

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

El gradiente empuja x hacia la energía baja. El ruido evita que se atasque. En equilibrio, la distribución de las muestras es proporcional a exp(-U(x) / temperatura).

> 梯度把 x 推向低能量区, ruido evitar caer en la situación mejor.

### Paso 4: Metrópolis-Hastings

> Se trata de un sistema de cálculo de la cantidad de datos que se pueden obtener en el sistema de cálculo de la cantidad de datos que se pueden obtener en el sistema de cálculo de la cantidad de datos que se pueden obtener en el sistema de cálculo de datos.

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

El algoritmo propone un nuevo punto, verifica si tiene una probabilidad mayor (o acepta con probabilidad proporcional a la proporción) y repite.

> 算法流程:提议新点 → 检查概率是否更高 (或按比例接受)→ 重复.

## Usalo con el marco de ejecución

En la práctica, se utilizan bibliotecas establecidas para estos algoritmos, pero entender la mecánica es importante para el depuración y sintonización.

>  En realidad, se utilizan bases de datos para implementar estos algoritmos.

```python
import numpy as np

rng = np.random.RandomState(42)
walk = np.cumsum(rng.choice([-1, 1], size=10000))
print(f"Final position: {walk[-1]}")
print(f"Expected distance: {np.sqrt(10000):.1f}")
print(f"Actual distance: {abs(walk[-1])}")
```

> NumPy 实现随机游走:一行代码生成 10000 步 ±1 随机游走,验证实际距离与理论值 √10000 = 100 接近──

### Numpy para matrices de transición

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

> NumPy 处理转移矩阵: de [1,0,0] 出发,反复左乘 P 100 veces, automático recepción 到平稳分布──这是PageRank等算法的核心──

Multiplicar la distribución inicial por P repetidamente. Después de suficientes iteraciones, converge a la distribución estacionaria independientemente de dónde comenzó. Este es el método de potencia para encontrar el vector propio izquierdo dominante.

> La distribución inicial se repite por P. Suficiente cantidad de veces después, sin importar de dónde se empieza a recibir hasta la distribución plana.

### Conexiones con marcos reales

- **PyTorch diffusion:**El `DDPMScheduler`En el rostro abrazado`diffusers`Implementa las cadenas Markov hacia adelante y hacia atrás
- **NumPyro / PyMC:**Utilice MCMC (muestreo NUTS, que mejora en Metropolis-Hastings) para la inferencia bayesiana
- **Gymnasium (RL):**La función de paso medio ambiente define un proceso de decisión de Markov

> Enlace con el verdadero marco:`diffusers`El DDPMS programador logró la cadena de marcóffice de un modelo de expansión hacia adelante/en contra;NumPyro/PyMC con NUTS 采样器 (la versión mejorada de Metropolis-Hastings) para hacer una hipótesis de base;La función de paso del gimnasio definió el proceso de decisión de Marcóffice.

### Verificación de la convergencia de la cadena de Markov

```python
import numpy as np

P = np.array([[0.9, 0.1], [0.3, 0.7]])

eigenvalues = np.linalg.eigvals(P)
spectral_gap = 1 - sorted(np.abs(eigenvalues))[-2]
print(f"Eigenvalues: {eigenvalues}")
print(f"Spectral gap: {spectral_gap:.4f}")
print(f"Approximate mixing time: {1/spectral_gap:.1f} steps")
```

La brecha espectral le dice a qué tan rápido la cadena olvida su estado inicial. Una brecha de 0.2 significa aproximadamente 5 pasos para mezclar. Una brecha de 0.01 significa aproximadamente 100 pasos. Siempre compruebe esto antes de ejecutar simulaciones largas - un cálculo de residuos de cadena mezclar lentamente.

> 谱隙告诉你链多快忘初状态――0.2 间隙大约需要5步混合;0.01 大约需要100步――运行长仿真前总要检查这个慢混合的链浪费算力――

## Envíe el producto .

Esta lección produce:
- `outputs/prompt-stochastic-process-advisor.md`-- un prompt que ayuda a identificar qué marco de proceso estocástico se aplica a un problema dado

> Este curso se desarrolla en el campo de la información y de la información.

## Conexiones conceptos relacionados mapa

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

> 概念关联:随机游走(Node2Vec、RL 探索)、马尔可夫链(LLM token 生成、MCMC)、布朗运动) (DDPM 前向过程)、Langevin 动力学(Score-based 模型、SGLD)、平稳分布(MCMC 收目标、PageRank)、Metropolis-Hastings(贝叶斯后验、模拟退火)、Temperatura(LLM 采样、Boltzmann 探索)、Mixing time(MCMC 收速度)、Absorbing state(序列结束、RL 终止状态)、Detallada balance 证券(MCMC 采样器的正确性保证)、

Los modelos de difusión merecen una atención especial.

```
q(x_t | x_{t-1}) = N(x_t; sqrt(1-beta_t) * x_{t-1}, beta_t * I)
```

donde beta_t es un cronograma de ruido. Después de T pasos, x_T es aproximadamente N(0, I). El proceso inverso es parametrizado por una red neuronal que predice el ruido:

```
p_theta(x_{t-1} | x_t) = N(x_{t-1}; mu_theta(x_t, t), sigma_t^2 * I)
```

Cada paso de generación es un paso en una cadena de Markov aprendida.

SGLD (Dynamics de Langevin de Gradiente Stocástico) combina la baja de gradiente de mini lote con el ruido de Langevin. En lugar de calcular el gradiente completo, se usa una estimación estocástica y se añade ruido calibrado. A medida que la tasa de aprendizaje disminuye, SGLD pasa de la optimización a la muestreo -- obtienes muestras posteriores bayesianas aproximadas de forma gratuita. Esta es una de las formas más simples de obtener estimaciones de incertidumbre de una red neuronal.

La clave de todas estas conexiones: los procesos estocásticos no son solo herramientas teóricas. Son los mecanismos computacionales dentro de los sistemas modernos de IA. Cuando ajustes la temperatura de un LLM, estás ajustando una cadena de Markov. Cuando entrenas un modelo de difusión, estás aprendiendo a revertir un proceso similar al movimiento browniano. Cuando ejecutas la inferencia bayesiana, estás construyendo una cadena que converge a la posterior.

> Caminando por todos estos vínculos, el proceso de paso no es sólo un instrumento teórico, sino un mecanismo de cálculo interno de la IA moderna.  Cuando ajustes la temperatura del LLM, estás ajustando la cadena de la marca; cuando entrenas el modelo de expansión, estás aprendiendo el proceso de cambio de diseño; cuando ejecutas la teoría de Bayes, estás construyendo la cadena de la recepción hasta la última experiencia.

## Los ejercicios.

1. **Simulate 1000 random walks of 10000 steps.**Traza la distribución de las posiciones finales. Verifique que es aproximadamente gaussiano con media 0 y desviación estándar sqrt(10000) = 100.

2. **Build a text generator using a Markov chain.**Entrenamiento en un corpus pequeño: para cada palabra, contar las transiciones a la siguiente palabra. Construir la matriz de transición. Generar nuevas frases mediante muestreo de la cadena.

3. **Implement simulated annealing**El método de cálculo de la función de un mínimo de función con muchos mínimos locales es el método de cálculo de la función de una función de un mínimo de función con una función de una función de mayor temperatura.

4. **Compare Langevin dynamics at different temperatures.**Muestra de un potencial de pozo doble U(x) = (x^2 - 1)^2. a baja temperatura, las muestras se agrupan en un pozo. a alta temperatura, se propagan a través de ambos.

5. **Implement the forward diffusion process.**Comience con una señal 1D (por ejemplo, una onda seno). Agregue el ruido progresivamente más de 100 pasos con un cronograma de ruido lineal. Muestre cómo la señal se degrada a ruido puro. Luego implemente un simple denoizador que invierte el proceso (incluso uno ingenuo que solo restará el ruido estimado).

## Términos clave .

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

> 术语速查:Random walk (随机游走) ‧Markov property ([[no memoria]]) ‧Transition matrix ([[转移矩阵]] P[i][j]) ‧Estacionario distribución ([[plane distribution]] π·P=π) ‧Brownian motion ([[Brownian motion]] ‧布朗运动 ([[Brownian motion]]) ‧N ([[N]] ]] ]] ‧Langevin dynamics ([[带噪声的梯度下降]] ‧MCMC]] ‧Construcción de distribución (平稳分布) ‧Málkova 链) ‧Metropolis-Hastings ([[Temporada]] ‧Temporada]] ‧Exploración/Utilización de la equilibrio ‧MCM }} ‧Difusión ([[pre-加噪]] ‧反-向去噪生成数据) ‧) ‧

## Más Leer más Leer más

- **Ho, Jain, Abbeel (2020)**-- "Deniendo los modelos probabilísticos de difusión". El documento del DDPM que lanzó la revolución del modelo de difusión.
- **Song & Ermon (2019)**-- "Modelado generacional mediante la estimación de gradientes de la distribución de datos". Un enfoque basado en puntajes utilizando dinámica Langevin para muestreo.
- **Roberts & Rosenthal (2004)**"Cadenas generales de estado espacial Markov y algoritmos MCMC". La teoría detrás de cuándo y por qué funciona MCMC.
- **Norris (1997)**- "Cadenas de Markov". El libro de texto estándar.
- **Welling & Teh (2011)**-- "Aprendizaje bayesiano a través de la Dinámica de Langevin Gradiente Estocástico". Combina SGD con la Dinámica de Langevin para la inferencia bayesiana escalable.
