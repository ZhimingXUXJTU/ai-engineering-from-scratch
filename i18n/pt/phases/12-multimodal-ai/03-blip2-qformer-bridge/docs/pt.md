# De CLIP para BLIP-2  Q-Former como modality bridge  de CLIP para BLIP-2: Q-Former 模态桥接

> O CLIP alinha imagem e texto, mas não pode gerar legendas, responder perguntas ou manter uma conversa. BLIP-2 (Salesforce, 2023) resolveu que com uma pequena ponte treinável: 32 vetores de consulta aprendizagem atender sobre os recursos de um ViT congelado através da atenção cruzada, em seguida, slot diretamente no fluxo de entrada de um LLM congelado. 188 milhões de parâmetros de ponte conectaram um LLM 11B a um ViT-g/14. Cada VLM baseado em adaptador até 2026  MiniGPT-4, InstructBLIP, primos de LLaVA  é um descendente. Esta lição lê a arquitetura do Q-Former, explica o seu treinamento em duas etapas e constrói uma versão de brinquedo que alimenta tokens visuais em um decodificador de texto congelado.

> **【中文解读】**CLIP só pode ver o texto em conjunto, mas não pode ser gerado. BLIP-2 usa 32 volumes de perguntas que podem ser aprendidas através de um ponto de referência de ViT e LLM, apenas 188M de parâmetros podem ser inseridos em 11B de um modelo de linguagem.

> **【拓展：Q-Former→多模态架构演进】**Q-Former é o fundador do modelo de "结视觉编码器+结LLM+轻量桥接", MiniGPT-4、InstructBLIP、LLaVA 都是其思想的后代──

**Type:** Build | **类型:** 构建
**Languages:** Python (stdlib, cross-attention + learnable-query demo) | **语言:** Python（标准库，交叉注意力 + 可学习查询演示）
**Prerequisites:** Phase 12 · 02 (CLIP), Phase 7 (Transformers) | **前置知识:** Phase 12 · 02（CLIP），Phase 7（Transformer）
**Time:** ~180 minutes | **时间:** ~180 分钟

> - Não .**【前置】**学本节前请先掌握:Fase 12·02(CLIP对比学习);Fase 7(Transformer自注意力和交叉注意力);Fase 11·04(Embebimentos)。
> - Não .**【类比】**Q-Ex = "Journalist interview"──32 个记者(question) Stand ViT 出来的 256 补丁 前面,每个人都提问自己的问题,听完回答后写下 32 条新闻摘要──这32 条摘要就是给 LLM 的"新闻简报",LLM 不用看完整 256 张原始图片──

## Objetivos de aprendizagem

- Explique por que um gargalo de engarrafamento treinavel entre um codificador de visão congelado e um LLM congelado supera a fixação de custos e estabilidade de ponta a ponta.
  Tradução do inglês para tradução do inglês para tradução do inglês para inglês para tradução do inglês para inglês para tradução do inglês para inglês para inglês para tradução do inglês para inglês para inglês para inglês para tradução do inglês para inglês para inglês para inglês para inglês para inglês para inglês para inglês para inglês para inglês para inglês para inglês para inglês para inglês para inglês para inglês para inglês para inglês para inglês para inglês para inglês para inglês para inglês para inglês para inglês para inglês para inglês para inglês para inglês para inglês para inglês
- Implementar um bloco de atenção cruzada onde um conjunto fixo de consultas de aprendizagem atende às características externas da imagem.
  Tradução do inglês para tradução do inglês para tradução do inglês para tradução do inglês para tradução do inglês para tradução do inglês para tradução do inglês para tradução do inglês para tradução do inglês para tradução do inglês para tradução do inglês para tradução do inglês para tradução do inglês para tradução do inglês para tradução do inglês para o inglês para tradução do inglês para o inglês para tradução do inglês para o inglês para tradução do inglês para o inglês para tradução do inglês para o inglês para o inglês para o inglês para tradução do inglês para o inglês para o inglês para o inglês para o inglês para o inglês para o inglês para o inglês para o inglês para o inglês para o inglês para o inglês para o inglês para o inglês para o inglês para o inglês para o inglês para o inglês para o inglês para o inglês para o inglês para o inglês para o inglês para o inglês para o inglês para o inglês para o inglês para o inglês para o inglês para o inglês.
- Passe pelo pré-treino em duas etapas do BLIP-2: representação (ITC + ITM + ITG) e depois geração (perda de LM com decodificador congelado).
  Tradução do inglês para tradução do inglês para tradução do inglês para tradução do inglês para inglês para tradução do inglês para inglês para tradução do inglês para inglês para tradução do inglês para inglês para tradução do inglês para inglês para tradução do inglês para inglês para tradução do inglês para inglês para tradução do inglês para inglês para tradução do inglês para o inglês para tradução do inglês para o inglês para tradução do inglês para o inglês para o inglês para tradução do inglês para o inglês para o inglês para o inglês para tradução do inglês para o inglês para o inglês para o inglês para o inglês para o inglês para o inglês para o inglês para o inglês para o inglês para o inglês para o inglês para o inglês para o inglês para o inglês para o inglês para o inglês para o inglês para o inglês para o inglês para o inglês para o inglês para o inglês para o inglês para o inglês para o português para o português para o português para o que significa tradução para o tradução do inglês para o tradução do inglês para o tradução do inglês para o tradução do inglês para o tradução do inglês para o tradução do inglês para o tradução do inglês para o tradução do inglês para o tradução do inglês para o tradução do inglês para o tradução do inglês para o tradução do inglês para o tradução do inglês para o tradução do inglês para o tradução do inglês para o tradução do inglês para o inglês para o tradução do inglês para o inglês para o inglês para o inglês para o tradução do inglês para o tradução do inglês para o tradução do inglês para o inglês para o inglês para o inglês para o inglês para o inglês para o inglês para o inglês.
- Compare Q-Former com o simples projetor MLP usado em LLaVA e discuta quando cada escolha ganha.
  Comparar Q-Former 和 LLaVA utilizações mais simples MLP 投影器,论证各自优势场景──

## O problema é o problema da introdução

Você tem um ViT congelado que produz 256 tokens de parches de dim 1408 por imagem. Você tem um LLM congelado 7B que espera incrustamentos de tokens de dim 4096. A ponte óbvia  uma camada linear de 1408 a 4096  funciona, mas alimentar todos os 256 tokens de parches no contexto do LLM custa 256 tokens extras por imagem.

> Você tem uma visão de visão de visão de visão de visão de visão de visão de visão de visão de visão de visão de visão de visão de visão de visão de visão de visão de visão de visão de visão de visão de visão de visão de visão de visão de visão de visão de visão de visão de visão de visão de visão de visão de visão de visão de visão de visão de visão de visão de visão de visão de visão de visão de visão de visão de visão de visão de visão de visão de visão de visão de visão de visão de visão de visão de visão de visão de visão de visão de visão de visão de visão de visão de visão de visão de visão de visão de visão de visão de visão de visão de visão de visão de visão de visão de visão de visão de visão de visão de visão de visão de visão de visão de visão de visão de visão de visão de visão de visão de visão de visão de visão de visão de visão de visão de visão de visão de visão de visão de visão de visão de visão de visão de visão de visão de visão de visão de visão de visão de visão de visão de visão de visão de visão de visão de visão de visão de visão de visão de visão de visão de visão de visão de visão de visão de visão de visão de visão de visão de visão de visão de visão de visão de visão de visão de visão de visão de visão de visão de visão de visão de visão de visão de visão de visão de visão de visão de visão de visão de visão de visão de visão de visão de visão de visão de visão de visão de visão de visão de visão de visão de visão de visão de visão de visão de visão de visão de visão de visão de

A pergunta do BLIP-2: pode comprimir a representação da imagem de 256 tokens em muito menos tokens (digamos 32) enquanto preserva informações suficientes para o LLM captar, responder perguntas e raciocinar sobre a imagem? E pode treinar esta ponte sem tocar nas espinhas congeladas, mantendo o custo de treinamento apenas nos parâmetros da ponte?

> Questão do BLIP-2: Você pode comprimir 256 tokens de imagem para significar muito menos de 32 tokens, mantendo informações suficientes para que o LLM faça descrição de imagem, responder a perguntas e raciocínio?

A resposta: um Q-Former. 32 vectores "queri" aprendizes que atendem aos tokens de patch do ViT, produzindo um resumo visual de 32 tokens que o LLM consome. Parâmetros 188M no total. Treinado com objetivos contrastativos, de correspondência e gerativos antes de tocar o LLM.

> A resposta é: Q-Former──32 个可学习的"查询"量通过交叉注意关注 ViT 的补丁代币,产生LLM 消费的32代币 视觉摘要──总共188M 参数──在接触LLM 之前使用比较、匹配和生成目标进行训练──

## O conceito central.

> **【中文解读】**BLIP-2  Introdução Q-Former  como 结视觉编码器和结 LLM 之间的轻量桥接层。Q-Former Utilize a一组可学习的查询代币 从视觉编码器提取与文本最相关的视觉特征,大幅减少了训练参数(仅训练 Q-Former),实现了高效的视觉语言对齐──

> **【拓展：BLIP-2 的高效训练】**BLIP-2 pode ser concluído em apenas um A100 em 12 horas, em comparação com o anterior método, o BLIP-2 alcançou 82,2% de precisão, perto do nível ideal da época.


> **【拓展：Q-Former 的影响】**Q-Former's design ideas ([[Use a aprender query from 结编码器提取任务相关特征) ]]) são amplamente emprestadas.


### Questões que podem ser aprendidas

O truque principal do Q-Former: em vez de deixar que os tokens de texto do LLM assistam a parches de imagem, introduzir um novo conjunto de 32 vetores de consulta apropriados `Q`As consultas são parâmetros do modelo  que são aprendidas durante o treinamento e as mesmas 32 consultas são utilizadas para cada imagem.

> Técnicas principais do Q-Former: não deixe o texto do LLM token  concentrar-se em imagem de parche, mas introduzir um novo grupo de 32 `Q`, deixem-nos* observar os patches de imagem. As consultas são os parâmetros do modelo que aprendemos no treinamento e cada imagem usa as mesmas 32 consultas.

> ️ **【易错点】**Para "32 queries is 32 张 different image queries" 错!32 queries are fixed ∼ for all images are the same ∼ para todas as imagens são as mesmas ∼ elas aprendem "como extrair 32 tipos de dimensões de informação de imagens" ∼ como cores, objetos, relações espaciais ∼) ∼ cada imagem através de Q-Former produz a mesma estrutura de 32 dimensões ∼
> 🤔 **【困惑】**P: 32 个查询 如何知道每个该看什么?A: 训练时三个损失(ITC/ITM/ITG) 会反向传播梯度告诉每个查询 该专精什么;;最终学到的 32 维编码是"损失下降最快的那个方向",不是人为指定的"颜色/物体/背景"――

Após a atenção cruzada, cada consulta contém um resumo comprimido da imagem  "descrever o objeto principal", "descrever o fundo", " contar os objetos", etc. As consultas não se especializam literalmente em rótulos semânticos; elas aprendem qualquer codificação que faça cair as perdas no fluxo de baixo.

