# Évaluation audio  WER, MOS, UTMOS, MMAU, FAD, et les classements ouverts 音频评估指标

> Vous ne pouvez pas envoyer ce que vous ne pouvez pas mesurer. Cette leçon nomme les mesures 2026 pour chaque tâche audio: ASR (WER, CER, RTFx), TTS (MOS, UTMOS, SECS, WER-on-ASR-round-trip), audio-langue (MMAU, LongAudioBench), musique (FAD, CLAP), et haut-parleur (EER).

> **【中文解读】**无法量就无法交付──本课列出 2026年所有音频任务的评估指标:ASR 用 WER(词错率) ✓ TTS 用 MOS(平均意见分) ✓ 音频语言模型用 MMAU、音乐用 FAD、说话人识别用 EER──还有对比排行榜──

> **【拓展：WER 是语音识别的黄金指标】**WER(Rate d'erreur de mot,词错率) = (替换+删除+插入) / 总词数──Whisper Grand v3 在英文上达到 ~5% WER,接近人类水平──中文用 CER(字错率)──

**Type:** Learn | **类型:** 学习
**Languages:** Python | **语言:** Python
**Prerequisites:** Phase 6 · 04, 06, 07, 09, 10; Phase 2 · 09 (Model Evaluation) | **前置知识:** 阶段 6 · 04、06、07、09、10；阶段 2 · 09（模型评估）
**Time:** ~60 minutes | **预计用时:** ~60 分钟

## Le problème , l' introduction du problème

Chaque tâche audio a plusieurs mesures, chacune mesurant un axe différent. En utilisant la mauvaise mesure, vous envoyez un modèle qui a l'air superbe sur votre tableau de bord et terrible en production.

> Chaque tâche audio a plusieurs indicateurs, chaque indicateur mesure différentes dimensions. L'utilisation erronée d'un indicateur est la façon dont un modèle est excellent sur le tableau de bord mais mal performé en production. Liste standard de 2026:

> **【中文解读】**La question posée dans ce chapitre est la suivante: comment comprendre et appliquer correctement cette technique dans la conception pratique. Comprendre le contexte de la question aide à saisir les principaux facteurs de décision concernant le type de technologie. Dans les systèmes d'IA réels, le type de technique erroné coûte souvent plus cher que le coût de la mise en œuvre de détails.


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

> **【中文解读】**Le présent article présente les concepts et les bases théoriques de base. La connaissance de ces concepts est la prémisse de la réalisation de la réalisation de la réalisation, mais aussi le point de connaissance de l'interview et de la pratique de l'ingénierie.


## Le concept de base.

![Audio evaluation matrix — metrics vs tasks vs 2026 leaderboards](../assets/eval-landscape.svg)

### Les mesures ASR

> Indicateur d'évaluation des RAS

**WER (Word Error Rate).** `(S + D + I) / N`- Les minuscules, la ponctuation, la normalisation des chiffres avant de marquer.`jiwer`ou de OpenAI `whisper_normalizer`. &lt; 5% = lecture du discours parité humaine.

> **WER（词错率）。** `(替换 + 删除 + 插入) / 总词数`◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊    ◊ ◊    ◊ ◊    ◊ ◊                                                                                                                                                                                                         `jiwer`Ou ouvrir des`whisper_normalizer`❖ inférieur à 5% = niveau de la population ❖

**CER (Character Error Rate).**La même formule, au niveau des caractères. Utilisé pour les langues de ton (mandarin, cantonais) où la segmentation des mots est ambiguë.

> **CER（字错率）。**La même formule, le langage et la langue sont utilisés pour la séquence de la langue.

**RTFx (inverse real-time factor).**Les secondes audio sont traitées par seconde de l'horloge murale.

> **RTFx（逆实时因子）。**Chaque seconde de traitement de son de seconde.

**First-token latency.**Le mur de l'horloge de l'entrée audio au premier jeton de transcription.

> **首 token 延迟。**Du signal de sortie au premier enregistrement du jeton.

### Les mesures TTS

> TTS évaluation indice

**MOS (Mean Opinion Score).**1 à 5 pour les humains, standard d'or mais lent, plus de 20 auditeurs par échantillon, plus de 100 échantillons par modèle.

> **MOS（平均意见分）。**1-5 分人工评分──黄金标准但速度慢──每样本收集20+听者,每模型100+样本──

**UTMOS (2022-2026).**Prédicteur de MOS appris. Corrélate avec ~ 0,9 avec MOS humain sur des critères de référence standard. F5-TTS: UTMOS 3,95; vérité de base: 4,08.

> **UTMOS（2022-2026）。**Le modèle de MOS est un modèle de MOS.

**SECS (Speaker Encoder Cosine Similarity).**Pour le clonage vocal. ECAPA intégrant cosine entre référence et sortie clonée. &gt; 0,75 = clone reconnaissable.

> **SECS（说话人编码器余弦相似度）。**Utilisation de l'ECAPA entre le langage et le langage.

**WER-on-ASR-round-trip.**Exécutez Whisper sur la sortie TTS, calculer WER contre le texte d'entrée. Capture des régressions d'intelligibilité. 2026 SOTA: &lt; 2% CER.

> **WER-on-ASR-round-trip（ASR 回环 WER）。**Pour le TTS 输出运行 Whisper, calcul relative à WER du texte de l'entrée.

**TTFA (time-to-first-audio).**La latence de l'horloge murale Kokoro-82M: ~100 ms; F5-TTS: ~1 seconde.

> **TTFA（首个音频时间）。**实际延迟──Kokoro-82M: environ 100 ms; F5-TTS: environ 1 seconde──

### Clonage de la voix spécifique

> 语音克隆专用标志

**SECS + MOS + CER**Le clonage qui a un SECS élevé mais un MOS bas signifie timbre-bon mais-non-naturel; le contraire signifie voix naturelle mais mauvais haut-parleur.

> **SECS + MOS + CER**作为三重指标──克隆分高SECS但低MOS signifie sonore correct mais pas naturel;反之则 signifie son naturel mais parler人不对──

### Vérification des haut-parleurs

> Il y a aussi le nombre de personnes qui ont été testées.

**EER (Equal Error Rate).**Le seuil où le taux de faux acceptation est égal au taux de faux rejet.

> **EER（等错误率）。**Le taux d'erreur d'acceptation est égal à la valeur du taux d'erreur de rejet.

**minDCF (min Detection Cost).**Coût pondéré à un point d'exploitation choisi (souvent FAR = 0,01).

> **minDCF（最小检测代价）。**Dans le cadre de la réforme des prix de production, les prix de production sont généralement plus élevés que dans le secteur de la production.

### Diarrhée

> Il y a une autre personne qui a été victime de violences sexuelles.

**DER (Diarization Error Rate).** `(FA + Miss + Confusion) / total_speaker_time`. Discours manqué + discours d'alarme fausse + confusion des haut-parleurs, chacun en fraction. Rencontre AMI: DER ~10-20% est réaliste. note 3.1 + précision-2 commercial: &lt;10% DER sur audio bien enregistré.

> **DER（说话人日志错误率）。** `(虚警 + 漏检 + 混淆) / 总说话时间`◊漏检语音 + 虚警语音 + 说话人混,各占比例──AMI 会议:DER 约 10-20% 是现实水平──piannote 3.1 + Precision-2 商业版:在良好录音上 DER 低于10%──

**JER (Jaccard Error Rate).**Alternative à la DER, robuste à la partialité de segment court.

> **JER（Jaccard 错误率）。**Le DER est un programme de démarche de démarche de démarche de démarche de démarche de démarche de démarche de démarche de démarche de démarche de démarche de démarche de démarche de démarche de démarche de démarche de démarche de démarche de démarche de démarche de démarche de démarche de démarche de démarche de démarche de démarche de démarche de démarche de démarche de démarche de démarche de démarche de démarche de démarche de démarche de démarche de démarche de démarche de démarche de démarche de démarche de démarche de démarche de démarche de démarche de démarche de démarche de démarche de démarche de démarche de démarche de démarche de démarche de démarche de démarche de démarche de démarche de démarche de démarche de démarche de démarche de démarche de démarche de démarche de démarche de démarche de démarche de démarche de démarche de démarche de démarche de démarche de démarche de démarche.

### Classification audio

> 音频分类标签

- Le produit est à l' étiquette: **mAP (mean Average Precision)**Pour les classes BEAT-iter3, le MAP est de 0,548 mAP.

> Les étoiles**mAP（平均精度均值）**, couvre toutes les catégories。AudioSet:BEATs-iter3 为 0.548 mAP。

Exclusifs pour plusieurs classes: **top-1, top-5 accuracy**- Commande de parole v2: 99,0% top-1 (Audio-MAE).

> Les différents types de références:**top-1、top-5 准确率**❖ Commandes de parole v2:99.0% top-1

- Il est déséquilibré .**macro F1**+ **per-class recall**. Rapport par classe  la précision globale cache les classes qui échouent.

> données déséquilibrées:**macro F1**+ **每类召回率** Le rapport de catégorie  taux de précision global couvrira les catégories de défaillance

### Génération de musique

> 音乐生成指标

**FAD (Fréchet Audio Distance).**Distance entre les distributions intégrées VGGish d'audio réel et généré.

> **FAD（Fréchet 音频距离）。**La différence entre la fréquence de production et la fréquence de production est de 4,5 à 4,0 à 4,0 à 5,0 à 5,0 à 5,0 à 5,0 à 5,0 à 5,0 à 5,0 à 5,0 à 5,0 à 5,0 à 5,0 à 5,0 à 5,0 à 5,0 à 5,0 à 5,0 à 5,0 à 5,0 à 5,0 à 5,0 à 5,0 à 5,0 à 5,0 à 5,0 à 5,0 à 6,0 à 7,0 à 7,0 à 7,0 à 7,0 à 7,0 à 7,0 à 7,0 à 7,0 à 7,0 à 7,0 à 7,0 à 7,0 à 7,0 à 7,0 à 7,0 à 7,0 à 7,0 à 7,0 à 7,0 à 7,0 à 7,0 à 7,0 à 7,0 à 7,0 à 7,0 à 7,0 à 7,0 à 7,0 à 7,0 à 7,0 à 7,0 à 7,0 à 7,0 à 7,0 à 7,0 à 7,0 à 7,0 à 7,0 à 7,0 à 7,0 à 7,0 à 7,0 à 7,0 à 7,0 à 7,0 à 7,0 à 7,0 à 7,0 à 7,0 à 7,0 à 7,0 à 7,0 à 7,0 à 7,0 à 7,0 à 7,0 à 7,0 à 7,0 à 10 à 10 à 10 à 10 à 10 à 10

**CLAP Score.**Score d'alignement texte-audio en utilisant des emblèmes CLAP. &gt; 0,3 = alignement raisonnable.

> **CLAP 分数。**Utilisez CLAP 嵌入的文本音频对齐分数──大于0.3 = 合理对齐──

**Listening panel MOS.**Le dernier mot pour la musique de consommation.

> **听音评审团 MOS。**Le niveau d'évaluation de la musique est encore le plus élevé.

### Indices de référence pour le langage audio

> 音频语言基准测试

**MMAU (Massive Multi-Audio Understanding).**10 000 paires de QA audio.

> **MMAU（大规模多音频理解）。**10 000 voix pour le QA.

**MMAU-Pro.**1800 objets durs, quatre catégories: parole / son / musique / multi-audio. Chance aléatoire 25% sur quatre voies. Gémeaux 2.5 Pro globalement ~ 60%; multi-audio ~ 22% sur tous les modèles.

> **MMAU-Pro。**1800 个难题,四个类别:语音/声音/音乐/多音频──4 选 1 随机猜测 25%──Gemini 2.5 Pro 整体约60%;所有模型在多音频上约22%──

**LongAudioBench.**Des clips de plusieurs minutes avec des requêtes sémantiques.

> **LongAudioBench。**Peut-être une vidéo de la série "Flamingo"

**AudioCaps / Clotho.**Les indicateurs de référence sont sous-titrés: SPICE, CIDER, FENSE.

> **AudioCaps / Clotho。**音频描述基准测试──SPICE、CIDER、FENSE 指标──

### Diffusion de discours en direct

> 流式语音到语音指标

**Latency P50 / P95 / P99.**Montres murales de la fin de l'interface utilisateur à la première réponse audible.

> **延迟 P50 / P95 / P99。**De l'utilisateur de la voix fin à la première réponse à l'écoute.

**WER / MOS**sur la sortie.

>                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                              **WER / MOS**Il y a une autre.

**Barge-in responsiveness.**Temps de l'interruption de l'utilisateur à l'assistant muet.

> **打断响应时间。**Du temps de l'utilisateur à l'aide du silence.

### Les classements de 2026

| Leaderboard | Tracks | URL |
|------------|--------|-----|
| Open ASR Leaderboard (HF) / 开源 ASR 排行榜（HF） | English + multilingual + long-form / 英语 + 多语言 + 长音频 | `huggingface.co/spaces/hf-audio/open_asr_leaderboard` |
| TTS Arena (HF) / TTS 竞技场（HF） | English TTS / 英语 TTS | `huggingface.co/spaces/TTS-AGI/TTS-Arena` |
| Artificial Analysis Speech / Artificial Analysis 语音 | TTS + STT, ELO from paired votes / TTS + STT，配对投票 ELO | `artificialanalysis.ai/speech` |
| MMAU-Pro / MMAU-Pro | LALM reasoning / LALM 推理 | `mmaubenchmark.github.io` |
| SpeakerBench / VoxSRC / 说话人基准 / VoxSRC | Speaker recognition / 说话人识别 | `voxsrc.github.io` |
| MMAU music subset / MMAU 音乐子集 | Music LALM / 音乐 LALM | （在 MMAU 内） |
| HEAR benchmark / HEAR 基准 | Self-supervised audio / 自监督音频 | `hearbenchmark.com` |

> **【中文解读】**Cette méthode "de zéro" peut aider à comprendre le principe derrière le cadre, en cas de problème, ne sera pas bloqué dans une boîte noire.

> **【拓展：语音 AI 的产品化】**La technologie du langage est confrontée à des défis particuliers dans la fabrication de produits: différents sons, bruits de fond, prises de vue, nombreux discours, etc. Les produits de Siri, Alexa, et de petite enfance ont été largement optimisés pour résoudre ces "problèmes de longue durée".

> **【拓展：多语言语音技术】**Les caractéristiques du langage mondial sont énormes: la voix de la langue (en chinois comme en chinois) est à un niveau élevé, les ressources linguistiques sont faibles et les données de formation manquent.




## Construisez-le et mettez-le en œuvre.
```figure
sp-wer-align
```

## Faites-le

### Étape 1: REM avec normalisation

> 步骤 1: Avec la répartition des données standardisée

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

### Étape 2: REM de retour et retour de TTS

> 步骤 2: TTS Retour à l'échelle

```python
def ttr_wer(tts_model, asr_model, texts):
    errors = []
    for txt in texts:
        audio = tts_model.synthesize(txt)
        recog = asr_model.transcribe(audio)
        errors.append(wer(truth=txt, hypothesis=recog))
    return sum(errors) / len(errors)
```

### Étape 3: SECS pour le clonage vocale

> 步骤 3: Séquence de la langue du pays

```python
from speechbrain.inference.speaker import EncoderClassifier
sv = EncoderClassifier.from_hparams("speechbrain/spkrec-ecapa-voxceleb")

emb_ref = sv.encode_batch(load_wav("reference.wav"))
emb_clone = sv.encode_batch(load_wav("cloned.wav"))
secs = torch.nn.functional.cosine_similarity(emb_ref, emb_clone, dim=-1).item()
```

### Étape 4: FAD pour la génération de musique

> 步骤 4: musique générée de FAD

```python
from frechet_audio_distance import FrechetAudioDistance
fad = FrechetAudioDistance()
score = fad.get_fad_score("generated_folder/", "reference_folder/")
```

### Étape 5: RÉE pour la vérification des haut-parleurs (même code que leçon 6)

> 步骤 5: EER du programme de certification (code identique à celui du cours 6)

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

> **【中文解读】**Dans ce chapitre, nous allons montrer comment utiliser un cadre mature (comme PyTorch, HuggingFace, etc.) pour appliquer rapidement cette technique.





> **【拓展：语音与情感计算】**Le langage n'est pas seulement un moyen de transmettre des informations, il est également un moyen de transmettre des signaux émotionnels riches.

## Utilisez-le avec le cadre de réalisation

Parler chaque déploiement avec un harnais d'évaluation fixe qui fonctionne sur chaque mise à jour de modèle.

> Chaque déploiement est équipé d'un outil d'évaluation fixe, fonctionnant à chaque mise à jour du modèle.

1. **Normalize before scoring.**La minuscule, la bande de ponctuation, le nombre, rapportez la règle de normalisation.
   Le mot grec traduit par " le mot grec "**评分前标准化。**转小写、去标点、数字展开―― rapport de la normalisation
2. **Report distributions, not averages.**P50/P95/P99 pour la latence. Rappel par classe pour la classification. Par catégorie pour MMAU.
   Le mot grec traduit par " le mot grec "**报告分布而非均值。**延迟用P50/P95/P99──分类用每类召回率──MMAU用每类──
3. **Run one canonical public benchmark.**Même si vos données de production diffèrent, les rapports sur Open ASR / TTS Arena / MMAU permettent aux critiques de comparer les pommes aux pommes.
   Le mot grec traduit par " le mot grec "**运行一个权威公共基准。**Même si vos données de production sont différentes, le rapport de l'Open ASR / TTS Arena / MMAU peut permettre aux évaluateurs de faire une comparaison équitable.



## Les pièges

> 常见陷

- **UTMOS extrapolation.**Formé à la parole propre au style VCTK; score faible en audio bruyant / cloné / émotionnel.
  Le mot grec traduit par " le mot grec "**UTMOS 外推问题。**En ce qui concerne la formation de la langue, la formation de la langue est une formation de la langue.
- **MOS panel bias.**20 employés d'Amazon Mechanical Turk ≠ 20 utilisateurs cibles.
  Le mot grec traduit par " le mot grec "**MOS 评审团偏差。**20 Amazon Mechanical Turk 工作者不等于 20 目标用户──如果风险高,花钱请领域专家评审团──
- **FAD depends on reference set.**Comparer avec la même répartition de référence entre les modèles.
  Le mot grec traduit par " le mot grec "**FAD 依赖参考集。**跨模型比较时使用相同的参考分布──
- **Aggregate WER.**Un REM global de 5% peut cacher 30% du REM sur le discours accentué.
  Le mot grec traduit par " le mot grec "**汇总 WER。**Le taux de réaction des femmes dans les pays de l'UE est de 5%, ce qui représente 30% de la réaction des femmes dans les pays de l'UE.
- **Public benchmark saturation.**La plupart des modèles frontaliers sont proches du plafond sur des critères de référence standard.
  Le mot grec traduit par " le mot grec "**公共基准饱和。**La plupart des modèles avant-gardistes sur le standard basé sont déjà proches du plancher de travail.

> **【中文解读】**Cette section se concentre sur la façon de déployer le modèle en tant que produit disponible. De l'original au système de production, il faut considérer plusieurs dimensions de l'optimisation des performances, du traitement des erreurs, du contrôle, etc.


## Envoyez-le . Produit .

- Je ne sais pas .`outputs/skill-audio-evaluator.md`Choisissez des métriques, des critères de référence et le format de rapport pour toute version de modèle audio.

> 保存为 `outputs/skill-audio-evaluator.md`◊ Pour tout modèle de son, éditer des indicateurs de sélection, des bases de données et des formats de rapport.

## Les exercices

1. **Easy.**On court .`code/main.py`. Comptez le WER / CER / EER / SECS / FAD-ish / MMAU-ish sur les entrées de jouets.
   Le mot grec traduit par " le mot grec "**简单。**运行  référencement`code/main.py` dans le jeu de l'équipe de calcul WER / CER / EER / SECS / 类 FAD / 类 MMAU
2. **Medium.**Construisez un harnais WER aller-retour TTS. Exécutez votre sortie Kokoro ou F5-TTS via Whisper. Computez WER sur 50 demandes.
   Le mot grec traduit par " le mot grec "**中等。**Construire TTS 回环 WER 评估工具──用 Whisper 处理你的Kokoro 或 F5-TTS 输出──在 50 个提示上计算 WER──标记 WER 大于10% 的提示──
3. **Hard.**Résumez votre choix de LALM de leçon 10 sur le discours MMAU-Pro + plusieurs sous-ensembles audio (50 éléments chacun).
   Le mot grec traduit par " le mot grec "**困难。**Dans le MMAU-Pro's语音 + 多音频子集上 (en anglais) chaque 50 épisodes, évaluer votre 10ème choix de cours LALM.

> **【中文解读】**Dans le tableau des termes, la définition du terme "ce que les gens disent" et "ce qu'il signifie réellement" est différenciée entre le langage quotidien et la signification technique précise.


## Les termes clés

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

> **【中文解读】**延伸阅读 fournit des ressources de haute qualité pour l'apprentissage en profondeur. Ces articles et cours sont des références classiques dans ce domaine, adaptés aux lecteurs qui ont besoin d'une compréhension approfondie.


## Encore une lecture

- [jiwer](https://github.com/jitsi/jiwer) Bibliothèque WER/CER avec des utilitaires de normalisation.
  Les outils de normalisation des ressources humaines
- [UTMOS (Saeki et al. 2022)](https://arxiv.org/abs/2204.02152) apprend le prédicteur de MOS.
  UTMOS(Saeki 等 2022) 学习型 MOS 预测器。
- [Fréchet Audio Distance (Kilgour et al. 2019)](https://arxiv.org/abs/1812.08466) la norme de la génération musicale.
  Distance audio de Fréchet ((Kilgour 等 2019) 音乐生成的标准指标──
- [Open ASR Leaderboard](https://huggingface.co/spaces/hf-audio/open_asr_leaderboard) 2026 classement en direct.
  Résultats de la rédaction de la liste des rédacteurs
- [TTS Arena](https://huggingface.co/spaces/TTS-AGI/TTS-Arena) Le classement des TTS par vote humain.
  TTS Arena Les électeurs humains de TTS 排行榜。
- [MMAU-Pro benchmark](https://mmaubenchmark.github.io/) Tableau de classement de raisonnement LALM.
  MMAU-Pro 基准LALM 推理排行榜
- [HEAR benchmark](https://hearbenchmark.com/) les références SSL audio.
  Écoute 基准音频 SSL 评估基准──

> **【中文解读】**延伸阅读 a fourni des ressources de haute qualité pour l'apprentissage en profondeur, y compris des articles, des cours et des outils.

