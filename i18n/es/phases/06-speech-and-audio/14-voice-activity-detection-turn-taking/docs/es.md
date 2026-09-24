# Detección de actividad de voz y toma de vueltas  Silero, Cobra y el truco de Flush 语音活动检测与轮次切换

> Cada agente de voz vive o muere por dos decisiones: ¿habla el usuario ahora y están terminados? VAD responde a la primera. La detección de giros (VAD + silencio-hangower + modelo de punto final semántico) responde a la segunda.

> **【中文解读】**El éxito de cada asistente de voz depende de dos juicios: ¿Usuario ahora está hablando? ¿Usuario dice terminado?

**Type:** Build | **类型:** 构建
**Languages:** Python | **语言:** Python
**Prerequisites:** Phase 6 · 11 (Real-Time Audio), Phase 6 · 12 (Voice Assistant) | **前置知识:** 阶段 6 · 11（实时音频），阶段 6 · 12（语音助手）
**Time:** ~45 minutes | **预计用时:** ~45 分钟

## El problema es la introducción del problema

Tres decisiones distintas que un agente de voz toma en cada 20 ms:

> El asistente de voz necesita hacer tres juicios diferentes en cada 20 ms de un bloque de audio:

> **【中文解读】**La pregunta planteada en este capítulo es: ¿cómo entender y aplicar correctamente esta tecnología en la ingeniería real? Comprender el contexto de la cuestión ayuda a comprender los puntos clave de decisión del tipo de selección técnica. En los sistemas de IA reales, el tipo de selección técnica errónea suele ser más alto que el costo de error de la realización de detalles.


1. **Is this frame speech?**- VAD, binario, por marco.
   En inglés, el idioma es el idioma de la lengua.
2. **Has the user started a new utterance?** detección de inicio.
   ¿Ha comenzado un nuevo proceso de investigación?
3. **Has the user finished?** apuntar al final (turn-end).
   En inglés, el usuario dice que está terminado.

La respuesta ingenua (umbral de energía) falla en cualquier ruido  tráfico, teclados, charlatos de la multitud. La respuesta 2026: Silero VAD (abierto, profundamente aprendido) + un modelo de detección de turno (indicación semántica de extremo) + una resaca de silencio calibrada por VAD.

> 朴素的答案(能量值) bajo cualquier ambiente ruido, todos fracasarán交通声、键盘声、人群杂声。 2026 años de respuesta es: Silero VAD(开源、深度学习) + 轮次检测模型(语义端点检测) + VAD 校准的静音持续等──

## El concepto central.

> **【中文解读】**Este capítulo presenta los conceptos y teorías básicos. La comprensión de estos conceptos es el prerrequisito de la realización posterior de la actividad, y también el conocimiento de los puntos de alta frecuencia de la entrevista y la práctica de la ingeniería.


![VAD cascade: energy → Silero → turn-detector → flush trick](../assets/vad-turn-taking.svg)

### La cascada de tres niveles de VAD

> Tres clases de VAD

**Tier 1: energy gate.**El límite RMS es de -40 dBFS, filtra el silencio obvio pero dispara cualquier ruido por encima del límite.

> **第一层：能量门控。**El método más barato: RMS                                                                                                                                                                                                                                                            

**Tier 2: Silero VAD**(2020-2026, MIT). 1M parámetros. Entrenado en más de 6000 idiomas. Se ejecuta en ~1 ms por 30 ms de trozo en un solo hilo de CPU.

> **第二层：Silero VAD**(2020-2026, MIT 许可) ∙100.000参数── en 6000+ 种语言上训练── en una sola CPU 线程 每30 ms 块约1 ms 推理时间──5% FPR 下 TPR 达 87.7%──开源方案的默认选择──

**Tier 3: semantic turn detector.**El modelo de detección de turno de LiveKit (2024-2026) o su propio clasificador pequeño. Distingue "pausa a mitad de oración" de "hablar terminado".

> **第三层：语义轮次检测器。**Modelo de revisión de la serie de LiveKit (en inglés) (en inglés) (en inglés) (en inglés) (en inglés) (en inglés) (en inglés) (en inglés) (en inglés) (en inglés) (en inglés) (en inglés) (en inglés) (en inglés) (en inglés) (en inglés) (en inglés) (en inglés) (en inglés) (en inglés) (en inglés) (en inglés) (en inglés) (en inglés) (en inglés) (en inglés) (en inglés) (en inglés) (en inglés) (en inglés) (en inglés) (en inglés) (en inglés) (en inglés) (en inglés) (en inglés) (en inglés) (en inglés) (en inglés) (en inglés) (en inglés) (en inglés) (en inglés) (en inglés) (en inglés) (en inglés) (en inglés) (en inglés) (en inglés) (en inglés) (en inglés) (en inglés) (en inglés) (en inglés) (en inglés) (en inglés) (en inglés) (en inglés) (en) (en) (en) (en) (en) (en) (en) (en) (en) (en) (en) (en) (en) (en) (en) (en) (en) (en) (en) (en) (en) (en) (en) (en) (en) (en) (en) (en) (en) (en) (en) (en) (en) (en) (en) (en) (en) (en) (en) (en) (en) (en) (en) (en) (en) (en) (en) (en) (en) (en) (en) (en) (en) (en) (en) (en) (en) (en) (en) (en) (en) (en) (en) (en) (en) (en) (en) (en) (en) (en) (en) (en) (en) (en) (en) (en) (en) (en)

### Parámetros clave y sus valores predeterminados

> 关键参数 y su valor de usuario

- **Threshold.**Silero produce una probabilidad; clasificar el habla en &gt; 0.5 (default) o &gt; 0.3 (sensitivo). umbral más bajo = menos clips de primera palabra, más falsos positivos.
  En inglés:**阈值。**Silero 输出概率值;以 > 0.5(默认) o > 0.3(敏感模式) 分类语音──值越低 = 首词截断越少,但误报越多──
- **Minimum speech duration.**Rechazar el habla menor a 250 ms  usualmente tos o ruido de la silla.
  En inglés:**最小语音时长。**拒绝短于250 ms 的语音通常是咳或椅子噪音──
- **Silence hangover (end-pointing).**Después de que el VAD vuelva a 0, espere 500-800 ms antes de declarar el final del giro. Demasiado corto → interrumpir al usuario. Demasiado largo → se siente lento.
  En inglés:**静音持续等待（端点检测）。**VAD vuelve hasta 0 后, espera 500-800 ms Reanunciar la última vez que termina.
- **Pre-roll buffer.**Mantenga 300-500 ms de audio antes de que el VAD dispare.
  En inglés:**预滚缓冲。**En VAD 触发前保留 300-500 ms 音频──防止""字被截断──

### El truco de la roca (Kyutai 2025)

Los modelos STT en streaming tienen un retraso de vista hacia adelante (500 ms para Kyutai STT-1B, 2,5 s para STT-2.6B). Normalmente esperarías tanto tiempo después del final del discurso para la transcripción.**send a flush signal to the STT**El proceso de STT se realiza en tiempo real de ~4×, por lo que el buffer de 500 ms termina en ~125 ms.

> 流式 STT 模型有前视延迟(Kyutai STT-1B 为500 ms,STT-2.6B 为2.5 s)  Usualmente necesitas esperar tanto tiempo después del final del discurso para obtener resultados de la transmisión.**向 STT 发送刷新信号**, forzada de salida inmediata;. STT a aproximadamente 4 veces la velocidad de procesamiento real, por lo que 500 ms 缓冲区 en aproximadamente 125 ms en completado。

End-to-end: 125 ms VAD + flush STT = latencia de conversación.

> 端到端:125 ms VAD + 刷新 STT = 对话级延迟──

### Comparación de las VAD 2026

> VAD por el año 2026

| VAD | TPR @ 5% FPR | Latency | License |
|-----|--------------|---------|---------|
| WebRTC VAD (Google, 2013) | 50.0% | 30 ms | BSD |
| Silero VAD (2020-2026) | 87.7% | ~1 ms | MIT |
| Cobra VAD (Picovoice) | 98.9% | ~1 ms | commercial |
| pyannote segmentation | 95% | ~10 ms | MIT-ish |

Silero es el correcto por defecto. Cobra es la actualización de cumplimiento / precisión.

> Silero es una opción de elevación de la calidad de COBRA, basada en la energía, y no tiene lugar en el entorno de producción de 2026

> **【中文解读】**Este capítulo a través del código de la implementación de algoritmos centrales de cero. Este método "desde cero" puede ayudar a entender el principio detrás del marco, no se encuentra en la caja negra cuando se encuentran problemas.

> **【拓展：语音 AI 的产品化】**La tecnología de voz se enfrenta a un desafío único en la productorización: diferentes voces, ruidos de contexto, remota recogida, muchos hablar, etc.

> **【拓展：多语言语音技术】**Las características de los idiomas de todo el mundo son muy diferentes: el sonido de los idiomas de todo el mundo (como el chino) es alto, el lenguaje de bajo recurso es poco capacitado.

> **【拓展：语音隐私与安全】**语音数据 contiene una gran cantidad de información personal privada ([[音纹]], diálogo contenido) ◦ profundidad falsificación (Deepfake) 语音技术 (语音技术) puede ser utilizada para fraude (音频水印) 音频水印 (音频水印) 音纹水标 (音符标) 声纹反欺诈 (音纹反欺诈) ]] ]] ]] ]] ]] ]] ]] ]] ]] ]] ]] ]] ]] ]] ]] ]] ]] ]] ]] ]] ]] ]] ]] ]] ]] ]] ]] ]] ]] ]] ]] ]] ]] ]] ]] ]] ]] ]] ]] ]] ]] ]] ]] ]] ]] ]] ]] ]] ]] ]] ]] ]] ]] ]] ]] ]] ]] ]] ]] ]] ]] ]] ]] ]] ]] ]] ]] ]] ]] ]] ]] ]] ]] ]] ]] ]] ]] ]] ]] ]] ]] ]] ]] ]] ]] ]] ]] ]] ]] ]] ]] ]] ]] ]] ]] ]] ]]





## Construye y realiza.
```figure
sp-vad-cascade
```

## Construye el mismo

### Paso 1: la puerta de energía

> Paso 1: energía en control

```python
def energy_vad(chunk, threshold_dbfs=-40.0):
    rms = (sum(x * x for x in chunk) / len(chunk)) ** 0.5
    dbfs = 20.0 * math.log10(max(rms, 1e-10))
    return dbfs > threshold_dbfs
```

### Paso 2: Silero VAD en Python

> Paso 2: en Python usar Silero VAD

```python
from silero_vad import load_silero_vad, get_speech_timestamps

vad = load_silero_vad()
audio = torch.tensor(waveform_16k, dtype=torch.float32)
segments = get_speech_timestamps(
    audio, vad, sampling_rate=16000,
    threshold=0.5,
    min_speech_duration_ms=250,
    min_silence_duration_ms=500,
    speech_pad_ms=300,
)
for s in segments:
    print(f"{s['start']/16000:.2f}s - {s['end']/16000:.2f}s")
```

### Paso 3: máquina de estado de turno

> Paso 3: Rúa de final de estado

```python
class TurnDetector:
    def __init__(self, silence_hangover_ms=500, min_speech_ms=250):
        self.state = "idle"
        self.speech_ms = 0
        self.silence_ms = 0
        self.silence_hangover_ms = silence_hangover_ms
        self.min_speech_ms = min_speech_ms

    def update(self, is_speech, chunk_ms=20):
        if is_speech:
            self.speech_ms += chunk_ms
            self.silence_ms = 0
            if self.state == "idle" and self.speech_ms >= self.min_speech_ms:
                self.state = "speaking"
                return "START"
        else:
            self.silence_ms += chunk_ms
            if self.state == "speaking" and self.silence_ms >= self.silence_hangover_ms:
                self.state = "idle"
                self.speech_ms = 0
                return "END"
        return None
```

### Paso 4: el esqueleto de trucos de la roza

> Paso 4: actualizar las nuevas técnicas de código de marco

```python
def flush_on_end(stt_client, audio_buffer):
    stt_client.send_audio(audio_buffer)
    stt_client.send_flush()
    return stt_client.recv_transcript(timeout_ms=150)
```

> **【中文解读】**Este capítulo muestra cómo utilizar un marco maduro (como PyTorch、HuggingFace, etc.) para aplicar rápidamente esta tecnología. En los proyectos reales, se realiza con prioridad el uso de un marco experimentado, se pueden reducir errores y mejorar la eficiencia de desarrollo.


STT (Kyutai, Deepgram, AssemblyAI) debe soportar el flush para que esto funcione.

> STT(Kyutai、Deepgram、AssemblyAI) debe apoyar el flush 才能使此技巧生效──Whisper 流式不支持它是基于块的,总是等待完整块──




