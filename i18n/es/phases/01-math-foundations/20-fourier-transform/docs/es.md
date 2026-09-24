# La transformación de Fourier se ha cambiado.

> Cada señal es una suma de ondas senoides. La transformación de Fourier le dice cuáles son.
> Cada señal es una superposición de la onda de los cuerpos.

**Type:** Build | **类型:** 动手
**Language:**¿ Qué pasa ?**语言:**Python
**Prerequisites:** Phase 1, Lessons 01-04, 19 (complex numbers) | **前置知识:** Phase 1, 第 01-04 课、第 19 课（复数）
**Time:** ~90 minutes | **时间:** ~90 分钟

## Objetivos de aprendizaje

- Implementar el DFT desde cero y verificarlo con respecto al O(N registro N) Cooley-Tukey FFT
  Desde el zero de la realización de DFT y con O(N log N) de Cooley-Tukey FFT 验证
- Interpreta los coeficientes de frecuencia: extrae amplitud, fase y espectro de potencia de una señal
  解释频率系数: de la señal entre提取幅度、相位和功率谱(Espectro de potencia)
- Aplicar el teorema de la convolución para realizar la convolución a través de la multiplicación FFT
  应用卷积定理 通过 FFT 乘法执行卷积
- Conectar la descomposición de frecuencia de Fourier a las codificaciones posicionales de transformador y las capas de convolución de CNN
  Codificación de la posición y la red de revólveres de CNN


> **【中文解读】**
>  cualquier señal puede ser dividida en la línea de cuerdas                                                                                                                                                                                                                                                         

## El problema es la introducción del problema

Una grabación de audio es una secuencia de mediciones de presión a lo largo del tiempo. Un precio de acciones es una secuencia de valores a lo largo de días. Una imagen es una cuadrícula de intensidades de píxeles sobre el espacio. Todos estos son datos en el dominio del tiempo (o dominio del espacio).

> 音频录制 (音频录制) es una serie de medidas de presión que cambian con el tiempo. El precio de las acciones es una serie de valores que cambian con el tiempo. La imagen es una red de intensidad de la imagen en el espacio.

Pero muchos patrones son invisibles en el dominio del tiempo. ¿Es este señal de audio un tono puro o un acorde? ¿Tiene este precio de las acciones un ciclo semanal? ¿Tiene esta imagen una textura repetitiva? Estas preguntas son sobre el contenido de frecuencia, y el dominio del tiempo lo oculta.

> Pero muchos patrones en el tiempo son invisibles. ¿Es el audio de la señal sonora o sonora? ¿Tiene el precio de la acción un ciclo de semana? ¿Tiene la imagen una estructura repetitiva?

La transformación de Fourier convierte datos del dominio del tiempo al dominio de la frecuencia. Toma una señal y la descompone en ondas senoides de diferentes frecuencias. Cada onda senoide tiene una amplitud (qué tan fuerte es) y una fase (donde comienza).

> 里叶变换将数据从时域转换到频域── recibe una señal y se descompone en diferentes frecuencias de los movimientos de los cuerpos de la línea de un solo cuadro. Cada una de las líneas de la línea de un solo cuadro tiene amplitud y fase.

Esto es importante para ML porque el pensamiento del dominio de frecuencia aparece en todas partes. Las redes neuronales convolucionales realizan la convolución, que es la multiplicación en el dominio de frecuencia. Los codificadores de posición de transformadores utilizan la descomposición de frecuencia para representar la posición. Los modelos de audio (reconocimiento de voz, generación de música) operan en espectrogramas - representaciones de frecuencia del sonido. Los modelos de series temporales buscan patrones periódicos. Comprender la transformación de Fourier le da el vocabulario para trabajar con todos estos.

> Esto es importante para el ML, ya que el dominio de la reflexión está inexpreso. El volumen de la red de la ejecución de la secuencia de tiempo es multiplicado. El modelo de la secuencia de tiempo busca un modelo periódico.

## El concepto central.

> **【中文解读】**
> 里叶变换的核心思想: cualquier señal puede ser desglosada en diferentes frecuencias de la cuerda y de la onda. DFT Colocar el señal de tiempo en un número de frecuencias. Cada número le dice "esta frecuencia tiene mucha energía".

> **【拓展：FFT 的计算影响力】**
> FFT es considerado uno de los algoritmos de valores numéricos más importantes del siglo XX. Gauss descubrió la estrategia de separación en 1805, pero Cooley-Tukey en su trabajo de 1965 sólo hizo que FFT se aplicara ampliamente. Hoy en día, cada vez que se utiliza el 4G / LTE, cada JPEG 照片、 cada MP3 canciones han pasado por el tratamiento de FFT. En el campo de la IA, el modelo de voz de susurro calcula aproximadamente 100 veces el tiempo de FFT por segundo, el tubo de tratamiento de imágenes de difusión estable también utiliza una gran cantidad de operaciones de dominio de frecuencia.

### La definición de DFT

Dadas N muestras x[0], x[1], ..., x[N-1], la Transforma de Fourier Discreta produce N coeficientes de frecuencia X[0], X[1], ..., X[N-1]:

> 给定 N 个样本 x[0], x[1], ..., x[N-1],离散里叶变换产生 N 个频率系数 X[0], X[1], ..., X[N-1]:

```
X[k] = sum_{n=0}^{N-1} x[n] * e^(-2*pi*i*k*n/N)

for k = 0, 1, ..., N-1
```

Cada X[k] es un número complejo. Su magnitud. X[k] destiene la amplitud de la frecuencia k. Su ángulo de fase ((X[k]) le dice la compensación de fase de esa frecuencia.

> Cada X[k] es el número de veces. El X[k] es el número de veces. El X[k] es el número de veces.

La clave de la información:`e^(-2*pi*i*k*n/N)`es un faseor rotativo en la frecuencia k. El DFT calcula la correlación entre la señal y cada una de las frecuencias de N espaciadas igualmente. Si la señal contiene energía en la frecuencia k, la correlación es grande.

> 关键洞察:`e^(-2*pi*i*k*n/N)`Es la frecuencia de la frecuencia de la frecuencia k de la cantidad de rotación.

### Lo que significa cada coeficiente

**X[0]: the DC component.**Esta es la suma de todas las muestras, proporcional a la media. Representa la constante (de frecuencia cero) de la señal.

> **X[0]：直流分量（DC Component）。**Es el total de todas las muestras y el valor medio en proporción correcta.

```
X[0] = sum_{n=0}^{N-1} x[n] * e^0 = sum of all samples
```

**X[k] for 1 <= k <= N/2: positive frequencies.**X[k] representa los ciclos de frecuencia k por muestras N. Un k más alto significa una frecuencia más alta (oscillación más rápida).

> **X[k]（1 <= k <= N/2）：正频率。**X[k] 代表每 N 个样本中 k 个周期的频率──k 越大频率越高(振荡越快)──

**X[N/2]: the Nyquist frequency.**La frecuencia más alta que se puede representar con muestras N. Por encima de esto, se obtiene alias -- frecuencias altas disfrazadas de bajas.

> **X[N/2]：Nyquist 频率。**Usando N 个样本能表示的最高频率──超过此频率会产生混叠高频伪装成低频──

**X[k] for N/2 < k < N: negative frequencies.**Para señales de valor real, X[N-k] = conj(X[k]). Las frecuencias negativas son imágenes especulares de las positivas.

> **X[k]（N/2 < k < N）：负频率。**对于实值信号,X[N-k] = conj(X[k])。负频率是正频率的镜像──这就是为什么有用信息在前N/2 + 1 系数中──

### DFT inverso

El DFT inverso reconstruye la señal original a partir de sus coeficientes de frecuencia:

```
x[n] = (1/N) * sum_{k=0}^{N-1} X[k] * e^(2*pi*i*k*n/N)

for n = 0, 1, ..., N-1
```

Las únicas diferencias con respecto al DFT delantero: el signo en el exponente es positivo (no negativo), y hay un factor de normalización 1/N.

> La única diferencia entre el DFT y el DFT es que el índice es positivo (non negativo), y tiene un factor de reintegración de 1/N.

La DFT inversa es una reconstrucción perfecta. No se pierde información. Puedes pasar de dominio de tiempo a dominio de frecuencia y de vuelta sin ningún error. La DFT es un cambio de base - reexpresa la misma información en un sistema de coordenadas diferente.

> En cambio, la DFT es una reconstrucción perfecta. No hay información perdida. Puedes volver de un dominio temporal a otro de la frecuencia, sin ningún error.

### El FFT: hacerlo rápido

El DFT definido anteriormente es O(N^2): para cada uno de los coeficientes de salida N, sumamos sobre muestras de entrada N. Para N = 1 millón, es 10^12 operaciones.

> Para N = 100.000, es 10^12 veces el cálculo.

La transformación de Fourier rápida (FFT) calcula el mismo resultado en O  N log N. Para N = 1 millón, eso es aproximadamente 20 millones de operaciones en lugar de un billón. Esto es lo que hace que el análisis de frecuencia sea práctico.

> 快速里叶变换(FFT) con O(N log N) 计算相同的结果──对于N = 100,000,000,大约是20000000次运算而不是1000000次──这就是使频率分析变得可行的原因──

> **【中文解读】**
> La cantidad de cálculo de DFT es O(N^2), pero FFT 通过分治策略把它降低到O(N log N) ⋅ Para la señal de N=100 millones, DFT 需要万次运算, FFT 需要约2000 millones de veces 加速5万倍!秘是把信号按奇偶下标分成两半,递归计算后再使用"旋转因子"合并──这要求信号长度是2的──

El algoritmo Cooley-Tukey (el FFT más común) funciona dividido y conquistado:

> Cooley-Tukey 算法 (FFT) más habitual (Divide and Conquer)

1. Dividir la señal en muestras de índice par y impar.
   Se dividirá la señal en ejemplos de índice de números impares y índice de números raros.
2. Calcule el DFT de cada mitad de forma recursiva.
   递归计算每一半的 DFT──
3. Combine las dos DFT de medio tamaño utilizando "factores de doble" e^(-2*pi*i*k/N).
   Uso de "旋转因子" (twice factor) e^(-2*pi*i*k/N) 合并两个半尺寸的DFT──

```
X[k] = E[k] + e^(-2*pi*i*k/N) * O[k]          for k = 0, ..., N/2 - 1
X[k + N/2] = E[k] - e^(-2*pi*i*k/N) * O[k]    for k = 0, ..., N/2 - 1

where E = DFT of even-indexed samples
      O = DFT of odd-indexed samples
```

La simetría significa que cada nivel de recursión funciona O(N), y hay niveles log2(N. Total: O(N log N).

> 对称性 significa cada nivel de regreso a hacer O (N) 工作,共享 log2 (N) 层――总计:O (N) log N) ⋅

```mermaid
graph TD
    subgraph "8-point FFT (Cooley-Tukey)"
        X["x[0..7]<br/>8 samples"] -->|"split even/odd"| E["Even: x[0,2,4,6]"]
        X -->|"split even/odd"| O["Odd: x[1,3,5,7]"]
        E -->|"4-pt FFT"| EK["E[0..3]"]
        O -->|"4-pt FFT"| OK["O[0..3]"]
        EK -->|"combine with twiddle factors"| XK["X[0..7]"]
        OK -->|"combine with twiddle factors"| XK
    end
    subgraph "Complexity"
        C1["DFT: O(N^2) = 64 multiplications"]
        C2["FFT: O(N log N) = 24 multiplications"]
    end
```

El FFT requiere que la longitud de la señal sea de 2 potencia. En la práctica, las señales se empalan a cero a la siguiente potencia de 2.

### Análisis espectral

El **power spectrum**Es X [k] cuadrado - la magnitud cuadrada de cada coeficiente de frecuencia.

El **phase spectrum**es ángulo ((X[k]) -- la fase de compensación de cada frecuencia. Para la mayoría de las tareas de análisis, se preocupa por el espectro de potencia e ignora la fase.

```
Power at frequency k:  P[k] = |X[k]|^2 = X[k].real^2 + X[k].imag^2
Phase at frequency k:  phi[k] = atan2(X[k].imag, X[k].real)
```

### Resolución de frecuencia

La resolución de frecuencia del DFT depende del número de muestras N y de la tasa de muestreo fs.

```
Frequency of bin k:      f_k = k * fs / N
Frequency resolution:    delta_f = fs / N
Maximum frequency:       f_max = fs / 2  (Nyquist)
```

Para resolver dos frecuencias que están cerca de uno a otro, se necesitan más muestras. Para capturar frecuencias altas, se necesita una tasa de muestreo más alta.

### El teorema de la convolución

Este es uno de los resultados más importantes en el procesamiento de señales y directamente relevante para las CNN.

> Este es uno de los resultados más importantes en el procesamiento de señales, directamente relacionado con CNN.

**Convolution in the time domain equals pointwise multiplication in the frequency domain.**

> **时域中的卷积等于频域中的逐点相乘。**

```
x * h = IFFT(FFT(x) . FFT(h))

where * is convolution and . is element-wise multiplication
```

Por qué esto es importante:

- La convolución directa de dos señales de longitud N y M realiza operaciones O(N*M).
  两个长度为 N 和 M 的信号直接卷积需要 O(N*M) 次运算──
- La convolución basada en FFT toma O(N log N): transforma ambos, multiplica, transforma de nuevo.
  基于 FFT的卷积需要 O(N log N):变换两个信号、相乘、逆变换。
- Para núcleos grandes, la convolución FFT es dramáticamente más rápida.
  Para el gran volumen de energía, el FFT 卷积快得多.
- Esto es exactamente lo que sucede en las capas convolutivas con grandes campos receptivos.
  Esto es lo que ocurre en el ámbito de la gran sensibilidad.

> **【拓展：卷积定理在 CNN 中的实际应用】**
> 標準的3x3卷积直接计算比FFT 快,但当感受野变大时FFT 优势显现──ConvNeXt 和 Global Convolution 网络在7x7或更大的卷积中使用FFT 加速──FNet (Lee-Thorp et al., 2021) 更大胆地使用FFT 替代变压器的自注意,在GLUE基准上达到 92% de BERT 精度,但训练速度快7 倍──频域复制的杂度是O(N) 而时域卷积是O(N^2)。

Nota: el DFT calcula la convolución circular (la señal se envuelve). Para la convolución lineal (sin envoltura), cero-pad ambas señales a longitud N + M - 1 antes de la computación.

> Nota:DFT  calcular es un ciclo de volumen 信号会环绕) ・・・对于线性卷积 无环绕), en el cálculo anterior se completarán dos señales hasta la longitud N + M - 1 ・・・

