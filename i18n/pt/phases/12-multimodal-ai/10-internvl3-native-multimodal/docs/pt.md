# InternVL3: Pré-treinamento Multimodal Nativo

> Todos os VLM abertos antes do InternVL3 seguiram a mesma receita de três passos: pegue num texto LLM treinado em trilhões de tokens de texto, aperte um codificador de visão, e depois ajuste as costuras. O texto LLM gastou todo o seu orçamento pré-treino em texto puro e não entende nativamente os tokens visuais. Quando adicionar a visão post-hoc, o LLM tem que reaprender a relacionar a entrada visual ao seu raciocínio do texto sem esquecer o texto. O InternVL3 (Zhu et al., abril 2025) rejeita a abordagem pós-hoc: uma corrida pré-treino, texto e multimodal interligados a partir do primeiro passo. O resultado coincide com o Gemini 2.5 Pro no MMMU-Pro com 78B params abertos. Esta lição diz o caso do pré-treino nativo e o que muda quando o fizer.

> **【中文解读】**A inovação central do InternVL3 é a rejeição do "pré-trainamento do texto LLM Reconectar o vídeo codificador" no programa de formação, transformado de um primeiro passo para um treino de texto e de dados de vários modos.

> **【拓展：原生预训练 vs 后装的成本权衡】**O pre-conceito de vida original eliminou a dívida total, mas o custo é muito maior do que o pre-conceito de vida real.

**Type:** Learn  | **类型：学习**
**Languages:** Python (stdlib, training-corpus mixer)  | **语言：Python（标准库，训练语料混合器）**
**Prerequisites:** Phase 12 · 05, Phase 12 · 07 (recipes)  | **前置：阶段12第05课、阶段12第07课（配方）**
**Time:** ~120 minutes  | **时长：约120分钟**

> - Não .**【前置】**O curso de formação em formação em formação em formação em formação em formação em formação em formação em formação em formação em formação em formação em formação em formação em formação em formação em formação em formação em formação em formação em formação em formação em formação em formação em formação em formação em formação em formação em formação em formação em formação em formação em formação em formação em formação em formação em formação em formação em formação em formação em formação em formação em formação em formação em formação em formação em formação em formação em formação em formação em formação em formação em formação em formação em formação em formação em formação em formação em formação em formação em formação em formação em formação em formação em formação em formação em formação em formação em formação em formação em formação em formação em formação em formação em formação em formação em formação em formação em formação em formação em formação em formação em formação em formação em formação em formação em formação em formação em formação em formação em formação em formação em formação em formação em formação em formação em formação em formação em formação em formação em formação em formação em formação em formação em formação em formação em formação em formação em formação em formação em formação em formação em formação em formação em formação em formação em formação em formação em formação em formação em formação em formação em formação em formação em formação em formação em formação em formação em formação em formação em formação em formação em formação em formação em formação em formação em formação em formação em formação em formação em formação em formação em formação em formação em formação em formação em formação em formação em formação em formação em formação em formação em formação em formação em formação em formação em formação em formação em formação em formação em formação em formação em formação em formação em formação em formação em formação em formação em formação em formação em formação em formação em formação em formação em formação em formação em formação em formação em formação em formação em uma.
> - Não .**【类比】**后装 VLM(LLaVA) = "成年后学外语" já aprendeu母语(文本),再艰难学第二语言(视觉) ・・・原生 VLM(InternVL3) = "双语家庭长大"两种语言同时学,没有翻译损耗──后装方案便宜但有口音(对齐债务),原生方案昂贵但流利──
> 🤔 **【困惑】**P: Uma vez que o treinamento de pre-vida original é tão bom, por que o LLaVA continua a ser o principal?

## Objetivos de aprendizagem

- Explique por que o treinamento pós-hoc de VLM acumula dívidas de alinhamento, citando os três sintomas mensuráveis (esquecimento catastrófico, deriva de resposta, inconsistência visual-texto).
- Descreva a mistura de corpus de pré-treino nativo do InternVL3 e por que a proporção de texto: interligado: subtítulo importa.
- Compare V2PE (codificação de posição visual variável) com M-RoPE do Qwen2-VL.
- Nomear o Router de Resolução Visual (ViR) e as optimizações de implantação de Língua de Visão Desacoplada (DvD).

## O problema é o contexto do problema .

O treinamento pós-hoc é o padrão. LLaVA, BLIP-2, Qwen-VL, Idefics  todos tomam um LLM já treinado (Llama, Vicuna, Qwen, Mistral) e adicionam visão.

1. Mestrado em Mestrado em Física + codificador de visão congelado + projetor treinável, treinado em pares de legendas para alinhar as incorporações.
2. Desbloquear o LLM, treinar em dados de instrução (LLaVA-Instruir, ShareGPT4V).
3. Opcional, precisão específica de tarefa.

Três sintomas da dívida de alinhamento aparecem:

- O VLM pós-hoc esquece habilidades apenas de texto. As pontuações GSM8K caem 5-10 pontos. As pontuações Hellaswag caem. Agentes de texto puro regressam.
- Responder deriva / 回答漂移. Pequenas frases da mesma pergunta visual recebem respostas diferentes. O codificador de visão se conecta ao LLM com ligações mais fracas do que os próprios tokens do LLM.
- Incoerência visual-textual / 视觉-文本不一致. O VLM pode descrever uma imagem corretamente e, em seguida, responder a uma pergunta contradizendo sua própria descrição. Tokens visuais não participam das verificações internas de consistência do LLM da mesma forma que o texto faz.

> **【中文解读】**后装 VLM's Three Forward Debt:(1) 灾难性遗忘GSM8K 掉 5-10 分;(2) 回答漂移 漂移 漂移 漂移 漂移 漂移 漂移 漂移 漂移 漂移 漂移 漂移 漂移 漂移 漂移 漂移 漂移 漂移 漂移 漂移 漂移 漂移 漂移 漂移 漂移 漂移 漂移 漂移 漂移 漂移 漂移 漂移 漂移 漂移 漂移 漂移 漂移 漂移 漂移 漂移 漂移 漂移 漂移 漂移 漂移 漂移 漂移 漂移 漂移 漂移 漂移 漂移 漂移 漂移 漂移 漂移 漂移 漂移 漂移 漂移 漂移 漂移 漂移 漂移 漂移 漂移 漂移 漂移 漂移 漂移 漂移 漂移 漂移 漂移 漂移 漂移 漂移 漂移 漂移 漂移 漂移 漂移 漂移 漂移 漂移 漂移 漂移 漂移 漂移 漂移 漂移 漂移 漂移 漂移 漂移 漂移 漂移 漂移 漂移 漂移 漂移 漂移 漂移 漂移 漂移 漂移 漂移 漂移 漂移 漂移 漂移 漂移 漂移 漂移 漂移 漂移 漂移 漂移 漂移

## O conceito central.

### Pre-treino nativo multimodal

InternVL3 treina a partir do zero em um corpus que é nativo multimodal a partir do primeiro passo.

- 40% de dados apenas de texto (FineWeb, Proof-Pile-2, etc.) / 40% 纯文本数据
- 35% de dados de imagem-texto entrelaçados (OBELICS, estilo MMC4) / 35% 交织图文数据
- 20% de dados de imagem em par / 20% 图文配对数据
- 5% dados de vídeo-texto / 5% 视频文本数据

Tokens de visão, tokens de texto e interações transmodais participam da mesma perda desde o primeiro passo do gradiente.

O modelo base é uma fase única, seguindo-se a sintonia de instruções, mas o modelo base já entende os tokens visuais como cidadãos de primeira classe.

> **【中文解读】**InternVL3 desde o primeiro passo em relação a um token de visão, texto e um token de forma transmodelo, entrar na mesma função de perda. Não é necessário um treinamento de preparação, não é necessário um projeto, não é necessário uma recuperação do esquecimento de catástrofe.

### V2PE (codificação de posição visual variável)

O Qwen2-VL utiliza M-RoPE com alocação de eixo fixo. InternVL3 introduz V2PE: a codificação de posição varia por tipo de modalidade (texto, imagem, vídeo) com escalabilidade apropriada.

- Tokens de texto obtêm posição 1D (index de texto).
- Os patches de imagem obtêm posição 2D (linha, col).
- Os quadros de vídeo têm posição 3D (tempo, linha, col).

Os três compartilham a mesma base de frequência RoPE, mas a alocação de dim oculta por banda é um parâmetro aprendido em vez de uma divisão fixa.

A afirmação de ablação do V2PE: 1-2 pontos em benchmarks de vídeo sobre M-RoPE no mesmo cálculo.

> **【中文解读】**Diferença entre V2PE e M-RoPE: a dimensão oculta é distribuída entre os diferentes frequências, sendo que os parâmetros são leváveis e não divididos. O modelo pode medir automaticamente o tempo e a frequência espacial no processo de treinamento preliminar.

### Roteador de resolução visual (ViR)                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                   

Optimização de implantação. Nem todas as imagens precisam de codificação em resolução completa. Uma foto com um objeto em baixo detalhe desperdiça tokens quando codificada em 1280px nativo. ViR é um pequeno classificador que prevê a resolução mínima necessária para responder à pergunta, antes de codificar.

O roteamento tem três níveis: baixa resolução (256 tokens), média (576), alta (2048+). Para 60% das consultas no tráfego de produção, baixa ou média é suficiente. Efeito líquido: 2-3x de transmissão em qualidade igual.

> **【中文解读】**ViR é implementado de forma optimista: uma pequena classificação de um sistema de codificação de pré-previsão com a menor resolução necessária para uma consulta.

> **【拓展：ViR 与金融场景】**No tratamento de arquivos financeiros, a maior parte das consultas (como "o montante total do emissão é quanto") necessitam apenas de baixa resolução, mas as tarefas de OCR (como "Tirar todos os projetos") necessitam de alta resolução.

### Desacoplado de implantação de linguagem de visão (DvD) 解视觉-语言部署

Quando você serve um grande VLM, o codificador de visão é executado uma vez por imagem, mas o LLM é executado autoregressivamente para cada token de saída. Os dois componentes têm gargalos de engarrafamento diferentes (visão = largura de banda de memória da GPU para conv + atenção; LLM = cache KV).

Para um modelo de codificador 8B + 400M, DvD aproximadamente dobrar a capacidade de transmissão por nó versus co-localizado.

> **【中文解读】**O DVD irá distribuir o vídeo e o LLM em diferentes GPUs, através de ligações de transmissão de fluxo.

### Qualidade de uma fase versus uma de várias etapas

A principal referência de InternVL3 é: em 78B params, coincidem com o MMMU-Pro do Gemini 2.5 Pro. Em 38B, coincidem com o GPT-4o. Em 8B, liderem o ranking de 8B aberto. Tudo em uma receita de preparação de um único estágio + instrução-tune.

A hipótese de dívida de alinhamento é mensurável: o InternVL3-8B perde menos pontos de referência de texto (MMLU, GSM8K) do que o Qwen2.5-VL-7B por unidade de ganho de referência de visão.

> **【中文解读】**InternVL3-8B Cada obtenção de um visual base de pontuação de aumento, perda de texto base de pontuação de Qwen2.5-VL-7B menor.

### InternVL3.5 e InternVL-U

O InternVL3.5 (agosto 2025) amplia a receita. A mesma abordagem nativa, mais dados, mais parâmetros. Melhorias no MMMU são incrementais.

O InternVL-U (2026) adiciona a saída de imagem de geração unificada  através de cabeças MMDiT no topo da mesma espinha dorsal. A "U" significa "Entendimento + geração", perseguindo modelos unificados de estilo Transfusão (Lessão 12.13).

> **【中文解读】**InternVL-U(2026) se juntou à capacidade de geração de imagens no mesmo tronco (em tradução livre) através do MMDiT 头), buscando a compreensão do estilo de transfusão + geração de um modelo único.

### Comércio de pré-treino nativo .

A formação pré-aprendizagem nativa não é gratuita:

- Computação / 计算. Treinar um novo VLM a partir do zero custa o mesmo que treinar um texto LLM  milhões de horas GPU.
- Dados / dados. Corpos de imagem e texto interligados em escala são raros. OBELICS é 141M documentos; MMC4 é 571M. O texto sozinho é enviado em tokens 15T. A escassez de dados pré-aprendizagem multimodal é uma restrição dura.
- Base-LLM reutilização / 基础LLM复用. Pre-aprendizagem nativa desiste da opção de cair em um novo LLM mais tarde. Post-hoc permite que você troque Llama-3.1 por Llama-4 re-entrenando apenas o adaptador.

A aposta que faz o InternVL3 é que a dívida de alinhamento é pior do que a perda de reutilização. Os valores de referência apoiam a alegação. Os custos para produzir impedem que futuros laboratórios replicem barato.

> **【中文解读】**O estudo de base apoia este julgamento. Mas o alto custo do treinamento pré-existente faz com que a maioria dos projetos ainda escolha o programa de reinstalação.

## Use-o em prática.
```figure
l5-native-pretrain
```

## Usá-lo

`code/main.py`é um misturador de treinamento e um simulador de roteador ViR.

- Toma um mix de corpus-alvo (% texto, % interleaved, % caption, % video) e calcula as etapas esperadas por modalidade.
- Simula o envio de ViR em um lote de consultas (distribuição: 50% de baixo detalhe, 30% médio, 20% de alto detalhe) e relata a contagem média de tokens.
- Relatório DvD estimativas de rendimento dado codificador versus LLM FLOPs.
- Imprime um lado a lado de pós-hoc vs nativo pré-treinamento em parâmetros, computação, dados, e sintomas de alinhamento-devedores esperados.

## Envia-o .

Esta lição produz`outputs/skill-native-vs-posthoc-auditor.md`- Tendo em conta um plano de formação VLM proposto, verifica se é necessário proceder a um processo de formação nativa ou pós-hoc, indica o risco de alinhamento-devedor e recomenda um mix de corpus.

> **【中文解读】**O curso de formação em engenharia de telecomunicações (VLM) foi desenvolvido em 2006 e foi desenvolvido em 2006 e foi desenvolvido em 2008.

## Exercícios.

1. Estima o delta de computação entre o InternVL3-8B (pre-treino nativo) e o LLaVA-OneVision-7B (post-hoc).
   | 估算 InternVL3-8B（原生预训练）和 LLaVA-OneVision-7B（后装）的计算量差距。GPU 小时比率大约多少？什么解释了这个差距？

2. InternVL3 relata 40% de texto / 35% entrelaçado / 20% de legenda / 5% de vídeo. Se a sua tarefa-alvo é video-pesado, propor uma nova proporção e argumentar por que o modelo base ainda precisa de substantivos dados de texto e legenda.
   | InternVL3 的语料比例是 40/35/20/5。如果目标任务是视频密集的，提出新比例，论证为什么基础模型仍需要大量文本和描述数据。

3. Leia MM1.5 Secção 4 sobre esquecimento. Nomear o indicador exato onde o treinamento pós-hoc mostrou a maior regressão.
   | 阅读 MM1.5 第 4 节关于遗忘的内容。指出后装训练在哪个基准上退化最大？退化了多少？

4. O ViR encaminha 60% do tráfego para codificação de baixa resolução. Que tipos de consultas encaminha mal (envia para baixa resolução quando é necessária alta resolução)? Propõe três modos de falha do roteador.
   | ViR 将 60% 流量路由到低分辨率。哪些查询会被错误路由（需要高分辨率却发了低分辨率）？提出三种路由失败模式。

5. O DvD divide a visão e o LLM em GPUs separadas.
   | DvD 将视觉和 LLM 分到不同 GPU。在什么流量模式下 DvD 反而降低吞吐量？

## Termos-chave .

| Term | What people say | What it actually means | 中文含义 | 中文释义 |
|------|-----------------|------------------------|----------|---------|
| Native multimodal pretraining | "From scratch together" | Text + image + video tokens participate in the loss from step 1, not bolted on later | 从第一步就将文本+图像+视频 token 纳入损失函数 | |
| Alignment debt | "Post-hoc penalty" | Measurable regression in text skills and answer consistency that comes from bolting vision onto a frozen LLM | 后装 VLM 带来的文本技能退化和回答一致性下降 | |
| V2PE | "Variable visual pos encoding" | Per-modality learnable position encoding allocation; InternVL3's M-RoPE successor | 按模态类型可学习的位置编码分配 | |
| ViR | "Resolution router" | Small classifier that picks minimum resolution needed per query before encoding, saving inference tokens | 编码前选择最低所需分辨率的小型分类器 | |
| DvD | "Decoupled deployment" | Vision encoder on one GPU, LLM on another, with stream handoff; doubles throughput for large VLMs | 视觉编码器和 LLM 分 GPU 部署，流式传输连接 | |
| InternVL-U | "Unified understanding + generation" | 2026 follow-up that adds image-generation heads to the native-pretrain backbone | 在原生预训练骨干上加入图像生成头的统一模型 | |
| Interleaved corpus | "OBELICS / MMC4" | Documents with text and images in natural reading order; the raw material for native pretraining | 文本和图像按自然阅读顺序交织的文档语料 | |

## Mais leitura 延伸阅读

- [Chen et al. — InternVL 1 (arXiv:2312.14238)](https://arxiv.org/abs/2312.14238)- Não, não.
- [Zhu et al. — InternVL3 (arXiv:2504.10479)](https://arxiv.org/abs/2504.10479)O treinamento de vida.
- [InternVL3.5 (arXiv:2508.18265)](https://arxiv.org/abs/2508.18265)O InternVL3.5 é expandido.
- [InternVL-U (arXiv:2603.09877)](https://arxiv.org/abs/2603.09877)O InterVL-U compreender + gerar união
- [Zhang et al. — MM1.5 (arXiv:2409.20566)](https://arxiv.org/abs/2409.20566)O MM1.5 para a quantificação da dívida
