# Modèles audio-langue: le sourire à l'audio flamingo 3 arc

> Whisper (Radford et coll., décembre 2022) a réglé la reconnaissance vocale  680 000 heures de discours multilingue mal supervisé, un simple transformateur de codeur-décodeur, une référence qui a fait que chaque version ASR ultérieure le cite. Mais reconnaître n'est pas raisonner. Pour demander "quels instruments sont dans cet enregistrement" ou "quels sentiments l'orateur exprime" ou "qu'est-il arrivé à la 3e minute", il faut comprendre l'audio, pas la transcription. Qwen-Audio, SALMONN, LTU et Audio Flamingo 3 de NVIDIA (AF3, juillet 2025) ont progressivement construit cette pile: garder les encoders de la classe Whisper, boulonner les Q-formateurs, former les données d'instruction audio-textuelle, ajouter le raisonnement de la chaîne de pensée. Cette leçon est à l'honneur.

> **【中文解读】**Le son de la musique a été développé en tant que logiciel de communication audio et audio. Le son de la musique a été développé en tant que logiciel de communication audio et audio.

**Type:** Build
**Languages:** Python (stdlib, log-Mel spectrogram + audio Q-former skeleton)
**Prerequisites:** Phase 6 (Speech and Audio), Phase 12 · 03 (Q-Former)
**Time:** ~180 minutes

>  **【前置】**Pour les autres, il est nécessaire de prendre en compte la phase 6 du programme.
>  **【类比】**音频 LLM = "pour LLM 装耳朵"。Whisper = 助听器(只能转录不能思考); SALMONN = 聋学校的翻译员(Whisper 转录→LLM 思考);AF3 = 直接给 LLM 装耳(端到端听+想+答)。端到端的好处:能捕捉转录丢失信息(语调、情绪、停顿), voilà les clés de la théorie。

## Objectifs d'apprentissage

- Comptez un spectrogramme log-Mel à partir d'une forme d'onde: fenêtre, FFT, banques de filtres, transformation de journaux.
  Le nombre de changements est le même que celui de la fréquence de calcul.
- Comparez les options d'encodeur: encodeur à sourciller, BEATs, hybride AF-Whisper.
  Le mot "souple" est le mot de passe de la phrase "souple" dans le mot "souple".
- Construire un Q-former audio: N requêtes apprenables en répondant aux patchs spectrogrammes.
  Le texte de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la
- Expliquer la formation en cascade (Whisper-then-LLM) par rapport à l'entraînement audio-LLM de bout en bout: pourquoi l'entraînement de bout en bout est mieux adapté au raisonnement.
  Le programme de formation de l'équipe de formation de l'équipe de formation de l'équipe de formation de l'équipe de formation de l'équipe de formation de l'équipe de formation de l'équipe de formation de l'équipe de formation de l'équipe de formation de l'équipe de formation de l'équipe de formation de l'équipe de formation de l'équipe de formation de l'équipe de formation de l'équipe de formation de l'équipe de formation de l'équipe de formation de l'équipe de formation de l'équipe de formation de l'équipe de formation de l'équipe de formation de l'équipe de formation de l'équipe de formation de l'équipe de formation de formation de l'équipe de formation de formation de l'équipe de formation de formation de l'équipe de formation de formation de l'équipe de formation de formation de l'équipe de formation de formation de l'équipe de formation de formation de l'équipe de formation de formation de l'équipe de formation de formation de l'équipe de formation de formation de l'équipe de formation de formation de formation de l'équipe de formation de formation de l'équipe de formation de formation de l'équipe de formation de formation de l'équipe de formation de formation de l'équipe de formation de formation de l'équipe de formation de formation de l'équipe de formation de l'équipe de formation de l'équipe de formation de l'équipe de formation de formation de l'équipe de l'équipe de formation de formation de formation de l'équipe de formation de l'équipe de formation de l'équipe de l'équipe de formation de l'équipe de l'équipe de formation de l'équipe de formation de l'équipe de formation de l'équipe de l'équipe de formation de l'équipe de formation de l'équipe de l'équipe de la formation de l'équipe de la formation de la formation de la formation de la formation de la formation.

## Le problème , l' introduction du problème

La reconnaissance de la parole a été résolue par Whisper. OCR-of-audio est une marchandise. Mais "commodity" s'arrête à la transcription. Si le modèle ne peut pas raisonner sur ce qu'il a entendu  timing, haut-parleurs, émotion, structure musicale, sons environnementaux  transcription seule ne peut pas conduire les caractéristiques du produit.

> 语音识别 has been Whisper 解决──音频 OCR 已成为基础能力──但"基础能力" est arrêté de se transférer──如果模型无法推理时间、说话人、情绪、音乐结构、环境声仅靠转录无法驱动产品功能──

Trois itinéraires évidents:

> 3° Le chemin du retour

1. Cascade: Whisper transcrit, LLM raisonne sur la transcription. Fonctionne pour les scénarios de langage pur. Échecs pour la musique, l'audio environnemental, le chevauchement multi-speakers, l'émotion.
   Le texte de la traduction de la langue française est en français.

2. Audio-LLM de bout en bout: un encodeur audio alimente les jetons audio directement dans un LLM, en évitant la transcription. Préserve les informations acoustiques (émotion, haut-parleur, environnement).
   Le code de la musique est un code de la musique, qui est un code de la musique.

3. Hybride: encodeur audio + décodeur de texte qui peut à la fois transcrire et raisonner.
   Le système de programmation est un système de programmation de programmation de programmation de programmation de programmation de programmation de programmation de programmation de programmation de programmation de programmation de programmation de programmation de programmation de programmation de programmation de programmation de programmation de programmation de programmation de programmation de programmation de programmation de programmation de programmation de programmation de programmation de programmation de programmation de programmation de programmation de programmation de programmation de programmation de programmation de programmation de programmation de programmation de programmation de programmation de programmation de programmation de programmation de programmation de programmation de programmation de programmation de programmation de programmation de programmation de programmation de programmation de programmation de programmation de programmation de programmation de programmation de programmation de programmation de programmation de programmation de programmation de programmation de programmation de programmation de programmation de programmation de programmation de programmation de programmation de programmation de programmation de programmation de programmation de programmation de programmation de programmation de programmation de programmation de programmation de programmation de programmation de programmation de programmation de programmation de programmation de programmation de programmation de programmation de programmation de programmation de programmation de programmation de programmation de programmation de programmation de programmation de programmation de programmation de programmation de programmation de programmation de programmation de programmation de programmation de programmation de programmation de programmation de programmation de programmation de programmation de programmation de programmation de programmation de programmation de programmation de programmation de programmation de programmation de programmation de programmation de programmation de programmation de programmation de programmation de programmation de programmation de programmation de programmation de programmation de programmation de programmation de programmation de programmation de programmation de programmation de programmation de programmation de programmation de programmation de programmation de programmation de programmation de programmation de programmation de programmation de programmation de programmation de programmation de programmation de programmation de programmation de programmation de programmation de programmation de programmation de programmation de programmation de programmation de programmation de programmation de programmation de programmation de programmation de programmation de programmation de programmation de

## Le concept de base.

> **【中文解读】**Le modèle de la langue est basé sur le modèle de la langue. La nouvelle génération de modèles ne peut pas seulement transcrire, mais aussi comprendre le contenu de la musique.

> **【拓展：语音 AI 的前沿**Whisper-large-v3  support environ 100 种语言的语音识别──2024-2025 趋势是语音大模型:GPT-4o 原生语音输入输出(延迟约 320ms),Gemini 的实时语音对话,ElevenLabs 的语音克隆──AudioFlamingo 在音频理解任务上达到SOTA,能回答关于音乐和声音的复杂问题──


### Spectrogramme log-mel: la fonction d'entrée

Chaque encodeur audio commence par la même fonctionnalité: un spectrogramme log-Mel.

> Chaque éditeur de fréquences est basé sur les mêmes caractéristiques.

1. Remplacer à 16 kHz.
   Le nombre de fréquences est de 16 kHz.
2. Transformation Fourier à court terme avec des fenêtres de 25 ms, saut de 10 ms.
   Le temps de la réaction est de 25ms.
3. Prenez l'ampleur du résultat de la FFT.
   Le résultat de la recherche est le résultat de la recherche.
4. Appliquer des bancs de filtres Mel (habituellement 80 filtres à intervalles logs de 0 à 8000 Hz) pour déformer la fréquence perceptuelle.
   L'application Mel 波器组 (habituellement 80 个波器, à intervalles de 0 à 8000 Hz) est réalisée à la fréquence de perception.
5. Compresseur de log (log(1 + x)) pour la plage dynamique.
   Le nombre de personnes qui ont été affectées à l'activité de l'entreprise est de 0,5% à 0,5% en moyenne.

Résultat: un tableau en 2D de forme (T, 80) où T est le nombre de cadres temporels. Pour un clip de 30 secondes à la fréquence d'image de 100 Hz: (3000, 80).

> 结果:形状为 (T, 80) de 2D 数组, dont T est le temps数──30 秒片段在 100 Hz 率下:(3000, 80)──

### Le codeur de Whisper

Le codeur de Whisper est un transformateur de style ViT de 12 couches qui traite le spectrogramme log-Mel comme une séquence de cadres temporels.

> Whisper's编码器 est un transformateur de 12 niveaux ViT 风格, qui sera log-Mel 频谱图作为时间序列处理――输出:

Pour ASR, le décodeur de Whisper est un transformateur d'attention croisée qui génère des jetons de texte conditionnés sur la sortie de l'encodeur.

> Pour ASR, Whisper's de codeur est un transformateur de concentration de référence, selon le codeur输出生成文本代币──标准编码器-解码器──

Pour les ALM (audio-LLM), vous voulez que le codeur soit utilisé comme entrée dans un autre LLM. Le modèle: encodeur à sourcillement gelé, Q-former entraîneable, LLM gelé ou réglé.

> Pour ALM, il faut un codeur pour faire une autre mise en mode.

### Les encoders BEAT et audio spécifiques

Whisper a été formé sur des données dominantes par la parole.

> Sous-pard dans les données de la formation de la voix dominée.

BEATs (Chen et coll., 2022) est un transformateur auto-supervisé formé sur AudioSet. Capture la musique et les sons environnementaux mieux que Whisper au même nombre de paramètres.

> BEATs(Chen 等人,2022) est un transformateur auto-surveillant de l'AudioSet.

AF-Whisper (hybride d'Audio Flamingo 3): Whisper + BEATs est le signal audio de l'audio.

> AF-Whisper(Audio Flamingo 3 的混合方案):拼音 Whisper + BEATs 特征作为音频输入──Whisper 携带语言信号,BEATs 携带声学信号──

### Le Q-former audio

Le même schéma que le Q-former visuel de BLIP-2. un nombre fixe de requêtes apprenables (souvent 32 ou 64) se croisent sur les cadres de sortie de l'encodeur audio.

> La même méthode que BLIP-2 Q-former.

Étapes d'alignement de formation: Q-former seul, perte de contraste + sous-titres sur les paires audio-textuelles (AudioCaps, Clotho).

> 訓練對齐阶段:仅 Q-former,音频-文本对上对比+描述损失(AudioCaps、Clotho) 』 instruction阶段:端到端,解 LLM,在指令数据上训练──

### Le arc  SALMONN, Qwen-Audio, AF3

SALMONN (Tang et coll., 2023): Whisper + BEATs + Q-former + LLaMA. Le premier audio-LLM ouvert avec une capacité de raisonnement sérieuse.

> SALMONN(Tang 等人,2023):Susper + BEATs + Q-former + LLaMA。

Qwen-Audio (Chu et coll., 2023): architecture similaire, formée sur un ensemble de données plus riche, réglée pour le dialogue multi-tours. MMAU ~ 0,60.

> Qwen-Audio Chu 等人,2023): similaire architecture, dans un ensemble de données plus riche, pour une optimisation de dialogue en plusieurs rounds.

LTU  Écoutez, pensez, comprenez (Gong et coll., 2023): données explicites de raisonnement, se concentrent sur la chaîne de pensée sur les clips audio.

> LTU 听、想、理解(Gong 等人,2023): données de raisonnement explicite, consacrée à la pensée en chaîne sur les épisodes audio.

Audio Flamingo 3 (Goel et coll., juillet 2025): le SOTA ouvert en cours. 8B LLM spine dorsale (Qwen2 7B), Whisper-grand encodeur concat BEATs, 64 requêtes Q-former, formation sur 1M + paires d'instructions audio-texte. MMAU 0.72, correspond à la frontière propriétaire sur certaines sous-tasques.

> Audio Flamingo 3(Goel 等人,2025年7月):当前开放 SOTA──8B LLM 主干(Qwen2 7B),Whisper-large 编码器拼接 BEATs,64 查询 Q-former,在100万+音频-文本指令对上训练──MMAU 0.72,在某些子任务上匹配闭源前沿──

AF3 introduit également une chaîne de pensée sur demande pour l'audio: le modèle peut émettre optionnellement des jetons de pensée ("laissez-moi d'abord identifier les instruments: ...") avant la réponse finale.

> AF3 introduit également un système de pensée à la demande: le modèle peut être utilisé dans la réponse finale avant sélection et produire des jetons de pensée avant de commencer à réfléchir.

### Cascade contre bout à bout

L'équipement de transport en cascade:

> Le système de gestion des ressources humaines

1. Whisper transcrit le texte audio → texte.
   Le son est en train de se transformer en textes.
2. Les raisons de la maîtrise de la loi sur le texte.
   Le texte est en cours de révision.

Il fonctionne parfaitement pour "récapituler ce podcast".
- "Quelle est l'humeur de cette chanson?"  L'humeur est dans le son, pas les mots.
- "Qui parle, Alice ou Bob?"  nécessite l'identification de l'orateur.
- "A quelle seconde l'explosion se produit-elle ?"
- "Est-ce que c'est réel ou une source audio?"  La détection de faux profonds a besoin de fonctionnalités acoustiques.

> Pour "总结这个播客" parfaitement adapté... mais dans les scénarios suivants:
> - "Qu'est-ce que cette chanson évoque ?"
> - " Qui est en train de parler, Alice ou Bob ? "
> - " Explosion en quelques secondes ? "
> - "Est-ce que c'est vrai ou généré ?"

Le Qwen-Audio et l'AF3 gèrent la musique, l'environnement et les émotions de manière native.

> 端到端保留声学信号──Qwen-Audio 和 AF3 原生处理音乐、环境和情绪──

> **【中文解读】**级联管道 (LLM) est adapté à des situations de langage purement audio comme un résumé de la série, mais ne peut pas gérer les émotions musicales, les conversations, la reconnaissance de personnes, le temps de mise en place, la falsification de données, etc. nécessitent des caractéristiques sonores.

> **【拓展：金融场景的音频理解】**Dans le domaine financier, la compréhension audio peut être utilisée: analyse émotionnelle des réunions de finance, non seulement pour les enregistrements de texte, mais aussi pour les échanges de voix et de voix, reconnaissance des commandes de voix des opérateurs, contrôle de la qualité des clients, analyse émotionnelle des conversations de conférences, séparation de personnes, ou communication de la classe de communication.

### Récipes de production 2026

Pour un nouveau produit audio-compréhensible:

> 对于新音频理解产品:

- Cascade si: la transcription est le but, pas de musique, pas d'inférence émotionnelle.
  Si l'objectif est de transformer, pas de musique, pas besoin de sentiment de conclusion.
- AF3 / Qwen-Audio-famille si: musique, émotion, haut-parleur, ou raisonnement audio complexe.
  La série de Qwen-Audio: If there is music、情绪、多人说话或复杂音频推理── est une série de films en direct réalisés par le groupe de musique.

Le cascade est moins cher et plus simple.

> Le niveau de la communication est plus facile, plus simple, plus fort.

### MMAU  le critère de référence de la raisonnement audio

MMAU (Massive Multimodal Audio Understanding) est le critère de référence pour le raisonnement audio de 2024 à 2025:

> MMAU (en anglais: MMAU) est un programme de communication de la population en ligne pour les années 2024-2025.

- 10 000 couples de QA audio-textuels à travers la parole, la musique, les sons environnementaux.
  Le texte de la première partie de la série est le texte de la première partie de la série.
- Il couvre la classification, le raisonnement temporel, le raisonnement causale, l'AQ à durée indéterminée.
  Le temps de la réflexion, l'effet de la réflexion ouverte.
- Tests de ce que les pipelines en cascade manquent systématiquement.
  Le contenu de la mise en œuvre de la méthode de gestion de la gestion des émissions de gaz

L'écart est plus petit que le delta ouvert versus fermé de VideoMME, ce qui indique que les LLM audio sont en train de mûrir.

> 开源 SOTA(AF3) 0.72;闭源前沿约0.78(Gemini 2.5 Pro、Claude Opus 4.7)。差距小于VideoMME 的开源-闭源差距,说明音频 LLM 正在成熟──

## Utilisez-le avec le cadre de réalisation
```figure
audio-text-ctc
```

## Utilisez-le

`code/main.py`- Le numéro de la liste:

- Implémentation de calcul de spectrogramme log-Mel dans stdlib: fenêtre, DFT naïf, filtre-banque Mel.
  Le code de référence est le code de référence de la carte de référence.
- Audio Q-ancien squelette: donné encodeur cadres de sortie, calculer Q, K, V, attention, et émettre N jetons.
  Le code de l'écriture est un code de l'écriture.
- Comparaison cascade contre bout à bout sur une tâche de jouet.
  Traduction anglaise: en jouet, en jeu, en jeu.

## Envoyez-le . Produit .

Cette leçon produit `outputs/skill-audio-llm-pipeline-picker.md`. En raison d'une tâche audio (transcription, marquage de musique, inférence des émotions, diarisation multi-enceintes, classification de l'environnement), il choisit en cascade, AF3 de bout en bout ou un hybride.

> 本课产 出 `outputs/skill-audio-llm-pipeline-picker.md`◊ donner une tâche de fréquence fixe ([[转录、音乐标注、情绪推断、多人说话分离、环境分类), elle choisit le niveau de connexion 端到端 AF3 或混合方案。

## Les exercices

1. Compute la dimension du spectrogramme log-Mel pour un clip de 30 secondes à 16 kHz, une fenêtre de 25 ms, un saut de 10 ms, 80 bins Mel. Comment cela change-t-il à 48 kHz?

2. Pourquoi Whisper ne joue pas bien dans la musique? Quelles fonctionnalités audio les BEAT captent que Whisper ne fait pas? Pourquoi Whisper ne joue pas bien dans la musique?

3. Audio Q-former avec 64 requêtes contre 32: à quelle complexité de tâche 64 paie-t-il? 32 sauvegarder le calcul pour quoi? 64 查询 contre 32 查询的 Audio Q-former:在什么任务复杂度下 64 更值得?32 节省了什么计算?

4. Lisez la section 4 de l'AF3 sur la pensée à la demande. Proposez trois tâches audio où la chaîne de pensée est la plus utile.

5. Comment signer les changements de haut-parleur ? Utilisez AF3 输出实现一个最小的说话人分离管道。如何标记说话人切换?

## Les termes clés

| Term | What people say | What it actually means | 中文释义 |
|------|-----------------|------------------------|---------|
| Log-Mel spectrogram | "Mel features" Mel 频谱 | 2D (time, frequency) array of log-magnitude values after Mel filter banks 经 Mel 滤波器组后的对数幅度二维数组 | |
| Audio Q-former | "Audio Perceiver" 音频感知器 | Cross-attention bottleneck from audio encoder output to fixed-length queries feeding the LLM 音频编码器输出到固定长度查询的交叉注意力瓶颈 | |
| Cascaded | "ASR-then-LLM" 级联管道 | Pipeline where Whisper transcribes and a text LLM reasons; loses acoustic information Whisper 转录后文本 LLM 推理的管道；丢失声学信息 | |
| End-to-end | "Audio-LLM" 端到端音频 LLM | Audio features enter the LLM directly via Q-former; preserves acoustic signal 音频特征通过 Q-former 直接进入 LLM；保留声学信号 | |
| BEATs | "Audio AudioSet encoder" 音频自监督编码器 | SSL transformer trained on AudioSet; strong on music + environmental sounds 在 AudioSet 上训练的自监督 Transformer；擅长音乐和环境声 | |
| MMAU | "Audio reasoning bench" 音频推理基准 | 10k QA pairs across speech, music, environment; 2024 eval standard 跨语音、音乐、环境的 1 万条 QA；2024 年评估标准 | |
| On-demand thinking | "Audio CoT" 按需音频思考 | Model can optionally emit reasoning tokens before final answer, lifts accuracy 3-5 pts 模型可在最终回答前输出推理 token，提升准确率 3-5 个百分点 | |

## Encore une lecture

- [Radford et al. — Whisper (arXiv:2212.04356)](https://arxiv.org/abs/2212.04356)
- [Chu et al. — Qwen-Audio (arXiv:2311.07919)](https://arxiv.org/abs/2311.07919)
- [Goel et al. — Audio Flamingo 3 (arXiv:2507.08128)](https://arxiv.org/abs/2507.08128)
- [Tang et al. — SALMONN (arXiv:2310.13289)](https://arxiv.org/abs/2310.13289)
- [Gong et al. — LTU (arXiv:2305.10790)](https://arxiv.org/abs/2305.10790)
