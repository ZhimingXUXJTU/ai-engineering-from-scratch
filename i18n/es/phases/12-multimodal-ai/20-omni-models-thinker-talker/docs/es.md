# Modelos omni: Qwen2.5 Omni y el pensador-hablante dividido .

> La demostración del producto de GPT-4o en mayo de 2024 fue disruptiva no por el modelo subyacente sino por la forma del producto  una interfaz de voz donde se habla, el modelo ve lo que ve la cámara, y habla de nuevo en menos de 250 ms. El ecosistema abierto pasó el resto de 2024 y 2025 corriendo para alcanzar esa superficie de producto. Qwen2.5-Omni (marzo 2025) es el diseño abierto de referencia: un Thinker (gran transformador generador de texto) más un Talker (transformador generador de voz paralelo), unido por tokens de voz de transmisión. Mini-Omni lo simplificó, Moshi coincidió con su latencia, GLM-4-Voice lo extendió a chino. Esta lección lee la arquitectura de Thinker-Talker y el presupuesto de latencia que hace que el diálogo en tiempo real funcione.

> **【中文解读】**La ruptura de GPT-4o no se encuentra en el modelo de nivel inferior, sino en el formato de producto 250ms                                                                                                                                                                                                                                                 

**Type:** Build
**Languages:** Python (stdlib, streaming pipeline latency simulator + VAD loop)
**Prerequisites:** Phase 12 · 19 (audio-LLMs), Phase 12 · 16 (any-to-any)
**Time:** ~180 minutes

> ¿ Qué es esto ?**【前置】**学本节前请先掌握:Fase 12·16(MIO 任意到任意流式)、Fase 12·19(音频 LLM)、Fase 6·04(VAD 语音活动检测)。Qwen2.5-Omni = "开源版 GPT-4o",核心是思想家讲话者 双流架构,并行化降低延迟到250ms内。
> ¿ Qué es esto ?**【类比】**Pensador-Hablante 架构 = "翻译员 + 同传播音员"。其他 omni 模型 = 一个人又要思考又要说话(串行,慢);Qwen2.5-Omni = Pensador(大脑,想"说什么")+ Hablante(嘴巴,把文字变语音)并行工作。Thinker 流式吐出文本代币,Talker 一边接收一边合成语音,用户听到的是流水线输出,总延迟大幅降低。

## Objetivos de aprendizaje

- Divide la línea de inferencia en Pensador (razón del texto) y Hablador (sintesis del habla) y explique por qué funciona la transmisión paralela.
  La traducción del lenguaje chino se basa en el lenguaje chino.
- Calcular el presupuesto de tiempo a primer byte de audio (TTFAB) para una interacción de conversación, componente por componente.
  El tiempo de la conversación se ha convertido en un tiempo de conversación.
- Describa la posición de TMRoPE en línea con el tiempo codificando en la visión, el audio y el texto dentro del Pensador.
  En el texto se describe Thinker 内 TMRoPE 跨视觉、音频和文本的时间对齐位置编码──
- Nombren los tres patrones de conversación en tiempo real: medio duplex, turno, doble completo.
  El lenguaje chino es el idioma de la lengua china.

## El problema es la introducción del problema

Un asistente de voz en tiempo real tiene que hacer mucho, rápido:

> El asistente de voz necesita hacer muchas cosas rápidamente:

1. Escucha al usuario. Tokenización de voz en tiempo real, detección de actividad de voz (VAD) para saber cuando terminan de hablar.
   En el caso de los usuarios de la lengua árabe, el idioma se utiliza para la traducción de la lengua árabe.
2. Opcionalmente, la entrada de la cámara a 2-4 FPS, fluye al Thinker junto con el audio.
   China:                                                                                                                                                                                                                                                              
3. Piensa, compone una respuesta condicionada al historial de conversación.
   Según el diálogo histórico, la organización respondió.
4. Sintéese tokens de audio, decodifique a forma de onda, transmita a los altavoces del usuario.
   En el caso de los usuarios de la plataforma de intercambio, el usuario puede utilizar la plataforma de intercambio de datos.

Cada paso añade latencia. La sensación de conversación requiere un total de ida y vuelta < 500ms  por debajo de eso, el usuario deja de notar el retraso. GPT-4o reclama ~250ms. Moshi ~160ms. Qwen2.5-Omni ~350-500ms.

> Cada paso aumenta la demora. El requisito de diálogo siempre vuelve a la hora de llegar.

Todo componente tiene que ser transmitido. Nada puede ser "parcela todo y luego decodificar".

> Cada componente necesita un tratamiento continuo. No se puede "procesar en primera batería y volver a resolver el código".

## El concepto central.

> **【中文解读】**Todo el mundo tiene que aprender a pensar y a hablar de su lengua, y a hablar de su lengua, y a hablar de su lengua.

> **【拓展：实时多模态交互**GPT-4o es el primer modelo de interacción real real-time multi-modelo: el usuario puede hacer preguntas de voz, el modelo puede ver imágenes de cámara simultáneamente, responder en el tiempo real de voz.


### Pensador y hablador

La descomposición de Qwen2.5 Omni:

> Qwen2.5-Omni 的分解:

- Pensador: un transformador de generación de texto 7B-80B. Consume tokens de texto + imagen + audio entrelazados. Saque tokens de texto que representan lo que se dice.
  En el texto original, el texto se traduce en el texto de la traducción de la traducción de la traducción de la traducción de la traducción de la traducción de la traducción de la traducción de la traducción de la traducción de la traducción de la traducción de la traducción de la traducción de la traducción de la traducción de la traducción de la traducción de la traducción de la traducción de la traducción de la traducción de la traducción de la traducción de la traducción de la traducción de la traducción de la traducción de la traducción de la traducción de la traducción de la traducción de la traducción de la traducción de la traducción de la traducción de la traducción de la traducción de la traducción de la traducción de la traducción de la traducción de la traducción de la traducción de la traducción de la traducción de la traducción de la traducción de la traducción de la traducción de la traducción de la traducción de la traducción de la traducción de la traducción de la traducción de la traducción de la traducción de la traducción de la traducción de la traducción de la traducción de la traducción de la traducción de la traducción de la traducción de la traducción de la traducción de la traducción de la traducción de la traducción de la traducción de la traducción de la traducción de la traducción de la traducción de la traducción de la traducción de la traducción de la traducción de la traducción de la traducción de la traducción de la traducción de la traducción de la traducción de la lengua de la lengua de la lengua inglesa.
- Hablante: un transformador generador de voz más pequeño (200M-1B). Consume los tokens de salida de texto de Thinker más los tokens recientes de contexto de habla.
  El lenguaje de la lengua se traduce en lenguaje de la lengua de la lengua de la lengua de la lengua de la lengua de la lengua de la lengua de la lengua de la lengua de la lengua de la lengua de la lengua de la lengua de la lengua de la lengua de la lengua de la lengua de la lengua de la lengua de la lengua de la lengua de la lengua de la lengua de la lengua de la lengua de la lengua de la lengua de la lengua de la lengua de la lengua de la lengua de la lengua de la lengua de la lengua de la lengua de la lengua de la lengua de la lengua de la lengua de la lengua de la lengua de la lengua de la lengua de la lengua de la lengua de la lengua de la lengua de la lengua de la lengua de la lengua de la lengua de la lengua de la lengua de la lengua de la lengua de la lengua de la lengua de la lengua de la lengua de la lengua de la lengua de la lengua de la lengua de la lengua de la lengua de la lengua de la lengua de la lengua de la lengua de la lengua de la lengua de la lengua de la lengua de la lengua de la lengua de la lengua de la lengua de la lengua de la lengua de la lengua de la lengua de la lengua de la lengua de la lengua de la lengua de la lengua de la lengua de la lengua de la lengua de la lengua de la lengua de la lengua de la lengua de la lengua de la lengua de la lengua de la lengua de la lengua de la lengua de la lengua de la lengua de la lengua de la lengua de la lengua de la lengua de la lengua de la lengua de la lengua de la lengua de la lengua de la lengua de la lengua de la lengua de la lengua de la lengua de la lengua de la lengua de la lengua de la lengua de la lengua de la lengua de la lengua de la lengua de la lengua de la lengua de la lengua de la lengua de la lengua de la lengua de la lengua de la lengua de la lengua de la lengua de la lengua de la lengua de la lengua de la lengua de la lengua de la lengua de la lengua de la lengua de la lengua de la lengua de la lengua de la lengua de la lengua de la lengua de la lengua de la lengua de la lengua de la lengua de la lengua de la lengua de la lengua de la lengua de la lengua de la lengua de la lengua de la lengua de la lengua de la lengua de la lengua de la lengua de la lengua de la lengua de la lengua
