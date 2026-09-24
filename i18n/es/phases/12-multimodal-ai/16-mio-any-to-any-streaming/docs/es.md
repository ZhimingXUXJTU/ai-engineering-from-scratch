# MIO y cualquier-a-cualquier streaming de modelos multimodal.

> GPT-4o envía un producto que los modelos más abiertos no pueden replicar: un agente que escucha voz, ve video y habla en tiempo real. La respuesta del ecosistema abierto para finales de 2024 fue MIO (Wang et al., septiembre 2024). MIO tokeniza texto, imagen, habla y música, entrena a un transformador causal sobre las secuencias entrelazadas y genera cualquier modalidad a cualquier modalidad. AnyGPT (Zhan et al., febrero 2024) fue la prueba del concepto; MIO es la escalada; Unified-IO 2 (Allen AI, diciembre 2023) es el primo con visión + acción de tierra. Esta lección lee el patrón de cualquier a cualquier  cuatro tokenizers, un transformador, decodificación amigable para streaming.

> **【中文解读】**GPT-4o  muestra un sorprendente modelo de producto: un agente capaz de escuchar, ver, hacer realidad el proceso de traducción de los idiomas. La comunidad abierta sólo tiene MIO hasta finales de 2024 para este programa.

**Type:** Learn | **类型:** 学习
**Languages:** Python (stdlib, four-modality token allocator + streaming decode loop) | **语言:** Python（标准库，四模态 token 分配器 + 流式解码循环）
**Prerequisites:** Phase 12 · 11 (Chameleon), Phase 6 (Speech and Audio) | **前置知识:** Phase 12 · 11（Chameleon），Phase 6（语音与音频）
**Time:** ~120 minutes | **时间:** ~120 分钟

> ¿ Qué es esto ?**【前置】**学本节前请先掌握:Fase 12·11(Chameleon 早期融合 token 思路)、Fase 6·01-03(语音/音频 tokenizer:SpeechTokenizer、EnCodec)、Fase 8(VQ-VAE) ・・・MIO = 把Chameleon 思路扩展到4种模态(文本+图像+语音+音乐) ・・・
> ¿ Qué es esto ?**【类比】**MIO = "万能翻译耳机"──其他多模态系统 = 一堆翻译器接力(视觉翻译→文本→语音翻译→音频), cada salto de retraso+ pérdida de información; MIO = un cerebro simultáneamente escucha、看、 decir, como GPT-4o 那样端到端低延迟── el reto es que cada tipo de modelos deben ser tokenizados, y los tokens no pueden entrar en conflicto entre sí──

## Objetivos de aprendizaje

- Diseñe un vocabulario compartido que albergue textos, imágenes, voz y fichas de música sin colisiones.
  En el contexto de la historia, el lenguaje de la lengua se ha convertido en lenguaje de la lengua.
- Comparar SEED-Tokenizer (imágenes) y SpeechTokenizer residual-VQ (habla) en compresión + reconstrucción trade-offs.
  Se trata de un sistema de control de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de
- Explica el plan de estudios de cuatro etapas que construye a cualquier generación.
  Traducción:Explanar la construcción arbitraria a la generación arbitraria de cuatro fases de curso de aprendizaje.
- Nombrar las tres recetas abiertas a cualquier persona y sus principales compensaciones: MIO, AnyGPT, Unified-IO 2.
  En el caso de los sistemas de control de datos, el sistema de control de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de

## El problema es la introducción del problema

Un modelo multimodal unificado es fácil de reclamar y difícil de construir a escala. La mayoría de los sistemas "de cualquier a cualquier" hasta 2024 fueron enducidos: modelo de visión → representación de texto → modelo de habla → audio. Cada espera pierde información, agrega latencia y complica el entrenamiento.

> 统一多模态模型易声称但难以大规模构建――2024 años antes la mayoría de los sistemas "任意到任意" eran tubular: modelos de visión→文本表示→语音模型→音频――每跳都会丢失信息、增加延迟、复杂化训练――GPT-4o muestra un video de demostración que muestra un modelo único sustitutivo, el tiempo de respuesta en segundo grado inferior; el sistema abierto se retrasa varios meses―

> **【中文解读】**El mayor reto del sistema de múltiples modelos es no poder volver a usar las líneas de los sistemas de los sistemas de los sistemas de los sistemas de los sistemas de los sistemas de los sistemas de los sistemas de los sistemas de los sistemas de los sistemas de los sistemas de los sistemas de los sistemas de los sistemas de los sistemas de los sistemas de los sistemas de los sistemas de los sistemas de los sistemas de los sistemas de los sistemas de los sistemas de los sistemas de los sistemas de los sistemas de los sistemas de los sistemas de los sistemas de los sistemas de los sistemas de los sistemas de los sistemas de los sistemas de los sistemas de los sistemas de los sistemas de los sistemas de los sistemas de los sistemas de los sistemas de los sistemas de los sistemas de los sistemas de los sistemas de los sistemas de los sistemas de los sistemas de los sistemas de los sistemas de los sistemas de los sistemas de los sistemas de los sistemas de los sistemas de los sistemas de los sistemas de los sistemas de los sistemas de los sistemas de los sistemas de los sistemas de los sistemas de los sistemas de los sistemas de los sistemas de los sistemas de los sistemas de los sistemas de los sistemas de los sistemas de los sistemas de los sistemas de los sistemas de los sistemas de los sistemas de los sistemas de los sistemas de los sistemas de los sistemas de los sistemas de los sistemas de los sistemas de los sistemas de los sistemas de los sistemas de los sistemas de los sistemas de los sistemas de los sistemas de los sistemas de los sistemas de los sistemas de los sistemas de los sistemas de los sistemas de los sistemas de los sistemas de los sistemas de los sistemas de los sistemas de los sistemas de los sistemas de los sistemas de los sistemas de los sistemas de los sistemas de los sistemas de los sistemas de los sistemas de los sistemas de los sistemas de los sistemas de los sistemas de los sistemas de los sistemas de los sistemas de los sistemas de los sistemas de los sistemas de los sistemas de los sistemas de los sistemas de los sistemas de los sistemas de los sistemas de los sistemas de los cuales se pueden utilizar los sistemas de los sistemas de los sistemas de los sistemas de los sistemas de los sistemas de los sistemas de los sistemas de los sistemas de los cuales se pueden utilizar.

Los retos de ingeniería:

> 工程挑战:

- Los tokenizers deben existir para cada modalidad, comprimir sin pérdidas - lo suficiente para la reconstrucción, y producir tokens a las tasas que el transformador puede consumir.
  Cada tipo de modelo tiene que tener un separador, comprimir el perdimiento lo suficiente para reconstruir, y generar un token con la velocidad de transformación.
- Un vocabulario único debe asignar espacio para texto (32k+), imagen (16k+), habla (4k+), música (8k+).
  En el texto original, el texto se basa en el texto de la traducción de la lengua inglesa.
- Los datos de formación deben cubrir cada par de entradas y salidas (texto→imagen, imagen→habla, habla→imagen, etc.) o el modelo debe componerse.
  En el texto chino, el formato de la información debe ser el siguiente:
- La inferencia debe transmitir tokens de salida lo suficientemente rápido como para la latencia de conversación (<500ms tiempo-a-primero-byte de audio).
  Traducción:El argumento debe ser emitido con una velocidad suficiente para satisfacer el retraso del diálogo.

## El concepto central.

> **【中文解读】**MIO 实现 arbitrario a arbitrario de múltiples modos de procesamiento: entre texto, imágenes, audio, vídeo puede combinarse arbitrariamente entre entrada y salida.

> **【拓展：全模态模型的趋势】**La tendencia del 2025 es que el modelo de visión+ lenguaje se desplace hacia el modelo completo: GPT-4o Original Supporting语音输入输出, Gemini 支持视频实时流, Meta's Spirit LM 统一语音和文本。 El modelo completo necesita solucionar el problema central de diferentes modelos de densidad de información diferencias1 segundos de vídeo alrededor de 30 1, segundos de voz alrededor de 16K muestras, necesita alta eficiencia compresión。


### Cuatro tokenizers para cuatro modalidades

La pila de tokenizadores de MIO:

> **【中文解读】**MIO para cuatro modelos de diferentes distribuciones de un tokenizer especial, los tokens de salida están mapeados a un código de identificación de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código

- Texto: BPE estándar, vocabulario ~32000.
  El texto original de la traducción de la palabra BPE, en inglés, se traduce en "BPE estándar".
- Imagen: SEED-Tokenizer (2023)  VAE cuantizado con libro de código discreto, 4096 entradas, 32x32 tokens por imagen.
  En el año 2023, el nombre de los tokenizadores se ha convertido en el nombre de los tokenizadores.
- Habla: SpeechTokenizer residual-VQ (2023)  codifica la forma de onda de 16 kHz en 8 libros de código jerárquicos; el primer nivel es contenido grueso, los niveles posteriores añaden prosodia e identidad del altavoz.
  La versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión de la versión original de la versión de la versión original de la versión de la versión original de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de 16 de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de 20 de la versión de la versión de 20 de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de 20 de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión
- Música: VQ residual similar (familia MusicGen / Encodec de Meta), 4-8 libros de código.
  La música es un tema muy importante para la música.

Cada modalidad produce tokens de números enteros. Los tokens obtienen rangos de ID desarticulados en el vocabulario compartido:

> Cada tipo de modo genera un número total de tokens.

```
text:   0..31999
image:  32000..36095  (4096 image tokens)
speech: 36096..40191  (4096 speech base tokens, plus residual layers)
music:  40192..48383  (8192 music tokens)
sep:    48384..48390  (<image>, <speech>, <music>, </...>, etc.)
```

Total: ~ 48k vocabulario. La entrada de inserción y la proyección de salida abarcan todo ello.

> 总计约 48k 词汇量──输入嵌入和输出投影覆盖全部词汇──

### Descódigo de transmisión

La generación de voz utiliza residual-VQ. El transformador predice las fichas de voz de base (capas 0); un cuantificador residual decodificado en paralelo predice las capas posteriores. Cada token de capas 0 es aproximadamente 50 ms de audio a 16 kHz.

> 语音生成使用残差 VQ──Transformer 预测基础层(第0层)语音代币;并行解码的残差量化器预测后续层──每一层代币 大约对应 16kHz 下的50ms 音频──

> **【中文解读】**El clave de la secuencia de código es la secuencia de procesamiento: Transformer 预测语音基础层代币,残差量化器并行预测后层── cada secuencia de código tiene una secuencia de 50ms 音频── toda la cadena desde el aire hasta la primera secuencia de audio produce unos 300-500ms, cerca de los 250ms de GPT-4o.

El patrón de transmisión:

> 流式模式:

1. El usuario habla en el micrófono; el tokenizer de audio en tiempo real emite tokens de voz cada 50 ms.
   Traducción: usuario se dirige a un dispositivo de comunicación de 50 ms.
2. MIO consume tokens a su llegada (precarga inmediata + adelanto incremental).
   En inglés, el nombre de la moneda se traduce en inglés como "MIO" en inglés.
3. Los tokens de salida se transmiten como generados; un decodificador de voz paralelo los convierte en muestras de audio con ~50-150ms de latencia.
   En la actualidad, el sistema de resolución de los voces de la lengua se ha convertido en un sistema de resolución de voces de la lengua en 50-150 ms.
4. Tiempo a primer byte de audio: ~300-500 ms en papel MIO, acercándose a ~250 ms de GPT-4o.
   La versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión de la versión original de la versión de la versión de la versión de la versión original de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de

Mini-Omni (arXiv:2408.16725), GLM-4-Voice (arXiv:2412.02612), y Moshi (arXiv:2410.00037) son diseños complementarios de transmisión de voz-LLM. Moshi en particular logra 160ms de ida y vuelta en una sola GPU.

> Mini-Omni、GLM-4-Voice 和 Moshi es el diseño de LLM en lenguaje de forma complementaria.

### Currículo de cuatro etapas

Programa de formación del MIO:

> Programa de entrenamiento de la MIO:

1. Estadio 1  Alineación. Corporación de pareja de modalidad a gran escala: imagen de texto, discurso de texto, música de texto. Cada pareja utiliza su propio segmento de vocabulario token. Entrena el vocabulario compartido.
   La lengua de la lengua se utiliza para el uso de la lengua en la lengua de la lengua.
2. Esta etapa 2  interconectado. Documentación interconectada de múltiples modalidades (blogs con imágenes + video, podcasts con transcripciones, etc.).
   La formación de la formación de la formación de la formación de la formación de la formación de la formación de la formación de la formación de la formación de la formación de la formación de la formación de la formación de la formación de la formación de la formación de la formación de la formación de la formación de la formación de la formación de la formación de la formación de la formación de la formación de la formación de la formación de la formación de la formación de la formación de la formación de la formación de la formación de la formación de la formación de la formación de la formación de la formación de la formación de la formación de la formación de la formación de la formación de la formación de la formación de la formación de la formación de la formación de la formación de la formación de la formación de la formación de la formación de la formación de la formación de la formación de la formación de la formación de la formación de la formación de la formación de la formación de la formación de la formación de la formación de la formación de la formación de la formación de la formación de la formación de la formación de la formación de la formación de la formación de la formación de la formación de la formación de la formación de la formación de la formación de la formación de la formación de la formación de la formación de la formación en la formación de la formación de la formación de la formación de la formación de la formación en la formación de la formación de la formación de la formación en la formación de la formación en la formación de la formación en la formación de la formación de la formación en la formación de la formación en la formación en la formación de la formación en la formación de la formación de la formación en la formación en la formación en la formación en la formación de la formación en la formación de la formación de la formación en la formación en la formación en la formación de la formación en la formación en la formación de la formación en la formación en la formación en la formación en la formación en la formación en la formación en la formación en la formación en la formación en la formación en la formación en la formación en la formación en la formación en la formación en la formación en la formación en la formación en la formación en la formación en la formación en la formación en la formación en la formación en la formación en la formación en la formación en la formación en la formación en la formación en la formación en la formación en la formación en la formación en la formación en la formación en la formación en la formación en la formación en la formación en la formación en la formación en la formación en la formación en
3. Etapa 3  mejorado con voz. Datos de audio adicionales para elevar la calidad del habla sin perder la capacidad del texto.
   China: 阶段 3  语音增强──额外音频数据提升语音质量,不损失文本能力──
4. Fase 4  FIS. La instrucción se ajusta a través de modalidades: VQA, subtítulos, narración, diálogo discurso a discurso.
   La primera de las cuatro ediciones de la serie de televisión de la serie de televisión de televisión de la televisión de la televisión de la televisión de la televisión de la televisión de la televisión de la televisión de la televisión de la televisión de la televisión de la televisión de la televisión de la televisión de la televisión de la televisión de la televisión de la televisión de la televisión de la televisión de la televisión de la televisión de la televisión de la televisión de la televisión de la televisión de la televisión de la televisión de la televisión de la televisión de la televisión de la televisión de la televisión de la televisión de la televisión de la televisión de la televisión de la televisión de la televisión de la televisión de la televisión de la televisión de la televisión de la televisión de la televisión de la televisión de la televisión de la televisión de la televisión de la televisión de la televisión de la televisión de la televisión de la televisión de la televisión de la televisión de la televisión de la televisión de la televisión de la televisión de la televisión de la televisión de la televisión de la televisión de la televisión de la televisión de la televisión de la televisión de la televisión de la televisión de la televisión de la televisión de la televisión de la televisión de la televisión de la televisión de la televisión de la televisión de la televisión de la televisión de la televisión de la televisión de la televisión de la televisión de la televisión de la televisión de la televisión de la televisión de la televisión de la televisión de la televisión de la televisión de la televisión de la televisión de la televisión de la televisión de la televisión de la televisión de la televisión de la televisión de la televisión de la televisión de la televisión de la televisión de la televisión de la televisión de la televisión de la televisión de la televisión de la televisión de la televisión de la televisión de la televisión de la televisión de la televisión de la televisión de la televisión de la televisión de la televisión de la televisión de la televisión de la televisión de la televisión de la televisión de la televisión de la televisión de la televisión de la televisión de la televisión de la televisión de la televisión de la televisión de la televisión de la televisión de la televisión de la televisión de la televisión de la televisión de la televisión de la televisión de la televisión de la televisión de la televisión de la televisión de la televisión de la televisión de la televisión de la televisión de la televisión de la televisión de la televisión de la televisión de la televisión de la televisión de la televisión de la televisión de la televisión de la televisión de la televisión de la televisión de la televisión de la televisión de la televisión de la televisión de la

El hecho de que no haya una etapa degrada las capacidades específicas: omitir la etapa 2 y el modelo pierde el contexto de modalidad cruzada; omitir la etapa 3 y el habla es pobre.

> 跳过某一阶段会导致特定能力退化: jump过阶段 2 模型失去跨模态上下文; jump过阶段 3 语音质量差──

> **【中文解读】**El programa de entrenamiento de cuatro fases del MIO es un proceso de formación gradual de la capacidad: 1) modelado para la formación de gráficos de gran escala, textos y parámetros de voz, 2) formación de varios tipos de texto, etc.; 3) formación de datos de voz y de alta frecuencia, 4) instrucciones para la modificación de la forma de VQA, etc.;

### La cadena del pensamiento visual

MIO introduce la cadena de pensamiento visual: el modelo emite fichas de imagen intermedias como un paso de razonamiento.

> MIO introdujo la cadena de pensamiento visual: modelo en el proceso de reflexión generando un token de imagen medio.

1. Emite`<image>`fichas que renten la escena (desde la imagen de entrada o un boceto).
   Traducción: 输出`<image>`En el caso de los niños, el número de niños en edad avanzada es de aproximadamente un millón.
2. Emite un texto analizando el boceto.
   Traducción: 输出文本分析草图.
3. Emite la respuesta final.
   Traducción:Enlace final.

La imagen intermedia que se hace servir de raspad. Los puntos de referencia mejoran las tareas de razonamiento espacial. La idea refleja la cadena de pensamiento para el razonamiento de texto.

> 染的中间图像充当草稿板──在空间推理任务上基准测试有所改善──这个思路映射了文本推理中的思维链──

> **【拓展：视觉思维链的应用前景】**En el ámbito financiero, esta técnica se puede utilizar para el análisis de gráficos complejos: en el campo de la máquina, el modelo VLA puede utilizarse primero para planificar y ejecutar los caminos de la visión.

### Los competidores en cualquier

- AnyGPT (arXiv:2402.12226): 4 modalidades (texto, imagen, habla, música), diseño similar.
  En el caso de los grupos de la música, el nombre de la música es "Creo que la música es una forma de música".
- Unified-IO 2 (arXiv:2312.17172): añade resultados de acción de visión, profundidad, normales. Más diversidad de tareas, menor escala.
  China:Unified-IO 2: Add加视觉动作输出、深度、法线──任务更多样,规模更小──
- NExT-GPT (arXiv:2309.05519): LLM + decodificadores de difusión específicos de modalidad. No es un enfoque de modelo único.
  En el caso de los sistemas de gestión de los sistemas de gestión de datos, el sistema de gestión de los sistemas de gestión de datos de datos de los sistemas de gestión de datos de datos de los sistemas de gestión de datos de datos de los sistemas de gestión de datos de datos de los sistemas de gestión de datos de datos de los sistemas de gestión de datos de datos de los sistemas de gestión de datos de datos de datos de los sistemas de gestión de datos de datos de datos de datos de datos de los sistemas de gestión de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de
- CoDi (arXiv:2305.11846): difusión composible; cualquiera a cualquiera a través de latencia compartida.
  En el contexto de la actualidad, el sistema de distribución de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos

MIO es el más cercano a la señal pura de cualquier-a-algo. AnyGPT es su antepasado conceptual.

> MIO, más cercano a la pura señal de arbitrario a arbitrario.

### Presupuesto de la latencia

Para un producto de conversación, la latencia de cada componente importa:

> Para los productos de diálogo, el retraso de cada componente es importante:

- Micrófono a tokens de audio: ~ 50 ms.
  En inglés, el tiempo de la transmisión de la voz es de 50 ms.
- Preemplaje (tokens de audio + historial): ~ 100 ms en un modelo 8B.
  En inglés, el nombre de la fuente de la información es "Special" (en inglés, "Special") (en inglés, "Special") (en inglés, "Special") (en inglés, "Special") (en inglés, "Special") (en inglés, "Special") (en inglés, "Special") (en inglés, "Special") (en inglés, "Special") (en inglés, "Special") (en inglés, "Special") (en inglés, "Special") (en inglés, "Special") (en inglés, "Special) (en inglés, "Special) " (en inglés, "Special) " (en inglés, "Special) " (en inglés, "Special) " (en inglés, "Special) " (en inglés, "Special) " (en inglés, "Special) " (en inglés, "Special) " (en inglés, "Special) " (en inglés, "Special) " (en inglés) " (en inglés) " (en inglés) " (en inglés) " (en inglés) " " " " " " (en inglés) " " " (en inglés) " " " (en inglés) " " " " (en inglés) "
- El primer token de salida: ~ 50ms.
  En inglés, el primer token de salida es de 50 ms.
- Descóder de voz paralelo residual-VQ + ~ 100-150 ms.
  China: 并行残差 VQ + 语音解码器: alrededor de 100-150ms。

El tiempo total de audio-primero-byte: ~300ms mínimo. GPT-4o afirma ~250ms. Moshi afirma 160ms. MIO / AnyGPT están en el rango de 400-600ms por puntos de referencia públicos.

> 首音频字节时间总计至少约300ms──GPT-4o 声称约250ms──Moshi 声称160ms──MIO/AnyGPT 在公开基准测试中约400-600ms──

> **【中文解读】**Sobre el presupuesto de la producción:麦克风→语音代币(~50ms)→ 预填充(~100ms)→ 首个输出代币(~50ms)→ 残差 VQ + 语音解码(~100-150ms)。总计 TTFAB 约300ms 起──GPT-4o 约250ms,Moshi 仅160ms(单 GPU 上最快的开源方案)。

### ¿Por qué cualquiera a cualquiera se mantiene duro

Incluso en 2026, los modelos abiertos a cualquier modelo siguen a los cerrados en dos ejes:

> Incluso en 2026, el modelo libre de arbitrariedad en dos dimensiones sigue quedando atrás en el modelo de origen cerrado:

- La calidad del habla. El tokenizador residual-VQ es perdedor; el habla conversacional suena robótica en comparación con las voces de la clase ElevenLabs.
  En el caso de los elevenLabs, el diálogo se produce en el mismo modo que los elevenLabs.
- El razonamiento de modalidad cruzada. "Cantar sobre lo que ves" sigue fracasando más a menudo que las tareas de visión pura.
  La traducción del lenguaje chino es "transformar" y "transformar" en lenguaje chino.

Estos son problemas de investigación abiertos. Qwen3-Omni (Lección 12.20) es el intento abierto más avanzado en 2025.

> Estos son problemas de investigación abiertos.

## Usalo con el marco de ejecución
```figure
any-to-any-stream
```

## Usalo

`code/main.py`¿Qué es esto ?

> `code/main.py`¿Qué es esto ?

- Define la asignación de vocabulario de cuatro modalidades y lo imprime.
  La traducción del idioma chino es: define cuatro modalidades de distribución y impresión.
