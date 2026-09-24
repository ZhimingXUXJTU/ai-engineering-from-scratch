# Susurro  Arquitectura y ajuste fino  Susurro  Arquitectura y micro-modución

> Whisper es un transformer de ventana de 30 segundos, entrenado en 680 mil horas de pares de audio-texto multilingües con poca supervisión. Una arquitectura, múltiples tareas, robusta en 99 idiomas.

> **【中文解读】**Whisper es un transformer de 30 segundos en una ventana de 30 segundos, en 680.000 horas en más de un idioma.

> **【拓展：Whisper 的生态】**El susurro 衍生了 el susurro.cpp(本地部署)、Faster-Whisper(CTtranslate2 加速)、WhisperX(词级时间)、Bloomsbury(实时流式)等工具链,是语音识别工业部署的事实标准──

**Type:** Build | **类型:** 构建
**Languages:** Python | **语言:** Python
**Prerequisites:** Phase 6 · 04 (ASR), Phase 5 · 10 (Attention), Phase 7 · 05 (Full Transformer) | **前置知识:** 阶段 6 · 04（ASR），阶段 5 · 10（注意力机制），阶段 7 · 05（完整 Transformer）
**Time:** ~75 minutes | **预计用时:** ~75 分钟

## El problema es la introducción del problema

Whisper, lanzado por OpenAI en septiembre de 2022, fue el primer modelo ASR en ser enviado como un producto básico: pegar audio, obtener texto, 99 idiomas, robusto al ruido, se ejecuta en una computadora portátil. Para 2024 OpenAI había enviado variantes Large-v3 y Turbo; para 2026, Whisper es la línea de base predeterminada para todo, desde la transcripción de podcast hasta asistentes de voz hasta subtítulos de YouTube.

> Whisper fue lanzado por OpenAI en septiembre de 2022, es el primer modelo de ASR publicado como producto general: adhesivo, audio, 99 idiomas, anti ruido, puede funcionar en el ordenador.

> **【中文解读】**La pregunta planteada en este capítulo es: ¿cómo entender y aplicar correctamente esta tecnología en la ingeniería real? Comprender el contexto de la cuestión ayuda a comprender los puntos clave de decisión del tipo de selección técnica. En los sistemas de IA reales, el tipo de selección técnica errónea suele ser más alto que el costo de error de la realización de detalles.

Pero Whisper no es un pipeline que se puede tratar como una caja negra para siempre.

> Pero el susurro no es el flujo de agua que se puede usar en la caja negra. El desvío de campo destruye el término técnico.

1. Lo que realmente es dentro.
   En su interior es la estructura.
2. Cómo darlo en pedazos, en streaming o en formato largo correctamente.
   ¿Cómo se puede darle correctamente un bloque de entrada?
3. ¿Cuándo y cómo ajustar?
   ¿Cuándo se hace la diferencia y cómo se hace la diferencia?

> **【中文解读】**Este capítulo presenta los conceptos y teorías básicos. La comprensión de estos conceptos es el prerrequisito de la realización posterior de la actividad, y también el conocimiento de los puntos de alta frecuencia de la entrevista y la práctica de la ingeniería.


## El concepto central.

![Whisper encoder-decoder, tasks, chunked inference, fine-tune](../assets/whisper.svg)

**Architecture.**El transformer estándar codificador-decodificador.

> **架构。**标准 Transformer 编码器-解码器──

- Entrada: Espectograma log-mel de 30 segundos, 80 mels, 10 ms hop → 3000 cuadros.
  输入30 秒 log-mail 频谱图,80 mels,10 ms 步长 → 3000 ──短片段零填充,长片段分块──
- Encodrador: muestra de la con-descisión (fase 2) + `N`Bloques de transformador para grandes v3: 32 capas, 1280-dim, 20 cabezas.
  编码器:卷积下采样(步幅 2) + `N`个 Transformer 块──Large-v3:32 层,1280 维,20 头──
- Descriptor:`N`bloques de transformador con auto-atn causal + atn cruzado a salida de codificador. del mismo tamaño que el codificador.
  解码器:`N`个带因果自注意力 + Transformer 块──与编码器同大小──
- Resultado: Tokens BPE sobre una vocabulario de 51.865 tokens.
  输出:51,865 token 词表上的 BPE token──

El Large-v3 tiene parámetros de 1.55B. Turbo utiliza un decodificador de 4 capas (desde 32), reduciendo la latencia 8x con un golpe WER <1% .

> El mayor número de V3 tiene 15,5 mil millones de parámetros.

**The prompt format.**Whisper es un modelo multitarea dirigido por tokens especiales en el descifrador de instrucciones:

> **提示格式。**Whisper es un modelo de múltiples tareas, a través de un token especial en el que se controla:

```
<|startoftranscript|><|en|><|transcribe|><|notimestamps|> Hello world.<|endoftext|>
```

- `<|en|>` etiqueta de lenguaje; obliga el comportamiento traducción-versus-transcripción.
  `<|en|>` 语言标签; 强制翻译或转录行为──
- `<|transcribe|>`o `<|translate|>` traducir la salida en inglés de cualquier entrada de idioma, o literalmente.
  `<|transcribe|>`O `<|translate|>` From any language输入翻译为英文输出,或逐字转录──
- `<|notimestamps|>` saltar las temporadas de nivel de palabra (más rápido).
  `<|notimestamps|>` 跳过词级时间(更快)。

El prompt es lo que permite a un modelo hacer muchas tareas.`<|en|>`¿ Qué ?`<|fr|>`y transcribe francés.

> 提示就是让一个模型完成多种任务的关键.`<|en|>`改为     cambió por`<|fr|>`En el transcurso de la historia.

**30-second window.**Todo está fijado a 30 segundos. Los clips más largos necesitan ser recheados; los clips más cortos están empolgados. Windows no se transmiten de forma nativa.

> **30 秒窗口。**Todo se realiza en 30 segundos. Los sonidos más largos necesitan ser reabastecidos. Los sonidos más cortos necesitan ser reabastecidos.

**Log-mel normalization.** `(log_mel - mean) / std`donde las estadísticas provienen del propio cuerpo de entrenamiento de Whisper.`whisper.audio.log_mel_spectrogram`), no `librosa.feature.melspectrogram`¿ Qué ?

> **Log-mel 归一化。** `(log_mel - mean) / std`, de los cuales la estadística proviene de Whisper  propio entrenamiento语料──你*必须*使用 Whisper 的预处理(`whisper.audio.log_mel_spectrogram`), en lugar de `librosa.feature.melspectrogram`¿Qué es eso?

### Variantes en 2026

> ### Cambios en el año 2026

| Variant | Params | Latency (A100) | WER (LibriSpeech-clean) |
|---------|--------|----------------|------------------------|
| Tiny | 39M | 1× realtime | 5.4% |
| Base | 74M | 1× | 4.1% |
| Small | 244M | 1× | 3.0% |
| Medium | 769M | 1× | 2.7% |
| Large-v3 | 1.55B | 2× | 1.8% |
| Large-v3-turbo | 809M | 8× | 1.58% |
| Whisper-Streaming (2024) | 1.55B | streaming | 2.0% |

| 变体 | 参数量 | 延迟（A100） | WER（LibriSpeech-clean） |
|------|--------|--------------|-------------------------|
| Tiny | 3900 万 | 1× 实时 | 5.4% |
| Base | 7400 万 | 1× | 4.1% |
| Small | 2.44 亿 | 1× | 3.0% |
| Medium | 7.69 亿 | 1× | 2.7% |
| Large-v3 | 15.5 亿 | 2× | 1.8% |
| Large-v3-turbo | 8.09 亿 | 8× | 1.58% |
| Whisper-Streaming（2024） | 15.5 亿 | 流式 | 2.0% |

### Arreglamiento

> ### 微调

Flujo de trabajo canónico en 2026:

> El proceso estándar para 2026:

1. Recoger 10100 horas de audio del dominio objetivo con transcripciones alineadas.
   收集 10-100 小时目标领域的音频及对应转录文本──
2. - ¿ Qué ?`transformers.Seq2SeqTrainer`con`generate_with_loss`- ¿Qué?
   Uso `transformers.Seq2SeqTrainer`Y `generate_with_loss`De acuerdo con el equipo de la compañía.
3. Eficiencia parámetrica: LoRA en `q_proj`¿ Qué ?`k_proj`¿ Qué ?`v_proj`de capas de atención reduce la memoria de la GPU 4× con < 0,3 costo WER.
   参数高效: en el nivel de atención `q_proj`¿Qué es esto?`k_proj`¿Qué es esto?`v_proj`上使用Lora,GPU内存降低4倍,WER 损失 <0.3──
4. Congelar el codificador si tiene < 10 horas. Sólo sintonizar el decodificador.
   Si los datos no alcanzan los 10 minutos, sólo se puede modificar el código.
