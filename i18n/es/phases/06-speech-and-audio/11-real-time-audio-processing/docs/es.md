# Procesamiento de audio en tiempo real                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                      

> Los oleoductos de lote procesan un archivo. Los oleoductos en tiempo real procesan los próximos 20 milisegundos antes de que lleguen los próximos 20. Cada IA conversacional, estudio de transmisión y bot de telefonía vive y muere con este presupuesto de latencia.

> **【中文解读】**批处理流水线处理文件,实时流水线在下20毫秒到达之前处理完整了这20毫秒──每一个对话式AI、广播系统和电话机器人都在这个延迟预算中存活死死――实时音频处理是语音AI落地的关键工程挑战──

**Type:** Build | **类型:** 构建
**Languages:** Python | **语言:** Python
**Prerequisites:** Phase 6 · 02 (Spectrograms), Phase 6 · 04 (ASR), Phase 6 · 07 (TTS) | **前置知识:** 阶段 6 · 02（频谱图），阶段 6 · 04（ASR），阶段 6 · 07（TTS）
**Time:** ~75 minutes | **预计用时:** ~75 分钟

## El problema es la introducción del problema

Si quieres un asistente de voz que se sienta vivo, la latencia de toma de vueltas de conversación humana es de ~ 230 ms. Cualquier cosa por encima de 500 ms se siente robótica, más de 1500 ms se siente rota. El presupuesto para una conversación completa**hear → understand → respond → speak**el ciclo en 2026 es:

> Usted quiere un asistente de voz "vivo"― Human Dialogue Round Delay de aproximadamente 230 ms(静音到回应)― Más de 500 ms 感觉像机器人; más de 1500 ms 感觉坏掉―2026年完整**听 → 理解 → 回应 → 说**ciclo presupuestario es:

> **【中文解读】**La pregunta planteada en este capítulo es: ¿cómo entender y aplicar correctamente esta tecnología en la ingeniería real? Comprender el contexto de la cuestión ayuda a comprender los puntos clave de decisión del tipo de selección técnica. En los sistemas de IA reales, el tipo de selección técnica errónea suele ser más alto que el costo de error de la realización de detalles.

| Stage | Budget |
|-------|--------|
| Mic → buffer | 20 ms |
| VAD | 10 ms |
| ASR (streaming) | 150 ms |
| LLM (first token) | 100 ms |
| TTS (first chunk) | 100 ms |
| Render → speaker | 20 ms |
| **Total** | **~400 ms** |

| 阶段 | 预算 |
|------|------|
| 麦克风 → 缓冲 | 20 ms |
| VAD | 10 ms |
| ASR（流式） | 150 ms |
| LLM（首 token） | 100 ms |
| TTS（首块） | 100 ms |
| 渲染 → 扬声器 | 20 ms |
| **总计** | **约 400 ms** |

Moshi (Kyutai, 2024) logró 200 ms de doble completo. GPT-4o en tiempo real (2024) relojes ~ 320 ms. Las tuberías cascadas en 2022 se enviaron a 2500 ms. La mejora de 10 veces vino de tres técnicas: (1) streaming en todas partes, (2) tuberías asincronas con resultados parciales, (3) generación interrumpida.

> Moshi(Kyutai,2024) logró 200 ms 全双工──GPT-4o-realtime(2024) aproximadamente 320 ms──2022 años de nivel de la línea de flujo de agua retrasado 2500 ms──10 veces mejorado de tres técnicas:

## El concepto central.

> **【中文解读】**Este capítulo presenta los conceptos y teorías básicos. La comprensión de estos conceptos es el prerrequisito de la realización posterior de la actividad, y también el conocimiento de los puntos de alta frecuencia de la entrevista y la práctica de la ingeniería.


![Streaming audio pipeline with ring buffer, VAD gate, interruption](../assets/real-time.svg)

**Frame / chunk / window.**El audio fluye en tiempo real como bloques de tamaño fijo.

> **帧/块/窗口。**实时音频以固定大小的块流动──常见选择:20 ms(16 kHz 下 320 采样点)──下游一切都必须跟上这个节奏──

**Ring buffer.**Buffer circular de tamaño fijo. El hilo de productor escribe nuevos marcos, el hilo de consumo lee. Previene las asignaciones en el camino caliente. Tamaño ≈ latencia máxima × tasa de muestra; un anillo de 2 segundos de 16 kHz = 32.000 muestras.

> **环形缓冲区。**固定大小的循环缓冲区── producidor线程写入新,消费者线程读取── prevenir la distribución de la memoria en el camino de calor──大小约等于最大延迟 × 采样率;2秒 16 kHz 环形缓冲 = 32,000 采样点──

**VAD (Voice Activity Detection).**Los Gates funcionan en aguas subterráneas cuando nadie está hablando. Silero VAD 4.0 (2024) ejecuta <1 ms por 30 ms de fotogramas en CPU. `webrtcvad`es la alternativa más antigua.

> **VAD（语音活动检测）。**无人说话时阻止下游工作──Silero VAD 4.0(2024) en la CPU por cada 30 ms 运行 <1 ms──`webrtcvad`Es una alternativa más antigua.

**Streaming ASR.**Modelos que emiten transcripciones parciales a medida que llega el audio. Parakeet-CTC-0.6B en modo de transmisión (NeMo, 2024) hace un WER del 25% a una latencia de 320 ms.

> **流式 ASR。**随音频到达而输出部分转录的模型──Parakeet-CTC-0.6B 流式模式──NeMo,2024) en 320 ms 延迟下实现 2-5% WER──Whisper-Streaming──Macháček等,2023) hará Whisper 分块以实现接近流式的约2秒延迟──

**Interruption.**Cuando el usuario habla mientras el asistente habla, debe (a) detectar el barge-in, (b) detener el TTS, (c) descartar la salida restante de LLM. Todo dentro de 100 ms, o el usuario percibe el asistente sordo.

> **打断。**Cuando el asistente en el discurso abre la puerta del usuario, usted debe (a) 检测到抢话, (b) 停止 TTS, (c) 丢弃剩余LLM 输出──全部在100 ms内完成,否则用户感觉助手是聋子──

**WebRTC Opus transport.**20 ms de fotogramas, 48 kHz, bitrate adaptativo 8128 kbps. estándar para navegador y móviles. LiveKit, Daily.co, Pion son las pilas 2026 para la construcción de aplicaciones de voz.

> **WebRTC Opus 传输。**20 ms ,48 kHz, tasa de adaptación automática 8-128 kbps。 navegador y móvil de nivel de calidad。LiveKit、Daily.co、Pion es la tecnología para la construcción de aplicaciones de voz ──

**Jitter buffer.**Los paquetes de red llegan fuera de orden / tarde. El buffer jitter reordena y se suaviza; tropiezos → brechas audibles, demasiado grandes → latencia. 6080 ms típicos.

> **抖动缓冲区。**网络包乱序/迟到到达──动缓冲区重排和平滑;太小 → 可听间隙,太大 → 延迟── típico valor 60-80 ms──

### Gotas comunes

> ### 常见陷

- **Thread contention.**Los modelos pesados GIL + de Python pueden deshacerse del hilo de audio. Utilice una biblioteca de audio de llamada C (dispositivo de sonido, PortAudio) y mantenga a Python fuera del camino caliente.
  **线程竞争。**Python GIL + 重模型会使音频线程饥饿──使用 C 回调音频库(sounddevice、PortAudio), hacer que Python 远离热路径──
- **Sample-rate conversion latency.**El nuevo muestreo dentro de la tubería agrega 520 ms. O sea que se vuelva a muestrar de antemano o se utiliza un nuevo muestreo de latencia cero (PolyPhase, `soxr_hq`¿Qué es lo que se hace?
  **采样率转换延迟。**流水线内部重采样增加 5-20 ms──要么提前重采样,要么使用零延迟重采样器──
- **TTS priming.**Incluso TTS rápido como Kokoro tiene un calentamiento de 100 200 ms a primera solicitud.
  **TTS 预热。**Incluso como Kokoro, TTS rápido en la primera solicitud también tiene 100-200 ms de pre-calentamiento.
- **Echo cancellation.**Sin AEC, la salida TTS vuelve a entrar en el micrófono y activa ASR en la propia voz del bot.
  **回声消除。**没有 AEC, TTS 输出重新进入麦克风并触发 ASR 识别机器人自己的声音──WebRTC AEC3 es un código abierto默认方案──

> **【中文解读】**Este capítulo a través del código de la implementación de algoritmos centrales de cero. Este método "desde cero" puede ayudar a entender el principio detrás del marco, no se encuentra en la caja negra cuando se encuentran problemas.

> **【拓展：语音 AI 的产品化】**La tecnología de voz se enfrenta a un desafío único en la productorización: diferentes voces, ruidos de contexto, remota recogida, muchos hablar, etc.

> **【拓展：多语言语音技术】**Las características de los idiomas de todo el mundo son muy diferentes: el sonido de los idiomas de todo el mundo (como el chino) es alto, el lenguaje de bajo recurso es poco capacitado.

> **【拓展：语音隐私与安全】**语音数据 contiene una gran cantidad de información personal privada ([[音纹]], diálogo contenido) ◦ profundidad falsificación (Deepfake) 语音技术 (语音技术) puede ser utilizada para fraude (音频水印) 音频水印 (音频水印) 音纹水标 (音符标) 声纹反欺诈 (音纹反欺诈) ]] ]] ]] ]] ]] ]] ]] ]] ]] ]] ]] ]] ]] ]] ]] ]] ]] ]] ]] ]] ]] ]] ]] ]] ]] ]] ]] ]] ]] ]] ]] ]] ]] ]] ]] ]] ]] ]] ]] ]] ]] ]] ]] ]] ]] ]] ]] ]] ]] ]] ]] ]] ]] ]] ]] ]] ]] ]] ]] ]] ]] ]] ]] ]] ]] ]] ]] ]] ]] ]] ]] ]] ]] ]] ]] ]] ]] ]] ]] ]] ]] ]] ]] ]] ]] ]] ]] ]] ]] ]] ]] ]] ]] ]] ]] ]] ]]





## Construye y realiza.
```figure
nyquist-aliasing
```

## Construye el mismo

### Paso 1: amortiguador de anillos

```python
import collections

class RingBuffer:
    def __init__(self, capacity):
        self.buf = collections.deque(maxlen=capacity)
    def write(self, frame):
        self.buf.extend(frame)
    def read(self, n):
        return [self.buf.popleft() for _ in range(min(n, len(self.buf)))]
    def level(self):
        return len(self.buf)
```

La capacidad determina la latencia máxima de amortiguación. 32.000 muestras a 16 kHz = 2 segundos.

### Paso 2: Puerta de VAD

```python
def simple_energy_vad(frame, threshold=0.01):
    return sum(x * x for x in frame) / len(frame) > threshold ** 2
```

Reemplazar con Silero VAD en producción:

```python
import torch
vad, _ = torch.hub.load("snakers4/silero-vad", "silero_vad")
is_speech = vad(torch.tensor(frame), 16000).item() > 0.5
```

### Paso 3: transmisión de ASR

```python
# Parakeet-CTC-0.6B streaming via NeMo
from nemo.collections.asr.models import EncDecCTCModelBPE
asr = EncDecCTCModelBPE.from_pretrained("nvidia/parakeet-ctc-0.6b")
# chunk_ms=320 ms, look_ahead_ms=80 ms
for chunk in audio_stream():
    partial_text = asr.transcribe_streaming(chunk)
    print(partial_text, end="\r")
```

### Paso 4: manipulador de interrupciones

```python
class Dialog:
    def __init__(self):
        self.tts_task = None

    def on_user_speech(self, frame):
        if self.tts_task and not self.tts_task.done():
            self.tts_task.cancel()   # barge-in
        # then feed to streaming ASR

    def on_final_user_utterance(self, text):
        self.tts_task = asyncio.create_task(self.reply(text))

    async def reply(self, text):
        async for tts_chunk in llm_then_tts(text):
            speaker.write(tts_chunk)
```

> **【中文解读】**Este capítulo muestra cómo utilizar un marco maduro (como PyTorch、HuggingFace, etc.) para aplicar rápidamente esta tecnología. En los proyectos reales, se realiza con prioridad el uso de un marco experimentado, se pueden reducir errores y mejorar la eficiencia de desarrollo.


Se puede ver en la transmisión de audio sincronizada y cancelable.

> Dependiendo de los diferentes pasos I/O y eliminación de TTS 流式传输──WebRTC's peerconnection.stop() 停止音频轨道是标准方式──




> **【拓展：语音与情感计算】**语音 no sólo transmite información escrita, también lleva una rica cantidad de señales emocionales (en inglés: voice signal) 语调、语速、音高变化) 情感语音识别 (en inglés: speech emotion recognition, SER) 语音 no solo transmite información escrita, sino que también lleva una gran cantidad de señales emocionales (en inglés: voice signal). 语音 tiene una amplia aplicación en el campo de la evaluación de calidad de los clientes, la vigilancia de la salud mental, la educación inteligente, etc.  Los modelos actuales de SOTA se basan en modelos de entrenamiento de las ondas 2vec 2.0 o HuBERT.

## Usalo con el marco de ejecución

La pila de 2026:

| Layer | Pick |
|-------|------|
| Transport | LiveKit (WebRTC) or Pion (Go) |
| VAD | Silero VAD 4.0 |
| Streaming ASR | Parakeet-CTC-0.6B or Whisper-Streaming |
| LLM first-token | Groq, Cerebras, vLLM-streaming |
| Streaming TTS | Kokoro or ElevenLabs Turbo v2.5 |
| Echo cancel | WebRTC AEC3 |
| End-to-end native | OpenAI Realtime API or Moshi |

| 层 | 选择 |
|----|------|
| 传输 | LiveKit（WebRTC）或 Pion（Go） |
| VAD | Silero VAD 4.0 |
| 流式 ASR | Parakeet-CTC-0.6B 或 Whisper-Streaming |
| LLM 首 token | Groq、Cerebras、vLLM-streaming |
| 流式 TTS | Kokoro 或 ElevenLabs Turbo v2.5 |
| 回声消除 | WebRTC AEC3 |
| 端到端原生 | OpenAI Realtime API 或 Moshi |



## Las trampas

> 常见陷

- **Buffering 500 ms to be safe.**El amortiguador es tu piso de latencia.
  **缓冲 500 ms 求安全。**缓冲区*就是*你的延迟下限──缩小它──
- **Not pinning threads.**Recall de audio en un hilo de prioridad inferior a la UI = fallos bajo carga.
  **没有绑定线程。**音频回调 en bajo de la U.I. 优先线程上 = 负载下出现故障──
- **TTS chunks too small.**Los fragmentos de sub-200 ms hacen audibles los artefactos del vocoder.
  **TTS 块太小。**Un bloque de menos de 200 ms es el mejor punto de equilibrio.
- **No jitter buffer.**Las redes reales son nerviosas; sin suavizar se obtienen pops.
  **没有抖动缓冲。**La verdadera red tiene movimiento; no hay nada que se haga.
- **Single-shot error handling.**Las tuberías de audio deben ser a prueba de choque.
  **单次错误处理。**La línea de agua debe resistir el colapso.

> **【中文解读】**Este capítulo se centra en cómo se puede implementar el modelo como producto disponible. Desde el modelo original hasta el sistema de producción, se deben considerar múltiples dimensiones de optimización de rendimiento, tratamiento de errores, control, etc.


## Envíe el producto .

Salvo como`outputs/skill-realtime-designer.md`Diseñar una línea de audio en tiempo real con presupuestos concretos de latencia por etapa.

> 保存为                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           `outputs/skill-realtime-designer.md`◊ diseño de cada etapa tiene un presupuesto específico de retraso real tiempo

## Los ejercicios.

1. **Easy.**- ¿ Qué ?`code/main.py`Simula un amortiguador de anillo + energía VAD; Imprime las latencias de etapa para una corriente falsa de 10 segundos.
   **简单。**运行                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           `code/main.py`◊模拟环形缓冲区 + 能量 VAD;印印假 10 秒流的各阶段延迟──
2. **Medium.**Usando`sounddevice`, construir un paso a través de un bucle que procesa su micrófono en 20 ms de marcos y impresiones estado VAD en cada marco.
   **中等。**Uso `sounddevice`Construir un ciclo directo, en 20 ms procesar el aire y imprimirlo en estado de VAD.
3. **Hard.**Construir una prueba de eco duplex completa con `aiortc`: navegador → WebRTC → Python → WebRTC → navegador. Medir la latencia de vidrio a vidrio con un pulso de 1 kHz.
   **困难。**¿ Qué ?`aiortc`构建全双工回声测试:浏览器 → WebRTC → Python → WebRTC → 浏览器──用 1 kHz 脉冲测量端到端延迟──

> **【中文解读】**En el lenguaje de los términos "Lo que la gente dice" vs "Lo que realmente significa" se distingue entre el lenguaje diario y la definición técnica de significado.


## Términos clave .

| Term | What people say | What it actually means |
|------|-----------------|-----------------------|
| Ring buffer | The circular queue | Fixed-size, lock-free (or SPSC-locked) FIFO for audio frames. |
| VAD | Silence gate | Model or heuristic marking speech vs non-speech. |
| Streaming ASR | Real-time STT | Emits partial text as audio arrives; bounded lookahead. |
| Jitter buffer | Network smoother | Queue reordering out-of-order packets; 60–80 ms typical. |
| AEC | Echo cancellation | Subtracts speaker-to-mic feedback path. |
| Barge-in | User interrupt | System detects user speech mid-TTS; must cancel playback. |
| Full duplex | Simultaneous both ways | User and bot can talk at the same time; Moshi is full duplex. |

| 术语 | 人们常说的 | 实际含义 |
|------|-----------|---------|
| 环形缓冲 | 那个循环队列 | 固定大小、无锁（或 SPSC 锁）的音频帧 FIFO。 |
| VAD | 静音门 | 标记语音 vs 非语音的模型或启发式。 |
| 流式 ASR | 实时 STT | 随音频到达输出部分文本；有限前瞻。 |
| 抖动缓冲 | 网络平滑器 | 重排乱序包的队列；典型 60-80 ms。 |
| AEC | 回声消除 | 减去扬声器到麦克风的反馈路径。 |
| 抢话 | 用户打断 | 系统在 TTS 播放中检测用户语音；必须取消播放。 |
| 全双工 | 双向同时 | 用户和机器人可以同时说话；Moshi 是全双工。 |

> **【中文解读】**延伸阅读 proporciona un alto nivel de recursos para el aprendizaje profundo. Estos artículos y cursos son los referentes clásicos en el campo, adecuados para los lectores que necesitan una comprensión profunda.


## Más Leer más Leer más

- [Macháček et al. (2023). Whisper-Streaming](https://arxiv.org/abs/2307.14743) Chunked casi fluyendo susurro.
  Macháček 等 (2023).
- [Kyutai (2024). Moshi](https://kyutai.org/Moshi.pdf) 200 ms de latencia de doble completo.
  Kyutai (2024). Moshi全双工 200 ms 延迟──
- [LiveKit Agents framework (2024)](https://docs.livekit.io/agents/) Orquestación de agentes de producción de audio.
  LiveKit Agents 框架(2024) 生产级音频智能体编排──
- [Silero VAD repo](https://github.com/snakers4/silero-vad) sub-1 ms VAD, Apache 2.0.
  Silero VAD  almacenes 亚毫秒 VAD, Apache 2.0
- [WebRTC AEC3 paper](https://webrtc.googlesource.com/src/+/main/modules/audio_processing/aec3/) cancelación de eco bajo código abierto.
  WebRTC AEC3 论文 开源回声消除──

> **【中文解读】**延伸阅读 proporciona recursos de alta calidad para el aprendizaje profundo, incluyendo artículos, tutorials y herramientas.

