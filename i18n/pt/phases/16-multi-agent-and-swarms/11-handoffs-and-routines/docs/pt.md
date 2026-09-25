# "Das e rotinas" "Orquestração sem Estado"

> O Swarm (outubro de 2024) da OpenAI destila a orquestração multi-agente para dois primitivos: **routines**(instruções + ferramentas como um sistema de instrução) e **handoffs**(uma ferramenta que devolve outro agente). Não há máquina de Estado, não há DSL ramificante, as rotas de LLM chamando a ferramenta de transferência certa. O OpenAI Agents SDK (março 2025) é o sucessor da produção. O próprio enxame continua a ser a referência conceitual mais limpa. O padrão é viral porque a superfície da API é aproximadamente "agente = prompt + ferramentas; transferência = agente de devolução de função". Limitação: sem estado, então a memória é o problema do chamador.

> **【中文解读】**Esta secção apresenta os processos e processos de comunicação e de controlo de tarefas de transferência entre agentes.

> **【拓展：handoffs and routines→具体应用】**交接(Handoffs) é o conceito central do OpenAI Agents SDKAgent A vai transferir o controle para o Agente B。Key Design Decision:(1) 上下文传递B 收到多少 A 的历史?(2) 恢复机制B 完成后控制权回到 A 还是交给C?(3) 超时处理B 如果卡住怎么办?


**Type:** Learn + Build | **类型:** 学习 + 构建
**Languages:** Python (stdlib) | **语言:** Python (标准库)
**Prerequisites:** Phase 16 · 04 (Primitive Model) | **前置知识:** Phase 16 · 04 (原语模型)
**Time:** ~60 minutes | **时间:** ~60 分钟

> - Não .**【前置】**学本节前请先掌握:Fase 16·04(原语模型)、Fase 14·07(工具调用)。OpenAI Swarm 把多 Agent 简化为2 原语:routine(系统提示+工具)+ handoff(返回另一个代理的工具)。
> - Não .**【类比】**Handoff = "客服转接"──用户问技术问题→客服 A 接听→判断需要技术支持→转接给技术专员 B。Swarm 的天才之处:handoff 就是一个普通工具调用(回归代理),LLM 自动路由──无状态机、无 DSL,几百行代码搞定──OpenAI Agents SDK 是生产版本──

## Problema Introdução

Cada framework multi-agente quer que você aprenda o seu DSL: nós e bordas de LangGraph, equipes e tarefas CrewAI, AutoGen GroupChat e gerentes. Os DSLs são abstrações reais, mas eles fazem a coisa sentir mais pesada do que precisa ser.

> Cada um dos vários agentes quer que você aprenda os níveis e bordas do DSL:LangGraph, a equipe e as tarefas do CrewAI, o Grupo de Chat e gerente do AutoGen.

O bloqueio DSL é o imposto de estrutura multi-agente. Cada DSL tem seus próprios conceitos, suas próprias ferramentas de depuração, sua própria comunidade. Uma vez que você se compromete, a migração é cara. A aposta do Swarm: pular o DSL inteiramente, usar a chamada de ferramentas existente do modelo.

> DSL 锁定是多代理 框架税── cada DSL tem seu próprio conceito、 seu próprio instrumento de调试、 sua própria comunidade── once you promise,迁移昂贵──Swarm's 注: completamente saltar DSL, usar o modelo existente ferramentas de调用──

O grupo empurra na direção oposta: use a capacidade de chamada de ferramentas que o modelo já tem. As entregas se tornam chamadas de ferramentas. O orquestrador é o agente que atualmente mantém a conversa. A máquina de estado está implícita nas instruções do sistema dos agentes.

> Swarm 推向相反的方向: usar o modelo de ferramentas existentes capacidade de调用.

A visão é profunda: não é necessário um DSL de orquestração porque os LLM já são orquestrais.

> 洞察深: você não precisa editar DSL, porque LLM 已是编排器── cada LLM 调用根据上下文决定下一步做什么──交接只是将该决策暴露为模型可调用工具──

## Conceptos básicos

### Dois primitivos

**Routine.**Um sistema de instruções que define o papel de um agente e as ferramentas disponíveis. Pense nisso como um conjunto de instruções com escopo: "você é um agente de triagem; se o usuário perguntar sobre reembolsos, entregue ao agente de reembolso".

> **例程。**definição de Agente 角色和可用工具的系统提示──把它想象成一组范围化的命令:" Você é um Agente de diagnóstico; se o usuário perguntar sobre o reembolso, entregue-se ao Agente de reembolso──"

**Handoff.**Uma ferramenta que o agente pode chamar que retorna um novo objeto do agente.

> **交接。**Agente pode ser utilizado como ferramenta, devolver um novo Agente a um objeto. Agente de controle de carga. Agente de devolução e para a próxima rodada de atividade de troca. Agente de câmbio.

É toda a abstração.

> É o que é todo o abstracto.

```
def transfer_to_refunds():
    return refund_agent  # Swarm sees Agent return → switch active agent

triage_agent = Agent(
    name="triage",
    instructions="Route the user to the right specialist.",
    functions=[transfer_to_refunds, transfer_to_sales, transfer_to_support],
)
```

O pedido do sistema do agente de triagem faz com que ele escolha a transferência certa com base na mensagem do usuário.

> O sistema de instruções do Agente de diagnóstico permite que ele escolha o caminho de execução de acordo com a mensagem do usuário.

Este é o movimento elegante: reutilizar a infraestrutura de chamada de ferramentas existente do modelo para a orquestração. Sem novo DSL, sem editor de gráficos, sem máquina de estado. O modelo já sabe como escolher a ferramenta certa; as entregas são apenas ferramentas que retornam agentes.

> É uma iniciativa de Ulia: reutilizar os instrumentos existentes do modelo para a organização da infraestrutura. Não há novos DSLs, não há editores de gráficos, não há máquinas de estado. O modelo já sabe como escolher os instrumentos corretos; o contato é apenas o instrumento de devolvimento do Agente.

### Por que é viral

- **Small API.**Dois conceitos a aprender.
  Tradução:**小型 API。**Só preciso de aprender dois conceitos.
- **Uses what the model already does.**A chamada de ferramentas já é de nível de produção entre os fornecedores.
  Tradução:**使用模型已有的能力。**工具调用已在各供应商中已是生产级.
- **No state-machine burden.**Não descreve o gráfico, as instruções dos agentes descrevem a quem entregam.
  Tradução:**无状态机负担。**Não descreve o quadro; As dicas do agente descrevem-nas.

### O comércio sem Estado

O conjunto é explicitamente sem estatuto entre corridas. O framework mantém um histórico de mensagem durante uma corrida, mas não persiste nada. Memória, continuidade, tarefas de longa duração  todo o problema do chamador.

> Swarm entre os operadores é claro que não há nenhum estado.

O projeto sem estado é intencional: torna o framework trivialmente reiniciavel, horizontalmente escalável e depurável (cada execução é independente). O custo é que os fluxos de trabalho de longa duração exigem gerenciamento externo de estado (base de dados, filas, pontos de verificação).

> 无状态设计是有意的: faz com que o framework possa ser facilmente reiniciado, expandido e ajustado, cada vez que se executa independentemente.

Na produção (OpenAI Agents SDK, março 2025) esta foi uma das principais coisas que mudou: o SDK adiciona gerenciamento de sessões incorporado, barris de segurança e rastreamento, mantendo a entrega primitiva.

> Em produção ambiente (OpenAI Agents SDK, 2025 3 月), esta é uma das principais mudanças: o SDK adicionou a gestão de sessões internas, a protecção e o rastreamento, mantendo o contacto original.

### Quando o Enxame/Handoffs se encaixam

- **Triage patterns.**O agente da linha de frente encaminha o usuário para um especialista.
  Tradução:**分诊模式。**O agente da linha de trabalho vai ligar o usuário para o especialista.
- **Skill-based handoffs.**"Se a tarefa precisa de código, ligue ao programador; se precisa de pesquisa, ligue ao pesquisador".
  Tradução:**基于技能的交接。**"Se as tarefas precisam de codificação, use o codificador; se precisam de estudo, use o pesquisador"".
- **Short, bounded conversations.**Suporte ao cliente, FAQ-to-ticket, fluxos de trabalho simples.
  Tradução:**短、有界对话。**客户支持、FAQ 到工单、简单工作流──

### Quando o Enxame luta

- **Long sessions with shared memory.**As transferências resetaram o estado da conversa para o histórico de resposta do novo agente.
  Tradução:**需要共享内存的长会话。**交接将对话状态重置为新代理的提示加历史―― não há memória do administrador do调用员, não há estado permanente do trans-agente――
- **Parallel execution.**O Handoff é um-a-tempo  os agentes ativos alternam. Paralelamente requer que o chamador orquestre várias corridas Swarm.
  Tradução:**并行执行。**交接是逐一的活动 交换――并行性需要调用者编排多个 Swarm 运行――
- **Audit and replay.**As corridas sem estatuto são difíceis de repeti-las exatamente; a escolha de transferência do LLM não é determinista.
  Tradução:**审计和回放。**无状态运行难以精确回放; LLM 交接选择不确定性──

### O programa de desenvolvimento de agentes OpenAI (março 2025)

O sucessor da produção acrescenta:

> Produção de produtos

- **Session state.**Fios persistentes em corridas.
  Tradução:**会话状态。**跨运行的持久线程──
- **Guardrails.**Anéis de validação de entrada/saída.
  Tradução:**防护栏。**输入/输出验证子──
- **Tracing.**Todas as chamadas e transferências de ferramentas estão registradas.
  Tradução:**追踪。**Cada vez que as ferramentas são usadas e as comunicações são registradas.
- **Handoff filters.**Controlar o que o contexto transfere na transferência.
  Tradução:**交接过滤器。**Controle o contato, transmite o que está a acontecer.

O primitivo de entrega sobrevive; a ergonomia da produção é adicionada ao seu redor.

> 交接原语存活下来; produção humana engenharia em torno dele adicionar.

Esta é a progressão padrão para abstracções virais: naves primitivas simples primeiro (Swarm), produção preocupa camada em cima (Agents SDK).

> É o padrão de progresso de vírus: primeiro publicar simplesmente original (Swarm), produzir preocupações em seu nível superior (Agents SDK)

### Swarm vs GroupChat

Ambos usam o roteamento orientado para o LLM, mas diferem em**who picks next**- Não .

> Os dois usam o LLM, mas**谁选择下一个**上不同:

- GrupoChat: um selector (função ou LLM) escolhe o próximo orador de fora.
  中文翻译:GroupChat:选择器(函数或 LLM) de externa seleccionar 下一个发言者──
- O agente atual escolhe o seu sucessor chamando uma ferramenta de transferência.
  O agente está em um processo de seleção de seu reitor.

Swarm é "agente decide o que é o próximo"; GroupChat é "gerente decide o que é o próximo". A decisão de Swarm vive na chamada de ferramenta do agente ativo; GroupChat vive no `GroupChatManager`- Não .

> Swarm é "Agente decide o próximo passo";GroupChat é "administrador decide o próximo passo"。Swarm é a decisão existente na atividade Agente é ferramenta de调用;GroupChat é existente em`GroupChatManager`- Não.

Implicação prática: Swarm é mais fácil de depurar ( Siga as chamadas de ferramentas do agente ativo) mas mais difícil de restringir (qualquer agente pode entregar em qualquer lugar). GroupChat é o oposto: fácil de restringir (a função selector é um lugar para adicionar regras), mais difícil de depurar (a lógica do selector pode ser opaca).

> 实际影响:Swarm 更容易调试(跟踪活动Agente 的工具调用) mas更难约束(quer um Agente pode se comunicar em qualquer lugar) ――GroupChat 相反:容易约束(

## Construí-lo e realizei-o.
```figure
sw-handoff-routing
```

## Construí-lo

`code/main.py`Implementa o Swarm desde o zero: uma classe de dados do agente, um mecanismo de transferência (outil retorna o agente) e um loop de execução que detecta os switches do agente.

> `code/main.py`Desde o início da realização Swarm:Agente dados tipos  mecanismo de comunicação  ferramentas de devolução Agente) e inspecção Agente  ciclo de funcionamento de troca 

Demo: um agente de triagem rotas para reembolso, vendas ou especialistas de suporte. Cada especialista tem suas próprias ferramentas.

> 演示:分诊 Agent 路由到退款、销售或支持专家── cada especialista tem seus próprios instrumentos──运行循环印每次交接──

- Correr .

```
python3 code/main.py
```

## Use-o com o framework implementado.

`outputs/skill-handoff-designer.md`Designa uma topologia de transferência para uma determinada tarefa: quais agentes existem, quais transferências podem ser chamadas, quais transferiam o contexto.

> `outputs/skill-handoff-designer.md`Para determinar a tarefa de design de ligação: quais agentes existem, podem ser utilizados para a ligação, o que é transmitido.

## Envia-o . Produto .

Lista de verificação:

> 检查清单:

- **Handoff logging.**Cada transferência escreve um evento de rastreamento com um snapshot de agente para agente, contexto.
  Tradução:**交接日志。**Cada contacto é um evento de acompanhamento, que inclui um agente para um agente.
- **Context transfer rules.**Decida o que se move na transferência: histórico completo (caros), últimas N mensagens, ou um resumo.
  Tradução:**上下文传输规则。**Decide quando comunicar: completa história (preço) 、 última N 条消息或摘要──
- **Guardrail on handoff.**Uma entrega a um especialista com diferentes permissões de ferramenta deve ser autenticada  caso contrário, a injecção imediata pode forçar a entrega indesejada.
  Tradução:**交接防护栏。**                                                                                                                                                                                                                                                              
- **Loop detection.**Dois agentes que se entregam é uma falha comum; detecta com uma simples verificação de anel de última K.
  Tradução:**循环检测。**Os dois agentes voltaram a entrar em contato com os outros.
- **Fallback agent.**Se não existir um alvo de transferência, volte a um padrão seguro.
  Tradução:**后备 Agent。**Se o objetivo de ligação não existir, retornar ao valor de segurança embutido.

## Exercícios.

1. Corra .`code/main.py`Confirme que o agente ativo da segunda volta é o reembolso.
   Tradução: 运行`code/main.py`,分诊到退款代理──确认第二轮活动代理是退款──
2. Adicione uma regra de detecção de circuito: se os mesmos dois agentes tiverem dado 3 vezes seguidas, forçar uma saída.
   Tradução do inglês: Additional loop test rules: Se os mesmos dois agentes continuam a fazer contacto 3 vezes, forçar a retirada.
3. Leia os documentos do OpenAI Agents SDK sobre filtros de entrega. Implemente uma versão "summarise-on-handoff": o agente de saída comprime o contexto para um resumo de bala antes que o agente de entrada assuma.
   Tradução do original: Translação do original: Translação do original: Translação do original: Translação do original: Translação do original: Translação do original: Translação do original: Translação do original: Translação do original: Translação do original: Translação do original: Translação do original: Translação do original: Translação do original: Translação do original: Translação do original: Translação do original: Translação do original: Translação do original: Translação do original: Translação do original: Translação do original: Translação do original: Translação do original: Translação do original: Translação do original: Translação do original: Translação do original: Translação do original: Translação do original: Translação do original: Translação do original: Translação do original: Translação do original: Translação do original: Translação do original: Translação do original: Translação do original: Translação do original: Translação do original: Translação do original: Translação do original: Translação do original: Translação do original: Translação do original: Translação do original: Translação do original: Translação do original: Translação do original: Translação do original: Translação do original: Translação do original: Translação do original: Translação de um segundo.
4. Compare a transferência do Swarm com um selector do GroupChatManager.
   中文翻译:比较 Swarm 交接与 GroupChatManager 选择器──哪种模式使提示注入更糟糕,为什么?
5. Leia o livro de cozinha do Swarm. Identifique uma decisão explícita de design que o Swarm faz que o SDK OpenAI Agents seja alterado ou mantido.
   O Swarm fez uma decisão de design definida, OpenAI Agents SDK  alterou ou manteve-a.

## Termos-chave .

| Term | What people say | What it actually means |
|------|----------------|------------------------|
| Routine / 例程 | "The agent prompt" / "Agent 提示" | System prompt + tool list. Defines role and available handoffs. / 系统提示 + 工具列表。定义角色和可用交接。 |
| Handoff / 交接 | "Transfer to another agent" / "转移到另一个 Agent" | A tool the active agent can call that returns a new Agent. The runtime switches active agent. / 活动 Agent 可以调用的工具，返回新 Agent。运行时切换活动 Agent。 |
| Stateless / 无状态 | "No memory between runs" / "运行间无记忆" | Swarm does not persist anything; memory is the caller's responsibility. / Swarm 不持久化任何东西；内存是调用者的责任。 |
| Active agent / 活动 Agent | "Who's speaking now" / "现在谁在说话" | The agent currently holding the conversation. Handoff changes this. / 当前持有对话的 Agent。交接改变这个。 |
| Context transfer / 上下文传输 | "What moves on handoff" / "交接时传输什么" | Policy for what history the incoming agent sees: full, last N, or summarized. / 传入 Agent 看到什么历史的策略：完整、最后 N 条或摘要。 |
| Handoff loop / 交接循环 | "Agents ping-pong" / "Agent 乒乓" | Failure mode where two agents keep handing back to each other. / 两个 Agent 持续互相交接的失败模式。 |
| OpenAI Agents SDK | "Production Swarm" / "生产 Swarm" | March 2025 successor; adds sessions, guardrails, tracing on top of the handoff primitive. / 2025 年 3 月继任者；在交接原语之上添加会话、防护栏、追踪。 |
| Handoff filter / 交接过滤器 | "Gate on transfer" / "传输门" | SDK feature to inspect and modify context at the handoff boundary. / 在交接边界检查和修改上下文的 SDK 特性。 |

## Mais leitura 延伸阅读

- [OpenAI cookbook — Orchestrating Agents: Routines and Handoffs](https://developers.openai.com/cookbook/examples/orchestrating_agents) a articulação de referência
  Tradução do idioma: OpenAI 手册  编排 Agente:例程和交接  参考阐述
- [OpenAI Swarm repo](https://github.com/openai/swarm) implementação original, mantida como referência conceitual
  中文翻译:OpenAI Swarm 仓库  原始实现,保留为概念参考
- [OpenAI Agents SDK docs](https://openai.github.io/openai-agents-python/) Sucessor de produção com sessões e rastreamento
  中文翻译:OpenAI Agents SDK 文档  带会话和追踪的生产继任者
- [Anthropic handoff-in-Claude notes](https://docs.anthropic.com/en/docs/claude-code) como os subagentes do código Claude usam um padrão de transferência através de`Task`
  Tradução do idioma: Antropic Claude 中中的交接说明  Claude Code 子 Agente 如何通过 `Task`Usar um modo similar de comunicação