5. Utilice el propio tokenizer y formato de solicitud de Whisper; nunca cambie los tokenizadores.
   Use Whisper  tu propio tokenizer 和提示格式; Nunca sustituir el tokenizer。

Resultados comunitarios: ajuste fino Mediano en 20 horas de dictado médico disminuye el WER de 12% a 4,5% en el vocabulario médico.

> 社区结果: 在 20 小时医疗口述上微调 Medium,医疗词汇 WER de 12% 降至4.5%── 在 4 小时冰岛语上微调 Turbo, WER de 18% 降至6%──

> **【拓展：语音 AI 的产品化】**La tecnología de voz se enfrenta a un desafío único en la productorización: diferentes voces, ruidos de contexto, remota recogida, muchos hablar, etc.

> **【拓展：多语言语音技术】**Las características de los idiomas de todo el mundo son muy diferentes: el sonido de los idiomas de todo el mundo (como el chino) es alto, el lenguaje de bajo recurso es poco capacitado.



## Construye y realiza.

> **【中文解读】**Este capítulo a través del código de la implementación de algoritmos centrales de cero. Este método "desde cero" puede ayudar a entender el principio detrás del marco, no se encuentra en la caja negra cuando se encuentran problemas.

```figure
sp-asr-attention
```

## Construye el mismo

### Paso 1: ejecutar el susurro fuera de la caja

```python
import whisper
model = whisper.load_model("large-v3-turbo")
result = model.transcribe(
    "clip.wav",
    language="en",
    task="transcribe",
    temperature=0.0,
    condition_on_previous_text=False,  # prevents runaway repetition
)
print(result["text"])
for seg in result["segments"]:
    print(f"[{seg['start']:.2f}–{seg['end']:.2f}] {seg['text']}")
```

Las diferencias clave que siempre debe anotar: `temperature=0.0`(muestreo de valores por defecto a 0,0 → 0,2 → 0,4 ... cadena de retroceso), `condition_on_previous_text=False`(previene el problema de alucinación en cascada), y `no_speech_threshold=0.6`(detección de silencio).

> Usted siempre debe cubrir los valores clave:`temperature=0.0`(采样默认为 0.0 → 0.2 → 0.4 ... 回退链)`condition_on_previous_text=False`(prevenir los problemas de nivel de la sociedad) y `no_speech_threshold=0.6`(静音检测)

### Paso 2: forma larga en pedazos

```python
# whisperx is the 2026 reference for long-form with word-level timestamps
import whisperx
model = whisperx.load_model("large-v3-turbo", device="cuda", compute_type="float16")
segments = model.transcribe("1hour.mp3", batch_size=16, chunk_size=30)
```

WhisperX añade (1) Silero VAD gateing, (2) alineación a nivel de palabras a través de wav2vec 2.0, (3) diarización a través de `pyannote.audio`El caballo de trabajo 2026 para la transcripción de producción.

> WhisperX 添加了 (1) Silero VAD 门控,(2) 通过 wav2vec 2.0 实现词级对齐,(3) 通过 `pyannote.audio`实现说话人分离──2026年生产转录的主力工具──

### Paso 3: ajuste a la perfección con LoRA

```python
from transformers import WhisperForConditionalGeneration, WhisperProcessor
from peft import LoraConfig, get_peft_model

model = WhisperForConditionalGeneration.from_pretrained("openai/whisper-large-v3-turbo")
lora = LoraConfig(
    r=16, lora_alpha=32, target_modules=["q_proj", "v_proj"],
    lora_dropout=0.1, bias="none", task_type="SEQ_2_SEQ_LM",
)
model = get_peft_model(model, lora)
# model.print_trainable_parameters()  -> ~3M trainable / 809M total
```

Luego el bucle de entrenadores estándar, un punto de control cada 1000 pasos, evalúa con WER el tiempo de espera.

> Luego el entrenador estándar  entrenamiento ciclo ⋅ cada 1000 pasos de conservación de los puntos de control ⋅ en el abandono de la colección ⋅ evaluación WER ⋅

### Paso 4: inspeccionar lo que cada capa aprende

```python
# Grab cross-attention weights during decode to see what the decoder attends to.
with torch.inference_mode():
    out = model.generate(
        input_features=features,
        return_dict_in_generate=True,
        output_attentions=True,
    )
# out.cross_attentions: layer × head × step × src_len
```

> **【中文解读】**Este capítulo muestra cómo utilizar un marco maduro (como PyTorch、HuggingFace, etc.) para aplicar rápidamente esta tecnología. En los proyectos reales, se realiza con prioridad el uso de un marco experimentado, se pueden reducir errores y mejorar la eficiencia de desarrollo.


Visualice con una mapa de calor  verá la alineación diagonal a medida que los pasos del decodificador escanean a través de los marcos del codificador. Esa diagonal es la noción de tiempo de palabras de Whisper.

> Usando el calor de la imagen visualizada verás el descifrador paso en paso en el descifrador de la imagen de la línea de frente a la línea de frente a la línea.




> **【拓展：语音与情感计算】**语音 no sólo transmite información escrita, también lleva una rica cantidad de señales emocionales (en inglés: voice signal) 语调、语速、音高变化) 情感语音识别 (en inglés: speech emotion recognition, SER) 语音 no solo transmite información escrita, sino que también lleva una gran cantidad de señales emocionales (en inglés: voice signal). 语音 tiene una amplia aplicación en el campo de la evaluación de calidad de los clientes, la vigilancia de la salud mental, la educación inteligente, etc.  Los modelos actuales de SOTA se basan en modelos de entrenamiento de las ondas 2vec 2.0 o HuBERT.

## Usalo con el marco de ejecución

La pila de 2026:

> Tecnología de 2026:

| Situation | Pick |
|-----------|------|
| General English, offline | Large-v3-turbo via `whisperx` |
| Mobile / edge | Whisper-Tiny quantized (int8) or Moonshine |
| Multilingual long-form | Large-v3 via `whisperx` + diarization |
| Low-resource language | Fine-tune Medium or Turbo with LoRA |
| Streaming (2 s latency) | Whisper-Streaming or Parakeet-TDT |
| Word-level timestamps | WhisperX (forced alignment via wav2vec 2.0) |

| 场景 | 选择 |
|------|------|
| 通用英文、离线 | 通过 `whisperx` 使用 Large-v3-turbo |
| 移动端/边缘设备 | 量化 Whisper-Tiny（int8）或 Moonshine |
| 多语言长音频 | 通过 `whisperx` 使用 Large-v3 + 说话人分离 |
| 低资源语言 | 用 LoRA 微调 Medium 或 Turbo |
| 流式（2 秒延迟） | Whisper-Streaming 或 Parakeet-TDT |
| 词级时间戳 | WhisperX（通过 wav2vec 2.0 强制对齐） |

`faster-whisper`(CTranslate2 backend) es el tiempo de ejecución de inferencia CPU+GPU más rápido en 2026  4x más rápido que la vainilla con salida idéntica.

> `faster-whisper`(CTranslate2 后端) es el CPU + GPU más rápido del año 2026 推理运行时比原版快4倍,输出完全相同──



## Las trampas que todavía se envían en 2026

> 2026 año todavía en la trampa de los culpables

- **Hallucinated text on silence.**El susurro entrenado en los títulos incluye "Gracias por ver!", "Abonéctate!", letras de las canciones.
  **静音上的幻觉文本。**Susurrar en su subtitulo datos sobre el entrenamiento, incluirá "Gracias por ver!"、"Subscribe!"、歌词──调用前务必用 VAD 过──
- **`condition_on_previous_text` cascade.**Una alucinación contamina las ventanas posteriores.`False`a menos que necesites fluidez en pedazos.
  **`condition_on_previous_text` 级联。**Una vez que se haya visto contaminación posterior a la ventana, excepto si se necesita un flujo transversal, se debe establecer`False`¿Qué es eso?
- **Short-clip padding.**Un clip de 2 segundos empolvado a 30 segundos puede alucinar en el silencio posterior.`pad=False`o VAD-gate.
  **短片段填充。**2 segundos de tiempo para llenar hasta 30 segundos puede ocurrir en el final de la sesión.`pad=False`O VAD 过──
- **Wrong mel stats.**Usar los mels de librosa en lugar de los de Whisper produce una salida casi aleatoria.`whisper.audio.log_mel_spectrogram`¿ Qué ?
  **错误的 mel 统计量。**Utiliza la librería de los mels y no el susurro de los resultados casi casual.`whisper.audio.log_mel_spectrogram`¿Qué es eso?

> **【中文解读】**Este capítulo se centra en cómo se puede implementar el modelo como producto disponible. Desde el modelo original hasta el sistema de producción, se deben considerar múltiples dimensiones de optimización de rendimiento, tratamiento de errores, control, etc.


## Envíe el producto .

Salvo como`outputs/skill-whisper-tuner.md`Diseñar un flujo de sintonía o inferencia de Whisper para un dominio determinado.

> 保存为                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           `outputs/skill-whisper-tuner.md`◊ para un determinado campo de diseño

## Los ejercicios.

1. **Easy.**- ¿ Qué ?`code/main.py`Se tokeniza un mensaje de estilo Whisper, calcula los presupuestos de forma decodificada, e imprime el horario de piezas para un clip de 10 minutos.
   **简单。**运行                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           `code/main.py`◊ se trata de un plan de parámetros de un programa de programación de 10 minutos de audio.
2. **Medium.**Instalar`faster-whisper`, transcribir un podcast de 10 minutos, comparar WER con una transcripción humana.`language="auto"`contra forzado `language="en"`¿ Qué ?
   **中等。**Instalación`faster-whisper`, Transcripción 10 minutos de programación, con la traducción artificial comparada con WER.`language="auto"`Con la obligación`language="en"`¿Qué es eso?
3. **Hard.**El uso de HF `datasets`, elegir un idioma con el que Whisper lucha (por ejemplo, Urdu), ajustar mediano con LoRA durante 2 épocas en 2 horas, y informar WER delta.
   **困难。**Uso de HF `datasets`,select a Whisper 困难的语言 (如乌尔都语), en 2 小时数据上使用 LoRA 微调 Medium 2 个时代,报告 WER 差值──

> **【中文解读】**En el lenguaje de los términos "Lo que la gente dice" vs "Lo que realmente significa" se distingue entre el lenguaje diario y la definición técnica de significado.


## Términos clave .

| Term | What people say | What it actually means |
|------|-----------------|-----------------------|
| 30-sec window | Whisper's limit | Hard input cap; chunk longer audio. |
| SOT | Start-of-transcript | `<\|startoftranscript\|>` kicks off the decoder prompt. |
| Timestamps token | Temporal alignment | Every 0.02 s offset is a special token in the 51k vocab. |
| Turbo | The fast variant | 4-decoder layers, 8× faster, <1% WER regression. |
| WhisperX | The long-form wrapper | VAD + Whisper + wav2vec alignment + diarization. |
| LoRA fine-tune | Efficient tuning | Add low-rank adapters to attention; train ~0.3% of params. |
| Hallucination | The silent failure | Whisper produces fluent English from noise/silence. |

| 术语 | 人们常说的 | 实际含义 |
|------|-----------|---------|
| 30 秒窗口 | Whisper 的限制 | 硬性输入上限；更长音频需分块。 |
| SOT | 转录开始 | `<\|startoftranscript\|>` 启动解码器提示。 |
| 时间戳 token | 时间对齐 | 每 0.02 秒偏移是 51k 词表中的特殊 token。 |
| Turbo | 快速变体 | 4 层解码器，快 8 倍，WER 回退 <1%。 |
| WhisperX | 长音频封装 | VAD + Whisper + wav2vec 对齐 + 说话人分离。 |
| LoRA 微调 | 高效调优 | 在注意力层添加低秩适配器；仅训练约 0.3% 参数。 |
| 幻觉 | 静默失败 | Whisper 从噪声/静音中产生流畅的英文。 |

> **【中文解读】**延伸阅读 proporciona un alto nivel de recursos para el aprendizaje profundo. Estos artículos y cursos son los referentes clásicos en el campo, adecuados para los lectores que necesitan una comprensión profunda.


## Más Leer más Leer más

- [Radford et al. (2022). Whisper paper](https://arxiv.org/abs/2212.04356) la arquitectura original y la receta de formación.
  Radford et al (2022).
- [OpenAI (2024). Whisper Large-v3-turbo release](https://github.com/openai/whisper/discussions/2363)- Decodificador de 4 capas, acelerador de 8 veces.
  OpenAI (2024). Whisper Large-v3-turbo 发布4 层解码器,8 倍加速──
- [Bain et al. (2023). WhisperX](https://arxiv.org/abs/2303.00747)- de forma larga, alineada con las palabras, diarializada.
  La gente se ha quedado en el lugar de la reunión.
- [Systran — faster-whisper repo](https://github.com/SYSTRAN/faster-whisper) CTranslate2 respaldado, 4x más rápido.
  Sistema de flujo de información más rápido: almacenamiento, translado, rápido 4 veces.
- [HuggingFace — Whisper fine-tune tutorial](https://huggingface.co/blog/fine-tune-whisper) canónica LoRA / Full-FT de paso.
  AcogidaFaceSusurrido 微调教程标准 LoRA/全参数微调指南。

> **【中文解读】**延伸阅读 proporciona recursos de alta calidad para el aprendizaje profundo, incluyendo artículos, tutorials y herramientas.