```mermaid
graph LR
    subgraph "Time Domain"
        TA["Signal x[n]"] -->|"convolve (slow: O(NM))"| TC["Output y[n]"]
        TB["Filter h[n]"] -->|"convolve"| TC
    end
    subgraph "Frequency Domain"
        FA["FFT(x)"] -->|"multiply (fast: O(N))"| FC["FFT(x) * FFT(h)"]
        FB["FFT(h)"] -->|"multiply"| FC
        FC -->|"IFFT"| FD["y[n]"]
    end
    TA -.->|"FFT"| FA
    TB -.->|"FFT"| FB
    FD -.->|"same result"| TC
```

### Las ventanas

El DFT asume que la señal es periódica - trata las muestras N como un período de una señal infinitamente repetida. Si la señal no comienza y termina en el mismo valor, esto crea una discontinuidad en el límite, que aparece como contenido de alta frecuencia falso. Esto se llama fuga espectral.

> DFT 假设信号是周期的它将N个样本视为无限重复信号的一个周期――如果信号不在相同的值处开始和结束,边界处会产生不连续性,表现为虚假的高频内容――这称为频谱泄漏(Spectral Leakage) ――

La ventana reduce la fuga reduciendo la señal a cero en ambos extremos antes de calcular el DFT.

> 窗函数(Windowwing) a través de la calculación de DFT 之前, los dos extremos de la señal disminuirán gradualmente hasta el cero para reducir las fugas.

