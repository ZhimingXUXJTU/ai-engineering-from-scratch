# Camelão e early-fusion tokens-only multimodal models

> Todos os VLM que vimos até agora mantêm imagens e texto separados. Os tokens visuais vêm de um codificador de visão, fluem para um projetor, e depois encontram texto dentro do LLM. O vocabulário da visão e do texto nunca se sobrepõem. O camaleão (Meta, maio de 2024) perguntou: e se fizessem? Treinar um VQ-VAE que transforma uma imagem em uma sequência de tokens discretos de um vocabulário compartilhado. Cada documento multimodal é agora uma sequência de tokens de texto e tokens de imagem intercalados, uma única perda autoregressiva. Efeito secundário: o modelo pode gerar saídas de modalidade mista  tokens alternando texto e imagem em uma única chamada de inferência. Esta lição lê a tese da fusão inicial e constrói uma versão de brinquedo de ponta a ponta.

> **【中文解读】**Chameleon (Meta, 2024: 5 de maio de 2014) propôs um método de forma mais intensa: usando VQ-VAE, transformar imagens em tokens dispersos, com tokens de texto, compartilhar com um mesmo vocabulário, usando um único treinamento de perda de auto-regressão.

> **【拓展：早期融合 vs 后期融合】**Antes de todos os VLM(LLaVA、BLIP-2、Qwen-VL) todos mantêm imagens e textos separados. O "enfoque precoce" de Camelion significa imagens e textos desde o início, em um mesmo espaço, sendo que os modelos podem naturalmente se trocar por output de textos e imagens.

**Type:** Build  | **类型:** 构建
**Languages:** Python (stdlib, VQ-VAE tokenizer + interleaved decoder) | **语言:** Python（标准库，VQ-VAE tokenizer + 交织解码器）
**Prerequisites:** Phase 12 · 05, Phase 8 (Generative AI) | **前置知识:** Phase 12 · 05，Phase 8（生成式 AI）
**Time:** ~180 minutes | **时间:** ~180 分钟

> - Não .**【前置】**O Camilo é o outro extremo do "Anti-LLaVA": todos os modelos são usados para perder o próximo token.
> - Não .**【类比】**Chameleon = "Weltseite"――LLaVA = 翻译机;;视觉编码器把图片翻译成LLM 能懂的语言);Chameleon = Welt语(图片和文本都用同一种人造语言,模型不用翻译) ・・・ Worldseite de benefação é que o modelo pode ser ininterrupto para gerar textos e imagens;坏处是每种模态必须分离化(VQ-VAE 给图片"造词"), informação perda grande。

## Objetivos de aprendizagem

- Explique por que um vocabulário compartilhado + perda única muda o que o modelo pode fazer.
  > 解释为什么共享词汇表 + 单一损失能改变模型能力──
- Descreva como um VQ-VAE tokeniza uma imagem em uma sequência discreta compatível com o próximo objetivo de tokens de um transformador.
  > 描述 VQ-VAE 如何将图像分词为与变压器 下一代标题 目标兼容的离散序列──
- Nomear os truques de treinamento-estabilidade do Chameleon: QK-Norm, colocação de abandono, LayerNorm encomenda.
  > 列举 Chameleon's training稳定性技巧:QK-Norm、Dropout 位置、LayerNorm 顺序──
- Compare a abordagem Q-Former do Chameleon vs BLIP-2 e descreva quando cada uma é a escolha certa.
  > Comparar o esquema Q-Former do Camelão com o BLIP-2, descreva o seu cenário adequado.

## O problema é o contexto do problema .

Os VLMs baseados em adaptadores (LLaVA, BLIP-2, Qwen-VL) tratam texto e imagem como duas coisas diferentes.`embed(text_token)`Uma imagem passa por lá .`visual_encoder(image) → projector → ... pseudo_tokens`O modelo tem dois caminhos de entrada que se fundem em parte.

> 适配器式 VLM(LLaVA、BLIP-2、Qwen-VL) vai ver texto e imagem como duas coisas diferentes.`embed(text_token)`- Imagens passam .`visual_encoder(image) → projector → ... pseudo_tokens`◊ Modelo tem duas rotas de entrada em meio ◊

Três consequências:

> Três consequências:

1. O LLM só pode consumir imagens, não emitir.
   Não posso gerar imagens.
2. Documentos de modalidade mista (alternação de parágrafos e imagens, como em um artigo) são estranhos  você analisa a entrada multimodal fora do modelo ou gerações de cadeia.
   Tradução em inglês: 文档 (文档) 段落和图像交替,如文章) 很别扭 你要么在模型外解析多模态输入,要么链式生成──
3. Descoincidência distributiva. Tokens visuais e tokens de texto vivem em diferentes regiões do espaço oculto, criando problemas de alinhamento sutis.
   Tradução do inglês: Distribuição não coincide.

O Camelão rejeita a premissa: as imagens são apenas sequências de tokens discretos de um vocabulário compartilhado. Treinar o modelo em documentos entrelaçados, uma perda, um decodificador autoregressivo, e você desbloqueia a geração de modalidade mista gratuitamente.

> Camelão rejeitou esta premissa: imagens são apenas uma sequência de tokens em partilha.

## O conceito central.

> **【中文解读】**Chameleon(Meta) adotou estratégia de fusão inicial: imagem e texto são dispersos em sequência de tokens unificados, usando o mesmo transformador 处理── imagem através de VQGAN 编码为离散 token,与文本 token 在同一词表中── é a máxima realização da unificação do modelo de compreensão──

> **【拓展：早期融合 vs 晚期融合】**早期融合 (Chameleon) 将多模态统一到同一代号空间,理论上优雅但训练成本高──晚期融合 (LLaVA) manter a independência do modelo visual e linguístico através de uma ligação de nível, treinando mais高效──


### VQ-VAE como tokenizer de imagem

O tokenizer é um autoencodeador variável quantizado por vetores.

> 分词器 é um vector quantificador de variações de código-fonte.

- Encoder: CNN + ViT que mapeia imagem para um mapa de recursos espaciais, digamos 32x32 recursos de dim 256.
  Tradução do inglês:编码器:CNN + ViT irá mapear imagens para características espaciais, como 32x32 个维度为 256 个特征.
- Código: um vocabulário aprendido de vetores K (Chameleon usa 8192), também dim 256.
  O termo "Chameleon" significa "o que é conhecido como "o que é conhecido como "o que é conhecido como "o que é conhecido como "o que é conhecido como "o que é conhecido como "o que é conhecido como "o que é conhecido como "o que é conhecido como "o que é conhecido como "o que é conhecido como "o que é conhecido como "o que é conhecido como "o que é conhecido como "o que é conhecido como "o que é conhecido como "o que é conhecido como "o que é conhecido como "o que é conhecido como "o que é conhecido como "o que é conhecido como "o que é conhecido como "o que é conhecido como "o que é conhecido como "o que é conhecido como "o que é conhecido como "o que é conhecido como "o que é conhecido como "o que é conhecido como " é " é conhecido como " .
- Quantização: para cada característica espacial, procure a entrada de código mais próxima por distância L2. Substitua a característica contínua pelo índice de números inteiros.
  Chinese: 量化:对每个空间特征,用 L2 距离查找最近的码本条目──用整数索引替换连续特征──
- Decodificador: CNN que leva recursos quantizados de volta para pixels.
  Tradução do inglês:CNN:CNN:CNN:CNN:CNN:CNN:CNN:CNN:CNN:CNN:CNN:CNN:CNN:CNN:CNN:CNN:CNN:CNN:CNN:CNN:CNN:CNN:CNN:CNN:CNN:CNN:CNN:CNN:CNN:CNN:CNN:CNN:CNN:CNN:CNN:CNN:CNN:CNN:CNN:CNN:CNN:CNN:CNN:CNN:CNN:CNN:CNN:CNN:CNN:CNN:CNN:CNN:CNN:CNN:CNN:CNN:CNN:CNN:CNN:CNN:CNN:CNN:CNN:CNN:CNN:CNN:CNN:CNN:CNN:CNN:CNN:CNN:CNN:CNN:CNN:CNN:CNN:CNN:CNN:CNN:CNN:CNN:CNN:CNN:CNN:CNN:CNN:CNN:CNN:CNN:CNN:CNN:CNN:CNN:CNN:CNN:CNN:CNN:CNN:CNN:CNN:CNN:CNN:CNN:CNN:CNN:CNN:CNN:CNN:CNN:CNN:CNN:CNN:CNN:CNN:CNN:CNN:CNN:CNN:CNN:CNN:CNN:CNN:CNN:CNN:CNN:CNN:CNN:CNN:CNN:CNN:CNN:CNN:CNN:CNN:CNN:CNN:CNN:CNN:CNN:CNN:CNN:CNN:CNN:CNN:CNN:CNN:CNN:CNN:CNN:CNN:CNN:CNN:CNN:CNN:CNN:CNN:CNN:CNN:CNN:CNN:CNN:CNN:CNN:CNN:CNN:CNN:CNN:

Formação: perda de reconstrução de VAE + perda de compromisso + perda de livro de códigos.

> 訓練:VAE 重建损失 + 承诺损失 + 码本损失──码本索引构成图像的离散字母表──

Para o chameleão: uma imagem torna-se 32*32 = 1024 tokens extraídos de um vocabulário de 8192. Concatenate com tokens de texto (do vocabulário BPE do LLM, digamos 32000).

> 对于Chameleon:一张图像变成32*32 = 1024 个符号, 来源: 8192 的词汇表, 来源: 8192 的词汇表, 来源: 8192 的词汇表, 来源: 8192 的词汇表, 来源: 8192 的词汇表, 来源: 8192 的词汇表, 来源: 8192 的词汇表, 来源: 8192 的词汇表, 来源: 8192 的词汇表, 来源: 8192 的词汇表, 来源: 8192 的词汇表, 来源: 8192 的词汇表, 来源: 8192 的词汇表, 来源: 8192 的词汇表, 来源: 8192 的词汇表, 来源: 8192 的词汇表, 来源: 8192 的词汇表, 来源: 8192 的词汇表, 来源: 8192 的词汇表, 来源: 8192 的词汇表, 来源: 10192 的词汇表, 来源: 10192 的词汇表, 来源: 10192 的词汇表, 来源: 10192 的词汇, 来源: 10192 的词汇, 来源: 10192 的词汇, 来源: 10192 的 词汇, 来源: 10192 的 词汇, 来源:                                                                                                                                                                                   

### O vocabulário compartilhado

O vocabulário do Chameleon combina tokens de texto, tokens de imagem e separadores de modalidade. Cada token tem um único ID. A camada de inserção de entrada mapeia cada ID para um vetor oculto D-dim. O mapa de projeção de saída oculta para logits de vocab. Softmax escolhe o próximo token, seja qual for a modalidade.

> O Chameleon's vocabulário combina o texto token、 imagem token 和模态分隔符── cada token tem um único ID── entrada embutida camada irá cada ID 映射到D 维隐藏向量── saída de projeção 映射到隐藏向量── logits.

Os separadores são importantes: `<image>`E ...`</image>`tags brackets a sequência de imagem-token. no momento de geração, se o modelo emite `<image>`O software de baixo nível sabe que os próximos 1024 tokens são índices VQ para enviar ao decodificador para render de pixels.

> É muito importante:`<image>`和 `</image>`标签包裹图像代币 序列──生成时,如果模型输出 `<image>`O software já sabe que os próximos 1024 tokens são índices VQ, precisam ser enviados para o decodificador para fazer a imagem.

### Geração de modalidade mista

A inferência é a previsão de next-token no vocabulário compartilhado.

> 推理是共享词汇表中的下一代标语 预测。示例提示:"画一只猫并描述它──"Chameleon 输出:

```
<image> 4821 1029 2891 ... (1024 image tokens) </image>
The cat is orange, sitting on a windowsill...
```

O modelo escolhe a ordem de forma autônoma. Pode produzir imagem, depois texto, texto, depois imagem ou interlease.

> O modelo pode escolher por si mesmo a ordem, pode ser primeiro a imagem, depois a imagem, depois a imagem, ou trocar por saída.

Comparar com os VLMs adaptadores onde a geração é apenas de texto.

> Comparado com o adaptador VLM (VLM) (only can generate text)

### Estabilidade de formação  QK-Norm, abandono, LayerNorm

O treinamento de fusão precoce é instável em escala.

> O estudo chameleon descreve três técnicas:

- QK-Norm. Aplicar LayerNorm para a consulta e projeções-chave dentro da atenção, antes do produto ponto. Prevenção da explosão de magnitude logit em profundidade. Usado por vários modelos grandes pós-2024.
  Chinese: 中文翻译:QK-Norm──在注意力内部的查询 和关键 投影上应用 LayerNorm,在点积之前──防止深度上的逻辑幅度爆炸──被多个2024年后的大模型使用──
- Colocação de abandono. abandono após cada adição residual, não apenas após atenção e MLP. Mais regularização necessária quando os gradientes dos tokens de imagem podem dominar.
  Em cada fase de queda, o abandono é mais do que apenas atenção e MLP.
- LayerNorm ordenamento. Pre-LN no ramo residual (padrão), mais um LN extra na conexão skip do último bloco. Estabiliza o fluxo de gradiente de camada final.
  LayerNorm 顺序──残差分支上的 Pre-LN(標準做法),加上最后一块跳跃连接上的额外LN──稳定最后一层的梯度流──

Sem estes truques, o treinamento do 34B-param Camelão divergiu em vários pontos de controle. Com eles, converge. A receita de treinamento é tanto da contribuição quanto a arquitetura.

>  sem estas habilidades, o Camaleão de 340 bilhões de parâmetros  treina em vários pontos de inspecção  dispõe de eles,  recebe                                                                                                                                                                                                                                          

### O teto de reconstrução do tokenizer

VQ-VAE é perdedor. Em 8192 entradas de código e 1024 tokens por imagem 512x512, a reconstrução PSNR limita-se em torno de 26-28 dB. Isso é suficiente para uma imagem reconhecível, mas visiblemente pior do que a difusão no espaço contínuo (Stable Diffusion 3 atinge 32+ dB).

> VQ-VAE é um problema. 8192 个码本条目和每张 512x512 图像 1024 个代币, reconstrução PSNR 顶限约26-28 dB.

O tokenizer é o gargalo. O melhor tokenizer (MAGVIT-v2, IBQ, SBER-MoVQGAN) levanta o teto.

> O sistema de expressão é um sistema de expressão mais eficaz.

### Camelão vs BLIP-2 / LLaVA

Camelão (fuso precoce, vocabulário compartilhado):
- Uma perda, um decodificador.
  Tradução do inglês:
- Gera saída de modalidade mista.
  O que é um sistema de produção?
- O tokenizer é o teto de qualidade.
  O que é que é um sistema de qualidade?
- Preço: Decodificador VQ-VAE por imagem gerada no caminho de inferência.
  Por exemplo, a imagem de um personagem é uma imagem de um personagem que é um personagem de um personagem.

BLIP-2 / LLaVA (fusão tardia, torres separadas):
- Visão, só mensagens de texto.
  Tradução do português:
- Reutiliza o Mestrado em Direito.
  Tradução do inglês para tradução inglesa:
- Não há gargalos de botelha para compreensão.
  Tradução do inglês: entender não há um instrumento de expressão.
- Barata: passes individuais para frente.
  中文翻译:便宜:单次前向传播──

Se precisarem de geração de imagens, família Chameleon, se precisarem de compreensão, o adaptador VLM é mais simples e reutiliza mais computação pré-treinada.

> 按任务选择──如果需要图像生成,选择Chameleon 系列──如果只需要理解,适配器 VLM更简单且复用更多预训计算──

### Fuyu e AnyGPT

Fuyu (Adept, 2023) é uma abordagem relacionada: pular o codificador de visão separado inteiramente, alimentar os patches de imagem crua através da projeção de entrada do LLM como se fossem tokens, sem tokenizer.

> Fuyu(Adept,2023) é uma metodologia relacionada: completamente saltando sobre o visual editor independente, vai fazer um patch de imagem original através de entrada de lançamento de LLM, assim como eles são símbolos, sem distinção de palavras.

AnyGPT (Zhan et al., 2024) estende o Chameleon a quatro modalidades: texto, imagem, fala, música.

> AnyGPT(Zhan 等人,2024) vai ampliar o Camelão para quatro modelos: texto, imagem, voz, música, todos os modelos usam o mesmo VQ-VAE 技巧, Compartilhamento Transformer, qualquer que seja.


> **【拓展：早期融合的训练挑战】**O Camelão de Meta utilizou o VQGAN de 8192 código-fonte, em ImageNet, fazendo uma balança de precisão entre a qualidade de construção (rFID 约 5.0) e a compatibilidade do texto.


## Use-o em prática.
```figure
vq-codebook
```

## Usá-lo

`code/main.py`Construirá um modelo de fusão precoce de brinquedo de ponta a ponta:

> `code/main.py`Construir um modelo de integração inicial de brinquedos de ponta a ponta:

- Um pequeno quantificador de estilo VQ-VAE que mapeia 8x8 patches para índices de código (K=16).
  Chinese:                                                                                                                                                                                                                                                              
- Um vocabulário compartilhado de (id de texto 0..31) + (id de imagem 32..47) + (separadores 48, 49).
  Tradução do português:共享词汇表(文本 id 0..31) +(图像 id 32..47) +(分隔符 48, 49)。
- Um decodificador autoregressivo de brinquedo (tabela de bigramas) treinado em legendas sintéticas + sequências de imagem-token.
  Tradução do inglês para tradução do inglês para inglês: 漢語訳: 一玩具自归归解码器 (中文译: 一玩具自归解码器), em sintet description + 图像代币序列上训练──
- Loop de amostragem que emite tokens de texto + imagem alternados dados um pedido.
  Tradução do inglês: 采样循环,给定提示后输出交换的文本 + 图像代币──

O código intencionalmente mantém o transformador pequeno (bigramas) para que você possa rastrear o fluxo de sinal de ponta a ponta.

> O Transformador é muito pequeno, para que possa seguir o sinal de volta.

## Envia-o .

Esta lição produz`outputs/skill-tokenizer-vs-adapter-picker.md`. Dada uma especificação do produto (entender apenas versus compreender + gerar, qualidade de imagem exigida, orçamento de custos), ele escolhe entre família Chameleon (fusão precoce) e família LLaVA (fusão tardia) e justifica com regras quantitativas.

> 本课产 出 `outputs/skill-tokenizer-vs-adapter-picker.md` fornecer produtos específicos (compreender + gerar  necessários qualidade de imagem  orçamento de custos), ele escolhe entre a série Chameleon                                                                                                                                                                                                                                             

## Exercícios.

1. O Chameleon usa K=8192 entradas de código e 1024 tokens por imagem 512x512. Estima a relação de compressão versus uma imagem RGB de 24 bits.
   Chameleon utiliza K=8192 个码本条目和每张 512x512 图像 1024 个代币――estimativa em relação a 24 bits RGB 图像的压缩比──有损吗?损失多少?

2. Uma imagem 4K (3840x2160) com a mesma densidade VQ-VAE produz quantos tokens de imagem? Um modelo de estilo camaleão pode gerar uma imagem 4K em uma chamada de inferência? O que rompe primeiro o contexto, a qualidade do tokenizer ou o cache KV?
   O modelo de estilo chameleão pode uma vez considerar a utilização de uma imagem 4K?

3. Implementar QK-Norm em Python puro. Dado uma consulta e chave de 64 dimensões, mostre o produto de pontos antes e depois do LayerNorm. Por que o controle de magnitude é importante na profundidade?
   Tradução do inglês para Python: Usar puro Python  implementar QK-Norm──给定 64 维的查询 和键,展示 LayerNorm 前后的点积──为什么在深度网络中幅度控制很重要?

4. Leia a Seção 2.3 do Camelão sobre estabilidade de treinamento. Descreva o modo de falha exato observado no papel no 34B sem QK-Norm. Qual foi a assinatura de "explosão normal"?
   Chinese Language Translation: read Chameleon 第 2.3 节关于训练稳定性――描述论文在340亿参数下不使用QK-Norm 观察到的确失败模式――"范数爆炸"s características são quais?

5. Extenda o decodificador de brinquedo para emitir uma resposta de modalidade mista dada uma solicitação apenas de texto. Messa com que frequência o modelo escolhe imagem em primeiro lugar versus texto em primeiro lugar dada formação - distribuição de dados 60% texto em primeiro lugar / 40% imagem em primeiro lugar.
   Tradução em chinês: expandido brinquedo des codificador, que permite que em uma determinada proposta de texto puro, emite um mixed mode de resposta.

## Termos-chave .

| Term | What people say | What it actually means | 中文含义 | 中文释义 |
|------|-----------------|------------------------|---------|
| Early fusion | "Unified tokens" | Images converted to discrete tokens sharing the transformer's vocabulary from step one | 图像从第一步就转换为与 Transformer 共享词汇表的离散 token |
| VQ-VAE | "Image tokenizer" | CNN + ViT + codebook that maps images to integer indices the transformer can predict | CNN + ViT + 码本，将图像映射为 Transformer 可预测的整数索引 |
| Shared vocabulary | "One dictionary" | A single token ID space covering text + image + modality separators | 覆盖文本 + 图像 + 模态分隔符的单一 token ID 空间 |
| QK-Norm | "Attention stabilizer" | LayerNorm applied to query and key before their dot product, prevents norm blowup | 在 query 和 key 点积前应用 LayerNorm，防止范数爆炸 |
| Mixed-modality generation | "Text + image output" | Inference that autonomously produces interleaved text and image tokens in one pass | 推理时自主产生交替的文本和图像 token |
| Codebook size | "K entries" | Number of discrete vectors the VQ-VAE can quantize to; trades compression for fidelity | VQ-VAE 可量化到的离散向量数；压缩与保真度的权衡 |
| Tokenizer ceiling | "Reconstruction limit" | Best PSNR achievable by decoding VQ tokens; bounds the model's image quality | 解码 VQ token 可达到的最佳 PSNR；限制模型的图像质量上限 |

## Mais leitura 延伸阅读

- [Chameleon Team — Chameleon: Mixed-Modal Early-Fusion Foundation Models (arXiv:2405.09818)](https://arxiv.org/abs/2405.09818)
  Chameleon 混合模态早期融合基础模型──
- [Aghajanyan et al. — CM3 (arXiv:2201.07520)](https://arxiv.org/abs/2201.07520)
  O primeiro livro de um livro de ficção científica, de um livro de ficção científica, foi publicado em 1928.
- [Yu et al. — CM3Leon (arXiv:2309.02591)](https://arxiv.org/abs/2309.02591)
  Tradução do português:CM3Leon,Chameleon's close kinsman.
- [Zhan et al. — AnyGPT (arXiv:2402.12226)](https://arxiv.org/abs/2402.12226)
  Tradução do inglês para Chinês:AnyGPT, expand expandido para quatro formas:
- [Adept — Fuyu-8B blog (adept.ai)](https://www.adept.ai/blog/fuyu-8b)
  Tradução do português:Fuyu-8B 博客,跳过视觉编码器的方案──
