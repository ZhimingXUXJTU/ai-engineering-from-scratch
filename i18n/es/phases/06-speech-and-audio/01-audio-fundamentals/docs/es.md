# Fundamentos de audio  Olas, muestras, transformación de Fourier  音频基础  波形、采样与里叶变换

> Las formas de onda son la señal bruta. Los espectrogramas son la representación. Las características de Mel son la forma amigable con ML. Cada tubería moderna de ASR y TTS camina esta escalera, y el primer paso es entender el muestreo y Fourier.

> **【中文解读】**波形是原始信号,频谱图是表示形式,Mel特征是机器学习的友好的形式──每现代语音识别(ASR) 和语音合成(TTS) sistemas están a lo largo de esta escala.

> **【拓展：音频 AI 的基础】**采样率 (como 16kHz) determina la frecuencia máxima que puede ser expresada 奈奎斯特定理) 里叶变化将时域信号分解为频域成分── Estos conceptos son la base de Whisper、TTS、语音克隆等所有音频 AI──

**Type:** Learn | **类型:** 学习
**Languages:** Python | **语言:** Python
**Prerequisites:** Phase 1 · 06 (Vectors & Matrices), Phase 1 · 14 (Probability Distributions) | **前置知识:** 阶段 1 · 06（向量与矩阵），阶段 1 · 14（概率分布）
**Time:** ~45 minutes | **预计用时:** ~45 分钟

## El problema es la introducción del problema

Un micrófono produce una señal de presión contra tiempo. Su red neuronal consume tensores. Entre ellos se encuentra una pila de convenciones que, cuando se violan, producen errores silenciosos: el modelo se entrena bien pero el WER se duplica, o TTS envía un silbido, o un sistema de clonación de voz memoriza el micrófono en lugar del altavoz.

> 麦克风产生一个压力-时间信号―― tu consumo de red neuronal es de张量―― entre ambos hay una serie de reglas que no cumplen con estas reglas que producen un error de ocultación: el modelo de entrenamiento es normal pero WER 双倍, o TTS 输出声, o el sistema de habla de Klon se acuerda de麦克风 en lugar de hablar de la persona―

> **【中文解读】**La pregunta planteada en este capítulo es: ¿cómo entender y aplicar correctamente esta tecnología en la ingeniería real? Comprender el contexto de la cuestión ayuda a comprender los puntos clave de decisión del tipo de selección técnica. En los sistemas de IA reales, el tipo de selección técnica errónea suele ser más alto que el costo de error de la realización de detalles.

Cada error en los sistemas de habla se remonta a una de las tres preguntas:

> Cada error en el sistema de voz se remonta a uno de los siguientes tres problemas:

1. ¿A qué tasa de muestreo se registraron los datos, y qué espera el modelo?
   ¿Cuál es la tasa de recogida de datos, cuál es la tasa de recogida de modelos esperados?
2. ¿La señal es alias?
   ¿Hay alguna confusión?
3. ¿Está operando en muestras crudas o en una representación de frecuencia?
   ¿Estás tratando el punto de muestra original o la frecuencia de la muestra?

Si haces esto bien, el resto de la Fase 6 es manejable, si haces esto mal, incluso Whisper-Large-v4 produce basura.

> Se puede entender fácilmente el resto de la etapa 6.

## El concepto central.

> **【中文解读】**Este capítulo presenta los conceptos y teorías básicos. La comprensión de estos conceptos es el prerrequisito de la realización posterior de la actividad, y también el conocimiento de los puntos de alta frecuencia de la entrevista y la práctica de la ingeniería.


![Waveform, sampling, DFT, and frequency bins visualized](../assets/audio-fundamentals.svg)

**Waveform.**Una matriz unidimensional de flotadores en `[-1.0, 1.0]`Para convertir en segundos, dividir por la tasa de muestra:`t = n / sr`Un clip de 10 segundos a 16 kHz es un conjunto de 160.000 floats.

> **波形（Waveform）。**Un valor en el`[-1.0, 1.0]`间一维浮点数组──以采样编为索引──转换为秒数,除以采样率:`t = n / sr`◊ 1 段 10 segundos de 16 kHz 音频 es un número de 160.000 个浮点数.

**Sampling rate (sr).**¿Cuántas muestras por segundo?

> **采样率（sr）。**Número de puntos de extracción por segundo.

| Rate | Use |
|------|-----|
| 8 kHz | Telephony, legacy VOIP. Nyquist at 4 kHz kills consonants. Avoid for ASR. |
| 16 kHz | ASR standard. Whisper, Parakeet, SeamlessM4T v2 all consume 16 kHz. |
| 22.05 kHz | TTS vocoder training for older models. |
| 24 kHz | Modern TTS (Kokoro, F5-TTS, xTTS v2). |
| 44.1 kHz | CD audio, music. |
| 48 kHz | Film, pro audio, high-fidelity TTS (VALL-E 2, NaturalSpeech 3). |

| 采样率 | 用途 |
|--------|------|
| 8 kHz | 电话、传统 VOIP。奈奎斯特频率 4 kHz 会丢失辅音。ASR 应避免使用。 |
| 16 kHz | ASR 标准。Whisper、Parakeet、SeamlessM4T v2 均使用 16 kHz。 |
| 22.05 kHz | 旧模型 TTS 声码器训练。 |
| 24 kHz | 现代 TTS（Kokoro、F5-TTS、xTTS v2）。 |
| 44.1 kHz | CD 音质、音乐。 |
| 48 kHz | 电影、专业音频、高保真 TTS（VALL-E 2、NaturalSpeech 3）。 |

**Nyquist-Shannon.**Una tasa de muestreo de `sr`puede representar de forma inequívoca frecuencias de hasta `sr/2`- El .`sr/2`La energía que se encuentra por encima de Nyquist se dobla hacia abajo en frecuencias más bajas y corrompe la señal.

> **奈奎斯特-香农定理。**采样率                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                          `sr`Puede decir sin diferencia hasta`sr/2`La frecuencia de la acción.`sr/2`边界就是奈奎斯特频率 (n) ⋅超奈奎斯特的能量会被混叠 (n) 折叠到更低的频率 (n) ⋅破坏信号 (n) ⋅降采采前务必先进行低通波 (n) ⋅降采前务必先进行低通波 (n) ⋅

**Bit depth.**PCM de 16 bits (firmado int16, rango ±32,767) es el formato de intercambio universal.`soundfile`leer int16 pero exponer float32 matrices en `[-1, 1]`¿ Qué ?

> **位深度。**16 位 PCM(有符号 int16,范围 ±32,767) es el formato de intercambio general.`soundfile`Esperar a leer en 16 pero regresar `[-1, 1]`范围的浮动32 数组──

**Fourier Transform.**Cualquier señal finita es una suma de sinusoides en diferentes frecuencias.`N`muestras, `N`coeficientes complejos  uno por cuadro de frecuencia. `bin k`mapas a la frecuencia `k · sr / N`La magnitud es la amplitud en esa frecuencia, el ángulo es la fase.

> **傅里叶变换。**Cualquier señal limitada puede ser dividida en diferentes frecuencias de la onda de los cuerpos.`N`个采样点计算                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        `N`个复数系数 个频率 bin 一个 个频率 bin 一个`bin k`Por lo tanto, el número de`k · sr / N`Hz── amplitud es la amplitud de la frecuencia, ángulo es fase──

**FFT.**Transformación rápida de Fourier: un `O(N log N)`algoritmo para el DFT cuando `N`Una FFT de 1024 muestras a 16 kHz da 512 contenedores de frecuencia utilizables que abarcan 08 kHz a una resolución de 15.6 Hz.

> **FFT。**快速里叶变换:当 `N`Por 2 de las horas, DFT de`O(N log N)`算法── cada nivel de base de la base de sonido utiliza FFT──16 kHz 下 1024 采样点的 FFT 产生 512 个可用频率bin,覆盖08 kHz,分辨率为15.6 Hz──

**Framing + window.**No FFT un clip entero. lo cortamos en *frames* superpuestos (generalmente 25 ms con 10 ms saltar), multiplicamos cada frame por una función de ventana (Hann, Hamming) para eliminar las discontinuidades de borde, luego FFT cada frame. Esto es el Short-Time Fourier Transform (STFT).

> **分帧 + 加窗。**Nosotros no hacemos FFT en todo el tiempo sino que lo cortamos en una serie de grabaciones de la misma forma. Normalmente, 25 ms, 10 ms, cada vez más en función de ventana.

> **【拓展：语音 AI 的产品化】**La tecnología de voz se enfrenta a un desafío único en la productorización: diferentes voces, ruidos de contexto, remota recogida, muchos hablar, etc.

> **【拓展：多语言语音技术】**Las características de los idiomas de todo el mundo son muy diferentes: el sonido de los idiomas de todo el mundo (como el chino) es alto, el lenguaje de bajo recurso es poco capacitado.



## Construye y realiza.

> **【中文解读】**Este capítulo a través del código de la implementación de algoritmos centrales de cero. Este método "desde cero" puede ayudar a entender el principio detrás del marco, no se encuentra en la caja negra cuando se encuentran problemas.

```figure
mel-scale
```

## Construye el mismo

### Paso 1: lee un clip y traza la forma de onda

`code/main.py`sólo utiliza el stdlib `wave`Modulo para mantener la demostración libre de dependencia.`soundfile`o `torchaudio.load`(ambos regresan `(waveform, sr)`Túples:

> `code/main.py`                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             `wave`模块 保持演示无依. 生产环境你会使用 `soundfile`O `torchaudio.load`(两者都回归 `(waveform, sr)`- ¿Qué es esto?

```python
import soundfile as sf
waveform, sr = sf.read("clip.wav", dtype="float32")  # shape (T,), sr=int
```

### Paso 2: sintetizar una onda seno a partir de los primeros principios

```python
import math

def sine(freq_hz, sr, seconds, amp=0.5):
    n = int(sr * seconds)
    return [amp * math.sin(2 * math.pi * freq_hz * i / sr) for i in range(n)]
```

Un seno de 440 Hz (concierto A) a 16 kHz durante 1 segundo es 16.000 flotantes.`wave.open(..., "wb")`utilizando codificación PCM de 16 bits.

> 16 kHz 采样率下 440 Hz 正弦波(标准音 A) duración 1 秒是 16,000 个浮点数──使用 `wave.open(..., "wb")`Es un programa de trabajo de 16 personas.

### Paso 3: calcular el DFT a mano

```python
def dft(x):
    N = len(x)
    out = []
    for k in range(N):
        re = sum(x[n] * math.cos(-2 * math.pi * k * n / N) for n in range(N))
        im = sum(x[n] * math.sin(-2 * math.pi * k * n / N) for n in range(N))
        out.append((re, im))
    return out
```

`O(N²)` bien por `N=256`Para confirmar la corrección, inútil para el audio real.`numpy.fft.rfft`o `torch.fft.rfft`¿ Qué ?

> `O(N²)`complejidad 对 `N=256`验证正确性还行,对真实音频没有用──实际代码调用 `numpy.fft.rfft`O `torch.fft.rfft`¿Qué es eso?

### Paso 4: encontrar la frecuencia dominante

Indice de pico de magnitud `k_star`mapas a la frecuencia `k_star * sr / N`Si ejecutamos esto en el seno de 440 Hz , volveremos a ver un pico en bin .`440 * N / sr`¿ Qué ?

> 幅度峰值索引 `k_star`Por lo tanto, el número de`k_star * sr / N`△ En 440 Hz, esta función debe estar en el bin `440 * N / sr`处返回峰值──

### Paso 5: demostrar el alias

Muestre un seno de 7 kHz a 10 kHz (Nyquist = 5 kHz). El tono de 7 kHz está por encima de Nyquist y se pliega a`10 − 7 = 3 kHz`El máximo de FFT aparece a 3 kHz. Esta es la demo de alias clásica y la razón por la cual todos los DAC / ADC envían con un filtro de paso bajo de pared de ladrillo.

> Es decir, el tiempo de la frecuencia de la voz de la voz de la voz de la voz de la voz de la voz de la voz de la voz de la voz de la voz de la voz de la voz de la voz de la voz de la voz de la voz de la voz de la voz de la voz de la voz de la voz de la voz de la voz de la voz de la voz de la voz de la voz de la voz de la voz de la voz de la voz de la voz de la voz de la voz de la voz de la voz de la voz de la voz de la voz de la voz de la voz de la voz de la voz de la voz de la voz de la voz de la voz de la voz de la voz de la voz de la voz de la voz de la voz de la voz de la voz de la voz de la voz de la voz de la voz de la voz de la voz de la voz de la voz de la voz de la voz de la voz de la voz de la voz de la voz de la voz de la voz de la voz de la voz de la voz de la voz de la voz de la voz de la voz de la voz de la voz de la voz de la voz de la voz de la voz de la voz de la voz de la voz de la voz de la voz de la voz de la voz de la voz de la voz de la voz de la voz de la voz de la voz de la voz de la voz de la voz de la voz de la voz de la voz de la voz de la voz de la voz de la voz de la voz de la voz de la voz de la voz de la voz de la voz de la voz de la voz de la voz de la voz de la voz de la voz de la voz de la voz de la voz de la voz de la voz de la voz de la voz de la voz de la voz de la voz de la voz de la voz de la voz de la voz de la voz de la voz de la voz de la voz de la voz de la voz de la voz de la voz de la voz de la voz de la voz de la voz de la voz de la voz de la voz de la voz de la voz de la voz de la voz de la voz de la voz de la voz de la voz de la voz de la voz de la que se.`10 − 7 = 3 kHz` La máxima de FFT se encuentra en 3 kHz  Este es el clásico show de la mezcla, también es la razón de cada DAC / ADC están equipados con un dispositivo de carga de alta velocidad 

> **【中文解读】**Este capítulo muestra cómo utilizar un marco maduro (como PyTorch、HuggingFace, etc.) para aplicar rápidamente esta tecnología. En los proyectos reales, se realiza con prioridad el uso de un marco experimentado, se pueden reducir errores y mejorar la eficiencia de desarrollo.





> **【拓展：语音与情感计算】**语音 no sólo transmite información escrita, también lleva una rica cantidad de señales emocionales (en inglés: voice signal) 语调、语速、音高变化) 情感语音识别 (en inglés: speech emotion recognition, SER) 语音 no solo transmite información escrita, sino que también lleva una gran cantidad de señales emocionales (en inglés: voice signal). 语音 tiene una amplia aplicación en el campo de la evaluación de calidad de los clientes, la vigilancia de la salud mental, la educación inteligente, etc.  Los modelos actuales de SOTA se basan en modelos de entrenamiento de las ondas 2vec 2.0 o HuBERT.

## Usalo con el marco de ejecución

La pila que enviará en 2026:

> 2026 años que usted realmente utilizará las técnicas:

| Task | Library | Why |
|------|---------|-----|
| Read/write WAV/FLAC/OGG | `soundfile` (libsndfile wrapper) | Fastest, stable, returns float32. |
| Resample | `torchaudio.transforms.Resample` or `librosa.resample` | Correct anti-aliasing built in. |
| STFT / Mel | `torchaudio` or `librosa` | GPU-friendly; PyTorch ecosystem. |
| Real-time streaming | `sounddevice` or `pyaudio` | Cross-platform PortAudio bindings. |
| Inspect a file | `ffprobe` or `soxi` | CLI, fast, reports sr/channels/codec. |

| 任务 | 库 | 原因 |
|------|----|------|
| 读写 WAV/FLAC/OGG | `soundfile`（libsndfile 封装） | 最快、最稳定，返回 float32。 |
| 重采样 | `torchaudio.transforms.Resample` 或 `librosa.resample` | 内置正确的抗混叠滤波。 |
| STFT / Mel | `torchaudio` 或 `librosa` | GPU 友好；PyTorch 生态。 |
| 实时流 | `sounddevice` 或 `pyaudio` | 跨平台 PortAudio 绑定。 |
| 检查文件 | `ffprobe` 或 `soxi` | 命令行工具，快速报告采样率/声道/编码。 |

> **【中文解读】**Este capítulo se centra en cómo se puede implementar el modelo como producto disponible. Desde el modelo original hasta el sistema de producción, se deben considerar múltiples dimensiones de optimización de rendimiento, tratamiento de errores, control, etc.


Regla de decisión: **match sample rate before you match anything else**Whisper espera una mono float de 16 kHz.

>  决策规则:**在匹配其他任何东西之前先匹配采样率**❖ Susurro 期望 16 kHz 单声道 float32──传入 44.1 kHz 立体声, usted se verá como el resultado de un error de modelo ⋅

> **【中文解读】**Practice los temas de fácil/medio/duro  3 difficulty to pass in  Recomenda al menos completar los temas de grado medio  Grado duro  para la preparación de la entrevista




## Envíe el producto .

Salvo como`outputs/skill-audio-loader.md`La habilidad le ayuda a comprobar si la entrada de audio coincide con las expectativas del modelo en línea y repeticiones correctas cuando no lo hace.

> 保存为                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           `outputs/skill-audio-loader.md`◊ Esta habilidad te ayuda a comprobar si la entrada de audio coincide con las expectativas del modelo de audio y si es correctamente re-escrita cuando no coincide.

## Los ejercicios.

1. **Easy.**Sintetiza una mezcla de 1 segundo de 220 Hz + 440 Hz + 880 Hz a 16 kHz. ejecuta DFT. Confirme tres picos en los contenedores esperados.
   **简单。**合成一 220 Hz + 440 Hz + 880 Hz de 1 segundo de señal mixta, tasa de toma de 16 kHz──运行 DFT── confirmar en la posición de espera bin  有三个峰值──
2. **Medium.**Graba un WAV de 3 segundos de tu voz a 48 kHz.`torchaudio.transforms.Resample`(con antialiasing), luego a 16 kHz usando decimación ingenua (cada tercera muestra).
   **中等。**录制一段 3 秒 48 kHz 的语音 WAV──使用 `torchaudio.transforms.Resample`(带抗混叠)降采样到16 kHz,然后用朴素抽取(每隔三个样本取一个)降采样到16 kHz──对两者做FFT──混叠现在出哪里?
3. **Hard.**Construir el STFT desde cero usando sólo `math`y el DFT de la etapa 3. tamaño de cuadro 400, salta 160, ventana Hann.`matplotlib.pyplot.imshow`Este es el espectrograma de la Lección 02.
   **困难。**Sólo para usar`math`Y paso 3 de DFT desde el punto de construcción STFT──大小 400,步长 160,Hann 窗──用 `matplotlib.pyplot.imshow`图绘幅度图―― ése es el cuadro de frecuencia de la segunda clase ⋅

> **【中文解读】**En el lenguaje de los términos "Lo que la gente dice" vs "Lo que realmente significa" se distingue entre el lenguaje diario y la definición técnica de significado.


## Términos clave .

| Term | What people say | What it actually means |
|------|-----------------|-----------------------|
| Sample rate | How many samples per second | Frequency in Hz at which the ADC measures the signal. |
| Nyquist | The max frequency you can represent | `sr/2`; energy above it aliases back down. |
| Bit depth | Resolution of each sample | `int16` = 65,536 levels; `float32` = 24-bit precision in `[-1, 1]`. |
| DFT | The Fourier transform for sequences | `N` samples → `N` complex frequency coefficients. |
| FFT | The fast DFT | `O(N log N)` algorithm requiring `N` = power of 2. |
| Bin | Frequency column | `k · sr / N` Hz; resolution = `sr / N`. |
| STFT | Spectrogram under the hood | Framed + windowed FFT over time. |
| Aliasing | Weird frequency ghosts | Energy above Nyquist mirroring down to lower bins. |

| 术语 | 人们常说的 | 实际含义 |
|------|-----------|---------|
| 采样率 | 每秒多少个采样点 | ADC 测量信号的频率（Hz）。 |
| 奈奎斯特 | 能表示的最大频率 | `sr/2`；超过它的能量会混叠回来。 |
| 位深度 | 每个采样点的精度 | `int16` = 65,536 级；`float32` = `[-1, 1]` 中 24 位精度。 |
| DFT | 序列的傅里叶变换 | `N` 个采样 → `N` 个复数频率系数。 |
| FFT | 快速 DFT | `O(N log N)` 算法，要求 `N` 为 2 的幂。 |
| Bin | 频率列 | `k · sr / N` Hz；分辨率 = `sr / N`。 |
| STFT | 频谱图的底层实现 | 分帧 + 加窗的 FFT 随时间推移。 |
| 混叠 | 奇怪的频率鬼影 | 超过奈奎斯特的能量镜像到更低的 bin。 |

> **【中文解读】**延伸阅读 proporciona un alto nivel de recursos para el aprendizaje profundo. Estos artículos y cursos son los referentes clásicos en el campo, adecuados para los lectores que necesitan una comprensión profunda.


## Más Leer más Leer más

- [Shannon (1949). Communication in the Presence of Noise](https://people.math.harvard.edu/~ctm/home/text/others/shannon/entropy/entropy.pdf) el papel detrás del teorema de muestreo.
  Shannon (1949) 带噪音条件下的通信采样定理后背的论文──
- [Smith — The Scientist and Engineer's Guide to Digital Signal Processing](https://www.dspguide.com/ch8.htm) libro de texto canónico de DSP.
  Smith  Científico e Ingeniero  Digital Signal Processing Guide  Gratis clásico material de enseñanza DSP 
- [librosa docs — audio primer](https://librosa.org/doc/latest/tutorial.html) Un paso práctico con el código.
  Bibliografía 文档音频入门带代码的实践教程──
- [Heinrich Kuttruff — Room Acoustics (6th ed.)](https://www.routledge.com/Room-Acoustics/Kuttruff/p/book/9781482260434) referencia de por qué el audio del mundo real no es un sinusoide limpio.
  Heinrich Kuttruff 房间声学(第 6 版)  Explicar por qué el verdadero mundo sonido no está haciendo puro.
- [Steve Eddins — FFT Interpretation notebook](https://blogs.mathworks.com/steve/2020/03/30/fft-spectrum-and-spectral-densities/)La intuición del contenedor de frecuencia se despejó en 10 minutos.
  Steve Eddins FFT 解读笔记10 分钟搞清频率 bin 的直觉──

> **【中文解读】**延伸阅读 proporciona recursos de alta calidad para el aprendizaje profundo, incluyendo artículos, tutorials y herramientas.

