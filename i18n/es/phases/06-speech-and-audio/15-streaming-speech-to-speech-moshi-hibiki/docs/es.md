# Transmitir en directo el discurso a la palabra  Moshi, Hibiki y diálogo doble completo 流式语音到语音  Moshi、Hibiki y全双工对话

> 2024-2026 redefinió la IA de voz. Moshi envía un solo modelo que escucha y habla simultáneamente a 200 ms de latencia. Hibiki hace la traducción de voz a voz pieza por pieza. Ambos abandonan la tubería ASR → LLM → TTS para una arquitectura unificada de doble completo sobre tokens de codec Mimi. Este es el nuevo diseño de referencia.

> **【中文解读】**2024-2026 años redefinió el lenguaje AI。Moshi usó un solo modelo en 200ms 延迟内同时听和说。Hibiki 逐块进行语音到语音翻译。 ambos abandonaron ASR→LLM→TTS 流水线, adoptando una estructura unificada de dos componentes basada en los tokens Mimi 编解码器。 este es un nuevo diseño de referencia。

> **【拓展：全双工语音 AI】**傳統语音助手是"半双工" (en español: "mi-du-yu"),Moshi 实现了"全双工" (en español: "mi-du-yu"),就像人类自然对话 (en español: "mi-du-yu"), es la dirección de la AI de 2026 en el lenguaje.

**Type:** Learn | **类型:** 学习
**Languages:** Python | **语言:** Python
**Prerequisites:** Phase 6 · 13 (Neural Audio Codecs), Phase 6 · 11 (Real-Time Audio), Phase 7 · 05 (Full Transformer) | **前置知识:** 阶段 6 · 13（神经音频编解码器），阶段 6 · 11（实时音频），阶段 7 · 05（完整 Transformer）
**Time:** ~75 minutes | **预计用时:** ~75 分钟

## El problema es la introducción del problema

Cada agente de voz construido a partir de las lecciones 11 + 12 tiene un nivel de latencia fundamental de alrededor de 300-500 ms: incendios VAD, procesos STT, razones LLM, TTS genera. Cada etapa tiene su propia latencia mínima. Puedes sintonizar y paralelalizar, pero la forma de la tubería te limita.

> 基于第11和12 课程构建的每个语音助手都有一个约300-500 ms的基础延迟下限:VAD 触发、STT 处理、LLM 推理、TTS 生成──每个阶段都有自己的最小延迟──你可以调优和并行化,但流水线架构本身限制你──

> **【中文解读】**La pregunta planteada en este capítulo es: ¿cómo entender y aplicar correctamente esta tecnología en la ingeniería real? Comprender el contexto de la cuestión ayuda a comprender los puntos clave de decisión del tipo de selección técnica. En los sistemas de IA reales, el tipo de selección técnica errónea suele ser más alto que el costo de error de la realización de detalles.


Moshi (Kyutai, 2024-2026) hace una pregunta diferente: ¿qué pasa si no hay un conducto? ¿Qué pasa si un modelo toma audio y emite audio directamente, continuamente, con texto como un "monólogo interno" intermedio en lugar de una etapa requerida?

> Moshi ((Kyutai,2024-2026) planteó un problema diferente: ¿qué pasaría si no hubiera flujo de agua? ¿qué pasaría si un modelo directamente 持续地接收音频输入并输出音频,文本只是中间的内心独白而不是必要阶段?

La respuesta es:**full-duplex speech-to-speech**La latencia teórica 160 ms (80 ms Mimi frame + 80 ms retraso acústico) La latencia práctica 200 ms en una sola GPU L4. Eso es la mitad de lo que un mejor agente de voz en tubos de su clase logra.

> La respuesta es:**全双工语音到语音**△ teoría延迟 160 ms(80 ms Mimi  + 80 ms 声学延迟) ・・・ 在单张 L4 GPU 上实际延迟 200 ms──这是最好的流水线语音助手延迟的一半──

## El concepto central.

> **【中文解读】**Este capítulo presenta los conceptos y teorías básicos. La comprensión de estos conceptos es el prerrequisito de la realización posterior de la actividad, y también el conocimiento de los puntos de alta frecuencia de la entrevista y la práctica de la ingeniería.


![Moshi architecture: two parallel Mimi streams + inner-monologue text](../assets/moshi-hibiki.svg)

### La arquitectura de Moshi

> Moshi 架构

**Inputs.**Dos flujos de códec Mimi, ambos a 12,5 Hz × 8 libros de códigos:

> **输入。**两个 Mimi 编解码器流, media de 12,5 Hz × 8 个码本:

- Flujo 1: audio de usuario (Mimi codificado, llegando constantemente)
  En inglés, el nombre de usuario es "Mimi" (en inglés, "Mimi"), y el nombre de usuario es "Mimi" (en inglés, "Mimi"), y el nombre de usuario es "Mimi" (en inglés, "Mimi").
- Stream 2: audio propio de Moshi (generado por Moshi)
  El nombre de la persona que ha sido elegida para ser el primer ministro de la República de China.

**The transformer.**Un transformador temporal de parámetro 7B procesa las dos corrientes y un flujo de texto "monólogo interno".

> **Transformer。**Un transformer de tiempo de 70 mil millones de parámetros, que procesa dos flujos y un flujo de texto "in-heart-on-the-art" en cada 80 ms, dice:

1. Consume las fichas Mimi de usuario más recientes (8 libros de código).
   En el caso de los usuarios de la plataforma, el usuario de la plataforma tiene que utilizar el token Mimi.
2. Consume los tokens Moshi Mimi más recientes (8 libros de código, según se ha producido).
   En el caso de los monjes de la ciudad de Moshi, el nombre de la persona que se ha convertido en el nombre de la persona que se ha convertido en el nombre de la persona que se ha convertido en el nombre de la persona que se ha convertido en el nombre de la persona que se ha convertido en el nombre de la persona que se ha convertido en el nombre de la persona que se ha convertido en el nombre de la persona que se ha convertido en el nombre de la persona que se ha convertido en el nombre de la persona que se ha convertido en el nombre de la persona que se ha convertido en el nombre de la persona que se ha convertido en el nombre de la persona que se ha convertido en el nombre de la persona.
3. Genera el siguiente símbolo de texto Moshi (monólogo interno).
   En el texto original, el texto se traduce en "Moshí" (Moshí).
4. Generar los siguientes tokens de Moshi Mimi (8 libros de código a través de un pequeño Transformador de Profundidad).
   En el caso de los monedas de la India, el número de monedas de la India es de 1.

Los tres flujos  audio del usuario, audio de Moshi, texto de Moshi  funcionan en paralelo. Moshi puede escuchar al usuario mientras habla; puede interrumpirse cuando el usuario interrumpe; puede retrocanicular ("mhm") sin romper su pronunciación principal.

> Tres流 usuario音频、Moshi 音频、Moshi 文本并行运行──Moshi puede escuchar al usuario mientras habla; puede interrumpirse cuando el usuario rompe; puede realizarse en caso de no destruir la palabra principal.

**The depth transformer.**En un marco, los 8 códigos no se predicen en paralelo  tienen dependencias entre códigos. Un pequeño "transformador de profundidad" de 2 capas los predice secuencialmente dentro de 80 ms. Esta es la factorization estándar para los LMs de códigos AR (también utilizado por VALL-E, VibeVoice).

> **深度 Transformer。**En un 内, 8 códigos no se componen de predicciones de  entre ellos existe un  间依赖. En un 内, un pequeño "transformador de profundidad" de 2 niveles en 80 ms, los predicta en orden.

### Por qué ayuda el texto del monólogo interno

Sin texto explícito, el modelo tiene que modelar implícitamente el lenguaje en su flujo acústico. La visión de Moshi: forzarlo a emitir tokens de texto junto con el audio. El flujo de texto es esencialmente la transcripción de lo que Moshi está diciendo. Esto mejora la coherencia semántica, hace que sea más fácil intercambiar una cabeza de modelo de lenguaje y le da transcripciones de forma gratuita.

> Por qué el texto único en el interior ayuda: no hay texto claro, el modelo debe estar en el flujo de voz en forma oculta de la construcción de lenguaje.

### Hibiki: traducción de voz a voz en streaming

La misma arquitectura, entrenada en pares de traducciones. Audio de origen en, audio de idioma objetivo fuera, continuamente. Hibiki-Zero (feb 2026) elimina la necesidad de datos de entrenamiento alineados a nivel de palabras  utiliza datos de nivel de oración + aprendizaje de refuerzo GRPO para la optimización de latencia.

> Hibiki:流式语音到语音翻译──相同架构,使用翻译对训练──源语言音频输入,目标语言音频输出,持续进行──Hibiki-Zero(2026年 2月) eliminó la necesidad de datos de entrenamiento en términos de palabras  usando datos de los niveles de frase + GRPO 强化学习进行延迟优化──

Cuatro pares de idiomas soportados inicialmente; pueden adaptarse a un nuevo idioma con ≈1000 horas.

> Inicialmente soportan cuatro idiomas; se puede usar alrededor de 1000 horas de datos para adaptarse a nuevos idiomas.

### La pila más amplia de Kyutai (2026)

> Más amplio de Kyutai 技术(2026 años)

- **Moshi** Diálogo duplex completo (francés primero, inglés bien apoyado)
  En español: "Moshi" (en francés: Moshi)
- **Hibiki / Hibiki-Zero** Traducción simultánea del habla
  中文翻译:Hibiki / Hibiki-Zero  同步语音翻译
- **Kyutai STT** RAS de transmisión (500 ms o 2,5 segundos de vista hacia adelante)
  中文翻译:Kyutai STT  流式语音识别(500 ms o 2,5 s 前视)
- **Kyutai Pocket TTS** TTS de 100M-param se ejecuta en CPU (Jan 2026)
  China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China China
- **Unmute** un conjunto completo de sistemas que combinan estos en servidores públicos
  Unmute                                                                                                                                                                                                                                                              

Despliegue en una GPU L40S: 64 sesiones simultáneas en 3x tiempo real.

> En la GPU L40S, la potencia de 64 bits, 3 veces la velocidad real.

### El C.S.M. de sésamo  el primo

Sesame CSM (2025) utiliza una idea similar  una columna vertebral Llama-3 con una cabeza de códec Mimi. Pero CSM es unidireccional (tomando contexto + texto, produce voz) en lugar de doble. Es el mejor TTS "presencia de voz" en el mercado; no es del todo lo mismo que la capacidad de doble completo de Moshi.

> Sesame CSM(2025) utilizó ideas similaresLlama-3 骨干网络 + Mimi 编解码器头── pero CSM es un solo orientado a la recepción de los textos + textos, la generación de los lenguajes), y no a la producción de los lenguajes.

### Números de rendimiento 2026

| Model | Latency | Use case | License |
|-------|---------|----------|---------|
| Moshi | 200 ms (L4) | full-duplex English / French dialogue / 全双工英/法对话 | CC-BY 4.0 |
| Hibiki | 12.5 Hz framerate | French ↔ English streaming translation / 法↔英流式翻译 | CC-BY 4.0 |
| Hibiki-Zero | same | 5 language-pairs, no aligned data / 5 语言对，无需对齐数据 | CC-BY 4.0 |
| Sesame CSM-1B | 200 ms TTFA | context-conditioned TTS / 上下文条件 TTS | Apache-2.0 |
| GPT-4o Realtime | ~300 ms | closed, OpenAI API / 闭源，OpenAI API | commercial |
| Gemini 2.5 Live | ~350 ms | closed, Google API / 闭源，Google API | commercial |

> **【中文解读】**Este capítulo a través del código de la implementación de algoritmos centrales de cero. Este método "desde cero" puede ayudar a entender el principio detrás del marco, no se encuentra en la caja negra cuando se encuentran problemas.

> **【拓展：语音 AI 的产品化】**La tecnología de voz se enfrenta a un desafío único en la productorización: diferentes voces, ruidos de contexto, remota recogida, muchos hablar, etc.

> **【拓展：多语言语音技术】**Las características de los idiomas de todo el mundo son muy diferentes: el sonido de los idiomas de todo el mundo (como el chino) es alto, el lenguaje de bajo recurso es poco capacitado.




## Construye y realiza.
```figure
sp-fullduplex
```

## Construye el mismo

### Paso 1: la interfaz

> Paso 1: Enlace

Moshi expone un servidor WebSocket que toma 80 ms de audio codificado por Mimi y devuelve 80 ms de audio codificado por Mimi.

> Moshi expone un WebSocket  servidor, recibe 80 ms de Mimi 编码音频块并返回 80 ms de Mimi 编码音频块──双向,持续进行──

```python
import asyncio
import websockets
from moshi.client_utils import encode_audio_mimi, decode_audio_mimi

async def moshi_chat():
    async with websockets.connect("ws://localhost:8998/api/chat") as ws:
        mic_task = asyncio.create_task(stream_mic_to(ws))
        spk_task = asyncio.create_task(stream_from_to_speaker(ws))
        await asyncio.gather(mic_task, spk_task)
```

### Paso 2: el bucle de doble completo

> Paso 2: ciclo completo

```python
async def stream_mic_to(ws):
    async for chunk_80ms in mic_stream_at_12_5_hz():
        mimi_tokens = encode_audio_mimi(chunk_80ms)
        await ws.send(serialize(mimi_tokens))

async def stream_from_to_speaker(ws):
    async for msg in ws:
        mimi_tokens, text_token = deserialize(msg)
        audio = decode_audio_mimi(mimi_tokens)
        await play(audio)
```

Ambas direcciones se ejecutan simultáneamente. Python asyncio o futuros de Rust son el transporte estándar.

> 两个方向同时运行──Python asyncio o Rust futuros es el método estándar de transmisión──

### Paso 3: el objetivo de la formación (conceptual)

> 步骤 3: entrenamiento objetivos

Por cada fotograma de 80 ms `t`¿Qué es esto ?

> 对于每80 ms 的 `t`¿Qué es esto ?

- Entrada: `user_mimi[0..t]`¿ Qué ?`moshi_mimi[0..t-1]`¿ Qué ?`moshi_text[0..t-1]`
  En inglés:`user_mimi[0..t]`¿Qué es esto?`moshi_mimi[0..t-1]`¿Qué es esto?`moshi_text[0..t-1]`
- Previsión: `moshi_text[t]`, entonces`moshi_mimi[t, codebook_0..7]`
  El nombre de la ciudad de Nueva York es el de la ciudad de Nueva York.`moshi_text[t]`, y luego es`moshi_mimi[t, codebook_0..7]`

El texto se predice antes del audio (monólogo interno); el audio se predice secuencial en el libro de códigos dentro del transformador de profundidad.

> 文本在音频之前预测(内心独白);音频在深度 Transformer 内按码本顺序预测。

### Paso 4: donde el Moshi gana y donde no

> Paso 4: Las ventajas y las deficiencias de Moshi

Moshi gana:

> Los beneficios de Moshi:

- Sub-250 ms de extremo a extremo en hardware barato.
  En el extremo inferior de 250 ms.
- Canales de retroceso naturales y interrupciones.
  Traducción:El contrario de la naturaleza y el poder de romper.
- No hay código de pegamento de tubería.
  Sin necesidad de flujo de agua.

Moshi no gana:

> Las deficiencias de Moshi:

- La llamada de herramientas (no está capacitada para ello; necesita un camino separado de LLM).
  La formación de la LLM en el campo de la educación superior se ha desarrollado en el campo de la educación superior.
- El razonamiento largo (Moshi es un modelo de diálogo 8B, no Claude/GPT-4).
  El modelo de diálogo de Moshi es de unos 80 mil millones de dólares, no Claude/GPT-4)
- Precisión factual en temas de nicho.
  La verdad es que el tema es un tema de interés.
- La mayoría de los casos de uso de las empresas de producción (todavía se utilizan tuberías en 2026).
  La mayoría de las empresas de producción en el año 2026 siguen utilizando el flujo de agua.

> **【中文解读】**Este capítulo muestra cómo utilizar un marco maduro (como PyTorch、HuggingFace, etc.) para aplicar rápidamente esta tecnología. En los proyectos reales, se realiza con prioridad el uso de un marco experimentado, se pueden reducir errores y mejorar la eficiencia de desarrollo.





> **【拓展：语音与情感计算】**语音 no sólo transmite información escrita, también lleva una rica cantidad de señales emocionales (en inglés: voice signal) 语调、语速、音高变化) 情感语音识别 (en inglés: speech emotion recognition, SER) 语音 no solo transmite información escrita, sino que también lleva una gran cantidad de señales emocionales (en inglés: voice signal). 语音 tiene una amplia aplicación en el campo de la evaluación de calidad de los clientes, la vigilancia de la salud mental, la educación inteligente, etc.  Los modelos actuales de SOTA se basan en modelos de entrenamiento de las ondas 2vec 2.0 o HuBERT.

## Usalo con el marco de ejecución

| Situation | Pick |
|-----------|------|
| Lowest-latency voice companion / 最低延迟语音伴侣 | Moshi |
| Live translation call / 实时翻译通话 | Hibiki |
| Voice demo / research / 语音演示/研究 | Moshi, CSM |
| Enterprise agent with tools / 企业级带工具的 agent | Pipeline（第 12 课），不是 Moshi |
| Custom-voice TTS in context / 上下文中的自定义音色 TTS | Sesame CSM |
| Speech-to-speech, any languages / 任意语言的语音到语音 | GPT-4o Realtime 或 Gemini 2.5 Live（商业） |



## Las trampas

> 常见陷

- **Limited tool calling.**Moshi es un modelo de diálogo, no un marco de agentes.
  En inglés:**有限的工具调用。**Moshi es un modelo de diálogo, no un agente 框架.
- **Specific-voice conditioning.**Moshi usa un solo personaje entrenado; la clonación es una carrera de entrenamiento separada.
  En inglés:**特定语音调节。**Moshi utiliza un solo entrenamiento personaje; Klon necesita un proceso de entrenamiento individual.
- **Language coverage.**El francés + inglés es excelente; otros son limitados. Hibiki-Zero ayuda, pero todavía necesitas datos de formación.
  En inglés:**语言覆盖。**漢語 + 英语表现优秀;其他语言有限──Hibiki-Zero tiene ayuda, pero todavía necesita entrenamiento datos──
- **Resource cost.**Una sesión completa de Moshi tiene un espacio de GPU; no un patrón de implementación compartido barato.
  En inglés:**资源成本。**Un completo programa de Moshi ocupa una GPU; no es un modo de distribución de alquiler barato.

> **【中文解读】**Este capítulo se centra en cómo se puede implementar el modelo como producto disponible. Desde el modelo original hasta el sistema de producción, se deben considerar múltiples dimensiones de optimización de rendimiento, tratamiento de errores, control, etc.


## Envíe el producto .

Salvo como`outputs/skill-duplex-pipeline.md`Elige pipeline vs. arquitectura de doble completo para una carga de trabajo de agente de voz, con razón.

> 保存为                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           `outputs/skill-duplex-pipeline.md`◊ para un asistente de voz de trabajo carga de agua o de la estructura de la estructura,并说明理由──

## Los ejercicios.

1. **Easy.**- ¿ Qué ?`code/main.py`Simula simbólicamente la arquitectura de dos corrientes + monólogo interno.
   En inglés:**简单。**运行                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           `code/main.py` It's a symbol mode模拟双流 + 内心独白架构
2. **Medium.**Trae a Moshi de HuggingFace, ejecuta el servidor, prueba una conversación, mide la latencia del reloj de la pared desde el final del discurso del usuario hasta el inicio de la respuesta de Moshi.
   En inglés:**中等。**Desde HuggingFace 拉取 Moshi,运行服务器,测试一段对话──测量 desde el usuario语音结束到 Moshi 回复开始的实际延迟──
3. **Hard.**Toma tu agente de tubería de la Lección 12 y compara la latencia P50 vs Moshi en 20 declaraciones de prueba coincidentes.
   En inglés:**困难。**Usando el 12o curso de Asistente de Flujo de Agua y Moshi en 20 条匹配测试语句上比较 P50 延迟――escribir un informe que explica cómo flujo de Agua en la estructura es mejor―

> **【中文解读】**En el lenguaje de los términos "Lo que la gente dice" vs "Lo que realmente significa" se distingue entre el lenguaje diario y la definición técnica de significado.


## Términos clave .

| Term | What people say | What it actually means |
|------|-----------------|-----------------------|
| Full-duplex | Hear-and-speak at once | Two audio streams active simultaneously on the same model. / 同一模型同时维护两条音频流 |
| Inner monologue | Model's text stream | Moshi emits text tokens alongside its audio output. / Moshi 在音频输出同时输出文本 token |
| Depth transformer | Inter-codebook predictor | Small transformer that predicts 8 codebooks within one 80 ms frame. / 在一个 80 ms 帧内预测 8 个码本的小型 Transformer |
| Mimi | Kyutai's codec | 12.5 Hz × 8 codebooks; semantic+acoustic; powers Moshi. / 12.5 Hz × 8 码本；语义+声学；驱动 Moshi |
| Streaming S2S | Audio → audio live | Chunk-by-chunk translation/dialogue, no pipeline stages. / 逐块翻译/对话，无流水线阶段 |
| Back-channeling | "Mhm" reactions | Moshi can emit small acknowledgments without breaking its turn. / Moshi 可发出小反馈而不打断自己的轮次 |

> **【中文解读】**延伸阅读 proporciona un alto nivel de recursos para el aprendizaje profundo. Estos artículos y cursos son los referentes clásicos en el campo, adecuados para los lectores que necesitan una comprensión profunda.


## Más Leer más Leer más

- [Défossez et al. (2024). Moshi — speech-text foundation model](https://arxiv.org/html/2410.00037v2)- El periódico.
  Desfossez 等(2024). Moshi语音-文本基础模型原始论文──
- [Kyutai Labs (2026). Hibiki-Zero](https://arxiv.org/abs/2602.12345) Translaciones en streaming sin datos alineados.
  Laboratorios de Kyutai ([[2026]]). Hibiki-Zero 无需对齐数据的流式翻译──
- [Sesame (2025). Crossing the uncanny valley of voice](https://www.sesame.com/research/crossing_the_uncanny_valley_of_voice) Específico del MCS.
  Sesame (en inglés) 跨越语音的恐怖谷 (en inglés) 规范 (en inglés) 规范 (en inglés) 规范 (en inglés) 规范 (en inglés) 规范 (en inglés) 规范 (en inglés) 规范 (en inglés) 规范 (en inglés) 规范 (en inglés) 规范 (en inglés) 规范 (en inglés) 规范 (en inglés) 规范 (en inglés) 规范 (en inglés) 规范 (en inglés) 规范 (en inglés) 规范 (en inglés) 规范 (en inglés) 规范 (en inglés) 规范 (en inglés) 规范 (en inglés) 规范 (en inglés) 规范 (en inglés) 规范 (en inglés) 规范 (en inglés) 规范) 规范 (en inglés) 跨越语音的恐怖谷) 跨越语音的恐怖谷
- [Kyutai — Moshi repo](https://github.com/kyutai-labs/moshi) instalar + servidor.
  KyutaiMoshi 仓库安装 + 服务器。
- [OpenAI — Realtime API](https://platform.openai.com/docs/guides/realtime) cerrado comercial.
  OpenAIRealtime APIClosed Source Commercial
- [Kyutai — Delayed Streams Modeling](https://github.com/kyutai-labs/delayed-streams-modeling) el marco STT/TTS debajo del capó.
  KyutaiDelayed Streams Modeling底层 STT/TTS 框架──

> **【中文解读】**延伸阅读 proporciona recursos de alta calidad para el aprendizaje profundo, incluyendo artículos, tutorials y herramientas.

