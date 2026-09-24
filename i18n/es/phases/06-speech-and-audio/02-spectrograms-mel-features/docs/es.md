# Espectogramas, escala de Mel y características de audio.

> Las redes neuronales no consumen bien las formas de onda crudas. Consumen espectrogramas. Consumen espectrogramas mel aún mejor. Cada clasificador de audio, TTS y ASR en 2026 vive o muere por esta sola elección de procesamiento previo.

> **【中文解读】**El procesamiento de la red de nervios no tiene un buen efecto, pero el procesamiento de la frecuencia es bueno, el procesamiento de la frecuencia es mejor. El éxito de todos los ASR、TTS y los equipos de clasificación de la frecuencia en 2026 depende de esta opción de procesamiento previo.

> **【拓展：Mel 频谱图是音频 AI 的 "图像"】**Mel 频谱图将音频转换为 2D 图像(时间×频率), se puede usar para CNN/ViT 处理──Whisper、MusicGen、Stable Audio 都使用 Mel 频谱图作为中间表示──

**Type:** Build | **类型:** 构建
**Languages:** Python | **语言:** Python
**Prerequisites:** Phase 6 · 01 (Audio Fundamentals) | **前置知识:** 阶段 6 · 01（音频基础）
**Time:** ~45 minutes | **预计用时:** ~45 分钟

## El problema es la introducción del problema

Toma un clip de 10 segundos de 16 kHz. Eso es 160.000 floats, todo en`[-1, 1]`La forma de onda cruda tiene la información pero en una forma que el modelo no puede extraer fácilmente. Dos fonemas idénticos hablados a 100 ms de distancia tienen muestras crudas completamente diferentes.

> Una secuencia de 10 segundos de 16 kHz de frecuencia.`[-1, 1]`En el ámbito, casi no se relaciona con el etiquetado "perro llama" o "gato palabra" en absoluto. La forma original de la onda contiene información, pero la forma es difícil de extraer.

> **【中文解读】**La pregunta planteada en este capítulo es: ¿cómo entender y aplicar correctamente esta tecnología en la ingeniería real? Comprender el contexto de la cuestión ayuda a comprender los puntos clave de decisión del tipo de selección técnica. En los sistemas de IA reales, el tipo de selección técnica errónea suele ser más alto que el costo de error de la realización de detalles.

Un espectrograma corrige esto. Se derrumba el detalle temporal donde la percepción humana lo ignora (miocrosegundo de nerviosismo) y conserva la estructura donde la percepción asiste (que son frecuencias energéticas, en ventanas de tiempo de ~ 1025 ms).

> 频谱图 resuelve este problema. Se comprime el tiempo de la percepción humana ignora detalles de tiempo (microsegundos de movimiento), se conserva la estructura de la percepción de la preocupación (en la ventana de tiempo de aproximadamente 1025 ms, qué frecuencias tienen energía) 

Los espectrogramas mel empujan más lejos. Los humanos perciben el tono logaritmicamente: 100 Hz vs 200 Hz suenan "la misma distancia entre sí" que 1000 Hz vs 2000 Hz. La escala mel deforma el eje de frecuencia para que coincida. Un espectrograma a escala mel es la característica más importante en el lenguaje ML desde 2010 hasta 2026.

> La percepción humana de la frecuencia sonora es proporcional a la de la cantidad: 100 Hz y 200 Hz, y 1000 Hz y 2000 Hz "a la misma distancia".

## El concepto central.

> **【中文解读】**Este capítulo presenta los conceptos y teorías básicos. La comprensión de estos conceptos es el prerrequisito de la realización posterior de la actividad, y también el conocimiento de los puntos de alta frecuencia de la entrevista y la práctica de la ingeniería.


![Waveform to STFT to mel spectrogram to MFCC ladder](../assets/mel-features.svg)

**STFT (Short-Time Fourier Transform).**Cortar la forma de onda en cuadros superpuestos (típico: ventana de 25 ms, 10 ms hop = 400 muestras / 160 muestras a 16 kHz). Multiplicar cada cuadro por una función de ventana (Hann es el predeterminado; Hamming un poco diferente tradeoff). FFT cada cuadro. apilar los espectros de magnitud en una matriz de forma `(n_frames, n_freq_bins)`Ese es tu espectrograma.

> **STFT（短时傅里叶变换）。**Se puede ver en el gráfico de la pantalla de la pantalla de la pantalla de la pantalla de la pantalla de la pantalla de la pantalla de la pantalla de la pantalla de la pantalla de la pantalla de la pantalla de la pantalla de la pantalla de la pantalla de la pantalla de la pantalla de la pantalla de la pantalla de la pantalla de la pantalla de la pantalla de la pantalla de la pantalla de la pantalla de la pantalla de la pantalla de la pantalla de la pantalla de la pantalla de la pantalla de la pantalla de la pantalla de la pantalla de la pantalla de la pantalla de la pantalla de la pantalla de la pantalla de la pantalla de la pantalla de la pantalla de la pantalla de la pantalla de la pantalla de la pantalla de la pantalla de la pantalla de la pantalla de la pantalla de la pantalla de la pantalla de la pantalla de la pantalla de la pantalla de la pantalla de la pantalla de la pantalla de la pantalla de la pantalla de la pantalla de la pantalla de la pantalla de la pantalla de la pantalla de la pantalla de la pantalla de la pantalla de la pantalla de la pantalla de la pantalla de la pantalla de la pantalla de la pantalla de la pantalla de la pantalla de la pantalla de la pantalla de la pantalla de la pantalla de la pantalla de la pantalla de la pantalla de la pantalla de la pantalla de la pantalla de la pantalla de la pantalla de la pantalla de la pantalla de la pantalla de la pantalla de la pantalla de la pantalla de la pantalla de la pantalla de la pantalla de la pantalla de la pantalla de la pantalla de la pantalla de la pantalla de la pantalla de la pantalla de la pantalla de la pantalla de la pantalla de la pantalla de la pantalla de la pantalla de la pantalla de la pantalla de la pantalla de la pantalla de la pantalla de la pantalla de la pantalla de la pantalla de la pantalla de la pantalla de la pantalla de la pantalla de la pantalla de la pantalla de la pantalla de la pantalla de la pantalla de la pantalla de la pantalla de la pantalla de la pantalla de la pantalla de la pantalla de la pantalla de la pantalla de la pantalla de la pantalla de la pantalla de la pantalla de la pantalla de la pantalla de la pantalla de la pantalla de la pantalla de la pantalla de la pantalla de la pantalla de la pantalla de la pantalla de la pantalla de la pantalla de la pantalla de la del del del del del del del del del del del del del del del del del del del del.`(n_frames, n_freq_bins)`Es tu cuadro de frecuencia.

**Log-magnitude.**Las magnitudes primas abarcan entre 5 y 6 órdenes de magnitud.`log(|X| + 1e-6)`o `20 * log10(|X|)`Cada línea de producción utiliza la magnitud de registro, no la magnitud en bruto.

> **对数幅度。**La amplitud original transcende entre 5 y 6 grados de cantidad.`log(|X| + 1e-6)`O `20 * log10(|X|)`Para comprimir el rango de movimiento, cada línea de producción se utiliza para la amplitud numérica y no la amplitud original.

**Mel scale.**Frecuencia `f`en mapas Hz a mel `m`por `m = 2595 * log10(1 + f / 700)`. El mapeo es aproximadamente lineal por debajo de 1 kHz y aproximadamente logaritmico por encima. 80 melbins que cubren 08 kHz es la entrada estándar de ASR.

> **Mel 尺度。** frecuencia `f`(Hz) la proyección hasta el`m`de la fórmula por`m = 2595 * log10(1 + f / 700)`◊该映射在1 kHz 以下大致线性,以上大致对数──覆盖08 kHz 80  mel bin es estándar ASR 输入──

**Mel filterbank.**Un conjunto de filtros triangulares espaciados igualmente en la escala mel. Cada filtro es una suma ponderada de contenedores FFT adyacentes. Multiplicando la magnitud STFT por la matriz de filtro banco se da el espectrograma mel en un matmul.

> **Mel 滤波器组。**Un grupo en la escala mel igual a la distancia entre la fila de los tres angles de la masa. Cada una de las tres partes es el aumento de la masa de la masa de la masa de la masa de la masa de la masa de la masa de la masa.

**Log-mel spectrogram.** `log(mel_spec + 1e-10)`La entrada de Whisper, la entrada de Parakeet, la entrada de SeamlessM4T, el frontend de audio universal 2026.

> **对数 Mel 频谱图。** `log(mel_spec + 1e-10)`❖ Whisper 的输入──Parakeet 的输入──SeamlessM4T 的输入──2026年通用音频前端──

**MFCCs.**Tomar el espectrograma de log-mel, aplicar un DCT (tipo II), mantener los primeros 13 coeficientes. Descoorrela las características y comprime más. característica dominante hasta alrededor de 2015 cuando CNNs / Transformers en los log-mels crudos se recuperaron. Todavía se utiliza en el reconocimiento de altavoces (vectores x, ECAPA).

> **MFCC。**取对数 Mel 频谱图,应用 DCT(类 II), retención de 13 个系数── eliminación de rasgos entre la correlación y la composición adicional── después de 2015 años de la principal característica, después CNN/Transformer 在原始 log-mel 上追上── todavía se utiliza para hablar de personas identificación(x-vectores、ECAPA)──

**Resolution trade.**FFT más grande = mejor resolución de frecuencia pero peor resolución de tiempo. 25 ms / 10 ms es el audio-ML predeterminado; 50 ms / 12.5 ms para la música; 5 ms / 2 ms para la detección transitoria (batería, plosivos).

> **分辨率权衡。**Más grande FFT = mejor frecuencia resolución pero peor de tiempo resolución──25 ms / 10 ms es el valor predeterminado de la FM de la FM de la FM de la FM de la FM de la FM de la FM de la FM de la FM de la FM de la FM de la FM de la FM de la FM de la FM de la FM de la FM de la FM de la FM de la FM de la FM de la FM de la FM de la FM de la FM de la FM de la FM de la FM de la FM de la FM de la FM de la FM de la FM de la FM de la FM de la FM de la FM de la FM de la FM de la FM de la FM de FM de FM de FM de FM de FM de FM de FM de FM de FM de FM de FM de FM de FM de FM de FM de FM de FM de FM de FM de FM de FM de FM de FM de FM de FM de FM de FM de FM de FM de FM de FM de FM de FM de FM de FM de FM de FM de FM de FM de FM de FM de FM de FM de FM de FM de FM de FM de FM de FM de FM de FM de FM de FM de FM de FM de FM de FM de FM de FM de FM de FM de FM de FM de FM de FM de FM de FM de FM de FM de FM de FM de FM de FM de FM de FM de FM de FM de FM de FM de FM de FM de FM de FM de FM de FM de FM de FM de FM de FM de FM de FM de FM de FM de FM de FM de FM de FM de FM de FM de FM de FM de FM de FM de FM de FM de FM de FM de FM de FM de FM de FM de FM de FM de FM de FM de FM de FM de FM de FM de FM de FM de FM de FM de FM de FM de FM de FM de FM de FM de FM de FM de FM de FM de FM de FM de FM de FM de FM de FM de FM de FM de FM de FM de FM de FM de FM de FM de de de FM de FM de FM de de FM de FM de de de de FM de FM de de de de FM de FM de FM de de de de de de FM de FM de FM de de FM de FM de de de de de de de de de de de FM de FM de de de de FM de FM de de

> **【拓展：语音 AI 的产品化】**La tecnología de voz se enfrenta a un desafío único en la productorización: diferentes voces, ruidos de contexto, remota recogida, muchos hablar, etc.

> **【拓展：多语言语音技术】**Las características de los idiomas de todo el mundo son muy diferentes: el sonido de los idiomas de todo el mundo (como el chino) es alto, el lenguaje de bajo recurso es poco capacitado.



## Construye y realiza.

> **【中文解读】**Este capítulo a través del código de la implementación de algoritmos centrales de cero. Este método "desde cero" puede ayudar a entender el principio detrás del marco, no se encuentra en la caja negra cuando se encuentran problemas.

```figure
spectrogram-window
```

## Construye el mismo

### Paso 1: Enmarque la forma de onda

```python
def frame(signal, frame_len, hop):
    n = 1 + (len(signal) - frame_len) // hop
    return [signal[i * hop : i * hop + frame_len] for i in range(n)]
```

Un clip de 10 segundos de 16 kHz con `frame_len=400, hop=160`y produce 998 cuadros.

> Una sección 10 秒 16 kHz 的音频,使用 `frame_len=400, hop=160`, obtuve 998 🏼

### Paso 2: Ventana Hann

```python
import math

def hann(N):
    return [0.5 * (1 - math.cos(2 * math.pi * n / (N - 1))) for n in range(N)]
```

Multiplicar el elemento con la inteligencia antes de la FFT. Elimina la fuga espectral causada por el truncado en puntos finales no cero.

> En el FFT  previo a cada elemento                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    

### Paso 3: magnitud de la FST

```python
def stft_magnitude(signal, frame_len=400, hop=160):
    win = hann(frame_len)
    frames = frame(signal, frame_len, hop)
    return [magnitudes(dft([w * s for w, s in zip(win, f)])) for f in frames]
```

Utilizaciones en la producción `torch.stft`o `librosa.stft`El ciclo aquí es pedagógico; se ejecuta en cortos clips en`code/main.py`¿ Qué ?

> Productos y medio ambiente`torch.stft`O `librosa.stft`(basado en la FFT ∞ ∞) ∞ El ciclo de este es el propósito de la enseñanza; está en ∞`code/main.py`En el medio de la obra, el texto se traduce en "La vida de los hombres".

### Paso 4: banco de filtros de mel

```python
def hz_to_mel(f):
    return 2595.0 * math.log10(1.0 + f / 700.0)

def mel_to_hz(m):
    return 700.0 * (10 ** (m / 2595.0) - 1)

def mel_filterbank(n_mels, n_fft, sr, fmin=0, fmax=None):
    fmax = fmax or sr / 2
    mels = [hz_to_mel(fmin) + (hz_to_mel(fmax) - hz_to_mel(fmin)) * i / (n_mels + 1)
            for i in range(n_mels + 2)]
    hzs = [mel_to_hz(m) for m in mels]
    bins = [int(h * n_fft / sr) for h in hzs]
    fb = [[0.0] * (n_fft // 2 + 1) for _ in range(n_mels)]
    for m in range(n_mels):
        for k in range(bins[m], bins[m + 1]):
            fb[m][k] = (k - bins[m]) / max(1, bins[m + 1] - bins[m])
        for k in range(bins[m + 1], bins[m + 2]):
            fb[m][k] = (bins[m + 2] - k) / max(1, bins[m + 2] - bins[m + 1])
    return fb
```

80 mels que cubren 08 kHz con `n_fft=400`da una`(80, 201)`Matriz. Multiplicar el `(n_frames, 201)`La magnitud de la STFT por la transposición para obtener `(n_frames, 80)`Es un espectrograma de mel.

> 覆盖 08 kHz de 80 个 mel 波器,`n_fft=400`, lo conseguí`(80, 201)`¿Qué es eso?`(n_frames, 201)`La amplitud de la STFT se traduce en`(n_frames, 80)`De la mel 频谱图:

### Paso 5: registro de correo electrónico

```python
def log_mel(mel_spec, eps=1e-10):
    return [[math.log(max(v, eps)) for v in frame] for frame in mel_spec]
```

Alternativas comunes: `librosa.power_to_db`(dB normalizado en referencia),`10 * log10(power + eps)`. Whisper utiliza un clip más involucrado + normaliza la rutina (ver Whisper's `log_mel_spectrogram`¿Qué es lo que se hace?

> 常见替代方案:`librosa.power_to_db`(en referencia a la reducción de dB)`10 * log10(power + eps)`✿ Susurro ✿ Uso de cortes más complejos ✿ ✿ ✿ ✿ ✿ ✿ ✿ ✿ ✿ ✿ ✿ ✿ ✿ ✿ ✿ ✿ ✿ ✿ ✿ ✿ ✿ ✿ ✿ ✿ ✿ ✿ ✿ ✿ ✿ ✿ ✿ ✿ ✿ ✿ ✿ ✿ ✿ ✿ ✿ ✿ ✿ ✿ ✿ ✿ ✿ ✿ ✿ ✿ ✿ ✿ ✿ ✿ ✿ ✿ ✿ ✿ ✿ ✿ ✿ ✿ ✿ ✿ ✿ ✿ ✿ ✿ ✿ ✿ ✿ ✿ ✿ ✿ ✿ ✿ ✿ ✿ ✿ ✿ ✿ ✿ ✿ ✿ ✿ ✿ ✿ ✿ ✿ ✿ ✿ ✿ ✿ ✿ ✿ ✿ ✿ ✿ ✿ ✿ ✿ ✿ ✿ ✿ ✿ ✿ ✿ ✿ ✿ ✿ ✿ ✿ ✿ ✿ ✿ ✿ ✿ ✿ ✿ ✿ ✿ ✿ ✿ ✿ ✿ ✿ ✿ ✿ ✿ ✿ ✿ ✿ ✿ ✿ ✿ ✿ ✿`log_mel_spectrogram`)。

### Paso 6: CFCM

```python
def dct_ii(x, n_coeffs):
    N = len(x)
    return [
        sum(x[n] * math.cos(math.pi * k * (2 * n + 1) / (2 * N)) for n in range(N))
        for k in range(n_coeffs)
    ]
```

> **【中文解读】**Este capítulo muestra cómo utilizar un marco maduro (como PyTorch、HuggingFace, etc.) para aplicar rápidamente esta tecnología. En los proyectos reales, se realiza con prioridad el uso de un marco experimentado, se pueden reducir errores y mejorar la eficiencia de desarrollo.


Aplicar DCT a cada marco de log-mel, mantener los primeros 13 coeficientes. Esa es su matriz MFCC. El primer coeficiente se cae generalmente (que codifica la energía total).

> Para cada log-mail  aplica DCT, reserva anterior 13 系数── esto es tu MFCC 矩阵── el primer系数 se suele desechar.




> **【拓展：语音与情感计算】**语音 no sólo transmite información escrita, también lleva una rica cantidad de señales emocionales (en inglés: voice signal) 语调、语速、音高变化) 情感语音识别 (en inglés: speech emotion recognition, SER) 语音 no solo transmite información escrita, sino que también lleva una gran cantidad de señales emocionales (en inglés: voice signal). 语音 tiene una amplia aplicación en el campo de la evaluación de calidad de los clientes, la vigilancia de la salud mental, la educación inteligente, etc.  Los modelos actuales de SOTA se basan en modelos de entrenamiento de las ondas 2vec 2.0 o HuBERT.

## Usalo con el marco de ejecución

La pila de 2026:

> Tecnología de 2026:

| Task | Features |
|------|----------|
| ASR (Whisper, Parakeet, SeamlessM4T) | 80 log-mels, 10 ms hop, 25 ms window |
| TTS acoustic model (VITS, F5-TTS, Kokoro) | 80 mels, 5–12 ms hop for fine temporal control |
| Audio classification (AST, PANNs, BEATs) | 128 log-mels, 10 ms hop |
| Speaker embedding (ECAPA-TDNN, WavLM) | 80 log-mels or raw-waveform SSL |
| Music (MusicGen, Stable Audio 2) | EnCodec discrete tokens (not mels) |
| Keyword spotting | 40 MFCCs for tiny devices |

| 任务 | 特征配置 |
|------|----------|
| ASR（Whisper、Parakeet、SeamlessM4T） | 80 log-mels，10 ms 步长，25 ms 窗口 |
| TTS 声学模型（VITS、F5-TTS、Kokoro） | 80 mels，5–12 ms 步长，精细时间控制 |
| 音频分类（AST、PANNs、BEATs） | 128 log-mels，10 ms 步长 |
| 说话人嵌入（ECAPA-TDNN、WavLM） | 80 log-mels 或原始波形 SSL |
| 音乐（MusicGen、Stable Audio 2） | EnCodec 离散 token（非 mels） |
| 关键词检测 | 40 MFCCs，用于小型设备 |

Regla de oro: **if you are not working on music, start with 80 log-mels.**La carga de la prueba está en cualquier desviación.

> 经验法则:**如果你不是在做音乐，就从 80 log-mels 开始。**Cualquier desviación necesita demostrar su razonabilidad.



## Las trampas que todavía se envían en 2026

> 2026 año todavía en la trampa de los culpables

- **Mel count mismatch.**Entrenamiento con 80 mels, inferencia con 128 mels, fallo silencioso, registro de la forma de la característica en ambos extremos.
  **Mel 数量不匹配。**Entrenamiento con 80 mels, recomendación con 128 mels.
- **Sample-rate mismatch upstream.**Los Mels calculados a 22,05 kHz se ven diferentes a los 16 kHz.
  **上游采样率不匹配。**Los datos de la información de la información de la información de la información de la información de la información de la información de la información de la información de la información de la información de la información de la información de la información de la información de la información de la información de la información de la información de la información de la información de la información de la información de la información de la información de la información de la información de la información de la información de la información de la información de la información de la información de la información de la información de la información de la información de la información de la información de la información de la información de la información de la información de la información de la información de la información de la información de la información de la información de la información de la información de la información de la información de la información de la información de la información de la información de la información de la información de la información de la información de la información de la información de la información de la información de la información de la información de la información de la información de la información de la información de la información de la información de la información de la información de la información de la información de la información de la información de la información de la información de la información de la información de la información de la información de la información de la información de la información de la información de la información de la información de la información de la información de la información de la información de la información de la información de la información de la información de la información de la información de la información de la información de la información de la información de la información de la información de la información de la información de la información de la información de la información de la información de la información de la información de la información de la información de la información de la cuidad de la cuidad de la cuidad de la cuidad de la cuidad de la cuidad de la cuidad de cuidad de la cuidad de cuidad de la cuidad de cuidad de la cuidad de la cuidad de cuidad de cuidad de la cuidad de cuidad de la cuidad de cuidad de cuidad de cuidad de cuidad de cuidad de cuidad de cuidad de cuidad de cuidad de cuidad de cuidad de cuidad de cuidad de cuidad de cuidad de cuidad de cuidad de cuidad de cuidad de cuidad de cuidad de cuidad de cuidad de cuidad de cuidad de cuidad de cuidad de cuidad
- **dB vs log.**Whisper espera log-mel, no dB-mel. Algunas tuberías HF se detecten automáticamente, su código personalizado no lo hará.
  **dB 与 log。**Susurro 期望 log-mel y no dB-mel。 ciertos HF 流水线会自动检测; tu código de autodeterminación no será。
- **Normalization drift.**Normalización de la producción durante el entrenamiento, normalización global durante la inferencia.
  **归一化漂移。**                                                                                                                                                                                                                                                              
- **Leakage from padding.**El empate cero en el extremo de un clip produce un espectro plano en los marcos traseros.
  **填充泄漏。**Para el final de un episodio de la serie, se produce un espectro plano.

> **【中文解读】**Este capítulo se centra en cómo se puede implementar el modelo como producto disponible. Desde el modelo original hasta el sistema de producción, se deben considerar múltiples dimensiones de optimización de rendimiento, tratamiento de errores, control, etc.


## Envíe el producto .

Salvo como`outputs/skill-feature-extractor.md`La habilidad selecciona el tipo de característica, el recuento de mel, el marco/salto y la normalización para un objetivo de modelo determinado.

> 保存为                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           `outputs/skill-feature-extractor.md` Esta habilidad se utiliza para determinar el modelo objetivo de selección de características tipo, número de datos, y forma de integración.

## Los ejercicios.

1. **Easy.**- ¿ Qué ?`code/main.py`. Sintetiza una chirp (frecuencia barrida 200 → 4000 Hz) e imprime el argmax mel bin por fotograma.
   **简单。**运行                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           `code/main.py`△ se compone una señal  frecuencia de 200 扫 hasta 4000 Hz) 并印每的 argmax mel bin──绘图(可选)并确认与扫频匹配──
2. **Medium.**Re-corre con `n_mels`En el`{40, 80, 128}`y `frame_len`En el`{200, 400, 800}`¿Cuál combinación resuelve mejor el chimp?
   **中等。**¿ Qué ?`n_mels`Por lo tanto ,`{40, 80, 128}`Y `frame_len`Por lo tanto ,`{200, 400, 800}`重新运行. ¿Cuál es el mejor conjunto para detectar señales?
3. **Hard.**Implementación `power_to_db`y comparar la precisión de ASR de un pequeño clasificador CNN en AudioMNIST utilizando (a) el registro de datos en bruto, (b) el dB-mel con `ref=max`, (c) MFCC-13 + delta + delta-delta.
   **困难。**                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             `power_to_db`, en AudioMNIST 上用微型 CNN 分类器比较 (a) 始日志-mail、(b) `ref=max`准确率──报告 top-1 准确率── MFCC-13 + delta + delta-delta 准确率──

> **【中文解读】**En el lenguaje de los términos "Lo que la gente dice" vs "Lo que realmente significa" se distingue entre el lenguaje diario y la definición técnica de significado.


## Términos clave .

| Term | What people say | What it actually means |
|------|-----------------|-----------------------|
| Frame | A slice | 25 ms chunk of waveform fed to one FFT. |
| Hop | Stride | Samples between consecutive frames; 10 ms is ASR default. |
| Window | Hann/Hamming thing | Point-wise multiplier that tapers the frame edges to zero. |
| STFT | Spectrogram generator | Framed + windowed FFT; yields time × frequency matrix. |
| Mel | Warped frequency | Log-perception scale; `m = 2595·log10(1 + f/700)`. |
| Filterbank | The matrix | Triangular filters that project STFT onto mel bins. |
| Log-mel | Whisper's input | `log(mel_spec + eps)`; standardized in 2026. |
| MFCC | Old-school feature | DCT of log-mel; 13 coeffs, decorrelated. |

| 术语 | 人们常说的 | 实际含义 |
|------|-----------|---------|
| 帧 | 一段切片 | 送入一次 FFT 的 25 ms 波形片段。 |
| 步长 | 步幅 | 连续帧之间的采样点数；10 ms 是 ASR 默认值。 |
| 窗函数 | Hann/Hamming 那个东西 | 将帧边缘逐渐缩减为零的逐点乘数。 |
| STFT | 频谱图生成器 | 分帧 + 加窗的 FFT；产生时间 × 频率矩阵。 |
| Mel | 扭曲的频率 | 对数感知尺度；`m = 2595·log10(1 + f/700)`。 |
| 滤波器组 | 那个矩阵 | 将 STFT 投影到 mel bin 的三角滤波器。 |
| Log-mel | Whisper 的输入 | `log(mel_spec + eps)`；2026 年标准化。 |
| MFCC | 老派特征 | log-mel 的 DCT；13 个系数，去相关。 |

> **【中文解读】**延伸阅读 proporciona un alto nivel de recursos para el aprendizaje profundo. Estos artículos y cursos son los referentes clásicos en el campo, adecuados para los lectores que necesitan una comprensión profunda.


## Más Leer más Leer más

- [Davis, Mermelstein (1980). Comparison of parametric representations for monosyllabic word recognition](https://ieeexplore.ieee.org/document/1163420) el documento de la MFCC.
  Davis、Mermelstein (1980) 单音节词识别的参数化表示比较MFCC 论文──
- [Stevens, Volkmann, Newman (1937). A Scale for the Measurement of the Psychological Magnitude Pitch](https://pubs.aip.org/asa/jasa/article-abstract/8/3/185/735757/) la escala mel original.
  Stevens Volkmann Newman (1937) 心理音高量级的尺度尺度 原始 mel 尺度──
- [OpenAI — Whisper source, log_mel_spectrogram](https://github.com/openai/whisper/blob/main/whisper/audio.py) leer la aplicación de referencia.
  OpenAIWhisper 源码,log_mel_spectrogram阅读参考实现──
- [librosa feature extraction docs](https://librosa.org/doc/main/feature.html) referencia para `mfcc`¿ Qué ?`melspectrogram`, y salta / ventana.
  librosa 特征提取文档`mfcc`¿Qué es esto?`melspectrogram`Y salta/ventana de referencia
- [NVIDIA NeMo — audio preprocessing](https://docs.nvidia.com/deeplearning/nemo/user-guide/docs/en/main/asr/asr_all.html#featurizers) tubería a escala de producción para los modelos Parakeet + Canary.
  NVIDIA NeMo音频预处理Parakeet + Canary 模型的生产级流水线──

> **【中文解读】**延伸阅读 proporciona recursos de alta calidad para el aprendizaje profundo, incluyendo artículos, tutorials y herramientas.

