# Evaluación de audio  WER, MOS, UTMOS, MMAU, FAD, y los cuadros de clasificación abiertos 音频评估指标

> No se puede enviar lo que no se puede medir. Esta lección nombra las métricas 2026 para cada tarea de audio: ASR (WER, CER, RTFx), TTS (MOS, UTMOS, SECS, WER-on-ASR-round-trip), audio-lenguaje (MMAU, LongAudioBench), música (FAD, CLAP), y altavoz (EER). Además de los tablones de clasificación donde se compara.

> **【中文解读】**无法量就无法交付──本课列出 2026年所有音频任务的评估指标:ASR 用 WER(词错率) ✓ TTS 用 MOS(平均意见分) ✓ 音频语言模型用 MMAU、音乐用 FAD、说话人识别用 EER──还有对比排行榜──

> **【拓展：WER 是语音识别的黄金指标】**WER(Rate de error de palabra,词错率) = (替换+删除+插入) / 总词数──Whisper Large v3 在英文上达到 ~5% WER,接近人类水平──中文用 CER(字错率)──

**Type:** Learn | **类型:** 学习
**Languages:** Python | **语言:** Python
**Prerequisites:** Phase 6 · 04, 06, 07, 09, 10; Phase 2 · 09 (Model Evaluation) | **前置知识:** 阶段 6 · 04、06、07、09、10；阶段 2 · 09（模型评估）
**Time:** ~60 minutes | **预计用时:** ~60 分钟

## El problema es la introducción del problema

Cada tarea de audio tiene múltiples métricas, cada una midiendo un eje diferente. Usando la métrica equivocada es cómo envías un modelo que se ve muy bien en tu tablero de instrumentos y terrible en producción.

> Cada tarea de audio tiene varios indicadores, cada indicador mide diferentes dimensiones. El indicador de uso erróneo es cómo se pone en línea un modelo que se ve muy bien en el tablero de instrumentos pero que se desempeña mal en la producción.

> **【中文解读】**La pregunta planteada en este capítulo es: ¿cómo entender y aplicar correctamente esta tecnología en la ingeniería real? Comprender el contexto de la cuestión ayuda a comprender los puntos clave de decisión del tipo de selección técnica. En los sistemas de IA reales, el tipo de selección técnica errónea suele ser más alto que el costo de error de la realización de detalles.


| Task | Primary | Secondary |
|------|---------|-----------|
| ASR | WER | CER · RTFx · first-token latency |
| TTS | MOS / UTMOS | SECS · WER-on-ASR-round-trip · CER · TTFA |
| Voice cloning | SECS (ECAPA cosine) | MOS · CER |
| Speaker verification | EER | minDCF · FAR / FRR at operating point |
| Diarization | DER | JER · speaker confusion |
| Audio classification | top-1 · mAP | macro F1 · per-class recall |
| Music generation | FAD | CLAP · listening panel MOS |
| Audio language model | MMAU-Pro | LongAudioBench · AudioCaps FENSE |
| Streaming S2S | latency P50/P95 | WER · MOS |

> **【中文解读】**Este capítulo presenta los conceptos y teorías básicos. La comprensión de estos conceptos es el prerrequisito de la realización posterior de la actividad, y también el conocimiento de los puntos de alta frecuencia de la entrevista y la práctica de la ingeniería.


## El concepto central.

![Audio evaluation matrix — metrics vs tasks vs 2026 leaderboards](../assets/eval-landscape.svg)

### Metricas de RAS

> Indicador de evaluación de la RAS

**WER (Word Error Rate).** `(S + D + I) / N`. letra pequeña, puntuación de la tira, normaliza los números antes de marcar.`jiwer`o de OpenAI `whisper_normalizer`. &lt;5% = lectura del discurso por igualdad humana.

> **WER（词错率）。** `(替换 + 删除 + 插入) / 总词数`◊评分前需转小写、除标点、标准化数字──使用 `jiwer`O de la apertura de la`whisper_normalizer`❖ Bajo el 5% = 朗讀语音的人类水平。

**CER (Character Error Rate).**La misma fórmula, nivel de caracteres. Se utiliza para los lenguajes de tono (mandarín, cantonés) donde la segmentación de palabras es ambigua.

> **CER（字错率）。**La forma de la palabra es la forma de la palabra.

**RTFx (inverse real-time factor).**Se trata de un segundo de audio procesado por segundo de un reloj de pared.

> **RTFx（逆实时因子）。**Cada segundo real de procesamiento de sufre de segundos.

**First-token latency.**Un reloj de pared desde la entrada de audio hasta el primer token de transcripción.

> **首 token 延迟。**Desde el audio input hasta el primer token de transferencia tiempo real.

### Metricas de TTS

> TTS  evaluación indicador

**MOS (Mean Opinion Score).**1-5 calificación humana. estándar de oro pero lento. Recolectar más de 20 oyentes por muestra, más de 100 muestras por modelo.

> **MOS（平均意见分）。**1-5 分人工评分──黄金标准但速度慢──每样本收集20+ 听者,每模型100+ 样本──

**UTMOS (2022-2026).**Aprendió predictor MOS. Correlación de ~ 0,9 con MOS humano en puntos de referencia estándar. F5-TTS: UTMOS 3.95; verdad de fondo: 4.08.

> **UTMOS（2022-2026）。**El modelo de aprendizaje MOS 预测器──在标准基准上与人类 MOS 相关性约0.9──F5-TTS:UTMOS 3.95;真实值:4.08──

**SECS (Speaker Encoder Cosine Similarity).**Para clonación de voz. ECAPA que incorpora cosino entre la referencia y la salida clonada. &gt; 0,75 = clona reconocible.

> **SECS（说话人编码器余弦相似度）。**Utilizado en el lenguaje de clón. Referencia de ECAPA entre el audio y el clón.

**WER-on-ASR-round-trip.**ejecuta Whisper sobre la salida de TTS, computa WER contra el texto de entrada. Captura regresiones de inteligencia. 2026 SOTA: &lt; 2% CER.

> **WER-on-ASR-round-trip（ASR 回环 WER）。**Para TTS 输出运行 Whisper, calculación relativa a WER de texto de entrada ⋅ capture可理解度退化──2026 SOTA:CER 低于2%──

**TTFA (time-to-first-audio).**La latencia del reloj de pared. Kokoro-82M: ~ 100 ms; F5-TTS: ~ 1 s.

> **TTFA（首个音频时间）。**实际延迟──Kokoro-82M: aproximadamente 100 ms; F5-TTS: aproximadamente 1 s──

### Específico para el clonamiento de voz

> 语音克隆专用标志

**SECS + MOS + CER**El clonado que obtiene un alto SECS pero un bajo MOS significa timbre-correcto-pero-innaturalizado; lo contrario significa voz natural pero fallo de altavoz.

> **SECS + MOS + CER**Como tres indicadores, el CLON tiene un puntaje alto en SECS pero bajo MOS significa sonido correcto pero no natural; el contrario significa sonido natural pero el habla no se opone.

### Verificación de altavoces

> 说话人验证指标

**EER (Equal Error Rate).**El umbral en el que la tasa de aceptación falsa es igual a la tasa de rechazo falso.

> **EER（等错误率）。** error accept rate = error rejection rate value ⋅ ECAPA en VoxCeleb1-O 上: 0.87% ⋅

**minDCF (min Detection Cost).**Costo ponderado en un punto de operación elegido (a menudo FAR=0,01).

> **minDCF（最小检测代价）。**En el punto de trabajo determinado (normalmente FAR=0.01) se incrementa el precio de producción en comparación con la EER.

### Diarización

> 说话人日志 标签

**DER (Diarization Error Rate).** `(FA + Miss + Confusion) / total_speaker_time`. Habla perdida + falso alarma + confusión de altavoces, cada uno como fracción. Encuentros AMI: DER ~10-20% es realista. nota 3.1 + Precisión-2 comercial: &lt;10% DER en audio bien grabado.

> **DER（说话人日志错误率）。** `(虚警 + 漏检 + 混淆) / 总说话时间`◊漏检语音 + 虚警语音 + 说话人混,各占比例──AMI 会议:DER 约 10-20% 是现实水平──piannote 3.1 + Precision-2 商业版:在良好录音上 DER 低于10%──

**JER (Jaccard Error Rate).**Alternativa a DER, robusta a la inclinación de segmentos cortos.

> **JER（Jaccard 错误率）。**El programa de trabajo de la DER, para el desarrollo de la tecnología de la información, es un programa de trabajo de la DER.

### Clasificación de audio

> 音频分类标签

Multi-etiqueta: **mAP (mean Average Precision)**AudioSet: 0.548 mAP para BEATs-iter3.

> Más de un año**mAP（平均精度均值）**, cubre todas las categorías。AudioSet:BEATs-iter3 为 0.548 mAP。

Exclusivo de varias clases: **top-1, top-5 accuracy**. Comando de habla v2: 99,0% top-1 (Audio-MAE).

> Más de un grupo:**top-1、top-5 准确率**❖ Comando de habla v2:99.0% top-1 ❖Audio-MAE)

Desbalanceado: **macro F1**¿ Qué es eso ?**per-class recall**.Informe por clase  la precisión agregada oculta qué clases fallan.

> Datos desequilibrados:**macro F1**¿ Qué es eso ?**每类召回率** El informe de los tipos de desempleo                                                                                                                                                                                                                                                          

### Generación de música

> 音乐生成指标 音乐生成指标

**FAD (Fréchet Audio Distance).**Distancia entre las distribuciones de audio real y generado por VGGish. MusicGen-small en MusicCaps: 4.5. MusicLM: 4.0.

> **FAD（Fréchet 音频距离）。**La verdad y la producción de sonido de VGGish 嵌入分布之间的距离──MusicGen-small 在 MusicCaps 上:4.5──MusicLM:4.0──越低越好──

**CLAP Score.**Score de alineación de texto y audio utilizando embebedidos CLAP. &gt; 0.3 = alineación razonable.

> **CLAP 分数。**Utiliza CLAP 嵌入的文本音频对齐分数──大于0.3 = 合理对齐──

**Listening panel MOS.**Aún es la última palabra para la música de consumo. Suno v5 ELO 1293 en TTS Arena (desde preferencias humanas emparejadas).

> **听音评审团 MOS。**El ELO de TTS Arena es 1293 (proveniente de la preferencia humana)

### Indicadores de referencia de lenguaje de audio

> 音频语言基准测试

**MMAU (Massive Multi-Audio Understanding).**10K pares de audio-QA.

> **MMAU（大规模多音频理解）。**10 000 audio-QA para el

**MMAU-Pro.**1800 artículos duros, cuatro categorías: habla / sonido / música / multi-audio. casualidad 25% en 4 vías. Gemini 2.5 Pro en general ~ 60%; multi-audio ~ 22% en todos los modelos.

> **MMAU-Pro。**1800 个难题,四个类别:语音/声音/音乐/多音频──4 选 1 随机猜测 25%──Gemini 2.5 Pro 整体约60%;所有模型在多音频上约22%.──

**LongAudioBench.**Clip de varios minutos con consultas semánticas.

> **LongAudioBench。**Quizás钟音频片段 + 语义查询──Audio Flamingo Siguiente 超过 Gemini 2.5 Pro──

**AudioCaps / Clotho.**Los indicadores de referencia de la SPICE, CIDER y FENSE.

> **AudioCaps / Clotho。**音频描述基准测试──SPICE、CIDER、FENSE 指标──

### Transmisiones de habla a palabra

> 流式语音到语音指标

**Latency P50 / P95 / P99.**Reloj de pared desde el final del usuario de la voz a la primera respuesta audible.

> **延迟 P50 / P95 / P99。**Desde el usuario de voz termina hasta el primer tiempo real de respuesta audible.

**WER / MOS**en la salida.

>                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                              **WER / MOS**¿Qué es eso?

**Barge-in responsiveness.**Tiempo desde la interrupción del usuario hasta el silencio del asistente.

> **打断响应时间。**Desde el tiempo de interrupción del usuario hasta el tiempo de silencio del asistente.

### Las tablas de clasificación de 2026

| Leaderboard | Tracks | URL |
|------------|--------|-----|
| Open ASR Leaderboard (HF) / 开源 ASR 排行榜（HF） | English + multilingual + long-form / 英语 + 多语言 + 长音频 | `huggingface.co/spaces/hf-audio/open_asr_leaderboard` |
| TTS Arena (HF) / TTS 竞技场（HF） | English TTS / 英语 TTS | `huggingface.co/spaces/TTS-AGI/TTS-Arena` |
| Artificial Analysis Speech / Artificial Analysis 语音 | TTS + STT, ELO from paired votes / TTS + STT，配对投票 ELO | `artificialanalysis.ai/speech` |
| MMAU-Pro / MMAU-Pro | LALM reasoning / LALM 推理 | `mmaubenchmark.github.io` |
| SpeakerBench / VoxSRC / 说话人基准 / VoxSRC | Speaker recognition / 说话人识别 | `voxsrc.github.io` |
| MMAU music subset / MMAU 音乐子集 | Music LALM / 音乐 LALM | （在 MMAU 内） |
| HEAR benchmark / HEAR 基准 | Self-supervised audio / 自监督音频 | `hearbenchmark.com` |

> **【中文解读】**Este capítulo a través del código de la implementación de algoritmos centrales de cero. Este método "desde cero" puede ayudar a entender el principio detrás del marco, no se encuentra en la caja negra cuando se encuentran problemas.

> **【拓展：语音 AI 的产品化】**La tecnología de voz se enfrenta a un desafío único en la productorización: diferentes voces, ruidos de contexto, remota recogida, muchos hablar, etc.

> **【拓展：多语言语音技术】**Las características de los idiomas de todo el mundo son muy diferentes: el sonido de los idiomas de todo el mundo (como el chino) es alto, el lenguaje de bajo recurso es poco capacitado.




## Construye y realiza.
```figure
sp-wer-align
```

## Construye el mismo

### Paso 1: WER con normalización

> Paso 1: con el ERM estandarizado

```python
from jiwer import wer, Compose, ToLowerCase, RemovePunctuation, Strip

transform = Compose([ToLowerCase(), RemovePunctuation(), Strip()])
score = wer(
    truth="Please turn on the lights.",
    hypothesis="please turn on the light",
    truth_transform=transform,
    hypothesis_transform=transform,
)
# ~0.17
```

### Paso 2: TTS WER de ida y vuelta

> 步骤 2: TTS 回环 WER

```python
def ttr_wer(tts_model, asr_model, texts):
    errors = []
    for txt in texts:
        audio = tts_model.synthesize(txt)
        recog = asr_model.transcribe(audio)
        errors.append(wer(truth=txt, hypothesis=recog))
    return sum(errors) / len(errors)
```

### Paso 3: SECS para la clonación de voz

> Paso 3: Secciones de la lengua

```python
from speechbrain.inference.speaker import EncoderClassifier
sv = EncoderClassifier.from_hparams("speechbrain/spkrec-ecapa-voxceleb")

emb_ref = sv.encode_batch(load_wav("reference.wav"))
emb_clone = sv.encode_batch(load_wav("cloned.wav"))
secs = torch.nn.functional.cosine_similarity(emb_ref, emb_clone, dim=-1).item()
```

### Paso 4: FAD para la generación de música

> Paso 4: FAD de la producción de música

```python
from frechet_audio_distance import FrechetAudioDistance
fad = FrechetAudioDistance()
score = fad.get_fad_score("generated_folder/", "reference_folder/")
```

### Paso 5: EER para la verificación de altavoces (el mismo código que la lección 6)

> Paso 5: el código de EER de la enseñanza de la lengua inglesa (EER) es el mismo que el código de la enseñanza de la lengua inglesa (EER)

```python
def eer(same_scores, diff_scores):
    thresholds = sorted(set(same_scores + diff_scores))
    best = (1.0, 0.0)
    for t in thresholds:
        far = sum(1 for s in diff_scores if s >= t) / len(diff_scores)
        frr = sum(1 for s in same_scores if s < t) / len(same_scores)
        if abs(far - frr) < best[0]:
            best = (abs(far - frr), (far + frr) / 2)
    return best[1]
```

> **【中文解读】**Este capítulo muestra cómo utilizar un marco maduro (como PyTorch、HuggingFace, etc.) para aplicar rápidamente esta tecnología. En los proyectos reales, se realiza con prioridad el uso de un marco experimentado, se pueden reducir errores y mejorar la eficiencia de desarrollo.





> **【拓展：语音与情感计算】**语音 no sólo transmite información escrita, también lleva una rica cantidad de señales emocionales (en inglés: voice signal) 语调、语速、音高变化) 情感语音识别 (en inglés: speech emotion recognition, SER) 语音 no solo transmite información escrita, sino que también lleva una gran cantidad de señales emocionales (en inglés: voice signal). 语音 tiene una amplia aplicación en el campo de la evaluación de calidad de los clientes, la vigilancia de la salud mental, la educación inteligente, etc.  Los modelos actuales de SOTA se basan en modelos de entrenamiento de las ondas 2vec 2.0 o HuBERT.

## Usalo con el marco de ejecución

Enpareja cada implementación con un arnés de evaluación fijo que se ejecuta en cada actualización del modelo.

> Cada implementación está equipada con una herramienta de evaluación fija, en cada modelo actualizada.

1. **Normalize before scoring.**La letra baja, la franja de puntuación, el número ampliado, informe la regla de normalización.
   En inglés:**评分前标准化。**转小写、去标点、数字展开――报告标准化规则――
2. **Report distributions, not averages.**P50/P95/P99 para latencia. Recall por clase para clasificación. Por categoría para MMAU.
   En inglés:**报告分布而非均值。**延迟用P50/P95/P99──分类用每类召回率──MMAU用每类──
3. **Run one canonical public benchmark.**Incluso si sus datos de producción difieren, el reporte en Open ASR / TTS Arena / MMAU permite a los revisores comparar manzanas con manzanas.
   En inglés:**运行一个权威公共基准。**Incluso si tu producción de datos no es igual, en el Open ASR / TTS Arena / MMAU el informe puede permitir que los evaluadores hagan una comparación justa.



## Las trampas

> 常见陷

- **UTMOS extrapolation.**Entrenado en el estilo de voz limpia VCTK; califica ruidosos / clonados / audio emocional mal.
  En inglés:**UTMOS 外推问题。**En el estilo VCTK, el entrenamiento en lenguaje puro y puro; en el lenguaje de la lengua, el entrenamiento en lenguaje puro y puro y puro.
- **MOS panel bias.**20 trabajadores de Amazon Mechanical Turk ≠ 20 usuarios objetivo.
  En inglés:**MOS 评审团偏差。**20 个 Amazon Mechanical Turk 工作者不等于 20 个目标用户──如果风险高,花钱请领域专家评审团──
- **FAD depends on reference set.**Comparar con la misma distribución de referencia entre los modelos.
  En inglés:**FAD 依赖参考集。**跨模型比较时使用相同的参考分布──
- **Aggregate WER.**Un 5% de RAE en general puede ocultar el 30% de RAE en el habla acentuada.
  En inglés:**汇总 WER。**El 5% de la RAE en general puede oculpar el 30% de la RAE en el informe del grupo de población.
- **Public benchmark saturation.**La mayoría de los modelos fronterizos están cerca del techo en los puntos de referencia estándar.
  En inglés:**公共基准饱和。**La mayoría de los modelos de vanguardia en el estándar de base se han acercado al cielo.

> **【中文解读】**Este capítulo se centra en cómo se puede implementar el modelo como producto disponible. Desde el modelo original hasta el sistema de producción, se deben considerar múltiples dimensiones de optimización de rendimiento, tratamiento de errores, control, etc.


## Envíe el producto .

Salvo como`outputs/skill-audio-evaluator.md`Seleccionar métricas, puntos de referencia y formato de informes para cualquier versión de modelo de audio.

> 保存为                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           `outputs/skill-audio-evaluator.md`◊ para cualquier modelo de audio publicar índices de selección, base y formato de informe.

## Los ejercicios.

1. **Easy.**- ¿ Qué ?`code/main.py`. Calcular WER / CER / EER / SECS / FAD-ish / MMAU-ish en las entradas de juguete.
   En inglés:**简单。**运行                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           `code/main.py` en el juego输入上计算 WER / CER / EER / SECS / 类 FAD / 类 MMAU。
2. **Medium.**Construye un arnés WER de ida y vuelta TTS. ejecuta su salida Kokoro o F5-TTS a través de Whisper. Computa WER más de 50 instrucciones. Indicaciones de bandera con WER &gt; 10%.
   En inglés:**中等。**Construir TTS 回环 WER 评估工具──用 Whisper 处理你的 Kokoro 或 F5-TTS 输出──在 50 个提示上计算 WER──标记 WER大于10%的提示──
3. **Hard.**Obtenga un puntaje en la opción de LALM de la Lección 10 en el discurso MMAU-Pro + subconjuntos de audio múltiples (50 elementos cada uno).
   En inglés:**困难。**En MMAU-Pro de la lengua + 多音频子集上 (en inglés) de cada 50 artículos, evalúa tu 10o 课选择的 LALM.

> **【中文解读】**En el lenguaje de los términos "Lo que la gente dice" vs "Lo que realmente significa" se distingue entre el lenguaje diario y la definición técnica de significado.


## Términos clave .

| Term | What people say | What it actually means |
|------|-----------------|-----------------------|
| WER | ASR score | `(S+D+I)/N` at word level after normalization. / 标准化后的词级 `(S+D+I)/N` |
| CER | Character WER | For tone languages or char-level systems. / 用于声调语言或字符级系统 |
| MOS | Human opinion | 1-5 rating; 20+ listeners × 100 samples. / 1-5 分评分；20+ 听者 × 100 样本 |
| UTMOS | ML MOS predictor | Learned model; correlates ~0.9 with human MOS. / 学习型模型；与人类 MOS 相关性约 0.9 |
| SECS | Voice-clone similarity | ECAPA cosine between reference and clone. / 参考与克隆之间的 ECAPA 余弦相似度 |
| EER | Speaker verif score | Threshold where FAR = FRR. / FAR = FRR 的阈值 |
| DER | Diarization score | (FA + Miss + Confusion) / total. / (虚警 + 漏检 + 混淆) / 总时间 |
| FAD | Music-gen quality | Fréchet distance on VGGish embeddings. / VGGish 嵌入上的 Fréchet 距离 |
| RTFx | Throughput | Audio seconds per wall-clock second. / 每实际秒处理的音频秒数 |

> **【中文解读】**延伸阅读 proporciona un alto nivel de recursos para el aprendizaje profundo. Estos artículos y cursos son los referentes clásicos en el campo, adecuados para los lectores que necesitan una comprensión profunda.


## Más Leer más Leer más

- [jiwer](https://github.com/jitsi/jiwer) Biblioteca WER/CER con utilidades de normalización.
  La Comisión Europea ha aprobado el proyecto de ley de la UE en el marco del Programa de Estadísticas de la UE.
- [UTMOS (Saeki et al. 2022)](https://arxiv.org/abs/2204.02152) aprendido predictor de MOS.
  UTMOS(Saeki 等 2022) 学习型 MOS 预测器。
- [Fréchet Audio Distance (Kilgour et al. 2019)](https://arxiv.org/abs/1812.08466) el estándar de la generación musical.
  Distancia de audio de Fréchet ((Kilgour 等 2019) 音乐生成的标准指标──
- [Open ASR Leaderboard](https://huggingface.co/spaces/hf-audio/open_asr_leaderboard) 2026 rankings en vivo.
  Abre ASR 排行榜2026 实时排名──
- [TTS Arena](https://huggingface.co/spaces/TTS-AGI/TTS-Arena) el ranking de TTS con votos humanos.
  TTS Arena  TTS 排行榜 de los ciudadanos en el mundo 
- [MMAU-Pro benchmark](https://mmaubenchmark.github.io/) Lista de resultados del razonamiento LALM.
  MMAU-Pro 基准LALM 推理排行榜
- [HEAR benchmark](https://hearbenchmark.com/) índices de referencia de SSL de audio.
  Escucha 基准音频 SSL 评估基准──

> **【中文解读】**延伸阅读 proporciona recursos de alta calidad para el aprendizaje profundo, incluyendo artículos, tutorials y herramientas.