Ventanas comunes:

| Window | Shape | Main lobe width | Side lobe level | Use case |
|--------|-------|----------------|-----------------|----------|
| Rectangular | Flat (no window) | Narrowest | Highest (-13 dB) | When signal is exactly periodic in N samples |
| Hann | Raised cosine | Moderate | Low (-31 dB) | General purpose spectral analysis |
| Hamming | Modified cosine | Moderate | Lower (-42 dB) | Audio processing, speech analysis |
| Blackman | Triple cosine | Wide | Very low (-58 dB) | When side lobe suppression is critical |

```
Hann window:    w[n] = 0.5 * (1 - cos(2*pi*n / (N-1)))
Hamming window: w[n] = 0.54 - 0.46 * cos(2*pi*n / (N-1))
```

Aplique la ventana multiplicándola por elemento con la señal anterior al DFT: `X = DFT(x * w)`¿ Qué ?

### Propiedades de DFT

| Property | Time Domain | Frequency Domain |
|----------|-------------|-----------------|
| Linearity | a*x + b*y | a*X + b*Y |
| Time shift | x[n - k] | X[f] * e^(-2*pi*i*f*k/N) |
| Frequency shift | x[n] * e^(2*pi*i*f0*n/N) | X[f - f0] |
| Convolution | x * h | X * H (pointwise) |
| Multiplication | x * h (pointwise) | X * H (circular convolution, scaled by 1/N) |
| Parseval's theorem | sum \|x[n]\|^2 | (1/N) * sum \|X[k]\|^2 |
| Conjugate symmetry (real input) | x[n] real | X[k] = conj(X[N-k]) |

El teorema de Parseval dice que la energía total es la misma en ambos dominios.

> La teoría de la parseval 定理说明 dos dominios tienen la misma energía.

### Conexión a codificaciones posicionales

El Transformer original utiliza codificaciones posicionales sinusoidales:

```
PE(pos, 2i)   = sin(pos / 10000^(2i/d_model))
PE(pos, 2i+1) = cos(pos / 10000^(2i/d_model))
```

Cada par de dimensiones (2i, 2i+1) oscila a una frecuencia diferente. Las frecuencias están espaciadas geométricamente desde las altas (dimensión 0,1) hasta las bajas (última dimensión). Esto da a cada posición un patrón único en todas las bandas de frecuencia, similar a cómo los coeficientes de Fourier identifican de forma única una señal.

> Cada dimensión se compara con (2i, 2i+1) con diferentes frecuencias de oscilación. La frecuencia de alta (dimensión 0,1) a baja (dimensión final) se presenta a través de intervalos de tiempo.

Las propiedades clave que proporciona:

- **Uniqueness:**No hay dos posiciones que tengan la misma codificación.
  **唯一性：**No hay dos posiciones con el mismo código.
- **Bounded values:**El pecado y el cos están siempre en [-1, 1].
  **有界值：**Sin 和 cos 始终在 [-1, 1] 中──
- **Relative position:**La codificación de la posición p+k se puede expresar como una función lineal de la codificación en la posición p. El modelo puede aprender a atender a posiciones relativas.
  **相对位置：**位置 p+k 编码可以表示为位置 p 编码的线性函数──模型可以学习关注相对位置──

### Conexión con las CNN

Una capa de convolución aplica un filtro aprendido (núcleo) a la entrada deslizándolo a través de la señal o la imagen.

> En matemáticas, esto es el cálculo de la cantidad de volúmenes.

Por el teorema de la convolución, esto es equivalente a:
1. FFT la entrada
   FFT 输入
2. FFT el núcleo
   FFT 卷积核
3. Multiplicar en el dominio de frecuencia
   En el campo de la frecuencia
4. Si el resultado es
   IFFT  resultados

Las implementaciones estándar de CNN utilizan la convolución directa (más rápida para pequeños núcleos 3x3). Pero para núcleos grandes o convolución global, los enfoques basados en FFT son significativamente más rápidos. Algunas arquitecturas (como FNet) reemplazan la atención por completo con FFT, logrando precisión competitiva con O(N log N) en lugar de complejidad O(N^2).

> 标准 CNN 实现使用直接卷积 (小的3x3卷积核更快) ⋅ pero para el gran卷积核或全局卷积, basado en el método de FFT es significativamente más rápido. Algunas estructuras (como FNet) utilizan completamente el FFT 替代注意力, con O  N log N) y no O  N ⋅ N2) para alcanzar la complejidad de la competencia.

### Espectogramas y la transformación de Fourier de corto plazo

Una sola FFT le da el contenido de frecuencia de toda la señal, pero no le dice nada sobre cuándo ocurren esas frecuencias.

> 单次 FFT 给你整个信号的频率内容, pero no te dice cuándo aparecen estas frecuencias. 信号频率随着时间的增加信号) 和和弦频率同时出现) pueden tener la misma amplitud.

La Transforma de Fourier de Tiempo Corto (STFT) resuelve esto calculando FFTs en ventanas superpuestas de la señal. El resultado es un espectrograma: una representación 2D con tiempo en un eje y frecuencia en el otro. La intensidad en cada punto muestra la energía en esa frecuencia en ese momento.

> 短时里叶变换(STFT) calcula FFT para resolver este problema a través de la ventana de superposición de la señal. El resultado es un gráfico de frecuencias: una en tiempo para un eje, la frecuencia para otro eje, es una expresión 2D de la intensidad de cada punto que muestra la frecuencia en el tiempo en ese tiempo.

```
STFT procedure:
1. Choose a window size (e.g., 1024 samples)
2. Choose a hop size (e.g., 256 samples -- 75% overlap)
3. For each window position:
   a. Extract the windowed segment
   b. Apply a Hann/Hamming window
   c. Compute FFT
   d. Store the magnitude spectrum as one column of the spectrogram
```

Los espectrogramas son la representación de entrada estándar para los modelos de audio ML. Los modelos de reconocimiento de voz (Whisper, DeepSpeech) operan en espectrogramas mel - espectrogramas con frecuencias mapeadas a la escala mel, que se ajusta mejor a la percepción de tono humano.

> 频谱图是音频ML 模型的标准输入表示──语音识别模型(Whisper、DeepSpeech) en el Mel-Spectrogram 频谱图 (Mel-Spectrogram) 频率映射到梅尔刻度的频谱图, mejor se ajusta al sonido humano.

> **【中文解读】**
> 单次 FFT sólo puede ver la frecuencia de la estructura de la señal entera, pero no sabe cada frecuencia en "qué momento" aparece. 短时里叶变换(STFT) a través de la ventana de rodaje se resuelve este problema: hacer FFT por separado en cada sección de la ventana, obtener tres dimensiones de tiempo-frecuencia-energía.

