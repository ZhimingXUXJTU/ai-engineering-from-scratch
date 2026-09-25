# FinOps para LLM  Economia Unitaria e Atribuição de Multi-Tenant  FinOps de LLM  Unidade Econômica e Multi-Arrentador

> As FinOps tradicionais rompem com os gastos de LLM. Os custos são transações de token, não recursos de uptime. Tags não mapeam  uma chamada de API é uma transação, não um ativo. As decisões de engenharia (design de urgência, janela de contexto, comprimento de saída) são decisões financeiras. O playbook de 2026 tem três dimensões de atribuição ao instrumento no primeiro dia: por usuário (`user_id`) para o preço dos assentos e a expansão, por tarefa (`task_id`+ `route`) para o custo e a prioridade da superfície do produto, per tenente (`tenant_id`) para a economia unitária e a renovação. Quatro camadas de tokens  prompt, ferramenta, memória, resposta  um balde de esconderijos gastam. Escala de execução para produtos multi-arrendatários: limites de taxas por arrendatário (2-3x o pico esperado, limpo 429 + retest-after); limite de gastos diários (1,5-3x o limite contratado; desencadeia aperto de taxas + alerta); interruptores de apagão no gasto z-score > 4 (pausa automática + página em chamada). Padrões de atribuição: tag-and-aggregate, telemetria-joiner (trace-ID → faturamento; maior precisão), amostragem e extrapolação, alocação baseada em modelo, streaming em tempo real. Metrica unitária: custo por consulta resolvida, custo por artefato gerado  não tokens $/M. A etiquetação retroativa sempre falha; instrumento de criação a pedido.

> **【中文解读】** Tradicional FinOps em LLM  gastos falhou  custo é Token 交易而非资源运行时间──工程决策──提示设计、上下文窗口、输出长度) 提示设计、上下文窗口、输出长度) 提示输出长度) 提示设计、上下文窗口、输出长度) 提示2026年Playbook 建议在第一天就建立三个归因维度:按用户,按任务,按租户──四个 Token 层──提示、工具、单位记忆、响应) não pode ser agrupada em um barril──标标应为"每次解决的查询成本",而不是"每百万 Token 成本"──

> **【拓展：FinOps → LLM 成本优化】**Em aplicações de LLM, o controle de custos é um desafio central. O programa de gestão de custos é um processo de desenvolvimento de projetos de gestão de custos.

**Type:** Learn | **类型:** 学习
**Languages:** Python (stdlib, toy cost-attribution simulator with kill switch) | **语言:** Python
**Prerequisites:** Phase 17 · 13 (Observability), Phase 17 · 14 (Caching) | **前置知识:** Phase 17 · 13 (Observability), Phase 17 · 14 (Caching)

> - Não .**【前置】**学本节前请先掌握:Fase 17·13(可观测性)、Fase 17·14(缓存)、云 FinOps 基础。LLM FinOps = 传统 FinOps 失效后的新方法。
> - Não .**【类比】**LLM FinOps = "按用收费的水电费"──传统 FinOps = 按服务器 uptime(标签=资产);LLM FinOps = 按代币交易(标签=交易)──三大归因维度(1 day-one 必埋):por-user(席位定价)、per-task(product cost)、per-tenant(单位经济)──四层代币(prompt/tool/memory/response)
> ️ **【易错点】**单位指标使用 $/M tokens 是错的,应使用"每次解决查询的成本"──强制阶梯:限流(2-3x 峰值)→日上限(1.5-3x 合约)→ kill switch(z-score>4 自动暂停)──
**Time:** ~60 minutes | **时间:** ~60 minutes

## Objetivos de aprendizagem

- Explique por que as FinOps tradicionais (tags + tiers) rompem com o gasto LLM e nomeie as três novas dimensões de atribuição.
  Tradução do inglês para Chinês: explica por que a tradição FinOps (Legio de Pós-Graduação) não funciona no gasto de LLM, e diz que há três novas dimensões.
- Enumere as quatro camadas de token (prompt, ferramenta, memória, resposta) e por que a faturamento de um único balde oculta o custo.
  Chinese: 列举四个标识层 (四个标识层) 提示、工具、记忆、响应),以及为什么单桶计费产生误导──
- Desenhar uma escada de aplicação (taxa → limite de gastos → interruptor de eliminação) para um produto multi-arrendatário.
  Tradução do inglês para tradução do inglês: design execution阶梯(速率 -> 支出上限 -> 断开关) para uso em vários serviços de LLM.
- Escolha uma métrica unitária (custo por consulta / artefato resolvido) em vez de tokens $ / M.
  Chinese: 选择单位指标 (), em vez de tokens de $/M.

## O problema é o problema da introdução

> **【中文解读】** Tradicional FinOps na LLM  despesas falha causa central: LLM Cumpração é token 交易而不是资源运行时间──标签(tags) não pode ser diretamente mapeadoAPI 调用是交易而非资产──工程决策(提示设计、上下文窗口、输出长度) é a decisão financeira── sua conta mostra US$40.000, mas você não sabe: qual inquilino gastou quanto, quais produtos, funções driven utility abuse 、 é rápido 膨胀还是工具调用还是记忆放大导致──

A sua conta diz 40.000 dólares.
- Que inquilino a gastou.
- Que característica do produto a levou.
- Se qualquer utilizador individual foi abusador.
- Se a inflamação rápida, as chamadas de ferramentas ou a amplificação da memória foi o culpado.

Tag-and-aggregate no lado do provedor funciona para recursos de nuvem (EC2, S3) onde as tags se propagam para itens de linha. Chamadas LLM API não são auto-tagadas  você tem que estampar usuário / tarefa / inquilino no site da chamada e levar a cabo. Atribuição retroativa sempre perde casos de borda.

## O conceito central.

### Três dimensões de atribuição

**Per-user**(`user_id`): quem está a custar o que.

**Per-task**(`task_id`+ `route`Os drives apresentam prioridades, decisões sobre características de morte e custo.

**Per-tenant**(`tenant_id`): qual cliente é rentável.

O instrumento todos os três no local de chamada no primeiro dia.

### Quatro camadas simbólicas

| Layer | Example | Typical % of total |
|-------|---------|---------------------|
| Prompt | system + user input | 40-60% |
| Tool | tool-call results fed back | 20-40% (agent workloads) |
| Memory | prior conversation / retrieved docs | 10-30% |
| Response | model output | 10-30% |

A combinação de todos os quatro faz com que a otimização se torne cega.

### Escada de execução

> **【中文解读】**Dois tipos de produtos de aluguel são obrigatórios: 1) Limitar a taxa de pagamento  Por aluguel 2-3x                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                 

> **【拓展：LLM FinOps 的复合优化栈】**O resultado da superposição é: 1) L2 (Fase 17·14) 10x mais barato de entrada; 2) L2 (Fase 17·15) 50% de desconto; 3) L2 (Fase 17·16) 60% de custo reduzido; 4) 网关效率 (Fase 17·19) 冗余 + 重试――全 (Fase 17·14) 10% de total superposição 

1. **Rate limit**- O número de inquilinos é de 2 a 3 vezes o máximo esperado.`Retry-After`O inquilino vê fricção, não há conta de surpresa.

2. **Daily spend cap**O limite de taxa de aperto + alerta de sucesso do cliente.

3. **Kill switch**Em termos de pontuação z de gastos > 4 em relação à linha de base do inquilino.

### Padrões de atribuição

- **Tag-and-aggregate**As informações sobre o processo de elaboração de dados são:
- **Telemetry joiner**A maior precisão, o que as equipes maduras fazem.
- **Sampling + extrapolation**A taxa de desemprego é de 5 a 10% e a taxa de desemprego é de 5 a 10%.
- **Model-based allocation**Para dados legais sem etiquetas.
- **Event-sourced**O custo é o resultado de eventos em um fluxo (Kafka/Kinesis).
- **Real-time streaming**: actualizações do painel de instrumentos subsegundo.

### O custo por X é a métrica unitária

> **【中文解读】**Os tokens $/M são um idioma fornecedor. Os indicadores de produtos devem ser: 1) Cada solução é suportada por um único custo; 2) Cada custo de produção; 3) Cada custo de tarefa de um agente bem sucedido; 4) Cada usuário vai ter um minuto de custo.

Os tokens $/M são vendedores.

- Custo por bilhete de apoio resolvido.
- Custo por artigo gerado.
- Custo por tarefa de agente bem sucedida.
- Custo por minuto de sessão de utilizador.

A ligação do custo ao resultado do produto, caso contrário, a otimização não é corrigida.

### Forma de rastreamento da atribuição de custos

```
trace_id: abc123
  user_id: u_42
  tenant_id: t_7
  task_id: task_classify_doc
  route: model_haiku
  layers:
    prompt_tokens: 1800
    tool_tokens: 600
    memory_tokens: 400
    response_tokens: 150
  cost_usd: 0.0135
  cached_input: true
  batch: false
```

Emite em cada chamada. Armazenar em data lake. Agregado por dimensão. Fase 17 · 13 observabilidade stack é onde esta vive.

### A pilha de poupanças compostas

Stack: cache + batch + rota + gateway.
- Cache L2 (Fase 17 · 14): entrada ~10 vezes mais barata.
- Batch (Fase 17 · 15): desconto de 50%.
- Rota para modelo barato (fase 17 · 16): redução de custos de 60%.
- Eficiência do gateway (fase 17 · 19): redundância + retestes.

O melhor caso empilhado: ~ 5-10% da linha de base ingênua. A maioria das equipes tem 2-3 alavancas envolvidas; poucos empilham todas as quatro.

### Números que você deve lembrar

- Dimensões de atribuição: por utilizador, por tarefa, por inquilino.
- Quatro camadas de símbolo: prompt, ferramenta, memória, resposta.
- Desligação de disparos: gastar pontuação z > 4.
- Metrica unitária: custo por consulta resolvida, não tokens $/M.
- Optimizações em pilhas: ~ 5-10% da linha de base possível.

## Use-o com o framework implementado.
```figure
i4-spend-ladder
```

## Usá-lo

`code/main.py`Simula um serviço de LLM para vários inquilinos com a escada de execução de três níveis. Injeta um inquilino abusivo e demonstra o disparo do interruptor de morte.

> `code/main.py`Simula um serviço de LLM para vários inquilinos com a escada de execução de três níveis. Injeta um inquilino abusivo e demonstra o disparo do interruptor de morte.

> `code/main.py`Simula um serviço de LLM para vários inquilinos com a escada de execução de três níveis. Injeta um inquilino abusivo e demonstra o disparo do interruptor de morte.

## Envia-o . Produto .

Esta lição produz`outputs/skill-finops-plan.md`- Tendo em conta o produto e a escala, desenha o esquema de atribuição e a escada de execução.

> 本课产 出 `outputs/skill-finops-plan.md`- Tendo em conta o produto e a escala, desenha o esquema de atribuição e a escada de execução.

## Exercícios.

1. Corra .`code/main.py`Em que ponto do "s" o interruptor de morte dispara?
   Tradução: 运行`code/main.py`Como é que podemos evitar erros de comunicação?
2. Desenhe um painel de custos por inquilino, por tarefa.
   Chinese Language Translation: Design per rent户, per task de custo instrumental board. Você primeiro construiu quais 5 visões?
3. O teu maior inquilino é negativo por unidade econômica, e propõe três intervenções por impacto do cliente.
   Chinese Translation: 你最大的租户单位经济学为负. Propôs três medidas de intervenção em função do ranking.
4. Calcula o custo por bilhete resolvido para um produto de suporte: 3M tokens/bilhete, ~800 bilhetes/dia, taxa em cache GPT-5.
   Chinese Translation: calcular suportar produtos de cada solução de um só custo de trabalho: 3M tokens/工单, cerca de 2,5 vezes重试――单位经济学可行吗?
5. Argumentem se a etiquetação retroativa pode funcionar.

## Termos-chave .

| Term | What people say | What it actually means |
|------|----------------|------------------------|
| Per-user attribution | "user-level cost" | `user_id` stamped on every call |
| Per-task attribution | "feature cost" | `task_id` + `route` identify product surface |
| Per-tenant attribution | "customer cost" | `tenant_id`; drives unit economics |
| Four token layers | "cost layers" | prompt + tool + memory + response |
| Rate limit | "429 guard" | Per-tenant ceiling enforced at gateway |
| Daily spend cap | "daily ceiling" | Tenant-scoped budget with alert |
| Kill switch | "auto-pause" | Spend z-score > 4 triggers auto-suspension |
| Cost per resolved | "product unit metric" | Cost tied to product outcome, not tokens |
| Telemetry joiner | "trace-to-billing" | Highest-accuracy attribution pattern |
| Stacked optimization | "cache+batch+route+gateway" | Compounding savings to ~5-10% baseline |

## Mais leitura 延伸阅读

- [FinOps Foundation — FinOps for AI Overview](https://www.finops.org/wg/finops-for-ai-overview/)
- [FinOps School — Cost per Unit 2026 Guide](https://finopsschool.com/blog/cost-per-unit/)
- [Digital Applied — LLM Agent Cost Attribution 2026](https://www.digitalapplied.com/blog/llm-agent-cost-attribution-guide-production-2026)
- [PointFive — Managed LLMs in Azure OpenAI](https://www.pointfive.co/blog/finops-for-ai-economics-of-managed-llms-in-azure-open-ai)
