# Flamingo e Gated Cross-Attention para VLMs de poucos tiros

> O Flamingo de DeepMind (2022) fez duas coisas antes de qualquer outra pessoa. Mostrou que um único modelo poderia processar sequências arbitrariamente entrelaçadas de imagens, vídeos e texto. E mostrou que os VLMs podiam aprender no contexto  dar um prompt de alguns tiros com três pares de exemplos (imagem, legenda) e o modelo substitui uma nova imagem sem qualquer passo de gradiente. O mecanismo: camadas de atenção cruzada fechadas, inseridas entre as camadas existentes do LLM congelado, com um portal tanh aprendido que começa a zero para que a capacidade de texto do LLM seja preservada na inicialização. Esta lição percorre o re-sampler Perceptor do Flamingo e a arquitetura de atenção cruzada fechada, o ancestral das entradas entrelaçadas do Gemini e dos tokens visuais do Idefics2.

> **【中文解读】**Flamingo  primeira implementação de gráficos                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                     

> **【拓展：Flamingo→Gemini交织输入】**O modelo de processamento de gráficos de Flamingo é o modelo original de tokens visuais de Gemini 交织输入和 Idefics2, iniciando o processo de aprendizagem literária em vários modos.

**Type:** Learn | **类型:** 学习
**Languages:** Python (stdlib, gated cross-attention + Perceiver resampler demo) | **语言:** Python（标准库，门控交叉注意力 + Perceiver resampler 演示）
**Prerequisites:** Phase 12 · 03 (BLIP-2 Q-Former) | **前置知识:** Phase 12 · 03（BLIP-2 Q-Former）
**Time:** ~120 minutes | **时间:** ~120 分钟

> - Não .**【前置】**O primeiro é o primeiro: "Blocker" (Blocker) (Blocker) (Blocker) (Blocker) (Blocker) (Blocker) (Blocker) (Blocker) (Blocker) (Blocker) (Blocker) (Blocker) (Blocker) (Blocker) (Blocker) (Blocker) (Blocker) (Blocker) (Blocker) (Blocker) (Blocker) (Blocker) (Blocker) (Blocker) (Blocker) (Blocker) (Blocker) (Blocker) (Blocker) (Blocker) (Blocker) (Blocker) (Blocker) (Blocker) (Blocker) (Blocker) (Blocker) (Blocker) (Blocker) (Blocker) (Blocker) (Blocker) (Blocker) (Blocker) (Blocker) (Blocker) (Blocker) (Blocker) (Blocker) (Blocker) (Blocker) (Blocker) (Blocker) (Blocker) (Blocker) (Blocker) (Blocker) (Blocker) (Blocker) (Blocker) (Blocker) (Blocker) (Blocker) (Blocker) (Blocker) (Blocker) (Blocker) (Blocker) (Blocker) (Blocker) (Blocker) (Blocker) (Blocker) (Blocker) (Blocker) (Blocker) (Blocker) (Blocker) (B) (Blocker) (B) (Blocker) (Blocker) (B) (Blocker) (Blocker) (B) (B) (B) (BlockerB) (Blocker) (B) (B) (B) (B) (B) (B) (B) (B) (B) (B) (B) (B) (B) (B) (B) (B) (B) (B) (
> - Não .**【类比】**Flamingo's Gate Control Intersectional Attention = "Migrar transformação de engenharia externa"―BLIP-2 = "en LLM 大门口装一个翻译员"―输入端桥接一次);Flamingo = "en LLM's every level office inside a window"― (em cada 4 níveis de uma porta control intersectional Attention)―门控初始为 0 = 窗一开始是关闭的,模型行为和原 LLM 完全一样;训练慢慢开窗 = 视觉信息逐渐注入但不破坏原文能力──

## Objetivos de aprendizagem

- Explique como a atenção cruzada por gate preserva a capacidade de texto do LLM congelado na inicialização via tanh(gate) = 0.
  Tradução do inglês para tradução do inglês:
- Passe por um resampler Perceptor: N patches de imagem → K fixa "latentes" consultas através da atenção cruzada.
  Por meio de um sistema de observação, o sistema de observação pode ser usado para fazer uma observação de dados.
- Descreva como Flamingo lida com sequências de imagem-texto entrelaçadas com mascaramento causal que respeita a colocação da imagem.
  Tradução do idioma francês: descrever Flamingo  como usar o respeito por um quadro de um quadro de um quadro de um quadro de um quadro de um quadro de um quadro de um quadro de um quadro de um quadro de um quadro de um quadro de um quadro de um quadro de um quadro de um quadro de um quadro de um quadro de um quadro de um quadro de um quadro de um quadro de um quadro de um quadro de um quadro de um quadro de um quadro de um quadro de um quadro de um quadro de um quadro de um quadro de um quadro de um quadro de um quadro de um quadro de um quadro de um quadro de um quadro de um quadro de um quadro de um quadro de um quadro de um quadro de um quadro de um quadro de um quadro de um quadro de um quadro de um quadro de um quadro de um quadro de um quadro de um quadro de um quadro de um quadro de um quadro de um quadro de um quadro de um quadro de um quadro de um quadro de um quadro de um quadro de um quadro de um quadro.
- Reproduzir uma estrutura de prompt multimodal de algumas fotos (3 exemplos de captura de imagem e depois uma imagem de consulta).
  Tradução do inglês: 复现少样本多模态提示结构 (多模态提示结构)

## O problema é o problema da introdução

BLIP-2 alimenta 32 tokens visuais na camada de entrada de um LLM congelado. Funciona para uma imagem por pedido. Mas e se quiserem alimentar *muitas* imagens entrelaçadas com texto, como em "aqui está a imagem A, subtítulo; aqui está a imagem B, subtítulo; agora aqui está a imagem C, subtítulo"? A auto-atenção do LLM precisaria lidar com tokens de imagem e tokens de texto em um único fluxo, e a questão de quais posições podem atender a quais imagens se torna agitada.

> BLIP-2 vai colocar 32 tokens visuais 结 LLM 入层――适用于每个提示一张图像――但如果你想入与文本交织的*多张*图像呢,例如"É uma imagem A, descreve-a; é uma imagem B, descreve-a; é uma imagem C, descreve-a"; LLM precisa de auto-atenção para processar em um único fluxo de tokens de imagem 和文本 token, quais posições podem se concentrar em quais questões de imagem tornam-se complicadas.

A resposta do Flamingo: não alterem o fluxo de entrada do LLM. Insira camadas de atenção cruzada extra entre os blocos de LLM existentes. Os tokens de texto ainda fluem através da auto-atenção causal do LLM como sempre. Entre cada poucos blocos de LLM, tokens de texto também atendam às características da imagem através de uma nova camada fechada. O portal (iniciado para zero) significa que no passo zero as novas camadas são sem operações  o modelo se comporta exatamente como o LLM pré-treinado. À medida que o treinamento progride, o portão abre-se e a informação visual começa a fluir.

> Resposta de Flamingo: totalmente não alterar o fluxo de entrada do LLM. Em blocos existentes, o LLM é um token de texto que se insere em um nível de atenção adicional. Como sempre, o LLM é um elemento de atenção.

A segunda pergunta Flamingo respondeu: como você lida com um número variável de imagens (0, 1 ou muitas) por prompt? Um resampler Perceptor  um pequeno módulo de atenção cruzada que toma qualquer número de patches que você tem e produz um número fixo de tokens visuais latentes. A camada de atenção cruzada LLM vê a mesma forma independentemente de quantas imagens estão no prompt.

> Flamingo 回答的第二个问题:如何处理每个提示中可变数量的图像 ((0、1或多张)?Perceptor resampler é um pequeno módulo de atenção de交叉, recebe um número arbitrário de patches并产生固定数量的视觉潜在 token── não importa qual seja a quantidade de imagens em cada提示,LLM 交叉注意力层看到的形状都相同──

## O conceito central.

> **【中文解读】**Flamingo(Mente Profunda) Introdução de controle de entrada e entrada de informações, introdução de valor de controle de entrada e entrada de informações, introdução de tempo de 0 (((informação visual não entra), introdução de informações entre os níveis de LLM e os níveis de controle de entrada e entrada de informações, introdução de informações, introdução de informações, introdução de informações, introdução de informações, introdução de informações, introdução de informações, introdução de informações, introdução de informações, introdução de informações, introdução de informações, introdução de informações, introdução de informações, introdução de informações, introdução de informações, introdução de informações, introdução de informações, introdução de informações, introdução de informações, introdução de informações, introdução de informações, introdução de informações, introdução de informações, introdução de informações, introdução de informações, introdução de informações, introdução de informações, introdução de informações, introdução de informações, introdução de informações, introdução de informações, introdução de informações, introdução de informações, introdução de informações, introdução de informações, introdução de informações, introdução de informações, ou de informações, ou de informações, ou de outras informações, ou de outras informações, ou de outras informações, ou de outras, ou de outras, ou de, ou de, ou de, ou de, ou de, ou de, ou de, ou de, ou de, ou de, ou de, ou de, ou de, ou de, ou de, ou de, ou de, ou de, ou de, ou de, ou de, ou de, ou de, ou de, ou de, ou de, ou de, de, ou de, de, ou de, ou de, ou de, ou de, de, ou de, ou de, ou de, ou de, ou de, de, de, ou de, ou de, ou de, ou de, ou de, ou de, ou de, ou de, ou de, ou de, de, ou de, ou de, ou de, ou de, ou de, de, ou de, ou de, ou de, ou de, ou de, ou de, ou de, de, ou de, ou de, ou de, ou de, ou de, ou de, ou de, ou de, ou de, ou de, ou de, ou de

> **【拓展：Flamingo 的高效适配】**Flamingo  apenas treinamento de cerca de 1%  门控交叉注意力层), já pode alcançar SOTA em poucos tiros 视觉推理任务                                                                                                                                                                                                                                            


> **【拓展：门控机制的数学原理】**O valor de inicialização do controle de entrada do controle de atenção é 0, o que significa que a informação visual não entra completamente no LLM quando o treinamento começa. Com o treinamento, o controle de entrada é gradualmente aberto. Isso impede que o treinamento inicie o ruído visual interferindo com a capacidade de linguagem do LLM.


### O LLM congelado

Flamingo começa com um LLM congelado Chinchilla 70B. Todos os pesos 70B intactos.

> Flamingo 以结的Chinchilla 70B LLM 为起点──所有700亿权重不触碰──现有文本自注意力和FFN 正常运行──

### Re-estampilador de percepção

Para cada imagem no prompt, o ViT produz N patch tokens. O resampler Perceptor tem K latentes fixas aprendíveis (Flamingo usa K=64).

> 对于提示中的每张图像,ViT 产生 N 个补丁代币──Perceptor resampler 有 K 个固定的可学习潜在向量(Flamingo 使用 K=64)──每个 resampler 块有两个步骤:

> 🤔 **【困惑】**P: Re-sampulador de percepção 和 BLIP-2 de Q-Former Há alguma diferença?A: 思想几乎一样(learnable query from patch 提取信息), mas Flamingo's Re-sampulador de percepção apenas faz características de compressão visual、 não participa em comparação com o treinamento de perda; Q-Former é transformador 结构且有ITC/ITM/ITG 三个损失── pode ser considerado Re-sampulador de percepção é a versão simplificada de Q-Former──

1. Atensão cruzada: os K latentes atendem aos tokens de patches N (Q dos latentes, K/V dos patches).
   O que é que você está fazendo?
2. Auto-atenção + FFN dentro dos latentes.
   Tradução do inglês: potential impulso interno de auto-attenção + FFN。

Após 6 blocos de resampler, a saída é K = 64 tokens visuais de dim 1024, independentemente do número de patches produzidos pela ViT. Uma imagem 224x224 (196 patches) e uma imagem 480x480 (900 patches) ambos saem como 64 tokens de resampler.

> 经过 6 个复制器块后,输出是K=64 个维度为 1024 的视觉代币,无论 ViT 产生多少补丁──224x224 的图像──196 个补丁) 和 480x480 的图像──900 个补丁) 都输出为 64 个复制器代币──

Para o vídeo, o resampler é aplicado temporalmente: os patches de cada quadro produzem 64 latentes, e uma codificação posicional temporal permite que o modelo distingua t=0 de t=N. O vídeo completo se torna T * 64 tokens visuais.

> 对于视频,resampler 按时间维度应用:每的补丁 产生 64 潜在向量,时间位置编码让模型区分 t=0 和 t=N──完整视频变成T * 64 视频代币──

### Atensão transversal

Entre cada camada M do ML congelado (Flamingo usa M=4), inserir um novo bloco de atenção cruzada fechado:

> Em seguida, você pode ver o que é o M = 4 e o que é o M = 4 em cada um dos níveis de M = 5 e M = 5 em cada um dos níveis de M = 4 em cada um dos níveis de M = 4 em cada um dos níveis de M = 4 em cada um dos níveis de M = 5 em cada um dos níveis de M = 4 em cada um dos níveis de M = 5 em cada um dos níveis de M = 5 em cada um dos níveis de M = 5 em cada um dos níveis de M = 4 em cada um dos níveis de M = 5 em cada um dos níveis de M = 5 em cada um dos níveis de M = 5 em cada um dos níveis de M = 5 em cada um dos níveis de M = 5 em cada um dos níveis de M = 5 em cada um dos níveis de M = 5 em cada um dos níveis de M = 5 em cada um.

```
x_after_llm_block = llm_block(x_before)
cross = cross_attn(x_after, resampler_output)
gated = tanh(alpha) * cross + x_after
x_before_next_block = gated
```

- `alpha`é um escalar aprendizagem iniciado em zero.
  Tradução:`alpha`É um valor de aprendizagem, inicialmente para zero.
- `tanh(0) = 0`, então no init o ramo fechado contribui com zero.
  Tradução:`tanh(0) = 0`, por isso, o tempo inicial de controle da contribuição é zero.
- Como ...`alpha`Se a contribuição de atenção cruzada se afastar do zero, a contribuição cresce sem problemas.
  Tradução do português:`alpha`远离零,交叉注意力贡献平滑增长──
- A conexão residual significa que mesmo um portal totalmente aberto não sobreescreve a representação do texto do LLM; apenas adiciona informações visuais no topo.
  O texto do LLM também não se resume ao texto do LLM.

Esta é a escolha de design mais importante no Flamingo: o condicionamento visual é aditivo, fechado e zero na inicialização.

> É a escolha mais importante do design do Flamingo: as condições de visão são adicionais, controladas, inicializadas para zero.

> ️ **【易错点】**Auto-realização: esquecimento inicialização alfa=0, imediato随机初始化 → 训练前几步 LLM 文本能力就会崩塌──原因:未训练的交叉注意力输出是噪音,混入 LLM 内部表示会破坏文本知识──修复:alpha 必须初始化为0,让模型从"完美 LLM"出发,缓慢学习──
> - Não .**【类比】**零初始化门控 = "nova empregada entra em trabalho"──新员工 (新员工) 视觉层) 第一周只观察、不说话(gate=0);熟悉业务后逐渐发言(gate 慢慢打开)──直接让新员工主导决策(gate≠0初始化) 会扰乱团队原奏(破坏 LLM 文本能力)──

