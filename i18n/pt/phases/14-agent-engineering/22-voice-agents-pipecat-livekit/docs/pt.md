# Agentes de voz: Pipecat e LiveKit

> Os agentes de voz são uma categoria de produção de primeira classe em 2026. Pipecat oferece um pipeline baseado em Python (VAD → STT → LLM → TTS → transporte). LiveKit Agents faz pontes entre os modelos de IA para os usuários através do WebRTC.

**Type:** Learn | **类型:** 学习
**Languages:** Python (stdlib) | **语言:** Python (标准库)
**Prerequisites:** Phase 14 · 01 (Agent Loop), Phase 14 · 12 (Workflow Patterns) | **前置知识:** 见原文
**Time:** ~60 minutes | **时间:** 见原文

## Objetivos de aprendizagem

- Descreva o sistema de condução baseado em quadros da Pipecat: DOWNSTREAM (fonte→sink) e UPSTREAM (controle).
- Nomear os estágios do pipeline de voz canônico e que transportam os suportes da Pipecat.
- Explique as duas classes de agentes de voz do LiveKit Agents (MultimodalAgent, VoicePipelineAgent) e quando cada uma se encaixa.
- Resumir as expectativas de latência de produção de 2026 e como elas impulsionam as escolhas de arquitetura.

## O problema é o problema da introdução

Os agentes de voz não são um ciclo de texto com TTS ligado. Os orçamentos de latência são brutais (~ 600ms), o áudio parcial é o padrão, a detecção de viradas é um modelo, e os transportes variam de telefonia SIP para WebRTC. Ou você constrói um pipeline baseado em quadros (Pipecat) ou você se apoia em uma plataforma (LiveKit).

> 语音 Agente não é um ciclo de texto adicionado ao TTS──延迟预算极极苛(约600ms), parte do estrado é um estado de memória, a rotada de teste é um modelo, o modo de transmissão de um telefone SIP até WebRTC 不等── você vai construir um tubo baseado em  (Pipecat), ou depender de uma plataforma (LiveKit) ──


> **【中文解读】**语音 Agente 需要实时处理音频流语音识别(ASR)、LLM 推理、语音合成(TTS) de atraso deve ser de 300ms 以内以维持自然对话──Pipecat 和 LiveKit 提供构建低延迟语音 Agente estrutura e infraestrutura──

> **{【拓展：Pipecat（开源框架）和 LiveKit（实时音频基础设施）是 2026 年语音 Agent 生...】}**Pipecat (pipecat) é uma empresa de telecomunicações que desenvolve sistemas de rede de rede de rede de rede de rede de rede de rede de rede de rede de rede de rede de rede de rede de rede de rede de rede de rede de rede de rede de rede de rede de rede de rede de rede de rede de rede de rede de rede de rede de rede de rede de rede de rede de rede de rede de rede de rede de rede de rede de rede de rede de rede de rede de rede de rede de rede de rede de rede de rede de rede de rede de rede de rede de rede de rede de rede de rede de rede de rede de rede de rede de rede de rede de rede de rede de rede de rede de rede de rede de rede de rede de rede de rede de rede de rede de rede de rede de rede de rede de rede de rede de rede de rede de rede de rede de rede de rede de rede de rede de rede de rede de rede de rede de rede de rede de rede de rede de rede de rede de rede de rede de rede de rede de rede de rede de rede de rede de rede de rede de rede de rede de rede de rede de rede de rede de rede de rede de rede de rede de rede de rede de rede de rede de rede de rede de rede de rede de rede de rede de rede de rede de rede de rede de rede de rede de rede de rede de rede de rede de rede de rede de rede de rede de rede de rede de rede de rede de rede de rede de rede de rede de rede de rede de rede de rede de rede de rede de rede de rede de rede de rede de rede de rede de rede de rede de rede de rede de rede de rede de rede de rede de rede de rede de rede de rede de rede de rede de rede de rede de rede de rede de rede de rede de rede de rede de rede de rede de rede de rede de rede de rede de rede de rede de rede de rede de rede de rede de rede de rede de rede de rede de rede de rede de rede de rede de rede de rede de rede de rede de rede de rede de rede de rede de rede de rede de rede de rede de rede de rede de rede de rede de rede de rede de rede de rede de rede de rede de rede de rede de rede de rede de rede de rede de rede de rede de rede de rede de rede de rede de rede de rede de rede de rede de rede de rede de rede

> - Não .**【前置】**O processo de produção de um fluxo de trabalho é um processo de produção de um fluxo de trabalho de um fluxo de trabalho de um fluxo de trabalho de um fluxo de trabalho de um fluxo de trabalho de um fluxo de trabalho de um fluxo de trabalho de um fluxo de trabalho de um fluxo de trabalho de um fluxo de trabalho de um fluxo de trabalho de um fluxo de trabalho de um fluxo de trabalho de um fluxo de trabalho de um fluxo de trabalho de um fluxo de trabalho de um fluxo de trabalho de um fluxo de trabalho de um fluxo de trabalho de um fluxo de trabalho de um fluxo de trabalho de um fluxo de trabalho de um fluxo de trabalho de um fluxo de trabalho de um fluxo de trabalho de um fluxo de trabalho de um fluxo de trabalho de um fluxo de fluxo de um fluxo de trabalho de um fluxo de fluxo de fluxo de um fluxo de fluxo de fluxo de um fluxo de fluxo de fluxo de fluxo de fluxo de um fluxo de fluxo de fluxo de fluxo de fluxo de fluxo de fluxo de fluxo de fluxo de fluxo de fluxo de fluxo de fluxo de fluxo de fluxo de fluxo de fluxo de fluxo de fluxo de fluxo de fluxo de fluxo de fluxo de fluxo de fluxo de fluxo de fluxo de fluxo de fluxo de fluxo de fluxo de fluxo de fluxo de fluxo de fluxo de fluxo de fluxo de fluxo de fluxo de fluxo de fluxo de fluxo de fluxo de fluxo de fluxo de fluxo de fluxo de fluxo de fluxo de fluxo de fluxo de fluxo de fluxo de fluxo de fluxo de fluxo de fluxo de fluxo de fluxo de fluxo de fluxo de fluxo de fluxo de fluxo de fluxo de fluxo de fluxo de fluxo de fluxo de fluxo de fluxo de fluxo de fluxo de fluxo de fluxo de fluxo de fluxo de fluxo de fluxo de fluxo de fluxo de fluxo de fluxo de fluxo de fluxo de fluxo de fluxo de fluxo de fluxo de fluxo de fluxo de fluxo de fluxo de fluxo de

## O conceito central.

### Pipecat (pipecat-ai/pipecat)

- Framework de pipeline baseado em Python.
- `Frame`→ `FrameProcessor`- A cadeia.
- Duas direcções de fluxo:
  - **DOWNSTREAM** fonte → fregona (áudio dentro, TTS fora).
  - **UPSTREAM** Feedback e controlo (cancelação, métricas, barge-in).
- `PipelineTask`gerenciam o ciclo de vida com eventos (`on_pipeline_started`- Não .`on_pipeline_finished`- Não .`on_idle_timeout`) e observadores para métricas/ rastreamento/RTVI.

Pipeline típica:

```
VAD (Silero) → STT → LLM (context alternates user/assistant) → TTS → transport
```

Transporte: Diário, LiveKit, SmallWebRTCTransport, FastAPI WebSocket, WhatsApp.

> - Não .**【类比】**Pipecat's frame-based pipeline 像汽车流水线:每个工位(Processor) só faz uma coisa  VAD 工位识别有没有人说话、STT 工位把语音转文字、LLM 工位想回复、TTS 工位把文字转语音),车架(Frame) do caminho do caminho do fluxo do caminho do caminho do caminho do caminho do caminho do caminho do caminho do caminho do caminho do caminho do caminho do caminho do caminho do caminho do caminho do caminho do caminho do caminho do caminho do caminho do caminho do caminho do caminho do caminho do caminho do caminho do caminho do caminho do caminho do caminho do caminho do caminho do caminho do caminho do caminho do caminho do caminho do caminho do caminho do caminho do caminho do caminho do caminho do caminho do caminho do caminho do caminho do caminho do caminho do caminho do caminho do caminho do caminho do caminho do caminho do caminho do caminho do caminho do caminho do caminho do caminho do caminho do caminho do caminho do caminho do caminho do caminho do caminho do caminho do caminho do caminho do caminho do caminho do caminho do caminho do caminho do caminho do caminho do caminho do caminho do caminho do caminho do caminho do caminho do caminho do caminho do caminho do caminho do caminho do caminho do caminho do caminho do caminho do caminho do caminho do caminho do caminho do caminho do caminho do caminho do caminho do caminho do caminho do caminho do caminho do caminho do caminho do caminho do caminho do caminho do caminho do caminho do caminho do caminho do caminho do caminho do caminho do caminho do caminho do caminho do caminho do caminho do caminho do caminho do caminho do caminho do caminho do caminho do caminho do caminho do caminho do caminho do caminho do caminho do caminho do caminho do caminho do caminho do caminho do caminho do caminho do caminho do caminho do caminho do caminho do caminho do caminho do caminho do caminho do caminho do caminho do caminho do caminho do caminho do caminho do caminho do caminho do caminho do caminho do caminho do caminho do caminho do caminho do caminho do caminho do caminho do caminho do caminho do caminho do caminho do caminho do caminho do caminho do caminho.

> 语音代理 结合 LLM 和实时语音处理──Pipecat 和 LiveKit são duas principais frameworks de agência de voz, separadamente de tratamento de canais de áudio e comunicação real.

Pipecat Fluxes adiciona conversas estruturadas (máquinas de estado).

> 语音代理 结合 LLM 和实时语音处理──Pipecat 和 LiveKit são duas principais frameworks de agência de voz, separadamente de tratamento de canais de áudio e comunicação real.

### Agentes do LiveKit (livekit/agentes)

- Ponte de modelos de IA para os usuários através de WebRTC.
- Conceptos-chave: `Agent`- Não .`AgentSession`- Não .`entrypoint`- Não .`AgentServer`- Não .
- Duas aulas de agentes vocais:
  - **MultimodalAgent** áudio direto através do OpenAI em tempo real ou equivalente.
  - **VoicePipelineAgent** STT → LLM → TTS cascata; dá controle a nível de texto.
- Detecção semântica de viradas através de um modelo transformador.
- Integração nativa de MCP.
- Telefone por SIP.
- 50+ modelos sem chaves de API através do LiveKit Inference; mais 200+ através de plugins.

### Plataformas comerciais

Vapi (~ 450600ms em uma pilha premium otimizada) e Retell (~ 600ms de ponta a ponta em 180 chamadas de teste) se baseiam nesses.

> 🤔 **【困惑】**P: MultimodalAgent (音频进音频出) 和 VoicePipelineAgent (STT→LLM→TTS 级联) ¿Dónde底选哪个? A: 看你需要多少控制权? A: 看你需要多少控制权? A: 看你需要多少控制权? A: 看你需要多少控制权? A: 看你需要多少控制权? A: 看你需要多少控制权? A: 看你需要多少控制权? A: A: 看你需要多少控制权? A: A: 看你需要多少控制权? A: A: 看你需要多少控制权? A: A: 看你需要多少控制权? A: A: 看你需要多少控制权? A: A: 看你需要多少控制权? A: A: 看你需要多少控制权? A: A: 看你需要多少控制权? A: A: 看你需要多少控制权? A: A: 看你需要多少控制权? A: A: 看你需要多少控制权? A: 看你需要多少控制权? A: 看你需要多少控制权? A: 看你需要多少控制权? A: 延迟更少两次转换? A: 迟迟?

> Vapi(optimização posterior de alta堆 cerca de 450-600ms) e Retell(180 vezes teste de conversação de fim a fim de cerca de 600ms) construído sobre estes.

> 语音代理 结合 LLM 和实时语音处理──Pipecat 和 LiveKit são duas principais frameworks de agência de voz, separadamente de tratamento de canais de áudio e comunicação real.

### Onde este padrão vai mal

- **No barge-in handling.**O usuário interrompe, o agente continua a falar. Requer que o UPSTREAM cancele quadros no Pipecat, equivalente no LiveKit.
- **STT confidence ignored.**Transcrições de baixa confiança alimentadas ao LLM como se fossem evangelhos.
- **TTS mid-sentence cutoff.**Quando o tubo cancelar a meia-terminação, o TTS precisa saber ou cortar áudio.
- **Latency budget ignored.**Cada componente adiciona 50200ms. Sumem a cadeia antes do envio.

> **没有打断处理。**Utilizador: Abre; Agente: Continuar a falar:
> **忽略 STT 置信度。**O processo de transferência de confiança foi considerado como a transferência de verdade para o LLM.
> **TTS 句中截断。**Quando o tubo está em meio ao discurso, o TTS precisa saber ou cortar o som.
> **忽略延迟预算。**Cada componente aumenta 50-200ms.

### Tópicas latências de 2026

- VAD: 2060ms
- Teste de transmissão de dados:
- LLM primeiro token: 150400ms
- TTS primeiro áudio: 100200ms
- RTT de transporte: 3080ms

End-to-end 450600ms é premium. 8001200ms é comum. Qualquer coisa > 1500ms parece quebrado.

> 端到端 450-600ms é alto nível. 800-1200ms é comum.

> 语音代理 结合 LLM 和实时语音处理──Pipecat 和 LiveKit são duas principais frameworks de agência de voz, separadamente de tratamento de canais de áudio e comunicação real.

## Construí-lo e realizei-o.

> ️ **【易错点】**Novo uso de tubos de voz:**不做 barge-in 处理** usuário quando o agente ainda está em sua própria experiência, deve estar no processador TTS  monitorar o sistema de cancelamento UPSTREAM 并立即停止音频输出──(2) **忽略 STT 置信度**置信度 0.3 的""被当成用户回答,Agente 走错分支;修复:confiança < 0.7 时让Agente 反问"我没听清,能再说一次吗"―(3) **延迟预算算总账** Individualmente ver cada componente todo até o momento(VAD 40ms + STT 200ms + LLM 300ms + TTS 150ms = 690ms), mas no topo de linha, do final ao final 1200ms, porque漏算了网络 RTT 和队列等待──修复:
```figure
voice-pipeline
```

## Construí-lo

`code/main.py`é um tubo de brinquedos baseado em quadro com:

> 语音代理 结合 LLM 和实时语音处理──Pipecat 和 LiveKit são duas principais frameworks de agência de voz, separadamente de tratamento de canais de áudio e comunicação real.

- `Frame`tipos (áudio, transcrição, texto, tts_audio, controle).
- `Processor`Interface com `process(frame)`- Não .
- Um gasoduto de cinco etapas (VAD → STT → LLM → TTS → transporte) como processadores de guião.
- Um quadro de cancelamento UPSTREAM para demonstrar a barragem.

- É o que é ?

```
python3 code/main.py
```

O rastro mostra fluxo normal e um barge-in cancelar que pára TTS em meados de pronunciamento.

> Trace mostra o normal do processo e um interrupção no meio do discurso de TTS.

> 语音代理 结合 LLM 和实时语音处理──Pipecat 和 LiveKit são duas principais frameworks de agência de voz, separadamente de tratamento de canais de áudio e comunicação real.

## Use-o com o framework implementado.

- **Pipecat**para controlo total  processadores personalizados, fornecedores plug-in Python-first.
- **LiveKit Agents**para as primeiras instalações WebRTC e telefonia.
- **Vapi / Retell**para agentes de voz hospedados sem uma equipa WebRTC.
- **OpenAI Realtime / Gemini Live**para entrada/saída de áudio direta (MultimodalAgent).

## Envia-o . Produto .

`outputs/skill-voice-pipeline.md`Estabelece um canal de voz em forma de Pipecat com VAD + STT + LLM + TTS + transporte mais manuseio de embarque.

> `outputs/skill-voice-pipeline.md`Construir um Pipecat 形态语音管道, incluindo VAD + STT + LLM + TTS + 传输以及打断处理──

> 语音代理 结合 LLM 和实时语音处理──Pipecat 和 LiveKit são duas principais frameworks de agência de voz, separadamente de tratamento de canais de áudio e comunicação real.

## Exercícios.

1. Adicione um observador de métricas à sua linha de brinquedos: conte quadros por estágio por segundo. Onde se acumula a latência?
  Tradução do inglês para tradução do inglês:
2. Implementar STT com limite de confiança: abaixo do limiar, solicitar "poderia repetir isso?"
  Tradução do inglês para tradução do inglês:
3. Adicione detecção semântica de virada: regra simples  se a transcrição termina com "?", fim da virada.
  Tradução do inglês para tradução do inglês:
4. Leia os documentos de transporte da Pipecat. Troque o transporte stdlib para o SmallWebRTCTransport config (stub).
  Tradução do inglês para tradução do inglês:
5. Meter uma cascata OpenAI em tempo real versus STT+LLM+TTS na mesma consulta. Qual o custo de latência que o controle de nível de texto leva?
  Tradução do inglês para tradução do inglês:

## Termos-chave .

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

## Mais leitura 延伸阅读

- [Pipecat docs](https://docs.pipecat.ai/getting-started/introduction) Tubos de produção baseados em quadros, processadores, transportes
  Tradução do português:
- [LiveKit Agents docs](https://docs.livekit.io/agents/) WebRTC + primitivos de voz
  Tradução do português:
- [Vapi](https://vapi.ai/) Plataforma de voz gerenciada
  Tradução do português:
- [Retell AI](https://www.retellai.com/) voz gerenciada, com marcador de latência
  Tradução do português:
