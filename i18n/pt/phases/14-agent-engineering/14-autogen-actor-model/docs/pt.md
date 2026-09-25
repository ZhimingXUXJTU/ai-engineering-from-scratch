# AutoGen v0.4: Modelo de ator e quadro de agente
# O Modelo de Ator para Agentes  Mensagens de sincronia e tempos de execução tipografados

> Agentes como atores: intercâmbio de mensagens asíncronas, geradores de eventos, isolamento de falhas, concurência natural. AutoGen v0.4 (Microsoft Research, janeiro 2025) redesenhou a orquestração de agentes em torno deste modelo; a estrutura está agora em modo de manutenção, com a Microsoft Agent Framework (previsão pública de outubro 2025) como seu sucessor de produção.

> **【中文解读】**AutoGen v0.4 (Microsoft Research Center, 1 de janeiro de 2025) Redesignado em torno do modelo Actor  Ação (Actor) 编排, 异步消息交换, 事件驱动, 故障隔离, 天然并发, 事件驱动, 事件驱动, 故障隔离, 天然并发, ), o framework está atualmente em manutenção.

**Type:** Learn + Build | **类型:** 学习 + 构建
**Languages:** Python (stdlib) | **语言:** Python (标准库)
**Prerequisites:** Phase 14 · 01 (Agent Loop), Phase 14 · 12 (Workflow Patterns) | **前置知识:** Phase 14 · 01 (Agent 循环), Phase 14 · 12 (工作流模式)
**Time:** ~75 minutes | **时间:** ~75 分钟

## Objetivos de aprendizagem

- Descreva o modelo de ator: agentes como atores, mensagens como o único IPC, isolamento de falhas por ator.
  Ação de um ator, como um ator, informação como um único processo de comunicação, cada ator, como um ator independente.
- Nomear as três camadas de API do AutoGen v0.4  Core, AgentChat, Extensions  e para o que cada uma é.
  中文翻译:说出 AutoGen v0.4 三个 API层Core、AgentChat、Extensions及各自的用途──
- Explique por que a desconexão da entrega de mensagens da manipulação dá isolamento de falhas e simetria natural.
  Tradução do inglês para "Legendamento de um texto"
- Implementar um stdlib actor runtime em Python e puxar um fluxo de revisão de código de dois agentes para ele.
  Tradução do idioma: Us Python 标准库实现 Actor 运行时并将双 Agent 代码审查流程移植到其上──

## O problema é o problema da introdução

A maioria dos quadros de agentes são sincrónicos: um agente produz, um agente consome, em uma pilha de chamadas. Falhas caem na pilha. A concurrença é ligada. A distribuição requer reescritura.

> A maioria dos agentes  estrutura é simultânea: um agente produzir, um agente consumir, em调用中, 失败会使崩──并发是后加的──分布式需要重写──

A resposta do AutoGen v0.4 é: o modelo de ator. Cada agente é um ator com uma caixa de entrada privada. As mensagens são a única interação. O tempo de execução desacopla a entrega do manuseio. As falhas isolam-se a um ator. A concorrência é nativa. A distribuição é apenas um transporte diferente.

> A resposta de AutoGen v0.4:Actor 模型── cada agente é um ator com caixa de correio privada──消息是唯一交互方式──运行时将交付与处理解──失败隔离到一个 Actor──并发是原生──分布式只是不同的传输方式──

> **【中文解读】**AutoGen v0.4  Adoptando Actor 模型 Cada Agente é um Actor independente, através de mensagens de comunicação.

> **【拓展：AutoGen 的演进】**AutoGen desenvolvido pelo Microsoft Research Institute, v0.4 (2025) é uma grande reestruturação. De um modelo de diálogo de v0.3 para o modelo de Actor, inspiração vem do modelo de Erlang/Akka.

> - Não .**【前置】**必須先掌握:Fase 14·01(Agent Loop) 和Fase 14·12(Antropic Workflow Patterns) 本節是这些模式在"并发场景"下延伸──还需要"Actor 模型"的基本概念如果不知道Erlang/Akka是什么,先去补一节分布式系统课──本节硬核在"异步消息传递"而不是"LLM 调用"──

## O conceito central.

### Atores

Um ator tem:

> Um ator tem:

- Um Estado privado (nunca tocado diretamente por fora).
  Tradução do inglês: Private State (私有状态)
- Uma caixa de entrada (fila de mensagens).
  Tradução do inglês:
- Um manipulador:`receive(message) -> effects`onde os efeitos podem ser "responde", "enviar para outro ator", "espalhar um novo ator", "atender o estado", "deter-se".
  Tradução do português:`receive(message) -> effects`O resultado pode ser "回复", "enviar para outros atores", "crear um novo ator", "actualizar o estado", "arrê-se".

Dois atores não podem partilhar memória, só podem enviar mensagens.

> - Não .**【类比】**Ator 模型像办公室里互相见的同事: cada um tem seu próprio empreito (private state) e caixa de receita (消息队列) ⋅ Você quer fazer com que seu colega ajude, não pode ir diretamente para o seu empreito (共享内存), só pode enviar um e-mail (发消息) ⋅**关键**Não afeta os outros. É o que se passa.

> Dois atores não podem partilhar a memória.

### Três camadas de API no AutoGen v0.4
### Três camadas de API

AutoGen v0.4 divide a sua superfície em três:

1. **Core.**Estrutura de actores de baixo nível. `AgentRuntime`- Não .`Agent`- Não .`Message`- Não .`Topic`Troca de mensagens sincronizada, orientada por eventos.
   Tradução:**Core。**Ação de base 框架。`AgentRuntime`- Não.`Agent`- Não.`Message`- Não.`Topic`异步消息交换,事件驱动──
2. **AgentChat.**API de alto nível orientado para tarefas (substituição do ConversableAgent do v0.2). `AssistantAgent`- Não .`UserProxyAgent`- Não .`RoundRobinGroupChat`- Não .`SelectorGroupChat`- Não .
   Tradução:**AgentChat。**任务驱动的高级 API(替代 v0.2 的可谈话机) 』`AssistantAgent`- Não.`UserProxyAgent`- Não.`RoundRobinGroupChat`- Não.`SelectorGroupChat`- Não.
3. **Extensions.**Integrações  OpenAI, Anthropic, Azure, ferramentas, memória.
   Tradução:**Extensions。**集成OpenAI、Antropic、Azure、工具、记忆──

### Por que é importante o desacoplamento

No modelo v0.2, chamando`agent_a.chat(agent_b)`Bloqueia sincronicamente o agente_a até o agente_b retornar.`send(agent_b, msg)`O tempo de execução entrega mais tarde.

> Em v0.2 模型中,调用 `agent_a.chat(agent_b)`Com o agente de bloqueio até o agente de regresso.`send(agent_b, msg)`A partir de agora, o agente_b poderá enviar uma mensagem para a caixa de recepção e devolver-a.

- **Fault isolation.**Agente B que se desabar não desabar Agente A  o tempo de execução pega a falha no manipulador de B e decide o que fazer (log, retry, letra morta).
  Tradução:**故障隔离。**Agente B 崩 não causará que Agente A 崩运行时在B's processador中捕获故障并决定做什么 () 日志、重试、死信) 
- **Natural concurrency.**Muitas mensagens em voo ao mesmo tempo; os atores processam a caixa de entrada simultaneamente.
  Tradução:**天然并发。**Dois relatórios são transmitidos ao mesmo tempo; O ator não é responsável por processá-los.
- **Distribution-ready.**O cartão de entrada + transporte é a mesma abstração, quer o ator esteja em processo ou em outro hospedeiro.
  Tradução:**分布式就绪。**O recebimento + a transmissão são os mesmos abstractos, seja o ator no processo ou na outra máquina.

> ️ **【易错点】**Usado por um ator, mas esqueci-me de que a mensagem tem de ser processada.**后果**O processo de produção é distribuído em vários momentos, e o processo de produção não chega ao seu objeto.**一行修复**Todos os dados devem ser definidos com pydantic/dataclass/JSON-schema, proibindo transmitir lambda、文件句柄、数据库连接等不可序列化对象──

### Topologias

- **RoundRobinGroupChat.**Os agentes fazem turnos numa rotação fixa.
  Tradução:**RoundRobinGroupChat。**Agente 按固定轮换顺序轮流──
- **SelectorGroupChat.**Um agente selector escolhe quem vai a seguir com base no contexto da conversa.
  Tradução:**SelectorGroupChat。**选择器 Agente 根据对话上下文选择下一个发言人──
- **Magentic-One.**Equipe de referência multi-agente para navegação na web, execução de código, tratamento de arquivos.
  Tradução:**Magentic-One。**Utilizado para a página de web para a navegação, execução de código, tratamento de documentos, referência para Agente  Equipo  Baseado em Agente Chat  Construção 

### Observabilidade

O suporte à OpenTelemetry está incorporado.`gen_ai.*`Atributos de acordo com as convenções semânticas OTel GenAI de 2026 (Lessão 23).

> OpenTelemetry 支持内置──每条消息发发出一个跨度;工具调用携带 `gen_ai.*`属性, conforme 2026 anos OTel GenAI 语义约定(第 23 课)

### Status: modo de manutenção

Começo de 2026: AutoGen v0.7.x é estável para pesquisa e prototyping. A Microsoft mudou o desenvolvimento ativo para o Microsoft Agent Framework, o sucessor da produção (previsão pública 1 de outubro de 2025; 1.0 GA foi alvo para o final do primeiro trimestre de 2026).

```figure
actor-mailbox
```

> 🤔 **【困惑】**P: AutoGen  já entrou em um modelo de manutenção, eu também deveria aprender?**别在生产上选 AutoGen**△原因:(1) 微软 já passou para Microsoft Agent Framework(MAF),AutoGen não mais obtém novas características;(2) Actor 模型本身是个**经久不衰的分布式设计思想**(de 1973 论文 Hewitt,比 LLM 老 50 年), entender que é importante avaliar MAF、Erlang、Akka、Ray  都有帮助──把 AutoGen当"教材",把 MAF或LangGraph当"生产工具"──

> 2026 início de ano:AutoGen v0.7.x em pesquisa e desenvolvimento de modelo estável. Microsoft já vai transferir o desenvolvimento ativo para o Microsoft Agent Framework.

## Construí-lo.

`code/main.py`Implementa um runtime de atores stdlib:

> `code/main.py`Usando o padrão de execução do Actor:

- `Message` cargas úteis tipografadas com `sender`- Não .`recipient`- Não .`topic`- Não .`body`- Não .
  Tradução:`Message`- Não .`sender`- Não.`recipient`- Não.`topic`- Não.`body`O que é o carregamento?
- `Actor` abstracto com `receive(message, runtime)`- Não .
  Tradução:`Actor`- Não .`receive(message, runtime)`O que é que é isso?
- `Runtime` Loop de eventos com uma fila compartilhada, entrega, isolamento de falhas.
  Tradução:`Runtime`带共享队列、投递、故障隔离的事件循环──
- Uma demonstração de dois atores:`ReviewerAgent`código de revisão, `ChecklistAgent`Elas trocam mensagens até chegarem a um consenso.
  Tradução do português:`ReviewerAgent`审查代码,`ChecklistAgent`运行检查清单; eles trocaram notícias até chegarem a um acordo.

- É o que é ?

> 运行:

```
python3 code/main.py
```

O rastro mostra a entrega de mensagens, um fracasso simulado em um ator que não bate o outro, e convergência em um veredicto compartilhado.

> A forma como um ator se falha não levará a outro colapso, bem como a recepção de decisões compartilhadas.

## Use-o com o framework implementado.

- **AutoGen v0.4/v0.7**(manutenção)  estável para pesquisa, prototipagem, padrões multi-agentes.
  Tradução:**AutoGen v0.4/v0.7**(维护中) 研究、原型、多 Agent 模式稳定──
- **Microsoft Agent Framework**(previsão pública)  o caminho para a frente; as mesmas ideias de modelo de atores em uma API atualizada.
  Tradução:**Microsoft Agent Framework**(公开预览) 前进方向; 更新的API 中体现相同的 Actor 模型理念──
- **Microsoft Agent Framework** a sucessora da produção (previsão pública de outubro de 2025); as mesmas ideias de modelo de ator em uma API atualizada.
- **LangGraph swarm topology**(Lessão 13)  padrão semelhante através de transferências de ferramentas compartilhadas.
  Tradução:**LangGraph 群体拓扑**(第 13 课)  através de ferramentas compartilhadas de transferência de um modelo semelhante.
- **Custom actor runtime** quando precise de transporte específico (NATS, RabbitMQ, gRPC).
  Tradução:**自定义 Actor 运行时**Quando precisares de uma transmissão específica (NATS, RabbitMQ, GRPC)

## Envia-o . Produto .

`outputs/skill-actor-runtime.md`gera um tempo de execução mínimo de atores mais um modelo de equipe (RoundRobin ou Selector) para uma determinada tarefa multi-agente.

> `outputs/skill-actor-runtime.md`Para determinar mais Agente  tarefa gerar menor Actor 运行时加团队模板(RoundRobin ou Selector) ⋅

## Exercícios.

1. Adicione uma fila de letras mortas: quando um manipulador levantar, estacione a mensagem falha para inspeção humana.
   Quando o processador lança uma anomalia, será que a mensagem falha é colocada para inspeção artificial.
2. Implementação `SelectorGroupChat`: um ator selector escolhe quem processar a próxima mensagem com base no estado da conversação.
   Tradução do português:`SelectorGroupChat`Ação: Ação: Ação: Ação: Ação: Ação: Ação: Ação: Ação: Ação: Ação: Ação: Ação: Ação: Ação: Ação: Ação: Ação: Ação: Ação: Ação: Ação: Ação: Ação: Ação: Ação: Ação: Ação: Ação: Ação: Ação: Ação: Ação: Ação: Ação: Ação: Ação: Ação: Ação: Ação: Ação: Ação: Ação: Ação: Ação: Ação: Ação: Ação: Ação: Ação: Ação: Ação: Ação: Ação: Ação: Ação: Ação: Ação: Ação: Ação: Ação: Ação: Ação: Ação: Ação: Ação: Ação: Ação: Ação: Ação: Ação: Ação: Ação: Ação: Ação: Ação: Ação: Ação: Ação: Ação: Ação: Ação: Ação: Ação: Ação: Ação: Ação: Ação: Ação: Ação: Ação: Ação: Ação: Ação: Ação: Ação: Ação: Ação: Ação: Ação: Ação: Ação: Ação: Ação: Ação: Ação: Ação: Ação: Ação: Ação: Ação: Ação: Ação: Ação: Ação: Ação: Ação: Ação: Ação: Ação: Ação: Ação: Ação: Ação: Ação: Ação: de de de de de de de de de de de de de de de de de de de de de de de de de de de de de de de de de de de de de de de de de de de de de de de de de de de de de de de de de de de de de de de de de de de de de de de de de de de de de de de de de de de de de de de de de de de de de de de de de de de de de de de de de de de de de de de de de de de de de de de de de de de de de de de de de de de de
3. Adicionar transporte distribuído: trocar a fila de processo por um servidor JSON-over-HTTP para que os atores possam executar processos separados.
   Chinese: 添加分布式传输:将进程内队列替换为 JSON-over-HTTP 服务器,使 Actor可以在独立进程中运行──
4. Transmitir um tempo de OTel por mensagem (ou um no-op substitutivo).`gen_ai.agent.name`- Não .`gen_ai.operation.name`Por lição 23.
   Tradução do português em inglês:`gen_ai.agent.name`- Não.`gen_ai.operation.name`- Não.
5. Leia o post de arquitetura do AutoGen v0.4.`autogen_core`O que é que você deixou de ser importante na produção?
   Tradução do inglês: read AutoGen v0.4's architecture文章──将玩具移植到真正的`autogen_core`O que é que você passou por cima?

## Termos-chave .

| Term | What people say | What it actually means |
|------|-----------------|-----------------------|
| 术语 | 通俗说法 | 实际含义 |
| Actor | "Agent" / "Agent" | Private state + inbox + handler; no shared memory / 私有状态 + 收件箱 + 处理器；无共享内存 |
| Message | "Event" / "事件" | Typed payload; the only way actors interact / 带类型载荷；Actor 唯一的交互方式 |
| Inbox | "Mailbox" / "邮箱" | Per-actor queue of pending messages / 每个 Actor 的待处理消息队列 |
| Runtime | "Agent host" / "Agent 宿主" | Event loop that routes messages and isolates failures / 路由消息和隔离故障的事件循环 |
| Topic | "Channel" / "通道" | Named publish-subscribe route between actors / Actor 之间的命名发布-订阅路由 |
| Fault isolation | "Let it crash" / "让它崩溃" | One actor failing does not crash others / 一个 Actor 失败不会导致其他崩溃 |
| RoundRobinGroupChat | "Fixed-rotation team" / "固定轮换团队" | Agents take turns in order / Agent 按顺序轮流 |
| SelectorGroupChat | "Context-routed team" / "上下文路由团队" | Selector picks who goes next / 选择器选择下一个发言者 |
| Magentic-One | "Reference team" / "参考团队" | Multi-agent squad for web + code + files / 用于网页+代码+文件的多 Agent 小队 |

## Mais leitura 延伸阅读

- [AutoGen v0.4, Microsoft Research](https://www.microsoft.com/en-us/research/articles/autogen-v0-4-reimagining-the-foundation-of-agentic-ai-for-scale-extensibility-and-robustness/) o post de redesenho
  中文翻译:AutoGen v0.4 微软研究院重新设计文章──
- [LangGraph overview](https://docs.langchain.com/oss/python/langgraph/overview) Alternativa em forma de gráfico
  中文翻译:LangGraph 概览图形替代方案──
- [OpenTelemetry GenAI semantic conventions](https://opentelemetry.io/docs/specs/semconv/gen-ai/) extensão emite AutoGen por padrão
  中文翻译:OpenTelemetry GenAI 语义约定AutoGen 默认发射跨度──
