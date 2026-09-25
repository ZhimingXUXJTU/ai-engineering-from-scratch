# LLaVA e instrução visual de sintonização .

> LLaVA (abril de 2023) é a arquitetura multimodal mais copiada do planeta. Substituiu o Q-Former do BLIP-2 com um MLP de 2 camadas, substituiu a atenção cruzada fechada do Flamingo com concatenamento de token ingênuo e treinou em 158k viradas de instrução visual geradas pelo GPT-4 a partir de legendas apenas de texto. Qualquer praticante que construiu um VLM entre 2023 e 2026 construiu alguma variante do LLaVA. LLaVA-1.5 adicionou AnyRes. A resolução do LVA-NEXT aumentou. LLaVA-OneVision imagem unificada, multi-imagem e vídeo em uma receita. Esta lição lê a receita, implementa o projetor e explica por que "o mais simples venceu".

> **【中文解读】**LLaVA é a mais duplicada de várias estruturas entre 2023-2026 anos. Seu conceito central é muito simples: usar 2 níveis de MLP para colocar o visual editor de saída projetado para o modelo de linguagem em um espaço embuído, e então colocar o visual token diretamente em conjunto com a série de textos.

> **【拓展：多模态大模型的起源】**Antes do LLaVA, o modelo multimodelo dependia principalmente de mecanismos complexos de atenção transmodelo (como o Flamingo's Gate Control Intercept Attention  BLIP-2's Q-Former)  LLaVA marcou o sucesso de estudos multimodelo de "design better transmodelo interface" para "converter com interface mais simples + 更多数据"  This thoughtstyle directly affected all subsequent mainstream VLMs  InternVL Qwen-VL、Phi-Vision etc) 

**Type:** Build  | **类型：构建**
**Languages:** Python (stdlib, projector + instruction-template builder)  | **语言：Python（标准库，投影器 + 指令模板构建器）**
**Prerequisites:** Phase 12 · 02 (CLIP), Phase 11 (LLM Engineering — instruction tuning)  | **前置：阶段12第02课（CLIP）、阶段11（LLM工程——指令微调）**
**Time:** ~180 minutes  | **时长：约180分钟**

> - Não .**【前置】**O primeiro é o primeiro, o segundo, que é o segundo, que é o segundo, que é o segundo.
> - Não .**【类比】**LLaVA = "把图片直接印出贴在文档里"──BLIP-2 Q-Former = "把 256 páginas书压成 32 pages摘要再交给LLM"; LLaVA MLP = "576 páginas原文整本贴给LLM"──前者省纸张但丢信息,后者费纸张但LLM 看得到全部细节LLM 上下文变长后",费纸"不再是问题,LLaVA自然就赢了──

## Objetivos de aprendizagem

- Construir um projeto de MLP de 2 camadas que mapeia as incorporações de parches ViT (dim 1024) para a incorporação de um LLM dim (dim 4096).
- Caminhe pela receita de dois estágios do LLaVA: (1) alinhamento do projeto em pares de captura de 558k, (2) sintonização de instruções visuais em 158k giras geradas por GPT-4.
- Construa um prompt em formato LLaVA com o marcador de lugar do token de imagem, o prompt do sistema e as viradas de usuário/assistente.
- Explicar por que a comunidade mudou de Q-Former para MLP apesar da vitória do orçamento de tokens de Q-Former.

## O problema é o contexto do problema .

O Q-Former do BLIP-2 (Lessão 12.03) comprime uma imagem para 32 tokens. Limpo, eficiente, bom para benchmarks. Mas tem dois problemas.

Primeiro, o Q-Former é treinável, mas sua perda não é a tarefa final. A primeira fase treina ITC+ITM+ITG. A segunda fase treina perda de LM. As consultas aprendem alguma representação intermediária que o LLM então tem que decodificar.

Em segundo lugar, o Q-Former toma 188 milhões de parâmetros, e na escala de 2023 da LLaVA você teve que co-desenhá-lo com o seu LLM alvo. Mudança o LLM, retrain o Q-Former. Mudança o codificador de visão, retrain. Cada combinação foi um projeto de P&D separado.

> **【中文解读】**O Q-Former do BLIP-2 vai comprimir imagens em 32 tokens, parece altamente eficaz, mas tem dois problemas principais: 1)  Training Objective não concorda Primeira fase com ITC/ITM/ITG 损失, segunda fase apenas com linguagem construção 损失, informação em botelha  丢失; 2) 参数大 ((188M) 且与特定 LLM 合,换 LLM 就需要重新训练;;

A resposta LLaVA foi embaraçosa em sua simplicidade: pegue os 576 tokens de parche do ViT, cada um através de um MLP de 2 camadas (`1024 → 4096 → 4096`Não há gargalos, não há estágio 1 de pré-treino em objetivos estranhos, apenas treine o MLP em uma perda direta de LM.

> **【中文解读】**LLaVA é um programa simples e embaraçoso: directamente transferir 576 tokens de complemento do ViT através de um MLP de 2 níveis.`1024 → 4096 → 4096`), então tudo foi jogado na série de entrada do LLM. Não há botelhas, não há objetivos de treinamento estranhos, apenas usando linguagem.

> ️ **【易错点】**A primeira fase deve treinar! Muitos pensam que podem saltar a primeira fase  direct do instrução 微调不行! não treinado de projector de saída de livre circulação, LLM 完全看不懂视觉代币 含义, etapa 2 vai fazer LLM Colocar o token de visão quando o ruído é ignorado.

A segunda visão da LLaVA: usar GPT-4 (apenas texto) para gerar dados de instrução. Alimentar GPT-4 a legenda COCO e dados de caixa de limites para uma imagem, pedir que produzam conversas, descrições e perguntas de raciocínio complexas. 158k instrução-resposta gira gratuitamente.

> **【中文解读】**Data from Where?LLaVA's second innovation: using GPT-4(pure text model) generate instrução dados。 will give COCO image's description text text and borderline information to GPT-4, let it generate dialogue、 description and suggest questions, get 158k 条 instrução-回复对, completely no need of artificial marking。

O resultado: um VLM que correu em 8 A100s por um dia, venceu Flamingo no MMMU, e enviou um ponto de controle aberto que a comunidade poderia estender.

> **【拓展：LLaVA 的产业影响】**A LLaVA provou que o VLM não precisa de grande capacidade de cálculo. O LLaVA foi usado para entender gráficos de jornais financeiros, imagens de bilheteria, etc.

## O conceito central.

> **【中文解读】**LLaVA irá conectar CLIP  visual editor com LLM  através de instrução visual                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                          

> **【拓展：LLaVA 的开源生态】**LLaVA é o modelo de código aberto mais bem sucedido. LLaVA-NeXT  suporta entrada de resolução arbitrária, LLaVA-OneVision 统一图像和视频理解── desempenho próximo de 80% do GPT-4V, causou um grande número de modelos derivados.


### A arquitetura, a arquitetura.

LLaVA-1.5 em 13B:  LLaVA-1.5 13B 参数版本:
- Encoder de visão / 视觉编码器: CLIP ViT-L/14 @ 336 (congelado durante a fase 1, opcionalmente descongelado fase 2 / 第一阶段结,第二阶段可选解).
- Projector / 投影器: MLP de 2 camadas com ativação GELU / 2层MLP + GELU激活, `1024 → 4096 → 4096`- Não .
- LLM / 语言模型: Vicuna-13B (mais tarde Llama-3.1-8B / 后续使用 Llama-3.1-8B).

Forward passando uma imagem + texto de prompt: 图像+文本提示的前向传播:

```
img -> ViT -> 576 patches of dim 1024           # 图像 -> ViT -> 576个维度1024的补丁
patches -> MLP -> 576 tokens of dim 4096         # 补丁 -> MLP -> 576个维度4096的token
prompt: system + "<image>" placeholder + user question  # 提示词：系统提示 + <image>占位符 + 用户问题
replace <image> token with the 576 projected tokens      # 用576个投影token替换<image>
feed the full sequence to the LLM                       # 将完整序列送入LLM
decode response                                         # 解码响应
```

A imagem ocupa 576 tokens do contexto LLM. No contexto de 2048, isso deixa 1472 tokens para o texto. No contexto de 32k, é um erro de arredondamento.

> **【中文解读】**Em 2048 no topo da janela de texto, isso representa 28%, apenas restam 1472 janela de texto; mas em 32k no topo da janela de texto, isso quase pode ser ignorado. É por isso que com o crescimento da janela de texto do LLM, a estratégia de "violência de combinação" da LAVA está cada vez mais disponível.

### Fase 1: Alineação do projector.

Freeze ViT. Freeze LLM. Treinar apenas a MLP de 2 camadas. Dataset: 558k pares de imagem-caption (LAION-CC-SBU). Loss: modelagem de linguagem na legenda, condicionada aos tokens de imagem projetados.

Em uma única época no lote 128 isso é feito em algumas horas. O projetor aprende a mapear o espaço ViT para o espaço LLM.

> **【中文解读】**Primeiro estágio 结 ViT 和 LLM, apenas treinamento 2 Layer MLP──用558k图文对,以语言建模损失训练──MLP 学会将 ViT's视觉嵌入空间映射到 LLM's语义空间──单个时代、批量128 几小时即可完成──

### Fase 2: A regulação de instruções visuais.

Desbloquear o projector (ainda treinável). Desbloquear o LLM (geralmente totalmente, às vezes LoRA). Treinar em 158k viradas de instrução visual.

Os dados de instrução são o truque.
1. Tome uma imagem de COCO.
2. Extrair a descrição do texto (5 legendas humanas + lista de caixa de limites).
3. Enviar para GPT-4 com três modelos de solicitação:
   - Conversação / 对话: "Generar um diálogo de ida e volta entre um usuário e assistente sobre esta imagem".
   - Descrição detalhada / 详细描述: "Dá uma rica e detalhada descrição da imagem".
   - Raciocínio complexo: "Pergunte uma pergunta que exige raciocínio sobre a imagem, e depois responda-a".
4. Parse GPT-4 saída em pares (instrução, resposta).

Nada disso toca diretamente à imagem  apenas a descrição do texto. GPT-4 alucina conteúdo de imagem plausível. Um pouco de ruído, mas funcionou: 158k voltas foi suficiente para desbloquear o diálogo.

> **【中文解读】**关键创新: dados geração completamente não contato imagem em si mesma apenas com a descrição do texto. GPT-4 会"幻觉" de um conteúdo de imagem razoável, embora haverá ruído, mas 158k 条数据足以解锁对话能力── esse "usar um modelo forte para gerar dados de formação de modelos fracos" pensamento foi mais tarde amplamente adotado ((como Auto-Instrução、Alpaca, etc.)

> 🤔 **【困惑】**P: GPT-4 没看图只看描述,那 LLaVA 训练时实际学学的"视觉"是什么?A: LLaVA 学习是两件事: 1) 投影机把 ViT 的视觉特征翻译成 LLM 能理解的语义; 2) LLM 学会"看图片 → 生成符合 GPT-4 风格的描述"――GPT-4 的"幻觉"实际上是合理的描述(基于标题),所以最终 LLaVA 也能产生合理的描述──
> ️ **【易错点】**Auto-treinamento LLaVA 时数据不清洗 → GPT-4 的幻觉污染训练集,模型可能描述图中没有的东西──修复:用 GPT-4V(多模态版本)替代纯文本 GPT-4,让 GPT-4V 真的看图生成描述(ShareGPT4V就是这个思路),质量更高──

> **【拓展：数据合成的范式意义】**O método de síntese de dados do LLaVA (GPT-4 生成指令数据) foi utilizado para criar uma nova modalidade de engenharia de dados do VLM.

### Porque é que a comunidade copiou isto?

- Não há perdas específicas para a fase 1 para sintonizar.
- O projeto treina em horas, não dias.
- LLM pode ser trocado (LLaVA-Llama2, LLaVA-Mistral, LLaVA-Llama3) reestruturando apenas o projetor.
- O pipeline de dados de instrução visual usa GPT-4 e é barato para regenerar para um novo domínio.

### LLaVA-1.5 e LLaVA-NEXT

LLaVA-1.5 (outubro 2023) adicionado:  LLaVA-1.5 ((2023年10月) 新增:
- Os dados acadêmicos-tarefa (VQA, OKVQA, RefCOCO) misturados em sintonia de instruções.
- Melhor sistema de aconselhamento.
- 2048 → 32k contexto.

LLaVA-NeXT ( janeiro 2024) adicionado: ➡️ LLaVA-NeXT(2024年1月) 新增:
- AnyRes: dividir imagens de alta resolução em uma grade de 2x2 ou 1x3 de 336x336 culturas, mais uma miniatura global de baixa resolução. Cada cultura se torna 576 tokens; total de cerca de 2880 tokens visuais por imagem. OCR e tarefas de gráfico saltaram.
- Melhor mistura de dados de instruções com ShareGPT4V (capções de alta qualidade GPT-4V).
- Mas, por isso, não é necessário que o governo do país seja mais forte.

> **【拓展：AnyRes 与高分辨率理解】**AnyRes é a técnica chave para o tratamento de imagens de alta resolução LLaVA. Para os relatórios, emissões e imagens de arquivo, a alta resolução é fundamental para a compreensão.

### LLaVA-OneVision

A lição 12.08 abrange OneVision em profundidade. versão curta: o mesmo projetor, mas treinado com um currículo que abrange uma imagem única, várias imagens e vídeo em um modelo com orçamento compartilhado de tokens visuais.

> **【中文解读】**Seção 12.08  课将深入讲解 OneVision──简言之: Usar o mesmo projector, mas através do curso aprender a cobrir três tarefas de um único gráfico, gráfico e vídeo, em um modelo compartilhar o token visual 预算──

### A comparação com o Q-Former

| | Q-Former (BLIP-2) | MLP (LLaVA) |
|---|---|---|
| Visual tokens per image / 每张图视觉token数 | 32 | 576 (base/基础) or 2880 (AnyRes) |
| Trainable params / 可训练参数 | 188M + LM | 40M + LM |
| Stage 1 loss / 第一阶段损失 | ITC+ITM+ITG | LM only / 仅语言建模 |
| LLM drop-in / LLM替换 | Requires retrain / 需重新训练 | Swap with minimal retrain / 几乎无需重训 |
| Multi-image / 多图像 | Awkward / 不自然 | Natural (concat) / 自然拼接 |
| Video / 视频 | Awkward / 不自然 | Natural (per-frame concat) / 逐帧拼接 |
| Token budget / Token预算 | Small / 小 | Large / 大 |

O MLP ganha na simplicidade e flexibilidade de tokens. Q-Former ganha no orçamento de tokens. No final de 2023, o orçamento de tokens não era mais a restrição obrigatória (contextos LLM cresceram para 32k-128k +) e a simplicidade dominou.

> **【中文解读】**MLP em Simplicidade e Token 灵活性上胜出, Q-Former em Token 预算上胜出. Mas até o final de 2023, com o crescimento da janela do LLM para 32k-128k, o token 预算不再是瓶, Simplicidade se torna um fator decisivo.

> 🤔 **【困惑】**O que é que não é LLaVA?  加 加复度变高、训练难度大、收益小(除非视频这样的标签 预算紧张场景) ⋅ 2) LLaVA-1.5 和 LLaVA-NeXT

### O formato de sugestão.

```
A chat between a curious human and an artificial intelligence assistant. The assistant gives helpful, detailed, and polite answers to the human's questions. USER: <image> Describe this image in detail. ASSISTANT: The image shows ...
```

`<image>`O Tokenizer vê uma sequência ligeiramente mais longa do que foi treinado, mas o LLM lida com a nova entrada porque a etapa 1 ensinou a.

> **【中文解读】** `<image>`É um token de posicionamento, antes de ser substituído por 576 个 (ou 2880 个) de tokens de visão sob o modelo AnyRes. LLM é capaz de processar essas entradas nunca vistas, porque a primeira fase de treinamento ensinou a entender o visual após a projeção.

### Economia de parâmetros.

LLaVA-1.5-7B desintegração:
- CLIP ViT-L/14 @ 336: 303M (estágio congelado 1, muitas vezes descongelado estágio 2 / 第一阶段结,第二阶段通常解).
- Projector (2x linear) / 投影器: ~22M treinable / 可训练.
- Llama-7B: 7B.
- Total / 总计: 7.3B params. Treinável durante a fase 2 / Segunda fase: projector completo 7B + 22M / 全部7B + 22M projector.

O custo de treinamento para a etapa 2: ~ 20 horas em 8xA100. Este é o número chave  um dia, um nó, reprodutivel.

> **【中文解读】**Segundo estágio custo de treinamento: 8 张 A100 跑约20 小时──这是关键数字一天──一台机器──可复现──这是LLaVA 能够迅速传播的原因──
```figure
mm-llava-projector
```

## Usá-lo

## Use-o em prática.

`code/main.py`- Não é o que é ?`code/main.py`实现:

1. O projeto de MLP de 2 camadas (dim 16 → 32 → 32 para escala de brinquedo) em Python puro.
2. O canal de construção de sistemas de controlo: sistema de controlo de controlo + `<image>`substituído por N tokens projetados + turno de usuário + assistente de geração de lugar.`<image>`替换为N个投影代币 + 用户轮次 + 助手生成占位符──
3. Um visualizer para o que o bloco visual de 576 tokens parece no contexto LLM (percentagem de 2k / 32k / 128k contexto consumido).

## Envia-o .

Esta lição produz`outputs/skill-llava-vibes-eval.md`. Tendo em conta um ponto de controlo da família LLaVA, ele opera uma suite de vibrações de 10 pulsos (3 subtítulos, 3 VQA, 2 raciocínios, 2 recusa) e informa um cartão de pontuação legível ao ser humano.

> **【中文解读】**本课产 出 `outputs/skill-llava-vibes-eval.md` Dado um ponto de verificação da série LLaVA, executar 10 suítes de teste "vibes-eval"  3 descrições  3 VQA  2 sugestões  2 rejeitamentos), gerar resultados artificiais.

## Exercícios.

1. Calcule o número de parâmetros treinaveis para o projeto MLP de 2 camadas em `1024 → 4096 → 4096`Com GELU e Bias, que fracção de LLaVA-13B representa?
   | 计算维度为 `1024 → 4096 → 4096` 的 2 层 MLP 投影器的可训练参数量。含 GELU 和 bias，它占 LLaVA-13B 的多少比例？

2. Construir um aviso de LLaVA para um caso de "recusar"  a imagem contém um indivíduo privado. Escrever a resposta esperada do assistente. Por que o LLaVA deve recusar este tiro zero e que dados de treinamento seriam necessários para reforçar a recusa?
   | 为"拒绝"场景构建 LLaVA 提示词——图像包含私人个体。写出期望的助手回复。为什么 LLaVA 应该零样本拒绝？需要什么训练数据来强化拒绝行为？

3. Leia a seção AnyRes do blog LLaVA-NeXT. Calcule a contagem de tokens visuais para uma imagem de 1344x672 em AnyRes. Compare com 576 tokens base em 336x336.
   | 阅读 LLaVA-NeXT 博客的 AnyRes 部分。计算 1344x672 图像在 AnyRes 下的视觉 token 数量，并与 336x336 基础设置的 576 个 token 比较。

4. O projeto LLaVA estágio 1 é treinado com perda de LM em legendas. O que acontece se você saltar a etapa 1 e passar diretamente para a etapa 2 (ajuste de instruções visuais)? Cite a ablação Prismatic VLMs (arXiv:2402.07865) para a resposta.
   | LLaVA 第一阶段投影器用描述文本的语言建模损失训练。如果跳过第一阶段直接进入第二阶段会怎样？引用 Prismatic VLMs 消融实验（arXiv:2402.07865）回答。

5. LLaVA-Instruct-150k usa GPT-4 com legendas COCO para gerar instruções. Para um novo domínio (radiografias médicas, imagens de satélite), descreva o pipeline de dados em quatro etapas para gerar instruções de domínio. O que pode dar errado em cada etapa?
   | LLaVA-Instruct-150k 用 GPT-4 从 COCO 描述生成指令。对于新领域（医疗X光、卫星图像），描述生成领域指令的四步数据管线。每步可能出什么问题？

## Termos-chave .

| Term | What people say | What it actually means | 中文含义 | 中文释义 |
|------|----------------|------------------------|----------|---------|
| Projector | "MLP bridge" | 2-layer MLP with GELU mapping ViT dim to LLM dim | 投影器：将ViT维度映射到LLM维度的2层MLP | |
| Image token | "<image> placeholder" | Prompt marker replaced by N projected visual tokens before inference | 图像token：推理前被替换为N个投影视觉token的提示标记 | |
| Visual instruction tuning | "LLaVA stage 2" | Training on GPT-4-generated (image, instruction, response) triplets | 视觉指令微调：在GPT-4生成的（图像,指令,回复）三元组上训练 | |
| Stage 1 alignment | "Projector pretraining" | Freeze ViT and LLM, train projector with LM loss on captions | 第一阶段对齐：冻结ViT和LLM，用描述文本的LM损失训练投影器 | |
| AnyRes | "Multi-crop tiling" | Split high-res image into a tile grid and concatenate each tile's visual tokens | AnyRes：将高分辨率图像切分为网格，拼接各切片的视觉token | |
| LLaVA-Instruct | "GPT-4-generated" | 158k instruction-response pairs synthesized from COCO captions + GPT-4 | LLaVA指令数据：用COCO描述+GPT-4合成的158k指令-回复对 | |
| Vision encoder freeze | "Backbone locked" | CLIP weights do not update in stage 1, sometimes not in stage 2 either | 视觉编码器冻结：CLIP权重在阶段1不更新，有时在阶段2也不更新 | |
| ShareGPT4V | "Better captions" | 1M dense captions generated by GPT-4V, used for higher-quality alignment | 100万条GPT-4V生成的密集描述，用于更高质量的对齐 | |
| VQA | "Visual question answering" | Task of answering a free-form question about an image | 视觉问答：回答关于图像的自由形式问题 | |
| Prismatic VLMs | "Design-space paper" | Karamcheti 2024 ablation systematically testing projector and data choices | 系统测试投影器和数据选择的设计空间消融实验论文 | |

## Mais leitura 延伸阅读

- [Liu et al. — Visual Instruction Tuning (arXiv:2304.08485)](https://arxiv.org/abs/2304.08485)O artigo da LLAVA.
- [Liu et al. — Improved Baselines with Visual Instruction Tuning (arXiv:2310.03744)](https://arxiv.org/abs/2310.03744)- LLaVA-1.5. - LLaVA-1.5 - Edição melhorada.
- [Chen et al. — ShareGPT4V (arXiv:2311.12793)](https://arxiv.org/abs/2311.12793) conjunto de dados de legendas densas. 密集描述数据集
- [Karamcheti et al. — Prismatic VLMs (arXiv:2402.07865)](https://arxiv.org/abs/2402.07865)- Ablações de design-espaço.
- [Li et al. — LLaVA-OneVision (arXiv:2408.03326)](https://arxiv.org/abs/2408.03326) Unified Single-Image, Multi-Image, Video.
