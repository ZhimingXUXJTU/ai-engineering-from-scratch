# MIO e qualquer-para-qualquer streaming Multimodal Modelos MIO: arbitrário a arbitrário fluxo multimodelo modelo

> O GPT-4o envia um produto que a maioria dos modelos abertos não pode replicar: um agente que ouve voz, vê vídeo e fala em tempo real. A resposta do ecossistema aberto até o final de 2024 foi MIO (Wang et al., setembro 2024). MIO tokeniza texto, imagem, fala e música, treina um transformador causal sobre as sequências entrelaçadas e gera qualquer modalidade para qualquer modalidade. AnyGPT (Zhan et al., fevereiro 2024) foi a prova do conceito; MIO é a escalada; Unified-IO 2 (Allen AI, dezembro 2023) é o primo com a visão + ação de terra. Esta lição lê o padrão de qualquer um para qualquer um  quatro tokenizers, um transformador, decodificação amigável para streaming.

> **【中文解读】**GPT-4o  mostrou uma forma de produto impressionante: um agente capaz de ouvir, ver, fazer a voz de volta e volta. A comunidade de fontes abertas até o final de 2024 só teve o MIO neste programa disponível.

**Type:** Learn | **类型:** 学习
**Languages:** Python (stdlib, four-modality token allocator + streaming decode loop) | **语言:** Python（标准库，四模态 token 分配器 + 流式解码循环）
**Prerequisites:** Phase 12 · 11 (Chameleon), Phase 6 (Speech and Audio) | **前置知识:** Phase 12 · 11（Chameleon），Phase 6（语音与音频）
**Time:** ~120 minutes | **时间:** ~120 分钟

> - Não .**【前置】**O que é que você tem a ver com o seu nome? Você pode ver o nome do nome do nome do nome do nome do nome do nome do nome do nome do nome do nome do nome do nome do nome do nome do nome do nome do nome do nome do nome do nome do nome do nome do nome do nome do nome do nome do nome do nome do nome do nome do nome do nome do nome do nome do nome do nome do nome do nome do nome do nome do nome do nome do nome do nome do nome do nome do nome do nome do nome do nome do nome do nome do nome do nome do nome do nome do nome do nome do nome do nome do nome do nome do nome do nome do nome do nome do nome do nome do nome do nome do nome do nome do nome do nome do nome do nome do nome do nome do nome do nome do nome do nome do nome do nome do nome do nome do nome do nome do nome do nome do nome do nome do nome do nome do nome do nome do nome do nome do nome do nome do nome do nome do nome do nome do nome do nome do nome do nome do nome do nome do nome do nome do nome do nome do nome do nome do nome do nome do nome do nome do nome do nome do nome do nome do nome do nome do nome do nome do nome do nome do nome do nome do nome do nome do nome do nome do nome do nome do nome do nome do nome do nome do nome do nome do nome do nome do nome do nome do nome do nome do nome do nome do nome do nome do nome do nome do nome do nome do nome do nome do nome do nome do nome do nome do nome do nome do nome do nome do nome do nome do nome do nome do nome do nome do nome do nome do nome do nome do nome do nome do nome do nome do nome do nome do nome do nome do nome do nome do nome do nome do nome do nome do nome do nome do nome do nome do nome do nome do nome do nome do nome do nome do nome do nome do nome do nome do nome do nome do nome do nome do nome do nome do nome do nome do nome do nome do nome do nome do nome do nome do nome do nome do nome do nome do nome do nome do nome do nome do nome do nome do nome do nome do nome do nome do nome do nome do nome do nome do nome do nome do nome do nome do nome do nome do nome do nome
> - Não .**【类比】**MIO = "万能翻译耳机"──其他多模态系统 = 一堆翻译器接力(视觉翻译→文本→语音翻译→音频), cada salto atrasado+ perda de informação; MIO = um cérebro ao mesmo tempo ouvir、看、说, assim como GPT-4o 那样端到端低延迟── desafio é que cada tipo de modo seja tokenizer, e os tokens não podem entrar em conflito entre si──

## Objetivos de aprendizagem

- Desenhe um vocabulário compartilhado que hospede textos, imagens, fala e tokens de música sem colisões.
  Tradução do inglês para o inglês: Design a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a
- Compare SEED-Tokenizer (imagem) e SpeechTokenizer residual-VQ (discurso) em compressão + reconstrução trade-offs.
  中文翻译:比较 SEED-Tokenizer (图像) 和 SpeechTokenizer 残差 VQ (语音) 在压缩+重建方面的权衡──
- Explique o currículo de quatro etapas que constrói qualquer geração para qualquer geração.
  Tradução do inglês para tradução do inglês:
- Cite as três receitas abertas a qualquer pessoa e as suas principais compensações: MIO, AnyGPT, Unified-IO 2.
  O que é o problema do sistema de controle de dados?

## O problema é o problema da introdução

Um modelo multimodal unificado é fácil de reivindicar e difícil de construir em escala. A maioria dos sistemas "de qualquer a qualquer" até 2024 foram pipelineados: modelo de visão → representação de texto → modelo de fala → áudio. Cada espera perde informações, adiciona latência e complica o treinamento. O vídeo demo do GPT-4o mostrou uma alternativa de modelo único com resposta subsequente; sistemas abertos seguidos por meses.

> 统一多模态模型易声称但难以大规模构建──2024 anos antes, a maioria dos sistemas "voluntários a arbitrários" são tubulares: modelos de visão→文本表示→语音模型→音频──每跳都会丢失信息、增加延迟、复杂化训练──GPT-4o apresentação vídeo mostra um único modelo alternativo, tempo de resposta em segundo grau abaixo; sistema aberto ficou atrasado por alguns meses──

> **【中文解读】**O maior desafio do sistema de múltiplos modelos é: não pode reutilizar os canais de comunicação (vidência, texto, texto, palavras, palavras, etc.), pois cada fase é perdida e aumenta o atraso.

Os desafios de engenharia:

> 工程挑战:

- Os tokenizers devem existir para todas as modalidades, comprimir sem perdas - o suficiente para reconstrução, e produzir tokens às taxas que o transformador pode consumir.
  Tradução do inglês para o inglês: Every kind of mode is required to have a分词器, comprimir losses small enough in order to rebuild, e produzir tokens com a taxa de consumo do transformador.
- Um único vocabulário deve atribuir espaço para texto (32k+), imagem (16k+), fala (4k+), música (8k+).
  No entanto, o que não é necessário para o seu uso é que o seu uso seja feito com a sua própria capacidade de uso.
- Os dados de formação devem abranger cada par de entrada e saída (texto→imagem, imagem→discurso, fala→imagem, etc.) ou o modelo deve ser composto.
  Tradução em inglês: training data must cover every input-output for (((文本→图像、图像→语音、语音→图像等), ou modelo must be able to assemble。
- A inferência deve transmitir tokens de saída rápido o suficiente para a latência de conversação (<500ms tempo-a-primeiro-byte de áudio).
  Tradução do inglês para o inglês:                                                                                                                                                                                                                                                          

## O conceito central.

> **【中文解读】**MIO                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            

> **【拓展：全模态模型的趋势】**A tendência de 2025 é de "visão+linguagem" para "todo modo": GPT-4o Origins Support语音输入输出,Gemini 支持视频实时流,Meta's Spirit LM 统一语音和文本。


### Quatro tokenizers para quatro modalidades

A pilha de tokenizer da MIO:

> **【中文解读】**MIO para quatro modelos, em conjunto com um tokenizer especial, o token de saída são mapeados para o código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de

- Texto: BPE padrão, vocabulário ~32000.
  O seu nome é "BPE Standard", o que significa "BPE Standard".
- Imagem: SEED-Tokenizer (2023)  VAE quantizado com livro de código discreto, 4096 entradas, 32x32 tokens por imagem.
  Tradução do português: 图像:SEED-Tokenizer(2023) 带离散码本的量化 VAE,4096 条目,每张图 32x32 个代币──
- Discurso: SpeechTokenizer residual-VQ (2023)  codifica a forma de onda de 16 kHz em 8 codebooks hierárquicos; o primeiro nível é conteúdo grosseiro, níveis posteriores adicionam prosodia e identidade do alto-falante.
  Chinese Language Translation:语音:SpeechTokenizer 残差 VQ(2023) 将16kHz 波形编码为8层级码本;第一层是粗粒度内容,后续层添加律和说话人身份──
- Música: resíduos similares-VQ (família MusicGen / Encodec da Meta), 4-8 codebooks.
  No entanto, o que não é verdade é que o que não é verdade é que o que é verdade é que o que é verdade é que o que é verdade é que é verdade.

Cada modalidade produz tokens inteiros. Os tokens recebem intervalos de ID desarticulados no vocabulário compartilhado:

> Cada modo produz um número total de tokens. Tokens obtidos não sobrepostos em um conjunto de palavras:

```
text:   0..31999
image:  32000..36095  (4096 image tokens)
speech: 36096..40191  (4096 speech base tokens, plus residual layers)
music:  40192..48383  (8192 music tokens)
sep:    48384..48390  (<image>, <speech>, <music>, </...>, etc.)
```

Total: ~ 48k vocabulário. A inserção de entrada e projeção de saída abrangem todo.

> 总计约 48k 词汇量──输入嵌入和输出投影覆盖全部词汇──

### Descódigo de streaming

A geração de fala usa o restante-VQ. O transformador prevê os tokens de fala base (camada 0); um quantificador residual decodificado paralelo prevê as camadas subsequentes. Cada token de camada 0 é de aproximadamente 50 ms de áudio em 16 kHz.

> 语音生成使用残差 VQ──Transformer 预测基础层(第0层)语音代币;并行解码的残差量化器预测后续层──每个第0层代币 大约对应 16kHz 下的50ms 音频──

> **【中文解读】**O processo de resolução de código é executado por um processador de dados, que é um processador de dados, que é um processador de dados, que é um processador de dados, que é um processador de dados, que é um processador de dados, que é um processador de dados, que é um processador de dados, que é um processador de dados, que é um processador de dados, que é um processador de dados, que é um processador de dados, que é um processador de dados, que é um processador de dados, que é um processador de dados, que é um processador de dados, que é um processador de dados, que é um processador de dados, que é um processador de dados, que é um processador de dados, que é um processador de dados, que é um processador de dados, que é um processador de dados, que é um processador de dados, que é um processador de dados, que é um processador de dados, que é um processador de dados, que é um processador de dados, que é um processador de dados, que é um processador de dados, que é um processador de dados, que é um processador de dados, que é um processador de dados, que é um processador de dados, que é um processador de dados, que é um processador de dados, que é um processador de dados, que é um processador de dados, que é um processador de dados, que é um processador de dados, um processador de dados, que é um processador de dados, um processador de dados, um processador de dados, um processador de dados, que é um processador de dados, um processador de dados, um processador de dados, um processador de dados, um processador de dados, um processador de dados, um processador de dados, um processador de dados, um processador de dados, um processador de dados, um processador de dados, um processador de dados, um processador de dados, um processador de dados, um processador de dados, um processador de dados, um processador de dados, um processador de um servidor de um servidor de um servidor de um servidor de um servidor de um servidor de um servidor de um servidor de um servidor, por um servidor,

O padrão de streaming:

> 流式模式:

1. O usuário fala em microfone; o tokenizer de áudio em tempo real emite tokens de fala a cada 50 ms.
   Chinese: user对着麦克风说话;实时音频分词器每50ms 输出语音代币──
2. MIO consome tokens à sua chegada (preenchimento imediato + avanço incremental).
   Chinese:MIO 在 token 到达时即时消费 (MIO 在代币到达时即时消费)
3. Os tokens de saída fluem como gerados; um decodificador de voz paralelo os converte em amostras de áudio com ~ 50-150ms de latência.
   Tradução do idioma em inglês: 中文翻译:输出代币 在生成时流式输出;并行语音解码器以约50-150ms 延迟将其转换为音频样本──
4. Tempo de primeira audiobitação: ~300-500ms no papel MIO, aproximando-se dos ~250ms do GPT-4o.
   Tradução do inglês para inglês: MIO 论文约300-500ms,接近GPT-4o 的约250ms──

Mini-Omni (arXiv:2408.16725), GLM-4-Voice (arXiv:2412.02612), e Moshi (arXiv:2410.00037) são projetos complementares de streaming de fala-LLM. Moshi, em particular, alcança 160ms viagem de ida e volta em uma única GPU.

> Mini-Omni、GLM-4-Voice 和 Moshi é um complemento de fluência de voz LLM design。Moshi em um único GPU alcançou 160ms 往返延迟。

### Currículo de quatro etapas

Currículo de formação do MIO:

> Programa de treinamento do MIO:

1. Estação 1  alinhamento. Corporação de pares de modalidade em grande escala: imagem-texto, fala-texto, música-texto. Cada par usa seu próprio segmento de vocabulário token. Treina o vocabulário compartilhado.
   O texto original é escrito em uma linguagem de língua inglesa, que é traduzida em grego como "Letração de uma língua inglesa".
2. Estação 2  interligados. Documentos interligados de várias modalidades (blogs com imagens + vídeo, podcasts com transcrições, etc.).
   O que é que você está fazendo?
3. Fase 3  Voz melhorada. Dados de áudio extras para elevar a qualidade da voz sem perder a capacidade de texto.
   Chinese: 阶段 3  语音增强──额外音频数据提升语音质量,不损失文本能力──
4. Fase 4  FSS. Aligação de instruções entre modalidades: VQA, subtítulos, narração, diálogo fala-a-fala.
   中文翻译:阶段 4  指令微调(SFT) ――跨模态指令调优:VQA、描述、旁白、语音对话。

O facto de não ter um estágio degrada as capacidades específicas: saltar a fase 2 e o modelo perder o contexto de modalidade cruzada; saltar a fase 3 e a fala ser pobre.

> 跳过某一阶段会导致特定能力退化:跳过阶段 2 模型失去跨模态上下文;跳过阶段 3 语音质量差──

> **【中文解读】**O curso de treinamento em quatro fases do MIO é de capacidade de construção gradual: 1) modelo para a produção de gráficos em grande escala, texto-idioma para o diálogo, treinamento em partilha de palavras; 2) treinamento em vários tipos de linguagem; 3) treinamento em linguagem para aumentar o volume de dados; 4) instrução para a redução de VQA em formato transversal, descrever o diálogo, etc.

### Cadeia de pensamento visual

MIO introduz a cadeia de pensamento visual: o modelo emite tokens de imagem intermediários como um passo de raciocínio.

> MIO introduziu a cadeia de pensamento visual: modelo em processo de raciocínio gerar símbolos de imagem intermediária.

1. Emissões `<image>`Tokens que retransmitem a cena (a partir da imagem de entrada ou de um esboço).
   Tradução: 输出`<image>`token 染场景 (染场景)
2. Emite texto analisando o esboço.
   Tradução do português: 输出文本分析草图.
3. Emite a resposta final.
   Tradução do português:输出最终答案.

A imagem intermediária é uma ferramenta de rascunho, e as referências melhoram as tarefas de raciocínio espacial.

> O quadro intermediário do roteiro é um quadro de um projecto.

> **【拓展：视觉思维链的应用前景】**A cadeia de pensamento visual é a expansão do campo da visão. Em cenários financeiros, esta técnica pode ser usada para analisar gráficos complexos:

### Competidores em qualquer

- AnyGPT (arXiv:2402.12226): 4 modalidades (texto, imagem, fala, música), design semelhante.
  Tradução do inglês para o português: AnyGPT:4 种模态(文本、图像、语音、音乐), similar design。
- Unified-IO 2 (arXiv:2312.17172): adiciona resultados de ação de visão, profundidade, normais. Mais diversidade de tarefas, menor escala.
  Tradução do inglês:Unified-IO 2: Add加视觉动作输出、深度、法线──任务更多样,规模更小──
- NExT-GPT (arXiv:2309.05519): LLM + decodificadores de difusão específicos de modalidade. Não é uma abordagem de modelo único.
  Tradução do português:NExT-GPT:LLM + 模态特定扩散解码器──非单模型方案──
- CoDi (arXiv:2305.11846): difusão compostavel; qualquer-a-qualquer via latente compartilhado.
  Tradução do inglês:CoDi:可组合扩散; através do espaço secreto de compartilhamento, realizar qualquer coisa até qualquer coisa.

O MIO é o mais próximo de qualquer token puro a qualquer.

> MIO é o símbolo mais próximo de qualquer um dos quais.

### Orçamento de latência

Para um produto de conversação, a latência de cada componente importa:

> Para os produtos de diálogo, é importante que cada componente seja atrasado:

- Microphone para tokens de áudio: ~ 50ms.
  O que é o "tôquio de rádio" de MacKenzie?
- Preencher (tokens de áudio + histórico): ~ 100ms em um modelo 8B.
  中文翻译:预填充(音频代币 + 历史):8B 模型约100ms。
- Primeiro token de saída: ~ 50ms.
  Chinese:首个输出代币:约50ms──
- Descóder de voz paralelo residual-VQ +: ~ 100-150ms.
  中文翻译:并行残差 VQ + 语音解码器: cerca de 100-150ms。

Tempo total de primeira audiobita: ~ 300ms mínimo. GPT-4o afirma ~ 250ms. Moshi afirma 160ms. MIO / AnyGPT estão na faixa de 400-600ms por referência pública.

> 首音频字节时间总计至少约300ms──GPT-4o 声称约250ms──Moshi 声称160ms──MIO/AnyGPT 在公开基准测试中约400-600ms──

> **【中文解读】**O orçamento de atraso do produto:麦克风→语音代币(~50ms)→ 预填充(~100ms)→ 首个输出代币(~50ms)→ 残差 VQ + 语音解码(~100-150ms)。

### Porque é que qualquer um fica duro

Mesmo em 2026, os modelos abertos de qualquer tipo seguem os fechados em dois eixos:

> Mesmo em 2026, o modelo livre de arbitrariedade em duas dimensões ainda está atrasado no modelo fechado:

- Qualidade da fala. O tokenizador residual-VQ é perdedor; fala conversacional soa robótica em comparação com vozes da classe ElevenLabs.
  Tradução do inglês: 中文翻译:语音质量──残差 VQ 分词器是有损的; em comparação com elevenLabs 级别的语音相比,对话语音听起来机械──
- O modelo de "cantando sobre o que vê" ainda falha mais frequentemente do que as tarefas de visão pura.
  O modelo "cantando o que você vê" ainda é mais frequentemente falhado do que o trabalho de simples visão.

Estes são problemas de pesquisa aberta. Qwen3-Omni (Lessão 12.20) é a tentativa aberta mais avançada em 2025.

> Estas são questões de investigação aberta.

## Use-o com o framework implementado.
```figure
any-to-any-stream
```

## Usá-lo

`code/main.py`- Não .

> `code/main.py`- Não .

- Define a alocação de vocabulário de quatro modalidades e imprime-a.
  Tradução do inglês: definição de quatro formas de expressão
- Roteia uma lista de entradas multimodal (texto, imagem, áudio-clip, música) através do roteador do tokenizer.
  Tradução do inglês: 文本、图像、音频片段、音乐)
- Simula o decodificação de streaming para uma resposta de texto a fala com contagem de latência.
  O que é que se passa com o seu trabalho?
- Calcula o tempo esperado de primeiro byte de áudio dado por latências de codificação, preenchimento e decodificação.
  Tradução do inglês: According编码器、预填充和解码器延迟计算预期的首音频字节时间──

## Envia-o . Produto .

Esta lição produz`outputs/skill-any-to-any-pipeline-auditor.md`- Tendo em conta a especificação do produto conversativo (modalidades de entrada, modalidades de saída, meta de latência), verifica as escolhas de design da família MIO e calcula o orçamento de latência.

> 本课产 出 `outputs/skill-any-to-any-pipeline-auditor.md`◊ fornecer o modelo de diálogo, o modelo de entrada, o modelo de saída, o objetivo de atraso), auditando a seleção de projetos da série MIO e calcula o orçamento de atraso.

## Exercícios.

1. Seu produto aceita entrada de voz e retorna saída de voz. Qual é o objetivo de orçamento de latência de ponta a ponta? Lista os componentes que gastam tempo.

2. O SpeechTokenizer residual-VQ usa 8 codesbooks. Propõe por que a decodificação paralela dos níveis residuais é necessária (versus sequencial) e quais economias de latência traz.

3. Seu vocabulário tem 32k texto + 4k imagem + 4k fala. Adicione 8k música e ~10 separadores. Qual é o custo do parâmetro de matrizes de incorporação em dim 4096 oculto?

4. A cadeia de pensamento visual emite uma imagem intermediária. Que tipos de perguntas beneficiam? Que tipos são prejudicados pelos tokens extras?

5. Leia Moshi (arXiv:2410.00037). Descreva sua técnica de "monólogo interno" e compare com a cadeia de pensamento visual do MIO.

## Termos-chave .

| Term | What people say | What it actually means | 中文释义 |
|------|-----------------|------------------------|---------|
| Any-to-any | "Multimodal in/out" 任意模态进出 | A single model that accepts and emits text, image, speech, and music in any direction 单一模型接受并以任意方向输出文本、图像、语音、音乐 | |
| Residual-VQ | "Speech tokenizer stack" 语音分词器栈 | Multi-codebook tokenization where each layer adds information; base layer is content, later layers are prosody 多码本分词，每层添加信息；基础层是内容，后续层是韵律 | |
| SEED-Tokenizer | "Image codes" 图像编码 | Discrete image tokenizer with 4096-entry codebook used by MIO 离散图像分词器，4096 码本 | |
| Chain-of-visual-thought | "Visual scratchpad" 视觉草稿板 | The model generates an intermediate image as a reasoning step before its final answer 模型在最终回答前生成中间图像作为推理步骤 | |
| Time-to-first-audio-byte | "TTFAB" 首音频字节延迟 | Latency from user voice to first audio output; <500ms for conversational feel 用户语音到首个音频输出的延迟；<500ms 才有对话感 | |
| Four-stage curriculum | "Training recipe" 训练配方 | Alignment -> interleaved -> speech-enhanced -> SFT, in that order 对齐→交错→语音增强→指令微调的四阶段训练流程 | |

## Mais leitura 延伸阅读

- [Wang et al. — MIO (arXiv:2409.17692)](https://arxiv.org/abs/2409.17692)
- [Zhan et al. — AnyGPT (arXiv:2402.12226)](https://arxiv.org/abs/2402.12226)
- [Lu et al. — Unified-IO 2 (arXiv:2312.17172)](https://arxiv.org/abs/2312.17172)
- [Wu et al. — NExT-GPT (arXiv:2309.05519)](https://arxiv.org/abs/2309.05519)
- [Tang et al. — CoDi (arXiv:2305.11846)](https://arxiv.org/abs/2305.11846)
