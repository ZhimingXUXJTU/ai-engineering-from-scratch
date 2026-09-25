# Agentes de voz: Pipecat y LiveKit

> Los agentes de voz son una categoría de producción de primera clase en 2026. Pipecat le ofrece un pipeline basado en Python (VAD → STT → LLM → TTS → transporte). LiveKit Agents conecta modelos de IA con los usuarios a través de WebRTC.

**Type:** Learn | **类型:** 学习
**Languages:** Python (stdlib) | **语言:** Python (标准库)
**Prerequisites:** Phase 14 · 01 (Agent Loop), Phase 14 · 12 (Workflow Patterns) | **前置知识:** 见原文
**Time:** ~60 minutes | **时间:** 见原文

## Objetivos de aprendizaje

- Describa la tubería basada en el marco de Pipecat: DOWNSTREAM (fuente→sink) y UPSTREAM (control).
- Nombre de las etapas de la tubería de voz canónica y que transportan los soportes de Pipecat.
- Explica las dos clases de agentes de voz de LiveKit Agents (MultimodalAgent, VoicePipelineAgent) y cuándo cada una se ajusta.
- Resumen las expectativas de latencia de producción 2026 y cómo impulsan las opciones de arquitectura.

## El problema es la introducción del problema

Los agentes de voz no son un bucle de texto con TTS encendido. Los presupuestos de latencia son brutales (~ 600 ms), el audio parcial es el predeterminado, la detección de giras es un modelo, y los transportes van desde la telefonía SIP a WebRTC.

> 语音 Agent 不是文本循环加上 TTS──延迟预算极极苛(约600ms),部分音频是默认状态,轮次检测是一个模型,传输方式从电话SIP到WebRTC 不等──你要么构建一个基于的管道(Pipecat),要么依赖一个平台(LiveKit)──


> **【中文解读】**语音 Agent 需要实时处理音频流语音识别(ASR) LLM 推理、语音合成(TTS) de retraso debe ser de 300ms en el interior de mantener el diálogo natural。Pipecat 和 LiveKit 提供构建低延迟语音 Agent marco y infraestructura。

> **{【拓展：Pipecat（开源框架）和 LiveKit（实时音频基础设施）是 2026 年语音 Agent 生...】}**Pipecat (en inglés) es un sistema de comunicación de voz de la Unión Europea (UE) que se desarrolla desde el año 2026 hasta el año 2026.

> ¿ Qué es esto ?**【前置】**学本节前请先掌握:Fase 14·01(Agent Loop) 理解 ReAct 循环,本节在循环外加一层音频管道;Fase 14·12(Workflow Patterns) 理解多阶段工作流的概念──另外最好有数字信号处理基础概念──采样率、、流式处理),否则见"框架为基础的管道" 会很──

## El concepto central.

### El producto se clasifica en el anexo II del Reglamento (UE) n.o 1069/2013.

- Marco de tuberías basado en marco Python.
- `Frame`¿ Qué es esto ?`FrameProcessor`- ¿Qué es eso?
- Dos direcciones de flujo:
  - **DOWNSTREAM** fuente → fregadero (audio en, TTS fuera).
  - **UPSTREAM** retroalimentación y control (cancelación, métricas, barge-in).
- `PipelineTask`gestiona el ciclo de vida con eventos (`on_pipeline_started`¿ Qué ?`on_pipeline_finished`¿ Qué ?`on_idle_timeout`) y observadores de métricas/trazaje/RTVI.

Tipico de tubería:

```
VAD (Silero) → STT → LLM (context alternates user/assistant) → TTS → transport
```

Transporte: diario, LiveKit, SmallWebRTCTransport, FastAPI WebSocket, WhatsApp.

> ¿ Qué es esto ?**【类比】**Pipecat de la línea de tubería basada en el marco 像汽车流水线:每个工位(Procesador) sólo hace una cosa  VAD 工位识别有没有人说话、STT 工位把语音转文字、LLM 工位想回复、TTS 工位把文字转语音),车架(Frame) desde el camino hacia el río hacia el fondo (DOWNSTREAM), cualquier un trabajo puede encontrar un problema de calidad puede hacerse en línea roja stop  UPSTREAM cancelar  es el mecanismo de barge-in 打断) 

> 语音代理 结合 LLM 和实时语音处理──Pipecat 和 LiveKit son dos tipos principales de agencias de voz 框架,分别处理音频管道和实时通信──

Pipecat Fluxes añade conversaciones estructuradas (máquinas de estado). Pipecat Cloud es el tiempo de ejecución administrado.

> 语音代理 结合 LLM 和实时语音处理──Pipecat 和 LiveKit son dos tipos principales de agencias de voz 框架,分别处理音频管道和实时通信──

### Los agentes de LiveKit (livekit/agentes)

- Se conectan modelos de IA a los usuarios a través de WebRTC.
- Conceptos clave: `Agent`¿ Qué ?`AgentSession`¿ Qué ?`entrypoint`¿ Qué ?`AgentServer`¿ Qué ?
- Dos clases de agentes de voz:
  - **MultimodalAgent** audio directo a través de OpenAI en tiempo real o equivalente.
  - **VoicePipelineAgent** STT → LLM → TTS cascada; da control a nivel de texto.
- Detección semántica de la vuelta a través de un modelo transformador.
- Integración de MCP nativo.
- Telefono por SIP.
- 50+ modelos sin claves de API a través de LiveKit Inference; 200+ más a través de plugins.

### Plataformas comerciales

Vapi (~ 450600ms en una pila premium optimizada) y Retell (~ 600ms de extremo a extremo en 180 llamadas de prueba) se basan en esto.

> ¿ Qué es esto ?**【困惑】**P: MultimodalAgent (en inglés) (en inglés) (en inglés) (en inglés) (en inglés) (en inglés) (en inglés) (en inglés) (en inglés) (en inglés) (en inglés) (en inglés) (en inglés) (en inglés) (en inglés) (en inglés) (en inglés) (en inglés) (en inglés) (en inglés) (en inglés) (en inglés) (en inglés) (en inglés) (en inglés) (en inglés) (en inglés) (en inglés) (en inglés) (en inglés) (en inglés) (en inglés) (en inglés) (en inglés) (en inglés) (en inglés) (en inglés) (en inglés) (en inglés) (en inglés) (en inglés) (en inglés) (en inglés) (en inglés) (en inglés) (en inglés) (en inglés) (en inglés) (en inglés) (en inglés) (en inglés) (en inglés) (en inglés) (en inglés) (en inglés) (en inglés) (en inglés) (en inglés) (en inglés) (en inglés) (en inglés) (en inglés) (en inglés) (en inglés) (en inglés) (en inglés) (en inglés) (en inglés) (en inglés) (en inglés) (en inglés) (en inglés) (en inglés) (en inglés) (en inglés) (en inglés) (en inglés) (en inglés) (en inglés) (en inglés) (en inglés) (en inglés) (en inglés) (en inglés (en inglés) (en inglés) (en inglés (en inglés) (en inglés) (en inglés) (en inglés (en inglés) (en inglés) (en inglés (en) (en inglés (en) (en) (en) (en) (en) (en) (en) (en) (en) (en) (en) (en) (en) (en) (en) (en) (en) (en) (en) (en) (en) (en) (en) (en) (en) (en) (en) (en) (en) (en) (en) (en) (en) (en) (en) (en) (en) (en) (en) (en) (en) (

> Vapi(optimización posterior de alto nivel de la conversación de 450-600ms) y Retell(180 veces de prueba de la conversación de final a final de 600ms) construido sobre estos.

> 语音代理 结合 LLM 和实时语音处理──Pipecat 和 LiveKit son dos tipos principales de agencias de voz 框架,分别处理音频管道和实时通信──

### Cuando este patrón va mal

- **No barge-in handling.**El usuario interrumpe; el agente sigue hablando. Requiere UPSTREAM cancelar los cuadros en Pipecat, equivalente en LiveKit.
- **STT confidence ignored.**Transcripciones de baja confianza alimentadas al LLM como si fueran un evangelio.
- **TTS mid-sentence cutoff.**Cuando la tubería cancela la emisión en medio, TTS necesita saber o cortar el audio.
- **Latency budget ignored.**Cada componente añade 50200ms. Sumar su cadena antes de enviar.

> **没有打断处理。**Usuario: Abre; Agente: Continuar hablando: Necesita UPSTREAM:
> **忽略 STT 置信度。**低信度转录被当作真理传给LLM. 根据信度门控或请求确认.
> **TTS 句中截断。**Cuando el tubo en el medio del habla se elimina, TTS necesita saber o cortar el audio.
> **忽略延迟预算。**Cada componente aumenta 50-200ms.

### Las latencias típicas para 2026

- VAD: 2060ms
- TPS parcial: 100250ms
- LLM primer token: 150400ms
- TTS primer audio: 100200ms
- RTT de transporte: 3080ms

El tiempo de entrega de 450 a 600 ms es de primera calidad. 800 a 1200 ms es común. Cualquier cosa > 1500 ms se siente rota.

> 端到端 450-600ms es alto nivel. 800-1200ms es habitual.

> 语音代理 结合 LLM 和实时语音处理──Pipecat 和 LiveKit son dos tipos principales de agencias de voz 框架,分别处理音频管道和实时通信──

## Construye y realiza.

> ️ **【易错点】**Nuevo teléfono de la voz de la gente de la ciudad de Nueva York**不做 barge-in 处理** usuario打断时 Agent还在自顾自地说,体验极差,必须在TTS procesador 监听UPSTREAM cancelación de marco 并立即停止音频输出──(2) **忽略 STT 置信度**置信度 0.3 的""被当成用户回答,Agencia 走错分支;修复:confianza < 0.7 时让Agencia 反问"我没听清,能再说一次吗"―(3) **延迟预算算总账** Individualmente ver cada componente todo el tiempo  VAD 40ms + STT 200ms + LLM 300ms + TTS 150ms = 690ms), pero en la línea de arriba, después de la línea hasta la línea de 1200ms, ya que se ha perdido la red RTT y la fila de espera.
```figure
voice-pipeline
```

## Construye el mismo

`code/main.py`es un tubo de juguete basado en un marco con:

> 语音代理 结合 LLM 和实时语音处理──Pipecat 和 LiveKit son dos tipos principales de agencias de voz 框架,分别处理音频管道和实时通信──

- `Frame`tipos (audio, transcripción, texto, tts_audio, control).
- `Processor`interfaz con `process(frame)`¿ Qué ?
- Un oleoducto de cinco etapas (VAD → STT → LLM → TTS → transporte) como procesadores con guión.
- Un marco de cancelación UPSTREAM para demostrar el barrido.

- ¿Qué quieres decir ?

```
python3 code/main.py
```

El rastro muestra flujo normal y una cancelación de barga que detiene el TTS en medio de la pronunciación.

>  Trace muestra el proceso normal y un interrupto de TTS en el medio del discurso 

> 语音代理 结合 LLM 和实时语音处理──Pipecat 和 LiveKit son dos tipos principales de agencias de voz 框架,分别处理音频管道和实时通信──

## Usalo con el marco de ejecución

- **Pipecat**para el control total  procesadores personalizados, proveedores de Python-first, enchufables.
- **LiveKit Agents**para las primeras implementaciones y telefonía de WebRTC.
- **Vapi / Retell**para agentes de voz alojados sin un equipo WebRTC.
- **OpenAI Realtime / Gemini Live**para la entrada/salida directa de audio (MultimodalAgent).

## Envíe el producto .

`outputs/skill-voice-pipeline.md`Esta plataforma tiene una tubería de voz en forma de Pipecat con VAD + STT + LLM + TTS + transporte más manejo de barcazas.

> `outputs/skill-voice-pipeline.md`Construir un tubo de voz de Pipecat 形态, que incluya VAD + STT + LLM + TTS + 传输以及打断处理──

> 语音代理 结合 LLM 和实时语音处理──Pipecat 和 LiveKit son dos tipos principales de agencias de voz 框架,分别处理音频管道和实时通信──

## Los ejercicios.

1. Añadir un observador de métricas a su pipeline de juguetes: contar cuadros por etapa por segundo. ¿Dónde se acumula la latencia?
  En inglés, "pensar y practicar" significa "pensar y practicar".
2. Implementar STT con puertas de confianza: por debajo del umbral, pedir "puedes repetir eso?"
  En inglés, "pensar y practicar" significa "pensar y practicar".
3. Añadir detección semántica de giro: regla simple  si la transcripción termina con "?", final de giro.
  En inglés, "pensar y practicar" significa "pensar y practicar".
4. Lea los documentos de transporte de Pipecat. Cambiar el transporte stdlib por la configuración de SmallWebRTCTransport (stub).
  En inglés, "pensar y practicar" significa "pensar y practicar".
5. Mide una cascada OpenAI en tiempo real vs STT+LLM+TTS en la misma consulta. ¿Qué costo de latencia tiene el control a nivel de texto?
  En inglés, "pensar y practicar" significa "pensar y practicar".

## Términos clave .

| Term | What people say | What it actually means |
|------|----------------|------------------------|---|
| Frame | "Event" | Typed unit of data in the pipeline (audio, transcript, text, control) |  |
| Processor | "Pipeline stage" | Handler with process(frame) |  |
| DOWNSTREAM | "Forward flow" | Source to sink: audio in, speech out |  |
| UPSTREAM | "Feedback flow" | Control: cancel, metrics, barge-in |  |
| VAD | "Voice activity detection" | Detects when user is speaking |  |
| Semantic turn detection | "Smart end-of-turn" | Model-based decision that the user is done |  |
| MultimodalAgent | "Direct audio agent" | Audio in, audio out; no text in the middle |  |
| VoicePipelineAgent | "Cascade agent" | STT + LLM + TTS; text-level control |  |

## Más Leer más Leer más

- [Pipecat docs](https://docs.pipecat.ai/getting-started/introduction) tuberías basadas en marcos, procesadores, transportes
  En el caso de los niños, el nombre de la persona que se encuentra en el lugar de residencia es el de la persona que se encuentra en el lugar de residencia.
- [LiveKit Agents docs](https://docs.livekit.io/agents/) WebRTC + primitiva de voz
  En el caso de los niños, el nombre de la persona que se encuentra en el lugar de residencia es el de la persona que se encuentra en el lugar de residencia.
- [Vapi](https://vapi.ai/) Plataforma de voz gestionada
  En el caso de los niños, el nombre de la persona que se encuentra en el lugar de residencia es el de la persona que se encuentra en el lugar de residencia.
- [Retell AI](https://www.retellai.com/) voz gestionada, con marcador de latencia
  En el caso de los niños, el nombre de la persona que se encuentra en el lugar de residencia es el de la persona que se encuentra en el lugar de residencia.
