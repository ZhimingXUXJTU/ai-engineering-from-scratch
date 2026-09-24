# Transformadores de audio  Arquitectura de susurros 音频 Transformer  Arquitectura de susurros

> El sonido es una imagen de frecuencia a lo largo del tiempo.

> **【中文解读】**Susurrar con el Transformer hacer语音识别和翻译──理解音频如何变成代号序列送进的Transformer──

**Type:** Study | **类型:** 学习
**Language:**¿ Qué pasa ?**语言:**Python
**Prerequisites:** Phase 7 · 05 (Full Transformer), Phase 7 · 08 (Encoder-Decoder), Phase 7 · 09 (ViT) | **前置知识:** Phase 7 · 05 (Full Transformer), Phase 7 · 08 (Encoder-Decoder), Phase 7 · 09 (ViT)
**Time:** ~45 minutes | **时间:** ~45 分钟

## El problema es la introducción del problema

Antes de Whisper (OpenAI, Radford et al. 2022), el reconocimiento automático de voz (ASR) de vanguardia significaba que los extractores de características de wav2vec 2.0 y HuBERT  se supervisan por sí mismos más una cabeza afinada.

> En el año 2022, los primeros sistemas de reconocimiento automático de idiomas (ASR) utilizaron las ondas 2.0 y HuBERT, pero la calidad de los datos era alta, y el nivel de reconocimiento de idiomas era muy alto.

Whisper hizo tres apuestas:

> Susurro hizo tres cosas:

1. **Train on everything.**680.000 horas de audio deficiente en 97 idiomas, sin un cuerpo académico limpio, sin etiquetas fonéticas.
   En inglés:**用一切数据训练。**680.000 horas de la red de Internet, en 97 idiomas.
2. **Multi-task single model.**Un decodificador entrenado conjuntamente en transcripción, traducción, detección de actividad de voz, ID de idioma y timestamping a través de tokens de tarea.
   En inglés:**单模型多任务。**Un descifrador a través de un token de tarea 联合训练转录、翻译、语音活动检测、语言识别和时间──
3. **Standard encoder-decoder transformer.**El codificador consume espectrogramas log-mail. El decodificador produce tokens de texto autoregresivamente.
   En inglés:**标准编码器-解码器 Transformer。**编码器消费 log-mail 频谱图──解码器自归生成文本代币──没有声码器,没有CTC,没有HMM──

El resultado: Whisper big-v3 es robusto en acentos, ruido y lenguajes que tienen datos de etiqueta limpia cero. Es el front-end de voz predeterminado para todos los asistentes de voz de código abierto y la mayoría de los comerciales en 2026.

> Resultado: El lenguaje de susurro grande-v3 a la voz, el ruido y los datos de zéro marcado tiene una robustez.

> **【中文解读】**Whisper's Three Big Innovations: 1) Used 680.000小时弱标注音频训练,覆盖 97 种语言; 2) 单模型多任务(转录、翻译、语种识别、时间); 3) 标准编码器-解码器 Transformer 架。音频被转构为 log-mail 频谱图(类似图像),编码器处理频谱特征,解码器生成文本。

## El concepto central.

![Whisper pipeline: audio → mel → encoder → decoder → text](../assets/whisper.svg)

### Paso 1  repetición + ventana

Audio a 16 kHz. Clip/pad a 30 segundos. Computa el espectrograma log-mel: 80 mel bin, 10 ms de paso → ~ 3.000 cuadros × 80 características. Esta es la "imagen de entrada" que Whisper ve.

> 音频采样率 16 kHz──剪剪/填充到30秒──计算日志-mail 频谱图:80 个梅尔频率 bin,10 ms 步长 → 约 3,000  × 80特征──这是Whisper 看到的"输入图像"──

### Paso 2  tronco convolucionario

Dos capas Conv1D con el núcleo 3 y el paso 2 reducen los 3.000 cuadros a 1.500.

> 两层 Conv1D(核大小 3,步长 2) reducirá 3,000  a 1,500── reducirá la longitud del tramo a la mitad sin aumentar demasiado los parámetros──