> **【拓展：语音与情感计算】**语音 no sólo transmite información escrita, también lleva una rica cantidad de señales emocionales (en inglés: voice signal) 语调、语速、音高变化) 情感语音识别 (en inglés: speech emotion recognition, SER) 语音 no solo transmite información escrita, sino que también lleva una gran cantidad de señales emocionales (en inglés: voice signal). 语音 tiene una amplia aplicación en el campo de la evaluación de calidad de los clientes, la vigilancia de la salud mental, la educación inteligente, etc.  Los modelos actuales de SOTA se basan en modelos de entrenamiento de las ondas 2vec 2.0 o HuBERT.

## Usalo con el marco de ejecución

| Situation | VAD choice |
|-----------|-----------|
| Open, fast, general / 开源、快速、通用 | Silero VAD |
| Commercial call center / 商业呼叫中心 | Cobra VAD |
| On-device (phone) / 端侧（手机） | Silero VAD ONNX |
| Research / diarization / 研究/说话人日志 | pyannote segmentation |
| Zero-dependency fallback / 零依赖后备方案 | WebRTC VAD（传统） |
| Need turn-ending quality / 需要轮次结束质量 | Silero + LiveKit 轮次检测器分层 |

Regla de oro: nunca envíe VAD sólo de energía a menos que realmente no tenga otra opción.

> 經驗法则: a menos que realmente no haya otra opción, entonces nunca te metas en línea basado sólo en la energía VAD。



## Las trampas

> 常见陷

- **Fixed threshold.**Funciona en silencio, falla en ruido, calibra en el dispositivo o cambia a Silero.
  En inglés:**固定阈值。**En un ambiente tranquilo, vale la pena, en un ambiente inestable, no puede ser.
- **Too-short silence hangover.**El agente interrumpe la mitad de la oración. 500-800 ms es el punto ideal para el discurso de conversación.
  En inglés:**静音持续等待过短。**助手在句子中打断用户──500-800 ms es el mejor alcance de diálogo语音──
- **Too-long hangover.**Se siente lento. Prueba A/B con usuarios objetivo.
  En inglés:**静音持续等待过长。**感觉迟──与目标用户进行A/B 测试──
- **No pre-roll buffer.**Los primeros 200-300 ms de audio del usuario se pierden.
  En inglés:**没有预滚缓冲。**Usuario de audio de los primeros 200-300 ms                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    
- **Ignoring semantic endpointing.**"Hmm, déjame pensar"... contiene largas pausas. Los usuarios odian ser cortados en medio de la reflexión.
  En inglés:**忽略语义端点检测。**",让我想想......" contiene un largo parado.

> **【中文解读】**Este capítulo se centra en cómo se puede implementar el modelo como producto disponible. Desde el modelo original hasta el sistema de producción, se deben considerar múltiples dimensiones de optimización de rendimiento, tratamiento de errores, control, etc.


## Envíe el producto .

Salvo como`outputs/skill-vad-tuner.md`Seleccione el modelo VAD, el umbral, la resaca, la estrategia de pre-rollo y detección de turno para una carga de trabajo.

> 保存为                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           `outputs/skill-vad-tuner.md`◊ para una carga de trabajo seleccionar VAD 模型、值、静音持续等待、预滚缓冲和轮次检测策略──

## Los ejercicios.

1. **Easy.**- ¿ Qué ?`code/main.py`Simula una secuencia de habla + silencio + habla + tos y prueba tres niveles de VAD.
   En inglés:**简单。**运行                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           `code/main.py`∼ Se parece a un segmento de语音 + 静音 + 语音 + 咳的序列,并测试三层 VAD──
2. **Medium.**Instalar`silero-vad`, procesar una grabación de 5 minutos, ajustar el umbral para minimizar los clips de primera palabra y los disparadores falsos.
   En inglés:**中等。**Instalación`silero-vad`, tratamiento un apartado 5 minutos de grabación, ajuste valor para minimizar el primer corte y error de la palabra                                                                                                                                                                                                                                                 
3. **Hard.**Construir un mini detector de giras: Silero VAD + una MLP de 3 capas en las últimas 10 palabras (utilizar transformadores de oraciones). Entrenar en un conjunto de datos de giras final etiquetado a mano.
   En inglés:**困难。**Construir un pequeño revisor de rutas: Silero VAD +  basado en 10 个近词嵌入的 3 层 MLP(utilizando transformadores de oraciones) ⋅ en el manual de etiquetado de rutas de data集上训练──比纯Silero 方案 F1 高 10%──

> **【中文解读】**En el lenguaje de los términos "Lo que la gente dice" vs "Lo que realmente significa" se distingue entre el lenguaje diario y la definición técnica de significado.


## Términos clave .

| Term | What people say | What it actually means |
|------|-----------------|-----------------------|
| VAD | Voice detector | Binary per-frame: is this speech? / 逐帧二分类：这是语音吗？ |
| Turn detection | End-pointing | VAD + silence-hangover + semantic endpoint. / VAD + 静音持续 + 语义端点 |
| Silence hangover | Wait-after-speech | Time to wait before declaring turn end; 500-800 ms. / 宣布轮次结束前的等待时间；500-800 ms |
| Pre-roll | Pre-speech buffer | Keep 300-500 ms audio before VAD fires. / 在 VAD 触发前保留 300-500 ms 音频 |
| Flush trick | Kyutai hack | VAD → flush-STT → 125 ms instead of 500 ms delay. / VAD → 刷新 STT → 125 ms 而非 500 ms 延迟 |
| Semantic endpoint | "Did they mean to stop?" | ML classifier that looks at words, not just silence. / 看词汇而非仅看静音的 ML 分类器 |
| TPR @ FPR 5% | ROC point | Standard VAD benchmark; 87.7% for Silero, 50% WebRTC. / 标准 VAD 基准；Silero 87.7%，WebRTC 50% |

> **【中文解读】**延伸阅读 proporciona un alto nivel de recursos para el aprendizaje profundo. Estos artículos y cursos son los referentes clásicos en el campo, adecuados para los lectores que necesitan una comprensión profunda.


## Más Leer más Leer más

- [Silero VAD](https://github.com/snakers4/silero-vad) el VAD de referencia abierto.
  Silero VAD                                                                                                                                                                                                                                                             
- [Picovoice Cobra VAD](https://picovoice.ai/products/cobra/) líder en precisión comercial.
  El primer ministro de la República de China, Juan Carlos I, ha sido el primer ministro de la República de China.
- [Kyutai — Unmute + flush trick](https://kyutai.org/stt) el truco de ingeniería sub-200 ms.
  KyutaiUnmute + 刷新技巧亚 200 ms 的工程技巧──
- [LiveKit — turn detection](https://docs.livekit.io/agents/logic/turns/) Endpointing semántico en la producción.
  En la producción de los productos de la producción de los productos de la producción de los productos de la producción de los productos de la producción de la producción de los productos de la producción de la producción de los productos de la producción de la producción de los productos de la producción de la producción de la producción de los productos de la producción de la producción de la producción de los productos de la producción de la producción de la producción de la producción de la producción de productos de la producción de la producción de la producción de la producción de la producción de la producción de productos de la producción de la producción de la producción de la producción de la producción de la producción de la producción de la producción de la producción de la producción de la producción de la producción de la producción de la producción de la producción de la producción de la producción de la producción de la producción de la producción de la producción de la producción de la producción de la producción de la producción de la producción de la producción de la producción de la producción de la producción de la producción de la producción de la producción de la producción de la producción de la producción de la producción de la producción de la producción de la producción de la producción de la producción de la producción de la producción de la producción de la producción de la producción de la producción de la producción de la producción de la producción de la producción de la producción de la producción de la producción de la producción de la producción de la producción de la producción de la producción de la producción de la producción de la producción de la producción de la producción de la producción de la producción de la producción de la producción de la producción de la producción de la producción de la producción de la producción de la producción de la producción de la producción de la producción de la producción de la producción de la producción de la producción de la producción de la producción de la producción de la producción de la producción de la producción de la producción de la producción de la producción de la producción de la producción de la producción de la producción de la producción de la producción de la producción de la producción de la producción de la producción de la producción de la producción de la producción de la producción de la producción de la producción de la producción de la producción de la producción de la producción de la producción de la producción de la de la producción de la de la de la producción de la de la de la de la de los productos de la producción de la de la producción de la cubierna.
- [WebRTC VAD](https://webrtc.googlesource.com/src/) el nivel de base heredado.
  WebRTC VAD tradicional
- [pyannote segmentation](https://github.com/pyannote/pyannote-audio) Segmentación de grado de diarización.
  segmentación de notas de pián 说话人日志级别的分分──

> **【中文解读】**延伸阅读 proporciona recursos de alta calidad para el aprendizaje profundo, incluyendo artículos, tutorials y herramientas.

