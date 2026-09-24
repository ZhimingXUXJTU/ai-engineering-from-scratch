# Construire un pipeline d'assistants vocaux La phase 6 Capstone

> Toutes les leçons du 1er au 11e, cousues ensemble. Construisez un assistant vocal qui écoute, raisonne et parle. En 2026, c'est un problème d'ingénierie résolu, pas un problème de recherche  mais les détails d'intégration décident si cela se produit.

> **【中文解读】**Mettre en ligne tout ce qui est contenu dans les cours, construire un assistant de parole capable de penser et de parler.

**Type:** Build | **类型:** 构建
**Languages:** Python | **语言:** Python
**Prerequisites:** Phase 6 · 04, 05, 06, 07, 11; Phase 11 · 09 (Function Calling); Phase 14 · 01 (Agent Loop) | **前置知识:** 阶段 6 · 04、05、06、07、11；阶段 11 · 09（函数调用）；阶段 14 · 01（智能体循环）
**Time:** ~120 minutes | **预计用时:** ~120 分钟

## Le problème , l' introduction du problème

Construire un assistant de bout en bout:

> Construire un assistant de bout en bout:

> **【中文解读】**La question posée dans ce chapitre est la suivante: comment comprendre et appliquer correctement cette technique dans la conception pratique. Comprendre le contexte de la question aide à saisir les principaux facteurs de décision concernant le type de technologie. Dans les systèmes d'IA réels, le type de technique erroné coûte souvent plus cher que le coût de la mise en œuvre de détails.

1. Capture de l'entrée de micro (16 kHz mono).
   - Je suis en train de faire une pause.
2. Détecte le début et la fin de la parole de l'utilisateur.
   检测用户语音的开始/结束──
3. Il transcrit le streaming.
   - Je suis en train de faire un tour.
4. Passe la transcription à un LLM qui peut appeler des outils (timer, météo, calendrier).
   Il sera transféré à l'équipe de formation de l'équipe de formation de l'équipe de formation de l'équipe de formation de l'équipe de formation de l'équipe de formation de l'équipe de formation de l'équipe de formation de l'équipe de formation de l'équipe de formation de l'équipe de formation de l'équipe de formation de l'équipe de formation de l'équipe de formation de l'équipe de formation de l'équipe de formation de l'équipe de formation de l'équipe de formation de l'équipe de formation de l'équipe de formation de l'équipe de formation de l'équipe de formation de l'équipe de formation de formation de l'équipe de formation de l'équipe de formation de formation de l'équipe de formation de formation de l'équipe de formation de l'équipe de formation de formation de l'équipe de formation de formation.
5. Il transmet un texte de LLM à un TTS.
   Le programme de formation en droit est transmis à TTS.
6. Reproduit l'audio à l'utilisateur.
   À l'utilisateur
7. Arrête si l'utilisateur interrompt la réponse en milieu.
   Si l'utilisateur se déconnecte dans la réponse, il s'arrête.

Objectif de latence: premier octet audio TTS dans les 800 ms de l'utilisateur terminant sa déclaration sur un processeur de ordinateur portable. Objectif de qualité: aucun mot manqué, aucun sous-titre halluciné sur le silence, aucune fuite de clonage vocale, aucun succès d'injection rapide.

> 延迟目标: 延迟目标: 延迟目标: 延迟目标: 延迟目标: 延迟目标: 延迟目标: 延迟目标: 延迟目标: 延迟目标: 延迟目标: 延迟目标: 延迟目标: 延迟目标: 延迟目标: 延迟目标: 延迟目标: 延迟目标: 延迟目标: 延迟目标: 延迟目标: 延迟词: 延迟词: 延迟词: 延迟词: 延迟词: 延迟词: 延迟词: 延迟词: 延迟词: 延迟词: 延迟词: 延迟词: 延迟词: 延迟词: 延迟词: 延迟词: 延迟词: 延迟词: 延迟词: 延迟词: 延迟词: 延迟词: 延迟词: 延迟词: 延迟词: 延迟词: 延迟词: 延迟词: 延迟词: 延迟词: 延迟词: 延迟词: 延迟词: 延迟词: 延迟

## Le concept de base.

> **【中文解读】**Le présent article présente les concepts et les bases théoriques de base. La connaissance de ces concepts est la prémisse de la réalisation de la réalisation de la réalisation, mais aussi le point de connaissance de l'interview et de la pratique de l'ingénierie.


![Voice assistant pipeline: mic → VAD → STT → LLM+tools → TTS → speaker](../assets/voice-assistant.svg)

### Les sept composantes

1. **Audio capture.**Mic → 16 kHz mono → 20 ms. Généralement `sounddevice`en Python ou en AudioUnit/ALSA/WASAPI natif en production.
   **音频捕获。**麦克风 → 16 kHz 单声道 → 20 ms 块──Python 中通常使用 `sounddevice`, production environnement avec le produit original AudioUnit/ALSA/WASAPI
2. **VAD (Lesson 11).**Silero VAD @ seuil 0,5, min discours 250 ms, silence pendu 500 ms. Signes "début" et "fin".
   **VAD（第 11 课）。**Silero VAD @ 值 0.5, minimum语音 250 ms,静音持续 500 ms──信号"开始"和"结束"──
3. **Streaming STT (Lesson 4-5).**Whisper-streaming, Parakeet-TDT ou Deepgram Nova-3 (API). Transcriptions partielles + finales.
   **流式 STT（第 4-5 课）。**Résumé du film: "C'est un film de la série de télévision américaine".
4. **LLM with tool calling.**GPT-4o / Claude 3.5 / Gemini 2.5 Flash. Schéma JSON pour les outils. Tokens de flux.
   **带工具调用的 LLM。**GPT-4o / Claude 3.5 / Gemini 2.5 Flash──工具的 JSON schema──流式代币──
5. **Streaming TTS (Lesson 7).**Kokoro-82M (ouverture la plus rapide) ou Cartesia Sonic (commercial).
   **流式 TTS（第 7 课）。**Kokoro-82M (TTS) ou Cartesia Sonic (TTS)
6. **Playback.**Le haut-parleur est sorti, le code opus pour les réseaux à faible bande passante.
   **回放。**扬声器输出;低带宽网络用 opus 编码。
7. **Interruption handler.**Si le VAD prend feu pendant la lecture de TTS, arrêtez la lecture, annulez LLM, redémarrez STT.
   **打断处理器。**Si le TTS est diffusé pendant la période de VAD, arrêtez de diffuser, annulez le LLM, redémarrez le STT.

### Les trois modes d'échec que vous allez atteindre

> ### Il y a trois types de défaites que vous rencontrerez.

1. **First-word clip.**Le VAD commence un rythme trop tard, le "hey" de l'utilisateur manque.
   **首词截断。**VAD 启动晚一拍;; user's "" 丢失;;
2. **Mid-response interrupt confusion.**LLM continue de générer après l'interruption de l'utilisateur; l'assistant parle à l'utilisateur.
   **回应中打断混乱。**Utilisateur: L'équipe de formation continue de produire des cours de formation en ligne.
3. **Silence hallucination.**Les sons de "merci de regarder" sur les cadres silencieux.
   **静音幻觉。**Sous-pard dans le silence pré-chauffé 输出 "Merci de vous avoir regardé"

### 2026 stacks de référence de production

| Stack | Latency | License | Notes |
|-------|---------|---------|-------|
| LiveKit + Deepgram + GPT-4o + Cartesia | 350-500 ms | commercial API | Industry default 2026 |
| Pipecat + Whisper-streaming + GPT-4o + Kokoro | 500-800 ms | mostly open | DIY-friendly |
| Moshi (full-duplex) | 200-300 ms | CC-BY 4.0 | Single-model; different architecture, lesson 15 |
| Vapi / Retell (managed) | 300-500 ms | commercial | Fastest to launch; limited customization |
| Whisper.cpp + llama.cpp + Kokoro-ONNX | offline | open | Privacy / edge |

| 技术栈 | 延迟 | 许可 | 备注 |
|--------|------|------|------|
| LiveKit + Deepgram + GPT-4o + Cartesia | 350-500 ms | 商业 API | 2026 行业默认 |
| Pipecat + Whisper-streaming + GPT-4o + Kokoro | 500-800 ms | 多数开源 | DIY 友好 |
| Moshi（全双工） | 200-300 ms | CC-BY 4.0 | 单模型；不同架构，第 15 课 |
| Vapi / Retell（托管） | 300-500 ms | 商业 | 最快上线；定制有限 |
| Whisper.cpp + llama.cpp + Kokoro-ONNX | 离线 | 开源 | 隐私/边缘 |

> **【中文解读】**Cette méthode "de zéro" peut aider à comprendre le principe derrière le cadre, en cas de problème, ne sera pas bloqué dans une boîte noire.

> **【拓展：语音 AI 的产品化】**La technologie du langage est confrontée à des défis particuliers dans la fabrication de produits: différents sons, bruits de fond, prises de vue, nombreux discours, etc. Les produits de Siri, Alexa, et de petite enfance ont été largement optimisés pour résoudre ces "problèmes de longue durée".

> **【拓展：多语言语音技术】**Les caractéristiques du langage mondial sont énormes: la voix de la langue (en chinois comme en chinois) est à un niveau élevé, les ressources linguistiques sont faibles et les données de formation manquent.

> **【拓展：语音隐私与安全】**Les données de la langue contiennent une grande quantité d'informations personnelles confidentielles (en anglais) et sont très fausses (en anglais).





## Construisez-le et mettez-le en œuvre.
```figure
v4-voice-latency
```

## Faites-le

### Étape 1: capture de microphone par déchiquetage (pseudocode)

```python
import sounddevice as sd

def mic_stream(chunk_ms=20, sr=16000):
    q = queue.Queue()
    def cb(indata, frames, time, status):
        q.put(indata.copy().flatten())
    with sd.InputStream(channels=1, samplerate=sr, blocksize=int(sr * chunk_ms/1000), callback=cb):
        while True:
            yield q.get()
```

### Étape 2: Capture de tour à travers le VAD

```python
def capture_turn(stream, vad, pre_roll_ms=300, silence_ms=500):
    buf, pre, triggered = [], collections.deque(maxlen=pre_roll_ms // 20), False
    silent = 0
    for chunk in stream:
        pre.append(chunk)
        if vad(chunk):
            if not triggered:
                buf = list(pre)
                triggered = True
            buf.append(chunk)
            silent = 0
        elif triggered:
            silent += 20
            buf.append(chunk)
            if silent >= silence_ms:
                return b"".join(buf)
```

### Étape 3: diffusion en streaming STT → LLM → TTS

```python
async def turn(audio_bytes):
    transcript = await stt.transcribe(audio_bytes)
    async for token in llm.stream(transcript):
        async for audio in tts.stream(token):
            await speaker.play(audio)
```

### Étape 4: appel à l'outil à l'intérieur de la boucle de LLM

```python
tools = [
    {"name": "get_weather", "parameters": {"location": "string"}},
    {"name": "set_timer", "parameters": {"seconds": "int"}},
]

async for chunk in llm.stream(user_text, tools=tools):
    if chunk.type == "tool_call":
        result = dispatch(chunk.name, chunk.args)
        continue_streaming(result)
    if chunk.type == "text":
        await tts.stream(chunk.text)
```

### Étape 5: manipulation des interruptions

> **【中文解读】**Dans ce chapitre, nous allons montrer comment utiliser un cadre mature (comme PyTorch, HuggingFace, etc.) pour appliquer rapidement cette technique.


```python
tts_task = asyncio.create_task(tts_loop())
while True:
    chunk = await mic.get()
    if vad(chunk):
        tts_task.cancel()
        await speaker.stop()
        await new_turn()
        break
```




> **【拓展：语音与情感计算】**Le langage n'est pas seulement un moyen de transmettre des informations, il est également un moyen de transmettre des signaux émotionnels riches.

## Utilisez-le avec le cadre de réalisation

Regardez !`code/main.py`pour une simulation exécutable qui câble les sept composants avec des modèles de bâton, de sorte que vous pouvez voir la forme du pipeline même sans matériel.

> 参见 `code/main.py`获取可运行的模拟,将七组件用模块连接,无需硬件即可见流水线形状──实际实现时,将模块替换为:

- `silero-vad`(le secteur de l'énergie)`pip install silero-vad`) / VAD 模块
- `deepgram-sdk`ou `openai-whisper`/ 流式 STT
- `openai`(le secteur de l'énergie)`gpt-4o`) ou `anthropic`/ LLM + 工具调用
- `kokoro`ou `cartesia`/ 流式 TTS
- `sounddevice`pour I/O / 音频输入输出



## Les pièges

> 常见陷

- **Logging PII forever.**L'audio à tour complet est une information personnelle dans la plupart des juridictions.
  **永久记录 PII。**完整轮次音频在多数司法管辖区属于PII──30 天保留,静态加密──
- **No barge-in.**Les utilisateurs vont interrompre, votre assistante doit arrêter de parler.
  **没有抢话。**Le utilisateur va se casser. Votre assistant doit arrêter de parler.
- **TTS that blocks.**TTS synchrone bloque la boucle d'événement. Utilisez asynchrony ou un fil séparé.
  **阻塞式 TTS。**Dans le même temps, le TTS est un cycle d'événements de blocage.
- **No tool-call error handling.**Les outils échouent. LLM doit récupérer l'erreur + réessayer une fois, puis dégrader graceusement.
  **没有工具调用错误处理。**Il faut recevoir l'erreur + refaire une fois, puis la mise à niveau.
- **Overzealous hallucination filters.**Le filtre trop long et l'assistant répète "je ne peux pas m'y prendre".
  **过度激进的幻觉过滤。**过度过助手会重复"我帮不了"──过不足则什么都说──在留出集上校准──
- **No wake-word option.**L'écoute est une responsabilité de la vie privée.
  **没有唤醒词选项。**Il est un peu comme un "poursuite" ou "ouverture".

> **【中文解读】**Cette section se concentre sur la façon de déployer le modèle en tant que produit disponible. De l'original au système de production, il faut considérer plusieurs dimensions de l'optimisation des performances, du traitement des erreurs, du contrôle, etc.


## Envoyez-le . Produit .

- Je ne sais pas .`outputs/skill-voice-assistant-architect.md`. Compte tenu des contraintes budgétaires + d'échelle + de langue + de conformité, produire une spécification complète de la pile.

> 保存为 `outputs/skill-voice-assistant-architect.md` Donner un budget + une taille + un langage + un code de la législation, produire une technologie complète  une norme 

## Les exercices

1. **Easy.**On court .`code/main.py`Il simule un tour complet de bout en bout avec des modules de bout et des empreintes par étape de latence.
   **简单。**运行  référencement`code/main.py`模块模拟一个完整轮次端到端并印各阶段延迟──
2. **Medium.**Remplacez le bâton de la STT par un vrai modèle Whisper sur une préenregistrée `.wav`- Mesurer le WER et la latence de bout en bout.
   **中等。**Dans l' annonce`.wav`上用真实 Whisper 模型替换STT 模块──测量 WER 和端到端延迟──
3. **Hard.**Ajouter des appels à outils: mettre en œuvre `get_weather`(toute API) et `set_timer`.Conduire le LLM à travers les outils et vérifier que lorsque l'utilisateur dit "configure un temporiseur de 5 minutes", la bonne fonction s'allume et la réponse orale le confirme.
   **困难。**添加工具调用: réaliser `get_weather`(tout API) et `set_timer` À travers les outils de l'LLM, la vérification lorsque l'utilisateur dit "setting a 5 minutes timer" lorsque la fonction correcte est utilisée.

> **【中文解读】**Dans le tableau des termes, la définition du terme "ce que les gens disent" et "ce qu'il signifie réellement" est différenciée entre le langage quotidien et la signification technique précise.


## Les termes clés

| Term | What people say | What it actually means |
|------|-----------------|-----------------------|
| Turn | A user + assistant round-trip | One VAD-bounded user speech + one LLM-TTS response. |
| Barge-in | Interruption | User speaks while assistant talks; assistant stops. |
| Wake word | "Hey assistant" | Short keyword detector; Porcupine, Snowboy, openWakeWord. |
| End-pointing | Turn ending | VAD + min-silence decision that user has finished. |
| Pre-roll | Pre-speech buffer | Keep 200-400 ms of audio before VAD fires to avoid first-word clip. |
| Tool call | Function invocation | LLM emits JSON; runtime dispatches; result feeds back in-loop. |

| 术语 | 人们常说的 | 实际含义 |
|------|-----------|---------|
| 轮次 | 用户+助手一个来回 | 一次 VAD 界定的用户语音 + 一次 LLM-TTS 回应。 |
| 抢话 | 打断 | 助手说话时用户开口；助手停止。 |
| 唤醒词 | "嘿助手" | 短关键词检测器；Porcupine、Snowboy、openWakeWord。 |
| 端点检测 | 轮次结束 | VAD + 最小静音决策用户已说完。 |
| 预滚 | 语音前缓冲 | 在 VAD 触发前保留 200-400 ms 音频以避免首词截断。 |
| 工具调用 | 函数调用 | LLM 输出 JSON；运行时分发；结果在循环中反馈。 |

> **【中文解读】**延伸阅读 fournit des ressources de haute qualité pour l'apprentissage en profondeur. Ces articles et cours sont des références classiques dans ce domaine, adaptés aux lecteurs qui ont besoin d'une compréhension approfondie.


## Encore une lecture

- [LiveKit — voice agent quickstart](https://docs.livekit.io/agents/) référence au niveau de production.
  LiveKit语音智能体快速入门生产级参考──
- [Pipecat — voice agent examples](https://github.com/pipecat-ai/pipecat) Cadre adapté aux bricolages.
  Pipecat语音智能体示例DIY 友好框架。
- [OpenAI Realtime API](https://platform.openai.com/docs/guides/realtime) le chemin de la voix native géré.
  OpenAI API en temps réel 托管的语音原生路径──
- [Kyutai Moshi](https://github.com/kyutai-labs/moshi) référence à double double (leçon 15).
  Kyutai Moshi 全双工参考(第 15 课) 』
- [Porcupine wake-word](https://picovoice.ai/products/porcupine/)- Le réveil.
  Le porc-poisson
- [Anthropic — tool use guide](https://docs.anthropic.com/en/docs/build-with-claude/tool-use) Appel à la fonction de LLM.
  Les outils utilisés dans les applications de l'application de la loi

> **【中文解读】**延伸阅读 a fourni des ressources de haute qualité pour l'apprentissage en profondeur, y compris des articles, des cours et des outils.

