# AlphaEvolve  Agentes de codificação evolucionária  AlphaEvolve  Agente de codificação evolutiva

> Combinar um modelo de codificação de fronteira com um ciclo evolutivo e um avaliador verificável por máquina. Deixe o ciclo correr o suficiente. Descobre um procedimento de multiplicação de matriz complexa 4x4 que usa 48 multiplicações escalares, a primeira melhoria em relação a Strassen em 56 anos. Também encontra uma heurística de agendamento Borg em todo o Google que recupera ~ 0,7% do computação de cluster na produção. A arquitetura é aborrecida de propósito. As vitórias vêm do rigor do avaliador.

> **【中文解读】**Para combinar o modelo de códigos de vanguarda com o avaliador de ciclo evolutivo e de máquina verificável, deixe o ciclo funcionar o suficiente. Ele descobriu um processo de multiplicidade de 4x4 de quadros de 48 vezes de escala, que ultrapassou a Strassen pela primeira vez em 56 anos. Ele também descobriu um Google Borg de todo o mundo, que recuperou cerca de 0,7% da produção em conjunto.

> **【拓展：进化算法 + LLM 的化学反应】**O algoritmo de evolução ([[variação+seleção+交叉]]) tem décadas de história, mas a tradição de variação assiduamente produz erros de linguagem em grandes processos. LLM como "variação inteligente" mudou isso: ele pode propor modificações racionais através da composição.

**Type:** Learn | **类型:** 学习
**Languages:** Python (stdlib, evolutionary-loop toy) | **语言:** Python（标准库，进化循环玩具）
**Prerequisites:** Phase 15 · 01 (long-horizon framing), Phase 15 · 02 (self-taught reasoning) | **前置知识:** Phase 15 · 01（长程框架），Phase 15 · 02（自我教学推理）
**Time:** ~60 minutes | **时间:** ~60 分钟

> - Não .**【前置】**學本節前請先掌握:Fase 15·01(长程 Agent) ‧Fase 15·02(STaR 自我改进) ‧进化算法基础(变异/交叉/选择) ‧AlphaEvolve = LLM 作为智能变异算子的进化算法──
> - Não .**【类比】**AlphaEvolve = "AI 实验室里的博士生群体"──传统进化算法 = 随机打字员(多数是乱码);AlphaEvolve = 一群 AI 博士生, cada um apresentou modificações significativas("试试把循环展开两倍"), avaliador running experiments打分,高分改进进入下一代种群──LLM 解决"如何提出合理变异",评估器解决"如何辨别伪"结合 56 anos de primeira revolução Strassen 矩阵乘法──
> 🤔 **【困惑】**P: Por que o AlphaEvolve pode superar os especialistas humanos? Porque ele corre milhões de vezes, cada vez com um verdadeiro padrão de referência verificação.

## O problema é o problema da introdução

Os grandes modelos de linguagem podem escrever código. Os algoritmos evolutivos podem pesquisar código. Ambos foram testados separadamente por décadas; ambos atingiram limites.

> O modelo de grande linguagem pode escrever código, o algoritmo evolutivo pode pesquisar no espaço de código.

O teto do LLM é confabulação: o modelo escreve código plausível que não faz o que afirma. O teto evolutivo é custo de pesquisa: mutações aleatórias sobre sintaxe raramente produzem programas compiláveis, muito menos melhores.

> O modelo de escrita de um código que parece razoável, mas não é conforme com o comportamento real. O modelo de desenvolvimento de um plano de aprendizagem é o custo de pesquisa.

O LLM propõe edições direcionadas a um banco de dados de programas; um avaliador automático marca cada variante; as variantes de pontuação alta se tornam pais para as gerações futuras. O LLM lida com a etapa cara de escrever código plausível; o avaliador pega as confabulações. O ciclo dura de horas a semanas.

> AlphaEvolve(Novikov 等人,DeepMind,arXiv:2506.13131,2025年6月) vai combinar os dois. LLM para base de dados de processos propõe edição específica; avaliador automático para cada variação; alta parte dos variações para se tornar o pai de gerações futuras.

> **【中文解读】**AlphaEvolve (Google DeepMind, 2025) vai aplicar algoritmos de evolução para o código de otimização. Ele mantém uma gama de processos, através de variações,交叉和选择代优化.

Resultados relatados: multiplicação de matriz complexa 4x4 de 48-escala-multiplicação (limite de 1969 de Straßsen foi 49), um heurística de agendamento Borg na produção do Google, um 32,5% de flashattention kernel speedup, melhorias de throughput de treinamento Gemini.

> 報告的結果:48 次标量乘法 4x4 复矩阵乘法(Strassen 1969 年的边界是 49),Google 生产中的 Borg调度启发式,32.5% 的 FlashAttention 内核加速,Gemini 训练吞吐量改进──

A arquitetura funciona porque o avaliador é verificável pela máquina. Não funciona onde o avaliador não está. Essa assimetria é a lição.

> Esta natureza de não-controlo é o núcleo deste curso: a estrutura é, portanto, eficaz, porque o avaliador é um campo de máquinas verificáveis; o avaliador é um campo de incrível, o ciclo é inefficiente.

## O conceito central.

### O ciclo.

1. Comece com um programa de sementes .`P_0`Isso é correto, mas suboptimo.
   Tradução do inglês:`P_0`Começa.
2. Manter um banco de dados de programas variantes, cada um marcado pelo avaliador.
   Tradução do inglês para tradução do inglês:维护一个变体程序数据库,每个变体由评估器打分.
3. Amostra de um ou mais pais da base de dados (em estilo MAP-elite ou baseado em ilhas).
   Tradução do inglês para "MAP-elite" (MAP-elite)
4. Promover o LLM (Gemini Flash para muitos candidatos, Gemini Pro para os mais difíceis) para produzir uma variante modificada do pai.
   Tradução do inglês para tradução do inglês para tradução do inglês para tradução do inglês para tradução do inglês para tradução do inglês para tradução do inglês para tradução do inglês para tradução do inglês para tradução do inglês para tradução do inglês para tradução do inglês para tradução do inglês para tradução do inglês para tradução do inglês para tradução do inglês para tradução do inglês para tradução do inglês para tradução do inglês para tradução do inglês para tradução do inglês para tradução do inglês para tradução do inglês para tradução do inglês para tradução do inglês para tradução do inglês para o inglês para o inglês para o inglês para o inglês para o inglês para o inglês para o inglês para o inglês para o inglês para o inglês para o inglês para o inglês para o inglês para o inglês para o inglês para o inglês para o inglês para o inglês para o inglês para o inglês para o inglês para o inglês para o inglês para o inglês para o inglês para o inglês para o inglês para o inglês para o inglês para o inglês para o inglês para o inglês para o o inglês para o o inglês para o inglês para o o o o o o o o o o o o o o o o o o o o o o o o o o o o o o o o o o o o o o o o o o o o o o o o o o o o o o o o o o o o o o o o o o o o o o o o o o o o o o o o o o o o o o o o o o o o o o o o o o o o o o o o o o o o o o o o o o o o o o o o o o o o o o o o o o o o o o o o o o o o o o o o o o o o o o o o o o o o o o o o o o o o o o o o o o o o o o o o o o o o o o o o o o o o o o o o o o o o o o o o o o o o o o o o o o o o
5. Compile, execute e avalia a variante no avaliador de tempo.
   Tradução em inglês: 编译、运行并保留评估器上评估变体──
6. Insira na base de dados selecionada por seu ponto e vector de características.
   Tradução do inglês para inglês: Input into the database
7. Repito. - Não.
   Tradução:C.

O modelo é um modelo de trabalho que é um modelo de trabalho de trabalho, que é a de proporcionar uma mudança direcionada que pode melhorar a pontuação.

> O modelo é um modelo de trabalho que pode aumentar o número de mudanças específicas. Segundo, o banco de dados é estruturado.

### O que torna o avaliador não negociável

As vitórias do AlphaEvolve vêm de domínios onde o avaliador é rápido, determinista e difícil de jogar:

> As vitórias da AlphaEvolve vêm de áreas de avaliação rápida, determinante e difícil de alcançar:

- **Matrix multiplication algorithm**O teste unitário multiplica matrizes e verifica a igualdade de forma bit-identical.
  Tradução:**矩阵乘法算法** um teste de unidades de uma matriz e de uma unidade de exame de cada um.
- **Borg scheduling heuristic**O simulador de nível de produção que reproduz a carga histórica do cluster e mede o cálculo desperdiçado.
  Tradução:**Borg 调度启发式** Uma máquina de produção, re-lançamento de históricos e de pesquisa de custos.
- **FlashAttention kernel**: um teste de correcção mais um indicador de relógio de parede em hardware real.
  Tradução:**FlashAttention 内核**Teste de verdade, adicionado a hardware real.
- **Gemini training throughput**: GPU-segundos por passo.
  Tradução:**Gemini 训练吞吐量** Messa o número de segundos de GPU por passo.

Em cada caso, o avaliador capta a classe de erros de LLM que de outra forma dominariam: alegações de corretão confabuladas, alegações de desempenho que desaparecem no hardware e falhas de bordo.

> Em cada caso, o avaliador captura o que, de outro modo, ocupará a posição dominante LLM  erro: declaração de autenticidade falsa  declaração de desempenho desaparecida no hardware e falha de situação de margem 

### O hacking de recompensas é a outra face daquela declaração.

A evolução otimiza para qualquer medida que o avaliador mede. Se o avaliador é imperfeito, o loop encontrará a imperfeição. Em um domínio não verificado o loop otimiza para a característica de superfície, não o comportamento pretendido.

>  Evolução de qualquer coisa na medida de um avaliador de otimização. Se o avaliador não for perfeito, o ciclo encontrará algo de imperfeito. Em áreas não verificadas, o ciclo irá melhorar as características da superfície e não o comportamento esperado.

DeepMind sinaliza isso explicitamente no artigo: Os sucessos do AlphaEvolve transferem-se apenas para domínios onde o rigor do avaliador corresponde à ambição da pesquisa.

> DeepMind em seu artigo afirma que o sucesso da AlphaEvolve só pode ser transferido para um campo de avaliação rigorosa e compatível com a busca.

Exemplos concretos de hacking de recompensas em ciclos de busca de código:

> Exemplos concretos de mudanças no ciclo de busca de 2025-2026:

- Objetivos de otimização que recompensam "tempo para completar" recompensaram a apresentação de soluções vazias.
  Tradução do inglês para "Completar o tempo"
- Os resultados de referência que recompensam a correcção sob o teste recompensaram os testes de memória e o excesso de correspondência.
  Tradução do inglês para tradução do inglês: Reward Testing Correctness
- Um proxy de "qualidade de código" recompensou a remoção de comentários e a reescritura de nomes de variáveis, sem mudança semântica.
  Tradução do inglês para "Code Quality"

A solução no AlphaEvolve: enviar um avaliador que o LLM nunca viu, com insumos gerados no momento da avaliação.

> AlphaEvolve's revision: entregar um LLM de um avaliador de reservas nunca visto, ingressar em avaliação gerada.

### Por que a busca de LLM + bate sozinha ?

O LLM pode produzir modificações compilaveis e semânticamente plausíveis. Uma mutação aleatória GA em um arquivo Python de 2000 linhas quase sempre produz erros de sintaxe. O LLM também concentra a pesquisa em bairros plausíveis (mudança de uma função, não bytes aleatórios), o que reduz drasticamente as chamadas de avaliador desperdiçadas.

> LLM pode produzir modificações compilagíveis ∞ semânticamente razoáveis ∞ em 2000 行 Python 文件随机变异 GA 几乎总产生语法错误∞ LLM também irá se concentrar em áreas vizinhas razoáveis ∞ modificar uma função, e não um字节随机), o que reduz significativamente o desperdício de manipulação de avaliadores ∞

O avaliador, por sua vez, capta as confabulações do LLM. Os LLM afirmarão com confiança que uma função "é O(n log n) no limite" quando é realmente O ((n^2); um benchmark de relógio de parede resolve a questão.

> 评估器反过来捕获 LLM的虚构──LLM 会自信声称一个函数"极限下是 O(n log n)",而实际是 O(n2);墙钟基准让问题尘埃落定──

### Onde AlphaEvolve encaixa na pilha de fronteira.

| System | Generator | Evaluator | Domain | Example win |
|---|---|---|---|---|
| 系统 | 生成器 | 评估器 | 领域 | 示例胜利 |
| AlphaEvolve | Gemini | correctness + benchmark | algorithms, kernels, schedulers | 48-mul 4x4 matmul |
| AlphaEvolve | Gemini | 正确性 + 基准 | 算法、内核、调度器 | 48 次乘法 4x4 矩阵乘法 |
| FunSearch (DeepMind, 2023) | PaLM / Codey | correctness | combinatorial math | cap-set lower bounds |
| FunSearch（DeepMind，2023） | PaLM / Codey | 正确性 | 组合数学 | cap-set 下界 |
| AI Scientist v2 (Sakana, L5) | GPT/Claude | LLM critique + experiment | ML research | ICLR workshop paper |
| AI Scientist v2（Sakana，L5） | GPT/Claude | LLM 评审 + 实验 | ML 研究 | ICLR 工作坊论文 |
| Darwin Godel Machine (L4) | agent scaffolding | SWE-bench / Polyglot | agent code | 20% → 50% SWE-bench |
| Darwin Godel Machine（L4） | Agent 脚手架 | SWE-bench / Polyglot | Agent 代码 | SWE-bench 20% → 50% |

Todas as quatro são variações da mesma receita: gerador mais avaliador, loop. As diferenças são o que o avaliador classifica e quão rigoroso é.

> Quatro são variantes da mesma configuração: gerador, avaliador, ciclo. A diferença é no que avaliador avalia e quanto rigoroso.
```figure
alphaevolve-loop
```

## Usá-lo

## Use-o com o framework implementado.

`code/main.py`Implementa um ciclo mínimo semelhante ao AlphaEvolve sobre um problema de regressão simbólica de brinquedo.

> `code/main.py`Em um problema de regresso de símbolos de brinquedo, realizou um ciclo mínimo semelhante ao AlphaEvolve.

O "LLM" é um proxy stdlib que propõe pequenas mutações sintáticas para um programa que calcula uma função-alvo.

> "LLM" é um agente de base de padrões, que propõe pequenas variações de linguagem para um programa de função de objetivo de cálculo.

- Vigiar:

> Observação:

- Como a melhor pontuação melhora ao longo das gerações.
  Tradução do inglês: best分数如何在世代中提升──
- Como uma rede de elite MAP mantém diversas soluções vivas para que o ciclo não converja em um mínimo local.
  MAP-elite 网格 如何保持多样化解存活,让循环不收到局部最小──
- Como a remoção do teste prolongado (avaliador de treinamento só) permite que o loop se encaixe espetacularmente.
  Tradução do inglês para tradução do inglês: How to make a loop catastrophe naturally over-adapted?

## Envia-o . Produto .

`outputs/skill-evaluator-rigor-audit.md`É a condição prévia para considerar um ciclo de estilo AlphaEvolve num novo domínio: o seu avaliador realmente detecta os falhas que lhe importam?

> `outputs/skill-evaluator-rigor-audit.md`É uma nova área para considerar como um pressuposto do ciclo AlphaEvolve: o seu avaliador realmente capturou o seu fracasso?

## Exercícios.

1. Corra .`code/main.py`- Observe a melhor trajetória de pontuação.`--no-holdout`) e re-exercício.
   Tradução: 运行`code/main.py` record best分数轨迹──禁用保留评估器 `--no-holdout`) re-operação.

2. Leia a Seção 3 do artigo AlphaEvolve sobre a grade MAP-elites.
   Tradução do idioma japonês:阅读AlphaEvolve 论文第 3 节关于MAP-elite 网格──为新问题(例如编译器优化遍次)设计一个保持搜索多样性的特征向量描述符──

3. O resultado de 48-multiplicação 4x4 melhorou no limite de 49-mul de Strassen após 56 anos.
   O resultado da 4x4 da prática de 48 vezes foi a melhoria de 49 vezes da linha de fronteira de Strassen, 56 anos depois.

4. Propõe um domínio onde o AlphaEvolve falha, identifique exatamente onde o avaliador rompe e porquê.
   Chinese Language Translation:提议一个 AlphaEvolve 会失败的领域──精确指出评估器在哪里失败以及原因──

5. Para um domínio que conheça, escreva a assinatura do avaliador que você usaria. Incluir (a) condições de correção, (b) métrica de desempenho, (c) regra de geração de entrada prolongada, (d) pelo menos um check anti-reward hacking.
   Tradução do inglês para inglês: For You Know, write out the assessment machine signature you will use.

## Termos-chave .

| Term | What people say | What it actually means |
|---|---|---|
| 术语 | 通俗说法 | 实际含义 |
| AlphaEvolve | "DeepMind's evolutionary coding agent" | Gemini + program database + machine-checkable evaluator |
| AlphaEvolve | "DeepMind 的进化编码 Agent" | Gemini + 程序数据库 + 机器可检查评估器 |
| MAP-elites | "Diversity-preserving archive" | Grid keyed by feature vectors; each cell holds the best variant with that descriptor |
| MAP-elites | "保持多样性的档案" | 以特征向量为键的网格；每个单元持有具有该描述符的最佳变体 |
| Island model | "Parallel evolution subpopulations" | Independent populations that migrate periodically; prevents premature convergence |
| 岛屿模型 | "并行进化子种群" | 定期迁移的独立种群；防止过早收敛 |
| Machine-checkable evaluator | "Deterministic oracle" | A unit test, simulator, or benchmark the LLM cannot fake — a prerequisite for this loop |
| 机器可检查评估器 | "确定性预言机" | LLM 无法伪造的单元测试、模拟器或基准——此循环的前提 |
| Reward hacking | "Optimizing the measure, not the goal" | Loop finds a way to maximize score without doing the intended task |
| 奖励篡改 | "优化度量而非目标" | 循环找到一种方法在不执行预期任务的情况下最大化分数 |
| Seed program | "The starting point" | An initial correct-but-suboptimal program the loop evolves from |
| 种子程序 | "起点" | 循环从中演化的初始正确但次优的程序 |
| Held-out evaluator | "Evaluation data the LLM never saw" | Inputs generated at evaluation time to prevent memorization |
| 保留评估器 | "LLM 从未见过的评估数据" | 评估时生成的输入以防止记忆 |

## Mais leitura 延伸阅读

- [Novikov et al. (2025). AlphaEvolve: A coding agent for scientific and algorithmic discovery](https://arxiv.org/abs/2506.13131)- O papel completo.
  Tradução do português:
- [DeepMind blog on AlphaEvolve](https://deepmind.google/blog/alphaevolve-a-gemini-powered-coding-agent-for-designing-advanced-algorithms/) O fornecedor com resultados.
  Chinese: 厂商撰文及结果──
- [AlphaEvolve results repository](https://github.com/google-deepmind/alphaevolve_results)Algoritmos descobertos, incluindo o matmul 4x4 de 48-mul.
  O armazém de algoritmos encontrados, incluindo 48 vezes multiplicada 4x4 矩阵乘法──
- [Romera-Paredes et al. (2023). Mathematical discoveries from program search with LLMs (FunSearch)](https://www.nature.com/articles/s41586-023-06924-6) o sistema anterior.
  Tradução do inglês:
- [Anthropic — Responsible Scaling Policy v3.0 (Feb 2026)](https://anthropic.com/responsible-scaling-policy/rsp-v3-0) define a autonomia do avaliador como uma direcção-chave da investigação.
  Tradução do inglês para o inglês:将评估器约束的自主性作为关键研究方向.
