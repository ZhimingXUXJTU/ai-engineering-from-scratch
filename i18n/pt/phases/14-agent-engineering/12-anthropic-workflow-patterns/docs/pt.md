# Padrões de fluxo de trabalho da Antropic: simples sobre complexo Antropic  工作流模式:简单优于复杂

> Schluntz e Zhang (Anthropic, Dec 2024) distinguem fluxos de trabalho (pistas predefinidas) de agentes (uso dinâmico de ferramentas). Cinco padrões de fluxo de trabalho cobrem a maioria dos casos. Comece com chamadas diretas de API. Adicione agentes apenas quando as etapas não podem ser previstas.

> **【中文解读】**Em um artigo publicado em 12 de dezembro de 2024, a Anthropic distinguia entre o fluxo de trabalho (pre-definido) e o uso de ferramentas de trabalho (Agent) e o uso de ferramentas de trabalho (Agent).

**Type:** Learn + Build | **类型:** 学习 + 构建
**Languages:** Python (stdlib) | **语言:** Python (标准库)
**Prerequisites:** Phase 14 · 01 (Agent Loop) | **前置知识:** Phase 14 · 01 (Agent 循环)
**Time:** ~60 minutes | **时间:** ~60 分钟

## Objetivos de aprendizagem

- Nomear os cinco padrões de fluxo de trabalho da Anthropic: cadeia de prompt, roteamento, paralelação, orquestor-trabalhadores, avaliador-optimizador.
  Chinese:                                                                                                                                                                                                                                                              
- Explique a distinção entre o fluxo de trabalho e o custo de engenharia de cada um.
  Tradução do inglês para tradução do inglês: Explanation of Agent and Workflow's differences and their respective project costs.
- Identificar quando escolher um fluxo de trabalho em vez de um agente (e vice-versa).
  O que é que é o trabalho?
- Implementar os cinco padrões em STDlib contra um Mestrado em Direito.
  Tradução do inglês para o inglês: using standard library aiming for script LLM 实现所有五种模式──

## O problema é o problema da introdução

As equipes buscam quadros multi-agente para problemas que querem uma única chamada de função. O custo é real: os quadros adicionam camadas que obscurecem pedidos, escondem o fluxo de controle e convidam complexidade prematura. O post de Schluntz e Zhang de dezembro de 2024 é o retorno mais citado da indústria: comece simples, adicione complexidade apenas quando ganha seu custo.

> 团队为只需要一次函数调用的问题选择多 机构框架――代价是真实的:框架添加模糊提示、隐藏控制流、引入过早复杂性的层――Schluntz 和 Zhang de 2024 12 月 文章是最被引用的行业反思:从简单开始,只有在复杂性值其成本时才添加――

> **【中文解读】**Antropic em 12 de dezembro de 2024 Publicado em Construção de Agentes Eficazes define quatro tipos de processos: 1) Cadeia Prometida; 2) Roteamento; 3) Paralelação; 4) Orquestra-Trabalhadores;

> **【拓展：Anthropic 的工作流模式分类已成为 Agent 工程的事实标准】**LangGraph utiliza o estado de imagem para implementar estes modelos, OpenAI Agents SDK utiliza as mãos para implementar a rotação e a organização, CrewAI usa as equipes para implementar a unificação.

> - Não .**【前置】**必須先通過Fase 14·01 (Agent Loop) 本節就是它的"模式提炼"──還需要看Fase 14·02 (ReWOO) ‧Fase 14·05 (Self-Refine) ‧Fase 14·10 (Skills) 五种工作流模式都对应前面学过的具体技术,没基础会感觉空洞──

## O conceito central.

### Fluxos de trabalho versus agentes

- **Workflow.**LLM e ferramentas orquestradas através de caminhos de código predefinidos.
  Tradução:**工作流。**通過预定义代码路径编排的 LLM 和工具──工程师拥有图──
- **Agent.**Os LLM dirigem dinâmicamente as suas próprias ferramentas e tomam os seus próprios passos.
  Tradução:**Agent。**LLM 动态 orienta seus próprios instrumentos e passos.

Os fluxos de trabalho são mais baratos, mais rápidos e mais fáceis de depurar. Agentes desbloqueam problemas sem fim, mas tornam os modos de falha mais difíceis de raciocinar.

> - Não .**【类比】**Fluxo de trabalho vs agente 像地铁 vs 自驾:地铁(fluxo de trabalho) Route fixed、便宜、可靠, but you can only go to station;自驾(agent)灵活、能去任何地方, but可能迷路、烧油、出车祸。日常通勤选地铁(workflow),探索未知地区选自驾(agent) ⋅ o erro mais comum dos novos é "todas as tarefas são autogestíveis" ⋅ na verdade 80% das tarefas de produção são realizadas pelo ferro.

>  ambos têm seu uso em campo de batalha                                                                                                                                                                                                                                                         

### O Mestrado em Direito e Direito

Fundamento para todos os cinco padrões: um LLM com três capacidades conectadas em busca (retorno), ferramentas (ações), memória (persistência).

> Todas as aplicações de um Mestrado em Ciências Humanas podem ser utilizadas em qualquer um dos seus programas.

### Os cinco padrões

1. **Prompt chaining.**A saída da chamada 1 é a entrada para a chamada 2. Utilize quando uma tarefa tem uma decomposição linear limpa. Portas programáticas opcionais entre etapas.
   Tradução:**提示链。**调用 1 的输出是调用 2 的输入. 调用 2 的输入. 调用 2 的输入. 调用 2 的输出是调用 2 的输入. 调用 2 的输出是调用 2 的输入. 调用 2 的输出是调用 2 的输入. 调用 2 的输入. 调用 2 的输入. 调用 2 的输入. 调用 2 的输入. 调用 2 的输入. 调用 2 的输入. 调用 2 的输入. 调用 2 的输入.
2. **Routing.**Um LLM classificador escolhe qual LLM ou ferramenta para invocar.
   Tradução:**路由。**选择调用哪个下游 LLM或工具── quando diferentes categorias de entrada necessitam de diferentes processos de utilização──
3. **Parallelization.**Execução de chamadas de N LLM simultâneas, resultados agregados. Duas formas: seccionamento (parcelações diferentes) e votação (o mesmo prompt, N runs, maioria/síntese).
   Tradução:**并行化。**Não é possível fazer o mesmo, mas é possível fazer o mesmo.
4. **Orchestrator-workers.**Um LLM orquestador decide dinâmicamente quais trabalhadores (também LLM) executar e sintetiza sua produção.
   Tradução:**编排器-工作者。**编排器 LLM 动态决定运行哪些工作者( também LLM)并综合其输出── similar to Agent 循环, mas 编排器 não será um ciclo ilimitado──
5. **Evaluator-optimizer.**Um LLM propõe uma resposta, outro LLM avalia. Iterar até que o avaliador passe. Isto é auto-refinado (Lessão 05) generalizado.
   Tradução:**评估器-优化器。**Um LLM  propõe resposta, outro LLM  avaliá-lo.

### Onde os fluxos de trabalho vencem os agentes

> 工作流优于 Agente's cenário:

- **Predictable tasks.**Se consegues enumerar os passos, devias.
  Tradução:**可预测任务。**Se consegues fazer um passo, devias fazer-o.
- **Cost-bound tasks.**Os fluxos de trabalho têm números de passos limitados; os agentes podem circular.
  Tradução:**成本受限任务。**工作流有有限步数;Agente pode estar fora de controle.
- **Compliance-bound tasks.**Os auditores querem ler o gráfico, não inferir-lo a partir de trajetórias.
  Tradução:**合规受限任务。**O auditor quer ler o quadro, e não o seu próprio caminho.

### Onde os agentes vencem os fluxos de trabalho

> Agente 优于工作流的场景:

- **Open-ended research.**Quando o próximo passo depende do que o último passo retorna.
  Tradução:**开放式研究。**Quando o próximo passo depende do que o passo anterior retorna.
- **Variable-length tasks.**Minutos a horas de trabalho em que não se sabe o número de etapas.
  Tradução:**可变长度任务。**De minutos a horas de trabalho, número de passos desconhecidos.
- **Novel domains.**Quando ainda não conheces o fluxo de trabalho certo, primeiro explora, codifica depois.
  Tradução:**新领域。**Quando ainda não sabes o que é o verdadeiro fluxo de trabalho, primeiro explora, depois escreve.

### O companheiro de engenharia de contexto

"Effective context engineering for AI agents" (Anthropic 2025) formaliza a disciplina adjacente: a janela 200k é um orçamento, não um recipiente. O que incluir, quando compactar, quando deixar o contexto crescer. Coberto em detalhe na lição Fase 14 sobre compressão de contexto.

> "AI Agent's有效上下文工程" (Antropic 2025) formalizou a sua área de estudo:

## Construí-lo.

> ️ **【易错点】**团队最常踩的坑: ver Antropic 五种模式就直接全部上 LangGraph/CrewAI 框架──**后果**O que é um "project" de Python?**先直接 API 调用，加复杂度只为换取能力**" Uma cadeia de prompt usando uma função Python comum está pronta, não precisa de qualquer quadro".""**一行修复**A avaliação de cada tarefa pode ser realizada com o seu objetivo, pode ser feita em outro quadro.
```figure
workflow-chain
```

## Construí-lo

`code/main.py`Implementa os cinco padrões de fluxo de trabalho contra um `ScriptedLLM`- Não .

> `code/main.py` para`ScriptedLLM`实现 todos os cinco modos de trabalho:

- `prompt_chain(input, steps)`- sequenciais.
- `route(input, classifier, handlers)` Classificação + expedição.
- `parallel_vote(prompt, n, aggregator)` N corridas, agregado.
- `orchestrator_workers(task, workers)`O orquestrador escolhe os trabalhadores.
- `evaluator_optimizer(task, proposer, evaluator, max_iter)` Loop até passar.

- É o que é ?

> 运行:

```
python3 code/main.py
```

Cada padrão imprime seu rastro. O total de linhas de código por padrão é de ~10-15; o custo de uma estrutura é medido em milhares.

> Cada modelo imprime seu trajeto. Cada modelo tem um número de linhas de código de cerca de 10 a 15 linhas.

> 🤔 **【困惑】**P: 既然 o "fluxo de trabalho  prioritário" é tão claro, por que LangGraph、CrewAI esses frameworks são tão quentes?**持久化、可观测性、人在回路、监控**Estes "运维级" funções. Você usa 30 行 stdlib 写的提示链 运挂了, você conseguiu se pensar como recuperar do 17 步步; usando LangGraph 写的,框架免费给你检查点.

## Use-o com o framework implementado.

- A API direta requer a maioria das tarefas.
  中文翻译: maioria das tarefas usa diretamente API 调用。
- Framework apenas quando o padrão realmente precisa de estado durável (LangGraph), concurência entre modelo de ator (AutoGen v0.4), ou modelo de papel (CrewAI).
  Tradução do inglês para tradução do inglês: Only in mode really needs to last a long time (Langgraph)
- Procure o SDK do Agente Claude quando quiser a forma do arsenal do código Claude sem reconstruí-lo.
  Quando você quer Claude Code 框架形态而不重建时选择Claude Agent SDK──

## Envia-o . Produto .

`outputs/skill-workflow-picker.md`seleciona o padrão adequado para uma determinada descrição de tarefa, incluindo a lógica da decisão e o caminho de refactor para um agente caso os fluxos de trabalho não sejam suficientes.

> `outputs/skill-workflow-picker.md`Para determinar a tarefa, descrever a escolha do modelo correto, incluindo os motivos de decisão e a forma como o agente é reestruturado quando o fluxo de trabalho é insuficiente.

## Exercícios.

1. Implementar roteamento com um limiar de confiança. Abaixo do limiar -> escala para humanos. Onde o limiar de aterrissagem para um caso de uso de suporte de nível 1?
   Tradução do inglês para tradução do inglês: 值的路由──低于值 -> 升级给人类──一级支持用例的值在哪里?
2. Adicionar um timeout para `parallel_vote`O que acontece quando uma chamada é pendurada?
   Tradução:`parallel_vote`Como é que se faz quando um turno de votação está em aberto?
3. Vire .`evaluator_optimizer`para um bandido: manter as saídas dos dois primeiros em iterações para que um bom resultado tardío não seja sobreescrevido por um mau tardío.
   Tradução:将`evaluator_optimizer`变成 bandit:跨代保留 top-2 输出, evitar后期好结果被后期坏结果覆盖──
4. Combine a cadeia de prompt com roteamento: um roteador escolhe uma das três cadeias.
   O que é um símbolo de um grande ponto de troca?
5. Escolha uma das suas características de produção, desenhe o gráfico do fluxo de trabalho, conte os passos.
   Chinese Translation: escolher uma função de produção, desenhar um plano de trabalho, fazer um cálculo, fazer um trabalho, fazer um trabalho, fazer um trabalho, fazer um trabalho, fazer um trabalho, fazer um trabalho, fazer um trabalho, fazer um trabalho, fazer um trabalho, fazer um trabalho, fazer um trabalho, fazer um trabalho, fazer um trabalho, fazer um trabalho, fazer um trabalho, fazer um trabalho, fazer um trabalho, fazer um trabalho, fazer um trabalho, fazer um trabalho, fazer um trabalho, fazer um trabalho, fazer um trabalho, fazer um trabalho, fazer um trabalho, fazer um trabalho, fazer um trabalho, fazer um trabalho, fazer um trabalho, fazer um trabalho, fazer um trabalho, fazer um trabalho, fazer um trabalho, fazer um trabalho, fazer um trabalho, fazer um trabalho, fazer um trabalho, fazer um trabalho, fazer um trabalho, fazer um trabalho, fazer um trabalho, fazer um trabalho, fazer um trabalho, fazer um trabalho, fazer um trabalho, fazer um trabalho, fazer um trabalho, fazer um trabalho, fazer um trabalho, fazer um trabalho, fazer um trabalho, fazer um trabalho, fazer um trabalho, fazer algo, fazer algo ou fazer algo, fazer algo, fazer algo, fazer algo, ou fazer algo, ou fazer algo, ou fazer algo, ou fazer algo, ou fazer?

## Termos-chave .

| Term | What people say | What it actually means |
|------|-----------------|-----------------------|
| 术语 | 通俗说法 | 实际含义 |
| Workflow | "Predefined flow" / "预定义流程" | Engineer-owned graph of LLM and tool calls / 工程师拥有的 LLM 和工具调用图 |
| Agent | "Autonomous AI" / "自主 AI" | Model-owned graph; dynamic tool direction / 模型拥有的图；动态工具指导 |
| Augmented LLM | "LLM with tools" / "带工具的 LLM" | LLM + search + tools + memory; the atomic unit / LLM + 搜索 + 工具 + 记忆；原子单元 |
| Prompt chaining | "Sequential calls" / "串行调用" | Output of call N is input to call N+1 / 调用 N 的输出是调用 N+1 的输入 |
| Routing | "Classifier dispatch" / "分类分派" | Pick which chain/model handles the input / 选择哪个链/模型处理输入 |
| Parallelization | "Fan out" / "扇出" | N concurrent calls; aggregate by sectioning or voting / N 个并发调用；按分段或投票聚合 |
| Orchestrator-workers | "Dispatcher agent" / "分派 Agent" | Orchestrator LLM picks specialist LLMs dynamically / 编排器 LLM 动态选择专家 LLM |
| Evaluator-optimizer | "Proposer + judge" / "提议者 + 评判者" | Iterate until evaluator passes; Self-Refine generalized / 迭代直到评估器通过；Self-Refine 的泛化 |

## Mais leitura 延伸阅读

- [Anthropic, Building Effective Agents (Dec 2024)](https://www.anthropic.com/research/building-effective-agents) os cinco padrões de fluxo de trabalho
  Chinese: 关于构建有效代理 的文章五种工作流模式──
- [Anthropic, Effective context engineering for AI agents](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents) a disciplina do companheiro
  Chinese:Anthropic 关于 AI Agent 有效上下文工程的文章伴随学科──
- [LangGraph overview](https://docs.langchain.com/oss/python/langgraph/overview) quando os gráficos estatais ganham o seu custo
  O longgraph 概览有状态图何时值得其成本──
- [OpenAI Agents SDK](https://openai.github.io/openai-agents-python/)O modelo de orquestração-trabalhador, produzido
  Tradução do inglês para "OpenAI Agents"
