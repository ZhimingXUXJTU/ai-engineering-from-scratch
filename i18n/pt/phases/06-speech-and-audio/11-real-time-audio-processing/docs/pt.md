# Processamento de áudio em tempo real.

> As pipelines em batch processam um arquivo. As pipelines em tempo real processam os próximos 20 milissegundos antes que os próximos 20 cheguem. Toda IA conversacional, estúdio de transmissão e bot de telefonia vive e morre com este orçamento de latência.

> **【中文解读】**批处理流水线处理文件,实时流水线在下20毫秒到达之前处理完结这20毫秒──每一个对话式AI、广播系统和电话机器人都在这个延迟预算上存活死――实时音频处理是语音AI落地的关键工程挑战──

**Type:** Build | **类型:** 构建
**Languages:** Python | **语言:** Python
**Prerequisites:** Phase 6 · 02 (Spectrograms), Phase 6 · 04 (ASR), Phase 6 · 07 (TTS) | **前置知识:** 阶段 6 · 02（频谱图），阶段 6 · 04（ASR），阶段 6 · 07（TTS）
**Time:** ~75 minutes | **预计用时:** ~75 分钟

## O problema é o problema da introdução

Você quer um assistente de voz que se sinta vivo. A latência de conversas humanas é de ~ 230 ms (silêncio-resposta). Qualquer coisa acima de 500 ms parece robótica; acima de 1500 ms parece quebrado. O orçamento para uma completa **hear → understand → respond → speak**Loop em 2026 é:

> Você quer um assistente de voz "vivo" ― Human Dialogue Round Delay About 230 ms(静音到回应) ― Mais de 500 ms 感觉像机器人; mais de 1500 ms 感觉坏掉―2026 完整的**听 → 理解 → 回应 → 说**O orçamento é:

> **【中文解读】**A questão que se coloca neste capítulo é: como entender e aplicar esta tecnologia de forma correta na engenharia real.

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

Moshi (Kyutai, 2024) obteve 200 ms de duplex completo. GPT-4o-relógio real (2024) relógios ~ 320 ms. Os oleodutos em cascata em 2022 foram enviados a 2500 ms. A melhoria de 10 x veio de três técnicas: (1) streaming em todos os lugares, (2) oleodutos assíncronos com resultados parciais, (3) geração interrompida.

> Moshi(Kyutai,2024) realizou 200 ms 全双工──GPT-4o-realtime(2024) cerca de 320 ms──2022 anos de nível de nível de fluxo de água atrasado 2500 ms──10 倍提升来自三个技术:(1) 全面流式化,(2) 带部分结果的异步流水线,(3) 可中断生成──

## O conceito central.

> **【中文解读】**Este capítulo apresenta os conceitos e teorias fundamentais.


![Streaming audio pipeline with ring buffer, VAD gate, interruption](../assets/real-time.svg)

**Frame / chunk / window.**O áudio em tempo real é transmitido como blocos de tamanho fixo.

> **帧/块/窗口。**实时音频以固定大小的块流动──常见选择:20 ms(16 kHz 下 320 采样点)──下游一切都必须跟上这个节奏──

**Ring buffer.**O filtro de produção escreve novos quadros, o filtro de consumo lê. Impede a alocação no caminho quente. Dimensão ≈ latência máxima × taxa de amostra; um anel de 2 segundos de 16 kHz = 32.000 amostras.

> **环形缓冲区。**固定大小的循环缓冲区──生产者线程写入新,消费者线程读取──防止热路中的内存分配──大小约等于最大延迟 × 采样率;2秒 16 kHz 环形缓冲 = 32.000 采样点──

**VAD (Voice Activity Detection).**Os gates funcionam em baixo fluxo quando ninguém está falando. Silero VAD 4.0 (2024) executa < 1 ms por 30 ms de frame na CPU. `webrtcvad`É a alternativa mais antiga.

> **VAD（语音活动检测）。**无人说话时阻止下游工作──Silero VAD 4.0(2024) em CPU 运行 <1 ms──`webrtcvad`É uma alternativa mais antiga.

**Streaming ASR.**Modelos que emitem transcrições parciais à medida que chega o áudio. Parakeet-CTC-0.6B em modo de streaming (NeMo, 2024) faz 25% WER em 320 ms de latência.

> **流式 ASR。**随音频到达而输出部分转录的模型──Parakeet-CTC-0.6B 流式模式──NeMo,2024) em 320 ms 延迟下达到 2-5% WER──Whisper-Streaming──Macháček 等,2023) irá Whisper 分块实现接近流式的约2秒延迟──

**Interruption.**Quando o usuário fala enquanto o assistente está falando, você deve (a) detectar a barge-in, (b) parar o TTS, (c) descartar o resultado restante do LLM. Tudo isso dentro de 100 ms, ou o usuário percebe o assistente surdo.

> **打断。**Quando o assistente em conversa abre a porta do usuário, você deve (a) verificar o que está sendo falado, (b) parar o TTS, (c) abandonar o restante LLM, (output;; tudo em 100 ms dentro do processo, caso contrário o usuário sente que o assistente é surdo;;

**WebRTC Opus transport.**20 ms de quadros, 48 kHz, bitrate adaptativa 8128 kbps. padrão para navegador e móvel. LiveKit, Daily.co, Pion são as pilhas 2026 para a construção de aplicativos de voz.

> **WebRTC Opus 传输。**20 ms ,48 kHz, taxa de adaptação automática 8-128 kbps。 browser and mobile端标准。LiveKit、Daily.co、Pion é uma tecnologia de construção de aplicações de voz ── em 2026

**Jitter buffer.**Pacotes de rede chegam fora de ordem / atrasado. O buffer jitter reordena e suave; muito pequenas → lacunas audíveis, muito grande → latência. 6080 ms típico.

> **抖动缓冲区。**网络包乱序/迟到到达──动缓冲区重排和平滑;太小 → 可听间隙,太大 → 延迟──典型值 60-80 ms──

### Gotas comuns

> ### 常见陷

- **Thread contention.**Os modelos pesados GIL + do Python podem deixar de usar o fio de áudio. Use uma biblioteca de áudio de chamadas C (dispositivo de áudio, PortAudio) e mantenha o Python fora do caminho quente.
  **线程竞争。**Python GIL + 重模型会使音频线程饥饿──使用 C 回调音频库(sounddevice、PortAudio),让 Python 远离热路径──
- **Sample-rate conversion latency.**A re-sampulação dentro do gasoduto adiciona 520 ms. Ou re-sampulação antecipada ou utilização de um re-sampulador de latência zero (PolyPhase, `soxr_hq`)).
  **采样率转换延迟。**O fluxo de água interna aumenta 5-20 ms.
- **TTS priming.**Mesmo TTS rápido como Kokoro tem um aquecimento de 100200 ms em primeiro pedido. modelo de cache + aquecê-lo com uma jogada de maniquí antes da primeira virada real.
  **TTS 预热。**Mesmo assim como Kokoro, TTS rápido na primeira solicitação também tem 100-200 ms 预热──缓存模型 + na primeira rodada real 前用假运行预热──
- **Echo cancellation.**Sem AEC, a saída TTS re-entrada no microfone e desencadeia ASR na própria voz do bot.
  **回声消除。**没有AEC,TTS 输出重新进入麦克风并触发 ASR 识别机器人自己的声音──WebRTC AEC3 é um código aberto默认方案──

> **【中文解读】**Este é um método de "desde zero" que ajuda a entender o princípio da estrutura, não é um problema que se encontra em uma caixa negra.

> **【拓展：语音 AI 的产品化】**A tecnologia de voz enfrenta desafios únicos na produção: diferentes sons, ruídos de contexto, remoção de chamadas, conversas de pessoas, etc. Os produtos de Siri, Alexa, Pequeno Amor e outros são empregados em grande quantidade de engenharia para resolver esses "problemas de longo prazo".

> **【拓展：多语言语音技术】**As características do som de uma língua mundial são enormes: a alta densidade de voz de uma língua (como o chinês) é de baixa capacidade, a falta de dados de treinamento em linguagem.

> **【拓展：语音隐私与安全】**语音数据 contém uma grande quantidade de informações pessoais de privacidade (→ "faixas") 语音数据包含大量个人隐私信息 (→ "faixas") 语音技术 (→ "faixas") 语音技术 (→ "faixas") 语音技术 (→ "faixas") 语音技术 (→ "faixas") 语音技术 (→ "faixas") 语音技术 (→ "faixas") 语音技术 (→ "faixas") 语音数据 (→ "faixas") 语音技术 (→ "faixas") 语音技术 (→ "faixas") 语音技术 (→ "faixas") 语音技术 (→ "faixas") 语音技术 (→ "faixas") 语音音音水印 (→ "Audio Watermarking") 音纹反欺诈 (→ "Anti-faixas") 音纹) 音反欺诈 (→ "Anti-faixas") 音) 音) 音音是当前研究热点点.





## Construí-lo e realizei-o.
```figure
nyquist-aliasing
```

## Construí-lo

### Passo 1: tampão de anel

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

A capacidade determina a latença máxima de amortecimento. 32.000 amostras a 16 kHz = 2 s.

### Passo 2: Porta de VAD

```python
def simple_energy_vad(frame, threshold=0.01):
    return sum(x * x for x in frame) / len(frame) > threshold ** 2
```

Substituição por Silero VAD em produção:

```python
import torch
vad, _ = torch.hub.load("snakers4/silero-vad", "silero_vad")
is_speech = vad(torch.tensor(frame), 16000).item() > 0.5
```

### Passo 3: streaming de ASR

```python
# Parakeet-CTC-0.6B streaming via NeMo
from nemo.collections.asr.models import EncDecCTCModelBPE
asr = EncDecCTCModelBPE.from_pretrained("nvidia/parakeet-ctc-0.6b")
# chunk_ms=320 ms, look_ahead_ms=80 ms
for chunk in audio_stream():
    partial_text = asr.transcribe_streaming(chunk)
    print(partial_text, end="\r")
```

### Passo 4: Gestor de interrupção

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

> **【中文解读】**Este capítulo mostra como usar um framework maduro (como PyTorch、HuggingFace etc) rápida aplicação desta tecnologia.


Assincroniza-se a I/O e o streaming TTS cancelável.

> Dependendo do I/O e da transferência de transmissão de TTS 流式传输──WebRTC's peerconnection.stop.() 停止音频轨道是标准方式──




> **【拓展：语音与情感计算】**语音 não apenas transmite informações escritas, mas também carrega um rico sinal emocional (语调、语速、音高变化) ◦情感语音识别 (语调、语速、音高变化) ◦情感语音识别 (语音识别, speech emotion recognition, SER) tem uma ampla aplicação em áreas como o controle de qualidade de clientes, a monitorização de saúde mental, a educação inteligente e outras.

## Use-o com o framework implementado.

A pilha de 2026:

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



## Encurralagens

> 常见陷

- **Buffering 500 ms to be safe.**O amortecedor é o teu piso de latência.
  **缓冲 500 ms 求安全。**缓冲区*就是*你的延迟下限──缩小它──
- **Not pinning threads.**Recall de áudio em um fio de prioridade inferior à UI = falhas sob carga.
  **没有绑定线程。**音频回调 低于 UI 优先线程上 = 负载下出现故障──
- **TTS chunks too small.**Os fragmentos sub-200 ms fazem os artefatos do vocoder sonoros. Os fragmentos 320 ms são o ponto ideal.
  **TTS 块太小。**Blocos de menos de 200 ms são o melhor ponto de equilíbrio.
- **No jitter buffer.**As redes reais são nervosas; sem suavizar, você fica com um pop.
  **没有抖动缓冲。**A verdadeira rede tem ação; não há uma escalada de explosões.
- **Single-shot error handling.**Os canais de áudio devem ser resistentes a acidentes.
  **单次错误处理。**O que é que se passa?

> **【中文解读】**Este capítulo se concentra em como o modelo será implantado como produto disponível. De modelo original a nível de produção, os sistemas precisam considerar várias dimensões de otimização de desempenho, tratamento de erros, controle, etc.


## Envia-o . Produto .

Salva como`outputs/skill-realtime-designer.md`- Projetar um canal de áudio em tempo real com orçamentos concretos de latência por etapa.

> 保存为 `outputs/skill-realtime-designer.md`❖ O projeto de cada fase tem um orçamento específico atrasado de real-time

## Exercícios.

1. **Easy.**Corra .`code/main.py`Simula um tampão de anel + energia VAD; Imprime latências de fase para uma corrente falsa de 10 segundos.
   **简单。**运行 `code/main.py`❖模拟环形缓冲区 + 能量 VAD;印印假 10 秒流的各阶段延迟──
2. **Medium.**Usando`sounddevice`, construir um loop que processa o microfone em 20 ms de quadros e imprime estado VAD em cada quadro.
   **中等。**Utilização `sounddevice`Construir um ciclo direto, em 20 ms processar o ar e imprimir o VAD por ano.
3. **Hard.**Construa um teste de eco duplex completo com `aiortc`: browser → WebRTC → Python → WebRTC → browser. Medir latência de vidro a vidro com um pulso de 1 kHz.
   **困难。**- Não .`aiortc`构建全双工回声测试:浏览器 → WebRTC → Python → WebRTC → 浏览器──用 1 kHz 脉冲测量端到端延迟──

> **【中文解读】**No 术语表中的"O que as pessoas dizem" vs "O que realmente significa" 区分日常口语和精确技术含义── em equipe,统一术语定义可以避免大量沟通误解──


## Termos-chave .

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

> **【中文解读】**延伸阅读 fornece recursos de alta qualidade para a aprendizagem profunda.


## Mais leitura 延伸阅读

- [Macháček et al. (2023). Whisper-Streaming](https://arxiv.org/abs/2307.14743)- Um sussurro quase que fluindo.
  Macháček 等 (2023).
- [Kyutai (2024). Moshi](https://kyutai.org/Moshi.pdf) Latência de 200 ms de duplex completo.
  Kyutai (2024). Moshi全双工 200 ms 延迟──
- [LiveKit Agents framework (2024)](https://docs.livekit.io/agents/)- Orquestração de agentes de produção.
  LiveKit Agents 框架(2024) 生产级音频智能体编排──
- [Silero VAD repo](https://github.com/snakers4/silero-vad) sub-1 ms VAD, Apache 2.0.
  Silero VAD  magazinho 亚毫秒 VAD, Apache 2.0
- [WebRTC AEC3 paper](https://webrtc.googlesource.com/src/+/main/modules/audio_processing/aec3/) cancelamento de eco em código aberto.
  WebRTC AEC3 论文开源回声消除──

> **【中文解读】**延伸阅读 forneceu recursos de alta qualidade para a aprendizagem profunda, incluindo artigos, tutoriais e ferramentas.

