# A2A  O protocolo de agente a agente  A2A: Agente 间通信协议

> O Google anunciou A2A em abril de 2025; em abril de 2026 a especificação está em https://a2a-protocol.org/latest/specification/e 150 organizações apoiam-na. A2A é o complemento horizontal do MCP (Lessão 13): onde o MCP é vertical (agente  ferramentas), A2A é peer-to-peer (agente  agente). Ele define os Cartões de Agente (descoberta), tarefas com artefatos (texto, dados estruturados, vídeo), ciclos de vida de tarefas opacos e auth. Os sistemas de produção combinam cada vez mais o MCP com o A2A. O Google Cloud lançou o suporte A2A no Vertex AI Agent Builder durante 2025-2026.

> **【中文解读】**O Google em abril de 2025 lançou o A2A  acordo; até abril de 2026, a regulamentação já tem 150+  organização de apoio. A2A é o nível complementar de MCP: MCP é vertical.

> **【拓展：A2A → Google 的 Agent 协议】**A2A é um protocolo de Agente 间通信标准协议, liderado pelo Google, com o MCP do Anthropic (Modelio de Protocolo Contextual) (MCP) e MCP (MCP)  resolver Agente e ferramenta de ligação, A2A  resolver Agente e Agente de colaboração.

**Type:** Learn + Build | **类型:** 学习 + 构建
**Languages:** Python (stdlib, `http.server`, `json`) | **语言:** Python (标准库, `http.server`, `json`)
**Prerequisites:** Phase 16 · 04 (Primitive Model) | **前置知识:** Phase 16 · 04 (原语模型)
**Time:** ~75 minutes | **时间:** ~75 分钟

> - Não .**【前置】**学本节前请先掌握:Fase 13·15-20(MCP 协议套件) 、Fase 16·04(原语) ・・・A2A é o nível do MCP:MCP=Agente 调工具(垂直),A2A=Agente 找 Agente(横向) ・・・
> - Não .**【类比】**MCP + A2A = "电话黄页 + 直接通话"──MCP = 工具目录(agent 找工具用);A2A = Agent 间通话协议(agent 找 agent 协作)──2026 生产系统标配:MCP(连工具) + A2A(连其他 Agent) + Agent Card(发现)──Google 主导,150+ 组织支持──

## Problema Introdução

O seu agente precisa chamar outro agente em outro sistema. Como? Você pode expor um endpoint HTTP, definir um esquema JSON personalizado, e esperar que o outro lado fale. Cada par de agentes se torna uma integração personalizada.

> Você pode expor um ponto final HTTP, definir um padrão JSON personalizado, e esperar que o outro lado possa entendê-lo.

O problema de integração N-quadrado: com N agentes, você precisa de N × 1) / 2 integrações personalizadas. Com 10 agentes, isso é 45 integrações. Com 100 agentes, 4950. A2A desintegra isso para N Agente Cartões, cada descrevendo um agente.

> N 平方集成問題:N 个代理 需要 N×(N-1)/2 个定制集成──10 个代理 是 45 个集成──100 个代理 是 4950 个──A2A reduzir para N 个代理卡片, cada descrição de um agente──

A2A é o protocolo universal para essa chamada. Descoberta padrão, modelo de tarefa padrão, transporte padrão, artefatos padrão.

> A2A é um protocolo de linha geral que deve ser usado.

A abstração chave: os agentes são endpoints de rede end-respeitáveis e descobre-se. Você não "importa" um agente; você "chamá-lo".

> 关键抽象:Agent é可寻址、可发现的网络端点──你不"导入"Agent;你"调用"它──这解已部署Agent 运行在任何地方、使用任何语言、使用任何框架,只要它说 A2A──

## Conceptos básicos

### Os quatro elementos

> Quatro elementos

**Agent Card.**Um documento JSON em `/.well-known/agent.json`A descrição do agente: nome, competências, pontos finais, modalidades suportadas, requisitos de autor.

> **Agent 卡片。**                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             `/.well-known/agent.json`O JSON 文档,描述 Agent:名称、技能、端点、支持的模态、认证要求──通过读取卡进行发现──

A convenção URL conhecida reflete os padrões da web (`/.well-known/`é o mesmo caminho usado para `robots.txt`Qualquer agente compatível com A2A pode ser descoberto através da obtenção desse URL.

> Conheça o URL 约定镜像 Web 标准(`/.well-known/`É utilizado`robots.txt`、ACME 挑战、OIDC 发现的相同路径) ∼ Qualquer agente A2A 兼容 都可通过获取该URL 发现──不需要注册表、代理或中央目录──

**Task.**Uma unidade de trabalho, um objeto sincronizado, com um ciclo de vida:`submitted -> working -> completed / failed / canceled`Um cliente envia uma tarefa, pesquisas ou subscreve para atualizações.

> **任务。**工作单元── objetos com um estado de vida diferente:`submitted -> working -> completed / failed / canceled` O cliente deve enviar tarefas, consultas ou subscrições.

**Artifact.**O tipo de resultado produzido por uma tarefa. texto, JSON estruturado, imagem, vídeo, áudio. Artefatos são digitalizados para que diferentes modalidades sejam de primeira classe.

> **工件。**O resultado da tarefa é o tipo de trabalho.

**Opaque lifecycle.**A A2A não prescreve *como* o agente remoto resolve a tarefa. O cliente vê transições de estado e artefatos; a implementação é livre de usar qualquer framework.

> **不透明生命周期。**A2A 不规定远程 Agent *如何* 解决任务──客户端看状态转换和工件;实现可以自由使用任何框架──

Esta opacidade é por design. Um agente remoto construído em LangGraph, CrewAI ou um script Python personalizado todos parecem idênticos ao cliente A2A. Interoperabilidade vem de concordar no formato de fio, não os internos.

> Esta forma de transparência é concebida assim. Baseado em LangGraph, CrewAI ou Python, o agente remoto construído para o cliente A2A parece ser o mesmo.

### A divisão MCP/A2A

- **MCP**(Lessão 13): ferramenta de agente <->. O agente lê/escreve através de JSON-RPC para um servidor de ferramentas.
  Tradução:**MCP**(Lessão 13):Agente <-> 工具──Agente 通过 JSON-RPC 读写工具服务器──默认无状态──
- **A2A**O protocolo de par; ambas as partes são agentes com o seu próprio raciocínio.
  Tradução:**A2A**Agente: Agente: Agente: Agente: Agente: Agente: Agente: Agente: Agente: Agente: Agente: Agente: Agente: Agente: Agente: Agente: Agente: Agente: Agente: Agente: Agente: Agente: Agente: Agente: Agente: Agente: Agente: Agente: Agente: Agente: Agente: Agente: Agente: Agente: Agente: Agente: Agente: Agente: Agente: Agente: Agente: Agente: Agente: Agente: Agente: Agente: Agente: Agente: Agente: Agente: Agente: Agente: Agente: Agente: Agente: Agente: Agente: Agente: Agente: Agente: Agente: Agente: Agente: Agente: Agente: Agente: Agente: Agente: Agente: Agente: Agente: Agente: Agente: Agente: Agente: Agente: Agente: Agente: Agente: Agente: Agente: Agente: Agente: Agente: Agente: Agente: Agente: Agente: Agente: Agente: Agente: Agente: Agente: Agente: Agente: Agente: Agente: Agente: Agente: Agente: Agente: Agente: Agente: Agente: Agente: Agente: Agente: Agente: Agente: Agente: Agente: Agente: Agente: Agente: Agente: Agente: Agente: Agente: Agente: Agente: Agente: Agente: Agente: Agente: Agente: Agente: Agente: Agente: Agente: Agente: Agente: Agente: Agente: Agente: Agente: Agente: Agente: Agente: Agente: Agente: Agente: Agente: Agente: Agente: Agente: Agente: Agente: Agente: Agente: Agente: Agente: Agente: Agente: Agente: Agente: Agente: Agente: Agente: Agente: Agente: Agente: Agente: Agente: Agente: Agente: Agente: Agente: Agente: Agente: Agente:

Os sistemas de produção multi-agentes usam ambos. Um par A2A chama ferramentas MCP de seu lado. A divisão mantém as duas preocupações limpas.

> O sistema de produção de agentes múltiplos é utilizado por ambos os tipos de A2A.

Um padrão comum: um "agente de pesquisa" A2A na empresa A chama um servidor de ferramenta de pesquisa MCP internamente, e depois retorna suas descobertas a um "agente de análise" A2A na empresa B. A comunicação transorg é A2A; o uso interno de ferramentas é MCP. Cada protocolo faz o que é melhor.

> 常见模式: A2A "Agenta de estudo" da empresa A internaliza MCP 搜索工具服务器, então será encontrado de volta para A2A "Agenta de análise" da empresa B.

Ou com streaming: subscrição SSE para `/tasks/{id}/events`Para atualizações de pressão.

> Ou usar 流式:SSE 订阅 `/tasks/{id}/events`获取推送更新──

### Autor

A A2A suporta três padrões comuns:

> A2A 支持三种常见模式:

Os três padrões cobrem o espectro de "Confio no meu provedor de identidade" (portador OAuth2) para "nos verificamos mutuamente" (mTLS) para "não confiamos em terceiros" (assinatura HMAC). Escolha o mais leve que atenda às suas exigências de segurança.

> O modelo abrangerá desde "我信任我的身份提供商" (OAuth2 portador) até " nós nos verificamos uns aos outros " (MTLS) até " nós não confiamos em qualquer terceiro " (HMAC) do âmbito de aplicação.

- **Bearer token** OAuth2 ou opaco.
  Tradução:**Bearer token** OAuth2 或不透明令牌。
- **mTLS** TLS mútuo; organizações provam identidade uns aos outros.
  Tradução:**mTLS** 双向 TLS; organização mutuamente certificando de identidade。
- **Signed requests**HMAC sobre a carga útil.
  Tradução:**签名请求** para HMAC de carga válida

A autoria é declarada no Cartão de Agente; os clientes descobrem e cumprem.

> 认证在代理卡片中声明;客户端发现并遵守──

### 150+ organizações até abril de 2026

A adoção da empresa impulsionou a escala A2A. O título: A2A tornou-se a forma como os sistemas de agentes empresariais cruzaram as fronteiras de confiança. O Google Cloud enviou o suporte Vertex AI Agent Builder A2A; o Microsoft Agent Framework o suporta; a maioria das principais frameworks (LangGraph, CrewAI, AutoGen) enviam adaptadores A2A.

> 企业采用推动了A2A's scalealisation──标题:A2A 成为企业 Agent 系统跨越信任边界的方式──Google Cloud 提供 Vertex AI Agent Builder A2A 支持;Microsoft Agent Framework 支持它;大多数主要框架(LangGraph、CrewAI、AutoGen) fornecer A2A 适配器──

A razão pela qual a A2A ganhou a adoção empresarial onde a FIPA-ACL falhou: A2A é nativo de JSON, usa a infraestrutura web existente (HTTP, SSE, OAuth), e não requer ontologias compartilhadas.

> A2A é a causa do fracasso da FIPA-ACL em empresas: A2A é o JSON original, utiliza a infraestrutura web existente, não precisa de partilha de recursos.

### Onde A2A ganha

- **Cross-organization calls.**Agente da empresa A chama agente da empresa B. Sem A2A, cada par é um contrato feito sob medida.
  Tradução:**跨组织调用。**Empresa A de Agente Empresa B de Agente Não há A2A, cada um é um contrato de confecção.
- **Heterogeneous frameworks.**O agente LangGraph chama o agente CrewAI chama o agente Python personalizado.
  Tradução:**异构框架。**LangGraph Agent 调用 CrewAI Agent 调用自定义 Python Agent──A2A 标准化──
- **Typed artifacts.**Resultado de vídeo, JSON estruturado, áudio  todos de primeira classe.
  Tradução:**类型化工件。**视频结果、结构化 JSON、音频都是一等公民──
- **Long-running tasks.**O ciclo de vida opaco + pesquisas tornam as tarefas de horas simples.
  Tradução:**长时间运行的任务。**O ciclo de vida + rotinação torna as tarefas de classe de horas simples.

### Onde A2A luta

- **Latency-sensitive micro-calls.**O ciclo de vida do A2A é assíncrono. Sub-milissegundos agente-a-agente não se encaixa; usar RPC direto.
  Tradução:**延迟敏感的微调用。**O ciclo de vida do A2A é diferente.
- **Tight-coupled in-process agents.**Se ambos os agentes executarem no mesmo processo Python, a viagem de ida e volta HTTP do A2A é exagerada.
  Tradução:**紧耦合的进程内 Agent。**Se dois Agentes estiverem a funcionar no mesmo processo Python, o HTTP de A2A retornará é exagerado.
- **Small teams.**Os custos gerais das especificações são reais; os agentes internos só podem não precisar da formalidade.
  Tradução:**小团队。**                                                                                                                                                                                                                                                              

### A2A vs ACP, ANP, NLIP

Várias especificações relacionadas surgiram em 2024-2026:

> Entre 2024 e 2026, surgiram várias regras relacionadas:

- **ACP**(IBM/Linux Foundation)  antecessor do A2A, escopo mais estreito.
  Tradução:**ACP**(IBM/Linux Foundation)  A2A's anterior, alcance mais estreito.
- **ANP**(Protocolo de Rede de Agentes)  Peer-discovery-heavy, descentralizado-first.
  Tradução:**ANP**(Protocolo da Rede de Agentes)  重对等发现,去中心化优先
- **NLIP**(Protocolo de Interação da Língua Natural da Ecma, padronizado em dezembro de 2025)  tipo de conteúdo em língua natural.
  Tradução:**NLIP**(Ecma Naturalidade Lingüística de Intercâmbio (2025 12 月 標準化)

A2A é o protocolo de pares mais adotado em abril de 2026. Veja arXiv:2505.02279 (Liu et al., "Um levantamento de protocolos de interoperabilidade de agentes") para comparação.

> 截至 2026 年 4 月,A2A é a adopção mais ampla de acordos de parceria.

A paisagem do protocolo 2026 está estabilizada: A2A para a colaboração com agentes, MCP para ferramentas, ACP absorvido em A2A para a registros de trajetórias, ANP para a identidade transorgânica.

> O protocolo de 2026 já está estabelecido: A2A para Agente 协作, MCP para ferramentas, ACP para absorver A2A para轨迹日志, ANP para跨组织身份──NLIP 仍然小众── nova proposta precisa mostrar uma verdadeira diferença para obter atenção──

## Construí-lo e realizei-o.
```figure
sw-agent-card-discovery
```

## Construí-lo

`code/main.py`implementa um servidor e cliente A2A-minimal usando `http.server`O servidor:

> `code/main.py`Utilização `http.server`E JSON  implementar A2A 最小服务器和客户端──服务器:

- expõe`/.well-known/agent.json`- Não .
  Tradução do português: exposit`/.well-known/agent.json`- Não .
- Aceita .`POST /tasks`- Não .
  Tradução: 接受`POST /tasks`- Não .
- gerencia o estado da tarefa,
  Tradução do inglês:
- Retorna artefatos em `GET /tasks/{id}`- Não .
  Tradução:`GET /tasks/{id}`- Não.

O cliente:

> 客户端:

- - Vai buscar o cartão de agente.
  Tradução do inglês:
- apresenta uma tarefa,
  Tradução do inglês:
- sondagens até à conclusão,
  Tradução do inglês:
- - Ele lê o artefato.
  Tradução do português:

O script inicia o servidor em um fio de fundo, e depois corre o cliente contra ele.

> 脚本在后台线程中启动服务器,然后运行客户端──你看完整流程:发现、提交、轮询、工件── você vê o processo completo: descoberta、 submissão、轮询、工件──

## Use-o com o framework implementado.

`outputs/skill-a2a-integrator.md`Desenha uma integração A2A: conteúdo do Cartão de Agente, esquemas de tarefas, escolha de autor, streaming versus sondagens.

> `outputs/skill-a2a-integrator.md`设计 A2A 集成:Agente 卡片内容、任务模式、认证选择、流式 vs 轮询──

## Envia-o . Produto .

Lista de verificação:

> 检查清单:

- **Pin the spec version.**A2A ainda está a evoluir. O cartão do agente deve declarar a versão do protocolo.
  Tradução:**固定规范版本。**A2A  ainda em desenvolvimento; Agente 卡片应声明协议版本.
- **Idempotent task creation.**As apresentações duplicadas (retestes de rede) devem produzir uma tarefa.
  Tradução:**幂等任务创建。**重复提交 (网络重试) deve surgir uma tarefa.
- **Artifact schemas.**Declare quais são as formas que o agente retorna; os consumidores devem validar.
  Tradução:**工件模式。**声明 Agente 返回什么形状;消费者应验证──
- **Rate limits + auth.**A2A é de uso público; aplica segurança web padrão.
  Tradução:**速率限制 + 认证。**A2A 面向公众; aplicação de normas de segurança da Web.
- **Dead-letter for failed tasks.**Inspeccionar os padrões ao longo do tempo para detectar tipos de falhas recorrentes.
  Tradução:**失败任务死信。**随时检查模式以发现反复出现的失败类型──

## Exercícios.

1. Corra .`code/main.py`Confirme que o cliente descobre o servidor e recebe o artefato correto.
   Tradução: 运行`code/main.py` Confirmar que o cliente encontra o servidor e não recebe as obras corretas.
2. Adicionar uma segunda habilidade ao servidor (por exemplo, "resumir"). Atualizar o Cartão de Agente. Escrever um cliente que escolha a habilidade com base no tipo de tarefa.
   中文翻译:向服务器添加第二个技能(如"summarize")。更新 Agente 卡片──编写根据任务类型选择技能的客户端──
3. Implementar um endpoint de streaming de SSE: `/tasks/{id}/events`O que o cliente precisa fazer de forma diferente?
   中文翻译:实现 SSE 流式端点:`/tasks/{id}/events`O cliente precisa fazer o que é diferente?
4. Leia a especificação A2A. Identifique três coisas que a especificação manda que esta demonstração não implementa.
   Chinese: 阅读 A2A 规范──识别规范要求的三此演示未实现的东西──
5. Compare A2A (Agent Card discovery) com MCP (Listing of Server-side capabilities via `listTools`O que é a compensação entre agentes que se descrevem e testes de capacidade?
   中文翻译:比较 A2A(Agent 卡片发现) com MCP(通过 `listTools`O que é o balanço entre o agente e a capacidade de pesquisa?

## Termos-chave .

| Term | What people say | What it actually means |
|------|----------------|------------------------|
| A2A | "Agent-to-agent" / "Agent 对 Agent" | Peer protocol for agents to call other agents across systems. Google 2025. / Agent 跨系统调用其他 Agent 的对等协议。Google 2025。 |
| Agent Card / Agent 卡片 | "The agent's business card" / "Agent 的名片" | JSON at `/.well-known/agent.json` describing skills, endpoints, auth. / 描述技能、端点、认证的 JSON。 |
| Task / 任务 | "The unit of work" / "工作单元" | Async stateful object with a lifecycle; artifacts produced on completion. / 具有生命周期的异步有状态对象；完成时产生工件。 |
| Artifact / 工件 | "The result" / "结果" | Typed output: text, structured JSON, image, video, audio. First-class media. / 类型化输出：文本、结构化 JSON、图像、视频、音频。一等媒体。 |
| Opaque lifecycle / 不透明生命周期 | "How it's solved is the agent's business" / "如何解决是 Agent 的事" | Client sees state transitions; server is free to choose framework/tools. / 客户端看到状态转换；服务器自由选择框架/工具。 |
| Discovery / 发现 | "Finding the agent" / "找到 Agent" | `GET /.well-known/agent.json` returns the card. / 返回卡片的 GET 请求。 |
| MCP vs A2A | "Tools vs peers" / "工具 vs 对等" | MCP: vertical agent <-> tool. A2A: horizontal agent <-> agent. / MCP：垂直 Agent <-> 工具。A2A：水平 Agent <-> Agent。 |
| ACP / ANP / NLIP | "Sibling protocols" / "兄弟协议" | Adjacent specs; A2A is the most-adopted 2026. / 相邻规范；A2A 是 2026 年采用最广泛的。 |

## Mais leitura 延伸阅读

- [A2A specification](https://a2a-protocol.org/latest/specification/) a especificação canónica
  中文翻译:A2A 规范  权威规范
- [Google Developers Blog — A2A announcement](https://developers.googleblog.com/en/a2a-a-new-era-of-agent-interoperability/) Abril de 2025
  中文翻译:Google 开发者博客  A2A 公告  2025 年 4 月发布文章
- [A2A GitHub repo](https://github.com/a2aproject/A2A) Implementações de referência e KDS
  中文翻译:A2A GitHub 仓库  参考实现和 SDK
- [Liu et al. — A Survey of Agent Interoperability Protocols](https://arxiv.org/html/2505.02279v1) Comparar MCP, ACP, A2A, ANP
  中文翻译:Liu 等人  Agente 互操作性协议综述  MCP、ACP、A2A、ANP 比较
