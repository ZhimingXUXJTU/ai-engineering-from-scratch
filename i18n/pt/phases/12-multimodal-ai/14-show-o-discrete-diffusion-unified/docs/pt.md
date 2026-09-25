# Show-o e Discreto-Difusão Modelos Unificados .

> A transfusão mistura representações contínuas e discretas. Show-o (Xie et al., agosto 2024) vai pelo outro lado: tokens de texto usam previsão causal do próximo token, tokens de imagem usam difusão discreta mascarada no espírito do MaskGIT. Ambos sentam-se dentro de um transformador com uma máscara híbrida de atenção. O resultado unifica VQA, texto-para-imagem, inpainting e geração de modalidade mista em uma espinha dorsal, um tokenizer por modalidade, uma formulação de perda (next-token estendido para previsão mascarada). Esta lição segue o design Show-o  por que a difusão discreta mascarada é um gerador de imagem paralelo, em poucos passos  e contrasta com Transfusão e Emu3.

> **【中文解读】**Show-o(2024年8月)走另一条路:文本代币 用因果下一代币 预测,图像代币 用掩码离散散散散散(MaskGIT风格) ・・・ ambos compartilham um Transformer, usarem mistura de atenção掩码。 resulta um ponto de verificação 同时支持 VQA、文本生成图像和图像修复──

> **【拓展：并行解码的速度优势】**Show-o produz imagens apenas precisa de cerca de 16 passos, enquanto o Camelão/Emu3 precisa de 1024-4096 passos, cada token se regenera. Isso torna o Show-o o mais rápido de todo o seu tempo, mas a qualidade da imagem é limitada à reconstrução do token VQ.

**Type:** Learn  | **类型:** 学习
**Languages:** Python (stdlib, masked-discrete-diffusion sampler) | **语言:** Python（标准库，掩码离散扩散采样器）
**Prerequisites:** Phase 12 · 13 (Transfusion) | **前置知识:** Phase 12 · 13（Transfusion）
**Time:** ~120 minutes | **时间:** ~120 分钟

> - Não .**【前置】**學本節前請先掌握:Fase 12·13(Transfusão 双损失) ‧Fase 12·11-12(Chameleon/Emu3 离散代币) ‧Fase 8(MaskGIT 离散扩散概念) ‧Show-o = 全离散 + 图像用MaskGIT 风格并行解码,速度比Emu3 快 60 倍──
> - Não .**【类比】**Show-o = "并行开锁"──Emu3 = 一把钥匙开 1024 把锁(自归单个代币);Show-o = 16 步内同时尝试所有锁(掩码扩散并行解码)──代价:图像质量略差(VQ 量化损失),但推理快得多──

## Objetivos de aprendizagem

- Explicar a difusão discreta mascarada: o cronograma que mascara os tokens uniformemente e então pede ao transformador para recuperá-los.
  > Explicar o cache de dispersação: um token de mascarada, e depois deixar o transformador recuperar a sua regulação.
- Compare a descodificação de imagem paralela (Show-o, MaskGIT) com a descodificação de imagem autoregressiva (Chameleon, Emu3) em velocidade e qualidade.
  > Comparar e fazer imagens de vídeo (Show-o、MaskGIT) com imagens de vídeo (Chameleon、Emu3) em velocidade e qualidade.
- Nomear as três tarefas que o Show-o realiza num único ponto de controlo: T2I, VQA, pintura de imagem.
  > 列举 Show-o em um checkpoint 中支持的三种任务:T2I、VQA、图像修复──
- Escolha um cronograma de enmascaramento (cosinoso, linear, truncado) e racionalize o seu efeito sobre a qualidade da amostra.
  > 选择掩码调度 (余弦、线性、截断)并分析其对采样质量的影响.

## O problema é o contexto do problema .

A transfusão funciona com dois perdas de treinamento, mas tem dinâmica mais complicada. A perda contínua de difusão vive em uma escala numérica diferente da perda discreta de NTP.

> O treinamento de dupla perda de transfusão é possível mas o comportamento é mais complexo  perda de expansão contínua e perda de NTP separada  perda em escala numérica diferem                                                                                                                                                                                                                                         

A resposta de Show-o: mantenha ambas as modalidades discretas (como o Camelão), mas gerar imagens em paralelo através de difusão discreta mascarada em vez de sequencialmente.

> A resposta do show-o: manter dois tipos de modelos são separados, mas através do esconde se espalham e geram imagens, e não em ordem de geração.

## O conceito central.

> **【中文解读】**Show-o 统一多模态理解和生成, usando o deslocamento de expansão substituindo o tradicional continuidade de expansão── deslocamento de expansão diretamente em token 级别操作,将遮罩预测(理解任务) 和去噪音(生成任务)统一在同一框架下──

> **【拓展：离散扩散的统一优势】**离散扩散将文本生成和图像生成统一到同一个数学框架 () 掩码代币 预测), fazendo o treinamento conjunto de vários modelos mais simples.


### Dispersão discreta mascarada (MaskGIT)

O truque original Chang et al. (2022) MaskGIT é elegante. Comece com uma imagem totalmente mascarada (cada token é o especial `<MASK>`Em cada etapa, prevê todos os tokens mascarados em paralelo, em seguida, mantenha as previsões mais confiantes do top-K e re-mascarar o resto. Após ~ 8-16 iterações, todos os tokens são preenchidos. O cronograma de quantos tokens desmascarar por etapa é sintonizado.

> O original Chang 等人(2022) MasksGIT 技巧很优雅──从完全掩码的图像开始(cada token 都是特殊的`<MASK>`ID) ・ por cada passo e fazer a previsão de todos os tokens de mascaragem, e então manter o top-K 最有信心的预测并重新掩掩其他的──

O treinamento é simples: amostrar uma proporção de mascaramento uniformemente a partir de [0, 1], aplicá-lo aos tokens VQ da imagem, treinar o transformador para recuperar os mascarados.

> 訓練很簡單: desde [0, 1] 均采样掩码比例, aplicado a imagem de VQ token, 訓練 變形器 恢复被掩码的 token──就是BERT对文本做,扩展到图像生成──

### Show-o: um transformador, máscara híbrida

O show-o coloca o MaskGIT dentro de um transformador de modelo de linguagem causal.

> Show-o vai colocar MaskGIT 放入因果语言模型 Transformer 中──注意力掩码是:

- Tokens de texto: causal (MLL padrão).
  Tradução do inglês:
- Tokens de imagem: bidirecionais completos dentro do bloco de imagem (para que os tokens mascarados possam ver todos os outros tokens de imagem durante a previsão).
  O símbolo de imagem pode ser visto durante a previsão.
- Texto-a-imagem: texto atende às imagens anteriores, imagem atende ao texto anterior.
  Tradução do inglês:文本到图像:文本关注之前的图像,图像关注之前的文本──

Formação alternada entre:
1. NTP padrão em sequências de texto.
   Tradução do inglês: Standard NTP on文本序列
2. T2I amostras: texto → imagem com tokens de imagem mascarados, perda de previsão de tokens mascarados.
   Tradução do inglês:T2I 样本:文本→带掩码图像代币的图像,掩码代币 预测损失──
3. amostras de VQA: imagem → texto com tokens de texto mascarados (na verdade apenas NTP).
   O texto é um símbolo de um texto que é um símbolo de um texto.

A perda unificada é a entropia cruzada em`<MASK>`Tokens, que abrange tanto o texto NTP (apenas o último token é "mascarado") como a difusão mascarada de imagem (subconjunto aleatório é mascarado).

> 统一损失是                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        `<MASK>`token 上的交叉,同时覆盖文本 NTP(apenas o último token é "掩码" de)

### Amostragem paralela

Show-o gera uma imagem em ~16 passos em vez de ~1000 (autoregressivo por token) ou ~20 (difusão). Em cada passo, prevê todos os tokens mascarados em paralelo; comprometa o top-K confiante; repita.

> Show-o em cerca de 16 etapas em produção de imagem, e não cerca de 1000 etapas em cada token auto-regressão) ou cerca de 20 etapas em expansão)

Comparar:
- Chameleon / Emu3 (autoregressivo sobre tokens): N_tokens passes para a frente, normalmente 1024-4096 por imagem.
  中文翻译:Chameleon / Emu3(逐 token 自归归):N_tokens 次前向传播, normalmente每张图像 1024-4096──
- Transfusão (difusão contínua): ~ 20 passos, cada um com um transformer completo.
  Transfusão: Transfusão: 20 步, cada passo de uma vez
- Show-o (difusão discreta mascarada): ~ 16 passos, cada um com passagem de transformador completo.
  Tradução do inglês:Show-o(掩码离散扩散): cerca de 16 步, cada passo uma vez completo Transformer 传播。

O Show-o é mais rápido do que o Chameleon em modelos de escala similar, correspondendo aproximadamente ao número de etapas da Transfusão com menor custo por etapa (logits de vocabulário discreto vs perda contínua de MSE).

> Show-o em modelo de tamanho similar em comparação com o Camelão, mais rápido, passo grande para o mesmo Transfusão, mas cada passo custo menor

### Funções num único ponto de controlo

Show-o suporta quatro tarefas na inferência, selecionadas por formato prompt:

> Show-o em sugestão apoiar quatro tarefas, através de sugestão de forma seletiva:

- Geração de texto: saída de texto autoregressivo padrão.
  中文翻译:文本生成:标准自归文本输出。
- Imagem, mensagem.
  O que é o que é o que é o que é o que é o que é o que é o que é o que é o que é o que é o que é o que é o que é o que é o que é o que é o que é o que é o que é o que é o que é o que é o que é o que é o que é o que é o que é o que é o que é o que é o que é o que é?
- T2I: entrada de texto, saída de imagem através de difusão discreta mascarada.
  Tradução do português:T2I:文本输入,通过掩码离散扩散输出图像──
- Imagem com alguns tokens enmascarados, preencher.
  Chinese:图像修复:带部分掩码 token 的图像,填充缺失部分──

A capacidade de pintura vem gratuitamente do treinamento de previsão mascarada. Mascarar uma região da grade de tokens VQ, alimentar o resto mais um prompt de texto, prever os tokens mascarados.

> 图像修复能力从掩码预测训练中免费获得──掩码 VQ token 网格的一个区域,进入其余部分加上文本提示,预测被掩码的 token──

### Programa de enmascaramento

O cronograma de quantos tokens devem ser desmascarados por passo forma a qualidade.

> Cada passo resolve a quantidade de tokens que influenciam a qualidade.

```
mask_ratio(t) = cos(pi * t / (2 * T))   # t = 0..T
```

No passo 0, todos os tokens são mascarados (ratio 1.0). No passo T, nenhum é mascarado. Cosino concentra massa em proporções de médio alcance onde a previsão é mais informativa.

> 第 0 步, todos os tokens 被掩码(比例 1.0) ――第 T 步,无掩码──余弦调度将质量集中在中程比例上,此时预测信息量最大──线性调度也可用但更早和──

### - O2

Show-o2 (2025 acompanhamento, arXiv 2506.15564) escalas Show-o: maior base de LLM, melhor tokenizer, melhor cronograma de máscara.

### Onde o Show-o está sentado

Na taxonomia de 2026:

> Em 2026 ano:

- Tokens discretos + NTP: camaleão, Emu3.
  中文翻译:离散代币 + NTP:Chameleon、Emu3──简单但推理慢──
- Tokens discretos + difusão mascarada: Show-o, MaskGIT, LlamaGen, Muse. Amostração paralela, ainda perdida pelo tokenizer.
  O que é que você está fazendo?
- Transfusão contínua + difusão: Transfusão, MMDiT, DiT. Formação de alta qualidade, mais complexa.
  Tradução do português:连续 + 扩散:Transfusion、MMDiT、DiT──最高质量,训练更复杂──
- Combinação contínua + fluxo em um VLM: JanusFlow, InternVL-U. Mais recente.
  中文翻译:VLM 中连续 + 流匹配:JanusFlow、InternVL-U──最新──

Selecionar por tarefa: Show-o quando quiser T2I + inpainting + VQA em um modelo aberto com velocidade razoável; Transfusão quando a qualidade é primordial e você pode pagar a canalização de duas perdas.

> 按任务选择: necessita de um modelo aberto simultaneamente fazer T2I + 修复 + VQA 且速度合理时选 Show-o;质量至上且能承担双损失复杂性时选 转移――


> **【拓展：Show-o 的离散扩散方法】**Show-o de separação de expansão usando escondido previsão:随机遮盖部分 token,模型预测被遮盖的 token──理解任务遮盖答案部分,生成任务从全遮盖开始逐步到噪声──数学上等价于多项式扩散──


## Use-o em prática.
```figure
masked-diffusion-unmask
```

## Usá-lo

`code/main.py`Simula a amostragem de show-o:

> `code/main.py`模拟 Show-o 采样:

- Uma grade de brinquedos de 16 tokens VQ.
  Chinese: 16 个VQ token 的玩具网格.
- Um falso "transformador" que prevê logits com base em um prompt e os tokens atualmente desmascarados.
  中文翻译:一个模拟"Transformer",基于提示和当前未掩码 token 预测 logits。
- Amostragem paralela mascarada em 8 etapas com cronograma cosínico.
  O que é um "show" de um personagem?
- Imprime os estados intermediários (evolução de padrão de máscara) e os tokens finais.
  O que significa que o sistema de controle de dados é um sistema de controle de dados?

- É melhor. - Vamos, vamos.

> Operar, observar mascarar o problema.

## Envia-o .

Esta lição produz`outputs/skill-unified-gen-model-picker.md`. Tendo em conta um produto que necessita de compreensão (VQA, subtítulos) e geração (T2I, inpainting) com restrições de peso aberto, escolha entre a família Show-o, a família Transfusion/MMDiT e a família Emu3/Chameleon com compensações concretas.

> 本课产 出 `outputs/skill-unified-gen-model-picker.md`△给定需要理解(VQA、描述) 和生成(T2I、修复) 和限开权重的产品,在 Show-o、Transfusion/MMDiT 和 Emu3/Chameleon 家族之间选择,附具体权衡──

## Exercícios.

1. Mascaradas amostras de difusão discreta em ~16 passos. Por que não 1? O que se rompe se você desmascarar tudo no passo 0?
   Mas, por que não um passo? Se em um passo resolver todos os tokens, o que acontecerá?

2. A pintura é gratuita com difusão mascarada. Propõe um caso de utilização do produto (real ou hipotético) em que a pintura do Show-o seja superior a um modelo especializado.
   Tradução do inglês para tradução do inglês:掩码扩散的图像修复是免费的――提出一个展示修复能力胜过专业模型的产品用例――

3. Calendário cosínico vs calendário linear: rastrear o número de tokens desmascarados por passo para T=8. Qual é mais equilibrado?
   Tradução do inglês: 余弦调度 vs 线性调度: 追踪 T=8 时每步解掩码的符号 数――哪个更平衡?

4. Uma imagem de 512x512 Show-o é de 1024 tokens. Na vocab K = 16384, o modelo emite 1024 * log2(16384) = 14.336 bits (~ 1,75 KiB) de dados.
   O modelo de produção é de aproximadamente 1,75 KiB dados, SD, 768 KiB de imagens, compressão é de quanto?

5. Leia LlamaGen (arXiv:2406.06525). Como o modelo de imagem autoregressiva condicional de classe do LlamaGen é diferente da abordagem mascarada do Show-o?
   Chinese: 阅读 LlamaGen(arXiv:2406.06525) ―― Qual a diferença entre os termos de classificação de LlamaGen e o método de esconde de Show-o?

## Termos-chave .

| Term | What people say | What it actually means | 中文含义 | 中文释义 |
|------|-----------------|------------------------|---------|
| Masked discrete diffusion | "MaskGIT-style" | Training to predict masked tokens; at inference, iteratively unmask the most-confident predictions | 训练预测掩码 token；推理时迭代解掩码最有信心的预测 |
| Cosine schedule | "Unmask schedule" | Decay of mask ratio over inference steps; concentrates confidence growth at mid-range | 推理步骤中掩码比例的衰减；将信心增长集中在中程 |
| Parallel decoding | "All tokens at once" | Every step predicts the full sequence of masked tokens in one forward pass, then commits top-K | 每步在一次前向传播中预测所有掩码 token，然后提交 top-K |
| Hybrid attention | "Causal + bidirectional" | Mask that is causal over text tokens and bidirectional within image blocks | 文本 token 因果、图像块内双向的掩码 |
| Inpainting | "Fill-in generation" | Condition on an image with some tokens masked, predict the missing ones; free from the training objective | 以部分掩码图像为条件，预测缺失 token；从训练目标免费获得 |
| Commitment rate | "Top-K per step" | How many tokens are declared "done" per iteration; controls inference vs quality trade-off | 每次迭代声明"完成"的 token 数；控制推理与质量的权衡 |

## Mais leitura 延伸阅读

- [Xie et al. — Show-o (arXiv:2408.12528)](https://arxiv.org/abs/2408.12528)
  O que é que é o que é o que é o que é o que é o que é o que é o que é o que é o que é o que é o que é o que é o que é o que é o que é o que é o que é o que é o que é o que é o que é o que é o que é o que é o que é o que é o que é?
- [Show-o2 (arXiv:2506.15564)](https://arxiv.org/abs/2506.15564)
  Tradução do português:Show-o2
- [Chang et al. — MaskGIT (arXiv:2202.04200)](https://arxiv.org/abs/2202.04200)
  MascGIT 论文,掩码离散扩散的原始工作──
- [Sun et al. — LlamaGen (arXiv:2406.06525)](https://arxiv.org/abs/2406.06525)
  Tradução do inglês:LlamaGen
- [Chang et al. — Muse (arXiv:2301.00704)](https://arxiv.org/abs/2301.00704)
  Muze 掩码图像生成──