### A atenção cruzada mascarada para entradas entrelaçadas

Em um prompt como "<imagem A> legenda A <imagem B> legenda B <imagem C> ?", cada token de texto deve ver apenas imagens que vieram antes dele na sequência. A máscara de atenção cruzada impõe: token de texto na posição `t`Atende apenas a imagem resampler tokens cujo índice de imagem `i < i_t`onde`i_t`é a imagem mais recente antes da posição `t`"Vede apenas a última imagem anterior" ou "veja todas as imagens anteriores" são ambas opções válidas; Flamingo escolheu a primeira.

> Em similar "<imagem A> descrição A <imagem B> descrição B <imagem C> ?" de sugestões, cada texto token só deve ver a sequência localizada antes dele imagens;.`t`Of text token apenas seguir imagem índice `i < i_t`Of imagem resampler token, entre eles `i_t`É a posição`t`之前最近的图像──"Vê apenas a imagem mais recente" ou "Vê todas as imagens anteriores" são todas validas; Flamingo 选择前者──

### Aprendizagem em poucos tiros no contexto

Um sinal do Flamingo parece:

> Flamingo 提示 looks like this:

```
<image1> A photo of a cat. <image2> A photo of a dog. <image3> A photo of a
```

O modelo vê o padrão de conclusão e produz " pássaro" (ou o que a imagem 3 mostra). Não há passos de gradiente. A capacidade de aprendizagem no contexto do LLM congelado leva através da atenção cruzada fechada.

> 模型看补全模式并输出"bird" () 图片3 显示的任何内容) 无需梯度步骤──结 LLM 上下文学习能力通过门控交叉注意力传递

> 🤔 **【困惑】**P: Por que Flamingo pode aprender no contexto, enquanto BLIP-2 não pode? A: Flamingo em LLM Cada 4 layers injected visual information, LLM  interno de aprendizagem no contexto está em fase 11·05 aprendizagem) ainda está em perfeito trabalho; BLIP-2 Colocar 32 tokens de vídeo  direta para o imediato frontal, LLM colocá-los como token comum  processar, mas o objetivo de treinamento não é de poucos tiros de forma evidente, portanto, capacidade é fraca.

### Dados de formação

Flamingo treinado em três conjuntos de dados:

> Flamingo está em três grupos de treinamento:

1. MultiModal MassiveWeb (M3W): 43 milhões de páginas web com imagens e texto entrelaçados, reconstruindo a ordem de leitura.
   O site de criação de imagens e textos em formato de tela é o site de criação de imagens e textos em formato de tela.
2. Pares de imagem-texto (ALIGN + LTIP): 4,4B pares.
   O que é que você tem a ver com o seu nome?
3. Pairagem de vídeo-texto (VTP): 27 milhões de clips de vídeo curtos.
   O filme foi lançado em outubro de 2015 e conta com o apoio de um grupo de fãs.

