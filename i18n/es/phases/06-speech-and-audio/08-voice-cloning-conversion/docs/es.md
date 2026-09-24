# Cloning de voz y conversión de voz .

> La clonación de voz lee tu texto en la voz de otra persona. La conversión de voz reescribe tu voz en la de otra persona mientras se conserva lo que dijiste. Ambos se apoyan en la misma descomposición: la identidad del hablante separada del contenido.

> **【中文解读】**语音克隆 usar la voz de otra persona para leer tu texto;语音转换把你的声音变成别人的但保留内容── los dos son el mismo núcleo de descomposición:将说话人身份与内容分离──

> **【拓展：语音克隆的伦理与法律】**语音克隆技术引发严重伦理和法律问题深度伪造语音欺诈、名人声音未经授权使用──2025-2026 años más de litigios ((como Warner Music 5 mil millones de dólares) promovió el desarrollo de la tecnología de audio频水印和防伪──

**Type:** Build | **类型:** 构建
**Languages:** Python | **语言:** Python
**Prerequisites:** Phase 6 · 06 (Speaker Recognition), Phase 6 · 07 (TTS) | **前置知识:** 阶段 6 · 06（说话人识别），阶段 6 · 07（TTS）
**Time:** ~75 minutes | **预计用时:** ~75 分钟

## El problema es la introducción del problema

En 2026, un clip de audio de 5 segundos es suficiente para producir un clon de alta calidad de la voz de cualquier persona con una GPU de consumo. ElevenLabs, F5-TTS, OpenVoice v2, VoiceBox envían todos clonamiento de cero disparos o pocos disparos. La tecnología es una bendición (accesividad TTS, doblaje, voces asistentes) y un arma (llamadas de estafa, deepfakes políticos, robo de IP).

> 2026 años, un segmento de 5 segundos de audio está disponible para usar el uso de GPU de consumo de alta calidad para hacer cualquier voz de cualquier persona. ElevenLabs, F5-TTS, OpenVoice v2, VoiceBox, ofrecen un modelo o un poco de clon. Esta tecnología es un instrumento de inteligencia, es también un arma.

> **【中文解读】**La pregunta planteada en este capítulo es: ¿cómo entender y aplicar correctamente esta tecnología en la ingeniería real? Comprender el contexto de la cuestión ayuda a comprender los puntos clave de decisión del tipo de selección técnica. En los sistemas de IA reales, el tipo de selección técnica errónea suele ser más alto que el costo de error de la realización de detalles.

Dos tareas estrechamente relacionadas:

> Dos tareas estrechamente relacionadas:

- **Voice cloning (TTS-side):**texto + 5 segundos de voz de referencia → audio en esa voz.
  **声音克隆（TTS 侧）：**文本 + 5 秒参考声音 → El sonido de la voz
- **Voice conversion (speech-side):**Audio fuente (persona A diciendo X) + voz de referencia de la persona B → audio de B diciendo X.
  **语音转换（语音侧）：**源音频(说话人 A 说 X) + 说话人 B 的参考声音 → B 说 X 的音频。

Ambos factorizan una forma de onda en (contenido, altavoz, prosodia) y recombinan contenido de una fuente con altavoz de otra.

> 两者都将波形分解为(内容、说话人、律) y se vuelve a reunir de una fuente a otra fuente de contenido y de la otra fuente de la conversación.

La principal restricción que ahora se embarca en 2026:**watermarking and consent gates are legally required in the EU (AI Act, enforceable August 2026) and in California (AB 2905, effective 2025)**Su oleoducto debe emitir una marca de agua inaudible y rechazar clones no consensuados.

> 2026 años que usted enfrenta:**水印和同意门在 EU（AI 法案，2026 年 8 月生效）和加利福尼亚州（AB 2905，2025 年生效）是法律要求的**Su flujo de agua debe emitir una huella inaudible y rechazar el clorón sin su consentimiento.

## El concepto central.

> **【中文解读】**Este capítulo presenta los conceptos y teorías básicos. La comprensión de estos conceptos es el prerrequisito de la realización posterior de la actividad, y también el conocimiento de los puntos de alta frecuencia de la entrevista y la práctica de la ingeniería.


![Voice cloning vs conversion: factorize, swap speaker, recombine](../assets/voice-cloning.svg)

**Zero-shot cloning.**Pasar un clip de 5 segundos a un modelo que ha sido entrenado en miles de altavoces. El codificador de altavoces mapea el clip a un altavoces que se incorpora; el decodificador TTS condiciones en esa incorporación más texto.

> **零样本克隆。**Se puede utilizar un sistema de programación de audio en 5 segundos para transmitir a un modelo entrenado por miles de personas.

Utilizado por: F5-TTS (2024), YourTTS (2022), XTTS v2 (2024), OpenVoice v2 (2024).

> Usuario:F5-TTS(2024) 、TuTTS(2022) 、XTTS v2(2024) 、OpenVoice v2(2024) ✿

**Few-shot fine-tuning.**El programa de audio de la audiencia de la audiencia de la audiencia de la audiencia de la audiencia de la audiencia de la audiencia de la audiencia de la audiencia de la audiencia de la audiencia de la audiencia de la audiencia de la audiencia de la audiencia de la audiencia de la audiencia de la audiencia de la audiencia de la audiencia de la audiencia de la audiencia de la audiencia de la audiencia de la audiencia de la audiencia de la audiencia de la audiencia de la audiencia de la audición de la audición de la audición de la audición de la audición de la audición de la audición de la audición de la audición de la audición de la audición de la audición de la audición de la audición de la audición de la audición de la audición de la audición de la audición de la audición de la audición de la audición de la audición de la audición de la audición de la audición de la audición de la audición de la audición de la audición de la audición de la audición de la audición de la audición de la audición de la audición de la audición de la audición de la audición de la audición de la audición de la audición de la audición de la audición de la audición de la audición de la audición de la audición de audición de la audición de la audición de la audición de audición de la audición de la audición de la audición de audición de la audición de audición de la audición de la audición de audición de la audición de audición de la audición de audición de la audición de audición de la audición de audición de la audición de audición de la audición de la audición de la audición de audición de audición de la audición de la audición de la audición de la audición de audición de la audición de la audición de la audición de la audición de audición de la audición de la audición de la audición de la audición de la audición de la audición de la audición de la audición de la audición de la audición de la audición de la audición de la audición de la audición

> **少样本微调。**录制目标声音 5-30 分钟──LoRA 微调基础模型一小时──质量从"还行"跳到"无法区分"──Coqui 和 ElevenLabs 都支持这种模式;社区用F5-TTS 实现──

**Voice conversion (VC).**Dos familias:

> **语音转换（VC）。**两个家族:

- **Recognition-synthesis.**ejecuta un modelo similar a ASR para extraer la representación de contenido (por ejemplo, posteriors fonéticos blandos, PPGs), luego sintetizar con el incrustamiento de altavoces objetivo. Robusto para el lenguaje y el acento.
  **识别-合成。**运行类 ASR 模型提取内容表示 (如软音素后验、PPG), luego utilizar el objetivo de la lenguaje para la gente en el nuevo conjunto.
- **Disentanglement.**Entrenar un autoencoder que separa el contenido, el altavoz y la prosodia en un espacio latente en el cuello de botella. Swap altavoz que se incorpora en la inferencia. Calidad menor pero más rápida. Utilizado por AutoVC (2019), VITS-VC variantes.
  **解耦。**訓練自編編機在瓶处的潜在空间中分离内容、言論者和律──推理时交换言人嵌入──質量较低但更快──AutoVC(2019)、VITS-VC 变体使用──

**Neural codec-based cloning (2024+).**VALL-E, VALL-E 2, NaturalSpeech 3, VoiceBox  tratan el audio como tokens discretos de SoundStream / EnCodec, entrenan un modelo autorregresivista o de coincidencia de flujo sobre los tokens de codec.

> **基于神经编解码器的克隆（2024+）。**VALL-E、VALL-E 2、NaturalSpeech 3、VoiceBox将音频视为 SoundStream/EnCodec's离散代币, en编解码代币上训练大型自归归或流匹配模型──短提示上质量可与ElevenLabs相当──

### El poco de ética, no un paralelo

> ### 伦理问题, no es opcional

**Watermarking.**PerTh (Perth) y SilentCipher (2024) incorporan un ID de ~16-32 bits imperceptiblemente en el audio. Sobrevive al reencodificación, transmisión y edición común.

> **水印。**PerTh 和 SilentCipher(2024) En el audio se insensible en 16-32 bits ID.

**Consent gates.**Debe combinar cada salida clonada con un registro de consentimiento verificable. "Yo, Rohit, el 2026-04-22, autorizar esta voz para el propósito X".

> **同意门。**Cada uno de los productos de clón debe estar acompañado de un registro de consentimiento verificable.

**Detection.**AASIST, RawNet2 y Wav2Vec2-AASIST se utilizan como detectores. ASVspoof 2025 desafío publicó EERs de 0.82.3% para detectores de última generación contra ElevenLabs, VALL-E 2, y las salidas de Bark.

> **检测。**AASIST、RawNet2 和 Wav2Vec2-AASIST 作为检测器发布──ASVspoof 2025 挑战赛发布了SOTA 检测器对ElevenLabs、VALL-E 2 和 Bark 输出 EER为0.8-2.3%──

### Números (2026)

> Número de años 2026

| Model | Zero-shot? | SECS (target sim) | WER (intel.) | Params |
|-------|-----------|--------------------|--------------|--------|
| F5-TTS | Yes | 0.72 | 2.1% | 335M |
| XTTS v2 | Yes | 0.65 | 3.5% | 470M |
| OpenVoice v2 | Yes | 0.70 | 2.8% | 220M |
| VALL-E 2 | Yes | 0.77 | 2.4% | 370M |
| VoiceBox | Yes | 0.78 | 2.1% | 330M |

| 模型 | 零样本？ | SECS（目标相似度） | WER（可懂度） | 参数量 |
|------|---------|-------------------|--------------|--------|
| F5-TTS | 是 | 0.72 | 2.1% | 3.35 亿 |
| XTTS v2 | 是 | 0.65 | 3.5% | 4.7 亿 |
| OpenVoice v2 | 是 | 0.70 | 2.8% | 2.2 亿 |
| VALL-E 2 | 是 | 0.77 | 2.4% | 3.7 亿 |
| VoiceBox | 是 | 0.78 | 2.1% | 3.3 亿 |

> **【中文解读】**Este capítulo a través del código de la implementación de algoritmos centrales de cero. Este método "desde cero" puede ayudar a entender el principio detrás del marco, no se encuentra en la caja negra cuando se encuentran problemas.


SECS > 0,70 es generalmente indistinguible del objetivo para la mayoría de los oyentes.

> SECS > 0,70 para la mayoría de los oyentes, normalmente no se puede distinguir entre el objetivo y el objetivo.

> **【拓展：语音 AI 的产品化】**La tecnología de voz se enfrenta a un desafío único en la productorización: diferentes voces, ruidos de contexto, remota recogida, muchos hablar, etc.

> **【拓展：多语言语音技术】**Las características de los idiomas de todo el mundo son muy diferentes: el sonido de los idiomas de todo el mundo (como el chino) es alto, el lenguaje de bajo recurso es poco capacitado.



## Construye y realiza.
```figure
sp-voice-factorize
```

## Construye el mismo

### Paso 1: descomponer con reconocimiento-síntesis (demo de código sólo en main.py)

```python
def clone_pipeline(ref_audio, text, target_embedder, tts_model):
    speaker_emb = target_embedder.encode(ref_audio)
    mel = tts_model(text, speaker=speaker_emb)
    return vocoder(mel)
```

Conceptualmente simple; la masa de implementación es de`tts_model`y el codificador de altavoces.

> 概念上简单; realización en`tts_model`Y habla de gente en el ordenador.

### Paso 2: clona de tiro cero con F5-TTS

```python
from f5_tts.api import F5TTS
tts = F5TTS()
wav = tts.infer(
    ref_file="rohit_5s.wav",
    ref_text="The quick brown fox jumps over the lazy dog.",
    gen_text="Please add milk and bread to my list.",
)
```

La transcripción de referencia debe coincidir exactamente con el audio; la falta de coincidencia rompe la alineación.

> 参考转录必须与音频完全匹配; 不匹配将破坏对齐──

### Paso 3: conversión de voz con KNN-VC

```python
import torch
from knnvc import KNNVC  # 2023 model, https://github.com/bshall/knn-vc
vc = KNNVC.load("wavlm-base-plus")
out_wav = vc.convert(source="my_voice.wav", target_pool=["alice_1.wav", "alice_2.wav"])
```

KNN-VC ejecuta WavLM para extraer embebidos por marco para el pool de fuentes y objetivos, luego reemplaza cada marco de origen con su vecino más cercano en el pool.

> KNN-VC 运行 WavLM 提取源和目标池的逐嵌入, luego usar el vecino más cercano en el池 para reemplazar cada fuente──非参数化,一分钟目标语音即可工作──

### Paso 4: incrustar una marca de agua

```python
from silentcipher import SilentCipher
sc = SilentCipher(model="2024-06-01")
payload = b"consent_id:abc123;ts:1745353200"
watermarked = sc.embed(wav, sr=24000, message=payload)
detected = sc.detect(watermarked, sr=24000)   # returns payload bytes
```

~ 32 bits de carga útil, detectable después de la recodificación de MP3 y ruido ligero.

> 约 32 位载荷,MP3 重编码和轻度噪音后仍可检测──

### Paso 5: Puerta de consentimiento

```python
def cloned_inference(text, ref_audio, consent_record):
    assert verify_signature(consent_record), "Signed consent required"
    assert consent_record["speaker_id"] == hash_speaker(ref_audio)
    wav = tts.infer(ref_file=ref_audio, gen_text=text)
    wav = watermark(wav, payload=consent_record["id"])
    return wav
```

> **【中文解读】**Este capítulo muestra cómo utilizar un marco maduro (como PyTorch、HuggingFace, etc.) para aplicar rápidamente esta tecnología. En los proyectos reales, se realiza con prioridad el uso de un marco experimentado, se pueden reducir errores y mejorar la eficiencia de desarrollo.





> **【拓展：语音与情感计算】**语音 no sólo transmite información escrita, también lleva una rica cantidad de señales emocionales (en inglés: voice signal) 语调、语速、音高变化) 情感语音识别 (en inglés: speech emotion recognition, SER) 语音 no solo transmite información escrita, sino que también lleva una gran cantidad de señales emocionales (en inglés: voice signal). 语音 tiene una amplia aplicación en el campo de la evaluación de calidad de los clientes, la vigilancia de la salud mental, la educación inteligente, etc.  Los modelos actuales de SOTA se basan en modelos de entrenamiento de las ondas 2vec 2.0 o HuBERT.

## Usalo con el marco de ejecución

La pila de 2026:

> Tecnología de 2026:

| Situation | Pick |
|-----------|------|
| 5-sec zero-shot clone, open-source | F5-TTS or OpenVoice v2 |
| Commercial production cloning | ElevenLabs Instant Voice Clone v2.5 |
| Voice conversion (rewriting) | KNN-VC or Diff-HierVC |
| Many-speaker fine-tune | StyleTTS 2 + speaker adapter |
| Cross-lingual cloning | XTTS v2 or VALL-E X |
| Deepfake detection | Wav2Vec2-AASIST |

| 场景 | 选择 |
|------|------|
| 5 秒零样本克隆，开源 | F5-TTS 或 OpenVoice v2 |
| 商业生产级克隆 | ElevenLabs Instant Voice Clone v2.5 |
| 语音转换（重写） | KNN-VC 或 Diff-HierVC |
| 多说话人微调 | StyleTTS 2 + 说话人适配器 |
| 跨语言克隆 | XTTS v2 或 VALL-E X |
| 深度伪造检测 | Wav2Vec2-AASIST |



## Las trampas

> 常见陷

- **Misaligned reference transcript.**F5-TTS y similares requieren que el texto de referencia coincida exactamente con el audio de referencia, incluida la puntuación.
  **参考转录不对齐。**F5-TTS etc. Requieren que el texto de referencia se ajuste completamente con el audio de referencia, incluyendo los puntos de referencia.
