# Recetas de VLM em peso aberto: o que realmente importa

> A literatura VLM de peso aberto 2024-2026 é uma floresta de tabelas de ablação. O MM1 da Apple testou 13 combinações de codificador de imagem, conector e mix de dados. O Molmo de Allen AI provou que as legendas humanas detalhadas superam a destilação GPT-4V. Cambrian-1 fez mais de 20 comparações de codificadores. Idefics2 formalizou o espaço de design de cinco eixos. Os VLMs prismáticos compararam 27 receitas de formação em um índice de referência controlado. De todo esse barulho, um pequeno conjunto de resultados é válido em todos os papéis: o codificador de imagem importa mais do que a arquitetura do conector, a mistura de dados importa mais do que qualquer um dos dois, e as legendas humanas detalhadas superam os dados sintéticos destilados. Esta lição lê essas tabelas para que não tenha de ler.

> **【中文解读】**O estudo de 2024-2026 foi publicado em um artigo de revisão de um estudo de revisão de dados sobre o desenvolvimento de um sistema de gestão de dados (VLM) com base no artigo de revisão de revisão de dados (VLM) de 2024-2026 .

> **【拓展：VLM 工程的实践指南】**Os resultados deste curso orientam diretamente a prática de engenharia VLM. Quando você descobrir que o VLM não alcança o seu nível de desempenho, deve ser classificado em conformidade com as seguintes prioridades: 1) o número de tokens visuais é suficiente para o sistema de dados (%) (%) (%) (%) (%) (%) (%) (%) (%) (%) (%) (%) (%) (%) (%) (%) (%)), (%) (%) (%) (%) (%) (%) (%) (%) (%) (%) (%) (%) (%) (%) (%) (%) (%) (%) (%) (%) (%) (%) (%) (%) (%) (%) (%) (%) (%) (%) (%) (%) (%) (%) (%) (%) (%) (%) (%) (%) (%) (%) (%) (%) (%) (%) (%) (%) (%) (%) (%) (%) (%) (%) (%) (%) (%) (%) (%) (%) (%) (%) (%) (%) (%) (%) (%) (%)) (%) (%) (%) (%) (%) (%)) (%) (%) (%) (%) (%)) (%) (%) (%)) (%) (%) (%) (%)) (%) (%)) (%) (%)) (%) (%) (%)) (%) (%)) (%) (%)) (%) (%)) (%) (%)) (%) (%)) (%)) (%) (%)) (%) (%)) (%)) (%) (%)) (%)) (%) (%)) (%)) (%)) (%) (%)) (%)) (), (%) (%) (%) (%)) (%)) (%) (%)) (%)) (%) (%)) (%)) (), (%) (%) (%)) (%) (%)) (%)) (), (%) (%)) (%) (%) (%)) (%)) (%) (%)) (%) (%)) (%)) (), (%) (%) (%)) (%)) (%)) (%)) (), (%) (%) (%) (%)) (%)) (%) (%)) (%)) (), (%)) (%) (%) (%)) (%)) (%)) (), (%) (%) (%)) (%)) (%) (%)

**Type:** Learn + lab  | **类型：学习 + 实验**
**Languages:** Python (stdlib, ablation table parser + recipe picker)  | **语言：Python（标准库，消融表解析器 + 配方选择器）**
**Prerequisites:** Phase 12 · 05 (LLaVA baseline)  | **前置：阶段12第05课（LLaVA基线）**
**Time:** ~180 minutes  | **时长：约180分钟**

> - Não .**【前置】**O primeiro é o primeiro, o segundo é o segundo, o segundo é o segundo. O segundo é o segundo.
> - Não .**【类比】**开源 VLM 五轴选择 = "买车选配置"──编码器 = 发动机(персона差 5-7 分);连接器 = 中控台界面(几乎不影响驾驶);LLM = 车身大小;数据 = 油品(差油再好的发动机也跑不快);分辨率 = 轮胎(决定能跑什么地形)──纠结界面(连接器) é uma nova armadilha, os antigos motoristas priorizam o desenvolvimento de máquinas e óleos。

## Objetivos de aprendizagem

- Nomear o espaço de design VLM de cinco eixos: codificador de imagem, conector, LLM, mix de dados, cronograma de resolução.
- Leia uma tabela de ablação MM1 / Idefics2 / Cambrian-1 e prevê qual botão move um determinado índice de referência.
- Escolha uma receita (encodor, conector, dados, resolução) para um novo VLM dado um orçamento computacional e mistura de tarefas.
- Explica por que as legendas humanas detalhadas superam a destilação GPT-4V na mesma contagem de tokens.

## O problema é o contexto do problema .

Há centenas de VLMs de peso aberto. A maior parte da diferença entre "bom" e "estado-de-arte" não é arquitetura. É dados, cronograma de resolução e escolha de codificador. Saber qual botão girar primeiro quando seu modelo não funciona melhor salva-lhe um erro de 5 milhões de GPUs.

A onda de 2023 (LLaVA-1.5, InstructBLIP, MiniGPT-4) correu em pre-treino de par de captura + LLaVA-Instruct-150k. Boa linha de base.

A onda 2024 (MM1, Idefics2, Molmo, Cambrian-1, Prismatic VLMs) teve ablações exaustivas.

> **【中文解读】**Em algumas centenas de VLMs de código aberto, a diferença entre "bom" e "melhor" não é principalmente a estrutura, mas sim os dados, a resolução de ajustes e a seleção de codificadores.

## O conceito central.

### O espaço de design de cinco eixos.

Idefics2 (Laurençon et al., 2024) nomeou os eixos:

1. Encoder de imagem / 图像编码器. CLIP ViT-L/14, SigLIP SO400m/14, DINOv2 ViT-g/14, InternViT-6B. Encoder diferem em tamanho de parcheiro, resolução e objetivo de pré-treino / 编码器在补丁大小、分辨率和预训目标上各不相同.
2. Conector / 连接器. MLP (2-4 camadas), Q-Former (32 consultas + cross-attn), Perceptor Resampler (64 consultas), C-Abstractor (convolucional + bilinear pooling) / MLP(2-4层)、Q-Former(32查询+交叉注意力)、Perceptor 重采样器(64查询)、C-Abstractor(卷积+双线性池化).
3. Modelo de linguagem / 语言模型. Llama-3 8B / 70B, Mistral 7B, Phi-3, Gemma-2, Qwen2.5.
4. Dados de treinamento / 训练数据. pares de legendas (CC3M, LAION), entrelaçados (OBELICS, MMC4), instrução (LLaVA-Instruct, ShareGPT4V, PixMo, Cauldron) / 描述对、交错数据、指令数据.
5. Calendário de resolução / resolução de resolução. Fixa 224/336/448, AnyRes, dinâmica nativa. Ramped durante o treinamento ou constante / 固定分辨率、AnyRes、原生動态分辨率── treinamento em cada passo ou恒定.

Cada VLM de produção faz uma escolha em cada eixo. A maior parte da variação nas pontuações do MMMU é explicada pelos eixos 1, 4 e 5  não pelo conector escolhido.

> **【中文解读】**Cada VLM é feito em cinco eixos. A maior parte do número de MMMU é dividido em eixos1 (axis4 (axis4) e axis5 (axis5 (axis5)).

### Exi 1: Encoder > Conector

MM1 Secção 3.2 mostrou: trocar de CLIP ViT-L/14 para SigLIP SO400m/14 adicionou 3 pontos MMMU. trocar o conector de MLP para Perceptor Resampler adicionou menos de 1 ponto. Idefics2 replicado: SigLIP > CLIP, Q-Former ≈ MLP ≈ Perceptor na mesma contagem de tokens.

Cambrian-1 "Cambrian Vision Encoders Match-Up" (Tong et al., 2024) executou 20 + codificadores em um benchmark centrado na visão (CV-Bench).

O codificador padrão 2026 para VLMs abertos é SigLIP 2 SO400m/14 para recursos semânticos + densos, às vezes concatenado com recursos DINOv2 ViT-g/14 (o "Aggregador de Visão Espacial" de Cambrian faz isso).

> **【中文解读】**换编码器(CLIP→SigLIP)加3+ 分 MMMU,换连接器(MLP→Perceptor)加不到1分──2026年开源 VLM 的默认编码器是SigLIP 2 SO400m/14,有时与DINOv2 ViT-g/14 拼接(Cambrian 的"空间视觉聚合器"就是这样做的)──

> ️ **【易错点】**Novos usuários estão sempre em perigo de "reconstruir uma rede de rede" que pensam que o Q-Former é melhor que o que vale a pena pesquisar.

### O design do conector é um lavagem.

MM1, Idefics2, Prismatic e MM-Interleaved todos chegaram à mesma conclusão: em uma contagem fixa de tokens visuais, a arquitetura do conector dificilmente importa.

O que importa é a contagem de tokens. Mais tokens visuais = mais computação LLM = melhor desempenho até um ponto, em seguida, retorno diminuindo. 64 tokens por imagem é muito pouco para OCR. 576-1024 tokens é o ponto ideal para a maioria dos VLMs abertos. 2048+ ajuda apenas para documentos e gráficos.

Q-Former vs MLP é uma questão de custo, não uma questão de qualidade: Q-Former limita os tokens em 32-64 independentemente da resolução da imagem; MLP emite todos os tokens de parche. Para entradas de alta resolução, Q-Former salva contexto LLM; para baixa resolução, a diferença é ruído.

> **【中文解读】**Em números de tokens de visão fixa, a arquitetura do conector quase não afeta o desempenho. 2 níveis MLP e 32 consultas Q-Former diferença é de 1 por cento.

### E o número três é o número de pessoas que estão no limite.

O duplicado do LLM de 7B para 13B adiciona de forma confiável 2-4 pontos sobre o MMMU em cada documento VLM. Em 70B você satura a maioria dos referências.

É por isso que Qwen2.5VL-72B e Claude Opus 4.7 esmagam MMMU-Pro e ScreenSpot-Pro: o cérebro linguístico é enorme. Um VLM 7B não pode substituir um VLM 70B através de um design inteligente de conector.

> **【中文解读】**LLM 翻倍(7B→13B) 稳定增加 2-4 分 MMMU──70B 时大多数基准和──VLM 的多模态推理天花板就是LLM 的文本推理天花板视觉编码器只能""数据,不能取代推理──这就是为什么72B 参数的VLM 能压7B 的语言大脑的规模不可替代的原因──

### Exi 4: dados  detalhes de legendas humanas superam a destilação DATA:

Molmo + PixMo (Deitke et al., 2024) é o resultado 2024 que todos devem ler. Allen AI teve anotadores humanos descrevendo imagens em passes de fala a texto de 1-3 minutos densos, produzindo imagens de 712K de legendas densas.

Molmo-72B venceu Llama-3.2-90B-Vision em 11 de 11 benchmarks. O delta não é arquitetura  é qualidade de legendas.

ShareGPT4V (Chen et al., 2023) e Cauldron (Idefics2) seguiram o mesmo manual de jogo com legendas misturadas de humanos + GPT-4V. A tendência é clara: para a fronteira de 2026, densidade de legendas > quantidade de legendas > conveniência de destilação.

> **【中文解读】**O principal descoberto de Molmo: fazer com que os marcadores humanos usem imagens de descrição de voz de 1-3 minutos, obtendo imagens de 712K de alta qualidade, completamente sem usar o GPT-4V 蒸── Molmo-72B derrotou o Llama-3.2-90B-Vision em 11/11 基准.

> **【拓展：数据质量的投资回报】**Esta descoberta tem uma importante inspiração para a construção vertical do VLM: com o seu gasto de grande quantidade de capacidade de cálculo para modificar a estrutura, não é como investir recursos para obter dados de alta qualidade em um campo.

### Eixo 5: resolução e seu horário, resolução e sua regulação.

As ablações do Idefics2: 384 -> 448 adiciona 1-2 pontos. 448 -> 980 com divisão de imagem (AnyRes) adiciona mais 3-5 em benchmarks OCR. Planícies de treinamento de resolução plana com precisão média; rampa de resolução (começa 224, termine 448 ou nativo) trens mais rápido e termina mais alto.

Cambrian-1 executou uma troca de resolução versus tokens: em computação fixa, você pode ter mais tokens com resolução menor ou menos tokens com resolução maior. Resolução maior ganha para OCR; menor-resolução-mais-tokens ganha para compreensão geral de cena.

A receita de produção para 2026: treinar a fase 1 a 384 fixas, a fase 2 com resolução dinâmica até 1280 para tarefas pesadas em OCR.

> **【中文解读】**Resolução aumentada de 384  升升至448 加 1-2 分,448 加 980 加 AnyRes) em OCR 基准再加 3-5 分──分辨率增调度(de 224 开始,到 448 或原生分辨率结束) treino mais rápido、 resultados melhores──

### A comparação controlada de Prismatic contra a experiência

Prismatic VLMs (Karamcheti et al., 2024) é o artigo que controlava todos os eixos.

- O número de tokens visuais por imagem explica 60% da variação.
- A escolha do codificador explica ~20%.
- A arquitetura de conectores explica ~5%.
- Tudo o resto (mix de dados, cronógrafo, LR) o restante ~15%.

Esta é uma decomposição grosseira, mas é a resposta mais limpa à pergunta "o que devo abater primeiro" na literatura.

> **【中文解读】**Os VLMs prismáticos são os mais puros de controle experimental o mesmo 13B LLM o mesmo instrução dados a mesma avaliação, cada vez apenas mudar um eixo conclusão:

### Um selector para 2026

Dadas as evidências, a receita padrão de VLM aberto para um novo projeto em 2026:

- Encoder / 编码器: SigLIP 2 SO400m/14 em resolução nativa com NaFlex, concatenado com DINOv2 ViT-g/14 para recursos densos se você precisar de segmentação / grounding / 如需分割/定位则拼接 DINOv2.
- Conector / 连接器: MLP de 2 camadas em tokens de correção. Salte Q-Former a menos que você esteja com restrição de token / 除非 token 受限否则跳过 Q-Former.
- LLM / 语言模型: Qwen2.5 / Llama-3.1 / Gemma 2, 7B para custo / 成本优先选7B, 70B para qualidade / 质量优先选70B, escolhido por latência-alvo / 按延迟目标选择.
- Dados / dados: PixMo + ShareGPT4V + Cauldron, complementado com dados de instrução específicos de tarefas / 补充任务特定指令数据.
- Resolução / 分辨率: dinâmica (min 256, max 1280 pixels por lado longo) / 动态(minimum256,最大1280像素每长边).
- Orçamento / 调度: Alinhamento de estágio 1 (apenas projeto / 仅投影器), estágio 2 de ajuste fino completo / 全参数微调, estágio 3 de ajuste fino específico de tarefa / 任务特定微调.

Cada uma dessas falhas remonta a uma ablação medida nos artigos citados no final desta lição.

> **【中文解读】**Os resultados de cada uma das opções preferidas podem ser traçados para os resultados do experimento de dissi­mimento citado neste artigo.

## Use-o em prática.
```figure
l5-vlm-recipe-knobs
```

## Usá-lo

`code/main.py`É um analisador de tabelas de ablação e selecionador de receitas.

- "Dado o orçamento X e a tarefa Y, qual receita ganha?"
- "Se eu trocar SigLIP por CLIP em um Llama 7B, qual é o delta esperado de MMMU?"
- "Qual eixo devo ablacionar primeiro para uma resposta de 80% de confiança?"

A saída é uma lista de receitas classificada com delta de referência esperada e uma recomendação de "ablate first".

## Envia-o .

Esta lição produz`outputs/skill-vlm-recipe-picker.md`. Dada uma combinação de tarefas-alvo, um orçamento de computação e uma meta de latência, emite uma receita completa (encoder, conector, LLM, mix de dados, cronograma de resolução) com citações da ablação que justifica cada escolha.

> **【中文解读】**Este curso é elaborado por um grupo de engenheiros que trabalham em projetos de gestão de recursos humanos e de gestão de recursos humanos.

## Exercícios.

1. Leia MM1 Secção 3.2. Para um LLM fixo 2B com orçamento 50M imagens, qual codificador ganha?
   | 阅读 MM1 第 3.2 节。在固定 2B LLM 和 50M 图像预算下，哪个编码器最优？在 13B LLM 时答案会翻转吗？为什么？

2. Cambrian-1 constata que a concatenagem DINOv2 + SigLIP supera a performance de uma só vez em referências centrais na visão, mas não adiciona sinal na MMMU.
   | Cambrian-1 发现 DINOv2+SigLIP 拼接在视觉中心基准上优于单独使用，但在 MMMU 上无增益。预测哪些基准提升、哪些持平。

3. O seu alvo é um agente de interface móvel em um 2B LLM. Escolha o codificador, conector, resolução e mix de dados. Justifique cada escolha com uma tabela de ablação específica.
   | 目标是在 2B LLM 上构建移动端 UI 代理。选择编码器、连接器、分辨率和数据混合，用具体消融表论证每个选择。

4. Molmo navega modelos 4B e 72B. O 4B é competitivo com 7B VLMs fechados; o 72B vence Llama-3.2-90B-Vision em 11/11 benchmarks. O que isso diz sobre a hipótese de plato de tamanho LLM?
   | Molmo 的 4B 模型与闭源 7B VLM 竞争力相当；72B 在 11/11 基准上击败 Llama-3.2-90B-Vision。这对 LLM 规模饱和假说意味着什么？

5. Desenhar uma tabela de ablação para isolar a qualidade da mistura de dados da qualidade do codificador em um VLM 7B. Quantas corridas de treinamento mínimas? Proporcionar as quatro configurações de eixos.
   | 设计消融实验表，在 7B VLM 上隔离数据混合质量和编码器质量。最少需要多少次训练？提出四组轴设置。

## Termos-chave .

| Term | What people say | What it actually means | 中文含义 | 中文释义 |
|------|-----------------|------------------------|----------|---------|
| Ablation | "Turning one knob" | Training multiple runs that differ in exactly one design-space axis, holding everything else constant | 消融实验：只改变一个设计轴、保持其他不变的多组训练 | |
| Connector | "Bridge" / "projector" | Trainable module that maps vision encoder output into the LLM's token space (MLP, Q-Former, Perceiver) | 连接器：将视觉编码器输出映射到 LLM token 空间的可训练模块 | |
| Detailed human caption | "Dense caption" | A multi-sentence human-written description (typically 80-300 tokens) richer than a web alt text | 详细人工描述：人类编写的多句描述（通常80-300 token） | |
| Distillation | "GPT-4V captions" | Training data generated by a stronger proprietary VLM; convenient but prone to inherited hallucination | 蒸馏：用更强的专有 VLM 生成训练数据；方便但会继承幻觉 | |
| AnyRes / dynamic res | "High-res path" | Strategy to feed images larger than the encoder's native resolution via tiling or M-RoPE | AnyRes/动态分辨率：通过切片或 M-RoPE 处理超过编码器原生分辨率的图像 | |
| Resolution ramp | "Curriculum" | Training schedule that starts low-resolution and increases, speeding alignment learning | 分辨率递增：从低分辨率开始逐步增加的训练调度 | |
| Vision-centric bench | "CV-Bench / BLINK" | Evaluation that stresses fine-grained visual perception rather than language-heavy reasoning | 视觉中心基准：测试精细视觉感知能力而非语言推理 | |
| PixMo | "Molmo's data" | Allen AI's 712K densely-captioned image dataset; human speech transcribed into dense captions | Allen AI 的 712K 密集标注图像数据集；人工语音转录为密集描述 | |

## Mais leitura 延伸阅读

- [McKinzie et al. — MM1 (arXiv:2403.09611)](https://arxiv.org/abs/2403.09611)Apple MM1 Multi-modelo modelo de experimentação de fusão
- [Laurençon et al. — Idefics2 / What matters building VLMs (arXiv:2405.02246)](https://arxiv.org/abs/2405.02246)Factor-chave para construir VLM
- [Deitke et al. — Molmo and PixMo (arXiv:2409.17146)](https://arxiv.org/abs/2409.17146)Molmo e PixMo
- [Tong et al. — Cambrian-1 (arXiv:2406.16860)](https://arxiv.org/abs/2406.16860)∙ Cambrian-1 + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + +
- [Karamcheti et al. — Prismatic VLMs (arXiv:2402.07865)](https://arxiv.org/abs/2402.07865)O VLM Prismático controla a experiência de desintegração
