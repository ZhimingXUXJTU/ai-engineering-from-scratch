# Orçamentos de Ação, Capas de Iteração e Governadores de Custos

> O custo mensal de LLM de um agente de comércio eletrônico de médio porte aumentou de $1,200 to $O software de gestão de dados da Microsoft, que é o software de gestão de dados, é o mais recente e mais recente de todos os sistemas de gestão de dados da Microsoft.`max_tokens`O SDK de código Claude da Anthropic envia os mesmos primitivos sob diferentes nomes. Limites de velocidade financeira , por exemplo, cortar o acesso em > $ 50 em 10 minutos  pegar loops mais rápido do que os limites mensais.

> **【中文解读】**Emprego de Mestrado em Gestão de Serviços de Empresa em Empresas de Minas Gerais$1,200 跳到 $4.800── isto não é um bug de preços── isto é um agente que encontra um novo ciclo e continua a gastar nele── Microsoft's Agent Governance Toolkit (WEB`max_tokens`、 cada token de tarefa 和美元预算、每日/月上限、代上限、分层模型路由、提示缓存、上下文窗口、昂贵动作上 HITL 检查点、预算违反时的终止开关。Antropic's Claude Code Agent SDK 以不同名称出货相同原语──金融速度限制例如10分钟内 >$50 切断访问比月度上限更快捕获循环──

> **【拓展：单一上限不够 → 分层栈】**失败模式和时间尺度需要应对:5 秒重试的失控循环 (失控循环) 速度限制捕获) 工作的缓慢泄漏 (失败模式和时间尺度需要应对:5 秒重试的失控循环) 速度限制捕获) 任务 2x 工作的缓慢泄漏 (失控漏漏) 每日上限) 新版本 5x token 的坏发布 (失败模式和时间尺度需要应对:5 秒重试的失控循环) 任务 2x 工作的缓慢泄漏 (失控漏) 每周/月上限) 实际需求的合法激增 (失败模式和时间尺度需要应对) 小时/日上限带清晰日志) 单一上限在钱包已空后才被捕获; 分层在分钟内被捕获失控、数小时内被捕获泄漏、一天内被捕获发布

**Type:** Learn | **类型:** 学习
**Languages:** Python (stdlib, layered cost-governor simulator) | **语言:** Python（标准库，分层成本治理器模拟器）
**Prerequisites:** Phase 15 · 10 (Permission modes), Phase 15 · 12 (Durable execution) | **前置知识:** Phase 15 · 10（权限模式），Phase 15 · 12（持久执行）
**Time:** ~60 minutes | **时间:** ~60 分钟

> - Não .**【前置】**O governo da República Federal da China (Federal Republic of China) não aceitou a decisão de tomar medidas para impedir a transferência de recursos para a União Europeia.
> - Não .**【类比】**Custos Governador = "Agentão de crédito de crédito"―普通 LLM 调用 = 刷卡(每次小钱);Agentão 进入死循环 = 盗刷(一夜烧光)―防御分层:(1) 速度限制10分钟 >$50 切断（防失控）；(2) 每日上限——$200/天(防慢泄漏);$3000/月（防坏发布）；(4) 单任务上限——$5/ tarefa (防单次任务爆炸)
> ️ **【易错点】**Apenas se estabelecer limite de velocidade → Uma noite de queimação do orçamento do mês é apenas encontrado.

## O problema é o problema da introdução

> **【中文解读】**Gerenciadores de custos) Monitoramento e limitação do consumo de recursos do agente Principalmente é API 调用费用和代币使用量──没有成本控制器的代理可能在循环或低效执行中产生巨额账单──三种控制策略:(1) 预算上限硬性代币/费用限制;(2) 速度限制每分/每小时调用上限;(3) 效率门控当成本/收益比恶化时暂停──

> **【拓展：cost governors】**O controle de desempenho é o principal desafio da implantação de produtos de agentes em 2025-2026.

Os agentes autônomos gastam dinheiro a cada turno.

> Agente independente, em cada rodada, gasta dinheiro e dinheiro.

O mau resultado de um chatbot é uma má resposta; o mau ciclo de um agente é uma conta. O termo documentado pela indústria para o modo de falha é "Denial of Wallet"

> 聊天机器人错误输出是一条错误回复;A err err err err err cycle of an agent is a bill单―― 行业记录的失败模式术语是"Denial of Wallet"Agent 持续推理、持续调用工具、持续计费,没有什么阻止它,因为没有什么被设计为阻止──

