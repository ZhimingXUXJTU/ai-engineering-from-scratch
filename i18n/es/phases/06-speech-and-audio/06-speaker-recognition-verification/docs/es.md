# El Presidente reconocimiento y verificación habla identificación y verificación de personas.

> ASR pregunta "¿qué dijeron?" el reconocimiento del orador pregunta "¿quién lo dijo?" La matemática se ve igual  embebidos más cosino  pero cada decisión de producción depende de un solo número EER.

> **【中文解读】**ASR 问"说了什么",说话人识别问"谁说的"―― matemáticas se ven como 嵌向量+余弦相似度, pero cada decisión de producción depende de un EER等误差率) número de valores──EER 越低,系统越可靠──

> **【拓展：声纹识别应用】**声纹识别用于银行电话认证、智能音箱用户识别、安防监控──声纹(voz huella) Tal como los dedos del lenguaje, es una importante rama del reconocimiento de las características biológicas──

**Type:** Build | **类型:** 构建
**Languages:** Python | **语言:** Python
**Prerequisites:** Phase 6 · 02 (Spectrograms & Mel), Phase 5 · 22 (Embedding Models) | **前置知识:** 阶段 6 · 02（频谱图与 Mel），阶段 5 · 22（嵌入模型）
**Time:** ~45 minutes | **预计用时:** ~45 分钟

## El problema es la introducción del problema

Un usuario dice una frase de contraseña. ¿Quieres saber: es esta la persona que dicen ser (*verificación*, 1:1), o es la primera persona en tu banco de inscripción (*identificación*, 1:N)?

> Usador dice una frase. ¿Sabes que es la persona que ellos afirman que es? ¿Está usted la primera persona en el registro?

> **【中文解读】**La pregunta planteada en este capítulo es: ¿cómo entender y aplicar correctamente esta tecnología en la ingeniería real? Comprender el contexto de la cuestión ayuda a comprender los puntos clave de decisión del tipo de selección técnica. En los sistemas de IA reales, el tipo de selección técnica errónea suele ser más alto que el costo de error de la realización de detalles.

Pre-2018: GMM-UBM + i-vectores. EER razonable pero frágil para el cambio de canal (teléfono vs portátil) y la emoción. 20182022: x-vectores (espina dorsal TDNN entrenada con margen angular). 2022+: ECAPA-TDNN y WavLM-embeddings grandes. Para 2026 el campo está dominado por tres modelos y una métrica.

> 2018 años anterior:GMM-UBM + i-vectores。EER 合理但对信道偏移(电话 vs 笔记本) 和情绪敏感。2018-2022:x-vectores(u using angle间隔 training of TDNN 骨干)。2022+:ECAPA-TDNN 和 WavLM-large 嵌入──到2026年,该领域由三个模型和一个指标主导────

La métrica es **EER** tasa de error igual. Establezca su umbral de decisión para que False Accept Rate = False Reject Rate. El crossover es EER.

> Este indicador es**EER**等错误率──设置决策值使假接受率 =假拒绝率──交叉点就是 EER──用于每篇论文、每排行榜、每采购评审──

## El concepto central.

> **【中文解读】**Este capítulo presenta los conceptos y teorías básicos. La comprensión de estos conceptos es el prerrequisito de la realización posterior de la actividad, y también el conocimiento de los puntos de alta frecuencia de la entrevista y la práctica de la ingeniería.


![Enrollment + verification pipeline with embedding + cosine + EER](../assets/speaker-verification.svg)

**The pipeline.**Inscripción: grabar 530 segundos del altavoz objetivo; calcular una incorporación de dimensión fija (192-d para ECAPA-TDNN, 256-d para WavLM-large). Verificación: obtener la incorporación de la expresión de prueba; calcular la similitud cosina; comparar con un umbral.

> **流水线。**Registrar: Registro de objetivos de la lengua 5-30 segundos de voz; calcular dimensiones fijas de la lengua; ECAPA-TDNN para 192 维, WavLM-large para 256 维)

**ECAPA-TDNN (2020, still dominant 2026).**Enfatizado de la atención de canal, propagación y agregación - red neuronal de retraso en el tiempo. Bloques de convoluciones 1D con excitación de apretón, concentración de atención multi-cabeza, seguido de una capa lineal a 192-d. Entrenado en VoxCeleb 1+2 (2,700 altavoces, 1.1M pronunciamientos) con pérdida de margen angular aditiva (AAM-softmax).

> **ECAPA-TDNN（2020，2026 年仍占主导）。**Enfatizado en el tiempo de la comunicación y la concentración de la red nerviosa.1.D. 卷积块 + compresión-excitación + 多头注意池化,接线性层输出192维── en VoxCeleb 1+2(2,700 说话人,110万条语音) con ángulo de separación adicional.

**WavLM-SV (2022+).**Ajuste la columna vertebral de SSL de WavLM con pérdida de AAM.

> **WavLM-SV（2022+）。**Usar AAM 损失微调预训练的 WavLM-large SSL 骨干──质量更高但更慢300+ MB vs 15 MB──

**x-vector (baseline).**TDNN + estadísticas de agrupación. clásico; todavía útil en CPU / borde.

> **x-vector（基线）。**TDNN + 统计池化── clásico; todavía es útil en los dispositivos de CPU/margen.

**AAM-softmax.**Softmax estándar con margen añadido `m`en el espacio angular: `cos(θ + m)`Las fuerzas de separación angular entre clases.`m=0.2`, escala `s=30`¿ Qué ?

> **AAM-softmax。**En el espacio de ángulo añadir espacios`m`                                                                                                                                                                                                                                                              `cos(θ + m)` Fuerza de clase entre ángulos de separación  valor típico `m=0.2`, reducido`s=30`¿Qué es eso?

### Punto de juego

> ### 评分:

- **Cosine**La decisión basada en el umbral.
  **余弦**Similaridad, en el registro de la inserción y la prueba de la inserción entre cálculos.
- **PLDA (Probabilistic LDA).**Embedings de proyectos en un espacio latente donde el mismo altavoz vs altavoz diferente tiene una proporción de probabilidad de forma cerrada. Añadido en la parte superior del cosino para una reducción de EER de +1020%. estándar pre-2020; ahora solo se utiliza en configuraciones cerradas.
  **PLDA（概率 LDA）。**Se incorporará proyección en el espacio potencial, en el que el interlocutor vs. el interlocutor tiene un tipo de parecido cerrado.
- **Score normalization.** `S-norm`o `AS-norm`La normalización de cada puntuación en relación con una cohorte de medios imposter y etc. Es esencial para la evaluación de distintos dominios.
  **分数归一化。** `S-norm`O `AS-norm`El valor medio y el estándar de los grupos de los iniciadores se clasifican en cada porcentaje.

### Números que usted debe saber (2026)

> 2026 años que deberías saber números

| Model | VoxCeleb1-O EER | Params | Throughput (A100) |
|-------|-----------------|--------|-------------------|
| x-vector (classic) | 3.10% | 5 M | 400× RT |
| ECAPA-TDNN | 0.87% | 15 M | 200× RT |
| WavLM-SV large | 0.42% | 316 M | 20× RT |
| Pyannote 3.1 segmentation + embedding | 0.65% | 6 M | 100× RT |
| ReDimNet (2024) | 0.39% | 24 M | 100× RT |

| 模型 | VoxCeleb1-O EER | 参数量 | 吞吐量（A100） |
|------|-----------------|--------|----------------|
| x-vector（经典） | 3.10% | 500 万 | 400× 实时 |
| ECAPA-TDNN | 0.87% | 1500 万 | 200× 实时 |
| WavLM-SV large | 0.42% | 3.16 亿 | 20× 实时 |
| Pyannote 3.1 分割 + 嵌入 | 0.65% | 600 万 | 100× 实时 |
| ReDimNet（2024） | 0.39% | 2400 万 | 100× 实时 |

### Diarización

> ### 说话人日志 ((quien está hablando en el momento)

"Quién habló cuando" en un clip de altavoces. Pipeline: VAD → segmento → incrusta cada segmento → grupo (aglomerativo o espectral) → límites suaves.`pyannote.audio`3.1, que agrupa la segmentación de altavoces + incorporación + agrupación detrás de una llamada. 2026 SOTA DER en AMI es de ~ 15% (descenso del 23% en 2022).

> Más información sobre el proceso de creación de un sistema de gestión de la información y la información de la información.`pyannote.audio`3.1,将说话人分割 + 嵌入 + 聚类打包为一个调用──2026 años AMI 上 SOTA DER 约15%(de 2022 años 23% 下降)──

> **【拓展：语音 AI 的产品化】**La tecnología de voz se enfrenta a un desafío único en la productorización: diferentes voces, ruidos de contexto, remota recogida, muchos hablar, etc.

> **【拓展：多语言语音技术】**Las características de los idiomas de todo el mundo son muy diferentes: el sonido de los idiomas de todo el mundo (como el chino) es alto, el lenguaje de bajo recurso es poco capacitado.



## Construye y realiza.

> **【中文解读】**Este capítulo a través del código de la implementación de algoritmos centrales de cero. Este método "desde cero" puede ayudar a entender el principio detrás del marco, no se encuentra en la caja negra cuando se encuentran problemas.

```figure
sp-eer-crossover
```

## Construye el mismo

### Paso 1: incorporación de juguetes de las estadísticas de la MFCC

```python
def embed_mfcc_stats(signal, sr):
    frames = featurize_mfcc(signal, sr, n_mfcc=13)
    mean = [sum(f[i] for f in frames) / len(frames) for i in range(13)]
    std = [
        math.sqrt(sum((f[i] - mean[i]) ** 2 for f in frames) / len(frames))
        for i in range(13)
    ]
    return mean + std  # 26-d
```

No SOTA por una milla  sólo para la enseñanza. `code/main.py`utiliza esto como prueba de concepto en los datos de altavoces sintéticos.

> 离 SOTA 差得远 sólo para la enseñanza.`code/main.py`La introducción de la lengua en el lenguaje humano es una forma de traducción de la lengua en lenguaje humano.

### Paso 2: similitud cosina + umbral

```python
def cosine(a, b):
    dot = sum(x * y for x, y in zip(a, b))
    na = math.sqrt(sum(x * x for x in a))
    nb = math.sqrt(sum(x * x for x in b))
    return dot / (na * nb) if na and nb else 0.0

def verify(enroll, test, threshold=0.75):
    return cosine(enroll, test) >= threshold
```

### Paso 3: EER de pares de similitudes

```python
def eer(same_scores, diff_scores):
    thresholds = sorted(set(same_scores + diff_scores))
    best = (1.0, 1.0, 0.0)  # (fa, fr, threshold)
    for t in thresholds:
        fr = sum(1 for s in same_scores if s < t) / len(same_scores)
        fa = sum(1 for s in diff_scores if s >= t) / len(diff_scores)
        if abs(fa - fr) < abs(best[0] - best[1]):
            best = (fa, fr, t)
    return (best[0] + best[1]) / 2, best[2]
```

Las devoluciones (eer, threshold_at_eer) reportan ambas.

> 返回 (eer, threshold_at_eer) ⋅两者都要报告──

### Paso 4: producción con SpeechBrain

```python
from speechbrain.pretrained import EncoderClassifier

clf = EncoderClassifier.from_hparams(source="speechbrain/spkrec-ecapa-voxceleb")

# enroll: average the embeddings of 3-5 clean samples
enroll = torch.stack([clf.encode_batch(load(x)) for x in enrollment_clips]).mean(0)
# verify
score = clf.similarity(enroll, clf.encode_batch(load("test.wav"))).item()
verdict = score > 0.25   # ECAPA typical threshold; tune on your data
```

### Paso 5: Diario con nota de piña

```python
from pyannote.audio import Pipeline

pipe = Pipeline.from_pretrained("pyannote/speaker-diarization-3.1")
diarization = pipe("meeting.wav", num_speakers=None)
for turn, _, speaker in diarization.itertracks(yield_label=True):
    print(f"{turn.start:.1f}–{turn.end:.1f}  {speaker}")
```

> **【中文解读】**Este capítulo muestra cómo utilizar un marco maduro (como PyTorch、HuggingFace, etc.) para aplicar rápidamente esta tecnología. En los proyectos reales, se realiza con prioridad el uso de un marco experimentado, se pueden reducir errores y mejorar la eficiencia de desarrollo.





> **【拓展：语音与情感计算】**语音 no sólo transmite información escrita, también lleva una rica cantidad de señales emocionales (en inglés: voice signal) 语调、语速、音高变化) 情感语音识别 (en inglés: speech emotion recognition, SER) 语音 no solo transmite información escrita, sino que también lleva una gran cantidad de señales emocionales (en inglés: voice signal). 语音 tiene una amplia aplicación en el campo de la evaluación de calidad de los clientes, la vigilancia de la salud mental, la educación inteligente, etc.  Los modelos actuales de SOTA se basan en modelos de entrenamiento de las ondas 2vec 2.0 o HuBERT.