- Decodificador de voz: un decodificador de forma de onda de transmisión (SNAC, familia MoVQGAN) que lleva tokens de voz a muestras de audio en tiempo real.
  En el caso de los que se encuentran en la zona de la zona central, el número de usuarios de la zona central es de aproximadamente un millón de personas.

La separación es importante. El pensador tiene que ser grande para un buen razonamiento. El hablante puede ser pequeño porque su trabajo es local  convertir texto en tokens de habla. El hablante más grande no es más expresivamente; es más lento.

> El pensador debe tener un gran talento para hacer buenas reflexiones. El hablante puede ser pequeño porque su tarea es la de un token de cambio de voz.

Correr ambos en paralelo:

> Y se ejecutó en dos:

1. El pensador emite un token de texto.
   En inglés, el pensador es un símbolo de la cultura.
2. El hablante consume t_i (a través de streaming) y emite tokens de habla s_i, s_{i+1}, ..., s_{i+k}.
   El lenguaje de la lengua se traduce en lenguaje de la lengua.
3. El decodificador de voz consume tokens de voz a medida que vienen y emite muestras de audio.
   China: en el idioma de la lengua de los idiomas de la lengua de los idiomas de la lengua de los idiomas de la lengua de los idiomas de la lengua de los idiomas de la lengua de los idiomas de la lengua de los idiomas de la lengua de los idiomas de la lengua de los idiomas de la lengua de los idiomas de la lengua de los idiomas de la lengua de los idiomas de la lengua de los idiomas de la lengua de los idiomas de la lengua de los idiomas de la lengua de los idiomas de la lengua de los idiomas de la lengua de los idiomas de la lengua de los idiomas de los idiomas de los idiomas de la lengua de los idiomas de los idiomas de los idiomas de los idiomas de los idiomas de los idiomas de los idiomas de los idiomas de los idiomas de los idiomas de los idiomas de los idiomas de los idiomas de los idiomas de los idiomas de los idiomas de los idiomas de los idiomas de los idiomas de los idiomas de los idiomas de los idiomas de los idiomas de los idiomas de los idiomas de los idiomas de los idiomas de los idiomas de los idiomas de los idiomas de los idiomas de los idiomas de los idiomas de idiomas de idiomas de idiomas de idiomas de idiomas de idiomas de idiomas de idiomas de idiomas de idiomas de idiomas de idiomas de idiomas de idiomas de idiomas de idiomas de idiomas de idiomas de idiomas de idiomas de idiomas de idiomas de idiomas de idiomas de idiomas de idiomas de idiomas de idiomas de idiomas de idiomas de idiomas de idiomas de idiomas de idiomas de idiomas de idiomas de idiomas de idiomas de idiomas de idiomas de idiomas de idiomas de idiomas de idiomas de idiomas de idiomas de idiomas de idiomas de idiomas de idiomas de idiomas de idiomas de idiomas de idiomas de idiomas de idiomas de idiomas de idiomas de idiomas de idiomas de idiomas de idiomas de idiomas de idiomas de idiomas de idiomas de idiomas de idiomas de idiomas de idiomas de idiomas de idiomas de idiomas de idiomas de idiomas de idiomas de
4. Para cuando Thinker esté en el token de texto, Talker ya ha transmitido audio para t_0..t_{i+2}.
   Cuando el pensador está tratando el texto, el hablante ya está en la emisión.

> **【中文解读】**El pensador 必須大(7B-80B) para hacer una buena reflexión, el hablante puede ser pequeño(200M-1B) porque su tarea es la de una localización de un texto translúcido.

> **【拓展：Token 速率数学】**16kHz 语音使用50Hz 基础语音代币, significa que por segundo se necesitan 50 语音代币──Horror cada segundo debe emitir >= 50 token 才能跟上──H100 上,200-300M de H100 语音每秒可输出数百 token,远超需求; pero 7B Talker 会跟不上──Es por eso que se necesita un pequeño modelo de hablante especializado y no un modelo principal en directo──

### Posiciones multimodal TMRoPE  alineadas en el tiempo

El pensador necesita integrar marcos de imagen (alcanzando, digamos, 4 FPS), marcos de audio (alcanzando a 50 marcos/segundo) y texto del historial de conversaciones.

> El pensador necesita integrar imágenes (por ejemplo 4 FPS) 音频(50 /秒) y el texto en el diálogo histórico──pueces secuencias ordenadas (todas las imágenes、 y luego todos los audio、 y luego el texto) se perderá tiempo para reunirse──

TMRoPE asigna sellos de tiempo absolutos a cada token. El token de visión en t=2.3s. El token de audio en t=2.32s. El token de texto del usuario "detenta" en t=2.35s. RoPE gira la atención por sello de tiempo; el modelo los ve como temporalmente simultáneos.

> TMRoPE para cada token Distribución absoluta tiempo──visión token 在 t=2.3s──音频 token 在 t=2.32s── usuario de "stop" texto token 在 t=2.35s──RoPE 按时间旋转注意力;模型将它们视为时间同时发生──

Esta es la infraestructura para "el saludaba mientras saludaba" para que funcione  el modelo ve el marco de vídeo y el audio en el mismo momento conceptual.

> Es "el que está en el lado de la mano dice que está bien" puede funcionar normalmente infraestructura  modelo en el mismo concepto  video y audio

### Sintesis de habla en streaming

Los tokens de voz deben transmitirse. Mini-Omni (Xie & Wu, 2024) introdujo "modelos de lenguaje pueden escuchar, hablar mientras piensan en transmisión": los tokens de salida de pensador y los tokens de salida de conversador se intercaudan en la misma secuencia.

> 语音代币 必须流式传输──Mini-Omni 引入了"语言模型可以在流式思考的同时听和说":Pensador 输出代币 和 Talker 输出代币 在同一序列中交错──Pensador Una vez que se presenta el siguiente texto de la señal, Talker 立即触发──没有批量边界──

Moshi (Défossez et al., octubre 2024) es la implementación abierta más rápida. 160ms TTFAB en un solo A100. Arquitectura: un único transformador 7B que emite tokens de texto y habla en posiciones alternadas, con un "monólogo interno" que separa el flujo de pensamiento del flujo de habla. Esto es efectivamente Thinker + Talker fusionado en un modelo con un entrenamiento cuidadoso.

> Moshi es la implementación de código abierto más rápida. Solo A100 en 160 ms TTFAB.

### VAD y la toma de vueltas

La detección de la actividad de voz se ejecuta en el lado de entrada.

> 语音活动检测在输入端运行──两种模式:

- Medio dúplex: el usuario habla, el modelo escucha. El modelo habla, el usuario escucha.
  En el caso de los usuarios de la red, el usuario puede utilizar la red de red de red de la red de red de red de red de red de red de red de red de red de red de red de red de red de red de red de red de red de red de red de red de red de red de red de red de red de red de red de red de red de red de red de red de red de red de red de red de red de red de red de red de red de red de red de red de red de red de red de red de red de red de red de red de red de red de red de red de red de red de red de red de red de red de red de red de red de red de red de red de red de red de red de red de red de red de red de red de red de red de red de red de red de red de red de red de red de red de red de red de red de red de red de red de red de red de red de red de red de red de red de red de red de red de red de red de red de red de red de red de red de red de red de red de red de red de red de red de red de red de red de red de red de red de red de red de red de red de red de red de red de red de red de red de red de red de red de red de red de red de red de red de red de red de red de red de red de red de red de red de red de red de red de red de red de red de red de red de red de red de red de red de red de red de red de red de red de red de red de red de red de red de red de red de red de red de red de red de red de red de red de red de red de red de red de red de red de red de red de red de red de red de red de red de red de red de red de red de red de red de red de red de red de red de red de red de red de red de red de red de red de red de red de red de red de red de red de red de red de red de red de red de red de red de red de red de red de red de red de red de red de red de red de red de red de red de red de red de red de red de red de red de red de red de red de red de
- Duplex completo: ambos pueden hablar simultáneamente. El modelo puede retrocanicular ("uh-huh") o interrumpir.
  En el caso de los dos países, el gobierno de China ha adoptado una política de paz con el fin de mantener la paz.

Qwen2.5 Omni admite medio duplex por defecto, con la toma de vueltas a través del umbral de silencio.

> Qwen2.5 Omni 默认支持半双工, 通过静音值实现轮流──全双工需要应用层处理──

### Qwen3-Omni (novembre 2025)

El sucesor. Qwen3-80B Thinker, más grande Talker, mejoró TMRoPE-v2. La latencia cerca de 250ms de GPT-4o. Pesos abiertos.

> 继任者──Qwen3-80B Pensador, más grande Hablante,改进的TMRoPE-v2──延迟接近 GPT-4o 的250ms──开放权重──OmniBench 基准与 Gemini 2.0 Live 竞争──

### Presupuesto de latencia de producción

Para una interacción de transmisión típica:

> 典型流式交互:

- Mic -> fichas de audio: 40-80 ms.
  En inglés, el nombre de la señal de la señal de la señal de la señal de la señal de la señal de la señal de la señal de la señal de la señal de la señal de la señal de la señal de la señal de la señal de la señal de la señal de la señal de la señal de la señal de la señal de la señal de la señal de la señal de la señal de la señal de la señal de la señal de la señal de la señal de la señal de la señal de la señal de la señal de la señal de la señal de la señal de la señal de la señal de la señal de la señal de la señal de la señal de la señal de señal de la señal de señal de la señal de señal de la señal de señal de la señal de señal de señal de la señal de señal de señal de la señal de señal de señal de señal de la señal de señal de señal de señal de señal de la señal de señal de señal de señal de señal de 40-80ms.
- Preempleo (prompt + historial): 100-200 ms en 7B, mucho más en 70B.
  En inglés, el nombre de la persona que se encuentra en el sitio web es el nombre de la persona que se encuentra en el sitio web.
- Primero token de texto de pensador: 40ms.
  Sin embargo, el proyecto de la empresa no se ha convertido en un proyecto de investigación.
- El hablador procesa el primer token de texto: 20 ms.
  En el lenguaje de la lengua se trata de un lenguaje de la lengua.
- Los primeros tokens de voz se comprometen: 40 ms.
  En inglés, el nombre de la persona que ha sido enviada es el de la persona que ha sido enviada.
- Descodificación residual-VQ: 30 ms.
  En inglés, el tiempo de la prueba es de 30 minutos.
- Descodificación de la forma de onda de habla: 50-80 ms.
  En inglés, el tiempo de la transmisión de datos es de 50 a 80 ms.

TTFAB total: 320-510ms en 7B, 600-900ms en 70B. La calidad fronteriza generalmente significa 70B +; de ahí la brecha de latencia fronteriza.

> 总 TTFAB:7B 约 320-510ms,70B 约 600-900ms──前沿质量通常意味着70B+; por lo tanto, existe una diferencia de延迟前沿──

### Matemáticas de la tasa de tokens

En 16 kHz de habla con 50 Hz de tokens de voz base, se necesitan 50 tokens de voz por segundo de salida. El hablante debe emitir ≥50 tok/s para mantenerse al día. En un rendimiento típico de LLM de 30-80 tok/s en un H100, un pequeño 200-300M de hablante es lo suficientemente rápido; un 7B de hablante quedaría atrás.

> 16kHz 语音以 50 Hz 基础语音代币 计算,每秒输出需要50 语音代币──讲者 必须以 ≥50 tok/s 的速度输出──H100 上典型 LLM 吞吐量为 30-80 tok/s,小型(200-300M)

Esta es la razón por la cual existen pequeños modelos dedicados Talker en lugar de "sólo usar el modelo principal".

> Es por eso que existe un modelo de charla especial y no un modelo principal de uso directo.

## Usalo con el marco de ejecución
```figure
l5-thinker-talker
```

## Usalo

`code/main.py`¿Qué es esto ?

- Simula una línea de pensadores-hablantes con tasas falsas de emisión de tokens.
  Sinopsis: El hombre que habla de la verdad es un hombre que habla de la verdad.
