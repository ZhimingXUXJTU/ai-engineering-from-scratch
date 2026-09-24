# Voix anti-fraudes et marquage d'eau audio  ASVspoof 5, AudioSeal, WaveVerify 语音防伪与音频水印

> Le clonage vocale est livré plus rapidement que les défenses. Les systèmes de voix de production 2026 ont besoin de deux choses: un détecteur (AASIST, RawNet2) qui classe la parole réelle contre fausse, et un marque-eau (AudioSeal) qui survit à la compression et à l'édition.

> **【中文解读】**Le système de production de langage de 2026 ans nécessite deux choses: un testeur (AASIST, RawNet2) et un véritable système de langage (AudioSeal) qui peut être utilisé pour la compression et l'édition.

**Type:** Build | **类型:** 构建
**Languages:** Python | **语言:** Python
**Prerequisites:** Phase 6 · 06 (Speaker Recognition), Phase 6 · 08 (Voice Cloning) | **前置知识:** 阶段 6 · 06（说话人识别），阶段 6 · 08（语音克隆）
**Time:** ~75 minutes | **预计用时:** ~75 分钟

## Le problème , l' introduction du problème

Trois défenses connexes:

> 3 types de défense:

> **【中文解读】**La question posée dans ce chapitre est la suivante: comment comprendre et appliquer correctement cette technique dans la conception pratique. Comprendre le contexte de la question aide à saisir les principaux facteurs de décision concernant le type de technologie. Dans les systèmes d'IA réels, le type de technique erroné coûte souvent plus cher que le coût de la mise en œuvre de détails.


1. **Anti-spoofing / deepfake detection.**Compte tenu d'un clip audio, est-il synthétique ou réel ?
   Le mot grec traduit par " le mot grec "**反欺骗/深度伪造检测。**给定一段音频, juger si c'est synthétique ou réel ?
2. **Audio watermarking.**Embed un signal imperceptible dans l'audio généré qu'un détecteur peut extraire plus tard.
   Le mot grec traduit par " le mot grec "**音频水印。**En effet, les signaux sont insérés dans le son généré, puis peuvent être extraits.
3. **Authenticated provenance.**Signature cryptographique des fichiers audio + métadonnées.
   Le mot grec traduit par " le mot grec "**认证来源。**音频文件 + 元数据的加密签名──C2PA / 内容真实性倡议──

La détection gère les adversaires qui ne coopèrent pas. Le marquage d'eau gère la conformité  L'audio généré par l'IA devrait être identifiable comme tel. Les deux sont nécessaires en 2026.

> 检测应对不配合的攻击者──水印应对合规性AI 生成的音频应被识别──2026年 两者都是必需的──

## Le concept de base.

> **【中文解读】**Le présent article présente les concepts et les bases théoriques de base. La connaissance de ces concepts est la prémisse de la réalisation de la réalisation de la réalisation, mais aussi le point de connaissance de l'interview et de la pratique de l'ingénierie.


![Anti-spoofing vs watermarking vs provenance — three defense layers](../assets/spoofing-watermark.svg)

### ASVspoof 5  le point de référence 2024-2025

> ASVspoof 5  2024-2025 年基准测试

Le plus grand changement par rapport aux éditions précédentes:

> La plus grande variation par rapport à la version précédente:

- **Crowdsourced data**(pas de studio propre)  conditions réalistes.
  Le mot grec traduit par " le mot grec "**众包数据**(Non enregistré)
- **~2000 speakers**(versus ~ 100 avant).
  Le mot grec traduit par " le mot grec "**约 2000 名说话人**(Béché environ 100 名)
- **32 attack algorithms.**TTS + conversion vocale + perturbation adversitaire.
  Le mot grec traduit par " le mot grec "**32 种攻击算法。**TTS + 语音转换 + 对抗性扰动──
- **Two tracks.**Contremaçon (CM) détection autonome; ASV (SASV) à contre-pied pour les systèmes biométriques.
  Le mot grec traduit par " le mot grec "**两个赛道。**Les mesures de lutte contre la fraude (CM)

Le plus récent sur ASVspoof 5: ~ 7,23% EER. Sur le plus ancien ASVspoof 2019 LA: 0,42% EER. Déploiement dans le monde réel: attendez-vous à 5-10% EER sur les clips en plein air.

> Les résultats de l'étude de la première année de l'étude de l'ASV sont les suivants:

### Familles de modèles de détection AASIST et RawNet2 

> AASIST 和 RawNet2  检测模型家族

**AASIST**(en 2021, mis à jour jusqu'en 2026).

> **AASIST**Les mesures de réaction sont les suivantes:

**RawNet2.**Convolution de l'avant-dernier sur la forme d'onde brute + L'épine dorsale TDNN.

> **RawNet2。**Le premier est le premier et le dernier est le second.

**NeXt-TDNN + SSL features.**Variante 2025: ECAPA-style + fonctionnalités WavLM + perte de focus. atteint le 0,42% EER sur ASVspoof 2019 LA.

> **NeXt-TDNN + SSL 特征。**2025 年变体:ECAPA 风格 + WavLM 特征 + perte de focus──在 ASVspoof 2019 LA atteint 0,42% de l'EER──

### AudioSeal  le marque-eau 2024 par défaut

> AudioSeal  2024 année de l'écriture

Les méta **AudioSeal**(Jan 2024, v0.2 Déc 2024): conception clé:

> Meta **AudioSeal**Le projet de loi de la République de Suisse est un projet de loi de la République de Suisse.

- **Localized.**Détecte le marque-eau par cadre à 16 kHz (1/16000 s) de résolution de l'échantillon.
  Le mot grec traduit par " le mot grec "**局部化。**É 16 kHz 采样分辨率逐检测水印 ((1/16000 秒) ⋅
- **Generator + detector jointly trained.**Le générateur apprend à intégrer un signal inaudible; le détecteur apprend à le trouver par des augmentations.
  Le mot grec traduit par " le mot grec "**生成器 + 检测器联合训练。**Il est également possible de trouver des informations sur les données de l'appareil.
- **Robust.**Survient à la compression MP3 / AAC, à l' EQ, à la vitesse de changement ±10%, au mélange bruyant +10 dB SNR.
  Le mot grec traduit par " le mot grec "**鲁棒。**能经受 MP3/AAC 压缩、均衡、±10% 变速、+10 dB SNR 噪音混合──
- **Fast.**Le détecteur fonctionne à 485 fois en temps réel, 1000 fois plus vite que WavMark.
  Le mot grec traduit par " le mot grec "**快速。**Le détecteur fonctionne à 485 fois la vitesse réelle; par rapport à WavMark 快 1000 倍。
- **Capacity.**Charge utile de 16 bits (peut encoder le modèle ID, le timestamp de génération, l'ID utilisateur) intégrable dans chaque déclaration.
  Le mot grec traduit par " le mot grec "**容量。**16 位载荷(可编码模型 ID、生成时间、用户 ID) peut être intégré dans chaque segment语音。

### Le marqueur

Le baseline pré-AudioSeal est ouvert.

> AudioSeal 之前的开源基线──可逆神经网络,32 位/秒──问题:

- La synchronisation brute force est lente.
  Le violent coup de foudre est lent.
- Peut être retiré par bruit gaussien ou par compression MP3.
  En français, le mot "révérence" est traduit par "révérence".
- Pas amicale en temps réel.
  Le film est aussi connu sous le nom de "The Real World".

### La révision de la loi sur les droits de l'homme

Résolve les faiblesses d'AudioSeal  spécifiquement les manipulations temporelles (inversion, vitesse). Utilise un générateur basé sur FiLM + détecteur Mixture-of-Experts. Compétitif avec AudioSeal sur les attaques standard; gère les modifications temporelles.

> Résoudre les faiblesses de l'AudioSeal  en particulier l'opération de temps 反转、变速)  Utiliser un générateur basé sur FiLM + MoE 检测器──

### Les adversaires exploitent les lacunes

De AudioMarkBench: "sous le changement de pitch, tous les marqueurs d'eau montrent une précision de récupération de bits inférieure à 0,6, ce qui indique une suppression presque complète". **Pitch-shift is the universal attack.**Le marquage d'eau n° 2026 est entièrement robuste pour la modification agressive du ton.

> 攻击者利用的漏洞──来自 AudioMarkBench:"En dessous du seuil de déviation, le taux de récupération de tous les emblèmes est inférieur à 0,6, ce qui indique qu'ils ont été presque complètement supprimés".""**音高偏移是通用攻击。**没有任何2026年水印能完全抵御激进的音高修改──这就是为什么你需要检测(AASIST) 和水印配合使用──

### C2PA / Initiative sur l'authenticité du contenu

Il est également possible de modifier le format de la vidéo en utilisant des fichiers audio.

> C2PA / 内容真实性倡议──不是机器学习技术是一种清单形式──音频文件携带关于创建工具、作者、日期的加密签名元数据──Audobox / Seamless 使用它── est avantageux pour la retracée; mais si les malfaiteurs re-chodifient et déchiffrent les données, elles sont inefficaces──

> **【拓展：语音 AI 的产品化】**La technologie du langage est confrontée à des défis particuliers dans la fabrication de produits: différents sons, bruits de fond, prises de vue, nombreux discours, etc. Les produits de Siri, Alexa, et de petite enfance ont été largement optimisés pour résoudre ces "problèmes de longue durée".

> **【拓展：多语言语音技术】**Les caractéristiques du langage mondial sont énormes: la voix de la langue (en chinois comme en chinois) est à un niveau élevé, les ressources linguistiques sont faibles et les données de formation manquent.

> **【拓展：语音隐私与安全】**Les données de la langue contiennent une grande quantité d'informations personnelles confidentielles (en anglais) et sont très fausses (en anglais).




## Construisez-le et mettez-le en œuvre.

> **【中文解读】**Cette méthode "de zéro" peut aider à comprendre le principe derrière le cadre, en cas de problème, ne sera pas bloqué dans une boîte noire.

```figure
v4-audio-watermark
```

## Faites-le

### Étape 1: un simple détecteur de caractéristiques spectrales (jouet)

> 步骤 1: simple séquence de fréquence

```python
def spectral_rolloff(spec, percentile=0.85):
    cum = 0
    total = sum(spec)
    if total == 0:
        return 0
    threshold = total * percentile
    for k, v in enumerate(spec):
        cum += v
        if cum >= threshold:
            return k
    return len(spec) - 1

def is_suspicious(audio):
    spec = magnitude_spectrum(audio)
    rolloff = spectral_rolloff(spec)
    return rolloff / len(spec) > 0.92
```

La parole synthétique a souvent une énergie à haute fréquence inhabituellement plate.

> Le synthèse de la voix a généralement une énergie de haute fréquence inhabituelle.

### Étape 2: Embed audioSeal + détecte

> 步骤 2:AudioSeal 嵌入 + 检测

```python
from audioseal import AudioSeal
import torch

generator = AudioSeal.load_generator("audioseal_wm_16bits")
detector = AudioSeal.load_detector("audioseal_detector_16bits")

audio = load_wav("generated.wav", sr=16000)[None, None, :]
payload = torch.tensor([[1, 0, 1, 1, 0, 1, 0, 0, 1, 1, 0, 1, 0, 1, 1, 0]])
watermark = generator.get_watermark(audio, sample_rate=16000, message=payload)
watermarked = audio + watermark

result, decoded_payload = detector.detect_watermark(watermarked, sample_rate=16000)
# result: float in [0, 1] — probability of watermark presence
# decoded_payload: 16 bits; match against embedded payload
```

### Étape 3: évaluation  RSE

> 步骤 3: évaluer  EER(等 taux d'erreur)

```python
def eer(real_scores, fake_scores):
    thresholds = sorted(set(real_scores + fake_scores))
    best = (1.0, 0.0)
    for t in thresholds:
        far = sum(1 for s in fake_scores if s >= t) / len(fake_scores)
        frr = sum(1 for s in real_scores if s < t) / len(real_scores)
        if abs(far - frr) < best[0]:
            best = (abs(far - frr), (far + frr) / 2)
    return best[1]
```

### Étape 4: intégration de la production

> 步骤 4: production de la classe de l'intégration

```python
def safe_tts(text, voice, clone_reference=None):
    if clone_reference is not None:
        verify_consent(user_id, clone_reference)
    audio = tts_model.synthesize(text, voice)
    audio_with_wm = audioseal_embed(audio, payload=build_payload(user_id, model_id))
    manifest = c2pa_sign(audio_with_wm, user_id, timestamp=now())
    return audio_with_wm, manifest
```

> **【中文解读】**Dans ce chapitre, nous allons montrer comment utiliser un cadre mature (comme PyTorch, HuggingFace, etc.) pour appliquer rapidement cette technique.


Chaque génération de navires: (1) marque d'eau, (2) manifeste signé, (3) journal d'audit conforme à la politique de conservation.

> Chaque production est composée de: 1) un code d'eau, 2) une liste de signatures, 3) un journal d'audit conforme à la stratégie de conservation.




> **【拓展：语音与情感计算】**Le langage n'est pas seulement un moyen de transmettre des informations, il est également un moyen de transmettre des signaux émotionnels riches.

## Utilisez-le avec le cadre de réalisation

| Use case | Defense |
|----------|---------|
| Shipping TTS / voice cloning / 上线 TTS/语音克隆 | AudioSeal embed on every output (non-negotiable) / 每次输出嵌入 AudioSeal（不可妥协） |
| Biometric voice unlock / 生物识别语音解锁 | AASIST + ECAPA ensemble; liveness challenge / AASIST + ECAPA 集成；活体挑战 |
| Call-center fraud detection / 呼叫中心欺诈检测 | AASIST on 20% sample of incoming calls / 对 20% 的来电做 AASIST 检测 |
| Podcast authenticity / 播客真实性 | C2PA signing on upload, AudioSeal if AI-generated / 上传时 C2PA 签名，AI 生成则加 AudioSeal |
| Research / training detectors / 研究/训练检测器 | ASVspoof 5 train/dev/eval sets / ASVspoof 5 训练/开发/评估集 |



## Les pièges

> 常见陷

- **Watermark without detector ever running.**Pas de sens, envoyez le détecteur dans votre informateur.
  Le mot grec traduit par " le mot grec "**嵌入水印但从未运行检测器。**Il n'y a pas de sens à la mise en place de l'émetteur de test.
- **Detection without calibration.**AASIST est formé à des sur-exploits de l'ASV, des baisses de précision dans le monde réel.
  Le mot grec traduit par " le mot grec "**检测未校准。**Les résultats de l'AASIST sont adaptés; le taux de précision réel est en baisse.
- **Pitch-shift gap.**Le changement de pitch agressif supprime la plupart des marqueurs d'eau.
  Le mot grec traduit par " le mot grec "**音高偏移漏洞。**激进的音高偏移能去除大多数水印──准备检测作为后备──
- **Metadata strip-and-rehost.**C2PA est trivialement contourné par le re-encodage. Ajoutez toujours la défense cryptographique + perceptuelle (marque d'eau) ensemble.
  Le mot grec traduit par " le mot grec "**元数据剥离重新托管。**C2PA 通过重新编码即可轻松绕过──始终同时使用加密 + 感知(水印) défense──
- **Liveness as detection.**Demandez à l'utilisateur de dire une phrase aléatoire.
  Le mot grec traduit par " le mot grec "**活体检测作为检测手段。**让用户说一个随机短语──能防止重发攻击但不能防止实时克隆──

> **【中文解读】**Cette section se concentre sur la façon de déployer le modèle en tant que produit disponible. De l'original au système de production, il faut considérer plusieurs dimensions de l'optimisation des performances, du traitement des erreurs, du contrôle, etc.


## Envoyez-le . Produit .

- Je ne sais pas .`outputs/skill-spoof-defender.md`. Choisir le modèle de détection, le marque-eau, le manifeste de provenance et le manuel de jeu opérationnel pour un déploiement de génération de voix.

> 保存为 `outputs/skill-spoof-defender.md`◊ Pour un modèle de production de voix, un modèle de sélection de tests, un code d'origine et un manuel de gestion.

## Les exercices

1. **Easy.**On court .`code/main.py`- Détecteur de jouets + marque d'eau de jouets intégré/détecté sur audio synthétique.
   Le mot grec traduit par " le mot grec "**简单。**运行  référencement`code/main.py`◊ dans le synthétiseur audio sur test test de jouets tester + 玩具水印嵌入/检测。
2. **Medium.**Installez`audioseal`, intégrer une charge utile de 16 bits dans une sortie TTS, redécoder, corrompre l'audio avec le bruit et mesurer la précision de récupération de bits.
   Le mot grec traduit par " le mot grec "**中等。**Montage`audioseal`, dans le TTS 输出嵌入 16 位荷荷,重新解码──使用噪音损坏音频并测量位恢复准确率──
3. **Hard.**Télégraphie un RawNet2 ou un AASIST sur ASVspoof 2019 LA. Mesure EER. Testez sur un ensemble de clips générés par F5-TTS  voir comment la détection OOD se dégrade.
   Le mot grec traduit par " le mot grec "**困难。**En 2019, la première édition de l'ASIS est diffusée en ligne.

> **【中文解读】**Dans le tableau des termes, la définition du terme "ce que les gens disent" et "ce qu'il signifie réellement" est différenciée entre le langage quotidien et la signification technique précise.


## Les termes clés

| Term | What people say | What it actually means |
|------|-----------------|-----------------------|
| ASVspoof | The benchmark | Biennial challenge; 2024 = ASVspoof 5. / 双年挑战赛；2024 = ASVspoof 5 |
| CM (countermeasure) | Detector | Classifier: real speech vs synthetic / converted. / 分类器：真实语音 vs 合成/转换语音 |
| SASV | Speaker verif + CM | Integrated biometric + spoof detection. / 集成生物识别 + 欺骗检测 |
| AudioSeal | Meta watermark | Localized, 16-bit payload, 485× faster than WavMark. / 局部化，16 位载荷，比 WavMark 快 485 倍 |
| Bit Recovery Accuracy | Watermark survival | Fraction of payload bits recovered after attack. / 攻击后恢复的载荷位比例 |
| C2PA | Provenance manifest | Cryptographic metadata about creation / authorship. / 关于创建/作者身份的加密元数据 |
| AASIST | Detector family | Graph-attention-based anti-spoofing SOTA. / 基于图注意力的反欺骗 SOTA |

> **【中文解读】**延伸阅读 fournit des ressources de haute qualité pour l'apprentissage en profondeur. Ces articles et cours sont des références classiques dans ce domaine, adaptés aux lecteurs qui ont besoin d'une compréhension approfondie.


## Encore une lecture

- [Todisco et al. (2024). ASVspoof 5](https://dl.acm.org/doi/10.1016/j.csl.2025.101825) l'indice de référence actuel.
  Le président de la République a déclaré que la Commission européenne avait été informée de la décision de la Commission européenne de la mise en œuvre de la politique de sécurité et de sécurité.
- [Defossez et al. (2024). AudioSeal](https://arxiv.org/abs/2401.17264) la marque d'eau par défaut.
  Le programme de défense des droits de l'homme est présenté en décembre 2024.
- [Chen et al. (2025). WaveVerify](https://arxiv.org/abs/2507.21150)Détecteur de détection de température.
  Chen 等(2025). Vérifier les ondes en fonction des attaques de temps MoE 检测器
- [Jung et al. (2022). AASIST](https://arxiv.org/abs/2110.01200) l'épine dorsale de détection de SOTA.
  Pour les personnes âgées, il est nécessaire de faire une évaluation de la qualité de la structure de la structure.
- [AudioMarkBench (2024)](https://proceedings.neurips.cc/paper_files/paper/2024/file/5d9b7775296a641a1913ab6b4425d5e8-Paper-Datasets_and_Benchmarks_Track.pdf) évaluation de la robustesse.
  L'équipe de recherche a été créée pour la première fois en 2024.
- [C2PA specification](https://c2pa.org/specifications/specifications/) format du manifeste de provenance.
  C2PA 规范来源清单格式──

> **【中文解读】**延伸阅读 a fourni des ressources de haute qualité pour l'apprentissage en profondeur, y compris des articles, des cours et des outils.

