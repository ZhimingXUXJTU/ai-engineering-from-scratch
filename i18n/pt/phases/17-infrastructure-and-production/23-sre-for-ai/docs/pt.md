# SRE para IA  Responsas a Incidentes de Multidistribuição, Runbooks, Detecção Preditiva 

> A AI SRE utiliza LLM baseados em dados de infraestrutura (logs, runbooks, topologia de serviços) através do RAG para automatizar as fases de investigação, documentação e coordenação. O padrão de arquitetura de 2026 é a orquestração de vários agentes  agentes especializados (logs, métricas, runbooks) coordenados por um supervisor; A IA propõe hipóteses e consultas, os seres humanos aprovam chamadas de julgamento. Datadog Bits AI e Azure SRE Agent enviam isto como produtos gerenciados. Os runbooks estão evoluindo: NeuBird Hawkeye usa avaliação adversária (dois modelos analisam o mesmo incidente; acordo = confiança, desacordo = incerteza); a memória operacional persiste em todas as mudanças da equipe. A auto-remediação permanece cautelosa: a IA sugere, os seres humanos aprovam. A ação totalmente autónoma é estreita (pod de reinicialização, implantação específica de retorno) com guardrails apertados  qualquer pessoa vendendo "set it and forget it" está supervendendo. Fronteira emergente: previsão pré-incidente. A pesquisa do MIT relata que um LLM treinado em registros históricos + tempos de GPU + padrões de erro de API prevê 89% das interrupções 10-15 minutos antes. Projeção: 95% dos LLM em empresas já têm uma falha automática até o final de 2026.

> **【中文解读】**Este capítulo apresenta a SRE  prática LLM  serviço de AI  estação de confiabilidade engenharia metodologia ⋅


**Type:** Learn | **类型:** 学习
**Languages:** Python (stdlib, toy multi-agent incident triage simulator) | **语言:** Python
**Prerequisites:** Phase 17 · 13 (Observability), Phase 17 · 24 (Chaos Engineering) | **前置知识:** Phase 17 · 13 (Observability), Phase 17 · 24 (Chaos Engineering)

> - Não .**【前置】**學本节前请先掌握:Fase 17·13(可观测性) ‧Fase 17·24(混沌工程) ‧SRE 基础(runbook/incident 响应) ‧AI SRE = LLM 加持的故障响应──
> - Não .**【类比】**AI SRE = "AI 急诊医生"。多 Agent 编排:日志 Agent+指标 Agent+runbook Agent 协调;AI 提假设+查日志,人类批准判断。Datadog Bits AI、Azure SRE Agent 是托管产品。NeuBird Hawkeye 用对抗评估(两模型同分析事件,一致=高置信)。自动修复保持谨慎:AI 建议+人批准。前沿:预故障预测(MIT 用历史日志+GPU 温度+API 错误提模式预测 89% 故障 10-15 分钟)。
**Time:** ~60 minutes | **时间:** ~60 minutes

## Objetivos de aprendizagem

- Diagrama da arquitetura multi-agente AI SRE: supervisor + agentes especializados (logs, métricas, runbooks) + portal de aprovação humana.
  Tradução do inglês para tradução do inglês: 図制多 Agent AI SRE 架构: 主管 + 专业 Agent (日志、指标、运行手册)
- Explique por que a remediação automática é limitada (capsula de reinicialização, reimplementação reversa) e não ampla (serviço de rearquitetura).
  Tradução do inglês para tradução do inglês para tradução do inglês para tradução do inglês para tradução do inglês para tradução do inglês para tradução do inglês para tradução do inglês para tradução do inglês para tradução do inglês para tradução do inglês para tradução do inglês para tradução do inglês para tradução do inglês para tradução do inglês para tradução do inglês para tradução do inglês para o inglês para tradução do inglês para o inglês para tradução do inglês para o inglês para o inglês para tradução do inglês para o inglês para o inglês para o inglês para o inglês para o inglês para o inglês para o inglês para o inglês para o inglês para o inglês para o inglês para o inglês para o inglês para o inglês para o inglês para o inglês para o inglês para o inglês para o inglês para o inglês para o inglês para o inglês para o inglês para o inglês para o inglês para o inglês para o inglês para o inglês para o inglês para o inglês para o inglês.
- Nomear o padrão de avaliação adversária (NeuBird Hawkeye): dois modelos concordam = confiança; discordar = escalada.
  Tradução do inglês para tradução inglesa: ︎-︎-︎-︎-︎-︎-︎-︎-︎-︎-︎-︎-︎-︎-︎-︎-︎-︎-︎-︎-︎-︎-︎-︎-︎-︎-︎-︎-︎-︎-︎-︎-︎-︎-︎-︎-︎-︎-︎-︎-︎-︎-︎-︎-︎-︎-︎-︎-︎-︎-︎-︎-︎-︎-︎-︎-︎-︎-︎-︎-︎-︎-︎-︎-︎-︎-︎-︎-︎-︎-︎-︎-︎-︎-︎-︎-︎-︎-︎-︎-︎-︎-︎-︎-︎-︎-︎-︎-︎-︎-------------------------------------------------------------------------------------------------------------------
- Cite o resultado de detecção precoce do MIT 89% e a restrição operacional: as previsões sem ativação são apenas painéis de controle.
  Chinese Translation: Citation MIT 89% 早期检测结果和运维约束:无历史基线的预测不可行──

## O problema é o problema da introdução

> **【中文解读】**O AI SRE tem uma visão central: em 2026, o primeiro 20 minutos da investigação de eventos foram automatizados, conforme o serviço, distribuindo o seu diário, conectando-se à implementação recente, combinando o seu runbook com o RAG +  ferramentas.

> **【拓展：AI SRE 产品市场】**2026 ano AI SRE  produtos:(1) Datadog Bits AIDatadog  interno de gestão SRE copiloto;(2) Azure SRE AgenteAzure 原生;(3) NeuBird Hawkeye对抗性评估(两个模型独立分析同一事件,一致=高置信,不一致=升级) + 操作记忆(post-mortem 存入向量 DB);(4) PagerDuty AIOps分类 + 去重;5)(Incident.io Autopilot事件指挥官 + 协调。MIT 2025 Pesquisas mostram, GPULLM em 历史志 + 温度 + API 错误模式训练,可在 10-15 分钟前预测机停机89% .

Um engenheiro em chamada recebe um sinal às 3 da manhã "Alta taxa de erro na caixa de pagamento". Eles verificam Datadog, Loki, três livretes de execução, o registro de implantação. 30 minutos depois percebem que a causa raiz é um OOM vLLM de um cache de KV. Eles reiniciar a cápsula; erro limpo.

Em 2026 os primeiros 20 minutos dessa investigação são automatizados. Grupar registros por serviço, correlacionando com implantações recentes, combinando com runbooks  todos são RAG + uso de ferramentas. Um agente supervisionado pode fazer triagem de primeira passagem e apresentar uma hipótese antes que o humano abra Datadog.

A remediação totalmente autônoma é um problema diferente. Reiniciar a cápsula: seguro. Polaridade de GPU: seguro se a política permitir. Rearquitar o serviço: absolutamente não. A disciplina está desenhando a linha estreita.

## O conceito central.

### Arquitetura multi-agente

> **【中文解读】**架构:Supervisor 将事件分为查询,分派给专业化 Agent(日志 Agent 搜索日志、指标 Agent 查询 PromQL、Runbook Agent 检索文档) Supervisor 综合,向人类呈现假设 + 证据──人类批准或重定向──安全自动修复范围:重启 Pod、回滚特定部署、在预批准范围内扩展池──不安全范围:更改服务拓、更改资源限制、部署新代码、更改 IAM──

```
          Incident
             │
             ▼
        Supervisor
        /    |    \
       ▼     ▼     ▼
  Log agent  Metric agent  Runbook agent
       │     │     │
       └─────┴─────┘
             │
             ▼
        Hypothesis + evidence
             │
             ▼
        Human approval
             │
             ▼
        Action (narrow set)
```

O supervisor divide o incidente em sub-queries. Agentes especializados têm acesso a ferramentas (busca de registro, PromQL, recuperação de documentos).

### Ámbito de aplicação da remediação automática

> **【拓展：AI SRE 自动修复的安全边界】**AI SRE Automatic Modification of Security Borders (AI SRE Automatic Modification) Segurança (AI SRE Automatic Modification) Reboot Pod、回滚特定部署、在预批准范围内扩展池、启用预批准功能旗──不安全(广范围) 改进服务拓、改进资源限制、部署新代码、改进 IAM、改进数据库── Qualquer fornecedor que afirma que "set up after we forget" está em excesso de compromisso com segurança.

**Safe (narrow)**: reiniciar a cápsula, reverter a implantação específica, agrupar a escala dentro dos limites pré-aprovados, ativar a bandeira de características pré-aprovada.

**Not safe (broad)**A Comissão propõe que a Comissão adopte um novo regulamento relativo à aplicação do código de base.

Quem vende "set it and forget it" está a vender demais. O set de segurança cresce à medida que a AI SRE amadurece, mas o limite é real.

### Avaliação adversária (NeuBird Hawkeye)

Dois modelos analisam o mesmo incidente de forma independente. Se concordarem sobre a causa raiz, a confiança é alta. Se discordarem, escalam para humanos com ambas as hipóteses visíveis. Padrão simples, filtro eficaz contra causas raiz alucinadas.

### Memória operacional

O turnover de equipe é a morte silenciosa das folhas tradicionais de conhecimento tribal SRE. A AI SRE armazena runbooks + post-mortems em um vector DB; agentes recuperam em cada novo incidente. Quando novos engenheiros se juntam, a AI tem história completa.

### Previsão de incidentes

Pesquisa MIT 2025: LLM treinado em registros históricos, temperaturas de GPU, padrões de erro API previu 89% de interrupções 10-15 minutos antes de acontecerem no conjunto de testes.

Verificação da realidade: as previsões sem ativação são painéis de controle. A pergunta operacional é "quando nós predizemos, o que fazemos?" Desgaste preventivo? Pager? Auto-escalada? A resposta é específica da política.

### Produtos em 2026

- **Datadog Bits AI**- O co-piloto da SRE no Datadog.
- **Azure SRE Agent**- Nativo de Azure.
- **NeuBird Hawkeye** Avaliação adversária + memória operacional.
- **PagerDuty AIOps** triagem + deduplicação.
- **Incident.io Autopilot**- Comandante de incidentes + coordenação.

### Livros de execução como código

> **【拓展：AI SRE 实施路径】**1) primeiro, implementar um runbook não estruturado 转换为结构化标注down symptoms 假设 验证、行动; 2) implementar uma avaliação de resistência  dois modelos independentes de análise do mesmo evento; 3) estabelecer uma memória de operação  post-mortem + runbook 存入向量 DB; 4) começar com "AI 建议人类批准", não saltar diretamente para uma acção autónoma; 5) pré-evento pré-evento 预测MIT estudos mostram 10-15 minutos de pré-evento, mas "pre-evento depois de fazer" estratégia definição  pré-evento?

Os runbooks evoluem de páginas de Confluence para marcas de versão com seções estruturadas (símbolo, hipótese, verificação, ato).

### Números que você deve lembrar

- Detecção precoce do MIT: 89% de interrupções, tempo de liderança de 10-15 minutos.
- Classificação multi-agente: supervisor + (registros, métricas, runbooks) + humano.
- Set de remediação automática segura: reinicialização da cápsula, reimplementação, escala dentro dos limites.
- Avaliação adversária: dois modelos independentes; acordo = confiança.

## Use-o com o framework implementado.
```figure
i4-incident-agents
```

## Usá-lo

`code/main.py`Simula uma triagem de vários agentes: o agente de registro encontra erro, o agente métrico encontra spike da CPU, o agente do runbook corresponde a um problema conhecido.

> `code/main.py`Simula uma triagem de vários agentes: o agente de registro encontra erro, o agente métrico encontra spike da CPU, o agente do runbook corresponde a um problema conhecido.

> `code/main.py`Simula uma triagem de vários agentes: o agente de registro encontra erro, o agente métrico encontra spike da CPU, o agente do runbook corresponde a um problema conhecido.

## Envia-o . Produto .

Esta lição produz`outputs/skill-ai-sre-plan.md`Dada a atualidade de chamada, o volume de incidentes, a maturidade da equipa, desenha uma implantação de SRE.

> 本课产 出 `outputs/skill-ai-sre-plan.md`Dada a atualidade de chamada, o volume de incidentes, a maturidade da equipa, desenha uma implantação de SRE.

## Exercícios.

1. Corra .`code/main.py`E se os agentes registos e métricos discordarem?
   Tradução: 运行`code/main.py`Se o agente não concordar, como será que o director vai arbitrar?
2. Defina três ações de auto-remediamento "seguras" para o seu serviço.
   Por sua vez, o governo não pode fazer nada para o governo.
3. Escrever um modelo estruturado de runbook: seções, campos exigidos, comandos de verificação.
   Tradução do inglês para o português: 编写结构化运行手册模板:章节、必填字段、验证命令──
4. Que é a sua política?
   O que é que você está fazendo?
5. Argumentar se uma equipe de 3 pessoas deve adotar a AI SRE em 2026 ou esperar.

## Termos-chave .

| Term | What people say | What it actually means |
|------|----------------|------------------------|
| AI SRE | "agent for on-call" | LLM-backed incident investigation + coordination |
| Supervisor agent | "the orchestrator" | Top-level agent breaking incidents into sub-queries |
| Specialized agent | "domain agent" | Sub-agent with tool access (logs, metrics, runbooks) |
| Auto-remediation | "AI fixes it" | Narrow pre-approved action; NOT broad re-architecture |
| Operational memory | "vector runbooks" | Post-mortems + runbooks in vector DB for RAG |
| Adversarial eval | "two-model check" | Independent analyses; agreement = confidence |
| NeuBird Hawkeye | "the adversarial one" | Product with adversarial-eval + memory pattern |
| Bits AI | "Datadog's SRE agent" | Datadog-managed AI SRE |
| Pre-incident prediction | "early detection" | 10-15 min lead time on outage prediction |

## Mais leitura 延伸阅读

- [incident.io — AI SRE Complete Guide 2026](https://incident.io/blog/what-is-ai-sre-complete-guide-2026)
- [InfoQ — Human-Centred AI for SRE](https://www.infoq.com/news/2026/01/opsworker-ai-sre/)
- [DZone — AI in SRE 2026](https://dzone.com/articles/ai-in-sre-whats-actually-coming-in-2026)
- [Datadog Bits AI](https://www.datadoghq.com/product/bits-ai/)
- [NeuBird Hawkeye](https://www.neubird.ai/)
- [awesome-ai-sre](https://github.com/agamm/awesome-ai-sre)
