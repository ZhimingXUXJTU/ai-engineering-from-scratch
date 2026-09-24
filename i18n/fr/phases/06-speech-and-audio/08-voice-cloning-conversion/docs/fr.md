# Clonage de voix et conversion de voix

> La clonage vocale lit votre texte dans la voix d'autrui. La conversion vocale réécrit votre voix dans celle d'autrui tout en préservant ce que vous avez dit. Les deux dépendent de la même décomposition: une identité séparée de l'orateur du contenu.

> **【中文解读】**语音克隆 Utilisez la voix d'un autre pour lire vos mots;语音转换把你的声音变成别人的但保留内容── les deux sont au cœur d'une même décomposition:将说话人身份与内容分离──

> **【拓展：语音克隆的伦理与法律】**Les problèmes éthiques et juridiques liés à la fraude et à la fraude de la voix ont été largement évoqués.

**Type:** Build | **类型:** 构建
**Languages:** Python | **语言:** Python
**Prerequisites:** Phase 6 · 06 (Speaker Recognition), Phase 6 · 07 (TTS) | **前置知识:** 阶段 6 · 06（说话人识别），阶段 6 · 07（TTS）
**Time:** ~75 minutes | **预计用时:** ~75 分钟

## Le problème , l' introduction du problème

En 2026, un clip audio de 5 secondes suffit pour produire un clone de haute qualité de la voix de n'importe qui avec un GPU de consommation. ElevenLabs, F5-TTS, OpenVoice v2, VoiceBox envoient tous un clonage à tir zéro ou à quelques tirages. La technologie est une bénédiction (accessibilité TTS, doublage, voix d'assistance) et une arme (appels frauduleux, faux profonds politiques, vol d'IP).

> En 2026 année, un épisode de 5 secondes de son est disponible pour le monde entier avec des GPU de haute qualité. ElevenLabs, F5-TTS, OpenVoice v2, VoiceBox fournissent des échantillons ou des échantillons de clones. Cette technologie est aussi une arme.

> **【中文解读】**La question posée dans ce chapitre est la suivante: comment comprendre et appliquer correctement cette technique dans la conception pratique. Comprendre le contexte de la question aide à saisir les principaux facteurs de décision concernant le type de technologie. Dans les systèmes d'IA réels, le type de technique erroné coûte souvent plus cher que le coût de la mise en œuvre de détails.

Deux tâches étroitement liées:

> Deux missions étroitement liées:

- **Voice cloning (TTS-side):**texte + voix de référence de 5 secondes → audio dans cette voix.
  **声音克隆（TTS 侧）：**文本 + 5 秒参考音 → The sound of the audio
- **Voice conversion (speech-side):**audio source (personne A disant X) + voix de référence de personne B → audio de B disant X.
  **语音转换（语音侧）：**源音频(说话人 A 说 X) + 说话人 B 的参考声音 → B 说 X 的音频。

Les deux facteurs d'une forme d'onde en (contenu, haut-parleur, prosodie) et recombiner le contenu d'une source avec le haut-parleur d'une autre.

> 两者都将波形分解为(内容、说话人、律) et se regrouper de la même source de contenu à la même source de la personne qui parle.

La contrainte clé que vous soumettez maintenant en 2026:**watermarking and consent gates are legally required in the EU (AI Act, enforceable August 2026) and in California (AB 2905, effective 2025)**Votre pipeline doit émettre une marque d'eau inaudible et refuser des clones non consensuels.

> Les principales difficultés que vous rencontrez en 2026:**水印和同意门在 EU（AI 法案，2026 年 8 月生效）和加利福尼亚州（AB 2905，2025 年生效）是法律要求的** Votre ligne d'eau doit émettre des empreintes inaudibles et refuser des clones non autorisées

## Le concept de base.

> **【中文解读】**Le présent article présente les concepts et les bases théoriques de base. La connaissance de ces concepts est la prémisse de la réalisation de la réalisation de la réalisation, mais aussi le point de connaissance de l'interview et de la pratique de l'ingénierie.


![Voice cloning vs conversion: factorize, swap speaker, recombine](../assets/voice-cloning.svg)

**Zero-shot cloning.**Passez un clip de 5 secondes à un modèle qui a été formé sur des milliers de haut-parleurs. Le codeur haut-parleur cartographiera le clip à un haut-parleur intégré; le décodeur TTS conditionne cette intégration plus texte.

> **零样本克隆。**Le programme de télévision en ligne est basé sur le modèle de télévision en ligne.

Utilisé par: F5-TTS (2024), YourTTS (2022), XTTS v2 (2024), OpenVoice v2 (2024).

> Il est également possible de faire une demande de règlement de la situation en cas de non-respect des droits de l'homme.

**Few-shot fine-tuning.**Enregistrer 5 à 30 minutes de la voix cible. LoRA-fin-tune un modèle de base pendant une heure. La qualité passe de "okay" à "indistinguible". Coqui et ElevenLabs soutiennent tous deux ce modèle; la communauté l'utilise avec F5-TTS.

> **少样本微调。**L'équipe de formation de la société de formation de la formation de la formation de la formation de la formation de la formation de la formation de la formation de la formation de la formation de la formation de la formation de la formation de la formation de la formation de la formation de la formation de la formation de la formation de la formation de la formation de la formation de la formation de la formation de la formation de la formation de la formation de la formation de la formation de la formation de la formation de la formation de la formation de la formation de la formation de la formation de la formation de la formation de la formation de la formation de la formation de la formation de la formation de la formation de la formation de la formation de la formation de la formation de la formation de la formation de la formation de la formation de la formation de la formation de la formation de la formation de la formation de la formation de la formation de la formation de la formation de la formation de la formation de la formation de la formation de la formation de la formation de la formation de la formation de la formation de la formation de la formation de la formation de la formation de la formation de la formation de la formation de la formation de la formation de la formation de la formation de la formation de la formation de la formation de la formation de la formation de la formation de la formation de la formation de la formation de la formation de la formation de la formation de la formation de la formation de la formation de la formation de la formation de la formation de la formation de la formation de la formation de la formation de la formation de la formation de la formation de la formation de la formation de la formation de la formation de la formation de la formation de la formation de la formation de la formation de la formation de la formation de la formation de la formation de la formation de la formation de la formation de la formation de la formation de la formation de la formation de la formation de la formation de la formation de la formation de la formation de la formation de la formation de la formation de la formation de la formation de la formation de la formation de la formation de la formation de la formation de la formation de la formation de la formation de la formation de la formation de la formation de la formation de la formation de la formation de la formation de la formation de la formation de la formation de la formation de la formation de la formation de la formation de la formation de la formation de la formation de la formation de la formation de la formation de la formation de la formation de la formation de

**Voice conversion (VC).**Deux familles:

> **语音转换（VC）。**两个家族:

- **Recognition-synthesis.**Exécutez un modèle ASR pour extraire la représentation du contenu (par exemple, des postérieurs phonémiques doux, PPG), puis la résynthétisez avec l'intégration de haut-parleurs cibles. Robuste pour le langage et l'accent. Utilisé par KNN-VC (2023), Diff-HierVC (2023).
  **识别-合成。**运行类 ASR 模型提取内容表示 (如软音素后验、PPG), puis utiliser le but de la langue et du langage pour la recréer.
- **Disentanglement.**Exercer un autoencodeur qui sépare le contenu, l'enceinte et la prosodie dans un espace latent à la boucle de fer. Swap le haut-parleur intégrant à l'inférence. Moins de qualité mais plus rapide. Utilisé par AutoVC (2019), VITS-VC variantes.
  **解耦。**訓練自编码器在瓶处的潜在空间中分离内容、说话人和律──推理时交换说话人嵌入──质量较低但更快──AutoVC(2019)、VITS-VC 变体使用──

**Neural codec-based cloning (2024+).**VALL-E, VALL-E 2, NaturalSpeech 3, VoiceBox  traiter l'audio comme des jetons discrets de SoundStream / EnCodec, entraîner un grand modèle autorégressif ou de correspondance de flux sur les jetons codec.

> **基于神经编解码器的克隆（2024+）。**VALL-E、VALL-E 2、NaturalSpeech 3、VoiceBox将音频视为 SoundStream/EnCodec's离散代币, 在编解码代币上训练大型自归归或流匹配模型──短提示上质量可与ElevenLabs相当──

### Le morceau d'éthique, pas un boulon

> ### 伦理问题, est pas option

**Watermarking.**PerTh (Perth) et SilentCipher (2024) incorporent un ID de ~16-32 bits imperceptiblement dans l'audio. Survient à la re-encodage, au streaming et aux éditions courantes.

> **水印。**PerTh 和 SilentCipher(2024) est inséré dans le son en 16 à 32 places.

**Consent gates.**Il faut associer chaque sortie clonée à un enregistrement de consentement vérifiable. "Je, Rohit, le 2026-04-22, autorise cette voix à des fins X".

> **同意门。**Chaque sortie de clone doit être accompagnée d'un enregistrement de consentement vérifiable.

**Detection.**AASIST, RawNet2 et Wav2Vec2-AASIST sont utilisés comme détecteurs.

> **检测。**AASIST、RawNet2 和 Wav2Vec2-AASIST 作为检测器发布──ASVspoof 2025 挑战赛 发布 SOTA 检测器对ElevenLabs、VALL-E 2 和 Bark 输出 EER为 0.8-2.3%──

### Nombre de personnes

> Numéro de l'année 2026

| Model | Zero-shot? | SECS (target sim) | WER (intel.) | Params |
|-------|-----------|--------------------|--------------|--------|
| F5-TTS | Yes | 0.72 | 2.1% | 335M |
| XTTS v2 | Yes | 0.65 | 3.5% | 470M |
| OpenVoice v2 | Yes | 0.70 | 2.8% | 220M |
| VALL-E 2 | Yes | 0.77 | 2.4% | 370M |
| VoiceBox | Yes | 0.78 | 2.1% | 330M |

| 模型 | 零样本？ | SECS（目标相似度） | WER（可懂度） | 参数量 |
|------|---------|-------------------|--------------|--------|
| F5-TTS | 是 | 0.72 | 2.1% | 3.35 亿 |
| XTTS v2 | 是 | 0.65 | 3.5% | 4.7 亿 |
| OpenVoice v2 | 是 | 0.70 | 2.8% | 2.2 亿 |
| VALL-E 2 | 是 | 0.77 | 2.4% | 3.7 亿 |
| VoiceBox | 是 | 0.78 | 2.1% | 3.3 亿 |

> **【中文解读】**Cette méthode "de zéro" peut aider à comprendre le principe derrière le cadre, en cas de problème, ne sera pas bloqué dans une boîte noire.


SECS > 0,70 est généralement indistinguible de la cible pour la plupart des auditeurs.

> SECS > 0,70 pour la plupart des auditeurs est généralement indistinguible de l'objectif.

> **【拓展：语音 AI 的产品化】**La technologie du langage est confrontée à des défis particuliers dans la fabrication de produits: différents sons, bruits de fond, prises de vue, nombreux discours, etc. Les produits de Siri, Alexa, et de petite enfance ont été largement optimisés pour résoudre ces "problèmes de longue durée".

> **【拓展：多语言语音技术】**Les caractéristiques du langage mondial sont énormes: la voix de la langue (en chinois comme en chinois) est à un niveau élevé, les ressources linguistiques sont faibles et les données de formation manquent.



## Construisez-le et mettez-le en œuvre.
```figure
sp-voice-factorize
```

## Faites-le

### Étape 1: décomposer avec la synthèse de reconnaissance (démo de code seulement dans main.py)

```python
def clone_pipeline(ref_audio, text, target_embedder, tts_model):
    speaker_emb = target_embedder.encode(ref_audio)
    mel = tts_model(text, speaker=speaker_emb)
    return vocoder(mel)
```

Conceptuellement simple; la masse de mise en œuvre est en `tts_model`et le haut-parleur encodeur.

> 概念上简单; réalisation`tts_model`Et le rédacteur en chef...

### Étape 2: clone à tir zéro avec F5-TTS

```python
from f5_tts.api import F5TTS
tts = F5TTS()
wav = tts.infer(
    ref_file="rohit_5s.wav",
    ref_text="The quick brown fox jumps over the lazy dog.",
    gen_text="Please add milk and bread to my list.",
)
```

La transcription de référence doit correspondre exactement à l'audio; l'incohérence rompt l'alignement.

> Les transcriptions doivent être complètement conformes à la fréquence; les non conformes peuvent nuire à la fréquence.

### Étape 3: Conversion vocale avec KNN-VC

```python
import torch
from knnvc import KNNVC  # 2023 model, https://github.com/bshall/knn-vc
vc = KNNVC.load("wavlm-base-plus")
out_wav = vc.convert(source="my_voice.wav", target_pool=["alice_1.wav", "alice_2.wav"])
```

KNN-VC exécute WavLM pour extraire des emblèmes par cadre pour la base de sources et la base de cibles, puis remplace chaque cadre source par son voisin le plus proche dans la base.

> KNN-VC 运行 WavLM 提取源和目标池的逐嵌入, puis utiliser le voisin le plus proche dans la piscine pour remplacer chaque source──非参数化,一分钟目标语音即可工作──

### Étape 4: intégrer une marque d'eau

```python
from silentcipher import SilentCipher
sc = SilentCipher(model="2024-06-01")
payload = b"consent_id:abc123;ts:1745353200"
watermarked = sc.embed(wav, sr=24000, message=payload)
detected = sc.detect(watermarked, sr=24000)   # returns payload bytes
```

~ 32 bits de charge utile, détectable après le recodage MP3 et le bruit léger.

> Environ 32 places de charge, MP3 encore à tester après le codage et le bruit léger.

### Étape 5: porte de consentement

```python
def cloned_inference(text, ref_audio, consent_record):
    assert verify_signature(consent_record), "Signed consent required"
    assert consent_record["speaker_id"] == hash_speaker(ref_audio)
    wav = tts.infer(ref_file=ref_audio, gen_text=text)
    wav = watermark(wav, payload=consent_record["id"])
    return wav
```

> **【中文解读】**Dans ce chapitre, nous allons montrer comment utiliser un cadre mature (comme PyTorch, HuggingFace, etc.) pour appliquer rapidement cette technique.





> **【拓展：语音与情感计算】**Le langage n'est pas seulement un moyen de transmettre des informations, il est également un moyen de transmettre des signaux émotionnels riches.

## Utilisez-le avec le cadre de réalisation

La pile de 2026:

> 2026:

| Situation | Pick |
|-----------|------|
| 5-sec zero-shot clone, open-source | F5-TTS or OpenVoice v2 |
| Commercial production cloning | ElevenLabs Instant Voice Clone v2.5 |
| Voice conversion (rewriting) | KNN-VC or Diff-HierVC |
| Many-speaker fine-tune | StyleTTS 2 + speaker adapter |
| Cross-lingual cloning | XTTS v2 or VALL-E X |
| Deepfake detection | Wav2Vec2-AASIST |

| 场景 | 选择 |
|------|------|
| 5 秒零样本克隆，开源 | F5-TTS 或 OpenVoice v2 |
| 商业生产级克隆 | ElevenLabs Instant Voice Clone v2.5 |
| 语音转换（重写） | KNN-VC 或 Diff-HierVC |
| 多说话人微调 | StyleTTS 2 + 说话人适配器 |
| 跨语言克隆 | XTTS v2 或 VALL-E X |
| 深度伪造检测 | Wav2Vec2-AASIST |



## Les pièges

> 常见陷

- **Misaligned reference transcript.**F5-TTS et autres éléments similaires exigent que le texte de référence correspond exactement à l'audio de référence, la ponctuation comprise.
  **参考转录不对齐。**F5-TTS et autres exigences de référence correspondent parfaitement aux émissions de référence, y compris les points de référence.
- **Reverberant reference.**Echo tue le clone, disque sec, microphone proche.
  **混响参考。**Je vais détruire le Klon.
- **Emotional mismatch.**La référence d'entraînement "joyeux" produit des clones joyeux de tout.
  **情感不匹配。**                                                                                                                                                                                                                                                              
- **Language leakage.**Le clonage d'un anglophone puis la demande au modèle de parler français porte souvent l'accent de toute façon; utilisez des modèles multilingues (XTTS, VALL-E X).
  **语言泄漏。**克隆英文说话人然后让模型说法语仍将带有口音; utiliser跨语言模型 (XTTS、VALL-E X) ⋅
- **No watermark.**Il est légalement impérissable dans l'UE à partir d'août 2026.
  **没有水印。**Depuis le 8 août 2026, il est indépendant de la législation de l'UE.

> **【中文解读】**Cette section se concentre sur la façon de déployer le modèle en tant que produit disponible. De l'original au système de production, il faut considérer plusieurs dimensions de l'optimisation des performances, du traitement des erreurs, du contrôle, etc.


## Envoyez-le . Produit .

- Je ne sais pas .`outputs/skill-voice-cloner.md`. Conception d'un pipeline de clonage ou de conversion avec passerelle de consentement + marque d'eau + cible de qualité.

> 保存为 `outputs/skill-voice-cloner.md`◊ design avec consentement + 水印 + 质量目标的克隆或转换流水线──

## Les exercices

1. **Easy.**On court .`code/main.py`. Démontre le swap intégrant le haut-parleur en calculant le cosine entre deux " haut-parleurs " avant et après le swap.
   **简单。**运行  référencement`code/main.py`◊ par calcul de la similitude des deux "parlers" qui se sont insérés dans le partage.
2. **Medium.**Utilisez OpenVoice v2 pour cloner votre propre voix. Mesurez SECS entre référence et clone. Mesurez CER via Whisper.
   **中等。**Avec OpenVoice v2 克隆你自己的声音──测量参考与克隆之间的SECS──通过 语测 CER──
3. **Hard.**Appliquez le symbole d'eau SilentCipher à 20 clones, exécutez-les à travers le code MP3 + décode de 128 kbps, détectez la charge utile.
   **困难。**Pour 20 000 applications SilentCipher, l'imprimerie est en cours de 128 kbps MP3 编码+解码,检测载荷――报告比特准确率──

> **【中文解读】**Dans le tableau des termes, la définition du terme "ce que les gens disent" et "ce qu'il signifie réellement" est différenciée entre le langage quotidien et la signification technique précise.


## Les termes clés

| Term | What people say | What it actually means |
|------|-----------------|-----------------------|
| Zero-shot clone | 5 seconds is enough | Pretrained model + speaker embedding; no training. |
| PPG | Phonetic posteriorgram | Per-frame ASR posteriors used as language-agnostic content rep. |
| KNN-VC | Nearest-neighbor conversion | Replace each source frame with nearest target-pool frame. |
| Neural codec TTS | VALL-E style | AR model over EnCodec/SoundStream tokens. |
| Watermark | Inaudible signature | Bits embedded in audio, survive re-encode. |
| SECS | Cloning fidelity | Cosine between target and clone speaker embeddings. |
| AASIST | Deepfake detector | Anti-spoof model; detects synthesized speech. |

| 术语 | 人们常说的 | 实际含义 |
|------|-----------|---------|
| 零样本克隆 | 5 秒就够了 | 预训练模型 + 说话人嵌入；无需训练。 |
| PPG | 音素后验图 | 逐帧 ASR 后验，用作语言无关的内容表示。 |
| KNN-VC | 最近邻转换 | 用目标池中最近邻替换每个源帧。 |
| 神经编解码 TTS | VALL-E 风格 | 在 EnCodec/SoundStream token 上的 AR 模型。 |
| 水印 | 不可听签名 | 嵌入音频中的比特，经受重编码。 |
| SECS | 克隆保真度 | 目标与克隆说话人嵌入之间的余弦相似度。 |
| AASIST | 深度伪造检测器 | 反欺诈模型；检测合成语音。 |

> **【中文解读】**延伸阅读 fournit des ressources de haute qualité pour l'apprentissage en profondeur. Ces articles et cours sont des références classiques dans ce domaine, adaptés aux lecteurs qui ont besoin d'une compréhension approfondie.


## Encore une lecture

- [Chen et al. (2024). F5-TTS](https://arxiv.org/abs/2410.06885) clonage de SOTA à source ouverte.
  Le projet de loi de la Commission sur les droits de l'homme (CEP) est en cours de réalisation.
- [Baevski et al. / Microsoft (2023). VALL-E](https://arxiv.org/abs/2301.02111)et [VALL-E 2 (2024)](https://arxiv.org/abs/2406.05370) TTS de codec neuronal.
  Baevski 等 / 微软 (2023). VALL-E 和 VALL-E 2(2024)  神经编解码 TTS──
- [Qian et al. (2019). AutoVC](https://arxiv.org/abs/1905.05879) conversion vocale basée sur la décomposition.
  Qian 等 (2019). AutoVC basé sur la résolution的语音转换──
- [Baas, Waubert de Puiseau, Kamper (2023). KNN-VC](https://arxiv.org/abs/2305.18975) VC basé sur la récupération.
  Baas, Waubert de Puiseau, Kamper (2023). KNN-VC basé sur le contrôle des échanges de voix
- [SilentCipher (2024) — Audio Watermarking](https://github.com/sony/silentcipher) Marque-eau audio 32 bits prête à la production.
  SilentCipher 音频水印 生产可用 32 位音频水印──
- [ASVspoof 2025 results](https://www.asvspoof.org/) course aux armements détecteur contre synthétiseur, mise à jour en 2026.
  ASVspoof 2025 结果检测器 vs 合成器军备竞赛,2026 年更新。

> **【中文解读】**延伸阅读 a fourni des ressources de haute qualité pour l'apprentissage en profondeur, y compris des articles, des cours et des outils.

