# Modelagem autoregressiva visual (VAR): previsão em próxima escala.

> Os modelos de difusão amostram iterativamente no tempo (denotando passos). As amostras VAR iterativamente na escala  prevê um token 1x1, em seguida, 2x2, em seguida, 4x4, até a resolução final, cada escala condicionando sobre a anterior. O artigo de 2024 mostrou que o VAR combina com as leis de escalagem de estilo GPT para geração de imagem e supera o DiT no mesmo orçamento de computação. Esta lição constrói o mecanismo central.

> **【中文解读】**扩散模型在时间维度上代采样 (代采样) 去噪步骤), VAR在尺度维度上代先预测 1x1 token,再2x2,再4x4,直到目标分辨率──2024 论文证明 VAR 展现了GPT 风格的规模法,在相同计算预算下超越DiT──

> **【拓展：VAR 是生成模型的新范式】**O VAR voltará a se tornar um pensamento que se estenderá de "next one token" para "next one scale", abrindo novas direções para a geração de imagens.

**Type:** Build / 构建型
**Languages:** Python (with PyTorch)
**Prerequisites:** Phase 7 Lesson 03 (Multi-Head Attention / 多头注意力), Phase 8 Lesson 06 (DDPM)
**Time:** ~90 minutes

## O problema é o problema da introdução

A geração autoregressiva dominou a modelagem de linguagem porque escala de forma previsível: mais computação, mais parâmetros, menor perplexidade, melhores saídas. A geração de imagens teve duas tentativas principais de AR antes de 2024: PixelRNN/PixelCNN (pixel-by-pixel) e DALL-E 1 / Parti / MuseGAN (token-by-token em códigos VQ-VAE).

> O desenvolvimento de imagens em imagens de imagem de imagem de imagem de imagem de imagem de imagem de imagem de imagem de imagem de imagem de imagem de imagem de imagem de imagem de imagem de imagem de imagem de imagem de imagem de imagem de imagem de imagem de imagem de imagem de imagem de imagem de imagem de imagem de imagem de imagem de imagem de imagem de imagem de imagem de imagem de imagem de imagem de imagem de imagem de imagem de imagem de imagem de imagem de imagem de imagem de imagem de imagem de imagem de imagem de imagem de imagem de imagem de imagem de imagem de imagem de imagem de imagem de imagem de imagem de imagem de imagem de imagem de imagem de imagem de imagem de imagem de imagem de imagem de imagem de imagem de imagem de imagem de imagem de imagem de imagem de imagem de imagem de imagem de imagem de imagem de imagem de imagem de imagem de imagem de imagem de imagem de imagem de imagem de imagem de imagem de imagem de imagem de imagem de imagem de imagem de imagem de imagem de imagem de imagem de imagem de imagem de imagem de imagem de imagem de imagem de imagem de imagem de imagem de imagem de imagem de imagem de imagem de imagem de imagem de imagem de imagem de imagem de imagem de imagem de imagem de imagem de imagem de imagem de imagem de imagem de imagem de imagem de imagem de imagem de imagem de imagem de imagem de imagem de imagem de imagem de imagem de imagem de imagem de imagem de imagem de imagem de imagem de imagem de imagem de imagem de imagem de imagem de imagem de imagem de imagem de imagem de imagem de imagem de imagem de imagem de imagem de imagem de imagem de imagem de imagem de imagem de imagem de imagem de imagem de imagem de imagem de imagem de

Ambos sofreram um problema de ordem de geração. Pixels e tokens são dispostos em uma grade 2D, mas o modelo AR tem que visitá-los em uma ordem raster 1D. Um pixel de canto inicial não tem idéia do que a imagem acaba se tornando.

> 两者都困难在生成顺序问题──像素和代币 排列在2D 网格中,但AR 模型必须以1D光顺序访问──早期角落像素不知道图像最终将变成什么──生成质量扩展不像GPT,在相同计算量下从未达到扩散模型质量──

O VAR corrige o problema da ordem de geração alterando o que está sendo gerado. Em vez de prever tokens de imagem um por um no espaço, o VAR prevê uma imagem inteira com resoluções crescentes. Etapa 1: prevê um token 1x1 (a imagem geral "resumo"). Etapa 2: prevê uma grade de tokens 2x2 (funções mais grosseiras). Etapa 3: prevê uma grade de 4x4. Etapa K: prevê a grade final (H/8) x ((W/8)).

> VAR 通過改變生成對象來修复生成序列問題──不再逐空間預測圖像代號, VAR 以增分辨率預測整圖──步骤 1:預測 1x1代號(全局摘要)──步骤 2:預測 2x2代號 网格──步骤 K:預測最終网格──

Cada escala atende a todas as escalas anteriores (causalmente em "ordem de escala") e paralelo dentro de sua própria escala.

> Cada medida atende todas as medidas anteriores (em "ordem de medida" sobre o resultado), em sua própria medida.

> **【中文解读】**A inovação central do VAR(Visual Autoregressive) é: eliminar a "problemática de produção" de imagens em cada medida, eliminando a "problemática de produção" da AR.

> **【拓展：VAR 与扩散模型的对比】**O VAR é o modelo de re-amplificação mais potencial para gerar imagens novas. O VAR é o modelo de re-amplificação. O VAR é o modelo de re-amplificação de imagens.

## O conceito central.

### O Tokenizer VQ-VAE em Multicálculo

> ### VQ-VAE Tokenizer de várias dimensões

A VAR precisa de um**multi-scale discrete tokenizer**Para uma imagem x, produz uma sequência de grades de tokens de resolução progressiva mais alta:

> VAR  precisa um**多尺度离散 tokenizer** Para imagem x, ela produz uma série de aumentos de resolução de símbolos:

```
x -> encoder -> latent f
f -> tokenize at 1x1: token grid z_1 of shape (1, 1)
f -> tokenize at 2x2: token grid z_2 of shape (2, 2)
...
f -> tokenize at (H/p)x(W/p): token grid z_K of shape (H/p, W/p)
```

Cada z_k usa o mesmo livro de códigos ( tamanho típico 4096-16384). A tokenização em cada escala não é independente  é treinada de modo que a soma dos resíduos em cada escala reconstrui f:

```
f ≈ upsample(embed(z_1), target_size) + ... + upsample(embed(z_K), target_size)
```

Isto é um**residual VQ**variante. escala k capta o que escalas 1..k-1 faltaram. decodificador leva a soma de todos os embutidos da escala e produz a imagem.

> É um**残差 VQ**变体──尺度 k 捕获尺度 1..k-1 遗漏的内容──解码器将所有尺度嵌入并产生图像──

O tokenizer VQ em várias escalas é treinado uma vez (como VQGAN) e depois congelado.

> Multi-dimensional VQ tokenizer  treinar uma vez (como VQGAN) 结── todos os trabalhos de geração são realizados pelo modelo de auto-regressão do nível superior.

### Próxima previsão

> ### Próximo passo

O modelo gerativo é um transformador que vê tokens de todas as escalas anteriores e prevê os tokens na próxima escala.

> O modelo de produção é um transformador, vê todos os tokens de dimensões anteriores e prevê os tokens de dimensões seguintes.

Estrutura de sequência de entrada:
```
[START, z_1 tokens, z_2 tokens, z_3 tokens, ..., z_K tokens]
```

Os embebedamentos de posição codificam tanto o índice de escala quanto a posição espacial dentro da escala. A atenção é causal em ordem de escala: token na escala k, posição (i, j) pode atender a todos os tokens em escalas 1..k e para tokens na escala k que vêm antes em qualquer ordem intra-escala que seja usada (VAR usa atenção posicional fixa sem causalidade intra-escala  todas as posições dentro de uma escala são previstas em paralelo).

Perda de treinamento: em cada escala k, prever os tokens z_k dados todos os tokens de escala anterior. Perda de entropia cruzada nos códigos VQ discretos. A mesma estrutura que GPT exceto a "seqüência" é agora estruturada em escala.

### Geração

Na inferência:
```
generate z_1 = sample from p(z_1)                    # 1 token
generate z_2 = sample from p(z_2 | z_1)              # 4 tokens in parallel
generate z_3 = sample from p(z_3 | z_1, z_2)         # 16 tokens in parallel
...
decode: f = sum of embed-and-upsample scales 1..K
image = VAE_decoder(f)
```

Para uma escala K = 10, a geração é de 10 passes de transformador para a frente. Cada pass produz toda a sua escala em paralelo  sem autorregressão por token dentro de uma escala. Para uma imagem 256x256 isso é aproximadamente 10 passes versus 28-50 de DiT.

> Para K = 10 个尺度, produzir é 10 vezes transformador 前向传播──每次产生整个尺度尺度内无逐代号自归──256x256 图像约10次传播 vs DiT 的 28-50 次──

### Por que a próxima escala vence a próxima

> ### Por que a medida de baixo venceu a medida de baixo?

Três vitórias estruturais:

> Três vantagens estruturais:

1. **Coarse-to-fine aligns with natural image statistics.**A percepção visual humana e os conjuntos de dados de imagem apresentam regularidades dependentes da escala: a estrutura de baixa frequência é estável e previsível; os detalhes de alta frequência são condicionados ao conteúdo de baixa frequência.
   **从粗到细与自然图像统计一致。**低频结构稳定可预测;高频细节依赖低频内容──
2. **Parallel generation within scale.**Ao contrário do token AR do estilo GPT, o VAR produz todos os tokens em uma escala em um passo.
   **尺度内并行生成。**Diferente do GPT, AR, VAR um passo para produzir todo o tamanho de todos os tokens.
3. **No generation order bias.**Tokens na escala k vêem toda a escala k-1; não há "esquerdade" ou "acima" que força os tokens iniciais a se comprometer antes que o contexto tardío esteja disponível.
   **无生成顺序偏差。**O símbolo da medida k vê a medida k-1 de todas.

### Lei de Escalada

> ### Lei de escala / 缩放定律

Tian et al. demonstrou que o VAR segue uma curva de escalagem de poder para a FID na ImageNet  assim como o GPT faz para a perplexidade. O duplicado de parâmetros ou de cálculo reduz de forma confiável o erro à metade. Este foi o primeiro modelo gerador de imagens a exibir este tipo de comportamento de escala tão limpo quanto os modelos de linguagem. O resultado é que as previsões em escala VAR se tornam previsíveis a partir de computação, não suposições empíricas por arquitetura.

> Tian 等人 provou que VAR em ImageNet em FID segue a curva de encolhimento de regras  assim como GPT para a confusão . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .

### Relação com a difusão

> ### Relação com o modelo de expansão

A VAR e a difusão compartilham a mesma história de compressão de dados: ambos dividem o problema de geração em uma sequência de subproblemas mais fáceis.

> VAR e expansão compartilham a mesma história de compressão de dados: tudo irá gerar problemas divididos em uma sequência de problemas mais simples.

- Difusão: adicionar gradualmente ruído, aprender a desviar um passo.
  扩散: passo a passo aumentar o ruído, aprender a retirar passo a passo.
- VAR: adicionar gradualmente resolução, aprender a prever a próxima escala.
  VAR: passo a passo, aumento da resolução, aprendizagem de previsão da medida seguinte.

Eles são eixos diferentes através do problema. Ambos produzem distribuições condicionais tratáveis. Empiricamente, VAR é mais rápido na inferência (menos passes, todos paralelos dentro de uma escala) e corresponde ou supera o DiT na ImageNet condicional de classe.

> 它们是穿越问题的不同轴──两者都产生可处理的条件分布──实验上 VAR 推理更快(更少传播,尺度内全并行),在类别条件上 ImageNet 上匹配或超越 DiT──文本条件 VAR 是活跃研究方向──

## Construí-lo e realizei-o.
```figure
gx-var-next-scale
```

## Construí-lo

- Não .`code/main.py`Você vai:
1. Construir um pequeno .**multi-scale VQ tokenizer**em dados sintéticos de "imagem" (2 anéis gaussianos em dimensão).
2. Treinar um**VAR-style transformer**para a próxima escala-previsão dos tokens.
3. Amostra por chamada ao transformador 4 vezes (4 escalas) e decodificação.
4. Verificar que a formação em ordem de escala faz a geração paralela dentro de uma escala.

É uma implementação de brinquedo. O ponto é ver a máscara de atenção estruturada em escala e a geração paralela dentro da escala realmente a funcionar.

> Este é um brinquedo de realização. O foco é ver a estruturação da escala e a concentração de atenção em mascaradas e em escala para gerar um trabalho real.

## Envia-o . Produto .

Esta lição produz`outputs/skill-var-tokenizer-designer.md` habilidade para a concepção de um tokenizer de várias escalas: número de escalas, proporções de escala, tamanho do livro de códigos, partilha residual, arquitetura de decodificadores.

> 本课产生 `outputs/skill-var-tokenizer-designer.md` Design multi-dimensional tokenizer habilidade: dimensão número, dimensão proporcional, dimensão grande, divisão de divisão, estrutura de código.

## Exercícios.

1. **Scale count ablation.**Treinar VAR com 4, 6, 8, 10 escalas. Medir a qualidade da reconstrução vs número de passes autoregressivos. Mais escalas = restantes mais finos = melhor qualidade mas mais passes.

2. **Codebook size.**Trem tokenizers com tamanhos de código de 512, 4096, 16384.

3. **Parallel-within-scale check.**Para um VAR treinado, medir o padrão de atenção explicitamente. Dentro da escala k, o modelo atende a posições em escala transversal, mas não intra-escala? Verifique a implementação da máscara.

4. **VAR vs DiT scaling.**Para a mesma tarefa condicional de classe ImageNet, treine VAR e DiT em orçamentos de parâmetros iguais (por exemplo, 33M, 130M, 458M). Plot FID vs computação. VAR deve avançar em frente de DiT em cada tamanho  reproduzir o resultado do papel em pequena escala.

5. **Text conditioning.**Extender VAR para tomar uma incorporação de texto (CLIP agrupado) como uma entrada de condicionamento extra através da adaLN. Esta é a receita HART.

## Termos-chave .

| Term | What people say | What it actually means |
|------|----------------|----------------------|
| VAR | "Visual AutoRegressive" | Image generation by next-scale prediction over a pyramid of VQ token grids |
| Next-scale prediction | "Predict coarser, then finer" | The model predicts tokens at increasing resolution scales, conditioning on all previous scales |
| Multi-scale VQ tokenizer | "Residual VQ" | VQ-VAE that produces K token grids of increasing resolution, with decoder summing all scales |
| Scale k | "Pyramid level k" | One of K resolution levels, from 1x1 at k=1 up to (H/p)x(W/p) at k=K |
| Parallel-within-scale | "One forward per scale" | All tokens at scale k are predicted in one transformer pass, not autoregressively |
| Causal-across-scales | "Scale-ordered attention" | Token at scale k can attend to all of scales 1..k but not scales k+1..K |
| Residual VQ | "Additive tokenization" | Each scale's tokens encode the residual left by lower scales; decoder sums all scale embeddings |
| VAR scaling law | "Image GPT scaling" | FID follows a predictable power law in compute, like language models' perplexity |
| HART | "Hybrid VAR + text" | Text-conditional VAR variant combining MaskGIT-style iterative decoding with VAR's scale structure |
| Scale position embedding | "(scale, row, col) triple" | Positional encoding carries both the scale index and spatial coordinates within the scale |

## Mais leitura 延伸阅读

- [Tian et al., 2024 — "Visual Autoregressive Modeling: Scalable Image Generation via Next-Scale Prediction"](https://arxiv.org/abs/2404.02905) o documento VAR, referência canónica
- [Peebles and Xie, 2022 — "Scalable Diffusion Models with Transformers"](https://arxiv.org/abs/2212.09748) DiT, linha de base de comparação de difusão
- [Esser et al., 2021 — "Taming Transformers for High-Resolution Image Synthesis"](https://arxiv.org/abs/2012.09841) VQGAN, a família de tokenizadores VAR extensão de tokenizadores em várias escala
- [van den Oord et al., 2017 — "Neural Discrete Representation Learning"](https://arxiv.org/abs/1711.00937) VQ-VAE, a base da tokenização de imagens discretas
- [Tang et al., 2024 — "HART: Efficient Visual Generation with Hybrid Autoregressive Transformer"](https://arxiv.org/abs/2410.10812) VAR condicional de texto
