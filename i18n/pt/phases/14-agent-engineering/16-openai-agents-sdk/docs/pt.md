# OpenAI Agents SDK: Transferências, guardrails, rastreamento

> O OpenAI Agents SDK é o framework multi-agente leve construído sobre a API Responses. Cinco primitivos: Agente, Handoff, Guardrail, Sessão, Tracing.`transfer_to_<agent>`Os guardrails desligam-se na entrada ou saída.

**Type:** Learn + Build | **类型:** 构建
**Languages:** Python (stdlib) | **语言:** Python (标准库)
**Prerequisites:** Phase 14 · 01 (Agent Loop), Phase 14 · 06 (Tool Use) | **前置知识:** 见原文
**Time:** ~75 minutes | **时间:** 见原文

## Objetivos de aprendizagem

- Nomear os cinco primitivos do OpenAI Agents SDK.
- Explique as entregas: por que são modeladas como ferramentas, que forma de nome o modelo vê e como o contexto se transfere.
- Distinguir entre barris de entrada, barris de saída e barris de ferramenta; explicar `run_in_parallel`- Contra o modo de bloqueio.
- Implementar um tempo de execução de stdlib com manchas + barris + rastreamento de estilo span.

## O problema é o problema da introdução

Agentes que não podem delegar limpo acabam por encher tudo em um prompt. Agentes sem barris enviam PII, saída que viola as políticas ou loop para sempre. O SDK do OpenAI codifica os três primitivos que tornam o trabalho de vários agentes tratável.

> 无法干净地委派任务的代理 最终将所有东西塞进一个提示词中. 无护的代理会泄露PII. 输出违反政策内容或永远循环. OpenAI SDK vai tornar mais de um trabalho de agente administrável.


> **【中文解读】**OpenAI Agents SDK(orig Swarm) é o modelo de design do SDK 简洁至上 以最小抽象实现最常见的代理模式.

> **{【拓展：OpenAI Agents SDK 是 2025-2026 年最流行的轻量级 Agent 框架。其 ...】}**O OpenAI Agents SDK é o mais popular modelo de Agente de classe leve de 2025-2026. O seu modelo de entrega de Agente de vários países é o de "controle de agências" e um Agente vai transferir o controle para o próximo.

> - Não .**【前置】**必須先掌握:Fase 14·01(Agent Loop) 和Fase 14·06(Tool Use) OpenAI Agents SDK 就是這些概念的产品化封装──还需要熟悉OpenAI Responses API( não é o antigo Chat Completions API), pois o SDK é baseado em Resposta API 构建的──

## O conceito central.

### Cinco primitivos

1. **Agent.**LLM + instruções + ferramentas + entregas.
2. **Handoff.**Delegação para outro agente. Representado para o modelo como uma ferramenta chamada `transfer_to_<agent_name>`- Não .
3. **Guardrail.**A validação em entrada (apenas primeiro agente), saída (apenas último agente) ou invocação de ferramenta (por ferramenta de função).
4. **Session.**História de conversação automática ao longo das curvas.
5. **Tracing.**Formas de ligação para gerações de LLM, chamadas de ferramentas, entregas, barris.

### As entregas como ferramentas

O modelo vê .`transfer_to_billing_agent`A chamada indica o tempo de execução para:

> 模型在其工具列表中看 `transfer_to_billing_agent`调用 significa que se opera quando é necessário:

> O OpenAI Agents SDK 提供四种核心概念:Agents (Agentes) 带指令和工具的 LLM) ‧Handoffs (Handoffs) ‧Agent 间移交) ‧Guardrails (Guardails) 输入/输出验证) ‧Tracing (Tracking) 运行追踪) ‧Producção (Classe) 开发框架 (Classe) ‧Agent 开发框架──

1. Copiar o contexto da conversa (ou desintegrá-la através de `nest_handoff_history`- O que é?
2. Inicialize o agente-alvo com as instruções.
3. Continuem a correr com o agente alvo.

Este é o padrão de supervisão (Lessão 13 / Lessão 28) produzido.

> É o modelo de supervisor de produtos depois de serem produzidos.

> - Não .**【类比】**O médico da clínica disse: "Você vai para a clínica".`transfer_to_cardiology_agent` doente (doente)  doente (doente)  doente (doente)  doente (doente)  doente (doente)  doente (doente)  doente (doente)  doente (doente)  doente (doente)  doente (doente)  doente (doente)  doente (doente)  doente (doente)  doente (doente)  doente (doente)  doente (doente)  doente (doente)  doente (doente)  doente (doente)  doente (doente)  doente (doente)  doente (doente)  doente (doente)  doente (doente)  doente (doente)  doente (doente)  doente (doente)  doente (doente)  doente (doente)  doente (doente)  doente (doente)  doente)  doente (doente)  doente (doente)  doente (doente) **关键**O supervisor de LangGraph é diferente. O supervisor sempre mantém o controle, apenas "envia" um especialista.

> O OpenAI Agents SDK 提供四种核心概念:Agents (Agentes) 带指令和工具的 LLM) ‧Handoffs (Handoffs) ‧Agent 间移交) ‧Guardrails (Guardails) 输入/输出验证) ‧Tracing (Tracking) 运行追踪) ‧Producção (Classe) 开发框架 (Classe) ‧Agent 开发框架──

### Ferras de guarda

Três sabores:

> Três tipos:

- **Input guardrails.**Rejeita pedidos inseguros ou fora do alcance antes de qualquer chamada de LLM.
- **Output guardrails.**Aplique o último agente, detecta vazamentos de PII, violações de políticas, respostas mal formadas.
- **Tool guardrails.**Executa ferramentas por função, valida argumentos, verifique permissões, executa auditoria.

Modo:

> 模式:

- **Parallel**(default) O LLM Guardrail funciona ao lado do LLM principal. Latência inferior da cauda. Se tropeçar, o trabalho do LLM principal é descartado (desemprego de tokens).
- **Blocking**(`run_in_parallel=False`O Master em Direito da Guarda vai primeiro, se tropeçar, não há tokens desperdiçados na chamada principal.

Os trifles aumentam .`InputGuardrailTripwireTriggered`- Não .`OutputGuardrailTripwireTriggered`- Não .

> 触发器会抛出 `InputGuardrailTripwireTriggered`- Não .`OutputGuardrailTripwireTriggered`- Não é normal.

> O OpenAI Agents SDK 提供四种核心概念:Agents (Agentes) 带指令和工具的 LLM) ‧Handoffs (Handoffs) ‧Agent 间移交) ‧Guardrails (Guardails) 输入/输出验证) ‧Tracing (Tracking) 运行追踪) ‧Producção (Classe) 开发框架 (Classe) ‧Agent 开发框架──

### Traçamento

Cada geração de LLM, chamada de ferramentas, transferência e guarda-roupa emite um tempo.`OPENAI_AGENTS_DISABLE_TRACING=1`- Não.`add_trace_processor(processor)`Os fãs vão para o seu próprio backend ao lado do OpenAI.

> 默认开启──每次LLM 生成、工具调用、交接和护都发出一个跨度──`OPENAI_AGENTS_DISABLE_TRACING=1`Pode escolher sair.`add_trace_processor(processor)`Pode ser enviado ao mesmo tempo para o seu próprio terminal e para o terminal do OpenAI.

> O OpenAI Agents SDK 提供四种核心概念:Agents (Agentes) 带指令和工具的 LLM) ‧Handoffs (Handoffs) ‧Agent 间移交) ‧Guardrails (Guardails) 输入/输出验证) ‧Tracing (Tracking) 运行追踪) ‧Producção (Classe) 开发框架 (Classe) ‧Agent 开发框架──

### Sessões

`Session`armazena histórico de conversação em um backend (SQLite, Redis, custom). `Runner.run(agent, input, session=session)`Cargas automáticas e acessórios.

> `Session`Em segundo lugar, o sistema de armazenamento de dados é um sistema de armazenamento de dados.`Runner.run(agent, input, session=session)`Autocarga e adição.

> O OpenAI Agents SDK 提供四种核心概念:Agents (Agentes) 带指令和工具的 LLM) ‧Handoffs (Handoffs) ‧Agent 间移交) ‧Guardrails (Guardails) 输入/输出验证) ‧Tracing (Tracking) 运行追踪) ‧Producção (Classe) 开发框架 (Classe) ‧Agent 开发框架──

### Onde este padrão vai mal

> ️ **【易错点】**Drift de transferência (de transferência) (Agent A 移交给 B,B 又移交给 A,A 再移交给 B...**后果**O que é que eu faço?**一行修复**: em Runner 里加 hop counter`max_handoffs=5`), supera-`HandoffBudgetExceeded`Não há proteção, mas temos de nos adicionar.

- **Handoff drift.**Agente A entrega para o Agente B, que entrega para o Agente A. Adicione um contador de saltos.
- **Guardrail bypass.**As barragens de ferramentas só disparam em ferramentas funcionais; ferramentas incorporadas (leitor de arquivos, web-trach) precisam de uma política separada.
- **Over-tracing.**O conteúdo sensível em intervalos.

> 🤔 **【困惑】**P: Parallel de guardrail                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                     **选择规则**Se o barranco de segurança 触发率高 (como >20%), use bloqueio 省钱; se o índice de触发率 baixa (como <5%), use paralelo 省延迟。

> **交接漂移。**Agente A 交交给Agente B,Agente B também交交回Agente A 添加跳数计器
> **护栏绕过。**工具护只在函数工具上触发; 内置工具(文件读取器、网页抓取) requer estratégia única。
> **过度追踪。**Span 中包含敏感内容──配合 OTel GenAI 内容捕获规则 (§ 23 课) 使用外部存储,按 ID 引用──

## Construí-lo e realizei-o.
```figure
ae-agent-handoff
```

## Construí-lo

`code/main.py`Implementa a forma do SDK no stdlib:

> `code/main.py`Utilizando o padrão de biblioteca realizou o formato de SDK:

> O OpenAI Agents SDK 提供四种核心概念:Agents (Agentes) 带指令和工具的 LLM) ‧Handoffs (Handoffs) ‧Agent 间移交) ‧Guardrails (Guardails) 输入/输出验证) ‧Tracing (Tracking) 运行追踪) ‧Producção (Classe) 开发框架 (Classe) ‧Agent 开发框架──

- `Agent`- Não .`FunctionTool`- Não .`Handoff`(como ferramenta de função com semântica de transferência).
- `Runner`com barris de entrada/saída/herramienta, remessa de mão e contador de saque.
- Um simples emissor de espaço para mostrar a forma do rastro.
- Um agente de triagem que entrega a faturamento ou suporte com base na consulta do usuário; viagens de guarda em uma entrada.

- É o que é ?

```
python3 code/main.py
```

O rastro mostra duas entregas bem sucedidas, uma viagem de entrada e uma árvore espalhando o que o SDK real emite.

>  tracking mostra duas vezes de sucesso de ligação ∞ uma vez de entrada ∞ ∞ ∞ ∞ ∞, bem como uma que reflete o verdadeiro SDK ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞   ∞ ∞ ∞    ∞                                                

> O OpenAI Agents SDK 提供四种核心概念:Agents (Agentes) 带指令和工具的 LLM) ‧Handoffs (Handoffs) ‧Agent 间移交) ‧Guardrails (Guardails) 输入/输出验证) ‧Tracing (Tracking) 运行追踪) ‧Producção (Classe) 开发框架 (Classe) ‧Agent 开发框架──

## Use-o com o framework implementado.

- **OpenAI Agents SDK**para os produtos OpenAI-first.
- **Claude Agent SDK**(Lessão 17) para produtos Claude-first.
- **LangGraph**(Lessão 13) quando quiser um estado explícito e um currículo duradouro.
- **Custom**Quando precisar de controlo exato (voz, multi-provedor, implantações federadas).

## Envia-o . Produto .

`outputs/skill-agents-sdk-scaffold.md`Estabelece um aplicativo de SDK Agents com um agente de triagem, manuais, barris de entrada/saída/herramienta, armazenamento de sessões e um processador de rastreamento.

> `outputs/skill-agents-sdk-scaffold.md`construir um SDK de Agentes  aplicativo, contendo um Agente de diagnóstico 交接、输入/输出/工具护、会话存储和追踪处理器──

> O OpenAI Agents SDK 提供四种核心概念:Agents (Agentes) 带指令和工具的 LLM) ‧Handoffs (Handoffs) ‧Agent 间移交) ‧Guardrails (Guardails) 输入/输出验证) ‧Tracing (Tracking) 运行追踪) ‧Producção (Classe) 开发框架 (Classe) ‧Agent 开发框架──

## Exercícios.

1. Adicione um contador de transferências: rejeitar após transferências N.
  Tradução do inglês para tradução do inglês:
2. Implementação `nest_handoff_history`como opção  colapsa as mensagens anteriores num só resumo antes da transferência.
  Tradução do inglês para tradução do inglês:
3. Escreva um barranco de saída de bloqueio, compara a latência de pedidos que o tropeçam com os que passam.
  Tradução do inglês para tradução do inglês:
4. - O fio .`add_trace_processor`Que forma emite por período?
  Tradução do inglês para tradução do inglês:
5. Leia os documentos do SDK.`openai-agents-python`O que é que você fez de errado?
  Tradução do inglês para tradução do inglês:

## Termos-chave .

| Term | What people say | What it actually means |
|------|----------------|------------------------|---|
| Agent | "LLM + instructions" | Agent type in the SDK; owns tools and handoffs |  |
| Handoff | "Transfer" | Tool the model calls to delegate to another agent |  |
| Guardrail | "Policy check" | Validation on input / output / tool invocation |  |
| Tripwire | "Guardrail trip" | Exception raised when guardrail rejects |  |
| Session | "History store" | Conversation memory persisted between runs |  |
| Tracing | "Spans" | Built-in observability over LLM + tool + handoff + guardrail |  |
| Blocking guardrail | "Sequential check" | Guardrail runs first; no token waste on trip |  |
| Parallel guardrail | "Concurrent check" | Guardrail runs alongside; lower latency, wastes tokens on trip |  |

## Mais leitura 延伸阅读

- [OpenAI Agents SDK docs](https://openai.github.io/openai-agents-python/) primitivos, remessas, vigas, rastreamento
  Tradução do português:
- [Claude Agent SDK overview](https://platform.claude.com/docs/en/agent-sdk/overview) Coleta de sabor a clado
  Tradução do português:
- [Anthropic, Building Effective Agents](https://www.anthropic.com/research/building-effective-agents) quando se pode procurar por entregas
  Tradução do português:
- [OpenTelemetry GenAI semantic conventions](https://opentelemetry.io/docs/specs/semconv/gen-ai/) o SDK padrão Agents abrange o mapa para
  Tradução do português:
