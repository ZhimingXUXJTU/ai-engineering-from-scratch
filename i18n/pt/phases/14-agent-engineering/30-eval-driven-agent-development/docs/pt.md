# Desenvolvimento de Agentes Eval-Driven  Desenvolvimento  Driven  Avaliação

> A orientação da Anthropic: "comece com pedidos simples, otimize-os com avaliação abrangente e adicione sistemas agenciários em várias etapas apenas quando necessário". A avaliação não é o último passo.

**Type:** Learn + Build | **类型:** 构建
**Languages:** Python (stdlib) | **语言:** Python (标准库)
**Prerequisites:** All of Phase 14. | **前置知识:** 见原文
**Time:** ~60 minutes | **时间:** 见原文

> - Não .**【前置】**O que é que é o "failure mode" do "failure mode" é uma "prevenção" para o "failure mode"?

## Objetivos de aprendizagem

- Nomear as três camadas de avaliação  referências estáticas, offline personalizada, produção on-line  e para o que cada uma é para.
- Explica o ciclo apertado do avaliador-optimizador.
- Descrever as melhores práticas para 2026: avaliações ao lado do código, executadas em CI, gate PRs.
- Conecte cada lição da Fase 14 ao caso de avaliação que gera.

## O problema é o problema da introdução

Os agentes passam por demonstrações. Eles falham na produção de maneiras que as demonstrações não podem prever. Os indicadores de referência respondem "este modelo é amplamente capaz?" não "este agente está enviando os patches certos para o meu produto?" A resposta: avaliação em três camadas, executando continuamente, com cada guarda-roupa e regra aprendida mapeada para um caso de avaliação.

> - Não .**【类比】**O agente eval 像给运动员做体检3 个层级:(1) **静态基准**(SWE-bench、BFCL) =国家体能测试,比平均水平;**定制离线 eval**= para o seu projeto de design (((como "a taxa de sucesso de "reconstruir este bug") = treinamento em equipe;(3) **在线生产 eval**= verdadeiro usuário = A/B 测试──三层缺一不可只看基准会过适应,只看生产反周期太长──

> ️ **【易错点】**O agente eval de 3 个坑:(1) **只测 happy path**eval 集全是简单查询, complexa situação não cobre;务必构构建对抗性 测试(模糊指令、攻击、边界值)**eval 不进 CI** desenvolvimento时手工跑一次就过,上线后没人跑;eval 必须进 GitHub Actions,PR 不过 eval 不能合并──(3) **eval 集污染**eval dados misturados em seguida de alguns tiros exemplo,分数虚高;eval dados rigoroso isolação。

> O agente passou por uma demonstração. Eles falharam de forma imprevisível na produção. O ponto de partida é "O modelo tem capacidade ampla?" ao invés de "O agente está a entregar o remédio correto para o meu produto?" A resposta é: avaliação de três níveis, funcionamento contínuo, cada cuidado e regras de aprendizagem são mapeadas em um exemplo de avaliação.


> **【中文解读】**评估驱动的代理 开发(Eval-Driven Development) será o TDD no engenho de software tradicional  aplicado ao Agente:predefinir os critérios de avaliação, reimplementar o Agente。 O desafio central é a incerteza do Agente As mesmas entradas podem produzir diferentes rotas de execução e saídas, necessitam de avaliação baseada em trilhas e não em avaliações baseadas em rápidos照──

> **{【拓展：Eval-Driven Agent Development 是 2025-2026 年的最佳实践。核...】}**O desenvolvimento de agentes Eval-Driven é a melhor prática de 2025-2026: 1) Ops Agente Tracking and Assessment Platform; 2) O LangSmith LangChain Assessment Kit; 3) Braintrust AI Assessment Framework; Key Insight:A avaliação de agentes deve ser baseada em uma trajetória completa (trájetória) e não em uma saída final.
## O conceito central.

### Três camadas de avaliação

1. **Static benchmarks** SWE-bench Verificado para código (Lessão 19), WebArena/OSWorld para navegação / desktop (Lessão 20), GAIA para generalista (Lessão 19), BFCL V4 para uso de ferramentas (Lessão 06). Uso para comparação entre modelos e gating de regressão. Contaminação é real: SWE-bench+ encontrou vazamento de solução de 32,67%.

2. **Custom offline evals** a forma do seu produto:
   - LLM como juiz (Langfuse, Phoenix, Opik  Lição 24).
   - Baseado em execução (exercer o corrector, testes de verificação).
   - Baseada em trajetória (comparar sequências de ação contra o ouro; OSWorld-Human mostra agentes superiores 1,4-2,7x sobre o ouro).

3. **Online evals** produção:
   - Repetições de sessão (Langfuse).
   - Alertas activadas por guarda-pista (Lessão 16, 21).
   - Per-passo de rastreamento de custos / latência (Lessão 23 OTel abrangem).

### Otimizador de avaliação (antrópico)

O circuito apertado:

1. O proponente gera saída.
2. Jueiros de avaliação.
3. Refinem até o avaliador passar.

Este é o Auto-Refino (Lessão 05) generalizado. Qualquer fluxo de agentes que você se importa pode envolver em avaliador-optimizador para confiabilidade.

> É a generalização da Auto-Refinação. Qualquer processo de Agente que você se preocupe pode ser usado em um avaliador-optimizador para aumentar a confiabilidade.

> 评估驱动的代理 开发(Eval-Driven Development) será avaliada como o núcleo do desenvolvimento de um agente 

### 2026 melhores práticas

- Os Evals vivem ao lado do código.
- - É um bom trabalho.
- A combinação de gate em pontuações de eval (por exemplo, "sem regressão > 5% vs principal").
- Cada guarda-redes faz um mapa para um caso de avaliação.
- Cada regra aprendida (Reflexão, regra de aprendizagem pró-fluxo de trabalho) mapeia um caso de falha.

### A ligação da fase 14

Cada lição da Fase 14 gera casos de avaliação:

| Lesson | Eval case it generates |
|--------|------------------------|
| 01 Agent Loop | Budget-exhausted, infinite-loop guard |
| 02 ReWOO | Planner replans correctly when a tool fails |
| 03 Reflexion | Learned reflections apply on retry |
| 05 Self-Refine/CRITIC | Judge passes refined output |
| 06 Tool Use | Argument coercion works; unknown tools rejected |
| 07-10 Memory | Retrieval citations match sources; stale facts invalidate |
| 12 Workflow Patterns | Each pattern produces correct output |
| 13 LangGraph | Resume reproduces state exactly |
| 14 AutoGen Actors | DLQ catches crashed handlers |
| 16 OpenAI Agents SDK | Guardrail trips on the right inputs |
| 17 Claude Agent SDK | Subagent results return to orchestrator |
| 19-20 Benchmarks | SWE-bench Verified score, WebArena success rate, OSWorld efficiency |
| 21 Computer Use | Per-step safety catches injected DOM |
| 23 OTel | Spans emit required attributes |
| 26 Failure Modes | Detectors tag known failures |
| 27 Prompt Injection | PVE refuses poisoned retrievals |
| 28 Orchestration | Supervisor routes to the right specialist |
| 29 Runtime Shapes | DLQ handles N% failure |

Se a sua equipa de avaliação tiver casos para cada um, já cobriu a Fase 14.

> Se o teu conjunto de avaliação tiver um exemplo de uso de cada aula, já cobres a Fase 14.

> 评估驱动的代理 开发(Eval-Driven Development) será avaliada como o núcleo do desenvolvimento de um agente 

### Quando o desenvolvimento orientado pela avaliação falhar

- **No baseline.**Evals sem o último bom conhecido são ilegíveis.
- **LLM-judge without grounding.**O padrão crítico (Lessão 05)  julgar fundamentos em ferramentas externas.
- **Over-fitting to evals.**Otimizar para a avaliação diverge da utilidade da produção.
- **Flaky evals.**Casos não deterministas causam falsos alarmes.

> **没有基线。** não há avaliação de estado de bom estado conhecido é indispensável 
> **LLM 评审器没有基础。**评审器也会幻觉──CRITIC 模式(第 5 课) 评审器基于外部工具──
> **过拟合评估。**Para avaliar a optimização da produção e da utilização prática,
> **不稳定的评估。**Não-confiança de uso casos de erro de comunicação.

## Construí-lo e realizei-o.
```figure
ae-eval-three-layers
```

## Construí-lo

`code/main.py`é um arame de avaliação stdlib:

- Registro de casos com categorias (marca de referência, personalidade, on-line).
- Um agente com guião em teste.
- Localização de avaliação-otimizador: propor, julgar, refinar até passar ou rodadas máximas.
- Portão de CI: taxa de passagem agregada + regressão em relação à linha de base.

- É o que é ?

```
python3 code/main.py
```

Resultado: passagem/falha por caso, bandeira de regressão, veredicto da porta CI.

> 输出: cada caso de uso através/失败、归归标志、CI 门控裁定。

> 评估驱动的代理 开发(Eval-Driven Development) será avaliada como o núcleo do desenvolvimento de um agente 

## Use-o com o framework implementado.

- Escreva casos de avaliação no mesmo repo do seu código de agente.
- Controla-os em todas as relações públicas através de informadores.
- Falha na construção da regressão.
- Rate de passagem ao longo do tempo.
- Através de um novo caso, é possível que cada falha da produção seja relacionada a um novo caso.

## Envia-o . Produto .

`outputs/skill-eval-suite.md`Construirá uma suíte de avaliação de três camadas para um produto agente com portões de CI e rastreamento de regressão.

> `outputs/skill-eval-suite.md`Para a construção de produtos de agentes, três níveis de avaliação, incluindo CI e controle de regresso.

> 评估驱动的代理 开发(Eval-Driven Development) será avaliada como o núcleo do desenvolvimento de um agente 

## Exercícios.

1. Tome uma das falhas da produção, escreva um caso de avaliação que a reproduza.
  Tradução do inglês para tradução do inglês:
2. Construa uma rubrica de juiz de LLM para o seu domínio com três dimensões (factual, tone, scope).
  Tradução do inglês para tradução do inglês:
3. Enviar o conjunto de avaliação para CI. Falhar na construção de >=5% regressão.
  Tradução do inglês para tradução do inglês:
4. Adicione uma métrica de eficiência de trajetória: quantos passos o agente fez contra uma trajetória de ouro?
  Tradução do inglês para tradução do inglês:
5. Mapa de cada aula da Fase 14 para um caso de avaliação na sua suite.
  Tradução do inglês para tradução do inglês:

## Termos-chave .

| Term | What people say | What it actually means |
|------|----------------|------------------------|---|
| Static benchmark | "Off-the-shelf eval" | SWE-bench, GAIA, AgentBench, WebArena, OSWorld |  |
| Custom offline eval | "Domain eval" | LLM-as-judge / exec / trajectory on your product shape |  |
| Online eval | "Production eval" | Session replay, guardrail alerts, cost/latency tracking |  |
| Evaluator-optimizer | "Propose-judge-refine" | Iterate until judge passes |  |
| CI gate | "Merge blocker" | Fail the build on eval regression |  |
| Baseline | "Last-known-good" | Reference score to detect regression |  |
| Trajectory efficiency | "Steps over gold" | Agent step count divided by human expert minimum |  |

## Mais leitura 延伸阅读

- [Anthropic, Building Effective Agents](https://www.anthropic.com/research/building-effective-agents)"Comece simples, otimize com avaliações"
  Tradução do português:
- [OpenAI, SWE-bench Verified](https://openai.com/index/introducing-swe-bench-verified/) o índice de referência seleccionado
  Tradução do português:
- [Berkeley Function Calling Leaderboard](https://gorilla.cs.berkeley.edu/leaderboard.html) Indicador de referência de utilização de ferramentas
  Tradução do português:
- [Langfuse docs](https://langfuse.com/) avaliações + repetição de sessões na prática
  Tradução do português:
