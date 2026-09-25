# Transformadores de visão e o primitivo de patch-tokens

> Antes de qualquer coisa multimodal, uma imagem tem de se tornar uma sequência de tokens que um transformador pode comer. O documento ViT de 2020 respondeu a isso com parches de 16x16 pixels, uma projeção linear e uma inserção de posição. Cinco anos depois, cada modelo de fronteira de 2026 (Claude Opus 4.7 em 2576px nativo, Gemini 3.1 Pro, Qwen3.5-Omni) ainda começa desta forma  o codificador mudou de ViT para DINOv2 para SigLIP 2, foram adicionados tokens de registro, o esquema posicional tornou-se 2D-RoPE, mas o primitivo manteve. Esta lição lê o pipeline de patch-tokens de ponta a ponta e constrói-o em stdlib Python para que o resto da Fase 12 tenha um modelo mental concreto para "tokens visuais".

> **【中文解读】**Antes de entrar em multimodus, a imagem deve primeiro se tornar em um sequência de tokens transformador capaz de processar. ViT utilizou blocos de imagem 16x16 + projeção linear + código de posição para realizar essa transformação, que ainda é a base de todos os modelos de vanguarda.

> **【拓展：ViT Patch→多模态基础】**Patch-Token é a base de todos os modelos de linguagem visual, quer seja o visual editor do CLIP, quer o modelo de entrada de imagens do LLaVA ou o modelo de compreensão de documentos, tudo a partir do Patch 切分开始──

> - Não .**【前置】**O primeiro é o primeiro: 1) Fase 7·01-05 (Transformer 基础)  Comprender Auto-Attenção、Posição Embedding; 2) Fase 4·03 (CNNs)  Comprender卷积特征提取,对比 ViT 的补丁方法; 3) Fase 10·01 (Tokenizers)  Comprender文本代币,本节是其视觉对应; 4) Numpy 矩阵运算──本节是 Fase 12 全部 25 节的基础,跳过会看不懂后续──

**Type:** Learn | **类型:** 学习
**Languages:** Python (stdlib, patch tokenizer + geometry calculator) | **语言:** Python（标准库，patch tokenizer + 几何计算器）
**Prerequisites:** Phase 7 (Transformers), Phase 4 (Computer Vision) | **前置知识:** Phase 7（Transformer），Phase 4（计算机视觉）
**Time:** ~120 minutes | **时间:** ~120 分钟

## Objetivos de aprendizagem

- Converte uma imagem HxWx3 em uma sequência de tokens de correção com codificação posicional correta.
  中文翻译:将 HxWx3 图像转换为带有正确位置编码的补丁代币序列──
- Calcule o comprimento da sequência, a contagem de parâmetros e os FLOPs para um ViT de um dado ( tamanho do parche, resolução, escuridão oculta, profundidade).
  Chinese: 計算给定 ([[patch]] ]] ]] ]] ]] ]] ]] ]] ]] ]] ]] ]] ]] ]] ]] ]] ]] ]] ]] ]] ]] ]] ]] ]] ]] ]] ]] ]] ]] ]] ]] ]] ]] ]] ]] ]] ]] ]] ]] ]] ]] ]] ]] ]] ]] ]] ]] ]] ]] ]] ]] ]] ]] ]] ]] ]] ]] ]] ]] ]] ]] ]] ]] ]] ]] ]] ]] ]] ]] ]] ]] ]] ]] ]] ]] ]] ]] ]] ]] ]] ]] ]]
- Cite as três atualizações que levaram a ViT da pesquisa de 2020 para a produção de 2026: pré-treinamento auto-supervisionado (DINO / MAE), tokens de registro e embalagem de resolução nativa.
  Chinese Translation:列举将 ViT From 2020研究推向 2026 年生产环境的三大升级:自监督预训练(DINO / MAE) 、register token 和原生分辨率打包──
- Escolha entre o CLS pooling, o pooling médio e o registro de tokens para uma tarefa a jusante.
  中文翻译:为下游任务选择 CLS 池化、平均值池化或注册代币──

## O problema é o problema da introdução

Os transformadores operam em sequências de vetores. O texto já é uma sequência (bytes ou tokens). Uma imagem é uma grade 2D de pixels com três canais de cores  não uma sequência. Se você achar cada pixel, uma imagem RGB 224x224 se torna 150.528 tokens, e a auto-atenção naquele comprimento é um não-starter (quadrático no comprimento da sequência).

> O transformador  opera é a sequência de velocidades. O texto em si é a sequência. Mas a imagem é uma imagem de três cores que atravessa o caminho de imagens em 2D. Se você expor em plano cada imagem, uma imagem RGB de 224x224 se torna 150.528 token, enquanto a auto-attenção nessa longitude é impossível.

As abordagens pré-2020 viraram um extractor de recursos da CNN para a frente: a ResNet produz um mapa de recursos 7x7 de vetores de 2048 dimensões, alimenta esses 49 tokens para um transformador.

> O método anterior a 2020 foi o seguinte: ResNet produz um gráfico de características de dimensão 2048 de 7x7 de um modelo de divisão de divisão de divisão, que vai dar os 49 tokens ao Transformer.

Dosovitskiy et al. (2020) fez a pergunta contundente: e se saltarmos a CNN? Divida a imagem em parches de tamanho fixo (digamos 16x16 pixels), projetar linearmente cada parche em um vetor, adicionar um inserimento posicional e alimentar a sequência para um transformador de vainilha. Na época, esta era uma visão herésica sem convulsões. Com dados suficientes (JFT-300M, então LAION) ele venceu a ResNet na ImageNet e continuou a melhorar.

> Dosovitskiy  et al. (2020) propôs uma questão direta: se saltarmos a CNN, a imagem será dividida em parches de tamanho fixo (por exemplo, 16x16), projetando linearmente cada parche para um veículo, adicionando o código de localização, e então entregando a sequência ao Transformer padrão.

Em 2026, o ViT primitivo é o fundamento incontestável. Cada torre de visão de VLM de peso aberto é algum descendente (DINOv2, SigLIP 2, CLIP, EVA, InternViT). A questão não é mais "deveríamos usar patches?" mas "que tamanho de patch, qual cronograma de resolução, qual objetivo de pré-treino, qual codificação posicional".

> Até 2026, o ViT original já se tornou indiscutível base. Cada torre de visão de VLM com peso aberto é de sua geração seguinte. A questão não é mais "dever ou não usar um patch?" mas "o que patch é grande?

## O conceito central.

> **【中文解读】**O Transformador de Visão (ViT) dividirá o imagem em um parche fixo de grande porte, como 16x16 , cada parche 展平后通过线性投影变成一个代币,然后像NLP中的Transformer一样处理── é o que introduzirá a estrutura do Transformer no pioneiro da visão do computador, substituindo a CNN 成为视觉的脊柱──

> **【拓展：ViT 的影响】**Dosovitskiy  et al. Propôs em 2020 ViT prova transformador em imagem em classificação pode superar CNN;. ViT-L/14 em ImageNet alcançar 88.5% top-1  precision rate;. ViT é a base de vídeo codificador do modelo CLIP、GPT-4V、Gemini etc.


> **【拓展：ViT 对 CNN 的优势】**A integração da ViT em sua auto-atenção em quantidade de dados é suficientemente grande quando (como JFT-300M ou LAION-5B) é significativamente melhor do que a sensação local da CNN.


### Patches como tokens

Dado uma imagem `x`de forma`(H, W, 3)`e um tamanho de parche `P`, você esculpir a imagem em uma grade de`(H/P) x (W/P)`- não se sobrepõem.`P x P x 3`Cubo de pixels. Aplanar cada cubo para um `3 P^2`Aplicar uma projeção linear compartilhada `W_E`de forma`(3 P^2, D)`para mapear cada parche na dimensão oculta do modelo `D`- Não .

> 给定形为 `(H, W, 3)`De imagens`x`和 patch , grande`P`, vai cortar imagem para`(H/P) x (W/P)`个不重叠的补丁 网格── cada um é um `P x P x 3`de imagem quadrada.`3 P^2`维向量── aplicação forma为 `(3 P^2, D)`                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             `W_E`, vai cada parche  mapear para a dimensão oculta do modelo `D`- Não.

Para a configuração canónica ViT-B/16:
- Resolução 224, tamanho do parche 16 → rede 14x14 → 196 tokens do parche.
  中文翻译:分辨率 224, patch 大小 16 → 网格 14x14 → 196 个补丁代币──
- Cada parche é`16 x 16 x 3 = 768`Valores de pixels, projetados para `D = 768`- Não .
  中文翻译: cada parche 包含 `16 x 16 x 3 = 768`个像素值, projeção até `D = 768`- Não.
- Adicionar um aprendizagem `[CLS]`token → sequência de longo 197.
  Tradução do inglês: 添加一个可学习的`[CLS]`token → 序列长度 197。

A projeção de correio é matematicamente idêntica a uma convolução 2D com tamanho do núcleo `P`, passo `P`, e `D`É assim que o código de produção realmente o implementa.`nn.Conv2d(3, D, kernel_size=P, stride=P)`O enquadramento da "projeção linear" é conceitual; o enquadramento do núcleo é eficiente.

> Patch  projeção em matemática é igual ao núcleo`P`、步长为 `P`、Exportação e Transporte`D`O código de produção é assim realizado.`nn.Conv2d(3, D, kernel_size=P, stride=P)`"Línea projeção" é conceitual; a implementação do volume nuclear é altamente eficaz

### Embedings de posição

Os parches não têm ordem inerente  o transformador os vê como um saco. Os primeiros ViTs adicionaram um inserimento posicional 1D aprendizagem (um vetor de 768-dim por posição, 197 deles). Funciona, mas liga o modelo à resolução de treinamento: na inferência você tem que interpolar a tabela de posição se você mudar a grade.

> Patch  não tem ordem fixa Transformer os considera como um conjunto de ordens.

Os espinhos de visão modernos usam 2D-RoPE (M-RoPE do Qwen2-VL, padrão do SigLIP 2) ou posições 2D factorizadas. 2D-RoPE gira a consulta e vetores-chave com base no índice do parche (fila, coluna), de modo que o modelo infere a posição 2D relativa do ângulo de rotação.

> O modelo pode ser processado de forma arbitrária em tamanho de rede.

### Tokens CLS, saída conjunta e tokens de registro

O que é a representação no nível da imagem?

> O que é um gráfico?

1. `[CLS]`token. Prepare um vetor apropriado para a sequência de correção. Depois de todos os blocos transformadores, o estado oculto do token CLS é a representação da imagem. Herda do BERT. usado pelo ViT original, CLIP.
   Tradução:`[CLS]`token──在补丁序列前拼接一个可学习向量──所有变压器块之后,CLS token's hidden state is the image representation──继承自BERT──原始 ViT 和 CLIP 使用──
2. Uma média de estados ocultos dos tokens dos patches, usada pela SigLIP, DINOv2, a maioria dos VLMs modernos.
   中文翻译:均值池化──对所有补丁代币的输出隐藏状态取平均──SigLIP、DINOv2 和大多数现代VLM使用──
3. Os dados de registro são de acordo com o estudo de Darcet e outros (2023) que os vídeos treinados sem um token de lavagem explícito desenvolvem patches de "artifatos" de alta norma que sequestram a auto-atenção.
   O sistema de registro pode ser usado para fazer o registro de dados, mas não pode ser usado para fazer o registro de dados.

A escolha importa para tarefas a jusante. CLS é bom para classificação. Para VLMs que alimentam tokens de patch em um LLM, você evita a agregação inteira  cada patch se torna um token de entrada do LLM. Os registros são descartados antes da entrega (eles são andares, não conteúdo).

> 选择对下游任务很重要──CLS 适合分类──对于将补丁代币进入 LLM的VLM,完全跳过池化每个补丁都成为LLM的输入代币──Register在交接前被丢弃(它们是脚手架,不是内容)──

### Pre-treinamento: supervisionado, contrastivo, mascarado, auto-destilado

O ViT 2020 foi pré-treinado com classificação supervisionada no JFT-300M. Substituído rapidamente por:

> O ViT de 2020 em JFT-300M 上用监督分类进行预训――很快被以下方法取代:

- CLIP (2021): texto de imagem contrastante em pares 400M. Lição 12.02.
  O estudo foi realizado em uma área de estudos de ciências da informação.
- MAE (2021, He et al.): mascar 75% dos patches, reconstruir pixels. Auto-supervisionado, trabalha em imagens puras.
  中文翻译:MAE(2021,He 等人): cobrir 75% do parche, re-construir imagem, auto-supervisionar, aplicado a imagem pura,
- DINO (2021) / DINOv2 (2023): auto-distilação com aluno-professor, sem rótulos, sem legendas. O 2023 DINOv2 ViT-g/14 é a espinha dorsal puramente visual mais forte e o padrão para casos de uso de "características densas".
  O DINOV2 ViT-g/14 é a rede mais forte de pure-visão principal, também é um "trato intenso" de uso de casos de preferência.
