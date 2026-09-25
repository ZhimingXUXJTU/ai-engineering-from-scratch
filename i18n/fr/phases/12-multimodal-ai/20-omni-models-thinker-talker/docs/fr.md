# Modèles omni: Qwen2.5 Omni et le penseur-parleur séparé

> La démo de produit de GPT-4o en mai 2024 a été perturbateur non pas à cause du modèle sous-jacent mais à cause de la forme du produit  une interface vocale où vous parlez, le modèle voit ce que voit la caméra, et il parle en moins de 250 ms. L'écosystème ouvert a passé le reste de 2024 et 2025 à courir pour atteindre cette surface de produit. Qwen2.5 Omni (mars 2025) est la conception ouverte de référence: un Thinker (grand transformateur générateur de texte) plus un Talker (transformateur générateur de parole parallèle), relié par des jetons de parole en streaming. Mini-Omni l'a simplifié, Moshi a correspondu à sa latence, GLM-4-Voice l'a étendu au chinois. Cette leçon explique l'architecture Thinker-Talker et le budget de latence qui permet de diffuser en temps réel le dialogue.

> **【中文解读】**La rupture de GPT-4o ne se situe pas dans le modèle de base, mais dans l'expérience de communication de voix dans le format de produit250ms ⋅ Qwen2.5-Omni est une référence mondiale:Thinker(massive text text text generating Transformer) responsable de la conception de " quoi dire ",Talker(small voice generating Transformer) responsable de la production de tokens de voix── les deux sont utilisés par le biais de tokens de connexion, réaliser des conversations réelles──

**Type:** Build
**Languages:** Python (stdlib, streaming pipeline latency simulator + VAD loop)
**Prerequisites:** Phase 12 · 19 (audio-LLMs), Phase 12 · 16 (any-to-any)
**Time:** ~180 minutes

>  **【前置】**Il est également possible de faire une analyse de la situation de la situation de l'entreprise.
>  **【类比】**Le penseur-parleur 架构 = "翻译员 + 同传播音员"。其他 omni 模型 = 一个人又要思考又要说话(串行,慢);Qwen2.5-Omni = Penseur(大脑,想"说什么")+ Parleur(嘴巴,把文字变语音)并行工作。Penseur 流式吐出文本代币,Talker 一边接收一边合成语音,用户听到的是流水线输出,总延迟大幅降低。

## Objectifs d'apprentissage

- Divisez le pipeline d'inférence en Thinker (réflexion par texte) et Talker (synthèse de la parole) et expliquez pourquoi le streaming parallèle fonctionne.
  Le langage est composé de deux parties: le langage est composé de deux parties: le langage est composé de deux parties: le langage est composé de deux parties: le langage est composé de deux parties: le langage est composé de deux parties: le langage est composé de deux parties: le langage est composé de deux parties: le langage est composé de deux parties: le langage est composé de deux parties: le langage est composé de deux parties; le langage est composé de deux parties: le langage est composé de deux parties; le langage est composé de deux parties: le langage est composé de deux parties; le langage est composé de deux parties; le langage est composé de deux parties; le langage est composé de deux parties; le langage est composé de deux parties; le langage est composé de deux parties; le langage est composé de deux parties; le langage est composé de deux parties; le langage est composé de deux parties; le langage est composé de deux parties; le langage est composé de deux parties; le langage est composé de deux parties; le langage est composé de deux parties; le langage est composé de deux parties; le langage est composé de deux parties; le langage est composé de deux parties; le langage est composé de deux.
- Calculer le budget de temps à premier octet audio (TTFAB) pour une interaction de conversation, composante par composante.
  Le premier épisode de la série est consacré à la réalisation de la série de films de télévision.
- Décrivez la position alignée dans le temps de TMRoPE en codant à travers la vision, l'audio et le texte dans le Thinker.
  Le temps de l'écriture est le temps de la rédaction.
- Nombre des trois modes de conversation en temps réel: demi-duplex, tour à tour, plein-duplex.
  Le mot "réalité" est traduit par "réalité".

## Le problème , l' introduction du problème

Un assistant vocale en temps réel doit faire beaucoup, rapidement:

> L'assistant de la voix doit faire vite beaucoup de choses.

1. Écoutez l'utilisateur. Tokenization de la parole en temps réel, détection de l'activité vocale (VAD) pour savoir quand ils ont fini de parler.
   Le mot "déjà" est traduit par "déjà" et "déjà".
2. Optionnellement, l'entrée de la caméra à 2 à 4 FPS, diffusée dans le Thinker avec l'audio.
   La vidéo est en 2 à 4 FPS, avec le flux de pensée.
3. Réfléchissez, composez une réponse conditionnée par l'historique de la conversation.
   Selon le dialogue historique, l'organisation répond à:
4. Synthétisez des jetons audio, décodez en forme d'onde, diffusez-les sur les haut-parleurs de l'utilisateur.
   Le mot de passe est le mot de passe de la langue française.

Chaque étape ajoute une latence. Le sentiment de conversation nécessite un total de retour et retour < 500ms  en dessous de cela, l'utilisateur arrête de remarquer le retard.

> Chaque étape augmente le retard. Le dialogue sens demande un total de retour < 500ms, l'utilisateur ne fait pas trop attention au retard.

Tout le matériel doit être diffusé en streaming.

> Chaque composant a besoin d'un traitement courant.

## Le concept de base.

> **【中文解读】**Le penseur-parleur 架构将"思考" (penser) et "说话" (parler)

> **【拓展：实时多模态交互**GPT-4o est le premier modèle d'interaction multi-modèles réellement réalisé: l'utilisateur peut poser des questions de voix, le modèle peut voir simultanément une image de la caméra, en réponse à une question de voix naturelle.


### Pensant et parlant

La décomposition de Qwen2.5 Omni:

> Qwen2.5-Omni des décompositions:

- Pensateur: un transformateur générateur de texte 7B-80B. Consomme des jetons de texte + image + audio interligés.
  Le récit de la première partie de la série est le récit de la première partie de la série.
- Parleur: un transformateur générateur de voix plus petit (200M-1B). Consomme les jetons de sortie de texte de Thinker ainsi que les jetons de contexte de parole récents.
  Le récit de la première partie de la série est le récit de la première partie de la série de la série de films de la série.
- Décodeur de parole: un décodeur de forme d'onde en streaming (SNAC, famille MoVQGAN) qui prend des jetons de parole à des échantillons audio en temps réel.
  Le mot "SNAC" est traduit par "SNAC" (SNAC), en français par "SNAC" (SNAC), en français par "SNAC").

La séparation est importante. Le penseur doit être grand pour un bon raisonnement. Le locuteur peut être petit parce que son travail est local  convertir le texte en jetons de parole. Le plus grand locuteur n'est pas plus expressif; il est plus lent.

> Le penseur doit être doué pour faire de bonnes conclusions. Le parleur peut être petit car sa tâche est de transformer le texte en un langage local.

- Les deux en parallèle:

> Il y a deux choses à faire:

1. Le Thinker émet un jeton texte.
   Le récit de la rédaction de la Bible est le récit de la rédaction de la Bible.
2. Le locuteur consomme t_i (via streaming) et émet des jetons de parole s_i, s_{i+1}, ..., s_{i+k}.
   Le langage de la langue de l'écriture est le langage de la langue de l'écriture.
3. Le décodeur de parole consomme des jetons de parole à leur arrivée et émet des échantillons audio.
   Le codeur de la langue chinoise est un codeur de la langue chinoise.
4. Au moment où Thinker est au jeton texte t_{i+3}, Talker a déjà diffusé audio pour t_0..t_{i+2}.
   Le récit de la première partie de la série est en cours de production.

> **【中文解读】**Le penseur 必須大(7B-80B) 才能做好推理,Talker 可以小(200M-1B) 由于它的 tâche est de localiser 文本转语音代币──更大的Talker 不会有更有表现力,只会更慢──并行运行时,当Thenker 在生成第一个+3 文本代币时,Talker 已在播放第一个到 i+2 文本对应的音频──

> **【拓展：Token 速率数学】**16kHz 语音 avec 50Hz 语音代币基础, signifie que chaque seconde a besoin de 50 语音代币──Speaker chaque seconde doit sortir >= 50 语音代币 才能跟上──H100 上200-300M de speakers peuvent sortir 100 语音代币每秒,远超需求; mais 7B Talker 会跟不上──这就是为什么需要专用小谈话模型而不是直接使用主模型──

### TMRoPE  positions multimodelles alignées dans le temps

Le penseur doit intégrer des images (arrivant à, disons, 4 FPS), des images audio (arrivant à 50 images/seconde) et du texte de l'historique de la conversation.

> Le penseur a besoin d'intégrer des images (par exemple 4 FPS) 音频(50 /秒) et des textes dans l'histoire du dialogue── simple séquence de séquences  Tous les images、 puis tous les audio、 puis les textes) seront perdus pour le temps de se rassembler──

TMRoPE attribue des timestamps absolus à chaque jeton. jeton de vision à t=2,3s. jeton audio à t=2,32s. jeton de texte de l'utilisateur "arrête" à t=2,35s. RoPE fait tourner l'attention par timestamp; le modèle les voit comme temporairement concurrents.

> TMRoPE pour chaque jeton Répartition absolue du temps── Vidéo jeton 在 t=2.3s──音频 jeton 在 t=2.32s── utilisateur "arrêter" texte jeton 在 t=2.35s── RoPE 按时间旋转注意力;模型将它们视为时间同时发生──

C'est l'infrastructure pour "il a fait signe de la main en disant bonjour" pour fonctionner  le modèle voit le cadre vidéo et l'audio au même moment conceptuel.

> C'est "il est en train de dire que tu es bien" qui peut fonctionner normalement.

### Synthèse du discours en continu

Les jetons de parole doivent être en flux. Mini-Omni (Xie & Wu, 2024) a introduit "les modèles de langage peuvent entendre, parler tout en pensant en streaming": les jetons de sortie Thinker et les jetons de sortie Talker interviennent dans la même séquence.

> 语音代币 必须流式传输──Mini-Omni 引入了"语言模型可以在流式思考的同时听和说":Thinker 输出代币 和 Talker 输出代币 在同一序列中交错──Thinker 一旦提交下一个文本代币,Talker 立即触发──没有批量边界──

Moshi (Défossez et al., octobre 2024) est la mise en œuvre ouverte la plus rapide. 160 ms TTFAB sur un seul A100. Architecture: un transformateur 7B unique qui émet des jetons de texte et de parole sur des positions alternatives, avec un "monologue interne" qui sépare le flux de pensée du flux de parole.

> Moshi est la réalisation la plus rapide de l'open source. Un seul A100 sur 160ms TTFAB.

### VAD et tournée

La détection de l'activité vocale est effectuée sur le côté d'entrée.

> 语音活动检测在输入端运行──两种模式:

- demi-duplex: l'utilisateur parle, le modèle écoute. le modèle parle, l'utilisateur écoute. transfert clair via la détection du silence VAD (~ 200 ms).
  Le nombre de personnes qui ont été interrogées par le groupe de travail est de 12 à 15 ans.
- Le modèle peut revenir en arrière ou interrompre. Beaucoup plus difficile. Moshi prend en charge cela.
  Le modèle peut être relayé avec le mot " " ou " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " "

Qwen2.5 Omni prend en charge la moitié du duplex par défaut, avec la prise de tour via un seuil de silence.

> Qwen2.5 Omni 默认支持半双工,通过静音值实现轮流──全双工需要应用层处理──

### Qwen3-Omni (novembre 2025)

Le successeur. Qwen3-80B Thinker, plus grand Talker, amélioré TMRoPE-v2. La latence proche de 250ms de GPT-4o. Poids ouverts.

> Le groupe de travail de la société GPT-4o est en train de se lancer dans la création de la série GPT-4o.

### Budget de la latence de production

Pour une interaction de streaming typique:

> 典型流式交互:

- Mic -> jetons audio: 40-80 ms.
  Le code de la radio est le code de la radio.
- Préchargement (immédiat + historique): 100-200 ms à 7B, beaucoup plus à 70B.
  Le nombre de personnes concernées est de 7 B.
- Le premier jeton de texte de Thinker: 40 ms.
  Le premier penseur est un symbole de la littérature.
- Le premier jeton texte est traité par le locuteur: 20 ms.
  Le mot de passe de la page est:
- Premiers jetons de parole engagés: 40 ms.
  Le code de la langue est le code de la langue.
- Décodeur résiduel-VQ: 30 ms.
  Le texte de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la
- Décode de forme d'onde de parole: 50-80 ms.
  Le nombre de coups de poing est de 50 à 80 ms.

TTFAB total: 320-510 ms à 7B, 600-900 ms à 70B. La qualité frontalière signifie généralement 70B+; d'où l'écart de latence frontalière.

> 总 TTFAB:7B 约 320-510ms,70B 约 600-900ms。前沿质量通常 signifie 70B+; il existe donc une différence de retard de la première ligne。

### Mathématiques du taux de jetons

À 16 kHz de la parole avec des jetons de parole de base de 50 Hz, vous avez besoin de 50 jetons de parole par seconde de sortie. Le locuteur doit émettre ≥ 50 tok/s pour suivre le rythme.

> 16 kHz 语音以 50 Hz 基础语音代币 计算, per second output needs 50 语音代币。Speaker 必须以 ≥50 tok/s de la vitesse de sortie。H100 上典型 LLM 吞吐量为 30-80 tok/s,小型(200-300M)Talker 足够快;7B Talker 会跟不上。

C'est pourquoi de petits modèles Talker dédiés existent plutôt que "utiliser simplement le modèle principal".

> C'est pourquoi il existe un modèle de petit parleur spécial et non un modèle principal directement utilisé.

## Utilisez-le avec le cadre de réalisation
```figure
l5-thinker-talker
```

## Utilisez-le

`code/main.py`- Le numéro de la liste:

- Simule un pipeline Thinker-Talker avec des taux d'émission de jetons simulés.
  Le nombre de personnes qui ont été interrogées par le gouvernement est de 22 à 25 ans.
- Compute TTFAB pour les tailles de modèle configurables et les taux d'échantillonnage du micro.
  Pour le modèle de taille et de taille de la taille du modèle de taille de la taille du modèle de modèle de modèle de modèle de modèle de modèle de modèle de modèle de modèle de modèle de modèle de modèle de modèle de modèle de modèle de modèle de modèle de modèle de modèle de modèle de modèle de modèle de modèle de modèle de modèle de modèle de modèle de modèle de modèle de modèle de modèle de modèle de modèle de modèle de modèle de modèle de modèle de modèle de modèle de modèle de modèle de modèle de modèle de modèle de modèle de modèle de modèle de modèle de modèle de modèle de modèle de modèle de modèle de modèle de modèle de modèle de modèle de modèle de modèle de modèle de modèle de modèle de modèle de modèle de modèle de modèle de modèle de modèle de modèle de modèle de modèle de modèle de modèle de modèle de modèle de modèle de modèle de modèle de modèle de modèle de modèle de modèle de modèle de modèle de modèle de modèle de modèle de modèle de modèle de modèle de modèle de modèle de modèle de modèle de modèle de modèle de modèle de modèle de modèle de modèle de modèle de modèle de modèle de modèle de modèle de modèle de modèle de modèle de modèle de modèle de modèle de modèle de taille de taille de taille de taille de taille de modèle de modèle de modèle de modèle de modèle de modèle de modèle de modèle de modèle de modèle de modèle de modèle de modèle de modèle de modèle de modèle de modèle de modèle de modèle de modèle de modèle de modèle de modèle de modèle de modèle de modèle de modèle de modèle de modèle de modèle de modèle de modèle de modèle de modèle de modèle de modèle de modèle de modèle de modèle de modèle de modèle de modèle de modèle de modèle de modèle de modèle de modèle de modèle de modèle de modèle de modèle de modèle de modèle de modèle de modèle de modèle de modèle de modèle de modèle de modèle de modèle de modèle de modèle de modèle de modèle de modèle de modèle de modèle de modèle de modèle de modèle de modèle de modèle de modèle de modèle de modèle de modèle de modèle de modèle de modèle de modèle de modèle de modèle de modèle de modèle de modèle de modèle de modèle de modèle de modèle de modèle de modèle de modèle de modèle de modèle de modèle de modèle de modèle de modèle de modèle de modèle de modèle de modèle de modèle de modèle de modèle de modèle de modèle de modèle de modèle de modèle de modèle de modèle de modèle de modèle de modèle de modèle de modèle de modèle de modèle de modèle de modèle de modèle de modèle de modèle de modèle de modèle de modèle de modèle
- Il montre une demi-duplex avec un seuil de silence VAD.
  Le mot "VAD" est traduit par "VAD".

## Envoyez-le . Produit .

Cette leçon produit `outputs/skill-omni-streaming-budget.md`. Compte tenu du TTFAB cible et du jeu de fonctionnalités (vision-in, bilingue, double-ensemble) d'un produit vocal en temps réel, il choisit Qwen2.5-Omni, Qwen3-Omni, Moshi ou Mini-Omni et taille le Thinker/Talker.

> 本课产 出 `outputs/skill-omni-streaming-budget.md`△ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △

## Les exercices

1. Votre objectif TTFAB est de 300ms. Sur un 7B Thinker et 300M Talker, écrivez la latence de chaque composant.

2. Qwen2.5-Omni utilise TMRoPE. Décrivez ce que le modèle voit pour une demande où l'utilisateur commence à parler à t=1s et la caméra capture un geste à t=1.2s. Qwen2.5-Omni utilise TMRoPE。 description模型在用户 t=1s 开始说话、摄像头 t=1.2s 捕获手势时看的输入。

3. Le support du duplex complet exige que le modèle émette de l'audio en écoutant. Proposez un format de données de formation qui enseigne cela.

4. Lisez l'article de Moshi Section 4. Décrivez la séparation du "monologue intérieur" et pourquoi elle évite la séparation de penseur-parleur.

5. Comptez le budget de débit: à quelle vitesse un interlocuteur doit-il émettre des jetons pour suivre le rythme de la parole à 16 kHz à 50 jetons de couche de base/seconde ?

## Les termes clés

| Term | What people say | What it actually means | 中文释义 |
|------|-----------------|------------------------|---------|
| Thinker | "Reasoning brain" 思考者 | Large text-generating transformer producing what to say 生成"说什么"的大型文本生成 Transformer | |
| Talker | "Speech-generating mouth" 说话者 | Small transformer producing discrete speech tokens from Thinker's text 将 Thinker 文本转为语音 token 的小型 Transformer | |
| TTFAB | "Latency budget" 首音频字节延迟 | Time-to-first-audio-byte: from user speech end to first audio sample out 从用户说话结束到首个音频样本输出的延迟 | |
| TMRoPE | "Time-aligned RoPE" 时间对齐旋转位置编码 | Position encoding using absolute timestamps across vision, audio, text 跨视觉、音频、文本使用绝对时间戳的位置编码 | |
| Half-duplex | "Turn-taking" 半双工 | User and model alternate; VAD silence detects user-done 用户和模型交替说话；VAD 静音检测用户说完 | |
| Full-duplex | "Simultaneous" 全双工 | Model can speak and listen at the same time; backchannel capable 模型可同时说话和监听；支持回话 | |
| Inner monologue | "Moshi separation" 内心独白 | Single-model design where thinking-stream and speaking-stream interleave 单模型设计，思考流和说话流交替出现 | |

## Encore une lecture

- [Xu et al. — Qwen2.5-Omni (arXiv:2503.20215)](https://arxiv.org/abs/2503.20215)
- [Qwen Team — Qwen3-Omni (arXiv:2509.17765)](https://arxiv.org/html/2509.17765v1)
- [Xie & Wu — Mini-Omni (arXiv:2408.16725)](https://arxiv.org/abs/2408.16725)
- [Défossez et al. — Moshi (arXiv:2410.00037)](https://arxiv.org/abs/2410.00037)
- [Zeng et al. — GLM-4-Voice (arXiv:2412.02612)](https://arxiv.org/abs/2412.02612)
