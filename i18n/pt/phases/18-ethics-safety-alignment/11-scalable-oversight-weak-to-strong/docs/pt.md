# Supervisão Escalavel e Generalização Fraca a Forte

> Burns et al. (OpenAI Superalignment, "Generalização fraca a forte", 2023) propôs um proxy para o problema de superalignment: ajustar um modelo forte usando rótulos produzidos por um modelo mais fraco. Se o modelo forte generaliza corretamente a partir da supervisão fraca imperfeita, os métodos atuais de alinhamento em escala humana podem se estender a sistemas sobre-humanos. A supervisão escalável e o W2SG são complementares. A supervisão escalável (debate, modelagem recorrente de recompensas, decomposição de tarefas) aumenta a capacidade eficaz do superintendente para que possa acompanhar o modelo sob supervisão. O W2SG garante que o modelo forte generaliza corretamente qualquer supervisão imperfeita que o superintendente forneça. O debate ajuda o W2SG (arXiv:2501.13124, janeiro 2025) combina-os.

> **【中文解读】**Este capítulo apresenta supervisão expandível de fraca para forte AI segurança avaliação método。Burns 等人(OpenAI 超级对齐, 2023) propõe um agente do super super-对齐 problema: etiquetas geradas com modelos fracos modelo.

> **【拓展：弱到强泛化 → 超级对齐路径】**PGR(Performance Gap Recovered) = (微调后-弱) /(上限-弱) ――PGR 为 1.0 significa que o supervisor fraco completamente compensou o diferencial;PGR 为 0 significa que o supervisor fraco não ajudação。Burns 等人 descobriu que o PGR em NLP、国际象棋题和奖励建模任务一致于正的(约20%-80%),强模型利用预训先验"理解"的意图任务,超越了弱监督者的错误。

**Type:** Learn | **类型:** 学习
**Languages:** Python (stdlib, W2SG gap simulator) | **语言:** Python（标准库，W2SG 差距模拟器）
**Prerequisites:** Phase 18 · 01 (instruction-following), Phase 18 · 10 (AI Control), Phase 09 (RL foundations) | **前置知识:** Phase 18 · 01 (指令遵循), Phase 18 · 10 (AI 控制), Phase 09 (RL 基础)
**Time:** ~60 minutes | **时间:** ~60 分钟

> - Não .**【前置】**O que é que é que é o que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é
> - Não .**【类比】**W2SG = "小学生教中学生"── Se o estudante secundário puder aprender de um professor secundário, ele deve entender que o seu método pode ser ampliado para superhuman AI──PGR 指标(Performance Gap Recovered) = 弱监督弥合差距比例──Burns 2023 测出 PGR 约20-80%强模型能"理解"意图超越弱监督者的错误──
> 🤔 可扩展监督(debate/递归奖励建模) + W2SG 互补: 前者提升监督者能力,后者确保强模型从不完美监督中泛化──

## Objetivos de aprendizagem

- Defina a supervisão escalável e a generalização fraca a forte e explique como são complementares.

> Definir o controle e a vulnerabilidade a fortalecimento, e explicar como os dois se complementam.

- Descreva a configuração experimental de Burns et al. 2023: ajuste fino do GPT-4 usando rótulos do GPT-2.

> 描述 Burns 等人 2023 年的实验设置:使用GPT-2 产生的标签微调GPT-4──

- Explicar a métrica de diferença de desempenho recuperada (PGR) e o que ela mede.

> 解释性能差距恢复 (PGR) índice e seu conteúdo de medida:

- Indique os três principais mecanismos de supervisão escalável (debate, modelagem recorrente de recompensas, decomposição de tarefas) e um ponto forte de cada um.

> 列出三种主要可扩展监督机制 (三种主要可扩展监督机制) 辩论,递归奖励, 任务分解, 建设模, 任务分解) 及各自优点──

## O problema é o problema da introdução

Cada técnica de alinhamento até agora na Fase 18 assume que o supervisor pode avaliar o comportamento do modelo. Quando o modelo é super-humano, o supervisor é o elo fraco. A questão de supera alinhamento: um supervisor mais fraco pode produzir com confiança um modelo mais forte e alinhado?

> Fase 18 da fase 18 até agora, cada tipo de supervisor de tecnologia está supondo que pode avaliar o comportamento do modelo. Quando o modelo é super-humano, o supervisor é um fraco e fraco componente.

Burns et al. reduzem isso a uma configuração empírica operacional: supervisionar forte com fraco, medir quanto da capacidade do modelo forte sobrevive à supervisão fraca.

> Burns  et al. simplificou a sua configuração prática para operacionalização: com supervisão fraca, a capacidade de medir um modelo forte tem muito a sobreviver sob supervisão fraca. Não é uma solução super-preparada, mas é um agente que nos permite medir o progresso.

## O conceito central.

> **【中文解读】**Burns  et al. Configuração de experiência: weak模型 GPT-2 级别,强模型 GPT-4 级别,目标是强模型在金标签上限.流程:获取弱模型零样本预测 → 在弱标签上微调强模型 → 测量强微调模型准确率.

### W2SG: a configuração de Burns et al.

- Modelo fraco: classe GPT-2.
- Modelo forte: classe GPT-4.
- Objetivo: um limite de GPT-4 forte na tarefa.

Procedimento:
1. Obter as previsões de zero-shot do modelo fraco numa tarefa.
2. Ajustar o modelo forte em dados de marcas fracas.
3. Meter a precisão do modelo forte e perfeitamente ajustado.

> 流程:1. 获取弱模型在任务上的零样本预测――2. 在弱标签数据上微调强模型――3. 测量强微调模型的准确率――. 测量强微调模型的准确率――. 测量强微调模型的准确率――. 测量强微调模型的准确率――. 测量强微调模型的准确率――. 测量强微调模型的准确率――.

Linhas de base: precisão do modelo fraco, limite supervisionado do modelo forte em etiquetas de ouro.

> 基线: weak模型自身的准确率,强模型在金标签上监督上限──

Metrica de diferença: Gap Recovered (PGR) = (finamente ajustado - fraco) / (loft - fraco). PGR de 1,0 significa que a supervisão fraca fecha completamente a diferença; PGR de 0 significa que a supervisão fraca não ajudou.

> 差距指标: performance gap recovery (PGR) = ((微调后 - 弱) / ((上限 - 弱) ・PGR 为表示弱监督完全弥合差距;PGR 为 0 表示弱监督没有帮助。

### Burns et al. Resultados empíricos

Em todas as tarefas de PNL, xadrez-puzzle e modelagem de recompensas, o PGR foi consistentemente positivo: o modelo forte generalizou-se além dos erros do supervisor fraco.

> Na NLP, PGR foi generalizado em torno de 20% a 80% de PGR de tarefas específicas. O modelo forte foi "entendido" em uma etiqueta imperfeita, sendo complementado com um pre-treino prévio.

Limitações Burns et al. nota:
- A diferença entre fraco e forte aqui é a capacidade, não o alinhamento. O modelo fraco é alinhado; um modelo verdadeiramente sobre-humano pode ser alinhado por um humano, mas com uma diferença de capacidade muito maior.

> O fraco a forte diferença é capacidade, e não para si. O modelo fraco é para si. O modelo super-humano real pode ser comparado por humanos, mas a diferença de capacidade é muito maior.

- A generalização do modelo forte pode ser mais sobre as tarefas anteriores do que sobre a recuperação da intenção de verdade no fundo.

> A generalização do modelo forte pode ser mais sobre a experiência da missão, e não sobre a recuperação da realidade.

- A obtenção do conhecimento latente do modelo forte é o verdadeiro problema; a PGR mede uma operacionalização específica.

> O conhecimento potencial do modelo é o verdadeiro problema; o PGR mede uma operacionalização específica.

> **【拓展：三种可扩展监督机制 → 辩论/递归奖励建模/任务分解】**辩论(Irving 等人 2018): dois U 实例争论相反立场,弱评判者决定──归归奖励建模(Leike 等人 2018):U 帮助人类训练 U+1 的奖励模型,监督者的有效能力随模型增长──任务分解(Christiano 等人 2018):将硬任务分解成人类可检查的子任务,归归执行──每种机制都假设关于任务结构或中间组件对齐的某些东西──

### Supervisão em escalabilidade: três mecanismos

- **Debate (Irving et al. 2018).**Dois casos de U argumentam lados opostos; o juiz fraco decide. A suposição: encontrar uma resposta verdadeira convincente é mais fácil do que encontrar uma resposta falsa convincente. O trabalho recente de 2024-2025 (Khan et al., Michael et al.) mostra que o debate às vezes ajuda e às vezes não, e se ajuda depende da estrutura da tarefa.

> **辩论（Irving 等人 2018）。**Dois exemplos de U debatem contra a posição; fraco juiz decide. Suposição: encontrar uma resposta verdadeira convincente é mais fácil do que encontrar uma resposta falsa convincente.

- **Recursive Reward Modeling (Leike et al. 2018).**A U ajuda o ser humano a treinar o modelo de recompensa para a U+1.

> **递归奖励建模（Leike 等人 2018）。**U  ajudar humanos treinamento U + 1 奖励模型──监督者的有效能力随模型增长──

- **Task Decomposition (Christiano, Shlegeris, Amodei 2018).**Descompõe uma tarefa difícil em subtarefas que o ser humano pode verificar, recursivamente.

> **任务分解（Christiano, Shlegeris, Amodei 2018）。**Para resolver a questão, a tarefa dura deve ser sub-tarefa de análise humana.

Cada mecanismo assume algo sobre a estrutura da tarefa ou o alinhamento dos componentes intermediários.

> Cada mecanismo assume que a estrutura de tarefas ou os componentes intermédios são iguais.

### Por que a supervisão escalável e o W2SG são complementares

A superintendência escalavel aumenta a qualidade do sinal eficaz do superintendente.
O W2SG fecha a lacuna de qualquer sinal imperfeito que o superintendente possa fornecer.

> 可扩展监督提高监督人有效信号质量──弱到强泛化── qualquer diferença fechada entre os sinais imperfeitos que o supervisor pode fornecer──

Lang et al.  Debate Helps Weak-to-Strong Generalization (arXiv:2501.13124) combina-os: um protocolo de debate fornece melhores rótulos fracos, e o modelo forte é treinado nessas rótulos.

> Lang 等人 debate ajuda a fortalecer até fortalecer a generalização ((arXiv:2501.13124)) vai combinar os dois: debate protocol fornecer melhores marcadores fracos, forte modelo em treinar sobre esses marcadores.

> **【中文解读】**Organização Teatro:OpenAI's super super-equipos em 2024 Jan Leike 离职加入人类的后解散──但研究议程(可扩展监督、弱到强泛化、自动化对齐研究)

### O drama organizacional

A equipe de Superalinhamento da OpenAI foi dissolvida em maio de 2024 após a partida de Jan Leike para a Anthropic. A agenda (supervisão escaladora, W2SG, pesquisa de alinhamento automatizado) continuou na Anthropic e nos laboratórios acadêmicos  MATS (Lessão 28), Redwood (Lessão 10), Apollo (Lessão 8), METR (Lessão 28).

> O grupo de super-prefeitos da OpenAI em 2024 em maio Jan Leike 离职加入人类 后解散──研究议程(可扩展监督、弱到强泛化、自动化对齐研究) em Antropic 和学术实验室继续MATS、Redwood、Apollo、METR── estrutura da organização mudou; problemas de estudo não mudarão──

### Onde isto encaixa na Fase 18

As lições 6-10 descrevem a ameaça e o paradigma defensivo sob a suposição de que U é improvável. A lição 11 é o paradigma ofensivo: fazer com que o supervisor seja forte o suficiente para verificar o alinhamento de U. As lições 12-16 então se voltam para a ferramenta prática de avaliação adversária.

> Lições 6-10  Descrição de ameaças e hipóteses U não-confiável de defesa paradigma  Lição 11 é um paradigma positivo: fazer superintendente suficientemente forte para verificar U de um conjunto  Lições 12-16                                                                                                                                                                                                                                                                                                                                                                                                                                                                      

> **【拓展：辩论帮助弱到强泛化 → 2025 组合】**Lang 等人(arXiv:2501.13124, 2025 1 月) vai ampliar supervisão e debilitar para reforçar a generalização combinado: Protocolo de debate fornecerá melhores marcas fracas, forte modelo em treinar sobre essas marcas.

## Use-o com o framework implementado.
```figure
scalable-oversight
```

## Usá-lo

`code/main.py`Simula uma sintonia W2SG em uma tarefa sintética. O etiquetador fraco tem 70% de precisão com erros estruturados; o modelo forte tem um teto de 95% em etiquetas de ouro.

> `code/main.py`Em tarefas sintéticas simuladas W2SG 微调── taxa de precisão do marcador fraco 70% 带有结构性错误; strong模型在金标上上限为95%── você em weak标上微调强模型,测量PGR,并与强模型在金标和弱模型单独结果比较──

## Envia-o . Produto .

Esta lição produz`outputs/skill-w2sg-pgr.md`. Dada uma descrição da configuração de supervisão, identifica o supervisor fraco, o modelo forte, a qualidade da supervisão e calcula (ou solicita) a PGR. Marca se a alegação é "fraco pode supervisionar forte" ou "fraco + mecanismo de supervisão pode supervisionar forte".

> 本课产 出 `outputs/skill-w2sg-pgr.md`△ dados de supervisão configuração descrição, identificação de supervisor de baixa qualidade,并计算((或请求) PGR。

## Exercícios.

1. Corra .`code/main.py`. Relata PGR para fraca_acuração = 0,60, 0,70, 0,80. Explique a forma da curva PGR.

2. Modificar o rotulador fraco para ter um erro estruturado (por exemplo, sempre errado em uma classe de entrada específica). Aumente, diminui ou permanece a mesma PGR? Explique.

3. Leia Burns et al. 2023 Secção 4.3 (Tasks NLP). Reproduzir a intuição de "perda auxiliar de confiança": quando o modelo forte é mais confiante do que os rótulos fracos, quem ganha?

4. Desenhar um protocolo de supervisão escalável que combina debate e decomposição de tarefas para uma tarefa de engenharia de software. Nomear um modo de falha de cada componente e explicar como a combinação resolve ou não resolve cada um.

5. Articular o que falsificaria a afirmação de que "a generalização fraca a forte é um caminho viável para a superaligação".

## Termos-chave .

| Term | What people say | What it actually means |
|------|-----------------|------------------------|
| Scalable oversight | "making the overseer stronger" | Mechanisms that increase an overseer's ability to evaluate a more-capable model |
| W2SG | "weak supervises strong" | Fine-tuning a strong model on weak labels and measuring the capability recovered |
| PGR | "performance gap recovered" | (fine-tuned - weak) / (ceiling - weak); 1.0 = fully closed, 0 = no help |
| Debate | "two U instances argue" | Scalable oversight mechanism where a weak judge picks between two U defenders |
| RRM | "recursive reward modeling" | U helps train the reward model for U+1; overseer capability tracks U |
| Task decomposition | "sub-tasks the human checks" | Break a hard task into sub-tasks the human can verify, recursively |
| Superalignment | "aligning superhuman AI" | The research agenda concerned with aligning models the human cannot directly evaluate |

## Mais leitura 延伸阅读

- [Burns et al. — Weak-to-Strong Generalization (OpenAI 2023)](https://openai.com/index/weak-to-strong-generalization/) O papel W2SG
- [Irving, Christiano, Amodei — AI safety via debate (arXiv:1805.00899)](https://arxiv.org/abs/1805.00899) o mecanismo de debate
- [Leike et al. — Scalable agent alignment via reward modeling (arXiv:1811.07871)](https://arxiv.org/abs/1811.07871) Modelagem recorrente de recompensas
- [Khan et al. — Debating with More Persuasive LLMs Leads to More Truthful Answers (arXiv:2402.06782)](https://arxiv.org/abs/2402.06782) 2024 Estudo empírico do debate com debatedores mais fortes
- [Lang et al. — Debate Helps Weak-to-Strong Generalization (arXiv:2501.13124)](https://arxiv.org/abs/2501.13124) 2025 combinação de debates + W2SG
