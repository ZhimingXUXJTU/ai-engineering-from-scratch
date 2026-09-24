# Modelos de audio-linguas: el susurro a audio flamingo 3 arc 音频语言模型: desde susurro a audio flamingo 3

> Whisper (Radford et al., diciembre 2022) estableció el reconocimiento del habla  680k horas de habla multilingüe supervisionada de forma débil, un simple transformador de codificador-decodificador, un punto de referencia que hizo que cada lanzamiento posterior de ASR lo citara. Pero reconocer no es razonar. Para preguntar "qué instrumentos hay en esta grabación" o "qué emoción expresa el orador" o "qué pasó en el minuto 3" se requiere un entendimiento de audio, no una transcripción. Qwen-Audio, SALMONN, LTU y Audio Flamingo 3 de NVIDIA (AF3, julio 2025) construyeron progresivamente esa pila: mantener los codificadores de la clase Whisper, conectar los formadores Q, entrenar en datos de instrucción de audio-texto, agregar el razonamiento de cadena de pensamiento. Esta lección va por el arco.

> **【中文解读】**El susurro  resolvió la identificación de los idiomas, pero el reconocimiento no es una hipótesis. "Este episodio de la grabación utiliza un instrumento" El hablante expresa qué sentimiento etc.

**Type:** Build
**Languages:** Python (stdlib, log-Mel spectrogram + audio Q-former skeleton)
**Prerequisites:** Phase 6 (Speech and Audio), Phase 12 · 03 (Q-Former)
**Time:** ~180 minutes

> ¿ Qué es esto ?**【前置】**学本节前请先掌握:Fase 6·01-02(语音信号处理:FFT/Mel 频谱图/Whisper);Fase 12·03(Q-Former 桥接,本节复用为音频 Q-Former);Fase 7(Transformer 编码器-解码器)。音频 LLM = 视觉 LLM 的"听觉版",只是输入从图像补丁 变成 Mel 频谱图补丁──
> ¿ Qué es esto ?**【类比】**音频 LLM = "Para LLM 装耳朵"──Whisper = 助听器(只能转录不能思考); SALMONN = 聋学校的翻译员(Whisper 转录→LLM 思考);AF3 = 直接给 LLM 装耳(端到端听+想+答)──端到端的好处:能捕捉转录丢失的信息(语调、情绪、停顿), estas son las claves de la hipótesis──

## Objetivos de aprendizaje

- Computa un espectrograma log-Mel a partir de una forma de onda: ventana, FFT, bancos de filtros, transformación de registro.
  En inglés, el nombre de la máquina de calcular es el de la máquina de calcular.
- Compare las opciones de codificación: codificador de susurros, BEATs, híbrido AF-Whisper.
  En el caso de los equipos de clasificación, el equipo de clasificación de los equipos de clasificación de los equipos de clasificación de los equipos de clasificación de los equipos de clasificación de los equipos de clasificación de los equipos de clasificación de los equipos de clasificación de los equipos de clasificación de clasificación de los equipos de clasificación de clasificación de los equipos de clasificación de clasificación de los equipos de clasificación de clasificación de los equipos de clasificación de clasificación de clasificación de los equipos de clasificación de clasificación de clasificación de los equipos de clasificación de clasificación de clasificación de los equipos de clasificación de clasificación de clasificación de los equipos de clasificación de clasificación de clasificación de clasificación de los equipos de clasificación de clasificación de clasificación de clasificación de clasificación de clasificación de clasificación de clasificación de clasificación de clasificación de clasificación de clasificación de clasificación de clasificación de clasificación de clasificación de clasificación de clasificación de clasificación de clasificación de clasificación de clasificación de clasificación de clasificación de clasificación de clasificación de clasificación de clasificación de clasificación de clasificación de clasificación de clasificación de clasificación de clasificación de clasificación de clasificación de clasificación de clasificación de clasificación de clasificación de clasificación de clasificación de clasificación de clasificación de clasificación de clasificación de clasificación de clasificación de clasificación de clasificación de clasificación de clasificación de clasificación de clasificación de clasificación de clasificación de clasificación de clasificación de clasificación de clasificación de clasificación de clasificación de clasificación de clasificación de clasificación de clasificación de clasificación de clasificación de clasificación de clasificación de clasificación de clasificación de clasificación de clasificación de clasificación de clasificación de clasificación de clasificación de clasificación de clasificación de clasificación de clasificación de clasificación de clasificación de clasificación de clasificación de clasificación de clasificación de clasificación de clasificación de clasificación de clasificación de clasificación de clasificación de clasificación de clasificación de clasificación de clasificación de clasificación de clasificación de clasificación de clasificación de clasificación de clasificación de clasificación de clasificación de clasificación de clasificación de clasificación de clasificación de clasificación de clasificación de clasificación de clasificación de clasificación de clasificación de clasificación de clasificación de clasificación de clasificación de clasificación de clasificación de clasificación de clasificación de clasificación de clasificación de clasificación de clasificación de clasificación de clasificación de clasificación de clasificación de clasificación de clasificación de clasificación de clasificación de clasificación de clasificación de clasificación de clasificación de clasificación de clasificación de clasificación de clasificación de clasificación de clasificación de clasificación de clasificación de clasificación de clasificación de clasificación de clasificación de clasificación de clasificación de clasificación de clasificación de clasificación de clasificación de clasificación de clasificación de clasificación de clasificación de clasificación de clasificación de clasificación de clasificación de clasificación de clasificación de clasificación de clasificación de clasificación de clasificación de clasificación de clasificación de clasificación de clasificación de clasificación de clasificación de clasificación de clasificación de clasificación de clasificación de clasificación de clasificación de clasificación de clasificación de clasificación de clasificación de clasificación de clasificación de clasificación de clasificación
- Construir un formato de audio Q: N consultas de aprendizaje que atenden a parches de espectrograma.
  La información de la información de la red de radio de la red de radio de la red de radio de la red de radio de la red de radio de la red de radio de la red de radio de la red de radio de la red de radio de la red de radio de la red de radio de la red de radio de la red de radio de la red de radio de la red de radio de la red de radio de la red de radio de la red de radio de la red de radio de la red de radio de la red de radio de la red de la red de radio de la red de radio de la red de radio de la red de radio de la red de radio de la red de radio de la red de radio de la red de radio de la red de radio de la red de radio de la red de radio de la red de radio de la red de la red de radio de la red de radio de la red de la red de radio de la red de la red de radio de la red de radio de la red de la red de radio de la red de la red de radio de la red de la red de radio de la red de la red de radio de la red de la red de radio de la red de la red de la red de radio de la red de la red de la red de radio de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de la red de
- Explica cascada (Whisper-then-LLM) vs. capacitación de audio-LLM de extremo a extremo: por qué la escala de extremo a extremo es mejor para el razonamiento.
  China 后接 LLM) vs 端到端音频 LLM 训练:为什么端到端在推理上扩展更好──

## El problema es la introducción del problema

El reconocimiento de voz fue resuelto por Whisper. OCR de audio es una mercancía. Pero "comodidad" se detiene en la transcripción. Si el modelo no puede razonar sobre lo que escuchó  tiempo, altavoces, emoción, estructura musical, sonidos ambientales  la transcripción sola no puede impulsar las características del producto.

> 语音识别 has been Whisper 解决──音频 OCR 已成为基础能力── pero "基础能力" se detiene a la transcripción── si el modelo no puede razonar sobre lo que escucha, el tiempo, el habla, el sentimiento, la estructura musical, el ambiente, el sonido, sólo se puede utilizar para la transcripción, no puede impulsar la función de producto──

Tres rutas obvias:

> 3⁄4 Viaje claro:

1. Cascada: Whisper transcribe, LLM razona sobre la transcripción. Trabaja para escenarios de habla pura. Falta para música, audio ambiental, superposición de varios altavoces, emoción.
   La traducción de la lengua inglesa en inglés es la siguiente: "La traducción de la lengua inglesa en inglés en inglés en inglés en inglés en inglés en inglés en inglés en inglés en inglés en inglés en inglés en inglés en inglés en inglés en inglés en inglés en inglés en inglés en inglés en inglés en inglés en inglés en inglés en inglés en inglés en inglés en inglés en inglés en inglés en inglés en inglés en inglés en inglés en inglés en inglés en inglés en inglés en inglés en inglés en inglés en inglés en inglés en inglés en inglés en inglés en inglés en inglés en inglés en inglés en inglés en inglés en inglés en inglés en inglés en inglés en inglés en inglés en inglés".

2. Audio-LLM de extremo a extremo: un codificador de audio alimenta los tokens de audio directamente en un LLM, saltando la transcripción. Preserva la información acústica (emoción, altavoz, entorno). Necesita nuevos datos de capacitación.
   China: 音频编码器将音频代币 直接输入 音频代码器 直接输入 音频代码器 直接输入 音频代码器 直接输入 音频代码器 直接输入 音频代码器 直接输入 音频代码器 直接输入 音频代码器 直接输入 音频代码器 音频代码器 音频代码器 音频代码器 音频代码器 音频代码器 音频代码器 音频代码器 音频代码器 音频代码器 音频代码器 音频代码器 音频代码器 音频代码器 音频代码器 音频代码器 音频代码器 音频代码器 音频代码器 音频代码器 音频代码器 音频代码器 音频代码器 音频代码器 音频代码器 音频代码器 音频代码器 音频代码器 音频代码器 音频代码器 音频代码器 音频代码器 音频代码器 音音音 音音音音音代码器 音音代码器 音音音代码器 音代码器 音代码器 音音音代码器 音音代码器 音代码器 音音代码器 音代码器 音代码器 音音代码器 音代码器 音代码器 音代码器 音代码器 音代码器 音代码器 音代码器 音代码器 音代码器 音代码器 音代码器 音代码器 音代码器 音代码器 音代码器 音代码器 音代码器 音代码器 音代码器 音代码器 音代码器 音代码器 音代码器 音代码器 音代码器 音代码器 音代码器 音代码器 音代码器 音代代

3. El código de audio + decodificador de texto que puede transcribir y razonar.
   En el caso de los grupos de la lengua inglesa, el nombre de la lengua inglesa es "Codex".

## El concepto central.

> **【中文解读】**语音语言模型从Whisper(OpenAI's语音识别模型) hasta la evolución de AudioFlamingo. 语音语言模型从Whisper (en inglés) 语音识别模型从OpenAI的语音识别模型到AudioFlamingo的演技. 语音语言模型从Whisper (en inglés) 语音识别模型到AudioFlamingo的演技. 语音语言识别模型从Whisper (en inglés) 语音识别模型从OpenAI的语音识别模型到AudioFlamingo的演技. 语音识别模型从Whisper (en inglés) 语音识别模型从Whisper (en inglés) 语音识别模型到AudioFlamingo (en inglés) 语音识别模型从Whisper (en inglés) 语音识别模型到AudioFlamingo (en inglés) 语音识别模型从Whisper (en inglés) 语音识别模型到AudioFlamingo (en inglés) 语音识别模型到AudioFlamingo (en inglés) 语音识别模型的演技.

> **【拓展：语音 AI 的前沿**Whisper-large-v3 支持约100种语言的语音识别──2024-2025年的趋势是语音大模型:GPT-4o 原生语音输入输出(延迟约 320ms),Gemini的实时语音对话,ElevenLabs的语音克隆──AudioFlamingo en su misión de comprensión de la frecuencia de sonido alcanza SOTA, puede responder a los problemas complejos de música y sonido──


### Espectograma de registro-Mel: la característica de entrada

Cada codificador de audio comienza con la misma característica: un espectrograma log-Mel.

> Cada unidad de audio está basada en el mismo rasgo.

1. Reparación a 16 kHz.
   Traducción:重采样至16 kHz.
2. La transformación de Fourier de corto tiempo con ventanas de 25 ms, salto de 10 ms.
   China 短时里叶变换, 25 ms 窗口,10 ms 步长。
3. Tomemos la magnitud del resultado de FFT.
   En la actualidad, el número de personas que han recibido el premio es de aproximadamente un millón de personas.
4. Aplicar bancos de filtros Mel (normalmente 80 filtros con espacio de registro de 0-8000 Hz) para warp a la frecuencia perceptiva.
   La aplicación de los dispositivos de reflexión de la luz es de 80 个波器, a intervalos de 0-8000 Hz.
5. Compreso de registro (log(1 + x)) para el rango dinámico.
   En inglés, el nombre de la persona que se encuentra en el área de trabajo es el nombre de la persona que se encuentra en el área de trabajo.

Resultado: una matriz 2D de forma (T, 80) donde T es el número de marcos de tiempo. Para un clip de 30 segundos a 100 Hz: (3000, 80).

> 结果:形状为 (T, 80) de 2D 数组, de los cuales T es tiempo数──30 秒片段在 100 Hz 率下:(3000, 80)──

### El codificador de Whisper

El codificador de Whisper es un transformador de estilo ViT de 12 capas que procesa el espectrograma log-Mel como una secuencia de marcos de tiempo.

> Whisper's编码器 es un transformador de 12 niveles ViT 风格, que se realizará como el tiempo 序列处理──输出: cada tiempo 一个隐藏状态向量──

Para ASR, el decodificador de Whisper es un transformador de atención cruzada que genera tokens de texto condicionados a la salida del codificador.

> Para ASR, el descifrador de susurros es un transformador de atención de un modo que se basa en el código de código de un código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de

Para los ALM (audio-LLM), se desea que el codificador sea ingresado a un LLM diferente. El patrón: codificador de susurros congelado, Q-former trainable, LLM congelado o sintonizado.

> 对于ALM(音频LLM),需要将编码器输出作为另一个LLM的输入──模式:Whisper 编码器结,Q-former 可训练,LLM 结或微调──

### Los sistemas de codificación de audio específicos

Whisper fue entrenado en datos dominantes del habla. Es más débil para la música y el audio ambiental.

> El susurro en los datos de la voz dominada entraña.

BEATs (Chen et al., 2022) es un transformador auto supervisado entrenado en AudioSet. Captura música y sonidos ambientales mejor que Whisper en el mismo conteo de parámetros.

> BEATs(Chen 等人,2022) fue entrenado en AudioSet 上 訓練的自监督 Transformer──在相同参数下比 Whisper 更好地捕捉音乐和环境声──

AF-Whisper (híbrido de Audio Flamingo 3): Whisper + BEATs se presenta como la entrada de audio.

> AF-Whisper(Audio Flamingo 3 的混合方案):拼音 Whisper + BEATs 特征作为音频输入──Whisper 携带语言信号,BEATs 携带声学信号──

### Audio Q-former

El mismo patrón que el Q-former visual de BLIP-2. un número fijo de consultas de aprendizaje (a menudo 32 o 64) se cruzan sobre los marcos de salida del codificador de audio.

> Con el BLIP-2 de la visión Q-ex similar a la modelo.

Estadio de alineación de formación: Q-former solo, pérdidas de contraste + subtítulos en pares de audio-texto (AudioCaps, Clotho).

> 训练对齐阶段:仅 Q-former,音频-文本对上对比+描述损失(AudioCaps、Clotho) 』 instrucción阶段:端到端,解 LLM,在指令数据上训练──

### El arco  SALMONN, Qwen-Audio, AF3

SALMONN (Tang et al., 2023): Whisper + BEATs + Q-former + LLaMA. El primer LLM de audio abierto con capacidad de razonamiento serio.

> SALMONN(Tang 等人,2023):Susurro + BEATs + Q-ex + LLaMA。

Qwen-Audio (Chu et al., 2023): arquitectura similar, entrenada en un conjunto de datos más rico, sintonizada para el diálogo de múltiples giros. MMAU ~ 0.60.

> Qwen-Audio(Chu 等人,2023): similar arquitectura, en más rico de datos en el entrenamiento, para el diálogo de varias rondas optimización.

LTU  Escucha, piensa, entienda (Gong et al., 2023): datos de razonamiento explícito, enfoque en la cadena de pensamiento sobre los clips de audio.

> LTU听、想、理解(Gong 等人,2023): datos de reflexión de forma clara, enfocados en la cadena de reflexión en los segmentos de la serie de audio.

Audio Flamingo 3 (Goel et al., julio 2025): la SOTA abierta actual. 8B LLM backbone (Qwen2 7B), Whisper-large encoder concat BEATs, 64-query Q-former, entrenamiento en 1M + pares de instrucción de audio-texto. MMAU 0.72, coincide con la frontera patentada en algunas subtareas.

> Audio Flamingo 3(Goel 等人,2025年7月):当前开放 SOTA──8B LLM 主干(Qwen2 7B),Whisper-large 编码器拼接 BEATs,64 查询 Q-former,在100万+音频-文本指令对上训练──MMAU 0.72,在某些子任务上匹配闭源前沿──

AF3 también introduce una cadena de pensamiento a pedido para el audio: el modelo puede emitir tokens de pensamiento opcionalmente ("permítanme identificar los instrumentos primero: ...") antes de la respuesta final.

> AF3 también introdujo la cadena de pensamiento de audio en demanda: el modelo puede ser utilizado en la respuesta final de la pregunta previa a la elección para producir un token de pensamiento.

### Cascada vs extremo a extremo

El gasoducto en cascada:

> 级联管道:

1. Whisper transcribe audio → texto.
   Sinopsis: El libro de la película se ha convertido en un libro de historias.
2. Razones de LLM sobre texto.
   En inglés, el texto se puede traducir en inglés.

Funciona perfectamente para "resumir este podcast". No funciona para:
- "¿Qué humor tiene esta canción?"  El humor está en el sonido, no en las palabras.
- "¿Quién está hablando, Alice o Bob?"  requiere la identificación del hablante.
- "¿A qué momento ocurre la explosión?"  Terreno temporal perdido en el texto.
- "Es este audio real o generado?"  La detección de deepfake necesita características acústicas.

> Para "总结这个播客" perfectamente se aplica... pero en los siguientes escenarios fracaso:
> - "¿Qué es el sentimiento de esta canción?"
> - "¿Quién está hablando, Alice o Bob?"
> - ¿Explosión en los segundos?
> - "¿Es verdadero o es generado?"

El Qwen-Audio y el AF3 manejan la música, el ambiente y las emociones de forma nativa.

> 端到端保留了声学信号──Qwen-Audio 和 AF3 原生处理音乐、环境和情绪──

> **【中文解读】**级联管道 (Whisper 转录→LLM 推理) se adapta a la pura escena de voz como resumen de un programa, pero no puede procesar la música, el tiempo de identificación, la detección de falsificaciones y otros requisitos de la voz.

> **【拓展：金融场景的音频理解】**En el ámbito financiero, el entendimiento de audio se puede utilizar en: análisis de emociones de las reuniones de finanzas, no sólo en el transcribido de textos, sino también en el lenguaje y la comunicación de los intercambiadores, reconocimiento de órdenes de voz de los operadores, control de calidad de los clientes, análisis de emociones, análisis de conversaciones de las reuniones, separación de personas, etc.

### Recepta de producción 2026

Para un nuevo producto de audio-comprensión:

> 对于新音频理解产品:

- Cascada si: la transcripción es el objetivo, no hay música, no hay inferencia emocional.
  Si el objetivo es la traducción, no hay música, no hay necesidad de un sentimiento de conclusión.
- AF3 / Qwen-Audio-familia si: música, emoción, multi- altavoz, o razonamiento de audio complejo.
  La serie de audio de Qwen-Audio: If there is music、情绪、多人说话或复杂音频推理──

Cascada es más barata y sencilla.

> 级联更便宜更简单――端到端更强大――

### MMAU  el punto de referencia de razonamiento de audio

MMAU (Entendición de Audio Multimodal masivo) es el punto de referencia de razonamiento de audio 2024-2025.

> MMAU (en inglés: MMAU) es el programa de audiencia de 2024-2025.

- 10.000 pares de audio-texto de calidad a través del habla, la música, los sonidos ambientales.
  Traducción: 10.000 个跨语音、音乐、环境声的音频-文本 QA 对──
- Abarca la clasificación, el razonamiento temporal, el razonamiento causal, la evaluación de calidad sin límite.
  En inglés, el tiempo es el tiempo de la evolución de la evolución.
- Prueba qué oleoductos en cascada se pierden sistemáticamente.
  En inglés, el contenido de la prueba es el siguiente:

Open SOTA (AF3) en 0,72; frontera patentada ~ 0,78 (Gemini 2.5 Pro, Claude Opus 4.7). La brecha es menor que el delta abierto versus cerrado de VideoMME, lo que indica que los audio-LLM están madurando.

> 开源 SOTA(AF3) 0.72;闭源前沿约0.78(Gemini 2.5 Pro、Claude Opus 4.7)。差距小于VideoMME 的开源-闭源差距,说明音频 LLM 正在成熟──

## Usalo con el marco de ejecución
```figure
audio-text-ctc
```

## Usalo

`code/main.py`¿Qué es esto ?

- Implementa el cálculo de espectrogramas de log-Mel en stdlib: ventana, DFT ingenuo, banco de filtros de Mel.
  En el caso de los sistemas de registro de datos, el sistema de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de
- Audio Q-ex esqueleto: dado los marcos de salida del codificador, calcular Q, K, V, atención, y emitir N tokens.
  China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China: China:
- Comparación cascada contra extremo a extremo en una tarea de juguete.
  En la actualidad, el sistema de juego está en el mismo nivel que el sistema de juego.

## Envíe el producto .

Esta lección produce`outputs/skill-audio-llm-pipeline-picker.md`. Dado una tarea de audio (transcripción, etiquetado musical, inferencia de emociones, diarización de varios altavoces, clasificación del entorno), elige una cascada, AF3 de extremo a extremo o un híbrido.

> 本课产 出  `outputs/skill-audio-llm-pipeline-picker.md`◊ dado un determinado número de tareas de audio, esto es, la elección de un nivel de conexión, de un extremo a otro o de un esquema de mezcla.

## Los ejercicios.

1. Compute la dimensión del espectrograma log-Mel para un clip de 30 segundos a 16 kHz, ventana de 25 ms, salto de 10 ms, 80 barras de Mel. ¿Cómo cambia esto a 48 kHz? 计算 30 秒音频在 16 kHz、25ms 窗口、10ms 步长、80 Mel 频段下 log-Mel 频谱图维度、48 kHz 时如何变化?

2. ¿Por qué Whisper tiene un rendimiento inferior en la música? ¿Qué características de audio captura el BEAT que Whisper no tiene? ¿Por qué Whisper no se desempeña bien en la música?

3. Audio Q-former con 64 consultas vs 32: ¿En qué complejidad de tarea 64 paga? 32 guardar computación para qué? 64  consulta vs 32  consulta de Audio Q-former: en qué tarea de complejidad bajo 64 更值得? 32 节省了什么计算?

4. Lea la sección 4 de AF3 sobre pensamiento bajo demanda. Propón tres tareas de audio en las que la cadena de pensamiento ayuda más.

5. Implementar una tubería de diarización mínima utilizando la salida de AF3. ¿Cómo se señalan los cambios de altavoz?

## Términos clave .

| Term | What people say | What it actually means | 中文释义 |
|------|-----------------|------------------------|---------|
| Log-Mel spectrogram | "Mel features" Mel 频谱 | 2D (time, frequency) array of log-magnitude values after Mel filter banks 经 Mel 滤波器组后的对数幅度二维数组 | |
| Audio Q-former | "Audio Perceiver" 音频感知器 | Cross-attention bottleneck from audio encoder output to fixed-length queries feeding the LLM 音频编码器输出到固定长度查询的交叉注意力瓶颈 | |
| Cascaded | "ASR-then-LLM" 级联管道 | Pipeline where Whisper transcribes and a text LLM reasons; loses acoustic information Whisper 转录后文本 LLM 推理的管道；丢失声学信息 | |
| End-to-end | "Audio-LLM" 端到端音频 LLM | Audio features enter the LLM directly via Q-former; preserves acoustic signal 音频特征通过 Q-former 直接进入 LLM；保留声学信号 | |
| BEATs | "Audio AudioSet encoder" 音频自监督编码器 | SSL transformer trained on AudioSet; strong on music + environmental sounds 在 AudioSet 上训练的自监督 Transformer；擅长音乐和环境声 | |
| MMAU | "Audio reasoning bench" 音频推理基准 | 10k QA pairs across speech, music, environment; 2024 eval standard 跨语音、音乐、环境的 1 万条 QA；2024 年评估标准 | |
| On-demand thinking | "Audio CoT" 按需音频思考 | Model can optionally emit reasoning tokens before final answer, lifts accuracy 3-5 pts 模型可在最终回答前输出推理 token，提升准确率 3-5 个百分点 | |

## Más Leer más Leer más

- [Radford et al. — Whisper (arXiv:2212.04356)](https://arxiv.org/abs/2212.04356)
- [Chu et al. — Qwen-Audio (arXiv:2311.07919)](https://arxiv.org/abs/2311.07919)
- [Goel et al. — Audio Flamingo 3 (arXiv:2507.08128)](https://arxiv.org/abs/2507.08128)
- [Tang et al. — SALMONN (arXiv:2310.13289)](https://arxiv.org/abs/2310.13289)
- [Gong et al. — LTU (arXiv:2305.10790)](https://arxiv.org/abs/2305.10790)
