# Classification audio  De k-NN sur les MFCC à AST et BEATs  音频分类  De MFCC+KNN à AST 和 BEATs

> Tout, de " chien aboyer contre la sirène " à " quel langage est ce " est la classification audio. Les caractéristiques sont des mels. L'architecture se déplace chaque décennie. L'évaluation reste AUC, F1, et par classe rappel.

> **【中文解读】**De "dog calling还是警笛" à "这是什么语言", sont toutes des catégories de son (audio) et de son (audio) de la série.

**Type:** Build | **类型:** 构建
**Languages:** Python | **语言:** Python
**Prerequisites:** Phase 6 · 02 (Spectrograms & Mel), Phase 3 · 06 (CNNs), Phase 5 · 08 (CNNs & RNNs for Text) | **前置知识:** 阶段 6 · 02（频谱图与 Mel），阶段 3 · 06（CNN），阶段 5 · 08（文本的 CNN 与 RNN）
**Time:** ~75 minutes | **预计用时:** ~75 分钟

## Le problème , l' introduction du problème

Vous obtenez un clip de 10 secondes. Vous voulez savoir: "Qu'est-ce que c'est?" Son urbain (sirène, exercice, chien), commandement de la parole (oui/non/arrêt), ID de langue (en/es/ar), émotion des haut-parleurs (énervé/neutral), ou son environnemental (intérieur/extérieur, babble).

> Vous avez un passage de 10 secondes de son. Vous savez: "Qu'est-ce que c'est ?" Les sons de la ville: "C'est un son" (en anglais: "C'est un son")

> **【中文解读】**La question posée dans ce chapitre est la suivante: comment comprendre et appliquer correctement cette technique dans la conception pratique. Comprendre le contexte de la question aide à saisir les principaux facteurs de décision concernant le type de technologie. Dans les systèmes d'IA réels, le type de technique erroné coûte souvent plus cher que le coût de la mise en œuvre de détails.

Le problème principal n'est pas le réseau. Ce sont les données. Les ensembles de données audio ont un déséquilibre de classe brutal, un fort changement de domaine (nettous contre bruyant) et le bruit d'étiquette (qui a décidé " babble urbain " contre " bruit de restaurant ").

> Le problème principal n'est pas le net, mais dans les données. Le groupe de données a une série de catégories d'inéquilibres, de déviations de champs et de bruit de marque. Qui a défini "bruit de ville" contre "bruit de salle"?

## Le concept de base.

> **【中文解读】**Le présent article présente les concepts et les bases théoriques de base. La connaissance de ces concepts est la prémisse de la réalisation de la réalisation de la réalisation, mais aussi le point de connaissance de l'interview et de la pratique de l'ingénierie.


![Audio classification ladder: k-NN on MFCCs to AST to BEATs](../assets/audio-classification.svg)

**k-NN on MFCCs (the 1990s baseline).**MFCC plates par clip, calculer la similitude cosine à une banque étiquetée, retourner le vote majoritaire du K supérieur. Surprenantement fort sur les petits ensembles de données propres (Speech Commands, ESC-50).

> **MFCC 上的 k-NN（1990 年代基线）。**Pour calculer la similitude des états de la carte de référence, il faut revenir à la majorité des voix de K 个.

**2D CNN on log-mels (2015-2019).**Traiter le `(T, n_mels)`La moyenne globale de l'axe de temps. Softmax sur les classes. Toujours la ligne de base dans la plupart des concours de 2026 kaggle.

> **log-mel 上的 2D CNN（2015-2019）。**Il va`(T, n_mels)`Les résultats de la recherche ont été obtenus en utilisant le système de gestion des images de la classe de la classe de la classe de la classe de la classe de la classe de la classe de la classe de la classe de la classe de la classe de la classe de la classe de la classe de la classe de la classe de la classe de la classe de la classe de la classe de la classe de la classe de la classe de la classe de la classe de la classe de la classe de la classe de la classe de la classe de la classe de la classe de la classe de la classe de la classe de la classe de la classe de la classe de la classe de la classe de la classe de la classe de la classe de la classe de la classe de la classe de la classe de la classe de la classe de la classe de la classe de la classe de la classe de la classe de la classe de la classe de la classe de la classe de la classe de la classe de la classe de la classe de la classe de la classe de la classe de la classe de la classe de la classe de la classe de la classe de la classe de la classe de la classe de la classe de la classe de la classe de la classe de la classe de la classe de la classe de la classe de la classe de la classe de la classe de la classe de la classe de la classe de la classe de la classe de la classe de la classe de la classe de la classe de la classe de la classe de la classe de la classe de la classe de la classe de la classe de la classe de la classe de la classe de la classe de la classe de la classe de la classe de la classe de la classe de la classe de la classe de la classe de la classe de la classe de la classe de la classe de la classe de la classe de la classe de la classe de la classe de la classe de la classe de la classe de la classe de la classe de la classe de la classe de la classe de la classe de la classe de la classe de la classe de la classe de la classe de la classe de la classe de la classe de la classe de la classe de la classe de la classe de la classe de la classe de la classe de la classe de la classe de la classe de la classe de la classe de la classe de la classe de la classe de la classe de la classe de la classe de la classe de la classe de la classe de la classe de la classe de la classe de la classe de la classe

**Audio Spectrogram Transformer, AST (2021-2024).**Partagez le log-mail (par exemple, 16×16 patches), ajoutez des emblèmes de position, fournissez un ViT.

> **音频频谱图 Transformer，AST（2021-2024）。**Pour les autres, il est nécessaire de faire une mise à jour de la carte de l'appareil.

**BEATs and WavLM-base (2024-2026).**Préentraînement autonome sur des millions d'heures. Téléchargez votre tâche avec 1 à 10% des données supervisées dont vous auriez besoin. En 2026, ce sera le point de départ par défaut pour l'audio non-speech. BEATs-iter3 bat AST de 1-2 mAP sur AudioSet en utilisant 1/4 du calcul.

> **BEATs 和 WavLM-base（2024-2026）。**En 2026 il s'agit du point de départ par défaut du non-linguisme.

**Whisper-encoder as a frozen backbone (2024).**Prenez l'encodeur de Whisper, laissez tomber le décodeur, attachez un classifiateur linéaire.

> **Whisper 编码器作为冻结骨干（2024）。**取 Whisper 的编码器,丢弃解码器,接一个线性分类器──在语言ID 和简单事件分类上接近SOTA,无需任何音频增强──"免费午餐"基线──

### Le déséquilibre des classes est le véritable défi

> ### Le déséquilibre est le vrai défi

ESC-50: 50 classes, 40 clips chacun  équilibré, facile. UrbanSound8K: 10 classes, déséquilibré 10:1. AudioSet: 632 classes avec une longue queue de 100,000:1.

> Les résultats de l'étude sont les suivants:

- Prise d'échantillons équilibrée pendant la formation (pas lors de l'évaluation).
  訓練時平衡采样 () 
- Mélange: interpolez linéairement deux clips (et leurs étiquettes) en augmentation.
  Mixup: 线性插值两段音频 (→ L'article suivant)
- SpecAugment: masquer le temps aléatoire et les bandes de fréquences.
  Spécification: couverture avec temps et fréquence.

### Évaluation

> ###  évaluer

- Exclusif en plusieurs classes (commandes de parole): précision de haut à haut, précision de haut à haut à haut à haut.
  Peut-être que les commandes de parole sont les plus élevées.
- Multiclass multi-label (AudioSet, UrbanSound-style): précision moyenne moyenne (mAP).
  Peut-être plusieurs types de son (AudioSet, UrbanSound): moyenne d'épreuve moyenne (MAP)
- En effet, les données de référence sont généralement définies comme étant les données de référence.
  严重不平衡: pour chaque classe de recrutement + pour l'ensemble de la classe F1

2026 numéros que vous devriez savoir:

> 2026 année que vous devriez savoir:

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

> **【中文解读】**Cette méthode "de zéro" peut aider à comprendre le principe derrière le cadre, en cas de problème, ne sera pas bloqué dans une boîte noire.

> **【拓展：语音 AI 的产品化】**La technologie du langage est confrontée à des défis particuliers dans la fabrication de produits: différents sons, bruits de fond, prises de vue, nombreux discours, etc. Les produits de Siri, Alexa, et de petite enfance ont été largement optimisés pour résoudre ces "problèmes de longue durée".

> **【拓展：多语言语音技术】**Les caractéristiques du langage mondial sont énormes: la voix de la langue (en chinois comme en chinois) est à un niveau élevé, les ressources linguistiques sont faibles et les données de formation manquent.

> **【拓展：语音隐私与安全】**Les données de la langue contiennent une grande quantité d'informations personnelles confidentielles (en anglais) et sont très fausses (en anglais).





## Construisez-le et mettez-le en œuvre.
```figure
mfcc-pipeline
```

## Faites-le

### Étape 1: Featurisez

```python
def featurize_mfcc(signal, sr, n_mfcc=13, n_mels=40, frame_len=400, hop=160):
    mag = stft_magnitude(signal, frame_len, hop)
    fb = mel_filterbank(n_mels, frame_len, sr)
    mels = apply_filterbank(mag, fb)
    log = log_transform(mels)
    return [dct_ii(frame, n_mfcc) for frame in log]
```

### Étape 2: résumé de longueur fixe

```python
def summarize(mfcc_frames):
    n = len(mfcc_frames[0])
    mean = [sum(f[i] for f in mfcc_frames) / len(mfcc_frames) for i in range(n)]
    var = [
        sum((f[i] - mean[i]) ** 2 for f in mfcc_frames) / len(mfcc_frames) for i in range(n)
    ]
    return mean + var
```

Simple mais fort: moyenne + variance à travers le temps donne une intégration fixe de 26 dimensions pour un MFCC à 13 côtes.

>  Simple mais efficace: la valeur moyenne + la différence de 13 nombres à l'axe temporel  MFCC a donné 26 dimensions fixes ⋅ en-métrage instantané ⋅ en fonctionnement ⋅ en ESC-50 jusqu'en 2017 encore capable de battre alors SOTA

### Étape 3: k-NN

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

### Étape 4: mise à niveau vers CNN sur les log-mels

Dans PyTorch:

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

Paramètres 3M. Trains en 10 minutes sur ESC-50 avec une seule RTX 4090.

> 300 000 paramètres. Dans le système ESC-50, l'utilisation d'une seule carte RTX 4090 est pratiquée pendant environ 10 minutes.

### Étape 5: les BEATs de 2026 par défaut  fine-tune

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

Pour les BEAT, utilisez `microsoft/BEATs-base`par le `beats`bibliothèque; l'API des transformateurs est de la même forme.

> Pour les battements, par`beats`库使用 `microsoft/BEATs-base`;les transformateurs API de la même forme:




> **【拓展：语音与情感计算】**Le langage n'est pas seulement un moyen de transmettre des informations, il est également un moyen de transmettre des signaux émotionnels riches.

## Utilisez-le avec le cadre de réalisation

La pile de 2026:

> 2026:

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

> **【中文解读】**Cette section se concentre sur la façon de déployer le modèle en tant que produit disponible. De l'original au système de production, il faut considérer plusieurs dimensions de l'optimisation des performances, du traitement des erreurs, du contrôle, etc.


Règle de décision: **start with a frozen backbone, not a fresh model**Une tête de BEATs à réglage fin vous donne 95% de SOTA en quelques heures, pas en quelques semaines.

> Règles de décision:**从冻结骨干开始，而不是从头训练模型**Les classes de BEATs peuvent atteindre 95% de SOTA en quelques heures, plutôt que quelques semaines.



## Envoyez-le . Produit .

- Je ne sais pas .`outputs/skill-classifier-designer.md`. Choisir l'architecture, les augmentations, la stratégie d'équilibre des classes et évaluer les mesures pour une tâche de classification audio donnée.

> 保存为 `outputs/skill-classifier-designer.md`◊ pour une série de tâches déterminées, sélectionner des structures, renforcer des stratégies, équilibrer des stratégies et évaluer des indicateurs.

## Les exercices

1. **Easy.**On court .`code/main.py`Il forme la base de base de la K-NN MFCC sur un ensemble de données synthétiques de 4 classes (tons purs à différents tons).
   **简单。**运行  référencement`code/main.py`Il est utilisé dans 4 catégories de données synthétiques (en anglais seulement)
2. **Medium.**Remplacez`summarize`Le regroupement de 4 moments bat-il le moyen + le ver sur le même ensemble de données synthétiques ?
   **中等。**Il va`summarize`替换为 [mean, var, skew, kurtosis]──四矩池化 est-il supérieur à la valeur moyenne+quadré différence sur le même ensemble de données de synthèse?
3. **Hard.**En utilisant `torchaudio`En plus de la précision de validation croisée, il est nécessaire d'ajouter un accroissement de la spécification (masque temporelle = 20, masque fréquence = 10) et de signaler le delta.
   **困难。**Utilisation `torchaudio`, dans le cadre de l'ESC-50 plier 1 上训练 2D CNN──rapport 5 折交叉验证准确率──添加 规范Augmentation(时间掩码 = 20,频率掩码 = 10)并报告差值──

> **【中文解读】**Dans le tableau des termes, la définition du terme "ce que les gens disent" et "ce qu'il signifie réellement" est différenciée entre le langage quotidien et la signification technique précise.


## Les termes clés

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

> **【中文解读】**延伸阅读 fournit des ressources de haute qualité pour l'apprentissage en profondeur. Ces articles et cours sont des références classiques dans ce domaine, adaptés aux lecteurs qui ont besoin d'une compréhension approfondie.


## Encore une lecture

- [Gong, Chung, Glass (2021). AST: Audio Spectrogram Transformer](https://arxiv.org/abs/2104.01778) l'architecture de l'enregistrement à partir de 20212024.
  Gong, Chung, Glass (2021). AST:音频频谱图 Transformer2021-2024 年的记录架构──
- [Chen et al. (2022, rev. 2024). BEATs: Audio Pre-Training with Acoustic Tokenizers](https://arxiv.org/abs/2212.09058) le défaut de 2024+.
  Chen 等 (2022, 修订 2024). BEATs:声学 tokenizer 的音频预训练2024+ 的默认选择──
- [Park et al. (2019). SpecAugment](https://arxiv.org/abs/1904.08779) l'augmentation de l'audio dominante.
  Park 等 (2019). SpecAugmentmainstream音频增强方法──
- [Piczak (2015). ESC-50 dataset](https://github.com/karolpiczak/ESC-50) 50 classes de référence qui vit sur.
  Piczak (2015). 50 types de base de données de l'ESC-50 en continu utilisation
- [Gemmeke et al. (2017). AudioSet](https://research.google.com/audioset/) Taxonomie YouTube de classe 632; toujours la norme en or.
  Gemmeke 等 (2017). AudioSet632 类 YouTube 分类体系; encore est un standard de qualité.

> **【中文解读】**延伸阅读 a fourni des ressources de haute qualité pour l'apprentissage en profondeur, y compris des articles, des cours et des outils.