OBELICS (2023) é uma reprodução aberta do corpus web entrelaçado, que Idefics, Idefics2 e os modelos mais abertos "como Flamingo" treinam.

> OBÉLICAS(2023) é um modelo aberto de um conjunto de linguagens de rede, ideias, ideias2 e a maioria dos modelos "casos flamingos" abertos em seu treinamento.

### OpenFlamingo e Otter

O OpenFlamingo (2023) é a reprodução aberta. Arquitetura idêntica (re-sampler do perceptor + atenção cruzada fechada em LLaMA congelado ou MPT).

> OpenFlamingo(2023) é aberto a revisão.

Otter (2023) baseia-se no OpenFlamingo com sintonização de instruções no MIMIC-IT (um conjunto de dados de instruções multimodal), mostrando também funções de atenção cruzada fechada para instruções seguidas.

> Otter(2023) em OpenFlamingo  base usando MIMIC-IT(多模态指令数据集) para realizar instruções de micro调, prova门控交叉注意力 também se aplica a instruções de seguimento.

### Os descendentes

- Idefics / Idefics2 / Idefics3: A linhagem de atenção cruzada fechada do Hugging Face, progressivamente mais simples (Idefics2 deixou cair o resampler em favor de tokens de parche direto com pooling adaptativo).
  Tradução do inglês para inglês: Idefics / Idefics2 / Idefics3: Hugging Face's门控交叉注意力谱系,逐步简化(Idefics2 去掉了 resampler,改用自适应池化的直接补丁代币)
