# Planejamento com HTN e Pesquisa Evolucional .

> O planejamento simbólico lida com os casos em que o plano é provavelmente correto. A pesquisa de código evolutivo lida com os casos em que a função de fitness é verificável pela máquina. ChatHTN (2025) e AlphaEvolve (2025) mostram o que cada um desbloqueia quando combinado com um LLM.

> **【中文解读】**O programa de processamento de código-fonte pode ser comprovado como sendo verdadeiro.

**Type:** Build | **类型:** 构建
**Languages:** Python (stdlib) | **语言:** Python (标准库)
**Prerequisites:** Phase 14 · 02 (ReWOO and Plan-and-Execute) | **前置知识:** Phase 14 · 02 (ReWOO 与计划-执行)
**Time:** ~75 minutes | **时间:** ~75 分钟

## Objetivos de aprendizagem

- Explicar as redes de tarefas hierárquicas: tarefas, métodos, operadores, pré-condições, efeitos.
  Tradução do inglês para tradução inglesa: explicação de um nível de tarefas:
- Descreva o ciclo híbrido de ChatHTN  pesquisa simbólica com decomposição de volta do LLM.
  Tradução do inglês para tradução do inglês: ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎
- Explica o ciclo evolutivo do AlphaEvolve e porque só funciona com um avaliador programático.
  Tradução do inglês para tradução do inglês: Explain AlphaEvolve's evolutionary cycle and why it only works when there is a processorized assessment machine.
- Implementar um planeador de brinquedos HTN e uma pesquisa evolutiva de brinquedos em Stdlib.
  Tradução do inglês para Chinês: using standard library implement toy tools HTN 规划器和玩具进化搜索。

## O problema é o problema da introdução

ReWOO (Lessão 02), Planear e Executa e ReAct cobrem a maioria dos planos de agentes.

> ReWOO(第 2 课) 、Plan-and-Execute 和 ReAct 覆盖了大多数 Agent 规划──两种它们不能很好覆盖的情况:

1. **Plans with provable correctness.**A programação, o itinerário de voo, os fluxos de trabalho de conformidade  o plano deve ser sólido por construção.
   Tradução:**可证明正确性的计划。**O plano de planejamento de rotação de voo e de conformidade deve ser confiável na construção.
2. **Optimizations with a machine-checkable fitness function.**Multiplicação de matriz, planejamento heurística, passes de compilador  o objetivo não é "um plano correto" mas "o melhor plano".
   Tradução:**有机器可检查适应度函数的优化。**O objetivo não é "um plano correcto" mas "o melhor plano".

> **【中文解读】**O programa de planejamento de agentes  pode ser dividido em duas principais categorias:                                                                                                                                                                                                                                                     

O planejamento HTN e o AlphaEvolve resolvem os dois problemas diferentes.

> HTN 规划和 AlphaEvolve 解决两个不同的问题──两者都将 LLM用作放大器而非替代品──

> **【拓展：2026 年 Agent 规划的前沿】**AlphaEvolve e Darwin-Godel Machine vão aplicar algoritmos de desenvolvimento para o próprio Agente                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                         

> - Não .**【前置】**必須先通過Fase 14·02 (ReWOO/Plan-and-Execute) HTN é sua versão "rigidamente formalizada";以及基本的经典 AI 规划知识 (status,前置条件,效果) ── Se você não ouviu STRIPS ou PDDL, sugere primeiro补一两节"经典符号 AI"教程本节的"可证明正确性"依赖于这个形式化语言──

## O conceito central.

### Redes de tarefas hierárquicas

Uma HTN é:

> HTN é:

- **Tasks** composto (a ser decomposto) e primitivo (executivo direto).
  Tradução:**任务**复合(待分解)和原始(直接可执行)
- **Methods** formas de decompor uma tarefa composta em subtarefas, com condições prévias.
  Tradução:**方法**将复合任务分解为子任务的方式,带前置条件――
- **Operators** Ações primitivas com condições prévias e efeitos.
  Tradução:**操作符**带前置条件和效果的原始动作──
- **State** um conjunto de fatos.
  Tradução:**状态**一组事实──

Planejamento: dada uma tarefa-alvo e um estado inicial, encontrar uma decomposição em operadores primitivos cujas pré-condições são satisfeitas em sequência.

> 规划: dado um objetivo determinado tarefa e estado inicial, encontrar um esquema de descomposição para o operador original, suas condições de pré-posição em ordem de satisfação.

O HTN é mais antigo do que os LLM e ainda é a referência para planos provavelmente corretos.

> O HTN é mais antigo do que o LLM, ainda é um referente do programa correto.

### ChatHTN (Gopalakrishnan et al., 2025)

ChatHTN (arXiv:2505.11814) interliga HTN simbólico com consultas de LLM:

> ChatHTN(arXiv:2505.11814)交替进行符号 HTN 和 LLM 查询:

1. Tente decompor a tarefa composta atual com métodos existentes.
   Tradução do inglês para tradução do inglês: try using existing methods to break down current complex tasks。
2. Se não for aplicado nenhum método, pergunte ao LLM: "como se descompõe?`task`em estado`s`"O que é isso?
   Se não houver um método adequado, pergunte LLM:" em estado `s`Como é que vais desintegrar ?`task`"O que é isso?
3. Traduzir a resposta do LLM em subtarefas candidatas.
   Tradução do inglês para "L.L.M".
4. Validar contra o esquema do operador; rejeitar descomposições inválidas.
   O que é que é o "desenvolvimento" do sistema de controle?
5. Recurso.
   Tradução do português:递归――

A afirmação central do artigo: cada plano produzido é provavelmente sólido porque as sugestões de LLM só entram como decomposições candidatas, nunca como edições diretas de planos.

> - Não .**【类比】**ChatHTN 像严格的审计员 (严格的审计员) 符号层) + 创意实习生 (创意实习生) LLM (实习生提建议:"Eu acho que este objetivo pode ser desintegrado assim..."审计员严格检查:"Se as condições de pré-imposição da sua sub-tarefa estão em estado atual?**结果**Todos os planos de adoção final foram auditados, a sua fiabilidade é garantida.

> 论文的核心主张: Cada plano que surge pode ser provado como confiável, pois o LLM 建议只作为候选分进入,从不作为直接计划编辑;;

Aprendizagem de métodos on-line (OpenReview `gwYEDY9j2x`O programa de acompanhamento de 2025) adiciona um aprendiz que generaliza as decomposições produzidas pelo LLM por regressão  reduzindo a frequência de consulta do LLM até 75%.

> Em 2025, o programa de aprendizagem LLM                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                   

### AlphaEvolve (Novikov et al., 2025)

AlphaEvolve (arXiv:2506.13131, DeepMind, junho 2025) é uma besta diferente: pesquisa de código evolutivo orquestrada por um conjunto Gemini 2.0 Flash / Pro.

> AlphaEvolve ((arXiv:2506.13131,DeepMind,2025 年 6 月) é uma existência diferente: por Gemini 2.0 Flash/Pro 集群编排的进化代码搜索──

Loop:

> 循环:

1. Comece com um programa de sementes + um avaliador programático (retorna uma pontuação de aptidão).
   Tradução do inglês: from种子程序 + 程序化评估器 (→ "título original")
2. O conjunto de LLM propõe mutações.
   O LLM 集群提出变异──
3. Faça as mutações através do avaliador.
   Tradução do inglês:                                                                                                                                                                                                                                                            
4. Mantém o melhor, muta novamente.
   中文翻译:保留最好的;再次变异──

Ganhos publicados:

> outro resultado publicado:

- Primeira melhoria em relação a Strassen para a multiplicação de matriz complexa 4x4 em 56 anos (48 multiplicações escalares).
  Chinese Translation: 56 anos para a primeira vez em 4x4 复矩阵乘法 Strassen 算法(48 次标量乘法)
- 0,7% recuperou o computador do Google através de uma heurística de programação Borg.
  Por meio de Borg 调度启发式回收 0.7% do Google 计算资源──
- 32% de aceleração da FlashAttention numa carga de trabalho de fronteira.
  Tradução do inglês:

A restrição dura: a função de fitness deve ser verificável pela máquina.

> ️ **【易错点】**Colocar AlphaEvolve 套到"创意写作优化"上让LLM usar algoritmo de evolução para escrever小说, usar LLM 评分作为健身──**后果**Não recebe, porque a função de fitness em si é LLM (随机+不稳定),**一行修复**A partir de agora, o sistema de gestão de dados é mais fácil de usar.

> 硬约束: a função de adaptação deve ser de máquina verificável.

### Quando utilizar qual

| Problem class | Use | Why |
|---------------|-----|-----|
| 问题类别 | 使用 | 原因 |
| Scheduling with hard constraints | HTN + ChatHTN | Provable soundness / 可证明的可靠性 |
| Compiler optimization | AlphaEvolve | Machine-checkable fitness / 机器可检查的适应度 |
| Multi-step task execution | ReAct / ReWOO | LLM in the loop, no formal guarantees / LLM 在循环中，无形式化保证 |
| Code improvement with tests | AlphaEvolve | Tests are the evaluator / 测试即评估器 |
| Policy-bound automation | HTN | Preconditions encode policy / 前置条件编码策略 |

### Onde este padrão vai mal

- **HTN without operators.**Sem esquemas de pré-condição/efeito, a alegação de solidez desmorona. "LLM sugere decomposição" do ChatHTN exige que o esquema rejeite movimentos inválidos.
  Tradução:**没有操作符的 HTN。** não há condições pré-impostas/modelo de efeito, declarações de fiabilidade já caíram.
- **AlphaEvolve without a real evaluator.**"Pergunte ao Mestrado em Direito se o código é melhor" não é uma função de fitness.
  Tradução:**没有真正评估器的 AlphaEvolve。**"Question LLM 代码是否更好" não é uma função de adaptação.
- **Over-engineering.**A maioria das tarefas de agentes não precisam de nada.
  Tradução:**过度工程。**A maioria dos agentes não precisa de qualquer um.

> 🤔 **【困惑】**P: ChatHTN 论文说"LLM 只是提建议不直接进计划"这跟LangChain Agent 调用工具不是一回事吗? A: 不一样.

## Construí-lo.
```figure
htn-tree-expand
```

## Construí-lo

`code/main.py`Implementa dois brinquedos:

> `code/main.py`Realizei dois brinquedos:

- Um planejador de HTN com operadores, métodos, pré-condições, efeitos e um `LLMFallback`O LLM é um decomposador scriptado, o que faz com que o planejador seja executado offline.
  Tradução em inglês: a standard library HTN 规划器,带操作符、方法、前置条件、效果和当没有方法匹配复合任务时触发的`LLMFallback`"LLM" é um script-decomposer, planejador disponível para operação
- Uma busca evolutiva em programas aritméticos: crescer expressões cuja produção minimiza`|f(x) - target|`O avaliador é determinista.
  Tradução do inglês para inglês:`|f(x) - target|`Em testes de conjunto, a expressão mínima é definida.

- É o que é ?

> 运行:

```
python3 code/main.py
```

O rastro mostra o planejador HTN desintegrando uma tarefa composta (com um retorno de LLM no plano médio) e o ciclo evolutivo convergindo em uma expressão-alvo.

> 轨迹显示 HTN 规划器分解复合任务(带中途 LLM 回退) 和进化循环收到目标表达式──

## Use-o com o framework implementado.

- **HTN planners**- Não .`pyhop`- Não .`SHOP3`, ou construir o seu próprio para a aplicação de políticas específicas de domínio.
  Tradução:**HTN 规划器**`pyhop`- Não.`SHOP3`, ou para estratégias específicas de domínio para executar a sua própria construção.
- **ChatHTN** código de investigação; o padrão (símbolo + LLM fallback) é portado de forma limpa a qualquer planejador HTN.
  Tradução:**ChatHTN**研究代码;模式(符号 + LLM 回退)可干净地移植到任何HTN 规划器──
- **AlphaEvolve** Papel DeepMind; o padrão (ensemble + evaluator) é reprodutivo.
  Tradução:**AlphaEvolve**DeepMind 论文;模式(集群 + 评估器)可复现──OpenEvolve 和类似开源分支正在涌现──
- **Agent frameworks**Não se deve construir ainda um HTN de primeira classe ou um AlphaEvolve.
  Tradução:**Agent 框架** Atualmente não existe um HTN ou AlphaEvolve integrado.

## Envia-o . Produto .

`outputs/skill-hybrid-planner.md`gera um andamio de planejamento híbrido (HTN ou evolutivo) com o papel do MLL explicitamente definido.

> `outputs/skill-hybrid-planner.md`O que é o que é o que é o que é o que é o que é o que é o que é o que é o que é o que é o que é o que é o que é o que é o que é o que é o que é o que é o que é o que é o que é o que é o que é o que é o que é o que é o que é o que é o que é o que é o que é o que é o que é o que é o que é o que é?

## Exercícios.

1. Extender o planejador de HTN com retrocesso: quando a post-condição do operador falhar no tempo de execução, recuar e tentar o próximo método.
   Chinese Translation:为 HTN 规划器添加回溯: quando as condições de supressão do operador estiverem em funcionamento quando não estiverem em funcionamento, volte a rolar e tente o próximo método.
2. Adicionar um cache do método LLM ao ChatHTN: quando o LLM descompõe a tarefa `T`em padrão de estado `P`Reverifique a biblioteca de métodos na próxima chamada.
   Tradução do inglês para tradução do inglês para tradução do inglês para tradução do inglês para tradução do inglês para tradução do inglês para tradução do inglês para tradução do inglês para tradução do inglês para tradução do inglês para tradução do inglês para tradução do inglês para tradução do inglês para tradução do inglês para tradução do inglês para tradução do inglês para tradução do inglês para tradução do inglês para tradução do inglês para tradução do inglês para tradução do inglês para o inglês para tradução do inglês para o inglês para o inglês para o inglês para o inglês para o inglês para o inglês para o inglês para o inglês para o inglês para o inglês para o inglês para o árabe para o árabe para o árabe para o árabe para o árabe   ภาษา as ánglish: ภาษา as as su su anhêêêêêêêêêêêêêêêêêêêêêêêêêêêêêêêêêêêêêêêêêêêêêêêêêêêêêêêêêêêêêêêêêêêêêêêêêêêêêêêêêêêêêêêêêêêêêêêêêêêêêêêêêêêêêêêêêêêêêêêêêêêêêêêêêêêêêêêêêêêêêêêêêêêêêêêêêêêêêêêêêêêêêêêêêêêêêêêêêêêêêêêêêêêêêêêêêêêêêêêêêêêêêêêêêêêêêêêêêêêêêêêêêêêêêêêêêêêêêêêêêêêêêêêêêêêêêêêêêêêêêêêêêêêêêêêêêêêêêêêêêêêêêêêêêêêêêêêêêêêê`P`- Não .`T`时,储存结果──下次调用时先重新检查方法库──
3. Troque o evaluador de pesquisa evolutiva para um conjunto de testes real. Desenvolva uma função de classificação que passa por 20 casos de teste; informe gerações para a convergência.
   Tradução do inglês para tradução livre:将进化搜索评估器替换为真实测试套件──进化一个通过 20 试用例的排序函数;报告收代数──
4. Leia as notas de design de avaliador do AlphaEvolve. Desenhe um avaliador para um domínio que você se importa (otimizar a consulta SQL, minimizar a série de testes, implementar YAML).
   Tradução do inglês para o inglês:PDF, tradução do inglês:PDF, tradução do inglês:PDF, tradução do inglês:PDF, tradução do inglês:PDF, tradução do inglês:PDF, tradução do inglês:PDF, tradução do inglês:PDF, tradução do inglês:PDF, tradução do inglês:PDF, tradução do inglês:PDF, tradução do inglês:PDF, tradução do inglês:PDF, tradução do inglês:PDF, tradução do inglês:PDF, tradução do inglês:PDF, tradução do inglês:PDF, tradução do inglês:PDF, tradução do inglês:PDF, tradução do inglês:PDF, tradução do inglês:PDF, tradução do inglês:PDF, tradução do inglês:PDF, tradução do inglês:PDF, tradução do inglês:PDF, tradução do inglês:PDF, tradução do inglês:PDF, tradução do inglês:PDF, tradução do inglês:PDF, tradução do inglês:
5. Combine: use HTN para decompor uma tarefa composta em subtarefas, em seguida, use a pesquisa evolutiva no operador primitivo de cada subtarefa. Onde brilha, onde é super-engenharia?
   O que é que você quer dizer com o seu computador?

## Termos-chave .

| Term | What people say | What it actually means |
|------|-----------------|-----------------------|
| 术语 | 通俗说法 | 实际含义 |
| HTN | "Hierarchical planner" / "分层规划器" | Task decomposition with operators, preconditions, effects / 带操作符、前置条件、效果的任务分解 |
| Method | "Decomposition rule" / "分解规则" | Way to break a compound task into subtasks / 将复合任务分解为子任务的方式 |
| Operator | "Primitive action" / "原始动作" | Concrete step with precondition and effect / 带前置条件和效果的具体步骤 |
| ChatHTN | "LLM + HTN" / "LLM + HTN" | Symbolic planner asks LLM when no method matches / 符号规划器在没有方法匹配时询问 LLM |
| AlphaEvolve | "Evolutionary code search" / "进化代码搜索" | Ensemble LLMs mutate code; deterministic evaluator selects / LLM 集群变异代码；确定性评估器选择 |
| Fitness function | "Evaluator" / "评估器" | Deterministic, machine-checkable score over outputs / 输出上的确定性、机器可检查分数 |
| Online method learning | "Cached LLM decomposition" / "缓存的 LLM 分解" | Store + generalize LLM plans to cut query cost / 存储并泛化 LLM 计划以降低查询成本 |

## Mais leitura 延伸阅读

- [Gopalakrishnan et al., ChatHTN (arXiv:2505.11814)](https://arxiv.org/abs/2505.11814) Planeador híbrido de LLM
  Tradução do inglês para tradução do inglês: ChatHTN 论文符号 + LLM 混合规划器。
- [Novikov et al., AlphaEvolve (arXiv:2506.13131)](https://arxiv.org/abs/2506.13131) Pesquisa de código evolutivo com mutações de LLM
  Tradução do português:AlphaEvolve 论文带 LLM 变异的进化代码搜索──
- [Anthropic, Building Effective Agents](https://www.anthropic.com/research/building-effective-agents) quando chegar a um planejador versus um ciclo simples
  Tradução do inglês para Chinês:Antropic 关于构建有效代理的指导何时使用规划器而非简单循环──
