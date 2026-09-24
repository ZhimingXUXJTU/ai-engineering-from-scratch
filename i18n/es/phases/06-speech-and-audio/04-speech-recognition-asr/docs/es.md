# Reconocimiento del habla (ASR)  CTC, RNN-T, atención 语音识别  CTC、RNN-T y mecanismo de atención

> El reconocimiento del habla es una clasificación de audio en cada paso del tiempo, pegada entre sí por un modelo de secuencia que conoce el inglés y el silencio. CTC, RNN-T y atención son las tres formas de hacerlo. Elige una y entienda por qué.

> **【中文解读】**语音识别 se hace en cada paso del tiempo haciendo su频分类, reutiliza el modelo de secuencias ((知道语言和静音规律) para unirlas.

> **【拓展：ASR 的应用】**语音识别是语音助手(Siri、小爱同学) 、会议记录(飞书/钉钉实时字幕) 、视频字幕自动生成的核心──Whisper es la fuente abierta de 2026 años ASR 标杆──

**Type:** Build | **类型:** 构建
**Languages:** Python | **语言:** Python
**Prerequisites:** Phase 6 · 02 (Spectrograms & Mel), Phase 5 · 08 (CNNs & RNNs for Text), Phase 5 · 10 (Attention) | **前置知识:** 阶段 6 · 02（频谱图与 Mel），阶段 5 · 08（文本的 CNN 与 RNN），阶段 5 · 10（注意力机制）
**Time:** ~45 minutes | **预计用时:** ~45 分钟

## El problema es la introducción del problema

El problema es estructural: los marcos de audio no se alinean uno a uno con los caracteres. La palabra "okay" puede tardar 200 ms o 1200 ms. El silencio puntua la pronunciación. Algunos fonemas son más largos que otros. El número de tokens de salida no se conoce de antemano.

> Usted tiene un pasaje de 10 segundos 16 kHz de sonido. Usted quiere una cadena: "Enciende las luces de la cocina".

> **【中文解读】**La pregunta planteada en este capítulo es: ¿cómo entender y aplicar correctamente esta tecnología en la ingeniería real? Comprender el contexto de la cuestión ayuda a comprender los puntos clave de decisión del tipo de selección técnica. En los sistemas de IA reales, el tipo de selección técnica errónea suele ser más alto que el costo de error de la realización de detalles.

Tres formulaciones resuelven esto:

> Tres soluciones para resolver este problema:

1. **CTC (Connectionist Temporal Classification).**Emite probabilidades de tokens por marco incluyendo un *blanco especial*. Repeticiones de colapso y espacios en tiempo de decodificación. No autoregresivos, rápido. Usado por wav2vec 2.0, MMS.
   **CTC（连接时序分类）。**逐发射代币 概率, incluidos los especiales *blank*──解码时折重复和空白──非自归,快速──wav2vec 2.0、MMS 使用──
2. **RNN-T (Recurrent Neural Network Transducer).**La red conjunta predice el próximo token dado marco de codificación y los tokens anteriores.
   **RNN-T（递归神经网络转换器）。**联合网络根据编码器和之前的代币 预测下一个代币──可流式处理──Google 端侧 ASR、NVIDIA Parakeet 使用──
3. **Attention encoder-decoder.**El codificador comprime el audio a estados ocultos, el decodificador atende cruzando para generar tokens autoregresivamente.
   **注意力编码器-解码器。**编码器将音频压缩为隐藏状态,解码器通过交叉注意力自归归地生成代币──Whisper、SeamlessM4T 使用──

En 2026, el SOTA WER en LibriSpeech es de 1,4% (Parakeet-TDT-1.1B, NVIDIA) y 1,58% (Whisper-Large-v3-turbo). Las diferencias son pequeñas; las diferencias de despliegue son enormes.

> En el año 2026, LibriSpeech test-clean 上的 SOTA WER fue de 1.4% (Parakeet-TDT-1.1B,NVIDIA) y 1.58% (Whisper-Large-v3-turbo)

## El concepto central.

> **【中文解读】**Este capítulo presenta los conceptos y teorías básicos. La comprensión de estos conceptos es el prerrequisito de la realización posterior de la actividad, y también el conocimiento de los puntos de alta frecuencia de la entrevista y la práctica de la ingeniería.


![Three ASR formulations: CTC, RNN-T, attention-encoder-decoder](../assets/asr-formulations.svg)

**CTC intuition.**Deja que el codificador salga `T`distribuciones a nivel de marco en `V+1`Tokens (V caracteres + blanco). Para una cadena objetivo `y`de longitud `U < T`, cualquier alineación de marco que se derrumbe a`y`Contiene. CTC pérdida suma sobre todas estas alineaciones. Inferencia: por marco argmax, colapso repite, eliminar espacios en blanco.

> **CTC 直觉。**让编码器输出                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                       `T`个级分布, cada distribución cubre `V+1`个 token(V 个字符 + blanco) ⋅对于长度为 `U < T`                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             `y`, cualquier doblaje después es igual a `y`La diferencia entre los valores de la diferencia de diferencia entre los valores de la diferencia de diferencia entre los valores de la diferencia entre los valores de la diferencia entre los valores de la diferencia entre los valores de la diferencia entre los valores de la diferencia entre los valores de la diferencia entre los valores de la diferencia entre los valores de la diferencia entre los valores de la diferencia entre los valores de la diferencia entre los valores de la diferencia entre los valores de la diferencia entre los valores de la diferencia entre los valores de la diferencia entre los valores de la diferencia entre los valores de la diferencia entre los valores de la diferencia entre los valores de la diferencia entre los valores de la diferencia y la diferencia entre los valores de la diferencia entre los valores de la diferencia entre los valores de la diferencia y la diferencia entre los valores de la diferencia entre los valores de la diferencia entre los valores de la diferencia y la diferencia entre los valores de la diferencia entre los valores de la diferencia entre los valores de la diferencia entre los valores de la diferencia entre los valores de la diferencia entre los valores de la diferencia entre los valores de la diferencia entre los valores de la diferencia entre los valores de la diferencia entre los valores de la diferencia entre los valores de la diferencia entre los valores de la diferencia entre los valores de la diferencia entre los valores de la diferencia entre los valores de la diferencia entre los valores de la diferencia entre los valores de la diferencia entre los valores de la diferencia entre los valores de la diferencia entre los valores de la diferencia entre los valores de la diferencia entre los valores de la diferencia entre los valores de la diferencia entre los valores de la diferencia entre los valores de la diferencia entre los valores de la diferencia entre los valores de la diferencia entre los valores de la diferencia entre los valores de la diferencia entre los valores de la diferencia entre los valores de la diferencia de la diferencia entre los valores de la diferencia de la diferencia entre los valores de la diferencia de la diferencia de la diferencia de la diferencia entre los valores de la diferencia de la diferencia de la diferencia de la diferencia entre los valores de la diferencia de la diferencia de la diferencia de la diferencia de la diferencia de la diferencia de la diferencia de la diferencia de la diferencia de la diferencia de la diferencia de la diferencia de la diferencia de la diferencia de la diferencia de la diferencia de la diferencia de la diferencia de la diferencia de la diferencia de la diferencia de la diferencia de la diferencia de la diferencia de la diferencia de la diferencia de la diferencia de la diferencia de la diferencia de la diferencia de la diferencia de la diferencia de la diferencia de la diferencia

Ventajas: no autoregresivos, transmitibles, cero mirador. Desventaja: * suposición de independencia condicional *  cada predicción de cuadro es independiente de los demás, por lo que no hay un modelo de lenguaje interno.

> 优势:非自归、可流式处理、零前──缺点:* Condiciones independencia性假设*每预测彼此独立,因此没有内部语言模型──通过束搜索或浅融合的外部LM 来修复──

**RNN-T intuition.**Añade una red de * predictor* que incorpora el historial de los tokens y una *joiner* que combina el estado de predictor con un marco de codificación en una distribución conjunta de `V+1`(la `+1`Es una dependencia condicional que se ignora en CTC. Se puede transmitir porque cada paso solo se condiciona en marcos y tokens pasados.

> **RNN-T 直觉。**Añadir un token embedded  historio                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    `V+1`联合分布的 *joiner*(`+1`Es decir, el proceso de procesamiento de los datos de la CTC es totalmente inalterable.

Ventajas: transmisión + LM interna. Desventaja: el entrenamiento es más complejo y hambriento de memoria (3D retícula de pérdida); los núcleos de pérdida RNN-T son una categoría de biblioteca completa por sí mismos.

> 优势:可流式 + 内部 LM。缺点: entrenamiento más complejo、 más consumo de memoria(3D 损失格);RNN-T 损失核本身就是一个完整的库类──

**Attention encoder-decoder.**El codificador (6-32 capas de transformador) sobre los marcos de log-mail. El decodificador (6-32 capas de transformador) atende cruzando a las salidas de codificación para generar tokens autoregresivamente.

> **注意力编码器-解码器。**编码器(6-32 层变压器) 处理日志 ──解码器(6-32 层变压器) 通过交叉注意力自归归生成代币──无对齐约束注意力可以看向音频的任何位置──除非限制注意力(分块 微笑流,2024),否则不可流式处理──

Ventajas: la más alta calidad en ASR fuera de línea, fácil de entrenar con herramientas seq2seq estándar. Desventaja: la latencia autoregressiva es proporcional a la longitud de salida; no puede transmitirse sin ingeniería.

> 优势:离线 ASR 质量最高,使用标准seq2seq 工具易训练──缺点:自归延迟与输出长度成正比;不做工程优化无法流式处理──

### WER: el número uno

> ### WER: único indicador

**Word Error Rate**¿ Qué es esto ?`(S + D + I) / N`, donde S=substituciones, D=eliminaciones, I=inserciones, N=conto de palabras de referencia.

> **词错误率**¿ Qué es esto ?`(S + D + I) / N`, entre los cuales S= sustitución, D= eliminación, I= inserción, N= referencia palabra número。对应词级别的 Levenshtein 编辑距离──越低越好──WER 超过 20% normalmente no utilizable; inferior a 5% para el nivel humano de lectura.

| Model | LibriSpeech test-clean | LibriSpeech test-other | Size |
|-------|------------------------|------------------------|------|
| Parakeet-TDT-1.1B | 1.40% | 2.78% | 1.1B params |
| Whisper-Large-v3-turbo | 1.58% | 3.03% | 809M |
| Canary-1B Flash | 1.48% | 2.87% | 1B |
| Seamless M4T v2 | 1.7% | 3.5% | 2.3B |

| 模型 | LibriSpeech test-clean | LibriSpeech test-other | 大小 |
|------|------------------------|------------------------|------|
| Parakeet-TDT-1.1B | 1.40% | 2.78% | 11 亿参数 |
| Whisper-Large-v3-turbo | 1.58% | 3.03% | 8.09 亿 |
| Canary-1B Flash | 1.48% | 2.87% | 10 亿 |
| Seamless M4T v2 | 1.7% | 3.5% | 23 亿 |

> **【中文解读】**Este capítulo a través del código de la implementación de algoritmos centrales de cero. Este método "desde cero" puede ayudar a entender el principio detrás del marco, no se encuentra en la caja negra cuando se encuentran problemas.


Todos estos sistemas son codificadores-decodificadores o basados en RNN-T. Los sistemas de CTC puros (wav2vec 2.0) se encuentran en torno al 1,82,1% en la prueba de limpieza.

> Estos son codificadores-descodificadores o RNN-T 架构──纯 CTC 系统(wav2vec 2.0) en el test-clean 上约1.82.1%──

> **【拓展：语音 AI 的产品化】**La tecnología de voz se enfrenta a un desafío único en la productorización: diferentes voces, ruidos de contexto, remota recogida, muchos hablar, etc.

> **【拓展：多语言语音技术】**Las características de los idiomas de todo el mundo son muy diferentes: el sonido de los idiomas de todo el mundo (como el chino) es alto, el lenguaje de bajo recurso es poco capacitado.



## Construye y realiza.
```figure
ctc-collapse
```

## Construye el mismo

### Paso 1: codificación codificada por CTC

```python
def ctc_greedy(frame_logits, blank=0, vocab=None):
    # frame_logits: list of per-frame probability vectors
    preds = [max(range(len(p)), key=lambda i: p[i]) for p in frame_logits]
    out = []
    prev = -1
    for p in preds:
        if p != prev and p != blank:
            out.append(p)
        prev = p
    return "".join(vocab[i] for i in out) if vocab else out
```

Dos reglas: derrumbar repetidas consecutivas, dejar en blanco. Ejemplo: `a a _ _ a b b _ c`¿ Qué es esto ?`a a b c`¿ Qué ?

> 两条规则: plegamiento连续重复,丢弃空白── ejemplos:`a a _ _ a b b _ c`¿ Qué es esto ?`a a b c`¿Qué es eso?

### Paso 2: CTC de búsqueda de haz

```python
def ctc_beam(frame_logits, beam=8, blank=0):
    import math
    beams = [([], 0.0)]  # (tokens, log_prob)
    for p in frame_logits:
        log_p = [math.log(max(pi, 1e-10)) for pi in p]
        candidates = []
        for seq, lp in beams:
            for t, lpt in enumerate(log_p):
                new = seq[:] if t == blank else (seq + [t] if not seq or seq[-1] != t else seq)
                candidates.append((new, lp + lpt))
        candidates.sort(key=lambda x: -x[1])
        beams = candidates[:beam]
    return beams[0][0]
```

La producción utiliza búsqueda de prefijos de haces de árboles con fusión LM; este es el esqueleto conceptual.

> El uso de la luz en el ambiente de producción es un concepto de la búsqueda de rayos de árboles.

### Paso 3: WER

```python
def wer(ref, hyp):
    r, h = ref.split(), hyp.split()
    dp = [[0] * (len(h) + 1) for _ in range(len(r) + 1)]
    for i in range(len(r) + 1):
        dp[i][0] = i
    for j in range(len(h) + 1):
        dp[0][j] = j
    for i in range(1, len(r) + 1):
        for j in range(1, len(h) + 1):
            cost = 0 if r[i - 1] == h[j - 1] else 1
            dp[i][j] = min(
                dp[i - 1][j] + 1,
                dp[i][j - 1] + 1,
                dp[i - 1][j - 1] + cost,
            )
    return dp[len(r)][len(h)] / max(1, len(r))
```

### Paso 4: Inferencia contra el susurro

```python
import whisper
model = whisper.load_model("large-v3-turbo")
result = model.transcribe("clip.wav")
print(result["text"])
```

Un linear para el ASR general más fuerte en 2026.

> Una línea de código de ASR con mayor capacidad general del año 2026 se ejecuta en una GPU de 24 GB con una velocidad de 20 veces más alta en el tiempo real.

### Paso 5: transmisión con Parakeet o wav2vec 2.0

```python
from transformers import pipeline
asr = pipeline("automatic-speech-recognition", model="nvidia/parakeet-tdt-1.1b")
for chunk in streaming_audio():
    print(asr(chunk, return_timestamps=True))
```

> **【中文解读】**Este capítulo muestra cómo utilizar un marco maduro (como PyTorch、HuggingFace, etc.) para aplicar rápidamente esta tecnología. En los proyectos reales, se realiza con prioridad el uso de un marco experimentado, se pueden reducir errores y mejorar la eficiencia de desarrollo.


La transmisión de ASR requiere de la atención del codificador en pedazos y el estado de transferencia; utilice una biblioteca que lo admita (NeMo para Parakeet, `transformers`el oleoducto con `chunk_length_s`¿Qué es lo que se hace?

> 流式 ASR 需要分块编码器注意力和转移状态; usar para apoyar su biblioteca`transformers`el oleoducto 带 `chunk_length_s`)。




> **【拓展：语音与情感计算】**语音 no sólo transmite información escrita, también lleva una rica cantidad de señales emocionales (en inglés: voice signal) 语调、语速、音高变化) 情感语音识别 (en inglés: speech emotion recognition, SER) 语音 no solo transmite información escrita, sino que también lleva una gran cantidad de señales emocionales (en inglés: voice signal). 语音 tiene una amplia aplicación en el campo de la evaluación de calidad de los clientes, la vigilancia de la salud mental, la educación inteligente, etc.  Los modelos actuales de SOTA se basan en modelos de entrenamiento de las ondas 2vec 2.0 o HuBERT.

## Usalo con el marco de ejecución

La pila de 2026:

> Tecnología de 2026:

| Situation | Pick |
|-----------|------|
| English, offline, max quality | Whisper-large-v3-turbo |
| Multilingual, robust | SeamlessM4T v2 |
| Streaming, low latency | Parakeet-TDT-1.1B or Riva |
| Edge, mobile, <500 ms latency | Whisper-Tiny quantized or Moonshine (2024) |
| Long-form | Whisper with VAD-based chunking (WhisperX) |
| Domain-specific (medical, legal) | Fine-tune wav2vec 2.0 + domain LM fusion |

| 场景 | 选择 |
|------|------|
| 英文、离线、最高质量 | Whisper-large-v3-turbo |
| 多语言、鲁棒 | SeamlessM4T v2 |
| 流式、低延迟 | Parakeet-TDT-1.1B 或 Riva |
| 边缘/移动、<500 ms 延迟 | 量化 Whisper-Tiny 或 Moonshine（2024） |
| 长音频 | Whisper + VAD 分块（WhisperX） |
| 特定领域（医疗、法律） | 微调 wav2vec 2.0 + 领域 LM 融合 |



## Las trampas que todavía se envían en 2026

> 2026 año todavía en la trampa de los culpables

- **No VAD.**El funcionamiento de Whisper en silencio produce alucinaciones ("Gracias por ver!").
  **没有 VAD。**En su momento, el grupo de la banda de música de la banda de rock de la banda de rock de la banda de rock de la banda de rock de la banda de rock de la banda de la banda de rock de la banda de la banda de rock de la banda de la banda de rock de la banda de la banda de rock de la banda de la banda de rock de la banda de la banda de rock de la banda de la banda de rock de la banda de la banda de rock de la banda de la banda de rock de la banda de la banda de rock de la banda de la banda de rock de la banda de la banda de rock de la banda de la banda de rock de la banda de la banda de rock de la banda de la banda de la banda de rock de la banda de la banda de la banda de rock de la banda de la banda de la banda de la banda de la banda de la banda de la banda de la banda de la banda de la banda de la banda de la banda de la banda de la banda de la banda de la banda de la banda de la banda de la banda de la banda de la banda de la banda de la banda de la banda de la banda de la banda de la banda de la banda de la banda de la banda de la banda de la banda de la banda de la banda de la banda de la banda de la banda de la banda de la banda de la banda de la banda de la banda de la banda de la que se llama.
- **Character vs word vs subword WER.**Informar el nivel de palabra WER *after* normalización (minus letra, puntuación despojada).
  **字符 vs 词 vs 子词 WER。**報告归一化后 (小写、去标点) de la palabra clase WER。
- **Language ID drift.**El LID automático de Whisper desvía los clips ruidosos al japonés o gales; fuerza `language="en"`Cuando lo sepas.
  **语言识别漂移。**El reconocimiento automático de idiomas de susurros se traduce en japonés o en gales; conocidos idiomas obligatorios.`language="en"`¿Qué es eso?
- **Long clips without chunking.**Whisper tiene una ventana de 30 segundos.`chunk_length_s=30, stride=5`por cualquier cosa más larga.
  **长音频不分块。**Susurro tiene 30 segundos de ventana.`chunk_length_s=30, stride=5`¿Qué es eso?

> **【中文解读】**Este capítulo se centra en cómo se puede implementar el modelo como producto disponible. Desde el modelo original hasta el sistema de producción, se deben considerar múltiples dimensiones de optimización de rendimiento, tratamiento de errores, control, etc.


## Envíe el producto .

Salvo como`outputs/skill-asr-picker.md`Seleccionar el modelo, la estrategia de decodificación, el desglose y la fusión de LM para un objetivo de despliegue determinado.

> 保存为                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           `outputs/skill-asr-picker.md` para una determinada implementación de objetivos de selección de modelos, estrategias de descifrado, bloques y LM 融合方案.

## Los ejercicios.

1. **Easy.**- ¿ Qué ?`code/main.py`- Descifrará codiciosamente una salida CTC hecha a mano y calculará WER con una referencia.
   **简单。**运行                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           `code/main.py`◊ se trata de la producción manual de CTC 输出进行贪解码并计算 WER。
2. **Medium.**Implemente correctamente la búsqueda de haces de árbol de prefijo en el paso 2 (cuenta con la regla de fusión en blanco).
   **中等。**Correcto realizar paso 2 En el medio de la búsqueda de la viga de árbol anterior, consideremos el blanco de la combinación de las reglas.
3. **Hard.**Usar`whisper-large-v3-turbo`En el[LibriSpeech test-clean](https://www.openslr.org/12)Comparar con los números publicados.
   **困难。**En el[LibriSpeech test-clean](https://www.openslr.org/12)上使用 `whisper-large-v3-turbo`◊ calcular ‡ 100 ‡ ‡ ‡ ‡ ‡ ‡ ‡ ‡ ‡ ‡ ‡ ‡ ‡ ‡ ‡ ‡ ‡ ‡ ‡ ‡ ‡ ‡ ‡ ‡ ‡ ‡ ‡ ‡ ‡ ‡ ‡ ‡ ‡ ‡ ‡ ‡ ‡ ‡ ‡ ‡ ‡ ‡ ‡ ‡ ‡ ‡ ‡ ‡ ‡ ‡ ‡ ‡ ‡ ‡ ‡ ‡ ‡ ‡ ‡ ‡ ‡ ‡ ‡ ‡ ‡ ‡ ‡ ‡ ‡ ‡ ‡ ‡ ‡ ‡ ‡ ‡ ‡ ‡ ‡ ‡ ‡ ‡ ‡ ‡ ‡ ‡ ‡ ‡ ‡ ‡ ‡ ‡ ‡ ‡ ‡ ‡ ‡ ‡ ‡ ‡ ‡ ‡ ‡ ‡ ‡ ‡ ‡ ‡ ‡ ‡ ‡ ‡ ‡ ‡ ‡ ‡ ‡ ‡ ‡ ‡ ‡ ‡ ‡ ‡ ‡ ‡ ‡ ‡ ‡ ‡ ‡ ‡ ‡ ‡ ‡ ‡ ‡ ‡ ‡ ‡ ‡ ‡ ‡ ‡ ‡ ‡ ‡ ‡ ‡ ‡ ‡ ‡ ‡ ‡ ‡ ‡ ‡ ‡ ‡ ‡ ‡ ‡ ‡ ‡ ‡ ‡ ‡ ‡ ‡ ‡ ‡ ‡ ‡ ‡ ‡ ‡ ‡ ‡ ‡ ‡ ‡ ‡ ‡ ‡ ‡ ‡ ‡ ‡ ‡ ‡ ‡ ‡ ‡ ‡ ‡ ‡ ‡ ‡ ‡ ‡

> **【中文解读】**En el lenguaje de los términos "Lo que la gente dice" vs "Lo que realmente significa" se distingue entre el lenguaje diario y la definición técnica de significado.


## Términos clave .

| Term | What people say | What it actually means |
|------|-----------------|-----------------------|
| CTC | The blank-token loss | Marginal over all frame-to-token alignments; non-AR. |
| RNN-T | The streaming loss | CTC + next-token predictor; handles word-order. |
| Attention enc-dec | Whisper-style | Encoder + cross-attending decoder; best offline quality. |
| WER | The number you report | `(S+D+I)/N` at word level. |
| Blank | The emptiness | Special token in CTC signalling "no emission this frame". |
| LM fusion | External language model | Add weighted LM log-probs during beam search. |
| VAD | The silence gate | Voice activity detector; trims non-speech. |

| 术语 | 人们常说的 | 实际含义 |
|------|-----------|---------|
| CTC | blank token 损失 | 所有帧到 token 对齐的边际概率；非自回归。 |
| RNN-T | 流式损失 | CTC + 下一 token 预测器；处理词序。 |
| 注意力编解码 | Whisper 风格 | 编码器 + 交叉注意力解码器；最佳离线质量。 |
| WER | 你报告的数字 | 词级别的 `(S+D+I)/N`。 |
| Blank | 空白 | CTC 中表示"本帧不发射"的特殊 token。 |
| LM 融合 | 外部语言模型 | beam search 中加入加权的 LM 对数概率。 |
| VAD | 静音门 | 语音活动检测器；裁剪非语音部分。 |

> **【中文解读】**延伸阅读 proporciona un alto nivel de recursos para el aprendizaje profundo. Estos artículos y cursos son los referentes clásicos en el campo, adecuados para los lectores que necesitan una comprensión profunda.


## Más Leer más Leer más

- [Graves et al. (2006). Connectionist Temporal Classification](https://www.cs.toronto.edu/~graves/icml_2006.pdf) el documento del CTC.
  Graves 等 (2006). 连接时序分类CTC 论文。
- [Graves (2012). Sequence Transduction with RNNs](https://arxiv.org/abs/1211.3711) el papel RNN-T.
  Graves (2012). Usar RNN  realizar un proceso de transformación RNN-T 论文。
- [Radford et al. / OpenAI (2022). Whisper: Robust Speech Recognition via Large-Scale Weak Supervision](https://arxiv.org/abs/2212.04356) el documento canónico de 2022; extensión v3-turbo en 2024.
  Radford 等 / OpenAI (2022). Susurro: Masselva weak监督的鲁棒语音识别2022 年经典论文;2024 年 v3-turbo 扩展──
- [NVIDIA NeMo — Parakeet-TDT card](https://huggingface.co/nvidia/parakeet-tdt-1.1b) Líder del Directorio de RAS Abiertos para 2026.
  NVIDIA NeMoParakeet-TDT 模型卡2026 年 排行榜领先者──
- [Hugging Face — Open ASR Leaderboard](https://huggingface.co/spaces/hf-audio/open_asr_leaderboard) referencia en vivo en más de 25 modelos.
  Abrazar la cara Open ASR 排行榜 25+ 模型的实时基准测试──

> **【中文解读】**延伸阅读 proporciona recursos de alta calidad para el aprendizaje profundo, incluyendo artículos, tutorials y herramientas.