### Alfabetización

Si una señal contiene frecuencias superiores a fs/2 (la frecuencia de Nyquist), la muestreo a la frecuencia fs creará copias alias. Una señal de 90 Hz muestrada a 100 Hz se ve idéntica a una señal de 10 Hz. No hay manera de distinguirlos de las muestras por sí solas.

> Si el señal contiene una frecuencia superior a fs/2 (frecuencia de Nyquist), se producen dos copias de mezcla en la velocidad de fs 采样.

```
Example:
  True signal: 90 Hz sine wave
  Sampling rate: 100 Hz
  Apparent frequency: 100 - 90 = 10 Hz

  The samples from the 90 Hz signal at 100 Hz sampling rate
  are identical to the samples from a 10 Hz signal.
  No amount of math can recover the original 90 Hz.
```

Es por eso que los convertidores analógicos a digitales incluyen filtros antialiasing que eliminan las frecuencias por encima de Nyquist antes de la muestreo. En ML, el aliasing aparece cuando se muestran los mapas de características sin filtración de bajo paso adecuada.

> Es por eso que los transformadores de módulos contienen un transbordador de ondas anti-confusión, que elimina la frecuencia de Nyquist antes de la toma de muestras. En el ML, cuando no hay una carga de onda baja adecuada, se producen algunas estructuras con una capa de acumulación de ondas anti-confusión para resolver este problema.

### El empolvimiento cero no aumenta la resolución

Un error común: empolvar cero una señal antes de que FFT mejore la resolución de frecuencia. No lo hace. empolvar cero interpola entre los contenedores de frecuencia existentes, lo que le da un espectro más liso. Pero no puede revelar detalles de frecuencia que no estaban presentes en las muestras originales.

> 常见误解: antes de FFT 补零 puede mejorar la resolución de frecuencia. En realidad no puede. 补零 entre los binos de frecuencia existentes, le da una apariencia de espectro más suave.

La resolución de frecuencia verdadera depende sólo del tiempo de observación T = N / fs. Para resolver dos frecuencias separadas por delta_f, se necesita al menos T = 1 / delta_f segundos de datos. Ninguna cantidad de empate cero cambia este límite fundamental.

> La verdadera frecuencia de resolución sólo depende del tiempo de observación T = N / fs. Para resolver las dos frecuencias de separación delta_f, al menos se necesita datos de T = 1 / delta_f 秒.

> **【拓展：频谱图在语音 AI 中的标准地位】**
> OpenAI Whisper 模型将音频转换为 log-Mel 频谱图后输入编码器──Mel 刻度模拟人耳对频率的感知(低频区分更细)──Whisper utiliza 80 个 Mel 波器组、25ms 窗口、10ms 步长──一段 30 segundos de audio produce alrededor de 3000 x 80 de la matriz de la frecuencia──Google's WaveNet、Meta's EnCodec también se utiliza en la frecuencia gráfica o el dominio de la frecuencia para representar las características intermedias──

## Construye y realiza.
```figure
fourier-synthesis
```

## Construye el mismo

### Paso 1: DFT desde cero

La DFT O ((N^2) se sigue directamente de la definición.

```python
import math

class Complex:
    ...

def dft(x):
    N = len(x)
    result = []
    for k in range(N):
        total = Complex(0, 0)
        for n in range(N):
            angle = -2 * math.pi * k * n / N
            w = Complex(math.cos(angle), math.sin(angle))
            xn = x[n] if isinstance(x[n], Complex) else Complex(x[n])
            total = total + xn * w
        result.append(total)
    return result
```

### Paso 2: DFT inverso

La misma estructura, exponente positivo, dividido por N.

```python
def idft(X):
    N = len(X)
    result = []
    for n in range(N):
        total = Complex(0, 0)
        for k in range(N):
            angle = 2 * math.pi * k * n / N
            w = Complex(math.cos(angle), math.sin(angle))
            total = total + X[k] * w
        result.append(Complex(total.real / N, total.imag / N))
    return result
```

### Paso 3: FFT (Cooley-Tukey)

El FFT recursivo requiere un poder de 2 de longitud. Dividido en par y impar, recursivo, combinado con factores de tortuga.

```python
def fft(x):
    N = len(x)
    if N <= 1:                                      # 基础情况：长度 1 的 DFT 就是自身
        return [x[0] if isinstance(x[0], Complex) else Complex(x[0])]
    if N % 2 != 0:                                  # 非偶数长度，回退到普通 DFT
        return dft(x)

    even = fft([x[i] for i in range(0, N, 2)])     # 递归：偶数下标子序列
    odd = fft([x[i] for i in range(1, N, 2)])      # 递归：奇数下标子序列

    result = [Complex(0)] * N
    for k in range(N // 2):
        angle = -2 * math.pi * k / N                # 旋转因子角度
        twiddle = Complex(math.cos(angle), math.sin(angle))  # 旋转因子 e^(-2piik/N)
        t = twiddle * odd[k]                        # 蝶形运算：旋转后的奇数部分
        result[k] = even[k] + t                    # 前半：E[k] + twiddle * O[k]
        result[k + N // 2] = even[k] - t           # 后半：E[k] - twiddle * O[k]
    return result
```

### Paso 4: Auxiliares de análisis espectral

```python
def power_spectrum(X):
    return [xk.real ** 2 + xk.imag ** 2 for xk in X]

def convolve_fft(x, h):
    N = len(x) + len(h) - 1                         # 线性卷积的输出长度
    padded_N = 1
    while padded_N < N:
        padded_N *= 2                                # 补零到 2 的幂次

    x_padded = x + [0.0] * (padded_N - len(x))      # 补零避免循环卷积混叠
    h_padded = h + [0.0] * (padded_N - len(h))

    X = fft(x_padded)                               # 信号 FFT
    H = fft(h_padded)                               # 滤波器 FFT

    Y = [xk * hk for xk, hk in zip(X, H)]          # 频域逐点相乘（卷积定理）

    y = idft(Y)                                     # 逆 FFT 回到时域
    return [y[n].real for n in range(N)]
```

## Usalo con el marco de ejecución

Para el trabajo real, utilice la FFT de numpy que está respaldada por bibliotecas C altamente optimizadas.

```python
import numpy as np

signal = np.sin(2 * np.pi * 5 * np.arange(256) / 256)
spectrum = np.fft.fft(signal)
freqs = np.fft.fftfreq(256, d=1/256)

power = np.abs(spectrum) ** 2

positive_freqs = freqs[:len(freqs)//2]
positive_power = power[:len(power)//2]
```

Para el análisis espectral de ventanas y más avanzado:

```python
from scipy.signal import windows, stft

window = windows.hann(256)
windowed = signal * window
spectrum = np.fft.fft(windowed)
```

Para la convolución:

```python
from scipy.signal import fftconvolve

result = fftconvolve(signal, kernel, mode='full')
```

Para los espectrogramas:

```python
from scipy.signal import stft

frequencies, times, Zxx = stft(signal, fs=sample_rate, nperseg=256)
spectrogram = np.abs(Zxx) ** 2
```

La matriz de espectrograma tiene forma (n_frecuencias, n_time_frames). Cada columna es el espectro de potencia en una ventana de tiempo. Esto es lo que los modelos de audio ML consumen como entrada.

> 频谱图矩阵形状是 (n_frequencias, n_time_frames) ⋅ cada fila es una ventana de tiempo ⋅ this is the input of the audio ML 模型 ⋅

## Envíe el producto .

- ¿ Qué ?`code/fourier.py`para generar `outputs/prompt-spectral-analyzer.md`¿ Qué ?

> 运行                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           `code/fourier.py`¿Qué es esto ?`outputs/prompt-spectral-analyzer.md`(Frequentes análisis de datos)

## Los ejercicios.

1. **Pure tone identification.**Crear una señal con una sola onda senoidal a una frecuencia desconocida (entre 1 y 50 Hz), muestreado a 128 Hz durante 1 segundo. Utilice su DFT para identificar la frecuencia. Verifique las coincidencias de las respuestas. Ahora añada el ruido gaussiano con desviación estándar 0.5 y repita. ¿Cómo afecta el ruido al espectro?

2. **FFT vs DFT verification.**Generar una señal aleatoria de longitud 64. Compute tanto DFT (O(N^2)) como FFT. Verifique si todos los coeficientes coinciden con dentro de 1e-10. El tiempo funciona en señales de longitud 256, 512, 1024, y 2048.

3. **Convolution theorem proof by example.**Crea la señal x = [1, 2, 3, 4, 0, 0, 0, 0] y filtra h = [1, 1, 1, 0, 0, 0, 0, 0]. Computa su convolución circular directamente (bucle anidado). Luego computa a través de FFT (transformación, multiplicación, transformación inversa). Verifique la coincidencia de los resultados. Ahora realiza la convolución lineal mediante empadejamiento cero adecuadamente.

4. **Windowing effects.**Crear una señal que sea la suma de dos ondas senolares a 10 Hz y 12 Hz (muy cerca). Muestrear a 128 Hz durante 1 segundo. Compute el espectro de potencia sin ventana, ventana Hann y ventana Hamming. ¿Qué ventana hace que sea más fácil distinguir los dos picos? ¿Por qué?

5. **Positional encoding analysis.**Generar las codificaciones posicionales sinusoidales para d_model = 128 y max_pos = 512. Para cada par de posiciones (p1, p2), calcular el producto de puntos de sus codificaciones. Muestre que el producto de puntos depende solo de p1 - p2 y no de las posiciones absolutas. ¿Qué sucede con el producto de puntos a medida que aumenta la distancia?

## Términos clave .

| Term | What it means |
|------|---------------|
| DFT (Discrete Fourier Transform) | Converts N time-domain samples into N frequency-domain coefficients. Each coefficient is the correlation with a complex sinusoid at that frequency |
| FFT (Fast Fourier Transform) | An O(N log N) algorithm to compute the DFT. The Cooley-Tukey algorithm splits even/odd indices recursively |
| Inverse DFT | Reconstructs the time-domain signal from frequency coefficients. Same formula as DFT with flipped exponent sign and 1/N scaling |
| Frequency bin | Each index k in the DFT output represents frequency k*fs/N Hz. The "bin" is the discrete frequency slot |
| DC component | X[0], the zero-frequency coefficient. Proportional to the signal mean |
| Nyquist frequency | fs/2, the maximum frequency representable at sampling rate fs. Frequencies above this alias |
| Power spectrum | \|X[k]\|^2, the squared magnitude of each frequency coefficient. Shows energy distribution across frequencies |
| Phase spectrum | angle(X[k]), the phase offset of each frequency component. Often ignored in analysis |
| Spectral leakage | Spurious frequency content caused by treating a non-periodic signal as periodic. Reduced by windowing |
| Window function | A tapering function (Hann, Hamming, Blackman) applied before DFT to reduce spectral leakage |
| Twiddle factor | The complex exponential e^(-2*pi*i*k/N) used to combine sub-DFTs in the FFT butterfly computation |
| Convolution theorem | Convolution in time domain equals pointwise multiplication in frequency domain. Fundamental to signal processing and CNNs |
| Circular convolution | Convolution where the signal wraps around. This is what the DFT naturally computes |
| Linear convolution | Standard convolution without wraparound. Achieved by zero-padding before DFT |
| Parseval's theorem | Total energy is preserved through the Fourier transform. sum \|x[n]\|^2 = (1/N) sum \|X[k]\|^2 |
| Aliasing | When frequencies above Nyquist appear as lower frequencies due to insufficient sampling rate |

> 术语速查:DFT(离散里叶变换)、FFT(快速里叶变换 O(N log N))、Inverse DFT(逆 DFT)、Frequency bin(频率槽)、DC componente(直流分量 X[0])、Nyquist frecuencia(奈奎斯特频率 fs/2)、Power spectrum(功率谱X[k]2)、Phase spectrum(相位谱)、Spectral leakage(频谱泄漏)、Window function function function function (window function)、Twiddle factor (window function) 旋转因子)、Convolution the卷积定理:时卷积=频域乘法)、Circular/Linear convolution循环/环积分 (环节) Parse's the energy 恒定orem (恒定orem) 

## Más Leer más Leer más

- [Cooley & Tukey: An Algorithm for the Machine Calculation of Complex Fourier Series (1965)](https://www.ams.org/journals/mcom/1965-19-090/S0025-5718-1965-0178586-1/)- el papel original de FFT que cambió la informática
- [3Blue1Brown: But what is the Fourier Transform?](https://www.youtube.com/watch?v=spUNpyF58BY)- la mejor introducción visual a las transformaciones de Fourier
- [Lee-Thorp et al.: FNet: Mixing Tokens with Fourier Transforms (2021)](https://arxiv.org/abs/2105.03824)- sustituye la autoatención por FFT en transformadores
- [Smith: The Scientist and Engineer's Guide to Digital Signal Processing](http://www.dspguide.com/)- libro de texto en línea gratuito que cubre en profundidad la FFT, la ventana y el análisis espectral
- [Vaswani et al.: Attention Is All You Need (2017)](https://arxiv.org/abs/1706.03762)- codificaciones sinusoidales de posición derivadas de la descomposición de la frecuencia de Fourier
- [Radford et al.: Whisper (2022)](https://arxiv.org/abs/2212.04356)- reconocimiento del habla mediante el uso de espectrogramas mel como representación de entrada
