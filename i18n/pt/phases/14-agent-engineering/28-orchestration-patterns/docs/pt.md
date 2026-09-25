# Padrões de Orquestração: Supervisor, Cama, Hierarquial 编排 分层 主管 模式 群体

> Quatro padrões de orquestração se repetem em 2026 frameworks: supervisor-worker, enxame / peer-to-peer, hierarquica, debate. orientação de Anthropic: "É sobre a construção do sistema certo para suas necessidades". Comece simples; adicionar topologia apenas quando um único agente mais cinco padrões de fluxo de trabalho é insuficiente.

**Type:** Learn + Build | **类型:** 构建
**Languages:** Python (stdlib) | **语言:** Python (标准库)
**Prerequisites:** Phase 14 · 12 (Workflow Patterns), Phase 14 · 25 (Multi-Agent Debate) | **前置知识:** 见原文
**Time:** ~60 minutes | **时间:** 见原文

> - Não .**【前置】**學本節前請先掌握:Fase 14·01(Agent Loop) 单代理 基础;Fase 14·12(Workflow Patterns) Anthropic 的 5 种工作流模式;Fase 14·25(Multi-Agent Debate) 多代理 协作基础。**重要原则**Primeiro, só um agente + um fluxo de trabalho, não há tempo suficiente para voltar a ter mais agentes.

## Objetivos de aprendizagem

- Cite os quatro padrões de orquestração recorrentes e quando cada um se encaixa.
- Descreva a recomendação de LangChain de 2026: supervisão baseada em ferramentas versus bibliotecas de supervisão.
- Explique a regra do Anthropic de "construir o sistema certo" e como ele abrange a escolha de topologia.
- Implementar os quatro em STDlib contra um Mestrado em Direito Comum.

## O problema é o problema da introdução

As equipes buscam "multi-agente" antes de precisarem dele. Quatro padrões se repetem em todos os quadros; uma vez que você pode nomeá-los, você pode escolher o certo  ou ignorar a topologia inteiramente.

> O time usa "Multi-Agent" quando não é necessário. Quatro padrões aparecem repetidamente no quadro; uma vez que você consegue nomeá-los, você pode escolher um certo ou saltar completamente sobre eles.


> **【中文解读】**O modelo de organização de agentes define a distribuição e coordenação de tarefas em vários agentes no sistema. O modelo é de quatro tipos: 1) a ordem das tarefas entre agentes; 2) a realização de várias tarefas entre agentes; 3) o gerenciamento de uma equipe; 4) a partilha de tarefas entre agentes; 4) a cooperação entre agentes.

> - Não .**【类比】**4 种编排模式 = 4 种公司组织:(1) **Supervisor-Worker**= 老板分活给员工 () **Swarm/P2P**= 同事相互协作 ([[: " 'OutoGroupschat " '),**Hierarchical**= 多层老板(CEO→总监→员工,超复杂任务);(4) **Debate**= 委员会投票 (comissão de votação)

> ️ **【易错点】**编排选错的 3 个坑:(1) **简单任务用多 Agent** Single Agent + 5 工具能解决 80% 需求,过早使用监督反而增加复杂度;Antropic 明确建议"先简单再拓"――(2) **Supervisor 成瓶颈** todas as tarefas passadas por supervisor 转发,单点延迟 + 单点失败;让工人间直接通信(仅必要时报 supervisor)**没设 worker 超时**lora trabalhadora 卡住整个流程; cada trabalhador 调用必须设时out,超时返回降级结果──

> **{【拓展：Agent 编排是 2026 年生产 Agent 系统的核心挑战。Anthropic 的模式分类（P...】}**O processo de agência 编排是2026年生产 系统的核心挑战――Anthropic的模式分类 (Prompt Chaining、Routing、Parallelization、Orchestrator-Workers) tornou-se padrão――na aplicação real, a maioria dos sistemas mistura-se com vários modelos, como por exemplo, o sistema de clientes, que primeiro utiliza o modelo de rotas, reutiliza o modelo de camadas distribuído para um agente específico――LangGraph's state diagram é um instrumento de regeneração da linha de trabalho――
## O conceito central.

### Supervisor-trabalhador

- Um LLM central de envio enviado para agentes especializados.
- Decide: voltar ao eu, entregar ao especialista, terminar.
- Os especialistas não falam entre si; toda a rotina passa pelo supervisor.

Estruturas: LangGraph `create_supervisor`, Orquestra Antropical-trabalhadores, CrewAI Processos Hierárquicos.

> 编排模式描述多 系统的组织方式──主要模式包括:监督者(中央路由)、群体(点对点移交)、层次化(嵌套监督)、管道(顺序处理)──

**2026 LangChain recommendation:**Fazer supervisão através de chamadas diretas de ferramentas em vez de `create_supervisor`. dá um controlo mais preciso da engenharia de contexto.

> **2026 年 LangChain 建议：**通过直接工具调用而不是 `create_supervisor`Para realizar o controle, fornecer um controle mais preciso do projeto, você pode decidir com precisão o que cada especialista ver.

### Swarm / peer-to-peer

- Os agentes transmitem directamente através de uma superfície de ferramentas compartilhada.
- Sem roteador central.
- Menos atraso do que o supervisor (menos saltos).
- Mais difícil de raciocinar (não há um único ponto de controlo).

Estruturas: Topologia do enxame de LangGraph, transferências do SDK OpenAI Agents (quando todos os agentes podem transferir para todos os outros).

> 编排模式描述多 系统的组织方式──主要模式包括:监督者(中央路由)、群体(点对点移交)、层次化(嵌套监督)、管道(顺序处理)──

### - Hierarquias

- Supervisores gerentes sub-supervisores gerentes de trabalhadores.
- Implementados como subgrafos aninhados em LangGraph; tripulações aninhadas em CrewAI.
- Escala para grandes populações de agentes, a custo da complexidade operacional.

Quando é necessário: quando o orçamento contextual de uma única supervisão não pode conter descrições de todos os especialistas.

> Qual é a necessidade de: quando um único supervisor não pode suportar a descrição de todos os especialistas?

> 编排模式描述多 系统的组织方式──主要模式包括:监督者(中央路由)、群体(点对点移交)、层次化(嵌套监督)、管道(顺序处理)──

### Debate

- Proponentes paralelos + crítica cruzada iterativa (Lessão 25).
- Não é realmente orquestração  mais verificação  mas aparece como uma escolha de topologia em quadros.

### Equipamentos autônomos vs fluxos deterministas

A CrewAI formaliza dois modos de implantação:

- **Flow**para a automação determinista orientada por eventos (ponto de partida recomendado para a produção).
- **Crew**para a colaboração autónoma baseada em funções.

Isto é ortogonal aos quatro padrões acima, mas mapeia a topologia: Flow é tipicamente supervisor ou hierárquico; Crew é tipicamente supervisor com um roteador LLM.

> 编排模式描述多 系统的组织方式──主要模式包括:监督者(中央路由)、群体(点对点移交)、层次化(嵌套监督)、管道(顺序处理)──

### A orientação do Antropic

"O sucesso no espaço de LLM não é sobre a construção do sistema mais sofisticado, é sobre a construção do sistema certo para as suas necessidades".

> 编排模式描述多 系统的组织方式──主要模式包括:监督者(中央路由)、群体(点对点移交)、层次化(嵌套监督)、管道(顺序处理)──

Ordem de decisão:

1. O único agente + padrões de fluxo de trabalho (Lessão 12)
2. Supervisor-trabalhador  quando tiver 2-4 especialistas.
3. Swarm  quando a latência importa mais do que a clareza do raciocínio.
4. Hierarquica  apenas quando o orçamento do contexto da supervisão falhar.
5. Debate  quando a precisão é mais importante do que o custo.

### Onde este padrão vai mal

- **Topology-first thinking.**"Precisamos de multi-agente" antes de identificar o problema que multi-agente resolve.
- **Bouncing handoffs in swarm.**A -> B -> A -> B. Use contadores de saltos.
- **Fake hierarchy.**Três camadas por "empresa", duas equipes reais.

> **拓扑优先思维。**Antes de decidir qual é o problema, diz: "Precisamos de mais agentes".
> **群体中弹跳交接。**A -> B -> A -> B。 Utilizar salto num contador。
> **虚假层级。**Porque "níveis empresariais" já têm três níveis; na realidade, existem apenas dois grupos.

## Construí-lo e realizei-o.
```figure
orchestration-pattern
```

## Construí-lo

`code/main.py`Implementa os quatro padrões em stdlib contra um LLM escrito:

> 编排模式描述多 系统的组织方式──主要模式包括:监督者(中央路由)、群体(点对点移交)、层次化(嵌套监督)、管道(顺序处理)──

- `Supervisor`Roteador central.
- `Swarm`- Peer-to-peer com transferências diretas.
- `Hierarchical` Supervisores de supervisores.
- `Debate` Propostas paralelas + crítica.

Cada padrão lida com a mesma tarefa de três intenções (reembolso / bug / vendas).

> 编排模式描述多 系统的组织方式──主要模式包括:监督者(中央路由)、群体(点对点移交)、层次化(嵌套监督)、管道(顺序处理)──

- É o que é ?

```
python3 code/main.py
```

Output: rastreamento por padrão + contagem de opções. Supervisor é mais limpo; enxame é mais curto; hierárquico é mais profundo; debate é mais caro.

> 输出: cada modo de acompanhamento + 操作数──监督者最清晰;群体最短;层级最深;辩论最昂贵──

> 编排模式描述多 系统的组织方式──主要模式包括:监督者(中央路由)、群体(点对点移交)、层次化(嵌套监督)、管道(顺序处理)──

## Use-o com o framework implementado.

- **LangGraph**para supervisores e hierárquicos (subgrafos aninhados).
- **OpenAI Agents SDK**para transferências como ferramentas (em forma de supervisor).
- **CrewAI Flow**para a determinação da produção.
- **Custom**Para debater ou quando quiserem o controlo exato.

## Envia-o . Produto .

`outputs/skill-orchestration-picker.md`escolhe uma topologia e a implementa.

> `outputs/skill-orchestration-picker.md`选择一个拓并实现它──

> 编排模式描述多 系统的组织方式──主要模式包括:监督者(中央路由)、群体(点对点移交)、层次化(嵌套监督)、管道(顺序处理)──

## Exercícios.

1. Converter um supervisor-trabalhador em um enxame removendo o roteador.
  Tradução do inglês para tradução do inglês:
2. Adicione um contador de saltos ao enxame: rejeita após 3 entregas.
  Tradução do inglês para tradução do inglês:
3. Construir um sistema hierárquico de dois níveis para um domínio de 12 especialistas. Onde o orçamento contextual falha sem anidar?
  Tradução do inglês para tradução do inglês:
4. Profila os quatro padrões de uma carga de trabalho em forma de produção. Qual vence em que métrica (latencia, custo, precisão, depurabilidade)?
  Tradução do inglês para tradução do inglês:
5. Leia o post da Anthropic sobre "Eficientes Agentes de Construção", mapeando cada um dos fluxos de produção para um dos quatro.
  Tradução do inglês para tradução do inglês:

## Termos-chave .

| Term | What people say | What it actually means |
|------|----------------|------------------------|---|
| Supervisor-worker | "Router + specialists" | Central LLM dispatches to specialists; they don't talk to each other |  |
| Swarm | "Peer-to-peer" | Direct handoffs via shared tools; no central router |  |
| Hierarchical | "Supervisors of supervisors" | Nested subgraphs for large populations |  |
| Debate | "Proposer + critique" | Parallel proposers, cross-critique (Lesson 25) |  |
| Tool-call-based supervision | "Supervisor without a library" | Implement supervisor as direct tool calls for context control |  |
| Crew | "Autonomous team" | CrewAI's role-based collaboration mode |  |
| Flow | "Deterministic workflow" | CrewAI's event-driven production mode |  |

## Mais leitura 延伸阅读

- [Anthropic, Building Effective Agents](https://www.anthropic.com/research/building-effective-agents) cinco padrões + agente vs fluxo de trabalho
  Tradução do português:
- [LangGraph overview](https://docs.langchain.com/oss/python/langgraph/overview) supervisor, enxame, hierarquica
  Tradução do português:
- [CrewAI docs](https://docs.crewai.com/en/introduction) Tripulação vs Fluxo
  Tradução do português:
- [Du et al., Society of Minds (arXiv:2305.14325)](https://arxiv.org/abs/2305.14325) Padrão de debate
  Tradução do português:
