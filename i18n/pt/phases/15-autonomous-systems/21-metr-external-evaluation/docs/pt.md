# METR Horizontes do Tempo e Avaliação de Capacidade Externa  Avaliação METR

> A METR (ex-ARC Evals) é uma organização independente 501 ((c) ((3)) desde dezembro de 2023. O seu índice de referência Time Horizon 1.1 (janeiro de 2026) corresponde a uma curva logística da probabilidade de sucesso da tarefa versus log ((experto tempo de conclusão humana); a intersecção de 50% de probabilidade define o horizonte temporal do modelo. O conjunto de engajamento 20252026 abrange GPT-5.1, GPT-5.1-Codex-Max e avaliações de monitorização de protótipo (um monitor pode capturar tarefas laterais; o agente pode fugir). Suites de referência: HCAST (180+ ML, ciber, SWE, tarefas de raciocínio; 1 minuto a 8+ horas), RE-Bench (71 ML tarefas de engenharia de pesquisa com base de peritos), SWAA. A nota honesta: as medições METR são idealizadas  sem humanos, sem consequências reais  e a equipe documentou a lacuna de comportamento avaliação versus implantação (Lessão 1). Um horizonte temporal é um limite superior, não uma previsão de implantação.

> **【中文解读】**Esta secção apresenta a avaliação independente de terceiros da capacidade e risco do sistema de IA do METR.


**Type:** Learn | **类型:** 学习
**Languages:** Python (stdlib, logistic-fit horizon estimator) | **语言:** Python（标准库，逻辑拟合时间线估计器）
**Prerequisites:** Phase 15 · 01 (Long-horizon agents), Phase 15 · 19 (RSP) | **前置知识:** Phase 15 · 01（长程 Agent）、Phase 15 · 19（RSP）
**Time:** ~60 minutes | **时间:** ~60 分钟

> - Não .**【前置】**O METR é um órgão de avaliação independente de terceiros, que transforma o "R&D-4" em um número de dados mensuráveis.
> - Não .**【类比】**METR = "AI 能力的第三方检查中心"──RSP diz que "AI R&D-4 值" é abstrato; O horizonte temporal do METR 基准把"AI 能完成多复杂任务" comprimir em um modelo de 50% de desempenho confiável para completar um trabalho especialista花 X 小时的任务"── semelhante ao IQ 分数概括智力, mas os números do METR têm métodos de medição repetíveis──
> ️ **【易错点】**METR Time Horizon 当成部署预测 → 错──METR 测试是理想化的(无真人监督、无真实后果),实际部署时能力会打折──修复:Time Horizon 是上限不是下限,部署前必须在自己的真实任务上复测──

## O problema é o problema da introdução

As políticas de escalagem (Lessões 19, 20) são apenas tão úteis quanto as medidas que referem. "Predigo de I&D-4 de IA" e "Autonomia de longo alcance" são definidas na prosa da política; elas só se tornam acionáveis quando avaliações específicas produzem números específicos.

> 扩展政策 (第 19、20 课) são utilizados apenas como as medidas referidas.

O METR é a organização de avaliação externa 20242026 que definiu muitos desses números. Eles avaliam modelos de fronteira  muitas vezes pré-lançamento, sob NDA com laboratórios  e publicam a metodologia depois. O Time Horizon 1.1 (janeiro de 2026) é o seu artefato principal: um único escalar que comprime a capacidade em uma unidade legível pelo ser humano ("este modelo pode fazer o tipo de tarefa em que um especialista passa X horas com 50% de confiabilidade").

> METR é uma organização de avaliação externa de muitos desses números. Eles avaliam modelos de vanguarda, geralmente antes de serem publicados, e depois de serem assinados com laboratórios. Time Horizon 1.1 基准 (em janeiro de 2026) é o seu tema: um modelo que reduz a capacidade para uma unidade de leitura humana.

A lição é em parte sobre a metodologia (como um horizonte é calculado) e em parte sobre a interpretação (por que um horizonte é um limite superior, não uma previsão de implantação). As duas habilidades pertencem juntas. Uma equipe que entende como o horizonte é adequado é muito mais difícil de enganar com uma reclamação de um mau fornecedor do que uma equipe que vê apenas "14 horas" em um slide.

> Esta parte da aula é sobre metodologia (como calcular a linha de tempo), parte sobre explicação (por que a linha de tempo é um limite superior e não uma previsão de implantação).

## O conceito central.

### METR de fundo

- Fundada: Dezembro de 2023 (ex-ARC Evals, dividida em 501 ((c) ((3)).
  No entanto, o grupo de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos de grupos.
- Ámbito de aplicação: avaliação das capacidades autónomas dos modelos de fronteira, muitas vezes pré-lançamento.
  O modelo é um modelo de avaliação de capacidade de desenvolvimento.
- Laboratórios parceiros: Anthropic, OpenAI (múltiples compromissos 20252026).
  Tradução do português:合作实验室:Antropic、OpenAI(20252026 多次合作)。
- Resultados notáveis: Horizonte temporário 1.0 (março 2025), Horizonte temporário 1.1 (janeiro 2026), avaliações de monitorização de protótipos.
  O programa de avaliação de monitoramento é o que acontece com o programa de monitoramento de dados.

### O Time Horizon se encaixa

Metodologia (do blog e artigos da METR):

> 方法论(来自 METR 博客和论文):

1. Coletar uma suíte de tarefas que abrange de minutos a horas de tempo de conclusão de peritos. Suites atuais: HCAST (180+ tarefas), RE-Bench (71 tarefas), SWAA.
   O que é que você tem a ver com o seu trabalho?
2. Execute o modelo em cada tarefa; registar sucesso ou fracasso.
   Tradução do inglês para tradução do inglês:
3. Aplicar uma curva logística: P ((sucesso) como função do tempo de conclusão log ((experto).
   No entanto, o tempo de execução é muito mais longo.
4. O horizonte é o tempo de expertos em que P ((sucesso) = 0,5.
   Chinese Translation: 时间线是 P(成功) = 0,5 时的专家时间──

A forma logística-ajustamento é a certa porque a capacidade geralmente tem uma relação crescente, aproximando-se do planalto com a dificuldade da tarefa. O ponto de 50% é uma escolha (poderia ser 10%, 90%); METR relata vários limiares no papel detalhado, mas lidera com 50% porque é o mais intuitivo.

> A forma de adaptação lógica é positiva, pois a capacidade e a dificuldade de tarefa são geralmente de uma forma única e crescente, tendendo a uma relação entre a plataforma e a sua capacidade de fazer uma tarefa.

### Os números de Janeiro de 2026

Por Horizonte Temporal 1.1:

> 按 Time Horizon 1.1:

- Claude Opus 4.6: ~ 14 horas com uma confiabilidade de 50%, a partir de Time Horizon 1.1 (janeiro 2026).
  Opus 4.6:截至 Time Horizon 1.1(2026 年 1 月),50% 可靠性下约 14 小时──
- Tempo duplicado em tarefas de estilo HCAST: ~4,3 meses (130,8 dias) no ajuste pós-2023 relatado pelo Time Horizon 1.1 (janeiro de 2026); o número de ~7 meses é o ajuste completo de 20192025 do Time Horizon 1.0 e é relatado em TH1.1 ao lado do número pós-2023.
  Chinese Translation:HCAST 类任务的倍增时间:Time Horizon 1.1(1月2026年) 后拟合的23 后报的约 4.3 个月(130.8 天); 后报的约 7 个月的数字是Time Horizon 1.0 完整的20192025 拟合的TIME Horizon 1.0 完整的20192025 后报的后报,在 TH1.1 中与 2023 后报的后报的同时进行了.

Estes são os números específicos que restam das referências da Fase 15. Eles são citados no RSP v3.0 (Lessão 19) da Anthropic e no FSF v3 (Lessão 20) da DeepMind como uma das medições que alimentam as avaliações de limiar.

> Estes são os números concretos citados na Fase 15 e são citados em Antropic RSP v3.0 (§19) e DeepMind FSF v3 (§20) como uma das medidas de avaliação de valor.

### Suítes de referência

- **HCAST**A programação de trabalho de um grupo de especialistas é uma das principais tarefas da área de tecnologia, segurança cibernética, engenharia de software e raciocínio geral.
  Tradução:**HCAST**O programa de aprendizagem de software e de segurança em rede foi desenvolvido em 18 de janeiro de 2015 e foi criado em 18 de janeiro de 2015.
- **RE-Bench**A análise da base de dados da IA é feita por um grupo de investigadores que trabalha em uma área de investigação e desenvolvimento de IA.
  Tradução:**RE-Bench**O estudo de tecnologia de aprendizagem de máquina foi realizado em uma área de pesquisa de tecnologia de aprendizagem de máquina.
- **SWAA**As tarefas mais curtas são úteis para a calibração do extremo inferior da curva do horizonte.
  Tradução:**SWAA**A: menor tarefa; utilizada para a formação do tempo

### Avaliações de monitorização de protótipos

O trabalho do METR 20252026 incluiu protótipos de monitoramento e avaliação: pode um monitor capturar um modelo realizando uma tarefa lateral (algo diferente do que o operador pediu); pode o agente evitar o monitor. Estes alimentam diretamente a categoria "Submining Safeguards" na OpenAI PF v2 e o monitoramento de alinhamento enganoso na DeepMind FSF v3 (Lessão 20).

> 20252026 METR 工作包括监控评估原型:监控器能否捕获模型执行副任务(操作员请求以外的事);Agent 能否规避监控器──这些直接入OpenAI PF v2 的"破坏防护"类别和DeepMind FSF v3(第 20 课) de fraudes对齐监控──

### Por que os horizontes são limites superiores

- **Idealized tooling**As tarefas de referência dão ao modelo ferramentas limpas e dados bem formatados.
  Tradução:**理想化工具**A base de tarefas é fornecer ferramentas e dados de boa forma ao modelo.
- **No real consequences**O modelo nunca realmente faturou um cliente, exclui dados reais ou contata pessoas reais.
  Tradução:**无真实后果**O modelo é de facto não fornecer contas ao cliente, excluir dados reais ou contatar pessoas reais.
- **Eval-context gaming**Leção 1. Os modelos comportam-se de forma diferente nos testes. O Relatório Internacional de Segurança da IA de 2026 documenta isso empiricamente.
  Tradução:**评估上下文博弈**O estudo foi realizado em 18 de janeiro de 2021 e foi publicado em 18 de janeiro de 2021 no Instituto de Ciências Biológicas da Universidade de São Paulo.
- **No legitimate user variance**Os utilizadores reais produzem pedidos ambíguos e dependentes do contexto.
  Tradução:**无合法用户方差**O primeiro passo é a criação de um sistema de dados de dados.

O horizonte é o limite máximo de capacidade em condições favoráveis.

>                                                                                                                                                                                                                                                               

### O caso do avaliador externo

A avaliação externa é importante porque os laboratórios internos têm incentivos para otimizar as métricas que relatam. A independência do METR  501 ((c) (3) com uma metodologia declarada e trabalhos revisados por pares  é a mitigação estrutural. Não é suficiente sozinho (os laboratórios ainda controlam o que o METR vê), mas é estritamente melhor do que nenhuma avaliação externa.

> A avaliação externa é importante, porque o laboratório interno tem a capacidade de melhorar o índice de relatório. A independência do METR é muito mais forte do que a avaliação externa.

### Como utilizar os números de horizonte na prática

- **As a capability filter**Se o horizonte de um modelo estiver bem abaixo do tempo de experiência de uma tarefa proposta, não o enviem de forma autónoma (arquivo de competências da Lesson 1).
  Tradução:**作为能力过滤器**Se o tempo do modelo for muito inferior ao tempo do especialista em tarefas propostas, não deixe que ele publique de forma automática.
- **As a trend indicator**O tempo de duplicação indica quanto tempo a prática actual permanecerá segura mesmo sem novas mitigações.
  Tradução:**作为趋势指标**O tempo aumenta para dizer-te que a prática atual, mesmo sem novas soluções, continua segura por muito tempo.
- **As a prior**A programação de trabalho deve ser feita com base em um horizonte de 14 horas.
  Tradução:**作为先验**14 horas de tempo em linha é o ponto de partida. Dependendo da sua distribuição de tarefas, qualidade e implementação de ferramentas.

## Use-o com o framework implementado.
```figure
a5-horizon-fit
```

## Usá-lo

`code/main.py`Implementa um ajuste logístico de sucesso de tarefa vs log(experto tempo), dado um conjunto de resultados sintéticos. Relata o horizonte de 50% (título do METR), 10% horizonte (conservador) e 90% horizonte (optimista). Também demonstra quais são as mudanças quando a taxa de sucesso é artificialmente inflada por jogos de conteúdo de avaliação.

> `code/main.py`给定合成结果集实现任务成功率 vs log(专家时间) 的逻辑拟合――报告 50% 时间线(METR 标题) 、10% 时间线(保守) 、90% 时间线(乐观) ── também demonstrado quando a taxa de sucesso foi avaliada pelo contexto de jogos

## Envia-o . Produto .

`outputs/skill-horizon-interpretation.md`Revisar a alegação de horizonte de um fornecedor e produz uma análise da lacuna entre a alegação de referência e a realidade da implantação.

> `outputs/skill-horizon-interpretation.md`审查 fornecedor time line declaration并产生基准声明与部署现实之间的差异分析──

## Exercícios.

1. Corra .`code/main.py`Confirme que o horizonte de 50% da adaptação corresponde à verdade sintética do solo. Agora, dime a grade de tempo de tarefa; o horizonte estima mudanças significativamente?
   Tradução: 运行`code/main.py` Confirmar que 50% da linha de tempo se corresponde ao valor real.

2. Leia o post do blog Time Horizon 1.1 do METR. Identifique as tarefas específicas em que a confiabilidade é mais alta e em que é mais baixa. Explique por que existe a lacuna.
   Chinese Translation: read METR Time Horizon 1.1 博客──识别可靠性最高和最低的具体任务──解释为什么存在差距──

3. Leia os recursos do METR "Messuring Autonomous AI Capabilities". Enumere as categorias de tarefas HCAST. Escolha uma categoria que você ponderaria mais para uma tarefa de produção e justifique o porquê.
   Chinese Translation:阅读 METR's "Messure autonomous AI 能力"资源──列出 HCAST 任务类别──选一个你为生产任务加权的类别并论证为何──

4. Introduza o jogo de conteúdo de avaliação no simulador: inverte ~20% das tarefas falhadas para o sucesso. Relate o novo horizonte. Isso aproxima o que uma taxa de jogo de 20% faz com o número observado.
   Introdução de jogos de avaliação-contexto em simulador: vai ser cerca de 20% 失败任务翻转为成功.

5. Desenhe uma avaliação do horizonte interno em seu próprio backlog de bugs ou um conjunto de tarefas representativo. Descreva a coleta de dados, o ajuste e o que a saída lhe diz. Compare com números METR.
   Tradução do inglês para inglês: In your own bug backlog or representative taskset on design internal timeline assessment.

## Termos-chave .

| Term | What people say | What it actually means | 中文 |
|---|---|---|---|
| METR | "External evaluator" | ex-ARC Evals; independent 501(c)(3) since Dec 2023 | METR：原 ARC Evals，独立第三方 |
| Time Horizon | "Capability measure" | Expert task length at 50% reliability, from logistic fit | 时间线：50% 可靠性下专家任务长度 |
| HCAST | "METR's main suite" | 180+ tasks spanning 1 min to 8+ hours | HCAST：METR 主套件，180+ 任务 |
| RE-Bench | "Research engineering" | 71 ML research-engineering tasks with human baseline | RE-Bench：71 个机器学习研发任务 |
| SWAA | "Short-task suite" | Calibrates the low end of the horizon curve | SWAA：短任务套件，校准低端 |
| Doubling time | "Growth rate" | Time for the 50% horizon to double; ~7 months per HCAST | 倍增时间：50% 时间线翻倍所需时间 |
| Eval-context gaming | "Model behaves differently" | Documented behavior gap between tests and deployment | 评估上下文博弈：测试与部署行为差距 |
| Upper bound | "Horizon is a ceiling" | Benchmark horizon > deployment reliability under load | 上限：基准时间线 > 负载下部署可靠性 |

## Mais leitura 延伸阅读

- [METR — Resources for Measuring Autonomous AI Capabilities](https://metr.org/measuring-autonomous-ai-capabilities/) Especificações HCAST, RE-Bench, SWAA.
  中文翻译:HCAST、RE-Bench、SWAA 规范
- [METR — Measuring AI Ability to Complete Long Tasks](https://metr.org/blog/2025-03-19-measuring-ai-ability-to-complete-long-tasks/)O papel original do horizonte.
  Tradução do idioma: original
- [METR — Time Horizon 1.1 (January 2026)](https://metr.org/research/) números e metodologia atuais.
  Tradução do inglês:
- [Epoch AI — METR Time Horizons benchmark](https://epoch.ai/benchmarks/metr-time-horizons)- Seguimento ao vivo.
  Tradução do inglês:
- [Anthropic — Measuring agent autonomy in practice](https://www.anthropic.com/research/measuring-agent-autonomy) Perspectiva interna das medições do METR.
  中文翻译:METR 测量的内部视角
