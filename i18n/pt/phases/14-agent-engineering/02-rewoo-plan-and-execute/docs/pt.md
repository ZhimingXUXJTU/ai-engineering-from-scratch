# ReWOO e Plano-e-Executar: Planejamento Desacoplado .

> ReAct interliga pensamento e ação em um fluxo. ReWOO os separa: um grande plano de frente, em seguida, executar. 5x menos tokens, +4% de precisão no HotpotQA, e você pode destilar o planejador em um modelo 7B. Plan-and-Execute generalizou-o; Plan-and-Act escalado para a navegação na web.

> **【中文解读】**ReAct em um fluxo de transformação de pensamentos e ações. ReWOO irá separá-los: primeiro, uma vez, elaborar um plano completo, depois executar.

> **【拓展：ReWOO → 现代 Agent 架构】**Entre os cinco modelos de trabalho da Antropic "Building Effective Agents", o modelo de planejamento-execução é um dos principais.

> - Não .**【前置】**精通本节前 請先掌握:Phase 14·01(Agent Loop / ReAct 循环) You must understand ReAct's "thought-action-observe" exchange mode, because ReWOO is for understanding ReAct's token Second Growth problem;以及 the basic diagrammatic concept (((DAG、拓排序), is not familiar DAG 会卡在"dependência解析"那一步──

**Type:** Build | **类型:** 构建
**Languages:** Python (stdlib) | **语言:** Python (标准库)
**Prerequisites:** Phase 14 · 01 (Agent Loop) | **前置知识:** Phase 14 · 01 (Agent 循环)
**Time:** ~60 minutes | **时间:** ~60 分钟

## Objetivos de aprendizagem

- Explique por que a divisão Planner / Worker / Solver da ReWOO salva tokens e melhora a robustez sobre o loop interleaved da ReAct.
  Tradução do inglês para tradução do inglês: ReWOO's Planner/工作器/求解器分离能节省代币并比 ReAct's交换循环更健壮.
- Implementar um plano DAG, um executor de ordem dependência e um solvente que compõe as saídas de trabalho  todos os stdlib.
  Tradução do inglês para tradução do inglês: implement plan DAG、 dependência de ordem executador e conjunto de trabalho
- Decidir quando uma tarefa deve ser executada como plano-depois-execução vs. ReAct interleaved, usando o enquadramento de 2026 "cinco padrões de fluxo de trabalho" (Antropic).
  Tradução do inglês para Chinês: usando o "五种工作流模式" framework de 2026 年 (Antropic), determinação das tarefas é usar o plano-execução ou o cambio de ReAct.
- Reconhecer quando os dados sintéticos do plano do Plan-and-Act são necessários para tarefas de longo prazo na web ou móveis.
  Chinês Tradução:识别何时需要计划和行动的合成计划数据来处理长程网页或移动任务──

## O problema é o problema da introdução

O loop de pensamento-ação-observação interligado do ReAct é simples e flexível, mas cada chamada de ferramenta tem que levar o contexto anterior completo  incluindo cada pensamento anterior. O uso de tokens cresce quadraticamente com a profundidade. Pior: quando uma ferramenta falha no meio do loop, o modelo tem que redirecionar todo o plano da observação de erro.

> ReAct's switching thinking-action-observation cycle is simple and flexible, but every tool调用都需要携带完整的前置上下文包括每一个思考.

ReWOO (Xu et al., arXiv:2305.18323, maio 2023) notou isso e fez uma aposta: planejar a coisa toda com antecedência, buscar evidências em paralelo, compor a resposta no final. Uma chamada de LLM para planejar, N ferramenta pede evidências (pode ser paralelo), uma chamada de LLM para resolver. O comércio é menos flexibilidade (o plano é estático) para uma melhor eficiência de token e modos de falha mais claros.

> - Não .**【类比】**ReWOO 像装修房子前先出施工图: designer一次性画完全部工序 (设计师一次性画完全部工序) 工人按图并行施工互不打扰 (工程器) 工人按图并行施工互不打扰 (工程器) 验收时把所有工序结果拼拼拼到一起结算 (求解器) ⋅ ReAct 则像边施工边设计,每个工人都可以翻阅前面所有工人的笔记动手,所以10 步后笔记就堆成山──

> ReWOO(Xu 等人,arXiv:2305.18323,2023 年 5 月) observou este ponto e propôs um esquema: primeiro planejar toda a tarefa,并行获证,最后组合答案――一次 LLM 调用规划、N 次工具调用获证 (可并行) 一次 LLM 调用求解――代价是灵活性降低 (计划是静态), mas em troca veio melhor token 效率和更清的失败模式――

## O conceito central.

### Os três papéis

```
Planner:  user_question -> [plan_dag]        # 规划器：将用户问题转为计划 DAG
Workers:  [plan_dag]     -> [evidence]        # 工作器：执行工具调用获取证据（可并行）
Solver:   user_question, plan_dag, evidence -> final_answer  # 求解器：组合证据生成最终答案
```

Planner produz um DAG. Cada nó nomeia uma ferramenta, seus argumentos e quais nós anteriores dependem (referências como `#E1`- Não .`#E2`Os trabalhadores executam os nós em ordem topológica.

> 规划器 generar um DAG. Cada ponto especifica um instrumento, seus parâmetros e dependentes de anterior ponto.`#E1`- Não.`#E2`É o que eu quero dizer.

### Por que 5x menos tokens

O ReAct aumenta a comprimento do prompt linearmente com a contagem de passos. No passo 10, o prompt contém pensamento 1 mais ação 1 mais observação 1 mais pensamento 2 mais ação 2 mais observação 2, e assim por diante. Cada passo intermediário também inclui redundantemente o prompt original.

> A duração do presente passo é de um número de passos que aumentam. Até o décimo passo, o presente passo inclui o pensamento 1 + ção 1 +  observo 1 + ção 2 + ção 2 + observo 2, segundo esse tipo de recomendação.

O ReWOO paga um plano de planejamento (grande), N pequenos trabalhadores (cada um apenas a chamada de ferramenta, sem cadeia), e um solver.

> ReWOO só precisa de uma única dica do planejador, cada uma contém apenas ferramentas de manipulação, sem cadeia de história, e uma única dica do resolvedor.

### Por que é mais robusto

Se o operador 3 falhar no ReAct, o loop tem que raciocinar a partir do erro no meio do fluxo. No ReWOO, o operador 3 retorna uma cadeia de erro; o resolvedor vê-a em contexto com o plano original e pode degradar graciosamente.

> Se o trabalho 3 falhar no ReAct, o ciclo deve ser ponderado em meio ao processo a partir do erro. Em ReWOO, o trabalho 3 retorna uma cadeia de erro; o solvente vê que o processo pode ser degradado de forma ótima no plano inicial.

### Destilação de planeador

O segundo resultado do artigo: porque o planejador não vê observações, você pode ajustar um modelo 7B em saídas do planejador de um professor 175B. O modelo pequeno lida com o planejamento; o modelo grande não é necessário na inferência.

> O segundo resultado do artigo: Como o planejador não vê resultados observados, você pode, no planejamento do modelo de professor 175B, emitir um pequeno planejamento de um modelo 7B.

> **【拓展：规划器蒸馏 → 成本优化】**Como o planejador não precisa de resultados observados, pode-se exportar o planejamento do modelo de professor 175B para o modelo 7B. Em 2026, o agente de produção usa universalmente a estrutura mista de "planagem de pequeno modelo + execução do grande modelo" para otimizar os custos.

### Planejamento e execução (LangChain, 2023)
### Planejamento e execução (2023)

O post de agosto de 2023 da equipe da LangChain generalizou ReWOO em um nome de padrão: Planejar e executar. O planejador de frente emite uma lista de passos, o executor executa cada passo, um replaneador opcional pode revisar após observar os resultados. Isso é mais próximo do ReAct do que ReWOO (o replaneador traz as observações de volta ao planejamento), mas preserva as poupanças de token.

> LangChain 团队 O artigo de agosto de 2023 irá reorganizar ReWOO 泛化为一个模式名称:Plan-and-Execute.

### Planos e Acto (Erdogan et al., arXiv:2503.09572, ICML 2025)

Plan-and-Act escala o padrão para agentes de web e móveis de longo horizonte. A contribuição chave são dados de planos sintéticos: um gerador de trajetória rotulado produz dados de treinamento onde o plano é explícito. Usado para ajustar os modelos de planejador que continuam trabalhando depois de 3050 passos em tarefas semelhantes à WebArena onde uma única trajetória ReAct perde coerência.

> O Plan-and-Act vai expandir esse modelo para longitudes de páginas web e agentes móveis. A contribuição chave é a de dados do plano sintético: o gerador de rotas de marcação produz dados de treinamento, dos quais o plano é evidente.

### Quando escolher qual

| Pattern | When | 适用场景 |
|---------|------|----------|
| ReAct | Short tasks, unknown environment, need reactive exception handling | 短任务、未知环境、需要响应式异常处理 |
| ReWOO | Structured tasks with known tools, token-sensitive, parallelizable evidence | 结构化任务、已知工具、Token 敏感、可并行 |
| Plan-and-Execute | Like ReWOO but with replanning after partial execution | 类似 ReWOO 但支持执行后重新规划 |
| Plan-and-Act | Long-horizon (>30 steps), web/mobile/computer-use | 长程任务(>30步)、网页/移动端/计算机使用 |
| Tree of Thoughts | Search is worth paying for (Lesson 04) | 值得付出搜索成本的场景 |

A diretriz de Anthropic de dezembro de 2024: comece com o mais simples. Se a tarefa é uma chamada de ferramenta mais um resumo, não construa ReWOO. Se a tarefa é uma tarefa de pesquisa de 40 passos, não faça ReAct sozinho.

> 🤔 **【困惑】**P: 既然 ReWOO 省5倍代币还准确,为什么不全部使用 ReWOO? A: 因为 ReWOO 的计划是"静态"的一旦发发发就不再根据观察调整.

> Antropic 2024  12 月 ガイド: From the simplest of beginnings──If a missão é um instrumento, não construam ReWOO──If a missão é uma missão de pesquisa de 40 passos, não usem apenas ReAct──

## Construí-lo e realizei-o.

> ️ **【易错点】**实现 ReWOO 时新手最常踩的坑: esquece de planejar DAG fazer um ciclo de teste.`#E1`Depende .`#E2`E o que é?`#E2`Depende também.`#E1`, , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , ,**后果**O executor está a ser executado.**一行修复**: To sequência posterior chequeada se o número de pontos de sequência é igual ao número total de pontos, não é igual em relação à poluição`CycleDetectedError`- Não.
```figure
rewoo-plan
```

## Construí-lo

`code/main.py`Implementa um brinquedo ReWOO:

> `code/main.py`实现一个玩具 ReWOO:

- `Planner` uma política escrita que emite um plano DAG a partir de um aviso.
  Tradução:`Planner` From Tip Generating Plan DAG's脚本策略──
- `Worker` Envia a chamada de ferramenta de cada nó através do registo.
  Tradução:`Worker` através do registro de distribuição de cada ponto de ferramenta调用──
- `Solver` composição escrita que lê evidências e produz uma resposta final.
  Tradução:`Solver`读取证据并生成最终答案的脚本组合器──
- Resolução de dependência  referências como `#E1`são substituídos por resultados de trabalhadores anteriores.
  Tradução do português: depender de resolver`#E1`O seu uso foi substituído por um outro.

A demonstração responde "Qual é a população da capital da França, redondeada em milhões?" usando um plano de duas etapas: (1) procurar a capital, (2) procurar a população, e depois resolver.

> 演示回答"Qual é a população da capital francesa, quatro舍五入到百万?"

- É o que é ?

> 运行:

```
python3 code/main.py
```

O rastro mostra o plano completo primeiro, depois os resultados do trabalhador, depois a composição do solver. Compare a contagem de tokens (imprimiremos uma contagem de caracteres aproximada) com uma corrida interleaved de estilo ReAct  ReWOO ganha neste tipo de tarefa estruturada.

> 轨迹 primeiro mostra o plano completo, depois é o resultado do trabalho, finalmente é o conjunto de ferramentas.

## Use-o com o framework implementado.

O LangGraph envia o Plan-and-Execute como receita (`create_react_agent`Para ReAct, gráficos personalizados para executar planos). Os fluxos da CrewAI codificam o padrão diretamente: você define tarefas de antemão e o Flow DAG as executa.

> LangGraph vai planejar e executar como equipamento`create_react_agent`Usado para ReAct, auto-definido para planejar-execução)  Fluxos de tripulação  diretamente codificados para este modelo: você previamente define tarefas, Flow DAG  execução delas.

## Envia-o . Produto .

`outputs/skill-rewoo-planner.md`gera um plano DAG do ReWOO a partir de uma solicitação do usuário, dado um catálogo de ferramentas. Valida o plano (acíclico, todas as referências resolvidas, todas as ferramentas existem) antes de entregar a um executor.

> `outputs/skill-rewoo-planner.md`根据用户请求和工具目录生成 ReWOO 计划 DAG──它在移交给执行器之前验证计划(无环、每个引用已解析、每个工具存在)──

## Exercícios.

1. Paralelamente execução de trabalhadores para nós de plano independente. O que é que você compra em um DAG de 6 nós com 2 grupos paralelos?
   Chinese Translation:将独立计划节点的工作器并行化.
2. Adicione um nó de replanagem que dispara se um trabalhador retornar um erro. Qual é a menor mudança para ReWOO que faz com que seja Plane-and-Execute?
   Chinese Translation: Add a one in the work machine return error when触发的重新规划节点──ReWOO 变成计划执行的最小改动是什么?
3. Substitui`Planner`com um modelo pequeno (classe 7B) e manter `Solver`Comparar qualidade de ponta a ponta  onde falha a divisão?
   O que é que se passa com o modelo de desenvolvimento?
4. Leia a secção 4 do artigo da ReWOO sobre destilação de planeadores.
   中文翻译:阅读 ReWOO论文第 4 节关于规划器蒸的内容──概念上重现 175B→7B 结果:需要什么训练数据?如何评估计划质量?
5. Portar o brinquedo para a forma de trajetória do Plano e Ação: plano é uma sequência, não um DAG. Que compensações mudam?
   O sistema de jogos será transferido para o plano e o ato de forma de trajeto: plano é sequência e não DAG.

## Termos-chave .

| Term | What people say | What it actually means |
|------|-----------------|-----------------------|
| 术语 | 通俗说法 | 实际含义 |
| ReWOO | "Reasoning without observations" / "无观察推理" | Plan, then fetch evidence in parallel, then solve — no observations in the planning prompt / 先规划，再并行获取证据，最后求解——规划提示中不包含观察 |
| Plan-and-Execute | "LangChain's plan-execute pattern" / "LangChain 的计划-执行模式" | ReWOO with an optional replanner node after execution / 带可选重新规划节点的 ReWOO |
| Plan-and-Act | "Scaled plan-execute" / "扩展版计划-执行" | Explicit planner/executor split with synthetic plan training data for long-horizon tasks / 使用合成计划训练数据的长程任务显式规划器/执行器分离 |
| Evidence reference | "#E1, #E2, ..." / "证据引用" | Plan-node placeholder substituted with prior worker output at dispatch time / 计划节点占位符，在分派时替换为工作器输出 |
| Planner distillation | "Small planner, big executor" / "小规划器，大执行器" | Fine-tune a small model on planner traces from a large teacher / 用大模型的规划轨迹微调小模型 |
| Token efficiency | "Fewer round trips" / "更少往返" | 5x fewer tokens on HotpotQA vs ReAct in the paper / 论文中 HotpotQA 上比 ReAct 减少 5 倍 token |
| DAG executor | "Topological dispatcher" / "拓扑分派器" | Runs plan nodes in dependency order; parallel at each level / 按依赖顺序运行计划节点；每层可并行 |

## Mais leitura 延伸阅读

- [Xu et al., ReWOO: Decoupling Reasoning from Observations (arXiv:2305.18323)](https://arxiv.org/abs/2305.18323) o papel canônico
  ReWOO 经典论文将推理与观察解──
- [Erdogan et al., Plan-and-Act (arXiv:2503.09572)](https://arxiv.org/abs/2503.09572) Planeador-executor em escala com planos sintéticos
  Plano-e-Act utilizando sintetplano de ampliação edição
- [LangGraph Plan-and-Execute tutorial](https://docs.langchain.com/oss/python/langgraph/overview) a receita-quadro
  Tradução do idioma:LangGraph Plane-and-Execute 教程框架配方──
- [Anthropic, Building Effective Agents](https://www.anthropic.com/research/building-effective-agents) escolher o padrão mais simples que funciona
  Tradução do inglês para "Antropic"  About building effective Agent  choose the simplest of available modes―
