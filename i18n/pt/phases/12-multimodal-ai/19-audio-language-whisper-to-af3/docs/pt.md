# Modelos de áudio-linguagem: o sussurro para áudio flamingo 3 arc .

> Whisper (Radford et al., dezembro de 2022) resolveu o reconhecimento de fala  680k horas de fala multilingue deficiente, um simples transformador de codificador-decodificador, um ponto de referência que fez com que cada versão subsequente da ASR o citasse. Mas reconhecer não é raciocínio. Perguntar "que instrumentos estão nesta gravação" ou "que emoção o orador está expressando" ou "o que aconteceu no minuto 3" requer entendimento de áudio, não transcrição. Qwen-Audio, SALMONN, LTU e o Audio Flamingo 3 da NVIDIA (AF3, julho 2025) construíram progressivamente essa pilha: manter os codificadores da classe Whisper, ligar os Q-formadores, treinar dados de instrução de texto de áudio, adicionar raciocínio de cadeia de pensamento. Esta lição vai no arco.

> **【中文解读】**O Whisper resolveu a identificação de idiomas, mas o reconhecimento não é uma hipótese. Este episódio de gravação usava um instrumento, um discurso, um sentimento, um sentimento, um sentimento, um sentimento, um sentimento, um sentimento, um sentimento, um sentimento, um sentimento, um sentimento, um sentimento, um sentimento, um sentimento, um sentimento, um sentimento, um sentimento, um sentimento, um sentimento, um sentimento, um sentimento, um sentimento, um sentimento, um sentimento, um sentimento, um sentimento, um sentimento, um sentimento, um sentimento, um sentimento, um sentimento, um sentimento, um sentimento, um sentimento, um sentimento, um sentimento, um sentimento, um sentimento, um sentimento, um sentimento, um sentimento, um sentimento, um sentimento, um sentimento, um sentimento, um sentimento, um sentimento, um sentimento, um sentimento, um sentimento, um sentimento, um sentimento, um sentimento, um sentimento, um sentimento, um sentimento, um sentimento, um sentimento, um sentimento, um sentimento, um sentimento, um sentimento, um sentimento, um sentimento, um sentimento, um sentimento, um sentimento, um sentimento, um sentimento, um sentimento, um sentimento, um sentimento, um sentimento, um sentimento, um sentimento, um sentimento, um sentimento, um sentimento, um sentimento, um sentimento, um sentimento, um sentimento, um sentimento, um sentimento, um sentimento, um sentimento, um sentimento, um sentimento, um sentimento, um sentimento, um sentimento, um sentimento, um sentimento, um sentimento, um sentimento, um sentimento, um sentimento, um sentimento, um sentimento, um sentimento, um sentimento, um sentimento, um sentimento, um sentimento, um sentimento, um sentimento, um sentimento, um sentimento, um sentimento, um sentimento, um sentimento, um sentimento, um sentimento, um sentimento, um sentimento, um sentimento, um sentimento, um sentimento, um sentimento

**Type:** Build
**Languages:** Python (stdlib, log-Mel spectrogram + audio Q-former skeleton)
**Prerequisites:** Phase 6 (Speech and Audio), Phase 12 · 03 (Q-Former)
**Time:** ~180 minutes

> - Não .**【前置】**學本节前请先掌握:Fase 6·01-02(语音信号处理:FFT/Mel 频谱图/Whisper);Fase 12·03(Q-Former 桥接,本节复用为音频 Q-Former);Fase 7(Transformer 编码器-解码器)。音频 LLM = 视觉 LLM 的"听觉版",只是输入从图像补丁 变成 Mel 频谱图补丁──
> - Não .**【类比】**音频 LLM = "为 LLM 装耳朵"──Whisper = 助听器(只能转录不能思考); SALMONN = 聋学校的翻译员(Whisper 转录→LLM 思考);AF3 = 直接给 LLM 装耳(端到端听+想+答)──端到端的好处:能捕捉转录丢失的信息(语调、情绪、停顿), estes são os principais fatores da raciocínio──

