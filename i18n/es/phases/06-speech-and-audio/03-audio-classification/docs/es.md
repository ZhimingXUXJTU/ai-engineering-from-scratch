# Clasificación de audio  De k-NN en MFCC a AST y BEATs  音频分类  de MFCC+KNN a AST y BEATs

> Todo, desde "dog barking vs sirena" hasta "qué idioma es este" es la clasificación de audio. Las características son mels. La arquitectura se mueve cada década. La evaluación permanece AUC, F1, y recall por clase.

> **【中文解读】**Desde "dog calls or警笛" hasta "This is what language", todos los tipos de sonido son de diferentes tipos de sonidos.

**Type:** Build | **类型:** 构建
**Languages:** Python | **语言:** Python
**Prerequisites:** Phase 6 · 02 (Spectrograms & Mel), Phase 3 · 06 (CNNs), Phase 5 · 08 (CNNs & RNNs for Text) | **前置知识:** 阶段 6 · 02（频谱图与 Mel），阶段 3 · 06（CNN），阶段 5 · 08（文本的 CNN 与 RNN）
**Time:** ~75 minutes | **预计用时:** ~75 分钟

## El problema es la introducción del problema

Obtienes un clip de 10 segundos. Quiere saber: "¿qué es?" sonido urbano (sirena, simulacro, perro), comando de voz (sí/no/stop), ID de idioma (en/es/ar), emoción del altavoz (enojado/neutral), o sonido ambiental (interior/exterior, babilón). Todos estos son *clasificación de audio*, y en 2026 la arquitectura de base está madura: log-mel → CNN o Transformer → softmax.

> Usted consigue un pasaje de 10 segundos de audio. Usted piensa saber:"¿Qué es esto?"

> **【中文解读】**La pregunta planteada en este capítulo es: ¿cómo entender y aplicar correctamente esta tecnología en la ingeniería real? Comprender el contexto de la cuestión ayuda a comprender los puntos clave de decisión del tipo de selección técnica. En los sistemas de IA reales, el tipo de selección técnica errónea suele ser más alto que el costo de error de la realización de detalles.

El problema principal no es la red. Son los datos. Los conjuntos de datos de audio tienen un desequilibrio de clase brutal, un fuerte cambio de dominio (limpio vs ruidoso) y ruido de etiqueta (quién decidió "barbudo urbano" vs "ruido de restaurante"?).

> ¿Quién ha definido el "ruido de la ciudad" frente al ruido de la sala de comida"?) ■ El 80% de los problemas son la organización, la mejora y la evaluación de datos, en lugar de convertir a CNN en un transformador。

## El concepto central.

> **【中文解读】**Este capítulo presenta los conceptos y teorías básicos. La comprensión de estos conceptos es el prerrequisito de la realización posterior de la actividad, y también el conocimiento de los puntos de alta frecuencia de la entrevista y la práctica de la ingeniería.


![Audio classification ladder: k-NN on MFCCs to AST to BEATs](../assets/audio-classification.svg)

**k-NN on MFCCs (the 1990s baseline).**MFCCs planos por clip, computa cosino similaridad a un banco etiquetado, devuelve el voto mayoritario de la parte superior K. Sorprendentemente fuerte en los conjuntos de datos limpios y pequeños (Comando de habla, ESC-50).

> **MFCC 上的 k-NN（1990 年代基线）。**Para calcular la similaridad de los cuerpos de la base de datos, regresar a la mayoría de los votos anteriores K 个.

**2D CNN on log-mels (2015-2019).**Tratar el`(T, n_mels)`El log-mail como una imagen. Aplicar ResNet-18 o estilo VGG. Medio global de la combinación del eje de tiempo. Softmax sobre las clases. Aún la línea de base en la mayoría de las competiciones de 2026 kaggle.

> **log-mel 上的 2D CNN（2015-2019）。**¿ Qué ?`(T, n_mels)`La mayoría de las competencias de 2026 siguen siendo básicas.

**Audio Spectrogram Transformer, AST (2021-2024).**Parchear el registro (por ejemplo, parches 16×16), añadir inserciones de posición, alimentar a un ViT. Estado de la técnica en AudioSet (mAP 0.485) para el aprendizaje supervisado.

> **音频频谱图 Transformer，AST（2021-2024）。**将 log-mail 分块((tal como 16×16 块),添加位置嵌入,送入 ViT──AudioSet 上监督学习的 SOTA(mAP 0.485)──

**BEATs and WavLM-base (2024-2026).**Pre-entrenamiento auto supervisado en millones de horas. Ajuste bien tu tarea con 1-10% de los datos supervisados que habría necesitado. En 2026 este es el punto de partida predeterminado para el audio no hablado. BEATs-iter3 supera a AST en 1-2 mAP en AudioSet mientras utiliza 1/4 de la computación.

> **BEATs 和 WavLM-base（2024-2026）。**En millones de horas de datos, la supervisión pre-entrenamiento. Utiliza el 1-10% de los datos de supervisión que usted debería necesitar en 2026 es el punto de partida de la serie de datos de supervisión.

**Whisper-encoder as a frozen backbone (2024).**Toma el codificador de Whisper, deja caer el decodificador, adjunta un clasificador lineal. Casi SOTA en ID de idioma y clasificación de eventos simple con aumento de audio cero. La línea de base de "almuerzo gratis".

> **Whisper 编码器作为冻结骨干（2024）。**取 Whisper 的编码器,丢弃解码器,接一个线性分类器──在语言ID 和简单事件分类上接近SOTA,无需任何音频增强──"免费午餐"基线──

### El desequilibrio de clases es el verdadero desafío

> ### El desequilibrio es el verdadero reto

ESC-50: 50 clases, 40 clips cada  equilibrado, fácil. UrbanSound8K: 10 clases, desequilibrado 10:1. AudioSet: 632 clases con una cola larga de 100,000:1. Técnicas que funcionan:

> ESC-50:50 个类, por clase 40 个片段平衡、简单。UrbanSound8K:10 个类,10:1 不平衡──AudioSet:632 个类,长尾比例 100,000:1──有效的技术:

- Muestreo equilibrado durante la formación (no en la evaluación).
  訓練時平衡采样 (en inglés) 
- Mezcla: interpolar linealmente dos clips (y sus etiquetas) como aumento.
  Mixup:线性插值两段音频 (en inglés) y su etiqueta) como incremento.
- SpecAugment: enmascarar el tiempo aleatorio y las bandas de frecuencia.
  EspecAugment: oscurece con tiempo y frecuencia.

### Evaluación

> ###  evaluación

- Exclusivo para múltiples clases (Comando de habla): precisión superior a 1, precisión superior a 5.
  Quizás clases de intercambio de comandos de habla: top-1 准确率、top-5 准确率。
- Multi-etiqueta de múltiples clases (AudioSet, UrbanSound-style): precisión media (mAP).
  Quizás tipo de etiquetas:
- Desbalanceado en gran medida: recuerdo por clase + macro F1.
  严重不平衡: cada clase de reclutamiento + 宏观 F1──

2026 números que usted debe saber:

> 2026 años que deberías saber números:

| Benchmark | Baseline | SOTA 2026 | Source |
|-----------|----------|-----------|--------|
| ESC-50 | 82% (AST) | 97.0% (BEATs-iter3) | BEATs paper (2024) |
| AudioSet mAP | 0.485 (AST) | 0.548 (BEATs-iter3) | HEAR leaderboard 2026 |
| Speech Commands v2 | 98% (CNN) | 99.0% (Audio-MAE) | HEAR v2 results |

| 基准测试 | 基线 | 2026 SOTA | 来源 |
|----------|------|-----------|------|
| ESC-50 | 82%（AST） | 97.0%（BEATs-iter3） | BEATs 论文（2024） |
| AudioSet mAP | 0.485（AST） | 0.548（BEATs-iter3） | HEAR 排行榜 2026 |
| Speech Commands v2 | 98%（CNN） | 99.0%（Audio-MAE） | HEAR v2 结果 |

> **【中文解读】**Este capítulo a través del código de la implementación de algoritmos centrales de cero. Este método "desde cero" puede ayudar a entender el principio detrás del marco, no se encuentra en la caja negra cuando se encuentran problemas.

> **【拓展：语音 AI 的产品化】**La tecnología de voz se enfrenta a un desafío único en la productorización: diferentes voces, ruidos de contexto, remota recogida, muchos hablar, etc.

> **【拓展：多语言语音技术】**Las características de los idiomas de todo el mundo son muy diferentes: el sonido de los idiomas de todo el mundo (como el chino) es alto, el lenguaje de bajo recurso es poco capacitado.

> **【拓展：语音隐私与安全】**语音数据 contiene una gran cantidad de información personal privada ([[音纹]], diálogo contenido) ◦ profundidad falsificación (Deepfake) 语音技术 (语音技术) puede ser utilizada para fraude (音频水印) 音频水印 (音频水印) 音纹水标 (音符标) 声纹反欺诈 (音纹反欺诈) ]] ]] ]] ]] ]] ]] ]] ]] ]] ]] ]] ]] ]] ]] ]] ]] ]] ]] ]] ]] ]] ]] ]] ]] ]] ]] ]] ]] ]] ]] ]] ]] ]] ]] ]] ]] ]] ]] ]] ]] ]] ]] ]] ]] ]] ]] ]] ]] ]] ]] ]] ]] ]] ]] ]] ]] ]] ]] ]] ]] ]] ]] ]] ]] ]] ]] ]] ]] ]] ]] ]] ]] ]] ]] ]] ]] ]] ]] ]] ]] ]] ]] ]] ]] ]] ]] ]] ]] ]] ]] ]] ]] ]] ]] ]] ]] ]]





## Construye y realiza.
```figure
mfcc-pipeline
```

## Construye el mismo

### Paso 1: Featurizar

```python
def featurize_mfcc(signal, sr, n_mfcc=13, n_mels=40, frame_len=400, hop=160):
    mag = stft_magnitude(signal, frame_len, hop)
    fb = mel_filterbank(n_mels, frame_len, sr)
    mels = apply_filterbank(mag, fb)
    log = log_transform(mels)
    return [dct_ii(frame, n_mfcc) for frame in log]
```

### Paso 2: resumen de longitud fija

```python
def summarize(mfcc_frames):
    n = len(mfcc_frames[0])
    mean = [sum(f[i] for f in mfcc_frames) / len(mfcc_frames) for i in range(n)]
    var = [
        sum((f[i] - mean[i]) ** 2 for f in mfcc_frames) / len(mfcc_frames) for i in range(n)
    ]
    return mean + var
```

Simple pero fuerte: media + variación a través del tiempo da una incorporación fija de 26 dimensiones para una MFCC de 13 cuerdas. Se ejecuta instantáneamente.

>  Simple pero válido: el promedio del eje temporal + 方差 es de 13 números en el MFCC                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                     

### Paso 3: k-NN

```python
def cosine(a, b):
    dot = sum(x * y for x, y in zip(a, b))
    na = math.sqrt(sum(x * x for x in a)) or 1e-12
    nb = math.sqrt(sum(x * x for x in b)) or 1e-12
    return dot / (na * nb)

def knn_classify(q, bank, labels, k=5):
    sims = sorted(range(len(bank)), key=lambda i: -cosine(q, bank[i]))[:k]
    votes = Counter(labels[i] for i in sims)
    return votes.most_common(1)[0][0]
```

### Paso 4: actualización a CNN en log-mels

En PyTorch:

```python
import torch.nn as nn

class AudioCNN(nn.Module):
    def __init__(self, n_mels=80, n_classes=50):
        super().__init__()
        self.body = nn.Sequential(
            nn.Conv2d(1, 32, 3, padding=1), nn.ReLU(), nn.MaxPool2d(2),
            nn.Conv2d(32, 64, 3, padding=1), nn.ReLU(), nn.MaxPool2d(2),
            nn.Conv2d(64, 128, 3, padding=1), nn.ReLU(),
            nn.AdaptiveAvgPool2d(1),
        )
        self.head = nn.Linear(128, n_classes)

    def forward(self, x):  # x: (B, 1, T, n_mels)
        return self.head(self.body(x).flatten(1))
```

Parámetros 3M. Trenes en ~10 min en ESC-50 con una sola RTX 4090. 80% + precisión.

> 300 000 parámetros. En el ESC-50 上 utiliza un solo张 RTX 4090  entrenamiento de aproximadamente 10 minutos.

### Paso 5: los 2026 por defecto  de ajuste fino BEATs

