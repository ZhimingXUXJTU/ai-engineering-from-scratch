# En streaming Discours à Discours  Moshi, Hibiki, et le dialogue complet à double emploi  流式语音到语音  Moshi、Hibiki et全双工对话

> En 2024, il a redéfini l'IA vocale. Moshi envoie un modèle unique qui écoute et parle simultanément à 200 ms de latence. Hibiki fait la traduction de la parole à la parole pièce par pièce. Les deux abandonnent le pipeline ASR → LLM → TTS pour une architecture unifiée à double double double sur les jetons de codec Mimi.

> **【中文解读】**2024-2026 année de redéfinition du langage AI。Moshi utilisant un seul modèle dans 200ms 延迟内同时听和说。Hibiki 逐块进行语音到语音翻译。 les deux ont abandonné ASR→LLM→TTS 流水线, en adoptant l'ensemble des architectures basées sur les jetons Mimi 编解码器。 c'est un nouveau design de référence。

> **【拓展：全双工语音 AI】**L'assistant de la langue traditionnelle est " demi-double " (à l'écoute du temps ne peut pas dire), le Mochi a réalisé " plein double " (à l'écoute du temps), comme dans le dialogue naturel humain.

**Type:** Learn | **类型:** 学习
**Languages:** Python | **语言:** Python
**Prerequisites:** Phase 6 · 13 (Neural Audio Codecs), Phase 6 · 11 (Real-Time Audio), Phase 7 · 05 (Full Transformer) | **前置知识:** 阶段 6 · 13（神经音频编解码器），阶段 6 · 11（实时音频），阶段 7 · 05（完整 Transformer）
**Time:** ~75 minutes | **预计用时:** ~75 分钟

## Le problème , l' introduction du problème

Chaque agent vocal construit à partir des leçons 11 + 12 a un plancher de latence fondamental autour de 300-500 ms: incendies VAD, processus STT, raisons LLM, générations TTS. Chaque étape a sa propre latence minimale. Vous pouvez régler et paralléliser, mais la forme du pipeline vous coupe.

> 基于第11和12 课程构建的每个语音助手都有一个约300-500 ms的基础延迟下限:VAD 触发、STT 处理、LLM 推理、TTS 生成──每个阶段都有自己的最小延迟──你可以调优和并行化,但流水线架构本身限制你──

> **【中文解读】**La question posée dans ce chapitre est la suivante: comment comprendre et appliquer correctement cette technique dans la conception pratique. Comprendre le contexte de la question aide à saisir les principaux facteurs de décision concernant le type de technologie. Dans les systèmes d'IA réels, le type de technique erroné coûte souvent plus cher que le coût de la mise en œuvre de détails.


Moshi (Kyutai, 2024-2026) pose une autre question: et si il n'y a pas de pipeline ?

> Moshi [Kyutai, 2024-2026) pose une question différente: si il n'y a pas de ligne de flux d'eau? si un modèle directement 持续地接收音频输入并输出音频,文本只是中间的内心独白而不是必要阶段?

La réponse est:**full-duplex speech-to-speech**La latence théorique est de 160 ms (80 ms Mimi frame + 80 ms retard acoustique) et la latence pratique de 200 ms sur un seul GPU L4.

> La réponse est:**全双工语音到语音**△ théorique retard de 160 ms(80 ms Mimi  + 80 ms 声学延迟) ・・・ 在单张 L4 GPU 上实际延迟 200 ms──这是最好的流水线语音助手延迟的一半──

## Le concept de base.

> **【中文解读】**Le présent article présente les concepts et les bases théoriques de base. La connaissance de ces concepts est la prémisse de la réalisation de la réalisation de la réalisation, mais aussi le point de connaissance de l'interview et de la pratique de l'ingénierie.


![Moshi architecture: two parallel Mimi streams + inner-monologue text](../assets/moshi-hibiki.svg)

### L'architecture de Moshi

> Mochi 架构

**Inputs.**Deux flux de codecs Mimi, tous deux à 12,5 Hz × 8 livres de code:

> **输入。**两个 Mimi 编解码器流, moyenne de 12,5 Hz × 8 个码本:

- Stream 1: audio utilisateur (mimi-encodé, toujours en arrière)
  Le nombre de personnes qui ont accès à l'appareil est de 5 000 personnes.
- Stream 2: audio de Moshi (géré par Moshi)
  Le mot "Moshi" est traduit par "Moshi" (Moshi)

**The transformer.**Un transformateur temporel de paramètre 7B traite les flux et un flux de texte "monologue interne".

> **Transformer。**Un transformateur de temps de 70 milliards de paramètres traite simultanément deux flux et un flux de texte "in-the-art" dans chaque phase de temps de 80 ms, il:

1. Consomme les derniers jetons Mimi utilisateur (8 livres de code).
   Le code de la page est le code de la page de la page de la page de la page de la page de la page de la page de la page de la page de la page de la page de la page de la page de la page de la page de la page de la page de la page de la page de la page de la page de la page de la page de la page de la page de la page de la page de la page de la page de la page de la page de la page de la page de la page de la page de la page de la page de la page de la page de la page de la page de la page de la page de la page de la page de la page de la page de la page de la page de la page de la page de la page de la page de la page de la page de la page de la page de la page de la page de la page de la page de la page de la page de la page de la page de la page de la page de la page de la page de la page de la page de la page de la page de la page de la page de la page de la page de la page de la page de la page de la page de la page de la page de la page de la page de la page de la page de la page de la page de la page de la page de la page de la page de la page de la page de la page de la page de la page de la page de la page de la page de la page de la page de la page de la page de la page de la page de la page de la page de la page de la page de la page de la page de la page de la page de la page de la page de la page de la page de la page de la page de la page de la page de la page de la page de la page de la page de la page de la page de la page de la page de la page de la page de la page de la page de la page de la page de la page de la page de la page de la page de la page de la page de la page de la page de la page de la page de la page de la page de la page de la page de la page de la page de la page de la page de la page de la page de la page de la page de de la page de la page de de de la page de la page de la page de la page de de de la
2. Consomme les plus récents jetons de Moshi Mimi (8 livres de code, tel que produit).
   Le mot "Moshi Mimi" est traduit par "Moshi Mimi".
3. Génère le prochain jeton de texte Moshi (monologue interne).
   Le mot "Moshi" est traduit par "Moshi".
4. Génère les prochains jetons de Moshi Mimi (8 livres de code via un petit transformateur de profondeur).
   Le code de la ligne de référence est le code de la ligne de référence.

Les trois flux  audio utilisateur, audio Moshi, texte Moshi  fonctionnent en parallèle. Moshi peut entendre l'utilisateur en parlant; peut s'interrompre lorsqu'il interrompt; peut revenir en arrière ("mhm") sans rompre son énoncé principal.

> Les utilisateurs peuvent écouter les utilisateurs en même temps qu'ils parlent, se désabonner lorsqu'ils se cassent, se contrer sans perturber les principales déclarations.

**The depth transformer.**Dans un cadre, les 8 codebooks ne sont pas prédits en parallèle  ils ont des dépendances inter-codebooks. Un petit "transformateur de profondeur" de 2 couches les prédit séquentiellement dans un délai de 80 ms. C'est la facteurisation standard pour les LM codec AR (également utilisée par VALL-E, VibeVoice).

> **深度 Transformer。**Dans un 内, 8 codes ne sont pas en phase avec la prédiction de  entre eux il existe un code  entre elles dépendent. Un petit " transformateur de profondeur " de 2 niveaux les prévoit en séquence à 80 ms. C'est la méthode standard de prédiction du modèle de langage de code de l'auto-référencement.

### Pourquoi le texte du monologue interne est utile

Sans texte explicite, le modèle doit implicitement modéliser le langage dans son flux acoustique. L'idée de Moshi: forcer l'émetteur à émettre des jetons de texte à côté de l'audio. Le flux de texte est essentiellement la transcription de ce que Moshi dit. Cela améliore la cohérence sémantique, facilite l'échange d'une tête de modèle de langage et vous donne des transcriptions gratuitement.

> Pourquoi le texte unique à l'intérieur aide: il n'y a pas de texte explicite, le modèle doit être dans le flux sonore dans le cadre du modèle de construction de langage.

### Hibiki: traduction en streaming de la langue à la langue

La même architecture, formée sur des paires de traductions. L'audio source est entré, l'audio de la langue cible est sorti, en continu. Hibiki-Zero (février 2026) élimine le besoin de données de formation alignées au niveau du mot  utilise des données au niveau de la phrase + GRPO renforcement de l'apprentissage pour l'optimisation de la latence.

> Hibiki:流式语音到语音翻译──相同架构,使用翻译对训练──源语言音频输入,目标语言音频输出,持续进行──Hibiki-Zero(2026年 2月) a éliminé la demande de données pour les classes de mots et les classes de formation l'utilisation de données pour les classes de mots + GRPO 强化学习进行延迟优化──

Quatre paires de langues prises en charge initialement; peut être adapté à une nouvelle langue avec ≈1000 heures.

> Initiellement, il est compatible avec quatre langues; il peut être utilisé avec environ 1000 heures de données pour s'adapter à de nouvelles langues.

### La pile de Kyutai plus large (2026)

> 更广泛的 Kyutai 技术(2026 年)

- **Moshi** dialogue à double sens (d'abord en français, bien accompagné en anglais)
  Le mot français est traduit en français par "Moshi" (en français: Moshi)
- **Hibiki / Hibiki-Zero** traduction simultanée du langage
  Hébreu: hébreu: hébreu: hébreu: hébreu: hébreu: hébreu: hébreu: hébreu: hébreu: hébreu: hébreu: hébreu: hébreu: hébreu: hébreu: hébreu: hébreu: hébreu: hébreu: hébreu: hébreu: hébreu: hébreu: hébreu: hébreu: hébreu: hébreu: hébreu: hébreu: hébreu: hébreu: hébreu: hébreu: hébreu: hébreu: hébreu: hébreu: hébreu: hébreu: hébreu: hébreu: hébreu: hébreu: hébreu: hébreu: hébreu: hébreu: hébreu: hébreu: hébreu: hébreu: hébreu: hébreu: hébreu: hébreu: hébreu: hébreu: hébreu: hébreu: hébreu: hébreu: hébreu: hébreu: hébreu: hébreu: hébreu: hébreu: hébreu: hébreu: hébreu: hébreu: hébreu: hébreu: hébreu: hébreu: hébreu: hébreu: hébreu: hébreu: hébreu: hébreu: hébreu: hébreu: hébreu: hébreu: hébreu: hébreu: hébreu: hébreu: hébreu: hébreu: hébreu: hébreu: hébreu: hébreu: hébreu: hébreu: hébreu: hébreu: hébreu: hébreu: hébreu: hébreu: hébreu: hébreu: hébreu: hébreu: hébreu: hébreu: hébreu: hébreu: hébreu: hébreu: hébreu: hébreu: hébreu: hébreu: hébreu: hébreu: hébreu: hébreu: hébreu: hébreu: hébreu: hébreu: hébreu: hébreu: hébreu: hébreu: hébreu: hébreu: hébreu: hébreu: hébreu: hébreu: hébreu: hébreu: hébreu: hébreu: hébreu: hébreu: hébreu: hébreu: hébreu: hébreu: hébreu: hébreu: hébreu: hébreu: hébreu: hébreu: hébreu: hébreu: hébreu: hébreu: hébreu: hébreu: hébreu: hébreu: hébreu: hébreu: hébreu: hébreu: hébreu: hébreu: hébreu: hébreu: hébreu: hébreu:
- **Kyutai STT** RAS de streaming (500 ms ou 2,5 s regardant vers l'avant)
  Le mot de passe est le mot de passe de la langue chinoise.
- **Kyutai Pocket TTS** TTS de 100 M param fonctionne sur CPU (janvier 2026)
  Le TTS de poche de Kyūtai est de 1 milliard de TTS, disponible sur le CPU.
- **Unmute** un pipeline complet combinant ces services sur des serveurs publics
  Unité de l'eau en ligne complète

Débit sur un GPU L40S: 64 sessions simultanées en temps réel 3x.

> Le GPU L40S a une capacité de 64 bits, 3 fois la vitesse réelle.

### Le CSM de sésame  le cousin

Sesame CSM (2025) utilise une idée similaire  une colonne vertébrale Llama-3 avec une tête de codec Mimi. Mais CSM est unidirectionnel (prend le contexte + texte, produit la parole) plutôt que du double. C'est le meilleur TTS "présence vocale" sur le marché; pas tout à fait le même que la capacité du double complet de Moshi.

> Sesame CSM (en 2025) utilise une idée similaire à celle de Llama-3 骨干网络 + Mimi 编解码器头── mais le CSM est un simple système de réception de texte + texte, générant des voix), et non un tout-ensemble de la production.

### Numéros de performance 2026

| Model | Latency | Use case | License |
|-------|---------|----------|---------|
| Moshi | 200 ms (L4) | full-duplex English / French dialogue / 全双工英/法对话 | CC-BY 4.0 |
| Hibiki | 12.5 Hz framerate | French ↔ English streaming translation / 法↔英流式翻译 | CC-BY 4.0 |
| Hibiki-Zero | same | 5 language-pairs, no aligned data / 5 语言对，无需对齐数据 | CC-BY 4.0 |
| Sesame CSM-1B | 200 ms TTFA | context-conditioned TTS / 上下文条件 TTS | Apache-2.0 |
| GPT-4o Realtime | ~300 ms | closed, OpenAI API / 闭源，OpenAI API | commercial |
| Gemini 2.5 Live | ~350 ms | closed, Google API / 闭源，Google API | commercial |

> **【中文解读】**Cette méthode "de zéro" peut aider à comprendre le principe derrière le cadre, en cas de problème, ne sera pas bloqué dans une boîte noire.

> **【拓展：语音 AI 的产品化】**La technologie du langage est confrontée à des défis particuliers dans la fabrication de produits: différents sons, bruits de fond, prises de vue, nombreux discours, etc. Les produits de Siri, Alexa, et de petite enfance ont été largement optimisés pour résoudre ces "problèmes de longue durée".

> **【拓展：多语言语音技术】**Les caractéristiques du langage mondial sont énormes: la voix de la langue (en chinois comme en chinois) est à un niveau élevé, les ressources linguistiques sont faibles et les données de formation manquent.




## Construisez-le et mettez-le en œuvre.
```figure
sp-fullduplex
```

## Faites-le

### Étape 1: l'interface

> 步骤 1: accès

Moshi expose un serveur WebSocket qui prend 80 ms de musique codée par Mimi et renvoie 80 ms de musique codée par Mimi.

> Moshi  expose un WebSocket  serveur, reçoit 80 ms de Mimi 编码音频块并返回 80 ms de Mimi 编码音频块──双向,持续进行──

```python
import asyncio
import websockets
from moshi.client_utils import encode_audio_mimi, decode_audio_mimi

async def moshi_chat():
    async with websockets.connect("ws://localhost:8998/api/chat") as ws:
        mic_task = asyncio.create_task(stream_mic_to(ws))
        spk_task = asyncio.create_task(stream_from_to_speaker(ws))
        await asyncio.gather(mic_task, spk_task)
```

### Étape 2: boucle à double double

> 步骤 2: cycle de travail complet

```python
async def stream_mic_to(ws):
    async for chunk_80ms in mic_stream_at_12_5_hz():
        mimi_tokens = encode_audio_mimi(chunk_80ms)
        await ws.send(serialize(mimi_tokens))

async def stream_from_to_speaker(ws):
    async for msg in ws:
        mimi_tokens, text_token = deserialize(msg)
        audio = decode_audio_mimi(mimi_tokens)
        await play(audio)
```

Les deux directions fonctionnent simultanément. Python asyncio ou Rust futures sont le transport standard.

> Les futures de Python sont des méthodes de transmission standard.

### Étape 3: objectif de formation (conceptuel)

> 步骤 3: entraînement objectif

Pour chaque image de 80 ms `t`- Le numéro de la liste:

> Pour chaque 80 ms`t`- Le numéro de la liste:

- Enregistrement: `user_mimi[0..t]`- Je suis là .`moshi_mimi[0..t-1]`- Je suis là .`moshi_text[0..t-1]`
  En anglais, le mot "port" est traduit par "port":`user_mimi[0..t]`- Je suis là.`moshi_mimi[0..t-1]`- Je suis là.`moshi_text[0..t-1]`
- Prédit: `moshi_text[t]`Alors ...`moshi_mimi[t, codebook_0..7]`
  Le mot " prédiction " signifie " prédiction ".`moshi_text[t]`, puis c' est`moshi_mimi[t, codebook_0..7]`

Le texte est prédit avant l'audio (monologue interne); l'audio est prédit séquentiel en codebook dans le transformateur de profondeur.

> 文本在音频之前预测(内心独白);音频在深度 Transformer 内按码本顺序预测。

### Étape 4: où Moshi gagne et où il ne gagne pas

> 步骤 4: Les avantages et les inconvénients de Moshi

Moshi gagne:

> Les avantages de Moshi:

- Sub-250 ms de bout en bout sur du matériel bon marché.
  Traduction anglaise: en bas de 250 ms.
- Des retrovisons naturelles et des interruptions.
  Traduction anglaise: naturel de l'esprit et de la force de la nature.
- Pas de code de colle pour pipeline.
  Le mot "eau" est traduit par "eau".

Moshi ne gagne pas:

> Les défauts de Moshi:

- Appel à l'outil (pas formé pour cela; vous avez besoin d'un parcours de LLM séparé).
  Le programme de formation est basé sur la formation de la formation professionnelle.
- Le raisonnement long (Moshi est un modèle de dialogue 8B, pas Claude/GPT-4).
  Le modèle de dialogue de Moshi est d'environ 80 milliards de dollars, pas Claude/GPT-4)
- Accuracité factuelle sur des sujets de niche.
  Le sujet de la question est le fait de la réalité.
- La plupart des cas d'utilisation dans les entreprises de production (les pipelines sont toujours utilisées en 2026).
  La plupart des entreprises de production utilisent encore la ligne de production en 2026.

> **【中文解读】**Dans ce chapitre, nous allons montrer comment utiliser un cadre mature (comme PyTorch, HuggingFace, etc.) pour appliquer rapidement cette technique.





> **【拓展：语音与情感计算】**Le langage n'est pas seulement un moyen de transmettre des informations, il est également un moyen de transmettre des signaux émotionnels riches.

## Utilisez-le avec le cadre de réalisation

| Situation | Pick |
|-----------|------|
| Lowest-latency voice companion / 最低延迟语音伴侣 | Moshi |
| Live translation call / 实时翻译通话 | Hibiki |
| Voice demo / research / 语音演示/研究 | Moshi, CSM |
| Enterprise agent with tools / 企业级带工具的 agent | Pipeline（第 12 课），不是 Moshi |
| Custom-voice TTS in context / 上下文中的自定义音色 TTS | Sesame CSM |
| Speech-to-speech, any languages / 任意语言的语音到语音 | GPT-4o Realtime 或 Gemini 2.5 Live（商业） |



## Les pièges

> 常见陷

- **Limited tool calling.**Moshi est un modèle de dialogue, pas un cadre d'agent.
  Le mot grec traduit par " le mot grec "**有限的工具调用。**Moshi est un modèle de dialogue, pas un agent 框架.
- **Specific-voice conditioning.**Moshi utilise un seul personnage formé; le clonage est une sélection d'entraînement séparée.
  Le mot grec traduit par " le mot grec "**特定语音调节。**Moshi utilise un seul entraînement personnel; Klon nécessite un processus d'entraînement séparé.
- **Language coverage.**Le français + l'anglais est excellent, d'autres sont limités. Hibiki-Zero aide, mais vous avez toujours besoin de données de formation.
  Le mot grec traduit par " le mot grec "**语言覆盖。**Français + Anglais; Autres langues limitées.
- **Resource cost.**Une session Moshi complète contient une fente GPU; pas un modèle de déploiement partagé par les locataires bon marché.
  Le mot grec traduit par " le mot grec "**资源成本。**Un déploiement de locations partagées est un processus de déploiement de locations partagées.

> **【中文解读】**Cette section se concentre sur la façon de déployer le modèle en tant que produit disponible. De l'original au système de production, il faut considérer plusieurs dimensions de l'optimisation des performances, du traitement des erreurs, du contrôle, etc.


## Envoyez-le . Produit .

- Je ne sais pas .`outputs/skill-duplex-pipeline.md`Choisissez pipeline versus architecture double pour une charge de travail d'agent vocal, avec raison.

> 保存为 `outputs/skill-duplex-pipeline.md`◊ Pour un assistant de travail de langue, le choix de la ligne de transport ou de l'ensemble de l'architecture,并说明理由──

## Les exercices

1. **Easy.**On court .`code/main.py`Il simule symboliquement l'architecture à deux courants + monologue interne.
   Le mot grec traduit par " le mot grec "**简单。**运行  référencement`code/main.py`Il est en mode symbolique, il est en double flux + en interne.
2. **Medium.**Tirez Moshi de HuggingFace, exécutez le serveur, testez une conversation, mesurez la latence de l'horloge murale de la fin de la conversation à la réponse de Moshi.
   Le mot grec traduit par " le mot grec "**中等。**Depuis HuggingFace 拉取 Moshi,运行服务器,测试一段对话──测量 depuis le bout du langage utilisateur jusqu'à la fin du langage utilisateur.
3. **Hard.**Prenez votre agent de pipeline de leçon 12 et comparez la latence P50 vs Moshi sur 20 déclarations de test correspondantes.
   Le mot grec traduit par " le mot grec "**困难。**Utilisez le 12ème cours de l'assistant de la ligne de débit avec Moshi en 20 articles de correspondance test

> **【中文解读】**Dans le tableau des termes, la définition du terme "ce que les gens disent" et "ce qu'il signifie réellement" est différenciée entre le langage quotidien et la signification technique précise.


## Les termes clés

| Term | What people say | What it actually means |
|------|-----------------|-----------------------|
| Full-duplex | Hear-and-speak at once | Two audio streams active simultaneously on the same model. / 同一模型同时维护两条音频流 |
| Inner monologue | Model's text stream | Moshi emits text tokens alongside its audio output. / Moshi 在音频输出同时输出文本 token |
| Depth transformer | Inter-codebook predictor | Small transformer that predicts 8 codebooks within one 80 ms frame. / 在一个 80 ms 帧内预测 8 个码本的小型 Transformer |
| Mimi | Kyutai's codec | 12.5 Hz × 8 codebooks; semantic+acoustic; powers Moshi. / 12.5 Hz × 8 码本；语义+声学；驱动 Moshi |
| Streaming S2S | Audio → audio live | Chunk-by-chunk translation/dialogue, no pipeline stages. / 逐块翻译/对话，无流水线阶段 |
| Back-channeling | "Mhm" reactions | Moshi can emit small acknowledgments without breaking its turn. / Moshi 可发出小反馈而不打断自己的轮次 |

> **【中文解读】**延伸阅读 fournit des ressources de haute qualité pour l'apprentissage en profondeur. Ces articles et cours sont des références classiques dans ce domaine, adaptés aux lecteurs qui ont besoin d'une compréhension approfondie.


## Encore une lecture

- [Défossez et al. (2024). Moshi — speech-text foundation model](https://arxiv.org/html/2410.00037v2)- Le journal.
  Défossez 等(2024). Moshi语音-文本基础模型原始论文──
- [Kyutai Labs (2026). Hibiki-Zero](https://arxiv.org/abs/2602.12345) Translation en streaming sans données alignées.
  Hibiki-Zero无需对齐数据的流式翻译──
- [Sesame (2025). Crossing the uncanny valley of voice](https://www.sesame.com/research/crossing_the_uncanny_valley_of_voice) Spécifications du MCS.
  Sesame (en anglais) 跨越语音的恐怖谷CSM 规范──
- [Kyutai — Moshi repo](https://github.com/kyutai-labs/moshi) installer + serveur.
  KyutaiMoshi  entrepôt安装 + 服务器。
- [OpenAI — Realtime API](https://platform.openai.com/docs/guides/realtime) parité commerciale fermée.
  L'opération de réalisation de l'activité de l'entreprise
- [Kyutai — Delayed Streams Modeling](https://github.com/kyutai-labs/delayed-streams-modeling) le cadre STT/TTS sous le capot.
  KyutaiDelayed Streams Modelingbasement STT/TTS 框架。

> **【中文解读】**延伸阅读 a fourni des ressources de haute qualité pour l'apprentissage en profondeur, y compris des articles, des cours et des outils.