> **【拓展：Whisper 的多语言能力来源】**El susurro en 97 种语言、68万小时音频上训练, la capacidad multilingüe proviene de dos factores: 1) 超大规模的弱标注数据覆盖绝大多数语言; 2) 统一的 BPE 词表是GPT-2 词表的超集,天然支持多语言──decoder prompt 中的语言代币如`<|zh|>`) control de la lengua de salida, para que el mismo modelo pueda ejecutar las tareas de traducción o traducción.

### Paso 3  codificador

Un codificador de transformador de 24 capas (para grandes) en 1.500 pasos de tiempo. codificación posicional sinusoidal, autoatención, GELU FFN. Produce estados ocultos de 1.500 × 1.280 .

> Una versión de 24 niveles (gran) Transformer 编码器处理 1,500 个时间步──正弦位置编码、自注意力、GELU FFN── generar un estado oculto de 1,500 × 1,280 años──

### Paso 4  decodificador

Un decodificador de transformador de 24 capas. Produce automáticamente tokens de un vocabulario BPE que es un superconjunto de GPT-2 con algunos tokens especiales específicos de audio.

> Una 24 niveles Transformer 解码器──自归地从 BPE 词表生成代币,该词表是GPT-2 词表的超集,外加几个音频专用特殊代币──

### Paso 5  Tokens de tarea

El descifrador comienza con fichas de control que dicen al modelo qué hacer:

> Para controlar el token, abre y dile al modelo qué hacer.

```
<|startoftranscript|>  <|en|>  <|transcribe|>  <|0.00|>
```

o

```
<|startoftranscript|>  <|fr|>  <|translate|>   <|0.00|>
```

El modelo fue entrenado en esta convención. controlas tareas por prefijo. el equivalente de instrucción de 2026 pero aplicado al habla.

> 模型按这种约定训练──你通过前控制任务──这是指令微调在语音领域的等价──

> **【中文解读】**El mecanismo de control de tareas de Whisper es muy bueno: mediante el adición de tokens especiales en el dispositivo de descifrado`<|transcribe|>`O `<|translate|>`) para especificar el tipo de tarea. Es la "ordenada de la modificación" en la aplicación en el ámbito del lenguaje.

> **【拓展：Whisper 在语音助手中的应用】**El susurro es un componente básico de la IA de 2026 en el lenguaje. Desde el tiempo real el asistente de voz hasta la producción de vídeos, hasta la traducción de conferencias de varios idiomas, el susurro proporciona un sistema de comunicación de voz único. El susurro-turbo (en inglés: Whisper-turbo) reducirá la demora 8 veces, lo que hará posible el diálogo real.

### Paso 6  salida

Buscar en haz (ancho 5) con un umbral de log-prob.`<|notimestamps|>`El token está ausente.

> 束搜索(宽度 5)加对数概率值──当没有 `<|notimestamps|>`En cualquier caso, cada 0,02 segundos se hace una prueba de tiempo.

### Tamaños de susurros

| Model | Params | Layers | d_model | Heads | VRAM (fp16) |
|-------|--------|--------|---------|-------|-------------|
| 模型 | 参数量 | 层数 | d_model | 头数 | 显存 (fp16) |
| Tiny | 39M | 4 | 384 | 6 | ~1 GB |
| Base | 74M | 6 | 512 | 8 | ~1 GB |
| Small | 244M | 12 | 768 | 12 | ~2 GB |
| Medium | 769M | 24 | 1024 | 16 | ~5 GB |
| Large | 1550M | 32 | 1280 | 20 | ~10 GB |
| Large-v3 | 1550M | 32 | 1280 | 20 | ~10 GB |
| Large-v3-turbo | 809M | 32 | 1280 | 20 | ~6 GB (4-layer decoder) |

El decodificador de 32 capas se reduce a 4.8 veces más rápido con regresión de <1 punto WER.

> El gran v3-turbo(2024) reducirá el descifrador de 32 niveles a 4 niveles. La velocidad de descifrado aumentará 8 veces, WER 退化不到 1个百分点.

> **【拓展：音频 Transformer 的统一趋势】**语音识别(Whisper)、语音合成(VALL-E, Kokoro)、音乐生成(MusicGen) 都在转向 Transformer 架构──核心思路相同:将音频转换为频谱图或离散代币 序列,然后使用标准 Transformer 处理──这验证了 Transformer 作为通用序列建模器的地位──

### Lo que el susurro no hace

- No hay diarios, para eso se empareja con la nota de piano.
  No hay nadie que se quede en el lugar.
- No se transmite en tiempo real de forma nativa  la ventana de 30 segundos está fija.`faster-whisper`¿ Qué ?`WhisperX`) para el streaming a través de la superposición de VAD +.
  No hay ningún proceso de procesamiento de 30 segundos.`faster-whisper`¿Qué es esto?`WhisperX`) a través de VAD + 重叠实现流式处理──
- No hay contexto de forma larga más allá de 30 s sin fragmentos externos. Funciona bien en la práctica porque el habla humana rara vez necesita contexto de largo alcance para la transcripción.
  No hay partes externas de los bloques que no admiten el formato de 30 segundos o más en el texto siguiente.

### 2026 paisaje

| Task | Model | Notes |
|------|-------|-------|
| 任务 | 模型 | 备注 |
| English ASR | Whisper-turbo, Moonshine | Moonshine is 4× faster on edge |
| 英语 ASR | Whisper-turbo, Moonshine | Moonshine 在边缘设备上快 4 倍 |
| Multilingual ASR | Whisper-large-v3 | 97 languages |
| 多语言 ASR | Whisper-large-v3 | 97 种语言 |
| Streaming ASR | faster-whisper + VAD | 150 ms latency targets achievable |
| 流式 ASR | faster-whisper + VAD | 可实现 150ms 延迟目标 |
| TTS | Piper, XTTS-v2, Kokoro | Encoder-decoder pattern, but Whisper-shaped |
| TTS | Piper, XTTS-v2, Kokoro | 编码器-解码器模式，但类似 Whisper |
| Audio + language | AudioLM, SeamlessM4T | Text tokens + audio tokens in one transformer |
| 音频 + 语言 | AudioLM, SeamlessM4T | 文本 token + 音频 token 在一个 Transformer 中 |

## Construye y realiza.
```figure
n5-mel-decode
```

## Construye el mismo

¿ Qué ?`code/main.py`No entrenamos Whisper, construimos el log-mail espectrogram pipeline + task-token prompt formator. Esas son las piezas que realmente tocan en la producción.

> 参见 `code/main.py` Nosotros no entrenamos Susurro  Nosotros construimos un registro de correo  un canal de frecuencias  un token de tareas  un formato de sugerencias  Estas son las partes del contacto real que tienes en la producción 

### Paso 1: sintetizar el audio

Generar una onda seno-segunda a 440 Hz muestrada a 16 kHz. 16.000 muestras.

> Se produce una onda de 440 Hz de 1 segundo, de 16 kHz, de 16.000 puntos de toma.

### Paso 2: Espectograma de registro de correo electrónico (simplificado)

El espectrograma de mel completo necesita FFT. hacemos un marco simplificado + versión de energía por marco que muestra la tubería sin necesidad de`librosa`¿Qué es esto ?

> 完整的梅尔频谱图需要FFT──我们做一个简化分+逐能量版本,无需`librosa`Es decir, el

```python
def frame_signal(x, frame_size=400, hop=160):
    frames = []
    for start in range(0, len(x) - frame_size + 1, hop):
        frames.append(x[start:start + frame_size])
    return frames
```

En el marco = 25 ms, en el hop = 10 ms.

>  = 25 ms,步长 = 10 ms── corresponde con Whisper's window── cada energía utilizada para la enseñanza, sustituyendo la frecuencia de la transmisión.

### Paso 3: envasado a 30 s

Whisper siempre procesa trozos de 30 segundos.

> Susurrar 总是处理 30 segundos de分块──将频谱图填充或剪) hasta 3.000 ──

### Paso 4: crear los tokens de solicitud

```python
def whisper_prompt(lang="en", task="transcribe", timestamps=True):
    tokens = ["<|startoftranscript|>", f"<|{lang}|>", f"<|{task}|>"]
    if not timestamps:
        tokens.append("<|notimestamps|>")
    return tokens
```

Esa es toda la superficie de control de tareas.

> Ésta es la tarea de todo el control de la interfaz.

## Usalo con el marco de ejecución

```python
import whisper
model = whisper.load_model("large-v3-turbo")
result = model.transcribe("meeting.wav", language="en", task="transcribe")
print(result["text"])
print(result["segments"][0]["start"], result["segments"][0]["end"])
```

Más rápido, compatible con OpenAI:

> Más rápidamente, con OpenAI compatible:

```python
from faster_whisper import WhisperModel
model = WhisperModel("large-v3-turbo", compute_type="int8_float16")
segments, info = model.transcribe("meeting.wav", vad_filter=True)
for s in segments:
    print(f"{s.start:.2f} - {s.end:.2f}: {s.text}")
```

**When to pick Whisper in 2026:**

> **2026 年何时选择 Whisper：**

- RAS multilingüe con un modelo.
  En español: "Con un modelo de ASR".
- Una robusta transcripción de ruidosos y diversos sonidos.
  Traducción:La voz de los niños en el mundo de la música.
- Investigación / prototipo ASR  punto de partida más rápido.
  La primera de las primeras generaciones de la lengua inglesa fue la de la lengua inglesa.

**When to pick something else:**

> **何时选择其他方案：**

- Ultra baja latencia streaming en el borde Moonshine supera a Whisper en calidad igualada.
  Traducción:Más tarde que el tiempo de la luz de la luna.
- AI de conversación en tiempo real que necesita <200 ms  ASR de transmisión dedicada.
  Needs <200ms of real time dialogue AI专用流式 ASR──
- Diario de altavoces  Susurro no hace esto; paralizador en la nota de piano.
  China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China:

## Envíe el producto .

¿ Qué ?`outputs/skill-asr-configurator.md`La habilidad elige un modelo ASR, parámetros de decodificación y una tubería de procesamiento previo para una nueva aplicación de voz.

> 参见 `outputs/skill-asr-configurator.md`◊ Esta habilidad se utiliza para la nueva aplicación de los idiomas seleccionar modelos de ASR, descifrar los parámetros y el preprocesamiento de tubos.

## Los ejercicios.

1. **Easy.**- ¿ Qué ?`code/main.py`Confirmar el recuento de fotogramas para una señal de 1 segundo a 16 kHz con 10 ms saltar es ~ 100 fotogramas.
   Traducción:运行`code/main.py` Confirmar 1 秒 señal en 16 kHz、10 ms 步长下约100 ──30 秒:约3,000 ──
2. **Medium.**Construir el espectro completo de log-mel usando `numpy.fft`Verifique si 80 mil contenedores coinciden .`librosa.feature.melspectrogram(n_mels=80)`dentro del error numérico.
   En inglés:`numpy.fft`构建完整的日志频谱图――验证 80 个日志频率bin                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        `librosa.feature.melspectrogram(n_mels=80)`En el rango de los errores de valor coinciden en la misma.
3. **Hard.**Implemente inferencia de transmisión: fragmento de audio en ventanas de 10 segundos con superposición de 2 segundos, ejecuta Whisper en cada fragmento, fusione las transcripciones. Mide la tasa de error de palabra frente a un solo paso en una muestra de podcast de 5 minutos.
   En el caso de los programas de televisión de 5 minutos, el número de usuarios que han recibido la información de la red de televisión de la red de televisión de la red de televisión de la red de televisión de la red de televisión de la red de televisión de la red de televisión de la red de televisión de la red de televisión de la red de televisión de la red de televisión de la red de televisión de la red de televisión de la red de televisión de la red de televisión de la red de televisión de la red de televisión de la red de televisión de la red de televisión de la red de televisión de la red de televisión de la red de televisión de la red de televisión de la red de televisión de la red de televisión de la red de televisión de la red de televisión de la red de televisión de la red de televisión de la red de televisión de la red de televisión de la red de televisión de la red de televisión de la red de televisión de la red de televisión de la red de televisión de la red de televisión de la red de televisión de la red de televisión de la red de televisión de la red de televisión de televisión de la red de televisión de la red de televisión de televisión de la red de televisión de televisión de la red de televisión de televisión de la red de televisión de televisión de la red de televisión de televisión de la red de televisión de televisión de la red de televisión de televisión de la red de televisión de televisión de la televisión de la red de televisión de televisión de la televisión de la televisión de la televisión de China de China de China de China de China de China de China de China de China de 9 años más se hacierra en más.

## Términos clave .

| Term | What people say | What it actually means |
|------|-----------------|-----------------------|
| 术语 | 通俗说法 | 实际含义 |
| Mel spectrogram | "Audio image" | 2D representation: frequency bins on one axis, time frames on the other; log-scaled energy per cell. |
| 梅尔频谱图 | "音频图像" | 2D 表示：一个轴是频率 bin，另一个是时间帧；每个单元是对数缩放的能量。 |
| Log-mel | "What Whisper sees" | Mel spectrogram passed through log; approximates human perception of loudness. |
| Log-mel | "Whisper 看到的" | 梅尔频谱图取对数；近似人类对响度的感知。 |
| Frame | "One time slice" | A 25 ms window of samples; overlapping at 10 ms stride. |
| 帧 | "一个时间切片" | 25 ms 的采样窗口；10 ms 步长重叠。 |
| Task token | "Prompt prefix for speech" | Special tokens like `<\|transcribe\|>` / `<\|translate\|>` in the decoder prompt. |
| 任务 token | "语音的提示前缀" | 解码器提示中的特殊 token，如 `<\|transcribe\|>` / `<\|translate\|>`。 |
| Voice activity detection (VAD) | "Find the speech" | Gate that removes silence before ASR; cuts cost massively. |
| 语音活动检测 (VAD) | "找到语音" | 在 ASR 之前去除静音的门控；大幅降低成本。 |
| CTC | "Connectionist Temporal Classification" | Classic ASR loss for alignment-free training; Whisper does NOT use it. |
| CTC | "连接主义时间分类" | 经典的 ASR 对齐无关训练损失；Whisper 不使用它。 |
| Whisper-turbo | "Small decoder, full encoder" | large-v3 encoder + 4-layer decoder; 8× faster decoding. |
| Whisper-turbo | "小解码器，全编码器" | large-v3 编码器 + 4 层解码器；解码速度提高 8 倍。 |
| Faster-whisper | "The production wrapper" | CTranslate2 reimplementation; int8 quantization; 4× faster than OpenAI's reference. |
| Faster-whisper | "生产封装器" | CTranslate2 重新实现；int8 量化；比 OpenAI 参考实现快 4 倍。 |

## Más Leer más Leer más

- [Radford et al. (2022). Robust Speech Recognition via Large-Scale Weak Supervision](https://arxiv.org/abs/2212.04356) Papel de susurros.
  El lenguaje de la lengua se traduce en inglés como "sobre la lengua".
- [OpenAI Whisper repo](https://github.com/openai/whisper) código de referencia + pesos del modelo.`whisper/model.py`para ver el código de base Conv1D + codificador + decodificador de arriba a abajo en ~ 400 líneas.
  China OpenAI Whisper 代码仓库, alrededor de 400 行代码展示 Conv1D stem + 编码器 + 解码器──
- [OpenAI Whisper — `whisper/decoding.py`](https://github.com/openai/whisper/blob/main/whisper/decoding.py) la lógica de búsqueda de haces + ficha de tarea descrita en los pasos 56 está aquí; 500 líneas, completamente legibles.
  En inglés, el nombre de la palabra "tónico de tarea" se traduce en "tónico de tarea" (tónico de tarea) 逻辑的实现,500 行代码,完全可读──.
- [Baevski et al. (2020). wav2vec 2.0: A Framework for Self-Supervised Learning of Speech Representations](https://arxiv.org/abs/2006.11477) precursor; todavía cuenta con SOTA en algunas configuraciones.
  El uso de la palabra "Whisper" en algunos casos es un fenómeno que se ha visto en el pasado.
- [SYSTRAN/faster-whisper](https://github.com/SYSTRAN/faster-whisper) envase de producción, 4 veces más rápido que el de referencia.
  En el caso de los productos de la industria de la producción, el precio de producción de los productos de la industria de la producción de la producción de la producción de la producción de la producción de la producción de la producción de la producción de la producción de la producción de la producción de la producción de la producción de la producción de la producción de la producción de la producción de la producción de la producción de la producción de la producción de la producción de la producción de la producción de la producción de la producción de la producción de la producción de la producción de la producción de la producción de la producción de la producción de la producción de la producción de la producción de la producción de la producción de la producción de la producción de la producción de la producción de la producción de la producción de la producción de la producción de la producción de la producción de la producción de la producción de la producción de la producción de la producción de la producción de la producción de la producción de la producción de la producción de la producción de la producción de la producción de la producción de la producción de la producción de la producción de la producción de la producción de la producción de la producción de la producción de la producción de la producción de la producción de la producción de la producción de la producción de la producción de la producción de la producción de la producción de la producción de la producción de la producción de la producción de la producción de la producción de la producción de la producción de la producción de la producción de la producción de la producción de la producción de la producción de la producción de la producción de la producción de la producción de la producción de la producción de la producción de la producción de la producción de la producción de la producción de la producción de la producción de la producción de la producción de la producción de la producción de la producción de la producción de la producción de la producción de la producción de la producción de la producción de la producción de la producción de la producción de la producción de la producción de la producción de la producción de la producción de la producción de la producción de la producción de la producción de la producción de la producción de la producción de la producción de la producción de la producción de la producción de la producción de la producción de la producción de la producción de la producción de la producción de la producción de la producción de la producción de la producción de la producción de la producción de la producción de la de la de la producción de la producción de la de la de la de la de la de la de la de la de la de la de la de la de la de
- [Jia et al. (2024). Moonshine: Speech Recognition for Live Transcription and Voice Commands](https://arxiv.org/abs/2410.15608) 2024 ASR amigable con los bordes, en forma de susurro pero más pequeño.
  China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China:
- [HuggingFace blog — "Fine-Tune Whisper For Multilingual ASR with 🤗 Transformers"](https://huggingface.co/blog/fine-tune-whisper) receta de ajuste fino canónico, incluido el preprocesador del espectrograma mel y el manejo de las sellas de tiempo de los tokens.
  China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China:
- [HuggingFace `modeling_whisper.py`](https://github.com/huggingface/transformers/blob/main/src/transformers/models/whisper/modeling_whisper.py) Implementación completa (encodificador, decodificador, atención cruzada, generación) que refleje el diagrama de arquitectura de la lección.
  En el caso de los estudiantes de la escuela de la Universidad de San Francisco, el programa de formación de estudiantes de la Universidad de San Francisco, el programa de formación de estudiantes de la Universidad de San Francisco, el programa de formación de estudiantes de la Universidad de San Francisco, el programa de formación de estudiantes de la Universidad de San Francisco, el programa de formación de estudiantes de la Universidad de San Francisco, el programa de formación de estudiantes de la Universidad de San Francisco, el programa de formación de estudiantes de la Universidad de San Francisco, el programa de formación de estudiantes de la Universidad de San Francisco, el programa de la Universidad de San Francisco, el programa de formación de estudiantes de la Universidad de San Francisco, el programa de la Universidad de San Francisco, el programa de la Universidad de San Francisco, el programa de la Universidad de San Francisco, el programa de la Universidad de San Francisco, el programa de la Universidad de San Francisco, el cual se desarrolla en el año 2000.