- Transição Flamingo-Chameleon: até 2024, muitas equipes mudaram para fusão precoce (Lessão 12.11); A atenção cruzada fechada no estilo Flamingo permanece em produção onde é necessária a congelação da espinha dorsal.
  Tradução do idioma japonês: Flamingo ao Camelão: até 2024 muitos times se mudaram para a primeira fase de integração.
- A entrada entrelaçada de Gémeos: conceitualmente herda a flexibilidade de formato entrelaçado do Flamingo, embora o mecanismo exato seja proprietário.
  O conceito de gerenciamento de germes germes germes germes germes germes germes germes germes germes germes germes germes germes germes germes germes germes germes germes germes germes germes germes germes germes germes germes germes germes germes germes germes germes germes germes germes germes germes germes germes germes germes germes germes germes germes germes germes germes germes germes germes germes germes germes germes germes germes germes germes germes germes germes germes germes germes germes germes germes germes germes germes germes germes germes germes germes germes germes germes germes germes germes germes germes germes germes germes germes germes germes germes germes germes germes germes germes germes germes germes germes germes germes germes germes germes germes germes germes germes germes germes germes germes germes germes germes germes germes germes germes germes germes germes germes germes germes germes germes germes germes germes germes germes germes germes germes germes germes germes germes germes germes germes germes germes germes germes germes germes germes germes germes germes germes germes ger ger ger germes germes germes germes ger ger ger ger ger germes ger ger germes ger ger ger ger ger germes ger ger ger ger ger ger ger ger ger ger germes ger ger ger ger ger ger ger germes germes ger ger ger ger ger ger ger ger ger ger ger ger ger ger ger ger ger ger ger ger ger ger ger ger ger ger ger ger ger ger ger ger ger ger ger ger ger ger ger ger ger ger ger ger ger ger ger ger ger ger ger ger ger ger ger ger ger ger ger ger ger ger ger ger ger ger ger ger ger ger ger ger ger ger ger ger ger ger ger ger ger ger ger ger ger ger ger ger ger ger ger ger ger ger ger ger ger ger ger ger ger ger ger ger ger ger ger ger ger ger ger ger ger ger ger ger ger ger ger ger ger ger ger ger ger ger ger ger ger ger ger ger ger ger ger ger

### Comparar com BLIP-2

| | BLIP-2 | Flamingo |
|---|---|---|
| / | BLIP-2 | Flamingo |
| Visual bridge | Q-Former once at input | Gated cross-attention at every M layers |
| 视觉桥接 | 输入层一次 Q-Former | 每 M 层一次门控交叉注意力 |
| Visual tokens | 32 per image | 64 per image per cross-attn layer |
| 视觉 token | 每图 32 个 | 每个交叉注意力层每图 64 个 |
| Frozen LLM | Yes | Yes |
| 冻结 LLM | 是 | 是 |
| Few-shot in-context | Weak | Strong — the paper's centerpiece |
| 少样本上下文学习 | 弱 | 强——论文的核心亮点 |
| Interleaved inputs | No native support | Yes, the design target |
| 交织输入 | 无原生支持 | 是，设计目标 |
| Training data | 130M pairs | 1.3B pairs + 43M interleaved pages |
| 训练数据 | 1.3 亿对 | 13 亿对 + 4300 万交织网页 |
| Parameter count | 188M trained | ~10B trained (cross-attn layers) |
| 参数量 | 训练 1.88 亿 | 训练约 100 亿（交叉注意力层） |
| Compute | Days on 8 A100s | Weeks on thousands of TPUv4 |
| 计算量 | 8 块 A100 数天 | 数千块 TPUv4 数周 |

Escolha BLIP-2 para VQA de imagem única em um orçamento. Escolha Flamingo/Idefics2 para raciocínio interligado, de poucas fotos ou de imagem múltipla.

> 预算有限的单图像 VQA 选 BLIP-2──交织、少样本或多图像推理选 Flamingo/Idefics2──

## Use-o com o framework implementado.
```figure
cross-attention-fusion
```

## Usá-lo

`code/main.py`demonstra:

> `code/main.py`- O que é isso ?

1. Um resampler Perceptor em 36 tokens de patch falsos com 8 latentes aprendizes (pura atenção cruzada Python).
   Por exemplo, a tecnologia de computador de computador de computador de computador de computador de computador de computador de computador de computador de computador de computador de computador de computador de computador de computador de computador de computador de computador de computador de computador de computador de computador de computador de computador de computador de computador de computador de computador de computador de computador de computador de computador de computador de computador de computador de computador de computador de computador de computador de computador de computador de computador de computador de computador de computador de computador de computador de computador de computador de computador de computador de computador de computador de computador de computador de computador de computador de computador de computador de computador de computador de computador de computador de computador de computador de computador de computador de computador de computador de computador de computador de computador de computador de computador de computador de computador de computador de computador de computador de computador de computador de computador de computador de computador de computador de computador de computador de computador de computador de computador de computador de computador de computador de computador de computador de computador de computador de computador de computador de computador de computador de computador de computador de computador de computador de computador de computador de computador de computador de computador de computador de computador de computador de computador de computador de computador de computador de computador de computador de computador de computador de computador de computador de computador de computador de computador de computador de computador de computador de computador de computador de computador de computador de computador de computador de computador de computador de computador de computador de computador de computador de computador de computador de computador de computador de computador de computador de computador de computador de computador de computador de computador de computador de computador de computador de computador de computador de computador de computador de computador de computador de computador de computador de computador de computador de computador de computador de computador de
2. Um passo de atenção cruzada com um portão .`alpha = 0`→ saída é igual a entrada (LLM inalterado), então `alpha = 2.0`→ contribuição visual misturada.
   O que é que você está fazendo?`alpha = 0`→ 输出等于输入 (LLM 不变), então `alpha = 2.0`→ 视觉贡献混入──
3. Um construtor de máscaras entrelaçadas que produz a máscara de atenção 2D para uma sequência "(imagem 1) (texto 1) (imagem 2) (texto 2)".
   Tradução do inglês para tradução livre:交织掩码构建器,为"(图像 1) (文本 1) (图像 2) (文本 2)"序列生成 2D 注意力掩码。

## Envia-o . Produto .

Esta lição produz`outputs/skill-gated-bridge-diagnostic.md`. Dada a configuração de um VLM aberto (resampler Y/N, frequência de atn, esquema de gate), ele identifica os elementos da linhagem Flamingo e explica a estratégia de congelamento. Útil para depurar por que um ajuste fino degradou o desempenho do texto (resposta: o gate se alargou demais e rapidamente).

> 本课产 出 `outputs/skill-gated-bridge-diagnostic.md` Providenciar a configuração do VLM (se há um modelo, a frequência de atenção de transferência, o controle de portas), identificando os elementos de fluxo e explicando a estratégia de conclusão.

## Exercícios.

1. Compute o número de parâmetros visuais do Flamingo-9B: 9B LLM + 1,4B camadas de atenção cruzada fechadas + 64M resampler. Que fração dos parâmetros totais é treinada?
   Chinese Translation:计算 Flamingo-9B 的视觉参数:9B LLM + 14 亿门控交叉注意力层 + 6400 万 resampler。 Qual a proporção dos parâmetros do treinamento em relação ao total?

2. Implementar o resíduo fechado `y = tanh(alpha) * cross + x`Demonstre experimentalmente que com`alpha=0`- Não .`y==x`- Exactamente no início.
   中文翻译:用 PyTorch 实现门控残差 `y = tanh(alpha) * cross + x` Prova de experiência`alpha=0`时  `y==x`精确成立── Não é verdade.

3. Leia a Seção 3.2 do OpenFlamingo (arXiv:2308.01390) sobre como eles tratam várias imagens em um lote quando cada prompt tem uma contagem de imagens diferente. Descreva a estratégia de enchimento.
   No entanto, o que não é um problema é que o que você está fazendo é fazer uma mudança de tamanho.

4. Por que a máscara de atenção cruzada do Flamingo permite que um token de texto atenda apenas à imagem anterior mais recente do que a todas as imagens anteriores?
   Por que Flamingo está em um momento de grande dificuldade para fazer o seu trabalho?

5. Pouco-choque no contexto: construa um prompt com 4 exemplos de "imagem → cor do objeto principal" para uma nova variante do Flamingo. Descreva o padrão de precisão esperado ao variar o número de exemplos de 0 a 8.
   No entanto, o número de exemplos de 0 变到 8 时预期的准确率模式―― é o número de exemplos que são descritos em um modelo de 4 "imagem → principal objeto de cores".

## Termos-chave .

| Term | What people say | What it actually means | 中文释义 |
|------|----------------|------------------------|---------|
| 术语 | 通俗说法 | 实际含义 | |
| Perceiver resampler | "Fixed-latent cross-attention" | Module that produces K fixed tokens from a variable number of input patches | 从可变数量输入 patch 产生 K 个固定 token 的模块 |
| Gated cross-attention | "Tanh-gated bridge" | Residual layer `y = tanh(alpha)*cross + x`, learnable alpha, init 0 | 残差层 `y = tanh(alpha)*cross + x`，可学习 alpha，初始化为 0 |
| Interleaved input | "Mixed sequence" | Prompt format with images and text mixed freely in reading order | 图像和文本按阅读顺序自由混合的提示格式 |
| Frozen LLM | "No LLM gradients" | The text LLM's weights do not update; only resampler + cross-attn layers train | 文本 LLM 权重不更新；仅 resampler + 交叉注意力层训练 |
| Few-shot | "In-context examples" | Give a few (image, answer) pairs in the prompt; model generalizes without finetuning | 在提示中给几个（图像，答案）对；模型无需微调即可泛化 |
| OBELICS | "Interleaved web corpus" | Open dataset of 141M web pages with images and text in reading order | 1.41 亿网页的开放数据集，包含按阅读顺序排列的图像和文本 |
| Chinchilla | "70B frozen base" | Flamingo's frozen text LLM, from DeepMind's Chinchilla paper | Flamingo 的冻结文本 LLM，来自 DeepMind 的 Chinchilla 论文 |
| Gate schedule | "How alpha moves" | The rate at which the cross-attention gate opens during training | 训练过程中交叉注意力门控打开的速率 |
| Cross-attn frequency | "Every M layers" | How often a gated cross-attention block is inserted; Flamingo uses M=4 | 门控交叉注意力块插入的频率；Flamingo 使用 M=4 |
| OpenFlamingo | "Open reproduction" | MosaicML/LAION open checkpoint at 3-9B; architecture-identical to Flamingo | MosaicML/LAION 的 3-9B 开放检查点；架构与 Flamingo 相同 |

## Mais leitura 延伸阅读

- [Alayrac et al. — Flamingo (arXiv:2204.14198)](https://arxiv.org/abs/2204.14198)- O papel original.
  Tradução do português:Flamingo
- [Awadalla et al. — OpenFlamingo (arXiv:2308.01390)](https://arxiv.org/abs/2308.01390) Reprodução aberta.
  Tradução do português:
- [Laurençon et al. — OBELICS (arXiv:2306.16527)](https://arxiv.org/abs/2306.16527) Corpus de telas entrelaçadas.
  Tradução do inglês:交织网络语料库.
- [Jaegle et al. — Perceiver IO (arXiv:2107.14795)](https://arxiv.org/abs/2107.14795)A arquitetura geral do Perceptor.
  中文翻译:通用 Perceiver 架构──
- [Li et al. — Otter (arXiv:2305.03726)](https://arxiv.org/abs/2305.03726)- Descendente flamingo com instruções.
  Tradução do inglês: instrução de flamengo
- [Laurençon et al. — Idefics2 (arXiv:2405.02246)](https://arxiv.org/abs/2405.02246) simplificação moderna da abordagem Flamingo.
  Tradução do português:Flamingo 方法的现代化简化──
