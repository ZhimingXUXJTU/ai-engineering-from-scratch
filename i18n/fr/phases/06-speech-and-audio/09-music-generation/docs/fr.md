# La génération de musique  La génération de musique, l'audio stable, le Suno, et le séisme de licence  La génération de musique  La génération de musique  La génération de musique  La génération de musique  La génération de musique  La génération de musique  La génération de musique  La génération de musique  La génération de musique  La génération de musique  La génération de musique  La génération de musique  La génération de musique  La génération de musique  La génération de musique  La génération de musique  La génération de musique  La génération de musique  La génération de musique  La génération de musique  La génération de musique  La génération de musique  La génération de musique  La génération de musique  La génération de musique  La génération de musique  La génération de musique  La génération de musique 

> La génération de musique 2026: Suno v5 et Udio v4 dominent les affaires; MusicGen, Stable Audio Open et ACE-Step sont principalement open-source. Le problème technique est principalement résolu. Le problème juridique (Warner Music $ 500M règlement, UMG règlement) remodelée le domaine en 2025-2026.

> **【中文解读】**2026 années de musique génération:Suno v5 和 Udio v4 主导商业产品;MusicGen、Stable Audio Open 和 ACE-Step 领先开源;; problèmes techniques fondamentaux résolus, mais problèmes juridiques(Warner Music 5 milliards de dollars et règlement案) dans les années 2025-2026 réformé ce domaine;;

> **【拓展：AI 音乐的法律风暴】**Les questions de droits d'auteur sur l'IA produites par la musique ont provoqué un tremblement de terre dans l'industrie de la musique.

**Type:** Build | **类型:** 构建
**Languages:** Python | **语言:** Python
**Prerequisites:** Phase 6 · 02 (Spectrograms), Phase 4 · 10 (Diffusion Models) | **前置知识:** 阶段 6 · 02（频谱图），阶段 4 · 10（扩散模型）
**Time:** ~75 minutes | **预计用时:** ~75 分钟

## Le problème , l' introduction du problème

Text → un clip musical de 30 secondes à 4 minutes, avec paroles, voix et structure.

> 文本 → 30 secondes à 4 minutes de musique, avec des chansons, des voix et des structures.

> **【中文解读】**La question posée dans ce chapitre est la suivante: comment comprendre et appliquer correctement cette technique dans la conception pratique. Comprendre le contexte de la question aide à saisir les principaux facteurs de décision concernant le type de technologie. Dans les systèmes d'IA réels, le type de technique erroné coûte souvent plus cher que le coût de la mise en œuvre de détails.

1. **Instrumental generation.**Textes comme "lo-fi hip-hop drums avec des touches chaudes" → audio.
   **器乐生成。**Comme "la batterie hip-hop lo-fi avec des touches chaudes"
2. **Song generation (with vocals + lyrics).**"Cant country sur les nuits pluvieuses au Texas" → chanson complète.
   **歌曲生成（带人声+歌词）。**"Cant country sur les nuits pluvieuses au Texas" → 完整歌曲──Suno、Udio、YuE、ACE-Step──
3. **Conditional / controllable.**Extendre un clip existant, régénérer un pont, échanger le genre, séparer la tige ou la peinture.
   **条件/可控生成。**扩展现有片段、重新生成桥段、切换风格、分轨或内画──Udio's内画 + 分轨是2026年追赶的功能──

## Le concept de base.

> **【中文解读】**Le présent article présente les concepts et les bases théoriques de base. La connaissance de ces concepts est la prémisse de la réalisation de la réalisation de la réalisation, mais aussi le point de connaissance de l'interview et de la pratique de l'ingénierie.


![Music generation: token-LM vs diffusion, the 2026 model map](../assets/music-generation.svg)

### Les codes de codec neuraux

> ### LM de jeton basé sur le code

Les méta **MusicGen**(2023, MIT) et de nombreux dérivés: condition sur les emblèmes de texte/mélodie, prévoir autorégressivement les jetons EnCodec (32 kHz, 4 codebooks), décoder avec EnCodec. 300M - 3.3B paramètres.

> Meta **MusicGen**(2023, MIT) et de nombreux dérivés: en texte/旋律嵌入为条件, auto-retour prédiction EnCodec token(32 kHz,4 个码本), en utilisant EnCodec 解码──3 亿到33 亿参数──强基线; dépassant 30 秒效果下降──

**ACE-Step**(open source, 4B XL sorti en avril 2026) étend cela à la génération liricale à chansons complètes.

> **ACE-Step**(Open Source, 2026 4 mois de publication 40 milliards XL 版本) sera étendu à la production de tous les mots.

### Diffusion sur les fondements ou les latents

> ### basé sur la propagation des variables

**Stable Audio (2023)**et **Stable Audio Open (2024)**Il est excellent pour les boucles, la conception sonore, les textures ambiantes, pas très bien pour les chansons complètes structurées.

> **Stable Audio（2023）**et **Stable Audio Open（2024）**Le son est très bien structuré.

**AudioLDM / AudioLDM2**: texte à audio via diffusion latente de style T2I, généralisée à la musique, aux effets sonores, à la parole.

> **AudioLDM / AudioLDM2**Le contenu est généré par le T2I.

### Hybride (production)  Suno, Udio, Lyria

> ### 混合(生产)  Suno、Udio、Lyria

Poids fermé. Probablement le codec AR LM + vocodeur basé sur la diffusion avec des têtes de voix / tambour / mélodie spécialisées. Suno v5 (2026) est le leader de qualité ELO 1293. Udio v4 ajoute la peinture + séparation de tige (bass, tambour, voix séparées téléchargements).

> 闭源权重──可能是 AR 编解码 LM + 基于扩散的声码器,配有专门语音/鼓/旋律头──Suno v5(2026) est le leader de la qualité ELO 1293──Udio v4 增加内画 + 分轨(贝斯、鼓、人声分别下载)──

### Évaluation

> ###  évaluer

- **FAD (Fréchet Audio Distance).**Distance de niveau d'intégration entre la distribution audio générée et la distribution audio réelle à l'aide de fonctionnalités VGGish ou PANN. Moins est mieux. MusicGen petit: 4,5 FAD sur MusicCaps; SOTA ~ 3.0.
  **FAD（Fréchet 音频距离）。**Utilisation de VGGish ou de PANNs Trets de génération vs 真实音频分布的嵌入级距离──越低越好──MusicGen petit:MusicCaps 上 4.5 FAD;SOTA 约 3.0──
- **Musicality (subjective).**La préférence humaine.
  **音乐性（主观）。**Il est le premier à avoir été tué.
- **Text-audio alignment.**CLAP score entre le prompt et la sortie.
  **文本-音频对齐。**CLAP entre les points de pointe et les points de sortie
- **Musicality artifacts.**Des transitions hors rythme, une dérive vocal, une perte de structure après 30 secondes.
  **音乐性伪影。**跑拍过渡、人声短语漂移、 plus de 30 secondes après la perte de la structure。

> **【拓展：语音 AI 的产品化】**La technologie du langage est confrontée à des défis particuliers dans la fabrication de produits: différents sons, bruits de fond, prises de vue, nombreux discours, etc. Les produits de Siri, Alexa, et de petite enfance ont été largement optimisés pour résoudre ces "problèmes de longue durée".

> **【拓展：多语言语音技术】**Les caractéristiques du langage mondial sont énormes: la voix de la langue (en chinois comme en chinois) est à un niveau élevé, les ressources linguistiques sont faibles et les données de formation manquent.



## Carte modèle 2026

> 2026 année modèle

| Model | Params | Length | Vocals | License |
|-------|--------|--------|--------|---------|
| MusicGen-large | 3.3B | 30 s | no | MIT |
| Stable Audio Open | 1.2B | 47 s | no | Stability non-commercial |
| ACE-Step XL (Apr 2026) | 4B | > 2 min | yes | Apache-2.0 |
| YuE | 7B | > 2 min | yes, multilingual | Apache-2.0 |
| Suno v5 (closed) | ? | 4 min | yes, ELO 1293 | commercial |
| Udio v4 (closed) | ? | 4 min | yes + stems | commercial |
| Google Lyria 3 (closed) | ? | real-time | yes | commercial |
| MiniMax Music 2.5 | ? | 4 min | yes | commercial API |

| 模型 | 参数量 | 时长 | 人声 | 许可 |
|------|--------|------|------|------|
| MusicGen-large | 33 亿 | 30 秒 | 无 | MIT |
| Stable Audio Open | 12 亿 | 47 秒 | 无 | Stability 非商业 |
| ACE-Step XL（2026.04） | 40 亿 | > 2 分钟 | 有 | Apache-2.0 |
| YuE | 70 亿 | > 2 分钟 | 有，多语言 | Apache-2.0 |
| Suno v5（闭源） | ? | 4 分钟 | 有，ELO 1293 | 商业 |
| Udio v4（闭源） | ? | 4 分钟 | 有 + 分轨 | 商业 |
| Google Lyria 3（闭源） | ? | 实时 | 有 | 商业 |
| MiniMax Music 2.5 | ? | 4 分钟 | 有 | 商业 API |

## Le paysage juridique (2025-2026)

> ## 法律环境(2025-2026)

- **Warner Music vs Suno settlement.**500 millions de dollars. WMG a maintenant la supervision de l'intelligence artificielle, des droits de musique et des pistes générées par l'utilisateur sur Suno.
  **Warner Music 诉 Suno 和解。**5 milliards de dollars. WMG a maintenant le droit de contrôler la similarité de l'IA de Suno.
- **EU AI Act**+ **California SB 942**: La musique générée par l'IA doit être divulguée.
  **EU AI 法案**+ **加利福尼亚 SB 942**Il faut le dévoiler.
- **Riffusion / MusicGen**Les membres du groupe ne sont pas des professionnels de la musique.
  **Riffusion / MusicGen**Il n'y a pas de charge de conformité sous licence MIT, mais il n'y a pas de voix de commerçant.

Modèles de sécurité pour le navire:

> Mode de mise en ligne:

1. Générer uniquement des instruments (MusicGen, Stable Audio Open, sorties MIT/CC0).
   仅生成器乐(MusicGen、Stable Audio Open、MIT/CC0 输出)
2. Utilisez des API commerciales (Suno, Udio, ElevenLabs Music) avec une licence par génération.
   Utilisation avec chaque génération de permis de l'API commerciale (Suno, Audio, ElevenLabs Music)
3. Le train sur le catalogue de propriété ou de licence (la plupart des entreprises finissent ici).
   Dans le cadre de la formation en auto-autorisation, la plupart des entreprises ont finalement atteint cet objectif.
4. Étiquettez les générations avec des balises d'eau + métadonnées.
   Uzd水印 + 元数据标记生成内容──

> **【中文解读】**Cette méthode "de zéro" peut aider à comprendre le principe derrière le cadre, en cas de problème, ne sera pas bloqué dans une boîte noire.


## Construisez-le et mettez-le en œuvre.
```figure
sp-codec-tokens
```

## Faites-le

### Étape 1: générer avec MusicGen

```python
from audiocraft.models import MusicGen
import torchaudio

model = MusicGen.get_pretrained("facebook/musicgen-small")
model.set_generation_params(duration=10)
wav = model.generate(["upbeat synthwave with driving drums, 128 BPM"])
torchaudio.save("out.wav", wav[0].cpu(), 32000)
```

Trois tailles: `small`(300 M, rapide),`medium`Le rapport de la Commission`large`(3.3B) Le petit suffit pour "faire tomber l'idée".

> Il y a trois petits.`small`- Je suis en train de me lancer.`medium`15 milliards de personnes`large`Il est également important de prendre en compte les besoins de la population.`small`L'idée de "pourquoi faire preuve de courage"

### Étape 2: conditionnement de la mélodie

```python
melody, sr = torchaudio.load("humming.wav")
wav = model.generate_with_chroma(
    ["jazz piano cover"],
    melody.squeeze(),
    sr,
)
```

MusicGen-melody prend un chromagramme et préserve la mélodie tout en échangeant le timbre.

> Musique Gen-melodie  accepter un tableau et en échange de sonores lorsqu'il conserve une mélodie。

### Étape 3: évaluation du FAD

```python
from frechet_audio_distance import FrechetAudioDistance
fad = FrechetAudioDistance()

fad.get_fad_score("generated_folder/", "reference_folder/")
```

Compute la distance de VGGish. Utilisée pour les tests de régression au niveau du genre; pas un substitut pour les auditeurs humains.

> 計算 VGGish 嵌入距離── s'applique au cours de la période de réintégration; ne peut remplacer l'audience humaine──

### Étape 4: ajouter au flux de travail de la maîtrise en musique

Combinez avec les idées de l'étude 7-8:

> **【中文解读】**Dans ce chapitre, nous allons montrer comment utiliser un cadre mature (comme PyTorch, HuggingFace, etc.) pour appliquer rapidement cette technique.


```python
prompt = "Write a 30-second jazz loop. Describe the drums, bass, and piano voicing."
description = llm.complete(prompt)
music = musicgen.generate([description], duration=30)
```




> **【拓展：语音与情感计算】**Le langage n'est pas seulement un moyen de transmettre des informations, il est également un moyen de transmettre des signaux émotionnels riches.

## Utilisez-le avec le cadre de réalisation

| Goal | Stack |
|------|-------|
| Instrumental sound design | Stable Audio Open |
| Game / adaptive music | Google Lyria RealTime (closed) |
| Full songs with vocals (commercial) | Suno v5 or Udio v4 with explicit license |
| Full songs with vocals (open) | ACE-Step XL or YuE |
| Short ad jingle | MusicGen melody-conditioned on a hummed reference |
| Music-video background | MusicGen + Stable Video Diffusion |

| 目标 | 技术栈 |
|------|--------|
| 器乐声音设计 | Stable Audio Open |
| 游戏/自适应音乐 | Google Lyria RealTime（闭源） |
| 带人声的完整歌曲（商业） | Suno v5 或 Udio v4 带明确许可 |
| 带人声的完整歌曲（开源） | ACE-Step XL 或 YuE |
| 短广告曲 | MusicGen 在哼唱参考上的旋律条件 |
| 音乐视频背景 | MusicGen + Stable Video Diffusion |



## Des pièges qui vont encore arriver en 2026

> 2026 est toujours en train de tomber

- **Copyright-laundering prompts.**"Cant dans le style de Taylor Swift"  commercial Suno / Audio filtrer ces maintenant, les modèles ouverts ne. Ajoutez votre propre liste de filtres.
  **版权洗钱提示。**"C'est une chanson au style de Taylor Swift"
- **Repetition / drift past 30 s.**Modèles AR boucle. croiser plusieurs générations, ou utiliser ACE-Step pour la cohérence structurelle.
  **超过 30 秒的重复/漂移。**AR 模型会循环──交叉淡进多个生成,或使用 ACE-Step 保持结构一致性──
- **Tempo drift.**Les modèles se détournent du BPM. Utilisez les balises BPM dans le prompt et le post-filtre avec librosa's `beat_track`- Je suis désolé .
  **节奏漂移。**模型偏离 BPM──在提示中使用 BPM 标签并使用图书馆 的 `beat_track`Je suis en train de vous dire:
- **Vocal intelligibility.**Le Suno est excellent; les modèles ouverts sont souvent mal à l'aise avec les mots.
  **人声清晰度。**Suno 表现出色; open source模型的歌词经常模糊──如果歌词重要,使用商业API或微调──
- **Mono output.**Les modèles ouverts génèrent des stéréos mono ou faux.
  **单声道输出。**Open source Modèle générer un seul son ou un faux son.

> **【中文解读】**Cette section se concentre sur la façon de déployer le modèle en tant que produit disponible. De l'original au système de production, il faut considérer plusieurs dimensions de l'optimisation des performances, du traitement des erreurs, du contrôle, etc.


## Envoyez-le . Produit .

- Je ne sais pas .`outputs/skill-music-designer.md`. Choisir le modèle, la stratégie de licence, la longueur / plan de structure et les métadonnées de divulgation pour un déploiement de génération de musique.

> 保存为 `outputs/skill-music-designer.md` Pour la production de musique, le déploiement de choix de modèle, de stratégie de licence, de longueur/de structure et de données de communication.

## Les exercices

1. **Easy.**On court .`code/main.py`Il produit une progression d'accord "générative" + un motif de batterie comme symboles ASCII  un dessin animé de génération musicale.
   **简单。**运行  référencement`code/main.py`Il est utilisé pour la production de caractères ASCII et pour la production de chords.
2. **Medium.**Installez`audiocraft`, générer des clips de 10 secondes sur 4 genres avec MusicGen-small, mesurer FAD contre un ensemble de genres de référence.
   **中等。**Montage`audiocraft`, avec MusicGen-small dans 4 流派提示上生成10秒片段,对照参考流派集测量 FAD──
3. **Hard.**En utilisant ACE-Step (ou MusicGen-melody), générez trois variations de la même mélodie avec des commandes de timbre différentes.
   **困难。**Utilisation de l'ACE-Step (ou de la musique générée par la mélodie), avec différents sons de la musique, pour produire les trois variantes de la même mélodie.

> **【中文解读】**Dans le tableau des termes, la définition du terme "ce que les gens disent" et "ce qu'il signifie réellement" est différenciée entre le langage quotidien et la signification technique précise.


## Les termes clés

| Term | What people say | What it actually means |
|------|-----------------|-----------------------|
| FAD | Audio FID | Fréchet distance between embedding distributions of real vs generated. |
| Chromagram | Melody as pitches | 12-dim per-frame vector; input to melody conditioning. |
| Stems | Instrument tracks | Separated bass / drums / vocals / melody as WAV. |
| Inpainting | Regen a section | Mask a time window; model regenerates just that. |
| CLAP | Text-audio CLIP | Contrastive audio-text embedding; eval text-audio alignment. |
| EnCodec | Music codec | Meta's neural codec used by MusicGen; 32 kHz, 4 codebooks. |

| 术语 | 人们常说的 | 实际含义 |
|------|-----------|---------|
| FAD | 音频 FID | 真实 vs 生成嵌入分布之间的 Fréchet 距离。 |
| 色度图 | 旋律即音高 | 12 维逐帧向量；旋律条件的输入。 |
| 分轨 | 乐器轨道 | 分离的贝斯/鼓/人声/旋律 WAV。 |
| 内画 | 重生成一段 | 遮蔽时间窗口；模型只重生成那部分。 |
| CLAP | 文本-音频 CLIP | 对比音频-文本嵌入；评估文本-音频对齐。 |
| EnCodec | 音乐编解码器 | Meta 的神经编解码器，MusicGen 使用；32 kHz，4 个码本。 |

> **【中文解读】**延伸阅读 fournit des ressources de haute qualité pour l'apprentissage en profondeur. Ces articles et cours sont des références classiques dans ce domaine, adaptés aux lecteurs qui ont besoin d'une compréhension approfondie.


## Encore une lecture

- [Copet et al. (2023). MusicGen](https://arxiv.org/abs/2306.05284) l'indice de référence autorégressif ouvert.
  Le groupe de musique est en train de se lancer dans la musique.
- [Evans et al. (2024). Stable Audio Open](https://arxiv.org/abs/2407.14358) la conception sonore par défaut.
  Evans et autres (2024).
- [ACE-Step](https://github.com/ace-step/ACE-Step) ouverture 4B générateur de chansons complète, avril 2026.
  ACE-Step开源 40 亿参数全曲生成器,2026 年 4 月。
- [Suno v5 platform docs](https://suno.com) le leader de la qualité commerciale.
  Suno v5 商业质量领先者──
- [AudioLDM2](https://arxiv.org/abs/2308.05734) diffusion latente pour la musique + effets sonores.
  AudioLDM2音乐 + 音效的潜变量扩散──
- [WMG-Suno settlement coverage](https://www.musicbusinessworldwide.com/suno-warner-music-settlement/) Novembre 2025 précédent.
  Le WMG-Suno 和解报道2025 年 11 月判例──

> **【中文解读】**延伸阅读 a fourni des ressources de haute qualité pour l'apprentissage en profondeur, y compris des articles, des cours et des outils.

