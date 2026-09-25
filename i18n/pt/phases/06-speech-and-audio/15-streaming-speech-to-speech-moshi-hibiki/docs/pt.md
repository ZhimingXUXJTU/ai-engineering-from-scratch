# Transmissão de fala-a-fala  Moshi, Hibiki e diálogo duplo completo 流式语音到语音  Moshi、Hibiki与全双工对话

> 2024-2026 redefinido voz IA. Moshi envia um único modelo que ouve e fala simultaneamente em 200 ms de latência. Hibiki faz a tradução de fala para fala pedaço por pedaço. Ambos abandonam o pipeline ASR → LLM → TTS para uma arquitetura unificada de duplex completo sobre tokens de codec Mimi. Este é o novo design de referência.

> **【中文解读】**2024-2026 anos redefiniram o idioma AI。Moshi usando um único modelo em 200ms 延迟内同时听和说。Hibiki 逐块进行语音到语音翻译。 ambos abandonaram ASR→LLM→TTS 流水线, adoptando uma estrutura de conjunto de dois tipos baseada em tokens Mimi 编解码器。 este é um novo design de referência。

> **【拓展：全双工语音 AI】**傳統语音助手是"半双工" (tempo não pode dizer),Moshi 实现了"全双工" (tempo não pode dizer),就像人类自然对话 (tempo não pode dizer), assim como o diálogo humano.

**Type:** Learn | **类型:** 学习
**Languages:** Python | **语言:** Python
**Prerequisites:** Phase 6 · 13 (Neural Audio Codecs), Phase 6 · 11 (Real-Time Audio), Phase 7 · 05 (Full Transformer) | **前置知识:** 阶段 6 · 13（神经音频编解码器），阶段 6 · 11（实时音频），阶段 7 · 05（完整 Transformer）
**Time:** ~75 minutes | **预计用时:** ~75 分钟

## O problema é o problema da introdução

Cada agente de voz construído a partir das lições 11 + 12 tem um nível de latência fundamental de cerca de 300-500 ms: incêndios VAD, processos STT, razões LLM, gera TTS. Cada etapa tem sua própria latência mínima. Você pode sintonizar e paralelalizar, mas a forma do pipeline o limita.

> Baseado em 11 e 12                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        

> **【中文解读】**A questão que se coloca neste capítulo é: como entender e aplicar esta tecnologia de forma correta na engenharia real.


Moshi (Kyutai, 2024-2026) faz uma pergunta diferente: e se não houver um pipeline? e se um modelo absorver áudio e emitir áudio diretamente, continuamente, com texto como um "monólogo interno" intermediário em vez de um estágio necessário?

> Moshi ((Kyutai,2024-2026) propôs uma questão diferente: se não houver fluxo de água? se um modelo direto ▌continuamente recebe a transmissão de áudio, o texto é apenas um "interior de um único" e não uma fase necessária?

A resposta é:**full-duplex speech-to-speech**A latença teórica de 160 ms (80 ms Mimi frame + 80 ms atraso acústico) a latença prática de 200 ms em uma única GPU L4.

> A resposta é:**全双工语音到语音**△ teoria延迟 160 ms(80 ms Mimi  + 80 ms 声学延迟) ・・・在单张 L4 GPU 上实际延迟 200 ms──这是最好的流水线语音助手延迟的一半──

## O conceito central.

> **【中文解读】**Este capítulo apresenta os conceitos e teorias fundamentais.


![Moshi architecture: two parallel Mimi streams + inner-monologue text](../assets/moshi-hibiki.svg)

### A arquitetura Moshi

> Moshi 架构

**Inputs.**Dois fluxos de codec Mimi, ambos a 12,5 Hz × 8 codes:

> **输入。**两个 Mimi 编解码器流,均为12.5 Hz × 8 个码本:

- Fluxo 1: áudio do usuário (Mimi-encodado, chegando constantemente)
  Tradução do idioma: user 编码,持续到达)
- Stream 2: Áudio próprio de Moshi (generado por Moshi)
  Tradução do idioma:Moshi 自身的音频 (由Moshi 生成)

**The transformer.**Um Transformador Temporal de parâmetro 7B processa ambos os fluxos e um fluxo de texto "monólogo interno".

> **Transformer。**Um transformer de tempo de 70 bilhões de parâmetros, processando simultaneamente dois fluxos e um fluxo de texto "in-heart-out" em cada 80 ms, ele:

1. Consuma os mais recentes tokens Mimi (8 codes).
   O que é o nome de um usuário?
2. Consume os mais recentes tokens Moshi Mimi (8 codes, conforme produzido).
   Chinese: 漢字字: 漢字: 漢字: 漢字: 漢字: 漢字: 漢字: 漢字: 漢字: 漢字: 漢字: 漢字: 漢字: 漢字: 漢字: 漢字: 漢字: 漢字: 漢字: 漢字: 漢字: 漢字: 漢字: 漢字: 漢字: 漢字: 漢字: 漢字: 漢字: 漢字: 漢字: 漢字: 漢字: 漢字: 漢字: 漢字: 漢字: 漢字: 漢字: 漢字: 漢字: 漢字: 漢字: 漢字: 漢字: 漢字: 漢字: 漢字: 漢字: 漢字: 漢字: 漢字: 漢字: 漢字: 漢字: 漢字: 漢字: 漢字: 漢字: 漢字: 漢字: 漢字: 漢字: 漢字: 漢字: 漢字: 漢字: 漢字: 漢字: 漢字: 漢字: 漢字: 漢字: 漢字: 漢字: 漢字: 漢字: 漢字: 漢字: 漢字: 漢字: 漢字: 漢字: 漢字: 漢字: 漢字: 漢字: 漢字: 漢字: 漢字: 漢字: 漢字: 漢字: 漢字: 漢字: 漢字: 漢字: 漢字: 漢字: 漢字: 漢字: 漢字: 漢字: 漢字: 漢字: 漢字: 漢字: 漢字: 漢字: 漢字: 漢字: 漢字: 漢字: 漢字: 漢字: 漢字: 漢字: 漢字: 漢字: 漢字
3. Gera o próximo token de texto Moshi (monólogo interno).
   No entanto, o que não é verdade é que o que não é verdade.
4. Gera os próximos tokens Moshi Mimi (8 cédulos através de um pequeno Transformador de Profundeza).
   Não é um símbolo de grandeza.

Os três fluxos  áudio do usuário, áudio de Moshi, texto de Moshi  funcionam em paralelo. Moshi pode ouvir o usuário enquanto fala; pode interromper-se quando o usuário interrompe; pode retrocânal ("mhm") sem quebrar sua pronunciação principal.

> Os usuários podem ouvir os usuários ao mesmo tempo que falam; podem interromper-se ao mesmo tempo que o usuário interrompe; podem interromper as principais palavras sem que elas sejam destruídas.

**The depth transformer.**Dentro de um quadro, os 8 codebooks não são previstos em paralelo  eles têm dependências entre os codebooks. Um pequeno "transformador de profundidade" de 2 camadas prevê-los sequencialmente dentro de 80 ms. Esta é a fatorização padrão para os LMs de codec AR (também usado por VALL-E, VibeVoice).

> **深度 Transformer。**Em um 内, 8 码本不是并行预测的它们之间存在码本间依赖. Em um 内, 8 码本不是并行预测的它们之间存在码本间依赖. Em um 内, um pequeno "transformador de profundidade" de 2 níveis, em 80 ms, os pré-pregui em ordem.

### Por que o texto interno do monólogo ajuda

Sem texto explícito, o modelo tem que modelar a linguagem em sua corrente acústica. Moshi: forçá-lo a emitir tokens de texto ao lado do áudio. O fluxo de texto é essencialmente a transcrição do que Moshi está dizendo. Isso melhora a coerência semântica, torna mais fácil trocar uma cabeça de modelo de linguagem e dá-lhe transcrições gratuitamente.

> Por que o texto interno único ajuda: não há texto expresso, o modelo deve ser usado em um processo de construção de linguagem oculta no fluxo sonoro.

### Hibiki: translação de fala em fala em streaming

A mesma arquitetura, treinada em pares de traduções. Áudio de origem, áudio de língua-alvo, continuamente. Hibiki-Zero (Feb 2026) elimina a necessidade de dados de treinamento alinhados a nível de palavras  usa dados de nível de frase + aprendizado de reforço GRPO para otimização de latência.

> Hibiki:流式语音到语音翻译──相同架构,使用翻译对训练──源语言音频输入,目标语言音频输出,持续进行──Hibiki-Zero(2026年 2月) eliminou a necessidade de dados de treinamento em termos de palavras para dados de treinamento

Quatro pares de línguas suportados inicialmente; podem ser adaptados a uma nova língua com ≈1000 horas.

> Inicialmente suportado quatro idiomas; pode ser usado cerca de 1000 horas de dados para se adaptar a novas línguas.

### A pilha mais ampla de Kyutai (2026)

> 更广泛的 Kyutai 技术(2026 年)

- **Moshi** Diálogo duplex completo (em primeiro lugar em francês, com boa assistência em inglês)
  中文翻译:Moshi  全双工对话(法语优先,英语支持良好)
- **Hibiki / Hibiki-Zero** Tradução simultânea de fala
  中文翻译:Hibiki / Hibiki-Zero  同步语音翻译
- **Kyutai STT** RAS de streaming (500 ms ou 2,5 segundos de antecedência)
  中文翻译:Kyutai STT  流式语音识别(500 ms ou 2,5 s 前视)
- **Kyutai Pocket TTS** TTS de 100M-param executado em CPU (Jan 2026)
  Chinese:  1 亿参数 TTS,可在 CPU 上运行(2026 年 1 月)
- **Unmute** um conjunto completo de canais combinando estes em servidores públicos
  Chinese Translation:Unmute  在公共服务器上组合这些组件的完整流水线

Transmissão em uma GPU L40S: 64 sessões simultâneas em 3x em tempo real.

> Na GPU L40S, a velocidade de transmissão é de 64 bits, 3 vezes maior.

### Sesame CSM  o primo

O Sesame CSM (2025) usa uma ideia similar  uma espinha dorsal Llama-3 com uma cabeça de codec Mimi. Mas o CSM é unidirecional (tomando contexto + texto, produz fala) em vez de duplex completo. É o melhor TTS "presença de voz" no mercado; não é o mesmo que a capacidade de duplex completo de Moshi.

> O Sesame CSM(2025) usou uma ideia semelhanteLlama-3 骨干网络 + Mimi 编解码器头── mas o CSM é um único método de "receber" o texto e gerar o idioma, e não o "todo-todo-todo-todo-todo-todo". É o melhor "todo-todo-todo-todo-todo-todo-todo-todo-todo" do mercado; mas não é completamente o mesmo que o TTS de Moshi.

### Números de desempenho 2026

| Model | Latency | Use case | License |
|-------|---------|----------|---------|
| Moshi | 200 ms (L4) | full-duplex English / French dialogue / 全双工英/法对话 | CC-BY 4.0 |
| Hibiki | 12.5 Hz framerate | French ↔ English streaming translation / 法↔英流式翻译 | CC-BY 4.0 |
| Hibiki-Zero | same | 5 language-pairs, no aligned data / 5 语言对，无需对齐数据 | CC-BY 4.0 |
| Sesame CSM-1B | 200 ms TTFA | context-conditioned TTS / 上下文条件 TTS | Apache-2.0 |
| GPT-4o Realtime | ~300 ms | closed, OpenAI API / 闭源，OpenAI API | commercial |
| Gemini 2.5 Live | ~350 ms | closed, Google API / 闭源，Google API | commercial |

> **【中文解读】**Este é um método de "desde zero" que ajuda a entender o princípio da estrutura, não é um problema que se encontra em uma caixa negra.

> **【拓展：语音 AI 的产品化】**A tecnologia de voz enfrenta desafios únicos na produção: diferentes sons, ruídos de contexto, remoção de chamadas, conversas de pessoas, etc. Os produtos de Siri, Alexa, Pequeno Amor e outros são empregados em grande quantidade de engenharia para resolver esses "problemas de longo prazo".

> **【拓展：多语言语音技术】**As características do som de uma língua mundial são enormes: a alta densidade de voz de uma língua (como o chinês) é de baixa capacidade, a falta de dados de treinamento em linguagem.




## Construí-lo e realizei-o.
```figure
sp-fullduplex
```

## Construí-lo

### Passo 1: interface

> 步骤 1: interfaz

Moshi expõe um servidor WebSocket que recebe 80 ms de áudio codificado por Mimi e retorna 80 ms de áudio codificado por Mimi.

> Moshi expõe um WebSocket  servidor, recebe 80 ms de Mimi 编码音频块并返回 80 ms de Mimi 编码音频块──双向,持续进行──

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

### Passo 2: o ciclo duplex completo

> 步骤 2: ciclo de produção total

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

As duas direções executam simultaneamente. Python asyncio ou futuros Rust são o transporte padrão.

> 两个方向同时运行──Python asyncio 或 Rust futures é o método de transmissão padrão──

### Passo 3: objectivo da formação (concepcional)

> 步骤 3: treinamento objetivos

Por cada quadro de 80 ms `t`- Não .

> 对于每80 ms 的 `t`- Não .

