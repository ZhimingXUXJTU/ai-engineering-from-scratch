# Tempo de execução da produção: fila, evento, cron  produção  operação  UE

> Agentes de produção executam em seis formas de tempo de execução: solicitação-resposta, streaming, execução duradoura, fundo baseado em fila, orientado por eventos e agendado. Escolha a forma antes de escolher o quadro.

**Type:** Learn | **类型:** 学习
**Languages:** Python (stdlib) | **语言:** Python (标准库)
**Prerequisites:** Phase 14 · 13 (LangGraph), Phase 14 · 22 (Voice) | **前置知识:** 见原文
**Time:** ~60 minutes | **时间:** 见原文

> - Não .**【前置】**學本節前 請先掌握:Fase 14·13(LangGraph) 状态图基础;Fase 17 ((Infraestrutura & Produção) 本节是其前置概念,深入生产部署看Fase 17 全部。

## Objetivos de aprendizagem

- Nomear as seis formas de execução da produção e combinar cada uma com um padrão de quadro / produto.
- Explique por que a execução duradoura (LangGraph) é importante para tarefas de longo prazo.
- Descreva o tempo de execução baseado no evento e quando Claude Managed Agents se encaixa.
- Explique a alegação de observabilidade como carga de carga para agentes em várias etapas.

## O problema é o problema da introdução

Agentes de produção falham de maneiras que um notebook Jupyter não aparece: o timeout da rede no passo 37, o usuário pendura a chamada de voz no meio, o trabalho cron morre no reinicio da máquina, o trabalhador de fundo fica sem memória. A forma de tempo de execução determina quais falhas são susceptíveis de sobreviver.

> O modo de falha do Agente de Produção é o de Jupyter  Notícias não podem ser mostradas: 37o passo de rede superhora, o usuário está ligado ao meio da conversação, a missão está determinada quando a máquina reinicia, a morte, a falta de memória no segundo tempo de funcionamento, o que determina quais falhas são recuperáveis, o que determina o estado de funcionamento.


> **【中文解读】**O agente de produção  Quando executado  Quando executado  Quando executado  Quando executado  Quando executado  Quando executado  Quando executado  Quando executado  Quando executado  Quando executado  Quando executado  Quando executado  Quando executado  Quando executado  Quando executado  Quando executado  Quando executado  Quando executado  Quando executado  Quando executado  Quando executado  Quando executado  Quando executado  Quando executado  Quando executado  Quando executado  Quando executado  Quando executado  Quando executado  Quando executado  Quando executado  Quando executado  Quando executado  Quando executado  Quando executado  Quando executado  Quando executado  Quando executado  Quando executado  Quando executado  Quando executado  Quando executado  Quando executado  Quando executado  Quando executado  Quando executado  Quando executado  Quando executado  Quando executado  Quando executado  Quando executado  Quando executado  Quando executado  Quando executado  Quando executado  Quando executado  Quando executado  Quando executado  Quando executado  Quando executado  Quando executado  Quando executado  Quando executado  Quando executado  Quando executado  Quando executado  Quando executado  Quando executado  Quando executado  Quando executado  Quando executado  Quando executado  Quando executado  Quando executado  Quando executado  Quando executado  Quando executado  Quando executado  Quando executado  Quando executado  Quando executado  Quando executado  Quando executado  Quando executado  Quando executado  Quando executado  Quando executado  Quando executado  Quando executado  Quando executado  Quando executado  Quando executado  Quando executado  Quando executado  Quando executado  Quando executado  Quando executado  Quando executado  Quando executado  Quando executado  Quando executado  Quando executado  Quando executado  Quando executado  Quando executado  Quando executado  Quando executado  Quando executado  Quando executado  quando  quando  quando  quando  quando o executado  quando  quando o executado  quando  quando  quando o executado  quando  quando  quando o executado  quando  quando  quando  quando  quando  quando  quando  quando  quando  executado  quando  quando  quando  quando  quando 

> - Não .**【类比】**6 种运行时 = 6 种交通工具:(1) **request-response**=出租车(一次一结,最简单);(2) **streaming**= 高铁(边走边看风景,token 流式);(3) **durable execution**=房车(sleeping awake to continue open, ponto de controlo LangGraph);(4) **queue-based**= Ltv Companhia (TSA), Celery/RQ;**event-driven**= plataforma de venda externa (事件触发,Claude Managed Agents);**scheduled**=钟(定时执行,cron) ・ tarefas多长多复杂决定选择哪个──

> ️ **【易错点】**运行时选错的 3 个坑:(1) **长任务用 request-response**3 小时任务挂 HTTP  请求,nginx 60s 超时切断; usando execução durável(LangGraph) + 后台轮询──(2) **observability 当可选**上线后发现"不知道为失败"; desde o primeiro dia em que entrou em contato com Langfuse/LangSmith, cada ferramenta é usada para rastrear──(3) **没做 graceful shutdown** serviço reiniciação quando está executando tarefas diretamente morte; usando SIGTERM 子 guardar checkpoint, reiniciação após checkpoint 续跑──

> **{【拓展：2026年生产 Agent 运行时的选择：(1) LangGraph Cloud——LangGrap...】}**2026 anos de produção Agente 运行时的选择:(1) LangGraph CloudLangGraph's托管服务,内置状态检查点和重放;(2) Temporal通用工作流引擎,配合AI SDK可构建持久化 Agent;(3) Autoconstrução baseada em Redis/Kafka's消息队列 +自定义 Agent 循环──
## O conceito central.

### Requisito-resposta

- HTTP sincrono. O usuário espera a conclusão.
- Apenas viável para tarefas curtas (< 30 anos).
- Estacas: Agno (Python + FastAPI), Mastra (TypeScript + Express/Hono/Fastify/Koa).
- Observabilidade: registos de acesso HTTP padrão + intervalos OTel.

### Transmissão

- SSE ou WebSocket para saída progressiva.
- O LiveKit estende isso ao WebRTC para voz/vídeo (Lessão 22).
- Stacks: qualquer framework com suporte de streaming + uma frontend que lida com SSE/WS.
- Observabilidade: tempo por peça, latença de primeiro token, latença de cauda.

### Execução duradoura

- O estado está em checkpoint após cada passo, resume automaticamente em caso de falha.
- O modelo de atores do AutoGen v0.4 isola falhas em um agente (Lessão 14).
- O diferenciador central do LangGraph (Lessão 13).
- É essencial quando o número de etapas é desconhecido e o custo de recuperação é elevado.

### Baseada em fila / fundo

- O trabalho entra em fila, os trabalhadores recolhem, os resultados fluem para trás através de webhooks ou pub/sub.
- Essenciais para agentes de longo horizonte (dezenas a centenas de passos por tarefa, por anúncio de uso do computador da Anthropic).
- Estacas: Celery (Python), BullMQ (Node), SQS + Lambda (AWS), personalizado.
- Observabilidade: profundidade da fila, distribuição de latência por trabalho, tamanho do DLQ.

### Evento-driven

- Agentes assinam os gatilhos: novo e-mail, aberta PR, fogo cron.
- Claude Managed Agents cobre isto fora da caixa (Lessão 17).
- Os fluxos de CrewAI (Lessão 15) estruturam fluxos de trabalho deterministas orientados por eventos.
- Observabilidade: fonte de desencadeamento, latência do evento para o início, latência do agente.

### Programação

- Agentes em forma de Cron que executam periodicamente.
- Combine com execução duradoura para que uma corrida noturna falha retoma na próxima vez.
- Stacks: Kubernetes CronJob + um framework durável; hospedado (Render cron, Vercel cron).

### Modelos de implantação em 2026

- **CrewAI Flows**para a produção orientada a eventos.
- **Agno**FastAPI sem estado para microsserviços Python.
- **Mastra**Adaptadores de servidor (Express, Hono, Fastify, Koa) para inserção.
- **Pipecat Cloud / LiveKit Cloud**para a voz gerenciada (Lessão 22).
- **Claude Managed Agents**para assincronização de longa duração hospedada.

### Observabilidade é suportável

Sem OpenTelemetry GenAI (Lessão 23) mais um Langfuse / Phoenix / Opik backend (Lessão 24), você não pode depurar um agente multi-passo que falhou na etapa 40.

> 没有 OpenTelemetry GenAI span(第 23 课)加上Langfuse/Phoenix/Opik 后端(第 24 课),you cannot调试在第 40 步失败的多步代理―― isso não é opcional para o ambiente de produção―― é a diferença entre "rápido调试" e "从头重放并添加更多日志"――

> O desenvolvimento de um sistema de gestão de custos e de gestão de custos, incluindo a gestão de estado, a recuperação de erros, a limitação de fluxo, a gestão de fileiras e o controlo de custos, é um dos principais factores de consideração.

### Quando os tempos de execução da produção falham

- **Wrong shape choice.**Escolher solicitações-resposta para uma tarefa de 5 minutos.
- **No DLQ.**Trabalhadores em fila sem letra morta.
- **Opaque background work.**Agente de fundo funciona sem rastro de exportação. falhas são invisíveis até o usuário relatá-los.
- **Skipping durable state.**Qualquer execução > 30 segundos em que não se pode permitir reiniciar requer execução duradoura.

> **错误的形态选择。**Por 5 minutos tarefas escolher solicitação-resposta.
> **没有 DLQ。**队列工作器没有死信队列──失败的任务消失──
> **不透明的后台工作。**后台 Agente 运行没有追踪导出――失败不可见直到用户报告――
> **跳过持久化状态。**Qualquer operação que exceda 30 segundos e não seja suportável para reiniciar é necessária uma execução duradoura.

## Construí-lo e realizei-o.
```figure
wb-runtime-shapes
```

## Construí-lo

`code/main.py`é uma demonstração multi-forma stdlib:

- O ponto final de resposta-requisito (função simples).
- Gestor de transmissão (generador).
- Trabalhador de fila com DLQ.
- Registro de desencadeamento de eventos.
- Agendador em forma de cron.

- É o que é ?

```bash
python3 code/main.py
```

Output: cinco traços mostrando o comportamento de cada forma na mesma tarefa. A mesma lógica do agente, diferentes conchas externas. A execução duradoura (a sexta forma) é intencionalmente coberta na lição 13 com o ponto de verificação LangGraph.

> 输出:五种追踪显示每种形态在同一任务上的行为――相同的代理 逻辑,不同的外──持久化执行――第六种形态) 有意在第13 课中通过 LangGraph 检查点覆盖――

> O desenvolvimento de um sistema de gestão de custos e de gestão de custos, incluindo a gestão de estado, a recuperação de erros, a limitação de fluxo, a gestão de fileiras e o controlo de custos, é um dos principais factores de consideração.

## Use-o com o framework implementado.

- **Request-response**para UX no estilo chat.
- **Streaming**para respostas progressivas.
- **Durable**para tarefas de longo prazo.
- **Queue**para lote / async / de longa duração.
- **Event**para a reactividade do agente.
- **Cron**para a manutenção da casa (consolidação de memória, avaliações, relatórios de custos).

## Envia-o . Produto .

`outputs/skill-runtime-shape.md`seleciona uma forma de execução para uma tarefa e fixa os requisitos de observabilidade.

> `outputs/skill-runtime-shape.md`Para tarefa de escolher um funcionamento, forma e conectar observação requisitos.

> O desenvolvimento de um sistema de gestão de custos e de gestão de custos, incluindo a gestão de estado, a recuperação de erros, a limitação de fluxo, a gestão de fileiras e o controlo de custos, é um dos principais factores de consideração.

## Exercícios.

1. Portar a sua lição 01 ReAct loop para todas as seis formas em sua pilha.
  Tradução do inglês para tradução do inglês:
2. Adicione um DLQ à demonstração baseada na fila. Simula 10% falha de trabalho; tamanho de DLQ de superfície.
  Tradução do inglês para tradução do inglês:
3. Escreva um agente de avaliação com cron que corre todas as noites contra os 20 principais vestígios do dia.
  Tradução do inglês para tradução do inglês:
4. Implementar o streaming com pressão de contração: se o cliente é lento, pause o agente. Como isso interage com um orçamento de turno?
  Tradução do inglês para tradução do inglês:
5. Quando é que mudas um agente de longo horizonte para o de gestão?
  Tradução do inglês para tradução do inglês:

## Termos-chave .

| Term | What people say | What it actually means |
|------|----------------|------------------------|---|
| Request-response | "Synchronous" | User waits; short tasks only |  |
| Streaming | "SSE / WS" | Progressive output; better UX; latency observable per chunk |  |
| Durable execution | "Resume from failure" | Checkpointed state; restart at last step |  |
| Queue-based | "Background jobs" | Producer / worker pool / DLQ |  |
| Event-driven | "Trigger-based" | Agent reacts to external events |  |
| DLQ | "Dead-letter queue" | Parking lot for failed jobs |  |
| Claude Managed Agents | "Hosted harness" | Anthropic-hosted long-running async with caching + compaction |  |

## Mais leitura 延伸阅读

- [LangGraph overview](https://docs.langchain.com/oss/python/langgraph/overview) Detalhes de execução duradoura
  Tradução do português:
- [Claude Managed Agents overview](https://platform.claude.com/docs/en/managed-agents/overview) acomodação de longa data
  Tradução do português:
- [Anthropic, Introducing computer use](https://www.anthropic.com/news/3-5-models-and-computer-use) "dezenas a centenas de passos por tarefa"
  Tradução do português:
- [AutoGen v0.4 (Microsoft Research)](https://www.microsoft.com/en-us/research/articles/autogen-v0-4-reimagining-the-foundation-of-agentic-ai-for-scale-extensibility-and-robustness/) Isolamento de falhas de modelo de actor
  Tradução do português:
