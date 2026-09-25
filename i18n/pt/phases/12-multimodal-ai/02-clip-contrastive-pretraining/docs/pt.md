# CLIP e Contraste Visão-Linguagem Pré- Treinamento

> O CLIP (2021) da OpenAI provou uma única ideia grande o suficiente para alimentar os próximos cinco anos: alinhar um codificador de imagem e um codificador de texto no mesmo espaço vetorial usando apenas pares ruidosos de imagem-caption da web e uma perda contrastiva. Zero rótulos supervisionados. 400 milhões de pares. O espaço de incorporação resultante faz classificação de tiro zero, recuperação de imagem-texto e conecta-se a cada VLM de 2026 como sua torre de visão. SigLIP 2 (2025) substituiu o softmax pelo sigmoide e ultrapassou o CLIP a um custo mais baixo. Esta lição percorre as matemáticas do InfoNCE para a perda pares sigmoid e constrói o passo de treinamento em stdlib Python.

> **【中文解读】**CLIP utilizou 400 milhões de gráficos em rede, em comparação com a perda, para codificar imagens e textos no mesmo volume de espaço.

> **【拓展：CLIP→多模态大模型】**O texto do CLIP sobre comparativo de aprendizagem é a base do modelo LLaVA、BLIP-2 e outros modelos.

**Type:** Build | **类型:** 构建
**Languages:** Python (stdlib, InfoNCE + sigmoid loss implementations) | **语言:** Python（标准库，InfoNCE + sigmoid 损失实现）
**Prerequisites:** Phase 12 · 01 (ViT patches), Phase 7 (Transformers) | **前置知识:** Phase 12 · 01（ViT patch），Phase 7（Transformer）
**Time:** ~180 minutes | **时间:** ~180 分钟

> - Não .**【前置】**学本节前请先掌握:Fase 12·01(ViT Colocar imagens cortadas em parche);Fase 11·04(Embutidos 向量空间概念);Fase 7(Transformador 自注意力)。本节核心数学是软max + 交叉,Fase 7·04 有详推导──
> - Não .**【类比】**CLIP 訓練 = "中外文词典配对游戏"── dar 32k para ((imagem, descrição), deixe a modelo academia colocar cada imagem e sua própria descrição na mesma posição do espaço volumétrico, lance a descrição de outras 31999 张图片.

## Objetivos de aprendizagem

- Derivar a perda de InfoNCE a partir de informações mútuas e implementar uma versão vectorizada numericamente estável.
  Tradução do inglês para inglês: From the Internet Information Guide InfoNCE 损失,并实现数值稳定的向量化版本──
- Explique por que a perda em pares sigmoide (SigLIP) se escala para lote 32768+ sem as exigências de softmax de carga total.
  Tradução do inglês para tradução do inglês para grego: [ˈsiːgmoid 成对损失]
- Execute classificação de imagem de zero-shot construindo modelos de texto (`a photo of a {class}`) e tomar argmax em vez de similaridade cosínica.
  Tradução do inglês: 文本模板`a photo of a {class}`)并对余弦相似度取 argmax 来运行零样本 ImageNet 分类──
- Nomear as quatro alavancas que o CLIP / SigLIP pré-treino lhe dá: tamanho do lote, temperatura, modelo de solicitação, qualidade dos dados.
  O que você quer fazer é fazer um teste de qualidade de qualidade de qualidade de dados.

## O problema é o problema da introdução

A visão pré-CLIP foi supervisionada. Coletar conjuntos de dados rotulados (ImageNet: 1.2M imagens, 1000 classes), treinar uma CNN, enviá-la.

> O CLIP                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           

A web de captura de imagens tem mais de um bilhão de pares de rotulagem vagas gratuitamente. Uma foto de um retriever de ouro com texto alternativo "meu cão Max no parque" carrega um sinal de supervisão.

>  Há mais de um bilhão de imagens de marcas de marcas em rede disponíveis para uso gratuito.  Uma foto de um caça-pau-do-do-do-do-do-do-do-do-do-do-do-do-do-do-do-do-do-do-do-do-do-do-do-do-do-do-do-do-do-do-do-do-do-do-do-do-do-do-do-do-do-do-do-do-do-do-do-do-do-do-do-do-do-do-do-do-do-do-do-do-do-do-do-do-do-do-do-do-do-do-do-do-do-do-do-do-do-do-do-do-do-do-do-do-do-do-do-do-do-do-do-do-do-do-do-do-do-do-do-do-do-do-do-do-do-do-do-do-do-do-do-do-do-do-do-do-do-do-do-do-do-do-do-do-do-do-do-do-do-do-do-do-do-do-do-do-do-do-do-do-do-do-do-do-do-do-do-do-do-do-do-do-do-do-do-do-do-do-do-do-do-do-do-do-do-do-do-do-do-do-do-do-do-do-do-do-do-do-do-do-do-do-do-do-do-do-do-do-do-do-do-do-do-do-do-do-do-do-do-do-do-do-do-do-do-do-do-do-do-do-do-do-do-do-do-do-do-do-do-do-do-do-do-do-do-do-do-do-do-do-do-do-do-do-do-do-

A resposta do CLIP: trate os pares de imagens-caption como uma tarefa de correspondência. Dado um lote de imagens N e captions N, aprenda a combinar cada imagem com sua própria legenda contra distractores N-1. A supervisão é "estas duas coisas pertencem juntas; estes N-1 não".

> A resposta do CLIP: "Os dois pertencem juntos; este N-1 não pertence" foi o sinal de supervisão, pois não há etiquetas de classe, não há etiquetas artificiais, apenas perdas de comparação.

O espaço de inserção resultante faz mais do que o CLIP foi treinado para. ImageNet funciona com tiros zero porque "uma foto de um gato" se inclui perto de fotos de gatos que nunca foram expressamente rotulados gatos. Esta é a aposta que gerou cada 2026 VLM.

> 得到的嵌入空间超越了CLIP's training goal──ImageNet 零样本分类有效,因为"uma foto de um gato" é inserida até nunca foi claramente marcada para uma imagem de gato em proximidade── é o que ocasionou todas as observações de 2026 do VLM.

## O conceito central.

> **【中文解读】**CLIP(Contrastive Language-Image Pre-training) através de comparação de aprendizagem, imagens e textos serão mapeados para o mesmo volume espaço: imagens correspondentes à distância próxima, não correspondentes a sugestões. CLIP em 4 bilhões de imagens para o treinamento superior, sem necessidade de micro-modução, é possível realizar o zero-shot 图像分类, é a base da capacidade de OpenAI 多模态.

> **【拓展：CLIP 的应用生态】**O CLIP tem uma grande aplicação: DALL-E 2/3 com CLIP para gerar imagens, Diffusão estável com OpenCLIP como filtro de segurança, LLaVA com CLIP para criar um código de vídeo para conectar LLM e compreender imagens.


> **【拓展：CLIP 的 zero-shot 能力】**A capacidade mais surpreendente do CLIP é de zero-shot 分类不需要任何下游任务的训练数据,只需提供类别名称就能分类图像――在ImageNet上, CLIP ViT-L/14 零-shot 准确率(76.2%) aproxima-se da ResNet-50 完全监督准确率(76.7%)── essa capacidade provém de 4 bilhões de gráficos em comparação com o estudo.


### O duplo codificador

O CLIP tem duas torres:

> CLIP tem duas torres:

- Encoder de imagem `f`: ViT ou ResNet, produz um vetor D-dim por imagem.
  Tradução do inglês:`f`:ViT ou ResNet, cada imagem de saída de um D 维向量──
- Encoder de texto`g`: transformador pequeno, produz um vetor D-dim por subtítulo.
  Tradução do português:`g`Transformador pequeno, cada descrição

Ambas as torres normalizam suas saídas para a extensão da unidade.`cos(f(x), g(y)) = f(x)^T g(y)`já que ambas são norma-unidade.

> Os dois tours serão exportados para a unidade de longitude.`cos(f(x), g(y)) = f(x)^T g(y)`Porque ambas são unidades de volume.

> ️ **【易错点】**忘归一化 (L2) normalize) on calculação similaridade → 向量模长大的样本天然有更大的点积,模型会偏向"长向量"而不是"语义匹配"──修复:每次前进 后必`f = f / ||f||`E depois , depois ,`cos`- Não.
> 🤔 **【困惑】**P: Por que usar o restinho semelhante não usa a distância de O? A: O restinho só vê direção não vê modelagem, para "luz diferente mas o mesmo conteúdo" de imagem é um erro; a distância de O será orientada por modelagem de volumes.

Para um lote de pares N (imagem, legenda), construir a semelhança矩阵 `S`de forma`(N, N)`- Não .

> 对于一批 N 个 (图像,描述) 对, 构建形状为`(N, N)`de ressemblança`S`- Não .

```
S[i, j] = cos(f(x_i), g(y_j)) / tau
```

onde`tau`é uma temperatura aprendida (CLIP inicializa-se em 0,07; aprendida no log-space).

> Entre eles `tau`é um parâmetro de temperatura que pode ser aprendido.

### Perda de InfoNCE

O CLIP utiliza uma entropia cruzada simétrica sobre linhas e colunas:

> CLIP para o uso de dados e dados

```
loss_i2t = CE(S, labels=identity)     # each image's positive is its own caption
loss_t2i = CE(S^T, labels=identity)   # each caption's positive is its own image
loss = (loss_i2t + loss_t2i) / 2
```

Esta é a InfoNCE. A softmax em CE obriga cada imagem a corresponder à sua legenda mais do que qualquer outra legenda no lote. Os "negativos" são todos os outros itens do lote. Batches maiores = mais negativos = sinal mais forte. CLIP treinado no lote 32k; escala importa.

> É o que significa que a suavidade máxima no InfoNCE.CE é a maior correspondência de cada imagem com a sua descrição.

> ️ **【易错点】**batch_size 太小(如 64) 训不出好 CLIP负样本太少,模型学不到"什么算真正的相似"──CLIP 原文 batch_size=32768 才有效果──如果你只能跑批量=256,要么要么要么要么要么要么要么要么要么要么要么要么要么要么要么要么要么要么要么要么要么要么要么要么要么要么要么要么要么要么要么要么要么要么要么要么要么要么要么要么要么要么要么要么要么要么要么要么要么要么要么要么要么要么要么要么要么要么要么要么要么要么要么要么要么要么要么要么要么要么要么要么要么要么要么要么要么要么要么要么要么要么要么要么要么要么要么要么要么要么要么要么要么要么要么要么要么要么要么要么要么要么要么要么要么要么要么要么要么要么要么要么要么要么要么要么要么要么要么要要要要要要要要要么要么要么要要要要要要么要要么要要要要要要要要要要要要要要要要要要要要要要要要要要要要要要要要要要要要要要要要要要要要要要要要要要要要要要要要要要要要要要要要要要要要要要要要要要要要要要要要要要要要要要要要要要要要要要要要要要要要要要要要要要要要要要要要要要要要要要要要要要要要要要要要要要要要要要要要要要要要要要要要要要要要要要要要要要要要要要要要要要要要要要要要要要要要要要要要要要要要要要要要
> - Não .**【类比】**InfoNCE 像"找卧底游戏":32k 张图片对应 32k 个描述, cada imagem deve encontrar seu próprio verdadeiro suporte em um monte de descrições.

### Temperatura

`tau`O sistema de controle de temperatura é o sistema de controle de temperatura. o sistema de controle de temperatura é o sistema de controle de temperatura. o sistema de controle de temperatura é o sistema de controle de temperatura. o sistema de controle de temperatura é o sistema de controle de temperatura. o sistema de controle de temperatura é o sistema de controle de temperatura. o sistema de controle de temperatura é o sistema de controle de temperatura. o sistema de controle de temperatura é o sistema de controle de temperatura. o sistema de controle de temperatura é o sistema de controle de temperatura. o sistema de controle de temperatura é o sistema de controle de temperatura. o sistema de controle de temperatura é o sistema de controle de temperatura. o sistema de controle de temperatura é o sistema de controle de temperatura. o sistema de controle de temperatura é o sistema de controle de temperatura. o sistema de controle de temperatura é o sistema de controle de temperatura. o sistema de controle de temperatura é o sistema de controle de temperatura. o sistema de controle de temperatura é o sistema de controle de temperatura. o sistema de controle de temperatura é o sistema de controle de temperatura é o sistema de controle de temperatura. o sistema de controle de temperatura é o sistema de controle de temperatura é o sistema de controle de temperatura é o sistema de controle de temperatura ética ética é o sistema de controle de temperatura ética ética ética ética ética ética ética ética ética ética ética ética ética ética ética ética ética ética ética ética ética ética ética ética ética ética ética ética ética ética ética ética ética ética ética ética ética ética ética ética ética ética ética ética ética ética ética ética ética ética ética ética ética ética ética ética ética ética ética ética ética ética ética ética ética ética ética ética ética ética ética ética ética ética ética ética ética ética ética ética ética ética ética ética ética ética ética ética ética ética ética ética ética ética ética ética ética ética ética ética ética ética ética ética ética ética ética ética ética ética ética ética ética ética ética ética ética ética ética ética é

> `tau`控制 softmax 的度──低 tau → 尖分布,具有难负例挖掘效果──高 tau → 平滑, todos os exemplos têm contribuição──CLIP 学习 log(1/tau),并剪剪以防止崩──SigLIP 2 固定初始 tau 并使用可学习的偏置替──

### Por que a sigmoide se balança melhor (SigLIP)

Softmax precisa de toda a matriz de semelhança em sincronia. No treinamento distribuído você deve reunir todas as incorporações para cada réplica, então fazer o softmax.

> Softmax  necessita de toda a matriz de semelhança simetricidade  Em treinamento distribuído, você deve colocar cada um em todo-ajuntado para cada dupla, e então fazer softmax

SigLIP substitui softmax por sigmoide por elemento: para cada par `(i, j)`, a perda é uma classificação binária de "estes são o par de correspondência?"

> SigLIP Usando por elemento sigmoide  Substituição de softmax: para cada对 `(i, j)`, perda é para "serão eles correspondentes?"

> 🤔 **【困惑】**P: Por que o softmax  precisa de tudo reunido e o sigmoid  não precisa? A: a softmax                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                   
> - Não .**【类比】**InfoNCE = "32k 選 1 選題", deve看完整张卷子才能做; SigLIP = "32k 个判断题 (((这对配对吗?)), "每个独立答──前者需要老师收齐所有卷子,后者每个学生自己批改──

```
L = -1/N sum over (i, j) [ y_ij log sigmoid(S[i,j]) + (1-y_ij) log sigmoid(-S[i,j]) ]
```

`y_ij = 1`se`i == j`Cada GPU calcula seu bloco local e somas. SigLIP 2 escala para lotes 32k-512k a baixo custo onde CLIP precisaria de proporcionalmente mais comunicação.

> `y_ij = 1`Se `i == j`, se não for 0── per per par de perdas é independente── não precisa de todo-conjunto── cada GPU  calcula seu próprio bloco 并求和──SigLIP 2 pode expandir-se a baixo custo para 32k-512k 批次, enquanto CLIP 需要相应更多的通信──

### Classificação de tiros zero

Dados nomes de classes N, para cada classe criar um modelo de texto:

> 给定 N 个类别名称,为每个类别构建文本模板:

```
"a photo of a {class}"
```

Embed cada modelo com o codificador de texto. Embed sua imagem com o codificador de imagem. Argmax cosine similaridade = classe prevista. Nenhum treinamento sobre as classes alvo.

> Use um codificador de texto em cada modelo. Use um codificador de imagem em imagem.

> ️ **【易错点】**直接用 `"cat"`作为提示 → 比 `"a photo of a cat"`Diferença 10+ 个百分点──CLIP 训练时文本端看的描述大多是完整句子,单词作为提示会让分布偏移──修复:始终用模板 `"a photo of a {class}"`,多模板集成更好──
> 🤔 **【困惑】**P: ImageNet 1000 类全算一遍文嵌入 不是很慢吗?A: Apenas算一次然后缓存──1000 个提示 在文本编码器里跑一遍(毫秒级),后面每张新图片只需要1次图像嵌入+1000 次余弦相似度(向量化矩阵乘)──

Templates de imediato importam. O papel original do CLIP usava 80 modelos por classe (planos, artísticos, fotos, pinturas, etc.) e mediou os embutidos. +3 pontos ImageNet. O uso moderno normalmente escolhe um ou dois modelos.

> 提示模板很重要──CLIP 原始文每类使用80模板(普通、艺术、照片、绘画等)并对嵌入取平均──ImageNet 上提升3个百分点──现代用法通常选择一个两个模板──

### Análises lineares e ajustes finos

A sonda linear (treinar uma camada linear em cima de recursos CLIP congelados para suas classes alvo) supera a sonda linear em tarefas no domínio.

> 零样本是基线――线性探测;;在结的 CLIP特征之上为目标类训练一线性层) em tarefas dentro do domínio 超越零样本――全量微调在域内超越线性探测,但可能损害零样本迁移――三种模式,三种权衡――

### SigLIP 2: NaFlex e características densas

A SigLIP 2 (2025) acrescenta:

> SigLIP 2(2025)

- NaFlex: um modelo único lida com proporções de aspecto e resoluções variáveis.
  NaFlex: simples modelo de tratamento de variação de largura e resolução.
- Melhores características densas para a segmentação e a estimativa da profundidade, com foco na utilização como espinha dorsal congelada em VLMs.
  O objetivo é a divisão e a profundidade da rede como um conjunto de elementos de VLM.
- Multilíngue: formado em mais de 100 línguas, onde o CLIP era apenas em inglês.
  No entanto, o CLIP é apenas limitado ao inglês.
- 1B escala paramétrica onde o CLIP alcançou o topo em 400M.
  Chinese: 10 mil milhões de parâmetros, enquanto o CLIP máximo é de 4 mil milhões.

Em 2026 VLMs abertos, SigLIP 2 SO400m/14 é a torre de visão padrão. CLIP continua a ser o padrão para recuperação de texto de imagem pura, onde a distribuição de treinamento específica LAION-2B corresponde ao padrão de consulta.

> Em 2026 em aberto VLM, SigLIP 2 SO400m/14 é a torre de visão padrão.

### A Comissão deve apresentar ao Parlamento Europeu e ao Conselho um relatório sobre a aplicação do artigo 108.o, n.o 1, do Regulamento (CE) n.o 1069/2009 do Parlamento Europeu e do Conselho.

ALIGN (Google, 2021): a mesma ideia que CLIP, escala de pares 1,8B, 90% barulhento. Escalas de dados barulhentos comprovadas. OpenCLIP (LAION): reprodução aberta de CLIP no LAION-400M / 2B, escalas múltiplas, o ponto de verificação de entrada para abertura. EVA-CLIP: inicializa a partir de modelagem de imagem mascarada; forte espinha dorsal para VLMs. Básico: híbrido CLIP+ALIGN do Google. Todas as mesmas famílias, dados diferentes e sintonização.

> ALIGN(Google,2021): ideia semelhante à CLIP, 18 mil milhões em escala, 90% de dados de ruído.

### O teto de tiro zero

Os modelos CLIP-class cobrem cerca de 76% ImageNet zero-shot (CLIP-G, OpenCLIP-G). Além disso, requer dados muito maiores (SigLIP 2 obtém 80% +) ou mudanças de arquitetura (cabeças supervisionadas, mais parâmetros).

> O limite máximo de CLIP 类模型 em ImageNet 零样本分类 é de cerca de 76% (CCLIP-G、OpenCLIP-G) ◦ Mais do que esse nível precisa de dados maiores (CCLIP 2 sigLIP 2 达到 80%+) ou estrutura mudar (监督头、更多参数) ◦

> 🤔 **【困惑】**O que é que o CLIP não consegue fazer? O CLIP só aprendeu a fazer "qualquer tipo de correspondência", não aprendeu a fazer "qualquer tipo de correspondência", é o que é o trabalho do VLM.

## Use-o com o framework implementado.
```figure
multimodal-fusion
```

## Usá-lo

`code/main.py`Implementos:

> `code/main.py`实现:

1. Um duplo codificador de brinquedo (funções de imagem baseadas em hash, funções de gráfico de texto) para que você possa ver a forma InfoNCE sem numpy.
   Tradução do inglês para o inglês: a······································································································································································································································································································································································································································································································
2. Perda de InfoNCE em Python puro (estabilidade numérica através de log-sum-exp).
   Tradução do inglês para o português: pur Python 实现的 InfoNCE 损失(通过 log-sum-exp 实现数值稳定性) ⋅
3. Perda em pares Sigmoide para comparação.
   Tradução do português: Sigmoide 成对损失用于对比.
4. Uma rotina de classificação de tiro zero: computa a semelhança cosínica contra um conjunto de instruções de texto, argmax para previsão.
   O que é o que significa que o sistema de cálculo é um sistema de cálculo?

Os números absolutos são brinquedos, a forma corresponde ao que um treinador real emite.

> 运行它并观察损失曲线──绝对数值是玩具级的;但形状与真实CLIP 训练机的输出匹配──

## Envia-o . Produto .

Esta lição produz`outputs/skill-clip-zero-shot.md`. Tendo em conta um conjunto de imagens (via caminho) e uma lista de classes-alvo, ele cria instruções de texto com o modelo CLIP, incorpora ambos os lados com um ponto de controlo indicado (por exemplo, `openai/clip-vit-large-patch14`A habilidade recusa-se a fazer alegações sobre classes não na lista de solicitações.

> 本课产 出 `outputs/skill-clip-zero-shot.md` dado um grupo de imagens (passagem) e um grupo de objetivos (categoria), ele usa o CLIP 模板 para construir texto, usando pontos de verificação definidos (exemplo:`openai/clip-vit-large-patch14`) embutidos em ambos os lados, e retornar com o número de semelhanças entre os principais 1 / 5 预测──

## Exercícios.

1. Implementar InfoNCE para um lote de 4 pares à mão. Construa a matriz de semelhança 4x4, execute softmax, escolha a diagonal, computa entropia cruzada. Verifique sua implementação Python contra este cálculo manual.
   Tradução do inglês para inglês: manualmente implementado 4 para o modelo de InfoNCE.

2. O SigLIP utiliza um parâmetro de preconceito `b`Além da temperatura: `S'[i,j] = S[i,j]/tau + b`- Que papel faz ?`b`A série de jogo é executada quando o lote apresenta um grande desequilíbrio de classes (muitos mais negativos do que positivos por fila)?
   Chinese: SigLIP , além de temperatura também utiliza parâmetros de colocação`b`- Não .`S'[i,j] = S[i,j]/tau + b`◊ Quando existem grandes categorias de desequilíbrio (per dia)`b`O que é que acontece?

3. Construir um classificador de tiros zero para gatos versus cães. Tente dois modelos rápidos: `a photo of a {class}`E ...`a picture of a {class}`- Medir a precisão em 100 imagens de teste.
   Tradução do inglês para inglês: construir gato gato零样本分类器──尝试两种提示模板:`a photo of a {class}`和 `a picture of a {class}`◊ Precision rate de medição em 100 张试图图片──模板集成是否优于单模板?

4. Calcule o custo de comunicação de softmax InfoNCE vs sigmoid em pares para uma corrida de 512 GPU no lote 32k. Que escalas como O(N), que como O(N^2)? Cite Secção SigLIP 4.
   Chinese Translation:计算 512 GPU、批次 32k 下 softmax InfoNCE 与 sigmoid 成对损失的通信成本──哪个是 O(N),哪个是 O(N^2)?引用 SigLIP 第 4 节──

5. Leia o artigo sobre as leis de escalagem do OpenCLIP (arXiv:2212.07143, Cherti et al.). Reproduzir a sua conclusão para a escalagem de dados a partir dos números: em tamanho fixo do modelo, qual é a relação log-linear entre a precisão de imagem de imagem de imagem de imagem de imagem zero e o tamanho dos dados de treinamento?
   Chinese Translation: read OpenCLIP 缩放定律论文(arXiv:2212.07143,Cherti 等人) ⋅ De um gráfico, eles concluíram sobre a expansão de dados:

## Termos-chave .

| Term | What people say | What it actually means | 中文释义 |
|------|----------------|------------------------|---------|
| 术语 | 通俗说法 | 实际含义 | |
| InfoNCE | "Contrastive loss" | Cross-entropy over a batch's similarity matrix; each item's positive is its paired item, negatives are everything else | 批次相似度矩阵上的交叉熵；每项的正样本是其配对项，负样本是所有其他项 |
| Sigmoid loss | "SigLIP loss" | Per-pair binary cross-entropy; no softmax, no all-gather, scales cheaply in distributed training | 逐对二分类交叉熵；无 softmax，无 all-gather，分布式训练中扩展成本低 |
| Temperature | "tau" | Scalar that scales logits before softmax/sigmoid; controls sharpness of the distribution | softmax/sigmoid 前缩放 logits 的标量；控制分布的锐度 |
| Zero-shot | "no-finetune classification" | Use text prompts to construct class embeddings and classify by cosine similarity; no training on target classes | 用文本提示构建类别嵌入，通过余弦相似度分类；无需在目标类别上训练 |
| Prompt template | "a photo of a ..." | Text scaffold around a class name; affects zero-shot accuracy by 1-5 points | 类别名周围的文本支架；影响零样本准确率 1-5 个百分点 |
| Dual encoder | "Two-tower" | One image encoder + one text encoder, outputs in shared D-dim space | 一个图像编码器 + 一个文本编码器，输出在共享的 D 维空间 |
| Hard negative | "Tough distractor" | A negative similar enough to the positive that the model has to work to separate them | 与正样本足够相似的负样本，模型需要努力区分它们 |
| Linear probe | "Frozen + one layer" | Train only a linear classifier on top of frozen features; measures feature quality | 仅在冻结特征之上训练线性分类器；衡量特征质量 |
| NaFlex | "Native flexible resolution" | SigLIP 2 capability to ingest images at any aspect ratio and resolution without resizing | SigLIP 2 以任意宽高比和分辨率输入图像的能力，无需调整大小 |
| Temperature scaling | "log-parametrized tau" | CLIP parametrizes `log(1/tau)` so gradients behave; clips to prevent collapse to near-zero tau | CLIP 参数化 `log(1/tau)` 使梯度行为正常；裁剪防止 tau 崩溃到接近零 |

## Mais leitura 延伸阅读

- [Radford et al. — Learning Transferable Visual Models From Natural Language Supervision (arXiv:2103.00020)](https://arxiv.org/abs/2103.00020)- O documento CLIP.
  Tradução do português:CLIP 论文。
- [Zhai et al. — Sigmoid Loss for Language Image Pre-Training (arXiv:2303.15343)](https://arxiv.org/abs/2303.15343) SigLIP.
  Tradução do português:SigLIP 论文。
- [Tschannen et al. — SigLIP 2 (arXiv:2502.14786)](https://arxiv.org/abs/2502.14786) multilíngue + NaFlex.
  中文翻译:多语言 + NaFlex。
- [Jia et al. — ALIGN (arXiv:2102.05918)](https://arxiv.org/abs/2102.05918) Escala com dados da web barulhentos.
  Tradução do inglês: using noise network data expand.
- [Cherti et al. — Reproducible scaling laws for contrastive language-image learning (arXiv:2212.07143)](https://arxiv.org/abs/2212.07143) Leis de escalação OpenCLIP.
  O que é que é o "conjunto de um país"?
