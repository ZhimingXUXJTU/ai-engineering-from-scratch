# Construir un tubo de ayuda de voz  La Fase 6 Capstone  Construir un proyecto de formación  阶段 6 毕业项目

> Todo desde las lecciones 01-11, unido. Construye un asistente de voz que escuche, razone y hable. En 2026 ese es un problema de ingeniería resuelto, no un problema de investigación  pero los detalles de integración deciden si se lanza.

> **【中文解读】**Colocar todo el contenido de las clases en un conjunto, construir un asistente de voz capaz de escuchar, pensar, hablar. En 2026 es un problema de ingeniería resuelto, no de investigación.

**Type:** Build | **类型:** 构建
**Languages:** Python | **语言:** Python
**Prerequisites:** Phase 6 · 04, 05, 06, 07, 11; Phase 11 · 09 (Function Calling); Phase 14 · 01 (Agent Loop) | **前置知识:** 阶段 6 · 04、05、06、07、11；阶段 11 · 09（函数调用）；阶段 14 · 01（智能体循环）
**Time:** ~120 minutes | **预计用时:** ~120 分钟

## El problema es la introducción del problema

Construir un asistente de extremo a extremo:

> Construir un ayudante de extremo a extremo:

> **【中文解读】**La pregunta planteada en este capítulo es: ¿cómo entender y aplicar correctamente esta tecnología en la ingeniería real? Comprender el contexto de la cuestión ayuda a comprender los puntos clave de decisión del tipo de selección técnica. En los sistemas de IA reales, el tipo de selección técnica errónea suele ser más alto que el costo de error de la realización de detalles.

1. Captura la entrada de micrófono (16 kHz mono).
   捕获麦克风输入(16 kHz 单声道)
2. Detecta el inicio y el final del habla del usuario.
   检测用户语音的开始/结束──
3. Transcribe el streaming.
   流式转录──
4. Pases transcripción a un LLM que puede llamar a herramientas (timer, clima, calendario).
   Se transmitirá el transcripto a la LLM de herramientas de ajuste (tiempo, tiempo, tiempo, calendario).
5. Transmite un texto de LLM a un TTS.
   La enseñanza superior se transmite a TTS.
6. Reproduce el audio al usuario.
   A los usuarios la reproducción de la voz.
7. Se detiene si el usuario interrumpe la respuesta media.
   Si el usuario está en respuesta, entonces se detiene.

Objetivo de latencia: primer byte de audio TTS dentro de los 800 ms del usuario terminando su pronunciación en una CPU portátil. Objetivo de calidad: no faltan palabras, no hay subtítulos alucinados en silencio, no hay filtración de clonación de voz, no hay éxito de inyección rápida.

> 延迟目标: 在笔记本 CPU 上用户说完话后 800 ms 内发出第一 TTS 音频字节──质量目标:不漏词、静音不产生幻觉字幕、无声音克隆泄漏、提示注入不成功──

## El concepto central.

> **【中文解读】**Este capítulo presenta los conceptos y teorías básicos. La comprensión de estos conceptos es el prerrequisito de la realización posterior de la actividad, y también el conocimiento de los puntos de alta frecuencia de la entrevista y la práctica de la ingeniería.


![Voice assistant pipeline: mic → VAD → STT → LLM+tools → TTS → speaker](../assets/voice-assistant.svg)

### Los siete componentes

1. **Audio capture.**Mic → 16 kHz mono → 20 ms trozos. Por lo general `sounddevice`en Python o AudioUnit/ALSA/WASAPI nativo en producción.
   **音频捕获。**麦克风 → 16 kHz 单声道 → 20 ms 块──Python 中通常使用 `sounddevice`, producción ambiental en el mundo de la música
2. **VAD (Lesson 11).**Silero VAD @ umbral 0,5, min habla 250 ms, silencio colgar 500 ms. Las señales "inicio" y "fina".
   **VAD（第 11 课）。**Silero VAD @ 值 0.5, mínimo语音 250 ms,静音持续 500 ms──信号"开始"和"结束"──
3. **Streaming STT (Lesson 4-5).**Whisper-streaming, Parakeet-TDT, o Deepgram Nova-3 (API). Transcripciones parciales + finales.
   **流式 STT（第 4-5 课）。**Se puede escuchar en el video de Whisper-streaming, Parakeet-TDT o Deepgram Nova-3...
4. **LLM with tool calling.**GPT-4o / Claude 3.5 / Gemini 2.5 Flash. esquema JSON para herramientas. Tokens de transmisión.
   **带工具调用的 LLM。**GPT-4o / Claude 3.5 / Gemini 2.5 Flash──工具的 JSON schema──流式代币──
5. **Streaming TTS (Lesson 7).**Kokoro-82M (abriendo más rápido) o Cartesia Sonic (comercial).
   **流式 TTS（第 7 课）。**Kokoro-82M (más reciente de la actualidad) o Cartesia Sonic (más reciente de la actualidad)
6. **Playback.**El altavoz fuera; código opus para redes de bajo ancho de banda.
   **回放。**扬声器输出;低带宽网络用 opus 编码──
7. **Interruption handler.**Si el VAD dispara durante la reproducción de TTS, detenga la reproducción, cancele LLM, reinicie STT.
   **打断处理器。**Si el programa se emite durante el período de VAD, se detiene el programa, se elimina el programa, se reinicia el programa.

### Los tres modos de fracaso que golpearás

> ### Hay tres tipos de fracasos que encontrarás.

1. **First-word clip.**VAD comienza un ritmo demasiado tarde. "Hey" del usuario falta.
   **首词截断。**VAD  iniciación tarde una vez ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞
2. **Mid-response interrupt confusion.**LLM sigue generando después de que el usuario interrumpa; el asistente habla sobre el usuario.
   **回应中打断混乱。**Usuario:                                                                                                                                                                                                                                                              
3. **Silence hallucination.**Los susurros dicen "gracias por ver" en los cuadros silenciosos de calentamiento.
   **静音幻觉。**Susurro en vivo en vivo en vivo en vivo en vivo en vivo en vivo en vivo en vivo en vivo en vivo en vivo en vivo en vivo en vivo en vivo en vivo en vivo en vivo en vivo en vivo en vivo en vivo en vivo en vivo en vivo en vivo en vivo en vivo en vivo en vivo en vivo en vivo en vivo en vivo en vivo en vivo en vivo en vivo en vivo en vivo en vivo en vivo en vivo en vivo en vivo en vivo en vivo en vivo en vivo en vivo en vivo en vivo en vivo en vivo en vivo en vivo en vivo en vivo en vivo en vivo en vivo en vivo en vivo en vivo en vivo en vivo en vivo en vivo en vivo en vivo en vivo en vivo en vivo en vivo en vivo en vivo en vivo en vivo en vivo en vivo en vivo en vivo en vivo en vivo en vivo en vivo en vivo en vivo en vivo en vivo en vivo en vivo en vivo en vivo en vivo en vivo en vivo en vivo en vivo en vivo en vivo en vivo en vivo en vivo en vivo en vivo en vivo en vivo en vivo en vivo en vivo en vivo en vivo en vivo en vivo en vivo en vivo en vivo en vivo en vivo en vivo en vivo en vivo en vivo en vivo en vivo en vivo en vivo en vivo en vivo en vivo en vivo en vivo en vivo en vivo en vivo en vivo en vivo en vivo en vivo en vivo en vivo en vivo en vivo en vivo en vivo en vivo en vivo en vivo en vivo en vivo en vivo en vivo en vivo en vivo en vivo en vivo en vivo en vivo en vivo en vivo en vivo en vivo en vivo en vivo en vivo en vivo en vivo en vivo en vivo en vivo en vivo en vivo en vivo en vivo en vivo en vivo en vivo en vivo en vivo en vivo en vivo en vivo en vivo en vivo en vivo en vivo en vivo en vivo en vivo en vivo en vivo en vivo en vivo en vivo en vivo en vivo en vivo en vivo en vivo en vivo en vivo en vivo en vivo en vivo en vivo en vivo en vivo en vivo en vivo en vivo en vivo en vivo en vivo en vivo en vivo en vivo en vivo en vivo en vivo en vivo en vivo en vivo en vivo en vivo en vivo en vivo en vivo en vivo en vivo en vivo en vivo en vivo en vivo en vivo en vivo en vivo en vivo en vivo en vivo en vivo en vivo en vivo en vivo en vivo en vivo en vivo en vivo en vivo en vivo en vivo en vivo en

### 2026 Estadios de referencia de producción

| Stack | Latency | License | Notes |
|-------|---------|---------|-------|
| LiveKit + Deepgram + GPT-4o + Cartesia | 350-500 ms | commercial API | Industry default 2026 |
| Pipecat + Whisper-streaming + GPT-4o + Kokoro | 500-800 ms | mostly open | DIY-friendly |
| Moshi (full-duplex) | 200-300 ms | CC-BY 4.0 | Single-model; different architecture, lesson 15 |
| Vapi / Retell (managed) | 300-500 ms | commercial | Fastest to launch; limited customization |
| Whisper.cpp + llama.cpp + Kokoro-ONNX | offline | open | Privacy / edge |

| 技术栈 | 延迟 | 许可 | 备注 |
|--------|------|------|------|
| LiveKit + Deepgram + GPT-4o + Cartesia | 350-500 ms | 商业 API | 2026 行业默认 |
| Pipecat + Whisper-streaming + GPT-4o + Kokoro | 500-800 ms | 多数开源 | DIY 友好 |
| Moshi（全双工） | 200-300 ms | CC-BY 4.0 | 单模型；不同架构，第 15 课 |
| Vapi / Retell（托管） | 300-500 ms | 商业 | 最快上线；定制有限 |
| Whisper.cpp + llama.cpp + Kokoro-ONNX | 离线 | 开源 | 隐私/边缘 |

> **【中文解读】**Este capítulo a través del código de la implementación de algoritmos centrales de cero. Este método "desde cero" puede ayudar a entender el principio detrás del marco, no se encuentra en la caja negra cuando se encuentran problemas.

> **【拓展：语音 AI 的产品化】**La tecnología de voz se enfrenta a un desafío único en la productorización: diferentes voces, ruidos de contexto, remota recogida, muchos hablar, etc.

> **【拓展：多语言语音技术】**Las características de los idiomas de todo el mundo son muy diferentes: el sonido de los idiomas de todo el mundo (como el chino) es alto, el lenguaje de bajo recurso es poco capacitado.

> **【拓展：语音隐私与安全】**语音数据 contiene una gran cantidad de información personal privada ([[音纹]], diálogo contenido) ◦ profundidad falsificación (Deepfake) 语音技术 (语音技术) puede ser utilizada para fraude (音频水印) 音频水印 (音频水印) 音纹水标 (音符标) 声纹反欺诈 (音纹反欺诈) ]] ]] ]] ]] ]] ]] ]] ]] ]] ]] ]] ]] ]] ]] ]] ]] ]] ]] ]] ]] ]] ]] ]] ]] ]] ]] ]] ]] ]] ]] ]] ]] ]] ]] ]] ]] ]] ]] ]] ]] ]] ]] ]] ]] ]] ]] ]] ]] ]] ]] ]] ]] ]] ]] ]] ]] ]] ]] ]] ]] ]] ]] ]] ]] ]] ]] ]] ]] ]] ]] ]] ]] ]] ]] ]] ]] ]] ]] ]] ]] ]] ]] ]] ]] ]] ]] ]] ]] ]] ]] ]] ]] ]] ]] ]] ]] ]]





## Construye y realiza.
```figure
v4-voice-latency
```

## Construye el mismo

### Paso 1: captura de micrófono con fragmentación (pseudocodo)

```python
import sounddevice as sd

def mic_stream(chunk_ms=20, sr=16000):
    q = queue.Queue()
    def cb(indata, frames, time, status):
        q.put(indata.copy().flatten())
    with sd.InputStream(channels=1, samplerate=sr, blocksize=int(sr * chunk_ms/1000), callback=cb):
        while True:
            yield q.get()
```

### Paso 2: Captura de la vuelta con puerta VAD

```python
def capture_turn(stream, vad, pre_roll_ms=300, silence_ms=500):
    buf, pre, triggered = [], collections.deque(maxlen=pre_roll_ms // 20), False
    silent = 0
    for chunk in stream:
        pre.append(chunk)
        if vad(chunk):
            if not triggered:
                buf = list(pre)
                triggered = True
            buf.append(chunk)
            silent = 0
        elif triggered:
            silent += 20
            buf.append(chunk)
            if silent >= silence_ms:
                return b"".join(buf)
```

### Paso 3: transmisión de STT → LLM → TTS

```python
async def turn(audio_bytes):
    transcript = await stt.transcribe(audio_bytes)
    async for token in llm.stream(transcript):
        async for audio in tts.stream(token):
            await speaker.play(audio)
```