A solução não é um número. É uma pilha de limites em diferentes escalas de tempo e granularidades: por pedido, por tarefa, por hora, por dia, por mês. Uma pilha bem projetada pega um loop fugitivo em minutos, um vazamento lento em horas e uma liberação ruim em um dia. A mesma pilha mantém um orçamento quando o agente é de longo horizonte e autônomo.

> 修复不是一个数字──它是不同的时间尺度和粒度的限制: por pedido, por missão, por hora, por dia, por mês── 良好的设计在分钟内捕获失控循环,在数小时内捕获缓慢泄漏,在一天内捕获坏发布── 同在代理长程自主时保持预算── 修复不是一个数字.

> **【中文解读】**Esta secção apresenta o conceito e o método de implementação do Agente de IA. O Agente é um sistema autónomo impulsionado pelo LLM, capaz de observar o ambiente, pensar decisões, executar a ação e ciclo de vida até a conclusão do objetivo.

Esta é uma lição de engenharia: a matemática é trivial, a disciplina é onde as equipes falham. A lista de limites abaixo é todos nomeados ou no Microsoft Agent Governance Toolkit ou no Antropic Claude Code Agent SDK documentos.

> É uma aula de engenharia: Matemática comum, é um ponto de sucesso da equipe.

## O conceito central.

### O governador de custos está em pé.

1. **`max_tokens` per request.**Simples, impede que qualquer chamada emite um final ilimitado.
   Tradução:**每请求 `max_tokens`。**简单―― evitar que o único uso seja feito sem limites.
2. **Per-task token budget.**Ao longo da corrida, não exceda os tokens N. Parar duro no limite.
   Tradução:**每任务 token 预算。**O total do funcionamento não excede N 个 token.
3. **Per-task dollar budget.**O mesmo que os tokens, mas em moeda.`max_budget_usd`em Claude Code.
   Tradução:**每任务美元预算。**Com token similar mas em moeda.`max_budget_usd`- Não.
4. **Per-tool call cap.**Não mais do que N `WebFetch`- chamadas, N`shell_exec`chamadas, etc.
   Tradução:**每工具调用上限。**Não excede N 个 `WebFetch`- Não.`shell_exec`调用等──
5. **Iteration cap (`max_turns`).**Iterações de loop de agente total; impede loop de raciocínio infinito.
   Tradução:**迭代上限（`max_turns`）。**总 Agente 循环代数; prevenir o ciclo de propulsão ilimitada
6. **Per-minute / per-hour / per-day / per-month cap.**Fragmentos de vidro, vazamentos em diferentes escalas de tempo.
   Tradução:**每分/时/日/月上限。**滚动窗口──在不同时间尺度捕获泄漏──
7. **Financial velocity limit.**Por exemplo, "se gastar mais de 50 dólares em 10 minutos, corte o acesso".
   Tradução:**金融速度限制。**Por exemplo, "se 10 minutos de tempo gastarem mais de US$ 50, cortem a visita"
8. **Tiered model routing.**Default para um modelo menor; escala para um maior apenas quando um classificador julgar a tarefa que o justifica.
   Tradução:**分层模型路由。**默认小模型; apenas quando a classificação de um determinado tipo de tarefa vale a pena ser promovida a um modelo maior.
9. **Prompt caching.**Contexto de sistema rápido e estável armazenado no cache do fornecedor; custo de token de reenvio é próximo de zero.
   Tradução:**提示缓存。**系统提示和稳定上下文存储在供应商缓存; 重发的代币 成本接近零──
10. **Context windowing.**Compactação / resumo para manter o contexto ativo abaixo de um limiar; redução direta de custos de tokens.
    Tradução:**上下文窗口。**压缩/摘要 值低于值; direct token 成本降低──
11. **HITL checkpoints on expensive actions.**Antes de uma ação conhecida por ser cara (longa chamada de ferramentas, grande download, uma atualização de modelo cara), é necessário um toque humano.
    Tradução:**昂贵动作上的 HITL 检查点。**Na conhecida mobilização caro (長工具调用,大下载,昂贵模型升级) 之前要求人类点击──
12. **Kill switch on budget breach.**A sessão aborta quando qualquer tampa se acende. A tampa é gravada; requer um caminho separado de reabilitação.
    Tradução:**预算违反时终止开关。**任一上限触发时会话停止──上限被记录; 需要单独重新启动路径──

### Por que a pilha, não um limite? Por que é o limite?

Um único limite mensal pega um agente fugitivo apenas depois que a carteira desapareceu. Um único limite por solicitação não pega nada no nível da sessão. Diferentes modos de falha exigem diferentes escalas de tempo:

> 单一月度上限只在钱包空后捕获失控 单一每请求上限在会话级中什么也没捕获 单一月度上限只在钱包空后捕获失控 单一每请求上限在会话级中什么也没捕获 单一月度上限只在钱包空后捕获失控 单一每请求上限在会话级中什么也没捕获 单一月度上限只在钱包空后捕获失控 单一每请求上限在会话级中什么也没捕获 单一月度上限只在钱包空后捕获失败模式需要不同的时间度:

- **Runaway loop**(Agente preso em uma nova tentativa de 5 segundos): capturado pelo limite de velocidade.
  Tradução:**失控循环**(Agente 卡在 5 秒重试): velocidade limite capture
- **Slow leak**(agente que realiza ~ 2x o trabalho esperado por tarefa): capturado pelo limite diário.
  Tradução:**缓慢泄漏**(Agente cada tarefa faz cerca de 2x 预期工作):
- **Bad release**(nova versão utiliza tokens 5x): capturado por limite semanal / mensal.
  Tradução:**坏发布**(nova versão com token 5x): Cada semana / mês
- **Legitimate surge**(demanda real, não um bug): capturado por limite hora/dia com registro claro.
  Tradução:**合法激增**(真实需求,非 bug):小时/日上限带清晰日志捕获──

### A superfície do orçamento de Claude Code.
### Superfície de orçamento de arame

O SDK Claude Code Agent expõe (documentos públicos):

> Claude Code Agent SDK 暴露(公开文档):

- `max_turns` Capítulo de iteração.
  Tradução:`max_turns`- Não.
- `max_budget_usd`- Capítulo de 1 do artigo 92.° do Tratado.
  Tradução:`max_budget_usd`美元上限;违反时会话中止──
- `allowed_tools`- Não .`disallowed_tools` alufrator de ferramentas e denilista.
  Tradução:`allowed_tools`- Não .`disallowed_tools` ferramentas permitindo e rejeitando a lista
- Pontos de gancho antes da utilização da ferramenta para contabilização de custos personalizada.
  O primeiro passo é o cálculo de custos.

Combinar com a escada de modo de autorização (Lessão 10).`autoMode`sessão sem `max_budget_usd`O Antropic define explicitamente o modo automático como exigindo controles de orçamento; o classificador é ortogonal ao custo.

> Com o poder de forma de escadação (第 10 课)结合──无 `max_budget_usd`de `autoMode`O Modo Automático é um sistema de controle de orçamento;

### Lei da UE sobre IA, Agente OWASP Top 10

O Kit de Ferramentas de Governança de Agentes da Microsoft abrange os requisitos do Top 10 do Agente OWASP e do artigo 14.o da Lei da IA da UE (supervisão humana).

> O conjunto de ferramentas de governança de agentes da Microsoft  abrangendo o OWASP Agentic Top 10 e a Lei da UE sobre IA n.o 14 条

### O observado .$1,200 → $4.800 casos observados.$1,200 → $4.800 casos

O caso real nos documentos da Microsoft: um agente de comércio eletrônico cujo custo mensal triplicou após a adição de uma nova ferramenta.

> O caso real no arquivo da Microsoft: um agente de comércio eletrônico aumentou três vezes o custo de adição de novos instrumentos no mês seguinte.

A ferramenta permitiu que o agente pesquisasse o estado do pedido durante cada sessão. Sem detecção de loop. Sem limite de cada ferramenta. Sem alerta sobre crescimento semana a semana. A correção foi um limite de cada ferramenta mais um alerta de crescimento diário. Esta é uma modelo: cada nova superfície de ferramenta é um novo ciclo potencial; cada nova ferramenta precisa de seu próprio limite e seu próprio alerta.

> O instrumento permite ao Agente, durante cada sessão, fazer uma consulta de ordem de estado. Não há limite de cada instrumento. Não há limite de cada instrumento.

## Use-o com o framework implementado.
```figure
cost-governor-stack
```

## Usá-lo

`code/main.py`O agente simulado entra em um ciclo de pesquisa após algumas voltas; o pilão em camadas o pega dentro da janela de velocidade enquanto um único limite mensal não dispararia até dias depois.

> `code/main.py`模拟有和没有分层成本管理的代理运行;模拟代理在某些轮次后漂移到轮询循环;分层在速度窗口内捕获它,而单一级上限直到几天后才触发;

## Envia-o . Produto .

`outputs/skill-agent-budget-audit.md`Audita a pilha de governadores de custos da implantação de agentes proposta e identifica as camadas ausentes.

> `outputs/skill-agent-budget-audit.md`O orçamento da Comissão para o exercício de 2015 foi de um modo geral mais elevado do que o previsto no artigo 1.o, n.o 1, do Regulamento (CE) n.o 1083/2005.

## Exercícios.

1. Corra .`code/main.py`Confirme o limite de velocidade antes do limite de iteração em uma trajetória de ciclo de votação.
   Tradução: 运行`code/main.py`■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■

2. Desenhar um conjunto de tampas por ferramenta para um agente do navegador (Lessão 11). Qual ferramenta precisa do tampão mais apertado?
   Por exemplo, a primeira vez que o usuário de um dispositivo de navegação usa um dispositivo de navegação, ele pode usar um dispositivo de navegação.

3. Leia os documentos do Kit de ferramentas de governança de agentes da Microsoft. Enumere cada tipo de tampa os nomes do kit de ferramentas. Mapeie cada um para um dos modos de falha (loop de fuga, vazamento lento, liberação ruim, aumento).
   Chinese: 文译:阅读Microsoft Agent Governance Toolkit 文档――列出工具包命名的每个上限类型――将各映射到失败模式之一(失控循环、缓慢泄漏、坏发布、激增) 』

4. Preço de uma execução durante a noite sem supervisão para uma tarefa realista (por exemplo, "triar 50 emissão num repo").`max_budget_usd`2x a sua estimativa de pontos.
   Tradução em inglês: для истинных задач (например, "分类 50 个仓库 issue")`max_budget_usd`Para você, a sua avaliação é de 2x.

5. O Claude Code.`max_budget_usd`Desenhar um limite de velocidade complementar que você impõe externamente.
   Tradução do português:`max_budget_usd`Em um discurso total custo em causa. O que é que você vai fazer para restringir a velocidade de complemento de forças externas.

## Termos-chave .

| Term | What people say | What it actually means |
|---|---|---|
| 术语 | 通俗说法 | 实际含义 |
| Denial of Wallet | "Runaway bill" | Agent loop generating spend with no cap to stop it |
| Denial of Wallet | "失控账单" | 无上限阻止的 Agent 循环产生花费 |
| max_tokens | "Per-request cap" | Ceiling on a single completion's size |
| max_tokens | "每请求上限" | 单次补全大小上限 |
| max_turns | "Iteration cap" | Ceiling on agent loop iterations in a session |
| max_turns | "迭代上限" | 会话中 Agent 循环迭代数上限 |
| max_budget_usd | "Dollar kill switch" | Session cost cap; aborts on breach |
| max_budget_usd | "美元终止开关" | 会话成本上限；违反时中止 |
| Velocity limit | "Rate cap" | Limit on spend per short window (e.g., $50 / 10 min) |
| 速度限制 | "速率上限" | 短窗口花费限制（例如 $50/10 分钟） |
| Tiered routing | "Small model first" | Cheap model default; escalate only when classifier warrants |
| 分层路由 | "小模型优先" | 默认廉价模型；仅当分类器批准时升级 |
| Prompt caching | "Cached system prompt" | Provider-side cache reduces re-send token cost to near zero |
| 提示缓存 | "缓存系统提示" | 提供商侧缓存将重发 token 成本降至接近零 |
| HITL checkpoint | "Human approval gate" | Human tap required before expensive action |
| HITL 检查点 | "人类批准门" | 昂贵动作前需人类点击 |

## Mais leitura 延伸阅读

- [Anthropic Claude Code Agent SDK — agent loop and budgets](https://code.claude.com/docs/en/agent-sdk/agent-loop)- Não .`max_turns`- Não .`max_budget_usd`, alistadores de ferramentas.
  Tradução:`max_turns`- Não.`max_budget_usd`、 ferramentas permitindo a lista
- [Microsoft Agent Framework — human-in-the-loop and governance](https://learn.microsoft.com/en-us/agent-framework/workflows/human-in-the-loop)- pontos de controlo de governadores de custos.
  O custo de gestão de dados é o resultado da análise.
- [Anthropic — Claude Managed Agents overview](https://platform.claude.com/docs/en/managed-agents/overview) Controle dos custos do lado do fornecedor.
  Tradução do inglês:
- [Anthropic — Prompt caching (Claude API docs)](https://platform.claude.com/docs/en/prompt-caching)- Mecânica de cache.
  Tradução do inglês:缓存机械──
- [Anthropic — Prompt caching (Claude API docs)](https://platform.claude.com/docs/en/build-with-claude/prompt-caching)- Mecânica de cache.
- [Anthropic — Measuring agent autonomy in practice](https://www.anthropic.com/research/measuring-agent-autonomy) perfil de custos para agentes de longo horizonte.
  Tradução do inglês:长程 Agent 的成本档案──