- **Reverberant reference.**Echo mata al clon, graba en secas y cercanas.
  **混响参考。**De acuerdo con el director de la compañía, el proyecto de investigación de la compañía de investigación de la industria de la energía, se encuentra en una fase de desarrollo.
- **Emotional mismatch.**La referencia de entrenamiento "alegre" produce clones alegres de todo.
  **情感不匹配。**                                                                                                                                                                                                                                                              
- **Language leakage.**Clonar a un hablante inglés y luego pedir al modelo que hable francés a menudo lleva el acento de todos modos; use modelos interlinguísticos (XTTS, VALL-E X).
  **语言泄漏。**克隆英文说话人然后让模型说法语仍将带有口音; usar modelos跨语言 (translanguage) XTTS、VALL-E X) 
- **No watermark.**No se puede enviar legalmente en la UE a partir de agosto de 2026.
  **没有水印。**Desde el 8 de agosto de 2026 se impone la publicación en la UE.

> **【中文解读】**Este capítulo se centra en cómo se puede implementar el modelo como producto disponible. Desde el modelo original hasta el sistema de producción, se deben considerar múltiples dimensiones de optimización de rendimiento, tratamiento de errores, control, etc.


## Envíe el producto .

Salvo como`outputs/skill-voice-cloner.md`. Diseñar un conducto de clonación o conversión con puerta de consentimiento + marca de agua + objetivo de calidad.

> 保存为                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           `outputs/skill-voice-cloner.md`◊ diseño con consentimiento + 水印 + 质量目标的克隆或转换流水线──

## Los ejercicios.

1. **Easy.**- ¿ Qué ?`code/main.py`.Demonstra el intercambio entre altavoces integrados calculando el cosino entre dos " altavoces" antes y después del intercambio.
   **简单。**运行                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           `code/main.py`◊ Por medio de la cálculo de los intercambios anteriores y posteriores, los otros dos "el lenguaje" se parecen a los otros dos y se presentan en el lenguaje.
2. **Medium.**Utilice OpenVoice v2 para clonar su propia voz. Medir SECS entre referencia y clonación. Medir CER a través de Whisper.
   **中等。**Usando OpenVoice v2 克隆你自己的声音──测量参考与克隆之间的SECS──通过 语测 CER──
3. **Hard.**Aplicar el signo de agua SilentCipher a 20 clones, ejecutarlos a través de 128 kbps MP3 codificación + decodificación, detectar la carga útil.
   **困难。**Para 20 aplicaciones en el mundo de la tecnología SilentCipher, por 128 kbps MP3 编码+解码,检测载荷――报告比特准确率──

> **【中文解读】**En el lenguaje de los términos "Lo que la gente dice" vs "Lo que realmente significa" se distingue entre el lenguaje diario y la definición técnica de significado.