### Paso 4: herramienta de llamadas dentro del bucle de LLM

```python
tools = [
    {"name": "get_weather", "parameters": {"location": "string"}},
    {"name": "set_timer", "parameters": {"seconds": "int"}},
]

async for chunk in llm.stream(user_text, tools=tools):
    if chunk.type == "tool_call":
        result = dispatch(chunk.name, chunk.args)
        continue_streaming(result)
    if chunk.type == "text":
        await tts.stream(chunk.text)
```

### Paso 5: Manejo de interrupciones

> **【中文解读】**Este capítulo muestra cómo utilizar un marco maduro (como PyTorch、HuggingFace, etc.) para aplicar rápidamente esta tecnología. En los proyectos reales, se realiza con prioridad el uso de un marco experimentado, se pueden reducir errores y mejorar la eficiencia de desarrollo.


```python
tts_task = asyncio.create_task(tts_loop())
while True:
    chunk = await mic.get()
    if vad(chunk):
        tts_task.cancel()
        await speaker.stop()
        await new_turn()
        break
```




> **【拓展：语音与情感计算】**语音 no sólo transmite información escrita, también lleva una rica cantidad de señales emocionales (en inglés: voice signal) 语调、语速、音高变化) 情感语音识别 (en inglés: speech emotion recognition, SER) 语音 no solo transmite información escrita, sino que también lleva una gran cantidad de señales emocionales (en inglés: voice signal). 语音 tiene una amplia aplicación en el campo de la evaluación de calidad de los clientes, la vigilancia de la salud mental, la educación inteligente, etc.  Los modelos actuales de SOTA se basan en modelos de entrenamiento de las ondas 2vec 2.0 o HuBERT.

## Usalo con el marco de ejecución

¿ Qué ?`code/main.py`para una simulación ejecutable que conecta los siete componentes con modelos de estubes, para que pueda ver la forma de la tubería incluso sin hardware.

> 参见 `code/main.py`获取可运行的模拟,将七组件用模块连接,无需硬件即可见流水线形状──实际实现时,将模块替换为:

- `silero-vad`(El artículo`pip install silero-vad`) / VAD 模块
- `deepgram-sdk`o `openai-whisper`/ 流式 STT
- `openai`(El artículo`gpt-4o`) o `anthropic`/ LLM + 工具调用
- `kokoro`o `cartesia`/ 流式 TTS
- `sounddevice`para I/O / 音频输入输出



## Las trampas

> 常见陷

- **Logging PII forever.**El audio de giro completo es información personal en la mayoría de jurisdicciones.
  **永久记录 PII。**完整轮次音频在多数司法管辖区属于PII──30 天保留,静态加密──
- **No barge-in.**Los usuarios interrumperán, su asistente debe dejar de hablar.
  **没有抢话。**Su asistente debe dejar de hablar.
- **TTS that blocks.**TTS sincrónico bloquea el bucle de eventos.
  **阻塞式 TTS。**Concomitente TTS  bloqueo de eventos ciclo ∞ uso de diferentes pasos o líneas independientes ∞
- **No tool-call error handling.**Las herramientas fallan. LLM debe recuperar el error + volver a intentar una vez, luego degradar con gracia.
  **没有工具调用错误处理。**工具会失败──LLM 必须收到错误 + 重试一次,然后优雅降级──
- **Overzealous hallucination filters.**Superfiltrado y el asistente repite "No puedo evitarlo" subfiltrado y dice cualquier cosa calibra en un set aguantado.
  **过度激进的幻觉过滤。**过度过助手会重复"Mi ayuda no ha llegado"―过不足则什么都说―在留出集上校准―
- **No wake-word option.**Siempre escuchar es una responsabilidad de privacidad. Añadir una puerta de advertencia (Porcupine o openWakeWord).
  **没有唤醒词选项。**持续监听是隐私负担──添加唤醒词门控(Porcupine o openWakeWord)──

> **【中文解读】**Este capítulo se centra en cómo se puede implementar el modelo como producto disponible. Desde el modelo original hasta el sistema de producción, se deben considerar múltiples dimensiones de optimización de rendimiento, tratamiento de errores, control, etc.


## Envíe el producto .

Salvo como`outputs/skill-voice-assistant-architect.md`. Dadas las limitaciones presupuestarias + de escala + de lenguaje + de cumplimiento, elaborar una especificación completa de la pila.

> 保存为                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           `outputs/skill-voice-assistant-architect.md` Presta un presupuesto + 规模 + 语言 + 合规约束,产出完整技术规格──

## Los ejercicios.

1. **Easy.**- ¿ Qué ?`code/main.py`Simula una vuelta completa de extremo a extremo con módulos de estub y grabadas por latencia de etapa.
   **简单。**运行                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           `code/main.py` 模块模拟一个完整轮次端到端并印各阶段延迟
2. **Medium.**Reemplaza el estubito de STT con un modelo real de Whisper en una grabación previa `.wav`- Medir el WER y la latencia de extremo a extremo.
   **中等。**En el pre-registro`.wav`上用真实 Whisper 模型替换STT 模块──测量 WER 和端到端延迟──
3. **Hard.**Añadir la llamada de herramientas: implementar `get_weather`(cualquier API) y `set_timer`. Envía el LLM a través de las herramientas y comprueba que cuando el usuario dice "establecer un temporizador de 5 minutos" se activa la función correcta y la respuesta oral lo confirma.
   **困难。**添加工具调用: ejecutar `get_weather`(cualquier API) y `set_timer` A través de la herramienta de LLM, la verificación cuando el usuario dice "establecer un fijación de tiempo de 5 minutos" cuando se utiliza la función correcta 

> **【中文解读】**En el lenguaje de los términos "Lo que la gente dice" vs "Lo que realmente significa" se distingue entre el lenguaje diario y la definición técnica de significado.


## Términos clave .

| Term | What people say | What it actually means |
|------|-----------------|-----------------------|
| Turn | A user + assistant round-trip | One VAD-bounded user speech + one LLM-TTS response. |
| Barge-in | Interruption | User speaks while assistant talks; assistant stops. |
| Wake word | "Hey assistant" | Short keyword detector; Porcupine, Snowboy, openWakeWord. |
| End-pointing | Turn ending | VAD + min-silence decision that user has finished. |
| Pre-roll | Pre-speech buffer | Keep 200-400 ms of audio before VAD fires to avoid first-word clip. |
| Tool call | Function invocation | LLM emits JSON; runtime dispatches; result feeds back in-loop. |

| 术语 | 人们常说的 | 实际含义 |
|------|-----------|---------|
| 轮次 | 用户+助手一个来回 | 一次 VAD 界定的用户语音 + 一次 LLM-TTS 回应。 |
| 抢话 | 打断 | 助手说话时用户开口；助手停止。 |
| 唤醒词 | "嘿助手" | 短关键词检测器；Porcupine、Snowboy、openWakeWord。 |
| 端点检测 | 轮次结束 | VAD + 最小静音决策用户已说完。 |
| 预滚 | 语音前缓冲 | 在 VAD 触发前保留 200-400 ms 音频以避免首词截断。 |
| 工具调用 | 函数调用 | LLM 输出 JSON；运行时分发；结果在循环中反馈。 |

> **【中文解读】**延伸阅读 proporciona un alto nivel de recursos para el aprendizaje profundo. Estos artículos y cursos son los referentes clásicos en el campo, adecuados para los lectores que necesitan una comprensión profunda.


## Más Leer más Leer más

- [LiveKit — voice agent quickstart](https://docs.livekit.io/agents/) Referencia de grado de producción.
  LiveKit语音智能体快速入门生产级参考──
- [Pipecat — voice agent examples](https://github.com/pipecat-ai/pipecat) Marco de trabajo personal.
  Pipecat语音智能体示例DIY 友好框架──
- [OpenAI Realtime API](https://platform.openai.com/docs/guides/realtime) el camino nativo de voz gestionado.
  OpenAI API en tiempo real 托管的语音原生路径──
- [Kyutai Moshi](https://github.com/kyutai-labs/moshi) Referencia de doble completo (lección 15).
  Kyutai Moshi 全双工参考(第 15 课) 』
- [Porcupine wake-word](https://picovoice.ai/products/porcupine/) la puerta de la palabra de la alarma.
  Porcupine 唤醒词唤醒词门控──
- [Anthropic — tool use guide](https://docs.anthropic.com/en/docs/build-with-claude/tool-use) Llamamiento de funciones de LLM.
  Antropic工具使用指南LLM 函数调用──

> **【中文解读】**延伸阅读 proporciona recursos de alta calidad para el aprendizaje profundo, incluyendo artículos, tutorials y herramientas.