- Computa TTFAB para los tamaños de modelos configurables y las tasas de muestra de micrófono.
  Traducción:Por el modelo de tamaño y la tasa de la calidad de la máquina.
- Demuestra medio doble giro con umbral de silencio VAD.
  En español, el nombre de la obra es "VAD".

## Envíe el producto .

Esta lección produce`outputs/skill-omni-streaming-budget.md`. Dado el objetivo TTFAB y el conjunto de características (vision-in, bilingüe, duplex completo) de un producto de voz en tiempo real, elige Qwen2.5-Omni, Qwen3-Omni, Moshi o Mini-Omni y mide el Thinker/Talker.

> 本课产 出  `outputs/skill-omni-streaming-budget.md`△ dado cierto tiempo de los productos de voz TTFAB 目标和功能集(视觉输入、双语、全双工), seleccionar Qwen2.5Omni、Qwen3-Omni、Moshi o Mini-Omni 并配置 Thinker/Talker 大小──

## Los ejercicios.

1. Su objetivo TTFAB es de 300ms. En un pensador 7B y 300M Talker, escriba la latencia de cada componente. Su objetivo TTFAB  objetivo es de 300ms.

2. Qwen2.5-Omni utiliza TMRoPE. Describa lo que el modelo ve para un prompt donde el usuario comienza a hablar a t=1s y la cámara capta un gesto a t=1.2s. Qwen2.5-Omni utiliza TMRoPE。 describir modelo en usuario t=1s 开始说话、摄像头 t=1.2s 捕获手势时看的输入。

3. El soporte de doble completo requiere que el modelo emita audio mientras escucha. Proponga un formato de datos de entrenamiento que enseñe esto.

4. Lea el artículo de Moshi Sección 4. Describe la separación del "monólogo interno" y por qué evita la división Pensador-Hablante.

5. Compute el presupuesto de rendimiento: ¿a qué velocidad debe emitir un Talker tokens para mantenerse al día con el discurso de 16 kHz a 50 tokens de capa base/segundo? 计算吞吐量预算:Talker 需要多快的速度输出 token 才能跟上 16 kHz 语音(50 基础层 token/秒)?

## Términos clave .

| Term | What people say | What it actually means | 中文释义 |
|------|-----------------|------------------------|---------|
| Thinker | "Reasoning brain" 思考者 | Large text-generating transformer producing what to say 生成"说什么"的大型文本生成 Transformer | |
| Talker | "Speech-generating mouth" 说话者 | Small transformer producing discrete speech tokens from Thinker's text 将 Thinker 文本转为语音 token 的小型 Transformer | |
| TTFAB | "Latency budget" 首音频字节延迟 | Time-to-first-audio-byte: from user speech end to first audio sample out 从用户说话结束到首个音频样本输出的延迟 | |
| TMRoPE | "Time-aligned RoPE" 时间对齐旋转位置编码 | Position encoding using absolute timestamps across vision, audio, text 跨视觉、音频、文本使用绝对时间戳的位置编码 | |
| Half-duplex | "Turn-taking" 半双工 | User and model alternate; VAD silence detects user-done 用户和模型交替说话；VAD 静音检测用户说完 | |
| Full-duplex | "Simultaneous" 全双工 | Model can speak and listen at the same time; backchannel capable 模型可同时说话和监听；支持回话 | |
| Inner monologue | "Moshi separation" 内心独白 | Single-model design where thinking-stream and speaking-stream interleave 单模型设计，思考流和说话流交替出现 | |

## Más Leer más Leer más

- [Xu et al. — Qwen2.5-Omni (arXiv:2503.20215)](https://arxiv.org/abs/2503.20215)
- [Qwen Team — Qwen3-Omni (arXiv:2509.17765)](https://arxiv.org/html/2509.17765v1)
- [Xie & Wu — Mini-Omni (arXiv:2408.16725)](https://arxiv.org/abs/2408.16725)
- [Défossez et al. — Moshi (arXiv:2410.00037)](https://arxiv.org/abs/2410.00037)
- [Zeng et al. — GLM-4-Voice (arXiv:2412.02612)](https://arxiv.org/abs/2412.02612)
