# Qualquer resolução de visão: Patch-n'-Pack e NaFlex  arbitrário de resolução

> Imagens reais não são 224x224 quadrados. Um recibo é 9:16, um gráfico é 16:9, uma varredura médica pode ser 4096x4096, uma captura de tela móvel é 9:19.5. A resposta VLM pré-2024  redimensionar tudo para um quadrado fixo  jogou fora o sinal que faz OCR, compreensão de documentos e análise de cena de alta resolução trabalhar. NaViT (Google, 2023) mostrou que você pode embalar patches de resolução variável em um único lote de transformador com mascaramento de diagonal de bloco. O M-RoPE (2024) do Qwen2-VL desistiu completamente das tabelas de posições absolutas. AnyRes do LLaVA-NeXT enrolaram imagens de alta resolução em uma base + sub-imagens. A variante NaFlex (2025) do SigLIP 2 é agora o codificador padrão para VLMs abertos que querem um único ponto de verificação para atender a cada relação de aspecto. Esta lição implementa patch-n'-pack de ponta a ponta.

> **【中文解读】**A imagem do mundo real não é quadrada de 224x224                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                              

> **【拓展：金融文档场景的分辨率挑战】**No cenário financeiro, a amplitude dos documentos de relatórios, emissão de votos, contratos e outros documentos é superior a mil diferenças. A redução de forma quadrada fixa leva a uma redução da precisão do texto.

**Type:** Build  | **类型:** 构建
**Languages:** Python (stdlib, patch packer + block-diagonal mask)  | **语言:** Python（标准库，补丁打包器 + 块对角掩码）
**Prerequisites:** Phase 12 · 01 (ViT patches), Phase 12 · 05 (LLaVA)  | **前置知识:** Phase 12 · 01（ViT补丁）、Phase 12 · 05（LLaVA）
**Time:** ~120 minutes  | **时间:** ~120 分钟

> - Não .**【前置】**學本节前 請先掌握:Fase 12·01 ViT 把图切成补丁;Fase 12·05 LLaVA 投影器);Fase 7·04 RoPE 位置编码,本节用2D-RoPE) 
> - Não .**【类比】**NaViT's patch-n'-pack = "mover-se para um pacote"── tradicional ViT = Colocar tudo em uma caixa de grandes cortes, pernas de peças cortadas e embutidas; NaViT = diferentes tipos de caixas de tamanho em forma de pacote, um caminhão em um pacote de vários pacoteiros.
> ️ **【易错点】**实现 NaViT 时忘记块对角掩码 → 三张图的补丁 会相互注意,模型训练完全失败──修复:必须构建 (N,N) 的注意矩阵,只允许注意,块外为 -inf──

## Objetivos de aprendizagem

- Envolva os patches de um lote de imagens de resolução variável numa sequência e construa a máscara de atenção de bloco-diagonal.
  > Envolver os complementos de imagens de diferentes resoluções em uma sequência, construindo blocos em função do ângulo.
- Escolha entre o OneRes tiling (LLaVA-NeXT), o NaFlex (SigLIP 2) e o M-RoPE (Qwen2-VL) para uma determinada tarefa.
  > De acordo com o trabalho que você tem feito, você pode fazer um trabalho de pesquisa com o seu próprio computador.
- Compute orçamentos de tokens para OCR, gráficos e fotografia sem redimensionar.
  > 计算无缩缩的情况下 OCR、图表和摄影的代币 预算──
- Cite os três modos de falha de quadrado: texto esmagado, conteúdo cortado, tokens desperdiçados no enchimento.
  > 列举正方形缩放的三种失败模式:文字压缩,内容裁剪,padding 浪费, 文字压缩,内容裁剪, padding 浪费, 文字压缩,内容裁剪, padding 浪费, 文字压缩, 文字压缩, 文字剪, 文字剪, 文字剪, 文字剪, 文字剪, 文字剪, 文字剪, 文字剪, 文字剪, 文字剪, 文字剪, 文字剪, 文字剪, 文字剪, 文字剪, 文字, 文字, 文字, 文字, 文字, 文字, 文字, 文字, 文字, 文字, 文字, 文字, 文字, 文字, 文字, 文字, 文字, 文字, 文字, 文字, 文字, 文字, 文字, 文字, 文字, 文字, 文字, 文字, 文字, 文字, 文字, 文字, 文字, 文字, 文字, 文字, 文字, 文字, 文字, 文字, 文字, 文字, 文字, 文字, 文字, 文字, 文字, 文字, 文字, 文字, 文字, 文字, 文字, 文字, 文字, 文字, 文字, 文字, 文字, 文字, 文字, 文字, 文字, 文字, 文字,  文字,       文字,                                                                                                                                                                          

## O problema é o contexto do problema .

Os transformadores esperam uma sequência. Um lote é uma pilha de sequências do mesmo comprimento. Se as suas imagens são 224x224, você recebe 196 tokens de parche toda vez, não é necessário enchimento, o trabalho feito. Trein no 224, infer no 224, nunca mais pense sobre resolução.

> Transformador 期望固定长度序列──一批就是一堆等长序列──如果图像都是224x224,每次都产生196补丁代币,无需填充,问题解决──训练和推理都用224,永远不用考虑分辨率──

Os documentos são retratos (8,5x11 polegadas, 2:3-ish). As imagens de gráficos são paisagem (16:9). Os recibos são altos e finos (1:3). Os navios de imagem médica em 2048x2048 ou maior.

> 现实世界不配──文档是向的(8.5x11英寸,约 2:3)──图表截图是横向的(16:9)──收据又高又窄(1:3)──医疗影像动 2048x2048或更大──移动设备截图是1170x2532(0.46:1)──

Três opções pré-2024 e por que cada uma falha:

> Três opções anteriores a 2024 e as suas causas de fracasso:

1. Reduzir para um quadrado fixo (224x224 ou 336x336). O squish distorce texto e faces. A escala baixa destrói os rótulos de gráficos e o conteúdo de OCR. Prática padrão até LLaVA-1.5.
   > 缩放为固定正方形(224x224或336x336) ――压缩会扭曲文字和人脸──下采样会破坏图表标签和OCR 内容──LLaVA-1.5 之前的标准做法──
2. A colheita em uma relação de aspecto fixa, você joga fora a maior parte da imagem, e escolher o local da colheita é seu próprio problema de visão.
   > 剪裁为固定宽高比──将丢弃大部分图像,而选择剪裁位置本身就是一个视觉问题──
3. Pad para o lado mais longo. Corre distorção, mas desperdiça 50%+ de tokens em padding para imagens de retrato.
   > 填充到最长边──修复扭曲但对屏图像浪费50%+的代币 在填充上──所有填充代币的注意成本是二次的──

> **【中文解读】**Transformador  expectativa fixa de longitude de sequência。 real world imagens宽高比不同,2024 年前有三种做法:(1) 缩缩为正方形文字变形、OCR 内容丢失;(2) 剪丢弃大量内容;(3) 填充屏图像浪费 50%+ 的代币 在填充上,注意计算成本第二次增长──

A resposta 2024-2025: deixe o transformador comer manchas na resolução nativa da imagem, e descobrir como empacotar um lote heterogêneo em uma sequência sem desperdiçar computação.

> Resposta para 2024-2025: Deixar o transformador "comer" diretamente com o remédio de resolução original, e depois pensar em como transformar a nova construção em uma série sem desperdiçar a sua calculação.

## O conceito central.

### NaViT e patch-n'-pack

NaViT (Dehghani et al., 2023) foi o artigo que mostrou que isso funciona em escala.

> NaViT ((Dehghani 等人,2023) provou esse pensamento em grande escala.

1. Para cada imagem no lote, calcule a sua grade de parche nativa em um tamanho de parche escolhido (digamos 14).
   > Para cada imagem em lote, para especificar o tamanho do aditamento (como 14)
2. Aplanar os patches de cada imagem em sua própria sequência de comprimento variável.
   > Para cada imagem, o arquivo é dividido em sequências de tamanho variável.
3. Concatenar todos os parches de imagens em uma longa sequência para o lote.
   > Vou fazer todas as correções de imagens em uma longa sequência como batidas.
4. Construir uma máscara de atenção de diagonal de bloco para que os parches da imagem A só atendam dentro da imagem A.
   > Construir blocos para ocultar a atenção dos cantos, fazendo com que os correções da imagem A sejam apenas no interior da imagem A.
5. Carregar informações de posição por parche (2 RoPE ou inserções de posição fracionária).
   > Para cada um dos equipamentos, carrega informações de localização.

Um lote de três imagens em 336x336 (576 tokens), 224x224 (256 tokens) e 448x336 (768 tokens) se torna uma sequência de 1600 tokens com uma máscara de bloco-diagonal 1600x1600.

> Três diferentes resoluções imagens ((336x336=576 tokens、224x224=256 tokens、448x336=768 tokens) de lote transformado em uma sequência de 1600 tokens, usando 1600x1600 blocos em canto escondido──零填充,零浪费──Transformer Natural Processing arbitrária宽高比──

NaViT também introduziu a queda de parches fracionários durante o treinamento  queda de 50% de parches aleatórias em todo o lote  que regulariza e acelera o treinamento.

> NaViT também introduziu o treinamento de quantidade de suplementos abandonados em loteamento de 50% de cada vez em cada lote.

> **【中文解读】**NaViT's core: 三张不同分辨率的图像(576 + 256 + 768 = 1600 个代币) foi embalado em uma sequência, usando blocos em torno de ângulos para evitar o atraso de imagens. Zero acoplamento, zero perda de energia. NaViT também introduziu treinamento, ao perder 50% de técnicas de correção, tanto a normalização quanto a aceleração do treinamento.

### Qualquer um de nós pode ser um bom homem.

O AnyRes da LLaVA-NeXT é a alternativa pragmática. Dada uma imagem de alta resolução e um codificador fixo (CLIP ou SigLIP em 336), o quadro é feito de azulejo:

1. Escolha um layout de grade de um conjunto predefinido  (1x1), (1x2), (2x1), (1x3), (3x1), (2x2), etc.  que melhor se adapte à relação de aspecto da imagem.
2. Tire a imagem completa na grade; cada telha torna-se uma colheita de 336x336.
3. Também produzir uma miniatura: toda a imagem redimensionada para 336x336 como um token de contexto global.
4. Encode cada telha através do encodeador congelado 336. Concatenate os tokens de telha + tokens de miniatura.

Para uma imagem 672x672 em 2x2 grade mais miniatura: 4 * 576 + 576 = 2880 tokens visuais.

AnyRes é a rota de escolha quando o seu codificador está congelado e suporta apenas uma resolução. Ele explode a contagem de tokens para imagens grandes (uma imagem de 1344x1344 em 4x4 grade é 9216 + 576 ≈ 9800 tokens, que preenche a maior parte de um contexto LLM de 8k).

> **【中文解读】**AnyRes  Aplica-se para codificadores de resolução única e apenas para soluções de resolução única.

### M-RoPE (Qwen2-VL)  M-RoPE 多模态旋转位置编码

Qwen2-VL introduziu a Embedding Multimodal Rotary Positioning. Em vez das posições fracionárias do NaViT ou da telha e miniatura do AnyRes, cada parche carrega uma posição 3D (temporal, altura, largura). As rotações de consulta / chave gerenciam H, W e comprimento temporal arbitrários.

M-RoPE envia resolução dinâmica nativa sem reformulação. Na inferência de você alimentar qualquer imagem HxW, o inseridor de patch produz tokens H/14 x W/14, cada token obtém sua posição (t=0, r=row, c=col), RoPE gira a atenção com as frequências certas, feito. Qwen2.5-VL e Qwen3-VL continuam assim. V2PE do InternVL3 é a mesma ideia com codificação variável por modalidade.

Ao contrário de AnyRes, M-RoPE é O(H x W / P^2) tokens em resolução nativa  sem sobrecarga de azulejos multiplicativos. Ao contrário de NaViT, ele ainda espera uma única imagem por avanço. Batching em resoluções ainda precisa de patch-n'-pack no topo.

> **【中文解读】**M-RoPE para cada complemento atribui três dimensões de posição (tempo, altura, largura), usando o código de posição de rotação para processar qualquer H、W 和 tempo de comprimento.

### NaFlex (SigLIP 2) NaFlex                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                   

NaFlex é o modo nativo do checkpoint SigLIP 2. Um único modelo serve vários comprimentos de sequência (256, 729, 1024 tokens) na inferência. Internamente, ele usa patch-n'-pack no estilo NaViT durante o treinamento e posições fraccionais absolutas por patch.

Para uma tarefa semântica (classificação, recuperação), 256 tokens. Para OCR ou compreensão de gráficos, 1024 tokens. Sem reformulação.

> **【中文解读】**NaFlex's core selling point: um checkpoint, recomendação em função de tarefa seleção de token  orçamento。语义任务使用256 token,OCR或图表理解使用1024 token,无需重训──这非常适合构建成本敏感多模态服务按需分配 token 预算──

### A máscara de embalagem.

A máscara de diagonal de bloco é onde a maioria das implementações tropeça.`N_total`Representações de imagens `i=0..B-1`com comprimentos `n_i`, a máscara .`M`de forma`(N_total, N_total)`é 1 se ambos os índices caem no mesmo bloco da imagem, ou 0. Você pode construí-lo a partir de uma lista de comprimento cumulativo:

```
offsets = [0, n_0, n_0+n_1, ..., N_total]                         # 累积偏移量
M[i, j] = 1 iff there exists b where offsets[b] <= i < offsets[b+1] # 同一图像块内为1
                        and offsets[b] <= j < offsets[b+1]
```

Esta é uma linha em PyTorch com `torch.block_diag`O caminho de comprimento variável da FlashAttention (`cu_seqlens`) salta a máscara inteiramente e atende em sequências usando o tensor de comprimento acumulativo diretamente  ~ 10 vezes mais rápido do que uma máscara densa para lotes típicos.

> **【中文解读】**Bloco contra canto escondido para garantir que cada imagem de correção apenas se concentre em si mesmo, não "ver" com os outros lotes de correções de imagem.`cu_seqlens`) direto com a acumulação de longitude, a concentração, saltando sobre o esconderijo, velocidade de cerca de 10 vezes.

### Orçamento de tokens

Escolha a sua estratégia por tarefa:

- OCR / documentos: 1024-4096 tokens. SigLIP 2 NaFlex em 1024, ou AnyRes 3x3 + miniatura.
- Gráficos e UI: 729-1024 tokens em 384-448 nativo. Qwen2.5VL resolução dinâmica com limite máximo de pixels.
- Fotos naturais: 256-576 tokens está bem. O LLM em baixo vai ver o suficiente. Pague para tokens onde a densidade de conteúdo é alta.
- Vídeo: 64-128 tokens por quadro após a agregação espacial, 2-8 FPS. Lição 12.17 abrange isto.

A regra de produção de 2026: escolher um limite máximo de pixels por tarefa, codificar em relação de aspecto nativa até esse limite, embalar o lote e saltar empilhadeira.`min_pixels`E ...`max_pixels`Para este botão.

> **【拓展：Token 预算与成本优化】**Em ambiente de produção, o token  orçamento afeta diretamente a API 成本和延迟── para as tarefas OCR 分配 1024+ tokens é necessário, mas naturalmente fotos com 256 tokens já são suficientes──按任务动态调整分辨率是2026年 VLM 部署的最佳实践──

> 🤔 **【困惑】**O que é que é que é o que é o que é o que é o que é o que é o que é o que é o que é o que é o que é o que é o que é o que é o que é o que é o que é o que é o que é o que é o que é o que é o que é o que é o que é o que é o que é o que é o que é o que é o que é o que é o que é o que é o que é o que é o que é o que é o que é o que é o que é o que é o que é o que é o que é o que é o que é o que é o que é o que é o que é o que é o que é o que é o que é o que é o que é o que é o que é o que é o que é o que é o que é o que é o que é o que é o que é o que é o que é o que é o que é o que é o que é o que é que é o que é que é o que é que é o que é que é o que é?

## Use-o em prática.
```figure
mm-patch-n-pack
```

## Usá-lo

`code/main.py`Implementa o patch-n'-pack para um lote heterogêneo de imagens com coordenadas de pixel inteiros.

> `code/main.py`Usando um conjunto inteiro de imagens, o sitemap conseguiu um pacote de imagens de diferentes conjuntos.

- Toma uma lista de tamanhos de imagem (H, W).
  > 接收 (H, W) 图像尺寸列表──
- Calcula o comprimento da sequência de parches de cada imagem no tamanho de parche 14.
  > 計算每张图像在补丁大小 14 下的序列长度──
- Enchém-os numa sequência de comprimento total .`sum(n_i)`- Não .
  > 打包为总长度 `sum(n_i)`De uma única sequência.
- Construi a máscara de atenção de bloco-diagonal (densa, para clareza).
  > Construção de blocos em angulares
- Compara o custo de embalagem com o tamanho quadrado e o revestimento de AnyRes.
  > Comparado com o custo de embalagem versus o de forma quadrada e o de qualquer pedaço de material.
- Imprime uma tabela de orçamento simbólico para um lote misturado (receito, gráfico, captura de tela, foto).
  > 打印混合批次(收据、图表、截图、照片) do token  orçamento

Os números que caem são a razão de cada VLM aberto em 2026 usarem patch-n'-pack.

> O número impresso é o que faz com que todos os VLMs usem patch-n'-pack em 2026.

## Envia-o .

Esta lição produz`outputs/skill-resolution-budget-planner.md`. Dada uma carga de trabalho de relação de aspecto mista (OCR, gráficos, fotos, quadros de vídeo) e um orçamento total de tokens, ele escolhe a estratégia certa (NaFlex, AnyRes, M-RoPE ou quadrado fixo) e emite uma configuração por pedido.

> 本课产 出 `outputs/skill-resolution-budget-planner.md` dado um mix mixed width-high-比工作 load (OCR, gráfico, fotografia, vídeo) e um total de tokens 预算, ele escolhe a estratégia correta (NaFlex, AnyRes, M-RoPE ou quadrado fixo) e gera a configuração de pedido  Usando esta habilidade para a seleção de produtos VLM                                                                                                                                                                                                                      

> **【中文解读】**O programa de avaliação de desempenho de um grupo de empresas de pesquisa e pesquisa em pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa em pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa em pesquisa de pesquisa de pesquisa de pes

## Exercícios.

1. Um recibo é 600x1500 (1:2.5). No tamanho do patch 14, quantos tokens de resolução nativa? Quantos depois de quadrado para 336? Que perde mais precisão OCR na prática?
   | 一张收据 600x1500（1:2.5）。补丁大小14下，原始分辨率多少 token？缩放到336正方形后多少？实际中哪种 OCR 精度损失更大？

2. Construa a máscara de diagonal de bloco para um lote de quatro imagens com comprimentos 256, 576, 729, 1024. Verifique a matriz de atenção é 2585x2585 e tem exatamente `256^2 + 576^2 + 729^2 + 1024^2`Notas não-zero.
   | 为四张长度分别为 256、576、729、1024 的图像构建块对角掩码。验证注意力矩阵为 2585x2585 且非零元素数精确为 `256^2 + 576^2 + 729^2 + 1024^2`。

3. Para uma imagem 1792x896 no patch 14, compare: (a) quadrado-dimensional para 336 e então codificar, (b) AnyRes 2x1 + miniatura, (c) M-RoPE em nativo. Qual usa menos tokens?
   | 对于 1792x896 的图像（补丁14），对比：(a) 缩放到336正方形，(b) AnyRes 2x1+缩略图，(c) M-RoPE 原始分辨率。哪种 token 最少？哪种保留最多细节？

4. Implementar a queda de parche fracionário: dada uma sequência embalada, solte 50% dos tokens uniformemente ao acaso e atualize a máscara de diagonal de bloco em conformidade. Meter a mudança de esparcia da máscara.
   | 实现分数补丁丢弃：给定打包序列，随机均匀丢弃50%的token，更新块对角掩码，测量掩码稀疏度变化。

5. Leia a secção 3.2 do documento Qwen2-VL (arXiv:2409.12191).`min_pixels`E ...`max_pixels`O controlo e por que ambas as fronteiras importam.
   | 阅读 Qwen2-VL 论文第 3.2 节（arXiv:2409.12191）。用两句话描述 `min_pixels` 和 `max_pixels` 控制什么，为什么两个边界都很重要。

## Termos-chave .

| Term | What people say | What it actually means | 中文含义 | 中文释义 |
|------|-----------------|------------------------|----------|---------|
| Patch-n'-pack | "NaViT-style packing" | Concatenate variable-length patch sequences from different images into one batch dimension | 将不同图像的可变长度补丁序列拼接到一个批次维度 | |
| Block-diagonal mask | "Packing mask" | Attention mask that confines each image's patches to attend only to themselves, not neighbors in the pack | 块对角掩码：限制每张图像的补丁只关注自身 | |
| AnyRes | "LLaVA-NeXT tiling" | Split a high-res image into a grid of fixed-size tiles plus a global thumbnail; encode every tile with a fixed encoder | 将高分辨率图像切分为固定大小网格+全局缩略图 | |
| NaFlex | "SigLIP 2 native-flex" | Single SigLIP 2 checkpoint that serves 256/729/1024-token budgets at inference without retraining | 单一 SigLIP 2 checkpoint 推理时支持多种 token 预算 | |
| M-RoPE | "Multimodal RoPE" | 3D rotary position encoding (time, row, column) that handles arbitrary H, W, T without position tables | 三维旋转位置编码（时间、行、列），处理任意宽高和时间长度 | |
| cu_seqlens | "FlashAttention packing" | Cumulative-length tensor the FlashAttention varlen path uses instead of a dense block-diagonal mask | FlashAttention 可变长度路径使用的累积长度张量 | |
| min_pixels / max_pixels | "Resolution bounds" | Qwen2.5-VL per-request knobs capping token count on very small or very large inputs | Qwen2.5-VL 按请求控制最小/最大像素数的参数 | |
| Visual token budget | "How many tokens per image" | Rough count of patch tokens emitted per image; sets the LLM's prompt budget and attention cost | 每张图像产生的补丁 token 数，决定 LLM 的提示预算和注意力成本 | |

## Mais leitura 延伸阅读

- [Dehghani et al. — Patch n' Pack: NaViT (arXiv:2307.06304)](https://arxiv.org/abs/2307.06304)O treinamento de NaviT de resolução arbitrária
- [Wang et al. — Qwen2-VL (arXiv:2409.12191)](https://arxiv.org/abs/2409.12191) Qwen2-VL Multi-modo de rotação
- [Laurençon et al. — What matters when building vision-language models? (Idefics2, arXiv:2405.02246)](https://arxiv.org/abs/2405.02246)Factor-chave para construir VLM
- [Tschannen et al. — SigLIP 2 (arXiv:2502.14786)](https://arxiv.org/abs/2502.14786)O Siglip 2 NaFlex
- [Qwen Team — Qwen2.5-VL Technical Report (arXiv:2502.13923)](https://arxiv.org/abs/2502.13923) Qwen2.5VL  relatório técnico
