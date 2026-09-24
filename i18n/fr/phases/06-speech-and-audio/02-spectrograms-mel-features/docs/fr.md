# Spectrogrammes, échelle de Mel et caractéristiques audio.

> Les réseaux neuraux ne consomment pas bien les formes d'onde brutes. Ils consomment des spectrogrammes. Ils consomment encore mieux les spectrogrammes mel. Chaque classifiateur ASR, TTS et audio en 2026 vit ou meurt par ce seul choix de préprocessage.

> **【中文解读】**Le traitement de la bande originale de la bande ne fonctionne pas bien, mais le traitement de la bande de fréquences fonctionne bien, le traitement de la bande de fréquences de la bande de fréquences est meilleur.

> **【拓展：Mel 频谱图是音频 AI 的 "图像"】**Le temps et la fréquence sont utilisés pour traiter le message.

**Type:** Build | **类型:** 构建
**Languages:** Python | **语言:** Python
**Prerequisites:** Phase 6 · 01 (Audio Fundamentals) | **前置知识:** 阶段 6 · 01（音频基础）
**Time:** ~45 minutes | **预计用时:** ~45 分钟

## Le problème , l' introduction du problème

Prenez une vidéo de 10 secondes à 16 kHz, c'est 160 000 floats, tout en`[-1, 1]`La forme d'onde brute contient les informations mais dans une forme que le modèle ne peut pas extraire facilement.

> 16 kHz de 10 secondes. C'est le nombre de 160 000 points de mouvement.`[-1, 1]`Dans le cadre, presque pas de lien avec les étiquettes "dog call" ou "单词 cat" . Les formes originales de la vague contiennent des informations, mais la forme est difficile à extraire .

> **【中文解读】**La question posée dans ce chapitre est la suivante: comment comprendre et appliquer correctement cette technique dans la conception pratique. Comprendre le contexte de la question aide à saisir les principaux facteurs de décision concernant le type de technologie. Dans les systèmes d'IA réels, le type de technique erroné coûte souvent plus cher que le coût de la mise en œuvre de détails.

Un spectrogramme corrige cela. Il effondre le détail temporel où la perception humaine l'ignore (tremblement de microseconde) et préserve la structure où la perception assiste (qui sont des fréquences énergétiques, sur des fenêtres temporelles de ~ 1025 ms).

> Le diagramme de fréquence a résolu ce problème. Il conclut les détails du temps ignoré par la perception humaine (microsécès de séquence) et conserve la structure de la perception (environ 1025 ms, quelle fréquence a de l'énergie)

Les spectrogrammes de mélomène poussent plus loin. Les humains perçoivent le pitch logarithmiquement: 100 Hz vs 200 Hz sonne "la même distance entre eux" que 1000 Hz vs 2000 Hz. L'échelle de mélomène déforme l'axe de fréquence pour correspondre. Un spectrogramme à l'échelle de mélomène est la caractéristique la plus importante du langage ML de 2010 à 2026.

> Le schéma de fréquence des humains est le même: 100 Hz et 200 Hz, et 1000 Hz et 2000 Hz sont " aussi loin ". Le schéma de fréquence des humains est le plus important dans l'apprentissage des machines de langue de 2010 à 2026.

## Le concept de base.

> **【中文解读】**Le présent article présente les concepts et les bases théoriques de base. La connaissance de ces concepts est la prémisse de la réalisation de la réalisation de la réalisation, mais aussi le point de connaissance de l'interview et de la pratique de l'ingénierie.


![Waveform to STFT to mel spectrogram to MFCC ladder](../assets/mel-features.svg)

**STFT (Short-Time Fourier Transform).**Coupez la forme d'onde en cadres superposés (typiquement: fenêtre de 25 ms, 10 ms hop = 400 échantillons / 160 échantillons à 16 kHz). Multipliez chaque cadre par une fonction de fenêtre (Hann est la fonction par défaut; Hamming un compromis légèrement différent). FFT chaque cadre. Ampiler les spectres de magnitude en une matrice de forme `(n_frames, n_freq_bins)`C'est votre spectrogramme.

> **STFT（短时傅里叶变换）。**Pour chaque action, la longueur du schéma est de 16 kHz.`(n_frames, n_freq_bins)`C'est votre tableau de fréquence.

**Log-magnitude.**Les magnitudes brutes sont de 5 à 6 ordres.`log(|X| + 1e-6)`ou `20 * log10(|X|)`Chaque pipeline de production utilise une grandeur de log, pas une grandeur brute.

> **对数幅度。**La longueur initiale est de 5 à 6 niveaux.`log(|X| + 1e-6)`Ou `20 * log10(|X|)`Pour réduire la gamme de la production, chaque ligne de production utilise la longueur de la production plutôt que la longueur d'origine.

**Mel scale.**La fréquence`f`en Hz pour les cartes à mel `m`par `m = 2595 * log10(1 + f / 700)`. Le mappage est à peu près linéaire en dessous de 1 kHz et à peu près logarithmique au-dessus.

> **Mel 尺度。** fréquence `f`(Hz) Météo à la mi`m`                `m = 2595 * log10(1 + f / 700)`◊ Le programme est diffusé à 1 kHz, à 80 mètres de 08 kHz, à l'intérieur de la norme ASR 输入──

**Mel filterbank.**Un ensemble de filtres triangulaires espacés de manière égale sur l'échelle mel. Chaque filtre est une somme pondérée des poubelles FFT adjacentes. Multiplication de la magnitude STFT par la matrice de la banque de filtres donne le spectrogramme mel en un matmul.

> **Mel 滤波器组。**Un groupe à l'échelle métale et à l'intervalle des trois côtés de la rangée. Chaque groupe est le gain et le gain de la bin FFT adjacente.

**Log-mel spectrogram.** `log(mel_spec + 1e-10)`- L'entrée de Whisper, l'entrée de Parakeet, l'entrée de Seamless M4T, le front-end audio universel 2026.

> **对数 Mel 频谱图。** `log(mel_spec + 1e-10)`❖ Whisper 的输入──Parakeet 的输入──SeamlessM4T 的输入──2026 年通用音频前端──

**MFCCs.**Prenez le spectrogramme log-mel, appliquez un DCT (type II), gardez les 13 premiers coefficients. Décorrelate les caractéristiques et comprime plus loin. Fonction dominante jusqu'en 2015 environ, lorsque les CNNs / Transformers sur les log-mels bruts ont été capturés.

> **MFCC。**取对数 Mel 频谱图,应用 DCT(类 II), retenue 之前 13 个系数──除特征间相关性并进一步压缩──2015年之前的主流特征,之后 CNN/Transformer 在原始 log-mel 上追上──仍然用于说话人识别(x-vecteurs、ECAPA)──

**Resolution trade.**Plus grand FFT = meilleure résolution de fréquence mais pire résolution de temps. 25 ms / 10 ms est la résolution audio-ML par défaut; 50 ms / 12,5 ms pour la musique; 5 ms / 2 ms pour la détection transitoire (batte de tambour, plosives).

> **分辨率权衡。**Plus grand FFT = meilleure fréquence de résolution mais moins grande de temps de résolution.

> **【拓展：语音 AI 的产品化】**La technologie du langage est confrontée à des défis particuliers dans la fabrication de produits: différents sons, bruits de fond, prises de vue, nombreux discours, etc. Les produits de Siri, Alexa, et de petite enfance ont été largement optimisés pour résoudre ces "problèmes de longue durée".

> **【拓展：多语言语音技术】**Les caractéristiques du langage mondial sont énormes: la voix de la langue (en chinois comme en chinois) est à un niveau élevé, les ressources linguistiques sont faibles et les données de formation manquent.



## Construisez-le et mettez-le en œuvre.

> **【中文解读】**Cette méthode "de zéro" peut aider à comprendre le principe derrière le cadre, en cas de problème, ne sera pas bloqué dans une boîte noire.

```figure
spectrogram-window
```

## Faites-le

### Étape 1: encadrer la forme d'onde

```python
def frame(signal, frame_len, hop):
    n = 1 + (len(signal) - frame_len) // hop
    return [signal[i * hop : i * hop + frame_len] for i in range(n)]
```

Un clip de 10 secondes à 16 kHz avec `frame_len=400, hop=160`Il donne 998 cadres.

> Une section 10 秒 16 kHz 的音频,使用 `frame_len=400, hop=160`Je suis en 998.

### Étape 2: fenêtre Hann

```python
import math

def hann(N):
    return [0.5 * (1 - math.cos(2 * math.pi * n / (N - 1))) for n in range(N)]
```

Multipliez par élément avant la FFT. Élimine la fuite spectrale causée par le troncage à des points d'extrémité non zéro.

> En FFT, les émissions de fréquences entraînant une rupture de la fréquence à des points non-zéro sont éliminées.

### Étape 3: Ampleur de la FST

```python
def stft_magnitude(signal, frame_len=400, hop=160):
    win = hann(frame_len)
    frames = frame(signal, frame_len, hop)
    return [magnitudes(dft([w * s for w, s in zip(win, f)])) for f in frames]
```

Utilisation dans la production `torch.stft`ou `librosa.stft`La boucle est pédagogique, elle se déroule sur de courts clips en`code/main.py`- Je suis désolé .

> Produit et environnement`torch.stft`Ou `librosa.stft`(basé sur la FFT ≈ météorisation) ◊ Le cycle ici est un but pédagogique; il est en`code/main.py`Il est également un film de cinéma.

### Étape 4: filtrage de la méle

```python
def hz_to_mel(f):
    return 2595.0 * math.log10(1.0 + f / 700.0)

def mel_to_hz(m):
    return 700.0 * (10 ** (m / 2595.0) - 1)

def mel_filterbank(n_mels, n_fft, sr, fmin=0, fmax=None):
    fmax = fmax or sr / 2
    mels = [hz_to_mel(fmin) + (hz_to_mel(fmax) - hz_to_mel(fmin)) * i / (n_mels + 1)
            for i in range(n_mels + 2)]
    hzs = [mel_to_hz(m) for m in mels]
    bins = [int(h * n_fft / sr) for h in hzs]
    fb = [[0.0] * (n_fft // 2 + 1) for _ in range(n_mels)]
    for m in range(n_mels):
        for k in range(bins[m], bins[m + 1]):
            fb[m][k] = (k - bins[m]) / max(1, bins[m + 1] - bins[m])
        for k in range(bins[m + 1], bins[m + 2]):
            fb[m][k] = (bins[m + 2] - k) / max(1, bins[m + 2] - bins[m + 1])
    return fb
```

80 mels couvrant 08 kHz avec `n_fft=400`donne une`(80, 201)`La matrice.`(n_frames, 201)`L' magnitude de la TFT par la transposition pour obtenir `(n_frames, 80)`Le spectrogramme de MEL.

> Couverture de 80 mL à 8 kHz,`n_fft=400`Je suis là .`(80, 201)`Je suis un homme.`(n_frames, 201)`La taille du STFT est multipliée par le transfert.`(n_frames, 80)`Le nombre de personnes qui ont été tuées est de plus de 500 personnes.

### Étape 5: log-mail

```python
def log_mel(mel_spec, eps=1e-10):
    return [[math.log(max(v, eps)) for v in frame] for frame in mel_spec]
```

Les alternatives communes: `librosa.power_to_db`(db normalité de référence),`10 * log10(power + eps)`. Whisper utilise un clip plus impliqué + normaliser la routine (voir Whisper's `log_mel_spectrogram`)

> 常见替代方案:`librosa.power_to_db`(pour référence à la définition des dB)`10 * log10(power + eps)`◊ Sous-sueur usage plus compliqué de coupe + 归一化流程(参见 Sous-sueur `log_mel_spectrogram`)。

### Étape 6: CFCM

```python
def dct_ii(x, n_coeffs):
    N = len(x)
    return [
        sum(x[n] * math.cos(math.pi * k * (2 * n + 1) / (2 * N)) for n in range(N))
        for k in range(n_coeffs)
    ]
```

> **【中文解读】**Dans ce chapitre, nous allons montrer comment utiliser un cadre mature (comme PyTorch, HuggingFace, etc.) pour appliquer rapidement cette technique.


Appliquez DCT à chaque cadre log-mel, gardez les 13 premiers coefficients. C'est votre matrice MFCC. Le premier coefficient est généralement déroulé (il encode l'énergie globale).

> Pour chaque log-mail  appliquer DCT, conserver 13 系数── voilà votre MFCC 矩阵── le premier系数 est généralement abandonné




> **【拓展：语音与情感计算】**Le langage n'est pas seulement un moyen de transmettre des informations, il est également un moyen de transmettre des signaux émotionnels riches.

## Utilisez-le avec le cadre de réalisation

La pile de 2026:

> 2026:

| Task | Features |
|------|----------|
| ASR (Whisper, Parakeet, SeamlessM4T) | 80 log-mels, 10 ms hop, 25 ms window |
| TTS acoustic model (VITS, F5-TTS, Kokoro) | 80 mels, 5–12 ms hop for fine temporal control |
| Audio classification (AST, PANNs, BEATs) | 128 log-mels, 10 ms hop |
| Speaker embedding (ECAPA-TDNN, WavLM) | 80 log-mels or raw-waveform SSL |
| Music (MusicGen, Stable Audio 2) | EnCodec discrete tokens (not mels) |
| Keyword spotting | 40 MFCCs for tiny devices |

| 任务 | 特征配置 |
|------|----------|
| ASR（Whisper、Parakeet、SeamlessM4T） | 80 log-mels，10 ms 步长，25 ms 窗口 |
| TTS 声学模型（VITS、F5-TTS、Kokoro） | 80 mels，5–12 ms 步长，精细时间控制 |
| 音频分类（AST、PANNs、BEATs） | 128 log-mels，10 ms 步长 |
| 说话人嵌入（ECAPA-TDNN、WavLM） | 80 log-mels 或原始波形 SSL |
| 音乐（MusicGen、Stable Audio 2） | EnCodec 离散 token（非 mels） |
| 关键词检测 | 40 MFCCs，用于小型设备 |

Règle générale: **if you are not working on music, start with 80 log-mels.**Le fardeau de la preuve est de toute déviation.

> 经验法则:**如果你不是在做音乐，就从 80 log-mels 开始。**Toutes les parties doivent prouver leur rationalité.



## Des pièges qui vont encore arriver en 2026

> 2026 est toujours en train de tomber

- **Mel count mismatch.**Formation à 80 mels, inférence à 128 mels, défaillance silencieuse, enregistrement de la forme des caractéristiques aux deux extrémités.
  **Mel 数量不匹配。**訓練用80m,推理用128m. 静默失败. 
- **Sample-rate mismatch upstream.**Les Mels calculés à 22,05 kHz sont différents de 16 kHz.
  **上游采样率不匹配。**Le taux de débit de la moyenne de la fréquence de calcul est de 22,05 kHz par rapport à 16 kHz.
- **dB vs log.**Whisper s'attend à ce que le code log-mel, pas le dB-mel, soit détecté par lui-même.
  **dB 与 log。**Whisper 期望 log-mel et non dB-mel。 certains HF 流水线会自动检测; votre code de définion ne le fera pas。
- **Normalization drift.**Normalité par éternuement pendant l'entraînement, normalité globale pendant l'inférence.
  **归一化漂移。**                                                                                                                                                                                                                                                              
- **Leakage from padding.**Le rembourrage à zéro de l'extrémité d'un clip produit un spectre plat dans les cadres arrière.
  **填充泄漏。**Pour les émissions de musique, le terme "réfléchisse" est utilisé pour désigner le "réfléchisse".

> **【中文解读】**Cette section se concentre sur la façon de déployer le modèle en tant que produit disponible. De l'original au système de production, il faut considérer plusieurs dimensions de l'optimisation des performances, du traitement des erreurs, du contrôle, etc.


## Envoyez-le . Produit .

- Je ne sais pas .`outputs/skill-feature-extractor.md`. La compétence choisit le type de fonctionnalité, le nombre de mélanges, le cadre/hop et la normalisation pour un modèle donné.

> 保存为 `outputs/skill-feature-extractor.md` Cette compétence est utilisée pour le choix des caractéristiques de type, de nombre, de longueur de pas et de mode de regroupement.

## Les exercices

1. **Easy.**On court .`code/main.py`Il synthétise un chirp (frequence balayée 200 → 4000 Hz) et imprime le bin argmax mel par cadre.
   **简单。**运行  référencement`code/main.py`◊ elle synthétise un signal  fréquence de 200 扫 à 4000 Hz)  imprime le maximum de argmax de chaque bin 
2. **Medium.**Retournez avec `n_mels`dans `{40, 80, 128}`et `frame_len`dans `{200, 400, 800}`- Mesurer la bande passante à hauteur de pointe à travers l'axe temporel.
   **中等。**- Je veux le faire .`n_mels`Pour`{40, 80, 128}`et `frame_len`Pour`{200, 400, 800}`重新运行. Quelle est la meilleure combinaison pour détecter les signaux ?
3. **Hard.**Mise en œuvre `power_to_db`et comparer la précision ASR d'un minuscule classifiateur CNN sur AudioMNIST en utilisant (a) le log-mel brut, (b) le dB-mel avec `ref=max`C) MFCC-13 + delta + delta-delta.
   **困难。** réaliser `power_to_db`, en AudioMNIST 上Utilisez le micro type CNN 分类器比较 (a)`ref=max`Le taux de réaction des données de référence de la CFAE est de 0,5% en moyenne.

> **【中文解读】**Dans le tableau des termes, la définition du terme "ce que les gens disent" et "ce qu'il signifie réellement" est différenciée entre le langage quotidien et la signification technique précise.


## Les termes clés

| Term | What people say | What it actually means |
|------|-----------------|-----------------------|
| Frame | A slice | 25 ms chunk of waveform fed to one FFT. |
| Hop | Stride | Samples between consecutive frames; 10 ms is ASR default. |
| Window | Hann/Hamming thing | Point-wise multiplier that tapers the frame edges to zero. |
| STFT | Spectrogram generator | Framed + windowed FFT; yields time × frequency matrix. |
| Mel | Warped frequency | Log-perception scale; `m = 2595·log10(1 + f/700)`. |
| Filterbank | The matrix | Triangular filters that project STFT onto mel bins. |
| Log-mel | Whisper's input | `log(mel_spec + eps)`; standardized in 2026. |
| MFCC | Old-school feature | DCT of log-mel; 13 coeffs, decorrelated. |

| 术语 | 人们常说的 | 实际含义 |
|------|-----------|---------|
| 帧 | 一段切片 | 送入一次 FFT 的 25 ms 波形片段。 |
| 步长 | 步幅 | 连续帧之间的采样点数；10 ms 是 ASR 默认值。 |
| 窗函数 | Hann/Hamming 那个东西 | 将帧边缘逐渐缩减为零的逐点乘数。 |
| STFT | 频谱图生成器 | 分帧 + 加窗的 FFT；产生时间 × 频率矩阵。 |
| Mel | 扭曲的频率 | 对数感知尺度；`m = 2595·log10(1 + f/700)`。 |
| 滤波器组 | 那个矩阵 | 将 STFT 投影到 mel bin 的三角滤波器。 |
| Log-mel | Whisper 的输入 | `log(mel_spec + eps)`；2026 年标准化。 |
| MFCC | 老派特征 | log-mel 的 DCT；13 个系数，去相关。 |

> **【中文解读】**延伸阅读 fournit des ressources de haute qualité pour l'apprentissage en profondeur. Ces articles et cours sont des références classiques dans ce domaine, adaptés aux lecteurs qui ont besoin d'une compréhension approfondie.


## Encore une lecture

- [Davis, Mermelstein (1980). Comparison of parametric representations for monosyllabic word recognition](https://ieeexplore.ieee.org/document/1163420) le document de la CFPM.
  Davis、Mermelstein (1980) 单音节词识别的参数化表示比较MFCC 论文──
- [Stevens, Volkmann, Newman (1937). A Scale for the Measurement of the Psychological Magnitude Pitch](https://pubs.aip.org/asa/jasa/article-abstract/8/3/185/735757/) l'échelle de la méle originale.
  Stevens Volkmann Newman (1937)  psychologie 高量级的尺度尺度 原始 mel 尺度
- [OpenAI — Whisper source, log_mel_spectrogram](https://github.com/openai/whisper/blob/main/whisper/audio.py) lire la mise en œuvre de référence.
  Ouvrir le code de l'émission, enregistrer le spectre
- [librosa feature extraction docs](https://librosa.org/doc/main/feature.html) référence à `mfcc`- Je suis là .`melspectrogram`, et le saut / fenêtre.
  bibliothèque`mfcc`- Je suis là.`melspectrogram`Et le point de vue de la fenêtre.
- [NVIDIA NeMo — audio preprocessing](https://docs.nvidia.com/deeplearning/nemo/user-guide/docs/en/main/asr/asr_all.html#featurizers) pipeline à l'échelle de la production pour les modèles Parakeet + Canary.
  NVIDIA NeMo音频预处理Parakeet + Canary 模型的生产级流水线──

> **【中文解读】**延伸阅读 a fourni des ressources de haute qualité pour l'apprentissage en profondeur, y compris des articles, des cours et des outils.

