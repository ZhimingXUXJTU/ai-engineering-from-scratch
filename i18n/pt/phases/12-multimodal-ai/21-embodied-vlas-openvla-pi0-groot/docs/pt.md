# VLAs incorporados: RT-2, OpenVLA, π0, GR00T.

> A primeira vez que um modelo leu uma receita de um site e a executou em um robô de cozinha foi RT-2 (Google DeepMind, julho de 2023). RT-2 discretou ações como tokens de texto, co-finou um VLM em dados web mais dados de ação de robôs, e provou que a escala web de linguagem de visão transfere conhecimento para controle robótico. O OpenVLA (Junho de 2024) enviou a referência aberta 7B. A série π0 da Inteligência Física (2024-2025) adicionou especialistas em ação de correspondência de fluxo. O GR00T N1 da NVIDIA (março de 2025) forneceu controle de sistema duplo (Sistema 1 / Sistema 2) para robôs humanoides em escala. O VLA primitivo  ação de linguagem de visão, um único modelo que vê, lê e age  é a ponte entre os modelos de compreensão desta fase e os sistemas autônomos na Fase 15.

> **【中文解读】**RT-2  primeira prova de rede nível de conhecimento de linguagem visual pode ser transferido para controle de máquinas:将关节动作分散化为文本代币,与VLM 联合微调;; OpenVLA é open source 7B 参考,π0 引入流匹配动作专家,GR00T N1 实现双系统(快思考/慢思考) 人形机器人控制──VLA(视觉-语言-动作) é uma ligação entre um modo de compreensão e um sistema autónomo de ponteponto──

> **【拓展：Embodied VLA 到机器人产业】**O modelo VLA está indo da laboratória para a indústria: Tesla Optimus, Figura 01  1X Tecnologias e outros sistemas de controle baseados em VLA estão em desenvolvimento. No cenário industrial, VLA pode ser usado em máquinas de armazenamento de materiais, máquinas de montagem, etc. O desafio central é a segurança e a confiabilidade.

**Type:** Learn
**Languages:** Python (stdlib, action tokenizer + VLA inference skeleton)
**Prerequisites:** Phase 12 · 05 (LLaVA), Phase 15 (Autonomous Systems, referenced)
**Time:** ~180 minutes

> - Não .**【前置】**O VLA = VLM 输出从文本变成机器人动作,是Phase 12到Phase 15 (Fase 12 até Fase 15)
> - Não .**【类比】**VLA = "deixar o copo vermelho na mesa"→ ver o copo→ planejar o caminho→ controlar os laços de execução)。RT-2 Colocar o movimento em token = Colocar o movimento em texto em prompt;π0 流匹配 = 输出连续动作而非离散 token,更精确──

## Objetivos de aprendizagem

- Descrever a tokenização de ação: codificação discreta de bin (RT-2), tokens de ação eficientes FAST, ações de correspondência contínua de fluxo (π0).
  中文翻译:描述动作分词化:离散bin 编码(RT-2) 、FAST 高效动作符号、连续流匹配动作(π0)。
- Explique por que a co-ajustação dos dados da web + dos robôs preserva a transferência de conhecimentos gerais para novas tarefas.
  Tradução do inglês para tradução do inglês: Explain why in the netpage+机器人数据 on united micro调能保留通用知识迁移到新任务的能力──
- Compare OpenVLA (aberto 7B Llama+VLM), π0 (corresponsão de fluxo) e GR00T N1 (sistema duplo) na mesma tarefa robótica.
  Tradução do inglês em japonês: в одно и то же机器人任务 на сравнение OpenVLA(開放 7B Llama+VLM) 、π0(流匹配) и GR00T N1(双系统) ⋅
- Cite o conjunto de dados Open X-Embodiment e o seu papel como corpo de formação RT-X.
  O programa foi lançado em outubro de 2015 e foi lançado em outubro de 2015.

## O problema é o problema da introdução

Um robô que faz tarefas a partir de instruções de linguagem natural tem sido um alvo de pesquisa desde a década de 1970. A resposta da década de 2020: um modelo de ação de linguagem de visão (VLA). A mesma arquitetura VLM usada para VQA, mas a saída é ações (torques conjuntos, poses de efetores finais, comandos discretos) em vez de texto.

> Usando a ordem de linguagem natural para fazer o trabalho doméstico desde 1970 é o objetivo da pesquisa.

Desafios específicos dos VLA:

> Desafios especiais da VLA:

1. Os espaços de acção são contínuos (ângulos conjuntos, forças) e de alta dimensão (7-DOF braço + 3-DOF aderente = 10 dims a 30 Hz).
   O espaço é um espaço de movimento.
2. Os dados de treinamento específicos para robôs são escassos. O Open X-Embodiment tem ~ 1M trajetórias; imagem de texto na web é 5B +.
   O sistema de controle de dados é um sistema de controle de dados de dados de computadores.
3. O circuito de controlo de 30 Hz significa um orçamento de 33 ms por ação.
   Tradução do inglês: Control Frequency is important.
4. Ação errada danifica hardware, humanos ou propriedades.
   Chinese Translation: segurança.                                                                                                                                                                                                                                                             

## O conceito central.

> **【中文解读】**具身視觉-语言-动作模型(VLA)让机器人理解语言指令和视觉场景后执行物理动作──OpenVLA é a fonte aberta VLA, pi0(Intelligência Física) e NVIDIA Groot é o modelo representativo do corpo inteligente──VLA = 视觉编码器 + LLM + 动作解码器──

> **【拓展：具身智能的进展**OpenVLA-7B em Google Robot realiza cerca de 80% da taxa de sucesso de missão. Pi0 Utilização de fluxo de correspondência (Flow Matching) para gerar tráfego de continuidade de movimentação, em comparação com a tradicional separação de movimentação mais fácil. NVIDIA Groot  especializado em máquinas humanas.


### Tokenization de ações (RT-2)

RT-2 truque: representar cada alvo conjunto como um token de texto quantizado. Discrete o normal [-1, 1] gama em 256 canas, mapear cada canha para um vocabulário ID. Uma ação de 10 DOF se torna 10 tokens em cada etapa de controle.

> Técnicas do RT-2:将每个关节目标表示为量化文本代币――将归结化的 [-1, 1] 范围离散化为 256 个 bin, cada bin 映射到一个词汇 ID──10 自由度动作在每个控制步骤变成10 个 token──

Co-finação de um VLM PaLM-X em uma mistura:

> Em dados mistos em conjunto, PaLM-X VLM:

- Pares de imagem e texto da Web (captioning, VQA).
  Tradução do português:
- Demonstrações de robôs, ação como tokens.
  Tradução do inglês para o inglês:

O modelo vê "colher o cubo vermelho" (linguagem) → imagem (visão) → sequência de ação de 10 tokens (alvos conjuntos discretos). O treinamento pré-web preserva a transferência de conhecimento geral: RT-2 pode seguir "mover-se em direção ao objeto em movimento rápido" mesmo que "muover-se rápido" não esteja em dados de treinamento.

> 模型看"拿起红色方块" (→ 图像) 视觉) → 10 tokens 动作序列 (→ "o movimento é um movimento") 网页预训练保留通用知识迁移:RT-2 能执行"移向快速移动的物体", mesmo que"快速移动" não esteja incluído no training data。

Inferência de 3 a 5 Hz no papel RT-2, limitada pelo decodificação autoregressiva VLM.

> RT-2 论文中推理速度 3-5 Hz, limitada ao VLM 自归解码──

### OpenVLA  a referência aberta 7B

OpenVLA (Kim et al., junho 2024) é o equivalente RT-2 de peso aberto. 7B Llama backbone, DINOv2 + SigLIP dual vision encoder, tokenization de ação em 256 canas.

> OpenVLA é um sistema de código aberto de RT-2 para PCs.

Formada em Open X-Embodiment (970 mil trajetórias em 22 robôs).

> Em Open X-Embodiment 上 тренинг(22 个机器人共 97万条轨迹) ・内置 LoRA 微调支持,适配新机器人──

Inferência: 4-5 Hz em um A100 com quantização.

> 推理:A100 上量化后 4-5 Hz──对慢速操作足够,不适合高频控制──

### FAST tokenizer  decodificação de ação mais rápida

Pertsch et al. (2024) mostrou que a tokenização discreta bin é ineficiente  a maioria das ações agrupam-se em uma pequena região do espaço bin. FAST (Frequency-domain Action Sequence Tokenizer) comprime as sequências de ação através de DCT e quantiza os coeficientes.

> Pertsch 等人(2024) demonstrou que a eficiência de separação binária dividida em palavras é baixa A maioria dos movimentos se agrupam em pequenas regiões do espaço.

Uma trajetória de ação de 30 passos torna-se ~ 10 tokens FAST em vez de 300 tokens discretos.

> 30 步动作轨迹 se transformou em cerca de 10 快速代币, em vez de 300 离散 bin token──推理速度提升 3-5 倍,质量无损──

### π0 e ações de correspondência de fluxo

A π0 da Inteligência Física (Black et al., outubro de 2024) substitui os tokens de ação discretos por um especialista em ação de correspondência de fluxo:

> Inteligência Física π0 Us流匹配动作专家替代离散动作代币:

- Um pequeno transformador de ação lê os estados ocultos do VLM e produz uma sequência de ação contínua de 50 passos através de fluxo rectificado.
  Tradução do inglês para Transformer 读取 VLM 隐藏状态,通过正流输出连续的50步动作序列──
- A cabeça de ação entra com perda de correspondência de fluxo; o VLM permanece inalterado antes do treino.
  Chinese:动作头用流匹配损失训练; VLM 预训练不变──
- Inferência: sequência de ação completa emitida em ~5 passos de denotação, controlo efetivo de 50 Hz.
  O sistema de movimentos completo está em 5 passos em saída, igual a 50Hz.

A fórmula de acção contínua preserva a suavidade que a discretizão destrói.

> π0  afirmação: em uma ampla operação de tarefas derrotar OpenVLA e Octo.

> **【中文解读】**π0 Usando fluxo de correspondência alternativo de movimento token: um pequeno movimento Transformador 读取 VLM 隐藏状态, através de 正流输出连续的50 步动序列──推理时只需要约5步去噪音,实现效率等效50Hz 控制频率──连续动作表达保留了离散会破坏的动作平滑性──

π0.5 e π0-FAST são atualizações incrementais. π0-FAST combina a tokenização FAST com a correspondência de fluxo.

> π0.5 和 π0-FAST é um aumento de escalação.

### GR00T N1  Sistema duplo para humanoides

A GR00T N1 da NVIDIA (março 2025) é construída para robôs humanoides (> 30 DOF, corpo inteiro):

> GR00T N1 da NVIDIA para design de máquina em forma humana:

- Sistema 2: uma grande cena de leitura VLM + instrução, produzindo sub-objetivos de alto nível em ~ 1 Hz.
  Sistema 2: VLM 读取场景+ instrução, em torno de 1Hz 生成高层子目标──
- Sistema 1: um pequeno transformador de cabeça de ação que produz comandos conjuntos de baixo nível de 50-100 Hz condicionados aos subobjetivos.
  Sistema 1: pequeno movimento cabeça Transformador 根据子目标生成底层 50-100Hz 关节命令。

Os mapas divididos para o pensamento rápido e lento de Kahneman: planos do sistema 2, o sistema 1 atua. Benefícios: planejamento lento do tamanho VLM não bloqueia o controle rápido; o sistema 1 permanece pequeno para a latência.

> Este tipo de separação de mapas para o pensamento rápido de Carniman: sistema 2  planejamento, sistema 1  execução.

GR00T N1.7 (final de 2025) melhora a escalação de dados. GR00T sintoniza com dados sim-to-real do Omniverse.

> GR00T N1.7 ((2025 anos de fim) - melhorou a expansão de dados.

### O corpo X aberto

Os dados de treinamento. RT-X (outubro de 2023) reuniram 22 conjuntos de dados que cobrem 1M de trajetórias em 22 robôs.

> 训练数据──RT-X(2023 年 10 月) integrou 22 datasets, cobrindo 100 000 条轨迹 de 22 机器人──Open X-Embodiment é o idioma usado por todos:

- ALOHA / Bridge V2 / Droid / RT-2 Kitchen / Language Table.
  中文翻译:ALOHA / Bridge V2 / Droid / RT-2 Kitchen / Language Table。
- Cada amostra: (estado do robô, visualização da câmera, instrução, sequência de ação).
  Tradução do inglês para o português: cada um dos seus componentes é um membro da família.
- Higiene de treinamento: unificar espaço de ação, normalizar os rangos articulares, redimensionar as câmeras.
  Tradução do inglês para o inglês: training规范:统一动作空间、归一化关节范围、统一摄像头分辨率──

OpenVLA e π0 treinam em Open X-Embodiment.

> OpenVLA 和 π0 em Open X-Embodiment 上訓練── com um determinado órgão de campo diferença através de 100-1000 个任务特定演示的 LoRA 微调来弥合──

### Co-ajuste perfeito versus apenas robô

A co-ajuste de qualidade mistura dados VQA da web com trajetórias de robôs. A relação importa: muito VQA e o modelo esquece ações; muito dados robóticos e o modelo perde conhecimento geral.

> 联合微调将网页 VQA 数据与机器人轨迹混合──比例很重要: VQA 太多模型忘记动作;机器人数据太多模型失去通用知识──

Ratio RT-2: ~1:1. OpenVLA: ~0.5:1 web-to-robot. π0: similar. A relação precisa é um hiperparâmetro para sintonizar por tamanho de conjunto de dados.

> RT-2 proporção cerca de 1:1──OpenVLA 约 0.5:1──π0 类似──精确比例是按数据集大小调节的超参数──

O treinamento apenas com robôs produz modelos específicos de tarefas que falham em instruções fora da distribuição. Co-fine-tuning é a diferença entre "colher o cubo vermelho (em demonstração) " e "colher o terceiro maior objeto da esquerda (fraseamento de novidade). "

>                                                                                                                                                                                                                                                               

### Limite de segurança e de acção

Todos os navios VLA de produção com:

> Cada VLA de produção está equipado:

- Limites de articulação rígida (não pode passar o torque da especificação).
  O que é um sistema de controle de dados?
- Limite de velocidade (clipagem suave).
  Tradução do inglês: velocidade limitada (s)
- Limitações do espaço de trabalho (o efetor final não pode sair da mesa).
  中文翻译:工作空间边界 (末端执行器不能离开桌面)
- Homem em curso de aprovação para novas tarefas.
  Tradução do inglês para Chinês: 新任务的人工审批.

Estes estão fora do VLA como controles de camada de controle.

> Estes estão localizados fora do VLA  controles de nível de controle  VLA  Output                                                                                                                                                                                                                                                    

## Use-o com o framework implementado.
```figure
mm-action-tokens
```

## Usá-lo

`code/main.py`- Não .

- Implementa tokenização e destokenização de ações de 256 bin.
  Tradução do inglês: implementar 256 bin 动作分词化和反分词化──
- Esboça um tokenizer FAST baseado na quantização DCT +.
  Tradução do inglês: Based on DCT + 量化勾勒 FAST 分词器──
- Comparar o número de tokens por passo de ação (bin discreto, FAST, fluxo contínuo).
  Comparar separado bin、FAST、连续流三种方式的每步符号 数──
- Imprime um resumo de linhagem de RT-2 → OpenVLA → π0 → GR00T.
  中文翻译:打印 RT-2 → OpenVLA → π0 → GR00T 的谱系摘要──

## Envia-o . Produto .

Esta lição produz`outputs/skill-vla-action-format-picker.md`. Dada uma tarefa robótica (manipulação, navegação, corpo humanoide), escolha entre bin discreto + RT-2, FAST + OpenVLA, fluxo de correspondência + π0, ou sistema duplo + GR00T.

> 本课产 出 `outputs/skill-vla-action-format-picker.md`△ dados dados de trabalho de um dispositivo (operation, navigation, human form), em separado bin+RT-2、FAST+OpenVLA、流匹配+π0 ou bin systems+GR00T 之间选择──

## Exercícios.

1. Um braço 10 DOF com taxa de controle de 30 Hz. Tokenization de bin discreto em 256 canhões emite quantos tokens por segundo? um VLM 7B pode acompanhar? 10 liberdade de arma mecânica 30Hz  controle freqüência, 256 离散bin。 por segundo produzir quantos tokens? 7B VLM 能跟上?

2. A tokenization FAST comprime as trajetórias de 30 passos para ~ 10 tokens. O que perde o usuário se a trajetória tiver movimento de alta frequência (por exemplo, bateria)? FAST vai reduzir 30 passos de rotação para cerca de 10 tokens.

3. A cabeça de correspondência de fluxo de π0 denota em ~5 passos. Compare a passagem ao decodificador autoregressivo de OpenVLA em 4-5 Hz.

4. O Sistema 1 / Sistema 2 do GR00T divide mapas para Kahneman. Propõe uma divisão diferente (Sistema 3?) que pode ajudar a andar bipedal. GR00T's sistema1/sistema2 separ separado contra a teoria de Karniemann. Propõe um esquema separado diferente ((sistema3?) para ajudar a andar em dois pés.

5. Leia a Seção 4 do Open X-Embodiment sobre curatividade de conjuntos de dados. Numa lei de curatividade que impede a fuga de domínios.

## Termos-chave .

| Term | What people say | What it actually means | 中文释义 |
|------|-----------------|------------------------|---------|
| VLA | "Vision-language-action" 视觉-语言-动作模型 | Model that takes image + instruction and outputs action commands 接受图像+指令并输出动作命令的模型 | |
| Action tokenization | "Discrete bins" 离散 bin 编码 | Quantize continuous joint targets into 256 bins per dim, each a vocab ID 将连续关节目标量化为每维 256 个 bin，每个 bin 对应一个词表 ID | |
| FAST tokenizer | "Frequency action tokens" 频域动作 token | DCT + quantize to compress 30-step trajectories to ~10 tokens 用 DCT + 量化将 30 步轨迹压缩为约 10 个 token | |
| Co-fine-tune | "Mix web + robot" 混合微调 | Train on web VQA data alongside robot demos to preserve general knowledge 在网络 VQA 数据和机器人演示上联合训练以保留通用知识 | |
| Flow-matching action head | "pi0 continuous output" 流匹配动作头 | Small transformer that outputs a 50-step action sequence via rectified flow 通过矫正流输出 50 步连续动作序列的小型 Transformer | |
| System 1 / System 2 | "Dual-system control" 双系统控制 | Large VLM plans slowly, small action head acts quickly; GR00T pattern 大 VLM 慢规划，小动作头快执行；GR00T 模式 | |
| Open X-Embodiment | "RT-X dataset" 开放具身数据集 | 1M-trajectory cross-robot dataset; the training corpus 100 万轨迹跨机器人数据集；标准训练语料 | |

## Mais leitura 延伸阅读

- [Brohan et al. — RT-2 (arXiv:2307.15818)](https://arxiv.org/abs/2307.15818)
- [Kim et al. — OpenVLA (arXiv:2406.09246)](https://arxiv.org/abs/2406.09246)
- [Black et al. — π0 (arXiv:2410.24164)](https://arxiv.org/abs/2410.24164)
- [NVIDIA — GR00T N1 (arXiv:2503.14734)](https://arxiv.org/abs/2503.14734)
- [Open X-Embodiment Collab — RT-X (arXiv:2310.08864)](https://arxiv.org/abs/2310.08864)
