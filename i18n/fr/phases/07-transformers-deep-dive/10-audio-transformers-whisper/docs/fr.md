# Transformateurs audio  Architecture de murmure  Transformateur  Architecture de murmure

> L'audio est une image de fréquence au fil du temps.

> **【中文解读】**Sourire avec Transformer faire la reconnaissance et la traduction.

**Type:** Study | **类型:** 学习
**Language:**Je suis un Python .**语言:**Python
**Prerequisites:** Phase 7 · 05 (Full Transformer), Phase 7 · 08 (Encoder-Decoder), Phase 7 · 09 (ViT) | **前置知识:** Phase 7 · 05 (Full Transformer), Phase 7 · 08 (Encoder-Decoder), Phase 7 · 09 (ViT)
**Time:** ~45 minutes | **时间:** ~45 分钟

## Le problème , l' introduction du problème

Avant Whisper (OpenAI, Radford et coll. 2022), la reconnaissance automatique de la parole (ASR) de pointe signifiait les extracteurs de fonctionnalités autosuvisés wav2vec 2.0 et HuBERT  plus une tête fine-tunée. Pipelines de données de haute qualité, coûteuses, fragiles de domaine. La reconnaissance de la parole multilingue nécessitait des modèles distincts par famille de langues.

> Avant 2022, les plus avancées de l'identification automatique des voix (ASR) utilisaient les ondes 2vec 2.0 et HuBERT pour contrôler les caractéristiques de l'émetteur de données.

Whisper a fait trois paris:

> Je suis en train de faire trois remarques:

1. **Train on everything.**680.000 heures d'audio mal étiqueté, extraites d'Internet dans 97 langues, sans corpus académique propre, sans étiquettes phonémiques.
   Le mot grec traduit par " le mot grec "**用一切数据训练。**680.000 heures de diffusion sur Internet, couvrant 97 langues.
2. **Multi-task single model.**Un décodeur a été formé conjointement à la transcription, à la traduction, à la détection de l'activité vocale, à l'identification de la langue et au timestamping via des jetons de tâche.
   Le mot grec traduit par " le mot grec "**单模型多任务。**Un décodeur passe par le jeton de mission 联合 training转录、翻译、语音活动检测、语言识别和时间──
3. **Standard encoder-decoder transformer.**Le codeur consomme des spectrogrammes log-mail. Le décodeur produit des jetons de texte autoregressif. Aucun vocodeur, aucun CTC, aucun HMM.
   Le mot grec traduit par " le mot grec "**标准编码器-解码器 Transformer。**编码器消费 log-mail 频谱图──解码器自归生成文本代币──没有声码器,没有CTC,没有HMM──

Le résultat: Whisper large-v3 est robuste sur les accents, le bruit et les langages qui ont zéro données étiquetées. C'est la version par défaut de la bouche à oreille pour chaque assistant vocal open source et la plupart des commerciaux en 2026.

> 结果:Whisper large-v3 à l'oral, le bruit et les données de zéro marqueur sont tous des langues avec une rudesse. Il est le premier de chaque assistant de langage à source ouverte et de la plupart des assistants de langage professionnels.

> **【中文解读】**Les trois grandes innovations de Whisper: 1) avec 680.000 heures de formation, couvrant 97 langues; 2) un seul modèle à plusieurs tâches; 3) un transformateur à format standard;

## Le concept de base.

![Whisper pipeline: audio → mel → encoder → decoder → text](../assets/whisper.svg)

### Étape 1  Résemplaire + fenêtre

Audio à 16 kHz. Clip/pad à 30 secondes. Compute le spectrogramme log-mail: 80 billets de métro, 10 ms de décalage → ~ 3000 images × 80 fonctionnalités. C'est l'"image d'entrée" que voit Whisper.

> 音频采样率 16 kHz──剪剪/填充到30秒──计算日志-mail 频谱图:80 个梅尔频率 bin,10 ms 步长 → 约 3,000  × 80特征──这是Whisper 看到的"输入图像"──

### Étape 2  tronc convolutif

Deux couches Conv1D avec le noyau 3 et la phase 2 réduisent les 3000 images à 1 500.

> 两层 Conv1D(核大小 3,步长 2) réduira les 3000  à 1500 , réduira la longueur du séquence à moitié sans augmenter trop de paramètres

> **【拓展：Whisper 的多语言能力来源】**Whisper dans 97 种语言、68万小时音频上训练, la capacité multilinguiste provient de deux facteurs: 1) 超大规模的弱标注数据覆盖绝大多数语言; 2) 统一的BPE 词表是GPT-2 词表的超集,天然支持多语言──decoder prompt 中的语言代币如`<|zh|>`) contrôler la langue de sortie, permettant à la même modèle d'exécuter des tâches de traduction ou de transcription.

### Étape 3  encodeur

Un encodeur transformateur à 24 couches (pour les grands) sur 1 500 étapes de temps.

> Un transformateur 编码器 traitement 1500 个时间步──正弦位置编码、自注意力、GELU FFN── générer des états cachés de 1500 × 1,280──

### Étape 4  décodeur

Un décodeur transformateur à 24 couches. Il produit autorégressivement des jetons à partir d'un vocabulaire BPE qui est un superensemble de GPT-2 avec quelques jetons spéciaux audio-specifiques.

> Un transformateur de 24 niveaux 解码器──自归地从 BPE 词表生成代币,该词表是GPT-2 词表的超集,外加几个音频专用特殊代币──

### Étape 5  jetons de tâche

Le décodeur commence par des jetons de contrôle qui indiquent au modèle ce qu'il doit faire:

> Pour contrôler le jeton, ouvrez le code et dites au modèle ce qu'il doit faire.

```
<|startoftranscript|>  <|en|>  <|transcribe|>  <|0.00|>
```

ou

```
<|startoftranscript|>  <|fr|>  <|translate|>   <|0.00|>
```

Le modèle a été formé sur cette convention. Vous contrôlez la tâche par préfixe. L'équivalent de 2026 de l'instruction-tuning, mais appliqué à la parole.

> 模型按这种约定训练──你通过前控制任务──这是语音领域的指令微调等价──

> **【中文解读】**Le mécanisme de contrôle des tâches de Whisper est très élégant: en ajoutant des jetons spéciaux comme`<|transcribe|>`Ou `<|translate|>`) pour spécifier le type de tâche. C'est une "instruction de modification" dans l'application du même modèle dans le domaine du langage par le biais de différents symboles de performance.

> **【拓展：Whisper 在语音助手中的应用】**Le whisper est un composant de base de l'IA du langage en 2026[6]. De l'assistant de langage en temps réel à la production de sous-titrage vidéo, à la production de plusieurs langues, le whisper fournit un système de langage en temps réel.

### Étape 6  sortie

Le nombre de journées de recherche (largeur 5) avec un seuil de log-prob.`<|notimestamps|>`Le token est absent.

> 束搜索(宽度 5)加对数概率值──当没有 `<|notimestamps|>`Je suis en train de faire une petite annonce.

### Tailles de murmure

| Model | Params | Layers | d_model | Heads | VRAM (fp16) |
|-------|--------|--------|---------|-------|-------------|
| 模型 | 参数量 | 层数 | d_model | 头数 | 显存 (fp16) |
| Tiny | 39M | 4 | 384 | 6 | ~1 GB |
| Base | 74M | 6 | 512 | 8 | ~1 GB |
| Small | 244M | 12 | 768 | 12 | ~2 GB |
| Medium | 769M | 24 | 1024 | 16 | ~5 GB |
| Large | 1550M | 32 | 1280 | 20 | ~10 GB |
| Large-v3 | 1550M | 32 | 1280 | 20 | ~10 GB |
| Large-v3-turbo | 809M | 32 | 1280 | 20 | ~6 GB (4-layer decoder) |

Le décodeur est coupé de 32 couches à 4,8 fois plus rapide avec une régression de <1 point WER.

> Le grand v3-turbo(2024) réduira le décodeur de 32 niveaux à 4 niveaux. La vitesse de décode sera augmentée de 8 fois, le WER ne sera pas réduit à 1 个百分点.

> **【拓展：音频 Transformer 的统一趋势】**语音识别(Whisper)、语音合成(VALL-E, Kokoro)、音乐生成(MusicGen) 都在转向 Transformer 架构──核心思路相同:将音频转换为频谱图或离散代币序列,然后使用标准 Transformer 处理──

### Ce que ne fait pas Whisper

- Pas de journalisation, partagez avec une note de piane.
  Il faut le mettre en place.
- Aucun streaming en temps réel natif  la fenêtre de 30 secondes est fixe.`faster-whisper`- Je suis là .`WhisperX`) à la transmission par voie de superposition VAD +.
  Le temps de travail est de 30 secondes.`faster-whisper`- Je suis là.`WhisperX`) par le biais de VAD + 重叠实现流式处理。
- Aucun contexte de forme longue dépassant 30 s sans fragmentation externe. Cela fonctionne bien dans la pratique car la parole humaine a rarement besoin de contexte à longue portée pour la transcription.
  Il n'y a pas de bloc extérieur qui ne supporte pas le format de langage de plus de 30 secondes.

### paysage 2026

| Task | Model | Notes |
|------|-------|-------|
| 任务 | 模型 | 备注 |
| English ASR | Whisper-turbo, Moonshine | Moonshine is 4× faster on edge |
| 英语 ASR | Whisper-turbo, Moonshine | Moonshine 在边缘设备上快 4 倍 |
| Multilingual ASR | Whisper-large-v3 | 97 languages |
| 多语言 ASR | Whisper-large-v3 | 97 种语言 |
| Streaming ASR | faster-whisper + VAD | 150 ms latency targets achievable |
| 流式 ASR | faster-whisper + VAD | 可实现 150ms 延迟目标 |
| TTS | Piper, XTTS-v2, Kokoro | Encoder-decoder pattern, but Whisper-shaped |
| TTS | Piper, XTTS-v2, Kokoro | 编码器-解码器模式，但类似 Whisper |
| Audio + language | AudioLM, SeamlessM4T | Text tokens + audio tokens in one transformer |
| 音频 + 语言 | AudioLM, SeamlessM4T | 文本 token + 音频 token 在一个 Transformer 中 |

## Construisez-le et mettez-le en œuvre.
```figure
n5-mel-decode
```

## Faites-le

Regardez !`code/main.py`Nous ne formons pas Whisper, nous construisons le pipeline de spectrogrammes log-mail + formatateur de prompt de jetons de tâche. Ce sont les pièces que vous touchez réellement en production.

> 参见 `code/main.py` Nous ne faisons pas de formation: "Susper"  Nous construisons des logs-mail 频谱图管道 + 任务代码 提示格式化器──

### Étape 1: synthétiser l'audio

Générer une onde sinusoïdale de 1 seconde à 440 Hz échantillonnée à 16 kHz. 16 000 échantillons.

> Il est à l'origine d'une bande de 440 Hz à 1 seconde, avec un taux de 16 kHz.

### Étape 2: spectrogramme log-mel (simplifié)

Le spectrogramme complet de MEL a besoin de FFT. Nous faisons une version simplifiée de l'encadrement + par cadre énergie qui montre le pipeline sans avoir besoin `librosa`- Le numéro de la liste:

> Nous avons fait une version simplifiée de l'énergie, sans besoin.`librosa`Il est possible de présenter des tuyaux:

```python
def frame_signal(x, frame_size=400, hop=160):
    frames = []
    for start in range(0, len(x) - frame_size + 1, hop):
        frames.append(x[start:start + frame_size])
    return frames
```

La forme de l'énergie par cadre représente les poubelles de la pédagogie.

>  = 25 ms,步长 = 10 ms── avec Whisper's window matching──

### Étape 3: plaquette à 30 s

Whisper traite toujours des morceaux de 30 secondes.

> Sourire 总是 traiter 30 secondes de fractions.

### Étape 4: construire les jetons de commande

```python
def whisper_prompt(lang="en", task="transcribe", timestamps=True):
    tokens = ["<|startoftranscript|>", f"<|{lang}|>", f"<|{task}|>"]
    if not timestamps:
        tokens.append("<|notimestamps|>")
    return tokens
```

C'est la surface de contrôle de tâches.

> C'est la totalité de la tâche de contrôle de l'interface.

## Utilisez-le avec le cadre de réalisation

```python
import whisper
model = whisper.load_model("large-v3-turbo")
result = model.transcribe("meeting.wav", language="en", task="transcribe")
print(result["text"])
print(result["segments"][0]["start"], result["segments"][0]["end"])
```

Plus rapide et compatible avec OpenAI:

> Plus rapide, avec OpenAI compatible:

```python
from faster_whisper import WhisperModel
model = WhisperModel("large-v3-turbo", compute_type="int8_float16")
segments, info = model.transcribe("meeting.wav", vad_filter=True)
for s in segments:
    print(f"{s.start:.2f} - {s.end:.2f}: {s.text}")
```

**When to pick Whisper in 2026:**

> **2026 年何时选择 Whisper：**

- RAS multilingue avec un modèle.
  Le mot "Astron" est traduit par "Astron".
- Une transcription robuste de son son bruyant et diversifié.
  Le nombre de personnes qui ont entendu le bruit a augmenté de près de 1 000 voix.
- Réservation / prototype ASR  point de départ le plus rapide.
  Le plus rapide des démarches de recherche

**When to pick something else:**

> **何时选择其他方案：**

- La diffusion à faible latence sur Edge  Moonshine bat Whisper à une qualité correspondante.
  Lune dans la même qualité, plus vite que le sourire.
- IA en conversation en temps réel nécessitant < 200 ms  ASR de streaming dédié.
  Il faut <200ms de réel temps pour parler en français.
- Le son de la musique ne fait pas cela.
  Le mot "soupçonner" est traduit par "soupçonner".

## Envoyez-le . Produit .

Regardez !`outputs/skill-asr-configurator.md`. La compétence choisit un modèle ASR, des paramètres de décoding et un pipeline de prétraitement pour une nouvelle application de la parole.

> 参见 `outputs/skill-asr-configurator.md`◊ Cette compétence est utilisée pour la nouvelle application de la langue.

## Les exercices

1. **Easy.**On court .`code/main.py`Confirmer le nombre de images pour un signal de 1 seconde à 16 kHz avec 10 ms saut est ~ 100 images.
   Le mot " l' économie " est traduit par " l' économie ".`code/main.py` Confirmer un signal de 1 seconde à 16 kHz  10 ms 步长下约100 ──30 secondes: environ 3000 ──
2. **Medium.**Construisez le spectrogramme complet de log-mail en utilisant `numpy.fft`- Vérifiez la correspondance de 80 billets .`librosa.feature.melspectrogram(n_mels=80)`dans l'erreur numérique.
   Le mot " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " "`numpy.fft`构建完整的日志 频谱图――验证 80 个梅尔频率bin 与 `librosa.feature.melspectrogram(n_mels=80)`Dans le cadre d'une erreur de valeur, il convient de noter que:
3. **Hard.**Implémenter l'inférence de streaming: une pièce audio dans des fenêtres de 10 secondes avec une superposition de 2 secondes, exécuter Whisper sur chaque pièce, fusionner les transcriptions. Mesurer le taux d'erreur de mot par rapport au single-pass sur un échantillon de podcast de 5 minutes.
   Le temps de réaction est de 10 secondes. Le temps de réaction est de 5 minutes.

## Les termes clés