- Envía una lista de entradas multimodal (texto, imagen, audio, música) a través del router del tokenizer.
  En el texto original, el texto se traduce por "la lengua de los idiomas" (en inglés: "la lengua de los idiomas").
- Simula el decodificación de transmisión para una respuesta de texto a voz con recuento de latencia.
  El texto de la traducción de la lengua china se traduce en inglés como "la lengua de los idiomas de la lengua china".
- Computa el tiempo esperado de primer byte de audio dado en codificador, preempleo y latencias de decodificador.
  Según el codificador, preempleo y el codificador, la fecha de inicio de la sesión es el tiempo de inicio de la sesión.

## Envíe el producto .

Esta lección produce`outputs/skill-any-to-any-pipeline-auditor.md`. Dado un producto de conversación (modalidades de entrada, modalidades de salida, objetivo de latencia), audita las opciones de diseño de la familia MIO y calcula el presupuesto de latencia.

> 本课产 出  `outputs/skill-any-to-any-pipeline-auditor.md`◊ a la hora de determinar los productos de la serie MIO, la auditoría de la selección de diseño y el cálculo de la demora presupuestaria.

## Los ejercicios.

1. Su producto acepta la entrada de voz y devuelve la salida de voz. ¿Cuál es el objetivo del presupuesto de latencia de extremo a extremo?

2. El speechtokenizer residual-VQ utiliza 8 libros de código. Proponga por qué es necesario decodificar los niveles residuales en paralelo (vs secuencial) y qué ahorros de latencia trae.

3. Su vocabulario tiene 32k texto + 4k imagen + 4k habla. Agregue 8k música y ~10 separadores. ¿Cuál es el costo del parámetro de matrices de incorporación en dim 4096 oculto?

4. La cadena de pensamiento visual emite una imagen intermedia. ¿Qué tipos de preguntas benefician? ¿Qué tipos son perjudicados por los tokens adicionales?

5. Leer Moshi (arXiv:2410.00037). Describir su técnica de "monólogo interno" y comparar con la cadena de pensamiento visual de MIO.

## Términos clave .

| Term | What people say | What it actually means | 中文释义 |
|------|-----------------|------------------------|---------|
| Any-to-any | "Multimodal in/out" 任意模态进出 | A single model that accepts and emits text, image, speech, and music in any direction 单一模型接受并以任意方向输出文本、图像、语音、音乐 | |
| Residual-VQ | "Speech tokenizer stack" 语音分词器栈 | Multi-codebook tokenization where each layer adds information; base layer is content, later layers are prosody 多码本分词，每层添加信息；基础层是内容，后续层是韵律 | |
| SEED-Tokenizer | "Image codes" 图像编码 | Discrete image tokenizer with 4096-entry codebook used by MIO 离散图像分词器，4096 码本 | |
| Chain-of-visual-thought | "Visual scratchpad" 视觉草稿板 | The model generates an intermediate image as a reasoning step before its final answer 模型在最终回答前生成中间图像作为推理步骤 | |
| Time-to-first-audio-byte | "TTFAB" 首音频字节延迟 | Latency from user voice to first audio output; <500ms for conversational feel 用户语音到首个音频输出的延迟；<500ms 才有对话感 | |
| Four-stage curriculum | "Training recipe" 训练配方 | Alignment -> interleaved -> speech-enhanced -> SFT, in that order 对齐→交错→语音增强→指令微调的四阶段训练流程 | |

## Más Leer más Leer más

- [Wang et al. — MIO (arXiv:2409.17692)](https://arxiv.org/abs/2409.17692)
- [Zhan et al. — AnyGPT (arXiv:2402.12226)](https://arxiv.org/abs/2402.12226)
- [Lu et al. — Unified-IO 2 (arXiv:2312.17172)](https://arxiv.org/abs/2312.17172)
- [Wu et al. — NExT-GPT (arXiv:2309.05519)](https://arxiv.org/abs/2309.05519)
- [Tang et al. — CoDi (arXiv:2305.11846)](https://arxiv.org/abs/2305.11846)
