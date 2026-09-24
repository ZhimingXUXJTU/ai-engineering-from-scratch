# Text-to-Speech (TTS)  De Tacotron a F5 y Kokoro 语音合成  De Tacotron a F5 y Kokoro

> ASR inverte el habla al texto; TTS inverte el texto al habla. La pila 2026 está compuesta por tres partes: texto → tokens, tokens → mel, mel → waveform. Cada parte tiene un modelo predeterminado que se ajusta a una computadora portátil.

> **【中文解读】**ASR Colocar el lenguaje en el lenguaje, TTS Colocar el lenguaje en el lenguaje.

> **【拓展：TTS 的应用】**TTS es una tecnología central de la tecnología TTS, que se utiliza en el desarrollo de la tecnología de la comunicación digital.

**Type:** Build | **类型:** 构建
**Languages:** Python | **语言:** Python
**Prerequisites:** Phase 6 · 02 (Spectrograms & Mel), Phase 5 · 09 (Seq2Seq), Phase 7 · 05 (Full Transformer) | **前置知识:** 阶段 6 · 02（频谱图与 Mel），阶段 5 · 09（Seq2Seq），阶段 7 · 05（完整 Transformer）
**Time:** ~75 minutes | **预计用时:** ~75 分钟

## El problema es la introducción del problema

Tienes una cadena: "Por favor, recuerda que regar las plantas a las 6 pm". Necesitas un clip de audio de 3 segundos que suene natural, tenga una prosodia correcta (pausas, estrés), pronuncie "plantes" con la vocales correctas y se ejecuta en menos de 300 ms en una CPU para un asistente de voz en vivo. También necesitas intercambiar voces, manejar entradas con código cambiado ("recordame a las 6 pm, daijoubu?"), y no avergonzarte por los nombres.

> Usted tiene una字符串:"Por favor, recuerde que rege las plantas a las 6 p.m. " Usted necesita un段 3 segundos de audio, escucha la naturaleza,律正确(停顿、重音), "plantes" de los "元音发音正确, y en la CPU arriba no hasta 300 ms, 就能运行以用于实时语音助手──你还需要切换声音、处理混合语言输入("Recuerde a las 6 p.m., daijoubu?"),且不能在人名上出错──

> **【中文解读】**La pregunta planteada en este capítulo es: ¿cómo entender y aplicar correctamente esta tecnología en la ingeniería real? Comprender el contexto de la cuestión ayuda a comprender los puntos clave de decisión del tipo de selección técnica. En los sistemas de IA reales, el tipo de selección técnica errónea suele ser más alto que el costo de error de la realización de detalles.

Los oleoductos modernos TTS se ven así:

> 现代 TTS 流水线如下:

1. **Text frontend.**Normaliza el texto (fechas, números, correos electrónicos), convierta en fonemas o fichas de palabras, predica las características de prosodia.
   **文本前端。**归一化文本(日期、数字、邮箱),转换为音素或子词代币,预测律特征──
2. **Acoustic model.**Texto → espectrograma mel. Tacotron 2 (2017), FastSpeech 2 (2020), VITS (2021), F5-TTS (2024), Kokoro (2024).
   **声学模型。**文本 → Mel 频谱图──Tacotron 2(2017)、FastSpeech 2(2020)、VITS(2021)、F5-TTS(2024)、Kokoro(2024)。
3. **Vocoder.**Mel → forma de onda. WaveNet (2016), WaveRNN, HiFi-GAN (2020), BigVGAN (2022), vocoders de códec neural en 2024+.
   **声码器。**Mel → 波形──WaveNet(2016)、WaveRNN、HiFi-GAN(2020)、BigVGAN(2022)、2024+ 的神经编解码声码器──

En 2026 el vocalista acústico + vocoder se desdivide con modelos de difusión de extremo a extremo y de coincidencia de flujo.

> En 2026, con la aparición de un modelo de propagación y de flujo de la línea de juego, los límites del modelo sonoro + el codor sonos se vuelven más confusos.

## El concepto central.

> **【中文解读】**Este capítulo presenta los conceptos y teorías básicos. La comprensión de estos conceptos es el prerrequisito de la realización posterior de la actividad, y también el conocimiento de los puntos de alta frecuencia de la entrevista y la práctica de la ingeniería.


![Tacotron, FastSpeech, VITS, F5/Kokoro side-by-side](../assets/tts.svg)

**Tacotron 2 (2017).**Seq2seq: car-embedding → BiLSTM encoder → atención sensible a la ubicación → autoregressive LSTM decoder emite marcos mel. lento (AR), oscilante en texto largo.

> **Tacotron 2（2017）。**Seq2seq:字符嵌入 → BiLSTM 编码器 → 位置敏感注意力 → 自归 LSTM 解码器输出 mel ──慢(AR),长文本不稳定── todavía se cita为基线──

**FastSpeech 2 (2020).**No autorregresivista. El predictor de duración saca cuántos marcos mel cada fonema obtiene. 1-pasar, 10 veces más rápido que Tacotron. pierde algo de naturalidad (alineamiento monótono) pero navega por todas partes.

> **FastSpeech 2（2020）。**No se vuelve a la naturaleza. Pero en todas partes están en uso.

**VITS (2021).**En conjunto, el programa de entrenamiento de código + duración basada en flujo + vocoder HiFi-GAN de extremo a extremo con inferencia variativa. Alta calidad, modelo único. TTS de código abierto dominante 20222024. Variantes: YourTTS (multiplicador de tiro cero), XTTS v2 (2024, Coqui).

> **VITS（2021）。**联合训练编码器 + 基流的时长预测 + HiFi-GAN 声码器端到端,使用变分推断。高质量,单模型──2022-2024年主导开源 TTS──变体:YourTTS(多说话人零样本)、XTTS v2(2024,Coqui)──

**F5-TTS (2024).**Transformador de difusión sobre la coincidencia de flujo. Prósodia natural, clonación de voz de tiro cero con 5 segundos de audio de referencia.

> **F5-TTS（2024）。**基于流匹配的扩散变压器──自然律,5 秒参考音频零样本声音克隆──2026年开源 TTS 排行榜榜榜首──3.35亿参数──

**Kokoro (2024).**Pequeño (82M), ejecutado por CPU, mejor TTS de inglés para uso en tiempo real.

> **Kokoro（2024）。**Por ejemplo, el sistema operativo de Apache 2.0 puede funcionar en la CPU, con el mejor tiempo real en inglés TTS.

**OpenAI TTS-1-HD, ElevenLabs v2.5, Google Chirp-3.**El estado comercial de la técnica. ElevenLabs v2.5 etiquetas de emoción ("[susurrado]", "[risas]") y voces de personajes dominan la producción de audiolibros en 2026.

> **OpenAI TTS-1-HD、ElevenLabs v2.5、Google Chirp-3。**商业 SOTA──ElevenLabs v2.5 的情感标签("[susurrido]"、"[risas]")和角色声音主导 2026 年有声书制作──

### Evolución del vocoder

> ### 声码器演进

| Era | Vocoder | Latency | Quality |
|-----|---------|---------|---------|
| 2016 | WaveNet | offline only | SOTA at release |
| 2018 | WaveRNN | ~realtime | good |
| 2020 | HiFi-GAN | 100× realtime | near-human |
| 2022 | BigVGAN | 50× realtime | generalizes across speakers/langs |
| 2024 | SNAC, DAC (neural codecs) | integrated with AR models | discrete tokens, bit-efficient |

| 时代 | 声码器 | 延迟 | 质量 |
|------|--------|------|------|
| 2016 | WaveNet | 仅离线 | 发布时 SOTA |
| 2018 | WaveRNN | 约实时 | 良好 |
| 2020 | HiFi-GAN | 100× 实时 | 接近人类 |
| 2022 | BigVGAN | 50× 实时 | 跨说话人/语言泛化 |
| 2024 | SNAC, DAC（神经编解码器） | 与 AR 模型集成 | 离散 token，比特高效 |

Para 2026, la mayoría de los modelos "TTS" son de extremo a extremo desde el texto a la forma de onda; el espectrograma mel es una representación interna.

> Para 2026, la mayoría de los modelos "TTS" son de texto a forma de onda; el gráfico de frecuencia es el representativo interno.

### Evaluación

> ###  evaluación

- **MOS (Mean Opinion Score).**Escala de 1 a 5, de fuente multitudinaria, todavía el estándar de oro, dolorosamente lento.
  **MOS（平均意见分）。**1-5 分量表,众包── sigue siendo el estándar de oro; velocidad dolorosamente lenta──
- **CMOS (Comparative MOS).**Preferencia A-vs-B. Intervalos de confianza más estrechos por anotación.
  **CMOS（比较 MOS）。**A-vs-B  preferencia. Cada marca de la posición de la zona es más estrecha.
- **UTMOS, DNSMOS.**Predictores neuronales de MOS sin referencias, usados para los rankings.
  **UTMOS、DNSMOS。**无参考神经 MOS 预测器──用于排行榜──
- **CER (Character Error Rate) via ASR.**Ejecutar la salida TTS a través de Whisper, calcular CER contra el texto de entrada.
  **CER（字符错误率）通过 ASR。**Para que el TTS pueda ser emitido por susurros, se debe utilizar el código de código de entrada.
- **SECS (Speaker Embedding Cosine Similarity).**La calidad de clonación de voz.
  **SECS（说话人嵌入余弦相似度）。**声克隆质量── también se puede decir que el

Números 2026 de limpieza de ensayo LibriTTS:

> 2026 años LibriTTS prueba-limpio 上的数字:

| Model | UTMOS | CER (via Whisper) | Size |
|-------|-------|-------------------|------|
| Ground truth | 4.08 | 1.2% | — |
| F5-TTS | 3.95 | 2.1% | 335M |
| XTTS v2 | 3.81 | 3.5% | 470M |
| VITS | 3.62 | 3.1% | 25M |
| Kokoro v0.19 | 3.87 | 1.8% | 82M |
| Parler-TTS Large | 3.76 | 2.8% | 2.3B |

| 模型 | UTMOS | CER（通过 Whisper） | 大小 |
|------|-------|---------------------|------|
| 真实音频 | 4.08 | 1.2% | — |
| F5-TTS | 3.95 | 2.1% | 3.35 亿 |
| XTTS v2 | 3.81 | 3.5% | 4.7 亿 |
| VITS | 3.62 | 3.1% | 2500 万 |
| Kokoro v0.19 | 3.87 | 1.8% | 8200 万 |
| Parler-TTS Large | 3.76 | 2.8% | 23 亿 |

> **【中文解读】**Este capítulo a través del código de la implementación de algoritmos centrales de cero. Este método "desde cero" puede ayudar a entender el principio detrás del marco, no se encuentra en la caja negra cuando se encuentran problemas.

> **【拓展：语音 AI 的产品化】**La tecnología de voz se enfrenta a un desafío único en la productorización: diferentes voces, ruidos de contexto, remota recogida, muchos hablar, etc.

> **【拓展：多语言语音技术】**Las características de los idiomas de todo el mundo son muy diferentes: el sonido de los idiomas de todo el mundo (como el chino) es alto, el lenguaje de bajo recurso es poco capacitado.




## Construye y realiza.
```figure
sp-tts-stack
```

## Construye el mismo

### Paso 1: fonemizar la entrada

```python
from phonemizer import phonemize
ph = phonemize("Hello world", language="en-us", backend="espeak")
# 'həloʊ wɜːld'
```

Los fonemas son el puente universal. Evite alimentar texto crudo a cualquier cosa por debajo del nivel de calidad de VITS.

> 音素是通用桥梁──避免将原始文本输入到VITS 级别以下的任何模型──

### Paso 2: ejecutar Kokoro (2026 CPU por defecto)

```python
from kokoro import KPipeline
tts = KPipeline(lang_code="a")  # "a" = American English
audio, sr = tts("Please remind me to water the plants at 6 pm.", voice="af_bella")
# audio: float32 tensor, sr=24000
```

Se ejecuta fuera de línea, un solo archivo, 82M params.

> 离线运行,单文件, 82 millones de parámetros

### Paso 3: ejecutar F5-TTS con clonación de voz

```python
from f5_tts.api import F5TTS
tts = F5TTS()
wav = tts.infer(
    ref_file="my_voice_5s.wav",
    ref_text="The quick brown fox jumps over the lazy dog.",
    gen_text="Please remind me to water the plants.",
)
```

Pasar un clip de referencia de 5 segundos + su transcripción; F5 clona prosodia y timbre.

> 传入 5 秒参考音频 + 其转录文本; F5 克隆律和音色──

### Paso 4: Vocoder HiFi-GAN desde cero

Demasiado grande para encajar en un guión de tutoriales, pero la forma es:

```python
class HiFiGAN(nn.Module):
    def __init__(self, mel_channels=80, upsample_rates=[8, 8, 2, 2]):
        super().__init__()
        # 4 upsample blocks, total 256x to go from mel-rate to audio-rate
        ...
    def forward(self, mel):
        return self.blocks(mel)  # -> waveform
```

Formación: adversarial (discriminador en ventanas cortas) + pérdida de reconstrucción del espectrograma mel + pérdida de coincidencia de características.`hifi-gan`¿Qué es esto?

> 训练:对抗式(短窗口判别器) + Mel 频谱图重建损失 + 特征匹配损失──已商品化使用 `hifi-gan`仓库或 nvidia-NeMo 的预训练检查点──

### Paso 5: el conjunto completo de tuberías (pseudocodo)

```python
text = "Please remind me at 6 pm."
phones = phonemize(text)
mel = acoustic_model(phones, speaker=alice)      # [T, 80]
wav = vocoder(mel)                                # [T * 256]
soundfile.write("out.wav", wav, 24000)
```

> **【中文解读】**Este capítulo muestra cómo utilizar un marco maduro (como PyTorch、HuggingFace, etc.) para aplicar rápidamente esta tecnología. En los proyectos reales, se realiza con prioridad el uso de un marco experimentado, se pueden reducir errores y mejorar la eficiencia de desarrollo.





> **【拓展：语音与情感计算】**语音 no sólo transmite información escrita, también lleva una rica cantidad de señales emocionales (en inglés: voice signal) 语调、语速、音高变化) 情感语音识别 (en inglés: speech emotion recognition, SER) 语音 no solo transmite información escrita, sino que también lleva una gran cantidad de señales emocionales (en inglés: voice signal). 语音 tiene una amplia aplicación en el campo de la evaluación de calidad de los clientes, la vigilancia de la salud mental, la educación inteligente, etc.  Los modelos actuales de SOTA se basan en modelos de entrenamiento de las ondas 2vec 2.0 o HuBERT.

## Usalo con el marco de ejecución

La pila de 2026:

> Tecnología de 2026:

| Situation | Pick |
|-----------|------|
| Real-time English voice assistant | Kokoro (CPU) or XTTS v2 (GPU) |
| Voice cloning from 5 s reference | F5-TTS |
| Commercial character voices | ElevenLabs v2.5 |
| Audiobook narration | ElevenLabs v2.5 or XTTS v2 + fine-tune |
| Low-resource language | Train VITS on 5–20 h target-lang data |
| Expressive / emotion tags | ElevenLabs v2.5 or StyleTTS 2 fine-tune |

| 场景 | 选择 |
|------|------|
| 实时英文语音助手 | Kokoro（CPU）或 XTTS v2（GPU） |
| 5 秒参考音频声音克隆 | F5-TTS |
| 商业角色声音 | ElevenLabs v2.5 |
| 有声书朗读 | ElevenLabs v2.5 或 XTTS v2 + 微调 |
| 低资源语言 | 在 5-20 小时目标语言数据上训练 VITS |
| 表达性 / 情感标签 | ElevenLabs v2.5 或 StyleTTS 2 微调 |

Líder de código abierto a partir de 2026: **F5-TTS for quality, Kokoro for efficiency**No llegues a Tacotron a menos que seas un historiador.

> 2026 años de liderazgo abierto:**F5-TTS 追求质量，Kokoro 追求效率**❖ A menos que seas un historiador, o bien no uses Tacotron.



## Las trampas

> 常见陷

- **No text normalizer.**"Dr. Smith" se lee como "Doctor" o "Drive"? "2026" como "veinte veintiséis" o "dos cero dos seis"?
  **没有文本归一化器。**¿Dr. Smith es el "Doctor" o el "Drive"? 2026 ¿Es el "Vinte veintiséis" o el "Dos cero dos seis"?
- **OOV proper nouns.**"Ghumare" → "ghyu-mair"? Envía un modelo de fallback grapheme-to-phoneme para tokens desconocidos.
  **OOV 专有名词。**¿Ghumare → Gyu-mair?
- **Clipping.**La salida del vocoder rara vez se hace, pero la desajuste de escalación de mel en la inferencia puede superar ±1.0.`np.clip(wav, -1, 1)`¿ Qué ?
  **削波。**声码器输出很少削波,但推理时 Mel 缩放不匹配可能超出 ±1.0──始终使用 `np.clip(wav, -1, 1)`¿Qué es eso?
- **Sample-rate mismatch.**Kokoro emitirá 24 kHz; su tubería aguas abajo espera 16 kHz → replantear o obtener alias.
  **采样率不匹配。**Kokoro 输出 24 kHz; 你的下游流水线期望 16 kHz → 重采样否则产生混叠──

> **【中文解读】**Este capítulo se centra en cómo se puede implementar el modelo como producto disponible. Desde el modelo original hasta el sistema de producción, se deben considerar múltiples dimensiones de optimización de rendimiento, tratamiento de errores, control, etc.


## Envíe el producto .

Salvo como`outputs/skill-tts-designer.md`Diseñar una tubería TTS para una determinada voz, latencia y lenguaje objetivo.

> 保存为                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           `outputs/skill-tts-designer.md`◊ para un determinado sonido、延迟和语言目标设计 TTS 流水线──

## Los ejercicios.

1. **Easy.**- ¿ Qué ?`code/main.py`Construye un diccionario de fonemas a partir de una vocabulario de juguete, estima la duración por fonema e imprime un calendario falso de "mel".
   **简单。**运行                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           `code/main.py`∼ desde el lenguaje de los juguetes, la construcción de un lenguaje, la estimación de cada lenguaje, la impresión de un falso "mel" plan─
2. **Medium.**Instala Kokoro, sintetiza la misma oración en voz.`af_bella`y `am_adam`Comparar las duradas de audio y la calidad subjetiva.
   **中等。**Installación Kokoro, usar `af_bella`Y `am_adam`音合成同一句话──比较音频时长和主观质量──
3. **Hard.**Graba un clip de referencia de 5 segundos de ti mismo, usa F5-TTS para clonarlo, informe SECS entre la referencia y la salida clonada.
   **困难。**录制一段 5 segundos de su propia referencia 频频──Utiliza F5-TTS 克隆──报告参考与克隆输出之间的SECS──

> **【中文解读】**En el lenguaje de los términos "Lo que la gente dice" vs "Lo que realmente significa" se distingue entre el lenguaje diario y la definición técnica de significado.


## Términos clave .

| Term | What people say | What it actually means |
|------|-----------------|-----------------------|
| Phoneme | Sound unit | Abstract sound class; 39 in English (ARPABet). |
| Duration predictor | How long each phoneme lasts | Non-AR model output; integer frames per phoneme. |
| Vocoder | Mel → waveform | Neural net mapping mel-spec to raw samples. |
| HiFi-GAN | Standard vocoder | GAN-based; dominant 2020–2024. |
| MOS | Subjective quality | 1–5 mean opinion score from human raters. |
| SECS | Voice-clone metric | Cosine similarity between target and output speaker embedding. |
| F5-TTS | 2024 open-source SOTA | Flow-matching diffusion; zero-shot cloning. |
| Kokoro | CPU English leader | 82M-param model, Apache 2.0. |

| 术语 | 人们常说的 | 实际含义 |
|------|-----------|---------|
| 音素 | 声音单位 | 抽象声音类别；英文有 39 个（ARPABet）。 |
| 时长预测器 | 每个音素持续多久 | 非自回归模型输出；每个音素的整数帧数。 |
| 声码器 | Mel → 波形 | 将 mel 频谱映射为原始采样的神经网络。 |
| HiFi-GAN | 标准声码器 | 基于 GAN；2020-2024 年主导。 |
| MOS | 主观质量 | 人工评分员的 1-5 平均意见分。 |
| SECS | 声音克隆指标 | 目标与输出说话人嵌入之间的余弦相似度。 |
| F5-TTS | 2024 开源 SOTA | 流匹配扩散；零样本克隆。 |
| Kokoro | CPU 英文领导者 | 8200 万参数模型，Apache 2.0。 |

> **【中文解读】**延伸阅读 proporciona un alto nivel de recursos para el aprendizaje profundo. Estos artículos y cursos son los referentes clásicos en el campo, adecuados para los lectores que necesitan una comprensión profunda.


## Más Leer más Leer más

- [Shen et al. (2017). Tacotron 2](https://arxiv.org/abs/1712.05884) el nivel de base de seguimiento.
  Shen 等 (2017). Tacotron 2seq2seq 基线。
- [Kim, Kong, Son (2021). VITS](https://arxiv.org/abs/2106.06103) basado en flujo de extremo a extremo.
  Kim, Kong, Son (2021). VITS端到端基于流的模型──
- [Chen et al. (2024). F5-TTS](https://arxiv.org/abs/2410.06885) SOTA de código abierto actual.
  Chen 等 (2024). F5-TTS当前开源SOTA──
- [Kong, Kim, Bae (2020). HiFi-GAN](https://arxiv.org/abs/2010.05646) el vocoder que todavía se envía en 2026.
  Kong, Kim, Bae (2020). HiFi-GAN2026 año todavía en uso
- [Kokoro-82M on HuggingFace](https://huggingface.co/hexgrad/Kokoro-82M) 2024 TTS inglés compatible con la CPU.
  Kokoro-82M 在 HuggingFace 上2024年 CPU 友好的英文 TTS──

> **【中文解读】**延伸阅读 proporciona recursos de alta calidad para el aprendizaje profundo, incluyendo artículos, tutorials y herramientas.

