# Detecção de atividade de voz e tomada de viradas Silero, Cobra e o truque Flush

> Cada agente de voz vive ou morre por duas decisões: o usuário está falando agora e eles terminaram? VAD responde ao primeiro. Detecção de viradas (VAD + silêncio-hangover + modelo de ponto final semântico) responde ao segundo.

> **【中文解读】**Cada assistente de voz é bem sucedido dependendo de dois julgamentos: o usuário agora está falando? o usuário diz terminado?

**Type:** Build | **类型:** 构建
**Languages:** Python | **语言:** Python
**Prerequisites:** Phase 6 · 11 (Real-Time Audio), Phase 6 · 12 (Voice Assistant) | **前置知识:** 阶段 6 · 11（实时音频），阶段 6 · 12（语音助手）
**Time:** ~45 minutes | **预计用时:** ~45 分钟

## O problema é o problema da introdução

Três decisões distintas que um agente de voz toma a cada 20 ms:

> O assistente de voz precisa fazer três julgamentos diferentes em cada bloco de 20 ms:

> **【中文解读】**A questão que se coloca neste capítulo é: como entender e aplicar esta tecnologia de forma correta na engenharia real.


1. **Is this frame speech?**Binário, por quadro.
   Tradução do inglês para o português:
2. **Has the user started a new utterance?** detecção de início.
   Chinese: user has started a new发言?
3. **Has the user finished?** apontamento final (torno final).
   中文翻译:用户说完了吗?端点检测(轮次结束)

A resposta ingênua (ponto de energia) falha em qualquer ruído  tráfego, teclados, babilhões da multidão. A resposta de 2026: Silero VAD (aberto, profundamente aprendido) + um modelo de detecção de virada (indicação semântica final) + uma ressaca de silêncio calibrada por VAD.

> 朴素的答案(能量值) 在任何噪音环境下都会失败交通声、键盘声、人群杂声──2026 年的答案是:Silero VAD(开源、深度学习) + 轮次检测模型(语义端点检测) + VAD 校准的静音持续等──

## O conceito central.

> **【中文解读】**Este capítulo apresenta os conceitos e teorias fundamentais.


![VAD cascade: energy → Silero → turn-detector → flush trick](../assets/vad-turn-taking.svg)

### A cascata de três níveis VAD

> 3o nível de VAD

**Tier 1: energy gate.**O limite RMS é de -40 dBFS, filtra o silêncio óbvio, mas dispara em qualquer ruído acima do limite.

> **第一层：能量门控。**O método mais barato é o RMS                                                                                                                                                                                                                                                           

**Tier 2: Silero VAD**(2020-2026, MIT). 1M parâmetros. Treinado em mais de 6000 idiomas. Executa em ~1 ms por 30 ms por peça em um único fio de CPU. 87,7% TPR em 5% FPR. O código aberto padrão.

> **第二层：Silero VAD**(2020-2026, MIT 许可) ・100.000参数── em 6000+ 种语言上训练── em uma única linha de CPU 块 de 30 ms 约1 ms 推理时间──5% FPR 下 TPR 达 87.7%──开源方案的默认选择──

**Tier 3: semantic turn detector.**O modelo de detecção de turnos do LiveKit (2024-2026) ou seu próprio pequeno classificador.

> **第三层：语义轮次检测器。**O LiveKit é um sistema de teste de rotas de vídeo (Radio) que é usado para fazer a análise de dados de dados.

### Parâmetros-chave e suas definições padrão

> 关键参数 e seu valor de configuração

- **Threshold.**Silero produz uma probabilidade; classifique a fala em &gt; 0,5 (default) ou &gt; 0,3 (sensível). limiar inferior = menos clips de primeira palavra, mais falsos positivos.
  Tradução:**阈值。**Silero 输出概率值;以 > 0.5(默认) ou > 0.3(sensitive模式) 分类语音──值越低 = 首词截断越少,但误报越多──
- **Minimum speech duration.**Rejeitar a fala menor que 250 ms  geralmente tosse ou ruído de cadeira.
  Tradução:**最小语音时长。**拒绝短于250 ms 的语音通常是咳或椅子噪音──
- **Silence hangover (end-pointing).**Depois que o VAD retornar a 0, espere 500-800 ms antes de declarar o fim da rotação.
  Tradução:**静音持续等待（端点检测）。**VAD Volta até 0 后, espere 500-800 ms Reanunciar a sua rota terminar.
- **Pre-roll buffer.**Mantenha 300-500 ms de áudio antes de disparar o VAD.
  Tradução:**预滚缓冲。**Em VAD 触发前保留 300-500 ms 音频──防止""字被截断──

### O truque de flush (Kyutai 2025)

Os modelos STT em streaming têm um atraso de olhar para a frente (500 ms para Kyutai STT-1B, 2,5 segundos para STT-2.6B). Normalmente você esperaria tanto tempo após o fim da fala para a transcrição.**send a flush signal to the STT**O STT processa em 4× em tempo real, então o buffer de 500 ms termina em 125 ms.

> 流式 STT 模型有前视延迟(Kyutai STT-1B é de 500 ms, STT-2.6B é de 2,5 s)  Normalmente você precisa esperar tanto tempo após o término do seu discurso para obter o resultado do seu discurso 刷新技巧: quando o VAD 触发语音结束时,**向 STT 发送刷新信号**, Força imediata de saída;. STT é de cerca de 4 vezes a velocidade de processamento real, por isso 500 ms 缓冲区在约125 ms 内完成──

End-to-end: 125 ms VAD + flush STT = latência de conversação.

> 端到端:125 ms VAD + 刷新 STT = 对话级延迟──

### Comparador de ADV 2026

> 2026 ano VAD

| VAD | TPR @ 5% FPR | Latency | License |
|-----|--------------|---------|---------|
| WebRTC VAD (Google, 2013) | 50.0% | 30 ms | BSD |
| Silero VAD (2020-2026) | 87.7% | ~1 ms | MIT |
| Cobra VAD (Picovoice) | 98.9% | ~1 ms | commercial |
| pyannote segmentation | 95% | ~10 ms | MIT-ish |

Silero é o padrão certo. Cobra é a atualização de conformidade / precisão.

> Silero é uma escolha preferida correta. Cobra é uma escolha de elevação de conformidade/precisação.

> **【中文解读】**Este é um método de "desde zero" que ajuda a entender o princípio da estrutura, não é um problema que se encontra em uma caixa negra.

> **【拓展：语音 AI 的产品化】**A tecnologia de voz enfrenta desafios únicos na produção: diferentes sons, ruídos de contexto, remoção de chamadas, conversas de pessoas, etc. Os produtos de Siri, Alexa, Pequeno Amor e outros são empregados em grande quantidade de engenharia para resolver esses "problemas de longo prazo".

> **【拓展：多语言语音技术】**As características do som de uma língua mundial são enormes: a alta densidade de voz de uma língua (como o chinês) é de baixa capacidade, a falta de dados de treinamento em linguagem.

> **【拓展：语音隐私与安全】**语音数据 contém uma grande quantidade de informações pessoais de privacidade (→ "faixas") 语音数据包含大量个人隐私信息 (→ "faixas") 语音技术 (→ "faixas") 语音技术 (→ "faixas") 语音技术 (→ "faixas") 语音技术 (→ "faixas") 语音技术 (→ "faixas") 语音技术 (→ "faixas") 语音技术 (→ "faixas") 语音数据 (→ "faixas") 语音技术 (→ "faixas") 语音技术 (→ "faixas") 语音技术 (→ "faixas") 语音技术 (→ "faixas") 语音技术 (→ "faixas") 语音音音水印 (→ "Audio Watermarking") 音纹反欺诈 (→ "Anti-faixas") 音纹) 音反欺诈 (→ "Anti-faixas") 音) 音) 音音是当前研究热点点.





## Construí-lo e realizei-o.
```figure
sp-vad-cascade
```

## Construí-lo

### Passo 1: o portal de energia

> Passo 1: Energia em controle

```python
def energy_vad(chunk, threshold_dbfs=-40.0):
    rms = (sum(x * x for x in chunk) / len(chunk)) ** 0.5
    dbfs = 20.0 * math.log10(max(rms, 1e-10))
    return dbfs > threshold_dbfs
```

### Passo 2: Silero VAD em Python

> 步骤 2: Use Silero VAD em Python

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

### Passo 3: máquina de estado de turno

> 步骤 3: Rodeo de conclusão

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

### Passo 4: o esqueleto do truque de flush

> 步骤 4:刷新技巧框架代码

```python
def flush_on_end(stt_client, audio_buffer):
    stt_client.send_audio(audio_buffer)
    stt_client.send_flush()
    return stt_client.recv_transcript(timeout_ms=150)
```

> **【中文解读】**Este capítulo mostra como usar um framework maduro (como PyTorch、HuggingFace etc) rápida aplicação desta tecnologia.


STT (Kyutai, Deepgram, AssemblyAI) deve suportar flush para que isso funcione.

> STT(Kyutai、Deepgram、AssemblyAI) deve apoiar o flush 才能使这一技巧生效──Whisper 流式不支持它是基于块的,总是等待完整块──




> **【拓展：语音与情感计算】**语音 não apenas transmite informações escritas, mas também carrega um rico sinal emocional (语调、语速、音高变化) ◦情感语音识别 (语调、语速、音高变化) ◦情感语音识别 (语音识别, speech emotion recognition, SER) tem uma ampla aplicação em áreas como o controle de qualidade de clientes, a monitorização de saúde mental, a educação inteligente e outras.

## Use-o com o framework implementado.

| Situation | VAD choice |
|-----------|-----------|
| Open, fast, general / 开源、快速、通用 | Silero VAD |
| Commercial call center / 商业呼叫中心 | Cobra VAD |
| On-device (phone) / 端侧（手机） | Silero VAD ONNX |
| Research / diarization / 研究/说话人日志 | pyannote segmentation |
| Zero-dependency fallback / 零依赖后备方案 | WebRTC VAD（传统） |
| Need turn-ending quality / 需要轮次结束质量 | Silero + LiveKit 轮次检测器分层 |

Regra geral: nunca envie VADs exclusivamente energéticos, a menos que realmente não tenha outra opção.

> 經驗法则: Se realmente não houver outra opção, então nunca mais seja baseado apenas na energia VAD.



## Encurralagens

> 常见陷

- **Fixed threshold.**Funciona em silêncio, falha em barulho, calibra no dispositivo ou passa para Silero.
  Tradução:**固定阈值。**Em ambiente tranquilo, válido, falhado, em ambiente difícil.
- **Too-short silence hangover.**O agente interrompe a metade da frase. 500-800 ms é o ponto ideal para conversação.
  Tradução:**静音持续等待过短。**助手在句子中打断用户──500-800 ms é o melhor alcance do diálogo语音──
- **Too-long hangover.**Teste A/B com usuários alvo.
  Tradução:**静音持续等待过长。**感觉迟──与目标用户进行A/B 测试──
- **No pre-roll buffer.**Os primeiros 200-300 ms de áudio do usuário perdidos.
  Tradução:**没有预滚缓冲。**Usuário de rádio de 200-300 ms                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                     
- **Ignoring semantic endpointing.**"Hmm, deixe-me pensar"... contém longas pausas. Os usuários odeiam ser cortados no meio do pensamento.
  Tradução:**忽略语义端点检测。**",让我想想......" contém um longo intervalo.

> **【中文解读】**Este capítulo se concentra em como o modelo será implantado como produto disponível. De modelo original a nível de produção, os sistemas precisam considerar várias dimensões de otimização de desempenho, tratamento de erros, controle, etc.


## Envia-o . Produto .

Salva como`outputs/skill-vad-tuner.md`Escolha o modelo VAD, o limiar, a ressaca, a estratégia de pré-rol e de detecção de voltas para uma carga de trabalho.

> 保存为 `outputs/skill-vad-tuner.md`◊ para um trabalho de carga escolher VAD 模型、值、静音持续等待、预滚缓冲和轮次检测策略──

## Exercícios.

1. **Easy.**Corra .`code/main.py`Simula uma sequência de fala + silêncio + fala + tosse e testa três níveis de VAD.
   Tradução:**简单。**运行 `code/main.py`∼ It模拟一段语音 + 静音 + 语音 + 咳的序列,并测试三层 VAD──
2. **Medium.**Instalação`silero-vad`, processar uma gravação de 5 minutos, ajustar o limiar para minimizar os clips de primeira palavra e os desencadeadores falsos.
   Tradução:**中等。**Instalação`silero-vad`, processar um parágrafo 5 minutos de gravação, ajustar o valor para minimizar o corte de palavras e o erro de toque.
3. **Hard.**Construir um mini-detector de viradas: Silero VAD + um MLP de 3 camadas em embutidos das últimas 10 palavras (use transformadores de frases). Treinar em um conjunto de dados de viradas rotulados a mão. Bater Silero apenas em 10% F1.
   Tradução:**困难。**Construir um pequeno rotador de teste: Silero VAD + baseado em 10 个近词嵌入的 3层 MLP(utilizando transformadores de frases) ⋅ em rotas de marcação manual de conclusão do conjunto de dados ⋅ em treinamento ⋅ em puro Silero 方案 F1 ⋅ 10% ⋅

> **【中文解读】**No 术语表中的"O que as pessoas dizem" vs "O que realmente significa" 区分日常口语和精确技术含义── em equipe,统一术语定义可以避免大量沟通误解──


## Termos-chave .

| Term | What people say | What it actually means |
|------|-----------------|-----------------------|
| VAD | Voice detector | Binary per-frame: is this speech? / 逐帧二分类：这是语音吗？ |
| Turn detection | End-pointing | VAD + silence-hangover + semantic endpoint. / VAD + 静音持续 + 语义端点 |
| Silence hangover | Wait-after-speech | Time to wait before declaring turn end; 500-800 ms. / 宣布轮次结束前的等待时间；500-800 ms |
| Pre-roll | Pre-speech buffer | Keep 300-500 ms audio before VAD fires. / 在 VAD 触发前保留 300-500 ms 音频 |
| Flush trick | Kyutai hack | VAD → flush-STT → 125 ms instead of 500 ms delay. / VAD → 刷新 STT → 125 ms 而非 500 ms 延迟 |
| Semantic endpoint | "Did they mean to stop?" | ML classifier that looks at words, not just silence. / 看词汇而非仅看静音的 ML 分类器 |
| TPR @ FPR 5% | ROC point | Standard VAD benchmark; 87.7% for Silero, 50% WebRTC. / 标准 VAD 基准；Silero 87.7%，WebRTC 50% |

> **【中文解读】**延伸阅读 fornece recursos de alta qualidade para a aprendizagem profunda.


## Mais leitura 延伸阅读

- [Silero VAD](https://github.com/snakers4/silero-vad) o VAD aberto de referência.
  Silero VAD  Open Source Referência VAD
- [Picovoice Cobra VAD](https://picovoice.ai/products/cobra/) líder em precisão comercial.
  Picovoice Cobra VAD
- [Kyutai — Unmute + flush trick](https://kyutai.org/stt)O truque de engenharia de sub-200 ms.
  KyutaiUnmute + 刷新技巧亚 200 ms 的工程技巧──
- [LiveKit — turn detection](https://docs.livekit.io/agents/logic/turns/) endpointing semântico na produção.
  O Livro de Kit 轮次检测 生产中的语义端点检测 
- [WebRTC VAD](https://webrtc.googlesource.com/src/) a linha de base herdada.
  WebRTC VAD tradição
- [pyannote segmentation](https://github.com/pyannote/pyannote-audio) Segmentação de nível de diarização.
  Pyannote segmentação说话人日志级别的分分──

> **【中文解读】**延伸阅读 forneceu recursos de alta qualidade para a aprendizagem profunda, incluindo artigos, tutoriais e ferramentas.

