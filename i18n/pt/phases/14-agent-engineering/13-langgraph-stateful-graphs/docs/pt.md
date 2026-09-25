# LangGraph: Graficos de estado e execução duradoura
# Orquestração de gráficos estatais  Execução duradoura e pontos de controlo

> O agente é uma máquina de estado; nós são funções; bordas são transições; estado é posto em ponto de checagem após cada nó. Resume de qualquer falha no último ponto de checagem bem sucedido. LangGraph é a referência de 2026 para este modelo de orquestração estadual de baixo nível.

> **【中文解读】**LangGraph é uma referência para a realização de uma organização de estado de 2026 em nível inferior.

**Type:** Learn + Build | **类型:** 学习 + 构建
**Languages:** Python (stdlib) | **语言:** Python (标准库)
**Prerequisites:** Phase 14 · 01 (Agent Loop), Phase 14 · 12 (Workflow Patterns) | **前置知识:** Phase 14 · 01 (Agent 循环), Phase 14 · 12 (工作流模式)
**Time:** ~75 minutes | **时间:** ~75 分钟

## Objetivos de aprendizagem

- Descreva o modelo central do LangGraph: máquina de estado com estado imutável, nós de função, bordas condicionais e pontos de controle pós-passo.
  Tradução do inglês para tradução do inglês: description of LangGraph's core model:带不可变状态、函数节点、条件边和步后检查点的状态机――
- Descreva o modelo central do LangGraph: máquina de estado com estado tipado, nós de função, bordas condicionais e pontos de verificação pós-nodo.
- Nomear as quatro capacidades que os documentos destacam: execução duradoura, streaming, humano-no-loop, memória abrangente.
  O texto também é traduzido em português por "Pessoas em movimento" (em português: "personas em movimento").
- Explique as três topologias de orquestração que LangGraph suporta: supervisor, peer-to-peer (swarm), hierárquica (subgrafos aninhados).
  Tradução do inglês para tradução livre: tradução livre: tradução livre: tradução livre: tradução livre: tradução livre: tradução livre: tradução livre: tradução livre: tradução livre: tradução livre: tradução livre: tradução livre: tradução livre: tradução livre: tradução livre: tradução livre: tradução livre: tradução livre: tradução livre: tradução livre: tradução livre: tradução livre: tradução livre: tradução livre: tradução livre: tradução livre: tradução livre: tradução livre: tradução livre: tradução livre: tradução livre: tradução livre: tradução livre: tradução livre: tradução livre: tradução livre: tradução livre: tradução livre: tradução livre: tradução livre: tradução livre: tradução livre: tradução livre: tradução livre: tradução livre: tradução livre: tradução livre: tradução livre: tradução livre: tradução livre: tradução livre: tradução livre: tradução livre: tradução livre: tradução livre: tradução livre: tradução livre: tradução livre: tradução livre: tradução livre: tradução livre: tradução livre: tradução livre: tradução livre: tradução livre: tradução livre: tradução livre: livre: tradução livre: tradução livre: livre: tradução livre: livre: tradução livre: tradução livre: livre: tradução livre: livre: tradução livre: livre: tradução livre: livre: livre
- Implementar um gráfico de estado stdlib com estado imutável, bordas condicionais e um ciclo de checkpoint/resume.
  Tradução do inglês para o inglês: Standard Library Implementation带不可变状态、条件边和检查点/恢复周期的状态图──
- Implementar um gráfico de estado stdlib com estado digitado, bordas condicionais e um ciclo de checkpoint/resume.

## O problema é o problema da introdução

Agentes e fluxos de trabalho compartilham um problema: quando uma execução de 40 passos falha na etapa 38, você quer retomar a partir da etapa 38, não recomeçar. Modelos de estado de segunda classe deixam os operadores tentando invadir novamente uma biblioteca que assume novas corridas.

> Agente 和工作流共享一个问题: quando 40 步运行在第38步失败时, você quer recuperar do 38 步步, em vez de começar do início.

A resposta de design do LangGraph: o estado é um objeto de primeira classe, as mutações são explícitas e os pontos de verificação persistem após cada nó.`load_state(session_id)`- Não.

> O estado é um objeto de tipo de banda de cidadão igual, a mudança operacional é evidente, o ponto de verificação é prolongado após cada ponto.`load_state(session_id)`- Não.

> **【中文解读】**Agente 和工作流共享一个问题: quando 40 步运行在第 38 步失败时, você quer recuperar do 38 步步而不是从头开始.`load_state(session_id)`- Não.

> **【拓展：LangGraph → 状态图编排】**LangGraph é uma referência para a realização de uma organização de estado no nível de base de 2026.[1] Ele vai ser usado como um ponto de função, além de uma condição de transformação, o estado em cada etapa é verificado e guardado.

> - Não .**【前置】**必須先掌握:Fase 14·01(Agent Loop) e Fase 14·12(Antropic Workflow Patterns) Langgraph é a "version permanente" do mode de trabalho.

## O conceito central.

### O gráfico

Um gráfico é definido por: Um ditado tipado (ou modelo Pydantic) que cada nó lê e muda.

> 图由以下定义:一个每个节点都读写的带类型 dict (图由以下定义:一个每个节点都读写的带类型 dict) 

- **Nodes.**Funções puras`(state) -> state_update`As atualizações são fundidas no estado após o retorno.
  Tradução:**节点。**纯函数 `(state) -> state_update`更新在返回后合并到状态中──
- **Edges.**Transições condicionais ou diretas entre nós.
  Tradução:**边。**节点之间的条件或直接转换──
- **Entry and exit.** `START`E ...`END`Os nós sentinela marcam a fronteira.
  Tradução:**入口和出口。** `START`和 `END`O posto de comando é o ponto de referência.

> **【中文解读】**O gráfico de LangGraph é definido por três elementos: 1) tipo de estado cada ponto de leitura de tipo de dit ou modelo Pydantic; 2) ponto pura função `(state) -> state_update`, retornar valor combinado ao estado; 3) 边节点之间的条件或直接转换──

Exemplo: um agente com `classify`- Não .`refund`- Não .`bug`- Não .`sales`- Não .`done`nós  um fluxo de trabalho de roteamento como um gráfico.

> exemplo: um contendo`classify`- Não.`refund`- Não.`bug`- Não.`sales`- Não.`done`节点的代理路由工作流作为图──

### Execução duradoura

Após cada nó retornar, o runtime serializa o estado e o escreve para um checkpointer (SQLite, Postgres, Redis, custom).`resume(session_id)`e retomar a partir do passo N + 1 com estado exato.

> Cada ponto retorna depois, o estado de execução é executado e é escrito no ponto de verificação.`resume(session_id)`Não é do passo N+1 Usar o estado preciso continuar.

Os documentos do LangGraph destacam explicitamente os usuários da produção onde isso importa: Klarna, Uber, JP Morgan. A alegação não é a forma do gráfico; é que a forma do gráfico mais o ponto de verificação torna a recuperação barata.

> - Não .**【类比】**O ponto de controle do LangGraph é como o "arquivo automático" do jogo: por cada um dos blocos de dados (por exemplo, um bloco de dados) é o arquivo automático de dados (por exemplo, um bloco de dados) de um bloco de dados (por exemplo, um bloco de dados) de um bloco de dados (por exemplo, um bloco de dados) de um bloco de dados (por exemplo, um bloco de dados) de um bloco de dados (por exemplo, um bloco de dados) de um bloco de dados (por exemplo, um bloco de dados) de um bloco de dados (por exemplo, um bloco de dados) de um bloco de dados (por exemplo, um bloco de dados) de um bloco de dados (por exemplo, um bloco de dados) de um bloco de dados (por exemplo, um bloco de dados) de um bloco de dados (por exemplo, um bloco de dados) de um bloco de dados (por exemplo, um bloco de dados) de um bloco de dados (por exemplo, um bloco de um bloco de dados) de um bloco de um bloco de dados (por exemplo, um bloco de um bloco de um bloco de um bloco de dados) de um bloco de um bloco de dados) de um bloco de um bloco de um bloco de dados (se pode ser executado) de um bloco de um bloco de um bloco de um bloco de um bloco de um bloco de dados (se por um bloco de um bloco de um bloco de bloco de dados) de um bloco de um bloco de um bloco de bloco de bloco de bloco de dados) de um bloco de bloco de bloco de bloco de bloco de bloco de bloco de bloco de bloco de bloco de bloco de bloco de bloco de bloco de bloco de bloco de bloco de bloco de bloco de bloco de bloco de bloco de bloco de bloco de bloco de bloco de bloco de bloco de bloco de bloco de bloco de bloco de bloco de bloco de bloco de bloco de bloco de bloco de bloco de bloco de`resume(session_id)`- Não.

