# Les agents de voix: Pipecat et LiveKit

> Les agents vocaux sont une catégorie de production de première classe en 2026. Pipecat vous offre un pipeline basé sur le cadre Python (VAD → STT → LLM → TTS → transport). LiveKit Agents renvoie les modèles d'IA aux utilisateurs via WebRTC.

**Type:** Learn | **类型:** 学习
**Languages:** Python (stdlib) | **语言:** Python (标准库)
**Prerequisites:** Phase 14 · 01 (Agent Loop), Phase 14 · 12 (Workflow Patterns) | **前置知识:** 见原文
**Time:** ~60 minutes | **时间:** 见原文

## Objectifs d'apprentissage

- Décrivez le pipeline basé sur le cadre de Pipecat: DOWNSTREAM (source→sink) et UPSTREAM (contrôle).
- Nombre des étapes du pipeline vocal canonique et qui transportent les supports Pipecat.
- Expliquez les deux classes d'agents vocaux de LiveKit Agents (MultimodalAgent, VoicePipelineAgent) et quand chacune s'adapte.
- Résumez les attentes de latence de production en 2026 et comment elles influencent les choix d'architecture.

## Le problème , l' introduction du problème

Les agents vocaux ne sont pas une boucle de texte avec TTS connecté. Les budgets de latence sont brutaux (~ 600 ms), l'audio partiel est par défaut, la détection de virage est un modèle, et les transports vont de la téléphonie SIP à WebRTC.

> 语音 Agent 不是文本循环加上 TTS──延迟预算极极苛(约600ms),部分音频是默认状态,轮次检测是一个模型,传输方式从电话SIP到WebRTC 不等──你要么构建一个基于的管道(Pipecat),要么依赖一个平台(LiveKit)──


> **【中文解读】**语音 Agent 需要实时处理音频流语音识别(ASR)、LLM 推理、语音合成(TTS) du retard doit être de 300ms et en interne pour maintenir le dialogue naturel。Pipecat 和 LiveKit 提供构建低延迟语音 Agent's framework and infrastructure。

> **{【拓展：Pipecat（开源框架）和 LiveKit（实时音频基础设施）是 2026 年语音 Agent 生...】}**Pipecat fournit des canaux de traitement audio modulaires, prend en charge plusieurs types d'ASR/TTS/LLM 后端──LiveKit fournit des infrastructures WebRTC, assure une transmission audio tardive.

>  **【前置】**學本節前 請先掌握:Phase 14·01 (Agent Loop) 理解 ReAct 循环,本节是循环外加一层音频管道;Phase 14·12 (Patrons de flux de travail) 理解多阶段工作流的概念──另外最好有数字信号处理基础概念──采样率、、流式处理),否则看"框架型管道" 会很──

## Le concept de base.

### Le piquet (piquet-ai/piquet)

- Cadre de pipeline basé sur le cadre Python.
- `Frame`- Je suis là.`FrameProcessor`une chaîne.
- Deux directions de débit:
  - **DOWNSTREAM** source → évier (audio en, TTS hors).
  - **UPSTREAM** rétroaction et contrôle (annulation, métriques, barge-in).
- `PipelineTask`gère le cycle de vie avec des événements (`on_pipeline_started`- Je suis là .`on_pipeline_finished`- Je suis là .`on_idle_timeout`) et des observateurs pour les mesures/traçage/RTVI.

L'équipement de transport typique:

```
VAD (Silero) → STT → LLM (context alternates user/assistant) → TTS → transport
```

Les transports: quotidien, LiveKit, SmallWebRTCTransport, FastAPI WebSocket, WhatsApp.

>  **【类比】**Pipecat du pipeline basé sur le cadre 像汽车流水线:每个工位(Processeur) seulement faire une chose  VAD 工位识别有没有人说话、STT 工位把语音转文字、LLM 工位想回复、TTS 工位把文字转语音),车架(Frame) de se rendre à l'arrière流 (DOWNSTREAM), n'importe quel工位 trouver des problèmes de qualité peut être arrêté sur la ligne rouge(UPSTREAM annuler  c'est le mécanisme de barge-in 打断)  Key: chaque lieu entre les deux est par une résolution standardisée du format "Frame", afin que vous puissiez placer le STT 工位 de Whisper 换成深gram et ne pas déplacer d'autres工位

> 语音代理 结合 LLM 和实时语音处理──Pipecat 和 LiveKit sont les deux principaux cadres d'agents de la voix, séparément de traitement du son du canal et de la communication en temps réel──

Pipecat Flow ajoute des conversations structurées (machines d'état).

> 语音代理 结合 LLM 和实时语音处理──Pipecat 和 LiveKit sont les deux principaux cadres d'agents de la voix, séparément de traitement du son du canal et de la communication en temps réel──

### Les agents de LiveKit (livekit/agents)

- Il permet de passer des modèles d'IA aux utilisateurs via WebRTC.
- Concepts clés: `Agent`- Je suis là .`AgentSession`- Je suis là .`entrypoint`- Je suis là .`AgentServer`- Je suis désolé .
- Deux cours d'agents vocales:
  - **MultimodalAgent** audio direct via OpenAI en temps réel ou équivalent.
  - **VoicePipelineAgent** STT → LLM → TTS cascade; donne un contrôle au niveau du texte.
- Détection sémantique du tour par un modèle transformateur.
- Intégration de MCP natifs.
- Téléphonie par SIP.
- 50+ modèles sans API-clés via LiveKit Inference; 200+ plus via des plugins.

### Plateformes commerciales

Vapi (~ 450600ms sur une pile premium optimisée) et Retell (~ 600ms de bout en bout sur 180 appels de test) s'ajoutent à ces deux.

> 🤔 **【困惑】**Q: MultimodalAgent (en anglais) et VoicePipelineAgent (en anglais) (en anglais) (en anglais) (en anglais) (en anglais) (en anglais) (en anglais) (en anglais) (en anglais) (en anglais) (en anglais) (en anglais) (en anglais) (en anglais) (en anglais) (en anglais) (en anglais) (en anglais) (en anglais) (en anglais) (en anglais) (en anglais) (en anglais) (en anglais) (en anglais) (en anglais) (en anglais) (en anglais) (en anglais) (en anglais) (en anglais) (en anglais) (en anglais) (en anglais) (en anglais) (en anglais) (en anglais) (en anglais) (en anglais) (en anglais) (en anglais) (en anglais) (en anglais) (en anglais) (en anglais) (en anglais) (en anglais) (en anglais) (en anglais) (en anglais) (en anglais) (en anglais) (en anglais) (en anglais) (en anglais) (en anglais) (en anglais) (en anglais) (en anglais) (en anglais) (en anglais) (en anglais) (en anglais) (en anglais) (en anglais) (en anglais) (en anglais) (en anglais) (en anglais) (en anglais) (en anglais) (en anglais) (en anglais) (en anglais) (en anglais) (en anglais) (en anglais) (en anglais) (en anglais) (en anglais) (en anglais) (en anglais) (en anglais) (en anglais) (en anglais) (en anglais) (en anglais) (en anglais) (en anglais) (en anglais) (en anglais) (en anglais) (en anglais) (en anglais) (en anglais) (en anglais) (en anglais) (en anglais)

> Vapi(optimisation post-High Levels: 450-600ms) et Retell(180 fois Test Talk End to End 600ms) construit sur ces éléments.

> 语音代理 结合 LLM 和实时语音处理──Pipecat 和 LiveKit sont les deux principaux cadres d'agents de la voix, séparément de traitement du son du canal et de la communication en temps réel──

### Où ce modèle va mal

- **No barge-in handling.**L'utilisateur interrompt, l'agent continue de parler. Require UPSTREAM d'annuler des images dans Pipecat, équivalent dans LiveKit.
- **STT confidence ignored.**Des transcriptions de faible confiance sont envoyées à la maîtrise comme un évangile.
- **TTS mid-sentence cutoff.**Lorsque le pipeline annule le milieu de l'utterance, TTS doit savoir ou couper l'audio.
- **Latency budget ignored.**Chaque composant ajoute 50 à 200 ms. Résumez votre chaîne avant expédition.

> **没有打断处理。**Utilisateur: Arrêtez;Agent: Continuez à parler:
> **忽略 STT 置信度。**La transcription de la confiance est considérée comme la vérité transmise à la LLM.
> **TTS 句中截断。**Lorsque le tube est en train de disparaître, TTS a besoin de savoir ou de couper le son.
> **忽略延迟预算。**Chaque composant augmente de 50 à 200 ms.

### La latence typique en 2026

- VAD: 20 à 60 ms
- TTS partiel: 100 à 250 ms
- Le premier jeton LLM: 150400ms
- TTS première voix: 100 à 200 ms
- RTT de transport: 3080ms

Le temps de transmission de 450 à 600 ms est très élevé. 800 à 1200 ms est courant. Tout ce qui est supérieur à 1500 ms semble cassé.

> Le niveau de la hauteur est de 450 à 600 ms. Le niveau de la hauteur est de 800 à 1200 ms.

> 语音代理 结合 LLM 和实时语音处理──Pipecat 和 LiveKit sont les deux principaux cadres d'agents de la voix, séparément de traitement du son du canal et de la communication en temps réel──

## Construisez-le et mettez-le en œuvre.

> ️ **【易错点】**Il y a trois chutes de l'eau:**不做 barge-in 处理** l'utilisateur se casse quand l'agent est encore en train de se casser, il faut être en processeur TTS 监听UPSTREAM annuler le cadre 并立即停止音频输出──(2) **忽略 STT 置信度**置信度 0.3 的""被当成用户回答,Agent 走错分支;修复:confiance < 0.7 时让Agent 反问"我没听清,能再说一次吗"──(3) **延迟预算算总账** Individuellement regarder chaque composé tout à fait identifié(VAD 40ms + STT 200ms + LLM 300ms + TTS 150ms = 690ms), mais sur la ligne postérieure à la ligne postérieure 1200ms, parce que le réseau RTT et la file d'attente sont en panne.
```figure
voice-pipeline
```

## Faites-le

`code/main.py`est un pipeline de jouets à base de cadres avec:

> 语音代理 结合 LLM 和实时语音处理──Pipecat 和 LiveKit sont les deux principaux cadres d'agents de la voix, séparément de traitement du son du canal et de la communication en temps réel──

- `Frame`types (audio, transcription, texte, tts_audio, contrôle).
- `Processor`interface avec `process(frame)`- Je suis désolé .
- Un pipeline en cinq étapes (VAD → STT → LLM → TTS → transport) en tant que processeurs scriptés.
- Un cadre UPSTREAM pour démontrer le barge-in.

- Je vais le faire.

```
python3 code/main.py
```

La trace montre un débit normal et une annulation de barge qui arrête le TTS à mi-écoute.

> Trace montre le processus normal et un arrêt en milieu de conversation TTS 打断取消──

> 语音代理 结合 LLM 和实时语音处理──Pipecat 和 LiveKit sont les deux principaux cadres d'agents de la voix, séparément de traitement du son du canal et de la communication en temps réel──

## Utilisez-le avec le cadre de réalisation

- **Pipecat**pour un contrôle complet  processeurs personnalisés, fournisseurs de services Python-first, enregistreurs.
- **LiveKit Agents**pour les déploiements WebRTC et la téléphonie.
- **Vapi / Retell**pour les agents de voix hébergés sans équipe WebRTC.
- **OpenAI Realtime / Gemini Live**pour l'audio-en/audio-sortie directe (MultimodalAgent).

## Envoyez-le . Produit .

`outputs/skill-voice-pipeline.md`Il est équipé d'un pipeline vocal en forme de Pipecat avec VAD + STT + LLM + TTS + transport plus maniabilité à la barge.

> `outputs/skill-voice-pipeline.md`Construire un pipeline de voix en forme de Pipecat, comprenant VAD + STT + LLM + TTS + 传输以及打断处理──

> 语音代理 结合 LLM 和实时语音处理──Pipecat 和 LiveKit sont les deux principaux cadres d'agents de la voix, séparément de traitement du son du canal et de la communication en temps réel──

## Les exercices

1. Ajoutez un observateur de métriques à votre pipeline de jouets: comptez les cadres par étape par seconde.
  Le mot "exercer" est traduit par "exercer".
2. Mettre en œuvre une TST avec un dégagement de confiance: en dessous du seuil, demander "peut-on le répéter?"
  Le mot "exercer" est traduit par "exercer".
3. Ajouter la détection sémantique du tour: règle simple  si la transcription se termine par "?", fin du tour.
  Le mot "exercer" est traduit par "exercer".
4. Lisez les documents de transport de Pipecat.
  Le mot "exercer" est traduit par "exercer".
5. Mesurer une cascade OpenAI en temps réel par rapport à STT+LLM+TTS sur la même requête. Quel coût de latence le contrôle au niveau du texte implique-t-il ?
  Le mot "exercer" est traduit par "exercer".

## Les termes clés

| Term | What people say | What it actually means |
|------|----------------|------------------------|---|
| Frame | "Event" | Typed unit of data in the pipeline (audio, transcript, text, control) |  |
| Processor | "Pipeline stage" | Handler with process(frame) |  |
| DOWNSTREAM | "Forward flow" | Source to sink: audio in, speech out |  |
| UPSTREAM | "Feedback flow" | Control: cancel, metrics, barge-in |  |
| VAD | "Voice activity detection" | Detects when user is speaking |  |
| Semantic turn detection | "Smart end-of-turn" | Model-based decision that the user is done |  |
| MultimodalAgent | "Direct audio agent" | Audio in, audio out; no text in the middle |  |
| VoicePipelineAgent | "Cascade agent" | STT + LLM + TTS; text-level control |  |

## Encore une lecture

- [Pipecat docs](https://docs.pipecat.ai/getting-started/introduction) pipeline à base de cadres, transformateurs, transports
  Le mot "réfléchisseur" est traduit par "réfléchisseur".
- [LiveKit Agents docs](https://docs.livekit.io/agents/) WebRTC + voix primitives
  Le mot "réfléchisseur" est traduit par "réfléchisseur".
- [Vapi](https://vapi.ai/) plateforme vocale gérée
  Le mot "réfléchisseur" est traduit par "réfléchisseur".
- [Retell AI](https://www.retellai.com/) voix gérée, marquée par la latence
  Le mot "réfléchisseur" est traduit par "réfléchisseur".