## Usalo con el marco de ejecución

La pila de 2026:

> Tecnología de 2026:

| Situation | Pick |
|-----------|------|
| Closed-set 1:1 verification, edge | ECAPA-TDNN + cosine threshold |
| Open-set verification, cloud | WavLM-SV + AS-norm |
| Diarization (meetings, podcasts) | `pyannote/speaker-diarization-3.1` |
| Anti-spoofing (replay / deepfake detection) | AASIST or RawNet2 |
| Tiny embedded (KWS + enrollment) | Titanet-Small (NeMo) |

| 场景 | 选择 |
|------|------|
| 封闭集 1:1 验证，边缘设备 | ECAPA-TDNN + 余弦阈值 |
| 开放集验证，云端 | WavLM-SV + AS-norm |
| 说话人日志（会议、播客） | `pyannote/speaker-diarization-3.1` |
| 反欺诈（回放/深度伪造检测） | AASIST 或 RawNet2 |
| 小型嵌入式（关键词检测 + 注册） | Titanet-Small（NeMo） |



## Las trampas

> 常见陷

- **Channel mismatch.**Modelo entrenado en VoxCeleb (vídeo web) ≠ audio de llamada telefónica. Siempre evalúa en el canal objetivo.
  **信道不匹配。**En VoxCeleb (en inglés) el modelo de entrenamiento no es igual a un teléfono.
- **Short utterances.**El EER se degrada marcadamente por debajo de los 3 segundos de audio de prueba.
  **短语音。**测试音频低于3秒时 EER 剧恶化──
- **Enrollment with noise.**Una inscripción ruidosa envenena el anclaje.
  **带噪注册。**Una muestra de registro de la agencia de la información de la agencia de la información de la agencia de la información de la agencia de la información de la agencia de la información de la agencia de la agencia de la información de la agencia de la agencia de la información de la agencia de la agencia de la información de la agencia de la agencia de la información de la agencia de la agencia de la información de la agencia de la agencia de la información de la agencia de la agencia de la información de la agencia de la agencia de la agencia de la información de la agencia de la agencia de la agencia de la agencia de la información de la agencia de la agencia de la agencia de la agencia de la agencia de la agencia de la agencia de la agencia de la agencia de la agencia de la agencia de la agencia de la agencia de la agencia de la agencia de la agencia de la agencia de agencia de agencia de agencia de agencia de agencia de agencia de agencia de agencia de agencia de agencia de agencia de agencia de agencia de agencia de agencia de agencia de agencia de agencia de agencia de agencia de agencia de agencia de agencia de agencia de agencia de agencia de agencia de agencia de agencia de agencia de agencia de agencia de agencia de agencia de agencia de agencia de agencia de agencia de agencia de agencia de agencia de agencia de agencia de agencia de agencia de agencia de agencia de agencia de agencia de agencia de agencia de agencia de agencia de agencia de agencia de agencia de agencia de agencia de agencia de agencia de agencia de agencia de agencia de agencia de agencia de agencia de agencia de agencia de agencia de agencia de agencia de agencia de agencia de agencia de agencia de agencia de agencia de agencia de agencia de agencia de agencia de agencia de agencia de agencia de agencia de agencia de agencia de agencia de agencia de agencia de agencia de agencia de agencia de agencia de agencia de agencia de agencia de
- **Fixed threshold across conditions.**Siempre sintonice el umbral en un conjunto de desarrollo prolongado del dominio objetivo.
  **跨条件固定阈值。**始终在目标领域的留出开发集上调整值──
- **Cosine on non-normalized embeddings.**L2-normalizan primero; de lo contrario la magnitud domina.
  **未归一化嵌入上的余弦。**El primer hecho de L2 归一化;否则模值会占主导.

> **【中文解读】**Este capítulo se centra en cómo se puede implementar el modelo como producto disponible. Desde el modelo original hasta el sistema de producción, se deben considerar múltiples dimensiones de optimización de rendimiento, tratamiento de errores, control, etc.


## Envíe el producto .

Salvo como`outputs/skill-speaker-verifier.md`- Selección de modelo, protocolo de inscripción, plan de ajuste de umbral y garantías de fraude.

> 保存为                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           `outputs/skill-speaker-verifier.md` Selección de modelos, acuerdo de registro, programa de mejoras de valor y medidas de prevención contra el fraude.

## Los ejercicios.

> **【中文解读】**En el lenguaje de los términos "Lo que la gente dice" vs "Lo que realmente significa" se distingue entre el lenguaje diario y la definición técnica de significado.


1. **Easy.**- ¿ Qué ?`code/main.py`. Construye altavoces sintéticos (profiles de tono diferentes), registra y calcula EER en una lista de ensayos de 100 pares.
   **简单。**运行                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           `code/main.py`◊ Construir un conjunto de ensayos, en el que se calcula la EER en 100 para la lista de ensayos.
2. **Medium.**Utilice el ECAPA SpeechBrain en 30 declaraciones VoxCeleb1 (5 altavoces × 6 cada uno).
   **中等。**En 30 条 VoxCeleb1 语音上使用SpeechBrain ECAPA(5 个说话人 × 6 条) ――用余弦和 PLDA 计算 EER。
3. **Hard.**Construir el registro completo → diario → verificar la tubería con `pyannote.audio`Evaluar el DER en el set de desarrollo de AMI.
   **困难。**¿ Qué ?`pyannote.audio`构建完整的注册 → 日志 → 验证流水线──在 AMI 开发集上评估 DER──

## Términos clave .

| Term | What people say | What it actually means |
|------|-----------------|-----------------------|
| EER | The headline metric | Threshold where False Accept = False Reject. |
| Verification | 1:1 | "Is this Alice?" |
| Identification | 1:N | "Who is speaking?" |
| Open-set | Unknown possible | Test set can contain unenrolled speakers. |
| Enrollment | Registering | Computing a speaker's reference embedding. |
| AAM-softmax | The loss | Softmax with additive angular margin; forces cluster separation. |
| PLDA | Classic scoring | Probabilistic LDA; likelihood-ratio scoring on top of embeddings. |
| DER | Diarization metric | Diarization Error Rate — miss + false alarm + confusion. |

| 术语 | 人们常说的 | 实际含义 |
|------|-----------|---------|
| EER | 头条指标 | 假接受率 = 假拒绝率时的阈值。 |
| 验证 | 1:1 | "这是 Alice 吗？" |
| 识别 | 1:N | "谁在说话？" |
| 开放集 | 可能有未知者 | 测试集可包含未注册的说话人。 |
| 注册 | 登记 | 计算说话人的参考嵌入。 |
| AAM-softmax | 那个损失 | 带加性角度间隔的 softmax；强制聚类分离。 |
| PLDA | 经典评分 | 概率 LDA；嵌入之上的似然比评分。 |
| DER | 日志指标 | 说话人日志错误率——漏检 + 误检 + 混淆。 |

> **【中文解读】**延伸阅读 proporciona un alto nivel de recursos para el aprendizaje profundo. Estos artículos y cursos son los referentes clásicos en el campo, adecuados para los lectores que necesitan una comprensión profunda.


## Más Leer más Leer más

- [Snyder et al. (2018). X-Vectors: Robust DNN Embeddings for Speaker Recognition](https://www.danielpovey.com/files/2018_icassp_xvectors.pdf) el clásico papel de inserción profunda.
  Snyder 等 (2018). X-Vectors:说话人识别的鲁棒 DNN 嵌入经典的深度嵌入论文──
- [Desplanques et al. (2020). ECAPA-TDNN](https://arxiv.org/abs/2005.07143) arquitectura dominante 20202026.
  Desplantes, entre otros (2020). ECAPA-TDNN2020-2026 años de ocupación de la arquitectura dominante.
- [Chen et al. (2022). WavLM: Large-Scale Self-Supervised Pre-Training for Full Stack Speech Processing](https://arxiv.org/abs/2110.13900) Espionaje SSL para SV y diarización.
  Chen 等 (2022). WavLM: 整语音处理大规模自监督预训练SV 和日志的 SSL 骨干──
- [Bredin et al. (2023). pyannote.audio 3.1](https://github.com/pyannote/pyannote-audio) Diarización de la producción + pila de incorporación.
  Bredin 等 (2023). pyannote.audio 3.1生产级日志 + 嵌入技术。
- [VoxCeleb leaderboard (updated 2026)](https://www.robots.ox.ac.uk/~vgg/data/voxceleb/) las clasificaciones actuales de la EER en los modelos.
  VoxCeleb 排行榜(2026年更新) 各模型当前 EER 排名。

> **【中文解读】**延伸阅读 proporciona recursos de alta calidad para el aprendizaje profundo, incluyendo artículos, tutorials y herramientas.