> LangGraph 文档明确强调对这一点的生产用户:Klarna、Uber、J.P. Morgan──声明不是图形;而是图形的形状加上检查点使恢复成本很低──

### Transmissão

Cada nó pode produzir saída parcial. O gráfico transmite eventos por nó-delta para o chamador para que as UI atualizem à medida que o gráfico é executado.

> Cada ponto pode gerar uma parte de saída.

### Homem no circuito

Inspectar e modificar o estado entre nós. Implementações: pausa antes de um nó crítico, estado de superfície para um humano, aceitar modificações, retomar. O checkpointer torna isso fácil porque o estado já está serializado.

> O dispositivo de verificação e modificação faz com que seja fácil, pois o estado já está sequenciado.

### Memória

Curto prazo (dentro de um run  histórico de conversação no estado) e longo prazo (contínuo através do checkpointer e de uma loja separada a longo prazo).

> 短期 (一次运行内状态中的对话历史) 和长期 (长期) 跨运行 (长期) 通过检查点器加独立长期储存持久化) 长图 通过工具与外部记忆系统 (外记记系统) 长期 (长期) 跨运行 (长期) 通过检查点器加独立长期储存持久化) 长图 (长图) 通过工具与外部记忆系统 (外部记忆系统) 长期 (长期) 长期 (长期) 长期 (长期) 长期 (长期) 长期 (长期) 长期 (长期) 长期 (长期) 长期 (长期) 长期 (长期) 长期 (长期) 长期 (长期) 长期 (长期) 长期 (长期) 长期 (长期) 长期 (长期) 长期 (长期) 长期 (长期) 长期) 长期 (长期) 长期 (长期) 长期) 长期 (长期) 长期 (长期) 长期 (长期) 长期) 长期 (长期) 长期 (长期) 长期) 长期 (长期) 长期 (长期) 长期) 长期 (长期) 长期 (长期) 长期 (长期) 长期) 长期 (长期) 长期 (长期) 长期 (长期) 长期) 长期 (长期) 长期 (长期) 长期 (长期) 长期 (长期) 长期) 长期 (长期) 长期 (长期) 长期 (长期) 长期 (长期) 长期) 长期 (长期) 长期 (长期) 长期 (长期) 长期 (长期) 长期) 长期 (长期) 长期 (长期) 长期 (长期) 长期 (长期) 长期) 长期 (长期) 长期 (长期) 长期

### Três topologias

1. **Supervisor.**O roteador central LLM envia para os subagentes especializados. `create_supervisor()`em `langgraph-supervisor`(embora a equipe da LangChain em 2026 recomende fazer isso através de ferramentas que pedem diretamente mais controle de contexto).
   Tradução:**监督者。**Centro de viagens de LLM
2. **Swarm / peer-to-peer.**Os agentes transmitem directamente através de uma superfície de ferramentas compartilhada.
   Tradução:**群体/点对点。**Agente 通過共享工具接口直接移交──无中央路由──
3. **Hierarchical.**Supervisores que gerenciam sub-supervisores, implementados como subgrafos aninhados.
   Tradução:**层次化。**监督者管理子监督者, realizado para嵌套子图──

### Onde este padrão vai mal

> ️ **【易错点】**O que é que é mais comum é que não se tenha feito.`datetime.now()`Ou, como o número, estes valores vão mudar quando se recuperar.**后果**A partir do ponto de controle, o ponto é re-executado com resultados diferentes dos de funcionamento original, o estado inteiro entra em confusão.**一行修复**Todas as fontes de incerteza (tempo, tempo, tempo, tempo) devem ser capturadas no estado, não diretamente.`datetime.now()`- Não.

- **Checkpoints too small.**Apenas as conversas de ponto de verificação deixam o estado da ferramenta e a memória escreve irrecuperavelmente.
  Tradução:**检查点太小。**                                                                                                                                                                                                                                                              
- **Non-deterministic nodes.**Resume assume que as entradas de nós produzem a mesma atualização de estado. Sementes aleatórias, relógio de parede, API externas devem ser capturadas.
  Tradução:**非确定性节点。**恢复假设节点输入产生相同状态更新──随机种子、挂钟时间、外部 API 必须被捕──
- **Over-use of conditional edges.**Um gráfico com cada borda condicional é uma máquina de estado que não pode ser raciocinado.
  Tradução:**过度使用条件边。**Cada linha é um quadro condicional de um estado inexplicável.

> 🤔 **【困惑】**P: 三种拓(supervisor、swarm、hierárquico) ¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿A: 三个原则:**任务可分解为独立角色**(如客服/退款/技术) - Supervisor de selecção;**Agent 之间是协作关系而非派发关系**(如辩、相互 review) 选群;**任务有天然层次结构**(como "Producto Line A 下分 5 个团队") selecionar hierárquico。LangChain 团队 2026 年建议:能直接用工具调用解决就别上监督直接工具调用上下文控制更精细──

## Construí-lo.
```figure
langgraph-state
```

## Construí-lo

`code/main.py`Implementa um gráfico de estado stdlib:

> `code/main.py`Utilizando o padrão de biblioteca realizou um status:

- `State` um ditado com `messages`- Não .`step`- Não .`route`- Não .`output`- Não .`human_approval`- Não .
  Tradução:`State`包含 `messages`- Não.`step`- Não.`route`- Não.`output`- Não.`human_approval`O que é que é isso?
- `Node` Callable tomando estado e devolvendo um ditado de atualização.
  Tradução:`Node` aceitar estado e retornar a atualização de ditos de objetos ajustaveis.
- `StateGraph` nós + bordas + bordas condicionais + execução + resumindo.
  Tradução:`StateGraph`节点 + 边 + 条件边 + 运行 + 恢复。
- `SQLiteCheckpointer`(in-memory fake)  serializa estado após cada nó; `load(session_id)`- Não, não.
  Tradução:`SQLiteCheckpointer`(内存模拟)  Estado de sequenciação de cada ponto;`load(session_id)`- Recuperação.
- Um gráfico de demonstração: classificar -> ramo(reembolso / bug / vendas) -> portal humano -> enviar.
  No entanto, o que é um problema é que o sistema de controle de dados não é um sistema de controle de dados.

- É o que é ?

> 运行:

```
python3 code/main.py
```

O rastro mostra a primeira corrida falhando no portal humano, persistência, e depois retomando a produção final.

> O trajeto mostra que a primeira operação no controle humano falhou e se perpetuou, e depois a recuperação produziu o resultado final.

## Use-o com o framework implementado.

- **LangGraph** o referente, pronto para produção.`create_react_agent`- Não .`create_supervisor`, ou construir o seu próprio gráfico.
  Tradução:**LangGraph**参考实现,生产就绪──使用 `create_react_agent`- Não.`create_supervisor`Ou construir o seu próprio quadro.
- **AutoGen v0.4**(Lessão 14)  Modelo de ator alternativa para cenários de alta concorrência.
  Tradução:**AutoGen v0.4**(第 14 课) 高并发场景的 Actor 模型替代方案──
- **Claude Agent SDK**(Lessão 17)  Arneses gerenciados com loja de sessões integrada.
  Tradução:**Claude Agent SDK**(第 17 课) 带内置会话存储的托管框架──
- **Custom** quando você precisa de um controlo exato sobre a forma do estado ou o backend do checkpointer.
  Tradução:**自定义** Quando você precisa de um controle preciso de estado de forma ou de um ponto de inspecção no final do tempo.

## Envia-o . Produto .

`outputs/skill-state-graph.md`gera um gráfico de estado em forma de LangGraph em qualquer tempo de execução de destino com checkpointing e resume conectado.

> `outputs/skill-state-graph.md`Em qualquer objetivo de execução gerar LangGraph forma de estado gráfico, interno checkpoint e recuperação.

## Exercícios.

1. Adicionar uma borda condicional de `classify`- Não .`end`Quando a confiança da classificação está abaixo de um limiar, retoma a corrida após um conjunto humano.`route`Manualmente.
   Tradução do inglês:                                                                                                                                                                                                                                                            `classify`Até`end`Os termos são:`route`后恢复运行──
2. Troca o falso SQLite por um checkpointer SQLite real.
   Chinese: 模拟替换为真实 SQLite 检查点器──测量每步序列化开销──
3. Implementar bordas paralelas: dois nós executam simultaneamente, se fundem por um redutor personalizado.
   Tradução do inglês: implement并行边:两个节点并发运行, usando o redutor de auto-definição 合并―― não pode mudar o estado aqui?
4. Leia `langgraph-supervisor`Referência.`create_supervisor`Comparar as formas das vestígios.
   Tradução:`langgraph-supervisor`Referência:`create_supervisor`◊ Comparar os traços
5. Adicionar streaming: cada nó produz estado parcial enquanto corre. Imprima os deltas à sua chegada.
   Tradução do inglês para o inglês: Additional flow: Each node runs when there is a part state.

## Termos-chave .

| Term | What people say | What it actually means |
|------|-----------------|-----------------------|
| 术语 | 通俗说法 | 实际含义 |
| State graph | "Agent as state machine" / "Agent 即状态机" | Typed state + nodes + edges + reducers / 带类型状态 + 节点 + 边 + reducer |
| Checkpointer | "Persistence backend" / "持久化后端" | Serializes state after every node; enables resume / 每个节点后序列化状态；支持恢复 |
| Reducer | "State merger" / "状态合并器" | Function that combines current state with a node's update / 将当前状态与节点更新合并的函数 |
| Conditional edge | "Branch" / "分支" | Edge chosen by a function of state / 由状态函数选择的边 |
| Subgraph | "Nested graph" / "嵌套图" | A graph used as a node inside another graph / 作为另一个图内节点使用的图 |
| Durable execution | "Resume from failure" / "从失败恢复" | Restart at the last successful node with exact state / 在最后成功节点处用精确状态重启 |
| Supervisor | "Router LLM" / "路由 LLM" | Central dispatcher for specialist subagents / 专家子 Agent 的中央分派器 |
| Swarm | "P2P agents" / "P2P Agent" | Agents hand off via shared tools; no central router / Agent 通过共享工具移交；无中央路由 |

## Mais leitura 延伸阅读

- [LangGraph overview](https://docs.langchain.com/oss/python/langgraph/overview) os documentos de referência
  中文翻译:LangGraph 概览参考文档。
- [langgraph-supervisor reference](https://reference.langchain.com/python/langgraph/supervisor/) API de padrão de supervisão
  Tradução do inglês para inglês: langgraph-supervisor
- [AutoGen v0.4, Microsoft Research](https://www.microsoft.com/en-us/research/articles/autogen-v0-4-reimagining-the-foundation-of-agentic-ai-for-scale-extensibility-and-robustness/) Modelo alternativo de ator
  Tradução do inglês:AutoGen v0.4 微软研究Actor 模型替代方案。
- [Claude Agent SDK overview](https://platform.claude.com/docs/en/agent-sdk/overview) loja de sessões e subagentes
  Tradução do inglês:Claude Agent SDK 概览会话存储和子代理。
