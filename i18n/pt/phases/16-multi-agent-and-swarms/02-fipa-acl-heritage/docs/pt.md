# Património da FIPA-ACL e de Acto de Discursão .

> Antes da MCP, antes da A2A, havia a FIPA-ACL. Em 2000, a Fundação IEEE para Agentes Físicos Inteligentes ratificou uma linguagem de comunicação de agentes com vinte performativos, duas linguagens de conteúdo e um conjunto de protocolos de interação  contrato net, assinar/notificar, solicitação-quando. Ele desapareceu da indústria porque a carga de ontologia era muito pesada para a web, mas o revival do LLM de sistemas multi-agente está silenciosamente reimplementando as mesmas ideias sem a semântica formal: os contratos JSON representam os performativos, a linguagem natural representa as ontologias. Esta lição leva a sério a FIPA-ACL para que você possa ver quais decisões do protocolo 2026 são reinvenções, que são novidades, e onde a onda atual vai redescobrir problemas já resolvidos na década de 2000.

> **【中文解读】**Este curso fala sobre o FIPA-ACL  Eredit多 系统通信协议的历史标准与现代发展──2000年定型的二十个施事行为 (performance) 内容语言和交互协议, é precisamente o que estão sendo reinventados em 2026 pelos MCP/A2A/ACP: JSON 契约替换施事行为,自然语言替换本体── compreender esta história, você pode perceber quais são as novas inovações.

> **【拓展：FIPA ACL 遗产→具体应用】**FIPA ACL (Fundação para Agentes Físicos Inteligentes Língua de Comunicação de Agentes) é um sistema de comunicação de 1990-2000 anos. Embora a FIPA tenha se dissolvido em 2013, sua ideia central (standardised communication origin languages such as INFORM, REQUEST, PROPOSE) ainda afeta o protocolo de Agentes Inteligentes.

> - Não .**【前置】**O curso de aprendizagem é um curso de história para entender o ACL para entender o acordo de 2026.

> - Não .**【类比】**FIPA-ACL = "AI 界的拉丁语"── 2000 anos de padrão,2026 anos de acordo(MCP/A2A) muito reiterado seu pensamento──区别:FIPA 用形式化本体(重)、现代协议用 JSON+自然语言(轻)──学历史的价值:避免重复覆FIPA 因为"本体太重"而死,现代协议要保持轻量──

**Type:** Learn | **类型:** 学习
**Languages:** Python (stdlib) | **语言:** Python（标准库）
**Prerequisites:** Phase 16 · 01 (Why Multi-Agent) | **前置知识:** Phase 16 · 01（为什么需要多 Agent）
**Time:** ~60 minutes | **时间:** 约 60 分钟

## Problema Introdução

> **【中文解读】**O acordo de 2026 parece estar em plena evolução, praticamente em todo o mundo.

O cenário do protocolo de agentes para 2026 está ocupado: MCP para ferramentas, A2A para agentes, ACP para auditoria empresarial, ANP para confiança descentralizada, NLIP para conteúdo em língua natural, além de CA-MCP e duas dúzias de propostas de investigação.

> O MCP utiliza ferramentas, A2A utiliza agentes, AACP utiliza auditoria empresarial, ANP utiliza descentralização de confiança, NLP utiliza conteúdo de linguagem natural, além de CA-MCP e mais de vinte propostas de pesquisa.

A leitura honesta é que a maioria deles está redescobrindo uma árvore de decisão muito específica de vinte anos. A teoria do discurso-ato de Austin (1962) e Searle (1969) nos deu "expresões são ações". A FIPA-ACL (ratificada em 2000) produziu a normalização de referência: vinte performativos, linguagens de conteúdo SL0/SL1, protocolos de interação para a rede de contratos e subscrição-notificação. JADE e JACK foram as plataformas de referência Java. O esforço desvaneceu-se em torno de 2010 porque a ontologia sobrecarga era muito pesada e a web estava ganhando.

> A teoria do comportamento de palavras de Austin (1962) e Searle (1969) nos diz que "话语即行动" (话语即行动). KQML (KQML) 1993), será transformado em linha de acordo.

Quando olhamos para o MCPs`tools/call`O processo de criação de um novo sistema de gestão de dados é um processo de desenvolvimento de dados que permite a criação de um novo sistema de gestão de dados, que permite a criação de um novo sistema de gestão de dados, que permite a criação de um novo sistema de gestão de dados, que permite a criação de novos sistemas de gestão de dados, que permite a criação de novos sistemas de gestão de dados, que permitem a criação de novos sistemas de gestão de dados, que permitem a criação de novos sistemas de gestão de dados, que permitem a criação de novos sistemas de gestão de dados, que permitem a criação de novos sistemas de gestão de dados, que permitem a criação de novos sistemas de gestão de dados, que permitem a criação de novos sistemas de gestão de dados, que permitem a criação de novos sistemas de gestão de dados, que permitam a criação de novas tecnologias de gestão de dados e que permitem a criação de novas tecnologias de gestão de dados.

> Quando você revisar MCP `tools/call`Quando você vê o ciclo de vida de missões do A2A ou o CA-MCP, você vê uma retrospectiva mais suave da decisão da FIPA, JSON.

## Conceptos básicos

> **【中文解读】**本节把谱系讲全:言语行为理论(Austin/Searle)→ KQML(1993)→ FIPA-ACL(2000,二十个施事行为 + SL0/SL1 内容语言 + 交互协议)→ JADE/JACK 平台 → 衰落 → LLM 时代以 JSON 语法复活──核心洞察:Agen 通信的语法表示小而稳定,只有方式在变──

### Acto de discurso, num parágrafo

> **【中文解读】**Searle colocou-as em cinco categorias; KQML colocou esse conceito filosófico em um protocolo de linha de software executável; FIPA-ACL 收尾标准化;; todos os protocoles de agentes modernos são a última geração dessa cadeia;;

Austin notou que algumas frases não descrevem o mundo, mas o mudam. "Prometho". "Pedito". "Declaro". Ele chamou estas declarações performativas. Searle formalizou cinco categorias: assertivo, diretivo, comissório, expressivo e declarativo. A KQML (Finin et al., 1993) tornou operacional para agentes de software: uma mensagem é um performativo (a ação) mais conteúdo (o que a ação é sobre). A FIPA-ACL limpou as lacunas da KQML e padronizou cerca de vinte performativos.

> Austin observou que algumas frases não descrevem o mundo, que mudam o mundo. "Eu prometo que isso vai acontecer. Eu solicito que isso aconteça. Eu proclamo que isso aconteça. Searle classificou isso em cinco categorias: afirmações, instruções, promessas, declarações, declarações, KQML.

### Os vinte performativos da FIPA (lista parcial)

| Performative | Intent |
|---|---|
| `inform` | "I tell you P is true" |
| `request` | "I ask you to do X" |
| `query-if` | "Is P true?" |
| `query-ref` | "What is the value of X?" |
| `propose` | "I propose we do X" |
| `accept-proposal` | "I accept the proposal" |
| `reject-proposal` | "I reject the proposal" |
| `agree` | "I agree to do X" |
| `refuse` | "I refuse to do X" |
| `confirm` | "I confirm P is true" |
| `disconfirm` | "I deny P" |
| `not-understood` | "Your message did not parse" |
| `cancel` | "Cancel the ongoing X" |
| `cfp` | "Call for proposals on X" |
| `subscribe` | "Notify me when X changes" |
| `failure` | "I tried X and failed" |

A lista completa está aqui .`fipa00037.pdf`O ponto não é memorizá-lo. O ponto é que cada um deles corresponde a um protocolo primitivo que um LLM eventualmente adiciona novamente.

> Lista completa`fipa00037.pdf`(FIPA ACL 消息结构) 中── Emfocado não é na memória, mas em cada um de nós em relação a um acordo LLM 最终会重新添加原语──

### Mensagem canónica FIPA-ACL

> **【中文解读】**Só há sete títulos, mais um.`content`- Não, não.`conversation-id`和 `reply-with`É um requisito-resposta a coisas que o sistema moderno de mudanças continua a reinventar; sem elas, não é possível fazer a troca de rotas.

```
(inform
  :sender       agent1@platform
  :receiver     agent2@platform
  :content      "((price IBM 83))"
  :language     SL0
  :ontology     finance
  :protocol     fipa-request
  :conversation-id   conv-42
  :reply-with   msg-17
)
```

Sete campos contêm o envelope do protocolo; um campo (`content`O resto dos campos são exatamente o que você reinventa cada vez que você conecta retries, threading e ontologia em um protocolo JSON.

> 七个字段承载协议信封;一个字段(`content`O restante é o que você vai reinventar cada vez que você re-essaja, o fio e o corpo adicionados ao protocolo JSON.

### As duas plataformas legais

**JADE**(Java Agent DEvelopment framework, 19992020s) foi o tempo de execução mais usado de conformidade com a FIPA. Agentes estenderam uma classe base, trocaram mensagens ACL, executaram dentro de contentores e coordenaram usando "comportamentos".

> **JADE**(Java Agent 开发框架, 1999-2020 年代) é o mais comum FIPA 兼容运行时.

**JACK**(Software orientado para agentes, comercial) enfatizou o raciocínio BDI (Crédito-Desejo-Intenção) em cima das mensagens FIPA.

> **JACK**(Software orientado para agentes, produtos comerciais) enfatizar em FIPA 消息之上 BDI (confiança-a-vida-intenção)

Ambos diminuíram quando a pilha de web comeu casos de uso de multi-agentes. MCP e A2A são os "containers" de tempo de execução de 2026.

> Uma vez que a Web 技术 absorveu vários agentes, por exemplo, ambos se desmoronaram. MCP e A2A são "containers" de 2026 em funcionamento.

### Por que a FIPA desapareceu

- **Ontology overhead.**A FIPA exigia uma ontologia compartilhada para análise `content`Concordar em ontologias é um processo de padrões de anos. A web acabou de usar HTTP + JSON.
  Tradução:**本体开销。**FIPA  precisa de partilha `content`                                                                                                                                                                                                                                                              
- **Formal semantics nobody used.**SL (Linguagem Semântica) deu condições rigorosas de verdade, mas a maioria dos sistemas de produção usava conteúdo de forma livre e ignorava o formalismo.
  Tradução:**没人用的形式语义。**SL (语义语言) fornece condições de valor real rigorosas, mas a maioria dos sistemas de produção usa o conteúdo em formato livre e ignora o formalismo.
- **Tooling lock-in.**O JADE era apenas para Java, o JACK era comercial.
  Tradução:**工具锁定。**JADE 仅支持Java;JACK 是商业的多语言团队绕过了两者──
- **The internet won the stack.**REST, depois JSON-RPC, então gRPC substituído transporte de ACL.
  Tradução:**互联网赢得了技术栈。**REST, então JSON-RPC, então gRPC substituiu a transmissão ACL.

### O revival do LLM é FIPA-lite

> **【中文解读】**" " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " "`request`E MCP `tools/call`Não há nenhuma definição de um sistema de dados que possa ser usado para identificar os dados de dados de um grupo de dados de um grupo de dados de um grupo de dados de um grupo de dados de um grupo de dados de um grupo de dados de um grupo de dados de um grupo de dados de um grupo de dados de um grupo de dados de um grupo de dados de um grupo de dados de um grupo de dados de um grupo de dados de um grupo de dados de dados de um grupo de dados de um grupo de dados de dados de um grupo de dados de dados de um grupo de dados de dados de um grupo de dados de dados de um grupo de dados de dados de um grupo de dados de dados de um grupo de dados de dados de um grupo de dados de dados de um grupo de dados de dados de um grupo de dados de dados de um grupo de dados de dados de um grupo de dados de dados de um grupo de dados de dados de um grupo de dados de dados de um grupo de dados de dados de um grupo de dados de dados de um grupo de dados de dados de dados de um grupo de dados de dados de dados de um grupo de dados de dados de dados de dados de um grupo de dados de dados de dados de dados de dados de um grupo de dados de dados de dados de dados de dados de dados de dados de um grupo de dados de dados de dados de dados de dados de dados de dados de dados de um grupo de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de um grupo de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados

Comparar uma FIPA `request`para um MCP `tools/call`- Não .

> O FIPA `request`Com o MCP`tools/call` fazer comparação:

```
(request                                {
  :sender  agent1                         "jsonrpc": "2.0",
  :receiver tool-server                   "method":  "tools/call",
  :content "(lookup stock IBM)"           "params":  {"name":"lookup_stock",
  :ontology finance                                   "arguments":{"symbol":"IBM"}},
  :conversation-id c42                    "id": 42
)                                        }
```

O mesmo envelope, sintaxe diferente. Ambos carregam: quem, quem, intenção, carga útil, correlação id. Nem é uma revolução sobre o outro  eles são diferentes trade-offs no mesmo projeto.

> As duas são diferentes: quem, contra quem, intenção, carga válida, ID associada.

A pesquisa de 2025 de Liu et al. ("A Survey of Agent Interoperability Protocols: MCP, ACP, A2A, ANP", arXiv:2505.02279) torna esta linhagem explícita: MCP corresponde a atos de fala de uso de ferramentas, A2A a atos de fala de agente-peer, ACP a atos de fala de auditoria-trail, ANP a extensões de identidade descentralizada. As novas especificações são descendentes do ACL com sintaxe JSON e semântica mais solta.

> Liu 等人 2025 综述("Agent 互操作性协议综述:MCP, ACP, A2A, ANP",arXiv:2505.02279) claramente aponta esta parêntesis:MCP para lidar com ferramentas de uso de palavras, A2A para lidar com agentes para outros comportamentos de palavras, ACP para lidar com auditoria de tráfego de palavras, ANP para lidar com descentralização de identidade,

### A compensação, claramente declarada

> **【中文解读】**权衡要明说:FIPA 给形式语义(可证明) 规范施事行为目录(不用重辩) 带正确性保证的交互协议模式;现代规范给 JSON 原生载荷、自然语言内容、Web 传输、能力发现──交换的就是"更松散的意图语义换更容易实现"──

**What FIPA gave you and modern specs drop:**

> **FIPA 给你的而现代规范丢弃的：**

- Semântica formal  você pode provar `inform`implica que o remetente acredita no conteúdo.
  Tradução do inglês: forma语义你可以证明`inform`Significa que o enviador acredita no conteúdo.
- Um catálogo canônico de performativos  não é preciso re-argumentar "deveríamos ter um `cancel`" ? "
  Não há necessidade de discutir novamente.`cancel`- Não, não.
- Décadas de padrões de interação-protocolo  contrato-rede, assinar-notificar, propor-aceitar  com propriedades de corretão conhecidas.
  Tradução em chinês: décadas de interação de acordo modelo 合同网、订阅-通知、提议-接受具有已知正确性属性──

**What modern specs give you and FIPA did not:**

> **现代规范给你的而 FIPA 没有的：**

- Cargas úteis nativas JSON compatíveis com todas as ferramentas modernas.
  Tradução do inglês para JSON Original
- Conteúdo em linguagem natural que os LLM possam interpretar sem ontologia codificada à mão.
  Tradução do idioma japonês:LLM pode ser explicado sem código manual.
- Transporte de pilha de web (HTTP, SSE, WebSocket).
  中文翻译:Web 技术传输(HTTP、SSE、WebSocket)
- Descoberta de capacidade através de MCPs em directo `server/discover`E os cartões de agente A2A.
  Tradução do português: 通过实时 MCP `server/discover`E o cartão de agente A2A  Capacidade de detecção 

Semântica de intenções mais flexível para uma implementação mais fácil.

> Mais relaxado, mais fácil, mais fácil, mais fácil, mais fácil, mais fácil, mais fácil, mais fácil, mais fácil, mais fácil, mais fácil, mais fácil, mais fácil, mais fácil, mais fácil, mais fácil, mais fácil, mais fácil, mais fácil, mais fácil, mais fácil, mais fácil, mais fácil, mais fácil, mais fácil, mais fácil, mais fácil, mais fácil, mais fácil, mais fácil, mais fácil, mais fácil, mais fácil, mais fácil, mais fácil, mais fácil, mais fácil, mais fácil, mais fácil, mais fácil, mais fácil, mais fácil, mais fácil, mais fácil, mais fácil, mais fácil, mais fácil, mais fácil, mais fácil, mais fácil, mais fácil, mais fácil, mais fácil, mais fácil, mais fácil, mais fácil, mais fácil, mais fácil, mais fácil, mais mais fácil, mais fácil, mais mais fácil, mais fácil, mais mais fácil, mais mais mais fácil, mais mais mais mais mais fácil, mais mais mais mais, mais mais mais mais, mais mais mais mais, mais mais mais mais mais, mais mais mais mais mais, mais mais mais mais, mais mais mais mais mais, mais mais mais mais mais, mais mais mais mais mais mais, mais mais mais mais mais mais, mais mais mais mais mais mais, mais mais mais mais mais mais mais, mais mais mais mais mais mais mais, mais mais mais mais mais mais mais mais mais, mais mais mais mais mais mais, mais mais mais mais mais mais mais mais mais mais, mais mais mais mais mais mais mais, mais mais mais mais mais mais mais mais, mais mais mais mais mais mais mais mais mais mais mais mais, mais mais mais mais mais mais mais mais, mais mais mais mais mais mais mais mais mais mais mais, mais mais mais mais mais mais, mais mais mais mais mais mais mais mais mais mais mais mais, mais mais mais mais mais mais mais mais mais mais mais, mais mais mais mais mais mais mais mais mais, mais mais mais mais mais mais mais mais mais mais, mais mais mais mais mais mais mais mais mais mais mais, mais mais mais mais mais mais mais mais mais mais mais, mais mais mais mais mais, mais mais mais mais mais mais mais mais mais mais mais mais mais mais mais mais mais mais mais, mais mais mais mais mais mais mais mais mais mais mais, mais mais mais mais mais mais mais mais mais mais mais mais, mais mais mais mais mais mais mais mais mais mais mais, mais mais

### Protocolos de interação que valham a pena ser portados

> **【中文解读】**FIPA 约15 交互协议里,三个值搬进 LLM 多 Agent 系统:合同网:任务市场模式,对应阶段16·16 协商) 订阅/通知 ((每个事件总线) 请求-当(持久工作流引擎的延迟任务,对应阶段16·22) 它们都能干净映射到现代消息队列、HTTP + 轮询或 SSE 流──

A FIPA enviou cerca de 15 protocolos de interação. Três vale a pena levar para os sistemas multi-agente LLM:

> A FIPA lançou cerca de 15 acordos de intercâmbio. Três deles devem ser prolongados até o Mestrado em Gestão de Empresas:

1. **Contract Net Protocol (CNP).**Questões de gerente `cfp`(convocatória de propostas); os licitantes respondem com `propose`• o gerente aceita/rechaça. Este é o padrão canônico do mercado de tarefas (fase 16 · 16 de negociação).
   Tradução:**合同网协议 (CNP)。**管理者发布 `cfp`(征求提案);投标者用 `propose`响应;管理者接受/拒绝──这是典型任务市场模式(Phase 16 · 16 协商)──
2. **Subscribe/Notify.**Assinador envia `subscribe`; editor envia `inform`É o que acontece em todos os eventos de 2026.
   Tradução:**订阅/通知。**订阅者发送 `subscribe`; editor in tema mudação `inform`É a linha de todos os eventos de 2026.
3. **Request-When.**"Faça X quando a condição Y é válida". Ação retardada com pré-condições. O analógico 2026 é tarefas diferidas em motores de fluxo de trabalho duradouros (Fase 16 · 22 Escalagem de Produção).
   Tradução:**请求-当。**"quando as condições Y 成立时执行 X──"带前置条件的延迟动作──2026 ano similar é a tarefa de atraso no mecanismo de trabalho permanente (Fase 16 · 22 生产扩展) ―

Cada mapa mostra limpa linha de mensagens modernas, pesquisas HTTP + ou streaming SSE.

> Cada um pode ser claramente mapeado para a linha de notícias moderna, HTTP + 轮询 ou SSE 流.

### O que rompe quando você deixa cair a ontologia

> **【中文解读】**O preço de perder o corpo é**语义漂移**O processo de análise de dados é um processo de análise de dados que permite a análise de dados e de dados.`content`上加 JSON Schema、类型化工件(A2A)、信封里显式施事行为──

Sem uma ontologia compartilhada, os agentes deduzem o significado a partir do conteúdo em linguagem natural.**semantic drift**: dois agentes usam a mesma palavra (`"customer"`O requerimento ontológico da FIPA teria rejeitado a mensagem no momento da análise.

> 没有共享本体,Agent de contenidos de linguagem natural 记录在案的2026年失败模式是**语义漂移**Duas pessoas para o mesmo termo.`"customer"`O processo de detecção de dados é um processo de detecção de dados que é feito por um agente de detecção de dados.

Mitigations sem entrar em ontologia completa:

> Não utilizar completamente as medidas de alívio do corpo:

- JSON Schema em `content` rejeita erros estruturais no fio.
  Tradução do português:对 `content`Usar JSON Schema  em transmissão rejeitar erros estruturais.
- Artefactos de tipo (A2A)  rejeita modalidade errada.
  Chinese:                                                                                                                                                                                                                                                              
- O performativo explícito no envelope  torna a intenção inequívoca mesmo quando o conteúdo é linguagem natural.
  O que é que é um comportamento de construção?

### As especificações de 2026, mapeadas para o patrimônio de fala-ato

| Modern spec | FIPA analog | What it keeps | What it drops |
|---|---|---|---|
| MCP `tools/call` | `request` | explicit intent, correlation id | formal semantics, ontology |
| MCP `resources/read` | `query-ref` | explicit intent, correlation id | formal semantics |
| A2A Task lifecycle | contract-net + request-when | async lifecycle, state transitions | formal completeness guarantees |
| A2A streaming events | subscribe/notify | async push | typed-predicate subscription |
| CA-MCP shared context | blackboard (Hayes-Roth 1985) | multi-writer shared memory | logical consistency model |
| NLIP | natural-language content | LLM-native | schema |

Leindo a tabela de cima para baixo, o padrão é: manter a estrutura primitiva, deixar cair o formalismo, deixar LLMs papel sobre a ambigüidade.

> De cima para baixo, o modelo é: manter a estrutura original, abandonar o formalismo, fazer LLM 弥补模糊性.

> **【中文解读】**Uma frase总结全表:2026 规范保留的是结构性原语(显式意图、关联 id、异步生命周期), abandonado é形式主义(形式语义、本体、逻辑一致性), com a capacidade de explicação do LLM para preencher歧义── é uma clara troca de "capacidade de prova de interação barata"──

```figure
sw-contract-net
```

## Construí-lo e realizei-o.

> **【中文解读】**Demonstração de código é uma biblioteca de padrões puros de FIPA-ACL  Traductor:把五条 MCP/A2A 风格消息编码成 FIPA-ACL 再解码回来,并跑一个"一个管理员 + 三投标者"玩具合同网协商――输出并排显示相同消息的2026 JSON 形态和FIPA-ACL 形态和一些协议原语在往返中存活,只有语法不同――

`code/main.py`Implementa um tradutor FIPA-ACL de pure-stdlib. Ele codifica e decodifica o envelope ACL canônico e mostra como cada forma de mensagem MCP / A2A se reduz aos mesmos sete campos.

> `code/main.py`实现一纯标准库的FIPA-ACL 翻译器──它编解码标准ACL 信封,并展示每个MCP / A2A 消息形状如何简化为相同的七段――演示内容:

- Encode cinco mensagens de estilo MCP e A2A como FIPA-ACL.
  Tradução do inglês para "FIFA-ACL"
- Decodifica a FIPA-ACL para o equivalente moderno.
  O sistema de controle de dados é um sistema de controle de dados de dados.
- Executa um contrato de brinquedo Negociação de rede entre um gerente e três licitantes usando `cfp`- Não .`propose`- Não .`accept-proposal`- Não .`reject-proposal`- Não .
  Tradução:`cfp`- Não.`propose`- Não.`accept-proposal`- Não.`reject-proposal`Entre um administrador e três proponentes, é executado um acordo de negociação.

- Correr .

```
python3 code/main.py
```

A saída é um rastro lado a lado mostrando cada mensagem moderna em sua forma JSON 2026 e sua forma FIPA-ACL, em seguida, uma viagem de ida e volta de uma oferta de rede de contrato. Os mesmos protocolos primitivos sobrevivem à viagem de ida e volta; apenas a sintaxe difere.

> 输出是一个并排追踪,显示每条现代消息的 2026 JSON 形式和 FIPA-ACL 形式,然后是合同网投标标的往返──同样的协议原语在往返中存活;只有语法不同──

## Use-o com o framework implementado.

`outputs/skill-fipa-mapper.md`É uma habilidade que lê qualquer especificação do protocolo de agente e produz o mapeamento FIPA-ACL.`inform`com a sintaxe JSON?"

> `outputs/skill-fipa-mapper.md`É uma habilidade, ler qualquer Agente 协议规范并生成 FIPA-ACL 映射.`inform`"O que é isso?

## Envia-o . Produto .

> **【中文解读】**Não ressuscitar FIPA-ACL, para trazer de volta sua lista de verificação:意图原语、关联 id、显式内容语言、一等公民的交互协议、语义漂移预案── qualquer novo protocolo na produção, primeiro responder a estas cinco questões──

Não traga a FIPA-ACL de volta.

> Não traga o FIPA-ACL para cá. Traga-o para cá.

- Qual é a intenção primitiva (performativa) de cada mensagem?
  Tradução do inglês para "qualquer coisa que você quer fazer"
- Existe uma identificação de correlação para a resposta-requisito e cancelamento?
  Tradução do inglês: Is there a relevant ID for request-responding and cancel?
- Existe uma linguagem de conteúdo explícito (JSON-RPC, texto simples, artefato de tipo estruturado)?
  中文翻译: há algum tipo de material em linguagem JSON-RPC?
- Os protocolos de interação são de primeira classe, ou estão a reimplementar a rede de contratos a partir do zero?
  O protocolo de intercâmbio é um cidadão igual, ou você está começando a re-implementar o contrato?
- O que acontece quando dois agentes discordam sobre o significado do conteúdo (drift semântico)?
  Quando dois agentes têm diferenças no conteúdo, o que acontece?

Documentar estas cinco perguntas para qualquer novo protocolo antes de enviá-lo para produção.

> Antes de publicar qualquer novo protocolo até ao ambiente de produção, registem estas cinco questões.

## Exercícios.

1. Corra .`code/main.py`- Observar a codificação de ida e volta. Identificar qual o performativo da FIPA corresponde `tools/call`- Não .`resources/read`, e criação de tarefas A2A.
   Tradução: 运行`code/main.py` observar os dados e os dados.`tools/call`- Não.`resources/read`E A2A 任务创建――
2. Extender a demonstração da rede de contratos com um `cancel`O que é que o gerente faz quando o problema é que o gerente não consegue fazer a tarefa?`cancel`Resolver essa retemporada sozinho não?
   Tradução:`cancel`施事行为扩展合同网演示, permitir que os administradores possam retirar as tarefas no meio do concurso.`cancel`Resolveu o que falhou que não podia ser resolvido apenas por tentar novamente?
3. Leia a estrutura de mensagens da FIPA ACL (http://www.fipa.org/specs/fipa00037/) secções 4.14.3. Escolha um performativo não abrangido nesta lição e descreva o seu analogo JSON-RPC moderno.
   中文翻译:阅读 FIPA ACL 消息结构(http://www.fipa.org/specs/fipa00037/）第4.1-4.3 节──选择本课未涵盖的一个施事行为并描述其现代 JSON-RPC类比──
4. Leia Liu et al., arXiv:2505.02279. Para cada um dos MCP, A2A, ACP, ANP, lista as famílias performativas FIPA que eles mantêm e deixam.
   Para cada um dos MCP, A2A, ACP, ANP, lista os seus conservados e abandonados FIPA 施事行为族──
5. Desenhar um JSON-Schema mínimo para o `content`campo de uma `request`O que é que esse esquema dá que a linguagem natural pura não dá e quanto custa?
   Tradução do português:`request`施事行为                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                          `content`字段设计一个最小的JSON-Schema―― esse modelo lhe fornece uma linguagem pura natural sem nada, o que é o custo?

## Termos-chave .

| Term | What people say | What it actually means | 中文术语 |
|------|----------------|------------------------|----------|
| Speech act | "An utterance that does something" | Austin/Searle: utterances as actions. The theoretical parent of ACL. | 言语行为 |
| FIPA | "That old XML thing" | IEEE Foundation for Intelligent Physical Agents. Standardized ACL in 2000. | FIPA 基金会 |
| ACL | "Agent Communication Language" | FIPA's envelope format: performative + content + metadata. | Agent 通信语言 |
| Performative | "The verb" | The intent class of a message: `inform`, `request`, `propose`, `cfp`, etc. | 施事行为 |
| KQML | "FIPA's predecessor" | Knowledge Query and Manipulation Language (1993). Simpler, narrower. | KQML |
| Ontology | "Shared vocabulary" | A formal definition of the concepts the content language talks about. | 本体 |
| SL0 / SL1 | "FIPA content languages" | Semantic Language levels 0 and 1 — the formal content language family. | SL 内容语言 |
| Contract Net | "Task market" | Manager issues cfp; bidders propose; manager accepts. The canonical interaction protocol. | 合同网 |
| Interaction protocol | "Pattern of messages" | A sequence of performatives with known correctness: request-when, subscribe-notify, etc. | 交互协议 |

## Mais leitura 延伸阅读

- [Liu et al. — A Survey of Agent Interoperability Protocols: MCP, ACP, A2A, ANP](https://arxiv.org/html/2505.02279v1) a pesquisa canónica de 2025 que liga as especificações modernas ao património da FIPA
  中文翻译:Liu 等人Agen 互操作性协议综述,连接现代规范与FIPA 遗产的权威 2025 综述
- [FIPA ACL Message Structure Specification (fipa00037)](http://www.fipa.org/specs/fipa00037/) o formato do envelope de 2000 ratificado
  Tradução do inglês:FIPA ACL 消息结构规范2000年批准的信封格式
- [FIPA Communicative Act Library Specification (fipa00037)](http://www.fipa.org/specs/fipa00037/) o catálogo completo de desempenho
  Tradução do inglês para tradução do inglês: FIPA 通信行为库规范完整的施事行为目录
- [MCP specification 2026-07-28](https://modelcontextprotocol.io/specification/2026-07-28) o equivalente atual de utilização de ferramentas sem estado de `request`- Não .`query-ref`
  Tradução do Novo Mundo:MCP 2026-07-28 规范`request`- Não .`query-ref`de atual sem estado ferramentas uso eficácia
- [A2A specification](https://a2a-protocol.org/latest/specification/) o equivalente moderno de agente-peer de contrato-net e assinatura-notificação
  Tradução do inglês para o inglês: A2A 规范合同网和订阅-通知的现代代理对等效
