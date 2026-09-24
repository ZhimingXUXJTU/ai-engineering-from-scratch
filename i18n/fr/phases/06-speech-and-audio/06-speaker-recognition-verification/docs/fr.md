# Le Président Reconnaissance et vérification

> L'ASR demande "qu'ont-ils dit?" La reconnaissance du haut-parleur demande "qui l'a dit?" Les mathématiques sont les mêmes  embeddings plus cosine  mais chaque décision de production dépend d'un seul numéro EER.

> **【中文解读】**ASR 问"说了什么",说话人识别问"谁说的"―― mathématiques ressemblent à des dimensions plus similaires à des êtres, mais chaque décision de production dépend d'une EER (e.g. taux d'erreur) △EER 越低,系统越可靠――

> **【拓展：声纹识别应用】**L'empreinte vocale est utilisée comme une marque de référence pour la reconnaissance des caractéristiques biologiques.

**Type:** Build | **类型:** 构建
**Languages:** Python | **语言:** Python
**Prerequisites:** Phase 6 · 02 (Spectrograms & Mel), Phase 5 · 22 (Embedding Models) | **前置知识:** 阶段 6 · 02（频谱图与 Mel），阶段 5 · 22（嵌入模型）
**Time:** ~45 minutes | **预计用时:** ~45 分钟

## Le problème , l' introduction du problème

Un utilisateur dit un mot de passe. Vous voulez savoir: est-ce la personne qu'il prétend être (* vérification*, 1:1), ou est-ce la première personne dans votre banque d'inscription (* identification*, 1: N)?

> Utilisateur: Vous voulez savoir: est-ce que c'est la personne qu'ils prétendent être ?

> **【中文解读】**La question posée dans ce chapitre est la suivante: comment comprendre et appliquer correctement cette technique dans la conception pratique. Comprendre le contexte de la question aide à saisir les principaux facteurs de décision concernant le type de technologie. Dans les systèmes d'IA réels, le type de technique erroné coûte souvent plus cher que le coût de la mise en œuvre de détails.

Avant 2018: GMM-UBM + i-vecteurs. EER raisonnable mais fragile pour le changement de canal (phone contre ordinateur portable) et l'émotion. 20182022: x-vecteurs (réteau TDNN entraîné avec marge angulaire). 2022+: ECAPA-TDNN et WavLM-grandes emblèmes.

> 2018 前年:GMM-UBM + i-vecteurs。EER 合理但对信道偏移(电话 vs 笔记本) 和情绪敏感。2018-2022:x-vecteurs(用角度间隔训练的 TDNN 骨干)。2022+:ECAPA-TDNN 和 WavLM-large 嵌入──到2026年, ce domaine est dominé par trois modèles et un indicateur。

La métrique est **EER** Taux d'erreur égal. Définissez votre seuil de décision de sorte que le taux de faux acceptation = taux de faux rejet. Le crossover est EER. Utilisé dans chaque document, chaque tableau de classement, chaque appel d'achat.

> Cet indicateur est**EER**等错误率──设置决策值使假接受率 =假拒绝率──交叉点就是 EER──用于每篇论文、每排行榜、每采购评审──

## Le concept de base.

> **【中文解读】**Le présent article présente les concepts et les bases théoriques de base. La connaissance de ces concepts est la prémisse de la réalisation de la réalisation de la réalisation, mais aussi le point de connaissance de l'interview et de la pratique de l'ingénierie.


![Enrollment + verification pipeline with embedding + cosine + EER](../assets/speaker-verification.svg)

**The pipeline.**Enregistrement: enregistrer 530 secondes de l'enceinte cible; calculer une intégration en dimension fixe (192-d pour ECAPA-TDNN, 256-d pour WavLM-large).

> **流水线。**Registration: enregistrement objectif de la personne 5-30 secondes de voix; calcul fixé dimension emplacement(ECAPA-TDNN 为 192 维,WavLM-large 为 256 维) 

**ECAPA-TDNN (2020, still dominant 2026).**Accentué l'attention, la propagation et l'agrégation du canal - Réseau neuronal retardé dans le temps. Blocs de convection 1D avec excitation de compresser, pooling d'attention multi-têtes, suivis d'une couche linéaire à 192-d. Formé sur VoxCeleb 1+2 (2 700 haut-parleurs, 1,1M déclarations) avec perte de marge angulaire additive (AAM-softmax).

> **ECAPA-TDNN（2020，2026 年仍占主导）。**En soulignant la durée de la propagation et de la concentration du réseau neurologique.1.D. Le volume + l'excitation de compression + le nombre de points de concentration, la couche de contact de la ligne 192 dimensions.

**WavLM-SV (2022+).**Télécharger une mémoire de base SSL de taille WavLM pré-entrainée avec perte AAM.

> **WavLM-SV（2022+）。**Utilisation de la formation préliminaire avec AAM 损失微调 WavLM-large SSL 骨干──质量更高但更慢300+ MB vs 15 MB──

**x-vector (baseline).**La mise en commun des statistiques TDNN +. classique; toujours utile sur le bord du processeur.

> **x-vector（基线）。**TDNN + 统计池化──经典方案; encore utile sur les appareils de bord du CPU/

**AAM-softmax.**Softmax standard avec marge ajoutée `m`dans l'espace angulaire: `cos(θ + m)`Pour la classe correcte, la séparation angulaire entre les classes.`m=0.2`, l' échelle `s=30`- Je suis désolé .

> **AAM-softmax。**Dans un espace angulaire, ajouter un espace`m`                                                                                                                                                                                                                                                              `cos(θ + m)` Forces de classe à l'angle de séparation  valeur typique `m=0.2`, réduit`s=30`Il y a une autre.

### Score

> ### 评分 Leur nom

- **Cosine**Les résultats de l'enquête ont été évalués en fonction des résultats obtenus.
  **余弦**La similitude, calculée entre les inscriptions et les inscriptions à l'essai, est basée sur la valeur de la décision.
- **PLDA (Probabilistic LDA).**Embedding de projet dans un espace latent où le même haut-parleur vs un haut-parleur différent a un rapport de probabilité de forme fermée. Ajouté en haut du cosine pour une réduction de +1020% de la REE.
  **PLDA（概率 LDA）。**Il sera intégré dans le potentiel de projection, où les interlocuteurs ont un taux de fermeture de 20 à 20% de la valeur égale à la valeur égale.
- **Score normalization.** `S-norm`ou `AS-norm`Les résultats obtenus par les chercheurs sont essentiels pour une évaluation interdomaine.
  **分数归一化。** `S-norm`Ou `AS-norm`Les résultats de l'évaluation sont également disponibles dans les pays tiers.

### Numéros que vous devriez connaître (2026)

> 2026 ans que vous devriez savoir

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

### Diarrhée

> ### Il est un homme qui parle en français.

" Qui a parlé quand " dans un clip multi- haut-parleurs. Pipeline: VAD → segment → intégrer chaque segment → cluster (agglomératif ou spectrale) → limites lisses.`pyannote.audio`3.1, qui regroupe la segmentation des haut-parleurs + l'intégration + le regroupement derrière un appel.

> Pour les personnes qui ont des problèmes de santé, il est nécessaire de se concentrer sur la santé et la santé.`pyannote.audio`3.1,将说话人分割 + 嵌入 + 聚类打包为一个调用──2026 ans AMI 上 SOTA DER 约15%(à partir de 2022 ans 23% 下降)──

> **【拓展：语音 AI 的产品化】**La technologie du langage est confrontée à des défis particuliers dans la fabrication de produits: différents sons, bruits de fond, prises de vue, nombreux discours, etc. Les produits de Siri, Alexa, et de petite enfance ont été largement optimisés pour résoudre ces "problèmes de longue durée".

> **【拓展：多语言语音技术】**Les caractéristiques du langage mondial sont énormes: la voix de la langue (en chinois comme en chinois) est à un niveau élevé, les ressources linguistiques sont faibles et les données de formation manquent.



## Construisez-le et mettez-le en œuvre.

> **【中文解读】**Cette méthode "de zéro" peut aider à comprendre le principe derrière le cadre, en cas de problème, ne sera pas bloqué dans une boîte noire.

```figure
sp-eer-crossover
```

## Faites-le

### Étape 1: intégration de jouets à partir des statistiques de la CFPM

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

Pas de SOTA par un mile  pour l'enseignement seulement. `code/main.py`utilise cette méthode comme preuve de concept sur les données des haut-parleurs synthétiques.

> 离 SOTA 差得远仅用于教学──`code/main.py`Le terme "concept de l'homme" est utilisé pour désigner le concept de l'homme.

### Étape 2: similitude cosine + seuil

```python
def cosine(a, b):
    dot = sum(x * y for x, y in zip(a, b))
    na = math.sqrt(sum(x * x for x in a))
    nb = math.sqrt(sum(x * x for x in b))
    return dot / (na * nb) if na and nb else 0.0

def verify(enroll, test, threshold=0.75):
    return cosine(enroll, test) >= threshold
```

### Étape 3: EER à partir de paires de similitudes

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

Retour (eer, threshold_at_eer).

> 返回 (eer, threshold_at_eer) ⋅两者都要报告──

### Étape 4: production avec SpeechBrain

```python
from speechbrain.pretrained import EncoderClassifier

clf = EncoderClassifier.from_hparams(source="speechbrain/spkrec-ecapa-voxceleb")

# enroll: average the embeddings of 3-5 clean samples
enroll = torch.stack([clf.encode_batch(load(x)) for x in enrollment_clips]).mean(0)
# verify
score = clf.similarity(enroll, clf.encode_batch(load("test.wav"))).item()
verdict = score > 0.25   # ECAPA typical threshold; tune on your data
```

### Étape 5: Diary avec note de piane

```python
from pyannote.audio import Pipeline

pipe = Pipeline.from_pretrained("pyannote/speaker-diarization-3.1")
diarization = pipe("meeting.wav", num_speakers=None)
for turn, _, speaker in diarization.itertracks(yield_label=True):
    print(f"{turn.start:.1f}–{turn.end:.1f}  {speaker}")
```

> **【中文解读】**Dans ce chapitre, nous allons montrer comment utiliser un cadre mature (comme PyTorch, HuggingFace, etc.) pour appliquer rapidement cette technique.





> **【拓展：语音与情感计算】**Le langage n'est pas seulement un moyen de transmettre des informations, il est également un moyen de transmettre des signaux émotionnels riches.

## Utilisez-le avec le cadre de réalisation

La pile de 2026:

> 2026:

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



## Les pièges

> 常见陷

- **Channel mismatch.**Modèle formé sur VoxCeleb (vidéo web) ≠ audio d'appel téléphonique.
  **信道不匹配。**Le modèle de formation sur VoxCeleb ne correspond pas à celui de la téléphonie.
- **Short utterances.**L'EER se dégrade nettement en dessous de 3 secondes d'audio de test.
  **短语音。**测试音频低于3秒时 EER Urgent dégradation
- **Enrollment with noise.**Une inscription bruyante empoisonne l'ancre.
  **带噪注册。**Un échantillon d'enregistrement de la population est en état de toxicité.
- **Fixed threshold across conditions.**Toujours régler le seuil sur un ensemble de développement détenu depuis le domaine cible.
  **跨条件固定阈值。**始终在目标领域的留出开发集上调整值──
- **Cosine on non-normalized embeddings.**L2 normaliser d'abord; sinon la magnitude domine.
  **未归一化嵌入上的余弦。**Il est nécessaire de faire une première analyse de la valeur de l'élément.

> **【中文解读】**Cette section se concentre sur la façon de déployer le modèle en tant que produit disponible. De l'original au système de production, il faut considérer plusieurs dimensions de l'optimisation des performances, du traitement des erreurs, du contrôle, etc.


## Envoyez-le . Produit .

- Je ne sais pas .`outputs/skill-speaker-verifier.md`- Le modèle de sélection, le protocole d'inscription, le plan de réglage des seuils et les garanties contre la fraude.

> 保存为 `outputs/skill-speaker-verifier.md` choisir un modèle, un accord d'inscription, un programme de réforme de la valeur et des mesures de prévention de la fraude.

## Les exercices

> **【中文解读】**Dans le tableau des termes, la définition du terme "ce que les gens disent" et "ce qu'il signifie réellement" est différenciée entre le langage quotidien et la signification technique précise.


1. **Easy.**On court .`code/main.py`- Construit des " haut-parleurs " synthétiques (profiles de tonalité différents), inscrit, calcula EER sur une liste d'essai de 100 paires.
   **简单。**运行  référencement`code/main.py`◊ Construire un ensemble de personnes ([[]]), enregistrer, calculer l'EER à 100 pour la liste de tests.
2. **Medium.**Utilisez SpeechBrain ECAPA sur 30 déclarations VoxCeleb1 (5 haut-parleurs × 6 chacun).
   **中等。**Dans le même temps, le groupe de travail est également utilisé pour la communication.
3. **Hard.**Construire l' inscription complète → diary → vérifier le pipeline avec `pyannote.audio`- Évaluer le DER sur le set de développement AMI.
   **困难。**- Je veux le faire .`pyannote.audio`构建完整的注册 → 日志 → 验证流水线──在 AMI 开发集上评估 DER──

## Les termes clés

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

> **【中文解读】**延伸阅读 fournit des ressources de haute qualité pour l'apprentissage en profondeur. Ces articles et cours sont des références classiques dans ce domaine, adaptés aux lecteurs qui ont besoin d'une compréhension approfondie.


## Encore une lecture

- [Snyder et al. (2018). X-Vectors: Robust DNN Embeddings for Speaker Recognition](https://www.danielpovey.com/files/2018_icassp_xvectors.pdf) le papier classique à plomb profond.
  Snyder 等 (2018). X-Vectors:说话人识别的鲁棒 DNN 嵌入经典的深度嵌入论文──
- [Desplanques et al. (2020). ECAPA-TDNN](https://arxiv.org/abs/2005.07143) architecture dominante 20202026.
  Des plans et autres (2020). ECAPA-TDNN2020-2026 ans occupant la principale structure
- [Chen et al. (2022). WavLM: Large-Scale Self-Supervised Pre-Training for Full Stack Speech Processing](https://arxiv.org/abs/2110.13900) L'épine dorsale SSL pour SV et la diarisation.
  Chen 等 (2022). WavLM: traitement de la voix à grande échelle de l'auto-surveillance pré-entraînement SV 和日志的 SSL 骨干──
- [Bredin et al. (2023). pyannote.audio 3.1](https://github.com/pyannote/pyannote-audio) Diarilisation de la production + pile d'intégration.
  Bredin et autres (2023). pyannote.audio 3.1生产级日志 + 嵌入技术。
- [VoxCeleb leaderboard (updated 2026)](https://www.robots.ox.ac.uk/~vgg/data/voxceleb/) classement actuel des EER sur les différents modèles.
  VoxCeleb 排行榜(2026年更新) 各模型当前 EER 排名。

> **【中文解读】**延伸阅读 a fourni des ressources de haute qualité pour l'apprentissage en profondeur, y compris des articles, des cours et des outils.

