# Los códec de audio neural  EnCodec, SNAC, Mimi, DAC y la división semántica-acústica

> La generación de audio 2026 es casi toda una serie de tokens. EnCodec, SNAC, Mimi y DAC convierten formas de onda continuas en secuencias discretas que un transformador puede predecir. La división de tokens semánticos vs acústicos  primer código como semántico, descanso como acústico  es el cambio arquitectónico más importante desde el transformador para el audio.

> **【中文解读】**La generación de sonido de 2026 años casi todo se basa en el token. EnCodec, SNAC, Mimi y DAC se continuará transformando en secuencias de separación, haciendo que el Transformer pueda predecir.

> **【拓展：音频 token 化】**Como en el texto hay un tokenizer BPE, el texto se convierte en un token, el audio tiene un EnCodec, etc.

**Type:** Learn | **类型:** 学习
**Languages:** Python | **语言:** Python
**Prerequisites:** Phase 6 · 02 (Spectrograms), Phase 10 · 11 (Quantization), Phase 5 · 19 (Subword Tokenization) | **前置知识:** 阶段 6 · 02（频谱图），阶段 10 · 11（量化），阶段 5 · 19（子词分词）
**Time:** ~60 minutes | **预计用时:** ~60 分钟

## El problema es la introducción del problema

Los modelos de lenguaje trabajan en tokens discretos. El audio es continuo. Si desea un modelo de estilo LLM para el habla / música  MusicGen, Moshi, Sesame CSM, VibeVoice, Orpheus  primero necesita un **neural audio codec**: un codificador aprendido que discrete el audio en un pequeño vocabulario de tokens, y un decodificador que coincide que reconstruye la forma de onda.

> 语言模型处理离散 token──音频是连续的── si quieres construir un modelo de LLM 风格的模型MusicGen、Moshi、Sesame CSM、VibeVoice、Orpheus你首先需要一个**神经音频编解码器**Un codificador de aprendizaje se despliega en un token de pequeño valor de palabras, además de un codificador de correlación.

> **【中文解读】**La pregunta planteada en este capítulo es: ¿cómo entender y aplicar correctamente esta tecnología en la ingeniería real? Comprender el contexto de la cuestión ayuda a comprender los puntos clave de decisión del tipo de selección técnica. En los sistemas de IA reales, el tipo de selección técnica errónea suele ser más alto que el costo de error de la realización de detalles.

Dos familias han surgido:

> Se han creado dos familias:

1. **Reconstruction-first codecs** EnCodec, DAC. Optimiza la calidad de audio perceptual. Los tokens son "acústicos"  capturan todo, incluida la identidad del altavoz, el timbre, el ruido de fondo.
   **重建优先编解码器**EnCodec、DAC──优化感知音频质量──Token es "声学学"它们 captan todo, incluyendo la identidad del habla, la calidad de la voz, el ruido de fondo.
2. **Semantic-first codecs** Mimi (Kyutai), SpeechTokenizer. Forza el primer código para codificar contenido lingüístico / fonético (a menudo destilizando de WavLM).
   **语义优先编解码器**Mimi(Kyutai)、SpeechTokenizer。强制第一码本编码语言/语音内容(usualmente pasando por WavLM 蒸)。后续码本是声学细节。

Las perspectivas de 2024-2026: **a pure reconstruction codec gives you blurry speech when you try to generate from text.**El LLM sobre tokens de codec tiene que aprender tanto la estructura del lenguaje como la estructura acústica en el mismo libro de código, que no se escala.

> Intuición de la temporada 2024-2026:**纯重建编解码器在从文本生成时给你模糊的语音。**El LLM superior debe aprender simultáneamente la estructura lingüística y la estructura sonora en el mismo código, esto no puede expandirse.

## El concepto central.

> **【中文解读】**Este capítulo presenta los conceptos y teorías básicos. La comprensión de estos conceptos es el prerrequisito de la realización posterior de la actividad, y también el conocimiento de los puntos de alta frecuencia de la entrevista y la práctica de la ingeniería.


![Four codec landscape: EnCodec, DAC, SNAC (multi-scale), Mimi (semantic+acoustic)](../assets/codec-comparison.svg)

### El truco principal: Cuantización de vectores residuales (RVQ)

En lugar de un libro de códigos grande (que necesitaría millones de códigos para una buena calidad), todos los códigos de audio modernos usan **RVQ**El primer libro de código cuantifica la salida del codificador; el segundo cuantifica el residual; etc. Cada libro de código es de 1024 códigos.

> En lugar de usar un código grande, todo el mundo utiliza un código de calidad.**RVQ**Un grupo de pequeños códigos de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código

En el momento de la inferencia, el decodificador suma todos los códigos elegidos por marco para reconstruir.

>  En el caso de la solución, el descifrador se va a buscar y reconstruir todos los codes de la selección 

### Los cuatro códec que importan en 2026

**EnCodec (Meta, 2022).**El código base. Encoder-decodificador sobre forma de onda, cuello de botella RVQ. 24 kHz, 32 libretas de código posibles, 4 libretas de código predeterminadas @ 1.5 kbps. Utiliza `1D conv + transformer + 1D conv`arquitectura. Usado por MusicGen.

> **EnCodec（Meta，2022）。**基线──波形上的编码器-解码器,RVQ 瓶──24 kHz, máximo 32 个码本,默认 4 个码本 @ 1.5 kbps──使用 `1D conv + transformer + 1D conv`架构──MusicGen Uso──

**DAC (Descript, 2023).**RVQ con libros de código L2-normalizados, funciones de activación periódicas, pérdidas mejoradas. La mayor fidelidad de reconstrucción de cualquier código abierto  a veces indistinguible del habla original con 12 libros de código. 44.1 kHz banda completa.

> **DAC（Descript，2023）。** Adopción de L2 归一化码本、周期性激活函数和改进损失的 RVQ──开源编码器中重建保真度最高12个码本时有时与原始语音无法区分──44.1 kHz 全频带──

**SNAC (Hubert Siuzdak, 2024).**RVQ a múltiples escalas  los libros de código gruesos operan a una velocidad de cuadros más baja que los finos. Modelan eficazmente el audio jerárquicamente: un "bozón" grueso a ~ 12 Hz más detalles a 50 Hz. Usado por Orpheus-3B porque la estructura jerárquica se adapta bien a la generación basada en LM.

> **SNAC（Hubert Siuzdak，2024）。**La variedad de RVQ粗码本以细码本比较低的率运行──有效地分层建模音频:约12 Hz 的粗草图加50 Hz 的细节──Orpheus-3B 使用,因为分层结构很好地映射到基于LM的生成──

**Mimi (Kyutai, 2024).**El cambio de juego 2026 . 12.5 Hz frecuencia de fotogramas (extremadamente baja), 8 libros de código @ 4.4 kbps.**distilled from WavLM** entrenado para predecir las características de contenido de voz de WavLM. Los códigos 1-7 son residuos acústicos. Esta división potencia Moshi (lección 15) y Sesame CSM.

> **Mimi（Kyutai，2024）。**2026 años de juego cambia de reglamento ⋅ 12.5 Hz 率(极低),8 个码本 @ 4.4 kbps⋅码本 0 **从 WavLM 蒸馏** entrenamiento para predecir el contenido del lenguaje de WavLM 码本 1-7  声学残差──这种分离驱动了Moshi第15课) y Sesame CSM──

### Las velocidades de cuadros son importantes para la modelado del lenguaje

Rate de fotogramas más bajo = secuencia más corta = LM más rápido.

> 率对语言建模很重要: 率越低 = 序列越短 = LM 越快──

| Codec | Frame rate | 1 s = N frames | Good for |
|-------|-----------|----------------|---------|
| EnCodec-24k | 75 Hz | 75 | music, general audio |
| DAC-44.1k | 86 Hz | 86 | high-fidelity music |
| SNAC-24k (coarse) | ~12 Hz | 12 | AR-LM efficient |
| Mimi | 12.5 Hz | 12.5 | streaming speech |

| 编解码器 | 帧率 | 1 秒 = N 帧 | 适用场景 |
|---------|------|------------|---------|
| EnCodec-24k | 75 Hz | 75 | 音乐、通用音频 |
| DAC-44.1k | 86 Hz | 86 | 高保真音乐 |
| SNAC-24k（粗） | ~12 Hz | 12 | AR-LM 高效 |
| Mimi | 12.5 Hz | 12.5 | 流式语音 |

A 12,5 Hz, una declaración de 10 segundos es sólo 125 marcos de códec  un transformador puede predecirlos fácilmente.

> En 12,5 Hz, el volumen de 10 segundos de voz es de 125 códigos.

### Señales semánticos vs acústicos

> 语义 vs 声学 token

```
frame_t → [semantic_token_t, acoustic_token_0_t, acoustic_token_1_t, ..., acoustic_token_6_t]
```

- **Semantic token (codebook 0 in Mimi).**Encodifica lo que se dijo  fonemas, palabras, contenido. Destilado de WavLM a través de una pérdida de predicción auxiliar.
  **语义 token（Mimi 中的码本 0）。**编码说了什么音素、单词、内容──通过辅助预测损失从波LM 蒸──
- **Acoustic tokens (codebooks 1-7).**Timbre de código, identidad del altavoz, prosodia, ruido de fondo, detalles finos.
  **声学 token（码本 1-7）。**编码音色、说话人身份、律、背景噪音、精细细节──

Un AR LM predice primero el token semántico (condicionado en texto), luego predice los tokens acústicos (condicionados en referencia semántica + altavoz). Esta factorization es la razón por la que el TTS moderno puede cero-shot-clone voces: el modelo semántico maneja el contenido; el modelo acústico maneja el timbre.

> Autorecambio de TTS 能够零样本克隆声音的原因:语义模型处理内容,声学模型处理音色──

### 2026 calidad de reconstrucción (bites por segundo, menor bitrate es mejor)

| Codec | Bitrate | PESQ | ViSQOL |
|-------|---------|------|--------|
| Opus-20kbps | 20 kbps | 4.0 | 4.3 |
| EnCodec-6kbps | 6 kbps | 3.2 | 3.8 |
| DAC-6kbps | 6 kbps | 3.5 | 4.0 |
| SNAC-3kbps | 3 kbps | 3.3 | 3.8 |
| Mimi-4.4kbps | 4.4 kbps | 3.1 | 3.7 |

| 编解码器 | 比特率 | PESQ | ViSQOL |
|---------|--------|------|--------|
| Opus-20kbps | 20 kbps | 4.0 | 4.3 |
| EnCodec-6kbps | 6 kbps | 3.2 | 3.8 |
| DAC-6kbps | 6 kbps | 3.5 | 4.0 |
| SNAC-3kbps | 3 kbps | 3.3 | 3.8 |
| Mimi-4.4kbps | 4.4 kbps | 3.1 | 3.7 |

Los codecs tradicionales como Opus siguen ganando por bit en calidad perceptiva.**discrete tokens**(que no produce Opus) y **generative-model quality**(lo que el LM puede hacer con esos tokens).

> 傳統編解碼器 (Opus) sigue ganando en cada bit de la calidad del conocimiento.**离散 token**(Opus 不产生) y**生成模型质量**(LM 能用这些符号做什么) 上胜出.

> **【拓展：语音 AI 的产品化】**La tecnología de voz se enfrenta a un desafío único en la productorización: diferentes voces, ruidos de contexto, remota recogida, muchos hablar, etc.

> **【拓展：多语言语音技术】**Las características de los idiomas de todo el mundo son muy diferentes: el sonido de los idiomas de todo el mundo (como el chino) es alto, el lenguaje de bajo recurso es poco capacitado.



## Construye y realiza.

> **【中文解读】**Este capítulo a través del código de la implementación de algoritmos centrales de cero. Este método "desde cero" puede ayudar a entender el principio detrás del marco, no se encuentra en la caja negra cuando se encuentran problemas.

```figure
rvq-codec-cascade
```

## Construye el mismo

### Paso 1: codificar con EnCodec

```python
from encodec import EncodecModel
import torch

model = EncodecModel.encodec_model_24khz()
model.set_target_bandwidth(6.0)  # kbps

wav = torch.randn(1, 1, 24000)
with torch.no_grad():
    encoded = model.encode(wav)
codes, scale = encoded[0]
# codes: (1, n_codebooks, n_frames), dtype=int64
```

`n_codebooks=8`Cada código es 0-1023 (10 bits).

> 6 kbps abajo `n_codebooks=8` Cada uno de ellos tiene un valor de 0-1023  10 比特) 

### Paso 2: Descifrar y medir la reconstrucción

```python
with torch.no_grad():
    wav_recon = model.decode([(codes, scale)])

from torchaudio.functional import compute_deltas
import torch.nn.functional as F

mse = F.mse_loss(wav_recon[:, :, :wav.shape[-1]], wav).item()
```

### Paso 3: la división semántica-acústica (estilo Mimi)

```python
from moshi.models import loaders
mimi = loaders.get_mimi()

with torch.no_grad():
    codes = mimi.encode(wav)  # shape (1, 8, frames@12.5Hz)

semantic = codes[:, 0]
acoustic = codes[:, 1:]
```

El código semántico 0 está alineado con WavLM. Se puede entrenar un transformador de texto a semántica  un vocabulario mucho más pequeño que ir directamente al audio. Luego, un decodificador de forma acústica a onda separado condiciones en una referencia de altavoz.

> 语义码本 0 与 WavLM 对齐──你可以训练一个文本→语义 Transformer词表比直接到音频小得多──然后一个独立的声学→波形解码器以说话人参考为条件──

### Paso 4: por qué funciona el AR LM sobre los tokens de codec

Para un clip de 10 segundos de voz en los libros de códigos de Mimi de 12,5 Hz × 8:

```
N_tokens = 10 * 12.5 * 8 = 1000 tokens
```

> **【中文解读】**Este capítulo muestra cómo utilizar un marco maduro (como PyTorch、HuggingFace, etc.) para aplicar rápidamente esta tecnología. En los proyectos reales, se realiza con prioridad el uso de un marco experimentado, se pueden reducir errores y mejorar la eficiencia de desarrollo.


1000 tokens es un contexto trivial para un transformador. Un transformador de parámetro de 256M puede generar 10 segundos de habla en milisegundos en una GPU moderna.

> 1000 tokens para el Transformer son insignificantes para el transformer de 2.56 mil millones de parámetros en la GPU moderna puede generar 10 segundos de voz en pocos segundos.




> **【拓展：语音与情感计算】**语音 no sólo transmite información escrita, también lleva una rica cantidad de señales emocionales (en inglés: voice signal) 语调、语速、音高变化) 情感语音识别 (en inglés: speech emotion recognition, SER) 语音 no solo transmite información escrita, sino que también lleva una gran cantidad de señales emocionales (en inglés: voice signal). 语音 tiene una amplia aplicación en el campo de la evaluación de calidad de los clientes, la vigilancia de la salud mental, la educación inteligente, etc.  Los modelos actuales de SOTA se basan en modelos de entrenamiento de las ondas 2vec 2.0 o HuBERT.

## Usalo con el marco de ejecución

Problema de mapa → codec:

| Task | Codec |
|------|-------|
| General music generation | EnCodec-24k |
| Highest-fidelity reconstruction | DAC-44.1k |
| AR LM over speech (TTS) | SNAC or Mimi |
| Streaming full-duplex speech | Mimi (12.5 Hz) |
| Sound-effect library with text | EnCodec + T5 condition |
| Fine-grained audio editing | DAC + inpainting |

| 任务 | 编解码器 |
|------|---------|
| 通用音乐生成 | EnCodec-24k |
| 最高保真重建 | DAC-44.1k |
| 语音上的 AR LM（TTS） | SNAC 或 Mimi |
| 流式全双工语音 | Mimi（12.5 Hz） |
| 文本驱动的音效库 | EnCodec + T5 条件 |
| 细粒度音频编辑 | DAC + 内画 |

Regla de oro: **if you're building a generative model, start with Mimi or SNAC. If you're building a compression pipeline, use Opus.**

> 经验法则:**如果你在构建生成模型，从 Mimi 或 SNAC 开始。如果在构建压缩流水线，使用 Opus。**



## Las trampas

- **Too many codebooks.**Añadir libros de código aumenta la fidelidad linealmente pero la longitud de la secuencia LM también linealmente.
  **码本过多。**增加码本会线性提高保真度, pero LM 序列长度也线性增长──停在 8-12──
- **Frame-rate mismatch.**El entrenamiento de LM en 12,5 Hz Mimi luego el ajuste fino en 50 Hz EnCodec falla silenciosamente.
  **帧率不匹配。**En 12,5 Hz Mimi arriba entrenar LM, luego en 50 Hz EnCodec arriba en la cámara baja fracaso.
- **Assuming all codebooks equal.**En Mimi, el código 0 lleva contenido; perderlo destruye la inteligencia.
  **假设所有码本同等重要。**En Mimi, el código 0 carga contenido; perderlo destruirá la comprensibilidad.
- **Using reconstruction quality as the only metric.**Un codec puede tener una gran reconstrucción pero no servirá para la generación basada en LM si la estructura semántica es mala.
  **仅用重建质量作为唯一指标。**Un codificador puede reconstruir la calidad muy bien, pero si la estructura de la lengua es diferente, no es necesario para la generación basada en LM.

> **【中文解读】**Este capítulo se centra en cómo se puede implementar el modelo como producto disponible. Desde el modelo original hasta el sistema de producción, se deben considerar múltiples dimensiones de optimización de rendimiento, tratamiento de errores, control, etc.


## Envíe el producto .

Salvo como`outputs/skill-codec-picker.md`Seleccione un codec para una tarea generativa o de compresión dada.

> 保存为                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           `outputs/skill-codec-picker.md`◊ para una determinada tarea de generación o compresión seleccionar el código.

## Los ejercicios.

1. **Easy.**- ¿ Qué ?`code/main.py`Implementa un cuantificador de juguete escalar + residual y mide el error de reconstrucción al agregar libros de código.
   **简单。**运行                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           `code/main.py`  logró un marcado de juguete + residuo de la medición, la medición con el aumento de la codificación de la reconstrucción de la diferencia
2. **Medium.**Instalar`encodec`y comparar 1, 4, 8, 32 libros de código en un clip de discurso prolongado.
   **中等。**Instalación`encodec`, en el que se deja un audio en la parte superior, comparar 1⁄4, 8⁄32 个码本── dibujar PESQ o MSE vs 比特率──
3. **Hard.**Carga Mimi. Encienda un clip. reemplace el código 0 con números enteros aleatorios; decodifique. Luego reemplace el código 7 de manera similar. Compara las dos corrupciones  código 0 corrupción debe destruir la inteligencia; código 7 corrupción apenas debe cambiar nada.
   **困难。**La versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión original de la versión de la versión original de la versión de la versión original de la versión de la versión original de la versión original de la versión original de la versión de la versión original de la versión de la versión original de la versión de la versión original de la versión de la versión de la versión de la versión de la versión original de la versión de la versión de la versión original de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de

> **【中文解读】**En el lenguaje de los términos "Lo que la gente dice" vs "Lo que realmente significa" se distingue entre el lenguaje diario y la definición técnica de significado.


## Términos clave .

| Term | What people say | What it actually means |
|------|-----------------|-----------------------|
| RVQ | Residual quantization | Cascade of small codebooks; each quantizes the previous residual. |
| Frame rate | Codec speed | How many token-frames per second. Lower = faster LM. |
| Semantic codebook | Codebook 0 (Mimi) | Codebook distilled from SSL features; encodes content. |
| Acoustic codebooks | Everything else | Timbre, prosody, noise, fine detail. |
| PESQ / ViSQOL | Perceptual quality | Objective metrics correlating with MOS. |
| EnCodec | Meta codec | The RVQ baseline; used by MusicGen. |
| Mimi | Kyutai codec | 12.5 Hz frame rate; semantic-acoustic split; powers Moshi. |

| 术语 | 人们常说的 | 实际含义 |
|------|-----------|---------|
| RVQ | 残差量化 | 小码本级联；每个量化前一个残差。 |
| 帧率 | 编解码器速度 | 每秒多少 token 帧。越低 = LM 越快。 |
| 语义码本 | 码本 0（Mimi） | 从 SSL 特征蒸馏的码本；编码内容。 |
| 声学码本 | 其余所有 | 音色、韵律、噪声、精细细节。 |
| PESQ / ViSQOL | 感知质量 | 与 MOS 相关的客观指标。 |
| EnCodec | Meta 编解码器 | RVQ 基线；MusicGen 使用。 |
| Mimi | Kyutai 编解码器 | 12.5 Hz 帧率；语义-声学分离；驱动 Moshi。 |

> **【中文解读】**延伸阅读 proporciona un alto nivel de recursos para el aprendizaje profundo. Estos artículos y cursos son los referentes clásicos en el campo, adecuados para los lectores que necesitan una comprensión profunda.


## Más Leer más Leer más

- [Défossez et al. (2023). EnCodec](https://arxiv.org/abs/2210.13438) el nivel de referencia de RVQ.
  Desfossez 等 (2023). EnCodecRVQ 基线。
- [Kumar et al. (2023). Descript Audio Codec (DAC)](https://arxiv.org/abs/2306.06546) La máxima fidelidad abierta.
  Kumar 等 (2023). DAC最高保真开源编解码器──
- [Siuzdak (2024). SNAC](https://arxiv.org/abs/2410.14411) RVQ a escala múltiple.
  Siuzdak (2024). SNAC 多尺度 RVQ──
- [Kyutai (2024). Mimi codec](https://kyutai.org/codec-explainer) división semántica-acústica, destilación de WavLM.
  Kyutai (2024). Mimi 编解码器语义-声学分离,WavLM 蒸。
- [Borsos et al. (2023). AudioLM](https://arxiv.org/abs/2209.03143) el paradigma semántico/acústico de dos etapas.
  Borsos 等 (2023). AudioLM两阶段语义/声学范式──
- [Zeghidour et al. (2021). SoundStream](https://arxiv.org/abs/2107.03312) el código RVQ original en streaming.
  El programa de televisión de la televisión de la Unión Europea (UAE) se desarrolla en el Reino Unido.

> **【中文解读】**延伸阅读 proporciona recursos de alta calidad para el aprendizaje profundo, incluyendo artículos, tutorials y herramientas.

