# Détection et prise de tournée de l'activité vocale Silero, Cobra et le flush trick

> Chaque agent vocal vit ou meurt sur deux décisions: l'utilisateur parle maintenant, et sont-ils terminés? VAD répond au premier. Détection de virage (VAD + silence-hangover + modèle de point d'extrémité sémantique) répond au second.

> **【中文解读】**Le succès de chaque assistant de voix dépend de deux jugements: le utilisateur est-il en train de parler ? L'utilisateur dit-il terminé ?

**Type:** Build | **类型:** 构建
**Languages:** Python | **语言:** Python
**Prerequisites:** Phase 6 · 11 (Real-Time Audio), Phase 6 · 12 (Voice Assistant) | **前置知识:** 阶段 6 · 11（实时音频），阶段 6 · 12（语音助手）
**Time:** ~45 minutes | **预计用时:** ~45 分钟

## Le problème , l' introduction du problème

Trois décisions distinctes qu' un agent de voix prend sur chaque pièce de 20 ms:

> L'assistant de son a besoin de faire trois jugements différents sur chaque bloc de 20 ms:

> **【中文解读】**La question posée dans ce chapitre est la suivante: comment comprendre et appliquer correctement cette technique dans la conception pratique. Comprendre le contexte de la question aide à saisir les principaux facteurs de décision concernant le type de technologie. Dans les systèmes d'IA réels, le type de technique erroné coûte souvent plus cher que le coût de la mise en œuvre de détails.


1. **Is this frame speech?**- Le VAD, binaire, par cadre.
   Le mot "je suis" est traduit par "je suis" en français.
2. **Has the user started a new utterance?** détection de l'apparition.
   Le site officiel de l'équipe de télévision de la Chine est en cours de développement.
3. **Has the user finished?** point de fin (tour de fin).
   Le nombre de personnes qui ont été interrogées est de 12 à 15 ans.

La réponse naïve (troisième limite d'énergie) échoue sur tout bruit  trafic, claviers, babbling de foule. La réponse 2026: Silero VAD (ouverte, profondément apprise) + un modèle de détection de tour (section de bout sémantique) + une gueule de bois de silence calibrée par VAD.

> 朴素的答案(能量值) Dans tout environnement bruyant, tout va mal交通声、键盘声、人群杂声。 La réponse de l'année 2026 est: Silero VAD(开源、深度学习) + 轮次检测模型(语义端点检测) + VAD 校准的静音持续等待──

## Le concept de base.

> **【中文解读】**Le présent article présente les concepts et les bases théoriques de base. La connaissance de ces concepts est la prémisse de la réalisation de la réalisation de la réalisation, mais aussi le point de connaissance de l'interview et de la pratique de l'ingénierie.


![VAD cascade: energy → Silero → turn-detector → flush trick](../assets/vad-turn-taking.svg)

### La cascade de trois niveaux de VAD

> 3e classe VAD

**Tier 1: energy gate.**Le plus bon marché, le seuil RMS à -40 dBFS, filtre le silence évident mais tire sur tout bruit au-dessus du seuil.

> **第一层：能量门控。**Le plus bon marché est de mettre la valeur de RMS à -40 dBFS.

**Tier 2: Silero VAD**Paramètres 1M. Formé sur 6000 langues. Runs en ~1 ms par 30 ms de pièce sur un seul fil de CPU. 87,7% TPR à 5% FPR.

> **第二层：Silero VAD**(MIT) 许可) ∙100.000参数── dans 6000+ 种语言上训练── dans un seul CPU 线程 ⋅ 30 ms 块 ⋅ 1 ms ⋅ 推理时间──5% FPR 下 TPR ⋅ 87.7%──

**Tier 3: semantic turn detector.**Le modèle de détection de tour de LiveKit (2024-2026) ou votre propre petit classifiateur.

> **第三层：语义轮次检测器。**Le modèle de suivi de LiveKit est de 2024 à 2026.

### Paramètres clés et leurs défauts

> 关键参数 et sa valeur par défaut

- **Threshold.**Silero produit une probabilité; classer le discours à &gt; 0,5 (par défaut) ou &gt; 0,3 (sensitif).
  Le mot grec traduit par " le mot grec "**阈值。**Silero 输出概率值;以 > 0.5(默认) ou > 0.3(sensitive模式) 分类语音──值越低 = 首词截断越少,但误报越多──
- **Minimum speech duration.**Rejeter le discours plus court que 250 ms  généralement la toux ou le bruit de la chaise.
  Le mot grec traduit par " le mot grec "**最小语音时长。**拒绝短于250 ms的语音通常是咳或椅子噪音──
- **Silence hangover (end-pointing).**Après que le VAD soit revenu à 0, attendez 500 à 800 ms avant de déclarer la fin du tour. Trop court → interrompre l'utilisateur. Trop longtemps → semble lent.
  Le mot grec traduit par " le mot grec "**静音持续等待（端点检测）。**VAD retour à 0 后, attendre 500-800 ms pour réaffirmer la fin de la ronde.
- **Pre-roll buffer.**Gardez 300 à 500 ms d'audio avant que le VAD ne tire.
  Le mot grec traduit par " le mot grec "**预滚缓冲。**Dans le VAD 触发前保留 300-500 ms 音频──防止""字被截断──

### Le truc du flush (Kyutai 2025)

Les modèles STT en streaming ont un retard de vision (500 ms pour Kyutai STT-1B, 2,5 s pour STT-2.6B). Normalement, vous attendez aussi longtemps après la fin de la parole pour la transcription.**send a flush signal to the STT**Le processus STT est effectué en temps réel, donc le tampon de 500 ms se termine en 125 ms.

> 流式 STT 模型有前视延迟(Kyutai STT-1B 为 500 ms,STT-2.6B 为 2.5 s)  Vous devez généralement attendre si longtemps après la fin du langage pour obtenir le résultat du langage.**向 STT 发送刷新信号**, Forcément immédiatement de sortie;. STT avec environ 4 fois la vitesse de traitement en temps réel, donc 500 ms 缓冲区在约125 ms内完成──

Fin à fin: 125 ms VAD + flush STT = latence de conversation.

> 端到端:125 ms VAD + 刷新 STT = 对话级延迟──

### Comparaison du VAD 2026

> Comparativement à la VAD de 2026

| VAD | TPR @ 5% FPR | Latency | License |
|-----|--------------|---------|---------|
| WebRTC VAD (Google, 2013) | 50.0% | 30 ms | BSD |
| Silero VAD (2020-2026) | 87.7% | ~1 ms | MIT |
| Cobra VAD (Picovoice) | 98.9% | ~1 ms | commercial |
| pyannote segmentation | 95% | ~10 ms | MIT-ish |

Silero est la bonne option par défaut. Cobra est la mise à niveau de conformité / précision.

> Silero est une option de mise à niveau conforme à la norme et à la norme. Le VAD basé uniquement sur l'énergie n'a pas de place dans l'environnement de production de 2026 .

> **【中文解读】**Cette méthode "de zéro" peut aider à comprendre le principe derrière le cadre, en cas de problème, ne sera pas bloqué dans une boîte noire.

> **【拓展：语音 AI 的产品化】**La technologie du langage est confrontée à des défis particuliers dans la fabrication de produits: différents sons, bruits de fond, prises de vue, nombreux discours, etc. Les produits de Siri, Alexa, et de petite enfance ont été largement optimisés pour résoudre ces "problèmes de longue durée".

> **【拓展：多语言语音技术】**Les caractéristiques du langage mondial sont énormes: la voix de la langue (en chinois comme en chinois) est à un niveau élevé, les ressources linguistiques sont faibles et les données de formation manquent.

> **【拓展：语音隐私与安全】**Les données de la langue contiennent une grande quantité d'informations personnelles confidentielles (en anglais) et sont très fausses (en anglais).





## Construisez-le et mettez-le en œuvre.
```figure
sp-vad-cascade
```

## Faites-le

### Étape 1: la porte d'énergie

> 步骤 1: L'énergie est contrôlée

```python
def energy_vad(chunk, threshold_dbfs=-40.0):
    rms = (sum(x * x for x in chunk) / len(chunk)) ** 0.5
    dbfs = 20.0 * math.log10(max(rms, 1e-10))
    return dbfs > threshold_dbfs
```

### Étape 2: Silero VAD en Python

> 步骤 2: utiliser Silero VAD dans Python

```python
from silero_vad import load_silero_vad, get_speech_timestamps

vad = load_silero_vad()
audio = torch.tensor(waveform_16k, dtype=torch.float32)
segments = get_speech_timestamps(
    audio, vad, sampling_rate=16000,
    threshold=0.5,
    min_speech_duration_ms=250,
    min_silence_duration_ms=500,
    speech_pad_ms=300,
)
for s in segments:
    print(f"{s['start']/16000:.2f}s - {s['end']/16000:.2f}s")
```

### Étape 3: machine d'état de tournage

> 步骤 3: Retour à la fin de l'état

```python
class TurnDetector:
    def __init__(self, silence_hangover_ms=500, min_speech_ms=250):
        self.state = "idle"
        self.speech_ms = 0
        self.silence_ms = 0
        self.silence_hangover_ms = silence_hangover_ms
        self.min_speech_ms = min_speech_ms

    def update(self, is_speech, chunk_ms=20):
        if is_speech:
            self.speech_ms += chunk_ms
            self.silence_ms = 0
            if self.state == "idle" and self.speech_ms >= self.min_speech_ms:
                self.state = "speaking"
                return "START"
        else:
            self.silence_ms += chunk_ms
            if self.state == "speaking" and self.silence_ms >= self.silence_hangover_ms:
                self.state = "idle"
                self.speech_ms = 0
                return "END"
        return None
```

### Étape 4: le squelette de la ruse

> 步骤 4: Les nouveaux techniques du code du cadre

```python
def flush_on_end(stt_client, audio_buffer):
    stt_client.send_audio(audio_buffer)
    stt_client.send_flush()
    return stt_client.recv_transcript(timeout_ms=150)
```

> **【中文解读】**Dans ce chapitre, nous allons montrer comment utiliser un cadre mature (comme PyTorch, HuggingFace, etc.) pour appliquer rapidement cette technique.


STT (Kyutai, Deepgram, AssemblyAI) doit prendre en charge le flush pour que cela fonctionne.

> STT(Kyutai、Deepgram、AssemblyAI) doit soutenir le flush pour que ces techniques soient efficaces。Whisper 流式不支持




> **【拓展：语音与情感计算】**Le langage n'est pas seulement un moyen de transmettre des informations, il est également un moyen de transmettre des signaux émotionnels riches.

## Utilisez-le avec le cadre de réalisation

| Situation | VAD choice |
|-----------|-----------|
| Open, fast, general / 开源、快速、通用 | Silero VAD |
| Commercial call center / 商业呼叫中心 | Cobra VAD |
| On-device (phone) / 端侧（手机） | Silero VAD ONNX |
| Research / diarization / 研究/说话人日志 | pyannote segmentation |
| Zero-dependency fallback / 零依赖后备方案 | WebRTC VAD（传统） |
| Need turn-ending quality / 需要轮次结束质量 | Silero + LiveKit 轮次检测器分层 |

Règle générale: ne jamais expédier de VAD à usage énergétique uniquement à moins que vous n'ayez vraiment pas d'autre option.

> 經驗法则: à moins que vous n'ayez vraiment pas d'autre choix, alors ne vous lancez jamais sur la ligne uniquement en fonction de la quantité d'énergie VAD.



## Les pièges

> 常见陷

- **Fixed threshold.**Il fonctionne en silence, il échoue en bruit.
  Le mot grec traduit par " le mot grec "**固定阈值。**Dans un environnement calme, il est possible de passer à Silero.
- **Too-short silence hangover.**L'agent interrompt la moitié de la phrase. 500 à 800 ms est le bon point pour le discours de conversation.
  Le mot grec traduit par " le mot grec "**静音持续等待过短。**助手在句子中打断用户──500-800 ms est la meilleure plage de dialogue语音──
- **Too-long hangover.**C'est un test A/B avec des utilisateurs cibles.
  Le mot grec traduit par " le mot grec "**静音持续等待过长。**感觉迟──与目标用户进行A/B 测试──
- **No pre-roll buffer.**Les 200 à 300 ms d'audio perdus par l'utilisateur.
  Le mot grec traduit par " le mot grec "**没有预滚缓冲。**Les utilisateurs de la vidéo ont perdu 200 à 300 ms.
- **Ignoring semantic endpointing.**"Hmm, laisse-moi penser"... contient de longues pauses. Les utilisateurs détestent être coupés au milieu de la pensée. Utilisez le détecteur de tour de LiveKit ou quelque chose comme ça.
  Le mot grec traduit par " le mot grec "**忽略语义端点检测。**",让我想想......" contient un long arrêt. Les utilisateurs ne veulent pas être interrompus dans le processus de réflexion.

> **【中文解读】**Cette section se concentre sur la façon de déployer le modèle en tant que produit disponible. De l'original au système de production, il faut considérer plusieurs dimensions de l'optimisation des performances, du traitement des erreurs, du contrôle, etc.


## Envoyez-le . Produit .

- Je ne sais pas .`outputs/skill-vad-tuner.md`Choisissez le modèle VAD, le seuil, la gueule de bois, la stratégie de pré-rolling et de détection de tour pour une charge de travail.

> 保存为 `outputs/skill-vad-tuner.md`◊ Choisir un modèle VAD value、静音

## Les exercices

1. **Easy.**On court .`code/main.py`Il simule une séquence de discours + silence + discours + toux et teste trois niveaux de VAD.
   Le mot grec traduit par " le mot grec "**简单。**运行  référencement`code/main.py`Il est en train de faire une séquence de voix + de voix + de voix + de voix + de tousse,并测试三层 VAD。
2. **Medium.**Installez`silero-vad`, traiter une enregistrement de 5 minutes, régler le seuil pour minimiser les clips de premier mot et les faux déclencheurs.
   Le mot grec traduit par " le mot grec "**中等。**Montage`silero-vad`, traitement un paragraphe 5 minutes enregistrement, ajustement de la valeur pour minimiser la première phrase coupure et erreur de toucher.
3. **Hard.**Construisez un mini détecteur de virage: Silero VAD + un MLP à 3 couches sur les emblèmes des 10 derniers mots (utilisez des transformateurs de phrases).
   Le mot grec traduit par " le mot grec "**困难。**Construire un petit détecteur de rotations: Silero VAD +  basé sur 10 个近词嵌入的3层 MLP(Utilisation de transformateurs de phrases) ⋅ entraînement sur le cycle de fin de données du marquage manuel ⋅比纯 Silero 方案 F1 ⋅ 10% ⋅

> **【中文解读】**Dans le tableau des termes, la définition du terme "ce que les gens disent" et "ce qu'il signifie réellement" est différenciée entre le langage quotidien et la signification technique précise.


## Les termes clés

| Term | What people say | What it actually means |
|------|-----------------|-----------------------|
| VAD | Voice detector | Binary per-frame: is this speech? / 逐帧二分类：这是语音吗？ |
| Turn detection | End-pointing | VAD + silence-hangover + semantic endpoint. / VAD + 静音持续 + 语义端点 |
| Silence hangover | Wait-after-speech | Time to wait before declaring turn end; 500-800 ms. / 宣布轮次结束前的等待时间；500-800 ms |
| Pre-roll | Pre-speech buffer | Keep 300-500 ms audio before VAD fires. / 在 VAD 触发前保留 300-500 ms 音频 |
| Flush trick | Kyutai hack | VAD → flush-STT → 125 ms instead of 500 ms delay. / VAD → 刷新 STT → 125 ms 而非 500 ms 延迟 |
| Semantic endpoint | "Did they mean to stop?" | ML classifier that looks at words, not just silence. / 看词汇而非仅看静音的 ML 分类器 |
| TPR @ FPR 5% | ROC point | Standard VAD benchmark; 87.7% for Silero, 50% WebRTC. / 标准 VAD 基准；Silero 87.7%，WebRTC 50% |

> **【中文解读】**延伸阅读 fournit des ressources de haute qualité pour l'apprentissage en profondeur. Ces articles et cours sont des références classiques dans ce domaine, adaptés aux lecteurs qui ont besoin d'une compréhension approfondie.


## Encore une lecture

- [Silero VAD](https://github.com/snakers4/silero-vad) l'ouverture de référence du VAD.
  Silero VAD  Open Source en référence à VAD
- [Picovoice Cobra VAD](https://picovoice.ai/products/cobra/) leader de la précision commerciale.
  Le premier groupe de la société a été créé en 1999 pour la création de nouveaux modèles de services de télécommunications.
- [Kyutai — Unmute + flush trick](https://kyutai.org/stt)- Le truc de l'ingénierie sous 200 ms.
  KyutaiUnmute + 刷新技巧亚 200 ms 的工程技巧──
- [LiveKit — turn detection](https://docs.livekit.io/agents/logic/turns/) définition sémantique de la production.
  Le programme de recherche de l'équipe de recherche de l'équipe de recherche de l'équipe de recherche de l'équipe de recherche de l'équipe de recherche de l'équipe de recherche de l'équipe de recherche de l'équipe de recherche de l'équipe de recherche de l'équipe de recherche de l'équipe de recherche de l'équipe de recherche de l'équipe de recherche de l'équipe de recherche de l'équipe de recherche de l'équipe de recherche de l'équipe de recherche de l'équipe de recherche de l'équipe de recherche de l'équipe de recherche de l'équipe de recherche de l'équipe de recherche de l'équipe de recherche de l'équipe de recherche de l'équipe de recherche de l'équipe de recherche de recherche de l'équipe de recherche de l'équipe de recherche de recherche de l'équipe de recherche de recherche de l'équipe de recherche de l'équipe de recherche de recherche de l'équipe de recherche de l'équipe de recherche de recherche de l'équipe de recherche de l'équipe de recherche de l'équipe de recherche de l'équipe de l'équipe de recherche de l'équipe de l'équipe de l'équipe de l'équipe de l'équipe de l'équipe de l'équipe de l'équipe de l'équipe de l'équipe de l'équipe de l'équipe de l'équipe de l'équipe de l'équipe de la région de l'équipe de l'équipe de l'équipe de la région de la région de la région de la région de la région de la région de la région de la région de
- [WebRTC VAD](https://webrtc.googlesource.com/src/) la ligne de base héritée.
  Le réseau WebRTC VAD traditionnel
- [pyannote segmentation](https://github.com/pyannote/pyannote-audio) Segmentation au niveau de la diarisation.
  Le groupe de la section de notes de piyannote

> **【中文解读】**延伸阅读 a fourni des ressources de haute qualité pour l'apprentissage en profondeur, y compris des articles, des cours et des outils.