## Objetivos de aprendizagem

- Compute um espectrograma log-Mel a partir de uma forma de onda: ventana, FFT, bancos de filtros, transformação de log.
  Tradução do português: 波器组、对数变换──
- Compare as opções de codificadores: Whisper encoder, BEATs, AF-Whisper híbrido.
  中文翻译:比较编码器选项:Whisper 编码器、BEATs、AF-Whisper 混合──各自何时胜出──
- Construa um formato de áudio Q: N consulta aprendizagem atendendo aos patches do espectrograma.
  Tradução do inglês: Construir o freqüência de gravações
- Explique a formação em cascata (Whisper-then-LLM) versus end-to-end audio-LLM: por que a escala end-to-end é melhor para o raciocínio.
  Tradução do inglês para tradução do inglês para tradução do inglês para tradução do inglês para tradução do inglês para tradução do inglês para tradução do inglês para tradução do inglês para tradução do inglês para tradução do inglês para tradução do inglês para tradução do inglês para tradução do inglês para tradução do inglês para tradução do inglês para tradução do inglês para tradução do inglês para tradução do inglês para tradução do inglês para tradução do inglês para tradução do inglês para tradução do inglês para tradução do inglês para tradução do inglês para tradução do inglês para tradução do inglês para o inglês para o inglês para o inglês para o inglês para o inglês para o inglês para o inglês para o inglês para o inglês para o inglês para o inglês para o árabe para o árabe para o árabe para o árabe para o árabe para o árabe para o árabe para o árabe para o árabe para o árabe para o árabe para o árabe para o árabe: , tradução do árabe para tradução do árabe para tradução do árabe para tradução do árabe para tradução do árabe para tradução do árabe para tradução do árabe para árabe para árabe para árabe para árabe: 

## O problema é o problema da introdução

O reconhecimento de fala foi resolvido por Whisper. O OCR de áudio é uma mercadoria. Mas " mercadoria " pára na transcrição. Se o modelo não consegue raciocinar sobre o que ouviu  tempo, alto-falantes, emoção, estrutura musical, sons ambientais  transcrição sozinha não pode impulsionar as características do produto.

> 语音识别已被语音识别已被语音识别已被语音识别已被语音识别已成为基础能力──但"基础能力"止步于转录──如果模型无法推理所听的内容时刻、说话人、情绪、音乐结构、环境声只靠转录无法驱动产品功能──

Três rotas óbvias:

> 3 条                                                                                                                                                                                                                                                              

1. Cascade: Whisper transcribe, LLM argumenta sobre a transcrição. Funciona para cenários de fala pura. Falha para música, áudio ambiental, superposição de multi-falantes, emoção.
   O texto original é escrito em língua portuguesa, mas não é escrito em língua portuguesa.

2. End-to-end audio-LLM: um codificador de áudio alimenta tokens de áudio diretamente em um LLM, ignorando a transcrição. Preserva informações acústicas (emoção, alto-falante, ambiente). Necessita de novos dados de treinamento.
   Tradução do inglês para tradução do inglês para tradução do inglês para tradução do inglês para tradução do inglês para tradução do inglês para tradução do inglês para tradução do inglês para tradução do inglês para tradução do inglês para tradução do inglês para tradução do inglês para tradução do inglês para tradução do inglês para tradução do inglês para tradução do inglês para tradução do inglês para tradução do inglês para tradução do inglês para tradução do inglês para tradução do inglês para inglês para tradução do inglês para inglês para tradução do inglês para inglês para tradução do inglês para inglês para inglês para tradução do inglês para inglês para inglês para inglês para inglês para inglês para inglês para inglês para inglês para inglês para inglês para inglês para inglês para inglês para inglês para inglês para inglês para inglês para inglês para inglês para inglês

3. Híbrido: codificador de áudio + decodificador de texto que pode transcrever e raciocinar.
   Tradução do inglês: Mixed:音频编码器 + 文本解码器,既能转录又能推理──Qwen-Audio 和 Audio Flamingo 选择此路径──

## O conceito central.

> **【中文解读】**O modelo de linguagem é fundamental para a identificação de voz. A nova geração de modelos não só pode transcrever, mas também pode compreender o conteúdo do som.

> **【拓展：语音 AI 的前沿**Whisper-large-v3  suportar cerca de 100 种语言的语音识别──2024-2025 趋势是语音大模型:GPT-4o 原生语音输入输出(延迟约 320ms),Gemini's实时语音对话,ElevenLabs's语音克隆──AudioFlamingo em sua tarefa de entendimento de áudio频, alcança SOTA, capaz de responder aos problemas complexos sobre música e som──


### Espectograma log-Mel: a função de entrada

Cada codificador de áudio começa com a mesma característica: um espectrograma log-Mel.

> Cada um deles tem a mesma característica.

1. Re-estampagem a 16 kHz.
   Tradução do português:重采样至16 kHz。
2. Transformação Fourier de curto prazo com janelas de 25 ms, salto de 10 ms.
   Tradução do inglês:短时里叶变换,25ms 窗口,10ms 步长。
3. Tomar a magnitude do resultado da FFT.
   Chinese: 取 FFT 结果的幅度──
4. Aplicar bancos de filtros Mel (normalmente 80 filtros com espaço de registro de 0-8000 Hz) para distorcer a frequência perceptiva.
   Em inglês, a aplicação Mel 波器组 (normalmente 80 个波器, em intervalos de 0-8000 Hz) é feita de modo que a frequência de detecção seja menor.
5. Compressão de log (log(1 + x)) para o intervalo dinâmico.
   Tradução do inglês para tradução do inglês para inglês para tradução do inglês para inglês para tradução do inglês para inglês para inglês para tradução do inglês para inglês para inglês para inglês para inglês para inglês para inglês para inglês para inglês para inglês para inglês para inglês para inglês para inglês para inglês para inglês para inglês para inglês para inglês para inglês para inglês para inglês para inglês para inglês para inglês para inglês para inglês para inglês para inglês para inglês para inglês para inglês para inglês para inglês para inglês para inglês para inglês para inglês para inglês para inglês

Resultado: uma matriz 2D de forma (T, 80) onde T é o número de quadros de tempo. Para um clip de 30 segundos a frequência de quadros de 100 Hz: (3000, 80).

> Resultado: números 2D de forma (T, 80) em que T é tempo  número──30 秒片段在 100 Hz 率下:(3000, 80)──

### O codificador do sussurro

O codificador do Whisper é um transformador de estilo ViT de 12 camadas que processa o espectrograma log-Mel como uma sequência de quadros de tempo.

> Whisper é um transformer de 12 níveis ViT 风格, que será log-Mel 频谱图作为时间序列处理――输出:每个时间一个隐藏状态向量――

Para ASR, o decodificador do Whisper é um transformador de atenção cruzada que gera tokens de texto condicionados à saída do encodificador.

> Para ASR, Whisper é um transformer de atenção de um modo que é um símbolo de código-fonte.

Para ALMs (audio-LLMs), você quer a saída do codificador como entrada para um LLM diferente. O padrão: Whisper encoder congelado, Q-former treinable, LLM congelado ou sintonizado.

> 对于ALM(音频 LLM),需要将编码器输出作为另一个LLM的输入──模式:Whisper 编码器结,Q-former 可训练,LLM 结或微调──

### Codificadores de áudio específicos

O Whisper foi treinado com dados dominantes da fala. É mais fraco para música e áudio ambiental.

> Fosseiro em dados de voz dominados em treino.

O BEATs (Chen et al., 2022) é um transformador auto-supervisionado treinado no AudioSet. Captura música e sons ambientais melhor do que o Whisper no mesmo número de parâmetros.

> BEATs(Chen 等人,2022) é um Transformador de Auto-Supervisão treinado em AudioSet.

AF-Whisper (Híbrido do Audio Flamingo 3): Whisper + BEATs concato funciona como entrada de áudio.

> AF-Whisper(Audio Flamingo 3 的混合方案):拼音 Whisper + BEATs 特征作为音频输入──Whisper 携带语言信号,BEATs 携带声学信号──

### Audio Q-former

O mesmo padrão que o visual Q-former do BLIP-2. um número fixo de consultas aprendíveis (muitas vezes 32 ou 64) atender cruzada sobre os quadros de saída do codificador de áudio. As consultas se tornam tokens de áudio consumidos pelo LLM.

> Com a visão Q-former similar modelo. Uma quantidade fixa de perguntas que podem ser aprendidas (normalmente 32 ou 64) sobre a saída de um editador de som.

Estágio de alinhamento de formação: Q-former sozinho, perdas contraditórias + de legendas em pares de texto e áudio (AudioCaps, Clotho).

> 訓練對齐阶段:仅 Q-former,音频-文本对上对比+描述损失(AudioCaps、Clotho) 』 instrução阶段:端到端,解 LLM,在指令数据上训练──

### O arco  SALMONN, Qwen-Audio, AF3

SALMONN (Tang et al., 2023): Whisper + BEATs + Q-former + LLaMA. O primeiro LLM de áudio aberto com capacidade de raciocínio sério.

> SALMONN(Tang 等人,2023):Susper + BEATs + Q-former + LLaMA。

Qwen-Audio (Chu et al., 2023): arquitetura similar, treinada em um conjunto de dados mais rico, sintonizada para diálogo de várias voltas. MMAU ~ 0,60.

> Qwen-Audio(Chu 等人,2023): similar architecture, em mais rico de dados, treinamento, para o diálogo em várias rotas optimization──MMAU 约 0.60──

LTU  Ouça, pense, compreenda (Gong et al., 2023): dados de raciocínio explícito, foque na cadeia de pensamento em cima de clips de áudio.

> LTU听、想、理解(Gong 等人,2023): evidentes dados de reflexão, focado em pensamentos em cadeia em episódios de rádio.

Audio Flamingo 3 (Goel et al., julho 2025): a atual SOTA aberta. 8B LLM backbone (Qwen2 7B), Whisper-large encoder concat BEATs, 64 query Q-former, treinamento em 1M + pares de instrução de áudio-texto. MMAU 0.72, combina fronteira proprietária em algumas sub-tarefas.

> Audio Flamingo 3(Goel 等人,2025年7月):当前开放 SOTA──8B LLM 主干(Qwen2 7B),Whisper-large 编码器拼接 BEATs,64 查询 Q-former,在100万+音频-文本指令对上训练──MMAU 0.72,在某些子任务上匹配闭源前沿──

AF3 também introduz uma cadeia de pensamento sob demanda para áudio: o modelo pode emitir tokens de pensamento opcionalmente ("deixe-me identificar os instrumentos primeiro: ...") antes da resposta final.

> AF3 também introduziu press demand audio频思维链: modelo pode ser usado em resposta final antes de escolher para fazer um token de pensamento ("já me identificou primeiro o instrumento:...")

### Cascada vs end-to-end

Tubos em cascata:

> O sistema de transporte de energia

1. Whisper transcreve áudio → texto.
   Chinese:                                                                                                                                                                                                                                                              
2. - O LLM é por texto.
   Tradução do português em inglês:

Funciona perfeitamente para "resumir este podcast". Falha para:
- "Qual é o humor desta música?"  O humor está no som, não nas palavras.
- "Quem está falando, Alice ou Bob?"  requer identificação do orador.
- "Em que segundo acontece a explosão?" "A terra temporal perdida no texto".
- "É real ou gerado áudio?"  Detecção de deepfake precisa de recursos acústicos.

> Para "总结这个播客" é perfeitamente adequado.
> - "O que é o sentimento desta canção?"
> - "Quem está falando, Alice ou Bob?"
> - "Explode em segundos?" Perdeu o tempo no texto.
> - "É verdade ou é de origem?"

Qwen-Audio e AF3 lidam com música, ambiente e emoção de forma nativa.

> 端到端保留声学信号──Qwen-Audio 和 AF3 原生处理音乐、环境和情绪──

> **【中文解读】**级联管道 (Whisper 转录→LLM 推理) é adequado a um simples cenário de som, como resumo de um programa, mas não pode lidar com a música, a identificação de pessoas, a localização do tempo, a análise de falsificação profunda, etc.

> **【拓展：金融场景的音频理解】**No campo financeiro, o entendimento de rádio pode ser usado para: análise emocional de reuniões de telefonia financeira ( não apenas tradução de texto, também de linguagem e de fala)  reconhecimento de instruções de voz do comerciante  controlo de qualidade do cliente  análise emocional de conversas de reuniões  separação de pessoas  canais de comunicação não conseguem captar esses sinais de nível de audição 

### 2026 receita de produção

Para um novo produto de audiovisão:

> 对于新音频理解产品:

- Cascada se: transcrição é o objetivo, sem música, sem inferência emocional.
  Se o objetivo é transferir, não há música, não há necessidade de um sentimento de sucesso.
- AF3 / Qwen-Audio-família se: música, emoção, multi-falantes ou raciocínio de áudio complexo.
  No entanto, o que não é um problema é que o que você está fazendo é muito difícil.

Cascada é mais barata e simples.

> 级联更便宜更简单――端到端更强大――

### MMAU  o critério de referência de raciocínio de áudio

MMAU (Massive Multimodal Audio Understanding) é o padrão de referência de raciocínio de áudio 2024-2025.

> MMAU (大规模多模态音频理解) é um programa de audiência de 2024-2025

- 10.000 pares de QA de texto de áudio através da fala, música, sons ambientais.
  Tradução do inglês: 个跨语音、音乐、环境声的音频-文本 QA 对──
- Abrange classificação, raciocínio temporal, raciocínio causal, QA aberto.
  Tradução do inglês para inglês: 覆盖分类、时间推理、因果推理、开放式 QA。
- Teste o que os oleodutos em cascata sistematicamente perdem.
  Tradução do inglês para "Testamentation"

O SOTA aberto (AF3) em 0,72; fronteira proprietária ~ 0,78 (Gemini 2.5 Pro, Claude Opus 4.7).

> 开源 SOTA(AF3) 0.72;闭源前沿约0.78(Gemini 2.5 Pro、Claude Opus 4.7)。差距小于VideoMME 的开源-闭源差距,说明音频 LLM 正在成熟──

## Use-o com o framework implementado.
```figure
audio-text-ctc
```

## Usá-lo

`code/main.py`- Não .

- Implementa o cálculo de espectrograma log-Mel em stdlib: windowswing, naívo DFT, Mel filter-bank.
  中文翻译:用标准库实现 log-Mel 频谱图计算:窗口化、朴素 DFT、Mel 波器组。
- O esqueleto de áudio Q-ex: dados quadros de saída do codificador, computa Q, K, V, atenção e emite tokens N.
  Chinese: 音频 Q-former 骨架:给定编码器输出,计算 Q、K、V、注意力并输出 N 个代币──
- Comparar cascada contra extremo a extremo numa tarefa de brinquedo.
  Tradução do inglês em japonês:                                                                                                                                                                                                                                                           

## Envia-o . Produto .

Esta lição produz`outputs/skill-audio-llm-pipeline-picker.md`. Dada uma tarefa de áudio (transcrição, etiquetado musical, inferência de emoção, diarização de alto-falantes, classificação do ambiente), ele escolhe a AF3 em cascata, de ponta a ponta ou um híbrido.

> 本课产 出 `outputs/skill-audio-llm-pipeline-picker.md`◊ dado um determinado volume de trabalho ([[transcord]] ]] , [[marca musical]] ]] , ]] , ]] , ]] , ]] , ]] , ]] , ]] , ]] , ]] , ]] , ]] , ]] , ]] , ]] , ]] , ]] , ]] , ]] , ]] , ]] , ]] , ]] , ]] , ]] , ]] , ]] , ]] , ]] , ]] , ]] , ]] , ]] , ]] , ]] , ]] , ]] , ]] , ]] , ]] , ]] , ]] , ]] , ]] , ]] , ]] , ]] , ]] , ]] , ]] , ]] , ]] , ]] , ]] , ]] , ]] , ]] , ]] , ]] , ]] , ]] , ]] , ]] , ]] , ]] , ]] , ]] , ]] , ]] ,

## Exercícios.

1. Calcule a dimensão do espectrograma log-Mel para um clip de 30 segundos em 16kHz, janela de 25ms, salto de 10ms, 80 binos de Mel. Como muda isso em 48kHz? 计算 30 秒音频在 16kHz、25ms 窗口、10ms 步长、80 Mel 频段下 log-Mel 频谱图维度、48kHz 时如何变化?

2. Por que o Whisper tem um desempenho inferior na música? Que recursos de áudio os BEATs capturam que o Whisper não? Por que o Whisper não apresenta bem na música?

3. Audio Q-former com 64 consultas vs 32: em que complicação de tarefa 64 paga? 32 salvar computação para quê? 64  consulta vs 32  consulta de Audio Q-former: em que tarefa complexidade?

4. Leia a secção 4 do AF3 sobre pensamento sob demanda. Propõe três tarefas de áudio em que a cadeia de pensamento ajuda mais.

5. Implementar um pipeline de diarização mínima usando a saída do AF3. Como você sinaliza mudanças de alto-falantes?

## Termos-chave .

| Term | What people say | What it actually means | 中文释义 |
|------|-----------------|------------------------|---------|
| Log-Mel spectrogram | "Mel features" Mel 频谱 | 2D (time, frequency) array of log-magnitude values after Mel filter banks 经 Mel 滤波器组后的对数幅度二维数组 | |
| Audio Q-former | "Audio Perceiver" 音频感知器 | Cross-attention bottleneck from audio encoder output to fixed-length queries feeding the LLM 音频编码器输出到固定长度查询的交叉注意力瓶颈 | |
| Cascaded | "ASR-then-LLM" 级联管道 | Pipeline where Whisper transcribes and a text LLM reasons; loses acoustic information Whisper 转录后文本 LLM 推理的管道；丢失声学信息 | |
| End-to-end | "Audio-LLM" 端到端音频 LLM | Audio features enter the LLM directly via Q-former; preserves acoustic signal 音频特征通过 Q-former 直接进入 LLM；保留声学信号 | |
| BEATs | "Audio AudioSet encoder" 音频自监督编码器 | SSL transformer trained on AudioSet; strong on music + environmental sounds 在 AudioSet 上训练的自监督 Transformer；擅长音乐和环境声 | |
| MMAU | "Audio reasoning bench" 音频推理基准 | 10k QA pairs across speech, music, environment; 2024 eval standard 跨语音、音乐、环境的 1 万条 QA；2024 年评估标准 | |
| On-demand thinking | "Audio CoT" 按需音频思考 | Model can optionally emit reasoning tokens before final answer, lifts accuracy 3-5 pts 模型可在最终回答前输出推理 token，提升准确率 3-5 个百分点 | |

## Mais leitura 延伸阅读

- [Radford et al. — Whisper (arXiv:2212.04356)](https://arxiv.org/abs/2212.04356)
- [Chu et al. — Qwen-Audio (arXiv:2311.07919)](https://arxiv.org/abs/2311.07919)
- [Goel et al. — Audio Flamingo 3 (arXiv:2507.08128)](https://arxiv.org/abs/2507.08128)
- [Tang et al. — SALMONN (arXiv:2310.13289)](https://arxiv.org/abs/2310.13289)
- [Gong et al. — LTU (arXiv:2305.10790)](https://arxiv.org/abs/2305.10790)