- SigLIP / SigLIP 2 (2023, 2025): CLIP com perda sigmoide e NaFlex para relação de aspecto nativa. A torre de visão dominante em 2026 VLMs abertos (Qwen, Idefics2, LLaVA-OneVision).
  中文翻译:SigLIP / SigLIP 2(2023,2025): usar sigmoid 损失和 NaFlex 原生宽高比的 CLIP──2026年开放 VLM(Qwen、Idefics2、LLaVA-OneVision) 主导视觉塔──

A escolha de um pré-treino determina para que a coluna vertebral é boa: CLIP/SigLIP para a correspondência semântica com o texto, DINOv2 para características visuais densas, MAE como ponto de partida para a sintonização de fundo.

> 预训练方式决定主干网络擅长什么:CLIP/SigLIP Used for syntax matching of text,DINOv2 Used for dense visual features,MAE 作为下游微调的起点──

### Leis de escalagem

A escalação ViT (Zhai et al. 2022) estabeleceu que a qualidade de uma ViT obedece a leis previsíveis no tamanho do modelo, tamanho dos dados e computação.

> ViT 缩放定律(Zhai 等人,2022) estabeleceu a qualidade de ViT seguindo sobre modelos de grandeza, dados de grandeza e quantidade de cálculo.

- Um modelo maior + mais dados → melhor qualidade.
  Tradução do inglês: 更多数据 → 更好的质量──
- O tamanho do patch é uma alavanca no comprimento da sequência versus fidelidade. Patch 14 (típico para DINOv2/SigLIP SO400m) dá mais tokens por imagem do que patch 16; melhor para OCR e tarefas densas, pior para velocidade.
  Patch 大小是序列长度与保真度之间的杆──Patch 14(DINOv2/SigLIP SO400m 的典型配置) Em comparação com o patch 16, cada imagem produz mais tokens; mais adequado para OCR e tarefas densas, mas a velocidade é mais lenta──
- A resolução é a outra grande alavanca. Passar de 224 para 384 para 512 quase sempre ajuda, a um custo quadrático em FLOPs.
  O nível de resolução é outro importante. A partir de 224 升升到384 再到512 几乎总是有助, mas FLOPs 成本呈二次增长──

ViT-g/14 (1B params, patch 14, resolução 224 → 256 tokens) e SigLIP SO400m/14 (400M params, patch 14) são os dois codificadores de cavalo de trabalho para 2026 VLMs abertos.

> ViT-g/14(10 mil milhões de parâmetros, parâmetro 14, resolução 224 → 256 tokens) e SigLIP SO400m/14(4 mil milhões de parâmetros, parâmetro 14) são os dois principais codificadores de VLM em 2026:

### Contagem de parâmetros para um ViT

O cálculo completo está em`code/main.py`Para ViT-B/16 em 224:

> 完整计算见 `code/main.py`❖ Para ViT-B/16 em 224 resolução:

```
patch_embed = 3 * 16 * 16 * 768 + 768  =  591k
cls + pos    = 768 + 197 * 768          =  152k
block        = 4 * 768^2 (QKVO) + 2 * 4 * 768^2 (MLP) + 2 * 2*768 (LN)
             = 12 * 768^2 + 3k          =  7.1M
12 blocks    = 85M
final LN    = 1.5k
total       ≈ 86M
```

Estabeleça cada ViT desta forma antes de carregar o ponto de controlo.

> Antes do ponto de verificação de carga, com este método, a estimativa de cada ViT.

### Configuração de produção 2026

O codificador mais aberto que os VLMs enviam em 2026 é SigLIP 2 SO400m/14 em resolução nativa (NaFlex).

> A maioria dos editores de VLM em 2026 são originais de resolução (NaFlex) SigLIP 2 SO400m/14──.

- Parâmetros de 400M.
  Tradução do inglês:
- Tamanho do parche 14, resolução padrão 384 → 729 tokens de parche por imagem.
  Patch 大小 14,默认分辨率 384 → 每张图像 729 个补丁代币──
- Pool médio para tarefas de nível de imagem; todos os 729 patches fluem para o LLM para VQA.
  Tradução do inglês para tradução do inglês para inglês: image class task usage average value池化; all 729 个补丁 流入 LLM 进行视觉问答。
- 4 fichas de registro, descartadas antes da entrega do LLM.
  Tradução do inglês:
- 2D-RoPE com escalação de nível de imagem para a relação de aspecto nativa.
  Tradução do inglês: 2D-RoPE, com imagem de escala reduzida para apoiar o tamanho original.

Cada decisão nesse config remonta a um jornal que você pode ler.

> Cada decisão da configuração pode ser traçada ao artigo que pode ler.

## Use-o com o framework implementado.
```figure
image-patch-tokens
```

## Usá-lo

`code/main.py`é um tokenizer de parche e calculadora de geometria.

> `code/main.py`é um tokenizer de parche 和几何计算器──它接收(图像 H, W, parche P, 隐藏维度 D, 深度 L)并报告:

- Forma da grade e comprimento da sequência após a fixação.
  Tradução do inglês:Patch 切分后的网格形和序列长度──
- Seqüência de tokens para uma imagem de brinquedo sintética de 8x8 pixels (caminhar pela trajetória plano + projeto).
  Chinese Translation: sintetizado 8x8 像素玩具图像的符号序列 (图像) 序列 (图像) 序列 (图像) 序列 (图像) 序列 (图像) 序列 (图像) 序列 (图像) 序列 (图像) 序列 (图像) 序列 (图像) 序列 (图像) 序列 (图像) 序列 (图像) 序列 (图像) 序列 (图像) 序列 (图像) 序列 (图像) 序列 (图像) 序列 (图像) 序列) 序列 (图像) 序列 (图像) 序列) 序列 (图像) 序列) 序列 (图像) 序列) 序列 (图像) 序列) 序列 (图像) 序列) 序列) 序列 (图) 序列) 序列) 序列 (图) 序列) 序列) 序列 (图) 序列)
- Contagem de parâmetros dividida por inserção de parche, inserção de posição, blocos de transformador e cabeça.
  Tradução do inglês para tradução do inglês: 嵌入,位置编码, Transformer 块和头分解的参数.
- FLOPs por passagem avançada na resolução-alvo.
  Tradução do inglês para o inglês:
- Uma tabela de comparação em ViT-B/16 @ 224, ViT-L/14 @ 336, DINOv2 ViT-g/14 @ 224, SigLIP SO400m/14 @ 384.
  中文翻译:ViT-B/16 @ 224、ViT-L/14 @ 336、DINOv2 ViT-g/14 @ 224、SigLIP SO400m/14 @ 384 的对比表──

Aplique o número de parâmetros com os números publicados, use o tamanho e a resolução do parche para sentir o custo da contagem de tokens.

> 运行它――将参数与发布数据对比――调整补丁大小和分辨率来感受代币数量成本――

## Envia-o . Produto .

Esta lição produz`outputs/skill-patch-geometry-reader.md`. Dada uma configuração ViT ( tamanho do parche, resolução, escuridão oculta, profundidade), produz uma contagem de tokens, contagem de parâmetros e estimativa VRAM com justificativas.

> 本课产 出 `outputs/skill-patch-geometry-reader.md` Fornecer uma configuração de ViT  patch                                                                                                                                                                                                                                                        

## Exercícios.

1. Calcule o comprimento da sequência de patch-token para Qwen2.5-VL na entrada nativa 1280x720 com tamanho do patch 14. Como isso se compara a uma representação apenas CLS?
   Qual a diferença entre Qwen2.5VL em original 1280x720 输入、patch 大小 14 下的补丁符号序列长度──和仅使用 CLS 的表示相比?

2. Um quadro 1080p (1920x1080) no patch 14 produz quantos tokens? A 30 FPS em um vídeo de 5 minutos, quantos tokens visuais totais? Qual é o custo mais economizado: pooling, amostragem de quadro ou fusão de tokens?
   Chinese Language Translation: 一 1080p 图像(1920x1080) Em patch 14 下 produzir quantas parâmetros? em 30 FPS 播放 5 分钟视频,总共多少视觉 token?

3. Implementar o pooling médio sobre tokens de patch em Python puro. Verifique se o pool médio sobre 196 tokens de uma saída DINOv2 corresponde ao modelo `forward`Retorna quando pedem uma incorporação em conjunto.
   Tradução do inglês para Python: Usar Python para implementar o padrão de patch token 验证对 DINOv2 输出196 token 做平均值池化是否与模型 `forward`                                                                                                                                                                                                                                                              

4. Leia a Seção 3 do livro "Os Transformadores de Visão precisam de Registros" (arXiv:2309.16588). Descreva em duas frases o que os registros absorvem e por que é importante para a previsão densa a jusante.
   中文翻译:阅读"Vision Transformers Need Registers" (ArXiv:2309.16588) 节──第 3 节──用两句描述登记 吸收了什么伪影,以及为什么对下游密集预测很重要──

5. Modificar`code/main.py`Para suportar o patch-n'-pack: dada uma lista de imagens de diferentes resoluções, produzir uma única sequência de embalagens e a máscara de atenção de diagonal de blocos.
   Tradução do português:`code/main.py`Em apoio a patch-n'-pack: dado um conjunto de imagens de diferentes resoluções, gerar uma série de pacotes e blocos em relação ao ângulo de atenção escondido.

## Termos-chave .

| Term | What people say | What it actually means | 中文释义 |
|------|----------------|------------------------|---------|
| 术语 | 通俗说法 | 实际含义 | |
| Patch | "16x16 pixel square" | A fixed-size non-overlapping region of the input image; becomes one token | 固定大小的非重叠图像区域；成为一个 token |
| Patch embedding | "Linear projection" | A shared learned matrix (or Conv2d with stride=P) mapping flattened patch pixels to D-dim vectors | 共享的学习矩阵（或步长为 P 的 Conv2d），将展平的 patch 像素映射为 D 维向量 |
| CLS token | "Class token" | Prepended learnable vector whose final hidden state represents the whole image; optional in 2026 | 前置可学习向量，其最终隐藏状态代表整张图像；2026 年可选 |
| Register token | "Sink token" | Extra learnable tokens that absorb the high-norm attention artifacts ViTs develop during pretraining | 额外可学习 token，吸收 ViT 预训练中产生的高范数注意力伪影 |
| Position embedding | "Positional info" | Per-position vector or rotation making the sequence-order-aware; 2D-RoPE is the modern default | 每个位置的向量或旋转，使序列具有顺序感知；2D-RoPE 是现代默认方案 |
| Grid | "Patch grid" | The (H/P) x (W/P) 2D array of patches for a given resolution and patch size | 给定分辨率和 patch 大小下的 (H/P) x (W/P) 2D patch 数组 |
| NaFlex | "Native flexible resolution" | SigLIP 2 feature: single model serves multiple aspect ratios and resolutions without retraining | SigLIP 2 特性：单一模型服务多种宽高比和分辨率，无需重新训练 |
| Backbone | "Vision tower" | The pretrained image encoder whose patch-token outputs feed the LLM in a VLM | 预训练的图像编码器，其 patch-token 输出喂入 VLM 中的 LLM |
| Pooling | "Image-level summary" | Strategy to turn patch tokens into one vector: CLS, mean, attention pool, or register-based | 将 patch token 转为一个向量的策略：CLS、均值、注意力池化或基于 register |
| Patch 14 vs 16 | "Finer vs coarser grid" | Patch 14 produces more tokens per image, better fidelity for OCR, slower; patch 16 is the classic default | Patch 14 每张图产生更多 token，OCR 保真度更高但更慢；patch 16 是经典默认值 |

## Mais leitura 延伸阅读

- [Dosovitskiy et al. — An Image is Worth 16x16 Words (arXiv:2010.11929)](https://arxiv.org/abs/2010.11929)- ViT original.
  中文翻译:原始 ViT 论文。
- [He et al. — Masked Autoencoders Are Scalable Vision Learners (arXiv:2111.06377)](https://arxiv.org/abs/2111.06377) MAE, auto-supervisão pré- treino.
  Tradução do português:MAE,自监督预训练──
- [Oquab et al. — DINOv2 (arXiv:2304.07193)](https://arxiv.org/abs/2304.07193)- Auto-distilação em escala, sem rótulos.
  Tradução do inglês: Masselha, não precisa de etiquetas.
- [Darcet et al. — Vision Transformers Need Registers (arXiv:2309.16588)](https://arxiv.org/abs/2309.16588) registar tokens e análise de artefatos.
  Tradução do inglês para tradução do inglês:
- [Tschannen et al. — SigLIP 2 (arXiv:2502.14786)](https://arxiv.org/abs/2502.14786) a torre de visão padrão de 2026.
  Tradução do inglês:
- [Zhai et al. — Scaling Vision Transformers (arXiv:2106.04560)](https://arxiv.org/abs/2106.04560) leis empíricas de escala.
  Tradução do inglês:
