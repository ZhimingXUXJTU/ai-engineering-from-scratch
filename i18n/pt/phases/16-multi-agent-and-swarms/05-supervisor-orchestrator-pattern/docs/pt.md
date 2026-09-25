# Supervisor / Orquestra-Trabalhador Padrão .

> Um agente principal planeja e delega; trabalhadores especializados executam em contextos paralelos e relatam. Este é o padrão por trás do sistema de pesquisa da Anthropic (Claude Opus 4 como chumbo, Sonnet 4 como subagentes), medido em +90,2% sobre o Opus 4 de um único agente em avaliações internas de pesquisa. O post de engenharia da Anthropic relata que 80% da variância no BrowseComp é explicada pelo uso de tokens sozinho  multi-agente ganha em grande parte porque cada subagente recebe uma janela de contexto fresca. Esta lição constrói o padrão de supervisor a partir dos primitivos e abrange as lições de engenharia de 2026 das implantações de produção.

> **【中文解读】**Um agente responsável  planejar e comandar tarefas; especialização em trabalho                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                              

> **【拓展：Supervisor 模式 → Claude DevFleet】**Claude Code multi-agent  editora de ferramentas Claude DevFleet é o supervisor                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           

**Type:** Learn + Build | **类型:** 学习 + 构建
**Languages:** Python (stdlib, `threading`) | **语言:** Python (标准库, `threading`)
**Prerequisites:** Phase 16 · 04 (Primitive Model) | **前置知识:** Phase 16 · 04 (原语模型)
**Time:** ~75 minutes | **时间:** ~75 分钟

> - Não .**【前置】**學本節前 請先掌握:Fase 16·04(4 个原语) 、Fase 14·01(Agente 循环) ‧Supervisor 模式 = 多 Agente ‧中最常用的一种一个主管 + 多个工作器──
> - Não .**【类比】**Supervisor 模式 = "projeto gerente + 工程师团队"──主管(Opus)分解任务+审查,工作器(Sonnet) 各干一摊──Antropic 数据:BrowseComp 80% 方差由代币 使用解释多 代理 赢是因为每个子 代理有独立上下文窗口(fresh context),不是协调本身魔法──

## Problema Introdução

A pesquisa é a tarefa prototípica que os sistemas de agente único falham. Você pergunta "o que mudou nos sistemas de agentes múltiplos entre 2023 e 2026?" Um agente único lê cinco artigos sequencialmente, preenche metade do seu contexto com seu texto, e depois tem que raciocinar sobre todos eles juntos. Esquece o primeiro artigo quando chega ao quinto. Não pode paralelalizar.

> A investigação é uma tarefa típica do fracasso de um único agente. Você pergunta: "Que mudanças ocorreram no sistema de vários agentes entre 2023 e 2026?" Um único agente leu cinco artigos em ordem, preenchendo metade do texto sobre os artigos, e então deve ponderá-los juntos.

A falha de um único agente é estrutural, não pode ser corrigida com melhores instruções. Não importa o quão bom seja o instrução do sistema, a janela de contexto se enche. As informações necessárias para a síntese (conclusões-chave de todos os cinco trabalhos) fisicamente não se encaixam ao lado do texto bruto dos trabalhos.

> 单代理 失败是结构性的,无法用更好的提示修复──不管系统提示多好,上下文窗口都会填满──综合需要信息(所有五篇论文的关键发现) Físico não pode ser comparado com o artigo.

O padrão de supervisor corrige isso: um agente principal planeja a pesquisa, delega cada sub-question para um trabalhador e sintetizou. Cada trabalhador recebe sua própria janela de 200k-token para uma pergunta estreita. O líder nunca vê os trabalhos brutos  apenas os resumos dos trabalhadores.

> O supervisor model corrigido este problema: um agente dominante planeja a busca, envia cada um dos problemas para uma máquina de trabalho, então integra.

O fluxo de informações é o design: os dados brutos permanecem em contextos de trabalhadores; apenas as descobertas comprimidas chegam ao lead. O contexto do lead é dedicado à síntese, não ao carregamento de dados.

> 信息流是设计: data original permanece no trabalho; apenas o comprimento do descoberto chega ao director.

O sistema de pesquisa de produção da Anthropic relata +90,2% sobre avaliações internas de pesquisa versus um único Opus 4.

> O relatório de pesquisa de produção de Anthropic em avaliação interna de pesquisas em relação a um único Opus 4 aumentou +90.2%。 o mesmo artigo aponta que 80% da diferença de browseComp é apenas por causa da *token utilization*                                                                                                                                                                                                                                  

O número de 80% é a descoberta principal: a escolha de modelo, a engenharia de prompt e a ferramenta juntos explicam apenas 20% da variância. Se você quer um melhor desempenho de agente de pesquisa, gaste mais tokens (mais sub-gentes, contextos maiores) antes de ajustar as instruções.

> 80% Este número é um tópico descoberto: modelo seleção, sugerência engenharia e ferramenta adicionada apenas explica 20% da diferença.

## Conceptos básicos

### O padrão

```
                 ┌──────────────┐
                 │   Lead       │  plans, decomposes,
                 │  (Opus 4)    │  synthesizes
                 └──┬────┬───┬──┘
                    │    │   │
            ┌───────┘    │   └───────┐
            ▼            ▼           ▼
      ┌─────────┐  ┌─────────┐  ┌─────────┐
      │ Worker1 │  │ Worker2 │  │ Worker3 │
      │(Sonnet) │  │(Sonnet) │  │(Sonnet) │
      └─────────┘  └─────────┘  └─────────┘
         fresh       fresh        fresh
         context     context      context
```

O chumbo nunca lê as matérias-primas, os trabalhadores nunca veem o trabalho uns dos outros até que o chumbo se sintetize, cada flecha é uma entrega com um artefato estreito.

> O director nunca lê o material original. O trabalho do director nunca se vê antes do complexo. Cada arco é um conjunto de elementos estreitos.

Este isolamento de informações é a escolha principal de design. A janela de contexto do lead permanece focada no planejamento e síntese  nunca poluída por 200 mil tokens de resultados de pesquisa crus.

> Este tipo de isolamento de informações é o design central da seleção.

### Por que ganha

Três mecanismos:

> Três mecanismos:

1. **Fresh context per subagent.**Um trabalhador que explora "herança da FIPA-ACL" não carrega os 40 mil tokens que o líder gastou no planejamento.
   Tradução:**每个子 Agent 的清新上下文。**探索"FIPA-ACL 遗产"的工作器不携带主导人用于规划的40k token──它获得一个用于一个问题的200k 窗口──
2. **Specialization via prompt.**A ordem do líder é "decompor e sintetizar", não "investigar". A ordem de cada trabalhador é estreita: "encontrar o que mudou em X". As instruções focalizadas produzem resultados focados.
   Tradução:**通过提示专业化。**A dica do principal orientador é "descomposição e integração", em vez de "investigação"― a dica de cada máquina de trabalho é estreita:" descobrir o que X mudou―" a dica do foco para produzir o foco de saída―".
3. **Parallelism.**Os trabalhadores correm simultaneamente.`max(worker_times) + plan + synthesis`Não , não .`sum(worker_times)`- Não .
   Tradução:**并行性。**工作器并发运行──挂钟时间大约是 `max(worker_times) + plan + synthesis`- Não .`sum(worker_times)`- Não.

### Lições de engenharia (Antropic 2025)

O post Anthropic lista várias lições de produção que ainda são relevantes para 2026:

> Anthropic's artigo lista algumas regras ainda aplicáveis à experiência de produção de 2026:

- **Scale effort to query complexity.**Queries simples: um agente, 3-10 chamadas de ferramentas. Queries complexas: 10+ agentes. O líder deve estimar isso, não o chamador.
  Tradução:**按查询复杂度缩放工作量。**简单查询: One Agent,3-10次工具调用──复杂查询:10+ 个 个 个 个 个 个 个 个 个 个 个 个 个 个 个 个 个 个 个 个 个 个 个 个 个 个 个 个 个 个 个 个 个 个 个 个 个 个 个 个 个 个 个 个 个 个 个 个 个 个 个 个 个 个 个 个 个 个 个 个 个 个 个 个 个 个 个 个 个 个 个 个 个 个 个 个 个 个 个 个 个 个 个 个 个 个 个 个 个 个 个 个 个 个 个 个 个 个 个 个 个 个 个 个 个 个 个 个 个 个 个 个 个 个 个 个 个 个 个 个 个 个 个 个 个 个 个 个 个 个 个 个 个 个 个 个 个 个 个 个 个 个 个 个 个 个 个 个 个 个 个 个 个 个 个 个 个 个 个 个 个 个 个 个 个 个 个 个 个 个 个 个 个 个 个 个 个 个 个 个 个 个 个 个 个 个 个 个 个 个 个 个 个 个 个 个 个 个 个 个 个 个 个 个 个 个 个 个 个 个 个 个 个 个 个 个 个 个 个 个 个 个 个 个 个 个 个 个 个 个 个 个 个 个 个 个 个 个 个 个 个 个 个 个 
- **Broad then narrow.**Decompor em sub-perguntas amplas primeiro, e depois gerar mais trabalhadores por sub-perguntas se a resposta justificar profundidade.
  Tradução:**先宽后窄。**Antes de se descomplicar em problemas de sub-processo amplo, se a resposta precisar de profundidade, então para cada problema de sub-projeto gerar mais máquinas de trabalho.
- **Rainbow deployments.**Os agentes são de longa duração e estado. O azul-verde tradicional não funciona.
  Tradução:**彩虹部署。**Agente é um agente de longa duração em funcionamento e com estado.
- **Token usage dominates.**Multi-agente é ~ 15x os tokens de um único agente. só executá-lo quando o valor da tarefa justifica o custo.
  Tradução:**Token 使用量占主导。**Do agente é cerca de 15 vezes mais do que um agente único.

### A curva gráfica-nativa

A LangGraph originalmente enviou um `langgraph-supervisor`Biblioteca com um nível elevado `create_supervisor`Em 2025, a LangChain mudou a recomendação para a implementação do padrão de supervisor através de chamadas de ferramentas diretamente, porque as chamadas de ferramentas dão mais controle sobre o que o supervisor vê* (engenharia de contexto).

> O LangGraph publicou um primeiro com um alto nível .`create_supervisor`助手 `langgraph-supervisor`库──2025年 LangChain vai sugerir mudar para ferramentas para implementar diretamente o modelo de supervisor, pois ferramentas para implementar o sistema de supervisor ver o que (→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→

A mudança reflete uma visão de 2025-2026: a engenharia de contexto importa mais do que a engenharia de orquestração. O que o supervisor vê determina o que ele pode planejar. Passar o contexto de trabalhador bruto mata a capacidade de planejamento do líder; passando resumos estreitos preserva-o.

> Esta transformação reflete a visão de 2025-2026, que o engenharia superior ao que o engenharia de montagem é mais importante. O supervisor vê o que decide o que pode planejar.

### Os modos de falha

- **Lead hallucinates the plan.**Se o lead gera subquestions que não descompõem a verdadeira pergunta, os trabalhadores fazem pesquisas precisas sobre o alvo errado.
  Tradução:**主导者幻觉计划。**Se o problema gerado pelo gerador não resolver o problema real, a máquina de trabalho fará uma pesquisa precisa no objetivo errado.
- **Workers over-explore.**Sem limites explícitos de âmbito, os trabalhadores desviam para além da subquestionaria atribuída e poluem a fase de síntese.
  Tradução:**工作器过度探索。** sem limites de alcance definidos, o trabalho irá se deslocar para além do seu subproblemas distribuídos e contaminar os passos abrangentes
- **Synthesis conflicts.**Dois trabalhadores retornam fatos contraditórios. O líder deve perguntar novamente (agrega uma rodada) ou notar explicitamente o desacordo.
  Tradução:**综合冲突。**两个工作器回复矛盾的事实──主导者必须重新询问(增加一轮) 或明确记录分歧──静默选择一方是最糟糕的失败:用户永远不知道发生分歧──

### Quando o supervisor está errado

- **Sequential tasks.**Se o passo 2 precisa literalmente da saída do passo 1, o paralelismo não compra nada. Use um pipeline (CrewAI Sequential, LangGraph linear graph).
  Tradução:**顺序任务。**Se o passo 2 realmente precisa de saída do passo 1, não há ajuda.
- **Simple queries.**O agente único trata-os mais rápido e mais barato.
  Tradução:**简单查询。**单代理 更快更便宜地处理它们―― antes de gerar a máquina de gerar, utilizar o cheque de "conclusão de trabalho" do orientador―
- **Strict determinism.**O supervisor usa delegação selecionada pelo LLM. Os gráficos estáticos são melhores quando a auditoria/replay é mais importante do que a adaptabilidade.
  Tradução:**严格确定性。**监督者使用 LLM 选择的委派──当审计/回放比适应性更重要时,静态图更好──

## Construí-lo e realizei-o.
```figure
supervisor-hierarchy
```

## Construí-lo

`code/main.py`Implementa um supervisor de três trabalhadores paralelos utilizando `threading`O lead decompõe uma consulta em subquestions, os trabalhadores executam simultaneamente em cada subquestion e o lead sintetizes.

> `code/main.py`Utilização `threading` Realizar um supervisor de três trabalhos em conjunto.  O supervisor irá dividir as perguntas em questões, o trabalho em cada problema em conjunto.  Não há um verdadeiro LLM  O trabalho foi escrito para obter e resumir.

Estrutura chave:

> 关键结构:

- `Lead.plan(query)`Divide uma consulta em 3 subperguntas.
  Tradução:`Lead.plan(query)`A consulta será dividida em três questões.
- `Worker.run(sub_q)`Retorna um resumo falso (poderá ser qualquer agente que utilize ferramentas na produção).
  Tradução:`Worker.run(sub_q)`返回一个假摘要 ()                                                                                                                                                                                                                                                          
- `Lead.run(query)`Desliga os trabalhadores em fios, juntas e sintetizas.
  Tradução:`Lead.run(query)`Em linha, inicia a máquina, espera, então completa-se.

- Correr .

```
python3 code/main.py
```

A saída mostra o plano, os trabalhadores paralelos rastream com timestamps de início/final e a síntese final.

> 输出显示计划、带有开始/结束时间的并行工作器跟踪和最终综合―― você pode ver o tempo de execução de três 0.3 segundos

## Use-o com o framework implementado.

`outputs/skill-supervisor-designer.md`O sistema de supervisão é um sistema de supervisão que permite a criação de um modelo de supervisão.

> `outputs/skill-supervisor-designer.md`接收用户查询并生成监督者模式设计:主导系统提示、工作器角色、子问题分解规则和综合模板──在构建新研究风格 系统之前使用──

## Envia-o . Produto .

Lista de verificação antes de implantar um padrão de supervisão:

> 部署监督者模式之前的检查清单:

- **Model pairing.**O plomo em um modelo de raciocínio (classe Opus, `o3`Os trabalhadores de um modelo mais rápido e mais barato (Sonnet, `o4-mini`)).
  Tradução:**模型配对。**主导者使用推理级模型(Opus 类、`o3`类) ・工作器使用更快、更便宜的模型(Sonnet、`o4-mini`)。
- **Worker timeout.**Qualquer trabalhador que exceda 2x o tempo médio de execução é morto; o líder re-aparece com um escopo mais estreito ou prossegue sem ele.
  Tradução:**工作器超时。** qualquer máquina de trabalho de mais de 2 vezes o tempo de funcionamento é encerrada; o director deve reproduzir-se em um âmbito mais restrito ou não continuar a usá-la.
- **Token cap per worker.**O limite duro (por exemplo, 10 vezes a entrada esperada da síntese) impede que um trabalhador fugitivo explode o orçamento.
  Tradução:**每个工作器的 Token 上限。**硬限制 (por exemplo, 10 vezes do que o previsto) impedir que o trabalho perdido seja consumido pelo orçamento.
- **Observability.**Rastrear o plano do líder, as chamadas de ferramentas de cada trabalhador e a síntese.
  Tradução:**可观测性。**O plano do instrutor, a manipulação e a integração das ferramentas de cada máquina, é a base de qualquer manipulação posterior.
- **Rainbow rollout.**Os agentes de longa data do Estado precisam de transição gradual, não de troca de troca.
  Tradução:**彩虹推出。**Há um agente de transição de versão progressiva, não de troca de calor.

## Exercícios.

1. Corra .`code/main.py`Em que número de trabalhadores a despesa de criação excede as economias paralelas nesta demonstração?
   Tradução: 运行`code/main.py`, então modifique o director para gerar 5 em vez de 3 máquinas. Observe o efeito do tempo de pendura.
2. Implementar um tempo de trabalho para os trabalhadores: matar qualquer trabalhador que corre mais de 0,5 segundos e ter o lead sintetizar os resultados restantes. Que observabilidade você precisa para saber que um trabalhador foi cortado?
   Tradução do inglês para tradução do inglês: implementar um trabalho ultra-tempo: terminar qualquer operação de mais de 0,5 segundos em um trabalho, fazer com que o director compreenda os resultados restantes.
3. Adicione um passo de detecção de conflitos à síntese do líder: se dois trabalhadores retornam respostas contraditórias, o líder nota a discórdia em vez de escolher uma.
   Tradução do inglês: In Master's Complex Add conflict check steps: Se dois trabalhos retornarem à resposta de contradição, o autor registra diferenças em vez de escolher uma delas.
4. Leia o artigo de engenharia de sistemas de pesquisa da Anthropic.
   Chinese: 阅读 Antropic 的研究系统工程文章.
5. Comparar com o de LangGraph `create_supervisor`O que lhe dá um melhor controle sobre o que o supervisor vê? Por que a Anthropic só passa explícitamente sub-respostas e não conteúdo de trabalhador bruto para a síntese?
   Tradução do idioma:`create_supervisor`(Via edição) Com novas ferramentas de admissão. O que faz você melhor controlar o supervisor ver o quê?

## Termos-chave .

| Term | What people say | What it actually means |
|------|----------------|------------------------|
| Supervisor / 监督者 | "Lead agent" / "主导 Agent" | An orchestrator agent that plans, delegates, and synthesizes. Does not do the work itself. / 规划、委派和综合的编排 Agent。不做实际工作。 |
| Worker / 工作器 | "Subagent" / "子 Agent" | A focused agent invoked by the supervisor with narrow scope and its own context window. / 由监督者调用的聚焦 Agent，具有狭窄范围和自己的上下文窗口。 |
| Orchestrator-worker / 编排器-工作器 | "Supervisor pattern" / "监督者模式" | Same thing, different name. The 2026 literature uses both. / 同一事物，不同名称。2026 年文献两者都用。 |
| Fresh context / 清新上下文 | "Clean window" / "干净窗口" | A worker's context starts from its system prompt and assigned question, not the lead's history. / 工作器的上下文从其系统提示和分配的问题开始，而不是主导者的历史。 |
| Rainbow deployment / 彩虹部署 | "Gradual rollout" / "渐进推出" | Long-running stateful agents need versioned drain-and-replace, not blue-green. / 长时间运行的有状态 Agent 需要版本化的排空和替换，而不是蓝绿部署。 |
| Token dominance / Token 主导 | "Context is the variable" / "上下文是变量" | 80% of research-eval variance comes from total tokens used, not model choice, per Anthropic. / 80% 的研究评估方差来自使用的总 token，而不是模型选择，据 Anthropic。 |
| Scale effort / 缩放工作量 | "Match agent count to complexity" / "按复杂度匹配 Agent 数量" | Lead estimates query difficulty, spawns 1 vs 10+ workers accordingly. / 主导者估计查询难度，相应地生成 1 个或 10+ 个工作器。 |
| Synthesis conflict / 综合冲突 | "Workers disagree" / "工作器不一致" | Two workers return contradictory facts; the lead must surface disagreement, not silently pick one. / 两个工作器返回矛盾的事实；主导者必须揭示分歧，而不是静默选择一方。 |

## Mais leitura 延伸阅读

- [Anthropic engineering — How we built our multi-agent research system](https://www.anthropic.com/engineering/multi-agent-research-system) a referência de produção para o modelo de supervisão
  Tradução do inglês para tradução do inglês: Antropic 工程  我们如何构建多 Agent 研究系统  监督者模式的生产参考
- [LangGraph workflows and agents](https://docs.langchain.com/oss/python/langgraph/workflows-agents) Supervisor de chamada de ferramentas é agora o formulário recomendado
  Tradução do inglês:LangGraph 工作流和 Agent  工具调用监督者现在是推的形式
- [LangGraph supervisor reference](https://reference.langchain.com/python/langgraph-supervisor) o auxiliar legado, ainda utilizado na produção de 2026
  中文翻译:LangGraph 监督者参考  旧版助手, ainda em uso 2026年生产
- [OpenAI cookbook — Orchestrating Agents: Routines and Handoffs](https://developers.openai.com/cookbook/examples/orchestrating_agents) Variante de supervisor baseada em transferência
  Tradução do inglês:OpenAI 手册  编排 Agente:例程和交接  基于交接的监督者变体
