# Reconnaissance du langage (ASR)  CTC, RNN-T, Attention  语音识别  CTC、RNN-T avec mécanisme d'attention

> La reconnaissance de la parole est une classification audio à chaque étape, collée par un modèle de séquence qui connaît l'anglais et le silence. CTC, RNN-T et l'attention sont les trois façons de le faire. Choisissez une et comprenez pourquoi.

> **【中文解读】**L'identification du langage est effectuée à chaque étape du processus de séquence, en utilisant de nouveau le modèle de séquence (voir la loi du langage et du silence) pour les joindre à l'autre.

> **【拓展：ASR 的应用】**语音识别是语音助手(Siri、小爱同学) 、会议记录(飞书/钉钉实时字幕) 、视频字幕自动生成的核心──Whisper is the 2026 year's open source ASR 标杆──

**Type:** Build | **类型:** 构建
**Languages:** Python | **语言:** Python
**Prerequisites:** Phase 6 · 02 (Spectrograms & Mel), Phase 5 · 08 (CNNs & RNNs for Text), Phase 5 · 10 (Attention) | **前置知识:** 阶段 6 · 02（频谱图与 Mel），阶段 5 · 08（文本的 CNN 与 RNN），阶段 5 · 10（注意力机制）
**Time:** ~45 minutes | **预计用时:** ~45 分钟

## Le problème , l' introduction du problème

Vous avez un clip de 10 secondes à 16 kHz. Vous voulez une chaîne: "allumer les lumières de cuisine". Le défi est structurel: les cadres audio ne s'alignent pas un à un avec les caractères. Le mot "ok" peut prendre 200 ms ou 1200 ms. Le silence ponctue la prononciation. Certains phonèmes sont plus longs que d'autres. Le nombre de jetons de sortie n'est pas connu à l'avance.

> Vous avez un passage de 10 secondes 16 kHz de son. Vous voulez un string: "allumer les lumières de cuisine"[2]. Le défi est structural:

> **【中文解读】**La question posée dans ce chapitre est la suivante: comment comprendre et appliquer correctement cette technique dans la conception pratique. Comprendre le contexte de la question aide à saisir les principaux facteurs de décision concernant le type de technologie. Dans les systèmes d'IA réels, le type de technique erroné coûte souvent plus cher que le coût de la mise en œuvre de détails.

Trois formules résolvent ceci:

> Trois solutions pour résoudre ce problème:

1. **CTC (Connectionist Temporal Classification).**Émettez des probabilités de jetons par cadre, y compris un *blanc* spécial. Répéter et blanchir à la fois à décoder. Non autorégressif, rapide. Utilisé par wav2vec 2.0, MMS.
   **CTC（连接时序分类）。**逐发射代币 概率, incluant les spéciaux *blank*──解码时折叠重复和空白──非自归,快速──wav2vec 2.0、MMS 使用──
2. **RNN-T (Recurrent Neural Network Transducer).**Le réseau commun prédit le prochain jeton donné à un cadre d'encodeur et des jetons précédents.
   **RNN-T（递归神经网络转换器）。**联合网络根据编码器和之前的代币 预测下一个代币──可流式处理──Google 端侧 ASR、NVIDIA Parakeet 使用──
3. **Attention encoder-decoder.**L'encodeur comprime l'audio dans des états cachés, le décodeur serve à générer des jetons autoregressivement.
   **注意力编码器-解码器。**Le codeur sera réduit en un état caché, le codeur sera réduit en un état caché, le codeur sera réduit en un état caché.

En 2026, le SOTA WER sur LibriSpeech est de 1,4% (Parakeet-TDT-1.1B, NVIDIA) et de 1,58% (Whisper-Large-v3-turbo). Les différences sont minuscules; les différences de déploiement sont énormes.

> En 2026 année, le taux de SOTA de LibriSpeech test-clean est de 1,4% (parakeet-TDT-1.1B,NVIDIA) et de 1,58% (Whisper-Large-v3-turbo)

## Le concept de base.

> **【中文解读】**Le présent article présente les concepts et les bases théoriques de base. La connaissance de ces concepts est la prémisse de la réalisation de la réalisation de la réalisation, mais aussi le point de connaissance de l'interview et de la pratique de l'ingénierie.


![Three ASR formulations: CTC, RNN-T, attention-encoder-decoder](../assets/asr-formulations.svg)

**CTC intuition.**Laissez le codeur exister `T`répartitions au niveau du cadre sur `V+1`jetons (V caractères + blanc). Pour une chaîne cible `y`de longueur `U < T`, tout alignement de cadre qui s' effondre à `y`Les données de l'analyse de la valeur de l'alignement sont calculées.

> **CTC 直觉。**让编码器输出 `T`个级分布, chaque distribution est couverte `V+1`个标志(V 个字符 + blanc) ⋅对于长度为 `U < T`Le but de la série`y`, tout pliage après équivaut à `y`Les données de l'équipe de formation sont les données de formation de la formation de formation de formation professionnelle.

Les avantages: non autorégressif, diffusable, point de vue zéro. Défaut: * hypothèse d'indépendance conditionnelle *  chaque prédiction de cadre est indépendante des autres, il n'y a donc pas de modèle de langage interne. Fixer avec un LM externe via recherche de faisceau ou fusion superficielle.

> 优势:非自归、可流式处理、零前──缺点:* condition independencia性假设*每预测彼此独立, therefore no internal language模型──通过beam search 或浅融合的外部 LM 来修复──

**RNN-T intuition.**Ajout d' un * prédicteur * réseau qui intègre l' histoire des jetons et un * joiner * qui combine l' état prédicteur avec le cadre d' encodeur dans une distribution commune sur `V+1`(le `+1`est un nul / no-emission). Modèle explicitement la dépendance conditionnelle CTC ignoré. diffusable parce que chaque étape conditionne uniquement sur les cadres passés et les jetons passés.

> **RNN-T 直觉。**                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             `V+1`联合分布的 *joiner*(`+1`CTC 忽略的条件依赖──可流式处理,因为每步只依赖过去和过去的代币──

Avantages: streaming + LM interne. Défaut: la formation est plus complexe et manque de mémoire (3D retable de perte); les noyaux de perte RNN-T constituent une catégorie de bibliothèques entière.

> 优势:可流式 + 内部 LM。缺点: entraînement plus complexe、更耗内存(3D 损失格);RNN-T 损失核本身就是一个完整的库类──

**Attention encoder-decoder.**Le décodeur (6-32 couches de transformateur) sur les cadres log-mail. Le décodeur (6-32 couches de transformateur) assiste aux sorties d'encodeur pour générer des jetons autoregressivement. Aucune contrainte d'alignement  L'attention ne peut regarder n'importe où dans l'audio. Non diffusable à moins que vous restreignez l'attention (chunked Whisper-Streaming, 2024).

> **注意力编码器-解码器。**编码器(6-32 层变压器) 处理日志 ──解码器(6-32 层变压器) 通过交叉注意力自归归生成代币──无对齐约束注意力可以看向音频的任何位置──除非限制注意力(分块 微笑流,2024),否则不可流式处理──

Avantage: la plus haute qualité sur ASR hors ligne, facile à entraîner avec des outils standard seq2seq.

> 优势:离线 ASR 质量最高, us standard seq2seq 工具易训――缺点:自归延迟与输出长度成正比;不做工程优化无法流式处理――

### WER: le numéro unique

> ### WER: indicateur unique

**Word Error Rate**- Je suis là.`(S + D + I) / N`, où S = substitutions, D = suppressions, I = insertions, N = nombre de mots de référence. Correspond à la distance de modification de Levenshtein au niveau des mots. Plus bas est mieux. Un WER supérieur à 20% est généralement inutilisable; inférieur à 5% est la parité humaine pour le discours de lecture.

> **词错误率**- Je suis là.`(S + D + I) / N`, dont S = remplacement, D = suppression, I = insertion, N = nombre de mots de référence.

| Model | LibriSpeech test-clean | LibriSpeech test-other | Size |
|-------|------------------------|------------------------|------|
| Parakeet-TDT-1.1B | 1.40% | 2.78% | 1.1B params |
| Whisper-Large-v3-turbo | 1.58% | 3.03% | 809M |
| Canary-1B Flash | 1.48% | 2.87% | 1B |
| Seamless M4T v2 | 1.7% | 3.5% | 2.3B |

| 模型 | LibriSpeech test-clean | LibriSpeech test-other | 大小 |
|------|------------------------|------------------------|------|
| Parakeet-TDT-1.1B | 1.40% | 2.78% | 11 亿参数 |
| Whisper-Large-v3-turbo | 1.58% | 3.03% | 8.09 亿 |
| Canary-1B Flash | 1.48% | 2.87% | 10 亿 |
| Seamless M4T v2 | 1.7% | 3.5% | 23 亿 |

> **【中文解读】**Cette méthode "de zéro" peut aider à comprendre le principe derrière le cadre, en cas de problème, ne sera pas bloqué dans une boîte noire.


Tous ces systèmes sont basés sur un encodeur-décodeur ou RNN-T. Les systèmes CTC purs (wav2vec 2.0) sont situés autour de 1,82,1% sur le test-clean.

> Ces sont des codeurs-décodeurs ou RNN-T 架构── Pure CTC 系统(wav2vec 2.0) dans le test-clean en haut d'environ 1,82,1%──

> **【拓展：语音 AI 的产品化】**La technologie du langage est confrontée à des défis particuliers dans la fabrication de produits: différents sons, bruits de fond, prises de vue, nombreux discours, etc. Les produits de Siri, Alexa, et de petite enfance ont été largement optimisés pour résoudre ces "problèmes de longue durée".

> **【拓展：多语言语音技术】**Les caractéristiques du langage mondial sont énormes: la voix de la langue (en chinois comme en chinois) est à un niveau élevé, les ressources linguistiques sont faibles et les données de formation manquent.



## Construisez-le et mettez-le en œuvre.
```figure
ctc-collapse
```

## Faites-le

### Étape 1: décodeur avide de CTC

```python
def ctc_greedy(frame_logits, blank=0, vocab=None):
    # frame_logits: list of per-frame probability vectors
    preds = [max(range(len(p)), key=lambda i: p[i]) for p in frame_logits]
    out = []
    prev = -1
    for p in preds:
        if p != prev and p != blank:
            out.append(p)
        prev = p
    return "".join(vocab[i] for i in out) if vocab else out
```

Deux règles: répétition de l'effondrement consécutive, déposez des espaces vides.`a a _ _ a b b _ c`- Je suis là.`a a b c`- Je suis désolé .

> 两条规则: pliage连续重复, abandonner le vide.`a a _ _ a b b _ c`- Je suis là.`a a b c`Il y a une autre.

### Étape 2: CTC de recherche par faisceau

```python
def ctc_beam(frame_logits, beam=8, blank=0):
    import math
    beams = [([], 0.0)]  # (tokens, log_prob)
    for p in frame_logits:
        log_p = [math.log(max(pi, 1e-10)) for pi in p]
        candidates = []
        for seq, lp in beams:
            for t, lpt in enumerate(log_p):
                new = seq[:] if t == blank else (seq + [t] if not seq or seq[-1] != t else seq)
                candidates.append((new, lp + lpt))
        candidates.sort(key=lambda x: -x[1])
        beams = candidates[:beam]
    return beams[0][0]
```

La production utilise la recherche de faisceaux d'arbres préfixes avec fusion LM; c'est le squelette conceptuel.

> Le concept de l'environnement de production est de la recherche de faisceaux de bois.

### Étape 3: REM

```python
def wer(ref, hyp):
    r, h = ref.split(), hyp.split()
    dp = [[0] * (len(h) + 1) for _ in range(len(r) + 1)]
    for i in range(len(r) + 1):
        dp[i][0] = i
    for j in range(len(h) + 1):
        dp[0][j] = j
    for i in range(1, len(r) + 1):
        for j in range(1, len(h) + 1):
            cost = 0 if r[i - 1] == h[j - 1] else 1
            dp[i][j] = min(
                dp[i - 1][j] + 1,
                dp[i][j - 1] + 1,
                dp[i - 1][j - 1] + cost,
            )
    return dp[len(r)][len(h)] / max(1, len(r))
```

### Étape 4: inférence contre le murmure

```python
import whisper
model = whisper.load_model("large-v3-turbo")
result = model.transcribe("clip.wav")
print(result["text"])
```

Un liner pour le plus fort ASR général en 2026.

> La première ligne de code de l'ASR la plus puissante de l'année 2026: elle fonctionne à environ 20 fois la vitesse de fonctionnement de la GPU de 24 Go.

### Étape 5: streaming avec Parakeet ou wav2vec 2.0

```python
from transformers import pipeline
asr = pipeline("automatic-speech-recognition", model="nvidia/parakeet-tdt-1.1b")
for chunk in streaming_audio():
    print(asr(chunk, return_timestamps=True))
```

> **【中文解读】**Dans ce chapitre, nous allons montrer comment utiliser un cadre mature (comme PyTorch, HuggingFace, etc.) pour appliquer rapidement cette technique.


La diffusion en continu d'ASR nécessite une attention et un état de transport par codeur en morceaux; utilisez une bibliothèque qui la supporte (NeMo pour Parakeet, `transformers`pipeline avec `chunk_length_s`)

> L'ASR a besoin d'un système de codeur à l'aide de NeMo pour Parakeet.`transformers`pipeline 带 `chunk_length_s`)。




> **【拓展：语音与情感计算】**Le langage n'est pas seulement un moyen de transmettre des informations, il est également un moyen de transmettre des signaux émotionnels riches.

## Utilisez-le avec le cadre de réalisation

La pile de 2026:

> 2026:

| Situation | Pick |
|-----------|------|
| English, offline, max quality | Whisper-large-v3-turbo |
| Multilingual, robust | SeamlessM4T v2 |
| Streaming, low latency | Parakeet-TDT-1.1B or Riva |
| Edge, mobile, <500 ms latency | Whisper-Tiny quantized or Moonshine (2024) |
| Long-form | Whisper with VAD-based chunking (WhisperX) |
| Domain-specific (medical, legal) | Fine-tune wav2vec 2.0 + domain LM fusion |

| 场景 | 选择 |
|------|------|
| 英文、离线、最高质量 | Whisper-large-v3-turbo |
| 多语言、鲁棒 | SeamlessM4T v2 |
| 流式、低延迟 | Parakeet-TDT-1.1B 或 Riva |
| 边缘/移动、<500 ms 延迟 | 量化 Whisper-Tiny 或 Moonshine（2024） |
| 长音频 | Whisper + VAD 分块（WhisperX） |
| 特定领域（医疗、法律） | 微调 wav2vec 2.0 + 领域 LM 融合 |



## Des pièges qui vont encore arriver en 2026

> 2026 est toujours en train de tomber

- **No VAD.**Le silence provoque des hallucinations ("Merci de vous avoir regardé!").
  **没有 VAD。**Dans la suite, il est possible de voir le film en direct.
- **Character vs word vs subword WER.**Rapporte la réaction de réaction de niveau mot *après* normalisation (minuscule, ponctuation dépourvue).
  **字符 vs 词 vs 子词 WER。**報告归一化后 (小写、去标点) du mot "réponse" est un mot qui signifie "réponse".
- **Language ID drift.**L'ID automatique de Whisper dérote les clips bruyants vers le japonais ou le gallois; force `language="en"`Quand tu le sais.
  **语言识别漂移。**L'identification automatique de la langue par le sourire est une erreur de jugement en japonais ou en wels;`language="en"`Il y a une autre.
- **Long clips without chunking.**Whisper a une fenêtre de 30 secondes.`chunk_length_s=30, stride=5`Pour tout ce qui reste.
  **长音频不分块。**Sous-suceur Il y a une fenêtre de 30 secondes.`chunk_length_s=30, stride=5`Il y a une autre.

> **【中文解读】**Cette section se concentre sur la façon de déployer le modèle en tant que produit disponible. De l'original au système de production, il faut considérer plusieurs dimensions de l'optimisation des performances, du traitement des erreurs, du contrôle, etc.


## Envoyez-le . Produit .

- Je ne sais pas .`outputs/skill-asr-picker.md`- Choisir un modèle, décoder une stratégie, déchiffrer et fusionner des LM pour une cible de déploiement donnée.

> 保存为 `outputs/skill-asr-picker.md` Pour un déploiement déterminé, l'objectif est de choisir un modèle, de déchiffrer une stratégie, de partager des blocs et de mettre en œuvre un programme de fusion de LM.

## Les exercices

1. **Easy.**On court .`code/main.py`Il décode avidement une sortie CTC fabriquée à la main et calcula WER par rapport à une référence.
   **简单。**运行  référencement`code/main.py`Il est également utilisé pour la production de produits de base.
2. **Medium.**Appliquez correctement la recherche de faisceau de préfixe dans l'étape 2 (compte pour la règle de fusion en blanc).
   **中等。**Réfléchissez à la recherche de faisceaux de bois en blanc 合并规则) ⋅ en 10 个合成样本上与贪方法比较──
3. **Hard.**Utilisation `whisper-large-v3-turbo`sur[LibriSpeech test-clean](https://www.openslr.org/12)- Comparer les chiffres publiés avec les 100 premiers discours.
   **困难。**Dans le[LibriSpeech test-clean](https://www.openslr.org/12)上使用 `whisper-large-v3-turbo`◊ calculer ◊ 100 条语音的 WER──与发表的数据比较──

> **【中文解读】**Dans le tableau des termes, la définition du terme "ce que les gens disent" et "ce qu'il signifie réellement" est différenciée entre le langage quotidien et la signification technique précise.


## Les termes clés

| Term | What people say | What it actually means |
|------|-----------------|-----------------------|
| CTC | The blank-token loss | Marginal over all frame-to-token alignments; non-AR. |
| RNN-T | The streaming loss | CTC + next-token predictor; handles word-order. |
| Attention enc-dec | Whisper-style | Encoder + cross-attending decoder; best offline quality. |
| WER | The number you report | `(S+D+I)/N` at word level. |
| Blank | The emptiness | Special token in CTC signalling "no emission this frame". |
| LM fusion | External language model | Add weighted LM log-probs during beam search. |
| VAD | The silence gate | Voice activity detector; trims non-speech. |

| 术语 | 人们常说的 | 实际含义 |
|------|-----------|---------|
| CTC | blank token 损失 | 所有帧到 token 对齐的边际概率；非自回归。 |
| RNN-T | 流式损失 | CTC + 下一 token 预测器；处理词序。 |
| 注意力编解码 | Whisper 风格 | 编码器 + 交叉注意力解码器；最佳离线质量。 |
| WER | 你报告的数字 | 词级别的 `(S+D+I)/N`。 |
| Blank | 空白 | CTC 中表示"本帧不发射"的特殊 token。 |
| LM 融合 | 外部语言模型 | beam search 中加入加权的 LM 对数概率。 |
| VAD | 静音门 | 语音活动检测器；裁剪非语音部分。 |

> **【中文解读】**延伸阅读 fournit des ressources de haute qualité pour l'apprentissage en profondeur. Ces articles et cours sont des références classiques dans ce domaine, adaptés aux lecteurs qui ont besoin d'une compréhension approfondie.


## Encore une lecture

- [Graves et al. (2006). Connectionist Temporal Classification](https://www.cs.toronto.edu/~graves/icml_2006.pdf) le papier du CTC.
  Graves 等 (2006). 连接时序分类CTC 论文。
- [Graves (2012). Sequence Transduction with RNNs](https://arxiv.org/abs/1211.3711) le papier RNN-T.
  Graves (2012). Utiliser RNN  pour effectuer des séries de transformation RNN-T 论文。
- [Radford et al. / OpenAI (2022). Whisper: Robust Speech Recognition via Large-Scale Weak Supervision](https://arxiv.org/abs/2212.04356) le papier canonique de 2022; extension v3-turbo en 2024.
  Radford 等 / OpenAI (2022). Sous-mort: Masseille faible surveillance des rou棒语音识别2022 年经典论文;2024 年 v3-turbo 扩展。
- [NVIDIA NeMo — Parakeet-TDT card](https://huggingface.co/nvidia/parakeet-tdt-1.1b) Leader du tableau des priorités des RSA ouverts de 2026.
  NVIDIA NeMoParakeet-TDT 模型卡2026 年 Open ASR 排行榜领先者──
- [Hugging Face — Open ASR Leaderboard](https://huggingface.co/spaces/hf-audio/open_asr_leaderboard) référence en direct sur plus de 25 modèles.
  Coups de cœur  Open ASR 排行榜 25+ 模型的实时基准测试──

> **【中文解读】**延伸阅读 a fourni des ressources de haute qualité pour l'apprentissage en profondeur, y compris des articles, des cours et des outils.