| Term | What people say | What it actually means |
|------|-----------------|-----------------------|
| 术语 | 通俗说法 | 实际含义 |
| Mel spectrogram | "Audio image" | 2D representation: frequency bins on one axis, time frames on the other; log-scaled energy per cell. |
| 梅尔频谱图 | "音频图像" | 2D 表示：一个轴是频率 bin，另一个是时间帧；每个单元是对数缩放的能量。 |
| Log-mel | "What Whisper sees" | Mel spectrogram passed through log; approximates human perception of loudness. |
| Log-mel | "Whisper 看到的" | 梅尔频谱图取对数；近似人类对响度的感知。 |
| Frame | "One time slice" | A 25 ms window of samples; overlapping at 10 ms stride. |
| 帧 | "一个时间切片" | 25 ms 的采样窗口；10 ms 步长重叠。 |
| Task token | "Prompt prefix for speech" | Special tokens like `<\|transcribe\|>` / `<\|translate\|>` in the decoder prompt. |
| 任务 token | "语音的提示前缀" | 解码器提示中的特殊 token，如 `<\|transcribe\|>` / `<\|translate\|>`。 |
| Voice activity detection (VAD) | "Find the speech" | Gate that removes silence before ASR; cuts cost massively. |
| 语音活动检测 (VAD) | "找到语音" | 在 ASR 之前去除静音的门控；大幅降低成本。 |
| CTC | "Connectionist Temporal Classification" | Classic ASR loss for alignment-free training; Whisper does NOT use it. |
| CTC | "连接主义时间分类" | 经典的 ASR 对齐无关训练损失；Whisper 不使用它。 |
| Whisper-turbo | "Small decoder, full encoder" | large-v3 encoder + 4-layer decoder; 8× faster decoding. |
| Whisper-turbo | "小解码器，全编码器" | large-v3 编码器 + 4 层解码器；解码速度提高 8 倍。 |
| Faster-whisper | "The production wrapper" | CTranslate2 reimplementation; int8 quantization; 4× faster than OpenAI's reference. |
| Faster-whisper | "生产封装器" | CTranslate2 重新实现；int8 量化；比 OpenAI 参考实现快 4 倍。 |

## Encore une lecture

- [Radford et al. (2022). Robust Speech Recognition via Large-Scale Weak Supervision](https://arxiv.org/abs/2212.04356)- Le papier à murmures.
  Le mot "soupçon" est traduit par "soupçon".
- [OpenAI Whisper repo](https://github.com/openai/whisper) code de référence + poids du modèle.`whisper/model.py`pour voir le codeur + décodeur + codeur de haut en bas en 400 lignes.
  Le code de la société est un code de la société de données.
- [OpenAI Whisper — `whisper/decoding.py`](https://github.com/openai/whisper/blob/main/whisper/decoding.py) la logique de recherche de faisceau + de jeton de tâche décrite dans les étapes 56 est ici; 500 lignes, entièrement lisibles.
  Le code de la tâche est le code de la tâche.
- [Baevski et al. (2020). wav2vec 2.0: A Framework for Self-Supervised Learning of Speech Representations](https://arxiv.org/abs/2006.11477) précurseur; encore fonctionnalités SOTA dans certains paramètres.
  Le phénomène de Whisper est toujours présent dans certains cas.
- [SYSTRAN/faster-whisper](https://github.com/SYSTRAN/faster-whisper) enveloppe de production, 4 fois plus rapide que la référence.
  Le plus rapide et le plus rapide.
- [Jia et al. (2024). Moonshine: Speech Recognition for Live Transcription and Voice Commands](https://arxiv.org/abs/2410.15608) 2024 ASR à bord, en forme de chuchotement mais plus petit.
  Le récit de l'édition de l'édition de 2021 est en cours de rédaction.
- [HuggingFace blog — "Fine-Tune Whisper For Multilingual ASR with 🤗 Transformers"](https://huggingface.co/blog/fine-tune-whisper) recette de réglage canonique, y compris le préprocesseur de spectrogramme de méle et la manipulation des timestamps de jetons.
  Le temps de la rédaction de la série est de plus en plus long.
- [HuggingFace `modeling_whisper.py`](https://github.com/huggingface/transformers/blob/main/src/transformers/models/whisper/modeling_whisper.py) mise en œuvre complète (encodeur, décodeur, attention croisée, génération) qui reflète le diagramme d'architecture de la leçon.
  Le programme est en cours de préparation et de mise en œuvre.