>  Após a atenção de intercâmbio, cada consulta possui resumo de compressão de imagem"descrição dos principais objetos""",descrição de contexto""",número de objetos calculados"etc.

### Arquitetura

O Q-Former é um pequeno transformador (12 camadas, ~ 100M params) com dois caminhos:

> Q-Former é um pequeno transformador (~12 níveis, ~100M),

1. Caminho de consulta: 32 vetores de consulta fluem através da auto-atenção (entre si), então a atenção cruzada sobre os tokens de parche do ViT congelado, depois FFN.
   Chinese: 查询路径:32 个查询向量流过自注意力(彼此之间), então, em relação ao patch token do ViT, fazer um交叉注意力,最后是FFN。
2. Caminho de texto: um codificador de texto semelhante ao BERT compartilha a auto-atenção e pesos FFN com o caminho de consulta.
   Tradução do inglês:Women's Literary Road: Klasse BERT's Women's Literary Road:Women's Literary Road:Women's Literary Road:Women's Literary Road:Women's Literary Road:Women's Literary Road:Women's Literary Road:Women's Literary Road:Women's Literary Road:Women's Literary Road:Women's Literary Road:Women's Literary Road:Women's Literary Road:Women's Literary Road:Women's Literary Road:Women's Literary Road:Women's Literary Road:Women's Literary Road:Women's Literary Road:Women's Literary Road:Women's Literary Road:Women's Literary Road:Women's Literary Road:Women's Literary Road:Women's Literary Road:Women's Literary Road:Women's Literary Road:Women's Literary Road:Women's Literary Road:Women's Literary Road:Women's Literary Road:Women's Literary Road:Women's Literary Road:Women's Literary Road:Women's the Road to the Road:Women's literary Road:Women's the Road to the Road:Women's own right

No tempo de treinamento, ambos os caminhos são executados. As consultas e o texto interagem através da auto-atenção compartilhada, o que significa que as consultas podem condicionar o texto para tarefas que precisam dele (ITM, ITG). No momento de inferência para a entrega do VLM, apenas as consultas fluem, produzindo 32 tokens visuais.

>  training 时两条路径同时运行──查询和文本通过共享的自注意交互, isto significa que a consulta pode ser feita em condições de texto em função das tarefas do texto.

### Formação em duas fases

O BLIP-2 prepara-se em duas fases:

> BLIP-2 分两阶段预训练:

Fase 1: aprendizagem representativa (sem Mestrado em Direito Executivo).
- ITC (imagem-texto contrastivo): contrastivo de estilo CLIP entre os tokens de consulta em conjunto e o token CLS de texto.
  Chinese Translation:ITC(图文对比):池化查询 token e文本 CLS token 之间类 CLIP对比损失──
- ITM (imagem-texto de correspondência): classificador binário  é este par de imagem-texto de correspondência?
  O que é que é o problema do uso de um sistema de controle de dados?
- ITG (Generação de texto baseada em imagem): LM causal cabeçalho em texto, condicionado às consultas. Força consultas a codificar conteúdo gerável por texto.
  Tradução do inglês para tradução do inglês para tradução do inglês para tradução do inglês para tradução do inglês para tradução do inglês para tradução do inglês para tradução do inglês para tradução do inglês para tradução do inglês para tradução do inglês para tradução do inglês para tradução do inglês para tradução do inglês para tradução do inglês para tradução do inglês para tradução do inglês para tradução do inglês para tradução do inglês para tradução do inglês para tradução do inglês para tradução do inglês para tradução do inglês para tradução do inglês para tradução do inglês para tradução do inglês para tradução do inglês para tradução do inglês para tradução do inglês para tradução do inglês para o inglês para o inglês para tradução do inglês para o inglês para o inglês para o inglês para o inglês para o inglês para o inglês para o inglês para o inglês para o inglês para o inglês para o inglês para o inglês para o inglês para o inglês para o inglês para o inglês para o inglês para o inglês para o inglês para o inglês para o inglês para o inglês para o inglês para o inglês.

> - Não .**【类比】**Três perdas de trabalho:ITC = "ver o texto" ([[grossura]] em linha de frente);ITM = "julgar que o texto não é realmente escrito" ([[grossura]] em linha de frente);ITG = "ver o texto escrito em linha de frente" ([[capacidade de produção]])

Só os trens Q-Former, o ViT está congelado, não há LLM envolvido.

> 仅训练 Q-Former──ViT 结──不涉及 LLM──

Fase 2: aprendizagem gerativa. Anexe um LLM congelado (OPT-2.7B ou Flan-T5-XL, etc.). Projete os 32 resultados de consulta para o LLM de inserção dim através de uma pequena camada linear. Prepare-os para o texto de instrução. Treinar apenas a projeção linear e o Q-Former em LM perda sobre a sequência de instrução + imagem + legenda concatenada.

> Segundo estágio: gerar aprendizagem. Conectar um LLM 结(OPT-2.7B ou Flan-T5-XL etc)  através de um pequeno nível linear, 32 consultas serão enviadas para o LLM 嵌度.

Após a etapa 2, a projeção Q-Former + é o adaptador visual completo. Na inferência: imagem → ViT → Q-Former → proj linear → pré-pendido ao texto → LLM congelado emite saída.

> Segundo estágio, Q-Former + 投影就是完整的视觉适配器──推理时:图像 → ViT → Q-Former → 线性投影 → 前置到文本 → 结 LLM 生成输出──

### Economia de parâmetros

BLIP-2 com ViT-g/14 (1.1B, congelado) + OPT-6.7B (6.7B, congelado) + Q-Former (188M, treinado) = 8B total, 188M treinado. O Q-Former sozinho é ~ 2,4% dos parâmetros da pilha completa.

> BLIP-2 Utilize ViT-g/14(11 mil milhões,结) + OPT-6.7B(67 mil milhões,结) + Q-Former(1.88 mil milhões, treinamento) = 共 80 mil milhões, treinamento 1.88 mil milhões, Q-Former 僅占全参数约2.4%──

Qualidade: BLIP-2 combina ou supera o Flamingo-80B em VQA de tiro zero, enquanto é 50 vezes menor.

> 质量:BLIP-2 在零样本 VQA 上匹配或超越 Flamingo-80B,同时小了50倍──桥接方案有效──

### O instructoBLIP e o Q-Former, que tem conhecimento das instruções

O instructoBLIP (2023) estende o Q-Former com uma entrada extra: o próprio texto de instrução. No tempo de atenção cruzada, as consultas agora têm acesso tanto aos patches de imagem quanto à instrução. As consultas podem se especializar por instrução ("contar os carros", "descrever o humor") em vez de aprender um único resumo fixo.

> InstructBLIP(2023) através de extra-input expandido Q-Former: instrução texto em si mesma. Em Atenção de intervalo, consulta pode ser feita simultaneamente para visualizar o parche de imagem e instrução.

### MiniGPT-4 e a abordagem apenas com projector

MiniGPT-4 manteve o Q-Former, mas treinou apenas a projeção linear de saída enquanto congelava tudo o resto. Barato, mas o custo é qualidade  as consultas eram de BLIP-2, não suas. Boa para iteração rápida, não a melhor arquitetura.

> MiniGPT-4 guarda Q-Former, mas apenas treinamento de saída linear projeção,结其他一切──便宜,但代价是质量查询是BLIP-2,不是你的──适合快速代,不是最佳架构──

### Por que a LLaVA foi mais simples

LLaVA (2023, lição 12.05) substituiu o Q-Former por um simples MLP de 2 camadas que projeta cada token de patch ViT em espaço LLM  576 tokens por imagem para uma grade 24x24, todos alimentados para o LLM. Pior compressão, mas deixa o LLM assistir em vez de manchas crudas. Na época, isso era controverso; no final de 2023 era dominante porque os dados de instrução visual (LLaVA-Instruct-150k) provaram que o MLP poderia ser treinado para preservar sinal suficiente. A compensação: O contexto do LLaVA se enche mais rápido, mas se escala naturalmente para a imagem e o vídeo.

> LLaVA(2023, § 12.05 课) substituiu o MLP de 2 níveis simples por Q-Former, que projetará cada token de parche ViT 投投投到LLM 空间24x24 网格下每张图像 576 个 token,全部给LLM.

> 🤔 **【困惑】**学完本节还会问:Q-Former vs LLaVA MLP 该选哪个? 短上下文 + 高质量 → Q-Former(压缩32 token 精心训练);长上下文 + 多图/视频 → LLaVA MLP(per token 信息量大但灵活) ⋅ 2026 ̇ Most VLMs use MLP,因为 visual instrução dados são suficientes, MLP aprender de suficientemente boa e mais fácil de expandir―

Em 2026, o campo se divide: Q-Former sobrevive onde o orçamento de token importa (vídeo longo, muitas imagens); o projeto MLP domina onde a qualidade bruta por token é a prioridade.

> Até 2026, áreas de divisão: Q-Former  em token  orçamento importante  长视频、多图像) sobreviver; MLP 投影器  em cada token 原质量优先占占占い

### Atensão cruzada: Flamingo, o ancestral

Flamingo (Lessão 12.04) antecedeu BLIP-2 e usou a mesma ideia de atenção cruzada, mas em cada camada LLM congelada, não como uma única ponte. BLIP-2 mostrou que você pode comprimir apenas para a camada de entrada e ainda funcionar. Gemini e Idefics combinam ambos: tokens de entrada entrelaçados mais atenção cruzada fechada opcional para poucas fotos no contexto.

> Flamingo (第 12.04 课) anterior ao BLIP-2, usando o mesmo pensamento de transferência de atenção, mas em cada nível de LLM, e não em um único ponto de ligação.

### Os descendentes de 2026

- Q-Former: BLIP-2, InstructBLIP, MiniGPT-4, e a maioria dos modelos de vídeo-linguagem por razões de orçamento token.
  中文翻译:Q-Former:BLIP-2、InstructBLIP、MiniGPT-4,以及大多数视频语言模型 (), já que é um símbolo do orçamento.
- Re-estamplador de percepção: variante do Flamingo (Lessão 12.04); família Idefics, Eagle, OmniMAE.
  Tradução do português:Persceptor resampler:Flamingo 的变体 (Flamingo 的变体)
- Projector MLP: LLaVA, LLaVA-NeXT, LLaVA-OneVision, Cambrian-1.
  中文翻译:MLP 投影器:LLaVA、LLaVA-NeXT、LLaVA-OneVision、Cambrian-1──
- Polar de atenção: VILA, PaliGemma.
  O que é que é o "PaliGemma"?

A questão decisiva é se você está limitado no orçamento de token ou na qualidade por token.

> Quatro esquemas são válidos. A questão decisiva é se o seu limite é o token.

## Use-o com o framework implementado.
```figure
modality-projection
```

## Usá-lo

`code/main.py`construi uma atenção cruzada no estilo stdlib Q-Former:

> `code/main.py`Construir uma biblioteca de padrões Q-Former 风格的交叉注意力:

1. Simula 256 tokens de parche de imagem (dim 128).
   Chinese: 模拟 256 个图像补丁代号 ((维度 128) 』
2. Instantanear 32 consultas de aprendizagem (dim 128).
   Tradução do inglês: 个可学习查询
3. Execute a atenção cruzada ponto-produto escalado (Q das consultas, K/V dos patches).
   Tradução do inglês: 运行缩放点积交叉注意力
4. Projeto para LLM-dim (512) através de uma camada linear.
   Tradução do inglês:                                                                                                                                                                                                                                                            
5. Faça 32 tokens visuais prontos para LLM.
   Tradução do inglês para tradução do inglês:

Todas as matemáticas em Python puro (bucles aninhados sobre vetores). Joguete mas forma correta. A matriz de peso de atenção é impressa para que você possa ver quais patches cada consulta tirada de.

> Todos os cálculos matemáticos usam Python puro (~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~

## Envia-o . Produto .

Esta lição produz`outputs/skill-modality-bridge-picker.md`. Dada a configuração de VLM-alvo (contagem de tokens do codificador de visão, orçamento contextual do LLM, restrições de implantação, objetivo de qualidade), recomenda o resampler Q-Former vs. MLP vs. Perceptor com uma breve justificação e uma estimativa da contagem de parâmetros para cada ponte.

> 本课产 出 `outputs/skill-modality-bridge-picker.md`△ deu-se um determinado objetivo VLM 配置(vidéo编码器 token 数、LLM 上下文预算、部署约束、质量目标), recomenda Q-Former vs MLP vs Perceiver resampler,

## Exercícios.

1. Implementar o bloco de atenção cruzada no PyTorch. Verifique que com 32 consultas e 256 chaves/valores, a matriz de peso da atenção é 32 x 256 e cada linha somou a 1 após softmax.
   O sistema de controle de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados

2. No BLIP-2 estágio 1, o Q-Former executa três perdas simultaneamente: ITC, ITM, ITG. Escreva a assinatura para frente para cada um em pseudo-código. Qual deles requer que o caminho de codificação de texto seja ativo?
   Em primeiro lugar, Q-Former, em terceiro lugar, em terceiro lugar, em terceiro lugar, em terceiro lugar, em terceiro lugar, em terceiro lugar, em terceiro lugar, em terceiro lugar, em terceiro lugar, em terceiro lugar, em terceiro lugar, em terceiro lugar, em terceiro lugar, em terceiro lugar, em terceiro lugar, em terceiro lugar, em terceiro lugar, em terceiro lugar, em terceiro lugar, em terceiro lugar, em terceiro lugar, em terceiro lugar, em terceiro lugar, em terceiro lugar, em terceiro lugar, em terceiro lugar, em terceiro lugar, em terceiro lugar, em terceiro lugar, em terceiro lugar, em terceiro lugar, em terceiro lugar, em terceiro lugar, em terceiro lugar, em terceiro lugar, em terceiro lugar, em terceiro lugar, em terceiro lugar, em terceiro lugar, em terceiro lugar, em terceiro lugar, em terceiro lugar, em terceiro lugar, em terceiro lugar, em terceiro lugar, em terceiro lugar, em terceiro lugar, em terceiro lugar, em terceiro lugar, em terceiro lugar, em terceiro lugar, em terceiro lugar, em terceiro lugar, em terceiro lugar, em terceiro lugar, em terceiro lugar, em terceiro lugar, em terceiro lugar, em terceiro lugar, em terceiro lugar, em terceiro lugar, em terceiro lugar, em terceiro lugar, em terceiro lugar, em terceiro, em terceiro lugar, em terceiro, em terceiro, em terceiro lugar, em terceiro, em terceiro, em terceiro, em terceiro, em terceiro, em terceiro, em terceiro, em terceiro, em terceiro, em terceiro, em terceiro, em terceiro, em terceiro, em terceiro, em terceiro, em terceiro, em terceiro, em terceiro, em terceiro, em terceiro, em terceiro, em terceiro, em terceiro, em terceiro, em terceiro, em terceiro, em terceiro, em terceiro, em terceiro, em terceiro, em terceiro, em terceiro, em terceiro, em terceiro, em terceiro, em terceiro, em terceiro, em terceiro, em terceiro, em terceiro, em terceiro, em terceiro, em terceiro, em terceiro, em terceiro, em terceiro, em terceiro, em terceiro, em terceiro, em terceiro, em terceiro, em terceiro, em terceiro, em terceiro, em terceiro, em terceiro, em terceiro, em terceiro, em terceiro, em terceiro, em a em terceiro, em terceiro, em a em terceiro, em a em a em a em terceiro, em a em a em a em a em a em a em a mais em a mais em a mais em a mais em a

3. Comparar contagens de parâmetros: Q-Former (12 camadas, 768 escondidas) vs um projetor MLP de 2 camadas (1408 → 4096, duas camadas). Em que escala LLM o custo de 188M Q-Former compensa na eficiência do treinamento?
   Chinese: Q-Former (Q-Former) 12 层,768 隐藏维度) vs 2 层 MLP 投影器 (MLP 投影器) 1408 → 4096,两层) 

4. Leia a Seção 3.2 do artigo BLIP-2 (arXiv:2301.12597) sobre como o Q-Former é iniciado.
   Tradução do inglês para tradução do português: read BLIP-2 论文(arXiv:2301.12597) 节 3.2 节关于Q-Former 初始化部分──解释为什么从BERT-(base非随机)初始化加速收──

5. Para um vídeo de 10 minutos a 1 FPS amostrado para 60 quadros, calcule o custo de token por quadro em (Q-Former → 32 tokens / frame) vs (projector MLP → 576 tokens / frame). Qual se encaixa em uma janela de contexto de LLM com 128k-token?
   Para 10 minutos de vídeo em 1 FPS 采样为60 ,计算每代币 成本:(Q-Former → 32 token/) vs.

## Termos-chave .

| Term | What people say | What it actually means | 中文释义 |
|------|----------------|------------------------|---------|
| 术语 | 通俗说法 | 实际含义 | |
| Q-Former | "Querying transformer" | Small transformer with 32 learnable query vectors that cross-attend to frozen ViT features | 带有 32 个可学习查询向量的小型 Transformer，交叉关注冻结的 ViT 特征 |
| Learnable queries | "Soft prompt for vision" | A fixed set of parameters that serve as the query side of cross-attention; learned per model, shared across all inputs | 作为交叉注意力查询侧的固定参数集；按模型学习，所有输入共享 |
| Cross-attention | "Q from here, K/V from there" | Attention where query, key, and value come from different sources; how the queries pull from ViT patches | 查询、键和值来自不同来源的注意力；查询如何从 ViT patch 提取信息 |
| ITC | "Image-text contrastive" | CLIP-style loss applied to Q-Former pooled queries vs text CLS | 应用于 Q-Former 池化查询与文本 CLS 的类 CLIP 对比损失 |
| ITM | "Image-text matching" | Binary classifier on hard-negative-mined pairs; forces the queries to discriminate fine-grained mismatches | 难负例挖掘对上的二分类器；强制查询区分细粒度不匹配 |
| ITG | "Image-grounded text generation" | Causal LM loss where text is generated conditioned on queries; forces queries to encode text-decodable content | 以查询为条件生成文本的因果 LM 损失；强制查询编码可解码为文本的内容 |
| Two-stage pretraining | "Representation then generative" | Stage 1 trains Q-Former alone (ITC/ITM/ITG); Stage 2 attaches frozen LLM and trains only the projection + Q-Former | 第一阶段仅训练 Q-Former；第二阶段连接冻结 LLM，仅训练投影 + Q-Former |
| Frozen backbone | "Do not finetune" | The vision encoder and LLM weights are fixed; only the bridge trains | 视觉编码器和 LLM 权重固定；仅训练桥接层 |
| Projection head | "Linear to LLM dim" | Final linear layer mapping Q-Former output to the LLM's embedding dimension | 将 Q-Former 输出映射到 LLM 嵌入维度的最终线性层 |
| Perceiver resampler | "Flamingo's version" | Similar learnable-query cross-attention, used by Flamingo at every layer rather than as a single bridge | 类似的可学习查询交叉注意力，Flamingo 在每层使用而非单一桥接 |

## Mais leitura 延伸阅读

- [Li et al. — BLIP-2 (arXiv:2301.12597)](https://arxiv.org/abs/2301.12597) o papel central.
  Tradução do português:BLIP-2
- [Li et al. — BLIP (arXiv:2201.12086)](https://arxiv.org/abs/2201.12086) o antecessor com o trio ITC/ITM/ITG.
  中文翻译:前作,包含 ITC/ITM/ITG 三联损失──
- [Li et al. — ALBEF (arXiv:2107.07651)](https://arxiv.org/abs/2107.07651) "align antes de fusão"  o ancestral conceitual do treino de fase 1.
  Tradução do inglês para "Predecessor de um treinamento"
- [Dai et al. — InstructBLIP (arXiv:2305.06500)](https://arxiv.org/abs/2305.06500)- Q-Former, consciente de instruções.
  中文翻译:指令感知的 Q-Former。
- [Zhu et al. — MiniGPT-4 (arXiv:2304.10592)](https://arxiv.org/abs/2304.10592) abordagem apenas de projector.
  Tradução do inglês:
- [Jaegle et al. — Perceiver IO (arXiv:2107.14795)](https://arxiv.org/abs/2107.14795) arquitetura geral para a atenção transversal entre as questões de aprendizagem.
  Tradução do inglês para tradução livre:
