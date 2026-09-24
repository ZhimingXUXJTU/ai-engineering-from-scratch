# Traitement audio en temps réel.

> Les pipelines en série traitent un fichier. Les pipelines en temps réel traitent les 20 millisecondes suivantes avant l'arrivée des 20 suivantes. Chaque IA de conversation, studio de diffusion et robot téléphonique vit et meurt avec ce budget de latence.

> **【中文解读】**Le traitement de l'eau en série est effectué en 20 secondes, et le traitement de l'eau en série est effectué en 20 secondes.

**Type:** Build | **类型:** 构建
**Languages:** Python | **语言:** Python
**Prerequisites:** Phase 6 · 02 (Spectrograms), Phase 6 · 04 (ASR), Phase 6 · 07 (TTS) | **前置知识:** 阶段 6 · 02（频谱图），阶段 6 · 04（ASR），阶段 6 · 07（TTS）
**Time:** ~75 minutes | **预计用时:** ~75 分钟

## Le problème , l' introduction du problème

Vous voulez un assistant vocal qui se sent vivant. La latence de prise de tour de conversation humaine est d'environ 230 ms (silence à réponse). Tout ce qui dépasse 500 ms se sent robotique; au-dessus de 1500 ms se sent cassé. Le budget pour une pleine**hear → understand → respond → speak**la boucle en 2026 est:

> Vous voulez un assistant de parole "vivant" ― un assistant de parole humain ⋅ un assistant de dialogue humain ⋅ un assistant de parole humain ⋅ un assistant de parole "vivant" ― un assistant de parole humain ⋅ un assistant de dialogue humain ⋅ un assistant de parole humain ⋅ un assistant de parole humain ⋅ un assistant de parole humain ⋅ un assistant de parole humain ⋅ un assistant de parole humain ⋅ un assistant de parole humain ⋅ un assistant de dialogue humain ⋅ un assistant de dialogue humain ⋅ un assistant de dialogue humain ⋅ un assistant de dialogue humain ⋅ un assistant de dialogue humain ⋅ un assistant de dialogue humain ⋅ un assistant de dialogue humain ⋅ un assistant de dialogue humain ⋅ un assistant de dialogue humain ⋅ un assistant de dialogue humain ⋅ un assistant ⋅ un assistant ⋅ un assistant ⋅ un assistant ⋅ un assistant ⋅ un assistant ⋅ un assistant ⋅ un assistant ⋅ un assistant ⋅ un assistant ⋅ un assistant ⋅ un assistant ⋅ un assistant ⋅ un assistant ⋅ un assistant ⋅ un assistant ⋅ un assistant ⋅ un assistant ⋅ un assistant ⋅ un assistant ⋅ un assistant ⋅ un assistant ⋅ un assistant ⋅ un assistant ⋅ un assistant ⋅ un assistant ⋅ un assistant ⋅ un assistant ⋅ un assistant ⋅ un assistant ⋅ un assistant ⋅ un assistant ⋅ un assistant ⋅ un assistant ⋅ un assistant ⋅ un assistant ⋅ un un assistant ⋅ un un un un assistant ⋅ un un un un ⋅ un ⋅ un un un ⋅ un ⋅ un un ⋅ un ⋅ un ⋅ un ⋅ un ⋅ un ⋅ un ⋅ un ⋅ un ⋅ un ⋅ un ⋅ un ⋅ un ⋅ un ⋅ un ⋅ un ⋅ un ⋅ un ⋅ un ⋅ un ⋅ un ⋅ un ⋅ un ⋅ un ⋅ un ⋅ un ⋅ un ⋅ un ⋅ un ⋅**听 → 理解 → 回应 → 说**Le budget de cycle est:

> **【中文解读】**La question posée dans ce chapitre est la suivante: comment comprendre et appliquer correctement cette technique dans la conception pratique. Comprendre le contexte de la question aide à saisir les principaux facteurs de décision concernant le type de technologie. Dans les systèmes d'IA réels, le type de technique erroné coûte souvent plus cher que le coût de la mise en œuvre de détails.

| Stage | Budget |
|-------|--------|
| Mic → buffer | 20 ms |
| VAD | 10 ms |
| ASR (streaming) | 150 ms |
| LLM (first token) | 100 ms |
| TTS (first chunk) | 100 ms |
| Render → speaker | 20 ms |
| **Total** | **~400 ms** |

| 阶段 | 预算 |
|------|------|
| 麦克风 → 缓冲 | 20 ms |
| VAD | 10 ms |
| ASR（流式） | 150 ms |
| LLM（首 token） | 100 ms |
| TTS（首块） | 100 ms |
| 渲染 → 扬声器 | 20 ms |
| **总计** | **约 400 ms** |

Moshi (Kyutai, 2024) a réalisé 200 ms de double-duplex. GPT-4o en temps réel (2024) montre ~ 320 ms. Les pipelines en cascade en 2022 ont été expédiées à 2500 ms. L'amélioration de 10 fois est venue de trois techniques: (1) streaming partout, (2) pipeline asynchrone avec des résultats partiels, (3) génération interrompue.

> Moshi(Kyutai,2024) a réalisé 200 ms 全双工──GPT-4o-réal-time(2024) environ 320 ms──2022 années de niveau de niveau de flux d'eau retardé 2500 ms──10 fois la progression de trois techniques:

## Le concept de base.

> **【中文解读】**Le présent article présente les concepts et les bases théoriques de base. La connaissance de ces concepts est la prémisse de la réalisation de la réalisation de la réalisation, mais aussi le point de connaissance de l'interview et de la pratique de l'ingénierie.


![Streaming audio pipeline with ring buffer, VAD gate, interruption](../assets/real-time.svg)

**Frame / chunk / window.**Les flux audio en temps réel sont des blocs de taille fixe.

> **帧/块/窗口。**实时音频以固定大小的块流动──常见选择:20 ms(16 kHz 下 320 采样点)──下游一切都必须跟上这个节奏──

**Ring buffer.**Bouffer circulaire de taille fixe. Le fil de producteur écrit de nouveaux cadres, le fil de consommation est lu. empêche l'allocation dans le chemin chaud. Taille ≈ latence maximale × taux d'échantillonnage; un anneau de 2 secondes 16 kHz = 32 000 échantillons.

> **环形缓冲区。**固定大小的循环缓冲区──producteur线程写入新,消费者线程读取──防止热路中的内存分配──大小约等于最大延迟 × 采样率;2秒 16 kHz 环形缓冲 = 32.000 采样点──

**VAD (Voice Activity Detection).**Les portes fonctionnent en aval quand personne ne parle. Silero VAD 4.0 (2024) fonctionne < 1 ms par frame de 30 ms sur CPU. `webrtcvad`est l'alternative plus ancienne.

> **VAD（语音活动检测）。**无人说话时阻止下游工作──Silero VAD 4.0(2024) sur le processeur sur 30 ms 运行 <1 ms──`webrtcvad`C'est une alternative plus ancienne.

**Streaming ASR.**Modèles qui émettent des transcriptions partielles à l'arrivée de l'audio. Parakeet-CTC-0.6B en mode streaming (NeMo, 2024) fait 25% WER à 320 ms de latence.

> **流式 ASR。**Le modèle de transmission de la parakeet-CTC-0.6B est le modèle de transmission de la parakeet-CTC-0.6B (NeMo,2024) qui atteint un retard de 2 à 5% en 320 ms.

**Interruption.**Lorsque l'utilisateur parle pendant que l'assistant parle, vous devez (a) détecter le barge-in, (b) arrêter le TTS, (c) jeter le reste de la sortie LLM. Tout cela dans un délai de 100 ms, ou l'utilisateur perçoit l'assistant sourd.

> **打断。**Lorsque l'assistant dans le langage ouvre la porte à l'utilisateur, vous devez (a) vérifier le langage, (b) arrêter le TTS, (c) abandonner le reste du LLM, (d) le tout à 100 ms, sinon l'assistant se sent sourd.

**WebRTC Opus transport.**20 ms de cadres, 48 kHz, bitrate adaptative 8128 kbps. Standard pour navigateur et mobile. LiveKit, Daily.co, Pion sont les piles 2026 pour la construction d'applications vocales.

> **WebRTC Opus 传输。**20 ms ,48 kHz, taux de mise en œuvre automatique 8-128 kbps。

**Jitter buffer.**Les paquets réseau arrivent en panne / en retard. Le tampon jitter réordonne et se déplace; trop petits → espaces audibles, trop grands → latence. 6080 ms typique.

> **抖动缓冲区。**网络包乱序/迟到达──动缓冲区重排和平滑;太小 → 可听间隙,太大 → 延迟──典型值 60-80 ms──

### Les goutches communes

> ### 常见陷

- **Thread contention.**Les modèles lourds GIL + de Python peuvent affamer le fil audio. Utilisez une bibliothèque audio C-callback (appareil sonore, PortAudio) et gardez Python hors du chemin chaud.
  **线程竞争。**Python GIL + 重模型会使音频线程饥饿──使用 C 回调音频库(sounddevice、PortAudio),让 Python 远离热路径──
- **Sample-rate conversion latency.**Le reéchantillonnage à l'intérieur du pipeline ajoute 520 ms.`soxr_hq`)
  **采样率转换延迟。**L'accélération de la prise de poids à l'intérieur de la ligne de transport est de 5 à 20 ms.
- **TTS priming.**Même un TTS rapide comme Kokoro a un réchauffement de 100 à 200 ms sur première demande.
  **TTS 预热。**Même comme Kokoro, le TTS rapide a également 100-200 ms de préchauffement lors de la première demande.
- **Echo cancellation.**Sans AEC, la sortie TTS rentre dans le micro et déclenche ASR sur la voix du robot.
  **回声消除。**没有AEC,TTS 输出重新进入麦克风并触发 ASR 识别机器人自己的声音──WebRTC AEC3 输出重新进入麦克风并触发 ASR 识别机器人自己的声音──WebRTC AEC3 输出重新进入麦克风并触发 ASR 识别机器人自己的声音──WebRTC AEC3 输出重新输入麦克风并触发 ASR 识别机器人自己的声音──WebRTC AEC3 是开源默认方案──

> **【中文解读】**Cette méthode "de zéro" peut aider à comprendre le principe derrière le cadre, en cas de problème, ne sera pas bloqué dans une boîte noire.

> **【拓展：语音 AI 的产品化】**La technologie du langage est confrontée à des défis particuliers dans la fabrication de produits: différents sons, bruits de fond, prises de vue, nombreux discours, etc. Les produits de Siri, Alexa, et de petite enfance ont été largement optimisés pour résoudre ces "problèmes de longue durée".

> **【拓展：多语言语音技术】**Les caractéristiques du langage mondial sont énormes: la voix de la langue (en chinois comme en chinois) est à un niveau élevé, les ressources linguistiques sont faibles et les données de formation manquent.

> **【拓展：语音隐私与安全】**Les données de la langue contiennent une grande quantité d'informations personnelles confidentielles (en anglais) et sont très fausses (en anglais).





## Construisez-le et mettez-le en œuvre.
```figure
nyquist-aliasing
```

## Faites-le

### Étape 1: tampon à anneaux

```python
import collections

class RingBuffer:
    def __init__(self, capacity):
        self.buf = collections.deque(maxlen=capacity)
    def write(self, frame):
        self.buf.extend(frame)
    def read(self, n):
        return [self.buf.popleft() for _ in range(min(n, len(self.buf)))]
    def level(self):
        return len(self.buf)
```

La capacité détermine la latence maximale du tampon. 32 000 échantillons à 16 kHz = 2 s.

### Étape 2: Porte de détection

```python
def simple_energy_vad(frame, threshold=0.01):
    return sum(x * x for x in frame) / len(frame) > threshold ** 2
```

Remplacez par Silero VAD en production:

```python
import torch
vad, _ = torch.hub.load("snakers4/silero-vad", "silero_vad")
is_speech = vad(torch.tensor(frame), 16000).item() > 0.5
```

### Étape 3: diffusion de l' ASR

```python
# Parakeet-CTC-0.6B streaming via NeMo
from nemo.collections.asr.models import EncDecCTCModelBPE
asr = EncDecCTCModelBPE.from_pretrained("nvidia/parakeet-ctc-0.6b")
# chunk_ms=320 ms, look_ahead_ms=80 ms
for chunk in audio_stream():
    partial_text = asr.transcribe_streaming(chunk)
    print(partial_text, end="\r")
```

### Étape 4: gestionnaire d'interruption

```python
class Dialog:
    def __init__(self):
        self.tts_task = None

    def on_user_speech(self, frame):
        if self.tts_task and not self.tts_task.done():
            self.tts_task.cancel()   # barge-in
        # then feed to streaming ASR

    def on_final_user_utterance(self, text):
        self.tts_task = asyncio.create_task(self.reply(text))

    async def reply(self, text):
        async for tts_chunk in llm_then_tts(text):
            speaker.write(tts_chunk)
```

> **【中文解读】**Dans ce chapitre, nous allons montrer comment utiliser un cadre mature (comme PyTorch, HuggingFace, etc.) pour appliquer rapidement cette technique.


Le lien est en continu avec le réseau TTS.

> En fonction des différents étapes de l'I/O et de la transmission TTS 流式传输──WebRTC's peerconnection.stop() 停止音频轨道是标准方式──




> **【拓展：语音与情感计算】**Le langage n'est pas seulement un moyen de transmettre des informations, il est également un moyen de transmettre des signaux émotionnels riches.

## Utilisez-le avec le cadre de réalisation

La pile de 2026:

| Layer | Pick |
|-------|------|
| Transport | LiveKit (WebRTC) or Pion (Go) |
| VAD | Silero VAD 4.0 |
| Streaming ASR | Parakeet-CTC-0.6B or Whisper-Streaming |
| LLM first-token | Groq, Cerebras, vLLM-streaming |
| Streaming TTS | Kokoro or ElevenLabs Turbo v2.5 |
| Echo cancel | WebRTC AEC3 |
| End-to-end native | OpenAI Realtime API or Moshi |

| 层 | 选择 |
|----|------|
| 传输 | LiveKit（WebRTC）或 Pion（Go） |
| VAD | Silero VAD 4.0 |
| 流式 ASR | Parakeet-CTC-0.6B 或 Whisper-Streaming |
| LLM 首 token | Groq、Cerebras、vLLM-streaming |
| 流式 TTS | Kokoro 或 ElevenLabs Turbo v2.5 |
| 回声消除 | WebRTC AEC3 |
| 端到端原生 | OpenAI Realtime API 或 Moshi |



## Les pièges

> 常见陷

- **Buffering 500 ms to be safe.**Le tampon est votre plancher de latence.
  **缓冲 500 ms 求安全。**Le casse-tête est votre retard.
- **Not pinning threads.**Rappel d'audio sur un fil de priorité inférieure à l'interface utilisateur = défauts sous chargement.
  **没有绑定线程。**音频回调 sur des lignes de priorité inférieure à l'interface utilisateur = 负载出现故障──
- **TTS chunks too small.**Les pièces sous 200 ms rendent audibles les objets du vocoder.
  **TTS 块太小。**Un bloc inférieur à 200 ms est le meilleur point d'équilibre.
- **No jitter buffer.**Les réseaux réels sont nerveux; sans lisser, on se fait des coups.
  **没有抖动缓冲。**Le réel réseau est en mouvement, il n'y a pas de bruit.
- **Single-shot error handling.**Les conduites audio doivent être résistantes aux chocs.
  **单次错误处理。**Il faut résister à l'effondrement.

> **【中文解读】**Cette section se concentre sur la façon de déployer le modèle en tant que produit disponible. De l'original au système de production, il faut considérer plusieurs dimensions de l'optimisation des performances, du traitement des erreurs, du contrôle, etc.


## Envoyez-le . Produit .

- Je ne sais pas .`outputs/skill-realtime-designer.md`- Conception d'un pipeline audio en temps réel avec des budgets concrets de latence par étape.

> 保存为 `outputs/skill-realtime-designer.md`◊ Le projet de chaque étape a un budget spécifique retardé en temps réel.

## Les exercices

1. **Easy.**On court .`code/main.py`Simulation d'un tampon d'anneau + VAD d'énergie; imprime les latences de l'étape pour un faux flux de 10 secondes.
   **简单。**运行  référencement`code/main.py`◊模拟环形缓冲区 + 能量 VAD; imprimer faux 10 secondes de retard de chaque étape du flux
2. **Medium.**En utilisant `sounddevice`, construire un passage à travers la boucle qui traite votre micro en 20 ms cadres et imprime l'état de VAD à chaque cadre.
   **中等。**Utilisation `sounddevice`Construire un cycle direct, en 20 ms de traitement du vent et d'impression par jour en état de VAD.
3. **Hard.**Construisez un test d' écho duplex complet avec `aiortc`: navigateur → WebRTC → Python → WebRTC → navigateur. Mesurer la latence verre à verre avec un pulsation de 1 kHz.
   **困难。**- Je veux le faire .`aiortc`构建全双工回声测试:浏览器 → WebRTC → Python → WebRTC → 浏览器──用 1 kHz 脉冲测量端到端延迟──

> **【中文解读】**Dans le tableau des termes, la définition du terme "ce que les gens disent" et "ce qu'il signifie réellement" est différenciée entre le langage quotidien et la signification technique précise.


## Les termes clés

| Term | What people say | What it actually means |
|------|-----------------|-----------------------|
| Ring buffer | The circular queue | Fixed-size, lock-free (or SPSC-locked) FIFO for audio frames. |
| VAD | Silence gate | Model or heuristic marking speech vs non-speech. |
| Streaming ASR | Real-time STT | Emits partial text as audio arrives; bounded lookahead. |
| Jitter buffer | Network smoother | Queue reordering out-of-order packets; 60–80 ms typical. |
| AEC | Echo cancellation | Subtracts speaker-to-mic feedback path. |
| Barge-in | User interrupt | System detects user speech mid-TTS; must cancel playback. |
| Full duplex | Simultaneous both ways | User and bot can talk at the same time; Moshi is full duplex. |

| 术语 | 人们常说的 | 实际含义 |
|------|-----------|---------|
| 环形缓冲 | 那个循环队列 | 固定大小、无锁（或 SPSC 锁）的音频帧 FIFO。 |
| VAD | 静音门 | 标记语音 vs 非语音的模型或启发式。 |
| 流式 ASR | 实时 STT | 随音频到达输出部分文本；有限前瞻。 |
| 抖动缓冲 | 网络平滑器 | 重排乱序包的队列；典型 60-80 ms。 |
| AEC | 回声消除 | 减去扬声器到麦克风的反馈路径。 |
| 抢话 | 用户打断 | 系统在 TTS 播放中检测用户语音；必须取消播放。 |
| 全双工 | 双向同时 | 用户和机器人可以同时说话；Moshi 是全双工。 |

> **【中文解读】**延伸阅读 fournit des ressources de haute qualité pour l'apprentissage en profondeur. Ces articles et cours sont des références classiques dans ce domaine, adaptés aux lecteurs qui ont besoin d'une compréhension approfondie.


## Encore une lecture

- [Macháček et al. (2023). Whisper-Streaming](https://arxiv.org/abs/2307.14743)- Il y a des morceaux de "Whisper" qui circulent.
  Macháček et similaires (2023).
- [Kyutai (2024). Moshi](https://kyutai.org/Moshi.pdf) La latence de 200 ms à double intégral.
  Kyutai (2024). Moshi全双工 200 ms 延迟──
- [LiveKit Agents framework (2024)](https://docs.livekit.io/agents/) orchestration d'agents audio de production.
  Les agents de LiveKit 框架(2024) 生产级音频智能体编排──
- [Silero VAD repo](https://github.com/snakers4/silero-vad) sous-1 ms VAD, Apache 2.0.
  Silero VAD 仓库 亚毫秒 VAD, Apache 2.0
- [WebRTC AEC3 paper](https://webrtc.googlesource.com/src/+/main/modules/audio_processing/aec3/) annulation de l'écho sous source ouverte.
  Le projet de loi de la Commission sur les droits de l'homme (CEPC) n'a pas été modifié.

> **【中文解读】**延伸阅读 a fourni des ressources de haute qualité pour l'apprentissage en profondeur, y compris des articles, des cours et des outils.

