# Text-to-Speech (TTS)  De Tacotron à F5 et Kokoro 语音合成  De Tacotron à F5 et Kokoro

> L'ASR inverse la parole vers le texte; TTS inverse le texte vers la parole. La pile 2026 est composée de trois parties: texte → jetons, jetons → mel, mel → forme d'onde. Chaque partie a un modèle par défaut qui s'inscrit dans un ordinateur portable.

> **【中文解读】**ASR Faire un changement de langage, TTS Faire un changement de langage.

> **【拓展：TTS 的应用】**TTS est une technique de base, qui est la plus répandue de tous les pays.

**Type:** Build | **类型:** 构建
**Languages:** Python | **语言:** Python
**Prerequisites:** Phase 6 · 02 (Spectrograms & Mel), Phase 5 · 09 (Seq2Seq), Phase 7 · 05 (Full Transformer) | **前置知识:** 阶段 6 · 02（频谱图与 Mel），阶段 5 · 09（Seq2Seq），阶段 7 · 05（完整 Transformer）
**Time:** ~75 minutes | **预计用时:** ~75 分钟

## Le problème , l' introduction du problème

Vous avez une chaîne: "S'il vous plaît rappelez-moi d'arroser les plantes à 18h". Vous avez besoin d'un clip audio de 3 secondes qui sonne naturel, a une prosodie correcte (pauses, stress), prononce "plants" avec la bonne voyelle, et fonctionne en moins de 300 ms sur un processeur pour un assistant vocal en direct. Vous devez également échanger des voix, gérer des entrées modifiées par code (" rappelez-moi à 18h, daijoubu ? ") et ne pas vous embarrasser sur les noms.

> Vous avez besoin d'un passage de 3 secondes pour arroser les plantes à 18h. Vous avez besoin de trois secondes pour les arroser. Vous avez besoin de trois secondes pour les arroser. Vous avez besoin de trois secondes pour les arroser.

> **【中文解读】**La question posée dans ce chapitre est la suivante: comment comprendre et appliquer correctement cette technique dans la conception pratique. Comprendre le contexte de la question aide à saisir les principaux facteurs de décision concernant le type de technologie. Dans les systèmes d'IA réels, le type de technique erroné coûte souvent plus cher que le coût de la mise en œuvre de détails.

Les conduites TTS modernes ressemblent à ceci:

> 现代 TTS 流水线如下:

1. **Text frontend.**Normalizer le texte (dates, numéros, courriels), convertir en phonèmes ou en jetons de sous-parts, prédire les caractéristiques de prosodie.
   **文本前端。**归一化文本(日期、数字、邮箱),转换为音素或子词代币,预测律特征──
2. **Acoustic model.**Le texte → spectrogramme mel. Tacotron 2 (2017), FastSpeech 2 (2020), VITS (2021), F5-TTS (2024), Kokoro (2024).
   **声学模型。**文本 → Mel 频谱图──Tacotron 2(2017)、FastSpeech 2(2020)、VITS(2021)、F5-TTS(2024)、Kokoro(2024)。
3. **Vocoder.**Mel → forme d'onde. WaveNet (2016), WaveRNN, HiFi-GAN (2020), BigVGAN (2022), vocoders de codec neuronal en 2024+.
   **声码器。**Le réseau de référencement de l'équipe de référencement de l'équipe de référencement de l'équipe de référencement de l'équipe de référencement de l'équipe de référencement de l'équipe de référencement de l'équipe de référencement de l'équipe de référencement de l'équipe de référencement de l'équipe de référencement de l'équipe de référencement de l'équipe de référencement de l'équipe de référencement de l'équipe de référencement de l'équipe de référencement de l'équipe de référencement de l'équipe de référencement de l'équipe de référencement de référencement de l'équipe de référencement de référencement de l'équipe de référencement de référencement de référencement de l'équipe de référencement de référencement de référencement de référencement de référencement de référencement de référencement de référencement de référencement de référencement de référencement de référencement de référencement de référencement de référencement de référencement de référencement de référencement de référencement de référencement de référencement de référencement de référencement de référencement de référencement de référencement de référencement de référencement de référencement de référencement de référencement de référencement de référencement de référencement de référencement de référencement de référencement de référencement de référencement de référencement de référencement de référencement de référencement de référencement de référencement de référencement de référencement de référencement de référencement de référencement de référencement de référencement de référencement de référencement de référencement de référ

En 2026, le vocomodeur acoustique + se divise avec des modèles de diffusion de bout en bout et de correspondance de flux.

> En 2026, avec l'émergence du modèle de diffusion et de coordonnée, les limites du modèle sonore + du codeur sonore deviennent floues.

## Le concept de base.

> **【中文解读】**Le présent article présente les concepts et les bases théoriques de base. La connaissance de ces concepts est la prémisse de la réalisation de la réalisation de la réalisation, mais aussi le point de connaissance de l'interview et de la pratique de l'ingénierie.


![Tacotron, FastSpeech, VITS, F5/Kokoro side-by-side](../assets/tts.svg)

**Tacotron 2 (2017).**Seq2seq: char-embedding → BiLSTM encoder → attention à l'emplacement → décodeur LSTM autorégressif émet des cadres mel. Lent (AR), oscillant sur le texte long.

> **Tacotron 2（2017）。**Seq2seq:字符嵌入 → BiLSTM 编码器 → 位置敏感注意力 → 自归 LSTM 解码器输出 mel ──慢(AR),长文本不稳定──仍被引用为基线──

**FastSpeech 2 (2020).**Non autorégressif. Prédcteur de durée donne le nombre de cadres mel chaque phonème obtient. 1 passe, 10 fois plus rapide que Tacotron. Perde une certaine naturalité (alignement monotonique) mais se déplace partout.

> **FastSpeech 2（2020）。**Non-auto-retour. Le temps de prédiction est de 10 fois plus rapide que le Tacotron.

**VITS (2021).**Le système de communication est un système de communication de données qui permet de créer des connexions de connexion entre les deux systèmes.

> **VITS（2021）。**联合训练编码器 + 基流的时长预测 + HiFi-GAN 声码器端到端,使用变分推断。高质量,单模型。2022-2024年主导开源 TTS。变体:YourTTS(多说话人零样本)、XTTS v2(2024,Coqui)。

**F5-TTS (2024).**Transformateur de diffusion sur l'alignement de flux. prosodie naturelle, clonage vocale à tir zéro avec 5 secondes d'audio de référence. haut des classements TTS open source 2026.

> **F5-TTS（2024）。**基于流匹配的扩散 Transformer──自然律,5 seconds référence音频零样本声音克隆──2026年开源 TTS 排行榜榜榜首──3.35亿参数──

**Kokoro (2024).**Petit (82M), fonctionnel par CPU, TTS anglais de première classe pour une utilisation en temps réel.

> **Kokoro（2024）。**Il est également disponible en version téléphonique en anglais TTS.

**OpenAI TTS-1-HD, ElevenLabs v2.5, Google Chirp-3.**ElevenLabs v2.5 émotion tags (" [soupçonné]", "[rires] ") et les voix des personnages dominent la production de livres audio en 2026.

> **OpenAI TTS-1-HD、ElevenLabs v2.5、Google Chirp-3。**商业 SOTA──ElevenLabs v2.5 的情感标签("sussurré"、"rires")和角色声音主导 2026 年有声书制作──

### Évolution du vocoder

> ### 声码器演进

| Era | Vocoder | Latency | Quality |
|-----|---------|---------|---------|
| 2016 | WaveNet | offline only | SOTA at release |
| 2018 | WaveRNN | ~realtime | good |
| 2020 | HiFi-GAN | 100× realtime | near-human |
| 2022 | BigVGAN | 50× realtime | generalizes across speakers/langs |
| 2024 | SNAC, DAC (neural codecs) | integrated with AR models | discrete tokens, bit-efficient |

| 时代 | 声码器 | 延迟 | 质量 |
|------|--------|------|------|
| 2016 | WaveNet | 仅离线 | 发布时 SOTA |
| 2018 | WaveRNN | 约实时 | 良好 |
| 2020 | HiFi-GAN | 100× 实时 | 接近人类 |
| 2022 | BigVGAN | 50× 实时 | 跨说话人/语言泛化 |
| 2024 | SNAC, DAC（神经编解码器） | 与 AR 模型集成 | 离散 token，比特高效 |

D'ici 2026, la plupart des modèles "TTS" sont de bout en bout du texte à la forme d'onde; le spectrogramme mel est une représentation interne.

> En 2026, la plupart des modèles "TTS" sont de texte à forme de mouvement; le schéma de fréquence est une représentation interne.

### Évaluation

> ###  évaluer

- **MOS (Mean Opinion Score).**1 à 5 écailles, crowd-sourced.
  **MOS（平均意见分）。**1-5 分量表,众包── encore est le standard; speed painfully slow──
- **CMOS (Comparative MOS).**Préférence A-V-B, intervalles de confiance plus resserrés par annotation.
  **CMOS（比较 MOS）。**A-vs-B  préférence ⋅ chaque marque de la position de confiance ⋅
- **UTMOS, DNSMOS.**Préditeurs neuraux sans référence, utilisés pour les classements.
  **UTMOS、DNSMOS。**无参考神经 MOS 预测器──用于排行榜──
- **CER (Character Error Rate) via ASR.**Exécutez la sortie TTS par Whisper, calculer le CER contre le texte d'entrée.
  **CER（字符错误率）通过 ASR。**Pour les TTS, le code de référence est le code de référence.
- **SECS (Speaker Embedding Cosine Similarity).**Qualité du clonage vocale.
  **SECS（说话人嵌入余弦相似度）。**La qualité de la musique

Numéros 2026 sur le nettoyage des essais LibriTTS:

> Les résultats de l'essai LibriTTS de 2026

| Model | UTMOS | CER (via Whisper) | Size |
|-------|-------|-------------------|------|
| Ground truth | 4.08 | 1.2% | — |
| F5-TTS | 3.95 | 2.1% | 335M |
| XTTS v2 | 3.81 | 3.5% | 470M |
| VITS | 3.62 | 3.1% | 25M |
| Kokoro v0.19 | 3.87 | 1.8% | 82M |
| Parler-TTS Large | 3.76 | 2.8% | 2.3B |

| 模型 | UTMOS | CER（通过 Whisper） | 大小 |
|------|-------|---------------------|------|
| 真实音频 | 4.08 | 1.2% | — |
| F5-TTS | 3.95 | 2.1% | 3.35 亿 |
| XTTS v2 | 3.81 | 3.5% | 4.7 亿 |
| VITS | 3.62 | 3.1% | 2500 万 |
| Kokoro v0.19 | 3.87 | 1.8% | 8200 万 |
| Parler-TTS Large | 3.76 | 2.8% | 23 亿 |

> **【中文解读】**Cette méthode "de zéro" peut aider à comprendre le principe derrière le cadre, en cas de problème, ne sera pas bloqué dans une boîte noire.

> **【拓展：语音 AI 的产品化】**La technologie du langage est confrontée à des défis particuliers dans la fabrication de produits: différents sons, bruits de fond, prises de vue, nombreux discours, etc. Les produits de Siri, Alexa, et de petite enfance ont été largement optimisés pour résoudre ces "problèmes de longue durée".

> **【拓展：多语言语音技术】**Les caractéristiques du langage mondial sont énormes: la voix de la langue (en chinois comme en chinois) est à un niveau élevé, les ressources linguistiques sont faibles et les données de formation manquent.




## Construisez-le et mettez-le en œuvre.
```figure
sp-tts-stack
```

## Faites-le

### Étape 1: phonémiser l'entrée

```python
from phonemizer import phonemize
ph = phonemize("Hello world", language="en-us", backend="espeak")
# 'həloʊ wɜːld'
```

Les phonèmes sont le pont universel. Évitez de fournir du texte brut à tout ce qui est en dessous de la qualité du niveau VITS.

> 音素是通用桥梁──避免将原始文本输入到VITS 级别以下的任何模型──

### Étape 2: exécuter Kokoro (2026 CPU par défaut)

```python
from kokoro import KPipeline
tts = KPipeline(lang_code="a")  # "a" = American English
audio, sr = tts("Please remind me to water the plants at 6 pm.", voice="af_bella")
# audio: float32 tensor, sr=24000
```

Il fonctionne hors ligne, un seul fichier, 82M paramètres.

> - Il y a une seule série de documents.

### Étape 3: exécuter F5-TTS avec clonage vocale

```python
from f5_tts.api import F5TTS
tts = F5TTS()
wav = tts.infer(
    ref_file="my_voice_5s.wav",
    ref_text="The quick brown fox jumps over the lazy dog.",
    gen_text="Please remind me to water the plants.",
)
```

Passez un clip de référence de 5 secondes + sa transcription; F5 clone la prosodie et le timbre.

> 传入 5 seconds référence audio频 + 其转录文本; F5 克隆律和音色──

### Étape 4: Vocoder HiFi-GAN à partir de zéro

Trop grand pour s'intégrer dans un script tutoriel, mais la forme est:

```python
class HiFiGAN(nn.Module):
    def __init__(self, mel_channels=80, upsample_rates=[8, 8, 2, 2]):
        super().__init__()
        # 4 upsample blocks, total 256x to go from mel-rate to audio-rate
        ...
    def forward(self, mel):
        return self.blocks(mel)  # -> waveform
```

Formation: adversitaire (discriminateur sur les fenêtres courtes) + perte de reconstruction du spectrogramme méle + perte de correspondance des caractéristiques.`hifi-gan`repo ou nvidia-neMo.

> 訓練:对抗式(短窗口判别器) + Mel 频谱图重建损失 + 特征匹配损失──已商品化使用 `hifi-gan`Les résultats de la formation de l'équipe de formation de l'équipe de formation de l'équipe de formation de l'équipe de formation de l'équipe de formation de l'équipe de formation de l'équipe de formation de l'équipe de formation de l'équipe de formation de l'équipe de formation de l'équipe de formation de l'équipe de formation de l'équipe de formation de l'équipe de formation de l'équipe de formation de l'équipe de formation de l'équipe de formation de l'équipe de formation de formation de l'équipe de formation de l'équipe de formation de formation de l'équipe de formation de formation de l'équipe de formation de formation de l'équipe de formation de formation de l'équipe de formation de formation de l'équipe de formation de formation de l'équipe de formation de formation de formation de l'équipe de formation de formation de l'équipe de formation de formation de formation de l'équipe de formation de formation de formation de l'équipe de formation de formation de formation de l'équipe de formation de formation de formation de l'équipe de formation de formation de l'équipe de formation de formation de l'équipe de formation de formation de l'équipe de formation de formation de l'équipe de formation de l'équipe de formation de NVIDIA.

### Étape 5: l'ensemble du pipeline (pseudocode)

```python
text = "Please remind me at 6 pm."
phones = phonemize(text)
mel = acoustic_model(phones, speaker=alice)      # [T, 80]
wav = vocoder(mel)                                # [T * 256]
soundfile.write("out.wav", wav, 24000)
```

> **【中文解读】**Dans ce chapitre, nous allons montrer comment utiliser un cadre mature (comme PyTorch, HuggingFace, etc.) pour appliquer rapidement cette technique.





> **【拓展：语音与情感计算】**Le langage n'est pas seulement un moyen de transmettre des informations, il est également un moyen de transmettre des signaux émotionnels riches.

## Utilisez-le avec le cadre de réalisation

La pile de 2026:

> 2026:

| Situation | Pick |
|-----------|------|
| Real-time English voice assistant | Kokoro (CPU) or XTTS v2 (GPU) |
| Voice cloning from 5 s reference | F5-TTS |
| Commercial character voices | ElevenLabs v2.5 |
| Audiobook narration | ElevenLabs v2.5 or XTTS v2 + fine-tune |
| Low-resource language | Train VITS on 5–20 h target-lang data |
| Expressive / emotion tags | ElevenLabs v2.5 or StyleTTS 2 fine-tune |

| 场景 | 选择 |
|------|------|
| 实时英文语音助手 | Kokoro（CPU）或 XTTS v2（GPU） |
| 5 秒参考音频声音克隆 | F5-TTS |
| 商业角色声音 | ElevenLabs v2.5 |
| 有声书朗读 | ElevenLabs v2.5 或 XTTS v2 + 微调 |
| 低资源语言 | 在 5-20 小时目标语言数据上训练 VITS |
| 表达性 / 情感标签 | ElevenLabs v2.5 或 StyleTTS 2 微调 |

Leader de l' open source à partir de 2026: **F5-TTS for quality, Kokoro for efficiency**Ne touchez pas Tacotron à moins d'être historien.

> 2026: dirigeants ouverts**F5-TTS 追求质量，Kokoro 追求效率**À moins que vous ne soyez historien, ou bien utilisez Tacotron.



## Les pièges

> 常见陷

- **No text normalizer.**"Dr Smith" est "Doctor" ou "Drive"? "2026" est "vingt-vingt-six" ou "deux zéro deux six"?
  **没有文本归一化器。**"Dr Smith" 读成"Doctor"还是"Drive"?2026"读成"20266"还是"two zero two six"?在音素化之前归一化──
- **OOV proper nouns.**"Ghumare" → "ghyu-mair"? Envoyez un modèle de graphème à phonème pour des jetons inconnus.
  **OOV 专有名词。**"Ghumare" → "ghyu-mair"? Pour un signe inconnu 提供备用字素到音素模型──
- **Clipping.**Les résultats du vocoder sont rarement clips, mais l'incohérence de l'échelle de la mémoire à l'inférence peut dépasser ±1,0.`np.clip(wav, -1, 1)`- Je suis désolé .
  **削波。**音码器输出很少削波,但推理时 Mel 缩放不匹配可能超出 ±1.0──始终使用 `np.clip(wav, -1, 1)`Il y a une autre.
- **Sample-rate mismatch.**Kokoro produit 24 kHz; votre pipeline en aval s'attend à 16 kHz → à nouveau échantillonner ou à obtenir un aliasing.
  **采样率不匹配。**Kokoro 输出 24 kHz; votre downstream stream water line expectation 16 kHz →

> **【中文解读】**Cette section se concentre sur la façon de déployer le modèle en tant que produit disponible. De l'original au système de production, il faut considérer plusieurs dimensions de l'optimisation des performances, du traitement des erreurs, du contrôle, etc.


## Envoyez-le . Produit .

- Je ne sais pas .`outputs/skill-tts-designer.md`. Conception d'un pipeline TTS pour une voix, une latence et une langue cible données.

> 保存为 `outputs/skill-tts-designer.md`◊ Pour un son donné、延迟和语言目标设计 TTS 流水线──

## Les exercices

1. **Easy.**On court .`code/main.py`- Construit un dictionnaire phonémique à partir d'un vocabulaire jouet, estime la durée par phonème, et imprime un faux calendrier "mail".
   **简单。**运行  référencement`code/main.py`                                                                                                                                                                                                                                                              
2. **Medium.**Installez Kokoro, synthétisez la même phrase à la voix `af_bella`et `am_adam`- Comparer la durée de l'audio et la qualité subjective.
   **中等。**On est en train de faire un coup de pied.`af_bella`et `am_adam`音合成同一句话──比较音频时长和主观质量──
3. **Hard.**Enregistrez un clip de référence de 5 secondes de vous-même. Utilisez F5-TTS pour le cloner.
   **困难。**Récordée un passage de 5 secondes de son propre écoute de référence.

> **【中文解读】**Dans le tableau des termes, la définition du terme "ce que les gens disent" et "ce qu'il signifie réellement" est différenciée entre le langage quotidien et la signification technique précise.


## Les termes clés

| Term | What people say | What it actually means |
|------|-----------------|-----------------------|
| Phoneme | Sound unit | Abstract sound class; 39 in English (ARPABet). |
| Duration predictor | How long each phoneme lasts | Non-AR model output; integer frames per phoneme. |
| Vocoder | Mel → waveform | Neural net mapping mel-spec to raw samples. |
| HiFi-GAN | Standard vocoder | GAN-based; dominant 2020–2024. |
| MOS | Subjective quality | 1–5 mean opinion score from human raters. |
| SECS | Voice-clone metric | Cosine similarity between target and output speaker embedding. |
| F5-TTS | 2024 open-source SOTA | Flow-matching diffusion; zero-shot cloning. |
| Kokoro | CPU English leader | 82M-param model, Apache 2.0. |

| 术语 | 人们常说的 | 实际含义 |
|------|-----------|---------|
| 音素 | 声音单位 | 抽象声音类别；英文有 39 个（ARPABet）。 |
| 时长预测器 | 每个音素持续多久 | 非自回归模型输出；每个音素的整数帧数。 |
| 声码器 | Mel → 波形 | 将 mel 频谱映射为原始采样的神经网络。 |
| HiFi-GAN | 标准声码器 | 基于 GAN；2020-2024 年主导。 |
| MOS | 主观质量 | 人工评分员的 1-5 平均意见分。 |
| SECS | 声音克隆指标 | 目标与输出说话人嵌入之间的余弦相似度。 |
| F5-TTS | 2024 开源 SOTA | 流匹配扩散；零样本克隆。 |
| Kokoro | CPU 英文领导者 | 8200 万参数模型，Apache 2.0。 |

> **【中文解读】**延伸阅读 fournit des ressources de haute qualité pour l'apprentissage en profondeur. Ces articles et cours sont des références classiques dans ce domaine, adaptés aux lecteurs qui ont besoin d'une compréhension approfondie.


## Encore une lecture

- [Shen et al. (2017). Tacotron 2](https://arxiv.org/abs/1712.05884) la ligne de base de la séquence.
  Shen 等 (2017). Tacotron 2seq2seq 基线。
- [Kim, Kong, Son (2021). VITS](https://arxiv.org/abs/2106.06103) basé sur le flux de bout en bout.
  Kim, Kong, Son (2021). VITS端到端 Basée sur le modèle de flux.
- [Chen et al. (2024). F5-TTS](https://arxiv.org/abs/2410.06885) SOTA en source ouverte actuelle.
  Chen 等 (2024). F5-TTS当前开源SOTA──
- [Kong, Kim, Bae (2020). HiFi-GAN](https://arxiv.org/abs/2010.05646)Le vocoder qui se déploie encore en 2026.
  Kong, Kim, Bae (2020).
- [Kokoro-82M on HuggingFace](https://huggingface.co/hexgrad/Kokoro-82M) 2024 TTS anglais convivial pour les processeurs.
  Kokoro-82M 在 HuggingFace 上2024年 CPU 友好的英文 TTS。

> **【中文解读】**延伸阅读 a fourni des ressources de haute qualité pour l'apprentissage en profondeur, y compris des articles, des cours et des outils.