```python
from transformers import ASTFeatureExtractor, ASTForAudioClassification

ext = ASTFeatureExtractor.from_pretrained("MIT/ast-finetuned-audioset-10-10-0.4593")
model = ASTForAudioClassification.from_pretrained(
    "MIT/ast-finetuned-audioset-10-10-0.4593",
    num_labels=50,
    ignore_mismatched_sizes=True,
)

> **【中文解读】** 本节展示如何用成熟框架（如 PyTorch、HuggingFace 等）快速应用该技术。在实际项目中，优先使用经过验证的框架实现，可以减少 bug 并提高开发效率。


inputs = ext(audio, sampling_rate=16000, return_tensors="pt")
logits = model(**inputs).logits
```

Para los BEATs, utilizar `microsoft/BEATs-base`por medio de la`beats`la biblioteca; la API de los transformadores es de la misma forma.

> Para los golpe, a través `beats`库使用                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           `microsoft/BEATs-base`;transformers API de la forma es la misma:




> **【拓展：语音与情感计算】**语音 no sólo transmite información escrita, también lleva una rica cantidad de señales emocionales (en inglés: voice signal) 语调、语速、音高变化) 情感语音识别 (en inglés: speech emotion recognition, SER) 语音 no solo transmite información escrita, sino que también lleva una gran cantidad de señales emocionales (en inglés: voice signal). 语音 tiene una amplia aplicación en el campo de la evaluación de calidad de los clientes, la vigilancia de la salud mental, la educación inteligente, etc.  Los modelos actuales de SOTA se basan en modelos de entrenamiento de las ondas 2vec 2.0 o HuBERT.

## Usalo con el marco de ejecución

La pila de 2026:

> Tecnología de 2026:

| Situation | Start with |
|-----------|-----------|
| Tiny dataset (<1000 clips) | k-NN on MFCC means (your baseline) + audio augmentation |
| Medium dataset (1K–100K) | BEATs or AST fine-tune |
| Large dataset (>100K) | Train from scratch or fine-tune Whisper-encoder |
| Real-time, edge | 40-MFCC CNN, quantized to int8 (KWS-style) |
| Multi-label (AudioSet) | BEATs-iter3 with BCE loss + mixup + SpecAugment |
| Language ID | MMS-LID, SpeechBrain VoxLingua107 baseline |

| 场景 | 起始方案 |
|------|----------|
| 小数据集（<1000 段） | MFCC 均值上的 k-NN（基线）+ 音频增强 |
| 中等数据集（1K–100K） | BEATs 或 AST 微调 |
| 大数据集（>100K） | 从零训练或微调 Whisper 编码器 |
| 实时、边缘设备 | 40-MFCC CNN，量化为 int8（关键词检测风格） |
| 多标签（AudioSet） | BEATs-iter3 + BCE 损失 + mixup + SpecAugment |
| 语言识别 | MMS-LID，SpeechBrain VoxLingua107 基线 |

> **【中文解读】**Este capítulo se centra en cómo se puede implementar el modelo como producto disponible. Desde el modelo original hasta el sistema de producción, se deben considerar múltiples dimensiones de optimización de rendimiento, tratamiento de errores, control, etc.


Regla de decisión: **start with a frozen backbone, not a fresh model**La perfección de una cabeza de BEATs te da el 95% de SOTA en horas, no semanas.

>  决策规则:**从冻结骨干开始，而不是从头训练模型**❖ Las categorías de BEATs pueden alcanzar el 95% de SOTA en unas horas, en lugar de unas semanas.



## Envíe el producto .

Salvo como`outputs/skill-classifier-designer.md`. Seleccionar arquitectura, aumentos, estrategia de equilibrio de clases y métricas de evaluación para una tarea de clasificación de audio dada.

> 保存为                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           `outputs/skill-classifier-designer.md`◊ para la selección de la estructura de tareas de una determinada clase de audio, la estrategia de mejora, la estrategia de equilibrio y la evaluación de la clase ◊

## Los ejercicios.

1. **Easy.**- ¿ Qué ?`code/main.py`. El sistema de formación de base de la K-NN MFCC en un conjunto de datos sintéticos de 4 clases (tones puros en diferentes tonos).
   **简单。**运行                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           `code/main.py`◊ se encuentra en 4 clases de datos de composición ◊ diferentes sonidos de pureza) en el entrenamiento k-NN MFCC 基线── informes混矩阵──
2. **Medium.**Reemplazar`summarize`¿El agrupamiento de 4 momentos supera el valor medio + variable en el mismo conjunto de datos sintéticos?
   **中等。**¿ Qué ?`summarize`替换为 [medio, var, sesgo, kurtosis]── ¿Se encuentra la rectangularidad en el mismo conjunto de datos de composición superior al promedio + diferencia?
3. **Hard.**Usando`torchaudio`, entrenar una CNN 2D en ESC-50 plegado 1. informar 5 veces la precisión de validación cruzada. añadir SpecAugment (máscara de tiempo = 20, máscara de frecuencia = 10) y informar el delta.
   **困难。**Uso `torchaudio`, en ESC-50 plega 1 上训练 2D CNN──报告 5折交叉验证准确率──添加规格Augment(时间掩码 = 20,频率掩码 = 10)并报告差值──

> **【中文解读】**En el lenguaje de los términos "Lo que la gente dice" vs "Lo que realmente significa" se distingue entre el lenguaje diario y la definición técnica de significado.


## Términos clave .

| Term | What people say | What it actually means |
|------|-----------------|-----------------------|
| AudioSet | The ImageNet of audio | Google's 2M-clip, 632-class weakly-labeled YouTube dataset. |
| ESC-50 | Small classification benchmark | 50 classes × 40 clips of environmental sounds. |
| AST | Audio Spectrogram Transformer | ViT on log-mel patches; 2021 SOTA. |
| BEATs | Self-supervised audio | Microsoft model, iter3 leads AudioSet as of 2026. |
| Mixup | Pair augmentation | `x = λ·x1 + (1-λ)·x2; y = λ·y1 + (1-λ)·y2`. |
| SpecAugment | Mask-based augmentation | Zero-out random time and frequency bands of the spectrogram. |
| mAP | Main multi-label metric | Mean average precision across classes and thresholds. |

| 术语 | 人们常说的 | 实际含义 |
|------|-----------|---------|
| AudioSet | 音频界的 ImageNet | Google 的 200 万片段、632 类弱标注 YouTube 数据集。 |
| ESC-50 | 小型分类基准 | 50 类 × 40 个环境声音片段。 |
| AST | 音频频谱图 Transformer | log-mel 块上的 ViT；2021 SOTA。 |
| BEATs | 自监督音频 | 微软模型，iter3 截至 2026 年领先 AudioSet。 |
| Mixup | 配对增强 | `x = λ·x1 + (1-λ)·x2; y = λ·y1 + (1-λ)·y2`。 |
| SpecAugment | 掩码增强 | 将频谱图的随机时间和频率带置零。 |
| mAP | 主要多标签指标 | 各类别和阈值的平均精度均值。 |

> **【中文解读】**延伸阅读 proporciona un alto nivel de recursos para el aprendizaje profundo. Estos artículos y cursos son los referentes clásicos en el campo, adecuados para los lectores que necesitan una comprensión profunda.


## Más Leer más Leer más

- [Gong, Chung, Glass (2021). AST: Audio Spectrogram Transformer](https://arxiv.org/abs/2104.01778) la arquitectura de registro desde 20212024.
  Gong, Chung, Glass (2021). AST:音频频谱图 Transformer2021-2024 年的记录架构──
- [Chen et al. (2022, rev. 2024). BEATs: Audio Pre-Training with Acoustic Tokenizers](https://arxiv.org/abs/2212.09058) el impago de 2024+.
  Chen 等 (2022, 修订 2024). BEATs:声学 tokenizer 的音频预训练2024+ 的默认选择──
- [Park et al. (2019). SpecAugment](https://arxiv.org/abs/1904.08779) el aumento de audio dominante.
  Park 等 (2019). SpecAugmentMainstream音频增强方法──
- [Piczak (2015). ESC-50 dataset](https://github.com/karolpiczak/ESC-50) 50 clases de referencia que vive.
  Piczak (2015). ESC-50 datos continuous use  50 类基准──
- [Gemmeke et al. (2017). AudioSet](https://research.google.com/audioset/) Taxonomía de YouTube de clase 632; todavía el estándar de oro.
  Gemmeke 等 (2017). AudioSet632 类 YouTube 分类体系; todavía es un estándar de oro.

> **【中文解读】**延伸阅读 proporciona recursos de alta calidad para el aprendizaje profundo, incluyendo artículos, tutorials y herramientas.

