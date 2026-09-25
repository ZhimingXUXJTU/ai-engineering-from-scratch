# O Agente Claude SDK: Subbagents e loja de sessões
# O Arnes como uma biblioteca  Subbagents e loja de sessões

> Um arnes que você pode importar: ferramentas incorporadas, subagentes para isolamento de contexto, ganchos, propagação de vestígios W3C, persistência de sessão. O Claude Agent SDK é o exemplo de referência  a forma de biblioteca do arnes Claude Code  e Claude Managed Agents é a alternativa hospedada para trabalho de sincronia de longa duração.

**Type:** Learn + Build | **类型:** 构建
**Languages:** Python (stdlib) | **语言:** Python (标准库)
**Prerequisites:** Phase 14 · 01 (Agent Loop), Phase 14 · 10 (Skill Libraries) | **前置知识:** 见原文
**Time:** ~75 minutes | **时间:** 见原文

## Objetivos de aprendizagem

- Explique a diferença entre o SDK do cliente antropico (API bruto) e o SDK do agente Claude (forma de arnes).
- Descrever os sub-gêneros  paralelação e isolamento de contexto  e quando alcançá-los.
- Nomear a superfície de armazenamento de sessão do Python SDK (`append`- Não .`load`- Não .`list_sessions`- Não .`delete`- Não .`list_subkeys`) e o papel de `--session-mirror`- Não .
- Implementar um arnes de stdlib com ferramentas incorporadas, desovação subagente com contexto isolado, ganchos do ciclo de vida e uma loja de sessões.

## O problema é o problema da introdução

Uma API LLM cru obtém uma viagem de ida e volta. Um agente de produção precisa de execução de ferramentas, servidores MCP, ganchos do ciclo de vida, reprodução subagente, persistência de sessão, propagação de vestígios. Claude Agent SDK envia esta forma como uma biblioteca  o mesmo arnes Claude Code usa, exposto para agentes personalizados.

> O código de produção do agente precisa de ferramentas de execução, MCP, servidor, ciclo de vida, filho, agente, formação, reunião, perseguição, divulgação, e assim por diante.


> **【中文解读】**Claude Agent SDK é um sistema de desenvolvimento de um agente (o que significa "Agente") (o que significa "Agente") (o que significa "Agente") (o que significa "Agente") (o que significa "Agente") (o que significa "Agente"), "Agente" (o que significa "Agente"), "Agente" (o que significa "Agente"), "Agente" (o que significa "Agente"), "Agente" (o que significa "Agente"), "Agente" (o que significa "Agente"), "Agente" (o que significa "Agente"), "Agente" (o que significa "Agente"), "Agente" (o que significa "Agente"), "Agente" (o que significa "Agente"), "Agente" (o que significa "Agente"), "Agente" (o que significa "Agente"), "Agente" (o que significa "Agente"), "Agente" (o que significa "Agente"), "Agente" (o que significa "Agente"), "Agente" (o que significa "Agente"), "Agente" (o que significa "Agente"), "Agente" (o que significa "Agente"), "Agente" ou "Agente" (o que significa "Agente").

> **{【拓展：Claude Agent SDK 是 2026 年 Claude 生态的核心开发工具。与 OpenA...】}**O Claude Agent SDK é um instrumento de desenvolvimento central do Claude 生态 de 2026.[1] Em comparação com o OpenAI Agents SDK, ele concentra mais na integração profunda das habilidades únicas de Claude (como o pensamento prolongado e uso de computadores).

> - Não .**【前置】**必須先掌握:Fase 14·01(Agent Loop) e Fase 14·10(Skill Libraries) Claude Agent SDK 内置了技能 系统作为子 Agent的标准模式──如果你没有使用Claude Code CLI,强烈建议先使用几天本SDK就是Claude Code的库形式,理解CLI's behavior pattern对学习SDK事半功倍──

## O conceito central.

### SDK do cliente vs SDK do agente

- **Client SDK (`anthropic`).**A API de mensagens brutas é tua, possues o circuito, as ferramentas, o estado.
- **Agent SDK (`claude-agent-sdk`).**Execução de ferramentas integradas, conexões MCP, ganchos, reprodução de subagentes, loja de sessões, o ciclo de código Claude como biblioteca.

> **Client SDK（`anthropic`）。**O primeiro é o primeiro, que é o primeiro.
> **Agent SDK（`claude-agent-sdk`）。**O código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código

### Ferramentas incorporadas

O SDK envia mais de 10 ferramentas fora da caixa: ler/escrever arquivos, shell, grep, glob, web fetch, etc. Ferramentas personalizadas registram-se através da interface padrão de esquema de ferramentas.

> SDK 开箱提供 10+ 工具:文件读写、shell、grep、glob、网页抓取等──自定义工具通过标准工具-schema 接口注册──

> Claude Agent SDK é o agente oficial da Anthropic 框架──核心概念:Agent (Agent) 带系统提示和工具的 LLM) 、Tools (Tools) 可调用函数 (Função) 、Subagents (Sub-Agent) 子代理委派 (Sub-Agent) 、Session Store (Specialist) 会话持久化 (Specialist) 

### Sub-gêneros

Dois propósitos documentados pela Anthropic:

> O Antropic 文档 registrou dois usos:

1. **Parallelization.**Execute simultaneamente trabalhos independentes. "Encontre o arquivo de teste para cada um destes 20 módulos" é 20 tarefas paralelas.
2. **Context isolation.**Os subagentes usam sua própria janela de contexto; apenas os resultados retornam ao orquestrador.

Python SDK adições recentes: `list_subagents()`- Não .`get_subagent_messages()`para a leitura de transcrições de subagens.

> Python SDK Recent Recently New Features:`list_subagents()`- Não.`get_subagent_messages()`Usado para ler o registro de conversa do agente.

> - Não .**【类比】**O "projeto" da empresa é o seguinte: o "CEO" (o "agente principal") ocupa a totalidade da área, mas cada projeto específico é executado por um grupo de projetos específicos.**关键收益是上下文隔离**Se o "调研竞品" desse tipo de trabalho para ler 100 artigos se preenchem, o Agente principal se faz e fica afogado; se o Agente substituto, o Agente substituto, 100 artigos de leitura não contaminam o ponto de vista do Agente principal, apenas retornar à " 3 conclusões da análise do produto " .

> Claude Agent SDK é o agente oficial da Anthropic 框架──核心概念:Agent (Agent) 带系统提示和工具的 LLM) 、Tools (Tools) 可调用函数 (Função) 、Subagents (Sub-Agent) 子代理委派 (Sub-Agent) 、Session Store (Specialist) 会话持久化 (Specialist) 

### Loja de sessões

Paridade de protocolo com o TypeScript:

> Com o tipo de acordo de versão do TypeScript:

- `append(session_id, message)` adicionar um giro.
- `load(session_id)`- Restaurar a conversa.
- `list_sessions()` enumerar.
- `delete(session_id)` com sessões em cascata para subagentes.
- `list_subkeys(session_id)` lista de chaves subagentes.

`--session-mirror`(Bandera CLI) reflete a transcrição para um arquivo externo enquanto ele fluir, para depurar.

> `--session-mirror`(CLI 标志) durante o fluxo de transmissão, será o diálogo registrado em imagens de documentos externos, para serem utilizados em sua manipulação.

> Claude Agent SDK é o agente oficial da Anthropic 框架──核心概念:Agent (Agent) 带系统提示和工具的 LLM) 、Tools (Tools) 可调用函数 (Função) 、Subagents (Sub-Agent) 子代理委派 (Sub-Agent) 、Session Store (Specialist) 会话持久化 (Specialist) 

### Anéis

Anéis de ciclo de vida que podem ser registados:

> Registro de ciclo de vida:

- `PreToolUse`- Não .`PostToolUse` chamadas de porta ou de ferramenta de auditoria.
- `SessionStart`- Não .`SessionEnd`- Configurar e derrubar.
- `UserPromptSubmit` agir sobre a entrada do utilizador antes que o modelo a veja.
- `PreCompact` executar antes da compactação do contexto.
- `Stop`- Limpeza na saída do agente.
- `Notification` Alertas de canais laterais.

Os ganchos são como o pro-fluxo de trabalho (referência ao currículo da Fase 14) e sistemas semelhantes adicionam comportamento transversal.

> 子是专业工作流 (Fase 14 课程参考) e similar system 子是专业工作流 (Fase 14 课程参考) e similar system 子是专业工作流 (Fase 14 课程参考) e similar system 子是专业工作流 (Fase 14 课程参考)

> Claude Agent SDK é o agente oficial da Anthropic 框架──核心概念:Agent (Agent) 带系统提示和工具的 LLM) 、Tools (Tools) 可调用函数 (Função) 、Subagents (Sub-Agent) 子代理委派 (Sub-Agent) 、Session Store (Specialist) 会话持久化 (Specialist) 

### Contexto de rastreamento W3C

Os intervalos OTel ativos no chamador se propagam para o subprocesso CLI através de cabeçalhos de contexto de rastreamento W3C. Todo o rastreamento de múltiplos processos aparece como um rastreamento no seu backend.

> 调用方上活跃的OTel span 通过W3C 追踪上下文头传播到CLI 子进程──整个多进程追踪在你的后端显示为一个追踪──

> Claude Agent SDK é o agente oficial da Anthropic 框架──核心概念:Agent (Agent) 带系统提示和工具的 LLM) 、Tools (Tools) 可调用函数 (Função) 、Subagents (Sub-Agent) 子代理委派 (Sub-Agent) 、Session Store (Specialist) 会话持久化 (Specialist) 

### Claude gerenciava agentes

A alternativa hospedada (beta header `managed-agents-2026-04-01`O controlo comercial para infraestruturas gerenciadas.

> 托管替方案 (tradução de um programa de gestão de dados)`managed-agents-2026-04-01`O processo de gestão da infraestrutura de gestão é o seguinte:

> Claude Agent SDK é o agente oficial da Anthropic 框架──核心概念:Agent (Agent) 带系统提示和工具的 LLM) 、Tools (Tools) 可调用函数 (Função) 、Subagents (Sub-Agent) 子代理委派 (Sub-Agent) 、Session Store (Specialist) 会话持久化 (Specialist) 

### Onde este padrão vai mal

> ️ **【易错点】**O pior desastre é que a 100 pequenas missões geram 100 agentes.**后果**Cada agente tem seu próprio sistema de execução + 工具注册 + 上下文初始化,开销 30-60 秒/个,100 个就是 1 小时;并发又有限制(Antropic 每分钟代币 限制),最终任务跑一晚上──**一行修复**A única coisa que realmente é necessário é a tarefa de "independência sobre a janela de baixo" (como a profundidade do estudo) para gerar um agente.

- **Subagent over-spawn.**Desembaraçar 100 subagentes para 100 tarefas pequenas.
- **Hook creep.**Cada equipa adiciona ganchos, balões de tempo de arranque, revisa os ganchos trimestralmente.
- **Session bloat.**As sessões acumulam-se, o tamanho aumenta.`list_sessions`+ Política de expiração.

> 🤔 **【困惑】**P: Claude Agent SDK 和直接用人类Python SDK 写 agent loop 有什么本质区别?为什么要使用SDK? A: 三个不可替代能力:(1) **内置工具开箱即用**(文件、shell、grep 等 10+ 工具, 自己写至少两天);(2) **Session 持久化协议**(incluindo:**Hook 生命周期**(PreToolUse、PostCompact etc 7 个子点) ⋅ Se o seu Agente 只是简单问答, use SDK antropico就够了; se você quiser escrever Claude Code 那种生产级 Agent,SDK 省你几周工程时间──

> **子 Agent 过度生成。**Para 100 pequenas tarefas gerar 100 agentes.
> **钩子膨胀。**Cada equipa adiciona o tempo; o tempo de iniciação aumenta.
> **会话膨胀。**会话不断积累; 大小增长──使用 `list_sessions`+ 过期策略──

## Construí-lo e realizei-o.
```figure
ae-subagent-isolation
```

## Construí-lo

`code/main.py`Implementa a forma do SDK no stdlib:

> `code/main.py`Utilizando o padrão de biblioteca realizou o formato de SDK:

> Claude Agent SDK é o agente oficial da Anthropic 框架──核心概念:Agent (Agent) 带系统提示和工具的 LLM) 、Tools (Tools) 可调用函数 (Função) 、Subagents (Sub-Agent) 子代理委派 (Sub-Agent) 、Session Store (Specialist) 会话持久化 (Specialist) 

- `Tool`- Não .`ToolRegistry`com incorporado`read_file`- Não .`write_file`- Não .`list_dir`- Não .
- `Subagent` contexto privado, execução isolada, resultados devolvidos.
- `SessionStore` apenda, carrega, lista, exclui, list_subkey.
- `Hooks`- Não .`pre_tool_use`- Não .`post_tool_use`- Não .`session_start`- Não .`session_end`- Não .
- Uma demonstração: o agente principal gera 3 sub-agentes em paralelo (cada um isolado), agrega resultados, persiste sessão.

- É o que é ?

```
python3 code/main.py
```

O rastro mostra isolamento de contexto subagente (o tamanho do contexto do orquestrador permanece limitado), execução de gancho e persistência da sessão.

> 追踪显示子 Agent 的上下文隔离(编排者 上下文大小保持有界) 子执行和会话持久化──

> Claude Agent SDK é o agente oficial da Anthropic 框架──核心概念:Agent (Agent) 带系统提示和工具的 LLM) 、Tools (Tools) 可调用函数 (Função) 、Subagents (Sub-Agent) 子代理委派 (Sub-Agent) 、Session Store (Specialist) 会话持久化 (Specialist) 

## Use-o com o framework implementado.

- **Claude Agent SDK**para produtos Claude-first que querem a forma do arnés Claude Code.
- **Claude Managed Agents**para trabalhos de sincronização de longa duração hospedados.
- **OpenAI Agents SDK**(Lessão 16) para as contrapartes OpenAI-primeiras.
- **LangGraph + custom tools**Se quiserem a máquina de estado em forma de gráfico em vez disso.

## Envia-o . Produto .

`outputs/skill-claude-agent-scaffold.md`Estafa de um Claude Agent SDK app com subagens, ganchos, loja de sessões, MCP servidor anexo, e W3C rastreamento propagação.

> `outputs/skill-claude-agent-scaffold.md`                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             

> Claude Agent SDK é o agente oficial da Anthropic 框架──核心概念:Agent (Agent) 带系统提示和工具的 LLM) 、Tools (Tools) 可调用函数 (Função) 、Subagents (Sub-Agent) 子代理委派 (Sub-Agent) 、Session Store (Specialist) 会话持久化 (Specialist) 

## Exercícios.

1. Adicione um deslizador de subbagentes que distribui 20 tarefas em grupos de 5 subbagentes paralelos.
  Tradução do inglês para tradução do inglês:
2. Implementar um `PreToolUse`- O que é isso ?`write_file`As chamadas (5 por minuto por sessão).
  Tradução do inglês para tradução do inglês:
3. - O fio .`list_subkeys`Como é o ninho profundo?
  Tradução do inglês para tradução do inglês:
4. Leva o brinquedo para o real .`claude-agent-sdk`Pacote Python. Que mudanças no registro de ferramentas?
  Tradução do inglês para tradução do inglês:
5. Quando é que passaria de auto-host para gerenciado?
  Tradução do inglês para tradução do inglês:

## Termos-chave .

| Term | What people say | What it actually means |
|------|----------------|------------------------|---|
| Agent SDK | "Claude Code as a library" | Harness shape: tools, MCP, hooks, subagents, session store |  |
| Subagent | "Child agent" | Separate context, own budget; results bubble up |  |
| Session store | "Conversation DB" | Persist, load, list, delete turns with subagent cascade |  |
| Hook | "Lifecycle callback" | Pre/post tool, session, prompt submit, compact, stop |  |
| W3C trace context | "Cross-process trace" | Parent span propagates into CLI subprocess |  |
| Managed Agents | "Hosted harness" | Anthropic-hosted long-running async work |  |
| `--session-mirror` | "Transcript mirror" | Writes session turns to an external file as they stream |  |
| MCP server | "Tool surface" | External tool/resource source attached to the agent |  |

## Mais leitura 延伸阅读

- [Claude Agent SDK overview](https://platform.claude.com/docs/en/agent-sdk/overview) a forma de biblioteca do Código Claude
  Tradução do português:
- [Anthropic, Building agents with the Claude Agent SDK](https://www.anthropic.com/engineering/building-agents-with-the-claude-agent-sdk) Padrões de produção
  Tradução do português:
- [Claude Managed Agents overview](https://platform.claude.com/docs/en/managed-agents/overview) alternativa hospedada
  Tradução do português:
- [OpenAI Agents SDK](https://openai.github.io/openai-agents-python/) contraparte
  Tradução do português:
