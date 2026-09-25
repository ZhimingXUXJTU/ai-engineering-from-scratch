# Cientista de IA v2  Taller-Level Pesquisa Autônoma  Cientista de IA v2  Trabalho

> O Cientista de IA de Sakana v2 (Yamada et al., arXiv:2504.08066) executa o ciclo completo de pesquisa: hipótese, código, experimentos, números, redação, submissão. É o primeiro sistema a ter uma revisão de pares de passagens de papel gerada num workshop do ICLR 2025. A avaliação independente (Beel et al.) descobriu que 42% das experiências falharam em erros de codificação e revisão de literatura frequentemente rotulava erroneamente conceitos estabelecidos como novos. Os próprios docentes de Sakana alertam que a base de código executa código escrito pelo LLM e recomendam o isolamento do Docker. Ambas as metades da imagem são o ponto.

> **【中文解读】**O Cientista de IA de Sakana v2(Yamada 等人,arXiv:2504.08066) executou um ciclo de pesquisa completo: hipóteses, codificação, experimentação, gráficos, redação, submissão. Foi o primeiro artigo gerado em um estudo realizado pelo ICLR 2025 工作坊同行评审的系统――独立评估(Beel 等人) descobriu que 42% dos experimentos causaram erros de codificação, literatura综述频繁将建立概念错误标记为新────Sakana 自己的文档警告代码库执行 LLM 编写代码并建议 Docker 隔离── estes dois aspectos são os principais pontos de estudo──

> **【拓展：开放式研究的代价】**O AlphaEvolve e o DGM também têm "máquinas de avaliação verificáveis" teste de unidade ou base de dados. Não há estudos: o estudo é avaliado pelo revisor, e não por um teste de unidade.

**Type:** Learn | **类型:** 学习
**Languages:** Python (stdlib, research-loop state-machine toy) | **语言:** Python（标准库，研究循环状态机玩具）
**Prerequisites:** Phase 15 · 03 (AlphaEvolve), Phase 15 · 04 (DGM) | **前置知识:** Phase 15 · 03（AlphaEvolve），Phase 15 · 04（DGM）
**Time:** ~60 minutes | **时间:** ~60 分钟

> - Não .**【前置】**O estudo foi realizado em um laboratório de ciências de ciência em São Paulo, onde o estudo foi realizado em uma clínica de ciência de ciência de ciência de ciência de ciência de ciência de ciência de ciência de ciência de ciência de ciência de ciência de ciência de ciência de ciência de ciência de ciência de ciência de ciência de ciência de ciência de ciência de ciência de ciência de ciência de ciência de ciência de ciência de ciência de ciência de ciência de ciência de ciência de ciência de ciência de ciência de ciência de ciência de ciência de ciência de ciência de ciência de ciência de ciência de ciência de ciência de ciência de ciência de ciência de ciência de ciência de ciência de ciência de ciência de ciência de ciência de ciência de ciência de ciência de ciência de ciência de ciência de ciência de ciência de ciência de ciência de ciência de ciência de ciência de ciência de ciência de ciência de ciência de ciência de ciência de ciência de ciência de ciência de ciência de ciência de ciência de ciência de ciência de ciência de ciência de ciência de ciência de ciência de ciência de ciência de ciência de ciência de ciência de ciência de ciência de ciência de ciência de ciência de ciência de ciência de ciência de ciência de ciência de ciência de ciência de ciência de ciência de ciência de ciência de ciência de ciência de ciência de ciência de ciência de ciência de ciência de ciência de ciência de ciência de ciência de ciência de ciência de ciência de ciência de ciência de ciência de ciência de ciência de ciência de ciência de ciência de ciência de ciência de ciência de ciência de ciência de ciência de ciência de ciência de ciência de ciência de ciência de ciência de ciência de ciência de ciência de ciência de ciência de ciência de ciência de ciência de ciência de ciência de ciência de ciência de ciência de ciência de ciência de ciência de ciência de ciência
> - Não .**【类比】**Cientista de IA = "AI 博士生"──AlphaEvolve/DGM = 工程师(评估器=单元测试,强信号);AI Cientista = 博士生(评估器=审稿人,弱信号)── igualmente correr experimento- avaliação-代循环, mas weak signal evaluation让 Agent 容易欺骗自己42% 的实验代码有错误,文献综述把已知概念当新发现──修复:(1) Docker 隔离(必须执行 LLM 代码沙盒);(2) 人类复核(披露出强信号检查(如复现性测试) (((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((

## O problema é o problema da introdução

A investigação é uma tarefa aberta.

> O estudo é uma missão aberta.

Ao contrário da pesquisa algorítmica da AlphaEvolve ou da auto-modificação limitada por benchmark da DGM, um resultado de pesquisa não tem um critério de corretão verificável por máquina. Um artigo é julgado por revisores, não por testes unitários. Isso torna o ciclo mais difícil de fechar  e mais valioso se fechado, porque a pesquisa é onde o progresso composto vive.

> Diferente do algoritmo de pesquisa da AlphaEvolve ou da base de restrições da DGM, os resultados do estudo não têm padrões de corretão que podem ser verificados por máquinas.

O Cientista de IA v1 (Sakana, 2024) fechou o ciclo começando com modelos de autoria humana. O LLM completou experimentos dentro de um andaime fixo. AI Scientist v2 (Yamada et al., 2025) remove o requisito de modelo usando a pesquisa agencial de árvore com um ciclo de crítica de modelo de linguagem de visão. O sistema gera ideias, implementa experimentos, produz números, escreve um artigo e retrata os comentários dos revisores.

> AI Scientist v1(Sakana,2024) através do padrão de escrita humana começar a fechar ciclo. LLM em um cadastro de escrita fixo.

> **【中文解读】**AI Scientist v2 (Sakana, 2025) 运行完整的研究循环:假设,编码,实验,图表,论文撰写和提交―― é o primeiro trabalho gerado através do ICLR 2025 工作坊同行评审系统―― mas uma avaliação independente descobriu que 42% dos experimentos causam erros de codificação, a literatura geral frequentemente será marcada por conceitos estabelecidos como novos── ambas as faces são verdadeiras──

Veredicto de revisão por pares: um artigo gerado por v2 foi aceito em uma oficina do ICLR 2025 (com divulgação). Veredicto de avaliação independente: o sistema está longe de ser confiável. Ambos são verdadeiros.

> O estudo foi concluído em um estudo de investigação sobre a existência de um sistema de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de

## O conceito central.

### A arquitetura, a arquitetura.

1. **Idea generation.**O LLM propõe ideias de pesquisa condicionadas a um tópico e literatura anterior. v1 utiliza modelos; v2 usa pesquisa agencial sobre um espaço de hipóteses.
   Tradução:**想法生成。**LLM  baseado em temas e publicações anteriores propõe ideias de estudo.
2. **Novelty check.**A fase de recuperação da literatura verifica se a ideia foi publicada. Esta é a etapa em que a avaliação de Beel et al. encontrou erroneamente etiquetado  métodos estabelecidos frequentemente classificados como novidade.
   Tradução:**新颖性检查。**文献检查步骤检查想法是否已发表──这是 Beel 等人评估发现错误标记的步骤已建立的方法频繁被分类为新──
3. **Experiment plan.**O agente desenha um protocolo experimental e escreve código.
   Tradução:**实验计划。**Agente 起草实验协议并编写代码──
4. **Execution.**O código corre em uma caixa de areia. Os erros são enviados de volta para um ciclo de retest. Nas medições de Beel et al., 42% das experiências falharam por erros de codificação nesta fase.
   Tradução:**执行。**Em pesquisas de pessoas como Beel, 42% das experiências neste estágio foram por erro de codificação.
5. **Figure generation.**Um modelo de linguagem visual lê figuras geradas e as reescreve para clareza.
   Tradução:**图表生成。**视觉语言模型读取生成图表并为清晰性重写它们── é a técnica chave do v2 
6. **Writeup.**O LLM elabora um artigo, reitera com um revisor interno.
   Tradução:**撰写。**LLM 起草论文,与内部审稿人代──
7. **Optional: submission.**O papel é apresentado a um local.
   Tradução:**可选：提交。**论文 submetido à reunião。

### O que significa o resultado de aceitação do workshop?

Um artigo gerado por v2 passou por revisão por pares em um workshop do ICLR 2025. Os autores revelaram a origem do artigo ao comitê do programa. A aceitação é um ponto de dados; não é uma licença para reivindicar que o sistema "faz pesquisa".

> Um artigo v2 生成的论文在ICLR 2025 工作坊通过同行评审――作者向程序委员会披露论文的来源――接受是一个数据点;不是声称系统"做研究"的许可――

Contexto importante: os trabalhos de oficina são uma barra mais baixa do que os trabalhos de conferência principal. A revisão entre pares é barulhenta; uma pequena fração das apresentações são aceitas em qualquer dia dado. Um sucesso é uma prova de conceito, não uma alegação de confiabilidade. O artigo Nature 2026 documenta o ciclo de ponta a ponta e foi co-autor por pesquisadores humanos; não é "o sistema escreveu um artigo Nature".

> 重要背景:工作坊论文的门低于主会议论文──同行评审有噪音;任何一天都有一小部分提交被接受──一次成功是概念证明,不是可靠性声明──Nature 2026 论文记录端到端循环,本身由人类研究人员共同撰写;不是"系统写了一篇 Nature 论文"──

### O que a avaliação independente descobriu

A Beel et al. (arXiv:2502.14297) realizou uma avaliação externa.

> Beel 等人 (arXiv:2502.14297)运行了外部评估──标题性发现:

- **Experiment failures.**42% das experiências falharam por erros de codificação (importações erradas, desajustes de forma, variáveis não definidas).
  Tradução:**实验失败。**42% das experiências foram erradas em codificação, mas não todas.
- **Novelty mislabeling.**O passo de recuperação de literatura frequentemente sinalizava conceitos estabelecidos como novos.
  Tradução:**新颖性错误标记。**文献检索步骤频繁将已建立的概念标记为新── é o fenómeno e efeito do estudo.
- **Presentation-quality gap.**A crítica de figuras de linguagem visual produziu visuais de qualidade de publicação, mascando as fraquezas experimentais subjacentes.
  Tradução:**呈现质量差距。**O estudo de linguagem visual e gráfico de avaliação gerou resultados de qualidade, mas ocultava os pontos fracos da experiência de base.

A última descoberta é a importante para esta fase: um sistema que produz resultados convincentes sem fazer pesquisas convincentes é mais perigoso, não mais seguro, do que um que falha obviamente.

> A última descoberta é importante para esta fase: gerar resultados convincentes, mas não concluir estudos convincentes, que são mais perigosos do que sistemas que fracassam claramente, e não mais seguros.

A avaliação deve chegar às alegações subjacentes, não parar no número.

>  a avaliação deve abordar as declarações de nível inferior, em vez de ficar na tabela:

### A preocupação com a fuga da caixa de areia.

O próprio repositório de Sakana README adverte:

> Sakana  própria armazém README 警告:

> Devido à natureza deste software, que executa código gerado pela LLM, não podemos garantir a segurança. Há riscos de pacotes perigosos, acesso à web descontrolado e reprodução de processos não intencionais. Use a seu próprio risco e considere o isolamento do Docker.

> Como este software executa o código de desenvolvimento do LLM, não podemos garantir a segurança. Há riscos de acesso à rede e de gerar processos inesperados.

Este é o formato operacional da autonomia em um domínio não verificado. O LLM escreve código; o código é executado; o código pode fazer qualquer coisa que o processo seja autorizado a fazer. Sem uma caixa de areia que limite duramente o sistema de arquivos, rede e ações de processo, qualquer agente de pesquisa autodirigido pode exfiltrar dados, queimar computação ou se reescrever.

> É um modo de operação autónoma no domínio não verificado. LLM escreve código; código opera; código pode fazer qualquer coisa que seja permitido. Não há barreiras de hardware para sistemas de documentos, redes e operações de processo, qualquer agente de investigação autónoma pode divulgar dados, queimar computadores ou se reescrever.

A história da caixa de areia do AlphaEvolve é mais fácil porque seu avaliador é apertado. O loop do AI Scientist v2 executa código aberto com metas abertas. É por isso que precisa de um isolamento mais forte (Docker mínimo; seccomp / gVisor preferido) e uma revisão manual de cada submissão antes de sair do sistema.

> A descrição da caixa de dados do AlphaEvolve é mais fácil, porque seu avaliador é rigoroso.

### Onde o v2 está na pilha de fronteira.

| System | Target | Output kind | Evaluator | Known failure |
|---|---|---|---|---|
| 系统 | 目标 | 输出类型 | 评估器 | 已知失败 |
| AlphaEvolve | algorithms | code | unit + benchmark | bounded by evaluator rigor |
| AlphaEvolve | 算法 | 代码 | 单元 + 基准 | 受评估器严谨性约束 |
| DGM | agent scaffolding | code | SWE-bench | reward hacking |
| DGM | Agent 脚手架 | 代码 | SWE-bench | 奖励篡改 |
| AI Scientist v2 | research papers | text + code + figures | peer review (weak) | experiment failures, mislabeling, polish masking weakness |
| AI Scientist v2 | 研究论文 | 文本 + 代码 + 图表 | 同行评审（弱） | 实验失败、错误标记、修饰掩盖弱点 |

O v2 tem o avaliador automático mais fraco dos três, a superfície de saída mais ampla e o caminho mais curto para artefatos públicos.

> V2 dos três possui o mais fraco avaliador automático, a maior gama de produtos e o menor número de rotas de produtos públicos.

Os controles operacionais (caixa de areia, revisão, divulgação) estão a fazer a maior parte do trabalho de segurança.

> 操作控制 (操作控制) (sabox 审查 披露) assumiu a maior parte do trabalho de segurança.

## Use-o com o framework implementado.
```figure
mx-research-loop
```

## Usá-lo

`code/main.py`Simula o loop v2 como uma máquina de estado: ideia → novidade verificação → experimento → figura → escrever → revisão → aceitar-ou-iterar. Cada estado tem uma probabilidade de falha configurável tirada dos resultados de Beel et al.

> `code/main.py`将 v2 循环模拟为状态机:想法 → 新性检查 → 实验 → 图表 → 撰写 → 审稿 → 接受或代―― cada estado tem de Beel 等人 encontrados entre提取的可配置失败概率──运行模拟器 N 个循环并计数:

- Quantas ideias chegam à submissão.
  Tradução do português:
- Quantas submissões teriam uma falha experimental crítica que o papel polido esconde.
  Tradução do inglês: How many submitted will have modifications?
- Como os orçamentos de retest trocam qualidade vs rendimento.
  Tradução do inglês para tradução do inglês:重试预算如何衡量质量与产量之间.

## Envia-o . Produto .

`outputs/skill-ai-scientist-sandbox-review.md`é uma lista de revisão de dois portões para qualquer coisa produzida por um agente de ciclo de pesquisa antes de sair da caixa de areia.

> `outputs/skill-ai-scientist-sandbox-review.md`É um ciclo de estudo de qualquer produto produzido por um agente.

## Exercícios.

1. Corra .`code/main.py`Qual fração de loop runs produz um papel "limpo"?
   中文翻译:使用默认参数运行 `code/main.py` Quantas proporções de ciclos de execução produzem artigos "cânticos"?

2. As defesas já utilizam o 42% / 25% da Beel et al.`--experiment-failure 0.20 --novelty-mislabel 0.10`E depois com `--experiment-failure 0.60 --novelty-mislabel 0.40`Como é que a parte polida, mas imperfeita, muda entre as duas corridas?
   中文翻译:默认已使用BeeL等人的 42% / 25%──用 `--experiment-failure 0.20 --novelty-mislabel 0.10`Cravam e depois usam.`--experiment-failure 0.60 --novelty-mislabel 0.40`◊ Como varia a proporção de alterações e de falhas entre duas operações?

3. Leia o repo README de Sakana AI Scientist v2 sobre requisitos de caixa de areia. Cite duas restrições adicionais (além do Docker) que você aplicaria para uma execução autónoma de vários dias.
   Chinese: 阅读 Sakana AI Scientist v2 仓库 README 关于沙箱要求──命名你会为多日自主运行添加的两项额外限制(除Docker 外)──

4. Leia a secção 4 sobre a lacuna de qualidade da apresentação.
   Chinese Translation: read Beel  et al. 4o parágrafo sobre a diferença de qualidade presente.

5. Propõe um protocolo de revisão humana para resultados de agentes de pesquisa que se balanceie melhor do que "um doutorado lê cada artigo". Identifique o gargalo de engarrafamento e o projeto em torno dele.
   Por exemplo, a empresa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa em pesquisa de pesquisa de pesquisa de pesquisa em pesquisa de pesquisa de pesquisa em pesquisa de pesquisa de pesquisa de pesquisa em pesquisa de pesquisa de pesquisa em pesquisa de pesquisa em pesquisa de pesquisa em pesquisa de pesquisa de pesquisa em pesquisa de pesquisa em pesquisa em pesquisa em pesquisa de pesquisa em pesquisa em pesquisa em pesquisa de pesquisa em pesquisa em pesquisa de pesquisa em pesquisa em pesquisa em pesquisa de pesquisa em pesquisa em pesquisa em pesquisa em pesquisa em pesquisa em pesquisa em pesquisa em pesquisa em pesada.

## Termos-chave .

| Term | What people say | What it actually means |
|---|---|---|
| 术语 | 通俗说法 | 实际含义 |
| AI Scientist v1 | "Sakana's templated research agent" | Filled experiments into a fixed scaffold |
| AI Scientist v1 | "Sakana 的模板研究 Agent" | 在固定脚手架中填充实验 |
| AI Scientist v2 | "Template-free research agent" | Agentic tree search with VLM figure critique |
| AI Scientist v2 | "无模板研究 Agent" | 带有 VLM 图表评审的 Agent 式树搜索 |
| Agentic tree search | "Branching research agent" | Expands multiple experiment plans in parallel; prunes by internal critic |
| Agent 式树搜索 | "分支研究 Agent" | 并行展开多个实验计划；由内部评论者修剪 |
| Vision-language critique | "VLM polish on figures" | Multimodal model reads figures and rewrites them for clarity |
| 视觉语言评审 | "VLM 修饰图表" | 多模态模型读取图表并为清晰性重写 |
| Literature retrieval | "Novelty check" | Searches prior work to confirm idea novelty — documented to mislabel |
| 文献检索 | "新颖性检查" | 搜索先前工作以确认想法新颖性——文档记录会错误标记 |
| Polish masking | "Pretty paper, broken research" | Presentation quality exceeds experimental quality; hides weaknesses |
| 修饰掩盖 | "漂亮论文，破碎研究" | 呈现质量超过实验质量；隐藏弱点 |
| Sandbox escape | "LLM code breaks out" | Agent-executed code does things the loop designer did not intend |
| 沙箱逃逸 | "LLM 代码逃逸" | Agent 执行的代码做循环设计者未预期的事 |

## Mais leitura 延伸阅读

- [Yamada et al. (2025). The AI Scientist-v2](https://arxiv.org/abs/2504.08066)- Papel.
  Tradução do português:
- [Sakana blog on the Nature 2026 publication](https://sakana.ai/ai-scientist-nature/) resumo do fornecedor com contexto de revisão por pares.
  Chinese: 厂商摘要,含同行评审背景.
- [Beel et al. (2025). Independent evaluation of The AI Scientist](https://arxiv.org/abs/2502.14297) Números de avaliação externa.
  Tradução do inglês: externa avaliação digital.
- [Sakana AI Scientist v1 paper](https://arxiv.org/abs/2408.06292) o antecessor templado.
  Tradução do português:模板化前身──
- [Anthropic — Measuring AI agent autonomy](https://www.anthropic.com/research/measuring-agent-autonomy) mais amplo enquadramento dos agentes de investigação de âmbito aberto.
  Tradução do inglês: Open Studies Agent's wider framework.