- - Introdução:`user_mimi[0..t]`- Não .`moshi_mimi[0..t-1]`- Não .`moshi_text[0..t-1]`
  Tradução:`user_mimi[0..t]`- Não.`moshi_mimi[0..t-1]`- Não.`moshi_text[0..t-1]`
- Previsão: `moshi_text[t]`, então`moshi_mimi[t, codebook_0..7]`
  Tradução do português:`moshi_text[t]`E depois é .`moshi_mimi[t, codebook_0..7]`

O texto é previsto antes do áudio (monólogo interno); o áudio é previsto como sequencial de código dentro do transformador de profundidade.

> 文本在音频之前预测;;内心独白;音频在深度 Transformer 内按码本顺序预测。

### Passo 4: onde o Moshi ganha e onde não ganha

> 步骤 4: Os pontos positivos e os pontos negativos de Moshi

Moshi ganha:

> Os benefícios de Moshi:

- Sub-250 ms de ponta a ponta em hardware barato.
  Tradução do inglês: Incheirés.
- - Cabeça natural e interrupções.
  Tradução do inglês: Natural de contra-ataque e de ruptura.
- Não há código de cola de oleoduto.
  Não é necessário fluir água.

Moshi não ganha:

> Os problemas de Moshi:

- O curso de formação profissional é gratuito e é gratuito.
  Tradução do inglês para tradução do inglês:
- Raciocínio longo (Moshi é um modelo de diálogo 8B, não Claude/GPT-4).
  O Moshi é um modelo de diálogo de cerca de 80 bilhões de dólares, não é Claude/GPT-4)。
- Precisão factual em tópicos de nicho.
  O que é que é o fato de que o homem é um homem?
- A maioria dos casos de utilização das empresas de produção (a seguir a utilizar oleodutos em 2026).
  Chinese:                                                                                                                                                                                                                                                              

> **【中文解读】**Este capítulo mostra como usar um framework maduro (como PyTorch、HuggingFace etc) rápida aplicação desta tecnologia.





> **【拓展：语音与情感计算】**语音 não apenas transmite informações escritas, mas também carrega um rico sinal emocional (语调、语速、音高变化) ◦情感语音识别 (语调、语速、音高变化) ◦情感语音识别 (语音识别, speech emotion recognition, SER) tem uma ampla aplicação em áreas como o controle de qualidade de clientes, a monitorização de saúde mental, a educação inteligente e outras.

## Use-o com o framework implementado.

| Situation | Pick |
|-----------|------|
| Lowest-latency voice companion / 最低延迟语音伴侣 | Moshi |
| Live translation call / 实时翻译通话 | Hibiki |
| Voice demo / research / 语音演示/研究 | Moshi, CSM |
| Enterprise agent with tools / 企业级带工具的 agent | Pipeline（第 12 课），不是 Moshi |
| Custom-voice TTS in context / 上下文中的自定义音色 TTS | Sesame CSM |
| Speech-to-speech, any languages / 任意语言的语音到语音 | GPT-4o Realtime 或 Gemini 2.5 Live（商业） |



## Encurralagens

> 常见陷

- **Limited tool calling.**O Moshi é um modelo de diálogo, não um quadro de agentes.
  Tradução:**有限的工具调用。**Moshi é um modelo de diálogo, não um agente 框架.
- **Specific-voice conditioning.**Moshi usa uma única persona treinada; clonagem é uma corrida de treinamento separada.
  Tradução:**特定语音调节。**Moshi utiliza um único treinamento personalidade; Klon necessita de um processo de treinamento individual.
- **Language coverage.**O francês + inglês é excelente; outros são limitados. Hibiki-Zero ajuda, mas ainda precisa de dados de treinamento.
  Tradução:**语言覆盖。**Français + Inglês表现优秀;其他语言有限──Hibiki-Zero 有帮助,但仍需训练数据──
- **Resource cost.**Uma sessão completa do Moshi tem um slot da GPU; não um padrão de implantação barata de inquilinos compartilhados.
  Tradução:**资源成本。**Uma reunião completa de Moshi ocupa uma GPU; não é um modo de distribuição de aluguel barato.

> **【中文解读】**Este capítulo se concentra em como o modelo será implantado como produto disponível. De modelo original a nível de produção, os sistemas precisam considerar várias dimensões de otimização de desempenho, tratamento de erros, controle, etc.


## Envia-o . Produto .

Salva como`outputs/skill-duplex-pipeline.md`Escolha pipeline versus arquitetura duplex completa para uma carga de trabalho de agente de voz, com razão.

> 保存为 `outputs/skill-duplex-pipeline.md`◊ para um assistente de voz, escolher fluxo de água ou estrutura de trabalho,并说明理由──

## Exercícios.

1. **Easy.**Corra .`code/main.py`Simula simbolicamente a arquitetura de dois fluxos + monólogo interno.
   Tradução:**简单。**运行 `code/main.py`                                                                                                                                                                                                                                                              
2. **Medium.**Pegue Moshi no HuggingFace, execute o servidor, teste uma conversa, mede a latência do relógio de parede do end-of-user speech ao começo da resposta de Moshi.
   Tradução:**中等。**Desde HuggingFace 拉取 Moshi,运行服务器,测试一段对话──测量 desde o usuário语音结束到 Moshi 回复开始的实际延迟──
3. **Hard.**Leve o seu agente de pipeline lição 12 e compare a latência P50 vs Moshi em 20 declarações de teste correspondentes.
   Tradução:**困难。**Use o curso 12 de Assistente de Fluxo de Água e Moshi em 20 条匹配测试语句上比较 P50 延迟―― escrever um relatório que descreve o fluxo de Água em Arquitetura

> **【中文解读】**No 术语表中的"O que as pessoas dizem" vs "O que realmente significa" 区分日常口语和精确技术含义── em equipe,统一术语定义可以避免大量沟通误解──


## Termos-chave .

| Term | What people say | What it actually means |
|------|-----------------|-----------------------|
| Full-duplex | Hear-and-speak at once | Two audio streams active simultaneously on the same model. / 同一模型同时维护两条音频流 |
| Inner monologue | Model's text stream | Moshi emits text tokens alongside its audio output. / Moshi 在音频输出同时输出文本 token |
| Depth transformer | Inter-codebook predictor | Small transformer that predicts 8 codebooks within one 80 ms frame. / 在一个 80 ms 帧内预测 8 个码本的小型 Transformer |
| Mimi | Kyutai's codec | 12.5 Hz × 8 codebooks; semantic+acoustic; powers Moshi. / 12.5 Hz × 8 码本；语义+声学；驱动 Moshi |
| Streaming S2S | Audio → audio live | Chunk-by-chunk translation/dialogue, no pipeline stages. / 逐块翻译/对话，无流水线阶段 |
| Back-channeling | "Mhm" reactions | Moshi can emit small acknowledgments without breaking its turn. / Moshi 可发出小反馈而不打断自己的轮次 |

> **【中文解读】**延伸阅读 fornece recursos de alta qualidade para a aprendizagem profunda.


## Mais leitura 延伸阅读

- [Défossez et al. (2024). Moshi — speech-text foundation model](https://arxiv.org/html/2410.00037v2)- O jornal.
  Défossez 等(2024). Moshi语音-文本基础模型原始论文──
- [Kyutai Labs (2026). Hibiki-Zero](https://arxiv.org/abs/2602.12345) Translação em streaming sem dados alinhados.
  Kyutai Labs ([[2026) ]]). Hibiki-Zero无需对齐数据的流式翻译──
- [Sesame (2025). Crossing the uncanny valley of voice](https://www.sesame.com/research/crossing_the_uncanny_valley_of_voice) Especificidade do CSM.
  Sesame (s) 跨越语音的恐怖谷 (s) 规范 (s) 规范 (s) 规范 (s) 规范 (s) 规范 (s) 规范 (s) 规范 (s) 规范 (s) 规范 (s) 规范 (s) 规范 (s) 规范 (s) 规范 (s) 规范 (s) 规范 (s) 规范 (s) 规范 (s) 规范 (s) 规范 (s) 规范 (s) 规范 (s) 规范 (s) 规范 (s) 规范 (s) 规范 (s) 规范 (s) 规范 (s) 规范 (s) 规范 (s) 规范 (s) 规范 (s) 规范 (s)
- [Kyutai — Moshi repo](https://github.com/kyutai-labs/moshi) instalar + servidor.
  KyutaiMoshi 仓库安装 + 服务器。
- [OpenAI — Realtime API](https://platform.openai.com/docs/guides/realtime)- Peer comercial fechado.
  OpenAIRealtime APIClosed Source Commercial
- [Kyutai — Delayed Streams Modeling](https://github.com/kyutai-labs/delayed-streams-modeling) o quadro STT/TTS sob o capô.
  KyutaiDelayed Streams Modeling底层 STT/TTS 框架──

> **【中文解读】**延伸阅读 forneceu recursos de alta qualidade para a aprendizagem profunda, incluindo artigos, tutoriais e ferramentas.