## Términos clave .

| Term | What people say | What it actually means |
|------|-----------------|-----------------------|
| Zero-shot clone | 5 seconds is enough | Pretrained model + speaker embedding; no training. |
| PPG | Phonetic posteriorgram | Per-frame ASR posteriors used as language-agnostic content rep. |
| KNN-VC | Nearest-neighbor conversion | Replace each source frame with nearest target-pool frame. |
| Neural codec TTS | VALL-E style | AR model over EnCodec/SoundStream tokens. |
| Watermark | Inaudible signature | Bits embedded in audio, survive re-encode. |
| SECS | Cloning fidelity | Cosine between target and clone speaker embeddings. |
| AASIST | Deepfake detector | Anti-spoof model; detects synthesized speech. |

| 术语 | 人们常说的 | 实际含义 |
|------|-----------|---------|
| 零样本克隆 | 5 秒就够了 | 预训练模型 + 说话人嵌入；无需训练。 |
| PPG | 音素后验图 | 逐帧 ASR 后验，用作语言无关的内容表示。 |
| KNN-VC | 最近邻转换 | 用目标池中最近邻替换每个源帧。 |
| 神经编解码 TTS | VALL-E 风格 | 在 EnCodec/SoundStream token 上的 AR 模型。 |
| 水印 | 不可听签名 | 嵌入音频中的比特，经受重编码。 |
| SECS | 克隆保真度 | 目标与克隆说话人嵌入之间的余弦相似度。 |
| AASIST | 深度伪造检测器 | 反欺诈模型；检测合成语音。 |

> **【中文解读】**延伸阅读 proporciona un alto nivel de recursos para el aprendizaje profundo. Estos artículos y cursos son los referentes clásicos en el campo, adecuados para los lectores que necesitan una comprensión profunda.


## Más Leer más Leer más

- [Chen et al. (2024). F5-TTS](https://arxiv.org/abs/2410.06885) Cloning de código abierto de SOTA con disparos cero.
  Chen 等 (2024). F5-TTS开源 SOTA 零样本克隆──
- [Baevski et al. / Microsoft (2023). VALL-E](https://arxiv.org/abs/2301.02111)y [VALL-E 2 (2024)](https://arxiv.org/abs/2406.05370) TTS de codec neuronal.
  Baevski 等 / 微软 (2023). VALL-E 和 VALL-E 2(2024)  神经编解码 TTS──
- [Qian et al. (2019). AutoVC](https://arxiv.org/abs/1905.05879) conversión de voz basada en desentrañación.
  Qian 等 (2019). AutoVC 基于解的语音转换──
- [Baas, Waubert de Puiseau, Kamper (2023). KNN-VC](https://arxiv.org/abs/2305.18975) VC basado en la recuperación.
  Baas, Waubert de Puiseau, Kamper (2023). KNN-VC 基于检索的语音转换──
- [SilentCipher (2024) — Audio Watermarking](https://github.com/sony/silentcipher) Marca de agua de audio de 32 bits lista para producción.
  SilentCipher ((2024) 音频水印生产可用 32 位音频水印。
- [ASVspoof 2025 results](https://www.asvspoof.org/) detector vs sintetizador carrera de armamento, actualizada en 2026.
  ASVspoof 2025 结果检测器 vs 合成器军备竞赛,2026 年更新──

> **【中文解读】**延伸阅读 proporciona recursos de alta calidad para el aprendizaje profundo, incluyendo artículos, tutorials y herramientas.

