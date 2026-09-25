# OpenTelemetry GenAI Semantic Conventions 约定 GenAI METR

> O SIG GenAI da OpenTelemetry (lançado em abril de 2024) define o esquema padrão para telemetria de agentes. Os nomes de espaços, atributos e regras de captura de conteúdo convergem entre os fornecedores, de modo que os rastros de agentes significam a mesma coisa em Datadog, Grafana, Jaeger e Honeycomb.

**Type:** Learn + Build | **类型:** 构建
**Languages:** Python (stdlib) | **语言:** Python (标准库)
**Prerequisites:** Phase 14 · 13 (LangGraph), Phase 14 · 24 (Observability Platforms) | **前置知识:** 见原文
**Time:** ~60 minutes | **时间:** 见原文

## Objetivos de aprendizagem

- Nomear as categorias de abrangência da GenAI: modelo/cliente, agente, ferramenta.
- Distinguir`invoke_agent`CLIENT vs INTERNAL e quando cada um se aplica.
- Lista dos atributos de nível superior da GenAI: nome do fornecedor, modelo de solicitação, ID da fonte de dados.
- Explicar o contrato de captura de conteúdo: optar-in, `OTEL_SEMCONV_STABILITY_OPT_IN`, recomendação de referência externa.

## O problema é o problema da introdução

> **【中文解读】**Cada fornecedor desenvolveu seu próprio espaço de tempo, os grupos de desenvolvimento de sistemas de transporte e transporte de energia necessitam de construir um sistema de instrumentos independente para cada quadro.

Cada fornecedor inventa seus próprios nomes de espaço. equipes de operações acabam construindo painéis de controle por quadro.

> Cada fornecedor desenvolveu seu próprio espaço de tempo. A equipe de transporte precisa finalmente construir um painel de instrumentos independente para cada quadro.

> **【拓展：OTel GenAI 规范的跨平台统一】**OpenTelemetry GenAI 语义约定 (2024年4月启动) 定义 Agent 遥测的标准方案:span 名称、属性和内容捕获规则跨供应商统一,使 Agent 追踪在 Datadog、Grafana、Jaeger 和 Honeycomb 中具有相同语义──一次埋点,多后端通用──

> - Não .**【前置】**O que é que é um "Agent Loop" (ou "Agent Loop")? Você precisa de um "Agent" para dar um ponto de enterro; O que é um "Agent Loop" (ou "Agent Loop")?

## O conceito central.

### Categoria de espaços

> - Não .**【类比】**Os três tipos de OTel GenAI 像医院的分级诊疗记录:**Model span**É o que eu faço para fazer isso.**Agent span**É um processo completo de diagnóstico da doença, que inclui várias experiências.**Tool span**É um projeto de inspecção. Cada vez são uma operação independente.`parent_span_id`链回父记录这样 Datadog 里你能展开看: Todo o Agente 调用 → 5 vezes ferramenta 调用 → Cada vez ferramenta 调用里 2 vezes LLM 调用。

1. **Model / client spans.**Cobrir chamadas de LLM crus. emitidas pelos SDKs (Antropic, OpenAI, Bedrock) e adaptadores de modelos frameworks.
2. **Agent spans.** `create_agent`(quando o agente é construído) e `invoke_agent`(quando ele corre).
3. **Tool spans.**Uma por invocação de ferramenta; ligada ao espaço de agente pela relação pai-filho.

### Nomeamento do agente span

- Nome em espanhol: `invoke_agent {gen_ai.agent.name}`se for nomeado; retorno a `invoke_agent`- Não .
- Tipo de espinha:
  - **CLIENT** para serviços de agentes remotos (OpenAI Assistants API, Bedrock Agents).
  - **INTERNAL** para os quadros de agentes em processo (LangChain, CrewAI, local ReAct).

### Atributos-chave

- `gen_ai.provider.name`- Não .`anthropic`- Não .`openai`- Não .`aws.bedrock`- Não .`google.vertex`- Não .
- `gen_ai.request.model` Identificação do modelo.
- `gen_ai.response.model` o modelo resolvido (poderá diferir do pedido devido ao roteamento).
- `gen_ai.agent.name`Identificação do agente.
- `gen_ai.operation.name`- Não .`chat`- Não .`completion`- Não .`invoke_agent`- Não .`tool_call`- Não .
- `gen_ai.data_source.id` para o RAG: qual o corpus ou loja foi consultado.

Existem convenções específicas de tecnologia para Anthropic, Azure AI Inference, AWS Bedrock, OpenAI.

> OpenTelemetry GenAI 语义约定 define LLM 和 Agent's可观测性标准──`gen_ai.request.model`- Não.`gen_ai.usage.input_tokens`- Não.`gen_ai.agent.name`E assim...

### Captura de conteúdo

> ️ **【易错点】**场景: desenvolvedor图省事在 `invoke_agent`span 里把完整提示(含用户 PII、API key、客户合同条款) como atributo 直接塞进去 → 后果:运维在 Jaeger 网页里点开就能看到所有的明文,Datadog ainda irá fazer o índice de busca completa, é igual a colocar o risco de se espalhar por toda a cadeia de observação → 修复:默认关闭内容 capture,需要时只在 span 里存指针 ID(`gen_ai.input.message_id=row42`), original落到带带 ACL 的对象存储 S3 里,运维要查时通过 ID 跳转授权访问──这就是本节反复强调的"recomendação de referência externa"──

A regra padrão: as instrumentações NÃO DEVEM capturar entradas/salidas por padrão.

> OpenTelemetry GenAI 语义约定 define LLM 和 Agent's可观测性标准──`gen_ai.request.model`- Não.`gen_ai.usage.input_tokens`- Não.`gen_ai.agent.name`E assim...

- `gen_ai.system_instructions`
- `gen_ai.input.messages`
- `gen_ai.output.messages`

Padrão de produção recomendado: armazenar conteúdo externamente (S3, a sua loja de log), registar referências em intervalos (ID de indicador, não prosa). Esta é a lição 27 de defesa contra intoxicação de conteúdo conectada à observabilidade.

> 的生产模式:将内容外存储(S3、你的日志存储),在 span 上记录引用(指针 ID,不是原文) .

> OpenTelemetry GenAI 语义约定 define LLM 和 Agent's可观测性标准──`gen_ai.request.model`- Não.`gen_ai.usage.input_tokens`- Não.`gen_ai.agent.name`E assim...

### Estabilidade

A maioria das convenções é experimental a partir de março de 2026.

> OpenTelemetry GenAI 语义约定 define LLM 和 Agent's可观测性标准──`gen_ai.request.model`- Não.`gen_ai.usage.input_tokens`- Não.`gen_ai.agent.name`E assim...

```
OTEL_SEMCONV_STABILITY_OPT_IN=gen_ai_latest_experimental
```

O DataDog v1.37+ mapeia que a GenAI atribui nativamente ao seu esquema de observabilidade LLM. Outros backends (Grafana, Honeycomb, Jaeger) suportam os atributos brutos.

> 🤔 **【困惑】**P: `invoke_agent`A: O agente que está sendo chamado não é "outro processo/serviço" A: O agente que está sendo chamado não é "outro processo/serviço" A: O agente que está sendo chamado não é um "outro processo/serviço" A: O agente que está sendo chamado não é um "outro processo/serviço" A: O agente que está sendo chamado não é um "outro processo/serviço" A: O agente que está sendo chamado não é um "outro processo/serviço" A: O agente que está sendo chamado não é um "outro processo/serviço" A: O agente que está sendo chamado não é um "outro processo/serviço" A: O agente que está sendo chamado não é um "outro processo/serviço" A: O agente que está sendo chamado não é um "outro processo" A: O agente que está sendo chamado não é um "outro processo" A: O agente que está sendo chamado para ser um agente de código interno, mas é um agente que está sendo chamado para ser um agente interno. Se você estiver usando o seu próprio código em um código interno, é um agente interno ou um agente de código interno, é um agente chamado para ser chamado para ser um agente de código interno ou um servidor, é um agente de código interno ou um servidor como o servidor de código de código aberto ou servidor de código aberto ou servidor de servidor, é um servidor de código aberto ou servidor de servidor de servidor de servidor de servidor, como o cliente.`rpc.system`- Não.`rpc.service`), conveniência e tradição de microserviços

> Datadog v1.37+ 原生将 GenAI 属性映射到其LLM Observability schema──其他后端(Grafana、Honeycomb、Jaeger) suport原始属性──

> OpenTelemetry GenAI 语义约定 define LLM 和 Agent's可观测性标准──`gen_ai.request.model`- Não.`gen_ai.usage.input_tokens`- Não.`gen_ai.agent.name`E assim...

### Onde este padrão vai mal

- **Capturing full prompts in spans.**Informações pessoais, segredos, dados de clientes em vestígios que podem ser lidos.
- **No `gen_ai.provider.name`.**Os painéis de multi-provedor quebram quando falta atribuição.
- **Spans without parent links.**Ferramentas órfãs, sempre propagam contexto.
- **Not setting stability opt-in.**Os seus atributos podem ser renomeados no upgrade de backend.

> **在 span 中捕获完整提示。**运维可以读取的追踪包含PII、密钥、客户数据──外部存储──
> **缺少 `gen_ai.provider.name`。**缺少归属时,多供应商仪表盘会出错.
> **没有父链接的 span。**孤立的工具 span──始终传播上下文──
> **不设置稳定性选择加入。**A sua característica pode ser renomeada no final da substituição.

## Construí-lo e realizei-o.
```figure
ae-genai-span-tree
```

## Construí-lo

`code/main.py`Implementa um emissor de estdlib com um período de tempo correspondente às convenções da GenAI:

> OpenTelemetry GenAI 语义约定 define LLM 和 Agent's可观测性标准──`gen_ai.request.model`- Não.`gen_ai.usage.input_tokens`- Não.`gen_ai.agent.name`E assim...

- `Span`com esquema de atributos GenAI.
- `Tracer`com`start_span`, contextos aninhados.
- Um agente com roteiro que emite:`create_agent`- Não .`invoke_agent`(INTERNAL), por ferramenta,`chat`- As chamadas de LLM.
- Um modo de captura de conteúdo que armazena pedidos externamente e registra IDs em intervalos.

- É o que é ?

```
python3 code/main.py
```

Output: uma árvore de extensão com todos os atributos GenAI necessários e uma "localização externa" que mostra as referências de conteúdo de opção.

> 输出: um que contenha todos os elementos essenciais do genAI 属性 树, bem como um que mostra escolha de incluir o "exterior de armazenamento" do conteúdo.

> OpenTelemetry GenAI 语义约定 define LLM 和 Agent's可观测性标准──`gen_ai.request.model`- Não.`gen_ai.usage.input_tokens`- Não.`gen_ai.agent.name`E assim...

## Use-o com o framework implementado.

- **Datadog LLM Observability**(v1.37+) mapas atributos nativo.
- **Langfuse / Phoenix / Opik**(Lessão 24)  auto-instrumentar o ecossistema.
- **Jaeger / Honeycomb / Grafana Tempo** rastreamento bruto de OTel; criar painéis de controle a partir de atributos GenAI.
- **Self-hosted** executar o Colector OTel com um processador GenAI.

## Envia-o . Produto .

`outputs/skill-otel-genai.md`Os cabos OTel GenAI se estendem a um agente existente com padrões de captura de conteúdo e armazenamento de referências externos.

> `outputs/skill-otel-genai.md`O OTel GenAI vai ser o agente existente, contendo o conteúdo capturado em valor de predefinição e armazenamento de referência externa.

> OpenTelemetry GenAI 语义约定 define LLM 和 Agent's可观测性标准──`gen_ai.request.model`- Não.`gen_ai.usage.input_tokens`- Não.`gen_ai.agent.name`E assim...

## Exercícios.

1. Instrumenta a sua lição 01 ReAct loop com `invoke_agent`(INTERNAL) + extensões por ferramenta. Enviar para uma instância Jaeger.
  Tradução do inglês para tradução do inglês:
2. Adicionar captura de conteúdo no modo "apenas referências": pedidos para SQLite, atributos span carregam apenas IDs de fila.
  Tradução do inglês para tradução do inglês:
3. Leia a especificação para `gen_ai.data_source.id`Entre em sua pesquisa Memorandum de lição 9.
  Tradução do inglês para tradução do inglês:
4. Set `OTEL_SEMCONV_STABILITY_OPT_IN=gen_ai_latest_experimental`e verifique se os seus atributos não são renomeados pelo coletor.
  Tradução do inglês para tradução do inglês:
5. Construir um painel de instrumentos: "qual erro de ferramenta correlaciona com quais modelos" apenas a partir dos atributos da GenAI.
  Tradução do inglês para tradução do inglês:

## Termos-chave .

| Term | What people say | What it actually means |
|------|----------------|------------------------|---|
| GenAI SIG | "OpenTelemetry GenAI group" | OTel working group defining the schema |  |
| invoke_agent | "Agent span" | Name of the span representing an agent run |  |
| CLIENT span | "Remote call" | Span for a call to a remote agent service |  |
| INTERNAL span | "In-process" | Span for an in-process agent run |  |
| gen_ai.provider.name | "Provider" | anthropic / openai / aws.bedrock / google.vertex |  |
| gen_ai.data_source.id | "RAG source" | Which corpus/store a retrieval hit |  |
| Content capture | "Prompt logging" | Opt-in capture of messages; store externally in prod |  |
| Stability opt-in | "Preview mode" | Env var to pin experimental conventions |  |

## Mais leitura 延伸阅读

- [OpenTelemetry GenAI semantic conventions](https://opentelemetry.io/docs/specs/semconv/gen-ai/) a especificação
  Tradução do português:
- [OpenAI Agents SDK](https://openai.github.io/openai-agents-python/) Gênero de tempo de tempo por padrão
  Tradução do português:
- [AutoGen v0.4 (Microsoft Research)](https://www.microsoft.com/en-us/research/articles/autogen-v0-4-reimagining-the-foundation-of-agentic-ai-for-scale-extensibility-and-robustness/) Espaços OTel incorporados
  Tradução do português:
- [Claude Agent SDK](https://platform.claude.com/docs/en/agent-sdk/overview) Proibição de conteúdo de rastreamento W3C
  Tradução do português:
