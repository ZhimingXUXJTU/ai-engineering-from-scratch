# Modelos Omni: Qwen2.5 Omni e o Pensador-Falar Dividiu .

> A demonstração do produto do GPT-4o em maio de 2024 foi perturbadora não por causa do modelo subjacente, mas por causa da forma do produto  uma interface de voz onde você fala, o modelo vê o que a câmera vê, e fala de volta em menos de 250ms. O ecossistema aberto passou o resto de 2024 e 2025 a correr para alcançar essa superfície do produto. Qwen2.5-Omni (março 2025) é o projeto aberto de referência: um Thinker (grande transformador de geração de texto) mais um Talker (transformador paralelo de geração de voz), ligado por tokens de streaming de fala. Mini-Omni simplificou, Moshi combinou a latência, GLM-4-Voice estendeu para o chinês. Esta lição lê a arquitetura Thinker-Talker e o orçamento de latência que faz com que o diálogo em tempo real funcione.

> **【中文解读】**O avanço do GPT-4o não está no modelo de nível inferior, mas em termos de forma de produto 250ms  ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ 

**Type:** Build
**Languages:** Python (stdlib, streaming pipeline latency simulator + VAD loop)
**Prerequisites:** Phase 12 · 19 (audio-LLMs), Phase 12 · 16 (any-to-any)
**Time:** ~180 minutes

> - Não .**【前置】**学本节前请先掌握:Fase 12·16(MIO 任意到任意流式)、Fase 12·19(音频 LLM)、Fase 6·04(VAD 语音活动检测)。Qwen2.5-Omni = "开源版 GPT-4o",核心是思想家讲者 双流架构,并行化降低延迟到250ms 内。
> - Não .**【类比】**Pensador-falantes 架构 = "翻译员 + 同传播音员"。其他 omni 模型 = 一个人又要思考又要说话(串行,慢);Qwen2.5-Omni = Pensador(大脑,想"说什么")+ Falare(嘴巴,把文字变语音)并行工作。Thinker 流式吐出文本代币,Talker 一边接收一边合成语音,用户听到的是流水线输出,总延迟大幅降低。

## Objetivos de aprendizagem

- Divida o pipeline de inferência em Thinker (razão de texto) e Talker (sinteze de fala) e explique por que o streaming paralelo funciona.
  Tradução do inglês para tradução do inglês para tradução do inglês para tradução do inglês para tradução do inglês para tradução do inglês para tradução do inglês para tradução do inglês para tradução do inglês para tradução do inglês para tradução do inglês para tradução do inglês para tradução do inglês para tradução do inglês para tradução do inglês para tradução do inglês para tradução do inglês para tradução do inglês para tradução do inglês para tradução do inglês para tradução do inglês para tradução do inglês para tradução do inglês para tradução do inglês para tradução do inglês para tradução do inglês para tradução do inglês para tradução do inglês para tradução do inglês para o inglês para o inglês para o inglês para o inglês para o inglês para o inglês para o inglês para o inglês para o inglês para o inglês para o inglês para o inglês para o inglês para o árabe para o árabe para tradução do inglês para o árabe para o árabe para o árabe para o árabe para o árabe para o árabe para o árabe para o árabe para o árabe para o árabe.
- Calcular o orçamento de tempo para primeiro byte de áudio (TTFAB) para uma interação de conversação, componente por componente.
  Tradução do inglês para o inglês: 字节时间 (TTFAB) 预算──
- Descreva a posição alinhada com o tempo do TMRoPE codificando visão, áudio e texto dentro do Pensador.
  Tradução do inglês para o inglês: Thinker in TMRoPE 跨视觉、音频和文本的时间对齐位置编码──
- Nomear os três padrões de conversação em tempo real: meio duplex, turno-tomando, duplex completo.
  O que é um diálogo de dois dias?

## O problema é o problema da introdução

Um assistente de voz em tempo real tem que fazer muito, rápido:

> O assistente de voz precisa de fazer muitas coisas rapidamente.

1. Ouça o usuário. Tokenização de fala em tempo real, detecção de atividade vocal (VAD) para saber quando terminam de falar.
   中文翻译:听用户说话──实时语音分词化,语音活动检测(VAD) julgar usuário何时说完──
2. A entrada da câmera a 2 a 4 FPS, fluída para o Thinker ao lado do áudio.
   Tradução do inglês:                                                                                                                                                                                                                                                            
3. Pense, escreva uma resposta condicionada ao histórico da conversa.
   Tradução do inglês para tradução inglesa:
4. Sintetizar tokens de áudio, decodificar para forma de onda, transmitir para os alto-falantes do usuário.
   Tradução do inglês para o português: 語語, 語, 語, 語, 語, 語, 語, 語, 語, 語, 語, 語, 語, 語, 語, 語, 語, 語, 語, 語, 語, 語, 語, 語, 語, 語, 語, 語, 語, 語, 語, 語, 語, 語, 語, 語, 語, 語, 語, 語, 語, 語, 語, 語, 語, 語, 語, 語, 語, 語, 語, 語, 語, 語, 語, 語, 語, 語, 語, 語, 語, 語, 語, 語, 語, 語, 語, 語, 語, 語, 語, 語, 語, 語, 語, 語, 語, 語

Cada passo adiciona latência. A sensação de conversação requer total de ida e volta < 500ms  abaixo disso, o usuário deixa de notar o atraso. GPT-4o afirma ~250ms. Moshi ~160ms. Qwen2.5-Omni ~350-500ms.

> Cada passo aumenta o atraso. O requisito de diálogo é de volta ao ar.

Nada pode ser "batch everything then decode".

> Cada componente precisa de tratamento fluido. Não pode ser "processado em bateria antes de terminar a sua análise".

## O conceito central.

> **【中文解读】**O pensador-falante 架构将"思考" (pensar) e "说话" (fazer)

> **【拓展：实时多模态交互**GPT-4o é o primeiro modelo de interação real-tempo multi-modelo real: usuário pode fazer perguntas de voz, o modelo pode ver simultaneamente imagens de fotografia, responder em tempo real de voz.


### Pensador e Falador

A decomposição do Qwen2.5 Omni:

> Qwen2.5-Omni 的分解:

- Pensador: um transformador de geração de texto 7B-80B. Consome tokens de texto + imagem + áudio entrelaçados.
  Tradução do inglês:Thinker:7B-80B 文本生成 Transformer──消费交错的文本+图像+音频 token──输出代表"说什么"的文本 token──
- Falante: um transformador gerador de fala menor (200M-1B). Consome os tokens de saída de texto do Thinker além de tokens recentes de contexto de fala.
  Tradução do inglês para tradução do português: Tradução do inglês para tradução do português: Tradução do inglês para tradução do português: Tradução do inglês para tradução do português: Tradução do inglês para tradução do inglês: Tradução do inglês para tradução do inglês: Tradução do inglês para tradução do inglês: Tradução do inglês: Tradução do inglês: Tradução do inglês: Tradução do inglês: Tradução do inglês: Tradução do inglês: Tradução do inglês: Tradução do inglês: Tradução do inglês: Tradução do inglês: Tradução do inglês: Tradução do inglês: Tradução do inglês: Tradução do inglês para tradução do inglês: Tradução do inglês para tradução do inglês: Tradução do inglês para tradução do inglês para tradução do inglês para tradução do inglês: Tradução do inglês para tradução do inglês para tradução do inglês para tradução do inglês para tradução do inglês: Tradução do inglês para tradução do inglês para tradução do inglês para o que significa "VQ" (残差差差差 VQ 索引引引引引引引引引引引引引引引引引引引引引引引引引引引引引引引引引引引引引引引引引引引引引引引引引).
- Decodificador de voz: um decodificador de forma de onda de streaming (SNAC, família MoVQGAN) que leva tokens de voz para amostras de áudio em tempo real.
  Tradução do inglês em língua portuguesa: 流式波形解码器 (SNAC、MoVQGAN 系列),实时将语音代币 转为音频样本。

A separação é importante. O pensador tem que ser grande para um bom raciocínio. O conversador pode ser pequeno porque seu trabalho é local  converter texto em tokens de fala. O grande conversador não é mais expressivo; é mais lento.

> O pensador deve ter grande talento para fazer uma boa reflexão. O falante pode ser pequeno porque sua tarefa é a de um local.

- Elas estão em paralelo.

> E não é o caso.

1. O pensador emite um sinal de texto.
   Tradução do inglês: Thinker 输出文本代号 t_i。
2. O falante consome t_i (via streaming) e emite tokens de fala s_i, s_{i+1}, ..., s_{i+k}.
   Tradução do idioma: "São os seus próprios"
3. O decodificador de voz consome tokens de voz à medida que eles chegam e emite amostras de áudio.
   Tradução do inglês para inglês: Chinese language language language language language language language language language language language language language language language language language language language language language language language language language language language language language language language language language language language language language language language language language language language language language language language language language language language language language language language language language language language language language language language language language language language language language language language language language language language language language language language language language language language language language language language language language language language language language language language language language language language language language language language language language language language language language language language language language language language language language language language language language language language language language language language language language language language language language language language language language language language language language language language language language language language language language language language language language language language language language language language language language language language language language language language language language language language language language language language language language language language language language language language language language language language language language language language language language language language language language language language language language language language language language language language language language language language language language language language language language language language language language language language language language language language language language language language language language language language language language language language language language language language language language language language language language language language language language language language language language language language language language language language language language language language language language language language language language language language language language language language language language language language language language language language language language language language language language language language language language language language language language language language language language language language language language language language language language language language language language language language language language language language language language language language language language language language language language language language language language language language language language language language language language language language language language language language language language language language language language language language language language language language language language language language language language language language language language language language language language language language language language language language language language language language language language language language language language language language language language language language language language language language language language language language language language language language language language language language language language language language language language language language language language language language language language language language language language language language language language language language language language language language language language language language language language language language language language language language language language language language language language language language language language language language language language language language language language language language language language language language language language language language language language language language language language language language language language language language language language language language language
4. Quando o Thinker está no token de texto, o Talker já transmitiu áudio para t_0..t_{i+2}.
   Quando o pensador está em processamento de textos, o orador já está em transmissão.

> **【中文解读】**O pensador 必須大 ((7B-80B) 才能做好推理,Talker 可以小 ((200M-1B) 由于它的任务是局部的文本转语音符号──更大的Talker 不会有更大的表现力,只会更慢──并行运行时,当 Thinker 在生成第一个i+3文本符号时,Talker 已经播放第一个到第一个i+2文本对应的音频──

> **【拓展：Token 速率数学】**16kHz 语音使用50Hz 基础语音代币, significa que por segundo é necessário 50 语音代币――Speaker cada segundo deve emitir >= 50 token 才能跟上──在H100 上,200-300M 语音的讲者每秒可输出数百 token,远超需求;但7B 语音会跟不上──这就是为什么需要专用小讲者模型而不是直接使用主模型──

### Posições multimodal TMRoPE  alinhadas no tempo

O pensador precisa integrar quadros de imagem (que chegam a, digamos, 4 FPS), quadros de áudio (que chegam a 50 quadros/segundo) e texto do histórico de conversação.

> Pensador 需要整合图像((tal como 4 FPS) 音频(50 /秒) 和对话历史中的文本──简单序列顺序──所有图像──然后所有音频──然后文本) 会丢失时间对齐──

TMRoPE atribui timestamps absolutos a cada token. token de visão em t = 2,3s. token de áudio em t = 2,32s. token de texto do usuário "stop" em t = 2,35s. RoPE gira a atenção por timestamp; o modelo vê-los como temporariamente simultâneos.

> TMRoPE para cada token distribuído absolutamente tempo──visão token 在 t=2.3s──音频 token 在 t=2.32s──user's"stop"文本 token 在 t=2.35s──RoPE 按时间旋转注意力;模型将它们视为时间同时发生──

Esta é a infraestrutura para "ele acenou enquanto dizia olá" para funcionar  o modelo vê o quadro de vídeo e o áudio no mesmo momento conceitual.

> É "Ele está a dizer que você está bem" que pode funcionar normalmente infraestrutura.

### Sintese de fala em streaming

Tokens de fala devem ser transmitidos. Mini-Omni (Xie & Wu, 2024) introduziu "modelos de linguagem podem ouvir, falar enquanto pensam em streaming": Tokens de saída do pensador e tokens de saída do conversador interceptam-se na mesma sequência.

> 语音代币 必须流式传输──Mini-Omni 引入了"语言模型可以在流式思考的同时听和说":Thinker 输出代币 和 Talker 输出代币 在同一序列中交错──Thinker 一旦提交下一个文本代币,Talker 立即触发──没有批量边界──

Moshi (Défossez et al., outubro 2024) é a implementação aberta mais rápida. 160ms TTFAB em um único A100. Arquitetura: um único transformador 7B que emite tokens de texto e fala em posições alternadas, com um "monólogo interno" que separa o fluxo de pensamento do fluxo de fala.

> Moshi é a mais rápida implementação de código aberto. A estrutura: um único transformador 7B em troca de saída de texto e de voz, com "interior de um único" separado de fluxo de pensamento e de fala.

### VAD e viragem

A detecção da atividade vocal é executada no lado de entrada.

> 语音活动检测在输入端运行──两种模式:

- Meio duplex: usuário fala, modelo ouve. Modelo fala, usuário ouve. Transferência clara através da detecção de silêncio VAD (~ 200ms).
  Tradução do português: 半双工: user说话,模型听──模型说话,用户听──通过 VAD 静音检测(约200ms)
- Duplex completo: ambos podem falar simultaneamente. Modelo pode backchannel ("uh-huh") ou interromper. Muito mais difícil. Moshi suporta isso.
  O modelo pode voltar a falar em simultâneo.

Qwen2.5 Omni suporta meio duplex por padrão, com a tomada de turno através do limiar de silêncio.

> Qwen2.5 Omni 默认支持半双工,通过静音值实现轮流──全双工需要应用层处理──

### Qwen3-Omni (novembro 2025)

O sucessor. Qwen3-80B Thinker, maior Talker, melhorou TMRoPE-v2. Latência próxima a 250ms de GPT-4o. Pesos abertos. Benchmarks em OmniBench competitivo com Gemini 2.0 Live.

> 继任者──Qwen3-80B Thinker, Greater Talker,改进的TMRoPE-v2──延迟接近 GPT-4o 的250ms──开放权重──OmniBench 基准与 Gemini 2.0 Live 竞争──

### Orçamento de latência de produção

Para uma interação de streaming típica:

> 典型流式交互:

- Mic -> tokens de áudio: 40-80ms.
  O que é o "tôquio de rádio"?
- Preenchimento (promete + histórico): 100-200 ms em 7B, muito mais em 70B.
  Tradução do inglês:                                                                                                                                                                                                                                                            
- Primeiro token de texto do Thinker: 40ms.
  Tradução do inglês: 首个 Thinker 文本代币:40ms。
- Talker processar o primeiro token de texto: 20ms.
  Tradução do idioma: "Palavras"
- Primeiros tokens de fala comprometem-se: 40ms.
  Tradução do inglês:首个语音代币 提交:40ms。
- Decodificação residual-VQ: 30 ms.
  O que é que você está fazendo?
- Decodificação de forma de onda de fala: 50-80ms.
  Tradução do português:语音波形解码:50-80ms。

TTFAB total: 320-510ms em 7B, 600-900ms em 70B. A qualidade de fronteira geralmente significa 70B +; portanto, a diferença de latência de fronteira.

> 总 TTFAB:7B 约 320-510ms,70B 约 600-900ms──前沿质量通常意味着70B+;因此存在前沿延迟差距──

### Matemática de taxa de tokens

Em 16kHz de fala com 50 Hz de tokens de fala base, você precisa de 50 tokens de fala por segundo de saída. O falante deve emitir ≥ 50 tok/s para acompanhar. Em um rendimento típico de LLM de 30-80 tok/s em um H100, um pequeno (200-300M) falante é rápido o suficiente; um 7B falante ficaria para trás.

> 16kHz 语音以 50 Hz 基础语音代号 计算, per second output needs 50 语音代号──Talker 必须以 ≥50 tok/s 的速度输出──H100 上典型 LLM 吞吐量为 30-80 tok/s,小型(200-300M)Talker 足够快;7B Talker 会跟不上──

É por isso que existem pequenos modelos dedicados Talker em vez de "apenas usar o modelo principal".

> É por isso que existe um modelo de conversador pequeno e não um modelo principal de uso direto.

## Use-o com o framework implementado.
```figure
l5-thinker-talker
```

## Usá-lo

`code/main.py`- Não .

- Simula um pipeline Thinker-Talker com taxas de emissão de tokens falsas.
  Tradução do inglês para inglês: using模拟的代币 输出速率模拟思维者-谈话者管道
- Computa TTFAB para tamanhos de modelos configuráveis e taxas de amostragem de microfones.
  Tradução do inglês para tradução do inglês para tradução do inglês para tradução do inglês para tradução do inglês para tradução do inglês para tradução do inglês para tradução do inglês para tradução do inglês para tradução do inglês para tradução do inglês para tradução do inglês para tradução do inglês para tradução do inglês para tradução do inglês para tradução do inglês para tradução do inglês para tradução do inglês para tradução do inglês para tradução do inglês para o inglês para tradução do inglês para o inglês para tradução do inglês para o inglês para o inglês para tradução do inglês para o inglês para o inglês para o inglês para o inglês para o inglês para o inglês para o inglês para o inglês para o inglês para o inglês para o árabe para o árabe para o árabe para o árabe para o árabe para o árabe para o árabe para o árabe para o árabe para o árabe para o árabe:
- Demonstra uma rotação de meio duplex com um limiar de silêncio VAD.
  Tradução do inglês para tradução livre:

## Envia-o . Produto .

Esta lição produz`outputs/skill-omni-streaming-budget.md`. Tendo em conta o objetivo TTFAB e o conjunto de recursos (visão, bilíngue, duplex completo) de um produto de voz em tempo real, escolhe Qwen2.5-Omni, Qwen3-Omni, Moshi ou Mini-Omni e dimensionar o Thinker/Talker.

> 本课产 出 `outputs/skill-omni-streaming-budget.md`△ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △                                                                        

## Exercícios.

1. Seu objetivo TTFAB é de 300ms. Em um 7B Thinker e 300M Talker, escreva a latência de cada componente.

2. Qwen2.5-Omni usa TMRoPE. Descreva o que o modelo vê para um prompt em que o usuário começa a falar em t=1s e a câmera capta um gesto em t=1.2s. Qwen2.5-Omni utiliza TMRoPE。 descrição modelo em usuário t=1s 开始说话、摄像头 t=1.2s 捕获手势时看的输入。

3. O suporte de duplex completo requer que o modelo emite áudio enquanto ouve. Proponha um formato de dados de treinamento que ensine isso.

4. Leia o artigo de Moshi Secção 4. Descreva a separação do "monólogo interno" e por que evita a divisão Pensador-Palavoro.

5. Calcule o orçamento de transferência: a que velocidade um Talker deve emitir tokens para acompanhar a fala de 16kHz a 50 tokens de camada base/segundo? 计算吞吐量预算:Talker 需要多快的速度输出 token 才能跟上 16kHz 语音(50 基础层 token/秒)?

## Termos-chave .

| Term | What people say | What it actually means | 中文释义 |
|------|-----------------|------------------------|---------|
| Thinker | "Reasoning brain" 思考者 | Large text-generating transformer producing what to say 生成"说什么"的大型文本生成 Transformer | |
| Talker | "Speech-generating mouth" 说话者 | Small transformer producing discrete speech tokens from Thinker's text 将 Thinker 文本转为语音 token 的小型 Transformer | |
| TTFAB | "Latency budget" 首音频字节延迟 | Time-to-first-audio-byte: from user speech end to first audio sample out 从用户说话结束到首个音频样本输出的延迟 | |
| TMRoPE | "Time-aligned RoPE" 时间对齐旋转位置编码 | Position encoding using absolute timestamps across vision, audio, text 跨视觉、音频、文本使用绝对时间戳的位置编码 | |
| Half-duplex | "Turn-taking" 半双工 | User and model alternate; VAD silence detects user-done 用户和模型交替说话；VAD 静音检测用户说完 | |
| Full-duplex | "Simultaneous" 全双工 | Model can speak and listen at the same time; backchannel capable 模型可同时说话和监听；支持回话 | |
| Inner monologue | "Moshi separation" 内心独白 | Single-model design where thinking-stream and speaking-stream interleave 单模型设计，思考流和说话流交替出现 | |

## Mais leitura 延伸阅读

- [Xu et al. — Qwen2.5-Omni (arXiv:2503.20215)](https://arxiv.org/abs/2503.20215)
- [Qwen Team — Qwen3-Omni (arXiv:2509.17765)](https://arxiv.org/html/2509.17765v1)
- [Xie & Wu — Mini-Omni (arXiv:2408.16725)](https://arxiv.org/abs/2408.16725)
- [Défossez et al. — Moshi (arXiv:2410.00037)](https://arxiv.org/abs/2410.00037)
- [Zeng et al. — GLM-4-Voice (arXiv:2412.02612)](https://arxiv.org/abs/2412.02612)
