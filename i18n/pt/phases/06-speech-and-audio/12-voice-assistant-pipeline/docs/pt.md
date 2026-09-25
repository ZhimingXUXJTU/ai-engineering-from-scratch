# Construir um Pipeline de Assistente de Voz  A Fase 6 Capstone  Construir um projeto de formação  阶段 6 毕业项目

> Tudo das lições 01-11, coçadas juntas. Construir um assistente de voz que ouça, razona e fala. Em 2026 isso é um problema de engenharia resolvido, não um problema de pesquisa  mas os detalhes de integração decidem se ele vai enviar.

> **【中文解读】**Colocar todos os conteúdos das aulas para cima, construir um assistente de voz capaz de ouvir, pensar, falar.

**Type:** Build | **类型:** 构建
**Languages:** Python | **语言:** Python
**Prerequisites:** Phase 6 · 04, 05, 06, 07, 11; Phase 11 · 09 (Function Calling); Phase 14 · 01 (Agent Loop) | **前置知识:** 阶段 6 · 04、05、06、07、11；阶段 11 · 09（函数调用）；阶段 14 · 01（智能体循环）
**Time:** ~120 minutes | **预计用时:** ~120 分钟

## O problema é o problema da introdução

Construa um assistente de ponta a ponta:

> Construir um assistente de ponta a ponta:

> **【中文解读】**A questão que se coloca neste capítulo é: como entender e aplicar esta tecnologia de forma correta na engenharia real.

1. Captura entrada de microfone (16 kHz mono).
   捕获麦克风输入(16 kHz 单声道)
2. Detecta o início/final da fala do utilizador.
   检测用户语音的开始/结束──
3. Transcreve o streaming.
   流式转录──
4. Passa a transcrição para um LLM que pode chamar ferramentas (timer, tempo, calendário).
   Transmitir o transmissão para ferramentas de manipulação de tempo (L.L.M.):
5. Transmitir texto de LLM para um TTS.
   Transmitir o Mestrado em Letras para o TTS.
6. Reproduza áudio para o usuário.
   À usuário播放音频──
7. Parará se o utilizador interromper a resposta média.
   Se o usuário em resposta interromper, parar.

Meta de latência: primeiro byte de áudio TTS dentro de 800 ms do usuário terminando sua declaração em uma CPU de computador portátil. Meta de qualidade: nenhuma palavra perdida, nenhum subtítulo alucinado no silêncio, nenhum vazamento de clonagem de voz, nenhum sucesso de injeção rápida.

> 延迟目标:在笔记本 CPU 上用户说完话后 800 ms 内发发第一个 TTS 音频字节──质量目标:不漏词、静音不产生幻觉字幕、无声音克隆泄漏、提示注入不成功──

## O conceito central.

> **【中文解读】**Este capítulo apresenta os conceitos e teorias fundamentais.


![Voice assistant pipeline: mic → VAD → STT → LLM+tools → TTS → speaker](../assets/voice-assistant.svg)

### Os sete componentes

1. **Audio capture.**Mic → 16 kHz mono → 20 ms. Geralmente `sounddevice`em Python ou em AudioUnit/ALSA/WASAPI nativo em produção.
   **音频捕获。**麦克风 → 16 kHz 单声道 → 20 ms 块──Python 中通常使用 `sounddevice`, produção ambiental us native AudioUnit/ALSA/WASAPI。
2. **VAD (Lesson 11).**Silero VAD @ limiar 0,5, min fala 250 ms, silêncio pendurado 500 ms. Sinais "começo" e "fim".
   **VAD（第 11 课）。**Silero VAD @ 值 0.5, mínimo语音 250 ms,静音持续 500 ms── sinal"开始"和"结束"──
3. **Streaming STT (Lesson 4-5).**Whisper-streaming, Parakeet-TDT, ou Deepgram Nova-3 (API). Transcrições parciais + finais.
   **流式 STT（第 4-5 课）。**Whisper-streaming、Parakeet-TDT 或 Deepgram Nova-3(API) 』部分 + 最终转录──
4. **LLM with tool calling.**GPT-4o / Claude 3.5 / Gemini 2.5 Flash. JSON esquema para ferramentas. Tokens de streaming.
   **带工具调用的 LLM。**GPT-4o / Claude 3.5 / Gemini 2.5 Flash──工具的 JSON schema──流式代币──
5. **Streaming TTS (Lesson 7).**Kokoro-82M (aberto mais rápido) ou Cartesia Sonic (comercial).
   **流式 TTS（第 7 课）。**Kokoro-82M (最快的开源)  Cartesia Sonic (商业)  在 20 个 LLM token 后启动 TTS──
6. **Playback.**- O que é isso? - O que é isso?
   **回放。**扬声器输出;低带宽网络用 opus 编码──
7. **Interruption handler.**Se o VAD disparar durante a reprodução do TTS, parar a reprodução, cancelar o LLM, reiniciar o STT.
   **打断处理器。**Se o TTS estiver em transmissão, o VAD 触发, parar de ser transmitido, eliminar o LLM, reiniciar o STT.

### Os três modos de falha que você vai acertar

> ### Três tipos de falhas que você vai encontrar.

1. **First-word clip.**O VAD começa a bater tarde demais, o "hei" do usuário está faltando.
   **首词截断。**VAD  inicialização tarde um tempo. O "" do usuário foi perdido.
2. **Mid-response interrupt confusion.**LLM continua a gerar após interrupções do usuário; assistente conversa sobre o usuário.
   **回应中打断混乱。**Utilizador                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           
3. **Silence hallucination.**O sussurro diz "Obrigado por assistir" nos quadros silenciosos.
   **静音幻觉。**Whisper 在静音预热上输出"Obrigado por assistir"──务必用 VAD 过──

### 2026 Estacas de referência de produção

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

> **【中文解读】**Este é um método de "desde zero" que ajuda a entender o princípio da estrutura, não é um problema que se encontra em uma caixa negra.

> **【拓展：语音 AI 的产品化】**A tecnologia de voz enfrenta desafios únicos na produção: diferentes sons, ruídos de contexto, remoção de chamadas, conversas de pessoas, etc. Os produtos de Siri, Alexa, Pequeno Amor e outros são empregados em grande quantidade de engenharia para resolver esses "problemas de longo prazo".

> **【拓展：多语言语音技术】**As características do som de uma língua mundial são enormes: a alta densidade de voz de uma língua (como o chinês) é de baixa capacidade, a falta de dados de treinamento em linguagem.

> **【拓展：语音隐私与安全】**语音数据 contém uma grande quantidade de informações pessoais de privacidade (→ "faixas") 语音数据包含大量个人隐私信息 (→ "faixas") 语音技术 (→ "faixas") 语音技术 (→ "faixas") 语音技术 (→ "faixas") 语音技术 (→ "faixas") 语音技术 (→ "faixas") 语音技术 (→ "faixas") 语音技术 (→ "faixas") 语音数据 (→ "faixas") 语音技术 (→ "faixas") 语音技术 (→ "faixas") 语音技术 (→ "faixas") 语音技术 (→ "faixas") 语音技术 (→ "faixas") 语音音音水印 (→ "Audio Watermarking") 音纹反欺诈 (→ "Anti-faixas") 音纹) 音反欺诈 (→ "Anti-faixas") 音) 音) 音音是当前研究热点点.





## Construí-lo e realizei-o.
```figure
v4-voice-latency
```

## Construí-lo

### Passo 1: captura de microfone com fragmentação (pseudocód)

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

### Passo 2: Captura de viradas com porta VAD

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

### Passo 3: streaming STT → LLM → TTS

```python
async def turn(audio_bytes):
    transcript = await stt.transcribe(audio_bytes)
    async for token in llm.stream(transcript):
        async for audio in tts.stream(token):
            await speaker.play(audio)
```

### Passo 4: chamada de ferramenta dentro do ciclo de LLM

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

### Passo 5: Manutenção de interrupção

> **【中文解读】**Este capítulo mostra como usar um framework maduro (como PyTorch、HuggingFace etc) rápida aplicação desta tecnologia.


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




> **【拓展：语音与情感计算】**语音 não apenas transmite informações escritas, mas também carrega um rico sinal emocional (语调、语速、音高变化) ◦情感语音识别 (语调、语速、音高变化) ◦情感语音识别 (语音识别, speech emotion recognition, SER) tem uma ampla aplicação em áreas como o controle de qualidade de clientes, a monitorização de saúde mental, a educação inteligente e outras.

## Use-o com o framework implementado.

Veja .`code/main.py`Para uma simulação executável que conecta todos os sete componentes com modelos de estúdio, para que você possa ver a forma do pipeline mesmo sem hardware.

> 参见 `code/main.py`获取可运行的模拟,将七组件用模块连接,无需硬件即可见流水线形状──实际实现时,将模块替换为:

- `silero-vad`(`pip install silero-vad`) / VAD 模块
- `deepgram-sdk`ou `openai-whisper`/ 流式 STT
- `openai`(`gpt-4o`) ou `anthropic`/ LLM + 工具调用
- `kokoro`ou `cartesia`/ 流式 TTS
- `sounddevice`para I/O / 音频输入输出



## Encurralagens

> 常见陷

- **Logging PII forever.**O áudio de rotação completa é PII na maioria das jurisdições. 30 dias de retenção, criptografado em repouso.
  **永久记录 PII。**完整轮次音频在多数司法管辖区属于PII──30 天保留,静态加密──
- **No barge-in.**Os usuários interromperão, o seu assistente deve parar de falar.
  **没有抢话。**O usuário vai-se interromper.
- **TTS that blocks.**TTS sincrônico bloqueia o ciclo de eventos. Use async ou um fio separado.
  **阻塞式 TTS。**Simpele TTS  bloqueio de eventos ciclo.
- **No tool-call error handling.**As ferramentas falham. LLM deve recuperar o erro + tentar novamente uma vez, e depois graciosamente degradar.
  **没有工具调用错误处理。**工具会失败──LLM 必须收到错误 + 重试一次,然后优雅降级──
- **Overzealous hallucination filters.**O assistente repete "Não posso ajudar com isso". O subfiltro diz qualquer coisa.
  **过度激进的幻觉过滤。**过度过助手会重复"我帮不了"──过不足则什么都说──在留出集上校准──
- **No wake-word option.**Sempre ouvir é uma responsabilidade de privacidade. Adicione um portal de despertar (Porcupine ou openWakeWord).
  **没有唤醒词选项。**Continuar a ouvir é um problema de privacidade.

> **【中文解读】**Este capítulo se concentra em como o modelo será implantado como produto disponível. De modelo original a nível de produção, os sistemas precisam considerar várias dimensões de otimização de desempenho, tratamento de erros, controle, etc.


## Envia-o . Produto .

Salva como`outputs/skill-voice-assistant-architect.md`. Tendo em conta as limitações orçamentais + de escala + de língua + de conformidade, produzir uma especificação completa da pilha.

> 保存为 `outputs/skill-voice-assistant-architect.md` O orçamento + a dimensão + a língua + a regulamentação, produzindo um total de técnicas  regulamentações.

## Exercícios.

1. **Easy.**Corra .`code/main.py`Simula uma rotação completa de ponta a ponta com módulos de estúdio e impressões por estágio de latência.
   **简单。**运行 `code/main.py`模块模拟一个完整轮次端到端并印各阶段延迟
2. **Medium.**Substitua o estúdio STT por um modelo real de Whisper num pré-registado `.wav`- Meter o WER e a latência de ponta a ponta.
   **中等。**Em pré-registro`.wav`上用真实 Whisper 模型替换STT 模块──测量 WER 和端到端延迟──
3. **Hard.**Adicionar chamada de ferramenta: implementar `get_weather`(qualquer API) e `set_timer`. Enviar o Mestrado em Direito através das ferramentas e verificar que quando o utilizador diz "configurar um temporizador de 5 minutos", a função correta dispara e a resposta falada confirma isso.
   **困难。**添加工具调用: realizar `get_weather`(qualquer API) e `set_timer` através do instrumento de LLM, verificando quando o usuário diz "por um dispositivo de fixação de 5 minutos" quando a função correta é utilizada 

> **【中文解读】**No 术语表中的"O que as pessoas dizem" vs "O que realmente significa" 区分日常口语和精确技术含义── em equipe,统一术语定义可以避免大量沟通误解──


## Termos-chave .

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

> **【中文解读】**延伸阅读 fornece recursos de alta qualidade para a aprendizagem profunda.


## Mais leitura 延伸阅读

- [LiveKit — voice agent quickstart](https://docs.livekit.io/agents/)Referência de nível de produção.
  LiveKit语音智能体快速入门生产级参考──
- [Pipecat — voice agent examples](https://github.com/pipecat-ai/pipecat) Framework amigável para o DIY.
  Pipecat语音智能体示例DIY 友好框架──
- [OpenAI Realtime API](https://platform.openai.com/docs/guides/realtime) o caminho de voz nativa gerenciado.
  OpenAI Realtime API托管的语音原生路径──
- [Kyutai Moshi](https://github.com/kyutai-labs/moshi) Referência duplex completa (Lessão 15).
  Kyutai Moshi全双工参考(第 15 课)。
- [Porcupine wake-word](https://picovoice.ai/products/porcupine/)- O gating de palavras de despertar.
  Porcupine 唤醒词唤醒词门控──
- [Anthropic — tool use guide](https://docs.anthropic.com/en/docs/build-with-claude/tool-use) Chamando a função de LLM.
  Antropic工具使用指南LLM 函数调用──

> **【中文解读】**延伸阅读 forneceu recursos de alta qualidade para a aprendizagem profunda, incluindo artigos, tutoriais e ferramentas.

