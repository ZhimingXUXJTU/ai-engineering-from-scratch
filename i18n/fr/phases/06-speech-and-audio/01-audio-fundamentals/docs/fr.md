# Les fondements audio  Des ondes, des échantillons, des transformations Fourier  音频基础  波形、采样与里叶变换

> Les formes d'onde sont le signal brut. Les spectrogrammes sont la représentation. Les caractéristiques Mel sont la forme ML-friendly. Chaque pipeline moderne ASR et TTS marche cette échelle, et le premier pas est la compréhension de l'échantillonnage et Fourier.

> **【中文解读】**Le schéma de fréquence est le schéma de la fréquence, le schéma de fréquence est le schéma de la fréquence.

> **【拓展：音频 AI 的基础】**Le taux de fréquence (tels que 16 kHz) détermine la fréquence maximale indiquée.

**Type:** Learn | **类型:** 学习
**Languages:** Python | **语言:** Python
**Prerequisites:** Phase 1 · 06 (Vectors & Matrices), Phase 1 · 14 (Probability Distributions) | **前置知识:** 阶段 1 · 06（向量与矩阵），阶段 1 · 14（概率分布）
**Time:** ~45 minutes | **预计用时:** ~45 分钟

## Le problème , l' introduction du problème

Un microphone produit un signal de pression contre temps. Votre réseau neural consomme des tensors. Entre eux se trouve une pile de conventions qui, lorsqu'elles sont violées, produisent des bugs silencieux: le modèle fonctionne bien mais le WER double, ou TTS envoie un sifflement, ou un système de clonage vocale mémorise le microphone au lieu de l'enceinte.

> 麦克风产生一个压力-时间信号―― Votre consommation de réseau neural est de la quantité de张―― entre les deux, il existe une série de conventions qui enfreignent ces conventions et génèrent des bugs de l'inconnu: le modèle entraîne normalement mais est double, ou TTS 输出声, ou encore le langage du système de langage qui se souvient du麦克风 plutôt que de parler à l'homme――

> **【中文解读】**La question posée dans ce chapitre est la suivante: comment comprendre et appliquer correctement cette technique dans la conception pratique. Comprendre le contexte de la question aide à saisir les principaux facteurs de décision concernant le type de technologie. Dans les systèmes d'IA réels, le type de technique erroné coûte souvent plus cher que le coût de la mise en œuvre de détails.

Chaque bug dans les systèmes de parole remonte à une des trois questions:

> Chaque bug dans le système de voix peut être daté de l'une des trois questions suivantes:

1. À quel taux de l'échantillon les données ont-elles été enregistrées, et à quoi le modèle s'attend-il?
   Quel est le taux d'enregistrement des données, quel est le taux d'échantillonnage des modèles ?
2. Le signal est alias ?
   - Il y a un signal de confusion ?
3. Vous opérez sur des échantillons bruts ou sur une représentation de fréquence ?
   Vous traitez le point de sample original ou la fréquence de la montre ?

Si vous faites ça correctement, le reste de la phase 6 est traitable, mais même Whisper-Large-v4 produit des ordures.

> Pour résoudre ces trois problèmes, le reste de la phase 6 est facile à comprendre.

## Le concept de base.

> **【中文解读】**Le présent article présente les concepts et les bases théoriques de base. La connaissance de ces concepts est la prémisse de la réalisation de la réalisation de la réalisation, mais aussi le point de connaissance de l'interview et de la pratique de l'ingénierie.


![Waveform, sampling, DFT, and frequency bins visualized](../assets/audio-fundamentals.svg)

**Waveform.**Un ensemble unidimensionnel de flottes dans `[-1.0, 1.0]`Pour convertir en secondes, partager par le taux d'échantillonnage:`t = n / sr`Une vidéo de 10 secondes à 16 kHz est un array de 160 000 floats.

> **波形（Waveform）。**Une valeur en`[-1.0, 1.0]`间一维浮点数组──以采样编为索引──应转换为秒数,除以采样率:`t = n / sr`◊ un passage de 10 secondes 16 kHz 音频 est un nombre de 160 000 个浮点数.

**Sampling rate (sr).**Combien d'échantillons par seconde.

> **采样率（sr）。**Nombre de points d'échantillonnage par seconde:

| Rate | Use |
|------|-----|
| 8 kHz | Telephony, legacy VOIP. Nyquist at 4 kHz kills consonants. Avoid for ASR. |
| 16 kHz | ASR standard. Whisper, Parakeet, SeamlessM4T v2 all consume 16 kHz. |
| 22.05 kHz | TTS vocoder training for older models. |
| 24 kHz | Modern TTS (Kokoro, F5-TTS, xTTS v2). |
| 44.1 kHz | CD audio, music. |
| 48 kHz | Film, pro audio, high-fidelity TTS (VALL-E 2, NaturalSpeech 3). |

| 采样率 | 用途 |
|--------|------|
| 8 kHz | 电话、传统 VOIP。奈奎斯特频率 4 kHz 会丢失辅音。ASR 应避免使用。 |
| 16 kHz | ASR 标准。Whisper、Parakeet、SeamlessM4T v2 均使用 16 kHz。 |
| 22.05 kHz | 旧模型 TTS 声码器训练。 |
| 24 kHz | 现代 TTS（Kokoro、F5-TTS、xTTS v2）。 |
| 44.1 kHz | CD 音质、音乐。 |
| 48 kHz | 电影、专业音频、高保真 TTS（VALL-E 2、NaturalSpeech 3）。 |

**Nyquist-Shannon.**Un taux d'échantillonnage de `sr`peut représenter sans ambiguïté des fréquences allant jusqu' à `sr/2`- Le .`sr/2`La limite est la fréquence Nyquist. L'énergie au-dessus de Nyquist est *aliasée*  pliée vers le bas dans les fréquences plus basses  et corrompt le signal.

> **奈奎斯特-香农定理。**采样率 `sr`Ça peut être le plus haut.`sr/2`La fréquence de la réaction`sr/2`La limite est la fréquence de l'énergie de l'énergie de l'énergie de l'énergie de l'énergie de l'énergie de l'énergie de l'énergie de l'énergie de l'énergie de l'énergie de l'énergie de l'énergie de l'énergie de l'énergie de l'énergie de l'énergie de l'énergie de l'énergie de l'énergie de l'énergie de l'énergie de l'énergie de l'énergie de l'énergie de l'énergie de l'énergie de l'énergie de l'énergie de l'énergie de l'énergie de l'énergie de l'énergie de l'énergie de l'énergie de l'énergie de l'énergie de l'énergie de l'énergie de l'énergie de l'énergie de l'énergie de l'énergie de l'énergie de l'énergie de l'énergie de l'énergie de l'énergie de l'énergie de l'énergie de l'énergie de l'énergie de l'énergie de l'énergie de l'énergie de l'énergie de l'énergie de l'énergie de l'énergie de l'énergie de l'énergie de l'énergie de l'énergie de l'énergie de l'énergie de l'énergie de l'énergie de l'énergie de l'énergie de l'énergie de l'énergie de l'énergie de l'énergie de l'énergie de l'énergie de l'énergie de l'énergie de l'énergie de l'énergie de l'énergie de l'énergie de l'énergie de l'énergie de l'énergie de l'énergie de l'énergie de l'énergie de l'énergie de l'énergie de l'énergie de l'énergie de l'énergie de l'énergie de l'énergie de l'énergie de l'énergie de l'énergie de l'énergie de l'énergie de l'énergie de l'énergie de l'énergie de l'énergie de l'énergie de l'énergie de l'énergie de l'énergie de l'énergie de l'énergie de l'énergie de l'énergie de l'énergie de l'énergie de l'énergie de l'énergie de l'énergie de l'énergie de l'énergie de l'énergie de l'énergie de l'énergie de l'énergie de l'énergie de l'énergie de l'énergie de l'énergie

**Bit depth.**Le PCM à 16 bits (signé int16, plage ±32.767) est le format d'échange universel.`soundfile`lire int16 mais exposer les matrices float32 dans `[-1, 1]`- Je suis désolé .

> **位深度。**16 位 PCM(有符号 int16,范围 ±32,767) est un format de commutation général.`soundfile`J'attends de lire le 16 mais je reviens.`[-1, 1]`范围的浮动32 数组──

**Fourier Transform.**Tout signal fini est une somme de sinus à différentes fréquences.`N`échantillons `N`coefficients complexes  un par bac à fréquences. `bin k`cartes à fréquence `k · sr / N`La magnitude est l'amplitude à cette fréquence, l'angle est la phase.

> **傅里叶变换。**Tout signal limité peut être décomposé en différentes fréquences de la fréquence des ondes de l'or.`N`个采样点计算 `N`个复数系数 个频率 bin 个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个`bin k`Pour la fréquence de traitement`k · sr / N`Hz. La longueur est la longueur de la fréquence, l'angle est la phase.

**FFT.**Transformation rapide de Fourier: une `O(N log N)`algorithme pour le DFT lorsque `N`Une FFT de 1024 échantillons à 16 kHz donne 512 poubelles de fréquences utilisables couvrant 08 kHz à une résolution de 15,6 Hz.

> **FFT。**快速里叶变换:当 `N`Pour 2 de l'heure,DFT de `O(N log N)`L'algorithme. Tous les niveaux de base de la base de son utilisent FFT. 16 kHz.

**Framing + window.**Nous ne faisons pas FFT d'un clip entier. Nous le couperons en *frame* qui se chevauchent (généralement 25 ms avec 10 ms hop), multiplier chaque cadre par une fonction de fenêtre (Hann, Hamming) pour supprimer les discontinuités de bord, puis FFT chaque cadre.

> **分帧 + 加窗。**Nous ne faisons pas de FFT à l'ensemble du son. Nous le faisons en coupe de coupe de coupe.

> **【拓展：语音 AI 的产品化】**La technologie du langage est confrontée à des défis particuliers dans la fabrication de produits: différents sons, bruits de fond, prises de vue, nombreux discours, etc. Les produits de Siri, Alexa, et de petite enfance ont été largement optimisés pour résoudre ces "problèmes de longue durée".

> **【拓展：多语言语音技术】**Les caractéristiques du langage mondial sont énormes: la voix de la langue (en chinois comme en chinois) est à un niveau élevé, les ressources linguistiques sont faibles et les données de formation manquent.



## Construisez-le et mettez-le en œuvre.

> **【中文解读】**Cette méthode "de zéro" peut aider à comprendre le principe derrière le cadre, en cas de problème, ne sera pas bloqué dans une boîte noire.

```figure
mel-scale
```

## Faites-le

### Étape 1: lire un clip et tracer la forme d'onde

`code/main.py`utilise uniquement le stdlib `wave`Le module de démo pour garder la démo libre de dépendance.`soundfile`ou `torchaudio.load`(les deux retournent `(waveform, sr)`- les deux couches:

> `code/main.py`                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             `wave`模块以保持演示无依赖. 生产环境你会使用 `soundfile`Ou `torchaudio.load`(Les deux sont de retour `(waveform, sr)`- Je suis un homme.

```python
import soundfile as sf
waveform, sr = sf.read("clip.wav", dtype="float32")  # shape (T,), sr=int
```

### Étape 2: synthétiser une onde sine à partir des premiers principes

```python
import math

def sine(freq_hz, sr, seconds, amp=0.5):
    n = int(sr * seconds)
    return [amp * math.sin(2 * math.pi * freq_hz * i / sr) for i in range(n)]
```

Un sinus de 440 Hz (concert A) à 16 kHz pendant 1 seconde est de 16 000 flottes.`wave.open(..., "wb")`en utilisant le codage PCM à 16 bits.

> 16 kHz 采样率下 440 Hz 正弦波(标准音 A) durée 1 秒 est de 16 000 个浮点数──使用 `wave.open(..., "wb")`É 16 places PCM 编码写入。

### Étape 3: calculer le DFT à la main

```python
def dft(x):
    N = len(x)
    out = []
    for k in range(N):
        re = sum(x[n] * math.cos(-2 * math.pi * k * n / N) for n in range(N))
        im = sum(x[n] * math.sin(-2 * math.pi * k * n / N) for n in range(N))
        out.append((re, im))
    return out
```

`O(N²)` bien pour `N=256`Pour confirmer la précision, inutile pour l'audio réel.`numpy.fft.rfft`ou `torch.fft.rfft`- Je suis désolé .

> `O(N²)`La complexité`N=256`验证正确性还行,对真实音频没有用──实际代码调用 `numpy.fft.rfft`Ou `torch.fft.rfft`Il y a une autre.

### Étape 4: trouver la fréquence dominante

Indice de pointe de la magnitude `k_star`cartes à fréquence `k_star * sr / N`En exécutant ce sur le sinus de 440 Hz , il devrait retourner un pic à bin .`440 * N / sr`- Je suis désolé .

> 幅度峰值索引 `k_star`Pour la fréquence de traitement`k_star * sr / N`◊ à 440 Hz 正弦波运行`440 * N / sr`Retour à la valeur de la plus haute.

### Étape 5: démontrer l'aliasing

Prenez un signe de 7 kHz à 10 kHz (Nyquist = 5 kHz).`10 − 7 = 3 kHz`Le pic FFT apparaît à 3 kHz. C'est la démo d'alias classique et la raison pour laquelle chaque DAC/ADC envoie un filtre à basse fréquence.

> À partir de 10 kHz 采样 7 kHz 正弦波(奈奎斯特频率 = 5 kHz)`10 − 7 = 3 kHz`Le maximum de FFT est présent à 3 kHz. C'est la raison de la mise en place classique de chaque DAC/ADC.

> **【中文解读】**Dans ce chapitre, nous allons montrer comment utiliser un cadre mature (comme PyTorch, HuggingFace, etc.) pour appliquer rapidement cette technique.





> **【拓展：语音与情感计算】**Le langage n'est pas seulement un moyen de transmettre des informations, il est également un moyen de transmettre des signaux émotionnels riches.

## Utilisez-le avec le cadre de réalisation

La pile que vous expédierez en 2026:

> 2026 années que vous allez utiliser réellement:

| Task | Library | Why |
|------|---------|-----|
| Read/write WAV/FLAC/OGG | `soundfile` (libsndfile wrapper) | Fastest, stable, returns float32. |
| Resample | `torchaudio.transforms.Resample` or `librosa.resample` | Correct anti-aliasing built in. |
| STFT / Mel | `torchaudio` or `librosa` | GPU-friendly; PyTorch ecosystem. |
| Real-time streaming | `sounddevice` or `pyaudio` | Cross-platform PortAudio bindings. |
| Inspect a file | `ffprobe` or `soxi` | CLI, fast, reports sr/channels/codec. |

| 任务 | 库 | 原因 |
|------|----|------|
| 读写 WAV/FLAC/OGG | `soundfile`（libsndfile 封装） | 最快、最稳定，返回 float32。 |
| 重采样 | `torchaudio.transforms.Resample` 或 `librosa.resample` | 内置正确的抗混叠滤波。 |
| STFT / Mel | `torchaudio` 或 `librosa` | GPU 友好；PyTorch 生态。 |
| 实时流 | `sounddevice` 或 `pyaudio` | 跨平台 PortAudio 绑定。 |
| 检查文件 | `ffprobe` 或 `soxi` | 命令行工具，快速报告采样率/声道/编码。 |

> **【中文解读】**Cette section se concentre sur la façon de déployer le modèle en tant que produit disponible. De l'original au système de production, il faut considérer plusieurs dimensions de l'optimisation des performances, du traitement des erreurs, du contrôle, etc.


Règle de décision: **match sample rate before you match anything else**S'il vous plaît, passez-le à 44,1 kHz et vous obtiendrez des ordures qui ressemblent à un bug de modèle.

> Règles de décision:**在匹配其他任何东西之前先匹配采样率**❖ Sous-suce 期望 16 kHz 单声道 float32──传入 44.1 kHz 立体声, vous allez avoir l'air comme une sortie de déchets de bugs du modèle──

> **【中文解读】** Exercices de base selon Easy/Medium/Hard 三个难度递进──建议至少完成  级别的题目,  级别适合深入研究或面试准备──




## Envoyez-le . Produit .

- Je ne sais pas .`outputs/skill-audio-loader.md`La compétence vous aide à vérifier que l'entrée audio correspond aux attentes du modèle en aval et à reproduire correctement quand elle ne le fait pas.

> 保存为 `outputs/skill-audio-loader.md`◊ Cette compétence vous aide à vérifier si les données de l'entrée audio correspondent aux attentes du modèle et à les reprendre correctement si elles ne correspondent pas.

## Les exercices

1. **Easy.**Synthétisez un mélange de 1 seconde de 220 Hz + 440 Hz + 880 Hz à 16 kHz. Exécutez DFT. Confirmez trois pics aux poubelles attendues.
   **简单。**合成 un signal mixte de 1 seconde de 220 Hz + 440 Hz + 880 Hz, taux d'échantillonnage de 16 kHz──运行 DFT── confirmer que la position prévue du bin 位置  possède trois sommets──
2. **Medium.**Enregistrez un WAV de 3 secondes de votre voix à 48 kHz.`torchaudio.transforms.Resample`(avec anti-aliasing), puis à 16 kHz en utilisant une décimation naïve (tous les trois échantillons).
   **中等。**Récordée à 3 secondes 48 kHz`torchaudio.transforms.Resample`(带抗混叠)降采样到16 kHz, puis avec simple extraction (((每隔三个样本取一个)降采样到16 kHz──对两者做FFT──混叠现出哪里?
3. **Hard.**Construire le STFT à partir de zéro en utilisant seulement `math`et le DFT de l'étape 3. Taille de cadre 400, hop 160, fenêtre Hann.`matplotlib.pyplot.imshow`C'est le spectrogramme de la leçon 02.
   **困难。**                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             `math`Et le 3ème étape de la DFT est de la construction de STFT.`matplotlib.pyplot.imshow`C'est le tableau de fréquence du deuxième cours.

> **【中文解读】**Dans le tableau des termes, la définition du terme "ce que les gens disent" et "ce qu'il signifie réellement" est différenciée entre le langage quotidien et la signification technique précise.


## Les termes clés

| Term | What people say | What it actually means |
|------|-----------------|-----------------------|
| Sample rate | How many samples per second | Frequency in Hz at which the ADC measures the signal. |
| Nyquist | The max frequency you can represent | `sr/2`; energy above it aliases back down. |
| Bit depth | Resolution of each sample | `int16` = 65,536 levels; `float32` = 24-bit precision in `[-1, 1]`. |
| DFT | The Fourier transform for sequences | `N` samples → `N` complex frequency coefficients. |
| FFT | The fast DFT | `O(N log N)` algorithm requiring `N` = power of 2. |
| Bin | Frequency column | `k · sr / N` Hz; resolution = `sr / N`. |
| STFT | Spectrogram under the hood | Framed + windowed FFT over time. |
| Aliasing | Weird frequency ghosts | Energy above Nyquist mirroring down to lower bins. |

| 术语 | 人们常说的 | 实际含义 |
|------|-----------|---------|
| 采样率 | 每秒多少个采样点 | ADC 测量信号的频率（Hz）。 |
| 奈奎斯特 | 能表示的最大频率 | `sr/2`；超过它的能量会混叠回来。 |
| 位深度 | 每个采样点的精度 | `int16` = 65,536 级；`float32` = `[-1, 1]` 中 24 位精度。 |
| DFT | 序列的傅里叶变换 | `N` 个采样 → `N` 个复数频率系数。 |
| FFT | 快速 DFT | `O(N log N)` 算法，要求 `N` 为 2 的幂。 |
| Bin | 频率列 | `k · sr / N` Hz；分辨率 = `sr / N`。 |
| STFT | 频谱图的底层实现 | 分帧 + 加窗的 FFT 随时间推移。 |
| 混叠 | 奇怪的频率鬼影 | 超过奈奎斯特的能量镜像到更低的 bin。 |

> **【中文解读】**延伸阅读 fournit des ressources de haute qualité pour l'apprentissage en profondeur. Ces articles et cours sont des références classiques dans ce domaine, adaptés aux lecteurs qui ont besoin d'une compréhension approfondie.


## Encore une lecture

- [Shannon (1949). Communication in the Presence of Noise](https://people.math.harvard.edu/~ctm/home/text/others/shannon/entropy/entropy.pdf) le document derrière le théorème de l'échantillonnage.
  Shannon (1949) 带噪音条件下的通信采样定理后背的论文──
- [Smith — The Scientist and Engineer's Guide to Digital Signal Processing](https://www.dspguide.com/ch8.htm) livre de cours canonique gratuit sur les SPD.
  Le guide de traitement des signaux numériques des scientifiques et des ingénieurs Smith
- [librosa docs — audio primer](https://librosa.org/doc/latest/tutorial.html) un parcours pratique avec le code.
  bibliothèque 文档音频入门带代码的实践教程──
- [Heinrich Kuttruff — Room Acoustics (6th ed.)](https://www.routledge.com/Room-Acoustics/Kuttruff/p/book/9781482260434) référence pour expliquer pourquoi l'audio du monde réel n'est pas un sinus propre.
  Heinrich Kuttruff 房间声学(第 6 版)  Expliquer pourquoi le réel monde son est pas propre à la musique.
- [Steve Eddins — FFT Interpretation notebook](https://blogs.mathworks.com/steve/2020/03/30/fft-spectrum-and-spectral-densities/)L'intuition du bac à fréquences a été nettoyée en 10 minutes.
  Steve Eddins FFT 解读笔记10 分钟搞清频率 bin 的直觉──

> **【中文解读】**延伸阅读 a fourni des ressources de haute qualité pour l'apprentissage en profondeur, y compris des articles, des cours et des outils.

