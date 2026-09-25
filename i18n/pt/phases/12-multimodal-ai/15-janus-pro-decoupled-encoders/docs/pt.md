# Janus-Pro: Encoders Desacoplados para Modelos Multimodal Unificados

> Os modelos multimodal unificados têm uma tensão inevitável. A compreensão requer características semânticas  VECTORES de saída SigLIP ou DINOv2 ricos em informações de nível conceitual. A geração quer códigos amigáveis à reconstrução. Tokens VQ que se compõem de volta em pixels crisp. Os dois objetivos não são compatíveis em um único codificador. Janus (DeepSeek, outubro de 2024) e Janus-Pro (DeepSeek, janeiro de 2025) argumentam que a solução é parar de tentar: desacoplar os dois codificadores. Compartilhar o corpo do transformador entre tarefas, mas compreensão de rota através de SigLIP e geração através de um tokenizer VQ. No 7B, o Janus-Pro vence o DALL-E 3 no GenEval enquanto compara o LLaVA no MMMU. Esta lição explica por que dois codificadores funcionam quando um falha.

> **【中文解读】**Janus-Pro(DeepSeek,2025年1月) resolver uma contradição fundamental: compreender tarefas precisa de significados característicos(SigLIP), gerar tarefas precisa de reconstruir um bom código(token VQ)。 ambos não podem ser compativeis com um único codificador。 Janus-Pro's resposta é: compreender por SigLIP 路径, gerar por VQ 路径, compartir Transformer 主体。7B 参数就在 GenEval 上击败了DALL-E 3。

> **【拓展：解耦编码器的产业影响】**O conceito de codificador já se tornou uma estrutura padrão do modelo de 2026.[1] O InternVL-U integrará o conceito de codificador no quadro de treinamento prévio de vários modelos.

**Type:** Build  | **类型:** 构建
**Languages:** Python (stdlib, dual-encoder routing + shared-body signal) | **语言:** Python（标准库，双编码器路由 + 共享体信号）
**Prerequisites:** Phase 12 · 13 (Transfusion), Phase 12 · 14 (Show-o) | **前置知识:** Phase 12 · 13（Transfusion），Phase 12 · 14（Show-o）
**Time:** ~120 minutes | **时间:** ~120 分钟

> - Não .**【前置】**O estudo foi realizado em uma área de pesquisa de pesquisa em pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa em pesquisa de pesquisa de pesquisa de pesquisa em pesquisa de pesquisa de pesquisa de pesquisa em pesquisa de pesquisa em pesquisa de pesquisa de pesquisa de pesquisa de pesquisa em pesquisa de pesquisa em pesquisa de pesquisa em pesquisa de pesquisa em pesquisa de pesquisa de pesquisa de pesquisa de pesquisa em pesquisa de pesquisa em pesquisa de pesquisa de pesquisa em pesquisa de pesquisa de pesquisa em pesquisa de pesquisa em pesquisa em pesquisa em pesquisa em pes
> - Não .**【类比】**Janus-Pro = "esquerra esquerda" (左脑) = SigLIP (语义理解,认识"猫"的概念); Right Brain = VQ-VAE (右脑) (像素重建,能画出猫的细节) (VQ-VAE) (像素重建,能画出猫的细节) (其他统一模型) (Janus-Pro = 强迫一个脑区同时做两件事,两边都不极致; Janus-Pro = 接受左右脑分工,共享脑干 (共脑干) (Transformer 主体) (Transformer 主体) (Transformer 主体) (Transformer 主体) (Transformer 主体) (Transformer 主体) (Transformer 主体) (Transformer 主体) (Transformer 主体) (Transformer 主体) (Transformer 主体) (Transformer 主体) (Transformer 主体) (Transformer) (Transformer) (Transforming) (Transforming) (Transforming) (Transforming) (Transforming) (Transforming) (Transforming) (Transforming) (Transforming) (Transforming) (Transforming) (Transforming))) (Transforming) (Transforming) (Transforming) (Transforming) (Transforming) (Transforming) (Transforming) (Transforming) (Transforming) (Transforming) (Transforming) (Transforming) (Transforming) (Transforming) (Transforming) (Transforming) (Transforming) (Transforming) (Transforming) (Transforming) (Transforming) (Transforming) (Trans) (Trans) (Transforming) (Transforming) (Trans) (Trans) (Trans) (Trans) (Trans) (Trans) (Trans) (Trans) (Trans) (Trans) (Trans) (Trans) (Trans) (Trans) (Trans) (Trans) (Trans) (Trans) (Trans) (Trans) (Trans) (Trans) (Trans) (Trans) (Trans) (Trans) (Trans) (Trans) (Trans) (Trans) (Trans) (Trans) (Trans) (Trans) (Trans) (Trans) (

## Objetivos de aprendizagem

- Explique por que um único codificador compartilhado compromete a compreensão ou a qualidade da geração.
  > Explica por que um único codificador compartilhado prejudicará a compreensão ou gerará qualidade.
- Descreva o roteamento do Janus-Pro: SigLIP funciona no lado de entrada para compreensão, tokens VQ tanto na entrada quanto na saída para geração.
  > Descrição de rotas de Janus-Pro: compreender rotas de entrada com SigLIP características, gerar rotas de entrada e saída com token VQ。
- Rastrear a escalagem de dados que faz o Janus-Pro ter sucesso onde o Janus não.
  > 追溯让Janus-Pro Success e Janus 失败的数据混合扩展──
- Compare arquiteturas descopladas (Janus-Pro), acopladas-contínuas (Transfusão) e acopladas-discreta (Show-o).
  > Comparar o que é o "Jano-Pro"

## O problema é o contexto do problema .

Os modelos unificados compartilham um corpo transformador em toda a compreensão e geração.

> 统一模型在理解和生成之间共享 Transformer 主体──之前的尝试(Chameleon、Show-o、Transfusion)都使用一个视觉分词器处理两个方向──分词器是妥协:

- Otimizado para reconstrução (geração): VQ-VAE capta detalhes de píxeles finos, mas produz tokens com fraca coerência semântica.
  Chinese: 中文翻译:为重建优化 (生成):VQ-VAE 捕获细粒度像素细节,但产生的代号语义一致性弱──
- Otimizado para semântica (compreensão): Embedings SigLIP agrupam imagens "cat" perto de tokens "cat", mas não permitem boa reconstrução.
  Chinese: 译文:为语义优化(理解):SigLIP 嵌入将"猫"图像归归归"猫"的代号附近,但不允许好的重建──

A empresa de tecnologia de telecomunicações (Show-o e Transfusion) paga por isso com um imposto de qualidade visível em uma direcção.

> Show-o 和 Transfusion para isso pagou um ótimo imposto de qualidade.

## O conceito central.

> **【中文解读】**Janus-Pro(DeepSeek) utilizando o mesmo sistema de programação de Mestrado em Matemática, cada um deles se concentra em diferentes formas de programação de vídeo.

> **【拓展：解耦编码器的动机】**Compreender tarefas requer características linguísticas de alto nível, gerar tarefas requer características de detalhes de nível inferior. Um único programador é difícil de fazer bem o mesmo.


### Codificação visual descoplada

A arquitetura do Janus-Pro separa os dois codificadores:

> A estrutura do Janus-Pro será dividida em dois programadores:

- Compreensão do caminho. Imagem de entrada → SigLIP-SO400m → 2 camadas MLP → corpo transformador.
  中文翻译:理解路径──输入图像 → SigLIP-SO400m → 2 层 MLP → Transformer 主体──
- Caminho de geração. Imagem de entrada (se condicionada em uma imagem existente) → Tokenizer VQ → IDs de token → corpo transformador.
  中文翻译:生成路径──输入图像(如果以现有图像为条件)→ VQ 分词器 → token ID → Transformer 主体──
- Geração de saída. Tokens de imagem previstos pelo transformador → decodificador VQ → pixels.
  中文翻译:输出生成──Transformer 预测的图像代币 → VQ 解码器 → 像素──

O corpo do transformador é compartilhado, tudo a montante e a baixo do corpo é específico para a tarefa.

> Transformer 主体是共享的. Tudo o que tem a ver com o transformador é um trabalho específico.

As entradas são desambiguadas por formato de prompt: a `<understand>`rotas de rotas através do SigLIP; `<generate>`Ou o roteamento é implícito da tarefa.

> 输入通过提示格式消歧:`<understand>`标签路由到 SigLIP;`<generate>`路由到VQ──或路由从任务隐式确定──

### Por que isto funciona

Compreender a perda obtém recursos SigLIP, que o pré-treinamento de estilo CLIP ajudou para a semântica semelhança.

> Compreender a perda de obter características SigLIP, o treinamento previo do estilo CLIP já melhorou estas características para significar a semelhança entre as características.

A perda de geração obtém tokens VQ, que um tokenizer ajudou para reconstrução. A qualidade da imagem melhora em relação ao Show-o porque os códigos VQ se compõem de volta para pixels de forma limpa.

> O VQ 码能干净地组合回像素── já foi re-construído.

O corpo do transformador compartilhado vê duas distribuições de entrada (SigLIP e VQ) e aprende a trabalhar com ambos.

> Compartilha de Transformadores: √√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√

### Escalagem de dados  Janus vs Janus-Pro

Janus (original, arXiv 2410.13848) introduziu o desacoplamento, mas em pequena escala (1.3B parâmetros, dados limitados).

> Janus(原始版,arXiv 2410.13848) introdução para o conhecimento 但规模较小(13 亿参数,有限数据) ・Janus-Pro(arXiv 2501.17811) foi expandido:

- Parâmetros 7B (versus 1.3B).
  Tradução do inglês:70 mil milhões de参数 (em grego:70 mil milhões de参数)
- 90 milhões de pares de imagem-texto para a fase 1 (alinhamento) a partir de 72 milhões.
  Chinese translation: 9000 milhões de dólares em dólares para a primeira fase, de 7200 milhões em aumento.
- 72M para a fase 2 (unificada) a partir de 26M.
  O número de pessoas que estão em situação de risco é de aproximadamente 20 milhões.
- Adicionou 200 mil amostras de instruções de geração de imagens para a fase 3.
  Para a terceira fase, foram aumentados 200.000 imagens de instruções de gerenciamento de imagens.

O resultado: Janus-Pro-7B combina com LLaVA na MMMU (60.3 vs ~ 58) e vence DALL-E 3 na GenEval (0.80 vs 0.67). Um modelo aberto, competitivo em ambos os lados do espectro unificado.

> Resultado:Janus-Pro-7B em MMMU 上匹配 LLaVA(60.3 vs ~58), em GenEval 上击败DALL-E 3(0.80 vs 0.67);; um modelo aberto, em ambos os lados do conjunto da família têm competência;;

### JanusFlow  a variante de fluxo rectificada

JanusFlow (arXiv 2411.07975) troca o caminho de geração de VQ por um caminho de geração de fluxo rectificado (contínuo). A divisão se torna SigLIP-para-entendimento + fluxo rectificado-para-geração.

> JanusFlow(arXiv 2411.07975) vai substituir o VQ 生成路径为整流流生成路径(连续) ・・・分离成 SigLIP 用于理解 + 整流用于生成──质量上限进一步提升──架构仍然是解编码器-共享主体──

### O trabalho do corpo compartilhado

O corpo transformador processa uma sequência unificada, mas com duas distribuições de entrada.

> Transformador principal processamento de unidade de ordem mas tem duas distribuições de entrada.

- Para compreensão: consome recursos SigLIP + tokens de texto → emitir texto autoregressivamente.
  中文翻译:理解:消费 SigLIP特征 + 文本代币 → 自回归输出文本。
- Para geração: consome tokens de texto + (tokens opcionais de imagem VQ) → emite tokens de imagem VQ de forma autoregressiva.
  中文翻译:生成:消费文本代币 +(可选图像 VQ代币)→ 自回归输出图像 VQ代币──

O corpo não tem pesos específicos de modalidade por bloco. É o transformador de estilo texto que você espera encontrar dentro de Qwen ou Llama, mais os dois adaptadores de entrada.

> O principal não tem um modelo específico de peso. É o que você espera encontrar no Qwen ou Llama Central.

Curiosamente, isso significa que o corpo do Janus-Pro pode ser iniciado a partir de um LLM pré-treinado.

> Curiosamente, isso significa que o Janus-Pro  tema pode ser iniciado a partir do LLM pré-treinamento.

### Comparado com o InternVL-U

O curso de formação (LEC 12.10) é o de acompanhamento de 2026.

> InternVL-U(第 12.10 课) é o segundo ciclo de 2026 ano.

- Pre-treinamento multimodal nativo (internVL3 spine).
  Tradução do português: originalvivo (de origem)
- Roteamento de codificador descoplado (SigLIP em, VQ + difusão termina).
  Tradução do inglês para tradução livre: [ˈɡɒnɡɡɡɡɡɡɡɡɡɡɡɡɡɡɡɡɡɡɡɡɡɡɡɡɡɡɡɡɡɡɡɡɡɡɡɡɡɡɡɡɡɡɡɡɡɡɡɡɡɡɡɡɡɡɡɡɡɡɡɡɡɡɡɡɡɡɡɡɡɡɡɡɡɡɡɡɡɡɡɡɡɡɡɡɡɡɡɡɡɡɡɡɡɡɡɡɡɡɡɡɡɡɡɡɡɡɡɡɡɡɡɡɡɡɡɡɡɡɡɡɡɡɡɡɡɡɡɡɡɡɡɡɡɡɡɡɡɡɡɡɡɡɡɡɡɡɡɡɡɡɡɡɡɡɡɡɡɡɡɡɡɡɡɡɡɡɡɡɡɡɡɡɡɡɡɡɡɡɡɡɡɡɡɡɡɡɡɡɡɡɡɡɡɡɡɡɡɡɡɡɡɡɡɡɡɡɡɡɡɡɡɡɡɡɡɡɡɡɡɡɡɡɡɡɡɡɡɡɡɡɡɡɡɡɡɡɡɡɡɡɡɡɡɡɡɡɡɡɡɡɡɡɡɡɡɡɡɡɡɡɡɡɡɡɡɡɡɡɡɡɡɡɡɡɡɡɡɡɡɡɡɡɡɡɡɡɡɡɡɡɡɡɡɡɡɡɡɡɡɡɡɡɡɡɡɡɡɡɡɡɡɡɡɡɡɡɡɡɡɡɡɡɡɡɡɡɡɡɡɡɡɡɡɡɡɡɡɡɡɡɡɡɡɡɡɡɡɡɡɡɡɡɡɡɡɡɡɡɡɡɡɡɡɡɡɡɡɡɡɡɡɡɡɡɡɡɡɡɡɡɡɡɡɡɡɡɡɡɡɡɡɡɡɡɡɡɡɡɡɡɡɡɡɡɡɡɡɡɡɡɡɡɡɡɡɡɡɡɡɡɡɡɡɡɡɡɡɡɡɡɡɡɡɡɡɡɡɡɡɡɡɡɡɡɡɡɡɡɡɡɡɡɡɡɡɡɡɡɡɡɡɡɡɡɡɡɡɡɡɡɡɡɡɡɡɡɡɡɡɡɡɡɡɡɡɡɡɡɡɡɡɡɡɡɡ
- Compreensão unificada + geração + edição.
  中文翻译:统一理解 + 生成 + 编辑。

O InternVL-U substitui a escolha arquitetônica do Janus-Pro em um quadro maior.

> O InternVL-U incorporou a estrutura do Janus-Pro em um quadro maior.

### Limitações

Os codificadores descoplados adicionam complexidade arquitetônica. Dois tokenizadores para treinar, dois caminhos de entrada para manter, dois conjuntos de modos de falha. Para produtos que não precisam de geração, o Janus-Pro é superengenharia.

> O editor aumentou a complexidade da estrutura. Dois componentes foram treinados, dois caminhos de entrada foram mantidos, dois grupos foram derrotados.

Para os produtos que não necessitam de compreensão, o Janus- Pro é supercalificado  escolha um modelo Stable Diffusion 3 / Flux.

> 对于不需要理解的产品,Janus-Pro 大材小用选择 稳定扩散 3 /流动模型──

Para produtos que precisam de ambos, o Janus-Pro é agora a arquitetura aberta de referência.

> Para os dois produtos necessários, o Janus-Pro é agora uma estrutura aberta de referência.


> **【拓展：Janus-Pro 在基准上的表现】**O Janus-Pro em vários modelos compreende o modelo de um programador superior a um modelo de código de base de 3 a 5%, em imagens de geração de base de cerca de 10 a 15%.


## Use-o em prática.
```figure
l5-janus-decouple
```

## Usá-lo

`code/main.py`Simula o roteamento Janus-Pro:

> `code/main.py`模拟 Janus-Pro 路由:

- Dois codificadores simulados: SigLIP-like (produz vectores semânticos de 256 dimensões) e VQ-like (produz códigos inteiros).
  Chinese: 拼音: 拼音: 拼音: 拼音: 拼音: 拼音: 拼音: 拼音: 拼音: 拼音: 拼音: 拼音: 拼音: 拼音: 拼音: 拼音: 拼音: 拼音: 拼音: 拼音: 拼音: 拼音: 拼音: 拼音: 拼音: 拼音: 拼音: 拼音: 拼音: 拼音: 拼音: 拼音: 拼音: 拼音: 拼音: 拼音: 拼音: 拼音: 拼音: 拼音: 拼音: 拼音: 拼音: 拼音: 拼音: 拼音: 拼音: 拼音: 拼音: 拼音: 拼音: 拼音: 拼音: 拼音: 拼音: 拼音: 拼音: 拼音: 拼音: 拼音: 拼音: 拼音: 拼音: 拼音: 拼音: 拼音: 拼音: 拼音: 拼音: 拼: 拼音: 拼: 拼: 拼: 拼: 拼: 拼: 拼: 拼: 拼: 拼: 拼: 拼: 拼: 拼: 拼: 拼: 拼: 拼: 拼: 拼: 拼: 拼: 拼: 拼: 拼: 拼: 拼: 拼: 拼: 拼: 拼: 拼: 拼: 拼: 拼: 拼:
- Um roteador de prompt que escolhe o codificador com base em uma etiqueta de tarefa.
  Tradução do inglês para Chinês:
- Um corpo compartilhado (stand-in) que processa sequências de tokens independentemente de qual codificador as tenha produzido.
  Tradução do inglês para tradução do inglês: 代代), em inglês: 代代, 代代, 代代, 代代, 代代, 代代, 代代, 代代, 代代, 代代, 代代, 代, 代, 代, 代, 代, 代, 代, 代, 代, 代, 代, 代, 代, 代, 代, 代, 代, 代, 代, 代, 代, 代, 代, 代, 代, 代, 代, 代, 代, 代, 代, 代, 代, 代, 代, 代, 代, 代, 代, 代, 代, 代, 代, 代, 代, 代, 代, 代, 代, 代, 代, 代, 代, 代, 代, 代, 代, 代, 代, 代, 代, 代, 代, 代, 代, 代, 代, 代, 代, 代, 代, 代, 代, 代, 代, 代, 代, 代, 代, 代, 代, 代, 代, 代, 代, 代, 代, 代, 代, 代, 代, 代, 代, 代, 代, 代, 代, 代, 代, 代, 代, 代, 代, 代, 代, 代, 代, 代, 代 代, 代 代 代 代 代 代 代 代 代 代 代 代 代 代 代 代 代 代 代 代 代 代 代 代 代 代 代 代 代 代 代 代 代 代 代 代 代 代 代 代 代 代 代 代 代 代 代 代 代 代 代 代 代 代 代 代 代 代 
- Uma transição da fase 1 (alinhamento) para a fase 3 (tune de instrução) do cronograma de amostra ponderada.
  Tradução do inglês para o inglês: from the first stage (→ primeira fase)

Imprimir os caminhos encaminhados para 3 exemplos: imagem QA, T2I, edição de imagem.

> Imprimir 3 exemplos de rotas de rotas: imagem, pergunta, T2I, edição de imagem,

## Envia-o .

Esta lição produz`outputs/skill-decoupled-encoder-picker.md`. Dado um produto que quer geração unificada + compreensão em qualidade de fronteira, ele escolhe Janus-Pro, JanusFlow ou InternVL-U com uma recomendação concreta de escala de dados.

> 本课产 出 `outputs/skill-decoupled-encoder-picker.md` Foram necessários dados específicos para a compreensão dos produtos, que são escolhidos entre Janus-Pro、JanusFlow ou InternVL-U, com recomendações de tamanho de dados específicas.

## Exercícios.

1. Explique por que um modelo aberto 7B pode corresponder a um modelo proprietário de fronteira em geração, mas não em compreensão.
   Tradução do inglês:Janus-Pro-7B em GenEval 上击败 DALL-E 3── explica por que 7B 开放模型能在生成上匹敌前沿专专业模型,但在理解上不能──

2. Implementar uma função de roteador: dado texto imediato, classificar como `understand`ou `generate`Como é que lidas com pedidos ambíguos como "descrever e depois esboçar"?
   Tradução do inglês:                                                                                                                                                                                                                                                            `understand`Ou `generate`Como lidar com o "descrição e depois desenho"?

3. O JanusFlow substitui o caminho VQ por fluxo rectificado. O que o corpo do transformador produz agora e quais mudanças na perda?
   Tradução do original: JanusFlow Usar o fluxo completo para substituir o VQ 路径──Transformer 主体现在输出什么?损失有什么变化?

4. Propõe uma quarta tarefa que a arquitetura Janus-Pro poderia lidar com mais um codificador descoplado.
   Tradução do inglês:                                                                                                                                                                                                                                                            

5. Leia a Seção 4.2 do Janus-Pro sobre a escalação de dados.
   Chinese Translation: read Janus-Pro 第 4.2 节关于数据扩张―― qual é a fase de dados que mais contribui para o aumento da qualidade do T2I?

## Termos-chave .

| Term | What people say | What it actually means | 中文含义 | 中文释义 |
|------|-----------------|------------------------|---------|
| Decoupled encoding | "Two visual encoders" | Separate tokenizer or encoder per direction: semantic for understanding, reconstruction for generation | 每个方向使用独立的分词器或编码器：理解用语义，生成用重建 |
| Shared body | "One transformer" | Single transformer processes either encoder's output; no modality-specific weights | 单一 Transformer 处理任一编码器的输出；无模态特定权重 |
| SigLIP for understanding | "Semantic features" | CLIP-family vision tower providing rich conceptual features but poor reconstruction | CLIP 家族视觉塔，提供丰富的概念特征但重建能力差 |
| VQ for generation | "Reconstruction codes" | Vector-quantized tokens that decode cleanly back to pixels | 可干净解码回像素的向量量化 token |
| JanusFlow | "Rectified-flow variant" | Janus-Pro with a continuous flow-matching generation head instead of VQ | 使用连续流匹配生成头替代 VQ 的 Janus-Pro |
| Routing tag | "Task tag" | Prompt marker (`<understand>` / `<generate>`) that picks the input encoder | 选择输入编码器的提示标记 |

## Mais leitura 延伸阅读

- [Wu et al. — Janus (arXiv:2410.13848)](https://arxiv.org/abs/2410.13848)
  Tradução do português:Janus 论文。
- [Chen et al. — Janus-Pro (arXiv:2501.17811)](https://arxiv.org/abs/2501.17811)
  Tradução do português:Janus-Pro
- [Ma et al. — JanusFlow (arXiv:2411.07975)](https://arxiv.org/abs/2411.07975)
  Tradução do português:JanusFlow
- [InternVL-U (arXiv:2603.09877)](https://arxiv.org/abs/2603.09877)
  Tradução do português:InternVL-U 论文。
- [Dong et al. — DreamLLM (arXiv:2309.11499)](https://arxiv.org/abs/2309.11499)
  Tradução do português:DreamLLM
