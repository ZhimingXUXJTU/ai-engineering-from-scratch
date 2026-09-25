# Emu3: Próximo Token Previsão para geração de imagem e vídeo

> O Emu3 da BAAI (Wang et al., setembro de 2024) é o resultado de 2024 que deveria ter terminado o debate difusão versus autorregressão. Um único transformador de decodificador de estilo Llama, treinado apenas no objetivo de previsão de tokens próximos, através de um vocabulário unificado de texto + tokens de imagem VQ + tokens de vídeo VQ 3D, bate o SDXL na geração de imagem e o LLaVA-1.6 na percepção. Sem perda de CLIP. Não há programa de difusão. A orientação sem classificador é usada na inferência para a qualidade, mas o objetivo principal do treinamento é a previsão do próximo token com o professor forçando. Publicado na revista Nature. Esta lição lê a tese Emu3  por que um melhor tokenizer mais escala é tudo que você precisa  e contrasta com as abordagens de difusão.

> **【中文解读】**Emu3(BAAI,2024年9月) usando um único token de auto-regressão 预测目标, em formação no texto unificado + imagem + vídeo vocabulário, derrotou SDXL na geração de imagem, derrotou LLaVA-1.6在视觉理解.

> **【拓展：自回归 vs 扩散的争论】**A contribuição central da Emu3 é conceitual: se o seguinte token 预测 预测 预测 预测 预测 预测 预测 预测 预测 预测 预测 预测 预测 预测 预测 预测 预测 预测 预测 预测 预测 预测 预测 预测 预测 预测 预测 预测 预测 预测 预测 预测 预测 预测 预测 预测 预测 预测 预测 预测 预测 预测 预测 预测 预测 预测 预测 预测 预测 预测 预测 预测 预测 预测 预测 预测 预测 预测 预测 预测 预测 预测 预测 预测 预测 预测 预测 预测 预测 预测 预测 预测 预测 预测 预测 预测 预测 预测 预测 预测 预测 预测 预测 预测 预测 预测 预测 预测 预测 预测 预测 预测 预测 预测 预测 预测 预测 预测 预测 预测 预测 预测 预测 预测 预测 预测 预测 预测 预测 预测 预测 预测 预测 预测 预测 预测 预测 预测 预测 预测 预测 预测 预测 预测 预测 预测 预测 预测 预测 预测 预测 预测 预测 预测 预测 预测 预测 预测 预测 预测 预测 预测 预测 预测 预测 预测 预测 预测 预测 预测 预测 预测 预测 预测 预测 预测 预测 预测 预测 预测 预测 预测 预测 预测 

**Type:** Learn  | **类型:** 学习
**Languages:** Python (stdlib, 3D video tokenizer math + autoregressive sampler skeleton) | **语言:** Python（标准库，3D 视频分词器数学 + 自回归采样器骨架）
**Prerequisites:** Phase 12 · 11 (Chameleon) | **前置知识:** Phase 12 · 11（Chameleon）
**Time:** ~120 minutes | **时间:** ~120 分钟

> - Não .**【前置】**學本节前请先掌握:Fase 12·11(Chameleon 早期融合 token) 、Fase 8·01-03(扩散模型基础,对照学习) 、Fase 7(自归下次代币 训练) ⋅Emu3 =Chameleon 思路 + 更好VQ 分词器 +大规模训练──
> - Não .**【类比】**扩散模型 vs Emu3 = "画油画" vs "拼乐高"。扩散 = 从噪音开始一步精修(连续去噪), cada passo todos re-draw整张图;Emu3 = 一个标记 往下拼拼;;离散乐高块),按顺序拼出图片──乐高看粗,但块足够小+种类足多时也能拼出逼真画面,而且和文本生成同一套机制(都是下一个标语)。
> 🤔 **【困惑】**P: 既然 Emu3 é tão forte, por que a difusão estável  ainda é dominante?                                                                                                                                                                                                                                                   

## Objetivos de aprendizagem

- Explique por que o objetivo de tokens de próxima perda única da Emu3 funciona apesar da suposição de que a difusão é necessária para a qualidade da imagem.
  >  Explicar por que a Emu3  单一损失下一代币 目标在长期假设"图像生成必须扩散"的情况下仍然有效──
- Descreva o tokenizer de vídeo 3D: como é um livro de códigos VQ espacial-temporal, por que os patches duram o tempo.
  > 描述 3D 视频分词器:时空 VQ 码本长什么样、为什么补丁 需要跨时间维度──
- Compare Emu3 vs. Stable Diffusion XL (computação de formação, custo de inferência, limite de qualidade).
  > Comparar Emu3 com a Estabilidade de Difusão XL em diferença na capacidade de treinamento, custo e qualidade.
- Nomear os três papéis que o mesmo modelo Emu3 desempenha: Emu3-Gen (gênero de imagem), Emu3-Chat (percepção), Emu3-Stage2 (gênero de vídeo).
  > 列举同一 Emu3 模型扮演的三种角色:Emu3-Gen(图像生成)、Emu3-Chat(感知)、Emu3-Stage2(视频生成)。

## O problema é o contexto do problema .

A sabedoria convencional até 2024: geração de imagens precisa de difusão. O argumento: os tokens de imagem discretos perdem muita informação para reconstruir detalhes, e a amostragem autoregressiva acumula erro em milhares de tokens. Estabilidade de difusão, DALL- E 3, Imagen, Midjourney todos usam alguma forma de difusão. O Camelão (Lessão 12.11) refutou parcialmente esta conclusão em pequena escala, mas não foi igual à SDXL em termos de qualidade.

> O resultado foi uma grande quantidade de dados que foram obtidos em uma série de imagens, incluindo imagens de imagens, que foram distribuídas em vários tipos de imagens, incluindo imagens de imagens, que foram distribuídas em vários tipos de imagens, e que foram distribuídas em vários tipos de imagens.

Emu3 atacou o argumento de frente. A alegação: melhor tokenizer visual + escala suficiente + perda de token seguinte = geração de imagem de difusão em batimento no mesmo modelo que também faz percepção.

> Emu3 está enfrentando esse ponto. Ele afirma: melhor visual divisor de palavras + 足够的规模 + 下一 token 损失 = gerar imagens que se espalham mais do que o normal no mesmo modelo, ao mesmo tempo que também podem fazer percepção.

A aposta foi controversa quando foi publicada. Dois anos depois, a família de geração unificada de código aberto (Emu3, Show-o, Janus-Pro, Transfusion) é o caminho padrão para a pesquisa; modelos de fronteira de produção parecem usar alguma variante.

> Esta publicação foi discutida. Dois anos depois, a sua vida inteira foi transformada em uma série de estudos.

## O conceito central.

> **【中文解读】**EMU3 Utilizando puro auto-regressão a um token  pré-determinado unificou multi-modelo entendimento e geração。 imagens são dispersadas em token  sequência, modelo como pré-determinado texto como pré-determinado a um token visual。

> **【拓展：自回归图像生成的挑战】**O método de auto-regressão da EMU3 ainda está atrasado no modelo de expansão na geração de imagens, pois a duração do token visual depende do texto mais difícil de aprender.


### O tokenizer Emu3

O ingrediente chave é o tokenizer visual. Emu3 treina um tokenizer personalizado da classe IBQ (Quantizer de garganta inversa, família SBER-MoVQGAN) a 8x8 de redução de resolução por token. Uma imagem de 512x512 torna-se 64x64 = 4096 tokens no tamanho do livro de código 32768.

> 关键成分是视觉分词器──Emu3 训练了自定义 IBQ 类分词器(逆瓶量化器,SBER-MoVQGAN 家族), cada token 8x8 分辨率缩减──一张 512x512 图像变成64x64 = 4096 代币,码本大小 32768──

Esta é maior do que os 1024 tokens do Chameleon por 512x512 em K=8192 mas mais barato por token (buscas de código menores, codec mais simples).

> É maior do que o Chameleon por 512x512 图像 1024 个标签(K=8192) maior, mas cada token mais barato(更小的码本查找、更简单的编解码器)  Key indicator: reconstruir PSNR para 30,5 dB, com o potencial de continuidade de Diffusion estável de 32 dB 竞争──

Para vídeo: um tokenizer VQ 3D codifica um patch espaciotemporal (4x4x4 pixels) para um número inteiro. Um clip 4s em 8 FPS tem 32 quadros; em 256x256 com 4x redução espacial e 4x temporal, a contagem de tokens é (256/4) * (256/4) * (32/4) = 64 * 64 * 8 = 32.768 tokens.

> 对于视频:3D VQ 分词器将时空补丁(4x4x4 像素)编码为整数──4秒片段在 8 FPS 下有 32 ;256x256 分辨率下 4x 空间和 4x 时间缩减,代码数字为 32768──

A qualidade do tokenizer é o teto.

> A contribuição do Emu3 está em "Nós treinamos um excelente eficiente eficiente"

### Formação de perda única

O Emu3 usa um objetivo: previsão do próximo token em um vocabulário compartilhado entre tokens de texto, tokens de imagem 2D e tokens de vídeo 3D. Os pesos são multiplicados por fatores específicos da modalidade durante o treinamento para equilibrar a contribuição, mas a função de perda é idêntica.

> Emu3 Utilize a um objetivo: em comunagem palavra-chave 预测, abrangendo texto token、2D 图像 token 和 3D 视频 token。 treinamento tempo de peso multiplicado em modo de fatores específicos para equilibrar contribuição, mas a função de perda é a mesma。

Trem em uma mistura de:
- Gênero de imagem: `<text caption> <image> image_tokens </image>`
  Tradução do inglês:
- Percepção de imagem: `<image> image_tokens </image> <question> text_tokens`
  Tradução do inglês:
- Gênero de vídeo: `<text caption> <video> video_tokens </video>`
  Tradução do português:
- Percepção de vídeo: análogo.
  Tradução do inglês:
- Apenas texto: NTP padrão.
  Tradução do inglês: 预测。

O modelo aprende quando emitir tokens de imagem versus tokens de texto a partir da distribuição de dados.`<image>`- Não.

> 模型从数据分布中学习何时输出图像代币与文本代币―― capacidade de geração de modelos em `<image>`标签后预测 Token de imagem

### Orientação e temperatura sem classificador

A geração de imagens autoregressivas fica muito melhor com a orientação sem classificador (CFG) na inferência. Emu3 usa: gerar duas vezes, uma vez com a legenda completa, uma vez com uma legenda vazia, misturar os logits com um peso de orientação (típico 3.0-7.0).

> Auto-registo imagem gerada em sugestão usando sem-classe orientador(CFG) efeito é melhor.

Temperatura é importante: muito alta, artefatos; muito baixa, colapso de modo.

> Temperatura muito importante: muito alta terá falsas imagens; muito baixa levará ao colapso do modelo.

### Três papéis, um modelo

Navio Emu3 como três APIs funcionalmente distintas, mas um conjunto de peso subjacente:

> Emu3 以三个功能不同 API 发货, mas usar o mesmo conjunto de权重:

- Emu3-Gen. geração de imagens.
  Em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em
- Emu3-Chat. VQA e legendas. Imagem de entrada (tokens), texto de saída.
  Em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em
- Emu3-Stage2. Geração de vídeo e VQA de vídeo. Entrada de texto ou vídeo, saída de texto ou vídeo.
  Em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em

Sem cabeças específicas, apenas modelos de instruções diferentes, o mesmo ponto de controlo.

> Não há nenhuma tarefa específica. Apenas um modelo de dica diferente.

### Indicadores de referência

Do artigo Emu3 (septembro 2024):

> 来自 Emu3 论文(2024 年 9 月):

- Geração de imagem: supera a SDXL no MJHQ-30K FID (5.4 vs 5.6), GenEval em geral (0.54 vs 0.55  empatia estatística), e o composto de Deep-Eval no par.
  No entanto, o resultado foi um resultado positivo, que não foi o mesmo que o resultado de uma nova versão.
- Percepção de imagem: supera a LLaVA-1.6 na VQAv2 (75.1 vs 72.4) e coincide aproximadamente na MMMU.
  No entanto, o que não é verdade é que o que não é verdade é que o mundo não é um mundo.
- Geração de vídeo: qualidade de vídeo de 4 segundos em FVD competitivo com modelos de referência pública da era Sora.
  O filme é uma adaptação do romance de ficção científica de ficção científica de ficção científica.

Os números nem sempre estão ganhando  Emu3 negocia um ponto aqui por um ponto lá  mas a afirmação "a previsão do próximo token é tudo o que você precisa" é defensivel em todas as modalidades.

> O número não é sempre vencedor em um ponto em troca de outro ponto, mas a afirmação de que "o seguinte token                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                  

### Custo de cálculo

Emu3 foi treinado em ~300 bilhões de tokens multimodal com um modelo de parâmetro 7B. Horas de GPU aproximadamente comparáveis ao pre-treinamento Llama-2-7B (2k-4k GPU-anos no silício da classe A100). Modelos de difusão como Stable Diffusion 3 treinam em orçamentos semelhantes, mas precisam de codificadores de texto separados e pipelines mais complexos.

> Emu3 em cerca de 3000 bilhões de tokens de modo modo que se exercitam com 70 bilhões de parâmetros. GPU: número de horas em comparação com Llama-2-7B  pre-treinamento equivalente (A100) em 2k-4k GPU ano) ⋅ Estabilidade Diffusion 3 etc.

Em inferência, Emu3 é mais lento do que SDXL por imagem: 4096 tokens de imagem a 30 tok/s é ~2 minutos por imagem 512x512 versus 2-5 segundos para SDXL. A descodificação especulativa e a otimização do cache KV reduzem a lacuna, mas não a fecham.

> 推理时,Emu3 Cada imagem em emagrecimento em comparação com SDXL 慢:4096 个图像代币 以 30 tok/s 生成,每张 512x512 图像约2分钟,而 SDXL只需2-5秒――投机解码和KV 缓存优化缩小了差距但没有关闭它――自归图像生成密度计算;这是持续存在的权衡――

### Por que é importante

A contribuição profunda do Emu3 é conceitual. Se a escala de previsão do token seguinte corresponder à difusão na geração de imagem, o caminho do modelo unificado (uma perda, uma espinha dorsal, qualquer modalidade) é viável. Os modelos futuros não precisam de codificadores de texto separados, agendadores de difusão separados, VAEs separados. Um transformador, um tokenizer por modalidade, escala.

> Se o token seguinte 预测能扩展到在图像生成上匹敌扩散,统一模型路径 ((un损失、一个骨干、任何模态) ), é viável.

Show-o, Janus-Pro e InternVL-U todos se baseiam ou desafiam essa tese. Os laboratórios chineses (BAAI, DeepSeek) publicam mais agressivamente nesta direção do que os laboratórios dos EUA até 2025.

> Show-o、Janus-Pro 和 InternVL-U foram construídos sobre este ponto de vista ou desafiaram-no.


> **【拓展：EMU3 的统一训练策略】**A contribuição central da EMU3 é a de provar que o método de auto-regressão puro pode ser simultaneamente compreendido e gerado.


## Use-o em prática.
```figure
l5-emu3-next-token
```

## Usá-lo

`code/main.py`Construi duas peças de brinquedo:

> `code/main.py`Construí dois componentes de brinquedos:

- Uma calculadora de contagem de tokenizer VQ 2D vs 3D: dada (resolução, correção, comprimento de clip, FPS), contagem de tokens de computação para imagem vs vídeo.
  Chinese Translation: 2D vs 3D VQ 分词器计数计算器:给定(分辨率、patch、片段长度、FPS),计算图像与视频的代号 数――
- Um amostragem autoregressiva de imagem-token com orientação de temperatura livre de classificador.
  Tradução do inglês para "Temporada"

A implementação do CFG corresponde à receita da Emu3  misturar logitas condicionais e incondicionais com um peso de orientação.

> CFG                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            

## Envia-o .

Esta lição produz`outputs/skill-token-gen-cost-analyzer.md`. Dada uma especificação de produto de geração (imagem ou vídeo, resolução-alvo, nível de qualidade, orçamento de latência), ele calcula o conteúdo dos tokens, o custo de inferência e escolhe a família Emu3 versus difusão.

> 本课产 出 `outputs/skill-token-gen-cost-analyzer.md` Foram fornecidas especificações de produtos (imagem ou vídeo  resolução de objetivos  qualidade  orçamento de atraso), ele calcula o número de tokens  custo de cálculo e seleciona entre a série Emu3 e o modelo de expansão 

## Exercícios.

1. Emu3 produz 4096 tokens por imagem de 512x512 com redução de 8x8.
   Em 3x8  redução                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                       

2. Leia a Seção 3.3 do Emu3 no tokenizer de vídeo. Descreva a forma do parche VQ 3D e por que é 4x4x4 e não 8x8x1.
   Em tradução do inglês, em português, em português, em português, em português, em português, em português, em português, em português, em português, em português, em português, em português, em português, em português, em português, em português, em português, em português, em português, em português, em português, em português, em português, em português, em português, em português, em português, em português, em português, em português, em português, em português, em português, em português, em português, em português, em português, em português, em português, em português, em português, em português, em português, em português, em português, em português, em português, em português, em português, em português, em português, em português, em português, em português, em português, em português, em português, em português, em português, em português, em português, em português, em português, em português, em português, em português, em português, em português, em português, em português, em português, em português, em português,

3. Peso de orientação livre de classificadores 5.0 vs 3.0: que efeito visual?`code/main.py`- Não .
   Não há nenhuma classificação para controlar o peso de 5.0 vs 3.0: visual effect é?`code/main.py`Matemática Central.

4. Compute os FLOP de treinamento para Emu3-7B a 300B tokens e compare com a Diffusão Estabilizada 3.
   Em tradução do inglês, calcula-se o Emu3-7B em 300B token, que é mais caro do que o FLOP?

5. A Emu3 supera a SDXL na FID, mas não na VQAv2 versus VLM especializados.
   Em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em

## Termos-chave .

| Term | What people say | What it actually means | 中文含义 | 中文释义 |
|------|-----------------|------------------------|---------|
| Next-token prediction | "NTP" | Standard autoregressive loss: predict token[i+1] given token[0..i]; works for every modality when tokenized | 标准自回归损失：给定 token[0..i] 预测 token[i+1]；分词后适用于所有模态 |
| IBQ tokenizer | "Inverse bottleneck quantizer" | A class of VQ-VAE with larger codebooks (32768+) and better reconstruction than Chameleon's | 一类更大码本（32768+）和更好重建质量的 VQ-VAE |
| 3D VQ | "Spatiotemporal quantizer" | Codebook indexed by (time, row, col); one token covers a 4x4x4 pixel cube | 按（时间、行、列）索引的码本；一个 token 覆盖 4x4x4 像素立方体 |
| Classifier-free guidance | "CFG" | Mix conditional and unconditional logits with weight gamma; boosts image quality at inference | 用权重 gamma 混合条件和无条件 logits；提升推理图像质量 |
| Unified vocabulary | "Shared tokens" | Text + image + video all draw from the same integer space; model predicts whichever modality comes next | 文本+图像+视频共享同一整数空间；模型预测下一个模态 |
| MJHQ-30K | "Image gen benchmark" | Midjourney-quality benchmark with 30k prompts; Emu3 reports FID here | 30k 提示的 Midjourney 质量基准；Emu3 报告 FID |

## Mais leitura 延伸阅读

- [Wang et al. — Emu3: Next-Token Prediction is All You Need (arXiv:2409.18869)](https://arxiv.org/abs/2409.18869)
  Em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em
- [Sun et al. — Emu: Generative Pretraining in Multimodality (arXiv:2307.05222)](https://arxiv.org/abs/2307.05222)
  Em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em
- [Liu et al. — LWM (arXiv:2402.08268)](https://arxiv.org/abs/2402.08268)
  Tradução do português:LWM
- [Yu et al. — MAGVIT-v2 (arXiv:2310.05737)](https://arxiv.org/abs/2310.05737)
  Tradução do português:MAGVIT-v2 视频分词器──
- [Tian et al. — VAR (arXiv:2404.02905)](https://arxiv.org/abs/2404.02905)
  O que é que é o "VAR" ?
